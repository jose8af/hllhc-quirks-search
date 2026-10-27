# U-2 (a): measured B + multiple-scattering combination panel for P1 (truth level)

Executor, 2026-10-13. Task: Stage-4 plan §9 (`acts/stage4/plan.md`); user decision U-2 (a) (`LOG.md`).
Script: `acts/stage4/u2_panel/make_u2_panel.py`. Run from `theory_track/` with
`pixi run python acts/stage4/u2_panel/make_u2_panel.py` (about 7 s, under 0.01 CPU-h). Every plotted number is in
`acts/stage4/u2_panel/u2_panel.json`.

## 1. What is plotted

The observable is the P1 plane thickness Δs. It is the thickness on the 10 virtual T3 barrel layers of the plane through
the vertex (`ds_barrel_um`, the Stage-1 definition). The sample is the Stage-3 P1 production: |η_pair| < 1, vertex at the
origin, truth level, 300 events per cell (200 at 7 and 10 keV). Three Stage-3 configurations run on the **same generated
events**:
- B: solenoid field, no material.
- M: material, no field (MS only).
- BM: field and material.

Selection, as in `sim/stage3/scripts/p1_results.py`: status = 1 and a finite Δs > 0 in each configuration. Paired ratios
use only the rows that are valid in all three. Errors are the bootstrap of the median (1000 resamples, seed 12345, the
`p1_results.py` recipe) and are statistical only.

- **Thickness panels** (`fig/u2_thickness_<point>`, one per species-mass):
  - Main panel: median Δs_B, Δs_MS and Δs_BM vs Λ. Two reference curves built from the measured medians are overlaid:
    the quadrature sum √(Δs̃_B² + Δs̃_MS²) (dashed) and the linear sum Δs̃_B + Δs̃_MS (dotted). Here Δs̃ is the median.
  - Ratio panel: the per-event paired median r_q = Δs_BM/√(Δs_B² + Δs_MS²) with its bootstrap error. The line at 1
    marks quadrature. The dotted line is median[(Δs_B + Δs_MS)/√(Δs_B² + Δs_MS²)], the value r_q would take if B and MS
    added linearly event by event.
  - The dash-dot line is Λ_cross.
  - Above 5 keV, the B-only error bars include the unattributed ±5 % (P-9) in quadrature. Its effect on r_q there is
    ≤ 0.02 %, because Δs_B ≪ Δs_MS.
- **Ratio vs x** (`fig/u2_ratio_vs_x`): r_q for all 34 cells vs x = median per-event Δs_B/Δs_MS. The references are 1
  (quadrature) and the single-event linear-sum identity (1 + x)/√(1 + x²), which peaks at √2 when x = 1.
- **Ratio vs Λ/Λ_cross** (`fig/u2_ratio_vs_lamcross`): the same 34 r_q values vs Λ/Λ_cross. Λ_cross is the B = MS
  crossover from `P1.json` `B_MS_crossover_keV`, the log-log interpolation where the median Δs_B equals the median Δs_MS.

**Figure label.** The label is the user-approved one: "Private work (simulation)" top left, "truth level" as an
in-figure tag, and "√s = 14 TeV, PU 200, 3 ab⁻¹" top right. There is no experiment name or logo. The right-hand label is
the project label, not a property of these figures: **PU is not simulated at truth level** and nothing is normalised to
3 ab⁻¹. The captions say this.

**Plot-helper deviation.** `code/plotting.py` does not exist in theory_track, and mplhep is not installed in the
theory_track pixi env. The only existing helper is `sim/stage3/scripts/s3common.fig_label`, a one-line `ax.text`
label. The script therefore sets a CMS-like stylesheet through rcParams and draws the label with a small
`exp_label()` that places text the way `mplhep.label.exp_label(loc=0)` does. These three label/tag `ax.text` calls are
the only text calls. All other JFC rules hold: figsize 10×10, ratio panels 3:1 with `sharex` and `hspace=0`, no title,
no numeric font sizes, PDF + PNG at dpi 200. No pixi environment was changed.

## 2. Traceability check (VERIFIED)

The script recomputes every median and error from `data/sim_stage3/summary/events_p1.npz` and compares them with
`sim/stage3/results/P1.json`:
- `points.<sp>.by_lambda.<Λ>.Ds_B/Ds_MS/Ds_BM`;
- `B_MS_combination.median_BM_over_quadrature`, `err` and `median_BM_over_linear`.

The maximum difference is **0** for every quantity (`u2_panel.json` → `check_vs_P1json`). There are 34 cells with B, M
and BM, as stated in plan §9.

## 3. Key numbers

The r_q values below are VERIFIED: measured on the Stage-3 production and reproduced exactly from P1.json.

| Λ band | cells | r_q range | reading |
|---|---|---|---|
| 0.45 keV (Λ/Λ_cross 0.24-0.39) | 5 | 0.989-1.005 (± 0.003-0.008) | quadrature |
| 0.6 keV (0.31-0.52) | 5 | 0.950-0.998 (± 0.007-0.015) | at or slightly below quadrature; E 500 0.964 ± 0.012 (−3.0σ), E 1500 0.950 ± 0.015 (−3.3σ) |
| 1-3 keV (0.52-2.6) | 15 | **0.804-0.972** (± 0.02-0.06) | **sub-quadrature** |
| 5-10 keV (2.6-8.6) | 9 | 0.895-1.095 (± 0.05-0.12) | consistent with quadrature: all within 2σ (largest E 200 at 5 keV, 0.895 ± 0.053, −1.97σ) |

- The deepest cell is E 200 at 3 keV: r_q = 0.804 ± 0.042 (−4.7σ from 1). E 500 at 2 keV gives 0.810 ± 0.043 (−4.4σ).
  The cells more than 3σ below quadrature are E 200/3 keV, E 500/2 keV, E 500/0.6 keV and E 1500/0.6 keV. No cell is
  more than 2σ above it.
- In every species-mass the deficit is largest at **Λ/Λ_cross = 1.25-1.73**, where the median per-event x is
  0.29-0.50. The deficit is not at x = 1. Because the per-event Δs_B distribution is broad, the median of x is not the
  ratio of the medians.
- For comparison, the linear-sum expectation for r_q is 1.13-1.34 in the 1-3 keV cells: the dotted ratio-panel lines, with
  values in `u2_panel.json`. The measured ratio to the linear sum, r_l, is 0.62-1.00. B and MS **never add linearly**.
  At the crossover they add **below quadrature**, typically by 5-20 %.
- Λ_cross: 1.91 / 1.50 / 1.25 / 1.16 keV for E 200/500/1000/1500 GeV and 1.59 keV for Ẽ 500 GeV. These come from
  P1.json and are VERIFIED as a measurement. The interpolation between grid points is log-log. The MS floor Δs_MS is
  10-28 µm and nearly flat in Λ.
- **Correlations.** The cells of one species-mass share the same generated events across Λ, and the B, M and BM
  configurations share rows. The per-cell errors are therefore not independent across Λ. No average, fit or combination
  rule is derived here.

### Per-cell table (from `u2_panel.json`; errors are bootstrap, statistical)

Δs_B is "not in P1 grid" where the Stage-3 P1 grid has no B-only run: E 200, E 1500 and Ẽ 500 at 7 and 10 keV. The
floor flag is given where the fraction of B-only events at the double-precision floor is ≥ 0.10. All such fractions are
below the 0.5 withholding rule of P1.json.

| Point | Λ [keV] | Λ/Λ_cross | Δs_B [µm] | Δs_MS [µm] | Δs_BM [µm] | n | x = Δs_B/Δs_MS | r_q = Δs_BM/√(Δs_B²+Δs_MS²) | pull vs 1 | r_l = Δs_BM/(Δs_B+Δs_MS) |
|---|---|---|---|---|---|---|---|---|---|---|
| E 200 | 0.45 | 0.24 | 137 ± 8 | 9.62 ± 0.69 | 140 ± 9 | 300 | 12.5 ± 0.93 | 1.004 ± 0.004 | +1.1 | 0.939 ± 0.008 |
| E 200 | 0.6 | 0.31 | 78.4 ± 4.5 | 10.4 ± 0.9 | 78.3 ± 3.2 | 300 | 6.43 ± 0.55 | 0.998 ± 0.007 | -0.3 | 0.888 ± 0.019 |
| E 200 | 1 | 0.52 | 31.1 ± 1.8 | 9.85 ± 0.60 | 33.3 ± 2.4 | 300 | 2.66 ± 0.18 | 0.972 ± 0.022 | -1.3 | 0.795 ± 0.023 |
| E 200 | 2 | 1.04 | 9.32 ± 0.61 | 10.1 ± 0.6 | 13.0 ± 1.2 | 300 | 0.811 ± 0.053 | 0.939 ± 0.058 | -1.1 | 0.721 ± 0.040 |
| E 200 | 3 | 1.57 | 4.28 ± 0.28 | 11.2 ± 0.9 | 10.2 ± 0.6 | 300 | 0.324 ± 0.028 | 0.804 ± 0.042 | -4.7 | 0.635 ± 0.043 |
| E 200 | 5 | 2.61 | 1.64 ± 0.09 | 11.3 ± 0.6 | 10.2 ± 0.6 | 300 | 0.127 ± 0.014 | 0.895 ± 0.053 | -2.0 | 0.769 ± 0.052 |
| E 200 | 7 | 3.66 | not in P1 grid | 10.4 ± 1.1 | 10.6 ± 0.8 | – | – | – | – | – |
| E 200 | 10 | 5.22 | not in P1 grid | 10.6 ± 1.0 | 9.95 ± 0.64 | – | – | – | – | – |
| E 500 | 0.45 | 0.30 | 132 ± 8 | 13.3 ± 0.9 | 132 ± 8 | 300 | 8.79 ± 0.81 | 1.005 ± 0.005 | +1.0 | 0.925 ± 0.010 |
| E 500 | 0.6 | 0.40 | 77.2 ± 3.6 | 13.2 ± 0.9 | 75.1 ± 5.1 | 300 | 5.44 ± 0.49 | 0.964 ± 0.012 | -3.0 | 0.855 ± 0.018 |
| E 500 | 1 | 0.67 | 29.5 ± 1.6 | 13.2 ± 1.1 | 33.2 ± 1.4 | 299 | 1.8 ± 0.17 | 0.938 ± 0.023 | -2.7 | 0.740 ± 0.023 |
| E 500 | 2 | 1.34 | 8.77 ± 0.51 | 15.6 ± 1.2 | 16.0 ± 0.9 | 299 | 0.47 ± 0.049 | 0.810 ± 0.043 | -4.4 | 0.623 ± 0.035 |
| E 500 | 3 | 2.00 | 3.99 ± 0.20 | 14.3 ± 1.5 | 13.6 ± 0.8 | 299 | 0.252 ± 0.024 | 0.885 ± 0.062 | -1.9 | 0.726 ± 0.051 |
| E 500 | 5 | 3.34 | 1.56 ± 0.08 | 15.5 ± 1.0 | 15.2 ± 1.3 | 299 | 0.0935 ± 0.006 | 0.995 ± 0.064 | -0.1 | 0.882 ± 0.058 |
| E 500 | 7 | 4.67 | 0.910 ± 0.069 (+5 % syst) | 14.9 ± 1.5 | 15.4 ± 1.6 | 199 | 0.0514 ± 0.0072 | 0.981 ± 0.122 | -0.2 | 0.932 ± 0.084 |
| E 500 | 10 | 6.68 | 0.482 ± 0.040 (+5 % syst) [floor-flag 0.17] | 12.8 ± 1.2 | 12.2 ± 0.9 | 199 | 0.0324 ± 0.0025 | 0.946 ± 0.077 | -0.7 | 0.922 ± 0.071 |
| E 1000 | 0.45 | 0.36 | 131 ± 7 | 17.8 ± 1.4 | 141 ± 6 | 300 | 7.06 ± 0.75 | 0.994 ± 0.008 | -0.7 | 0.895 ± 0.013 |
| E 1000 | 0.6 | 0.48 | 75.6 ± 3.9 | 17.2 ± 1.5 | 84.3 ± 4.6 | 300 | 3.63 ± 0.28 | 0.995 ± 0.009 | -0.6 | 0.854 ± 0.019 |
| E 1000 | 1 | 0.80 | 28.7 ± 1.5 | 18.2 ± 1.2 | 38.9 ± 2.2 | 300 | 1.35 ± 0.13 | 0.951 ± 0.034 | -1.4 | 0.778 ± 0.023 |
| E 1000 | 2 | 1.60 | 8.23 ± 0.42 | 21.7 ± 1.6 | 23.4 ± 1.6 | 300 | 0.3 ± 0.034 | 0.884 ± 0.043 | -2.7 | 0.696 ± 0.044 |
| E 1000 | 3 | 2.41 | 3.91 ± 0.17 | 18.9 ± 1.5 | 21.8 ± 2.3 | 300 | 0.186 ± 0.018 | 0.954 ± 0.052 | -0.9 | 0.784 ± 0.066 |
| E 1000 | 5 | 4.01 | 1.49 ± 0.08 | 22.3 ± 1.5 | 21.2 ± 2.5 | 300 | 0.0598 ± 0.0058 | 0.928 ± 0.067 | -1.1 | 0.875 ± 0.057 |
| E 1000 | 7 | 5.62 | 0.821 ± 0.051 (+5 % syst) [floor-flag 0.17] | 19.3 ± 1.8 | 18.5 ± 2.0 | 199 | 0.0361 ± 0.0046 | 1.020 ± 0.078 | +0.3 | 0.961 ± 0.070 |
| E 1000 | 10 | 8.02 | 0.445 ± 0.032 (+5 % syst) [floor-flag 0.37] | 19.4 ± 1.8 | 18.3 ± 2.1 | 199 | 0.0251 ± 0.0032 | 0.976 ± 0.061 | -0.4 | 0.930 ± 0.062 |
| E 1500 | 0.45 | 0.39 | 136 ± 6 | 17.6 ± 1.7 | 137 ± 6 | 300 | 6.66 ± 0.79 | 0.989 ± 0.006 | -1.9 | 0.883 ± 0.013 |
| E 1500 | 0.6 | 0.52 | 78.9 ± 3.2 | 22.4 ± 1.8 | 77.1 ± 3.7 | 300 | 3.48 ± 0.28 | 0.950 ± 0.015 | -3.3 | 0.799 ± 0.026 |
| E 1500 | 1 | 0.86 | 30.4 ± 1.1 | 22.8 ± 1.5 | 38.8 ± 2.2 | 299 | 1.21 ± 0.11 | 0.929 ± 0.043 | -1.7 | 0.753 ± 0.052 |
| E 1500 | 2 | 1.73 | 8.18 ± 0.36 | 23.9 ± 2.4 | 25.3 ± 1.9 | 299 | 0.287 ± 0.02 | 0.889 ± 0.041 | -2.7 | 0.747 ± 0.031 |
| E 1500 | 3 | 2.59 | 3.95 ± 0.14 | 23.3 ± 2.7 | 24.4 ± 2.2 | 298 | 0.14 ± 0.02 | 0.969 ± 0.052 | -0.6 | 0.842 ± 0.052 |
| E 1500 | 5 | 4.32 | 1.56 ± 0.05 [floor-flag 0.10] | 24.5 ± 2.0 | 24.7 ± 2.3 | 298 | 0.0509 ± 0.0058 | 1.095 ± 0.073 | +1.3 | 1.004 ± 0.068 |
| E 1500 | 7 | 6.05 | not in P1 grid | 25.6 ± 2.7 | 24.4 ± 3.0 | – | – | – | – | – |
| E 1500 | 10 | 8.64 | not in P1 grid | 28.1 ± 2.3 | 22.3 ± 2.0 | – | – | – | – | – |
| Ẽ 500 | 0.45 | 0.28 | 162 ± 8 | 12.9 ± 0.9 | 159 ± 7 | 300 | 9.98 ± 0.96 | 0.997 ± 0.003 | -1.1 | 0.937 ± 0.011 |
| Ẽ 500 | 0.6 | 0.38 | 90.4 ± 3.9 | 11.5 ± 1.1 | 84.1 ± 3.4 | 300 | 5.64 ± 0.48 | 0.980 ± 0.010 | -2.0 | 0.876 ± 0.017 |
| Ẽ 500 | 1 | 0.63 | 33.9 ± 2.3 | 14.5 ± 1.3 | 34.2 ± 1.7 | 300 | 2.03 ± 0.16 | 0.946 ± 0.021 | -2.6 | 0.798 ± 0.027 |
| Ẽ 500 | 2 | 1.25 | 9.27 ± 0.58 | 14.0 ± 1.1 | 16.7 ± 1.1 | 300 | 0.495 ± 0.056 | 0.852 ± 0.064 | -2.3 | 0.690 ± 0.046 |
| Ẽ 500 | 3 | 1.88 | 4.44 ± 0.25 | 15.7 ± 0.9 | 15.0 ± 1.4 | 300 | 0.259 ± 0.031 | 0.922 ± 0.059 | -1.3 | 0.801 ± 0.039 |
| Ẽ 500 | 5 | 3.14 | 1.79 ± 0.12 | 14.3 ± 0.9 | 14.8 ± 0.8 | 300 | 0.103 ± 0.0097 | 1.026 ± 0.069 | +0.4 | 0.920 ± 0.050 |
| Ẽ 500 | 7 | 4.39 | not in P1 grid | 15.0 ± 1.2 | 12.9 ± 1.2 | – | – | – | – | – |
| Ẽ 500 | 10 | 6.27 | not in P1 grid | 13.6 ± 1.5 | 14.2 ± 1.4 | – | – | – | – | – |

## 4. Captions

**`fig/u2_thickness_<point>` (5 figures: E 200, E 500, E 1000, E 1500, Ẽ 500 GeV).** These panels show the median plane
thickness of quirk-pair hits on the 10 barrel layers vs the string scale Λ, at truth level. Three configurations run on
the same generated events (P1 sample, |η_pair| < 1): field only (Δs_B), material only (Δs_MS) and field plus material
(Δs_BM).
- Main panel: the dashed and dotted lines are the quadrature and linear sums of the measured medians.
- Ratio panel: the per-event median of Δs_BM/√(Δs_B² + Δs_MS²). The dotted line is the value this ratio would take if
  the two effects added linearly in every event. The dash-dot line marks the B = MS crossover Λ_cross.

Below Λ_cross the field-driven thickness dominates and the combination is at quadrature. Around 1-3 keV the measured
combination lies 3-20 % below quadrature and far below the linear sum. Well above Λ_cross the MS floor (10-28 µm)
dominates. Errors are bootstrap and statistical; above 5 keV the B-only bars include the ±5 % unattributed systematic.
Pile-up is not simulated at this truth level: the "PU 200, 3 ab⁻¹" label is the project label.

**`fig/u2_ratio_vs_x`.** This figure shows the per-event median of Δs_BM/√(Δs_B² + Δs_MS²) for all 34 P1 cells (five
species-masses × Λ = 0.45-10 keV, truth level), vs the median per-event ratio x = Δs_B/Δs_MS of the same events.
- Dashed line: quadrature.
- Dotted line: the single-event linear-sum identity (1 + x)/√(1 + x²).

The cells are within 5 % of quadrature when B dominates (x > 3). They fall to 0.80-0.90 at x ≈ 0.3-0.5 and return toward 1 when MS
dominates. B and MS add sub-quadrature, never linearly. This is a measured combination; no rule is fitted. Pile-up is not
simulated at truth level.

**`fig/u2_ratio_vs_lamcross`.** This figure shows the same 34 ratios vs Λ/Λ_cross, where Λ_cross is the measured B = MS
crossover of each species-mass (1.16-1.91 keV). When Λ is expressed in units of Λ_cross, all five species-masses follow
the same pattern:
- within 4 % of quadrature (ratio ≥ 0.96) at Λ/Λ_cross ≤ 0.5;
- a minimum of 0.80-0.89 at Λ/Λ_cross = 1.25-1.73;
- a return to quadrature within errors at Λ/Λ_cross ≳ 3.

The points of one species-mass share events across Λ, so their errors are correlated. Truth level; pile-up not simulated.

## 5. Text block for P1 (5 lines; measured combination, no fitted rule)

> B-driven and multiple-scattering thicknesses were measured separately and together on the same events (truth level).
> They do not add linearly: per event, Δs_BM/(Δs_B + Δs_MS) = 0.62-1.00.
> Relative to quadrature, the median Δs_BM/√(Δs_B² + Δs_MS²) is 0.99-1.00 at 0.45 keV and 0.95-1.00 at 0.6 keV. It is
> 0.80-0.97 at 1-3 keV, around the crossover Λ_cross = 1.16-1.91 keV, and consistent with 1 within 2σ at 5-10 keV.
> The deepest deficit, 0.80-0.89, sits at Λ/Λ_cross = 1.25-1.73 for every species-mass.
> Quadrature is therefore an upper estimate of the combined thickness, conservative by up to 20 % near the crossover.
> We quote the measured ratio and claim no combination rule. Stage 1 (`analytic/NEAR_MISS_IMPULSE.md` §0, item 6) treats
> MS only as the measured floor.

## 6. Tags and provenance

| Item | Tag | Source |
|---|---|---|
| Δs_B, Δs_MS, Δs_BM medians and errors | VERIFIED (measured, reproduced exactly) | `sim/stage3/results/P1.json` `points.*.by_lambda.*.Ds_*`; `data/sim_stage3/summary/events_p1.npz` |
| r_q, r_l per cell | VERIFIED (measured, reproduced exactly) | P1.json `B_MS_combination` |
| x = median Δs_B/Δs_MS (per event), median linear-sum expectation of r_q | VERIFIED (new medians on the same rows; bootstrap) | `u2_panel.json` `paired` |
| Λ_cross | VERIFIED measurement; log-log interpolation between grid points | P1.json `B_MS_crossover_keV` |
| Quadrature/linear sum of medians (main-panel lines) | derived reference (arithmetic on measured medians), not a model | `u2_panel.json` |
| (1 + x)/√(1 + x²) curve | algebraic identity, not a fit | — |
| ±5 % on Δs_B above 5 keV | ESTIMATE (P-9 unattributed systematic, as in P1.json) | P1.json `syst_unattributed_rel` |
| MS floor 10-28 µm | VERIFIED | `sim/stage3/README.md` item 5; P1.json `Ds_MS` |

Nothing outside `acts/stage4/u2_panel/` was written apart from one line in `LOG.md`.
