# Orchestrator state (resume point)

**Updated:** 2026-11-24 10:09 -0500 (Opus orchestrator, PHASE-3 session) · **Branch:** `v2-jfc` · **Phase:** **3 RUNNING** (started 24 Nov 10:04); day 8 (day 0 = 2026-11-16)

A new session starts here. **Prompt for the user to paste into a fresh Claude Code session (model: Opus), started in
`/home/users/jdochoa/hllhc-quirks-search`:**

> You are the orchestrator of the quirks v2 study, continuing a study in progress. Read
> `QUIRKS_V2_ORCHESTRATOR_PROMPT.md` (the brief), then `analyses/quirks_v2/ORCHESTRATOR_STATE.md` in full, and follow
> the state file: it says what is running, what is waiting on me, and the rules that changed since the brief. Do not
> start Phase 1 or Phase 2 again. Phase 2 is closed; this session runs Phase 3. Begin with the section "First actions of a new session".


**PHASE 2 CLOSED 23 Nov 19:52 (read first).** Artifact `phase2_exploration/outputs/EXPLORATION.md` (Peder 4babc51 + orchestrator fills; tier: self-review + plot validator, done; no figures). Every Phase-2 PENDING block is filled except "Phase-3 inputs" (MET model, final pilot classification), which ARE Phase-3 work. Nothing runs on the cluster; no agent is alive. Power loss 19 Nov 17:54 – 23 Nov ≈ 13:00 (LOG 23 Nov). Worker hostname resolution fixed 23 Nov.
Results of 23 Nov (details LOG 23 Nov, EXPLORATION): DP1 passed (C1 41/41 with E1–E4, sealed 6/6); checkpoint 1 no stop rule (Leif); rule-1 validation (Ingvild) + subset review PASS with conditions (Nils; advisor Vigdis: binding-m candidate 1,501 (S) / 1,474 (F), lower bound, "above" only; axis + S3 conventions NOT fixed, → PREREG_v2) + B₅₀ arithmetic confirmed (Ylva: 63,167 at R09; single M = 993,885.9); D2 robust r(R06) 0.72, no correction (advisor Olav wording binding); FxFx E1500 inside band, S2-c FxFx complete, row open to 4a (advisor Siri); NI C′_PU ρ 0.024 (Kari); D8 top-up not drawn (advisor Runa; user may object); reach re-estimate (Tora; advisor Ulla; RESULT notice 16:38: more promising, weakly, not established; mixed-fraction table).
The BINDING day-15 reading is NOT made: it needs the user's calendar answer (rider 2 of option C), the Phase-3 final pilot classification and MET model, and its own advisor call; then a RESULT notice; the pause itself is the user's.
Crons of the 23 Nov session (daily 18:47, heartbeat 3 h) die with it: RE-CREATE them in the new session.
---

**PHASE 3 SESSION (24 Nov, read first).** Session started 10:04; all nodes had rebooted 09:53 (no shutdown record; nothing was running; LOG 24 Nov). Crons re-created (daily 47 18, heartbeat 13 */3). Brief for every Phase-3 agent: `phase3_selection/PHASE3_BRIEF.md`; slots `phase3_selection/SLOTS.md`; notes `phase3_selection/DAILY_NOTES.md`. Wave 1 running (see §1). Wave 2 queue in LOG 24 Nov (wave-1 entry). If this session dies: the three agents die with it; read their session logs `phase3_selection/logs/executor_{aurora,birgit,casper}_*.md` and respawn successors from them.

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


**[HISTORY 19 Nov; superseded by §2]** Waiting on the user: nothing (19 Nov: S2-e (b) −10.6 % and P1 record decided as recommended; COMMITMENTS.md; into PREREG_v2). Running agents: Sune (FxFx), Tove (Fable, preliminary rule-1 B₅₀), Ulrika (D2), Vidar (C1-c). C1 complete 41/41 with E1–E4 (sealed 6/6 PASS, file sha256 ae4de9ec…). Next: CPU re-projection for checkpoint 1 (advisor), DP1 RESULT notice on 21 Nov.

**Strategy-revision inputs (19 Nov, advisor Dagny; for EXPLORATION.md and the pause package):** v1 SM counts are one-hit tags, not attributed (STR l.753 wrong); void: STR l.791-797, Table 4.4c m_H, B5 share l.1420; B4-c and B5 closures NOT EVALUABLE on SM → user question in the day-15 pause package; hold row-20 extra events (STR l.2116) until answered; attributed vs C′_PU-linked measurement (STR l.753-754) running. Rule-1 reading frozen-text clarifications (i)-(iii) in LOG 19 Nov (Åsa).

**[HISTORY; expired 23 Nov]** User away 20–22 Nov (decided 19 Nov 17:20): reversible new decisions → advisor-checked default labelled "default, user absent"; irreversible/outward (installs, new permissions, unsealing, deleting data, budget beyond approved, the day-15 pause) wait with a DECISION notice. Continue into Phase 3 in this session after closing Phase 2 (write the Phase-2 closing state first). Heartbeat cron every 3 h + daily-report cron 18:47 (both session-only).

**User request (19 Nov 17:25): reach outlook at every step.** Every daily report and every RESULT notice carries a line "Reach outlook vs last report: more / less / equally promising, because …" (ESTIMATE, v1 placeholder efficiencies only; no v2 signal efficiency). Planned item: once Cecilie's rule-1 validation is in, an Opus executor recomputes the Gate A reach estimate with the pilot-based backgrounds (Z(νν) own-hit count, Eskil's attributed conversion scale), same script and placeholder efficiencies as Gate A, labelled ESTIMATE; note that the rule-1 B₅₀ is a ceiling, not a background estimate.

**Standing user rule (19 Nov 11:20):** when no user decision is needed, start the next planned work at once; never leave nodes and agents idle while planned work remains.

## 1. What is running unattended (check, do not disturb)

Agents (24 Nov 10:08): **Aurora** (Fable, p3-a final pilot classification, landau ≤ 3), **Birgit** (Fable, p3-c MET model, schrodinger ≤ 2), **Casper** (Opus, p3-b B2 pile-up, maxwell ≤ 3). Campaigns p3-a-*, p3-b-*, p3-c-* are theirs (development only). Phase 2: nothing (23 Nov 19:52). The history of the
Phase-2 campaigns is in LOG.md and the markers (failed-marker check: the LAST line of each marker; known failed
last lines: p2-c-r1v-s2a 19 + s2b 17 (rerun as s3a/s3b, done), p2-b-s2-fxfx-e1500 grids3 (replaced by grids4)).

## 2. Waiting on the user

1. **Calendar shift** (DECISION notice 2026-11-23 13:41): default C on **Wed 25 Nov 12:00** ("default, user absent")
   if no answer: every later date +4 calendar days (day 15 → Sat 5 Dec, freeze 7–9 Dec, Gate B ≈ 8–10 Jan, Gate C
   ≈ 17–19 Jan), riders (1) user says weekend of 5 Dec or Mon 7 Dec for the pause, (2) binding reading as soon as its
   inputs exist, no later than 5 Dec; also: holiday availability (production ≈ 11–25 Dec). Then record it in
   COMMITMENTS + LOG and update §5.
2. **C1-c container test: docker build permission** (DECISION notice 2026-11-19 11:19): no default; needed by Phase 5.
   C1-c stays NOT TESTED until answered.
3. Optional: the user may ask for the D8 Z(νν) top-up anyway (+45 / +109 CPU-h).
4. At the binding day-15 reading: the pause package (B4-c / B5 NOT EVALUABLE on SM; evaluable B4-c ≈ 4,800 CPU-h
   would cross 5,992 alone; NI R05 test has almost no power; hold the row-20 extra events (STR l.2116)).

## 3. State of Phase 2, item by item

| item | state | file |
|---|---|---|
| C1-b arithmetic | central values PASS; B₈₄ FAIL as frozen on 29/86 (within v1's Monte Carlo scatter) → amended E1: PASS | `phase2_exploration/outputs/c1b_arith.json`, module `src/v2arith/` |
| C1-a/c/e, the 41 comparisons | campaigns running; comparison script prepared and tested on open quantities only; **needs a successor executor (Opus) when campaigns finish** | Rosalie's log (successor section), `outputs/EXPLORATION_i_rosalie_2026-11-16_14-43.md` |
| C1-d sealed comparison | NOT done: a separate short session reads the six sealed counts and writes PASS/FAIL only (advisor trigger: blinding). The command is in Rosalie's successor section | — |
| C2-a V4-5 | FAIL as frozen in both halves (independent fit 50/50, 50/50; brute-force optimum 0/50, 6/50) → amended E2: (i) PASS, (ii) restricted scan pending | `outputs/V45_RESULT_rosalie_2026-11-17_08-13.md` |
| C2-b V4-4, C2-c T_seed | queued behind C1 campaigns | — |
| Stitch check for f₂₀₀ | 100k inclusive sample `p2-a-c1-s2inc` generated; ratio not yet read (20k result: 1.118 at E 200, 2.3σ) | Rosalie's EXPLORATION §3 |
| S2-a | three validations PASS (validation 2 with the qualifier "independent public code run by us") | Sebastian's EXPLORATION §2 |
| S2-b…f, f₂₀₀, retrievals | **DONE (Edgar, 17 Nov 17:38)** except FxFx. S2-b met (σ tables, R = 0.971→1.000 from Resummino run by us; scalar's R applied to E, flagged). f₂₀₀ E 200/500/1000/1500 = 0.0484/0.1041/0.1480/0.1676, Ẽ 500 = 0.1142, within 1.5 % of v1; tune shift dominates at ≥ 1 TeV. S2-d met (production must pass `--qedfsr`). S2-e sourced, no uncertainty stated (user choice, §2). S2-f +5.7…+7.9 %, not sourced (R-12). Open retrievals R-4, R-5, R-6, R-10, R-11, R-13, R-19, R-20 (later deadlines). Channel (ii) charged 39.5 CPU-h of 139. **Channel (i)'s 100k stitch cross-check never reached Edgar: a real 5–12 % excess would bias f₂₀₀ low outside its band** | `phase2_exploration/outputs/EXPLORATION_ii_edgar_2026-11-17_08-17.md` (FxFx successor task in §2.8) |
| P1 | executed and read: B\* attribution not supported at 3σ; population estimator fails at 3 of 5 points; floor test 2 "not the floor pattern"; floor test 1 not done ([DT3]). Limits the paper's statements; no effect on the search | Sebastian's EXPLORATION §3 |
| T1-a | workspace validates | `outputs/t1_v1mode_workspace_flora.json` |
| T1-b | FAIL as frozen (902 ± 32 against 789.7 ± 10 %); likelihood agrees with v1 (asymptotic 828.7069 vs 828.7067) → amended E3: PASS. The toy recipe needs a bracket refinement and an empty-tail rule (pre-registration) | `outputs/T1B_RESULT_flora_2026-11-17_09-35.md` |
| Toys | jax + warm start: 47 / 108 / 228 CPU-h at 60 / 80 / 100 parameters against 183; re-measure on the first real v2 workspace | `outputs/TOY_COST_viktor_2026-11-16_16-33.md` |
| B1-d geometry, Fatras physics | PASS | Tatiana's EXPLORATION |
| Pilot | part 1 and part 2 running (§1) | `outputs/PILOT_READY_xavier_…`, `outputs/B1_READY_albert_…` |
| Half-turn limit | limitation [L15]; looper gun 0 of 2×10⁵; robustness test D2 accepted (600 pile-up events with later arcs restored, 22–28 CPU-h, before the freeze): **not yet started** | `outputs/HALF_TURN_xavier_…`, `outputs/LOOPER_GUN_xavier_…`, addendum §1.5 |
| MET model inputs (R-2, R-3) | sourced (L1 TDR; ATLAS notes; CMS NOTE-2018/006 supplied by the user); jet-response tail NOT sourced; construction choice is Phase-3 work (by day 10) | Sebastian's EXPLORATION §1 |
| Forced tt̄ decays in `s4pu.py` | measured (0.327 s per event); the file edit waits until the C1 campaigns are complete | `CHAIN_PROVENANCE.md` |

CPU used: 383 CPU-h at 18:55 on 18 Nov (ledger, 2,768 jobs: reproduction 195, theory 39, pilot channel 13, pilot 136). **Ledger pitfall:** `tools/runner/bin/qv2run rebuild-ledger` writes one row per output FILE in `ledger/jobs.tsv`; de-duplicate on (campaign, job_id, attempts) before summing cpu_s, or the total doubles. Projection 4,663–4,844 CPU-h (ESTIMATE) + 22–28 for D2. Storage
236 GB for this study (du, 18 Nov); 633 GB used on the pool in total, 3.7 TB free. Last bundle `repo-2026-11-18.bundle`. Pilot at 18:55: Z(νν) 457/460, B1 664/762 (hs block 98 pending), no failure; c1-pu1 173/200, c1-cppub 49/75.

## 4. First actions of a new session (Phase 3)

1. `date`; read this file; the last 25 entries of `LOG.md`; `git status`, `git log --oneline -5`; check `notices/` and
   chat for the user's answers to §2 (calendar default C applies Wed 25 Nov 12:00).
2. Re-create the crons (rule 4: daily `47 18 * * *`; heartbeat every 3 h).
3. Read the JFC files deferred in `DEVIATIONS.md` V11 (methodology/03-phases.md Phase 3, 07, 11, agent definitions
   `agents/`), the strategy's Phase-3 sections (channels B1–B7, T1, T2) and `EXPLORATION.md` §9–§11.
4. Phase-3 plan (executors start in plan mode; 1-bot review per channel): MET model (R-2, R-3 sourced; jet-response
   tail NOT sourced; construction choice) and the final pilot classification (by shifted day 12 ≈ 2 Dec); then the
   binding day-15 reading (advisor first; RESULT notice; pause for the user). PREREG_v2 to-dos (LOG 23 Nov 15:45,
   19:44, 19:50): single M = 993,885.9; v1 link rule g1b_tt.py l.354-355 (v1 d724a1c); D9 actions (2)(3); D2 [L15]
   text (Olav); readings S1–S5 + axis + S3 conventions (own advisor call, "fixed after the pilot count was seen");
   R04 subset width-cut deviation; NI test re-sizing; per-job NUMBA_CACHE_DIR in the runner pre-flight;
   `outputs/s2/f200_T1_inputs.json` before the first T1 consumer; tectonic in the pixi env before 4a; chain unit
   cost of Geant4 injection is 2.0× plan (D2) for any projection.
5. Forced tt̄ decays in `s4pu.py`: the file edit waited for the C1 campaigns (complete now): do it before production.

## 5. Key dates (day 0 = 16 Nov 2026)

Calendar shift pending (§2.1). Under default C (+4 days): MET model and final pilot classification ≈ 2 Dec;
**binding rule-1 reading ≤ Sat 5 Dec (a pause is expected, Q2 (a))**; freeze 7–9 Dec (PREREG_v2, 4-bot review, hash,
user notified); Gate B ≈ 8–10 Jan 2027; Gate C ≈ 17–19 Jan 2027. Unshifted (option B): 28 Nov / 1 Dec / 3–5 Dec /
4–6 Jan / 13–15 Jan.

## 6. Phase tracker

- [x] Preflight; scaffold
- [x] Phase 1: Strategy — review PASS cycle 10; Gate A passed 2026-11-16; addendum 1 approved 2026-11-17
- [x] Phase 2: Exploration — CLOSED 2026-11-23 (DP1 passed 23 Nov; EXPLORATION.md; self-review)
- [ ] **Phase 3: Processing, signal blind — RUNNING since 24 Nov** — channels B1–B7, T1, T2, each 1-bot; PREREG_v2 (4-bot, hash, notify user)
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
Session names already used (do not reuse; see `MODEL_LEDGER.md` and `LOG.md`): Ada … Ylva (23 Nov: Halvard, Ingvild, Jonas, Kari, Leif, Maren, Nils, Olav, Peder, Runa, Siri, Tora, Ulla, Vigdis, Ylva). Pick new ones.
