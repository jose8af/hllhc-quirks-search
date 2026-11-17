# Orchestrator state (resume point)

**Updated:** 2026-11-17 10:40 -05 (measured) · **Branch:** `v2-jfc` · **Phase:** 2 (Exploration), day 1 (day 0 = 2026-11-16)

A new session starts here. **Prompt for the user to paste into a fresh Claude Code session (model: Opus), started in
`/home/users/jdochoa/hllhc-quirks-search`:**

> You are the orchestrator of the quirks v2 study, continuing a study in progress. Read
> `QUIRKS_V2_ORCHESTRATOR_PROMPT.md` (the brief), then `analyses/quirks_v2/ORCHESTRATOR_STATE.md` in full, and follow
> the state file: it says what is running, what is waiting on me, and the rules that changed since the brief. Do not
> start Phase 1 again. Begin with the section "First actions of a new session".

---

## 0. Rules that changed since the brief (binding; details in `DEVIATIONS.md` V11–V16 and `LOG.md`)

1. **Orchestrator = Opus, with Fable on call** (user decision 2026-11-17, V16). Use Fable only for:
   (a) gate reviewers and arbiters (4-bot panels, pre-registration review, the Phase-4/5 reviews);
   (b) an **advisor call** (one fresh Fable subagent, a one-page brief with the facts and file paths, returning a
   ruling in ≤ 20 lines) BEFORE the orchestrator rules on any of the **triggers** below;
   (c) an executor whose output feeds the binding day-15 reading (rule 1 of STR §11.7): pilot classification,
   own-hit counts, the B₅₀ projection script.
   Everything else is Opus (or lower for mechanical work). Log every non-default choice in `MODEL_LEDGER.md`.
   **Advisor triggers (run this checklist on every agent report):**
   - a criterion, definition or number frozen at Gate A or by addendum 1 would be read, reworded, waived or failed;
   - a stop rule of the brief §7 might apply (projected CPU > 5,992; storage; MUST item infeasible; cluster fault);
   - a number, verdict or recommendation is about to go to the user in a DECISION or RESULT notice;
   - blinding: anything that could expose a v2 signal efficiency or a sealed C1 count;
   - an agent asks to launch a pilot/production campaign, to install software, or reports that a permission was
     denied (never run a command for an agent that was denied it: surface it to the user);
   - two agents or two documents disagree on a number.
2. **One session per phase** (user decision 2026-11-17). Close at each phase boundary after writing this file; the
   next session starts from it. Campaigns run from detached drivers on the workers and need no session.
3. **Token discipline.** Agents send ONE final report (≤ 15 lines; results go to files). No interim status
   reports; they wait on their own jobs with a background wait. Split work by deliverable up front so that an
   agent finishes before its context grows large; hand over only at a finished item (no hard context cap, the user
   declined one). Give agents short digests and the exact strategy sections, not whole documents. Review loops:
   two rounds, then the open list goes to the user. The orchestrator answers the user in chat only for decisions,
   problems and their questions; routine progress goes to the daily report.
4. **Pushing** (V14, V15b): commit and `git push origin v2-jfc` for the daily reports and notices only; never
   force-push, never rewrite history, nothing to `main`.
   - **Daily report:** each evening `daily/YYYY-MM-DD.tex` + compiled `.pdf` (style of `daily/2026-11-16.tex`;
     build with pdflatex twice into `/var/tmp/jdochoa/tex`, niced), `STATUS.md`, repo bundle to
     `/nfs/cajuela/jdochoa/quirks_v2/backup/repo-<date>.bundle` (`.part` → rename), commit, push. The trigger is a
     session cron (dies with the session): **re-create it** with CronCreate (`47 18 * * *`; expires after 7 days).
   - **Notices:** `tools/notify/notify.sh <DECISION|RESULT|PROBLEM|INFO> "<subject>" <body.md>` writes a new file in
     `notices/` and pushes. Only for: a decision needed (options, recommendation, deadline), a cluster fault or
     stop rule, a result that changes the outlook or a decision point, a failed criterion. Each notice stands alone.
5. **Cluster.** einstein: nothing heavy, light niced scripts only; 10 GB memory cap on the orchestrator's service.
   All compute through `tools/runner` on landau, maxwell, schrodinger; jobs ≤ 30 min; never rename a directory on
   cajuela; one pixi install at a time and none on einstein. Node caps: 3 jobs where a graphical login exists
   (landau, schrodinger at present), 4 otherwise. Geant4 is node-local on all three workers
   (`/home/scratch/jdochoa/envs/g4`); the jax toy environment only on schrodinger (`tools/install/pyhf_toys/`).
6. **Agents never launch pilot or production campaigns** (the permission system refuses them): the orchestrator
   launches, after the user's approval, with pre-flight, `pgrep` node counts and a line in
   `phase2_exploration/SLOTS.md`.
7. **Clock:** always run `date` before writing a time; git commit times are authoritative.

## 1. What is running unattended (check, do not disturb)

| what | where | status / end (ESTIMATE) | commands |
|---|---|---|---|
| Pilot part 1: `p2-c-pilot-mb` + `p2-c-pilot-znn-00…15` (2.3×10⁶ Z(νν) events) | schrodinger, 2 lanes | 169/500 at 10:10 on 17 Nov, 0 failed; about 18 Nov 19:00 | status `bash tools/runner/examples/p2x/pilot/STATUS_p2-c-pilot_mb-znn.sh`; resume `bash tools/runner/examples/p2x/pilot/LAUNCH_p2-c-pilot_mb-znn_2slots.sh` |
| Pilot part 2 (B1 streams): `p2-c-pilot_b1`, 762 jobs | schrodinger + landau + maxwell, 1 lane each | launched 17 Nov 10:10; class blocks about 16 h; the hard-scatter block starts after the last Z(νν) file | status `bash tools/runner/examples/p2x/b1/STATUS_p2-c-pilot_b1.sh schrodinger landau maxwell`; resume `NODECAPS="3 3 4" bash tools/runner/examples/p2x/b1/LAUNCH_p2-c-pilot_b1_3slots.sh schrodinger landau maxwell` (a lane stops after 4 h of retries: then run this line again) |
| Channel (i) reproduction campaigns `p2-a-*` (c1-pu1, c1-pu2, signal, rates, SM, C′_PU, T_seed, V4-4) | landau 2 slots, maxwell 2 slots, detached queues | all by about Thu 19 Nov midday | queue logs `ssh -x landau "tail /home/scratch/jdochoa/drivers/queue_landau_B.log"`; successor section at the end of `phase2_exploration/logs/executor_rosalie_2026-11-16_11-55.md` |
| Channel (ii) re-showers `p2-b-s2c-rs` | maxwell, 1 slot | about 17 Nov 17:30 | `ssh -x maxwell tail -2 /home/scratch/jdochoa/drivers/queue_maxwell5.log` |

Do not edit files listed under `frozen_from_launch` in the two PLAN files while the pilot runs. Failed markers:
`grep -lsE '"(failed|timeout|oom|killed|lost|corrupt|verify_failed)"' ledger/markers/p2-c-pilot-*/*/*.marker`.
After each B1 stream's first chain campaign one validation job is due (read with `hard_except_early_product_hits`;
see `phase2_exploration/outputs/B1_READY_albert_2026-11-16_20-24.md` §9).

## 2. Waiting on the user

| item | notice | deadline | consequence |
|---|---|---|---|
| **E1–E3: three Gate-A criteria fail as worded** (C1-b B₈₄ tolerance; C2-a V4-5 brute-force comparison; T1-b toy limit) | `notices/2026-11-17_0937_DECISION_…` | 20 Nov | C2-a FAIL blocks decision point 1 (day 5 = 21 Nov) by STR §4.2 unless the user amends or lifts it. Recommendation given: accept E1 and E3 rewordings; for E2 run the restricted scan (1.5 CPU-h, not yet run: wait for the user's answer) |
| Exception to the 30-minute job rule for FxFx (two single-core jobs of about 1.5 h) | chat and `daily/2026-11-16` | none (S2-c deadline Phase 4a) | FxFx piece of the f₂₀₀ uncertainty stays "pending" |

Already decided by the user (all in `COMMITMENTS.md` and `LOG.md`): Gate A (all defaults; 4,609 CPU-h, stop-and-ask
5,992, about 60 days); pool at fixed CPU; option B on the half-turn limit; **addendum 1 D1–D9 as recommended
(17 Nov; in force; `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md`)**.

## 3. State of Phase 2, item by item

| item | state | file |
|---|---|---|
| C1-b arithmetic | central values PASS; B₈₄ FAIL as frozen on 29/86 (within v1's Monte Carlo scatter) → E1 | `phase2_exploration/outputs/c1b_arith.json`, module `src/v2arith/` |
| C1-a/c/e, the 41 comparisons | campaigns running; comparison script prepared and tested on open quantities only; **needs a successor executor (Opus) when campaigns finish** | Rosalie's log (successor section), `outputs/EXPLORATION_i_rosalie_2026-11-16_14-43.md` |
| C1-d sealed comparison | NOT done: a separate short session reads the six sealed counts and writes PASS/FAIL only (advisor trigger: blinding). The command is in Rosalie's successor section | — |
| C2-a V4-5 | FAIL as frozen in both halves (independent fit 50/50, 50/50; brute-force optimum 0/50, 6/50) → E2 | `outputs/V45_RESULT_rosalie_2026-11-17_08-13.md` |
| C2-b V4-4, C2-c T_seed | queued behind C1 campaigns | — |
| Stitch check for f₂₀₀ | 100k inclusive sample `p2-a-c1-s2inc` generated; ratio not yet read (20k result: 1.118 at E 200, 2.3σ) | Rosalie's EXPLORATION §3 |
| S2-a | three validations PASS (validation 2 with the qualifier "independent public code run by us") | Sebastian's EXPLORATION §2 |
| S2-b…f, f₂₀₀, retrievals R-1…R-20, final channel (ii) file | **Edgar (Opus) running**, one final report expected the evening of 17 Nov | `phase2_exploration/logs/executor_edgar_*.md` |
| P1 | executed and read: B\* attribution not supported at 3σ; population estimator fails at 3 of 5 points; floor test 2 "not the floor pattern"; floor test 1 not done ([DT3]). Limits the paper's statements; no effect on the search | Sebastian's EXPLORATION §3 |
| T1-a | workspace validates | `outputs/t1_v1mode_workspace_flora.json` |
| T1-b | FAIL as frozen (902 ± 32 against 789.7 ± 10 %); likelihood agrees with v1 (asymptotic 828.7069 vs 828.7067) → E3. The toy recipe needs a bracket refinement and an empty-tail rule (pre-registration) | `outputs/T1B_RESULT_flora_2026-11-17_09-35.md` |
| Toys | jax + warm start: 47 / 108 / 228 CPU-h at 60 / 80 / 100 parameters against 183; re-measure on the first real v2 workspace | `outputs/TOY_COST_viktor_2026-11-16_16-33.md` |
| B1-d geometry, Fatras physics | PASS | Tatiana's EXPLORATION |
| Pilot | part 1 and part 2 running (§1) | `outputs/PILOT_READY_xavier_…`, `outputs/B1_READY_albert_…` |
| Half-turn limit | limitation [L15]; looper gun 0 of 2×10⁵; robustness test D2 accepted (600 pile-up events with later arcs restored, 22–28 CPU-h, before the freeze): **not yet started** | `outputs/HALF_TURN_xavier_…`, `outputs/LOOPER_GUN_xavier_…`, addendum §1.5 |
| MET model inputs (R-2, R-3) | sourced (L1 TDR; ATLAS notes; CMS NOTE-2018/006 supplied by the user); jet-response tail NOT sourced; construction choice is Phase-3 work (by day 10) | Sebastian's EXPLORATION §1 |
| Forced tt̄ decays in `s4pu.py` | measured (0.327 s per event); the file edit waits until the C1 campaigns are complete | `CHAIN_PROVENANCE.md` |

CPU used: 53 CPU-h at the end of day 0 (ledger); projection 4,663–4,844 CPU-h (ESTIMATE) + 22–28 for D2. Storage
about 480 GB used on the pool in total, 3.8 TB free.

## 4. First actions of a new session

1. `date`; read this file; skim the last 15 entries of `LOG.md`; check `git status` and `git log --oneline -5`.
2. Check §1 (both pilot parts, failed markers, lanes alive; relaunch a dead lane with its LAUNCH line).
3. Re-create the daily-report cron (rule 4). Check for the user's answers to §2.
4. If Edgar's final report is not on disk (`phase2_exploration/outputs/EXPLORATION_ii_edgar_*.md`), spawn an Opus
   successor for channel (ii) from his log's successor section.
5. When channel (i)'s campaigns finish (about Thu 19 Nov): spawn an Opus successor for the 41 C1 comparisons,
   V4-4, T_seed and the channel (i) EXPLORATION file; then the sealed C1 comparison session (advisor first).
6. Pilot validation jobs per stream (§1); when both pilot parts are complete, record sizes and CPU-h from the ledger.
7. Day 5 (21 Nov): decision point 1 (C1, C2: needs the user's E1–E3 answer) and stop-rule checkpoint 1 (re-project
   CPU with the measured unit costs and the measured utilisation; advisor trigger). Day 7 (23 Nov): preliminary
   rule-1 projection from the pilot (Fable executor). Consolidate `phase2_exploration/outputs/EXPLORATION.md` from
   the channel files (Rosalie + successor, Sebastian/Edgar, Tatiana, Xavier, Albert, Flora, Viktor), self-review +
   plot validator (JFC Phase-2 tier), commit. **Then close the session**: Phase 3 starts in a new one, which first
   reads the JFC files deferred in `DEVIATIONS.md` V11 (03-phases Phase 3, 07, 11, agent definitions).

## 5. Key dates (day 0 = 16 Nov 2026)

Day 5 = 21 Nov (decision point 1, checkpoint 1) · day 7 = 23 Nov (preliminary projection; Z(νν) top-up decision,
D8) · day 12 = 28 Nov (MET model, final pilot classification) · **day 15 = 1 Dec (binding rule 1; a pause is
expected, Q2 (a))** · freeze days 17–19 = 3–5 Dec (PREREG_v2, 4-bot review, hash, user notified) · Gate B about
4–6 Jan 2027 · Gate C about 13–15 Jan 2027.

## 6. Phase tracker

- [x] Preflight; scaffold
- [x] Phase 1: Strategy — review PASS cycle 10; Gate A passed 2026-11-16; addendum 1 approved 2026-11-17
- [ ] **Phase 2: Exploration — in progress** (decision point 1 at day 5)
- [ ] Phase 3: Processing, signal blind — channels B1–B7, T1, T2, each 1-bot; PREREG_v2 (4-bot, hash, notify user)
- [ ] Phase 4a: Expected — production, closure verdicts; 4-bot+bib
- [ ] Phase 4b: selection rule on the optimisation half; 4-bot+bib → GATE B (human)
- [ ] Phase 4c: evaluation half; 1-bot
- [ ] Phase 5: note + paper + reproduction package; 5-bot + adversarial review → GATE C (human)

## 7. Where things are

`prompt.md` (brief) · `COMMITMENTS.md` (binding; Gate A answers; addendum 1) · `DEVIATIONS.md` · `LOG.md`
(append-only) · `STATUS.md` (user report) · `MODEL_LEDGER.md` · `AGENT_RULES.md` and
`phase2_exploration/PHASE2_BRIEF.md` (give these to every Phase-2 agent) · `phase2_exploration/SLOTS.md` ·
`phase2_exploration/DAILY_NOTES.md` · `daily/` · `notices/` · `gates/GATE_A.md` · strategy
`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` (333 kB: read by section) · agent definitions
`agents/` · runner `tools/runner/` (repo root) · notify script `tools/notify/notify.sh`.
Session names already used (do not reuse; see `MODEL_LEDGER.md` and `LOG.md`): Ada … Flora. Pick new ones.
