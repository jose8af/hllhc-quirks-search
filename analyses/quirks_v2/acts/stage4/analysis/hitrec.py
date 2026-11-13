"""hitrec.py -- offline quantities from the stored full hit records (WP_RULE §S S4 / S7): core membership, the
pre-declared signal match, and the F1 variables h (non-helicity) and o (opening linearity) of WP_RULE §1.4 [D6].

Hit records (run_stage4.pack): hit.trial / hit.cand (finder candidate index) / hit.off (CSR into hit.ref) / hit.ref
(rows of the per-file union hit table hit.xyz, hit.sid, hit.s01, hit.dE, hit.INT, hit.particle, hit.gen, hit.t).
The compact record of the same candidate is cand.* with the same (trial, idx).

Core (WP_RULE §1.1 items 6-7, as in g1b_tt.core_mask and kernels.cand_vars): IT+PS in-band hits with
|u.n2 - c| <= 2.5 w_core (c = median, w_core = 1.4826 MAD over IT+PS), plus 2S hits within that interval enlarged by
3 |n2_z| sigma_1.  Recomputed here from float32 xyz / normal / axis (stored precision); the self-check compares the
recomputed w_core and n_core with the stored cand.dw_core / cand.n_core.

Signal match (pre-declared, LOG 2026-10-13 20:35, before any signal efficiency): a candidate is signal-matched only if
>= 3 of its CORE hits, in >= 3 distinct layers, are quirk hits AND quirk hits are >= 50 % of its core hits.  A pool
hit is a quirk hit iff its stored interaction id is the quirk one (INT % 10^6 == 4000; a U-5 b merged measurement
carries the id of its largest-dE member -- frozen chain_inputs convention).
"""
import numpy as np
from scipy.optimize import least_squares

from acts.stage4.analysis.common import FF, SIG_VP

LC_OF = FF.LC_OF


def iter_records(d):
    """Yield (record index k, trial, cand idx, hit row indices) for every stored full hit record of a file."""
    if 'hit.off' not in d:
        return
    off = d['hit.off']; ref = d['hit.ref']
    for k in range(len(d['hit.cand'])):
        yield k, int(d['hit.trial'][k]), int(d['hit.cand'][k]), ref[off[k]:off[k + 1]]


def cand_lookup(d, prefix='cand.'):
    """(trial, idx) -> row of the compact records."""
    tr = d[prefix + 'trial'].astype(np.int64); ix = d[prefix + 'idx'].astype(np.int64)
    return {(int(a), int(b)): i for i, (a, b) in enumerate(zip(tr, ix))}


def geom(d, h, pv, normal, axis):
    """Per-hit geometry about the candidate plane: u, n2 coordinate, layer, IT+PS flag, sigma_1, n2-projected sigma."""
    xyz = d['hit.xyz'][h].astype(np.float64)
    u = xyz - pv[None, :]
    n = np.asarray(normal, np.float64); a = np.asarray(axis, np.float64)
    n2 = np.cross(n, a)
    wv = u @ n2
    sid = d['hit.sid'][h].astype(np.int64)
    LC = LC_OF[sid]
    s01 = d['hit.s01'][h].astype(np.float64)
    r = np.hypot(xyz[:, 0], xyz[:, 1])
    cx = xyz[:, 0] / r; cy = xyz[:, 1] / r
    s_n2 = np.sqrt((-n2[0] * cy + n2[1] * cx) ** 2 * s01[:, 0] ** 2 + n2[2] ** 2 * s01[:, 1] ** 2)
    return dict(xyz=xyz, u=u, n=n, a=a, n2=n2, wv=wv, LC=LC, ip=LC <= 6, s0=s01[:, 0], s1=s01[:, 1], s_n2=s_n2,
                cx=cx, cy=cy)


def core(g):
    """-> (core mask, centre c, w_core) exactly as g1b_tt.core_mask (needs >= 3 IT+PS hits, else empty core)."""
    ip = g['ip']; wv = g['wv']
    cm = np.zeros(len(wv), bool)
    if ip.sum() <= 2:
        return cm, np.nan, np.nan
    wi = wv[ip]
    c = float(np.median(wi))
    s = float(1.4826 * np.median(np.abs(wi - c)))
    lo = c - 2.5 * s; hi = c + 2.5 * s
    s2 = np.abs(g['n2'][2]) * g['s1']
    cm = np.where(ip, (wv >= lo) & (wv <= hi), (wv >= lo - 3 * s2) & (wv <= hi + 3 * s2))
    return cm, c, s


def signal_match(d, h, g, cm):
    """Pre-declared match on the core hits.  -> (matched, n_core, n_q_core, n_q_core_layers)."""
    q = (d['hit.INT'][h].astype(np.int64) % 1_000_000) == SIG_VP
    nq = int((q & cm).sum()); nc = int(cm.sum())
    nl = int(len(np.unique(g['LC'][q & cm])))
    return bool(nq >= 3 and nl >= 3 and nq >= 0.5 * nc), nc, nq, nl


# ------------------------------------------------------------------------------------------------ F1: h
def _circ_resid(params, P, pv, e1, e2, xyz, s0, s1, free):
    """Helix residuals: circle in the transverse (x, y) plane + straight line in (s, z) (WP_RULE §1.4).
    PV origin (free=False): params (kappa, phi0, tanl), origin = PV.  Free origin (free=True): params
    (kappa, phi0, tanl, alpha, beta), origin = PV + alpha e1 + beta e2 (a point ON the candidate plane)."""
    if free:
        k, ph, tl, al, be = params
        o = pv + al * e1 + be * e2
    else:
        k, ph, tl = params
        o = pv
    dx = xyz[:, 0] - o[0]; dy = xyz[:, 1] - o[1]
    c, s = np.cos(ph), np.sin(ph)
    xp = dx * c + dy * s; yp = -dx * s + dy * c
    f = 0.5 * k * (xp * xp + yp * yp) - yp
    gn = np.sqrt(np.maximum(k * k * (xp * xp + yp * yp) - 2 * k * yp + 1.0, 1e-12))
    r_t = f / gn
    if abs(k) > 1e-9:
        sarc = np.arctan2(k * xp, 1.0 - k * yp) / k
    else:
        sarc = xp
    r_z = (xyz[:, 2] - o[2]) - tl * sarc
    return np.concatenate([r_t / s0, r_z / s1])


def helix_chi2(xyz, s0, s1, pv, e1, e2, free):
    n = len(xyz)
    npar = 5 if free else 3
    if 2 * n - npar <= 0:
        return np.nan, 2 * n - npar
    d = xyz[:, :2] - pv[None, :2]
    ph0 = float(np.arctan2(d[:, 1].mean(), d[:, 0].mean()))
    rr = np.hypot(d[:, 0], d[:, 1])
    tl0 = float(np.sum((xyz[:, 2] - pv[2]) * rr) / max(np.sum(rr * rr), 1e-9))
    x0 = [0.0, ph0, tl0] + ([0.0, 0.0] if free else [])
    try:
        r = least_squares(_circ_resid, x0, args=(None, pv, e1, e2, xyz, s0, s1, free), method='lm', max_nfev=400)
        chi2 = float(np.sum(r.fun ** 2))
    except Exception:                                           # noqa: BLE001
        return np.nan, 2 * n - npar
    return chi2, 2 * n - npar


def h_var(g, c, pv):
    """h = min over hypotheses H in {PV origin (3 par), free origin on the plane (5 par)} of
    sum_subsets chi2 / sum_subsets (2 n_s - n_par); subsets = the two sides sign(u.n2 - c) of all in-band hits.
    Undefined (-> NaN, which PASSES every h rung): a non-empty subset with < 3 hits, or ndf_H <= 0 for both H."""
    if not np.isfinite(c):
        return np.nan
    side = g['wv'] - c >= 0
    subs = [np.where(side)[0], np.where(~side)[0]]
    subs = [s for s in subs if len(s)]
    if any(len(s) < 3 for s in subs):
        return np.nan
    e1 = g['a']; e2 = g['n2']
    best = np.inf
    for free in (False, True):
        chi = 0.0; ndf = 0; ok = True
        for s in subs:
            c2, nd = helix_chi2(g['xyz'][s], np.maximum(g['s0'][s], 1e-4), np.maximum(g['s1'][s], 1e-4), pv, e1, e2,
                                free)
            if not np.isfinite(c2):
                ok = False; break
            chi += c2; ndf += nd
        if ok and ndf > 0:
            best = min(best, chi / ndf)
    return float(best) if np.isfinite(best) else np.nan


# ------------------------------------------------------------------------------------------------ F1: o
def o_var(g, c):
    """o = chi2_lin/ndf of s_l = a (r_l - r0), a >= 0, r0 <= r_min, over the resolvable layers (IT + PS only; never 2S)
    with two clusters (sign(u.n2 - c)); s_l = |difference of the two cluster means along n2|, sigma_l from the hit
    errors projected on n2; r_l = mean transverse radius of the layer's hits; ndf = n_layers - 2.
    Undefined (< 4 resolvable two-cluster layers) -> NaN, which PASSES every o rung."""
    if not np.isfinite(c):
        return np.nan
    S, R, E = [], [], []
    for lay in range(7):
        m = g['LC'] == lay
        if not m.any():
            continue
        w = g['wv'][m] - c
        p = w >= 0; q = ~p
        if not p.any() or not q.any():
            continue
        sp = g['s_n2'][m]
        S.append(abs(w[p].mean() - w[q].mean()))
        E.append(np.sqrt(np.sum(sp[p] ** 2) / p.sum() ** 2 + np.sum(sp[q] ** 2) / q.sum() ** 2 + 1e-8))
        R.append(float(np.hypot(g['u'][m, 0], g['u'][m, 1]).mean()))
    if len(S) < 4:
        return np.nan
    S = np.array(S); R = np.array(R); E = np.array(E)
    rmin = float(R.min())

    def res(p):
        return (S - p[0] * (R - p[1])) / E
    a0 = max(float(np.polyfit(R, S, 1)[0]), 0.0)
    x0 = [a0, min(rmin - 1.0, float(R.min() - S.min() / a0) if a0 > 0 else rmin - 1.0)]
    try:
        r = least_squares(res, x0, bounds=([0.0, -np.inf], [np.inf, rmin]), max_nfev=400)
        chi2 = float(np.sum(r.fun ** 2))
    except Exception:                                           # noqa: BLE001
        return np.nan
    return chi2 / (len(S) - 2)


def record_vars(d, k, trial, h, pv, normal, axis, want_f1=True, want_match=False):
    """All offline per-record quantities of one stored candidate."""
    g = geom(d, h, pv, normal, axis)
    cm, c, w = core(g)
    out = dict(w_core_re=w, n_core_re=int(cm.sum()))
    if want_match:
        mt, nc, nq, nl = signal_match(d, h, g, cm)
        out.update(matched=mt, n_q_core=nq, n_q_core_layers=nl)
    if want_f1:
        out['h'] = h_var(g, c, pv)
        out['o'] = o_var(g, c)
    return out


def f1_pass(hv, ov, h_min=None, o_min=None):
    """Rung flags with the 'undefined passes' rule (WP_RULE §1.4 [D6])."""
    ph = True if h_min is None else (not np.isfinite(hv)) or hv > h_min
    po = True if o_min is None else (not np.isfinite(ov)) or ov > o_min
    return bool(ph and po)


def sep_it(g, c, cm=None):
    """sep_IT^det (plan §11 item 4): per IT layer (TBPX L1-L4) with two in-plane clusters (sign(u.n2 - c)), the
    separation |mean(+) - mean(-)| along n2; the median over those layers (mm).  NaN if no IT layer has two clusters.
    FIX R6 (INV_SIGNAL_EFF §5): only the CORE hits (cm) enter; the frozen version split every in-band hit, so under
    PU the +-W_c band of PU hits set the 'cluster means' (41-58 mm flat in Lambda).  Even core-only stays PU-dominated
    (13-20 mm vs 1-7 mm truth at E500): products.sep_it_det flags the PU-200 values NOT MEASURABLE."""
    if not np.isfinite(c):
        return np.nan
    S = []
    for lay in range(4):
        m = g['LC'] == lay
        if cm is not None:
            m = m & cm
        if not m.any():
            continue
        w = g['wv'][m] - c
        p = w >= 0
        if p.any() and (~p).any():
            S.append(abs(w[p].mean() - w[~p].mean()))
    return float(np.median(S)) if S else np.nan
