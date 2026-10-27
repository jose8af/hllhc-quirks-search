# T3: Quirk-pair propagation through the CMS Phase-2 magnetic field and material

Investigator: T3 (theory track, C001 quirks). Date: 2026-10-07. Status: COMPLETE (2026-10-08).

> **ERRATUM (2026-10-08, fix pass F1, after review R1-critical A-1 and B-2). This report is otherwise unchanged.**
> - The "lab straight string" of §3.1 (= T2 `LabStraightString`) is **not** the Li et al. algorithm, and no published paper uses it.
> - The literal Li integrator with thin-scatterer MS gives median Δs of 13/12/33 µm at 1/3/10 keV, against 30/15/22 µm for causal + MS. There is no secular growth and no mm-scale "fake thickness" (`code/R1_li_ms.py`, `figures/R1_li_ms_out.txt`).
> - So the "fake 0.2-21 mm" and "every published central-detector study is affected" statements marked **[superseded, see erratum]** describe labSS only. T2's "×0.04-60" is likewise a labSS/cmSS property; a converged Li integrator is ≈ 15 % low in thickness at 0.6-2 keV.
> - The causal propagator `T3_causal.py` is independently confirmed as exact classical NG (`code/R1_conformal_ng.py`, ≤ 1 %).
> - All Δs efficiencies in this report are at **truth level** (true hit positions). With Phase-2 hit resolution the coplanarity test is Inner-Tracker dominated: per-hit out-of-plane resolution ≈ 17 µm (IT), 0.25 mm (PS), 8 mm (2S). The pass fractions at low Λ change substantially (`code/F1_smear.py`).
> - Material per layer remains UNVERIFIED.
> - The hit recorder misses grazing double crossings within one chord (R1 C-1).
> - Current statement: `outputs/THEORY_GAPS_SYNTHESIS.md` S-1, S-2.


Conventions: Λ ≡ √σ (BRIEF §1; T1). σ = 50.68 GeV/cm (Λ/keV)² [T2 §2.2]. c = 29.979 cm/ns.
Code: `theory_track/code/T3_*.py` (builds on `T2_propagator.py`). Figures: `theory_track/figures/T3_*`.

## 1. Executive summary
1. **Every straight-string propagator fails once material is added, not only in B.** With MS kicks the lab-simultaneous straight string gives spurious plane thicknesses of 0.2-21 mm at Λ = 3-30 keV. The causal (Athena-type) Nambu-Goto string gives 2-25 µm on the same events. **[superseded, see erratum]**
   - I built a numba port of the causal algorithm with B, MS, dE/dx and straggling (`T3_causal.py`, validated against T2 and ExactPair, ~10³× faster). All results below use it. This confirms and extends T2 §5.
2. **MS sets a Λ-independent floor of Δs ≈ 11/15/22 µm** (median; 84th percentile ≤ 67 µm) at m_Q = 200/500/1000 GeV, with the Phase-2 material (≈ 19 % X0 at η = 0, UNVERIFIED per layer).
   - The causal B-field thickness is 32-38 µm at 1 keV, ∝ Λ^−1.9 and nearly m_Q-independent. It is ×7-50 above the m_Q/Λ⁴ formula at 3 keV.
   - **MS dominates for Λ ≳ 1.5-2 keV.** It does not break the Δs < 100 µm cut: pass fraction 0.93-1.00 at 1-30 keV.
   - It makes any Δs cut below ~30 µm cost 30-45 % of heavy signal.
3. **Revised window.** The 50 % edge of the coplanar finder is Λ_low ≈ 0.45-0.7 keV (200-1000 GeV), inside the strategy's band. At 1 TeV MS lowers the efficiency plateau, so ≥ 90 % needs Λ ≳ 2 keV. The upper (merging) edge is unchanged (Sec. 9).
4. **Timing with the real p_T > 200 GeV spectrum.**
   - Median BTL delay 3.5/9.6/18.7 ns for 200/500/1000 GeV. The strategy's 6/16/33 ns are the 84th percentiles.
   - OT hits outside ±12.5 ns: 7-33 % of 2S crossings at 500 GeV; 27 % (PS3) and 44-68 % (2S) at 1 TeV. The IT is unaffected.
   - Heavy slow pairs give ≈ 3 hits per IT/PS layer. The oscillation spreads hit times by > 1 ns only for Λ ≲ 0.5 keV.
5. **For T6: f_stop(EB+HB, |η| < 1) ≈ 1.0 ± 0.3 %** of produced pairs (6-9 % in any calorimeter, ≈ 10 % anywhere). The triggered 1 TeV sample gives 1.3-2.5 % (≈ 10-12 % anywhere). T6's yields sit at its f_stop = 1 % end unless the full calorimeter is used.
   - The merged pair deposits 9× (500 GeV) to 21× (1 TeV) MIP, not "2× MIP".
   - Killed: plane precession as a Λ meter (≤ 18 µrad, below the MS floor), B-field non-uniformity (B_r ≤ 0.9 % at |η| < 1), delta rays, straggling, net-charged/doublet signatures.

## 2. Material model of the CMS Phase-2 detector

**Tracker** (`T3_propagator.phase2_tracker()`). Thin cylindrical slabs. x/X0 is at normal incidence; the path factor 1/|cos α| comes from the integration. All values are ESTIMATE/UNVERIFIED unless a source is given. The Phase-2 Tracker TDR (CERN-LHCC-2017-009, CMS-TDR-014) could not be opened: the CDS download returned an HTML page, and the tkLayout material pages returned HTTP 404. Per-layer values are therefore a reconstruction.

| Element | R [cm] | \|z\| half-length [cm] | x/X0 per layer | Source / status |
|---|---|---|---|---|
| Be beam pipe, 0.8 mm | 2.2 | 300 | 0.23 % | Be X0 = 35.3 cm; geometry UNVERIFIED |
| IT TBPX L1-L4 | 3.0 / 6.1 / 10.4 / 14.6 | 20 | 1.2 % each | the module alone is 0.825 % (estimate), with measured values 0.72 ± 0.05 % and 0.95 ± 0.09 % [2407.13721 Tab.1, abstract]; +0.4 % for support, cooling and cables is UNVERIFIED. Radii: the T2 / CMSSW tracklet set |
| IT service cylinder | 19 | 120 | 1.0 % | UNVERIFIED |
| OT PS L1-L3 | 24.9 / 37.2 / 52.3 | 120 | 2.5 % each | UNVERIFIED (double-sensor module, MPA/SSA, CO2 cooling) |
| OT 2S L1-L3 | 68.8 / 86.0 / 108.3 | 120 | 1.8 % each | UNVERIFIED. A web summary of a tkLayout component table gives about 2 % for 2S hybrids, supports and spacers (secondary source) |
| **Sum at η = 0** | | | **≈ 19 % X0** | consistent with the qualitative "about half of Phase-1" statement [1912.02061 Sec.2, Fig.3]. Phase-1 is ≈ 0.4 X0 at η = 0 (UNVERIFIED) |

- Slab radial widths: 1 cm (IT), 2 cm (OT). Energy loss is computed in silicon-equivalent material, with density scaled so that x/X0 is reproduced.
- MS scales as √(x/X0). A pessimistic variant multiplies all values by ×2 (`phase2_tracker(scale=2)`).
- **Outside the tracker:** the Evans-Luty cylindrical CMS [1811.08903 Tab.1]: ECAL PbWO4 (ζ = 0.33), HCAL brass/Cu (0.68), coil as iron (0.5), barrel and endcap return-yoke iron (ζ = 1), air elsewhere.
- **Stopping power:** Bethe without density effect. L = ln(2m_eβ²γ²/I) is floored at 0.6, and below β = 0.02 the stopping power is linear in β. This is the same stopping power as T6 (`T6_stopping.py`), so f_stop and T6's yields use one model.
- **Straggling:** Gaussian with the Bohr variance 0.1569 MeV² ρ(Z/A) x [cm].
- **Multiple scattering:** Highland θ0 = 13.6 MeV/(βp) |q| √(x/X0) [1 + 0.038 ln(x q²/β²)] [PDG RPP 2024 Eq.34.16 (recalled, UNVERIFIED)]. It is applied as a Gaussian 3D deflection after every integration step, with variance proportional to the path in the step. The log term uses the full layer x/X0.
- **Delta rays: killed** (no separate treatment). The largest transverse recoil from a δ electron is ≈ √(m_e T_max) ≈ m_e βγ√2 ≈ 0.2 MeV at βγ = 0.3. This is ≪ the MS kick per layer, ≈ 13.6 MeV √(x/X0)/β ≈ 5-15 MeV, and electron scattering is already included in Highland (the Z(Z+1) term).
- **B field:** uniform 3.8112 T [CMSSW tracklet `bfield_`, via theory_signal_model §4.1]. A simplified CMS map (−1.8 T in the barrel yoke iron, UNVERIFIED) is used for stopping. A finite-solenoid map is used for the fringe estimate (Sec. 4.3).

## 3. Multiple scattering, straggling and delta rays vs the B-field plane thickness (Q1)

### 3.1 Propagator: the lab straight string cannot be used with kicks; the causal string is used
- I first built a fast numba lab-frame integrator (`T3_propagator.py`). It uses Kang-Luty forces with ŝ along the lab-simultaneous separation (= T2 `LabStraightString`) and adaptive Dormand-Prince 5(4). Crossings are landed on step boundaries, and the error norm is taken on the separation, not on the absolute position.
- Validation (`T3_test_propagator.py`, 14/14 pass): vacuum positions agree with T2 `ExactPair` to ≤ 10⁻⁶ cm (Λ ≤ 3 keV) and to 1.4 µm phase error after 2500 crossings at 10 keV. In 3.8 T it agrees with T2's solve_ivp version to < 0.01 µm at 0.6-1 keV and is 10²-10³× faster.
  - At 2 keV T3 and T2 differ by 2 µm after 170 crossings. T3 is converged in rtol to < 10⁻³ µm and is insensitive to a 10⁻⁹ change in initial conditions. The difference comes from T2's fixed, non-error-controlled "nudge" step after each crossing event.
- **However, the lab-straight-string model itself is wrong once any external force acts.** T2 shows this for B (T2 report §5.1: momentum non-conservation, thickness wrong by ×0.04-60). I confirm it independently for **material kicks with B = 0**: with MS on, the lab straight string gives a "plane thickness" that grows with the number of crossings.
  - Values: median 12-23 µm at 0.3 keV, 30-70 µm at 1 keV, 220-380 µm at 3 keV, 440-580 µm at 10 keV, 2.5-21 mm at 30 keV (16 events per point; ESTIMATE, first version of `T3_ms_thickness.py`).
  - The causal string on the same events gives 3-25 µm (Sec. 3.2).
  - The spurious work done at every near-miss crossing turns each MS kick into a secular drift. **Any straight-string study that adds material kicks would therefore grossly overestimate MS.** **[superseded, see erratum]**
- **Production propagator: `T3_causal.py`.** It is a numba port of the Athena/T2 causal null-vector string (exact Nambu-Goto for piecewise-null data). It adds a step-length cap (0.2 cm in the tracker) for hit interpolation, the material kicks of Sec. 2 applied to the endpoint after each of its steps, hit recording and stop/exit conditions.
  - Validation (`pixi run python code/T3_causal.py`): vacuum hits agree with `ExactPair` to ≤ 2.5 µm. This is an in-plane chord-interpolation error and does not affect the thickness.
  - In 3.8 T it reproduces T2's Python `CausalNullString` thickness exactly (105/169 µm at 0.6 keV; 13.8/17.2 µm at 2 keV), 400× faster.
  - It is converged: max_boost 10⁻² → 10⁻³ and h_max 0.2 → 0.05 cm change the thickness by 1-1.5 %.

### 3.2 Results: thickness with and without MS (causal string, CMS Phase-2 material)
Setup (`T3_ms_thickness.py`):
- Events: LO DY+ISR pairs from T2's cache, p_T(QQ̄) > 200 GeV, |η_pair| < 1.
- Each event is propagated with the same initial momenta in four configurations:
  - **B**: 3.8 T, no material (the literature case);
  - **B+E**: B plus dE/dx and straggling, no MS;
  - **B+M**: full material (MS, dE/dx, straggling);
  - **M**: material with B = 0 (MS-only thickness).
- Hits: every crossing of the 10 barrel layers. Δs = √(smallest eigenvalue) of the plane fit through the origin [1708.02243 Eq.11].

Statistics: 60 events per point for Λ ≤ 3 keV, 24 at 10 keV, 12 at 30 keV (`figures/T3_ms_thickness.npy`; figure `figures/T3_ms_thickness.png`). A 16-event trial run (`T3_ms_thickness_trial16.npy`) agrees within its statistics.

| m_Q [GeV] | Λ [keV] | B (no material) | B+E | **B+M (realistic)** | M (B = 0) | Li formula [1911.02223 Eq.III.12], 3.81 T | f(Δs < 100 µm): B → B+M |
|---|---|---|---|---|---|---|---|
| 200 | 0.3 | 362 (150-560) | 362 | 361 (160-550) | 11 (4-27) | 1090 | 0.10 → 0.10 |
| 200 | 1 | 38 (19-54) | 38 | 31 (15-57) | 11 (4-29) | 8.8 | 1.00 → 0.98 |
| 200 | 3 | 5.2 (2.5-7.5) | 5.5 | 11 (5.5-24) | 10 (5-29) | 0.11 | 1.00 → 1.00 |
| 200 | 10 | 0.73 (0.3-0.9) | 0.63 | 12 (5.6-25) | 15 (4-22) | 9×10⁻⁴ | 1.00 → 1.00 |
| 200 | 30 | 0.29 | 0.36 | 1.7 (1.1-4.9) | 2.2 | 10⁻⁵ | 1.00 → 1.00 |
| 500 | 0.3 | 278 (170-460) | 275 | 287 (160-460) | 12 (3-37) | 2730 | 0.08 → 0.07 |
| 500 | 1 | 34 (19-52) | 34 | 42 (22-69) | 16 (5-56) | 22 | 1.00 → 0.98 |
| 500 | 3 | 4.9 (2.6-6.9) | 4.9 | 15 (6-48) | 17 (7.5-42) | 0.27 | 1.00 → 0.98 |
| 500 | 10 | 0.58 (0.3-0.85) | 0.55 | 14 (5-27) | 13 (4-48) | 2×10⁻³ | 1.00 → 1.00 |
| 500 | 30 | 0.20 | 0.42 | 2.7 (2.0-6.4) | 4.2 | 3×10⁻⁵ | 1.00 → 1.00 |
| 1000 | 0.3 | 262 (79-520) | 265 | 273 (78-510) | 20 (3-66) | 5460 | 0.22 → 0.20 |
| 1000 | 1 | 32 (10-52) | 30 | 51 (22-77) | 21 (8-55) | 44 | 1.00 → 0.93 |
| 1000 | 3 | 3.9 (1.2-6.5) | 3.9 | 25 (8-63) | 24 (9-67) | 0.55 | 1.00 → 0.97 |
| 1000 | 10 | 0.36 (0.13-1.1) | 0.56 | 20 (7-50) | 21 (9-51) | 4×10⁻³ | 1.00 → 1.00 |
| 1000 | 30 | 0.22 | 0.82 | 7.1 (2.8-9.4) | 5.8 | 5×10⁻⁵ | 1.00 → 1.00 |

All values are median Δs in µm, with 16-84 % ranges in brackets.

Further numbers from the same run:
- Max |residual| from the plane, median, B → B+M: 84 → 103 µm (500 GeV, 1 keV), 11 → 34 µm (500 GeV, 3 keV), 9 → 64 µm (1 TeV, 3 keV), 0.9 → 48 µm (1 TeV, 10 keV).
- IT+PS-only thickness (true 3D points), B → B+M: 18 → 21 µm (1 keV), 2-3 → 5-10 µm (3 keV), 0.2-0.3 → 4-8 µm (10 keV).

Reading (ESTIMATE):
1. **MS sets a floor of Δs ≈ 10-25 µm (median; 84th percentile 25-65 µm) for 1 ≲ Λ ≲ 10 keV.** It is nearly independent of Λ and grows with m_Q: about 11, 15 and 22 µm at 200, 500 and 1000 GeV. The B-field thickness falls as ≈ Λ^−1.9: causal string 32-38 µm at 1 keV and 3.9-5.2 µm at 3 keV. Hence:
   - **MS dominates for Λ ≳ 1.5-2 keV at every mass.**
   - B dominates below ~1 keV.
   - At 1 keV the two are comparable and add roughly in quadrature: 31-51 µm with both.
2. **MS does not push the median above the 100 µm Knapen cut anywhere in 1-30 keV.** The 84th percentile of B+M is ≤ 77 µm.
   - The fraction passing Δs < 100 µm drops only from 1.00 to 0.93-0.98 at 1-3 keV (1 TeV: 0.93 at 1 keV, 0.97 at 3 keV).
   - The **maximum** residual (relevant for hit-association windows) grows from ~10 µm to 35-65 µm at 3 keV. A per-hit window ≲ 50 µm would lose hits.
   - **The lower edge of the coplanar window is set by the B field, not by MS.** MS moves the 50 %-efficiency lower edge only at 1 TeV (+0.15 keV), but it lowers the efficiency plateau there (Sec. 9).
   - The 100-µm cut has ×4-10 headroom against MS in the core window. Tightening it to ~30 µm (for PU rejection) would cost signal efficiency at Λ ≈ 1-10 keV because of MS. This is a new constraint on how tight Δs can be made.
3. **The B-field thickness is not the analytic formula.**
   - The exact causal NG gives 32-38 µm at 1 keV (formula 9-44 µm) and 3.9-5.2 µm at 3 keV (formula 0.1-0.55 µm, ×7-50 above).
   - At 10 keV it gives 0.4-0.7 µm (formula ≤ 0.004 µm).
   - At 0.3 keV the formula is high by ×3-20 (1090-5460 µm vs 260-360 µm), because the plane-through-origin fit over ≤ 2 crossings is not the formula's quantity.
   - **The thickness falls roughly as Λ^−1.9 and depends only weakly on m_Q** (32-38 µm at 1 keV for all three masses), not as m_Q/Λ⁴. This agrees with T2's 4-event study (T2 §5.1).
   - The lower window edge therefore barely depends on m_Q (Sec. 9).
4. **Energy-loss straggling (B+E vs B) changes nothing out of plane**, as expected: the force is along v, which lies in the plane to first order. Killed.
5. **IT+PS-only (true 3D points at CMS).** The 2S modules measure only rφ well: 5 cm strips [theory_signal_model §4.2]. The B+M thickness from IT+PS hits alone is 1.7-10 µm (Λ = 3-30 keV) and 16-21 µm (1 keV). MS acts mainly through the lever arm to the outer layers.
6. **How the string restores planarity** (analytic picture, checked against the M column):
   - A kick δp on one quirk changes the total momentum by δp, so the pair direction turns by δp/|P_QQ̄|. That is about half of what a free quirk with p ≈ |P|/2 would suffer.
   - The internal part, δp/2 of relative momentum, adds a bounded out-of-plane oscillation of amplitude ≈ ℓ δp/(2p*). This is negligible for ℓ ≪ R, i.e. Λ ≳ 1 keV.
   - Because δp⊥ = 13.6 MeV √x/β depends only on the quirk velocity, the MS thickness is set by the β distribution at the layers and by |P|, not by Λ. This explains the flat M column.
   - At 30 keV the two quirks' hits coincide to < 100 µm. The plane is then defined only by the CM line plus the ~50 µm oscillation, so Δs drops to 1.7-7 µm. The plane is not physically meaningful in that merged regime.
7. **Single-kick test** (`T3_kick.py`, causal string, B = 0, no material; a kick of 10 MeV along the plane normal on one quirk at r = 3 cm; m = 500 GeV, 3 events × Λ = 0.3/1/3/10 keV; table on stdout).
   - **The analytic CM picture is only a lower bound.**
   - For a tiny kick (1 keV) the response is exactly CM-like: 27 µm at 2S3 for both quirks, vs 28 µm predicted by (δp/|P|) × path.
   - For a realistic 10 MeV kick the two quirks separate out of the plane. Offsets at r = 108 cm are, e.g., (−8, +101) µm at Λ = 10 keV and (+165, −13) µm at 1 keV, vs a CM prediction of 28-44 µm.
   - The result is converged (max_boost 10⁻² → 10⁻³ changes it by < 0.2 %) and antisymmetric in the kick sign, but **non-linear** in δp.
   - Interpretation: the kick gives the internal motion an angular momentum L ≈ ℓ δp/2 lying in the old plane. The internal orbit then lives in a plane containing the old normal. The near-miss crossings that follow (impact parameter b ≈ ℓ δp/(2p*), sub-µm) precess the oscillation axis, so it walks out of the original plane by an amount that accumulates over the N_cross ∝ Λ² crossings, while b ∝ Λ⁻². The product is roughly Λ-independent.
   - **So the string does not simply "share" an MS kick. It also converts part of the kick into a slow out-of-plane rotation of the oscillation axis.**
   - This is the same crossing physics that makes the B-field thickness fall only as ≈ Λ^−2 (T2 §5.1, 5.3).
   - The full-material numbers of Sec. 3.2 include it, and they stay ≤ 77 µm at the 84th percentile.


## 4. B field: plane precession as a Λ meter; field non-uniformity (Q2)

### 4.1 What to expect (analytic, ESTIMATE)
- **Uniform B, neutral pair.**
  - Canonical momentum conservation, P_mech = P₀ − q d × B (d = x₁ − x₂, up to sign convention), forces the CM direction to wobble with amplitude q|d|B/|P|. That is 2×10⁻⁵ rad for ℓ = 0.5 cm and |P| = 300 GeV.
  - d reverses sign at every crossing. So this wobble is **bounded, not secular**, and there is no first-order secular rotation of the pair direction.
  - Knapen's torque estimate [1708.02243 Eq.8-9] gives Δφ ~ 10⁻⁵ (v_cm²/v²)(B/2 T)(2 keV/Λ)² **per oscillation**. They state that Δφ "oscillates and slowly accumulates … until it stabilizes" [1708.02243 Sec.II, Fig.3].
  - A secular rotation can only come at second order: the field-induced polarisation of the yo-yo times the CM-frame field, i.e. an induced-dipole torque that aligns the axis with E* = γv_cm × B. My order-of-magnitude estimate of the resulting rotation over the tracker is ~10⁻⁵ rad, **independent of Λ**: torque ∝ ℓ/σ and inertia ∝ ℓ² both scale as Λ⁻⁴.
  - That is ≈ 0.1-10 µm × (ℓ/cm) in hit displacement. It is below the MS floor (Sec. 3.2) everywhere except at ℓ ≳ 10 cm (Λ ≲ 0.5 keV).
- **Measurability.** A plane angle from hits over a 1 m lever arm with ~10-30 µm effective point precision is good to ~2-3×10⁻⁵ rad per event. That is already the MS-induced tilt per kick (δp/|P| ≈ 5-10 MeV/300 GeV).
  - A precession signal must therefore exceed ~3×10⁻⁵ rad to be measurable, which needs Λ ≲ 1 keV (numerics in 4.2).

### 4.2 Numerical test (causal string; `T3_precession.py`, 24 events per point, p_T > 200 GeV, |η| < 1; `figures/T3_precession.npy`)
Observable: the systematic **trend** of the signed out-of-plane residual with radius, i.e. the slope of residual vs r for the plane fitted to all barrel hits. It measures a rotation of the plane along the flight. Medians:

| m_Q | Λ [keV] | \|slope\|, B only [µrad] | \|slope\|, B + material [µrad] | Knapen Eq.9 at 3.8 T, × (v_cm/v)² [µrad] |
|---|---|---|---|---|
| 500 | 0.6 / 1 / 2 / 3 / 5 | 3.4 / 3.1 / 0.33 / 0.22 / 0.08 | 10 / 7.5 / 4.8 / 6.1 / 4.5 | 212 / 76 / 19 / 8.5 / 3.0 |
| 1000 | 0.6 / 1 / 2 / 3 / 5 | 18 / 5.7 / 0.9 / 0.5 / 0.3 | 30 / 10 / 9.5 / 5.8 / 8.2 | same |

- A second observable, the angle between planes fitted separately to the inner (r ≤ 25 cm) and outer hits, comes out at 2-80 mrad. This is **not physics**: the inner hit set is nearly collinear for ℓ ≪ 25 cm, so its fitted normal is ill-conditioned. Plane-by-segment fits are not a usable precession meter.
- **Verdict on "precession as a Λ meter": killed.**
  - The B-induced secular rotation over the tracker is 3-18 µrad at Λ = 0.6-1 keV and falls roughly as Λ^−2.5 to ≤ 0.3 µrad at 3-5 keV.
  - The same observable with material is 4.5-10 µrad, Λ-independent: it is the MS floor.
  - Knapen's per-oscillation estimate (×(v_cm/v)² ≈ 0.05-0.2) is the right order at 1-3 keV. It does not accumulate secularly, as the analytic argument of 4.1 predicts.
  - A rotation signal can be separated from MS only for Λ ≲ 1 keV. There the **thickness itself** (32-38 µm at 1 keV, 260-360 µm at 0.3 keV, ∝ Λ^−1.9) is a larger and more direct Λ handle.
- **Λ handles that survive** (to T4):
  - (i) the B-field thickness, for Λ ≲ 1.5 keV, where it exceeds the MS floor;
  - (ii) the oscillation period / crossing spacing D = 2p*(βγ)_pair/σ [T2 §2.2] from hit patterns;
  - (iii) the lab crossing time Δt_c from repeated BTL hits (Sec. 6, item 4);
  - (iv) for the merged regime, nothing in the tracker. The stopped-pair channel and the dE/dx-vs-β relation carry m_Q, not Λ.

### 4.3 Field non-uniformity inside the tracker (`T3_field.py`)
Model: ideal finite current sheet, a = 3.15 m, length 12.5 m (CMS coil, UNVERIFIED), no yoke, normalised to 3.8112 T. The missing yoke makes it an *over*estimate of B_r at the tracker ends.

| \|z\| [cm] | B_r/B₀ at r = 14.6 cm | r = 52.3 cm | r = 108.3 cm | B_z(108 cm, z)/B₀ |
|---|---|---|---|---|
| 50 | 0.05 % | 0.16 % | 0.33 % | 1.002 |
| 120 | 0.12 % | 0.41 % | 0.83 % | 0.995 |
| 200 | 0.21 % | 0.76 % | 1.53 % | 0.979 |
| 270 | 0.33 % | 1.18 % | 2.37 % | 0.955 |

On the outer OT radius: B_r/B₀ = 0.9 % at η = 1, 1.9 % at η = 1.5, 4.7 % at η = 2. The last point is already in the TEDD region, outside the barrel.
- The plane thickness is linear in the in-plane field component [2002.07503 Sec.V.A], so B_r changes the thickness by ≲ 1 % for |η| < 1 and ≲ 2-5 % for 1.5 < |η| < 2.
- The B_z drop (−4.5 % at the tracker end) changes it by about the same amount.
- **Killed as a physics effect.** The real CMS map should simply be used in simulation, as T5 already concluded. A **net-charged** pair (Sec. 5) feels B_r through the helix as any track does: standard field-map tracking.

## 5. Net-charged pairs and mid-flight charge change (Q3)

Short section: no new viable signature emerges.

1. **Doublet L (W-produced L±L⁰, net charge ±1) and triplets.**
   - The charged member decays, Q± → Q⁰π±, with cτ = 7.9 mm (doublet) or 6.0 cm (Y = 0 triplet) [T6 G-T6-2].
   - With βγ ≈ 0.13-0.6 per quirk, the doublet pair is neutral before the first pixel layer (survival to R = 3 cm ≤ 0.2 % [T6]).
   - For a Y = 0 triplet the survival is 40 / 14 / 2 % at 3 cm and ≈ 1.5 % / 10⁻⁴ / 0 at 15 cm, the last IT layer (ESTIMATE: decay length βγcτ = 3.6 / 1.5 / 0.8 cm for 200 / 500 / 1000 GeV).
   - **What the tracker sees.**
     - The neutral member leaves no hits.
     - Before the decay: hits from the charged member only, i.e. one wiggly track. Its guiding centre is the pair CM, and it oscillates about the CM with amplitude ≈ ℓ/2 (both members are tied by the string).
     - After Q± → Q⁰π±: a soft pion (p ≈ 0.2-0.3 GeV [T6]), and the quirk hits stop. A pion of 0.3 GeV curls with R = p/(0.3B) = 26 cm, so it is a looper inside the IT.
     - For most of the triplet sample this is a 1-3-hit stub followed by nothing. The existing disappearing-track searches need ≥ 4 pixel hits, so the triplet is not a tracker-quirk signature: survival to 15 cm is ≤ 1.5 % even at 200 GeV.
   - The surviving fraction is reachable only with the IT seeding of a short-track analysis. **Killed as a CMS tracker benchmark**, consistent with T6.
2. **Stable net-charged pair** (e.g. a W-produced pair with a stable charged partner, or q₁ + q₂ ≠ 0 multi-charge models).
   - The pair CM moves on a helix of radius R_c = p_T/(0.3 |q₁+q₂| B) = 219 m (p_T = 250 GeV, |q₁+q₂| = 1, 3.8 T), with the yo-yo superimposed.
   - The CM sagitta over 1.08 m is L²/(8R_c) = 0.67 mm. That is ≫ the 100 µm coplanarity cut whenever the oscillation plane is not the transverse plane.
   - So **a coplanar finder through the PV rejects net-charged pairs**, as Li et al. found (thickness ×20 for ±1/3, ±2/3 pairs [2002.07503 Sec.V.A]).
   - The right object is a **helicoidal sheet**: the helix of the CM with p_T measured from the sagitta, plus the oscillation direction. It is easily parameterised: p_T/q from curvature, as for any track.
   - The signature itself (two oscillating tracks about a common helix) is distinctive. It costs one extra parameter in the plane fit. **WORTH A CHECK** only if a model with stable net-charged pairs is adopted. None of the current benchmarks has one.
3. **One end changes charge mid-flight (Q± → Q⁰ π±) while the pair is still in the tracker** (triplet at 200 GeV only).
   - The pair becomes neutral, so the CM helix becomes a straight line with a kink in the guiding centre; the kink angle is ≈ p_π/|P| ≈ 10⁻³.
   - The B-field "thickness" switches from the net-charge (secular) to the neutral (bounded) form.
   - Hits stop if the remaining member is neutral.
   - No independent signature beyond a short track with a kink and a soft pion. Killed (rate ≤ 1.5 % of the triplet sample at 15 cm).

## 6. Hit timing and slow pairs (Q4)

Method (`T3_timing.py`, ESTIMATE; figure `figures/T3_timing.png`):
- Events: LO DY+ISR with the full p_T(QQ̄) > 200 GeV spectrum from T2's cache, |η_pair| < 1.5.
- Delay: toa = t − |r|/c, which is the quantity the CMSSW Phase-2 digitiser cuts on [STRATEGY_DRAFT C8].
- (a) Pair-CM delay. This is exact for the time of the pair centre: in vacuum the CM moves on a straight line, and the energy lost in the tracker is < 0.3 GeV of ≥ 100 GeV of kinetic energy (`T3_test_propagator.py`).
- (b) Exact per-quirk world lines (T2 `ExactPair`), Λ = 0.3/1/3 keV, 300 events per point.
- Windows: OT ±12.5 ns; IT [−5, 20) ns.
- Acceptance: barrel |z| < 20 cm (IT) and < 120 cm (OT), both UNVERIFIED.

**(a) Pair-CM delay toa [ns], median (16-84 %), and fraction of pairs whose CM is outside the window at that layer**

| m_Q | β_T (16/50/84 %) | IT4 (14.6 cm) | PS1 / PS2 / PS3 | 2S1 / 2S2 / 2S3 | BTL (114.8 cm) | lost: PS3, 2S1, 2S2, 2S3 |
|---|---|---|---|---|---|---|
| 200 | 0.32 / 0.42 / 0.55 | 0.5 (0.2-0.8) | 0.8 / 1.1 / 1.6 | 2.2 / 2.8 / 3.6 (1.7-6.2) | 3.5 (1.6-6.2) | 0, 0, 0.01, 0.02 |
| 500 | 0.17 / 0.25 / 0.39 | 1.3 (0.6-2.2) | 2.1 / 3.1 / 4.3 | 5.8 / 7.4 / 9.5 (4.2-16) | 9.6 (4.2-16.5) | 0.02, 0.07, 0.17, 0.33 |
| 1000 | 0.10 / 0.16 / 0.27 | 2.4 (1.1-4.2) | 4.1 / 6.1 / 8.5 | 11.3 / 14.1 / 17.9 (8-32) | 18.7 (8.5-33) | 0.27, 0.44, 0.57, 0.68 (PS2 0.07) |

No IT hit is lost: the IT delay is < 5 ns even at 1 TeV.

**(b) Effect of the oscillation itself** (per-quirk time minus CM time; all crossings):

| m_Q | Λ [keV] | median \|Δt\| | 95 % \|Δt\| | hits lost per hit: PS / 2S | hits per event per layer (IT1 … 2S3) |
|---|---|---|---|---|---|
| 500 | 0.3 | 0.60 ns | 7.7 ns | 0.03 / 0.16 | 2.0 … 1.6 |
| 500 | 1 | 0.08 ns | 0.9 ns | 0.01 / 0.21 | 2.5 … 1.5 |
| 500 | 3 | 0.008 ns | 0.10 ns | 0.01 / 0.22 | 2.5 … 1.5 |
| 1000 | 0.3 | 1.8 ns | 17.6 ns | 0.18 / 0.57 | 2.0 … 2.0 |
| 1000 | 1 | 0.25 ns | 2.6 ns | 0.19 / 0.69 | 2.9 … 1.8 |
| 1000 | 3 | 0.03 ns | 0.33 ns | 0.20 / 0.70 | 3.1 … 1.8 |

Reading (ESTIMATE):
1. **Cross-check of the strategy numbers.**
   - The strategy's BTL delays of 16 ns (500 GeV) and 33 ns (1 TeV) are for a fixed p_T(QQ̄) = 250 GeV and the median γ* [STRATEGY_DRAFT §4.2 C2]. With the real falling p_T > 200 GeV spectrum the medians are **9.6 ns and 18.7 ns**, because the spectrum has a tail to higher p_T. The 84th percentiles are 16.5 and 33 ns.
   - So the strategy's numbers are about the **slow third** of the triggered sample, not its median.
   - The qualitative conclusion stands: 2S hits are lost at m_Q ≥ 500 GeV. At 1 TeV, 44-68 % of 2S layer crossings and 27 % at PS3 fall outside ±12.5 ns.
   - At 500 GeV the loss is 7/17/33 % for 2S1/2S2/2S3: smaller than the strategy's "2S L3 lost" for the median pair.
2. **The internal motion (β* ≈ 0.5-0.9) matters for timing only at Λ ≲ 0.5 keV.**
   - Per-hit times scatter about the CM value by a median of 0.6-1.8 ns and up to 8-18 ns (95 %) at 0.3 keV, because ℓ is tens of cm.
   - For Λ ≥ 1 keV the scatter is < 0.3 ns median. At Λ ≥ 3 keV it is ≤ 30 ps, i.e. at the MTD resolution (30-60 ps), so the BTL time measures the pair-CM β directly.
3. **Slow heavy pairs cross a layer more than once.** At 1 TeV and Λ ≥ 1 keV there are ≈ 3 hits per event per IT/PS layer instead of 2. The radial component of the internal motion exceeds the radial CM velocity β_T ≈ 0.1-0.16, so a quirk crosses the same radius 1-2 extra times. This is consistent with 10-20 % of events having > 2 hits per layer in 2002.07503 Tab.I, but much more frequent at 1 TeV.
   - These extra hits are later and preferentially from slow pairs. The **per-hit** loss fraction is therefore higher than the per-pair one: 70 % of 2S hits and 20 % of PS hits at 1 TeV.
   - Plane finders that assume "two hits per layer" [1708.02243 Sec.III.C] must accept 3-4.
4. **Time ordering as a handle.** Within a layer, the multiple hits of one quirk are separated by the oscillation period in the lab, Δt_c = 2p*γ_pair/σ ≈ 0.13 ns γ*β* γ_pair (m/100 GeV)(keV/Λ)² [T2 §2.2]. This is ≈ 0.3 ns at 1 keV and m = 500 GeV.
   - The BTL (30-60 ps) could resolve the oscillation period for Λ ≲ 3 keV, if two crossings of the BTL by one quirk are both recorded. That would be a direct Λ measurement: Δt_c fixes p*/σ, and with the measured β it fixes Λ²/m_Q.
   - BTL bars are 3 mm thick, so a second crossing needs ℓ_radial ≳ mm, i.e. Λ ≲ 5 keV. WORTH A CHECK (MTD DPG: double-hit capability of TOFHIR).

## 7. Stopping fraction f_stop (Q5, for T6)

Method (`T3_stopping.py`, ESTIMATE):
- Propagator: causal NG string (`T3_causal`), simplified CMS field (3.8 T inside the coil, −1.8 T in the barrel yoke iron, UNVERIFIED).
- Material: Phase-2 tracker slabs plus the Evans-Luty cylindrical CMS [1811.08903 Tab.1]: ECAL PbWO4 ζ = 0.33, HCAL Cu ζ = 0.68, coil Fe ζ = 0.5, yoke Fe ζ = 1. Mean Bethe dE/dx (the same S(β) as T6), straggling, MS.
- Stop criterion: pair-CM velocity < 0.01, computed from the **total** 4-momentum (quirks + string vectors). The quirks alone are not enough: at a fixed lab time they are at different CM times, and using them alone gave spurious "stops".
- The internal energy left at that point is dissipated in place in ~0.1-0.3 µs [T6, `T6_stopping.py`].
- Exit: r > 7.5 m or |z| > 11 m.
- Fiducial region: ECAL+HCAL barrel with |η_stop| < 1, as in Evans-Luty.
- Samples:
  - **isr**: LO DY+ISR, p_T(QQ̄) > 200 GeV; this is the tracker-triggered sample.
  - **incl**: inclusive LO DY, given a Sudakov-like pair p_T ~ p_T e^{−p_T/15 GeV} (⟨p_T⟩ = 30 GeV, UNVERIFIED).
- Statistics: 80 events per (m_Q, Λ, sample) at Λ = 0.3/1/3 keV.
  - At 3 keV 18-40 % of events hit the step cap (6×10⁷). Almost all of them are fast pairs already beyond the calorimeters, or forward pairs. Only 2-3 are inside the barrel calorimeter envelope at |η| < 1, so the 3 keV fiducial numbers are biased low by ≲ 2 %.
  - Λ = 0.3 and 1 keV are combined below (160 events each), since their fractions agree within statistics, as Evans-Luty found above 300 eV [1811.08903 Sec.2].
  - A 400-event run at 1 keV is reported in 7.1.

| sample | m_Q | **f_stop, ECAL+HCAL \|η\| < 1** | all calorimeter (any η) | coil | yoke | tracker/beam pipe | any stop |
|---|---|---|---|---|---|---|---|
| isr (p_T > 200) | 200 | 0/160 (< 1.4 %, 90 % CL) | 0 | 0 | 0 | 0 | 0 |
| isr | 500 | 0/160 (< 1.4 %) | 0 | 0 | 1.9 % | 0 | 1.9 % |
| isr | 1000 | **2.5 ± 1.3 %** | 3.7 % | 2.5 % | 6.3 % | 0 | 12.5 % |
| incl (⟨p_T⟩ = 30) | 200 | 0.6 ± 0.6 % | 3.1 % | 0.6 % | 6.9 % | 0 | 10.6 % |
| incl | 500 | **1.3 ± 0.9 %** | 4.4 % | 0 | 0.6 % | 0 | 5.0 % |
| incl | 1000 | 0/160 (< 1.4 %) | 3.7 % | 0.6 % | 3.1 % | 2.5 % | 10.0 % |

Median time to stop for fiducial stops: 110 ns (isr, 1 TeV) and 190-370 ns (incl).

Reading (ESTIMATE):
1. **Agreement with Evans-Luty.** For inclusive pairs, f_stop(fiducial) ≈ 0.5-1.5 % and all-calorimeter ≈ 3-4.5 %. This is consistent with Evans-Luty's 1-5 % (|η| < 1) and "×3 for the full calorimeter" at 400 GeV [1811.08903 Fig.2, Fig.6], at the lower end.
   - My yoke fraction (0.6-7 %) is lower than their "about the same again".
   - The simplified field and the ⟨p_T⟩ model are the main uncertainties: f_stop(fiducial) needs |p_z| ≲ 1.2 p_T *and* a slow pair, so it scales roughly linearly with the low-p_T tail.
2. **T6's yields.** T6 assumed f_stop = 1-6 % [T6 G-T6-4] against the total DY cross-section. My inclusive numbers support the **lower end: ≈ 1 % fiducial** (7.1), with 6-9 % in the full calorimeter and ≈ 10 % anywhere.
   - **The 3-event reach of the delayed-annihilation channel is therefore T6's f_stop = 1 % value (≈ 0.65 TeV) for an EB+HB-only search.** Using the full calorimeter (|η| < 3) gives ×6-9 more stops. T6's f_stop = 6 % column then applies, ≈ 0.9 TeV.
3. **Triggered (ISR) sample.** Light pairs (200-500 GeV) essentially never stop: βγ_pair ≈ 0.3-0.7, with a range ≫ 1 m of iron-equivalent. At 1 TeV, **1.3-2.5 % stop in the barrel calorimeter and 10-12 % stop somewhere in CMS**, mostly coil and yoke.
   - So a fraction of exactly the events that fire the MET+ISR trigger produce a **delayed annihilation 0.1-1 µs later** in the same detector region.
   - That is a coincidence signature (prompt ISR jet + MET, then an out-of-time calorimeter deposit at the extrapolated impact point). It is not used anywhere. WORTH A CHECK, at the 1-3 % level of the triggered 1 TeV signal.
4. **The internal energy does not prevent stopping.** The CM stops first (Evans-Luty Sec.2), and the stop times of 0.1-0.4 µs include the internal dissipation. Λ-independence holds between 0.3 and 3 keV within statistics (3 keV: isr 1 TeV 3.7 %, incl 0-0 %).

### 7.1 Higher-statistics run at Λ = 1 keV
`T3_stopping.py 400 1`; 400 events per (m_Q, sample); `figures/T3_stopping_1.npy`.

| sample | m_Q | **ECAL+HCAL \|η\| < 1** | other calorimeter (\|η\| ≥ 1) | coil | yoke | tracker | escaped | unfinished | median t_stop (fiducial) |
|---|---|---|---|---|---|---|---|---|---|
| isr | 200 | 0 (< 0.6 %) | 0 | 0 | 0 | 0 | 100 % | 0 | − |
| isr | 500 | 0 (< 0.6 %) | 0 | 0.3 % | 3.7 % | 0 | 95.5 % | 0.5 % | − |
| isr | 1000 | **1.3 ± 0.6 %** | 0.5 % | 1.5 % | 6.2 % | 0 | 90.2 % | 0 | 93 ns |
| incl | 200 | **1.5 ± 0.6 %** | 4.3 % | 0.5 % | 2.5 % | 0 | 89.5 % | 1.8 % | 86 ns |
| incl | 500 | **0.7 ± 0.4 %** | 7.5 % | 0 | 2.2 % | 0.7 % | 87.5 % | 1.3 % | 130 ns |
| incl | 1000 | **1.0 ± 0.5 %** | 5.0 % | 0.3 % | 3.0 % | 1.3 % | 89.0 % | 0.5 % | 352 ns |

**Summary for T6 (ESTIMATE; 0.3-1 keV, Λ-independent within statistics):**
- f_stop(ECAL+HCAL, |η| < 1) ≈ **1.0 ± 0.3 %** of all produced pairs (200-1000 GeV, mass-independent within errors).
- ≈ **6-9 %** stop in any calorimeter (|η| < 3), and ≈ **10-11 %** stop anywhere in CMS.
- For the p_T > 200 GeV triggered sample: 0 % at 200-500 GeV and 1.3-2.5 % fiducial (≈ 10-12 % anywhere) at 1 TeV.
- Stops happen 0.1-0.4 µs after the collision.
- The uncertainty is dominated by the low-p_T model of the inclusive sample (⟨p_T⟩ = 30 GeV assumed) and by the simplified outer geometry, not by statistics. ×2 either way is a fair band.

## 8. dE/dx signature (Q6)

Method (`T3_dedx.py`, ESTIMATE):
- Exact vacuum world lines; mean Bethe S(β) in silicon integrated along each quirk's path inside a sensor (150 µm IT1 at 3 cm; 290 µm PS3 at 52 cm; thicknesses UNVERIFIED).
- Events: LO DY+ISR p_T > 200 GeV, |η| < 1.
- Ratios are given to a MIP crossing the same sensor at the same angle.
- The path inside the sensor includes the zig-zag of the internal motion when ℓ < sensor thickness.

| m_Q | Λ [keV] | pair deposit / MIP (median, 16-84 %) | one HSCP at β_cm / MIP | pair / (2 × HSCP at β_cm) |
|---|---|---|---|---|
| 500 | 3 | 6.6 (3.5-13.5) | 4.7 (2.4-9.0) | 0.84 |
| 500 | 10 | 7.7 (3.8-18) | 4.7 | 0.89 |
| 500 | 30 / 100 | 8.9-9.1 (4.5-15) | 4.7 | 0.90 |
| 1000 | 3 | 16 (7-38) | 14 (5-34) | 0.67-0.71 |
| 1000 | 30 / 100 | 20-21 (8.5-38) | 14 | 0.75 |

At Λ = 3 keV the two quirks cross the layer at different points; the column gives the sum per layer.

Reading:
1. **The merged pair (Λ ≳ 20-30 keV) is not "≈ 2 × MIP".** That number comes from FASER [2607.26195 p.4], where the pairs are relativistic (γ ~ TeV/m), and from D0 [1008.3547]. For the central, ISR-triggered sample the merged pair deposits a **median of 9× MIP (500 GeV) and 21× MIP (1 TeV)**, i.e. 0.75-0.9 × (two HSCPs at the pair-CM velocity).
   - The internal motion does **not** enhance the deposit. The longer zig-zag path inside the sensor is more than compensated by the higher instantaneous speed (S·v ∝ 1/β), so the ratio is < 1.
   - Practical statement for the strategy: **merged-pair dE/dx ≈ 1.5-1.8 × that of one HSCP of the same β**. Combined with 1/β from MTD, it gives a mass-like observable.
   - The ratio to an HSCP of the same β is ≈ 1.5-1.8, not 2. That is a distinctive "charge-2-like but not quite" signature. Unlike a |q| = 2 HSCP (4× at the same β), it **requires** the β measurement to be separated from charge-2.
2. **CMS Phase-2 readout.**
   - Only the IT has charge information (ToT, ≈ 4 bits [theory_signal_model §4.3], dynamic range UNVERIFIED). With 9-21× MIP medians and tails to ≳ 40× MIP, the IT ToT will saturate for a large fraction of hits. The Run-2 HSCP analysis needed a dedicated saturation correction even for strips [2410.09164 Sec.4].
   - The OT is binary, so no dE/dx there. The PS/2S HIP flag (a high-threshold bit) exists in the module design (UNVERIFIED). It would give a binary "HIP" tag per OT hit that the quirk passes on most layers.
   - The Run-2 strip "cluster cleaning" rejects multi-peak clusters [2410.09164 Sec.4]. It would reject the partially merged regime (Λ ≈ 10-20 keV, two quirks within one strip cluster) in any HSCP recast.
   - **Verdict: WORTH A CHECK.** The HSCP machinery (I_h from the IT, 1/β from the MTD) is directly applicable to the merged regime and to the high-mass core window. The quantitative gain depends on the ToT range, which is outside theory scope.
3. Resolved regime (Λ ≲ 10 keV): per-hit dE/dx follows each quirk's instantaneous β, between β_cm and β*. The hit-level 1/β² pattern along a single quirk oscillates with the period. In principle this is a phase tag (slow at the turning points), but only the 4 IT layers measure charge, so it is not usable. Killed.

## 9. Revised CMS Λ window

Signal efficiency of the Knapen plane cut Δs < 100 µm [1708.02243 Sec.IV] at truth-hit level. Inputs: causal NG, 3.8 T, Phase-2 material; p_T > 200 GeV, |η| < 1; no hit resolution, merging or PU. Sources: `T3_ms_thickness.npy` (0.3/1/3/10/30 keV, 60/24/12 events) and `T3_precession.npy` (0.6/1/2 keV, 24 events). ESTIMATE.

| m_Q | f(Δs < 100 µm), B+M, at Λ = 0.3 / 0.6 / 1 / 2 / 3 keV | Λ_low at 50 % (B only → B+M) | Λ for ≥ 90 % (B+M) | strategy Λ_low [STRATEGY_DRAFT §4.4] |
|---|---|---|---|---|
| 200 GeV | 0.10 / − / 0.98 / − / 1.00 | ≈ 0.5 → 0.5 keV | ≲ 1 keV | 0.54 (band 0.31-0.97) |
| 500 GeV | 0.07 / 0.83 / 0.96-0.98 / 1.00 / 0.98 | ≈ 0.45 → 0.45 keV | ≈ 0.8-1 keV | 0.69 (0.39-1.22) |
| 1000 GeV | 0.20 / 0.38 / 0.79-0.93 / 0.92 / 0.97 | ≈ 0.55 → 0.7 keV | ≈ 2 keV | 0.81 (0.46-1.45) |

At 200 GeV, Λ_low is interpolated between 0.3 and 1 keV; no 0.6 keV point was run.

Conclusions:
1. **Lower edge.** Λ_low(50 %) ≈ **0.45-0.7 keV** for 200-1000 GeV, inside the strategy's ×1.8 band and slightly below its central values. The causal B thickness is ∝ Λ^−1.9 with weak m_Q dependence, not m_Q/Λ⁴, so the edge is flatter in m_Q than the strategy's Λ_low ∝ m_Q^{1/4}.
   - **MS moves the 50 % edge only at 1 TeV (+0.15 keV).** But it lowers the efficiency plateau there: 79-93 % at 1 keV and 92 % at 2 keV, against 100 % without material. The "≥ 90 %" edge at 1 TeV therefore moves from ≈ 0.8 to ≈ 2 keV.
   - The numbers at 1 keV, 1 TeV differ between the two runs (0.79 with 24 events, 0.93 with 60). That spread is the statistical uncertainty.
2. **Upper edge.** It is unchanged by propagation effects: Λ_high^OT ≈ 11/16/19 keV and Λ_high^IT ≈ 22/31/39 keV [STRATEGY_DRAFT §4.4] come from two-hit merging, which MS does not affect. The MS thickness at 10-30 keV (2-20 µm) is far below the cut.
3. **Tighter Δs cuts are MS-limited.** If PU-200 forces Δs < 30 µm, the truth-level pass fraction at 3-10 keV becomes 0.93-0.92 (200 GeV), 0.68-0.83 (500 GeV) and 0.55-0.67 (1 TeV), compared with 1.00 without MS. At 1 keV it is 0.28-0.48. **The PU-driven optimisation of Δs must be done with MS in the signal model.** A Δs cut below ~30 µm costs ≳ 30-45 % of the heavy-mass signal at every Λ.
4. **Revised window statement (for the strategy):**
   - The coplanar finder at 3.8 T works from Λ ≈ 0.5 keV (200-500 GeV) or 0.7 keV (1 TeV) at 50 % plane efficiency, and from ≈ 1-2 keV at ≥ 90 %.
   - It extends up to the merging edge, ≈ 11-19 keV (OT) and 22-39 keV (IT-only).
   - The nominal "0.6-15 keV" stays a fair summary at 500 GeV. At 1 TeV the plateau starts later (≈ 2 keV) because of MS.

## 10. Gap entries

### G-T3-1  Multiple scattering sets a 10-25 µm floor on the quirk-plane thickness (first computation with an exact string)
- **Current treatment.** No quirk propagation includes MS or straggling in the EoM. Knapen et al. neglect material [1708.02243 Sec.II]. Li et al. include only the mean dE/dx with a 10 % smear [1911.02223; 2002.07503 Sec.VII]. Evans-Luty use continuous friction and explicitly do not model transverse kicks [1811.08903 App.B]. T5 estimated 50-400 µm as an upper bound with x/X0 = 1-3 % per layer and no plane fit (G-T5-1).
- **Why it is a gap.** The coplanarity cut acts at the 10⁻⁴ level of the trajectory. Heavy quirks are slow, so MS kicks of δp⊥ ≈ 13.6 MeV √x/β are comparable to the B-field effect.
- **Estimate (ESTIMATE, `T3_ms_thickness.py`, causal NG, Phase-2 material ≈ 19 % X0 at η = 0).**
  - Median Δs from MS alone is 11-24 µm, nearly independent of Λ from 0.3 to 10 keV, rising with m_Q (84th percentile ≤ 67 µm).
  - The B-only thickness is 32-38 µm at 1 keV and ∝ Λ^−1.9. **MS dominates for Λ ≳ 1.5-2 keV at every mass.**
  - The pass fraction of the 100 µm cut is ≥ 0.93-0.98 for 1-30 keV (≥ 0.79 at 1 TeV, 1 keV, in the 24-event sample), so the Knapen window survives.
  - A ≤ 30 µm cut would lose 30-45 % of the signal at 500-1000 GeV.
  - T5's upper bound is reduced ×5-20 by the plane fit and by the sharing of kicks within the pair. The pair direction turns by δp/|P|, not by δp/p_quirk.
  - The kick response is non-linear: a 10 MeV kick separates the two quirks out of the plane by up to ×3 the CM estimate, through crossing-induced rotation of the oscillation axis (`T3_kick.py`).
- **How to exploit.**
  - (c) The plane finder and the GNN training samples must include MS. The Δs cut can be optimised against PU only with it.
  - (e) A new signal systematic: material-budget uncertainty. Thickness ∝ √(x/X0), so a ±20 % material uncertainty gives ±10 % on Δs. That matters only if the cut is ≲ 50 µm.
  - (d) MS sets the floor below which the B-field thickness cannot be used as a Λ meter (Λ ≳ 1.5 keV).
  - (f) A short pheno note on MS and the causal string in quirk tracking is publishable.
- **Effort / confidence.** Done at toy level (days). The CMSSW version is the Athena-port item already in the strategy plus `G4hMultipleScattering`. Confidence **medium**: the per-layer x/X0 is UNVERIFIED (TDR not accessible), with ≈ ×1.4 on Δs for ×2 material (√ scaling, untested numerically).
- **Verdict: EXPLOIT** (the efficiency map and the Δs optimisation must include it; the window is not killed).

### G-T3-2  Instantaneous straight-string propagators are invalid as soon as material kicks (or fields) act; every published central-detector study is affected **[superseded, see erratum]**
- **Current treatment.** Knapen-Papucci, Li et al. and the GNN samples of Sha et al. use straight-string integrators [1708.02243 Sec.II; 1911.02223 Sec.III.B; 2410.00269 Sec.III]. Only the ATLAS/FASER Athena code is causal. T2 showed the B-field failure: thickness wrong by ×0.04-60. **[superseded, see erratum]**
- **Why it is a gap.** I show the same failure for material. With MS kicks and B = 0, a lab-simultaneous straight string gives median thicknesses of 220-580 µm at 3-10 keV and 2.5-21 mm at 30 keV. The causal string gives 10-24 µm and 2-6 µm on the same events (Sec. 3.1). The error grows with the number of crossings, because every near-miss crossing does spurious work.
- **Estimate.** As above; `T3_propagator.py` (lab straight string, validated in vacuum to 10⁻⁶ cm) vs `T3_causal.py` (numba port of Athena/T2, converged to 1-1.5 % in max_boost and step).
- **How to exploit.** (c)/(e) The CMS simulation must use the causal (Athena) algorithm; Geant4 material effects can then simply be switched on. Any recast of Knapen/Li efficiencies carries an O(1) unquantified error at Λ ≳ 2 keV. **[superseded, see erratum]** (f) Together with T2 §5, a "validation of quirk propagation" paper.
- **Effort / confidence.** Done (code in `T3_causal.py`, ~10³× faster than Python). Confidence **high** for the qualitative statement. Medium for the exact causal thickness, since it is not cross-checked against Athena itself.
- **Verdict: EXPLOIT** (simulation requirement).

### G-T3-3  Late hits: realistic per-layer losses and multiple hits per layer for heavy pairs
- **Current treatment.** The strategy uses the median pair at a fixed p_T(QQ̄) = 250 GeV [STRATEGY_DRAFT §4.2, OI-1]. Knapen applies a 25 ns cut [1708.02243 Sec.IV]. Li et al. note > 2 hits per layer in 10-20 % of events [2002.07503 Tab.I].
- **Why it is a gap.** The trigger sample has a falling p_T > 200 GeV spectrum. The internal motion and repeated layer crossings were not included.
- **Estimate (ESTIMATE, `T3_timing.py`).**
  - Median BTL delay 3.5 / 9.6 / 18.7 ns at m_Q = 200 / 500 / 1000 GeV (the strategy has 6 / 16 / 33 ns, which correspond to our 84th percentiles).
  - OT hits outside ±12.5 ns, per pair-CM crossing: 500 GeV 2S1/2S2/2S3 = 7 / 17 / 33 %; 1 TeV PS2/PS3 = 7 / 27 %, 2S = 44 / 57 / 68 %. The IT is never affected.
  - Per hit (including repeated crossings): 2S 21 % and PS 1 % at 500 GeV; 2S 70 % and PS 19 % at 1 TeV.
  - Heavy slow pairs make ≈ 3 hits per IT/PS layer per event (1 TeV, Λ ≥ 1 keV), not 2.
  - The internal motion spreads per-hit times by < 0.3 ns median for Λ ≥ 1 keV. It matters (ns) only at Λ ≲ 0.5 keV.
- **How to exploit.** (b)/(c) Plane finders must accept 3-4 hits per layer. The OI-1 readout study should use these per-layer fractions. (d) Repeated BTL crossings separated by Δt_c ≈ 0.3 ns (1 keV, 500 GeV) could measure the oscillation period, if TOFHIR records double hits.
- **Effort / confidence.** Days for analysis; the BTL double-hit question needs the MTD DPG. Confidence **high** for the CM numbers (exact kinematics, LO+ISR sample), medium for barrel acceptances (|z| limits UNVERIFIED).
- **Verdict: EXPLOIT** (corrects and refines OI-1). BTL period measurement: **WORTH A CHECK**.

### G-T3-4  Stopped-pair fraction f_stop(m_Q, Λ) at CMS for the triggered and the inclusive samples
- **Current treatment.** Evans-Luty [1811.08903 Fig.2, 6] give 1-5 % (|η| < 1) at 400 GeV, computed to 1 keV, with straight-string continuous friction. T6 used f_stop = 1-6 % without computing it.
- **Why it is a gap.** T6's delayed-annihilation channel yield is linear in f_stop. The triggered-sample stopping fraction was never computed.
- **Estimate (ESTIMATE, `T3_stopping.py`; causal string, Evans-Luty material; Sec. 7).**
  - Inclusive: f_stop(EB+HB, |η| < 1) = 1.0 ± 0.3 %, all calorimeter 6-9 %, anywhere ≈ 10 %, Λ-independent for 0.3-1 keV (3 keV consistent).
  - ISR-triggered: 0 % at 200-500 GeV; 1.3-2.5 % (fiducial) and 10-12 % (anywhere) at 1 TeV.
  - Stops occur at 0.1-0.4 µs.
- **How to exploit.**
  - (a) Use f_stop ≈ 1 % for an EB+HB recast of CMS 1801.00359 (reach ≈ 0.65 TeV per T6), or 6-9 % with the full calorimeter (≈ 0.9 TeV).
  - (b) New: for 1 TeV triggered events, a prompt ISR+MET event followed 0.1-1 µs later by an out-of-time deposit at the extrapolated position. That is a coincidence tag at the 1-3 % level, needing a delayed readout. WORTH A CHECK.
- **Effort / confidence.** Done (toy). A Geant4 version needs the Athena port. Confidence **medium**: low-p_T model and outer geometry give ×2.
- **Verdict: EXPLOIT** (number delivered to T6; it lowers T6's optimistic end unless the full calorimeter is used).

### G-T3-5  The merged pair is not a "2 × MIP" object at CMS
- **Current treatment.** "≥ 2× MIP" [theory_signal_model §4.3, 4.4; STRATEGY_DRAFT §4.3], taken from FASER (relativistic pairs) [2607.26195] and D0 [1008.3547].
- **Estimate (ESTIMATE, `T3_dedx.py`).**
  - For the p_T > 200 GeV central sample the merged pair (Λ ≥ 30 keV) deposits a median of 9× MIP (500 GeV) and 21× MIP (1 TeV), with 84th percentiles 15× and 38×.
  - That is 0.75-0.90 × two HSCPs at the pair velocity. The internal motion slightly *reduces* the deposit.
- **How to exploit.** (b) The high-Λ category should be an HSCP-like selection: IT I_h plus MTD 1/β plus the OT HIP bit. It is distinguishable from a |q| = 2 HSCP (4× at the same β) only with the β measurement. (a) A recast of the CMS HSCP search [2410.09164] with pair kinematics is possible, but Run-2 strip "cluster cleaning" rejects partially merged pairs.
- **Effort / confidence.** Days (parametric recast inputs); confidence medium (mean Bethe, ToT saturation UNVERIFIED).
- **Verdict: WORTH A CHECK** (EXPLOIT as a correction to the strategy's merged-regime description).

### G-T3-6  Plane precession in B as a Λ meter
- **Estimate.**
  - The secular plane rotation over the tracker is 3-18 µrad at 0.6-1 keV and ≤ 0.3 µrad at ≥ 3 keV.
  - The MS-induced equivalent is 4.5-10 µrad.
  - The inner-vs-outer plane angle is ill-conditioned (Sec. 4.2).
  - Field non-uniformity: B_r ≤ 0.9 % at |η| < 1.
- **Verdict: NOT A GAP (killed).** The B thickness itself (Λ^−1.9, usable for Λ ≲ 1.5 keV) and the crossing period are the Λ handles (to T4).

### G-T3-7  Net-charged pairs and charge-changing ends
- **Estimate.**
  - Doublet and triplet charged members decay before 3-15 cm (survival ≤ 1.5 % at 15 cm).
  - For a stable net-charged pair the CM follows a helix (R_c = 219 m at p_T = 250 GeV, sagitta 0.67 mm over 1.08 m), which fails a planar fit through the PV but is a simple helicoidal sheet.
- **Verdict: NOT A GAP for the current benchmarks.** WORTH A CHECK only if a stable net-charged model is adopted.

## 11. Killed ideas

| Idea | Killing number |
|---|---|
| Delta rays change the plane | maximal transverse recoil ≈ m_eβγ√2 ≈ 0.2 MeV (βγ = 0.3) ≪ MS kick 5-15 MeV per layer; already inside Highland (Sec. 2) |
| Energy-loss straggling thickens the plane | force ∥ v ⊂ plane; B+E vs B thickness identical within statistics (Sec. 3.2 table) |
| Field non-uniformity (B_r) in the barrel | B_r/B₀ ≤ 0.9 % at \|η\| < 1, ≤ 2.4 % anywhere in the tracker volume (overestimate, no yoke) → ≲ 1-2 % on the thickness (Sec. 4.3) |
| Internal motion enhances the merged-pair dE/dx | pair deposit = 0.75-0.90 × two HSCPs at β_cm: zig-zag path compensated by higher speed (Sec. 8) |
| Hit-level dE/dx phase tagging in the resolved regime | only 4 IT barrel layers measure charge (OT binary) |
| Triplet / doublet charged-member decay as a tracker quirk signature | survival to R = 15 cm ≤ 1.5 % (triplet, 200 GeV), ≤ 0.2 % at 3 cm (doublet) (Sec. 5) |
| Lab-simultaneous (or any instantaneous) straight-string propagation with material kicks | **[superseded, see erratum]** spurious thickness 0.2-21 mm at Λ = 3-30 keV vs 3-25 µm with the causal string (Sec. 3.1) – the model, not the effect, is killed |

## 12. Open questions for other workstreams

- **T2.**
  - (i) Independent cross-check of the causal B-field thickness, which I find ∝ Λ^−1.9 and nearly m_Q-independent (32-38 µm at 1 keV for 200-1000 GeV). T2's 4-event study agrees.
  - (ii) T2's `LabStraightString` "free nudge" step after crossing events introduces ~2 µm hit errors after ~170 crossings at 2 keV (Sec. 3.1). This is irrelevant now that the causal string is the reference.
  - (iii) Theory of the non-linear kick response: crossing-induced rotation of the oscillation axis (`T3_kick.py`).
- **T4.**
  - Λ handles after discovery are the B thickness (Λ ≲ 1.5 keV), the crossing spacing/period, and a possible BTL double-hit Δt_c. Precession is killed.
  - The trajectory fit must include an MS term: 4.5-10 µrad tilt, 10-25 µm thickness.
  - 3-4 hits per layer at 1 TeV.
- **T6.** f_stop from Sec. 7, for the yields. Calorimeter vs yoke split.
- **Experimental Phase 2.**
  - (i) Real Phase-2 per-layer material (TDR Fig. of x/X0 vs η, or tkLayout) to replace my UNVERIFIED 19 % X0.
  - (ii) Δs cut optimisation with MS-including signal: cuts below ~30 µm cost 30-45 %.
  - (iii) OT per-layer late-hit losses (Sec. 6) for OI-1; 2S SampledMode.
  - (iv) TOFHIR double-hit capability and dead time for a quirk crossing the BTL twice within ~0.1-1 ns.
  - (v) IT ToT dynamic range and the OT HIP bit for 9-21× MIP merged pairs.
  - (vi) Use the Athena causal algorithm (not a straight-string toy) for any fast propagator (W3).

## 13. References opened

- **0805.4642** (Kang-Luty): endpoint EoM Eq.3.8 (used via T2's code), the F_ext ≪ Λ² criterion Eq.3.10.
- **1708.02243** (Knapen et al.): torque estimate Eq.5-9 and Sec.II (ionisation torque ~10⁻³ per layer), plane-thickness definition Eq.11 and the Δs < 100 µm cut (Sec.IV), the 25 ns cut.
- **2002.07503** (Li et al.): Eq.II.15-II.21 (first-order B correction, z±), Eq.V.5-V.9 (thickness formula), Sec.V.A (charge dependence, ×20 for net-charged pairs), App.C accuracy statement, Sec.VI (> 2 hits per layer).
- **1911.02223**: Eq.III.12 thickness formula (via theory_signal_model.md and T2; not re-read).
- **1811.08903** (Evans-Luty): Sec.2 (stopping mechanism, Fig.2 1-5 % for 400 GeV, flat above 300 eV), App.A Tab.1 (CMS cylinder model, fill factors; used as the outer material model), App.B (de-excitation).
- **2407.13721**: Phase-2 TBPX prototype module material budget (0.825 % estimate; 0.72 ± 0.05 % and 0.95 ± 0.09 % measured), Tab.1.
- **1912.02061**: CMS OT for HL-LHC (only the qualitative material-reduction statement and Fig.3 caption; no numbers extractable from text).
- **2404.08794**: CMS 2S module beam test (searched for material numbers; none per module).
- **2410.09164**: CMS HSCP Run-2 – I_h definition Eq.3-4, saturation correction and strip "cluster cleaning" (Sec.4).
- **2607.26195**: FASER "≈ 2 × muon charge" statement (via theory_signal_model/strategy).
- Not opened (CDS unreachable): Phase-2 Tracker TDR CERN-LHCC-2017-009; MTD TDR CERN-LHCC-2019-003; tkLayout material pages (HTTP 404). PDG RPP Highland formula and Bohr straggling: recalled (UNVERIFIED).
- Internal: T2_string_dynamics.md §2, §5 (causal vs straight string, crossings), T2 code; T5 G-T5-1/2 and §8; T6 G-T6-2/4 and `T6_stopping.py`; T1 Λ convention; theory_signal_model.md §3-4; STRATEGY_DRAFT §4.2-4.4, C2, C8, OI-1.
