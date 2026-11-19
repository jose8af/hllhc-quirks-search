# [DECISION] Two small choices before the freeze: trigger turn-on uncertainty, thickness-law record (reply by Mon 23 Nov)

Written 2026-11-19 11:15 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

# Two small choices before the selection freeze: trigger turn-on uncertainty and the thickness-law record (reply by Mon 23 Nov 12:00)

Both were announced in the daily reports of 17 and 18 Nov. An independent advisor checked both recommendations
(LOG.md, 19 Nov). Neither choice touches the day-15 rule. Defaults are my recommendation.

## 1. Uncertainty of the trigger turn-on (S2-e)
The public trigger curve was found, but it states no uncertainty. At the selection threshold MET > 250 GeV it
reads 0.975, the same as v1's 0.974. Caveats: it is a Level-1 curve only, plotted against generator-level MET in
tt̄ events, and it does not treat quirk tracks.

- **(a)** A nuisance from the curve's error bars. Not recommended: the bars are statistical only and cover none
  of the caveats above.
- **(b)** A wide nuisance, threshold kept at 250 GeV. **Default.**
- **(c)** Raise the threshold to 275–300 GeV. Not recommended: the frozen text allows a raise only if the curve
  reaches its plateau above 250 GeV, and it does not. A raise would also cut signal where the reach is expected
  (below 243 GeV).

If (b), you also choose the size:
- **−10.6 % absolute efficiency** at 250 GeV, from the public table's turn-on (width 56 GeV). **Default.**
  The same nuisance is −4.9 % at 275 GeV and −1.9 % at 300 GeV.
- **About −6 %**, if the frozen wording "the v1 function" is read literally (width 20 GeV). This figure is the
  advisor's arithmetic, not from a source.

Option (b) combines two branches of the frozen text (the sourced curve, with a size that is not sourced). It is
recorded as a clarification before any efficiency is computed. No one has computed its effect on the reach yet.

## 2. Thickness-law diagnostic (P1)
v1 quoted a numerical precision of "44 bits". That is in fact a coarser precision (512u) than v1 meant (64u,
47 bits). The pre-declared test, run at 44 bits, read "not the floor pattern", and that verdict stays as recorded.

At 47 bits, a diagnostic on 40 events per point does not exclude the floor pattern (KS p = 0.53 and 0.47).

**Default: record the diagnostic beside the verdict, labelled "diagnostic, not a pre-declared test".**
The alternative is to leave it out.

Caveats:
- Floor test 1 was never run, so P1-a is incomplete; the diagnostic does not replace it.
- The diagnostic's medians are 1.3–1.4 times the nominal value, against 1.0 expected.
- P1-c remains a FAIL.
- P1 is not needed by the search.

**Correction.** The daily report of 17 Nov said the floor pattern "reappears (verified)". That overstates it.
The correct reading is "not excluded at the precision v1 meant (diagnostic)".

**If I hear nothing**, the defaults are used at the freeze, and the choice is labelled "default, no answer".
