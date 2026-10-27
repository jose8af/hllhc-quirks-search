# Critical review S3-R2: Stage 3 (truth-level quirk string propagation), C001 theory track

Reviewer: fresh critical reviewer, round 2, 2026-10-13. Protocol: `methodology/03-review.md` §6.1 (only Category A blocks).
Everything here is truth level and uses public information only.

**What was read.**
- The R1 reviews (critical and constructive) and `FIX_S3_R1.md`. FIX_S3_R1.md was used only as a map; every claim was
  checked against the files.
- The deliverables: VALIDATION.md, README.md, PROPOSED_CHANGES.md, HANDOVER_STAGE4.md, DECISIONS_PENDING.md, the scripts,
  the results JSONs and the figures.
- The data: `data/sim_stage3/summary/*.npz` and `data/sim_stage3/fix_r1/bstar/*.npz`.
- The Stage-1 context: NUMERICS §13 (FIX2) and `nm_bstar.py`.

**Scratch.** Everything is in `review/r2_checks/`. The scripts, with their outputs in `*.out`:
- `bstar_recompute.py`: an independent rebuild of the B*-on/off bins from the raw npz files;
- `bstar_dist.out`, `bstar_context.py`: the per-event on/off distributions, and the full-production comparison;
- `val_v8_merge_r2.py` and `v8_rerun.jsonl`: an ACTS spot-rerun. This is a copy of the script with its output redirected
  here;
- `sepit_check.py`: recomputes sep_IT and the slope;
- `syst_check.out`: the robust systematics;
- `r_half.py`: R(1/2);
- `repro/` and `jsondiff.py`: sandboxed reruns of P1 and P2, with a leaf diff.

CPU used: about 0.05 CPU-h.

## 0. Verdict: **PASS** (0 A, 1 B, 8 C)

All the R1 Category A items are resolved, in the files and in the data:
- critical A-1: the attribution is now ESTIMATE everywhere, and a discriminating B*-off test was run;
- constructive A-1: the V2b figure is no longer circular.

The B*-off run is a faithful reuse of Stage-1 FIX2. I rebuilt its numbers exactly from the raw outputs. The headline
conclusion holds as an ESTIMATE: B* off removes the bulk of the median excess, and the k_B ≥ 10 remainder fits inside the
floor allowance. One sentence of the reading overstates the per-bin evidence, and the significance is not quoted (B-1).
This is advisory, not blocking: no number changes, and the tag is already ESTIMATE.

Regression check: P1.json, P2.json and P2_points.json reproduce with 0 leaf differences. Every leaf that existed at R1 is
unchanged.

---

## 1. Verification of the R1 items

### (a) B*-off comparison: method faithful, control good, numbers reproduce

**Method.** `fix_bstar_off.py` calls `nm_bstar.bstar_off_fields`, which is the NUMERICS §13 formula:
- E_lab = γ²β×fB;
- B_lab = γ²[β(β·fB) − β²fB], built from the initial pair velocity.

`nm_kernel.run` is used for **both** arms, at the P1 production settings: vacuum, origin vertex, max_boost 10⁻³, hmax 0.2
cm. The estimator is c2 = (2Δs(B₀/2)/Δs(B₀) − 1)/ln 2, with the same plane fit on the 10 barrel layers as `ds_barrel_um`.
This is the FIX2 approach transposed to k_f = 2 at 5 keV. The field scaling f is applied before the transform, as in
FIX2. OK.

**Control.** I compared the on arm with production on the same events (`bstar_recompute.out`). The bin medians agree:

| k_B bin | 0-2 | 2-4 | 4-6 | 6-10 | ≥ 10 | all |
|---|---|---|---|---|---|---|
| production r/c_ev | +1.5 | +13.5 | +1.5 | +31.7 | +39.7 | +11.2 % |
| on arm | +1.5 | +13.5 | +1.7 | +31.7 | +37.5 | +10.3 % |

Per event, the median |c_on − c_prod| is 1.4×10⁻⁵. However, 5 of the 160 events have |Δc| > 0.01, with a maximum of 0.09.
These are events with Δs_B ≈ 0.03 µm. The quoted "max 2.3 % in Δs" is this same tail (see C-1).

**Selection.** The 16 events per k_B bin per mass are drawn at random from events with status 1 in both the B and B2
configurations, using two seeded draws. The 16 c5kev events are reported separately and kept out of the bins, which is
correct. All 171 events × 4 runs have status 1.

**Errors.** The bootstrap medians on 32 heavy-tailed events are honest, and the "measured only roughly" caveat is given.
The paired bootstrap of the difference of medians is in the JSON (`arm_median_difference`) but not in the text (B-1).

**Recomputed bin, k_B ≥ 10, pooled, 32 events, from the raw npz.**
- On arm: +37.5 ± 19.5 %. Off arm: **+12.2 ± 3.2 %**. JSON: +37.5 ± 20.4 and +12.2 ± 3.3. Exact central values.
- The floor allowance evaluated at this subsample's own ε⊥ is 6.9-18.2 %. The quoted range, from the full population, is
  8.8-23 %. The remainder is inside both.

### Conclusion: supported, tagged ESTIMATE, wording too strong (B-1)

The tag is right. These locations all give the attribution as ESTIMATE, and only the measured size as VERIFIED:
- VALIDATION §0 preface;
- the auto row ("measured (VERIFIED); attribution ESTIMATE");
- §8 item 5;
- README headline 4;
- PROPOSED_CHANGES §1 and P-10;
- DECISIONS_PENDING U-1.

### (b) No "VERIFIED" left on the attribution: resolved

I searched every `*.md`, the scripts and the results JSONs:
- "physical, not numerical" appears only in VALIDATION.md:298, where it is quoted as the corrected E8 tag;
- "round-off-stable (VERIFIED)" is gone;
- the JSON tags are `FIX_bstar_off.tag = "VERIFIED (measured, truth level)"` (the measurement only) and
  `FIX_A1_floor.tags = {measured_cells: VERIFIED, floor_law: ESTIMATE}`;
- `c5kev_diag.json` has no tag;
- PROPOSED_CHANGES:100 says "Size VERIFIED; it is step- and replica-stable", which is about the size only.

`VALIDATION_GATE.md:64` "The excess is not numerical (VERIFIED)" is the E7 gate record of the 1 keV V2b excess, which is a
different claim. OK.

### (c) V2b figure: resolved

The x axis of `p1_v2b_revisit.png` is now the zero-median symmetric-scatter model. The stratified permutation appears only
as grey "identity check" dots. The figure shows what the text says:
- the 1-2 keV cells lie near the diagonal;
- the 0.45 keV cells fall below it;
- the 5 keV cells sit at +9 to +17 % against x ≈ 1.2-2.8 %.

It is no longer circular.

### (d) V8 doMerge: diagnosis confirmed by a spot-rerun; handover complete

I reran `out_pc/p2/F_m1000/L30_BM_c00.npz` (variant A) in the acts env (pyacts 48.0.0), with the output redirected:
- doMerge = False: **448/448** measurements;
- doMerge = True: **375/448**;
- cross-quirk pairs within 30 µm: 72.

This is identical to `V8_merge.jsonl`. At 1 keV there are 40 same-quirk repeated crossings and 0 losses, so the
repeated-crossing hypothesis is correctly withdrawn. The §0 table shows a literal FAIL on the counts and a PASS on geometry
and units.

HANDOVER §4 lists the requirements:
- set doMerge explicitly;
- skip T3V;
- one ACTS event per physics event, with per-event barcodes;
- p4_after from h_dE (§1, l.88).

The geometry contract is in §2 (l.94).

### (e) P2 IT-separation handle: reproduces

I recomputed from `events_p2.npz` (template half, |η| < 2.5, status 1, plain np.median):

| point | median vs P2.json | slope over 1-30 keV, bootstrap | P2.json |
|---|---|---|---|
| F_m1000 | within ≤ 2.3 % (interpolated vs plain median) | −1.987 ± 0.025 | −1.985 |
| F_m300 | | −1.995 ± 0.032 | −1.997 |
| S_m500 | | −2.013 ± 0.020 | −2.013 |

The quoted range −1.98 … −2.02 is right. No error on the slope is quoted (C-3).

### (f) Interpolated merge100 edges: flagged, with fit errors

`P2.json edge_fits_in_m["F/upper_merge100_hit"].interpolated` carries:
- a `"how": "interpolated … not measured"` flag;
- `err_fit` of 0.40-0.58 keV.

The README table puts these values in parentheses marked "interpolated in ln m", and the figure marks them with crosses.
The fit is deg-2 with χ² 4.6/4 and the covariance is stored. The errors are fit (stat) only (C-5).

### (g) Robust systematics: reproduced; the method is defensible as conservative

The maximum total goes from 11.34 % (F_m1100, ℓ_max-based edges) to 8.05 % (F_m200 ℓ_max = 100 µm). At F_m1100 the PDF
component goes 7.25 → 2.17 % (`syst_check.out`). These match README headline 6.

The method is a bootstrap-averaged ("bagged") paired shift on common resamples. It removes the granularity of the
reweighted median and is a legitimate smoother. Its positive bias on envelope and quadrature terms is stated. Note,
however, that **198 of the 243 robust ℓ_max/QED/PDF components are below 2× their own sampling σ**. So the "after" totals
are mostly noise-limited upper bounds (C-4).

### (h) Validity window, Λ exponents, MS χ², B + MS combination, R(1/2): resolved

- **Validity window.** Stated as median ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4, tagged ESTIMATE as a boundary (VALIDATION §8.1,
  P-10).
- **Λ exponents.** Every P-11 interval now carries both pulls (PROPOSED_CHANGES P-11). The reading is ESTIMATE. The E8 line
  "within 0.03, VERIFIED" is explicitly superseded (README headline 4).
- **MS exponent.** χ² = 26.0/10, with the mass trend stated (README headline 5).
- **B + MS combination.** Measured sub-quadrature (0.80-0.97 at 1-3 keV). The combination rule is left as U-2.
- **R(1/2).** Stated as ≡ 1 + c ln 2. I recomputed 1.07372 ± 0.00066 (E500, 1 keV, n = 300), which gives
  (1.0737 − 1.072)/0.0007 = 2.4σ, as quoted.

### Other R1 B items

- **Critical B-1** (regime split; the 0.986 correlation withdrawn): done.
- **Critical B-2 and constructive B-2** (paired ratios): done.
- **Critical B-6 and constructive B-11** (√m replaced by 0.249 ± 0.019): done.
- **Critical B-7** (§9.1 deviations table): done.
- **Constructive B-6, B-7** (h_dE, geometry contract): done.
- **Constructive B-8** (handle and redundancy): done.
- **Constructive B-9** (robust shifts): done, see (g).
- **Constructive B-10** (toy restriction, U-3): done.
- **Critical C-8** (V9 wording): corrected.
- **Critical C-9 and constructive C-1** (one truth-level tag per panel): done.

## 2. Regressions

- **Sandbox rerun** of the current `p1_results.py` and `p2_results.py` (`repro/`, with redirected RES/FIG and a sandboxed
  numba cache; 11 s and 152 s):
  - **0 leaf differences** against the delivered P1.json (4736 leaves), P2.json (9473) and P2_points.json (22 718);
  - against R1's sandbox copies, 0 of the 4222 / 3427 / 22 718 R1-era leaves changed or were removed. The fix is purely
    additive (`jsondiff.out`).
- **Labels.** Every panel of the five figures carries "Private work (simulation) -- truth level". There is no CMS, ATLAS
  or "Preliminary" label in any script, figure or document. "CMS-like" appears only in prose, as a description of the
  geometry. OK.

## 3. DECISIONS_PENDING.md

U-1…U-5 are each given with context, options, costs and the reviewers' recommendations attributed to the reviewer
concerned. The file says explicitly that nothing is decided there. The presentation is neutral enough: each U item says
which reviewer recommends what, and none is imposed. U-4 (b) has the cost "not estimated here", which is acceptable for a
Stage-4 option. These are user decisions, not findings, and none of them is classed here.

## 4. Deferred items: honestly listed, none blocks Stage 3 PASS

| item | where listed | blocks? |
|---|---|---|
| D12/O-1 floor test | VALIDATION §9.1 "NOT DONE … planned side study", README headline 7, U-1 | No. The B*-off remainder is bounded by the floor allowance, and the attribution is ESTIMATE. O-1 would only sharpen the k_B ≥ 10 remainder. |
| pixi tasks | VALIDATION §9.1 (pixi.toml outside the write scope); §10 gives the full command chain | No. The chain is reproducible: 0 leaf differences. |
| symmetrisation, dropping shifts < 2σ, stat-syst correlation | FIX "Not done"; HANDOVER §4 states the correlation but **not** the symmetrisation or the < 2σ issue | No (C-4). |
| template ↔ toy swap | HANDOVER §5, U-3 | No. It is a Stage-4 closure input. |
| c06 model = 0 edge case | `P1.json paired_ratio_n_model_zero` (4 events in total; FIX says 5); not in VALIDATION §9 or HANDOVER | No. The events are excluded from the paired ratios and the medians do not move (C-6). |

---

## 5. Findings

### B-1: the B*-off reading overstates the per-bin evidence, and its significance is not quoted
**Evidence** (`bstar_recompute.out`, `bstar_context.out`, `bstar_dist.out`).

1. *The text contradicts its own table.* VALIDATION §8 item 5 says "switching B* off removes the bulk of the excess **in
   every bin**". In the same table, k_B 4-6 has on +1.7 ± 4.5 % against off +2.7 ± 1.3 %: there is no excess to remove in
   that same-event sample. At 0-2 the on arm (+1.5 ± 1.4 %) is itself consistent with zero.
2. *Weak paired significance.* The paired on − off difference of medians is:

   | selection | on − off | significance |
   |---|---|---|
   | 2-4 | +13.3 ± 7.5 % | 1.8σ |
   | 6-10 | +28.8 ± 18.7 % | 1.5σ |
   | ≥ 10 | +25.4 ± 19.6 % | 1.3σ |
   | k_B ≥ 6 pooled | +27.6 ± 12.1 % | 2.3σ |
   | all 160 events | +8.6 ± 4.2 % | 2.1σ |
   | k_B < 4 | +4.1 ± 2.2 % | 1.8σ |

   So "the +3-5 % cumulative part at k_B < 4 also disappears with B* off" is a 1.8σ statement.
3. *Mixed samples in one table.* The PROPOSED_CHANGES §1 table puts the B*-off row (E500 + E1000, 32-event subsample) under
   the production row (5 points pooled) without the B*-on row of the same events. At k_B 4-6 this shows 12.9 → 2.7 %,
   whereas the same-event comparison is 1.7 → 2.7 %.
4. *Where the decisive support lies.* The off arm compared with the full-statistics production population of the same two
   masses:
   - per k_B bin, production +1.2 / +6.9 / +9.6 / +16.7 / +56.8 % against off +0.3 / +0.2 / +2.7 / +2.9 / +12.2 %;
   - all events: +9.7 ± 1.2 % against +1.8 ± 0.7 %, about 5σ (partly overlapping samples).

   That comparison is not quoted.
5. *A population statement, not a per-event one.* B* broadens the per-event c rather than shifting every event. At
   k_B ≥ 10, the per-event (on − off)/c_ev has median +8 ± 19 % and interquartile range −30 … +112 %. The "removed
   excess" is a statement about the population median, not a per-event offset.

**Why B, not A.** No number is wrong. The aggregate conclusion (bulk removed; remainder within the floor) is supported, and
it is already tagged ESTIMATE.

**Fix (text only).** Do this in VALIDATION §8.5, PROPOSED_CHANGES §1 (table and attribution bullet), the P-10 wording and
README headline 4:
- replace "in every bin" with the pooled statements and their paired significances (all +8.6 ± 4.2 %; k_B ≥ 6
  +27.6 ± 12.1 %);
- add the B*-on row of the same events to the PROPOSED_CHANGES table, and the same-mass production comparison;
- reword the k_B < 4 sentence as "consistent with removal (1.8σ)";
- add one sentence noting that B* mainly widens the per-event c distribution at high k_B.

### C items (notes; no action required)

**C-1: on-arm control tail.** 5 of 160 events have |c_on − c_prod| > 0.01 (maximum 0.09, at Δs_B ≈ 0.03 µm). The "max
2.3 %" is quoted in Δs, which hides that it is ≈ 0.07 in c. The bin medians are unaffected. Quote the control in c units.

**C-2: floor allowance on the subsample.** At the B*-off sample's own ε⊥ the k_B ≥ 10 allowance is 6.9-18.2 % (quoted:
8.8-23 %, full population). The conclusion is unchanged.

**C-3: sep_IT slopes without errors.** The bootstrap error is ≈ ±0.02-0.03 (F_m1000 −1.987 ± 0.025). Add it to
`sep_IT_handle`.

**C-4: robust systematics are noise-limited.** 198 of the 243 robust ℓ_max/QED/PDF components are below 2σ of their
sampling sd. HANDOVER §4 should say that the robust totals are upper bounds, dominated by template sampling noise, and
should record the deferred symmetrisation and the < 2σ treatment. Today these appear only in FIX_S3_R1.md.

**C-5: interpolated merge100 edges carry fit (stat) errors only.** Stage 4 should add the systematic of the neighbouring
measured masses.

**C-6: the c06 model-zero edge case is not listed in VALIDATION §9 or HANDOVER.** The count is 4 in P1.json against "5" in
FIX_S3_R1.md. Add one line.

**C-7: figure cosmetics.**
- `p2_observables.png`: the top-row x labels overlap the bottom-row tags.
- `p1_v2b_revisit.png`: the grey dots use a different x quantity from the axis label. The legend explains it.

**C-8: V8 variant C still injects 10 physics events into one ACTS event.** The one-event-per-physics-event requirement is
specified but not tested. That is harmless, since doMerge = False gives exact counts in every variant.

## 6. Answers to the tasks

1. All R1 A items are resolved. Every R1 B item is resolved or deliberately deferred. The B*-off method is faithful to
   FIX2, the control reproduces production in the bin medians, and the k_B ≥ 10 bin reproduces exactly. The conclusion is
   ESTIMATE and is supported in aggregate; its wording is B-1.
2. No regressions (0 leaf differences). The figures are tagged truth level, and there is no experiment label.
3. DECISIONS_PENDING is neutral, with options and costs.
4. The deferred items are honestly listed (C-4 and C-6 are small gaps). None blocks the Stage-3 PASS.

**Category A open: none. Verdict: PASS** (1 B, 8 C). Do B-1 before the P-10 text leaves Stage 3.
