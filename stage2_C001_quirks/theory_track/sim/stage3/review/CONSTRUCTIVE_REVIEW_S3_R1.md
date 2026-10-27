# Stage 3 constructive review R1 (C001 theory track; truth-level quirk propagation)

Reviewer: constructive (angle: downstream fitness and publication grade). 2026-10-13.
Classification: `jfc/src/methodology/03-review.md` §6.1. A = correctness error, which blocks. B and C are advisory.
Items tagged **[USER]** are scope decisions for the user, not fixes.

Scratch checks are in `sim/stage3/review/r1_constructive_checks/` (scripts `c*.py`, outputs `c*.out`). They run with
`pixi run python` from `theory_track/`. c5 runs in the ACTS env.

| check | what | main number |
|---|---|---|
| c1 | Λ exponents: measured vs −2 + 2c_ev vs the full MG model (P1.json `exponents`) | 0.6→1 keV: 3.9-5.9σ off −2 + 2c_ev at all 5 points; full model \|d\| ≤ 1.2σ |
| c2 | per-event additivity of B and MS (same rows in B, M, BM) | BM/√(B² + M²) = 0.99-1.00 at 0.45 keV, 0.80-0.95 at 1-3 keV |
| c3 | smoothness of the P2 edges in m | χ²/ndf 11.5/11 … 16.5/11 (quadratic in ln m); d ln Λ_edge/d ln m = 0.25 |
| c4 | V8: hit distance from the nominal surface | max 2×10⁻¹⁰ µm in all 4 files (on-surface hypothesis refuted) |
| c5 | V8: digitiser probe (pyacts 48.0.0) | default `doMerge = True`, `mergeNsigma = 1`; with `doMerge = False`, measurements = SimHits (366/366, 362/362, 356/356) |
| c6 | status-4 / status-0 per (campaign, Λ) | P2 template: ≤ 3/200 per point (E1500, 10-40 keV); status 0 only at 0.3-0.4 keV |
| c7 | paired per-event test of the MG model: median of Δs_B(meas)/Δs_B(model) | E ≥ 500: 0.990-1.002 at 0.6-5 keV; Ẽ500 0.947-0.969 at 1-5 keV; 10 keV +1.6/+2.7 % |
| c8 | Λ sensitivity of the P2 per-point observables | sep_IT ∝ Λ⁻² over 1-30 keV; hits/event, delay and turn-around are flat in Λ |
| c9 | paired model ratio in γ* bins (F500, S500, F1000) | ≤ 0.6 % off for γ* < 1.3; −2 … −5 % at 1.3-1.6; −8 … −11 % above 1.6, the same for both spins |
| c10 | which "expected" shift the V2b figure plots | stratified permutation: corr(obs, x) = 0.999, rms 0.30 % over 30 cells, 5 keV included |

---

## Category A

### A-1 The V2b revisit figure is a near-identity presented as evidence (`figures/p1_v2b_revisit.png`)
**What.**
- The x-axis is `strat_perm_expected_Dc`: r permuted only within c_ev deciles (`p1_results.py` l.151-170, l.370).
- That permutation keeps the conditional distribution of r, including its non-zero conditional median. So
  median(c_ev + r_perm) ≈ median(c_ev + r) by construction.
- c10 confirms this: over the 30 cells, corr(obs, x) = 0.999 and rms(obs − x) = 0.30 %.
- The points sit on the diagonal from −7 % to +17 %. That includes the 5 keV cells (+9 … +17 %), which the text says are a
  **real** B* law failure (VALIDATION §8 item 4, PROPOSED_CHANGES §1 item 3).
- README l.178 captions it "population excess vs the median shift expected from the per-event scatter".

So the figure tells a reader that every excess, 5 keV included, is an estimator effect. That contradicts the conclusion
and is a tautological comparison (§6.4). The text's own argument is not affected: it uses the zero-median symmetric
model (`zero_median_symmetric_scatter_Dc`, +1.2 … +2.9 % at 0.6-3 keV), and that model is not tautological.

**Fix (cheap, re-plot only).**
- Put `zero_median_symmetric_scatter_Dc` on the x-axis. The 0.6-2 keV cells should then lie near the diagonal (c10:
  observed vs symmetric model at 1 keV is 0.7/2.0/1.1/2.1/3.2 % vs 2.1/1.9/1.7/1.9/2.9 %). The 0.45 keV cells and the
  3-5 keV high-k_B cells should stand off it, and that offset is the informative statement.
- Optionally show the stratified permutation as a grey identity check, labelled as such.
- Update the README caption and the auto-text in `make_docs.py` l.69 if the wording depends on the plot.

---

## Category B (advisory)

### P1: B-field coplanarity physics and the P-10 rewording

**B-1 P-11 (Λ exponent) is reported selectively. The −2 + 2c identity fails at 0.6-2 keV where the ℓ_max ~ R_IT terms act (c1).**
- PROPOSED_CHANGES §2 lists the 1→2, 1→3, 0.45→0.6 and 5→10 keV slopes. It omits 0.6→1 keV. There the median per-event
  slope is −1.88 … −1.95 against −2 + 2c_ev = −1.76 … −1.80, which is **3.9-5.9σ off at all 5 points**.
- In the same interval the full MG rotating-yo-yo population slope agrees (|d| ≤ 1.2σ; e.g. E500 −1.879 ± 0.061 vs model
  −1.893).
- 1→2 keV: E1500 is 4.1σ off and Ẽ500 4.5σ, while E200-E1000 are ≤ 1.2σ.
- 1→3 keV: "within 0.03" is 2.3-3.9σ at E200/E1000/E1500/Ẽ500.
- The size of the deviation follows ℓ_max: the points with the highest ℓ_max = R_IT edge (E1500 0.78 keV, Ẽ500 0.78 keV)
  deviate most at 1-2 keV. So −2 + 2c is the asymptotic (ℓ_max ≪ R_IT) exponent. The finite-tracker terms are in the
  full model but not in the closed form.
- The same reading fits the 0.45 keV failure of c (ℓ_max ≳ R_IT, few oscillations inside the tracker). PROPOSED_CHANGES
  instead attributes that failure to "non-secular b_odd ∝ m/Λ⁴ terms", which is an ESTIMATE and is not tested.
- A referee will ask for the validity window in dimensionless terms, not in keV for one detector.

Fix:
- Give every interval in P-11, with pulls against −2 + 2c_ev and against the full model.
- State the window as ℓ_max/R_IT (or the in-tracker oscillation count) and k_B, not keV.
- Tag the 0.45 keV attribution as ESTIMATE and name the alternative.

**B-2 P-9 rests on unpaired pulls with little power. The paired test is sharp and should be the paper statistic (c7, c9).**
The unpaired median errors are about 5-7 %, so "|pull| ≤ 1.7 everywhere" hides 5-10σ paired structure. Paired per-event
Δs_B(meas)/Δs_B(model) gives:
- E ≥ 500 fermions: 0.990-1.002 at 0.6-5 keV (0.980-1.001 at 0.45 keV).
- E200: 0.966/0.975 at 0.45/0.6 keV, and 0.986-0.990 at 1-5 keV.
- Ẽ500: 0.986 at 0.6 keV, then 0.969/0.954/0.947/0.952 at 1/2/3/5 keV.
- c9 shows the cause is γ*, not spin. The ratio is within 0.6 % for γ* < 1.3. It is 0.98/0.96 (F/S) at 1.3-1.6 and
  0.92/0.89 above 1.6, for both species. The scalar sample has the higher γ* (median 1.44 vs 1.27).
  Ẽ/E = 1.15 ± 0.10 vs 1.16 (P-24) is therefore a weak test, and the paired one is the useful one.
- **Above 5 keV:** the paired ratio is 1.001 (E500) and 1.008 ± 0.002 (E1000) at 7 keV, and 1.016 ± 0.005 / 1.027 ± 0.005
  at 10 keV. The unflagged events alone give 1.019 / 1.033. So the excess is **not** carried by floor-flagged events.
  This turns part of the "unattributed ±5 %" (P-9) into a measured, positive +1-3 %, the same sign as the 5 keV c
  excess.
- The paired 5→10 keV slope, 4.0-5.5σ off −2 + 2c, is the same effect.

Fix:
- Report the paired ratio per cell and per γ* bin as the P-9 evidence.
- Restate the 7-10 keV systematic as measured (+1-3 %, floor-independent) plus the residual unattributed part.
- Keep the unpaired pulls only as a secondary column.

**B-3 R(1/2) is c restated, not an independent confirmation.**
- R(1/2) = 2Δs(B₀/2)/Δs(B₀) ≡ 1 + c2 ln 2. For example (1.0737 − 1)/ln 2 = 0.1063, which is the measured c.
- README headline 3 and PROPOSED_CHANGES (P-13/P-14 "Agrees") present it as separate support.
- At E500 1 keV it is 1.0737 ± 0.0007 vs 1.072, i.e. 2.4σ. That is the same +2 % that fails the literal V2b criterion
  for c.

Fix: say "R(1/2) ≡ 1 + c ln 2 (not independent of P-10)", and quote the pull, not "agrees".

**B-4 How B and MS combine is not stated, and a referee will ask (c2).**
- Option (b) treats MS as a measured floor. The paper sentence "MS dominates from ≈ 1.5-2 keV" still needs a combination
  rule.
- Per event (same rows): Δs_BM/√(Δs_B² + Δs_M²) = 0.99-1.00 at 0.45 keV, 0.95-1.00 at 0.6 keV and **0.80-0.95 at
  1-3 keV**. So the sum is sub-quadrature in the crossover region, consistent with the two rotations acting on the same
  axis.
- The crossover Δs_B = Δs_MS falls at ≈ 1.2 keV (E1500), 1.3 (E1000), 1.5 (E500), 1.6 (Ẽ500) and 1.9 keV (E200), from
  the README medians.
- The MS exponent at E1000 is 0.36-0.38 ± 0.07, 2-2.5σ below 0.517.

Fix:
- One sentence plus one panel: Δs_BM vs the quadrature sum.
- Give the crossover as mass-dependent, 1.2-1.9 keV.
- Quote the measured MS exponents and credit Highland only for the √(x/X₀) expectation.

**Is the P1 evidence now sufficient for a paper statement?** Yes, for a re-scoped one, after A-1, B-1, B-2 and B-3. The
observable an experiment sees is Δs at B₀ (c needs two fields), so the publishable content is:
1. The full rotating-yo-yo model predicts Δs_B per event to ≤ 0.6 % for γ* < 1.3 and to −2 … −11 % above, at 0.45-7 keV
   on realistic MG spectra.
2. The closed-form c law holds in the conditional median for ℓ_max ≪ R_IT and k_B ≲ 4 (0.6-2 keV here).
3. The B* term gives a measured positive excess at high k_B. Its mechanism is open.
4. The MS floor takes over at 1.2-1.9 keV.

The window where B physics is visible above the MS floor (≲ 1.5 keV) largely overlaps the window where the law is
verified. That is a strong framing.

**Is the P-10 rewording honest and sufficient?** It is honest on c itself: conditional vs population, the 0.45 keV
failure, the 3-5 keV B* excess, and stability. It is **not sufficient as a package** because of B-1 (omitted interval and
untested attribution), B-2 (P-9 left on weak evidence) and B-3 (R(1/2) double count).

### Stage 4 handover

**B-5 The V8 "digitiser loses hits" is the ACTS default merging, not a loss (c5). It is resolved, but the documents need
changing.**
- `DigitizationAlgorithm.Config()` in pyacts 48.0.0 defaults to `doMerge = True`, `mergeNsigma = 1.0`. Smeared
  measurements on the same surface within 1σ (here 14.4 µm, the generic 50 µm/√12) are merged.
- In V8 each Stage-3 surface is one ACTS surface, i.e. a whole cylinder or disc. So the merged pair's close hits, and
  repeated crossings, merge.
- With `doMerge = False` the counts are exact: 366/366 (10 keV), 362/362 (15 keV), 356/356 (30 keV), with T3V excluded.
- Unique per-event barcodes change nothing (variants A = B).
- The hypothesis in VALIDATION §5 and HANDOVER §4 ("repeated crossings … the digitiser does not keep") is therefore
  wrong as stated. The V8 PASS criterion n_meas = n_simhits only tests this flag.

Fix:
- Rewrite VALIDATION §5 and §9 item 5 and HANDOVER §4 with this cause, and close the open item.
- Stage 4 must set `doMerge` explicitly (see U-5).

**B-6 The injected SimHits deposit zero energy.**
- val_v8 builds SimHits with p4_before = p4_after, so `depositedEnergy()` is 0.
- Smearing digitisation does not care. Geometric (channelised) digitisation with a charge threshold, which is what the
  CMS-like IT/PS/2S segmentation in INSTALL_CHECK §3 needs, would drop or mis-weight every quirk hit.

Fix: add to HANDOVER §1/§4 that Stage 4 builds p4_after with E reduced by `h_dE` (|p| kept on shell). Optionally add
Landau fluctuations; `h_dE` is the mean Bethe loss.

**B-7 The geometry contract for Stage 4 is implicit.**
- Stage-3 hits lie on the simplified cylinders and discs to 2×10⁻¹⁰ µm (c4). INSTALL_CHECK §3 plans to "intersect
  T3_causal chords with the module planes (17 092 modules)", but no trajectories are stored.
- Straight-line extrapolation from the cylinder to a module plane is not safe for quirks. The plane-cylinder sagitta is
  w²/8R ≈ 1.7 mm on TBPX L1. The string force σ ≈ 5 GeV/mm × (Λ/keV)² bends the track by O(10 µm) over that distance at
  1 keV, and by more at higher Λ (ESTIMATE).

Fix:
- State in HANDOVER §2 that Stage 4 must use the **same simplified surfaces** as sensitive surfaces, for the Fatras PU-200
  hits too, so that quirk and PU hits share one geometry (D1 (a)).
- Note that each cylinder is then one digitisation "module", which matters for merging and clustering.
- Module planes mean a rerun (plan D1 (b)): see U-4.

### P2: Λ edges and per-point observables as measurement inputs

**B-8 The six edges carry about two pieces of information. The continuous Λ meter is missing from the deliverable (c3, c8).**
- ℓ_max = R_IT and ℓ_max = 100 µm are the same median ℓ_max at two thresholds: identical m-slope 0.249 and a constant
  ratio.
- merge100 and merge25 are thresholds on the IT pair separation sep_IT ≈ 0.57 ℓ_max.
- The thickness edge is the only one tied to ε_B (B + MS).
- Among the per-point observables:
  - sep_IT scales as Λ⁻² cleanly from 1 to 30 keV (E1000: 38.5 mm → 9.3 mm → 0.37 mm → 95 µm at 1/2/10/20 keV), i.e.
    it measures ℓ₀ = m/Λ² as the degeneracy theorem (S-4) says;
  - Δs_all carries Λ only below ≈ 1.5 keV;
  - tracker hits/event, the maximum hit delay and the turn-around fraction are flat in Λ (they carry m via the
    velocities).
- A reader of the P2 table could take the edges for independent measurements.

Fix:
- Frame the Stage-3 P2 product as a sensitivity map: which observable carries Λ, m or ℓ₀ in which range, plus per-event
  templates.
- Add median sep_IT vs Λ to `p2_observables.png`.
- Mark the edge pairs that are the same quantity.
- Note that below ≈ 1.5 keV Δs_B (Λ only, m-flat) together with sep_IT (ℓ₀) breaks the degeneracy without the recoil,
  consistent with the S-4 "B only" row.

**B-9 The systematic shifts are dominated by the granularity of medians.**
- Example: F_m1100 `pdf_ct18_68cl` on ℓ_max = 100 µm shifts by +1.93 / +0.078 keV (7 % one-sided), and that edge's total
  is 11 %.
- PDF reweighting cannot move the γ* spectrum by 7 %. Reweighting 200 events moves the median across a gap between
  neighbouring events. The README says so (ESTIMATE), but the numbers are still added in quadrature into the totals.

Fix:
- Evaluate each shift with a smooth quantile estimator (e.g. Harrell-Davis), or on the smooth-in-m edge fit (c3), and give
  each shift its MC error (paired bootstrap of the shift).
- Symmetrise, or drop shifts < 2σ_MC.
- A measurement would also need the stat-syst correlation, since both use the same 200 events.

**B-10 The merged regime has toys at only 2 masses, so coverage cannot be tested elsewhere (c6).**
- At Λ ≥ 15 keV only E1000 and E1200 have toys (200 each). The other 5 masses and Ẽ have templates only.
- 200 toys give about 6 independent N = 30 pseudo-experiments per point. Bootstrapped pseudo-experiments are correlated.

Fix: for P2 closure, use template ↔ toy swap (cross-validation, free) where both exist, and state that merged-regime
coverage is tested at E1000/1200 only. More toys: U-3.

**B-11 Interpolation in m: the "√m" claim and the D5 interpolation are not borne out (c3).**
- README headline 6 and HANDOVER §5 say the ℓ_max = R_IT edge "scales as √m". The fitted d ln Λ_edge/d ln m is 0.249 for
  the ℓ_max edges and 0.248 for merge100 (E200→1500: ×1.8 and ×1.55, against ×2.7 for √m).
- VALIDATION §9 item 8 says the missing merging edges "come from interpolation in m (D5 option B)". The README table shows
  n/a at those 7 masses, and P2.json contains no interpolated value.
- The edges are smooth in m within stat (quadratic in ln m: χ²/ndf = 11.5/11 for ℓ_max, 4.6/4 for merge100), so the
  interpolation is feasible.

Fix:
- Replace "√m" with the measured slope.
- Either produce the D5 interpolated merge100 edges (flagged "interpolated", with the fit covariance) or correct §9
  item 8.
- Give the smooth parametrisation ln Λ_edge(ln m) with covariance as the P2 input.

---

## Category C (advisory, minor)

- **C-1 Figures for a phenomenology reader.**
  - Legends use code identifiers (`lower_Nosc1_closed`, `F_m200`, `S_m500`). Units are written "um", and "Etilde" and
    "Delta s_B" appear as plain text.
  - "truth level" appears twice per panel (top left and right).
  - No CMS-type label anywhere: good. "Private work (simulation) -- truth level" is appropriate.
  - Fix: use physics labels (N_osc = 1, ℓ_max = R_IT, Δs = 100 µm, …), µm, Ẽ, Δs_B (LaTeX), one truth-level tag, and
    2-line captions. Already deferred to Stage 5; listing it so it is not lost.
- **C-2 VALIDATION §0 is opaque outside the project.** It is full of internal IDs and jargon (V1-V9, eigh floor, status-4,
  legacy recorder, max_boost, T3V). Fix: a 5-line plain-language preface, saying what was propagated, what passed, the two
  physics findings and the open item. Also mark which literal FAILs are criterion-vs-floor artefacts (V7 vacuum, V3) and
  which are physics (V2b).
- **C-3 The MS crossover is stated as "≈ 1.5-2 keV"** (README headline 5, NEAR_MISS §0 item 6). It is 1.2-1.9 keV and
  falls with mass (B-4).
- **C-4 Status 4 biases the merging edge one way.**
  - These are near-threshold pairs (γ* − 1 ≤ 0.01, ℓ_max ≪ 100 µm, so physically merged), dropped at ≤ 3/200 per point
    (E1500 10-40 keV).
  - Worst case Δf = 0.015 with df/d ln Λ ≈ 0.78 shifts the E1500 merge100 edge up by ≈ 1.9 %, below its 4 % stat.
  - P1 material cells: ≤ 3/300, negligible.
  - Fix: count them as merged in f_merged (closed-form ℓ_max), or list a one-sided systematic.
- **C-5 Status 0 has limited impact.** It occurs only at 0.3-0.4 keV (34 template events in the counting set, ≤ 4/200 per
  point). The edges are unaffected: N_osc = 1 is closed form, and the Δs = 100 µm edge sits at 0.47-0.55 keV. Only the
  late-time hit and hit-count observables at 0.3 keV are affected. Say so in HANDOVER §0.
- **C-6 V-scale ran the legacy recorder.** The production s3 recorder is untested on the P-25 scaling identity, which
  underpins the "B₀/2 at 5 keV = per oscillation 7.1 keV" reading. Rerun the 5 events with the s3 recorder (< 0.01 CPU-h).
- **C-7 The model returns 0 for a few events** (`p1_model_mg.npz`: 5 events, e.g. F_m1000 0.45 keV, where model = 0 and
  measured = 58 µm). Check the c06 edge case; medians are unaffected.
- **C-8 V8 bookkeeping.** The T3V hits (92-113 per file) are injected and digitised, and are counted in the V8
  measurements. Stage 4 should filter them before digitisation. Use one ACTS event per physics event with per-event
  barcodes for truth matching.
- **C-9 Interpolate templates in degeneracy variables.** With S-4, vacuum observables depend on (m, Λ) only via ℓ₀ = m/Λ²
  and the velocities. Interpolating templates in (ℓ₀, ε_B, m) rather than (m, Λ) should cut interpolation error; sep_IT ∝
  Λ⁻² already shows it.
- **C-10 Label the merging thresholds.** Label the 100/25 µm thresholds "truth-level pair separation" and note that the
  physical merging edge is set in Stage 4 by IT clustering (25 × 100 µm²). Merging in a 2D pixel grid is anisotropic.
- **C-11 Open-item bookkeeping.** HANDOVER §5 item 3 copies "merged at 100 µm at 13-25 keV". Add that this is
  sep_IT-median based and that the 25 µm edge exists at 3 masses only.

---

## Data quality: can it bite P1 or P2?
- **108 status-4 events:** no for P1 (vacuum/B-only configurations have none; material cells ≤ 1 %). Marginal for P2, as
  a one-sided ≤ 2 % on the E1500 merging edge (C-4).
- **85 status-0 events:** no for the edges or P1. Only for late-time observables at 0.3 keV (C-5).
- **V7 vacuum (eigh floor 0.015 µm):** no. The smallest quoted B-only value is 0.445 µm, giving a ≤ 0.06 % effect.
- **V-scale 1/5:** no for the numbers. It is a legacy-recorder artefact, but the identity check should be redone on the
  production recorder (C-6).
- **V3/V4 literal:** no for P1 (P1 runs at 10⁻³; the two failing B-only cells are at 10⁻²).
- **Floor-flagged events at 7-10 keV:** they do not drive the 10 keV excess (B-2: unflagged 1.019/1.033).

## Scope decisions for the user [USER]
- **U-1 P1 claim above 3 keV.**
  - (a) Publish the B* excess as a measured, empirical result (k_B-binned table, step- and round-off-stable) with the
    mechanism open, and restrict the closed-form claims to ℓ_max ≪ R_IT and k_B ≲ 4.
  - (b) First derive or fit ΔK(k_B, ε, γ*) (NEAR_MISS §10). This adds weeks.
  - Recommendation: (a).
- **U-2 Non-additivity of B and MS in P1** (B-4): add one measured panel (stays within option (b)), or leave MS purely as
  a floor number.
- **U-3 Merged-regime coverage for P2** (B-10): accept toys at E1000/1200 only, or run toys at 2-3 more masses and Ẽ500 at
  15-40 keV. Cost: ≈ 0.03 CPU-h/event at Λ ≥ 15 keV (SAMPLES: p2_hi 323 CPU-h / 10 891 events), so ≈ 25 CPU-h per
  mass for 200 events × 4 Λ (ESTIMATE). The 25 µm edge needs Λ > 40 keV at most masses.
- **U-4 Stage-4 geometry** (B-7): the simplified surfaces as sensitive surfaces (D1 (a); no rerun), or module planes
  (D1 (b); rerun the Stage-4 subset with a module-plane recorder).
- **U-5 The Stage-4 digitisation model in the merged regime** (B-5): geometric digitisation with CMS-like pitch and
  clustering (the physical merging), or smearing with `doMerge = False` (no merging). The default `doMerge = True` at
  1σ = 14.4 µm on whole-cylinder "modules" matches neither.

## Verdict
**ITERATE (minor): one Category-A item, cheap to fix.** A-1 is a re-plot plus caption with the non-tautological
zero-median scatter model on the x-axis. Once it is fixed, Stage 3 is fit to advance to the user checkpoint Stage 3 → 4:
- The production is complete, cross-machine-consistent and reproducible.
- The P1 and P2 numbers trace to the JSON. Every spot check in c1-c10 reproduced the quoted values.
- The V8 open item is resolved (B-5).

B-1, B-2 and B-3 should be done before any P-10/P-11 text goes to `analytic/` or a paper draft. B-5, B-6 and B-7 should
go into HANDOVER_STAGE4.md before Stage 4 starts. B-8 to B-11 are needed before P2 uses the edges as measurement inputs.
Totals: 1 A, 11 B, 11 C, 5 user decisions.
