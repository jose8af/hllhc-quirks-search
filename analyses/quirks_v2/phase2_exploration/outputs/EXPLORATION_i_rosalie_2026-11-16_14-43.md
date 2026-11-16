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
