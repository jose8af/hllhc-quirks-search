# Fix R7: Stage-4 plan after review R7 (C001 quirks theory track)

Fixer S4PLAN-R7, 2026-10-13. Input: `review/REVIEW_S4PLAN_R7.md` (0 A, 1 B, 4 C). Only `acts/stage4/plan.md` was edited.
Text only; nothing computed (all numbers quoted are from `review_r7/r7_checks.json` or earlier fix outputs).

**Unchanged:** the C′ cost, every campaign and decision-table number, the schedule, the approved decisions, and the finder
speed-up files (`acts/stage4/finder/`, `data/acts_stage4/g2/`, `G2A_REPORT.md`).

## B-1: RESOLVED (reviewer's option (a))

- §2.2 step 3: **δn = min(δn_fit, δn_max)**, with δn_fit the angular standard error of the current normal (seed plane at
  collection, PV-constrained fit at each refit; the larger of its two components from the fit covariance) and
  δn_max = 2 mrad, stated as a chosen cap, not a bound on δn_fit. The prototype's δn = 0 satisfies the cap. Hence
  σ_tot,h ≤ σ̂_h for every candidate (σ_n ≤ σ_loc,max, reviewer-verified; min(δn, δn_max) ≤ δn_max).
- §4.2 preselection (σ̂_h paragraph) and attribution: "for δn ≤ δn_max" replaced by "for every candidate"; the attributed
  set is a superset of R5's for every candidate. The δn > δn_max sentence and its diagnostic are removed.
- §2.5 item 9: the capped δn of σ_tot is added to the `WP_RULE.md` freeze list.
- Consistency: every σ_tot/δn mention checked. §2.1 band (σ_tot² = σ_n² + t_tol²) and the §4.1 storage column are the
  δn = 0 prototype case, consistent with the cap. Header R6 bullet annotated "capped in fix R7".

## C-1: RESOLVED

§4.2 Overlay bullet: the preselection uses all stored toy measurements before CKF removal (§1.6) and before U-5 b merging
(§1.5); the V4-10 hash is on those pre-merge, pre-CKF measurements; the attribution tests each toy-linked core hit at its
stored C′₀ position and σ (truth link), not its merged position. What CKF/merging do in the with-PU event is part of the
measured P(pass | preselected, PU). §8 V4-10 row and §2.5 item 9 updated to match.

## C-2: RESOLVED (conservative-label option)

0.22 kept and labelled a **conservative upper value**: the per-event probability that some PU vertex coincides with the
PV (R1 critical l.117, B-4 (a): 200/(2√π σ_z) = 1.254 mm⁻¹, λ = 0.251, 1 − e^−λ = 0.222), not the per-NI fraction. The
per-NI fraction ≈ 0.006-0.014 (ESTIMATE, review R7 `PV_line`) and the ×15-35 (≈ 1.2-1.5 decade) overstatement are quoted.
Not replaced, because the per-NI value assumes the HS behaves as a PU vertex in the road and averages over plane
orientation, neither validated, so it is not cleanly derivable. Labelled in the §4.2 NI factor list, the B_NI formula
(with a note that the "8-9 decades" statements carry the same factor) and the C′ NI-rate note.

## C-3: RESOLVED

§4.2 C′₀ reach split: ≈ 4 × 10⁻⁵-1.3 × 10⁻⁴ for NI kinks (30 / 61.5 mm), ≈ 2.5 × 10⁻⁵-7.6 × 10⁻⁵ for DIF
(1.14/(5 × 10⁴ × 0.3-0.9)).

## C-4: RESOLVED (note added)

§4.2 attribution: one note that σ̂_h's δn_max·|u| term (≈ ±8 mrad from the PV) lets some pure-PU candidates be attributed
to toys as well as counted in B_PU; conservative double counting, negligible (≈ rate_NI × 0.22 × f_pre × O(10⁻³) × P_PU ≪
P_PU). The optional fraction report was not added.

## Neighbourhood check

grep over `plan.md` for σ_tot, δn, δn_max, σ̂_h, 0.22, V4-10, DIF reach, merging/CKF: header R6/R7 notes, §2.2, §2.5
item 9, §4.2 (C′ bullet, attribution, NI, DIF), §8 V4-10 and §11 item 5 agree. No numerical result changed; no
propagation needed.
