"""T3_field.py -- quick estimate of the radial (fringe) component of the CMS solenoid field inside the tracker (Q2).

Model (ESTIMATE): ideal finite solenoid = uniform azimuthal current sheet, radius a = 3.15 m, length 12.5 m
(CMS coil dimensions, UNVERIFIED, recalled), no iron yoke (the yoke straightens the field lines near the coil
ends, so the sheet model OVERestimates B_r at the tracker ends), normalised to B_z(0,0) = 3.8112 T.
Field of one current loop from the standard elliptic-integral formulas (Jackson-type / Smythe); the sheet
is integrated with Gauss-Legendre in z'.
Output: B_r/B_z on the tracker barrel layer radii at |z| = 0.5, 1.2, 2.0, 2.7 m, and at |eta| = 1, 1.5, 2, 2.5
on the outer OT radius; a map (r <= 1.2 m, |z| <= 3 m) saved to figures/T3_field_map.npz (for T3_propagator bmode=2).
Run: pixi run python code/T3_field.py
"""
import os
import numpy as np
from scipy.special import ellipk, ellipe

A_COIL = 315.0       # cm
HALF_L = 625.0       # cm
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')


def loop_field(r, z, a):
    """B_r, B_z (arbitrary units, mu0 I/(2 pi) = 1) of a current loop of radius a at z = 0."""
    r = np.maximum(r, 1e-9)
    k2 = 4 * a * r / ((a + r) ** 2 + z ** 2)
    K = ellipk(k2); E = ellipe(k2)
    den = np.sqrt((a + r) ** 2 + z ** 2)
    d2 = (a - r) ** 2 + z ** 2
    Bz = (K + (a * a - r * r - z * z) / d2 * E) / den
    Br = z / r * (-K + (a * a + r * r + z * z) / d2 * E) / den
    return Br, Bz


def sheet_field(r, z, n=400):
    x, w = np.polynomial.legendre.leggauss(n)
    zs = HALF_L * x; ws = HALF_L * w
    Br = np.zeros_like(np.asarray(r, float)); Bz = np.zeros_like(Br)
    for zp, wp in zip(zs, ws):
        br, bz = loop_field(r, z - zp, A_COIL)
        Br += wp * br; Bz += wp * bz
    return Br, Bz


if __name__ == '__main__':
    _, b0 = sheet_field(np.array([1e-3]), np.array([0.0]))
    norm = 3.8112 / b0[0]
    print('B_r / B_z(0) [%] for the finite-sheet CMS solenoid (no yoke; overestimate):')
    radii = [3.0, 14.6, 24.9, 52.3, 86.0, 108.3]
    print('| |z| [cm] | ' + ' | '.join(f'r={R}' for R in radii) + ' | B_z(r=108,z)/B_z(0) |')
    print('|---|' + '---|' * (len(radii) + 1))
    for zz in (50.0, 120.0, 200.0, 270.0):
        br, bz = sheet_field(np.array(radii), np.full(len(radii), zz))
        print(f'| {zz:.0f} | ' + ' | '.join(f'{100*b*norm/3.8112:.2f}' for b in br) + f' | {bz[-1]*norm/3.8112:.3f} |')
    print('On the outer OT radius r = 108.3 cm at fixed eta:')
    for eta in (0.5, 1.0, 1.5, 2.0, 2.4):
        zz = 108.3 * np.sinh(eta)
        br, bz = sheet_field(np.array([108.3]), np.array([zz]))
        print(f'  eta={eta}: z={zz:.0f} cm  B_r/B_z(0) = {100*br[0]*norm/3.8112:.2f} %,  B_z/B_z(0) = {bz[0]*norm/3.8112:.3f}')
    rg = np.linspace(0, 130, 66); zg = np.linspace(0, 300, 151)
    R, Z = np.meshgrid(rg, zg, indexing='ij')
    br, bz = sheet_field(R.ravel(), Z.ravel())
    grid = np.stack([br.reshape(R.shape) * norm, bz.reshape(R.shape) * norm])
    np.savez(os.path.join(FIG, 'T3_field_map.npz'), grid=grid, r=rg, z=zg)
    print('map saved')
