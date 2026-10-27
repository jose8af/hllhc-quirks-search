"""T1_lattice_conversions.py -- conversion table between Lambda conventions + RGE validation.

Purpose : (1) print sqrt(sigma), Tc, Lambda_MSbar, m(0++) ratios with propagated lattice errors for
          SU(2), SU(3), SU(4), SU(inf); (2) quantify the convention mismatch used in 2512.20696
          (Tc = 0.6 sqrt(sigma), m0 = 6 Tc) and 2504.02940 / 1501.05310 (m0 = 6.8 Lambda_MS, sigma = 3.6 L'^2);
          (3) validate the Lambda_MSbar machinery in T1_common against S.P. Martin 1012.2072 Table I.
Inputs  : T1_common.LAT (lattice values with refs).
Run     : cd theory_track && pixi run python code/T1_lattice_conversions.py
"""
import numpy as np
from T1_common import (LAT, tc_over_sqrtsig, m0_over_sqrtsig, lamms_over_sqrtsig, ym_coeffs,
                       lambda_ms)

print("=== Lattice conversion table (pure SU(N) YM), errors propagated in quadrature ===")
print(f"{'N':>4} {'Tc/sqs':>14} {'m0/sqs':>14} {'LMS/sqs':>18} {'m0/Tc':>12} {'m0/LMS':>12} {'Tc/LMS':>12}")
for N in (2, 3, 4):
    (tc, dtc), (m0, dm0), (lm, dls, dly) = LAT[N]
    dlm = np.hypot(dls, dly)
    r1, r2, r3 = m0 / tc, m0 / lm, tc / lm
    e1 = r1 * np.hypot(dm0 / m0, dtc / tc)
    e2 = r2 * np.hypot(dm0 / m0, dlm / lm)
    e3 = r3 * np.hypot(dtc / tc, dlm / lm)
    print(f"{N:>4} {tc:7.4f}({dtc:.4f}) {m0:7.3f}({dm0:.3f}) {lm:7.4f}({dlm:.4f}) {r1:6.2f}({e1:.2f}) {r2:6.2f}({e2:.2f}) {r3:6.2f}({e3:.2f})")
tc, m0, lm = 0.5949, 3.072, 0.5055
print(f"{'inf':>4} {tc:7.4f}(0.0017) {m0:7.3f}(0.014) {lm:7.4f}(0.0250) {m0/tc:6.2f}       {m0/lm:6.2f}       {tc/lm:6.2f}")

print("\n=== Convention mismatches in the quirk literature ===")
for N in (2, 3):
    tcr = tc_over_sqrtsig(N)
    print(f"SU({N}): 2512.20696 uses Tc/sqs=0.6 -> their 'Lambda=1 keV' = {1/0.6:.2f} keV sqs (as quoted in theory_signal_model.md);"
          f" lattice SU({N}) gives {1/tcr:.2f} keV sqs  (difference {100*(0.6/tcr-1):+.0f}% in Lambda)")
    print(f"        2512.20696 m0 = 6 Tc  vs lattice m0/Tc = {m0_over_sqrtsig(N)/tcr:.2f}  ({100*(6*tcr/m0_over_sqrtsig(N)-1):+.0f}% in m0)")
    print(f"        1501.05310/2504.02940 m0 = 6.8 L_MS vs lattice m0/L_MS = {m0_over_sqrtsig(N)/lamms_over_sqrtsig(N):.2f};"
          f" sigma = 3.6 L'^2 => sqs/L' = 1.90 vs lattice sqs/L_MS = {1/lamms_over_sqrtsig(N):.2f}")
print("Kang-Luty 0805.4642 Sec.5.7: m0 = 3.6 sqs (lattice SU(2) 3.78, SU(3) 3.41, SU(inf) 3.07)")

print("\n=== Validation of Lambda_MSbar code vs S.P. Martin 1012.2072 Table I (Q0 = 1 TeV, pure YM below) ===")
martin = {(2, 2): (19.5, 280e-6, 250e-6), (2, 3): (24.5, 4.1e-6, 3.7e-6), (2, 4): (29.5, 60e-9, 55e-9),
          (3, 8): (30.2, 160e-6, 140e-6), (3, 9): (35.2, 9.7e-6, 8.8e-6)}
for (N, ns), (ainv, l2, l3) in martin.items():
    L2 = lambda_ms(1 / ainv, 1000.0, ym_coeffs(N, loops=2))
    L3 = lambda_ms(1 / ainv, 1000.0, ym_coeffs(N, loops=3))
    L1 = 1000.0 * np.exp(-2 * np.pi * ainv / (11 * N / 3))
    print(f"SU({N}) nS={ns}: 1/alpha(1TeV)={ainv}: L1={L1*1e6:.3g} keV, L2={L2*1e6:.3g} keV (Martin {l2*1e6:.3g}),"
          f" L3={L3*1e6:.3g} keV (Martin {l3*1e6:.3g});  sqs = L3/{lamms_over_sqrtsig(N):.3f} = {L3/lamms_over_sqrtsig(N)*1e6:.3g} keV")
