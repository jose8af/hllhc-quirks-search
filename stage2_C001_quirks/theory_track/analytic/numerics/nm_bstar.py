"""nm_bstar.py -- E2 fix pass 2: lab fields that give the pure-E* pair-frame problem ("B* switched off").
For an event with pair velocity beta (P0/E0), the lab field B gives CM fields E* = gamma beta x B, B* = gamma B - (gamma-1)(B.bh)bh.
The uniform lab fields  E_lab = gamma^2 beta x B  (E_lab . beta = 0)  and  B_lab = gamma^2 [beta (beta.B) - beta^2 B]
transform to exactly (E*, 0) in the P0 frame (inverse boost of (E*, 0)).  Units: B in tesla; E in GeV/cm per unit charge
(x EB_GEV_PER_CM_PER_T).  check(): numerical transform of (E_lab, B_lab) back to the P0 frame.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'code'))
from T2_propagator import EB_GEV_PER_CM_PER_T as EB


def pair_beta(p1, p2, m):
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    return (np.asarray(p1) + np.asarray(p2)) / E


def bstar_off_fields(p1, p2, m, B=(0.0, 0.0, 3.8112)):
    b = pair_beta(p1, p2, m); B = np.asarray(B, float)
    g2 = 1.0 / (1.0 - b @ b)
    E_lab = g2 * np.cross(b, B) * EB
    B_lab = g2 * (b * (b @ B) - (b @ b) * B)
    return E_lab, B_lab


def cm_to_lab(Ep, Bp, b):
    """Inverse of to_cm: fields (Ep [GeV/cm per charge], Bp [T]) in the frame moving with b -> lab fields."""
    return to_cm(Ep, Bp, -np.asarray(b))


def eperp_only_fields(p1, p2, m, n0, B=(0.0, 0.0, 3.8112)):
    """Lab fields giving, in the P0 frame, only E*_perp = E* - (E*.n0) n0 (no E*_par, no B*); n0 = initial CM axis."""
    b = pair_beta(p1, p2, m)
    Es, _ = to_cm(np.zeros(3), np.asarray(B, float), b)
    n0 = np.asarray(n0, float) / np.linalg.norm(n0)
    Ep = Es - (Es @ n0) * n0
    return cm_to_lab(Ep, np.zeros(3), b)


def to_cm(E, B, b):
    """Fields in the frame moving with velocity b (E in GeV/cm per charge, B in T)."""
    Bn = B * EB                      # magnetic field in the same units as E (c = 1)
    g = 1 / np.sqrt(1 - b @ b); bh = b / np.linalg.norm(b)
    Ep = g * (E + np.cross(b, Bn)) - (g - 1) * (E @ bh) * bh
    Bp = g * (Bn - np.cross(b, E)) - (g - 1) * (Bn @ bh) * bh
    return Ep, Bp / EB


if __name__ == '__main__':
    rng = np.random.default_rng(1)
    for _ in range(3):
        p1 = rng.normal(0, 300, 3); p2 = rng.normal(0, 300, 3); m = 500.0
        b = pair_beta(p1, p2, m)
        E0, B0 = to_cm(np.zeros(3), np.array([0, 0, 3.8112]), b)
        El, Bl = bstar_off_fields(p1, p2, m)
        E1, B1 = to_cm(El, Bl, b)
        n0 = rng.normal(size=3); n0 /= np.linalg.norm(n0)
        El2, Bl2 = eperp_only_fields(p1, p2, m, n0)
        E2, B2 = to_cm(El2, Bl2, b)
        print(f"   E_perp-only: |E*.n0| = {abs(E2 @ n0):.2e}, |E*_perp - target| = {np.linalg.norm(E2 - (E0 - (E0 @ n0) * n0)):.2e}, |B*| = {np.linalg.norm(B2):.2e} T")
        print(f"|E*| full {np.linalg.norm(E0):.6e}, B*-off {np.linalg.norm(E1):.6e}, |E*_off - E*_full| {np.linalg.norm(E1 - E0):.2e}; "
              f"|B*| full {np.linalg.norm(B0):.4f} T, B*-off {np.linalg.norm(B1):.2e} T")
