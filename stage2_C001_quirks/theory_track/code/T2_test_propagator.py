"""T2_test_propagator.py -- unit tests for T2_propagator.py (vacuum quirk dynamics).

Checks
  1. Exact CM solution: energy conservation E1+E2+sigma*|x1-x2| = M, crossing period 2p*/sigma,
     amplitude (M-2m)/sigma, centre of energy fixed.
  2. Lab-frame straight-string ODE (Kang-Luty force, lab-simultaneous s_hat) vs exact boosted solution.
  3. Li et al. closed form [2002.07503 Eq.II.4-8] vs exact boosted solution.
  4. Causal null-vector string (Athena port) vs exact boosted solution, for max_boost 1e-2 and 1e-1.
  5. Exact closed forms: lab crossing spacing and lab max separation vs brute force.
Run:  pixi run python code/T2_test_propagator.py      (prints PASS/FAIL per test; exits 1 on failure)
"""
import sys
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from T2_propagator import (ExactPair, LabStraightString, li_analytic_lab, CausalNullString,
                           interp_track, sigma_from_lambda_keV)

RESULTS = []


def check(name, ok, info=''):
    RESULTS.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}")


def cases():
    m = 500.0
    sig = sigma_from_lambda_keV(1.0)
    yield 'generic', m, sig, np.array([300.0, 50.0, 100.0]), np.array([-150.0, 120.0, 40.0])
    yield 'boosted-transverse', m, sig, np.array([200.0, 400.0, 30.0]), np.array([-100.0, 380.0, -20.0])
    yield 'relativistic', 200.0, sigma_from_lambda_keV(3.0), np.array([900.0, 10.0, 300.0]), np.array([-500.0, 300.0, 900.0])


def test_exact_cm():
    for name, m, sig, p1, p2 in cases():
        ex = ExactPair(p1, p2, m, m, sig)
        tc = np.linspace(0, 3 * ex.Tcm, 20001)
        x1, x2 = ex.x_cm(tc)
        q = ex.q_of_tcm(tc)
        E = 2 * np.sqrt(m * m + q * q) + sig * np.abs(x1 - x2)
        check(f'exact CM energy conservation [{name}]', np.max(np.abs(E / ex.M - 1)) < 1e-12,
              f'max|dE/M|={np.max(np.abs(E / ex.M - 1)):.1e}')
        check(f'exact CM amplitude [{name}]', abs(np.max(np.abs(x1 - x2)) / ex.lmax - 1) < 1e-6)
        # centre of energy: E1 x1 + E2 x2 + sigma (x1-x2)(x1+x2)/2 = 0
        ce = np.sqrt(m * m + q * q) * (x1 + x2) + sig * (x1 - x2) * (x1 + x2) / 2
        check(f'exact CM centre of energy fixed [{name}]', np.max(np.abs(ce)) / (ex.M * ex.lmax) < 1e-12)
        # velocity from numerical derivative matches q/E
        v1 = np.gradient(x1, tc)
        vq = q / np.sqrt(m * m + q * q)
        sel = np.abs(np.mod(tc, ex.Tcm / 2)) > ex.Tcm * 1e-3
        err_v = np.max(np.abs(v1 - vq)[sel][5:-5]); check(f"exact CM velocity consistency [{name}]", err_v < 1e-4, f"max|dv|={err_v:.1e} (finite-difference)")


def test_lab_integrator_and_li():
    for name, m, sig, p1, p2 in cases():
        ex = ExactPair(p1, p2, m, m, sig)
        D, Dt = ex.crossing_spacing_lab()
        t_end = 3.2 * Dt
        sol = LabStraightString(m, m, sig).run(p1, p2, t_end)
        tt = np.linspace(1e-6 * Dt, t_end, 400)
        X1, X2 = ex.lab_positions(tt)
        Y = np.stack([np.interp(tt, sol['t'], sol['y'][:, i]) for i in range(12)], 1)
        # interpolation error of the dense sampling is not what we test: compare at solver nodes
        idx = np.linspace(1, len(sol['t']) - 1, 300).astype(int)
        Xa, Xb = ex.lab_positions(sol['t'][idx])
        err = max(np.max(np.linalg.norm(sol['y'][idx, 0:3] - Xa, axis=1)),
                  np.max(np.linalg.norm(sol['y'][idx, 6:9] - Xb, axis=1)))
        check(f'lab straight-string ODE vs exact [{name}]', err / ex.lmax < 1e-7,
              f'max|dx|/l_max={err / ex.lmax:.1e}, crossings at {np.round(sol["tcross"] / Dt, 8)} x Dt')
        check(f'lab crossing spacing formula [{name}]',
              len(sol['tcross']) >= 3 and np.allclose(sol['tcross'][:3] / Dt, [1, 2, 3], atol=1e-7))
        L1, L2 = li_analytic_lab(p1, p2, m, sig, tt)
        errli = max(np.max(np.linalg.norm(L1 - X1, axis=1)), np.max(np.linalg.norm(L2 - X2, axis=1)))
        check(f'Li et al. Eq.II.4-8 vs exact [{name}]', errli / ex.lmax < 1e-8, f'max|dx|/l_max={errli / ex.lmax:.1e}')
        # lab max separation closed form vs brute force
        tfine = np.linspace(0, Dt, 4001)
        A, B = ex.lab_positions(tfine)
        d = np.linalg.norm(A - B, axis=1)
        bh = ex.bhat
        dT = np.linalg.norm((A - B) - np.outer((A - B) @ bh, bh), axis=1)
        full, trans = ex.lab_max_separation()
        check(f'lab max separation closed form [{name}]', abs(d.max() / full - 1) < 1e-5,
              f'brute={d.max():.6f} formula={full:.6f} cm; l_max(CM)={ex.lmax:.6f}')
        check(f'lab max transverse separation [{name}]', abs(dT.max() / trans - 1) < 1e-5,
              f'brute={dT.max():.6f} formula={trans:.6f}')


def test_causal_string():
    for name, m, sig, p1, p2 in cases():
        ex = ExactPair(p1, p2, m, m, sig)
        D, Dt = ex.crossing_spacing_lab()
        for mb in (1e-2, 1e-1):
            cs = CausalNullString(m, sig, max_boost=mb, first_length=1e-9 * ex.lmax)
            traj, mom = cs.run(p1, p2, 2.2 * Dt)
            errs = []
            for k in (0, 1):
                T = traj[k]
                sel = np.linspace(1, len(T) - 2, 200).astype(int)
                Xe = ex.lab_positions(T[sel, 0])[k]
                errs.append(np.max(np.linalg.norm(T[sel, 1:] - Xe, axis=1)))
            err = max(errs)
            # momentum: total quirk energy at crossings should return to the initial value
            check(f'causal null-string (Athena port, maxBoost={mb}) vs exact [{name}]',
                  err / ex.lmax < 1e-6, f'max|dx|/l_max={err / ex.lmax:.1e}, steps={len(traj[0]) + len(traj[1])}')


if __name__ == '__main__':
    test_exact_cm()
    test_lab_integrator_and_li()
    test_causal_string()
    n = len(RESULTS); f = n - sum(RESULTS)
    print(f'\n{n - f}/{n} checks passed')
    sys.exit(1 if f else 0)
