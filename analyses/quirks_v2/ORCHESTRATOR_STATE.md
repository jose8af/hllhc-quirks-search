# Orchestrator state (resume point)

A fresh session reads `prompt.md` (the brief), then this file, then resumes at "Next action".

**Updated:** 2026-11-16 10:47 -05 (measured) · **Branch:** `v2-jfc` · **Phase:** 1 (Strategy) — **review cycle 10 running (authorised by the user 2026-11-16)**

**Cluster:** the user confirmed it healthy on 2026-11-16; cajuela and ssh re-checked at 10:40; bundle
`repo-2026-11-16.bundle` written. Workers may be used again. Still in force: 10 GB cap, nothing heavy on einstein.

**Next action:** fixer Oscar (Opus) is producing STRATEGY v10 from the cycle-9 verdict §5 (E1–E14 + bookkeeping;
verdict: `phase1_strategy/review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`). When it reports: commit;
spawn ONE fresh critical reviewer (Opus) for the mechanical check of verdict §9; then a fresh arbiter (not below Opus).
PASS → regression checklist, `gates/GATE_A.md` from `gates/GATE_A_DRAFT.md` (cite v10; "cycle 9: a stale count, fixed
in v10"), bundle, STATUS, stop for Gate A. ITERATE at cycle 10 = hard cap → go to the user, no cycle 11.
If a session resumes and no v10 file `phase1_strategy/outputs/STRATEGY_oscar_*.md` with a
`FIX_REPORT_cycle9_oscar.md` exists, re-spawn the fixer. Session names used through Oscar; next free: Pauline.

**Clock warning:** times in `LOG.md` and in file names before 2026-11-14 01:20 are sequence labels, not clock times;
git commit times are authoritative. Always call `date` before writing a time.

Read `LOG.md` entry "15:12 — INTERRUPTION" for the constraints in force (10 GB cap, nothing heavy on einstein, one
pixi install at a time, at most 3 subagents).

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
