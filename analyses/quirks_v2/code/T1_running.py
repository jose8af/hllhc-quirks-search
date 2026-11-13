"""T1_running.py -- what sets Lambda: RG running of the infracolor coupling, theory strips, priors.

Purpose :
  (A) SUSY-GUT ladder (Kang-Luty 0805.4642 Sec.2.5; S.P. Martin 1012.2072): alpha_X = alpha_GUT at M_U,
      IC-charged matter = N_IC copies of 5+5bar quirks (D, L) + nS SM-singlet IC flavours, all at an
      IC threshold ~ m_Q; pure SU(N) YM below.  Anchor: Martin's alpha_X^-1(1 TeV) (Table I).  The m_Q
      dependence is obtained by moving the IC threshold to m_Q with the SUSY 2-loop beta function
      above it (alpha_X(M_U) fixed).  Strip width: +-1.5 in alpha_X^-1(m_Q) (O(1) thresholds:
      factor-3 spread of IC-charged masses ~ (Delta b/2pi) ln 3 ~ 1.6 for SU(2); GUT thresholds).
  (B) Non-SUSY "infracolor coupling = SM coupling at M_UV" with only the quirk E (1 Dirac IC fundamental).
  (C) Flat prior in 1/g^2(M_UV): fraction landing in the mesoscopic band / CMS window.
Output  : printed tables + code/T1_running_strips.npz (used by T1_figure.py)
Run     : cd theory_track && pixi run python code/T1_running.py
"""
import numpy as np
from T1_common import (beta_coeffs, run_alpha, lambda_ms, ym_coeffs, lamms_over_sqrtsig,
                       alpha_from_lambda)

mQ = np.logspace(np.log10(100.), np.log10(3000.), 60)      # GeV
DA = 1.5                                                     # strip half-width in alpha^-1(m_Q)

def sqs_from_alpha(alpha, mu, N):
    return lambda_ms(alpha, mu, ym_coeffs(N, 3)) / lamms_over_sqrtsig(N)

# ---------------------------------------------------------------- (A) SUSY-GUT ladder
martin_ainv = {(2, 2): 19.5, (2, 3): 24.5, (2, 4): 29.5, (3, 8): 30.2, (3, 9): 35.2}
strips = {}
print("=== (A) SUSY-GUT ladder [anchor 1012.2072 Table I], Lambda = sqrt(sigma) in keV ===")
print("  N nS  b0_SUSY   m_Q=200      500     1000     2000 GeV   (central; band x/÷ from +-1.5 in 1/alpha)")
for (N, nS), ainv1 in martin_ainv.items():
    co = beta_coeffs(N, susy_pairs=5 + nS, loops=2)
    cen, lo, hi = [], [], []
    for m in mQ:
        a_m = run_alpha(1 / ainv1, 1000.0, m, co)
        cen.append(sqs_from_alpha(a_m, m, N))
        lo.append(sqs_from_alpha(1 / (1 / a_m + DA), m, N) * 0.9)   # also -10% Lambda_MS/sqs conversion
        hi.append(sqs_from_alpha(1 / (1 / a_m - DA), m, N) * 1.1)
    strips[f"susy_N{N}_nS{nS}"] = np.array([cen, lo, hi])
    sel = [np.argmin(abs(mQ - x)) for x in (200, 500, 1000, 2000)]
    print(f"  {N} {nS:2d}   {co[0]:+.0f}   " + "  ".join(f"{cen[i]*1e6:8.3g}" for i in sel)
          + f"   band factor {hi[sel[1]]/cen[sel[1]]:.1f}")
    # local slope dlnL/dlnm
    sl = np.gradient(np.log(cen), np.log(mQ))[sel[1]]
    print(f"           slope dlnLambda/dln m_Q at 500 GeV = {sl:.2f}")

# rung spacing (one extra IC flavour pair at the TeV scale, SUSY, M_U = 2e16)
for N in (2, 3):
    dainv = 1 / (2 * np.pi) * np.log(2e16 / 1e3)   # Delta b = +1 per extra flavour pair
    print(f"  rung spacing SU({N}): Delta(1/alpha)={dainv:.2f} -> Lambda factor {np.exp(2*np.pi*dainv/(11*N/3)):.0f}"
          f" ({2*np.pi*dainv/(11*N/3)/np.log(10):.2f} decades)")

# ---------------------------------------------------------------- (B) non-SUSY alpha_IC(M_UV) = alpha_SM(M_UV)
print("\n=== (B) non-SUSY, only quirk E (1 Dirac IC fundamental) above m_Q, alpha_IC(M_UV) given ===")
# SM 1-loop at M_UV (GUT-normalised alpha1); alpha^-1(MZ) = 59.0, 29.6, 8.47; b = 41/10, -19/6, -7
def sm_ainv(M):
    L = np.log(M / 91.19)
    return 59.0 - 4.1 / (2 * np.pi) * L, 29.6 + 19 / 6 / (2 * np.pi) * L, 8.47 + 7 / (2 * np.pi) * L
for MUV in (1e16, 1.2e19):
    a1, a2, a3 = sm_ainv(MUV)
    print(f"  M_UV={MUV:.1e}: SM alpha^-1 = {a1:.1f}, {a2:.1f}, {a3:.1f}")
    for N in (2, 3):
        co = beta_coeffs(N, nf_dirac=1, loops=2)
        for m in (200., 1000.):
            out = []
            for ainv in (min(a1, a2, a3), max(a1, a2, a3)):
                try:
                    a_m = run_alpha(1 / ainv, MUV, m, co)
                    out.append(sqs_from_alpha(a_m, m, N) if a_m < 2 else np.inf)
                except Exception:
                    out.append(np.inf)
            # alpha^-1(M_UV) needed for sqs = 0.1 keV, 100 keV
            need = []
            for Lt in (100e-6, 0.1e-6):
                a_m = alpha_from_lambda(Lt * lamms_over_sqrtsig(N), m, ym_coeffs(N, 3))
                need.append(1 / run_alpha(a_m, m, MUV, co))
            print(f"    SU({N}) m_Q={m:.0f}: alpha_IC^-1(M_UV) in [{min(a1,a2,a3):.0f},{max(a1,a2,a3):.0f}] -> sqs in "
                  f"[{out[0]:.2g}, {out[1]:.2g}] GeV;  band 0.1-100 keV needs alpha_IC^-1(M_UV) in [{need[0]:.1f}, {need[1]:.1f}]"
                  f"  (= {need[0]/np.mean([a1,a2]):.2f}-{need[1]/np.mean([a1,a2]):.2f} x <alpha1^-1,alpha2^-1>)")

# ---------------------------------------------------------------- (C) flat prior in 1/g^2(M_UV)
print("\n=== (C) flat prior in alpha_IC^-1(M_UV) (non-SUSY, E only, M_UV = 1e16 GeV, m_Q = 500 GeV) ===")
MUV, m = 1e16, 500.
a1, a2, a3 = sm_ainv(MUV)
aref = 0.5 * (a1 + a2)
for N in (2, 3):
    co = beta_coeffs(N, nf_dirac=1, loops=2)
    grid = np.linspace(0.3 * aref, 3.0 * aref, 3000)
    lam = []
    for ainv in grid:
        a_m = run_alpha(1 / ainv, MUV, m, co)
        lam.append(sqs_from_alpha(a_m, m, N) if (a_m > 0 and a_m < 1.5) else np.nan)
    lam = np.array(lam)
    for lo_f, hi_f in ((0.5, 2.0), (0.67, 1.5)):
        sel = (grid >= lo_f * aref) & (grid <= hi_f * aref)
        L = lam[sel]
        quirky = np.nan_to_num(L, nan=1e9) < m / 10
        band = (L > 0.1e-6) & (L < 100e-6)
        cms = (L > 0.6e-6) & (L < 15e-6)
        print(f"  SU({N}) prior alpha^-1 in [{lo_f},{hi_f}] x {aref:.1f}: P(band 0.1-100 keV)={band.mean():.3f}, "
              f"P(CMS 0.6-15 keV)={cms.mean():.3f}, P(quirky: L<m_Q/10)={quirky.mean():.2f}, "
              f"P(band|quirky)={band.sum()/max(quirky.sum(),1):.3f}")
    dl = np.gradient(np.log10(lam), grid)
    print(f"  SU({N}): d log10(Lambda)/d alpha^-1(M_UV) = {np.nanmedian(dl):.3f}  -> band = {3/abs(np.nanmedian(dl)):.1f} units of alpha^-1")

np.savez("code/T1_running_strips.npz", mQ=mQ, **strips)
print("\nsaved code/T1_running_strips.npz")
