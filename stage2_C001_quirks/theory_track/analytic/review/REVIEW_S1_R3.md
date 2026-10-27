# Review S1-R3 (Stage 1, theory track, round 3)

Reviewer: S1-R3. I took no part in rounds 1-2 or in writing the files. Date: 2026-10-11.

Under review:
- `NEAR_MISS_IMPULSE.md` v5 final, `predictions.json` v5 and `checks/c15`;
- `numerics/NUMERICS.md` (§1.3-1.5, §11-§13) with `results/FU.json`, `FIX1.json` and `FIX2.json`;
- `NOVELTY_AUDIT.md` and `PROPOSED_CHANGES.md`.

Protocol: jfc `03-review.md` and `critical_reviewer.md`, at iteration 3 (warn level). Classes are A = wrong, B = must fix before
PASS, C = style or clarity.

My scripts and outputs are in `review/r3_checks/`. They re-analyse E2's raw FIX2 and M2 data and make no new string runs. CPU
used is under 2 min.
- `r3_floor_test.py` contains two checks. (1) It tests the shape and coefficient of the M2b precision floor. (2) It compares a
  per-event floor prediction with E2's B*-off and pure-E*⊥ runs.
- `r3_floor_B0.py` estimates the floor content of E2's direct B₀ runs at 5-13 keV.
- `r3_impact_err.py` propagates the errors of the implied Δs_B(Λ)/Δs_B(3 keV) shift.

## 0 Summary
1. Round 2 is resolved in substance. N1: FIX2's B*-off and detector-scale scan replace the over-claim with a two-part
   decomposition. N2: the scale-free property is derived correctly (c15), and "only weak-field affected" is withdrawn. N3 and N4
   are restated as asked. Most C items are applied, with some stale leftovers (C-list).
2. FIX2 (i), the physical B* part, is evidenced. The cleanest evidence is not quoted in the note: for k_B ≥ 5 events, on − off
   Δc(4) is +0.0136 ± 0.0039 (500 GeV) and +0.0125 ± 0.0038 (1 TeV) at s = 1, and ≈ 0 at s = 1/9. These numbers are free of the floor: it cancels in on − off (same ε⊥), and B*-off Δc(4) ≈ 0.
3. FIX2 (ii), the precision floor, is plausible and now better supported.
   - The M2b excess is ∝ u/ε⊥² at every γ* and both step sizes: (0.5-1.3) u/ε⊥², local power −2.0 ± 0.2.
   - E2's pure-E*⊥ full-event residual follows ε⊥^(−2.09) and ε⊥^(−1.89) per event and is independent of γ* (Spearman ≈ 0.03).
   - Its amplitude is 3.8-3.9 × the CM-frame coefficient, so "the size matches" is too strong as written (C1).
4. **R3-B1.** The adopted "B*-driven +2-5 % on Δs_B above ≈ 5 keV" (§0 item 5, §5.5, P-9, predictions.json) is not supported
   as a B* number. It comes from direct-B₀ medians at 7-13 keV, which are not step-converged. With the measured floor law, a
   floor contribution of the same size is expected there (13 keV: +0.039 vs measured +0.044 in Δc(2)). This is the part E1 says
   "does not enter". Fix: restate as an unmeasured systematic (text only).
5. The headline scope is otherwise supported: c to 1-2 % and C to 0.1-0.2 at 1 keV; 3 keV at B₀/2 (and B₀/4 for k_B < 5);
   5 keV consistent (Δc(2) = +0.005 ± 0.007, floor-free).
6. Global consistency holds: 14 numbers spot-checked against JSON, 13 OK and 1 misquote (C3). The P1 scope (b) is applied in E1
   (title, §0, §11, Highland credited). Novelty and credit match NOVELTY_AUDIT. PROPOSED_CHANGES has stale caveats and misses the
   synthesis §5 P1 row (C9).

Verdict: **ITERATE** (A = 0, B = 1, C = 10). The single B is a restatement and needs no new run or derivation. A check of that one
fix is sufficient for PASS.

## 1 Resolution of round 2 (from the text, not the response tables)
| R2 item | Status | Evidence |
|---|---|---|
| N1 (3 keV excess "is B*") | **Resolved** (wording leftovers C1, C2) | §9.3 "Verdict (v5 final): two parts", §0 item 5, P-14, §10.1, predictions `v4_FIX1.verdict`; R2's confounding analysis and scale-free test are reproduced in §9.3; c14 "right size" withdrawn (§9.3 l.623); floor part tagged ESTIMATE with "not separately demonstrated … accumulation-model term not excluded" |
| N2 (impact at B₀ vs scale invariance) | **Partly resolved**: derivation and withdrawal correct; the replacement impact statement over-attributes (R3-B1) | §5.5 derivation (action scaling, checked below), "withdrawn" l.364; P-25; adopted systematic l.379 |
| N3 (C Λ-independence tautological) | **Resolved** | §5.2 "Λ independence holds by construction … not a measurement"; measured C 1.13 ± 0.18, two-solver 1.145/1.147; P-9 "(Λ-independent by construction)"; predictions `thickness_law_v4.Lambda_independence` |
| N4 (in/out-of-plane) | **Resolved** in §1.3 and predictions; one stale echo (C5) | §1.3 "Not a clean test; consistent for PS/2S at 500 GeV only"; but §12 row Constr. B3 still says "equal within 1 % from existing data" |
| C1 (NUMERICS FU1(b) sentence) | Resolved; stale pointers remain (C8) | NUMERICS §11 FU1(b) flagged "[withdrawn → §12.1, R2-C1]" |
| C2 (predictions v3 remnants) | Mostly resolved (C7) | assumptions[−1], v3_FU1 note, accuracy "MEDIAN", straight-string statement, regime_of_validity all flagged; unflagged: `c.comparison_E2` 3 keV "FAILED/open" (v2) |
| C3 (k_B labels, errors) | Resolved | §9.3 l.602-606 |
| C4 (Knapen Eq.9) | Resolved in E1; NOVELTY_AUDIT still has v_cm²/v² (C9) | §5.2: 6.5×10⁻⁶ (recomputed: 10⁻⁵ × 0.25/0.62² = 6.5×10⁻⁶ ✓; Eq.8/Eq.9 = 9.4 ✓; ×1 m = 6.5 µm ✓); NOVELTY_AUDIT l.113, l.155 |
| C5 (Li c within 3 %) | Resolved | §4.4, P-17, predictions `straight_string_models.statement` |
| C6 (\|q\| = 2) | Resolved | §6.5, P-24 |
| C7 (PROPOSED_CHANGES) | Partly resolved (C9) | item 10 FAILED ✓, items 12-13 added ✓, item 2 caveats added but now stale ("origin open", "+1.5-2 %") |
| C8 (tag systems) | Resolved | E1 header; NUMERICS §1.4 last lines |
| C9 (§5.1 n per bin) | Resolved | §5.1 l.273-274 |
| C10 (Li 10-event subset) | Resolved | §4.4, §9.5, P-17 |

## 2 New findings

### R3-B1 (B): the adopted "+2-5 % B*-driven systematic above ≈ 5 keV" is not a B* number
**Where:**
- §0 item 5: "a physical, cumulative CM-magnetic-field (B*) effect adds an estimated +2-5 % to Δs_B";
- §5.5 "Adopted systematic", §9.3 "Impact on the headline law", §10.1 and P-9;
- predictions.json `scale_free_v5.adopted_systematic` ("B*-driven … floor part does not enter the physical law") and
  `open_after_E2[0]`;
- PROPOSED_CHANGES item 2.

**Evidence.**
1. **Source of the number.** The +2-5 % is E2's integrated direct-B₀ medians, +0.3/+1.3/+2.8/+4.5 % at 5/7/10/13 keV (FIX2 N2
   `m500_implied_rel_change_of_Ds_vs_3keV`).
   - Above 5 keV these are not step-converged per event: 10⁻³ − 10⁻⁴ differs by up to 0.106 in c (FIX2
     `convergence_7keV_fine_minus_vfine`).
   - E1 §5.5 and NUMERICS §13.2 say themselves that the B₀ points "approach the precision floor".
2. **Floor content** (`r3_floor_B0_out.txt`).
   - By the scale-free property, (Λ, B₀/2) at 10-13 keV has the per-period ε⊥ of 3 keV at B₀/22 to B₀/38, i.e. ε⊥(B₀/2) median
     2.6×10⁻⁷ and 1.4×10⁻⁷ at 500 GeV.
   - The floor law measured in §3 below is δ = A u/ε⊥² on Δs. With A fitted to E2's own pure-E*⊥ lab runs, the predicted floor
     part of Δc(2) is:

     | m, Λ | floor predicted | measured |
     |---|---|---|
     | 500 GeV, 7 keV | +0.0025 | +0.025 ± 0.025 |
     | 500 GeV, 10 keV | +0.0105 | +0.017 ± 0.023 |
     | 500 GeV, 13 keV | +0.039 | +0.044 ± 0.058 (k_B < 5: +0.012 vs +0.028 ± 0.017) |
     | 1 TeV, 7 keV | +0.010 | +0.002 ± 0.017 |
     | 1 TeV, 10 keV | +0.037 | +0.079 ± 0.11 |

   - Even the CM-frame coefficient, a lower bound, gives +0.003-0.011 at 10-13 keV, i.e. 15-25 % of the measured values.
   - So the 10-13 keV values that set the "2-5 %" contain a floor part of comparable size, which §5.5 says "does not enter the
     physical B₀ law". They cannot be adopted as a B* effect.
3. **Size of the physical B* part at B₀.** It is demonstrated only in the scale-equivalent 3 keV B scan at the 3 keV
   oscillation number. It grows with N_osc (0 → +0.0014 → +0.0063 in Δc(20) for N/9 → N/3 → N, 500 GeV). E2 states that the
   extrapolation to N(13 keV) = 19 N(3 keV) "is not reliable". So "+2-5 %" is neither a measurement nor a bound on it: the true
   effect could be smaller or larger.
4. **Statistical errors.** The quoted errors (±1.5 % at 5 keV, ±10-30 % at 10-13 keV) are not reproduced by propagating the JSON
   bootstrap errors. That propagation gives ±0.4/±1.0/±2.0/±2.8 % at 5/7/10/13 keV (500 GeV) and ±0.4/±0.8/±4.2 % (1 TeV)
   (`r3_impact_err_out.txt`). If the larger numbers are meant to include step non-convergence, say so.

**Fix (text only).**
- §0 item 5, second sentence, along these lines: "Above ≈ 5 keV the B₀ law is not numerically verified. A physical B* effect that
  grows with the number of oscillations is demonstrated in the scale-equivalent 3 keV B scan (§9.3), but its size at B₀ is not
  measured. Direct runs give ≲ 1 % on Δs_B(Λ)/Δs_B(3 keV) at 5-7 keV. The +3-5 % at 10-13 keV is of the size expected from the
  precision floor (§5.5)."
- §5.5, P-9, §9.3, §10.1 and predictions.json: label the systematic as **unmeasured, provisional (order ±5 % on Δs_B for the
  population above ≈ 5 keV, sign expected positive), not attributed**, and keep "tens of % in c per event for k_B ≳ 10".
- Drop "B*-driven: +2-5 %" as a measured or estimated B* magnitude.
- The "Measuring it needs …" sentence can stay. Add that the floor part must be removed first, for example with the higher-precision
  test of §3.

### C notes
- **C1** (floor amplitude, §9.3 (ii), NUMERICS §13.1 reading 3).
  - "The floor accounts for the size" uses ε⊥ = 1-2×10⁻⁷. Per event, the median ε⊥(B₀/20) is 2.9×10⁻⁷ (500 GeV) and 1.9×10⁻⁷
    (1 TeV). There the CM-frame floor predicts Δc(20) = +0.0008 and +0.0019, against the measured pure-E*⊥ +0.0039 and +0.0062:
    median ratio 3.8 and 3.9.
  - The shape is what supports the attribution: ε⊥⁻² per event, no γ* dependence, and N-independence. A physical correction to an
    asymptotic weak-field law cannot grow as ε⊥⁻².
  - Suggested text: "shape matches the double-precision floor (ε⊥⁻², γ*-independent, per period); the amplitude needs a lab-frame
    floor coefficient ≈ 3-4× the CM-frame one (ESTIMATE, not demonstrated)". Quote the decisive test of §3 as the way to close it.
- **C2** (B* part wording, §9.3 (i), §13 response row, NUMERICS §13.1 reading 1).
  - "≈ half at B₀/20" holds at 500 GeV (0.0063 of 0.0121). At 1 TeV on − off Δc(20) is +0.0024 ± 0.0041, about 20 % of 0.0122.
  - "+0.006 … (1 TeV +0.006 at Δc(4))" mixes metrics between the masses.
  - Quote the floor-free k_B ≥ 5 Δc(4) numbers: on − off +0.0136 ± 0.0039 / +0.0125 ± 0.0038 at s = 1; +0.0055 ± 0.0029 /
    +0.0002 ± 0.0035 at s = 1/3; +0.0009 / −0.0003 at s = 1/9 (FIX2 `on_minus_off_s*.kB_ge5`). They are the best evidence that the
    B* part is physical and cumulative.
- **C3** (M2b numbers). "+11 % at 3.2×10⁻⁸" should read **+18 %**. From M2.json (γ* = 1.3, 10⁻³), (21.027 + 3.725)/(19.41 + 1.61)
  = 1.177. NUMERICS §13.1 reading 3 has the same number.
- **C4** NUMERICS §13.1 reading 2 says the B*-off part is "+0.005…+0.006 at 1 TeV" at all s. off_s3 is +0.0082 ± 0.0027 (E1's
  table has it right). The 500 GeV B*-off values also rise mildly with s (0.0030/0.0038/0.0044). Say "N-independent within
  errors".
- **C5** §12 row Constr. B3 still reads "in/out-of-plane response equal within 1 % from existing data", contrary to §1.3 (N4).
  §12 row Crit. A1 "Impact at B₀: ≈ −1 %" should add "and §5.5 above 5 keV".
- **C6** §11 (b) gives the title "e.g. 'Log-enhanced plane rotation of quirk pairs in a solenoid'", while the adopted title (line 1
  and the predictions changelog) is "Crossing-generated plane thickness …". Harmonise.
- **C7** predictions.json:
  - `c.comparison_E2` "500GeV_3keV"/"1TeV_3keV" "FAILED/open" (v2, blind production) is unflagged.
  - `v3_FU1.note_v5` "origin open" is interim wording; point it to the v5-final two-part verdict.
  - `meta.date` is 2026-10-10.
  - `impact_FIX2` errors: see R3-B1 item 4.
- **C8** NUMERICS (E2's file) has stale pointers:
  - §0 item 4 "[superseded → … a B*-correlated excess]" and §11 FU1 verdict "[withdrawn → §12.1: the excess is a B* effect]" /
    "[→ §12.1: B*-correlated physical effect]" should point to §13;
  - §12.6 response table "physical B* effect, origin identified" should be flagged "[superseded → §13]".
- **C9** PROPOSED_CHANGES:
  - Item 2 caveat "(origin open) … provisionally +1.5-2 %" should become the v5-final wording, and R3-B1 once fixed.
  - Item 6 "MS part not derived (P1 scope options)" should read "P1 scope decided: option (b)".
  - Missing: synthesis §5 P1 row. Its title "… exact string dynamics, crossing-generated plane thickness, and multiple scattering"
    and its physics/novelty columns (MS quantification) should be updated to the option-(b) scope and title.
  - Not E1's file, but to flag to E3/orchestrator: NOVELTY_AUDIT l.113 and the C2 row l.155 still read Knapen Eq.9 as
    v_cm²/v² (E1 and R2: v_cm/v²). The audit title still includes "exact string dynamics … and multiple scattering".
- **C10** §5.5 "Impact at B₀" item: say that the direct B₀ runs are one-solver with max_boost 10⁻³ (NUMERICS §1.4 row), as for the
  other 3 keV items.

## 3 Check 2: FIX2 decomposition of the 3 keV excess

**(i) Physical B* part.**
- **B*-off method.** I re-derived the inverse boost. For (E*, B* = 0) in a frame moving with β, E* ⊥ β:
  - E_lab = γE* = γ²β×fB;
  - B_lab = γβ×E* = γ²[β(β·fB) − β²fB].
  This matches NUMERICS §13 Method. Because the pair is neutral, its frame stays inertial with pure E*. The method is sound.
  E*∥-off is a further restriction to the M2b problem.
- **Cumulative growth.**
  - At 500 GeV, population on − off Δc(20) is 0.0000 / +0.0014 ± 0.0011 / +0.0063 ± 0.0023 for s = 1/9, 1/3, 1.
  - At 1 TeV the same quantity is not significant (+0.0024 ± 0.0041).
  - The k_B ≥ 5 Δc(4) numbers (C2) grow from ≈ 0 to 3.3-3.5σ in both masses. They are free of the floor, because the floor
    cancels in the paired on − off (same ε⊥), and at B₀/4 the B*-off Δc(4) is itself ≈ 0 (−0.0003, +0.0013).
- **k_B dependence.** On and off differ only for k_B ≥ 5: Δc(4) on/off is +0.0145/−0.0003 (500 GeV) and +0.0130/+0.0013 (1 TeV).
  For k_B < 5 they agree (−0.0001/+0.0000 and +0.0014/+0.0004).
- **Verdict.** Evidenced as a physical, deterministic, N-growing B* effect in k_B ≳ 5 events, with the mechanism not derived.
  Wording fixes are in C2.

**(ii) Per-period part attributed to the floor.**
- It is stated as ESTIMATE, with "not separately demonstrated" and "an accumulation-model term is not excluded". That labelling is
  correct.
- **M2b floor law** (`r3_floor_test_out.txt` (1)).
  - At all γ* = 1.05/1.3/2/3 and both step sizes, the excess of b_odd and of ψ_pair over the law is (0.5-1.3) u/ε⊥², with
    u = 2.2×10⁻¹⁶.
  - The local power between 3.2×10⁻⁷ and 10⁻⁷ is −1.8…−2.3 (one −3.0 at γ* = 1.05, 10⁻²).
  - It is step-independent (10⁻² ≈ 10⁻³).
  - This is the signature of an O(angle²) cancellation at relative precision u.
- **Full events** (`r3_floor_test_out.txt` (2), FIX2 raw `eperp_s1`, n = 40 per mass).
  - Per-event Δc(20) vs ε⊥(B₀/20): log-log slope −2.09 (500 GeV) and −1.89 (1 TeV).
  - Spearman with ε⊥ is −0.92/−0.65; with γ* it is +0.03/+0.04.
  - Tercile medians are +0.011/+0.004/+0.001 (500 GeV) and +0.024/+0.007/+0.003 (1 TeV).
  - Amplitude: 3.8-3.9 × the CM-frame coefficient.
- **Plausibility.** High. The shape is diagnostic, and a factor ≈ 4 between a lab-frame boosted computation and the CM-frame M2b
  is unremarkable. The "+1.7 % at 10⁻⁷" overshoot is part of this law.
- **Is there a cheap decisive test?**
  - Rescaling coordinates (by any factor) is not decisive. Floating-point error is relative, and classical NG and the floor are
    both scale-free, so rescaled runs reproduce the same ε⊥⁻² floor.
  - long double is float64 on Apple arm64 (NUMERICS §11 FU1b).
  - Two tests would decide it. I did not run them, because both need a kernel port beyond this review's budget.
    - (a) **Higher precision, short detector.** The per-period part is N-independent, so a scaled detector suffices. Run the 3-5
      `eperp` events with the smallest ε⊥(B₀/20) at s = 1/27, at B₀ and B₀/20, with the step map in double-double or mpmath
      (≥ 30 digits).
      - Prediction if floor: Δc(20) drops from +0.01-0.02 to ≲ 0.001.
      - E2's mpmath cost estimate (10³-10⁴ s per event per B at s = 1) gives ≈ 40-400 s per run, so under 1 CPU-h in total.
    - (b) **Reduced-precision emulation**, cheap in numba. Truncate the mantissa of every Minkowski product to 44 bits
      (u′ = 2⁻⁴⁴ ≈ 64u).
      - Prediction if floor: the same Δc distribution reappears at 8× larger ε⊥, i.e. at 3 keV and B₀/2.5 instead of B₀/20,
        with the ε⊥⁻² shape.
      - This tests the u-scaling of the residual directly.
  - Either would turn the ESTIMATE into a result. Neither is needed for the present (correctly labelled) scope, except for the
    measurement of the B₀ law above 5 keV (R3-B1), where the floor must be removed first.

## 4 Check 3: scope of the headline law
| Part | Evidence (JSON) | Verdict |
|---|---|---|
| Verified ≈ 1 keV: c to 1-2 %, C to 0.1-0.2 | M3: c = 0.105 ± 0.002 vs 0.104 → C = 1/c − ln(1/ε_B) = 1.13 ± 0.18 vs 1.22 (ln(1/2.254×10⁻⁴) = 8.397); FU1a 1 keV Δc ≤ 0.0015; R2 two-solver C = 1.145/1.147 | Supported |
| 3 keV: B₀/2 all events; B₀/4 for k_B < 5 | FIX2 on_s1 Δc(2) = −0.0005/+0.0005; k_B < 5 Δc(4) = −0.0001 ± 0.0015 / +0.0014 ± 0.0017 | Supported |
| Consistent to 5 keV | FIX2 N2: Δc(2) = +0.005 ± 0.007 / +0.004 ± 0.007 (floor-free: predicted floor +0.0007/+0.0026); Λ exponent 3→5 −1.76 ± 0.09 vs −1.87 | Supported (precision ±9 % in c, ±0.4 % in Δs_B(5)/Δs_B(3)) |
| "+2-5 % B* systematic above 5 keV" | see R3-B1 | **Not supported as a B* magnitude** |

- **c15 / §5.5 derivation.** It is correct.
  - Under x → λx at fixed momenta: dτ → λdτ, dA → λ²dA, and A(λx)·d(λx) = λ²A·dx for A = B×x/2. Hence
    S[λx; m, σ, qB] = λS[x; m, λσ, λqB], and a solution for (σ, qB) maps to λx(t/λ) for (σ/λ, qB/λ).
  - (Λ√k, B) ≡ (Λ, B/k) per oscillation, with N_osc × k. The quoted equivalents 4.24/6.00/13.42 keV are correct.
  - "The weak-field c equals half the slope of ln(Δs/ε_B) in ln Λ at fixed B": ε_B ∝ Λ⁻², so d/d ln Λ = 2 d/d ln(1/ε_B). Correct.
  - c15 is a schematic sympy check, not a solution of the EoM, which is adequate for a scaling identity.
  - One addition for §5.5: the precision floor is scale-free in the same way, since it depends on ε⊥. So it maps onto the B₀ law at
    high Λ in the numerics. This is why the direct B₀ runs at ≥ 10 keV cannot be used (R3-B1).

## 5 Number spot checks (note vs JSON)
| # | Note value | Source | Result |
|---|---|---|---|
| 1 | B* on, s = 1, Δc(20) +0.0121 ± 0.0031 / +0.0122 ± 0.0047 | FIX2 N1 on_s1 | OK |
| 2 | B* off s = 1 +0.0044 ± 0.0008 / +0.0064 ± 0.0020; E*∥ off +0.0039 ± 0.0010 / +0.0062 ± 0.0025 | off_s1, eperp_s1 | OK |
| 3 | on − off s = 1/9, 1/3, 1: +0.0000/+0.0014/+0.0063 ± 0.0023; −0.0005/+0.0010/+0.0024 ± 0.0041; Δc(4) 1 TeV +0.0061 ± 0.0030 | on_minus_off_s* | OK |
| 4 | k_B split on +0.0041/+0.033, +0.0049/+0.035; off +0.0023/+0.0106, +0.0033/+0.0184 | kB_lt5 / kB_ge5 | OK |
| 5 | partial(k_B \| b) B* off 0.82/0.46; Spearman 0.84/0.57; Spearman(k_B, b) −0.37/−0.61 | correlations_c20 | OK |
| 6 | b_odd/ℓ₀(B₀/20) median 1.5×10⁻⁷ / 0.9×10⁻⁷ | b_l0_B20_median | OK |
| 7 | 5 keV Δc(2) +0.005 ± 0.007 / +0.004 ± 0.007; k_B < 5 +0.003 ± 0.002; k_B > 10 +0.08 ± 0.04 (3) | N2 m500_L5, m1000_L5 | OK |
| 8 | implied +0.3/+1.3/+2.8/+4.5 % (500), +0.2/+0.4/+3.4 % (1 TeV) | N2 implied_rel_change | OK (errors: R3-B1.4) |
| 9 | 7 keV 10⁻³ − 10⁻⁴: +0.106, 0.000, +0.031, −0.026, 0.000 | convergence_7keV | OK |
| 10 | M2b ψ_odd 16.566/18.116/21.03, ψ_even 1.631/1.811/3.73 | M2.json g1.3_th90_causal0.001 | OK |
| 11 | M2b ψ_pair excess +0.15 %/+1.7 %/+11 % | same | **+0.16 %/+1.7 %/+18 %** (C3) |
| 12 | FIX1 10⁻⁴: +0.0122 ± 0.0027 / +0.0130 ± 0.0035; E1-k_B bins +0.004/…/+0.116 | FIX1 (via R2 checks, re-read) | OK |
| 13 | f(k_B > 6) 0.053/0.293/0.427; k_B ≳ 10 "10-18 %" | c13 out; FIX1 top bins n = 12/120, 22/120 | OK |
| 14 | B exponent ln(1.455)/ln 80 → 0.914; C = 1/0.104 − 8.397 = 1.22 | arithmetic | OK |

## 6 Checks 5-7
- **P1 scope (b).**
  - Title (line 1) has no "exact"; "classical Nambu-Goto" is used throughout.
  - §0 item 6 and §11: MS only as the measured floor 10-25 µm, Highland [NIM 129 (1975) 497; PDG] credited, "No analytic MS claim".
  - The MS conjecture is moved to §10 item 8 as future work, and credit sentence 7 is deferred.
  - No residual analytic MS claim found by grep. Leftovers C6 and C9.
- **Novelty and credit**, consistent with NOVELTY_AUDIT §0 and §4:
  - "analytic theory of Li et al.'s fitted η" (§0.3, §1.2, App.A Eq.A.6/A.17);
  - Knapen Eq.8-9 m-independent ∝ B/Λ² (§5.2);
  - Kang-Luty Eq.5.64 (§3.2);
  - the log as elementary near-radial orbit mechanics (§4.3, E3 apsidal check);
  - Artru/Lund/Athena (Black, Nelson) construction (§14 sentence 8, Artru/Lund marked UNVERIFIED);
  - KLN §3.2 / Evans-Luty retardation (sentence 9).
  Audit sentence 3's caveat (test the Li B non-linearity first) is satisfied by E2 M5. No over-claim found.
- **PROPOSED_CHANGES.** Items 1, 3-5, 7-8 and 10-14 are correct. Item 2 is stale, item 6 is stale, and the synthesis §5 P1 row and
  the NOVELTY_AUDIT Knapen reading are missing (C9).

## 7 Verdict
**ITERATE** (A = 0, B = 1, C = 10).
- R3-B1: restate the "+2-5 % B*-driven systematic above ≈ 5 keV" as an unmeasured, unattributed provisional systematic. The
  direct-B₀ values at 7-13 keV are not step-converged and contain a floor contribution of comparable size.
- No new runs or derivations are needed. The C items should be applied in the same pass.
- After that, a light check of R3-B1 alone suffices for PASS; no full fourth round is needed.
- Recommended before P1 figures, not required for PASS: either decisive floor test of §3 (higher precision on a short detector, or
  the 44-bit emulation). It would also allow the B₀ law above 5 keV to be measured.
