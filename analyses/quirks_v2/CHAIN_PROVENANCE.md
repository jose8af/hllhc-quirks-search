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

### Phase 2, channel (ii) (executor Sebastian, 2026-11-16 13:09)
- No file under `analytic/`, `sim/`, `acts/`, `code/` or `envs/` was modified.
- `phase2_exploration/src/p1/nm_kernel_t44.py` is a copy of `analytic/numerics/nm_kernel.py` with two changes (diff
  ≈ 15 lines): `mdot()` truncates every product and the result to a 44-bit mantissa (P1 floor test 2, STR §4.15), and
  `CODE` is an absolute path to `analyses/quirks_v2/code`.
- Phase-2 jobs import the chain code read-only, with `PYTHONDONTWRITEBYTECODE=1` and `NUMBA_CACHE_DIR` in job scratch.
- Node-local generator env (not chain code): maxwell `/home/scratch/jdochoa/envs/herwig`, manifest and lock in
  `phase2_exploration/src/herwig/pixi.{toml,lock}` (lock sha256 8d045f81…66a). Herwig 7.3.0 / ThePEG 2.3.0 for [DP5];
  Resummino 3.1.2 (conda-forge build h154ca16_2, sha256 c58d442d…e23d) as the fixed-order reference of S2-a validation 2.
  Package checksums: retrieval_log #21.

### Phase 2, channel (iii) (Tatiana, 2026-11-16 13:34): tt̄ samples with forced W decays, run-time injection only
- What: two entries added to `s4pu.SM_SAMPLES` **at run time** by `phase2_exploration/src/p2c_hs0.py` (`FORCED_TT`):
  `ttbar_1l_pos` = the `ttbar_1l` process lines + `24:onMode = off`, `24:onPosIfAny = 11 13 15`, `24:onNegIfAny = 1 2 3 4 5`;
  `ttbar_1l_neg` = the charge conjugate. The file `acts/stage4/code/s4pu.py` is **not edited** (0 lines of diff): channel (i)'s
  C1 campaigns record its sha256 while they run, and v1's own `gen_d123.py` injects its extra processes the same way.
- Why: 23.7 generator tries per kept event instead of 48.3 (strategy addendum 1 §3.3). The `ttbar_1l` one-lepton test of
  `HardScatter.generate` does not apply to the new names; every forced event has exactly one leptonic W by construction
  (0 of 7,100 tries failed the test, campaign p2-c-prof).
- If adopted for production: the same two entries (and their analogues for tt̄ 2ℓ, tW, t-channel) go into `SM_SAMPLES`
  in the file, 2 lines per sample, at the v2 code freeze.

## 2026-11-16 16:14 `phase2_exploration/src/g4/g4hv.cc`: option `allx` (Xavier, channel (iii))
- **What.** New optional last argument `allx` of the `prim` mode (in the place of `exit`): a record is written for every primary, also for one that ends without a vertex. Its `V` line then carries the pseudo-process `LeftWorld` (r > RMAX or |z| > 2700 mm) or `TimeLimit` (t > 25 ns) and the point where the primary was dropped, followed by all its crossings of sensitive surfaces as `X` lines. Products are recorded at the vertex and killed, as without `exit`.
- **Why.** Half-turn study (`phase2_exploration/outputs/HALF_TURN_xavier_2026-11-16_16-08.md`): Geant4 crossings of every charged particle as the reference for what Fatras records; then the looper gun (`p2x_looper_chain.py`).
- **Size.** 18 changed lines (diff against the previous file: 1 flag, 5 comment lines, 10 lines in the stepping action, 1 line in `main`, 1 usage line). **Default behaviour unchanged**: without `allx` no code path differs.
- **Hash.** sha256 before fd10a8906ba1d266…, after b5ad93a0eac98ace…. The node-local build is keyed on the source hash (`g4hv.sh`), so the new binary is `/home/scratch/jdochoa/cache/g4hv/3761b0df385463b0/`; the old one stays. No pilot or production sample was made with either; B1 jobs record this hash in their meta.
- Not part of the v1 chain (`acts/`, `sim/`): no file there was modified.
- 2026-11-16 17:18 `g4/g4hv.cc`, option `allx` only (Xavier): a primary that ends with no killing process other than transportation (first run: 0.9 % of central loopers, all π± / K±, with on average 13 counting-surface crossings; presumably Geant4's own killing of looping tracks in the field [U: not read from a Geant4 message]) had no record and lost its crossings; it now gets a `V` line with the pseudo-process `Stopped` at its last step and its `X` lines (+ 12 lines; default behaviour still unchanged). sha256 b5ad93a0eac98ace… → 55b434a3032c125d….
- 2026-11-16 17:32 (Albert, channel (iii)) **Three files of Xavier's B1 code changed; none is in the v1 chain (`acts/`, `sim/`) and none is in `frozen_from_launch` of the running pilot** (`tools/runner/examples/p2x/pilot/PLAN_p2-c-pilot_mb-znn.json`). In all three the default behaviour is unchanged (optional arguments; regression jobs `p2-c-pa-g4-reg`, `p2-c-pa-b1-reg-difc`).
  - `phase2_exploration/src/p2x_g4prod.py` (165 → 197 lines; sha256 0428253a06d6b117… → 4ad5ae2f173e5b66…). **What:** optional trailing arguments `sel=ptlo:pthi:etalo:etahi` (fire only pool rows in that window) and `draw=weighted` (draw pool rows in proportion to their weight); meta records the window, the draw, the number of distinct pool rows fired and the firings per distinct row. **Why:** the low-p_T and 1 < |η| < 1.5 parents are in the wider pool `xpool_*` of `pilot.mb`, and the hard-scatter parents of addendum v3 P2 are drawn in proportion to the event weight. Without the options the random-number sequence and every array are as before.
  - `phase2_exploration/src/p2x_b1.py` (296 → 320 lines; 13183f07f1cbc4bc… → see the PLAN of the B1 campaigns). **What:** optional 12th argument = seam window of the hybrid parent (default: the validated 0.005 ns), recorded in meta; two new per-event arrays `ev_mode` and `n_parent_inj`; pool selection and draw of the vertex file copied into meta. **Why:** each event must record its hand-over mode and the seam window (Phase 3). The hits and every earlier array are unchanged; the content hash of a file changes because two arrays are added.
  - `phase2_exploration/src/p2x_validate.py` (263 → 345 lines; d49ef21773bef56d… → see the PLAN). **What:** for files that carry `ev_mode`, "no parent hit beyond the vertex radius" is required of radius-cut events only and "no parent hit later than the vertex time" of the time-cut / hybrid events; parent phase space and road condition taken from the vertex file's recorded pool selection; new mode `hspool-x`; more fields of vertex files passed through. Files without `ev_mode` are checked as before.
  - New files (no change of existing code): `phase2_exploration/src/p2a_hspool.py`, `p2a_b1_campaigns.py`.
