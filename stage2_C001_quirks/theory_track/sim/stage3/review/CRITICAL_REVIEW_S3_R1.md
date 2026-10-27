# Critical review S3-R1: Stage 3 (truth-level T3_causal_s3 propagation), C001 quirks theory track

Reviewer: critical reviewer (R1), 2026-10-13. Classification: `methodology/03-review.md` §6.1. Category A blocks; B and C
are advisory.

**What was reviewed.** `sim/stage3/`:
- the documents: plan.md, VALIDATION_GATE.md (§7), VALIDATION.md, README.md, SAMPLES.md, PROPOSED_CHANGES.md,
  HANDOVER_STAGE4.md, E8_session_log.md;
- `code/`, `scripts/`, `results/*.json` and `figures/`;
- the data in `data/sim_stage3/`.

**Context read.**
- NEAR_MISS_IMPULSE §0, §5.3-§5.5, §6.4, §8 and §9.3 (FIX2);
- predictions.json;
- plan §5 (the validation criteria), §7 and §8 (D1-D16, all approved as recommended per LOG.md, 2026-10-11).

**Scratch.** Everything is in `review/r1_checks/`. The scripts, with their outputs in `*.out`:
- `c_svd.py`: SVD re-fit of every P1 B and B2 event;
- `c_law.py`: c-law recomputation;
- `c_floor.py`: floor versus cumulative test;
- `p1_paired.py`: paired Δs_B/model ratios;
- `p2_edge.py`: independent P2 edges, with and without the status ≠ 1 exclusion;
- `cev_check.py`: c_ev against c06;
- `v8_dup.py`: V8 missing-measurement diagnosis;
- `repro/`: sandboxed reruns of `xover.py`, `p1_results.py` and `p2_results.py`.

The checks took under 0.05 CPU-h in total.

## 0. Verdict: **ITERATE** (1 Category A, 7 B, 10 C)

The production, the merge, the P1 numbers, the P2 edges and the reproducibility all stand up to independent
recomputation. One claim does not: the attribution of the 3-5 keV c excess. It is tagged **VERIFIED "physical, not
numerical"** on the basis of tests that Stage 1 itself documented as blind to the precision floor. The plan's approved
floor test (D12/O-1) was dropped without being listed.

My own test suggests that the conclusion largely survives, but the evidence chain and the tag must be corrected before
this text goes into P-10. The fix is documentation plus one already-run analysis (A-1).

---

## 1. The c-law claims

### 1.1 Estimator identity with Stage 1: OK (C)
- c2 = (2Δs(B₀/2)/Δs(B₀) − 1)/ln 2 is NEAR_MISS §5.3 R(f) at k_f = 2, the convention of §9.3/FIX2.
- Δs = `ds_barrel_um` (10 T3 barrel layers, plane through the vertex). V2a reproduced Stage-1 per-event Δs bit for bit,
  960/960.
- c_ev in the files equals 1/(ln(ℓ_max/b_odd) + K(γ*)) from `c06.pair_params`: 0 difference on 120 events at 3 points
  (`cev_check.out`).
- **Post-processing floor excluded.** The stored Δs comes from the eigh plane fit, which has a floor of up to 0.015 µm.
  The top-r 5 keV events have Δs_B ≈ 0.06-0.25 µm, so I re-fitted every P1 B and B2 event (18 800) by SVD:
  - median |rel. diff| 1×10⁻⁷, maximum absolute difference 0.0066 µm;
  - every pooled k_B-bin median of r/c_ev is unchanged within errors (5 keV, k_B ≥ 10: +56.5 % stored, +55.3 % SVD).

  So the eigh floor plays no role (`c_law.out`).

### 1.2 Claim (a), the population excess as an estimator effect: holds at 1-2 keV (B-1 on the wording)
I recomputed this independently, with a deterministic symmetric-scatter model: r reflected about its γ*-bin or k_B-bin
median, both signs pooled (`c_law.out`).

| 1 keV | E200 | E500 | E1000 | E1500 | Ẽ500 |
|---|---|---|---|---|---|
| population excess | +0.70 % | +2.00 % | +1.07 % | +2.10 % | +3.15 % |
| paired median r/c_ev | −0.91 ± 0.88 % | +0.20 ± 0.38 % | −0.25 ± 0.29 % | −0.03 ± 0.33 % | +0.46 ± 0.87 % |
| symmetric-scatter shift (γ* / k_B conditioned) | +2.29/+2.15 % | +2.10/+2.16 % | +1.68/+1.87 % | +1.86/+1.82 % | +2.70/+2.81 % |

- Population ≈ paired + scatter closes to ≤ 0.7 % at every 1 keV point, and similarly at 2 keV. The mechanism is real:
  symmetric, heteroscedastic per-event scatter, largest on the low-c_ev and high-k_B side, raises the median.
- At 0.6 keV it does **not** close for F_m1500 (−1.36 % against +1.34 %) or Ẽ500 (−1.21 % against +2.79 %). That is the
  onset of the 0.45 keV failure.

### 1.3 Claim (b), the law fails at 0.45 keV: accepted (C)
- The pooled k_B-ordered residuals reproduce: +6.0 % (k_B < 2) down to −26 % (k_B ≥ 10). At 0.6 keV they still run
  +2.8 % → −7.3 %.
- The 0.45 keV point lies below the range of the c07 table (0.6-10 keV) and is where plan §1.2 expected non-secular
  terms. There is no contradiction with Stage 1.
- The c06 model Δs_B still holds there (|pull| ≤ 0.9), which is consistent: c06 is not the secular law.

### 1.4 Claim (c), the 3-5 keV excess: the numbers reproduce, but the attribution is not supported as tagged (**A-1**)
**The numbers reproduce.**
- Population at 5 keV: +9.45/+10.8/+13.3/+15.4/+17.1 %.
- Pooled 5 keV by k_B bin: +2.0/+6.5/+12.9/+18.6/+56.5 %.
- At 3 keV, k_B ≥ 10: +8.9 %.

**Consistency with Stage 1: no contradiction of the Stage-1 PASS.**
- The Stage-1 direct B₀ runs at 5 keV gave Δc(2) = +0.005 ± 0.007 (500 GeV) and +0.004 ± 0.007 (1 TeV) for the
  population, +0.003 ± 0.002 for k_B < 5, and +0.08-0.12 for k_B > 10 (3-5 events) (§5.5).
- Stage 3's paired values are +0.0065 (E500) and +0.0085 (E1000), within 1σ of Stage 1, with the same k_B ordering.
- FIX2 measured on − off Δc(4) = +0.0136 ± 0.0039 for k_B ≥ 5 at 3 keV and s = 1, where N_osc is 2.8× smaller than at
  5 keV. Stage 3's k_B ≥ 4 bins at 5 keV (+0.009 … +0.04) are of the same order. So the excess is consistent with
  Stage 1's documented B* part, and it lies inside §5.5's "up to tens of % in c per event for k_B ≳ 10".
- P-9's "≲ 1 % on Δs_B(5)/Δs_B(3)" still holds. The paired Δs_B/model ratio moves by only +0.2 % (E500, 0.995 → 0.997)
  and +0.3 % (E1000, 0.997 → 1.000) from 3 to 5 keV (`p1_paired.out`).

So (c) refines P-10; it does not overturn Stage 1.

**What is wrong.**
- VALIDATION §0, §8.5, README headline 4 and PROPOSED_CHANGES §1.3 and the P-10 wording state "VERIFIED: physical, not
  numerical" and "step- and round-off-stable (VERIFIED)". The evidence given is `val_c5kev.py`: 10⁻⁴ steps and momentum
  replicas.
- NEAR_MISS §9.3 (FIX2 verdict, part ii) says explicitly that the double-precision floor part is deterministic and
  step-independent, and that **"The step and replica tests do not probe this floor."** Stage 1 needed the B*-off runs to
  separate the two parts.
- `val_c5kev` therefore cannot exclude the floor. It also cannot isolate B* (there was no B*-off run).
- `c5kev_diag.json` itself shows 1e-3 → 1e-4 Δs_B changes of up to 20 % on individual top-r events (row 35480:
  0.0764 → 0.0616 µm).
- Plan D12 (floor test O-1, "do it", ≈ 1 CPU-h) was approved with all 16 decisions (LOG.md, 2026-10-11). It was neither
  done nor listed in VALIDATION §9 as a deviation.

**Reviewer's discriminating test** (`c_floor.out`).
- The precision floor depends on ε⊥ per oscillation and is N-independent (FIX2: B*-off Δc 0.0030/0.0038/0.0044 at
  s = 1/9, 1/3, 1). A cumulative effect grows with N_osc ∝ Λ².
- At matched (k_B, ε⊥(B₀)), the median r/c_ev is:

| cell | 2 keV | 3 keV | 5 keV |
|---|---|---|---|
| k_B 4-10, ε⊥ 1-3×10⁻⁶ | – | +1.7 ± 1.9 % | **+14.6 ± 2.3 %** |
| k_B < 4, ε⊥ 3-10×10⁻⁶ | −0.4 ± 0.6 % | +1.2 ± 0.5 % | +3.2 ± 1.1 % |
| k_B < 4, ε⊥ 1-3×10⁻⁶ | – | +0.9 ± 2.7 % | +4.8 ± 1.5 % |
| k_B ≥ 10, ε⊥ 1-3×10⁻⁶ | +5.6 ± 6.3 % | +8.4 ± 3.0 % | – |

- At fixed ε⊥ the excess grows strongly with Λ, so its bulk is cumulative (N-dependent), not the per-oscillation floor.
  Within one Λ the partial rank correlations are ≈ 0 (r vs k_B | ε⊥: +0.08; r vs ε⊥ | k_B: −0.05) because Spearman(k_B,
  ε⊥) = −0.91. **Within-Λ data cannot separate k_B from ε⊥**, which is the S1-R2 confounding point.
- The Stage-1 floor law (CM (0.5-1.3) u/ε⊥², full-event amplitude ≈ 3.85×; Δc ≈ 1.06·3δ/ln 2 at k_f = 2), applied to
  each event's ε⊥ at 5 keV, predicts:

| k_B bin | 0-2 | 2-4 | 4-6 | 6-10 | ≥ 10 |
|---|---|---|---|---|---|
| floor, as % of c | 0.1-0.3 % | 0.4-1.0 % | 1.0-2.6 % | 2.3-5.9 % | **8.7-23 %** |
| measured | +2.0 % | +6.5 % | +12.9 % | +18.6 % | +56.5 % |

  The floor is therefore minor below k_B ≈ 10, but it may be up to ~40 % of the k_B ≥ 10 excess.
- A cumulative excess of +3-5 % is also present at k_B < 4. FIX2 found B* on = off there, so not all of the "B*
  excess" is B*.

**A-1 required fix** (documentation; no new production).
1. Re-tag the attribution as **ESTIMATE**. The *size* of the excess stays VERIFIED.
2. Replace the step/replica evidence with evidence that discriminates: an N-dependence test at matched (k_B, ε⊥) like
   the one above, and the Stage-1 floor-law estimate per k_B bin. Quote the 5 keV k_B ≥ 10 value as "+57 %, of which
   ≈ 9-23 % of c may be the precision floor".
3. Say "cumulative; consistent with Stage 1's B* part for k_B ≳ 5 (FIX2); B* not isolated (no B*-off run); a +3-5 %
   cumulative part at k_B < 4 is unattributed".
4. In PROPOSED_CHANGES §2 (P-10 wording), drop "(VERIFIED)" after "step- and round-off-stable".
5. List D12/O-1 in VALIDATION §9 as an approved item not done, with its reason. Alternatively, run it, or run a FIX2-style
   B*-off on − off on the 12 + 4 c5kev events (≈ 1 CPU-h).

---

## 2. Category B (advisory; recommended before the Stage 3 → 4 checkpoint)

**B-1: the "+1.85 ± 0.19 % over 30 cells" statistic.** It averages over regimes the executor itself calls different:
0.45 keV (law fails), 1-2 keV (scatter only) and 3-5 keV (physical excess; cells up to +17 %). Its ±0.19 % is a formal
error on a heterogeneous mean.
- The 1-2 keV average happens to be ≈ +1.9 % as well, so the number survives, but the label "the median shift that the
  per-event scatter produces" is only demonstrated at 1-2 keV (§1.2).
- "Uncorrelated with the k_B ≥ 6 fraction (0.01 over 30 cells)" mixes Λ. At 1 keV the k_B < 6 sub-sample excess is
  smaller than the full one at 4 of 5 points (E500 +1.05 against +2.00 %; E1500 +0.26 against +2.10 %; Ẽ +0.87 against
  +3.15 %). The high-k_B events do drive part of the shift, through their scatter rather than through a conditional bias.
- `corr_rel_vs_scatter = 0.986` is near-tautological: the unstratified permutation keeps the median of r.
- Fix: quote the estimator statement at 1-2 keV (per Λ); describe the k_B ≥ 6 role as "via scatter"; drop the 0.986
  correlation as evidence.

**B-2: P1 Δs_B pulls understate the precision.**
- The MG model is the unmodified c06 (`p1_model_mg.py` imports `model_hits`, eta_scale = 1, K(γ*) from Stage 1).
  Nothing is fitted to Stage-3 data: OK.
- But the |pull| ≤ 1.7 uses only the unpaired bootstrap error of the measured median, while the model is evaluated on the
  same events. The paired per-event median ratio measured/model (`p1_paired.out`) is:
  - E1000/E1500: 0.997-1.002;
  - E500: 0.980-0.997;
  - E200: 0.966-0.990 (−3 … −11σ);
  - Ẽ500: 0.947-0.986 (−4 … −10σ);
  - 10 keV: 1.016 (E500), 1.027 (E1000).
- These deviations are within c06's declared accuracy (P-16: 1-4 %), and the 10 keV rise matches Stage-1 FIX2's direct
  B₀ shifts (+2.8/+3.4 %), which is good corroboration. But "predicts within |pull| ≤ 1.7" is not a precision statement.
- Fix: add the paired ratios to P1.json and the README table, and state the model agreement as "≤ 3.4 % (E), ≤ 5.3 % (Ẽ)".

**B-3: P-11 exponents.** "1→3 keV within 0.03 (VERIFIED)" holds numerically, but the pulls (README exponent table) are
−3.2σ (E1000, −1.849 ± 0.009 against −1.820), −3.4σ (E1500) and −4.0σ (Ẽ500). These go in the steeper direction,
opposite to the c excess. Fix: quote them as pulls; the reading belongs with B-2 (model accuracy).

**B-4: MS scaling exponent.**
- The ten population exponents against 0.517 give χ² ≈ 26/10, with E1000 and E1500 low by 2-2.6σ (0.36-0.38).
- 0.517 is a single-point code-scaling check (S_msscale, 500 GeV, 3 keV). Stage 3 agrees there (0.47 ± 0.07; event
  median 0.53).
- The README lists the "0.36-0.62" range without a verdict. Fix: state the tension and its mass trend. The P2 material
  systematic is unaffected, because it uses the direct ×0.5/×2 runs.

**B-5: V8 on production files.**
- (i) `V8_production.json` has `"PASS": false` for the 10, 15 and 30 keV files, but VALIDATION §0 shows "PASS
  (geometry, units)". Show it as a literal FAIL (as for V3/V4/V-scale), with the geometry and units passing.
- (ii) The stated hypothesis ("repeated crossings of one sensor by the same particle") is contradicted by the files
  (`v8_dup.out`):
  - same-quirk repeated crossings are 66/68/70/46 at 1/10/15/30 keV, with 0 measurements lost at 1 keV;
  - the losses (0/7/30/73) track the cross-quirk same-surface hit pairs closer than 30 µm (0/7/27/90).

  The likely cause is the digitiser merging the two quirks' smeared hits, which is the merged-pair signature itself. The
  10 events were also injected as one ACTS event.
- Fix the ESTIMATE in VALIDATION §5 and HANDOVER §4, and tell Stage 4 to check the digitiser's merge settings
  (doMerge/mergeNsigma or the equivalent) and to inject one ACTS event per physics event.

**B-6: merging-edge coverage (P2).**
- VALIDATION §9.8 says the edges at masses without Λ ≥ 15 keV points "come from interpolation in m". P2.json and the
  README give n/a there; no interpolated value exists.
- D5's premise ("the merging edge scales smoothly as √m") does not hold for the hit-level edge: 12.8 → 19.4 keV from
  200 to 700 GeV, then flat at 19.4-20.4 keV up to 1500 GeV. The closed-form ℓ_max = 100 µm edge does follow √m.
- The 7 measured masses bracket every gap, so interpolation in the measured shape is still safe. Fix the §9.8 sentence,
  and tell Stage 4 to interpolate the hit-level curve, not √m.

**B-7: delivery against plan §9.**
- O-1 (D12): see A-1.
- The plan's "pixi tasks for each step" are absent (no stage-3 task in `pixi.toml`). The script names differ from §9
  (produce/observables/sysweights versus run_stage3/extract/p2_results), and this is not stated.
- Fix: one line in README listing the deviations from §9. The reproduction chain in VALIDATION §10 is otherwise
  complete (see C-1).

---

## 3. Category C (notes; no action required)

**C-1: reproducibility (VERIFIED).** I reran `xover.py`, `p2_results.py` and `p1_results.py` in a sandbox from the
committed summary tables. `results/xover.json` (530 leaves), `P2.json` (3427), `P2_points.json` (22 718) and `P1.json`
(4222) were regenerated **with 0 differences** (wall time 1/24/9 s). The other JSONs come from scripts with stated costs
(V5 0.23, c5kev 0.96 CPU-h) and were not rerun.

**C-2: P2 edges (independent recomputation, `p2_edge.out`).**
- The merge100 edges agree exactly at all 10 masses that have them.
- The ds100 edges agree to ≤ 0.7 %. The difference is np.median against the interpolated weighted median, and is
  within the stat errors.
- Only the template half is used (tt_split = 0, in_eta25; 200 events per species-mass). The toy half is used only for
  counts.
- The weight-ratio indexing (`inputs[...][ev_index]`) matches the per-event stored tilts exactly.
- The bootstrap resamples the same events at every Λ, which is correct for crossings.

**C-3: status 4 (108) and status 0 (85).**
- Including them under extreme assumptions (status 4 = merged and thin; status 0 = infinitely thick) leaves every ds100
  edge unchanged. The status-0 events sit at 0.3-0.4 keV, below the 0.47-0.55 keV crossing.
- The merge100 edge moves by ≤ 0.9 % (E1500), well inside the 4 % stat error.
- In the template half there are 34 status-0 and 22 status-4 events. P1 losses are ≤ 1.5 %, in material configurations
  only.
- The exclusion is correct and harmless. `swapped` (10 593 Mac events) is the kernel's automatic in-run label swap at
  nsteps < 1000; those events are valid.

**C-4: P2 systematics.**
- The quadrature of ℓ_max, QED (one-sided, w_qed_19), the 7-point scale, the dynamical scale, CT18/1.645, merging and
  material is as in plan §7. Material uses the own MV points or the maximum over the MV masses (flagged). Closed forms
  carry no material term.
- The largest totals (11 % at F_m1100 ℓ_max-based edges: PDF 7.3 %, ℓ_max 6.6 %) are reweighted-median granularity on 200
  events. They are conservative.
- The F_m800 → F_m900 dip in the ℓ_max edges (−11 %) is template statistics: median γ* − 1 is 0.2525 → 0.1760 in the
  template set, against 0.2256 → 0.1936 in the full Stage-2 rows. Stage 4 should use the edges smoothed in m.

**C-5: merge and cross-machine.** merge.json PASS checks:
- partition disjoint and covering; 4582/4582 files;
- 0 code-md5, input-md5 or job-definition differences; 0 duplicate events;
- totals add up: 204 345 + 14 226 = 218 571 events; 11.996 M + 0.743 M hits; est. M3-CPU 208.4 + 290.1 = 498.5 h.

The cross-machine test is effectively a determinism test (224/225 bit-identical; KS p = 1 trivially). The one 4.4 µm
event is in a material + 10⁻³ job, consistent with libm ulp differences.

**C-6: V7 vacuum.** The literal failure is the eigh floor on the stored value. My SVD re-fit of all P1 B and B2 events
shows the floor has no effect on any P1 number (§1.1). Accepted as documented.

**C-7: V-scale 1/5, V3 and V4.** The legacy one-root-per-chord artefact (V-scale) and the gate items (V3/V4, user
decision §7) are acceptable as documented.

**C-8: V9.** "The samples share some rows, so these pulls are conservative" has the wrong direction. Shared rows
correlate the two medians, so the quoted pulls are *under*-estimated and the test is less stringent. With |pull| ≤ 0.6
the PASS is not in danger. Reword.

**C-9: tags and labels.**
- Every figure carries "Private work (simulation) — truth level". The `fig_label` helper has no experiment label, and
  there is no CMS-type label in any figure, script or document. "truth level" is printed twice per panel (cosmetic).
- The VERIFIED/ESTIMATE/UNVERIFIED usage is otherwise consistent: predictions.json values are UNVERIFIED-transcribed and
  MG re-derivations are ESTIMATE. A-1 is the exception.

**C-10: Stage-1 sample tension at 3 keV (FYI).**
- At 3 keV, E1000, the paired r/c_ev is +2.8 ± 0.9 % (≈ +0.0023). Stage 1 had −0.0003 ± 0.0006 at 1 TeV, k_f = 2, on
  the T3-cache sample: a 2.7σ tension.
- At 500 GeV the sign is reversed (Stage 3 −0.9 ± 1.0 %; Stage 1 +0.0021 ± 0.0015).
- The k_B spectra of the two samples differ, so this is not a contradiction. It is worth a sentence in PROPOSED_CHANGES.

---

## 4. Answers to the specific questions
1. **(a)** Holds at 1-2 keV (population ≈ paired + symmetric-scatter shift, closing to ≤ 0.7 %). The 30-cell average
   and the "uncorrelated with k_B ≥ 6" argument are poorly constructed (B-1). **(b)** Accepted. **(c)** The size is
   VERIFIED. It is consistent with Stage-1 FIX2 and §5.5 and does not contradict the Stage-1 PASS. The floor is **not**
   excluded by the executor's tests. It is excluded as the dominant cause for k_B < 10 by the reviewer's N-dependence
   test and the Stage-1 floor law, but it may be up to ~40 % of the k_B ≥ 10 excess. B* is not isolated (A-1). The c
   estimator is identical to Stage 1's (§1.1).
2. **P1 pulls.** Nothing is tuned (c06 unmodified). The pulls are unpaired and understate the model deviations (B-2).
   The MS-floor numbers are confirmed. The material exponent is in tension with 0.517 at E ≥ 1000 (B-4).
3. **P2 edges.** The definitions, template-only use, bootstrap and systematics propagation are correct (C-2, C-4). The
   coverage sentence and the √m premise need fixing (B-6).
4. **Data integrity.** OK (C-3, C-5). Status 0/4 cannot bias the low-Λ or merging edges beyond 1 %.
5. **Validation failures.** V7 vacuum, V-scale, V3 and V4 are acceptable (C-6, C-7). V8 is misreported and
   mis-diagnosed, and remains a real Stage-4 risk (B-5).
6. **Tags and labels.** OK except A-1 (C-9).
7. **Reproducibility.** Four result JSONs were regenerated with 0 differences (C-1).

**Category A open: A-1. Verdict: ITERATE.**
