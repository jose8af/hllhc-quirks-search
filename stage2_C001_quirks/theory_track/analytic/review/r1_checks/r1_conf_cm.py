"""r1_conf_cm.py -- S1-R1 critical reviewer: relativistic spot check of b_odd, eta (hence K) and the B* effect with the
conformal-gauge NG formulation of code/R1_conformal_ng.py (delay ODE, RK4), extended here (own code, not E2's
nm_conformal.py and not the causal kernel used by E1 c03/c12) to a uniform E and a uniform B vector in the pair rest frame.

Endpoint EOM (conformal gauge, metric +---):  m du/dtau = T (w - (u.w) u) + q (u.w) (E.u_vec, E u0 + u_vec x B)
with E, B given as force per unit charge [GeV/cm].  Pair at rest: p1 = +p* x_hat, p2 = -p* x_hat; E = eps*sigma*y_hat;
optional B = kB*eps*sigma*(direction).
Measured: b_1 = closest approach of the equal-time relative coordinate at the first (odd) crossing (component perp to x);
eta = mean over periods of the apocentre-to-apocentre in-plane angle change (as E1 c03/c12 define it).
Compared with E1: b_odd/(eps l0) = 2[g - asinh rho/rho];  K = eta/(eps G) - ln(l_max/b_odd) (E1 table: K(1.3) ~ -0.059).
Run: pixi run python analytic/review/r1_checks/r1_conf_cm.py > analytic/review/r1_checks/r1_conf_cm_out.txt
"""
import os, sys, time
import numpy as np
from numba import njit
from scipy.interpolate import CubicHermiteSpline

TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(TT, 'code'))
from R1_conformal_ng import sigma_keV  # noqa: E402  (unit conversion only)


@njit(cache=True)
def _mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


@njit(cache=True)
def _rhs(u, w, T, m, q, Ef, Bf):
    uw = _mdot(u, w)
    du = (T / m) * (w - uw * u)
    f0 = Ef[0] * u[1] + Ef[1] * u[2] + Ef[2] * u[3]
    fx = Ef[0] * u[0] + (u[2] * Bf[2] - u[3] * Bf[1])
    fy = Ef[1] * u[0] + (u[3] * Bf[0] - u[1] * Bf[2])
    fz = Ef[2] * u[0] + (u[1] * Bf[1] - u[2] * Bf[0])
    du[0] += q * uw * f0 / m
    du[1] += q * uw * fx / m
    du[2] += q * uw * fy / m
    du[3] += q * uw * fz / m
    return du, uw * u


@njit(cache=True)
def solve(p1, p2, m, T, Ef, Bf, N, t_end, Dvec, max_steps, guard):
    h = np.pi / N
    RB = N + 8
    o = np.zeros((2, RB, 4))
    u = np.zeros((2, 4)); X = np.zeros((2, 4))
    for k in range(2):
        p = p1 if k == 0 else p2
        E = np.sqrt(m * m + p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
        u[k, 0] = E / m; u[k, 1:] = p / m
    delta = np.sqrt(Dvec @ Dvec)
    n = Dvec / delta                       # initial static straight string from end 1 to end 2 (vector Dvec)
    X[0, 1:] = -0.5 * Dvec; X[1, 1:] = 0.5 * Dvec
    c = delta / np.pi
    a0 = N + 4
    for a in range(a0 + 1):
        o[1, a % RB, 0] = c; o[1, a % RB, 1:] = c * n
        o[0, a % RB, 0] = c; o[0, a % RB, 1:] = -c * n
    qs = np.array([1.0, -1.0])
    rec = np.zeros((max_steps + 1, 2, 8))
    for k in range(2):
        rec[0, k, :4] = X[k]; rec[0, k, 4:] = u[k]
    a = a0
    step = 0
    w0 = np.zeros((2, 4)); wh = np.zeros((2, 4)); w1 = np.zeros((2, 4))
    ku = np.zeros((4, 2, 4)); kX = np.zeros((4, 2, 4))
    status = 1
    while step < max_steps:
        for k in range(2):
            j = 1 - k
            w0[k] = o[j, (a - N) % RB]
            w1[k] = o[j, (a - N + 1) % RB]
            wh[k] = (-o[j, (a - N - 1) % RB] + 9 * o[j, (a - N) % RB] + 9 * o[j, (a - N + 1) % RB]
                     - o[j, (a - N + 2) % RB]) / 16.0
        for k in range(2):
            uw = _mdot(u[k], w0[k])
            o[k, a % RB] = 2 * uw * u[k] - w0[k]
        uk = u.copy(); Xk = X.copy()
        for s in range(4):
            if s == 0:
                us = uk; ws = w0
            elif s == 1:
                us = uk + 0.5 * h * ku[0]; ws = wh
            elif s == 2:
                us = uk + 0.5 * h * ku[1]; ws = wh
            else:
                us = uk + h * ku[2]; ws = w1
            for k in range(2):
                du, dX = _rhs(us[k], ws[k], T, m, qs[k], Ef, Bf)
                ku[s, k] = du; kX[s, k] = dX
        u = uk + h / 6.0 * (ku[0] + 2 * ku[1] + 2 * ku[2] + ku[3])
        X = Xk + h / 6.0 * (kX[0] + 2 * kX[1] + 2 * kX[2] + kX[3])
        for k in range(2):
            u[k, 0] = np.sqrt(1.0 + u[k, 1] ** 2 + u[k, 2] ** 2 + u[k, 3] ** 2)
            if guard and X[k, 0] < Xk[k, 0] - 1e-12 * (1.0 + abs(Xk[k, 0])):
                status = 7          # lab time decreasing (conformal gauge degenerate); zero increments at a fold allowed
        a += 1
        step += 1
        for k in range(2):
            rec[step, k, :4] = X[k]; rec[step, k, 4:] = u[k]
        if status != 1:
            break
        if X[0, 0] > t_end and X[1, 0] > t_end:
            break
    return rec[:step + 1], status


def run_cm(g, eps, N=1024, kB=0.0, Bdir=(0, 0, 1), nper=3, m=500.0, lam=1.0, delta=1e-9, guard=False, b0=0.0):
    sig = sigma_keV(lam); rho = np.sqrt(g * g - 1); ps = m * rho; Tper = 4 * ps / sig
    Ef = np.array([0.0, eps * sig, 0.0])
    Bf = kB * eps * sig * np.asarray(Bdir, float)
    p1 = np.array([ps, 0.0, 0.0]); p2 = -p1
    t_end = (nper + 0.1) * Tper
    max_steps = int(40 * N * nper * max(1.0, 1.0 / (g - 1)))
    Dvec = np.array([-delta, b0 * (m / sig), 0.0])   # end 1 at +x side moving +x; transverse offset b0*l0 along y
    rec, st = solve(p1, p2, m, sig, Ef, Bf, int(N), float(t_end), Dvec, max_steps, guard)
    if rec[-1, 0, 0] < t_end or rec[-1, 1, 0] < t_end:
        st = 8   # did not reach t_end
    return rec, st, Tper, sig, ps


def eq_time(rec, k, t):
    X = rec[:, k, :4]; U = rec[:, k, 4:]
    tt = X[:, 0]
    keep = np.concatenate([[True], tt[1:] > np.maximum.accumulate(tt)[:-1]])   # strictly monotone samples only
    tt = tt[keep]; X = X[keep]; U = U[keep]
    v = U[:, 1:] / U[:, 0:1]
    return CubicHermiteSpline(tt, X[:, 1:], v, axis=0)(t)


def analyse(g, eps, rec, Tper, sig, m=500.0, nper=3):
    l0 = m / sig
    th = Tper / 2
    # relative coordinate at equal times
    t = np.linspace(0.002 * Tper, (nper + 0.05) * Tper, 300001)
    r = eq_time(rec, 0, t) - eq_time(rec, 1, t)
    rr = np.linalg.norm(r, axis=1)
    ph = []
    for hh in range(2 * nper):
        sel = (t >= hh * th) & (t < (hh + 1) * th)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        ph.append(np.arctan2(r[i, 1], r[i, 0]))
    ph = (np.array(ph) + np.pi / 2) % np.pi - np.pi / 2
    ph = np.unwrap(2 * ph) / 2
    eta = np.mean(ph[2:] - ph[:-2])
    # closest approach near the first crossing
    tf = np.linspace(th * 0.995, th * 1.005, 200001)
    rf = eq_time(rec, 0, tf) - eq_time(rec, 1, tf)
    i = np.argmin(np.linalg.norm(rf, axis=1))
    b1 = np.hypot(rf[i, 1], rf[i, 2])
    return b1 / (eps * l0), eta, ph


def pm_run(g, eps, N, fb, **kw):
    """average over initial transverse offsets b0 = +/- fb * b_odd (cancels the offset at first order)."""
    rho = np.sqrt(g * g - 1); bpred = 2 * (g - np.arcsinh(rho) / rho)
    out = []
    for sgn in (+1, -1):
        rec, st, Tper, sig, ps = run_cm(g, eps, N=N, b0=sgn * fb * bpred * eps, **kw)
        if st != 1:
            return None, st
        nback = int((np.diff(rec[:, 0, 0]) < 0).sum() + (np.diff(rec[:, 1, 0]) < 0).sum())
        bn, eta, ph = analyse(g, eps, rec, Tper, sig)
        kw.setdefault('_nback', []).append(nback) if False else None
        out.append((bn, eta))
    return (0.5 * (out[0][0] + out[1][0]), 0.5 * (out[0][1] + out[1][1]), out), 1


if __name__ == '__main__':
    print('# R1-formulation conformal NG (own E/B extension), pair at rest, E = eps sigma y, m = 500 GeV, Lambda = 1 keV')
    print('# exactly head-on even crossings break the conformal gauge -> initial transverse offset b0 = +/- fb b_odd, averaged')
    g = 1.3
    bb = np.sqrt(1 - 1 / g ** 2); r_ = g * bb
    bpred = 2 * (g - np.arcsinh(r_) / r_); G = bpred / (r_ * np.arctanh(bb))
    lr = np.log((g - 1) / (g - np.arcsinh(r_) / r_))
    Kfit = (3 * np.log(2) - 2) - 0.506 * np.log(g) - 0.077 * np.log(g) ** 2
    print(f'# gamma* = {g}: E1 b_odd/(eps l0) = {bpred:.5f}, G = {G:.5f}, E1 K(1.3) from fit = {Kfit:+.4f} (c03 table: -0.049 at 1.28)')
    print('# eps     N    fb    b_1/(eps l0) (avg)  ratio_to_E1   eta/eps (avg)  K = eta/(eps G) - ln(l_max/b_odd)  [eta(+), eta(-)]/eps')
    base = {}
    for eps in (1e-5, 1e-4, 1e-3):
        for N, fb in ((1024, 0.03), (4096, 0.03), (1024, 0.3), (4096, 0.3)):
            tic = time.time()
            res, st = pm_run(g, eps, N, fb)
            if res is None:
                print(f'{eps:7.0e} {N:5d} {fb:4.2f}  status {st} (invalid)', flush=True); continue
            bn, eta, out = res
            K = eta / (eps * G) - (np.log(1 / eps) + lr)
            base[(eps, N, fb)] = eta
            print(f'{eps:7.0e} {N:5d} {fb:4.2f}    {bn:.5f}        {bn / bpred:.5f}     {eta / eps:9.5f}     {K:+.4f}'
                  f'        [{out[0][1] / eps:.4f}, {out[1][1] / eps:.4f}]  {time.time() - tic:.0f}s', flush=True)
    print('# B* test (B* along z, normal of the orbit plane; and along y = E*), N = 1024, fb = 0.03: eta/eta(E only) - 1')
    for eps in (1e-5, 1e-4):
        for name, d in (('z', (0, 0, 1)), ('y', (0, 1, 0))):
            for kB in (1.0, 2.0, 4.0, 8.0, 16.0):
                res, st = pm_run(g, eps, 1024, 0.03, kB=kB, Bdir=d)
                if res is None or (eps, 1024, 0.03) not in base:
                    print(f'{eps:7.0e} B*||{name} kB={kB}: status {st}', flush=True); continue
                print(f'{eps:7.0e} B*||{name} kB={kB:4.1f}: d eta/eta = {res[1] / base[(eps, 1024, 0.03)] - 1:+.4e}', flush=True)
