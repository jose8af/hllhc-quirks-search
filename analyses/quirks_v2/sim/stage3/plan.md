# Stage 3 plan: T3_causal propagation of the Stage-2 samples (≥ 200 effective events per grid point)

E6 (executor), 2026-10-11. **Plan only: nothing in production has run.** Probes: `probes/` (p0-p7), outputs
`../../data/sim_stage3/probes/` (22 MB). Status: plan complete, awaiting the user's review (decisions D1-D16, §8).
Tags: VERIFIED = measured here (probe timings, convergence) or two independent checks; ESTIMATE = our closed form, model or
extrapolation; UNVERIFIED = transcribed and not re-derived. Everything is truth level.

## 0. Summary
1. **Grid.**
   - *P1* (B-field physics, Stage-1 conventions: |η_pair| < 1, vertex at the origin, barrel Δs): E 200/500/1000/1500 and
     Ẽ 500 × Λ = 0.45, 0.6, 1, 2, 3, 5, 7, 10 keV. Configurations: B (Δs_B), B/2 (c), V, M (MS floor), BM, and material
     ×0.5/×2 at 1 and 3 keV.
   - *P2 + Stage-4 input* (|η_pair| < 2.5 or < 4 (D10), luminous-region vertex, barrel + stacked OT sensors + discs, B +
     nominal material): E at all 14 masses and Ẽ 200/500/1000. Λ: a dense lower band 0.3-1.2 keV (10 points), interior
     1.5-10 keV (6), upper 15/20/30 keV, and 40 keV for E ≥ 1000 and Ẽ ≥ 500 GeV. At Λ ≥ 15 keV the recommended option runs
     7 E masses + Ẽ.
   - *Edge placement* (§1.1): the lower edge is set by N_osc < 1 at 0.29-0.33 keV (m independent), Δs_B = 100 µm at
     ≈ 0.5 keV, and ℓ_max = R_IT at 0.47-0.78 keV (E) / 0.62-0.95 keV (Ẽ), which scales as √m. The upper edge is merging,
     ℓ_max = 100 µm at 17.8-29.7 keV (E, ∝ √m); there the B-only b_odd/ℓ₀ falls to the 3×10⁻⁸ double-precision floor.
2. **Events.**
   - ≥ 200 effective events everywhere, using the loader's deterministic unweighting (N_eff = N; the CPU-optimal choice).
   - P2: 200 template + 200 toy (pool for N_sig ≈ 30 pseudo-experiments).
   - P1: 300 events (200 at 7-10 keV).
   - Selection: TRGS, p_T(QQ̄) > 200 GeV (the L1-MET proxy). The same rows are used at every Λ.
3. **Scaling.** (Λ√k, B) ≡ (Λ, B/k) per oscillation. It saves no CPU for full events (N_osc is invariant and the cost per
   oscillation is scale-free), and none for any configuration with material. It is used only as a validation identity and
   to make the precision-floor test cheap.
4. **Kernel and schema.**
   - `code/T3_causal.py` is not sufficient for Stage 4: it has barrel radii only, one root per chord, no momentum direction,
     the vertex fixed at 0, and no disc material.
   - Proposal: a versioned copy `sim/stage3/code/T3_causal_s3.py` with a `legacy` switch that must be bit-identical to the
     original. It adds generic surfaces with all roots, hit 4-momenta, the vertex, disc material, and a bit-identical
     material fast path (×1.2).
   - Output: one npz per point/configuration (CSR hits in mm/ns/GeV, per-event truth, weights, systematic weights,
     plane-fit observables).
5. **Validation (V1-V9):** bit-identity with T3_causal, Stage-1 numbers on the same events, the c law on the MG sample
   (criteria fixed now), step and floor tests, R1 conformal cross-check, T2-cache continuity, reproducibility, ACTS
   ingestion, weighted vs unweighted.
6. **Compute** (measured per-event costs; ESTIMATE totals; §6):
   - recommended ≈ 330 CPU-h ≈ 47 h on 7 workers (range 250-460 CPU-h); full option ≈ 615 CPU-h (3.7 d);
   - B+M costs 5-10× B at ≥ 20 keV because of the per-step MS kicks, so 30/40 keV dominate (≈ 108 of the 167 CPU-h at
     Λ ≥ 15 keV);
   - max_boost 10⁻² is converged to ≲ 1 µm for hits at ≥ 2 keV; 3×10⁻² is rejected;
   - disk ≈ 2 GB (≤ 5 GB); memory < 2 GB.
7. **Systematics:** the tail rate as a normalisation; ℓ_max ±5 % and QED −1.1 ± 0.8 % as reweighting tilts in γ* (no
   re-propagation); scale/PDF/merging as stored weight ratios; material ×0.5/×2 by re-propagation at a subset.
8. **Decisions D1-D16** in §8. The main ones: D1 surface model, D4 disc material, D5 high-Λ coverage, D10 |η| acceptance,
   D12 the optional floor test.

## 1. Grid

### 1.1 Physics scales that place the Λ points (probe 2, `p2_edges.json`; ESTIMATE: closed forms on the Stage-3 selection)
Closed forms [T2 §2.2; synthesis Box B]: ℓ_max = 2(γ*−1)m/σ, σ = 50.68 GeV/cm (Λ/keV)²; N_osc = σR_eff/(2β*p_T) with
R_eff = min(108.3 cm, 265 cm/|sinh η_pair|); b_odd/ℓ₀ = 2ε⊥[γ* − asinh ρ/ρ] (P-1, c06 `pair_params`). Selection: TRGS,
p_T(QQ̄) > 200 GeV, |η_pair| < 2.5, template half, weighted.

| species, m [GeV] | median x = 2(γ*−1) | Λ where median N_osc = 1 | f(N_osc < 1) at 0.3/0.4/0.5 keV | Λ where median ℓ_max = R_OT (108 cm) | **= R_IT (14.6 cm)** | **= 100 µm** | = 25 µm | median b_odd/ℓ₀ at 10/20/30 keV | f(b_odd/ℓ₀ < 10⁻⁷) at 10/20/30 keV |
|---|---|---|---|---|---|---|---|---|---|
| E 200 | 0.80 | 0.290 | 0.45/0.12/0.02 | 0.17 | 0.47 | 17.8 | 35.5 | 8.8e-7/2.2e-7/9.8e-8 | 0.03/0.20/0.51 |
| E 300 | 0.69 | 0.297 | 0.49/0.14/0.03 | 0.19 | 0.53 | 20.2 | 40.3 | 5.0e-7/1.3e-7/5.6e-8 | 0.10/0.42/0.73 |
| E 500 | 0.55 | 0.298 | 0.49/0.15/0.03 | 0.22 | 0.61 | 23.2 | 46.5 | 3.2e-7/7.9e-8/3.5e-8 | 0.17/0.59/0.94 |
| E 700 | 0.46 | 0.296 | 0.48/0.16/0.04 | 0.24 | 0.66 | 25.2 | 50.4 | 2.0e-7/5.0e-8/2.2e-8 | 0.24/0.77/0.96 |
| E 1000 | 0.39 | 0.295 | 0.48/0.17/0.04 | 0.27 | 0.73 | 27.7 | 55.4 | 1.3e-7/3.3e-8/1.5e-8 | 0.37/0.91/0.99 |
| E 1200 | 0.34 | 0.290 | 0.45/0.15/0.03 | 0.27 | 0.75 | 28.5 | 57.1 | 9.3e-8/2.3e-8/1.0e-8 | 0.52/0.96/0.99 |
| E 1500 | 0.30 | 0.288 | 0.45/0.14/0.04 | 0.29 | 0.78 | 29.7 | 59.4 | 8.0e-8/2.0e-8/8.9e-9 | 0.60/0.97/1.00 |
| Ẽ 200 | 1.41 | 0.323 | 0.61/0.19/0.04 | 0.23 | 0.62 | 23.6 | 47.2 | 1.2e-6/3.0e-7/1.3e-7 | 0.01/0.10/0.34 |
| Ẽ 500 | 0.97 | 0.330 | 0.64/0.25/0.07 | 0.30 | 0.81 | 30.9 | 61.9 | 4.7e-7/1.2e-7/5.2e-8 | 0.07/0.43/0.79 |
| Ẽ 1000 | 0.66 | 0.330 | 0.64/0.24/0.06 | 0.35 | 0.95 | 36.2 | 72.4 | 1.8e-7/4.4e-8/2.0e-8 | 0.25/0.83/0.97 |

**Lower edge (mass dependent).** Four scales meet between 0.3 and ≈ 1 keV:
1. *N_osc < 1.* Half of the triggered pairs make less than one oscillation inside the tracker at 0.3 keV (m independent,
   since N_osc ≈ 11-12 (Λ/keV)²; Ẽ 9.2-9.6). Below ≈ 0.3 keV the pattern is two opposite arcs, not a quirk pattern, and the
   HSCP/out-of-time channels take over (Box A). **0.3 keV is the lowest point.**
2. *B thickness at the truth-level cut.* Δs_B ≈ 30 µm (keV/Λ)^1.8, m independent (S-3), reaches 100 µm at ≈ 0.5 keV: the
   truth-level finder edge 0.45-0.7 keV (Box A).
3. *ℓ_max against the Inner-Tracker lever arm.* With realistic resolution the coplanarity test is carried by the 4 IT
   layers at r ≤ 14.6 cm (S-2). When the median ℓ_max exceeds R_IT the pair has not turned around inside the IT, and the IT
   sees two prompt-looking arcs. This crossover scales as √m: **Λ_IT = 0.47 → 0.78 keV (E 200 → 1500) and 0.62 → 0.95 keV
   (Ẽ)**. It is the scale that makes the realistic (Stage 4) edge mass dependent, and where Stage 4 needs dense points. The
   non-secular first-order terms (b_odd ∝ m/Λ⁴, the origin of the formula edge Λ_low ∝ m^{1/4}) matter in the same range
   (NEAR_MISS §10 item 5).
4. *Precision floor: irrelevant here.* ε_B ≥ 2×10⁻⁴ and b_odd/ℓ₀ ≥ 10⁻⁵ for Λ ≤ 1 keV.

A common dense band **0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.85, 1.0, 1.2 keV** (Δ ln Λ = 0.13-0.2) covers all four scales
for every mass: it puts ≥ 4 points within ±30 % of each mass's Λ_IT and ≥ 3 points across the N_osc edge. The band costs
less than 1 % of the total (§6), so making it mass-specific would save nothing. In the mass-scaled variable u = Λ/Λ_IT(m) the
band spans u = 0.38-2.6 at 1500 GeV and 0.64-2.6 at 200 GeV, so the density in u is the same where the edge sits.

**Upper edge (mass dependent).**
1. *Merging.* The median ℓ_max equals 100 µm (IT long pitch, PS strip pitch) at **17.8 → 29.7 keV (E 200 → 1500)** and
   23.6-36.2 keV (Ẽ), and 25 µm (IT short pitch) at 35-59 keV. Between the two the pair becomes one IT/PS cluster, the
   merged 9-21× MIP object of S-10. This upper edge also scales as √m.
2. *The B thickness is below the double-precision floor there.* At 20 keV the median b_odd/ℓ₀ is 2×10⁻⁸-2×10⁻⁷, and at
   30 keV 9×10⁻⁹-10⁻⁷, against the floor b/ℓ₀ ≈ 3×10⁻⁸ (γ* ≤ 1.3; 10⁻⁶ at γ* ≥ 2) [NUMERICS §1.3]. A B-only Δs_B at
   ≥ 20 keV is **not computable in double precision**. In B+M the thickness is MS dominated (12-30 µm), so the floor does not
   affect the hit positions at the µm level. Each event carries a `floor_flag`.
3. *NG validity:* b_odd Λ ≈ 1 at 26 keV (typical events); model uncertainty on Δs_B 3-8 % at 30 keV (P-18), irrelevant
   once MS dominates.
Grid: **15, 20, 30 keV at every mass, plus 40 keV where Λ_100µm ≥ 27 keV (E ≥ 1000 GeV, Ẽ ≥ 500 GeV)**, so that the
merging edge is bracketed on both sides at every mass. 40 keV costs about twice 30 keV (§6; D6).

**Interior:** 1.5, 2, 3, 5, 7, 10 keV (the resolved-arc → aliased-band transition at 1-3 keV, S-7; the MS-dominance onset
at ≈ 1.5-2 keV, S-2).

### 1.2 P1 grid (B-field physics; truth level; Stage-1 conventions)
- **Selection:** |η_pair| < 1, vertex at the origin, Δs on the 10 barrel layers through the origin (the Stage-1 observable,
  NEAR_MISS §1.3), so P1 numbers compare directly with Stage 1 and T3.
- **Masses:** E 200, 500, 1000 (the Stage-1 masses, where C = 0.43/1.23/1.62 is predicted), E 1500 (the m-independence
  statement over the full Stage-2 range), Ẽ 500 (P-24: scalar prediction Δs_B 36 vs 31 µm at 1 keV, ESTIMATE).
- **Λ:** 0.45, 0.6, 1, 2, 3, 5, 7, 10 keV. 0.45 tests where the secular law should start to fail (non-secular Λ⁻⁴ terms);
  1-5 keV is the verified/consistent range of the law; 7 and 10 keV are the unattributed ±5 % region (NEAR_MISS §5.5),
  where the result is quoted with that systematic and the floor flag (37-60 % of 1000-1500 GeV events have
  b_odd/ℓ₀ < 10⁻⁷ at 10 keV). No B-only point above 10 keV (floor, §1.1).
- **Configurations** (same events in all):

| cfg | field | material | max_boost | Λ | purpose |
|---|---|---|---|---|---|
| B | B₀ = 3.8112 T | off | 10⁻³ | all | Δs_B, the headline law (P-9) |
| B/2 | B₀/2 | off | 10⁻³ | ≤ 5 keV | local slope c per event (P-10), R(1/2) (P-13); converged and floor-free to 5 keV (NUMERICS §13.2) |
| V | 0 | off | 10⁻³ | 1, 3 keV | Δs ≡ 0 sanity; reference for in-plane/out-of-plane hit displacements |
| M | 0 | nominal | 10⁻² | all | MS floor Δs_MS (the measured floor of option (b)) |
| BM | B₀ | nominal | 10⁻² | all | realistic Δs_B+M; where MS takes over |
| M×0.5, M×2, BM×0.5, BM×2 | as above | ×0.5, ×2 | 10⁻² | 1, 3 keV | √(x/X₀) scaling of the floor (nearly Λ independent, S-2); T3-material systematic |

  The B/2 run at Λ is, per oscillation, the B₀ law at Λ√2 (§3), so the B/2 set also spans the B₀ law to ≈ 7 keV per
  oscillation without the cumulative B* part.
- **Events:** 300 per point at Λ ≤ 5 keV (c to ≈ ±0.0015, scaled from Stage 1's ±0.002 with 120 events), 200 at 7 and
  10 keV. Template half at E 200/500/1000 and Ẽ 500 (640-775 and 350 unweighted |η| < 1 events available); both halves at
  E 1500 (168 + 157 available; P1 is not a template fit). Cost 56 CPU-h (§6.4).

### 1.3 P2 grid and Stage-4 truth input
- **Selection:** |η_pair| < 2.5 (or < 4, D10), smeared vertex (luminous region σ_z = 45 mm, σ_t = 190 ps, σ_xy = 5 µm;
  `cms_phase2_public.json` beamspot), all surfaces (barrel, stacked OT sensors, discs), configuration **BM** (nominal
  material), max_boost 10⁻³ for Λ ≤ 1.5 keV and 10⁻² above (§6.3). These files are the Stage-4 input.
- **Species and masses:** E at all 14 Stage-2 masses 200-1500 GeV for Λ ≤ 10 keV; Ẽ at 200, 500, 1000 GeV. For Λ ≥ 15 keV
  the recommended option (B, D5) runs the 7-mass subset E {200, 300, 500, 700, 1000, 1200, 1500} + Ẽ 3 and interpolates in m;
  option A runs all 14 masses (§6.4).
- **Λ:** the 16-point lower+interior set 0.3-10 keV of §1.1 plus 15, 20, 30 keV, plus 40 keV for E ≥ 1000 GeV and Ẽ ≥ 500 GeV:
  19-20 values per mass.
- **Events:** 200 template + 200 toy at Λ ≤ 10 keV; at Λ ≥ 15 keV 200 template (400 at E 1000/1200, the masses near the
  reach) in option B (§2, §6.4).
- **Material systematic:** BM×0.5 and BM×2 at E {200, 500, 1000, 1500} and Ẽ 500 × Λ {0.4, 0.6, 1, 3, 10, 20} keV
  (200 template events); interpolated elsewhere in m and Λ (50 CPU-h; 30 keV would add ≈ 60 CPU-h).

## 2. Events per point and event selection

**Pair-level selection** (Stage-2 conventions; SAMPLES.md):
- sample: the stitched trigger-region files `<P>-TRGS_m<m>.npz` (TRG ∪ INC[p_T,ME < 100 GeV]); `INC` and `LOPS` are not used
  (they are validation samples);
- rows with w > 0 (the loader drops the w = 0 rows kept for the qCut variations);
- **p_T(QQ̄) > 200 GeV**: the L1-MET trigger proxy. The pair deposits ≲ 5 GeV in the calorimeters, so MET ≈ p_T(QQ̄)
  (S-4 (iv), S-18). The MET resolution and trigger turn-on are Stage-4 items;
- |η_pair| < 1 (P1) or < 2.5 (P2/Stage 4). The 2.5 < |η_pair| < 4 region holds 13 % (200 GeV) to 24 % (1500 GeV) of the
  tail cross section and can still leave TFPX/TEPX hits; D10 asks whether to extend the Stage-4 sample to |η_pair| < 4 so
  that Stage 4 can define the fiducial denominator per quirk (Stage-2 DEFERRED handover note).

**Counting.** The loader's deterministic unweighting (`iter_events(..., unweight=True)`, seed 12345) is used: every
propagated event carries the common weight w_max, so N_eff = N. This is the CPU-optimal choice: a weighted run would spend
CPU on rows whose weights spread the Kish N_eff (TRGS tail N_eff/rows = 0.74-0.85), and the INC rows carry 3.7-9.6× the TRG
weight. Rows are taken in file order (TRGS rows are shuffled with a recorded seed, so any prefix is fair), and the same rows
are used at every Λ and configuration. Validation V9 checks the unweighted against the weighted mode at one point.

**Available unweighted events** (probe 0, `p0_event_budget.json`), per half (template/toy):
- |η_pair| < 2.5: 323-349 (E 400), 413-541 (E 600-1500 except 1000), 1048-2444 (E 200, 300, 500, 1000), 636-1277 (Ẽ);
- |η_pair| < 1: 107-168 (E 400-1500 except 500/1000), 640-798 (E 200, 500, 1000), 210-380 (Ẽ).
So 200 template + 200 toy events exist at every P2 point, and P1 needs both halves at E 1500.

**How many events.**
- *Requirement:* ≥ 200 effective events per grid point. **Base: 200 template events at every P2 point.**
- *P2 toys:* the measurement (S-4) is quoted for N_sig ≈ 30 events. With pseudo-experiments drawn from a toy pool by
  resampling, a pool of 200 keeps the overlap between toys small (N_sig/N_pool = 0.15). The 3 ab⁻¹ yields before the
  finder efficiency (p0) are 67 events at 1000 GeV, 24 at 1200, 5.6 at 1500, so N_sig ≲ 30 near the reach. **+200 toy events
  at every P2 point.** At 200-500 GeV (N_sig = 10³-10⁴) toys from a pool of 200 are not valid; there P2 uses Asimov
  templates, and the measurement is MET-scale limited anyway (S-4).
- *Template statistics:* with N_template = 200 and N_sig = 30, the template statistical variance adds ≈ N_sig/N_template
  = 15 % to the fitted-parameter variance (≈ 7 % on σ). Templates at neighbouring Λ use the same events, so morphing in Λ
  pools them. More than 200 template events helps only near the reach; D7 offers 400 template events at E 1000 and 1200
  GeV as an option.
- *P1:* 300 per point (§1.2).

## 3. Classical NG scaling: where it cuts cost and where it cannot

**Statement** (DERIVED, `analytic/checks/c15_scaling.py`; NEAR_MISS §5.5, P-25). With
S = −m Σᵢ∫dτᵢ − σ∫dA + Σᵢ qᵢ∫A·dxᵢ and A = B×x/2, scaling every coordinate by λ at fixed momenta gives
S[λx; m, σ, qB] = λ S[x; m, λσ, λqB]. A vacuum + uniform-B event at (σ, qB, detector D) is therefore the same event, scaled by
λ, as one at (λσ, λqB, D/λ). At a fixed detector this reads (Λ√k, B) ≡ (Λ, B/k) per oscillation, with N_osc larger by k.

**Where it saves CPU.**
1. *Per-oscillation physics of the c law (P1).* A weak-field run at Λ/√k probes the B₀ per-oscillation physics of Λ at a cost
   lower by about k (the cost is ∝ N_osc ∝ Λ², §6), but with N_osc smaller by k. It is valid only for N-independent quantities;
   the cumulative B* part (NEAR_MISS §5.5 (i)) is not reproduced. Stage 3 uses it in one place only: the B₀/2 runs (k_f = 2)
   that measure the local slope c (§1.2) are, per oscillation, the B₀ law at Λ√2. No production point is replaced by a
   scaled run, because the cumulative part is exactly what is unmeasured above 5 keV.
2. *A free validation test (V-scale, §5).* Running (Λ√k, B₀, D) and (Λ, B₀/k, kD) must give hits related by x → x/k up to
   round-off and the step cap hmax (which is not scaled). This tests the step convergence and the hit recorder exactly, at
   no physics cost.
3. *Precision floor tests.* The floor depends only on ε⊥ and b/ℓ₀, which are scale invariant, so it maps identically
   (NEAR_MISS §5.5). Rescaling cannot escape the floor, but it makes the decisive floor test cheap: the per-period part is
   N-independent, so a detector scaled by s = 1/27 suffices (NEAR_MISS §10 item 1(a); optional item O-1 in §8).

**Where it cannot save CPU.**
1. *Exact equivalence does not reduce the number of oscillations.* N_osc = σR/(2β*p_T) is invariant under the map
   (σ → λσ, R → R/λ), and the cost per oscillation is set by max_boost (§6), which is also scale-free. An exactly equivalent
   run costs the same.
2. *Material is not scale-free.* The Highland angle θ₀ ∝ √(x/X₀)/p and the Bethe loss per lab length are fixed in the lab, so
   (Λ√k, B₀, material) is not equivalent to anything at Λ. Every configuration with material (M, BM and all of P2 and the
   Stage-4 input) must run at its true (Λ, B, detector). These configurations dominate the cost (§6).
3. *Mass points do not map onto each other.* By the degeneracy theorem (S-4) hits depend on (ℓ₀ = m/σ, ε_B = qB/σ, the
   velocities, the material, R). Two grid points with the same ℓ₀ have different ε_B, and with the same Λ (same ε_B) have
   different ℓ₀. With B on, no grid point can be generated from another.
4. *The Λ-independence of the kinematics is used, but it saves no CPU*: the same Stage-2 rows are propagated at every Λ
   (`iter_events` in file order), so Λ-to-Λ differences carry no generator noise. That is a statistical gain for the
   templates and edge fits.

## 4. Observables and storage schema

### 4.1 Kernel version for Stage 3 (proposal; `code/T3_causal.py` is not modified)
The hit recorder of `T3_causal.py` is not sufficient for Stage 4:
- it records crossings of the 10 barrel radii (+ BTL, ECAL face) only. For |η_pair| < 2.5 about 70 % of the tail
  cross section has |η_pair| > 1 (`p0_event_budget.json`: σ(|η| < 1)/σ(|η| < 2.5) = 0.28-0.35), so many hits are on the
  TFPX/TEPX/TEDD discs;
- it records one root per chord, so grazing double crossings inside one step are lost (R1 C-1; 2-6 extra hits in 3 of 16
  events with the independent solver);
- a hit stores |p| and β, not the momentum direction or energy, which an ACTS `SimHit` needs (before/after 4-momenta);
- the pair always starts at the origin (no luminous region);
- the tracker material has barrel slabs only. A quirk that leaves through the endcap crosses no disc material
  (`T3_propagator.material_at`: inside r < 118.5 cm, |z| < 293.5 cm only the barrel slabs exist).

**Proposal: a versioned copy `sim/stage3/code/T3_causal_s3.py`** (header: derived from `code/T3_causal.py`, md5 recorded),
with these changes and nothing else:
1. a generic surface table: cylinders (r, z_min, z_max) and discs (z, r_min, r_max), with every root of the chord in
   [0, 1] recorded (two roots per cylinder when the chord dips across r; one per disc);
2. per hit: surface id, quirk, crossing index on that surface, t, x, y, z, the 4-momentum at the crossing (interpolated
   between the pre- and post-chord momenta), and the step length;
3. an initial vertex (x, y, z, t), translated consistently for the string bootstrap;
4. disc material slabs (TFPX/TEPX/TEDD) with the same per-module x/X₀ as the barrel slab of the same module type
   (UNVERIFIED, ×0.5-×2 systematic, as approved for the barrel; D4);
5. a vacuum fast path in the material kick: return at once when the endpoint is inside the tracker volume but in no slab
   (bit-identical by construction; ×1.18-1.24 measured, p5);
6. defaults qcap = 2¹⁹, max_steps = 2×10¹⁰ (§6.3), BTL and an ETL proxy surface for the timing observables;
7. a `legacy=True` switch (barrel `REC_RADII`, one root per chord, vertex at 0, no disc material) that must reproduce
   `T3_causal.run_causal` **bit for bit** (validation V1). The step map, borrowing, max-boost splitting, B kick, Bethe,
   straggling and Highland code are copied unchanged.
Versioning: `T3_causal_s3.py` carries `KERNEL_VERSION = "s3.1"`; every output file stores the version string, the md5 of
the kernel source and of `code/T3_causal.py`. Any later change bumps the version, and outputs of different versions are
never mixed in one grid point.

### 4.2 Surfaces (the Stage-4 interface)
The surface table is the `simplified` block of `acts/geometry/cms_phase2_public.json` (D111 nominal radii and z), with each
stacked OT module type represented by two concentric sensors at r ± s/2 (PS s = 1.6/2.6/4.0 mm, 2S 1.8/4.0 mm per layer;
TEDD rings likewise in z): 4 TBPX + 2×3 TBPS + 2×3 TB2S cylinders, 8 TFPX + 4 TEPX discs and 2×5 TEDD discs per side, plus
the BTL cylinder (r = 114.8 cm, the inner boundary of the BTL envelope 1148-1188 mm, |z| < 260 cm, MTD TDR §2) and an ETL
proxy disc at |z| = 292 cm (the ETL sits in front of the endcap calorimeter at |z| ≈ 3 m, 1.6 < |η| < 3.0 [MTD TDR §1];
the exact z is UNVERIFIED, and the proxy is kept inside the T3 tracker volume, which ends at |z| = 293.5 cm), about 60
surfaces. Each surface carries its D111 name, so Stage 4 maps
name → ACTS `GeometryIdentifier` when it builds the Blueprint from the same JSON. The tilted TBPS rings are flat in this
model (UNVERIFIED approximation already flagged in the JSON). Module-plane intersection (17 092 modules) is the
alternative (D1).

### 4.3 What is stored per event and per hit
One file per (species, m, Λ, configuration): `data/sim_stage3/<campaign>/<spin>_m<m>/L<Λ>_<cfg>.npz`, with per-event
arrays and the hits as one flat table plus offsets (CSR). Units: mm, ns, GeV (ACTS conventions; the Stage-4 injector
multiplies by `acts.UnitConstants`). npz is readable by numpy in both pixi environments (D15).

**File header**: kernel version and md5s; Stage-2 source file and md5; selection (pT, |η|, split, unweight seed);
configuration (B, material scale, eloss/straggling/MS flags, max_boost, hmax, qcap, max_steps); surface table; σ_norm,
σ_ref, the common weight w_max; the seed rule; creation time; CPU time.

**Per event**:
| field | meaning |
|---|---|
| `row`, `chunk`, `ievt_lhe`, `py8_seed` | Stage-2 provenance (joins to the full Pythia record via `reshower.py`) |
| `tt_split` | 0 template, 1 toy |
| `w`, `w_orig` | common unweighted weight w_max [fb, N_IC = 1] and the original row weight |
| `wvar_ratio[107]` (float32) | merged scale/PDF/merging weights divided by `w_orig` (names in the header) |
| `w_lmax_up/dn`, `w_qed` | ℓ_max-shape and QED-FSR reweighting factors (§7) |
| `p_qp`, `p_qm`, `recoil`, `jets` | initial quirk 3-momenta and the recoil (MET proxy), from Stage 2 |
| `gstar`, `cstar`, `x = 2(γ*−1)`, `pt`, `eta`, `M` | pair kinematics |
| `ell_max`, `N_osc_vac`, `eps_B`, `eps_perp`, `bodd_l0`, `k_B`, `c_ev`, `C_ev` | analytic truth per event (closed forms; c06 `pair_params`) |
| `vtx[4]`, `seed` | production vertex (mm, ns) and the kernel seed |
| `status`, `nsteps`, `maxq`, `cpu_s` | exit code (0 t_end, 1 left the volume, 2 stopped, 3 max_steps, 4 deadlock, 5 queue overflow), cost |
| `X_end[2,4]`, `P_end[2,4]`, `eacc[2]` | final positions/momenta and integrated ionisation loss |
| `ds_barrel`, `ds_all`, `ds_itps`, `res_max`, `n_plane[3]` | plane thickness through the vertex: 10 barrel layers (Stage-1 definition), all surfaces, IT+PS only; max residual; plane normal |
| `nhit_surf[n_surf, 2]` | hits per surface per quirk |
| `floor_flag` | b_odd/ℓ₀ < 10⁻⁷ (within ×3 of the double-precision floor; §1.1), and the replica spread where measured |

**Per hit** (flat table, `hit_offsets[n_events + 1]`): `quirk` (0 = +q, 1 = −q), `surf`, `icross`, `t`, `x`, `y`, `z`,
`px`, `py`, `pz`, `E`, `dE_sensor` (Bethe loss in the sensor thickness along the direction, for the digitiser).

**Derived observables** (computed by `observables.py` from the stored hits, written to a per-point summary table and
`results/*.json`; not re-propagated):
- P1: Δs (each definition) and its distribution, Δs_B, Δs_MS, Δs_B+M; per-event c from (B₀, B₀/2); the Λ exponents; the
  response R(1/2); the in-plane vs out-of-plane displacement relative to the vacuum hits (where V is run).
- P2: hits per layer, crossings per layer, maximum transverse pair separation on each layer, the hit-time delay
  t − r/c, the non-monotonic pair separation, the plane normal vs the recoil direction, N_osc (closed form and counted
  from the hit sequence), ℓ_max (closed form and the hit-level estimate), dE/dx sums, the merging fraction (pair separation
  below 25/100 µm on IT layers), and the exit/stop status.

## 5. Validation (all truth level; criteria fixed before running)

| # | Test | Inputs | Pass criterion | Cost (ESTIMATE) |
|---|---|---|---|---|
| V1 | Kernel regression | `T3_causal_s3(legacy=True)` vs `T3_causal.run_causal`, 20 MG events × {V, B, BM, M} × {0.6, 3, 10 keV}, same seeds | hits bit-identical (all 9 columns), same status and nsteps | < 0.2 CPU-h |
| V1b | New recorder | s3 non-legacy vs legacy on the same events | every legacy hit reproduced to < 10⁻⁹ cm; extra hits only grazing double roots or discs; disc hits checked against an independent numpy chord intersection on 5 events | minutes |
| V2a | Stage-1 numbers on the production driver, same events | old T2-cache events of M3 (seed 777 + m), 500/1000 GeV, 1 and 3 keV, B₀ and B₀/2 at max_boost 10⁻³ (120 events) | M3.json/FU.json medians and per-event c reproduced exactly (same kernel in legacy mode) | ≈ 0.5 CPU-h |
| V2b | c law on the MG sample (the physics test) | P1 points, B₀ and B₀/2 | median measured c vs the analytic per-event prediction (c06 `pair_params` on the same events): \|Δc\| ≤ 2σ and ≤ 1.5 % at 1 keV (P-10); Λ exponents vs −2 + 2c (P-11); R(1/2) (P-13); flat m dependence of Δs_B at 1 keV (P-15); scalar Ẽ 500 vs E 500 (P-24). C on the MG sample is re-derived and compared with predictions.json (0.43/1.23/1.62 on the T3 sample): a difference here is a sample effect (−ln γ_cm β_T sin α), not a failure | included in P1 |
| V3 | Step convergence and floor | 20 events per (m ∈ {200, 1000}, Λ ∈ {1, 3, 10, 20, 30}), configs B, BE and BK (deterministic); max_boost 10⁻²/10⁻³ everywhere and 10⁻⁴ at Λ ≤ 3 keV (10⁻⁴ costs ≈ 2500 s/event at 30 keV, so 10⁻³ is the reference there); hmax 0.2/0.05 cm at 0.3-1 keV | Δs_B change < 1 % (Λ ≤ 5 keV); hit positions matched by (quirk, surface, crossing index): < 1 µm out of plane and < 5 µm in plane (below the 3-10 µm IT resolution) for the production setting; replica test (initial momenta × (1 + 10⁻¹⁴), 3 replicas) at 10/20/30 keV gives the per-event round-off spread of Δs_B → `floor_flag` | ≈ 5-6 CPU-h |
| V-scale | NG scaling identity | 5 events: (3 keV, B₀, D) vs (1 keV, B₀/9, 9D), B only | hits agree after x → x/9 to the hmax interpolation error | < 0.1 CPU-h |
| V4 | Independent solver | `code/R1_conformal_ng.py` (N = 256, and 1024 on 2 events) vs s3 B config, 10 MG events at 500 GeV × {1, 2 keV} and 1000 GeV × 1 keV | Δs ratio 0.99-1.01; hits ≤ 8 µm (the S-1 / R1 criteria) | ≈ 0.5 CPU-h |
| V5 | Continuity with the old T2-cache results | (a) T3_ms_thickness configuration (B, B+M, M; 200/500/1000 GeV; 0.3/1/3/10 keV; 60 events; old cache, old seeds) through the production driver in legacy mode; (b) the same observables on MG events at matched selection (\|η\| < 1) | (a) identical to `figures/T3_ms_thickness.npy` (same events, seeds and kernel settings; if the original draw cannot be reconstructed, agreement within bootstrap errors); (b) report the MG − cache shift of each median with bootstrap errors; the expected direction is set by the ISR-tail change (ℓ_max −8…−26 %, VALIDATION §3) | ≈ 1 CPU-h |
| V6 | Seeds and reproducibility | 50 random jobs rerun; per-event seed = hash(spin, m, row, Λ, cfg) independent of the worker | output hit arrays bit-identical on rerun; different events never bit-identical; `spawn` start method (methodology 7.4) | minutes |
| V7 | Physics sanity | all production | vacuum Δs ≤ 10⁻³ µm; no status 3/4/5 (any occurrence is listed and rerun with a larger cap); hit time ≥ r/c; hits per layer vs the S-6 numbers (≈ 3 per layer for heavy pairs) | — |
| V8 | Stage-4 ingestion | 10 events from one P2 file → `acts` env → `SimHit` + digitisation (as `acts/scripts/smoke_test.py` part B) | every hit lands on its surface (`isOnSurface`), units correct, measurements produced | minutes |
| V9 | Unweighting | one point (E 500, 1 keV, BM) run in the weighted mode (first rows, weights w) vs unweighted | weighted and unweighted medians of Δs, ℓ_max, hits per layer agree within errors | ≈ 0.1 CPU-h |

## 6. Compute and disk

### 6.1 Probes (all on this machine: Apple M3, 4 performance + 4 efficiency cores, 24 GB; 7 workers, `nice`)
| probe | what | CPU | output |
|---|---|---|---|
| p0 | event budget per TRGS file (unweighted counts per split, N_eff, \|η\| fractions, yields) | seconds | `p0_event_budget.json` |
| p1 | T3_causal cost and step convergence: 4 masses × 9 Λ (0.3-30 keV) × {V, B, BM, M, BE} × {10⁻², 10⁻³, 10⁻³ with hmax 0.02 cm}, 4-16 events per cell, 2656 jobs | 3.4 CPU-h (30 min wall) | `p1/`, `p1_summary.json`, `p1_analyse_out.txt` |
| p2 | physics scales for the Λ edges (§1.1) | seconds | `p2_edges.json` |
| p3 | recorder overhead, 12 → 36 surfaces | 1 min | `p3_recorder_overhead.json` |
| p4 | coarser step (3×10⁻²) at 10-40 keV (deterministic BE) and the 40 keV BM cost | ≈ 0.7 CPU-h | `p4/`, `p4_summary.json` |
| p5 | vacuum fast path in the material kick (generated copy of the kernel in `probes/_gen/`) | 6 min | `p5_material_fastpath.json` |
| p6 | cost on the P1 selection (\|η\| < 1); one deterministic 3 MeV kick (BK) vs B vs BM; BK convergence | ≈ 0.9 CPU-h | `p6/`, `p6_summary.json` |
| p7 | cost model of the grid | seconds | `p7_cost_model.json`, `p7_cost_model_out.txt` |

### 6.2 Measured cost per event (mean wall time per event with 7 workers busy, so the P/E-core mix of production is included; VERIFIED as measurements, 4-16 events per cell)
| Λ [keV] | 0.3 | 1 | 3 | 5 | 10 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|
| BM, max_boost 10⁻² (\|η\| < 2.5; 200/500/1000/1500 GeV) | 0.01 | 0.03-0.04 | 0.5-0.8 | 2.0-3.1 | 8.8-16 | 39-88 | 51-149 | 112-194 (500, 1500) |
| BM, 10⁻³ | 0.01 | 0.24-0.35 | 5.5-8.7 | 22-35 | 125-228 | — | — | — |
| B, 10⁻² | 0.007 | 0.015-0.023 | 0.18-0.32 | 0.5-1.0 | 1.3-3.8 | 3.6-11 | 7-24 | — |
| B, 10⁻³ | 0.01 | 0.11-0.19 | 1.6-3.1 | 4.8-10.5 | 8.7-75 (3 ev.) | — | — | — |
| \|η\| < 1 (p6, 500/1000 GeV): B 10⁻³ / BM 10⁻² | — | 0.15-0.18 / 0.04 | 2.3-3.4 / 0.78 | 6.7-10 / 3.0-3.4 | 24-35 / 17-20 | — / 85-107 | — | — |

Findings:
- **Cost ∝ Λ^2.4 for BM at 10⁻² and Λ^1.9-2.2 for B** (pooled fits), and ∝ 1/max_boost. Light masses cost 2-3× more at
  ≥ 20 keV than heavy ones (harder γ* spectrum, more boost-limited steps per oscillation). Per cell, p90/mean ≈ 1.6-1.9; the
  longest single events are 470 s (BM 10⁻³, 10 keV) and 424 s (BM 10⁻², 40 keV), with up to 3.6×10⁹ steps.
- **Material, not the field, drives the high-Λ cost:** BM and M cost the same, and both cost 5-10× B at 20-30 keV
  (3-7×10⁸ vs 0.5-1×10⁸ steps). B+E (dE/dx without MS) costs about as much as B, so energy loss is not the cause, and one
  deterministic 3 MeV kick (BK) costs only 1.4-2× B. So the extra steps come from the repeated per-step MS kicks while the
  merged pair oscillates inside a slab. This is a property of the material model, which is not scale-free (§3), so it
  cannot be avoided.
- **Central events cost more:** \|η\| < 1 events cost 1.34× (BM) and 1.40× (B) the \|η\| < 2.5 average (p6/p1, range
  0.9-2.8 per cell). Adding disc material (§4.1 item 4) will raise the cost of the forward events toward this, so the P2
  estimate carries a factor up to 1.34.
- **Fast path:** the vacuum early return in the material kick is bit-identical and 1.18-1.24× faster (p5). A recorder with
  ~3× more surfaces costs +4-6 % (p3).

### 6.3 Step settings (from the convergence probes)
- **hmax:** 0.2 vs 0.02 cm gives identical hits above 1 keV and ≤ 1.5 µm differences at 0.3-0.6 keV (p1 `B_fvsff`).
  Keep 0.2 cm.
- **max_boost 10⁻² vs 10⁻³ (deterministic B, BE, BK):**
  - Δs_B is biased by +0.1…+1.6 % (median per cell) at 0.3-5 keV at 10⁻², the Stage-1 step bias. At 10 keV the per-event
    B-only ratio is 0.25-1.04 (floor plus steps). So **P1 B and B/2 use 10⁻³**, and P1 makes no B-only claim above 5 keV
    beyond Stage 1's ±5 % statement.
  - Hit positions at 10⁻²: the median over events of the per-event maximum displacement is 0.2-4 µm out of plane and
    0.5-6 µm in plane at 0.3-1 keV (worst events 15-17 µm), falling to ≤ 0.3/≤ 0.8 µm at 2-3 keV and ≤ 0.15/≤ 0.2 µm at
    5 keV. At 10 keV against 10⁻³: ≤ 0.44 µm out of plane and ≤ 12 µm in plane (BE, 8 events). With J ≠ 0 (BK) at 3 and
    10 keV: ≤ 2.5 µm out of plane and ≤ 1.4 µm in plane. One event in about 60 changes a grazing-crossing count (mm-scale
    in-plane shift of one hit). For comparison, the IT resolution is 3-13 µm (tkLayout parametrised) and 7/29 µm binary.
  - **Production setting P2/Stage 4: max_boost 10⁻³ for Λ ≤ 1.5 keV** (where 10⁻² errors reach the IT resolution, and 10⁻³
    is cheap), **10⁻² for Λ ≥ 2 keV.** V3 checks 10⁻³ against 10⁻⁴ and 10⁻² against 10⁻³ at 20-30 keV on more events.
- **3×10⁻² is rejected** (p4): at 1500 GeV and 20-40 keV it shifts in-plane hits by up to 140 µm and changes 6-20 crossing
  counts, and one 40 keV run ended in a mid-run queue deadlock (status 4 after 1.6×10⁸ steps).
- **Caps:** the string queue reached 1.2×10⁵ segments (10⁻³, 10 keV) → qcap = 2¹⁹; max_steps = 2×10¹⁰ (above the 3.6×10⁹
  maximum seen). At the production settings status 3/4/5 never occurred in 2656 + 79 + 222 probe jobs (one event reached t_end, status 0,
  at 0.3 keV in all its configurations). Production logs every status ≠ 1 and reruns status 3/4/5 with larger caps or the
  label swap (V7).

### 6.4 Total CPU and wall time (p7 cost model: measured means interpolated in log m and log-log in Λ; ESTIMATE)
| block | content | CPU-h |
|---|---|---|
| Validation V1-V9 | §5 | ≈ 8-10 |
| P1 | 5 species-masses × 8 Λ; B 27, B/2 7, M 10, BM 10, V 0.5, material variants 2 | **56** |
| P2, Λ ≤ 10 keV | E 14 masses + Ẽ 3 × 16 Λ × 400 events (200 template + 200 toy) | **46** |
| P2, Λ ≥ 15 keV (recommended option B) | 15/20/30 keV (+40 keV at E ≥ 1000, Ẽ ≥ 500) at 7 E masses {200, 300, 500, 700, 1000, 1200, 1500} + Ẽ 3, 200 template events; 400 (template + toy) at E 1000 and 1200 | **167** |
| P2 material variants | ×0.5, ×2 at E 200/500/1000/1500 + Ẽ 500 × {0.4, 0.6, 1, 3, 10, 20} keV × 200 events | **50** |
| **Total (recommended)** | | **≈ 330 CPU-h → ≈ 47 h wall on 7 workers (≈ 2 days)** |
| with D10 (\|η\| < 4, +30), D11 (−12), D12 (+1) as recommended | | ≈ 350 CPU-h → ≈ 50 h |

Uncertainty of the total: kernel factors 0.83 (fast path) to 1.12 (fast path × disc material, upper bound) and ±25 % from
the small cost samples: **≈ 250-460 CPU-h, 35-65 h wall.**

Where the CPU goes, per Λ, for P2 at 400 events and all 17 species-masses (option A): 15 keV 59, 20 keV 111, 30 keV 195,
40 keV 90 CPU-h, against 46 CPU-h for all 16 points at ≤ 10 keV. **The 30 and 40 keV points are the expensive ones.**

| P2 option | Λ ≥ 15 keV coverage | CPU-h (P2 only) | total with P1, variants, validation | wall (7 workers) |
|---|---|---|---|---|
| A (full) | all 14 E masses + Ẽ 3, 400 events | 501 | ≈ 615 | ≈ 88 h (3.7 d) |
| **B (recommended)** | 7 E masses + Ẽ 3, 200 events (400 at E 1000/1200) | 213 | **≈ 330** | **≈ 47 h** |
| C (minimal) | as B, 200 events everywhere (also ≤ 10 keV), no 40 keV, material variants to 10 keV | ≈ 155 | ≈ 245 | ≈ 35 h |

**Points flagged as expensive, and alternatives** (none is unaffordable on this machine; the question is wall time):
1. *30 keV* (≈ 70 CPU-h in option B) and *40 keV* (≈ 38 CPU-h); 15 and 20 keV cost ≈ 21 and 39 CPU-h: (a) the 7-mass subset with
   interpolation in m (the merging edge scales smoothly as √m, §1.1); (b) run them last, after Stage 4 has fixed the merging
   criterion (25 or 100 µm), and drop 40 keV if the edge is below 30 keV at all masses; (c) the fast path (×1.2).
2. *P1 B-only at 7-10 keV at 10⁻³* (≈ 20 of the 27 CPU-h of B): it documents the unattributed region and cannot remove the
   ±5 % without the floor test (O-1). Option: 7 and 10 keV at E 500/1000 only (saves ≈ 12 CPU-h; D11).
3. Not recommended: an approximate merged-pair model at ≥ 20 keV (not classical NG, and not truth level), MS aggregated per
   slab traversal (changes the material model), or max_boost 3×10⁻² (rejected above).

### 6.5 Disk and memory
- Per event: about 150 ± 50 hits (36 surfaces gave 123/event at 500 GeV, p3; ~60 with discs) × 48 bytes, plus ≈ 0.8 kB
  of per-event data (107 float32 weight ratios dominate) ≈ 8 kB uncompressed.
- Events: P2 ≈ 117 k, P1 ≈ 55 k (event × configuration), material variants 12 k, validation ≈ 20 k → ≈ 200 k → **≈ 1.6 GB
  (≤ 5 GB with margin)**, against ≈ 136 GB free. Probe outputs: 22 MB in `data/sim_stage3/probes/`.
- Memory: qcap 2¹⁹ (34 MB) + hit buffer (42 MB) per worker. The driver pre-extracts the selected Stage-2 rows per mass into
  a small event list, so workers do not load the full TRGS npz (up to ≈ 200 MB each with the weight columns): **< 2 GB in
  total** out of 24 GB.

### 6.6 Execution order (resumable; each job = one (point, configuration, chunk of 25 events); expensive chunks first)
Environment: `NUMBA_CACHE_DIR=sim/stage3/.numba_cache` and `PYTHONDONTWRITEBYTECODE=1`, so that no cache file is written
under `code/` or `sim/scripts/` (the probes refreshed numba cache files in `code/__pycache__/` for `T3_propagator`
and a bytecode file in `sim/scripts/__pycache__/`; caches only, no source touched).
1. Kernel `T3_causal_s3.py` + V1/V1b/V6/V8 (hours of person time, < 1 CPU-h).
2. V2a, V3, V4, V5, V-scale, V9 (≈ 7 CPU-h).
3. P1 (56 CPU-h, ≈ 8 h wall), including V2b. **Internal checkpoint:** if V2b fails (§5), stop and report before P2.
4. P2 at Λ ≤ 10 keV (46 CPU-h).
5. P2 material variants (50 CPU-h).
6. P2 at Λ ≥ 15 keV (167 CPU-h), 30/40 keV last.

## 7. Systematics to propagate

| Source | Size | How Stage 3 carries it | Stored as |
|---|---|---|---|
| Tail rate f(pT(QQ̄) > 200), LO-MLM | +12…+15 % / −11…−13 % (ESTIMATE; VALIDATION §5.1) | normalisation nuisance on yields (it is a rate, not a shape: ME α_s, merging, shower) | header number per mass; applied in Stage 4/5 |
| ℓ_max shape (reference medians) | ±5 % (ESTIMATE; VALIDATION §3) | event reweighting in x = 2(γ*−1): w ∝ (x/x̃)^(±a), normalised to preserve Σw, with a per mass such that the weighted median of ℓ_max moves by ±5 %. Kinematics are Λ-independent, so one set of factors serves every Λ | `w_lmax_up`, `w_lmax_dn` |
| QED FSR off the quirks (user decision 2026-10-11) | −1.1 ± 0.8 % (stat) on ℓ_max, one-sided | the same tilt, tuned to −1.1 % (and −1.9 % to cover the stat. error) | `w_qed`, `w_qed_19` |
| Scale (μ_R, μ_F; dynamical scale) and PDF (CT18NLO Hessian, NNPDF23LO), merging qCut | from the 107 merged weight columns | per-event weight ratios; 9-/7-point envelope, CT18 asymmetric Hessian (90 % → 68 % by ÷1.645) as in SAMPLES.md | `wvar_ratio` |
| T3 material ×0.5-×2 (user decision 2026-10-11, ACTS install check D4) | Δs_MS ∝ (x/X₀)^0.517 (S_msscale, same code) | re-propagation at a subset (configs BM×0.5, BM×2, M×0.5, M×2; §1); elsewhere interpolated in m and Λ | separate files `L<Λ>_BMx0.5.npz` etc. |
| Unattributed Δs_B systematic above ≈ 5 keV (Stage 1) | ±5 % on Δs_B (population) | quoted on P1 numbers at 7-10 keV; floor-flagged events listed | P1 results JSON |
| NG validity at near-miss crossings | 0 for Λ ≲ 10 keV, 3-8 % at 30 keV on Δs_B (P-18) | quoted; Δs at ≥ 20 keV is MS dominated | results JSON |
| Step convergence / precision floor | from V3 | quoted per configuration; `floor_flag` per event | per event + results JSON |
| σ_norm | ±5 % (K + EW scheme), PDF4LHC21 ±3.7/6.6/18.5 % at 200/500/1000 GeV; γγ (+4 %) and Sommerfeld not included | header numbers; yields only | header |
| Uniform 3.8112 T field | the fringe B_r at the tracker ends (T3_field estimate) is not modelled | stated as a limitation; not a Stage-3 variation (D14) | — |

## 8. Decision table (scope and design choices for the user; each with a recommendation)

| # | Decision | Options | Recommendation | Confidence | Cost impact |
|---|---|---|---|---|---|
| D1 | Surface model handed to Stage 4 | (a) the `simplified` cylinders/discs of `cms_phase2_public.json` with stacked OT sensors, BTL and an ETL proxy (§4.2); (b) the 17 092 D111 module planes intersected inside the kernel; (c) (a) now, (b) later at a few points | **(a)**: it is the block built for the ACTS Blueprint, it is exact for the coplanarity physics, and every hit carries the D111 surface name. (b) changes only the acceptance at the tilted TBPS rings and module edges, for 1-2 extra days of kernel work | medium | none (+5 % recorder) |
| D2 | Production vertex | (a) origin for P1, luminous region (σ_z 45 mm, σ_t 190 ps, σ_xy 5 µm) for P2/Stage 4; (b) origin everywhere, translated in Stage 4 | **(a)**. (b) is wrong for disc crossings and slab edges (the material and the surfaces are not translation invariant in z) | high | none |
| D3 | Kernel changes and versioning | versioned copy `sim/stage3/code/T3_causal_s3.py` (§4.1 items 1-7), `legacy=True` bit-identical to `code/T3_causal.py` (V1); or edit T3_causal.py | **versioned copy**; `code/T3_causal.py` untouched (rule); version + md5 in every output | high | — |
| D4 | Disc material | add TFPX/TEPX/TEDD slabs with the barrel x/X₀ of the same module type (UNVERIFIED, inside the approved ×0.5-×2 band); or none | **add**. Without it the ≈ 70 % of the \|η\| < 2.5 tail with \|η_pair\| > 1 crosses no material in the endcap tracker, so their MS floor is missing | medium (values UNVERIFIED) | up to ×1.34 on P2 (§6.2) |
| D5 | P2 coverage at Λ ≥ 15 keV | A: all 14 masses, 400 ev (≈ 615 CPU-h total, 3.7 d); **B**: 7 masses + Ẽ, 200 ev, 400 at E 1000/1200 (≈ 330, 2 d); C: B with 200 ev everywhere, no 40 keV (≈ 245, 1.5 d) | **B**; the merging edge scales smoothly as √m (§1.1), so interpolation in m is safe; the masses near the reach get toys | medium | §6.4 |
| D6 | Λ grid | lower band 0.3-1.2 keV (10 points, common to all masses), interior 1.5-10 (6), upper 15/20/30 keV, 40 keV at E ≥ 1000 and Ẽ ≥ 500 | **as proposed** (the band is < 1 % of the CPU, so a per-mass band would save nothing). Alternative: drop 40 keV (−38 CPU-h) if Stage 4 fixes the merging criterion at 100 µm | medium-high | 40 keV ≈ 38 CPU-h |
| D7 | Events per point | P2 200 template + 200 toy (≤ 10 keV); P1 300 (≤ 5 keV) / 200 (7-10 keV); option: 400 template at E 1000/1200 for all Λ | **as proposed**; the option adds ≈ 6 CPU-h at ≤ 10 keV and helps only if P2 fits near the reach are template-limited | medium | small |
| D8 | Step settings | P1 B, B/2, V at 10⁻³; M, BM at 10⁻²; P2 10⁻³ at Λ ≤ 1.5 keV, 10⁻² above; hmax 0.2 cm | **as proposed** (§6.3) | high (to be confirmed by V3) | — |
| D9 | Material variants | P2: ×0.5, ×2 at 5 points × {0.4, 0.6, 1, 3, 10, 20} keV; P1 at 1, 3 keV; option: add 30 keV | **as proposed** (50 CPU-h); 30 keV adds ≈ 60 CPU-h for a point where the MS floor is already measured at 20 keV | medium | 50 (+60) CPU-h |
| D10 | Pair acceptance for P2/Stage 4 | \|η_pair\| < 2.5 (Stage-2 reference); or \|η_pair\| < 4 (13-24 % more of the tail, so Stage 4 can define the fiducial denominator per quirk, Stage-2 DEFERRED handover), keeping ≥ 200 effective events inside \|η\| < 2.5 | **\|η_pair\| < 4** with the event count defined inside \|η\| < 2.5; forward events are cheaper (fewer oscillations before the endcap), so ≈ +15 % P2 CPU (ESTIMATE, ≈ +30 CPU-h) | medium | ≈ +30 CPU-h |
| D11 | P1 B-only at 7-10 keV | all 5 species-masses; or E 500/1000 only | **E 500/1000 only**: it documents the unattributed region and cannot remove the ±5 % without the floor test (D12) | medium | −12 CPU-h |
| D12 | Optional floor test O-1 (NEAR_MISS §10 item 1: double-double or mpmath step map on a detector scaled by 1/27, the 3-5 events with the smallest ε⊥) | do it after P1, separately; or not | **do it** as a small side study (≈ 1 CPU-h + 1-2 days of person time); it is the only way to turn the >5 keV ±5 % into a measurement. Not blocking for Stage 4 | medium | ≈ 1 CPU-h |
| D13 | Ẽ coverage | P2 at 200/500/1000 (all Stage-2 Ẽ masses), P1 at 500 | **as proposed** | high | included |
| D14 | Magnetic field | uniform 3.8112 T; or the T3_field current-sheet map | **uniform**: B_r ≤ 0.9 % at \|η\| < 1, 2-5 % at 1.5 < \|η\| < 2 in a model without yoke that over-estimates it (T3 §4.3) | high | — |
| D15 | Storage format | npz with CSR hits, mm/ns/GeV; or Parquet/HDF5 | **npz** (numpy in both pixi envs; no new dependency) | high | — |
| D16 | Workers | 7 (one core left free); or 8 (the 8th is an efficiency core, ≈ +8-10 %) | **7**, `nice` | high | — |

## 9. Deliverables and review plan

**Deliverables** (all inside `theory_track/`):
- Code (`sim/stage3/`): `code/T3_causal_s3.py` + `code/test_regression.py` (V1/V1b); `scripts/make_eventlists.py`
  (selected Stage-2 rows per mass and selection, with weights and provenance), `scripts/produce.py` (resumable driver:
  jobs = point × configuration × chunk of 25 events; per-event seed hash; `spawn`; CPU accounting), `scripts/observables.py`
  (Δs definitions, P1/P2 observables), `scripts/sysweights.py` (ℓ_max and QED tilts), `scripts/val_*.py` (V1-V9),
  `scripts/make_docs.py` (VALIDATION §0 generated from `results/*.json`, as in Stage 2); pixi tasks for each step.
- Data: `data/sim_stage3/{p1,p2,matvar,validation}/<spin>_m<m>/L<Λ>_<cfg>.npz`, `data/sim_stage3/STAGE3_INDEX.json`, and a
  section in `data/README.md`.
- Documents: `sim/stage3/README.md`, `SAMPLES.md` (inventory: points, configurations, events, md5, CPU), `VALIDATION.md`
  (§0 generated from the JSON), `results/*.json`, internal diagnostic figures (the JFC/mplhep restyle stays deferred to
  Stage 5, Stage-2 D-3).
- P1 results: Δs_B, c, Λ exponents, R(1/2), Δs_MS and Δs_B+M per point, with the pulls against `predictions.json` and the
  re-derived MG-sample predictions.
- Stage-4 handover note: schema, units, surface names → ACTS geometry identifiers, seeds, the V8 ingestion test.

**Review plan** (JFC loop, as for Stages 1-2):
1. The user reviews this plan and answers D1-D16 (this checkpoint).
2. Internal checkpoint after execution steps 1-3 (§6.6: kernel, validation, P1): a short report to the orchestrator.
   **If V1 or V2b fails, stop before P2.** V2b's criteria are fixed in §5 now, and no parameter is tuned toward
   predictions.json.
3. After production: a critical review (independent re-checks: kernel regression, recorder on discs, convergence and
   floor flags, the c-law comparison, weights and unweighting, the systematics tilts, units and schema) and a constructive
   review, in parallel → fixer → fresh reviewer → PASS → user checkpoint Stage 3 → 4.

**Risks**
- *c law on the MG sample.* In p6, per-event c(k_f = 2) at 5 keV on 6 MG events per mass scatters 0.07-0.29, and the medians
  (0.16 at 500 GeV, 0.11 at 1000 GeV) lie above the predicted 0.078/0.076 (at 3 keV: 0.086/0.080, close to the prediction).
  Six events say nothing statistically, but the MG tail is harder than the T3 sample, and events with k_B > 10 carry
  +0.08-0.12 in c (NEAR_MISS §5.5). V2b (300 events) decides. If the population median at 5 keV deviates, it is a finding
  (the B* effect on the realistic spectrum), reported as such, not tuned away.
- *Cost.* The estimate rests on 4-16 events per cell with long tails: 250-460 CPU-h for the recommended set. The order in
  §6.6 puts the cheap and decisive steps first.
- *Material.* Barrel and disc x/X₀ are UNVERIFIED (×0.5-×2 carried). They drive both the MS floor and the high-Λ cost.
- *New recorder.* Disc and double-root crossings are new code. V1b checks them against an independent numpy intersection.
- *Precision floor.* Above ≈ 10-20 keV the B-only thickness cannot be computed in double precision (§1.1). This does not
  affect B+M hit positions at the µm level, but no B-field statement is possible there without O-1.
- *Geometry.* If Stage 4 later moves to module-plane geometry (D1 (b)), the high-Λ points would need a rerun with the module
  recorder.

**Self-check against the executor role.** No result is produced yet. Every number in this plan is a probe measurement
(VERIFIED as a measurement on this machine), a closed-form ESTIMATE on the Stage-2 sample, or a citation of Stage-1/2 and
synthesis results with their location. The physics predictions that Stage 3 will test (V2b) are fixed before any
production run.
