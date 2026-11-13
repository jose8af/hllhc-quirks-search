# NUMERICS — crossing-resolved measurements of the near-miss transverse impulse (Stage 1, E2)

Status: v2 (fix pass 1, 2026-10-10; v1 kept as `NUMERICS_v1.md`). §0-§10 were written blind to the derivation (no E1 file opened),
which is not the same as solver-independent: see the provenance table in §1.4. §11 (follow-up) and §12 (fix pass) are post-unblinding.
Statements superseded later are flagged in place with **[superseded → §…]**.
All numbers are classical Nambu-Goto (NG) with massive point endpoints, **truth level**, B only (no material).
Tags: **VERIFIED** = causal kernel and conformal solver agree within the quoted tolerance; **ESTIMATE** = one solver.

## 0. Summary (≤ 15 lines)
1. **Vacuum near miss (M2a, exact b):** the axis turns towards b̂ by ψ = Â(b/ℓ_max)[ln(ℓ_max/b) + K_vac] (≡ Â(b/ℓ_max) ln(L/b), L ≡ ℓ_max e^{K_vac}), log-exact over 4.5 decades;
   Â = 0.996/0.951/0.88/0.79 and L/ℓ_max = 0.985/0.90/0.56/0.43 at γ* = 1.05/1.3/2/3 (VERIFIED at γ* ≤ 1.3); ~~non-relativistically L = ℓ_max, K → 0~~ **[superseded → §11 FU2: K_vac → 0.0791 ± 0.0003 = 3 ln 2 − 2, L/ℓ_max → 1.082]**.
2. The string impulse accrues as (σb/v)[κ ln(2vτ/b) + κ₀], κ = 0.963/0.840/0.653/0.52 (heuristic κ = 1). The turning-point-to-turning-point
   transfer has no log, (1.92/1.61/1.15/0.79) σb/v, so the log lives in the axis direction. A straight string has the same form with Â 0.93/0.67/0.33/0.17.
3. **Field-driven (M2b, M1):** b_odd = c_b ε⊥ℓ_max, c_b = 1.33/1.30/1.24/1.19, b ∥ E*_⊥ (|cos| = 1.0000); b_even ≲ 10⁻³ b_odd.
   ψ_odd = [M2a law at b_odd] − (1.3-1.6) ε⊥; ψ_even = +(1.6-1.7) ε⊥ (no log); per pair η/ε⊥ = ψ_pair = G_eff ln(1/ε⊥) + C_η with G_eff = 1.14-1.23 (in the tracker).
   In 18 full-event points (60-100 events each) ψ_odd matches the CM law to 1-2 % and b_odd to 0.6-2 %.
4. **Thickness (M3, truth, B only):** local Λ exponents −1.53…−2.16 (±0.07-0.18, mean ≈ −1.80), m_Q-independent; B exponent 0.911 ± 0.003.
   Response per unit B = 1 + c ln(B₀/B): c = 0.105 ± 0.002 (500 GeV, 1 keV), 0.101 (1 TeV), ~~0.093 (3 keV)~~ **[superseded → §11 FU1 and §13: 3 keV production c is step-biased; converged c(B₀/2) = 0.084-0.089 agrees with E1; the excess at B₀/4, B₀/20 has a physical, cumulative B* part and a per-period part of floor-like scaling (§13)]**, constant for k_f = 2-80 at 1 keV within ±2 % (but +1.5 % at B₀/20, 3σ, §12);
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
- **Per crossing j** (j = 1 first return; odd/even parity): miss distance b_j (component ⊥ axis), its components on
  ê_N = unit(n̂₀ × β̂_pair) (normal of the lab pair plane) and ê_P, |cos(b, E*_⊥)| with E* = γβ×B (CM electric field),
  γ*, CM speed v, separation amplitude ℓ_j (max equal-time separation in the preceding half period), the **apsidal (axis)
  rotation** ψ_j = change of the turning-point axis across the crossing (out-of-plane component ψ_N and component along b̂),
  the turning-point-to-turning-point change of the relative transverse momentum p_rel,⊥ = (p₁* − p₂*)⊥/2 (total; string part ΔΠ_s,
  stored as `J` in the records; Lorentz part), and the **impulse profile** Δp_rel,⊥(τ) = p_rel,⊥(t_j + τ) − p_rel,⊥(t_j − τ) on 30 log-spaced τ ∈ [10⁻⁵, 0.45] T_h
  (T_h = 2p*/σ, CM time between crossings).
- **Profile fit.** y(τ) = −ΔΠ_s,b v/(σb) (string impulse along b̂) = κ ln(2vτ/b) + κ₀ on 5b/(2v) ≤ τ ≤ 3×10⁻³ T_h. A straight string with constant offset b
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

### 1.4 Provenance: which numbers rest on two independent solvers (added in fix pass 1, constructive B5)
"Blind" in §0-§10 means **blind to E1's derivation**, not solver-independent. The production solver `nm_kernel` is a line-by-line copy
of T3_causal (Athena-type piecewise-null map, the same algorithm family as T2's CausalNullString that E1 used for K). The independent
second solver is the conformal-gauge delay ODE of R1 (`nm_conformal`, different formulation, discretisation and arithmetic). The
Li integrator (`nm_li`) is a different model (straight string), not a second solver for NG.

| quantity | causal (T3 copy) | conformal (R1) | other | status |
|---|---|---|---|---|
| M2a b = J/p*, Â, L/ℓ_max, κ, κ₀, TP impulse, γ* ≤ 1.3 | yes | yes (≤ 0.6 %) | — | two solvers |
| M2a at γ* = 2, 3 | yes (exact in vacuum) | invalid (gauge breakdown) | — | one solver |
| FU2 K_vac (γ* = 1.01-1.05) | yes | yes (≤ 0.0002) | E1 analytic 3 ln 2 − 2 | two solvers + analytic |
| M2b b_odd, G (JSON key `A_odd`), K_o, ψ_even, γ* = 1.05-3 | yes | yes (N = 256/1024) | E1 closed forms | two solvers |
| M1 per crossing b_odd, ψ_odd, κ (500 GeV, 0.6-3 keV) | yes | yes (6 events) | — | two solvers |
| M1 other masses, 5-10 keV; b_even | yes | — / solver-dependent (16-66 %) | — | one solver |
| M3 Δs and R(f) (500 GeV, 1-2 keV, 12 events) | yes | yes (ratio 0.999; R ±0.01) | — | two solvers |
| M3 Λ exponents, 200 GeV / 1 TeV, 3-10 keV; B scans at 3 keV | yes | — (conformal fails at weak B, 3 keV) | — | one solver |
| FU1 / §12 3 keV c(f) | yes (1e-2, 1e-3, 1e-4) | no valid run | E1 c_ev | one solver |
| M5 response, §12 Li ratio at γ* = 2 | yes | — | Li (different model) | model comparison |
The strongest missing third check is the Athena C++ itself (out of scope here).
Tag systems (R2-C8): in this note VERIFIED means two independent solvers agree; E1's VERIFIED-NUM allows a single solver. An E1
VERIFIED-NUM item that rests on one solver corresponds to ESTIMATE / "one solver" here (the rows of the table above).

### 1.5 Notation map to E1 (constructive B9; aligned to E1's binding table, NEAR_MISS_IMPULSE.md §1.1; text renamed accordingly, JSON keys unchanged)
| this note | E1 (NEAR_MISS_IMPULSE.md) | meaning / remark |
|---|---|---|
| j (crossing index; written k in M1/M2 tables and JSON key `k`) | j | renamed in text |
| f = B/B₀, k_f = 1/f; c(k_f) ≡ (R(1/k_f) − 1)/ln k_f | f, k_f, R(f) | renamed in text (JSON keys still `c_k`, `k4`, `R_ev_f…`) |
| L/ℓ_max = e^{K_vac} (tables of §2.1, §11 FU2) | K_vac | text now uses K_vac; E1's L_η ≡ ln(ℓ_max/b_odd) is a different object |
| ψ_j (per crossing, units of ε⊥); ψ_pair = ψ_odd + ψ_even | ψ_j; η/ε⊥ | same (per period) |
| G (M2b, JSON `A_odd`); G_eff, C_η (bridge, JSON `fit_a`, `fit_b`) | G(γ*) | renamed in text; G_eff is the in-tracker (γ*-mixed) value |
| K_o, b (bridge constant), K_vac | K (field, per period), K_vac | K = K_vac + δ_pair/G (E1 §9.1) |
| p_rel,⊥ (formerly Π) | p_rel,⊥ | renamed in text |
| ΔΠ_s (string impulse; record columns `J⁴`, code variable `J`) | ΔΠ_s (E1's J = angular momentum) | renamed in text |
| ε⊥ = q\|E*⊥\|/σ (ε in some JSON keys) | ε⊥ | the glueball-emission probability of T2/S-19 is ε_gb |
| c_b = b_odd/(ε⊥ℓ_max) | [γ* − asinh ρ/ρ]/(γ* − 1) | same, closed form E1 §3.2 |
| v (CM speed of one end) | β* | E1 also uses v = 2β* (NR relative speed) in §3.3 |
| k_B^tot = \|B*\|/\|E*⊥\| (JSON `by_kB`); k_B = \|B*⊥\|/\|E*⊥\| (JSON `by_kB_perp`) | k_B = \|B*⊥\|/\|E*⊥\| | §12.1 gives both |

## 2. M2 — controlled single crossings in the pair CM frame (`M2_single.py`, `M2_analysis.py`, `results/M2.json`)

### 2.1 M2a: vacuum angular-momentum yo-yo (b controlled exactly)
Setup: x₁,₂ = ±(d/2)ê, p₁,₂ = ±p* n̂ (n̂ ⊥ ê), static straight string of length d; d/ℓ₀ = 10⁻¹⁰…10⁻² (0.5 decade), γ* = 1.05,
1.3, 2, 3; m = 500 GeV, Λ = 1 keV; first 3 crossings. In vacuum the causal kernel is exact for this initial data (segment
splitting composes exactly), so max_boost 10⁻² and 10⁻³ must agree, and they do.
- **b = J/p* = d at every crossing**: b/d = 1 ± 3×10⁻⁶ (b/ℓ₀ ≤ 10⁻⁴), ± 6×10⁻⁵ at 10⁻³ (VERIFIED).
- **Axis rotation per crossing** (towards b̂), fitted on floor ≤ b/ℓ₀ ≤ 10⁻³, crossings 1-2:
  ψ_b = Â (b/ℓ_max)[ln(ℓ_max/b) + K_vac], K_vac ≡ ln(L/ℓ_max)  ⇔  ψ_b/(b/ℓ₀) = A ln(ℓ₀/b) + K, with Â = A ℓ_max/ℓ₀, L = ℓ₀ e^{K/A}.

| γ* | v | A | K | **Â** | **L/ℓ_max** | rms | solvers (Â) | straight string Â (L/ℓ_max) |
|---|---|---|---|---|---|---|---|---|
| 1.05 | 0.305 | 9.962 ± 0.010 | −23.09 ± 0.12 | **0.996** | **0.985** [free-slope fit; superseded → §11 FU2: 1.039 with Â fixed, b/ℓ_max ≤ 10⁻⁴] | 0.14 | causal 10⁻²: 0.9962, 10⁻³: 0.9979; conf 256: 0.9951, 2048: 0.9932 — VERIFIED | 0.934 (0.99) |
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
- **Where the impulse accrues (profile).** ΔΠ_s,b(τ) grows as −(σb/v)[κ ln(2vτ/b) + κ₀] from τ ~ b/v up to τ ~ 0.05 T_h, then
  turns over (the string pulls back during the rest of the half period):

| γ* | κ (median over b) | κ₀ | TP-to-TP impulse Δp_rel,⊥·b̂/(σb/v) (no log: A_tp consistent with 0) |
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

| γ* | b_odd/(ε⊥ℓ₀) | b_odd/(ε⊥ℓ_max) | ψ_odd/ε⊥ = G ln(1/ε⊥) + K_o (G: JSON key `A_odd`) | ψ_even/ε⊥ | ψ_odd − [M2a law at b_odd] | pair sum − [M2a law] |
|---|---|---|---|---|---|---|
| 1.05 | 0.1328 | 1.328 | 1.318 ln + (−1.91) | 1.606 | −1.561 ± 0.02 | +0.04 |
| 1.3 | 0.7790 | 1.298 | 1.241 ln + (−2.01) | 1.611 | −1.482 ± 0.01 | +0.13 |
| 2 | 2.480 | 1.240 | 1.0875 ln + (−2.22) | 1.646 | −1.367 ± 0.005 | +0.28 |
| 3 | 4.755 | 1.189 | 0.954 ln + (−2.40) | 1.696 | −1.327 ± 0.03 | +0.37 |

  (causal max_boost 10⁻³; conformal N = 256/1024 agree: b_odd to 0.03 %, G to 0.3 %, K_o to 0.01, ψ_even to 0.02 —
  VERIFIED for b_odd, G, K_o, ψ_even at all four γ*; max_boost 10⁻² changes ψ_even by +0.04…+0.1, i.e. ψ_even needs 10⁻³.)
- **The vacuum near-miss law predicts the field-driven log exactly**: G = (b_odd/ε⊥ℓ₀)·A = 1.323, 1.234, 1.089, 0.943
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

| m | Λ | ev | crossings | b_odd [Å] | b_odd/(ε⊥ℓ_j) | b_odd/M2b | ψ_odd/ε⊥ | M2b law | ψ_even/ε⊥ (fine) | κ | M2a κ |
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
- **b_odd = (1.30-1.34) ε⊥ ℓ_j**, the static polarisation by E*_⊥, aligned with E*_⊥ to |cos| = 1.00000 (0.99996 at 10 keV).
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
| point | Δs(f) median [µm]: 1/80, 1/20, 1/4, 1/2, 1, 2 | local exponents (f-intervals) | global (1/80-2) | R_ev = Δs(f)/(fΔs(1)): 1/2, 1/4, 1/20, 1/80 | c(k_f) = (R−1)/ln k_f: k_f = 2, 4, 20, 80 |
|---|---|---|---|---|---|
| 500, 1 keV | 0.536, 1.93, 8.34, 15.65, 29.05, 55.0 | 0.93, 0.91, 0.91, 0.89, 0.92 (±0.01-0.02) | **0.911 ± 0.003** | 1.073, 1.147, 1.320, 1.460 (±0.001-0.005) | **0.105, 0.106, 0.107, 0.105** |
| 1000, 1 keV | 0.563, 2.04, 8.80, 16.6, 30.7, 57.0 | 0.93, 0.91, 0.91, 0.90, 0.89 | **0.912 ± 0.003** | 1.070, 1.141, 1.302, 1.443 | **0.101, 0.102, 0.101, 0.101** |
| 500, 3 keV | (0.083), 0.248, 1.10, 1.99, 3.80, 7.18 | (0.79), 0.92, 0.86, 0.93, 0.92 | 0.885 ± 0.010 | 1.066, 1.130, 1.278, (1.61) | **0.095, 0.094, 0.093**, (0.14) [superseded → §11 FU1/§12.1: converged 0.089 / 0.092 / 0.096] |
| 1000, 3 keV | (0.088), 0.274, 1.12, 2.22, 4.16, 7.72 | (0.82), 0.88, 0.98, 0.91, 0.89 | 0.887 ± 0.010 | 1.066, 1.129, 1.272, (1.69) | **0.095, 0.093, 0.091**, (0.16) [superseded → converged 0.084 / 0.088 / 0.096] |

Values in parentheses are at the precision floor (b_odd/ℓ₀ ≈ 5×10⁻⁸ at B/80 and 3 keV), as is f = 10⁻³ at both Λ (1 keV:
R_ev = 2.00 ± 0.04, c = 0.145; 3 keV: meaningless). Their convergence tails are large (p95 |Δ| = 0.4-0.56 at 3 keV, f = 1/80).
- **Response per unit B = 1 + c ln(B₀/B), with c constant within ±2 % from k_f = 2 to k_f = 80** (1 keV): c = 0.105 ± 0.002
  (500 GeV), 0.101 ± 0.001 (1 TeV); at 3 keV c = 0.093 ± 0.002 **[superseded → §11 FU1 (production step bias) and §13 (two-part weak-field excess)]**. At 1 keV a small rise at B₀/20 exists: FU1a gives c(1/20) − c_E1 = +0.0015 ± 0.0005 (500 GeV, 3σ), so "constant within ±2 %" holds but the rise is significant (reviewer C8). Fine settings (20 events): 0.104-0.108 / 0.097-0.101 / 0.085-0.098.
  The measured c decreases with Λ, roughly as 1/ln(1/ε⊥) (§5.2).
- **Hits before the first crossing respond exactly linearly**: R_hit = 1.0000 at every f; the non-linearity metric
  Q68|d(B) − k_f d(B/k_f)|/Q68|d(B)| = 1×10⁻⁴ (pre) vs 0.15 / 0.36-0.39 / 0.71-0.82 (post, k_f = 4 / 20 / 80, 1 keV).
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
| M2b b_odd, G, K_o | ≤ 0.3 %, ≤ 0.5 %, ≤ 0.01 | ψ_even changes +0.04…+0.1 at 10⁻² |
| M3 Δs (≤ 3 keV) | 0.7-2 % / 2-13 % | converged; Λ ≥ 5 keV: 4 % / 17-57 % |
| M3 R_ev (1 keV, k_f ≤ 80) | prod vs fine on the same events: ≤ 0.012 | converged |
| M5 Li Δs response | 10⁻³ vs 3×10⁻⁴ step: ≤ 0.003 | hit-level k_f = 80 still moves 2.5 % |
| conformal vs causal (M1 per crossing, ≤ 3 keV) | b_odd 3-6×10⁻⁴; dA_odd 0.3-0.5 %; κ 0.1-0.4 % | VERIFIED |
| conformal vs causal Δs (M3 events, 12 ev × 1, 2 keV × B₀{1, 1/4, 1/20}) | median ratio 0.999 (outliers ≤ 1.17 from different hit counts) | VERIFIED |
| conformal vs causal R_ev | 1 keV: 1.152/1.329 (causal) vs 1.143/1.331 (N = 1024), 1.144/1.326 (4096); 2 keV: 1.126/1.295 vs 1.135/1.310 | VERIFIED (±0.01) |

### 5.2 Floors
- Vacuum (B = 0) thickness: median 0-0.001 µm (≤ 2 % of Δs at B₀/1000, 1 keV). Vacuum miss distance ≤ 10⁻¹² cm. The vacuum M2a
  run is exact up to round-off.
- Precision floor of both solvers: b/ℓ₀ ≈ 3×10⁻⁸ (γ* ≤ 1.3), 10⁻⁶ (γ* ≥ 2) (§1.3). It sets the reach of the B scan (k_f ≤ 80 at 1 keV,
  k_f ≤ 20 at 3 keV) and makes even-crossing b at ≥ 3 keV unmeasurable.
- Conformal-gauge breakdown (lab time runs backwards) for exactly head-on crossings: such runs abort (status 7) and are excluded.
  Invalid: in M2a, all runs at γ* ≥ 2 and those with b/ℓ₀ < 3×10⁻⁸; in M1, 4 of 36 conformal runs.

### 5.3 Consistency of the measured per-crossing law with the measured thickness response (`M13_bridge.py`, `results/M13_bridge.json`)
This is bookkeeping of measured quantities only, under the assumption Δs ∝ ℓ · N_pairs · ε⊥ ψ_pair. With ψ_pair measured in the
tracker (fine settings) and fitted as G_eff ln(1/ε⊥) + C_η (JSON keys `fit_a`, `fit_b`) over Λ = 0.6-5 keV: G_eff = 1.23 ± 0.07 (200 GeV), 1.14 ± 0.22 (500 GeV),
1.22 ± 0.11 (1 TeV). This predicts:
- c = a/ψ_pair: 0.092 ± 0.017 (500 GeV) and 0.096 ± 0.009 (1 TeV) at 1 keV, vs measured 0.106 and 0.101; 0.077-0.079 at 3 keV
  vs 0.093-0.094 (1-2σ low) [the 3 keV measured values are superseded → §11/§12.1; the converged c(B₀/2) = 0.084-0.089 agrees with the bridge to ≤ 1σ].
- B exponent 1 − c ≈ 0.90 (measured 0.911).
- Λ exponent −2 + 2c = −1.77 … −1.85 (measured −1.64 … −2.16; mean about −1.81).
The accumulated axis rotation accounts for most of the B ln(1/B) response, with a 10-20 % remainder at 3 keV (ESTIMATE).

## 6. M5 — does a converged straight string show the B ln(1/B) non-linearity? (`M5_li_blinearity.py`, `results/M5.json`)
Coordinator request (novelty audit). Literal Li CM-simultaneous straight string (`R1_li_literal` equations via `nm_li.py`),
R1 event recipe (m = 500 GeV, γ* = 1.28, p_T = 300 GeV), Λ = 1 keV, B = 3.8 T × {1, 1/4, 1/20, 1/80} and B = 0, 30 events at
10⁻³ of the printed step bound, the first 6 also at 3×10⁻⁴; causal kernel (max_boost 10⁻³, hmax 0.02 cm) on the same events.
d = hit(B) − hit(0) of the same integrator and step (step-dependent in-plane phase errors cancel to first order).

| integrator (events) | pre-crossing k_f\|d(B/k_f)\|/\|d(B)\| | R_post k_f=4 | k_f=20 | k_f=80 | Δs(B/k_f)k_f/Δs(B): k_f=4 | k_f=20 | k_f=80 |
|---|---|---|---|---|---|---|---|
| Li 10⁻³ (30) | 1.0000 (metric 1×10⁻⁴) | 1.150 ± 0.001 | 1.352 ± 0.009 | 1.84 ± 0.10 (not converged) | 1.144 ± 0.003 | 1.313 ± 0.005 | 1.461 ± 0.009 |
| causal (30) | 1.0000 (1×10⁻⁴) | 1.1443 ± 0.0004 | 1.312 ± 0.001 | 1.457 ± 0.001 | 1.145 ± 0.002 | 1.313 ± 0.003 | 1.459 ± 0.003 |
| Li 10⁻³ (first 6) | 1.0000 | 1.149 ± 0.002 | 1.329 ± 0.011 | 1.54 ± 0.03 | 1.142 ± 0.004 | 1.306 ± 0.008 | 1.450 ± 0.014 |
| Li 3×10⁻⁴ (first 6) | 1.0000 | 1.146 ± 0.002 | 1.319 ± 0.004 | 1.50 ± 0.02 | 1.142 ± 0.004 | 1.306 ± 0.008 | 1.447 ± 0.013 |
| causal (first 6) | 1.0000 | 1.146 ± 0.001 | 1.313 ± 0.002 | 1.459 ± 0.003 | 1.155 ± 0.016 | 1.320 ± 0.016 | 1.467 ± 0.008 |

**Answer: yes.** The step-converged straight string has the same non-linearity as the exact NG string: exactly linear before the
first crossing, and an event-level thickness response per unit B of 1.142 / 1.306 / 1.447 vs 1.155 / 1.320 / 1.467 (causal, same
events) at B/4, B/20, B/80 — equal within 1-2 % (the Li Δs response is converged between 10⁻³ and 3×10⁻⁴; the hit-level
k_f = 80 response still moves by 2.5 % between the two steps, because b_odd ∝ B/80 needs finer steps). The B ln(1/B) structure
therefore does **not** require string curvature or retardation; it is a property of the near-miss crossing itself, which a
straight string also has (M2a: same log form, smaller coefficient Â_SS < Â_NG). What curvature/retardation change is the
coefficient (the absolute thickness; cf. the γ*-dependent Li deficit of S-1), not the existence of the logarithm. Why the
relative response agrees so well although Â_SS/Â_NG = 0.70 at γ* = 1.3 is an open point: the response per unit B depends on
the ratio of the non-log to the log term (§2.2), not on Â alone (ESTIMATE, one straight-string implementation).

## 7. What is solver-independent (VERIFIED: causal kernel = conformal solver)
b = J/p* in vacuum; Â, L, κ, κ₀ and the TP impulse at γ* = 1.05 and 1.3; b_odd, G, K_o, ψ_even at γ* = 1.05-3 in a CM E field;
b_odd, ψ_odd and κ per crossing in full events (500 GeV, 0.6-3 keV); Δs and its response per unit B (1-2 keV); the exactly linear
pre-crossing response. **ESTIMATE (one solver):** Â, L, κ at γ* = 2, 3 (causal only, but exact in vacuum); straight-string
coefficients (one implementation); b_even in full events (the two solvers differ by 16-66 %); all M3 Λ exponents beyond 2 keV
and the 1 TeV/200 GeV B scans (causal only; the causal-vs-conformal agreement was shown at 500 GeV, 1-2 keV); M5 (different model).

## 8. Surprises
1. **The logarithm is in the axis direction, not in the momentum.** The near-crossing string impulse grows as κ ln τ, but the
   turning-point-to-turning-point momentum transfer is ≈ 1.6 σb/v (γ* = 1.3) with no log. The apsidal rotation keeps
   the log.
2. ~~**L = ℓ_max (and K ≈ 0) in the non-relativistic limit**~~ **[superseded → §11 FU2: the blind fit had a free slope and large-b points; K_vac → 0.0791 = 3 ln 2 − 2, L/ℓ_max → 1.082]**; relativistically L/ℓ_max falls to 0.43 at γ* = 3.
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
c(k_f) = (R(1/k_f) − 1)/ln k_f. Paired median differences (measured − E1) ± bootstrap:

| sample | k_f = 2 (B₀/2) | k_f = 4 (B₀/4) | k_f = 20 (B₀/20) |
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
  (1 TeV) at k_f = 2 / 4 / 20. Production gave 0.0945 / 0.0939 / 0.0928 and 0.0949 / 0.0930 / 0.0909. **The blind production c at 3 keV is
  step-biased** (by +0.006…+0.011 at k_f = 2). At 1 keV, production and fine agree (blind §4.2).
- max_boost 10⁻⁴: 45 % of runs overflow the string queue (status 5, 65 536 segments) and are excluded. On the 8-9 surviving events,
  fine − vfine = 0.0000 ± 0.001 at all k_f, so max_boost 10⁻³ is converged for c.
- **γ*:** the gap is not confined to γ* ≳ 2. It persists with γ* < 1.5, and the γ* ≥ 1.5 bins are noisy rather than biased. Restricting
  to γ* < 1.2 halves the k_f = 20 excess.

**(b) Precision.** Higher precision is not feasible here. numba has no float128, and np.longdouble is float64 on Apple arm64.
An mpmath port of the kernel costs ~10³-10⁴ s per event per B value at 3 keV (10⁶-10⁷ steps). Compensated (Kahan) summation of the
positions would not address the floor: the accumulated position error, ~√N·10⁻¹⁶·ℓ, is far below b. The floor arises in the
step map itself. Instead I measured the floor noise directly:
- **Round-off replicas** (30 events, initial momenta perturbed by 10⁻¹⁴, 5 replicas, production settings):
  - At 3 keV, Δs varies event by event by 0.147 / 0.236 / 0.441 / 0.739 % (median; p90 1.14 / 0.75 / 1.31 / 4.81 %) at f = 1, 1/2, 1/4, 1/20. Per-event c
    varies by 0.0060 / 0.0038 / 0.0044 (median; p90 0.0178 / 0.0119 / 0.0226) [values from FU.json `roundoff_L3`; corrected in fix pass 1].
  - **At 1 keV the same test gives ≤ 3.5×10⁻⁴ in Δs and 3×10⁻⁵ in c.**
  - ~~So 3 keV events amplify a 10⁻¹⁴ perturbation to the 10⁻³-10⁻² level~~ [withdrawn wording, reviewer C4: the replicas sample round-off realisations; they are not a deterministic amplification of the perturbation, see §12 A1 replica-size test].
    ~~A positive-definite thickness with such noise is biased upward at small f, which fits the k_f-dependent excess.~~ [withdrawn → §12.1, R2-C1: the bias enters only at second order, ~10⁻⁵ in c]
- **Independent arithmetic (conformal, N = 4096, 3 keV):** the thickness at B₀ agrees with causal (median ratio 0.997), but the weak-B runs
  are invalid or garbage (c < 0). No independent check is possible at 3 keV below B₀ with this solver.

**(c) B ratios clearly above the floor.** At B₀/2, b_odd/ℓ₀ ≈ 10⁻⁶ ≫ 3×10⁻⁸. With converged steps the gap closes there:
+0.0021 ± 0.0015 (500 GeV), −0.0003 ± 0.0006 (1 TeV).

**Verdict FU1 [partly withdrawn → §13 (and §12.1 for the refutation): the round-off attribution of the k_f ≥ 4 excess is refuted (noise enters √λ_min only at second order, bias ~10⁻⁵ in c); its origin is the two-part excess of §13].** With step-converged runs the 3 keV gap **closes at B₀/2**, **shrinks to +0.004…+0.005 (2-3σ) at B₀/4**, and **persists
(+0.011…+0.013) at B₀/20**. ~~At B₀/20 b_odd/ℓ₀ ≈ 10⁻⁷ and the measured round-off amplification is largest~~ [withdrawn; origin → §13: physical B* part + per-period part of floor-like shape]; the excess halves for γ* < 1.2.
The blind 4-5σ production gap had two numerical sources: a step bias at small k_f (production max_boost 10⁻² is not converged for c at
3 keV, although it is for Δs to 1-2 %) and ~~floor or chaotic noise at large k_f~~ [withdrawn → §13: two-part excess]. E1's c(3 keV) is consistent with the converged
measurement where the measurement is clean (k_f = 2). The blind M3 3 keV c values (0.093-0.094) should be read as superseded by
0.084-0.089 (k_f = 2, max_boost 10⁻³).

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

## 12. Fix pass 1 (reviews S1-R1) — `FIX1_runs.py`, `FIX1_analysis.py`, `results/FIX1.json`, `results/FIX1_stdout.txt`
New runs: 1072 jobs, 8.5×10³ s CPU (raw: `data/stage1_numerics/FIX1/`, plus 360 + 30 new M1 files). Earlier numbers are unchanged;
superseded statements are flagged in place.

### 12.1 Critical A1 — the 3 keV excess at B₀/4 and B₀/20
**The round-off attribution of §11 FU1 is withdrawn.** The reviewer is right: mean-zero noise enters Δs = √λ_min only at second
order, so the measured replica noise implies a bias of ~10⁻⁵ in c, against an excess of +0.005 / +0.012. Three new results:

**(b) Finest step on an unbiased sample.** The string-queue cap was raised from 2¹⁶ to 2²¹. At max_boost 10⁻⁴ / hmax 0.005 cm,
39 of 40 events per mass are now valid (previously 8-9 of 20 survived), and these are M3 events 0-39, not a selected subset.

| 3 keV, max_boost 10⁻⁴ (39 events) | c(1/2) − c_E1 | c(1/4) − c_E1 | c(1/20) − c_E1 | fraction > 0 at 1/20 |
|---|---|---|---|---|
| 500 GeV | +0.0017 ± 0.0021 | +0.0035 ± 0.0034 | **+0.0122 ± 0.0027** | 0.90 |
| 1 TeV | +0.0008 ± 0.0015 | +0.0028 ± 0.0033 | **+0.0130 ± 0.0035** | 0.97 |
| 10⁻³ − 10⁻⁴ (paired median) | −0.0002 / −0.0001 | −0.0007 / −0.0001 | −0.0010 / +0.0003 | — |

The per-event spread (500 GeV, 10⁻⁴) is p16-p84 = [−0.018, +0.013], [−0.003, +0.019], [+0.002, +0.063] at f = 1/2, 1/4, 1/20.
**c is step-converged at 10⁻³** (to ≤ 0.001). The B₀/20 excess is deterministic and one-sided (c(1/20) > c(1/2) in 85 % of events).
**Replica test** (reviewer C4; 10 events, max_boost 10⁻³, perturbations 10⁻¹⁴ / 10⁻¹⁰ / 10⁻⁸, 3 replicas each):
- The per-event spread of c does not scale with the perturbation: sd 0.0014 / 0.0015 / 0.0021 at f = 1/2, and ≈ 0.001 at 1/4 and 1/20.
- The mean shift of c is ≤ 5×10⁻⁴ at every size.

So the replicas sample round-off realisations; they do not amplify the perturbation. The excess is not noise.

**(a) It tracks the CM magnetic field.** Per-event c(f) − c_E1 at 3 keV, max_boost 10⁻³ (120 events per mass), in bins of
k_B^tot = |B*|/|E*⊥| (total B*; E1's binding k_B = |B*⊥|/|E*⊥| uses the component ⊥ n̂, JSON `by_kB_perp`, see below):

| k_B^tot bin | 500 GeV: n, Δc(1/2), Δc(1/4), Δc(1/20) | 1 TeV: n, Δc(1/2), Δc(1/4), Δc(1/20) |
|---|---|---|
| < 3 | 20: −0.0002, +0.0015, +0.0011 (±0.0013-0.0015) | 5: −0.0001, +0.0004, +0.0008 |
| 3-5 | 32: +0.0009, +0.0014, +0.0069 (±0.0015-0.0025) | 34: −0.0002, +0.0013, +0.0037 (±0.0006-0.0009) |
| 5-7 | 26: +0.012, +0.011, +0.014 (±0.004) | 18: −0.0017, +0.0016, +0.0090 |
| 7-10 | 27: +0.0004, +0.0145, +0.047 (±0.002-0.017) | 26: −0.0005, +0.0043, +0.0199 |
| > 10 | 13: +0.011, +0.019, +0.096 (±0.007-0.05) | 36: +0.016, +0.021, +0.098 (±0.003-0.017) |
| γ* < 1.3 and k_B^tot < 5 | 36: −0.0010, +0.0008, +0.0026 (±0.0011-0.0014) | 30: −0.0001, +0.0008, +0.0030 (±0.0005-0.0006) |

- Binned in E1's k_B (B*⊥) instead, the trend is the same: Δc(1/20) = +0.004 / +0.011 / +0.019 / +0.031 / +0.116 (500 GeV) and
  +0.005 / +0.005 / +0.014 / +0.036 / +0.135 (1 TeV) for k_B < 3 / 3-5 / 5-7 / 7-10 / > 10; at 1 keV all bins |Δc| ≤ 0.005.
- Correlation of Δc(1/20) with k_B^tot: r = 0.74 (500 GeV), 0.19 (1 TeV), against −0.05 and 0.07 with γ*.
- **At 1 keV there is no k_B^tot dependence**: all k_B^tot bins give |Δc| ≤ 0.004, consistent with 0, on the same kinematics (the k_B^tot
  distribution is identical, since k_B^tot depends only on kinematics).
- So the effect depends on k_B^tot **and** on ε⊥ (smaller at 3 keV), as predicted by critical B1: the B* change of η is ε-dependent and
  non-monotonic in k_B^tot, so it does not cancel in a ratio of B values.
- With B* small (k_B^tot < 5) and γ* < 1.3 the converged 3 keV c agrees with E1 to ≤ 0.003 at all f (≤ 0.001 at B₀/2 and B₀/4).

**(c) Verdict [superseded → §13: about half of the excess is a period-number-dependent B* effect; the other half is per-period, survives with B* and E*∥ switched off, and is consistent with the double-precision floor at ε⊥ ≈ 10⁻⁷].** ~~The excess is **explained in origin, not quantitatively**~~: it is a physical B* effect (deterministic, step-converged,
one-sided, carried by k_B^tot ≳ 5 events, absent at 1 keV and for k_B^tot < 5). It is not round-off and not step error. A quantitative
prediction needs E1's analytic or CM-frame B* law (in progress). The 1 keV agreement stands. At 3 keV, E1's c_ev is verified only
for k_B^tot ≲ 5, or at B₀/2 for the full sample.

### 12.2 Critical A2 — stale statements
Flagged in place: §0 items 1 and 4, §4.2 (3 keV c), §8 Surprise 2, §11 FU1(b) round-off numbers (now 0.147 / 0.236 / 0.441 / 0.739 %,
p90 1.14 / 0.75 / 1.31 / 4.81 %, c sd 0.0060 / 0.0038 / 0.0044, p90 0.0178 / 0.0119 / 0.0226, all from FU.json `roundoff_L3`), the
"amplification" wording, and the FU1 verdict.

### 12.3 Constructive B5 — provenance: new §1.4 (two solvers / one solver / T3 copy / model comparison); "blind" is now qualified.

### 12.4 Constructive B6 — cheap reruns
- **(i) Li/exact thickness at γ* = 2** (30 events, Λ = 1 keV, m = 500 GeV, p_T = 300 GeV, 3.8 T; Li at 10⁻³ of the printed step;
  3×10⁻⁴/10⁻³ = 1.0000 [0.9996, 1.0004], so converged): **Li/causal = 0.75 ± 0.08** (median; p16-p84 0.55-1.15). This agrees with
  R2's 0.69 (5 events). It is 3σ above E1's prediction of 0.50 (ESTIMATE, one Li implementation). Sample sensitivity (R2-C10):
  the 10-event subset run also at 3×10⁻⁴ has median 0.96 ± 0.10 (both steps identical), against 0.75 ± 0.08 on all 30, so the
  "3σ" depends on the sample; the event-to-event spread (p16-p84 0.55-1.15) dominates.
- **(ii) Medians 5-20 % below the T3 tables.** T3's own event list was regenerated (seed 2026, 60 / 24 events) and re-run: my kernel
  reproduces T3's per-event B-only thickness **exactly (ratio 1.000 for all 432 events)**. So the code and the hit definition are
  identical. The difference is the event draw: T3 vs M3 medians are 33.8 ± 4.1 vs 29.0 ± 2.1 µm (500 GeV, 1 keV), 4.90 ± 0.47 vs
  3.80 ± 0.29 (3 keV), 37.7 ± 2.5 vs 28.7 ± 2.6 (200 GeV, 1 keV), 3.86 ± 0.53 vs 4.16 ± 0.32 (1 TeV, 3 keV), i.e. 1-2.5σ
  fluctuations of 60-event samples. Physics is excluded as the cause.
- **(iii) Low-γ* residual.** Per pair vs E1's closed form, γ* < 1.2 (195 events: Λ = 0.6, 1, 2 keV, three masses, events 0-59):
  **+0.248 ± 0.019 ε⊥ (max_boost 10⁻²) → +0.029 ± 0.011 (10⁻³) → +0.026 (10⁻⁴, 7 events; paired 10⁻³ − 10⁻⁴ = +0.023 ± 0.009)**.
  The production residual is numerical (step error). The converged residual (+0.03 ε⊥, 0.2 % of ψ_pair) is consistent with zero at the
  10⁻⁴ level of statistics. The odd-only residual vs my γ*-interpolated M2b law converges to +0.12 instead (0.204 → 0.124 → 0.119);
  since the pair residual vs E1's closed form vanishes, that +0.12 is the interpolation of the M2b fits in γ*, not physics.
  Population residual at max_boost 10⁻³ (all γ*, first 20 events, FU.json `FU3.fine_first20.all.rel_pair`): −1.15 ± 0.36 % (reviewer C5),
  vs +0.3 % in production. The high-γ* deficit of §11 FU3 (−4 % to −7 %) is step-independent and is the B* effect of §12.1.

### 12.5 Constructive B9 — notation: new §1.5 (mapping to E1's symbols, following the reviewer's conflict table). E1's §1 table did not
exist at the time of writing; a full rename is deferred until it does.

### 12.6 Response table
| finding | resolution |
|---|---|
| [superseded → §13 for the origin] A1: round-off cannot explain the k_f ≥ 4 excess; the 10⁻⁴ check used 8-9 survivors | Round-off attribution withdrawn. Queue cap raised; 39/40 events at 10⁻⁴ per mass: c converged at 10⁻³ to ≤ 0.001. Excess at B₀/20 (+0.012-0.013) deterministic and one-sided; perturbation-size replicas show no scaling. It tracks k_B^tot (r = 0.74), is absent for k_B^tot < 5 and at 1 keV: physical B* effect, origin identified, quantitative law pending (E1) |
| A2: stale K_vac → 0, c(3 keV) = 0.093, round-off % mismatch | Flagged in place with pointers to §11/§12; all round-off numbers now from FU.json |
| B5: solver independence overstated | §1.4 provenance table; "blind to the derivation, not solver-independent" in the header |
| B6(i): Li/NG at γ* = 2 | 0.75 ± 0.08 (30 events, converged) vs E1 0.50, R2 0.69 |
| B6(ii): medians below T3 | Exact reproduction of T3 per event; event-draw fluctuation (1-2.5σ) |
| B6(iii): low-γ* residual | Step-dependent: +0.25 → +0.03 ε⊥ (10⁻² → 10⁻³ → 10⁻⁴); numerical |
| B9: notation | §1.5 mapping table (aligned to E1 symbols; full rename after E1's table) |
| C4 (critical): "amplify" wording | Withdrawn; replica-size test added |
| C5 (critical): quote fine rel_pair | −1.15 ± 0.36 % quoted (§12.4) |
| C8 (critical): 1 keV rise at k_f = 20 | Mentioned in §4.2 (+0.0015 ± 0.0005, 3σ) |
| C3 (constructive): K → 0 | Flagged (A2) |
| C6 (constructive): ε also = glueball emission | Noted in §1.5 |
| B2 (critical; E1's headline form) | My c is the local slope c_f = (R(f) − 1)/ln(1/f), i.e. the ε_B[ln(1/ε_B) + C] form's logarithmic derivative; no change to the measurements |


## 13. Fix pass 2 (review S1-R2: N1, N2) — `FIX2_runs.py`, `FIX2_analysis.py`, `nm_bstar.py`, `results/FIX2.json`
New runs: 735 jobs, 7.2×10³ s CPU (2.0 CPU-h; raw `data/stage1_numerics/FIX2/`). Earlier numbers are unchanged.
**Method.** The kernel now accepts a general uniform B vector; z-only runs remain bit-identical to T3_causal. Two switches were added:
- **B* off.** Uniform lab fields E_lab = γ²β×fB and B_lab = γ²[β(β·fB) − β²fB] transform to exactly (E*, B* = 0) in the event's pair
  (P₀) frame. Numerically the residual |B*| is ≤ 2×10⁻¹⁶ T and E* is unchanged to 10⁻¹⁹.
- **E*∥ off.** The pair-frame field is E*⊥ only (component ⊥ the initial axis n̂, with B* = 0), via the inverse boost.

**Period-number scan.** Classical NG is scale-free, so (1 keV, B₀/9, R) ≡ (3 keV, B₀, R/9) exactly. Scaling the detector (radii, z-limits,
exits, hmax) by s = 1/9, 1/3, 1 at Λ = 3 keV keeps every per-period quantity (ε⊥, b/ℓ₀, γ*, k_B, α) and changes only the number of
periods (∝ s). s = 1/9 is R2's 1-keV same-window test.

Setup: M3 events 0-39 per mass (seed 777 + m), f ∈ {1, 1/2, 1/4, 1/20}, max_boost 10⁻³ (converged for c, §12.1), all runs status 1.
Δc = c(k_f) − c_E1 (per event, median ± bootstrap, n = 40).

### 13.1 N1 — origin of the 3 keV weak-field excess
| setting | 500 GeV: Δc(2), Δc(4), Δc(20) | 1 TeV: Δc(2), Δc(4), Δc(20) |
|---|---|---|
| B* on, s = 1 (full tracker; FU runs) | −0.0005, +0.0038 ± 0.0032, **+0.0121 ± 0.0031** | +0.0005, +0.0071 ± 0.0032, **+0.0122 ± 0.0047** |
| B* on, s = 1/3 | −0.0005, +0.0012, +0.0049 ± 0.0027 | +0.0002, +0.0017, +0.0121 ± 0.0045 |
| B* on, s = 1/9 (= 1 keV, same window) | −0.0001, +0.0008 ± 0.0004, +0.0033 ± 0.0011 | +0.0005, +0.0009, +0.0048 ± 0.0022 |
| **B* off**, s = 1 | −0.0008, −0.0002 ± 0.0006, **+0.0044 ± 0.0008** | +0.0001, +0.0008 ± 0.0004, **+0.0064 ± 0.0020** |
| B* off, s = 1/3 | −0.0002, +0.0001, +0.0038 ± 0.0008 | +0.0002, +0.0008, +0.0082 ± 0.0027 |
| B* off, s = 1/9 | +0.0001, +0.0003, +0.0030 ± 0.0007 | +0.0005, +0.0008, +0.0054 ± 0.0024 |
| **B* off and E*∥ off**, s = 1 | −0.0001, +0.0002, **+0.0039 ± 0.0010** | +0.0003, +0.0009, **+0.0062 ± 0.0025** |
| B* off and E*∥ off, s = 1/9 | +0.0001, +0.0004, +0.0030 ± 0.0007 | +0.0004, +0.0008, +0.0055 ± 0.0020 |
| paired (on − off) at s = 1/9 / 1/3 / 1, Δc(20) | +0.0000 / +0.0014 / **+0.0063 ± 0.0023** | −0.0005 / +0.0010 / +0.0024 ± 0.0041 |
| paired (on − off) at s = 1, Δc(4) | +0.0014 ± 0.0038 | **+0.0061 ± 0.0030** |

Split by k_B = |B*⊥|/|E*⊥| (E1's definition) at s = 1, Δc(20): B* on +0.0041 (k_B < 5) / +0.033 (k_B ≥ 5) at 500 GeV and
+0.0049 / +0.035 at 1 TeV; B* off +0.0023 / +0.0106 and +0.0033 / +0.0184; B* and E*∥ off +0.0022 / +0.0100 and +0.0035 / +0.0189.
2D bins (k_B split at 5, b_odd/ℓ₀ at B₀/20 split at the class median): with B* off, smaller b gives a larger excess at fixed k_B (500 GeV:
+0.0030 vs +0.0013 for k_B < 5, +0.015 vs +0.008 for k_B ≥ 5). With B* off, the rank correlation of Δc(20) with k_B is 0.84 / 0.57 and the
partial correlation given b_odd/ℓ₀ is 0.82 / 0.46 (500 / 1000 GeV). In this sample k_B and b_odd/ℓ₀ are less collinear than in R2's
(Spearman −0.37 / −0.61).

**Reading.**
1. **B* gives a physical part that grows with the number of periods.** At B₀/20, on − off Δc(20) is +0.0000 / +0.0014 / +0.0063 ± 0.0023 at
   s = 1/9, 1/3, 1 (500 GeV): ≈ half of the full-scale 0.0121. At 1 TeV it is −0.0005 / +0.0010 / +0.0024 ± 0.0041, ≈ 20 % of 0.0122 (R3-C2).
   The floor-free evidence is Δc(4) for k_B ≥ 5: on − off = **+0.0136 ± 0.0039 (500 GeV) / +0.0125 ± 0.0038 (1 TeV) at s = 1**,
   +0.0055 ± 0.0029 / +0.0002 ± 0.0035 at s = 1/3, and ≈ 0 (+0.0009 / −0.0003) at s = 1/9. This is a physical, cumulative B* effect
   (deterministic, step-converged).
2. **The other half is per-period and is not B*, not E*∥.** It survives with both switched off and is N-independent within errors
   (500 GeV: +0.0030 / +0.0038 / +0.0044 at s = 1/9, 1/3, 1, a mild rise; 1 TeV: +0.0054 / +0.0082 ± 0.0027 / +0.0064) (R3-C4). With the CM field reduced to pure E*⊥ the problem is the M2b problem, whose
   per-period law is verified to 0.1 % for ε⊥ ≥ 3×10⁻⁷. At B₀/20 these events have median ε⊥ ≈ 2×10⁻⁷ (smaller for large k_B, i.e.
   small sin α) and b_odd/ℓ₀ ≈ 10⁻⁷ (median 1.5×10⁻⁷ / 0.9×10⁻⁷). That is at the double-precision floor.
3. **The floor matches in scaling, not in magnitude** (corrected after R3-C1, C3). M2b (γ* = 1.3, causal 10⁻³) measured ψ_pair excess over the
   law = +0.16 % at ε⊥ = 3.2×10⁻⁷, **+1.7 % at 10⁻⁷** and **+18 %** at 3.2×10⁻⁸ (ψ_odd 16.566 / 18.116 / 21.03 vs law 16.558 / 17.987 / 19.42; ψ_even 1.631 / 1.811 / 3.73 vs 1.61). An excess
   δ in Δs(B₀/20) shifts c(20) by δ/ln 20, i.e. +0.002…+0.006 for ε⊥ = 2-1×10⁻⁷. The per-event medians are ε⊥(B₀/20) = 2.9×10⁻⁷ (500 GeV) and 1.9×10⁻⁷ (1 TeV),
   where the CM-frame floor predicts Δc(20) ≈ +0.0008 / +0.0019 against the measured pure-E*⊥ +0.0039 / +0.0062. **The full-event pure-E*⊥ residual
   scales as ε⊥^−2.1 / ε⊥^−1.9 (500 / 1000 GeV, R3), with an amplitude ≈ 3.8× the CM-frame floor coefficient.** This is consistent with round-off in
   scaling (ε⊥⁻², γ*-independent, per period; a physical correction to an asymptotic weak-field law cannot grow as ε⊥⁻²), not in magnitude. The
   attribution to the precision floor stays **ESTIMATE**; it needs a lab-frame floor coefficient ≈ 3-4× the CM-frame one, not demonstrated,
   since higher precision is unavailable (§11 FU1b). An accumulation-model term is not
   excluded. Note that the step tests (10⁻⁴) and the replica tests do not probe this floor.
4. At B₀/2 (k_f = 2) nothing is left in any setting (|Δc| ≤ 0.001). At B₀/4 the excess is the B* part (+0.006 ± 0.003 at 1 TeV) plus ≤ 0.001.
5. Relation to R2's numbers: our s = 1/9 (B* on) gives +0.0033 ± 0.0011 / +0.0048 ± 0.0022 on events 0-39, against R2's 1-keV
   +0.0059 ± 0.0018 / +0.0078 ± 0.0022 on events 0-59 (consistent within 1-1.5σ).

**Verdict N1.** The 3 keV weak-field excess has **two parts**:
- **(i) a physical B* effect** (≈ half at B₀/20, the dominant part at B₀/4), which grows with the number of periods and is carried by
  k_B ≳ 5 events;
- **(ii) a per-period part** that survives with B* and E*∥ removed, is independent of the number of periods, scales with small ε⊥ and b_odd,
  and matches in size the double-precision floor of the pure-E* problem.
It is neither "a B* effect" alone (v2 §12.1) nor "small b_odd / period number" alone. E1's per-event law is verified wherever both are
small: k_f = 2 (all events) and k_B < 5 at k_f ≤ 4.

### 13.2 N2 — the excess at the nominal field B₀ for Λ = 5-13 keV
Direct runs at B₀ with k_f = 2 (c from B₀ and B₀/2; max_boost 10⁻³):

| m | Λ [keV] | n | c_E1 (median) | c measured (median) | Δc(2) population | Δc(2), k_B < 5 | Δc(2), k_B > 10 (n) |
|---|---|---|---|---|---|---|---|
| 500 | 5 | 30 | 0.0782 | 0.087 ± 0.006 | +0.005 ± 0.007 | +0.003 ± 0.002 | +0.08 ± 0.04 (3) |
| 500 | 7 | 30 | 0.0743 | 0.098 ± 0.024 | +0.025 ± 0.025 | +0.008 ± 0.009 | +0.03 ± 0.07 (3) |
| 500 | 10 | 30 | 0.0706 | 0.089 ± 0.023 | +0.017 ± 0.023 | +0.003 ± 0.015 | +0.2 ± 1.9 (3) |
| 500 | 13 | 20 | 0.0680 | 0.113 ± 0.057 | +0.044 ± 0.058 | +0.028 ± 0.017 | — (2) |
| 1000 | 5 | 20 | 0.0743 | 0.082 ± 0.007 | +0.004 ± 0.007 | +0.002 ± 0.004 | +0.12 ± 4 (5) |
| 1000 | 7 | 20 | 0.0708 | 0.078 ± 0.016 | +0.002 ± 0.017 | −0.002 ± 0.012 | −0.03 ± 2 (5) |
| 1000 | 10 | 20 | 0.0674 | 0.147 ± 0.112 | +0.08 ± 0.11 | +0.010 ± 0.024 | +1.1 ± 2.5 (5) |

- **Convergence (honest).** At 7 keV, five events re-run at max_boost 10⁻⁴ give per-event c(2) differences (10⁻³ − 10⁻⁴) of +0.106, 0.000, +0.031,
  −0.026 and 0.000. **c from a factor-2 B ratio is not step-converged per event above ≈ 5 keV at max_boost 10⁻³.** At 10-13 keV, ε⊥ at B₀ is
  (3/Λ)² × the 3 keV value, i.e. ≈ 4×10⁻⁷-2.4×10⁻⁷, so the B₀ points themselves approach the precision floor. The population medians at
  7-13 keV (errors ±0.02-0.1) do not constrain the effect.
- **Measurable part.** At Λ = 5 keV and B₀: Δc(2) = +0.005 ± 0.007 (500 GeV), +0.004 ± 0.007 (1 TeV), i.e. ≤ 10 % of c at 1σ. For k_B < 5 it is
  +0.003 ± 0.002, against +0.08-0.12 in the k_B > 10 tail (3-5 events, large errors).
- **Translation by scale equivalence.** (3 keV, B₀ → B₀/20) is the per-period B₀ law from 3 to 13.4 keV. Of the 3 keV excess, the physical part
  at real N is the B* part: +0.006 in c(20) (500 GeV) at the 3 keV period number. The number of periods at the real Λ = 3√k_f keV is larger
  (N ∝ Λ²), and the B* part grows with N (0 → +0.001 → +0.006 for N/9 → N/3 → N). An extrapolation to N(13 keV) = 19 N(3 keV) is not reliable.
  The per-period part (ii) is numerical and does not enter the physical B₀ law.
- **Impact statement for E1.** The population effect on Δs_B(Λ)/Δs_B(3 keV) at B₀, integrated from the direct medians (d ln Δs/d ln Λ = −2 + 2c),
  is +0.3 % (5 keV), +1.3 % (7), +2.8 % (10) and +4.5 % (13 keV) at 500 GeV, and +0.2 / +0.4 / +3.4 % (5 / 7 / 10 keV) at 1 TeV. Statistical errors
  (propagated bootstrap, R3-B1 item 4) are ±0.4 / ±1.0 / ±2.0 / ±2.8 % (500 GeV) and ±0.4 / ±0.8 / ±4.2 % (1 TeV). On top of these, the ≥ 7 keV
  points are not step-converged per event and carry a floor part of comparable size at 10-13 keV (R3: predicted floor Δc(2) +0.010-0.039 vs
  measured +0.017-0.079). These values are therefore **not** a B* magnitude. Direct runs give ≲ 1 % at 5-7 keV. Per event, k_B ≳ 10 events
  carry tens of % in c (as R2 says) but are statistically unresolved here. **Recommendation [revised after R3-B1]:** above ≈ 5 keV the B₀ law is not numerically
  verified. Carry an **unmeasured, unattributed provisional systematic of ±5 % on Δs_B** (population; sign expected positive), and up to tens of %
  in c per event for k_B ≳ 10. The physical B* part is demonstrated only in the scale-equivalent 3 keV B scan; its size at B₀ is not measured. Measuring it needs
  the floor part removed first (higher precision), then max_boost ≤ 10⁻⁴ (queue cap 2²¹) at ≥ 7 keV, about 10× the present cost. (The direct B₀
  runs are one-solver, max_boost 10⁻³; §1.4.)

### 13.3 R2 C items applied to NUMERICS.md
C1 (positive-definite sentence flagged as withdrawn), C8 (tag-system mapping line in §1.4), C10 (Li γ* = 2 subset 0.96 ± 0.10 vs 0.75 ± 0.08
noted in §12.4). §12.1(c) now points here. N3/N4 and C2-C7, C9 concern E1's files and PROPOSED_CHANGES.

### 13.4 Response table (fix pass 2)
| finding | resolution |
|---|---|
| N1: B* attribution not shown; k_B and b_odd collinear; half per-period | B* off, E*∥ off and period-number scan run. A physical, cumulative B* part (Δc(4), k_B ≥ 5: on − off +0.0136 / +0.0125 at full scale, ≈ 0 at 1/9; ≈ half of Δc(20) at 500 GeV, ≈ 20 % at 1 TeV) plus a per-period part, B*- and E*∥-independent, that matches the precision floor in scaling (ε⊥⁻²), not in magnitude (≈ 3.8×; ESTIMATE). §12.1(c) superseded |
| N2: impact at B₀ for 5-13 keV | Direct B₀ runs: Δc(2) = +0.004…+0.005 ± 0.007 at 5 keV; ≥ 7 keV not step-converged per event and floor-affected. Revised after R3-B1: an unmeasured, unattributed provisional ±5 % on Δs_B above ≈ 5 keV (not a B* number) |
| C1, C8, C10 | applied (§13.3) |


## 14. Fix pass 3 (review S1-R3, text only, no runs)
| R3 item | resolution |
|---|---|
| B1: "+2-5 % B*-driven systematic" | Replaced by an unmeasured, unattributed provisional ±5 % on Δs_B above ≈ 5 keV (§13.2). Statistical errors corrected to the propagated bootstrap (±0.4-2.8 %); floor content and one-solver status stated |
| C1: floor "size matches" | §13.1(3): the pure-E*⊥ residual scales as ε⊥^−2.1 / −1.9 with amplitude ≈ 3.8× the CM-frame floor coefficient; consistent with round-off in scaling, not magnitude; ESTIMATE |
| C2: B* part wording | §13.1(1): ≈ half at 500 GeV, ≈ 20 % at 1 TeV in Δc(20); floor-free Δc(4), k_B ≥ 5, on − off +0.0136 ± 0.0039 / +0.0125 ± 0.0038 at full scale, ≈ 0 at 1/9 |
| C3: M2b +11 % | corrected to +18 % (and +0.15 → +0.16 %), checked against M2.json |
| C4: "same at all s" | "N-independent within errors" with the 1 TeV +0.0082 ± 0.0027 point quoted |
| C8: stale pointers | §0 item 4, §4.2 and the §11 FU1 verdict and reading lines now point to §13 (§0 item 4 and the FU1 verdict completed after R4 C-a); §12.6 A1 row flagged "[superseded → §13]"; §13.4 rows rewritten |
