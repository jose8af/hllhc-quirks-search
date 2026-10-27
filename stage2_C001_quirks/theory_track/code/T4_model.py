"""T4_model.py -- fit-ready quirk-pair trajectory model (theory track, investigator T4).

Purpose
-------
A parametrised model of the hit positions, hit times and per-hit velocities of a quirk pair in the CMS Phase-2
barrel tracker, built for (i) least-squares / Fisher-information studies and (ii) validation against the exact
causal Nambu-Goto string.  The dynamics is the causal null-vector string of the ATLAS Athena Quirks package, as
ported by T2 (`T2_propagator.CausalNullString`) and T3 (`T3_causal.causal_propagate`); the kernel below is a
line-by-line copy of that algorithm (first string vector, borrowing, max-boost splitting, B kick + mass-shell
renormalisation) with two changes made for fitting:
  * material is THIN SCATTERERS at the T3 slab radii (beam pipe, 4 IT, IT service cylinder, 3 PS, 3 2S; x/X0 from
    T3 report Sec.2, all UNVERIFIED reconstructions of the Phase-2 TDR).  At each crossing of a slab radius the
    quirk receives a multiple-scattering deflection theta = theta0 * xi (Highland, PDG RPP Eq.34.16 as used by T3),
    with xi a DETERMINISTIC 2-vector supplied per (quirk, material-crossing index) -> the MS angles become explicit
    nuisance parameters (General-Broken-Lines style), so their Jacobian can be taken by finite differences; and an
    optional mean Bethe energy loss (same Bethe/I values as T3/T6, silicon equivalent).
  * hits are recorded at sensor radii (IT 4, OT 6, plus optional pseudo-sensors for stub studies and the BTL at
    r = 114.8 cm) with position, time, momentum vector and per-(quirk, layer) crossing count.

Parameters (physical set used for the fit, 9 + 1 nuisance):
    theta = [z0, ln pT, phi, eta, ln(gamma*-1), cos(theta*), phi*, ln m_Q, ln Lambda]   (+ mat_scale)
    z0: vertex z [cm]; (pT, phi, eta): pair 3-momentum; gamma*: per-quirk CM Lorentz factor (M = 2 gamma* m);
    (cos theta*, phi*): CM axis of quirk 1 relative to the pair velocity, phi* measured from e1 = unit(z x b_hat);
    m_Q [GeV]; Lambda [keV] (sigma = Lambda^2).

Units: cm, GeV, c = 1 (times in cm; /29.979 for ns).  B in tesla, uniform along z.
How to run: library; `pixi run python code/T4_model.py` runs self-checks (vacuum vs T2 ExactPair; B=3.8 T vs
T3 causal kernel without material).
"""
from __future__ import annotations

import os
import sys
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T, C_CM_PER_NS  # noqa: E402

B_CMS = 3.8112
# Thin-scatterer table (T3 report Sec.2; T3_propagator.phase2_tracker): R [cm], x/X0, |z| half-length [cm]
SLABS = np.array([
    [2.2, 0.0023, 300.0],
    [3.0, 0.012, 20.0], [6.1, 0.012, 20.0], [10.4, 0.012, 20.0], [14.6, 0.012, 20.0],
    [19.0, 0.010, 120.0],
    [24.9, 0.025, 120.0], [37.2, 0.025, 120.0], [52.3, 0.025, 120.0],
    [68.8, 0.018, 120.0], [86.0, 0.018, 120.0], [108.3, 0.018, 120.0],
])
# sensors: R, zmax ; index 0-3 IT, 4-6 PS, 7-9 2S, 10 BTL
SENS_R = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3, 114.8])
SENS_Z = np.array([20.0] * 4 + [120.0] * 6 + [230.0])
SENS_NAMES = ['IT1', 'IT2', 'IT3', 'IT4', 'PS1', 'PS2', 'PS3', '2S1', '2S2', '2S3', 'BTL']
# single-hit resolutions [cm] (rphi, z): IT 25x100 um pixels, PS 100 um x 1.5 mm, 2S 90 um x 5 cm, binary /sqrt(12)
# [theory_signal_model Sec.4.1-4.2; 2210.07766 Sec.2 for OT; IT pitch UNVERIFIED]
SIG_RPHI = np.array([25e-4 / np.sqrt(12)] * 4 + [100e-4 / np.sqrt(12)] * 3 + [90e-4 / np.sqrt(12)] * 3 + [np.inf])
SIG_Z = np.array([100e-4 / np.sqrt(12)] * 4 + [0.15 / np.sqrt(12)] * 3 + [5.0 / np.sqrt(12)] * 3 + [np.inf])

ME = 0.51099895e-3
K_BETHE = 0.307075e-3       # GeV cm^2/mol
ZA_SI, I_SI, X0_SI_G = 0.49848, 173e-9, 21.82   # Z/A, I [GeV], X0 [g/cm^2]


@njit(cache=True, inline='always')
def _md(a0, a1, a2, a3, b0, b1, b2, b3):
    return a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3


@njit(cache=True)
def bethe(beta):
    """Mean dE/dx [GeV per g/cm^2] in silicon, |q| = 1 (no density effect; L >= 0.6; linear below beta = 0.02),
    the same prescription as T3_propagator.stopping_power / T6_stopping."""
    bp = 0.02
    b = beta if beta > bp else bp
    g2 = 1.0 / (1.0 - b * b)
    L = np.log(2 * ME * b * b * g2 / I_SI) - b * b
    if L < 0.6:
        L = 0.6
    s = K_BETHE * ZA_SI * L / (b * b)
    if beta < bp:
        s *= beta / bp
    return s


@njit(cache=True)
def kernel(p1, p2, vtx, m, F, q1, q2, B0, slabs, sens_r, sens_z, xi, do_ms, do_eloss, mat_scale,
           t_end, r_exit, max_boost, hmax, first_length, max_hits, max_steps, qcap):
    """Causal null-vector string (Athena algorithm) + uniform B along z + thin scatterers.
    xi: (2, NC, 2) deterministic MS deviates per (quirk, material crossing).  Returns
    (status, hits[n, 11] = [k, L, t, x, y, z, px, py, pz, ncross, beta], ncross_mat[2], nsteps)."""
    maxexpy = np.sqrt((1 + max_boost) / (1 - max_boost))
    P = np.zeros((2, 4)); X = np.zeros((2, 4))
    for c in range(3):
        P[0, c + 1] = p1[c]; P[1, c + 1] = p2[c]
        X[0, c + 1] = vtx[c]; X[1, c + 1] = vtx[c]
    P[0, 0] = np.sqrt(m * m + p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    P[1, 0] = np.sqrt(m * m + p2[0] ** 2 + p2[1] ** 2 + p2[2] ** 2)
    qs = np.array([q1, q2])
    Q = np.zeros((2, qcap, 4))
    head = np.zeros(2, np.int64); cnt = np.zeros(2, np.int64)
    borrowed = np.zeros((2, 4))
    first_step = np.array([False, True])
    u0 = P[0] / m; u1 = P[1] / m
    dot = _md(u1[0], u1[1], u1[2], u1[3], u0[0], u0[1], u0[2], u0[3])
    s0 = u0 - u1 * (dot - np.sqrt(dot * dot - 1))
    s0 = s0 * (first_length / s0[0])
    s0[0] = np.sqrt(s0[1] ** 2 + s0[2] ** 2 + s0[3] ** 2)
    Q[1, 0] = s0; cnt[1] = 1
    hits = np.zeros((max_hits, 11)); nh = 0
    ncnt = np.zeros((2, sens_r.shape[0]))
    nmat = np.zeros(2, np.int64)
    NC = xi.shape[1]
    nsteps = 0; status = 0
    k = 1
    s = np.zeros(4); a = np.zeros(4); sout = np.zeros(4); dx = np.zeros(4); pn = np.zeros(4)
    while True:
        if nsteps >= max_steps:
            status = 3
            break
        if X[0, 0] > t_end and X[1, 0] > t_end:
            break
        if cnt[k] == 0:
            k = 1 - k
            if cnt[k] == 0:
                status = 4
                break
            continue
        while cnt[k] > 0 and nsteps < max_steps and X[k, 0] <= t_end:
            hidx = head[k] % qcap
            sin = Q[k, hidx]
            p = P[k]
            tmp = 2 * F * _md(sin[0], sin[1], sin[2], sin[3], p[0], p[1], p[2], p[3]) / (m * m)
            frac = 1.0
            if tmp > maxexpy - 1:
                frac = (maxexpy - 1) / tmp
            if sin[0] * frac > hmax:
                frac = hmax / sin[0]
            for c in range(4):
                s[c] = sin[c] * frac
                a[c] = p[c] + F * s[c]
            sa = _md(s[0], s[1], s[2], s[3], a[0], a[1], a[2], a[3])
            aa = _md(a[0], a[1], a[2], a[3], a[0], a[1], a[2], a[3])
            for c in range(4):
                sout[c] = 2 * sa / aa * a[c] - s[c]
                dx[c] = s[c] + sout[c]
                pn[c] = p[c] + F * (s[c] - sout[c])
            qk = qs[k]
            if qk != 0.0 and B0 != 0.0:
                cc = qk * EB_GEV_PER_CM_PER_T * B0
                pn[1] += cc * dx[2]
                pn[2] += -cc * dx[1]
            nrm = m / np.sqrt(_md(pn[0], pn[1], pn[2], pn[3], pn[0], pn[1], pn[2], pn[3]))
            for c in range(4):
                pn[c] *= nrm
            ra = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            xb = X[k, 1] + dx[1]; yb = X[k, 2] + dx[2]
            rb = np.sqrt(xb * xb + yb * yb)
            A2 = dx[1] ** 2 + dx[2] ** 2
            B2 = 2 * (X[k, 1] * dx[1] + X[k, 2] * dx[2])
            # sensor hits (on the chord)
            for L in range(sens_r.shape[0]):
                R = sens_r[L]
                if (ra - R) * (rb - R) < 0.0:
                    C2 = ra * ra - R * R
                    disc = max(B2 * B2 - 4 * A2 * C2, 0.0)
                    f1 = (-B2 + np.sqrt(disc)) / (2 * A2); f2 = (-B2 - np.sqrt(disc)) / (2 * A2)
                    f = f1 if (f1 >= 0 and f1 <= 1) else f2
                    zc = X[k, 3] + f * dx[3]
                    if abs(zc) < sens_z[L] and nh < max_hits:
                        ncnt[k, L] += 1
                        hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2] = X[k, 0] + f * dx[0]
                        hits[nh, 3] = X[k, 1] + f * dx[1]; hits[nh, 4] = X[k, 2] + f * dx[2]; hits[nh, 5] = zc
                        hits[nh, 6] = pn[1]; hits[nh, 7] = pn[2]; hits[nh, 8] = pn[3]
                        hits[nh, 9] = ncnt[k, L]
                        hits[nh, 10] = np.sqrt(pn[1] ** 2 + pn[2] ** 2 + pn[3] ** 2) / pn[0]
                        nh += 1
            # thin scatterers at slab radii (applied after the step that crosses them)
            if do_ms or do_eloss:
                for S in range(slabs.shape[0]):
                    R = slabs[S, 0]
                    if (ra - R) * (rb - R) < 0.0:
                        C2 = ra * ra - R * R
                        disc = max(B2 * B2 - 4 * A2 * C2, 0.0)
                        f1 = (-B2 + np.sqrt(disc)) / (2 * A2); f2 = (-B2 - np.sqrt(disc)) / (2 * A2)
                        f = f1 if (f1 >= 0 and f1 <= 1) else f2
                        zc = X[k, 3] + f * dx[3]
                        if abs(zc) < slabs[S, 2]:
                            xc = X[k, 1] + f * dx[1]; yc = X[k, 2] + f * dx[2]
                            px = pn[1]; py = pn[2]; pz = pn[3]
                            pp = np.sqrt(px * px + py * py + pz * pz)
                            cosa = abs(px * xc + py * yc) / (pp * R)
                            if cosa < 0.1:
                                cosa = 0.1
                            xx0 = slabs[S, 1] * mat_scale / cosa
                            E = np.sqrt(m * m + pp * pp)
                            beta = pp / E
                            if do_eloss:
                                dE = bethe(beta) * qk * qk * xx0 * X0_SI_G
                                Ek = E - m - dE
                                if Ek < 1e-9 * m:
                                    Ek = 1e-9 * m
                                pnew = np.sqrt((Ek + m) ** 2 - m * m)
                                fct = pnew / pp
                                px *= fct; py *= fct; pz *= fct; pp = pnew
                                E = Ek + m; beta = pp / E
                            ic = nmat[k]
                            if do_ms and ic < NC:
                                xr = xx0 * qk * qk / (beta * beta)
                                if xr < 1e-4:
                                    xr = 1e-4
                                flog = 1.0 + 0.038 * np.log(xr)
                                if flog < 0.5:
                                    flog = 0.5
                                th0 = 13.6e-3 / (beta * pp) * abs(qk) * np.sqrt(xx0) * flog
                                t1 = th0 * xi[k, ic, 0]; t2 = th0 * xi[k, ic, 1]
                                ux = px / pp; uy = py / pp; uz = pz / pp
                                # e1 = unit(z x u) (horizontal), e2 = u x e1
                                e1x = -uy; e1y = ux; e1z = 0.0
                                n1 = np.sqrt(e1x * e1x + e1y * e1y)
                                if n1 < 1e-12:
                                    e1x = 1.0; e1y = 0.0; n1 = 1.0
                                e1x /= n1; e1y /= n1
                                e2x = uy * e1z - uz * e1y; e2y = uz * e1x - ux * e1z; e2z = ux * e1y - uy * e1x
                                th = np.sqrt(t1 * t1 + t2 * t2)
                                if th > 0:
                                    cth = np.cos(th); sth = np.sin(th) / th
                                    px = pp * (cth * ux + sth * (t1 * e1x + t2 * e2x))
                                    py = pp * (cth * uy + sth * (t1 * e1y + t2 * e2y))
                                    pz = pp * (cth * uz + sth * (t1 * e1z + t2 * e2z))
                            nmat[k] += 1
                            pn[1] = px; pn[2] = py; pn[3] = pz
                            pn[0] = np.sqrt(m * m + px * px + py * py + pz * pz)
            for c in range(4):
                X[k, c] += dx[c]
                P[k, c] = pn[c]
            if frac >= 1.0:
                head[k] += 1; cnt[k] -= 1
            else:
                for c in range(4):
                    Q[k, hidx, c] = sin[c] * (1 - frac)
            if first_step[k]:
                for c in range(4):
                    borrowed[1 - k, c] += s[c]
                if frac >= 1.0:
                    first_step[k] = False
            j = 1 - k
            v0 = sout[0]; scale = 1.0
            if borrowed[j, 0] > 0:
                if borrowed[j, 0] <= v0:
                    scale = 1 - borrowed[j, 0] / v0
                    for c in range(4):
                        borrowed[j, c] = 0.0
                else:
                    f_ = 1 - v0 / borrowed[j, 0]
                    for c in range(4):
                        borrowed[j, c] *= f_
                    scale = 0.0
            if scale * v0 > 0:
                if cnt[j] >= qcap:
                    status = 5
                    return status, hits[:nh].copy(), nmat, nsteps
                tidx = (head[j] + cnt[j]) % qcap
                for c in range(4):
                    Q[j, tidx, c] = sout[c] * scale
                cnt[j] += 1
            nsteps += 1
        k = 1 - k
        r1 = np.sqrt(X[0, 1] ** 2 + X[0, 2] ** 2); r2 = np.sqrt(X[1, 1] ** 2 + X[1, 2] ** 2)
        if (r1 > r_exit or abs(X[0, 3]) > 300.0) and (r2 > r_exit or abs(X[1, 3]) > 300.0):
            status = 1
            break
    return status, hits[:nh].copy(), nmat, nsteps


# ------------------------------------------------------------------------------------------------
# parameters <-> momenta
# ------------------------------------------------------------------------------------------------
PNAMES = ['z0', 'lnpT', 'phi', 'eta', 'ln(g*-1)', 'cos*', 'phi*', 'ln m', 'ln L']


def momenta(theta):
    """theta = [z0, ln pT, phi, eta, ln(g*-1), cos*, phi*, ln m, ln Lambda] -> (p1, p2, vtx, m, lam_keV)."""
    z0, lpt, phi, eta, lg, cs, phs, lm, ll = theta[:9]
    m = np.exp(lm); gs = 1.0 + np.exp(lg); lam = np.exp(ll)
    pt = np.exp(lpt)
    M = 2 * gs * m
    P = np.array([pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta)])
    E = np.hypot(M, np.linalg.norm(P))
    b = P / E; bh = b / np.linalg.norm(b)
    e1 = np.cross([0, 0, 1.0], bh); e1 /= np.linalg.norm(e1); e2 = np.cross(bh, e1)
    st = np.sqrt(max(0.0, 1 - cs * cs))
    n = cs * bh + st * (np.cos(phs) * e1 + np.sin(phs) * e2)
    ps = m * np.sqrt(gs ** 2 - 1); es = np.hypot(m, ps)
    g = E / M; b2 = b @ b
    pv = []
    for sgn in (1, -1):
        q = sgn * ps * n
        bp = b @ q
        pv.append(q + ((g - 1) * bp / b2 + g * es) * b)
    return pv[0], pv[1], np.array([0.0, 0.0, z0]), m, lam


# Natural parameters: velocities + oscillation scale + string tension.  In vacuum the hit positions depend on
# (m, sigma) only through l0 = m/sigma (scale invariance of the Nambu-Goto + point-mass action), so the derivative
# w.r.t. ln sigma at fixed (velocities, l0) vanishes identically in vacuum: it isolates the B-field (eps_B = qB/sigma)
# and material (1/m) effects without numerical cancellation.
UNAMES = ['z0', 'ln uT', 'phi', 'eta', 'ln(g*-1)', 'cos*', 'phi*', 'ln l0', 'ln sigma']


def theta_to_nat(theta):
    z0, lpt, phi, eta, lg, cs, phs, lm, ll = theta[:9]
    gs = 1 + np.exp(lg)
    sig = sigma_from_lambda_keV(np.exp(ll))
    luT = lpt - np.log(2 * gs) - lm
    u = np.array([z0, luT, phi, eta, lg, cs, phs, lm - np.log(sig), np.log(sig)])
    return np.r_[u, theta[9:]]


def nat_to_theta(u):
    z0, luT, phi, eta, lg, cs, phs, ll0, lsig = u[:9]
    gs = 1 + np.exp(lg)
    lm = ll0 + lsig
    lam = np.sqrt(np.exp(lsig) / sigma_from_lambda_keV(1.0))
    lpt = luT + np.log(2 * gs) + lm
    return np.r_[np.array([z0, lpt, phi, eta, lg, cs, phs, lm, np.log(lam)]), u[9:]]


def dtheta_dnat(u):
    """Jacobian d theta / d u (rows theta, cols u) for the 9 (+1) parameters."""
    n = len(u)
    D = np.eye(n)
    gs = 1 + np.exp(u[4])
    D[1, :] = 0; D[1, 1] = 1; D[1, 4] = (gs - 1) / gs; D[1, 7] = 1; D[1, 8] = 1      # ln pT
    D[7, :] = 0; D[7, 7] = 1; D[7, 8] = 1                                             # ln m
    D[8, :] = 0; D[8, 8] = 0.5                                                        # ln Lambda
    return D


def run(theta, B0=B_CMS, xi=None, do_ms=False, do_eloss=False, mat_scale=1.0, max_boost=1e-2, hmax=0.01,
        sens_r=SENS_R, sens_z=SENS_Z, r_exit=116.0, charges=(1.0, -1.0), first_length=1e-9, nc=64):
    p1, p2, vtx, m, lam = momenta(theta)
    if len(theta) > 9:
        mat_scale = mat_scale * theta[9]
    F = sigma_from_lambda_keV(lam)
    if xi is None:
        xi = np.zeros((2, nc, 2))
    P = p1 + p2
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    bT = np.hypot(P[0], P[1]) / E
    t_end = 1.2 * r_exit / max(bT, 0.02) + 50.0
    st, hits, nmat, nsteps = kernel(p1, p2, vtx, float(m), float(F), float(charges[0]), float(charges[1]), float(B0),
                                    SLABS, np.asarray(sens_r, float), np.asarray(sens_z, float), xi, bool(do_ms),
                                    bool(do_eloss), float(mat_scale), float(t_end), float(r_exit), float(max_boost),
                                    float(hmax), float(first_length), 400000, 400_000_000, 1 << 16)
    return dict(status=st, hits=hits, nmat=nmat, nsteps=nsteps)


def hit_dict(hits):
    """{(k, L, n): row} for matching hits between runs."""
    return {(int(h[0]), int(h[1]), int(h[9])): h for h in hits}


# ------------------------------------------------------------------------------------------------
# event sampling (T2 cache, as T3_propagator.sample_events but returning theta)
# ------------------------------------------------------------------------------------------------
def sample_theta(m, n, rng, eta_max=1.0, spin='F'):
    from T3_propagator import load_cache
    c = load_cache(); key = f'{spin}_{int(m)}_isr'
    w = c[key + '_w']; gs = c[key + '_gamma_star']; cs = c[key + '_cstar']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
    M = 2 * m * gs; pt = M * bg / np.cosh(eta)
    sel = np.where(np.abs(eta) < eta_max)[0]
    p = w[sel] / w[sel].sum()
    idx = rng.choice(sel, size=n, p=p)
    out = []
    for k in idx:
        out.append(np.array([0.0, np.log(pt[k]), rng.uniform(0, 2 * np.pi), eta[k], np.log(gs[k] - 1), cs[k],
                             rng.uniform(0, 2 * np.pi), np.log(m), 0.0]))
    return out


if __name__ == '__main__':
    import time
    from T2_propagator import ExactPair
    rng = np.random.default_rng(3)
    th = sample_theta(500.0, 1, rng)[0]
    ok = True
    for lam in (1.0, 3.0):
        th[8] = np.log(lam)
        p1, p2, vtx, m, _ = momenta(th)
        t0 = time.time(); r = run(th, B0=0.0); dt = time.time() - t0
        ex = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam))
        err = 0.0
        for h in r['hits']:
            X1, X2 = ex.lab_positions([h[2]])
            err = max(err, np.linalg.norm((X1, X2)[int(h[0])][0] - h[3:6]))
        good = err < 1e-5
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] vacuum vs ExactPair, Lambda={lam}: max|dx| = {err*1e4:.3f} um over "
              f"{len(r['hits'])} hits ({dt:.2f} s, {r['nsteps']} steps)")
    # B field: compare with T3 causal kernel (no material) on the same event
    from T3_causal import run_causal
    for lam in (1.0, 3.0):
        th[8] = np.log(lam)
        p1, p2, vtx, m, _ = momenta(th)
        r = run(th, hmax=0.2)
        r3 = run_causal(p1, p2, m, lam, B0=B_CMS, material=False, hmax_trk=0.2, r_exit=116.0)
        H3 = {(int(h[0]), int(h[1]), int(h[8])): h for h in r3['hits'] if h[1] < 10}
        H4 = hit_dict(r['hits'])
        d = [np.linalg.norm(H4[key][3:6] - H3[key][3:6]) for key in H4 if key in H3]
        good = max(d) < 1e-4
        ok &= good
        print(f"[{'PASS' if good else 'FAIL'}] B=3.81 T vs T3_causal (no material), Lambda={lam}: max|dx| = "
              f"{max(d)*1e4:.3g} um over {len(d)} matched hits")
    print('ALL PASS' if ok else 'SOME FAILURES')
