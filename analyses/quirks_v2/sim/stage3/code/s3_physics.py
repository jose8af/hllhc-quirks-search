"""s3_physics.py -- Stage-3 per-event analytic truth, plane fits and sensor energy deposits (numpy only; bundled).

pair_truth(): closed forms per event, COPIED from analytic/checks/c06_rotating_yoyo.pair_params (K(gamma*) table of c03,
  G_of) and c13_population.angles (k_B); not re-derived here.  Sources: NEAR_MISS_IMPULSE.md §3-5, predictions.json 'c'.
    l0 = m/sigma, rho = sqrt(gamma*^2 - 1), b_odd = 2 eps_perp l0 (gamma* - asinh(rho)/rho), l_max = 2 (gamma* - 1) l0,
    L = ln(l_max/b_odd), c_ev = 1/(L + K(gamma*)), C_ev = 1/c_ev - ln(1/eps_B) with eps_B = q B c_EB / sigma (lab),
    k_B = |B*_perp n| / |E*_perp n| (CM frame), N_osc_vac = sigma R_eff / (2 beta* p_T), R_eff = min(108.3, 265/|sinh eta|) cm
    (plan §1.1, ESTIMATE closed form), floor_flag = b_odd/l0 < 1e-7 (plan §1.1).
plane_fit(): best plane through a point (the vertex): thickness = sqrt(min eigenvalue of sum h h^T/(N-1))
  [1708.02243 Eq.11; 2002.07503 Eq.C.1], as code/T3_propagator.plane_fit.
dE_sensor(): Bethe mean loss (stopping power copied in T3_causal_s3) in the active Si thickness of the surface along the
  momentum direction, path capped at 20 x thickness (grazing crossings; a real module is finite).
"""
import numpy as np

from T3_causal_s3 import (sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T, MAT, ME, KBB)

B_CMS = 3.8112
K_TAB_G = np.array([1.0, 1.05, 1.28, 1.6, 2.0, 3.0])
K_TAB_K = np.array([3 * np.log(2) - 2, 0.056, -0.05, -0.18, -0.31, -0.58])


def K_of(g):
    return np.interp(g, K_TAB_G, K_TAB_K)


def pair_truth(p1, p2, m, lam, B=B_CMS, q1=1.0):
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    sig = sigma_from_lambda_keV(lam)
    E1 = np.hypot(m, np.linalg.norm(p1)); E2 = np.hypot(m, np.linalg.norm(p2))
    P = p1 + p2; E = E1 + E2; beta = P / E; b2 = beta @ beta; g = 1 / np.sqrt(1 - b2); bh = beta / np.sqrt(b2)
    p1s = p1 + ((g - 1) * (p1 @ bh) - g * np.sqrt(b2) * E1) * bh
    ps = np.linalg.norm(p1s); n = p1s / ps
    gs = np.hypot(m, ps) / m
    rho = np.sqrt(gs * gs - 1)
    l0 = m / sig
    lmax = 2 * (gs - 1) * l0
    pt = np.hypot(P[0], P[1]); eta = np.arcsinh(P[2] / pt) if pt > 0 else np.sign(P[2]) * 20.0
    Reff = min(108.3, 265.0 / max(abs(np.sinh(eta)), 1e-12))
    bstar = rho / gs
    out = dict(gstar=gs, x=2 * (gs - 1), ell_max=lmax, l0=l0, N_osc_vac=sig * Reff / (2 * bstar * pt))
    if B == 0.0:
        out.update(eps_B=0.0, eps_perp=0.0, bodd_l0=0.0, k_B=np.nan, c_ev=np.nan, C_ev=np.nan, floor_flag=False)
        return out
    Bv = np.array([0, 0, B])
    qEs = q1 * EB_GEV_PER_CM_PER_T * g * np.cross(beta, Bv)
    Ep = qEs - (qEs @ n) * n
    eps_perp = np.linalg.norm(Ep) / sig
    bodd = 2 * eps_perp * l0 * (gs - np.arcsinh(rho) / rho)
    L = np.log(lmax / bodd)
    c_ev = 1.0 / (L + K_of(gs))
    eps_B = abs(q1) * EB_GEV_PER_CM_PER_T * B / sig
    Es = g * np.cross(beta, Bv); Bs = g * Bv - (g - 1) * (Bv @ bh) * bh
    Ep2 = Es - (Es @ n) * n; Bp = Bs - (Bs @ n) * n
    kB = np.linalg.norm(Bp) / np.linalg.norm(Ep2)
    out.update(eps_B=eps_B, eps_perp=eps_perp, bodd_l0=bodd / l0, k_B=kB, c_ev=c_ev, C_ev=1.0 / c_ev - np.log(1.0 / eps_B),
               floor_flag=bool(bodd / l0 < 1e-7))
    return out


def plane_fit(points, origin=None):
    h = np.asarray(points, float)
    if origin is not None:
        h = h - np.asarray(origin, float)
    if len(h) < 4:
        return np.nan, np.full(3, np.nan), np.nan
    T = h.T @ h / (len(h) - 1)
    w, v = np.linalg.eigh(T)
    nrm = v[:, 0]
    return float(np.sqrt(max(w[0], 0.0))), nrm, float(np.max(np.abs(h @ nrm)))


def stopping_power_np(beta, q2, za_rho, I):
    bp = 0.02
    b = np.maximum(beta, bp)
    g2 = 1.0 / (1.0 - b * b)
    L = np.maximum(np.log(2.0 * ME * b * b * g2 / I), 0.6)
    s = KBB * za_rho * q2 / (b * b) * (L - b * b)
    return np.where(beta < bp, s * beta / bp, s)


def dE_sensor(hits, surf, t_sens, m):
    """hits (n, 12) kernel columns (cm, GeV); returns the mean loss [GeV] in the active sensor thickness."""
    if len(hits) == 0:
        return np.zeros(0)
    L = hits[:, 1].astype(int)
    px, py, pz, E = hits[:, 7], hits[:, 8], hits[:, 9], hits[:, 10]
    p = np.sqrt(px * px + py * py + pz * pz)
    cyl = surf[L, 0] < 0.5
    r = np.hypot(hits[:, 4], hits[:, 5])
    cosn = np.where(cyl, np.abs(px * hits[:, 4] + py * hits[:, 5]) / np.maximum(p * r, 1e-300), np.abs(pz) / np.maximum(p, 1e-300))
    t = t_sens[L]
    path = np.where(t > 0, np.minimum(t / np.maximum(cosn, 1e-300), 20 * t), 0.0)
    za_rho = MAT[1, 0] * MAT[1, 3]
    return stopping_power_np(p / E, 1.0, za_rho, MAT[1, 1]) * path
