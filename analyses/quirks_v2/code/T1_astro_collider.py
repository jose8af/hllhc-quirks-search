"""T1_astro_collider.py -- stellar cooling and collider-indirect probes of the infracolor sector.

Purpose : (1) energy-loss rate per unit mass from gamma gamma -> g'g' (dim-8 operator, 2512.20696 Eq.19/31)
          in the Sun, red-giant core, HB core and SN1987A; resulting lower bound on m_Q (E quirk, N_IC = 2).
          This is an UPPER estimate of the emission (blackbody photons, no plasma suppression, and for
          T <~ m0 the g'g' pair must still hadronise into glueballs of mass 3.8 sqrt(sigma)).
          (2) Z -> g'g' branching ratio and e+e- -> gamma + g'g' at LEP / Belle II (order of magnitude).
Inputs  : stellar (T, rho, eps_max) benchmarks (Raffelt-style criteria; UNVERIFIED round numbers)
Run     : cd theory_track && pixi run python code/T1_astro_collider.py
"""
import numpy as np
from scipy.special import zeta
from T1_common import ALPHA_EM, GEV5_TO_ERG_CM3_S, GEV2_TO_CM2
from T1_cosmo import inv_M8, alpha_ic

N, lam = 2, 1e-6           # SU(2), sqrt(sigma) = 1 keV (alpha_IC(m_Q) enters only quadratically)
stars = {  # name: (T [GeV], rho [g/cm^3], eps_max [erg/g/s])
    "Sun core": (1.3e-6, 150., 0.2),
    "RG core (He flash)": (8.6e-6, 2e5, 10.),
    "HB core": (8.6e-6, 1e4, 10.),
    "SN1987A": (3e-2, 3e14, 1e19),
}
print("=== (1) stellar energy loss via gamma gamma -> g'g' (upper estimate) ===")
for name, (T, rho, emax) in stars.items():
    def eps(mQ):
        Q = 288 * np.pi * zeta(7) / 5 * (N * N - 1) * T**13 * inv_M8(N, lam, mQ)   # GeV^5
        return Q * GEV5_TO_ERG_CM3_S / rho
    e100 = eps(100.)
    mbound = 100. * (e100 / emax) ** (1 / 8)
    print(f"  {name:20s}: eps(m_Q=100 GeV) = {e100:.1e} erg/g/s (limit {emax:.0e}) -> m_Q > {mbound:.2g} GeV")
print("  (Primakoff-type gamma + p -> p + g'g' in the SN core adds at most a factor of a few: n_p/n_gamma ~ 200, x alpha)")

print("\n=== (2) collider-indirect (Lambda-independent at leading order) ===")
for mQ in (100., 200., 500.):
    iM8 = inv_M8(N, lam, mQ)
    mZ = 91.19
    # Gamma(Z -> g'g') ~ |c|^2 (N^2-1) m_Z^9 / (const ~ 100 pi) with c ~ 1/M^4 (photon->Z coupling: x tan^2 theta_W ~ 0.3)
    GZ = 0.3 * (N * N - 1) * mZ**9 * iM8 / (100 * np.pi)
    # sigma(e+e- -> gamma* -> ... ) : e+e- -> gamma g'g' ~ alpha * (N^2-1) s^3 / M^8 / (1000 pi)
    for rs in (10.58, 91.19, 209.):
        s = rs**2
        sig = ALPHA_EM * (N * N - 1) * s**3 * iM8 / (1000 * np.pi) * GEV2_TO_CM2 * 1e39   # fb
        if rs == 10.58:
            sB = sig
        if rs == 209.:
            sL = sig
    print(f"  m_Q={mQ:.0f}: BR(Z->g'g') ~ {GZ/2.495:.1e};  sigma(e+e- -> gamma + g'g') ~ {sB:.1e} fb (Belle II), {sL:.1e} fb (LEP2)")
print("  Lambda enters only via (Lambda/m_Q)^n corrections, (1 keV/100 GeV)^4 = 1e-32, or the glueball lifetime (>> age of Universe).")
