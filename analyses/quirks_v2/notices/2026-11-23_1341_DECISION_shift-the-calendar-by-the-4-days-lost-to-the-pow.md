# [DECISION] Shift the calendar by the 4 days lost to the power loss? (default C by Wed 25 Nov 12:00)

Written 2026-11-23 13:41 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

Written 2026-11-23 by the orchestrator. **Your answer is needed by Wed 25 Nov 12:00.** If no answer arrives by then, option C applies, labelled "default, user absent". Work continues unchanged meanwhile: every option runs the same next tasks.

**Why.** The power loss of 19–23 Nov (separate PROBLEM notice) stopped all work for **3.8 calendar days** (19 Nov 17:54 – 23 Nov 13:25; VERIFIED, `LOG.md`). The study's dates are calendar offsets from Gate A (day 0 = 16 Nov). They are a schedule, not frozen criteria (strategy l.2575, l.2607). The frozen text already lets the calendar "move day for day" after a delay (written for a C1 remediation, l.2612-2613; applied here by analogy) and says "the freeze moves; user informed" (l.2718). **No frozen criterion, limit or rule text changes under any option; only dates.**

**Budget check first (stop-rule checkpoint 1, done today).** No stop rule is near.
- CPU used: 431.6 CPU-h (VERIFIED, ledger markers).
- Projected total: about 4,600 CPU-h, band 4,070–5,050 (ESTIMATE), against the approved 4,609 and the stop-and-ask threshold of 5,992. The top of the band is 9.6 % above the approved figure: that would be a reported overrun, not a stop.
- Storage: 266 GB now, about 0.68 TB projected (ESTIMATE), against the 1.5 TB budget.
- Details: `phase2_exploration/outputs/CHECKPOINT1_leif_2026-11-23.md`.

**Options:**

| | Option | Day-15 binding reading | Freeze | Gate B | Gate C |
|---|---|---|---|---|---|
| A | Shift every later date by 4 days | Sat 5 Dec | 7–9 Dec | ≈ 8–10 Jan | ≈ 17–19 Jan |
| B | Keep the dates, compress the work | Tue 1 Dec | 3–5 Dec | ≈ 4–6 Jan | ≈ 13–15 Jan |
| **C (recommended)** | **A plus two riders** (below) | Sat 5 Dec at the latest | after your pause answer | ≈ 8–10 Jan | ≈ 17–19 Jan |

All dates in the table are ESTIMATE.

Riders of C:
1. Day 15 falls on a Saturday. Tell us whether you will answer the expected pause that weekend or on **Mon 7 Dec**; the freeze follows your answer.
2. The binding rule-1 reading is made as soon as all its listed inputs exist, and no later than 5 Dec.

Also: production would run about 11–25 Dec, and Gate B falls on about 8–10 Jan (ESTIMATE). Tell us if you are unavailable over the holidays.

**What each option costs:**
- **A / C:** the approved 60 days become **about 64** (ESTIMATE). That is an overrun reported in STATUS.md and the gate packages, not a stop rule. If production runs at the utilisation measured in Phase 2 (0.58) instead of the planned 0.75, it would be about 68 days (ESTIMATE).
- **B:** about 10 planned days of Phase-3 inputs for rule 1 would have to fit into about 8 (ESTIMATE). These are the occupancy-model inputs, the MET model at day 12, open retrievals and the D2 test. If they are not ready by 1 Dec, the reading would have to use stand-in inputs, which would reword a frozen rule and need an amendment. B gains 4 days against no hard deadline.

**For context:** the day-15 reading is expected to give a pause (pause expected, not decided). The present reading is PRELIMINARY, not binding: B₅₀(R09) = 10,777, near-pass inclusive. The count behind it is a lower bound on the rule-1 reading, valid only for an "above 300" verdict; the validation (a)–(e) is not complete. The rule-1 reading itself is a ceiling on the background, not a background estimate.

**Reach outlook vs the last report: equally promising.** No new background or reach number has been computed since 19 Nov (ESTIMATE, v1 placeholder efficiencies; no v2 signal efficiency looked at).

**How to answer:** reply in the Claude Code session with "C", "A", "B" or your own variant, and say whether you will answer the pause on the 5–6 Dec weekend or on Mon 7 Dec.
