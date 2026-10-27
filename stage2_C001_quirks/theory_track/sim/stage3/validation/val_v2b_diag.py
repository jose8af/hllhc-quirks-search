"""val_v2b_diag.py -- DIAGNOSTIC after the V2b gate failure (does NOT change the gate or its criteria).

Question: is the population-median excess of the measured c (V2b, max_boost 1e-3) a step-size effect?
Same 300 events, same selection and observable as V2b (P1 inputs F_m500_p1 / S_m500_p1, |eta| < 1, vertex at the origin,
B and B0/2, no material, ds on the virtual T3 barrel layers), Lambda = 1 keV, max_boost 1e-4 (10x finer; hmax 0.2 cm).
Reports the same statistics as V2b (median c2 - median c_ev with bootstrap sigma; paired median) and the per-event
change of c2 between 1e-3 (V2b production outputs) and 1e-4.
Output: sim/stage3/results/V2b_diag.json.  Run: nice pixi run python sim/stage3/validation/val_v2b_diag.py
"""
import glob
import json
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import vcommon as V


def job(a):
    spin, m, i, p1, p2 = a
    from T3_causal_s3 import run_causal_s3, load_surfaces
    from s3_physics import plane_fit
    S = load_surfaces(); t3v = [k for k, kd in enumerate(S['kinds']) if kd == 'T3V']
    ds = []
    for f in (1.0, 0.5):
        r = run_causal_s3(p1, p2, float(m), 1.0, B0=V.B0 * f, material=False, max_boost=1e-4)
        h = r['hits']; h = h[np.isin(h[:, 1], t3v)]
        ds.append(plane_fit(h[:, 4:7])[0] * 1e4)
    return spin, m, i, ds


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    V.add_orig_code_path()
    from c06_rotating_yoyo import pair_params, K_of
    T = []
    for spin, m in (('F', 500), ('S', 500)):
        z = np.load(V.TT / 'data' / 'sim_stage3' / 'inputs' / f'{spin}_m{m}_p1.npz')
        T += [(spin, m, i, z['p_qp'][i], z['p_qm'][i]) for i in range(300)]
    tic = time.time()
    with ProcessPoolExecutor(7) as ex:
        R = list(ex.map(job, T, chunksize=4))
    out = dict(wall_s=time.time() - tic, points={})
    rng = np.random.default_rng(12345)
    for spin, m in (('F', 500), ('S', 500)):
        rr = sorted([r for r in R if r[0] == spin], key=lambda r: r[2])
        d4 = np.array([r[3] for r in rr])
        c4 = (2 * d4[:, 1] / d4[:, 0] - 1) / np.log(2)
        # V2b (1e-3) production values on the same events
        b = {}; h = {}
        for cfg, D in (('B', b), ('B2', h)):
            for f in glob.glob(str(V.TT / 'data' / 'sim_stage3' / 'out' / 'p1' / f'{spin}_m{m}' / f'L1_{cfg}_c*.npz')):
                zz = np.load(f)
                for e, d in zip(zz['ev_index'], zz['ds_barrel_um']):
                    D[int(e)] = d
        c3 = np.array([(2 * h[i] / b[i] - 1) / np.log(2) for i in range(300)])
        z = np.load(V.TT / 'data' / 'sim_stage3' / 'inputs' / f'{spin}_m{m}_p1.npz')
        cev = np.array([1.0 / (pp['L'] + K_of(pp['gs'])) for pp in (pair_params(z['p_qp'][i], z['p_qm'][i], float(m), 1.0) for i in range(300))])
        ok = np.isfinite(c4) & np.isfinite(c3)
        boots = []
        for _ in range(2000):
            k = rng.integers(0, ok.sum(), ok.sum())
            boots.append(np.median(c4[ok][k]) - np.median(cev[ok][k]))
        dc = float(np.median(c4[ok]) - np.median(cev[ok]))
        out['points'][f'{spin}_m{m}'] = {
            'n': int(ok.sum()), 'median_c2_mb1e-4': float(np.median(c4[ok])), 'median_c2_mb1e-3': float(np.median(c3[ok])),
            'median_c_ev': float(np.median(cev[ok])), 'Dc_mb1e-4': dc, 'sigma': float(np.std(boots)),
            'rel_mb1e-4': dc / float(np.median(cev[ok])), 'paired_median_c2_minus_cev_mb1e-4': float(np.median((c4 - cev)[ok])),
            'median_c2_change_1e-4_minus_1e-3': float(np.median((c4 - c3)[ok])),
            'median_dsB_rel_change_1e-4_vs_1e-3': float(np.median(d4[ok, 0] / np.array([b[i] for i in range(300)])[ok] - 1))}
    V.dump('V2b_diag.json', out)
    print(json.dumps(out, indent=1))
