# [INFO] Addendum D9 update: slow-fragment artefact measured; pilot part 2 ready

Written 2026-11-16 20:28 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**No new decision.** This adds one fact to decision D9 of the addendum notice of 18:33, so you can answer both
together.

## The slow-fragment artefact is measured

- **What it is:** a slow proton or deuteron (speed 0.13–0.21 of light) born in an outer tracker layer gets
  simulated hits 12–35 ns before it is produced. It is an artefact of the fast simulation.
- **Rate (VERIFIED on test slices):** 4 events in 430,000, about 1 in 100,000. About 170 events expected in the
  17 million single-interaction pilot events (ESTIMATE).
- **Raising the speed cut does not remove it:** cuts of 0.1 / 0.15 / 0.2 / 0.3 leave 2 / 1 / 2 / 0 flagged events
  in 25,000, and the cut at 0.3 hands over 20 % fewer real products.

## What I propose under D9

Keep the speed cut at 0.1, as the addendum defines it. Every pilot file flags the affected events one by one.
"One validated job per sample" is then read as: all hard checks pass except the flagged events, whose rate is
reported. In Phase 3 the classification is done with and without them.

If you approve D9 as recommended, I take this reading unless you say otherwise.

## Second part of the pilot

The single-interaction campaigns are generated, tested on slices and pre-flighted: 762 jobs, 48 CPU-h, 91 GB, about
26 hours on two lanes (ESTIMATE). They are **not launched**; they wait for your answer to D1–D9.

File: `phase2_exploration/outputs/B1_READY_albert_2026-11-16_20-24.md`.
