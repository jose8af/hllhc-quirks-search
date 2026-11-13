"""T1_cosmo.py -- cosmology of the infracolor sector for the CMS mesoscopic window.

Purpose : independent re-derivation / check of 2512.20696 (Asadi-Kribs-Luty) for the E quirk:
  1. 0++ glueball lifetime  [2512.20696 Eq.4-5]
  2. thermal history (dark sector once in equilibrium with the SM): decoupling T, Delta N_eff (BBN, CMB),
     glueball relic Omega h^2 (instant-confinement and cannibal estimates), required dilution
  3. UV freeze-in (gamma gamma -> g'g' through the dim-8 operator) for T_RH << m_Q
     [2512.20696 Eq.19, 31-34]: T_RH,max(m_Q, Lambda) from overclosure and from a self-interacting
     sub-component limit f < f_max; scaling of Omega with T_RH.
  4. SIDM cross section [2512.20696 Eq.11].
Convention: Lambda = sqrt(sigma) (collider) unless stated; Tc and m0 from lattice (T1_common).
Quirk: E = (1,1)_{-1} Dirac, tr Q^2 = 1, N_IC = 2 (also 3).
Run     : cd theory_track && pixi run python code/T1_cosmo.py   (writes code/T1_cosmo_grid.npz)
"""
import numpy as np
from scipy.optimize import brentq
from scipy.special import zeta
from T1_common import (MPL, ALPHA_EM, HBAR_S, OMEGA_COEF, OMEGA_DM, GEV_TO_G, GEV2_TO_CM2, gstar,
                       tc_over_sqrtsig, m0_over_sqrtsig, lamms_over_sqrtsig, ym_coeffs, run_alpha,
                       alpha_from_lambda, beta_coeffs)

TRQ2 = 1.0


def glue(N, lam):
    """lam = sqrt(sigma) [GeV] -> (Tc, m0, g_dark)"""
    return tc_over_sqrtsig(N) * lam, m0_over_sqrtsig(N) * lam, 2 * (N * N - 1)


def alpha_ic(N, lam, mu):
    """IC coupling at mu > m_Q-threshold region (pure YM below m_Q, 3-loop): alpha(mu) from Lambda_MS."""
    return alpha_from_lambda(lam * lamms_over_sqrtsig(N), mu, ym_coeffs(N, 3))


def tau_glueball(N, lam, mQ, alpha=ALPHA_EM):
    """2512.20696 Eq.4-5 with alpha_2 -> alpha tr Q^2 (photons only); alpha_dark cancels."""
    m = m0_over_sqrtsig(N) * lam
    G = 9 * (alpha * TRQ2) ** 2 * m**9 / (16 * np.pi**2 * 57600 * np.pi * mQ**8)
    return HBAR_S / G


def inv_M8(N, lam, mQ, alpha=ALPHA_EM):
    """1/M^8 with 1/M^4 = e^2 g'^2 trQ^2 / (60 (4pi)^2 mQ^4)  [2512.20696 Eq.19]; g' at m_Q."""
    ad = alpha_ic(N, lam, mQ)
    invM4 = (4 * np.pi * alpha) * (4 * np.pi * ad) * TRQ2 / (60 * (4 * np.pi) ** 2 * mQ**4)
    return invM4**2


def freezein_Z(N, lam, mQ, TRH):
    """rho_dark/rho_gamma after freeze-in [2512.20696 Eq.34, x_f -> 0]."""
    return 167 * (N * N - 1) * MPL * TRH**7 / (7 * np.sqrt(gstar(TRH))) * inv_M8(N, lam, mQ)


def x_cannibal(N, lam, r):
    """3->2 freeze-out x_f = m0/T_dark for a glueball gas with dark/SM entropy ratio r.
    <sigma_32 v^2> ~ (4pi)^3/(N^6 m^5) (NDA, Forestell et al. scaling as quoted via 2512.20696 Eq.11; UNVERIFIED)."""
    m = m0_over_sqrtsig(N) * lam
    s32 = (4 * np.pi) ** 3 / (N**6 * m**5)
    def sd_of_x(x):            # dark entropy density in chemical equilibrium (mu=0), g=1
        Td = m / x
        n = (m * Td / (2 * np.pi)) ** 1.5 * np.exp(-x)
        return n * (x + 2.5), n
    def resid(x):
        sd, n = sd_of_x(x)
        ssm = sd / r                      # SM entropy at that moment
        # invert s_SM = 2pi^2/45 g T^3 (iterate g)
        T = (ssm / (2 * np.pi**2 / 45 * 3.91)) ** (1 / 3)
        for _ in range(5):
            T = (ssm / (2 * np.pi**2 / 45 * gstar(T))) ** (1 / 3)
        H = 1.66 * np.sqrt(gstar(T)) * T**2 / MPL
        return np.log(n**2 * s32 / H)
    return brentq(resid, 1.5, 200.)


def omega_from_r(N, lam, r, mode="instant"):
    """Glueball Omega h^2 for dark/SM entropy ratio r."""
    Tc, m, gd = glue(N, lam)
    if mode == "instant":            # 2512.20696 central: radiation until Tdark=Tc then matter
        n_over_sd = 0.75 * Tc / m
    else:                            # adiabatic cannibal evolution, 3->2 freeze-out
        n_over_sd = 1 / (x_cannibal(N, lam, r) + 2.5)
    return OMEGA_COEF * m * r * n_over_sd


def r_freezein(N, lam, mQ, TRH):
    Z = freezein_Z(N, lam, mQ, TRH)
    gd = 2 * (N * N - 1)
    rho_d = Z * np.pi**2 / 15 * TRH**4
    Td = (30 * rho_d / (np.pi**2 * gd)) ** 0.25
    return gd * Td**3 / (gstar(TRH) * TRH**3), Td / TRH, Z


def trh_max(N, lam, mQ, fmax=1.0, mode="instant"):
    f = lambda lt: np.log(omega_from_r(N, lam, r_freezein(N, lam, mQ, 10**lt)[0], mode) / (fmax * OMEGA_DM))
    try:
        return 10 ** brentq(f, -3, 4)
    except ValueError:
        return np.nan


def t_dec_thermal(N, lam, mQ):
    """Decoupling of the dark sector from the SM once in equilibrium: min over (i) dim-8 gamma gamma<->g'g'
    and (ii) on-shell quirk exchange gamma gamma, f fbar <-> Q Qbar <-> g'g' (sigma v ~ 10 pi alpha^2/m_Q^2)."""
    gd = 2 * (N * N - 1)
    iM8 = inv_M8(N, lam, mQ)
    def r_dim8(T):
        C = 288 * np.pi * zeta(7) / 5 * (N * N - 1) * T**13 * iM8
        return np.log(C / (gd * np.pi**2 / 30 * T**4) / (1.66 * np.sqrt(gstar(T)) * T**2 / MPL))
    def r_onshell(T):
        nQ = 4 * N * (mQ * T / (2 * np.pi)) ** 1.5 * np.exp(-mQ / T)
        C = 2 * mQ * nQ**2 * 10 * np.pi * ALPHA_EM**2 / mQ**2
        return np.log(C / (gd * np.pi**2 / 30 * T**4) / (1.66 * np.sqrt(gstar(T)) * T**2 / MPL))
    T1 = 10 ** brentq(lambda lt: r_dim8(10**lt), -3, 5)
    T2 = 10 ** brentq(lambda lt: r_onshell(10**lt), np.log10(mQ / 60), np.log10(mQ / 3))
    return min(T1, T2), T1, T2


if __name__ == "__main__":
    print("=== 1. 0++ glueball lifetime (E quirk, photons only) ===")
    for N in (2, 3):
        for mQ in (200., 500., 1000.):
            s = ", ".join(f"L={l*1e6:g}keV: {tau_glueball(N, l, mQ):.1e}s" for l in (0.1e-6, 1e-6, 15e-6, 100e-6))
            print(f"  SU({N}) m_Q={mQ:.0f}: {s}")
    for N in (2,):
        for mQ in (500., 1000.):
            lam_age = brentq(lambda l: np.log(tau_glueball(N, 10**l, mQ) / 4.35e17), -9, 3)
            lam_1s = brentq(lambda l: np.log(tau_glueball(N, 10**l, mQ) / 1.0), -9, 3)
            print(f"  SU({N}) m_Q={mQ:.0f}: tau = age of Universe at sqs = {10**lam_age*1e3:.3g} MeV; tau = 1 s at sqs = {10**lam_1s:.3g} GeV")

    print("\n=== 2. Thermal history (dark sector once in equilibrium with the SM) ===")
    for N in (2, 3):
        gd = 2 * (N * N - 1)
        for mQ in (200., 500., 1000.):
            Td, T1, T2 = t_dec_thermal(N, 1e-6, mQ)
            gs = gstar(Td)
            r = gd / gs
            dNbbn = 4 / 7 * gd * (10.75 / gs) ** (4 / 3)
            print(f"  SU({N}) m_Q={mQ:.0f}: T_dec(dim8)={T1:.1f} GeV, T_dec(on-shell quirks)={T2:.1f} GeV -> T_dec={Td:.1f}, "
                  f"g*s={gs:.1f}; DeltaNeff(BBN; and CMB if still deconfined)={dNbbn:.3f}")
            om = [(l, omega_from_r(N, l, r, 'instant'), omega_from_r(N, l, r, 'cannibal')) for l in (0.1e-6, 1e-6, 15e-6, 100e-6)]
            print("        Omega_G h^2 [instant | cannibal]: " + "; ".join(f"L={l*1e6:g}keV: {a:.2g} | {b:.2g}" for l, a, b in om))
            if mQ == 500.:
                # Lambda where thermal Omega h^2 = 0.12
                for mode in ("instant", "cannibal"):
                    l0 = 10 ** brentq(lambda ll: np.log(omega_from_r(N, 10**ll, r, mode) / 0.12), -12, -3)
                    print(f"        thermal Omega h^2 = 0.12 at sqs = {l0*1e9:.3g} eV ({mode});  x_f(1 keV) = {x_cannibal(N, 1e-6, r):.1f}")
                # dark confinement temperature (SM) for Lambda = 1 keV, after e+e- (g*s=3.91)
                xi = (r * 3.91 / gd) ** (1 / 3)
                print(f"        xi = Tdark/T after e+e- = {xi:.3f}; dark confinement at T_SM = Tc/xi = {tc_over_sqrtsig(N)*1e-6/xi*1e6:.2f} keV (for sqs=1 keV): after BBN, before CMB")
                print(f"        required dilution D = Omega/0.12 at 0.6/1/15 keV (instant): "
                      + ", ".join(f"{omega_from_r(N, l, r, 'instant')/0.12:.0f}" for l in (0.6e-6, 1e-6, 15e-6)))
    print("  Planck18 N_eff = 2.99 +0.34-0.33 (95%); ACT DR6 P-ACT-LB 2.86 +- 0.13; BBN 2.895 +- 0.142 [2512.20696 fn.5];"
          " SO sigma ~0.05-0.07, CMB-S4 sigma ~0.03 (UNVERIFIED survey numbers)")
    # invisible decays: entropy of dark sector converted into massless phi (g=1) -> CMB Delta Neff
    for N in (2, 3):
        gd = 2 * (N * N - 1)
        dN = 4 / 7 * gd * (10.75 / 86.25) ** (4 / 3)
        print(f"  SU({N}) thermal + glueballs -> invisible massless scalar (g=1): Delta N_eff(CMB) = {dN*(gd/1)**(1/3):.2f}")

    print("\n=== 3. UV freeze-in, T_RH < m_Q/25 ===")
    for N in (2, 3):
        for mQ in (200., 600., 1000.):
            for lam in (1e-6 / 0.6 * tc_over_sqrtsig(N) * 0 + 1e-6, 15e-6):
                r, xi, Z = r_freezein(N, lam, mQ, 10.)
                t_i = trh_max(N, lam, mQ, 1.0, 'instant')
                t_c = trh_max(N, lam, mQ, 1.0, 'cannibal')
                t_s = trh_max(N, lam, mQ, 0.025, 'instant')
                print(f"  SU({N}) m_Q={mQ:.0f} sqs={lam*1e6:g} keV (Tc={tc_over_sqrtsig(N)*lam*1e6:.2f} keV): T_RH,max = {t_i:.3g} GeV (overclosure, instant),"
                      f" {t_c:.3g} (cannibal), {t_s:.3g} (f<0.025 SIDM-like); m_Q/25 = {mQ/25:.0f}")
    # scaling exponent
    N, lam, mQ = 2, 1e-6, 600.
    o1 = omega_from_r(N, lam, r_freezein(N, lam, mQ, 5.)[0])
    o2 = omega_from_r(N, lam, r_freezein(N, lam, mQ, 10.)[0])
    print(f"  scaling: Omega ∝ T_RH^{np.log(o2/o1)/np.log(2):.2f} (2512.20696 Sec.4.2 states T_RH^7);"
          f" factor-100 abundance uncertainty -> T_RH factor {100**(1/np.log2(o2/o1)):.2f} (paper: <=2)")
    # check vs 2512.20696 Fig.4 (m_Q=600 GeV, their Lambda = Tc = 1 keV): read-off yellow ~ 13 GeV, red ~ 7 GeV
    lam_c = 1e-6 / tc_over_sqrtsig(2)
    print(f"  check vs 2512.20696 Fig.4 (m_Q=600, Tc=1 keV, read-off: overclosure ~13 GeV, SIDM ~7 GeV): "
          f"mine {trh_max(2, lam_c, 600., 1.0):.3g} GeV (overclosure), {trh_max(2, lam_c, 600., 0.025):.3g} (f<0.025)")
    r, xi, Z = r_freezein(2, 1e-6, 500., trh_max(2, 1e-6, 500.))
    print(f"  at the bound (SU2, 500 GeV, 1 keV): Z=rho_d/rho_gamma={Z:.2e}, xi={xi:.2f}, Delta N_eff(BBN)={3.43*(xi*(10.75/gstar(10.))**(1/3))**4:.1e}")
    # thermalisation of the frozen-in gluons: Gamma(2->3) ~ alpha_d^2 n_g/E^2 vs H
    TRH = trh_max(2, 1e-6, 500.)
    ad = alpha_ic(2, 1e-6, TRH)
    ng = Z * np.pi**2 / 15 * TRH**4 / (3 * TRH)
    print(f"  self-thermalisation of frozen-in gluons at T_RH: Gamma/H ~ {ad**2*ng/(3*TRH)**2/(1.66*np.sqrt(gstar(TRH))*TRH**2/MPL):.1e}")

    print("\n=== 4. SIDM ===")
    for N in (2, 3):
        for lam in (1e-6, 15e-6):
            m = m0_over_sqrtsig(N) * lam
            som = (4 * np.pi) ** 3 / (N**4 * m**2) / m   # GeV^-3
            print(f"  SU({N}) sqs={lam*1e6:g} keV: sigma/m ~ {som*GEV2_TO_CM2/GEV_TO_G:.1e} cm^2/g")

    # grid for the figure
    lams = np.logspace(-7.5, -3.0, 46)        # 30 eV .. 1 MeV sqrt(sigma)
    mqs = np.logspace(np.log10(150.), np.log10(3000.), 30)
    out = {}
    for N in (2, 3):
        for key, fm, mode in (("oc", 1.0, "instant"), ("sidm", 0.025, "instant"), ("can", 1.0, "cannibal")):
            g = np.array([[trh_max(N, l, m, fm, mode) for l in lams] for m in mqs])
            out[f"N{N}_{key}"] = g
        r_th = np.array([[2 * (N * N - 1) / gstar(t_dec_thermal(N, l, m)[0]) for l in lams] for m in mqs])
        out[f"N{N}_omth"] = np.array([[omega_from_r(N, l, r_th[i, j]) for j, l in enumerate(lams)] for i in range(len(mqs))])
        out[f"N{N}_tau"] = np.array([[tau_glueball(N, l, m) for l in lams] for m in mqs])
    np.savez("code/T1_cosmo_grid.npz", lams=lams, mqs=mqs, **out)
    print("\nsaved code/T1_cosmo_grid.npz")
