# FEAS-A: the v1 analysis chain on Linux, and its cost on a cluster worker (executor Anselm)

Phase 1 feasibility, 2026-11-13 (interrupted 15:12 by the einstein OOM, resumed 15:40). Plan: `plan_anselm.md`.
Session log: `../../logs/executor_anselm_2026-11-13_14-50.md`. Decisions and failed attempts: `../../experiment_log.md`
(`[Anselm]`). Machine-readable: `benchmarks_chain.json` (benchmarks + `job_sizing`); raw records: `bench_logs/*.jsonl`
(each holds the full `/usr/bin/time -v` text and the output tail). Code provenance: `analyses/quirks_v2/CHAIN_PROVENANCE.md`.
All timings are on **maxwell** (Intel i5-7500, 4 cores, 7.5 GiB), `nice -n 10`, warm env and caches unless stated.
Tags: VERIFIED = measured here (log path given); ESTIMATE = my inference; UNVERIFIED = copied from a v1 document.

## 1. Summary

- **The chain runs on linux-64 with no source build.** `pyacts-48.0.0-cp312-cp312-manylinux_2_34_x86_64.whl` exists on PyPI
  and has every component the chain uses. The v1 install check passes (`smoke_test.py 400 200`, 4/4 runs), and so do
  the Stage-3 smoke (3 jobs), the Stage-4 smoke (`run_stage4 smoke`, 3/3 jobs) and every benchmark job (V4-1 closure
  passes in all 7 PU-200 jobs and the 10 no-PU jobs of 20,000 events). No API change was needed (VERIFIED).
- **Environments:** TT (`envs/tt`), `sim` (mg, ana) and `acts` are solved and installed for linux-64. The only changes
  are patch-level (python 3.12.15 → 3.12.16, numpy 2.5.3 → 2.5.4 in TT, numba 0.68.0 → 0.68.1, awkward 2.14 → 2.15 in
  `ana`); the osx-arm64 solves are unchanged. Section 2.2 (VERIFIED).
- **Headline costs per unit** (VERIFIED; mean ± sd, N in section 3):

  | unit | 1 job on the node | 4 concurrent | max RSS | output |
  |---|---|---|---|---|
  | PU-200 event, chain (Pythia overlay + Fatras + digi + seeding + CKF) | 12.9 ± 0.6 s | 13.5 ± 1.1 s | 0.46 GiB per job | 0.52 MB/event |
  | finder trial (`process_trial`, road 0.25) | 9.4 ± 0.8 s | 10.8 ± 1.0 s | (in the same job) | — |
  | B1 event = chain + 4 trials, whole job | 53.7 s | 60.4 s | 0.46 GiB | — |
  | Stage-3 event, F 500 toy, Λ = 1 / 3 / 5 / 10 keV | 0.62 / 18.5 / 67 / 35 s | 0.65 / 18.8 / 68 / 36 s | 0.21 GiB | 4-8 kB/event |
  | no-PU single interaction (C′₀ `pvpair`) / 10-µ gun | 10.7 / 14.1 ms | 11.5 ms (`pvpair`) | grows 13-17 kB/event | 8 / 14 kB/event |

- **M3 → cluster: there is no single factor** (section 3.2). Measured maxwell/M3 ratios: 1.29-1.43 for the compiled
  Pythia/ACTS parts of `smoke_test.py`; 2.7 for the production chain against the G1 record; 0.67 for M5 event 0;
  3.35 for the short M2 runs. Plan with the direct maxwell numbers above, not with converted v1 hours.
- **Job sizing** (≤ 25 min of work in a 30-min job, ≤ 1.6 GB): 24 PU-200 B1 events (v1 used 25); Stage 3 F 500 at
  Λ = 1 / 3 / 5 / 10 keV: ≈ 2,300 / 79 / 22 / 41 events, to be halved for the per-event tail; no-PU guns 80-110 k events,
  limited by RSS (section 3.7).
- **Blockers: none for Phase 2.** The open items are in section 5. The main ones: the ρ = 2 (B2) memory at production
  size is not measured (1.46 GiB at 1 event); the finder frozen configuration is absent; Stage 3 was timed only on toy
  inputs; and cross-platform ACTS random streams differ, so C1 can only be a statistical reproduction.

## 2. Method

### 2.1 Copy (task 1)
`rsync -a` of `TT/{analytic,sim,acts,code}` (TT = `stage2_C001_quirks/theory_track`, HEAD `191be10`) with code and
configuration only: 545 files, 15.6 MB (VERIFIED, `find -printf %s`). Also `TT/pixi.{toml,lock}` → `QV2/envs/tt/`, because the
QV2 root `pixi.toml` is the JFC analysis env, and one figure-directory input, `figures/T3_ms_thickness.npy`, which
`FIX1_analysis.py:180` and `val_v5.py:72` read. Include/exclude lists and reasons are in `CHAIN_PROVENANCE.md`. Run from
`QV2/`: `data/…` resolves to cajuela through the `QV2/data` symlink.

### 2.2 Environments (task 2)
`linux-64` was added to the three manifests; `acts` needs `{ platform = "linux-64", glibc = "2.34" }`, because pixi's
default (glibc 2.28) finds no pyacts wheel and `[system-requirements]` is rejected once platforms carry virtual packages.
Solved with pixi 0.84.2, lockfiles kept. Envs live under `/home/users/jdochoa` (workspace `.pixi/`), with the cache at
`$PIXI_CACHE_DIR`. Every version that differs from v1 (full lists: `lockdiff/{tt,sim,acts}.json`, from `src/lock_diff.py`; VERIFIED):

| workspace / env | package | v1 osx-arm64 | v2 linux-64 | why |
|---|---|---|---|---|
| TT | python / numpy / numba | 3.12.15 / 2.5.3 / 0.68.0 | 3.12.16 / 2.5.4 / 0.68.1 | manifest pins only `3.12.*` / `*`; newest builds at solve time |
| sim `ana` | python / numba | 3.11.17 / 0.68.0 | 3.11.18 / 0.68.1 | same |
| sim `ana` | awkward / awkward-cpp (PyPI, pulled by fastjet) | 2.14.0 / 57 | 2.15.0 / 58 | unpinned PyPI dependency |
| sim `mg` | — | — | identical | — |
| acts | python | 3.12.15 | 3.12.16 | `3.12.*` |
| acts | pyacts | 48.0.0 (macosx_26_0_arm64) | 48.0.0 (manylinux_2_34_x86_64) | Linux wheel, same version |
| acts | pythia8 / hepmc3 / pyhepmc / numpy / scipy | 8.312 / 3.3.1 / 2.16.1 / 2.5.4 / 1.18.1 | identical | — |

`six` is an osx-arm64-only dependency. The osx-arm64 sections of all three locks are unchanged from v1. The installs ran on
einstein (local disk) at 14:58-14:59, after an NFS install from maxwell proved too slow (section 3.8). That procedure is
now revoked: AGENT_RULES allows one install slot study-wide, started from a worker.

### 2.3 pyacts on Linux (task 3)
I used route R1 (the wheel); the route-R3 source build was not needed and not attempted. All of these are present
(import check, VERIFIED): `acts.Blueprint`, the `CylinderContainer/Layer/Static/MaterialDesignator` blueprint nodes,
`acts.json.readDetectorElementsFromJson`, `acts.fatras`, `addFatras`, `addDigitization`, `addSeeding` (incl. `SeedingAlgorithm.GridTriplet`),
`addCKFTracks`, `TrackSelectorConfig`, `CkfConfig`, `acts.examples.hepmc3`, and also `pythia8` 8.312 and `pyhepmc`. **API
differences: none.** The copied Stage-4 code (`run_chain.py`, `s4geo.py`, …) runs unmodified apart from the path edits of
section 2.4.

### 2.4 Port edits (task 4)
Every change to the copies (relative to `analyses/quirks_v2/`):

| file | change | why |
|---|---|---|
| `acts/stage4/validation/{chain_c1,chain2_c1b,g1b_post_g3,prodstop_fri,prodstop_v2}.sh` | removed | macOS launchers: `#!/bin/zsh`, `caffeinate -i`, `shasum`, v1 PIDs/dates (replaced by the v2 runner) |
| `sim/stage3/code/make_bundle.py`, `sim/stage3/bundle_src/` | removed | Windows/USB bundle, `/Volumes/J8A/quirks_sim/env` |
| `sim/probes/*.mg` (18 files, 72 occurrences) | `/Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track/sim` → `@SIM@` | Mac absolute paths |
| `sim/scripts/run_all.sh` | `mgres()` substitutes `@SIM@` into `probes/*.resolved.mg` before MG runs (also the t3 rerun line) | — |
| `sim/scripts/produce.py:262`, `reshower.py:79`, `sim/probes/flowtest{,2}.py` | `DYLD_LIBRARY_PATH` → `LIBVAR` (`LD_LIBRARY_PATH` unless `sys.platform == 'darwin'`) | HEPTools libs on Linux |
| `sim/stage3/probes/_gen/T3_causal_fastmat.py` (2 lines) | absolute `sys.path` → `Path(__file__).resolve().parents[4] / 'code'` | Mac path |
| `acts/stage4/run_g1b.py` `probe_excluded()` | a missing `data/acts_stage4/fix_r1/f1r_summary.json` now raises (override `QV2_ALLOW_NO_F1R=1`, dev only) | v1 silently skipped the WP_RULE §5.4 item-10 exclusion |
| `acts/stage4/run_stage4.py:768-769`, `run_a2fc.py:63-64` | `--workers 7 → 4`, `--mem-gb 19.0 → 6.0` | 4-core, 7.5 GiB workers |
| `acts/stage4/run_stage4.py:47`, `acts/stage4/code/s4sig.py:32` | optional `QV2_S4_DATA`, `QV2_S3_DATA` overrides of `data/acts_stage4`, `data/sim_stage3` | feasibility outputs under `data/feasibility/chain/` |
| `acts/stage4/code/s4pu.py` `mpi_init_lines()` | Pythia MPI init file → `QV2_PYTHIA_INIT_DIR` (default node-local `/home/scratch/jdochoa/cache/pythia_init`) | it is a cache: not on cajuela |
| `acts/scripts/smoke_test.py:35` | temp HepMC3 dir → `QV2_SMOKE_TMP` if set | keep the 28 MB temp file off NFS |
| `analytic/numerics/M2_single.py:198` | pool size from `QV2_NPROC` (default 7 as in v1) | 4-core workers |
| the three `pixi.toml` | `linux-64` platform | task 2 |

Not changed, but documented:
- ~20 other scripts with `ProcessPoolExecutor(7)` or `default=7` (Stage-1 numerics, Stage-3 post scripts): set the worker count explicitly when they are used.
- `MG nb_core = 6` in `produce.py` (Stage 2, Basil's area).
- Markdown records with `caffeinate` lines (history).

The edited `run_stage4.py`, `s4pu.py`, `s4sig.py` and `run_g1b.py` no longer match v1's freeze hashes, so v2 needs its own freeze.

### 2.5 Inputs (task 5)
**Stage 3 used a toy input.** No Stage-2 sample existed (`data/feasibility/generators/` absent at 15:05, 15:40 and 17:00).
`src/make_s3_toy_input.py` builds the runner's input schema from the v1 T2 toy (`code/T2_kinematics.py`: LO q q̄ → V* g,
q g → V* q on CT18NLO member 0 from `sw/lhapdf_data`, pT(QQ̄) > 200 GeV, |η_pair| < 2.5, unweighted, seed 20261113),
with 60 events each for F at m = 500 and 1000 GeV. Checks (VERIFIED):
- the pair mass rebuilt from the two quirk momenta equals the sampled M to 1e-6 GeV;
- pT ≥ 200.7 GeV;
- median γ* is 1.259 / 1.188, against 1.27 for v1 MG (UNVERIFIED, v1 `sim/stage3/README.md`).

Not physics: recoil, jets and the weights are placeholders.

**The other stages are self-contained.**
- Stage 4 generates its Pythia8 CP5 minimum bias on the fly (Poisson μ = 200 per crossing); no pre-generated sample is needed.
- The no-PU unit is the C′₀ `pvpair` toy: two charged particles from **one** Pythia minimum-bias interaction, aimed into the MET road, with no pile-up.
- A 10-µ particle gun (`run_chain.py gun`, no PU) is the second no-PU unit.

### 2.6 Benchmark method (task 6)
`src/bench_chain.sh <unit> <rep> <conc> …` → `src/bench_run.py` runs `nice -n 10 /usr/bin/time -v` in node-local
`/home/scratch/jdochoa/anselm_bench/<unit>_…_r<rep>c<conc>/`. It appends one JSON record per run to `bench_logs/<label>.jsonl`.

What is measured:
- CPU = user + sys of the whole process tree; wall is elapsed time.
- Max RSS = the largest single process (the B1 chain runs as a child of the TT-side job).
- Repeats: each unit runs ≥ 3 times alone on the node, then 4 copies run concurrently (different seeds where the code allows).
- Per-unit stage timings come from the codes' own records: `chain.timing` and `trials.times` in Stage-4 outputs, and per-event `cpu_s` in Stage-3 outputs.

Isolation: numba, pyc and Pythia-init caches are node-local, and no other job of mine ran alongside, with one exception
(section 3.2, M5). Summaries: `src/summarise_bench.py` → `benchmarks_chain.json`; `src/job_sizing.py` → `job_sizing` block.

## 3. Results

### 3.1 Smoke tests (task 5; VERIFIED)
| test | what ran | result | cost | outputs (markers in `ledger/markers/feasibility_chain/`) |
|---|---|---|---|---|
| v1 ACTS install check | `acts/scripts/smoke_test.py 400 200` (GenericDetector + μ gun + injected hits; Pythia8 PU-200 → HepMC3 → Fatras → digi; D111 geometry JSON) | **PASS B, C, D**, 4/4 runs | 37.18 ± 0.13 s CPU, 275 MiB (N = 3) | scratch only |
| Stage-3 propagation | `run_stage3.py run` on `src/jobs/s3_smoke.json`: F 500 toy, Λ = 1, 3, 10 keV, 4 events each, cfg BM | 3/3 jobs valid (deep check), all 12 events status 1, 170-177 hits per job | 5:02 wall, 213.5 s CPU, 311 MB, incl. a slow cold NFS start | `data/feasibility/chain/stage3_smoke/s3smoke/F_m500/L{1,3,10}_BM_c00.npz` |
| Stage-4 chain + finder at PU 200, incl. PU overlay and TDR top-up | `run_stage4 smoke`: SMB1 (2 events, ρ = 1, 4 roads, S6 dumps), SMB2 (ρ = 2: 2 PU-200 crossings, 2 roads), DENSlow (B-9 top-up variation from the dumps) | **SMOKE PASS**, 3/3 jobs | 6:44 wall, 391 s CPU, **1.46 GiB** (SMB2) | `data/feasibility/chain/acts_s4/prod/smoke/{SMB1,SMB2,DENSlow}/*.npz` (5.30, 4.01, 0.27 MB) |
| plane finder | inside every Stage-4 job (20 trials per benchmark job) | runs; per-trial times in 3.4 | — | — |
| no-PU single interaction / gun | `run_chain.py cp --topo pvpair`, `run_chain.py gun` (10 µ) | V4-1 pass in all 7 + 3 jobs of 20,000 events | 3.6 | scratch only |

Configuration caveat: v2 has no freeze candidate (`data/acts_stage4/frozen/` is lost), so the finder runs with the
planning values (road 0.25 rad), as v1's smoke did. Timings are representative; finder outputs are not physics results.
No signal was run through the chain. The SMB1/SMB2 outputs hold pile-up background only, and no per-rung count was looked at.

### 3.2 M3 → cluster conversion (task 6; VERIFIED unless tagged)
| v1 job with an M3 time on record | M3 time and where it is recorded | maxwell (this study) | maxwell / M3 |
|---|---|---|---|
| `smoke_test.py 400 200`, ACTS part (2 PU-200 events, Fatras + digi, 1 thread) | 3.0 s, v1 `acts/scripts/smoke_test_output.txt` | 4.3 s (4/4 runs identical to 0.1 s) | **1.43** |
| same script, Pythia8 CP5 init | 20.6 s, same file | 26.6 ± 0.1 s | **1.29** |
| same script, whole job | 39.37 s user, same file, last line | 37.18 ± 0.13 s CPU (N = 3) | 0.94 (the M3 Pythia event loop, 15.4 s vs 3.8 s, is anomalous; cause not recorded) |
| G1 production chain per PU-200 event, 1 process | 4.83 s, v1 `acts/stage4/G1_REPORT.md` §2 table (UNVERIFIED there) | 12.94 ± 0.60 s (N = 3) | **2.68** |
| `M5_li_blinearity.py` event 0 (long numba kernel) | 126.1 s, v1 `analytic/numerics/results/raw/M5_run.log:1` (1 worker) | 84.1 ± 0.7 s (N = 3)* | **0.67** |
| `M2_single.py all`, 416 runs of 0.2-0.6 s (numba, overhead-dominated) | Σ 82.2 s per-run walls, 7 processes, v1 `results/raw/M2/*.npz` field `cpu` | Σ 248.9 s, 1 process | 3.0 (median per run **3.35**) |

\* An orphaned worker of a stopped 30-event M5 job was busy on a second core during the three event-0 reps
(experiment log). The 4-concurrent tests below show at most a few % effect from such sharing for numba kernels.

**Reading (ESTIMATE).** The v1 times were taken on a fanless MacBook Air (`Joses-MacBook-Air-4.local`), mostly under
unrecorded load. So v1 "M3 CPU-h" are not a stable unit, and the factor depends on the code:
- ≈ 1.3-1.4 for Pythia and Fatras in the light test;
- ≈ 2.7 for the CKF/finder-heavy production chain;
- ≈ 2 for Stage 3 (section 3.5, toy against MG inputs);
- 0.7-3.4 for numba numerics.

**For planning, use the maxwell per-unit costs of this section and section 3.7.** If v1 Stage-4 hours must be converted anyway, the
multiplier is ≈ 2.7 × v1 1-process times. v1's 382 Stage-4 "CPU-h" are loaded job walls and must not be converted.

Numerics, Linux vs M3 (VERIFIED, `compare_M2.json`, `compare_M5.json`, smoke diff):
- **M5 event 0:** the 17 hit arrays agree to ≤ 1.2e-7 relative (≤ 0.58 µm).
- **M2:** 4,333 of 5,059 arrays are bit-identical and 688 agree to floating point (median relative difference 1e-17). **One conformal run (`B_g1.3_e3.162e-05_th90_conf256`) gives 2 crossings instead of 6**, and a few integer `prof` bins differ by 1-2. The result is identical in all 4 Linux runs.
- **smoke test:** Pythia output is bit-identical (37,120 / 36,907 particles). Fatras/vertex values differ slightly: vertex rms z 44.1 / 45.2 mm against 48.4 / 49.1 mm, input 45 mm; part B 61/62/60 against 59/62/64 hits. ESTIMATE: ACTS uses C++ `std::` distributions, which differ between libc++ (macOS) and libstdc++ (Linux).
- **Consequence:** v2 can reproduce v1 only statistically downstream of ACTS.

### 3.3 ACTS/Fatras + digitisation + CKF at PU 200, per event (VERIFIED, `bench_logs/s4pu_n5_roads4_rho1.jsonl`)
Unit: `src/bench_s4_pu.py`, i.e. `run_stage4.run_pu_job` on a B1-like job: 5 PU-200 events, ρ = 1, 4 roads (20 trials),
no dumps. Single runs use seeds 1001-1003; the concurrent run uses seeds 2001-2004.

| per PU-200 event (mean ± sd) | 1 job, N = 3 | 4 concurrent, N = 4 | slowdown | v1 M3 1-process (G1_REPORT, UNVERIFIED) |
|---|---|---|---|---|
| **chain total (wall)** | **12.94 ± 0.60 s** | **13.53 ± 1.09 s** | 1.05 | 4.83 s |
| · Pythia PU generation | 0.67 ± 0.03 | 0.72 ± 0.04 | 1.07 | 0.30 |
| · reader | 0.12 ± 0.00 | 0.13 ± 0.01 | — | 0.05 |
| · Fatras + digitisation | 2.53 ± 0.07 | 2.69 ± 0.12 | 1.06 | 0.97 |
| · seeding (GridTriplet) | 0.82 ± 0.04 | 0.85 ± 0.07 | 1.04 | 0.40 |
| · **CKF** | **7.43 ± 0.41** | **7.71 ± 0.80** | 1.04 | 2.69 |
| · output | 0.98 ± 0.04 | 1.05 ± 0.06 | 1.07 | 0.42 |
| job CPU / wall (5 events + 20 trials) | 274.9 ± 21.7 / 269.1 ± 21.2 s | 299.3 ± 27.7 / 302.4 ± 27.3 s | 1.09 / 1.12 | — |
| job max RSS | 459 ± 29 MiB | 444 ± 29 MiB | — | B1 1.5 GB budget (`run_stage4.py:65`) |
| output, compressed npz | 0.54 ± 0.10 MB/event | 0.52 ± 0.10 MB/event | — | — |

Further observations:
- **Startup.** With the Pythia MPI init file present (node-local cache), the fixed overhead per job is < 5 s. The first job on
  a node also creates the file (≈ 30 s, SMB1 in 3.1).
- **Cold start.** The first import of the acts env over a congested NFS took minutes (section 3.8).
- **Packing.** Filling all 4 cores costs ≈ 5 % on the chain.

### 3.4 Finder per trial (VERIFIED, `bench_logs/s4_trials.jsonl` from `trials.times`)
| per trial | 1 job (3 jobs × 20 trials) | 4 concurrent (4 jobs × 20 trials) |
|---|---|---|
| `find` (plane finder) | **9.44 ± 0.81 s** (p90 12.7 ± 2.7 s) | **10.79 ± 0.99 s** (p90 14.6 ± 2.3 s) |
| all timed parts (btl + find + flags + group + store) | 10.04 ± 0.91 s | 11.56 ± 1.09 s |
| TT side per trial incl. top-up, CKF removal, merging, packing | 10.19 ± 0.92 s | 11.71 ± 1.10 s |

The 4-concurrent penalty is ≈ 15 %: the finder is more memory-bound than the chain. The v1 references are t₁ = 4.25 s at
road 0.25 and 3.26 s at the freeze-candidate road 0.15 (M3, 4 workers, G1_REPORT, UNVERIFIED), and 8.02 s under the 7-worker
production load (`run_stage4.py:63`). At the frozen road the cost may be ≈ × 0.77 (ESTIMATE, v1 ratio); this is not measured (open issue 3).

### 3.5 Stage-3 string propagation per event versus Λ (VERIFIED, `bench_logs/s3_m*_L*.jsonl`, `bench_logs/s3_events.jsonl`)
Unit: one v1 runner job (`run_stage3.py run --workers 1`) on the toy input with the v1 p2 settings: cfg BM (3.8112 T +
material), luminous vertex, hmax 0.2, max_boost 1e-3 at Λ ≤ 5 keV and 1e-2 at Λ ≥ 7 keV, as in v1 `jobs/all.json`.
Λ ≥ 15 keV was not run, as instructed. Every rep uses the same events, so the spreads are machine noise. Per-event cost varies
×5-×10 between events (smoke at 10 keV: 12.3-69.1 s), so a 4-30-event mean has a sampling error of tens of % (ESTIMATE).

| m [GeV] | Λ [keV] | events/job | kernel CPU per event, 1 job (N = 3) | 4 concurrent | job wall, 1 job | max RSS | output/event | v1 M3, MG inputs (`STAGE3_INDEX.json`) |
|---|---|---|---|---|---|---|---|---|
| 500 | 1 | 30 | **0.621 ± 0.006 s** | 0.651 ± 0.014 s (N = 3) | 21.5 ± 0.3 s | 207 MiB | 4.4 kB | 0.334 s |
| 500 | 3 | 8 | **18.5 ± 0.2 s** | 18.8 ± 0.1 s (N = 3) | 150.7 ± 1.8 s | 207 MiB | 5.9 kB | 8.18 s |
| 500 | 5 | 4 | **67.2 ± 1.1 s** | 67.8 ± 0.7 s (N = 3) | 271.5 ± 4.5 s | 207 MiB | 8.0 kB | 32.3 s |
| 500 | 10 | 6 | **34.8 ± 0.3 s** | 36.0 ± 0.9 s (N = 3) | 211.3 ± 1.5 s | 208 MiB | 6.7 kB | 16.5 s |
| 1000 | 1 | 30 | — | 0.818 s (N = 1) | — | 207 MiB | 5.2 kB | 0.310 s |
| 1000 | 3 | 8 | — | 15.3 s (N = 1) | — | 207 MiB | 6.7 kB | 7.25 s |
| 1000 | 5 | 4 | — | 34.2 s (N = 1) | — | 207 MiB | 8.0 kB | 29.3 s |
| 1000 | 10 | 6 | — | 24.4 s (N = 1) | — | 206 MiB | 6.6 kB | 14.2 s |

Further observations:
- **Overheads.** The fixed overhead per job is ≈ 3 s warm (imports, numba cache). Filling the 4 cores costs 1-5 %, because the kernel is compute-bound.
- **Comparison with v1.** The maxwell/v1-M3 ratio is ≈ 1.9-2.3 at m = 500 (ESTIMATE: toy vs MG events, few events).
- **Cost shape.** Cost rises ≈ Λ^2.9 at fixed max_boost (1 → 5 keV, m = 500). The step to max_boost 1e-2 halves the cost at 10 keV, as in v1.

### 3.6 No-pile-up single interaction and particle gun, per event (VERIFIED, `bench_logs/{cp_pvpair,gun}_*.jsonl`)
| unit | per event (slope between 2,000 and 20,000-event jobs, N = 3 each) | 4 concurrent (20,000 events, N = 4) | job wall at 20,000 ev | RSS at 2,000 / 20,000 ev | output |
|---|---|---|---|---|---|
| C′₀ `pvpair` (one Pythia minimum-bias interaction, no PU) | **10.7 ms** | 11.5 ms (job 233.6 ± 1.1 s vs 215.1 ± 1.0 s alone: × 1.09) | 215.1 ± 1.0 s | 140 / 370 MiB | 8.2 kB/event |
| `gun`, 10 µ⁻ per event, pT 1-10 GeV, |η| < 2.5 | **14.1 ms** | — | 282.0 ± 0.4 s | 131 / 443 MiB | 14.0 kB/event |

Startup is ≈ 1-2 s. RSS grows by 12.6 kB (`pvpair`) and 17.3 kB (`gun`) per event, because the chain keeps every
event's output until the end. For these units **memory, not time, sets the job size**. v1 G1 recorded ≈ 3 ms per C′₀ event (UNVERIFIED).

### 3.7 Projected per-job sizes (task 7; VERIFIED inputs, projection ESTIMATE; `benchmarks_chain.json` → `job_sizing`)
Rule: units per job = (1,500 s − fixed overhead) / per-unit wall at 4 concurrent jobs per node. That is 25 minutes of work
inside the 30-minute limit, leaving 5 minutes for slow events, a cold NFS start and the marker. The cap is RSS ≤ 1.6 GB.

| stage | per unit at 4 concurrent | units per job | max RSS at that size | output per job |
|---|---|---|---|---|
| Stage 4 PU 200, B1 (chain + 4 finder trials per event) | 60.4 s | **24 events** (v1: 25) | 0.47 GiB (does not grow with N, ESTIMATE) | 12.4 MB |
| Stage 4 B2 (ρ = 2) | not benchmarked; 1-event smoke 206 s wall | ≈ 8 events (ESTIMATE from SMB2) | **1.46 GiB at 1 event; v1 3.9-4.0 GB at production size** | — |
| Stage 3, F 500, Λ = 1 keV | 0.651 s | 2,299 → use ≤ 1,100 (tail) | 0.21 GiB | 10 MB |
| Stage 3, F 500, Λ = 3 keV | 18.8 s | 79 → use ≤ 40 | 0.21 GiB | 0.5 MB |
| Stage 3, F 500, Λ = 5 keV | 67.8 s | 22 → use ≤ 11 | 0.21 GiB | 0.2 MB |
| Stage 3, F 500, Λ = 10 keV | 36.0 s | 41 → use ≤ 20 | 0.21 GiB | 0.3 MB |
| Stage 3, F 1000, Λ = 1 / 3 / 5 / 10 keV | 0.82 / 15.3 / 34.2 / 24.4 s | 1,818 / 97 / 43 / 61 → use half | 0.21 GiB | 9 / 0.7 / 0.3 / 0.4 MB |
| no-PU `pvpair` | 11.5 ms | 140 k by time, **112 k by RSS** → use ≤ 80 k | 1.5 GB at 112 k | 0.65 GB at 80 k |
| no-PU 10-µ gun | 14.1 ms (1 job) | 106 k by time, **83 k by RSS** → use ≤ 60 k | 1.5 GB at 83 k | 0.84 GB at 60 k |

Notes:
- **Stage 3 is not ready to schedule as is.** The "use half" factor covers the per-event spread (×5-×10). Stage-3 jobs produce only 0.2-10 MB each, against the brief's ≥ 10 MB per file, so several (point, Λ) chunks must be packed per job or merged afterwards. The v1 chunks were 92 / 42 / 17 events at Λ = 1 / 2 / 3-5 keV (M3 units); on maxwell they would run about 2 × longer.
- **Throughput (ESTIMATE).** 1,000 B1 events cost ≈ 16.8 core-h at 4 per node, i.e. ≈ 1.4 h wall on the 12 worker cores.

### 3.8 Infrastructure findings (VERIFIED)
- **Installs over NFS are slow.** A `pixi install` over NFS from a worker reached 46/148 packages in about 20 min. Meanwhile einstein `sda`, the rotational disk under the `sync` `/home` export, was 85-94 % busy at about 1.3 MB/s of small writes, with all 8 nfsd threads in D state. A concurrent writer (an NFS install from schrodinger, about 700 kB/s) stalled NFS reads for the whole lab: maxwell read at about 150 kB/s. The same installs on einstein's local disk took 5-27 s, but that is now forbidden (AGENT_RULES).
- **Cold starts are slow.** Under that congestion, the first Python process of an env on a node spent more than 8 min in D state reading about 75 MB. Once the env is warm, startup is a few seconds. I could not measure a true cold start on an idle server: maxwell's page cache was already warm when I resumed.
- **Killing jobs by name leaves orphans.** `pkill -f <script>` left a `multiprocessing` spawn worker running (ppid 1) for 13 min. The runner must kill process groups.

## 4. Validation
- **Functional.** All smoke tests pass (3.1). Every benchmark run exited with status 0 (63 `time -v` records in `bench_logs/`). V4-1 ingestion closure passed in all 7 PU-200 jobs and in the 7 `pvpair` and 3 gun jobs of 20,000 events. All Stage-3 events have status 1.
- **Bit-level against v1.**
  - Stage-1 numerics agree to 1e-17 (M2) and ≤ 1.2e-7 (M5), apart from the single conformal M2 run.
  - Pythia8 output is bit-identical.
  - ACTS-sampled quantities differ at the few-% level per event (3.2).
- **Benchmark integrity.**
  - Single-job reps with the same input give spreads below 2 % (Stage 3, M5, smoke test), so the timer and node are stable.
  - Concurrent runs used distinct seeds and their outputs differ (PU job sizes 0.42-0.62 MB/event), so no fork-duplication bug.
  - The `nice 10` jobs were the only load of mine on maxwell, except the M5 overlap noted in 3.2. I did not check for other users' load at each run; `uptime` showed a load average below 0.2 before the session.
- **Blinding.** No signal sample was produced or run. The Stage-4 smoke and benchmark outputs are pile-up only. No efficiency or per-rung pass count was computed or recorded. `run_stage4 smoke` prints per-rung counts for its pile-up trials; I filtered those lines out of everything I read and did not record them.

## 5. Open issues
1. **The B2 (ρ = 2) memory at production size is unmeasured.** It was 1.46 GiB at 1 event; v1 measured 3.9 GB. If it exceeds 1.6 GB, a B2 job needs a dedicated node slot (≤ 1 per node) or a code change. Measure a 10-event B2 job before Phase 2 production.
2. **There is no finder freeze candidate in v2.** The timings use road 0.25. The finder cost at the frozen road and `t_seed` is not measured, and v2 needs its own freeze (the edited files no longer match v1's hashes).
3. **Stage 3 was timed on toy kinematics only.** Re-time a few chunks on Basil's MG samples once they exist. Also re-run one v1 chunk with its v1 input for a bit-level and timing check: the inputs are lost, but the per-chunk md5 and CPU are in `STAGE3_INDEX.json`, e.g. `p1/F_m500/L2_B2_c05`.
4. **One M2 conformal run (N = 256) differs from v1** (2 vs 6 crossings). `M2_analysis.py` was not re-run, so whether M2's conclusions move is open (P1 floor tests).
5. **Cross-platform ACTS random streams differ**, so the C1 v1-subset reproduction criterion must be statistical, not event by event.
6. **The signal injection modes are not benchmarked** (`run_chain.py sig`, A5 full chain; A2 numpy digitisation). They need Stage-3 outputs registered in a `STAGE3_INDEX.json`-like index, via `QV2_S3_DATA`. Their per-event cost is ESTIMATE ≈ PU event + 0.1 s (v1 G1).
7. **True cold-start time on an idle NFS server is not measured.** A per-node warm-up job is recommended.
8. **About 20 scripts still default to 7 workers**, and MG `nb_core = 6`. Set these per job.
9. **The `pixi run` wrapper adds the NFS manifest/lock check to every job start**, unmeasured. The runner could call the env's `python` directly.
10. **The M3 smoke test's Pythia event loop (15.4 s vs 3.8 s here) is unexplained.** It does not affect production numbers.

## 6. Code reference (exact commands)
Run from einstein only as `ssh -x maxwell '…'`; `S=$QV2/phase1_strategy/src`; each shell first sources `$REPO/tools/env.sh`.

- **C1 lock solve and version diff.** Lock solve (einstein, 14:50, before the rules changed): `cd $QV2/<envs/tt|sim|acts> && nice -n 19 pixi lock`.
  Version diff: `python3 -I $S/lock_diff.py <new lock> <v1 lock> > lockdiff/<name>.json`.
- **C2 install (record only; now forbidden on einstein).** `nice -n 19 ionice -c3 pixi install [-e mg|ana]` (einstein, 14:58).
- **C3 toy Stage-3 inputs and job lists.**
  - Inputs: `pixi run --manifest-path envs/tt/pixi.toml python $S/make_s3_toy_input.py data/feasibility/chain/stage3_inputs F <500|1000> 60`.
  - Job lists: `python3 -I $S/make_s3_bench_jobs.py` → `$S/jobs/*.json`.
- **C4 Stage-3 smoke.**
  `NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s3 pixi run --manifest-path envs/tt/pixi.toml python sim/stage3/code/run_stage3.py run --jobs $S/jobs/s3_smoke.json --workers 3 --inputs data/feasibility/chain/stage3_inputs --out data/feasibility/chain/stage3_smoke`
- **C5 Stage-4 smoke.**
  `QV2_S4_DATA=$QV2_DATA/feasibility/chain/acts_s4 NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s4 PYTHONPYCACHEPREFIX=$QV2_SCRATCH/cache/pyc QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH/cache/pythia_init /usr/bin/time -v nice -n 10 pixi run --manifest-path envs/tt/pixi.toml python -m acts.stage4.run_stage4 smoke --workers 1`
- **C6 markers.** `python3 -I $S/write_marker.py <file> --job <id> [--cpu-s X --max-rss-mb Y]`.
- **C7 benchmarks.** Each unit is `bash $S/bench_chain.sh <unit> <rep> <conc> <args>`; a 4-concurrent round is 4 such commands with `&`, then `wait`.
  - `smoke r 1 400 200`, with `BENCH_NOTE=cold` for rep 0.
  - `m2 r 4 4` (r = 1-3) and `m2 1 1 1`; `m5 r 1 1 1` (r = 1-3).
  - `s4pu r 1 5 4 1 $((1000+r))` (r = 1-3); `s4pu r 4 5 4 1 $((2000+r))` (r = 1-4, concurrent).
  - `s3 r 1 500 <1|3|5|10>` (r = 1-3); `s3 r 4 500 <Λ>` (the 4 Λ concurrent, r = 1-3); `s3 1 4 1000 <Λ>`.
  - `cp r 1 pvpair <2000|20000>` and `gun r 1 <2000|20000> 13` (r = 1-3); `cp r 4 pvpair 20000` (r = 1-4, concurrent).
- **C8 derived records.**
  - Numerics comparison: `$QV2/envs/tt/.pixi/envs/default/bin/python $S/compare_raw.py <scratch run>/tree/analytic/numerics/results/raw/M<2|5> $REPO/stage2_C001_quirks/theory_track/analytic/numerics/results/raw/M<2|5>` → `compare_M{2,5}.json`.
  - Finder timing: `…/python $S/s4_trial_times.py $QV2_SCRATCH/anselm_bench s4pu_n5_roads4_rho1`.
  - Summaries: `python3 -I $S/summarise_bench.py && python3 -I $S/job_sizing.py`.
