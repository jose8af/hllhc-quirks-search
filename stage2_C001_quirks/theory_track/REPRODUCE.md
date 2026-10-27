# Reproducing the C001 quirk theory track (handoff guide)

For a group starting from zero: a fresh machine, no access to the original 46 GB `data/` directory and no access to the
author's Mac. Every command and number below is copied from the file cited next to it. "NOT DOCUMENTED" means the project
files do not say. All paths are relative to `stage2_C001_quirks/theory_track/` (called **TT** below) unless they start
with `stage2_C001_quirks/` or are marked repo-root.

**Short version.**
- Most results are already in the repository as JSON, Markdown reports and figures (see "already in the repo" in §3), so you
  can read and check them without running anything.
- A full rerun chains four expensive steps: Stage 2 MadGraph (≈ 24 CPU-h), Stage 3 string propagation (≈ 583 CPU-h),
  Stage 4 ACTS at PU 200 (≈ 382 CPU-h), then the analysis. Each step reads the previous step's output from `data/`.
- The final deliverable is `paper/quirks_p1p2_note.pdf` (v0.4).
- Read `README.md` (TT) for status, then this file.

---

## 1. Prerequisites

### 1.1 Platform

| item | what the project used | source |
|---|---|---|
| main machine | Apple M3 MacBook, 8 cores, 24 GB RAM, macOS 26.6.2 (Darwin 25.6), arm64 | `acts/INSTALL_CHECK.md` l.4, §8 |
| second machine (Stage 3 only) | Windows 11 PC, AMD 7800X3D (8 cores / 16 threads) | `sim/stage3/RUNNING.md`, `sim/stage3/bundle_src/SETUP_WINDOWS.md` |
| package manager | pixi (0.72 named in `acts/INSTALL_CHECK.md` §8) | — |
| shells | bash (`sim/scripts/run_all.sh`), zsh (`acts/stage4/validation/chain_c1.sh` is `#!/bin/zsh`) | scripts |
| macOS-only commands used in launch lines | `caffeinate -i` (keeps the Mac awake) and `DYLD_LIBRARY_PATH` (`sim/scripts/reshower.py`) | `sim/stage3/RUNNING.md`, `acts/stage4/C1_LAUNCH.md`, `chain_c1.sh` |

**Three separate pixi workspaces, each with an `osx-arm64`-only lockfile:**

| workspace | manifest | contents (as declared) | used by |
|---|---|---|---|
| theory-track ("TT env") | `pixi.toml` | python 3.12, numpy, scipy, sympy, matplotlib, mpmath, numba. Recorded versions: Python 3.12.15, numpy 2.5.3, numba 0.68.0 (`sim/stage3/bundle_src/SETUP_WINDOWS.md`). **No mplhep** (`stage5/plotting.py` header) | `code/`, Stage 1, Stage 3, Stage 4 finder and analysis, Stage 5 |
| Stage 2 | `sim/pixi.toml` | env `mg`: python 3.9, six, numpy 1.26, lhapdf (conda-forge LHAPDF 6.5.5 per `sim/README.md`). Env `ana`: python 3.11, numpy, scipy, matplotlib, mplhep, pyhepmc, numba, PyPI fastjet (3.5.2 per `sim/E4_session_log.md`) | MadGraph runs (`mg`), conversion and validation (`ana`) |
| Stage 4 ACTS | `acts/pixi.toml` | python 3.12, numpy, scipy, matplotlib, mplhep, awkward, uproot, pythia8, pyhepmc; PyPI `pyacts==48.0.0`. Installed versions: pyacts 48.0.0, pythia8 8.312, hepmc3 3.3.1 / pyhepmc 2.16.1, numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, mplhep 1.3.3, uproot 5.7.7, awkward 2.14.0 (`acts/INSTALL_CHECK.md` §8). About 640 MB on disk | ACTS chain (Fatras, digitisation, CKF) |

Install each one with `pixi install` in its directory (`acts/INSTALL_CHECK.md` §8 used `nice -n 19 pixi install`). For
the Stage 2 workspace the named environments (`-e mg`, `-e ana`) are installed by `pixi run -e <env> ...` the first time
they are used.

**ACTS env needs macOS ≥ 26.** `acts/pixi.toml` declares `platforms = [{ platform = "osx-arm64", macos = "26.0" }]`
because the only pyacts 48.0.0 wheel recorded is tagged `macosx_26_0_arm64` (`acts/INSTALL_CHECK.md` §1, §8). On
macOS 15 the project notes that you must pin pyacts ≤ 46.8.1 (`macosx_15_0` wheels), but the Python API changed between
v46 and v48 (`acts/INSTALL_CHECK.md` §2, R1 row). The Stage 4 code was only run with 48.0.0.

**What a Linux user must change** (none of this was tested in the project):
1. In `pixi.toml` and `sim/pixi.toml`, add `"linux-64"` to `platforms`, then re-solve, which rewrites `pixi.lock`. Package
   versions will then differ from those recorded above.
2. In `acts/pixi.toml`, replace the `osx-arm64`/`macos = "26.0"` platform entry with `linux-64`. Whether a Linux wheel of
   `pyacts==48.0.0` exists is **NOT DOCUMENTED** (the project recorded only the macOS tag). Check PyPI. If there is none, the
   fallback documented in `acts/INSTALL_CHECK.md` §2 is a source build (route R3: `-DACTS_BUILD_PYTHON_BINDINGS=ON
   -DACTS_BUILD_FATRAS=ON -DACTS_BUILD_EXAMPLES=ON ...`, estimated 1–3 h on 8 cores).
3. Drop `caffeinate -i` from the launch commands. In `sim/scripts/reshower.py`, `DYLD_LIBRARY_PATH` becomes `LD_LIBRARY_PATH`.
4. Windows: `pyacts` has no win-64 wheel, so Stage 4 simulation needs WSL2 (`LOG.md` 2026-10-13 E9). The TT env has a
   verified win-64 solve (Stage 3 bundle), and the finder never imports ACTS (`acts/stage4/plan.md` §1.8).

### 1.2 External tools that pixi does NOT install

| tool | exact version used | needed for | where to get it / notes |
|---|---|---|---|
| **MadGraph5_aMC@NLO** | **v2.9.22** (release tarball `MG5_aMC_v2.9.22.tar.gz`, `sim/VALIDATION.md` §8) | Stage 2 | Upstream MG5_aMC distribution. Download URL NOT DOCUMENTED in the project. Never modify the install: models are imported by absolute path and every output directory gets its own `Cards/me5_configuration.txt` (`sim/scripts/mg_configure.py`) |
| MG HEPTools: **Pythia8** | **8.313** (`sim/plan.md` l.58, `sim/VALIDATION.md` title) | Stage 2 shower | Inside `$MG5_DIR/HEPTools/pythia8`. How HEPTools was installed is NOT DOCUMENTED |
| MG HEPTools: **MG5aMC_PY8_interface** | version NOT DOCUMENTED | Stage 2 (`produce.py` runs the interface jobs itself) | `$MG5_DIR/HEPTools/MG5aMC_PY8_interface` |
| MG HEPTools: **LHAPDF6** | present but **not used for Python**: the HEPTools py3.9 bindings segfault (they link a missing `libpython3.9.dylib`). The conda-forge LHAPDF 6.5.5 of `sim` env `mg` is used instead, via `mg_configure.py` | — | `sim/plan.md` l.55-56, `sim/scripts/mg_configure.py` header |
| Fortran compiler | gfortran 14.2 (`sim/E4_session_log.md` l.3) | MG matrix-element compilation | source NOT DOCUMENTED |
| system `python3` | any ≥ 3.8, stdlib only (`mg_configure.py` header; `produce.py` "system python3"); E4 had 3.14 | `sim/scripts/produce.py`, `mg_configure.py`; the `python3 -I` stdlib scripts of Stage 4/5 | — |
| **PDF sets** | **CT18NLO** full set (59 members, `lhaid = 14400`) and **NNPDF23_lo_as_0130_qed** member 0 | Stage 2 (`data/sim/lhapdf/`); CT18NLO member 0 also for `code/T2_kinematics.py` (`data/pdf/CT18NLO/`) | https://lhapdfsets.web.cern.ch/current/CT18NLO.tar.gz (`code/T2_kinematics.py` header; `sim/plan.md` D7). NNPDF23_lo_as_0130_qed from the same site, because the HEPTools tarballs are 0-byte files (`sim/plan.md` l.356). **The CT18NLO `.info` must be patched**; see §2.3 |
| FeynRules + Mathematica | FeynRules **2.3.49** (`sim/models/fr/make_ufo.log`), Mathematica **13.3.1** with `wolframscript` (`sim/plan.md` l.19) | **only** the cross-check UFO `sim/models/fr/quirkE_FR_UFO` (already in the repo) | Set `FEYNRULES_PATH`; run `wolframscript -file make_ufo.wls` from `sim/models/fr/` (`make_ufo.wls` header). Not needed for production |
| **xelatex + bibtex** | XeTeX 3.141592653-2.6-0.999997, TeX Live 2025 (first line of the paper's build log) | paper and companion | any TeX Live with fontspec, natbib, hyperref, longtable, xurl, etc. (`paper/preamble.tex`) |
| ImageMagick `magick` | NOT DOCUMENTED | one paper figure crop only (`paper/FIGURE_MANIFEST.md`: `magick -crop 540x493+1100+0`) | optional |
| `pdftotext` | NOT DOCUMENTED | made the `.txt` copies of the TDR PDFs in `data/tdr_geometry/` (`DATA_README_snapshot.md`) | optional; no script reads them |

### 1.3 MadGraph location: `MG5_DIR`

The original scripts hard-coded `/Users/jochoafl/8A/MadGraph/MG5_aMC_v2_9_22`. They now read an environment variable
instead (`produce.py`, `mg_configure.py` and `run_all.sh` exit with "set MG5_DIR …" if it is unset):

    export MG5_DIR=/path/to/MG5_aMC_v2_9_22      # must contain bin/mg5_aMC and HEPTools/{pythia8,MG5aMC_PY8_interface}

Scripts that read it: `sim/scripts/produce.py`, `sim/scripts/mg_configure.py` and `sim/scripts/run_all.sh`. It also reaches
`sim/scripts/reshower.py` and `run_alps.py` through `from produce import MG`. **Not covered:** the 18 MadGraph probe
scripts `sim/probes/*.mg` still contain absolute paths (§5).

Other environment variables used by the code:

| variable | effect | source |
|---|---|---|
| `LHAPDF_DATA_PATH` | set to `data/sim/lhapdf` by `run_all.sh` and `produce.py:env()` | scripts |
| `PYTHONDONTWRITEBYTECODE=1` | keeps MG from writing `.pyc` into its install | `sim/README.md` |
| `T2_PDF`, `T2_CACHE` | override `data/pdf/CT18NLO/CT18NLO_0000.dat` and `data/cache/T2_kinematics_cache.npz` | `code/T2_kinematics.py`, `code/T3_propagator.py` |
| `FEYNRULES_PATH` | FeynRules install for `make_ufo.wls` | `sim/models/fr/make_ufo.wls` |

---

## 2. The data directory `data/` (mostly NOT in the repository)

`data/` is excluded by the repo-root `.gitignore`, **except for a few small files (≈ 43 MB) that are tracked**:
`data/README.md`; `data/sim_stage3/STAGE3_INDEX.json` (frozen Stage 4 input); the Windows bundle env
`data/sim_stage3/bundle/quirks_sim/env/pixi.{toml,lock}`; the patched PDF `.info` files plus `lhapdf.conf` and
`pdfsets.index` in `data/sim/lhapdf/`; the final Stage 4 analysis output `data/acts_stage4/analysis/C12FC_v1/` and
`STAGE4_SUMMARY.json`; and the investigation outputs `data/acts_stage4/investigation/*.{json,txt}`. On 2026-10-18 it held 46 GB: 20,385 files plus 4,582 relative
symlinks, all of them in `sim_stage3/canon/` (`DATA_LOCATION.md`). About 200 scripts read `data/…` by **relative path**, so
recreate it at `TT/data/` or make it a symlink there (`DATA_LOCATION.md` "Restoring"). If you ever copy it, use a
filesystem that keeps symlinks (not exFAT/FAT32).

### 2.1 What lived there and how to regenerate it

| subdir | size | content | regenerate with | cost (as documented) |
|---|---|---|---|---|
| `acts_stage4/` | 39 GB | Stage 4 ACTS production at PU 200 (`prod/{C1,C2,A2FC,G3}/`, 2,295 production jobs), the frozen analysis run `analysis/C12FC_v1/` plus `analysis/STAGE4_SUMMARY.json`, `investigation/*.json`, gate and probe outputs (`g1`, `g2`, `g3`, `p0`–`p6`, `fix_r*`, …), the freeze candidate `frozen/` | rerun Stage 4 (§3.5) | 382 CPU-h production (`acts/stage4/STAGE4_RESULTS.md` §11.1); "~1 day" (`DATA_LOCATION.md`); C1b and C2B were ≈ 24–27 h wall each on 7 workers (`acts/stage4/C1_LAUNCH.md` §4) |
| `sim/` | 5.4 GB | Stage 2 samples: `lhapdf/` (local PDF dir), `npz/<ID>_m<m>.npz` (+ `chunks/`), `lhe/<ID>/`, `aux/<ID>/`, `SAMPLES_INDEX.json`; 2.41 M LHE events | Stage 2 driver (§3.3) | `DATA_LOCATION.md`: "~35 CPU-h" (the plan budget). Actually used: production ≈ 18 CPU-h plus ≈ 5.5 CPU-h of extras, **≈ 23.5 CPU-h** (`sim/VALIDATION.md` §8, l.624-625) |
| `sim_stage3/` | 1.1 GB | Stage 3 truth propagation: `inputs/`, `out/` (Mac), `out_pc/` (PC), `STAGE3_INDEX.json`, `canon/` (symlinks), `summary/`, `validation/`, `fix_r1/`, `probes/`, `bundle/` | Stage 3 (§3.4) | 207.5 CPU-h Mac + 375.5 CPU-h PC ≈ **583 CPU-h** (`sim/stage3/README.md` headline 1) |
| `stage1_numerics/` | 379 MB | Stage 1 blind numerics raw files: `M1/` (323 MB), `M3/` (30 MB), `FU/`, `FIX1/`, `FIX2/` | Stage 1 numerics scripts (§3.2) | `DATA_LOCATION.md` says "not recorded", but `analytic/numerics/NUMERICS.md` gives: M-runs ≈ 4.5 CPU-h (§10), FU 3.8×10³ s (§11), FIX1 8.5×10³ s, FIX2 2.0 CPU-h. Total **≈ 10 CPU-h**, plus ≈ 2 CPU-h lost to hung jobs |
| `tdr_geometry/` | 191 MB | public CMS Phase-2 TDR, tkLayout D111 pages, beam-spot TDRs | re-download (§2.2) | — |
| `cache/` | 166 MB | `T2_kinematics_cache.npz` (LO DY+ISR kinematics; read by `code/T3_*`, Stage 1 numerics, Stage 3 V5) | `pixi run python code/T2_kinematics.py` from TT (header: "about 1-2 minutes"; RNG seed 12345). Needs `data/pdf/CT18NLO/` | minutes |
| `pdf/` | <1 MB | `CT18NLO/` member 0 | re-download (§1.2) | — |
| `athena_quirks_snapshot/` | <1 MB | ATLAS Athena `Simulation/G4Extensions/Quirks`, branch `main`, downloaded 2026-10-07 (`investigations/T2_string_dynamics.md` l.425). Reference copy only; check the licences before redistributing (`DATA_README_snapshot.md`) | re-download from gitlab.cern.ch/atlas/athena. **The commit hash is NOT DOCUMENTED.** No script reads it | — |
| `README.md` | — | index; a copy is in `DATA_README_snapshot.md` | — | — |

### 2.2 Re-download sources for `tdr_geometry/` (from `DATA_README_snapshot.md`)

| file / folder | source |
|---|---|
| `CMS-TDR-014_Phase2_Tracker_TDR.pdf` | CMS, "The Phase-2 Upgrade of the CMS Tracker", CERN-LHCC-2017-009, INSPIRE 1614103: https://inspirehep.net/files/338a99fa62dec25fcbc18d806bd7fb71 |
| `tkLayout_OT806_IT742_D111/` (`layout.html`, `layoutpixel.html`, `index.html`, `info.html`, `DetId_modules_list.csv`, `DetId_sensors_list.csv`, `summary.root`) | https://cms-tklayout.web.cern.ch/cmssw/OT806_IT742/ (fetched 2026-10-11; page generated 2024-04-08, tkLayout revision current_xml-3600-89b31835). The page may have changed since |
| `tkLayout_indexes/` | index pages of https://cms-tklayout.web.cern.ch/{cmssw,main,recent,reference}/ and https://tklayout.web.cern.ch/ |
| `beamspot_sources/CMS-TDR-020_MTD_TDR.pdf` | CMS MTD TDR, CERN-LHCC-2019-003, INSPIRE 1819664 |
| `beamspot_sources/CERN-2020-010_HL-LHC_TDR.pdf` | HL-LHC TDR, INSPIRE 1840718 |
| `broken_downloads_2026-10-08/` | failed downloads kept for the record; not needed |

Only `acts/geometry/build_cms_phase2_public.py` reads this folder (default input
`data/tdr_geometry/tkLayout_OT806_IT742_D111/DetId_modules_list.csv`). Its output `acts/geometry/cms_phase2_public.json`
**is in the repo**, so you need the download only to rebuild the geometry. Numbers from the TDR and from arXiv:2407.13721 are
hard-coded in the script with page references.

### 2.3 Rebuilding `data/sim/lhapdf/`

`sim/E4_session_log.md` l.7 and l.15 and `sim/plan.md` l.57 and l.356 describe this directory:
- the full CT18NLO set (59 members) from lhapdfsets.web.cern.ch;
- NNPDF23_lo_as_0130_qed member 0 from the same site;
- the CT18NLO `.info` patched to add `AlphaS_FlavorScheme`, `AlphaS_NumFlavors`, `AlphaS_Lambda4` and `AlphaS_Lambda5`, which
  LHAPDF 6.5.5 and the MG Fortran glue need.

The patched files are **in the repo** (`data/sim/lhapdf/CT18NLO/CT18NLO.info`: `AlphaS_FlavorScheme: variable`,
`AlphaS_NumFlavors: 5`, `AlphaS_Lambda4: 0.3260`, `AlphaS_Lambda5: 0.2260`). Download the CT18NLO and
NNPDF23_lo_as_0130_qed member `.dat` files next to them and keep these `.info` files. The project notes that changing the
Λ placeholders left σ unchanged (2.454 fb both times; `sim/plan.md` l.57).

### 2.4 Inputs that exist only in `data/` and are not plain regenerations

- **`data/sim_stage3/STAGE3_INDEX.json` is part of the Stage 4 analysis freeze.** `acts/stage4/analysis/inputs/analysis_freeze.json`
  lists its sha256. The index records per-chunk CPU times and machine names (`sim/stage3/scripts/merge_index.py` header),
  so a re-generated index will almost certainly have a different hash. `run_all` would then refuse a non-DEV result until
  you re-freeze (§3.5). The original index **is in the repo**, so the freeze check passes as long as Stage 3 is not rerun.
- **Windows bundle environment** (`data/sim_stage3/bundle/quirks_sim/env/pixi.toml` + `pixi.lock`; Python 3.12, numpy 2.5,
  scipy, numba 0.68 per `sim/stage3/bundle_src/RUN.md`) **is in the repo**. `sim/stage3/code/make_bundle.py` copies it from
  the USB path `/Volumes/J8A/quirks_sim/env`; point that path at `data/sim_stage3/bundle/quirks_sim/env/` instead.
- **Stage 4 machine-readable results** (`data/acts_stage4/analysis/C12FC_v1/`, `STAGE4_SUMMARY.json`,
  `data/acts_stage4/investigation/*.json`) **are in the repo**, so the summary tables and most detector figures can be
  rebuilt without rerunning Stage 4.
- **Probe and gate outputs** (`data/acts_stage4/{p0..p6,g1,g2,g2b,g3,…}`) were used to *set* frozen numbers, e.g. `mip_gev`
  from `data/acts_stage4/g1/v49/v49.json`. These numbers are transcribed into `acts/stage4/frozen_inputs.json` (in the repo),
  so production does not need the outputs.

---

## 3. Stage-by-stage pipeline

General rules (from `README.md`, `analytic/README.md`, `acts/stage4/run_stage4.py`):
- Run from **TT** with `pixi run python <path>` (TT env) unless a different workspace is named.
- Stage 4 modules must be imported as `acts.stage4.…` from TT, because the numba cache is keyed to that import path
  (`acts/stage4/finder/README.md`).
- Decisions are logged in `LOG.md` (long; grep it).

Stage order and data flow:

```
code/T2_kinematics.py ─► data/cache ─► Stage 1 numerics (analytic/)              [P1 theory]
Stage 2 sim/ (MG+Pythia) ─► data/sim ─► Stage 3 sim/stage3/ ─► data/sim_stage3 ─► Stage 4 acts/stage4/ ─► data/acts_stage4
                                                         └────────────► Stage 5 truth figures      Stage 5 detector figures ◄┘
Stage 6 opendata/ (text only) ; paper/ (copies of figures + text)
```

### 3.0 Pre-stage: discovery phase and theory investigations (no rerun needed)

| what | where | notes |
|---|---|---|
| Discovery phase (candidate search) | repo-root `research/`, `TOP_CANDIDATES.md`, `REJECTED_CANDIDATES.md`, `RESEARCH_PLAN.md`, `report/hllhc_report.pdf` | `research/cache/` (download cache) is not in the repo; the tools in `research/tools/` refill it |
| C001 Phase 1/2 (strategy, sample requirements) | `stage2_C001_quirks/{literature,research,phase1_strategy,phase2_exploration}`, `stage2_C001_quirks/report/quirks_phase1_report.pdf` | — |
| Theory investigations T1–T6 and synthesis | `investigations/`, `code/` (`pixi run python code/<file>.py`), `outputs/THEORY_GAPS_SYNTHESIS.md` (v5), `report/quirks_theory_report.pdf` | the T2/T3/T4 scripts need `data/cache/` and `data/pdf/` |

The LaTeX build commands of the three `report/*.tex` files are NOT DOCUMENTED. The PDFs are in the repo.

### 3.1 Stage 1: analytic near-miss impulse coefficient c (P1 theory)

- **Purpose.** Derive c in Δs_B ∝ ε_B[ln(1/ε_B) + C] and validate it with blind numerics.
- **Read.** `analytic/NEAR_MISS_IMPULSE.md` §0 (v5.1), `analytic/numerics/NUMERICS.md` §0, `analytic/NOVELTY_AUDIT.md` §0
  (`README.md`).
- **Analytic checks.** `analytic/checks/c01…c16_*.py`, run one at a time and save stdout next to the script. Example from
  the `c07` header: `pixi run python analytic/checks/c07_predictions.py [nev] > analytic/checks/c07_predictions_out.txt`.
  These read `code/` and, for event samples, `data/cache/`.
- **Numerics.** All runs: `pixi run python analytic/numerics/<file>.py` from TT (`analytic/numerics/plan.md` l.5). Run
  scripts write raw files to `data/stage1_numerics/`; analysis scripts write `analytic/numerics/results/*.json`.

| step | run | analyse | raw output | CPU (`NUMERICS.md`) |
|---|---|---|---|---|
| M1 | `M1_events.py [prod\|fine\|conf\|all] [NEV]` | `M1_analysis.py` | `data/stage1_numerics/M1` | 1.0×10⁴ s |
| M2 | `M2_single.py` | `M2_analysis.py` | `results/raw/M2` (in repo) | 0.1×10³ s |
| M3 | `M3_thickness.py` | `M3_analysis.py` | `data/stage1_numerics/M3` | 3.2×10³ s |
| M4 | `M4_conformal_thickness.py` | `M4_summary.py` | — | 0.4×10³ s |
| M5 | `M5_li_blinearity.py` | — | `results/raw/M5` (in repo) | 1.2×10³ s |
| M1↔M3 | `M13_bridge.py` | — | — | — |
| FU (follow-up) | `FU_runs.py` | `FU_analysis.py` | `data/stage1_numerics/FU` | 3.8×10³ s |
| FIX1 | `FIX1_runs.py` | `FIX1_analysis.py` | `data/stage1_numerics/FIX1` | 8.5×10³ s |
| FIX2 | `FIX2_runs.py` | `FIX2_analysis.py` | `data/stage1_numerics/FIX2` | 2.0 CPU-h |

- **Inputs → outputs.** `data/cache/T2_kinematics_cache.npz` → `data/stage1_numerics/*` → `analytic/numerics/results/*.json`;
  checks → `analytic/checks/*_out.txt`, `analytic/predictions.json`.
- **Already in the repo.** `analytic/predictions.json`, every `analytic/checks/*_out.txt`,
  `analytic/numerics/results/*.json` (+ `raw/M2`, `raw/M5`, run logs), all notes and reviews (`analytic/review/`).
- Proposed edits to other files (not applied): `analytic/PROPOSED_CHANGES.md`.

### 3.2 (cache) T2 kinematics

    pixi run python code/T2_kinematics.py          # from TT; ~1-2 min; writes data/cache/T2_kinematics_cache.npz and figures/T2_*.png

Needs `data/pdf/CT18NLO/CT18NLO_0000.dat` (or `T2_PDF`). It reads the lhagrid1 file directly; no LHAPDF library is needed
(`code/T2_kinematics.py` header).

### 3.3 Stage 2: MadGraph5_aMC 2.9.22 + Pythia 8.313 samples (`sim/`)

- **Purpose.** LO-MLM 0–2j quirk-pair samples (E and Ẽ, 47 points, ≈ 2.41 M LHE events) with CP5. They replace the T2 toy.
- **Read.** `sim/VALIDATION.md` §0 then `sim/SAMPLES.md`; plan `sim/plan.md`; reproduction `sim/VALIDATION.md` §9;
  deferred items `sim/DEFERRED.md`.
- **Model and cards (in repo).** Hand-written UFO `sim/models/quirkE/` (imported as `…/sim/models/quirkE-no_b_mass`, i.e.
  with `restrict_no_b_mass.dat`), FeynRules cross-check `sim/models/fr/`, effective cards `sim/cards/*.dat`.
- **Prerequisites.** `MG5_DIR` (§1.3), `data/sim/lhapdf/` (§2.3), sim env `mg` installed (`mg_configure.py` points MG at
  `sim/.pixi/envs/mg/bin/lhapdf-config`).
- **Commands** (`sim/VALIDATION.md` §9; each pixi task runs `bash scripts/run_all.sh <stage>`):

```
cd TT/sim
pixi run -e ana probes      # MG LO probes t3/t4/t12/t15/t16 (VALIDATION §1)
pixi run -e ana produce     # produce.py (resumable; ~18 CPU-h) + produce.py --topup
pixi run -e ana vshower     # V-SHOWER re-showers (~1.2 CPU-h)
pixi run -e ana post        # add_rowmap.py, stitch_trg.py, run_alps.py
pixi run -e ana validate    # val_xsec -> annotate_npz -> val_spectra/mlm/tune/shower/lmax/interp/qed, reshower test, val_loader
pixi run -e ana docs        # make_samples_md.py, val_trgs_stats.py, val_summary.py, val_headlines.py
```

  **Caveat (§5).** In `sim/pixi.toml` the `produce` task `depends-on = ["probes"]`, and the probe scripts `sim/probes/*.mg`
  contain absolute paths. To produce without the probes, call the driver directly: `bash scripts/run_all.sh produce`, or
  `python3 scripts/produce.py` and then `python3 scripts/produce.py --topup` from `sim/` (`produce.py` header). Pilot only:
  `python3 scripts/produce.py --only P-INC,P-TRG,P-LOPS`. Dry run: `--dry`.
- **Inputs → outputs.** cards + UFO + PDFs → `sim/mg_out/` (MG output directories, not in the repo, 1.5 GB per `.gitignore`)
  → `data/sim/{lhe,aux,npz}/`, `data/sim/SAMPLES_INDEX.json` → `sim/results/*.json`, `sim/figures/*.png`, `sim/SAMPLES.md`,
  `sim/VALIDATION.md` §0.
- **Determinism.** Seeds are fixed per chunk (`seed = base(ID) + 100*mass_index + chunk`, `produce.py`). One Pythia job was
  re-showered bit-for-bit (`sim/results/reshower_repro.json`). LO σ reruns agree to ≤ 3×10⁻⁴ (`sim/results/probe_rerun.json`).
- **CPU.** ≈ 23.5 CPU-h actually used, out of a 35 CPU-h budget (`sim/VALIDATION.md` §8). MG uses `nb_core = 6`
  (`produce.py`).
- **Already in the repo.** `sim/results/*.json` (`xsec.json` holds σ_norm and the tail fractions used by Stage 4/5),
  `sim/results/{headlines,summary_tables}.md`, `sim/figures/`, `sim/cards/`, `sim/logs/` (MG/convert logs), `SAMPLES.md`,
  `VALIDATION.md`.
- **Loader for downstream use:** `sim/scripts/mg_events.py`. Use `sigma_norm_fb` for yields, not `sigma_lo_mlm_fb`
  (`sim/README.md`).

### 3.4 Stage 3: truth-level string propagation (`sim/stage3/`)

- **Purpose.** Propagate the Stage 2 events with the causal Nambu–Goto kernel `T3_causal_s3.py` (s3.2) through the
  Phase-2-like surfaces. 218,571 events; P1 and P2 truth-level deliverables.
- **Read.** `sim/stage3/README.md`, then `VALIDATION.md` §0; plan `plan.md`; job split `RUNNING.md`; Stage 4 handover
  `HANDOVER_STAGE4.md`; decisions `DECISIONS_PENDING.md` (U-1…U-5, all approved as recommended on 2026-10-13, `LOG.md`).
- **Preparation** (from TT; each script header gives the "Run" line):

```
pixi run python sim/stage3/code/make_surfaces.py   # acts/geometry/cms_phase2_public.json -> sim/stage3/code/surfaces_s3.json (in repo)
pixi run python sim/stage3/code/make_inputs.py     # data/sim/npz/*-TRGS_* -> data/sim_stage3/inputs/ (~1 min; seed 12345)
pixi run python sim/stage3/code/make_jobs.py       # -> sim/stage3/jobs/{all,mac,pc,overlap}.json (in repo) + split_summary.json
```

- **Production** (`sim/stage3/RUNNING.md`; runner `sim/stage3/code/run_stage3.py`, commands `run | status | smoke | check`):

```
# Mac share (3,986 jobs + 3 overlap clones), 7 workers:
nohup nice -n 10 caffeinate -i pixi run python sim/stage3/code/run_stage3.py run --jobs sim/stage3/jobs/mac.json sim/stage3/jobs/overlap.json --workers 7 --inputs data/sim_stage3/inputs --out data/sim_stage3/out > data/sim_stage3/out/run_mac_stdout.txt 2>&1 &
pixi run python sim/stage3/code/run_stage3.py status --jobs sim/stage3/jobs/mac.json sim/stage3/jobs/overlap.json --out data/sim_stage3/out
touch data/sim_stage3/out/STOP          # graceful stop; rerun the same command to resume (finished jobs are skipped)
```

- **Mac + Windows split.**
  - `jobs/all.json` = `mac.json` + `pc.json`. `pc.json` has 590 jobs: every P2 job at Λ ≥ 15 keV plus 137 MV jobs.
  - `overlap.json` has 3 jobs run on **both** machines, for the cross-machine check.
  - The split rule was PC share = R/(1+R) with R = 1.4 (`RUNNING.md`, `jobs/split_summary.json`).
  - The PC ran a self-contained bundle: `pixi run python sim/stage3/code/make_bundle.py stage` builds
    `data/sim_stage3/bundle/quirks_sim/`, and `… make_bundle.py usb <path>` copies it to a USB stick. Windows instructions:
    `sim/stage3/bundle_src/{SETUP_WINDOWS,RUN,PROMPT_FOR_CLAUDE}.md`, with 10 workers and `--low-priority`.
  - PC results came back as `out_pc/` and were copied to `data/sim_stage3/out_pc/`, kept separate from `out/`.
  - Kernel seeds are `blake2b("spin|m|row|lam|cfg")`, independent of machine and chunking (`run_stage3.py`). Mac and PC
    outputs are bit-identical in 224/225 overlap events (`results/xover.json`), so **one machine is enough**.
  - `merge_index.py` expects each job in the tree of the machine it was assigned to. For a single-machine rerun, run the
    `pc.json` jobs with `--out data/sim_stage3/out_pc` (or adapt `merge_index.py`). This is not described in the project
    docs; it follows from the `merge_index.py` header.
- **Merge and post-production**, in this order, from TT (`sim/stage3/VALIDATION.md` §10):

```
pixi run python sim/stage3/scripts/merge_index.py      # STAGE3_INDEX.json, canon/ symlinks, results/merge.json
pixi run python sim/stage3/scripts/extract.py          # data/sim_stage3/summary/events_*.npz
pixi run python sim/stage3/scripts/xover.py
pixi run python sim/stage3/scripts/p1_model_mg.py      # ~5 min
pixi run python sim/stage3/scripts/p1_results.py
pixi run python sim/stage3/scripts/p2_results.py
pixi run python sim/stage3/scripts/val_v5.py           # 0.23 CPU-h
pixi run python sim/stage3/scripts/val_v9.py
pixi run python sim/stage3/scripts/val_v7_status4.py
pixi run python sim/stage3/scripts/val_v7.py
pixi run python sim/stage3/scripts/val_vscale.py
pixi run python sim/stage3/scripts/val_c5kev.py        # 0.96 CPU-h
pixi run python sim/stage3/scripts/fix_a1_floor.py
pixi run python sim/stage3/scripts/fix_bstar_off.py    # 0.84 CPU-h
pixi run python sim/stage3/scripts/val_vscale_s3.py
(cd acts && pixi run python ../sim/stage3/validation/val_v8_merge.py <file> <A|C> <0|1> 10)   # acts env
(cd acts && pixi run python ../sim/stage3/validation/val_v8.py <file> 10)                     # acts env
pixi run python sim/stage3/scripts/fix_r2_bstar_context.py
pixi run python sim/stage3/scripts/fix_r2_notes.py
pixi run python sim/stage3/scripts/make_docs.py        # SAMPLES.md, README/VALIDATION auto blocks
```

  The gate validations V1–V6 (`sim/stage3/validation/val_v*.py`) were chained by `sim/stage3/validation/run_chain.sh`.
- **CPU.** 207.5 CPU-h on the Mac and 375.5 CPU-h on the PC (sum of per-event process time). The plan estimated 498 M3
  CPU-h (`README.md` headline 1).
- **Already in the repo.** `sim/stage3/results/*.json` (`P1.json`, `P2.json`, `P2_points.json`, `merge.json`, `xover.json`,
  `V*.json`, `FIX_*.json`), `figures/`, generated `SAMPLES.md`, `VALIDATION.md`, `README.md` tables, `jobs/*.json`,
  `code/surfaces_s3.json`.

### 3.5 Stage 4: ACTS Phase-2-like tracker at PU 200 and the analysis (`acts/`, `acts/stage4/`)

- **Purpose.** Inject the Stage 3 quirk hits into an ACTS geometry built from the Stage 3 surfaces, overlay Pythia8 PU 200
  through Fatras, digitise (smearing, `doMerge = False`), run CKF, run the dedicated barrel plane finder, and derive
  background, efficiency and fallback limits under a working-point rule frozen in advance.
- **Read.**
  - `acts/stage4/STAGE4_RESULTS.md`: results, §11 provenance and reproduction.
  - `acts/stage4/plan.md`: design, 2,111 lines.
  - `acts/stage4/WP_RULE.md`: frozen rule, plus `WP_RULE_PC19.md` and `HASH_ADDENDUM.md`.
  - Gate reports: `G1_REPORT.md`, `G1B_REPORT.md`, `G2A_REPORT.md`, `g3/G3_REPORT.md`.
  - Runs: `C1_LAUNCH.md` and `A2FC_REPORT.md`.
  - Install: `acts/INSTALL_CHECK.md`. Finder: `acts/stage4/finder/README.md`.
- **Environments.** The runner, finder and analysis run in the **TT env** from TT. Each job's simulation step runs in the
  **acts env** through `pixi run --manifest-path acts/pixi.toml …` (`run_stage4.py` header).
- **Smoke tests:**

```
cd TT/acts && nice pixi run python scripts/smoke_test.py 400 200     # acts env, ~39 s (INSTALL_CHECK §8)
pixi run python -m acts.stage4.run_stage4 smoke                       # from TT, 2 PU-only jobs, ~5 min (dev)
```

- **Geometry (already built, in the repo).** `python3 -I acts/geometry/build_cms_phase2_public.py` →
  `acts/geometry/cms_phase2_public.json` (needs `data/tdr_geometry/`). `acts/stage4/code/s4geo.py` builds the ACTS
  geometry at run time from `sim/stage3/code/surfaces_s3.json`.
- **Production** (from TT; `run_stage4.py` header, `C1_LAUNCH.md` §3–5, `run_a2fc.py` header). Job lists are in the repo
  (`acts/stage4/jobs/*.json`); `manifest` rewrites them.

```
pixi run python -m acts.stage4.run_stage4 manifest                    # writes acts/stage4/jobs/{C1,C2,C4p,G3,smoke}.json
nohup nice -n 10 caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign C1a --workers 7 --mem-gb 19 > data/acts_stage4/prod/C1/run_stdout_C1a.txt 2>&1 &
#   then C1b (output dir prod/C1), then C2B (output dir prod/C2) with the same flags; acts/stage4/validation/chain_c1.sh chains them
pixi run python -m acts.stage4.run_stage4 status --campaign C1a       # likewise C1b, C2B
pixi run python -m acts.stage4.run_stage4 check  --campaign C1a       # deep validation (V4-1)
pixi run python -m acts.stage4.run_a2fc manifest                      # A2FC: full-chain revert of the 9 points in investigation/V46_REVERT_SET.json
nohup nice -n 5 caffeinate -i pixi run python -m acts.stage4.run_a2fc run --workers 7 --mem-gb 19
pixi run python -m acts.stage4.run_a2fc check
```

  Graceful stop: create `data/acts_stage4/prod/<campaign>/STOP`. Reruns skip finished jobs. The memory budget assumes a
  24 GB machine (4 GB per B2 job; `C1_LAUNCH.md` §4).

| campaign | jobs | CPU-h (`STAGE4_RESULTS.md` §11.1) | wall (7 workers, `C1_LAUNCH.md` §4) |
|---|---|---|---|
| C1a (signal A1/A2/A5, C′) | 875 | 55.5 | 7.6–8.7 h (estimate) |
| C1b (PU B1, SM, density) | 760 | 172.1 | 23.4–26.9 h (estimate) |
| C2B (PU ρ = 2) | 480 | 145.0 | 23.7–27.2 h after reordering (estimate) |
| A2FC | 180 | 9.7 | — |
| **total** | **2,295** | **382** | |

- **Freeze guards. Read these before changing any file.**
  - `acts/stage4/frozen_inputs.json` (frozen 2026-10-13, `t_seed = 4`) holds the frozen finder constants and the sha256 of
    `WP_RULE.md`, `finder/finder.py`, `finder/kernels.py` and others. Production manifests **refuse to run** without it
    (`run_stage4.py` l.21, l.570-573).
  - **Stage 4 analysis freeze:** `acts/stage4/analysis/inputs/analysis_freeze.json` (sha256 b42aef4d…, 32 files) lists the
    sha256 of every analysis module (`acts/stage4/analysis/*.py`), its `inputs/*.json`, parts of `finder/`, `code/` and `g3/`,
    `jobs/C1.json`, `jobs/A2FC.json`, `investigation/V46_REVERT_SET.json`, `sim/stage3/results/P2.json` **and
    `data/sim_stage3/STAGE3_INDEX.json`**.
  - `run_all` prints signal efficiencies, products and limits only when every one of these files matches. Otherwise it
    needs `--dev`, and **every output is stamped "DEV (not frozen / not a result)"** (`analysis_freeze.json` "note";
    `run_all.py` l.169, l.262, l.291-304).
  - `run_all` also refuses if the governing documents changed (WP_RULE 1b2ea9bd…, PC19 d30bcc2f…, HASH_ADDENDUM e273c077…)
    or if one background union mixes T_seed values (`run_all.py` docstring).
  - Consequence: `jobs/C1.json` and `jobs/A2FC.json` are frozen files. Re-running `run_stage4 manifest` or
    `run_a2fc manifest` changes them unless the output is byte-identical. Run the existing job lists instead.
- **Analysis** (from TT; `run_all.py` docstring; the command of the result is in `STAGE4_RESULTS.md` §11.1):

```
nice -n 15 pixi run python -m acts.stage4.analysis.run_all --campaigns C1a,C1b,C2B,A2FC --out data/acts_stage4/analysis/C12FC_v1
python3 -I acts/stage4/results/make_stage4_summary.py      # -> data/acts_stage4/analysis/STAGE4_SUMMARY.json, acts/stage4/results/tables_C12FC_v1.md, headline_C12FC_v1.json
python3 -I acts/stage4/results/selfcheck_stage4.py         # headline numbers of STAGE4_RESULTS.md vs the JSON
```

  - The analysis run took 2,497 s (`STAGE4_RESULTS.md` §11.1). Module self-test: `acts/stage4/analysis/selftest.py`.
  - `make_stage4_summary.py` also reads `data/acts_stage4/investigation/*.json` (written by the scripts in
    `acts/stage4/investigation/`; the order to run them in is NOT DOCUMENTED in one place) and
    `data/sim/npz/S-TRGS_m500.npz`.
  - U-2 B+MS panel (truth level, < 1 CPU-min): `pixi run python acts/stage4/u2_panel/make_u2_panel.py`. It reads
    `data/sim_stage3/summary/events_p1.npz`.
- **Already in the repo.**
  - `acts/stage4/STAGE4_RESULTS.md` (and the superseded `STAGE4_RESULTS_C12v1.md`).
  - `acts/stage4/results/{headline_C12FC_v1.json,tables_C12FC_v1.md}`.
  - `acts/stage4/u2_panel/{u2_panel.json,U2_PANEL.md,fig/}`.
  - The frozen inputs and job lists.
  - `acts/stage4/investigation/INV_*.md`.
  - All reviews in `acts/stage4/review/`.
- **Also in the repo** (tracked exceptions under `data/`): `STAGE4_SUMMARY.json`, the `C12FC_v1/` outputs (`signal_eff.json`,
  `limits.json`, `bsum_wp.json`, `background.json`, …) and `data/acts_stage4/investigation/*.json`. The raw production
  (`data/acts_stage4/prod/`, 36 GB) is not.

### 3.6 Stage 5: figures (`stage5/`)

- **Purpose.** The final figure set with the project's plotting conventions and the non-CMS label "Private work
  (simulation)".
- **Read.** `stage5/FIGURES_FINAL.md`, plan `stage5/FIGURE_PLAN.md`, existing-limit overlay `stage5/EXTERNAL_BOUNDS.md`.
- **Commands** (from TT; `stage5/make_figures.py` header, `FIGURES_FINAL.md`):

```
nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --truth
nice -n 15 pixi run python stage5/make_figures.py --final --truth --truth-rlabel sqrt_s
nice -n 15 pixi run python stage5/make_figures.py --truth                                   # truth figures only
nice -n 15 pixi run python stage5/make_figures.py --results stage5/placeholder_inputs       # synthetic placeholders (pipeline test)
```

- **Inputs.**
  - Detector figures D1–D11 need `data/acts_stage4/analysis/C12FC_v1/` and `STAGE4_SUMMARY.json` (both in the repo), plus
    `data/sim/npz/S-TRGS_m500.npz` (Stage 2) and, for D11, a B1 job file in `data/acts_stage4/prod/` (Stage 4).
  - **Truth figures T1–T4 need only repo files** (`acts/stage4/u2_panel/u2_panel.json`, `sim/stage3/results/P2.json`), so
    they can be regenerated without `data/`.
  - `--final` refuses placeholder, DEV and dry-run inputs.
- **External bounds.** `stage5/external_bounds.json` is in the repo. To rebuild it:
  `python3 -I stage5/build_external_bounds.py --hepdata-t2 <t2.csv> --faser-fig5 <summary_limits_gray.pdf>`, with the CSV from
  https://www.hepdata.net/download/table/ins3184325/Exclusion%20Contours/1/csv and the PDF from the arXiv:2607.26195 source
  (`figs/summary_limits_gray.pdf`), per the script header.
- **CPU.** NOT DOCUMENTED (minutes).
- **Already in the repo.** `stage5/figures/final/` (PDF, PNG and JSON per figure, plus `index.json`), `final/truth/`,
  `final/truth_sqrt_s/`, `stage5/figures/placeholder/`.

### 3.7 Stage 6: CMS Open Data feasibility (`opendata/`)

- **Purpose.** A text-only note on which public CMS Open Data could validate the Stage 4 inputs. No data was downloaded or
  analysed.
- **Read.** `opendata/STAGE6_FEASIBILITY.md` (reviews in `opendata/review/`).
- **Nothing to run.** The policy caveat in the note applies: CMS members must check the internal rules before using
  Open Data.

### 3.8 Paper inputs

- The figures in `paper/figures/` are **copies** of reviewed figures. Sources and sha256 are in `paper/FIGURE_MANIFEST.md`.
- The schematic is made by `pixi run python paper/figures/src/make_schematic.py` (from TT; no data).
- Bibliography provenance (INSPIRE/DataCite queries) is in `paper/BIB_PROVENANCE.md`.
- The "where each number comes from" table is in `paper/sections/B_reproduction.tex`.

---

## 4. Building the paper

From `paper/` (header of `paper/quirks_p1p2_note.tex`, and `paper/sections/B_reproduction.tex`):

    xelatex quirks_p1p2_note && bibtex quirks_p1p2_note && xelatex quirks_p1p2_note && xelatex quirks_p1p2_note

Companion note, from `paper/companion/` (header of `prior_work_companion.tex`; it includes `../preamble`):

    xelatex prior_work_companion && xelatex prior_work_companion

The bibliography style `paper/unsrtnat_hep.bst` and `references.bib` are in `paper/`. The author field still reads
"AUTHOR(S) --- to be filled by the user" (`quirks_p1p2_note.tex`).

---

## 5. Known gaps

### 5.1 Missing or undocumented items needed for a rerun

1. ~~Patched CT18NLO `.info` values~~: resolved, the patched `.info` files are now tracked (§2.3).
2. **How MG HEPTools was installed** (Pythia 8.313, MG5aMC_PY8_interface version) and where MG 2.9.22 was downloaded from:
   NOT DOCUMENTED.
3. **Stage 2 `probes` stage cannot run as is.** The 18 `sim/probes/*.mg` scripts contain absolute paths (`import model …`,
   `output …`, `launch …`). Because the pixi task `produce` depends on `probes`, `pixi run -e ana produce` fails on a fresh
   machine. Workaround: `bash scripts/run_all.sh produce` (§3.3).
4. **Stage 4 analysis freeze is tied to a data file.** `data/sim_stage3/STAGE3_INDEX.json` (tracked) is in
   `analysis_freeze.json`. A rerun of Stage 3 will change its hash, so a new frozen (non-DEV) analysis needs a new
   pre-registration and re-freeze. How to re-freeze (who writes `analysis_freeze.json`) is NOT DOCUMENTED as a procedure; see
   `LOG.md` 2026-10-16 "FIXER R6" and `acts/stage4/HASH_ADDENDUM.md`.
5. **Windows bundle env**: now tracked in `data/sim_stage3/bundle/quirks_sim/env/`, but
   `sim/stage3/code/make_bundle.py` still hard-codes `/Volumes/J8A/quirks_sim/env` (§2.4).
6. **Single-machine Stage 3 rerun.** The two-tree layout `out/` / `out_pc/` expected by `merge_index.py` is not described for
   one machine (§3.4).
7. **Order of the Stage 4 investigation scripts** that write `data/acts_stage4/investigation/*.json` (read by
   `make_stage4_summary.py`): NOT DOCUMENTED in one place. Each `INV_*.md` names its scripts.
8. **Athena snapshot commit hash**: NOT DOCUMENTED (only "branch main, 2026-10-07").
9. **Build commands of the three `report/*.tex` reports** (repo-root `report/`, `stage2_C001_quirks/report/`,
   `TT/report/`): NOT DOCUMENTED.
10. **Linux:** whether a `pyacts==48.0.0` Linux wheel exists is NOT DOCUMENTED (§1.1).
11. **`data/acts_stage4/frozen/`** (the freeze candidate used by dev campaigns such as `smoke`) is not in the repo.
    Without it, `run_stage4.py` falls back to the planning values (`run_stage4.py` l.324-327). Production is unaffected.

### 5.2 Hard-coded `/Users/jochoafl` paths beyond the 8 files being fixed

Excluding the 8 files being fixed (`sim/scripts/{produce.py,mg_configure.py,run_all.sh}`,
`acts/stage4/validation/{chain_c1,chain2_c1b,g1b_post_g3,prodstop_fri,prodstop_v2}.sh`), a grep over the repo (excluding
`data/`, `.pixi/`, `sim/mg_out/`, `research/cache/`, `__pycache__`) finds 588 files, plus `sim/py.py`:

| category | count | matters for a rerun? |
|---|---|---|
| Stage 2 run logs `sim/logs/*.log`/`*.mg` (MG launch/output/convert logs, `produce.log`) | 507 | no (records) |
| **Stage 2 MadGraph probe scripts `sim/probes/*.mg`** | **18** | **yes**: used by the `probes` stage of `run_all.sh` |
| Stage 2 probe logs `sim/probes/*.log` | 19 | no |
| review check scripts (`sim/review/r2_checks/*.py` 9, `sim/stage3/review/r{1,2}_checks/**/*.py` 8) | 17 | only to re-run a reviewer's check |
| review records (`*.md`, `*.log`, `*.out`, MG config diffs under `sim/review/`, `sim/stage3/review/`, `analytic/review/`) | 16 | no |
| `sim/stage3/probes/_gen/T3_causal_fastmat.py` (`sys.path.insert` to `TT/code`) | 1 | only for that planning probe |
| `sim/models/fr/make_ufo.log`, `analytic/checks/c03_causal_E_out_alpha.txt`, `analytic/numerics/results/raw/M1_run{,2}.log` | 4 | no (outputs) |
| `stage5/figures/placeholder/index.json` (records the placeholder input path) | 1 | no |
| documents: `LOG.md`, `sim/README.md` (MG and FeynRules paths, run line), `acts/stage4/{G1B_REPORT,PHASE_A_REPORT}.md`, repo-root `research/methodology.md` | 5 | no; `sim/README.md` should point to `MG5_DIR` |
| `sim/py.py`: MG's PLY parser table written into `sim/` | 1 | no; already in `.gitignore` |

Other machine-specific paths: `/Volumes/J8A/quirks_sim` in `sim/stage3/code/make_bundle.py` (USB stick) and in
`sim/stage3/RUNNING.md`.

### 5.3 Validation items that were not completed (as recorded)

- Stage 3: O-1 / D12 double-precision floor test not done (`sim/stage3/README.md` item 7). 108 status-4 events.
- Stage 4: V4-3 PARTIAL, V4-4 PARTIAL, **V4-5 NOT RUN**, V4-7 FAIL (pre-registered anti-conservative end state), V4-8 N/A
  (Mac only) (`acts/stage4/STAGE4_RESULTS.md` §11.5).
- Stage 2: V1b extension (FeynRules vs hand-written UFO at 200/1000 GeV) not delivered (`sim/VALIDATION.md` §8).

---

## 6. Open work and next steps (prioritised)

The P2 outcome is **no working point and nothing excluded**. The best expected limit is 790 × the predicted signal
(E 200, Λ = 1.5 keV) (`acts/stage4/STAGE4_RESULTS.md`, paper §13). Items 1–6 address that. Every change to the Stage 4
analysis needs a **new pre-registration**; nothing may be changed in the frozen analysis (`STAGE4_RESULTS.md` §10).

| # | item | why | effort / cost (as documented) | pointer |
|---|---|---|---|---|
| 0 | **CMS-internal check before anything else**: search CADI, CDS, McM, DAS for "quirk", then contact the EXO-LLP conveners. **Still open:** neither `LOG.md` nor `stage2_C001_quirks/LOG.md` records that it was done. Also confirm the CMS-member rules before any Open Data use | a CMS-internal quirk effort may exist; policy | week 1 | `stage2_C001_quirks/phase1_strategy/outputs/OPEN_QUESTIONS.md` Q2 (and Q13); `opendata/STAGE6_FEASIBILITY.md` policy box |
| 1 | **Data-driven PU fake estimate** in control regions (inverted MET-road or Δφ(n₃, MET) sidebands, out-of-time crossings) | "the decisive one": replaces the ρ-thinning extrapolation (σ_ln 2–8) | needs real data | `STAGE4_RESULTS.md` §10 item 1; paper §13 (i) |
| 2 | Deeper PU simulation: ρ = 3 campaign (C5) or a closure test with a lever arm at R07–R09 | removes trend and closure terms, ≈ 1 decade of B₈₄ | ≈ 1-day campaigns (compute cap) | §10 item 2; `paper/sections/C_limitation_index.tex` (C5 deferred) |
| 3 | C′ conditionals from the no-PU C′₀ samples (10⁵ per gun) with their own closure; time-tag credit for SM/C′ in SR-T | ≈ 2–2.3 decades on C′ bounds; up to ≈ 4 decades in SR-T | — | §10 items 3–4; `acts/stage4/investigation/INV_STATS_BKG.md` §5 |
| 4 | Merging-robust signal selection (merging-tolerant counting rung or a line-topology category for Λ ≳ 3 keV), lower seed-opening cut, **endcap finder** | raises the ≈ 0.3 barrel-only ε ceiling; keeps high-Λ points | — | §10 item 5; `INV_SIGNAL_EFF.md` |
| 5 | Run **C4′** (A2 grid → full chain at every Λ ≥ 3 keV point); C2-C deferred | no numpy A2 where CKF matters | — | §10 item 6; `C_limitation_index.tex` |
| 6 | PU-robust sep_IT estimator (line-consistent hits across ≥ 3 IT layers) and in-time-hit rejection for ToF | recovers the Λ⁻² and m_Q handles at PU 200 | — | §10 item 7; paper §13 (v) |
| 7 | **NLO + FxFx point** (loop-capable UFO, `p p > xe+ xe- [QCD]`, FxFx 0–1j at 500 GeV, ~200k events) | ISR-tail rate f(pT > 200) carries +12…+15 % / −11…−13 % at LO-MLM | 1–2 person-days + ≈ 10–20 CPU-h; "before publication" | `sim/DEFERRED.md` D-1 |
| 8 | QED FSR off the quirks: re-shower with `cards/pythia8_quirk_qedfsr.dat`, or keep the one-sided ℓ_max systematic −1.1 ± 0.8 % (the user chose the systematic on 2026-10-11) | absent from the delivered samples | ≈ 15 CPU-h | `sim/DEFERRED.md`; `sim/VALIDATION.md` §7 |
| 9 | Stage 1/3 precision-floor test O-1 (extended-precision step map) and the B₀ law above 5 keV | turns the k_B ≥ 10 remainder and the > 5 keV ±5 % into measurements | ≈ 1 CPU-h + 1–2 person-days; then max_boost ≤ 10⁻⁴ at ≥ 7 keV (≈ 10× cost) | `sim/stage3/DECISIONS_PENDING.md` U-1; `outputs/THEORY_GAPS_SYNTHESIS.md` §8 row 4; `analytic/NEAR_MISS_IMPULSE.md` §10 |
| 10 | Analytic ΔK(k_B, ε, γ*) to claim a law above 3 keV (U-1 option b), and an analytic MS theory of the plane thickness | P1 completeness | weeks | `DECISIONS_PENDING.md` U-1; paper §13 |
| 11 | More merged-regime toys (U-3 b) at 2–3 more masses and Ẽ 500, 15–40 keV; finer interpolation closure (TRG 450/650 GeV) | P2 coverage away from 1 TeV | ≈ 25 CPU-h per mass; ≈ 1 CPU-h per point | `DECISIONS_PENDING.md` U-3; `sim/DEFERRED.md` |
| 12 | Module-plane geometry (U-4 b) and channelised digitisation (U-5 a) as a cross-check of the `doMerge = False` baseline | detector realism in the merged regime | kernel recorder change + rerun | `DECISIONS_PENDING.md` U-4, U-5; `LOG.md` 2026-10-13 |
| 13 | CMS Open Data checks, if policy allows: (1) NI/V0/conversion rates vs radius (AOD) ≈ 1–2 weeks, 10–30 CPU-h; (2) cluster density and PU slope (2017 RAW re-reco) ≈ 3–5 weeks; (3) NoBPTX cosmic/halo rate; plus kinematic checks (Z/V+jets pT, MET tails on NanoAOD) ≈ 1 week | validates the weakest Stage 4 inputs (top-up ratios, material) | as listed | `opendata/STAGE6_FEASIBILITY.md` §3–4 |
| 14 | Theory-track follow-ups: Evans–Luty out-of-time recast update (P6, "most likely route to a stronger limit"), Athena C++ standalone comparison on ~10 events, doublet monojet recast, \|q\| = 2 window, cosmology note, ε(b) for FASER, γγ → QQ̄ with PPS | see synthesis | 2–4 weeks for the recast; others days to weeks | `outputs/THEORY_GAPS_SYNTHESIS.md` §8 (rows 2, 5, 7–12) |
| 15 | Housekeeping: apply or close the proposed edits (`analytic/PROPOSED_CHANGES.md`, `acts/PROPOSED_CHANGES.md` P1–P3, `sim/stage3/PROPOSED_CHANGES.md` P-10 wording); `paper/ISSUES.md` items (e.g. relabel σ_norm "N_IC = 1" → 2 in `HANDOVER_STAGE4.md`, restyle the Stage 3 diagnostic figures); figure restyle D-3; fill the paper author list | consistency | small | files named |
