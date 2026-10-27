# REVIEW_RESULTS_R2 — critical review (round 2) of STAGE4_RESULTS.md + STAGE4_SUMMARY.json (C12FC_v1)

Reviewer: fresh critical reviewer (JFC), 2026-10-16. Status: COMPLETE. **Verdict ITERATE (0 A, 1 B, 9 C).**
Inputs: `acts/stage4/STAGE4_RESULTS.md` and `data/acts_stage4/analysis/STAGE4_SUMMARY.json` (both 13:30),
`review/REVIEW_RESULTS_R1.md`, `review/FIX_RESULTS_R1.md` (+ addendum), `investigation/INV_A2FC_E500.md` and its JSON
outputs, `stage5/review/REVIEW_STAGE5_R2.md`, the raw run `data/acts_stage4/analysis/C12FC_v1/`. Nothing else edited.

## Independent checks (own scripts, `.pixi/envs/default/bin/python`, scratchpad `r2_mass.py`)

| check | report / JSON | recomputed (raw C12FC_v1) | status |
|---|---|---|---|
| self-check | 121/121 | re-run `python3 -I selfcheck_stage4.py`: **121/121 passed** | OK |
| §6.3 A1 M_est median [q16, q84], E200…Ẽ500 | 541 [467, 764] / 1196 [1046, 1564] / 2270 [2026, 2648] / 3320 [3101, 4035] / 1410 [1184, 1812] | identical (signal_obs_a1.npz; BM ∧ L[:,3] ∧ first candidate per (key, row); n 723 / 853 / 611 / 747 / 674) | OK |
| §6.3 A2 R04 M_est | 483 [202, 702] / 1113 [332, 1467] / 2070 [279, 2566] / 3137 [155, 3652] / 1230 [190, 1688] | identical (n 200 / 280 / 166 / 199 / 211, inside the quoted 166–280) | OK |
| §6.3 A2 at r_fb M_est | 471 [316, 608] / 1083 [305, 1457] / 1951 [228, 2193] / 3358 [659, 3520] / 1316 [147, 1581] | identical (r_fb from limits.json admissibility; FB_k ∧ f_CKF < 0.2; n 52 / 71 / 49 / 42 / 49, inside 42–71) | OK |
| finite fraction A1 / A2 | 1.00/0.94, 1.00/0.91, 0.72/0.73, 0.49/0.59, 0.94/0.82 | identical | OK |
| β_ToF median A1 / A2 | 0.53/0.68, 0.33/0.39, 0.23/0.39, 0.24/0.45, 0.31/0.42; A2 q84 0.88–0.98 | identical; A2 q84 0.88–0.98 | OK |
| dE/dx median A1 / A2 | 1.78/1.52, 3.30/1.97, 5.53/2.53, 7.10/2.73, 2.42/1.69 | identical | OK |
| w_core E500 R04 A1 / A2 (1/2/3/5 keV) | 13.1/5.5/2.4/1.3; 13.3/12.8/10.9/12.2 mm | 13.06/5.49/2.44/1.26; 13.33/12.83/10.95/12.15 | OK |
| pooled M_est/m_Q (R04 ∧ f_CKF < 0.2) | A2: 1051 / 850 / 2.26 / 162 (19 %); A1: 0 of 9551 < 1.5, min 1.69 | A2 1051 / 850 / 2.256 / 162 (19.06 %); A1 9551 defined, 0 < 1.5, min 1.693, **median 2.464** | OK (A1 median not quoted, C-3) |
| ε(FB2) E200 1.5 keV CP | 9/200, 68 % [0.030, 0.065], 95 % [0.021, 0.084] | scipy beta: 68 % [0.0304, 0.0649], 95 % [0.0208, 0.0837]; JSON `fallback_points` n_den 200, k 9 | OK |
| other CP | FB3 11/200 68 % [0.039, 0.076], 95 % [0.028, 0.096]; R14 4/200 [0.010, 0.036] | [0.0389, 0.0762], [0.0278, 0.0963]; [0.0105, 0.0355] | OK |
| 37.6 | μ₉₅ 1.25 × 10⁷, N_exp from σ_norm 219.2 fb, A 0.5035 | 12 458 208 / 331 136 = 37.62; S = 14 901; σ₉₅ = 8 247 fb; 68 % CP → 26–56, 95 % → 20–81 ("≈ 1.5 either way" at 68 % is right) | OK |
| WP_RULE | no WP, §8 fallback | bsum_wp rule.wp {T: null, G: null}, branch "no WP in either category (§5.3): §8 fallback"; min B₈₄ 1.232e6 / 1.235e6 at ladder index 8 (R09), all 23 rungs > 0.11 in both; limits.json: 40/40 `branch = fallback both`, both categories `background_free_claim = false`, headline k_adm = table = 2, FB2 18.75 mm; mu_3events null everywhere | OK |
| E500 3 keV paired counts (§4.3) | R04 64→61, R08 31→19, R09 27→13, R11 23→5, R14 22→4, FB3 29→11; McNemar 7.6e-6 | inv_a2fc_e500_paired.json: identical; R10–R14 18/0, p = 7.63e-6; FB3 19/1 | OK |
| replicas | 10–12/200 at R14 | repsum.json: production numpy draw 12 (selection-biased), fresh draws 11, 10 | OK (C-5) |
| products.py bug (caveat 26) | `trials_phimet` absent from TR_KEYS | products.py l. 205–206 vs background.py l. 34: confirmed | OK |

All tabulated m_Q-handle values (A-1 of R1) reproduce exactly from `signal_obs_*.npz`. No headline number disagrees with
the raw outputs. No post-hoc element enters any number: the replica ε (≈ 0.05) is [E] and not used; the report says
explicitly that replacing/averaging A2FC with A2 would be post hoc; V4-3's `matched_any` and the merged-surface
comparator are labelled post hoc in §0, §4.1, §6.1, §11.5, Appendix A and caveat 24.

## R1 findings — status

| R1 | status | evidence |
|---|---|---|
| A-1 m_Q half of P2 | **RESOLVED** | §6 P2 verdict, §6.3 table + bullets, §0 P2 line, caveat 25, JSON `p2_detector.mass_observables`, `M_est_median_A1/A2_GeV`, `P2_verdict`; every value reproduced above; t_est / sensitivity.json "not produced" sentence present (§6, §6.3). M_est correctly re-worded as a pair-mass proxy (consistent with REVIEW_STAGE5_R2). |
| B-1 E500 3 keV scope | **RESOLVED in substance** (investigation closed and cited in §0, §4.3, §5, caveat 16, §10, §11.2, JSON), but the new conclusion text over-reaches in two places → new **B-1** below |
| B-2 V4-3 "MET" | RESOLVED (PARTIAL everywhere; post-hoc label; comparator (d) not met stated) |
| B-3 PU "not a sample-size problem" | RESOLVED (§2 row: ≈ 1.0 × 10⁹ trials, σ_ln ≈ 1.7 → median ≲ 0.02; checked 4.8e4 × 2330/0.11 = 1.02e9) |
| B-4 simulation-limited limits | RESOLVED (§0, §5, JSON note) |
| B-5 P1/P2 in §0 | RESOLVED (P1 line clear; P2 line present — see C-2 on its clarity) |
| B-6 FB_k definition | RESOLVED (§1.1 bullet and table label; §4.3 quotes FB3 29 → 11 directly) |
| C-1 … C-11 | all RESOLVED (C-4: 10⁻⁶/6 000 = 1.67e-10 ✓; C-9: ratios 0.91–1.12 / × 1.22–1.62 ✓ within rounding; C-10 point sets self-checked) |

## Findings

### Category A

None.

### Category B

**B-1. The E500 conclusion is stated more reassuringly than the investigation's own data support ("not a systematic
shift"; "the only genuine full-chain loss is one event").**
- *Location:* §4.3 last bullet ("At the other 8 revert points the full-chain/numpy ratio of ε(r_fb) is 0.67–1.25 …:
  noise-draw scatter of this size, **not a systematic shift**"); §0 "What changed" ("The only genuine full-chain loss is one
  event where the CKF stole quirk hits (≈ −5 % at R04, as estimated before)"); JSON `a2fc_revert.investigation.verdict`
  ("Only genuine full-chain loss: row 268 …, i.e. ~ −5 % at R04") and `p_tag` ("unusual but within the combined tail").
- *Evidence (inv_a2fc_e500_paired.json, summed over the 8 other revert points):* R04 382 → 318 (× 0.83), discordant
  A2-only / FC-only **84 / 20** (sign test p ≈ 10⁻¹⁰); R14 106 → 89 (× 0.84), 50 / 33 (p = 0.08); each point's r_fb 116 →
  101 (× 0.87), 52 / 37 (p = 0.14); FB3 63 / 39 (p = 0.02). 7 of the 8 ε(r_fb) ratios are ≤ 1. The report itself says
  one bullet earlier that R04 is 5–30 % lower "as expected from CKF stealing" and that R04 is genuinely paired; since
  every FB_k contains N_IP2 ≥ 7, that systematic loss propagates into ε(r_fb). At E500 3 keV, row 268 alone is 1/64 ≈
  −1.6 % at R04; the quoted −5 % is the net 64 → 61, which includes 7/4 noise flips. Also, the replica study re-drew only
  the *numpy* quirk noise; the single ACTS quirk draw lies below every numpy draw (R14 discordance 1/9, 1/8, 0/6, while
  numpy–numpy is 5/4, 5/3, 3/2), so "statistics" is a conclusion by exclusion with one direct test (fresh ACTS-seed quirk
  replicas) not run. The report's "somewhat unusual, no mechanism found" (§4.3, caveat 16) is honest; §0 omits it.
- *Failure:* a reader of §0/§4.3 concludes the full chain equals numpy A2 except for one event and pure scatter. The
  data say: a real CKF-driven deficit (≈ −15 % aggregate at R04 → r_fb at 3–5 keV) plus large noise scatter, and an
  E500 3 keV outlier whose explanation is statistical by exclusion. No number changes; the null conclusion is
  unaffected (lower ε only raises μ₉₅/N_exp; headline E200 1.5 keV is not a revert point).
- *Fix (text + JSON strings only):* (i) §4.3 last bullet → "0.67–1.25 (7 of 8 ≤ 1; aggregate r_fb × 0.87, R04 × 0.83):
  consistent with the CKF loss seen at R04 plus noise-draw scatter; E500 3 keV (0.38) is the outlier". (ii) §0 → "At
  E500 3 keV, the only identified full-chain-specific loss is one event (CKF stealing); the rest is attributed to
  measurement-noise draws — statistically unusual (global p ≈ 10⁻⁴–10⁻³), no mechanism found." (iii) §4.3 / caveat 16:
  add "the ACTS quirk-noise draw was not replicated (only numpy re-draws)". (iv) JSON: drop "i.e. ~ −5 % at R04" from the
  row-268 sentence (or say "net R04 64 → 61"), and "within the combined tail" → "no mechanism found; conclusion by
  exclusion".

### Category C (optional)

- **C-1. Noise draw vs binomial (§4.3 "Consequence", JSON `best_mu95_over_Nexp.tag`).** "CP intervals … do not include the
  noise-draw spread beyond binomial" / "binomial + noise-draw uncertainty" suggests an extra component. Each row's pass
  is one Bernoulli trial over (event, noise draw), so the binomial CP interval already contains the noise-draw variance
  (conditioned on fixed rows the spread is *smaller*, Σp_i(1−p_i)). What the investigation shows is that the A2/A2FC
  pair is effectively unpaired, not that CP undercovers. Suggest "the CP interval is the full statistical uncertainty;
  noise draws are part of it".
- **C-2. §0 P2 line has no verdict word, and §6 "m_Q: partial" is not defined.** P1 gets a bold "not addressed at
  detector level"; P2 is jargon (M_est, (βγ)_ToF, pair-mass threshold) with no plain conclusion. Suggest leading with
  "**P2: no measurement of m_Q or Λ at PU 200; only qualitative handles**" — the median of a pair-mass proxy orders the
  four E masses, but per-event spread is huge (A2 q16 155–332 GeV for *every* mass, e.g. E1000 [279, 2566] GeV), the
  median/m ratio is species-dependent (A2: 2.07–2.46; E500 1113 vs Ẽ500 1230 GeV), and Λ is only bracketed by where ε
  turns on/off. Define "partial" in §6 the same way.
- **C-3. "Median 2.26 m_Q … i.e. at the pair-mass threshold"** (§0, §6, §6.3, JSON): 2.26 is *above* 2 m_Q, and it is
  pulled down by the 19 % PU low cluster. Say "just above the 2 m_Q threshold (no PU: 2.46 m_Q, from the same
  `M_est_over_mQ_pooled.values.A1`)"; also 29 % (247/850) fall below 1.5 m_Q at PU 200, the natural counterpart of the
  "0 below 1.5 m_Q without PU" statement.
- **C-4. §0 "Why" 1: "These bounds are about 3–6 × 10⁵ events".** Individual bounds are 1.4–1.7 × 10⁵ (C′ DIF, PV
  pair); 3–4 × 10⁵ is their sum with the SM bounds (R08–R23, §1.3). Say "together ≈ 3–4 × 10⁵ events (median)".
- **C-5. Replica expectation is a slight lower bound.** The fresh draws cover only the 34 rows that passed R08 in either
  production (repsum.json); rows outside that set could also pass. "≈ 10–11/200" → "≳ 10–11/200" (and the JSON
  `replica_eps_R14_E500_3keV`). Direction strengthens the "A2FC is low" reading only marginally.
- **C-6. §6.1 table row "truth, correct comparator"** is bold and unlabelled in the table; the post-hoc label is only in
  the bullet. Add "(post hoc)" to the row label.
- **C-7. §0 heading "What is solid"** introduces a PARTIAL validation and a missed pre-declared comparator. "What was
  measured at detector level" would read more accurately.
- **C-8. §0 robustness sentence.** "A lower ε would only raise it, so 'no exclusion' is robust" — add the upper side
  too: even the 95 % CP upper ε (0.084) gives ≈ 20, and exclusion would need ε ≈ 1.7 (impossible).
- **C-9. §0 "best expected limit is 37.6 × the predicted signal yield"** — for a plain reader add "(the signal would have
  to be 37.6 times larger than predicted to be excluded)".

### Checked and fine (no finding)

WP_RULE §5.3 → §8 applied with nothing post-hoc (above); 37.6 and its CP intervals; all §6.3 m_Q-handle values; P1
verdict (§0, §7: D4-9, truth-level U-2 only — consistent with the plan); E500 numbers in §4.3 and caveat 16 match the
investigation JSONs; "replacing or averaging with A2 would be post hoc" correctly stated; investigation status CLOSED
consistently in report and JSON (no stale "pending"/"OPEN"); removal of R1's "31 numpy points carry an unassigned
full-chain systematic" is justified by the investigation (no numpy-vs-ACTS model difference found; CKF governed by the
pre-registered 5 % V4-6 rule, headline point not in the revert set); caveat 26 (products.py) verified against source;
§2 statistics-reach arithmetic; §3 ρ = 2 reach; §5 S, σ₉₅; §4.3 R04 relative losses (−5 to −13 % at 3 keV, −8 to
−30 % at 5 keV); §0 PU fall 4.9 decades.

## Verdict: **ITERATE**

Category A: 0. Category B: 1 (B-1: "not a systematic shift" / "only one genuine full-chain loss (≈ −5 %)" over-reach the
INV_A2FC_E500 evidence — aggregate R04 84/20 and r_fb × 0.87 at the other 8 revert points; ACTS quirk noise not
replicated; §0 omits "unusual, no mechanism found"). Category C: 9. All R1 items are resolved; every number checked
(m_Q table, 37.6, CP intervals, WP branch) agrees with the raw outputs. A text-only fix of B-1 (no re-run) should PASS.
