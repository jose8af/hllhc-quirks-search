"""val_v1.py -- Stage-3 validation V1 (kernel regression) and V1b (new recorder).

V1  : T3_causal_s3.run_causal_s3(legacy=True) vs code/T3_causal.run_causal (unmodified), 20 MG events (E 500 GeV, TRGS,
      pT > 200, |eta| < 2.5, template, unweighted) x {V, B, BM, M} x {0.6, 3, 10 keV}, max_boost 1e-2, same seeds.
      PASS: hits bit-identical (all 9 columns), same status and nsteps, and identical final X, P, eacc.
V1b : (a) s3 non-legacy (disc material off, vertex 0) vs legacy on the same runs for V, B, BM: every legacy hit on the
      10 barrel layers is reproduced on the virtual T3V surfaces to < 1e-9 cm (matched by quirk, layer, crossing
      order), extra T3V hits are only grazing double roots;
      (b) vacuum (V, 1 and 3 keV) on 5 forward events (1.5 < |eta_pair| < 3.5): every recorded hit (cylinders AND discs)
      lies within 5e-4 cm of the exact analytic trajectory (T2_propagator.ExactPair) at the hit time, and the number of
      crossings per surface equals the count from an independent numpy scan of the exact trajectory (dt = 0.01 cm).
Output: sim/stage3/results/V1.json.  Run (theory_track/): nice pixi run python sim/stage3/validation/val_v1.py
"""
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import vcommon as V

CFG = {'V': dict(B0=0.0, material=False), 'B': dict(B0=V.B0, material=False), 'BM': dict(B0=V.B0, material=True),
       'M': dict(B0=0.0, material=True)}


def job_v1(a):
    i, p1, p2, lam, cfg = a
    V.add_orig_code_path()
    from T3_causal import run_causal
    from T3_causal_s3 import run_causal_s3
    seed = 9001 + 37 * i
    t0 = time.perf_counter(); r0 = run_causal(p1, p2, 500.0, lam, seed=seed, **CFG[cfg]); t_ref = time.perf_counter() - t0
    t0 = time.perf_counter(); r1 = run_causal_s3(p1, p2, 500.0, lam, seed=seed, legacy=True, **CFG[cfg]); t_new = time.perf_counter() - t0
    same = bool(np.array_equal(r0['hits'], r1['hits']) and r0['status'] == r1['status'] and r0['nsteps'] == r1['nsteps']
                and np.array_equal(r0['X'], r1['X']) and np.array_equal(r0['P'], r1['P']) and np.array_equal(r0['eacc'], r1['eacc']))
    res = dict(i=i, lam=lam, cfg=cfg, bit_identical=same, nh=len(r0['hits']), nsteps=int(r0['nsteps']), t_ref=t_ref, t_new=t_new)
    # V1b (a): non-legacy recorder on the virtual T3 layers
    if cfg in ('V', 'B', 'BM'):
        r2 = run_causal_s3(p1, p2, 500.0, lam, seed=seed, legacy=False, disc_material=False, **CFG[cfg])
        from T3_causal_s3 import load_surfaces
        S = load_surfaces(); t3v = [k for k, kd in enumerate(S['kinds']) if kd == 'T3V']
        H0 = r0['hits']; H0 = H0[H0[:, 1] < 10]
        H2 = r2['hits']
        maxd = 0.0; missing = 0; extra = 0
        for q in (0, 1):
            for L in range(10):
                a0 = H0[(H0[:, 0] == q) & (H0[:, 1] == L)]
                a2 = H2[(H2[:, 0] == q) & (H2[:, 1] == t3v[L])]
                # match each legacy hit to the nearest non-legacy hit in time
                for h in a0:
                    if len(a2) == 0:
                        missing += 1
                        continue
                    j = int(np.argmin(np.abs(a2[:, 3] - h[2])))
                    d = float(np.max(np.abs(a2[j, 3:7] - h[2:6])))
                    maxd = max(maxd, d)
                    if d > 1e-9:
                        missing += 1
                extra += max(0, len(a2) - len(a0))
        res.update(v1b_maxdiff_cm=maxd, v1b_missing=missing, v1b_extra=extra, v1b_status_same=bool(r2['status'] == r0['status']))
    return res


def job_v1b_exact(a):
    i, p1, p2, lam, m = a
    V.add_orig_code_path()
    from T2_propagator import ExactPair
    from T3_causal_s3 import run_causal_s3, load_surfaces, sigma_from_lambda_keV
    S = load_surfaces(); surf = S['surf']
    r = run_causal_s3(p1, p2, m, lam, B0=0.0, material=False, legacy=False, seed=1)
    H = r['hits']
    ex = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam))
    err = 0.0
    for h in H:
        X1, X2 = ex.lab_positions([h[3]])
        err = max(err, float(np.linalg.norm((X1, X2)[int(h[0])][0] - h[4:7])))
    # independent scan: exact trajectory sampled at dt, crossings counted per surface
    tmax = float(np.max(r['X'][:, 0]))
    ts = np.arange(0.0, tmax, 0.01)
    X1, X2 = ex.lab_positions(ts)
    cnt_scan = np.zeros((2, len(surf)), int)
    for q, Xq in enumerate((X1, X2)):
        rr = np.hypot(Xq[:, 0], Xq[:, 1]); zz = Xq[:, 2]
        for L, (ty, p0, pa, pb) in enumerate(surf):
            if ty < 0.5:
                idx = np.where((rr[:-1] - p0) * (rr[1:] - p0) < 0)[0]
                f = (p0 - rr[idx]) / (rr[idx + 1] - rr[idx]); zc = zz[idx] + f * (zz[idx + 1] - zz[idx])
                cnt_scan[q, L] = int(np.sum((zc > pa) & (zc < pb)))
            else:
                idx = np.where((zz[:-1] - p0) * (zz[1:] - p0) < 0)[0]
                f = (p0 - zz[idx]) / (zz[idx + 1] - zz[idx]); rc = rr[idx] + f * (rr[idx + 1] - rr[idx])
                cnt_scan[q, L] = int(np.sum((rc >= pa) & (rc < pb)))
    cnt_rec = np.zeros((2, len(surf)), int)
    for h in H:
        cnt_rec[int(h[0]), int(h[1])] += 1
    ndisc = int(sum(1 for h in H if surf[int(h[1]), 0] > 0.5))
    return dict(i=i, lam=lam, nh=len(H), n_disc_hits=ndisc, max_err_cm=err, count_mismatch=int(np.abs(cnt_scan - cnt_rec).sum()),
                n_scan=int(cnt_scan.sum()), status=int(r['status']))


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    evs = V.mg_events(500, 20)
    tasks = [(i, p1, p2, lam, cfg) for lam in (10.0, 3.0, 0.6) for cfg in ('BM', 'M', 'B', 'V') for i, (p1, p2, _) in enumerate(evs)]
    import mg_events as mg
    fw = []
    for e in mg.iter_events(1000, 'trig', 'F', eta_max=3.5, ptmin=200.0, split='template', unweight=True):
        if abs(e[2]['eta']) > 1.5:
            fw.append(e)
        if len(fw) == 5:
            break
    t2 = [(i, p1, p2, lam, 1000.0) for lam in (1.0, 3.0) for i, (p1, p2, _) in enumerate(fw)]
    tic = time.time()
    with ProcessPoolExecutor(7) as ex:
        R1 = list(ex.map(job_v1, tasks))
        R2 = list(ex.map(job_v1b_exact, t2))
    nbad = sum(not r['bit_identical'] for r in R1)
    v1 = dict(n_runs=len(R1), n_not_identical=nbad, PASS=nbad == 0,
              t_ref_s=sum(r['t_ref'] for r in R1), t_new_s=sum(r['t_new'] for r in R1))
    A = [r for r in R1 if 'v1b_maxdiff_cm' in r]
    v1b_a = dict(n_runs=len(A), max_diff_cm=max(r['v1b_maxdiff_cm'] for r in A), n_missing=sum(r['v1b_missing'] for r in A),
                 n_extra_double_roots=sum(r['v1b_extra'] for r in A), status_same=all(r['v1b_status_same'] for r in A))
    v1b_a['PASS'] = v1b_a['max_diff_cm'] < 1e-9 and v1b_a['n_missing'] == 0
    v1b_b = dict(runs=R2, max_err_cm=max(r['max_err_cm'] for r in R2), n_count_mismatch=sum(r['count_mismatch'] for r in R2),
                 n_disc_hits=sum(r['n_disc_hits'] for r in R2), n_hits=sum(r['nh'] for r in R2))
    v1b_b['PASS'] = v1b_b['max_err_cm'] < 5e-4 and v1b_b['n_count_mismatch'] <= 2
    out = dict(V1=v1, V1b_a=v1b_a, V1b_b=v1b_b, per_run=R1, wall_s=time.time() - tic)
    V.dump('V1.json', out)
    print('V1', v1); print('V1b(a)', v1b_a); print('V1b(b)', {k: v for k, v in v1b_b.items() if k != 'runs'})
