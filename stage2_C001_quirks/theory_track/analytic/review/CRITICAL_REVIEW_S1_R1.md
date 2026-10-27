# Critical review S1-R1 (Stage 1, theory track, round 1)

Reviewer: S1-R1-critical (independent; did not write any reviewed file). Date: 2026-10-10.
Under review: `analytic/NEAR_MISS_IMPULSE.md` (v3), `predictions.json` (v3), `checks/c01-c12`; `numerics/NUMERICS.md` (+ §11),
`numerics/results/*.json`; `NOVELTY_AUDIT.md`.
Protocol: jfc `03-review.md` + `critical_reviewer.md`, theory-track variant (A = wrong result / would cause rejection;
B = weakens the result, must be fixed before PASS here; C = style/clarity).
My scripts and outputs: `analytic/review/r1_checks/` (`r1_derivations.py`, `r1_fu1_noise_bias.py`, `r1_conf_cm.py`,
`r1_conf_cm_g2.py`, `r1_lab_c.py`, `r1_lab_c_geom.py`, `r1_lab_c_conv.py`, each with `*_out.txt`). CPU used: about 6 min.

## 0 Summary
1. The core analytic chain is correct. I re-derived it independently (sympy, plus my own NR integrator and an E/B extension of
   the R1 conformal-gauge formulation): E* = γβ×B; b_odd = 2ε⊥ℓ₀[γ* − asinh ρ/ρ] (conformal: 0.77873 vs 0.77872 at γ* = 1.3,
   2.47933 vs 2.47931 at γ* = 2); G(γ*); K_NR = 3 ln 2 − 2 (my NR integration: +0.07944); K(1.3) = −0.058 vs E1 −0.0586;
   K(2) = −0.309…−0.314 vs E1 −0.309; c = 1/(L+K); exponents 1 − c, −2 + 2c. No sign or factor-2 error found.
2. The c prediction at 1 keV is not circular. c07 (0.1039) is timestamped 21:04, before E2's M3.json (22:20). An independent
   lab-frame check with the unmodified R1 solver gives median c₄ − c_E1 = +0.0016 on 16 events.
3. **A1.** The 3 keV "reclassification" is only partly supported. Step bias at k = 2 is real. But the claim that the k ≥ 4
   excess comes from round-off is refuted by E2's own replica data. Mean-zero noise enters √λ_min only at second order, so the
   measured noise implies a bias of ~10⁻⁵ in c, against the observed +0.0055 (k = 4) and +0.011 (k = 20). Even at 10⁻⁴ the
   per-event excess is one-sided. "c verified to 2-3 % at 3 keV" rests on one post-hoc-chosen B ratio.
4. **A2.** Stale or contradictory statements. E1 §0.1, §1.2, §1.3 item 4, §4.1 and predictions.json still say "B* inert" and
   "K depends on γ* only". NUMERICS §0/§8 still state K_vac → 0 and c(3 keV) = 0.093. The round-off figures in the text
   (0.26/0.47/0.89 %) do not match FU.json (0.24/0.44/0.74 %).
5. **B1.** The B* effect is mis-characterised. It is ε-dependent and non-monotonic in kB (confirmed with my independent
   solver), and it is not a constant ΔK. The γ* = 1.3 c12 scan (−2.6 % at kB = 8) is omitted from the note. The per-event
   c_ev fails by +17 % to +36 % for the large-kB (small sin α) events in my sample.
6. **B2.** The headline form Δs ∝ ε_B[1 + c ln(Λ²/qB)] with c ≈ 0.10 is inconsistent as written. The consistent form is
   Δs ∝ ε_B[ln(1/ε_B) + C] with C ≈ 1.2.
7. **B3.** Some tags overstate: "DERIVED" for the per-event c, "exact reduction", "exactly linear".
8. Novelty and credit are fine. E3's audit is thorough and I found no missed prior work.
Verdict: **ITERATE** (A = 2, B = 3, C = 8).

## 1 Findings

### A1 — 3 keV: the "round-off" attribution of the k ≥ 4 excess is refuted; "c verified to 2-3 % at 3 keV" is not supported (Category A)
Claims: NEAR_MISS §9.3 FU1/FU1b ("the excess that grows with k … follows the measured round-off amplification"; "Because Δs is
positive-definite, the noise biases R(f) and c upward at large k"; "c is verified to ≈ 1.5 % at 1 keV and ≈ 2-3 % at 3 keV; the
Λ dependence of c … is confirmed"). Also §10 item 11, P-14 (v3), predictions.json `c.comparison_E2.v3_FU1.verdict` ("CONSISTENT")
and `sensitive_dependence_v3`, and NUMERICS §11 FU1 verdict ("floor or chaotic noise at large k").

Evidence (`r1_checks/r1_fu1_noise_bias_out.txt`, from E2's raw `data/stage1_numerics/FU/*.npz`):
1. **The noise is too small, by a factor of ≥ 500 at the median.** Δs = √λ_min (T3_propagator.plane_fit). Mean-zero noise adds
   in quadrature, so the bias in Δs is about (rel. noise)²/2. With the generous bound b(f) = rs(f)² taken event by event from
   the 5 replicas, the implied bias of c_k at 3 keV is median 3×10⁻⁶ / 1.1×10⁻⁵ / 1.4×10⁻⁵ and mean ≤ 5×10⁻⁴ (k = 2, 4, 20).
   The observed fine-step excess is +0.0021 / +0.0055 / +0.0113 (500 GeV) and −0.0003 / +0.0043 / +0.0132 (1 TeV). It
   requires an *upward* bias of Δs(B₀/k) of 0.67 % (k = 4) and 2.6 % (k = 20). The replica noise itself is only
   0.44 % / 0.74 % (median rel. sd).
2. **The excess is one-sided, which noise is not.** On the 10⁻⁴ survivors, c₂₀ − c₂ is positive in 15 of 17 events (one is
   0.000 and one −0.0009). Five events have +0.019 to +0.033 (e.g. 500 GeV ev 14: c_vfine = 0.0695/0.0728/0.1029; 1 TeV ev 6:
   0.0728/0.0754/0.1044). These are converged against 10⁻³ to ≤ 0.007 (`r1_fu1_noise_bias_out.txt` (4)).
3. **Production runs carry the same round-off but show no k-growth.** The replicas were taken at production settings. There,
   c_k = 0.0945/0.0939/0.0928 (flat), while the fine runs give 0.0890/0.0918/0.0961. The paired prod − vfine difference changes
   sign with k (+0.014, +0.002, −0.016; FU.json `step_m500_L3`). So "step bias at small k + round-off at large k" does not
   describe the data.
4. **The scaling claim is not "as observed".** FU1b says the noise grows ∝ √N ∝ Λ. The replica ratio 3 keV / 1 keV at f = 1/20
   is 21 (median) and 9.5 (mean), not 3 (FU.json `roundoff_L1/L3`).
5. **The "clean ratio" criterion is post hoc and inconsistent.** "b_odd/ℓ₀ ≳ 10⁻⁶ ⇒ k ≤ 80 at 1 keV, k ≤ 2-4 at 3 keV". At
   1 keV, b_odd/ℓ₀ ≈ 1.8×10⁻⁵ at B₀, so k = 80 gives 2×10⁻⁷. That is the same as 3 keV at k ≈ 9, where the note calls the data
   unreliable, yet 1 keV k = 80 agrees (c₈₀ = 0.105). Whatever drives the excess is not b_odd/ℓ₀.
6. **The convergence of the 10⁻³ runs is shown only on 8/20 and 9/20 survivors.** 45 % of the 10⁻⁴ runs overflowed. The
   survivors are not representative: their fine c_k growth differs, and their median Δs(B₀) is 2.5 vs 3.8 µm (500 GeV). The
   paired fine − vfine median is ≈ 0, but the rms is 0.005-0.007, the size of the effect.
7. **The same k-growth is present at 1 keV, smaller.** c₂₀ − c₂ = +0.0020 ± 0.0011 (my check on 30 production events), and
   FU1a gives +0.0015 ± 0.0005 at k = 20 (3σ). From 1 to 3 keV it grows roughly ∝ Λ² ∝ N. That points to a per-crossing
   effect that does not scale with B, numerical or physical. It is open, not explained.

What is supported: the blind production c (0.093) was step-biased at k = 2, and at k = 2 the converged measurement agrees with
E1 (pulls 1.4 and −0.5).
Requested fix (either option is acceptable):
- (a) Restate. At 3 keV, agreement is established only at B₀/2. A k-dependent excess (c_k not constant, contrary to the
  predicted per-event linearity) of +5-6 % at B₀/4 and +13-16 % at B₀/20 is unexplained. Its origin, numerical or physical,
  is open. Remove "follows the measured round-off amplification", "biases R(f) upward because positive-definite", "verified to
  2-3 % at 3 keV" and "Λ dependence of c confirmed". Change the predictions.json status to "consistent at k = 2; k ≥ 4 open".
- (b) Demonstrate a numerical origin. For example, show a deterministic, one-signed floor bias, or reproduce the excess on a
  1 keV event with N artificially increased (a longer path at fixed Λ). Note that NG is scale-free, so 3 keV at B₀/20 differs
  from 1 keV at B₀/180 only through N.

Also give the per-event spread of c_k − c_E1, not only medians.

### A2 — Stale or contradictory statements and numbers that do not match the JSON (Category A)
1. **B* "inert" is still asserted** after v3 showed it is not:
   - NEAR_MISS §0 item 1: "B* is inert at first order (§1.3)". This contradicts §0 item 6 and §1.3 item 3 (v3 correction).
   - §1.2 table row "B* drops out at first order".
   - §1.3 item 4: "It depends on γ* and ε⊥ only".
   - §4.1: "everything else is a pure number that can depend only on γ*".
   - predictions.json `assumptions[2]`: "B* inert at first order (DERIVED)".
   The first-order problem depends on B*⊥/E*⊥ (and, per B1, on ε). The "exact reduction" headline must say that.
2. **NUMERICS summary statements contradict §11:**
   - §0 item 1 and §8 Surprise 2: "non-relativistically L = ℓ_max, K → 0". This is superseded by FU2 (L/ℓ_max → 1.083,
     K_vac → 0.0791).
   - §0 item 4: "c = … 0.093 (3 keV)". Superseded by FU1 (0.084-0.089 at k = 2).
   Keeping the blind record is fine, but the summary must flag these in place (e.g. "[superseded, §11 FU2]").
3. **Round-off numbers in the text do not match FU.json** (> 1 %):
   - NUMERICS §11 FU1(b) and NEAR_MISS §9.3 FU1b (also predictions.json `sensitive_dependence_v3`): Δs variation
     "0.15/0.26/0.47/0.89 %". FU.json `roundoff_L3.rel_sd_ds_median` = 0.147/0.236/0.441/0.739 %.
   - p90 "1.3/0.8/1.3/4.8 %" vs 1.14/0.75/1.31/4.81 %.
   - per-event c p90 "0.03/0.014/0.023" vs 0.0178/0.0119/0.0226.
   - FU_stdout.txt equals the JSON, so the text values have no source.
Fix: update all of these in place (E1 and E2 files), or regenerate and quote from the JSON.

### B1 — The B* effect (c12, P-22, §9.3 FU3, §10.12) is mis-characterised and its propagation to c is wrong (Category B)
1. **"The same at ε = 10⁻⁵ and 10⁻⁴" is false for B* ∥ E*.** c12_Bstar_test_out.txt: γ* = 1.3: −1.24×10⁻³ vs −4.37×10⁻³;
   γ* = 2: −4.2 % vs −7.7 %. For B* ∥ z it holds only at kB = 4. My independent conformal runs (`r1_conf_cm_out.txt`,
   `r1_conf_cm_g2_out.txt`) reproduce c12 at kB = 4 (γ* = 2: −6.74 %/−7.33 %; c12: −6.81 %/−7.33 %). They also show that the
   ε-dependence is kB-dependent:

   | γ* | kB | Δη/η at ε = 10⁻⁵ | Δη/η at ε = 10⁻⁴ | ratio 10⁻⁴/10⁻⁵ |
   |---|---|---|---|---|
   | 2 | 2 | −1.84 % | −3.38 % | 1.84 |
   | 2 | 8 | −13.7 % | −12.0 % | 0.88 |
   | 1.3 | 8 | −2.6 % | −0.68 % | 0.26 |

2. **"Enters K, not G" (c rises by |Δη/η|) does not follow.** A constant ΔK implies Δη/η ∝ 1/(L+K), i.e. a ratio
   10.99/8.69 = 1.26 between ε = 10⁻⁴ and 10⁻⁵ at γ* = 2. The observed ratios are 1.08 (kB = 4), 1.84 (kB = 2) and 0.88
   (kB = 8). The effect on c per event is −d(Δη/η)/d ln ε. Its size and sign depend on kB: for example, about +3 % (kB = 4) and
   −8 % (kB = 8) at γ* = 2, and about −8 % at γ* = 1.3, kB = 8. It is not +|Δη/η|.
3. **The γ* = 1.3 scan is omitted.** The note quotes "−0.2 % at γ* = 1.3" (kB = 4). c12_Bstar_kBscan_out.txt has −2.64 % at
   kB = 8 and −2.37 % at kB = 16, a jump of ×12 between kB = 4 and 8 that my independent solver reproduces (−2.61 %, −2.41 %).
   E1's own estimate of lab kB is 2-10. "≤ 0.5 % for γ* ≤ 1.3" and "quadratic at small B*, then logarithmic saturation" are
   not supported (at γ* = 2, kB 1→2 gives ×10.6).
4. **End-to-end failures of c_ev.** With the unmodified R1 solver (`r1_lab_c_out.txt`, converged at N = 16384 in
   `r1_lab_c_conv_out.txt`), 3 of 16 events at γ* = 1.28 deviate from c_ev by +0.016 / +0.032 / +0.035 (+17 % to +36 %).
   They are exactly the events with kB = 8.4-12 (sin α = 0.36-0.47) (`r1_lab_c_geom_out.txt`). Events with kB ≤ 6.5 agree
   within ±0.009. The population median is fine (+0.0016). So the per-event law (P-9, §5.3 "per event … exactly linear") fails
   for a sizeable class of events.
5. **The population bound "±0.5 %" uses the production residual (+0.3 %).** The step-converged subset gives a relative
   per-pair residual of −1.15 ± 0.36 % (FU.json `FU3.fine_first20.all.rel_pair`).

Fix:
- Rewrite P-22, §1.3 item 3 and §9.3 FU3 with the measured ε- and kB-dependence (ESTIMATE). Drop "enters K, not G" or replace
  it with what the data show.
- Restrict the per-event c_ev claim to kB ≲ 6 (or sin α ≳ 0.6), or add B* as an event-level systematic.
- Quote the population-level c uncertainty from the empirical 1 keV agreement (≤ 1.5 %, FU1a; my +1.5 %), not from c12.

### B2 — The headline parametrisation of c is inconsistent as written (Category B)
The task, the synthesis, P1 framing and predictions.json (`c.meaning`: "equivalently Ds ~ eps_B [1 + c ln(Lambda^2/qB)] with the
log referred to the operating point") use Δs ∝ ε_B[1 + c ln(Λ²/qB)] with c ≈ 0.10. Read literally with constant c, that form
gives a B exponent of 1 − c/(1 + c ln(σ/qB)) = 0.944 at 1 keV, not the measured 0.911 (`r1_derivations_out.txt` (d)). The
law E1 actually derives is

**Δs_B ∝ ε_B [ln(1/ε_B) + C(γ*, angles)]**, with C = −ln(γ_cm β_T sin α) + ln[(γ*−1)/(γ* − asinh ρ/ρ)] + K.

Over 0.6-10 keV, E1's own c values give C = 1.25/1.22/1.17/1.28 (population), i.e. Λ-independent. E1's c is the local log
slope c(Λ, B) = 1/[ln(1/ε_B) + C]. "1 + c ln(Λ²/qB)" with a log "referred to the operating point" is not equivalent; that would
be 1 + c ln(B₀/B). Fix: state the law in the ε_B[ln(1/ε_B) + C] form, with C ≈ 1.2 and its spread, as the P1 headline. Present
c(Λ) = 1/[ln(Λ²/qB) + C] as a derived consequence; the predicted fall 0.116 → 0.070 then becomes a test rather than a
nuisance. Correct predictions.json `c.meaning`.

### B3 — Tags overstate (Category B)
- P-9 / §5.3: c_ev is "DERIVED (given P-4)" and R(f) is "exactly linear in ln(1/f)". This also requires Δs ∝ η (accumulation
  model, ESTIMATE; non-secular terms omitted) and neglects B* (B1 item 4). Use "DERIVED under the rotating-yo-yo assumption;
  population median VERIFIED-NUM at 1 keV (≤ 1.5 %)".
- §1.3 "Exact reduction (DERIVED)": the reduction to a pure-E* problem is exact only for the linear dynamics (A2 item 1).
- §4.1 "(DERIVED, constant K by computation)": K now depends on γ*, kB and ε (B1).
- NEAR_MISS §0 item 6 and predictions.json: "3 keV … consistent" should be tagged as in A1.

### C notes (advisory)
- C1 §3.2: "So Eq.III.12 describes the odd-crossing miss distance". Better: "has the scaling of b_odd". Numerically, III.12 gives
  1.16 × 5 × 3.8 ≈ 22 µm × (B_xy/B) at 500 GeV, 1 keV, about 6× the median b_odd.
- C2 §5.2: Knapen Eq.8 as printed is ∝ γ²v²/(γ−1)², i.e. about 4ε/v² in the NR limit, not "ε⊥ × O(1)". E1 says the equation
  was not re-derived; soften the wording or re-derive.
- C3 §10 item 8 can be closed. E3's apsidal slope 0.354 = 1/(2√2) (units m = E = σ = 1, so v₀ = √2 and b = L/√2) gives a
  per-passage rotation 2 × 0.354 L ln(1/L) = (b/ℓ_max) ln(ℓ_max/b), i.e. exactly Â_NR = 1.
- C4 NUMERICS §11 FU1b: "amplify a 10⁻¹⁴ perturbation to 10⁻³-10⁻²" is misleading. Deterministic propagation through the
  (non-chaotic, J-conserving) map would give ~N · 10⁻¹⁴ ln(10¹⁴) ~ 10⁻¹⁰. The replicas sample round-off realisations. This
  supports "numerical, not chaos". A replica test with perturbation sizes 10⁻¹⁴/10⁻¹⁰/10⁻⁸ would make it decisive.
- C5 Quote FU3 `fine_first20.all.rel_pair` (−1.15 ± 0.36 %) next to the production +0.3 %.
- C6 c12 docstring says η comes "from apocentres of quirk 1 AND from the relative coordinate", but the code uses the relative
  coordinate only.
- C7 "KLN" (E3) vs "Kang-Luty" (E1) for 0805.4642: unify (two authors, per the earlier RP-fid check).
- C8 NUMERICS §4.2: "constant within ±2 % from k = 2 to k = 80 (1 keV)" is true for production, but FU1a shows a significant
  (3σ) +1.5 % rise at k = 20 for 500 GeV. Mention it.

## 2 Independent re-derivations (`r1_checks/r1_derivations.py` → `_out.txt`)
(a) **Frame and fields.** With the general boost, E' = γβ×B and B' = γB − (γ−1)(B·β̂)β̂ for a pure lab B (sympy: True/True).
The force bookkeeping for x₂ = −x₁, v₂ = −v₁, q₂ = −q₁ gives:
- relative force 2qE* (no B*);
- CM force 2q v₁×B* (shake);
- torque about the CM 2q x₁×E* = q(x₁−x₂)×E*, with no B* torque.
§1.3 items 1-3 are therefore correct *for linear response*. The v3 inner-region effect is beyond this, as E1 says (see B1).

(b) **b_odd.** I = ∫₀^{T_h} x dt = 2ℓ₀²(γρ − asinh ρ) (sympy), and b_odd = εσI/p* = 2εℓ₀[γ − asinh ρ/ρ]. The series
γ − asinh ρ/ρ = 2ρ²/3 − ρ⁴/5 gives the NR limit (4/3)qEmβ²/σ².
- Li: z⁻ ≡ (z₁ − z₂)/2 [2002.07503 Eq.II.18], and A.13 at g = 1 equals 2ρ asinh ρ (Eq.V.8 confirmed). So
  d_E/(b_odd/2) = 2ρ asinh ρ/(γ − asinh ρ/ρ) = 3.040/3.213/3.680/4.195 at γ* = 1.05/1.28/2/3, NR limit 3. E1's "3.0-4.2" is
  correct.
- KL Eq.5.64 [0805.4642 l.1600] has the scale q v_cm B m/σ², as credited.

(c) **G and K.** G = 2[γ − asinh ρ/ρ]/(ρ artanh β) → 4/3 − 8β²/45 (sympy), and σb_odd/(p* artanh β*) = εG (identity). G values
1.3159/1.2449/1.2393/1.1651/1.0869/0.9534 at γ* = 1.05/1.28/1.3/1.6/2/3 match the note.
My own NR two-body integration (relative coordinate r̈ = −r̂ + εŷ, DOP853, rtol 10⁻¹³, apocentre angles; no matched
asymptotics) gives, at ε = 10⁻⁶ … 10⁻⁴:
- b₁/((2/3)ε) = 1.000001 … 1.00007;
- K = η/((4/3)ε) − ln(3/(4ε)) = +0.07944 (to 5 digits for ε ≤ 3×10⁻⁵) = 3 ln 2 − 2;
- ψ_even/ε = 1.5909 = 2/3 + (4/3) ln 2;
- ψ_odd/ε = 13.4821 at ε = 10⁻⁵ = (4/3)[ln(1/ε) + ln 3 − 5/2];
- sign: toward +E*⊥.
So P-6, P-7 and P-20 are confirmed independently.

(d) **c and exponents.** For Δs ∝ (B/Λ²)[ln(Λ²/qB) + C]: d ln Δs/d ln B = 1 − c and d ln Δs/d ln Λ = −2 + 2c with
c = 1/(L+K) (sympy). This is correct; for the convention problem see B2.

Hidden assumptions checked:
- Coherence holds: J_odd ∥ n̂ × ê⊥ in every period; Θ ≲ 10⁻² keeps ê⊥ fixed.
- ε⊥ is consistently ⊥ to the initial n̂.
- "Response per unit B" is the same R(f) in E1 and E2.
- The plane fit includes the pre-crossing hits (linear, no log). This slightly lowers c and is part of the omitted
  non-secular terms (§10 item 3). Not a significant problem at ≥ 1 keV.

## 3 Independent numerical spot checks
1. **Relativistic CM frame, independent formulation** (`r1_conf_cm.py`): R1's conformal-gauge delay-ODE equations, own E/B
   extension (not E2's nm_conformal, not the causal kernel). The exactly head-on even crossing breaks the conformal gauge (as
   E2 documents), so I used an initial offset ±0.03 b_odd, averaged over sign, which cancels the offset at first order (O(f²)
   residual measured with f = 0.3: ΔK = −0.055, hence −0.0006 at f = 0.03).
   - γ* = 1.3: b₁/(εℓ₀) = 0.77873 (E1 0.77872); K = −0.0587 at ε = 10⁻⁵ and 10⁻⁴, −0.0578 at 10⁻³, N-converged
     (1024 = 4096 to 10⁻⁵); E1 −0.0586. So the slope equals G to < 0.1 %.
   - γ* = 2: b ratio 1.00001; K = −0.314 (10⁻⁵) / −0.309 (10⁻⁴); E1 −0.309.
2. **c at 1 keV, lab frame, unmodified R1 solver** (`r1_lab_c.py`): 16 events (γ* = 1.28, p_T = 300 GeV), B₀ and B₀/4,
   N = 4096. The median c₄ is 0.1050 vs median c_E1 0.1028; the median per-event difference is +0.0016 (1.5 %); the mean is
   +0.0057 ± 0.0030, driven by the large-kB outliers of B1 item 4.
3. **Re-analysis of E2's FU raw files** (`r1_fu1_noise_bias.py`): see A1.

## 4 Number spot checks against the machine outputs
| # | Note value | Source value | Result |
|---|---|---|---|
| 1 | c = 0.104 (0.098-0.112), 500 GeV, 1 keV; all 18 entries of the §5.3 table | c07_out: 0.1039 (0.0984-0.1118); all entries | OK |
| 2 | Λ exponents −1.79/−1.86/−1.78/−1.87/−1.84; 1→3 −1.83, 3→10 −1.85 | c07_out −1.794 … −1.836; from medians −1.827, −1.851 | OK |
| 3 | R(1/4, 1/20, 1/80, 1/1000) = 1.144/1.311/1.455/1.718; 3 keV 1.117/1.253/1.371/1.584 | c07_out | OK |
| 4 | K table +0.056/−0.049/−0.175/−0.309/−0.569 | c03_out_mb1e-4: +0.0563/−0.0490/−0.1754/−0.3095/−0.5688 | OK |
| 5 | E2: R = 1.073/1.147/1.320/1.460; c_k = 0.105/0.106/0.107/0.105; 3 keV 0.095/0.094/0.093 | M3.json `b_scan` | OK |
| 6 | b_odd/(εℓ₀) = 0.1328/0.7790/2.480/4.755 | M2.json M2b (causal 10⁻³) | OK |
| 7 | FU1 fine − E1 = +0.0021 ± 0.0015 / +0.0055 ± 0.0020 / +0.0113 ± 0.0018; 1 TeV −0.0003/+0.0043/+0.0132; c(k=2) 0.0890/0.0841 | FU.json `step_*_L3` | OK |
| 8 | K_vac 0.0709/0.0627/0.0382/−0.158/−0.560/−0.965; extrapolation 0.0791 | FU.json `FU2_blmax_le_1e-4` | OK |
| 9 | FU3 res_pair γ* bin 1.0-1.1 = +0.53 | FU.json `FU3.prodall` +0.525 | OK |
| 10 | Round-off Δs 0.15/0.26/0.47/0.89 %, p90 1.3/…, c p90 0.03/… | FU.json 0.147/0.236/0.441/0.739 %, p90 1.14/…, 0.0178/… | **mismatch (A2)** |
| 11 | P-12 1 − c = 0.884/0.896/0.915/0.930; P-11 −1.77/−1.79/−1.83/−1.86 | from c07 c values | OK |
| 12 | b_odd/(εℓ_max) 1.3268/1.2979/1.2397/1.1884; G 1.316/1.239/1.087/0.953 | my sympy | OK |

## 5 Circularity and blinding audit
- **Timeline (file mtimes).** E1's c01-c08 and the c07 population predictions date from 20:37-21:04; M3.json (the c and B
  exponent measurements) is from 22:18-22:20. The c prediction (0.1039 in c07_out) predates the measurement. predictions.json
  says "No v1 value changed", which matches c07_out.
- M2.json (21:01) predates c03_mb1e-4 (21:02) and c08 (21:03). But the K values come from E1's own c03 runs, not from M2, and
  K agrees with my independent conformal check.
- **K vs validation code.** E1's K uses T2's CausalNullString, and E2's thickness uses a copy of T3_causal (same algorithm
  family). The circularity risk is therefore partial dependence on the solver family, not tuning. My conformal K(1.3) and K(2)
  remove it. K enters c at ≤ 6 %.
- **Blindness of E2** is asserted (NUMERICS header) and is plausible: E2's blind statements include errors that E1's v1 would
  have corrected (K_vac → 0).
- **Post-hoc elements:**
  - P-19-P-22 are correctly labelled post-hoc.
  - The 3 keV "clean ratio" selection (k = 2 only) and the b_odd/ℓ₀ ≳ 10⁻⁶ criterion were introduced after seeing the
    k-dependence, and the criterion is inconsistent (A1 item 5). This is the one place where the analysis drifts toward
    explaining away a discrepancy.
  - The prior knowledge of the fitted c ≈ 0.10 is disclosed, and no parameter was adjusted toward it.

## 6 Novelty and credit
- **Supported by NOVELTY_AUDIT:**
  - "analytic theory of Li et al.'s η" (credited: 2002.07503 App.A, A.6, A.17, V.5-V.6);
  - b-scale credited to KL Eq.5.64;
  - the non-log m-independent rotation credited to Knapen Eq.8-9;
  - "the logarithm itself is not new" (near-radial orbit mechanics, E3 check);
  - "Li integrators have the log" (E2 M5).
  No statement in E1/E2 claims more than the audit supports, apart from the C1 wording on Eq.III.12.
- **Prior work.** The audit covers 1106.2569, 1703.00912, 1811.08903, the BKN/Sharov massive-charged-end literature and Li §VIII
  (fixed-ŝ). I know of no missed work that I could verify. A textbook reference for apsidal angles of near-radial orbits in
  power-law potentials would be nicer than E3's own check (not verified by me, so not asserted).

## 7 Physics validity
- **Classical NG at b < 1/Λ.** Odd crossings have b_odd Λ ≈ 1.8×10⁴ (keV/Λ)³ (checked: 3.5 µm / 1.97 Å), so this is fine for
  Λ ≲ 26 keV. Even crossings: b_even < 1/Λ is irrelevant to the log term (it is absent at first order); the smooth ψ_even is
  generated over the half-period. The statement is acceptable as written.
- **γ* ≳ 2 accumulation model (10-35 % off).** It is correctly tagged ESTIMATE and affects population medians at the few-%
  level (about 15 % of events). Part of it is plausibly B* (B1); with B1 fixed, say so quantitatively or not at all.
- **"Sensitive dependence is numerical".** Supported by my estimate (C4): deterministic propagation would give ~10⁻¹⁰. But the
  inference "therefore it biases c upward" is wrong (A1). The "physical analogue" paragraph is fine as CONJECTURE.

## 8 Verdict
**ITERATE.** Category A: 2 (A1, A2). Category B: 3 (B1, B2, B3). Category C: 8.
The derivation of the per-crossing law (b_odd, G, the log, K_NR, NR closed form) and the 1 keV c / B exponent agreement are
correct and independently confirmed. The fixes concern:
- (A1) the 3 keV claim and its unsupported round-off explanation;
- (A2) stale or contradictory statements and numbers;
- (B1) the characterisation of the B* effect and the per-event validity of c_ev;
- (B2) the headline parametrisation;
- (B3) tags.
None requires redoing the derivation. A1(b) and B1 would benefit from targeted runs.
