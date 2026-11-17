# EXPLORATION — channel (i), executor Rosalie (DRAFT, started 2026-11-16 14:43 -05)

Items: C1 (port and reproduction of v1), C2 (finder cross-checks), day-0 ρ = 2 memory/storage, unit costs.
Session log (detail, commands, state for a successor): `../logs/executor_rosalie_2026-11-16_11-55.md`.
Tags: VERIFIED (measured; campaign or file cited), ESTIMATE, UNVERIFIED. This draft is completed as verdicts arrive.

## 1. Measured unit costs against STR Table 4.0 (VERIFIED unless tagged)

| unit | measured | Table 4.0 | source (campaign) |
|---|---|---|---|
| ρ = 1 PU-200 event, chain + 4 finder trials, 3–4 jobs per node | 57–59 CPU-s | 60.4 s | p2-a-c1-pu1 (c1pu1-0000/0001) |
| chain per crossing (stage sum; Pythia overlay, Fatras, digi, seeding, CKF) | 12.3 s (CKF 7.1) | 13.5 s | p2-a-day0-pu1 |
| finder per ρ = 1 trial at the frozen road 0.15, T_seed 4, job alone | 11.27 ± 7.33 s (find 10.6 s); the assumed ×0.77 road saving is not seen | 11.7 s (road 0.25) | p2-a-day0-pu1 |
| ρ = 2 event (2 crossings, 2 trials, pre-merge store on) | 195 CPU-s (2,928 s / 15 events); maxwell was shared ≈ 11 min with a channel (ii) MG job during these jobs: timing caveat, memory unaffected | 206 s | p2-a-day0-pu2b, -pu2c |
| ρ = 2 max RSS vs events per job | 1.60 / 1.59 / 1.74 / 2.12 GB at 1 / 2 / 4 / 8 (1.08 GB at 1 event without the store) → 2 ρ = 2 jobs per node (STR §4.5 rule 2) | 1.46 GiB at 1 event | p2-a-day0-pu2, -pu2b, -pu2c |
| MLM 0–2j LHE event, MG + Pythia + conversion (FSR off) | 46 ms (928.5 CPU-s / 20,000) | 50 ms (G) | p2-a-c1-s2 |
| finder at T_seed = 2 (C2-c rerun) | same as T_seed 4: ρ = 1 49 s/event, ρ = 2 180 s/event | — | p2-a-c2-tstime |
| V4-5 direct-sum scan | 3.5 s per 101² normals at 17,951 window hits → ≈ 52 min per trial at full size | 0.3 CPU-h per event (E) | p2-a-c2-v45time2 |

## 2. Deviations (criterion as frozen / what is done / why / effect on the verdict)

**D-i-1 Pre-merge store size (STR §4.5 "Storage, redone"; COM B2-e).** Frozen: planning 3.6–14 MB per ρ = 2 trial,
200 GB planning, 400 GB cap. Measured: 33.8 MB per trial (1,015 MB / 30 trials; 110k–128k candidates with N_IP2 ≥ 6
per trial, ≈ 110 hits each) [VERIFIED, p2-a-day0-pu2b/c]. Projection: c1-pu2 ≈ 68 GB; with the 3,000-event 4a
sample ≈ 270 GB. Done: threshold kept at N_IP2 ≥ 6 (orchestrator, 2026-11-16). Effect: none on any verdict; 70 GB
above the planning value, below the cap.

**D-i-2 V4-5 scan algorithm (STR §4.2 table row V4-5; COM C2-a).** Frozen: exhaustive scan of plane normals on a
0.2 mrad grid within ±0.3 rad of the F0 normal, plus a 5 mrad global scan over the road, maximising the
resolution-weighted inlier count. Done: (i) the same grid (3001 × 3001 normals) and the same score, but each hit adds
its term only to the grid cells where |u·n| ≤ 4 σ (σ bounded per grid row); a cell outside a hit's band would receive
≤ exp(−8) = 3.4×10⁻⁴ from that hit. Built-in check: on each trial of the timing job the band result is compared with
the direct sum on a 41 × 41 sub-grid around n_F0 [size of the check and maximum difference: filled in from
p2-a-c2-v45time3]. (ii) The global scan uses all road hits on a 5 mrad grid of tangent coordinates within ±1.2 (±50°)
of n_F0, not the whole half sphere. Why: the direct sum costs ≈ 52 min per trial (18k window hits), 86 CPU-h for the
100 trials against 30 budgeted. What could hide outside ±50°: a plane through the PV whose normal is tilted by more
than 50° from F0's, i.e. a different candidate plane altogether (a different ribbon orientation in the road), not a
better fit of F0's own hits; it cannot change the fine-scan optimum, which lies within ±0.3 rad by construction, and so
it cannot change the C2-a pass/fail, which compares F0 with the fine-scan optimum and the fit. Closing check: a direct
half-sphere scan at 10 mrad (`--full-sphere 0.01`) on 10 PU trials (≈ 1 CPU-h ESTIMATE), reported as "best plane
outside ±50°: yes/no" per trial. Effect: the verdict is computed against a true exhaustive optimum on the frozen grid up
to the stated truncation.

**D-i-3 Probe-row exclusion off (STR §4.1 "Lost frozen inputs"; WP_RULE §5.4 item 10).** Frozen: v1 excluded probe
rows listed in `fix_r1/f1r_summary.json` (lost). Done: no exclusion in v2 (`QV2_ALLOW_NO_F1R=1` in the signal jobs).
Which comparisons it touches: only the ten signal counts. At the three C1 points v1 excluded **zero** rows (v1
`signal_eff.json` → `a2.points.A2|F|200|1.5|BM`, `|200|2|`, `|500|3|`: `excluded.probe_excluded = 0`, n_den = 200)
[VERIFIED]; and the v1 probe rows refer to v1 Stage-2 rows that do not exist in the regenerated sample. Effect: none,
in either direction.

**D-i-4 T_seed stability by regeneration (STR §4.2 table row T_seed; COM C2-c).** Frozen: "from stored hit dumps".
Done: the stored T_seed = 4 jobs (first 500 ρ = 1 and 200 ρ = 2 C1 events) are regenerated from the same job seeds
with the finder T_seed overridden to 2 (v1's own g3_rerun.py pattern), so events, PV, MET roads and trial seeds are
identical by construction; the chain is recomputed (≈ 13 s per crossing). Why: exact pairing with no new
reconstruction code; the dump route needs a new ρ = 2 rebuild. The pairing is checked (chain evstats and trial PV
identical). Effect: none on the statistic (paired event bootstrap as in v1 G3); cost ≈ 17 CPU-h (STR 44).

**D-i-5 C1 signal from regenerated Stage 2 and Stage 3 (STR §4.1 "Corrections to the plan"; COM C1-a, C1-e).**
v1's Stage-2 events and Stage-3 outputs are lost, so every signal comparison (the ten counts R04, R06, R07, FB at the
three points, and the twin ratios) is between **independent samples**: different MG events, different Stage-3 seeds,
different PU events (v1's per-row PU seeds hash the Stage-2 row, which is a new row). This was already the frozen
reading of STR §4.1 [A2] ("every C1 comparison is statistical and unpaired"). Power, stated: 400 v2 rows against 200
v1 rows, Fisher exact; the 2σ detectable relative shift is ≈ 34 % at R04 and ≈ 80 % at the fallback (STR §4.1 point 4,
script [13]); R07 and the fallback counts are "gross check only". The same holds for all background families (new seed
streams): the PU, C′, SM and rates comparisons are statistical by construction, with the bootstrap or binomial widths
in `c1_compare.py`. Stage 3 itself was not compared bit-level (D4 §5.1 A0 proposed it): its inputs are new.
Diagnostic of the regenerated Stage 2 (not a C1 quantity): see §3.

## 3. Stitch diagnostic (for S2-c / f₂₀₀, channel (ii))
v1's TRGS stitching (TRG with pT(QQ)_ME ≥ 100 GeV ∪ INC with pT_ME < 100) is exact if σ_TRG(pT > 200) equals
σ_INC(pT > 200, pT_ME ≥ 100) (stitch_trg.py docstring). With 20,000 LHE each, FSR off, CP5 [VERIFIED,
p2-a-c1-s2 + p2-a-c1-s3in, errors = √Σw²]:

| m | σ_TRG(pT > 200) [fb] | σ_INC(pT > 200, pT_ME ≥ 100) [fb] | ratio | z | INC rows used |
|---|---|---|---|---|---|
| 200 | 4.247 ± 0.074 | 3.798 ± 0.179 | 1.118 | +2.32 | 606 |
| 500 | 0.2437 ± 0.0038 | 0.2309 ± 0.0079 | 1.055 | +1.45 | 1,153 |

Reading: TRG above INC by 2.3σ and 1.5σ; both in the same direction (combined ≈ 2.7σ if independent, ESTIMATE). Not
conclusive with 20k INC events (its error dominates). If real, INC-based f₂₀₀ would be low by ≈ 5–12 % relative to the
TRG-based tail at these masses. A 100k INC chunk at m = 200 (≈ 1.3 CPU-h) would bring the INC error to ≈ 2 %.

## 4. Results (to be filled)
C1 families, C1-b arithmetic, C1-c container rerun, C2-a/b/c verdicts: pending (campaign states in the log).

## 5. C1-b — v2 arithmetic on v1's recorded counts (COM C1-b) [VERIFIED, outputs/c1b_arith.json, 2026-11-16 22:46]
Code: `src/v2arith/` (core.py: factor chain with the zero/low-count rule, SM / C′ / PU values, log-normal sum with
shared components, B84; test_core.py: 6 unit tests, all pass; run_c1b.py). Self-contained (numpy only, no v1 import).
Inputs: v1 `background.json` (recorded N/M chains, end-state PU factors, rates, σ, K) and `bsum_wp.json` (v1's terms
and B84 per rung).
- Central values: every term of SR-G R01–R14 and every non-PU term of SR-T R01–R14 recomputed from the recorded counts:
  worst relative difference 2.2×10⁻¹⁶; term widths identical. **PASS** (criterion 10⁻⁶).
- B84 (4×10⁶ draws, own RNG): worst relative difference 0.77 % (R03), 0.61 % at R14. **PASS** (criterion 1 %).
  Power: v1's own B84 used 10⁵ draws, whose Monte-Carlo spread is ≈ 1 % (sd over 20 seeds at 10⁵ draws: 0.95 % at R04,
  1.0 % at R14); at 2×10⁵ draws the v2 values differed from v1's by up to 1.55 %, i.e. the 1 % criterion sits at v1's
  MC precision. Stated with the verdict.
- NOT EVALUATED in this version (reason): the 28 SR-T pile-up terms (2 per rung; PC-19 time-tag factors from srt.json)
  and the F1 / fallback rungs R15–R23 and FB (h, o factorisation of wp.py). They feed the T1 inputs only at the fallback
  point; adding them is a few hours of work if the orchestrator wants the full ladder.
- Input schema against channel (iii)'s T1 builder (p2c_t1.py v1 mode): it reads v1 `limits.json` per point,
  b = [4.510×10⁵, 5.911×10⁵] (T, G) and σ_ln = [1.748, 2.709]. These are v1's Monte-Carlo **median** of the B sum and
  ln(B84/median) of the fallback rung FB2&h>5&o>5 (bsum_wp: median 4.510×10⁵ / 5.911×10⁵, B84 2.591×10⁶ / 8.875×10⁶;
  ln(2.591/0.4510) = 1.748), not the sum of the term values (2.05×10⁵ / 2.35×10⁵) and not the mean (1.9×10⁹ / 9.2×10⁹,
  heavy tails). Same source numbers, two representations: v2arith keeps the terms; T1-b collapses them into one
  log-normal per category. No disagreement on a number.

## 6. C2-a V4-5 — ruling of 2026-11-16 (orchestrator) and status
Evaluated **as frozen** (STR §4.2): PASS/FAIL separately for the PU-only and signal + PU halves and for the two
comparisons (F0 vs brute-force optimum within ±0.3 rad; F0 vs independent fit). Recorded per event in the same pass:
scores at n_F0 and at the optimum; the local optimum reached by steepest ascent on the same grid from n_F0 ("diagnostic,
no verdict"); the global scan ±50° (deviation D-i-2) and the 10 mrad full half sphere (first 17 PU trials); for PU-only
trials where the optimum is another plane: whether it is a stored candidate of the same trial (≤ 2 mrad), whether that
candidate passes R04, layers with an inlier, |n_z|. Signal + PU: direction differences and scores only.
Campaigns p2-a-c2-v45pu (3 jobs) and p2-a-c2-v45sig (3 jobs: 17 / 17 / 16 events from the a5 outputs at E200 1.5,
E200 2, E500 3 keV) queued on landau B after the signal full chain.
**Phase 1 assumed** that the maximum of the resolution-weighted inlier count within ±0.3 rad of the F0 normal is the
F0 plane's own optimum, so that a correct finder agrees with it to 1 mrad. **Phase 2 found** (two PU trials,
p2-a-c2-v45time4) that at pile-up 200 the ±75 mm window holds 18–24k hits and the maximum within ±0.3 rad is a
different plane 0.20–0.22 rad away with a higher score (50.6 vs 39.1; 53.7 vs 40.5), while F0 sits on a local maximum
(0.28 mrad within ±10 mrad) and agrees with the independent fit (0.20, 0.22 mrad). **Implications:** as frozen, C2-a is
expected to FAIL on PU trials for a reason unrelated to the accuracy of F0's plane; it tests global optimality of a
random plane in pile-up, which is the "optimality" question STR moved to Phase 4c.
**Proposed rewording (NOT applied; for the orchestrator and the user):** "|Δn| < 1 mrad between F0 and the maximum of
the resolution-weighted inlier count reached by steepest ascent from n_F0 on the exhaustive 0.2 mrad grid within
±0.3 rad (the plane's own optimum), and between F0 and the independent fit, in ≥ 48 of 50 events per half; the global
maximum within ±0.3 rad and over the road is reported with its score, without a criterion." Reasoning: it keeps the
exhaustive grid and the independent fit, removes the dependence on unrelated planes of the pile-up, and leaves global
optimality to the Phase-4c count where it was placed.

## 5b. C1-b completed — full ladder (supersedes the partial §5; VERIFIED, outputs/c1b_arith.json, 2026-11-16 22:54)
Scope: all 86 entries of v1's bsum_wp: SR-T and SR-G at the 23 ladder rungs (incl. the 28 SR-T pile-up terms with the
PC-19 time-tag factors of srt.json, the F1 h/o factorisation at R15–R23 with the trend re-evaluated at R15–R20) and the
20 fallback selections FB_k[e] & h>5 & o>5 in both categories (incl. v1's best point, FB2&h>5&o>5). Every term is
recomputed by `src/v2arith` (10 unit tests pass) from the recorded counts; no term is unmatched in either direction.
- **Central values: PASS.** Worst relative difference 0 (terms) and 2.2×10⁻¹⁶ (widths); criterion 10⁻⁶.
- **B84, criterion as frozen (within 1 %):** 57 of 86 entries within 1 %; **29 entries outside, worst 3.4 %**
  (SR-T R20 and FB4&h>5&o>5). Best point FB2&h>5&o>5: SR-T 0.87 %, SR-G 2.07 %. **As frozen: FAIL on 29 entries.**
- **Power, next to the verdict:** v2 B84 with 4×10⁶ draws; v1 computed each B84 with 10⁵ draws. The relative
  Monte-Carlo spread of a 10⁵-draw B84 (10 seeds) ranges 0.12–3.6 % over the 86 entries (1.85 % / 2.83 % at the best
  point T / G). The pull of v1's B84 against the 4×10⁶ value in units of that spread: max |pull| = 1.76, none above 3;
  best point 0.47 (T), 0.74 (G). Reading (no verdict change): every B84 difference is consistent with v1's own
  Monte-Carlo noise; the 1 % tolerance is tighter than v1's 10⁵-draw precision at the deep rungs, so the criterion
  cannot pass there even for identical arithmetic. Proposed (not applied): "within 1 % or within 3 times v1's own
  Monte-Carlo standard deviation".
- T1 input schema: v2arith reproduces channel (iii)'s limits.json inputs at the best point: median of the B sum
  4.503×10⁵ / 5.912×10⁵ (v1 4.510×10⁵ / 5.911×10⁵) and ln(B84/median) 1.741 / 2.688 (v1 1.748 / 2.709).
