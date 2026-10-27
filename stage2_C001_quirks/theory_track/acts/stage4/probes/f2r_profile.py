"""f2r_profile.py -- Stage-4 plan FIXER R2 probe (TT env). Where does the F0 prototype's time per trial go at the
TDR-normalised density?  rho = 1 PU-only trials only (no rho = 2 runs, no signal).

It imports acts/stage4/probes/f1r_finder.py read-only and re-runs its trial() logic step by step with timers:
  road   : road selection + array preparation
  seeds  : numba seeds() (all (a, b) pairs, per-pair full scan of the road hits for the seed score)
  refitnb: numba refit_nb() of every seed with seed N_L2 >= T_SEED
  dedup  : the Python 'normals within 2 mrad' merge loop (any(...) over the growing kept list; O(N_fast x N_kept))
  refitnp: numpy refit() of every non-duplicate candidate (stored variables)
  thin   : thin_weights() timing on up to 20 candidates per trial, at rho = 1 and with rho = 2 settings (timing only)
The dedup is executed exactly as in f1r_finder (same order, same criterion) but with the kept normals held in a numpy
array; the original Python any() cost is measured on the first N_DEDUP_TIMED fast candidates and extrapolated with the
measured per-comparison cost (it is O(N_fast x N_kept)).  The numpy refit is timed on all kept candidates unless more
than NP_CAP, in which case it is timed on the first NP_CAP and extrapolated linearly (recorded).

PU-only, signal-blind add-on for review R2 B-1: for candidates with N_IT2 >= 3 and N_L2 >= 8 it records the plain
robust core width (1.4826 MAD of u.n2 over the IT + PS in-band hits, = f1r 'dw_core'), the trimmed core width (the
same with three 2.5-sigma trimming iterations; the plan's new w_core), the number of core hits, and the core-hit chi2/ndf
(PV-constrained refit chi2_min = lambda_min(sum w u u^T) over the core hits, 2S hits kept when their n2 coordinate is
within the core interval).  No signal is used.

Run (theory_track): pixi run python acts/stage4/probes/f2r_profile.py <topup_mode> <n_events> <event_offset> [roads]
  topup_mode 2 = OT layers topped up (the fix-R1 'TDR-OT' density, 48 s/trial), 1 = IT + OT topped up (the plan's
  adopted TDR-normalised density, never timed before).
Output: data/acts_stage4/fix_r2/f2r_profile_t<mode>_o<offset>.json
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT / 'acts' / 'stage4' / 'probes'))
import f1r_finder as F  # noqa: E402  (read-only import; module globals set below exactly as its __main__ does)

OUT = TT / 'data' / 'acts_stage4' / 'fix_r2'
OUT.mkdir(parents=True, exist_ok=True)
TSEED = 6
N_DEDUP_TIMED = 3000
NP_CAP = int(os.environ.get('F2R_NP_CAP', '4000'))


def core_stats(U, X, Y, S0, S1, LC, hidx, n, axis):
    """Plain and trimmed robust core width over IT + PS in-band hits, and the core-hit chi2/ndf (PU-only diagnostic)."""
    n2v = np.cross(n, axis)
    w = U[hidx] @ n2v
    ip = LC[hidx] <= 6
    if ip.sum() < 3:
        return None
    wi = w[ip]
    c = np.median(wi); s = 1.4826 * np.median(np.abs(wi - c))
    plain = float(s)
    # one-step core (the plan's pre-registered definition after this probe): interval c +- 2.5 w_plain, no iteration
    s2_ = np.abs(n2v[2]) * S1[hidx]
    lo1, hi1 = c - 2.5 * s, c + 2.5 * s
    in1 = np.where(ip, (w >= lo1) & (w <= hi1), (w >= lo1 - 3 * s2_) & (w <= hi1 + 3 * s2_))
    h1 = hidx[in1]
    chi1 = float('nan')
    if len(h1) >= 4:
        sg1 = np.sqrt(np.maximum(F.sig_vec(n, X[h1], Y[h1], S0[h1], S1[h1]), 1e-4) ** 2 + F.T_TOL ** 2)
        M1 = (U[h1] * (1.0 / sg1 ** 2)[:, None]).T @ U[h1]
        chi1 = float(np.linalg.eigvalsh(M1)[0]) / max(len(h1) - 2, 1)
    one = dict(chi2_core1=chi1, n_core1=int(len(h1)), n_inband=int(len(hidx)))
    core = np.ones(len(wi), bool)
    for _ in range(3):
        core = np.abs(wi - c) < 2.5 * max(s, 1e-3)
        if core.sum() < 3:
            break
        c = np.median(wi[core]); s = 1.4826 * np.median(np.abs(wi[core] - c))
    lo, hi = c - 2.5 * s, c + 2.5 * s
    # core hit set: IT + PS hits inside [lo, hi]; 2S hits whose n2 coordinate is inside [lo - 3 sig_n2, hi + 3 sig_n2]
    # (2S long-strip error along z projected on n2: sigma_long * |n2_z|)
    s2 = np.abs(n2v[2]) * S1[hidx]
    incore = np.where(ip, (w >= lo) & (w <= hi), (w >= lo - 3 * s2) & (w <= hi + 3 * s2))
    h = hidx[incore]
    if len(h) < 4:
        return dict(w_plain=plain, w_trim=float(s), n_core=int(len(h)), chi2_core=float('nan'), **one)
    sg = np.sqrt(np.maximum(F.sig_vec(n, X[h], Y[h], S0[h], S1[h]), 1e-4) ** 2 + F.T_TOL ** 2)
    wt = 1.0 / sg ** 2
    M = (U[h] * wt[:, None]).T @ U[h]
    lam = float(np.linalg.eigvalsh(M)[0])
    return dict(w_plain=plain, w_trim=float(s), n_core=int(len(h)), chi2_core=lam / max(len(h) - 2, 1), **one)


def trial_prof(H, sid, INT, SIG, pv, phimet):
    T = {}
    t0 = time.perf_counter()
    U0 = H[:, 1:4] - pv[None, :]
    r0 = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    m = dph < F.ROAD + np.arcsin(np.minimum(1.0, F.W_C / r0))
    U = np.ascontiguousarray(U0[m]); X = np.ascontiguousarray(H[m, 1]); Y = np.ascontiguousarray(H[m, 2])
    S0 = np.ascontiguousarray(H[m, 4]); S1 = np.ascontiguousarray(H[m, 5])
    sd = sid[m]; LC = F.LC_OF[sd]; SD = F.SIDE_OF[sd]; INTm = INT[m]; SIGm = SIG[m]
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    A = np.where(sd == F.SID['TBPX_L4'])[0]; B = np.where(sd == F.SID['TBPX_L3'])[0]; C = np.where(sd == F.SID['TBPX_L2'])[0]
    T['road'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    out, ntrip = F.seeds(U, X, Y, S0, S1, LC, SD, A, B, C, phiU, etaU, phimet, F.ROAD, F.W_C, TSEED, F.T_TOL)
    T['seeds'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    fast = []
    for ia, ib, n1, n2 in out:
        n = np.cross(U[ia], U[ib]); n /= np.linalg.norm(n)
        axis = U[ia] / np.linalg.norm(U[ia]) + U[ib] / np.linalg.norm(U[ib]); axis /= np.linalg.norm(axis)
        nf, nl2, nit2, chi, ns, axf = F.refit_nb(U, X, Y, S0, S1, F.LC_OF[sd], SD, n, axis, F.W_C, 3, F.T_TOL)
        if nl2 >= 4:
            fast.append((nl2, chi, nf, n, axis, n2))
    T['refitnb'] = time.perf_counter() - t0
    fast.sort(key=lambda t: (-t[0], t[1]))
    # --- dedup + numpy refit, same order and criterion as f1r_finder.trial ---
    kept = []; Kn = np.zeros((len(fast), 3)); nk = 0
    t_dd_vec = 0.0; t_np = 0.0; n_np = 0; n_cmp = 0
    t_dd_py = 0.0; n_cmp_py = 0
    for j, (nl2, chi, nf, n, axis, n2) in enumerate(fast):
        if j < N_DEDUP_TIMED:                       # time the original Python any() on the first candidates
            ta = time.perf_counter()
            _ = any(abs(abs(nf @ g['n']) - 1.0) < 2e-6 for g in kept)
            t_dd_py += time.perf_counter() - ta; n_cmp_py += len(kept)
        ta = time.perf_counter()
        dup = nk > 0 and bool(np.any(np.abs(np.abs(Kn[:nk] @ nf) - 1.0) < 2e-6))
        t_dd_vec += time.perf_counter() - ta; n_cmp += nk
        if dup:
            continue
        if n_np < NP_CAP:
            ta = time.perf_counter()
            f = F.refit(U, X, Y, S0, S1, LC, SD, n, axis)
            t_np += time.perf_counter() - ta; n_np += 1
        else:
            f = F.refit(U, X, Y, S0, S1, LC, SD, n, axis)   # still needed for the kept list (untimed beyond the cap)
        if f is None:
            continue
        f['axis'] = axis
        kept.append(f); Kn[nk] = f['n']; nk += 1
    per_cmp = t_dd_py / max(n_cmp_py, 1)
    T['dedup_vectorised'] = t_dd_vec
    T['dedup_python_est'] = per_cmp * n_cmp            # original any() loop cost, O(N_fast x N_kept), extrapolated
    T['refitnp_est'] = t_np / max(n_np, 1) * nk if n_np else 0.0
    # thinning-weight timing (timing only): up to 20 candidates with N_L2 >= 5
    tw_t1 = []; tw_t2 = []
    for f in [g for g in kept if g['nl2'] >= 5][:20]:
        h = f['hidx']
        ta = time.perf_counter(); F.thin_weights(h, LC, SD, INTm, 1.0); tw_t1.append(time.perf_counter() - ta)
        ta = time.perf_counter(); F.thin_weights(h, LC, SD, INTm, 2.0); tw_t2.append(time.perf_counter() - ta)
    # PU-only core-width / core-chi2 diagnostics for N_IT2 >= 3, N_L2 >= 8 candidates
    cores = []
    for f in kept:
        if f['nit2'] >= 3 and f['nl2'] >= 8:
            cs = core_stats(U, X, Y, S0, S1, LC, f['hidx'], f['n'], f['axis'])
            if cs:
                cs.update(nl2=int(f['nl2']), chi2ndf=float(f['chi2ndf']), dw_core_f1r=float(f['dw_core']),
                          n_int=int(len(np.unique(INTm[f['hidx']]))))
                cores.append(cs)
    nsets = len({tuple(sorted(f['hidx'].tolist())) for f in kept})
    return dict(n_road=int(m.sum()), n_A=int(len(A)), n_B=int(len(B)), n_C=int(len(C)), n_trip=int(ntrip),
                n_refit=len(out), n_fast=len(fast), n_kept=nk, n_distinct_hitsets=nsets, n_cmp=int(n_cmp),
                per_cmp_python_us=per_cmp * 1e6, refitnp_ms_each=(t_np / max(n_np, 1)) * 1e3, n_np_timed=n_np,
                thin_ms_rho1_median=float(np.median(tw_t1) * 1e3) if tw_t1 else None,
                thin_ms_rho2_median=float(np.median(tw_t2) * 1e3) if tw_t2 else None,
                times_s={k: round(v, 3) for k, v in T.items()},
                total_original_est_s=round(T['road'] + T['seeds'] + T['refitnb'] + T['dedup_python_est'] + T['refitnp_est'], 2),
                cores_L8=cores)


if __name__ == '__main__':
    mode = int(sys.argv[1]); nev = int(sys.argv[2]); off = int(sys.argv[3]); roads = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    F.TOPUP_MODE = mode
    F.T_TOL = 0.030
    evs = F.load_pu()
    rng = np.random.default_rng(20261013 + 31 * mode + off)
    res = []
    tw0 = time.time(); tc0 = time.process_time()
    for i in range(off, off + nev):
        tag, e, vz = evs[i]
        H, sid, INT, SIG, uz = F.prep(e, vz, tag, rng, mode > 0)
        pv = F.lum_pv(rng); phi0 = rng.uniform(-np.pi, np.pi)
        for k in range(roads):
            tt = time.perf_counter()
            r = trial_prof(H, sid, INT, SIG, pv, float((phi0 + k * np.pi / 2 + np.pi) % (2 * np.pi) - np.pi))
            r['wall_s'] = round(time.perf_counter() - tt, 2)
            r.update(ev=int(tag), road=k, n_hits_event=int(len(H)))
            res.append(r)
            print('t%d ev %d road %d' % (mode, tag, k), r['times_s'], 'fast', r['n_fast'], 'kept', r['n_kept'],
                  'orig_est', r['total_original_est_s'], 'wall', r['wall_s'], flush=True)
    summ = dict(topup_mode=mode, n_trials=len(res), cpu_s=round(time.process_time() - tc0, 1), wall_s=round(time.time() - tw0, 1),
                tseed=TSEED, t_tol_mm=F.T_TOL, w_c_mm=F.W_C, trials=res)
    (OUT / f'f2r_profile_t{mode}_o{off}.json').write_text(json.dumps(summ, indent=1))
