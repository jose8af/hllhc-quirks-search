# [RESULT] Reach re-estimate: no longer pinned below 243 GeV, but not shown above it (estimate, range < 243 to about 440 GeV)

Written 2026-11-23 16:38 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

No decision is needed. Everything here is an ESTIMATE; no v2 signal efficiency is used (the signal side is v1's
placeholder efficiencies, known to be about 15 % high), and no signal file was opened.

**What was done.** Gate A's reach calculation was re-run unchanged (it reproduces Gate A exactly, VERIFIED, Tora
`phase2_exploration/outputs/REACH_REEST_tora_2026-11-23.md`), with only the background inputs replaced by what Phase 2 measured.

**Result** (reach = mass up to which we expect to exclude; all ESTIMATE, same source):
- Gate A as before: background 6,800–10,200 events, reach below 243 GeV. This stays the upper envelope.
- Counting only conversion candidates that the frozen rule attributes to the conversion (6–9 % of v1's, VERIFIED
  counts 10/174 and 1/11, Eskil 19 Nov), with no SM event after track removal in the pilot (0 counts, VERIFIED read,
  Tove): background 420–920 events, reach 350–445 GeV. This is an optimistic edge, not a central value.
- Same, with the 17 near-complete SM pilot patterns left after track removal: reach about 277–296 GeV.
- At the upper limit of the attributed fraction (22 %) with the 11 SM pilot events before track removal: reach
  below 243 to 266 GeV.

**Why it is not firmer.** (1) The 6–9 % rests on a single simulated source event; 0 % and 22 % are both compatible.
(2) 60 % of v1's conversion candidates are "mixed" (partly conversion, partly pile-up hits; VERIFIED share, Eskil).
They are in no term here. If more than roughly 10–20 % of them survive the selection, the reach is back below about
250 GeV (ESTIMATE). Nothing measures this yet; the frozen completeness test is where it will be measured.

**Reach outlook vs last report: more promising, because** the part of the conversion background that is really made by
conversions is measured 11–17 times smaller than Gate A assumed; **but not established, because** the mixed candidates
and the one-event statistics leave "below 243 GeV" fully possible.

**Separate and unchanged:** the day-15 reading (about 10,800 events against the limit of 300; 63,170 with the stricter
classifier count, not yet reviewed) is a deliberately high ceiling, counted before track removal and including
near-complete patterns. It is not the background used above. The pause on day 15 is still expected.

**Next:** a row showing the reach against the surviving mixed fraction; review of the classifier (running). Details:
`LOG.md` 23 Nov. Wording checked by an advisor (Ulla) before sending.
