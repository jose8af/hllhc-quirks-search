# Status — quirks v2

**2026-11-16 19:18 -05 (measured), day 0.** Phase 2 (Exploration) running. **Waiting for the user:** approval of strategy
addendum 1 (decisions D1–D9) by 18 November about 14:00; an exception to the 30-minute job rule for one generator
comparison (not urgent). Daily report: `daily/2026-11-16.pdf`. Notices: `notices/`.

| | |
|---|---|
| Approved schedule | 4,609 CPU-h, stop-and-ask at 5,992, about 60 days (Gate A, 16 Nov) |
| CPU-h used | 53.3 (ledger, 643 jobs) |
| Projected total | 4,663–4,844 CPU-h (ESTIMATE; holds if the faster toy configuration is confirmed on a real workspace) |
| Reported overruns | pilot 142 CPU-h against 54.5 budgeted |
| cajuela, this project | 25 GB of 1.5 TB; projected about 515 GB |
| cajuela pool free | 3.9 TB of 4.5 TB |
| last repo bundle | `repo-2026-11-16.bundle` (refreshed with the daily report) |

**Running:** pilot part 1 (minimum-bias pool + Z(νν), 2 lanes on schrodinger, 25 of 500 jobs done, none failed, ends
about 18 Nov 16:15); v1 reproduction campaigns (landau, maxwell); theory inputs; preparation of the
single-interaction pilot samples (not launched).

**Main findings today:** the v1 fast simulation records no hit beyond half a turn (25.2 % / 37.5 % of hits missing
in Z(νν) / pile-up events); Geant4 gives 3.66×10⁸ single-interaction vertices against 6.8×10⁷ assumed; hard-scatter
events cost 0.13–0.57 s against the guessed 0.045 s; toys fit the budget with a gradient backend up to about 80 fit
parameters; the NLO calculation passes its three validations.

**Day-15 outlook (ESTIMATE):** an empty pilot reads 161 (R09 candidate) and 238–284 (R08) against the threshold 300;
the pause remains expected. Upside reach 514–584 GeV (790 at Gate A).

**Open problems:** likelihood check against v1's limit not passing yet (ratio 1.05–1.16; different test statistic
in v1); a slow-fragment artefact holds the nuclear-interaction samples; jet-response tail not sourced.

**Limits in force:** 10 GB cap, nothing heavy on einstein, one pixi install at a time, never rename a directory on
cajuela, pushes only of `v2-jfc` for daily reports and notices, never forced.

**Next interventions:** 18 Nov 14:00 addendum decisions; 21 Nov (day 5) only if the reproduction fails or the stop
rule fires; 1 Dec (day 15) binding projection, pause expected.
