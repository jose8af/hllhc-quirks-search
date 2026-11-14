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
| Leopold | Phase-1 fixer, review cycle 7 → STRATEGY v8 (family V1: script-printed day-15 table + text S2–S19 + 14 C items) | opus | spawned 05:00 (14 Nov) | `phase1_strategy/outputs/STRATEGY_leopold_2026-11-14_05-00.md`, `…/FIX_REPORT_cycle7_leopold.md`, `budget_stdout_v8.txt` |

Phase-1 review history: cycles 1–7 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo, Johanna, Lena);
A 11→4→1→0→0→0→0; B 24→14→15→5→3→1→4. Versions kept: v1 Brigitte … v7 Jules, v8 Leopold.
Cycle 8 panel (fresh, narrow per Lena's verdict): physics Ludmila (recompute the day-15 table and the (c) grid),
critical Magnus (v7→v8 diff, greps, script), constructive Marcel (Gate-A package against the table), arbiter Margaret.
Iteration count: 7 done. **ESCALATION RULE: if cycle 9 does not PASS, stop and put the open list to the user (cap 10).**
Settled per the cycle-7 arbiter: design, criteria, samples, budget 4,609 CPU-h / threshold 5,992 / 60 days, default
(a), expected outcome. Open: only the human-facing description of the day-15 decision (family V1).
KEY FOR GATE A: expected outcome = background ≈ 0.7–1.0×10⁴ events (after CKF, as v1 counted) led by hard-scatter
conversions; reach below 243 GeV with the 0.17 normalisation width (bounds ≈ 180 GeV); day-15 pause expected (reads
before CKF, ×5–50 higher, on an assumed pair efficiency); no conversion rejection alone lifts the pause at v1's
central decays-in-flight size (that term rests on 1–2 v1 counts). Q2 central. Gate-A candidate text: Klaus's review
part 3 (1,499 words) + Lena's 11 corrections + the cycle-8 outcome.

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Isolde, Ivan, Jasper, Johanna, Jules. Katya, Kenji, Klaus, Lena, Leopold. Reserved for cycle 8: Ludmila, Magnus, Marcel, Margaret. Next free: Mireille.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Leopold reports: commit; spawn the cycle-8 narrow panel; then arbiter Margaret. PASS → steps 2–3.
   ITERATE → one more fix + cycle 9; if cycle 9 does not pass → stop and ask the user.
2. Regression checklist of the root CLAUDE.md (orchestrator, after the arbiter's PASS).
3. Write `gates/GATE_A.md` (3 pages or less; the arbiter's list of Gate-A decisions is the backbone), bundle
   `gate-A`, update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
