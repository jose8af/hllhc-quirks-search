# FIX_RESULTS_R3_NORM: signal normalisation (tail fraction f) — fixer, 2026-10-16

**Finding.** Category A, CONFIRMED in `acts/stage4/investigation/INV_NORM_F200.md` (output
`data/acts_stage4/investigation/inv_norm_f200.json`). Found by the P2 novelty audit and paper review R2 (A-2). The expected
signal yield was N_exp = σ_norm · L · A, with σ_norm the inclusive σ(pp → QQ̄) (N_IC = 2) and A = `acceptance.json →
A_trig_presel`, which is conditional on the Stage-3 template population (pT(QQ̄) > 200 GeV, |η_pair| < 4). The tail
fraction f was missing. Correct: **N_exp = σ_norm · f · L · A**; σ₉₅(inclusive) = μ₉₅/(L · f · A).

**Nature of the change.** This corrects an error that makes every limit **weaker** (ratios × 1/f = 5.9–21). It is
applied **after** the Stage-4 results review PASS. Conclusions unchanged: no WP; no point excluded or discoverable.
μ₉₅ and its bands, B, ε, `limits.json`, `acceptance.json` and the frozen analysis code (`acts/stage4/analysis/*`) are
unchanged; no Stage-4 re-run.

## Changes
1. `acts/stage4/results/make_stage4_summary.py`
   - new `tail_fraction()`: E reads `sim/results/xsec.json → trigger_yields_E.rows[m].f_pt200_TRG_over_INC`; Ẽ500 (no
     xsec.json row) computes Σw(pT_pair > 200, |η_pair| < 4)/σ_ref_fb from `data/sim/npz/S-TRGS_m500.npz` (the same
     computation as `inv_norm_f200.py`; stdlib npz reader); both carry provenance and the INV value for comparison;
   - `n_exp = σ_norm · f · L · A` (was l. 146), `sigma95_fb = μ/(L · A · f)` (was l. 165); S, μ₉₅/N_exp and the
     full-chain-systematic ratio follow;
   - new keys: `fallback_points.*.f_tail / A_incl (= A · f) / N_pt200_before_cuts_3ab`, top-level `normalisation`
     (formula, f per species-mass with source, definition, erratum), `outcome.best_mu95_over_Nexp.value_before_fix_r3_norm`;
     the tag's hard-coded "ratio ~ 43" is now computed (~ 907);
   - `tables_C12FC_v1.md`: f column and formula line.
   - Regenerated `data/acts_stage4/analysis/STAGE4_SUMMARY.json`, `acts/stage4/results/tables_C12FC_v1.md`,
     `acts/stage4/results/headline_C12FC_v1.json`. Max relative difference vs INV `ratio_corr`: 1.0 × 10⁻⁴ (E1500: xsec.json
     f has no |η| < 4 cut, 1.7 × 10⁻⁴ relative; as specified, f is read from xsec.json).
2. `acts/stage4/results/selfcheck_stage4.py`
   - new independent block: N_exp recomputed from `xsec.json` (σ_norm, f) + `acceptance.json` (A) (+ Ẽ500 f from the
     investigation's numpy value), σ₉₅ and μ₉₅/N_exp from `limits.json`, at all 40 points (1e-9); f(summary) = sources;
     **sanity N_exp ≤ N(pT > 200, |η| < 2.5) ≤ N(pT > 200) before cuts** at all 40 points (the old E200 N_exp fails it,
     checked); best = INV best_after (790); erratum box and new formula text present; old formula/headline gone;
   - updated assertions: best 790, second 820, worst 6.0 × 10⁷, S ≥ 3 set (27 → 20 points), E1500 max S 0.29, E1000 max
     S 3.4, C-8 (≈ 420; ε ≈ 36 needed), full-chain systematic ≈ 910 / ≈ 950, C-9 plain text.
   - **Result: 165/165 checks passed.**
   - Why the old self-check missed it: it re-read N_exp from the summary JSON produced by the same formula and only
     checked σ_norm(E200) = 219.2 fb (inclusive); nothing recomputed N_exp from primary inputs or compared it with
     N(pT > 200). Stage 5 cross-checked against the same JSON at 10⁻⁶.
3. `acts/stage4/STAGE4_RESULTS.md`: erratum box under the header; §0 (best 790, per-mass best, up to 6 × 10⁷, 95 % CP
   ≈ 420 / ε ≈ 36, systematic ≈ 910 / 950, E1500 ≤ 0.3 events, E1000 ≤ 3.4, C12_v1 comparison 1.1 × 10³ → 790); §4.3
   systematic; §4.4 acceptance table (f, A_incl, N(pT > 200) before cuts, new N_exp) + f paragraph and sanity check;
   N_IC sentence (790 → 527 at N_IC = 3; < 1 only for N_IC > 1.6 × 10³); §5 σ₉₅ definition (inclusive), headline
   (S = 710, μ₉₅/N_exp = 790, σ₉₅ = 1.7 × 10⁵ fb, N_exp = 1.58 × 10⁴), second best 820, range 2.3 × 10³–6.0 × 10⁷,
   μ_5σ/N_exp 1.9 × 10⁴–2.4 × 10⁸, full table (S and μ₉₅/N_exp for all 40 points); **zero-background reach**: S ≥ 3 at
   B = 0 only at 20 of 40 points (E200 all Λ, E500 Λ ≥ 0.6, E1000 2 and 5 keV, Ẽ500 Λ ≥ 2 keV; E1500 max 0.29); §6.4;
   §9 item 16; §10 item 8; §11.2 row; §11.3 heading + item 7; §11.4.
4. `stage5/make_figures.py` (targeted hunks only; the paper fixer's concurrent text edits were preserved — mtime checked
   and file re-read before editing): new `tail_fraction()`; `acceptance()` returns `A_trig_presel · f` for the
   acceptance.json branch (fixes `n_exp()` and the D6/D7 σ₉₅ together; consistent with the fallback branch, already
   inclusive); D5 legend "N_exp = σ_norm · f · L · A"; D6 y label "95 % CL limit on inclusive σ(pp → QQ̄) [fb]".
   Regenerated D5 (5), D6 (6), D7 (1) in `stage5/figures/final/` (`nice -n 15`, 5 s CPU); all 12 PNGs opened; N_exp
   cross-check vs the new summary passes. `stage5/FIGURES_FINAL.md`: new FIX R3-NORM section; D5/D6/D7 numbers; the
   "−2σ edge below N_exp/σ_th" caveats removed (min −2σ/N_exp now 1.7).
5. `LOG.md` lines appended.

**Not changed (out of scope, flagged):** `paper/figures/D5_limit_mu_vs_lambda_F200.pdf`, `D6_limit_xsec_vs_m_L1p5.pdf`,
`D7_exclusion_map.pdf` are now stale copies (differ from `stage5/figures/final/`), and the paper text cites 37.6 / ≈ 43;
the paper fixer must re-copy and update. `STAGE4_SUMMARY_C12v1.json` / `STAGE4_RESULTS_C12v1.md` (superseded) keep the
old formula. The tail-rate nuisance on f (+12…+15 / −11…−13 %, `sim/stage3/plan.md:431`) is not propagated (ESTIMATE-level,
small against the ×6–21 shift; no exclusion either way).

## Best μ₉₅/N_exp per species-mass (after)
| species-mass | point | before | after |
|---|---|---|---|
| E200 | 1.5 keV | 37.6 | **790** |
| E500 | 3 keV (FC) | 1.38 × 10³ | **1.33 × 10⁴** |
| E1000 | 3 keV (FC) | 5.51 × 10⁴ | **3.78 × 10⁵** |
| E1500 | 3 keV (FC) | 6.46 × 10⁵ | **3.83 × 10⁶** |
| Ẽ500 | 3 keV (FC) | 3.15 × 10⁴ | **2.77 × 10⁵** |

Full-chain systematic ESTIMATE on the best point: 37.6/0.87 ≈ 43 → **790/0.87 ≈ 907 (≈ 949 with the R04 factor)**.

## Before / after per point (μ₉₅, B, ε unchanged)
| point | f | A | A_incl | N_exp before → after | S before → after | σ₉₅ [fb] before → after | μ₉₅/N_exp before → after | μ_5σ/N_exp before → after |
|---|---|---|---|---|---|---|---|---|
| E200 0.45 | 0.0476 | 0.504 | 0.0240 | 3.31e+05 → 1.58e+04 | 3.31e+03 → 158 | 8.37e+04 → 1.76e+06 | 382 → **8.01e+03** | – → – |
| E200 0.6 | 0.0476 | 0.498 | 0.0237 | 3.28e+05 → 1.56e+04 | 3.28e+03 → 156 | 8.46e+04 → 1.78e+06 | 386 → **8.1e+03** | – → – |
| E200 0.85 | 0.0476 | 0.503 | 0.0240 | 3.31e+05 → 1.58e+04 | 6.62e+03 → 315 | 4.19e+04 → 8.79e+05 | 191 → **4.01e+03** | – → – |
| E200 1 | 0.0476 | 0.499 | 0.0238 | 3.28e+05 → 1.56e+04 | 6.98e+03 → 333 | 2.4e+04 → 5.03e+05 | 109 → **2.29e+03** | – → – |
| E200 1.5 | 0.0476 | 0.504 | 0.0240 | 3.31e+05 → 1.58e+04 | 1.49e+04 → 710 | 8.25e+03 → 1.73e+05 | 37.6 → **790** | – → – |
| E200 2 | 0.0476 | 0.493 | 0.0235 | 3.24e+05 → 1.55e+04 | 1.62e+04 → 773 | 8.56e+03 → 1.8e+05 | 39.1 → **820** | 906 → 1.9e+04 |
| E200 3 | 0.0476 | 0.493 | 0.0235 | 3.24e+05 → 1.55e+04 | 1.66e+04 → 792 | 2.92e+04 → 6.13e+05 | 133 → **2.8e+03** | 2.67e+03 → 5.61e+04 |
| E200 5 | 0.0476 | 0.500 | 0.0238 | 3.29e+05 → 1.57e+04 | 1.81e+04 → 861 | 3.07e+04 → 6.44e+05 | 140 → **2.94e+03** | 2.56e+03 → 5.38e+04 |
| E500 0.45 | 0.1042 | 0.565 | 0.0589 | 1.04e+04 → 1.08e+03 | 0 → 0 | – → – | – → **–** | – → – |
| E500 0.6 | 0.1042 | 0.566 | 0.0590 | 1.04e+04 → 1.08e+03 | 51.9 → 5.4 | 7.97e+04 → 7.65e+05 | 1.3e+04 → **1.25e+05** | – → – |
| E500 0.85 | 0.1042 | 0.572 | 0.0596 | 1.05e+04 → 1.09e+03 | 262 → 27.3 | 9.28e+04 → 8.9e+05 | 1.52e+04 → **1.46e+05** | – → – |
| E500 1 | 0.1042 | 0.572 | 0.0596 | 1.05e+04 → 1.09e+03 | 420 → 43.7 | 5.66e+04 → 5.43e+05 | 9.26e+03 → **8.89e+04** | – → – |
| E500 1.5 | 0.1042 | 0.570 | 0.0594 | 1.05e+04 → 1.09e+03 | 732 → 76.2 | 1.74e+04 → 1.67e+05 | 2.85e+03 → **2.74e+04** | 3.06e+04 → 2.93e+05 |
| E500 2 | 0.1042 | 0.567 | 0.0590 | 1.04e+04 → 1.08e+03 | 831 → 86.6 | 1.17e+04 → 1.13e+05 | 1.92e+03 → **1.84e+04** | 2.96e+04 → 2.84e+05 |
| E500 3 | 0.1042 | 0.571 | 0.0595 | 1.05e+04 → 1.09e+03 | 575 → 59.9 | 8.44e+03 → 8.11e+04 | 1.38e+03 → **1.33e+04** | 2.65e+04 → 2.54e+05 |
| E500 5 | 0.1042 | 0.571 | 0.0595 | 1.05e+04 → 1.09e+03 | 837 → 87.2 | 2.22e+04 → 2.13e+05 | 3.64e+03 → **3.49e+04** | 6.58e+04 → 6.31e+05 |
| E1000 0.45 | 0.1459 | 0.648 | 0.0944 | 382 → 55.7 | 0 → 0 | – → – | – → **–** | – → – |
| E1000 0.6 | 0.1459 | 0.649 | 0.0946 | 383 → 55.9 | 4.26 → 0.621 | 5.84e+04 → 4.01e+05 | 2.97e+05 → **2.04e+06** | – → – |
| E1000 0.85 | 0.1459 | 0.639 | 0.0932 | 377 → 55 | 7.54 → 1.1 | 1.01e+05 → 6.95e+05 | 5.15e+05 → **3.53e+06** | – → – |
| E1000 1 | 0.1459 | 0.641 | 0.0935 | 378 → 55.2 | 8.41 → 1.23 | 8.34e+04 → 5.72e+05 | 4.24e+05 → **2.91e+06** | – → – |
| E1000 1.5 | 0.1459 | 0.643 | 0.0937 | 379 → 55.3 | 11.4 → 1.66 | 3.83e+04 → 2.63e+05 | 1.95e+05 → **1.34e+06** | – → – |
| E1000 2 | 0.1459 | 0.646 | 0.0942 | 381 → 55.6 | 22.1 → 3.22 | 2.06e+04 → 1.41e+05 | 1.05e+05 → **7.19e+05** | 1.35e+06 → 9.22e+06 |
| E1000 3 | 0.1459 | 0.643 | 0.0938 | 380 → 55.4 | 20 → 2.91 | 1.08e+04 → 7.43e+04 | 5.51e+04 → **3.78e+05** | 7.66e+05 → 5.25e+06 |
| E1000 5 | 0.1459 | 0.642 | 0.0936 | 379 → 55.2 | 23.3 → 3.4 | 3.31e+04 → 2.27e+05 | 1.68e+05 → **1.15e+06** | – → – |
| E1500 0.45 | 0.1688 | 0.579 | 0.0978 | 25 → 4.21 | 0 → 0 | – → – | – → **–** | – → – |
| E1500 0.6 | 0.1688 | 0.582 | 0.0982 | 25.1 → 4.23 | 0 → 0 | – → – | – → **–** | – → – |
| E1500 0.85 | 0.1688 | 0.581 | 0.0981 | 25 → 4.22 | 0.125 → 0.0211 | 1.45e+05 → 8.59e+05 | 1.01e+07 → **5.99e+07** | – → – |
| E1500 1 | 0.1688 | 0.583 | 0.0985 | 25.1 → 4.24 | 0.267 → 0.0451 | 6.79e+04 → 4.02e+05 | 4.73e+06 → **2.8e+07** | – → – |
| E1500 1.5 | 0.1688 | 0.582 | 0.0983 | 25.1 → 4.23 | 0.752 → 0.127 | 4.41e+04 → 2.62e+05 | 3.08e+06 → **1.82e+07** | 3.66e+07 → 2.17e+08 |
| E1500 2 | 0.1688 | 0.581 | 0.0980 | 25 → 4.22 | 0.875 → 0.148 | 3.82e+04 → 2.26e+05 | 2.66e+06 → **1.58e+07** | 3.55e+07 → 2.1e+08 |
| E1500 3 | 0.1688 | 0.579 | 0.0978 | 25 → 4.21 | 1.75 → 0.295 | 9.28e+03 → 5.5e+04 | 6.46e+05 → **3.83e+06** | 8.74e+06 → 5.18e+07 |
| E1500 5 | 0.1688 | 0.583 | 0.0983 | 25.1 → 4.23 | 1.51 → 0.254 | 3.36e+04 → 1.99e+05 | 2.34e+06 → **1.39e+07** | 4.1e+07 → 2.43e+08 |
| Ẽ500 0.45 | 0.1135 | 0.545 | 0.0619 | 749 → 85 | 0 → 0 | – → – | – → **–** | – → – |
| Ẽ500 0.6 | 0.1135 | 0.551 | 0.0626 | 758 → 86 | 0 → 0 | – → – | – → **–** | – → – |
| Ẽ500 0.85 | 0.1135 | 0.552 | 0.0626 | 758 → 86 | 0 → 0 | – → – | – → **–** | – → – |
| Ẽ500 1 | 0.1135 | 0.551 | 0.0625 | 757 → 85.9 | 8.05 → 0.914 | 3.85e+04 → 3.39e+05 | 8.4e+04 → **7.4e+05** | – → – |
| Ẽ500 1.5 | 0.1135 | 0.548 | 0.0622 | 752 → 85.4 | 18.8 → 2.13 | 8.79e+04 → 7.75e+05 | 1.92e+05 → **1.69e+06** | – → – |
| Ẽ500 2 | 0.1135 | 0.548 | 0.0622 | 753 → 85.4 | 41.4 → 4.7 | 2.56e+04 → 2.26e+05 | 5.59e+04 → **4.93e+05** | 7.17e+05 → 6.32e+06 |
| Ẽ500 3 | 0.1135 | 0.550 | 0.0624 | 755 → 85.7 | 58.4 → 6.63 | 1.44e+04 → 1.27e+05 | 3.15e+04 → **2.77e+05** | 4.88e+05 → 4.3e+06 |
| Ẽ500 5 | 0.1135 | 0.553 | 0.0627 | 760 → 86.2 | 60.8 → 6.9 | 2.1e+04 → 1.85e+05 | 4.59e+04 → **4.04e+05** | 9.82e+05 → 8.66e+06 |
