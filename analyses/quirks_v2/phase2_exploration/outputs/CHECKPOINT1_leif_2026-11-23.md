# Stop-rule checkpoint 1: CPU, wall clock, storage (Leif, 2026-11-23)

Checkpoint 1 of STR §11.6 (l.2689-2690; COM ST-1 l.257): re-project the study's CPU with measured unit costs and
measured utilisation. Due day 5 (Sat 21 Nov); done Mon 23 Nov 13:31–13:42 -0500 after the power loss of
19 Nov 17:55 – 23 Nov 13:25 (LOG l.984). Approved schedule 4,609 CPU-h, stop-and-ask above 5,992 CPU-h
(COM l.39, l.257; STR l.2525-2531).

**Verdict. No stop rule is near.** Projected total: **≈ 4,600 CPU-h central, band 4,070–5,050** (ESTIMATE, §3).
The top of the band is 940 CPU-h below 5,992 and 9.6 % above the approved 4,609. The calendar has slipped
**about 4 days**, all of it the power loss. Gate B moves to about 8–10 Jan and the projected calendar is about
64 days against the approved 60. That overrun is reported under D6; it is not a stop rule. Storage is 266 GB now
and about 0.68 TB projected, against 1.5 TB budgeted and the 2.0 TB stop. The pool has 3.7 TiB free.

Tags: **V** = VERIFIED (I measured or re-derived it; command or file given), **E** = ESTIMATE, **U** = UNVERIFIED
(transcribed). Script: `phase2_exploration/src/checkpoint1_ledger.py`. It uses only the standard library, runs on
einstein under `nice -n 19` in 0.3 s and is read-only.

## 1. CPU used so far

Source: every marker under `ledger/markers/` (3,135 Phase-2 jobs; `_driver/` skipped), read on 23 Nov at 13:31.
I did not rebuild `jobs.tsv`, for two reasons. It dates from 19 Nov 17:18, and it keeps only the **last** line of
each marker (`tools/runner/qv2run/ledger.py:32`), with one row per output file. The script sums the CPU of
**every** attempt.

Cross-check: `jobs.tsv` de-duplicated on (campaign, job_id, attempts) gives 428.0 CPU-h for 3,105 jobs. The
orchestrator logged 428.5 at 17:18 (LOG l.982). The markers give 431.3 on the last-line convention and **431.6**
counting all attempts [V].

| channel / item | campaigns | jobs | CPU-h [V] | Gate-A Phase-2 line (STR l.2507-2521; ADD l.692) |
|---|---|---|---|---|
| C1 reproduction (`p2-a-c1-*` without cppuni) | 15 | 714 | 186.3 | 198 |
| B2 day-0 measurements (`p2-a-day0-*`) | 4 | 9 | 0.95 | 10 (B2 Phase 2) |
| C′_PU NI attribution run (Eskil, `p2-a-c1-cppuni-*`; approved 19 Nov, limit 9) | 2 | 10 | 2.30 (running) | new |
| C2 (`p2-a-c2-*`) | 15 | 147 | 22.45 | 81 |
| S2 (`p2-b-s2*` without FxFx) | 12 | 113 | 28.49 | 88 with FxFx |
| S2 FxFx (`p2-b-s2-fxfx*`; E 1500 job grids4 running) | 8 | 20 | 3.26 in markers (+≈ 3.2 MG child CPU not in markers, Sune, LOG l.972 [U]) | 40 inside the 88 |
| P1 (`p2-b-p1-*`) | 5 | 49 | 6.39 | 51 |
| DP5 Herwig (`p2-b-hw-*`) | 2 | 32 | 3.21 | not itemised |
| Pilot part 1: minimum bias + Z(νν) | 17 | 500 | 94.05 | 95.3 (addendum) |
| Pilot part 2: seven B1 classes, hard scatter, low-p_T, Geant4 | 39 | 762 | 46.80 | 47.0 (addendum) |
| Pilot validation jobs | 6 | 15 | 0.03 | — |
| Pilot classification and rule-1 preliminary reading (Tove) | 3 | 64 | 9.14 | Phase-3 B1/B4 development (135) |
| Rule-1 validation (Cecilie; `p2-c-r1v-*`, running) + `p2-c-rule1*` | 10 | 58 | 2.58 | Phase-3 development |
| D2 robustness test (Ulrika; `p2-c-d2*`, running) | 6 | 68 | 12.04 | + 22–28 (ADD l.299) |
| Toys and T1 measurements (`p2-c-toy-*`, `t-pyhf`, `t1*`) | 17 | 99 | 4.09 | — |
| Channel (iii) development and timing (`px`, `pa`, `pa-lt`, `t-`, other) | 132 | 475 | 9.52 | 5 (development and timing) + 5 (B3) |
| **Phase 2 total** | **293** | **3,135** | **431.6** | Gate A 506; with the addendum pilot 594 |

The two Phase-1 feasibility campaigns (0.5 CPU-h) are not counted.

- **CPU used by Phase 2: 431.6 CPU-h** [V], plus about 3–5 CPU-h that no marker holds [E]. That is the MG child
  processes of the killed FxFx E 1500 run (about 3.2 [U]) and the 9 attempts the power loss interrupted, whose wall
  time up to 17:54:50 adds to 1.56 slot-h. That is an upper bound; its CPU was not recorded.
- **Waste:** failed, timed-out and killed attempts that did record CPU come to 2.56 CPU-h, or 0.6 % [V]. There were
  40 failed, 7 timed out and 9 killed.
- **By channel:**
  - (i) reproduction: C1 + C2 + day 0 + attribution = 212.0;
  - (ii) theory: S2 + FxFx + P1 + DP5 = 41.4;
  - (iii) pilot generation: 140.9;
  - (iii) everything else: 37.4 (classification 9.1, D2 12.0, validation 2.6, toys/T1 4.1, development 9.5).
- **The finished Phase-2 items came in about 150 CPU-h under their lines:** C1 −12, C2 −59 (22 of 81), P1 −45
  (6 of 51), FxFx ≈ −32 (about 8 of 40) and the pilot −1 (140.9 of 142.3). The S1 Stage-2 production (≈ 46 of
  S2's 88) is deferred to Phase 3, not saved (LOG l.377).

## 2. Measured unit costs against Gate A (Table 4.0, STR l.348-366)

All measured with `cpu_s` from the markers, on the i5-7500 workers at 2–4 jobs per node. Event counts come from the
`--n` / `--size` arguments in the campaign files (`tools/runner/campaigns/*.json`, `tools/runner/examples/*`).

| unit | Gate A (prov.) | measured | ratio | source [V unless marked] | CPU-h it carries after Phase 2 |
|---|---|---|---|---|---|
| ρ = 1 event, chain + 4 trials | 60.4 s (M) | **55.7 s** (4,000 events; first jobs 57–59) | 0.92 | p2-a-c1-pu1, 61.93 CPU-h; Rosalie §1 | B2 direct 403, development 100 |
| ρ = 2 event, 2 trials, pre-merge on | 206 s (D) | **203.1 s** (1,000 events) | 0.99 | p2-a-c1-pu2, 56.43 CPU-h | B2 ρ = 2 172 |
| PU-200 row with one trial (overlay, hit-level SM, signal row) | 25.2 s (D) | **24.0 / 24.8 s** C′_PU rows (5,000); **26.1 s** hit-level Z(νν) (2,000) | 0.95–1.04 | p2-a-c1-cppua/b 33.8 CPU-h; p2-a-c1-sm 14.5 CPU-h | ≈ 1,287 (S1 chain 561, hit level 524, overlays 123, B6 59, pilot near-pass 7, development overlays 7; C1's 63 is spent) |
| finder trial at road 0.15 | 11.7 s (M) | 11.27 ± 7.33 s | 0.96 | p2-a-day0-pu1 (`day0_measurements.json`) | B5 163 |
| no-pile-up hard-scatter event (Z(νν), generation + shower + chain + summary) | **45 ms (G)** | **132 ms** (2.3×10⁶ events) | **2.9** | pilot-znn-00…15, 84.4 CPU-h | none at fixed CPU: the pool keeps 457 + 208 CPU-h and loses events (user decision 16 Nov, COM l.44). The multijet (+15) and B6-c (+46) lines are already in the addendum's +190 |
| minimum bias at generator level, per interaction | 2.0–2.5 ms (M, Pythia only) | 3.5 ms incl. summary (10⁷) | 1.4–1.7 | p2-c-pilot-mb, 9.66 CPU-h | spent (pilot) |
| B1 pilot chain, seven classes | 23.8 CPU-h (ADD l.697) | 21.2 | 0.89 | p2-c-pilot-c0-* without hs, lowpt | spent |
| B1 pilot Geant4 passes | 18.4 CPU-h (ADD l.695) | **23.0** | **1.25** | p2-c-pilot-g4{a,n,h,l}* | Geant4 spectra/variations 67 (G); vertices 98 (D, inside the fixed pool) |
| pilot hard-scatter + low-p_T | 4.2 + 0.5 | 2.30 + 0.26 | 0.54 | p2-c-pilot-c0-hs, -lowpt | spent |
| Stage-3 string, E 500 at 3 keV | 18.8 s (D, toy kinematics) | **13.1 s** (500 events) | 0.70 | p2-a-c1-s3 | S1 Stage 3 266 + B6 36. The 5 keV anchor (67.8 s, 71 % of the 95.6 s sum) is not measured in Stage 3 |
| Stage-3, E 200 at 1.5 / 2 keV | (v1 index × 2.14 at F 500) | 2.03 / 4.57 s | — (other mass) | p2-a-c1-s3 | as above |
| MLM 0–2j LHE event + shower + conversion | 50 ms (G) | 39.7 ms (production), 46 ms (FSR off) | 0.79–0.92 | Edgar §5 l.539 [U]; Rosalie §1 [U] | S1 Stage 2 (1.25×10⁶ LHE), migration 5×10⁵ |
| re-shower + conversion, per event and variant | 21 ms (M, shower only) | 32 ms | 1.52 | Edgar l.541 [U] | four re-showers of the S1 Stage 2 |
| FxFx, two masses | 40 CPU-h (G) | ≈ 7–8 (E 500 done 4.5; E 1500 one job ≤ 2.0 at 7,200 s) | ≈ 0.2 | LOG l.980 [U]; markers | spent / running |
| V4-5 + T_seed (C2) | 74 (G) | C2 complete at 22.45 | — | p2-a-c2-* | spent |
| P1 paired test, 5 keV, 4 kernel runs | 2 × 67.8 s (D) | 23.8 s | 0.18 | Edgar l.354 [U] | spent |
| toys, 1000 + 1000, jax | 652 s (G) | 168 / 385 / 817 s at 60 / 80 / 100 parameters | — | ADD l.722-735 [U] | 47 / 108 / 228 against 183; not yet measured on a real v2 workspace |

The guessed costs that day 5 was meant to fix (STR l.2700-2703) now stand as follows.
- The 45 ms event is ×2.9. That is absorbed by the fixed-CPU pool and the addendum.
- MLM is ×0.8.
- FxFx is ×0.2.
- V4-5/T_seed is ×0.3.
- The toys are ×0.6–1.2 on a synthetic workspace.

Not fixed yet: the Geant4 spectra and variations (67, G), the Geant4 vertex yield inside the pool, and the 442
CPU-h of allowances. Those are for checkpoint 2.

## 3. Projection of the total

**Base:** the addendum planning case, toys at 80 parameters, **4,723 CPU-h** (ADD l.733-736 [U]). It is
4,609 − 183 + 108 + 190 extras, the extras being pilot +88, multijet +15, B6-c +46 and the B1 closure designs +41.
The table changes the base only where a measurement or an event since 17 Nov gives a reason. Arithmetic [V]; inputs
as tagged.

| change against the base | central | low | high | basis |
|---|---|---|---|---|
| C1 done (186.3 + 0.95 day 0 vs 198) | −11.7 | −11.7 | −11.7 | §1 [V] |
| C2 done (22.45 vs 81) | −58.6 | −58.6 | −58.6 | §1 [V]; C2 verdicts are recorded (LOG l.960) |
| P1 done (6.4 vs 51); floor test 1 ([DT3]) left as a later trigger | −44.6 | −44.6 | −44.6 | §1 [V] |
| S2 + S1 Stage 2/migration at measured units: spent 31.8 + E 1500 ≤ 2 + Stage 2 1.25×10⁶ × (39.7 + 4 × 32) ms = 58.2 + migration 5.5, against 88 + 7 | +2.5 | −21 (the 5×10⁵ LHE of S2-c reused) | +6 | [E] from §2 |
| pilot actual vs the 142.3 forecast | −1.4 | −1.4 | −1.4 | [V] |
| DP5 Herwig, not itemised in §11.2 | +3.2 | +3.2 | +3.2 | [V] |
| Phase-2 lines B2 10, B3 5, development 5 (14.6 used; ≤ 5 still due) | −3 | −5 | 0 | [V] + [E] |
| C′_PU NI attribution run (new, approved 19 Nov, limit 9; more γ source events planned) | +7 | +5 | +12 | LOG l.979 [U]; 2.3 used [V] |
| D2 robustness test (accepted with addendum 1; plan 12.4–14.5 with the c1-pu1 partner, ≤ 24 if the nominal arm is rerun): 12.04 used, d2-find 28/60 | +16 | +14 | +24 | D2_PLAN §5 [U]; markers [V] |
| ρ = 1 rows at 55.7 s instead of 60.4 (B2 direct 403, development 100) | −39.2 | −39.2 | 0 (4 jobs/node may restore 60.4) | §2 |
| ρ = 2 rows at 203 s (172) | −2.7 | −2.7 | 0 | §2 |
| 25.2-s rows, 1,287 CPU-h: hit level at 26.1 s (+19), overlays at 24.4 s (−4); low all at 24.0, high all at 26.1 | +15 | −62 | +46 | §2 |
| finder trials at 11.27 s (B5 163) | −6 | −6 | 0 | §2 |
| Stage 3 (266 + 36 in B6): central replaces the 3 keV anchor (sum 95.6 → 89.9 s); low applies ×0.70 everywhere | −18 | −91 | 0 | §2 |
| toys: 108 at 80 parameters in the base; low 29 (60 parameters, ÷1.6), high 365 (100 parameters, ×1.6) | 0 | −79 | +257 | ADD l.728-735 [U] |
| Geant4 spectra and variations 67 (G) at the pilot's ×1.25; high ×2 | +17 | 0 | +67 | §2 |
| B4-c extra row-20 events, +258 sized on tagged counts (STR l.1381). Low = the user accepts NOT TESTED on SM (Dagny, LOG l.978) | 0 | −258 | 0 | [U]; pending the user |
| DIF test sample of 7,750 unbiased events (STR conditional, 19). Its sizing inputs (DIF 31 at R06, H(R06) ≥ 0.004) are void (Eskil, LOG l.979) | 0 | 0 | +19 | [U] |
| CPU not in markers (MG children, lost attempts) | +4 | +2 | +5 | §1 [E] |
| **sum of changes** | **−120.5** | **−656** | **+323** | |
| **projected total** | **≈ 4,603** | **≈ 4,067** | **≈ 5,046** | **[E]** |
| against 4,609 / 5,992 | −0.1 % / −1,389 | −11.8 % / −1,925 | **+9.5 %** / −946 | |

**What drives the band.**
- **Toys** (−79…+257) are the largest single term. The real v2 workspace does not exist yet; it is re-measured on
  that workspace before Phase 4b (ADD l.730).
- **B4-c** (−258 or 0). It depends on the user's answer in the day-15 pause package: whether to accept NOT TESTED on
  the SM samples or amend.
- **Unit-cost scatter on the 1,287 CPU-h of PU-200 rows** (±4 %). These rows run at 3–4 jobs per node in
  production; the Phase-2 measurements were at 2–3 per node.
- **Stage 3**, whose 5 keV anchor is not measured.
- The Geant4 lines.

Phase 2's underspend on C1, C2 and P1 (−115 together; FxFx sits inside the S2 line) is certain and pulls every
case down.

**Compared with the last projection** (4,663–4,844 + 22–28 for D2; ORCHESTRATOR_STATE §3): the central value is
145 CPU-h lower (4,748 with D2 at 25). The cause is the Phase-2 underspend and the 8 % cheaper ρ = 1 event. The
high end is about 175 higher (4,872) because the toy band is now carried in full.

**Not in the band.** These are conditional draws, outside the approved figure (STR l.2541-2554). Each is reported
as an overrun if drawn.

| conditional draw | size (CPU-h) | where the total lands, from the high end 5,046 |
|---|---|---|
| exact toys | ≤ 236 (296 per ADD l.732) | 5,342 |
| second direct pile-up sample | 403 | 5,449 |
| fresh test samples | ≤ 123 / 163 / 80 | — |
| Q3 annex processes sized for an evaluable test | ≈ 680 | 5,726 |
| S1 at 4,000 rows | +827 | 5,873 |
| Z(νν) top-up (D8) | +45 / +109 | — |
| a chain fix after D2 shows an effect (pilot regenerated) | ≈ 142, plus the other samples | — |
| a Q2 (c) redesign | not costed | — |

No single draw crosses 5,992 from the high end, but any two of the large ones (Q3 annex, second direct sample, S1
at 4,000 rows) would. On the D8 top-up: Tove's pilot count is m_Z = 253 near-passes (LOG l.974-977), so no
enlargement is needed for statistics [E, my reading; the orchestrator decides D8].

**One exposure that would trigger the stop rule on its own.** Suppose the B4-c closure were amended to an
**attributed** hard-scatter count and the hit-level samples were sized for it (N_eff ≥ 24 in the test half). The
like-for-like attributed/tagged gap is ×13 (Björn, LOG l.977 [U]). Scaling the four sized processes (52,792 events)
by 13 gives about 6.9×10⁵ events × 25.2 s ≈ **4,800 CPU-h** [E, rough], which crosses 5,992 alone. The pause
package should say this when it puts the B4-c question to the user.

## 4. Wall clock and utilisation

**Delivered against available slot-hours.** The capacity model of STR §11.1 (l.2490-2503) gives 9 slots on
weekdays 08:00–19:00 and 10 otherwise (landau and schrodinger capped at 3), which is 232 slot-h per day.

"Slot-h" is the summed wall-clock overlap of attempts per day; "CPU-h" is their `cpu_s` spread over the same
interval. Both come from the markers via `checkpoint1_ledger.py` [V].

| window | available slot-h | delivered slot-h | utilisation (slot / CPU) | note |
|---|---|---|---|---|
| Mon 16 Nov 12:00–24:00 | 113 | 96.7 | 0.86 / 0.81 | day 0, from Gate A |
| Tue 17 Nov | 232 | 204.0 | **0.88 / 0.82** | queues full all day: the only production-like day |
| Wed 18 Nov | 232 | 122.8 | 0.53 / 0.51 | queues drained (C1 and pilot campaigns ending) |
| Thu 19 Nov 00:00–17:55 | 169 | 47.3 | 0.28 / 0.20 | work-limited: "all nodes idle at 11:10" (LOG l.965) |
| **Phase 2 before the outage** | **746** | **471** | **0.63 / 0.58** | Gate A assumed 0.50 for development phases |
| power loss, 19 Nov 17:55 – 23 Nov 13:25 | 901 | 0 | 0 | einstein and landau without power; maxwell and schrodinger without NFS home (LOG l.984) |
| 16 Nov 12:00 – 23 Nov 13:25 | 1,647 | 471 | 0.29 / 0.26 | |

Reading. The development utilisation was **0.58–0.63**, above the 0.50 assumed, and it was limited by the work
queued, not by the nodes. The production factor 0.75 has a single full-queue day as evidence, at 0.82 CPU [V, one
day]. That supports it but does not establish it for a 14-day run [E].

A new risk to production utilisation since the outage: the workers cannot resolve each other's hostnames
(LOG l.984). Multi-node drivers therefore run from einstein. A driver failure there would idle every node.

**Lost time.**
- The power loss took **3.8 days**: 19 Nov 17:55 to 23 Nov 13:25, 91.5 h.
- No completed output was lost. 9 attempts were retried; at most 1.6 CPU-h was lost [V, LOG l.984 and §1].
- Phase 2 was about one day ahead before the outage, on the compute items only:
  - the pilot ended 19 Nov 00:17 against 15:45 forecast;
  - C1 41/41 was complete on day 3;
  - the preliminary rule-1 reading came on day 3 instead of day 7.
- The decision and agent work (DP1 package, EXPLORATION consolidation, Cecilie's validation, Eskil, Ulrika, Sune)
  stopped mid-way and is restarting now.
- **Net slip: 3–4 days, central 4** [E]. Phase 2 closes about Wed 25 Nov (day 9) instead of day 5.

**Projected dates.** These assume everything after Phase 2 moves day for day (STR l.2632-2633, l.2644-2645), the
expected day-15 pause, and the Gate-A durations.

| milestone | schedule (day; date) | projected, 4-day slip, production at 0.75 | if production runs at the measured development 0.58 |
|---|---|---|---|
| decision point 1, checkpoint 1 | day 5; 21 Nov | 23–25 Nov | — |
| rule 1 binding reading | day 15; 1 Dec | ≈ 5 Dec | — |
| freeze (PREREG_v2, 4-bot, hash) | days 17–19; 3–5 Dec | ≈ 7–9 Dec | — |
| 4a production (2,489 CPU-h at 174/day = 14.3 days) | days 21–35.3 | ≈ 11–25 Dec | 18.5 days at 134.6/day → ≈ 29 Dec |
| Gate B | ≈ 4–6 Jan 2027 | **≈ 8–10 Jan** | ≈ 12–14 Jan |
| Gate C | ≈ 13–15 Jan | **≈ 17–19 Jan** | ≈ 21–23 Jan |
| calendar | 60 days approved | **≈ 64 days** (+7 %) | ≈ 68 days (+13 %) |

The production window now falls over the holidays. Lab load may be lower then, which would help utilisation;
whether the user is available for the freeze notice and Gate B is a question for the user, not a compute issue.
CPU-h are not affected by the slip: unit costs do not depend on the date.

## 5. Storage

Measured on 23 Nov at 13:36: `nice -n 19 ionice -c3 du -s --block-size=1M` on `/nfs/cajuela/jdochoa/quirks_v2/*`,
and `df` [V].

- **Study:** 253,410 MiB = **247.5 GiB (266 GB)** in 9,090 files. Of that, `data/` is 253,065 MiB: pilot 157.6 GiB,
  phase2 80.2 GiB (c1-pu2 pre-merge store 63.1 GiB, c1-pu1 10.3 GiB), p2c 7.2 GiB, S2 1.7 GiB. Backup is 0.3 GiB
  and logs 0.05 GiB. The 18 Nov figure was 236 GB (ORCHESTRATOR_STATE §3).
- **Pool** (`192.168.10.254:/mnt/cajuela`): 4,583 GiB in all, 645 GiB used, **3,705 GiB free (3.6 TiB)**, against the
  1.0 TB floor.

**Per-event sizes against planning.**
- Pilot: 169 GB measured, against 167 GB in the addendum and 52 GB at Gate A.
- PU-200 trial records: 0.53–0.57 MiB per event (c2-tseed1, c2-v44a-c) against 0.52 MB.
- Hit dumps: 2.64 MiB per event (c1-pu1, dumped).
- ρ = 2 pre-merge store: 33.8 MB per trial, which gives ≈ 270 GB for c1-pu2 plus the 3,000-event 4a sample, against
  200 GB planned and a 400 GB cap (Rosalie D-i-1 [U]; c1-pu2 measured 63.1 GiB [V]).

**Projection [E].** Start from STR §11.4's 470 GB (l.2626-2636) and add:
- +117 for the pilot;
- +70 for the pre-merge store at the measured 33.8 MB per trial;
- +16 for the trial records;
- +3 for the hit dumps.

That gives **≈ 0.68 TB**. At the pre-merge cap of 400 GB it is ≈ 0.81 TB; with a chain fix that regenerates the
pilot, ≈ 0.98 TB. All are below the 1.5 TB budget and the 2.0 TB stop. The pool would keep ≥ 2.9 TiB free unless
other users fill it (they hold about 400 GiB now). The storage rule is not near.

## 6. Decisions taken here (judgment calls; for the orchestrator)

- DECISION: I took the base from the addendum planning case at 80 toy parameters, then adjusted it line by line. I
  did not rebuild the whole STR script.
  ALTERNATIVES: rerun the STR script [3]/[4] with new unit costs (not available as one runnable file here).
  CONFIDENCE: medium; every change is itemised and can be re-derived.
- DECISION: I kept the B4-c row-20 events (+258) in the central case, because the user has not answered.
  ALTERNATIVES: drop them now (central would be ≈ 4,345).
  CONFIDENCE: high that this is the conservative choice.
- DECISION: I counted CPU from every attempt in the markers, not from `jobs.tsv`.
  CONFIDENCE: high; the difference is 0.35 CPU-h now.
- FLAG FOR HUMAN: none needed for the stop rule. Two items go to the user:
  - the ≈ 4-day calendar overrun (+7 % on 60 days), reported under D6;
  - in the pause package, that an attributed-count amendment of B4-c, sized for evaluability, would on its own
    exceed 5,992 CPU-h [E].
