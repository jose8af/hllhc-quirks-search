# REVIEW_PAPER_A_R1: critical review of `paper/quirks_p1p2_note.pdf` (Phase-A sections)

Reviewer: fresh critical reviewer (JFC loop), 2026-10-16.
Scope: Phase-A sections only. These are the abstract (P1 part), Sec. 1–6, Sec. 9.1, Sec. 11, Sec. 12 (drafted items), and
App. A–C. The red P2 TODOs (results, limits, conclusions, Sec. 7/8/9.2–9.3/10/13) were not reviewed. The concise length
(31 pp now, 25–35 pp target) is a user decision and overrides the JFC 50–100 pp rule.
Method: read the methodology (critical_reviewer.md, 03-review.md, 04-output.md) and every in-scope `.tex` file. Grepped
the stage reports. Checked 12 + 10 bib entries against the INSPIRE API. Checked the equations by hand and the log-normal
constants numerically. Rendered PDF pages 7, 12, 13, 14 and 23.

## Verdict: **ITERATE** (1 A, 15 B, 11 C)

One Category-A item blocks: A-1, an undisclosed failed pre-declared validation gate in P1. It also causes an internal
inconsistency in the population-c uncertainty. It costs about three sentences to fix. Everything else is advisory. The
physics derivations are correct (§1 below). Number fidelity is very good: about 95 values were checked and two stale or
mixed ranges were found (B-6, B-7). The credit to prior work follows the novelty audit almost completely (§3).

---

## 1. What was verified (evidence)

**Equations (hand-checked):**
- Eq. 1 ℓ_max = 2(γ*−1)ℓ₀ and T_h = 2p*/σ: energy and impulse balance hold.
- σ = 50.68 GeV/cm (Λ/keV)²: correct. ℓ₀ = 1.97 cm at 100 GeV, 1 keV: correct.
- ε_B = 2.254×10⁻⁴ (0.2998 GeV T⁻¹ m⁻¹ × 3.8112 T / σ): correct.
- N_osc = σR/(2β*p_T) follows from the lab-dilated period 4γ_cm p*/σ with β_T γ_cm = p_T/(2γ* m_Q): correct.
- Eq. 5 b_odd: the NR limit is (4/3)q|E*⊥|m_Q β*²/σ². b_odd/(ε⊥ℓ_max) at γ* = 2 is 1.2397, which matches Tab. 3 (1.240).
- Eq. 6: the y(s,x) = (b/2)artanh(x/s)/artanh v solution satisfies y_tt = y_xx and the boundary conditions. The endpoint
  transverse force σ(y_x + v y_s) = σb/(2|s| artanh v) is correct.
- Δp⊥ integral → (σb/artanh β*)ln(L/b). Then ϑ = Δp⊥/p* reproduces G(γ*) of Eq. 7: G → 4/3 (NR) and G(2) = 1.087.
- Eq. 8: K(1) = 3 ln 2 − 2 = 0.0794.
- Eq. 9: C. The ln(ℓ_max/b_odd) expansion with ε⊥ = ε_B γ_cm β_T sin α (B ∥ z) reproduces the stated C.
- c = 1/L.
- Eq. 10: the exponents 1−c and −2+2c, and R(f) = 1 + c ln(1/f), which is exact for the law.
  1 + 0.104 ln 2 = 1.072 and ln 1.455/ln 80 = 0.914 (Tab. 3).
- Charge law q[1 − ln q/L] = 1.856 for q = 2.
- J = b p* at a crossing. J is maximal at odd crossings: the first half-period accumulates and the second returns.
- Rule constants: the 84th-percentile ratio of the sum of two i.i.d. log-normals at σ_ln = 2.3 is 2.710 (MC, 4×10⁶;
  pixi python), so 0.3/2.71 = 0.11. The 1.14/M bound is −ln 0.32 = 1.139.
- Fallback width admissibility Λ ≥ Λ_R·2^{(k+1)/2} ⇔ median ℓ_max ≲ R_IT/2^{k+1} ≈ W_c/2^k: consistent.

**Numbers spot-checked against the sources (all match unless listed in B-6/B-7):**
- Tab. 1 (7 rows: K, σ_norm, f₂₀₀, N₂₀₀) vs `sim/VALIDATION.md` l.118–131. Scalar σ_norm 19.2/0.458/0.0118. FeynRules
  +0.12/−0.11 %. xqcut 30/qCut 45. 47 points, 2.41 M. 107 weights. −0.36…+0.15 %. +4 %, +5–15 %. +12…+15/−11…−13 %.
  LO+PS 9–10 %. −26/−13/−8 %. QED −1.1 ± 0.8 % (LOG l.133 user decision).
- Stage 1 (`NEAR_MISS_IMPULSE.md`): 2.254e-4, 3.5 µm, G values, K values and the K fit, 3 ln 2−2, the 1.03–1.88 factor,
  C = 0.43/1.23/1.62, 33.5/31.1/29.5 µm, 0.944 vs 0.911, Tab. 2 (all 18 cells), 84–97 %/66 %, 16 %/7 %, −7…−21 %,
  +17…+36 %, 5/29/43 %, 3×10⁻⁸, 26 keV, 3–8 % at 30 keV, 1.86, 1.39 vs 1.23, 0.75 ± 0.08, 0.96 ± 0.10, 0.50.
- `NUMERICS.md`: 0.105 ± 0.002, 0.911 ± 0.003, R(f) numerics, 0.0791, b_odd 1.328/1.189, 0.6–2 %/1–2 %.
- Stage 3 (`README.md`, `VALIDATION.md`): all 15 rows × 9 columns of Tab. 4 match the README results table exactly.
  Also checked: 218 571 events/4576 jobs, 224/225 and 4.4 µm, ≤3.4 %/≤5.3 %, ±1.5 %/±2.4 %, 3.9–5.9σ, +57 ± 11 %,
  +6.22 ± 0.45 %, +1.8 ± 0.7 vs +9.7 ± 1.3 (5.5σ), +8.6 ± 4.2 %, +12 ± 3 %, 1.016/1.027, Δs_MS ranges, 0.36–0.62,
  χ² 26.0/10, 0.517, Λ_cross 1.91/1.50/1.25/1.16/1.59, 0.80–0.97, and the material x/X₀ (`T3_causal_s3.py`).
- U-2 panel (`U2_PANEL.md`): 1.25–1.73 and 0.62–1.00.
- Truth P2 handles: slopes −1.985…−2.022, 38.5/9.3/0.37 mm/95 µm, edges 0.28–0.33/0.43→0.78/0.59→0.94/0.47–0.55/
  12.8→20.4/17.7→25 keV, 38.2, 0.249 ± 0.019, R_IT = 146.5 mm.
- Stage 4 (`plan.md`, `WP_RULE.md`, `G1_REPORT.md`, `STAGE4_RESULTS.md`): 1.33×10⁵ hits, density ratios, σ_inel
  78.9 mb, σ_z/σ_t/σ_xy, Tab. 5 pitches and resolutions, 23–60 → 1.6–3.4 s, Highland 0.93, pMin 30 MeV, 0/208, PV
  (10, 15) µm/93 %, MET 25 GeV, trigger erf, preselection, δ₉₅ = 0.15 (0.130–0.149), W_c = 75 mm, t_tol = 30 µm, 2 mrad,
  ladder (23 rungs, all thresholds), rule, fallback, 5000 toys, 2295 jobs/382 CPU-h, 0.14 %.
- Open Data (`STAGE6_FEASIBILITY.md`): datasets, 1–2 weeks/3–5 weeks, and the policy caveat.

**Bibliography: INSPIRE API spot-check of 22 entries, all real and correctly identified (title, authors, journal, DOI).**
The entries checked were 0805.4642, 0810.3948, 1106.2569 (via audit), 2002.07503, 1708.02243, 2607.26195, 1008.3547,
2601.09023, 1911.02223, 2108.06748, 1811.08903, 2512.20696, 2509.08878, 0805.4667, 1012.2072, 2410.00269, 2106.13593,
and recids 2959 (Highland), 433985 (Petrov–Sharov), 120202 (BKNC), 1614103 (Tracker TDR), 7382 (Artru) and 152636
(Okun). The external claims also match the INSPIRE abstracts: D0 107 GeV for Λ = 10 keV–1 MeV, FASER 300 eV < Λ < 100 keV,
and Farina–Low 1–100 eV. Rendering problems are in B-11.

---

## 2. Findings

### Category A (must fix before PASS)

**A-1. P1: a failed pre-declared c-law validation gate is not disclosed, and the population-c uncertainty is
internally inconsistent.** The affected places are the abstract (00_abstract.tex l.13–16), Sec. 3.7
(03_string_dynamics.tex l.205 and l.209), Sec. 4.2 (04_truth_p1.tex l.36–37) and Sec. 4.4 (l.145–147).

- **Evidence.** `sim/stage3/VALIDATION.md` l.41 has gate V2b, "|Δc| ≤ 2σ and ≤ 1.5 % at all 5 points" at 1 keV.
  - The results are F_m200 +0.70 %, F_m500 **+2.00 %**, F_m1000 +1.07 %, F_m1500 **+2.10 %** and S_m500 **+3.15 %**.
  - The verdict is "**FAIL** (finding; user decision §7 of VALIDATION_GATE)".
  - The V2b revisit gives a population-median excess of +1.71 ± 0.29 % at 1–2 keV. It is read as a per-event-scatter
    estimator effect, and that reading is an ESTIMATE (VALIDATION §8 item 2, README §4).
  - R(1/2) = 1.0737 ± 0.0007 is 2.4σ above the predicted 1.072 (README l.63).
- **Problems in the note.**
  1. The abstract says that c ≃ 0.104 is "confirmed … by a 2.2×10⁵-event truth-level propagation". Tab. 4 of the same
     note shows 0.1064 ± 0.0009 against 0.1043 (+2.0 %, 2.2σ) at exactly that point.
  2. Sec. 3.7 l.205 says "the population-level uncertainty on c is taken from the empirical 1 keV agreement (≤ 1.5 %)".
     l.209 says "population c to 1–2 %". The Stage-3 production measures +2.0/+2.1/+3.2 % at 1 keV. Three different
     statements cover one quantity.
  3. Sec. 4.2 quotes only the per-event conditional median (±1.5 %, which is correct). It never mentions the population
     median, the failed gate, or the estimator-effect reading.
- **Why this is A.** A pre-declared validation test that failed is presented as a confirmation. This is the "passes:false
  in machine output while text claims acceptable" case of 03-review §6.4. The c law is the headline P1 result.
- **Fix (text only, no rerun).**
  - In Sec. 4.2, add one sentence: "The population median of the measured c lies +1.71 ± 0.29 % above the prediction
    at 1–2 keV (+2.0/+2.1/+3.2 % at E 500/E 1500/Ẽ 500 at 1 keV, a literal failure of the pre-declared ≤ 1.5 % gate).
    A zero-median symmetric per-event scatter reproduces it (+2.04 %), so we read it as an estimator effect (EST)."
  - Reconcile Sec. 3.7 so that the Stage-1 numerics agree to ≤ 1.5 % and the Stage-3 population agrees to +2–3 % (EST
    reading).
  - In the abstract, change "confirmed … by a … propagation" to "confirmed by blind numerics (0.105 ± 0.002); the
    2.2×10⁵-event propagation reproduces it per event within 1.5 % (population median +2 %, EST: estimator effect)".

### Category B (advisory; should be fixed in Phase B)

**B-1. Wrong oscillation scale at the low end of the window.**
- **Where.** Abstract l.5 and introduction l.13–14: "for Λ ∼ 0.1–100 keV the pair oscillates on micrometre-to-centimetre
  scales".
- **Problem.** At Λ = 0.1 keV, ℓ_max = 2(γ*−1)ℓ₀ ≈ 2(0.23)(985 cm) ≈ 4.5 m (m_Q = 500 GeV, median γ* = 1.23). The
  micrometre–centimetre range corresponds to Λ ≈ 1–100 keV.
- **Inconsistency.** The note itself puts the lower end of the coplanar regime at ≈ 0.3 keV (Sec. 2.1, N_osc = 1 at
  0.28–0.33 keV). The intro also says "Λ ≲ 100 eV ⇒ two separate tracks".
- **Fix.** Write "micrometres to metres". Alternatively, quote ℓ_max for 0.3/1/10/100 keV once.

**B-2. Dimensional slip in the heuristic derivation.**
- **Where.** 03_string_dynamics.tex l.117–118: "the total out-of-plane displacement is ∼ qBR G[…]/p*, a bending angle of
  momentum p* over R".
- **Problem.** qBR/p* is an angle, not a displacement. The displacement is that angle times the lever arm ∼ ℓ₀. This
  gives ε_B R/(γ*β*) × G L, which is the prefactor qBR/σ of Eq. 9.
- **Fix.** Write "the accumulated tilt is ∼ qBR G[…]/p* (a bending angle of momentum p* over R), and the out-of-plane
  displacement is this tilt times ℓ₀ ∝ m_Q/σ, i.e. ∝ ε_B R".

**B-3. Selective reporting of the Λ-exponent tests.**
- **Where.** 04_truth_p1.tex l.40–42.
- **Problem.** The note reports only the 0.6→1 keV deviations (3.9–5.9σ) and says the exponents "agree … asymptotically".
  README l.70–72 also lists 1→2 keV at 4.1σ/4.5σ (E 1500/Ẽ 500) and 1→3 keV at 3.0/3.4/3.9σ (E 1000/E 1500/Ẽ 500).
  E8 had wrongly called these "within 0.03, VERIFIED".
- **Fix.** Add these numbers and tie them to ℓ_max/R_IT ≈ 0.5–0.6. Otherwise the validity window "ℓ_max/R_IT ≲ 0.6"
  looks cleaner than it is at its edge.

**B-4. A stale statistical-validation claim.**
- **Where.** 06_strategy_wp.tex l.135–136: "the in-house implementation agrees with pyhf to 10⁻⁴".
- **Problem.** This comes from the dry run (LOG l.255, asymptotic CLs). STAGE4_RESULTS l.731/l.799 later found the
  in-house asymptotic CLs off by ×2.7×10⁻⁴ at FB0/FB1, from a saturated-NLL offset that was fixed in R6. The pyhf
  agreement therefore predates a bug in the same code path, and it is not shown to hold after the fix.
- **Fix.** Restrict the claim to "(dry run, before fix R6)". Better, redo the pyhf comparison post-R6 on two fallback
  points (≪ 1 CPU-h) and quote that.

**B-5. "Three changes after the freeze" is incomplete.**
- **Where.** 06_strategy_wp.tex l.142–144.
- **Problem.** `HASH_ADDENDUM.md` records two more post-freeze code changes: §1 the G1b hook in `run_stage4.py` and §2 the
  navigation-assertion recovery in `run_chain.py`. Both are regression-tested. Post-freeze analysis-level fixes also
  changed B (STAGE4_RESULTS R6 items 1–6: A28 merge population, looper, D11). Phase B must mention them.
- **Fix.** List all addendum items, or say "the logged changes (HASH_ADDENDUM §1–6) are …".

**B-6. Stale number: the CKF removal fraction.**
- **Where.** 05_detector_chain.tex l.78: "About 18 % of the measurements are removed".
- **Problem.** `G1_REPORT.md` l.111/l.319 corrects the plan's 18 % (3 probe events, different counter) to 13.9 % of all
  measurements and 19.5 % of the barrel.
- **Fix.** Quote the G1 numbers.

**B-7. Mixed before/after values in the edge systematics.**
- **Where.** 09_mass_lambda.tex l.32: "a median of 1.8–5.2 % per edge type and at most 8.1 %".
- **Problem.** README l.106–107 gives the after-fix-R1 medians as 2.3/4.2/3.6/4.2/5.2/3.7 %, i.e. 2.3–5.2 %. The 1.8 is
  a before value, while the 8.1 % maximum is an after value.
- **Fix.** Write 2.3–5.2 %.

**B-8. One symbol per quantity (04-output.md).** These are different quantities that share a symbol, which is not the
Cat-A case of one quantity under two names. The heaviest collisions are:
- c is both the local slope and the category index ("each category c", "(m_Q, Λ, c)", Sec. 6.4–6.5). It is also c = 1 in
  App. A.
- K is both the QCD K-factor (Eq. 2, K(m_Q)) and the rotation constant K(γ*) (Eqs. 7–9).
- R is the tracker radius (Eq. 9), the response R(f) (Eq. 10), R_eff and the rungs R01/R_A.
- Θ = Nϑ (Sec. 3.4, N undefined) appears next to Θ = N_odd ϑ (Fig. 1) and N_osc.
- Λ is also the baryon (Sec. 5.3).
- L is the luminosity (Eq. 12) and also the log cutoff L ∼ ℓ_max (Sec. 3.3).

Fix: use another letter for the category (e.g. κ ∈ {T, G}) and for the K-factor (K_QCD), N_osc for the number of
periods, and Λ⁰ for the baryon. Add these to App. A.

**B-9. Figure quality.**
- Fig. 5 (S3_p2_observables.png) is illegible at print size. On the page-23 render the axis labels and legends are about
  4 pt. It is matplotlib-stitched, PNG-only and has a custom figsize (ISSUES.md item 3).
- Fig. 2 (S3_p1_dsB_c.png) has the same origin.
- Fig. 6 carries the internal ID "(see D9)" inside the plot.
- The fix is the planned T5/T6 restyle in Stage 5, or splitting Fig. 5 into a 2×2 plus 1×3 at the JFC panel heights.
  Remove "(see D9)" from the T4 plot text.

**B-10. Truth-level (m_Q, Λ) degeneracy claim.**
- **Where.** 09_mass_lambda.tex l.18–20: "Below ≈ 1.5 keV the B-field thickness depends on Λ only … together they
  separate m_Q and Λ".
- **Problem.** Λ_cross is 1.16 keV at 1500 GeV, so at 1.2–1.5 keV the total thickness of heavy pairs is MS-dominated and
  m_Q-dependent. The claim is a truth-level reading, so it should carry EST. STAGE4_RESULTS also finds sep_IT not
  measurable at PU 200, but that belongs to Phase B.
- **Fix.** Write "below Λ_cross(m_Q) (1.2–1.9 keV)" and tag the degeneracy-breaking statement EST (truth level only).

**B-11. Bibliography rendering and attribution.** The relevant entries are FASER:2026fsy, CMS:2017lum, Butler:2019rpu,
Zabi:2020gjd and Barbashov:1977tv (`.blg`: "empty journal" warnings).
- With unsrtnat the three TDRs print as papers by their editors ("J. N. Butler and T. Tabarelli de Fatis. A MIP Timing
  Detector … 2019.") with no "CMS Collaboration", no report number and, for the MTD/L1 TDRs, no DOI. They cannot be
  retrieved as printed.
- BKNC prints without JINR-E2-10626.
- FASER prints without a journal. INSPIRE now lists it as Phys. Rev. Lett. (2026).
- No arXiv number is printed for any entry.

Fix: switch to a style that prints `reportNumber`/`eprint` and `collaboration` (e.g. JHEP.bst or a natbib style with
eprint), or add `note = {CMS Collaboration, CERN-LHCC-2019-003, CMS-TDR-020}` style fields. Add the FASER journal. Log
the change in BIB_PROVENANCE.md.

**B-12. Author-set attribution.**
- **Where.** 01_introduction.tex l.23–24: "Li, Li, Pei and Zhang studied energy-loss signatures, quirk trajectories and
  the FASER reach [Li:2019wce, Li:2020aoq, Li:2021tsy]".
- **Problem.** 2108.06748 is by Li, Pei, Ran and Zhang (INSPIRE).
- **Fix.** Write "Li et al.".

**B-13. External-bound wording.**
- **Where.** 01_introduction.tex l.19–20: FASER excludes "up to m_Q ≈ 180 GeV in the range Λ = 0.3–105 keV".
- **Problem.** The 179 GeV maximum occurs only at Λ ≈ 10 keV. The excluded mass is 57 GeV at 0.3 keV and 66 GeV at
  105 keV (EXTERNAL_BOUNDS.md l.58). The sentence reads as a uniform bound.
- **Fix.** Write "up to m_Q ≈ 180 GeV near Λ ≈ 10 keV (57–66 GeV at the ends of 0.3–105 keV)". At l.27, "No
  central-detector quirk search at the HL-LHC has been carried out" is trivially true. The intended statement is that
  ATLAS and CMS have no dedicated quirk search, since FASER's is the first LHC quirk search.

**B-14. Step-convergence statement does not cover all P1 material runs.**
- **Where.** 04_truth_p1.tex l.17–18: "10⁻² with material … converged to ≲ 1 µm for hits at ≥ 2 keV".
- **Problem.** The M and BM P1 runs at 0.45–1.5 keV also use 10⁻² (Stage-3 plan l.121–122). Those runs feed the B+MS
  dip at 1 keV (0.80–0.97) and Λ_cross. The note does not say whether they are converged there. VALIDATION V3 lists
  30/32 cells passing.
- **Fix.** State the convergence status below 2 keV for M/BM, which may be a non-issue because the MS floor is ≫ 1 µm.

**B-15. The dE/dx unit is misnamed.**
- **Where.** 06_strategy_wp.tex l.58–59: "in units of the MIP peak of a muon gun (3.558×10⁻⁴ GeV per TBPX hit)".
- **Problem.** Frozen PC-13 (WP_RULE l.226, l.813) defines the unit as the pooled truncated mean of all muon-gun hits.
  The superseded draft was the per-track median, and neither is a "peak".
- **Fix.** Write "pooled truncated mean (MIP unit)".

### Category C (optional notes)

**C-1. Credit gaps against the novelty audit (minor; the audit's main requirements are met).**
- Met: credit sentences 1, 2, 3, 4, 9 and 10 are present nearly verbatim (Kang–Luty Eq. 5.64; Li App. A Eqs. A.6/A.17/
  V.5–V.6/B.9; elementary near-radial log; the 7 % charge test; KLN §3.2/Evans–Luty §2; BKNC/Petrov–Sharov). Sentence 8
  is present.
- Missing:
  - The 1911.02223 Fig. 4 credit for the mild m-dependence (sentence 5, Sec. 3.5 l.145).
  - The FASER App. A Geant4-EM credit (sentence 7, Sec. 3.7 l.243). C4 is withdrawn, so this is optional.
  - A citation of the ATLAS Athena `Simulation/G4Extensions/Quirks` software itself (core list item 11). Only the FASER
    paper is cited.

**C-2. Wording of the K effect.** 03 l.104: "K moves the slope c below by at most 6 %". The source says "moves c by
≤ 6 %". Since K < 0 at large γ*, "below" suggests the wrong sign.

**C-3. Overlapping MS-dominance statements.** 03 l.219 says "Above Λ ≈ 1.5 keV Δs_B is below the MS floor anyway". At
200 GeV, Λ_cross = 1.91 keV. Use "above Λ_cross = 1.2–1.9 keV". The same applies to 06 l.44–45.

**C-4. Process-diary sentence.** 03 l.147–149 has the withdrawn "literal form … earlier project version" sentence. It
belongs in the Change Log or a footnote, not in the physics text.

**C-5. Internal decision labels in the body.** U-2, U-5 b, D4-9, D4-12, D4-15, D4-17, PC-19 and "species-masses" appear
in the body. They are defined only in App. C, if at all. Consider "(user decision, App. C)" in the body.

**C-6. Equation reference format.** Fig. 1 caption: "Eq. 5" vs "Eq. (7)" elsewhere. Use `\eqref` throughout.

**C-7. Too little prose before bullets in Sec. 9.1.** It has one sentence before the bullet list and the figures. Add one
sentence on why truth handles matter, which the section intro partly gives.

**C-8. Unexplained ratio.** Sec. 9.1 l.28 "fixed ratio 38.2" needs its origin: √(R_IT/100 µm) = √1465.

**C-9. ETL surfaces.** Sec. 5.2 l.19 says "Each of the 83 physical Stage-3 surfaces becomes a sensitive ACTS surface",
but the ETL is excluded (l.23–24). Write "all 83 … except the endcap timing layer".

**C-10. Truth-level T-figures carry "PU 200, 3 ab⁻¹".** This is user-approved and every caption says pile-up is not
simulated. A shorter right label ("√s = 14 TeV") would remove the need for the disclaimer.

**C-11. Uncited bibliography entries.** Five entries in `references.bib` are not cited (bbl 44 vs 49):
CMS:2008xjf, CMS:2024nhn, CMSTrackerGroup:2024fgx, Gubser:2016wno and FASER:HEPData181308v1. This is harmless; prune
or cite.

---

## 3. Checklist summary

| Check | Result |
|---|---|
| Numbers vs sources (≥ 15) | ≈ 95 checked. All match except B-6 (stale 18 %) and B-7 (mixed range). A-1 is a disclosure problem, not a transcription error. |
| Physics correctness of the derivations | Eqs. 1, 5–10 and the rule constants verified. One prose dimensional slip (B-2) and one wrong scale range (B-1). |
| One symbol per quantity | Collisions only (B-8). No quantity has two names. |
| Truth vs detector explicit | Yes. Every P1/9.1 figure and caption says "truth level". P2 is labelled detector level. Fig. 3 "PU 200" label (C-10). |
| EST/UNV caveats preserved | Yes. Spot-checked about 25 tags against the sources, all carried. Missing: the EST tag on the degeneracy reading (B-10) and on the estimator-effect reading (A-1). |
| Novelty and credit (NOVELTY_AUDIT) | Framed as "an analytic theory of Li et al.'s η", as the audit requires. KLN Eq. 5.64, Knapen Eqs. 8–9, Li App. A/C, the elementary log, Kang–Luty §3.2/Evans–Luty §2 and Barbashov/Petrov–Sharov are credited. Minor gaps in C-1. "Kang and Luty" is correctly two authors. |
| References real and correctly attributed | 22 INSPIRE spot-checks pass. Rendering and attribution of TDRs/preprints in B-11. Author set in B-12. |
| Figures | Labels say "Private work (simulation)" (+ truth level). Captions are full, 2–5 sentences. Fig. 5 is illegible (B-9). |
| Not implying a CMS result | Yes. Status box, "CMS Phase-2-like", no CMS logo, and the Open-Data policy caveat (Sec. 11) is careful. |
| Completeness test | Passes for a concise note: every choice is motivated in a sentence and points to a stage report. Undefined N in Θ = Nϑ (B-8). Decision labels (C-5). |
| Prose ≥ 2–3 sentences before figures/bullets | Sec. 9.1 is borderline (C-7). The others pass. |
