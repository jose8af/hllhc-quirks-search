"""c14_Bstar_cscan.py -- E1 fix pass S1-R1 (critical A1/B1): does the CM magnetic field B* change the B-response coefficient
c_k = [eta(eps0/k) k / eta(eps0) - 1]/ln k at the field values of the 3 keV (and 1 keV) B scans?
Exact causal string (T2_propagator.CausalNullString, imported), pair at rest, E* = eps sigma (cos a, sin a, 0) with the initial
axis n = x_hat, plus B* = kB eps sigma/q along z (normal to the orbit plane) or along E*.  kB = q|B*|/(q|E*|) is fixed while
the field is scaled (both scale with the lab B), so eta(eps; kB) at eps0/k gives the per-pair c_k with and without B*.
Under the per-pair hypothesis Ds ~ eta (rotating yo-yo), the B*-induced change of the per-event c is Delta c_k = c_k(kB) - c_k(0).
eps0 = 6e-6 ~ typical eps_perp at 3 keV, 500 GeV, B0 (k = 1, 2, 4, 20); eps0 = 5e-5 ~ 1 keV (k = 1, 4, 20, 80).
max_boost 1e-3 (b_odd/l0 >= 2e-7 for all runs; the with/without-B* difference is taken at identical settings).
Run: pixi run python analytic/checks/c14_Bstar_cscan.py > analytic/checks/c14_Bstar_cscan_out.txt
"""
import os, sys
import numpy as np
TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'code'))
from T2_propagator import CausalNullString, interp_track, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T  # noqa: E402


def eta_of(g, eps, kB, Bdir='z', alpha=np.pi / 2, nper=3, mb=1e-3, m=500.0, lam=1.0):
    sig = sigma_from_lambda_keV(lam); rho = np.sqrt(g * g - 1); ps = m * rho; T = 4 * ps / sig
    eh = np.array([np.cos(alpha), np.sin(alpha), 0.0])
    E = eps * sig * eh
    if kB == 0:
        B = None
    else:
        d = np.array([0, 0, 1.0]) if Bdir == 'z' else eh
        B = kB * eps * sig / EB_GEV_PER_CM_PER_T * d
    traj, _ = CausalNullString(m, sig, charges=(1.0, -1.0), Efield=E, Bfield=B, max_boost=mb,
                               first_length=1e-9).run(np.array([ps, 0, 0.0]), np.array([-ps, 0, 0.0]), (nper + 0.05) * T,
                                                      max_steps=80_000_000)
    t = np.linspace(0.001 * T, (nper + 0.04) * T, 200001)
    r = interp_track(traj[0], t) - interp_track(traj[1], t)
    rr = np.linalg.norm(r, axis=1)
    # rotation of the axis toward the E*_perp direction (y for alpha = 90 deg): in-plane angle in the x-y plane
    ph = []
    for h in range(2 * nper):
        sel = (t >= h * T / 2) & (t < (h + 1) * T / 2)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        ph.append(np.arctan2(r[i, 1], r[i, 0]))
    ph = (np.array(ph) + np.pi / 2) % np.pi - np.pi / 2
    ph = np.unwrap(2 * ph) / 2
    return np.mean(ph[2:] - ph[:-2])


if __name__ == '__main__':
    cases = [(1.1, 'z', 90), (1.3, 'z', 90), (1.6, 'z', 90), (1.3, 'E', 90), (1.3, 'z', 60)]
    for eps0, ks, tag in ((6e-6, (2, 4, 20), '3 keV-like'), (5e-5, (4, 20, 80), '1 keV-like')):
        print(f'\n## eps0 = {eps0:g} ({tag}); c_k = [k eta(eps0/k)/eta(eps0) - 1]/ln k', flush=True)
        print('# gamma*  B*dir  alpha  kB |  c_k (k = ' + ', '.join(map(str, ks)) + ')  |  Delta c_k vs kB = 0  | Delta eta/eta at eps0')
        for g, bd, a in cases:
            base = None
            for kB in (0, 2, 4, 8, 12):
                etas = [eta_of(g, eps0 / k, kB, bd, np.deg2rad(a)) for k in (1,) + ks]
                cks = [(k * etas[i + 1] / etas[0] - 1) / np.log(k) for i, k in enumerate(ks)]
                if kB == 0:
                    base = (cks, etas[0])
                    print(f'{g:5.2f}  {bd}  {a:3d}  {kB:3d} | ' + ' '.join(f'{c:.4f}' for c in cks) + ' |        (reference)', flush=True)
                else:
                    print(f'{g:5.2f}  {bd}  {a:3d}  {kB:3d} | ' + ' '.join(f'{c:.4f}' for c in cks) + ' | ' +
                          ' '.join(f'{c - b:+.4f}' for c, b in zip(cks, base[0])) + f' | {etas[0] / base[1] - 1:+.4f}', flush=True)
