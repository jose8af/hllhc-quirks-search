# Plan: feasibility executor A (Anselm), Phase 1, chain port and benchmarks

Session Anselm, 2026-11-13. Scope: make the v1 chain run on Linux and measure its cost on worker `maxwell`.
No production samples. Compute: maxwell (≤ 4 concurrent jobs, `nice -n 10`); einstein only for solves/edits (`nice -n 19`).

Notation: `TT = stage2_C001_quirks/theory_track` (read-only), `QV2 = analyses/quirks_v2`.

## 0. Pre-findings (from the reading pass)
- PyPI lists `pyacts-48.0.0-cp312-cp312-manylinux_2_34_x86_64.whl` (26.9 MB). The hosts run glibc 2.39, so route R1
  (wheel) should work on linux-64 and the R3 source build is not needed unless the wheel lacks a component.
- `data/acts_stage4/g1/pythia_init/mpi_cp5_14tev_minbias.dat` (Pythia MPI init cache) and `data/acts_stage4/frozen/`
  are lost with v1 `data/`; Stage-2/3 inputs (`data/sim/npz`, `data/sim_stage3/inputs`) are lost too.
- M3 timings on record that can be re-run without lost data (to be confirmed): `acts/scripts/smoke_test.py 400 200`
  (39 s wall, INSTALL_CHECK §8 and `smoke_test_output.txt`); G1 per-PU-event chain time 4.83 s, 1 process
  (`run_stage4.py` timing constants); Stage-1 numerics `M2_single.py` (0.1×10³ s, NUMERICS.md).

## 1. Copy (task 1)
1. `rsync` from TT to QV2 at the same relative names: `analytic/`, `sim/`, `acts/`, `code/`.
   Exclude: `.pixi/`, `__pycache__/`, `.numba_cache/`, `sim/mg_out/`, `review/` trees, `logs/` trees, `*.log`, `*.out`,
   generated `figures/` (except figures that are inputs, none expected), `acts/probe/` (scratch: downloaded docs and
   dry-run locks), `analytic/numerics/results/raw/` (outputs), `analytic/novelty_sources/` (third-party papers),
   session logs. Keep code, configs, cards, UFO models, job lists, frozen inputs, small result JSON that code reads.
2. Check by grep that every relative `data/...` read still resolves from `QV2/` (QV2/data → cajuela). Small tracked v1
   inputs that live in `TT/data/` (e.g. `sim/lhapdf/*.info`) are NOT copied into cajuela by me unless a smoke test needs
   them; listed in provenance.
3. Write `QV2/CHAIN_PROVENANCE.md` (source commit, include/exclude lists and reasons, file count, size; target < 60 MB).

## 2. linux-64 pixi workspaces (task 2)
- In the copies: `pixi.toml` (TT env, copied to `QV2/` — but `QV2/pixi.toml` already exists: inspect it first; if it
  is the JFC analysis env, put the TT env in `QV2/envs/tt/` or add it as a named feature; decide and log),
  `sim/pixi.toml` (envs `mg`, `ana`), `acts/pixi.toml`.
- Add `linux-64` (keep `osx-arm64`), `pixi lock` on einstein at `nice -n 19`, `pixi install` (envs under the
  workspace `.pixi/` on `/home/users/jdochoa`, same path on all nodes; cache `$PIXI_CACHE_DIR`).
- Diff linux-64 vs the recorded osx-arm64 versions; record every changed version and why.

## 3. pyacts on Linux (task 3)
- Install `pyacts==48.0.0` from the manylinux wheel; run `acts/scripts/smoke_test.py 400 200` (the v1 install check)
  on maxwell. Check imports of Fatras, digitisation, seeding, CKF, geometry/Blueprint, HepMC3 reader.
- Only if the wheel fails: R3 source build on maxwell (`/var/tmp/jdochoa/` → `/home/users/jdochoa/sw/acts-48.0.0/`).
- Record API differences with file:line in the copies.

## 4. macOS-only launchers and `/Users/jochoafl` paths (task 4)
- grep the copies for `/Users/jochoafl`, `/Volumes/`, `caffeinate`, `DYLD_`, `launchd`, `osascript`, `#!/bin/zsh`,
  `darwin`; fix code paths (derive from `__file__` or `tools/env.sh` variables), leave records (logs) alone (they are
  excluded anyway). List every change.

## 5. Smoke tests on maxwell (task 5)
Outputs under `QV2/data/feasibility/chain/<test>/` (directories created with final names; files `.part` → rename;
markers in `QV2/ledger/markers/`).
1. Stage 3: `run_stage3.py` on a handful of events at 2-3 Λ values. Input: Basil's small samples in
   `data/feasibility/generators/` if present, converted by `make_inputs.py`; otherwise a minimal synthetic input npz
   with the schema `run_job` reads (pair momenta from the T2 toy or a fixed-kinematics generator). State which.
2. ACTS chain at PU 200 (Fatras + digitisation + CKF, incl. the PU overlay and the TDR top-up): `run_stage4 smoke`
   (SMB1/SMB2) or, if its dependencies on lost data block it, `code/run_chain.py` directly on a few events after
   regenerating the Pythia MPI init file.
3. The plane finder (per trial) on that output (`finder/production.process_trial` / `finder.py`).
4. No-pile-up single-interaction gun (C′₀-type gun, `run_g1b.py` kind `cp0`, or the chain with PU = 0).

## 6. Benchmarks on maxwell (task 6)
- Driver script `QV2/phase1_strategy/src/bench_chain.sh` / `bench_chain.py`: wraps each unit in `/usr/bin/time -v`,
  parses user+sys, wall, max RSS, writes JSON lines; ≥ 3 repeats at 1 concurrent job, then 4 concurrent.
- Units: Stage-3 per event vs Λ (detector-relevant Λ < 15 keV, e.g. 0.6, 1, 2, 5, 10 keV); ACTS chain per PU-200
  event; finder per trial; no-PU gun per event.
- M3 → cluster factor from a v1 job with a recorded M3 time (pick from the candidates in §0; cite file:line).

## 7. Projections (task 7)
- Table: events per ≤ 30 min job at < 1.6 GB RSS, bytes/event, per stage, from the 4-concurrent numbers.

## 8. Deliverables
- `outputs/feasibility/FEAS_A_chain_anselm.md` (JFC sections), `outputs/feasibility/benchmarks_chain.json`.
- `src/` benchmark scripts; `experiment_log.md` (`[Anselm]`, append with `>>`); session log
  `logs/executor_anselm_2026-11-13_14-50.md`.
- Priorities if short of time: 2 → 3 → 5 → 6 (ACTS PU 200 first) → 4 → 7.
- Blinding: signal events may be timed; no efficiency or pass count is computed or printed.
