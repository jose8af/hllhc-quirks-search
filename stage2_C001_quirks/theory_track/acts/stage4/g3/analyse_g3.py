"""analyse_g3.py -- the pre-registered G3 pilot analysis (C001 Stage 4; PU-only, no signal input).

Authority: acts/stage4/WP_RULE.md (frozen; sha256 in acts/stage4/frozen_inputs.json) §2, §6.1-§6.4, §5.4 item 11, §S,
and acts/stage4/plan.md §4.1 step 4 / §11 item 4 (G3 must show (i)-(v)).  Nothing here is tuned; every threshold below
is a transcription.  Where the frozen text is ambiguous the conservative reading is taken and recorded in
RES['readings'] (and in G3_REPORT.md).

Samples: G3B1 (rho = 1, 25 events x 4 roads per job) and G3B2 (rho = 2, 10 events x 2 roads per job), production files
data/acts_stage4/prod/G3/<sample>/<job>.npz (run_stage4.pack keys; trials.road = road index, trials.road_cfg = the
road half-width).  G3B1_00021, G3B1_00059 and G3B1_00077 are LEFT OUT (orchestrator decision 2026-10-13, ACTS navigation failure;
WP_RULE item 11 admits only outputs with the frozen code hashes).

Tests (WP_RULE §6.4; counts per distinct hit set = trials.n_grp at rho = 1, trials.S_ded at rho = 2 -- §2 governing):
  T1   counting family (R01-R04; per-hit-set from R04 on, so r1 = R04): z = ln(N_obs/N_pred)/sqrt(1/N_obs + s_ln^2),
       N_pred = n_trials(B1) x <S_ded>(B2), s_ln from the B2 event bootstrap; pass |z| < 2; lever arm
       <S_ded>/<N_grp(rho=2)> <= 0.1.
  T1w  the same at the tightest width or chi2_core rung (R05-R11) with >= 10 B1 counts (lever-arm rule as T1).
  T1e  the same at the first dE/dx column (F0e>1.3) if it has >= 10 B1 counts, else T3.
  trend  T1 at every rung >= R04 (R04-R14) with >= 10 B1 counts; slope of ln(N_obs/N_pred) vs rung index; 2 sigma.
  T3   rung factorisation on B1 (only needed where a rung is not reachable at rho = 2; reported).
  (ii) SR-T time-position independence on the loose rungs (in-time BTL spectrum; see readings).
  (iii) reach at rho = 2 (>= 10 candidates), (v) PU population of every rung at rho = 1 and 2.
  (iv) T_seed stability (paired re-run with T_seed = 4, acts/stage4/g3/g3_rerun.py).
  C-4  nsub = 256 re-run of a rho = 2 job: S_ded shift.
Also: frozen-hash admission (item 11), V4-1 records, IS run checks (meanW_pull), throughput and disk.

    nice -n 15 pixi run python -m acts.stage4.g3.analyse_g3 [--nboot 1000] [--no-srt]
"""
import argparse
import glob
import hashlib
import json
import os
import re
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent            # acts/stage4/g3
S4 = HERE.parent
TT = S4.parents[1]
PROD = TT / 'data' / 'acts_stage4' / 'prod' / 'G3'
OUT = TT / 'data' / 'acts_stage4' / 'g3'
RERUN = OUT / 'rerun'
EXCLUDED = {'G3B1_00021': 'ACTS navigation failure (GridPortalLink insideBounds), left out by orchestrator decision',
            'G3B1_00059': 'ACTS navigation failure (GridPortalLink insideBounds), left out by orchestrator decision',
            'G3B1_00077': 'ACTS navigation failure (GridPortalLink insideBounds), same mode; left out by orchestrator '
                          'decision 2026-10-14 00:07 (G3 = 127/130 jobs)'}

from acts.stage4.finder import production as PR   # noqa: E402  (RUNGS, full_set_flags; frozen code, read-only use)
from acts.stage4.finder import weights as WG      # noqa: E402

RUNGS = list(PR.RUNGS)
NR = len(RUNGS)
LADDER = list(range(14))                 # R01..R14 = column 0..13; rung number = column + 1
NOGRP = set(PR.NOGRP)
FAM = {'counting': [0, 1, 2, 3], 'width': [4, 5, 6, 7], 'chi2core': [8, 9, 10], '2S': [11, 12, 13]}
DT_ACC = 25.0                            # ns (WP_RULE §1.4)
LATE_RATE = 1e-4                         # per-hit late rate threshold (WP_RULE §1.4, frozen_inputs sr_t)
OVERLAY_K = [k for k in range(-12, 4) if k != 0]     # out-of-time crossings (WP_RULE §1.4)
BX_NS = 25.0
SEED = 20261013


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def frozen_hashes():
    """WP_RULE.md Appendix A.3 (code files) + the WP_RULE sha256 recorded at the freeze."""
    txt = (S4 / 'WP_RULE.md').read_text()
    a3 = dict(re.findall(r'\| `([^`]+)` \| `([0-9a-f]{64})` \|', txt.split('### A.3')[1].split('### A.4')[0]))
    fz = json.loads((S4 / 'frozen_inputs.json').read_text())
    return a3, fz


# ----------------------------------------------------------------------------------------------- loading
CAND_KEYS = ['tag', 'group', 'trial', 'nit2', 'nip2', 'n2s2', 'nl2', 'dw_core', 'chi2_core', 'n_core', 'p_chi2core',
             'dedx', 'dphi_met', 'eta_axis', 'btl_n_band', 'btl_dt0', 'rungs', 'cross', 'normal', 'axis']


def load_job(p, want_cand, rho):
    out = {}
    with np.load(p, allow_pickle=False) as z:
        meta = json.loads(str(z['meta_json']))
        out['meta'] = meta
        out['complete'] = int(z['complete'])
        out['job_id'] = str(z['job_id'])
        n = int(z['n_trials'])
        tk = ['ev', 'road', 'n_pass', 'n_grp', 'n_road', 't_total', 'n_loose', 'pv', 'n_pass_T', 'n_grp_T']
        if rho > 1:
            tk += ['S_ded', 'S_uni', 'V_uni', 'meanW_pull', 'meanW_pull_T', 'S_ded_T', 'is_zero_draw_frac', 'n_is_sets']
        out['tr'] = {k: z['trials.' + k] for k in tk if 'trials.' + k in z.files}
        out['tr']['times'] = z['trials.times']
        out['times_cols'] = [str(c) for c in z['trials.times_cols']]
        out['n_trials'] = n
        for k in ('chain.v41', 'chain.v41_cols', 'chain.evstats', 'chain.evstats_cols'):
            if k in z.files:
                out[k] = z[k]
        if want_cand:
            out['cand'] = {k: z['cand.' + k] for k in CAND_KEYS if 'cand.' + k in z.files}
            if 'btl' in z.files:
                out['btl'] = z['btl']
    return out


def admission(meta, a3, fz):
    """WP_RULE §5.4 item 11: produced with the frozen code hashes (A.3) and the frozen WP_RULE sha256."""
    cs = meta.get('code_sha256', {})
    bad = {f: cs.get(f) for f, h in a3.items() if f in cs and cs[f] != h}
    missing = [f for f in a3 if f.startswith('acts/stage4/') and f.endswith('.py') and f not in cs
               and 'probes' not in f and 'eadm' not in f]
    wp_ok = cs.get('acts/stage4/WP_RULE.md') == fz['wp_rule_sha256']
    fz_ok = bool(meta.get('frozen_inputs', {}) and meta['frozen_inputs'].get('frozen'))
    return dict(ok=(not bad) and wp_ok and fz_ok, bad=bad, missing_from_meta=missing, wp_rule_ok=wp_ok, frozen=fz_ok)


# ----------------------------------------------------------------------------------------------- statistics
def boot_idx(n, nboot, rng):
    return rng.integers(0, n, size=(nboot, n))


def ev_sums(ev_of_trial, x, n_ev):
    """Per-event sums of per-trial rows x (ntr, ...)."""
    out = np.zeros((n_ev,) + x.shape[1:])
    np.add.at(out, ev_of_trial, x)
    return out


def ln_ratio_test(nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2, col):
    """T1-type statistic at one column.  nobs_ev (E1, NR) B1 per-event counts; s2_ev (E2, NR) B2 per-event S_ded sums.
    Returns dict with N_obs, N_pred, ln_r, s_ln_pred (B2 event bootstrap), z, and B1-bootstrap diagnostics."""
    N1 = ntr1_ev.sum(); N2 = ntr2_ev.sum()
    nobs = nobs_ev[:, col].sum()
    p1 = s2_ev[:, col].sum() / N2
    npred = N1 * p1
    res = dict(N_obs=float(nobs), N_pred=float(npred), P1_hat_per_trial=float(p1), n_trials_B1=int(N1),
               n_trials_B2=int(N2))
    if not (nobs > 0 and npred > 0):
        res.update(ln_r=None, z=None)
        return res
    pb = s2_ev[bi2, col].sum(1) / ntr2_ev[bi2].sum(1)
    pos = pb > 0
    s_ln = float(np.std(np.log(pb[pos]), ddof=1)) if pos.mean() > 0.99 else float(np.std(pb, ddof=1) / p1)
    lnr = float(np.log(nobs / npred))
    z = lnr / np.sqrt(1.0 / nobs + s_ln ** 2)
    ob = nobs_ev[bi1, col].sum(1) / ntr1_ev[bi1].sum(1)
    s_ln_obs_boot = float(np.std(np.log(ob[ob > 0]), ddof=1)) if (ob > 0).mean() > 0.99 else float(
        np.std(ob, ddof=1) / (nobs / N1))
    res.update(ln_r=lnr, ratio=float(nobs / npred), s_ln_pred=s_ln, z=float(z),
               s_ln_obs_poisson=float(1 / np.sqrt(nobs)), s_ln_obs_boot_diag=s_ln_obs_boot,
               z_with_B1_boot_diag=float(lnr / np.sqrt(s_ln_obs_boot ** 2 + s_ln ** 2)),
               boot_zero_frac_B2=float(1 - pos.mean()))
    return res


def branch_of(z):
    if z is None:
        return 'untestable'
    if z < -2:
        return 'conservative'
    if z > 2:
        return 'anti-conservative'
    return 'nominal'


SEVERITY = {'nominal': 0, 'trend': 1, 'conservative': 2, 'untestable': 3, 'anti-conservative': 4,
            'anti-conservative (missing lever arm)': 4}


def family_test(name, cols, nobs_ev, ntr1_ev, s2_ev, ntr2_ev, n2grp_ev, bi1, bi2):
    """WP_RULE §6.4 T1 rule inside one family: r1 = the tightest family rung with >= 10 B1 counts; lever arm
    <S_ded>/<N_grp(rho=2)> <= 0.1 else 'next tighter rung with >= 10 B1 counts' (none tighter exists by construction),
    else the rung with the largest lever arm (smallest ratio) and a closure failure of unknown direction."""
    N2 = ntr2_ev.sum()
    rows = []
    for c in cols:
        nobs = nobs_ev[:, c].sum()
        lev = (s2_ev[:, c].sum() / N2) / (n2grp_ev[:, c].sum() / N2) if n2grp_ev[:, c].sum() > 0 else np.nan
        rows.append(dict(col=c, rung=RUNGS[c], N_obs_B1=float(nobs), lever=float(lev)))
    ok = [r for r in rows if r['N_obs_B1'] >= 10]
    res = dict(test=name, family_rungs=[RUNGS[c] for c in cols], rows=rows)
    if not ok:
        res.update(r1=None, branch='untestable', note='no family rung with >= 10 B1 counts')
        return res
    r1 = ok[-1]
    looser_ok = [r['rung'] for r in ok[:-1] if np.isfinite(r['lever']) and r['lever'] <= 0.1]
    if np.isfinite(r1['lever']) and r1['lever'] <= 0.1:
        t = ln_ratio_test(nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2, r1['col'])
        res.update(r1=r1['rung'], lever=r1['lever'], lever_ok=True, **t, branch=branch_of(t['z']))
    else:
        best = min((r for r in ok if np.isfinite(r['lever'])), key=lambda r: r['lever'])
        t = ln_ratio_test(nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2, best['col'])
        res.update(r1=best['rung'], lever=best['lever'], lever_ok=False, **t,
                   branch='anti-conservative (missing lever arm)',
                   note='no rung with a 1-decade lever arm at the tightest >= 10-count rung; WP_RULE §6.4: closure '
                        'failure of unknown direction -> anti-conservative branch (upper envelope)',
                   looser_rungs_with_lever_ok=looser_ok)
    return res


def trend_test(cols, nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2):
    pts = []
    for c in cols:
        t = ln_ratio_test(nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2, c)
        if t['N_obs'] >= 10 and t['z'] is not None:
            pts.append(dict(col=c, rung=RUNGS[c], x=c + 1, ln_r=t['ln_r'],
                            sig=float(np.sqrt(1 / t['N_obs'] + t['s_ln_pred'] ** 2)), z=t['z'], N_obs=t['N_obs'],
                            N_pred=t['N_pred']))
    res = dict(points=pts)
    if len(pts) < 3:
        res.update(slope=None, significant=False, note='fewer than 3 rungs with >= 10 B1 counts: slope not testable')
        return res
    x = np.array([p['x'] for p in pts], float); y = np.array([p['ln_r'] for p in pts]); w = 1 / np.array(
        [p['sig'] for p in pts]) ** 2
    xm = np.sum(w * x) / np.sum(w)
    b = np.sum(w * (x - xm) * y) / np.sum(w * (x - xm) ** 2)
    a = np.sum(w * y) / np.sum(w) - b * xm
    sb_wls = float(np.sqrt(1 / np.sum(w * (x - xm) ** 2)))
    cols_ = [p['col'] for p in pts]
    N1b = ntr1_ev[bi1].sum(1); N2b = ntr2_ev[bi2].sum(1)
    bs = []
    for c in [cols_]:
        O = nobs_ev[:, c][bi1].sum(1) / N1b[:, None]       # (nboot, k) per-trial observed
        P = s2_ev[:, c][bi2].sum(1) / N2b[:, None]
        good = np.all((O > 0) & (P > 0), axis=1)
        Y = np.log(O[good] / P[good])
        bs = np.sum(w * (x - xm) * Y, axis=1) / np.sum(w * (x - xm) ** 2)
    sb_boot = float(np.std(bs, ddof=1))
    t_boot = b / sb_boot; t_wls = b / sb_wls
    sig = bool(abs(t_boot) > 2 or abs(t_wls) > 2)
    res.update(slope=float(b), intercept_at_x0=float(a), x_mean=float(xm), s_slope_boot=sb_boot, s_slope_wls=sb_wls,
               t_boot=float(t_boot), t_wls=float(t_wls), significant=sig,
               governing='significant if |slope|/sigma > 2 with EITHER the joint event-bootstrap sigma or the WLS sigma '
                         '(conservative reading: the cumulative rungs are correlated, the frozen text names no fit)',
               direction=('anti-conservative' if b > 0 else 'conservative') if sig else None,
               extrapolated_ln_r={RUNGS[k] if k < 14 else 'R%02d' % (k + 1): float(a + b * (k + 1))
                                  for k in range(3, 23)},
               n_boot_used=int(len(bs)))
    return res


# ----------------------------------------------------------------------------------------------- SR-T (ii)
def _srt_kernel():
    from numba import njit
    inb = WG._btl_inband
    C = WG.C_MM_PER_NS

    @njit(cache=False)
    def k(NRM, AXS, sel, UB, CXB, CYB, S0B, S1B, TB, ttol, wc, lo, binw, hist, nh, dt0):
        nb = UB.shape[0]
        nbin = hist.shape[0]
        for s in range(sel.shape[0]):
            c = sel[s]
            nx = NRM[c, 0]; ny = NRM[c, 1]; nz = NRM[c, 2]
            ax = AXS[c, 0]; ay = AXS[c, 1]; az = AXS[c, 2]
            n2x = ny * az - nz * ay; n2y = nz * ax - nx * az; n2z = nx * ay - ny * ax
            tb = np.inf
            for b in range(nb):
                if not inb(nx, ny, nz, ax, ay, az, n2x, n2y, n2z, UB[b, 0], UB[b, 1], UB[b, 2], CXB[b], CYB[b],
                           S0B[b], S1B[b], ttol, wc):
                    continue
                dt = TB[b] - np.sqrt(UB[b, 0] ** 2 + UB[b, 1] ** 2 + UB[b, 2] ** 2) / C
                nh[s] += 1
                if TB[b] < tb:
                    tb = TB[b]; dt0[s] = dt
                i = int(np.floor((dt - lo) / binw))
                if i < 0:
                    i = 0
                elif i >= nbin:
                    i = nbin - 1
                hist[i] += 1
    return k


HLO, HBW, HN = -100.0, 0.005, int(round(450.0 / 0.005))     # per-hit dt histogram: [-100, 350) ns, 5 ps bins (+ edges)


def srt_hits(job, ker, cfg_ttol, cfg_wc):
    """Per-hit dt histogram of the in-band BTL hits of the B1 LOOSE candidates (S3 sample passing R01), and a
    consistency check of the kernel against the stored btl_n_band / btl_dt0."""
    c = job['cand']; tr = job['tr']; B = job['btl']
    flags = np.unpackbits(c['rungs'], axis=1)[:, :NR].astype(bool)
    sel_all = np.where(((c['tag'] & 2) > 0) & flags[:, 0])[0]
    hist = np.zeros(HN, np.int64)
    nh = np.zeros(len(sel_all), np.int64); dt0 = np.full(len(sel_all), np.nan)
    ev0 = int(job['meta']['job']['ev0'])
    ti = c['trial'][sel_all]
    order = np.argsort(ti, kind='stable')
    sel_all = sel_all[order]; ti = ti[order]
    bev = B[:, 0].astype(np.int64)
    starts = np.searchsorted(ti, np.arange(job['n_trials'] + 1))
    nrm = np.ascontiguousarray(c['normal'], np.float64); axs = np.ascontiguousarray(c['axis'], np.float64)
    for t in range(job['n_trials']):
        a, b = starts[t], starts[t + 1]
        if a == b:
            continue
        ie = int(tr['ev'][t]) - ev0
        bb = B[bev == ie]
        pv = tr['pv'][t]
        UB = np.ascontiguousarray(bb[:, 2:5].astype(np.float64) - pv[None, :])
        r = np.hypot(bb[:, 2], bb[:, 3]).astype(np.float64)
        h_nh = np.zeros(b - a, np.int64); h_dt = np.full(b - a, np.nan)
        ker(nrm, axs, sel_all[a:b].astype(np.int64), UB, np.ascontiguousarray(bb[:, 2] / r),
            np.ascontiguousarray(bb[:, 3] / r), np.ascontiguousarray(bb[:, 5].astype(np.float64)),
            np.ascontiguousarray(bb[:, 6].astype(np.float64)), np.ascontiguousarray(bb[:, 8].astype(np.float64)),
            cfg_ttol, cfg_wc, HLO, HBW, hist, h_nh, h_dt)
        nh[a:b] = h_nh; dt0[a:b] = h_dt
    stored_n = c['btl_n_band'][sel_all].astype(np.int64)
    stored_dt = c['btl_dt0'][sel_all].astype(np.float64)
    both = np.isfinite(stored_dt) & np.isfinite(dt0)
    chk = dict(n_sel=int(len(sel_all)), n_mismatch_nband=int(np.sum(np.minimum(nh, 32767) != stored_n)),
               max_abs_ddt0_ns=float(np.max(np.abs(dt0[both] - stored_dt[both]))) if both.any() else 0.0)
    return hist, chk


def tmin_from_hist(hist, overlay):
    """t_min = the smallest delay t at which the per-hit late rate R(t) = (hits with dt in [t, dt_acc]) / (all hits)
    falls below 1e-4 (R is non-increasing in t).  overlay=True: in-time spectrum (+) the 15 out-of-time crossings,
    each an independent copy of the in-time spectrum shifted by k x 25 ns (same per-crossing time spread)."""
    edges = HLO + HBW * np.arange(HN + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    ks = [0] + (OVERLAY_K if overlay else [])
    grid = np.arange(0.0, DT_ACC + 1e-9, 0.005)
    tot = hist.sum() * len(ks)
    cs = np.concatenate([[0], np.cumsum(hist)])

    def n_in(lo_, hi_):        # hits with lo_ <= dt < hi_ (bin centres)
        i0 = np.searchsorted(centres, lo_, 'left'); i1 = np.searchsorted(centres, hi_, 'right')
        return cs[np.clip(i1, 0, HN)] - cs[np.clip(i0, 0, HN)]
    R = np.zeros(len(grid))
    for k in ks:
        R += n_in(grid - k * BX_NS, DT_ACC - k * BX_NS)
    R /= tot
    below = np.where(R < LATE_RATE)[0]
    tmin = float(grid[below[0]]) if len(below) else None
    probe = {f'{t:g}': float(R[np.searchsorted(grid, t)]) for t in (0.5, 1, 2, 3, 5, 10, 15, 20, 24, 24.5)}
    return dict(t_min_ns=tmin, n_hits_in_time=int(hist.sum()), rate_at=probe, overlay=overlay,
                n_hits_dt_gt_25_in_time=int(hist[centres > DT_ACC].sum()))


def indep_test(late, bins, rng, ev=None, nsim=10000, nboot=2000):
    """Homogeneity of the late fraction across bins (pass p > 0.05, plan §2.3).  Governing: Pearson X^2 with the
    Rao-Scott first-order correction for clustering (candidates of one event share BTL hits, so they are not
    independent): X^2_RS = X^2 / deff, deff = Var_event-bootstrap(pooled fraction) / [p(1-p)/N], p-value from
    chi2(nbins - 1).  Diagnostic: the naive X^2 with a parametric-bootstrap p-value (independent binomials)."""
    from scipy.stats import chi2 as CHI2
    ub = np.unique(bins[bins >= 0])
    n = np.array([np.sum(bins == b) for b in ub]); k = np.array([np.sum(late[bins == b]) for b in ub])
    p = k.sum() / max(n.sum(), 1)
    if k.sum() == 0 or len(ub) < 2:
        return dict(n=n.tolist(), k=k.tolist(), p_pool=float(p), p_value=None, note='no late candidates: untestable')

    def x2(kk):
        e = n * p
        return np.sum((kk - e) ** 2 / np.maximum(e * (1 - p), 1e-300), axis=-1)
    obs = x2(k)
    sim = x2(rng.binomial(n[None, :], p, size=(nsim, len(n))))
    pv_naive = float((np.sum(sim >= obs) + 1) / (nsim + 1))
    out = dict(n=n.tolist(), k=k.tolist(), frac=(k / np.maximum(n, 1)).tolist(), p_pool=float(p), X2=float(obs),
               p_value_naive=pv_naive)
    if ev is not None:
        m = bins >= 0
        ue, inv = np.unique(ev[m], return_inverse=True)
        ne = np.bincount(inv, minlength=len(ue)).astype(float)
        ke = np.bincount(inv, weights=late[m].astype(float), minlength=len(ue))
        bi = rng.integers(0, len(ue), size=(nboot, len(ue)))
        pb = ke[bi].sum(1) / ne[bi].sum(1)
        deff = float(np.var(pb, ddof=1) / (p * (1 - p) / n.sum()))
        x2rs = obs / max(deff, 1.0)
        pv = float(CHI2.sf(x2rs, len(n) - 1))
        out.update(deff=deff, X2_RS=float(x2rs), p_value=pv, pass_=bool(pv > 0.05), n_events=int(len(ue)))
    else:
        out.update(p_value=pv_naive, pass_=bool(pv_naive > 0.05))
    return out


def tercile_bins(x):
    x = np.asarray(x, float)
    ok = np.isfinite(x)
    out = np.full(len(x), -1)
    if ok.sum() < 3:
        return out
    q = np.quantile(x[ok], [1 / 3, 2 / 3])
    out[ok] = np.digitize(x[ok], q)
    return out


# ----------------------------------------------------------------------------------------------- T3 and c-test
def req_flags(c):
    """Single added requirement of each ladder rung (WP_RULE §3) on the stored S2 records (+ the fixed cuts)."""
    with np.errstate(invalid='ignore'):
        p = c['p_chi2core'].astype(float)
        w = c['dw_core'].astype(float)
        a = {0: (c['nit2'] >= 3) & (c['nip2'] >= 4), 1: c['nip2'] >= 5, 2: c['nip2'] >= 6, 3: c['nip2'] >= 7,
             4: w < 37.5, 5: w < 18.75, 6: w < 9.4, 7: w < 4.7, 8: p > 1e-3, 9: p > 0.01, 10: p > 0.05,
             11: c['n2s2'] >= 1, 12: c['n2s2'] >= 2, 13: c['n2s2'] >= 3}
    aligned = (c['dphi_met'] < 0.15) & (np.abs(c['eta_axis']) < 1.0)
    return a, aligned


VAR_OF = {0: 'cnt', 1: 'nip2', 2: 'nip2', 3: 'nip2', 4: 'w', 5: 'w', 6: 'w', 7: 'w', 8: 'p', 9: 'p', 10: 'p',
          11: '2s', 12: '2s', 13: '2s'}


# ----------------------------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--nboot', type=int, default=1000)
    ap.add_argument('--no-srt', action='store_true')
    ap.add_argument('--max-jobs', type=int, default=0, help='development: at most this many jobs per sample')
    ap.add_argument('--out', default=str(OUT / 'g3_results.json'))
    ap.add_argument('--dev-b2', nargs='*', default=[], help='development only: extra rho = 2 files used as G3B2 '
                    '(no admission check; never for the G3 result)')
    a = ap.parse_args(argv)
    try:
        os.nice(15)
    except OSError:
        pass
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    a3, fz = frozen_hashes()
    RES = dict(created=time.strftime('%Y-%m-%d %H:%M:%S'), wp_rule_sha256_file=sha256(S4 / 'WP_RULE.md'),
               wp_rule_sha256_frozen=fz['wp_rule_sha256'], rungs=RUNGS, excluded=EXCLUDED, readings={})
    RES['wp_rule_unchanged'] = RES['wp_rule_sha256_file'] == fz['wp_rule_sha256']
    man = json.loads((S4 / 'jobs' / 'G3.json').read_text())['jobs']
    jobs = {s: [j for j in man if j['sample'] == s] for s in ('G3B1', 'G3B2')}
    data = {}
    adm = {}
    status = {}
    for s, js in jobs.items():
        rho = 1 if s == 'G3B1' else 2
        data[s] = []
        st = dict(manifest=len(js), excluded=[], missing=[], invalid=[], not_admitted=[], used=0)
        for j in js:
            if a.max_jobs and len(data[s]) >= a.max_jobs:
                break
            if j['id'] in EXCLUDED:
                st['excluded'].append(j['id']); continue
            p = PROD / s / (j['id'] + '.npz')
            if not p.exists():
                st['missing'].append(j['id']); continue
            d = load_job(p, want_cand=True, rho=rho)
            if d['job_id'] != j['id'] or d['complete'] != 1 or d['n_trials'] != j['n_events'] * j['roads']:
                st['invalid'].append(j['id']); continue
            ad = admission(d['meta'], a3, fz)
            adm[j['id']] = ad
            if not ad['ok']:
                st['not_admitted'].append(j['id']); continue
            d['job'] = j
            data[s].append(d)
            st['used'] += 1
        if s == 'G3B2' and a.dev_b2:
            for p in a.dev_b2:
                d = load_job(p, want_cand=True, rho=2)
                d['job'] = dict(d['meta']['job']); d['job_id'] = d['job']['id']
                data[s].append(d); st['used'] += 1; st.setdefault('DEV_FILES', []).append(p)
            RES['DEVELOPMENT_RUN'] = True
        status[s] = st
    RES['status'] = status
    RES['admission'] = dict(all_ok=all(v['ok'] for v in adm.values()), n=len(adm),
                            any_bad={k: v for k, v in adm.items() if not v['ok']})
    print('loaded', {s: status[s]['used'] for s in status}, 'in %.0f s' % (time.time() - t_start), flush=True)

    # ---- per-trial / per-event tables
    def stack(s):
        tr = {}
        ev_of = []; evn = 0; ev_keys = []
        for ij, d in enumerate(data[s]):
            for k, v in d['tr'].items():
                tr.setdefault(k, []).append(v)
            ue, inv = np.unique(d['tr']['ev'], return_inverse=True)
            ev_of.append(inv + evn); evn += len(ue)
        tr = {k: np.concatenate(v) for k, v in tr.items()}
        return tr, np.concatenate(ev_of) if ev_of else np.zeros(0, int), evn
    tr1, ev1, E1 = stack('G3B1')
    tr2, ev2, E2 = stack('G3B2')
    have_b2 = E2 > 0
    ntr1_ev = ev_sums(ev1, np.ones(len(ev1)), E1)
    grp1 = np.where(tr1['n_grp'] < 0, tr1['n_pass'], tr1['n_grp']).astype(float)   # per-hit-set; union where none
    nobs_ev = ev_sums(ev1, grp1, E1)
    npass1_ev = ev_sums(ev1, tr1['n_pass'].astype(float), E1)
    bi1 = boot_idx(E1, a.nboot, rng)
    RES['samples'] = dict(B1_trials=int(len(ev1)), B1_events=int(E1), B2_trials=int(len(ev2)), B2_events=int(E2))
    if have_b2:
        ntr2_ev = ev_sums(ev2, np.ones(len(ev2)), E2)
        sded = np.where(np.isnan(tr2['S_ded']), tr2['S_uni'], tr2['S_ded'])           # union where no groups (R01-R03)
        s2_ev = ev_sums(ev2, sded, E2)
        suni_ev = ev_sums(ev2, tr2['S_uni'], E2)
        grp2 = np.where(tr2['n_grp'] < 0, tr2['n_pass'], tr2['n_grp']).astype(float)
        n2grp_ev = ev_sums(ev2, grp2, E2)
        n2pass_ev = ev_sums(ev2, tr2['n_pass'].astype(float), E2)
        bi2 = boot_idx(E2, a.nboot, rng)

    # ---- (v) population of every rung at rho = 1 and rho = 2, (iii) reach at rho = 2
    pop = []
    for c in range(NR):
        r = dict(rung=RUNGS[c], B1_sum_grp=float(nobs_ev[:, c].sum()), B1_sum_pass=float(npass1_ev[:, c].sum()),
                 B1_per_trial_grp=float(nobs_ev[:, c].sum() / max(len(ev1), 1)),
                 B1_trial_pass_frac=float(np.mean(grp1[:, c] > 0)))
        if have_b2:
            N2 = len(ev2)
            r.update(B2_sum_grp=float(n2grp_ev[:, c].sum()), B2_sum_pass=float(n2pass_ev[:, c].sum()),
                     B2_per_trial_grp=float(n2grp_ev[:, c].sum() / N2),
                     P1hat_ded=float(np.nansum(tr2['S_ded'][:, c]) / N2) if c not in NOGRP else None,
                     P1hat_uni=float(np.nansum(tr2['S_uni'][:, c]) / N2),
                     lever_ded=float(s2_ev[:, c].sum() / n2grp_ev[:, c].sum()) if n2grp_ev[:, c].sum() > 0 else None,
                     reachable_rho2=bool(n2grp_ev[:, c].sum() >= 10))
        pop.append(r)
    RES['population'] = pop
    if have_b2:
        reach = [RUNGS[c] for c in LADDER if pop[c]['reachable_rho2']]
        deepest = max((c for c in LADDER if pop[c]['reachable_rho2']), default=None)
        RES['reach_rho2'] = dict(reachable_ladder_rungs=reach, deepest_reachable=RUNGS[deepest] if deepest is not None
                                 else None, T3_takes_over_after=RUNGS[deepest] if deepest is not None else None,
                                 convention='per-hit-set groups (n_grp) >= 10 summed over B2 trials (R04+); union '
                                            'n_pass for R01-R03 (WP_RULE §2, §6.1)')
        RES['readings']['reach'] = ('"reachable at rho" counted in the governing per-hit-set convention (fewer '
                                    'counts than union -> fewer rungs reachable -> earlier T3: conservative)')

    # ---- (i) T1, T1w, T1e, trend
    if have_b2:
        RES['T1'] = family_test('T1', [3], nobs_ev, ntr1_ev, s2_ev, ntr2_ev, n2grp_ev, bi1, bi2)
        RES['T1_tightest_ladder_rung_diag'] = family_test('T1 (any ladder rung R04-R14; reading B)',
                                                          list(range(3, 14)), nobs_ev, ntr1_ev, s2_ev, ntr2_ev,
                                                          n2grp_ev, bi1, bi2)
        RES['T1w'] = family_test('T1w', list(range(4, 11)), nobs_ev, ntr1_ev, s2_ev, ntr2_ev, n2grp_ev, bi1, bi2)
        if nobs_ev[:, 14].sum() >= 10:
            RES['T1e'] = family_test('T1e', [14], nobs_ev, ntr1_ev, s2_ev, ntr2_ev, n2grp_ev, bi1, bi2)
        else:
            RES['T1e'] = dict(test='T1e', r1=None, N_obs_B1=float(nobs_ev[:, 14].sum()), branch='-> T3',
                              note='F0e>1.3 has < 10 B1 counts: the dE/dx family falls to T3 (WP_RULE §6.2)')
        RES['trend'] = trend_test(list(range(3, 14)), nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2)
        # union-count diagnostics at every rung (WP_RULE §2: diagnostics only)
        diag = []
        for c in range(NR):
            t = ln_ratio_test(npass1_ev, ntr1_ev, suni_ev, ntr2_ev, bi1, bi2, c)
            g = ln_ratio_test(nobs_ev, ntr1_ev, s2_ev, ntr2_ev, bi1, bi2, c) if c not in NOGRP else None
            diag.append(dict(rung=RUNGS[c], union=t, per_hit_set=g))
        RES['closure_all_columns'] = diag
        RES['readings']['T1_rung'] = (
            'T1 governs the counting rungs R01-R04 (WP_RULE §6.2 table, §6.4 "each family\'s test governs its own '
            'rungs"); per-hit-set counts are governing from R04 on (§2), so r1(T1) = R04. Reading B (T1 at the '
            'tightest ladder rung R04-R14 with >= 10 B1 counts) is also evaluated; the more severe branch is taken.')
        RES['readings']['lever_arm'] = (
            '"r1 = tightest rung with >= 10 B1 counts; if lever arm > 0.1 move to the next tighter rung with >= 10 B1 '
            'counts" has no tighter candidate by construction; a lever-arm failure at r1 is therefore taken directly '
            'as "no such rung" -> rung with the largest lever arm, closure failure of unknown direction '
            '(anti-conservative branch).')
        RES['readings']['z_B1_term'] = ('z uses 1/N_obs for the B1 term exactly as frozen; the B1 event-bootstrap '
                                        'sigma (4 correlated roads per event) is reported as a diagnostic z only.')

        # ---- IS run checks
        RES['is_checks'] = dict(meanW_pull_absmax=float(np.nanmax(np.abs(tr2['meanW_pull']))),
                                n_pull_ge3=int(np.sum(np.abs(tr2['meanW_pull']) >= 3)),
                                meanW_pull_T_absmax=float(np.nanmax(np.abs(tr2['meanW_pull_T'])))
                                if 'meanW_pull_T' in tr2 else None,
                                n_pull_T_ge3=int(np.sum(np.abs(tr2['meanW_pull_T']) >= 3)) if 'meanW_pull_T' in tr2
                                else None, n_trials=int(len(ev2)),
                                is_zero_draw_frac_mean=float(np.mean(tr2['is_zero_draw_frac'])))

    # ---- T3 (rung factorisation on B1, S2 records) at the tightest ladder rung with >= 10 B1 counts
    c1 = [c for c in range(3, 14) if nobs_ev[:, c].sum() >= 10]
    RES['T3'] = t3_test(data['G3B1'], c1[-1] if c1 else None, rng, a.nboot)

    # ---- factorisation / independence c-test (diagnostic at G3), SR-T (ii)
    RES['c_test'] = c_test(data['G3B1'], rng)
    if not a.no_srt:
        RES['srt'] = srt_test(data['G3B1'], rng)

    # ---- (iv) T_seed stability, C-4 nsub = 256
    RES['tseed'] = tseed_test(data, rng)
    RES['nsub256'] = nsub_test(data)

    # ---- V4-1, throughput, disk
    RES['v41'] = v41_summary(data)
    RES['throughput'] = throughput(data, tr1, tr2 if have_b2 else None)
    RES['disk_GB'] = dict(G3_prod=float(sum(f.stat().st_size for f in PROD.rglob('*.npz')) / 1e9),
                          rerun=float(sum(f.stat().st_size for f in RERUN.rglob('*.npz')) / 1e9) if RERUN.exists()
                          else 0.0)
    RES['decision'] = decide(RES) if have_b2 else None
    RES['runtime_s'] = time.time() - t_start
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(RES, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))
    print(json.dumps(dict(decision=RES['decision'], samples=RES['samples']), indent=1, default=str))
    print('wrote', a.out, 'in %.0f s' % RES['runtime_s'])
    return 0


def t3_test(jobs, r1, rng, nboot):
    """T3 (WP_RULE §6.4): predict r1 from r1 - 2 on B1 by step-3 factorisation: N_pred(r1) = N(r1-2) x
    p(a_{r1-1} | r1-2) x p(a_{r1} | r1-2) (each added requirement's conditional measured on the r1-2 population, as if
    r1-1 were below reach), compared with the direct count N(r1).  Counts per distinct hit set (group passes if any
    member passes).  Degenerate when a_{r1} tightens the same variable as a_{r1-1} (then a_{r1} implies a_{r1-1} and the
    prediction is p(a_{r1}|r1-2) N(r1-2) = N(r1) exactly)."""
    if r1 is None or r1 < 5:
        return dict(r1=None, note='no ladder rung >= R06 with >= 10 B1 counts')
    rows = []      # per event: N(r1-2), N(r1-2 & a1), N(r1-2 & a2), N(r1)
    for d in jobs:
        c = d['cand']
        s2 = (c['tag'] & 1) > 0
        req, aligned = req_flags(c)
        base = s2 & aligned
        for k in range(r1 - 1):
            base = base & req[k]
        A1 = base & req[r1 - 1]; A2 = base & req[r1]
        if VAR_OF[r1] == VAR_OF[r1 - 1]:
            A2 = A2 & req[r1 - 1]      # same variable: a_{r1} already implies a_{r1-1}; keep the cumulative flag
        full = A1 & req[r1]
        key = c['trial'].astype(np.int64) * 1_000_000 + c['group'].astype(np.int64)
        ev = d['tr']['ev'][c['trial']]
        evs = np.unique(d['tr']['ev'])
        for e in evs:
            me = ev == e
            row = []
            for m in (base, A1, A2, full):
                row.append(len(np.unique(key[me & m & (c['group'] >= 0)])))
            rows.append(row)
    R = np.array(rows, float)
    Nb, Na1, Na2, Nf = R.sum(0)
    degenerate = bool(VAR_OF[r1] == VAR_OF[r1 - 1])
    pred = (Na2 if degenerate else Na1 * Na2 / Nb) if Nb > 0 else 0.0
    out = dict(r1=RUNGS[r1], from_rung=RUNGS[r1 - 2], N_base=Nb, N_a1=Na1, N_a2=Na2, N_obs=Nf, N_pred=pred,
               degenerate=degenerate)
    if degenerate:
        out.update(z=0.0, pass_=None, informative=False,
                   note='a_{r1} tightens the same variable as a_{r1-1}: the step-3 prediction is exact by construction '
                        '(not informative). No non-degenerate T3 exists inside the S2 records (R04+) at G3 statistics: '
                        'R05 needs R03 (no S2 records), R09 needs R07 (0-few B1 counts).')
        return out
    # check of the S2-record flags against the stored cumulative rung flags
    mism = 0
    for d in jobs:
        c = d['cand']
        s2 = (c['tag'] & 1) > 0
        req, aligned = req_flags(c)
        cum = s2 & aligned
        F = np.unpackbits(c['rungs'], axis=1)[:, :NR].astype(bool)
        for k in range(14):
            cum = cum & req[k]
            mism += int(np.sum(cum != (F[:, k] & s2)))
    out['flag_recompute_mismatches'] = mism
    if Nf > 0 and pred > 0:
        bi = boot_idx(len(R), nboot, rng)
        Rb = R[bi].sum(1)
        pb = Rb[:, 1] * Rb[:, 2] / np.maximum(Rb[:, 0], 1)
        good = pb > 0
        s_ln = float(np.std(np.log(pb[good]), ddof=1))
        lnr = float(np.log(Nf / pred))
        z = lnr / np.sqrt(1 / Nf + s_ln ** 2)
        out.update(ln_r=lnr, s_ln_pred=s_ln, z=float(z), pass_=bool(abs(z) < 2))
    return out


def c_test(jobs, rng, nboot=100):
    """WP_RULE §6.4 factorisation/independence test on the B1 loose candidates (S3 sample passing R01): the joint
    probability of '>= 2 crossings' in pairs and triples of layers vs the product of the single-layer probabilities,
    in 3 bins of the trial's road-hit count; c = joint/product; flagged if c > 1 at 2 sigma (event bootstrap)."""
    from itertools import combinations
    X = []; B = []; EV = []
    evn = 0
    allroad = np.concatenate([d['tr']['n_road'] for d in jobs])
    q = np.quantile(allroad, [1 / 3, 2 / 3])
    for d in jobs:
        c = d['cand']
        F0 = np.unpackbits(c['rungs'][:, :1], axis=1)[:, 0].astype(bool)
        m = ((c['tag'] & 2) > 0) & F0
        X.append(c['cross'][m] >= 2)
        nr = d['tr']['n_road'][c['trial'][m]]
        B.append(np.digitize(nr, q))
        ue, inv = np.unique(d['tr']['ev'], return_inverse=True)
        EV.append(inv[c['trial'][m]] + evn); evn += len(ue)
    X = np.concatenate(X); B = np.concatenate(B); EV = np.concatenate(EV)
    combos = list(combinations(range(10), 2)) + list(combinations(range(10), 3))
    bi = boot_idx(evn, nboot, rng)
    res = []
    for b in range(3):
        mb = B == b
        Xe = X[mb]; Ee = EV[mb]
        n_ev = np.bincount(Ee, minlength=evn).astype(float)
        single = np.stack([np.bincount(Ee, weights=Xe[:, l], minlength=evn) for l in range(10)], 1)
        for cmb in combos:
            joint = np.bincount(Ee, weights=np.all(Xe[:, list(cmb)], axis=1), minlength=evn)
            N = n_ev.sum(); J = joint.sum(); S = single[:, list(cmb)].sum(0)
            if J == 0 or np.any(S == 0):
                continue
            cval = (J / N) / np.prod(S / N)
            Nb = n_ev[bi].sum(1); Jb = joint[bi].sum(1); Sb = single[:, list(cmb)][bi].sum(1)
            cb = (Jb / Nb) / np.prod(Sb / Nb[:, None], axis=1)
            sc = float(np.std(cb, ddof=1))
            res.append(dict(bin=b, layers=[int(x) for x in cmb], c=float(cval), s_c=sc, J=float(J),
                            sig=bool((cval - 1) > 2 * sc)))
    flagged = [r for r in res if r['sig']]
    cmax = max(res, key=lambda r: r['c']) if res else None
    return dict(n_loose=int(len(X)), n_tests=len(res), n_flagged=len(flagged), c_max=cmax,
                c_max_flagged=max(flagged, key=lambda r: r['c']) if flagged else None,
                note='diagnostic at G3: c multiplies the step-3 factorised estimates (post-production, §6.2), it does '
                     'not enter the G3 branch')


def srt_test(jobs, rng):
    """(ii) SR-T time-position independence on the loose rungs (plan §2.3, §11 G3 (ii); WP_RULE §1.4, §6.2)."""
    ker = _srt_kernel()
    hist = np.zeros(HN, np.int64)
    chk = dict(n_sel=0, n_mismatch_nband=0, max_abs_ddt0_ns=0.0)
    t0 = time.time()
    for d in jobs:
        h, ck = srt_hits(d, ker, 0.030, 75.0)
        hist += h
        chk['n_sel'] += ck['n_sel']; chk['n_mismatch_nband'] += ck['n_mismatch_nband']
        chk['max_abs_ddt0_ns'] = max(chk['max_abs_ddt0_ns'], ck['max_abs_ddt0_ns'])
    np.save(OUT / 'srt_dt_hist.npy', hist)
    tm_in = tmin_from_hist(hist, overlay=False)
    tm_ov = tmin_from_hist(hist, overlay=True)
    out = dict(kernel_check=chk, t_min_in_time=tm_in, t_min_with_overlay=tm_ov, seconds=time.time() - t0, tests={})
    # independence: late fraction of BTL-present loose candidates (S3 & R01) and of R04 candidates (S2) in bins
    for pop_name, bit, col in (('loose_S3_R01', 2, 0), ('R04_S2', 1, 3)):
        L = {}
        for d in jobs:
            c = d['cand']
            F = np.unpackbits(c['rungs'], axis=1)[:, :NR].astype(bool)
            m = ((c['tag'] & bit) > 0) & F[:, col] & (c['btl_n_band'] > 0)
            L.setdefault('dt0', []).append(c['btl_dt0'][m])
            L.setdefault('nip2', []).append(c['nip2'][m])
            L.setdefault('w', []).append(c['dw_core'][m])
            L.setdefault('p', []).append(c['p_chi2core'][m])
            L.setdefault('nroad', []).append(d['tr']['n_road'][c['trial'][m]])
            L.setdefault('ev', []).append(d['tr']['ev'][c['trial'][m]] + 1_000_000 * int(d['job']['chunk']))
        L = {k: np.concatenate(v).astype(float) for k, v in L.items()}
        res = dict(n_btl_present=int(len(L['dt0'])))
        for tag, tm in (('t_min_with_overlay', tm_ov['t_min_ns']), ('t_min_in_time', tm_in['t_min_ns'])):
            if tm is None:
                res[tag] = dict(note='t_min undefined (rate never below 1e-4 on [0, 25] ns)')
                continue
            late = (L['dt0'] >= tm) & (L['dt0'] <= DT_ACC)
            nip = np.clip(L['nip2'], 4, 7).astype(int) - 4
            E = L['ev']
            sub = dict(t_min=tm, n_late=int(late.sum()), late_frac=float(late.mean()),
                       by_nip2=indep_test(late, nip, rng, E), by_wcore=indep_test(late, tercile_bins(L['w']), rng, E),
                       by_chi2core_p=indep_test(late, tercile_bins(L['p']), rng, E),
                       by_density=indep_test(late, tercile_bins(L['nroad']), rng, E))
            ps = [v['p_value'] for k, v in sub.items() if k.startswith('by_') and v['p_value'] is not None]
            sub['all_pass'] = (all(p > 0.05 for p in ps) if ps else None)
            res[tag] = sub
        out['tests'][pop_name] = res
    out['readings'] = (
        'Per-hit late rate R(t) = in-band BTL hits of the B1 loose candidates (S3 & R01) with dt in [t, 25 ns] over all '
        'such hits; t_min = smallest t on a 5 ps grid with R < 1e-4 (R is non-increasing). The out-of-time overlay '
        '(k = -12..+3) is built as 15 independent copies of the measured in-time per-hit spectrum shifted by k x 25 ns '
        '(the overlay events are independent PU-200 events, so their in-band per-hit spectrum is the in-time one in '
        'expectation); no explicit overlay event mixing. Late candidate = earliest in-time in-band hit (stored '
        'btl_dt0) in [t_min, 25 ns]. Bins: N_IP2 in {<=4,5,6,7}, terciles of w_core, p(chi2_core) and road-hit count '
        '(not specified by the frozen text). Pass p > 0.05 (plan §2.3) per binning; governing p-value Rao-Scott '
        'corrected for event clustering (candidates of one trial share BTL hits; the naive binomial p is reported).')
    return out


def _pairs(data, tag):
    out = []
    for s in ('G3B1', 'G3B2'):
        for d in data[s]:
            p = RERUN / tag / (d['job_id'] + '.npz')
            if p.exists():
                out.append((s, d, p))
    return out


def tseed_test(data, rng, nboot=2000):
    """(iv) WP_RULE §6.4: per-family pass fractions at T_seed = 6 (stored) vs 4 (re-run), paired on identical events."""
    pr = _pairs(data, 'tseed4')
    if not pr:
        return dict(note='no T_seed = 4 re-run found', done=False)
    res = dict(done=True, jobs=[], rungs={})
    for s in ('G3B1', 'G3B2'):
        P6 = []; P4 = []; EV = []; evn = 0; repro = True; S6 = []; S4_ = []
        for s_, d, p in pr:
            if s_ != s:
                continue
            r = load_job(p, want_cand=False, rho=1 if s == 'G3B1' else 2)
            same_ev = np.array_equal(r.get('chain.evstats'), d.get('chain.evstats'))
            same_tr = bool(np.array_equal(r['tr']['ev'], d['tr']['ev']) and np.allclose(r['tr']['pv'], d['tr']['pv']))
            repro &= same_ev and same_tr
            res['jobs'].append(dict(job=d['job_id'], chain_evstats_identical=bool(same_ev), trials_identical=same_tr,
                                    tseed=r['meta']['finder_cfg']['tseed'], wall_s=r['meta']['wall_s'],
                                    t_find_mean_6=float(np.mean(d['tr']['t_total'])),
                                    t_find_mean_4=float(np.mean(r['tr']['t_total']))))
            g6 = np.where(d['tr']['n_grp'] < 0, d['tr']['n_pass'], d['tr']['n_grp'])
            g4 = np.where(r['tr']['n_grp'] < 0, r['tr']['n_pass'], r['tr']['n_grp'])
            P6.append(g6); P4.append(g4)
            ue, inv = np.unique(d['tr']['ev'], return_inverse=True)
            EV.append(inv + evn); evn += len(ue)
            if s == 'G3B2':
                S6.append(np.nan_to_num(np.where(np.isnan(d['tr']['S_ded']), d['tr']['S_uni'], d['tr']['S_ded'])))
                S4_.append(np.nan_to_num(np.where(np.isnan(r['tr']['S_ded']), r['tr']['S_uni'], r['tr']['S_ded'])))
        if not P6:
            continue
        P6 = np.concatenate(P6).astype(float); P4 = np.concatenate(P4).astype(float); EV = np.concatenate(EV)
        bi = boot_idx(evn, nboot, rng)
        rows = []
        metrics = [('pass_frac', (P6 > 0).astype(float), (P4 > 0).astype(float)), ('mean_grp', P6, P4)]
        if S6:
            metrics.append(('mean_S_ded', np.concatenate(S6), np.concatenate(S4_)))
        for name, A6, A4 in metrics:
            e6 = ev_sums(EV, A6, evn); e4 = ev_sums(EV, A4, evn); en = ev_sums(EV, np.ones(len(EV)), evn)
            for c in range(14):
                m6 = e6[:, c].sum() / en.sum(); m4 = e4[:, c].sum() / en.sum()
                b6 = e6[bi, c].sum(1) / en[bi].sum(1); b4 = e4[bi, c].sum(1) / en[bi].sum(1)
                sd_pair = float(np.std(b4 - b6, ddof=1)); sd_unp = float(np.hypot(np.std(b6, ddof=1), np.std(b4, ddof=1)))
                zp = (m4 - m6) / sd_pair if sd_pair > 0 else (0.0 if m4 == m6 else np.inf)
                zu = (m4 - m6) / sd_unp if sd_unp > 0 else (0.0 if m4 == m6 else np.inf)
                rows.append(dict(sample=s, metric=name, rung=RUNGS[c], v6=float(m6), v4=float(m4),
                                 rel=float(m4 / m6 - 1) if m6 > 0 else None, z_paired=float(zp), z_unpaired=float(zu),
                                 moved=bool(abs(zp) > 2)))
        res['rungs'][s] = rows
        res[s + '_reproducible'] = bool(repro)
        res[s + '_n_trials'] = int(len(P6))
    fam_of = {RUNGS[c]: f for f, cs in FAM.items() for c in cs}
    moved = [r for s in res['rungs'] for r in res['rungs'][s] if r['moved']]
    moved_pf = [r for r in moved if r['metric'] == 'pass_frac']
    res['moved_any_metric'] = [(r['sample'], r['metric'], r['rung'], fam_of[r['rung']], round(r['z_paired'], 2))
                               for r in moved]
    res['moved_pass_frac'] = [(r['sample'], r['rung'], round(r['z_paired'], 2)) for r in moved_pf]
    res['action_triggered_literal'] = bool(moved_pf)
    res['action_triggered_conservative'] = bool(moved)
    res['reading'] = ('"pass fraction" literally = fraction of trials with >= 1 passing distinct hit set (the primary '
                      'per-trial P_fake indicator); the conservative reading also tests the mean number of passing '
                      'sets per trial (the union-bound P-hat that B uses; S_ded at rho = 2). sigma = paired event '
                      'bootstrap of the difference (identical events; the unpaired sigma is reported). Families that '
                      'matter: counting N_IP2 (R01-R04), N_2S2 (R12-R14), width (R05-R08), chi2_core (R09-R11).')
    return res


def nsub_test(data):
    pr = [x for x in _pairs(data, 'nsub256') if x[0] == 'G3B2']
    if not pr:
        return dict(note='no nsub = 256 re-run found', done=False)
    rows = []
    a64 = []; a256 = []
    for s, d, p in pr:
        r = load_job(p, want_cand=False, rho=2)
        a64.append(d['tr']['S_ded']); a256.append(r['tr']['S_ded'])
    a64 = np.concatenate(a64); a256 = np.concatenate(a256)
    for c in range(3, 14):
        s64 = float(np.nansum(a64[:, c])); s256 = float(np.nansum(a256[:, c]))
        rows.append(dict(rung=RUNGS[c], S_ded_64=s64, S_ded_256=s256, ratio=s256 / s64 if s64 > 0 else None))
    return dict(done=True, jobs=[x[1]['job_id'] for x in pr], n_trials=int(len(a64)), rows=rows,
                note='WP_RULE §6.3 C-4: S_ded takes the max of noisy IS means (biased up, conservative); ratio < 1 '
                     'measures that bias. Diagnostic, reported only.')


def v41_summary(data):
    out = {}
    for s in data:
        fails = [d['job_id'] for d in data[s] if d['meta'].get('v41_pass') is not True]
        V = np.concatenate([d['chain.v41'] for d in data[s] if 'chain.v41' in d]) if data[s] else np.zeros((0, 13))
        cols = [str(c) for c in data[s][0]['chain.v41_cols']] if data[s] else []
        agg = {}
        if len(V):
            for i, cname in enumerate(cols):
                if cname in ('map_injective',):
                    agg[cname + '_all'] = bool(np.all(V[:, i] == 1))
                elif cname in ('max_onsurf_um',):
                    agg[cname] = float(V[:, i].max())
                elif cname in ('n_unmapped_geo', 'n_causal_viol', 'n_sig_simhits', 'n_sig_meas'):
                    agg[cname + '_sum'] = float(V[:, i].sum())
                else:
                    agg[cname + '_mean'] = float(V[:, i].mean())
        out[s] = dict(n_jobs=len(data[s]), n_v41_fail=len(fails), fails=fails, n_events=int(len(V)), agg=agg)
    return out


def throughput(data, tr1, tr2):
    prog = []
    for p in glob.glob(str(PROD / '_progress_*.jsonl')):
        for line in open(p):
            try:
                prog.append(json.loads(line))
            except ValueError:
                pass
    starts = [x['t'] for x in prog if x.get('event') == 'start']
    done = [x for x in prog if x.get('event') == 'done']
    out = dict(n_done_records=len(done))
    if starts and done:
        st = max(starts)
        dn = [x for x in done if x['t'] >= st]
        el = max(x['t'] for x in dn) - st
        out.update(start=time.strftime('%Y-%m-%d %H:%M', time.localtime(st)),
                   last_done=time.strftime('%Y-%m-%d %H:%M', time.localtime(max(x['t'] for x in dn))),
                   elapsed_h=el / 3600, sum_job_wall_h=sum(x['wall'] for x in dn) / 3600,
                   sum_est_h=sum(x['est'] for x in dn) / 3600,
                   wall_over_est=sum(x['wall'] for x in dn) / sum(x['est'] for x in dn),
                   est_cpu_s_per_wall_s=sum(x['est'] for x in dn) / el)
        for s in ('G3B1', 'G3B2'):
            ds = [x for x in dn if x['id'].startswith(s)]
            if ds:
                out[s] = dict(n=len(ds), wall_mean_s=float(np.mean([x['wall'] for x in ds])),
                              t_chain_mean_s=float(np.mean([x['t_chain'] for x in ds])),
                              wall_over_est=sum(x['wall'] for x in ds) / sum(x['est'] for x in ds),
                              MB_mean=float(np.mean([x.get('bytes', 0) for x in ds]) / 1e6))
    out['t1_finder_s'] = dict(mean=float(np.mean(tr1['t_total'])), median=float(np.median(tr1['t_total'])),
                              q90=float(np.quantile(tr1['t_total'], 0.9)), n=int(len(tr1['t_total'])))
    if tr2 is not None:
        out['t2_finder_weights_s'] = dict(mean=float(np.mean(tr2['t_total'])), median=float(np.median(tr2['t_total'])),
                                          q90=float(np.quantile(tr2['t_total'], 0.9)), n=int(len(tr2['t_total'])))
    out['chain_s_per_event'] = {s: float(np.mean([d['meta']['t_chain_s'] / (d['job']['n_events'] * d['job']['rho'])
                                                  for d in data[s]])) for s in data if data[s]}
    out['note'] = ('under production load: 7 workers on a MacBook Air M3 (4P + 4E); t1/t2 = in-job finder (+ weights) '
                   'time per trial from trials.t_total; chain time per PU event from meta.t_chain_s')
    return out


def decide(R):
    fam = {}
    for k in ('T1', 'T1w'):
        fam[k] = R[k].get('branch')
    worst_T1 = max([R['T1'].get('branch'), R['T1_tightest_ladder_rung_diag'].get('branch')],
                   key=lambda b: SEVERITY.get(b, 3))
    fam['T1_conservative_reading'] = worst_T1
    tr = R['trend']
    trend = None
    if tr.get('significant'):
        trend = 'anti-conservative trend' if tr['direction'] == 'anti-conservative' else 'conservative trend'
    ts = R['tseed']
    tseed_flag = ts.get('action_triggered_literal') if ts.get('done') else None
    srt = R.get('srt', {})
    return dict(family_branches=fam, trend=trend, tseed_action_literal=tseed_flag,
                tseed_action_conservative=ts.get('action_triggered_conservative') if ts.get('done') else None,
                T3=R['T3'].get('pass_'), admission_all_ok=R['admission']['all_ok'],
                reach=R.get('reach_rho2', {}).get('deepest_reachable'))


if __name__ == '__main__':
    raise SystemExit(main())
