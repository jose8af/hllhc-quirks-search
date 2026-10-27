# T2: Quirk-string dynamics in vacuum (oscillation length, period, angular momentum, approximations)

Investigator: T2 (theory track, C001 quirks). Date: 2026-10-07. Status: COMPLETE (2026-10-08).

> **ERRATUM (2026-10-08, fix pass F1, after review R1-critical A-1 and B-8). This report is otherwise unchanged.**
> - `LabStraightString` ("labSS", "lab-simultaneous straight string (≈ Li et al.)") and `CMStraightString` ("cmSS") are **not** the Li et al. algorithm, and no published paper uses them. Li et al. advance the quirks at different lab times so that they stay CM-simultaneous, which is covariant by construction [1911.02223 Eq.III.6-10]. The check "Li's ŝ reduces to the lab-simultaneous direction" holds only on the exact vacuum solution.
> - The literal Li integrator, step-converged, agrees with the causal string to 0.84-1.05 in thickness at 0.6-2 keV (`code/R1_li_literal.py`; on this report's own events: `code/F1_li_phase.py`, `code/F1_standin.py`, where labSS/Li = 1.6-73). At Li's printed step bound the Euler integration is not converged (×0.8-20). Convergence needs a step fraction that shrinks with Λ.
> - Therefore the statements marked **[superseded, see erratum]** below apply to labSS/cmSS only, not to Knapen, Li or the GNN samples: ×0.04-60 thickness; OT hits 0.2-35 mm; 140-570 µm frame dependence "(≈ Li et al.)"; "every central-detector study carries an O(1) model error"; "Λ^−2.5".
> - The causal column of §5.1 (max_boost 10⁻², 4 events) differs from the converged causal string by up to 25 % on the same events, and the Λ^−2.5 scaling is replaced by T3's Λ^−1.6…−2.0.
> - The causal port is independently confirmed as **exact classical Nambu-Goto** with point endpoints (conformal-gauge solver, ≤ 1 %; `code/R1_conformal_ng.py`). Near-miss crossings with b < 1/Λ (Λ ≳ 10-20 keV) lie outside the NG effective theory.
> - Unaffected: the vacuum results, closed forms, ISR, J, crossings, semiclassics, the MaxSteps killer and the ε(b) analysis.
> - Current statement: `outputs/THEORY_GAPS_SYNTHESIS.md` S-1, X-13.

> **ERRATUM 2 (2026-10-11, synthesis v5 fixer SYN5, from Stage 1 `analytic/PROPOSED_CHANGES.md` items 1 and 9). This report is otherwise unchanged.**
> - The **even-crossing miss distances** of §5.3 ("b ≈ 16-30 Å at 1 keV and 0.13-0.19 Å at 3 keV") and of the §6.3 table column "b, even crossings" (16-31 Å / 0.13-0.19 Å / 10⁻⁴-2×10⁻³ Å, and the 30-100 keV rows) are **not converged physical values**. Statements marked **[not converged, see erratum 2]** below are affected.
> - In a pure CM field E* ⊥ n̂ the causal code's even-crossing b is a splitting artefact ∝ max_boost: b_even/b_odd = 2.6×10⁻³ / 3×10⁻⁴ / 2.7×10⁻⁵ at max_boost 10⁻² / 10⁻³ / 10⁻⁴ (`analytic/checks/c03_*`; `analytic/numerics/NUMERICS.md` §2.2 M2b). Physically **b_even = 0 at first order** (J = 0 at every even crossing; DERIVED, `analytic/NEAR_MISS_IMPULSE.md` §3.1, §6.1).
> - In full events b_even is second order (E*∥ and the per-period rotation): ≲ 10⁻³ b_odd at 1 keV, growing with the crossing index, solver-dependent at 20-60 %, and below the double-precision floor of both solvers (b/ℓ₀ ≈ 3×10⁻⁸) above ≈ 2-3 keV (ESTIMATE; NUMERICS §3 M1, §8 item 4). Even crossings carry no log impulse.
> - The odd-crossing values stand (b_odd = 2ε⊥ℓ₀[γ* − asinh ρ/ρ], DERIVED and VERIFIED-NUM to 10⁻⁴; median ≈ 3.5 µm (keV/Λ)⁴ at 500 GeV, 3.8 T).
> - "Even crossings reconnect within 1/Λ from Λ ≈ 3 keV" (§6.3) holds **a fortiori, as an upper bound** on b_even. The ε_gb (glueball emission per crossing) conclusions keep their direction (ε_eff ≈ 0 for Λ ≲ 2 keV; ≈ ε/2 from ≈ 3 keV; ≈ ε above ≈ 30 keV).
> - Current statement: `outputs/THEORY_GAPS_SYNTHESIS.md` (v5) S-3 "NG validity", S-19, X-13.


Conventions: Λ ≡ √σ (BRIEF §1). Natural units unless stated; ħc = 1.97327×10⁻¹⁴ GeV·cm, c = 29.979 cm/ns.
Code: `theory_track/code/T2_*.py`. Figures: `theory_track/figures/T2_*.png`.

## 1. Executive summary
1. **The vacuum problem is solved exactly, and the vacuum "simultaneity problem" does not exist.**
   - In the CM frame the point-produced pair is an exact 1-D yo-yo. In the lab the string is straight with a fixed direction n̂⊥ + n̂∥/γ.
   - The Li et al. lab closed form [2002.07503 Eq.II.4-8], lab- and CM-straight integrators, and the Athena causal algorithm all agree to ≤ 2×10⁻⁸ ℓ_max (33/33 tests).
   - Exact formulas (Sec. 2.2): ℓ_max = 3.95 cm (γ*−1)(m/100 GeV)(keV/Λ)², and **N_osc(r<R) = σR/(2β*p_T) ≈ 12 (Λ/keV)² inside the CMS tracker, independent of m_Q**.
   - Literature shorthands are off by ×0.5 ("2 cm (γ−1)", systematic) and ×0.4-2.7 per event ("1 cm (m/100 GeV)").
2. **The DY oscillation-length distributions are fixed by M_QQ̄** (Tab. 3.1). Examples, medians with p_T(QQ̄) > 200 GeV: ℓ_max = 5.4 cm (500 GeV, 1 keV), 0.54 mm (10 keV), 60 cm (0.3 keV).
   - **44-47% of triggered pairs make < 1 oscillation in the tracker at Λ = 0.3 keV.**
   - A fixed-p_T ISR kick biases ℓ_max by −10 to −25% and N_osc by +20%.
3. **Main gap (G-T2-1, EXPLOIT).** The instantaneous straight-string approximation used by every central-detector trajectory study (Knapen, Li, and through them the GNN samples) is **uncontrolled at first order in F_ext, the order of the plane thickness**. **[superseded, see erratum]**
   - It is not Lorentz covariant: 140-570 µm frame dependence on a 150-190 µm effect. **[superseded, see erratum]**
   - It does spurious work at every crossing (−1.6 MeV per crossing in a pure B field).
   - In 3.8 T it gives thicknesses ×0.04-60 off and OT hit positions 0.2-35 mm off relative to the exact causal Nambu-Goto string. **[superseded, see erratum]**
   - **The ATLAS Athena quirk algorithm is that exact causal string.** It is exact, covariant to 0.05 µm and momentum conserving (verified with a Python port). No physics error was found in it.
   - It does carry a step-count killer (MaxSteps 2×10⁶) that would kill quirks inside a CMS-size tracker for Λ ≳ 24 keV (G-T2-2, WORTH A CHECK).
4. **Angular momentum.**
   - DY gives J ≤ 2.45ħ, so the rotating component is 3×10⁻¹⁷. Vacuum motion is collinear in the CM and hence planar.
   - In 3.8 T the quirks miss each other at crossings by b ≈ 3.5 µm (keV/Λ)⁴ (odd crossings), so J ≫ ħ from the first crossing. There is no capture or annihilation at crossings.
   - Glueball emission (ε) can act only when b < 1/Λ. In 3.8 T that is none of the crossings for Λ ≲ 2 keV, half of them for 3-20 keV, and all of them above about 30 keV. ε = 0.1 has no derivation; it is irrelevant for CMS and a structural (b-dependent) uncertainty for FASER at Λ ≥ 30 keV (G-T2-5).
5. **Semiclassics is excellent**: n ≈ 2×10¹⁶, spreading ~nm, Larmor ≲ 300 eV over the tracker. A tested vacuum and causal propagator is delivered for T3 (`code/T2_propagator.py`).

## 2. Exact vacuum solution and improved formulas

### 2.1 The exact solution is a 1-D yo-yo plus a Lorentz boost
Setup: Nambu-Goto string with massive endpoints, S = −m₁∫dτ₁ − m₂∫dτ₂ − σ∫dA [0805.4642 Eq.3.7; 1708.02243 Eq.2], endpoint equation of motion [0805.4642 Eq.3.8-3.9]. The pair is produced at one point with zero string length.

1. **CM frame.** The two quirks start at the origin with momenta ±p* n̂, so the motion is exactly one-dimensional along n̂. The world sheet is the flat region of the (t*, x*) plane between the two world lines. This is an exact solution of the full Nambu-Goto problem, not only of the straight-string ansatz: a 1-D string between collinear endpoints has no transverse degrees of freedom, and a Nambu-Goto string has no longitudinal ones [0805.4642 Sec.3.3]. The force on each endpoint is exactly σ, so the momentum of quirk 1 along n̂ is a triangle wave:
   q(t*) = p* − σt* for 0 ≤ t* ≤ 2p*/σ, then rising back, with full period T* = 4p*/σ.
   Positions: x₁* = ±(E₁* − √(m₁²+q²))/σ and x₂* = ∓(E₂* − √(m₂²+q²))/σ. The centre of energy, including the string, stays at the origin (verified to 10⁻¹²; `T2_test_propagator.py`).
2. **Lab frame.** The lab trajectories are the exact Lorentz transforms of these world lines. No simultaneity approximation is needed. The world sheet is a flat timelike 2-plane, so every lab-time slice of it is a straight segment. **In the lab the string is straight and has a fixed direction** ŝ_lab ∝ n̂⊥ + n̂∥/γ_pair, where ∥ and ⊥ are taken relative to the pair velocity. This equals unit(v₁ − v₂) at production (ESTIMATE, derivation Sec. 2.3; checked numerically).
3. **Consequences for the existing methods (ESTIMATE, numerical checks in `T2_test_propagator.py`, 33/33 pass):**
   - The Li-Li-Pei-Zhang lab-frame closed form [2002.07503 Eq.II.4-II.8] is **exact in vacuum**: it agrees with the boosted exact solution to 3×10⁻¹⁴ ℓ_max. It is not an approximation, contrary to its billing as "approximate".
   - A lab-frame integrator of the Kang-Luty equation with ŝ along the lab-simultaneous separation reproduces the exact solution to 10⁻¹⁰ ℓ_max.
   - The Li prescription for ŝ (CM-simultaneous events plus extrapolation along v₁) [1911.02223 Eq.III.6-III.9; 2002.07503 Eq.VIII.1-VIII.4] returns the exact ŝ_lab, to 2×10⁻⁸ rad, when fed the exact solution.
   - A Python port of the ATLAS Athena causal string algorithm reproduces the exact solution to ≤ 2×10⁻⁸ ℓ_max for maxBoost = 10⁻² and 10⁻¹ (Sec. 5.1).
   - So **in vacuum the "simultaneity problem" does not exist**: all four descriptions agree. Differences appear only at O(F_ext) (Sec. 5.1).

### 2.2 Improved formulas (closed forms; exact in vacuum unless stated)
Notation: m = m_Q; γ*, β*, p* = mγ*β* are the per-quirk CM quantities; M = 2γ*m = M_QQ̄; (βγ)_pair = |P_QQ̄|/M; σ = Λ² = **50.68 GeV/cm × (Λ/keV)²**. All entries are ESTIMATE; the derivations are in Sec. 2.1 and 2.3 and the code in `T2_propagator.py`.

| Quantity | Exact closed form | Numerical form | Validity |
|---|---|---|---|
| String tension | σ = Λ²/ħc | 50.68 GeV/cm (Λ/keV)² = 5.07 GeV/mm (Λ/keV)² | definition Λ ≡ √σ |
| Max CM separation | ℓ_max = (M − m₁ − m₂)/σ = 2(γ*−1)m/σ | **3.947 cm (γ*−1)(m/100 GeV)(keV/Λ)²** | exact in vacuum, any γ*, unequal masses allowed |
| CM time between crossings | t_c* = 2p*/σ (full period 4p*/σ) | 0.1317 ns γ*β* (m/100 GeV)(keV/Λ)² | exact; also relativistic |
| Lab distance between crossings along the pair line of flight | D = 2p*(βγ)_pair/σ | 3.947 cm γ*β*(βγ)_pair (m/100 GeV)(keV/Λ)² | exact (crossings are CM events at the CM origin) |
| Lab time between crossings | Δt_c = 2p*γ_pair/σ | 0.1317 ns γ*β* γ_pair (m/100)(keV/Λ)²; equals Li's t_p [2002.07503 Eq.II.8] | exact |
| **Oscillations inside a barrel of radius R** | N_osc = N_cross/2 = σR M/(4p* p_T,QQ̄) = **σR/(2β* p_T,QQ̄)** | **N_osc = 9.3 (R/1.1 m)(Λ/keV)² (0.6/β*)(500 GeV/p_T,QQ̄)**, independent of m_Q | exact for barrel exit, no external force |
| Lab string direction | ŝ_lab ∝ n̂⊥ + n̂∥/γ_pair = unit(v₁−v₂) at t = 0 | fixed in time | exact in vacuum |
| Max lab-simultaneous separation | L_lab = 2(m/σ)(γ* − √(1+u²))·√(1−β²cos²θ*), with u = |β cosθ*|(γ* − √(1+u²)) | ≤ ℓ_max; u ≈ |βcosθ*|(γ*−1) | exact (equal masses) |
| Max lab width ⊥ pair direction | w_T = 2(m/σ)(γ* − √(1+u²)) sinθ* | Li's L = ℓ_max sinθ* [2002.07503 Eq.III.1] overestimates by 0.8% (median), 13% (98th percentile) at 500 GeV, and by 2% (24%) at 200 GeV | exact |
| CM velocity distribution | the momentum of each quirk is uniform in time on [−p*, p*] | βγ uniform on [0, γ*β*] | exact |
| Energy stored in the string | ⟨E_str⟩/E_kin = (γ* − ⟨E⟩/m)/(γ*−1), ⟨E⟩/m = ½[γ* + asinh(γ*β*)/(γ*β*)] | 2/3 (non-relativistic virial) → 1/2 (ultra-relativistic); **0.62-0.66 for DY pairs** | exact |
| Relativistic yo-yo limit γ* ≫ 1 | ℓ_max → 2E*/σ, t_c* → ℓ_max; the endpoints move at ≈ c except within m/σ of the turning point | − | DY pairs never reach it: 84% quantile γ* ≤ 2.0 (E), ≤ 2.5 (Ẽ, 200 GeV) |

### 2.3 Derivation of the lab-frame string direction and width (sketch)
- Boost along the pair velocity β. A CM displacement Δx* n̂ taken along a lab-simultaneous slice (Δt* = −β cosθ* Δx*) becomes Δx_lab = Δx*[n̂ − (1 − 1/γ)cosθ* β̂]. Its direction is fixed, and its length is |Δx_lab| = Δx*√(1 − β²cos²θ*).
- The world-sheet region {|x*| ≤ X(t*)} is convex and centrally symmetric, since X(t*) = (m/σ)[γ* − √(1+(ρ − σt*/m)²)] is concave. Its longest chord along the slice direction therefore passes through the centre (x* = 0, t* = p*/σ). This gives the implicit equation for u in the table. Brute-force maximisation agrees to < 10⁻⁵ (`T2_test_propagator.py`).

### 2.4 Accuracy of the literature shorthands (Q1)
Ratio of each shorthand to the exact value, quantiles over LO DY pairs at 14 TeV with p_T(QQ̄) > 200 GeV (Sec. 3). ESTIMATE; `T2_approx_errors.py`, figure `figures/T2_approx_errors.png`.

| Shorthand (source) | E 500 GeV (16/50/84%) | Ẽ 500 GeV | E 1000 GeV | E 200 GeV | Verdict |
|---|---|---|---|---|---|
| "d_cm ~ 2 cm (γ−1)(m/100 GeV)(keV/Λ)²" [1708.02243 Eq.1; 2410.00269 Eq.1; also ℓ_c in 2002.07503 Sec.III] | 0.507 (constant) | 0.507 | 0.507 | 0.507 | This is the distance of each quirk from the CM. As a separation it is **low by ×1.97**. The same paper's Eq.4 gives the exact separation (max 3.95 cm…). |
| "ℓ ~ 1 cm (m/100 GeV)(keV/Λ)²" [2404.13814 Eq.2.6; 2607.26195 p.2; 2512.20696 Eq.1] = "10 cm (m/TeV)(keV/Λ)²" [1811.08903 Eq.1.1] | 0.38 / 0.92 / 2.7 | 0.26 / 0.54 / 1.24 | 0.57 / 1.31 / 3.9 | 0.25 / 0.64 / 1.9 | Right on average for E at ~500 GeV, which corresponds to γ*−1 = 0.25. Event by event it is wrong by a factor ~3 either way. It **underestimates scalars by ×1.9**. |
| Non-relativistic ℓ = mβ*²/σ | 0.48 / 0.70 / 0.88 | 0.39 / 0.57 / 0.76 | 0.59 / 0.77 / 0.91 | 0.37 / 0.62 / 0.83 | −30% (E) to −43% (Ẽ). Do not use. |
| Massless yo-yo ℓ = 2E*/σ | 2.5 / 4.6 / 11.7 | 2.0 / 3.1 / 5.9 | 3.3 / 6.2 / 16 | 2.0 / 3.5 / 8.7 | ×3-6 too large. DY pairs are far from the ultra-relativistic limit. |
| Crossing time 2√(2mE_kin)/σ [1811.08903 below Eq.B.3; 2404.13814 above Eq.4.2] | 0.87 / 0.94 / 0.98 | 0.82 / 0.90 / 0.95 | 0.91 / 0.96 / 0.98 | 0.81 / 0.91 / 0.97 | −6% (E) to −10% (Ẽ) bias in the oscillation period and hence in N_osc. Ratio = √(2/(γ*+1)). |
| Li et al. width L = ℓ_max sinθ* [2002.07503 Eq.III.1] | +0.8% median, +13% at the 98th percentile | − | − | +2%, +24% | Adequate; the exact form is in the table above. |
| Plane-thickness formula [2002.07503 Eq.V.6; 1911.02223 Eq.III.12] | − | − | − | − | Not a vacuum quantity (∝ B). Its stated accuracy of "within an order of magnitude" [2002.07503 App.C] concerns the B-field correction, not the vacuum part, which is exact. See Sec. 5.1 and T3. |

Bottom line for Q1:
- The vacuum kinematics is a solved problem: the exact formulas are elementary and already used correctly in `research/theory_signal_model.md` §1.1 and Tab.4.2a, which I confirm.
- The shorthands in abstracts and introductions are off by factors 0.5-3. Only the factor-2 inconsistency of the "2 cm (γ−1)" form is systematic.
- **Recommendation:** quote ℓ_max = 3.95 cm (γ*−1)(m/100 GeV)(keV/Λ)² and N_osc = σR/(2β* p_T) in all CMS documents.

## 3. Oscillation lengths at the 14 TeV LHC (Q2)

**Model** (ESTIMATE; `code/T2_kinematics.py`; figures `T2_lmax_distributions.png`, `T2_nosc_tracker.png`, `T2_isr_assumptions.png`):
- Parton-level LO at 14 TeV with CT18NLO (lhagrid1 read directly). The quirk is a vector-like singlet with charge −1, γ*/Z couplings as in `research/theory_signal_model.md` App. A.
- *Inclusive*: q q̄ → γ*/Z → QQ̄ with p_T(QQ̄) = 0.
- *ISR sample*: exact 2→2 matrix elements q q̄ → V*(M) g and q g → V*(M) q, times the V*(M) → QQ̄ line shape C_q(M)R(β)/M². One-loop α_s, μ = m_T. Cuts p_T(QQ̄) > 200 GeV and |η_QQ̄| < 2.5.
- Decay angle: (2 − β²sin²θ) for the fermion and sin²θ for the scalar, about the Collins-Soper axis. This is exact for the inclusive LO case and an approximation for V*+jet. It affects only the lab width w_T, not ℓ_max or N_osc.
- Tracker: r < 110 cm, |z| < 270 cm. No external forces.

Validation: the inclusive γ* quantiles reproduce `theory_signal_model.md` Tab.4.1 exactly. Medians are 1.30/1.25/1.19 (E) and 1.55/1.44/1.32 (Ẽ) at m = 200/500/1000 GeV.

**Table 3.1: fermion E, 14 TeV** (ESTIMATE). Columns:
- ℓ_max: exact CM maximum separation;
- w_T: median exact lab width ⊥ to the pair direction;
- N_osc: oscillations (= crossings/2) inside the tracker;
- Δt: lab time between successive crossings.

| m_Q | Λ [keV] | selection | ℓ_max 16/50/84% | w_T 50% | N_osc 16/50/84% | frac(N_osc<1) | Δt_cross 50% [ns] |
|---|---|---|---|---|---|---|---|
| 200 | 0.3 | incl. (p_T=0) | 8.7 cm / 27 cm / 69 cm | 19 cm | 0.52 / 1.4 / 5.9 | 0.38 | 4.5 |
| 200 | 0.3 | p_T>200, \|η\|<2.5 | 11 cm / 34 cm / 87 cm | 24 cm | 0.63 / 1.1 / 1.8 | 0.44 | 4.7 |
| 200 | 1 | incl. | 7.8 mm / 2.4 cm / 6.2 cm | 1.7 cm | 5.7 / 16 / 65 | 0 | 0.41 |
| 200 | 1 | p_T>200 | 1.0 cm / 3.1 cm / 7.9 cm | 2.2 cm | 7 / 12 / 20 | 0 | 0.42 |
| 200 | 3 | p_T>200 | 1.1 mm / 3.4 mm / 8.7 mm | 2.4 mm | 63 / 109 / 181 | 0 | 0.047 |
| 200 | 10 | p_T>200 | 102 / 307 / 786 µm | 215 µm | 700 / 1.2×10³ / 2.0×10³ | 0 | 4.2×10⁻³ |
| 200 | 30 | p_T>200 | 11 / 34 / 87 µm | 24 µm | 6.3×10³ / 1.1×10⁴ / 1.8×10⁴ | 0 | 4.7×10⁻⁴ |
| 500 | 0.3 | incl. | 18 cm / 54 cm / 130 cm | 38 cm | 0.46 / 1.1 / 4.2 | 0.45 | 7.6 |
| 500 | 0.3 | p_T>200 | 20 cm / 60 cm / 144 cm | 43 cm | 0.58 / 1.0 / 1.9 | 0.47 | 7.3 |
| 500 | 1 | incl. | 1.6 cm / 4.9 cm / 12 cm | 3.4 cm | 5.1 / 13 / 47 | 0 | 0.68 |
| 500 | 1 | p_T>200 | 1.8 cm / 5.4 cm / 13 cm | 3.9 cm | 6.5 / 12 / 21 | 0 | 0.65 |
| 500 | 3 | p_T>200 | 2.0 mm / 6.0 mm / 14 mm | 4.3 mm | 58 / 104 / 186 | 0 | 0.073 |
| 500 | 10 | p_T>200 | 184 / 541 / 1300 µm | 388 µm | 650 / 1.2×10³ / 2.1×10³ | 0 | 6.5×10⁻³ |
| 500 | 30 | p_T>200 | 20 / 60 / 144 µm | 43 µm | 5.8×10³ / 1.0×10⁴ / 1.9×10⁴ | 0 | 7.3×10⁻⁴ |
| 1000 | 0.3 | incl. | 28 cm / 81 cm / 187 cm | 58 cm | 0.46 / 1.1 / 3.8 | 0.47 | 11 |
| 1000 | 0.3 | p_T>200 | 28 cm / 84 cm / 194 cm | 62 cm | 0.58 / 1.1 / 2.0 | 0.46 | 10.5 |
| 1000 | 1 | p_T>200 | 2.5 cm / 7.6 cm / 17.5 cm | 5.6 cm | 6.5 / 12 / 22 | 0 | 0.95 |
| 1000 | 3 | p_T>200 | 2.8 mm / 8.4 mm / 19 mm | 6.2 mm | 58 / 107 / 201 | 0 | 0.105 |
| 1000 | 10 | p_T>200 | 252 / 758 / 1750 µm | 557 µm | 650 / 1.2×10³ / 2.2×10³ | 0 | 9.5×10⁻³ |
| 1000 | 30 | p_T>200 | 28 / 84 / 194 µm | 62 µm | 5.8×10³ / 1.1×10⁴ / 2.0×10⁴ | 0 | 1.05×10⁻³ |

The inclusive rows for Λ ≥ 3 keV are omitted for brevity. They follow from the Λ = 1 keV rows: ℓ_max ∝ Λ⁻² and N_osc ∝ Λ². The full table is printed by the script.

Scalar Ẽ (p_T > 200): ℓ_max is ×1.70-1.73 larger (median) and N_osc is ×0.81 smaller, at all three masses.

**Findings:**
1. **N_osc in the tracker is independent of m_Q** at fixed p_T(QQ̄): about 12 (Λ/keV)² oscillations (median) for p_T > 200 GeV. This follows from the exact formula N_osc = σR/(2β*p_T) of Sec. 2.2. Heavier pairs oscillate with longer amplitude but move proportionally more slowly.
2. **At Λ = 0.3 keV, 44-47% of triggered pairs complete less than one oscillation inside the tracker.** Their topology is a pair of open, curved arcs, not an oscillation. This is the low-Λ edge already flagged in `theory_signal_model.md` §4.4. It means a plane or helix-pair fit must handle ≤ 1 crossing. The tracker sees ≤ 2 crossings for 84% of such events.
3. The p_T > 200 GeV requirement makes the N_osc distribution much narrower (the 16-84% band shrinks from ×10 to ×3). It shifts ℓ_max up by +12% (500 GeV) to +28% (200 GeV), because the V*+jet matrix element at fixed p_T favours larger M_QQ̄/2m_Q.

**Which ISR assumptions matter** (m = 500 GeV fermion, Λ = 1 keV, medians):

| Kinematics model | γ* | ℓ_max | (βγ)_pair | β_T | N_osc |
|---|---|---|---|---|---|
| inclusive LO (p_T = 0) | 1.246 | 4.85 cm | 0.77 | 0 | 12.6 (beam-axis exit) |
| fixed p_T = 250 GeV added to LO DY (the method of `theory_signal_model.md` App. A) | 1.246 | 4.85 cm | 0.81 | 0.141 | 12.2 |
| V*+jet ME, p_T > 200 GeV | 1.276 | 5.44 cm | 0.76 | 0.176 | 10.0 |

- ℓ_max depends only on M_QQ̄. The ISR requirement raises γ*−1 by 12% at 500 GeV and 32% at 200 GeV. The fixed-p_T trick misses this, and it biases ℓ_max low by about 10-25%.
- N_osc ∝ 1/(β* p_T). The real p_T spectrum above a 200 GeV cut has a median of 298 GeV, so the fixed-250-GeV trick overestimates N_osc by about 20%.
- The decay-angle model (Collins-Soper versus the true V*+jet spin density matrix) changes only w_T, through sinθ*, at the 10% level. It does not change ℓ_max or N_osc.
- **For the Phase-2 sample plan:** a matched V+jets generator (MLM/FxFx; `theory_signal_model.md` §3.5) gets all three effects right automatically. The approximation errors above matter only for fast parametric scans. Use the V*+jet ME, as in `T2_kinematics.py`, not a fixed p_T kick.

## 4. Angular momentum and planarity (Q3)

**4.1 What Drell-Yan gives.**
- Each quirk pair is produced at a single vertex by the s-channel γ*/Z current, so J = 1. This holds with or without the ISR jet: the jet is emitted by the initial partons, and the QQ̄ pair still comes from V*(M) → QQ̄.
- Vector-like fermion E: the vector current couples to ³S₁ and ³D₁, i.e. L = 0 or 2. S-wave dominates near threshold, where σ ∝ β. Scalar Ẽ: pure P-wave, L = 1, σ ∝ β³. [Standard partial-wave content of e⁺e⁻ → ff̄, S̃S̃; UNVERIFIED as quoted for quirks, but this is textbook QED.]
- Photon fusion (T6) gives J = 0 or 2. For every channel, |**L**| ≤ √6 ħ ≈ 2.45ħ.
- **Classical consequence** (ESTIMATE). The effective impact parameter is b₀ = L/p* ≈ 2.45 × 0.197 GeV fm / 375 GeV ≈ 1.3×10⁻³ fm (m = 500 GeV, γ* = 1.28). The rotational fraction is L/(p*ℓ_max) ≈ 2.45ħ/(375 GeV × 5 cm) ≈ 3×10⁻¹⁷.
- **The vacuum motion is exactly collinear in the CM**, so in the lab it lies in the plane spanned by n̂ and β̂_pair, through the IP. No macroscopic rotating component exists in vacuum.
- Quantum mechanically, the axis n̂ is not defined before the first interaction: the state is Y_LM ⊗ (radial yo-yo). The angular distribution dσ/dΩ* (1 + cos²θ*-like for E, sin²θ* for Ẽ) is the probability distribution of the axis. It becomes classical (decoheres) at the first ionisation or hit. There is no observable consequence beyond the angular distribution already in the generator.

**4.2 Angular momentum stored in the string; when a Regge-like rotating string matters.**
- In the 1-D yo-yo the string carries no angular momentum.
- A rotating (Regge-like) configuration needs J comparable to p*ℓ_max ≈ 2(γ*−1)γ*β* (m/Λ)². This is about 10¹⁷ ħ for m = 500 GeV and Λ = 1 keV. Only external torques can supply it:
  - **Magnetic field.** Knapen et al. find L ≈ 10¹² ħ within a few cm (2 T, 1.8 TeV, 2 keV) [1708.02243 Fig.2]. That is J/(p*ℓ_max) ~ 10⁻⁵: negligible as rotation, but decisive for short-distance physics at the crossings (Sec. 5.3).
  - **Ionisation.** One hard ionisation changes ℓ by ~m_e L ~ 10¹⁰ (m/TeV)(Λ/GeV)⁻² ħ [0805.4642 Eq.4.2]. After the TAS/TAN copper on the FASER line, J reaches ~10²-10³ m·GeV ≈ 10¹⁸ ħ at Λ = 300 eV [2108.06748 Fig.5]. That is comparable to p*ℓ_max: the motion becomes a genuinely rotating string on the FASER path. Propagation in matter is T3's topic; this is flagged to T3.
- **Planarity does not require J = 0, only that J be conserved.** Central string and Coulomb forces conserve J, so even a rotating pair stays planar. Non-planarity comes only from torques that change the direction of J (B field, ionisation). In vacuum the plane always contains the CM line of flight, and therefore the IP.

**Verdict on Q3.** In vacuum the motion is planar (in fact collinear in the CM), and the rotating component is ~10⁻¹⁶ of the yo-yo. Rotation becomes macroscopic only through matter and field torques (T3). The DY spin structure only enters the axis distribution.

## 5. Beyond the straight string: simultaneity, causal string, string modes, crossings (Q4)

### 5.1 (a) Straight string in the CM frame vs fixed direction vs the Athena causal string

**What the Athena code actually does** (read from gitlab.cern.ch/atlas/athena, `main`, `Simulation/G4Extensions/Quirks/src/{InfracolorForce,StringVector,HyperbolaStep,HyperbolaStepper,QuirkTransportation,QuirkWatcher,QuirkStackingAction}.cxx`, `python/QuirksConfig.py`; 2026-10-07):
- The string is a FIFO of **null 4-vectors** s ("string vectors moving towards tracked quirk, each carrying momentum of F_string × value", InfracolorForce.h).
- Absorbing s_in, a quirk of momentum p emits s_out = reflection of s_in about (p + F s_in) into the partner's queue (`StringVector::reflect`, `HyperbolaStep::PrepareNextStep`). It moves dx = s_in + s_out and changes momentum by dp = F(s_in − s_out) (`HyperbolaStep::Step`).
- I verified algebraically that this map:
  - keeps p² = m²;
  - composes exactly (absorbing λ₁ then λ₂ equals absorbing λ₁ + λ₂);
  - is the hyperbolic motion of a massive endpoint fed by a straight null segment.
- **It is therefore the exact Nambu-Goto dynamics** for piecewise-null world-sheet data, in the Artru/Lund piecewise-linear string tradition. It is causal: signals travel along the string at c. It makes no straight-string assumption, and 4-momentum (quirks + queued string) is conserved identically.
- Fields enter as a kick q(E dt + dx × B) after each string step, followed by mass-shell renormalisation. This is first-order splitting with ≤ 10⁻² rapidity per step (`maxBoost = 1e-2`).

**Numerical verification with a Python port** (`T2_propagator.CausalNullString`; tests in `T2_test_propagator.py`, `T2_covariance_test.py`; ESTIMATE):
1. Vacuum: it agrees with the exact solution to ≤ 2×10⁻⁸ ℓ_max for maxBoost = 10⁻² and 10⁻¹.
2. With fields: maxBoost 10⁻² and 2×10⁻³ agree to 0.2-1% in the out-of-plane displacement.
3. **Lorentz covariance with an external field.**
   - Setup: a pair produced at rest in a transverse field E₀ = 10⁻⁴σ is solved in its rest frame and transformed to frames where it moves with β = 0.6 or 0.9. Those lab-frame runs use the transformed fields E = γE₀ and B = γβ×E₀, and are compared with the transformed rest-frame result.

   | boost | causal (Athena port) | lab-simultaneous straight string (≈ Li et al.) | straight string in quirk CM | **[superseded, see erratum]**
   |---|---|---|---|
   | β = 0.6 ⊥ string axis | 0.05 µm | 146 µm (own rest-frame solution); 271 µm (vs causal) | 136 µm; 271 µm |
   | β = 0.6 ∥ string axis | 0.05 µm | 569 µm; 567 µm | 307 µm; 358 µm |
   | β = 0.9 ⊥ | 0.05 µm | 226 µm; 258 µm | 228 µm; 262 µm |

   The signal itself, max|z₁ − z₂| after 3 periods, is 150-190 µm (m = 500 GeV, Λ = 1 keV, γ* = 1.3).
   - **The causal string is frame independent to numerical precision.**
   - **Both straight-string prescriptions are frame dependent at 100% of the effect they are meant to compute.**
   - Even in the rest frame, causal and straight disagree. They agree to ≈ 3% over the first periods for γ* = 1.05, but differ by ≈ 20% in amplitude for γ* = 1.3 (`figures/T2_transverse_check.png`).
   - In the first half-period, before the first crossing, all methods agree with an independent solution of the **linearised Nambu-Goto equations** obtained by characteristics (`T2_transverse_linear.py`). That linear check is not valid after a crossing, where the transverse slope is no longer small.
4. **Realistic events** (`T2_string_methods_B.py`, `figures/T2_string_methods_B.png`). Setup: m = 500 GeV, γ* = 1.28, p_T(QQ̄) = 300 GeV, uniform 3.8 T, no material, ideal hits at the 10 CMS Phase-2 barrel radii. Results, 4 events per Λ:

   | Λ [keV] | d_min causal [µm] | d_min lab-straight | d_min CM-straight | max hit displacement straight vs causal | energy drift of quirks at crossings |
   |---|---|---|---|---|---|
   | 0.6 | 17-169 | 24-1080 | 13-77 | 0.9-9 mm | − |
   | 1 | 7-65 | 18-1140 | 3.5-19 | 0.55-10 mm | lab-straight −1.6 MeV/crossing, CM-straight −0.4 → −0.1 MeV/crossing, causal 0 (exact) |
   | 2 | 1.7-17 | 19-990 | 0.5-2.2 | 0.16-35 mm | |
   | 5 | 0.09-2.5 | 21-430 | 0.06-0.8 | 0.02-5 mm | |

   - **Straight-string thicknesses differ from the exact causal ones by factors 0.04-60, depending on the prescription.** **[superseded, see erratum]**
   - Hit positions at the outer layers move by 0.2-35 mm. Part of this is an accumulated oscillation-phase error, since the straight-string codes lose energy at every crossing.
   - The causal thickness falls roughly as Λ^−2.5 at 2-5 keV, not as the Λ^−4 of the analytic formula [1911.02223 Eq.III.12; 2002.07503 Eq.V.6]. It sits above that formula by ×10-30 at Λ = 5 keV. **[superseded, see erratum]**
   - Near Λ = 0.6-1 keV the causal thickness is within the ×10 band of the formula, so the coplanar window edge (Λ where d ≈ 100 µm, ≈ 0.6-0.8 keV) is not strongly moved (ESTIMATE, 4 events only).

**Why the straight string fails** (ESTIMATE):
1. **Crossings.** When F_ext ≠ 0 the quirks miss each other by b ∝ F_ext/σ (Sec. 5.3). An "instantaneous straight string" then swings through 180° in a time b/v. This is not a Nambu-Goto configuration: the string ends move transversely at ~c, while a signal needs ≥ b/c to cross the string. The straight-string force does spurious work of order σb per crossing. Example: labSS at Λ = 1 keV has b = 0.54 µm, σb = 2.7 MeV, and the measured drift is −1.6 MeV per crossing. A magnetic field does no work, so this is a pure artefact.
2. **Moving pairs.** In the lab the string carries momentum, so "the CM frame" and "simultaneity" are ambiguous at O(F_ext). Each choice gives a different O(F_ext) answer. Using the true conserved total 4-momentum (quirks + string) does not cure it: energy drift −35 to −170 MeV over the tracker, d_min still off by ×2-20 (ESTIMATE, same events).
3. **Order counting.** The out-of-plane observables are first order in F_ext/σ. The straight-string error is also first order. The condition F_ext ≪ σ [0805.4642 Eq.3.10] guarantees small angles, **not** a small relative error on the plane thickness.

**Comparison with what the literature says.**
- Li et al. state "choosing the correct ŝ direction is critical" and find mm changes when ŝ is fixed [2002.07503 Sec.VIII, Fig.6].
- I confirm that the fixed-ŝ approximation is wrong once F_ext ≠ 0: it has no transverse restoring force. The fixed direction is exact only in vacuum.
- I add that their own CM-simultaneous straight string is not controlled at the same order. When fed exact vacuum data, their Eq.VIII.3 reduces to the lab-simultaneous direction (checked to 2×10⁻⁸ rad). **[superseded, see erratum]**
- **Every published central-detector trajectory study uses a straight-string integrator**: Knapen-Papucci, Li et al., and through them the GNN samples of Sha et al. [1708.02243 Sec.II; 1911.02223 Sec.III.B; 2410.00269 Sec.III]. Their predicted plane thicknesses and hit positions therefore carry an unquantified O(1) model error. **[superseded, see erratum]** The only public exact implementation is the ATLAS/FASER Athena one.

**Athena code review: possible issues** (none is a physics error):

| # | Item | Effect | Status |
|---|---|---|---|
| 1 | `DistChord()` returns 0 and `yerr` = 0 (TODOs) | G4 chord-error control is disabled. Boundary-crossing points rely on the exact partial-absorption map plus G4's intersection tolerance. | probably harmless (positions on the exact hyperbola); UNVERIFIED in ATLAS settings |
| 2 | Field kick + `m_momentum *= mass/m_momentum.m()` ("TODO: possible instability") | O(maxBoost) splitting error | ≤ 1% at maxBoost = 10⁻² (port) |
| 3 | `MonopoleLooperKiller`, MaxSteps = 2×10⁶, BSM_Only (added by `QuirksPreInclude`) | about 200 y* G4 steps per crossing, N_cross ≈ 24(Λ/keV)² in a CMS-size tracker → **quirks killed inside the tracker for Λ ≳ 24 keV**; at FASER (γ_pair ~ 5, about 10⁵ crossings across 5 m at 100 keV) possibly killed inside the detector | ESTIMATE; FASER configuration UNVERIFIED |
| 4 | Bootstrap first string vector (1 nm), "borrowed" length | none (≤ 10⁻⁸ ℓ_max) | verified (port) |
| 5 | Comment "TODO: Check oscillation period" in StartTracking | none | − |

### 5.2 (b) Transverse string modes
- **In vacuum, none are excited**, because the point-produced yo-yo is exactly 1-D. Endpoint kicks from fields or matter excite them, and they travel at c along a string whose energy is a large fraction of the endpoint energy: up to 2(γ*−1)m, ≈ 0.56 m for γ* = 1.28. They are not a small correction.
  - The string delay is ℓ_max/c compared with the CM time between crossings 2p*/σ, a ratio of (γ*−1)/(γ*β*) ≈ 0.3 for DY pairs.
  - Consistently, causal and straight strings differ by ≈ 3% at γ* = 1.05 and ≈ 20% at γ* = 1.3 even in the pair rest frame (Sec. 5.1).
- **They do change the endpoint motion at first order in F_ext/σ.** This is exactly the order of the plane thickness and of the crossing miss distance. So the transverse modes are part of the signal model, not a refinement. A correct propagator must carry them, as the causal null-vector string does.
- Quantum transverse fluctuations (Lüscher roughening) give a string width w ≈ √(ln(ℓΛ)/π)/Λ ≈ 2.4/Λ ≈ 5 Å for ℓ = 1 cm, Λ = 1 keV (ESTIMATE). That is irrelevant for the µm-scale endpoint motion. The quantised mode spacing πħc/ℓ ≈ 6×10⁻⁵ eV (ℓ = 1 cm) means classically excited modes are highly occupied, so the classical treatment is valid.

### 5.3 (c) What happens at a crossing
- **Vacuum (no field).** The quirks pass through the CM with impact parameter b₀ ≈ L/p* ~ 10⁻³ fm (Sec. 4.1). This is far inside every short-distance scale: 1/Λ ≈ 2 Å/(Λ/keV), 1/m_Z ≈ 2×10⁻³ fm.
  - The infra-Coulomb plus QED attraction, α_eff ≈ C_F α_IC + α ≈ 0.04-0.05 [α_IC(m_Q) from `theory_signal_model.md` §6.2], is in the Born regime: Sommerfeld parameter η = α_eff/v_rel ≈ 0.05 ≪ 1.
  - In the fixed-L partial wave a central potential only adds a phase shift. There is no deflection and no capture: binding needs the loss of ~E_kin ≈ 100-300 GeV per crossing, while radiation per crossing is ≲ 10⁻⁸ eV (Sec. 6).
  - The quirks therefore **pass through each other**.
  - Formally, the field-free ³S₁ part of the fermion state re-focuses at the origin every period. Its annihilation probability would be P ≈ Γ_n T ≈ 4α²N_IC β*/γ* × R ~ 10⁻³ per period (ESTIMATE; linear-potential |ψ(0)|² = μσ/2π). But it needs b ≲ 1/m_Q, which any J ≳ few ħ destroys (next bullet).
- **With the CMS field** (exact causal propagator, uniform 3.8 T, m = 500 GeV, 3 events; `T2_crossing_missdist.py`). The miss distance alternates between crossings:
  - **odd crossings:** b ≈ 3.5 µm × (keV/Λ)⁴. This is the out-of-plane separation driven by the CM-frame electric field γβ×B, cf. d_E of [2002.07503 Eq.V.8];
  - **even crossings:** b ≈ 16-30 Å at 1 keV and 0.13-0.19 Å at 3 keV, slowly growing with crossing number; **[not converged, see erratum 2]**
  - field-free control: 10⁻⁵ Å (numerical noise).
  - Details are in the table in Sec. 6.3. So J ≫ ħ from the first crossing on (J = b p* ~ 10⁴-10¹⁰ ħ for Λ = 100-1 keV). **Annihilation in flight and any l ≈ 0 short-distance physics are switched off in the CMS field**, consistent with Kang-Luty's argument [0805.4642 Sec.4.1].
  - The miss distance b also replaces the Coulomb core as the relevant short-distance scale. Coulomb deflection at b ≫ α_eff/(p v) ~ 10⁻⁵ fm is negligible.

## 6. Semiclassical validity and radiation in vacuum (Q5)

**6.1 Quantum numbers and semiclassics** (ESTIMATE).
- The radial action is ∮p dr ≈ (4/3)p*ℓ_max (non-relativistic form), so n ≈ (2/3π)·2γ*β*(γ*−1)(m_Q/Λ)².
- That gives **n ≈ 2×10¹⁶ for m = 500 GeV, Λ = 1 keV, γ* = 1.28**. It scales as (m/Λ)², i.e. "n ~ E²/Λ²" holds up to O(1) kinematic factors.
- The level spacing is ΔE = 2πħ/T = πσ/(2p*) ≈ 4×10⁻⁶ eV (1 keV) × (Λ/keV)². The motion is deeply classical.
- Wave-packet spreading after localisation by ionisation to δ ~ 1 nm: Δx ≈ ħt/(m_Q δ) ≈ 0.5 nm over a 1.2 m (4 ns) flight. This is irrelevant compared with µm hit resolution.
- Before the first interaction the axis is a quantum superposition (Sec. 4.1). This has no observable consequence.

**6.2 Photon (Larmor) radiation.**
- For collinear acceleration with dp/dt = σ exactly, the Liénard power per quirk is P = (2/3)α σ²/m², independent of velocity.
- Energy per crossing: ΔE = (4/3)α σ p*/m² ≈ 1.5×10⁻⁸ eV × (Λ/keV)⁴ (m = 500 GeV, γ* = 1.28; ≤ ×4 for coherent dipole emission).
- Over the tracker (N_cross ≈ 24(Λ/keV)²) this gives ≲ 300 eV at Λ = 30 keV. Emitted frequencies are ~2π/T ~ µeV. **Negligible** (ESTIMATE), consistent with [2108.06748 Eq.4.22].
- Hard bremsstrahlung in the Coulomb core needs b ≲ α/(pv) ~ 10⁻⁵ fm, which never happens once J ≫ ħ (Sec. 5.3).

**6.3 Glueball emission per crossing (ε).**
- *Current treatment.* Probability ε per crossing to radiate ~Λ, dE/dt = −εΛ/T [1811.08903 Eq.B.3; 2404.13814 Eq.4.1], with ε = 0.1 "not calculable from first principles" [2404.13814 Sec.4], varied ±30% by FASER [2607.26195 p.5].
- *Is ε = 0.1 justified?* There is no derivation; it is a heuristic. What can be said (ESTIMATE):
  1. **Perturbative IC radiation from the smooth string acceleration is negligible.** The lightest glueball has m_G ≈ 3.5-3.8√σ (SU(2)/SU(3) lattice, UNVERIFIED recalled values, cf. 3.6√σ quoted in `theory_signal_model.md` §1.1). The acceleration time scale is p*/σ ≫ 1/Λ, and the only sharp feature is the sign flip of the force at the crossing. Radiated energy above m_G is ~α_IC(σ/m)²/m_G ~ α_IC Λ³/m², i.e. ~10⁻²⁰Λ per crossing.
  2. **Only non-perturbative flux-tube collapse and re-formation can emit glueballs.** This happens when the ends pass within ~1/Λ [0805.4642 Sec.3.3; 1811.08903 App.B.1]. For DY pairs the passage is non-adiabatic, since v_rel ≈ 0.9 and the passage time 1/(Λv) is comparable to the gluonic time scale 1/Λ. An O(0.1-1) probability is plausible but uncalculated.
  3. Each glueball carries ≥ m_G ≈ 3.7Λ. "εΛ per crossing" therefore means an emission probability ≤ ε/3.7 per crossing.
  4. **The relevant control variable is the miss distance b at each crossing**, which the ε model ignores. With the exact causal propagator (uniform 3.8 T, m = 500 GeV, 3 events, first 6 crossings; `T2_crossing_missdist.py`):

| Λ [keV] | 1/Λ [Å] | b, odd crossings [Å] | b, even crossings [Å] **[not converged, see erratum 2]** | b·Λ (median) | b < 1/Λ at |
|---|---|---|---|---|---|
| 1 | 1.97 | 3.5×10⁴ | 16-31 | 7.8×10³ | none |
| 3 | 0.66 | 431 | 0.13-0.19 | 288 | even crossings only |
| 10 | 0.20 | 3.5 | 10⁻⁴-2×10⁻³ | 7.8 | even crossings only |
| 30 | 0.066 | 0.043-0.048 | 10⁻⁶-2×10⁻⁴ | 0.29 | all |
| 100 | 0.020 | 3-6×10⁻⁴ | 3-6×10⁻⁴ | 0.024 | all |
| B = 0 control | − | 10⁻⁹-10⁻⁵ (numerical) | | ≤ 10⁻⁵ | all |

  - In a solenoid-type field the odd-crossing miss distance is b ≈ 3.5 µm (keV/Λ)⁴, so ε is effectively switched off at odd crossings for Λ ≲ 20 keV.
  - The even crossings reconnect to within 1/Λ for Λ ≳ 3 keV (upper bound: even-crossing b values not converged; physically b_even ≲ 10⁻³ b_odd, see erratum 2). So ε_eff ≈ 0 for Λ ≲ 2 keV, ε_eff ≈ ε/2 for 3-20 keV, and ε_eff ≈ ε above about 30 keV, for this geometry (ESTIMATE).
  - **In matter** the ionisation torques give J up to ~10¹⁸ ħ [2108.06748 Fig.5], i.e. b = J/p ≫ 1/Λ at all Λ ≲ 0.5 MeV after a single hard collision [0805.4642 Eq.4.2]. This would switch ε off entirely in rock and concrete, but needs T3's treatment of stochastic kicks.
- **Verdict.**
  - For CMS: irrelevant. ε deposits ≲ 0.1 GeV in the tracker even with ε = 0.1 at every crossing (`theory_signal_model.md` §3.3, confirmed).
  - For FASER at Λ ≳ 30 keV: the survival weight uses ε at every crossing over 480 m, much of it in rock (`G-T2-5`). A b-dependent ε(b) ≈ ε₀ θ(1/Λ − b) is the better parametrisation (ESTIMATE). The ±30% variation used by FASER does not cover this structural uncertainty.

## 7. Deliverable code (all in `theory_track/code/`, run with `pixi run python code/<file>`)

| File | Content | Status |
|---|---|---|
| `T2_propagator.py` | `ExactPair` (exact CM yo-yo + exact Lorentz boost, lab positions, closed forms), `li_analytic_lab` (2002.07503 Eq.II.4-8), `LabStraightString` (Kang-Luty EoM, lab-simultaneous ŝ, DOP853 with crossing events, `fext(i,x,p,t)` hook), **`CausalNullString`** (port of the Athena null-vector string; uniform E, B kicks plus generic `fext_kick` hook), `plane_thickness`, `radius_crossings` | **reference for T3: use `CausalNullString` for anything at O(F_ext)** |
| `T2_test_propagator.py` | 33 unit tests: energy conservation (≤ 2×10⁻¹⁶), period, amplitude, centre of energy, lab integrator vs exact (≤ 6×10⁻¹⁰ ℓ_max), Li closed form vs exact (≤ 5×10⁻¹⁴), causal port vs exact (≤ 2×10⁻⁸), closed-form lab separations | 33/33 PASS |
| `T2_kinematics.py` | LO DY + V*+jet toy at 14 TeV (CT18NLO), Table 3.1, figures `T2_lmax_distributions.png`, `T2_nosc_tracker.png`, `T2_isr_assumptions.png`; writes a 170 MB cache to the session scratchpad (env `T2_CACHE`), not to the project | runs in ~30 s |
| `T2_approx_errors.py` | Sec. 2.4 table, `T2_approx_errors.png` (regenerates the cache if missing) | ok |
| `T2_string_methods_B.py` | causal vs straight strings in 3.8 T: thickness, hit displacements, momentum drift; `T2_string_methods_B.png` | ok (~10 min) |
| `T2_covariance_test.py` | Lorentz-covariance test of the methods with external fields (Sec. 5.1) | ok |
| `T2_transverse_linear.py` | independent linearised-NG solution (characteristics) for transverse response; `T2_transverse_check.png` | ok (valid until the first crossing) |
| `T2_crossing_missdist.py` | miss distance at crossings vs 1/Λ in 3.8 T (Sec. 6.3) | ok (~17 min) |

Limitations: uniform fields only; no material (T3); the causal port reproduces the algorithm, not the Athena C++ (G4 geometry, energy loss, stacking). T3 has a copy in `code/T3_propagator.py`; T2 did not edit it.

## 8. Gap entries

### G-T2-1 The instantaneous straight-string approximation is uncontrolled for the plane thickness and hit positions; the exact causal Nambu-Goto string (ATLAS Athena algorithm) should be the reference
- **Current treatment.**
  - Every central-detector trajectory study integrates the Kang-Luty endpoint equation with an instantaneous straight string: Knapen et al. [1708.02243 Sec.II]; Li et al. with CM simultaneity [1911.02223 Eq.III.6-9; 2002.07503 Eq.VIII.1-4]; Sha et al.'s GNN samples through the Knapen-Papucci code [2410.00269 Sec.III].
  - The analytic thickness formula is derived in the same approximation [1911.02223 Eq.III.12; 2002.07503 Eq.V.6].
  - Justification offered: F_ext ≪ σ [0805.4642 Eq.3.10].
- **Why it is a gap.**
  - F_ext ≪ σ guarantees small angles, but the plane thickness and crossing miss distance are themselves O(F_ext/σ), and so is the straight-string error.
  - Demonstrated (ESTIMATE, Sec. 5.1):
    - (i) the straight-string prescriptions are not Lorentz covariant: 140-570 µm frame dependence on a 150-190 µm effect, while the causal string is covariant to 0.05 µm;
    - (ii) they violate energy conservation in a pure B field, by −1.6 MeV per crossing (lab-simultaneous), through the 180° "snap" at each crossing with miss distance b;
    - (iii) different straight prescriptions disagree with each other by ×10-100 in thickness.
  - In vacuum all methods agree exactly, so nobody has noticed.
- **Quantitative effect for CMS Phase-2** (m = 500 GeV, 3.8 T, no material, 4 events per Λ):
  - d_min(straight)/d_min(exact) = 0.04-60 depending on prescription; **[superseded, see erratum]**
  - hit positions at the OT differ by 0.2-35 mm; **[superseded, see erratum]**
  - the exact thickness scales roughly as Λ^−2.5 (2-5 keV), not Λ^−4. **[superseded, see erratum]**
  - The coplanar edge (d ≈ 100 µm near 0.6-0.8 keV) moves little, but every analysis using a trajectory model (χ² fit, GNN training, multi-hit-per-layer patterns, plane-thickness cut efficiency) inherits an O(1) model error from straight-string codes. **[superseded, see erratum]**
- **Exploitation:**
  - (c) use a causal NG propagator (Athena algorithm ported to CMSSW, or `T2_propagator.CausalNullString` for fast scans) as the only signal model;
  - (e) removes an unrecognised O(1) signal-modelling systematic from straight-string-based efficiencies (incl. the Phase-1 strategy's reliance on the thickness formula);
  - (f) a short theory paper: "Quirk trajectories need the causal string", with the covariance test as the key figure.
- **Effort:** days (paper-level demonstration exists here); weeks with material (T3) and a full sample. **Confidence:** medium-high (port validated exactly in vacuum, covariant, momentum-conserving, step-converged; independent linearised check agrees up to the first crossing; not yet cross-checked against the Athena C++ itself).
- **Verdict: EXPLOIT.**

### G-T2-2 Step-count killer in the Athena quirk configuration
- **Current treatment.** `QuirksPreInclude` adds `MonopoleLooperKillerTool` with MaxSteps = 2×10⁶ (BSM_Only) [Athena `G4UserActionsConfig.py`]. The quirk stepper takes ≈ 2y*/maxBoost ≈ 150 G4 steps per crossing for γ* = 1.28.
- **Why it is a gap.** N_cross in a CMS-size tracker is ≈ 24(Λ/keV)², independent of m_Q (Sec. 2.2). Quirks are therefore killed inside the tracker for Λ ≳ 24 keV, and before the calorimeters at lower Λ (ESTIMATE). FASER: γ_pair ~ 5 gives ~10⁵ crossings across ~5 m of detector at Λ = 100 keV, so tracks could be killed mid-detector if Calypso uses the same killer (UNVERIFIED).
- **Effect.** It truncates CMS signal tracks at the high-Λ edge (20-30 keV grid points) if the configuration is ported naively. It may make FASER's 30-100 keV limits conservative.
- **Exploitation:** (e) set MaxSteps ≳ 10⁸ or exempt quirks in the CMS port (`theory_signal_model.md` §3.5 item 5 now quantified); (a) ask FASER whether their 100 keV point was affected.
- **Effort:** days. **Confidence:** medium (CMS), low (FASER).
- **Verdict: WORTH A CHECK.**

### G-T2-3 Exact closed forms replace factor-2-3 shorthands; N_osc is mass independent
- **Current treatment.** "2 cm (γ−1)" [1708.02243 Eq.1] is low by ×1.97; "1 cm (m/100 GeV)" [2404.13814 Eq.2.6; 2607.26195; 2512.20696] is wrong by ×0.4-2.7 per event and ×0.54 for scalars; the non-relativistic period is low by 6-10%; the fixed-p_T ISR trick biases ℓ_max by −10 to −25% and N_osc by +20%. The exact forms are in `theory_signal_model.md` §1.1 and Tab.4.2a and are correct.
- **Why it is a gap.** Minor. The new exact results here are N_osc = σR/(2β* p_T) (mass independent), the lab width and string direction, the string-energy fraction (0.62-0.66), and the statement that Li's lab solution [2002.07503 Eq.II.4-8] is exact in vacuum.
- **Effect.** Correct regime boundaries in fast scans:
  - 44-47% of triggered pairs complete < 1 oscillation inside the tracker at Λ = 0.3 keV;
  - 12(Λ/keV)² oscillations at p_T > 200 GeV.
- **Exploitation:** (c, e) adopt the Sec. 2.2 table in CMS documents and fast scans.
- **Effort:** none (done). **Confidence:** high.
- **Verdict: EXPLOIT (minor, documentation).**

### G-T2-4 Measuring Λ and m_Q from crossing spacing, amplitude and timing
- **Current treatment.** None in the literature (measurement after discovery is not discussed beyond rates).
- **Why it is a gap.** In vacuum the lab crossing spacing D = 2p*(βγ)_pair/σ, ℓ_max = 2(γ*−1)m/σ and the pair velocity (MTD timing) are exact functions of (m, σ, γ*). The ratio D/ℓ_max = γ*β*(βγ)_pair/(γ*−1) is independent of σ. So D, w_T and β_pair (MTD) over-determine (σ, γ*), and the recoil p_T then gives m_Q. Event by event this is exact only up to the O(F_ext) corrections of G-T2-1, hence with a causal model.
- **Effect.** Not quantified here (T4).
- **Exploitation:** (d).
- **Effort:** weeks (T4). **Confidence:** medium.
- **Verdict: WORTH A CHECK (hand to T4).**

### G-T2-5 The ε (glueball per crossing) model ignores the crossing miss distance
- **Current treatment.** Constant ε = 0.1 per crossing [1811.08903 Eq.B.3; 2404.13814 Eq.4.1; 2607.26195 p.3], applied to every crossing over 480 m, including rock.
- **Why it is a gap.**
  - Non-perturbative emission requires b ≲ 1/Λ [1811.08903 App.B.1].
  - In 3.8 T, odd crossings miss by 3.5 µm (keV/Λ)⁴, so ε is off at half the crossings for Λ ≲ 20 keV and at all crossings for Λ ≲ 2 keV (Sec. 6.3).
  - Ionisation torques in rock give J ~ 10¹⁸ ħ [2108.06748 Fig.5], plausibly b ≫ 1/Λ at all Λ.
- **Effect.** Nil for CMS (ε irrelevant in the tracker). For FASER, ε matters only for Λ ≳ 30 keV, where the B-field-only miss distances are already < 1/Λ. The open question is matter-induced J at 30-100 keV.
- **Exploitation:** (a) FASER limits at Λ ≥ 30 keV may be conservative, and the 71 GeV limit at 100 keV [HEPData t2] could rise if the survival weight → 1; (f) an ε(b) parametrisation.
- **Effort:** weeks (needs T3's stochastic-kick propagation). **Confidence:** low.
- **Verdict: WORTH A CHECK (low priority for CMS).**

## 9. Killed ideas (with the killing number)
- **The lab-frame simultaneity problem in vacuum.** It does not exist: the world sheet is a flat 2-plane, the lab string is straight with a fixed direction, and all four methods agree to ≤ 2×10⁻⁸ ℓ_max. The Li "approximate analytic solution" is exact in vacuum.
- **Fixed-ŝ approximation.** Exact in vacuum; wrong as soon as F_ext ≠ 0 (no transverse restoring force; mm effects [2002.07503 Fig.6]). Not a vacuum issue.
- **Rotating component from DY spin/partial waves.** J ≤ 2.45ħ gives J/(p*ℓ_max) ≈ 3×10⁻¹⁷ and impact parameter 10⁻³ fm.
- **Relativistic yo-yo regime at the LHC.** γ* ≤ 2.0 (E) and ≤ 2.5 (Ẽ, 200 GeV) at the 84% quantile, so the massless-yo-yo formula is ×3-6 off and never applicable.
- **Capture into quirkonium or annihilation at a crossing (CMS).** J ≥ 10⁶ ħ from the first crossing in 3.8 T (b ≥ 3×10⁻⁴ Å ≫ 1/m_Q ≈ 4×10⁻⁴ fm). Coulomb is in the Born regime (η ≈ 0.05).
- **Quantum spreading of the endpoints.** ≈ 0.5 nm over the tracker. Quantum numbers n ≈ 2×10¹⁶; level spacing 4 µeV (Λ/keV)².
- **Larmor radiation.** 1.5×10⁻⁸ eV (Λ/keV)⁴ per crossing, ≲ 300 eV over the tracker at 30 keV.
- **Quantum string roughening.** Width ≈ 5 Å.
- **Perturbative glueball radiation from the string acceleration.** ~α_IC Λ³/m_Q² per crossing (~10⁻²⁰ Λ).
- **ε inside the CMS tracker.** ≲ 0.1 GeV (confirms `theory_signal_model.md` §3.3).

## 10. Open questions for other workstreams
- **T3 (B + matter).**
  - Use `CausalNullString` (or the Athena algorithm) as the reference. Straight-string results for thickness or torques are not trustworthy at O(F_ext) (G-T2-1).
  - Add ionisation and multiple-scattering kicks through the `fext_kick` hook.
  - Re-derive the thickness scaling (Λ^−2.5 vs Λ^−4) on a full DY sample.
  - Quantify J and the crossing miss distance in silicon and in rock (G-T2-5).
- **T4 (trajectory model / measurement).** The fit model must be causal. Explore the (D, w_T, β_pair) → (σ, m_Q) measurement (G-T2-4). The 44-47% of pairs with < 1 oscillation at Λ = 0.3 keV need an arc-pair model rather than a plane.
- **T5.** Check whether any paper (Knapen-Papucci code, Sha et al., LHCb VELO toy) used a non-instantaneous string; I found none.
- **T6.** Photon-fusion pairs (J = 0, 2) and W-mediated mixed pairs: same vacuum kinematics. Unequal masses are supported by `ExactPair` (ℓ_max = (M − m₁ − m₂)/σ).
- **Experimental Phase 2 / CMSSW port.**
  - (i) Raise or exempt the step-count killer (G-T2-2).
  - (ii) Validate the port with the covariance test of `T2_covariance_test.py`, plus vacuum tests against `ExactPair`.
  - (iii) Check G4 `delta_intersection` with `DistChord() = 0`.
  - (iv) Generate with a matched V+jets ME, not a fixed p_T kick (Sec. 3).
  - (v) Ask FASER whether its configuration includes the looper killer.

## 11. References opened
- 0805.4642 Kang, Luty: Sec.3.2-3.4 (Eq.3.4-3.12: action, endpoint EoM, straight-string condition, glueball suppression), Sec.4.1 (Eq.4.2, no annihilation).
- 1708.02243 Knapen et al.: Eq.1-4 (d_cm shorthand vs exact), Sec.II, Fig.2 (L ~ 10¹² ħ), Eq.8-9.
- 1911.02223 Li, Li, Pei, Zhang: Sec.III Eq.III.1-III.10 (EoM, simultaneity), Eq.III.12.
- 2002.07503 Li, Li, Pei, Zhang: Sec.II Eq.II.1-II.21 (analytic solution, shown exact in vacuum), Sec.III-V (L, n_T, thickness), Sec.VIII Eq.VIII.1-4 and Fig.6, App.C.
- 1811.08903 Evans, Luty: App.B.1 (ε, impact-parameter condition, Eq.B.1-B.7), Tab.1.
- 2404.13814 Feng et al.: Sec.4 (Eq.4.1-4.9, ε = 0.1 "not calculable").
- 2108.06748 Li, Pei, Ran, Zhang: Sec.4.1 (angular momentum from ionisation, Fig.5).
- 2607.26195 FASER: p.3 (Athena Quirks used, ε survival weights), p.5 (systematics).
- 2410.00269 Sha et al.: trajectory code provenance (via `theory_signal_model.md`; not re-read).
- ATLAS Athena `Simulation/G4Extensions/Quirks` (main, gitlab.cern.ch/atlas/athena, downloaded 2026-10-07): `InfracolorForce.{h,cxx}`, `StringVector.h`, `HyperbolaStep.{h,cxx}`, `HyperbolaStepper.{h,cxx}`, `QuirkTransportation.cxx`, `QuirkWatcher.cxx`, `QuirkStackingAction.cxx`, `python/QuirksConfig.py`; `Simulation/G4Utilities/G4UserActions/python/G4UserActionsConfig.py` and `src/LooperKiller.cxx` (MaxSteps).
- `research/theory_signal_model.md` §0-§7 and App. A (inputs, CT18NLO method); CT18NLO lhagrid1 (lhapdfsets.web.cern.ch, copy from the earlier session scratchpad).
- Not opened: lattice glueball masses (values recalled, UNVERIFIED); Artru/Bars piecewise-linear string literature (cited from memory as background only).
