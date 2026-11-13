# INV_NORM_F200: is f = P(pT(QQ̄) > 200 GeV) missing from the Stage-4 N_exp?

Verifier (investigator role, adversarial), 2026-10-16. Read-only on the analysis. Script:
`acts/stage4/investigation/inv_norm_f200.py`. Output: `data/acts_stage4/investigation/inv_norm_f200.json`.

**Verdict: CONFIRMED.** N_exp leaves out the tail fraction f. Every μ₉₅/N_exp, σ₉₅/σ_th, S and μ_5σ/N_exp is too optimistic by
1/f = 5.9–21×. The best ratio moves from 37.6 to **790** (E200, 1.5 keV, still the best point; VERIFIED arithmetic).

## 1. Code path (VERIFIED by reading the code)
| step | file:line | what it does |
|---|---|---|
| N_exp | `acts/stage4/results/make_stage4_summary.py:145-146` | `A = acc[...]['A_trig_presel']; n_exp = SN[sp m] * L_FB * A` |
| σ_norm | same file `:47-52` | `sim/results/xsec.json` `normalisation_E.rows[m].sigma_norm_nic2_fb`; Ẽ uses `normalisation_S`. E200 = 219.2 fb = **inclusive** DY, N_IC = 2, LO×K. |
| σ₉₅, ratio | same file `:165-167` | `sigma95_fb = mu/(L_FB*A)`, `S_at_rfb = n_exp*eps`, `mu95_over_nexp = mu/n_exp` |
| A | `acts/stage4/analysis/products.py:53,57` | `A = Σ w·F·trig·presel / Σ w` over the Stage-3 p2 template half. This is a **ratio within the Stage-3 sample**, and every event carries the same weight w = w_max. |
| Stage-3 population | `sim/stage3/code/make_inputs.py:42,93-94` and `meta_json.selection` of `out/p2/F_m200/L1.5_BM_c00.npz` | `sample: trig (TRGS)`, `ptmin: 200.0`, `eta_max: 4.0`, w > 0, hit-or-miss unweighted |
| Stage 5 | `stage5/make_figures.py:245-255` (n_exp), `:556` (`f = 1/(LUMI_FB*A)` → σ₉₅ on the D6 y-axis "σ(pp→QQ̄)", compared with inclusive σ_th from `theory_E()` `:205-211`) | same formula. It cross-checks against `N_exp_3ab` at 1e-6, so it reproduces the error and cannot catch it. |

A's denominator is therefore the pT(QQ̄) > 200 GeV, |η_pair| < 4 population, while σ_norm is inclusive. The two do not
refer to the same population.

## 2. Is f included somewhere else? (attempts to refute; all fail)
- **σ_norm** is not a tail cross section. `xsec.json` stores the tail separately as `trigger_yields_E.rows[m].sigma_norm_pt200_nic2_fb`
  (E200: 10.44 fb vs 219.2). `make_stage4_summary.py` reads only `sigma_norm_nic2_fb`. VERIFIED.
- **A** is not per generated event. It is normalised to Σw of the Stage-3 template events, and those events all have pT > 200.
  Its factors (`fiducial_eta25` 0.847, `trigger` 0.903, `preselection_given_trigger` 0.658 at E200 1.5 keV) multiply to
  0.5035, with no tail factor among them. VERIFIED (`acceptance.json`).
- **The weights** cannot carry f. Stage-3 `w = w_max` is the same for every event (0.000846 fb at E200), and A is a ratio of
  weights, so any common normalisation cancels. VERIFIED.
- **Other code**: grep for `f_pt200|trigger_yields|sigma_ref|ptmin|pt200` in `acts/stage4/analysis/*.py` and
  `acts/stage4/results/*.py` finds no hits. VERIFIED.
- **The μ units** are not the issue. `run_all.py:139-143` defines μ as the "number of signal events in the trigger +
  preselection acceptance in 3 ab⁻¹ (Stage 5 divides by σ × L × A)", and s = ε_finder per bin. So μ95 is right as an absolute
  count, and only the predicted count N_exp is wrong.
- **What the project's own conventions say.** `sim/SAMPLES.md:3` and `sim/scripts/mg_events.py:152` define
  "Yield = 3000 fb⁻¹ × sigma_norm_fb × Σw_sel / sigma_ref_fb", and the npz files store `sigma_ref_fb`. The implementation
  drops the Σw_sel/σ_ref factor. `acts/stage4/plan.md:1050` ("N = σ_norm × L × ε ... on the unweighted Stage-3 events, with
  w_max per event") leaves this ambiguous: its ε chain (`:1049`) also has no tail factor. The **Stage-5 fallback**
  (`make_figures.py:220-232`) uses the inclusive-normalised `f_pt200_eta25_TRG_over_INC` as A when `acceptance.json` is
  absent. The two branches therefore define A differently, which confirms that the intended A includes f.

## 3. Numbers
### 3.1 Reproduction (VERIFIED)
N_exp(E200, 1.5 keV) = 219.2028 × 3000 × 0.503546 = 3.3114 × 10⁵. This equals `STAGE4_SUMMARY.json` `N_exp_3ab` exactly, and
the maximum relative difference over all 40 points is 0. μ95 (toys) = 1.2458 × 10⁷ from `limits.json` gives μ95/N_exp = 37.62,
as published.

### 3.2 Tail fraction f per mass point (VERIFIED, computed from the TRGS files)
f_p2 = Σw(TRGS, pT(QQ̄) > 200, |η_pair| < 4) / σ_ref, where σ_ref is the INC σ_matched from the npz `sigma_ref_fb`. This is the
`mg_events.sigma_norm_fb` convention, applied to the exact Stage-3 population.

| point | file | f_p2 (used) | hit-or-miss × w_max | no η cut | \|η\|<2.5 | xsec.json `f_pt200_TRG_over_INC` | correction ×1/f |
|---|---|---|---|---|---|---|---|
| E200 | E-TRGS_m200 | **0.04764** | 0.04781 | 0.04764 | 0.04127 | 0.04764 | **21.0** |
| E500 | E-TRGS_m500 | **0.10418** | 0.10468 | 0.10418 | 0.08529 | 0.10418 | **9.60** |
| E1000 | E-TRGS_m1000 | **0.14585** | 0.14628 | 0.14585 | 0.11397 | 0.14585 | **6.86** |
| E1500 | E-TRGS_m1500 | **0.16874** | 0.17044 | 0.16876 | 0.12913 | 0.16876 | **5.93** |
| Ẽ500 | S-TRGS_m500 | **0.11350** | 0.11564 | 0.11350 | 0.09187 | (none) | **8.81** |

Notes:
- No weights are negative. The |η| < 4 cut removes < 0.02 % of the tail.
- The audit's 0.0485 for E200 is `f_pt200_INC`, which uses the INC-only numerator and has 3× the statistical error. The
  TRGS value 0.0476 is the one that matches the Stage-3 rows.
- Stage-3 `sigma_norm_fb` in the npz equals the xsec.json value at all 5 points.

### 3.3 Corrected ratios (VERIFIED arithmetic; μ95 unchanged)
| point | μ95/N_exp published | corrected |
|---|---|---|
| E200 1.5 keV (best, before and after) | 37.6 | **790** |
| E200 2 keV | 39.1 | 820 |
| E200 1 keV | 109 | 2.29 × 10³ |
| E200 3 keV | 133 | 2.80 × 10³ |

All 40 points are in `inv_norm_f200.json` (`ratio_corr`). The best point stays the same because 1/f grows with falling mass
less steeply than μ95/N_exp grows with mass.

N_exp_corr(E200, 1.5 keV) = 3.311 × 10⁵ × 0.04764 = **1.578 × 10⁴** (VERIFIED). The audit's ≈ 780 used f = 0.0485. 790 is
the value at the exact Stage-3 population. ESTIMATE-level difference, 2 %.

### 3.4 The reviewer's N_200 vs N_exp observation (VERIFIED)
`xsec.json trigger_yields_E.rows.200.N_3iab_pt200_eta25` = 2.71 × 10⁴ events (pT > 200, |η| < 2.5, no trigger or
preselection). The published N_exp = 3.31 × 10⁵ is 12× larger, even though it adds trigger and preselection cuts (≤ 1). That
is impossible, so the published value is inconsistent with the project's own numbers.

After the correction, N_exp_corr / N_200,η<2.5 = 1.578e4 / 2.714e4 = 0.581. Compare A/ε_fid = 0.5035/0.8475 = 0.594, which is
ε_trig × ε_presel|trig. The two agree to 2 %, and the gap is consistent with the template statistics (236 events). The
correction makes the chain consistent.

## 4. Downstream impact
All of the following scale by f, or their ratios by 1/f:
- `STAGE4_SUMMARY.json`:
  - `fallback_points[*]`: `N_exp_3ab`, `S_at_rfb`, `sigma95_fb`, `mu95_over_Nexp`;
  - `outcome.best_mu95_over_Nexp` (37.6 → 790);
  - the matching `signal[*].limit` entries in `headline_C12FC_v1.json`, `tables_C12FC_v1.md`, `STAGE4_RESULTS*.md` §0/§4.4/§5,
    and `STAGE4_SUMMARY_C12v1.json` (same formula).
- **σ₉₅** (`sigma95_fb = μ/(L·A)`) is numerically a valid 95 % limit on σ(pT > 200, |η| < 4), but it is labelled and plotted
  as a limit on σ(pp→QQ̄). Against the inclusive σ_th it is too optimistic by 1/f.
- **Stage 5**:
  - D6 (`D6_limit_xsec_vs_m_L*.json` `sigma95_over_sigma_th`; E200 1.5 keV 37.6 → 790, E500 2852 → 2.74 × 10⁴, E1000
    1.95 × 10⁵ → 1.34 × 10⁶, E1500 3.08 × 10⁶ → 1.82 × 10⁷);
  - D7 (`min_sigma95_over_sigma_th` 37.6 → 790);
  - the σ-scaled μ_5σ in D6.
- **Discovery**:
  - `mu_5sigma` and `mu_3events` are absolute event counts and are unchanged, as are the expected ±1σ/±2σ bands of μ.
  - Every comparison with N_exp gets 1/f worse: μ_5σ/N_exp at the 16 points where it is non-null, and S = N_exp·ε (E200
    1.5 keV: 1.49 × 10⁴ → 710).
  - The qualitative outcome ("no expected exclusion or discovery at any point") does not change, but the distance from
    exclusion grows by 6–21×.
- **Unaffected**: background B, the WP/ladder, ε_finder, μ95 and its bands, `limits.json` itself (in event units), and
  `acceptance.json` (correct as a conditional acceptance).
- The audit's break-even numbers (`P2_NOVELTY_AUDIT.md` §2.0) carry over with f = 0.0476 instead of 0.0485 (−2 %).

## 5. Correct formula and minimal fix (not applied)
N_exp = σ_norm(N_IC = 2) × f_p2(m, spin) × L × A, with f_p2 = Σw_TRGS(pT > 200, |η_pair| < 4) / σ_ref.

Equivalently: N_exp = L × `mg_events.sigma_norm_fb(m, 'trig', spin, ptmin=200, eta_max=4)` × A. Then σ₉₅(inclusive) =
μ / (L × f_p2 × A).

Minimal patch, three places:
1. `make_stage4_summary.py`
   - `sigma_norm_fb()` (`:47-52`): return σ_norm × f_p2 per point, with f_p2 computed as in `inv_norm_f200.py`. For E, read
     `xsec.json trigger_yields_E.rows[m].f_pt200_TRG_over_INC`, which equals f_p2 to < 2e-4 relative. Ẽ500 needs f = 0.11350,
     because xsec.json has no S row.
   - Or multiply at `:146`: `n_exp = SN * F_TAIL * L_FB * A`, and use `L_FB * A * F_TAIL` at `:165`.
   - Re-tag `sigma_norm_fb` / `N_exp_3ab`.
2. `stage5/make_figures.py`
   - In `acceptance()` (`:226-227`), return `A_trig_presel × f_p2` for the acceptance.json branch. This fixes `n_exp` (`:252`)
     and the D6 σ₉₅ (`:556`) together, and makes it consistent with the fallback branch, which already uses an
     inclusive-normalised f.
3. Optional, cleanest: in `products.acceptance_point` (`products.py:57`), add `f_tail` and `A_incl = A × f_tail` as new keys
   in `acceptance.json`, so that consumers cannot mix populations. The analysis is frozen, so a product-level addition plus
   (1)+(2) is the smaller change.
4. Regenerate STAGE4_SUMMARY, the tables, the D6/D7 figures and the paper numbers. No Stage-4 re-run is needed: μ95, B and ε
   are unchanged. Carry the tail-rate nuisance (+12…+15 / −11…−13 %, `sim/stage3/plan.md:431`) on f.
