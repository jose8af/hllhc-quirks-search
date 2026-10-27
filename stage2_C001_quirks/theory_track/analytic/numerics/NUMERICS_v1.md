# NUMERICS — crossing-resolved measurements of the near-miss transverse impulse (Stage 1, E2)

Status: FINAL (2026-10-10). Written blind to E1 (no E1 file was opened before this note was final).
All numbers are classical Nambu-Goto (NG) with massive point endpoints, **truth level**, B only (no material).
Tags: **VERIFIED** = causal kernel and conformal solver agree within the quoted tolerance; **ESTIMATE** = one solver.

## 0. Summary (≤ 15 lines)
1. **Vacuum near miss (M2a, exact b):** the axis turns towards b̂ by ψ = Â(b/ℓ_max) ln(L/b), log-exact over 4.5 decades;
   Â = 0.996/0.951/0.88/0.79 and L/ℓ_max = 0.985/0.90/0.56/0.43 at γ* = 1.05/1.3/2/3 (VERIFIED at γ* ≤ 1.3); non-relativistically L = ℓ_max, K → 0.
2. The string impulse accrues as (σb/v)[κ ln(2vτ/b) + κ₀], κ = 0.963/0.840/0.653/0.52 (heuristic κ = 1). The turning-point-to-turning-point
   transfer has no log, (1.92/1.61/1.15/0.79) σb/v, so the log lives in the axis direction. A straight string has the same form with Â 0.93/0.67/0.33/0.17.
3. **Field-driven (M2b, M1):** b_odd = c_b ε⊥ℓ_max, c_b = 1.33/1.30/1.24/1.19, b ∥ E*_⊥ (|cos| = 1.0000); b_even ≲ 10⁻³ b_odd.
   ψ_odd = [M2a law at b_odd] − (1.3-1.6) ε⊥; ψ_even = +(1.6-1.7) ε⊥ (no log); per pair ψ_pair/ε⊥ = a ln(1/ε⊥) + b with a = 1.14-1.23.
   In 18 full-event points (60-100 events each) ψ_odd matches the CM law to 1-2 % and b_odd to 0.6-2 %.
4. **Thickness (M3, truth, B only):** local Λ exponents −1.53…−2.16 (±0.07-0.18, mean ≈ −1.80), m_Q-independent; B exponent 0.911 ± 0.003.
   Response per unit B = 1 + c ln(B₀/B): c = 0.105 ± 0.002 (500 GeV, 1 keV), 0.101 (1 TeV), 0.093 (3 keV), constant for k = 2-80;
   exactly linear before the first crossing (10⁻⁴). The per-pair law alone predicts c ≈ 0.09-0.10 at 1 keV and n ≈ −1.8.
5. **M5:** a converged Li straight string has the same response (Δs: 1.142/1.306/1.447 vs causal 1.155/1.320/1.467 at B/4, B/20, B/80),
   so B ln(1/B) does not need curvature or retardation. Precision floor of both solvers: b/ℓ₀ ≈ 3×10⁻⁸; T2's b_even values were step artefacts.

## 1. Methods

### 1.1 Codes (all in `analytic/numerics/`; nothing in `code/` edited)
| file | what | validation |
|---|---|---|
| `nm_kernel.py` | line-by-line copy of `T3_causal.causal_propagate` (Athena-type causal null-vector string), B only, + uniform E field, + static-straight-string initial data, + selective record of steps (X⁴, P⁴, absorbed null vector s⁴, cumulative string impulse J⁴) | hits **bit-identical** to `T3_causal.run_causal(material=False)` (9/9 events, 0.6-3 keV) |
| `nm_conformal.py` | copy of `R1_conformal_ng.solve` (conformal-gauge delay ODE, RK4) + E field, offset initial data, same record | hits **identical** (0.0 cm) to `R1_conformal_ng.run` |
| `nm_crossings.py` | per-crossing analysis (below) | vacuum: b ≤ 10⁻¹² cm, tilts 0 |
| `nm_li.py` | scalarised copy of `R1_li_literal.li_run` (literal Li Euler integrator), 10× faster | same hits as the original within 0.30 µm at 10⁻³ of the printed step (difference ∝ step: round-off amplified by the Euler step error at near-miss crossings) |
| `nm_stats.py` | bootstrap / JSON helpers | — |
| `M1_events.py`, `M2_single.py`, `M3_thickness.py`, `M5_li_blinearity.py`, `M*_analysis.py` | campaigns and analyses | — |

### 1.2 Per-crossing analysis (`nm_crossings.py`)
- **Frame.** For a neutral pair in uniform B the canonical momentum P_can = p₁ + p₂ + P_string − q(x₁ − x₂)×B is conserved; at a
  crossing x₁ ≈ x₂ and the string is collapsed, so p₁ + p₂ = P₀ at **every** crossing. All crossings of an event are analysed in
  the single rest frame of P₀ ("CM frame"), so axes at different crossings are directly comparable.
- **Exact positions inside a causal step.** Absorbing the fraction λ of the incoming null vector s moves the endpoint to
  x(λ) = x + 2λ(s·p)(p + Fλs)/(m² + 2Fλ s·p) (exact composition property of the Athena map; covariant, applied in the CM frame).
  Conformal solver: cubic Hermite in τ. The closest approach is found by Newton iteration on d/dt*|x₁*(t*) − x₂*(t*)|² at equal
  CM time.
- **Per crossing k** (k = 1 first return; odd/even parity): miss distance b_k (component ⊥ axis), its components on
  ê_N = unit(n̂₀ × β̂_pair) (normal of the lab pair plane) and ê_P, |cos(b, E*_⊥)| with E* = γβ×B (CM electric field),
  γ*, CM speed v, separation amplitude ℓ_k (max equal-time separation in the preceding half period), the **apsidal (axis)
  rotation** ψ_k = change of the turning-point axis across the crossing (out-of-plane component ψ_N and component along b̂),
  the turning-point-to-turning-point change of the relative transverse momentum Π = (p₁* − p₂*)/2 (total, string part
  J, Lorentz part), and the **impulse profile** ΔΠ(τ) = Π(t_k + τ) − Π(t_k − τ) on 30 log-spaced τ ∈ [10⁻⁵, 0.45] T_h
  (T_h = 2p*/σ, CM time between crossings).
- **Profile fit.** y(τ) = −ΔJ_b v/(σb) = κ ln(2vτ/b) + κ₀ on 5b/(2v) ≤ τ ≤ 3×10⁻³ T_h. A straight string with constant offset b
  gives y = asinh(2vτ/b), i.e. κ = 1, κ₀ = ln 2.
- Notation: ε = q|E⊥|/σ (dimensionless field; in the tracker ε⊥ = q|E*_⊥|/σ), ℓ₀ = m/σ, ℓ_max = 2(γ*−1)ℓ₀.

### 1.3 Precision floor (new; applies to both solvers)
Both solvers lose precision when b/ℓ falls below ~10⁻⁸: Minkowski products of nearly collinear null vectors at relative
angle ~b/ℓ cancel to O(angle²) ≈ 10⁻¹⁶. Observed floor (M2a, crossing 2 departs from b = J/p*): b/ℓ₀ ≈ 3×10⁻⁸ for γ* ≤ 1.3,
≈ 10⁻⁶ for γ* ≥ 2. The conformal gauge additionally degenerates (lab time stops being monotonic in τ) when a crossing is
exactly head-on (b → 0), e.g. even crossings in a pure CM E field, and for the vacuum offset initial data at γ* ≥ 2; such runs
are flagged invalid and excluded. In the tracker (M1) all odd crossings are far above the floor for Λ ≤ 10 keV
(b_odd/ℓ ≳ 10⁻⁶); even-crossing miss distances at ≥ 5 keV are at or below it (they carry negligible impulse).
Classical NG is scale free (only b/ℓ₀ and γ* enter), so "b below 1/Λ" is not a classical threshold: b = 1/Λ corresponds to
b/ℓ₀ = 2×10⁻⁹ (Λ/keV)(500 GeV/m), i.e. inside the floor at 1 keV, above it for Λ ≳ 15 keV at 500 GeV. The law below is
verified down to b/ℓ₀ = 3×10⁻⁸ with no sign of a change of slope.

## 2. M2 — controlled single crossings in the pair CM frame (`M2_single.py`, `M2_analysis.py`, `results/M2.json`)

### 2.1 M2a: vacuum angular-momentum yo-yo (b controlled exactly)
Setup: x₁,₂ = ±(d/2)ê, p₁,₂ = ±p* n̂ (n̂ ⊥ ê), static straight string of length d; d/ℓ₀ = 10⁻¹⁰…10⁻² (0.5 decade), γ* = 1.05,
1.3, 2, 3; m = 500 GeV, Λ = 1 keV; first 3 crossings. In vacuum the causal kernel is exact for this initial data (segment
splitting composes exactly), so max_boost 10⁻² and 10⁻³ must agree, and they do.
- **b = J/p* = d at every crossing**: b/d = 1 ± 3×10⁻⁶ (b/ℓ₀ ≤ 10⁻⁴), ± 6×10⁻⁵ at 10⁻³ (VERIFIED).
- **Axis rotation per crossing** (towards b̂), fitted on floor ≤ b/ℓ₀ ≤ 10⁻³, crossings 1-2:
  ψ_b = Â (b/ℓ_max) ln(L/b)  ⇔  ψ_b/(b/ℓ₀) = A ln(ℓ₀/b) + K, with Â = A ℓ_max/ℓ₀, L = ℓ₀ e^{K/A}.

| γ* | v | A | K | **Â** | **L/ℓ_max** | rms | solvers (Â) | straight string Â (L/ℓ_max) |
|---|---|---|---|---|---|---|---|---|
| 1.05 | 0.305 | 9.962 ± 0.010 | −23.09 ± 0.12 | **0.996** | **0.985** | 0.14 | causal 10⁻²: 0.9962, 10⁻³: 0.9979; conf 256: 0.9951, 2048: 0.9932 — VERIFIED | 0.934 (0.99) |
| 1.3 | 0.639 | 1.584 ± 0.005 | −0.98 ± 0.06 | **0.951** | **0.90** | 0.06 | 0.9505 / 0.9538 / 0.963 / 0.9567 — VERIFIED (±0.6 %) | 0.670 (0.80) |
| 2 | 0.866 | 0.439 ± 0.005 | +0.05 ± 0.06 | **0.878** | **0.56** | 0.03 | causal 10⁻²/10⁻³: 0.878 / 0.871; conformal invalid — ESTIMATE (causal exact in vacuum) | 0.332 (0.17) |
| 3 | 0.943 | 0.198 ± 0.004 | +0.11 ± 0.05 | **0.793** | **0.43** | 0.03 | 0.793 / 0.786 — ESTIMATE | 0.167 (0.002) |

  The log law is exact within the fit residuals over 4.5 decades (γ* ≤ 1.3; quadratic term ≤ 10⁻² of the slope). In the
  non-relativistic limit Â → 1 and L → ℓ_max; relativistically both fall. **Scale invariance**: Λ = 3 keV/m = 1 TeV and
  Λ = 0.6 keV/m = 200 GeV at the same (γ*, b/ℓ₀) reproduce ψ_b/(b/ℓ₀) to 0 (b/ℓ₀ = 10⁻³, 10⁻⁵; the 10⁻⁸ point is at the floor).
- **The exact NG crossing is not the straight-string crossing.** The CM-frame straight string (Kang-Luty force, T2
  `LabStraightString`; in the CM frame with P = 0 this is the Li CM-simultaneous prescription) has the same log form but a
  smaller coefficient: Â_SS/Â_NG = 0.94, 0.70, 0.38, 0.21 at γ* = 1.05, 1.3, 2, 3 (ESTIMATE, one straight-string code;
  DOP853 rtol 10⁻¹²).
- **Where the impulse accrues (profile).** ΔJ_b(τ) grows as −(σb/v)[κ ln(2vτ/b) + κ₀] from τ ~ b/v up to τ ~ 0.05 T_h, then
  turns over (the string pulls back during the rest of the half period):

| γ* | κ (median over b) | κ₀ | TP-to-TP impulse ΔΠ_b/(σb/v) (no log: A_tp consistent with 0) |
|---|---|---|---|
| 1.05 | 0.963 ± 0.002 | 0.657 | 1.92 ± 0.01 |
| 1.3 | 0.840 ± 0.013 | 0.44-0.45 | 1.61 ± 0.02 |
| 2 | 0.653 ± 0.006 | 0.09-0.14 | 1.15 ± 0.06-0.12 |
| 3 | 0.52 ± 0.03 | −0.01…−0.08 | 0.79 ± 0.09 |

  (κ, κ₀ VERIFIED at γ* ≤ 1.3: conformal κ = 0.963 / 0.841.) Straight-string heuristic: κ = 1, κ₀ = ln 2 = 0.69 — matched only
  as γ* → 1. **The turning-point-to-turning-point transverse momentum change has no logarithm**: the log lives in the
  *direction* of the axis (ψ), not in the net momentum transfer.

### 2.2 M2b: field-driven crossings (constant transverse E in the CM frame, pair produced at a point)
ε = qE/σ = 10⁻⁹…10⁻³ (0.5 decade), γ* = 1.05, 1.3, 2, 3, E ⊥ n̂ (and 60°, 30° at γ* = 1.3); 6 crossings. Fits use
ε⊥ ≥ 3×10⁻⁷ (below this the even crossings, which are exactly head-on in a pure E field, hit the precision floor).
- **b_even → 0**: in a pure CM E field the even-crossing miss distance is a splitting artefact ∝ max_boost (2.0×10⁻⁴ → 2.0×10⁻⁵
  εℓ₀ for 10⁻³ → 10⁻⁴ at γ* = 1.3). Physically b_even = 0 here.
- **b_odd ∝ ε⊥**, only the component of E ⊥ n̂ matters (θ_E = 90°, 60°, 30° give b_odd/(ε⊥ℓ₀) = 0.7790, 0.7791, 0.7793):

| γ* | b_odd/(ε⊥ℓ₀) | b_odd/(ε⊥ℓ_max) | ψ_odd/ε⊥ = A_o ln(1/ε⊥) + K_o | ψ_even/ε⊥ | ψ_odd − [M2a law at b_odd] | pair sum − [M2a law] |
|---|---|---|---|---|---|---|
| 1.05 | 0.1328 | 1.328 | 1.318 ln + (−1.91) | 1.606 | −1.561 ± 0.02 | +0.04 |
| 1.3 | 0.7790 | 1.298 | 1.241 ln + (−2.01) | 1.611 | −1.482 ± 0.01 | +0.13 |
| 2 | 2.480 | 1.240 | 1.0875 ln + (−2.22) | 1.646 | −1.367 ± 0.005 | +0.28 |
| 3 | 4.755 | 1.189 | 0.954 ln + (−2.40) | 1.696 | −1.327 ± 0.03 | +0.37 |

  (causal max_boost 10⁻³; conformal N = 256/1024 agree: b_odd to 0.03 %, A_o to 0.3 %, K_o to 0.01, ψ_even to 0.02 —
  VERIFIED for b_odd, A_o, K_o, ψ_even at all four γ*; max_boost 10⁻² changes ψ_even by +0.04…+0.1, i.e. ψ_even needs 10⁻³.)
- **The vacuum near-miss law predicts the field-driven log exactly**: A_o = (b_odd/ε⊥ℓ₀)·A = 1.323, 1.234, 1.089, 0.943
  vs measured 1.318, 1.241, 1.088, 0.954. The field adds a **non-logarithmic, alternating** rotation: −1.33…−1.56 ε⊥ at odd and
  +1.61…1.70 ε⊥ at even crossings (independent of ε to ±0.03 over 3.5 decades), which nearly cancels over a crossing pair
  (net +0.04…+0.37 ε⊥).
- **Per crossing pair** (what accumulates in the tracker): Δψ_pair/ε⊥ = c_b Â ln(L/(c_b ε⊥ ℓ_max)) + δ, with c_b = b_odd/(ε⊥ℓ_max)
  and δ = pair residual above.

## 3. M1 — per-crossing diagnostics in full events (`M1_events.py`, `M1_analysis.py`, `results/M1.json`)
Setup: B = 3.8112 T uniform, no material, T2 LO DY+ISR cache (p_T(QQ̄) > 200 GeV, |η| < 1), the same events at every Λ for a
given m. Production: causal max_boost 10⁻², hmax 0.2 cm, 100 events (Λ ≤ 3 keV; and 200 GeV/10 keV) or 60 events (5, 10 keV).
Convergence: 20 events at 10⁻³ / 0.02 cm. Solver check: conformal N = 256 and 1024 on 6 events (500 GeV, 0.6-3 keV).
Only crossings with r_lab < 108.3 cm are used. Errors are event-block bootstrap. ψ is projected on E*_⊥, which makes an angle
with the lab-plane normal (median |ê_N·Ê*_⊥| = 0.92-0.97); the pure out-of-plane component ψ_N is also in the JSON.
Predictions use the M2 fits interpolated in ln(γ*−1) at each event's γ*; median γ* = 1.27 / 1.19 / 1.14 at 200 / 500 / 1000 GeV.

| m | Λ | ev | crossings | b_odd [Å] | b_odd/(ε⊥ℓ_k) | b_odd/M2b | ψ_odd/ε⊥ | M2b law | ψ_even/ε⊥ (fine) | κ | M2a κ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 200 | 0.6 | 100 | 968 | 1.96×10⁵ | 1.304 ± 0.004 | 1.006 | 8.13 ± 0.10 | 8.12 | 1.608 ± 0.016 | 0.854 | 0.848 |
| 200 | 1 | 100 | 2781 | 2.55×10⁴ | 1.305 ± 0.004 | 1.007 | 9.40 ± 0.12 | 9.38 | 1.613 ± 0.012 | 0.852 | 0.848 |
| 200 | 2 | 100 | 11271 | 1598 | 1.308 ± 0.004 | 1.008 | 11.09 ± 0.15 | 11.10 | 1.62 ± 0.03 | 0.853 | 0.848 |
| 200 | 3 | 100 | 25429 | 316 | 1.310 ± 0.006 | 1.009 | 12.16 ± 0.19 | 12.11 | 1.62 ± 0.03 | 0.854 | 0.848 |
| 200 | 5 | 60 | 41442 | 34.8 | 1.316 ± 0.011 | 1.016 | 13.39 ± 0.30 | 13.41 | 1.61 ± 0.03 | 0.846 | 0.845 |
| 200 | 10 | 100 | 283088 | 2.56 | 1.30 ± 0.02 | 1.02 | 15.5 ± 0.4 | 15.1 | 1.79 ± 0.07 | 0.796 | 0.848 |
| 500 | 0.6 | 100 | 1049 | 1.57×10⁵ | 1.314 ± 0.003 | 1.007 | 9.33 ± 0.17 | 9.31 | 1.61 ± 0.04 | 0.885 | 0.870 |
| 500 | 1 | 100 | 3014 | 2.05×10⁴ | 1.315 ± 0.003 | 1.007 | 10.62 ± 0.19 | 10.58 | 1.61 ± 0.04 | 0.886 | 0.870 |
| 500 | 2 | 100 | 12196 | 1273 | 1.318 ± 0.004 | 1.009 | 12.38 ± 0.22 | 12.32 | 1.63 ± 0.02 | 0.887 | 0.870 |
| 500 | 3 | 100 | 27498 | 255 | 1.320 ± 0.006 | 1.012 | 13.47 ± 0.25 | 13.34 | 1.59 ± 0.02 | 0.887 | 0.870 |
| 500 | 5 | 60 | 48838 | 31.3 | 1.31 ± 0.01 | 1.011 | 14.3 ± 0.6 | 14.8 | 1.62 ± 0.03 | 0.872 | 0.870 |
| 500 | 10 | 60 | 195435 | 2.19 | 1.40 ± 0.05 | 1.09 | 14.6 ± 5.4 | 16.6 | 3.0 ± 0.5 | 0.77 | 0.870 |
| 1000 | 0.6 | 100 | 922 | 1.38×10⁵ | 1.323 ± 0.003 | 1.008 | 10.11 ± 0.16 | 10.00 | 1.59 ± 0.01 | 0.910 | 0.893 |
| 1000 | 1 | 100 | 2643 | 1.79×10⁴ | 1.323 ± 0.004 | 1.008 | 11.41 ± 0.16 | 11.28 | 1.59 ± 0.01 | 0.913 | 0.893 |
| 1000 | 2 | 100 | 10713 | 1123 | 1.329 ± 0.005 | 1.012 | 13.22 ± 0.17 | 13.06 | 1.60 ± 0.01 | 0.914 | 0.893 |
| 1000 | 3 | 100 | 24160 | 225 | 1.336 ± 0.006 | 1.017 | 14.45 ± 0.18 | 14.13 | 1.60 ± 0.01 | 0.915 | 0.893 |
| 1000 | 5 | 60 | 40401 | 31.0 | 1.32 ± 0.01 | 1.011 | 16.0 ± 0.3 | 15.5 | 1.63 ± 0.03 | 0.906 | 0.881 |
| 1000 | 10 | 60 | 161675 | 2.12 | 1.32 ± 0.05 | 1.02 | 17.2 ± 0.9 | 17.2 | 1.9 ± 0.5 | 0.79 | 0.881 |

(b_odd errors are about 15 % from the event-to-event kinematic spread, e.g. 2.05 ± 0.30 ×10⁴ Å; the normalised columns are
precise. The M2b "law" column is CM-frame, 6 crossings, E only.)
- **b_odd = (1.30-1.34) ε⊥ ℓ_k**, the static polarisation by E*_⊥, aligned with E*_⊥ to |cos| = 1.00000 (0.99996 at 10 keV).
  It scales as Λ⁻⁴ (b_odd ∝ ε⊥ℓ ∝ Λ⁻⁴): 2.05×10⁴ → 255 Å from 1 → 3 keV (ratio 80.4; 81 expected). VERIFIED (conformal/causal
  per crossing: 3-6×10⁻⁴).
- **ψ_odd/ε⊥ follows the CM-frame M2b law to 1-2 %** at all masses for Λ ≤ 5 keV. The residual ψ_odd − law is
  +0.09…+0.23 (±0.02-0.07), small but statistically significant; it may come from the CM magnetic field B* or from the
  interpolation in γ* (not resolved). VERIFIED (conformal/causal dA per crossing: 0.3-0.5 %).
- **ψ_even/ε⊥ = 1.59-1.63** (fine settings) = M2b 1.61: even crossings carry no logarithm. Production settings overestimate it
  by 2-17 %, growing with Λ, because the even crossings are step-sensitive.
- **κ (log slope of the impulse profile at odd crossings) = 0.85-0.91**, 1 % above the M2a vacuum value (κ − κ_M2a = +0.008…+0.012
  ± 0.002). At 10 keV it drops to 0.77-0.80, near the precision floor. VERIFIED (conformal/causal 0.1-0.4 %).
- **b_even** grows roughly linearly with the crossing index. Per crossing pair, 1 keV / 500 GeV: about 9 Å (causal fine,
  20 events) vs about 20 Å (conformal, 6 events); per crossing, the conformal and causal values differ by 16-66 %. b_even is
  ≈ 10⁻³ b_odd at 1 keV and less at higher Λ; at ≥ 3 keV it is at the precision floor. Unlike in the pure CM E field (M2b),
  b_even ≠ 0 here, probably through B* and the slow drift of the internal frame (ESTIMATE). Even crossings contribute no
  measurable near-miss impulse (ψ_even has no log term).
- **10 keV**: odd-crossing quantities are converged only to 4-10 % (median), with large tails; ψ_even and κ are near the floor.
  These rows are indicative only.

## 4. M3 — thickness scans with uncertainties (`M3_thickness.py`, `M3_analysis.py`, `results/M3.json`, `results/M3_stdout.txt`)
Setup: truth level, B only, plane through the PV, all hits on the 10 barrel layers (T3 definition). Same 120 events at every Λ
per mass (seed 777 + m). One event at 1 TeV is excluded: it ends in the inherited status-4 queue deadlock at Λ ≥ 2 keV, with
no hits (also present in T3_causal). Production settings; 20-event fine subset. **Stage 3 will redo M3 on MadGraph samples.**

### 4.1 Λ scan: median Δs_B [µm] ± bootstrap (p16-p84), local exponent n = d ln median/d ln Λ to the next point ± bootstrap
| Λ [keV] | 200 GeV | n | 500 GeV | n | 1000 GeV | n |
|---|---|---|---|---|---|---|
| 0.45 | 134 ± 9 (49-222) | −1.72 ± 0.17 | 132 ± 9 (58-218) | −2.01 ± 0.18 | 139 ± 11 (59-222) | −2.16 ± 0.17 |
| 0.6 | 81.7 ± 6.5 (28-135) | −2.05 ± 0.12 | 73.9 ± 6.6 (30-130) | −1.83 ± 0.10 | 74.4 ± 6.4 (33-135) | −1.72 ± 0.10 |
| 1 | 28.7 ± 2.6 (10-53) | −1.67 ± 0.08 | 29.1 ± 2.1 (11-49) | −1.83 ± 0.07 | 31.0 ± 2.2 (13-51) | −1.94 ± 0.07 |
| 2 | 9.0 ± 0.7 (2.9-15.5) | −1.95 ± 0.14 | 8.17 ± 0.72 (3.3-14) | −1.88 ± 0.11 | 8.08 ± 0.72 (3.4-13.4) | −1.64 ± 0.13 |
| 3 | 4.09 ± 0.38 (1.4-7.2) | −1.86 ± 0.18 | 3.80 ± 0.29 (1.8-6.8) | −1.76 ± 0.09 | 4.16 ± 0.31 (1.7-6.4) | −1.85 ± 0.09 |
| 5 | 1.58 ± 0.20 (0.53-2.8) | −1.53 ± 0.13 | 1.55 ± 0.11 (0.62-2.7) | −1.74 ± 0.14 | 1.61 ± 0.11 (0.68-2.6) | −1.75 ± 0.08 |
| 10 | 0.55 ± 0.04 (0.20-0.84) | — | 0.46 ± 0.06 (0.18-0.85) | — | 0.48 ± 0.03 (0.18-0.83) | — |

Medians of the per-event exponents: −1.68 … −1.96. A pure power law is not excluded; the median-based local exponents scatter by
about ±0.15 point to point, and their mean over 0.6-5 keV is −1.81 (200 GeV), −1.81 (500 GeV), −1.78 (1000 GeV). Δs_B is
m_Q-independent within errors at every Λ (cf. T3: 32-38 µm at 1 keV on different events). Q68 values are in the JSON.

**Split by the number of crossings inside the tracker** (terciles of N_cross at fixed Λ, 500 GeV): Δs falls with N, e.g.
42.7 / 29.8 / 21.7 µm for N ≈ 16 / 28 / 49 at 1 keV and 5.1 / 3.7 / 3.2 µm for N ≈ 146 / 256 / 440 at 3 keV. This is a
kinematic correlation, not a dose-response: at fixed Λ, N ∝ σR/(β*p_T), so large N means slow internal motion or low p_T. The
200 GeV and 1 TeV splits are flatter.

### 4.2 B scan (Λ = 1, 3 keV; 500 GeV and 1 TeV; 120 events; f = B/B₀)
| point | Δs(f) median [µm]: 1/80, 1/20, 1/4, 1/2, 1, 2 | local exponents (f-intervals) | global (1/80-2) | R_ev = Δs(f)/(fΔs(1)): 1/2, 1/4, 1/20, 1/80 | c_k = (R−1)/ln k: k = 2, 4, 20, 80 |
|---|---|---|---|---|---|
| 500, 1 keV | 0.536, 1.93, 8.34, 15.65, 29.05, 55.0 | 0.93, 0.91, 0.91, 0.89, 0.92 (±0.01-0.02) | **0.911 ± 0.003** | 1.073, 1.147, 1.320, 1.460 (±0.001-0.005) | **0.105, 0.106, 0.107, 0.105** |
| 1000, 1 keV | 0.563, 2.04, 8.80, 16.6, 30.7, 57.0 | 0.93, 0.91, 0.91, 0.90, 0.89 | **0.912 ± 0.003** | 1.070, 1.141, 1.302, 1.443 | **0.101, 0.102, 0.101, 0.101** |
| 500, 3 keV | (0.083), 0.248, 1.10, 1.99, 3.80, 7.18 | (0.79), 0.92, 0.86, 0.93, 0.92 | 0.885 ± 0.010 | 1.066, 1.130, 1.278, (1.61) | **0.095, 0.094, 0.093**, (0.14) |
| 1000, 3 keV | (0.088), 0.274, 1.12, 2.22, 4.16, 7.72 | (0.82), 0.88, 0.98, 0.91, 0.89 | 0.887 ± 0.010 | 1.066, 1.129, 1.272, (1.69) | **0.095, 0.093, 0.091**, (0.16) |

Values in parentheses are at the precision floor (b_odd/ℓ₀ ≈ 5×10⁻⁸ at B/80 and 3 keV), as is f = 10⁻³ at both Λ (1 keV:
R_ev = 2.00 ± 0.04, c = 0.145; 3 keV: meaningless). Their convergence tails are large (p95 |Δ| = 0.4-0.56 at 3 keV, f = 1/80).
- **Response per unit B = 1 + c ln(B₀/B), with c constant within ±2 % from k = 2 to k = 80** (1 keV): c = 0.105 ± 0.002
  (500 GeV), 0.101 ± 0.001 (1 TeV); at 3 keV c = 0.093 ± 0.002. Fine settings (20 events): 0.104-0.108 / 0.097-0.101 / 0.085-0.098.
  The measured c decreases with Λ, roughly as 1/ln(1/ε⊥) (§5.2).
- **Hits before the first crossing respond exactly linearly**: R_hit = 1.0000 at every f; the non-linearity metric
  Q68|d(B) − k d(B/k)|/Q68|d(B)| = 1×10⁻⁴ (pre) vs 0.15 / 0.36-0.39 / 0.71-0.82 (post, k = 4 / 20 / 80, 1 keV).
- **Hits after the first crossing**, out-of-plane response per unit B, 500 GeV / 1 keV: 1.076, 1.139, 1.319, 1.458 at
  f = 1/2, 1/4, 1/20, 1/80 (1 TeV: 1.077, 1.147, 1.308, 1.452). This equals the event-level R_ev.

## 5. M4 — convergence, solver independence, floors (`results/M4.json`, `M4_conformal_thickness.py`)
### 5.1 Convergence (settings ×10: max_boost 10⁻² → 10⁻³ together with hmax 0.2 → 0.02 cm; conformal N 256 → 1024/2048/4096)
| quantity | median / p95 relative change | comment |
|---|---|---|
| M1 b_odd, ψ_odd (Λ ≤ 3 keV) | 0.3-1.2 % / 1-14 % | converged |
| M1 b_odd, ψ_odd (5, 10 keV) | 1.2-21 % / 15-300 % | 10 keV indicative only |
| M1 κ (≤ 5 keV) | 0.06-1 % | converged |
| M1 even crossings: ψ_even / b_even | 2.5-20 % / 60-400 % | ψ_even needs 10⁻³; b_even ∝ step (causal), floor-limited |
| M2a (vacuum, causal) | Â changes 0.2-0.9 % between 10⁻² and 10⁻³ | difference = different fit sets (every 2nd d at 10⁻³); exact algorithm |
| M2b b_odd, A_o, K_o | ≤ 0.3 %, ≤ 0.5 %, ≤ 0.01 | ψ_even changes +0.04…+0.1 at 10⁻² |
| M3 Δs (≤ 3 keV) | 0.7-2 % / 2-13 % | converged; Λ ≥ 5 keV: 4 % / 17-57 % |
| M3 R_ev (1 keV, k ≤ 80) | prod vs fine on the same events: ≤ 0.012 | converged |
| M5 Li Δs response | 10⁻³ vs 3×10⁻⁴ step: ≤ 0.003 | hit-level k = 80 still moves 2.5 % |
| conformal vs causal (M1 per crossing, ≤ 3 keV) | b_odd 3-6×10⁻⁴; dA_odd 0.3-0.5 %; κ 0.1-0.4 % | VERIFIED |
| conformal vs causal Δs (M3 events, 12 ev × 1, 2 keV × B₀{1, 1/4, 1/20}) | median ratio 0.999 (outliers ≤ 1.17 from different hit counts) | VERIFIED |
| conformal vs causal R_ev | 1 keV: 1.152/1.329 (causal) vs 1.143/1.331 (N = 1024), 1.144/1.326 (4096); 2 keV: 1.126/1.295 vs 1.135/1.310 | VERIFIED (±0.01) |

### 5.2 Floors
- Vacuum (B = 0) thickness: median 0-0.001 µm (≤ 2 % of Δs at B₀/1000, 1 keV). Vacuum miss distance ≤ 10⁻¹² cm. The vacuum M2a
  run is exact up to round-off.
- Precision floor of both solvers: b/ℓ₀ ≈ 3×10⁻⁸ (γ* ≤ 1.3), 10⁻⁶ (γ* ≥ 2) (§1.3). It sets the reach of the B scan (k ≤ 80 at 1 keV,
  k ≤ 20 at 3 keV) and makes even-crossing b at ≥ 3 keV unmeasurable.
- Conformal-gauge breakdown (lab time runs backwards) for exactly head-on crossings: such runs abort (status 7) and are excluded.
  Invalid: in M2a, all runs at γ* ≥ 2 and those with b/ℓ₀ < 3×10⁻⁸; in M1, 4 of 36 conformal runs.

### 5.3 Consistency of the measured per-crossing law with the measured thickness response (`M13_bridge.py`, `results/M13_bridge.json`)
This is bookkeeping of measured quantities only, under the assumption Δs ∝ ℓ · N_pairs · ε⊥ ψ_pair. With ψ_pair measured in the
tracker (fine settings) and fitted as a ln(1/ε⊥) + b over Λ = 0.6-5 keV: a = 1.23 ± 0.07 (200 GeV), 1.14 ± 0.22 (500 GeV),
1.22 ± 0.11 (1 TeV). This predicts:
- c = a/ψ_pair: 0.092 ± 0.017 (500 GeV) and 0.096 ± 0.009 (1 TeV) at 1 keV, vs measured 0.106 and 0.101; 0.077-0.079 at 3 keV
  vs 0.093-0.094 (1-2σ low).
- B exponent 1 − c ≈ 0.90 (measured 0.911).
- Λ exponent −2 + 2c = −1.77 … −1.85 (measured −1.64 … −2.16; mean about −1.81).
The accumulated axis rotation accounts for most of the B ln(1/B) response, with a 10-20 % remainder at 3 keV (ESTIMATE).

## 6. M5 — does a converged straight string show the B ln(1/B) non-linearity? (`M5_li_blinearity.py`, `results/M5.json`)
Coordinator request (novelty audit). Literal Li CM-simultaneous straight string (`R1_li_literal` equations via `nm_li.py`),
R1 event recipe (m = 500 GeV, γ* = 1.28, p_T = 300 GeV), Λ = 1 keV, B = 3.8 T × {1, 1/4, 1/20, 1/80} and B = 0, 30 events at
10⁻³ of the printed step bound, the first 6 also at 3×10⁻⁴; causal kernel (max_boost 10⁻³, hmax 0.02 cm) on the same events.
d = hit(B) − hit(0) of the same integrator and step (step-dependent in-plane phase errors cancel to first order).

| integrator (events) | pre-crossing k\|d(B/k)\|/\|d(B)\| | R_post k=4 | k=20 | k=80 | Δs(B/k)k/Δs(B): k=4 | k=20 | k=80 |
|---|---|---|---|---|---|---|---|
| Li 10⁻³ (30) | 1.0000 (metric 1×10⁻⁴) | 1.150 ± 0.001 | 1.352 ± 0.009 | 1.84 ± 0.10 (not converged) | 1.144 ± 0.003 | 1.313 ± 0.005 | 1.461 ± 0.009 |
| causal (30) | 1.0000 (1×10⁻⁴) | 1.1443 ± 0.0004 | 1.312 ± 0.001 | 1.457 ± 0.001 | 1.145 ± 0.002 | 1.313 ± 0.003 | 1.459 ± 0.003 |
| Li 10⁻³ (first 6) | 1.0000 | 1.149 ± 0.002 | 1.329 ± 0.011 | 1.54 ± 0.03 | 1.142 ± 0.004 | 1.306 ± 0.008 | 1.450 ± 0.014 |
| Li 3×10⁻⁴ (first 6) | 1.0000 | 1.146 ± 0.002 | 1.319 ± 0.004 | 1.50 ± 0.02 | 1.142 ± 0.004 | 1.306 ± 0.008 | 1.447 ± 0.013 |
| causal (first 6) | 1.0000 | 1.146 ± 0.001 | 1.313 ± 0.002 | 1.459 ± 0.003 | 1.155 ± 0.016 | 1.320 ± 0.016 | 1.467 ± 0.008 |

**Answer: yes.** The step-converged straight string has the same non-linearity as the exact NG string: exactly linear before the
first crossing, and an event-level thickness response per unit B of 1.142 / 1.306 / 1.447 vs 1.155 / 1.320 / 1.467 (causal, same
events) at B/4, B/20, B/80 — equal within 1-2 % (the Li Δs response is converged between 10⁻³ and 3×10⁻⁴; the hit-level
k = 80 response still moves by 2.5 % between the two steps, because b_odd ∝ B/80 needs finer steps). The B ln(1/B) structure
therefore does **not** require string curvature or retardation; it is a property of the near-miss crossing itself, which a
straight string also has (M2a: same log form, smaller coefficient Â_SS < Â_NG). What curvature/retardation change is the
coefficient (the absolute thickness; cf. the γ*-dependent Li deficit of S-1), not the existence of the logarithm. Why the
relative response agrees so well although Â_SS/Â_NG = 0.70 at γ* = 1.3 is an open point: the response per unit B depends on
the ratio of the non-log to the log term (§2.2), not on Â alone (ESTIMATE, one straight-string implementation).

## 7. What is solver-independent (VERIFIED: causal kernel = conformal solver)
b = J/p* in vacuum; Â, L, κ, κ₀ and the TP impulse at γ* = 1.05 and 1.3; b_odd, A_o, K_o, ψ_even at γ* = 1.05-3 in a CM E field;
b_odd, ψ_odd and κ per crossing in full events (500 GeV, 0.6-3 keV); Δs and its response per unit B (1-2 keV); the exactly linear
pre-crossing response. **ESTIMATE (one solver):** Â, L, κ at γ* = 2, 3 (causal only, but exact in vacuum); straight-string
coefficients (one implementation); b_even in full events (the two solvers differ by 16-66 %); all M3 Λ exponents beyond 2 keV
and the 1 TeV/200 GeV B scans (causal only; the causal-vs-conformal agreement was shown at 500 GeV, 1-2 keV); M5 (different model).

## 8. Surprises
1. **The logarithm is in the axis direction, not in the momentum.** The near-crossing string impulse grows as κ ln τ, but the
   turning-point-to-turning-point momentum transfer is ≈ 1.6 σb/v (γ* = 1.3) with no log. The apsidal rotation keeps
   the log.
2. **L = ℓ_max (and K ≈ 0) in the non-relativistic limit**; relativistically L/ℓ_max falls to 0.43 at γ* = 3.
3. **A field-driven crossing = vacuum near-miss law + an alternating non-log field term** (−1.3…−1.6 ε at odd, +1.6…+1.7 ε at
   even crossings); per pair the non-log remainder is small (+0.04…+0.37 ε).
4. **Even-crossing miss distances in the literature (T2 §5.3/6.3: 16-31 Å at 1 keV, 0.13-0.19 Å at 3 keV) are splitting
   artefacts** of the causal kernel (∝ max_boost). Converged values are ~10⁻³ b_odd, growing with the crossing index; in a pure CM
   E field b_even = 0. The ε-per-crossing statement "even crossings reconnect within 1/Λ from 3 keV" is therefore an upper
   bound (if anything, stronger).
5. **Double-precision floor at b/ℓ ≈ 10⁻⁸ in both solvers**, from Minkowski cancellations. At B ≲ B₀/80 (3 keV) and B₀/1000
   (1 keV) earlier "response per unit B" numbers (S_Bscan R(10⁻⁴), R(10⁻³)) are floor-affected.
6. **The straight string reproduces the relative B non-linearity (M5)** although its per-crossing log coefficient is 30 % smaller
   at γ* = 1.3.
7. Production settings (max_boost 10⁻²) are fine for odd crossings and Δs, but bias ψ_even by up to 17 % at 3-5 keV.

## 9. Open issues
- The small positive residual ψ_odd − (CM-frame law) = +0.1…+0.2 ε⊥ in full events (B* or γ* interpolation?) and the 10-20 %
  part of c not accounted for by ψ_pair at 3 keV (other contributions to Δs: odd offsets b_odd themselves, in-plane terms).
- γ* ≥ 2 vacuum results rest on the causal kernel only (exact in vacuum, but the conformal solver fails for this initial data).
- 10 keV: odd quantities converged only to 4-10 %; need max_boost ≤ 10⁻³ in production at ≥ 5 keV.
- b_even in full events is solver-dependent at the 20-60 % level and floor-limited above 2 keV. Quad precision would be needed.
- All event samples are the T2 LO cache (Stage 3: MadGraph). No material (MS dominates Δs above ~1.5 keV, T3).
- The status-4 queue deadlock (1 event in 840 Λ-scan runs at 1 TeV) is inherited from T3_causal and not fixed here.

## 10. Files and CPU
Scripts: `nm_kernel.py`, `nm_conformal.py`, `nm_crossings.py`, `nm_li.py`, `nm_stats.py`, `M1_events.py`, `M1_analysis.py`,
`M2_single.py`, `M2_analysis.py`, `M3_thickness.py`, `M3_analysis.py`, `M4_conformal_thickness.py`, `M4_summary.py`,
`M5_li_blinearity.py`, `M13_bridge.py`. Results: `results/M1.json`, `M2.json`, `M3.json` (+ `M3_stdout.txt`), `M4.json`,
`M4_conformal_thickness.json`, `M5.json`, `M13_bridge.json`. Raw: `results/raw/M2` (6 MB), `results/raw/M5` (0.5 MB),
`data/stage1_numerics/M1` (323 MB), `data/stage1_numerics/M3` (30 MB). CPU: M1 1.0×10⁴ s, M3 3.2×10³ s, M5 1.2×10³ s, M2 0.1×10³ s,
M4 conformal 0.4×10³ s, analyses/tests ≈ 1×10³ s: about 4.5 CPU-h of completed jobs. About 2 further CPU-h were lost to hung
conformal jobs before the status-7 guard was added. About 2.5 h wall on 7 workers.

## 11. Follow-up (post-unblinding) — FU1-FU3 (`FU_runs.py`, `FU_analysis.py`, `results/FU.json`, `results/FU_stdout.txt`)
Written after reading E1's NEAR_MISS_IMPULSE.md §4, §5.3, §9 and predictions.json. The blind numbers above are unchanged;
the follow-up values are added next to them. Raw: `data/stage1_numerics/FU/` (708 jobs, 3.8×10³ s CPU).

### FU1 — c at 3 keV (E1: 0.085 / 0.082; blind production: 0.093 / 0.091-0.095)
**(a) Same events, per-event comparison.** E1's closed form c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)] is evaluated for each M3 event
(median c_E1 = 0.0839 at 500 GeV and 0.0815 at 1 TeV on my events) and compared with the measured per-event
c_k = (R(1/k) − 1)/ln k. Paired median differences (measured − E1) ± bootstrap:

| sample | k = 2 (B₀/2) | k = 4 (B₀/4) | k = 20 (B₀/20) |
|---|---|---|---|
| 1 keV, 500 GeV, production (120) | +0.0001 ± 0.0008 | +0.0010 ± 0.0004 | +0.0015 ± 0.0005 |
| 1 keV, 1 TeV, production (119) | +0.0003 ± 0.0005 | +0.0007 ± 0.0004 | +0.0001 ± 0.0003 |
| 3 keV, 500 GeV, production (120) | +0.0076 ± 0.0030 | +0.0072 ± 0.0025 | +0.0058 ± 0.0023 |
| 3 keV, 500 GeV, production, γ* < 1.5 (95) | +0.0094 ± 0.0035 | +0.0090 ± 0.0023 | +0.0041 ± 0.0026 |
| **3 keV, 500 GeV, max_boost 10⁻³ (119)** | **+0.0021 ± 0.0015** | **+0.0055 ± 0.0020** | **+0.0113 ± 0.0018** |
| 3 keV, 500 GeV, 10⁻³, γ* < 1.2 (50) | +0.0004 ± 0.0019 | +0.0020 ± 0.0016 | +0.0056 ± 0.0013 |
| 3 keV, 1 TeV, production (119) | +0.0095 ± 0.0035 | +0.0087 ± 0.0017 | +0.0074 ± 0.0031 |
| **3 keV, 1 TeV, max_boost 10⁻³ (120)** | **−0.0003 ± 0.0006** | **+0.0043 ± 0.0017** | **+0.0132 ± 0.0033** |
| 3 keV, 1 TeV, 10⁻³, γ* < 1.2 (64) | −0.0005 ± 0.0005 | +0.0011 ± 0.0004 | +0.0056 ± 0.0016 |
| 3 keV, max_boost 10⁻⁴ (only 8/9 valid events) | −0.003 ± 0.004 / +0.001 ± 0.002 | −0.001 ± 0.003 / +0.001 ± 0.001 | +0.004 ± 0.003 / +0.006 ± 0.006 |

- Population values (from the median R), max_boost 10⁻³, 120 events: c = 0.0890 / 0.0918 / 0.0961 (500 GeV) and 0.0841 / 0.0881 / 0.0956
  (1 TeV) at k = 2 / 4 / 20. Production gave 0.0945 / 0.0939 / 0.0928 and 0.0949 / 0.0930 / 0.0909. **The blind production c at 3 keV is
  step-biased** (by +0.006…+0.011 at k = 2). At 1 keV, production and fine agree (blind §4.2).
- max_boost 10⁻⁴: 45 % of runs overflow the string queue (status 5, 65 536 segments) and are excluded. On the 8-9 surviving events,
  fine − vfine = 0.0000 ± 0.001 at all k, so max_boost 10⁻³ is converged for c.
- **γ*:** the gap is not confined to γ* ≳ 2. It persists with γ* < 1.5, and the γ* ≥ 1.5 bins are noisy rather than biased. Restricting
  to γ* < 1.2 halves the k = 20 excess.

**(b) Precision.** Higher precision is not feasible here. numba has no float128, and np.longdouble is float64 on Apple arm64.
An mpmath port of the kernel costs ~10³-10⁴ s per event per B value at 3 keV (10⁶-10⁷ steps). Compensated (Kahan) summation of the
positions would not address the floor: the accumulated position error, ~√N·10⁻¹⁶·ℓ, is far below b. The floor arises in the
step map itself. Instead I measured the floor noise directly:
- **Round-off replicas** (30 events, initial momenta perturbed by 10⁻¹⁴, 5 replicas, production settings):
  - At 3 keV, Δs varies event by event by 0.15 / 0.26 / 0.47 / 0.89 % (median; p90 1.3 / 0.8 / 1.3 / 4.8 %) at f = 1, 1/2, 1/4, 1/20. Per-event c
    varies by 0.006 / 0.004 / 0.005 (median; p90 0.03 / 0.014 / 0.023).
  - **At 1 keV the same test gives ≤ 3.5×10⁻⁴ in Δs and 3×10⁻⁵ in c.**
  - So 3 keV events amplify a 10⁻¹⁴ perturbation to the 10⁻³-10⁻² level over ~250 crossings, and the amplification is largest at weak B.
    A positive-definite thickness with such noise is biased upward at small f, which fits the k-dependent excess.
- **Independent arithmetic (conformal, N = 4096, 3 keV):** the thickness at B₀ agrees with causal (median ratio 0.997), but the weak-B runs
  are invalid or garbage (c < 0). No independent check is possible at 3 keV below B₀ with this solver.

**(c) B ratios clearly above the floor.** At B₀/2, b_odd/ℓ₀ ≈ 10⁻⁶ ≫ 3×10⁻⁸. With converged steps the gap closes there:
+0.0021 ± 0.0015 (500 GeV), −0.0003 ± 0.0006 (1 TeV).

**Verdict FU1.** With step-converged runs the 3 keV gap **closes at B₀/2**, **shrinks to +0.004…+0.005 (2-3σ) at B₀/4**, and **persists
(+0.011…+0.013) at B₀/20**. At B₀/20 b_odd/ℓ₀ ≈ 10⁻⁷ and the measured round-off amplification is largest; the excess halves for γ* < 1.2.
The blind 4-5σ production gap had two numerical sources: a step bias at small k (production max_boost 10⁻² is not converged for c at
3 keV, although it is for Δs to 1-2 %) and floor or chaotic noise at large k. E1's c(3 keV) is consistent with the converged
measurement where the measurement is clean (k = 2). The blind M3 3 keV c values (0.093-0.094) should be read as superseded by
0.084-0.089 (k = 2, max_boost 10⁻³).

### FU2 — vacuum constant K_vac (E1: K_vac(NR) = 3 ln 2 − 2 = 0.0794, i.e. L/ℓ_max → 8/e² = 1.083)
The M2a data are refitted with Â fixed to E1's 2(γ* − 1)/(ρ artanh β*): K_vac = ⟨ψ_b/(Â b/ℓ_max) − ln(ℓ_max/b)⟩, crossings 1-2, with new
runs at γ* = 1.01 and 1.02 (4 solver settings). K_vac depends on the b range, because O(b/ℓ_max) corrections enter when b/ℓ_max ≳ 10⁻³
(at γ* = 1.01 my blind cut b/ℓ₀ ≤ 10⁻³ allowed b/ℓ_max up to 0.05). The per-b values are flat below b/ℓ_max ≈ 10⁻⁴.

| γ* | Â (E1) | K_vac, blind cut | K_vac, b/ℓ_max ≤ 10⁻³ | **K_vac, b/ℓ_max ≤ 10⁻⁴** | **L/ℓ_max = e^{K_vac}** | free slope (≤ 10⁻⁴) |
|---|---|---|---|---|---|---|
| 1.01 | 0.9983 | 0.032 ± 0.010 | 0.0696 ± 0.0003 | **0.0709 ± 0.0001** | 1.0735 | 0.9985 |
| 1.02 | 0.9967 | 0.041 ± 0.006 | 0.0614 ± 0.0004 | **0.0627 ± 0.0001** | 1.0647 | 0.9969 |
| 1.05 | 0.9918 | 0.029 ± 0.002 | 0.0363 ± 0.0006 | **0.0382 ± 0.0002** | 1.0389 | 0.9920 |
| 1.3 | 0.9549 | −0.157 ± 0.005 | −0.156 ± 0.006 | −0.158 ± 0.008 | 0.854 | 0.945-0.955 |
| 2 | 0.8768 | −0.560 ± 0.016 | — | −0.560 ± 0.014 | 0.571 | 0.871-0.878 |
| 3 | 0.8023 | −0.965 ± 0.031 | — | −0.965 ± 0.031 (floor-limited range) | 0.381 | 0.786-0.793 |

(Errors are the standard error over b and crossings. The causal 10⁻² / 10⁻³ and conformal 256 / 2048 settings agree to ≤ 0.0002 at
γ* ≤ 1.05, so these values are VERIFIED.) K_vac is linear in (γ* − 1) between 1.01 and 1.05 (slopes −0.82, −0.815). **Extrapolation:
K_vac(γ* → 1) = 0.0791 ± 0.0003, vs E1's 3 ln 2 − 2 = 0.0794: confirmed.** My blind statement "L → ℓ_max, K → 0 non-relativistically"
was a fit artefact: the slope was free, and the large-b points carry O(b/ℓ_max) corrections. It is superseded by L/ℓ_max → 1.082.

### FU3 — the full-event odd-crossing residual (blind: +0.09…+0.23 ε⊥)
Per event: res_odd = median over odd crossings of ψ_odd − (CM-frame M2b law interpolated in γ*); res_pair = ψ_odd + ψ_even − η/ε⊥ with
E1's closed form η/ε⊥ = G[ln(ℓ_max/b_odd) + K(γ*)], which needs no interpolation. Medians ± bootstrap over events (all production events):

| grouping | res_odd [ε⊥] | res_pair vs E1 [ε⊥] |
|---|---|---|
| all (1338 / 1294 events) | +0.065 ± 0.010 | +0.033 ± 0.014 (+0.3 %) |
| m = 200 / 500 / 1000 GeV | +0.055 / +0.021 / +0.115 | −0.03 / +0.03 / +0.10 |
| Λ = 0.6 / 1 / 2 / 3 / 5 keV | +0.06 / +0.06 / +0.07 / +0.07 / +0.12 (±0.01-0.07) | +0.03 / +0.02 / +0.03 / +0.06 / +0.17 (±0.02-0.12) |
| **γ* 1.0-1.1 / 1.1-1.2 / 1.2-1.35 / 1.35-1.6 / > 1.6** | **+0.29 / +0.24 / +0.05 / −0.35 / −1.04** (±0.01-0.08) | **+0.53 / +0.26 / +0.08 / −0.50 / −1.11** |
| same γ* bins, first 20 events, max_boost 10⁻³ | +0.12 / +0.16 / −0.01 / −0.36 / −0.98 | +0.03 / +0.04 / −0.05 / −0.59 / −1.16 |

**Classification: physics, not numerics.**
- It is independent of the step size: production and 10⁻³ show the same γ* pattern within errors at γ* ≥ 1.2.
- It is independent of Λ within errors, and its m dependence follows the γ* mix of the samples.
- It is strongly γ*-dependent: +2-4 % of ψ_pair at γ* < 1.2, −4 % and −7 % at γ* = 1.35-1.6 and > 1.6.
- The small positive blind average is a cancellation over the γ* distribution.
- The residual relative to E1's closed form (no interpolation) has the same pattern, so it is not an interpolation artefact. A lab
  event differs from the CM E-only problem by the CM magnetic field B* and by E*∥ at second order. The likely origin is B* acting on
  the oscillating ends, whose effect grows with β* (ESTIMATE; not isolated here). At γ* < 1.2 and with converged steps the per-pair
  residual vs E1 is ≤ 0.04 ε⊥ (≤ 0.3 %). Its effect on c (non-log, enters the denominator) is ≲ 1-2 % with sign depending on the γ* mix.
