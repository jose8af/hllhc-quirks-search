# Stage 4 results: quirk ribbons through an ACTS Phase-2-like tracker at PU 200 (C001 theory track)

Executor, 2026-10-16. Inputs: the frozen, non-DEV Stage-4 analysis (code freeze `bce02b6f…`, T_seed = 4).
- **Primary: `data/acts_stage4/analysis/C12_v1/`** (C1a + C1b + C2B; 875 + 760 + 480 jobs, 0 production errors).
- Comparison: `C1_v1/` (C1a + C1b), §9.
- Machine-readable headline numbers: `data/acts_stage4/analysis/STAGE4_SUMMARY.json`.

Governing documents: `plan.md` (§2.5, §2.6, §4, §8, §11), `WP_RULE.md` + `WP_RULE_PC19.md`, `g3/G3_REPORT.md`,
`analysis/inputs/ambiguities.json` (A01-A48, D1-D10) and `LOG.md`. Nothing frozen was edited. The tables here were
extracted read-only from the output JSON. The extraction scripts are in the session scratchpad and are not part of the
analysis.

**Tags.**
- **[V]** VERIFIED: read from the frozen pipeline outputs, or a direct ratio of such numbers.
- **[E]** ESTIMATE: model-dependent, derived here, or projected.
- **[U]** UNVERIFIED: transcribed, not checked against the primary source.

**Level.**
- "Detector level" means ACTS-hybrid: Fatras + the hybrid F0/F1 finder, PU 200 normalised to the TDR occupancy,
  **barrel only** (|η(n₃)| < 1.0).
- A1 = detector level with no PU. A2 = PU 200, row-major numpy digitisation. A5 = PU 200, full ACTS chain.
- "Truth level" means Stage-3 generator/kernel quantities (U-2 panel, acceptance A, the truth edges).
- B is in events per 3 ab⁻¹. B₈₄ is the 84th percentile of the log-normal sum.

**Novelty.** `plan.md` has no novelty audit, so this report makes no "first" or "new" claim.

---

## 1. Executive summary

**What was measured.** The Stage-3 truth hits of colour-neutral EW quirks were injected into TDR-normalised PU-200
events on the same ACTS surfaces. The samples are E (fermion) at 200/500/1000/1500 GeV and Ẽ (scalar) at 500 GeV, each
at Λ = 0.45-5 keV. They were reconstructed with a dedicated plane-through-the-vertex finder. The background in two
timing categories, SR-T (late BTL hit) and SR-G, was then estimated along a pre-registered 23-rung ladder. The
background sum is PU combinatorics, extrapolated from 4.8 × 10⁴ ρ = 1 and 6 × 10³ ρ = 2 trials, plus 12 SM processes
plus 8 C′ topologies.

**Main outcome [V].** There is **no working point in either category.** B₈₄ exceeds the 0.11 per-category budget at
every rung.
- The smallest B₈₄ is **1.6 × 10⁶ events in both SR-T and SR-G** (rung R09), i.e. **7.2 decades** above the budget.
- By the frozen rule (§5.3), every (m, Λ, spin) is therefore reported with the pre-defined fallback (plan §2.6,
  D4-17 (i)), with non-zero, log-normally uncertain B.

**What the fallback gives [V/E].**
- At every point it gives ε, B and the observables, plus an expected 95 % CL limit at the pre-declared admissible
  selection r_fb.
- The best expected limit is **μ₉₅ = 53 × the predicted signal yield**, at E200, Λ = 1.5 keV (toys).
- Everywhere else the limit is 55 to 6 × 10⁸ times the prediction, and 7 of the 40 points have ε = 0 in both bins.
- **No (m, Λ, spin) is excluded or discoverable.**

Physically:
1. **The background is not driven to zero.** The width rungs do act strongly on PU: B_PU falls from 1.1 × 10¹⁰ at the
   end of counting to 4 × 10³ at w_core < 4.7 mm, i.e. 6.4 decades [V]. Beyond R07, however, B is set by upper bounds
   from finite C′ (500 events per topology) and SM (2 000 events per sample) samples, about 4 × 10⁵ events [V]. These
   bounds are not measured fakes.
2. **The signal yield is small.**
   - The finder is barrel-only: 69 % of the counting set has |η_pair| > 1.
   - ε(r_fb) is 0-0.145, and ≤ 0.085 except E500 at 3-5 keV [V].
   - Heavy pairs have small cross sections: N_exp = 25 events at E1500 and 380 at E1000 in 3 ab⁻¹ after trigger and
     preselection [E].
   - **Even with B = 0, these points would remain out of reach** [E]:
     - E1500 at any Λ (S ≤ 1.9 events);
     - the seven ε = 0 points (E500/E1000/E1500 at 0.45 keV, E1500 at 0.6 keV, Ẽ500 at ≤ 0.85 keV).
   - With zero background, S ≥ 3 at [E]:
     - E200 at every Λ;
     - E500 at Λ ≥ 0.6 keV;
     - E1000 at Λ ≥ 0.6 keV;
     - Ẽ500 at Λ ≥ 1 keV.

This matches the plan's feasibility statement for Λ ≲ 1 keV and E200. For heavy E at Λ ≳ 2 keV it is worse than the
plan expected, because the binding backgrounds there are the statistics-limited SM and C′ bounds.

---

## 2. Background

### 2.1 Normalisation, samples, reach

| item | value |
|---|---|
| N_trig (after trigger + event-level preselection, user decision D1) | **4.08 × 10⁷** ± 2.0 % stat [V as pipeline number; E as physics]. Z(νν) 2.51, W(τ_h) 0.54, W(eν) 0.25, tt̄1ℓ 0.24, W(τ_ℓ) 0.23, W(μν) 0.22, tW 0.026 (allowance), tt̄2ℓ 0.021, WZ 0.014, WW 0.013, ZZ 0.010, single-top t 0.011 (× 10⁷). K = 1.4; K_tt = 1.9 |
| B1 (ρ = 1) / B2 (ρ = 2) | 12 000 events = 48 000 trials / 3 000 events = 6 000 trials [V] (C1: 20 000 / 2 000) |
| PU reach per trial, ρ = 2 thinning (k = 20, plan §4.1 formula 2⁻²⁰/N_trials) | **1.7 × 10⁻¹⁰** (C1 5 × 10⁻¹⁰) [E]. Requirement if PU took the whole SR-G budget: 0.011/N_trig = 2.7 × 10⁻¹⁰ |
| Deepest rung reachable at ρ = 2 (≥ 10 counts) / with ≥ 10 B1 counts | R06 (w_core < 18.75 mm) / R07 (< 9.4 mm) [V]. Every deeper rung rests on rung factorisation (T3 non-informative, §7) |
| SR-T window (PC-19, from C1 B1 + mixing) | [5.955, 24.035] ns [V]; time-independence test PASS (c_time = 1) [V] |
| ρ_dens (e_adm re-run trigger at 1.05) | 0.966, not triggered [V] |

### 2.2 PU closure end state and σ_ln

| test | rung | N_obs/N_pred | z | lever arm | branch applied (pre-registered) |
|---|---|---|---|---|---|
| T1 (counting) | R04 | **1.500** | +52.8 | 0.039 ✓ | anti-conservative: central × 1.500 [V] |
| T1w (width, χ²_core, 2S) | R05 (R06 lever 0.48 ✗) | **1.606** | +59.4 | 0.029 | anti-conservative (missing lever arm). Compounded with T1: **× 2.41 at every rung ≥ R05** [V] |
| T1e (dE/dx) | — | — | — | — | untestable (0 B1 counts at F0e > 1.3) → T3 |
| T3 (factorisation) | R07 from R05 | — | — | — | **degenerate, not informative** [V] |
| trend | R04-R07 | slope −0.361 per rung | significant | — | conservative: σ_ln only, growing linearly with the rung index [V] |
| factorisation c | — | c_max = 1.196 | — | — | multiplies every factorised chain [V] |

PU background (SR-G column) and the σ_ln budget [V]:

| rung | B_PU central | σ_ln(PU) [trend, density, model spread, closure, stat] | B₈₄ SR-T | B₈₄ SR-G | dominant term (SR-G) | decades over 0.11 (T / G) |
|---|---|---|---|---|---|---|
| R04 N_IP2 ≥ 7 (R_A) | 1.1 × 10¹⁰ | 1.94 [0.54, 1.80, 0.41, 0, 0.01] | 2.6 × 10⁹ | 7.5 × 10¹⁰ | PU | 10.4 / 11.8 |
| R05 w < 37.5 | 4.9 × 10⁹ | 2.03 [0.18, 1.89, 0.47, 0.47, 0.01] | 6.0 × 10⁸ | 3.7 × 10¹⁰ | PU | 9.7 / 11.5 |
| R06 w < 18.75 (R_B) | 3.8 × 10⁷ | 1.36 [0.18, 1.15, 0.46, 0.47, 0.01] | 4.0 × 10⁶ | 1.5 × 10⁸ | PU | 7.6 / 9.1 |
| R07 w < 9.4 | 1.4 × 10⁵ | 1.53 [0.54, 1.15, 0.63, 0.47, 0.18] | 1.6 × 10⁶ | 2.2 × 10⁶ | C′ DIF | 7.2 / 7.3 |
| R08 w < 4.7 (R_C) | 4.4 × 10³ (bound) | 1.92 [0.90, 1.15, 0.46, 0.47, 1.02] | 1.6 × 10⁶ | 1.6 × 10⁶ | C′ DIF (bound) | 7.2 / 7.2 |
| R09 p > 10⁻³ | 2.5 × 10² (bound) | 2.22 [1.26, 1.15, 0.46, 0.47, 1.24] | **1.6 × 10⁶** | **1.6 × 10⁶** | C′ DIF (bound) | **7.2 / 7.2** |
| R11 p > 0.05 | 2.8 × 10³ (bound) | 5.46 [1.98, 1.15, **4.76**, 0.47, 1.28] | 3.1 × 10⁶ | 3.1 × 10⁶ | C′ DIF (bound) | 7.4 / 7.4 |
| R14 N_2S2 ≥ 3 (R_D) | 2.6 × 10³ (bound) | 5.95 [3.07, 1.15, 4.76, 0.47, 1.32] | 4.2 × 10⁶ | 3.7 × 10⁶ | C′ DIF (bound) | 7.6 / 7.5 |
| R20 o > 5 | 2.6 × 10³ (bound) | 7.31 [5.23, …] | 1.2 × 10⁷ | 6.8 × 10⁶ | C′ DIF (bound) | 8.0 / 7.8 |
| R23 e > 2.0 (R_E) | 8.0 × 10² (bound) | 8.12 [6.31, …] | 8.8 × 10⁶ | 6.1 × 10⁶ | C′ PV pair (bound) | 7.9 / 7.7 |

Reading:
- σ_ln is dominated by the **density normalisation (1.15-1.89)** at loose rungs.
- Beyond R11 it is dominated by the **trend term (2-6.3, linear in the rung index)** and by the **model spread (4.76)**.
- The PC-19 timing terms are small: σ_ln,PV 0.38-0.65 and σ_ln,σt ≤ 0.08 [V].
- F1 h and o pass 100 % of the PU records at every measuring population (e.g. 65/65 at FB0) [V], so no h/o factor is
  credited and T3s is not required (D8).
- Because σ_ln grows along F1 and dE/dx, **B₈₄ rises again beyond R09** even where the median falls.

### 2.3 SM and C′, and which background dominates

Central values in SR-G (events) [V]. A12: SM and C′ enter both categories in full, with no time-tag credit, so the SR-T
B at deep rungs is SM + C′ by construction.

| rung | PU | SM (12 processes; 6 are flagged proxies) | C′ (8 topologies) |
|---|---|---|---|
| R04 | 1.1 × 10¹⁰ | 1.9 × 10⁹ (Z(νν) 1.2 × 10⁹) | 3.4 × 10⁷ |
| R06 | 3.8 × 10⁷ | 1.4 × 10⁶ | 9.1 × 10⁵ |
| R07 | 1.4 × 10⁵ | 7.0 × 10⁴ | 4.1 × 10⁵ |
| R08-R14 | 2.5 × 10²-4.4 × 10³ | 3.9-4.7 × 10⁴ (bound-dominated) | 3.5-4.0 × 10⁵ (**zero-count bounds**: DIF, PV pair, γ, looper) |
| R23 | 8.0 × 10² | 5.8 × 10³ | 1.9 × 10⁵ |

- **Up to R06, B is PU-dominated** in SR-G and SM-dominated in SR-T (Z(νν) HS candidates).
- **From R07 on, the C′ terms dominate**, and from R08 on they are zero-count bounds.
  - Example, C′ DIF: N_trig × rate_t (1.59) × f_pre (0.95) × P(R05 attributed; 81/500) × 1.14/81 (the 0/81 bound on
    w < 4.7) × c → 1.7 × 10⁵ central [V].
  - PV pairs: the 0/24 bound gives 1.2-1.4 × 10⁵ [V].
- C′ rate_t per triggered event (max over processes) [E]: PV pairs 30.3, DIF 1.59, γ 0.38, loopers 0.30, NI 0.124 × the
  0.22 PV-line factor, V0 0.052.
- V4-10 leak = 0 on every NI/DIF topology [V].
- The proxy SM processes (W(eν), W(μν), tt̄2ℓ, single top, VV, tW) carry 15-44 % of B_SM depending on the rung [V].

### 2.4 B₈₄ against the budget

| | SR-T | SR-G | combined (SR-T + SR-G) vs 0.3 |
|---|---|---|---|
| minimum B₈₄ on the ladder (rung) | 1.6 × 10⁶ (R09) | 1.6 × 10⁶ (R09) | — |
| decades above 0.11 | **7.2** | **7.2** | — |
| best fallback selection (FB3 = R14 ∧ w < 9.4) | 2.9 × 10⁶ | 2.9 × 10⁶ | ≈ 5.8 × 10⁶, i.e. **7.3 decades above 0.3** [E: sum of B₈₄s] |
| rung where B₈₄ first fails | R01: every rung fails | R01: every rung fails | — |

---

## 3. Signal (detector level)

### 3.1 Efficiency at the reporting rungs

ε = matched candidate passing the rung ∧ f_CKF < 0.2. The denominator is the template-half counting rows (|η_pair| <
2.5, status ≠ 1 counted as failures). n = 180-200 per A2 point. R_A is a lower bound (D9). A1 is all-η and status 1,
a different denominator. A5 is the full chain at 1 keV [V].

| point | A2 R_A | R_B | R_C | R_D | R_E | A1 R_A / R_D | A5 R_A / R_B / R_C |
|---|---|---|---|---|---|---|---|
| E200 0.6 / 1 / 2 / 5 keV | 0.035 / 0.101 / 0.225 / 0.215 | 0.025 / 0.074 / 0.210 / 0.215 | 0 / 0.016 / 0.055 / 0.130 | 0 / 0.005 / 0.025 / 0.070 | 0 / 0.005 / 0.005 / 0.015 | 1 keV: 0.164 / 0.016 | 0.101 / 0.074 / 0.021 |
| E500 0.6 / 1 / 2 / 5 | 0.055 / 0.145 / 0.260 / 0.300 | 0.025 / 0.100 / 0.235 / 0.295 | 0.005 / 0.005 / 0.060 / 0.205 | 0 / 0 / 0.030 / 0.120 | 0 / 0 / 0.025 / 0.095 | 0.177 / 0.028 | 0.140 / 0.090 / 0.005 |
| E1000 0.6 / 1 / 2 / 5 | 0.050 / 0.094 / 0.137 / 0.215 | 0.017 / 0.044 / 0.126 / 0.210 | 0 / 0.006 / 0.016 / 0.133 | 0 / 0 / 0.016 / 0.072 | 0 / 0 / 0.016 / 0.062 | 0.120 / 0.008 | 0.067 / 0.033 / 0.006 |
| E1500 0.6 / 1 / 2 / 5 | 0.035 / 0.085 / 0.205 / 0.275 | 0.005 / 0.059 / 0.175 / 0.265 | 0 / 0.005 / 0.035 / 0.155 | 0 / 0.005 / 0.015 / 0.075 | 0 / 0.005 / 0.015 / 0.075 | 0.132 / 0.002 | 0.090 / 0.053 / 0.005 |
| Ẽ500 0.6 / 1 / 2 / 5 | 0.015 / 0.085 / 0.230 / 0.265 | 0 / 0.027 / 0.175 / 0.260 | 0 / 0 / 0.030 / 0.160 | 0 / 0 / 0.020 / 0.085 | 0 / 0 / 0.015 / 0.055 | 0.127 / 0.002 | 0.090 / 0.011 / 0.000 |

- The ceiling of ≈ 0.3 is the barrel-only fiducial (WP_RULE §8 PC-7) [V/E].
- A5 (full chain) agrees with A2 within the binomial error at all five points; the largest difference is E1000,
  0.067 vs 0.094 (≈ 1.5σ, paired rows) [V].
- V4-6 CKF stealing in A5 is 0.21-0.57 % per point [V].
- The full 40-point tables are `signal_eff.json` → `a2.points.*.report_rungs` and `.fallback`.

### 3.2 Acceptance and the factor breakdown (truth level, template half)

A = ε_fid(|η_pair| < 2.5) × ε_trig × ε_presel|trig [V, truth]. ε_PV-ID = 1 (not modelled, U). Then
ε_total = A × ε_finder, which assumes the finder ε is independent of the preselection (A43).

| species-mass | ε_fid | ε_trig | ε_presel\|trig | A (flat in Λ to ±1 %) | σ_norm [fb, Stage-3 header, N_IC = 1] | N_exp = σ_norm·3 ab⁻¹·A |
|---|---|---|---|---|---|---|
| E200 | 0.847 | 0.90 | 0.65-0.66 | 0.49-0.50 | 219.2 | 3.3 × 10⁵ |
| E500 | 0.830 | 0.92 | 0.74-0.75 | 0.57 | 6.11 | 1.05 × 10⁴ |
| E1000 | 0.816 | 0.94 | 0.84-0.85 | 0.64-0.65 | 0.197 | 380 |
| E1500 | 0.752 | 0.95 | 0.82 | 0.58 | 0.0144 | 25 |
| Ẽ500 | 0.826 | 0.93 | 0.72 | 0.55 | 0.458 | 755 |

The σ_norm values are read from the Stage-3 npz headers [V as read]. Whether the physical σ includes N_IC = 2 (plan §3)
is [U]; a factor of 2 would not change any conclusion here.

### 3.3 SR-T signal efficiency

ε_SR-T(r_fb) (PC-19 window, OOT from the assigned C1 B1 events, 0 missing lookups) [V]:
- E200: 0-0.015;
- E500: 0.005-0.10;
- E1000: 0-0.026;
- E1500: 0-0.035;
- Ẽ500: 0-0.06.

That is ≈ 25-100 % (typically 40-70 %) of ε(r_fb) for m ≥ 500 GeV, and ≈ 0-20 % at E200. Full values are in §4. SR-G = ε(r_fb) − ε_SR-T
(limits flag).

---

## 4. The fallback deliverable (plan §2.6, WP_RULE §8, D4-17 (i))

**Rule.** k_adm comes from the smoothed Stage-3 truth Λ_R(m): k_adm = max k with Λ ≥ Λ_R·2^{(k+1)/2}. e_adm comes from
the dilution-aware table A.2b. Then r_fb = R14 (N_IP2 ≥ 7 ∧ p(χ²_core) > 0.05 ∧ N_2S2 ≥ 3) ∧ (w_core < W_k_adm) ∧ h > 5
∧ o > 5 ∧ (dE/dx > e_adm), plus the time tag in SR-T.
- No per-point best-of was done, and none could be: the selection is fixed by the table.
- The pipeline's k_adm agrees with the frozen A.2b table at every point (`k_consistent`) [V].
- Limits: the expected 95 % CL limit on μ = signal events within trigger + preselection acceptance. Two-bin (SR-T,
  SR-G) counting, each B as one log-normal. Hybrid CLs toys (5 000, seed 20261014) are primary (D4). Asymptotic is the
  cross-check.
- σ₉₅ = μ₉₅/(3 ab⁻¹ · A).
- μ₉₅/N_exp is the limit in units of the predicted yield; < 1 would be an exclusion.
- The plan file name `results/fallback_limits.json` corresponds to the pipeline's `limits.json`.

**Admissibility map for the 307-point grid.** This is the frozen table WP_RULE A.2b, unchanged.
- k_adm = 0 for Λ ≤ 0.85 keV at every species-mass. k_adm = 1 starts at 1.0 keV (E200), 1.2 keV (E300-E400) and 1.5 keV
  (E500-E1500).
- k_adm = 4 is reached at 3 keV (E200, E300), 7 keV (Ẽ1000) and 5 keV otherwise.
- dE/dx is admissible only at k_adm = 4 for E900-E1500 and Ẽ1000: 1.3 MIP for E900-E1200 and Ẽ1000 (Λ ≥ 7 keV for
  Ẽ1000), 1.6 MIP for E1300-E1500.

**B at the 20 fallback selections** [V]:

| selection | used at | B₈₄ SR-T | B₈₄ SR-G | B median SR-G | dominant |
|---|---|---|---|---|---|
| FB0 (no width cut) | Λ ≤ 0.85-1.5 keV | 1.7 × 10⁸ | 2.7 × 10⁸ | 8.8 × 10⁷ | SM Z(νν) |
| FB1 (w < 37.5) | first k_adm = 1 points | 1.4 × 10⁸ | 1.9 × 10⁸ | 6.5 × 10⁷ | SM Z(νν) |
| FB2 (w < 18.75) | E200 1.5, E500 2, Ẽ500 3 keV | **9.3 × 10⁷** (C1: 6.3 × 10⁶; see §10) | 1.0 × 10⁷ | 8.3 × 10⁵ | C′ PV pair |
| FB3 (w < 9.4) | 2-3 keV | 2.9 × 10⁶ | 2.9 × 10⁶ | 6.0 × 10⁵ | C′ PV pair |
| FB4 (w < 4.7) | 3-5 keV | 1.2 × 10⁷ | 6.8 × 10⁶ | 9.8 × 10⁵ | C′ DIF |
| FB4 ∧ e > 1.3 / 1.6 | E1000 5 / E1500 5 keV | 1.4 × 10⁷ / 1.1 × 10⁷ | 7.5 × 10⁶ / 6.3 × 10⁶ | 8.7 / 5.6 × 10⁵ | C′ PV pair |

**Primary results per point** (C1 + C2B). S = N_exp·ε(r_fb) is the expected signal at the fallback selection [E]. μ₉₅
is in events in acceptance [V, toys].

| point (Λ in keV) | r_fb | ε(r_fb) [68 % CP] | ε_SR-T | S | μ₉₅ toys [−1σ, +1σ] | μ₉₅ asym | μ₉₅/N_exp |
|---|---|---|---|---|---|---|---|
| E200 0.45 / 0.6 | FB0 | 0.010 [0.004, 0.023] | 0 | 3.3 × 10³ | 7.6 × 10⁹ [2.3 × 10⁹, 2.5 × 10¹⁰] | 2.1 × 10⁶ ⚠ | 2.3 × 10⁴ |
| E200 0.85 | FB0 | 0.020 | 0 | 6.6 × 10³ | 3.8 × 10⁹ | 1.0 × 10⁶ ⚠ | 1.2 × 10⁴ |
| E200 1 | FB1 | 0.021 | 0 | 7.0 × 10³ | 2.6 × 10⁹ | 8.7 × 10⁵ ⚠ | 8.0 × 10³ |
| **E200 1.5** | FB2 | 0.045 [0.030, 0.065] | 0 | 1.5 × 10⁴ | **1.7 × 10⁷** [1.5 × 10⁶, 2.1 × 10⁸] | 1.7 × 10⁷ | **53** |
| E200 2 | FB3 | 0.050 | 0.005 | 1.6 × 10⁴ | 1.8 × 10⁷ | 1.3 × 10⁷ | 55 |
| E200 3 / 5 | FB4 | 0.051 / 0.070 | 0.005 / 0.015 | 1.7 / 2.3 × 10⁴ | 3.9 / 4.0 × 10⁷ | 2.1 / 1.7 × 10⁷ | 120 / 120 |
| E500 0.45 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E500 0.6 / 0.85 / 1 | FB0 | 0.005 / 0.025 / 0.040 | 0.005 / 0.010 / 0.020 | 52 / 262 / 420 | 1.2 × 10¹⁰ / 5.7 × 10⁹ / 3.6 × 10⁹ | — / — / 7.9 × 10⁵ ⚠ | 1.1 × 10⁶ / 5.4 × 10⁵ / 3.4 × 10⁵ |
| E500 1.5 | FB1 | 0.070 | 0.045 | 730 | 1.4 × 10⁹ | 1.0 × 10⁹ | 1.4 × 10⁵ |
| E500 2 | FB2 | 0.080 | 0.055 | 830 | 8.3 × 10⁷ | 1.8 × 10⁷ | 7.9 × 10³ |
| E500 3 | FB3 | 0.145 [0.120, 0.174] | 0.100 | 1.5 × 10³ | 9.9 × 10⁶ [2.6 × 10⁶, 3.8 × 10⁷] | 5.6 × 10⁶ | 950 |
| E500 5 | FB4 | 0.120 | 0.075 | 1.3 × 10³ | 3.0 × 10⁷ | 1.1 × 10⁷ | 2.9 × 10³ |
| E1000 0.45 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E1000 0.6-1 | FB0 | 0.011-0.022 | 0-0.010 | 4-8 | 5.7-7.2 × 10⁹ | (0.6: 1.9 × 10⁶ ⚠) | 1.5-1.9 × 10⁷ |
| E1000 1.5 / 2 | FB1 | 0.030 / 0.058 | 0.010 / 0.026 | 11 / 22 | 3.4 / 1.9 × 10⁹ | 9.2 × 10⁵ ⚠ / 1.6 × 10⁹ | 9.1 / 5.0 × 10⁶ |
| E1000 3 | FB3 | 0.042 | 0.021 | 16 | 3.8 × 10⁷ | 2.5 × 10⁷ | 1.0 × 10⁵ |
| E1000 5 | FB4 ∧ e > 1.3 | 0.067 | 0.021 | 25 | 4.9 × 10⁷ | 1.9 × 10⁷ | 1.3 × 10⁵ |
| E1500 0.45 / 0.6 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E1500 0.85 / 1 | FB0 | 0.005 / 0.011 | 0 | 0.13 / 0.27 | 1.5 × 10¹⁰ / 7.2 × 10⁹ | 4.2 / 2.0 × 10⁶ ⚠ | 6.1 / 2.9 × 10⁸ |
| E1500 1.5 / 2 | FB1 | 0.030 / 0.035 | 0.015 | 0.75 / 0.88 | 3.6 / 3.1 × 10⁹ | 9.5 / 8.2 × 10⁵ ⚠ | 1.4 / 1.2 × 10⁸ |
| E1500 3 / 5 | FB3 / FB4 ∧ e > 1.6 | 0.075 / 0.075 | 0.035 | 1.9 / 1.9 | 2.1 / 3.7 × 10⁷ | 1.4 × 10⁷ | 8.5 × 10⁵ / 1.5 × 10⁶ |
| Ẽ500 0.45-0.85 | FB0 | 0 | 0 | 0 | no limit | — | — |
| Ẽ500 1 / 1.5 | FB0 | 0.011 / 0.025 | 0.011 / 0.015 | 8 / 19 | 5.6 / 5.4 × 10⁹ | 5.7 / 4.0 × 10⁹ | 7.4 / 7.2 × 10⁶ |
| Ẽ500 2 | FB1 | 0.055 | 0.025 | 41 | 2.0 × 10⁹ | 1.6 × 10⁹ | 2.6 × 10⁶ |
| Ẽ500 3 / 5 | FB2 / FB4 | 0.077 / 0.085 | 0.041 / 0.060 | 58 / 65 | 8.7 / 4.0 × 10⁷ | 2.0 / 1.6 × 10⁷ | 1.1 × 10⁵ / 5.2 × 10⁴ |

⚠ marks points where the asymptotic median is (2-3) × 10⁻⁴ of the toys; see §10.

- The best σ₉₅ is 1.2 × 10⁴ fb, at E200 1.5 keV, against σ_norm = 219 fb [E].
- **What the fallback can claim** (plan §2.6):
  - ε, B and the observables per point, at the pre-declared selection;
  - no exclusion anywhere, because S ≪ B₈₄;
  - no background-free statement, because B₈₄(r_fb) ≫ 0.3 everywhere;
  - no 3-event discovery reach (`mu_3events` = null everywhere);
  - nothing for ℓ_max > R_IT or for the merged regime.
- The 5σ discovery μ, where computed (10 points, Λ ≥ 2-3 keV), is 1.5 × 10⁸-1.0 × 10⁹ events [V], far above every
  N_exp.

---

## 5. P1 and P2

**P1, B-field coplanarity vs the MS floor (truth level only, decision D4-9; U-2 panel `u2_panel/`)** [V, truth].
- The paired r_q = Δs_BM/√(Δs_B² + Δs_MS²) is:
  - 0.989-1.005 at 0.45 keV (quadrature);
  - **0.804-0.972 at 1-3 keV (sub-quadrature)**; the deepest cell is E200 at 3 keV, 0.804 ± 0.042;
  - consistent with quadrature at 5-10 keV.
- B and MS never add linearly.
- Λ_cross = 1.91 / 1.50 / 1.25 / 1.16 keV (E200/500/1000/1500) and 1.59 keV (Ẽ500). The MS floor is 10-28 µm.
- There is no detector-level P1. The event-level resolution (23-30 µm) equals the MS floor (plan §5).

**P2, detector level vs Stage-3 truth** [V; outputs are identical in C1_v1 and C12_v1]:

| observable | no PU (A1) | PU 200 (A2/A5) | truth |
|---|---|---|---|
| lower ε edge (half max, R04) | 0.61-0.88 keV | 1.05-1.29 keV | ℓ_max = R_IT: 0.43-0.94; Δs = 100 µm: 0.47-0.55 keV |
| upper ε edge (R04) | **4.6-7.5 keV** | none inside 0.45-5 keV | hit merging (100 µm): 12.8-25 keV |
| sep_IT^det, median, matched R04 candidates | tracks truth within ≈ 10 % at Λ ≥ 1.5 keV (E500 2 keV: 6.9 vs 7.0 mm; 3 keV: 3.3 vs 3.1 mm); saturates at 25-35 mm below 1 keV | **flat, 41-58 mm, at every Λ** (truth 0.6-142 mm): no Λ information | Λ⁻² handle |
| w_core median (ℓ_max observable) | monotone in Λ: E500 13.1 / 5.5 / 2.4 / 1.3 mm at 1 / 2 / 3 / 5 keV | floor ≈ 9.5-12 mm at ≥ 3 keV; weak slope at 0.45-2 keV | ℓ_max ∝ Λ⁻² |
| M_est = MET·cosh η/(βγ)_ToF, median [q16, q84] | E200 541, E500 1196, E1000 2270, E1500 3320, Ẽ500 1410 GeV; finite for 49-100 % | E200 482 [202, 708], E500 1114 [343, 1439], E1000 2027 [270, 2403], E1500 3113 [155, 3565], Ẽ500 1230 [154, 1662] | monotone in m |
| β_ToF median | 0.53 (E200) to 0.24 (E1500) | 0.66 / 0.39 / 0.39 / 0.70 / 0.49; the q84 reaches 0.9-0.98 (in-time PU BTL hits) | — |
| dE/dx median (MIP) | 1.8 (E200) to 7.1 (E1500) | 1.5 / 2.0 / 2.5 / 2.8 / 1.7 (PU dilution) | — |

- M_est keeps a monotone mass ordering at PU 200 at the median. In-time PU BTL hits give it a low tail (q16 150-340
  GeV) [V].
- The M_est scale is ≈ 2.1-2.4 m, as expected for a pair-mass proxy [E].
- t_est/χ² vs Λ and `results/sensitivity.json` as such are **not produced** by the frozen pipeline. The limits and the
  discovery μ are in `limits.json`.

---

## 6. Validation status

| ID | status | evidence |
|---|---|---|
| V4-1 ingestion closure | **PASS** per job; analysis admission 0 invalid / 0 missing over all 2 115 production jobs [V]. A stand-alone `run_stage4 check` over C1/C2 is not logged | G1, G1b, G3 §0, manifests |
| V4-2 PU density | **DONE** (fix R1; top-up to the TDR); ρ_dens = 0.966 [V] | `f1r_density_bench.json`, background.json |
| V4-3 no-PU finder vs truth edges | **RUN, expectation not met**: ε ≥ 0.9 at 1-5 keV was expected; the measured maximum is 0.21 (all-η A1, barrel only). Detector edges in §5. The W_c/t_tol attribution exists only as a labelled diagnostic (D7) and is not reported here: **OPEN** | signal_eff.json, edges_det.json |
| V4-4 reproducibility | **PARTIAL**: T_seed = 4 production path bit-identical, 85/85 arrays, with a negative control; G1b regressions bit-identical. The "20 jobs rerun" test is not found | LOG 2026-10-14, HASH_ADDENDUM |
| V4-5 brute-force finder cross-check | **NOT RUN** (no record found) | — |
| V4-6 CKF stealing | **PASS**: 0.21-0.57 % per A5 point (max 6.1 % in one 10-row job, E1500) [V] | A5 meta.v46 |
| V4-7 closure | **FAIL → pre-registered anti-conservative end state** (×1.50, ×1.61); T1e untestable; T3 not informative; trend significant (conservative); c = 1.20; SR-T time independence PASS | G3_REPORT, background.json |
| V4-8 cross-machine | N/A (Mac only) | — |
| V4-9 geometry and material | **PASS** (17-hit pattern 99.4 %, on-surface < 0.1 µm, Highland 0.93) | G1_REPORT |
| V4-10 C′ preselection necessity | **PASS**, leak 0 on DIF and NI 22/30/61.5 [V] | background.json → cprime |

---

## 7. Limitations and caveats

1. **The factorisation chain beyond ρ = 2 reach is untested.** Width → χ²_core → 2S → F1 → dE/dx relies on conditionals
   measured on substitute populations, and T3 is degenerate (not informative). No cross-variable closure exists for
   R07-R23 or for any FB column. The B there could be wrong in either direction by an unknown factor.
2. **The trend term dominates σ_ln** at R11-R23 and in every FB column (2-6.3). With the model spread (4.76) it drives
   B₈₄ up along F1 and dE/dx. These are the pre-registered conservative readings (A07, A08), not measurements.
3. **Barrel only** (|η(n₃)| < 1). 69 % of counting-set events are outside the analysis. The endcap and the C2-C (SM
   statistics) and C4′ (rest of the A2 grid, A5 → 20 points) campaigns are future work. ε, B and limits exist only at
   40 of 307 points.
4. **SM proxies.** W(eν), W(μν), tt̄2ℓ, single top, WW/WZ/ZZ and tW have no hit-level sample. Each uses N_trig,p × the
   max P(r | preselected) of the nearest sample (conservative; 15-44 % of B_SM). Z(ττ), Z(ℓℓ) with lost leptons and QCD
   multijets are not in N_trig (A48, U).
5. **Normalisation ESTIMATEs.**
   - 5 % per-object veto inefficiency (A38; each extra 5 % ≈ +4 % N_trig).
   - tW allowance 0.10 × N_trig(tt̄) (A37, U ratio).
   - K_tt = 1.9 is a conservative deviation from the rule's 1.2-1.4 (D3).
   - The PV-line factor 0.22 is an upper value with no σ_ln (A39).
6. **Event replacement.** 11 events were replaced in admitted jobs (A5 1, C2B-B2 2, dens 2, SM 4, C′_PU 2) [V]. The
   orchestrator quotes 0.14 % overall [U].
7. **Excluded jobs.** The G3 jobs G3B1_00021/00059/00077 were excluded (ACTS navigation assertion). G3 is T_seed = 6 and
   is not in the union (T_seed-mixing refusal).
8. **SR-T** gets no time-tag credit on SM and C′ (A12, conservative). SR-T B at deep rungs therefore equals SR-G B by
   construction.
9. A ≈ truth level. ε_PV-ID = 1. The trigger turn-on and the TDR-021 thresholds are [U] (±25 GeV on T₅₀).
10. A1 (no PU) is **not** an upper bound on A2 in these outputs (§10, item 1). The "A1 = optimistic bound" label
    should not be used until that is understood.

---

## 8. What would make a working point reachable

Required: B₈₄,c ≤ 0.11, i.e. a median ≲ 10⁻² at σ_ln ≈ 2.3. Gaps at the best rung (R08-R09) [E, from the [V] terms]:

| class | B₈₄ at R08-R09 (one class alone) | decades to 0.11 | what limits it |
|---|---|---|---|
| C′ (DIF, PV pair, γ, looper) | ≈ 1 × 10⁶ | ≈ 7 | **zero-count bounds** 1.14/M with M = 16-81 attributed events out of 500 C′_PU events per topology |
| SM (Z(νν), W(τ), tt̄ + proxies) | ≈ 1.3 × 10⁵ | ≈ 6 | zero-count bounds on 2 000-event samples (C2-C not run) |
| PU | ≈ 2 × 10³ (R09) to 3 × 10⁴ (R08) | ≈ 4-5 | extrapolation σ_ln (density 1.15, trend, closure × 2.41) |

Possible handles. All are **speculation [E]**, and none could be applied without a new pre-registration (no rule change
after the freeze):
1. **Statistics alone cannot close the C′/SM gap.** A bound scales as 1/M, so ≈ 10⁶-10⁷ × more C′_PU/SM events would be
   needed. That is infeasible under the one-day cap.
2. **Measure the deep C′ conditionals on the no-PU C′₀ samples** (M up to 10⁵) and factorise "topology passes" ×
   "PU-assisted acceptance". This gains at most ≈ 2-3 decades from M, and needs its own closure test.
3. **Time-tag credit for SM/C′ in SR-T.** These particles are prompt and in time. If they shared the PU per-hit late
   fraction (~10⁻⁴ per edge, PC-19), up to ≈ 4 decades in SR-T, but only for SR-T, whose ε is 30-70 % of the total at
   m ≥ 500 GeV.
4. **PU.** A closing extrapolation at R07-R09 (lever arm, a working T3) would remove the trend and closure terms, about
   1.5-2 in σ_ln. That gains ≈ 1 decade in B₈₄; the remaining ≈ 4 decades need ρ = 3 (C5) or a stronger PU variable.
   F1 h and o give no PU rejection [V].
5. **Even all of 2 + 3 + 4 leave ≈ 0-2 decades** in SR-T and ≈ 4-5 decades in SR-G [E]. A WP also needs signal: with B
   = 0, only points with S ≥ 3 benefit: not E1500, and not the seven ε = 0 points (§1). A stronger handle would have
   to be non-geometric (e.g. a tighter dE/dx or timing combination at high m). None was tested here.

---

## 9. C1 → C1 + C2B changes [V]

| quantity | C1 (C1a + C1b) | C1 + C2B |
|---|---|---|
| B1 trials / B2 trials | 20 000 / 2 000 | 48 000 / 6 000 |
| ρ = 2 reach per trial [E] | 5.0 × 10⁻¹⁰ | 1.7 × 10⁻¹⁰ |
| T1 N_obs/N_pred (z) | 1.504 (32.6) | 1.500 (52.8) |
| T1w N_obs/N_pred (z) | 1.610 (36.6) | 1.606 (59.4) |
| trend slope per rung / c factor | −0.373 / 1.202 | −0.361 / 1.196 |
| deepest rung, ρ = 2 / ≥ 10 B1 | R06 / R07 | R06 / R07 (unchanged) |
| min B₈₄ SR-T (rung) | 1.6 × 10⁶ (R07) | 1.6 × 10⁶ (R09) |
| min B₈₄ SR-G (rung) | 1.7 × 10⁶ (R08) | 1.6 × 10⁶ (R09) |
| B_PU central / σ_ln at R06 | 3.9 × 10⁷ / 1.37 | 3.8 × 10⁷ / 1.36 |
| at R08 | 1.1 × 10⁴ / 1.95 | 4.4 × 10³ / 1.92 |
| at R14 | 5.6 × 10³ / **4.15** | 2.6 × 10³ / **5.95** (model spread 1.97 → 4.76) |
| at F0e > 2.0 | 4.7 × 10² / 7.13 | 8.0 × 10² / 8.12 |
| B₈₄ SR-T at FB2 | 6.3 × 10⁶ | **9.3 × 10⁷** (§10) |
| B₈₄ SR-G at FB3 | 4.8 × 10⁶ | 2.9 × 10⁶ |
| best μ₉₅/N_exp (E200 1.5 keV) | 54 | 53 |
| E500 2 keV / Ẽ500 3 keV μ₉₅ (FB2 points) | 3.5 / 4.1 × 10⁷ | 8.3 / 8.7 × 10⁷ |
| WP branch | no WP in either category | no WP in either category |
| signal, acceptance, edges, sep_IT^det, SR-T ε | — | identical (same A1/A2/A5) |

C2B tripled the PU statistics. That moved the closure z but not the ratios, and did not extend the ρ = 2 reach beyond
R06. The outcome is unchanged because the deep rungs are bounded by C′ and SM, which C2B did not touch.

---

## 10. Anomalies and possible bugs (flagged, not explained away)

1. **A1 (no PU) ε is below A2 (PU 200) ε at Λ ≥ 1.5-3 keV** for all five species-masses. Examples: E500 3 keV, 0.171
   vs 0.320; E200 5 keV, 0.084 vs 0.215. The denominators differ (A1 is all-η, which is worth ≤ ×1.2-1.3), but A1
   *falls* above 2 keV while A2 *rises*. Possibly PU hits supply missing second crossings to narrow ribbons; not
   investigated.
2. **A1 upper detector edge 4.6-7.5 keV vs the truth merging edge 12.8-25 keV.** The A1 no_trial count rises with Λ
   (E200: 49/463 at 0.45 keV → 132/463 at 10 keV; E1500: 35 → 191/514). The finder loses narrow ribbons well before
   hit merging.
3. **The asymptotic CLs cross-check fails at 11/33 limit points.** At every FB0/FB1 point listed with ⚠, the median is
   (2.2-3.3) × 10⁻⁴ of the toys, a near-constant factor. Example: E200 0.45 keV, 2.1 × 10⁶ vs 7.6 × 10⁹. The set of
   failing points differs between C1_v1 and C12_v1. A bracketing/root-finding problem is suspected. The primary (toys)
   is unaffected.
4. **SR-T FB2 factor chain (C12).** The χ²_core family enters as p(p > 0.05 | R06 ∧ R09) = 0/16 (bound 0.071) without
   the step p(R09 | R06), which the SR-G chain includes (126/11 858). The result is B_T(FB2) = 9.3 × 10⁷ > B_G(FB2) =
   1.0 × 10⁷, ×15 above C1, and P_T(r ∧ BTL) > P_G(r) (0.0092 vs 0.00085 per trial). That looks like a code-path
   inconsistency between the ladder and FB columns. It is conservative, but it doubles μ₉₅ at E500 2 keV and Ẽ500 3 keV.
5. **More statistics raised σ_ln.** The model spread at R11-R14/F0e went 1.97 → 4.76. The main and factorisation
   routes now credit different χ² conditionals beyond a bounded width factor. With the zero-count rule, the PU column is
   also non-monotone along the ladder: SR-G R09 = 2.5 × 10² < R08 4.4 × 10³ and < R11 2.8 × 10³; SR-T C1 R09/R10 lie
   ×130-400 below R08/R11. This is rule-consistent (B need not be monotone), but the deep-rung B depends on which zero
   factor carries the bound.
6. **sep_IT^det is flat (41-58 mm) at PU 200** at every Λ and mass. The Λ⁻² P2 handle is lost at detector level; only
   A1 tracks truth.
7. Cosmetic issues:
   - the manifest status for B1 records the event-display collect (20 jobs), not the full B1 count;
   - factor labels repeat cuts ("R07_w<9.4 & R07_w<9.4").

---

Reproduction (frozen, non-DEV): `pixi run python -m acts.stage4.analysis.run_all --campaigns C1a,C1b,C2B --out
data/acts_stage4/analysis/C12_v1` (2 473 s on the Mac). Every number above is in `C12_v1/*.json` (and `C1_v1/*.json`
for §9), or in `STAGE4_SUMMARY.json`.
