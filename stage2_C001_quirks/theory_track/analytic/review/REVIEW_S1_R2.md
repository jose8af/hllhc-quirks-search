# Review S1-R2 (Stage 1, theory track, round 2)

Reviewer: S1-R2 (fresh; took no part in round 1 or in writing the files). Date: 2026-10-11.
Under review: `NEAR_MISS_IMPULSE.md` v4, `predictions.json` v4, `checks/c13`, `checks/c14`, `numerics/NUMERICS.md` v2 (§1.4, §1.5, §11,
§12), `results/FU.json`, `results/FIX1.json`, `NOVELTY_AUDIT.md`, `PROPOSED_CHANGES.md`.
Protocol: jfc `03-review.md` and `critical_reviewer.md`, theory-track classes (A = wrong / rejection; B = must fix before PASS;
C = style).
My scripts and outputs are in `review/r2_checks/`:
- `r2_kB_confound.py` re-analyses E2's raw data, with no new runs;
- `r2_spot2.py` part S is the scale-free test (output `r2_spot2_partS_out.txt`);
- `r2_spot3.py` compares the causal and conformal solvers on the round-1 events and gives C;
- `r2_spot.py` was aborted with no output.

CPU used: about 50 min, over the 30 min budget. Two runs were lost because the unmodified R1 conformal solver does not finish
at 2 keV in a weak field, and an alarm guard cannot interrupt numba code. The kept results cost less than 3 min.

## 0 Summary
1. Round 1 is largely resolved: critical A2, B1, B2 and B3 and constructive B1, B3-B10, B12 and B13 are done, with small
   leftovers. For critical A1 the requested restatement is done: the round-off attribution and "verified to 2-3 %" are
   withdrawn, and the per-event spread is given. However, the note replaces it with a new attribution, "the excess is a B*
   effect", which the evidence does not support (N1).
2. Core physics is unchanged and still holds. My causal re-runs reproduce the round-1 conformal c₄ event by event to ≤ 0.001.
   For k_B < 6.5 the measured C (two solvers) is 1.15 against E1's 1.23. The |q| = 2 law matches E2's own f = 2 point to 0.1 %.
3. **N1 (B).** The weak-field excess at 3 keV is attributed to B* in §0, §9.3, P-14 and predictions.json. In the data, k_B and
   b_odd/ℓ_max are collinear (Spearman −0.9). The partial correlations favour small b_odd. My scale-free test runs the same
   events at 1 keV over the same per-period field window (B₀/9 → B₀/180). It finds about half of the excess there (+0.006 to
   +0.008, also rising with k_B), so the other half grows with the number of periods. c14 has the opposite k_f trend. The
   statement should be "origin open", not "explained qualitatively".
4. **N2 (B).** The impact statement says only the weak-field response at Λ ≳ 3 keV is affected. Classical NG is scale-free, so
   (3 keV, B₀/k) is the same per-period physics as (3√k keV, B₀). The measured per-period part therefore enters the B₀ law at
   Λ ≈ 5-13 keV, inside the claimed range: about +1.5-2 % on Δs_B in the population, and 10-40 % in c for events with k_B ≳ 10.
5. **N3 (B).** "C Λ-independent to ±0.01, as the derivation requires" is true by construction. C is the median of the per-event
   formula, and the ±0.01 is the rounding of c. The empirical support is much weaker, and the note should say so.
6. **N4 (B, minor).** The in-plane vs out-of-plane check is called "confirmed" from data that do not test it cleanly. The
   selected PS/2S layers at 500 GeV agree within 1 %, but IT and 1 TeV differ by 3-30 %.
7. Item 3(b) of my brief: E2's Δc(1/20) values of +0.004 → +0.116/+0.135 are correct. They are absolute units of c, in E1's
   k_B (B*⊥) bins, top bin k_B > 10 (n = 12 and 22). There is no typo. They are consistent with the population +0.012.
8. The failed Li/exact prediction at γ* = 2 is reported honestly. Novelty statements match NOVELTY_AUDIT. PROPOSED_CHANGES is
   correct but has one stale item and gaps (C).
Verdict: **ITERATE** (A = 0, B = 4, C = 10). Every fix is a restatement with no rederivation. The single most useful new run
is the scale-free test with B* switched off, or the same test at max_boost 10⁻⁴.

## 1 Round-1 resolution
| Round-1 item | Status | Evidence (file, section, number) |
|---|---|---|
| Crit. A1 (3 keV round-off attribution; "verified 2-3 %") | **Resolved as asked; replaced by a new over-claim (N1)** | Withdrawn in E1 §9.3 l.520-526 and predictions.json `sensitive_dependence_v3`. E2 did option (b): 39/40 events at 10⁻⁴ (FIX1 `A1b_vfine40`); replica size test, mean shift ≤ 5×10⁻⁴ (FIX1 `replicas`); per-event p16-p84 given (NUMERICS §12.1). Leftover: NUMERICS §11 FU1(b) l.394 "A positive-definite thickness with such noise is biased upward … fits the k_f-dependent excess" is not flagged (C1) |
| Crit. A2 (stale statements, round-off numbers) | Resolved (minor leftovers, C2) | E1 §1.4 items 3-4, §4.1 and predictions `assumptions[2]` are now restricted to linear dynamics. NUMERICS §0 items 1 and 4, §4.2 and §8.2 are flagged "[superseded → …]". Round-off numbers match FU.json `FU1b.roundoff_L3` (0.147/0.236/0.441/0.739 %, p90 1.14/0.75/1.31/4.81 %). Leftover: predictions `assumptions[-1]` (v3 "±0.5 % on c") is unflagged |
| Crit. B1 (B* characterisation) | Resolved | §6.4 table has the ε- and k_B-dependence, reviewer values, and non-monotonicity. "Enters K, not G" is withdrawn. Per-event c fails at k_B = 8-12 (+17…+36 %). Fractions: f(k_B > 6) = 0.053/0.293/0.427 (c13 ✓). Population uncertainty comes from the 1 keV agreement |
| Crit. B2 (headline parametrisation) | Resolved in form; new over-claim (N3) | §0 item 4, §5.2, P-9 use Δs ∝ ε_B[ln(1/ε_B) + C]. C = 1/c − ln(1/ε_B) recomputed from c07: 0.437/1.228/1.623 ✓. The literal form is withdrawn (0.944) |
| Crit. B3 (tags) | Resolved | §5.3, P-9 and P-10 read "DERIVED under the rotating-yo-yo assumption; population VERIFIED-NUM at 1 keV". §1.4 reads "linear dynamics: DERIVED" |
| Crit. C1-C8 | Resolved | §3.2 "has the scaling"; §5.2 Knapen (but see C4); §4.3 apsidal; §9.4; FU3 −1.15 ± 0.36 % quoted; c12 docstring; Kang-Luty; §9.2 row 12 |
| Constr. B1 (framing) | Resolved | §0, §5.2 |
| Constr. B2 (title/MS scope) | Acceptable: documented and decision deferred to the user | §11 options (a)/(b); "exact" is to be replaced in both |
| Constr. B3 (Δs definition; in/out-of-plane) | Definition resolved; check over-claimed (N4) | §1.3 |
| Constr. B4 (accuracy per γ* bin) | Resolved (C9 on wording) | §5.1 table, c13 (2) ✓ |
| Constr. B5 (solver lineage) | Resolved | E1 §9 intro = NUMERICS §1.4 table |
| Constr. B6 (discrepancies) | (a) see N1; (b) resolved, honest FAILED; (c) resolved (432/432 events reproduced exactly); (d) resolved (+0.248 → +0.029 ε⊥) | §9.3-9.5; FIX1 `B6ii`, `B6iii` |
| Constr. B7 (q, scalar) | Resolved (C6: cite the direct check) | §6.5; c13 (4) ✓ |
| Constr. B8 (angles) | Resolved | §6.3. Formula re-derived here: N̂ = (0, sin φ*, −cos φ*), f_N = \|sin φ*\|/sin α ✓ |
| Constr. B9 (notation) | Resolved (C3 leftover) | E1 §1.1, NUMERICS §1.5 |
| Constr. B10 (§0) | Resolved | §0 |
| Constr. B12 (Knapen, Li wording) | Resolved ("10-15×" withdrawn; "same order") (C4 on the Eq.9 reading) | §5.2 |
| Constr. B13 (upstream cascade) | Mostly resolved (C7) | PROPOSED_CHANGES items 1-11 |

## 2 New findings

### N1 (B): the 3 keV weak-field excess is not shown to be a B* effect
Claims: §0 item 5 ("is a B* effect"), §9.3 ("explained qualitatively … the physical B* effect of §6.4"; "c14 gets the right size"),
§10.1, P-14 ("origin explained"), predictions.json `v4_FIX1.verdict`, NUMERICS §12.1(c) ("explained in origin").

Evidence:
1. **Confounding.** In lab events k_B ≈ sin(n̂, ẑ)/(β_T sin α), so a large k_B goes with a small ε⊥ and a small b_odd. The 3 keV
   fine runs (E2 FU, 118/119 events, `r2_kB_confound_out.txt`) show:

   | quantity | 500 GeV | 1 TeV |
   |---|---|---|
   | Spearman(k_B, b_odd/ℓ_max at B₀/20) | −0.91 | −0.88 |
   | Spearman(Δc(1/20), k_B) | 0.65 | 0.68 |
   | Spearman(Δc(1/20), b_odd/ℓ_max) | −0.67 | −0.78 |
   | partial: Δc vs k_B, controlling b_odd/ℓ_max | +0.13 | −0.02 |
   | partial: Δc vs b_odd/ℓ_max, controlling k_B | −0.25 | −0.53 |

   2D split at 1 TeV, k_B ≥ 5: Δc(1/20) is +0.065 ± 0.016 (small b, n = 54) against +0.009 ± 0.006 (large b, n = 11). Low k_B
   with small b also shows an excess (+0.016/+0.026, n = 5-6). The data do not separate "B*" from "small field-driven miss"
   (closer to the solver floor, or any ε⊥-dependent effect), and where they can, b_odd wins.
2. **Scale-free test** (`r2_spot2_partS_out.txt`; causal, max_boost 10⁻³, M3 events 0-59). Classical NG is scale-free, so
   (1 keV, B₀/9 → B₀/180) has the same per-period ε⊥, b/ℓ₀, γ*, k_B and α as (3 keV, B₀ → B₀/20). Only the number of periods
   (9× fewer) and the lever differ, and c_E1 is identical. Results:

   | | 3 keV, E2 FU | 1 keV, same window | paired 3 keV − 1 keV |
   |---|---|---|---|
   | c − c_E1, all, 500 GeV | +0.0127 ± 0.0033 | +0.0059 ± 0.0018 | +0.0066 ± 0.0022 |
   | c − c_E1, all, 1 TeV | +0.0137 ± 0.0043 | +0.0078 ± 0.0022 | +0.0048 ± 0.0026 |
   | 1 keV value in k_B bins < 5 / 5-10 / > 10, 500 GeV | — | +0.0023 / +0.0106 / +0.037 | — |
   | 1 keV value in k_B bins < 5 / 5-10 / > 10, 1 TeV | — | +0.0025 / +0.0138 / +0.019 | — |

   About half of the excess is per-period: it is present at 1 keV when the same field window is probed, and it also rises with
   k_B. The other half grows with the number of periods. "Absent at 1 keV" (NUMERICS §12.1, E1 §9.3) holds only because the
   1 keV B scan (f ≥ 1/20, or 1/80) does not reach that window. The ε dependence used as support for B* is therefore not
   established as such.
3. **The per-period part is physical at 1 keV for large k_B.** For the round-1 events, E2's causal kernel (my run,
   `r2_spot3_out.txt`) reproduces the unmodified R1 conformal c₄ event by event: median |Δ| ≤ 0.001, with the k_B = 8.4-12
   outliers at +0.030/+0.035/+0.016 in both solvers. b/ℓ₀ there is about 10⁻⁶, far above the floor. So a physical small-sin α /
   large-k_B effect exists, and B* is a fair candidate for that part.
4. **c14 does not get the right size or pattern.**
   - At k_f = 20 (3 keV-like), c14 gives Δc ≤ +0.016 at γ* = 1.6 and ≤ +0.002 at γ* ≤ 1.3. Full events give +0.047/+0.096 in
     the k_B^tot 7-10 and > 10 bins.
   - c14's Δc falls with k_f (largest at k_f = 2). The full-event excess rises with k_f.
   - c14 has no effect at γ* = 1.1. Full events have +0.007 ± 0.002 in the γ* 1-1.15 bin at k_f = 20 (FIX1 `by_gstar`), and
     corr(Δc, γ*) = −0.05.

Requested fix: restate §0 item 5, §9.3 verdict, P-14, §10.1, predictions.json and NUMERICS §12.1(c) along these lines: "origin
open. The excess correlates with a small field-driven miss b_odd/ℓ_max (equivalently a large k_B). About half is per-period
physics, present at 1 keV in the same field window and seen by both solvers for large-k_B events; plausibly B*, not derived. The
other half grows with the number of periods, origin unknown." Drop "c14 gets the right size". A decisive run would be the
scale-free pair with B* removed (pure-E* forcing in the pair frame) or at max_boost 10⁻⁴.

### N2 (B): the stated impact at B₀ conflicts with scale invariance
Claim: §9.3 "Only the weak-field response at Λ ≳ 3 keV (B ≤ B₀/4), not used at a collider, carries the open B* term". Also "c at
B₀ is verified … at 3 keV through B₀/2".
- Δs_B/(ε_B R) = F[ln(1/ε_B) + C] depends on B and Λ only through ε_B, apart from the number of periods. So the window
  (3 keV, B₀ → B₀/20) is, per period, the B₀ law from Λ = 3 to 13.4 keV.
- The per-period part of the excess (N1.2: +0.006-0.008 in c) therefore enters the B₀ Λ-dependence at Λ ≈ 5-13 keV, inside the
  claimed 0.6-10 keV range of P-9 and P-11. In size it is about +1.5-2 % on Δs_B(13 keV)/Δs_B(3 keV) for the population, plus
  the period-number-dependent part, which is larger at the real N. For k_B ≳ 10 events it is +0.02-0.04 in c (20-40 %).
- E2's B₀ Λ exponents (3→5: −1.76 ± 0.09, 5→10: −1.74 ± 0.14, against −1.87/−1.84) cannot resolve this.

Fix: replace the sentence. State the impact on the B₀ law above ≈ 5 keV (population ≈ +2 % on Δs_B at 10-13 keV plus an unknown
period-number-dependent part; per event up to tens of % in c for k_B ≳ 10). Either restrict the "verified" range of P-9 to
Λ ≲ 3-5 keV, or add this as a systematic. The ≈ −1 % population effect at B₀ (FU3, per-pair rotation) is supported and can stay.

### N3 (B): "C Λ-independent to ±0.01, as the derivation requires" is a tautology
- c07 computes c as the median of the per-event formula c_ev = 1/[ln(1/ε_B) + C_ev] (c07 docstring). The median is preserved
  under the monotone map, so C_pop = median(C_ev) is Λ-independent by construction.
- The quoted ±0.01 is the 4-digit rounding of c (δc = 5×10⁻⁵ ⇒ δC ≈ 0.005).
- Empirical support for C in exact NG:
  - E2's c at 1 keV, 0.105 ± 0.002, gives C = 1.13 ± 0.18 (E1 1.23).
  - At 3 keV, B₀/2 (paired +0.0017 ± 0.0021), C changes by ≈ −0.24 ± 0.3.
  - My two-solver check on 16 events at 1 keV gives median C = 1.145 (conformal) and 1.147 (causal) for k_B < 6.5, against
    E1's 1.228. For k_B ≥ 6.5 it gives ≈ 0.0 against 2.14.
  - The Λ exponents test C only to about ±(1-2).

Fix: in §0 item 4, §5.2 and P-9 say "Λ-independent by construction of the per-event law (rotating-yo-yo model). Verified: C at
1 keV to ≈ 0.1-0.2 (population and k_B < 6.5 events), at 3 keV only at B₀/2, and above ≈ 5 keV see N2".

### N4 (B, minor): the in-plane vs out-of-plane check is over-claimed
§1.3 says "Equal within 1 %: confirmed" and cites `figures/S_Bnonlin_out.txt` (T4 kernel, 6 events) against E2 M3 (120 other
events).
- The quoted PS/2S values at 500 GeV, 1 keV agree: R(1/4) = 1.145/1.150, R(1/20) = 1.306/1.325, against 1.139/1.319.
- The omitted values do not: IT at 500 GeV has R(1/20) = 1.222. At 1 TeV, IT has 1.015/1.074 and PS has 1.109/1.253, against
  out-of-plane 1.147/1.308.
- The rφ displacement also contains the exactly linear CM bending and pre-crossing hits, which pull R towards 1. So it is not a
  clean test of the in-plane rotation response.

Fix: write "consistent for PS/2S hits at 500 GeV; not a clean test (rφ includes the linear CM bending); IT and 1 TeV lower".
Alternatively run the c06-type comparison the constructive reviewer asked for.

### C notes
- **C1** NUMERICS §11 FU1(b) l.394: the unflagged "positive-definite … biased upward … fits the excess" sentence. Flag it as
  withdrawn.
- **C2** predictions.json v3 remnants without a v4 flag:
  - `assumptions[-1]` "±0.5 % on c, up to 9 % in the tail";
  - `c.comparison_E2.v3_FU1` "k=20 … (numerically unreliable)";
  - `accumulation.accuracy_vs_causal` "1-4 % per event". It is a median; the per-event range reaches 0.877-1.123 at γ* < 1.6;
  - `straight_string_models.statement` "nearly the same c" (scope, see C5);
  - `regime_of_validity` "per-period law exact at first order for all gamma*".
- **C3** E1 §9.3 quotes E2's k_B^tot numbers (+0.001/…/+0.096, r = 0.74) under the binding symbol k_B (= \|B*⊥\|/\|E*⊥\|). In
  E1's k_B they are +0.004/+0.011/+0.019/+0.031/+0.116. The (ii) errors should read ±0.0012/±0.0005, not ±0.0014/±0.0006.
- **C4** Knapen Eq.9. The text layout of 1708.02243 (superscript under v_cm, at the denominator v) and the NR limit of their
  Eq.8 (4ε_B v_cm/v²) both point to 10⁻⁵ (v_cm/v²)(B/2T)(2 keV/Λ)², not v_cm²/v². That reading gives Eq.9 = 6.4×10⁻⁶ at the
  benchmark, ≈ 10× (not 40×) below Eq.8, and ≈ 6.4 µm (not 1.6 µm) at 1 m against 4.5 µm causal. The "same order" conclusion is
  unchanged. Check the PDF; the same reading is in NOVELTY_AUDIT §4 (C2 row).
- **C5** "Li has the log with c within ≈ 3 %" (§4.4, P-17, §9.5) is measured at γ* = 1.28 only (M5). E1's own K_KL(2) = −1.8 and
  b ratio 1.68 imply c_KL ≈ 1.25 c_NG at γ* = 2. Scope it to γ* ≲ 1.3.
- **C6** |q| = 2 can be upgraded. q enters only via qB, so |q| = 2 is exactly B → 2B. E2's M3 f = 2 point gives per-event
  Δs(2B₀)/Δs(B₀) = 1.849 (500 GeV) and 1.857 (1 TeV), against E1's 2[1 − c_E1 ln 2] = 1.857/1.863 (ratio 0.999 ± 0.001,
  `r2_kB_confound_out.txt` (3)). Cite this and tag it VERIFIED-NUM.
- **C7** PROPOSED_CHANGES:
  - Item 10 still says the γ* = 2 Li ratio is 0.69 and "open". It should read FAILED, 0.50 vs 0.75 ± 0.08 (FIX1).
  - Missing synthesis echoes: the §0.1 notation row (l.88, "Physically, this is what the formula d describes"); the priorities
    row l.925 ("derive … c ≈ 0.10", to be marked done); and the "10-30 % for Λ ≳ 10-20 keV" echoes at l.664 and l.977 (item 3
    names X-13 and §3.0 only).
  - Item 2 should carry the caveats: per event not valid for k_B ≳ 6; 3 keV only at B₀/2 (and N2).
  - The T2 erratum (1), S-3/X-2/X-3/§5 (2-6) and S_Bscan R(10⁻³, 10⁻⁴) (7-8) are otherwise correct.
- **C8** E1's VERIFIED-NUM allows one solver; E2's VERIFIED means two solvers. Add one line mapping the two tag systems (the E1
  §9 lists are consistent with NUMERICS §1.4).
- **C9** §5.1 table: give n per bin in the text (2 events in 1.6-2.0, 6 in 1.35-1.6). "1-4 %" is a median accuracy.
- **C10** The Li/causal γ* = 2 ratio: the 10-event 3×10⁻⁴ subset has median 0.96 ± 0.10 (FIX1 `B6i`) against 0.75 ± 0.08 on 30.
  Mention it, since it shows the sample sensitivity of the "3σ" statement.

## 3 Item-by-item answers to the brief
- **3(a) Headline law.** C is not fitted. The per-event formula is derived with numerical K, and the population C is a model
  median on the T3 sample. "Λ-independent ±0.01" is a tautology (N3).
  - The m dependence of C (0.43/1.23/1.62) is consistent with "nearly m_Q-independent". The derivation gives F independent of m
    and γ_cmβ_T, because N ∝ 1/(γβ) cancels η ∝ γβ. At fixed p_T, C adds +13 % from 200 to 1000 GeV (1 keV) and the γ* spectrum
    subtracts more. The model medians are 33.5/31.1/29.5 µm and E2's are 28.7/29.1/31.0, both flat within errors. Consistent.
- **3(b) The 3 keV excess.**
  - "Explained qualitatively, size open" is not fair (N1).
  - The −1 % population impact at B₀ (FU3 rel_pair −1.15 ± 0.36 %, 20 events) and −4…−9 % in the γ* > 1.35 tail are supported
    as per-pair rotation residuals at B₀.
  - "Only the weak-field response is affected" is not supported (N2).
  - The "+0.004 to +0.12-0.13" number is correct: FIX1 `by_kB_perp`, k_f = 20, absolute c, top bin k_B > 10, n = 12 and 22.
    The 500 GeV value is ±0.058 (2σ). It means R(1/20) larger by ≈ 0.35 in those events. Since that bin holds 10-18 % of events,
    it is compatible with the population median of +0.012.
- **3(c) Li at γ* = 2.**
  - Reported honestly as FAILED in §4.4, §9.5, §10.6, P-17 and predictions.json, with candidate causes that are not quantified.
  - "c within ≈ 3 %" is supported at γ* = 1.28 only (M5: R(1/80) 1.447 vs 1.467 on 6 events, 1.461 vs 1.459 on 30) (C5).
- **3(d) Charge, scalar, angles, in/out-of-plane.**
  - |q| = 2: derivation correct, and verified with E2's data (C6).
  - Scalar 36 vs 31 µm: c13 (4) ✓. It is a model number, and 32 % of scalar events lie where the model is 10-35 % off; flagged
    ESTIMATE with "≈ 2× model uncertainty". Fine.
  - η_N ∝ \|sin φ*\|: re-derived ✓; c13 (3) numbers ✓.
  - In/out-of-plane: N4.
- **3(e) Knapen.** The Eq.8 value 6.1×10⁻⁵ is reproduced (my 6.2×10⁻⁵) and η = 8.9×10⁻⁵ is reproduced. "Same order" holds. The
  Eq.9 reading is probably wrong (C4).
- **5 Tags.** Consistent with NUMERICS §1.4, except the over-claims N1, N3 and N4 and the tag-system note C8.
- **6 Novelty.** Consistent with NOVELTY_AUDIT. "Analytic theory of Li's η" and "the log itself is elementary" are both kept.
  Credit sentences 1-10 are mapped in §13. No over-claim found.
- **7 PROPOSED_CHANGES.** C7.

## 4 Independent numerical checks
| # | Check | Result | File |
|---|---|---|---|
| 1 | Causal (E2 kernel) vs unmodified R1 conformal c₄, 16 round-1 events, 1 keV, B₀ → B₀/4 | median conf − caus −0.0001, max \|Δ\| 0.0012; large-k_B outliers reproduced (+0.030/+0.035/+0.016 vs c_E1) | r2_spot3_out.txt |
| 2 | C from two B values, two solvers, 1 keV, 500 GeV | k_B < 6.5 (n = 12): C = 1.145 (conf), 1.147 (caus) vs E1 1.228; c₄ − c_E1 = +0.0011. k_B ≥ 6.5 (n = 4): C ≈ 0 vs 2.14 | r2_spot3_out.txt |
| 3 | \|q\| = 2 ⇔ 2B₀ (E2 M3 f = 2, 120 events per mass) | meas/pred 0.9989 ± 0.0007 (500), 0.9994 ± 0.0004 (1000) | r2_kB_confound_out.txt |
| 4 | Scale-free test of the B* attribution | per-period part ≈ half of the 3 keV excess (N1, N2) | r2_spot2_partS_out.txt |
| 5 | k_B vs b_odd confounding (E2 raw data) | partial correlations favour b_odd (N1) | r2_kB_confound_out.txt |

## 5 Number spot checks (notes vs JSON)
| # | Note value | Source | Result |
|---|---|---|---|
| 1 | round-off 0.147/0.236/0.441/0.739 %, p90 1.14/0.75/1.31/4.81 %, c sd 0.0060/0.0038/0.0044, p90 0.0178/0.0119/0.0226 | FU.json FU1b.roundoff_L3 | OK |
| 2 | 10⁻⁴: +0.0017 ± 0.0021 / +0.0035 ± 0.0034 / +0.0122 ± 0.0027; 1 TeV +0.0008/+0.0028/+0.0130; fraction > 0: 0.90/0.97; c₂₀ > c₂ in 85 % | FIX1 A1b_vfine40 | OK |
| 3 | per-event p16-p84 [−0.018, +0.013], [−0.003, +0.019], [+0.002, +0.063] | FIX1 A1b_vfine40 | OK |
| 4 | replica sd 0.0014/0.0015/0.0021; mean shift ≤ 5×10⁻⁴ | FIX1 replicas | OK |
| 5 | k_B^tot bins +0.0011/+0.0069/+0.014/+0.047/+0.096; r = 0.74 / 0.19 | FIX1 A1a by_kB | OK (labelled k_B in E1, C3) |
| 6 | k_B⊥ bins +0.004/+0.011/+0.019/+0.031/+0.116; 1 TeV …/+0.135 | FIX1 A1a by_kB_perp | OK |
| 7 | Li/causal 0.75 ± 0.08 (p16-p84 0.55-1.15) | FIX1 B6i (0.749 ± 0.081) | OK (C10) |
| 8 | FU3 converged rel_pair −1.15 ± 0.36 % | FU.json FU3.fine_first20.all.rel_pair | OK |
| 9 | K_vac(1.01) = 0.0709 | FU.json FU2_blmax_le_1e-4 | OK |
| 10 | 1 keV FU1a +0.0001/+0.0010/+0.0015 | FU.json FU1a m500_L1_prod | OK |
| 11 | C = 0.437/1.228/1.623 (and the 0.6/10 keV entries) | recomputed from c07 c medians | OK |
| 12 | f(k_B > 6) 0.053/0.293/0.427; \|q\| = 2 57.8/31.1; scalar 36/31, γ* 1.394/1.225 | c13_population_out.txt | OK |
| 13 | Knapen Eq.8 6.1×10⁻⁵, η 8.9×10⁻⁵ | own evaluation | OK (Eq.9: C4) |
| 14 | in-plane R(1/4) 1.145/1.150, R(1/20) 1.306/1.325 | figures/S_Bnonlin_out.txt (1e-3 rows) | OK as quoted (selection: N4) |

## 6 Verdict
**ITERATE.** A = 0, B = 4 (N1-N4), C = 10. Round 1 is resolved apart from A1's replacement claim.
- N1 is fixed by restating the 3 keV excess as "origin open, about half per-period physics".
- N2 is fixed by restating its impact at B₀ (or restricting the verified Λ range).
- N3 is fixed by re-wording the Λ-independence of C.
- N4 is fixed by rescoping the in/out-of-plane statement.

None of these needs a new derivation. A run with B* switched off in the scale-free pair would settle N1 and N2 together and is
recommended before P1 drafting.
