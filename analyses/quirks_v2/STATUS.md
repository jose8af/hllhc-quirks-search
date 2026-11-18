# Status — quirks v2

**2026-11-18 18:55 -05 (measured), day 2.** Phase 2 (Exploration) running. **Waiting for the user:** nothing. Two
small choices (trigger turn-on uncertainty; a thickness-law diagnostic) come with recommendations at decision point 1
(21 Nov). Daily report: `daily/2026-11-18.pdf`. Notices: `notices/`.

| | |
|---|---|
| Approved schedule | 4,609 CPU-h, stop-and-ask at 5,992, about 60 days (Gate A, 16 Nov) |
| CPU-h used | 383 (ledger, 2,768 jobs; VERIFIED): reproduction 195, theory 39, pilot channel 13, pilot 136 |
| Projected total | 4,663–4,844 CPU-h (ESTIMATE) + 22–28 for the robustness test D2; redone at the day-5 checkpoint |
| cajuela, this project | 236 GB of 1.5 TB |
| cajuela pool free | 3.7 TB of 4.5 TB |
| last repo bundle | `repo-2026-11-18.bundle` |

**Running:** pilot part 1 (Z(νν) 457 of 460 jobs, none failed, ends about 20:00 tonight); pilot part 2 (664 of 762
jobs, none failed; hard-scatter block of 98 jobs next, through about 20 Nov); v1 reproduction (pile-up ρ = 1 173/200,
ends about 19 Nov 04:30; pile-up pairs 49/75, overnight). No agent running.

**Decided today by the user:** amendment E4 (event-level errors for the SM family; frozen FAIL stays on record).

**Results today:** B1 per-stream validation 8/8 pass (318 flagged events pilot-wide against "about 170" announced;
D9 stands); C1 rates 5/5 pass after a rerun; SM family PASS 3/3 under E4 (z ≤ +0.57, ≤ +0.82 with v1 error 0); E2
restricted scan fails (46/50, 46/50), first half stands alone; C2-b pass, C2-c pass without power; stitching ratio
1.0001 ± 0.0252 (no f₂₀₀ bias).

**Open problems:** coherence test of the pile-up and closure families treats nested rungs as independent (fix before
reading); robustness test D2 not started; jet-response tail not sourced.

**Reach (ESTIMATE):** Gate A expected below 243 GeV (existing bounds about 180 GeV); nothing measured tests it yet.
A pause at day 15 remains expected.

**Limits in force:** 10 GB cap, nothing heavy on einstein, one pixi install at a time, never rename a directory on
cajuela, pushes only of `v2-jfc` for daily reports and notices, never forced.

**Next interventions:** 21 Nov (day 5) decision point 1; 23 Nov (day 7) preliminary projection; 1 Dec (day 15)
binding projection, pause expected.
