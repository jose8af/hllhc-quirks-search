# [INFO] Day-0 status and decisions expected 17 Nov

Written 2026-11-16 14:28 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**No action needed today.** Decisions are expected from you on **17 November** (see the end).

## Where the study stands (day 0)

- Phase 1 review passed and Gate A was answered with all defaults: 4,609 CPU-h, stop-and-ask at 5,992.
- Phase 2 is running: v1 reproduction, theory inputs, pilot preparation.
- The CMS note you supplied gives a second pile-up-200 source, so the missing-momentum model can be validated
  independently. A non-Gaussian jet-response tail is still not sourced.

## What changed since Gate A (estimates, under review)

| | Gate A | Now |
|---|---|---|
| Hard-scatter event cost | 0.045 s (guess) | 0.13–0.57 s (measured) |
| Decay and interaction vertices in the dataset | 6.8×10⁷ | about 3.7×10⁸ (Geant4; curling particles and other layers) |
| Summed pool floor at the fixed budget | 12.6 events | 99–137 with a chain change, 175–213 without |
| Upside reach, all ceilings empty | 790 GeV | 506–597 GeV |
| Pilot cost | 54.5 CPU-h | about 131 CPU-h |
| Toys | 183 CPU-h | about 7,600 CPU-h at 60 fit parameters unless a remedy works |

- The floor I quoted when you chose to keep 4,609 CPU-h (36–60 events) was wrong.
- The expected outcome is unchanged: a pause at day 15 with a background of about 10⁴ events. Whether the larger
  vertex count changes that headline is one of the reviewer's questions.
- The pilot is **held**. The strategy addendum that redefines it was sent back once (3 must-resolve, 10 must-fix),
  was fixed, and is being re-reviewed.

## Decisions coming to you

1. Pilot size: at the planned sizes an empty pilot would already read above the pause threshold; larger samples
   cost about 76 CPU-h over budget.
2. Which vertex classes are terms of the day-15 rule (the addendum proposes all seven).
3. Whether your pool decision stands at the corrected floor, or CPU is added (about 1,950–2,400 CPU-h for the
   planned pool against 665).

Approval by 17 November keeps the pilot inside day 5 (21 November), with little margin.

Files: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v2_tatiana_2026-11-16_14-14.md`, `daily/phase1_report.pdf`, `LOG.md`.
