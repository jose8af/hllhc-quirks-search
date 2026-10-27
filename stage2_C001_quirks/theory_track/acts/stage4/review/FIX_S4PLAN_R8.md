# Fix R8: Stage-4 plan after review R8 (C001 quirks theory track)

Fixer S4PLAN-R8, 2026-10-13. Input: `review/REVIEW_S4PLAN_R8.md` (0 A, 1 B, 2 C). Only `acts/stage4/plan.md` was edited.
Text only; nothing computed. Numbers quoted (×1.6-15 band widening) are from `review_r8/r8_checks.json`.

**Unchanged:** every numerical value in the plan, the C′ cost, the campaigns and decision table, the schedule, the
approved decisions, and the finder speed-up files (`acts/stage4/finder/`, `data/acts_stage4/g2/`, `G2A_REPORT.md`).

## B-1: RESOLVED (reviewer's preferred option (a))

- §2.2 step 3: the frozen nominal is **σ_tot² = σ_n²(n, hit) + t_tol², with no normal-uncertainty term (δn = 0)**. This
  is the prototype's definition (`f1r_finder.py`). Every probe, the margin study, T_seed, the §2.1 μ_c, the §4.1 storage
  and t₁ rest on it. Fix R7's δn = min(δn_fit, δn_max) is superseded. It is kept only as a **pre-declared A5/B1 variation
  (not the default)** beside t_tol = 0/100 µm. With the cap, σ_tot,h ≤ σ̂_h still holds under that variation.
- δn_max = 2 mrad now enters **only** σ̂_h, the preselection/attribution tolerance. σ_tot,h ≤ σ̂_h holds trivially,
  because σ_n(n, hit) ≤ σ_loc,max,h (R7-verified) and t_tol is common to both.
- **f_pre exactness is unchanged and independent of δn.** The proof is restated in §4.2, "Why the weight is exact":
  - an attributed candidate has ≥ 3 toy core hits in ≥ 3 layers from ≥ 2 particles;
  - each of those hits is within ±4σ̂_h of the candidate's PV plane, at its stored C′₀ position;
  - so some triple has λ_min ≤ 48 with the same σ̂_h, the same stored PV and the same hits, which means the event is
    preselected.
  - The argument never uses σ_tot, so it holds for any δn (as review R8 showed).
- The attributed set remains a superset of R5's for every candidate.
- Edited passages:
  - header R6 bullet ("σ_tot has no δn term since fix R8");
  - header R7 bullet (marked superseded);
  - a new header R8 block;
  - §2.2 step 3;
  - §2.5 item 9: the freeze list now reads "σ_tot with δn = 0 (§2.2 step 3; fix R8)";
  - §4.2 σ̂_h paragraph and the "why exact" paragraph;
  - §4.2 attribution, both "σ_tot caps δn" sentences and the removed-diagnostic sentence.
- "The prototype's δn = 0 satisfies the cap" is deleted everywhere.
- §2.1 band and §4.1 storage column: both are now labelled explicitly as δn = 0, the frozen definition.
- Grep check: no "caps δn", "satisfies the cap" or "capped δn" remains. δn_fit appears only in the variation and in the
  superseded-history notes.

## C-1: RESOLVED

"Merged" is replaced by "inserted" where it means putting the toy hits into the PU event:
- header R6 bullet: "inserted into the PU event, not re-simulated";
- §4.2 overlay: "are inserted into the PU event";
- §11 item 5: "the C′_PU job inserts the stored C′₀ toy hits".

All remaining "merge" wording refers to U-5 b analysis-level merging, the 2-mrad candidate merge or the duplicate-merge
loop. Each was checked.

## C-2: RESOLVED (one line added)

§4.2 attribution: a measurement that U-5 b formed from a toy hit and a PU (or second toy) hit is tested at each of its
toy-linked stored C′₀ positions, never at its merged position. This cannot leak, because the preselection uses all
stored toy measurements. A header R8 bullet records it.

## Neighbourhood check

- Checked every σ_tot, δn, δn_max, "cap" and "merge" mention: the header, §2.1, §2.2 steps 2-4, §2.5 item 9, §4.1
  storage, §4.2 (overlay, preselection, attribution, R7 C-4 note), §8 V4-10 and §11 item 5.
- The R7 C-4 note keeps σ̂_h's δn_max·|u| term (≈ ±8 mrad), which is still correct.
- The V4-10 row needs no change.
- No number changed, so there is nothing to propagate.
