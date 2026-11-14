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
| Jules | Phase-1 fixer, review cycle 6 → STRATEGY v7 (U1 + 10 C items) | opus | spawned 03:40 (14 Nov) | `phase1_strategy/outputs/STRATEGY_jules_2026-11-14_03-40.md`, `…/FIX_REPORT_cycle6_jules.md` |

Phase-1 review history: cycles 1–6 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo, Johanna); merged A
11→4→1→0→0→0; merged B 24→14→15→5→3→1 (U1). Versions kept: v1 Brigitte … v6 Ingrid, v7 Jules.
Cycle 7 panel (fresh, narrow per Johanna's verdict §12): physics Katya, critical Kenji, constructive Klaus, arbiter Lena
→ `STRATEGY_*_REVIEW_v7_*`. Iteration count: 6 done (strong-warn level passed; hard cap 10 → ESCALATE to the user if
cycle 9 still does not pass).
KEY FOR GATE A: expected outcome of the default plan = background ≈ 0.7–1.0×10⁴ events led by hard-scatter
conversions; with the strategy's own 0.17 normalisation width the reach is below 243 GeV (existing bounds ≈ 180 GeV);
day-15 pause expected; the day-15 reading is on all own hits before CKF (×5–50 above v1's credited basis). Q2 is the
central decision (optional rider: earlier decision at day 7, +7 CPU-h). Approve 4,609 CPU-h (4,616 with rider),
threshold 5,992 (6,001), 60 days incl. the pause. Gate-A candidate text: Jasper's review §5 — must be cut from 2,590
words to 3 pages and corrected per Johanna's verdict §9 (11 corrections) and the cycle-7 outcome.

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Isolde, Ivan, Jasper, Johanna, Jules. Reserved for cycle 7: Katya, Kenji, Klaus, Lena. Next free: Leopold.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Jules reports: commit; spawn the cycle-7 narrow panel; then arbiter Lena. Repeat until PASS.
2. Regression checklist of the root CLAUDE.md (orchestrator, after the arbiter's PASS).
3. Write `gates/GATE_A.md` (3 pages or less; the arbiter's list of Gate-A decisions is the backbone), bundle
   `gate-A`, update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
