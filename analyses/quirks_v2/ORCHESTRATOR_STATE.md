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
| Ingrid | Phase-1 fixer, review cycle 5 → STRATEGY v6 (T1–T3 only) | opus | spawned 02:20 (14 Nov) | `phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md`, `COMMITMENTS.md`, `…/FIX_REPORT_cycle5_ingrid.md` |

Phase-1 review history: cycles 1–5 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo); merged A 11→4→1→0→0;
cycle 5 left T1–T3 (B, text only). Versions kept: v1 Brigitte … v5 Gunnar, v6 Ingrid.
Cycle 6 panel (fresh, narrow scopes per Hugo's verdict): physics Isolde (T1, T2), critical Ivan (v5→v6 diff, greps,
T3 figures), constructive Jasper (Q2 and Q4 as the human reads them), arbiter Johanna → `STRATEGY_*_REVIEW_v6_*`.
Iteration count: 5 done (STRONG WARN reached; cap 10).
KEY FOR GATE A: expected outcome of the default plan = background ≈ 0.7–1.0×10⁴ events led by hard-scatter
conversions; with the strategy's own 0.17 normalisation width the reach is below 243 GeV (existing bounds ≈ 180 GeV);
day-15 pause expected even with a conversion veto alone (decays in flight 385–647 > 300). Q2 is the central decision
(with optional rider: earlier decision at day 7, +7 CPU-h). Approve figure 4,609 CPU-h (4,616 with the rider),
threshold 5,992 (6,001), calendar 60 days incl. the pause. Gate-A draft text: Hiroshi's review §5 (update with v6).

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Reserved for cycle 6: Isolde, Ivan, Jasper, Johanna. Next free: Jules.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Ingrid reports: commit; spawn the cycle-6 narrow panel; then arbiter Johanna. Repeat until PASS.
2. Regression checklist of the root CLAUDE.md (orchestrator, after the arbiter's PASS).
3. Write `gates/GATE_A.md` (3 pages or less; the arbiter's list of Gate-A decisions is the backbone), bundle
   `gate-A`, update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
