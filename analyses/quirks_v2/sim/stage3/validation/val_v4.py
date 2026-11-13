"""val_v4.py -- Stage-3 validation V4: independent solver cross-check.

code/R1_conformal_ng.run (conformal-gauge delay-ODE NG solver, shares no code with the causal map; read only) vs the
Stage-3 kernel (s3, non-legacy recorder, configuration B: 3.8112 T, no material, max_boost 1e-3 = the P1 B setting,
vertex at the origin) on 10 MG events of the P1 selection (|eta| < 1) at E 500 GeV x {1, 2 keV} and E 1000 GeV x 1 keV;
R1 with N = 256 on all events and N = 1024 on the first 2 of each set.
Hits: the 10 T3 barrel radii.  R1 records every crossing with no z cut, so the T3 z cut (|z| < 20 cm IT, < 120 cm OT)
is applied to the R1 hits; s3 hits are taken from the virtual T3V surfaces (same radii and cuts).
Matching: each R1 hit to the s3 hit of the same (quirk, layer) nearest in lab time.
PASS (S-1 / R1 criteria, plan §5): median per-event Delta_s ratio s3/R1 in 0.99-1.01 and max matched hit distance <= 8 um.
Output: sim/stage3/results/V4.json.  Run: nice pixi run python sim/stage3/validation/val_v4.py
"""
import sys
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import vcommon as V

ZMAX = np.array([20.0] * 4 + [120.0] * 6)


def job(a):
    tag, i, p1, p2, m, lam, N = a
    V.add_orig_code_path()
    import R1_conformal_ng as R1
    from T3_causal_s3 import run_causal_s3, load_surfaces
    from s3_physics import plane_fit
    S = load_surfaces(); t3v = np.array([k for k, kd in enumerate(S['kinds']) if kd == 'T3V'])
    t0 = time.perf_counter()
    hr, canon, nst = R1.run(np.asarray(p1), np.asarray(p2), m, lam, Bz=V.B0, N=N)
    t_r1 = time.perf_counter() - t0
    hr = hr[np.abs(hr[:, 5]) < ZMAX[hr[:, 1].astype(int)]] if len(hr) else hr
    r = run_causal_s3(p1, p2, m, lam, B0=V.B0, material=False, max_boost=1e-3)
    h = r['hits']; h = h[np.isin(h[:, 1], t3v)]
    lay = np.searchsorted(t3v, h[:, 1].astype(int))
    d_r1 = plane_fit(hr[:, 3:6])[0]; d_s3 = plane_fit(h[:, 4:7])[0]
    dmax = 0.0; nmatch = 0
    for q in (0, 1):
        for L in range(10):
            a1 = hr[(hr[:, 0] == q) & (hr[:, 1] == L)]
            a2 = h[(h[:, 0] == q) & (lay == L)]
            for x in a1:
                if len(a2) == 0:
                    continue
                j = int(np.argmin(np.abs(a2[:, 3] - x[2])))
                if abs(a2[j, 3] - x[2]) < 1.0:
                    dmax = max(dmax, float(np.linalg.norm(a2[j, 4:7] - x[3:6]))); nmatch += 1
    return dict(tag=tag, i=i, N=N, lam=lam, m=m, ds_r1_um=d_r1 * 1e4, ds_s3_um=d_s3 * 1e4, ratio=d_s3 / d_r1,
                n_r1=len(hr), n_s3=len(h), n_matched=nmatch, max_dist_um=dmax * 1e4, t_r1=t_r1)


DIAG = len(sys.argv) > 1 and sys.argv[1] == '--diag'      # DIAGNOSTIC (not the V4 test): R1 at N = 1024 and 4096 on all events

if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    tasks = []
    for m, lam in ((500, 1.0), (500, 2.0), (1000, 1.0)):
        z = np.load(V.TT / 'data' / 'sim_stage3' / 'inputs' / f'F_m{m}_p1.npz')
        for i in range(10):
            if DIAG:
                for N in (1024, 4096):
                    tasks.append((f'm{m}_L{lam:g}', i, z['p_qp'][i], z['p_qm'][i], float(m), lam, N))
                continue
            tasks.append((f'm{m}_L{lam:g}', i, z['p_qp'][i], z['p_qm'][i], float(m), lam, 256))
            if i < 2:
                tasks.append((f'm{m}_L{lam:g}', i, z['p_qp'][i], z['p_qm'][i], float(m), lam, 1024))
    tasks.sort(key=lambda t: -t[6])
    tic = time.time()
    with ProcessPoolExecutor(7) as ex:
        R = list(ex.map(job, tasks))
    out = dict(runs=R, wall_s=time.time() - tic, sets={})
    ok_all = True
    for tag in sorted({r['tag'] for r in R}):
        for N in (256, 1024, 4096):
            rr = [r for r in R if r['tag'] == tag and r['N'] == N and np.isfinite(r['ratio'])]
            if not rr:
                continue
            ratios = np.array([r['ratio'] for r in rr])
            s = dict(n=len(rr), median_ratio=float(np.median(ratios)), min_ratio=float(ratios.min()), max_ratio=float(ratios.max()),
                     max_hit_dist_um=float(max(r['max_dist_um'] for r in rr)))
            s['PASS'] = bool(0.99 <= s['median_ratio'] <= 1.01 and s['max_hit_dist_um'] <= 8.0)
            ok_all &= s['PASS'] if N == 256 else True
            s['n_hitcount_equal'] = int(sum(r['n_r1'] == r['n_s3'] for r in rr))
            s['ratios_hitcount_equal'] = [round(r['ratio'], 4) for r in rr if r['n_r1'] == r['n_s3']]
            s['max_dist_um_hitcount_equal'] = [round(r['max_dist_um'], 2) for r in rr if r['n_r1'] == r['n_s3']]
            out['sets'][f'{tag}_N{N}'] = s
    out['PASS'] = bool(ok_all)
    V.dump('V4_diag.json' if DIAG else 'V4.json', out)
    import json
    print(json.dumps(out['sets'], indent=1)); print('V4', 'PASS' if ok_all else 'FAIL')
