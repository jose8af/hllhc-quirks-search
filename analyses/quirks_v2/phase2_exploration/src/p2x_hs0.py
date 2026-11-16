"""p2x_hs0.py -- pilot no-pile-up hard-scatter events (Z(nunu)+jets pilot of STR §4.7, addendum 1 v2 P1).

  <acts python> p2x_hs0.py <sample> <out.npz> <n_events> <stream> <chunk>

Generator, filter, chain, seeds and every array of Tatiana's p2c_hs0.py (imported, not modified; same event seeds
s4pu.hseed('sm', sample, job_seed, i), so event i of a job is the event p2c_hs0 would make), plus what Phase 3 needs
and p2c_hs0 does not store:
  gsum (n_ev, len(GSUM_COLS))   generator-level sums of the visible final state (no neutrinos) for a reconstruction-
                                level MET model (STR §4.7): scalar sum pT, vector sum px, py in |eta| < 5 and < 3;
                                the same as scalar E_T sums; numbers of charged
                                particles, jets, tau_h; pT-hat and the generator weight of the event
  jets10 (J, 4), jets10_off     SlowJet anti-kT 0.4 on the visible final state, pT > 10 GeV, |eta| < 5: pT, eta, phi, m
  tau (T, 8), tau_off           every decayed tau: pdg, pT, eta, phi of the tau; visible pT, eta, phi of its decay
                                products (neutrinos removed); hadronic flag
  had (H, 6), had_off           final hadrons and photons of the hard scatter with |eta| < 1.5, pT > 0.3 GeV: pdg, pT, eta,
                                phi, production radius and z (review of addendum v2, C-8: also the parent pool of a
                                hard-scatter single-interaction sample, with the event's own road in `evt`)
  nu (N, 4), nu_off             every final neutrino: pdg, pT, eta, phi
  part (K, len(PART_COLS)), part_off   truth table of the generated particles that own at least one WRITTEN hit
                                (barcode vsec, particle -> pdg, charge, pT, eta, phi, production point and time, mother
                                pdg), so that own-hit candidates can be attributed to prompt pairs / conversions
                                (hits with gen >= 1 of a photon row) / V0 (vsec >= 1) without the generator record
The truth MET vector, tries, sigma_gen, the hard-scatter vertex, v1's preselection weight and flags, jets (pT > 20),
leptons and photons are in `evt`, `jets`, `lep` as in p2c_hs0.  No per-rung quantity is computed.
"""
import json
import math
import shutil
import sys
import tempfile
import time

import numpy as np

import p2c_common as C
import p2c_hs0 as H0
import p2x_common as X

rc = H0.rc
s4pu = H0.s4pu
pythia8 = H0.pythia8
gen_d123 = H0.gen_d123

log = C.setup_logging('p2x_hs0')
EVT_COLS = H0.EVT_COLS
GSUM_COLS = ['sumpt_eta5', 'px_eta5', 'py_eta5', 'sumpt_eta3', 'px_eta3', 'py_eta3', 'n_ch_pt05_eta25', 'n_final_vis',
             'n_jets10', 'n_tau', 'n_tau_had', 'sumet_eta5', 'sumet_eta3', 'pthat', 'gen_weight', 'n_nu', 'n_had']
HAD_COLS = ['pdg', 'pt', 'eta', 'phi', 'r_prod', 'z_prod']      # final hadrons and photons, |eta| < 1.5, pT > 0.3 GeV
NU_COLS = ['pdg', 'pt', 'eta', 'phi']
HAD_ETA, HAD_PT = 1.5, 0.3
PART_COLS = ['vsec', 'particle', 'pdg', 'q', 'pt', 'eta', 'phi', 'x', 'y', 'z', 't', 'mother_pdg', 'n_hits']
MAX_REPLACE = H0.MAX_REPLACE


def extra_summary(py, sj10):
    ev = py.event
    s5 = [0.0, 0.0, 0.0]; s3 = [0.0, 0.0, 0.0]; nch = 0; nvis = 0; et5 = 0.0; et3 = 0.0
    mother = {}; had = []; nus = []
    for k in range(ev.size()):
        p = ev[k]
        if not p.isFinal():
            continue
        m1 = p.mother1()
        mother[(p.id(), p.px(), p.py(), p.pz())] = ev[m1].id() if m1 > 0 else 0
        if p.idAbs() in (12, 14, 16):
            nus.append((p.id(), p.pT(), p.eta(), p.phi()))
            continue
        nvis += 1
        ae = abs(p.eta()); pt = p.pT()
        et = p.e() * pt / p.pAbs() if p.pAbs() > 0 else 0.0
        if ae < 5.0:
            s5[0] += pt; s5[1] += p.px(); s5[2] += p.py(); et5 += et
        if ae < 3.0:
            s3[0] += pt; s3[1] += p.px(); s3[2] += p.py(); et3 += et
        if ae < HAD_ETA and pt > HAD_PT and (p.idAbs() > 100 or p.id() == 22):
            had.append((p.id(), pt, p.eta(), p.phi(), math.hypot(p.xProd(), p.yProd()), p.zProd()))
        if p.charge() != 0 and pt > 0.5 and ae < 2.5:
            nch += 1
    sj10.analyze(ev)
    jets = [(sj10.pT(i), sj10.p(i).eta(), sj10.phi(i), sj10.m(i)) for i in range(sj10.sizeJet())]
    taus = []
    for k in range(ev.size()):
        p = ev[k]
        if p.idAbs() != 15 or p.daughter1() <= 0 or ev[p.daughter1()].idAbs() == 15:
            continue
        ds = [ev[j].idAbs() for j in range(p.daughter1(), p.daughter2() + 1)]
        is_had = 0.0 if any(x in (11, 13) for x in ds) else 1.0
        vx = vy = vz = 0.0
        for j in p.daughterListRecursive():
            d = ev[j]
            if d.isFinal() and d.idAbs() not in (12, 14, 16):
                vx += d.px(); vy += d.py(); vz += d.pz()
        vpt = math.hypot(vx, vy)
        taus.append((p.id(), p.pT(), p.eta(), p.phi(), vpt, math.asinh(vz / vpt) if vpt > 0 else 0.0, math.atan2(vy, vx), is_had))
    info = py.infoPython()
    gs = (*s5, *s3, nch, nvis, len(jets), len(taus), sum(t[7] for t in taus), et5, et3, info.pTHat(), info.weight(),
          len(nus), len(had))
    return gs, jets, taus, mother, had, nus


def particle_table(P, mother):
    """Compact float32 table of the Fatras input rows (s4pu.PCOLS) with the barcode numbering of run_chain.ParticleSource
    (particle = running count per (vp, vsec), from 1)."""
    cnt = {}
    out = np.zeros((len(P), len(PART_COLS)), np.float32)
    for r, row in enumerate(P.tolist()):
        vp, vsec, pdg, q, m, x, y, z, t, px, py, pz = row
        key = (int(vp), int(vsec)); k = cnt.get(key, 0) + 1; cnt[key] = k
        pt = math.hypot(px, py)
        out[r] = (vsec, k, pdg, q, pt, math.asinh(pz / pt) if pt > 0 else 0.0, math.atan2(py, px), x, y, z, t,
                  mother.get((int(pdg), px, py, pz), 0), 0)
    return out


def run(sample, out, n_events, stream, chunk):
    t_start = time.time()
    job_seed = C.qv2_seed(stream, chunk)
    if sample in H0.FORCED_TT:
        s4pu.SM_SAMPLES[sample] = (H0.FORCED_TT[sample], 150.0)
    scratch = tempfile.mkdtemp(prefix='p2x_hs0_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        sm = s4pu.SMEvent(rc.CP5, s4pu.load_beamspot(rc.TT), sample, mu=0.0, tt=rc.TT)
        sj20 = pythia8.SlowJet(-1, 0.4, 20.0, 4.7, 2, 1)
        sj10 = pythia8.SlowJet(-1, 0.4, 10.0, 5.0, 2, 1)
        sj30 = gen_d123.slowjet()
        ev_seeds = [s4pu.hseed('sm', sample, job_seed, i, mod=2 ** 62) for i in range(n_events)]
        replaced = []
        while True:
            store = {}; gen = {}; ext = {}
            rc.TIMES.clear()

            def provider(i):
                P, vz, info = sm.event(ev_seeds[i])
                py = sm.hs.gen.py
                gen[i] = H0.gen_summary(py, info['hs_met'], sample, ev_seeds[i], sj20, sj30) + (info,)
                gs, j10, taus, mother, had, nus = extra_summary(py, sj10)
                ext[i] = (gs, j10, taus, particle_table(P, mother), np.array(had, np.float32).reshape(-1, len(HAD_COLS)),
                          np.array(nus, np.float32).reshape(-1, len(NU_COLS)))
                return P, vz, info
            s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True)
            try:
                s.run()
                break
            except RuntimeError as exc:      # v1 G1b rule, as p2c_hs0: replace the event that hit the navigation assertion
                k = next((i for i in range(n_events) if 'ev' not in store.get(i, {})), None)
                if rc.NAV_ERR not in str(exc) or k is None or len(replaced) >= MAX_REPLACE:
                    raise
                old = ev_seeds[k]
                ev_seeds[k] = s4pu.hseed('nav-replace', 'p2c-hs0', job_seed, k, old, mod=2 ** 62)
                replaced.append(dict(event=k, old_seed=old, new_seed=ev_seeds[k]))
                log.warning('navigation assertion in event %d: job rerun with that event replaced', k)
        v41 = np.zeros((n_events, len(rc.V41_COLS))); tim = np.zeros((n_events, len(rc.T_COLS)))
        st = {}
        for e, nm, t in rc.TIMES:
            st.setdefault(e, {})[nm] = t
        evt = np.zeros((n_events, len(EVT_COLS))); gsum = np.zeros((n_events, len(GSUM_COLS)))
        hits = []; tru = []; vzs = []; jets = []; leps = []; j10s = []; taus = []; parts = []; hads = []; nul = []
        col = {k: i for i, k in enumerate(rc.COLS)}
        n_hit_nopart = 0
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
            gs, j10, tt, ptab, had, nus = ext[i]
            hads.append(had); nul.append(nus)
            gsum[i] = gs
            # particles with written hits: key (vsec, particle) of the hit barcode -> row of the table
            if len(ev):
                key_h = ev[:, col['vsec']].astype(np.int64) * 100000 + ev[:, col['particle']].astype(np.int64)
                key_p = ptab[:, 0].astype(np.int64) * 100000 + ptab[:, 1].astype(np.int64)
                uk, cnt = np.unique(key_h, return_counts=True)
                pos = {int(k): n for n, k in enumerate(key_p)}
                rows = [pos[int(k)] for k in uk if int(k) in pos]
                n_hit_nopart += int(sum(c for k, c in zip(uk, cnt) if int(k) not in pos))
                sel = ptab[rows]
                sel[:, -1] = [c for k, c in zip(uk, cnt) if int(k) in pos]
            else:
                sel = ptab[:0]
            hits.append(ev); tru.append(r['tru']); vzs.append(r['vz']); jets.append(jj); leps.append(ll)
            j10s.append(j10); taus.append(tt); parts.append(sel)
        Hh, hoff = C.concat(hits, len(rc.COLS), np.float32)
        T, _ = C.concat(tru, 3, np.float32)
        V, voff = C.concat(vzs, 8, np.float64)
        J, joff = C.concat(jets, 4, np.float32)
        L, loff = C.concat(leps, 6, np.float32)
        J10, j10off = C.concat(j10s, 4, np.float32)
        TA, taoff = C.concat(taus, 8, np.float32)
        PT, ptoff = C.concat(parts, len(PART_COLS), np.float32)
        HD, hdoff = C.concat(hads, len(HAD_COLS), np.float32)
        NU, nuoff = C.concat(nul, len(NU_COLS), np.float32)
        v41_pass = bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                        and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0])))
        w = evt[:, EVT_COLS.index('w_v1')]
        meta = dict(mode='hs0x', sample=sample, stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events,
                    mu=0.0, chain=rc.CHAIN, columns=rc.COLS, v41_cols=rc.V41_COLS, timing_cols=rc.T_COLS,
                    evt_cols=EVT_COLS, gsum_cols=GSUM_COLS, part_cols=PART_COLS, had_cols=HAD_COLS, nu_cols=NU_COLS,
                    had_selection=dict(abs_eta_max=HAD_ETA, pt_min=HAD_PT, what='final hadrons (|id| > 100) and photons'), jet_cols=['pt', 'eta', 'phi', 'm'],
                    lep_cols=['pdg', 'pt', 'eta', 'phi', 'iso_dr03', 'prompt'],
                    tau_cols=['pdg', 'pt', 'eta', 'phi', 'vis_pt', 'vis_eta', 'vis_phi', 'hadronic'], replaced_events=replaced,
                    v41_pass=v41_pass, n_lost_simhits=int(np.sum(v41[:, 0] - v41[:, 1])),
                    n_hits_without_particle_row=n_hit_nopart,
                    sum_w_v1=float(w.sum()), sum_w2_v1=float((w ** 2).sum()), n_w_v1_positive=int((w > 0).sum()),
                    code_sha256=dict(C.code_hashes([C.ANA / 'gen_d123.py']),
                                     **X.src_hashes('p2x_hs0.py', 'p2x_common.py', 'p2c_hs0.py', 'p2c_common.py')),
                    input_sha256=X.input_hashes(),
                    pythia=str(pythia8.__version__) if hasattr(pythia8, '__version__') else '8.312',
                    generator=dict(lines=s4pu.SM_SAMPLES[sample][0], pthat_min=s4pu.SM_SAMPLES[sample][1],
                                   met_min=s4pu.MET_MIN, pre_met=s4pu.PRE_MET),
                    t_total_s=round(time.time() - t_start, 3),
                    mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(rc.T_COLS)},
                    sum_tries=int(evt[:, 2].sum()), n_hits=int(len(Hh)), n_ckf_tracks=int(v41[:, 10].sum()),
                    n_part_rows=int(len(PT)))
        arrays = dict(hits=Hh, hit_off=hoff, tru=T, vz=V, vz_off=voff, v41=v41, timing=tim, evt=evt, jets=J, jet_off=joff,
                      lep=L, lep_off=loff, gsum=gsum, jets10=J10, jets10_off=j10off, tau=TA, tau_off=taoff, part=PT,
                      part_off=ptoff, had=HD, had_off=hdoff, nu=NU, nu_off=nuoff)
        X.save(out, arrays, meta)
        X.write_sha(str(out) + '.sha.json', dict(job=dict(sample=sample, stream=stream, chunk=chunk, job_seed=job_seed,
                                                          n_events=n_events),
                                                 files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
        log.info(json.dumps({k: meta[k] for k in ('sample', 'n_events', 't_total_s', 'v41_pass', 'mean_s_per_event',
                                                  'sum_tries', 'n_hits', 'n_part_rows', 'n_hits_without_particle_row',
                                                  'bytes', 'content_sha256')}))
        return meta
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]))
