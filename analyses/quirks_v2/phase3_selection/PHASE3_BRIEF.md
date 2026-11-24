# Phase 3 brief for the channel executors (orchestrator, 2026-11-24)

Phase 2 closed 2026-11-23 19:52 (`phase2_exploration/outputs/EXPLORATION.md`; decision point 1 passed). Phase 3
(JFC "Processing", signal blind) runs as parallel channels, each with a 1-bot review (critical + plot validator), then
a consolidation into `phase3_selection/outputs/SELECTION.md`, then the v2 pre-registration `PREREG_v2.md` (4-bot,
hash, commit before any v2 production; the user is notified).

`AN` = `/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2`. `STR` =
`AN/phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` (333 kB: do **not** read it whole; read the sections
listed for your work package, in full, with the Read tool using offset/limit from `grep -n '^## \|^### '`). `ADD` =
`AN/phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` (approved 17 Nov; binding).
`EXP` = `AN/phase2_exploration/outputs/EXPLORATION.md` (the Phase-2 hand-over; §0.2 lists the channel files).
`COM` = `AN/COMMITMENTS.md` (binding; amendments E1–E4; Gate A answers).

## 0. Calendar

Day 0 = 16 Nov 2026. A power loss cost ≈ 4 days; under the pending default calendar (option C, applies Wed 25 Nov
12:00 unless the user answers otherwise) every later date moves by +4 days: **day 12 → Wed 2 Dec** (MET model, final
pilot classification, A and m_mig), **day 14 → Fri 4 Dec** (pile-up development model's R04–R07 inputs), **day 15 → Sat
5 Dec at the latest** (binding rule-1 reading, decision point 2, STR §11.7; the reading is made **as soon as its
inputs exist**), freeze 7–9 Dec. Work toward the earliest date; never estimate a time, run `date`.

## 1. Read before planning (every work package)
1. `AN/AGENT_RULES.md` (binding), the STUDY OVERRIDES header of `AN/CLAUDE.md`, `AN/agents/executor.md` (your role;
   follow its prompt template), `AN/phase3_selection/CLAUDE.md`, `AN/methodology/03-phases.md` → "Phase 3"
   (l.358-529), `AN/methodology/11-coding.md`, `AN/methodology/appendix-plotting.md` if you make figures.
2. STR §0 (summary), §4.0 (unit costs, conventions), your item sections (your prompt names them), §11.7 (decision
   points; decision point 2 is the Phase-3 target), the rows of COM for your items, and the ADD sections your prompt
   names.
3. EXP §0.1 (verdicts), §9 (strategy-revision inputs: **the Phase-1 assumptions that turned out wrong; build on what
   Phase 2 found, not on what Phase 1 assumed**), §10 (open items for PREREG_v2 and the pause package), §12
   (number disagreements, unresolved), and the EXP sections and channel files your prompt names.
4. What runs and what it costs: `AN/CHAIN_PROVENANCE.md`, `AN/ledger/README.md`, the runner under
   `$REPO/tools/runner/`, EXP §3.1 and §5.1 (measured unit costs).

## 2. Rules specific to Phase 3
- **Plan first.** Before any code or job, write `phase3_selection/logs/executor_<session>_<YYYY-MM-DD_HH-MM>.md`
  with the plan (scripts, campaigns with events, jobs and CPU-h against your budget, outputs, checks, order, what you
  deliver and by when), then execute. Keep that log as you go.
- **Phase 3 executes the strategy; it does not redesign it.** Every criterion, definition or number frozen in STR,
  ADD or COM is used as written. If one cannot be applied as written, or a result would read, reword, waive or fail
  it, **stop and report** (the orchestrator runs an advisor call first). Never choose a convention after seeing the
  result it sets; where the frozen text leaves a choice open, report the result under every allowed reading.
- **Blinding (invariant).** No v2 signal efficiency is computed, printed, plotted or looked at. The only exceptions
  are those of COM BL-1 / STR §4.1 "Other quantities" items 1–2 (A, f₂₀₀, m_mig, computed **once**, in the STR order,
  by the work package assigned to it) and C1's open tier. The six sealed C1 points stay sealed. If unsure whether a
  number is an efficiency, do not look; ask in your report.
- **Where things run.** einstein: editing, light niced scripts only. All compute on landau, maxwell, schrodinger
  through the runner (`tools/runner`, SSH mechanism unless your prompt says Argo), jobs ≤ 30 min, idempotent,
  resumable, outputs `name.part` → rename on cajuela with a marker in `AN/ledger/markers/`. Never rename a directory
  on cajuela. Per-job work in `/home/scratch/jdochoa/<job_id>`. Campaign names start with `p3-<wp>-` (your prompt
  gives `<wp>`). Set a per-job `NUMBA_CACHE_DIR` under the job's scratch for numba code (EXP §10 item 13).
- **Slots.** Your prompt assigns your node(s) and job cap. Before launching, append a line to
  `phase3_selection/SLOTS.md` (time from `date`, node, jobs, duration, campaign) and a RELEASED line when done.
  Check `uptime`, `who` and `pgrep -u jdochoa -af qv2` on the node first. Weekdays 08:00–19:00 the lab uses the
  workers as terminals: stay within your cap.
- **Development, not production.** You may run development campaigns that STR assigns to Phase 3 within your CPU
  budget. You may **not** launch pilot or production campaigns, the S1 string propagation, or anything that STR
  labels as production: write the campaign definition and the exact launch command, and report; the orchestrator
  launches it. Any `pixi install`/`add` needs the orchestrator's go (one install at a time in the whole study).
- **CPU accounting.** CPU-h from the ledger (`qv2run rebuild-ledger` writes one row per output FILE: de-duplicate on
  (campaign, job_id, attempts) before summing). If your projected spend exceeds your budget by more than 30 %, stop
  and report before spending it.
- **Numbers.** VERIFIED / ESTIMATE / UNVERIFIED with file:line or campaign; no constant from memory (cite the source;
  log web lookups in `AN/retrieval_log.md`).
- **Write scope.** `AN/phase3_selection/{src,outputs,logs,review}`, `AN/phase3_selection/experiment_log.md`
  (append-only), `AN/phase3_selection/SLOTS.md` (append), `AN/retrieval_log.md` (append), bulk data via the runner.
  Chain code in `AN/{analytic,sim,acts,code,envs}` may be modified only with a note in your log and in
  `AN/CHAIN_PROVENANCE.md` (what, why, diff size). Phase-2 code may be imported or copied, not edited.
- **No git, no subagents.** The orchestrator commits.
- **Stop and report at once** (do not repair): a cluster service fails; a frozen criterion would be read, reworded,
  waived or failed; a MUST item looks infeasible after a real attempt; a result contradicts a Phase-1/Phase-2 input in
  a way that changes the plan ("Phase 1 assumed X. Phase 3 found Y. Implications: Z.").

## 3. Deliverables (each work package)
- Working code in `phase3_selection/src/<wp>/` (logging, not print; analysis and plotting separated).
- `phase3_selection/outputs/<WP>_<session>_<YYYY-MM-DD>.md`: what was run (campaign table: events, jobs, CPU-h), each
  item's result against its pre-declared criterion (PASS / FAIL / NOT TESTED as STR defines them), the numbers that
  feed decision point 2 in one table with their tags, figures with captions (if any), open issues, and a self-check
  against `phase3_selection/CLAUDE.md` (the JFC "≥ 2 selection approaches" and MVA items belong to T2 / the
  consolidation; say "not this work package" where they do not apply).
- Machine-readable results in `phase3_selection/outputs/<wp>/*.json` for every number another work package uses.
- **One final report** to the orchestrator (≤ 15 lines: artifact paths, verdicts, the decision-point-2 numbers, open
  issues). No interim reports: wait on your own jobs with a background wait. If you need a decision, write it in
  your artifact and end with it.
- A two-line entry in `phase3_selection/DAILY_NOTES.md` (append; date from `date`) when you finish.
