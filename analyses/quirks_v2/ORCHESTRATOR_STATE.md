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

## Active subagents (at most 3 at a time; each uses one worker; nothing heavy on einstein)
Investigators Ada, Agnes, Albert, Alfred, Amara, Andrzej: DONE, digests D1–D6 and `FRAMING.md` committed (`980d207`).

| name | role | model | worker | state | writes |
|---|---|---|---|---|---|
| Anselm | feasibility A: chain smoke tests and benchmarks (envs and port edits are done) | opus | maxwell | resumed 15:50 | `phase1_strategy/outputs/feasibility/FEAS_A_chain_anselm.md`, `benchmarks_chain.json` |
| Basil | feasibility B: MG5/Pythia/LHAPDF test generation and benchmarks, NLO K-factor route; Geant4 env reinstall LAST, only when told he holds the install slot | opus | schrodinger | resumed 15:50 | `…/FEAS_B_generators_basil.md`, `benchmarks_generators.json` |
| Boris | feasibility C: finish runner validation (mini-campaign, kill/resume, memory test, marker latency, pyhf timings) | opus | landau | resumed 15:50 | `tools/runner/`, `…/FEAS_C_runner_boris.md` |

Install slot for the shared home (one pixi install at a time): FREE, nothing pending.
Geant4 env: per-worker local install at `/home/scratch/jdochoa/envs/g4` (user decision 16:00, V13). schrodinger: Basil, now.
landau and maxwell: after Boris and Anselm finish their benchmarks there (Basil or a follow-up does it; check the stamp files).

Session names used so far: Ada, Agnes, Albert, Alfred, Amara, Andrzej, Anselm, Basil, Boris. Next free: Brigitte.
pixi 0.84.2 at `~/.pixi/bin`; every shell sources `tools/env.sh`.

## Campaigns running
None. No production before Gate A.

## Pending verdicts / open escalations
None.

## Next action
1. When all digests and both feasibility reports are on disk: read them (summaries only), commit.
2. If a feasibility item failed: escalate model/effort for the retry (brief §4), log in `MODEL_LEDGER.md`.
3. Read `agents/executor.md` (done), spawn the strategy executor (Brigitte, model fable: schedule + acceptance
   criteria are error-prone) → `phase1_strategy/outputs/STRATEGY_brigitte_<date>.md`, `COMMITMENTS.md` filled.
4. Read `agents/{physics,critical,constructive}_reviewer.md`, `arbiter.md`; run the 4-bot panel; iterate to PASS.
5. Write `gates/GATE_A.md` (3 pages or less), bundle, notify the user, **stop for Gate A**.

## Standing rules to remember
- Never rename a directory on cajuela. Files: `.part` → rename → marker.
- Daily: `STATUS.md`, repo bundle to `/nfs/cajuela/jdochoa/quirks_v2/backup/` (keep last 7 + one per gate).
- Before spawning anything: commit. Before any phase: read the JFC files deferred in `DEVIATIONS.md` V11.
- Weekdays 08:00–19:00: Argo parallelism at most 9; check `who`/load first; graphical session on a node → 3 jobs there.
