# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-16 16:40 -05 (measured) · **Branch:** `v2-jfc` · **Phase:** 2 (Exploration), day 0 of the calendar = 2026-11-16

**Gate A passed by the user 2026-11-16** with all defaults (`COMMITMENTS.md`, "Gate A answers"): 4,609 CPU-h approved,
stop-and-ask 5,992, about 60 days. Artifact of record: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`.

**Running (2026-11-16 16:40):**
- **PILOT part 1 RUNNING** on schrodinger, 2 lanes, launched by the orchestrator 16:39 on the user's approval:
  `p2-c-pilot-mb` (40 jobs) + `p2-c-pilot-znn-00…15` (460 jobs, 2.3×10⁶ events), ~95 CPU-h, ~48 h. Status:
  `bash tools/runner/examples/p2x/pilot/STATUS_p2-c-pilot_mb-znn.sh`; resume = `bash tools/runner/examples/p2x/pilot/LAUNCH_p2-c-pilot_mb-znn_2slots.sh`
  (idempotent). Do not edit files under `frozen_from_launch` of the PLAN. Verify first done markers + one file check.
- channel (i) Rosalie (Opus): C1 campaigns, C1 signal chain, C2 queued; landau 2, maxwell 2. Next report at first verdicts.
- channel (ii) Sebastian (Opus): S2-a 3× PASS (validation 2 with qualifier); K(m) done (CT18), PDF4LHC21 running;
  f₂₀₀, P1 runs, FxFx diagnosis (no 30-min exception yet), Herwig comparison. landau 1, maxwell 1.
- channel (iii) **Xavier** (Fable): ONE lane on schrodinger: looper gun (Geant4 trajectories injected; informs the
  chain decision) then option (a) slices for DIF-C/NI-C; then B1 production code/campaign files (not launched).
  Xavier may not launch pilot campaigns (permission system); the orchestrator launches on user approval.
- Toys solved up to ~80 parameters (jax + warm start; `phase2_exploration/outputs/TOY_COST_viktor_2026-11-16_16-33.md`).
- **Chain finding:** Fatras stops every particle at half a turn (v1 behaviour; 25–37 % of crossings missing;
  `phase2_exploration/outputs/HALF_TURN_xavier_2026-11-16_16-08.md`). User chose option B (measure loopers first;
  pilot on the present chain). If the looper gun shows candidates → notify (RESULT/DECISION): fix chain, regenerate pilot.
- **Addendum 1:** v3 written (`phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v3_yvonne_2026-11-16_15-04.md`), NOT yet
  reviewed a third time. Before the third (last 1-bot) review it needs a fresh fixer pass (v4): A-1 result
  (`phase2_exploration/outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md`), the half-turn finding and the treatment of
  DIF-C/NI-C (option (a) result), looper-gun result, jets stored to 10 GeV (not 15), toy projection with jax
  (47/108/228 CPU-h), pilot part 1 already launched. Then review → user approval (DECISION notice) → B1 pilot streams.
  User decisions still owed: B1 pilot sizes; number of terms; hard-scatter sample; unread populations; pool decision
  at the corrected floor (121–201 events; upside 514–584 GeV).
- Open: T1-b no verdict (resume with the jax configuration, successor session); MET-model construction (Phase 3);
  jet-response tail not sourced; R-15–R-17 open; `s4pu.py` forced-tt̄ edit waits for C1 campaigns to finish.

**Orchestrator duties now:** commit on each report; resume executors; spawn the separate sealed C1 comparison session
when channel (i) has the campaigns and the tested script (writes only PASS/FAIL per criterion; six sealed points);
day 5 (21 Nov): decision point 1 (C1, C2) + stop-rule checkpoint 1 (re-project CPU with measured unit costs and
utilisation); consolidate `EXPLORATION.md`, self-review + plot validator (JFC Phase-2 tier), then Phase 3.
**Daily report** (user request; DEVIATIONS V14): `daily/YYYY-MM-DD.tex` + compiled `.pdf` (LaTeX, built in `/var/tmp/jdochoa/tex`), STATUS.md, bundle, then **commit and `git push origin v2-jfc`** (authorised by the user 2026-11-16 for the daily reports; never force) each evening; a session cron (18:47,
session-only, expires after 7 days: re-create) triggers it; if the session was restarted, re-create the cron.
**Notifications to the user (user instruction 2026-11-16, DEVIATIONS V15b):** `tools/notify/notify.sh <KIND> "<subject>" <body.md>`
writes a NEW FILE `notices/<date_time>_<KIND>_<slug>.md`, commits only it and pushes `v2-jfc` (the user watches the
repository by hand; no mail exists; nothing is pushed to `main` any more). Only the orchestrator notifies. Send one
ONLY when: (DECISION) a decision of the user is needed, with options, recommendation and deadline; (PROBLEM) a
cluster or infrastructure fault needs the user or an admin, or a stop rule fires; (RESULT) a result that changes the
expected outcome, a decision point or gate is reached, or a criterion fails. The evening daily report (LaTeX + PDF in
`daily/`) is itself the routine notice. Batch what arrives within about an hour. Each notice stands alone: numbers
with tags, what is asked, by when. No sealed signal quantity ever. When the user has answered a DECISION notice,
say so in the next notice or daily report.

**User's next interventions:** day 5 only if the stop rule fires or C1 fails after three remediation attempts;
**day 15 = 1 Dec: expected pause (Q2 a)**; freeze notification days 17–19 (3–5 Dec); Gate B about 4–6 Jan 2027;
Gate C about 13–15 Jan 2027.
Session names used through Tatiana; next free: Ulrich.

**Clock warning:** times in `LOG.md` and in file names before 2026-11-14 01:20 are sequence labels, not clock times;
git commit times are authoritative. Always call `date` before writing a time.

Read `LOG.md` entry "15:12 — INTERRUPTION" for the constraints in force (10 GB cap, nothing heavy on einstein, one
pixi install at a time, at most 3 subagents).

## Phase tracker
- [x] Preflight — PASS on re-run after the cajuela fix (`PREFLIGHT.md`)
- [x] Scaffold, state files, first bundle, first commit
- [x] Phase 1: Strategy — review PASS cycle 10; Gate A passed by the user 2026-11-16
- [ ] Phase 2: Exploration / regenerate the base — executor(s) + self-review + plot validator; decision point 1
- [ ] Phase 3: Processing, signal blind — parallel channels B1–B7, T1, T2, each 1-bot; consolidation; PREREG_v2 (4-bot, hash, notify user)
- [ ] Phase 4a: Expected — production, closure verdicts; executor + note writer + typesetter + 4-bot+bib
- [ ] Phase 4b: selection rule on optimisation half — executor + note writer + typesetter + 4-bot+bib → GATE B (human)
- [ ] Phase 4c: evaluation half — executor + note writer + 1-bot (escalate to 4-bot per JFC 06 §6.4)
- [ ] Phase 5: AN + journal paper + Zenodo-ready package — executor + note writer + typesetter + 5-bot + adversarial 25-question review → GATE C (human)

## Active subagents (at most 3 at a time; nothing heavy on einstein)
DONE and committed: investigators D1–D6 + `FRAMING.md` (`980d207`); feasibility C runner (`0ff12df`), B generators/Geant4
(`6c1b760`), A chain (`3502634`). Reports: `phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md` + `benchmarks_*.json`.

No subagent is running.

Phase-1 review history: cycles 1–9 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo, Johanna, Lena, Margaret,
Odette); A 11→4→1→0→0→0→0→0→0; B 24→14→15→5→3→1→4→1→1. Versions kept: v1 Brigitte … v9 Mireille
(`phase1_strategy/outputs/STRATEGY_mireille_2026-11-14_06-55.md` is the current strategy).
Settled (cycle-7, -8 and -9 arbiters): design, criteria, samples, budget 4,609 CPU-h / threshold 5,992 / 60 days incl.
the expected pause, default answers, expected outcome; day-15 family closed with script self-test and text checker.
If the user authorises cycle 10: fixer applies verdict-v9 edits (B-1 + E2–E14; the arbiter's tested script is
`/var/tmp/jdochoa/arbiter_odette/apply_edits.py`, to be used only as a reference) → v10; verification per verdict §9
(narrow, mechanical, fresh sessions: diff v9→v10 equals the edit list; checker 45/45; script output unchanged).
Draft Gate-A package: `gates/GATE_A_DRAFT.md` (1,496 words; describes v9 with the edits applied).
KEY FOR GATE A: expected outcome = background ≈ 0.7–1.0×10⁴ events (after CKF, as v1 counted) led by hard-scatter
conversions; reach below 243 GeV with the 0.17 normalisation width (bounds ≈ 180 GeV); day-15 pause expected; no
conversion rejection alone lifts it at v1's central decays-in-flight size (1–2 v1 counts). Q2 central; Df-11 new.

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Isolde, Ivan, Jasper, Johanna, Jules. Katya, Kenji, Klaus, Lena, Leopold. Ludmila, Magnus, Marcel, Margaret, Mireille. Nadia, Nikolai, Nora, Odette. Next free: Oscar.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
WAIT for the user's answers to the two items at the top. Nothing else.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
