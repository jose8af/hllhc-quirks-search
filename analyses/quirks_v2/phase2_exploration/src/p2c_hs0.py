"""p2c_hs0.py -- no-pile-up SM hard-scatter events through the chain (Phase 2 channel (iii); pilot of STR §4.7).

  <acts python> p2c_hs0.py <sample> <out.npz> <n_events> <stream> <chunk>

Generator: s4pu.HardScatter unchanged (Pythia 8 CP5, 14 TeV, pT-hat > 150 GeV, MPI + hadronisation, truth MET(nu) >
200 GeV filter), no pile-up (s4pu.SMEvent with mu = 0).  Chain: run_chain.build_sequencer unchanged (Fatras,
smearing digitisation, GridTriplet seeding, CKF).  Seeds: job seed = blake2b("qv2|stream|chunk"); event seeds
s4pu.hseed('sm', sample, job_seed, i) as run_chain's 'sm' mode.

Output (p2c_common layout) plus the generator-level summary per event:
  evt (n_ev, len(EVT_COLS))   see EVT_COLS; w_v1 and the *_v1 columns are v1's generator-level preselection
                              (gen_d123.presel, unchanged), stored as a labelled v1 quantity
  jets (J, 4), jet_off        SlowJet anti-kT R = 0.4 on the visible final state, pT > 20 GeV, |eta| < 4.7: pT, eta, phi, m
  lep (L, 6), lep_off         final e, mu (pT > 5) and gamma (pT > 10), |eta| < 5: pdg, pT, eta, phi, iso(dR<0.3), prompt
No per-rung quantity is computed here: the pilot is classified in Phase 3.
"""
import json
import math
import shutil
import sys
import tempfile
import time

import numpy as np

import signal  # noqa: F401  (stdlib module, imported before acts/stage4/analysis/signal.py can shadow it)
import subprocess  # noqa: F401

import p2c_common as C

sys.path.insert(0, str(C.CODE))
sys.path.insert(0, str(C.ANA))
import run_chain as rc  # noqa: E402
import s4pu  # noqa: E402
import gen_d123  # noqa: E402
import pythia8  # noqa: E402

log = C.setup_logging('p2c_hs0')
EVT_COLS = ['met_x', 'met_y', 'hs_tries', 'sigma_gen_mb', 'vtx_x', 'vtx_y', 'vtx_z', 'vtx_t', 'n_hs_particles',
            'w_v1', 'met_reco_v1', 'phimet_reco_v1', 'eps_trig_v1', 'met250_v1', 'jet100_v1', 'mindphi_v1', 'n_veto_v1',
            'ev_seed_lo', 'ev_seed_hi']
MAX_REPLACE = 5
# tt-bar with forced decays (addendum 1 §3.3): the two charge-conjugate halves of "exactly one W -> l nu".  Injected at
# run time (as gen_d123.EXTRA does); acts/stage4/code/s4pu.py itself is not edited (see CHAIN_PROVENANCE.md).
TT = s4pu.SM_SAMPLES['ttbar_1l'][0]
FORCED_TT = {'ttbar_1l_pos': TT + ["24:onMode = off", "24:onPosIfAny = 11 13 15", "24:onNegIfAny = 1 2 3 4 5"],
             'ttbar_1l_neg': TT + ["24:onMode = off", "24:onNegIfAny = 11 13 15", "24:onPosIfAny = 1 2 3 4 5"]}


def gen_summary(py, met, sample, ev_seed, sj20, sj30):
    ev = py.event
    rng = np.random.default_rng(s4pu.hseed('p2c-presel', sample, ev_seed, mod=2 ** 62))
    w, det, phm = gen_d123.presel(ev, met, rng, sj30)
    sj20.analyze(ev)
    jets = [(sj20.pT(i), sj20.p(i).eta(), sj20.phi(i), sj20.m(i)) for i in range(sj20.sizeJet())]
    vis = [(ev[k].pT(), ev[k].eta(), ev[k].phi()) for k in range(ev.size())
           if ev[k].isFinal() and ev[k].idAbs() not in (12, 14, 16)]
    lep = []
    for k in range(ev.size()):
        p = ev[k]
        if not p.isFinal():
            continue
        a = p.idAbs()
        if a not in (11, 13, 22) or abs(p.eta()) > 5.0 or p.pT() < (10.0 if a == 22 else 5.0):
            continue
        iso = sum(q[0] for q in vis if 0 < math.hypot(q[1] - p.eta(), gen_d123.dphi(q[2], p.phi())) < 0.3)
        lep.append((p.id(), p.pT(), p.eta(), p.phi(), iso, 0.0 if gen_d123.hadron_ancestor(ev, k) else 1.0))
    return w, det, phm, jets, lep


def run(sample, out, n_events, stream, chunk):
    t_start = time.time()
    job_seed = C.qv2_seed(stream, chunk)
    if sample in FORCED_TT:
        s4pu.SM_SAMPLES[sample] = (FORCED_TT[sample], 150.0)
    scratch = tempfile.mkdtemp(prefix='p2c_hs0_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        sm = s4pu.SMEvent(rc.CP5, s4pu.load_beamspot(rc.TT), sample, mu=0.0, tt=rc.TT)
        sj20 = pythia8.SlowJet(-1, 0.4, 20.0, 4.7, 2, 1)
        sj30 = gen_d123.slowjet()
        ev_seeds = [s4pu.hseed('sm', sample, job_seed, i, mod=2 ** 62) for i in range(n_events)]
        replaced = []
        while True:
            store = {}; gen = {}
            rc.TIMES.clear()

            def provider(i):
                P, vz, info = sm.event(ev_seeds[i])
                gen[i] = gen_summary(sm.hs.gen.py, info['hs_met'], sample, ev_seeds[i], sj20, sj30) + (info,)
                return P, vz, info
            s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True)
            try:
                s.run()
                break
            except RuntimeError as exc:      # v1 G1b rule: replace the event that hit the ACTS navigation assertion
                k = next((i for i in range(n_events) if 'ev' not in store.get(i, {})), None)
                if rc.NAV_ERR not in str(exc) or k is None or len(replaced) >= MAX_REPLACE:
                    raise
                old = ev_seeds[k]
                ev_seeds[k] = s4pu.hseed('nav-replace', 'p2c-hs0', job_seed, k, old, mod=2 ** 62)
                replaced.append(dict(event=k, old_seed=old, new_seed=ev_seeds[k]))
                log.warning('navigation assertion in event %d: job rerun with that event replaced', k)
        # ---- per-event records (v41 and timing as run_chain.finish)
        v41 = np.zeros((n_events, len(rc.V41_COLS))); tim = np.zeros((n_events, len(rc.T_COLS)))
        st = {}
        for e, nm, t in rc.TIMES:
            st.setdefault(e, {})[nm] = t
        evt = np.zeros((n_events, len(EVT_COLS)))
        hits = []; tru = []; vzs = []; jets = []; leps = []
        for i in range(n_events):
            r = store[i]; ev = r['ev']
            v41[i] = (r['nh'], r['nm'], r['nmap'], r['bij'], r['nunm'], len(ev), r['onsurf'], 0, 0, 0, r['ntr'],
                      r['nckf'], r['n_in'])
            x = st.get(i, {})
            t2 = x.get('t2_digi', 0.0); t3 = x.get('t3_seed', t2); t4 = x.get('t4_ckf', t3)
            tim[i] = (r['t_gen'], r['t_source'], t2 - x.get('t1_source', t2), t3 - t2, t4 - t3, r['t_dump'])
            w, det, phm, jj, ll, info = gen[i]
            evt[i] = (info['hs_met'][0], info['hs_met'][1], info['hs_tries'], info['hs_sigma_gen_mb'], *info['hs_vtx'],
                      info['n_hs'], w, det['met_reco'], phm, det['eps_trig'], det['met250'], det['jet100'],
                      det['mindphi'], det['n_veto'], ev_seeds[i] % 2 ** 31, ev_seeds[i] // 2 ** 31)
            hits.append(ev); tru.append(r['tru']); vzs.append(r['vz']); jets.append(jj); leps.append(ll)
        H, hoff = C.concat(hits, len(rc.COLS), np.float32)
        T, _ = C.concat(tru, 3, np.float32)
        V, voff = C.concat(vzs, 8, np.float64)
        J, joff = C.concat(jets, 4, np.float32)
        L, loff = C.concat(leps, 6, np.float32)
        v41_pass = bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                        and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0])))
        meta = dict(mode='hs0', sample=sample, stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events,
                    mu=0.0, chain=rc.CHAIN, columns=rc.COLS, v41_cols=rc.V41_COLS, timing_cols=rc.T_COLS,
                    evt_cols=EVT_COLS, jet_cols=['pt', 'eta', 'phi', 'm'],
                    lep_cols=['pdg', 'pt', 'eta', 'phi', 'iso_dr03', 'prompt'], replaced_events=replaced,
                    v41_pass=v41_pass, n_lost_simhits=int(np.sum(v41[:, 0] - v41[:, 1])),
                    code_sha256=C.code_hashes([C.ANA / 'gen_d123.py', __file__, C.HERE / 'p2c_common.py']),
                    pythia=str(pythia8.__version__) if hasattr(pythia8, '__version__') else '8.312',
                    generator=dict(lines=s4pu.SM_SAMPLES[sample][0], pthat_min=s4pu.SM_SAMPLES[sample][1],
                                   met_min=s4pu.MET_MIN, pre_met=s4pu.PRE_MET),
                    t_total_s=round(time.time() - t_start, 3),
                    mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(rc.T_COLS)},
                    sum_tries=int(evt[:, 2].sum()), n_hits=int(len(H)), n_ckf_tracks=int(v41[:, 10].sum()))
        nbytes = C.save_job(out, dict(hits=H, hit_off=hoff, tru=T, vz=V, vz_off=voff, v41=v41, timing=tim, evt=evt,
                                      jets=J, jet_off=joff, lep=L, lep_off=loff), meta)
        meta['bytes'] = nbytes
        log.info(json.dumps({k: meta[k] for k in ('sample', 'n_events', 't_total_s', 'v41_pass', 'mean_s_per_event',
                                                  'sum_tries', 'n_hits', 'bytes')}))
        return meta
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]))
