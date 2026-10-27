# Stage-5 figure plan (C001 quirks theory track) — 2026-10-14, final set 2026-10-16

Sources: plan.md §11 "Stage-5 figure list" (C-6), §2.6 fallback deliverables, §9 (U-2), D4-13; LOG.md l.161, l.181.
Label: left "Private work (simulation)", right "√s = 14 TeV, PU 200, 3 ab⁻¹", no CMS name/logo; "truth level" tag on
truth figures. Truth figures only: `--truth-rlabel sqrt_s` gives the right label "√s = 14 TeV" (default = full label; the
user has not chosen yet; both variants are produced in `figures/truth/` and `figures/truth_sqrt_s/`).

## How to run
```
# FINAL set (real inputs only; refuses placeholder / DEV / dry-run inputs and any stamped figure), < 30 s CPU:
nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --truth
nice -n 15 pixi run python stage5/make_figures.py --final --truth --truth-rlabel sqrt_s
# development / placeholder runs (unchanged):
nice -n 15 pixi run python stage5/make_figures.py --results stage5/placeholder_inputs
```
Output of --final: `stage5/figures/final/` (detector-level D1-D11), `final/truth/` (T1-T4, full right label) and
`final/truth_sqrt_s/` (T1-T4, right label "√s = 14 TeV"); each `<id>.pdf/.png` + `<id>.json` sidecar (input and code
sha256, stamps, label variant) + `index.json` (status per id, Stage-4 outcome, final-mode checks). Schema-v2 extension
files are read from `<results>/proposed/` if it exists, else from `<results>` itself (real run_all layout).
`STAGE4_SUMMARY.json` (next to the run dir, used only if its primary_run.dir is the run) feeds the WP status / fallback
annotations, the N_exp cross-check and the truth merged-surface fractions of D9. Per-figure description:
`stage5/FIGURES_FINAL.md`.

## Figure list

| id | content | input (schema key) | level | label | status |
|---|---|---|---|---|---|
| D1 | ε(m, Λ) maps at R_A…R_E and at the §8 fallback selection r_fb (no WP) | signal_eff.json a2.points[].report_rungs; limits.json points[].s | det | full | **FINAL (real)** |
| D2 | ε vs ladder rung (23 rungs), one per species-mass, CP 68 % | signal_eff.json a2.points[].ladder | det | full | **FINAL (real)** |
| D3 | B₈₄ and median B vs rung, SR-T / SR-G, 0.11 / 0.3 lines; no-WP state + minimum B₈₄ | bsum_wp.json ladder, rule.wp; STAGE4_SUMMARY ladder | det | full | **FINAL (real)** |
| D4 | PU fake candidates per trial vs rung: B1 direct, ρ = 2 thinning, factorisation, end state ± σ_ln; closure N_obs/N_pred panel | background.json columns, end_state, closure.trend.points | det | full | **FINAL (real)** |
| D5 | expected 95 % CL limit on N_sig vs Λ per mass: toy median + TOY ±1/2σ bands (primary), asymptotic median cross-check, predicted N_exp | limits.json expected_toys/asymptotic; acceptance.json; xsec.json | det | full | **FINAL (real)** |
| D6 | expected σ limit vs m at Λ = 0.6/1/1.5/2/3/5 keV (toy bands) + σ_th (E, PDF band) | limits.json + acceptance.json + sim/results/xsec.json | det (A truth) | full | **FINAL (real)** |
| D7 | expected σ₉₅/σ_th map (toy median, cell values); exclusion / ±1σ / 5σ contours only where crossing 1 (none) + FASER overlay | limits.json + acceptance.json + xsec.json; stage5/external_bounds.json | det (A truth) | full | **FINAL (real)** |
| D8 | M_est spectra per mass at R_A and at r_fb (f_CKF < 0.2, best candidate per event) | signal_obs_a2.npz; limits.json primary | det | full | **FINAL (real)** |
| D9 | detector-level (A1 no PU, A2 PU 200) Λ edges vs truth comparators (ℓ_max = R_IT lower; merged-surface 50 % upper, post hoc) | edges_det.json; STAGE4_SUMMARY cited_investigations.truth_degeneracy | det + truth overlay | full | **FINAL (real)** |
| D10 | sep_IT^det vs truth sep_IT: A1 (no PU) calibration + ratio; PU 200 marked NOT MEASURABLE | sep_it_det.json | det | full | **FINAL (real)** |
| D11 | event display: signal candidate in PU 200 vs best PU-only fake (other event) | event_display.npz | det | full | **FINAL (real)** |
| T1 | U-2 thickness Δs_B, Δs_MS, Δs_BM vs Λ + ratio panel (E200/500/1000/1500, Ẽ500) | acts/stage4/u2_panel/u2_panel.json | truth | flag | **DONE (real)** |
| T2 | U-2 ratio to quadrature vs x = Δs_B/Δs_MS | u2_panel.json | truth | flag | **DONE (real)** |
| T3 | U-2 ratio vs Λ/Λ_cross | u2_panel.json | truth | flag | **DONE (real)** |
| T4 | Stage-3 truth Λ edges vs m (4 edges, E/Ẽ, smoothed fits) | sim/stage3/results/P2.json | truth | flag | **DONE (real)** |

T1–T3 are a restyle of the approved U-2 numbers (no recomputation); T4 plots P2.json as published.

## Still needed (schema gaps Stage 4 must fill; details in stage5/proposed_schema.json)
1. **A(trigger + preselection) per (m, Λ)** — limits are on μ = N_sig in acceptance; σ₉₅ = μ₉₅/(L·A) needs A. Fallback
   now: ESTIMATE trigger proxy from xsec.json (E only, no preselection; stamped in the figure).
2. **Detector-level edges** (D9), **sep_IT^det calibration** (D10), **event-display hit dump** (D11): not in schema v1.
3. **Toy quantiles** of the primary (toys) expected limit: v1 has bands only for the asymptotic cross-check.
4. ε **factor breakdown** (trigger/presel/PV/fiducial/finder; plan §11 item 3) is not in v1 → D1 is per rung, not per factor.
5. `limits.json` `discovery` is written by run_all but not listed in v1 (D7 reads it if present).
6. ~~Stage-5-own: digitise FASER / D0 / Farina-Low curves into `external_bounds.json` (D7 overlay).~~ DONE 2026-10-16: `stage5/external_bounds.json` (FASER HEPData t2; D0 and Farina-Low from paper text/tables; FASER Fig. 5 gray regions by vector extraction), see `EXTERNAL_BOUNDS.md`.

## Files
`plotting.py` (style, label, stamps, map2d, limit_plot, eff_vs_rung, hist_errorbar, save + sidecar), `make_figures.py`,
`make_placeholder_inputs.py` (synthetic, schema-exact; passes run_all.validate_outputs), `acts_names.py` (rung names,
checked against the frozen package), `proposed_schema.json`, `placeholder_inputs/`, `figures/{placeholder,truth,truth_sqrt_s}/`.
Deviation (stated): mplhep is not in the TT env; style via rcParams, histograms via `stairs` + explicit errors, colorbar via
`append_axes` (make_square_add_cbar equivalent). Palette: dataviz reference categorical (validator PASS; contrast WARN
relieved by markers + legends), sequential blue, diverging blue–grey–red.

## 2026-10-16: real-input fixes (C12FC_v1)
Fixed against the frozen run (mismatches listed in acts/stage4/STAGE4_RESULTS.md §11.3): extension files read from the
run-dir top level by default; D9 rewritten for the real `edges_det.json` layout with the merged-surface 50 % truth
comparator (the 13–25 keV median-separation edge is not drawn); D10 shows the A1 (no PU) calibration and marks PU 200
NOT MEASURABLE; D5–D7 use the toy bands (asymptotic median only as a cross-check); npz `file` ≡ `src_file`; WP / fallback
state from bsum_wp.json + STAGE4_SUMMARY.json; `--final` mode refuses placeholder/DEV inputs. Gaps 1, 3, 5 above are
closed by schema v2 (acceptance.json, toy bands, discovery); gap 4 (ε factor breakdown) is in acceptance.json but no
figure was added for it (see FIGURES_FINAL.md).
