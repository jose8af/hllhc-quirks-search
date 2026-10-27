"""nm_crossings.py -- E2: per-crossing analysis of recorded quirk-pair world lines (causal kernel or conformal solver).

Input: two "tracks" (one per quirk) of recorded rows in the LAB frame, plus the frame P0 (total 4-momentum at the
crossings; for a neutral pair in uniform B, p1 + p2 = P_can = P0 whenever x1 = x2 and the string is collapsed).
  causal rows    : [X^4, P^4, s^4, J^4]  (state before a step, absorbed null vector, cumulative string impulse)
                   positions/momenta inside a step from the exact Athena map (covariant, applied in the CM frame):
                   x(l) = X + 2 l (s.p)(p + F l s)/(m^2 + 2 F l s.p),  p(l) = a - F s_out(l),  a = p + F l s
  conformal rows : [tau, X^4, P^4, dX/dtau^4, J^4] -> cubic Hermite in tau between consecutive rows
Output per crossing k = 1, 2, ... (crossing 0 = production):
  t*_k (CM time of closest approach), b_k (|x1* - x2*| minimised at equal CM time; vector components on the
  fixed basis eN = unit(n0 x beta_hat) [normal of the lab pair plane], eP = eN x n0, and on the axis a_k),
  angle of b to E*_perp, v1*, v2*, gamma*_1, relative speed, axis a_k = (-1)^k unit(v1* - v2*),
  separation amplitude l_k (max equal-CM-time separation in the half period before crossing k),
  turning-point apse vectors, transverse impulse profile dPi(tau) = Pi(t_k + tau) - Pi(t_k - tau) of
  Pi = (p1* - p2*)/2 (total, string part from J, Lorentz part = rest), turning-point-to-turning-point impulse.
Library; used by M1_events.py, M2_single.py, M4_convergence.py.
"""
import numpy as np
from numba import njit


def boost_to_rest(P0):
    """4x4 Lorentz matrix L with L @ P0 = (M, 0, 0, 0)."""
    P0 = np.asarray(P0, float)
    E = P0[0]; p = P0[1:]
    M = np.sqrt(E * E - p @ p)
    b = p / E; b2 = b @ b
    L = np.eye(4)
    if b2 <= 0:
        return L
    g = E / M
    L[0, 0] = g; L[0, 1:] = -g * b; L[1:, 0] = -g * b
    L[1:, 1:] += (g - 1) * np.outer(b, b) / b2
    return L


@njit(cache=True, inline='always')
def _md(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


@njit(cache=True)
def consec_flags_causal(R, m, F, tol):
    n = R.shape[0]
    out = np.zeros(n, np.bool_)
    for i in range(n - 1):
        X = R[i, 0:4]; p = R[i, 4:8]; s = R[i, 8:12]
        sp = _md(s, p)
        den = m * m + 2 * F * sp
        err = 0.0; sc = 0.0
        for c in range(4):
            xe = X[c] + 2 * sp / den * (p[c] + F * s[c])
            err = max(err, abs(xe - R[i + 1, c]))
            sc = max(sc, abs(R[i + 1, c]))
        out[i] = err <= tol * (1.0 + sc)
    return out


@njit(cache=True)
def _causal_state(R, i, lam, m, F, out):
    """out[0:4] = x(lam), out[4:8] = p(lam), out[8:12] = J(lam) for row i (CM frame)."""
    X = R[i, 0:4]; p = R[i, 4:8]; s = R[i, 8:12]; J = R[i, 12:16]
    sp = _md(s, p)
    den = m * m + 2 * F * lam * sp
    for c in range(4):
        a = p[c] + F * lam * s[c]
        out[c] = X[c] + 2 * lam * sp / den * a
        so = 2 * lam * sp / den * a - lam * s[c]
        out[4 + c] = a - F * so
        out[8 + c] = J[c] + F * (lam * s[c] - so)


@njit(cache=True)
def state_at_causal(R, cons, tq, m, F, out):
    """State of a causal track at CM time tq (R rows in the CM frame, sorted in time). Returns flag:
    0 exact intra-step, 1 linear interpolation between non-consecutive rows, 2 outside."""
    n = R.shape[0]
    if tq < R[0, 0] or tq > R[n - 1, 0]:
        for c in range(12):
            out[c] = np.nan
        return 2
    lo = 0; hi = n - 1
    while hi - lo > 1:
        md = (lo + hi) // 2
        if R[md, 0] <= tq:
            lo = md
        else:
            hi = md
    i = lo
    if cons[i]:
        a = 0.0; b = 1.0
        for it in range(70):
            mid = 0.5 * (a + b)
            _causal_state(R, i, mid, m, F, out)
            if out[0] < tq:
                a = mid
            else:
                b = mid
        _causal_state(R, i, 0.5 * (a + b), m, F, out)
        return 0
    f = (tq - R[i, 0]) / max(R[i + 1, 0] - R[i, 0], 1e-300)
    for c in range(4):
        out[c] = R[i, c] + f * (R[i + 1, c] - R[i, c])
        out[4 + c] = R[i, 4 + c] + f * (R[i + 1, 4 + c] - R[i, 4 + c])
        out[8 + c] = R[i, 12 + c] + f * (R[i + 1, 12 + c] - R[i, 12 + c])
    return 1


@njit(cache=True)
def _herm(x0, x1, d0, d1, s):
    h00 = 2 * s ** 3 - 3 * s ** 2 + 1; h10 = s ** 3 - 2 * s ** 2 + s
    h01 = -2 * s ** 3 + 3 * s ** 2; h11 = s ** 3 - s ** 2
    return h00 * x0 + h10 * d0 + h01 * x1 + h11 * d1


@njit(cache=True)
def state_at_conf(R, cons, tq, out):
    """Conformal rows [tau, X^4, P^4, dX/dtau^4, J^4] (CM frame). Hermite in tau for consecutive rows."""
    n = R.shape[0]
    if tq < R[0, 1] or tq > R[n - 1, 1]:
        for c in range(12):
            out[c] = np.nan
        return 2
    lo = 0; hi = n - 1
    while hi - lo > 1:
        md = (lo + hi) // 2
        if R[md, 1] <= tq:
            lo = md
        else:
            hi = md
    i = lo
    h = R[i + 1, 0] - R[i, 0]
    if cons[i]:
        a = 0.0; b = 1.0
        for it in range(70):
            mid = 0.5 * (a + b)
            t = _herm(R[i, 1], R[i + 1, 1], h * R[i, 9], h * R[i + 1, 9], mid)
            if t < tq:
                a = mid
            else:
                b = mid
        sx = 0.5 * (a + b)
        for c in range(4):
            out[c] = _herm(R[i, 1 + c], R[i + 1, 1 + c], h * R[i, 9 + c], h * R[i + 1, 9 + c], sx)
            out[4 + c] = R[i, 5 + c] + sx * (R[i + 1, 5 + c] - R[i, 5 + c])
            out[8 + c] = R[i, 13 + c] + sx * (R[i + 1, 13 + c] - R[i, 13 + c])
        return 0
    f = (tq - R[i, 1]) / max(R[i + 1, 1] - R[i, 1], 1e-300)
    for c in range(4):
        out[c] = R[i, 1 + c] + f * (R[i + 1, 1 + c] - R[i, 1 + c])
        out[4 + c] = R[i, 5 + c] + f * (R[i + 1, 5 + c] - R[i, 5 + c])
        out[8 + c] = R[i, 13 + c] + f * (R[i + 1, 13 + c] - R[i, 13 + c])
    return 1


@njit(cache=True)
def coarse_causal(R1, R2, cons2, n0, m, F, i0, i1):
    out = np.empty((i1 - i0, 2)); buf = np.zeros(12)
    for j in range(i1 - i0):
        i = i0 + j
        state_at_causal(R2, cons2, R1[i, 0], m, F, buf)
        dx = R1[i, 1] - buf[1]; dy = R1[i, 2] - buf[2]; dz = R1[i, 3] - buf[3]
        out[j, 0] = dx * n0[0] + dy * n0[1] + dz * n0[2]
        out[j, 1] = np.sqrt(dx * dx + dy * dy + dz * dz)
    return out


@njit(cache=True)
def coarse_conf(R1, R2, cons2, n0, i0, i1):
    out = np.empty((i1 - i0, 2)); buf = np.zeros(12)
    for j in range(i1 - i0):
        i = i0 + j
        state_at_conf(R2, cons2, R1[i, 1], buf)
        dx = R1[i, 2] - buf[1]; dy = R1[i, 3] - buf[2]; dz = R1[i, 4] - buf[3]
        out[j, 0] = dx * n0[0] + dy * n0[1] + dz * n0[2]
        out[j, 1] = np.sqrt(dx * dx + dy * dy + dz * dz)
    return out


class Track:
    """One quirk's recorded world line, converted to the CM frame of P0."""

    def __init__(self, rows, kind, L, m, F, h_conf=None):
        self.kind = kind; self.m = float(m); self.F = float(F)
        R = np.array(rows, float, copy=True)
        if kind == 'causal':
            for j in range(4):
                R[:, 4 * j:4 * j + 4] = R[:, 4 * j:4 * j + 4] @ L.T
            self.R = R
            # consecutive-step flags (computed after the boost; tolerance relative)
            self.cons = consec_flags_causal(R, self.m, self.F, 1e-11)
            self.t = R[:, 0]
        else:
            for j in range(4):
                R[:, 1 + 4 * j:5 + 4 * j] = R[:, 1 + 4 * j:5 + 4 * j] @ L.T
            self.R = R
            n = len(R)
            dtau = np.diff(R[:, 0])
            h0 = h_conf
            self.cons = np.r_[np.abs(dtau - h0) < 1e-6 * h0, False]
            self.t = R[:, 1]
        self.buf = np.zeros(12)

    def state(self, tq):
        if self.kind == 'causal':
            fl = state_at_causal(self.R, self.cons, float(tq), self.m, self.F, self.buf)
        else:
            fl = state_at_conf(self.R, self.cons, float(tq), self.buf)
        return self.buf[0:4].copy(), self.buf[4:8].copy(), self.buf[8:12].copy(), fl


def analyse(rows1, rows2, kind, P0, m, F, n0, eN=None, Estar=None, ncross_max=None, tau_fracs=None,
            Th=None, p_init=None, h_conf=None):
    """Per-crossing table.  n0: initial CM axis (unit 3-vector, quirk 1 direction at production or a given axis).
    eN: out-of-plane unit vector (default unit(n0 x beta_hat)); Estar: CM electric field vector (GeV/cm per unit
    charge) used for the angle of b; Th: CM half period (2 p*/sigma); p_init: (p1_lab4, p2_lab4) initial momenta."""
    L = boost_to_rest(P0)
    T1 = Track(rows1, kind, L, m, F, h_conf); T2 = Track(rows2, kind, L, m, F, h_conf)
    n0 = np.asarray(n0, float); n0 = n0 / np.linalg.norm(n0)
    bvec = np.asarray(P0[1:], float) / P0[0]
    if eN is None:
        bh = bvec / np.linalg.norm(bvec)
        eN = np.cross(n0, bh)
    eN = np.asarray(eN, float); eN = eN - (eN @ n0) * n0; eN /= np.linalg.norm(eN)
    eP = np.cross(eN, n0)
    if tau_fracs is None:
        tau_fracs = np.logspace(-5, np.log10(0.45), 30)
    # initial momenta (CM) for the Lorentz-impulse bookkeeping
    p10 = L @ p_init[0]; p20 = L @ p_init[1]
    # coarse longitudinal separation on quirk-1 row times
    t1 = T1.t
    tlo = max(T1.t[0], T2.t[0]); thi = min(T1.t[-1], T2.t[-1])
    sel = np.where((t1 > tlo) & (t1 < thi))[0]
    if len(sel) == 0:
        return dict(crossings=[], eN=eN, eP=eP, n0=n0, tps=[])
    i0, i1 = sel[0], sel[-1] + 1
    if kind == 'causal':
        co = coarse_causal(T1.R, T2.R, T2.cons, n0, float(m), float(F), i0, i1)
    else:
        co = coarse_conf(T1.R, T2.R, T2.cons, n0, i0, i1)
    sel = np.arange(i0, i1)
    zeta = co[:, 0]; sep = co[:, 1]
    ts = t1[sel]
    sgn = np.sign(zeta)
    idx = np.where(sgn[:-1] * sgn[1:] < 0)[0]
    if Th is not None:
        idx = idx[ts[idx] > 0.3 * Th]
    # also drop spurious double sign changes closer than 0.3 Th
    keep = []
    for i in idx:
        if keep and Th is not None and ts[i] - ts[keep[-1]] < 0.3 * Th:
            continue
        keep.append(i)
    idx = np.array(keep, int)
    if ncross_max is not None:
        idx = idx[:ncross_max]
    crossings = []
    for kk, i in enumerate(idx):
        k = kk + 1
        # linear guess for the zero of zeta, then Newton on d/dt |dx|^2 with exact positions
        tg = ts[i] - zeta[i] * (ts[i + 1] - ts[i]) / (zeta[i + 1] - zeta[i])
        flag = 0
        for it in range(8):
            x1, p1, _, f1 = T1.state(tg); x2, p2, _, f2 = T2.state(tg)
            flag = max(flag, f1, f2)
            v1 = p1[1:] / p1[0]; v2 = p2[1:] / p2[0]
            dx = x1[1:] - x2[1:]; dvv = v1 - v2
            dt = -(dx @ dvv) / (dvv @ dvv)
            tg = tg + dt
            if abs(dt) < 1e-15 * (1 + abs(tg)):
                break
        x1, p1, J1, f1 = T1.state(tg); x2, p2, J2, f2 = T2.state(tg)
        flag = max(flag, f1, f2)
        v1 = p1[1:] / p1[0]; v2 = p2[1:] / p2[0]
        b = x1[1:] - x2[1:]
        ak = (-1) ** k * (v1 - v2) / np.linalg.norm(v1 - v2)
        vrel = np.linalg.norm(v1 - v2) / (1 - v1 @ v2)  # collinear relativistic relative speed (approx)
        g1 = p1[0] / m
        bperp = b - (b @ ak) * ak
        bh = bperp / max(np.linalg.norm(bperp), 1e-300)
        row = dict(k=k, parity=int(k % 2), t=tg, flag=int(flag), b=float(np.linalg.norm(bperp)),
                   b_raw=float(np.linalg.norm(b)), bN=float(b @ eN), bP=float(b @ eP), bA=float(b @ ak),
                   aN=float(ak @ eN), aP=float(ak @ eP), gamma1=float(g1), gamma2=float(p2[0] / m),
                   v1=float(np.linalg.norm(v1)), vrel=float(vrel), pstar=float(np.linalg.norm(p1[1:])),
                   r_lab=float(np.hypot(*(np.linalg.inv(L) @ x1)[1:3])))
        if Estar is not None:
            Ep = np.asarray(Estar) - (np.asarray(Estar) @ ak) * ak
            row['cos_b_E'] = float((bperp @ Ep) / max(np.linalg.norm(bperp) * np.linalg.norm(Ep), 1e-300))
            row['E_perp'] = float(np.linalg.norm(Ep))
        # transverse impulse profile around the crossing
        e1 = bh; e2 = np.cross(ak, bh)
        prof = []
        for f in tau_fracs:
            tau = f * Th
            s_ = []
            for tt in (tg - tau, tg + tau):
                xa, pa, Ja, fa = T1.state(tt); xb, pb, Jb, fb = T2.state(tt)
                Pi = 0.5 * (pa - pb); Js = 0.5 * (Ja - Jb)
                Ll = 0.5 * ((pa - p10 - Ja) - (pb - p20 - Jb))
                s_.append((Pi[1:], Js[1:], Ll[1:], max(fa, fb)))
            dP = s_[1][0] - s_[0][0]; dJ = s_[1][1] - s_[0][1]; dL = s_[1][2] - s_[0][2]
            prof.append([f, dP @ e1, dP @ e2, dJ @ e1, dJ @ e2, dL @ e1, dL @ e2, dP @ eN, dP @ eP, dJ @ eN,
                         dJ @ eP, max(s_[0][3], s_[1][3])])
        row['profile'] = np.array(prof)
        crossings.append(row)
    # turning points: max separation between consecutive crossings (and production -> crossing 1)
    tcs = [0.0] + [c['t'] for c in crossings]
    tps = []
    for j in range(len(tcs) - 1):
        msk = (ts > tcs[j]) & (ts < tcs[j + 1])
        if msk.sum() < 3:
            tps.append(None); continue
        ii = np.where(msk)[0][np.argmax(sep[msk])]
        # refine the maximum with a parabola through 3 equal-time samples
        tq = ts[ii]
        h = 0.02 * (tcs[j + 1] - tcs[j])
        vals = []
        for tt in (tq - h, tq, tq + h):
            x1, _, _, _ = T1.state(tt); x2, _, _, _ = T2.state(tt)
            vals.append(np.linalg.norm(x1[1:] - x2[1:]))
        den = vals[0] - 2 * vals[1] + vals[2]
        dtp = 0.5 * h * (vals[0] - vals[2]) / den if den < 0 else 0.0
        dtp = float(np.clip(dtp, -h, h))
        tq = tq + dtp
        x1, p1, J1, _ = T1.state(tq); x2, p2, J2, _ = T2.state(tq)
        d = x1[1:] - x2[1:]
        A = (-1) ** j * d / np.linalg.norm(d)
        Pi = 0.5 * (p1 - p2)[1:]
        tps.append(dict(t=tq, l=float(np.linalg.norm(d)), A=A, Pi=Pi, J=0.5 * (J1 - J2)[1:]))
    for c in crossings:
        k = c['k']
        if k - 1 < len(tps) and tps[k - 1] is not None:
            c['l_before'] = tps[k - 1]['l']
        if k < len(tps) and tps[k - 1] is not None and tps[k] is not None:
            dA = tps[k]['A'] - tps[k - 1]['A']
            dPi = tps[k]['Pi'] - tps[k - 1]['Pi']
            dJ = tps[k]['J'] - tps[k - 1]['J']
            bh = np.array([c['bN'], c['bP']])
            c['dA_N'] = float(dA @ eN); c['dA_P'] = float(dA @ eP)
            c['dPiTP_N'] = float(dPi @ eN); c['dPiTP_P'] = float(dPi @ eP)
            c['dJTP_N'] = float(dJ @ eN); c['dJTP_P'] = float(dJ @ eP)
            c['l_after'] = tps[k]['l']
    return dict(crossings=crossings, eN=eN, eP=eP, n0=n0, tps=tps)


def table(res, keys=('k', 'parity', 'b', 'bN', 'bP', 'gamma1', 'vrel', 'l_before', 'dA_N', 'dA_P', 'dPiTP_N',
                     'dPiTP_P', 'dJTP_N', 'dJTP_P', 'aN', 'aP', 'r_lab', 'flag', 'cos_b_E', 't')):
    rows = []
    for c in res['crossings']:
        rows.append([c.get(k, np.nan) for k in keys])
    return np.array(rows, float), list(keys)


def fit_profile(c, sig, Th, lo_mult=5.0, hi_frac=3e-3, min_pts=4):
    """Log-law fit of the string impulse along b-hat at crossing c:
    y(tau) = -dJ_b(tau) v / (sigma b) = kappa ln(2 v tau / b) + kappa0   on  5 b/(2v) <= tau <= 3e-3 Th.
    (Straight-string heuristic: y = asinh(2 v tau/b) -> kappa = 1, kappa0 = ln 2.)  Returns (kappa, kappa0, npts)."""
    pr = c['profile']; v = c['v1']; b = c['b']
    if not np.isfinite(b) or b <= 0:
        return np.nan, np.nan, 0
    tau = pr[:, 0] * Th
    y = -pr[:, 3] * v / (sig * b)
    sel = (tau >= lo_mult * b / (2 * v)) & (tau <= hi_frac * Th)
    if sel.sum() < min_pts:
        return np.nan, np.nan, int(sel.sum())
    x = np.log(2 * v * tau[sel] / b)
    A = np.vstack([x, np.ones_like(x)]).T
    k, k0 = np.linalg.lstsq(A, y[sel], rcond=None)[0]
    return float(k), float(k0), int(sel.sum())
