# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-13 14:45 -05 · **Branch:** `v2-jfc` · **Phase:** 1 (Strategy), step EXECUTE (investigation + feasibility)

## Phase tracker
- [x] Preflight — PASS on re-run after the cajuela fix (`PREFLIGHT.md`)
- [x] Scaffold, state files, first bundle, first commit
- [ ] **Phase 1: Strategy — investigators + feasibility executors + strategy executor + 4-bot review → GATE A (human)**
- [ ] Phase 2: Exploration / regenerate the base — executor(s) + self-review + plot validator; decision point 1
- [ ] Phase 3: Processing, signal blind — parallel channels B1–B7, T1, T2, each 1-bot; consolidation; PREREG_v2 (4-bot, hash, notify user)
- [ ] Phase 4a: Expected — production, closure verdicts; executor + note writer + typesetter + 4-bot+bib
- [ ] Phase 4b: selection rule on optimisation half — executor + note writer + typesetter + 4-bot+bib → GATE B (human)
- [ ] Phase 4c: evaluation half — executor + note writer + 1-bot (escalate to 4-bot per JFC 06 §6.4)
- [ ] Phase 5: AN + journal paper + Zenodo-ready package — executor + note writer + typesetter + 5-bot + adversarial 25-question review → GATE C (human)

## Active subagents (session name · role · output)
| name | role | model | writes |
|---|---|---|---|
| Ada | investigator: repo, READMEs, REPRODUCE | opus | `phase1_strategy/outputs/digests/D1_reproduce_ada.md` |
| Agnes | investigator: paper v0.4, novelty audit, ISSUES + bird's-eye framing | opus | `…/digests/D2_paper_agnes.md`, `…/outputs/FRAMING.md` |
| Albert | investigator: UNRESOLVED.md, book Part VI, checks | opus | `…/digests/D3_corrections_albert.md` |
| Alfred | investigator: v1 frozen record | opus | `…/digests/D4_v1_record_alfred.md` |
| Amara | investigator: stage documents (analytic, sim, stage3, acts) | opus | `…/digests/D5_stages_amara.md` |
| Andrzej | investigator: decision-history logs (grep digest) | sonnet | `…/digests/D6_history_andrzej.md` |
| Anselm | feasibility executor A: pixi, linux-64 port, pyacts, runner, pod template, chain benchmarks | opus | `…/outputs/feasibility/FEAS_A_env_anselm.md` |
| Basil | feasibility executor B: MG5_aMC + Pythia 8 + LHAPDF, Geant4 route, generator benchmarks | opus | `…/outputs/feasibility/FEAS_B_generators_basil.md` |

Session names used so far: Ada, Agnes, Albert, Alfred, Amara, Andrzej, Anselm, Basil. Next free: Boris.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When all digests and both feasibility reports are on disk: read them (summaries only), commit.
2. If a feasibility item failed: escalate model/effort for the retry (brief §4), log in `MODEL_LEDGER.md`.
3. Read `agents/executor.md` (done), spawn the strategy executor (Boris, model fable: schedule + acceptance
   criteria are error-prone) → `phase1_strategy/outputs/STRATEGY_boris_<date>.md`, `COMMITMENTS.md` filled.
4. Read `agents/{physics,critical,constructive}_reviewer.md`, `arbiter.md`; run the 4-bot panel; iterate to PASS.
5. Write `gates/GATE_A.md` (3 pages or less), bundle, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
