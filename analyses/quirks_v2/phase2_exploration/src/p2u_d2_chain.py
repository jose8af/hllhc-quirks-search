"""p2u_d2_chain.py -- D2 robustness row "later arcs restored" (ADD1 v5 §1.5; plan outputs/D2_PLAN_ulrika_2026-11-19.md),
step 1: the varied chain of one nominal C1 pile-up job.

  <acts python> p2u_d2_chain.py <out.npz> <nominal c1pu1-*.npz> [n_events]

For the events of the nominal job (same generator event seeds, read from the nominal file's chain_meta.event_seeds;
same Fatras random seed = the job seed): every charged row given to Fatras is also fired through Geant4 (g4hv option
'allx', as p2x_ht_g4.py), and its Geant4 crossings of sensitive surfaces that are (i) beyond half a turn and (ii) later
than the particle's last Fatras SimHit by more than HybridParent.T_EPS = 0.005 ns are added as SimHits (algorithm
HybridAll, the option-(a) mechanism of p2x_b1.HybridParent applied to every particle), then digitised, seeded and
CKF-tracked by the unchanged chain (run_chain.build_sequencer; no v1 file is changed).

Output (npz, p2c_common.save_job layout): per event i
  inj{i}      written measurements (barrel counting + BTL) of injected SimHits, run_chain.COLS (13), float64
  injtru{i}   their truth positions (float32)
  injturn{i}  Geant4 turn of each of them
and per event the stats `evs` (EVS_COLS), plus meta (checks against the nominal dumps: same written non-injected hits,
CKF-flag changes, V4-1 for injected SimHits).  No selection quantity.
"""
import json
import math
import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

import signal  # noqa: F401
import subprocess  # noqa: F401

import p2c_common as C
import p2c_g4vtx as GV

sys.path.insert(0, str(C.CODE))
import run_chain as rc  # noqa: E402
import s4pu  # noqa: E402

acts = rc.acts
u = rc.u
log = C.setup_logging('p2u_d2_chain')
B_T = 3.8112
T_EPS = 0.005              # ns, the validated seam of p2x_b1.HybridParent.T_EPS (not tuned)
SEAM_DUP = 0.05            # ns: injected crossing on the surface of the last Fatras hit within this window -> counted as seam duplicate
EVS_COLS = ['n_particles', 'n_charged', 'n_g4_cross', 'n_g4_cross_beyond_half', 'n_simhits_fatras', 'n_inj_simhits',
            'n_inj_simhits_written_surf', 'n_inj_meas_written', 'n_inj_nofatras', 'n_time_only_not_injected',
            'n_seam_dup', 'n_early_nofatras_not_injected', 'n_written_nominal_part', 'nominal_match', 'n_ckf_flag_changed', 'n_ckf_tracks', 'v41_ok']


class HybridAll(acts.examples.IAlgorithm):
    """Option (a) for every generation-0 particle: Fatras SimHits kept as they are; the stored Geant4 crossings of the
    particle beyond half a turn that are later than its last Fatras SimHit + T_EPS are added as SimHits (barcode of the
    particle, generation 0, Geant4 position / time / momentum, no deposit).  cross_of(event) -> dict
    key (vp, vsec, particle) -> list of (sid, x, y, z, t, px, py, pz, mass, turn), crossings beyond half a turn only."""

    def __init__(self, G, cross_of, store, early_of):
        acts.examples.IAlgorithm.__init__(self, 'HybridAll', acts.logging.WARNING)
        self.G = G; self.cross_of = cross_of; self.store = store; self.early_of = early_of
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_all')

    def execute(self, ctx):
        cr = self.cross_of(ctx.eventNumber)
        c = acts.examples.SimHitContainer()
        last = {}; nf = 0
        for h in self.inp(ctx.eventStore):
            c.insert(h)
            nf += 1
            b = h.particleId
            if int(b.generation) != 0:
                continue
            key = (int(b.vertexPrimary), int(b.vertexSecondary), int(b.particle))
            t = h.fourPosition[3] / u.ns
            if key not in last or t > last[key][0]:
                last[key] = (t, self.G['geo_sid'].get(h.geometryId.value, -1))
        geo_of = self.G['geo_of']; nphi = self.G['nphi']; tab = self.G['tab']; wsid = self.G['write_sid']
        inj = []; nnof = 0; ndup = 0; nwr = 0
        for key, xs in cr.items():
            tl, sl = last.get(key, (-1e30, -1))
            for x in xs:
                if x[4] <= tl + T_EPS:
                    continue
                sid = int(x[0])
                en = math.sqrt(x[5] ** 2 + x[6] ** 2 + x[7] ** 2 + x[8] ** 2)
                bc = acts.fatras.Barcode(); bc.vertexPrimary = key[0]; bc.vertexSecondary = key[1]; bc.particle = key[2]
                sec = 0 if tab[sid]['kind'] == 'BTL' else rc.s4geo.sector(x[1], x[2], nphi)
                p4 = acts.Vector4(x[5] * u.GeV, x[6] * u.GeV, x[7] * u.GeV, en * u.GeV)
                c.insert(acts.examples.SimHit(geo_of[(sid, sec)], bc, acts.Vector4(x[1] * u.mm, x[2] * u.mm, x[3] * u.mm, x[4] * u.ns),
                                              p4, p4, 200000 + len(inj)))
                inj.append((sid, x[1], x[2], x[3], x[4], x[9]))
                nnof += key not in last
                ndup += (sid == sl and x[4] - tl < SEAM_DUP)
                nwr += sid in wsid
        # diagnostic: Geant4 crossings before half a turn later than the last Fatras SimHit (not injected)
        nto = 0; neo = 0
        for key, ts in self.early_of(ctx.eventNumber).items():
            if key in last:
                nto += int(np.sum(np.asarray(ts) > last[key][0] + T_EPS))
            else:
                neo += len(ts)
        self.store[ctx.eventNumber].update(n_time_only=nto, n_early_nofatras=neo, n_simhits_fatras=nf, inj=np.array(inj, float).reshape(-1, 6), n_inj_nofatras=nnof,
                                           n_seam_dup=ndup, n_inj_written_surf=nwr)
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


def g4_crossings(P_ev, sid_of_name, seed):
    """Fire every charged row of every event through Geant4; return per event {key: [crossings beyond half a turn]}
    and per event (charged, crossings, beyond-half, time-only candidates list for the diagnostic)."""
    pc = {k: i for i, k in enumerate(s4pu.PCOLS)}
    rows = []; keys = []
    for e, P in enumerate(P_ev):
        cnt = {}
        for r in range(len(P)):
            k2 = (int(P[r, pc['vp']]), int(P[r, pc['vsec']])); cnt[k2] = cnt.get(k2, 0) + 1
            if P[r, pc['q']] != 0:
                rows.append((e, r)); keys.append((k2[0], k2[1], cnt[k2]))
    allP = np.array([P_ev[e][r] for e, r in rows]).reshape(-1, 12)
    pt = np.hypot(allP[:, pc['px']], allP[:, pc['py']]); pabs = np.sqrt(pt ** 2 + allP[:, pc['pz']] ** 2)
    beta = pabs / np.hypot(pabs, allP[:, pc['m']]); rad = pt / (0.299792458e-3 * B_T)
    fin = Path('prim_d2.txt'); fout = Path('vtx_d2.txt')
    with open(fin, 'w') as fh:
        for j, r in enumerate(allP):
            fh.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (j, r[pc['pdg']], r[pc['x']], r[pc['y']], r[pc['z']], r[pc['t']],
                                                                    r[pc['px']], r[pc['py']], r[pc['pz']]))
    t0 = time.process_time()
    kv, _ = GV.run_g4([GV.geom_file(), 'FTFP_BERT', int(seed) % (2 ** 31 - 2) + 1, fout, 'prim', fin, 1200.0, 'allx'])
    out = [dict() for _ in P_ev]; early = [dict() for _ in P_ev]; st = np.zeros((len(P_ev), 3))
    cur = None; e = None; key = None; fac = None; t_prod = None; mass = None
    with open(fout) as fh:
        for ln in fh:
            c0 = ln[0]
            if c0 == 'V':
                w = ln.split(); cur = int(w[1]); e = rows[cur][0]; key = keys[cur]
                fac = beta[cur] * 299.792458 * pt[cur] / pabs[cur] / (2 * math.pi * rad[cur])
                t_prod = allP[cur, pc['t']]; mass = allP[cur, pc['m']]
            elif c0 == 'X':
                w = ln.split()
                sid = sid_of_name.get(w[1])
                if sid is None:
                    continue
                x = [float(v) for v in w[2:9]]
                tn = fac * (x[3] - t_prod)
                st[e, 1] += 1
                if tn > 0.5:
                    st[e, 2] += 1
                    out[e].setdefault(key, []).append((sid, *x, mass, tn))
                else:
                    early[e].setdefault(key, []).append(x[3])
    for e, P in enumerate(P_ev):
        st[e, 0] = int(np.sum(P[:, pc['q']] != 0))
    fin.unlink(); fout.unlink()
    return out, early, st, dict(g4_event_cpu_s=float(kv.get('event_cpu_s', 'nan')), g4_wrapper_cpu_s=time.process_time() - t0,
                         n_fired=len(allP))


def run(out, nom_file, n_max=None):
    t0 = time.time()
    zn = np.load(nom_file)
    mn = json.loads(str(zn['meta_json']))
    cm = mn['chain_meta']
    job_seed = int(cm['job_seed']); ev_seeds = [int(x) for x in cm['event_seeds']]
    assert cm.get('replaced_events') is None, 'nominal job has replaced events: not handled'
    n = len(ev_seeds) if not n_max else min(int(n_max), len(ev_seeds))
    scratch = tempfile.mkdtemp(prefix='p2u_d2_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        sid_of_name = {s['name']: s['sid'] for s in G['surfs']}
        mb = s4pu.MinBias(rc.CP5, s4pu.load_beamspot(rc.TT), mu=float(cm.get('mu', 200.0)), tt=rc.TT)
        tg0 = time.time()
        gen = [mb.event(ev_seeds[i]) for i in range(n)]
        t_gen = time.time() - tg0
        tg0 = time.time()
        cross, early, g4st, g4info = g4_crossings([np.asarray(g[0], float).reshape(-1, 12) for g in gen], sid_of_name,
                                           C.qv2_seed('d2.g4', job_seed % 1_000_000_007))
        t_g4 = time.time() - tg0
        store = {}; rc.TIMES.clear()

        def provider(i):
            return gen[i]
        s = rc.build_sequencer(G, n, job_seed, provider, store, inject=HybridAll(G, lambda i: cross[i], store, lambda i: early[i]),
                               with_ckf=True)
        s.run()
        arrays = {}; evs = np.zeros((n, len(EVS_COLS)))
        mism = []
        for i in range(n):
            r = store[i]; ev = r['ev']; tru = r['tru']; inj = r['inj']
            # injected written measurements: truth position equal to an injected SimHit position on the same surface
            ik = {(int(a[0]), np.float32(a[1]), np.float32(a[2]), np.float32(a[3])): a[5] for a in inj}
            isinj = np.zeros(len(ev), bool); turn = np.zeros(len(ev))
            for k in range(len(ev)):
                kk = (int(ev[k, 0]), tru[k, 0], tru[k, 1], tru[k, 2])
                if kk in ik:
                    isinj[k] = True; turn[k] = ik[kk]
            arrays[f'inj{i}'] = ev[isinj]; arrays[f'injtru{i}'] = tru[isinj]; arrays[f'injturn{i}'] = turn[isinj].astype(np.float32)
            # nominal part against the nominal dump of the same event (same truth positions in the same order)
            p = f'dump.{i}_0.'
            dsid = zn[p + 'sid'].astype(np.int64); dtru = zn[p + 'tru']; dflag = zn[p + 'flag'].astype(np.int64)
            evn = ev[~isinj]; trn = tru[~isinj]
            match = bool(len(evn) == len(dsid) and np.array_equal(evn[:, 0].astype(np.int64), dsid)
                         and np.array_equal(trn, dtru.astype(np.float32)))
            nchg = int(np.sum((evn[:, 6].astype(np.int64) & 1) != (dflag & 1))) if match else -1
            if not match:
                mism.append(dict(event=i, n_var_nominal_part=int(len(evn)), n_dump=int(len(dsid))))
            ninj_sim_w = int(r['n_inj_written_surf'])
            v41_ok = bool(r['bij'] == 1 and r['nunm'] == 0 and r['nh'] - r['nm'] <= max(2, 1e-5 * r['nh']))
            evs[i] = (len(gen[i][0]), g4st[i, 0], g4st[i, 1], g4st[i, 2], r['n_simhits_fatras'], len(inj), ninj_sim_w,
                      int(isinj.sum()), r['n_inj_nofatras'], r['n_time_only'], r['n_seam_dup'], r['n_early_nofatras'], len(evn), match, nchg, r['ntr'], v41_ok)
        tim = {}
        for e, nm, t in rc.TIMES:
            tim.setdefault(e, {})[nm] = t
        stage = np.array([[tim[i].get('t2_digi', 0) - tim[i].get('t1_source', 0), tim[i].get('t3_seed', 0) - tim[i].get('t2_digi', 0),
                           tim[i].get('t4_ckf', 0) - tim[i].get('t3_seed', 0), store[i]['t_dump']] for i in range(n)])
        meta = dict(mode='d2-chain', nominal_file=str(nom_file), nominal_job=mn['job'], job_seed=job_seed, n_events=n,
                    event_seeds=ev_seeds[:n], columns=rc.COLS, evs_cols=EVS_COLS, seam_ns=T_EPS, seam_dup_ns=SEAM_DUP,
                    injection_rule='Geant4 crossings with turn > 0.5 and t > last Fatras SimHit of the particle (any surface) + 0.005 ns',
                    nominal_match_all=bool(np.all(evs[:, EVS_COLS.index('nominal_match')] == 1)), nominal_mismatch=mism,
                    n_ckf_flag_changed=int(evs[:, EVS_COLS.index('n_ckf_flag_changed')].sum()),
                    v41_ok_all=bool(np.all(evs[:, EVS_COLS.index('v41_ok')] == 1)),
                    inj_written_meas_vs_simhits=[int(evs[:, 7].sum()), int(evs[:, 6].sum())],
                    t_gen_s=t_gen, t_g4_s=t_g4, g4=g4info, stage_mean_s=dict(zip(['fatras_digi_inject', 'seeding', 'ckf', 'dump'],
                                                                                    stage.mean(0).tolist())),
                    t_total_s=round(time.time() - t0, 2),
                    code_sha256=dict(C.code_hashes(), **{Path(__file__).name: C.sha256_file(__file__)}))
        arrays['evs'] = evs
        C.save_job(out, arrays, meta)
        log.info('%s', json.dumps({k: meta[k] for k in ('n_events', 'nominal_match_all', 'n_ckf_flag_changed', 'v41_ok_all',
                                                        'inj_written_meas_vs_simhits', 't_gen_s', 't_g4_s', 'stage_mean_s',
                                                        't_total_s')}))
        log.info('per event: %s', json.dumps({c: float(evs[:, k].mean()) for k, c in enumerate(EVS_COLS)}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], a[2] if len(a) > 2 else None)
