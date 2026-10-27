# Stage 4 results: quirk ribbons through an ACTS Phase-2-like tracker at PU 200 (C001 theory track)

Executor, 2026-10-16 (final run); revised the same day by the fixer after `review/REVIEW_RESULTS_R1.md` (changes:
`review/FIX_RESULTS_R1.md`), and again after the results PASS for a normalisation error (FIX R3-NORM, below;
`review/FIX_RESULTS_R3_NORM.md`). **This report supersedes the C12_v1 version** (kept as `STAGE4_RESULTS_C12v1.md`).

> **Erratum (FIX R3-NORM, 2026-10-16).** *What was wrong:* the expected signal yield was computed as
> N_exp = σ_norm · 3 ab⁻¹ · A, with σ_norm the **inclusive** σ(pp → QQ̄) but A = `acceptance.json → A_trig_presel`
> a fraction **of the Stage-3 template population, which only contains pairs with pT(QQ̄) > 200 GeV and |η_pair| < 4**.
> The tail fraction f = P(pT(QQ̄) > 200 GeV, |η| < 4) was missing. Correct: **N_exp = σ_norm · f · 3 ab⁻¹ · A**, with
> f = 0.0476 / 0.104 / 0.146 / 0.169 (E200 / E500 / E1000 / E1500, `sim/results/xsec.json →
> trigger_yields_E.rows[m].f_pt200_TRG_over_INC`) and 0.1135 (Ẽ500, from `data/sim/npz/S-TRGS_m500.npz`).
> *How found:* the P2 novelty audit and paper review R2 (A-2) noticed that N_exp(E200) = 3.3 × 10⁵ exceeded the
> project's own N(pT > 200, |η| < 2.5) = 2.7 × 10⁴ before any trigger or preselection cut; verified in
> `investigation/INV_NORM_F200.md`. *Effect:* N_exp, S and the inclusive σ₉₅ were too optimistic, and every
> μ₉₅/N_exp, σ₉₅/σ_th and μ_5σ/N_exp too small, by 1/f = **5.9–21** (21 at m = 200 GeV). The best ratio goes from
> 37.6 to **790** (still E200, Λ = 1.5 keV). μ₉₅, B, ε, `limits.json` and `acceptance.json` are unchanged (no Stage-4
> re-run). *Conclusions unchanged:* no working point; no point excluded or discoverable — the distance to an
> exclusion is 6–21× larger. *Why the self-check missed it:* `selfcheck_stage4.py` re-read N_exp from the summary JSON
> that the same formula had produced, and only checked that σ_norm(E200) = 219.2 fb (the inclusive value); Stage 5
> cross-checked its own N_exp against that JSON at 10⁻⁶. Neither recomputed N_exp from the primary inputs or compared
> it with N(pT > 200). Both checks are now in `selfcheck_stage4.py` (§11.4).

**Inputs.** The frozen, non-DEV Stage-4 analysis `data/acts_stage4/analysis/C12FC_v1/` (code freeze `b42aef4d…`,
T_seed = 4, campaigns C1a + C1b + C2B + A2FC, exit 0, schema check ok; log `C12FC_v1.log`). Machine-readable numbers:
`data/acts_stage4/analysis/STAGE4_SUMMARY.json` (schema v2), built by `acts/stage4/results/make_stage4_summary.py`
(`python3 -I`, stdlib only). The same script writes the helper tables `acts/stage4/results/tables_C12FC_v1.md` and the
full extraction `headline_C12FC_v1.json`. The headline numbers below were re-checked against the JSON by
`acts/stage4/results/selfcheck_stage4.py` (§11.4).

**Tags.**
- **[V]** VERIFIED: read from the C12FC_v1 outputs, or a direct ratio or sum of such numbers.
- **[V-inv]** VERIFIED by an investigation (read here from its JSON output under `data/acts_stage4/investigation/`).
- **[E]** ESTIMATE: model-dependent, derived here, or projected.
- **[U]** UNVERIFIED: transcribed, not re-checked in this pass.

**Level.** Unless marked *truth level*, every result here is **detector-level simulation in a public-geometry
ACTS model** of a CMS-Phase-2-like tracker: Fatras simulation + the dedicated plane-through-the-vertex finder, PU 200
normalised to the TDR occupancy, **barrel only** (|η(n₃)| < 1). No CMS software, CMS data or CMS-internal geometry was
used. Samples: A1 = no PU (full ACTS chain); A2 = PU 200 with row-major numpy digitisation of the quirk hits, except at
the 9 V4-6 revert points, where A2 is the full ACTS chain (A2FC, §4.3); A5 = PU 200 full chain at Λ = 1 keV. *Truth
level* = Stage-3 generator/kernel quantities. B is in events per 3 ab⁻¹; B₈₄ is the 84th percentile of the
log-normal B sum; the WP budget is B₈₄ ≤ 0.11 per category (≤ 0.3 combined).

**Novelty.** `plan.md` has no novelty audit, so this report makes no "first" or "new" claim.

---

## 0. Summary in plain language

**What was done.** Quirks are pairs of heavy charged particles tied by a long, weak string. The pair moves as a thin
"ribbon": two tracks that wind around each other in a plane through the collision point, instead of two helices. We
took the Stage-3 simulated quirk hits and overlaid them on 200 simultaneous ordinary proton-proton collisions (pile-up,
PU 200), using a public model of a CMS-Phase-2-like silicon tracker. A dedicated finder then looked for ribbons, and a
pre-registered ladder of 23 cuts (a "ladder" of rungs) tried to bring the fake-ribbon background down to essentially
zero (< 0.11 events in 3 ab⁻¹ at the 84 % upper end, per category). There are two categories: SR-T, with a late timing
hit, and SR-G, the rest.

**Main result [V; the limit ratios are E].** **No working point exists in either category.**
- The lowest background reached is B₈₄ ≈ **1.2 × 10⁶ events** (SR-T and SR-G, at rung R09), **7.05 decades** above
  the 0.11 budget.
- So, by the frozen rule, the pre-defined fallback applies. Every one of the 40 simulated (mass, Λ, spin) points gets
  an efficiency and a background estimate at a fixed, pre-declared selection; the 33 points with ε > 0 also get an
  expected limit (7 have ε = 0 in both bins).
- **No point is excluded or discoverable.** The best expected limit is **790 × the predicted signal yield** (the
  signal would have to be 790 times larger than predicted to be excluded), at the fermion E with m = 200 GeV and
  Λ = 1.5 keV. Every other point is worse, up to 6 × 10⁷ ×. Best per species-mass: E200 790 (1.5 keV), E500
  1.3 × 10⁴ (3 keV), E1000 3.8 × 10⁵ (3 keV), E1500 3.8 × 10⁶ (3 keV), Ẽ500 2.8 × 10⁵ (3 keV) [E].
- These expected limits use zero-count simulation bounds as background central values: they measure the reach of
  this simulation set-up and are conservative, not the physics reach of a real search (they would move ∝ the bounds
  with more simulated events).
- The 790 rests on ε(FB2) = 9/200 = 0.045 (68 % CP [0.030, 0.065], 95 % [0.021, 0.084]). Deep-rung and fallback
  efficiencies have a large statistical uncertainty: few events pass, and the pass/fail of each event fluctuates with
  the measurement-noise draw (§4.3). The ratio is therefore uncertain by a factor ≈ 1.5 either way at 68 % CL. Even
  the 95 % CP upper ε (0.084) gives ≈ 420; an exclusion would need ε ≈ 36, which is impossible.
- **Full-chain systematic on ε [E].** At the 8 other full-chain revert points the full chain loses efficiency
  systematically against numpy A2 (paired R04: 84 vs 20 discordant events, p ≈ 1.6 × 10⁻¹⁰; at r_fb × 0.87 overall),
  from CKF hit stealing. E200 1.5 keV is one of the 31 points that stay on numpy A2, so its ε may be overestimated by up
  to about this factor: the best ratio becomes **≈ 910** (790/0.87; ≈ 950 with the R04 factor 0.83). The null result,
  no exclusion, is unaffected.

**Why.**
1. *The deep background is not measured, it is bounded.* PU fakes do fall along the width cuts: by 4.9 decades from
   R04 to R07 (1.1 × 10¹⁰ → 1.4 × 10⁵, the last rung with ≥ 10 B1 counts), and to a bound of 4.4 × 10³ at R08.
   Beyond rung R07, however, the background is set by "we saw 0 out of N" upper bounds from small simulated samples of
   specific SM processes (500 events per C′ topology, 2 000 per SM sample). Individually these bounds are 1.4–1.7 × 10⁵ events (C′ DIF, C′ PV pair); together with the SM bounds they make
   ≈ 3–4 × 10⁵ events (median).
   Shrinking them below 0.11 would need 10⁸–3 × 10⁹ simulated events per sample (§2): far beyond the budget.
2. *Even the pile-up part alone stays ~ 2.3 × 10³ events* (B₈₄ at R09), 4.3 decades over budget. It is extrapolated
   from a finite PU sample with a conservative closure correction (× 2.41) and a large trend uncertainty (§3). Its
   median is itself a zero-count bound: bringing it to 0.11 would need ≈ 10⁹ ρ = 1 trials (now 4.8 × 10⁴), and the
   trend + density uncertainty alone would still need a median ≲ 0.02 (§2).
3. *The signal efficiency is small at the selections the rule fixes:* 0–8 % (barrel only, and the deep cuts cost a
   lot). The heavy pairs also have small cross sections: E1500 gives at most 0.3 signal events and E1000 at most
   3.4, even with zero background.

**What was measured at detector level.** Inside the barrel and without PU, some finder candidate holds ≥ 50 % of the quirk hits in 90–97 %
of the pairs at Λ = 1.5–2 keV (64–77 % if the counting rung R04 is also required). V4-3 is therefore **PARTIAL**: its
ε ≥ 0.9 is reached at 1.5–2 keV only, with a match definition set after the C12_v1 failure, and not at 1, 3, 5 keV
(§4.1). The detector-level Λ window of the finder is measured: a lower edge 0.6–0.85 keV (no PU) / 1.0–1.2 keV (PU 200),
and an upper edge 4.7–6.6 keV without PU. That upper edge misses the pre-declared 13–25 keV truth comparator; it agrees
with a merged-on-*any*-of-10-surfaces comparator derived afterwards (§6.1).

**P1 and P2 in one line each.**
- **P1 (B-field coplanarity vs the MS floor): not addressed at detector level** (D4-9: the out-of-plane resolution,
  23–30 µm, equals the MS floor). Only the truth-level U-2 panel exists (§7).
- **P2 (m_Q, Λ): no measurement of m_Q or Λ at PU 200; only qualitative handles.** M_est = MET·cosh η/(βγ)_ToF
  estimates the **pair mass M_QQ̄ ≥ 2 m_Q**, not m_Q. Its median is 2.26 m_Q at PU 200 (pooled, N = 850 events), just
  above the 2 m_Q threshold (2.46 m_Q without PU). Without PU no event falls below 1.5 m_Q; at PU 200, 29 % fall below
  1.5 m_Q and 19 % below 0.5 m_Q (a low cluster induced by in-time PU timing hits). The medians order the four E masses
  (483 / 1 113 / 2 070 / 3 137 GeV), but the per-event spread is huge (q16 155–332 GeV for every mass) and the
  median/m ratio depends on the species. There is no m_Q fit. Λ is only bracketed by where ε turns on and off;
  sep_IT^det, the Λ⁻² handle, is **not measurable at PU 200** (§6).

**What changed since the C12_v1 report.** Four analysis fixes (R6) and the full-chain revert of 9 signal points
(A2FC) went in. The minimum B₈₄ fell 1.6 → 1.2 × 10⁶, and the best limit ratio improved 1.1 × 10³ → 790 (53 → 37.6 before FIX R3-NORM). The FB0/FB1
B₈₄ fell × 4–8 (SR-G) and × 50 (SR-T), because an SM "Z(νν) dominates" artefact is gone. All "possible bugs" of the old §10 are
resolved (Appendix A). One new surprise: at E500, 3 keV the full chain cut the fallback efficiency 0.145 → 0.055
(§4.3). The investigation (`investigation/INV_A2FC_E500.md`, closed) found no merge bug, identical inputs and an
identical noise model. At E500 3 keV the only identified full-chain-specific loss is one event (CKF stealing); the rest
is attributed to measurement-noise draws. That is statistically unusual (global p ≈ 10⁻⁴–10⁻³), and no mechanism was
found. At the other 8 revert points, however, the paired comparison shows a systematic full-chain loss (above): a
real CKF-driven inefficiency, not noise.

---

## 1. Outcome

### 1.1 WP status [V]

`bsum_wp.json → rule`: `wp = {T: null, G: null}`, branch **"no WP in either category (§5.3): §8 fallback, user
told"**, `complete_inputs = true`. B₈₄ > 0.11 already at R01 in both categories, and at every rung after it.

| | SR-T | SR-G |
|---|---|---|
| minimum B₈₄ on the ladder (rung) | **1.23 × 10⁶ (R09, p(χ²_core) > 10⁻³)** | **1.23 × 10⁶ (R09)** |
| decades above 0.11 at the minimum | **7.05** | **7.05** |
| B₈₄ at R04 (end of counting) | 2.6 × 10⁹ (10.4 decades) | 7.5 × 10¹⁰ (11.8 decades) |
| best fallback column (FB3 = R14's non-width cuts ∧ w < 9.4 mm) | 2.0 × 10⁶ | 2.0 × 10⁶ |
| combined SR-T + SR-G at FB3 vs 0.3 [E: sum of B₈₄] | ≈ 4.0 × 10⁶, i.e. 7.1 decades over | |

**§8 fallback deliverable (plan §2.6, WP_RULE §8, D4-17 (i)), and what it means.**
- For every (m, Λ, spin), a pre-declared admissible selection r_fb is taken from the frozen admissibility table
  (WP_RULE A.2b). Following WP_RULE §8, r_fb = FB_k ∧ h > 5 ∧ o > 5 (∧ dE/dx > e_adm), plus the time tag in SR-T.
  FB_k is **not** nested in the ladder rung R14 (which already contains w < 4.7 mm and p > 10⁻³). It is R14's
  non-width cuts (N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p(χ²_core) > 0.05 ∧ N_2S2 ≥ 3) with a single width cut w_core < W_k_adm. No
  per-point optimisation is possible or done. The pipeline's k_adm equals the frozen table at all 40 points
  (`k_consistent`) [V].
- At r_fb we report ε, B (non-zero, log-normally uncertain), the observables, and an expected 95 % CL limit (§5).
- It does **not** give a background-free statement (B₈₄ ≫ 0.3 everywhere), a 3-event discovery reach
  (`mu_3events` = null everywhere), or any statement in the merged regime (Λ above the upper edge).

### 1.2 Background along the ladder [V]

| rung | B_PU central | σ_ln(PU) [trend, density, model, closure, stat]; total also has normalisation 0.26 | B₈₄ SR-T | B₈₄ SR-G | dominant term (SR-G) | decades over 0.11 (T / G) |
|---|---|---|---|---|---|---|
| R04 N_IP2 ≥ 7 (R_A) | 1.1 × 10¹⁰ | 1.94 [0.54, 1.80, 0.41, 0, 0.01] | 2.6 × 10⁹ | 7.5 × 10¹⁰ | PU | 10.4 / 11.8 |
| R05 w < 37.5 mm | 4.9 × 10⁹ | 2.03 [0.18, 1.89, 0.47, 0.47, 0.01] | 6.0 × 10⁸ | 3.7 × 10¹⁰ | PU | 9.7 / 11.5 |
| R06 w < 18.75 (R_B) | 3.8 × 10⁷ | 1.36 [0.18, 1.15, 0.46, 0.47, 0.01] | 3.8 × 10⁶ | 1.5 × 10⁸ | PU | 7.5 / 9.1 |
| R07 w < 9.4 | 1.4 × 10⁵ | 1.53 [0.54, 1.15, 0.63, 0.47, 0.18] | 1.4 × 10⁶ | 2.0 × 10⁶ | C′ DIF | 7.1 / 7.3 |
| R08 w < 4.7 | 4.4 × 10³ (bound) | 1.92 [0.90, 1.15, 0.46, 0.47, 1.02] | 1.4 × 10⁶ | 1.4 × 10⁶ | C′ DIF (bound) | 7.1 / 7.1 |
| **R09 p > 10⁻³** | 2.5 × 10² (bound) | 2.22 [1.26, 1.15, 0.46, 0.47, 1.24] | **1.2 × 10⁶** | **1.2 × 10⁶** | C′ DIF (bound) | **7.05 / 7.05** |
| R11 p > 0.05 | 2.8 × 10³ (bound) | 5.46 [1.98, 1.15, 4.76, 0.47, 1.28] | 2.5 × 10⁶ | 2.5 × 10⁶ | C′ DIF (bound) | 7.4 / 7.4 |
| R14 N_2S2 ≥ 3 (R_D) | 2.6 × 10³ (bound) | 5.95 [3.07, 1.15, 4.76, 0.47, 1.32] | 3.3 × 10⁶ | 2.7 × 10⁶ | C′ DIF (bound) | 7.5 / 7.4 |
| R20 o > 5 | 2.6 × 10³ (bound) | 7.31 [5.23, 1.15, 4.76, 0.47, 1.33] | 1.1 × 10⁷ | 5.4 × 10⁶ | C′ DIF (bound) | 8.0 / 7.7 |
| R23 e > 2.0 MIP (R_E) | 8.0 × 10² (bound) | 8.12 [6.31, 1.15, 4.76, 0.47, 1.36] | 8.7 × 10⁶ | 6.3 × 10⁶ | C′ DIF (bound) | 7.9 / 7.8 |

"(bound)" means the term is a zero-count upper bound (0 passes in M, entered as 1.14/M), not a measured fake rate.

### 1.3 Background composition at the deep rungs [V]

Central values (events), SR-G. SR-T is identical for SM and C′, which get no time-tag credit (A12, conservative).

| rung | PU | SM (12 processes, 8 are flagged proxies) | C′ (8 topologies) | three largest terms |
|---|---|---|---|---|
| R04 | 1.1 × 10¹⁰ | 1.9 × 10⁹ | 3.4 × 10⁷ | PU; Z(νν) 1.2 × 10⁹; W(τ_h) 2.4 × 10⁸ |
| R06 | 3.8 × 10⁷ | 1.4 × 10⁶ | 8.8 × 10⁵ | PU; Z(νν) 9.6 × 10⁵; C′ γ 4.0 × 10⁵ |
| R07 | 1.4 × 10⁵ | 7.0 × 10⁴ | 3.8 × 10⁵ | C′ DIF 1.5 × 10⁵; C′ PV pair 1.4 × 10⁵; PU 1.4 × 10⁵ |
| R08 | 4.4 × 10³ (bound) | 4.7 × 10⁴ (bounds) | 3.7 × 10⁵ (bounds) | C′ DIF 1.7 × 10⁵; PV pair 1.4 × 10⁵; γ 4.2 × 10⁴ |
| **R09** | 2.5 × 10² (bound) | 4.6 × 10⁴ (bounds) | 3.3 × 10⁵ (bounds) | C′ DIF 1.7 × 10⁵; PV pair 1.4 × 10⁵; Z(νν) 1.6 × 10⁴ |
| R14 | 2.6 × 10³ (bound) | 3.9 × 10⁴ | 3.2 × 10⁵ | C′ DIF 1.5 × 10⁵; PV pair 1.2 × 10⁵; γ 3.9 × 10⁴ |
| R23 | 8.0 × 10² (bound) | 5.8 × 10³ | 3.2 × 10⁵ | C′ DIF 1.5 × 10⁵; PV pair 1.2 × 10⁵; γ 3.9 × 10⁴ |

Reading:
- **Up to R06 the background is PU** (SR-G). The SR-T PU column is × (0.6–3) × 10⁴ smaller, because a late BTL hit is rare,
  so SR-T is SM-dominated there (Z(νν) hard-scatter candidates).
- **From R07 on, the C′ topologies dominate, and from R08 on they are zero-count bounds** (DIF, PV pair, γ). The SM
  terms are also bounds there. The flagged proxy processes carry 45 % of B_SM at R09 [V]
  (`background.json → sm._proxy_fraction_of_B_SM`).
- Example C′ DIF chain at R08/R09 [V]: f_pre 0.949 × P(R05 attributed) 81/500 × the 0/81 width bound (1.14/81) × c
  (1.196), giving 1.7 × 10⁵ events. The bound's reach is ≈ 1.14·c/500 per event, independent of M (INV_STATS_BKG §5).
- The PU column is non-monotone (R09 2.5 × 10² < R08 4.4 × 10³ and < R11 2.8 × 10³). That is rule-consistent: B
  need not be monotone, and the deep-rung PU value depends on which zero factor carries the single allowed bound
  (INV_STATS_BKG §3).

### 1.4 The 20 fallback columns [V]

| selection | used at (r_fb) | B₈₄ SR-T | B₈₄ SR-G | median SR-G | dominant SR-G |
|---|---|---|---|---|---|
| FB0 (no width cut) | E200 ≤ 0.85; E500, E1000, E1500 ≤ 1; Ẽ500 ≤ 1.5 keV | 3.5 × 10⁶ | 6.4 × 10⁷ | 1.4 × 10⁶ | PU |
| FB1 (w < 37.5) | E200 1; E500 1.5; E1000, E1500 1.5–2; Ẽ500 2 keV | 2.2 × 10⁶ | 2.5 × 10⁷ | 8.1 × 10⁵ | C′ DIF |
| FB2 (w < 18.75) | E200 1.5, E500 2, Ẽ500 3 keV | 2.6 × 10⁶ | 8.9 × 10⁶ | 5.9 × 10⁵ | C′ PV pair |
| FB3 (w < 9.4) | E200 2; E500, E1000, E1500 3 keV | 2.0 × 10⁶ | 2.0 × 10⁶ | 4.3 × 10⁵ | C′ PV pair |
| FB4 (w < 4.7) | E200 3, 5; E500 5; Ẽ500 5 keV | 1.1 × 10⁷ | 5.4 × 10⁶ | 7.8 × 10⁵ | C′ DIF |
| FB4 ∧ e > 1.3 / 1.6 | E1000 5 / E1500 5 keV | 1.3 × 10⁷ / 1.1 × 10⁷ | 7.4 × 10⁶ / 6.6 × 10⁶ | 9.6 / 9.0 × 10⁵ | C′ DIF |

"Used at" lists every point whose r_fb is that column (`limits.json → points.*.primary.admissibility.r_fb`).
All 20 columns (incl. the e > x variants): `tables_C12FC_v1.md` → "FB", and `STAGE4_SUMMARY.json → fallback_B`.
SR-T > SR-G at FB4 and FB4e (1.1 × 10⁷ vs 5.4 × 10⁶) comes from the larger SR-T σ_ln, not a larger median. B need not
be monotone between columns (REVIEW_ANALYSIS_R6 C-1).

---

## 2. Why statistics alone cannot give a WP

Re-check of INV_STATS_BKG §5 on C12FC_v1 (`STAGE4_SUMMARY.json → statistics_reach`) [E, from [V] terms]. Each bounded
term is treated as a single log-normal with its central value as the median: B₈₄,alone = B·e^σ. Its bound scales as
1/N_events, so the events per sample needed to bring that term *alone* to 0.11 are N_now × B₈₄,alone / 0.11.

| term at R09 (SR-G) | central | σ_ln | B₈₄ alone | sample now | events needed for this term alone |
|---|---|---|---|---|---|
| C′ PV pair (0/24 width bound) | 1.4 × 10⁵ | 1.47 | 6.1 × 10⁵ | 500 | **2.8 × 10⁹** |
| C′ DIF (0/81) | 1.7 × 10⁵ | 1.05 | 4.8 × 10⁵ | 500 | **2.2 × 10⁹** |
| SM Z(νν) (0/81 HS candidates) | 1.6 × 10⁴ | 1.05 | 4.6 × 10⁴ | 2 000 | **8.4 × 10⁸** |
| C′ γ | 6.5 × 10³ | 1.31 | 2.4 × 10⁴ | 500 | 1.1 × 10⁸ (5.8 × 10⁸ at R08) |
| **PU alone** (bound, extrapolated) | 2.5 × 10² | 2.22 | **2.3 × 10³** | 4.8 × 10⁴ ρ = 1 trials | ≈ 1.0 × 10⁹ trials; and the irreducible trend + density σ_ln ≈ 1.7 alone would need a median ≲ 0.02 |

- **10⁸–3 × 10⁹ events per sample are needed, against 500–2 000 now** [E]. This confirms INV_STATS_BKG (1 × 10⁸–2.7 × 10⁹
  on C12_v1; the R6 fixes did not touch these ladder terms). All bounded C′ + SM terms together would need ≈ × 1.4 × 10⁷
  more statistics, i.e. ≈ 7 × 10⁹ C′_PU events per topology and ≈ 3 × 10¹⁰ SM events per sample [V-inv, INV_STATS_BKG
  §5]. That is ≳ 10–40 × the data-equivalent count of each process: infeasible under the one-day cap.
- **The PU term alone is B₈₄ = 2.3 × 10³ at R09** (3.0 × 10⁴ at R08) [E]. That is 4.3 (5.4) decades over budget, even
  with C′ and SM at zero. Its median is a zero-count bound and its σ_ln is 2.2 (trend 1.26, density 1.15, stat 1.24),
  on top of the × 2.41 closure factor. The bound and the stat part shrink ∝ 1/N with more PU events (≈ 10⁹ ρ = 1 trials
  for this term alone, by the same scaling as the rows above), but the trend + density part (σ_ln ≈ 1.7) and the
  closure factor do not: with them alone the median would have to be ≲ 0.02 (§3).
- **Conclusion: no achievable statistics produce a WP with this ladder.** A WP would need new handles or data-driven
  estimates, and a new pre-registration (§10).

---

## 3. PU extrapolation: closure at T_seed = 4, σ_ln, and the ρ = 2 reach [V]

| test | rung | N_obs/N_pred | z | lever arm | branch applied (pre-registered) |
|---|---|---|---|---|---|
| T1 (counting) | R04 | **1.500** | +52.8 | 0.039 ✓ | anti-conservative: central × 1.500 |
| T1w (width, χ²_core, 2S) | R05 (R06 lever arm fails) | **1.606** | +59.4 | 0.029 | anti-conservative (missing lever arm): × max(r, 1) and \|ln r\| = 0.47 in σ_ln |
| compounded | every column ≥ R05 | **× 2.409** | | | applied once (INV_STATS_BKG §4) |
| T1e (dE/dx) | — | — | — | — | untestable (< 10 B1 counts) → T3 |
| T3 (factorisation) | R07 from R05 | — | — | — | **degenerate, not informative** |
| trend | R04–R07 | slope −0.361 per rung | significant | — | conservative: σ_ln only, linear in the rung index |
| factorisation constant c | — | 1.196 | — | — | multiplies every factorised chain |

- **σ_ln dominance.** At loose rungs the density normalisation dominates (1.15–1.89). From R11 on, the **trend term**
  (1.98 → 6.31, linear in the rung index) and the **model spread** (4.76) dominate. The model spread is ln(P_fact/P_main)
  = ln 117. The central value is the upper envelope, so the spread only adds σ_ln (INV_STATS_BKG §3, class (i)). This
  is why B₈₄ rises again beyond R09 even where the median falls.
- **F1 h/o** pass 100 % of the PU records at every measuring population, so no h/o factor is credited, and T3s is not
  required (D8) [V].
- **ρ = 2 reach.** 48 000 ρ = 1 trials (12 000 events) and 6 000 ρ = 2 trials (3 000 events). The thinning reach per
  trial is ≈ 10⁻⁶/N_trials(ρ = 2) (2⁻²⁰ ≈ 10⁻⁶, plan l. 1110) = **1.7 × 10⁻¹⁰** [E] (C1 alone: 5 × 10⁻¹⁰). If PU took the whole SR-G budget it would
  need ≈ 0.011/N_trig = 2.7 × 10⁻¹⁰ (median ≈ 0.011 for B₈₄ = 0.11 at σ_ln ≈ 2.3) [E]. The deepest rung reachable at
  ρ = 2 (≥ 10 counts) is **R06**, and the deepest with ≥ 10 B1 counts is R07 (SR-T: R06). **Everything deeper rests on
  rung factorisation with no informative cross-variable closure test.**
- SR-T window (PC-19, from C1 B1 + mixing): **[5.955, 24.035] ns** [V]; time-independence PASS. ρ_dens = 0.966 < 1.05
  (no e_adm re-run) [V].

---

## 4. Signal efficiency (detector level)

ε = matched candidate (pre-declared core match: ≥ 3 core quirk hits in ≥ 3 layers and ≥ 50 % of the core) ∧ rung ∧
f_CKF < 0.2. The A2 denominator is the template-half counting rows with |η_pair| < 2.5 (status ≠ 1 counts as a failure),
n = 180–200 per point. ε at R01–R04 is a lower bound (D9). The barrel-only fiducial (|η(n₃)| < 1) is part of every rung,
so the ceiling is ≈ 0.3.

### 4.1 V4-3: PARTIAL [V-inv]

V4-3 (plan l. 1810) expects a **finder** efficiency ≥ 0.9 at 1–5 keV on no-PU events. The C12_v1 report compared 0.9
with the all-η A1 R_A number (max 0.21). That is a different quantity: it folds in the barrel fraction (0.19–0.28), the
R04 hit-count requirement and the core match. The table uses A1, no PU, |η_pair| < 1, status 1, and the match "some
candidate holds ≥ 50 % of the written quirk hits" (`matched_any`; `investigation/a1_ladder_*.json`, INV_SIGNAL_EFF §1).
That definition was introduced in INV_SIGNAL_EFF *after* the C12_v1 failure and is looser than the pre-declared signal
match; it is a post-hoc reading.

| Λ (keV) | E200 | E500 | E1000 | E1500 | Ẽ500 |
|---|---|---|---|---|---|
| 1 | 0.90 | 0.80 | 0.83 | 0.75 | 0.79 |
| **1.5** | **0.92** | **0.94** | **0.93** | **0.92** | — |
| **2** | **0.91** | **0.90** | **0.90** | **0.93** | **0.96** |
| 3 | 0.85 | 0.84 | 0.83 | 0.87 | 0.97 |
| 5 | 0.58 | 0.65 | 0.74 | 0.69 | 0.84 |

With R04 also required (`matched_R04`), the same rows give 0.64–0.77 at 1.5–2 keV (E200 0.65 / 0.64).

**V4-3 status: PARTIAL.** ε_find ≥ 0.9 holds at 1.5–2 keV (0.90–0.97; Ẽ500 also at 3 keV) with the post-hoc
any-candidate match. It is not met at 1 keV (the lower edge) or at 3 and 5 keV, for understood reasons. N_IP2 ≥ 7 needs ≥ 2 hits on *every* one of 10 inner surfaces, so one merged pair
kills it. The seed needs an opening ≥ 1 mrad, and CKF steals quirk hits (INV_SIGNAL_EFF §2–§4). The W_c/t_tol variants
leave R01/R04 unchanged at 2–5 keV (± 0.01). The high-Λ loss is therefore merging, seed degeneracy and CKF, not the
window or plane thickness [V-inv].

### 4.2 A2 (PU 200) at the reporting rungs [V]

R_A = R04; R_B = R04 ∧ w < 18.75 mm; R_C = R04 ∧ w < 4.7 mm; R_D = R14; R_E = R23. **FC** marks the A2FC full-chain
points.

| point | R_A | R_B | R_C | R_D | R_E | A5 (full chain, 1 keV) R_A / R_B / R_C |
|---|---|---|---|---|---|---|
| E200 0.6 / 1 / 2 / 3 FC / 5 FC | 0.035 / 0.101 / 0.225 / 0.185 / 0.150 | 0.025 / 0.074 / 0.210 / 0.179 / 0.145 | 0 / 0.016 / 0.055 / 0.087 / 0.085 | 0 / 0.005 / 0.025 / 0.051 / 0.055 | 0 / 0.005 / 0.005 / 0.026 / 0.015 | 0.101 / 0.074 / 0.021 |
| E500 0.6 / 1 / 2 / 3 FC / 5 FC | 0.055 / 0.145 / 0.260 / 0.305 / 0.235 | 0.025 / 0.100 / 0.235 / 0.290 / 0.230 | 0.005 / 0.005 / 0.060 / 0.095 / 0.135 | 0 / 0 / 0.030 / 0.020 / 0.080 | 0 / 0 / 0.025 / 0.020 / 0.060 | 0.140 / 0.090 / 0.005 |
| E1000 0.6 / 1 / 2 / 3 FC / 5 FC | 0.050 / 0.094 / 0.137 / 0.189 / 0.195 | 0.017 / 0.044 / 0.126 / 0.179 / 0.195 | 0 / 0.006 / 0.016 / 0.042 / 0.113 | 0 / 0 / 0.016 / 0.021 / 0.072 | 0 / 0 / 0.016 / 0.021 / 0.062 | 0.067 / 0.033 / 0.006 |
| E1500 0.6 / 1 / 2 / 3 FC / 5 FC | 0.035 / 0.085 / 0.205 / 0.210 / 0.200 | 0.005 / 0.059 / 0.175 / 0.195 / 0.190 | 0 / 0.005 / 0.035 / 0.075 / 0.130 | 0 / 0.005 / 0.015 / 0.030 / 0.060 | 0 / 0.005 / 0.015 / 0.030 / 0.055 | 0.090 / 0.053 / 0.005 |
| Ẽ500 0.6 / 1 / 2 / 3 / 5 FC | 0.015 / 0.085 / 0.230 / 0.242 / 0.245 | 0 / 0.027 / 0.175 / 0.232 / 0.245 | 0 / 0 / 0.030 / 0.046 / 0.125 | 0 / 0 / 0.020 / 0.031 / 0.080 | 0 / 0 / 0.015 / 0.021 / 0.035 | 0.090 / 0.011 / 0.000 |

- All 40 points (0.45–5 keV): `tables_C12FC_v1.md` → "eps at reporting rungs"; `signal_eff.json → a2.points.*`.
- **A1 vs A2.** At Λ ≳ 2 keV, A2 (PU 200) is *above* A1 (no PU) on the same rows. PU hits complete N_IP2 on surfaces
  where the quirk pair merged, and they seed planes for line-like ribbons. So **A1 is not an optimistic bound on A2 at
  Λ ≳ 2 keV**, and the high-Λ A2 candidates are PU-assisted: w_core, the plane and sep_IT^det are set by PU there
  (INV_SIGNAL_EFF §2–§3) [V-inv]. At Λ ≤ 1–1.5 keV, A1 > A2 (PU hurts wide ribbons).
- **A5 vs A2 at 1 keV:** they agree within the binomial error at R_A–R_C (largest difference E1000 R_A, 0.067 vs 0.094).
  The V4-6 CKF-stealing fraction in A5 is 0.21–0.57 % per point [U: transcribed from STAGE4_RESULTS_C12v1 §6, A5
  meta.v46; A5 is unchanged].

### 4.3 V4-6 full-chain revert (A2FC) [V]

A2 puts the quirk hits through numpy digitisation and never through the ACTS CKF, so CKF stealing was absent from A2.
The plan's rule (l. 1254, 1813) says a point with a V4-6 CKF-stealing fraction above 5 % reverts to the full chain.
The 9-point revert set was pre-declared from production A1 (fiducial ⟨f⟩ or pooled > 5 %), before any A2FC output
existed: {E200, E500, E1000, E1500} × {3, 5} keV plus Ẽ500 at 5 keV (`investigation/V46_REVERT_SET.json`, sha
`32e1c6c3…`). Ẽ500 at 3 keV (0.8 % / 1.9 %) and every point ≤ 2 keV stay numpy A2. The revert set uses A1 (no PU)
rather than the A5-with-PU wording of the plan. The with-PU paired re-runs give ⟨f⟩ at or below A1 at the 3 points
checked, so the set is plausibly complete (REVIEW_ANALYSIS_R6 C-3). Production: 180 jobs, 1 800 events, 9.7 CPU-h,
0 errors. Rows, order and seeds are identical to the paired A2 jobs. The PU measurement smearing is re-drawn by ACTS
(A2FC_REPORT §3).

Same rows; "numpy" = the previous A2 (`signal_eff.json → a2.a2fc_revert`, and C12_v1 for ε(r_fb) and μ₉₅):

| point | n | ε R04: numpy → full chain | ε R14: numpy → full chain | r_fb | ε(r_fb): numpy → full chain | μ₉₅ toys (events): C12_v1 → C12FC_v1 |
|---|---|---|---|---|---|---|
| E200 3 | 195 | 0.210 → 0.185 | 0.051 → 0.051 | FB4 | 0.051 → 0.051 | 3.9 → 4.3 × 10⁷ |
| E200 5 | 200 | 0.215 → 0.150 | 0.070 → 0.055 | FB4 | 0.070 → 0.055 | 4.0 → 4.6 × 10⁷ |
| **E500 3** | 200 | 0.320 → 0.305 | **0.110 → 0.020** | FB3 | **0.145 → 0.055** | 9.9 × 10⁶ → 1.4 × 10⁷ |
| E500 5 | 200 | 0.300 → 0.235 | 0.120 → 0.080 | FB4 | 0.120 → 0.080 | 3.0 → 3.8 × 10⁷ |
| E1000 3 | 190 | 0.216 → 0.189 | 0.026 → 0.021 | FB3 | 0.042 → 0.053 | 3.8 → 2.1 × 10⁷ |
| E1000 5 | 195 | 0.215 → 0.195 | 0.072 → 0.072 | FB4 ∧ e > 1.3 | 0.067 → 0.062 | 4.9 → 6.4 × 10⁷ |
| E1500 3 | 200 | 0.235 → 0.210 | 0.035 → 0.030 | FB3 | 0.075 → 0.070 | 2.1 → 1.6 × 10⁷ |
| E1500 5 | 200 | 0.275 → 0.200 | 0.075 → 0.060 | FB4 ∧ e > 1.6 | 0.075 → 0.060 | 3.7 → 5.9 × 10⁷ |
| Ẽ500 5 | 200 | 0.265 → 0.245 | 0.085 → 0.080 | FB4 | 0.085 → 0.080 | 4.0 → 3.5 × 10⁷ |

- **At R04 the full chain is 5–30 % below numpy A2** (relative: −5 to −13 % at 3 keV, −8 to −30 % at 5 keV), as
  expected from CKF stealing. R04 is the only rung where the comparison is genuinely paired (INV_A2FC_E500 §4). The in-job ε of A2FC_REPORT (a different definition) is 4–21 % below A2 [V-inv].
- Only the 9 revert points changed in `signal_eff.json` between C12_v1 and C12FC_v1; every other A2 point is
  identical [V].
- The μ₉₅ changes mix the ε change with the R6 background changes (§11.2), so they are not a pure A2FC effect.
- **E500 at 3 keV: statistical (`investigation/INV_A2FC_E500.md`, closed).** The full chain loses far more at the deep
  rungs than elsewhere. Pass counts of 200 rows, numpy → full chain: R04 64 → 61, R08 (w < 4.7) 31 → 19, R09 27 → 13,
  R11 (χ² p > 0.05) 23 → 5, R14 22 → 4. FB3 (R14's non-width cuts with w < 9.4 mm; not nested in R14, §1.1) passes 29 → 11 of 200,
  so ε(FB3) = 0.145 → 0.055 (−62 %). E500 3 keV was the largest-ε point of the C12_v1 table; with it,
  the maximum fallback ε falls from 0.145 to 0.080. E1000 3 keV moves *up* (8 → 10 of 190 rows at FB3).

<!-- INV_A2FC_E500 -->
**Investigation conclusion (INV_A2FC_E500, 2026-10-16).** Statistical. Deep-rung pass/fail is dominated by the
measurement-noise draw, which A2FC fully re-draws. A2 22/200 is high and A2FC 4/200 is low against a replica expectation
of ≳ 10–11/200. Bookkeeping and models verified identical (INV_A2FC_E500). Only the numpy quirk noise was re-drawn;
the ACTS quirk-noise draw was never replicated, so "statistics" is a conclusion by exclusion.
- **No bug** [V-inv]: the A2FC merge replaces whole accumulator entries; rows, row order and all seeded inputs are
  identical at all 9 points; the quirk SimHits entering A2FC equal the numpy-A2 input (4 994/4 994 hits); ACTS and numpy
  smearing are the same Gaussian model (residual rms 0.98–1.01 σ); recounts give exactly 22 and 4.
- **The deep-rung paired comparison is effectively unpaired.** Re-drawing the quirk and PU measurement noise flips
  ≈ 25–50 % of the passing rows at R08–R14, so "same rows, same seeds" gives almost no variance reduction there. The
  A2 → A2FC changes at R08 and deeper, at all 9 revert points, are two nearly independent samples. Only R04 is
  genuinely paired.
- **Replicas** [E]: fresh numpy noise draws on the A2FC PU events give 10–11/200 at R14 (12 for the selection-biased
  production draw), a slight lower bound because only the 34 rows passing R08 in either production were re-drawn: i.e.
  **ε_R14 ≈ 0.05**, against
  numpy A2 22/200 (≈ 3σ high, mostly from its PU-noise draw) and A2FC **4/200 = 0.020 (68 % CP [0.010, 0.036])**
  (≈ 2–2.5σ low). At r_fb the full chain gives ε(FB3) = **11/200 = 0.055, 68 % CP [0.039, 0.076], 95 % [0.028,
  0.096]** [V].
- **This is somewhat unusual, and no mechanism was found.** The exact McNemar p of the 18/0 discordance at R10–R14 is
  **7.6 × 10⁻⁶** [E]; after a look-elsewhere factor ≈ 9–30 over the revert points the global p is **≈ 10⁻⁴–10⁻³** [E].
  Every tested mechanism (bookkeeping, inputs, noise model, CKF flags) was excluded, so it is classed as a joint
  statistical tail of two draws from statistically identical models.
- **The one identified full-chain-specific loss at E500 3 keV** is row 268, where the CKF stole 46 of 83 quirk hits:
  1/64 = 1.6 % at R04. The net R04 change 64 → 61 (−5 %) also contains 7/4 noise flips.
- **Consequence.** No fix; C12FC_v1 stands, and the full chain is the pre-registered reference at the revert points
  (replacing or averaging it with A2 would be post hoc). Deep-rung and fallback ε carry a large statistical uncertainty
  from few passing events. The CP interval (`STAGE4_SUMMARY.json → fallback_points.*.eps_rfb_cp68 / eps_rfb_cp95`) is
  the full statistical uncertainty: each row's pass is one Bernoulli trial over (event, noise draw), so noise draws are
  part of it. What the investigation shows is that the A2/A2FC pair is effectively unpaired at the deep rungs.
- **Systematic full-chain loss at the other 8 revert points** [V from `inv_a2fc_e500_paired.json`; E as a systematic].
  Per-point ε(r_fb) ratio full chain/numpy **0.67–1.25** (7 of 8 ≤ 1); E500 3 keV is the outlier at **0.38**. Summed
  over the 8 points, same rows:

  | selection | numpy → full chain | ratio | discordant numpy-only / FC-only | sign-test p |
  |---|---|---|---|---|
  | R04 (genuinely paired) | 382 → 318 | **× 0.83** | **84 / 20** | **1.6 × 10⁻¹⁰** |
  | R14 | 106 → 89 | × 0.84 | 50 / 33 | 0.08 |
  | r_fb (each point's own) | 116 → 101 | **× 0.87** | 52 / 37 | 0.14 |
  | FB3 | 149 → 125 | × 0.84 | 63 / 39 | 0.02 |

  This is a **systematic full-chain inefficiency (CKF hit stealing), not noise**. Every FB_k contains N_IP2 ≥ 7, so the
  R04 loss propagates into ε(r_fb). Row 268 alone accounts for only 1.6 % at E500 3 keV.
- **Consequence for the 31 numpy-A2 points [E, systematic on ε].** They may overestimate ε by up to about this factor
  (× 0.87 at r_fb). The factor was measured at 3–5 keV, where the V4-6 CKF fraction exceeds 5 %; at ≤ 2 keV it is likely
  smaller. The best-limit point E200 1.5 keV is one of the 31: with the factor, its ratio is **≈ 910** (790/0.87; ≈ 950
  with the R04 factor 0.83). This is a systematic on ε, not applied to `limits.json`. The null result, no exclusion, is
  unaffected (lower ε only raises μ₉₅/N_exp). JSON: `a2fc_revert.paired_aggregate_other_8`,
  `a2fc_revert.fullchain_eps_systematic`.

### 4.4 Fallback ε, SR-T ε, acceptance

ε(r_fb) is **0–0.080** at all 40 points (max Ẽ500 5 keV and E500 2 and 5 keV, 0.080) [V]. Seven points have ε = 0 in
both bins: E500/E1000/E1500 at 0.45 keV, E1500 at 0.6 keV, Ẽ500 at ≤ 0.85 keV.

**SR-T signal ε at r_fb** (PC-19 window; OOT from the assigned C1 B1 events) [V]:
- E200: 0–0.015;
- E500: 0–0.055;
- E1000: 0–0.036;
- E1500: 0–0.035;
- Ẽ500: 0–0.055.

That is 0–100 % (typically 30–70 %) of ε(r_fb) at m ≥ 500 GeV, and ≤ 27 % of it at E200 (0 at Λ ≤ 1.5 keV). SR-G ε = ε(r_fb) −
ε_SR-T.

**Acceptance (truth level, Stage-3, template half)** [V as read from `acceptance.json`]. A = ε_fid(|η_pair| < 2.5) ×
ε_trig × ε_presel|trig; ε_PV-ID = 1 (not modelled, [U]). The total is ε_tot = A × ε_finder (A43 assumes independence).

| species-mass | ε_fid | ε_trig | ε_presel\|trig | A | f (pT > 200) | A_incl = A·f | σ_norm [fb] | N(pT > 200) before cuts | N_exp = σ_norm · f · 3 ab⁻¹ · A [E] |
|---|---|---|---|---|---|---|---|---|---|
| E200 | 0.847 | 0.90–0.91 | 0.65–0.66 | 0.49–0.50 | 0.0476 | 0.0235–0.0240 | 219.2 | 3.1 × 10⁴ | 1.55–1.58 × 10⁴ |
| E500 | 0.830 | 0.92–0.93 | 0.74–0.75 | 0.57 | 0.104 | 0.059–0.060 | 6.11 | 1.9 × 10³ | 1.08–1.09 × 10³ |
| E1000 | 0.816 | 0.93–0.94 | 0.84–0.85 | 0.64–0.65 | 0.146 | 0.093–0.095 | 0.197 | 86 | 55–56 |
| E1500 | 0.752 | 0.94–0.95 | 0.81–0.82 | 0.58 | 0.169 | 0.098–0.099 | 0.0144 | 7.3 | 4.2 |
| Ẽ500 | 0.826 | 0.93 | 0.71–0.72 | 0.55 | 0.1135 | 0.062–0.063 | 0.458 | 156 | 85–86 |

**f (FIX R3-NORM).** A (and every factor of it) is a fraction of the Stage-3 template population, which is generated
with pT(QQ̄) > 200 GeV, |η_pair| < 4 (`sim/stage3/code/make_inputs.py`). The yield therefore needs the tail fraction
f = Σw(TRGS, pT > 200, |η| < 4)/σ_ref (the `mg_events.sigma_norm_fb` convention): E from `sim/results/xsec.json →
trigger_yields_E.rows[m].f_pt200_TRG_over_INC`, Ẽ500 from `data/sim/npz/S-TRGS_m500.npz` (no xsec.json row) [V]. Sanity
check: N_exp ≤ N(pT > 200, |η| < 2.5) before cuts at all 40 points (E200: 1.58 × 10⁴ vs 2.7 × 10⁴, ratio 0.58 ≈
ε_trig · ε_presel|trig = 0.59). `STAGE4_SUMMARY.json → normalisation`, `fallback_points.*.f_tail / A_incl`.

σ_norm is read from `sim/results/xsec.json`: E = `sigma_norm_nic2_fb` (includes N_IC = 2, × K; K from TH is [U]); Ẽ =
the TH 14 TeV column [U]. **N_IC = 2 (resolved).** E200: 2 × K (1.11) × σ_LO (98.74 fb) = 219.2 fb, equal to the
Stage-3 npz header `sigma_norm_fb` (`data/sim_stage3/inputs/F_m200_p2.npz`), to TH's N_IC = 2 table (220 fb) and to
plan l. 1050 ("N_IC = 2, LO × K"). The label "[fb, N_IC = 1]" in `sim/stage3/HANDOVER_STAGE4.md` l. 52 (and in the
C12_v1 report) is the error; a doc correction is proposed upstream (FIX_RESULTS_R1). μ₉₅/N_exp is correct for the
N_IC = 2 benchmark. Another N_IC rescales every ratio by 2/N_IC (best 790 → 527 at N_IC = 3; below 1 only for
N_IC > 1.6 × 10³).

---

## 5. Fallback limits (`limits.json`)

Expected 95 % CL limit on μ = signal events within trigger + preselection acceptance. It uses two-bin counting (SR-T,
SR-G), with each bin's B as one log-normal (median, σ_eff = ln(B₈₄/B_median)). The cross-category correlation is not
carried (limits flag). **Primary: hybrid CLs toys** (5 000 toys, seed 20261014, common random numbers; D4). The
asymptotic q̃_μ result is the cross-check. Bands are quantiles of the b-only test statistic from the same toys
(discrete at small B). σ₉₅ = μ₉₅/(3 ab⁻¹ · f · A) is a limit on the inclusive σ(pp → QQ̄) (§4.4); N_exp = σ_norm · f · 3 ab⁻¹ · A;
μ₉₅/N_exp < 1 would be an exclusion.

**Headline [V for μ₉₅; E for the ratio].** These expected limits use zero-count simulation bounds as background central
values (at the headline point SR-G is dominated by the 0/24 C′ PV-pair bound, §1.4, §2). They measure the reach of this
simulation set-up and are conservative, not the physics reach of a real search. The ratio is an **ESTIMATE** with a
large statistical uncertainty on ε: at the best point ε(FB2) = 9/200, 68 % CP [0.030, 0.065], 95 % [0.021, 0.084], and
deep-rung pass/fail also fluctuates with the measurement-noise draw (§4.3, INV_A2FC_E500). E200 1.5 keV stays on
numpy A2, which may overestimate ε by up to × 1/0.87 (systematic full-chain loss at the revert points, §4.3); with that
systematic the ratio is ≈ 910 [E]. No exclusion either way.
- **Best: E200, Λ = 1.5 keV, r_fb = FB2.** ε = 0.045 [0.030, 0.065], ε_SR-T = 0, S = 710 events, B₈₄ T / G = 2.6
  × 10⁶ / 8.9 × 10⁶. Then μ₉₅ = **1.25 × 10⁷** events, toy ±1σ band [8.6 × 10⁵, 1.9 × 10⁸], ±2σ [5.3 × 10⁴, 2.7 × 10⁹].
  The asymptotic result is 1.31 × 10⁷ (ratio 1.05). **μ₉₅/N_exp = 790**, and σ₉₅ = 1.7 × 10⁵ fb against σ_norm =
  219 fb (inclusive; N_exp = 1.58 × 10⁴).
- Second best: E200 2 keV (FB3), 820. All other points: 2.3 × 10³ (E200 1 keV) up to 6.0 × 10⁷ (E1500 0.85 keV).
- 33 of 40 points have a limit; 7 have ε = 0 in both bins (no limit).
- The 5σ discovery μ, where computed (16 points), is 2.2 × 10⁸–1.0 × 10⁹ events, far above every N_exp (μ_5σ/N_exp = 1.9 × 10⁴ at E200 2 keV up to
  2.4 × 10⁸ at E1500 5 keV). `mu_3events`
  is null everywhere.
- **Asymptotic/toys: 0.32–1.07** [V]. It is 1.02–1.07 at the points where one bin carries all the signal. It is
  0.32–0.72 where both bins carry signal and σ_ln is large, a genuine difference between the asymptotic and hybrid-toy
  statistics (FIX R6 item 1). The ×10⁻⁴ failure of C12_v1 is gone.
- The asymptotic ±1σ bands are very narrow (E200 1.5 keV: [1.28, 1.31] × 10⁷) and should not be used as the expected
  band. Use the toy bands (§11.3).

| point (Λ keV) | r_fb | ε(r_fb) | ε_SR-T | S | μ₉₅ toys [±1σ] | asym/toys | μ₉₅/N_exp |
|---|---|---|---|---|---|---|---|
| E200 0.45 / 0.6 | FB0 | 0.010 | 0 | 158 / 156 | 1.3 × 10⁸ [2.9 × 10⁶, 5.9 × 10⁹] | 1.07 | 8.0 / 8.1 × 10³ |
| E200 0.85 | FB0 | 0.020 | 0 | 315 | 6.3 × 10⁷ | 1.07 | 4.0 × 10³ |
| E200 1 | FB1 | 0.021 | 0 | 333 | 3.6 × 10⁷ | 1.06 | 2.3 × 10³ |
| **E200 1.5** | FB2 | 0.045 | 0 | 710 | **1.25 × 10⁷** [8.6 × 10⁵, 1.9 × 10⁸] | 1.05 | **790** |
| E200 2 | FB3 | 0.050 | 0.005 | 773 | 1.3 × 10⁷ [3.2 × 10⁶, 5.1 × 10⁷] | 0.72 | 820 |
| E200 3 / 5 (FC) | FB4 | 0.051 / 0.055 | 0.010 / 0.015 | 792 / 861 | 4.3 / 4.6 × 10⁷ | 0.43 / 0.41 | 2.8 / 2.9 × 10³ |
| E500 0.45 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E500 0.6 / 0.85 / 1 | FB0 | 0.005 / 0.025 / 0.040 | 0.005 / 0.010 / 0.020 | 5.4 / 27 / 44 | 1.4 / 1.6 / 0.97 × 10⁸ | 1.02 / 0.43 / 0.36 | 1.3 / 1.5 / 0.89 × 10⁵ |
| E500 1.5 | FB1 | 0.070 | 0.045 | 76 | 3.0 × 10⁷ | 0.37 | 2.7 × 10⁴ |
| E500 2 | FB2 | 0.080 | 0.055 | 87 | 2.0 × 10⁷ | 0.40 | 1.8 × 10⁴ |
| E500 3 (FC) | FB3 | 0.055 | 0.045 | 60 | 1.4 × 10⁷ | 0.63 | 1.3 × 10⁴ |
| E500 5 (FC) | FB4 | 0.080 | 0.045 | 87 | 3.8 × 10⁷ | 0.51 | 3.5 × 10⁴ |
| E1000 0.45 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E1000 0.6 / 0.85 / 1 | FB0 | 0.011 / 0.020 / 0.022 | 0 / 0.010 / 0.006 | 0.62 / 1.1 / 1.2 | 1.1 / 1.9 / 1.6 × 10⁸ | 1.07 / 0.36 / 0.51 | 2.0 / 3.5 / 2.9 × 10⁶ |
| E1000 1.5 / 2 | FB1 | 0.030 / 0.058 | 0.010 / 0.026 | 1.7 / 3.2 | 7.4 / 4.0 × 10⁷ | 0.55 / 0.47 | 1.3 × 10⁶ / 7.2 × 10⁵ |
| E1000 3 (FC) | FB3 | 0.053 | 0.032 | 2.9 | 2.1 × 10⁷ | 0.61 | 3.8 × 10⁵ |
| E1000 5 (FC) | FB4 ∧ e > 1.3 | 0.062 | 0.036 | 3.4 | 6.4 × 10⁷ | 0.48 | 1.2 × 10⁶ |
| E1500 0.45 / 0.6 | FB0 | 0 | 0 | 0 | no limit | — | — |
| E1500 0.85 / 1 | FB0 | 0.005 / 0.011 | 0 | 0.021 / 0.045 | 2.5 / 1.2 × 10⁸ | 1.07 | 6.0 × 10⁷ / 2.8 × 10⁷ |
| E1500 1.5 / 2 | FB1 | 0.030 / 0.035 | 0.015 | 0.13 / 0.15 | 7.7 / 6.7 × 10⁷ | 0.43 / 0.49 | 1.8 / 1.6 × 10⁷ |
| E1500 3 (FC) / 5 (FC) | FB3 / FB4 ∧ e > 1.6 | 0.070 / 0.060 | 0.035 / 0.030 | 0.29 / 0.25 | 1.6 / 5.9 × 10⁷ | 0.67 / 0.49 | 3.8 × 10⁶ / 1.4 × 10⁷ |
| Ẽ500 0.45–0.85 | FB0 | 0 | 0 | 0 | no limit | — | — |
| Ẽ500 1 / 1.5 | FB0 | 0.011 / 0.025 | 0.011 / 0.015 | 0.91 / 2.1 | 6.4 × 10⁷ / 1.4 × 10⁸ | 1.02 / 0.32 | 7.4 × 10⁵ / 1.7 × 10⁶ |
| Ẽ500 2 | FB1 | 0.055 | 0.025 | 4.7 | 4.2 × 10⁷ | 0.47 | 4.9 × 10⁵ |
| Ẽ500 3 / 5 (FC) | FB2 / FB4 | 0.077 / 0.080 | 0.041 / 0.055 | 6.6 / 6.9 | 2.4 / 3.5 × 10⁷ | 0.44 / 0.46 | 2.8 / 4.0 × 10⁵ |

S = N_exp·ε(r_fb) with N_exp = σ_norm · f · 3 ab⁻¹ · A [E] (FIX R3-NORM: S and μ₉₅/N_exp × f and × 1/f vs the
earlier version). With 68 % CP intervals and both toy bands: `tables_C12FC_v1.md` → "signal / fallback";
`STAGE4_SUMMARY.json → fallback_points`.

**Even with B = 0** [E], S ≥ 3 only at E200 (every Λ), E500 at Λ ≥ 0.6 keV, E1000 at 2 and 5 keV (max 3.4) and Ẽ500 at Λ ≥ 2 keV
(20 of 40 points). E1500 never reaches S ≥ 3 (max 0.29 events), and neither do the seven ε = 0 points.

---

## 6. P2 handles (detector level vs the right truth comparator)

**P2 verdict [V, detector level].** No measurement of m_Q or Λ at PU 200; only qualitative handles. Here "partial"
means exactly that: an ordering, not a measurement. *m_Q:* M_est is a pair-mass estimator (M_QQ̄ ≥ 2 m_Q): its pooled
median is 2.26 m_Q at PU 200, just above the 2 m_Q threshold (2.46 m_Q without PU), with no event below 1.5 m_Q without
PU and a PU-induced low cluster (19 % below 0.5 m_Q) at PU 200. The per-species medians order the masses, with a huge
per-event spread and a species-dependent median/m; there is no m_Q fit (§6.3). *Λ:* only
through the ε window (§6.1); without PU, sep_IT^det and w_core track Λ (§6.2, §6.3); at PU 200 sep_IT^det is NOT
MEASURABLE and w_core flattens. t_est / χ² vs Λ and `results/sensitivity.json` are **not produced** by the frozen
pipeline; the limits and the discovery μ are in `limits.json` (§5).

### 6.1 Λ edges (`edges_det.json`, half-maximum of ε(R04) in ln Λ, row-level bootstrap) [V]

| | lower edge (keV) | upper edge (keV) |
|---|---|---|
| **A1, no PU** (E200 / E500 / E1000 / E1500 / Ẽ500) | 0.61 / 0.65 / 0.76 / 0.71 / 0.85 | **4.70 / 5.38 / 5.89 / 6.05 / 6.60** |
| **A2, PU 200** | 1.05 / 1.03 / 1.05 / 1.10 / 1.22 | none in 0.45–5 keV (A2 grid ends at 5 keV) |
| truth: ℓ_max = R_IT (closed form) | 0.43 / 0.63 / 0.68 / 0.78 / 0.78 | — |
| truth: Δs = 100 µm (hit level) | 0.50 / 0.51 / 0.47 / 0.49 / 0.55 | — |
| **truth, physically appropriate comparator (post hoc): f(any IP surface merged) = 50 %** [V-inv] | — | **≈ 5 keV** (f at 5 keV = 0.48 / 0.51 / 0.55 / 0.52 / 0.47) |
| truth, Stage-3 "merging edge": median IT sep < 100 µm | — | 12.8 / 16.4 / 19.4 / 19.8 / 22.9 (*not* the comparator) |

- **The pre-declared comparator (d) of V4-3 (plan l. 1810), the 12.8–25 keV hit-level merging edge, is not met:** the
  A1 upper edges 4.7–6.6 keV are × 2.7–3.5 lower. The merged-surface 50 % comparator below was derived *afterwards*
  (INV_SIGNAL_EFF, truth level, after seeing that miss). It is physically motivated, but it is a post-hoc comparator.
- **The physically appropriate truth comparator for the detector upper edge is the merged-surface 50 % edge, ≈ 5 keV,
  not the 13–25 keV raw Stage-3 edge.** R04 needs *every* IP surface unmerged, and the quirk separation oscillates through zero, so a
  merge somewhere happens long before the *median* separation reaches 100 µm (`investigation/truth_degeneracy_*.json`,
  INV_SIGNAL_EFF §3.1). Against it, the A1 upper edges 4.7–6.6 keV agree within ≈ 1 keV. If f(any merged) ∨ f(seed
  degenerate) is used, the 50 % crossing is at ≈ 4–5 keV (f_either 0.31–0.38 at 3 keV, 0.50–0.60 at 5 keV) [V-inv].
- **Lower edge vs truth.** The A1 lower edge equals the ℓ_max = R_IT truth within ≈ 10 % for E500, E1000, E1500 and
  Ẽ500 (ratio 0.92–1.11, about 1–2 σ_stat). E200 sits × 1.4 higher (0.61 vs 0.43 keV): its wide, slow ribbons need
  more than ℓ_max < R_IT to pass N_IP2 ≥ 7. All five are × 1.2–1.6 above the Δs = 100 µm hit-level edge.
- The lower edge moves from 0.6–0.85 keV (no PU) to 1.0–1.2 keV at PU 200. Wide ribbons lose to PU.
- `make_figures.py` D9 overlays the Stage-3 `upper_merge100_hit` (the wrong comparator) and, with the actual
  `edges_det.json` layout, draws no detector edge at all (§11.3).

### 6.2 sep_IT^det [V]

- **PU 200 (A2, A5, A2FC): "NOT MEASURABLE AT PU 200"** (`sep_it_det.json`: `pu200_measurable = false`, a flag on every
  PU point). With the core-only estimator (FIX R6), the medians are flat at ≈ 18–26 mm for Λ ≥ 1.5 keV at every
  species-mass, while truth goes from 23 mm to 0.6 mm (all A2 points, including low-n ones: 15.8–58.1 mm). **No Λ
  information at PU 200 with this estimator.** At Λ ≳ 3 keV the candidate plane is itself PU-defined, so no core-based
  estimator can recover Λ⁻² there (INV_SIGNAL_EFF §5).
- **No PU (A1): measurable; it tracks truth within ≈ 10 % at 1.5–3 keV.** Examples: E500 2 keV 6.9 vs 7.0 mm, 3 keV
  3.3 vs 3.1 mm; E1000 3 keV 4.7 vs 4.3 mm. Below ≈ 1 keV it saturates at ≈ 20–45 mm (truth 25–165 mm). Above 5 keV it
  sits on a resolution floor (E500 5 keV 1.7 vs 1.1 mm).

### 6.3 m_Q handles: M_est, β_ToF, dE/dx, and w_core as the ℓ_max observable (D4-13 (a)) [V]

Re-extracted from `signal_obs_a1.npz` / `signal_obs_a2.npz` of C12FC_v1 by `make_stage4_summary.py`
(`STAGE4_SUMMARY.json → p2_detector.mass_observables`). Selection as in the C12_v1 report (it reproduces those numbers
exactly on C12_v1): B-field model BM, signal-matched candidates passing R04, the first matched candidate per (point,
row), finite values, pooled over Λ (A1: its whole Λ grid; A2: 0.45–5 keV, with the A2FC full-chain rows at the 9 revert
points). M_est = MET·cosh η/(βγ)_ToF (BTL time of flight). Median [q16, q84]:

| species-mass | M_est A1, no PU (GeV) | M_est A2, PU 200, R04 (GeV) | M_est A2 at r_fb (GeV) | M_est finite A1 / A2 | β_ToF A1 / A2 (median) | dE/dx A1 / A2 (MIP, median) |
|---|---|---|---|---|---|---|
| E200 | 541 [467, 764] | **483** [202, 702] | 471 [316, 608] | 1.00 / 0.94 | 0.53 / 0.68 | 1.78 / 1.52 |
| E500 | 1196 [1046, 1564] | **1113** [332, 1467] | 1083 [305, 1457] | 1.00 / 0.91 | 0.33 / 0.39 | 3.30 / 1.97 |
| E1000 | 2270 [2026, 2648] | **2070** [279, 2566] | 1951 [228, 2193] | 0.72 / 0.73 | 0.23 / 0.39 | 5.53 / 2.53 |
| E1500 | 3320 [3101, 4035] | **3137** [155, 3652] | 3358 [659, 3520] | 0.49 / 0.59 | 0.24 / 0.45 | 7.10 / 2.73 |
| Ẽ500 | 1410 [1184, 1812] | **1230** [190, 1688] | 1316 [147, 1581] | 0.94 / 0.82 | 0.31 / 0.42 | 2.42 / 1.69 |

n (rows) A1 / A2 R04 / A2 r_fb: 611–853 / 166–280 / 42–71 per species-mass; quantiles of β_ToF and dE/dx, and the
per-point table: `tables_C12FC_v1.md` → "m_Q handles", "w_core median at R04".

- **M_est keeps a monotone mass ordering of the medians at PU 200** (E: 483 < 1 113 < 2 070 < 3 137 GeV), also at r_fb.
  In-time PU BTL hits give it a long low tail (A2 q16 155–332 GeV against A1 q16 467–3 101 GeV) and push the β_ToF q84 to
  0.88–0.98. M_est is undefined (β_ToF ≥ 1 or no BTL hit) for 6–41 % of the A2 candidates.
- **M_est estimates the pair mass M_QQ̄ ≥ 2 m_Q, not m_Q** (`signal.py` l. 203). Pooled over the 40 A2 points (R04 ∧
  f_CKF < 0.2, first matched candidate per event: 1 051 events, **N = 850** with M_est defined), the **median is 2.26 m_Q
  at PU 200**, just above the 2 m_Q threshold and pulled down by the PU low cluster (2.46 m_Q without PU). **Without PU
  no event falls below 1.5 m_Q** (0 of 9 551; minimum 1.69 m_Q); at PU 200, 29 % (247 of 850) do. **At PU 200, 19 % fall
  below 0.5 m_Q** (162 of 850): a PU-induced low cluster from in-time BTL hits
  (`p2_detector.mass_observables.M_est_over_mQ_pooled`; cross-checked in `stage5/review/REVIEW_STAGE5_R2.md`). No m_Q
  fit or template was run.
- **dE/dx is diluted by PU** (A2 median 1.5–2.7 MIP against 1.8–7.1 without PU), so it keeps only a weak mass ordering
  at PU 200.
- **w_core (the ℓ_max observable), median at R04.** Without PU it is monotone in Λ above ≈ 0.85 keV
  (E500: 13.1 / 5.5 / 2.4 / 1.3 mm at 1 / 2 / 3 / 5 keV). At PU 200 it flattens to a floor of ≈ 10–12 mm at ≥ 3 keV
  (E500: 13.3 / 12.8 / 10.9 / 12.2 mm at 1 / 2 / 3 / 5 keV; exceptions E1000 5 keV 7.0 mm, E1500 5 keV 9.7 mm), with a
  weak slope at 0.45–2 keV: PU hits enter the core.
- t_est / χ² vs Λ and `results/sensitivity.json` as such are **not produced** by the frozen pipeline.

### 6.4 Acceptance

See §4.4 (truth level). Stage 5 reads `acceptance.json` for σ₉₅ and multiplies A by f (FIX R3-NORM, §11.3).

---

## 7. P1 (B-field coplanarity vs the multiple-scattering floor)

**Not measured at detector level.** That was decided before production (plan l. 1520, decision D4-9): the event-level
out-of-plane resolution (23–30 µm) equals the MS floor, so the detector-level Δs carries no P1 information. The frozen
Stage-4 outputs contain no coplanarity observable. The width w_core and χ²_core are used as background cuts, not as a
P1 measurement.

The only P1 deliverable is the **truth-level** U-2 panel (`acts/stage4/u2_panel/u2_panel.json`) [V, truth level].
r_q = Δs_BM/√(Δs_B² + Δs_MS²) is:
- 0.989–1.005 at 0.45 keV (quadrature);
- 0.95–1.00 at 0.6 keV;
- **0.80–0.97 at 1–3 keV** (sub-quadrature);
- 0.89–1.09 at 5–10 keV.

The crossover Λ_cross (median Δs_B = Δs_MS) is 1.91 / 1.50 / 1.25 / 1.16 keV (E200/500/1000/1500) and 1.59 keV (Ẽ500).
Stage 4 adds no detector-level statement on coplanarity.

---

## 8. Caveats (all)

1. **Untested factorisation chain.** Beyond the ρ = 2 reach (R06), B rests on width → χ²_core → 2S → F1 → dE/dx
   conditionals measured on substitute populations. T3 is degenerate (non-informative), and no cross-variable closure
   test exists for R07–R23 or any FB column. B there could be off in either direction by an unknown factor.
2. **Trend σ_ln dominance.** The trend term (2–6.3) and model spread (4.76) dominate σ_ln from R11 on. They are
   pre-registered conservative readings (A07, A08), not measurements, and they drive B₈₄ up along F1 and dE/dx.
3. **Barrel only** (|η(n₃)| < 1). The A1 barrel fraction is 0.19–0.28. Endcap and forward events are outside the
   analysis.
4. **Flagged SM proxies, all [E].** W(eν) and W(μν) (proxy of W(τ)), tt̄2ℓ, single top (t-channel), WW/WZ/ZZ, and the
   tW allowance = 0.10 × N_trig(tt̄) (A37, [U] ratio) have no hit-level sample. Each takes the max P(r | preselected)
   of the nearest sample. They make up 15–45 % of B_SM depending on the rung or column [V]. Z(ττ), Z(ℓℓ) with lost leptons and QCD
   multijets are not in N_trig (A48, [U]).
5. **5 % per-object veto inefficiency** [E] (A38). Each extra 5 % raises N_trig by ≈ 4 %.
6. **K_tt = 1.9** is a conservative deviation from the rule's 1.2–1.4 (D3). K = 1.4 elsewhere, with a ±30 %
   normalisation nuisance (σ_ln 0.262).
7. **N_trig = 4.08 × 10⁷ ± 2.0 %** is counted after the event-level preselection (USER D1). It is generator-level
   Pythia, VERIFIED as a pipeline number and an ESTIMATE as physics.
8. **D11 C′ dE/dx and h/o: maximum of two readings.** Per C′ row the larger B of (C′_PU chain) and (C′₀ factor) is
   used. The C′₀ reading wins in 121 of 126 dE/dx rows (ni30 uses the C′_PU chain in 5) [V]. The h/o C′₀ factor is 1
   (no hit records), so no h/o rejection is credited for C′. The looper takes its depth from C′₀ (§7 "low gun counts";
   a no-PU sample: REVIEW_ANALYSIS_R6 C-2).
9. **ε(R01–R04) are lower bounds** (D9, S4 hit-record coverage).
10. **PV-line factor 0.22** for NI is an upper value with no σ_ln (A39). ε_PV-ID = 1 is not modelled ([U]). The trigger
    turn-on and the TDR-021 thresholds are [U] (± 25 GeV on T₅₀).
11. **Future work, not done.** C2-C (extra SM W/Z/tt̄ statistics; USER), C4′ (the rest of the A2 grid; A5 → 20 points;
    USER), the endcap finder, and ρ = 3 (C5). ε, B and limits therefore exist at only 40 of the 307 points of the
    admissibility grid.
12. **Event replacement.** 11 events were replaced in admitted jobs (A5 1, C2B-B2 2, dens 2, SM 4, C′_PU 2) [V], by
    deterministic seed replacement after an ACTS φ-sector portal assertion. The orchestrator quotes ≈ 0.14 % overall
    [U].
13. **3 excluded G3 jobs** (G3B1_00021/00059/00077, ACTS navigation assertion "volume outside of bounds"). G3 is
    T_seed = 6 and is not in the analysis union (T_seed-mixing refusal), so this touches only the G3 verdict
    (127/130 jobs).
14. **D13 (LOG 2026-10-16 11:50; renamed from D12): A2FC_F1000_L3_000 admitted** despite a V4-1 FAIL. In event 6, 3 of 145 007 PU
    SimHits got no measurement (ACTS bounded smearing; tolerance 2). The loss is PU-only, the quirk closure is exact
    (51/51), and the effect on ε is negligible.
15. **A2FC pairing is at the PU-event level.** PU SimHits are identical, but the PU measurement smearing is re-drawn,
    so numpy-vs-full-chain differences include re-smearing scatter (§4.3; E1000 3 keV moves up).
16. **Deep-rung and fallback ε are statistically fragile.** <!-- INV_A2FC_E500 --> The E500 3 keV full-chain deep-rung
    loss (§4.3; ε(FB3) 29 → 11 of 200) is statistical (INV_A2FC_E500, closed): statistics plus measurement-noise
    draws, no merge bug, identical inputs and noise model; the only identified full-chain-specific loss there is row 268
    (CKF stealing, 1/64 = 1.6 % at R04). The deep-rung paired comparison is effectively unpaired. McNemar p =
    7.6 × 10⁻⁶, global ≈ 10⁻⁴–10⁻³ after look-elsewhere [E]: somewhat unusual, with no mechanism found; the ACTS
    quirk-noise draw was not replicated (only numpy re-draws), so "statistics" is a conclusion by exclusion.
    Consequence for all 40 points: deep-rung and fallback ε carry a large statistical uncertainty (few passing events);
    the CP intervals in `fallback_points` are the full statistical uncertainty (E200 1.5 keV: 9/200, 68 % CP
    [0.030, 0.065]). **In addition, a systematic full-chain loss** is seen at the 8 other revert points (paired R04
    84/20, p ≈ 1.6 × 10⁻¹⁰; r_fb × 0.87): the 31 numpy-A2 points, incl. E200 1.5 keV, may overestimate ε by up to
    about this factor (best ratio ≈ 910 [E]). Neither affects "no exclusion".
17. **A1 is not an upper bound on A2 at Λ ≳ 2 keV.** High-Λ A2 candidates are PU-assisted (§4.2).
18. **σ_norm N_IC: resolved, N_IC = 2** (§4.4). The values used include N_IC = 2 (= the Stage-3 npz header and TH's
    N_IC = 2 table); the HANDOVER_STAGE4 l. 52 label "N_IC = 1" is the error (doc correction proposed upstream). Another
    N_IC would rescale every μ₉₅/N_exp by 2/N_IC.
19. **Two-bin limit** with one log-normal per bin: the SR-T/SR-G correlation of shared sources is not carried (limits
    flag). SM and C′ enter SR-T and SR-G with identical B (A12), so treating the bins as uncorrelated is
    anti-conservative where both bins carry signal (partly offset by that double counting of SM/C′). It is irrelevant
    at the headline point (ε_SR-T = 0; asym/toys 1.05).
20. **Public geometry, no CMS software.** A public-geometry ACTS model of a CMS-Phase-2-like tracker, TDR-normalised
    PU, our own finder. The numbers are not CMS performance and carry no CMS endorsement.
21. **Truth vs detector.** Acceptance A, the U-2 P1 panel and the truth edges are truth level. Everything else is
    detector-level simulation (§0 Level). Two specific traps: A1 "finder ε ≥ 0.9" (§4.1) and the 13–25 keV truth edge
    (§6.1) are not the quantities the old report compared them with.
22. **V4-5 (independent finder cross-check) NOT RUN**, and **V4-4 PARTIAL** (T_seed = 4 bit-identity and G1b
    regressions only) (§11.5).
23. **ε_tot = A × ε_finder** assumes the truth-level acceptance and the detector-level finder ε are independent (A43);
    not tested.
24. **V4-3 is PARTIAL** with a post-hoc match definition, and the detector upper edge misses its pre-declared
    comparator (d) (§4.1, §6.1).
25. **M_est estimates the pair mass (≥ 2 m_Q), not m_Q**, and has a PU-induced low cluster at PU 200 (19 % below
    0.5 m_Q; §6.3).
26. **Known cosmetic frozen-code bug (not fixed; frozen).** `acts/stage4/analysis/products.py` l. 205–206 looks up
    `'trials_phimet'`, which `background.TR_KEYS` lacks, so the event-display PU-only fake has `met_phi = null` in
    `event_display.npz`. No number in this report uses it; Stage 5 works around it.

---

## 9. Decisions (pointers to LOG.md, ambiguities.json, review files)

| ID | decision | by | pointer |
|---|---|---|---|
| C1/C2 scope | Run C1, then C2 as is (each ≈ 27–30 h, above the 1-day cap); C4′ dropped (future work) | **USER** | LOG 2026-10-13 20:12 |
| G1b/G3 items | The 2 (later 3) failed G3 jobs are left out; A5 = 5 species-masses at 1 keV; signal-match definition pre-declared before any ε was seen; event replacement accepted | orchestrator | LOG 2026-10-13 20:35 |
| G3 action | G3 verdict FAIL. The pre-declared WP_RULE §6.4 action **T_seed := 4** was applied as a logged frozen-input change (frozen_inputs 7574e0b5 → 2adc8f9d) | pre-declared rule; applied by orchestrator | LOG 2026-10-14 00:30/00:40; g3/G3_REPORT.md; HASH_ADDENDUM §5 |
| C2 scope | After C1, run only C2-B (PU B1/B2); C2-C (SM extra statistics) is future work | **USER** | LOG 2026-10-14 ~00:40 |
| closure | Accept the pre-registered conservative end state (× N_obs/N_pred compounded, trend in σ_ln); re-measure T1/T1w at T_seed = 4 on C1's B1/B2; decline the +50 % statistics steps; no union-count rule change | **USER** | LOG 2026-10-14 ~00:40 |
| C1 launch | C1a/C1b split; C2B longest-first order; Friday STOP helper; HASH_ADDENDUM §1–§5 counted as WP_RULE A.3 for admission | orchestrator | LOG 2026-10-14 00:35 |
| PC-19 | SR-T t_min/t_max fix. Design points: t_max from the next-crossing rate, threshold 1e-4 per edge, σ_t,PV = 190 ps (varied 150/230). `WP_RULE_PC19.md` frozen after REVIEW R3 PASS | **USER** (design points); review loop | LOG 2026-10-14 01:50; review/FIX_SRT_TMIN_R1-R3 |
| D1 | N_trig counted after the event-level preselection (→ 4.08 × 10⁷) | **USER** | ambiguities.json D1; LOG 2026-10-14 ~05:00 |
| D2 | C′ rate_t at generator level, road ± 0.15 rad; PV-line 0.22 for NI; old NI 0.64–3.6 banned | orchestrator | D2 |
| D3 | SM σ per sample with hadronisation-failure correction; W(τ) split; K_tt = 1.9 (conservative deviation); W(eν)/W(μν) proxy | orchestrator | D3 |
| D4 | Toys primary, asymptotic cross-check | orchestrator | D4 |
| D5 | Literal BTL-present conditionals for SR-T | orchestrator | D5 |
| D6 | No env change; in-house CLs (asymptotic NLL fixed in R6) | orchestrator | D6 |
| D7 | V4-3 W_c/t_tol variants are a labelled diagnostic | orchestrator | D7 |
| D8 | T3s required only if an h/o factor < 1 is credited (never happened) | orchestrator | D8 |
| D9 | ε(R01–R04) labelled lower bounds | orchestrator | D9 |
| D10 | A28 reading of nested same-variable cuts (conservative) | orchestrator | D10 |
| D11 | C′ dE/dx and h/o: both readings, larger B used | orchestrator | D11; FIX_ANALYSIS_R6 item 4 |
| D12 (ambiguities.json) | V4-6 revert of the 9 A2 points to the full chain (A2FC), pre-registered rule | pre-registered rule; orchestrator-authorised | D12; A2FC_REPORT.md; INV_SIGNAL_EFF §7 |
| D13 (LOG; was D12) | Admit A2FC_F1000_L3_000 despite V4-1 FAIL (PU-only loss 3/145 007) | orchestrator | LOG 2026-10-16 11:50 |

**Numbering clash (resolved 2026-10-16, orchestrator):** the LOG.md 11:50 admission was renamed D13; D12 = the A2FC revert rule (`ambiguities.json`).

---

## 10. Future work: what a WP would need (suggestions [E], none pre-registered)

None of these can be applied to the frozen analysis. Each needs a new pre-registration (no rule change after the
freeze).
1. **A data-driven PU fake estimate.** In real data, measure the fake rate in a control region (e.g. inverted MET-road
   or Δφ(n₃, MET) sidebands, or out-of-time crossings) at the deep rungs. This replaces the ρ-thinning extrapolation
   and its trend/closure σ_ln. This is the only route to a PU term that is not dominated by σ_ln 2–8.
2. **More, and deeper, PU simulation.** A ρ = 3 campaign (C5), or a closure test with a real lever arm at R07–R09, would
   remove the trend and closure terms (≈ 1.5–2 in σ_ln, i.e. ≈ 1 decade of B₈₄). The remaining ≈ 3–4 decades of PU need
   a stronger PU variable.
3. **C′ conditionals from the no-PU C′₀ samples** (10⁵ per gun), factorised as "topology passes" × "PU-assisted
   acceptance", with its own closure test. That is worth ≈ 2–2.3 decades on the C′ bounds (INV_STATS_BKG §5).
4. **Time-tag credit for SM/C′ in SR-T.** They are prompt; sharing the PU per-hit late fraction (~10⁻⁴ per edge,
   PC-19) is worth up to ≈ 4 decades, but in SR-T only.
5. **Merging-robust signal selection.** Replace the counting rung's "every surface ≥ 2 hits" by a merging-tolerant
   count, or add a line-topology category for Λ ≳ 3 keV. Lower the seed-opening cut. Run the endcap finder. Together
   these raise the barrel-only ε ceiling (≈ 0.3) and keep the high-Λ points.
6. **Run C4′** (A2 grid → full chain at every Λ ≥ 3 keV point) so that no numpy A2 is used where CKF matters, and, if a
   less noisy deep-rung ε is wanted, a pre-declared K-fold noise-replica average (needs pre-registration;
   INV_A2FC_E500 §6).
7. **A PU-robust sep_IT estimator** (line-consistent hits across ≥ 3 IT layers), so the Λ⁻² handle survives PU 200
   (INV_SIGNAL_EFF §5 option b).
8. Even with items 2 + 3 + 4, ≈ 0–2 decades (SR-T) and ≈ 4–5 decades (SR-G) would remain (C12_v1 estimate, [E];
   **stale, not re-derived on C12FC_v1**: the ladder B₈₄ changed by × 0.74–0.95 at R07–R20, i.e. ≤ 0.13 decades, so the
   order of magnitude holds).
   **Item 1 (data-driven) is therefore the decisive one.** On the signal side, E1500, E1000 at most Λ, Ẽ500 at Λ ≤ 1.5 keV and the
   ε = 0 points stay out of reach (S < 3) even at B = 0.

---

## 11. Inputs and provenance

### 11.1 Run [V]

| item | value |
|---|---|
| run dir | `data/acts_stage4/analysis/C12FC_v1/` (log `C12FC_v1.log`; `run_all.log`) |
| command | `run_all --campaigns C1a,C1b,C2B,A2FC --out data/acts_stage4/analysis/C12FC_v1` (frozen, non-DEV) |
| analysis freeze | `analysis_freeze.json` sha256 **b42aef4d7b8df2b863c945af29ea9abd3b9fefe708049019de02aa90ff58f29b** (32 files), `freeze_match = true`, `dev = false` |
| governing docs | WP_RULE.md 1b2ea9bd…, WP_RULE_PC19.md d30bcc2f…, HASH_ADDENDUM.md e273c077…, frozen_inputs.json 2adc8f9d… (all `ok`) |
| T_seed | 4 |
| campaigns / jobs | C1a 875 + C1b 760 + C2B 480 + A2FC 180 = **2 295 jobs**, 0 production errors; analysis admission 2 295 / 2 295, 0 missing / invalid / not admitted / excluded |
| production CPU | C1a 55.5 + C1b 172.1 + C2B 145.0 + A2FC 9.7 = **382 CPU-h** (sum of job walls in `prod/*/_progress_*.jsonl`; 1 core per job) [V as sum; E as CPU-h] |
| PU samples | B1 12 000 events / 48 000 trials; B2 3 000 events / 6 000 trials |
| analysis runtime | 2 497 s; schema check ok for all 10 outputs |
| output sha256 | bsum_wp.json 9077ba14…, limits.json 4f99fe6a…, signal_eff.json 1d487acb…, background.json d4308ec6… |
| superseded | `C12_v1/` (freeze bce02b6f…, C1a + C1b + C2B, numpy A2 at all points); `C1_v1/` (C1a + C1b) |

Cosmetic issues:
- The manifest status for B1 shows `used 20` (the event-display collect), not the full B1 count.
- `limits.json → provenance` has `t_seed` / `campaigns` = null (bsum_wp.json carries them).

### 11.2 What changed C12_v1 → C12FC_v1 [V]

| quantity | C12_v1 | C12FC_v1 | cause |
|---|---|---|---|
| min B₈₄ SR-T / SR-G (rung) | 1.6 × 10⁶ / 1.6 × 10⁶ (R09) | 1.23 × 10⁶ / 1.23 × 10⁶ (R09) | looper "low gun count" from C′₀ (R6 item 3) |
| B₈₄ T / G at FB0 | 1.7 × 10⁸ / 2.7 × 10⁸ | 3.5 × 10⁶ / 6.4 × 10⁷ | A28 merge-population fix (R6 item 2): SM Z(νν) artefact removed |
| B₈₄ T / G at FB1 | 1.4 × 10⁸ / 1.9 × 10⁸ | 2.2 × 10⁶ / 2.5 × 10⁷ | same |
| B₈₄ T / G at FB2 | 9.3 × 10⁷ / 1.0 × 10⁷ | 2.6 × 10⁶ / 8.9 × 10⁶ | same (SR-T FB2 chain) |
| B₈₄ T / G at FB3 | 2.9 × 10⁶ / 2.9 × 10⁶ | 2.0 × 10⁶ / 2.0 × 10⁶ | looper |
| B₈₄ at R07–R20 (both categories) | — | × 0.74–0.95 | looper (R6 item 3) |
| B₈₄ at R21–R23, FB4e | — | net × 0.98–1.05 | D11 (R6 item 4: × 1.2–1.6 up) partly cancelled by the looper fix |
| asymptotic/toys at FB0/FB1 | 2–3 × 10⁻⁴ (failed) | 0.32–1.07 | saturated NLL offset (R6 item 1) |
| sep_IT^det at PU 200 | 41–58 mm (all band hits) | ≈ 18–26 mm at Λ ≥ 1.5 keV, flagged NOT MEASURABLE | core-only + flag (R6 item 5) |
| ε at 9 revert points | numpy A2 | full chain (A2FC) | V4-6 revert (R6 item 6) |
| best μ₉₅/N_exp (FIX R3-NORM normalisation; 53 / 37.6 before) | 1.1 × 10³ (E200 1.5 keV) | **790** (E200 1.5 keV; ε = 9/200, large statistical uncertainty) | lower SR-G B at FB2 |
| max ε(r_fb) | 0.145 (E500 3 keV) | 0.080 (E500 3 keV drop is statistical, INV_A2FC_E500) | A2FC (§4.3) |
| WP | none | none | — |

The R6 ESTIMATEs (FIX_ANALYSIS_R6 cascade: min B₈₄ → 1.2 × 10⁶; E200 1.5 keV μ₉₅ 1.74 → 1.25 × 10⁷) are confirmed by
the run.

### 11.3 STAGE4_SUMMARY.json and stage5/make_figures.py (stage5 changed only by FIX R3-NORM, item 7)

- `make_figures.py` does **not** read `STAGE4_SUMMARY.json`. It reads the run directory per `analysis/inputs/schema.json`
  plus the proposed files of `stage5/proposed_schema.json`. The summary therefore has no consumer-side schema
  constraint; it is `STAGE4_SUMMARY v2` (v1 keys kept where meaningful, incl. `p2_detector.M_est_median_A1/A2_GeV`;
  new `p2_detector.mass_observables` and `P2_verdict` (FIX R1); `fallback_points` and `validations` updated; new `a2fc_revert`, `statistics_reach`, `cprime`, `production`, `cited_investigations`).
- Mismatches found between `make_figures.py` and C12FC_v1 (by its own `Inputs.check()` and by reading its readers):
  1. **Proposed-file location.** make_figures looks for acceptance / edges_det / sep_it_det / event_display under
     `<results>/proposed/`, but run_all writes them at the top level of the run dir. Run with `--proposed
     data/acts_stage4/analysis/C12FC_v1`. Otherwise D7/D8 silently fall back to the trigger proxy for A, and D9–D11 are
     skipped.
  2. **`edges_det.json` layout.** proposed_schema expects `'spin|m' → {lower, upper}`. The real file has `'A1|F|500'` /
     `'A2|F|500'` → `{sample, lam_keV, truth, R04: {eff, lower, upper}, R14}`. `fig_edges` filters on
     `k.split('|')[0] == spin`, so **with the real file it draws 0 detector edges** (checked), only the truth edges. Its
     truth overlay is also the 13–25 keV `upper_merge100_hit`, the wrong comparator (§6.1).
  3. **`sep_it_det.json`.** Keys and fields match, but `fig_sepit` ignores the new `measurable` / `flag` fields and
     plots only A2 keys. It would draw the PU-200 values (flagged NOT MEASURABLE) as a calibration and omit the
     measurable A1 values.
  4. **Limit bands.** `limits.json → expected_toys` now has `band_1s` / `band_2s`. make_figures still draws the
     asymptotic bands (its schema note says toys have only a median), and those bands are near-degenerate here (§5).
  5. **Schema check issue:** `signal_obs_a2.npz: missing array file` (the npz has `src_file`).
  6. Consistent: σ_norm (xsec.json `sigma_norm_nic2_fb`), `limits.json` keys `expected_toys/median`,
     `expected_asymptotic`, `discovery`, `bsum_wp.json → ladder/rule`.
  7. **FIX R3-NORM.** `make_figures.py acceptance()` returned `A_trig_presel` without the pT(QQ̄) > 200 GeV tail
     fraction f (same error as the summary). It now returns A · f, which fixes its N_exp and the D6 σ₉₅ (now a limit on
     the inclusive σ(pp → QQ̄)); D5–D7 regenerated (`stage5/FIGURES_FINAL.md`).

### 11.4 Reproduction and self-check

```
python3 -I acts/stage4/results/make_stage4_summary.py      # STAGE4_SUMMARY.json, tables_C12FC_v1.md, headline_C12FC_v1.json
python3 -I acts/stage4/results/selfcheck_stage4.py         # headline numbers of this report vs the JSON
```
Both read only. They take < 1 s, use the stdlib only, and read `C12FC_v1/`, `C12_v1/` (comparison), `sim/results/xsec.json`,
`acts/stage4/u2_panel/u2_panel.json`, `data/acts_stage4/investigation/*.json` and the production progress logs
(make_stage4_summary also reads `data/sim/npz/S-TRGS_m500.npz` for the Ẽ500 f). Since FIX R3-NORM the self-check
also recomputes N_exp = σ_norm · f · 3 ab⁻¹ · A, σ₉₅ and μ₉₅/N_exp independently from `xsec.json`, `acceptance.json`
and `limits.json` (Ẽ500 f from the investigation's numpy value), and checks N_exp ≤ N(pT > 200, |η| < 2.5) before
cuts at all 40 points (the old E200 N_exp fails this check).

### 11.5 Validation status

| ID | status |
|---|---|
| V4-1 | PASS in 2 294 / 2 295 jobs; A2FC_F1000_L3_000 FAIL admitted (D13, LOG); analysis admission 0 invalid |
| V4-2 | DONE (fix R1), ρ_dens 0.966 |
| V4-3 | **PARTIAL**: ε_find ≥ 0.9 at 1.5–2 keV (0.90–0.97; Ẽ500 also 3 keV) with the any-candidate ≥ 50 % match defined post hoc in INV_SIGNAL_EFF (with R04 required: 0.64–0.77); not met at 1, 3, 5 keV (merging / seed degeneracy / CKF); pre-declared comparator (d) not met (§6.1); W_c/t_tol attribution: no effect at 2–5 keV |
| V4-4 | PARTIAL (T_seed = 4 bit-identity 85/85 arrays + negative control; G1b regressions) |
| V4-5 | NOT RUN |
| V4-6 | A5 at 1 keV 0.21–0.57 % [U]; A1 > 5 % at 3–5 keV → the 9-point A2FC revert applied |
| V4-7 | FAIL → pre-registered anti-conservative end state (× 1.500, × 1.606); T3 non-informative |
| V4-8 | N/A (Mac only) |
| V4-9 | PASS (G1) |
| V4-10 | PASS, leak 0 on every C′ topology [V] |

---

## Appendix A. The C12_v1 "anomalies and possible bugs" (§10 there): all resolved

| C12_v1 §10 item | resolution | pointer |
|---|---|---|
| 1. A1 (no PU) ε < A2 (PU 200) ε at Λ ≥ 1.5–3 keV | (ii) different denominators (all-η vs template \|η\| < 2.5), plus (i) genuine: PU hits complete N_IP2 and seed degenerate ribbons. A1 is not an upper bound at Λ ≳ 2 keV | INV_SIGNAL_EFF §1–§3; this report §4.2 |
| 2. A1 upper edge 4.6–7.5 keV vs truth 13–25 keV; no-trial rising with Λ | (ii) the pre-declared comparator is not the physically appropriate one; the any-surface-merged 50 % edge (derived post hoc) is ≈ 5 keV; no-trial rows are forward (cosmetic) | INV_SIGNAL_EFF §3; §6.1 here |
| (V4-3) "max 0.21 vs 0.9" | (ii) not the V4-3 quantity; with the post-hoc any-candidate match 0.90–0.97 at 1.5–2 keV (V4-3 PARTIAL) | INV_SIGNAL_EFF §1; §4.1 here |
| (new) CKF stealing absent from A2 | (iv) coverage gap; pre-registered V4-6 revert applied (A2FC, 9 points) | INV_SIGNAL_EFF §4, §7; A2FC_REPORT; §4.3 here |
| 3. Asymptotic CLs ≈ 2.7 × 10⁻⁴ × toys at FB0/FB1 | (ii) bug, cross-check only: NLL without saturated offset → unprofiled q̃. Fixed (R6 item 1) | INV_STATS_BKG §1; FIX_ANALYSIS_R6 |
| 4. SR-T FB2 chain missing p(R09 \| R06) (and the SM twin at FB0/FB1) | (ii) bug, conservative: A28 merge population could contain an added cut of the merged variable. Fixed (R6 item 2) | INV_STATS_BKG §2; FIX_ANALYSIS_R6; REVIEW_ANALYSIS_R6 |
| 5. Model spread 1.97 → 4.76 with more statistics; PU column non-monotone | (i) correct per frozen rule (conservative envelope); policy note for a future pre-registration | INV_STATS_BKG §3 |
| 6. sep_IT^det flat 41–58 mm at PU 200 | (iii) estimator used all band hits; now core-only and flagged NOT MEASURABLE AT PU 200 | INV_SIGNAL_EFF §5; FIX_ANALYSIS_R6 item 5 |
| side: looper "low gun counts" not implemented; C′ dE/dx and h/o source | (ii) implemented (R6 item 3); D11 both readings, larger B (R6 item 4) | INV_STATS_BKG §5; D11 |
| 7. Cosmetic (B1 `used 20`; repeated factor labels) | still present, harmless | §11.1 |

Fix review: REVIEW_ANALYSIS_R6 **PASS** (0 A / 0 B / 6 C).
