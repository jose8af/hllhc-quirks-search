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
| Mireille | Phase-1 fixer, review cycle 8 → STRATEGY v9 (W1: rule-1 clarification, recomputed tables, self-test, text checker; verdict §3–§5 only) | opus | DONE (sha256 equal to expected, self-test 8/8, text check 45/45, O6 = Df-11 row; 33 hunks, 0 unattributed); cycle-9 panel Nadia, Nikolai, Nora spawned 07:25 | `phase1_strategy/outputs/STRATEGY_mireille_2026-11-14_06-55.md`, `src/strategy_budget.py`, `src/check_day15_text.py`, `budget_stdout_v9.txt`, `FIX_REPORT_cycle8_mireille.md` |

Phase-1 review history: cycles 1–8 all ITERATE (arbiters Dagmar, Eloise, Felix, Greta, Hugo, Johanna, Lena, Margaret);
A 11→4→1→0→0→0→0→0; B 24→14→15→5→3→1→4→1. Versions kept: v1 Brigitte … v8 Leopold, v9 Mireille.
Cycle 9 panel (fresh, per Margaret's verdict): physics Nadia (recompute tables from rule 1 independently: medians 1 %,
factors 5 %; run self-test), critical Nikolai (v8→v9 diff, stdout sha256 0ca4af15…003433d, byte-identity outside the
two tables, text checker), constructive Nora (final Gate-A package incl. 13 corrections), arbiter Odette.
Iteration count: 8 done. **CYCLE 9 IS THE LAST: if it does not PASS, stop and put the open list to the user.**
Settled: design, criteria, samples, budget 4,609 CPU-h / threshold 5,992 / 60 days, default (a), expected outcome.
Root cause of cycles 4–8 (found in cycle 8): rule 1 was ambiguous about SM processes without a day-15 sample; pinned
reading = all SM read through the Z(νν) pilot count; day-15 limit ≈ 12 Z(νν) pilot counts. This pinned reading must be
shown to the user at Gate A as an overridable default.
KEY FOR GATE A: expected outcome = background ≈ 0.7–1.0×10⁴ events (after CKF, as v1 counted) led by hard-scatter
conversions; reach below 243 GeV with the 0.17 normalisation width (bounds ≈ 180 GeV); day-15 pause expected; no
conversion rejection alone lifts it at v1's central decays-in-flight size (1–2 v1 counts). Q2 central.

Geant4 env (per-worker local, V13): schrodinger, landau, maxwell all installed, stamps match lock `edbcef24…`.
Install slot for the shared home: FREE, nothing pending.

Session names used so far: Ada … Brigitte, Casimir, Celeste, Cosima, Dagmar, Dmitri. Dolores, Dorothea, Edmund, Eloise, Emeric. Estelle, Fabian, Fabiola, Felix, Fiona. Florence, Gerald, Gertrude, Greta, Gunnar. Hana, Hedwig, Hiroshi, Hugo, Ingrid. Isolde, Ivan, Jasper, Johanna, Jules. Katya, Kenji, Klaus, Lena, Leopold. Ludmila, Magnus, Marcel, Margaret, Mireille. Reserved for cycle 9: Nadia, Nikolai, Nora, Odette. Next free: Oscar.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When Mireille reports: commit; spawn the cycle-9 panel; then arbiter Odette. PASS → steps 2–3.
   Not PASS → stop and put the open list to the user (do not start cycle 10 without the user).
2. Regression checklist of the root CLAUDE.md (orchestrator, after the arbiter's PASS).
3. Write `gates/GATE_A.md` (3 pages or less; the arbiter's list of Gate-A decisions is the backbone), bundle
   `gate-A`, update STATUS, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
