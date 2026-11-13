"""nm_conformal.py -- E2: instrumented copy of the R1 conformal-gauge Nambu-Goto solver (code/R1_conformal_ng.py).

Same formulation as R1 (X = [A(tau+sigma) + B(tau-sigma)]/2, massive endpoints, delay ODE w_k(tau) = o_{1-k}(tau-pi),
classical RK4 with step h = pi/N, 4-point Lagrange midpoint of the delayed history).  Additions:
  * uniform E field (GeV/cm per unit charge): dp^0/dtau += q E.dX/dtau, dp_vec/dtau += q E dX^0/dtau;
  * initial data option: static straight string of length d along unit vector e between X1 = +d/2 e and
    X2 = -d/2 e (incoming null vectors point from the owner towards the partner: w1 = c(1, -e), w2 = c(1, +e),
    c = d/pi); the default (d_init = 0) reproduces R1 (string of length delta along unit(v2 - v1), quirk 1 at -delta/2);
  * selective record (same criteria as nm_kernel): rows [tau, X^4, P^4 (= m u), dX/dtau^4, J^4] for both ends at
    the same tau, J = cumulative string impulse integral of T (w - (u.w) u) dtau (RK4 weights).
Abort (status 7) when lab time falls > 1e-3 (1 + t_max) below its running maximum (conformal-gauge breakdown near exactly head-on crossings); the run is
then flagged invalid by the callers.
Validation (run this file): default initial data, B = 3.8 T -> hits identical to R1_conformal_ng.run.
Units: cm, GeV, c = 1; B in tesla.  Run: pixi run python analytic/numerics/nm_conformal.py
"""
import os, sys
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
KAPPA = 2.99792458e-3


def sigma_keV(lam):
    return (lam * 1e-6) ** 2 / 1.9732698e-14


@njit(cache=True)
def _mdot(a, b):
    return a[0] * b[0] - a[1] * b[1] - a[2] * b[2] - a[3] * b[3]


@njit(cache=True)
def _rhs(u, w, T, m, q, Bz, Ev, sp):
    uw = _mdot(u, w)
    du = (T / m) * (w - uw * u)          # same arithmetic as R1
    for c in range(4):
        sp[c] = T * (w[c] - uw * u[c])
    du[1] += q * KAPPA * uw * u[2] * Bz / m
    du[2] -= q * KAPPA * uw * u[1] * Bz / m
    if Ev[0] != 0.0 or Ev[1] != 0.0 or Ev[2] != 0.0:
        du[0] += q * uw * (Ev[0] * u[1] + Ev[1] * u[2] + Ev[2] * u[3]) / m
        du[1] += q * uw * Ev[0] * u[0] / m
        du[2] += q * uw * Ev[1] * u[0] / m
        du[3] += q * uw * Ev[2] * u[0] / m
    dX = uw * u
    return du, dX


@njit(cache=True)
def _herm(X0, X1, D0, D1, s):
    h00 = 2 * s ** 3 - 3 * s ** 2 + 1; h10 = s ** 3 - 2 * s ** 2 + s
    h01 = -2 * s ** 3 + 3 * s ** 2; h11 = s ** 3 - s ** 2
    return h00 * X0 + h10 * D0 + h01 * X1 + h11 * D1


@njit(cache=True)
def solve(p1, p2, m, T, Bz, Ev, q1, q2, N, t_end, delta, d_init, e_init, x1_0, max_steps, radii, max_hits,
          do_rec, max_rec, rec_near, rec_dlog, rec_dt, r_stop):
    h = np.pi / N
    RB = N + 8
    o = np.zeros((2, RB, 4))
    u = np.zeros((2, 4)); X = np.zeros((2, 4))
    for k in range(2):
        p = p1 if k == 0 else p2
        E = np.sqrt(m * m + p[0] ** 2 + p[1] ** 2 + p[2] ** 2)
        u[k, 0] = E / m; u[k, 1:] = p / m
    a0 = N + 4
    if d_init > 0.0:
        e = e_init / np.sqrt(e_init @ e_init)
        for c in range(3):
            X[0, 1 + c] = x1_0[c] + 0.5 * d_init * e[c]; X[1, 1 + c] = x1_0[c] - 0.5 * d_init * e[c]
        cc = d_init / np.pi
        for a in range(a0 + 1):
            o[1, a % RB, 0] = cc; o[1, a % RB, 1:] = -cc * e     # -> w1 = c(1, -e) (towards quirk 2)
            o[0, a % RB, 0] = cc; o[0, a % RB, 1:] = cc * e      # -> w2 = c(1, +e)
    else:
        v1 = u[0, 1:] / u[0, 0]; v2 = u[1, 1:] / u[1, 0]
        n = v2 - v1
        n = n / np.sqrt(n @ n)
        X[0, 1:] = -0.5 * delta * n; X[1, 1:] = 0.5 * delta * n
        c = delta / np.pi
        for a in range(a0 + 1):
            o[1, a % RB, 0] = c; o[1, a % RB, 1:] = c * n
            o[0, a % RB, 0] = c; o[0, a % RB, 1:] = -c * n
    hits = np.zeros((max_hits, 6)); nh = 0
    nr = max_rec if do_rec else 1
    rec0 = np.zeros((nr, 17)); rec1 = np.zeros((nr, 17)); nrr = 0
    J = np.zeros((2, 4)); lsep = -1.0; lt = -1e300
    qs = np.array([q1, q2])
    a = a0
    step = 0
    dXprev = np.zeros((2, 4))
    w0 = np.zeros((2, 4)); wh = np.zeros((2, 4)); w1 = np.zeros((2, 4))
    ku = np.zeros((4, 2, 4)); kX = np.zeros((4, 2, 4)); kS = np.zeros((4, 2, 4))
    sp = np.zeros(4)
    tguard = np.zeros(2)
    status = 0
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
            dXprev[k] = uw * u[k]
        if do_rec:
            sep = np.sqrt((X[0, 1] - X[1, 1]) ** 2 + (X[0, 2] - X[1, 2]) ** 2 + (X[0, 3] - X[1, 3]) ** 2)
            stl = h * (dXprev[0, 0] + dXprev[1, 0])
            want = sep < rec_near * stl or lsep < 0.0 or X[0, 0] - lt > rec_dt
            if not want and sep > 0.0:
                want = abs(np.log(sep / lsep)) > rec_dlog
            if want:
                lsep = sep if sep > 0.0 else 1e-300
                lt = X[0, 0]
                if nrr < max_rec:
                    tau = (a - a0) * h
                    rec0[nrr, 0] = tau; rec1[nrr, 0] = tau
                    for c in range(4):
                        rec0[nrr, 1 + c] = X[0, c]; rec0[nrr, 5 + c] = m * u[0, c]
                        rec0[nrr, 9 + c] = dXprev[0, c]; rec0[nrr, 13 + c] = J[0, c]
                        rec1[nrr, 1 + c] = X[1, c]; rec1[nrr, 5 + c] = m * u[1, c]
                        rec1[nrr, 9 + c] = dXprev[1, c]; rec1[nrr, 13 + c] = J[1, c]
                    nrr += 1
                else:
                    status = 6
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
                du, dX = _rhs(us[k], ws[k], T, m, qs[k], Bz, Ev, sp)
                ku[s, k] = du; kX[s, k] = dX; kS[s, k] = sp
        u = uk + h / 6.0 * (ku[0] + 2 * ku[1] + 2 * ku[2] + ku[3])
        X = Xk + h / 6.0 * (kX[0] + 2 * kX[1] + 2 * kX[2] + kX[3])
        J += h / 6.0 * (kS[0] + 2 * kS[1] + 2 * kS[2] + kS[3])
        for k in range(2):
            u[k, 0] = np.sqrt(1.0 + u[k, 1] ** 2 + u[k, 2] ** 2 + u[k, 3] ** 2)
        if X[0, 0] < tguard[0] - 1e-3 * (1.0 + tguard[0]) or X[1, 0] < tguard[1] - 1e-3 * (1.0 + tguard[1]):
            status = 7          # conformal-gauge breakdown: lab time runs backwards by > 1e-3 (1 + t_max) -> abort (invalid)
            break
        for k in range(2):
            if X[k, 0] > tguard[k]:
                tguard[k] = X[k, 0]
        for k in range(2):
            dXn = _mdot(u[k], w1[k]) * u[k]
            r0 = np.sqrt(Xk[k, 1] ** 2 + Xk[k, 2] ** 2); r1 = np.sqrt(X[k, 1] ** 2 + X[k, 2] ** 2)
            for L in range(radii.shape[0]):
                R = radii[L]
                if (r0 - R) * (r1 - R) < 0 and nh < max_hits:
                    lo = 0.0; hi = 1.0
                    for it in range(60):
                        mid = 0.5 * (lo + hi)
                        P = _herm(Xk[k], X[k], h * dXprev[k], h * dXn, mid)
                        rm = np.sqrt(P[1] ** 2 + P[2] ** 2)
                        if (r0 - R) * (rm - R) > 0:
                            lo = mid
                        else:
                            hi = mid
                    P = _herm(Xk[k], X[k], h * dXprev[k], h * dXn, 0.5 * (lo + hi))
                    hits[nh, 0] = k; hits[nh, 1] = L; hits[nh, 2:6] = P
                    nh += 1
        a += 1
        step += 1
        if X[0, 0] > t_end and X[1, 0] > t_end:
            break
        if np.sqrt(X[0, 1] ** 2 + X[0, 2] ** 2) > r_stop and np.sqrt(X[1, 1] ** 2 + X[1, 2] ** 2) > r_stop:
            break
    return hits[:nh], step, rec0[:nrr].copy(), rec1[:nrr].copy(), status


RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3])


def run(p1, p2, m, lam=None, sigma=None, Bz=3.8, E=(0.0, 0.0, 0.0), N=256, delta=1e-7, d_init=0.0,
        e_init=(1.0, 0.0, 0.0), x_c=(0.0, 0.0, 0.0), radii=None, max_steps=2_000_000_000, t_end=None, rec=False,
        max_rec=4_000_000, rec_near=8.0, rec_dlog=0.05, rec_dt=1e30, r_stop=None, charges=(1.0, -1.0)):
    T = sigma_keV(lam) if sigma is None else float(sigma)
    radii = RADII if radii is None else np.asarray(radii, float)
    p1 = np.asarray(p1, float); p2 = np.asarray(p2, float)
    P = p1 + p2
    Et = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    if t_end is None:
        t_end = 1.3 * radii[-1] / max(np.hypot(P[0], P[1]) / Et, 1e-3) + 5
    if r_stop is None:
        r_stop = radii[-1] + 3
    hits, nst, r0, r1, st = solve(p1, p2, float(m), T, float(Bz), np.asarray(E, float), float(charges[0]),
                                  float(charges[1]), int(N), float(t_end), float(delta), float(d_init),
                                  np.asarray(e_init, float), np.asarray(x_c, float), int(max_steps), radii, 100000,
                                  bool(rec), int(max_rec), float(rec_near), float(rec_dlog), float(rec_dt),
                                  float(r_stop))
    return dict(hits=hits, nsteps=nst, rec=(r0, r1), status=st, sigma=T)


if __name__ == '__main__':
    from R1_conformal_ng import run as r1run, make_event
    rng = np.random.default_rng(11)
    ok = True
    for lam in (0.6, 1.0):
        p1, p2 = make_event(rng, 500.0)
        H, canon, nst = r1run(p1, p2, 500.0, lam, Bz=3.8, N=256)
        r = run(p1, p2, 500.0, lam, Bz=3.8, N=256, rec=True)
        same = H.shape == r['hits'].shape and np.allclose(H, r['hits'], rtol=0, atol=1e-12)
        ok &= same
        print(f"[{'PASS' if same else 'FAIL'}] Lambda={lam}: hits equal to R1_conformal_ng ({len(H)} hits; max diff "
              f"{np.abs(H - r['hits']).max() if H.shape == r['hits'].shape else np.nan:.2e} cm; {nst} steps, "
              f"{len(r['rec'][0])} rows)", flush=True)
    print('ALL PASS' if ok else 'SOME FAILURES')
