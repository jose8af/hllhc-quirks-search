# FIX_RESULTS_R2: fixes for REVIEW_RESULTS_R2 (0 A, 1 B, 9 C)

Fixer (JFC), 2026-10-16. Text and JSON changes only, with no re-run. The only new numbers are sums over the
investigation's paired output `data/acts_stage4/investigation/inv_a2fc_e500_paired.json`. Frozen code, production
data, `C12FC_v1/`, `stage5/`, `investigation/` and `sim/` were not touched.

Files changed:
- `acts/stage4/STAGE4_RESULTS.md`
- `acts/stage4/results/make_stage4_summary.py`: new `sign_test_p()` and `a2fc_paired_aggregate()`; new JSON blocks
  `a2fc_revert.paired_aggregate_other_8` and `a2fc_revert.fullchain_eps_systematic`; reworded strings.
- `acts/stage4/results/selfcheck_stage4.py`: 121 → **151 checks, 151/151 PASS**.
- Regenerated `data/acts_stage4/analysis/STAGE4_SUMMARY.json`, `tables_C12FC_v1.md` and `headline_C12FC_v1.json`.

No headline number changed. The ≈ 43 is an additional ESTIMATE, a systematic on ε. It is not applied to
`limits.json`.

## B-1: E500 conclusion over-reached (RESOLVED, following the coordinator's instruction)

The paired evidence, summed over the 8 other revert points (same rows), with the exact two-sided sign test:

| selection | numpy → full chain | ratio | discordant numpy-only / FC-only | p |
|---|---|---|---|---|
| R04 | 382 → 318 | × 0.83 | **84 / 20** | **1.6e-10** |
| r_fb | 116 → 101 | **× 0.87** | 52 / 37 | 0.14 |

7 of the 8 per-point ratios are ≤ 1.

Report changes:
- **§4.3:** new table and bullet stating that this is a **systematic full-chain inefficiency (CKF), not noise**.
  - Row 268 alone is 1.6 % (1/64) at R04; the net 64 → 61 also contains 7/4 noise flips.
  - Only the numpy quirk noise was re-drawn. The ACTS quirk-noise draw was never replicated, so "statistics" is a
    conclusion by exclusion.
  - Consequence: the 31 numpy-A2 points, including the best-limit point E200 1.5 keV, may overestimate ε by up to
    about × 1/0.87. The best ratio is then **≈ 43** (37.6/0.87; ≈ 45 with the R04 factor 0.83), labelled [E] as a
    systematic on ε. The factor was measured at 3–5 keV and is likely smaller at ≤ 2 keV. No exclusion either way.
- **§0:**
  - A new "Full-chain systematic on ε [E]" bullet (≈ 43, null result unaffected).
  - "What changed" now carries "statistically unusual (global p ≈ 10⁻⁴–10⁻³), no mechanism found".
  - "What changed" also states the systematic loss at the other 8 points.
- **Other places:**
  - §5 headline: the same systematic and ≈ 43.
  - Caveat 16 rewritten.
  - "not a systematic shift" and "only genuine full-chain loss … ≈ −5 %" removed.
- **JSON:**
  - `investigation.verdict`: "~ −5 % at R04" dropped; row 268 = 1.6 %; the systematic loss is stated.
  - `p_tag`: "somewhat unusual; no mechanism found; conclusion by exclusion".
  - `outcome.best_mu95_over_Nexp.tag` points to the systematic.

## Category C

| finding | change | status |
|---|---|---|
| C-1 CP vs noise draw | §4.3 Consequence and the JSON say the CP interval is the full statistical uncertainty and noise draws are part of it; the point is that the pair is unpaired. | RESOLVED |
| C-2 P2 verdict word | §0 P2 line leads with "**no measurement of m_Q or Λ at PU 200; only qualitative handles**". It adds the per-event spread (q16 155–332 GeV for every mass), the species-dependent median/m and that Λ is only bracketed by the ε turn-on/off. §6 defines "partial" the same way. JSON `P2_verdict.m_Q` updated. | RESOLVED |
| C-3 "at the pair-mass threshold" | Changed to "just above the 2 m_Q threshold (2.46 m_Q without PU)", pulled down by the PU low cluster. Added: 29 % (247/850) below 1.5 m_Q at PU 200. Applied in §0, §6, §6.3 and the JSON. | RESOLVED |
| C-4 bounds 3–6 × 10⁵ | §0 "Why" 1: "individually 1.4–1.7 × 10⁵ (C′ DIF, PV pair); together with the SM bounds ≈ 3–4 × 10⁵ (median)". | RESOLVED |
| C-5 replica lower bound | "≳ 10–11/200"; 10–11 from fresh draws (12 from the selection-biased production draw); only the 34 rows were re-drawn. JSON `replica_eps_R14_E500_3keV.lower_bound = true`. | RESOLVED |
| C-6 §6.1 row label | Now "physically appropriate comparator (post hoc)". | RESOLVED |
| C-7 "What is solid" | Renamed "What was measured at detector level". | RESOLVED |
| C-8 upper side | Added: even the 95 % CP upper ε (0.084) gives ≈ 20, and an exclusion would need ε ≈ 1.7. | RESOLVED |
| C-9 plain reading | Added: "(the signal would have to be 37.6 times larger than predicted to be excluded)". | RESOLVED |

## Verification

`python3 -I acts/stage4/results/make_stage4_summary.py`, then `selfcheck_stage4.py`: **151/151 PASS**.

The 30 new checks cover:
- the aggregates, recomputed from `inv_a2fc_e500_paired.json`: 84/20, p 1.6e-10, × 0.83, 116 → 101, × 0.87, 7 of 8,
  and per-selection consistency;
- the 31 affected points, with the best point among them;
- the corrected ratios 43 and 45;
- §0 containing "statistically unusual", "no mechanism was found", "not noise" and "unaffected";
- the absence of the over-reaching phrases;
- the C-3 numbers (2.46, 29 %, 247 of 850), the C-4 bound values, the C-8 arithmetic (≈ 20, ε ≈ 1.7) and the
  C-5/6/7/9/2 text.
