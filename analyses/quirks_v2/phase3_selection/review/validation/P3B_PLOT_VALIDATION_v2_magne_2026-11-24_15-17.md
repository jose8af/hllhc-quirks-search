# P3B plot validation, cycle 2 (Magne, fresh validator), 2026-11-24 15:17

Scope: `src/p3b/plots.py` (the only matplotlib user in `src/p3b/`; grep for savefig/pyplot over all subdirectories finds nothing else), figures `outputs/figures/b2_dev_{lnr,rates,neff}.{png,pdf}` (all six files exist, written 15:14, newer than plots.py 14:55), captions in `outputs/P3B_PILEUP_v2_ivar_2026-11-24.md` §9. All three PNGs were read.

## Part 1: code linter
`conventions/lint_plots.py` `lint_file()` run explicitly (nice -n 19, python3 -I) on `src/p3b/` (20 .py files: 0 violations), `src/p3b/campaigns/` and `campaigns/prod/` (0 .py files; JSON only). Manual checklist on plots.py: mplhep CMS style (l.150); figsize (10, 10) x3; no set_title; no numeric fontsize (only 'x-small'); bbox_inches tight, dpi 200, transparent, PDF + PNG (l.33-34); plt.close (l.35); no colorbar; no `.view()[:]=`; explicit yerr on every errorbar; `data=True` with llabel (l.28); label "Private work (simulation)", exp='' so no CMS name (matches STUDY OVERRIDES); x and y labels on all three; no code identifiers in labels (ticklabel() maps 'x' to ⊗ and '>=' to ≥). Legends are fixed `loc=` in empty regions (verified on the renders); no mpl_magic, acceptable under the "genuinely empty region" clause. No violations.

## Part 2: figures
- **b2_dev_lnr: PASS.** x label present. Both R07 points and all error bars are inside the frame (open markers, bars to about 1.85 and 1.75). Legend (lower left, 2 columns) sits in the empty band y < -0.5, no overlap with data or with the -ln 1.5 line. Text legible, no collision between "Private work (simulation)" and "PU 200". Error bars plausible. Filled/open distinction in the legend. WARNING (C): the top 0.35 of the y axis is empty headroom; tick label notation (⊗, 2S≥j, p>P) is defined in the §9 notation paragraph, not on the figure.
- **b2_dev_rates: PASS.** Legend is in the empty lower left, inside the frame (no spill onto the y label or tick labels, no overlap with the R04-R09 points or the dashed line). x label present. Error bars sensible (Poisson, bootstrap, asymmetric width bars). R08 diamond now has an error bar; R09 has orange and red points with bars. WARNING (C): ylim 1e-11 to 1e5 leaves about two empty decades above 1e3; could be tightened to about 1e4. "96,000 trials" in the legend is consistent with the note (§0.x, l.356) and the caption (485 events at N_trig).
- **b2_dev_neff: PASS.** x label present. Legend (upper right) in empty region above all data, no overlap. Rotated tick labels legible, not clipped. No error bars; the caption now states why. WARNING (C): ylim 1 to 1e7 leaves three empty decades above the data (max about 2e4); could be 1 to 1e5 with the legend placed accordingly.

## Cycle-1 items (Elias)
1. Missing x-axis labels (all three, A): RESOLVED (plots.py l.77, 115, 139; visible in renders).
2. rates legend overlap with tick label, y label and R04 data (A): RESOLVED (legend lower left, inside frame, shortened entries).
3. neff legend crowding R07 data (A): RESOLVED (upper right, empty).
4. lnr R07 points clipped with no marker (A): RESOLVED (ylim widened, markers and bars inside frame).
5. Undefined notation ⊗, 2S≥n, p> (B): RESOLVED in the caption (notation paragraph at the top of §9).
6. lnr occupancy-model squares absent at p-threshold rungs, not stated (B): RESOLVED (caption sentence).
7. rates R08 diamond without error bar; R09 explanation (B): RESOLVED (bars drawn on both occupancy readings; caption explains the no-credit value and R09).
8. neff: no error bars, caption silent (C): RESOLVED (caption sentence).
9. neff x order / "B2-b", "day-15" undefined (B/C): RESOLVED in caption ("reading (i)/(ii)", B2-b defined in the rates caption).
10. mpl_magic absent (root cause): RESOLVED in effect; legends placed in verified empty regions.
11. lint_plots.py not covering src/p3b/ (process): RESOLVED here by explicit per-directory run; the glob limit itself is unchanged (tools/jfc read-only; flagged by Ivar).

## Verdict
No RED FLAG, no Category A or B violation. Three Category C warnings (excess headroom on ylim in all three figures; notation defined in the caption rather than on the figure). All three figures PASS.
