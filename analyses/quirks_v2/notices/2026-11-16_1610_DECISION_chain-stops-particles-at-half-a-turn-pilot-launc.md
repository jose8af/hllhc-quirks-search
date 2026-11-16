# [DECISION] Chain stops particles at half a turn; pilot launch approvals needed

Written 2026-11-16 16:10 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Two things need you.** The first takes one line; the second is a real choice. Deadline: 17 November for both, to
keep day 5.

## 1. Approve the launch of the minimum-bias pool (10 CPU-h, generator level)

The session's permission system refused the executor's launch command, and I do not run a command on behalf of an
agent that was denied it. The campaign is tested and pre-flighted (0 failed checks). Either tell me "launch
pilot.mb", or run it yourself on einstein:

`bash /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/pilot/LAUNCH_p2-c-pilot_mb_1slots.sh`

## 2. The simulation chain stops every particle at half a turn (inherited from v1)

**Measured today (VERIFIED against Geant4; lower bounds):**

| per event | Z(νν), no pile-up | one minimum-bias interaction |
|---|---|---|
| hits written by the fast simulation | 833 | 244 |
| true crossings with no simulated hit | 209 (25 % of written) | 91 (37 %) |
| central charged particles below the looping threshold (0.63 GeV) | 48 % | 70 % |

- In the outer pixel-strip layers 34–58 % of the crossings are missing.
- 77 % of the particles that can loop are still alive after one full turn.
- Cause: the installed ACTS exposes no loop setting; the cut sits at exactly half a turn (inference: default loop
  protection). It can be changed only by rebuilding ACTS, not from configuration.
- v1 never mentions it. v1's looper test counted 0 of 10⁵, but a particle stopped at half a turn cannot cross a
  layer twice, so **that zero measured nothing**.

**Why it matters.** The signal is a thin plane with repeated crossings of the same layers. A low-momentum particle
that loops also crosses the same layers repeatedly. That background topology is absent from every v1 and v2 sample,
and the pile-up hit pattern lacks about a third of its correlated hits. Its size as a background is **unknown**.

**Options**

- **A. Fix the chain for all v2 samples** (rebuild ACTS on a worker, or re-fire particles in repeated passes).
  The v1 reproduction keeps v1's setting. Cost: a few days of development and validation (my estimate, not
  measured), at least 25–37 % more hits per event, a new budget projection, and the Z(νν) pilot waits.
- **B. Measure first (my recommendation).** Run a proper looper test now: Geant4 trajectories of low-momentum
  particles injected as hits, through the finder. A few CPU-h, about a day. Start the Z(νν) pilot today on the
  chain as it is. If loopers make candidates, go to A and regenerate the pilot (about 95 CPU-h lost, 2 % of the
  budget). If they do not, keep the chain and state the limitation with that measurement behind it.
- **C. Keep the chain and state it as a limitation**, with no measurement.

I have already ordered the looper test of option B, because it informs your choice in every case. What I need from
you is whether the Z(νν) pilot may start now on the present chain (B), or must wait (A).

**Also affected:** the strategy addendum. Two of its seven vertex classes come from particles that have curled
back, and no hit treatment passes for them on the present chain. Its third review waits for your choice.

Files: `phase2_exploration/outputs/HALF_TURN_xavier_2026-11-16_16-08.md`,
`phase2_exploration/outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md`, `LOG.md`.
