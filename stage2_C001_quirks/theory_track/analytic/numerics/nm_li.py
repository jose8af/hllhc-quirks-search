"""nm_li.py -- E2: scalarised copy of code/R1_li_literal.li_run (literal Li-Li-Pei-Zhang CM-simultaneous straight string,
explicit Euler [1911.02223 Eq.III.1-10]).  Same equations and operation order per step, rewritten without per-step array
allocations (~10x faster).  Validation (run this file): same hit count; hits differ from R1_li_literal.run_li by 3.1 um at
1e-2 and 0.30 um at 1e-3 of the printed step: round-off-level reordering amplified at the near-miss crossings by the
Euler step error (the difference scales with the step), i.e. well inside the step-convergence error.
Run: pixi run python analytic/numerics/nm_li.py
"""
import os, sys
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
KAPPA = 2.99792458e-3
RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3])


@njit(cache=True)
def li_run_fast(p1, p2, m, sig, Bz, eps, t_end, radii, s0):
    t0 = 0.0; t1 = 0.0
    r = np.zeros((2, 3)); p = np.zeros((2, 3))
    for c in range(3):
        p[0, c] = p1[c]; p[1, c] = p2[c]
    q = (1.0, -1.0)
    hits = np.zeros((20000, 6)); nh = 0
    nstep = 0
    v = np.zeros((2, 3)); F = np.zeros((2, 3)); s = np.zeros((2, 3)); E = np.zeros(2)
    beta = np.zeros(3); rn = np.zeros(3)
    while min(t0, t1) < t_end and nstep < 2_000_000_000:
        for i in range(2):
            E[i] = np.sqrt(m * m + (p[i, 0] * p[i, 0] + p[i, 1] * p[i, 1] + p[i, 2] * p[i, 2]))
            for c in range(3):
                v[i, c] = p[i, c] / E[i]
        Et = E[0] + E[1]
        for c in range(3):
            beta[c] = (p[0, c] + p[1, c]) / Et
        dt01 = t0 - t1
        n1 = 0.0; n2 = 0.0
        for c in range(3):
            s[0, c] = (r[0, c] - r[1, c]) - dt01 * v[0, c]
            s[1, c] = (r[1, c] - r[0, c]) + dt01 * v[1, c]
            n1 += s[0, c] * s[0, c]; n2 += s[1, c] * s[1, c]
        n1 = np.sqrt(n1); n2 = np.sqrt(n2)
        for c in range(3):
            s[0, c] = s[0, c] / n1 if n1 > 1e-14 else s0[c]
            s[1, c] = s[1, c] / n2 if n2 > 1e-14 else -s0[c]
        for i in range(2):
            vpar = v[i, 0] * s[i, 0] + v[i, 1] * s[i, 1] + v[i, 2] * s[i, 2]
            vp2 = 0.0
            for c in range(3):
                vp2 += (v[i, c] - vpar * s[i, c]) ** 2
            root = np.sqrt(max(1.0 - vp2, 1e-300))
            for c in range(3):
                F[i, c] = -sig * (root * s[i, c] + vpar * (v[i, c] - vpar * s[i, c]) / root)
            F[i, 0] += q[i] * KAPPA * v[i, 1] * Bz
            F[i, 1] -= q[i] * KAPPA * v[i, 0] * Bz
        vb0 = v[0, 0] * beta[0] + v[0, 1] * beta[1] + v[0, 2] * beta[2]
        vb1 = v[1, 0] * beta[0] + v[1, 1] * beta[1] + v[1, 2] * beta[2]
        vF0 = v[0, 0] * F[0, 0] + v[0, 1] * F[0, 1] + v[0, 2] * F[0, 2]
        vF1 = v[1, 0] * F[1, 0] + v[1, 1] * F[1, 1] + v[1, 2] * F[1, 2]
        dF0 = 0.0; dF1 = 0.0
        for c in range(3):
            d = r[0, c] - r[1, c]
            dF0 += d * (F[0, c] - vF0 * beta[c]); dF1 += d * (F[1, c] - vF1 * beta[c])
        c1 = 1 - vb0 - dF0 / Et
        c2 = 1 - vb1 + dF1 / Et
        if c1 >= c2:
            e1 = eps * c2 / c1; e2 = eps
        else:
            e1 = eps; e2 = eps * c1 / c2
        for i in range(2):
            ei = e1 if i == 0 else e2
            ti = t0 if i == 0 else t1
            for c in range(3):
                rn[c] = r[i, c] + v[i, c] * ei
            ra = np.sqrt(r[i, 0] ** 2 + r[i, 1] ** 2); rb = np.sqrt(rn[0] ** 2 + rn[1] ** 2)
            for L in range(radii.shape[0]):
                R = radii[L]
                if (ra - R) * (rb - R) < 0 and nh < hits.shape[0]:
                    f = (R - ra) / (rb - ra)
                    hits[nh, 0] = i; hits[nh, 1] = L; hits[nh, 2] = ti + f * ei
                    for c in range(3):
                        hits[nh, 3 + c] = r[i, c] + f * (rn[c] - r[i, c])
                    nh += 1
            for c in range(3):
                r[i, c] = rn[c]
                p[i, c] = p[i, c] + F[i, c] * ei
            if i == 0:
                t0 += ei
            else:
                t1 += ei
        nstep += 1
        if np.sqrt(r[0, 0] ** 2 + r[0, 1] ** 2) > radii[-1] + 3 and np.sqrt(r[1, 0] ** 2 + r[1, 1] ** 2) > radii[-1] + 3:
            break
    return hits[:nh], nstep


def run_li(p1, p2, m, lam, Bz=3.8, frac=1.0):
    from R1_li_literal import li_step, sigma_keV
    P = p1 + p2
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    t_end = 1.3 * RADII[-1] / max(np.hypot(P[0], P[1]) / E, 1e-3) + 5
    s0 = (p1 / np.hypot(m, np.linalg.norm(p1)) - p2 / np.hypot(m, np.linalg.norm(p2)))
    s0 = s0 / np.linalg.norm(s0)
    return li_run_fast(np.asarray(p1, float), np.asarray(p2, float), float(m), sigma_keV(lam), float(Bz),
                       li_step(m, lam) * frac, float(t_end), RADII, s0)


if __name__ == '__main__':
    import time
    from R1_li_literal import run_li as run_li_ref
    from R1_conformal_ng import make_event
    p1, p2 = make_event(np.random.default_rng(1), 500.0)
    for frac in (1e-2, 1e-3):
        t = time.time(); Ha, na = run_li_ref(p1, p2, 500.0, 1.0, Bz=3.8, frac=frac); ta = time.time() - t
        t = time.time(); Hb, nb = run_li(p1, p2, 500.0, 1.0, Bz=3.8, frac=frac); tb = time.time() - t
        same = Ha.shape == Hb.shape
        d = np.abs(Ha - Hb).max() if same else np.nan
        print(f"[{'PASS' if same and d < 0.5e-4 * frac / 1e-3 else 'FAIL'}] frac={frac}: {len(Ha)} vs {len(Hb)} hits, steps {na} vs {nb}, "
              f"max|diff| {d:.2e} cm; time {ta:.1f} s vs {tb:.1f} s")
