# Status — quirks v2

**2026-11-17 17:40 -05 (measured), day 1.** Phase 2 (Exploration) running. **Waiting for the user:** nothing urgent; two
small choices (trigger turn-on uncertainty; a thickness-law diagnostic) come with a recommendation before the selection
freeze. Daily report: `daily/2026-11-17.pdf`. Notices: `notices/`. The orchestrator session is being replaced
(restart instructions at the top of `ORCHESTRATOR_STATE.md`).

| | |
|---|---|
| Approved schedule | 4,609 CPU-h, stop-and-ask at 5,992, about 60 days (Gate A, 16 Nov) |
| CPU-h used | 228 (ledger, 1,611 jobs; VERIFIED): reproduction 110, theory 38, pilot channel 13, pilot 67 |
| Projected total | 4,663–4,844 CPU-h (ESTIMATE) + 22–28 for the robustness test D2; redone at the day-5 checkpoint |
| cajuela, this project | 127 GB of 1.5 TB |
| cajuela pool free | 3.8 TB of 4.5 TB |
| last repo bundle | `repo-2026-11-17.bundle` |

**Running:** pilot part 1 (242 of 500 jobs, none failed, ends about 18 Nov 20:00); pilot part 2 (single-interaction
samples, 128 of 762 jobs, none failed); v1 reproduction campaigns (all by about 19 Nov midday); compile jobs of the
generator comparison.

**Decided today by the user:** addendum 1 (D1–D9 as recommended); amendments E1–E3 (three Gate-A criteria failed as
frozen; the FAIL verdicts stay on record); exception to the 30-minute rule for the generator comparison; Opus
orchestrator with Fable on call, one session per phase (V16).

**Results today:** f₂₀₀ within 1.5 % of v1 at five points (0.0484 / 0.1041 / 0.1480 / 0.1676; scalar 0.1142; VERIFIED);
cross-section tables with resummed ratio 0.971–1.000; theory channel finished except the generator comparison.

**Open problems:** stitching cross-check of the inclusive sample not read (20k reading: 12 % excess at 200 GeV, 2.3σ);
restricted scan of amendment E2 not run; robustness test D2 not started; jet-response tail not sourced.

**Reach (ESTIMATE):** Gate A expected below 243 GeV (existing bounds about 180 GeV); nothing measured tests it yet;
the findings since Gate A point down. Upside 514–584 GeV. A pause at day 15 remains expected.

**Limits in force:** 10 GB cap, nothing heavy on einstein, one pixi install at a time, never rename a directory on
cajuela, pushes only of `v2-jfc` for daily reports and notices, never forced.

**Next interventions:** restart the session (tonight); 21 Nov (day 5) only if the reproduction fails or the stop rule
fires; 23 Nov (day 7) preliminary projection; 1 Dec (day 15) binding projection, pause expected.
