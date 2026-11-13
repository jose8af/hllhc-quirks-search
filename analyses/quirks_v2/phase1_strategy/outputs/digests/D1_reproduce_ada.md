# D1. v1 reproduction digest (investigator Ada, 2026-11-13)

Scope: repo-root `README.md`, `TT/README.md`, all of `TT/REPRODUCE.md`, `TT/DATA_LOCATION.md`,
`TT/DATA_README_snapshot.md` (TT = `stage2_C001_quirks/theory_track`; there is no separate `TT/data/README.md` beyond the
tracked copy, which is the same index). I followed pointers into the code to check claims. Tags: **V** = VERIFIED (I
re-derived it or read it from a machine record, with file:line or the command), **E** = ESTIMATE (mine), **U** = UNVERIFIED
(copied from a v1 document and not re-checked). "R" = `TT/REPRODUCE.md`. Nothing was run except greps, small JSON reads
and one PyPI metadata query.

---

## 1. Pipeline, stage by stage

| stage | entry points (from TT) | inputs | outputs (pattern; size, files as recorded) | env | documented command |
|---|---|---|---|---|---|
| cache | `code/T2_kinematics.py` | `data/pdf/CT18NLO/CT18NLO_0000.dat` (download) | `data/cache/T2_kinematics_cache.npz`, 166 MB (U, R:116) | TT | `pixi run python code/T2_kinematics.py`, about 1–2 min, seed 12345 (U, R:116, R:226) |
| 1 numerics (P1) | `analytic/numerics/{M1_events,M2_single,M3_thickness,M4_conformal_thickness,M5_li_blinearity,FU_runs,FIX1_runs,FIX2_runs}.py` + `*_analysis.py`; `analytic/checks/c01…c16` | T2 cache (M1, M3, FU, FIX1, FIX2 read it; M2, M4, M5 do not, V by grep) | `data/stage1_numerics/{M1,M3,FU,FIX1,FIX2}`, 379 MB (M1 323 MB, M3 30 MB) (U, R:114); `results/*.json` and `results/raw/{M2,M5}` are tracked (M2: 520 files, V `ls`) | TT | `pixi run python analytic/numerics/<file>.py` (R:203) |
| 2 MG+Py8 | `sim/scripts/run_all.sh` → `produce.py` (+`--topup`), `reshower.py`, `run_alps.py`, `add_rowmap.py`, `stitch_trg.py`, `val_*.py`, `make_samples_md.py` | UFO `sim/models/quirkE` (`restrict_no_b_mass`), `sim/cards/*.dat`, `data/sim/lhapdf/` (CT18NLO 59 members + NNPDF23_lo_as_0130_qed member 0; patched `.info` tracked), `MG5_DIR` | `sim/mg_out/` (1.5 GB, untracked); `data/sim/{lhe,aux,npz}/`, `SAMPLES_INDEX.json`; 5.4 GB, 2.41 M LHE events, 47 points (U, R:112, R:233) | `sim` env `mg` (py 3.9) for MG, `ana` (py 3.11) for the rest; system `python3` for `produce.py` | `cd TT/sim; pixi run -e ana {probes,produce,vshower,post,validate,docs}` (R:243-250); without the broken probes: `bash scripts/run_all.sh produce` (R:253) |
| 3 string | `sim/stage3/code/{make_surfaces,make_inputs,make_jobs,run_stage3}.py`; then 17 post scripts (R:308-327) | `acts/geometry/cms_phase2_public.json` → `surfaces_s3.json` (tracked); `data/sim/npz/*-TRGS_*` → `data/sim_stage3/inputs/` (7.3 MB, about 1 min) | `data/sim_stage3/out/<camp>/<spin>_m<m>/L<Λ>_<cfg>_c<k>.npz`: Mac 3,986 files + 3 xover, 204,345 events, 1.02 GB; PC `out_pc/` 590 + 3 files, 14,226 events, 70 MB (V, `STAGE3_INDEX.json` "totals"); `canon/` = 4,582 relative symlinks (U, DATA_LOCATION:3); `summary/events_*.npz` | TT (and the `bundle` env for the PC); two post steps in the acts env (R:323-324) | `run_stage3.py run --jobs …mac.json …overlap.json --workers 7 --inputs data/sim_stage3/inputs --out data/sim_stage3/out` (R:287), then `merge_index.py`, `extract.py`, … (R:308-327) |
| 4 ACTS PU 200 | `python -m acts.stage4.run_stage4 {manifest,run,status,check}`, `run_a2fc`; each job runs `acts/stage4/code/run_chain.py` in the acts env via `pixi run --manifest-path acts/pixi.toml` | Stage 3 chunks (through `STAGE3_INDEX.json` → `data/sim_stage3/<file>`, `code/s4sig.py:31`, `analysis/products.py:31-37`); `surfaces_s3.json`; `frozen_inputs.json`; frozen job lists `acts/stage4/jobs/{C1a,C1b,C2B,A2FC}.json` (tracked) | `data/acts_stage4/prod/{C1,C2,A2FC,G3}/`: 2,295 jobs, 36 GB of the 39 GB `acts_stage4/` (U, R:111, R:424, DATA_LOCATION:42) | TT for runner/finder/analysis; acts for simulation | `run_stage4 run --campaign C1a --workers 7 --mem-gb 19` (then C1b, C2B), `run_a2fc run --workers 7 --mem-gb 19` (R:366-371) |
| 4 analysis | `acts.stage4.analysis.run_all`; `acts/stage4/results/{make_stage4_summary,selfcheck_stage4}.py` | `prod/*`, analysis freeze (32 files, sha256 b42aef4d…) | `data/acts_stage4/analysis/C12FC_v1/` (19 files + 40 workspaces, tracked, V `find`), `STAGE4_SUMMARY.json` | TT; `python3 -I` for summary | `run_all --campaigns C1a,C1b,C2B,A2FC --out data/acts_stage4/analysis/C12FC_v1` (R:404) |
| 5 figures | `stage5/make_figures.py` | C12FC_v1 + `STAGE4_SUMMARY.json` (tracked); `data/sim/npz/S-TRGS_m500.npz` (lost); D11 needs one B1 job file in `prod/` (lost) | `stage5/figures/final/` (tracked) | TT (no mplhep) | `make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --truth` (R:434) |
| 6, paper | `opendata/` text only; `paper/` xelatex | — | `paper/quirks_p1p2_note.pdf` v0.4 | TeX Live 2025 | R:475 |

Job granularity (V, my reads of the tracked job lists and index):
- Stage 4: C1a 875 jobs, median `est_s` 72 s, max 768 s. C2B 480 jobs, median 1,057 s, max 1,198 s. A2FC 180 jobs × 200 s.
  None of these exceeds 1,800 s (`acts/stage4/jobs/*.json`). `C1b.json` holds 761 entries, one of which is a blocked
  `g1` placeholder at 54,000 s; the LOG says "760/760" (`TT/LOG.md:271`).
- Peak RSS per job: B1 1.5 GB, B2 4.0 GB, G1 1.0 GB (`acts/stage4/run_stage4.py:65`; G2b measured 3.9 GB at ρ = 2).
- Stage 3 Mac chunks: max 1,207 CPU-s, none over 1,800 s. PC chunks (Λ ≥ 15 keV): 299 of 593 are over 1,800 s, the
  largest 7,845 s (`p2/S_m200/L30_BM_c03`) (V, `STAGE3_INDEX.json`).

## 2. Software inventory

| item | version | how installed / source |
|---|---|---|
| MG5_aMC@NLO | 2.9.22, tarball `MG5_aMC_v2.9.22.tar.gz` (U, R:62) | by hand; the download URL and the HEPTools install method are NOT DOCUMENTED (R:491) |
| Pythia 8 (Stage 2 shower) | 8.313 inside MG HEPTools (U, R:63) | HEPTools |
| MG5aMC_PY8_interface | NOT DOCUMENTED (R:64) | HEPTools |
| Pythia 8 (Stage 4 PU and SM) | **8.312**, conda-forge `pythia8-8.312-py312habccb5d_7` (V, `acts/pixi.lock:106`) | acts env. Stage 2 and Stage 4 therefore use different Pythia builds |
| LHAPDF | conda-forge 6.5.5 in `sim` env `mg` (U, R:35); the HEPTools py3.9 bindings segfault (R:65) | pixi |
| PDF sets | CT18NLO full set, 59 members, lhaid 14400; NNPDF23_lo_as_0130_qed member 0; `.info` patched (AlphaS_* keys), tracked (U, R:68, R:146) | lhapdfsets.web.cern.ch |
| ACTS | `pyacts==48.0.0` PyPI wheel, route **R1** (U, `acts/INSTALL_CHECK.md:38`); the lock pins `pyacts-48.0.0-cp312-cp312-macosx_26_0_arm64.whl` (V, `acts/pixi.lock:122`) | R1 = conda deps + PyPI wheel. **R3** = source build with conda-forge deps (cxx-compiler, cmake, ninja, libboost-devel 1.92, eigen 5.0.1, pybind11 3.1, tbb-devel, nlohmann_json, hepmc3 3.3.1, pythia8 8.312, root 6.3x) and `-DACTS_BUILD_PYTHON_BINDINGS=ON -DACTS_BUILD_FATRAS=ON -DACTS_BUILD_EXAMPLES=ON -DACTS_BUILD_EXAMPLES_PYTHIA8=ON -DACTS_BUILD_PLUGIN_ROOT=ON -DACTS_BUILD_EXAMPLES_ROOT=ON` (+ Geant4/DD4hep optional): 511 MB of deps, or 2.29 GB with Geant4 11.4 + DD4hep, build tree 5–10 GB, 1–3 h on 8 cores. **R3 was never tried** (U, `INSTALL_CHECK.md:41`). Probe manifests for R3 exist in `acts/probe/solve_src{,_min}/` (osx-arm64 only) |
| **pyacts Linux wheel** | **Exists:** `pyacts-48.0.0-cp312-cp312-manylinux_2_34_x86_64.whl`, uploaded 2026-09-30, plus cp311/313/314 (V, PyPI JSON API query today). Needs glibc ≥ 2.34. The head node has glibc 2.39, Ubuntu 24.04.5 (V, `ldd --version`); the workers and the pinned container image were not checked | R:51 and R:509 ("NOT DOCUMENTED") are now answered: R1 works on linux-64 and R3 is not needed for v1 parity |
| Python | TT 3.12.15; acts 3.12.15; sim `mg` 3.9.*, `ana` 3.11.*; system python3 ≥ 3.8 (stdlib) | V: `pixi.lock:94`, `acts/pixi.lock:107`; manifests |
| key packages | TT: numpy 2.5.3, numba 0.68.0, scipy 1.18.1 (V, `pixi.lock:86,87,97`). acts: numpy 2.5.4, hepmc3 3.3.1, pyhepmc 2.16.1, awkward 2.14.0 (V, `acts/pixi.lock:16,58,98,105`); scipy 1.18.1, matplotlib 3.11.2, mplhep 1.3.3, uproot 5.7.7 (U, R:36). sim `ana`: fastjet 3.5.2 from PyPI (U) | pixi |
| Fortran | gfortran 14.2 (U, R:66) | source NOT DOCUMENTED |
| other | FeynRules 2.3.49 + Mathematica 13.3.1 (UFO cross-check only); XeTeX/TeX Live 2025; pixi 0.72 (U, R:69-70, R:26) | — |

**pixi workspaces** (V, `find -name pixi.toml`, platform lines read):

| manifest | platforms | lock | role |
|---|---|---|---|
| `TT/pixi.toml` | osx-arm64 | yes, osx-arm64 only | TT env |
| `TT/sim/pixi.toml` (envs `mg`, `ana`) | osx-arm64 | yes, osx-arm64 only | Stage 2 |
| `TT/acts/pixi.toml` | `{osx-arm64, macos = "26.0"}` | yes (lock v7, subdir osx-arm64, `__osx=26.0`) | Stage 4 |
| `TT/acts/probe/{solve_wheel,solve_src,solve_src_min}/pixi.toml` | osx-arm64 | yes | install probes (R1/R3 dry solves) |
| `TT/data/sim_stage3/bundle/quirks_sim/env/pixi.toml` | **win-64, osx-arm64, linux-64** | yes, **contains a linux-64 solve** (python 3.12.15, numpy 2.5.4, scipy 1.18.1, numba 0.68.0; V, lock l.47-52) | the Stage 3 worker env |

R and the root README speak of "three" workspaces. There are seven manifests, and the tracked Stage 3 bundle env is
already solved for Linux.

## 3. Recorded cost figures

Main machine: Apple M3, 8 cores, 24 GB, macOS 26.6.2 (U, R:24). The Stage 3 index records the hostname as
`Joses-MacBook-Air-4.local`, i.e. a MacBook **Air** (V, `STAGE3_INDEX.json` "environments"). Second machine: AMD 7800X3D,
Windows 11.

| stage / item | figure | hardware, load | tag, source |
|---|---|---|---|
| T2 cache | 1–2 min | M3 | U, R:226 |
| Stage 1 M-runs | M1 1.0×10⁴ s, M3 3.2×10³ s, M5 1.2×10³ s, M2 0.1×10³ s, M4 0.4×10³ s, analyses ≈ 1×10³ s; about 4.5 CPU-h, + about 2 CPU-h lost to hung jobs | M3, 7 processes | U, `analytic/numerics/NUMERICS.md:353-354` |
| Stage 1 FU / FIX1 / FIX2 | 3.8×10³ s (708 jobs) / 8.5×10³ s (1,072 jobs) / 7.2×10³ s = 2.0 CPU-h (735 jobs) | M3 | U, NUMERICS.md:359, 452, 550 |
| Stage 1 M2 | 416 runs in **13 s wall** | M3, 7 processes | V, `results/raw/M2_run.log:53` |
| Stage 1 M5 | cpu 1,153 s | M3 | V, `results/raw/M5_run.log` (last line) |
| Stage 2 total | ≈ 23.5 CPU-h (production ≈ 18 + extras ≈ 5.5: top-ups/V-INTERP 3.2, V-SHOWER 1.2, QED tests 0.5, alps 0.2, probes 0.2); plan budget 35 | M3, MG `nb_core = 6` | U, `sim/VALIDATION.md:624-625` |
| Stage 2 main production wall | 01:55:15 → 05:32:27 = 3.6 h | M3, 6 cores | V, `sim/logs/produce.log:1,545` |
| Stage 2 pilot | P-INC m500, 2,000 LHE: MG+PY8 95 s; P-TRG 107 s; P-LOPS 70 s; rerun P-INC: MG 26 s + PY8 8 s | M3 | V, `produce.log:49,54,59,65` |
| Stage 2 per sample | e.g. E-INC m500 (2 × 50k LHE) ≈ 19 min wall (02:34:05 → 02:53:04) | M3, 6 cores | V, `produce.log` (DRY lines + DONE timestamps) |
| Stage 2 QED re-shower (not done) | ≈ 15 CPU-h | M3 | U, `sim/VALIDATION.md:583` |
| Stage 3 Mac | 207.5 CPU-h (sum of per-event CPU), 204,345 events; p1 38.5 CPU-h / 55,800 events = 2.48 s/event; p2 157.2 / 137,120 = 4.13 s/event; mv 11.8 / 11,425 = 3.73 s/event | M3, 7 workers | V, `STAGE3_INDEX.json` totals/by_campaign + my sum over chunks |
| Stage 3 PC | 375.5 CPU-h, 14,226 events; Λ ≥ 15 keV p2 323.0 CPU-h = 107 s/event; mv-hi 48.0 CPU-h | 7800X3D, 10 workers, SMT | V, same |
| Stage 3, Λ ≥ 15 keV | **371.1 CPU-h** (64 % of 583.1), all PC hours | PC | V (my sum); matches plan l.442 |
| Stage 3 Mac wall | 29.7 h for the Mac share | M3 | U, DATA_README_snapshot.md:46 |
| Stage 3 cross-machine | the 3 overlap jobs (225 events): Mac 0.0579 CPU-h, PC 0.0726 CPU-h → PC/M3 = 1.25 per process | both | V, index totals `xover_*` |
| Stage 3 planning | 498 "M3 CPU-h" estimated (`est_cpu_h_M3` = 208.4 Mac + 290.1 PC) against 583 used | — | V, index |
| ACTS smoke test | 39.3 s wall, 1 thread (39.37 s user) | M3 | V, `acts/scripts/smoke_test_output.txt` (last 2 lines) |
| ACTS per event, ρ = 1 | chain 4.83 s/event (1 process; CKF 2.69, Fatras+digi 0.97); 5.9 s with 4 workers; **10.2 s under the 7-worker production load**; ρ = 2: 9.3 s; finder t₁ 3.26 s (1 process) → 8.02 s loaded at T_seed 4; t₂ 20.1 → 50.6 s | M3 | U, `acts/stage4/G1_REPORT.md:12,75,78`; `run_stage4.py:61-64` (V as constants) |
| ACTS pion gun | Fatras+digi 0.39 s/event (8,000 pions), 4.2 s/event with CKF | M3, 1 thread | U, `INSTALL_CHECK.md:58` |
| C′₀ chain | ≈ 3 ms/event | M3 | U, G1_REPORT.md:16 |
| Stage 4 production | C1a 55.5 + C1b 172.1 + C2B 145.0 + A2FC 9.7 = **382 CPU-h**, defined as the **sum of job walls under load**, 1 core per job | M3, 7 workers, 19 GB budget | U, `STAGE4_RESULTS.md:779` (it tags the figure "[V as sum; E as CPU-h]") |
| Stage 4 "1-process CPU-h" | C1a ≈ 29, C1b ≈ 88, C2B ≈ 80 | M3 | E (v1), `C1_LAUNCH.md` §4 |
| Stage 4 actual walls | C1b 24.7 h; C2B 23.3 h; A2FC 1.41 h | M3, 7 workers | U, `TT/LOG.md:271-272`; `A2FC_REPORT.md:46` (R:381-382 gives only the pre-run ESTIMATEs) |
| Stage 4 analysis | 2,497 s | M3 | U, STAGE4_RESULTS.md:781 |
| Stage 3 post | val_v5 0.23, val_c5kev 0.96, fix_bstar_off 0.84 CPU-h; p1_model_mg ≈ 5 min | M3 | U, R:311-321 |

**Unit warning (for converting the plan's CPU-h).**
- The Stage 4 "CPU-h" are loaded walls. 10.2 s against 4.83 s per PU event is a factor of 2.1 (U inputs) on a fanless
  Air running 7 workers on 8 cores. I believe the M3 has 4 performance and 4 efficiency cores, but that is UNVERIFIED and
  from memory.
- The Stage 3 figure of 583 mixes M3 and PC hours.
- The plan's own warning that laptop CPU-h and vCPU-h differ (plan l.415-416) understates this. A cluster core-hour should
  be calibrated separately against 1-process M3 time and against 7-way-loaded M3 time.

**Calibration candidates.** Both are cheap, need no lost data and have an M3 record.
1. **`acts/scripts/smoke_test.py 400 200`**, ACTS env: 39.3 s, 1 thread on the M3. It covers Pythia8 PU, Fatras,
   digitisation and the D111 geometry, which is exactly the Stage 4 hot path. Its inputs are all tracked. It needs only
   the linux-64 acts env (pyacts manylinux wheel).
2. **`analytic/numerics/M2_single.py`** (TT env, numba): 416 runs, 13 s wall with 7 processes. **`M5_li_blinearity.py`**:
   1,153 CPU-s. Both have their raw outputs tracked (`results/raw/{M2,M5}`), so the same run also gives a numerical
   Linux-vs-Mac comparison.
   - Change the hard-coded `ProcessPoolExecutor(7…)` (`M2_single.py:198`) to 4 on a worker. That means a copy, since the
     file is read-only.
   - Stretch candidate, once Stage 2 inputs exist: a few Stage 3 chunks. Their per-chunk Mac CPU-s and md5 are in
     `STAGE3_INDEX.json` (e.g. `p1/F_m500/L2_B2_c05`: 50 events, 54.6 s, md5 ce7cbfe0…). The seeds are machine-independent
     (R:300), so this would also be a bit-level reproducibility test.

## 4. Linux port work list

**Platform pins** (all V):
- `TT/pixi.toml:4`, `TT/sim/pixi.toml:7`, `TT/acts/probe/*/pixi.toml:4`: `platforms = ["osx-arm64"]`.
- `TT/acts/pixi.toml:8`: `{ platform = "osx-arm64", macos = "26.0" }`.
- `acts/probe/solve_wheel/pixi.toml:20-21`: `[system-requirements] macos = "26.0"`.
- All lockfiles except the bundle env are osx-arm64 only.
- `acts/pixi.lock:122` pins the macOS wheel URL; re-solving for linux-64 picks the manylinux wheel.

**macOS-only commands** (V):
- `caffeinate -i`:
  - in scripts: `acts/stage4/validation/chain_c1.sh:23`, `chain2_c1b.sh:16,21,25`;
  - in documented launch lines: R:287, R:366, R:371 (copied from `sim/stage3/RUNNING.md` and `C1_LAUNCH.md`).
- `DYLD_LIBRARY_PATH`:
  - `sim/scripts/produce.py:260` (**R:54 names only `reshower.py`**), `sim/scripts/reshower.py:77`;
  - `sim/probes/flowtest.py:8`, `flowtest2.py:7`;
  - must become `LD_LIBRARY_PATH` (HEPTools/lib).
- `#!/bin/zsh`: `acts/stage4/validation/{chain_c1,chain2_c1b,g1b_post_g3,prodstop_fri,prodstop_v2}.sh:1`.
- `shasum -a 256`: `g1b_post_g3.sh:10-11` (use `sha256sum`).
- `/Volumes/J8A/quirks_sim/env`: `sim/stage3/code/make_bundle.py:4,24`.
- **No `launchd`/`launchctl`/plist use anywhere** (V, grep). The validation `.sh` helpers are one-off chain and stop
  scripts with PIDs and dates built in, so they need replacing, not porting.

**Scheduling tied to the Mac** (V):
- `--workers` default 7 and `--mem-gb` default 19.0 (`run_stage4.py:766-767`, `run_a2fc.py:63-64`).
- `ProcessPoolExecutor(7…)` or `default=7` hard-coded in 22 `.py` files, including all Stage 1 run scripts,
  `sim/stage3/scripts/{merge_index,extract,p1_model_mg,val_v5,val_c5kev,fix_bstar_off,val_v7_status4}.py` and
  `code/make_jobs.py`.
- A worker has 7.5 GiB and 4 cores. A B2 job peaks at 4.0 GB (`run_stage4.py:65`), so at most one B2 job plus about two
  B1 jobs fit per node (E).
- MG uses `nb_core = 6` (`produce.py`), which is more than the 4 cores of a worker.

**Hard-coded `/Users/jochoafl`** (V, `grep -rlI` with `.pixi`, `mg_out`, `__pycache__`, `.git`, `analyses/` and
`tools/jfc` excluded): **596 files**, 1,595 occurrences.

| directory | files | matters? |
|---|---|---|
| `TT/sim/logs/` | 507 | no (MG/convert logs, `produce.log`) |
| `TT/sim/probes/` | 37 = 18 `.mg` + 19 `.log` | **the 18 `.mg` block `pixi run -e ana produce`** (e.g. `t3_E_incl.mg:4 launch /Users/jochoafl/FISICA_USFQ/hllhc_search/…/sim/mg_out/probe_E_incl`) |
| `TT/sim/review/`, `TT/sim/stage3/review/` | 16 + 17 incl. 17 `.py` check scripts | only to rerun reviewer checks |
| `TT/sim/stage3/probes/_gen/T3_causal_fastmat.py:26,327` | 1 | planning probe |
| `TT/analytic/{checks,numerics,review}` | 4 | outputs/logs |
| `TT/data/acts_stage4/analysis/C12FC_v1/{manifest.json:49,run_all.log}` | 2 | records only; the tracked result names its Mac path |
| `TT/stage5/figures/placeholder/index.json`, `TT/sim/models/fr/make_ufo.log` | 2 | no |
| docs: `TT/LOG.md`, `TT/REPRODUCE.md`, `TT/sim/README.md`, `acts/stage4/{G1B_REPORT,PHASE_A_REPORT}.md`, `research/methodology.md`, `QUIRKS_V2_ORCHESTRATOR_PROMPT.md` | 7 | no |
| `book/checks/ch26..ch29_checks.py` | 4 | **yes for the book checks**: `TT = Path("/Users/jochoafl/FISICA_USFQ/quirks/hllhc-quirks-search/…")` (`ch26_checks.py:16`), a second Mac root |

- The 8 files R says are "being fixed" (`sim/scripts/{produce.py,mg_configure.py,run_all.sh}` and the five validation
  `.sh`) now contain **0** `/Users/` strings (V), so that fix was applied.
- The TT-only, non-data count is 588, matching R:516. R also lists `sim/py.py`, which is absent; it is git-ignored.

**Architecture.** I found no arm64-specific code. `run_stage3.py:135` records `platform.machine()` as provenance only. The
numba caches are keyed to the import path (R:172) and must be rebuilt per node or kept off cajuela (AGENT_RULES: no caches
on cajuela).

**Relative `data/` paths.** At least 103 `.py`/`.sh` files outside `review/` reference `data/…` or `TT/'data'` (V, a
regex-limited lower bound; R says "about 200"). They should be redirected through a single `TT/data` symlink to
`$QV2_DATA/...`, which v2 cannot create inside the read-only TT. **Use copies** (E).

## 5. Lost versus tracked data, and the regeneration order

**Tracked** (V: `du` = 42 MB, 207 files, 0 symlinks):
- `data/README.md`;
- `data/sim/lhapdf/{CT18NLO/CT18NLO.info, NNPDF23…/…info, lhapdf.conf, pdfsets.index}`;
- `data/sim_stage3/STAGE3_INDEX.json` (1.9 MB, with per-chunk md5 and CPU);
- the bundle env `pixi.{toml,lock}`;
- `data/acts_stage4/analysis/C12FC_v1/` (59 files) and `STAGE4_SUMMARY.json`;
- `data/acts_stage4/investigation/` (139 files).

**Lost** (U sizes): `acts_stage4/` 39 GB (prod 36 GB plus gate and probe outputs `g1`, `g2`, `g2b`, `g3`, `p0`–`p6`,
`fix_r*`, `frozen/`, `review_*`); `sim/` 5.4 GB; `sim_stage3/` 1.1 GB (minus the index); `stage1_numerics/` 379 MB;
`tdr_geometry/` 191 MB; `cache/` 166 MB; `pdf/`; `athena_quirks_snapshot/`.

**Lost files that code still reads** (V by grep; consequences E):
- `data/acts_stage4/fix_r1/f1r_summary.json` (`run_g1b.py:77-81`). If it is absent, the probe-row exclusion of WP_RULE
  §5.4 item 10 is **silently skipped** (`if f1r.exists()`). Signal template rows would change without an error.
- `data/acts_stage4/frozen/` (`run_stage4.py:325`): dev and smoke campaigns fall back to planning values (R:511).
- `data/acts_stage4/{fix_r4,frozen,review_wp1,g1/v49}/…`: their sha256 are recorded in `frozen_inputs.json`, and
  `finder/wp_rule_tables.py:16-21` reads them. The production gate checks only the WP_RULE sha256 (`run_stage4.py:570-578`),
  so production is not blocked.
- `data/acts_stage4/g1/pythia_init/*.dat` is re-created on the first run (`code/s4pu.py:108-118`). Its hash is in
  `CODE_FILES` (`run_stage4.py:72`), so it will differ.
- `data/sim/npz/S-TRGS_m500.npz` (needed by `make_stage4_summary.py` and Stage 5) and one B1 job file (Stage 5 D11).

**Regeneration order (dependency chain).**
0. Environments:
   - linux-64 solves of the TT, sim and acts envs (the acts env through the manylinux pyacts wheel);
   - MG5_aMC 2.9.22 + HEPTools (Pythia 8.313, PY8 interface) with gfortran;
   - PDFs into `data/sim/lhapdf/` and `data/pdf/`, using the tracked `.info` files;
   - `tdr_geometry/` is optional (the geometry JSON is tracked).
1. `T2_kinematics` → cache (minutes) → Stage 1 numerics (≈ 10 CPU-h M3, U), independent of everything below.
2. Stage 2 (≈ 23.5 CPU-h M3, U) → `data/sim/npz`.
3. `make_inputs` → Stage 3 production (Λ < 15 keV only, if the plan's "do not rerun ≥ 15 keV" holds: ≈ 212 CPU-h M3 by
   the index, V sum of Mac + PC-lo) → `merge_index` (needs the single-machine layout fix, R:502) → `extract`, post scripts.
4. Stage 4 production (C1a → C1b → C2B, A2FC; 382 loaded M3 CPU-h, U) → analysis → summary → Stage 5.

Re-running Stage 3 changes `STAGE3_INDEX.json` and therefore the analysis freeze. Any non-DEV v2 result needs a re-freeze
or a new pre-registration (R:496-499).

## 6. Known gaps and open work, mapped to plan items

| R item | content (short) | plan item |
|---|---|---|
| §5.1-2 | HEPTools install and MG download not documented | C1 |
| §5.1-3 | probe `.mg` absolute paths break the `produce` task | C1 |
| §5.1-4 | Stage 4 freeze tied to `STAGE3_INDEX.json`; no re-freeze procedure | C1, v2 pre-registration (§5 of the plan) |
| §5.1-5 | `make_bundle.py` USB path | C1 (bundle is moot on the cluster) |
| §5.1-6 | single-machine Stage 3 layout | C1 |
| §5.1-7 | order of the investigation scripts not documented | C1 (needed for `make_stage4_summary`) |
| §5.1-8, -9 | Athena commit hash; report build commands | W1/C3 (documentation) |
| §5.1-10 | pyacts Linux wheel | C1: **resolved, the wheel exists** (§2) |
| §5.1-11 | `data/acts_stage4/frozen/` lost | C1 |
| §5.2 | hard-coded paths | C1 |
| §5.3 | Stage 3 O-1 double-precision floor test not done | P1 (floor tests) |
| §5.3 | V4-3, V4-4 PARTIAL; **V4-5 NOT RUN** | C2 |
| §5.3 | V4-7 FAIL (pre-registered); V4-8 N/A, Mac only | B2 (closure), C1 |
| §5.3 | Stage 2 V1b not delivered | S2 (theory inputs) |
| §6-0 | CMS-internal check | none (policy; outside the plan; flag for human) |
| §6-1 | data-driven PU estimate | B5 (in simulation), B2 |
| §6-2 | ρ = 3 / closure with lever arm | B2 (the plan rejects ρ = 3, plan l.444) |
| §6-3 | C′ conditionals from C′₀, time-tag credit | B1, B3 |
| §6-4 | merging-tolerant rung, seed opening, endcap | S4, S3 |
| §6-5 | C4′ full chain at all Λ ≥ 3 keV | S1 |
| §6-6 | sep_IT and ToF at PU 200 | S5 |
| §6-7 | NLO + FxFx (10–20 CPU-h) | S2 |
| §6-8 | QED FSR re-shower (≈ 15 CPU-h) | S2 |
| §6-9 | O-1 floor test, B₀ law above 5 keV | P1 |
| §6-10 | analytic ΔK, MS theory | P1 (partly; beyond the plan) |
| §6-11 | merged-regime toys, interpolation closure | S1 (coverage); no direct item |
| §6-12 | module-plane geometry, channelised digitisation | B6 |
| §6-13 | CMS Open Data checks | **dropped**: plan l.447 discards Open Data |
| §6-14 | theory follow-ups (Evans–Luty recast, Athena comparison, …) | none (outside the one paper) |
| §6-15 | housekeeping, PROPOSED_CHANGES, author list | C3/W1 |

## 7. Contradictions, doubts, open questions

1. **R §1.1 and §5.1-10 are out of date.** A `manylinux_2_34_x86_64` wheel of pyacts 48.0.0 exists (V, PyPI). Route R3 is
   not needed for parity. Open: glibc on landau/maxwell/schrodinger and in the pinned ubuntu image must be ≥ 2.34. I did
   not check; no node was assigned to me.
2. **CPU-h units are inconsistent.**
   - The Stage 4 382 is loaded wall, and about 197 "1-process" CPU-h by v1's own estimate (29 + 88 + 80 + ~10 for A2FC).
   - The Stage 3 583 is 207.5 M3 + 375.5 PC.
   - The 371 CPU-h at Λ ≥ 15 keV (plan l.442) is entirely PC time.
   - The plan's "168 CPU-h per day at seven workers" therefore counts loaded worker-hours.
   - The strategy needs one defined unit and a measured factor from §3's candidates.
3. **R:381-382 quotes pre-run ESTIMATE walls.** The actual walls are C1b 24.7 h and C2B 23.3 h (`TT/LOG.md:271-272`).
   C1_LAUNCH gives C2B 28.4–32.6 h before the reordering.
4. **R:54 omits `produce.py:260`'s `DYLD_LIBRARY_PATH`.** `produce.py` is the main Stage 2 driver, so the port must change
   it as well as `reshower.py`.
5. **Silent fallback in `run_g1b.py:77`.** A missing `fix_r1/f1r_summary.json` changes which signal rows are flagged, with
   no error. Whether the frozen `jobs/C1a.json` already carries the exclusion was not checked: **open**.
6. **Pythia versions differ.** Stage 2 uses 8.313 (HEPTools) and Stage 4 PU uses 8.312 (conda-forge). On Linux, conda-forge
   may resolve a different pythia8 build unless it is pinned.
7. **"Three workspaces" undercounts.** The tracked bundle env (`data/sim_stage3/bundle/quirks_sim/env`) already has a
   linux-64 lock and is the natural Stage 3 env on the cluster. Its numpy is 2.5.4, against 2.5.3 in the TT env that ran
   the Mac share.
8. **The 30-minute job rule.**
   - Stage 4 production jobs fit (max est 1,198 s at loaded M3 speed).
   - The Stage 3 PC jobs at Λ ≥ 15 keV do not (up to 7,845 s).
   - Several analysis steps do not either: run_all 2,497 s, and Stage 1 M1 runs.
   - MG production runs as one long multi-core process; produce.py chunks (50k LHE) took about 9 min per chunk on 6 cores.
   - All of these need splitting or checkpointing.
9. **DATA_LOCATION l.15 and R:114 disagree** on Stage 1 cost ("not recorded" against ≈ 10 CPU-h). R is right (NUMERICS).
   DATA_LOCATION l.13 says Stage 2 costs "~35 CPU-h", which is the budget; 23.5 was used.
10. **Plan C1 says "bring the 46 GB back from the external drive".** Per the brief it is lost, so C1 becomes a full
    regeneration (§5 chain). C1's criterion "v1 ladder reproduced within statistics" then costs about 23.5 + ~212 (or 583)
    + ~197–382 M3 CPU-h before any v2 work (E, from the U figures).
11. **Questions for the strategy.**
    - Rerun Stage 3 at Λ ≥ 15 keV at all?
    - Accept a new `STAGE3_INDEX.json` and re-freeze, versus reproducing under DEV stamps?
    - Where may the `TT/data` symlink live, given that TT is read-only (copy TT into `analyses/quirks_v2`)?
    - Which MG/HEPTools source and gfortran (conda-forge `gfortran` in a pixi env?) to standardise on?
