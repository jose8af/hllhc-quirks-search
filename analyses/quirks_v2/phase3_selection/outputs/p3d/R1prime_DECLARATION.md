# Reading R1′ of "workspaces built from v1 counts" (T1-c (iii)–(v), (iv)) — declaration before any R1′ toy

p3-d, executor Gorm. Written 2026-11-24 16:01 -0500 (`date`). Basis: the advisor ruling
`phase3_selection/review/advisor/ADVISOR_T1C_tuva_2026-11-24_15-57.md` (points 2–4), adopted by the orchestrator. The
binding T1-c text (STR l.1732-1745, COM l.210) is not changed. No R1′ toy, fit, coverage or limit had been run or
looked at when this file was written. Only the predictive Monte Carlo of R3, a background-only quantity, has been
computed. No reading is chosen by a coverage or a limit.

## 1. Status of R1 (as run)
R1 as run is **NOT EVALUABLE**: 15 of 80 toys dropped at 5,540 s per 1000+1000 unit, after three remediations of the
fit guard (session log 15:05). It is reported beside R1′. **No limit exists on either reading yet**: R1 gave CLs = 0
at μ = 300 and μ = 800, unresolved.

## 2. R1′
R1′ = R1 (session log P0 R1) with **every v1 estimator output above its cap set to no credit**:
- STR l.463: not submitted means no credit.
- STR l.1565: a no-credit factor is "fixed at its no-credit value (… a direct bound treated as 'counted')".
- STR l.1585-1588: the pile-up estimate is bounded by its no-credit value, the direct zero-count bound.
- STR l.1653: label "no credit".
- Caps: 0.231 at STR l.847, 0.135 at STR l.1165, §4.0 point 4 (c).

**v1 estimator outputs in R1 and their caps.**
- **Pile-up term (v1 thinning, all three PU terms).**
  - Its closure ln r at R04–R07 is +0.406, +0.474, −0.455, −0.954 (v1 `background.json` → `closure.trend.points`),
    so its r.m.s. is 0.61. That is above the pile-up cap of 0.135 (STR l.1165; F = 1.5). STR l.432-434 states that it
    "would not have been submitted".
  - The v1 log widths carried in R1 at FB2: SR-G stat 0.633, model spread 0.455, closure 0.474, trend 5.230,
    density 1.151 (`background.json` l.12186-12191). SR-T stat 1.105, trend 5.230 (l.13676-13680).
  - **→ no credit.**
- **SM proxies** (Wenu_j, Wmunu_j, ttbar_2l, top_t, WW, WZ, ZZ, top_tW; widths 1.04–1.28).
  - These are v1-proxy rates. They have no s_model, no closure test and, in v1, **no usable direct bound** (no
    sample of these processes exists).
  - They keep their R1 treatment (nominal with its v1 log width) and carry the label "no credit (proxy)" in the
    tables.
  - Flag: STR offers no counted no-credit value for them.
- Counted factors with pass fraction ≥ 0.1 (combined per term, binomial width, censored at 1): these are counted, not
  estimators. Unchanged.

**No-credit values of the pile-up terms (v1 direct counts, ρ = 1 direct sample).**
- M_direct = 48,000 trials: `background.json` l.17, `samples.B1_trials`.
- N_trig = 4.0848×10⁷: `bsum_wp.json` → `n_trig.value`.
- That gives **851.0 events per unit λ**.

| term | direct count m (file:line) | no-credit term | 68 % value |
|---|---|---|---|
| PU_G (SR-G) | 9 of 48,000 (`background.json` l.2632-2633, `columns[FB2].B1_groups`) | 851.0 × λ_G, λ_G ~ Gamma(10) | 851 × 11.2 ≈ 9.5×10³ [E: Gamma(10) 68 % quantile ≈ 11.2] |
| PU_T_late (SR-T, BTL present) | 0 of 48,000 (`background.json` l.8179-8180, `columns_T[FB2].B1_groups`) | 851.0 × λ_T, λ_T ~ Gamma(1); time-tag fraction 0/23 enters at 1 (one zero per term) | 970 |
| PU_T_oot (SR-T, not present) | λ_G (shared count) × time-tag fraction 0/39 (counted, `srt.json` columns FB2 P_oot) | 21.8 × λ_G × λ_oot | — |

The N_trig normalisation width (ln 1.3, shared `normalisation`) and the time-tag widths `srt_pv` 0.412 and `srt_sigt`
0.025 stay. No v1 pile-up estimator width enters R1′. The F1 conditional h>5&o>5 at FB2 is 46/46, i.e. 1.
Implementation: `p3d_model.v1count(..., reading='R1p')` (`_pileup_nocredit`), specs `v1countp_p1` and `v1countp_p2`.
R1′ has 47 parameters, 24 counted factors and 23 terms.

## 3. Unchanged from the session log P0 (14:32)
- **R2** points: A2|F|200|1.5|BM (v1 best point) and A2|F|500|2|BM. Signal = v1 placeholder efficiency × 15,775.
- **R3** leading zero-count term, computed before any toy (predictive Monte Carlo, 10⁵ draws, seed 1,
  `debug_insp.py v1countp_p1`): **CP_pvpair** (as in R1).
  - Predictive B50 / B84 = 2.15×10⁵ / 5.08×10⁵ (SR-T) and 2.23×10⁵ / 5.16×10⁵ (SR-G).
  - Total σ_ln 0.80 / 0.77; f₀ = 0.87; PU_G B50 8.2×10³.
- **R4** (A) other counted rates at m + 1, nuisances drawn; (B) the same with nuisances at 0.
- **R5** c_ref from the exact one-bin sums (a) without and (b) with the rest of the background as a fixed rate;
  ≤ 0.95.
- **R6** (a) inverse ECDF, (b) numpy.median.
- **R7** censoring off at the model's μ_true.
- **R8** alternatives (ii) fixed 1.139 and (iii) Jeffreys.
- **Stored μ grid** = μ_true × {0.4, 0.55, 0.75, 0.9, 1.0, 1.35, 1.8}, and also {2.5, 3.5, 5} at m′ = 0. m′ = every
  value drawn.
- **Seeds**: limits 2026112403 (point 1) and 2026112404 (point 2); stored distributions 2026112410 + 1000 m′;
  coverage 2026112420.
- **Recipe**: `PREREG_toy_recipe_draft.md` as of this declaration (sha256 in the session log); the static fit bounds
  as built.

## 4. Feasibility probe (advisor point 3) and its criterion, fixed now
Two approaches, each on R1 and R1′, 40 + 40 toys at two μ. The μ values are 0.5 μ_a and μ_a, where μ_a is the
Asimov limit of that workspace (or of R1′ for R1, where R1's own Asimov fit fails).
- **(A)** R1′ with the present fit guard (draft §2).
- **(B)** conditioning: the counted rates rescaled to λ′ = λ/(m + 1) and μ rescaled to O(1) by the workspace's
  μ_scale. This is the same likelihood (reparametrisation only).
  - Flora's exact-profile fitter is not applicable here: it exists only for the collapsed two-bin v1 mode, with
    one-dimensional profiles.
  - A logarithmic parametrisation of a normfactor is not expressible in pyhf without adding a constraint, so it is
    not used.
- **Feasible** = both of:
  - at most 2 % dropped (draft recipe §2) at both μ;
  - three different starts (generated values, default, previous toy) agree in twice-NLL within 10⁻³ for both fits
    on 20 toys.
- **Cap**: 5 CPU-h for the probes. T1-c (iii)–(v) are launched only if the projection with the measured unit cost is
  ≤ 45 CPU-h. If both approaches fail, the stop rule of the brief applies (l.345) and a DECISION goes to the user.
