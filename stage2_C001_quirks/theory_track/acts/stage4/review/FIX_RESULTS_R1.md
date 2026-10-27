# FIX_RESULTS_R1: fixes for REVIEW_RESULTS_R1 (STAGE4_RESULTS.md + STAGE4_SUMMARY.json, C12FC_v1)

Fixer (JFC), 2026-10-16. Input: `review/REVIEW_RESULTS_R1.md` (1 A, 6 B, 11 C). The final run `C12FC_v1/` was only read.
No frozen analysis code, production data, `stage5/`, `investigation/` or `sim/stage3/` file was touched.
CPU: < 1 CPU-s per regeneration (stdlib python).

Files changed:
- `acts/stage4/STAGE4_RESULTS.md` (pre-fix copy kept in the session scratchpad only)
- `acts/stage4/results/make_stage4_summary.py`: new `_npz` (stdlib .npz reader), `_q`, `mass_observables()`; new JSON
  keys; m_Q tables in `tables_C12FC_v1.md`
- `acts/stage4/results/selfcheck_stage4.py`: 33 new checks (65 → 98), **98/98 PASS**
- regenerated: `data/acts_stage4/analysis/STAGE4_SUMMARY.json`, `acts/stage4/results/tables_C12FC_v1.md`,
  `headline_C12FC_v1.json` (only the summary and tables changed)

## Category A

| finding | change | status |
|---|---|---|
| **A-1** m_Q half of P2 (D4-13 (a)) dropped | `mass_observables()` re-extracts M_est, β_ToF, dE/dx (median [q16, q84], finite fraction, n) per species-mass from `C12FC_v1/signal_obs_{a1,a2}.npz` (BM; matched; R04; first matched candidate per (point, row); finite; pooled over Λ). This is the C12_v1 selection: the self-check runs the same function on `C12_v1/` and **reproduces `STAGE4_SUMMARY_C12v1.json` M_est_median_A1/A2 exactly**. Also added: A2 at each point's r_fb (FB_k ∧ h, o ∧ f_CKF < 0.2), per-point w_core medians at R04 (A1 and A2), M_est/m scale [E]. JSON: `p2_detector.mass_observables`, `M_est_median_A1_GeV` / `M_est_median_A2_GeV` (v1 keys restored), `P2_verdict`. Report: new **§6.3 "m_Q handles"** (table + 5 bullets incl. the "t_est / χ² vs Λ and `results/sensitivity.json` are not produced" sentence), P2 verdict paragraph at the top of §6, P2 line in §0, caveat 25. Values: A2 M_est 483 / 1 113 / 2 070 / 3 137 / 1 230 GeV (E200…E1500, Ẽ500; monotone in m), A1 541 / 1 196 / 2 270 / 3 320 / 1 410 (unchanged from C12_v1); scale ≈ 2.1–2.5 m (PU 200), 2.2–2.8 m (no PU). | RESOLVED |

## Category B

| finding | change | status |
|---|---|---|
| **B-1** E500 3 keV caveat too narrow | §0 (main result + "One new surprise"), §4.3 (new "Scope" bullet; "under investigation"; re-run commitment), §5 headline tag, caveat 16, §11.2: cite `investigation/INV_A2FC_E500.md` as **OPEN**; 31 of 40 numpy A2 points (incl. headline E200 1.5 and E200 2 keV) carry an unassigned full-chain systematic; FC/numpy ε(r_fb) ratio at the other 8 revert points **0.67–1.25** (outlier 0.38) read from the outputs (`a2fc_revert.eps_rfb_fullchain_over_numpy`, `eps_rfb_ratio_range_other_8`; the reviewer's 1.26 used rounded ε); 37.6 tagged "ESTIMATE, numpy A2 ε (no CKF), pending INV_A2FC_E500"; direction conservative for "no exclusion"; ≈ 1.5 × possible optimism. JSON `a2fc_revert.open_investigation`, `outcome.best_mu95_over_Nexp.tag`. Anchors `<!-- INV_A2FC_E500 -->` placed in §4.3 (with a "conclusion pending" line) and caveat 16. | RESOLVED for now; conclusion to be inserted at the anchor when INV_A2FC_E500 closes |
| **B-2** V4-3 "MET" with post-hoc metric | Status → **PARTIAL** in §0, §4.1 (title, definition flagged post hoc, `matched_R04` 0.64–0.77 quoted), §11.5, Appendix A, JSON `validations.V4-3`; §6.1 states comparator (d) (12.8–25 keV) is not met (× 2.7–3.5) and the merged-surface comparator was derived afterwards. Caveat 24. | RESOLVED |
| **B-3** "not a sample-size problem" | §2 table row: ≈ 1.0 × 10⁹ ρ = 1 trials + "irreducible trend + density σ_ln ≈ 1.7 alone would need a median ≲ 0.02"; §2 bullet and §0 "Why" 2 reworded. | RESOLVED |
| **B-4** limits not identified as sim-statistics-limited | Sentence added in §0 and §5 headline (+ JSON `best_mu95_over_Nexp.note`). | RESOLVED |
| **B-5** §0 lacks P1/P2 outcome | §0 "P1 and P2 in one line each". | RESOLVED |
| **B-6** wrong FB_k definition | §1.1 bullet: FB_k = R14's non-width cuts with a single w < W_k (WP_RULE §8), not nested in R14; §1.1 table label; §4.3 quotes FB3 counts directly (29 → 11 of 200). | RESOLVED |

## Category C

| finding | change | status |
|---|---|---|
| C-1 σ_norm N_IC | §4.4 "Labelling inconsistency (flagged)" → "N_IC = 2 (resolved)" with the 2 × 1.11 × 98.74 = 219.2 fb chain and 2/N_IC scaling; caveat 18 closed. **Proposed doc correction (not applied, outside scope):** `sim/stage3/HANDOVER_STAGE4.md` l. 52 "[fb, N_IC = 1]" → "[fb, N_IC = 2, LO × K]". | RESOLVED (upstream doc fix proposed) |
| C-2 D12/V4-1 wording | JSON `validations.V4-1` and §11.5: "PASS in 2 294 / 2 295 jobs; A2FC_F1000_L3_000 FAIL admitted (D13)". | RESOLVED |
| C-3 tag/count in §0 | "Main result [V; the limit ratios are E]"; "33 points with ε > 0 also get an expected limit (7 have ε = 0)". | RESOLVED |
| C-4 ρ = 2 reach arithmetic | §3 and JSON formula: "≈ 10⁻⁶/N_trials (2⁻²⁰ ≈ 10⁻⁶, plan l. 1110)". | RESOLVED |
| C-5 caveat 19 direction | Anti-conservative where both bins carry signal, partly offset by SM/C′ double counting; irrelevant at the headline point. | RESOLVED |
| C-6 caveat completeness | Caveats 22 (V4-5 NOT RUN, V4-4 PARTIAL), 23 (A43 independence), 24 (V4-3 PARTIAL), 25 (M_est proxy). | RESOLVED |
| C-7 σ_ln bracket | §1.2 header: "total also has normalisation 0.26" (self-checked from bsum comps). | RESOLVED |
| C-8 §10 item 8 | Marked stale (C12_v1 estimate; ladder B₈₄ moved ≤ 0.13 decades at R07–R20). | RESOLVED |
| C-9 lower edge | §6.1 bullet: A1 lower edge within ≈ 10 % of ℓ_max = R_IT for 4 of 5 (ratio 0.92–1.11), E200 × 1.4; × 1.2–1.6 above the Δs = 100 µm edge. (The reviewer's "× 1.1–1.4 higher" is not right for E1500, 0.71 vs 0.78.) | RESOLVED |
| C-10 §1.4 "used at" | Column rewritten from `limits.json → primary.admissibility.r_fb`; self-check compares the full point sets. | RESOLVED |
| C-11 §0 PU fall | "4.9 decades from R04 to R07 (1.1 × 10¹⁰ → 1.4 × 10⁵), and to a bound of 4.4 × 10³ at R08". | RESOLVED |

## Verification and neighbourhood check

- `python3 -I acts/stage4/results/make_stage4_summary.py` then `selfcheck_stage4.py`: **98/98 PASS**. New checks: M_est
  selection reproduces C12_v1 (A1, A2); `mass_observables` recomputed = JSON; all five §6.3 table rows; A2 ordering text
  (§0, §6.3); M_est/m scale; w_core E500 A1/A2 strings; t_est sentence; FC/numpy range 0.67–1.25 and outlier 0.38;
  31 numpy points; INV anchor and OPEN status; FB3 29 → 11; PU N_needed 1.0 × 10⁹, σ_ln 1.7 → median 0.02,
  normalisation 0.26; matched_R04 range; V4-3 PARTIAL (JSON and text); σ_norm 219.2; N_IC text; 33-of-40 text; §1.4
  point sets; summary r_fb = limits.json r_fb.
- Grepped the report for stale phrases ("like for like", "MET like", "R14 ∧ w", "not investigated", "N_IC = 1",
  "6.4 decades"): only intended occurrences remain (the HANDOVER label quoted as the error).
- No headline number changed (all 65 original checks still pass). The A2 M_est medians differ slightly from C12_v1
  (e.g. E1000 2 027 → 2 070 GeV) because the 9 revert points now use the A2FC full-chain rows.

## Open

- ~~B-1 conclusion~~: done in the addendum below.
- Upstream doc fix (C-1): `sim/stage3/HANDOVER_STAGE4.md` l. 52 N_IC label.

## Addendum (coordinator follow-up, 2026-10-16): INV_A2FC_E500 closed, M_est wording, frozen-code bug

| item | change | status |
|---|---|---|
| **B-1 completion** (INV_A2FC_E500 closed: statistics + measurement-noise draws; no merge bug; identical inputs and noise model; only genuine FC loss row 268, CKF, ≈ −5 % at R04) | Both `<!-- INV_A2FC_E500 -->` anchors filled: §4.3 (the investigation's suggested wording + bullets: no bug; **deep-rung paired comparison effectively unpaired**, only R04 genuinely paired; replicas ε_R14 ≈ 0.05 (10–11/200) vs numpy 22/200 and A2FC 4/200 = 0.020, 68 % CP [0.010, 0.036]; ε(FB3) 11/200, 68 % CP [0.039, 0.076], 95 % [0.028, 0.096]; **McNemar p = 7.6 × 10⁻⁶, global ≈ 10⁻⁴–10⁻³ after look-elsewhere, both [E], somewhat unusual, no mechanism found**; row 268; consequence) and caveat 16 (rewritten: "Deep-rung and fallback ε are statistically fragile"). "Pending"/"OPEN" removed from §0, §5, §11.2, §10 item 6. The 37.6 now carries ε(FB2) = 9/200, 68 % CP [0.030, 0.065], 95 % [0.021, 0.084] and the statement that deep-rung / fallback ε have large statistical uncertainty (few passing events, noise-draw fluctuations). JSON: `a2fc_revert.investigation` (status CLOSED, verdict, p-values tagged ESTIMATE, replica ε), `best_mu95_over_Nexp.tag`; new `fallback_points.*.{n_den, k_rfb, eps_rfb_cp95}` (stdlib Clopper–Pearson; its 68 % interval reproduces the pipeline's `cp68` at all 40 points to 1e-6). | RESOLVED |
| **M_est is a pair-mass estimator** (signal.py l. 203: M_QQ̄ ≥ 2 m_Q) | "≈ 2.1–2.5 m proxy scale" wording removed from §0, §6 verdict, §6.3, caveat 25, JSON `P2_verdict`. New: pooled median **2.26 m_Q at PU 200 (N = 850 of 1 051 events)**, at the pair-mass threshold; **0 of 9 551 below 1.5 m_Q without PU** (min 1.69 m_Q); **19 % (162/850) below 0.5 m_Q at PU 200** (PU-induced low cluster). Computed in `mass_observables()` (`M_est_over_mQ_pooled`; selection R04 ∧ f_CKF < 0.2, first matched candidate per event, all A2 points) and equal to the stage5 REVIEW_STAGE5_R2 recomputation (1051 / 850 / 2.256 / 19.06 %). | RESOLVED |
| **Frozen-code cosmetic bug** | Caveat 26: `products.py` l. 205–206 looks up `'trials_phimet'`, absent from `background.TR_KEYS`, so the event-display PU fake `met_phi` is null; Stage 5 works around it; frozen code not edited. Self-checked against the source and `event_display.npz`. | LISTED |

Self-check extended 98 → **121 checks, 121/121 PASS** (new: anchors filled and no OPEN/pending; JSON CLOSED; McNemar
7.6e-6 and 18/0 from `inv_a2fc_e500_paired.json`; replica 10/11 from `inv_a2fc_e500_repsum.json`; CP68 = pipeline cp68
at 40 points; quoted CP strings; pair-mass numbers vs Stage-5 R2; old scale wording absent; products.py bug present in
source and output). No headline number changed.
