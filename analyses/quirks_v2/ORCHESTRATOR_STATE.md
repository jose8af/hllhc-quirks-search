# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-13 15:50 -05 · **Branch:** `v2-jfc` · **Phase:** 1 (Strategy), step EXECUTE (feasibility, resumed after the 15:12 interruption)

**Read `LOG.md` entry "15:12 — INTERRUPTION" first: it holds the constraints now in force (10 GB cap, nothing heavy on einstein, one pixi install at a time, modest number of subagents).**

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

## Active subagents (at most 3 at a time; nothing heavy on einstein)
DONE and committed: investigators D1–D6 + `FRAMING.md` (`980d207`); feasibility C runner (`0ff12df`), B generators/Geant4
(`6c1b760`), A chain (`3502634`). Reports: `phase1_strategy/outputs/feasibility/FEAS_{A,B,C}_*.md` + `benchmarks_*.json`.

| name | role | model | state | writes |
|---|---|---|---|---|
| Brigitte | Phase-1 strategy executor | fable | spawned 17:55 | `phase1_strategy/outputs/STRATEGY_brigitte_2026-11-13_17-55.md`, `COMMITMENTS.md` |

Geant4 env (per-worker local, V13): schrodinger OK, landau OK (17:07), maxwell installing (background, 17:55).
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada, Agnes, Albert, Alfred, Amara, Andrzej, Anselm, Basil, Boris, Brigitte. Next free: Casimir.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Brigitte reports: read the summary, check `COMMITMENTS.md` covers every MUST/SHOULD item, commit.
2. Read `agents/{physics_reviewer,critical_reviewer,constructive_reviewer,arbiter,fixer}.md`; run the 4-bot panel
   (3 reviewers in parallel = the concurrency cap; then the arbiter, on fable if the panel is contentious);
   iterate with a fixer and a fresh reviewer until PASS; numbered re-review artifacts.
3. Run the regression checklist of the root CLAUDE.md myself.
4. Write `gates/GATE_A.md` (3 pages or less), bundle (`gate-A`), update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
