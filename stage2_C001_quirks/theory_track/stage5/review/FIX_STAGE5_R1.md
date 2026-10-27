# Stage 5 final figures: fixes for REVIEW_STAGE5_R1 (2026-10-16)

Scope: only `stage5/` was changed (`make_figures.py`, `plotting.py`, `FIGURES_FINAL.md`, `EXTERNAL_BOUNDS.md`, `figures/final/`).
`acts/stage4/` and `data/` were read, never written. Backups of the pre-fix code, docs and `figures/final/` were kept in the
session scratchpad.

Regeneration (about 30 s CPU, nice 15):
`pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --only D2,D3,D4,D5,D6,D7,D8,D9,D11`.
D1, D10 and the truth figures are unchanged. The 31 regenerated PNGs were all opened after the last regeneration.
After the run, `index.json` still lists all 11 ids as OK (38 figures), `final_checks` pass with freeze_match = true, and the 38
detector sidecars carry 0 stamps. The plot lint gives 8 hits, the same count as before the fixes (see FIGURES_FINAL §lint).

## Category B

| finding | resolution | change |
|---|---|---|
| **B1** D8 caption/lines misread the bimodality; candidate-level statistic; Ẽ overflow | RESOLVED | **Lines.** The m_Q line is removed. The one line left is "2 m_Q (M_QQ̄ threshold)". **Text.** The in-figure text adds "M_est: pair-mass proxy, ≥ 2m_Q" and "low cluster: PU BTL hits (β → 1)". **Range.** Bins are 0.4 m_Q wide, with 2 m_Q on a bin edge. The range runs to the largest entry, between 3.2 and 6 m_Q. Overflow is now 0 % for every curve except rfb_S500 at 5 keV (1 of 13 events); before, it was 50–70 % for Ẽ500. **Sidecar.** Each sidecar records `per_curve_event_level` (N, N undefined, median/m, fraction < 0.5 m, n in 1.3–1.7 m, overflow). **FIGURES_FINAL §D8 rewritten.** It gives the pair-mass interpretation (signal.py l.203) and replaces the candidate-level "20 of 8 934" with event-level numbers that match the plot: N = 850, median 2.26, 3 events (0.35 %) in 1.3–1.7 m_Q, 19 % below 0.5 m_Q. It adds an A1 cross-check computed here: 10 406 events, median 2.46, q16 2.11, 0 events below 1.5 m_Q. |
| **B2** D11 fake road missing; caveat "not determined" | RESOLVED | **New `fake_road()`.** It reads `trials.phimet[28]` = 2.2974 rad and `trials.delta95[28]` = 0.15 rad from `data/acts_stage4/prod/C2/B1/B1_00201.npz` (read-only). That file is listed in the sidecar inputs. **Figure.** It draws "MET road of the fake trial (±0.15 rad)" as a dotted line in the fake's colour. The text adds "the fake lies along its own trial MET road by construction; that road is 0.017 rad from the signal MET (chance)". The frame was widened so the text no longer overlaps the hits. **Sidecar.** It records phi, delta95, ev 5032, road 0, Δφ = 0.0172 rad and the median hit azimuth 2.284 rad. **FIGURES_FINAL §D11.** The caveat is replaced. The frozen-code key mismatch is recorded under the new "Issues for Stage 4". |
| **B3** rung axis without rung numbers (D2, D3, D4) | RESOLVED | `plotting.eff_vs_rung` and the D4 ratio axis now use `rung_label(name, short=False)`, so the ticks read "R04 N_IP2 ≥ 7" and so on. |
| **B4** D9 text block runs past the y-axis | RESOLVED | The block is re-wrapped into 6 shorter lines, and ylim starts at 0.012 keV. The block now sits inside the frame, clear of the data. |
| **B5** D4 factorisation ≡ B1 direct at R01–R07 | RESOLVED | The diamonds are drawn only where B1_groups = 0 (R08–R14), labelled "factorisation (≥ R08)". The in-figure text adds "factorisation ≡ B1 direct at R01–R07 (not drawn)". The sidecar lists the drawn rungs and the equal rungs. FIGURES_FINAL §D4 is updated. |
| **B6** EXTERNAL_BOUNDS.md stale | RESOLVED | l.7 now points to `figures/final/D7_exclusion_map`, with no stamp; the placeholder version is marked superseded. Caveat 1 says "final D7 grid (C12FC_v1, A2 E points)" instead of "C1 placeholder grid". The data are unchanged. |

## Category C

| finding | resolution |
|---|---|
| C1 D5/D6 empty decades | RESOLVED. A new `log_frame()` keeps the data in the middle of the axes: the bottom 25 % holds the text and the top 32 % the legend. This removes about 4–6 empty decades. All 11 PNGs were checked: no text or legend overlaps (an intermediate fixed-factor version hit the N_exp line in D5_F1500 and was replaced). |
| C2 −2σ edge below N_exp / σ_th | RESOLVED (doc). FIGURES_FINAL §D5 and §D6 now state that this is not an expected exclusion, since the median stays ≥ 37.6×. |
| C3 Python bool in the D4 text | RESOLVED. It now reads "trend significant: yes". |
| C4 D10 right label | No change (acceptable under the approved convention, per the reviewer). |
| C5 "CMS … recast" in the D7 text | RESOLVED. The display names are now "Farina-Low HSCP recast", "monojet recast" and "Evans-Luty out-of-time recast" (`EXT_DISPLAY`). The JSON labels are unchanged. |
| C6 T1_F_m200 Δs_B absent at ≥ 7 keV | RESOLVED (doc). One line was added to the truth table in FIGURES_FINAL. |
| C7 D2 lower empty decades | No change (harmless, per the reviewer). The space holds the in-figure text. |
| C8 "PRL 2026" unconfirmed | RESOLVED. EXTERNAL_BOUNDS.md now cites "arXiv:2607.26195 (e-print; journal reference not checked)". `external_bounds.json` never carried the journal reference. |
| C9 truth right label | No change (user decision pending). The √s-only variant exists. |

## Other changes

- **`--only` partial runs keep `index.json` complete.** Before, `--only` overwrote `index.json` with only the subset. It now
  merges the subset into the existing entries, so `index.json` lists all 11 ids after this partial regeneration.
- **Lint recount.** The FIGURES_FINAL lint paragraph is corrected. The 8 hits are: 6 `ax.text` calls in helpers, 1
  exp_label heuristic, and 1 false-positive "bare underscore" from the f-string field `{lammax_a2:g}`. This false positive was
  already present before the fixes. The old paragraph said "7 ax.text".

## Issue for Stage 4 (frozen code, not edited)

`acts/stage4/analysis/products.py` l.205–206 looks up `dj['tr']['trials_phimet']`. The `tr` dict from
`background.to_g3_job()` (l.33–41) uses unprefixed keys, and `TR_KEYS` omits `phimet`. As a result, `event_display.npz`
always has `pu_fake.met_phi = null`. The bug is cosmetic. It is recorded in FIGURES_FINAL.md under "Issues for Stage 4"
and should also go in the Stage-4 report.
