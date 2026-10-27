# Fix report R2: Stage-4 plan (`acts/stage4/plan.md`), C001 quirks theory track

Fixer R2, 2026-10-13. Input: `review/REVIEW_S4PLAN_R2.md` (0 A, 5 B, 11 C), with the reviewer's scratch in
`data/acts_stage4/review_r2/`. The plan was edited in place. New probes are `acts/stage4/probes/f2r_profile.py`,
`f2r_analyse.py` and `f2r_cost.py`; outputs are in `data/acts_stage4/fix_r2/`. No install, no change to the acts pixi env,
no production run, no ρ = 2 run, no signal run.

**Compute this round: ≈ 0.22 CPU-h** (budget ≤ 1.5), all of it ρ = 1 PU-only trials at nice 15:
- 3 trials at the full normalised density: 0.17 CPU-h;
- 5 + 5 TDR-OT trials (the first set was superseded after the core-χ² definition changed);
- arithmetic.

## Headline

1. **Where the 48 s/trial goes (B-5).** About 72 % of it (TDR-OT) is a Python duplicate-merge loop in the probe. That
   loop is O(N_cand²) at 0.53 µs per comparison. With it vectorised, TDR-OT takes 5.7-11.8 s/trial.
   - **At the plan's adopted density** (IT + OT topped up; 3 trials, never timed before), the probe would take ≈ 3 400-6 000
     s/trial as coded, 97 % of it in that loop. With the loop vectorised it takes **167-228 s (median 211 s)**: seeding
     95 s, numpy refits 52 s, merge 33 s, numba refits 30 s.
   - The cause is real combinatorics: 2 × 10⁵ seeds pass T_seed = 6, because the L1/L2 and 2S bands saturate the seed score,
     and each seed scans ≈ 4 × 10⁴ road hits. The trials leave ≈ 10⁵ distinct candidates each.
   - The stored fix-R1 ρ = 2 counts attribute ≈ 46 % of the 400-1300 s per ρ = 2 trial to the same loop, and ≈ 26 % to
     per-candidate thinning Monte Carlo (12 ms × ≈ 2 × 10⁴ candidates).
   - **The 330 CPU-h needs a ×100 speed-up.** The listed routes reach 5-20 s/trial by ESTIMATE, i.e. ≈ 560-1 700 CPU-h
     recommended or ≈ 270-850 lean, plus B2 at its own ρ = 2 time.
   - `fix_r2/f2r_profile_summary.json`, `f2r_cost.json`.
2. **The core width is a real handle, but only in its plain form (B-1).** On PU only, the plain robust core width stays
   wide. At N_L2 ≥ 9 the per-trial minimum is 14.6-32 mm (TDR-OT, 5 trials) and 12.2-14.2 mm (full density, 3 trials,
   18 903 candidates). No PU candidate at N_L2 ≥ 9 is below 9.4 mm. An iteratively trimmed width collapses on PU (minimum
   0.5-3.4 mm) and was rejected before entering the plan.
3. **Feasibility (B-4), as now written in plan §2.6.**
   - At the normalised density, F0 counting and χ² leave PU at ~10⁻¹ per trial, against ≲ 3 × 10⁻⁹ per event needed.
   - The helix and opening tests act on single-interaction topologies, not on the dominant combinatorial PU. Only the ribbon
     width, dE/dx and BTL timing act on that class.
   - A B₈₄ ≤ 0.3 working point is plausible (ESTIMATE, not demonstrated) only for heavy masses (m ≳ 500 GeV) at
     Λ ≳ 2 keV. It is implausible at Λ ≲ 1 keV and at E200, where a result with non-zero, log-normally uncertain background
     is the honest expectation.
   - A fallback deliverable is pre-defined: ε and B at fixed rungs, and a limit with uncertain B.

## Changes to approved decisions

No approved decision (U-1…U-5, D4-1…D4-12) is reversed. The pending items stay **PROPOSED**:
- D4-10 (a′): only the floor wording changed, per C-7;
- D4-13, D4-14: unchanged, apart from a note on D4-14;
- the TDR top-up baseline: now labelled D4-15 and flagged as awaiting confirmation.

| Decision | What changed in R2 | Status |
|---|---|---|
| D4-1 (a) recommended scope (approved) | The cost is now stated as a function of the finder time per trial. ≈ 330 CPU-h holds only at 2 s/trial; the measured speed is 211 s at the adopted density, and the ESTIMATE after optimisation is ≈ 560-1 700 CPU-h. G2a (ρ = 1, ≤ 2 / ≤ 4 s) and G2b (ρ = 2, ≤ 20 / ≤ 60 s) gates ask the user before G3 | Decision unchanged. **The user should know now that (a) at 330 CPU-h is unlikely.** It is re-asked at G2a |
| D4-4 F0 + F1, B ≤ 0.3 (approved) | (i) F0 gains a ribbon-width rung family (w_core < W_c/2^k, k = 1…4) and a core-hit χ², defined from geometry and PU only. (ii) SR-T and SR-G each walk their own copy of the ladder, with B₈₄,c ≤ 0.15 each and a combined B₈₄ ≤ 0.3 check with joint tightening. (iii) A pre-defined **fallback deliverable** applies wherever no rung meets the rule | Inside the approved F0/F1 shape and B ≤ 0.3 total. **The fallback deliverable is new and needs user acknowledgement** before the G2 freeze |
| D4-5 (a) PU method (approved) | A per-rung-family method table; per-hit-set counting; a trend test; the failure path split by direction (a conservative failure means no extra statistics, with the bias added to σ_ln) | Inside (a) |
| D4-10 (a′) **PROPOSED** | Floor = max(\|smoothed shift\|, raw per-point sd), stated explicitly | still PROPOSED, awaiting the user |
| D4-13 **PROPOSED** | Unchanged. The fallback limit (§2.6) is built without D4-13 if D4-13 is declined | still PROPOSED |
| D4-14 **PROPOSED** | Note added: if (b) is chosen, the wide-regime topology gets its own frozen background-only ladder | still PROPOSED |
| D4-15 (label for the pending R1 item) | The TDR-normalised PU top-up stays the baseline and is flagged "awaiting user confirmation" (§1.4, §10) | awaiting the user |

## Item-by-item

Status: RESOLVED = fixed in the plan with evidence; RESOLVED (design) = fully specified, and the measurement belongs to a
named gate; PARTIAL = done as far as the plan can go; NOT ADOPTED = argued.

| Item | Action (plan §) | Evidence | Status |
|---|---|---|---|
| **B-1** core width excluded; "F0 alone does not separate" | **Width rung family:** w_core = 1.4826 × MAD of u·n₂ over the in-band IT + PS hits (the stored f1r `dw_core`), one step, no iteration; thresholds W_c/2^k = 37.5/18.75/9.4/4.7 mm (geometric halvings of the physics window). **Core-hit χ²:** χ²_core = λ_min(Σ_core w u uᵀ)/(n − 2) over the hits within c ± 2.5 w_core (2S hits with their projected error), one step. Inserted in the ladder after the N_IP2 rungs, before the core-χ² tightening, 2S and F1 (§2.2 items 5-6, §2.5 item 3). Ordering principle stated: counting first, then families by PU-only behaviour. Signal information disclosed: review R2's signal look prompted the family; the definitions, thresholds and placement come from geometry and PU only, and the probe rows are excluded. Width categories considered and not adopted (four-way budget; low Λ covered by the fallback). §0, §2.4, §12 risk 2 corrected ("layer count and χ² alone"); the expected consequence stated (edge moves up, WP likely Λ ≳ 1.5-2 keV) | `review_r2/r2_corewidth.json`. PU only, fix R2: per-trial min w_core 14.6-32 mm (TDR-OT, N_L2 ≥ 9), 12.2-14.2 mm (full density, 18 903 candidates), 0 PU candidates < 9.4 mm at N_L2 ≥ 9. Trimmed variant collapses (0.5-3.4 mm), **rejected**. The one-step core keeps ≈ 53/60 PU hits and leaves the PU χ² unchanged (median 2.87 vs 2.89) (`f2r_profile_summary.json`) | RESOLVED (design). The signal efficiency of the new rungs is deliberately not evaluated before the freeze (G2 V4-3) |
| **B-2** SR-T/SR-G 2-D WP | Scheme (c), budget split: each category walks its own copy of the ladder; r*_c = loosest rung with B₈₄,c ≤ 0.15 for it and all tighter rungs; then the combined B₈₄ (MC, shared sources correlated) must be ≤ 0.3, else both tighten one rung together. Justification against (a) and (b) given. §2.3 and §2.5 items 3, 5, 6 consistent | — | RESOLVED |
| **B-3** extrapolation covers only counting rungs | New §4.1 step 3b table with method, stored information, cost and closure test per family. Counting: per-subset thinning (enumeration / DP / importance sampling). w_core and χ²_core: per-subset recomputation (χ² as λ_min of summed per-interaction moment matrices = the exact refit of the fixed hit set). dE/dx: per-subset. h, o: factorisation with the conditional measured at ρ = 1, density-bin independence test and a 200-set recomputation check (T3s). SR-T: factorisation as before. Storage: weights computed in the job; hit records only for N_IP2 ≥ 7 sets and a 1 % sample (≈ 4 GB); a pre-declared sub-sampling fraction if the G2b time requires it. New closure tests T1w, T1e, T3s and a trend test (§4.1 step 4, V4-7) | Current thinning MC: 12-16 ms per candidate (VERIFIED, `f2r_profile_summary.json`). Hit records for all candidates would be ≳ 2 TB (1.1 × 10⁵ candidates per ρ = 1 trial at full density) | RESOLVED (design); costs ESTIMATE |
| **B-4** feasibility overstated; no fallback | New §2.6: (i) a table mapping each variable to background classes (combinatorial PU, k = 1, NI, DIF, cosmics), tagged M/D/E. The helix and opening tests give little against combinatorial PU. (ii) A plain statement: plausible region heavy E (≳ 500 GeV) and Ẽ500 at Λ ≳ 2 keV; uncertain at 1-2 keV and 300 GeV; implausible at Λ ≲ 1 keV and at E200. (iii) Fallback: ε and B at fixed rungs R_A…R_E; a Stage-5 limit with log-normal B at R_E (fixed rung, no per-point choice); Fatras/truth results only as labelled optimistic bounds; list of surviving outputs. §0, §2.3, §2.4, §2.5 item 6, §10 D4-4, §11, §12 aligned; the WP-rule strictness stated (median ≲ 0.015 per category) | measured inputs as cited in the table (`f1r_summary.json`, `r1c_*.json`, `f2r_profile_summary.json`) | RESOLVED. The feasibility itself is ESTIMATE |
| **B-5** cost headline vs measured speed | §0, §6.1, §6.2, §10 D4-1 and §12 risk 1 rewritten: cost = 179 + 53 t₁ + 2.8 t₂ CPU-h (recommended), 84 + 27 t₁ + 1.4 t₂ (lean), in a table. The 8 s → 840 sentence is replaced. **G2a** (ρ = 1, full normalised density, ≥ 20 trials: ≤ 2 s costed, ≤ 4 s proceed and report, > 4 s ask) and **G2b** (ρ = 2, ≥ 10 trials incl. thinning weights: ≤ 20 s, 20-60 s cut B2, > 60 s ask) come before any G3 ρ = 2 event. Required speed-up ×100 (×50 for 4 s). Routes, each ESTIMATE: hash-grid merge; (φ, z) hit index for the seed score (×20-50); N_IP2 seed score with T_seed(ρ) and seed-plane clustering (×5-20); numba refit for loose-rung candidates (×2-5); early termination (×1.5-2); DP thinning weights | **Profile (VERIFIED):** TDR-OT as coded 14-52 s (merge 72 %), 5.7-11.8 s vectorised. Full density as coded 3 400-6 000 s (merge 97 %), 167-228 s vectorised. The ρ = 2 pilot time is ≈ 46 % merge and ≈ 26 % thinning MC (`f2r_profile_summary.json`, `f2r_cost.json`) | RESOLVED (plan). **The speed itself is not demonstrated**: the combined ESTIMATE of 5-20 s does not support the 2 s target |
| Closure residual ×1.6-1.8 (review R2 §5) | §0, §4.1 box: stated as unexplained after de-duplication, with the candidate causes listed and "it is not the k model" withdrawn. The gate decides: G3 T1 plus the trend test with per-hit-set counting → nominal / conservative branch (thinning uncorrected, \|ln ratio\| ≈ 0.5-0.6 into σ_ln, no extra statistics) / anti-conservative branch (+50 % statistics ×2, then envelope × N_obs/N_pred). A cause found later cannot change the branch without a logged re-review | `review_r2/r2_dupcheck_summary.json` | RESOLVED (no cause claimed) |
| C-1 road overlap at 75 mm | §4.1 step 1: L3 ≈ 1.05 rad, shared; L4 at the edge | review R2 arithmetic | RESOLVED |
| C-2 per-event vs per-trial | Per-trial (single-road) rate is primary; ≥ 1-of-4 kept as a diagnostic; reach restated per trial | — | RESOLVED |
| C-3 "not the k model" | Withdrawn and rephrased (above) | — | RESOLVED |
| C-4 NI arithmetic and the L2 statement | All factors listed; P(NI fake) ≈ 2 × 10⁻³-3 × 10⁻² per event before F1 (6-7 decades). L2: without PU, N_IT2 ≥ 3 removes r_NI ≥ 61.5 mm; with PU, random L1/L2 crossings undo it, so the NI toy runs with PU. §4.2 table and text, §12 risk 3b | — | RESOLVED |
| C-5 T_seed criterion | T_seed(ρ) fixed on the stability of the pass fraction of every rung family that matters (N_L2, χ²_core, w_core), §2.2 item 4, G3 (iv) | `f1r_tseed_check.json` | RESOLVED |
| C-6 "one pre-declared F1 step" | Deleted; replaced by the fallback deliverable (§2.5 item 6) | — | RESOLVED |
| C-7 (a′) floor wording | "raw per-point sampling sd of the unsmoothed shift" (§7, §10); still PROPOSED | — | RESOLVED (wording) |
| C-8 signal χ² median | Measured values quoted: top-candidate all-hit χ²/ndf 1.0-2.1, median ≈ 1.4 over the 5 signal-top events at TDR-OT; Fatras medians 0.9-1.5 | `f1r_summary.json` → `sig_t2.*.chi2ndf_q` | RESOLVED |
| C-9 thinning MC | DP or importance sampling above \|S\| = 12, the MC error carried into σ_ln (§4.1 step 2); measured MC cost 12-16 ms per candidate | `f2r_profile_summary.json` | RESOLVED (design) |
| C-10 matched stubs | Stored as a diagnostic only, not a rung or a definition change: the full-cylinder geometry has no modules, and without a pT window the geometric match is weak. Can enter only at the freeze, on PU-only evidence | — | NOT ADOPTED as a rung (argued) |
| C-11 small-sample wording | Margin quoted with its uncertainty (5/14 signal, 8 of 14 at 1 keV; ratio 68 % range ≈ ×1-8), §0 and §2.4 | `f1r_margin.json` | RESOLVED |

## Things found while fixing

1. **The fix-R1 CPU picture was dominated by a probe artefact.** The O(N²) Python merge accounts for most of the ×4-5
   TDR-OT slowdown and about half of the ρ = 2 blow-up. Removing it does **not** rescue the cost: the full IT + OT density
   is still 211 s/trial, now for combinatorial reasons.
2. **The trimmed core width fails on PU.** Iterative trimming locks onto local hit clusters inside random candidates. Only
   the plain, one-step width is used.
3. **PU width falls with density.** The PU minimum at N_L2 ≥ 8 is 6.3-9.2 mm at the full density (3 trials, 75 323
   candidates; 3 below 9.4 mm, none below 4.7 mm). The narrow rungs carry the rejection, and their reach must be measured
   at G3.
4. **Discrepancy note.** The as-coded TDR-OT time from the profile is a median of 29 s (5 trials), against fix-R1's 48 s
   (32 other trials, with 7 parallel workers). The profile's "as coded" figure extrapolates the Python merge from its
   measured per-comparison cost. Both sets of trials show the same structure.

## Files

- plan: `acts/stage4/plan.md` (edited in place)
- new probes: `acts/stage4/probes/f2r_profile.py` (instrumented re-run of the f1r_finder trial, imported read-only;
  ρ = 1 PU only), `f2r_analyse.py`, `f2r_cost.py`
- outputs: `data/acts_stage4/fix_r2/f2r_profile_t1_o10.json`, `f2r_profile_t1_o20.json` (full density, 3 trials),
  `f2r_profile_t2_o0.json` (TDR-OT, 5 trials), `f2r_profile_summary.json`, `f2r_cost.json`, logs
