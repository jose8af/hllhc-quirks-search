"""p2x_looper_chain.py -- chain file of a PROPER looper gun (orchestrator request 2026-11-16 after the half-turn finding).

  <acts python> p2x_looper_chain.py <out.npz> <n_events> <job_seed> <set: nat|flat> <ev0> <pool: p2x_ht_chain mb file>

One event = one central charged particle below the looping threshold (pT < 0.63 GeV, |eta| < 1) from the primary
vertex.  The particle is NOT given to Fatras (which stops every particle at half a turn): Geant4 (g4hv option
'allx', FTFP_BERT, validated geometry, 3.8 T) tracks it until it decays, interacts, stops, leaves the tracker or
reaches 25 ns (g4hv TMAX, the bunch spacing; the chain itself applies no time window to tracker hits), and EVERY
crossing of a sensitive surface is injected as a SimHit through run_chain.Inject (the path of v1's stored C'0 toy
hits and of the quirk hits), then digitised, seeded and CKF-tracked by the unchanged chain.  Products of a decay or
interaction of the particle are not followed.
Sets:  nat   species, pT and eta of a prompt charged particle of a minimum-bias interaction (drawn from the Fatras
             input table of p2-c-px-ht-mb, rows with vsec = 0, |eta| < 1, pT < 0.63 GeV)
       flat  species and eta as 'nat', pT uniform in 0.1-0.63 GeV
Vertex, stored PV and road as v1's C' guns (s4cp.CPrime.event l.110-116, l.127): luminous-region vertex, PV smeared by
(10, 10, 15) um, phi_MET uniform, particle azimuth = phi_MET + U(-0.1, 0.1) (v1's road draw: ONE road per event, the
one the particle starts in).  Event g = ev0 + i is drawn from hseed('p2x-looper', set, g): independent of the job split.
Output: the format of `run_chain.py cp` (ev<i>, tru<i>, vz<i>, toy<i>, v41, timing, meta with ev_info), so that v1's
run_g1b.run_cp0_job reads it unchanged; plus <out>.truth.npz (per event: particle, end of the Geant4 track, crossings).
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
import p2x_validate as XV

sys.path.insert(0, str(C.CODE))
import run_chain as rc  # noqa: E402
import s4pu  # noqa: E402

log = C.setup_logging('p2x_looper_chain')
PT_LOOP = 0.63
AIM = 0.1
B_T = 3.8112
TCOLS = ['g', 'pdg', 'q', 'm', 'pt', 'eta', 'phi', 'phimet', 'vx', 'vy', 'vz', 'vt', 'end_proc', 'end_t', 'end_r', 'end_z',
         'end_turn', 'n_cross_all', 'n_cross_counting', 'n_cross_counting_after_half_turn', 'n_inj',
         't_first_after_half_turn', 't_median_after_half_turn', 't_last']


def run(out, n, job_seed, kind, ev0, pool_file):
    t0 = time.time()
    z, pm = C.load_job(pool_file)
    P = z['pin']; pc = {k: i for i, k in enumerate(pm['pcols'])}
    pt = np.hypot(P[:, pc['px']], P[:, pc['py']]); eta = np.arcsinh(P[:, pc['pz']] / np.maximum(pt, 1e-12))
    sel = (P[:, pc['q']] != 0) & (P[:, pc['vsec']] == 0) & (np.abs(eta) < 1.0) & (pt < PT_LOOP)
    pool = np.c_[P[sel, pc['pdg']], P[sel, pc['q']], P[sel, pc['m']], pt[sel], eta[sel]]
    n_int = pm['n_events']
    bs = s4pu.load_beamspot(rc.TT)
    sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm'], bs['sigma_t_ps'] * 1e-3])
    ev = []
    for i in range(n):
        g = ev0 + i
        rng = np.random.default_rng(s4pu.hseed('p2x-looper', kind, g, mod=2 ** 63))
        vtx = rng.normal(0, 1, 4) * sig
        pv = vtx[:3] + rng.normal(0, 1, 3) * np.array([0.010, 0.010, 0.015])
        phimet = rng.uniform(-math.pi, math.pi)
        r = pool[int(rng.integers(0, len(pool)))]
        ptv = float(r[3]) if kind == 'nat' else float(rng.uniform(0.1, PT_LOOP))
        phi = phimet + rng.uniform(-AIM, AIM)
        ev.append(dict(g=g, pdg=int(r[0]), q=float(r[1]), m=float(r[2]), pt=ptv, eta=float(r[4]), phi=phi, phimet=phimet,
                       vtx=vtx, pv=pv, p3=np.array([ptv * math.cos(phi), ptv * math.sin(phi), ptv * math.sinh(float(r[4]))])))
    # Geant4: all crossings of every particle
    geom = GV.geom_file()
    fin = Path('prim_lp.txt'); fout = Path('vtx_lp.txt')
    with open(fin, 'w') as fh:
        for i, e in enumerate(ev):
            fh.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (i, e['pdg'], *e['vtx'], *e['p3']))
    kv, _ = GV.run_g4([geom, 'FTFP_BERT', int(job_seed) % (2 ** 31 - 2) + 1, fout, 'prim', fin, 1200.0, 'allx'])
    cross = {i: [] for i in range(n)}; end = {}
    cur = None
    with open(fout) as fh:
        for ln in fh:
            w = ln.split()
            if w[0] == 'V':
                cur = int(w[1]); end[cur] = (w[2], float(w[8]), math.hypot(float(w[5]), float(w[6])), float(w[7]))
            elif w[0] == 'X':
                cross[cur].append((w[1],) + tuple(float(x) for x in w[2:9]))
    fin.unlink(); fout.unlink()
    scratch = tempfile.mkdtemp(prefix='p2x_lp_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        sid_of_name = {s['name']: s['sid'] for s in G['surfs']}
        store = {}; rc.TIMES.clear()
        proc_code = {}
        truth = np.zeros((n, len(TCOLS)))
        inj = {}
        for i, e in enumerate(ev):
            pabs = float(np.linalg.norm(e['p3'])); beta = pabs / math.hypot(pabs, e['m']); rad = e['pt'] / (0.299792458e-3 * B_T)
            turn = lambda t: beta * 299.792458 * (t - e['vtx'][3]) * e['pt'] / pabs / (2 * math.pi * rad)  # noqa: E731
            hl = []; tc = []; nall = 0
            for k, c in enumerate(cross[i]):
                nall += 1
                sid = sid_of_name.get(c[0])
                if sid is None:
                    continue
                en = math.sqrt(c[5] ** 2 + c[6] ** 2 + c[7] ** 2 + e['m'] ** 2)
                p4 = (c[5], c[6], c[7], en)
                hl.append((sid, s4pu.GUN_VP, 1, (c[1], c[2], c[3], c[4]), p4, p4, k, 0, 0, 0))
                if c[0] in XV.BARREL_COUNT:
                    tc.append(c[4])
            inj[i] = hl
            tc = np.array(tc); tn = np.array([turn(t) for t in tc]) if len(tc) else np.zeros(0)
            late = tc[tn > 0.5]
            pr, et, er, ez = end.get(i, ('none', np.nan, np.nan, np.nan))
            truth[i] = (e['g'], e['pdg'], e['q'], e['m'], e['pt'], e['eta'], e['phi'], e['phimet'], *e['vtx'],
                        proc_code.setdefault(pr, len(proc_code)), et, er, ez, turn(et) if np.isfinite(et) else np.nan, nall,
                        len(tc), len(late), len(hl), late.min() if len(late) else np.nan,
                        float(np.median(late)) if len(late) else np.nan, tc.max() if len(tc) else np.nan)

        def provider(i):
            e = ev[i]
            vz = np.array([[s4pu.GUN_VP, *e['vtx'], *e['p3']]])
            return np.zeros((0, 12)), vz, dict(topo='looper', pv=e['pv'].tolist(), phimet=e['phimet'], vtx=e['vtx'].tolist(),
                                               trunc=[], n_particles=0)
        s = rc.build_sequencer(G, n, job_seed, provider, store, inject=rc.Inject(G, lambda i: inj[i], store),
                               with_ckf=True, count_vp={s4pu.GUN_VP}, store_vp={s4pu.GUN_VP})
        s.run()
        meta = dict(mode='cp', topo='looper', job_seed=int(job_seed), looper_set=kind, ev0=ev0, toy_cols=rc.TOY_COLS,
                    pool_file=str(pool_file), pool_rows=int(len(pool)), pool_interactions=int(n_int),
                    loopers_prompt_central_per_mb_interaction=len(pool) / n_int, g4=kv,
                    source='p2x_looper_chain.py: Geant4 crossings injected through run_chain.Inject (no Fatras particle)',
                    code_sha256=C.code_hashes([__file__, C.HERE / 'g4' / 'g4hv.cc']))
        meta['ev_info'] = [{k: v for k, v in store[i]['info'].items()} for i in range(n)]
        meta = rc.finish(out, store, n, meta, t0)
        tmp = Path(str(out) + '.truth.tmp.npz')
        np.savez_compressed(tmp, truth=truth, cols=np.array(TCOLS), proc=np.array(json.dumps(proc_code)),
                            n_meas=np.array(meta['n_meas']), n_written=np.array(meta['n_written']))
        tmp.replace(str(out) + '.truth.npz')
        log.info('%s', json.dumps(dict(set=kind, n=n, v41_pass=meta['v41_pass'], t_total_s=meta['t_total_s'],
                                       mean_s_per_event=meta['mean_s_per_event'], g4_cpu_s=kv.get('event_cpu_s'),
                                       inj_per_event=float(truth[:, TCOLS.index('n_inj')].mean()),
                                       counting_cross_per_event=float(truth[:, TCOLS.index('n_cross_counting')].mean()),
                                       after_half_turn_per_event=float(truth[:, TCOLS.index('n_cross_counting_after_half_turn')].mean()))))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], int(a[1]), int(a[2]), a[3], int(a[4]), a[5])
