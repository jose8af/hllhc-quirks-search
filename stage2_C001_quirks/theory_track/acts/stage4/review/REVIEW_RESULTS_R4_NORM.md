# REVIEW_RESULTS_R4_NORM: verification of FIX R3-NORM (fresh reviewer, 2026-10-16)

Verdict: **PASS** (A = 0, B = 0, C = 3)

Checks
1. Independent recomputation (own script, xsec.json f_pt200_TRG_over_INC x sigma_norm_nic2_fb x 3000 fb^-1 x acceptance.json A_trig_presel; mu95 = limits.json expected_primary):
   E200 1.5 keV: f 0.04764, N_exp 1.5775e4, mu95/N_exp 789.7 (best, = 790). E500 3 keV: f 0.1042, N_exp 1090, ratio 1.327e4. E1000 3 keV 3.78e5, E1500 3 keV 3.83e6, S500 3 keV (f 0.1135, sigma 0.458 fb) N_exp 85.7, ratio 2.77e5. All match the fix table and STAGE4_SUMMARY.json.
2. Population: make_inputs.py selects pT(QQ) > 200, |eta_pair| < 4 (p2); A includes fiducial |eta| < 2.5, trigger, presel as conditional factors, so sigma_norm (N_IC = 2, K inside sigma_norm) x f x A has no double counting and no missing factor. sigma_norm*f = 10.44 fb = xsec.json sigma_norm_pt200_nic2_fb; N(pT>200)x3 ab^-1 = 31328 > N_exp. xsec f lacks the |eta|<4 cut (<2e-4 relative): immaterial.
3. selfcheck_stage4.py: 165/165 passed (re-run).
4. STAGE4_RESULTS.md: grep finds 37.6 / 3.3e5 / 1.1e3 only inside the erratum and explicit "before" notes; no stale N_exp; erratum accurate (5.9-21 shift, conclusions unchanged: ratios all >= 790, no exclusion).
5. D5_F200, D6_L1p5, D7 PNGs read: legend N_exp = sigma_norm.f.L.A, D6 axis "inclusive sigma", annotations 7.9e2, D7 cells match table (7.9e2 best, 6.0e7 max).
6. make_figures.py: all A uses go through acceptance() which now returns A*f (lines 237-247); D5/D6/D7 are the only consumers. No other Stage-5 figure uses A.

Category C (advisory)
- C1: paper/figures D5/D6/D7 PDFs and paper text (37.6, ~43) still stale; paper fixer must re-copy/update (already flagged by the fixer).
- C2: tail-rate nuisance on f (+12..15 / -11..13 %) not propagated; negligible vs 6-21x shift.
- C3: STAGE4_SUMMARY_C12v1.json / STAGE4_RESULTS_C12v1.md (superseded) keep the old formula.
