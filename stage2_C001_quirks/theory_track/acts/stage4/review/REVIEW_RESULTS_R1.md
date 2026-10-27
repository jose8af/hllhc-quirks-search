# REVIEW_RESULTS_R1 — critical review of STAGE4_RESULTS.md + STAGE4_SUMMARY.json (C12FC_v1)

Reviewer: fresh critical reviewer (JFC), 2026-10-16. Status: COMPLETE. Verdict ITERATE (1 A, 6 B, 11 C).

## Independent recomputation (from the raw C12FC_v1 outputs, not from STAGE4_SUMMARY.json)

| quantity | report | recomputed | source | status |
|---|---|---|---|---|
| min B84 SR-T / SR-G | 1.23e6 / 1.23e6 at R09 | 1.232e6 / 1.235e6 at R09_p>1e-3 | bsum_wp.json → ladder.T/G | OK |
| decades over 0.11 | 7.05 / 7.05 | 7.049 / 7.050 | log10(B84/0.11) | OK |
| WP branch | none, §8 fallback | rule.wp = {T: null, G: null}, branch "no WP in either category (§5.3): §8 fallback", complete_inputs true | bsum_wp.json → rule | OK |
| best mu95/N_exp | 37.6 (E200 1.5 keV, FB2) | 37.62 = 1.2458e7 / (219.2028 fb × 3000 fb⁻¹ × A = 0.50355) | limits.json expected_primary; acceptance.json A_trig_presel; xsec.json sigma_norm_nic2_fb | OK |
| second best | 39.1 (E200 2) | 39.07 | same | OK |
| worst / no-limit / 5σ | 1.0e7; 7 points no limit; 16 points 2.2e8–1.0e9 | 1.010e7 (E1500 0.85); 33/40 with limit; 16 points 2.18e8–1.03e9 | limits.json | OK |
| asym/toys | 0.32–1.07 | 0.320–1.071 | limits.json | OK |
| E200 1.5 SR-G B84 | 8.9e6 | 5.911e5 × e^2.709 = 8.88e6 | limits.json b, sigma_ln | OK |
| closure factor | × 2.409 | 1.50006 × 1.60609 = 2.4092 | STAGE4_SUMMARY closure.T1/T1w (= bsum) | OK |
| signal ε E500 3 keV FC | R04 0.305, R14 0.020, ε(FB3) 0.055, SR-T 0.045 | k = 61/200, 4/200, 11/200; limits s = [0.045, 0.010] | signal_eff.json a2.points; limits.json | OK |
| signal ε E200 1.5 keV | ε(FB2) 0.045 [0.030, 0.065], SR-T 0 | 9/200 = 0.045, CP68 [0.030, 0.065]; s = [0, 0.045] | signal_eff.json; limits.json | OK |
| SM proxy share | 45 % at R09; 15–45 % overall | 0.445 at R09; 0.146–0.445 over 37 columns | STAGE4_SUMMARY sm_proxy_fraction_of_B_SM | OK |
| PU alone B84 R09 / R08 | 2.3e3 / 3.0e4 (4.3 / 5.4 decades) | 2330 / 29927 (4.33 / 5.43) | statistics_reach | OK |
| σ_norm N_IC | flagged as inconsistent | 2 × K(1.11) × σ_LO(98.74 fb) = 219.2 fb; TH table "nic2" = 220 fb; plan l. 1050 "N_IC = 2, LO × K" | sim/results/xsec.json normalisation_E; plan.md | N_IC = 2 is settled (see C-finding) |
| selfcheck | 65/65 | re-run: 65/65 passed | selfcheck_stage4.py | OK |

No headline number disagrees with the outputs. No Category-A numerical inconsistency found.

## WP_RULE application

- `bsum_wp.json → rule.wp = {T: null, G: null}`; B84 > 0.11 at every one of the 23 rungs in both ladders (min 1.23e6
  at R09). The report applies WP_RULE §5.3 → §8 correctly: every one of the 40 points has `primary.branch = "fallback
  both"`, `background_free_claim = false`, `k_consistent = true` (limits.json). r_fb matches the WP_RULE §8 definition
  (N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p > 0.05 ∧ N_2S2 ≥ 3 ∧ w < W_k_adm ∧ h > 5 ∧ o > 5 [∧ e_adm], + time tag in SR-T).
- No per-point best-of, no limit at R_A–R_E, no 3-event discovery claim (mu_3events null everywhere), no merged-regime
  claim. The closure end state (×1.500, ×1.606, trend in σ_ln) is the pre-registered branch. Nothing post-hoc enters a
  number; the post-hoc elements are interpretive only (V4-3 "like for like", the new upper-edge comparator; B-2).
- The A2FC revert was pre-declared from production A1 before A2FC output existed (sha 32e1c6c3…), selected on the CKF
  fraction, not on ε; the A1-instead-of-A5 basis is disclosed. Acceptable.

## Findings

### Category A (must fix)

**A-1. The m_Q half of P2 is silently dropped from the final report and summary (user-approved D4-13 deliverable).**
- *Location:* STAGE4_RESULTS.md §6 ("P2 handles": only Λ edges, sep_IT^det, acceptance); §0 (no P2 statement);
  STAGE4_SUMMARY.json `p2_detector` (only `edges_A1_R04`, `edges_A2_R04`, `sep_IT_det_pu200`).
- *Evidence:* `grep M_est|beta_tof` → 0 hits in STAGE4_RESULTS.md, tables_C12FC_v1.md and the v2 summary. The superseded
  C12_v1 report §5 had the m_Q table (M_est = MET·cosh η/(βγ)_ToF, β_ToF, dE/dx median, w_core median as the ℓ_max
  observable; "M_est keeps a monotone mass ordering at PU 200 at the median", low tail from in-time PU BTL hits) and the
  statement that t_est/χ² vs Λ and `results/sensitivity.json` are not produced; STAGE4_SUMMARY_C12v1.json had
  `M_est_median_A2_GeV` / `M_est_median_A1_GeV`. plan.md l. 1856 (D4-13 (a), "approved by the user 2026-10-13") and
  l. 997 make these P2 observables a committed deliverable of the fallback. The arrays exist in the final run
  (`C12FC_v1/signal_obs_a2.npz`: M_est, beta_tof, dedx, w_core, sep_it_det_mm). The summary's own note says "v1 keys
  kept where meaningful", yet the M_est keys were dropped without a word.
- *Failure:* the task goal P2 is "measure m_Q and Λ". The final report gives the reader no detector-level statement at
  all on m_Q (nor on the w_core ℓ_max observable, nor that t_est / sensitivity.json were not produced), so the P2
  conclusion is incomplete and a committed, user-approved deliverable disappears between versions. A reader of the
  final report alone would conclude Stage 4 has nothing on m_Q.
- *Fix (cheap, read-only re-extraction):* in make_stage4_summary.py, extract per point (matched candidates at R04 and
  at r_fb, the same selection as C12_v1) the median [q16, q84] of M_est, β_ToF, dE/dx and w_core for A1 and A2
  (A2FC points included), write them to `p2_detector.mass_observables` (tag VERIFIED detector level; the "M_est ≈
  2.1–2.4 m" scale statement as ESTIMATE), add a §6.3 "m_Q handles" table plus a one-line P2 verdict for m_Q and Λ in
  §0 and §6, and restore the sentence that t_est/χ² vs Λ and `results/sensitivity.json` are not produced. Add the new
  numbers to selfcheck_stage4.py.

### Category B (should fix; advisory, do not block alone)

**B-1. E500 3 keV full-chain loss: scope of the caveat too narrow, headline not marked as dependent on it.**
- *Location:* §0 "One new surprise"; §4.3 last bullet; §8 caveat 16; §5 headline; §11.2 "max ε(r_fb)".
- *Evidence:* signal_eff.json a2.a2fc_revert: E500 3 keV R14 k 22 → 4, ε(FB3) 29 → 11 of 200 (−62 %). At the other 8
  revert points the full-chain/numpy ratio of ε(r_fb) is 0.67–1.26 (E500 5 keV 0.080/0.120 = 0.67; E1000 3 keV 1.26).
  Caveat 16 says only "3–5 keV-like topologies may be optimistic … only Ẽ500 3 keV is still numpy at ≥ 3 keV". But cause
  (b) of §4.3 (ACTS vs numpy digitisation in the χ²_core residuals) would act on *every* numpy A2 point, i.e. 31 of 40,
  including the headline E200 1.5 keV (FB2, p(χ²_core) > 0.05 inside) and the runner-up E200 2 keV. The report also
  does not mention that an investigation is open (`acts/stage4/investigation/INV_A2FC_E500.md`).
- *Failure:* a reader takes "37.6" and "max ε 0.080" as settled, while both rest on numpy-A2 ε whose full-chain
  validity is the open question. Direction is benign for the null conclusion (lower ε → larger μ95/N_exp, so "no
  exclusion" is robust), but the headline number could be optimistic by up to ≈ 1/0.67 ≈ 1.5× on the observed spread
  (more if the E500-3-type loss is generic).
- *Fix:* (i) in §0, §4.3 and caveat 16 state that the cause is under investigation in INV_A2FC_E500.md and that, until
  it closes, every numpy A2 ε (31 points, incl. the headline) carries an unassigned full-chain systematic, with the
  observed FC/numpy range 0.67–1.26 (outlier 0.38); (ii) tag the headline ratio "ESTIMATE, numpy A2 (no CKF), pending
  INV_A2FC_E500" and state the direction (conservative for the null result); (iii) commit to re-running the summary if
  the investigation finds a chain bug (it would change all 9 FC points and the "5–30 % below, as expected from CKF
  stealing" statement).

**B-2. V4-3 reported as "MET"; the upper-edge comparator is a post-hoc reinterpretation not labelled as such.**
- *Location:* §0 "What is solid"; §4.1; §11.5 V4-3; STAGE4_SUMMARY `validations.V4-3`; §6.1 "correct comparator".
- *Evidence:* plan l. 1810: "Expect ε ≥ 0.9 at 1–5 keV" and comparison (d) with "the hit-level merging edge at
  12.8–25 keV". Measured (cited_investigations.V4_3_A1_barrel): ≥ 0.9 only at 1.5 and 2 keV (Ẽ500 also 3 keV); 0.75–0.90
  at 1 keV, 0.83–0.87 at 3 keV, 0.58–0.84 at 5 keV. The definition used ("some candidate holds ≥ 50 % of the written
  quirk hits", `matched_any`) was introduced in INV_SIGNAL_EFF after the C12_v1 failure and is looser than the
  pre-declared signal match; with R04 required (`matched_R04`) E200 gives 0.63–0.65 at 1.5–2 keV. Comparator (d) is
  missed by × 2.7–3.5 (A1 upper edges 4.7–6.6 keV vs 12.8–22.9 keV); the "any-surface-merged 50 %" comparator was chosen
  after seeing that.
- *Failure:* "MET" on 2 of 5 Λ values with a post-hoc metric overstates a validation; plain-language §0 repeats it.
  The physics explanation (merging on any of 10 surfaces, seed degeneracy, CKF) is convincing, so the issue is the
  label, not the analysis.
- *Fix:* status "PARTIAL: ε_find ≥ 0.9 at 1.5–2 keV (any-candidate ≥ 50 % match, defined post hoc in INV_SIGNAL_EFF);
  not met at 1, 3, 5 keV (understood: merging / seed degeneracy / CKF)"; quote matched_R04 alongside. In §6.1 say that
  the pre-declared comparator (d) is not met and that the merged-surface comparator was derived afterwards (truth
  level, physically motivated).

**B-3. "PU alone … not a sample-size problem" contradicts the report's own "(bound)" label.**
- *Location:* §2 table last row ("not a sample-size problem (below)") and bullet 2; §0 "Why" 2.
- *Evidence:* §1.2 lists B_PU(R09) = 2.5 × 10² "(bound)"; bsum_wp.json ladder.G R09 term "PU R09_p>1e-3": value
  251.9, `zero_branch: true`, σ_ln comps stat 1.237, trend 1.262, density 1.151, closure 0.474, model 0.455, norm 0.262.
- *Failure:* the PU median at R09 is itself a zero-count bound and does shrink ∝ 1/N with more statistics of the bounded
  factor's population; only the trend/density/closure part is irreducible. The conclusion ("no achievable statistics")
  survives (scaling as in the other rows gives N ≈ 4.8e4 × 2330/0.11 ≈ 1e9 ρ = 1 trials, and the irreducible σ_ln ≈ 1.7
  alone needs a median ≲ 0.02), but the stated reason is wrong.
- *Fix:* replace "not a sample-size problem" with the N_needed estimate like the other rows plus "and the irreducible
  trend + density σ_ln ≈ 1.7 alone would need a median ≲ 0.02".

**B-4. The limits are not identified as simulation-statistics-limited in §0 / §5.**
- *Location:* §0 "Main result"; §5 headline.
- *Evidence:* at the headline point (E200 1.5 keV, FB2) SR-G is dominated by C′ PV pair (§1.4), a 0/24 zero-count bound
  entered as the log-normal median (§1.2 footnote, §2); likewise at every deep FB column.
- *Failure:* "best expected limit 37.6 × the predicted yield" reads as a physics-reach statement of a Phase-2-like
  search; it is a conservative number set by our 500–2 000-event MC samples (it would move ∝ the bound with more MC).
  §0 "Why" 1 explains the bounds but does not connect them to the limit numbers.
- *Fix:* one sentence in §0 and §5: "These expected limits use zero-count simulation bounds as background central values;
  they measure the reach of this simulation set-up and are conservative, not the physics reach of a real search."

**B-5. §0 does not state the P1 outcome (and, after A-1, the P2 outcome) in plain language.**
- *Location:* §0.
- *Failure:* the two project goals are P1 (B-field coplanarity vs MS floor) and P2 (m_Q, Λ, sensitivity). §0 covers
  sensitivity and the Λ window but never says that P1 is not addressed at detector level (D4-9: out-of-plane resolution
  23–30 µm = MS floor; truth-level U-2 panel only) or what Stage 4 says about m_Q and Λ measurement at PU 200
  (sep_IT^det NOT MEASURABLE; Λ only via the ε window).
- *Fix:* add a "P1 / P2 in one line each" bullet to §0.

**B-6. Wrong definition "FB_k = R14 ∧ w < W_k" makes §4.3 look self-contradictory.**
- *Location:* §1.1 table ("FB3 = R14 ∧ w < 9.4 mm") and bullet "r_fb = R14 ∧ (w_core < W_k_adm) ∧ …"; §4.3 "R14 22 → 4. So
  ε(FB3) = 0.145 → 0.055".
- *Evidence:* the ladder rung R14 is nested (it contains w < 4.7 mm and p > 10⁻³); WP_RULE §8 defines r_fb as the F0
  non-width cuts (N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p > 0.05 ∧ N_2S2 ≥ 3) with a single width cut w < W_k. Hence ε(FB3) = 0.055 >
  ε(R14) = 0.020 at E500 3 keV FC and ε(FB2) = 0.045 > ε(R_D) = 0.010 at E200 1.5 keV — impossible if FB_k ⊂ R14.
- *Fix:* define FB_k as in WP_RULE §8 ("R14's non-width cuts with the width rung replaced by w < W_k"); in §4.3 quote
  the FB3 counts directly (29 → 11 of 200) instead of deriving them from R14.

### Category C (optional)

- **C-1. σ_norm N_IC flag can be closed; no impact on the limit ratios.** The Stage-3 npz header `sigma_norm_fb` of
  `data/sim_stage3/inputs/F_m200_p2.npz` is 219.2028 = xsec.json `sigma_norm_nic2_fb` = 2 × K(1.11) × σ_LO(98.74 fb),
  and TH's N_IC = 2 table gives 220 fb; plan l. 1050 also says "N_IC = 2, LO × K". So the values used are N_IC = 2
  and the HANDOVER_STAGE4 l. 52 label "[fb, N_IC = 1]" is the error. μ95/N_exp is correct for the N_IC = 2 benchmark;
  a different N_IC would rescale every ratio by 2/N_IC (best 37.6 → 25 at N_IC = 3; below 1 only for N_IC > 75). Replace §4.4's
  "Labelling inconsistency (flagged)" and caveat 18 with this resolution (and flag the HANDOVER label upstream).
- **C-2. D12/D13 residue and V4-1 wording.** STAGE4_SUMMARY `validations.V4-1` still says "admitted by D12". §11.5 and
  the JSON say "PASS per job" next to an admitted FAIL; write "PASS in 2 294 / 2 295 jobs; A2FC_F1000_L3_000 FAIL
  admitted (D13)".
- **C-3. Tag and count consistency in §0.** "Main result [V]" contains the ratio 37.6, which §5 tags [E]. "Every one of
  the 40 points gets … an expected limit" vs 33/40 (7 have ε = 0 in both bins).
- **C-4. ρ = 2 reach arithmetic.** "2⁻²⁰/N_trials(ρ = 2) = 1.7 × 10⁻¹⁰": the value is 10⁻⁶/6 000; 2⁻²⁰/6 000 = 1.6 ×
  10⁻¹⁰ (plan l. 1110 uses 2⁻²⁰ ≈ 10⁻⁶). Write "≈ 10⁻⁶/N_trials".
- **C-5. Caveat 19 direction.** SM and C′ enter SR-T and SR-G with identical B (A12). Treating the two bins as
  uncorrelated is anti-conservative for the combination where both bins carry signal (partly offset by the double
  counting) and irrelevant at the headline point (ε_SR-T = 0, asym/toys 1.05). Say so.
- **C-6. Caveat list completeness.** V4-5 (independent finder cross-check) NOT RUN, V4-4 PARTIAL and the A43
  independence assumption (ε_tot = A × ε_finder) appear only in §11.5 / §4.4; list them in §8.
- **C-7. §1.2 σ_ln bracket** lists five components but the quadrature total also contains the normalisation term
  (0.262; bsum `comps.normalisation`). Add it or say "plus normalisation 0.26".
- **C-8. §10 item 8** re-uses the C12_v1 remaining-decades estimate; mark it stale or re-derive from C12FC_v1.
- **C-9. §6.1 lower edge.** No sentence compares the A1 lower edges (0.61–0.85 keV) with the ℓ_max = R_IT truth
  (0.43–0.78 keV): the detector edge sits × 1.1–1.4 higher; one line of interpretation would help.
- **C-10. §1.4 "used at" column** is approximate and overlapping (FB3 "2–3 keV", FB4 "3–5 keV"; E200 3 keV is FB4,
  the other 3 keV E points FB3). Generate it from limits.json `admissibility.fb_column`.
- **C-11. §0 "PU fakes fall by 6.4 decades … to 4.4 × 10³, already a bound"** — say "by at least" or quote the fall to
  R07 (last measured-ish value) to avoid mixing a measured and a bounded end point.

### Checked and fine (no finding)

Truth vs detector labelling (§0 Level, §4.4, §6.1, §7, caveat 21); barrel-only caveat; T3 non-informative and the
factorisation caveat (1); trend/model σ_ln dominance (2); flagged SM proxies with the 15–45 % share (4, verified
0.146–0.445); excluded G3 jobs (13); event replacement (12); D13 admission (14) — disclosed, PU-only, before the run;
A2FC pairing / re-smearing (15); future work and C4′/C2-C/C5 (11, §10); no novelty or "first" claim; make_figures
mismatch list (§11.3) is accurate and correctly kept out of scope; superseded C12_v1 versions kept and labelled stale;
selfcheck 65/65 reproduced.

## Verdict: **ITERATE**

Category A: 1 (A-1: m_Q half of P2 — the user-approved D4-13 mass observables M_est / β_ToF / dE/dx / w_core and the
"t_est / sensitivity.json not produced" statement — silently dropped from the final report and summary; cheap
re-extraction from C12FC_v1/signal_obs_*.npz). Category B: 6. Category C: 11.

All headline numbers (min B84 1.23e6, 7.05 decades, best μ95/N_exp 37.6, closure × 2.409, ε at E500 3 keV and E200
1.5 keV, 33/40 limits, asym/toys 0.32–1.07) agree with the raw C12FC_v1 outputs; the WP_RULE §8 fallback is applied
faithfully with nothing post-hoc in any number. After A-1 (and ideally B-1, B-2, B-6) the report should PASS.
