# Log-enhanced axis rotation at near-miss crossings and the B-field plane thickness of a quirk pair (classical Nambu-Goto)

E1, theory track Stage 1 (P1). **Status: v4 (2026-10-10), fix pass 1 after review S1-R1** (critical ITERATE 2A/3B/8C;
constructive 0A/12B/8C). Previous versions: `NEAR_MISS_IMPULSE_v3.md` (v1-v3 history in its §9 and in `predictions.json`
changelog). The response table is §12. §9.3 merges E2's fix pass (NUMERICS §12, results/FIX1.json) and c14.

Tags: **DERIVED** = derived here, checked by sympy and a limiting case; **VERIFIED-NUM** = a derived formula confirmed by
crossing-resolved numerics (causal string, and conformal-gauge solver where stated); **ESTIMATE** = numerically determined
constant, model step or population number; **CONJECTURE** = not checked. Check scripts: `analytic/checks/cNN_*.py`, outputs
`*_out*.txt` next to them. "E2" = the blind numerics in `analytic/numerics/NUMERICS.md` (+ `results/*.json`).

## 0 Summary (for collider phenomenologists)
1. A quirk pair is two heavy charged particles joined by a string of tension σ = Λ². Without fields they oscillate through
   each other along a line (a "yo-yo") and leave tracker hits on a plane through the vertex.
2. In the pair rest frame the solenoid field is a weak uniform electric field E* = γβ×B. Its torque gives angular momentum
   in one half-oscillation and takes it back in the next, so the ends miss by b ≈ 3.5 µm (keV/Λ)⁴ at every second ("odd")
   crossing (500 GeV, 3.8 T, median) and meet head-on at the others.
3. At a near miss the string pulls the ends sideways with σb/|x|, whose integral is ln(ℓ_max/b): the oscillation axis turns,
   always toward E*, by η = ε⊥G(γ*)[ln(ℓ_max/b) + K] per period. G (with the retardation factor 1/artanh β*) is derived and
   checked to 0.2 %; K ~ 0.1 is numerical (3 ln 2 − 2 analytic when slow). This is the analytic theory of Li et al.'s fitted η.
4. Accumulated, this gives **Δs_B ∝ ε_B[ln(1/ε_B) + C], ε_B = qB/Λ²**, C ≈ 0.4/1.2/1.6 at 200/500/1000 GeV (Λ-independent):
   Δs_B ≈ Λ^−1.8 B^0.9, nearly m_Q-independent. Li's Λ⁻⁴m_Q formula has the scaling of b, not of the thickness.
5. Blind numerics: local slope c = 1/[ln(1/ε_B) + C] = 0.104 vs 0.105 ± 0.002 (1 keV, 500 GeV); B exponent 0.914 vs
   0.911 ± 0.003; Λ exponents within errors. At 3 keV, B₀/2 agrees; the weak-field excess (+14 % at B₀/20) is a B* effect (§9.3).
6. Limits: classical NG holds at odd crossings for Λ ≲ 26 keV. The CM magnetic field alters η when |B*⊥| ≳ 6|E*⊥|
   (5-43 % of events; per-event c up to +36 % off, §6.4). Above ≈ 1.5 keV Δs_B is below the MS floor.

## 1 Setup, notation, observable

### 1.1 Notation (binding for E1 and E2; E2 aligns to this table)
| Symbol | Meaning | E2 name / old E1 use |
|---|---|---|
| σ = Λ², σ = 50.68 GeV/cm (Λ/keV)² | string tension (Λ ≡ √σ) | — |
| ε_B ≡ qB/σ = 2.254×10⁻⁴ (B/3.8112 T)(keV/Λ)² | dimensionless lab field (qB = 2.998×10⁻³ GeV/cm per T) | — |
| E*, B* | CM-frame fields, E* = γ_cm β_cm × B, B* = γ_cm B − (γ_cm−1)(B·β̂)β̂ | E2: E*, B* |
| n̂; ê⊥ | initial CM axis (direction of quirk 1, charge +q); unit vector of E*⊥ | — |
| ε⊥ ≡ q\|E*⊥\|/σ, ε∥ | CM field ⊥ and ∥ n̂ in units of σ | E2: ε, ε⊥. (T2/S-19's glueball emission probability is renamed ε_gb in E1 text) |
| k_B ≡ \|B*⊥\|/\|E*⊥\| | ratio of the CM magnetic to electric field components ⊥ n̂ | v3 "kB" |
| α | angle between E* and n̂ (CM) | — |
| φ* | azimuth of n̂ about β̂_cm, measured from the bending (transverse) plane | new (§6.3) |
| γ*, β*, ρ = γ*β*, χ* = artanh β* = asinh ρ | per-quirk CM kinematics | E2: γ*, v = β* |
| p*, ℓ₀ = m/σ, ℓ_max = 2(γ*−1)ℓ₀, T_h = 2p*/σ | CM momentum, length unit, max separation, half period | E2: ℓ_k ≈ ℓ_max |
| crossing index j (odd/even) | crossings j = 1, 2, …; odd j = Li's g = 1, 3, … | E2 M1: "k" (crossing). v3 E1: "k" |
| f = B/B₀, k_f = 1/f | field fraction in a B scan, B₀ = 3.8112 T | E2 M3/FU: "k = 2…80" |
| J | total angular momentum (ends + string) about the CM | E2: "J" also = string impulse ΔJ_b — E2 renames to ΔΠ_s |
| b_odd, b_even | miss distance at odd/even crossings | E2: c_b = b_odd/(ε⊥ℓ_max) |
| p_rel,⊥ = (p_1⊥ − p_2⊥)/2 | relative transverse momentum | E2: Π |
| v | CM speed of **one** end; the relative speed is 2v (NR) | v3 E1 §3.3 used v for the relative speed |
| η | axis rotation per CM period (absolute angle) | E2: ψ_pair ε⊥ = (ψ_odd + ψ_even) ε⊥ |
| ψ_j | rotation across crossing j, in units of ε⊥ | E2: ψ_odd, ψ_even |
| G(γ*) | log coefficient of η/ε⊥ | E2: A_o, "a" |
| L_η ≡ ln(ℓ_max/b_odd) | log of the field-driven rotation | v3 "L" |
| K(γ*) | constant of η (pure E*, per period) | E2: K_o + ψ_even = G[L_η − ln(1/ε⊥) + K] |
| Â, K_vac | vacuum per-crossing law ψ = Â(b/ℓ_max)[ln(ℓ_max/b) + K_vac] | E2: Â, ln(L/ℓ_max) = K_vac |
| C | constant of the thickness law Δs ∝ ε_B[ln(1/ε_B) + C] (§5.2) | new |
| c | local log slope d ln(Δs/ε_B)/d ln(1/B) = 1/[ln(1/ε_B) + C] | synthesis "c" |
| Δs_B | truth-level B-only plane thickness (§1.3) | E2: Δs_B |
| Kang-Luty | 0805.4642 (two authors; E3 writes "KLN") | — |

### 1.2 Map to Li et al.'s notation [2002.07503 §II, §V, App.A]
| Li et al. | here | relation |
|---|---|---|
| g (quirks meet at g = 2n) | crossing index j | g = j at crossings |
| η: rotation of the system per period about ê_yc [Eq.A.6], fitted, r(0.5)\|η\| ~ \|w₁\| ~ d_E [Eq.A.17] | η (§4) | same object |
| z⁻ = (z₁ − z₂)/2 [Eq.II.18], z⁻_o0 [Eq.A.13] | half the relative transverse offset | z⁻_o0 omits the string's transverse pull |
| d_E = (2mqE_z/Λ⁴) ρ sinh⁻¹ρ [Eq.V.8] | compare b_odd/2 (§3.2) | d_E/(b_odd/2) = 3.04/3.21/3.68/4.20 at γ* = 1.05/1.28/2/3 [c01] |
| E_z | E*·N̂ (out-of-plane part of E*) | |
| B_c | B* | enters the rotation only through the inner region (§6.4) |
| first term of Eq.V.5-V.6 / B.9 | §5 accumulation | secular accumulation of η |

### 1.3 The observable
**Δs** = √(smallest eigenvalue of T_ij = Σ_a h_i^a h_j^a/(N−1)) over all hits h^a of both quirks on the 10 Phase-2 barrel
layers (R = 3.0-108.3 cm, |z| within the layer length; every crossing of a layer counts), plane through the primary vertex
(origin) [1708.02243 Eq.11; 2002.07503 Eq.C.1; `T3_propagator.plane_fit`]. Truth level: true hit positions, known
assignment, no resolution, no material. **Δs_B** = Δs with the uniform lab field B and no material; the vacuum Δs is 0
(planar exact solution). The theory below predicts Δs_B through the out-of-plane part of the axis rotation (§5.1).
- In-plane vs out-of-plane: the same η (same logarithm) turns the axis toward ê⊥, which has both components (§6.3); so the
  response per unit B must be the same for in-plane (rφ) and out-of-plane hit displacements after the first crossing.
  Test (existing data, no new run): rφ displacements, S_Bnonlin (T4 kernel, 500 GeV, 1 keV, PS/2S, max_boost 10⁻³):
  R(1/4) = 1.145/1.150, R(1/20) = 1.306/1.325; out-of-plane, E2 M3 (500 GeV, 1 keV): R(1/4) = 1.139, R(1/20) = 1.319.
  Equal within 1 %: **confirmed** [figures/S_Bnonlin_out.txt; NUMERICS §4.2].

### 1.4 Reduction of the problem (linear dynamics: DERIVED; rotation: see item 4)
1. NG with massive point ends [0805.4642 Eq.3.7] plus Lorentz forces is Lorentz covariant. A uniform constant lab B is,
   in the frame of the initial pair velocity, the uniform constant pair E*, B* (table 1.1). Solving there and boosting
   back involves no simultaneity convention.
2. The pair starts at the origin of that frame with momenta ±p* n̂ (J = 0).
3. In the **linear** (outer) dynamics B* acts on neither the relative motion nor the angular momentum: for x₂ = −x₁,
   v₂ = −v₁, q₂ = −q₁ the magnetic forces on the two ends are equal, so they cancel in the relative equation, and their
   torque about the CM is (x₁ + x₂)×(q v₁×B*) = 0 [c01 (4); independently re-derived by the critical reviewer]. In symmetry
   terms: E* forcing is even under inversion through the CM combined with exchange of the ends, B* forcing is odd, and an
   axis rotation is even. So in linear response B* only shakes the CM, and b_odd does not depend on B* (checked: c12).
4. **The rotation η is not a linear-response quantity.** It is generated in the non-linear inner region of the odd
   crossing, where the B*-driven motion (odd parity, size comparable to b) enters at even order. So η depends on γ*, ε⊥
   **and** k_B, non-monotonically and with an ε dependence of its own (§6.4). The pure-E* problem (k_B = 0), which
   depends on γ* and ε⊥ only, is the reference used in §3-§5. E*∥ only makes successive half-periods unequal (second
   order, §6.1).
5. For a transverse pair (|η_pair| < 1): |E*| = γ_cm β_T,cm B, ε⊥ = ε_B γ_cm β_T,cm sin α.

### 1.5 Assumptions and scope
- Classical NG string with point ends; equal masses; charges ±q. The pair is produced at one point, with J = 0, a straight
  zero-length string, no transverse string excitation, no infracolour radiation. Classical motion (quantum numbers
  ~10¹⁶ [T2 §6.1]).
- Results depend on σ only, i.e. they are independent of N_IC and of the infracolour representation once Λ = √σ. Spin
  enters only through the γ* distribution (§6.5).
- Uniform B (3.8112 T), no material.

## 2 Vacuum yo-yo
- Exact solution [T2 §2.1; 0805.4642 §3.3]: in the CM the motion is along n̂; each end feels the constant force σ; the
  separation in the first half-period is **x(t) = 2ℓ₀[γ* − √(1 + (ρ − t/ℓ₀)²)]**, 0 ≤ t ≤ T_h, with x(0) = x(T_h) = 0,
  x_max = ℓ_max, end speed β* at the crossings, dp/dt = −σ exactly [c01 (1)]. The quirks pass through each other:
  x(t + T_h) = −x(t).
- The world sheet is the flat region of the (t, x) plane between the end world lines, a chain of lenses touching at the
  crossings. At a crossing the string has zero length (fold); once the ends miss each other the degenerate pieces become
  short string bits (§3.4).
- **Rigid-rotation lemma (DERIVED).** At a crossing the string has zero length and carries no momentum, so the state is
  given by the two end momenta; rotating both by δ about the crossing point produces the rotated vacuum solution. A
  transverse relative momentum Δp⊥ acquired around a crossing therefore rotates all later motion rigidly by δ = Δp⊥/p*.
- Half-period integral [c01 (2)]: **I ≡ ∫₀^{T_h} x dt = 2ℓ₀²[γ*ρ − asinh ρ]**.

## 3 Linear response and its breakdown

### 3.1 Torque and angular momentum (DERIVED)
Exactly, dJ/dt = Σᵢ xᵢ × qᵢE* = q(x₁ − x₂) × E* (the string is neutral; B* gives no torque, §1.4). On the vacuum yo-yo:
J(T_h) ≡ J_odd = q|E*⊥| I (direction n̂×ê⊥); J(2T_h) = J_odd − J_odd = 0 since x(t + T_h) = −x(t). J oscillates: 0 at
production and at even crossings, J_odd at odd ones (Li et al.'s "meet at g = 2n" [2002.07503 Eq.A.4-A.5], now with the
value at odd crossings).

### 3.2 Odd-crossing miss distance (DERIVED; VERIFIED-NUM)
At a crossing J is carried by the ends: J = b p*. Hence

**b_odd = J_odd/p* = 2 ε⊥ ℓ₀ [γ* − asinh(ρ)/ρ]**,   b_odd/(ε⊥ℓ_max) = [γ* − asinh ρ/ρ]/(γ* − 1).

- Limits [c01 (3)]: NR → (4/3) qE m β*²/σ²; E → 0 → 0; m → ∞ at fixed γ*: b/ℓ_max fixed.
- Exact NG (c03; E2 M2b causal and conformal): b₁/b_odd = 1.0000-1.0001; b_odd/(ε⊥ℓ_max) = 1.327/1.298/1.240/1.188 vs E2
  1.328/1.298/1.240/1.189 (γ* = 1.05/1.3/2/3). Full events: 1.30-1.34 (E2 M1). Independent of B* (c12).
- Size: median ≈ 3.5 µm (keV/Λ)⁴ for m = 500 GeV, 3.8 T on the T3 sample [T2 §5.3; c06 events 1.5-10 µm at 1 keV].
- **Credit.** The scale m qB/Λ⁴ of "a separation of classical quirk trajectories after one oscillation" is Kang-Luty's
  [0805.4642 §5.8, Eq.5.64]. Li et al.'s d_E [2002.07503 Eq.V.8] and the thickness formula d ≈ 1.16 µm (m/100 GeV)
  (keV/Λ)⁴(B/T) [1911.02223 Eq.III.12] have the same scaling, qBm/σ² × O(1). Numerically Eq.III.12 gives ≈ 22 µm × B_xy/B
  at 500 GeV, 1 keV, about 6× the median b_odd. Li's d_E is 3.0-4.2 × b_odd/2 because z⁻_o0 [Eq.A.13] integrates the field
  force without the string's transverse pull −σz/|x| (Li note the deviation, App.A after Eq.A.13). **Eq.III.12 thus has
  the scaling of the odd-crossing miss distance, not of the accumulated plane-fit thickness** (synthesis X-2).

### 3.3 Linearised outer equations and where they break down (DERIVED)
- Non-relativistic straight string (μ = m/2, transverse relative coordinate z along ê⊥, x(t) from §2, relative speed at the
  crossing 2v): μz̈ = −σz/|x(t)| + q|E*⊥|. z = θ₀x(t) is a zero mode (rigid rotation); the Wronskian μ(xż − zẋ) = J obeys
  the torque law; with θ = z/x: **θ̇ = J(t)/(μx²)**.
- Relativistic NG: in static gauge y_tt = y_xx on the flat world sheet; transverse momentum balance at a moving end
  x = X(t), Ẋ = V gives **dp_⊥,end/dt = ∓σ(y_x + V y_t) + qE*⊥** (derivation by Leibniz' rule on ∫σy_t dx; c02 (1)).
- **Breakdown.** Near a crossing x ≈ 2v|s|; σ/|x| ∝ 1/|s| makes s = 0 a regular singular point: z is continuous, ż has a
  log singularity, i.e. ∫σz_j/(2v|s|) ds diverges unless z_j = 0.
  - Production (z = 0, J = 0) and even crossings (z_j = J/p* = 0): regular. Hence first-order theory is exactly
    reproduced before the first crossing: pre-crossing response linear to 10⁻⁴ (E2 M3; S_Bnonlin; R1_Blinearity).
  - Odd crossings (z_j = b_odd ≠ 0): the linear connection is undefined; the impulse depends on b itself, ∝ b ln(1/b).
    **First-order perturbation theory fails at every odd crossing, and only there** (precise form of Li et al.'s remark
    after Eq.A.13, and of synthesis X-3).

### 3.4 The intermediate region of a near miss: exact NG solution (DERIVED)
For b ≪ |x| ≪ ℓ₀ the ends move freely at x = ±vs (v = β*); the world sheet is the wedge |x| < v|s|; the string piece is
light (σ|x| ≪ mγ*), so it is slaved to the end positions. For the relative offset Y_± = ±b/2 the solution of y_tt = y_xx is

**y(s, x) = (b/2) artanh(x/s)/artanh(v)**   [c02 (2)],   force on the ends **F_⊥ = ∓σb/(2|s| artanh v)**   [c02 (3)].

- v → 0: σb/(2v|s|), the straight-string value [c02 (4)]. The string is curved (y ∝ artanh(x/s)); 1/artanh v instead of 1/v
  is the retardation effect (v/artanh v = 0.97/0.85/0.66/0.53 at γ* = 1.05/1.28/2/3).
- Relative transverse velocity gives an s-independent force; free log-periodic string modes give convergent impulses
  [c02 (6)]. **Only the offset b produces the logarithm.**
- Over the intermediate region on both sides, p_rel,⊥ changes by −(σb/artanh β*)[ln(L_out/b) + O(1)] (L_out ~ ℓ_max; lower
  cut-off ∝ b from the inner region |x| ≲ bγ*²/artanh β*). In E2's profile normalisation (σb/v) the log slope is
  **κ = β*/artanh β*** = 0.968/0.845/0.658/0.535, measured 0.963/0.840/0.653/0.52 (E2 M2a).
- This momentum is accrued within |s| ≲ 0.05 T_h of the crossing, relative to the *incoming* axis, and equals p*δ, a
  rotation (rigid-rotation lemma). At the next turning point only J survives: p⊥ = J/[ℓ(1 + σℓ/6m)] for a rigidly rotating
  straight string, so the turning-point-to-turning-point transfer has **no** logarithm:
  ΔΠ/(σb/β*) = ρβ*/[(γ*−1)(1 + (γ*−1)/3)] = 1.920/1.608/1.125/0.800, measured 1.92/1.61/1.15/0.79 (E2 M2a; post-hoc,
  no parameter). **The logarithm ends up in the direction of the axis.**

## 4 Inner near-miss problem and matching

### 4.1 Structure of the result (pure E*, k_B = 0)
By the lemma the impulse of §3.4 rotates the axis by Δp_rel,⊥/p* toward +ê⊥ (the end of charge +q swings toward E*⊥).
The log coefficient follows from §3.4 with b = b_odd; with k_B = 0 the remaining constant can depend only on γ* (ε⊥ and ℓ₀
scaled out, E*∥ second order). So, per CM period,

**η = ε⊥ G(γ*)[ln(ℓ_max/b_odd) + K(γ*)],   G = 2[γ* − asinh ρ/ρ]/(ρ artanh β*)**   (DERIVED structure; K numerical).

- G → 4/3 − 8β*²/45 (NR); G = 1.316/1.245/1.239/1.165/1.087/0.953 at γ* = 1.05/1.28/1.3/1.6/2/3 [c01 (6)].
- ln(ℓ_max/b_odd) = ln(1/ε⊥) + ln[(γ*−1)/(γ* − asinh ρ/ρ)] (second term −0.28…−0.17).
- Limits: ε⊥ → 0: η ∝ ε ln(1/ε) (non-analytic); α = 0: η = 0 (c03); B → 0: η/B ∝ ln(1/B).
- Coherence: J_odd has the same direction every period, so η adds linearly (Θ = Nη).
- With B* (k_B ≠ 0) the constant becomes k_B- and ε-dependent (§6.4); G and b_odd do not change.

### 4.2 Exact NG constant K(γ*) (log coefficient VERIFIED-NUM; K ESTIMATE)
c03: exact causal string, pair at rest in E* ⊥ n̂, ε = 10⁻⁶…10⁻³; axis from the apocentres.

| γ* | G | K (max_boost 10⁻⁴) | spread over ε | independent checks |
|---|---|---|---|---|
| 1.05 | 1.316 | +0.056 | ±0.003 | E2 M2b: per-period constant G[ln((γ*−1)/(γ*−asinh ρ/ρ)) + K] −0.300 vs −0.304 |
| 1.28 / 1.3 | 1.245 / 1.239 | −0.049 / −0.059 (fit) | ±0.003 | E2: −0.396 vs −0.399; critical reviewer (conformal, own E/B extension): K(1.3) = −0.0587 |
| 1.6 | 1.165 | −0.175 | ±0.002 | — |
| 2.0 | 1.087 | −0.309 | ±0.002 | E2: −0.569 vs −0.574; reviewer: −0.309…−0.314 |
| 3.0 | 0.953 | −0.569 | ±0.003 | E2: −0.707 vs −0.704 |
| → 1 | 4/3 | 3 ln 2 − 2 = +0.0794 (analytic, §4.3) | | reviewer NR integration +0.07944 |

- The slope of η/ε⊥ against ln(1/ε⊥) equals G(γ*) to ≤ 0.1 % at every γ*, confirming the retardation factor (the
  quasi-static 1/β* would give slopes 1.03-1.88× larger). Interpolation: **K ≈ (3 ln 2 − 2) − 0.506 ln γ* − 0.077 ln²γ***
  (≤ 0.002 [c08]). |K| ≤ 0.6 against ln(ℓ_max/b) ≈ 8-14, so K moves c by ≤ 6 %.

### 4.3 Non-relativistic closed form (DERIVED)
Straight string, NR ends (the γ* → 1 limit of every model); μ = σ = 1, relative crossing speed v₀, ℓ_max = v₀²/2,
b = (2/3)εv₀² [c05]:
1. Outer (|x| > R): ∫θ̇ dt over one period minus the neighbourhood of the odd crossing:
   I_out = 2b/R + (2b/v₀²)[ln(2v₀²/R) − 1]; the even crossing is regular.
2. Inner (r < R): sweep angle from the radial action, Δφ = −∂S/∂J, first order in the potential:
   Δφ_in = π − 2b/R + (2b/v₀²)[ln(2R/b) − 1].
3. Sum (R drops out): **η_NR = (4/3) ε⊥[ln(6/ε⊥) − 2] = (4/3) ε⊥[ln(ℓ_max/b_odd) + 3 ln 2 − 2]**.
- Split at the turning points (post-hoc, c09): ψ_even = 2/3 + (4/3) ln 2 = 1.591 (E2: 1.606 at γ* = 1.05) and
  ψ_odd = (4/3)[ln(1/ε⊥) + ln 3 − 5/2]. The even crossing carries the smooth, non-log torque rotation; the odd one the log
  plus a non-log offset of opposite sign. Their sum is the K above.
- Vacuum (constant J, both parities): ψ = (b/ℓ_max)[ln(ℓ_max/b) + 3 ln 2 − 2] per crossing (c09, c10), i.e. Â_NR = 1,
  K_vac,NR = 3 ln 2 − 2; E2 FU2: 0.0791 ± 0.0003. E3's apsidal check (slope 0.354 = 1/(2√2) in units m = E = σ = 1, so
  v₀ = √2) gives the same Â_NR = 1 (critical reviewer C3).
- The L ln(1/L) structure is standard near-radial orbit mechanics in a linear potential (E3; NOVELTY_AUDIT §0). New here:
  that it acts only at the odd crossings of the field-driven yo-yo with b from the torque law, the relativistic NG
  coefficient with retardation, the constants, and the consequences for Δs_B.

### 4.4 Straight strings: the logarithm needs neither curvature nor retardation; its size does (DERIVED + VERIFIED-NUM)
Any attraction of fixed magnitude σ along the string gives σb/|x| and hence ln(1/b). c04 (same reduced problem, Li's CM
simultaneity [1911.02223 Eq.III.6] with P = 0, ŝ = unit separation [Eq.III.8-9], 8th-order adaptive integrator):

| model | transverse force (intermediate region) | b_odd | vacuum Â (E2 M2a) | K (field, own b) |
|---|---|---|---|---|
| exact NG | σb/(2\|s\| artanh β*) | angular-momentum formula | 2(γ*−1)/(ρ artanh β*) = 0.992/0.955/0.877/0.802 (meas. 0.996/0.951/0.878/0.793) | §4.2 |
| quasi-static central | σb/(2β*\|s\|) | same | 2(γ*−1)/(ρβ*) | +0.080/+0.104/+0.210/+0.485 (γ* = 1/1.05/1.28/2) |
| Kang-Luty (= Li in the CM) | σb(1 − β*²)/(2β*\|s\|) | ×1.040/1.213/1.680 (non-central force, ends' J not conserved) | 2(γ*−1)(1−β*²)/(ρβ*) = 0.929/0.669/0.333/0.167 (meas. 0.934/0.670/0.332/0.167) | +0.05/−0.18/−1.8 (γ* = 1.05/1.28/2) |

- A converged Li integrator has the same B ln(1/B) response, with c within ≈ 3 % of NG (c depends only on the constant,
  not on the log coefficient): confirmed by E2 M5 (Li 1.142/1.306/1.447 vs causal 1.155/1.320/1.467 at B/4, B/20, B/80).
- The size differs: per field-driven period η_KL/η_NG ≈ (Â_KL/Â_NG)(b_KL/b_NG)(ratio of constants) = 0.97/0.84/0.50 at
  γ* = 1.05/1.28/2; measured converged Li/causal thickness ratios: 0.97/0.85 (R2) and **0.75 ± 0.08 at γ* = 2** (E2 FIX1,
  30 events; R2: 0.69). **The γ* = 2 prediction (0.50) fails at 3σ** (diagnosis §9.5).

## 5 Accumulation over crossings → the Δs_B law, c, exponents

### 5.1 From η to the hits: the rotating yo-yo (structure DERIVED; model ESTIMATE)
- The axis turns by η toward ê⊥ at every odd crossing, coherently: Θ(t*) = η N_odd(t*). In the tracker Θ ≲ 10⁻², so the
  rotations stay linear and E*⊥ does not change appreciably (as Li et al. assume [2002.07503 App.C]).
- Only the out-of-plane part, η ê⊥·N̂, changes the plane fit (N̂ = unit(n̂ × β̂_cm); the CM and lab planes share N̂ because
  boosts along β̂ preserve directions ⊥ β̂). The in-plane part is T4's "mostly rφ" B displacement [T4 §3.2].
- **Rotating-yo-yo model** (c06): exact vacuum yo-yo with n̂ → n̂ cos Θ + ê⊥ sin Θ, Θ stepping by η (pure-E* K) at each odd
  crossing; boosted to the lab; hits and plane fit as in §1.3. **Nothing is fitted.** Omitted: the non-secular first-order
  offsets (b_odd, the alternating static tilt ±q|E*⊥|/σ), the B* effect (§6.4), and the spread of the rotation over the
  half-period at large γ*.
- Accuracy against the exact causal string, event by event (c06; T3_causal, 3.8112 T, no material), per γ* bin, with the
  fraction of events in each bin (c13, T3 sample, 150 events per mass):

| γ* bin | model/causal Δs_B, median (range), 0.6-3 keV | n | event fraction 200 / 500 / 1000 GeV |
|---|---|---|---|
| 1.0-1.1 | 0.968 (0.877-1.005) | 16 | 0.13 / 0.22 / 0.31 |
| 1.1-1.2 | 0.988 (0.964-1.039) | 18 | 0.16 / 0.21 / 0.29 |
| 1.2-1.35 | 0.988 (0.962-1.005) | 10 | 0.24 / 0.24 / 0.19 |
| 1.35-1.6 | 1.003 (0.995-1.123) | 6 | 0.13 / 0.17 / 0.17 |
| 1.6-2.0 | 1.014 (1.009-1.018) | 2 | 0.18 / 0.09 / 0.03 |
| > 2.0 | 1.173 (0.645-1.344) | 12 | 0.16 / 0.07 / 0.00 |

  At 10 keV (8 events) the median is 0.98; outliers (0.43, 0.81) are events with ε⊥ ten times below typical (E* almost
  ∥ n̂), where omitted terms dominate. Summary: 1-4 % for γ* ≲ 1.6 (84-97 % of events at 500-1000 GeV, 66 % at 200 GeV);
  10-35 % off for γ* > 2 (16 % of events at 200 GeV, 7 % at 500 GeV, 0 at 1 TeV). For γ* > 2 two known effects act, the
  delocalisation of the 1/s force over the half-period and the B* effect (§6.4: −7…−21 % of η at γ* = 2 for k_B = 4-16).
  They are not separated.

### 5.2 The thickness law (headline; DERIVED scaling, constants ESTIMATE)
In the model Δs is linear in η. Over the tracker N_osc = σR/(2β*p_T) ∝ σ [T2 §2.2], the lever (oscillation width) is ∝ ℓ₀,
and η ∝ ε⊥ ∝ γ_cm β_T,cm qB/σ. So the total out-of-plane rotation is ~ qBR G(L_η + K)/p* (a bending angle of momentum p*
over R), and

**Δs_B = (qBR/σ) · F · [ln(1/ε_B) + C],   C = −ln(γ_cm β_T,cm sin α) + ln[(γ*−1)/(γ* − asinh ρ/ρ)] + K(γ*)**,

with F dimensionless (γ*, angles, layer phases), independent of m and Λ at fixed velocities. Population values of C
(c07: C = 1/c_median − ln(1/ε_B), T3 sample):

| m [GeV] | C at Λ = 0.6 / 1 / 2 / 3 / 5 / 10 keV | C (adopted) |
|---|---|---|
| 200 | 0.437 / 0.437 / 0.432 / 0.431 / 0.432 / 0.439 | 0.43 |
| 500 | 1.223 / 1.228 / 1.230 / 1.226 / 1.221 / 1.223 | 1.23 |
| 1000 | 1.626 / 1.623 / — / 1.616 / — / 1.618 | 1.62 |

- **Λ-independent to ±0.01**, as the derivation requires. C depends on m through −ln(γ_cm β_T,cm) = −ln(p_T/M): at fixed
  p_T heavier pairs are slower. This is the only m dependence besides the γ* spectrum. The model medians are
  33.5/31.1/29.5 µm at 200/500/1000 GeV (1 keV); E2 measures 28.7 ± 2.6 / 29.1 ± 2.1 / 31.0 ± 2.2. Both are flat within
  errors; the sign of the weak trend is not resolved.
- The law is Δs_B ∝ B/Λ² times a slowly varying log: T4's x_B ≈ 0.5 qBR/σ [T4 §3.2] and the m-independent ∝ B/Λ² plane
  rotation of Knapen et al. [1708.02243 Eq.8-9] have the same leading scaling.
- **Comparison with Knapen et al. at their benchmark** (2 keV, 2 T; γ* = 1.28, v = 0.62, v_cm = 0.25):
  - Their Eq.8 as printed, Δφ ~ ε_B v_cm γ_cm γ*²v²/(γ*−1)², gives 6.1×10⁻⁵ per oscillation.
  - Their Eq.9 prefactor, 10⁻⁵ (v_cm²/v²), gives 1.6×10⁻⁶, about 40× smaller than Eq.8 at the same point.
  - Our η (sin α = 0.8) is 8.9×10⁻⁵ per period, of the same order as Eq.8. The parametric form differs: Eq.8 → 4ε/v² for
    v → 0, while η is finite (∝ (4/3)ε⊥ ln) and carries the logarithm.
  - At the thickness level, Eq.9 × 1 m gives ≈ 1.6 µm (E3's reading), against the causal Δs_B ≈ 4.5 µm (E2 M3 at 2 keV
    scaled to 2 T with B^0.91).
  - v3's "the secular part is larger by G(L+K) ≈ 10-15" is withdrawn. The robust statement: their torque estimate captures
    the scale q|E*|/σ and the alternating half-period rotation (their "Δφ oscillates and slowly accumulates"), not the
    logarithmic secular term or its origin.
- Relation to Li et al.'s Eq.A.17 (r(0.5)|η| ~ d_E, an order-of-magnitude statement): our η ℓ_max/2 = ε⊥ℓ₀(γ*−1)G(L_η+K)
  ≈ 3 d_E at γ* = 1.28. This is consistent with "~" at the factor-3 level, the factor coming mostly from the logarithm.

### 5.3 c as the local log slope; response per unit B
- Definition: **c ≡ d ln(Δs_B/ε_B)/d ln(1/B) = 1/[ln(1/ε_B) + C]** (per event, with the event's C). The response per unit B is
  R(f) ≡ Δs(fB)/(fΔs(B)) = 1 + c ln(1/f) under the rotating-yo-yo assumption.
  - DERIVED under that assumption (Δs ∝ η, pure E*, non-secular terms omitted).
  - Not valid per event for k_B ≳ 6, where B* changes η (§6.4).
  - Population median VERIFIED-NUM at 1 keV to ≤ 1.5 % (E2 FU1a: +0.0001…+0.0015; critical reviewer, independent solver:
    +0.0016 median on 16 events).
- **The literal form Δs ∝ ε_B[1 + c ln(Λ²/qB)] with a constant c ≈ 0.10 (synthesis S-3, v1-v3 predictions.json) is not
  equivalent and is withdrawn.** Read literally it gives d ln Δs/d ln B = 1 − c/(1 + c ln(σ/qB)) = 1 − 0.104/1.873 = 0.944
  at 1 keV (reviewer's value, confirmed), not the measured 0.911. The consistent statement is the law of §5.2, with
  c(Λ, B, m) = 1/[ln(Λ²/qB) + C(m)] its local log slope. The predicted fall of c with Λ (0.116 → 0.070 from 0.6 to 10 keV at
  500 GeV) is then a test.
- Population c (median, 16-84 %; c07):

| m [GeV] | Λ = 0.6 | 1 | 2 | 3 | 5 | 10 keV |
|---|---|---|---|---|---|---|
| 200 | 0.128 (0.122-0.136) | 0.113 (0.108-0.120) | 0.098 | 0.091 (0.087-0.095) | 0.083 | 0.074 (0.072-0.077) |
| 500 | 0.116 (0.109-0.126) | **0.104 (0.098-0.112)** | 0.091 | 0.085 (0.081-0.090) | 0.078 | 0.070 (0.068-0.074) |
| 1000 | 0.111 (0.105-0.120) | 0.100 (0.095-0.107) | 0.088 | 0.082 (0.078-0.086) | 0.076 | 0.068 (0.066-0.072) |

- Response at 500 GeV, 1 keV: predicted R(1/2, 1/4, 1/20, 1/80) = 1.072/1.144/1.311/1.455; E2 M3 (blind)
  1.073/1.147/1.320/1.460 (±0.001-0.005). B exponent over B/80…B: ln(1.455)/ln 80 → **B^0.914**, E2 0.911 ± 0.003.
  B₀/1000 (and ≤ B₀/80 at 3 keV) is at the double-precision floor of both solvers (b/ℓ₀ ≈ 3×10⁻⁸, E2 §1.3) and is not used.

### 5.4 Local exponents
Per event (only ln(1/ε_B) depends on Λ and B): **d ln Δs_B/d ln B = 1 − c; d ln Δs_B/d ln Λ = −2 + 2c**; d ln Δs_B/d ln m = 0
at fixed velocities (at fixed p_T: +c from C, plus the γ* spectrum). Values at 3.8 T, 500 GeV: 1 − c = 0.884/0.896/0.915/0.930
and −2 + 2c = −1.77/−1.79/−1.83/−1.86 at 0.6/1/3/10 keV. Population (model medians, c07): −1.79 (0.6→1), −1.86 (1→2),
−1.78 (2→3), −1.87 (3→5), −1.84 (5→10). E2 M3: −1.83 ± 0.10, −1.83 ± 0.07, −1.88 ± 0.11, −1.76 ± 0.09, −1.74 ± 0.14;
mean over 0.6-5 keV −1.81/−1.81/−1.78 at 200/500/1000 GeV. The ±0.1 point-to-point scatter is layer sampling.

## 6 Odd vs even crossings, γ*, angles, B*, charge and spin

### 6.1 Even crossings
- First order: J = 0 at every even crossing, so b_even = 0 and there is no near-miss (log) impulse. The even crossing does
  carry the smooth, non-log torque rotation: ψ_even = 2/3 + (4/3) ln 2 = 1.591 (NR, c09); E2: 1.61-1.70 (M2b), 1.59-1.63
  (M1). This term repeats every period and is part of K.
- Second order: (i) E*∥ makes the half-periods unequal: c03 at α = 45° gives b_even/b_odd ≈ 12 ε∥; (ii) the rotation by η
  changes the torque lever, b_even ~ η b_odd. In events b_even ≲ 10⁻³ b_odd (E2 M1), so the even-crossing log impulse is
  O(ε² ln ε) and negligible.
- With E* ⊥ n̂ the causal code's b_even is a splitting artefact ∝ max_boost (2.6×10⁻³/3×10⁻⁴/2.7×10⁻⁵ b_odd at
  10⁻²/10⁻³/10⁻⁴; c03, E2 M2b): proposed erratum to T2 §5.3/§6.3 (`analytic/PROPOSED_CHANGES.md`).
- Sign pattern: every odd-crossing log rotation is toward +E*⊥. No random walk in B-only propagation.

### 6.2 γ* dependence
b_odd/(ε⊥ℓ_max) = 1.33 → 1.19 for γ* = 1.05 → 3; G = 4/3 → 0.95 (retardation); K = +0.08 → −0.57. c depends on γ* through
ln[(γ*−1)/(γ*−asinh ρ/ρ)] + K (−0.23 → −0.74): c rises ≈ 5 % from γ* = 1.05 to 3 at fixed ε⊥. Model accuracy per γ*
bin: §5.1.

### 6.3 Angles ("crossing angle")
- The near miss itself has no free angle: it is head-on to b/ℓ ~ 10⁻⁶-10⁻⁹. The geometry enters through two CM angles:
  α (E* vs n̂, enters ε⊥ and the log) and φ* (azimuth of n̂ about β̂_cm, from the bending plane; it sets the out-of-plane
  share of the rotation).
- For B = Bẑ and a transverse pair (β̂_cm = x̂), with n̂ = (cos θ*, sin θ* cos φ*, sin θ* sin φ*), Ê* = −ŷ and
  N̂ = (0, sin φ*, −cos φ*) (DERIVED):
  - sin α = √(1 − sin²θ* cos²φ*);
  - ε⊥ = ε_B γ_cm β_T sin α;
  - out-of-plane share f_N ≡ |ê⊥·N̂| = |sin φ*|/sin α;
  - **η_N = η f_N = ε_B γ_cm β_T |sin φ*| G(γ*)[L_η + K]** (sin α survives only inside L_η).
  Pairs whose axis lies in the bending plane (φ* = 0, n_z = 0) rotate within their plane and get little thickness.
- Quantitatively (c13, model, 500 GeV, 1 keV, 150 events): median Δs/median(Δs) = 0.11/0.46/0.43/1.05/1.38 for
  f_N ∈ [0, .25)/[.25, .5)/[.5, .75)/[.75, .9)/[.9, 1] (54 % of events have f_N > 0.9); rank correlation of Δs with f_N
  0.69; vs sin α: 0.29/0.40/1.16/1.16/1.31 for [0, .4)/[.4, .6)/[.6, .8)/[.8, .9)/[.9, 1]. This angle structure drives
  the event-to-event spread of Δs_B (16-84 % = 0.3-1.7 × median).

### 6.4 The CM magnetic field B* (ESTIMATE, c12, critical-review numbers; mechanism CONJECTURE)
- B* does not change b_odd (c12) and gives no linear-response rotation (§1.4). Its effect on η comes from the non-linear
  inner region. Exact-string results in the pair rest frame (E* ⊥ n̂, B* along z unless stated):

| γ* | k_B | Δη/η at ε = 10⁻⁵ | at 10⁻⁴ | source |
|---|---|---|---|---|
| 1.05 | 4 | +3×10⁻⁵ | +1.5×10⁻⁵ | c12 |
| 1.3 | 1 / 2 / 4 / 8 / 16 | −0.02 % / −0.16 % / −0.22 % / **−2.6 %** / −2.4 % | — / — / −0.21 % / −0.68 % (reviewer) / — | c12 kB scan; reviewer r1_conf_cm |
| 1.3 | 4, B* ∥ E* | −0.12 % | −0.44 % | c12 |
| 2.0 | 1 / 2 / 4 / 8 / 16 | −0.18 % / −1.9 % / −6.8 % / −13.8 % / −21 % | — / −3.4 % (reviewer) / −7.3 % / −12.0 % (reviewer) / — | c12; reviewer r1_conf_cm_g2 |
| 2.0 | 4, B* ∥ E* | −4.2 % | −7.7 % | c12 |
| any | B* ∥ n̂ | ≤ 3×10⁻⁵ | ≤ 3×10⁻⁵ | c12 |

  The effect is even in B* (±k_B give the same value), vanishes as γ* → 1, is **non-monotonic in k_B** (a jump ×12 between
  k_B = 4 and 8 at γ* = 1.3) and **ε-dependent with a k_B-dependent sign of the slope** (ratio 10⁻⁴/10⁻⁵ = 1.84 at k_B = 2,
  0.88 at 8, γ* = 2; 0.26 at k_B = 8, γ* = 1.3). It is therefore not a constant shift of K. v3's "enters K, not G; c rises
  by |Δη/η|" is withdrawn.
- **Effect on c** (per pair, c14: c_k = [kη(ε₀/k)/η(ε₀) − 1]/ln k with fixed k_B, ε₀ = 6×10⁻⁶ (3 keV-like) and
  5×10⁻⁵ (1 keV-like)): see §9.3 (A1 test) for the table.
  - With the critical reviewer's end-to-end check (unmodified R1 solver, 16 events, γ* = 1.28, 1 keV): events with
    k_B ≤ 6.5 agree with c_ev within ±0.009; the three events with k_B = 8.4-12 (sin α = 0.36-0.47) are +0.016/+0.032/+0.035
    (**+17 % to +36 %**).
  - **Fraction of events with k_B > 6 (k_B > 8): 5 % (3 %) at 200 GeV, 29 % (16 %) at 500 GeV, 43 % (29 %) at 1 TeV** (c13;
    median k_B = 2.0/4.1/5.1). For these events the per-event c_ev is not reliable.
- In lab events k_B ≈ sin(n̂, ẑ)/(β_T,cm sin α) is 2-12 typically. The B* effect explains the sign and size of E2's
  high-γ* odd-crossing residual (FU3: −4 % at γ* = 1.35-1.6, −9 % above 1.6). With converged steps the population per-pair
  residual is −1.15 ± 0.36 % (FU3 fine subset; production +0.3 %).
- **Population-level c uncertainty is taken from the empirical 1 keV agreement (≤ 1.5 %; §5.3), not from c12.**

### 6.5 Charge and spin (DERIVED per event; population ESTIMATE, c13)
- Charge |q|: ε⊥, b_odd, B* all scale ∝ q (k_B unchanged), so ln(1/ε_B) → ln(1/ε_B) − ln q and
  **Δs_B(q)/Δs_B(1) = q[1 − ln q/(ln(1/ε_B) + C)], c(q) = 1/(ln(1/ε_B) + C − ln q)**. For |q| = 2: ratio 1.86 (not 2), c = 0.112
  vs 0.104 (1 keV, 500 GeV). Model population: 57.8 vs 31.1 µm (1.86) at 1 keV, 7.84 vs 4.18 µm (1.88) at 3 keV. The same
  formula gives the ≈ c ln 2 ≈ 7 % departure from linearity in Li et al.'s factor-two charge test, consistent with their
  "linearly proportional" at their precision [2002.07503 §V.A, Fig.4] (NOVELTY_AUDIT credit sentence 4).
- Scalar Ẽ: classical NG has no spin, so the per-event law is the same; only the production distributions change (scalar DY
  is P-wave, so larger γ*). Input needed: the scalar LO DY sample (available, T2 cache `S_*_isr`). Model population at
  500 GeV: median γ* 1.39 vs 1.23 (fermion); f(γ* > 1.6) 0.32 vs 0.16; median Δs_B 36 vs 31 µm (1 keV), 4.83 vs 4.18 µm
  (3 keV); c 0.103 vs 0.104. Because a third of scalar events sit in the γ* > 1.6 region (model 10-35 % off, larger B*
  effect), scalar predictions carry roughly twice the model uncertainty of the fermion case (ESTIMATE).

## 7 NG validity
- **Claim region:** the classical result is safe for Λ ≲ 10 keV and typical events up to Λ ≈ 26 keV, where
  b_odd Λ ≈ 1.8×10⁴ (keV/Λ)³ falls to 1 (≈ 12 keV for events with ε⊥ ten times below typical). Above ≈ 1.5 keV Δs_B is
  below the multiple-scattering floor anyway [T3 §3.2].
- For b_odd < 1/Λ the region |x| < 1/Λ is not NG and the lower cut-off of the log becomes ~1/Λ × O(1):
  L_η → ln(ℓ_max Λ) + K″. The model uncertainty on Δs_B is ≈ c[ln(1/(b_odd Λ)) + O(1)]: ≈ 3-8 % at 30 keV, 10-25 % at 100 keV
  (ESTIMATE). This replaces the synthesis' "10-30 % for Λ ≳ 10-20 keV" [S-3]. Below the cut-off the response becomes linear
  in B and d ln Δs/d ln Λ = −2 − 1/[ln(ℓ_max Λ) + K″] (CONJECTURE).
- Even crossings have b_even ≪ 1/Λ from a few keV but no log impulse (§6.1).
- Classical NG is scale-free: b/ℓ₀ ≈ 3×10⁻⁸ is a separate, numerical floor of the double-precision solvers, not a
  physical threshold (E2 §1.3).

## 8 Predictions table
B = 3.8112 T, truth level, B only, T3 event sample (|η_pair| < 1, LO DY+ISR) unless stated. Machine-readable:
`predictions.json` (v4). Post-hoc items (written after E2's results) are marked †.

| # | Quantity | Prediction | Status |
|---|---|---|---|
| P-1 | Odd-crossing miss distance | b_odd = 2ε⊥ℓ₀[γ* − asinh ρ/ρ]; median ≈ 3.5 µm (keV/Λ)⁴ at 500 GeV, 3.8 T; independent of B* | DERIVED; VERIFIED-NUM (10⁻⁴, two solvers) |
| P-2 | Even crossings | b_even = 0 at first order; ≲ 10⁻³ b_odd (second order); smooth non-log rotation ψ_even = 2/3 + (4/3) ln 2 (NR)† | DERIVED / ESTIMATE |
| P-3 | Transverse force, intermediate region | σb/(2\|s\| artanh β*) (NG); σb/(2β*\|s\|) (quasi-static); σb(1−β*²)/(2β*\|s\|) (Kang-Luty) | DERIVED; slope κ = β*/artanh β* VERIFIED-NUM |
| P-4 | Per-period axis rotation (pure E*) | η = ε⊥G(γ*)[ln(ℓ_max/b_odd) + K(γ*)], G = 2[γ* − asinh ρ/ρ]/(ρ artanh β*) | structure + G DERIVED, VERIFIED-NUM (0.1-0.2 %); K ESTIMATE |
| P-5 | K(γ*) (pure E*) | 3 ln 2 − 2 (γ* → 1, DERIVED); +0.056/−0.049/−0.175/−0.309/−0.569 at γ* = 1.05/1.28/1.6/2/3; fit (3 ln 2 − 2) − 0.506 ln γ* − 0.077 ln²γ* | ESTIMATE (two solvers at 1.3, 2) |
| P-6 | NR closed form | η_NR = (4/3)ε⊥[ln(6/ε⊥) − 2] | DERIVED; VERIFIED-NUM (reviewer, c04) |
| P-7 | Sign pattern | all odd-crossing log rotations toward +E*⊥; coherent, Θ = Nη | DERIVED |
| P-8 | Validity of P-4 | ε⊥ ≪ 1; b_odd ≫ 1/Λ (Λ ≲ 26 keV typical); first order in ε∥; k_B ≲ 6 (else §6.4) | DERIVED (conditions); k_B limit ESTIMATE |
| P-9 | Thickness law | Δs_B = (qBR/σ)F[ln(1/ε_B) + C], C = 0.43/1.23/1.62 at 200/500/1000 GeV, Λ-independent (±0.01, 0.6-10 keV) | scaling DERIVED under the rotating-yo-yo assumption; C ESTIMATE |
| P-10 | c (local log slope) | c = 1/[ln(1/ε_B) + C]; per event with the event's C; population medians §5.3 table, 0.104 at 1 keV/500 GeV | DERIVED under the rotating-yo-yo assumption; population median VERIFIED-NUM at 1 keV (≤ 1.5 %); per event not valid for k_B ≳ 6 |
| P-11 | d ln Δs_B/d ln Λ | −2 + 2c: −1.77/−1.79/−1.83/−1.86 at 0.6/1/3/10 keV (500 GeV) | as P-10 |
| P-12 | d ln Δs_B/d ln B at 3.8 T | 1 − c: 0.884/0.896/0.915/0.930 at 0.6/1/3/10 keV (500 GeV) | as P-10 |
| P-13 | Response per unit B, 500 GeV, 1 keV | R(1/2, 1/4, 1/20, 1/80) = 1.072/1.144/1.311/1.455; B^0.914 over B/80…B; B/1000 not testable (floor) | ESTIMATE (population) |
| P-14 | Same, 3 keV | 1.059/1.117/1.253 (k_f = 2/4/20); B/80 not testable | ESTIMATE; **k_f = 2 consistent; k_f ≥ 4 altered by B* for k_B ≳ 5 (origin explained, size not predicted, §9.3)** |
| P-15 | m dependence | only through C (−ln p_T/M) and the γ* spectrum; model medians 33.5/31.1/29.5 µm (1 keV) | DERIVED scaling; ESTIMATE numbers |
| P-16 | Rotating-yo-yo accuracy | 1-4 % for γ* ≲ 1.6; 10-35 % for γ* > 2 (per-bin table §5.1) | ESTIMATE (c06) |
| P-17 | Straight-string (Li) integrator | same log and B ln(1/B), c within ≈ 3 %; η_KL/η_NG ≈ 0.97/0.84/0.50 at γ* = 1.05/1.28/2 | DERIVED structure; VERIFIED-NUM (M5; ratios 0.97, 0.85 at γ* ≤ 1.28); **γ* = 2 FAILED (0.50 vs 0.75 ± 0.08)** |
| P-18 | NG-validity uncertainty on Δs_B | 0 for Λ ≲ 10 keV; ≈ 3-8 % at 30 keV; 10-25 % at 100 keV | ESTIMATE |
| P-19† | Vacuum per-crossing law | ψ = Â(b/ℓ_max)[ln(ℓ_max/b) + K_vac], Â = 2(γ*−1)/(ρ artanh β*); K_vac,NR = 3 ln 2 − 2 | DERIVED; VERIFIED-NUM (Â ≤ 1.2 %, K_vac,NR 0.0791 ± 0.0003) |
| P-20† | NR odd/even split | ψ_even = 2/3 + (4/3) ln 2; ψ_odd = (4/3)[ln(1/ε⊥) + ln 3 − 5/2] | DERIVED (c09; reviewer) |
| P-21† | Turning-point-to-turning-point transfer | ΔΠ/(σb/β*) = ρβ*/[(γ*−1)(1 + (γ*−1)/3)] (no log) | DERIVED (rigid straight string at the turning point); VERIFIED-NUM |
| P-22† | B* effect on η | even in B*, → 0 as γ* → 1, non-monotonic in k_B, ε-dependent (table §6.4); per-event c +17…+36 % at k_B = 8-12; f(k_B > 6) = 5/29/43 % at 200/500/1000 GeV | ESTIMATE; mechanism CONJECTURE |
| P-23† | Angle dependence | η_N = ε_Bγ_cmβ_T\|sin φ*\|G[L_η + K]; Δs/median 0.11 → 1.38 over f_N bins | DERIVED (formula); ESTIMATE (numbers, c13) |
| P-24† | Charge, spin | Δs(q)/Δs(1) = q[1 − ln q/(ln(1/ε_B) + C)] (1.86 for \|q\| = 2), c(2) = 0.112; scalar: same law, γ* spectrum (Δs 36 vs 31 µm at 1 keV) | DERIVED per event; ESTIMATE population |

## 9 Comparison with numerics
E2's campaign (`analytic/numerics/NUMERICS.md`, `results/*.json`) was blind to this note's coefficients (E2 did not open
E1 files before finishing; c07's predictions are timestamped before M3.json, checked by the critical reviewer). The solvers
are not independent of E1's code lineage: c03 uses T2's CausalNullString and E2's main kernel is a line-by-line copy of
T3_causal (both Athena-type piecewise-null maps). Second solvers: E2's conformal-gauge copy of R1, and the critical
reviewer's own E/B extension of the R1 formulation. **Two-solver (VERIFIED) numbers:** b_odd, G (A_o), the per-period
constant, ψ_even, Â/K_vac/κ at γ* ≤ 1.3, Δs and R at 500 GeV and 1-2 keV, K at γ* = 1.3 and 2 (reviewer). **One solver:**
Â, κ at γ* = 2-3; straight-string coefficients; thickness scans beyond 2 keV and at 200 GeV/1 TeV; the B* effect (c12; the
reviewer's conformal runs reproduce it at k_B = 2, 4, 8). Pull = (prediction − measurement)/σ_meas.

### 9.1 Per-crossing level (CM-frame controlled runs, M2; full events, M1)
| # | Quantity | E1 prediction (v1 formulas) | E2 measurement | pull / ratio | source |
|---|---|---|---|---|---|
| 1 | b_odd/(ε⊥ℓ_max) = [γ* − asinh ρ/ρ]/(γ* − 1), γ* = 1.05/1.3/2/3 | 1.3268/1.2979/1.2397/1.1884 | 1.328/1.298/1.240/1.189 (±0.03 %) | ratio 0.9991/0.9999/0.9998/0.9995 | M2.json (M2b) |
| 1b | same, full events (γ* mix) | 1.30-1.33 (γ* median 1.14-1.27) | 1.304-1.336; full/CM = 1.006-1.017 | ≤ 1.7 % | M1.json |
| 2 | Vacuum log coefficient Â = 2(γ*−1)/(ρ artanh β*) | 0.992/0.955/0.877/0.802 | 0.996±0.002/0.951±0.006/0.878±0.010/0.793±0.016 | −2.1/+0.6/−0.1/+0.6 | M2.json (M2a) |
| 3 | Impulse-profile slope κ = β*/artanh β* | 0.968/0.845/0.658/0.535 | 0.963±0.002/0.840±0.013/0.653±0.006/0.52±0.03 | +2.6/+0.4/+0.8/+0.5 (all ≤ 0.6 % but at 1.05; ≤ 3 % at γ* = 3) | M2.json |
| 4 | Field log coefficient per period G(γ*) | 1.316/1.239/1.087/0.953 | A_o = 1.318/1.241/1.0875/0.954 (±0.3 %) | ratio 0.998/0.999/0.999/0.999 | M2.json (M2b) |
| 5 | Per-period constant G[ln((γ*−1)/(γ*−asinh ρ/ρ)) + K] | −0.300/−0.396/−0.569/−0.707 | K_o + ψ_even = −0.304/−0.399/−0.574/−0.704 (±0.02) | +0.2/+0.2/+0.3/−0.1 | M2.json |
| 6 | ψ_even (smooth torque rotation across an even crossing) | not in v1; NR post-hoc 1.591 ε⊥ | 1.606/1.611/1.646/1.696 ε⊥ (M2b); 1.59-1.63 (M1) | NR vs γ* = 1.05: −0.9 % | M2.json, M1.json, c09 |
| 7 | Odd-crossing non-log constant | not in v1; NR post-hoc −1.869 | K_o = −1.91 (γ* = 1.05) | 2 % | M2.json, c09 |
| 8 | TP-to-TP transverse momentum (no log) | not in v1; post-hoc ρβ*/[(γ*−1)(1+(γ*−1)/3)] = 1.920/1.608/1.125/0.800 σb/β* | 1.92±0.01/1.61±0.02/1.15±0.06-0.12/0.79±0.09 | 0.0/−0.1/−0.3/+0.1 | M2.json |
| 9 | Straight-string (KL = Li in CM) vacuum Â | 0.929/0.669/0.333/0.167 | 0.934/0.670/0.332/0.167 | ratio 0.995/0.998/1.004/1.0 | M2.json, c10 |
| 10 | b_even | 0 at first order (pure E* ⊥ n̂); ~10⁻³-10⁻⁴ b_odd in events (second order) | M2b: ∝ max_boost (artefact), i.e. 0; M1: ≲ 10⁻³ b_odd, growing with crossing index | consistent | M2.json, M1.json |
| 11 | ψ_odd in full events = CM-frame law | CM law (§4) | matches to 1-2 %; residual +0.09…+0.23 ε⊥ (±0.02-0.07) | residual unexplained (§10) | M1.json |


### 9.2 Thickness level (M3 Λ and B scans; M13 bridge; M5)
| # | Quantity | E1 prediction (v1) | E2 measurement | pull / ratio | source |
|---|---|---|---|---|---|
| 12 | c, 500 GeV, 1 keV | 0.104 (event spread 0.098-0.112) | 0.105 ± 0.002 (k_f = 2-80; +1.5 % rise at k_f = 20, 3σ, FU1a) | −0.5 | M3.json |
| 13 | c, 1 TeV, 1 keV | 0.100 | 0.101 ± 0.001 | −1 | M3.json |
| 14 | c, 500 GeV, 3 keV | 0.085 | blind production 0.093 ± 0.002 (step-biased; superseded by §9.3) | blind −4 | M3.json |
| 14b | c, 1 TeV, 3 keV | 0.082 | blind production 0.091-0.095 (superseded by §9.3) | blind ≈ −5 | M3.json |
| 15 | R(1/2, 1/4, 1/20, 1/80), 500 GeV, 1 keV | 1.072/1.144/1.311/1.455 | 1.073/1.147/1.320/1.460 (±0.001-0.005) | −0.3/−1/−2/−1 | M3.json |
| 16 | same, 1 TeV, 1 keV | 1.069/1.138/1.299/1.437 | 1.070/1.141/1.302/1.443 | ≈ −1 each | M3.json |
| 17 | same, 500 GeV, 3 keV | 1.059/1.117/1.253/— | blind production 1.066/1.130/1.278/(floor); see §9.3 | blind −3/−4/−5 | M3.json |
| 18 | B exponent over B/80…B, 1 keV | 0.914 (500), 0.917 (1000) | 0.911 ± 0.003, 0.912 ± 0.003 | +1, +1.7 | M3.json |
| 19 | Λ exponents, 500 GeV (0.6→1, 1→2, 2→3, 3→5, 5→10) | −1.79, −1.86, −1.78, −1.87, −1.84 (model medians, c07) | −1.83±0.10, −1.83±0.07, −1.88±0.11, −1.76±0.09, −1.74±0.14 | +0.4, −0.4, +0.9, −1.2, −0.7 | M3.json |
| 19b | mean Λ exponent 0.6-5 keV | −1.79…−1.86 per event; −1.83 population | −1.81 (200), −1.81 (500), −1.78 (1000) | ≈ 0.3σ | M3.json |
| 20 | median Δs_B, 500 GeV, 1/2/3/5/10 keV [µm] | 31.1/8.6/4.18/1.61/0.45 (model, other events) | 29.1±2.1/8.17±0.72/3.80±0.29/1.55±0.11/0.46±0.06 | +1.0/+0.6/+1.3/+0.5/−0.2 | M3.json, c07 |
| 21 | m independence at 1 keV (200/500/1000) | 33.5/31.1/29.5 (weak decrease) | 28.7/29.1/31.0 (flat within ±2.5) | consistent within errors; the trend sign is not resolved | M3.json |
| 22 | Pre-crossing response | linear (first order exact there, §3.3) | R_hit = 1.0000, metric 10⁻⁴ | — | M3.json |
| 23 | Li vs causal response per unit B (M5) | c within a few % (§4.4: c_KL ≈ 0.106 vs c_NG ≈ 0.103 at γ* = 1.28, i.e. R(1/80) +1 %) | Li 1.142/1.306/1.447 vs causal 1.155/1.320/1.467 (same events) | consistent (−1 % to −1.4 %) | M5.json |


### 9.3 c at 3 keV (critical A1) — OPEN
**What is established** (E2 FU1, NUMERICS §11; FU.json): the blind production value (0.093) was step-biased (max_boost
10⁻² is converged for Δs to 1-2 % but not for c at 3 keV). With max_boost 10⁻³ (converged against 10⁻⁴ on the 8-9
surviving events, 45 % overflowed), per-event measured − E1 (same events):

| sample (3 keV) | k_f = 2 | k_f = 4 | k_f = 20 |
|---|---|---|---|
| 500 GeV, 10⁻³ (119 ev) | +0.0021 ± 0.0015 (pull 1.4) | +0.0055 ± 0.0020 (2.8) | +0.0113 ± 0.0018 (6.3) |
| 500 GeV, 10⁻³, γ* < 1.2 | +0.0004 ± 0.0019 | +0.0020 ± 0.0016 | +0.0056 ± 0.0013 |
| 1 TeV, 10⁻³ (120 ev) | −0.0003 ± 0.0006 (−0.5) | +0.0043 ± 0.0017 (2.5) | +0.0132 ± 0.0033 (4.0) |
| 1 keV, 500 GeV / 1 TeV (production = converged) | +0.0001 / +0.0003 | +0.0010 / +0.0007 | +0.0015 / +0.0001 |

Population c(k_f = 2) = 0.0890 (500 GeV), 0.0841 (1 TeV) vs E1 0.0839/0.0815 on the same events. **Agreement at 3 keV is
established only at B₀/2.** At B₀/4 and B₀/20 a k_f-dependent excess of +5-6 % and +13-16 % of c remains (c_k not constant,
contrary to the per-event linearity in ln(1/f)). One-sided: c₂₀ − c₂ > 0 in 15 of 17 converged events, five with
+0.019…+0.033 (reviewer). A smaller version of the same k-growth exists at 1 keV (+0.0015 ± 0.0005 at k_f = 20, 500 GeV;
reviewer +0.0020 ± 0.0011); from 1 to 3 keV it grows roughly ∝ N ∝ Λ².

**Withdrawn from v3:** "the excess follows the measured round-off amplification", "positive-definite noise biases c upward",
"c verified to 2-3 % at 3 keV", "the Λ dependence of c is confirmed", and the "b_odd/ℓ₀ ≳ 10⁻⁶ clean-ratio" criterion. The
reviewer showed that mean-zero noise enters √λ_min at second order: the measured replica noise (FU.json `roundoff_L3`:
rel. sd of Δs, median 0.147/0.236/0.441/0.739 % at f = 1, 1/2, 1/4, 1/20; p90 1.14/0.75/1.31/4.81 %; per-event c sd median
0.0060/0.0038/0.0044, p90 0.0178/0.0119/0.0226 for k_f = 2/4/20) implies a bias of ~10⁻⁵ in c, not +0.005-0.011. (v3 quoted
0.15/0.26/0.47/0.89 % and p90 1.3/0.8/1.3/4.8 %, with no source; corrected here.) Also the criterion was inconsistent:
1 keV at k_f = 80 has the same b_odd/ℓ₀ as 3 keV at k_f ≈ 9 and agrees.

**Test of the B* hypothesis (critical B1 → A1), c14:** per-pair c_k with and without B* in the reduced problem, at
ε₀ = 6×10⁻⁶ (3 keV-like, k_f = 2, 4, 20) and 5×10⁻⁵ (1 keV-like, k_f = 4, 20, 80), γ* = 1.1/1.3/1.6, B* along z and along
E*, α = 90° and 60°, k_B = 2-12 (`checks/c14_Bstar_cscan_out.txt`). Δc_k = c_k(k_B) − c_k(0):

| case | 3 keV-like (ε₀ = 6×10⁻⁶): Δc for k_f = 2; 4; 20 | 1 keV-like (ε₀ = 5×10⁻⁵): Δc for k_f = 4; 20; 80 |
|---|---|---|
| γ* = 1.1, B* ∥ z, k_B = 2-12 | \|Δc\| ≤ 0.0006 | \|Δc\| ≤ 0.0003 |
| γ* = 1.3, B* ∥ z, k_B = 4 / 8 / 12 | −0.010/−0.005/−0.032; \|Δc\| ≤ 0.002; \|Δc\| ≤ 0.002 | −0.000/+0.011/−0.005; +0.001/+0.004/+0.002; +0.001/+0.006/−0.001 |
| γ* = 1.3, B* ∥ E*, k_B = 8 / 12 | +0.002/+0.023; +0.004/+0.006; +0.000/+0.002 | −0.007/−0.003; +0.001/+0.003; −0.002/+0.002 |
| γ* = 1.3, α = 60°, k_B = 4-12 | −0.010…−0.023; −0.002…+0.005; ≤ 0.001 | −0.007…+0.001; ≤ 0.001; ≤ 0.002 |
| γ* = 1.6, B* ∥ z, k_B = 2 / 4 / 8 / 12 | +0.014/+0.007/+0.064/+0.028; +0.006/+0.017/+0.038/+0.027; +0.003/+0.014/+0.015/+0.016 | +0.007/+0.029/+0.045/+0.030; +0.003/+0.022/+0.021/+0.023; −0.002/+0.016/+0.005/+0.011 |

- In the reduced problem B* changes c by amounts of the observed size (up to +0.02-0.06), positive at k_f ≥ 4 for γ* ≳ 1.5
  or B* ∥ E*. It is erratic in sign at γ* = 1.3 (mostly negative at k_f = 2) and absent at γ* = 1.1.
- **E2's fix pass** (NUMERICS §12.1, FIX1.json) settles the origin in full events:
  - 39/40 events per mass reach max_boost 10⁻⁴. c is step-converged at 10⁻³ (≤ 0.001).
  - The B₀/20 excess persists: +0.0122 ± 0.0027 (500 GeV), +0.0130 ± 0.0035 (1 TeV), positive in 90-97 % of events.
  - Replicas with perturbations of 10⁻¹⁴-10⁻⁸ shift c by ≤ 5×10⁻⁴: the excess is deterministic.
  - It grows with k_B: at 500 GeV, Δc(1/20) = +0.001/+0.007/+0.014/+0.047/+0.096 for k_B < 3/3-5/5-7/7-10/> 10 (r = 0.74).
  - It is absent at 1 keV for the same k_B distribution (|Δc| ≤ 0.004).
  - For k_B < 5 and γ* < 1.3 the converged c agrees with E1 to ≤ 0.003 at all f (≤ 0.001 at B₀/2, B₀/4).
- **Verdict on A1: explained qualitatively, quantitatively open.** The 3 keV weak-field excess is the physical B* effect
  of §6.4. It is carried by k_B ≳ 5 events, depends on ε⊥ (present at 3 keV, absent at 1 keV) and does not cancel in B
  ratios because the B* change of η is ε-dependent.
- c14 (the reduced problem) gets the right size and, at large γ* or B* ∥ E*, the right sign. It does **not** reproduce
  the ε dependence seen in full events: its γ* = 1.6 effect is just as large at the 1 keV-like ε, whereas full events show
  none at 1 keV. So c14 is not a quantitative predictor. A likely reason is the full-event geometry, which the
  fixed-geometry CM runs lack: the B* direction relative to the orbit plane and E*, the CM shake by B*, and the
  accumulation over many periods.
- **Remaining open part, with size:**
  - (i) The B*-driven change of c at weak field for k_B ≳ 5 at 3 keV: population +0.012-0.013 (+14 % of c) at B₀/20,
    +0.003 at B₀/4 (1σ), +0.001-0.002 at B₀/2 (< 1σ).
  - (ii) A residual for k_B < 5, γ* < 1.3 at B₀/20: +0.0026 ± 0.0014 / +0.0030 ± 0.0006 (≈ 3 %). About +0.001 of it matches
    the floor-related drift of the pure-E* reference in c14 (c₂₀ − c₂ = +0.0007-0.0012); the rest is open.
  - (iii) The low-γ* residual that c14 could not explain was largely numerical: E2's per-pair γ* < 1.2 residual drops from
    +0.25 to +0.03 ε⊥ with finer steps (NUMERICS §12.4(iii)).
- **Impact on the headline law at the nominal field B₀:**
  - The law Δs_B ∝ ε_B[ln(1/ε_B) + C] and its local slope c are statements at B₀.
  - At B₀ the B* effect changes the population per-pair rotation by −1.15 ± 0.36 % (FU3, converged), i.e. Δs_B by ≈ −1 %;
    the γ* > 1.35 tail shifts by −4…−9 %.
  - c at B₀ is verified at 1 keV (≤ 1.5 %) and at 3 keV through B₀/2 (+0.0017 ± 0.0021, 2 %).
  - Only the weak-field response at Λ ≳ 3 keV (B ≤ B₀/4), not used at a collider, carries the open B* term.
- **Status:** P-14: k_f = 2 consistent; k_f ≥ 4 altered by B* for k_B ≳ 5 (origin explained, size not predicted).

### 9.4 Other follow-ups (E2 FU2, FU3)
- FU2: K_vac(γ* → 1) = 0.0791 ± 0.0003 (Â fixed to E1's formula, b/ℓ_max ≤ 10⁻⁴) vs 3 ln 2 − 2 = 0.0794: confirmed. Vacuum
  constants at γ* = 1.3/2/3: −0.158/−0.560/−0.965. E2's blind "L → ℓ_max, K → 0" was a free-slope fit artefact.
- FU3: odd-crossing residual vs the pure-E* law, per pair: production +0.53/+0.26/+0.08/−0.50/−1.11 ε⊥ in γ* bins
  1.0-1.1/1.1-1.2/1.2-1.35/1.35-1.6/> 1.6; step-converged (20 events) +0.03/+0.04/−0.05/−0.59/−1.16; all events relative per
  pair: −1.15 ± 0.36 % (converged), +0.3 % (production). The low-γ* positive part is numerical; the high-γ* negative part is
  physics, consistent with the B* effect (§6.4).
- FU1b, sensitivity: a 10⁻¹⁴ perturbation of the initial momenta changes Δs by the round-off amounts above at 3 keV and by
  ≤ 3.5×10⁻⁴ at 1 keV. Deterministic propagation through the non-chaotic, J-resetting map would give ~N·10⁻¹⁴ ln(10¹⁴) ~
  10⁻¹⁰ (reviewer C4), so the replicas sample round-off realisations: numerical, not chaos. At the nominal field this is
  ≤ 0.15-0.3 % of Δs (negligible); it does not explain the 3 keV excess (above). Physical analogue (flux-tube
  randomisation of the head-on even crossings at b < 1/Λ) would be of similar size: CONJECTURE.
- E2 FIX1 §12.4(ii): T3's per-event B-only thickness is reproduced exactly (ratio 1.000, 432 events). The 5-20 % median
  offsets are 1-2.5σ event-draw fluctuations of 60-event samples. Closed.

### 9.5 Li/exact thickness at γ* = 2: a failed prediction
Prediction (§4.4): η_KL/η_NG = (Â_KL/Â_NG)(b_KL/b_NG)(L_η,KL + K_KL)/(L_η + K) = 0.38 × 1.68 × 0.79 = 0.50. Measured (E2 FIX1,
converged Li, 30 events, γ* = 2): 0.75 ± 0.08 (p16-p84 0.55-1.15); R2: 0.69. **Failed at 3σ.** Candidate causes, none
quantified:
- (a) **B* in the exact string.** At γ* = 2 the NG η is reduced by 7-21 % for k_B = 4-16 (§6.4); the KL/Li response to B* was
  not measured. A B*-free Li would raise the ratio to ≈ 0.54-0.63: right direction, not enough alone.
- (b) **Δs ∝ η fails at γ* = 2.** The rotating yo-yo is +17 % (median) off for the exact string there (§5.1), because the
  rotation is spread over the half-period; the Li string's spread need not be the same.
- (c) **The Kang-Luty b_odd ratio** (1.68) was measured only in the CM reduced problem; Li's lab integration (ŝᵢ = Δr − Δt vᵢ,
  CM simultaneity with a drifting CM) may differ. Inside the logarithm the ratio enters as −ln 1.68 = −0.52; the linear factor
  dominates.
The structural statements (log present; c within ≈ 3 % of NG, E2 M5) are unaffected. The size ratio at γ* ≳ 2 is not
predicted correctly.

## 10 Open issues / where I am unsure
1. **c at 3 keV for k_f ≥ 4** (MEDIUM; not needed at B₀): origin explained (physical B* effect, k_B ≳ 5 events, E2 FIX1);
   size not predicted (+0.012-0.013 at B₀/20); c14 has the size but not the ε dependence; a ≈ 3 % residual for k_B < 5 at
   B₀/20 is open.
2. **B* effect (MEDIUM):** measured, not derived. Non-monotonic in k_B, ε-dependent. The per-event c_ev fails for k_B ≳ 6
   (5-43 % of events depending on m). An analytic inner-region theory with B* is needed for event-level predictions at
   large k_B (or at least a k_B-binned empirical correction).
3. **Relativistic K(γ*)** (LOW for c, ≤ 1 %): numerical (two solvers), no closed form.
4. **Accumulation at γ* > 2** (MEDIUM; 0-16 % of events): the model is 10-35 % off. Delocalisation and B* are not separated.
5. **Non-secular first-order terms** (LOW-MEDIUM): b_odd offsets and the static tilt are omitted. They scale as Λ⁻⁴ and
   matter at Λ ≲ 0.6 keV.
6. **Li/causal thickness ratio at γ* = 2: FAILED** (0.50 vs 0.75 ± 0.08, 3σ; §9.5). Not used elsewhere.
7. ~~Model medians vs T3 medians~~ **Closed** (E2 FIX1: event-draw fluctuations; T3 reproduced per event).
8. **Multiple scattering connection** (scope, §11): CONJECTURE.
9. **Solver lineage** (LOW-MEDIUM): one-solver items listed in §9; an Athena C++ standalone comparison would be the
   strongest third check.
10. **Proposed edits outside analytic/** (T2 erratum, synthesis wording, S_Bscan floor): `analytic/PROPOSED_CHANGES.md`,
    not applied.

Decisions flagged: (i) c is defined as the local log slope of the thickness law (§5.3); (ii) population numbers come from
the rotating-yo-yo model on the T3 sample, not from an analytic average over the DY spectrum (MEDIUM).

## 11 P1 scope options (decision for the user; not decided here)
The constructive review (B2) notes that the working title promises multiple scattering and "exact string dynamics", while
the MS mechanism here is a CONJECTURE (§6.3 of v3: a kick gives angular momentum J₀, and the vacuum per-crossing law
then rotates the axis at every crossing).
- **(a) Derive the MS part analytically.** Use the verified vacuum law ψ = Â(b/ℓ_max)[ln(ℓ_max/b) + K_vac] (P-19) with
  b = |J|/p* after a kick δp at separation x: J ≈ x δp/2.
  - Needed: (1) the single-kick response Δs(δp, x, γ*) (rotation at both parities, coherent until the next kick),
    tested against T3's single-kick runs [T3 §3.2 item 7];
  - (2) the random-kick ensemble: J performs a random walk; combine with the field-driven J_odd. Predict whether the log
    shifts the MS √(x/X₀) exponent (0.5 vs the measured ≈ 0.52);
  - (3) the interplay with the B-field rotation (both act on the same axis).
  - Cost (ESTIMATE): 1-2 weeks analytic plus a few days of causal runs with material (T3 code exists). Risk: random J
    near zero at many crossings brings in the log-sensitive head-on regime (§9.4).
- **(b) Narrow P1 to the B-field crossing physics.** Title e.g. "Log-enhanced plane rotation of quirk pairs in a
  solenoid", with MS as the measured numerical floor (T3/S-2: 10-25 µm), stated as such and credited to the existing
  numerics; MS theory as future work or a companion note.
- In both cases replace "exact" by "classical Nambu-Goto". Option (b) is ready now; option (a) adds a result but also
  risk.

## 12 Response to review S1-R1
| Finding | Resolution | Where |
|---|---|---|
| Crit. A1 (3 keV round-off attribution refuted) | Round-off, positive-definiteness, "verified to 2-3 %", "Λ dependence confirmed" and the clean-ratio criterion withdrawn. With E2's converged, unbiased runs (39/40 events at 10⁻⁴) the excess is deterministic and tracks k_B: a physical B* effect, explained qualitatively; size not predicted (c14 gets the size, not the ε dependence). Impact at B₀: ≈ −1 % on Δs_B | §0 item 5, §9.3, P-14, §10.1, predictions.json |
| Crit. A2 (stale statements) | Clean rewrite: "B* inert" now restricted to linear dynamics/b_odd everywhere; "K depends on γ* only" restricted to pure E*; round-off numbers taken from FU.json; NUMERICS stale lines are E2's (fix in progress there) | §1.1, §1.2, §1.4, §4.1, §9.3, predictions.json |
| Crit. B1 (B* mis-characterised) | Rewritten with ε- and k_B-dependence, reviewer's −2.6 % (γ* = 1.3, k_B = 8) and ratios; "enters K, not G" withdrawn; per-event c +17…+36 % at k_B = 8-12; event fractions; population c uncertainty from 1 keV agreement | §6.4, P-22, P-10 |
| Crit. B2 (headline parametrisation) | Headline is Δs ∝ ε_B[ln(1/ε_B) + C], C = 0.43/1.23/1.62; c = local log slope; literal form gives 0.944 (confirmed) and is withdrawn | §0 item 4, §5.2, §5.3, P-9, P-10 |
| Crit. B3 (tags) | c_ev "DERIVED under the rotating-yo-yo assumption; population median VERIFIED-NUM at 1 keV"; reduction "exact for linear dynamics"; "linear before the first crossing (first order exact there)"; 3 keV status per A1 | §1.4, §3.3, §5.3, §8 |
| Crit. C1 (Eq.III.12 wording) | "has the scaling of b_odd"; numerical 22 µm vs 3.5 µm added | §3.2 |
| Crit. C2 (Knapen Eq.8) | Re-evaluated at their benchmark; Eq.8 6.1×10⁻⁵, Eq.9 1.6×10⁻⁶ vs η 8.9×10⁻⁵; "10-15×" withdrawn | §5.2 |
| Crit. C3 (E3 apsidal) | Closed: Â_NR = 1 | §4.3 |
| Crit. C4 (determinism estimate) | Adopted: numerical, not chaos | §9.4 |
| Crit. C5 (fine FU3 residual) | −1.15 ± 0.36 % quoted next to +0.3 % | §6.4, §9.4 |
| Crit. C6 (c12 docstring) | Fixed: c12 uses the relative coordinate only | checks/c12 |
| Crit. C7 (KLN vs Kang-Luty) | "Kang-Luty" throughout E1; mapping in notation table | §1.1 |
| Crit. C8 (NUMERICS k = 20 rise) | E2's file; mentioned in §9.2 row 12 | §9.2 |
| Constr. B1 (framing) | §0 and §5.2 lead with the log-enhanced rotation and the Δs law; c is a derived slope | §0, §5 |
| Constr. B2 (title/scope, MS) | Not decided: options in §11 | §11 |
| Constr. B3 (Δs definition, in/out-of-plane) | Defined in §1.3; in/out-of-plane response equal within 1 % from existing data | §1.3 |
| Constr. B4 (accuracy per γ* bin) | Table with event fractions | §5.1 |
| Constr. B5 (solver independence) | Lineage stated; two-solver vs one-solver list | §9 intro |
| Constr. B6 (discrepancies) | (a) §9.3: B* origin, size open; (b) Li/exact at γ* = 2: FAILED, diagnosed §9.5; (c) T3 offset = event-draw fluctuation (closed); (d) low-γ* residual numerical (+0.25 → +0.03 ε⊥) | §9.3-9.5, §10 |
| Constr. B7 (\|q\| = 2, scalar) | Formulas and population numbers; inputs stated | §6.5, P-24 |
| Constr. B8 (crossing angle) | No free near-miss angle; α and φ*; f_N formula; quantitative Δs vs f_N, sin α | §6.3, P-23 |
| Constr. B9 (notation) | Binding table | §1.1 |
| Constr. B10 (§0 for phenomenologists) | Rewritten | §0 |
| Constr. B12 (Knapen, Li wording) | Corrected; Li's A.17 "consistent with ~ at the factor-3 level" | §5.2 |
| Constr. B13 (upstream cascade) | `analytic/PROPOSED_CHANGES.md` (not applied) | file |
| Constr. C1 | Claim region stated in §0 item 6 and §7 | §0, §7 |
| Constr. C2 (credit sentences) | All ten NOVELTY_AUDIT §4 sentences mapped in §13 | §13 |
| Constr. C3 | E2's file | — |
| Constr. C4 (initial conditions) | §1.5 | §1.5 |
| Constr. C5 (b_odd conditions) | §0 item 2, §3.2 | §0 |
| Constr. C6 (ε clash) | glueball probability → ε_gb; field ε⊥, ε_B | §1.1 |
| Constr. C7 (length, audit trail) | v1-v3 remarks removed from the main text (history in v3 file and predictions.json); appendix split deferred to the P1 draft | whole note |
| Constr. C8 (figure style, σ-only) | σ-only dependence stated (§1.5); figure style noted for the plotting stage | §1.5 |

## 13 References opened, and credit
- 0805.4642 (Kang-Luty): Eq.3.7-3.10 (endpoint EoM; straight-string remark and "useful to check by direct simulation",
  §3.2); §5.8 Eq.5.64 (separation after one oscillation ∝ v_cm B m/Λ⁴).
- 1911.02223 (Li et al.): Eq.III.6-III.12.
- 2002.07503 (Li et al.): §V Eq.V.1-V.9; App.A Eq.A.1-A.17; App.B; App.C Fig.8; §V.A/Fig.4 (charge linearity).
- 1708.02243 (Knapen et al.): §II Eq.5-9, Fig.3 (opened in the text cache; Eq.8 evaluated in §5.2).
- NOVELTY_AUDIT.md (E3) §0, §3-4; `novelty_sources/E3_apsidal_check_out.txt`.
- Review files: `review/CRITICAL_REVIEW_S1_R1.md`, `review/CONSTRUCTIVE_REVIEW_S1_R1.md`.
- Theory-track inputs: BRIEF; synthesis §0.1, S-1, S-3, X-2, X-3, X-13, §5; T2 §2, §5-6; T3 §3; T4 §3; code T3_causal.py,
  R1_conformal_ng.py, T2_propagator.CausalNullString, T2_crossing_missdist.py, S_Bnonlin.py/S_Bscan.py, R1_Blinearity.py.
- **Credit sentences (NOVELTY_AUDIT §4) and where they appear:**
  1. Kang-Luty Eq.5.64 scale → §3.2.
  2. Li et al. per-period rotation η (A.6, A.17, V.5-V.6, B.9) → §0 item 4, §1.2, §5.2.
  3. The log is not a retardation/curvature effect; Li integrators have it → §4.4 (confirmed by E2 M5).
  4. Li charge linearity, ≈ 7 % → §6.5.
  5. Knapen m-independent ∝ B/Λ² plane rotation → §5.2.
  6. Li App.C (D_N/D_A within an order of magnitude, Fig.8) and App.A after A.13 → §3.2, §3.3. Li et al. showed their
     analytic thickness agrees with their numerical one only within an order of magnitude [2002.07503 App.C, Fig.8], and
     their published reach uses the numerical thickness.
  7. MS credit (Knapen §II, Li 2108.06748 §4.1, FASER Geant4 EM) → belongs to the MS part (§11).
  8. Causal string = classical NG with point ends built from null segments: Artru [Phys. Rept. 97 (1983) 147] and the Lund
     model [Phys. Rept. 97 (1983) 31] (UNVERIFIED, not opened by E1), implemented for quirks in the ATLAS Athena Geant4
     extension by J. Black and T. Nelson [Athena `Simulation/G4Extensions/Quirks`; 2607.26195 App.A, acknowledgements].
  9. Kang-Luty's call for a direct check [0805.4642 §3.2] and Evans-Luty's neglect of retardation [1811.08903 §2]; this note
     shows where retardation enters (the coefficient 1/artanh β*, §3.4) → §4.4.
  10. Classical strings with massive charged ends in constant fields were solved only for motions linear in the endpoint
      proper time [Barbashov et al., JINR-E2-10626 (1977)], which in 3+1 dimensions reduce to uniform rotations [Petrov,
      Sharov, TMP 109 (1996) 1388] (as cited by E3; not opened by E1). The field-driven yo-yo with a near miss is outside
      that class.
