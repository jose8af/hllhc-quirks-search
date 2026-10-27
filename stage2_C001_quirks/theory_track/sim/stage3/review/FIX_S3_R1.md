# Fix pass S3-R1: response to the critical and constructive R1 reviews (Stage 3, C001 theory track)

Fixer, 2026-10-13. Everything is truth level. Tags: VERIFIED = measured (production or a rerun in this pass);
ESTIMATE = model or interpretation. File:line references are to the files as written at the end of this pass. New CPU in
this pass ≈ 1.0 CPU-h (B*-off 0.84, V-scale s3 0.008, P2 robust systematics ≈ 0.1, V8 merge test < 0.01), within the
3 CPU-h cap. Not edited: `analytic/`, `code/T3_causal.py`, anything outside `theory_track/`.

**Regression check.** `p1_results.py` and `p2_results.py` were rerun after the edits. Every pre-existing leaf of
`P1.json` (4222), `P2.json` (3427) and `P2_points.json` (22 718) is unchanged (0 differences, compared against copies taken
before the edits). The new content is additive. `make_docs.py` regenerated SAMPLES.md and the auto blocks of README and
VALIDATION.

## New and changed files
- New scripts:
  - `scripts/fix_a1_floor.py` → `results/FIX_A1_floor.json`;
  - `scripts/fix_bstar_off.py` → `results/FIX_bstar_off.json`, raw data in `data/sim_stage3/fix_r1/bstar/`;
  - `scripts/val_vscale_s3.py` → `results/Vscale_s3.json`;
  - `validation/val_v8_merge.py` → `results/V8_merge.jsonl`.
- Edited scripts (additive): `scripts/p1_results.py`, `scripts/p2_results.py`, `scripts/make_docs.py`.
- Documents:
  - edited: README.md, VALIDATION.md, PROPOSED_CHANGES.md, HANDOVER_STAGE4.md;
  - new: DECISIONS_PENDING.md, this file;
  - also: `data/README.md`, one line in `LOG.md`.
- Figures (re-made): `p1_v2b_revisit.png`, `p1_dsB_c.png`, `p1_B_MS_BM.png`, `p2_edges_vs_mass.png`, `p2_observables.png`.

## Critical review (CRITICAL_REVIEW_S3_R1.md)

### A-1: attribution of the 3-5 keV c excess. **Resolved.**

**Changes.**
- Re-tagged everywhere: the size is VERIFIED; the attribution is ESTIMATE. Locations:
  - VALIDATION.md:42 (§0 row) and :298 (§8 item 5);
  - README.md:64-78 (headline 4);
  - PROPOSED_CHANGES.md:67 (§1 attribution) and :90-104 (P-10 wording).
  The text "VERIFIED: physical, not numerical" and the "(VERIFIED)" after "step- and round-off-stable" are removed. The
  §0 row for `val_c5kev` now reads "size stable; does NOT probe the precision floor" (VALIDATION.md, auto row before :42).
- The step/replica evidence is replaced by the discriminating tests:
  - `scripts/fix_a1_floor.py` reproduces the critic's `c_law`/`c_floor` matched-ε⊥ table and the floor-law allowance per
    k_B bin on the stored Δs. The matched-cell and floor numbers are identical to `c_floor.out`. The floor % differs by
    ≤ 0.3 % of c, because the bin's own median c_ev is used instead of a flat 0.072.

**New numbers (VERIFIED as measured; floor law ESTIMATE).**
- Matched cell k_B 4-10, ε⊥ 1-3×10⁻⁶: +1.7 ± 1.9 % at 3 keV → +14.6 ± 2.3 % at 5 keV.
- Matched cell k_B < 4, ε⊥ 3-10×10⁻⁶: −0.4 / +1.2 / +3.2 % at 2 / 3 / 5 keV.
- Floor allowance at 5 keV: 0.1-0.2 / 0.3-0.9 / 0.9-2.4 / 2.2-5.7 / 8.8-23 % of c, against measured +2.0 / +6.5 / +12.9 /
  +18.6 / +56.5 %.
- Quoted in VALIDATION.md:298ff and PROPOSED_CHANGES.md:67ff as: **"k_B ≥ 10 at 5 keV: +57 ± 11 %, of which ≈ 9-23 % of c
  may be the precision floor"**.
- The +3-5 % cumulative excess at k_B < 4 is noted.

**B*-off vs B*-on run (approved; `scripts/fix_bstar_off.py`; VALIDATION.md §8 item 5 table).**
- Method:
  - The production kernel has no E-field input. The Stage-1 FIX2 method was therefore used: `nm_bstar.bstar_off_fields`
    with `nm_kernel.run`, both imported read-only; T3_causal.py was not modified.
  - Both arms use the same kernel, at P1 settings.
  - Control: the B*-on arm reproduces the production Δs (median relative difference 0, max 2.3 %, median |Δc| 1.4×10⁻⁵).
- Sample: E 500 + E 1000 at 5 keV, 16 random events per k_B bin per mass (160 events), plus the 16 c5kev events (reported
  separately). 0.84 CPU-h; all runs had status 1.
- Median r/c_ev, pooled:

| k_B bin | 0-2 | 2-4 | 4-6 | 6-10 | ≥ 10 |
|---|---|---|---|---|---|
| B* on | +1.5 ± 1.4 % | +13.5 ± 7.4 % | +1.7 ± 4.5 % | +31.7 ± 18.9 % | +37.5 ± 20.4 % |
| B* off | +0.3 ± 0.4 % | +0.2 ± 0.9 % | +2.7 ± 1.3 % | +2.9 ± 1.0 % | +12.2 ± 3.3 % |

- All 160 events: on +10.3 ± 4.1 %, off +1.8 ± 0.7 %.
- The c5kev top-r events: +402 % (on) against +60 ± 56 % (off).
- Reading (ESTIMATE): switching B* off removes the bulk of the excess. The B*-off remainder at k_B ≥ 10 lies inside the
  floor allowance. The cumulative part at k_B < 4 also goes away with B* off at 5 keV. The on-arm bins are heavy-tailed,
  so the B* size per bin is measured only roughly.

**Plan deviation.** D12/O-1 (the double-precision floor test) is listed explicitly as **NOT DONE, a planned side study**
(VALIDATION.md:368, §9.1 table; also DECISIONS_PENDING.md U-1).

**PROPOSED_CHANGES P-10/P-11.** Corrected: PROPOSED_CHANGES.md:90-104 (P-10) and :106 (P-11). Neither carries "VERIFIED"
on the attribution.

### B-1 to B-7

| item | change (file:line) | new numbers / reason |
|---|---|---|
| B-1 the 30-cell average | Average split by regime: `p1_results.py`:362 (`regime_split`); README.md:64ff and auto :190; VALIDATION.md:279ff item 2; PROPOSED_CHANGES.md:37ff. The k_B ≥ 6 role is now described as "via scatter". The 0.986 correlation is marked "not evidence" (P1.json `corr_rel_vs_scatter_note`). | 0.45 keV −1.43 ± 0.51 %; 0.6 keV +0.64 ± 0.40 %; **1-2 keV +1.71 ± 0.29 %** (zero-median model +2.04 %); 3-5 keV +6.22 ± 0.45 %. The +1.85 % average is withdrawn. |
| B-2 P1 pulls | Paired per-event ratio with bootstrap error and pull: `p1_results.py`:131; README auto table :ff "paired Ds_B/model" column; README.md:49 headline 3; PROPOSED_CHANGES.md:122 (P-9). | E ≥ 500: 0.990-1.002; E 200: 0.966-0.990; Ẽ: 0.947-0.986. Agreement stated as ≤ 3.4 % (E), ≤ 5.3 % (Ẽ). At 10 keV: 1.016 ± 0.005 / 1.027 ± 0.005. |
| B-3 P-11 exponents | Pulls against −2 + 2c_ev and against the full model, every interval: `p1_results.py`:251; README auto exponent table (:175ff); PROPOSED_CHANGES.md:106ff. | 1→3 keV: 3.0/3.4/3.9σ at E1000/E1500/Ẽ500, measured slopes steeper (prediction − measurement convention). The full model has \|pull\| ≤ 0.6 there. |
| B-4 MS exponent | χ² and mass trend: `p1_results.py`:304; README.md:79 headline 5 and auto line :188 area. | χ² = 26.0/10 vs 0.517. E1000/E1500 are low (0.36-0.38). The P2 material systematic is unaffected (direct runs). |
| B-5 V8 | §0 row split into a literal FAIL on counts and a PASS on geometry and units (VALIDATION.md:53-54). §5 rewritten (:212ff). §9 item 5. HANDOVER.md:234ff. New `validation/val_v8_merge.py`. | doMerge = False: 470/470, 472/472, 448/448 (as V8), and 366/366, 362/362, 356/356 without T3V. The losses follow the cross-quirk pairs < 30 µm (4/22/72), not repeated crossings. One ACTS event per physics event is now required (HANDOVER §4 action 3). |
| B-6 merging-edge coverage | VALIDATION.md:348 (§9 item 8) corrected. Interpolated merge100 edges produced: `p2_results.py`:419, README auto table, figure. The √m premise is withdrawn. HANDOVER.md:265. | Interpolated at E 400/600/800/900/1100/1300/1400: 15.9 / 17.7 / 18.8 / 19.2 / 19.8 / 20.2 / 20.3 keV (± 0.4-0.6 fit). Deg-2 fit in ln m, χ² 4.6/4. ESTIMATE, flagged. |
| B-7 delivery vs plan §9 | VALIDATION.md:368 §9.1 (O-1, pixi tasks, script names, V8 reporting); README.md status lines. | pixi tasks were not added: `pixi.toml` is outside the write scope. |

### C items

| item | resolution |
|---|---|
| C-1, C-2, C-3, C-5, C-6, C-7 | No action required. They are accepted findings. |
| C-4 | F_m800/900 dip: HANDOVER.md:265ff tells Stage 4 to use the edges smoothed in m (`edge_fits_in_m`). |
| C-8 V9 wording | VALIDATION.md:257 now says that shared rows make the pulls *under*estimate the significance. |
| C-9 labels | Each figure has one "Private work (simulation) -- truth level" tag; the duplicate titles are removed (`p1_results.py`:388ff, `p2_results.py`:444ff). |
| C-10 | One FYI sentence in PROPOSED_CHANGES.md:84. |

## Constructive review (CONSTRUCTIVE_REVIEW_S3_R1.md)

### A-1: the V2b revisit figure. **Resolved.**
- The x-axis is now `zero_median_symmetric_scatter_Dc` (`p1_results.py` `figures`, after :388). The stratified
  permutation is shown only as grey "identity check, not a model" dots. Colour encodes Λ and the marker encodes the point.
- New caption: README.md:235ff. The text in `make_docs.py` does not depend on the plot.
- What the figure now shows: the 1-2 keV cells lie near the diagonal; the 0.45 keV cells and the 3-5 keV cells stand off it.

### B-1 to B-11

| item | change (file:line) | new numbers / reason |
|---|---|---|
| B-1 P-11 selective; validity window | Every interval is given with both pulls (PROPOSED_CHANGES.md:106). Median ℓ_max/R_IT per cell: `p1_results.py`:134, README table column. Window stated as ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4 (README.md:64, PROPOSED_CHANGES.md:90). The 0.45 keV cause is tagged ESTIMATE, with the finite-tracker alternative named (PROPOSED_CHANGES.md 0.45 keV bullet; VALIDATION §8 item 3). | 0.6→1 keV: 3.9-5.9σ off −2 + 2c_ev at all 5 points; the full model is within ≤ 1.2σ. 1→2 keV: 4.1σ (E1500), 4.5σ (Ẽ500). |
| B-2 paired test as the P-9 statistic | Paired ratio per cell and per γ* bin: `p1_results.py`:131, :280; README auto tables. P-9 restated (PROPOSED_CHANGES.md:122). Unpaired pulls kept as a secondary column. | γ* < 1.3: within 0.8 % (E 200 [1, 1.05): 1.008 ± 0.005). γ* 1.3-1.6: 0.956-0.981. γ* ≥ 1.6: 0.890-0.928, for both spins. Above 5 keV: 1.001/1.008 at 7 keV; **+1.6/+2.7 % at 10 keV** (unflagged events: 1.019/1.033). The 5→10 keV slope is 4.0/5.5σ off. |
| B-3 R(1/2) | Now "≡ 1 + c ln 2, not independent of P-10", quoted with pulls: README.md:49ff, README table column "R(1/2) (pull)", PROPOSED_CHANGES.md:117. | 1.0737 ± 0.0007 against 1.072: 2.4σ. |
| B-4 B/MS combination | Per-event BM/√(B² + M²) per cell (`p1_results.py`:226; README table column) and the crossover vs mass (README.md:79). Presented without deciding: U-2 (DECISIONS_PENDING.md). | 0.99-1.00 at 0.45 keV; 0.95-1.00 at 0.6 keV; 0.80-0.97 at 1-3 keV. Crossover 1.91/1.50/1.25/1.16 keV (E 200/500/1000/1500), 1.59 keV (Ẽ 500). |
| B-5 V8 = doMerge | See critical B-5. The open item is closed in VALIDATION §9 item 5; U-5 is pending. | (as above) |
| B-6 zero energy deposit | HANDOVER.md:85: Stage 4 must build p4_after from `h_dE` (on shell) for a charge-threshold digitiser. | The note was written; no code change was needed in Stage 3. |
| B-7 geometry contract | HANDOVER.md:94 (§2 "Geometry contract"): hits lie on the simplified surfaces; Stage 4 and the PU-200 Fatras must use the same surfaces; no trajectories are stored; one module per cylinder; sagitta ESTIMATE. U-4 is pending. | |
| B-8 continuous handle; redundancy | `sep_IT_handle` and `edge_redundancy` in P2.json (`p2_results.py`:376, :421). New panel in `p2_observables.png` (:469). README.md:86 headline 6 and auto lines :206, :232. | sep_IT log-log slope over 1-30 keV: **−1.98 … −2.02** at all 17 species-masses (∝ Λ⁻², i.e. ℓ₀). sep_IT/ℓ_max ≈ 0.5-0.6. The two ℓ_max edges are one quantity (ratio 38.21 at every mass). The merge25/merge100 edges are thresholds on sep_IT. The thickness edge is the only one tied to ε_B. |
| B-9 median granularity in systematics | Bootstrap-averaged paired shifts (40 common resamples), with the per-shift sampling σ: `p2_results.py`:49, :276, :373. Before → after in the README P2 table. | Median total per edge type before → after: 1.8→2.3, 4.7→4.2, 3.7→3.6, 4.7→4.2, 5.0→5.2, 3.0→3.7 %. Maximum 11.3 → 8.1 %. At F_m1100 ℓ_max, PDF goes 7.3 → 2.2 %. The envelope terms carry a positive noise bias, so the "after" values are conservative. Not done: symmetrisation or dropping shifts < 2σ, and the stat-syst correlation (stated in HANDOVER.md:281). |
| B-10 toys only at E1000/1200 | Documented: README.md headline 6, HANDOVER.md:286, VALIDATION.md:365. U-3 is pending. | The template ↔ toy swap was not run (left to Stage 4). |
| B-11 √m claim; interpolation | "√m" was replaced by the measured slope (README, HANDOVER). Interpolated merge100 edges and the ln-m fits with covariance are in P2.json `edge_fits_in_m`. | d ln Λ/d ln m = 0.249 ± 0.019 (ℓ_max edges), 0.248 ± 0.022 (merge100). merge100 is flat at 19.4-20.4 keV above 700 GeV. |

### C items

| item | resolution |
|---|---|
| C-1 labels | Physics labels (E, Ẽ, Λ, Δs, ℓ_max, µm), no code identifiers in legends, one truth-level tag per panel (`p1_results.py`, `p2_results.py`). The full restyle remains a Stage-5 task. |
| C-2 §0 preface | VALIDATION.md:16 adds a plain-language preface. It marks the criterion-vs-floor or setting artefacts versus the physics findings. |
| C-3 crossover | 1.2-1.9 keV, falling with mass (README.md:79). |
| C-4 status-4 one-sided | HANDOVER.md:30: worst case +1.9 % on the E1500 merge100 edge. Use a one-sided systematic or count these events as merged. |
| C-5 status 0 | HANDOVER.md:34. |
| C-6 V-scale with the production recorder | `scripts/val_vscale_s3.py`, 0.008 CPU-h, VALIDATION.md:270. At max_boost 10⁻² the same event fails (134 vs 136 hits). At 10⁻³ (production) **5/5 PASS** (max \|Δx\| 2.7 µm, Δs ratio 0.9957-1.0005). The E8 explanation (legacy recorder) was wrong: the failure is a step effect at 10⁻², and scaling hmax or first_length does not change it. |
| C-7 model = 0 for 5 events | Counted (`paired_ratio_n_model_zero` in P1.json) and excluded from the paired ratios. Medians are unaffected. The c06 edge case was not investigated, because `analytic/` is out of scope. |
| C-8 V8 bookkeeping | HANDOVER §4 actions 2-3: skip T3V; one ACTS event per physics event with per-event barcodes. |
| C-9 degeneracy variables | Suggestion added (HANDOVER.md:288). |
| C-10 merging thresholds | Labelled as truth-level pair separations. The physical edge comes from Stage-4 clustering (HANDOVER.md:265ff). |
| C-11 open-item bookkeeping | The edge is described as median-based, with the 25 µm edge available at 3 masses only (HANDOVER.md:265ff). |

### U-1 … U-5
Not decided. They are written up in `DECISIONS_PENDING.md`, each with options, costs and the reviewers'
recommendations.

## Not done (and why)
- D12/O-1 floor test. It needs an extended-precision step map, i.e. new kernel code, which is out of scope for a fix
  pass. It is listed as a planned side study.
- Stage-3 pixi tasks. `pixi.toml` is outside the write scope.
- Symmetrising the systematic shifts or dropping those < 2σ, the stat-syst correlation, and the template ↔ toy swap. These
  are reported or recommended for Stage 4.
- Investigating the c06 zero-model edge case (in `analytic/`).
