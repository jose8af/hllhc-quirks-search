"""G2b input: per-set cost of the per-subset chi2_core recomputation (plan §4.1 step 3b) with the numba kernel
kernels.chi2core_subsets, on random samples of the stored rho = 2 sets passing N_IP2 >= 7 (PU-only), and a check
against the numpy proxy of bench_g2a (same definition).  Timing only.
Run (theory_track): pixi run python -m acts.stage4.finder.bench_g2b_core <i0> <i1> [nsamp]
  -> data/acts_stage4/g2/timing_rho2_chi2core.json"""
import json
import sys
import time

import numpy as np

from . import finder as FF
from . import kernels as K
from . import trials as TR
from .bench_g2a import chi2core_subsets as chi2core_np


def prep_set(h, U, X, Y, S0, S1, LC, INTm, n, axis, ttol=0.030):
    n2v = np.cross(n, axis)
    w = U[h] @ n2v
    ip = LC[h] <= 6
    s2 = 3 * np.abs(n2v[2]) * S1[h]
    r = np.hypot(X[h], Y[h]); cx = X[h] / r; cy = Y[h] / r
    a = -n[0] * cy + n[1] * cx
    sg = np.sqrt(np.maximum(np.sqrt(a * a * S0[h] ** 2 + n[2] ** 2 * S1[h] ** 2), 1e-4) ** 2 + ttol ** 2)
    ww = 1.0 / sg ** 2
    u = U[h]
    uu = np.c_[ww * u[:, 0] * u[:, 0], ww * u[:, 0] * u[:, 1], ww * u[:, 0] * u[:, 2], ww * u[:, 1] * u[:, 1],
               ww * u[:, 1] * u[:, 2], ww * u[:, 2] * u[:, 2]]
    ints, hint = np.unique(INTm[h], return_inverse=True)
    return w, ip, s2, np.ascontiguousarray(uu), hint.astype(np.int64), len(ints)


if __name__ == '__main__':
    i0, i1 = int(sys.argv[1]), int(sys.argv[2]); nsamp = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    rows = []
    first = True
    for i in range(i0, i1):
        x = TR.trial_inputs(i, 2)
        r = FF.find(x['H'], x['sid'], x['pv'], x['phimet'], store='loose', want_hits=True, rho=2.0)
        m = r['road_mask']
        U = x['H'][m, 1:4] - x['pv'][None, :]; X = x['H'][m, 1]; Y = x['H'][m, 2]
        S0 = x['H'][m, 4]; S1 = x['H'][m, 5]; LC = FF.LC_OF[x['sid'][m]]; INTm = x['INT'][m]
        s7 = np.where(r['vars']['nip2'] >= 7)[0]
        rng = np.random.default_rng(500 + i)
        samp = rng.choice(s7, min(nsamp, len(s7)), replace=False)
        P = [prep_set(r['hits'][q], U, X, Y, S0, S1, LC, INTm, r['normal'][q], r['axis'][q]) for q in samp]
        if first:
            K.chi2core_subsets(*P[0], 10, 0.5, 1); first = False
        t0 = time.perf_counter()
        for p in P:
            K.chi2core_subsets(*p, 1000, 0.5, 1)
        ms_nb = (time.perf_counter() - t0) / len(P) * 1e3
        # cross-check of the definition vs the numpy proxy on 5 sets (medians of the 1e3-subset distributions)
        chk = []
        for q, p in list(zip(samp, P))[:5]:
            a = K.chi2core_subsets(*p, 1000, 0.5, 3)
            b = chi2core_np(r['hits'][q], U, X, Y, S0, S1, LC, INTm, r['normal'][q], r['axis'][q])
            chk.append([float(np.nanmedian(a)), float(np.nanmedian(b))])
        row = dict(trial=i, n_sets_ip2ge7=int(len(s7)), n_sampled=int(len(samp)), ms_per_set_numba_1e3=round(ms_nb, 3),
                   t_all_ip2ge7_s=round(len(s7) * ms_nb / 1e3, 1), median_check_numba_vs_numpy=chk,
                   mean_hits_per_set=float(np.mean([len(p[0]) for p in P])))
        rows.append(row)
        print(json.dumps(row), flush=True)
    out = dict(rows=rows, ms_per_set_mean=float(np.mean([r_['ms_per_set_numba_1e3'] for r_ in rows])),
               t_all_ip2ge7_mean_s=float(np.mean([r_['t_all_ip2ge7_s'] for r_ in rows])))
    (TR.TT / 'data' / 'acts_stage4' / 'g2' / 'timing_rho2_chi2core.json').write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'}))
