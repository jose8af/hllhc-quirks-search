"""c12_Bstar_test.py -- E1 (after E2 FU3): does the CM magnetic field B* change the per-period axis rotation at first order?
Exact causal string (T2_propagator.CausalNullString, imported), pair at rest, uniform E* = eps sigma y_hat (perp. to n = x_hat)
plus a uniform B* with q|B*|/sigma = kB * eps (kB = 4 ~ 1/beta_cm for a transverse pair), along z (perp. to n and E*), along x (|| n),
or along y (|| E*).  Compares eta (rotation per period, from the apocentres of the relative coordinate x1 - x2 at equal CM time) and b_odd with the E*-only run.  Claim under test (§1.3, symmetry argument §9.3): B* gives no rotation at first order;
any change must scale as eps^2 (i.e. its ratio to the E*-only eta must scale as eps).
Usage: pixi run python analytic/checks/c12_Bstar_test.py > analytic/checks/c12_Bstar_test_out.txt
"""
import os, sys
import numpy as np
TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(TT, 'code'))
from T2_propagator import CausalNullString, interp_track, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T  # noqa: E402


def run(g, eps, Bdir, kB=4.0, nper=3, mb=1e-3, m=500.0, lam=1.0):
    sig = sigma_from_lambda_keV(lam); rho = np.sqrt(g * g - 1); ps = m * rho; T = 4 * ps / sig
    E = eps * sig * np.array([0, 1.0, 0])
    B = None if Bdir is None else kB * eps * sig / EB_GEV_PER_CM_PER_T * np.asarray(Bdir, float)
    cs = CausalNullString(m, sig, charges=(1.0, -1.0), Efield=E, Bfield=B, max_boost=mb, first_length=1e-9)
    traj, _ = cs.run(np.array([ps, 0, 0.0]), np.array([-ps, 0, 0.0]), (nper + 0.05) * T, max_steps=50_000_000)
    # relative coordinate at equal times; apocentres = max |r| per half period
    t = np.linspace(0.001 * T, (nper + 0.04) * T, 200001)
    r = interp_track(traj[0], t) - interp_track(traj[1], t)
    rr = np.linalg.norm(r, axis=1)
    ph = []
    for h in range(2 * nper):
        sel = (t >= h * T / 2) & (t < (h + 1) * T / 2)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        ph.append(np.arctan2(r[i, 1], r[i, 0]))   # in-plane (x-y) angle toward E*
    ph = (np.array(ph) + np.pi / 2) % np.pi - np.pi / 2
    ph = np.unwrap(2 * ph) / 2
    eta = np.mean(ph[2:] - ph[:-2])
    # out-of-plane (z) tilt of the axis per period
    phz = []
    for h in range(2 * nper):
        sel = (t >= h * T / 2) & (t < (h + 1) * T / 2)
        i = np.where(sel)[0][np.argmax(rr[sel])]
        phz.append(r[i, 2] / np.hypot(r[i, 0], r[i, 1]) * np.sign(r[i, 0]))
    phz = np.array(phz)
    return eta, np.mean(phz[2:] - phz[:-2])


if __name__ == '__main__':
    print('# gamma*  eps   B* direction   eta/eta(E only) - 1   z-tilt per period / eta(E only)')
    for g in (1.05, 1.3, 2.0):
        for eps in (1e-5, 1e-4):
            e0, z0 = run(g, eps, None)
            for name, d in (('z', (0, 0, 1)), ('x', (1, 0, 0)), ('y', (0, 1, 0))):
                e1, z1 = run(g, eps, d)
                print(f'{g:5.2f} {eps:7.0e}  B*||{name}:  {e1 / e0 - 1:+.2e}   {z1 / e0:+.2e}', flush=True)


def kB_scan():
    """Second test: sign and strength dependence of the B* effect (B* along z), gamma* = 1.3 and 2, eps = 1e-5."""
    print('# kB scan (B* along z), eps = 1e-5: kB, eta/eta(E only) - 1')
    for g in (1.3, 2.0):
        e0, _ = run(g, 1e-5, None)
        for kB in (-4.0, 1.0, 2.0, 4.0, 8.0, 16.0):
            e1, _ = run(g, 1e-5, (0, 0, 1), kB=kB)
            print(f'{g:5.2f}  kB={kB:+5.1f}:  {e1 / e0 - 1:+.4e}', flush=True)
