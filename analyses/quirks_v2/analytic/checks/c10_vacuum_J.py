"""c10_vacuum_J.py -- E1 (after E2): vacuum yo-yo with constant angular momentum J = b p* (no field), straight-string
models of c04 (QS central force; KL = Li in the CM frame), to check the NR closed form of c09(a):
psi_vac per crossing = (b/l_max)[ln(l_max/b) + 3 ln 2 - 2]  (NR), and to compare with E2's M2a fit
psi = A_hat (b/l_max) ln(L/b) (A_hat = 0.996/0.951/0.88/0.79, L/l_max = 0.985/0.90/0.56/0.43 at gamma* = 1.05/1.3/2/3, exact NG).
Initial data: r_1,2 = +/-(d/2) y_hat, p_1,2 = +/- p* x_hat (so b = d at every crossing for central forces).
Output: per gamma*, fitted A_hat_model and K_vac = ln(L/l_max) from d/l0 = 1e-7..1e-3, compared with
A_hat_pred(NG) = 2(gamma*-1)/(rho artanh beta*) and the model's own prediction.
Run: pixi run python analytic/checks/c10_vacuum_J.py > analytic/checks/c10_vacuum_J_out.txt
"""
import numpy as np
from scipy.integrate import solve_ivp
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c04_straight_E import rhs_factory


def run_vac(model, g, d, nhalf=4):
    rho = np.sqrt(g * g - 1); T = 4 * rho
    y0 = np.array([0, d / 2, 0, -d / 2, rho, 0, -rho, 0.0])
    sol = solve_ivp(rhs_factory(model, 0.0), (0, (nhalf / 2 + 0.05) * T), y0, method='DOP853', rtol=1e-12, atol=1e-18,
                    dense_output=True, max_step=T / 400)
    t = np.linspace(0, (nhalf / 2 + 0.05) * T, 200001)
    Y = sol.sol(t); r1 = Y[0:2].T; rr = np.linalg.norm(r1, axis=1)
    phis = []
    for h in range(nhalf):
        sel = (t >= h * T / 2) & (t < (h + 1) * T / 2)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        phis.append(np.arctan2(r1[i, 1], r1[i, 0]))
    phi = (np.array(phis) + np.pi / 2) % np.pi - np.pi / 2
    phi = np.unwrap(2 * phi) / 2
    return np.diff(phi)          # rotation across crossings 1, 2, 3 (apocentre to apocentre)


if __name__ == '__main__':
    for model in ('QS', 'KL'):
        for g in (1.0005, 1.05, 1.3, 2.0, 3.0):
            rho = np.sqrt(g * g - 1); be = rho / g; lmax = 2 * (g - 1)
            ds = np.logspace(-7, -3, 9) * min(1.0, lmax)
            psis = np.array([np.mean(np.abs(run_vac(model, g, d))) for d in ds])
            # fit psi/(b/lmax) = A_hat ln(lmax/b) + A_hat K
            X = np.log(lmax / ds); Yv = psis / (ds / lmax)
            Ah, c0 = np.polyfit(X, Yv, 1)
            Ah_ng = 2 * (g - 1) / (rho * np.arctanh(be))
            print(f'{model} gamma*={g}: A_hat={Ah:.4f} (NG pred {Ah_ng:.4f}; QS pred {Ah_ng*np.arctanh(be)/be:.4f}), '
                  f'K_vac=ln(L/l_max)={c0/Ah:+.4f}   (NR analytic 3ln2-2 = {3*np.log(2)-2:.4f})', flush=True)
