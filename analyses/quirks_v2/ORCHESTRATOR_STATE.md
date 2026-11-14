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
| Gunnar | Phase-1 fixer, review cycle 4 → STRATEGY v5 (R1–R5 only) | opus | spawned 00:50 (14 Nov) | `phase1_strategy/outputs/STRATEGY_gunnar_2026-11-14_00-50.md`, `COMMITMENTS.md`, `…/FIX_REPORT_cycle4_gunnar.md` |

Phase-1 review history: cycle 1 ITERATE (Dagmar, M1–M35); 2 ITERATE (Eloise, N1–N18); 3 ITERATE (Felix, P1–P16);
4 ITERATE (Greta: 0 A, R1–R5 B). Versions kept: v1 Brigitte, v2 Dmitri, v3 Emeric, v4 Fiona, v5 Gunnar.
Cycle 5 panel (fresh; scope = verify R1–R5 + adopted C items + v4→v5 diff check): physics Hana, critical Hedwig,
constructive Hiroshi, arbiter Hugo → `STRATEGY_*_REVIEW_v5_*`. Iteration count: 4 done (STRONG WARN at 5, cap 10).
KEY FOR GATE A: expected outcome of the default plan = background ~10⁴ events (conversions), reach ~270 GeV at the
84 % edge on v1 placeholder efficiencies; day-15 pause expected. Q2 is the central decision. Gate-A draft text:
Gertrude's review, last part (must be updated with R1 numbers from v5).

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Reserved for cycle 5: Hana, Hedwig, Hiroshi, Hugo. Next free: Ingrid.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Gunnar reports: commit; spawn cycle-5 reviewers (3 in parallel) to verify R1–R5 against STRATEGY v5 with a
   v4→v5 diff check; then arbiter Hugo. Repeat until PASS.
2. Regression checklist of the root CLAUDE.md (orchestrator, after the arbiter's PASS).
3. Write `gates/GATE_A.md` (3 pages or less; the arbiter's list of Gate-A decisions is the backbone), bundle
   `gate-A`, update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
