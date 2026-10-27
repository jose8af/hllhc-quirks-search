"""G2a / G2b timing of the production finder on PU-only trials (signal-blind), one process, one thread.

Production configuration: Config() defaults, store='loose' (candidates passing the loosest ladder rung), stored
variables included, the top candidate's thinning weights at rho = 1 (as f1r_finder.trial).  t (wall_s) = the finder
call.  rho = 2: the finder call is t2; the per-set costs of the in-job weights are timed on random samples of NSAMP sets
and extrapolated: the counting-rung thinning weights with the existing 2e4-subset MC (thin_weights), and the per-subset
chi2_core recomputation (plan §4.1 step 3b; 1e3 random interaction subsets at q = 1/2, plane fixed) for the sets
passing N_IP2 >= 7.
Input preparation (PU read + top-up) is NOT part of t (it belongs to the chain, plan §6.1).

Run (theory_track):  nice -n 10 pixi run python -m acts.stage4.finder.bench_g2a <rho> <i0> <i1> [tag]
  -> data/acts_stage4/g2/timing_rho<rho>[_tag].json
"""
import json
import resource
import sys
import time

import numpy as np

from . import finder as FF
NSAMP = 30
from . import trials as TR


def chi2core_subsets(hits_road, U, X, Y, S0, S1, LC, INTm, n, axis, nsub=1000, rng=None):
    """Timing proxy for plan §4.1 step 3b: per-subset re-centred core and chi2_core over nsub random interaction
    subsets (q = 1/2) of one candidate's hit set (plane and axis fixed).  Returns the chi2_core array."""
    rng = rng or np.random.default_rng(1)
    ints, inv = np.unique(INTm[hits_road], return_inverse=True)
    keepI = rng.random((nsub, len(ints))) < 0.5
    keep = keepI[:, inv]                                         # (nsub, nhit)
    n2v = np.cross(n, axis)
    w = U[hits_road] @ n2v
    ip = LC[hits_road] <= 6
    r = np.hypot(X[hits_road], Y[hits_road]); cx = X[hits_road] / r; cy = Y[hits_road] / r
    a = -n[0] * cy + n[1] * cx
    sg = np.sqrt(np.maximum(np.sqrt(a * a * S0[hits_road] ** 2 + n[2] ** 2 * S1[hits_road] ** 2), 1e-4) ** 2 + 0.03 ** 2)
    uu = U[hits_road][:, :, None] * U[hits_road][:, None, :] / (sg ** 2)[:, None, None]   # (nhit, 3, 3)
    wi = np.where(keep & ip[None, :], w[None, :], np.nan)
    c = np.nanmedian(wi, axis=1)
    s = 1.4826 * np.nanmedian(np.abs(wi - c[:, None]), axis=1)
    s2 = np.abs(n2v[2]) * S1[hits_road]
    lo = (c - 2.5 * s)[:, None]; hi = (c + 2.5 * s)[:, None]
    inn = keep & np.where(ip[None, :], (w >= lo) & (w <= hi), (w >= lo - 3 * s2) & (w <= hi + 3 * s2))
    M = np.einsum('sh,hij->sij', inn.astype(float), uu)
    nc = inn.sum(1)
    lam = np.linalg.eigvalsh(M)[:, 0]
    return lam / np.maximum(nc - 2, 1)


def run(rho, i0, i1, cfg=None):
    cfg = cfg or FF.Config()
    rows = []
    t_first = None
    for i in range(i0, i1):
        x = TR.trial_inputs(i, rho)
        if t_first is None:                      # first call: numba cache load (per job, not per trial)
            t0 = time.perf_counter()
            FF.find(x['H'], x['sid'], x['pv'], x['phimet'], cfg=cfg, store='loose')
            t_first = time.perf_counter() - t0
        w0 = time.perf_counter(); c0 = time.process_time()
        # rho = 1: top candidate's thinning weights in the job (as f1r_finder.trial); rho = 2: weights timed below
        r = FF.find(x['H'], x['sid'], x['pv'], x['phimet'], cfg=cfg, INT=x['INT'] if rho == 1 else None,
                    SIG=x['SIG'], rho=float(rho), store='loose', want_hits=(rho > 1))
        t_find = time.perf_counter() - w0
        cpu_find = time.process_time() - c0
        extra = {}
        if rho > 1:
            # per-set costs on random samples (timing only), extrapolated to all sets of the trial
            m = r['road_mask']
            U = x['H'][m, 1:4] - x['pv'][None, :]; X = x['H'][m, 1]; Y = x['H'][m, 2]
            S0 = x['H'][m, 4]; S1 = x['H'][m, 5]; LC = FF.LC_OF[x['sid'][m]]; SD = FF.SIDE_OF[x['sid'][m]]
            INTm = x['INT'][m]
            rng = np.random.default_rng(100 + i)
            nst = len(r['vars']['nl2'])
            samp = rng.choice(nst, min(NSAMP, nst), replace=False)
            tc = time.perf_counter()
            for q in samp:
                FF.thin_weights(r['hits'][q], LC, SD, INTm, 2.0)
            ms_thin = (time.perf_counter() - tc) / max(len(samp), 1) * 1e3
            s7 = np.where(r['vars']['nip2'] >= 7)[0]
            samp7 = rng.choice(s7, min(NSAMP, len(s7)), replace=False) if len(s7) else s7
            tc = time.perf_counter()
            for q in samp7:
                chi2core_subsets(r['hits'][q], U, X, Y, S0, S1, LC, INTm, r['normal'][q], r['axis'][q])
            ms_core = (time.perf_counter() - tc) / max(len(samp7), 1) * 1e3
            ip = r['vars']['nip2']
            extra = dict(n_sets_loose=int(nst), n_sets_ip2ge6=int(np.sum(ip >= 6)), n_sets_ip2ge7=int(len(s7)),
                         ms_per_set_thin_mc2e4=round(ms_thin, 2), ms_per_set_chi2core_1e3sub=round(ms_core, 2),
                         t_chi2core_all_ip2ge7_s=round(len(s7) * ms_core / 1e3, 2),
                         t_thin_all_loose_s=round(nst * ms_thin / 1e3, 1))
        t_core = 0.0; n_core_sets = 0
        wall = t_find; cpu = cpu_find
        row = dict(trial=i, rho=rho, ev=x['ev'], wall_s=round(wall, 3), cpu_s=round(cpu, 3), t_find_s=round(t_find, 3),
                   **extra,
                   stages_s={k: round(v, 3) for k, v in r['times_s'].items()},
                   n_road=r['n_road'], n_trip=r['n_trip'], n_refit=r['n_refit'], n_fast=r['n_fast'],
                   n_kept_all=r['n_kept_all'], n_stored=int(len(r['vars']['nl2'])), n_regather=r['n_regather'],
                   n_ip2ge7=int(np.sum(r['vars']['nip2'] >= 7)),
                   maxrss_GB=round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3))
        rows.append(row)
        print(json.dumps(row), flush=True)
    return rows, t_first


def summary(rows, key='wall_s'):
    t = np.array([r[key] for r in rows])
    rng = np.random.default_rng(7)
    bs = rng.choice(t, (4000, len(t)))
    return dict(n=len(t), mean=float(t.mean()), median=float(np.median(t)), p90=float(np.percentile(t, 90)),
                min=float(t.min()), max=float(t.max()), std=float(t.std(ddof=1)) if len(t) > 1 else 0.0,
                mean_err=float(t.std(ddof=1) / np.sqrt(len(t))) if len(t) > 1 else 0.0,
                median_boot68=[float(np.percentile(np.median(bs, 1), 16)), float(np.percentile(np.median(bs, 1), 84))],
                mean_boot68=[float(np.percentile(bs.mean(1), 16)), float(np.percentile(bs.mean(1), 84))])


if __name__ == '__main__':
    rho = int(sys.argv[1]); i0, i1 = int(sys.argv[2]), int(sys.argv[3])
    tag = sys.argv[4] if len(sys.argv) > 4 else ''
    cfg = FF.Config()
    rows, t_first = run(rho, i0, i1, cfg)
    out = dict(rho=rho, trials=rows, first_call_s=round(t_first, 2), summary_wall=summary(rows, 'wall_s'),
               summary_cpu=summary(rows, 'cpu_s'), summary_find=summary(rows, 't_find_s'),
               maxrss_GB=max(r['maxrss_GB'] for r in rows),
               config={k: (list(v) if isinstance(v, tuple) else v) for k, v in vars(cfg).items()},
               note='one process, one thread (numba njit, no parallel); input preparation excluded')
    path = TR.TT / 'data' / 'acts_stage4' / 'g2' / f'timing_rho{rho}{("_" + tag) if tag else ""}.json'
    path.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ('summary_wall', 'summary_cpu', 'maxrss_GB', 'first_call_s')}, indent=1))
