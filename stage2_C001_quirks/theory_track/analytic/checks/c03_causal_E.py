"""c03_causal_E.py -- E1 targeted numerical test of NEAR_MISS_IMPULSE.md §3-4 with the exact causal NG string.

Setup (the exact reduced problem of §1.3): a quirk pair produced at the origin of its rest frame with momenta
+/- p* x_hat, charges +/-1, in a uniform constant electric field E* (GeV/cm per unit charge) at angle alpha to x_hat
(in the x-y plane), no B*.  Propagator: T2_propagator.CausalNullString (Athena-type piecewise-null exact NG with
massive endpoints; imported, not modified), which supports a uniform E field.
Measured per run:
  * miss distance b_k at crossings k = 1..K (closest approach of the two quirks near t = k T*/2), compared with
    b_odd = 2 eps_perp l0 [gamma* - asinh(rho)/rho]  (§3.2, eps_perp = qE*_perp/sigma, l0 = m/sigma);
  * axis angle phi_j at the apocentres of quirk 0 (local maxima of |x_0|), mod pi; rotation per period
    eta = <phi_{j+2} - phi_j>, compared with eta = eps_perp G(gamma*) [ln(l_max/b_odd) + K]  (§4-5), from which
    K is extracted.
Usage: pixi run python analytic/checks/c03_causal_E.py [gamma*] [alpha_deg] [nper] [max_boost]
Output: printed table (saved as c03_causal_E_out*.txt).
"""
import os, sys, time
import numpy as np
TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'code'))
from T2_propagator import CausalNullString, interp_track, sigma_from_lambda_keV  # noqa: E402


def G_of(g):
    rho = np.sqrt(g * g - 1); be = rho / g
    return 2 * (g - np.arcsinh(rho) / rho) / (rho * np.arctanh(be))


def bodd_pred(eps_perp, g, l0):
    rho = np.sqrt(g * g - 1)
    return 2 * eps_perp * l0 * (g - np.arcsinh(rho) / rho)


def run_one(m, lam, g, eps, alpha, nper, mb, first_length=1e-9):
    sig = sigma_from_lambda_keV(lam)
    l0 = m / sig
    rho = np.sqrt(g * g - 1); ps = m * rho
    Tstar = 4 * ps / sig
    p1 = np.array([ps, 0, 0.0]); p2 = -p1
    E = eps * sig * np.array([np.cos(alpha), np.sin(alpha), 0.0])
    cs = CausalNullString(m, sig, charges=(1.0, -1.0), Efield=E if eps > 0 else None, max_boost=mb,
                          first_length=first_length)
    traj, mom = cs.run(p1, p2, (nper + 0.05) * Tstar, max_steps=50_000_000)
    # miss distances at crossings
    bs = []
    for k in range(1, 2 * nper + 1):
        tw = np.linspace((k / 2 - 0.02) * Tstar, (k / 2 + 0.02) * Tstar, 4001)
        for _ in range(4):
            d = np.linalg.norm(interp_track(traj[0], tw) - interp_track(traj[1], tw), axis=1)
            j = np.argmin(d)
            tw = np.linspace(tw[max(j - 3, 0)], tw[min(j + 3, len(tw) - 1)], 4001)
        bs.append(d[j])
    # apocentres of quirk 0
    X = traj[0]
    r = np.linalg.norm(X[:, 1:], axis=1)
    idx = [i for i in range(1, len(r) - 1) if r[i] >= r[i - 1] and r[i] > r[i + 1] and r[i] > 0.5 * (g - 1) * l0]
    # keep one per half period (largest r within each half period window)
    apo = []
    for h in range(2 * nper):
        sel = [i for i in idx if h * Tstar / 2 <= X[i, 0] < (h + 1) * Tstar / 2]
        if sel:
            i = max(sel, key=lambda i: r[i])
            apo.append(np.arctan2(X[i, 2], X[i, 1]))
    phi = np.array(apo)
    phi = (phi + np.pi / 2) % np.pi - np.pi / 2       # axis angle mod pi
    phi = np.unwrap(phi * 2) / 2
    return np.array(bs), phi, l0


if __name__ == '__main__':
    g = float(sys.argv[1]) if len(sys.argv) > 1 else 1.28
    alpha = np.deg2rad(float(sys.argv[2])) if len(sys.argv) > 2 else np.pi / 2
    nper = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    mb = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-3
    m, lam = 500.0, 1.0
    print(f'# causal NG, pair at rest in uniform E*, m={m} GeV, Lambda={lam} keV, gamma*={g}, alpha={np.rad2deg(alpha):.1f} deg,'
          f' max_boost={mb}, {nper} periods')
    print(f'# G(gamma*) = {G_of(g):.4f}')
    print('# eps=qE/sigma | b_1..b_4 / b_odd_pred | eta per period (mean, std over periods) | eta/(eps_perp G) | '
          'ln(lmax/b_odd) | K = eta/(eps_perp G) - ln')
    for eps in (0.0, 1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4, 1e-3):
        t0 = time.time()
        bs, phi, l0 = run_one(m, lam, g, eps, alpha, nper, mb)
        epp = eps * abs(np.sin(alpha))
        bp = bodd_pred(epp, g, l0) if eps > 0 else np.nan
        eta = phi[2:] - phi[:-2]
        lmax = 2 * (g - 1) * l0
        if eps > 0:
            ratio = np.mean(eta) / (epp * G_of(g))
            L = np.log(lmax / bp)
            print(f'{eps:8.1e} | ' + ' '.join(f'{x / bp:.4f}' for x in bs[:4]) +
                  f' | {np.mean(eta):.4e} +- {np.std(eta):.1e} | {ratio:.4f} | {L:.4f} | {ratio - L:+.4f}  ({time.time() - t0:.0f} s)',
                  flush=True)
        else:
            print(f'{eps:8.1e} | b = ' + ' '.join(f'{x:.2e}' for x in bs[:4]) + f' cm | eta = {np.mean(eta):.2e} '
                  f'({time.time() - t0:.0f} s)', flush=True)
