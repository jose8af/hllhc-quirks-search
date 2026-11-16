# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-16 10:54 -05 (measured) · **Branch:** `v2-jfc` · **Phase:** 1 (Strategy) — **review PASSED (cycle 10); STOPPED AT HUMAN GATE A**

**Waiting for the user's Gate-A answers** (package `gates/GATE_A.md`): Q1–Q5, any override of Df-1…Df-11, whether
to keep sentence E6 of rule 1, and approval of the schedule (4,609 CPU-h, threshold 5,992, about 60 days; rider
variant 4,616 / 6,001). Do NOT start Phase 2, any production or any worker job before the user answers.
Artifact of record: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` (v10, sha256 d806bb36…020b779) +
`COMMITMENTS.md` + `budget_stdout_v9.txt`. Verdict: `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v10_quentin_2026-11-16_10-51.md`.

**Next action after the answers:** record them in `COMMITMENTS.md` (frozen at Gate A) and `LOG.md`; if E6 is dropped
or a default overridden, a fixer applies it and the change is logged; commit; bundle; read the deferred JFC files for
Phase 2 (DEVIATIONS V11); plan Phase 2 (week 1: C1, C2, cost measurements, pilot; day-5/7/12/15 decision points).
Carry into Phase 2: the deferred item Physics C-4 of cycle 9 (self-test 7 at ±5 %, more draws for the DIF rows) and,
if E6 is dropped, the precision rule. Fixer prompts must repeat the no-git rule (two agents ran a read-only git).
Cluster confirmed healthy by the user 2026-11-16; workers usable; 10 GB cap and "nothing heavy on einstein" stay.
Session names used through Quentin; next free: Rosalie.

**Clock warning:** times in `LOG.md` and in file names before 2026-11-14 01:20 are sequence labels, not clock times;
git commit times are authoritative. Always call `date` before writing a time.

Read `LOG.md` entry "15:12 — INTERRUPTION" for the constraints in force (10 GB cap, nothing heavy on einstein, one
pixi install at a time, at most 3 subagents).

## Phase tracker
- [x] Preflight — PASS on re-run after the cajuela fix (`PREFLIGHT.md`)
- [x] Scaffold, state files, first bundle, first commit
- [ ] **Phase 1: Strategy — done and review PASSED (cycle 10, 2026-11-16); waiting at GATE A (human)**
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
