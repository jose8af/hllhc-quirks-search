"""T1_common.py -- shared inputs for the T1 (confinement scale Lambda) investigation.

Purpose : lattice conversion factors between Lambda conventions, SU(N) running (1-3 loop),
          Lambda_MSbar definition, g*(T) table, constants.  Imported by the other T1_*.py scripts.
Inputs  : lattice numbers typed in from the primary papers (refs in comments, all opened 2026-10-07).
Run     : not standalone; `pixi run python code/T1_lattice_conversions.py` etc. (from theory_track/).
"""
import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

# ----------------------------------------------------------------------------------------------
# Lattice continuum values (pure SU(N) Yang-Mills)
#   Tc/sqrt(sigma): Lucini-Teper-Wenger hep-lat/0307017 Table 6 (SU2 0.7091(36), SU3 0.6462(30),
#                   SU(inf) 0.5960(41)); Lucini-Rago-Rinaldi 1202.6684 Eq.12: 0.5949(17)+0.458(18)/N^2
#   m(0++)/sqrt(sigma): Athenodorou-Teper 2106.00364 Tables p.83-84 (SU2 3.781(23), SU3 3.405(21),
#                   SU4 3.271(27), SU5 3.156(31), SU6 3.102(32), SU8 3.099(26)); Table 31: SU(inf) 3.072(14)
#   LambdaMSbar/sqrt(sigma) (3-loop fit): 2106.00364 Table 15: SU2 0.5806(21)[570], SU3 0.5424(13)[185],
#                   SU4 0.5222(11)[230]; Eq.20: 0.5055(7)[250] + 0.306(12)/N^2
# ----------------------------------------------------------------------------------------------
LAT = {
    # N : (Tc/sqrt(s), err), (m0/sqrt(s), err), (LamMS/sqrt(s), err_stat, err_syst)
    2: ((0.7091, 0.0036), (3.781, 0.023), (0.5806, 0.0021, 0.0570)),
    3: ((0.6462, 0.0030), (3.405, 0.021), (0.5424, 0.0013, 0.0185)),
    4: ((0.634, 0.012), (3.271, 0.027), (0.5222, 0.0011, 0.0230)),
}


def tc_over_sqrtsig(N):
    if N in LAT:
        return LAT[N][0][0]
    return 0.5949 + 0.458 / N**2          # 1202.6684 Eq.12


def m0_over_sqrtsig(N):
    if N in LAT:
        return LAT[N][1][0]
    return 3.072 + (3.781 - 3.072) * 4 / N**2   # crude 1/N^2 interpolation to SU(inf)=3.072


def lamms_over_sqrtsig(N):
    if N in LAT:
        return LAT[N][2][0]
    return 0.5055 + 0.306 / N**2           # 2106.00364 Eq.20


# ----------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------
MPL = 1.22e19          # GeV (non-reduced Planck mass, as in 2512.20696 Eq.32)
ALPHA_EM = 1 / 137.036
HBAR_S = 6.582e-25     # GeV s
GEV5_TO_ERG_CM3_S = 1.602e-3 * (5.068e13) ** 3 * 1.519e24   # 1 GeV^5 in erg cm^-3 s^-1
GEV_TO_G = 1.783e-24
GEV2_TO_CM2 = 0.3894e-27
OMEGA_COEF = 2.744e8   # Omega h^2 = 2.744e8 (m/GeV) Y   (s0 = 2891 cm^-3, rho_c/h^2 = 1.0537e-5 GeV cm^-3)
OMEGA_DM = 0.12

# g*(T) ~ g*s(T) (rough SM table, T in GeV); adequate for O(10%) work
_GT = np.array([1e-5, 1e-4, 3e-4, 1e-3, 0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 1.0, 1.5, 3.0, 5.0, 10., 50., 80., 100., 150., 200., 1e5])
_GG = np.array([3.91, 3.91, 7.0, 10.75, 10.75, 10.75, 17.25, 30.0, 61.75, 61.75, 61.75, 72.25, 75.75, 75.75, 86.25, 86.25, 88.0, 92.0, 100.0, 106.75, 106.75])


def gstar(T):
    return np.interp(np.log10(T), np.log10(_GT), _GG)


# ----------------------------------------------------------------------------------------------
# Running of an SU(N) coupling. a = alpha/(4 pi);  da/dln mu^2 = -b0 a^2 - b1 a^3 - b2 a^4
# ----------------------------------------------------------------------------------------------
def beta_coeffs(N, nf_dirac=0.0, ns_complex=0.0, susy_pairs=None, loops=2):
    """Return (b0,b1,b2) in the a=alpha/4pi normalisation.
    Non-SUSY: nf Dirac fundamentals, ns complex-scalar fundamentals (2-loop scalar term included).
    SUSY (susy_pairs=n): SU(N) SYM + n flavour pairs of (fund+antifund) chiral multiplets."""
    CA, CF, TF = N, (N * N - 1) / (2 * N), 0.5
    if susy_pairs is not None:
        n = susy_pairs
        b0 = 3 * N - n
        b1 = 6 * N**2 - 2 * N * n - 4 * CF * n
        b2 = 0.0
    else:
        b0 = 11 / 3 * CA - 4 / 3 * TF * nf_dirac - 1 / 3 * TF * ns_complex
        b1 = (34 / 3 * CA**2 - 20 / 3 * CA * TF * nf_dirac - 4 * CF * TF * nf_dirac
              - 2 / 3 * CA * TF * ns_complex - 4 * CF * TF * ns_complex)
        b2 = 2857 / 54 * CA**3 if (nf_dirac == 0 and ns_complex == 0) else 0.0
    if loops < 3:
        b2 = 0.0
    if loops < 2:
        b1 = 0.0
    return b0, b1, b2


def run_alpha(alpha0, mu0, mu1, coeffs):
    """Run alpha from mu0 to mu1 with given (b0,b1,b2)."""
    b0, b1, b2 = coeffs
    def f(t, a):  # t = ln mu^2
        return [-(b0 * a[0]**2 + b1 * a[0]**3 + b2 * a[0]**4)]
    t0, t1 = 2 * np.log(mu0), 2 * np.log(mu1)
    sol = solve_ivp(f, (t0, t1), [alpha0 / (4 * np.pi)], rtol=1e-10, atol=1e-16)
    a = sol.y[0, -1]
    return 4 * np.pi * a


def lambda_ms(alpha, mu, coeffs):
    """Lambda_MSbar from alpha(mu) with the exact-integral definition (standard convention:
    ln(mu^2/L^2) = 1/(b0 a) + (b1/b0^2) ln(b0 a) + int_0^a [-1/B + 1/(b0 x^2) - b1/(b0^2 x)] dx)."""
    b0, b1, b2 = coeffs
    a = alpha / (4 * np.pi)
    B = lambda x: b0 * x**2 + b1 * x**3 + b2 * x**4
    c = b1 / b0**2
    integ = quad(lambda x: -1 / B(x) + 1 / (b0 * x**2) - c / x, 0, a, limit=200)[0] if b1 else 0.0
    L = 1 / (b0 * a) + c * np.log(b0 * a) + integ
    return mu * np.exp(-L / 2)


def alpha_from_lambda(Lam, mu, coeffs):
    """Inverse of lambda_ms."""
    f = lambda al: np.log(lambda_ms(al, mu, coeffs) / Lam)
    return brentq(f, 1e-4, 3.0)


def ym_coeffs(N, loops=3):
    return beta_coeffs(N, loops=loops)
