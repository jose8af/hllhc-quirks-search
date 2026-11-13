"""val_v5.py -- Stage-3 validation V5 (plan §5): continuity with the old T2-cache results (figures/T3_ms_thickness.npy,
made by code/T3_ms_thickness.py: B, B+E, B+M, M; 200/500/1000 GeV; 0.3/1/3/10/30 keV; 60 events at 0.3-3 keV, 24 at
10 keV, 12 at 30 keV; T2-cache sample sample_events(m, 60, default_rng(2026) shared over the masses, eta_max=1); seeds
1000 + k; T3_causal.run_causal defaults; material phase2_tracker(1)).

(a) The same events through the Stage-3 kernel in legacy mode (T3_causal_s3.run_causal_s3(legacy=True)), observables
    computed exactly as T3_ms_thickness.observables (code/T3_propagator.plane_fit, imported read-only).  CPU budget: a
    subset -- events k < 8 at 0.3/1/3 keV, k < 3 at 10 keV, k < 1 at 30 keV, all 4 configurations, 3 masses (171 x 4
    runs).  PASS: every (Delta_s, max residual, IT+PS Delta_s, n hits) identical to the stored row (bit for bit), and the
    regenerated (pT, gamma*, eta) identical to the stored columns for all 648 rows.
(b) The same observables on the MG sample at matched selection (|eta_pair| < 1, pT > 200 GeV, vertex at the origin; P1
    production: B at max_boost 1e-3, M and BM at 1e-2): median shift MG - cache with bootstrap errors, at 1, 3, 10 keV
    (0.3 and 30 keV have no P1 point).  Expected direction: the MG ISR tail is softer in l_max (-8 ... -26 %, Stage-2
    VALIDATION §3).  Reported, not a pass/fail item.
Output: sim/stage3/results/V5.json.  Run (theory_track/): pixi run python sim/stage3/scripts/val_v5.py
"""
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import s3common as C

MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.3, 1.0, 3.0, 10.0, 30.0]
CFGS = {'B': dict(B0=3.8112, material=False), 'B+E': dict(B0=3.8112, ms=False), 'B+M': dict(B0=3.8112), 'M': dict(B0=0.0)}
NSUB = {0.3: 8, 1.0: 8, 3.0: 8, 10.0: 3, 30.0: 1}


def orig_path():
    for p in (C.TT / 'code',):
        if str(p) not in sys.path:
            sys.path.append(str(p))


def observables(hits, plane_fit):
    H = hits[hits[:, 1] < 10]
    if len(H) < 4:
        return [np.nan, np.nan, np.nan, len(H)]
    d, n = plane_fit(H[:, 3:6])
    res = np.abs(H[:, 3:6] @ n)
    sel = H[:, 1] < 7
    d3 = plane_fit(H[sel, 3:6])[0] if sel.sum() >= 4 else np.nan
    return [d, res.max(), d3, len(H)]


def job(a):
    orig_path()
    from T3_propagator import plane_fit
    from T3_causal_s3 import run_causal_s3, phase2_tracker
    m, lam, k, p1, p2 = a
    out = []
    t0 = time.process_time()
    for name, cfg in CFGS.items():
        r = run_causal_s3(p1, p2, m, lam, slabs=phase2_tracker(1.0), seed=1000 + k, legacy=True, **cfg)
        out += observables(r['hits'], plane_fit)
    return m, lam, k, out, time.process_time() - t0


def boot_med(x, nb=1000, seed=7):
    rng = np.random.default_rng(seed)
    x = x[np.isfinite(x)]
    return float(np.std([np.median(x[rng.integers(0, len(x), len(x))]) for _ in range(nb)]))


def main():
    orig_path()
    from T3_propagator import sample_events
    rows = np.load(C.TT / 'figures' / 'T3_ms_thickness.npy')
    rng = np.random.default_rng(2026)
    evs = {m: sample_events(m, 60, rng=rng, eta_max=1.0) for m in MASSES}
    regen = True
    for r in rows:
        info = evs[r[0]][int(r[2])][2]
        regen &= bool(info['pt'] == r[3] and info['gstar'] == r[4] and info['eta'] == r[5])
    tasks = [(m, lam, k, evs[m][k][0], evs[m][k][1]) for m in MASSES for lam in LAMS for k in range(NSUB[lam])]
    tasks.sort(key=lambda t: -t[1])
    tic = time.time()
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        R = list(ex.map(job, tasks))
    ref = {(r[0], r[1], int(r[2])): r[6:] for r in rows}
    n_id = 0; diffs = []
    for m, lam, k, out, cpu in R:
        a = np.array(out, float); b = np.asarray(ref[(m, lam, k)], float)
        same = np.array_equal(a, b, equal_nan=True)
        n_id += same
        if not same:
            diffs.append(dict(m=m, lam=lam, k=k, max_rel=float(np.nanmax(np.abs(a - b) / np.maximum(np.abs(b), 1e-300)))))
    va = dict(n_rows_regenerated_identical=bool(regen), n_runs=len(R), n_identical=int(n_id), differing=diffs,
              cpu_h=sum(r[4] for r in R) / 3600, wall_s=time.time() - tic, PASS=bool(regen and n_id == len(R)))
    # (b) MG vs cache medians
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    vb = {}
    col = {'B': 6, 'B+M': 14, 'M': 18}
    pcfg = {'B': 'B', 'B+M': 'BM', 'M': 'M'}
    for m in MASSES:
        for lam in (1.0, 3.0, 10.0):
            for cname, ci in col.items():
                kk = f'p1/F_m{int(m)}/L{lam:g}_{pcfg[cname]}'
                if kk not in keys:
                    continue
                sel = (S['point'] == keys.index(kk)) & (S['status'] == 1)
                mg = S['ds_barrel_um'][sel]; mg = mg[np.isfinite(mg)]
                ca = rows[(rows[:, 0] == m) & (rows[:, 1] == lam), ci] * 1e4; ca = ca[np.isfinite(ca)]
                a, ea = float(np.median(mg)), boot_med(mg); b, eb = float(np.median(ca)), boot_med(ca)
                vb[f'm{int(m)}/L{lam:g}/{cname}'] = dict(mg_median_um=a, mg_err=ea, n_mg=len(mg), cache_median_um=b, cache_err=eb,
                                                         n_cache=len(ca), rel_shift=a / b - 1, pull=(a - b) / np.hypot(ea, eb))
    # l_max shift (gamma*): MG P1 events vs cache events
    lsh = {}
    for m in MASSES:
        kk = f'p1/F_m{int(m)}/L1_M'
        sel = S['point'] == keys.index(kk)
        x_mg = 2 * (S['gstar'][sel] - 1)
        x_ca = 2 * (rows[(rows[:, 0] == m) & (rows[:, 1] == 1.0), 4] - 1)
        lsh[f'm{int(m)}'] = dict(median_x_mg=float(np.median(x_mg)), median_x_cache=float(np.median(x_ca)),
                                 rel_shift_lmax=float(np.median(x_mg) / np.median(x_ca) - 1))
    res = dict(a=va, b=dict(note='MG (P1 production) vs T2-cache (T3_ms_thickness) medians, |eta|<1, 10 barrel layers; '
                                 'P1 B runs at max_boost 1e-3 (cache 1e-2: +0.1..+1.6 % step bias on B-only, plan §6.3); '
                                 'P1 has disc material (cache: barrel only), irrelevant at |eta|<1 to first order',
                            medians=vb, lmax_shift_1keV=lsh))
    C.dump('V5.json', res)
    print(json.dumps(va, indent=1))
    for k, v in vb.items():
        print(f"  {k}: MG {v['mg_median_um']:.3g}+-{v['mg_err']:.2g} cache {v['cache_median_um']:.3g}+-{v['cache_err']:.2g} "
              f"shift {100 * v['rel_shift']:+.1f} % ({v['pull']:+.1f} sig)")
    print(lsh)


if __name__ == '__main__':
    main()
