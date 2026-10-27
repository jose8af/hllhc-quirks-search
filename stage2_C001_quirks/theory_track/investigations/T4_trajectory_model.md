# T4: Trajectory model for reconstruction, measurement of (m_Q, Λ), information content of a quirk hit pattern

Investigator: T4 (theory track, C001 quirks). Date: 2026-10-08. Status: COMPLETE (2026-10-08).

Conventions: Λ ≡ √σ (BRIEF §1). σ = 50.68 GeV/cm (Λ/keV)² [T2 §2.2]. Units: cm, GeV, c = 1 unless stated.
Code: `theory_track/code/T4_*.py`. Figures: `theory_track/figures/T4_*`.
Builds on: T2 (`T2_propagator.py`, exact vacuum solution, causal string), T3 (`T3_causal.py` numba causal string, material table, timing).

## 1. Executive summary
1. **Degeneracy theorem (exact; G-T4-2, EXPLOIT).** Hit positions, hit times and dE/dx depend on (m_Q, Λ) only through ℓ₀ = m_Q/Λ², plus the velocities.
   - Scale invariance of the Nambu-Goto + point-mass action, checked in the Fisher matrix: the vacuum ln σ column is ≤ 3×10⁻⁷ of the largest.
   - **m_Q needs a momentum scale.** Only three exist: the recoil (MET = p_T(QQ̄)), the B field through ε_B = qB/σ, and material (∝ 1/m_Q).
   - dE/dx and MTD timing measure only velocities and add nothing to σ(m_Q).
2. **Measurement after discovery (G-T5-7 answered; Sec. 4.3).** Cramér-Rao with MS, Phase-2 resolutions, BTL 35 ps and MET 25 GeV/component:
   - **σ(m_Q)/m_Q ≈ 6-10 % and σ(Λ)/Λ ≈ 3-5 % per event; ≈ 1.0 % and 0.5 % with 30 events**, flat over m_Q = 200-1000 GeV and Λ = 1-10 keV.
   - The floor is the MET/JES scale (≈ 1-3 %, UNVERIFIED).
   - The trajectory alone fixes ℓ₀ to 0.02-3 % and γ* to 0.03-3 % per event.
3. **B field as a recoil-free Λ meter (G-T4-3, WORTH A CHECK).**
   - The informative B displacement is in-plane, ≈ 0.5 qBR/Λ² (20-150 µm in the OT at 1 keV), m_Q independent, not ∝ m_Q/Λ⁴.
   - After MS: σ(Λ)/Λ = 16-20 % per event and 1.5-2.2 % for 30 events at 1 keV; 17-29 % at 3 keV; nothing at 10 keV.
4. **Fit-ready model (G-T4-1, EXPLOIT).** A 9-parameter causal-string model (vertex z, P_QQ̄, γ*, CM axis, m_Q, Λ) plus MS kinks, against ~50-130 measurements per event.
   - It predicts each hit after the IT to 15-55 µm, inside strips 0.5-24 mm wide at 1-3 keV. That is ×20-100 (1 keV) and ×2-10 (3 keV) rejection of random in-plane hits per OT layer beyond the coplanar cut; no gain at 10 keV.
   - **Not linear enough for a Kalman filter.** The phase-linearity window is 2-10 % of a cycle, and there is an aliasing minimum at 10 keV. Use a global Gauss-Newton fit with a phase-scan seed.
   - **The B response is not linear in B** (G-T4-4): vacuum + first-order B misses 30-45 % of the B effect.
   - Mean energy loss shifts OT hits by 40 µm-1.5 mm (G-T4-7). Both must be in the model.
5. **Event-level handles.**
   - MET-strip alignment (G-T4-5, EXPLOIT): ×13-34 random-plane rejection at 95 % efficiency, plus a φ road for seeding.
   - Seeding (G-T4-6): the oscillation is resolved layer to layer only at Λ ≲ 1 keV, since ΔN_osc per IT gap = 0.4 (Λ/keV)². Above that, the pattern is a straight zig-zag band through the PV with non-monotonic separation (≈ 100 %).
   - Only 23-47 % of quirk OT crossings form 2 GeV stubs at Λ ≤ 3 keV.

## 2. The fit-ready trajectory model (Q1)

### 2.1 Scale invariance: the structure of the model (exact)
- The action S = −m∫dτ₁ − m∫dτ₂ − σ∫dA [0805.4642 Eq.3.7] plus the Lorentz force has one intrinsic length, **ℓ₀ ≡ m_Q/σ = 1.97 cm (m_Q/100 GeV)(keV/Λ)²**. Rescale x = ℓ₀ξ and t = ℓ₀τ. The endpoint equation becomes d(γv)/dτ = (string term in ξ) + ε_B v × B̂, with
  **ε_B ≡ qBc/σ = 2.25×10⁻⁴ (B/3.81 T)(keV/Λ)²** (ESTIMATE; qBc = 0.01143 GeV/cm at 3.81 T).
  - The string term contains no parameter: the Nambu-Goto area term scales like the mass term.
  - The causal null-vector algorithm is also invariant: its splitting variable 2σ s·p/m² is scale free.
  - Check (ESTIMATE, `T4_model.py` + `T4_fisher.py`): changing ln σ by 10⁻² at fixed (ℓ₀, velocities) moves vacuum hits by ≤ 0.09 µm, i.e. numerical noise.
- Material breaks the scaling only through 1/m_Q:
  - MS angle θ₀ ∝ 1/(βp) = 1/(m βγ β);
  - mean energy loss: ΔE/E_kin ∝ 1/m_Q.
- Therefore every hit position is
  **x_hit = ℓ₀ · F(z₀/ℓ₀, (βγ)_pair (3), γ*, n̂ (2); ε_B; κ_MS, κ_E)**, with κ_MS, κ_E ∝ 1/m_Q.
  Times are ℓ₀/c times the same kind of function. dE/dx is a function of the per-hit βγ only.

### 2.2 Parameter set and counting
- **9 physics parameters**, with the beam spot fixing x₀ and y₀:
  1. vertex z₀;
  2. pair momentum (p_T, φ, η): 3;
  3. γ* (equivalently M_QQ̄ = 2γ*m_Q);
  4. CM axis of quirk 1 relative to the pair velocity (cosθ*, φ*): 2;
  5. m_Q and Λ: 2.
  - The oscillation phase is **not** free: the pair starts at zero separation at the vertex.
  - Neither is the plane orientation: it is spanned by n̂ and β_pair.
- **Plus nuisance parameters:**
  - 2 MS angles per material crossing per quirk (typically 2 × 11-25 crossings). They are profiled analytically (covariance or broken-lines form, Sec. 2.4).
  - Optionally one material-scale factor.
- Fisher studies use the equivalent natural set u = (z₀, ln(βγ)_T, φ, η, ln(γ*−1), cosθ*, φ*, ln ℓ₀, ln σ). In vacuum the ln σ direction is an exact null direction (Sec. 3).
- Comparison with other models:

| Model | Free parameters | What it predicts inside the plane |
|---|---|---|
| Two helices (5 each) | 10 | wrong physics (quirk curvature radius ~ ℓ₀ ≈ cm, not p/qB ≈ km); χ² unusable |
| Coplanar plane + "anything inside" [1708.02243 Sec.III.C] | 2 (normal, through the PV) | nothing: accepts any hit within Δs = 100 µm of the plane, anywhere along the strip |
| **Causal quirk-pair model (this work)** | **9** (+ MS nuisances) | every hit position and time, both quirks, every crossing |

- Measurements available per event:
  - ≈ 20-60 position hits (2-3 per layer per quirk at Λ ≥ 1 keV [T3 §6]);
  - × 2 coordinates where both are measured: z is useless in 2S (σ_z = 1.4 cm);
  - +2 BTL times;
  - + ≈ 8-12 IT dE/dx values.
  - So ≈ 50-130 numbers for 9 parameters: the model is strongly over-constrained.

### 2.3 Validation against the full causal integrator: residuals per layer vs (m_Q, Λ)
Method: ESTIMATE, `code/T4_fisher.py` + `code/T4_fisher_report.py`; full output in `figures/T4_fisher_report_out.txt`.
- **Reference.** The `T4_model.kernel` reproduces T2 `ExactPair` in vacuum to ≤ 0.04 µm at 1 keV, 0.2 µm at 3 keV and 1-2 µm at 10 keV after ~2000 crossings. In 3.81 T without material it agrees with T3 `T3_causal` to ≤ 0.1 µm (`pixi run python code/T4_model.py`).
- **Events.** 16 LO DY+ISR events per point, p_T(QQ̄) > 200 GeV, |η| < 1.
- **What each column is.** The 68 % quantile of |Δ(rφ)| over all hits of a layer, in µm:
  - "B": full causal 3.81 T minus exact vacuum, i.e. the error of a vacuum-only model;
  - "B²": full minus [vacuum + 20 × (response at B/20)], i.e. the error of a model linear in B;
  - "dE/dx": the shift from the mean ionisation loss (T3 material, thin scatterers), i.e. the error of a model without energy loss;
  - "MS": the 1σ multiple-scattering displacement (Highland, thin scatterers);
  - "res": the single-hit resolution (IT 25 µm/√12, PS 100 µm/√12, 2S 90 µm/√12; [theory_signal_model §4.1-4.2; 2210.07766 Sec.2]; IT pitch UNVERIFIED).

| m_Q, Λ | layer | B | B² (non-linear) | dE/dx shift | MS 1σ | res |
|---|---|---|---|---|---|---|
| 200, 1 | IT1 / IT4 / PS3 / 2S3 | 3.0 / 18 / 81 / 121 | 0.1 / 6.6 / 27 / 40 | 0 / 1.6 / 15 / 43 | 0.1 / 3.8 / 26 / 63 | 7 / 7 / 29 / 26 |
| 200, 3 | " | 0.6 / 2.3 / 13 / 17 | 0.3 / 0.7 / 4.0 / 8.5 | 0 / 1.1 / 22 / 67 | 0.1 / 3.1 / 32 / 69 | " |
| 200, 10 | " | 0.1 / 0.4 / 1.7 / 2.5 | noise (≈ 20 × FD noise) | 0 / 1.4 / 13 / 39 | 0.1 / 5.0 / 32 / 73 | " |
| 500, 1 | " | 2.5 / 25 / 86 / 139 | 0.6 / 5.7 / 27 / 45 | 0 / 2.4 / 24 / 98 | 0.3 / 7.6 / 44 / 121 | " |
| 500, 3 | " | 0.6 / 2.4 / 8.7 / 18 | 0.2 / 0.8 / 2.8 / 6.8 | 0 / 2.0 / 25 / 126 | 0.1 / 4.6 / 37 / 101 | " |
| 500, 10 | " | 0.1 / 0.3 / 1.2 / 3.1 | noise | 0 / 2.1 / 38 / 176 | 0.1 / 6.1 / 49 / 118 | " |
| 1000, 1 | " | 1.8 / 24 / 80 / 148 | 0 / 6.0 / 25 / 48 | 0.2 / 22 / 408 / 781 | 0.2 / 13 / 87 / 209 | " |
| 1000, 3 | " | 0.6 / 2.8 / 9.2 / 17 | 0.6 / 0.7 / 3.8 / 8.4 | 0.2 / 23 / 286 / 1455 | 0.3 / 11 / 81 / 215 | " |
| 1000, 10 | " | 0.1 / 0.3 / 1.4 / 4.9 | noise | 0.1 / 27 / 155 / 318 | 0.2 / 13 / 103 / 280 | " |

**Reading (ESTIMATE).**
1. **The vacuum closed form is a valid model only in the IT (r ≲ 15 cm).**
   - There, every correction is ≤ 1 resolution unit at Λ ≥ 3 keV, and ≤ 3 units at 1 keV, where the B shift is 18-25 µm against 7 µm.
   - In the OT the B shift is 80-150 µm at 1 keV (×3-6 the resolution) and 9-18 µm at 3 keV.
   - **Use the vacuum solution for seeding (Sec. 6), not for the final fit.**
2. **The B-field displacement scales as Λ^−1.8…−2 and is nearly independent of m_Q.**
   - At fixed layer it is ≈ 0.5-0.6 ε_B R, with ε_B R = 244 µm (keV/Λ)² at 2S3.
   - So it is a direct σ meter (Sec. 3.2).
3. **The B response is not linear in B.** The "linear in B" model misses 30-45 % of the B effect at all layers and Λ = 1-3 keV (column B²); see the scaling test in Sec. 3.2.
   - **"Exact vacuum + first-order B correction" is therefore not a controlled model.** The fit must run the causal propagator with the full field.
   - Cost: 10⁻²-1 s per evaluation (numba).
4. **Mean energy loss must be in the model.**
   - Its effect grows with N_osc, because the period shrinks with the kinetic energy and the phase drifts, and with 1/(βγ)².
   - It shifts OT hits by 40-180 µm at 200-500 GeV and by 0.3-1.5 mm at 1 TeV, i.e. ≫ resolution.
   - Its uncertainty (material budget, Bethe at βγ ≈ 0.3-1) is therefore a fit nuisance, not negligible. Straggling, its stochastic part, was not modelled here; T3 found no out-of-plane effect.
5. **Multiple scattering exceeds the resolution in every OT layer** (37-280 µm vs 26-29 µm) and grows with m_Q (slower quirks).
   - A χ² that ignores MS will be wrong by factors of several in the OT. MS must be in the fit covariance or as broken-line kinks.
   - The thin-scatterer MS here matches T3's continuous-MS thickness floor of 10-25 µm (T3 §3.2) in order of magnitude.

### 2.4 Is it linear enough? Fit strategy
- **Linearity in the parameters** (`code/T4_comb.py`, `figures/T4_comb.png`; one event, m = 500 GeV; ESTIMATE). Along the oscillation-scale direction (ln ℓ₀ at fixed velocities):
  - χ²(δ) stays quadratic (the ratio χ²/(δ/σ_loc)² is constant within 10 %) up to |δ| ≈ 0.07/N_osc (1 keV, N_osc = 9), 0.02/N_osc (3 keV, N_osc = 83) and 0.1-0.3/N_osc (10 keV, N_osc = 920).
  - In words: **the model is linear only while the predicted oscillation phase at the last layer is within ≈ 2-10 % of a cycle.**
  - Outside that range χ² rises steeply, by 10⁴-10⁸ within one cycle. At 10 keV there is a secondary minimum at δ ln ℓ₀ ≈ 0.8/N_osc, with Δχ² = 3.6×10³: an aliasing alternative that a local minimiser can fall into.
  - Along the vacuum-degenerate direction (ln σ at fixed ℓ₀ and velocities: the pure B handle) χ² is smooth and quadratic over ±50 %.
- **Kalman filter: not natural.**
  - The causal string has memory (a queue of string segments), so the state is not (x, p) of two points.
  - The two quirks are coupled, with 2-3 hits per layer and an unknown assignment.
  - The phase-linearity window above (≤ 0.1 cycle) is narrower than what a layer-by-layer filter can keep at Λ ≳ 3 keV, where 3-300 oscillations happen between layers (Sec. 6).
- **Recommended: a global iterated least-squares fit** around the causal reference trajectory (Gauss-Newton / Levenberg-Marquardt).
  - 9 parameters (+1 material scale), with MS either in the covariance or as explicit broken-line kinks (2 per scatterer crossing, General-Broken-Lines style; this is exactly the Jacobian structure computed in `T4_fisher.py`).
  - Seed chain:
    1. vacuum closed form fitted to the IT hits;
    2. ℓ₀ from the crossing spacing/width;
    3. MET for p_T;
    4. BTL time for β_T;
    5. a 1-D phase scan in ln ℓ₀ over ±1/N_osc to pick the global minimum;
    6. full fit.
  - Cost: ~20 propagator calls per iteration × ≤ 10 iterations ≈ 0.2-20 s per candidate at Λ = 1-10 keV (numba; ESTIMATE).
  - This is fine offline on plane-finder candidates, too slow for the HLT except at Λ ≲ 1 keV.

## 3. Degeneracies: what the hits measure (Q2, Q3)

### 3.1 Exact statements (from the scaling of Sec. 2.1)
1. **Positions alone, in vacuum, measure ℓ₀ = m_Q/σ and the velocities, never m_Q and Λ separately.**
   - The measured set is (ℓ₀, (βγ)_T, φ, η, γ*, cosθ*, φ*, z₀): 8 numbers.
   - Absolute momenta are invisible: P_QQ̄ = 2γ* m_Q (βγ)_pair needs m_Q.
   - The familiar shorthand "ℓ_max ∝ (γ*−1)m_Q/Λ²" is the special case ℓ_max = 2(γ*−1)ℓ₀ [T2 §2.2].
   - The vacuum Fisher matrix confirms this. Its ln σ column, at fixed (ℓ₀, velocities), is ≤ 3×10⁻⁷ of the largest column, i.e. numerical noise (Sec. 4).
2. **Timing (OT/IT BX tags, MTD BTL σ_t ≈ 35 ps) measures velocities only:**
   - the pair β_T from the arrival time t = R/β_T at the BTL;
   - the oscillation phase from the time difference between the two quirks.
   - Timing removes correlations among the velocity parameters (Sec. 4.2: σ(ln ℓ₀) improves ×3-25). It does **not** lift the m/σ degeneracy.
3. **dE/dx measures the per-hit βγ, hence velocities again.** The Bethe-Bloch shape depends on βγ and q only. It is redundant with the trajectory shape for the mass, and adds nothing to σ(m) in Sec. 4 (rows M2 → M3).
   - The statement "dE/dx will be important to measure the mass and string tension" [1708.02243 App.A] holds only in combination with a momentum measurement.
4. **Only three things break the degeneracy:**
   - (a) **the magnetic field**, through ε_B = qBc/σ, which measures **σ = Λ² directly, independently of m_Q**;
   - (b) **the external momentum scale**, i.e. MET = p_T(QQ̄) in a monojet event: m_Q = p_T/(2γ*(βγ)_T), then σ = m_Q/ℓ₀;
   - (c) **material**, through 1/m_Q: the mean energy loss is deterministic but depends on the material budget; MS is stochastic.
   - Everything else (shape, period, crossing spacing, width, timing, dE/dx) measures ℓ₀ and velocities.
   - This turns the T2 proposal G-T2-4 into a precise statement. D, w_T and β_pair over-determine (ℓ₀, γ*, β), not σ. The recoil p_T is what gives m_Q.

### 3.2 How the B field enters, and whether it is a usable Λ meter (Q3)
**Size of the B-field displacement of the hits.** These are the RMS of y(3.81 T) − y(vacuum) per layer (Sec. 2.3 table). They are fitted by x_B ≈ c · ε_B · R with c ≈ 0.5 (ESTIMATE):
  - 3-130 µm in rφ at Λ = 1 keV, growing ≈ linearly with R;
  - 0.5-20 µm at 3 keV.
  - The ratio of 7-9 between 1 and 3 keV means x_B ∝ Λ^−1.8…−2, **not the Λ⁻⁴ (∝ m_Q/Λ⁴) of the analytic thickness formula** [1911.02223 Eq.III.12]. This agrees with T2/T3, who found that the causal thickness falls as Λ^−2…−2.5.
  - At fixed velocities it is **nearly m_Q independent** (Sec. 2.3), as expected for a term ∝ ε_B·R = qBR/σ.

**Physical picture (ESTIMATE, partly a hypothesis).**
- For a neutral pair, P(t) = P₀ + q(x₁−x₂)×B holds exactly, because the causal string conserves total 4-momentum.
- The measured displacement is mostly **in the plane** (rφ). It grows linearly with R, is ∝ 1/σ and is m_Q independent at fixed velocities. That is the signature of a small change of the centre-line direction relative to P₀, of order ε_B ~ 10⁻⁴ (keV/Λ)².
- T3 finds the **out-of-plane** secular rotation to be only 3-18 µrad at 0.6-1 keV and below the MS floor (T3 §4.2). The two results are compatible: the in-plane part does not tilt the plane.
- Most of a rigid rotation is absorbed by the fitted (φ, η). Only the non-rigid part (the kink at the vertex and the R dependence) carries information on σ. The Fisher matrix profiles this automatically, and the numbers in Sec. 4 are after that profiling.

**The B response is not analytic (linear) in B** (ESTIMATE, `T4_fisher.py`; scaling test on 6 hits).
- Divide the hit displacement by B: from B/80 to B it changes smoothly by a factor 0.66 for the large displacements. That is an effective exponent x_B ∝ B^0.91 between 0.05 and 3.8 T.
- Consistently, "vacuum + 20 × (response at B/20)" misses the 3.8 T hits by 30-40 % of the B effect at every layer and every Λ (Sec. 2.3).
- **A model "exact vacuum + first-order-in-B correction" is therefore not accurate to better than ~35 % of the B effect.** The fit model must be the full causal propagator.
- A plausible origin (not proven): the crossings, where the miss distance b ∝ B [T2 §5.3] sets the local string geometry, producing B log B-type terms.

**Verdict on Q3.**
- **Yes in principle.** The B field is the only *intrinsic* handle on Λ, independent of the recoil and of m_Q.
- **How much is left after MS** (Cramér-Rao, positions only, B + MS, all other parameters profiled; Sec. 4, row P2):

| Λ | per event σ(Λ)/Λ | N = 30 events |
|---|---|---|
| 1 keV | 16-20 % (median) | 1.5-2.2 % |
| 3 keV | 170-220 % | 17-29 % |
| 10 keV | unmeasured | unmeasured |

- MS degrades the no-MS result by ×2-4: P1 gives 6-8 % per event at 1 keV.
- **So the B handle is useful at Λ ≲ 2 keV only.** This is consistent with T3's conclusion that the B-field thickness exceeds the MS floor only for Λ ≲ 1.5 keV (T3 §4.2).
- The scaling "∝ q B m_Q/Λ⁴" [1911.02223 Eq.III.12] is the wrong guide here. The displacement that carries information is ∝ qBR/Λ², independent of m_Q, so the B handle measures Λ, not m_Q/Λ⁴.

## 4. Measurement of (m_Q, Λ) after discovery (Fisher / Cramér-Rao)

### 4.1 Method (ESTIMATE; `code/T4_fisher.py`, `code/T4_fisher_report.py`, output `figures/T4_fisher_report_out.txt`, figure `figures/T4_fisher_summary.png`)
- **Events and model.** 16 LO DY+ISR events per point (T2 cache; fermion E; p_T(QQ̄) > 200 GeV; |η| < 1). Causal string, uniform 3.81 T, thin-scatterer material.
- **Jacobians.** Central finite differences in the natural parameters u (Sec. 2.2), with adaptive steps (≈ 20 µm hit shifts). The vacuum symmetry direction is therefore exact and free of numerical cancellation.
  - A first version in the physical parameters (ln m, ln p_T, ln Λ) gave a spurious 1 % vacuum "measurement" of m_Q from finite-difference cancellation error. It was discarded.
- **Measurement vector.**
  - Per hit (quirk, layer, crossing): rφ and z, with Phase-2 resolutions (Sec. 2.3).
  - BTL arrival time of each quirk, σ_t = 35 ps. The MTD TDR quotes ≈ 30-40 ps at the start of life and 50-60 ps at the end [theory_signal_model §4.1, UNVERIFIED].
  - IT ln(dE/dx) per hit, 25 % resolution (4-bit ToT; UNVERIFIED; saturation ignored).
- **Covariance.** Resolution plus MS. The MS part is J_ξ J_ξᵀ, from 2 deflections per material crossing per quirk, i.e. ≈ 50-100 nuisance directions per event.
- **Priors.**
  - MET: σ⊥ = 25 GeV per component (PU 200, PUPPI; UNVERIFIED; scanned 15/35 GeV), on p_T and φ of the pair.
  - PV z₀: 30 µm.
  - Material scale: 10 %. In the ensemble it is a single shared nuisance.
- **Ensemble.** m_Q and Λ are common to all events; every other parameter is per event. Per-event Schur complements on (ln m, ln Λ) are summed and scaled to N = 10/30/100.
- **Caveats (all make the real resolution worse).**
  - Local Cramér-Rao bound: it assumes the fit converged to the global minimum (aliasing, Sec. 2.4) and that the hit-to-quirk assignment is known.
  - No PU or noise hits; no straggling; no misalignment.
  - Finite-difference noise of ±10 % on the Jacobians at 10 keV.

### 4.2 What the hits measure per event (natural parameters, ln σ fixed; per-event median 1σ)

| m_Q, Λ | positions + MS: σ(ln ℓ₀) | σ(ln(βγ)_T) | σ(ln(γ*−1)) | + BTL + IT dE/dx: σ(ln ℓ₀) | σ(ln(βγ)_T) | σ(ln(γ*−1)) |
|---|---|---|---|---|---|---|
| 200, 1 / 3 / 10 | 1.2 / 1.1 / 0.9 % | 0.4 / 0.9 / 0.9 % | 1.2 / 1.9 / 1.7 % | 0.44 / 0.10 / 0.09 % | 0.20 / 0.16 / 0.08 % | 0.45 / 0.26 / 0.18 % |
| 500, 1 / 3 / 10 | 2.9 / 0.9 / 0.8 % | 1.3 / 0.6 / 0.5 % | 3.0 / 1.2 / 1.3 % | 0.27 / 0.05 / 0.04 % | 0.12 / 0.07 / 0.04 % | 0.30 / 0.16 / 0.09 % |
| 1000, 1 / 3 / 10 | 1.2 / 0.35 / 0.34 % | 0.5 / 0.2 / 0.3 % | 1.2 / 0.5 / 0.6 % | 0.18 / 0.03 / 0.02 % | 0.08 / 0.03 / 0.02 % | 0.19 / 0.05 / 0.03 % |

- The pair direction is measured to σ_φ ≈ 3×10⁻⁵ rad and σ_η ≈ 2×10⁻⁴.
- **The trajectory determines ℓ₀ = m_Q/Λ² and all velocities to the 10⁻³-10⁻² level per event.**
- BTL timing improves these by ×3-25, by fixing β_T and breaking the β_T-ℓ₀ correlation.
- None of this constrains m_Q and Λ separately.

### 4.3 Expected resolutions on m_Q and Λ (the open problem "parameter measurement after discovery", G-T5-7)
Relative 1σ, ESTIMATE. "per ev." is the median over events, with the 16-84 % range in brackets in the report output. **Rows:**
- **B-only:** positions + MS, no external information. This is the intrinsic handle through ε_B = qB/σ.
- **+MET:** B-only + MET (25 GeV) + PV + BTL + IT dE/dx. This is the realistic full set.
- **eloss:** B-only + the mean energy-loss model with a 10 % material-scale nuisance, no MET.

| m_Q [GeV] | Λ [keV] | handle | σ(m)/m per ev. | σ(Λ)/Λ per ev. | N = 10: σ(m)/m, σ(Λ)/Λ | **N = 30** | N = 100 |
|---|---|---|---|---|---|---|---|
| 200 | 1 | B-only | 36 % | 17 % | 7.3 %, 3.7 % | **4.2 %, 2.1 %** | 2.3 %, 1.2 % |
| 200 | 1 | +MET | 9.2 % | 4.6 % | 2.0 %, 1.0 % | **1.2 %, 0.6 %** | 0.6 %, 0.3 % |
| 200 | 3 | B-only | 370 % | 180 % | 59 %, 29 % | **34 %, 17 %** | 19 %, 9 % |
| 200 | 3 | +MET | 9.5 % | 4.8 % | 2.1 %, 1.0 % | **1.2 %, 0.6 %** | 0.7 %, 0.3 % |
| 200 | 10 | B-only | — | — | — | **unmeasured (> 100 %)** | 160 %, 80 % |
| 200 | 10 | +MET | 9.6 % | 4.8 % | 2.1 %, 1.0 % | **1.2 %, 0.6 %** | 0.7 %, 0.3 % |
| 500 | 1 | B-only | 40 % | 20 % | 7.8 %, 3.9 % | **4.5 %, 2.2 %** | 2.5 %, 1.2 % |
| 500 | 1 | +MET | 7.2 % | 3.6 % | 1.7 %, 0.9 % | **1.0 %, 0.5 %** | 0.6 %, 0.3 % |
| 500 | 3 | B-only | 350 % | 170 % | 80 %, 40 % | **46 %, 23 %** | 25 %, 13 % |
| 500 | 3 | +MET | 7.8 % | 3.9 % | 1.8 %, 0.9 % | **1.0 %, 0.5 %** | 0.6 %, 0.3 % |
| 500 | 10 | B-only | — | — | — | **unmeasured** | 370 %, 190 % |
| 500 | 10 | +MET | 7.8 % | 3.9 % | 1.8 %, 0.9 % | **1.0 %, 0.5 %** | 0.6 %, 0.3 % |
| 1000 | 1 | B-only | 35 % | 16 % | 5.2 %, 2.6 % | **3.0 %, 1.5 %** | 1.6 %, 0.8 % |
| 1000 | 1 | +MET | 5.8 % | 2.9 % | 1.6 %, 0.8 % | **0.9 %, 0.5 %** | 0.5 %, 0.25 % |
| 1000 | 3 | B-only | 440 % | 220 % | 100 %, 51 % | **58 %, 29 %** | 32 %, 16 % |
| 1000 | 3 | +MET | 6.1 % | 3.0 % | 1.7 %, 0.9 % | **1.0 %, 0.5 %** | 0.5 %, 0.3 % |
| 1000 | 10 | B-only | — | — | — | **unmeasured** | 310 %, 150 % |
| 1000 | 10 | +MET | 6.1 % | 3.0 % | 1.7 %, 0.9 % | **1.0 %, 0.5 %** | 0.5 %, 0.3 % |
| all | 3-10 | eloss | 27-270 % | 13-130 % | ≈ 10-18 %, 5-9 % | **≈ 10-13 %, 5-6 %** | → 10 %, 5 % (material-prior floor) |

Variants and the pair momentum (ESTIMATE):
- **MET resolution.** σ⊥ = 15 (35) GeV scales the +MET column to 0.6-0.7 % (1.2-1.7 %) in m_Q at N = 30. The m_Q resolution is MET-statistics dominated.
- **Pair momentum.** σ(p_T)/p_T per event = 6-10 % with MET: the MET resolution itself, slightly improved by the hits. From hits + B alone it is 33-40 % at 1 keV and unmeasured above 3 keV. **The hits do not measure the pair momentum; the recoil does.**
- **Correlation.** ρ(m, Λ) = +0.95…+1.00 in every configuration. The measured combination is ℓ₀ = m/Λ² (Sec. 4.2), so σ(Λ)/Λ = ½ σ(m)/m.

### 4.4 Reading and systematics
1. **With the recoil, m_Q and Λ are measured at the per-cent level with ~30 events, at every point of the grid.**
   - m_Q comes from p_T(QQ̄) = MET and the velocities measured by the trajectory and the BTL: m_Q = p_T/(2γ*(βγ)_T).
   - Λ then follows from ℓ₀, with half the relative error.
   - The **systematic floor** is the MET/recoil energy scale. A common JES/MET-scale uncertainty δ_s (≈ 1-3 % for a 300 GeV hadronic recoil; UNVERIFIED) gives δm/m ≈ δ_s and δΛ/Λ ≈ δ_s/2. With 30 events the measurement is systematics-limited at ≈ 2 % on m_Q and ≈ 1 % on Λ.
   - Additional model systematics: ISR mis-modelling does **not** enter, because the recoil is measured event by event. The quirk charge enters through ε_B, and the spin only through the generator distributions.
2. **Without the recoil** (e.g. to cross-check the MET scale), only the B field breaks the degeneracy. It reaches 1.5-2.2 % on Λ (3-4.5 % on m_Q) at Λ = 1 keV with 30 events, 17-29 % at 3 keV, and nothing at 10 keV.
   - This is an **independent, recoil-free** determination of Λ at the low-Λ edge. It is the natural MET-scale calibration for quirks there.
3. **dE/dx and timing do not measure the mass** (rows M2/M3 = M1 for m_Q). They measure velocities, already known from the shape. They matter for background rejection and for fixing ℓ₀, which drops ×3-25 with BTL. The dE/dx–β relation of [1708.02243 App.A] measures only β.
4. **Mean energy loss** is a third, fragile mass handle. Its effect is ∝ (material scale)/m_Q, so it measures m_Q only as well as the material budget is known (the 10 % floor in the table).
5. **Exclusive production as an absolute mass scale.** T6's exclusive PPS events (35 events at 500 GeV) give M_QQ̄ directly from the protons. Combined with γ* from the trajectory (0.2-3 % per event) that is an independent m_Q, free of the MET scale. It is not quantified here.

## 5. Event-level handles: MET alignment, quirk-hypothesis χ², trigger features (Q4)

### 5.1 (a) Strip axis ∥ MET (open problem G-T5-10; [1708.02243 Sec.III.C] "n₃ is expected to be aligned with MET")
**Physics (exact in vacuum).**
- The pair centre moves on the straight line from the PV along P_QQ̄ [T2 §2.1], so the transverse strip axis is φ_pair.
- In 3.8 T the CM momentum oscillates by q(x₁−x₂)×B, which is ≤ qBℓ_max ≈ 0.06 GeV for ℓ_max = 5 cm. That is an angular wobble ≲ 2×10⁻⁴ rad. The fitted strip axis has σ_φ ≈ 3×10⁻⁵ rad from the hits (Fisher, Sec. 4).
- The pair deposits ≲ 5 GeV in the calorimeters within 25 ns [1911.02223 Sec.V], so the true MET equals p_T(QQ̄).
- **The alignment is therefore limited only by the MET resolution σ⊥ per component.** σ⊥ at PU 200 is UNVERIFIED (PUPPI), so it is scanned over 15/25/35 GeV.

**Background.**
- For random PU-hit planes, the strip azimuth is uniform relative to the MET.
- A cut |Δφ| < δ keeps a fraction δ/π of them (geometric ESTIMATE, as in G-T5-10).

**Numbers** (ESTIMATE, `code/T4_met.py`, `figures/T4_met_alignment.png`). LO DY+ISR pairs with p_T(QQ̄) > 200 GeV and |η| < 1.

| m_Q | σ⊥ [GeV] | median \|Δφ\| | 95 % quantile | signal eff. \|Δφ\| < 0.2 | random-plane rejection at 95 % signal eff. |
|---|---|---|---|---|---|
| 200 | 15 / 25 / 35 | 0.030 / 0.050 / 0.070 | 0.105 / 0.175 / 0.248 | 0.999 / 0.970 / 0.903 | **×30 / ×18 / ×13** |
| 500 | 15 / 25 / 35 | 0.025 / 0.041 / 0.058 | 0.096 / 0.161 / 0.226 | 0.999 / 0.979 / 0.927 | ×33 / ×20 / ×14 |
| 1000 | 15 / 25 / 35 | 0.022 / 0.037 / 0.052 | 0.092 / 0.152 / 0.215 | 0.999 / 0.982 / 0.938 | ×34 / ×21 / ×15 |

**Reading.**
- A single cut |Δφ(MET, strip)| < 0.15-0.25 rad keeps 95 % of the signal and rejects random planes by ×13-34.
- In the factorised background estimate this is the factor f_MET-plane [STRATEGY_DRAFT D10]. It is directly measurable in the low-MET control region, where real MET ≈ 0 makes the MET direction random. It is worth ×13-34 against the dominant B1/B2 background.
- **The MET direction can also seed the plane finder.** Restricting the seed wedge to |φ − φ_MET| < 0.2 rad cuts the combinatorics by π/0.2 ≈ 16 before any plane is built. This addresses the latency concern of [1708.02243 Sec.III.C].
- **Caveat 1: fake-MET events** (QCD with a mismeasured jet). There the MET is (anti-)parallel to a jet, and residual hits from that jet are aligned with the MET. The standard Δφ(jet, MET) > 0.5 cleaning cut removes this correlation. It must be applied *before* the alignment cut is counted as an independent factor.
- **Caveat 2: the rejection is only in φ.** MET carries no η information, so the plane tilt about the strip axis is not constrained.

### 5.2 (b) The quirk-pair hypothesis χ² vs unrelated hits (shared plane, centre line, period)
**Constraint counting.**
- The two quirks share every one of the 9 parameters: one vertex, one P_QQ̄, one γ*, one axis, one ℓ₀ and one ε_B.
- So the pair is described by 9 numbers, against ≈ 50-130 measurements (Sec. 2.2).
- Two *unrelated* oscillating tracks would need 2 × 9 − 1 (common vertex) = 17. The shared-pair hypothesis therefore imposes ≈ 8 extra constraints.
- The coplanar finder uses only 2 of them: the plane normal through the PV.

**Predictive power (the quantitative form of "one plane, one CM, one period").**
- Fit the model (B + MS + MET + PV priors, linearised) to the hits on layers < L. Then predict the rφ position of the hits on layer L.
- ESTIMATE, `T4_fisher_report.py` section (4). Median 1σ prediction vs the median rφ separation of the two quirks on that layer (≈ the strip width the coplanar finder has to accept):

| m_Q, Λ | IT3 | IT4 | PS1-PS3 | 2S1-2S3 | quirk separation (OT) |
|---|---|---|---|---|---|
| 200, 1 keV | 183 µm | 19 µm | 32-43 µm | 39-40 µm | 8-10 mm |
| 500, 1 keV | 27 | 14 | 32-38 | 38-39 | 5-9 mm |
| 1000, 1 keV | 31 | 14 | 33-45 | 45-46 | 16-24 mm |
| 200, 3 keV | 88 | 22 | 32-41 | 41-43 | 0.8-1.2 mm |
| 500, 3 keV | 17 | 13 | 33-42 | 40-43 | 0.5-1.0 mm |
| 1000, 3 keV | 25 | 15 | 35-43 | 42-55 | 2.0-2.8 mm |
| 200-1000, 10 keV | 19-42 | 15-21 | 34-51 | 48-58 | 50-230 µm |

**Reading (ESTIMATE).**
- After the IT doublet/triplet that fixes the phase, every subsequent hit is predicted to ≈ 15-55 µm (1σ). That is ≈ 1-2 × (resolution ⊕ MS).
- Inside the plane, a ±3σ window covers a fraction 6σ_pred/separation of the strip the coplanar finder accepts:
  - ≈ 1/20-1/100 per OT layer at 1 keV;
  - ≈ 1/2-1/10 at 3 keV;
  - ≈ 1 at 10 keV, where the strip is as narrow as the prediction.
- **For a random PU hit lying in the plane, the quirk-χ² requirement therefore suppresses the probability per layer by these factors.** With ≥ 4 OT layers required, a random coplanar set would have to pass ×(20-100)⁴ ≈ 10⁵-10⁸ more at Λ ≈ 1 keV and ×10-10⁴ at 3 keV, on top of Δs < 100 µm.
- At Λ ≳ 10 keV the in-plane prediction adds nothing beyond the plane cut. The pattern is then the merged-like zig-zag band (Sec. 6), and the extra rejection must come from the out-of-plane residual, dE/dx and timing.
- Caveat: this is an *idealised* figure. It assumes the inner hits were correctly assigned. The background tail is then set by wrong assignments and partial quirk + PU combinations, which needs a hit-level study (Phase 2).
- **A practical "quirk-hypothesis χ²"** is the χ² of the 9-parameter causal fit with the MS covariance, compared with the χ² of the same hits fitted as two independent 5-parameter helices. It must be calibrated on signal MC (MS model) and on inverted-Δs sidebands (strategy M1).

### 5.3 (c) Trigger-level features (theory side; brief)
1. **L1 track trigger.** Only 23-47 % of quirk OT crossings at Λ = 0.3-3 keV produce a stub within a 2 GeV bend window (76-89 % at 10 keV; Sec. 6). The two quirks' stubs do not form a consistent helix.
   - **Quirks are therefore largely invisible to L1 tracking.** They are not a source of L1 tracks that could fake prompt leptons, and they cannot be triggered on by L1 tracks below ~10 keV.
2. **L1 MET φ + OT activity.** 2-3 OT clusters per layer within one narrow φ road (width w_T = 0.02-6 cm at 1-10 keV) aligned with L1 MET φ (Sec. 5.1: |Δφ| ≲ 0.2). This is an L1-scouting-type pattern: cluster-pair multiplicity in a φ-road. The hardware feasibility is out of scope (G-T5-9).
3. **Timing.** All quirk OT hits are late by 1-18 ns (T3 §6). At HLT, a BTL/ETL time-of-flight-delayed track segment aligned with the MET φ is a clean slow-pair tag.

## 6. Seeding and local signatures (Q5)
Method: ESTIMATE, `code/T4_local.py`, `figures/T4_local.png`.
- 60 LO DY+ISR events per point, causal string in 3.8 T, no material.
- OT stub partner sensors are at R + d, with d = 1.6/2.6/2.6 mm (PS) and 1.8 mm (2S). These spacings are UNVERIFIED.
- Apparent stub p_T = 0.3BR/(2 sin|α|), with tan α = Δ(rφ)/d.

| m_Q | Λ [keV] | ΔN_osc between layers: IT1→IT2 / IT4→PS1 / 2S2→2S3 | OT stubs with p_T,app > 2 GeV | triplet (3 consecutive layers, one quirk): median p_T,app [GeV]; frac < 2 GeV | triplets curving towards the partner | non-monotonic quirk-quirk separation vs r | hits per layer (IT1…2S3) |
|---|---|---|---|---|---|---|---|
| 200 | 0.3 | 0.03 / 0.11 / 0.24 | 0.47 | 1.8; 0.52 | 0.97 | 0.98 | 1.9-2.4 |
| 200 | 1 | 0.37 / 1.2 / 2.7 | 0.36 | 1.6; 0.54 | 0.87 | 1.00 | 2.1-2.4 |
| 200 | 3 | 3.4 / 11 / 24 | 0.36 | 14; 0.15 | 0.86 | 1.00 | 2.1-2.3 |
| 200 | 10 | 37 / 120 / 270 | 0.89 | 160; 0.00 | 0.86 | 1.00 | 2.2-2.3 |
| 500 | 0.3 | 0.04 / 0.12 / 0.27 | 0.42 | 4.1; 0.38 | 0.97 | 0.95 | 1.8-2.9 |
| 500 | 1 | 0.41 / 1.4 / 3.0 | 0.25 | 1.2; 0.62 | 0.88 | 1.00 | 2.8-3.2 |
| 500 | 3 | 3.7 / 12 / 27 | 0.23 | 11; 0.18 | 0.79 | 1.00 | 2.8-3.0 |
| 500 | 10 | 41 / 140 / 300 | 0.76 | 110; 0.01 | 0.89 | 1.00 | 2.7-3.0 |
| 1000 | 0.3 | 0.03 / 0.11 / 0.24 | 0.36 | 2.2; 0.49 | 0.96 | 0.97 | 2.0-2.8 |
| 1000 | 1 | 0.38 / 1.3 / 2.7 | 0.25 | 1.3; 0.59 | 0.86 | 1.00 | 2.4-2.9 |
| 1000 | 3 | 3.4 / 11 / 24 | 0.26 | 8.5; 0.21 | 0.84 | 1.00 | 2.4-2.8 |
| 1000 | 10 | 38 / 130 / 270 | 0.80 | 95; 0.02 | 0.83 | 0.98 | 2.4-2.9 |

**Reading (ESTIMATE).**
1. **Two regimes, separated by ΔN_osc ≈ 0.5 between consecutive layers.**
   - The number of oscillations between radii r₁ < r₂ is σ(r₂−r₁)/(2β*p_T) [T2 §2.2], independent of m_Q.
   - **Resolved regime, Λ ≲ 1 keV in the IT (≲ 0.5 keV in the OT).** The oscillation is followed layer to layer. Local curvature is a strong signature: triplets of one quirk have apparent p_T ≈ 1-4 GeV for a quirk of p ≈ 100s of GeV, and both quirks curve towards each other in 87-97 % of triplets.
   - **Aliased regime, Λ ≳ 3 keV.** There are 3-300 oscillations between layers, so consecutive hits of one quirk sample an effectively random phase. Local curvature carries no dynamical information (apparent p_T 10-160 GeV). The pattern is then a **zig-zag band**: 2-3 hits per layer, all within ±w_T/2 of a straight, zero-curvature line through the PV.
   - The best seed in the aliased regime is a *straight-line* doublet/triplet through the PV with a hit pair at every layer, plus the MET-φ wedge (Sec. 5.1). The separation of the pair varies non-monotonically with r (98-100 % of events at every Λ), whereas opposite-charge helix pairs from one vertex separate monotonically.
2. **The most distinctive places along the trajectory.**
   - **(i) The first half-oscillation near the vertex.** In the IT for Λ ≲ 3 keV, the two quirks leave the PV back to back in the CM. The first turning point lies at ℓ_max/2 from the CM line: 1.5-4 cm at 1 keV, 0.15-0.4 cm at 3 keV.
     - Here the pattern is a *pair of opposite-curvature arcs from one point*, with curvature radius ~ℓ₀ = m/σ.
     - The B-field and MS perturbations are smallest here (Sec. 2.3 table: B effect ≤ 3 µm at IT1).
     - The vacuum closed form [2002.07503 Eq.II.4-8; T2 `ExactPair`] is valid there to < 1 resolution unit, so it is the ideal seed model.
   - **(ii) The turning points.** There the quirk moves slowly in the CM and its lab velocity is the pair velocity. The local direction then points along the CM line, which makes the turning point the place where a straight-line seed works.
   - **(iii) The crossings.** The two quirks pass within b ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3]. Two hits from different quirks on one layer within < 2 pixels occur only near crossings. Merged clusters near the CM line are therefore expected and should not be vetoed.
3. **L1 stubs.**
   - Only 23-47 % of the quirk OT layer crossings at 0.3-3 keV give a stub inside a 2 GeV bend window (36-47 % at m_Q = 200 GeV); 76-89 % do at 10 keV.
   - Quirks are therefore largely invisible to the L1 track finder at Λ ≲ 3 keV, which also requires stub consistency across layers that the oscillation breaks.
   - Trigger-level handles that remain (theory side): (a) a **wide-bend stub/cluster-pair multiplicity in a narrow φ wedge aligned with L1 MET φ** (2-3 OT hits per layer within ≲ w_T of one φ: 0.2-6 cm at 1-10 keV, 500 GeV); (b) at Λ ≳ 10 keV, ordinary high-p_T stubs from both quirks along one straight line, i.e. a *pair of nearly overlapping high-p_T L1 tracks*. The L1 implementation is out of scope (G-T5-9).
4. **The rφ midpoint of the two quirks' hits is not a clean "CM track".** Its RMS distance from the CM line is 0.35-0.5 of the half-separation, because the two hits on a layer are taken at different times. The CM line has to come from the fit, not from midpoints.

## 7. Gap entries

### G-T4-1 A 9-parameter causal quirk-pair fit model exists and is strongly predictive; the strategy's "straight-string EoM fit" and any vacuum + first-order-B shortcut are not adequate
- **Current treatment.**
  - The strategy plans to "fit the straight-string EoM (with B and mean dE/dx) … uses the analytic first-order solution as a fast seed" [STRATEGY_DRAFT §9.1].
  - No published trajectory fit exists [1708.02243 Sec.IV "obvious way…", 1911.02223 Sec.V "future work"; T5 G-T5-7].
  - GNN approaches classify edges with no physics model [2410.00269].
- **Why it is a gap.**
  - Straight strings are uncontrolled at O(F_ext) (G-T2-1).
  - Here: the B response is not linear in B (30-45 % misses for a linear-in-B model).
  - The mean energy loss shifts OT hits by 40 µm-1.5 mm.
  - MS exceeds the resolution in every OT layer (Sec. 2.3).
- **Estimate.**
  - The model has 9 parameters (vertex z, P_QQ̄, γ*, CM axis, m_Q, Λ) plus MS kinks.
  - Once the IT hits fix the phase, it predicts each later hit to 15-55 µm (1σ), against strips 0.5-24 mm wide at Λ = 1-3 keV.
  - It is locally linear only within ≈ 2-10 % of an oscillation cycle at the last layer (Sec. 2.4), so it needs a phase-scan seed.
  - Cost ≈ 0.2-20 s per candidate.
- **Exploitation:** (c) the reconstruction model for approach (a) of the strategy, and GNN training targets; (b) background rejection ×10⁵-10⁸ (1 keV) and ×10-10⁴ (3 keV) beyond the plane cut for random in-plane hits (Sec. 5.2); (d) the measurement below.
- **Effort:** weeks, to port `T4_model.kernel` + Gauss-Newton into a CMSSW-side fitter. **Confidence:** medium-high for the model; medium for the rejection, which is idealised (known assignment, no PU).
- **Verdict: EXPLOIT.**

### G-T4-2 Degeneracy theorem: trajectory, timing and dE/dx measure only ℓ₀ = m_Q/Λ² and velocities; m_Q comes from the recoil (or B at low Λ)
- **Current treatment.**
  - Thought to be measurable from the hits: "dE/dx will be important to measure the mass and string tension" [1708.02243 App.A]; "a trajectory fit measures m_Q and Λ" [STRATEGY_DRAFT §3 item 5].
  - Dimensional estimates m_Q ~ B ℓ²/d [T5 G-T5-7].
- **Why it is a gap.**
  - Exact scale invariance (Sec. 2.1): with ε_B and material switched off, positions and times depend on m_Q and σ only through ℓ₀. dE/dx depends only on βγ.
  - The Fisher matrix confirms it: the vacuum ln σ column is ≤ 3×10⁻⁷ of the largest of the largest.
  - **No amount of hit information gives m_Q without a momentum scale.** Only three exist: the recoil MET, ε_B = qB/σ, and material.
- **Estimate** (Sec. 4.3, N = 30 events).
  - With the MET: σ(m)/m ≈ 0.9-1.2 % and σ(Λ)/Λ ≈ 0.5-0.6 % at every (m_Q, Λ) in {200, 500, 1000} GeV × {1, 3, 10} keV. Per event it is 6-10 % (m_Q) and 3-5 % (Λ).
  - Systematics floor ≈ the MET/JES scale (≈ 1-3 %, UNVERIFIED).
  - The trajectory itself gives ℓ₀ to 0.02-3 % and γ* to 0.03-3 % per event.
- **Exploitation:** (d) the first quantitative answer to "parameter measurement after discovery"; (f) a short pheno note; (e) it removes dE/dx as a claimed mass handle.
- **Effort:** days to write up. **Confidence:** high for the theorem; medium for the numbers (CRB, idealised).
- **Verdict: EXPLOIT.**

### G-T4-3 The B field gives an intrinsic, recoil-free Λ measurement, but only for Λ ≲ 2 keV
- **Current treatment.** The thickness formula d ∝ qBm_Q/Λ⁴ [1911.02223 Eq.III.12] is proposed to combine with ℓ and l to give m_Q and Λ [T5 G-T5-7].
- **Why it is a gap.**
  - The informative B displacement is mostly in-plane, ≈ 0.5 ε_B R ∝ qBR/Λ², and m_Q independent. It is not ∝ m_Q/Λ⁴.
  - MS competes with it.
  - The secular out-of-plane precession is negligible (T3 §4.2).
- **Estimate** (positions + MS only).
  - σ(Λ)/Λ = 16-20 % per event and 1.5-2.2 % for 30 events at Λ = 1 keV.
  - 17-29 % (N = 30) at 3 keV.
  - Unmeasurable at 10 keV.
- **Exploitation:** (d) MET-scale-independent cross-check of Λ at the low edge of the coplanar window; (e) checks the B-field modelling of the signal MC.
- **Effort:** weeks (it comes with G-T4-1). **Confidence:** medium (MS model from T3 / thin scatterers; material UNVERIFIED).
- **Verdict: WORTH A CHECK.**

### G-T4-4 The B response of the causal string is not linear in B
- **Current treatment.** First-order perturbation in F_ext/σ is the basis of all analytic thickness formulas [2002.07503 Eq.V.6; 1911.02223 Eq.III.12]. T2 showed the straight-string versions are wrong at that order.
- **Why it is a gap.**
  - The exact causal string's hit displacement per unit B changes by a factor 0.66 between B/80 and B (effective exponent 0.91).
  - "Vacuum + 20 × response(B/20)" misses 30-45 % of the 3.8 T effect at every layer, for Λ = 1-3 keV and all masses.
  - The likely origin is the crossings (b ∝ B), which would give B log B terms. Not proven.
- **Estimate.** 25-50 µm in the OT at 1 keV: 1-2 × resolution.
- **Exploitation:** (c) any analytic/perturbative fast model must be calibrated against the full causal propagator; (f) a theory question (non-analytic response of a Nambu-Goto string with massive ends near reconnection).
- **Effort:** days to confirm with T2/T3 codes and a smaller max_boost. **Confidence:** medium (consistent across 9 points; a numerical artefact of the first-order B kick is not excluded, although T3 found 1-1.5 % convergence).
- **Verdict: WORTH A CHECK.**

### G-T4-5 MET-strip alignment: ×13-34 random-plane rejection at 95 % signal efficiency, and a seeding road
- **Current treatment.** Mentioned, never used [1708.02243 Sec.III.C; G-T5-10]; listed as O7 in STRATEGY_DRAFT §5 without numbers.
- **Estimate** (Sec. 5.1).
  - The strip axis equals φ_pair exactly in vacuum. The B wobble is ≲ 2×10⁻⁴ rad and the hit-fit error 3×10⁻⁵ rad.
  - Δφ(MET, strip) is set by σ⊥(MET). For |Δφ| < 0.15-0.25 rad: 95 % efficiency and ×13 (σ⊥ = 35 GeV) to ×34 (15 GeV) rejection of random planes.
  - It also cuts the plane-seeding combinatorics by ≈ π/0.2 ≈ 16.
- **Exploitation:** (b) a factorisable background-rejection factor f_MET-plane, measurable in the low-MET CR; (c) a φ road for the plane finder.
- **Effort:** days. **Confidence:** high (geometry); the PU-200 MET resolution is UNVERIFIED.
- **Verdict: EXPLOIT.**

### G-T4-6 Local signatures and seeding: two regimes split at ΔN_osc ≈ 0.5 per layer gap; quirks are invisible to L1 tracking at Λ ≲ 3 keV
- **Current treatment.**
  - Plane seeding with hit pairs from inner/outer layers [1708.02243 Sec.III.C].
  - "Two hits per layer" is assumed.
  - Stub formation is untested [theory_signal_model §3.5].
- **Estimate** (Sec. 6).
  - The number of oscillations between consecutive layers, ΔN = σΔr/(2β*p_T), is 0.4 (IT, 1 keV), 3.5 (IT, 3 keV) and 40 (IT, 10 keV), independent of m_Q.
  - At Λ ≲ 1 keV: local curvature with apparent p_T ≈ 1-4 GeV; both quirks curve towards each other in 87-97 % of triplets.
  - At ≥ 3 keV: an aliased zig-zag band about a zero-curvature line through the PV, with non-monotonic separation in 98-100 % of events.
  - 2-3 hits per layer per pair (up to 3.2 at 500 GeV).
  - Only 23-47 % of OT crossings give a 2 GeV stub at 0.3-3 keV.
- **Exploitation:** (c) a two-regime seeding (curved IT arc pair vs straight PV band + MET road); (b) L1-scouting cluster-road trigger idea.
- **Effort:** weeks (seeding prototype on hit-level MC). **Confidence:** medium (sensor spacings UNVERIFIED; no PU).
- **Verdict: WORTH A CHECK.**

### G-T4-7 Mean energy loss is a first-order trajectory effect and a material-budget systematic
- **Current treatment.** The strategy includes mean dE/dx in the fit; no published study quantifies its effect on hit positions.
- **Estimate.**
  - Shifts of 15-180 µm (PS3/2S3, 200-500 GeV) and 0.3-1.5 mm (1 TeV) in the OT, through the oscillation-phase drift.
  - A 10 % material-budget error therefore moves OT hits by 4-150 µm, comparable to or larger than the resolution at 1 TeV.
  - As a mass handle it is limited to the material-budget precision (≈ 10 %).
- **Exploitation:** (e) a signal-efficiency systematic for any χ²/GNN that uses OT positions; (c) the material scale must be a fit nuisance.
- **Effort:** days. **Confidence:** medium (thin-scatterer Bethe, UNVERIFIED material).
- **Verdict: WORTH A CHECK.**

## 8. Killed ideas
- **dE/dx as a mass handle.** It measures only βγ, and so does the trajectory. Adding IT dE/dx (25 %/hit) changes σ(m_Q) by 0 % in every configuration (rows M2 → M3, Sec. 4.3).
- **MTD/BTL timing as a mass handle.** It measures β only. It improves ℓ₀ and the velocities ×3-25, but not m_Q (M1 → M2: ≤ 15 % change, only at 1 keV via decorrelation).
- **"Positions alone measure m_Q and Λ".** Exact vacuum degeneracy: the ln σ Fisher column is ≤ 3×10⁻⁷ of the largest.
- **Plane precession / thickness growth ∝ m_Q/Λ⁴ as the Λ meter.** The informative B term is ∝ qBR/Λ² (m_Q independent). The secular out-of-plane rotation is ≤ 18 µrad, below MS (T3 §4.2). The in-plane B handle dies at Λ ≳ 3 keV: σ(Λ)/Λ ≥ 17 % for 30 events.
- **Vacuum + first-order-B analytic fit model in the OT.** Misses 30-45 % of the B effect (25-50 µm at 1 keV) and ignores the 40 µm-1.5 mm energy-loss phase drift.
- **Kalman filter with a two-point state.** The causal string has memory. The phase-linearity window is ≤ 0.1 cycle, while 3-300 oscillations occur between layers at Λ ≥ 3 keV.
- **The midpoint of the two quirk hits as a "CM track".** It deviates from the centre line by 35-50 % of the half-separation (unequal hit times).
- **Hit-level φ of the strip as a limiting factor for the MET alignment.** 3×10⁻⁵ rad from the fit vs 0.04-0.07 rad from the MET.

## 9. Open questions for other workstreams
- **T2.**
  - Confirm the non-linear B response (G-T4-4) with `CausalNullString` at max_boost 10⁻³ and B ∈ [B/100, B].
  - Is there an analytic B log B term from near-reconnections at crossings?
- **T3.**
  - (i) Replace the thin scatterers by your continuous MS/straggling in the Fisher (the `T4_fisher.py` Jacobian approach works with any deterministic kick hook).
  - (ii) Energy-loss straggling effect on the oscillation phase at 1 TeV, where the mean-loss shift is ≈ 1.5 mm.
  - (iii) The material-budget uncertainty to use as the s_mat prior.
- **T5.** Literature check that no recoil-based (MET + velocity) mass estimate exists for quirks. HSCP analyses use p from curvature and β from timing; the quirk analogue here is p_T(recoil) + β from trajectory/BTL.
- **T6.**
  - Exclusive γγ → QQ̄ with PPS gives M_QQ̄ directly. With γ* from the trajectory (0.03-3 % per event), m_Q follows without the MET scale. How many events, and with what PPS mass resolution?
  - Also: the scalar Ẽ has a different γ* distribution, but the same degeneracy theorem applies.
- **Experimental Phase 2.**
  - (a) PU-200 PUPPI MET resolution and scale for a 200-500 GeV hadronic recoil (sets the m_Q resolution and its floor).
  - (b) OT module sensor spacings and stub windows per layer (Sec. 6).
  - (c) IT ToT dE/dx resolution and saturation.
  - (d) Implement the causal fit (G-T4-1) on plane-finder candidates; measure the χ²-based rejection with real hit assignment and PU.
  - (e) Use the MET-φ road (G-T4-5) in the plane finder and the factorised background estimate.
  - (f) Signal MC must include mean energy loss with the real material map (G-T4-7).

## 10. References opened
- **0805.4642** (Kang, Luty): Eq.3.7 (Nambu-Goto + point-mass action: the scale invariance of Sec. 2.1).
- **1708.02243** (Knapen et al.): Sec.III.C (plane finder, "n₃ aligned with MET"), Sec.IV (Δs = 100 µm cut; "obvious way to … measure the mass and string tension"), App.A (dE/dx statement). Used through T5's audit and the cached text.
- **1911.02223** (Li, Li, Pei, Zhang): Eq.III.12 (thickness ∝ qBm/Λ⁴), Sec.V ("future work"), Sec.V (calorimeter deposits ≲ 5 GeV, via theory_signal_model §4.3).
- **2002.07503**: Eq.II.4-8 (vacuum closed form, shown exact by T2), Eq.V.6.
- **2410.00269** (Sha et al.): GNN approach (via STRATEGY_DRAFT §9.2; not re-read).
- **2210.07766**: OT module pitches and lengths (via theory_signal_model §4.1).
- Internal: T2 report (§2, §5.1, §5.3; `T2_propagator.py`), T3 report (§2 material table, §3.2 MS floor, §4.2 precession, §6 timing; `T3_causal.py`, `T3_propagator.sample_events`), T5 report (G-T5-7, G-T5-9, G-T5-10, §4b), T6 (exclusive PPS, via LOG), `research/theory_signal_model.md` §4, `phase1_strategy/outputs/STRATEGY_DRAFT.md` §5, §9, §11.
- **Not opened** (values used as UNVERIFIED): CMS Phase-2 Tracker TDR (pixel pitch orientation, sensor spacings), MTD TDR (σ_t), Phase-2 L1 TDR (stub windows), PUPPI MET resolution at PU 200, JES uncertainty.

## 11. Code and figures
| File | Content |
|---|---|
| `code/T4_model.py` | fit-ready model: numba causal-string kernel (copy of the Athena/T2/T3 algorithm) + uniform B + thin scatterers with explicit MS deviates + mean dE/dx; physical ↔ natural parametrisation; self-checks (vacuum vs ExactPair ≤ 0.04-2 µm; B vs T3_causal ≤ 0.1 µm) |
| `code/T4_fisher.py` | per-event Jacobians (vacuum, B, B+eloss; natural parameters), MS Jacobians, validation runs; output `figures/T4_fisher_<m>_<Λ>.pkl` (~2 h on 5 cores) |
| `code/T4_fisher_report.py` | validation table, degeneracy analysis, CRB per event and ensemble, prediction windows; `figures/T4_fisher_report_out.txt`, `T4_fisher_summary.png/.npz` |
| `code/T4_comb.py` | 1-D χ² scans (linearity / aliasing); `figures/T4_comb.png`, `.npy` |
| `code/T4_met.py` | MET-strip alignment; `figures/T4_met_alignment.png` |
| `code/T4_local.py` | ΔN per layer gap, stub bends, triplet curvature, separation monotonicity; `figures/T4_local.png` |
