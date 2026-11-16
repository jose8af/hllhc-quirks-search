# Chain provenance: v1 stage code copied into quirks v2

Written by feasibility executor Anselm (Phase 1), 2026-11-13.

## Source
- Repository HEAD at copy time: `191be1052d3c86cf93ac29667f85c6e28d1a0f75` (branch `v2-jfc`). The v1 tree was unchanged
  through HEAD `980d2078…` (`git log 191be10..980d207 -- stage2_C001_quirks` is empty). The last commit that touched
  `stage2_C001_quirks/theory_track` is `d724a1c48e541f86fa15d61cc64414c3158706f8` (initial import).
- Source directory: `stage2_C001_quirks/theory_track/` (TT, read-only). Destination: `analyses/quirks_v2/` (QV2) at the
  same relative names, so that the v1 convention "run from TT; `data/…` is relative" becomes "run from QV2".
  `QV2/data` is the symlink to `/nfs/cajuela/jdochoa/quirks_v2/data`, so every relative `data/…` read or write of the
  copied code resolves to the v2 bulk area.

## What was copied
`rsync -a --exclude-from=<list>` of `TT/{analytic,sim,acts,code}/` → `QV2/{analytic,sim,acts,code}/`, plus
`TT/pixi.{toml,lock}` → `QV2/envs/tt/pixi.{toml,lock}` (the QV2 root `pixi.toml` is the JFC analysis environment, so the
TT environment lives in its own workspace; use `pixi run --manifest-path envs/tt/pixi.toml …` from QV2).

| directory | files | bytes |
|---|---|---|
| `analytic/` | 86 | 1,406,702 |
| `sim/` | 228 | 8,633,106 |
| `acts/` | 174 | 4,825,102 |
| `code/` | 54 | 493,014 |
| `envs/tt/` | 2 | 126,822 |
| `figures/` | 1 | 114,176 |
| **total** | **545** | **15.6 MB** (target < 60 MB) |

Counts: `find <dir> -type f -not -path '*/.pixi/*'` before any environment install and after the edits listed below
(5 launcher scripts and the Windows bundle tool removed).

Kept: all `.py`/`.sh` code, configuration (`pixi.toml`/`pixi.lock`, MG cards, Pythia cards, UFO models, digitisation and
seeding JSON, geometry JSON, `surfaces_s3.json`), job lists (`sim/stage3/jobs/*.json`, `acts/stage4/jobs/*.json`), frozen
inputs (`acts/stage4/frozen_inputs.json`, `acts/stage4/analysis/inputs/*.json`), the small result JSON that code reads
(`sim/results/*.json`, e.g. `xsec.json`; `sim/stage3/results/*.json`; `analytic/predictions.json`), code-side `.npz`
inputs (`code/T1_cosmo_grid.npz`, `code/T1_running_strips.npz`) and the Markdown documents of each stage (plans, reports,
WP_RULE and its addenda, which some code hashes).

## What was left out, and why
| excluded pattern | why |
|---|---|
| `.pixi/`, `__pycache__/`, `.numba_cache/`, `*.pyc` | environments and caches; rebuilt |
| `sim/mg_out/`, `py.py` | MadGraph output trees (1.5 GB) and MG's parser table; regenerated |
| `review/` (all levels) | review records and reviewers' check scripts (v1 record; remain in TT) |
| `logs/`, `*.log`, `*.out` | run logs (MG, numerics, probes) — records, many with Mac paths |
| `figures/`, `*.png`, `*.pdf` | generated figures. One file of `TT/figures/` is a code input (`T3_ms_thickness.npy`, 114 kB, read by `analytic/numerics/FIX1_analysis.py:180` and `sim/stage3/scripts/val_v5.py:72`): copied to `QV2/figures/` (found by grepping for loads from `figures`) |
| `acts/probe/` | E5 scratch: downloaded ACTS docs/sources, dry-run solves |
| `analytic/numerics/results/raw/` | Stage-1 raw outputs (M2/M5 npz); compared against from TT, not needed as inputs |
| `analytic/novelty_sources/` | third-party papers |
| `*_session_log.md` | v1 session logs |
| `TT/data/` (tracked 42 MB: `STAGE3_INDEX.json`, LHAPDF `.info` files, C12FC_v1 results, investigation JSON) | `QV2/data` is the cajuela area; the v1 tracked data files stay in TT and are read from there when needed (e.g. by a C1 comparison). Not staged onto cajuela by this executor |
| `TT/{stage5,paper,report,opendata,investigations,outputs}` | not part of the chain to port in Phase 1 |

## Edits made to the copies (Linux port; also listed in `phase1_strategy/outputs/feasibility/FEAS_A_chain_anselm.md`)
- Removed (macOS-only launchers, `#!/bin/zsh`, `caffeinate -i`, `shasum`, PIDs and dates built in):
  `acts/stage4/validation/{chain_c1,chain2_c1b,g1b_post_g3,prodstop_fri,prodstop_v2}.sh`.
- Removed (Windows USB bundle, hard-coded `/Volumes/J8A/quirks_sim/env`; the cluster has one OS):
  `sim/stage3/code/make_bundle.py`, `sim/stage3/bundle_src/`.
- `/Users/jochoafl/…/theory_track/sim` → `@SIM@` placeholder in the 18 MadGraph probe scripts `sim/probes/*.mg`;
  `sim/scripts/run_all.sh` resolves it at run time (`mgres()`).
- `DYLD_LIBRARY_PATH` → `LIBVAR` (`LD_LIBRARY_PATH` on Linux) in `sim/scripts/produce.py`, `sim/scripts/reshower.py`,
  `sim/probes/flowtest.py`, `sim/probes/flowtest2.py`.
- `sim/stage3/probes/_gen/T3_causal_fastmat.py`: absolute `sys.path` → `__file__`-relative.
- `acts/stage4/run_g1b.py` `probe_excluded()`: a missing `data/acts_stage4/fix_r1/f1r_summary.json` now raises instead of
  silently skipping the WP_RULE §5.4 item-10 exclusion (`QV2_ALLOW_NO_F1R=1` to override, dev only).
- `acts/stage4/run_stage4.py`, `run_a2fc.py`: defaults `--workers 7 → 4`, `--mem-gb 19.0 → 6.0`.
- `acts/stage4/run_stage4.py` (`QV2_S4_DATA`), `acts/stage4/code/s4sig.py` (`QV2_S3_DATA`): optional overrides of the
  v1 data locations; `acts/stage4/code/s4pu.py`: the Pythia MPI init file (a cache) moves to node-local
  `QV2_PYTHIA_INIT_DIR` (default `/home/scratch/jdochoa/cache/pythia_init`).
- Platforms: `envs/tt/pixi.toml`, `sim/pixi.toml` gain `linux-64`; `acts/pixi.toml` gains
  `{ platform = "linux-64", glibc = "2.34" }` (needed for the `manylinux_2_34` pyacts wheel). Lockfiles re-solved; the
  osx-arm64 sections are unchanged from v1.

**Freeze consequence.** Several edited files (`run_stage4.py`, `code/s4pu.py`, `code/s4sig.py`, `run_g1b.py`) are hashed
in v1's `frozen_inputs.json` / `analysis_freeze.json` / `CODE_FILES`. Their sha256 now differ from v1; any v2 result
needs the v2 re-freeze (REPRODUCE §5.1-4).

### Later edits (same session, after the provenance above was first written)
- `acts/scripts/smoke_test.py:35`: temp HepMC3 directory from `QV2_SMOKE_TMP` if set (else the v1 `acts/probe/smoke_tmp`).
- `analytic/numerics/M2_single.py:198`: process-pool size from `QV2_NPROC` (default 7, as in v1).
- The full list of port edits with reasons is in `phase1_strategy/outputs/feasibility/FEAS_A_chain_anselm.md` §2.4.

### Phase-2 edits (channel (i), executor Rosalie, 2026-11-16 11:56 -05)
- `acts/stage4/finder/production.py` `process_trial(..., premerge_min_nip2=None)`: optional pre-merge candidate store
  of STR §4.5 (a) [SD4] (every loose candidate with N_IP2 ≥ threshold, before grouping, with its hit list and hit
  table) returned as `res['pre']`. Additive: no RNG draw, no change of any other output when unused or used
  (bit-identity checked on one ρ = 2 event, campaign `p2-a-day0-pu2`, jobs `d0pu2-n1` vs `d0pu2-n1-nopm`).
  Diff: +36 lines, 2 changed.
- `acts/stage4/run_stage4.py` `run_pu_job(job, allow_interim, premerge=None)`: forwards the threshold and hands each
  trial's store to a streaming writer (`phase2_exploration/src/c1_pu_job.py`), so it is not kept in memory.
  Diff: +7 lines, 1 changed. Why: the ρ = 2 C1 jobs are also the B2 development sample (STR §4.1, §4.17 row 2).
