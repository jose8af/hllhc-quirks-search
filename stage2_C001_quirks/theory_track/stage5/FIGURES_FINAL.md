# Stage-5 final figures (C001 quirks theory track), 2026-10-16

**Inputs.** The frozen, non-DEV Stage-4 run `data/acts_stage4/analysis/C12FC_v1` (freeze `b42aef4d…`, `freeze_match =
true`), `data/acts_stage4/analysis/STAGE4_SUMMARY.json` (schema v2; used because its `primary_run.dir` is this run),
`sim/results/xsec.json`, `stage5/external_bounds.json`, and for the truth figures `acts/stage4/u2_panel/u2_panel.json` and
`sim/stage3/results/P2.json`. Everything is read-only.

**Outcome shown.** There is no WP in SR-T or SR-G (`bsum_wp.json → rule.wp`, branch "no WP in either category (§5.3):
§8 fallback"). All limit figures are at the pre-declared fallback selection r_fb, and no figure implies a WP, an
exclusion or a discovery.

**Commands** (< 30 s CPU, nice 15):
```
nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --truth
nice -n 15 pixi run python stage5/make_figures.py --final --truth --truth-rlabel sqrt_s
# partial regeneration (review R1 fixes); --only now merges into the existing index.json instead of overwriting it
nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --only D2,D3,D4,D5,D6,D7,D8,D9,D11
```

**Output.**
- 38 detector-level figures in `stage5/figures/final/`.
- 8 truth-level figures in `final/truth/` (right label "√s = 14 TeV, PU 200, 3 ab⁻¹").
- The same 8 truth-level figures in `final/truth_sqrt_s/` (right label "√s = 14 TeV" only). **Not used (user decision 2026-10-16: truth figures use the full right label; `final/truth/` is the deliverable).**
- Each figure is written as `.pdf` + `.png` (dpi 200) + a `.json` sidecar (sha256 of the inputs and code, stamps, label
  variant, figure-specific numbers).
- `index.json` holds the status of each id, the Stage-4 outcome and the `--final` checks.
- 0 stamps and 0 missing inputs across all 54 sidecars.
- `--final` refuses the placeholder inputs. Tested: it exits with "REFUSED … inputs under stage5/placeholder_inputs;
  … PLACEHOLDER". `save()` also refuses any stamped figure in final mode.

**Labels.**
- Left: "Private work (simulation)". Right: "√s = 14 TeV, PU 200, 3 ab⁻¹". No experiment name or logo.
- Truth-level figures carry the "truth level" tag and also exist in the √s-only variant.
- Mixed figures (D6, D7: detector-level limits with a truth-level acceptance; D9: truth comparators) say so in the
  in-figure text.

**Level key.**
- *det* = detector-level simulation in a public-geometry ACTS model. It uses no CMS software and makes no CMS claim.
- *truth* = Stage-3 generator/kernel quantities.
- A1 = no PU. A2 = PU 200. A5 = PU 200 full chain at 1 keV.

## FIX R3-NORM (2026-10-16): signal normalisation (D5, D6, D7 regenerated)

Erratum, see `acts/stage4/investigation/INV_NORM_F200.md` and `acts/stage4/review/FIX_RESULTS_R3_NORM.md`.
`make_figures.py acceptance()` returned `acceptance.json → A_trig_presel`, a fraction of the Stage-3 template
population (pT(QQ̄) > 200 GeV, |η| < 4), and combined it with the inclusive σ_norm. It now returns A · f with the tail
fraction f = P(pT(QQ̄) > 200 GeV, |η| < 4) (E: `xsec.json → trigger_yields_E.rows[m].f_pt200_TRG_over_INC` = 0.0476 /
0.104 / 0.146 / 0.169; Ẽ500: 0.1135 from `data/sim/npz/S-TRGS_m500.npz`). This fixes N_exp (D5) and σ₉₅ (D6, D7) together;
σ₉₅ is now a limit on the inclusive σ(pp → QQ̄), the population σ_th refers to (D6 y label "95 % CL limit on inclusive
σ(pp → QQ̄)"; D5 legend "N_exp = σ_norm · f · L · A"). μ₉₅ and its bands are unchanged. Every μ₉₅/N_exp and σ₉₅/σ_th grows
by 1/f = 5.9–21: best 37.6 → **790** (E200 1.5 keV). The −2σ toy edge no longer dips below N_exp or σ_th anywhere
(min −2σ/N_exp = 1.7). The N_exp cross-check against `STAGE4_SUMMARY.json` (10⁻⁶) passes with the regenerated summary.
Command: `nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --only
D5,D6,D7` (5 s CPU). All 12 regenerated PNGs were opened.

## Paper fix round R2 (2026-10-16): print legibility and in-figure text

Review `paper/review/REVIEW_PAPER_R2.md` B-4 (in-plot text 3–4 pt at print size; stale and internal text). Changes in
`stage5/plotting.py` (all figures regenerated after it): legend and tag-block font `x-small` → `small`; map cell values and
rung tick labels `xx-small` → `x-small`. Changes in `stage5/make_figures.py` (text and layout only; no number changed):
- D1: tag "PU 200 (8 cells full chain)"; no "(WP_RULE A.2b)", no "(D9)". FALLBACK_TXT shortened (no "§8").
- D2: y range to 30 (legend clear of the data). D3: last tag line shortened. D4: legend `handlelength`/`columnspacing`
  reduced, label "end state (closure)", y range widened (tag below the data), tag lines regrouped.
- D5/D8: "(§8 fallback)" → "(fallback)". D6: "A: truth-level acceptance (Stage 3)" instead of the file name.
- D7: short tag (fermion/r_fb, A, FASER hatch, no exclusion ≥ 37.6 incl. −1σ (now ≥ 790, FIX R3-NORM), blank cells); the stale
  "INV_A2FC_E500 open" line, the zero-count line and the list of bounds outside the range were removed (paper caption);
  sidecar meta gains `outside_range`, `discovery_cells`.
- D8: tag reduced to 3 lines and placed below the legend; 2 m_Q line to ymax 0.45; y range ×2.5.
- D9: legend `x-small` (8 entries), shorter labels, y range to 3×10⁴; no "INV_SIGNAL_EFF §3.1"/"STAGE4_RESULTS §6.1".
- D10: axis labels and tag use the note symbol d_IT (was sep_IT); tag 2 lines; y range to 3×10⁴.
- D11: shorter legend labels and tag; no B1 job/trial id in the figure (still in the sidecar); frame enlarged.
- T4: "(see D9)" removed.
- σ_th labels (D6, D7) unchanged (held pending the normalisation check, NORM-ANCHOR in the paper). Resolved by FIX
  R3-NORM (above): σ₉₅ now uses A · f, so σ_th (inclusive) is the right comparator; D6 y label says "inclusive".
Commands: `nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1
--only D1,D2,D3,D4,D5,D6,D7,D8,D9,D10,D11` and `... --final --truth --only T4` (truth `index.json` merged by hand; the
`--only` merge exists only for the detector set). All regenerated PNGs (38 detector + T4) were opened (the 13 paper figures one by one, the siblings on contact sheets); the paper copies
are byte-identical.

## Paper review R3 (2026-10-16): text-only figure fixes
- D6 (all 6): theory legend "NLO K" → "$K_{QCD}$" (K is NNLO_approx+NNLL, sim/VALIDATION.md).
- D7: tag "no expected exclusion: median ≥ 790 in every cell, −1σ edge ≥ 54" (R4: floor) (min of the toy −1σ edge / N_exp, computed in code).
- D9: comparator "12.8-25 keV" (as in the Stage-3 numbers), was "13-25 keV".
Regenerated with `--final --results data/acts_stage4/analysis/C12FC_v1 --only D6,D7` and `--only D9`; PNGs opened.

## Plot lint and visual check

- **Visual check.** I opened every PNG (all 54).
  - Fixed during this pass: legend/tag overlaps (D3, D4, D5, D6, D8, D9, D10, T4), `2×10⁰`-style log tick labels (D5),
    and colliding 0.85/1 tick labels (D5).
  - Also fixed: a text overflow past the frame (D3, D11), the unused half of the colour scale and a legend covering map
    cells (D7), and the empty display area (D11).
  - Wrong units: the D4 y-axis said "probability" for values up to 3 × 10⁴. It now reads "PU fake candidates per trial".
- **Lint.** `~/FISICA_USFQ/jfc/src/conventions/lint_plots.py` (`lint_file` on `stage5/plotting.py` and
  `stage5/make_figures.py`) reports 8 hits (unchanged by the R1 fixes; recount 2026-10-16):
  - 6 are `ax.text(` calls inside the mplhep-equivalent helpers (`exp_label`, `add_text`, `draw_stamps`, map-cell
    annotation). mplhep is not in the TT environment, and figure code never calls `ax.text` directly.
  - 1 is the heuristic "multiple exp_label() on a sharex figure". The helper is defined once and called once per main
    panel, never on a ratio panel.
  - 1 is a false positive "bare underscore" on the D9 arrow label: the underscore is in the f-string field
    `{lammax_a2:g}`, which is replaced by a number and never rendered.
  - The first 7 are the documented deviation (FIGURE_PLAN.md). No other rule is violated.
- **Review R1 (2026-10-16).** `review/REVIEW_STAGE5_R1.md` (0 A, 6 B, 9 C) is addressed in
  `review/FIX_STAGE5_R1.md`. D2–D9 and D11 were regenerated, and every regenerated PNG (31) was opened.

## Detector-level figures (`stage5/figures/final/`)

### D1: signal efficiency maps (6 files)
- **Files:** `D1_eps_map_R_A`, `_R_B`, `_R_C`, `_R_D`, `_R_E`, `D1_eps_map_rfb`.
- **What it shows:** ε(m_Q, Λ) for E (fermion) on the A2 grid (4 masses × 8 Λ, 0.45–5 keV), with the cell values printed.
  - R_A = R04 (N_IP2 ≥ 7). R_B = R_A + w_core < 18.75 mm. R_C = R_A + w < 4.7 mm. R_D = R14. R_E = R23.
  - `rfb` = ε at the §8 fallback selection r_fb (SR-T + SR-G = `limits.json → s` summed).
- **Source:** `signal_eff.json → a2.points[*].report_rungs`; `limits.json → points[*].s`.
- **Level:** det (A2, PU 200).
- **Caveats:**
  - ε(R01–R04) are lower bounds (D9).
  - 9 points are the A2FC full chain (8 of them in the E maps); the other 31 are numpy A2 with no CKF.
    INV_A2FC_E500 is CLOSED: the full-chain systematic is ×0.87 at r_fb (STAGE4_RESULTS §4.3), not applied.
  - The barrel-only ceiling is ≈ 0.3.
  - Ẽ500 (a single mass) is in D2, D5 and D8, not in the maps.

### D2: ε vs ladder rung (5 files)
- **Files:** `D2_eff_vs_rung_{F200,F500,F1000,F1500,S500}`.
- **What it shows:** ε at each of the 23 cumulative rungs for each Λ, with CP 68 % error bars.
- **Source:** `signal_eff.json → a2.points[*].ladder`.
- **Level:** det (A2).
- **Caveats:** ε = 0 is not drawn on the log axis (stated in the figure). Rung-family boundaries are dotted. The rung
  ticks carry the rung number and the cut ("R04 N_IP2 ≥ 7"), as in D3 and D4, so rungs quoted by number can be found
  on the axis.

### D3: background vs rung, no-WP state (1 file)
- **File:** `D3_bsum_vs_rung`.
- **What it shows:**
  - B₈₄ and median B per rung for SR-T and SR-G.
  - The WP budget B₈₄ = 0.11 per category and 0.3 combined.
  - A star at the minimum B₈₄ = 1.2 × 10⁶ (R09, both categories), 7.05 decades above 0.11.
  - The text states the no-WP / §8 fallback state. There are no r* lines because there is no WP.
- **Source:** `bsum_wp.json → ladder`, `rule.wp`; `STAGE4_SUMMARY.json → ladder` (minimum and decades).
- **Level:** det.
- **Caveats:** The rung ticks carry the rung number (R01–R23), so the starred minimum "at R09" can be read off the
  axis. From R08 on, B is dominated by zero-count bounds (C′, SM). The deep-rung B₈₄ is driven by the trend term
  and the model σ_ln (STAGE4_RESULTS §1–3).

### D4: PU fake-rate extrapolation (1 file)
- **File:** `D4_pfake_extrapolation`.
- **What it shows:** Expected PU fake candidates per trial (one PU-200 event, one MET road) along R01–R14:
  - B1 direct (ρ = 1) with √N errors;
  - ρ = 2 thinning;
  - the factorisation model, drawn only at R08–R14 (B1 = 0), where it is an independent extrapolation. At R01–R07
    `P_fact` equals `B1_per_trial` exactly by construction, so drawing it there would look like an independent
    agreement; the in-figure text says so ("factorisation ≡ B1 direct at R01–R07 (not drawn)");
  - the end state (closure applied) with a ±σ_ln band.

  The ratio panel shows the closure trend N_obs/N_pred at R04–R07.
- **Source:** `background.json → columns`, `end_state`, `closure`.
- **Level:** det (PU only).
- **Caveats:**
  - The quantity is a mean count per trial, not a probability, because it exceeds 1 at loose rungs. The y-label was
    corrected.
  - Rungs ≥ R08 are zero-count bounds.
  - The ratio-panel error bars are smaller than the markers.
  - The closure-trend text reads "trend significant: yes" (`background.json → closure.trend.significant`;
    t_boot = −80, t_wls = −55).

### D5: expected limit on N_sig vs Λ (5 files)
- **Files:** `D5_limit_mu_vs_lambda_{F200,F500,F1000,F1500,S500}`.
- **What it shows:**
  - The expected 95 % CL limit on μ (signal events in the trigger + preselection acceptance): hybrid-CLs toy median
    with **toy ±1σ / ±2σ bands** (primary, D4).
  - The asymptotic median as a dotted cross-check. The near-degenerate asymptotic bands are not drawn.
  - The predicted N_exp = σ_norm · f · 3 ab⁻¹ · A (f = P(pT(QQ̄) > 200 GeV), FIX R3-NORM).
  - The text gives the best μ₉₅/N_exp (E200 790 at 1.5 keV; E500 1.3 × 10⁴; E1000 3.8 × 10⁵; E1500 3.8 × 10⁶;
    Ẽ500 2.8 × 10⁵, all at 3 keV) and lists the Λ values with no limit (ε = 0).
- **Source:**
  - `limits.json → expected_toys`, `expected_asymptotic`;
  - `acceptance.json → A_trig_presel` × f (`xsec.json` / `S-TRGS_m500.npz`);
  - `xsec.json` σ_norm. N_exp agrees with `STAGE4_SUMMARY → fallback_points.N_exp_3ab` to 10⁻⁶; this is checked in code
    and the figure fails on a mismatch.
- **Level:** det (A is truth level).
- **Caveats:**
  - These are expected limits at r_fb with no WP.
  - Deep-rung B central values are zero-count simulation bounds (conservative).
  - The best point (E200 1.5 keV) uses numpy-A2 ε; INV_A2FC_E500 is CLOSED (systematic ×0.87, not applied, ratio ≈ 910).
  - The toy bands are discrete at small B.
  - Since FIX R3-NORM the −2σ toy edge stays above N_exp everywhere (≥ 1.7 × N_exp); the median is ≥ 790 × N_exp.
  - The y range keeps the data in the middle half of the axes (bottom quarter for the text, top third for the legend);
    the earlier 4–6 empty decades are gone.

### D6: expected σ limit vs m_Q (6 files)
- **Files:** `D6_limit_xsec_vs_m_L{0p6,1,1p5,2,3,5}`.
- **What it shows:**
  - σ₉₅ = μ₉₅/(3 ab⁻¹ · f · A), a limit on the inclusive σ(pp → QQ̄), for E vs m_Q, with toy bands and the asymptotic median.
  - σ_th for E (`sigma_norm_nic2_fb`, N_IC = 2, NLO K, PDF band).
  - The text gives the minimum σ₉₅/σ_th (790 at 1.5 keV, 820 at 2 keV, ≥ 2.3 × 10³ elsewhere: "no exclusion").
- **Source:** `limits.json`, `acceptance.json`, `xsec.json`.
- **Level:** det limit with a truth-level A.
- **Caveats:**
  - Only 4 masses, joined by straight lines.
  - At 0.6 keV there is no limit at m_Q = 1500 GeV (ε = 0; stated).
  - The σ_norm N_IC label is inconsistent upstream (≤ ×2; STAGE4_RESULTS caveat 18).
  - The 0.85 keV slice is not drawn; it is in D7.
  - Since FIX R3-NORM the −2σ toy edge stays above σ_th at every mass and Λ; the median is σ₉₅/σ_th ≥ 790. Same
    y-range rule as D5.

### D7: exclusion / discovery map (1 file)
- **File:** `D7_exclusion_map`.
- **What it shows:**
  - The expected σ₉₅/σ_th (toy median) on the E (m_Q, Λ) grid, with every cell value printed, on a one-sided log
    colour scale from 1. No cell is below 1.
  - **No exclusion, ±1σ or 5σ-discovery contour exists, so none is drawn.** The text says so: min 790 (was 37.6 before FIX R3-NORM); also no
    crossing at the −1σ toy edge. (Since fix R2 the 5σ statement is in the paper caption and in the sidecar
    `discovery_cells` = 13.)
  - Blank cells are ε = 0 (no limit).
  - The FASER observed exclusion is shown hatched [VERIFIED].
  - The other existing limits lie outside the plotted range. Since fix R2 they are listed in the paper caption (Fig. 11)
    and in the sidecar `outside_range`, not in the figure. The recasts are named
    "Farina-Low HSCP recast", "monojet recast" and "Evans-Luty out-of-time recast", so no experiment name appears
    in the figure (display names only; `external_bounds.json` is unchanged).
- **Source:** `limits.json`, `acceptance.json`, `xsec.json`, `stage5/external_bounds.json`.
- **Level:** det limit with a truth-level A.
- **Caveats:**
  - Since fix R2 the zero-count-bound note and the full-chain systematic are stated in the paper caption, not in the
    figure (the stale in-figure text "INV_A2FC_E500 open" is gone).
  - Ẽ is not mapped: only one mass, Ẽ500, which is in D5.

### D8: M_est spectra (10 files)
- **Files:** `D8_mest_RA_{F200,F500,F1000,F1500,S500}`, `D8_mest_rfb_{…}`.
- **What it shows:**
  - The fraction of events per bin of M_est = |P_T^miss| cosh η_axis / (βγ)_ToF
    (`acts/stage4/analysis/signal.py` l.203). This is |P_pair| / (βγ): it estimates the **pair mass** M_QQ̄ ≥ 2 m_Q,
    not m_Q.
  - One entry per event (best candidate), f_CKF < 0.2, for up to 4 Λ values per mass. The legend gives the number of
    events N per curve.
  - Selections: R_A, or r_fb (the SR-G r_fb name, which is the inclusive fallback selection).
  - One reference line: **2 m_Q (M_QQ̄ threshold)**. The m_Q line was removed, since m_Q is not the M_est scale.
  - x range: 0 to the largest entry, between 3.2 and 6 m_Q, in bins of 0.4 m_Q (2 m_Q sits on a bin edge). The
    last bin holds the overflow, which is now 0 % for every curve except D8_mest_rfb_S500 at 5 keV (1 of 13 events).
    With the old fixed 3 m_Q range, 50–70 % of the Ẽ500 entries were in the overflow bin.
  - The per-curve event-level numbers (N, N with M_est undefined, median M_est/m_Q, fraction below 0.5 m_Q, number in
    1.3–1.7 m_Q, overflow fraction) are in each sidecar under `per_curve_event_level`.
- **Source:** `signal_obs_a2.npz` (key, row, L, FB, FB_names, f_ckf, M_est); `limits.json → primary`.
- **Level:** det (A2).
- **Interpretation (two clusters, nothing at m_Q by construction):**
  - **Upper cluster = pair mass.** It starts sharply at 2 m_Q (clearest in D8_mest_RA_F1500: nothing between
    ≈ 1.2 and 3.0 TeV). Without PU it never goes below that: A1 (no PU), same selection (R_A, f_CKF < 0.2, one entry
    per event, all A1 points), has 10 406 events with median M_est/m_Q = 2.46, 16 % quantile 2.11, and **0 events
    below 1.5 m_Q** (STAGE4_RESULTS §6.3: per-mass A1 q16 = 2.0–2.3 m).
  - **Low cluster (≈ 0.1–0.4 m_Q) = PU.** It appears only at PU 200: in-time PU BTL hits give β → 1, so (βγ)_ToF is
    large and M_est small.
  - **Nothing near m_Q is expected.** Pooled event-level numbers at R_A (all 40 A2 points, one entry per event,
    exactly what the figure plots): N = 850 events with M_est defined (of 1 051; 201 undefined), median
    M_est/m_Q = 2.26, **3 events (0.35 %) in 1.3–1.7 m_Q**, 19 % below 0.5 m_Q, 10 % in 0.5–1.5 m_Q.
  - The earlier catalogue numbers ("20 of 8 934 entries, 0.2 %, median 2.23") were candidate-level (all matched
    candidates, ≈ 10.9 per event), not what the figure shows. They are replaced by the event-level numbers above.
- **Caveats:**
  - At r_fb, N = 5–16 events per curve, so the shapes are statistically weak. The R_A version is the readable one.
  - M_est is an uncalibrated proxy, not an m_Q (or M_QQ̄) measurement.
  - Points with M_est undefined (β ≥ 1 or no BTL hit; 0–49 % per plotted curve) are not entered.

### D9: Λ edges, detector vs truth (1 file)
- **File:** `D9_edges_det_vs_truth`.
- **What it shows (vs m_Q):**
  - Detector-level half-maximum edges of ε(R_A) in ln Λ (row-level bootstrap errors):
    - A1 (no PU) lower and upper edges for E at 200–1500 GeV and Ẽ at 200, 500, 1000 GeV;
    - A2 (PU 200) lower edges;
    - A2 upper edge: none below 5 keV (grid end), drawn as arrows.
  - The truth comparators:
    - **lower:** median ℓ_max = R_IT (closed form);
    - **upper:** the Λ where f(any inner-pixel surface merged) = 50 %, and where f(merged or seed-degenerate) = 50 %.
      These come out at 4.5–5.5 and 4.1–4.9 keV (≈ 5 keV), against A1 upper edges of 4.7–6.6 keV.
  - The 13–25 keV Stage-3 median-separation edge is **not drawn**. It is not the comparator; the text says it was the
    pre-declared V4-3 (d) comparator and is not met (×2.7–3.5).
  - The truth upper markers (+30 / +60 GeV) and the A2 arrows (−30 GeV) are offset in m_Q for readability. The offsets
    are recorded in the sidecar.
- **Source:**
  - `edges_det.json` (real layout `sample|spin|m → R04.{lower, upper}`, `truth.lower_lmax_RIT_closed`);
  - `STAGE4_SUMMARY.json → cited_investigations.truth_degeneracy`, the same numbers as
    `data/acts_stage4/investigation/truth_degeneracy_*.json`.
- **Level:** det + truth overlay.
- **Caveats:**
  - The merged-surface comparator is **post hoc** (INV_SIGNAL_EFF §3.1, derived after the miss); the legend says so.
  - The 50 % crossings are interpolated here, linearly in ln Λ. The error is the binomial σ_f at 50 % divided by the
    local slope [E]. Values are in the sidecar (e.g. E500 4.87 ± 0.48 keV).
  - The truth fractions exist only for the 5 A2 species-masses.
  - The in-figure text block was re-wrapped into 6 shorter lines, and the y range starts at 0.012 keV, so the block
    no longer runs past the y-axis spine (review R1 B4).

### D10: sep_IT^det calibration (1 file)
- **File:** `D10_sepit_calibration`.
- **What it shows:**
  - The median sep_IT^det vs the median truth sep_IT (Stage 3), log–log, with the detector = truth line.
  - **A1 (no PU)** points for the 5 analysis species-masses (77 points; n ≥ 5 and an error given) in colour, with a
    det/truth ratio panel (A1 only). A1 tracks truth within ≈ 10 % at 3–20 mm truth, saturates at 20–45 mm below
    ≈ 1 keV, and sits on a floor at ≲ 1 mm.
  - **PU 200 (A2, A5; 45 points)** as grey crosses, labelled "NOT MEASURABLE (flag)", and excluded from the ratio
    panel. They are flat at ≈ 15–60 mm.
- **Source:** `sep_it_det.json` (`measurable`, `flag`, top-level `pu200_measurable = false`). Variant keys (BMx0.5, BMx2)
  are excluded.
- **Level:** det.
- **Caveats:** A1 is drawn for 5 of its 17 species-masses (all are in the JSON). At PU 200 there is no Λ information
  with this estimator.

### D11: event display (1 file)
- **File:** `D11_event_display`.
- **What it shows:**
  - The transverse (x, y) hits of one A2 signal candidate (E200, Λ = 0.45 keV, passes 14 of R01–R14): quirk hits plus
    the PU hits inside the candidate.
  - The best PU-only fake candidate (B1_00201, trial 28, passes 7 of R01–R14) from **another event**, overlaid in the
    same frame.
  - The signal MET direction (black dashed), and the **MET road of the fake trial** (dotted, in the fake's colour,
    road half-width ±δ95 = 0.15 rad). Equal-span axes; the frame leaves an empty band below the hits for the text.
- **Source:** `event_display.npz` (one in-band hit dump, chosen by run_all as the deepest candidate; not selected here).
  The fake's road is read from its B1 job file `data/acts_stage4/prod/C2/B1/B1_00201.npz` (read-only):
  `trials.phimet[28]` = 2.2974 rad, `trials.delta95[28]` = 0.15 rad, `trials.ev[28]` = 5032, road 0. The sidecar
  records these values, Δφ to the signal MET, the fake hits' median azimuth at r > 100 mm (2.284 rad), and the file's
  sha256.
- **Level:** det.
- **Caveats:**
  - Only candidate-band hits are stored, not the full event.
  - **The fake lies along its own trial's MET road by construction.** Each B1 trial sets φ_MET = φ₀ + road · 2π/roads,
    with φ₀ uniform in (−π, π) per event (`acts/stage4/run_stage4.py` l.379–380, 402–403), and the finder only
    searches ±δ95 = 0.15 rad around it. The fake's road is **0.017 rad** from the signal MET (2.3146 rad). The two
    directions are independent random draws (B1 φ₀ uniform; signal MET from its own seed), so the near-alignment is a
    chance coincidence of two independent events, not a property of the figure code. `products.event_display()` dumps
    the hits in the lab frame with no rotation. The figure says this in its text.
  - `event_display.npz` stores `met_phi = null` for the fake because of a key mismatch in frozen Stage-4 code (see
    "Issues for Stage 4"); the figure works around it by reading the B1 job file.

## Truth-level figures (`final/truth/` and `final/truth_sqrt_s/`, identical apart from the right label)

| file | what | source | caveats |
|---|---|---|---|
| `T1_u2_thickness_{F_m200,F_m500,F_m1000,F_m1500,S_m500}` | U-2 (P1) median plane thickness Δs_B, Δs_MS, Δs_BM vs Λ with quadrature / linear-sum curves; ratio panel Δs_BM/√(Δs_B² + Δs_MS²); Λ_cross marked | `acts/stage4/u2_panel/u2_panel.json` (restyle only, numbers unchanged) | truth level, \|η_pair\| < 1; the only P1 deliverable (no detector-level P1, D4-9). T1_F_m200: Δs_B is absent at Λ ≥ 7 keV in the panel, so the quadrature / linear-sum curves stop at 5 keV (data-limited, not a plotting cut) |
| `T2_u2_ratio_vs_x` | U-2 ratio vs x = Δs_B/Δs_MS, all 34 cells, with the single-event linear-sum curve | same | truth level |
| `T3_u2_ratio_vs_lamcross` | U-2 ratio vs Λ/Λ_cross | same | truth level |
| `T4_truth_edges_vs_mass` | Stage-3 truth Λ edges vs m_Q (lower: ℓ_max = R_IT, N_osc = 1; upper: 100 µm merging, ℓ_max = 100 µm) with the smoothed fits | `sim/stage3/results/P2.json` | truth level; the text now says the upper edges are median-separation quantities, not the comparator of the detector upper edge (D9). The y range was widened so the legend clears the data |

## Figures not made, and why

- **ε factor-breakdown figure** (trigger / presel / PV / fiducial / finder; plan §11 item 3). The numbers exist in
  `acceptance.json → factors` (truth-level A and the finder ε at the reporting rungs). No figure id was planned for
  them, and none was added in this pass. The A values enter D5–D7.
- **Ẽ σ-limit vs m and Ẽ exclusion map.** Only one Ẽ mass (500 GeV) exists in A2. Its limits are in D5_S500 (μ₉₅ and
  N_exp).
- **t_est / χ² vs Λ, `results/sensitivity.json`.** Not produced by the frozen Stage-4 pipeline (STAGE4_RESULTS §6).
- **Detector-level P1 (coplanarity).** Not measured, by decision D4-9. Only the truth-level T1–T3 exist.
- **WP-based sensitivity / discovery reach.** There is no WP. D5–D7 show the §8 fallback state, `mu_3events` is null
  everywhere, and the 5σ μ is ≫ N_exp.
- **A1 / A5 M_est spectra.** Not in the plan list. The pooled numbers are in STAGE4_RESULTS §6.3.
- **`stage5/figures/placeholder/`** (old, PLACEHOLDER-stamped). Not regenerated. The synthetic placeholder inputs are
  still in schema v1, so a placeholder run now skips D9 (edges layout). The final set does not use them.

## Issues for Stage 4 (frozen code; not edited here; also to be listed in the Stage-4 report)

- **`products.event_display()` never stores the PU fake's MET direction.** `acts/stage4/analysis/products.py`
  l.205–206 looks up `dj['tr']['trials_phimet']`, but the `tr` dict built by `background.to_g3_job()`
  (`background.py` l.33–41) holds keys **without** the `trials.` prefix (`tr = {k: d['trials.' + k] for k in TR_KEYS
  ...}`), and `TR_KEYS` does not include `phimet`. The key can never be found, so `event_display.npz` always has
  `pu_fake.met_phi = null`. Cosmetic (no number in any limit, background or efficiency depends on it). Fix for a
  future run: add `'phimet'` to `TR_KEYS` and look up `dj['tr']['phimet'][t]`. Stage 5 works around it by reading
  `trials.phimet[trial]` from the B1 job file (D11).

## Code changes (stage5 only)

- **`make_figures.py`:**
  - The extension files default to `<results>/proposed/` if that directory exists, else `<results>`.
  - npz alias `file` ≡ `src_file`.
  - It reads `STAGE4_SUMMARY.json`: the WP / fallback text, the minimum B₈₄, the N_exp cross-check, the truth
    merged-surface fractions, and the outcome in `index.json`.
  - `--final` mode with an input guard.
  - Toy bands in D5–D7.
  - D9 and D10 rewritten.
  - D11 `met_phi` fix.
  - Fallback-aware tags in D1, D3, D5–D8.
  - The visual fixes listed above.
- **`plotting.py`:**
  - `FINAL` refusal in `save()`;
  - explicit PDF / PNG `savefig`;
  - callable cell format;
  - `log_ticks`;
  - `ε = 0` handling on log axes;
  - a `fraction` histogram mode.
- **`FIGURE_PLAN.md`, `proposed_schema.json`:** status updated.
- **Review R1 fixes (2026-10-16; `review/FIX_STAGE5_R1.md`):**
  - `plotting.eff_vs_rung` and D4: rung ticks with the rung number (`rung_label(name, short=False)`);
  - D4: factorisation model drawn only where B1 = 0 (≥ R08), "trend significant: yes/no";
  - D5/D6: `log_frame()` y range (data in the middle, no empty decades);
  - D7: `EXT_DISPLAY` recast display names;
  - D8: pair-mass caption and 2 m_Q line, data-driven 0.4 m_Q binning up to 3.2–6 m_Q, per-curve event-level
    numbers in the sidecar;
  - D9: re-wrapped text block, y range from 0.012 keV;
  - D11: `fake_road()` reads the fake trial's φ_MET and δ95 from its B1 job file; road line, caveat text, frame;
  - `--only` merges into the existing `index.json` (it used to overwrite it with the subset).
