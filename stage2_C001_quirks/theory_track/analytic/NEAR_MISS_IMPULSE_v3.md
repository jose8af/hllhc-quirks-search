# Near-miss impulse and B-field plane thickness of a quirk pair (E1, Stage 1 / P1)

Status: v3 (2026-10-10): v2 + §9.3 (E2 follow-ups FU1-FU3) and the B* correction (§1.3, P-22, §10.11-14). For review. Every formula has a derivation here or a
check script in `analytic/checks/` (outputs `*_out*.txt` next to the scripts). Tags: **DERIVED** (derivation in
this note, checked by sympy and by a limiting case), **VERIFIED-NUM** (a derived formula confirmed by a targeted
exact-NG run), **ESTIMATE** (numerically determined constant or model step), **CONJECTURE**.

## 0 Summary
1. Exact reduction: in the pair rest frame the lab B is a uniform E* = γβ×B; B* is inert at first order (§1.3).
2. Odd-crossing miss distance b_odd = 2(q|E*⊥|m/σ²)[γ* − asinh ρ/ρ] ≈ 3.5 µm (keV/Λ)⁴ (derived); E2 confirms it to 0.1 %.
   b_even = 0 at first order. Li's d and Kang-Luty's Eq.5.64 estimate b_odd, which is not the thickness (§3.2).
3. First order fails only at odd crossings. The exact NG near miss y = (b/2) artanh(x/t)/artanh β* gives a log impulse near the
   crossing, i.e. a rotation of the axis. The turning-point-to-turning-point transfer has no log (§3.4; E2 confirms κ = β*/artanh β*).
4. Analytic theory of Li et al.'s rotation η: η = ε⊥G(γ*)[ln(ℓ_max/b_odd) + K(γ*)] per period, coherent.
   E2 blind: G to 0.2 %, the per-period constant to ≤ 0.006, vacuum Â = 2(γ*−1)/(ρ artanh β*) to ≤ 1.2 %. K is numerical (NR: 3 ln 2 − 2).
5. A rotating yo-yo (vacuum + η, nothing fitted) reproduces the causal Δs_B to 1-4 % per event for γ* ≲ 1.5.
   Δs_B ∝ (qBR/σ)[L + K]: m-independent, Λ⁻² × log (§5).
6. c = 1/[ln(ℓ_max/b_odd) + K]: 0.104 (pred.) vs 0.105 ± 0.002 (E2) at 1 keV, 500 GeV; 0.100 vs 0.101 at 1 TeV. B exponent 0.914 vs 0.911 ± 0.003.
   Λ exponents −1.79…−1.86 vs E2 mean −1.80. 3 keV: blind 0.093 was step-biased; converged 0.089/0.084 vs 0.085/0.082 (§9.3).
   v3: B* is not inert for η (inner region): −0.2 % at γ* = 1.3 to −7 % at γ* = 2; it explains E2's high-γ* residual; population c ±0.5 %.
7. Straight-string (Li) codes have the log with nearly the same c (E2 M5 confirms); only the size of the log coefficient needs retardation (§4.4).
   DERIVED: items 1-4 except K. ESTIMATE: K and the population numbers. B/1000 comparisons are dropped (precision floor).

## 1 Setup and notation

### 1.1 Units and symbols
- ħ = c = 1, lengths in cm, energies in GeV. Λ ≡ √σ, **σ = 50.68 GeV/cm (Λ/keV)²** [T2 §2.2; synthesis §0.1].
- Unit-charge magnetic force: qB = 2.998×10⁻³ GeV/cm per tesla [`T2_propagator.EB_GEV_PER_CM_PER_T`]. The
  dimensionless field is **ε_B ≡ qB/σ = 2.254×10⁻⁴ (B/3.8112 T)(keV/Λ)²**.
- Pair: equal masses m, charges ±q (quirk 1 carries +q), produced at one point. In the pair rest frame ("CM"):
  each quirk has γ*, β*, **ρ ≡ γ*β***, p* = mρ; ℓ₀ = m/σ; ℓ_max = 2(γ*−1)ℓ₀ (maximal separation); half-period
  (crossing to crossing) T_h = 2p*/σ; period T* = 2T_h [T2 §2.2]. n̂ is the direction of quirk 1 at production.
- χ* ≡ artanh β* (the CM rapidity of each end at the crossing).
- Crossings are numbered k = 1, 2, …; k odd = "odd crossings" (T2 §5.3 convention; Li et al.'s g = 1, 3, …),
  k even = "even crossings" (Li's g = 2n).
- Lab: uniform B = B ẑ (3.8112 T unless stated). Pair velocity β_cm = P/E at production, γ_cm.

### 1.2 Map to Li et al.'s notation [2002.07503 §II, §V, App.A]
| Li et al. | here | relation |
|---|---|---|
| g (time in units of the crossing interval; quirks meet at g = 2n) | k = crossing index | g = k at crossings |
| η: rotation angle of the quirk system per period, "about ê_yc" [Eq.A.6], fitted numerically, r(0.5)\|η\| ~ \|w₁\| ~ d_E [Eq.A.17] | η (§4-5), derived | same object: rotation of the oscillation axis per CM period; ours is the analytic theory of their η |
| z⁻(g) (half relative out-of-plane offset), z⁻_o0 [Eq.A.13] | z/2 (§3.3) | their z⁻_o0 omits the string's transverse pull |
| d_E = z⁻_o0(1) = (2mqE_z/Λ⁴) ρ sinh⁻¹ρ [Eq.V.8] | b_odd/2 (§3.2) | d_E/(b_odd/2) = 3.0-4.2 for γ* = 1.05-3 [c01 (5)] |
| E_z (CM electric field normal to their plane) | E*·N̂ (out-of-plane part of E*⊥) | |
| B_c (CM magnetic field) | B* | B* drops out at first order (§1.3) |
| first term of Eq.V.5-V.6 / B.9 (η² r² Σ(j − [i/2])²/3l₀) | §5 accumulation | secular accumulation of η |

### 1.3 Exact reduction of the problem (DERIVED)
1. The system (NG string with massive point endpoints [0805.4642 Eq.3.7] plus Lorentz forces) is Lorentz covariant.
   A uniform constant lab B is, in the frame moving with the initial pair velocity β_cm, a uniform constant field pair
   **E* = γ_cm β_cm × B**, B* = γ_cm B − (γ_cm − 1)(B·β̂)β̂ (standard field transformation). Solving the problem in
   that frame and boosting back is exact; no simultaneity convention is involved.
2. In that frame the pair starts at the origin with momenta ±p* n̂ and zero total momentum.
3. At first order in the fields, B* acts neither on the relative motion nor on the angular momentum: for x₂ = −x₁,
   v₂ = −v₁, q₂ = −q₁ the magnetic forces on the two ends are equal (q v₁×B*), so they cancel in the relative
   equation and their torque about the CM is (x₁ + x₂)×(q v₁×B*) = 0 [c01 (4)]. B* only shakes the CM (the exact lab
   statement is P(t) = P₀ + q(x₁ − x₂)×B [T4 §3.2], which has zero average over a period).
   **v3 correction (after E2 FU3; §9.3):** this holds for the *linear* (outer) dynamics. In particular B* does not
   change b_odd (checked: c12, B*-only runs give b = 0 and the same b_odd with E*). It is **not** true for the rotation
   η. The rotation is generated in the non-linear inner region of the odd crossing, where the B*-driven common
   transverse motion (whose size is comparable to b) enters. Measured with the exact string (c12): B* ⊥ n̂ changes η
   by an amount *even* in B*, first order overall (independent of ε), vanishing as γ* → 1. For q|B*⊥|/σ = 4ε⊥ it is
   −0.2 % at γ* = 1.3 and −7 % at γ* = 2; B* ∥ n̂ has no effect. So it modifies K event by event, not G.
4. Write E* = E*∥ n̂ + E*⊥ with E*⊥ ⊥ n̂, and **ε⊥ ≡ q|E*⊥|/σ**, ê⊥ ≡ E*⊥/|E*⊥|. E*∥ only makes successive
   half-periods unequal (second order in the rotation, §6.1). So the first-order problem is:
   **a pair produced at rest in a uniform transverse field E*⊥.** It depends on γ* and ε⊥ only (ℓ₀ sets the length
   unit). For a pair moving transversely (|η_pair| < 1) |E*| = γ_cm β_T,cm B and ε⊥ = ε_B γ_cm β_T,cm sin α, where
   α is the angle between E* and n̂ in the CM frame.

## 2 Vacuum yo-yo

- Exact solution [T2 §2.1; 0805.4642 §3.3]: in the CM the motion is one-dimensional along n̂; each end feels the
  constant force σ, so its momentum is a triangle wave of amplitude p*, and the separation in the first half-period is
  **x(t) = 2ℓ₀[γ* − √(1 + (ρ − t/ℓ₀)²)]**, 0 ≤ t ≤ T_h, with x(0) = x(T_h) = 0, x_max = ℓ_max, end speed β* at the
  crossings, and dp/dt = −σ exactly [c01 (1)]. In the next half-period quirk 1 is on the −n̂ side (the quirks pass
  through each other): x(t + T_h) = −x(t).
- The world sheet is the flat region of the (t, x) plane between the two end world lines, a chain of lenses that touch
  at the crossings. At a crossing the string has zero length and the world sheet folds: in conformal gauge a finite
  parameter interval maps onto the crossing point (null, degenerate pieces of the sheet). Transverse data on these
  degenerate pieces become short string bits once the ends miss each other (§3.4).
- **Rigid-rotation lemma (DERIVED).** At a crossing the string has zero length and carries no momentum, so the state
  of the system is fully given by the two end momenta. Rotating both momenta by a small angle δ about an axis
  through the crossing point produces the rotated vacuum solution. Hence a transverse relative impulse Δp⊥ received
  at (or concentrated around) a crossing rotates all later motion rigidly by **δ = Δp⊥/p***.
- Half-period integral used below [c01 (2)]: **I ≡ ∫₀^{T_h} x dt = 2ℓ₀²[γ*ρ − asinh ρ]**.

## 3 Linear response and its breakdown

### 3.1 Torque and angular momentum (DERIVED)
The total angular momentum J of the system (ends + string) about the CM obeys exactly
**dJ/dt = Σᵢ xᵢ × qᵢE* = q (x₁ − x₂) × E***, because the string carries no charge and B* gives no torque (§1.3). At
first order the right side is evaluated on the vacuum yo-yo, r ≡ x₁ − x₂ = x(t) n̂:
- after the first half-period: J(T_h) ≡ J_odd = q|E*⊥| I (direction n̂ × ê⊥);
- after the second half-period: J(2T_h) = J_odd + q|E*⊥| ∫ x dt over [T_h, 2T_h] = J_odd − J_odd = 0, because
  x(t + T_h) = −x(t).
So J oscillates: 0 at production and at every even crossing, J_odd at every odd crossing. This is exactly Li et al.'s
statement that the quirks "meet each other" at g = 2n [2002.07503 Eq.A.4-A.5], now with the value at odd crossings.

### 3.2 Odd-crossing miss distance (DERIVED; VERIFIED-NUM)
At a crossing the string has zero length, so J is carried by the ends: J = |r × p_rel| = b p*, with p_rel the relative
momentum (= p* n̂ at zeroth order). Hence

**b_odd = J_odd/p* = 2 (q|E*⊥| m/σ²) [γ* − asinh(ρ)/ρ] = 2 ε⊥ ℓ₀ [γ* − asinh(ρ)/ρ]**.

- Limits [c01 (3)]: non-relativistic b_odd → (4/3) qE m β*²/σ² (checked against a direct NR computation, μẍ = −σ);
  E → 0: b → 0; m → ∞ at fixed γ*: b ∝ m but b/ℓ_max = ε⊥[γ* − asinh ρ/ρ]/(γ* − 1) is m-independent.
- **Exact NG check** (`c03_causal_E.py`, causal string with a uniform E* in the pair rest frame, γ* = 1.05-3,
  ε = 10⁻⁶-10⁻³): b₁/b_odd = 1.00003-1.0001 at max_boost 10⁻⁴ (1.0002-1.0006 at 10⁻³) for all γ*, all ε.
- Typical size in CMS: for the c06 events (m = 500 GeV, Λ = 1 keV) ε⊥ ≈ 2-15×10⁻⁵, giving b_odd ≈ 1.5-10 µm, median
  ≈ 3.5 µm, in agreement with T2's measured b_odd ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] (that measurement used the lab-frame
  causal string, i.e. it is an independent check of the reduction §1.3).
- **Credit and relation to the literature.** The scale m qB/Λ⁴ of "a separation of classical quirk trajectories
  after one oscillation", Δr ~ (v_cm B/m)(m/Λ²)², is Kang-Luty's [0805.4642 §5.8, Eq.5.64], who used it to argue
  against re-annihilation. Li et al.'s d_E [2002.07503 Eq.V.8] and the thickness formula d ≈ 1.16 µm
  (m/100 GeV)(keV/Λ)⁴(B/T) [1911.02223 Eq.III.12] have the same scaling: d = qB m/σ² × O(1). Li's d_E is
  3.0-4.2 × b_odd/2 [c01 (5)] because their z⁻_o0 [Eq.A.13] integrates the field force without the string's
  transverse restoring pull −σz/|x| (they note the deviation in App.A after Eq.A.13). **So Eq.III.12 describes the
  odd-crossing miss distance (a static/dynamic polarisation of the yo-yo), not the accumulated plane-fit thickness**
  (synthesis X-2), and the exact coefficient is 2[γ* − asinh ρ/ρ] = 0.13/0.73/2.5/4.75 at γ* = 1.05/1.28/2/3 times
  q|E*⊥|m/σ².

### 3.3 Linearised outer equations and where they break down (DERIVED)
- Non-relativistic straight-string form (reduced mass μ = m/2, transverse relative coordinate z along ê⊥, longitudinal
  x(t) from §2): the string force −σ r̂ has the transverse component −σz/|x|, so
  **μ z̈ = −σ z/|x(t)| + q|E*⊥|**.
  Two exact facts: z = θ₀ x(t) solves the homogeneous equation (rigid rotation, μẍ = −σ sgn x), and the Wronskian
  μ(x ż − z ẋ) = J obeys dJ/dt = q|E*⊥| x (the torque law of §3.1). Writing θ ≡ z/x (the angle of r):
  **θ̇ = J(t)/(μ x²)**.
- Relativistic NG form: in static gauge on the flat world sheet the transverse displacement y(t, x) obeys
  y_tt = y_xx, and transverse momentum balance at a moving end x = X(t), Ẋ = V gives the boundary condition
  **dp_⊥,end/dt = ∓σ(y_x + V y_t) + qE*⊥** (− for the right end, + for the left) [derivation: d/dt ∫σ y_t dx between the
  moving ends with Leibniz' rule; c02 (1)]. This is the equation T2 solved by characteristics before the first
  crossing (`T2_transverse_linear.py`) [T2 §5.1].
- **Breakdown.** Near a crossing x ≈ v|s| (s = t − t_k, v = 2β* relative speed in the NR form). The coefficient σ/|x|
  ∝ 1/|s| makes s = 0 a regular singular point: z stays continuous but ż has a log singularity, i.e. the transverse
  impulse ∫σ z_k/(v|s|) ds diverges logarithmically unless z_k ≡ z(t_k) = 0. Equivalently θ̇ = J/(μx²) has a 1/s²
  pole (the π flip of r) whose sub-leading term J σ/(μ²v³|s|) is log divergent.
  - At production z = 0 and J = 0: no singularity. This is why first-order theory is exact before the first
    crossing [T2 §5.1; S_Bnonlin "ratio 1.000 before the first crossing"; R1_Blinearity pre-crossing metric
    2×10⁻⁴-2×10⁻²].
  - At even crossings z_k = J/p* = 0 at first order: no singularity.
  - At odd crossings z_k = b_odd ≠ 0: the linear connection across the crossing is undefined; the true impulse
    depends on b itself, ∝ b ln(1/b) ∝ B ln(1/B). **First-order perturbation theory in the field therefore fails at
    every odd crossing, and only there.** This is the precise form of Li et al.'s remark that z⁻_o and z⁻_o0 differ
    for g ∈ [0.5, 1] [2002.07503 App.A after Eq.A.13] and of the synthesis statement X-3.

### 3.4 The intermediate region of a near miss: exact NG solution (DERIVED)
For b ≪ |x| ≪ ℓ₀ (and |s| ≪ p*/σ) the ends move freely at x = ±v s with v = β* (CM speed of each end) and the
unperturbed world sheet is the wedge |x| < v|s|. The ends are heavy compared with the string piece between them
(σ|x| ≪ mγ*), so to leading order the transverse string field is slaved to the end positions (Dirichlet data
y(s, ±vs) = Y_±(s)). For the constant relative offset Y_± = ±b/2 the solution of y_tt = y_xx on the wedge is the
degree-0 self-similar solution

**y(s, x) = (b/2) artanh(x/s) / artanh(v)**   [c02 (2): solves the wave equation, takes the values ±b/2 at the ends],

and the boundary condition of §3.3 gives the transverse force on the ends

**F_⊥ = ∓ σ b / (2 |s| artanh v)**   [c02 (3)].

- Quasi-static limit v → 0: σb/(2v|s|) = σ × (Δy/separation), the straight-string value [c02 (4)].
- The string is curved (y ∝ artanh(x/s), not linear in x): the 1/artanh(v) instead of 1/v is the retardation effect,
  a reduction by v/artanh v = 0.97/0.85/0.66/0.53 at γ* = 1.05/1.28/2/3 [c02 (5)].
- Degree-1 data (relative transverse velocity) give an s-independent force (no log) [c02 (6)]; free log-periodic
  string modes y = τ^{ik} sin(nπ(χ+χ_v)/2χ_v) (Milne coordinates, k = nπ/2χ_v) give bounded oscillating forces whose
  impulse converges (no log) [c02 (6)]. So **the only log-producing term is the offset b.**
- Integrating the force over the intermediate region on both sides of the crossing, the relative transverse momentum
  p_rel,⊥ = (p_1⊥ − p_2⊥)/2 changes by **Δp_rel,⊥ = −(σ b/artanh β*) ln(L/b) + O(σb)** [c02 (7)], where L is the
  outer length scale (ℓ_max up to an O(1) factor) and the lower cut-off ∝ b is set by the inner (non-linear) region
  |x| ≲ b γ*²/artanh β*, where the slope of y is O(1).
- **Wording made precise after E2 (§9, item 3).** This is the transverse momentum accrued in the intermediate region
  around the crossing (|s| ≲ 0.05 T_h), measured relative to the *incoming* axis. It equals p*δ, i.e. it *is* the
  rotation δ of the relative momentum (rigid-rotation lemma, §2). After the crossing the motion continues along the
  rotated axis while |p_rel| falls to zero at the turning point. So the net transverse momentum change from one
  turning point to the next has **no** logarithm: there only the angular momentum survives, p⊥ = J/[ℓ(1 + σℓ/6m)]
  (§9 item 3). The logarithm ends up in the *direction* of the axis, not in the net momentum transfer.

## 4 Inner near-miss problem and matching

### 4.1 Structure of the result (DERIVED, constant K by computation)
By the rigid-rotation lemma (§2) the impulse of §3.4 rotates the oscillation axis by Δp_rel,⊥/p*, toward +ê⊥ (the
attraction deflects the relative orbit around the CM in the sense of J_odd = n̂ × ê⊥: the end of charge +q swings
toward E*⊥). The log coefficient is fixed by §3.4 and b = b_odd from §3.2; everything else is a pure number that can
depend only on γ* (scale invariance: ε⊥ and ℓ₀ have been scaled out, and E*∥ is second order). Therefore the
rotation of the axis per CM period is

**η = ε⊥ G(γ*) [ ln(ℓ_max/b_odd) + K(γ*) ],   G(γ*) = 2[γ* − asinh(ρ)/ρ] / (ρ artanh β*)**,

with σ b_odd/(p* artanh β*) = ε⊥ G. Equivalently ln(ℓ_max/b_odd) = ln(1/ε⊥) + ln[(γ* − 1)/(γ* − asinh ρ/ρ)]
(the second term is −0.28…−0.17 for γ* = 1.05…3 [c01 (6)]).
- G → 4/3 − 8β*²/45 (NR) [c01 (6)]; G = 1.316/1.245/1.165/1.087/0.953 at γ* = 1.05/1.28/1.6/2/3.
- Limits: ε⊥ → 0: η → 0 as ε ln(1/ε) (non-analytic); E*⊥ ∥ n̂ (α = 0): η = 0 (checked: c03, α = 0 gives exactly
  zero rotation); m → ∞ at fixed γ*: η unchanged (m-independent); B → 0: η/B ∝ ln(1/B) → ∞ slowly.
- **Coherence:** J_odd has the same direction at every odd crossing (it is generated afresh in every period by the
  same torque), so η has the same sign in every period: the rotations add linearly (Θ = Nη), they do not random-walk.

### 4.2 Exact NG constant K(γ*) (VERIFIED-NUM for the log coefficient; ESTIMATE for K)
`c03_causal_E.py`: exact causal string (Athena-type piecewise-null NG, `T2_propagator.CausalNullString`, imported),
pair at rest in uniform E* ⊥ n̂, ε = 10⁻⁶…10⁻³ (three decades), 3-4 periods, axis angle from the apocentres of quirk 1.

| γ* | G | K (max_boost 10⁻³) | K (max_boost 10⁻⁴) | spread of K over ε = 10⁻⁶…10⁻³ |
|---|---|---|---|---|
| 1.05 | 1.316 | +0.071 | +0.056 | ±0.003 |
| 1.28 | 1.245 | −0.041 | −0.049 | ±0.003 |
| 1.6 | 1.165 | −0.170 | −0.175 | ±0.002 |
| 2.0 | 1.087 | −0.304 | −0.309 | ±0.002 |
| 3.0 | 0.953 | −0.569 | −0.569 | ±0.003 |
| → 1 | 4/3 | K_NR = 3 ln 2 − 2 = +0.0794 (§4.3, analytic) | | |

- **The log coefficient is confirmed:** at every γ*, η/(ε⊥G) − ln(ℓ_max/b_odd) is constant to ±0.003 over three
  decades of ε, i.e. the slope of η/ε⊥ against ln(1/ε⊥) equals G(γ*) to ≤ 0.1 % (with the retardation factor
  1/artanh β*; the quasi-static 1/β* would give slopes 1.03-1.88× larger).
- K is small (|K| ≤ 0.6 compared with ln(ℓ_max/b) ≈ 8-14 in CMS), so it shifts c by ≤ 6 %. K approaches the analytic
  NR value as γ* → 1 (0.056 at γ* = 1.05 vs 0.079 at 1). A closed form for the relativistic K(γ*) is not derived (§10);
  the interpolation **K(γ*) ≈ (3 ln 2 − 2) − 0.506 ln γ* − 0.077 ln²γ*** reproduces all five points to ≤ 0.002 [c08].
  Convergence: max_boost 10⁻² → 10⁻³ → 10⁻⁴ changes K by 0.065 → 0.008-0.015; b_odd by 3×10⁻³ → 3×10⁻⁴ → 10⁻⁴.

### 4.3 Non-relativistic closed form (DERIVED)
For a straight string with non-relativistic ends (the γ* → 1 limit of every model) the whole first-order problem can be
solved by matched asymptotics [c05]. Units μ = σ = 1, relative speed at the crossing v₀, ℓ_max = v₀²/2,
b = J_odd/v₀ = (2/3)εv₀².
1. **Outer** (|x| > R, R = matching radius, b ≪ R ≪ ℓ_max): θ̇ = J/x² with x = t(v₀ − t/2), J = ε(v₀t²/2 − t³/6) in
   the first half-period and the mirror image after the odd crossing; integrating over one period with the
   neighbourhood |x| < R of the odd crossing removed:
   I_out = 2b/R + (2b/v₀²)[ln(2v₀²/R) − 1] + O(R/v₀²). The even crossing is regular (J/x² → ε/(2v₀) finite).
2. **Inner** (r < R): exact orbit with angular momentum J = bv₀ in the potential σr; sweep angle between the two
   passages through radius R from the radial action, Δφ = −∂S/∂J, S = 2∫√(v₀² − 2r − J²/r²) dr, to first order in
   the potential (2r ≪ v₀² for r ≤ R): Δφ_in = π − 2b/R + (2b/v₀²)[ln(2R/b) − 1].
3. **Sum** (R drops out): η = Δφ_in + I_out − π = (2b/v₀²)[ln(4v₀²/b) − 2], i.e.

   **η_NR = (4/3) ε⊥ [ ln(6/ε⊥) − 2 ] = (4/3) ε⊥ [ ln(ℓ_max/b_odd) + 3 ln 2 − 2 ]**.

- sympy check of every step and of the R-independence [c05]. Numerical check: the relativistic central-force model at
  γ* = 1.00001 gives K = 0.079448 vs 3 ln 2 − 2 = 0.079442 [c04].
- The L ln(1/L) structure is standard near-radial orbit mechanics in a linear potential: E3's side check finds the
  apsidal angle π/2 + L[0.354 ln(1/L) + O(1)] [`analytic/novelty_sources/E3_apsidal_check_out.txt`; NOVELTY_AUDIT §0].
  The logarithm itself is therefore not new; what is new here is (i) that it is generated only at the odd crossings
  of the field-driven yo-yo, with b fixed by the torque law, (ii) its exact relativistic NG coefficient including
  retardation, (iii) the constant, and (iv) the resulting c.

### 4.4 Does the logarithm need string curvature or retardation? (DERIVED + VERIFIED-NUM)
No. Any model in which the ends attract each other with a force of fixed magnitude σ along the string has the log,
because the transverse component σ b/|x| integrates to ln(1/b). What curvature/retardation change is the coefficient
and, for the Li/Kang-Luty straight string, also b. `c04_straight_E.py` solves the same reduced problem (CM frame,
equal CM times, i.e. Li's CM simultaneity [1911.02223 Eq.III.6] with P = 0; ŝ = unit separation, Li's Eq.III.8-9 with
Δt = 0) with an adaptive 8th-order integrator:

| model | transverse force in the intermediate region | b_odd | K | numbers |
|---|---|---|---|---|
| exact NG (causal) | σb/(2|s| artanh β*) (§3.4) | angular-momentum formula (exact) | table §4.2 | c03 |
| quasi-static central force (relativistic kinematics) | σb/(2β*|s|) | same (central force conserves J) | +0.080/+0.104/+0.210/+0.485 at γ* = 1→/1.05/1.28/2 | c04 'QS' |
| Kang-Luty straight string = Li in the CM frame [0805.4642 Eq.3.8] | σb(1 − β*²)/(2β*|s|) [c02 (5)] | 1.040/1.213/1.680 × the exact b at γ* = 1.05/1.28/2 (the KL force has a non-central term, so the ends' J is not conserved) | +0.05/−0.18/−1.8 (with its own b) | c04 'KL' |

- Consequences: (i) a step-converged Li integrator **must show the same B ln(1/B) non-linearity**, with nearly the
  same c = 1/(ln(ℓ_max/b) + K) (c depends on the model only through K and through ln(b_KL/b), i.e. by a few %); this
  is a prediction for E2's straight-string test. (ii) The *size* of η differs: η_KL/η_NG ≈ 0.97/0.84/0.50 at
  γ* = 1.05/1.28/2 (for ln(ℓ_max/b) ≈ 9.8). R2 measured converged Li/causal thickness ratios 0.97/0.85/0.92/0.69/0.65
  at γ* = 1.05/1.28/1.6/2/3 [synthesis S-1, R2]; the first two agree, at γ* = 2 the prediction (0.50) is lower than
  measured (0.69, single events 0.53-1.36). The deficit of the straight string is therefore mostly the missing
  retardation factor at the crossings plus its non-conservation of angular momentum (ESTIMATE; Li's lab-frame
  extrapolation ŝᵢ = Δr − Δt vᵢ and hit sampling are not modelled).
- So the answer to "is it a curvature/retardation effect?" is: the logarithm no; its coefficient yes (retardation:
  1/artanh β* instead of 1/β*), and the straight-string error grows with β* as observed.

## 5 Accumulation over crossings → Δs, c, exponents

### 5.1 From η to the hits: the rotating yo-yo (DERIVED structure; ESTIMATE as a model)
- By §4.1 the oscillation axis turns by η toward ê⊥ at every odd crossing, coherently. After N_odd(t*) odd crossings
  Θ(t*) = η N_odd(t*). The total in the tracker is small (Θ ~ 10⁻³-10⁻², §5.3), so the rotations stay linear and
  E*⊥ does not change appreciably (Li et al. make the same assumption, "E_z and B_c … invariant because of the small
  η" [2002.07503 App.C]).
- Only the component of the rotation out of the vacuum plane changes the plane fit. In the CM frame the vacuum plane is
  spanned by n̂ and β̂_cm, with normal N̂; the out-of-plane rate is η (ê⊥·N̂) and the in-plane rate η (ê⊥·(N̂×n̂)). For
  B ∥ ẑ and a transverse pair, E*·N̂ ∝ n_z: the out-of-plane rotation needs a longitudinal component of the oscillation
  axis; the in-plane part is the "mostly rφ" B displacement seen by T4 [T4 §3.2] (same η, same logarithm).
- **Rotating-yo-yo model** (`c06_rotating_yoyo.py`): exact vacuum yo-yo in the pair rest frame [T2 §2.1] with n̂
  replaced by n̂ cos Θ + ê⊥ sin Θ, Θ stepping by η at each odd crossing (where the string has zero length, so this is
  the exact zero mode of §2); boosted to the lab; hits at the 10 barrel radii; plane fit through the origin. **No
  parameter is fitted** (η from §4.1 with K from §4.2). The non-secular first-order offsets (b_odd, the alternating
  static tilt ±q|E*⊥|/σ of the half-periods) are omitted.
- **Check against the exact causal string**, event by event (T3_causal, B = 3.8112 T, no material, T3 event sample):

| m [GeV] | Λ [keV] | events | Δs_model/Δs_causal, median (16-84 %) | comment |
|---|---|---|---|---|
| 200 | 1 | 8 | 1.001 (0.978-1.009) | |
| 200 | 3 | 8 | 0.996 (0.985-1.016) | |
| 500 | 0.6 | 8 | 0.989 (0.78-1.02) | 0.98-1.03 for γ* < 1.2; 0.65-0.75 for γ* = 2.6-2.9 |
| 500 | 1 | 12 | 0.995 (0.987-1.156) | 0.98-1.01 for γ* < 1.2; 1.10-1.25 for γ* = 2.2-3.0 |
| 500 | 3 | 12 | 0.973 (0.964-1.236) | 0.96-0.99 for γ* < 1.2; 1.14-1.34 for γ* > 2 |
| 500 | 10 | 8 | 0.982 (0.83-1.15) | outliers 0.43, 0.81 where ε⊥ is 10× below typical (E* almost ∥ n̂) |
| 1000 | 1 | 8 | 0.991 (0.977-1.035) | |
| 1000 | 3 | 8 | 0.967 (0.943-0.993) | |

  [c06 outputs `c06_rotating_yoyo_out_m{200,500,500_b,1000}.txt`.] For γ* ≲ 1.5 (most DY events) the analytic η
  reproduces the exact thickness to 1-4 %. For γ* ≳ 2 the step model is 10-35 % off: for relativistic ends the 1/s
  force of §3.4 acts during the whole constant-speed part of the half-period, so the rotation is not localised at the
  crossing and its timing relative to the layer crossings matters (the per-period η itself is exact, §4.2). Where
  ε⊥ is accidentally small the omitted second-order and non-secular terms dominate.

### 5.2 Why Δs_B is m-independent and ∝ Λ⁻² × log (DERIVED scaling)
In the model Δs is linear in η. Over the tracker the number of periods is N_osc = σR/(2β*p_T) [T2 §2.2] ∝ σ, the
lever arm (the oscillation width) is ∝ ℓ₀ = m/σ, and η ∝ ε⊥ ∝ γ_cm β_T,cm qB/σ. Collecting the lab-time dilation,
the total out-of-plane rotation is Θ_N ~ η N_osc ~ qB R G (L + K)/p* (a bending angle of a momentum p* over R), and

**Δs_B = (qBR/σ) × F(γ*, cos θ*, angles, layer phases) × [L + K(γ*)],   L ≡ ln(ℓ_max/b_odd)**,

with F dimensionless and independent of m and Λ at fixed velocities (it depends on ℓ₀/R only through the sampling of
the oscillation phase by the layers). Hence:
- Δs_B ∝ ε_B R ∝ B/Λ², times the slowly varying [L + K]; this is T4's x_B ≈ 0.5 qBR/σ [T4 §3.2] and the m-independent
  ∝ B/Λ² plane rotation of Knapen et al. [1708.02243 Eq.8-9];
- **m enters only through L and through the γ* distribution.** L = ln(σ/(qB)) − ln(γ_cm β_T,cm sin α) +
  ln[(γ*−1)/(γ* − asinh ρ/ρ)]: at fixed p_T a heavier pair is slower, γ_cm β_T,cm = p_T/M is smaller, L is larger
  by ln(M₂/M₁). The γ* spectrum of heavier pairs also shifts. The model medians (c07, 150 events, Λ = 1 keV) are
  33.5/31.1/29.5 µm at m = 200/500/1000 GeV, the same weak decrease as the causal T3 medians 38/34/32 µm [T3 §3.2].
- Relation to Knapen et al.: their Δφ ~ |τ|Δt²/I is the rotation produced by the CM torque during one half-period,
  i.e. q|E*⊥|/σ × O(1), without the logarithm. In the exact dynamics that rotation alternates in sign between
  half-periods (J returns to 0 at every even crossing, §3.1), which is their observation "Δφ oscillates and slowly
  accumulates" [1708.02243 Fig.3]; the slow secular part is the crossing term, larger by G(L + K) ≈ 10-15.
- Relation to Li et al.'s Eq.A.17 (r(0.5)|η| ~ d_E): with r(0.5) = ℓ_max/2, our η ℓ_max/2 = ε⊥ℓ₀(γ*−1)G(L + K),
  which is ≈ 3 d_E at γ* = 1.28 and L + K ≈ 10. Their order-of-magnitude relation misses the logarithm.

### 5.3 The coefficient c and the response per unit B (DERIVED given §4; numbers ESTIMATE)
Because Δs (and every hit displacement after the first odd crossing) is ∝ η ∝ B[L + K] with L = ln(1/B) + const,
**per event**

**R(f) ≡ Δs(fB)/(f Δs(B)) = 1 + c_ev ln(1/f),   c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)]**,

exactly linear in ln(1/f) (as long as b_odd(fB) > 1/Λ, §7). Writing it as the synthesis' Δs ∝ ε_B[1 + c ln(Λ²/qB)]
(logarithm referred to the operating point) identifies c = c_ev. Explicitly

c_ev = 1 / { ln[σ/(qB)] − ln(γ_cm β_T,cm sin α) + ln[(γ*−1)/(γ* − asinh ρ/ρ)] + K(γ*) },

with ln[σ/(qB)] = 8.397 + 2 ln(Λ/keV) − ln(B/3.8112 T). Typical terms at Λ = 1 keV, 3.8 T, m = 500 GeV:
8.40 + 1.5 (γβ_T ≈ 0.23) + 0.2 (sin α ≈ 0.8) − 0.26 − 0.05 ≈ 9.8 → c ≈ 0.10.
Population values from the T3 event sample (c07, 150 events per mass; median and 16-84 %):

| m [GeV] | Λ = 0.6 | 1 | 2 | 3 | 5 | 10 keV |
|---|---|---|---|---|---|---|
| 200 | 0.128 (0.122-0.136) | 0.113 (0.108-0.120) | 0.098 | 0.091 (0.087-0.095) | 0.083 | 0.074 (0.072-0.077) |
| 500 | 0.116 (0.109-0.126) | **0.104 (0.098-0.112)** | 0.091 | 0.085 (0.081-0.090) | 0.078 | 0.070 (0.068-0.074) |
| 1000 | 0.111 (0.105-0.120) | 0.100 (0.095-0.107) | 0.088 | 0.082 (0.078-0.086) | 0.076 | 0.068 (0.066-0.072) |

**Comparison with the fitted numbers (not used anywhere above):** the synthesis fitted c ≈ 0.08-0.11 and the response
"1 + 0.10 ln(B₀/B)" at m = 500 GeV, Λ = 1 keV [S-3, X-3]. The derived median c = 0.104 is inside that range.

Response per unit B at m = 500 GeV, Λ = 1 keV (median of the event-wise R(f), c07) vs measured:

| f | predicted R(f) | measured (S: T4 kernel; R1: conformal solver) |
|---|---|---|
| 1/4 | 1.144 | 1.15-1.19 (S); 1.14 (R1) |
| 1/20 | 1.311 | 1.32-1.38 (S); 1.31 (R1) |
| 1/80 | 1.455 | 1.45-1.51 (S) |
| 1/1000 | 1.718 | ~~1.83 (S_Bscan, 3 events)~~ floor-affected, not testable (E2 §1.3) |

The effective exponent over B/80…B is ln(1.455)/ln 80 = 0.086, i.e. **Δs ∝ B^0.914**, vs T4's measured B^0.91
[T4 §3.2]. (v1 also compared B/1000 with S_Bscan's 1.83; withdrawn after E2, because that point is at the
double-precision floor of both solvers, §9 item 8.) E2's blind measurement: 1.073/1.147/1.320/1.460 at
B/2…B/80 and B^0.911 ± 0.003 (§9 rows 15, 18).

### 5.4 Local exponents (DERIVED per event; population numbers ESTIMATE)
Per event, from §5.2-5.3 (only L depends on Λ and B; L ∝ ln σ − ln B):
- **d ln Δs_B / d ln B = 1 − c_ev**;
- **d ln Δs_B / d ln Λ = −2 + 2 c_ev**;
- d ln Δs_B / d ln m = 0 at fixed velocities and fixed p_T/M; at fixed p_T, +c_ev (via ln M in L) plus the effect of
  the γ* spectrum.
Population (median Δs of the rotating-yo-yo model on 150 events, c07): local Λ exponents for m = 500 GeV are
−1.79 (0.6→1), −1.86 (1→2), −1.78 (2→3), −1.87 (3→5), −1.84 (5→10) keV; averaged over 1→3 keV −1.83 and over
3→10 keV −1.85 (m = 200 GeV: −1.86, −1.75; m = 1000 GeV 1→3: −1.86). The per-event formula gives −1.79, −1.83,
−1.86 at 1, 3, 10 keV. The scatter of the local population exponents (±0.1) comes from the layer sampling of the
oscillation phase, not from the physics. **Measured** (causal, 60 events): 1.76-1.92 (1→3 keV) and 1.63-1.98
(3→10 keV), median ≈ 1.9 [T3 §3.2; synthesis S-3]: consistent. The model's medians are 5-20 % below T3's causal
medians (31 vs 34 µm at 1 keV, 4.2 vs 4.9 at 3 keV, 0.45 vs 0.58 at 10 keV for 500 GeV): different event draws and the
omitted non-secular terms; the event-by-event check (§5.1) is the cleaner test.

## 6 Odd vs even crossings, γ*, angle

### 6.1 Even crossings (DERIVED at first order; second order ESTIMATE)
- At first order J = 0 at every even crossing (§3.1), so b_even = 0 and the near-miss (logarithmic) impulse is absent.
  **Clarified after E2 (§9 item 4):** the even crossing does carry a *smooth, non-logarithmic* rotation. The field
  torque turns the axis while J grows from zero (θ̇ = J/μx² in §3.3). Measured from turning point to turning point
  across the even crossing, NR theory gives ψ_even = (2/3 + (4/3) ln 2) ε⊥ = 1.591 ε⊥ [c09], and E2 measures 1.61-1.70 ε⊥.
  The odd crossing carries the log plus a non-log offset of nearly opposite sign; in NR its constant is
  (4/3) ln 3 − 10/3 = −1.869 [c09]. This alternating ±O(ε⊥) term is the half-period torque rotation that Knapen et
  al. estimated [1708.02243 Eq.8-9]. It almost cancels over a period. Its remainder is part of K (η is defined per
  period), so the accumulation formula already contains it. "No first-order impulse" in v1 meant no near-miss impulse.
- At second order: (i) E*∥ makes the two half-periods unequal, so ∫x dt over a period ≠ 0; c03 at α = 45° gives
  b_even/b_odd ≈ 12 ε∥ (0.0012/0.0028/0.0075 at ε = 10⁻⁴/3×10⁻⁴/10⁻³), i.e. b_even ∝ ε∥ε⊥; (ii) the rotation by η
  at the odd crossing changes the lever of the torque in the next half-period, b_even ~ η b_odd. Both give
  b_even/b_odd ~ 10⁻³-10⁻⁴ in CMS, so the even-crossing impulse is O(ε² ln ε) and negligible for Δs_B.
- **Numerical caveat found here:** with E* ⊥ n̂ (where the second-order sources vanish) the causal code gives
  b_even/b_odd = 2.6×10⁻³ / 3×10⁻⁴ / 2.7×10⁻⁵ at max_boost 10⁻² / 10⁻³ / 10⁻⁴, i.e. ∝ max_boost: a splitting
  artefact of the first-order field kick. T2's even-crossing values (16-31 Å at 1 keV with max_boost 10⁻³ [T2 §6.3])
  are of the same order as both the artefact (~10 Å) and the physical E*∥ term (~20 Å); they are not converged. This
  matters for the ε (glueball) discussion of T2 §6.3, not for the thickness.
- Sign pattern: every odd-crossing impulse has the same sign (toward E*⊥), so they accumulate coherently (∝ N). Even
  crossings carry no near-miss impulse, only the smooth +1.6 ε⊥ torque rotation above, which repeats identically every
  period. There is no random-walk component in B-only propagation.

### 6.2 γ* dependence
- b_odd ∝ γ* − asinh ρ/ρ (0.066/0.364/1.24/2.38 at γ* = 1.05/1.28/2/3); G(γ*) falls from 4/3 to 0.95 at γ* = 3
  (retardation); K(γ*) from +0.08 to −0.57; c_ev depends on γ* only through ln[(γ*−1)/(γ*−asinh ρ/ρ)] + K
  (−0.23 → −0.74 for γ* = 1.05 → 3), i.e. c rises by ≈ 5 % from γ* = 1.05 to 3 at fixed ε⊥.
- The accumulation model is accurate for γ* ≲ 1.5 and 10-35 % off for γ* ≳ 2 (§5.1).

### 6.3 Angle (definition and dependence)
- Define α as the angle between E* (= γ_cm β_cm × B, in the pair rest frame) and the initial axis n̂. Only
  ε⊥ = (q|E*|/σ) sin α enters at first order; E*∥ = |E*| cos α is second order (c03: α = 0 gives zero rotation; α = 45°
  gives the same K as α = 90° for ε ≲ 3×10⁻⁵).
- The rotation is toward ê⊥; its out-of-plane part, which makes the thickness, is η ê⊥·N̂, with E*·N̂ ∝ n_z for a
  transverse pair: pairs whose CM axis is perpendicular to B (n_z = 0) rotate within their plane and get a much smaller
  B thickness (they are the low tail of the Δs distribution; the 16 % quantile of the model is ≈ 0.3 × the median).
- Non-zero initial angular momentum J₀ (e.g. from a multiple-scattering kick): then both crossings have
  b = |J|/p* ≠ 0 and the axis precesses at every crossing even in vacuum, by the same law σb/(p*χ*)[ln(ℓ_max/b) + K_vac].
  E2 measured this (M2a). In E2's normalisation the coefficient is Â = 2(γ*−1)/(ρ artanh β*) and K_vac = ln(L/ℓ_max).
  In NR, K_vac = 3 ln 2 − 2 (c09, c10) (§9 item 1). This is the mechanism behind T3's single-kick test (a kick turns into a
  slow out-of-plane rotation of the axis; non-linear in δp because of the log) [T3 §3.2 item 7] (CONJECTURE for the
  quantitative form).

## 7 NG validity
- The classical NG string with point ends describes the flux tube only on scales ≫ 1/Λ = 1.97 Å (keV/Λ). The log of
  §3.4 runs over b ≲ |x| ≲ ℓ_max; if b < 1/Λ the region |x| < 1/Λ is not described by NG and the lower cut-off of
  the log becomes ~1/Λ times an unknown O(1) factor: L → ln(ℓ_max Λ) + K″.
- Odd crossings: b_odd ≈ 3.5 µm (keV/Λ)⁴ (median, m = 500 GeV, 3.8 T) → b_odd Λ ≈ 1.8×10⁴ (keV/Λ)³, which reaches 1
  at Λ ≈ 26 keV (≈ 12 keV for the 10 % of events with ε⊥ ten times below typical). Even crossings are below 1/Λ
  already at a few keV, but they carry no first-order impulse (§6.1), so they do not matter for Δs_B.
- Model uncertainty on Δs_B (ESTIMATE): zero for b_odd Λ ≫ 1 (Λ ≲ 10 keV); for b_odd Λ < 1 the relative uncertainty
  is ≈ c_ev [ln(1/(b_odd Λ)) + O(1)]: ≈ 3-8 % at 30 keV, ≈ 10-25 % at 100 keV. This replaces the synthesis'
  "10-30 % for Λ ≳ 10-20 keV" [S-3], which was too pessimistic at 10-20 keV. By then Δs_B ≪ Δs_MS anyway [T3 §3.2].
- Below the NG cut-off b no longer appears in L, so the response becomes linear in B (c → 0 in the B scan) while
  the Λ dependence becomes ∝ Λ⁻² ln(ℓ_max Λ), i.e. d ln Δs/d ln Λ = −2 − 1/[ln(ℓ_max Λ) + K″] (CONJECTURE).
- Other conditions used: ε⊥ ≪ 1 (linear rotation; ε⊥ ~ 10⁻⁴ at 1 keV); the ends heavy compared with the string piece
  in the intermediate region (σ|x| ≪ mγ*, true for |x| ≪ ℓ₀); classical motion (quantum numbers ~10¹⁶ [T2 §6.1]).

## 8 Predictions table
All at B = 3.8112 T, truth level, B only (no material), T3 event sample (|η_pair| < 1, LO DY+ISR), unless stated.
Machine-readable version: `analytic/predictions.json`.

| # | Quantity | Prediction | Status |
|---|---|---|---|
| P-1 | Odd-crossing miss distance | b_odd = 2 ε⊥ ℓ₀ [γ* − asinh ρ/ρ], ε⊥ = q\|E*⊥\|/σ; median ≈ 3.5 µm (keV/Λ)⁴ at m = 500 GeV | DERIVED, VERIFIED-NUM (≤ 10⁻⁴) |
| P-2 | Even crossings | b_even = 0 at first order; ≈ 12 ε∥ b_odd at second order | DERIVED / ESTIMATE |
| P-3 | Transverse force in the intermediate region | σ b/(2\|s\| artanh β*) per end (exact NG); quasi-static σb/(2β*\|s\|); Kang-Luty σb(1−β*²)/(2β*\|s\|) | DERIVED |
| P-4 | Per-crossing (= per-period) axis rotation | η = ε⊥ G(γ*) [ln(ℓ_max/b_odd) + K(γ*)], G = 2[γ* − asinh ρ/ρ]/(ρ artanh β*) | log coefficient DERIVED + VERIFIED-NUM (0.1 %); K ESTIMATE (exact-NG numerics) |
| P-5 | K(γ*) | +0.079 (γ*→1, = 3 ln 2 − 2, DERIVED), +0.056, −0.049, −0.175, −0.309, −0.569 at γ* = 1.05, 1.28, 1.6, 2, 3; fit (3 ln 2 − 2) − 0.506 ln γ* − 0.077 ln²γ* | ESTIMATE |
| P-6 | NR closed form | η_NR = (4/3) ε⊥ [ln(6/ε⊥) − 2] | DERIVED |
| P-7 | Sign pattern | all odd-crossing rotations toward +E*⊥ (end of charge +q swings toward E*): coherent, Θ = N η | DERIVED |
| P-8 | Regime of validity of P-4 | ε⊥ ≪ 1; b_odd ≫ 1/Λ (Λ ≲ 26 keV typical; ≲ 12 keV for small-ε⊥ events); first order in ε∥ | DERIVED (conditions) |
| P-9 | c (per event) | c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)] = 1/{ln[σ/(qB)] − ln(γ_cm β_T,cm sin α) + ln[(γ*−1)/(γ* − asinh ρ/ρ)] + K} | DERIVED (given P-4) |
| P-10 | c, population median (16-84 %), m = 500 GeV | 0.116 (0.6 keV), **0.104 (0.098-0.112) at 1 keV**, 0.085 (3 keV), 0.070 (10 keV); m = 200: 0.113 (1 keV); m = 1000: 0.100 (1 keV) | ESTIMATE (model on event sample) |
| P-11 | d ln Δs_B/d ln Λ | per event −2 + 2c_ev: −1.77, −1.79, −1.83, −1.86 at 0.6, 1, 3, 10 keV (m = 500); population medians −1.83 (1→3), −1.85 (3→10) | DERIVED per event; ESTIMATE population |
| P-12 | d ln Δs_B/d ln B at 3.8 T | 1 − c_ev: 0.884, 0.896, 0.915, 0.930 at 0.6, 1, 3, 10 keV (m = 500) | DERIVED per event |
| P-13 | Response per unit B, m = 500, 1 keV | R(1/4) = 1.144, R(1/20) = 1.311, R(1/80) = 1.455, R(1/1000) = 1.718 (**not testable**: B₀/1000 is at the double-precision floor of both solvers, E2 §1.3); effective B^0.914 over B/80…B | ESTIMATE (population of DERIVED per-event law) |
| P-14 | Same, 3 keV | 1.117, 1.253, 1.371 (B/80 not testable), 1.584 (not testable) | ESTIMATE; v2: "c 9 % below E2 (blind, production steps)"; **v3: consistent with step-converged E2 at B₀/2 (§9.3)**; B₀/20 numerically unreliable |
| P-22 (v3, post-hoc) | B* effect on η (CM magnetic field ⊥ n̂) | first order overall, even in B*, → 0 as γ* → 1; −0.2 % (γ* = 1.3), −7 % (γ* = 2) at q\|B*⊥\|/σ = 4ε⊥; −2…−21 % for 2-16 ε⊥ at γ* = 2. Enters K, not G | ESTIMATE (c12, exact string); mechanism CONJECTURE |
| P-15 | m dependence | none at fixed velocities; via ln M in L and the γ* spectrum; model medians 33.5/31.1/29.5 µm at 200/500/1000 GeV (1 keV) | DERIVED scaling; ESTIMATE numbers |
| P-16 | Accumulation model accuracy | rotating yo-yo vs causal: 0.97-1.00 median; 1-4 % for γ* ≲ 1.5; 10-35 % for γ* ≳ 2 | ESTIMATE (c06) |
| P-17 | Straight-string (Li) integrator | has the log and B ln(1/B) with c within a few % of NG; η_Li/η_NG ≈ 0.97/0.84/0.50 at γ* = 1.05/1.28/2 | DERIVED structure; ESTIMATE ratios (c04) |
| P-18 | NG-validity uncertainty on Δs_B | 0 for Λ ≲ 10 keV; ≈ 3-8 % at 30 keV; 10-25 % at 100 keV | ESTIMATE |
| P-19 (implied by P-3; written out after E2) | Vacuum per-crossing law in E2's form ψ = Â(b/ℓ_max) ln(L/b) | Â = 2(γ*−1)/(ρ artanh β*) = 0.992/0.955/0.877/0.802; impulse-profile slope κ = β*/artanh β* = 0.968/0.845/0.658/0.535 (γ* = 1.05/1.3/2/3); Kang-Luty Â = 2(γ*−1)(1−β*²)/(ρβ*) | DERIVED |
| P-20 (post-hoc) | NR vacuum constant; NR odd/even split | K_vac,NR = 3 ln 2 − 2; ψ_even = (2/3 + (4/3) ln 2) ε⊥; ψ_odd = (4/3)ε⊥[ln(1/ε⊥) + ln 3 − 5/2] | DERIVED (c09, c10) |
| P-21 (post-hoc) | Turning-point-to-turning-point transverse momentum | ΔΠ = 2J/[ℓ_max(1 + (γ*−1)/3)] ⇒ ΔΠ/(σb/β*) = ρβ*/[(γ*−1)(1 + (γ*−1)/3)] = 1.920/1.608/1.125/0.800 | DERIVED (assumes a rigidly rotating straight string at the turning point) |

## 9 Comparison with numerics
E2's campaign was blind to this note. Sources: `analytic/numerics/NUMERICS.md` and `numerics/results/{M1,M2,M3,M4,M5,
M13_bridge,M4_conformal_thickness}.json`. My numbers are in `checks/c11_e2_compare_out.txt` (formulas as in v1). Post-hoc
additions are c09, c10 and P-19-P-21. No constant in predictions.json was refitted. E2 uncertainties are their
bootstrap or solver-difference errors. "Pull" = (prediction − measurement)/σ_meas; where σ is negligible a ratio is given.

### 9.1 Per-crossing level (CM-frame controlled runs, M2; full events, M1)
| # | Quantity | E1 prediction | E2 measurement | pull / ratio | source |
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

Point-by-point answers to the coordinator:
1. **Per-crossing law and E2's (Â, L).** E2's M2a law is the *vacuum* law: constant J, the same b at every crossing.
   Its slope is my §3.4 coefficient in E2's normalisation, Â = (σ/p*χ*)·ℓ_max = 2(γ*−1)/(ρ artanh β*). This agrees to
   ≤ 1.2 % (row 2), and the agreement confirms the retardation factor. E2's ln(L/ℓ_max) is the vacuum constant K_vac,
   not my field constant K. The two are related by **K = K_vac + δ_pair/G**, where δ_pair is the per-period non-log
   remainder of the alternating field term (item 4). The cleanest test of K is therefore row 5 (field-driven
   constant per period, measured directly). It agrees to ≤ 0.006, i.e. |ΔK| ≤ 0.005 at every γ*. Through ln(L/ℓ_max) the
   comparison is less precise: E2's fit errors on ln L are ±0.012/±0.04/±0.14/±0.25. The implied δ_pair/G =
   K − ln(L/ℓ_max) = 0.070/0.047/0.27/0.27 vs E2's 0.030/0.105/0.26/0.39. These agree within those errors except at
   γ* = 1.05 (difference 0.04). One discrepancy in E2's text: "non-relativistically L = ℓ_max, K → 0". The NR analytic
   vacuum result is ψ = (b/ℓ_max)[ln(ℓ_max/b) + 3 ln 2 − 2] (c09), i.e. **L/ℓ_max → 8/e² = 1.083**. My straight-string
   vacuum runs give K_vac = +0.070 (free slope) at γ* = 1.0005 (c10). E2's γ* = 1.05 value (−0.015 ± 0.012) comes from
   a fit with the slope free. Their slope is 0.4 % above the analytic one, which over a lever arm ln(ℓ_max/b) ≈ 12
   shifts ln L by ≈ −0.05. I expect the difference to disappear if Â is fixed at the analytic value (LOW; affects c by
   < 0.5 %).
2. **κ vs β*/artanh β*: confirmed** (row 3). The coordinator's quick numbers are right (0.845/0.658/0.535). The 0.5 %
   offset at γ* = 1.05 (2.6σ) is at the level of the profile-fit window systematics. In full events κ = 0.85-0.91 is
   1 % above vacuum (M1), consistent with the γ* mix.
3. **TP-to-TP transfer without a log: consistent, wording fixed** (§3.4 now says so). The log impulse
   (σb/artanh β*) ln(ℓ/b) is accrued within |s| ≲ 0.05 T_h of the crossing. It is a rotation of p_rel by δ
   (rigid-rotation lemma). At the following turning point only the angular momentum survives. With a rigidly rotating
   straight string there (moment of inertia σℓ³/12 added to the ends'), ΔΠ = 2J/[ℓ_max(1 + (γ*−1)/3)]. This
   reproduces E2's 1.92/1.61/1.15/0.79 to ≤ 0.3σ (row 8; post-hoc, but no new parameter).
4. **Even crossings.** Yes: +1.61 ε⊥ is the smooth, non-log torque rotation (the Knapen-like term). In NR it equals
   (2/3 + (4/3) ln 2) ε⊥ = 1.591 ε⊥, derived post-hoc by splitting the outer integral of §4.3 at the turning points
   (c09). The odd-crossing non-log offset is the other half; in NR the pair sum relative to the NR vacuum law is
   exactly zero, and E2's "−(1.3-1.6) ε⊥" is measured relative to their fitted L. This term was already inside K
   (η is per period; row 5 confirms the per-period total). v1's "even crossings carry no first-order impulse" was
   correct for the near-miss impulse but misleading; corrected in §6.1. The full-event residual +0.1-0.2 ε⊥ is
   unexplained (§10). It is non-log, so it enters c only through the denominator. Size ≈ 1-2 % of ψ_pair: it would
   lower c by ≈ 1-2 %.
5. **b_odd = (1.30-1.34) ε⊥ℓ: confirmed.** E2 normalises by ℓ_k ≈ ℓ_max; my closed form gives
   b_odd/(ε⊥ℓ_max) = [γ* − asinh ρ/ρ]/(γ* − 1) = 1.327-1.188 (row 1, ratio 0.999-1.000).

### 9.2 Thickness level (M3 Λ and B scans; M13 bridge; M5)
| # | Quantity | E1 prediction (v1) | E2 measurement | pull / ratio | source |
|---|---|---|---|---|---|
| 12 | c, 500 GeV, 1 keV | 0.104 (event spread 0.098-0.112) | 0.105 ± 0.002 (k = 2-80) | −0.5 | M3.json |
| 13 | c, 1 TeV, 1 keV | 0.100 | 0.101 ± 0.001 | −1 | M3.json |
| 14 | c, 500 GeV, 3 keV | 0.085 | 0.093 ± 0.002 (prod.); 0.085-0.098 (fine, 20 ev) | **−4 (prod.)**; inside the fine-setting range | M3.json |
| 14b | c, 1 TeV, 3 keV | 0.082 | 0.091-0.095 | **≈ −5** | M3.json |
| 15 | R(1/2, 1/4, 1/20, 1/80), 500 GeV, 1 keV | 1.072/1.144/1.311/1.455 | 1.073/1.147/1.320/1.460 (±0.001-0.005) | −0.3/−1/−2/−1 | M3.json |
| 16 | same, 1 TeV, 1 keV | 1.069/1.138/1.299/1.437 | 1.070/1.141/1.302/1.443 | ≈ −1 each | M3.json |
| 17 | same, 500 GeV, 3 keV | 1.059/1.117/1.253/— | 1.066/1.130/1.278/(floor) | −3/−4/−5 | M3.json |
| 18 | B exponent over B/80…B, 1 keV | 0.914 (500), 0.917 (1000) | 0.911 ± 0.003, 0.912 ± 0.003 | +1, +1.7 | M3.json |
| 19 | Λ exponents, 500 GeV (0.6→1, 1→2, 2→3, 3→5, 5→10) | −1.79, −1.86, −1.78, −1.87, −1.84 (model medians, c07) | −1.83±0.10, −1.83±0.07, −1.88±0.11, −1.76±0.09, −1.74±0.14 | +0.4, −0.4, +0.9, −1.2, −0.7 | M3.json |
| 19b | mean Λ exponent 0.6-5 keV | −1.79…−1.86 per event; −1.83 population | −1.81 (200), −1.81 (500), −1.78 (1000) | ≈ 0.3σ | M3.json |
| 20 | median Δs_B, 500 GeV, 1/2/3/5/10 keV [µm] | 31.1/8.6/4.18/1.61/0.45 (model, other events) | 29.1±2.1/8.17±0.72/3.80±0.29/1.55±0.11/0.46±0.06 | +1.0/+0.6/+1.3/+0.5/−0.2 | M3.json, c07 |
| 21 | m independence at 1 keV (200/500/1000) | 33.5/31.1/29.5 (weak decrease) | 28.7/29.1/31.0 (flat within ±2.5) | consistent within errors; the trend sign is not resolved | M3.json |
| 22 | Pre-crossing response | exactly linear (§3.3) | R_hit = 1.0000, metric 10⁻⁴ | — | M3.json |
| 23 | Li vs causal response per unit B (M5) | c within a few % (§4.4: c_KL ≈ 0.106 vs c_NG ≈ 0.103 at γ* = 1.28, i.e. R(1/80) +1 %) | Li 1.142/1.306/1.447 vs causal 1.155/1.320/1.467 (same events) | consistent (−1 % to −1.4 %) | M5.json |

6. **Thickness exponents and c.** At 1 keV the derived c and the response agree within 1-2σ (rows 12-16, 18). The Λ
   exponents and absolute medians agree within 1.3σ (rows 19-20). **At 3 keV the prediction fails at the 4-5σ level:
   0.085 vs 0.093 (500 GeV), 0.082 vs 0.091-0.095 (1 TeV).** My formula predicts a drop from 1 to 3 keV:
   c ∝ 1/(L + K) with L growing by 2 ln 3. It predicts 0.104 → 0.085; E2 measures 0.105 → 0.093. So the formula
   gives the direction but too large a drop. E2's own bridge (M13), which uses their measured per-pair rotations,
   gives 0.077-0.079 at 3 keV, i.e. the same deficit. So the shortfall is *not* in my per-pair law (which matches E2
   per crossing to < 1 %, rows 1-5) but between the per-pair rotation and the measured thickness response. Candidate
   explanations, in my order of likelihood:
   - (a) **Precision floor at 3 keV (ESTIMATE, testable).** At 3 keV b_odd/ℓ₀ ≈ 2×10⁻⁶ at B₀, 6×10⁻⁷ at B₀/4 and
     1.2×10⁻⁷ at B₀/20. E2's floor is 3×10⁻⁸ for γ* ≤ 1.3 and ≈ 10⁻⁶ for γ* ≥ 2. So for the γ* ≳ 2 events (≈ 15 % of the
     sample) every B point at 3 keV is at or near the floor. A B-independent numerical rotation noise inflates
     R(f) = Δs(fB)/(fΔs(B)) as 1/f. A floor term of only ≈ 0.4 % of Δs(B₀) raises R(1/4) by ≈ 0.013, which is the
     observed excess. Supporting evidence: the fine-setting values at 3 keV (0.085-0.098) bracket my 0.085, while at
     1 keV the fine values (0.104-0.108) agree with production. Test: c at 3 keV restricted to γ* < 1.5, or in quad
     precision.
   - (b) **Thickness contributions not in the per-pair rotation** (E2's suggestion: in-plane terms, b_odd offsets).
     The linear-in-B ones (b_odd, static tilt) would *lower* c, not raise it, so they cannot explain the excess.
     Something with a stronger-than-log B dependence would be needed; I have no candidate.
   I do not adjust anything; prediction P-10/P-14 at 3 keV stands as failed at 4-5σ pending test (a).
7. **M5 (Li).** The vacuum Â of the straight string (0.93/0.67/0.33/0.17) is exactly my Kang-Luty formula (row 9).
   It is *not* the same quantity as my "η_Li/η_NG = 0.97/0.84/0.50", which is per *field-driven period*. In the field
   the KL string does not conserve the ends' angular momentum, so its b_odd is larger by 1.04/1.21/1.68 (c04), and
   its constant differs: η_KL/η_NG = (Â_KL/Â_NG)(b_KL/b_NG)(L+K)_KL/(L+K)_NG ≈ 0.94·1.04·1.0 / 0.70·1.21·0.97 /
   0.38·1.68·0.79. The thickness *ratio* Li/causal follows η_KL/η_NG: 0.84 vs R2's 0.85 at γ* = 1.28. The *response
   per unit B* depends only on c = 1/(L + K), where the log coefficient cancels. With L_KL = L − ln(b_KL/b) and K_KL,
   c_KL exceeds c_NG by ≈ 3 % at γ* = 1.28. That is why M5 finds the same response within 1-2 % although Â_SS/Â_NG = 0.70
   (E2's open point). The γ* = 2 thickness ratio (0.50 predicted vs 0.69 measured, R2) remains open (§10).
8. **Precision floor.** The B/1000 comparison is dropped: S_Bscan's 1.83 and E2's 2.00 ± 0.04 at f = 10⁻³ (1 keV) are
   floor-affected, and so is B/80 at 3 keV. P-13/P-14 are marked "not testable" there. The v1 statement "B/1000: 6 %
   below the measurement" (§5.3, §10 item 4) is withdrawn. Note also E2's point that classical NG is scale-free:
   "b < 1/Λ" in §7 is a *physical* validity limit of the classical string (flux-tube width), not a numerical threshold.
   The double-precision floor (b/ℓ₀ ≈ 3×10⁻⁸) is a separate, numerical limit.
9. **T2 erratum:** recorded in §10, item 10.

### 9.3 v3: E2's follow-ups FU1-FU3 (NUMERICS §11, results/FU.json); blind numbers above unchanged
**FU1, c at 3 keV.** E2 evaluated my c_ev on the same events (median c_E1 = 0.0839 / 0.0815 at 500 / 1000 GeV) and
measured the per-event c_k with 10× finer steps (max_boost 10⁻³, converged against 10⁻⁴ on 8-9 events).
| sample (3 keV) | measured − E1, k = 2 | k = 4 | k = 20 | pull k = 2 / 4 / 20 | note |
|---|---|---|---|---|---|
| 500 GeV, blind production (10⁻²) | +0.0076 ± 0.0030 | +0.0072 ± 0.0025 | +0.0058 ± 0.0023 | 2.5 / 2.9 / 2.5 | step-biased (§9.2 row 14) |
| **500 GeV, 10⁻³** | **+0.0021 ± 0.0015** | +0.0055 ± 0.0020 | +0.0113 ± 0.0018 | **1.4** / 2.8 / 6.3 | |
| 500 GeV, 10⁻³, γ* < 1.2 | +0.0004 ± 0.0019 | +0.0020 ± 0.0016 | +0.0056 ± 0.0013 | 0.2 / 1.3 / 4.3 | |
| 1 TeV, blind production | +0.0095 ± 0.0035 | +0.0087 ± 0.0017 | +0.0074 ± 0.0031 | 2.7 / 5.1 / 2.4 | step-biased |
| **1 TeV, 10⁻³** | **−0.0003 ± 0.0006** | +0.0043 ± 0.0017 | +0.0132 ± 0.0033 | **−0.5** / 2.5 / 4.0 | |
| 1 keV, 500 GeV / 1 TeV (production = converged) | +0.0001 ± 0.0008 / +0.0003 ± 0.0005 | +0.0010 ± 0.0004 / +0.0007 ± 0.0004 | +0.0015 ± 0.0005 / +0.0001 ± 0.0003 | ≤ 0.6 at k = 2; ≤ 3 at k = 4-20 (1-1.5 % of c) | |
Population values (converged, from median R): c(k = 2) = 0.0890 (500 GeV), 0.0841 (1 TeV) at 3 keV, vs my 0.0846 / 0.0819
(c07 sample) and 0.0839 / 0.0815 (E2's events). **Verdict:** the v2 "failure at 3 keV" was mostly numerical (production
step bias at small k). Where b_odd/ℓ₀ ≫ floor (k = 2, b_odd/ℓ₀ ≈ 10⁻⁶) the prediction agrees (pulls 1.4, −0.5). The
excess that grows with k (+0.004-0.005 at k = 4, +0.011-0.013 at k = 20) follows the measured round-off amplification
(item FU1b below). It halves for γ* < 1.2 and is not a γ* ≳ 2 effect, so my v2 hypothesis (a) is wrong in its γ* part.
A residual physical contribution at the 1-3 % level at k = 4 (part of FU3, below) cannot be excluded.

**FU1b, sensitive dependence: numerical or physical?** A 10⁻¹⁴ perturbation of the initial momenta changes Δs by
0.15/0.26/0.47/0.89 % at f = 1, 1/2, 1/4, 1/20 at 3 keV, but by ≤ 3.5×10⁻⁴ at 1 keV. My reading (ESTIMATE):
- The per-crossing map is not chaotic in the exponential sense. η is reset every period by the torque (J returns to
  ≈ 0 at every even crossing), so errors in J do not compound multiplicatively. But the rotation at a nearly head-on
  crossing is ∝ b ln(1/b), with dψ/db ∝ ln(ℓ/b), divergent as b → 0. The even crossings are head-on at first order, and
  at ≥ 3 keV their b_even sits at the double-precision floor (b/ℓ₀ ≈ 3×10⁻⁸, E2 §1.3). Each even crossing then adds a
  random rotation δψ ~ (floor)·ln(1/floor) ≈ 5×10⁻⁷, which random-walks over N/2 ≈ 125 periods to ≈ 6×10⁻⁶ rad.
- The signal is Θ = Nη. At fixed f it is Λ-independent (N ∝ Λ², η ∝ Λ⁻²), ≈ 6×10⁻⁴ rad at f = 1/20 (3 keV, 500 GeV).
  The ratio ≈ 1 % matches the measured 0.9 %. The noise grows ∝ √N ∝ Λ and its relative size ∝ 1/f, as observed (largest
  at weak B, small at 1 keV). Because Δs is positive-definite, the noise biases R(f) and c upward at large k.
- **Physically**, the classical string is not valid at these even crossings anyway (b_even ≪ 1/Λ = 0.66 Å at 3 keV).
  If the flux tube randomises the even-crossing geometry at the scale 1/Λ, the same estimate with 1/Λ in place of the
  floor gives δψ ~ (1/(Λℓ)) ln(Λℓ) ≈ 10⁻⁷ per even crossing at 3 keV. That is a physical irreducible noise of the
  same order as the numerical one (CONJECTURE; needs a non-classical model of the reconnection).
- **Consequences for P1:** at the nominal field (f = 1) the effect on Δs is ≤ 0.15-0.3 % for Λ ≤ 3 keV, negligible. c
  should be quoted from B ratios with b_odd/ℓ₀ ≳ 10⁻⁶: k ≤ 80 at 1 keV, k ≤ 2-4 at 3 keV. With that, c is verified to
  ≈ 1.5 % at 1 keV and ≈ 2-3 % at 3 keV; the Λ dependence of c (0.104 → 0.084 at 500 GeV) is confirmed. Weak-field
  response at Λ ≳ 3 keV is not a robust classical prediction.

**FU2, K_vac.** With Â fixed to 2(γ*−1)/(ρ artanh β*) and b/ℓ_max ≤ 10⁻⁴, E2 finds K_vac = 0.0709/0.0627/0.0382 at
γ* = 1.01/1.02/1.05, extrapolating to **0.0791 ± 0.0003 vs my 3 ln 2 − 2 = 0.0794** (pull −1). The vacuum constant at
γ* = 1.3/2/3 is −0.158/−0.560/−0.965 (field constant K: −0.059/−0.309/−0.569; the difference is δ_pair/G). §10 item 13
is closed.

**FU3, odd-crossing residual (physics).** Per pair vs my closed form: +0.53/+0.26/+0.08/−0.50/−1.11 ε⊥ in γ* bins
1.0-1.1/1.1-1.2/1.2-1.35/1.35-1.6/> 1.6 (production); +0.03/+0.04/−0.05/−0.59/−1.16 with max_boost 10⁻³ (20 events). It is
Λ- and step-independent at γ* ≥ 1.2. The low-γ* positive values shrink with finer steps (+0.53 → +0.03), so they are
mainly numerical. The high-γ* negative values are robust: −4 % of ψ_pair at γ* = 1.35-1.6 and −9 % at > 1.6.
- **Assessment.** The only first-order difference between a lab event and my reduced problem is B* (E*∥ is second
  order: its effect in units of ε⊥ would scale ∝ ε ∝ Λ⁻², which is excluded by the Λ independence). A symmetry
  argument (inversion through the CM combined with exchange of the ends: E* forcing is even, B* forcing odd, rotation
  even) shows that B* cannot rotate the axis in *linear* response. But the rotation is made in the non-linear inner
  region of the odd crossing, where B*-driven odd-parity motion of amplitude comparable to b can enter quadratically
  ((e/b)², with e and b both ∝ field). That gives a first-order, B*-even effect. I tested this directly (c12: exact
  string, pair at rest, E* ⊥ n̂ plus B*):
  - B* ∥ n̂: |Δη/η| ≤ 3×10⁻⁵ (no effect);
  - B* ⊥ n̂ (normal to the orbit plane or along E*), q|B*|/σ = 4ε⊥: Δη/η = +3×10⁻⁵ (γ* = 1.05), −0.2…−0.4 % (1.3),
    −4…−7 % (2), the same at ε = 10⁻⁵ and 10⁻⁴, and the same for ±B*;
  - strength scan at γ* = 2: −0.18/−1.9/−6.8/−13.8/−21 % for q|B*|/σ = 1/2/4/8/16 ε⊥ (quadratic at small B*, then
    logarithmic saturation, as expected if B* enlarges the effective inner cut-off b → b_eff).
  - In lab events q|B*⊥n̂|/σ ≈ ε⊥/(β_T,cm sin α) × O(1) ≈ 2-10 ε⊥. So **B* explains the sign, the γ* dependence and the
    size of E2's high-γ* residual** (−4 %, −9 %; c12 gives −2…−14 % at γ* = 2 for this range). It does not explain
    the low-γ* positive residual, which is mostly numerical (shrinks with finer steps).
  - The same effect also explains, at least in part, why my rotating-yo-yo model overestimates Δs at γ* ≳ 2 (§5.1:
    +10-35 %), previously attributed only to the non-localisation of the rotation.
- **Impact.** B* enters through K, not G: η → ε⊥G[L + K + ΔK_B*], ΔK_B* = (Δη/η)(L + K) ≤ 0. Per event
  c_ev → 1/(L + K + ΔK_B*), i.e. c rises by |Δη/η|: ≤ 0.5 % for γ* ≤ 1.3 (most of the DY spectrum), +4…+9 % in the
  γ* > 1.35 tail. On the population (E2's median per-pair residual over all events: +0.033 ± 0.014 ε⊥ ≈ +0.3 %) the
  effect on c is ≈ ±0.5 %. My v2 estimate "−1 to −2 %" had the wrong sign for the high-γ* tail and is replaced. The
  exponents change by 2Δc ≲ 0.01 (population). The per-crossing law (G, b_odd) is unchanged.
- **Status:** effect measured (ESTIMATE, c12); mechanism (inner cut-off enlarged by B*-driven motion) CONJECTURE.
  An analytic ΔK_B*(γ*, B*/E*) is not derived (§10 item 12).

## 10 Open issues / where I am unsure
1. **Relativistic K(γ*) is numerical, not analytic** (MEDIUM). The log coefficient and the NR constant are derived;
   the relativistic constant comes from exact-NG runs (converged to ≲ 0.01). A closed form would need the outer
   solution of the transverse wave equation on the yo-yo world sheet with the field source; I did not attempt it.
   Impact on c: ≤ 1 %.
2. **Accumulation at γ* ≳ 2** (MEDIUM). The step-at-the-crossing model is 10-35 % off there (§5.1). A better model
   would distribute the rotation over the half-period following the 1/s force law of §3.4. The per-period η is
   not in question.
3. **Non-secular first-order terms omitted** (LOW-MEDIUM). b_odd and the alternating static tilt are left out of the
   model. They scale as Λ⁻⁴ and matter at Λ ≲ 0.6 keV (few oscillations in the tracker), where they steepen the Λ
   exponent. Not quantified.
4. ~~R(1/1000)~~ **Resolved (E2):** the measured 1.83 (and E2's 2.00 ± 0.04) at B₀/1000 are at the double-precision
   floor (b/ℓ₀ ≈ 3×10⁻⁸); the comparison is dropped.
5. **Hit displacements vs thickness** (LOW). The measured responses (S, R1) are on hit displacements, mostly in-plane;
   the theory gives the same per-event factor for in-plane and out-of-plane rotation (same η, same L). I did not
   check this separately with the causal code.
6. **Even-crossing second order** (LOW): b_even ≈ 12 ε∥ b_odd is read off one γ*; the numerical floor ∝ max_boost was
   found here and means T2's even-crossing table is not converged (§6.1).
7. **Vacuum precession with initial J₀** (§6.3): the per-crossing law is now measured by E2 (M2a) and agrees with
   Â = 2(γ*−1)/(ρ artanh β*). The NR constant is K_vac = 3 ln 2 − 2 (c09, c10). The application to MS kicks is
   still not worked out (CONJECTURE).
8. **E3's apsidal coefficient** (LOW): E3 quotes a slope 0.354 = 1/(2√2) in their units; I did not map their units to
   mine. The structure L ln(1/L) agrees; my NR coefficient is checked independently (c04, c05).
9. **Li/causal ratio at γ* ≥ 2** (MEDIUM): predicted 0.50 vs measured 0.69 at γ* = 2 (§4.4). The lab-frame Li ŝ
   extrapolation and hit sampling are not modelled. Not used for any other conclusion.
10. **Proposed erratum to T2 §5.3 / §6.3 (T2 not edited).** The even-crossing miss distances in T2's table
    (16-31 Å at 1 keV, 0.13-0.19 Å at 3 keV, 10⁻⁴-2×10⁻³ Å at 10 keV) are not physical. In a pure CM E* ⊥ n̂ they are a
    splitting artefact of the first-order field kick, ∝ max_boost: b_even/b_odd = 2.6×10⁻³/3×10⁻⁴/2.7×10⁻⁵ at
    10⁻²/10⁻³/10⁻⁴ (c03), and E2 M2b finds the same. Physically b_even = 0 at first order. In full events it is second
    order, ≲ 10⁻³ b_odd at 1 keV and growing with the crossing index (E2 M1). It is solver-dependent at 20-60 % and at
    the precision floor above ≈ 2-3 keV. Consequence for T2 §6.3: "even crossings reconnect within 1/Λ from Λ ≈ 3 keV"
    holds a fortiori (an upper bound); the ε_eff estimates are unchanged in direction. Δs_B is unaffected.
11. ~~c at 3 keV 9-13 % above the derived value~~ **Mostly resolved (v3, FU1):** production-step bias at small k plus
    double-precision noise at large k. With converged steps at B₀/2: agreement (pulls 1.4, −0.5). An excess of
    +0.004-0.005 (2-3σ) at B₀/4 and +0.011-0.013 at B₀/20 remains. It follows the measured round-off amplification
    (§9.3 FU1b); a 1-3 % physical part (B*, item 12) cannot be excluded at k = 4 (LOW-MEDIUM).
12. **B* effect on the rotation (v3; MEDIUM).** My v1-v2 claim "B* inert at first order" is wrong for η (correct for
    b_odd and the linear dynamics) (§1.3, §9.3 FU3). Measured: −0.2 % (γ* = 1.3) to −7 % (γ* = 2) at q|B*|/σ = 4ε⊥,
    even in B*. It explains E2's high-γ* residual. Open: an analytic ΔK_B*(γ*, |B*⊥|/|E*⊥|), the low-γ* residual
    (mostly numerical), and folding ΔK_B* into c_ev event by event. Impact on population c ≈ ±0.5 %; +4…+9 % on c and
    −4…−9 % on η (hence on Δs) in the γ* > 1.35 tail.
13. ~~K_vac in the NR limit~~ **Closed (FU2):** E2's refit with Â fixed gives 0.0791 ± 0.0003 vs 3 ln 2 − 2 = 0.0794.
14. **Sensitive dependence at weak B and Λ ≳ 3 keV (v3; LOW for P1, MEDIUM as physics).** It is logarithmic
    sensitivity at the head-on even crossings, fed by noise at the precision floor and accumulated as a random walk
    over N ∝ Λ² crossings (§9.3 FU1b). Negligible at nominal B. It limits B scans to b_odd/ℓ₀ ≳ 10⁻⁶. A physical
    analogue (flux-tube reconnection at b_even < 1/Λ) would give noise of the same order; not modelled.

Decisions flagged: (i) defining c per event as 1/(L + K) at the operating point (the synthesis' "1 + c ln(Λ²/qB)" form
has its logarithm referred to that point) — MEDIUM, a convention; (ii) using the rotating yo-yo on the T3 sample for
population numbers rather than an analytic average over the DY spectrum — MEDIUM (needs E2 for causal confirmation).

## 11 References opened
- 0805.4642 (Kang-Luty): Eq.3.7-3.10 (endpoint equation of motion, straight-string remark, §3.2); §5.8 Eq.5.64
  (separation after one oscillation ∝ v_cm B m/Λ⁴).
- 1911.02223 (Li et al.): Eq.III.6-III.12 (CM simultaneity, ŝ prescription, step bound, thickness d, d_min ~ 1.16 µm
  formula).
- 2002.07503 (Li et al.): §V Eq.V.1-V.9; App.A Eq.A.1-A.17 (z±, per-period rotation η, A.17); App.B Eq.B.1-B.9;
  App.C Fig.8.
- 1708.02243 (Knapen et al.): §II Eq.8-9 (torque estimate of the plane rotation) — located in the text cache; content
  as summarised in NOVELTY_AUDIT §3.4 (E3), equations not re-derived by me.
- NOVELTY_AUDIT.md §0, §3-4 (E3) and `novelty_sources/E3_apsidal_check_out.txt`.
- Theory-track inputs: BRIEF; synthesis §0.1, S-1, S-3, X-2, X-3, X-13, §5; T2 §2, §5-6; T3 §3; T4 §3; code
  T3_causal.py, R1_conformal_ng.py (header), T2_propagator.CausalNullString, T2_crossing_missdist.py,
  S_Bnonlin.py/S_Bscan.py, R1_Blinearity.py; outputs S_Bnonlin_out.txt, R1_Blinearity_out.txt (no S_Bscan output
  file exists; its numbers are quoted from synthesis X-3).
- Artru / Lund piecewise-null string construction: cited as in the synthesis, UNVERIFIED (not opened).
