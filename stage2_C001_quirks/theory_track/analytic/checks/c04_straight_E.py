"""c04_straight_E.py -- E1: the same reduced problem as c03 (pair at rest in a uniform E*), solved with
STRAIGHT-STRING models instead of the exact NG string, to answer "does the logarithm need string curvature or
retardation?" (NEAR_MISS_IMPULSE.md §4.4) and to obtain the non-relativistic constant K_NR (§4.3).

Models (CM frame; both quirks at equal CM time, which is exactly Li et al.'s CM-simultaneity t1 - t2 = beta.(r1 - r2)
[1911.02223 Eq.III.6] for P = 0; s_hat_i = unit(r_i - r_j), which is Li's Eq.III.8-9 with Delta t = 0):
  'KL'  : Kang-Luty force [0805.4642 Eq.3.8]  d(m gamma v)/dt = -sigma[sqrt(1-v_perp^2) s + (v.s) v_perp/sqrt(1-v_perp^2)] + qE
          (= the Li et al. straight-string integrator in the pair rest frame, but integrated with an adaptive
          8th-order Runge-Kutta instead of explicit Euler);
  'QS'  : quasi-static central force  d(m gamma v)/dt = -sigma s + qE  (relativistic kinematics, no KL velocity terms).
Units: m = 1, sigma = 1 (lengths in l0 = m/sigma).  E = eps * sigma * y_hat, quirk 1 (charge +1) starts along +x.
Measured: b_odd/b_odd_pred (angular-momentum formula, §3.2) and the axis rotation per period eta;
fit eta/(eps G_model) - ln(l_max/b_odd) = K_model, with G_model = G_NG * A_model/A_NG, A_model/A_NG from §4.4
(KL: (1-beta^2) artanh(beta)/beta; QS: artanh(beta)/beta).
Run: pixi run python analytic/checks/c04_straight_E.py > analytic/checks/c04_straight_E_out.txt
"""
import numpy as np
from scipy.integrate import solve_ivp


def rhs_factory(model, eps):
    E = np.array([0.0, eps])

    def rhs(t, y):
        r1, r2, p1, p2 = y[0:2], y[2:4], y[4:6], y[6:8]
        d = r1 - r2
        s = d / np.linalg.norm(d)
        out = np.empty(8)
        for k, (p, sv, q) in enumerate(((p1, s, 1.0), (p2, -s, -1.0))):
            Ek = np.sqrt(1.0 + p @ p)
            v = p / Ek
            if model == 'KL':
                vpar = v @ sv
                vperp = v - vpar * sv
                vp2 = vperp @ vperp
                F = -(np.sqrt(1 - vp2) * sv + vpar * vperp / np.sqrt(1 - vp2)) + q * E
            else:
                F = -sv + q * E
            out[2 * k:2 * k + 2] = v
            out[4 + 2 * k:6 + 2 * k] = F
        return out
    return rhs


def run(model, g, eps, nper, rtol=1e-12):
    rho = np.sqrt(g * g - 1)
    T = 4 * rho                       # period (sigma = m = 1); exact for QS and KL in vacuum
    d0 = 1e-13
    y0 = np.array([d0 / 2, 0, -d0 / 2, 0, rho, 0, -rho, 0])
    sol = solve_ivp(rhs_factory(model, eps), (0, (nper + 0.05) * T), y0, method='DOP853', rtol=rtol, atol=1e-16,
                    dense_output=True, max_step=T / 400)
    t = np.linspace(0, (nper + 0.05) * T, 400001)
    Y = sol.sol(t)
    r1 = Y[0:2].T; r2 = Y[2:4].T
    # miss distances at crossings
    bs = []
    for k in range(1, 2 * nper + 1):
        tw = np.linspace((k / 2 - 0.02) * T, (k / 2 + 0.02) * T, 2001)
        for _ in range(5):
            Yw = sol.sol(tw)
            dd = np.linalg.norm(Yw[0:2] - Yw[2:4], axis=0)
            j = np.argmin(dd)
            tw = np.linspace(tw[max(j - 3, 0)], tw[min(j + 3, len(tw) - 1)], 2001)
        bs.append(dd[j])
    # apocentres of quirk 1 (max |r1| in each half period)
    rr = np.linalg.norm(r1, axis=1)
    phis = []
    for h in range(2 * nper):
        sel = (t >= h * T / 2) & (t < (h + 1) * T / 2)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        phis.append(np.arctan2(r1[i, 1], r1[i, 0]))
    phi = (np.array(phis) + np.pi / 2) % np.pi - np.pi / 2
    phi = np.unwrap(2 * phi) / 2
    return np.array(bs), phi[2:] - phi[:-2]


def G_NG(g):
    rho = np.sqrt(g * g - 1); be = rho / g
    return 2 * (g - np.arcsinh(rho) / rho) / (rho * np.arctanh(be))


def bodd(eps, g):
    rho = np.sqrt(g * g - 1)
    return 2 * eps * (g - np.arcsinh(rho) / rho)


if __name__ == '__main__':
    for model in ('QS', 'KL'):
        for g in (1.0005, 1.05, 1.28, 2.0):
            be = np.sqrt(g * g - 1) / g
            Arat = (np.arctanh(be) / be) * ((1 - be * be) if model == 'KL' else 1.0)
            Gm = G_NG(g) * Arat
            print(f'# model {model}, gamma*={g}, beta*={be:.4f}, A_model/A_NG={Arat:.4f}, G_model={Gm:.4f}')
            print('#   eps     b1/bpred  b2/b1    eta/(eps G_model)   ln(lmax/b_odd)   K_model')
            for eps in (1e-6, 1e-5, 1e-4):
                bs, eta = run(model, g, eps, 3)
                bp = bodd(eps, g)
                L = np.log(2 * (g - 1) / bp)
                ratio = np.mean(eta) / (eps * Gm)
                print(f'  {eps:8.1e}  {bs[0] / bp:.5f}  {bs[1] / bs[0]:.2e}   {ratio:9.4f} (std {np.std(eta)/np.mean(eta):.1e})'
                      f'   {L:8.4f}   {ratio - L:+.4f}', flush=True)
