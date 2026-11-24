# P3-C plot validation (Zakarias, 1-bot review, plot validator)

Scope: `phase3_selection/src/p3c/` (all subdirectories; no subdirectories exist) and `outputs/figures/p3c_*.png/.pdf`.
Only `p3c_plots.py` makes figures (the other files in `src/p3c/` contain no matplotlib or savefig calls; confirmed by grep).

## Part 1: code linter

`conventions/lint_plots.py` scans only `*/src/*.py`, so it found nothing on `src/p3c` directly ("No plotting scripts found").
I ran it on a copy of `p3c_plots.py` placed under a `<dir>/src/` layout (scratchpad). Result: 2 reports, both FALSE POSITIVES
("Missing PDF save", "Missing PNG save", line 0): `save()` (lines 26-29) loops `for ext in ('pdf','png')` with an f-string name, which the regex cannot see.
Both formats are saved with `bbox_inches='tight', dpi=200, transparent=True`, then `plt.close(fig)`.

Manual checklist on `p3c_plots.py`:
- PASS: `mh.style.use('CMS')`; `figsize=(10,10)` everywhere; no `set_title`; no colorbar; no numeric fontsize (only `'x-small'`);
  no `ax.text/annotate`; ratio plot has `sharex=True`, `subplots_adjust(hspace=0)`, `exp_label` on the main axes only.
- PASS (study override): label is `exp=''`, `llabel='Private work (simulation)'`, `rlabel='14 TeV'`, `data=True`; no CMS name. The template's "Open Simulation" rule is replaced.
- PASS: error bars are explicit `yerr` (`0.2*ref`, `0.2`, `0.5`); `mh.histplot` is called on model arrays (step style, no sqrt(N) bars).
- WARNING (B), lines 48, 79, 94: legends use no `mpl_magic` and no `loc=` (default "best"). Rendered results are checked below; none overlaps data on ntrig or multijet.
- WARNING (B), line 77: x tick labels are built with `v.replace('_',' ')`, so code identifiers become abbreviated words ("jes up", "dn", "lost e kept"), which is not publication wording.
- WARNING (B), lines 68-80: `fig_var` has no `set_xlabel`, so the x-axis has no axis label.
- WARNING (B), lines 68-95: `fig_var` and `fig_mj` plot yields and ratios derived from weighted samples with no statistical uncertainty.

## Part 2: visual validation (every PNG read)

All four figures: label "Private work (simulation)" present, no CMS name or logo, no "Axis 0" artifact, no titles, no offset text, text legible at 0.45 linewidth. Captions have at least 2 sentences.

1. `p3c_met_rms_ttbar`: PASS. Legend sits in empty space above the curves and does not touch data or curves. Axis labels carry units. The y-label is long but fits.
2. `p3c_met_shape_zmm`: VIOLATION (layout, clipped content, Category A). In the ratio panel the red curve (soft-term 25 GeV) drops below the y-limit 0.3 from about 90 GeV and the blue curve touches or leaves the bottom near 108 GeV, so the sharpest failures are not visible. Fix: widen `rax.set_ylim` (for example 0.05-3, or a log ratio axis) or draw clip markers. WARNING (B): the legend (default loc, lower left) ends within a few pixels of the red and orange tail histograms at the right edge of the legend box. Fix: `loc='lower left'` with `ncol` or a shorter legend, or extend the y-range downward.
3. `p3c_multijet_pthat`: PASS with WARNINGs (B). Legend at upper right is in empty space. (a) No statistical uncertainty is drawn, yet the caption says the two samples agree "within their statistics"; the orange step hides the blue. Add `yerr` bands or a ratio panel. (b) The y-label ("multijet cross section after the preselection per bin [pb]") is longer than the axes height and runs below the x-axis line. Shorten it. (c) The 10^3 axis has no intermediate tick labels (cosmetic).
4. `p3c_ntrig_variations`: VIOLATION (label quality, Category A). There is no x-axis label, and the tick labels ("jes up", "dn", "soft mix", "lost e kept", "all up") are code-derived abbreviations that the reader must decode from the caption. Fix: `set_xlabel('Declared variation')` and spell out the tick labels ("JES up", "soft term down", "lost electron kept"). WARNING (B): no error bars on the ratios; the multijet points that move by 11-60 are tail-dominated, so their statistical size is what a reader needs. Legend (upper left) does not overlap any point.

## Verdict summary
- p3c_met_rms_ttbar: PASS
- p3c_met_shape_zmm: VIOLATION A (clipped ratio panel), WARNING B (legend proximity)
- p3c_multijet_pthat: PASS with B warnings (no stat uncertainty; long y-label)
- p3c_ntrig_variations: VIOLATION A (missing x label, code-derived tick labels), WARNING B (no error bars)
- Code: no red flags; lint script false positives only.
