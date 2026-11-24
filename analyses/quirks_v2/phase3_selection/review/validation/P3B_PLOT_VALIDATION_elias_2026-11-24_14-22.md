# P3B plot validation (Elias, 1-bot review of p3-b B2 development figures), 2026-11-24

Scope: `phase3_selection/src/p3b/plots.py`; `outputs/figures/b2_dev_{lnr,rates,neff}.{png,pdf}`; captions in `outputs/P3B_PILEUP_casper_2026-11-24.md` §9. All three PNGs were read. PDFs exist for all three (listing checked).

## Part 1: code linter
`conventions/lint_plots.py` was run with `nice -n 19 python3 -I`; it reported "No plotting scripts found" because it only globs `*/src/*.py` and `plots.py` sits at `phase3_selection/src/p3b/` (one level deeper). The checklist was therefore applied by grep and reading (plots.py:1-134).

PASS: `mh.style.use('CMS')` (l.126); `figsize=(10, 10)` on all three; no `set_title`; no numeric fontsize (only `'x-small'`); `bbox_inches='tight'`, dpi 200, transparent, PDF and PNG (l.28-29); `plt.close(fig)` (l.30); no colorbar; no `.view()[:]=`; `data=True` with llabel (l.22). The label reads "Private work (simulation)" with `exp=''`, so no CMS name, which matches the STUDY OVERRIDES. Axis labels contain no code identifiers. The y-axis labels are dimensionless or counts, so no units are needed.

Violations:
- plots.py:63,97,118 (all three figures): no `ax.set_xlabel(...)`. The x axis is categorical, but it has no label. VIOLATION (A). Fix: add "Rung / crossing rung" (lnr, neff) and "Rung" (rates).
- plots.py:97 and 118: `loc='upper right'` and the default `loc` are used on populated axes without `mpl_magic(ax)`. The rendered figures confirm real overlap (see below). VIOLATION (A). plots.py:63 (`lower left`) is in genuinely empty space, so it is acceptable.
- plots.py:10 area: no `mpl_magic` import anywhere. This is the root cause of the two items above.
- WARNING (B): `exp=''` with `llabel` is acceptable under the override. The "PU 200" rlabel is fine.

## Part 2: visual validation

### b2_dev_lnr.png: VIOLATIONS
- Missing x-axis label (see above). VIOLATION (A).
- Legend: lower left, empty region, no overlap with data. PASS.
- Clipped content: both R07 points sit above the frame (ylim 1.2) and show only as truncated error-bar stubs at the top edge, with no marker. The reader cannot tell what they are. The caption notes it, but the figure itself does not. VIOLATION (A). Fix: draw up-arrow markers at the frame top annotated "R07: 7 direct counts", or widen the y range or use a broken axis.
- Tick labels such as `R05⊗p>0.001` use an undefined "p" (fit probability?). Neither the caption nor the axis defines "⊗", "2S≥n" or "p". WARNING (B). Fix: define them in the caption or the labels, e.g. "R05 ⊗ fit-prob. > 0.001".
- The occupancy-model squares are absent for the p-threshold rungs. Not stated in the caption. WARNING (B).
- Text legible, error-bar magnitudes plausible (they scale with the Poisson and bootstrap errors), no label collision. PASS on those checks.

### b2_dev_rates.png: RED-FLAG-class overlap
- Legend overlap. VIOLATION (A, mandatory fix). The four-line legend is wider than the axes. Its markers spill left of the frame onto the y-axis label "pile-up groups per trial" and the "10^4" tick label. Its text collides with the 10^4 tick label ("direct count" over "10^4"). The fourth legend row ("occupancy model, day-15 scale ...") sits at y ≈ 10^2 and overlaps the R04 data markers (black, blue, orange and red points). Fix: shorten the legend entries, use `loc='lower left'` (empty region below the falling spectrum) or raise the ylim top and call `mpl_magic`, and put the long explanation in the caption.
- Missing x-axis label. VIOLATION (A).
- The R08 red diamond has no error bar and R09 shows only the orange point. The caption explains R09 but not the missing diamond error bars. WARNING (B).
- The direct-count error bars are barely visible. Plausible for Poisson errors at high counts. PASS.

### b2_dev_neff.png: VIOLATIONS
- Legend placed in the data region (the default loc lands between R04-R07 at N_eff ~ 10^2-10^3). Its third row ("N_eff for s_P = ln 1.5/3 alone") extends toward the R07 points. The filled R07 marker at about 2×10^2 sits within the legend's text band, and the open R07 marker is directly above its first row. Visible crowding and partial overlap. VIOLATION (A). Fix: `loc='lower right'` or `'upper right'` with `mpl_magic`, or the empty band below the dashed line.
- Missing x-axis label. VIOLATION (A).
- Rotated tick labels ("R06⊗2S≥3", "R05⊗p>0.001") are legible but the undefined notation applies as above (WARNING B). The x order puts R05⊗p after R06⊗p without explanation. WARNING (C).
- No error bars on N_eff. Acceptable for a derived count; the caption should say so. WARNING (C).

## Captions (§9)
All three have 3 or more sentences, plot name first, and describe the symbols. Gaps: the notation ⊗, 2S≥n and p> is undefined (lnr, neff); the missing occupancy-model squares and the missing R08 error bars are not mentioned; the R07 statement "lie above the frame" is correct but should become an annotation on the figure. The rates caption's "B2-b" and "day-15" labels are not defined in the figure text. WARNING (B).

## Summary
| Figure | Verdict |
|---|---|
| b2_dev_lnr | FAIL: missing x label (A); R07 clipped with no marker (A); notation (B) |
| b2_dev_rates | FAIL: legend overlaps tick label, y-axis label and R04 data (A); missing x label (A) |
| b2_dev_neff | FAIL: legend crowds R07 data (A); missing x label (A) |

No RED FLAG in the strict sense (labels present, no "Axis 0" artifacts), but the rates legend overlap is a Category A overlap that the arbiter should not downgrade.
