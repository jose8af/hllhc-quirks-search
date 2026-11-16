# [DECISION] Approve strategy addendum 1 (D1-D9) by 18 Nov 14:00

Written 2026-11-16 18:33 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Your approval is needed for the strategy addendum.** It changes numbers you froze at Gate A and defines the
single-interaction pilot samples. **Deadline: 18 November, about 14:00**, so those samples can start when the Z(νν)
pilot frees the node (about 16:15) and finish before day 5 (21 November).

You can answer "D1–D9 as recommended", or list the ones you change.

Document: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` (its §0 is written for you).

## Review status, as it is

Three independent reviews, each ITERATE: 3 must-resolve / 10 must-fix, then 2 / 5, then 0 / 4. The third gave
exact replacement texts and said no further review of the text is needed. Those texts were applied and a fresh
mechanical check passed. The gate's three-round limit is reached, so this comes to you without a formal PASS of a
content review. The last reviewer recomputed 42 numbers with its own code; all reproduce.

## What changed since Gate A (estimates on v1 placeholder efficiencies)

| | Gate A | Now |
|---|---|---|
| Curling particles simulated? | assumed yes | no hit beyond half a turn; 25 % (Z(νν)) and 37 % (pile-up) of hits missing |
| Decay and interaction vertices in the dataset | 6.8×10⁷, 4 terms | 3.66×10⁸, 7 terms |
| Empty pilot reads, R09 candidate (pause above 300) | 76 | 161 |
| Empty pilot reads, R08 candidate | 156–204 | 238–284 |
| Pause at Z(νν) pilot counts (R09 / R08) | 12 / 6–8 | 4 / 1–2 |
| Pilot cost | 54.5 CPU-h, 52 GB | 142 CPU-h, 167 GB (95 CPU-h running) |
| Summed pool floor at the fixed budget | 12.6 events | 201 as timed; 121 with two cost measures |
| Upside reach, all ceilings empty | 790 GeV | 514–584 GeV |
| Projected total (stop-and-ask 5,992) | 4,609 CPU-h | 4,663–4,844 CPU-h |

The expected outcome is unchanged: a pause at day 15 with a background of about 10⁴ events.

## Decisions

| # | Decision | Recommended | Main alternative |
|---|---|---|---|
| D1 | Half-turn limit | Keep the chain (your option B), state it as a limitation. The looper test found 0 candidates in 2×10⁵ single loopers, but that zero still allows 2.2×10⁴ events and does not test a looper together with pile-up | Fix the chain: days of work, every sample regenerated |
| D2 | Pile-up robustness test | Accept: 600 pile-up events with the later arcs restored, 22–28 CPU-h, before the freeze. A measured increase enters the binding day-15 reading | Decline: the pile-up effect stays unmeasured and the paper says so |
| D3 | Single-interaction pilot sizes | As proposed, 47 CPU-h, ends about 19 Nov | The strategy's original sizes (24 CPU-h) pause on an empty pilot |
| D4 | Number of background terms | Seven, following the strategy's one-floor-per-term convention | Fewer terms on the same events read 65–99 instead of 161, but reopen a design frozen at Gate A |
| D5 | Hard-scatter parents | One sample of 2×10⁶ vertices read as one term, 4 CPU-h. This is 24 events more lenient than the literal reading | Literal reading: an empty pilot reads 307 at the upper R08 estimate |
| D6 | Three unread populations (0.3–0.5 GeV; pseudorapidity 1–1.5; off-road hard-scatter hadrons) | State them as untested, with an alarm sample only. They could under-read this background by up to about 3 | Read them as terms: +15 to +35 CPU-h, and an empty pilot reads 309 at the upper R08 estimate |
| D7 | Pool | Confirm your fixed-budget decision at the corrected floor (201 / 121 events; reach 514–584 GeV) | Add CPU: 1,094–1,984 CPU-h for a floor of 39 |
| D8 | R08 candidates pause on 1–3 counts | Accept; decide a Z(νν) top-up at day 7 from the first counts | Enlarge now: +45 or +109 CPU-h |
| D9 | Hit hand-over per vertex class | Approve. The nuclear-interaction samples are released only after a slow-fragment artefact (1 event in 25,000) is settled; a change of the speed cut comes back to you | — |

D10 (toys) is for information: a faster fitting backend brings them to 47–228 CPU-h at 60–100 fit parameters,
against 183 budgeted, to be re-measured on the first real workspace.

With D1 you also approve two changes to items frozen at Gate A: an added paper-correction item (v1's looper bound
measured nothing), and looper overlays made from Geant4 trajectories.

## Status tonight

- Z(νν) pilot and minimum-bias pool: running since 16:39, no failed job, first files validated.
- Theory inputs: the NLO calculation passes its three validations.
- v1 reproduction: campaigns running, no verdict yet.
