# Stage 4: ACTS install feasibility check (E5, 2026-10-11)

Scope: investigation and light probes only (1 thread, `nice`). Nothing was installed system-wide or into any project
environment. Machine: macOS 26.6.2 (Darwin 25.6), arm64, 8 cores, 24 GB, 180 GiB free disk. Evidence and commands are in
`E5_session_log.md`. Probe scripts: `probe_smoke.py`, `probe_hybrid.py`, `probe_pu_timing.py`, `probe_ckf_timing.py`,
`probe_locksize.py`. Geometry: `geometry/cms_phase2_public.json` (built by `geometry/build_cms_phase2_public.py`).

## 1. Summary and recommendation

> **Update 2026-10-11:** the user approved all recommendations. R1 is installed (`acts/pixi.toml`, 640 MB) and the smoke
> test passes, including the Pythia8 PU-200 → ACTS chain. See §8.

- **A ready-made ACTS with Python bindings exists for this Mac.** The ACTS project publishes PyPI wheels, `pyacts`
  48.0.0 (2026-09-30), cp311-cp314, tag `macosx_26_0_arm64`, 17.6 MB. They include Core, Fatras, the Examples framework,
  digitisation, seeding, CKF, vertexing, the Generic/Telescope detectors, and CSV/JSON/HepMC3/Parquet I/O. They do **not**
  include ROOT, Pythia8, EDM4hep, Geant4, DD4hep, TGeo or the Open Data Detector (ODD).
- conda-forge has only `acts-core` 45.5.1, the C++ core library with no bindings. A conda-forge `acts` package does not exist.
- **Tested here, in a scratch venv:**
  - The hybrid chain runs: geometry → Fatras on SM particles → externally computed sim-hits injected from a Python
    algorithm → ACTS digitisation → CSV output.
  - Timing: 0.39 s/event for 8000 pions (Fatras + digitisation), and 4.2 s/event when seeding + CKF are added.
- **Recommended route: R1.** A new pixi env in `acts/` with Python 3.12, conda-forge `pythia8` + `pyhepmc` (PU-200
  minimum bias written to HepMC3 and read by ACTS `HepMC3Reader`), and PyPI `pyacts==48.0.0`.
  - Cost: 174 MB conda download + 17.6 MB wheel, about 0.5-0.8 GB on disk (ESTIMATE), a few minutes, no compilation.
  - Do not source-build. That would need 0.5-2.3 GB of dependencies and about 1-3 h of compilation on 8 cores (ESTIMATE),
    and ACTS does not officially support it on macOS.
- **Custom stepper: not recommended.** ACTS steppers are C++ templates behind a single-trajectory interface. The causal
  string (two coupled endpoints plus a queue of null segments) does not fit the model. Keep T3_causal as the trajectory
  engine and use ACTS only for geometry, digitisation and SM backgrounds.
- **Geometry: the inputs in `data/tdr_geometry/` were all failed downloads** (CERN 404 pages and a bot-check page). The
  public layout was rebuilt from the TDR (fetched via INSPIRE) and from tkLayout OT806_IT742, the geometry CMS currently
  exports to CMSSW (scenario D111). Per-layer material is not public: the file marks it ESTIMATE/UNVERIFIED.

## 2. Install routes

| Route | Works on osx-arm64? | Python / Fatras / digitisation? | Download / disk | Build time | Risks |
|---|---|---|---|---|---|
| **R1. PyPI `pyacts` 48.0.0 wheel in a pixi env** (conda: python 3.12, numpy, scipy, matplotlib, mplhep, uproot, pythia8 8.312, pyhepmc, numba; PyPI: pyacts) | **Yes.** Tested: import, geometry, Fatras, digitisation, seeding/CKF, Python algorithms | Yes / yes / yes. No ROOT, Pythia8 or EDM4hep plugins and no ODD. Pythia8 runs standalone → HepMC3 → `acts.examples.hepmc3.HepMC3Reader`. ROOT files are readable via `acts.examples.uproot` | Dry-run solve: 107 conda packages, 174 MB, plus the 17.6 MB wheel. Installed ≈ 0.5-0.8 GB (ESTIMATE; the probe venv with the wheel unpacked was 70 MB) | Minutes, no compilation | (i) The wheel needs macOS ≥ 26: pixi needs `[system-requirements] macos = "26.0"`, and collaborators on macOS 15 must pin ≤ 46.8.1 (`macosx_15_0` wheels). (ii) Two HepMC3 copies (wheel-bundled and conda) live in one process; no clash seen, but untested with pyhepmc imported. (iii) The Python API changes between major versions (v46→48 within 6 months): pin the version |
| R1′. Same wheel in a plain venv on the TT Python | Yes (this is what the probes used: `acts/probe/venv`, `--system-site-packages` on TT's py3.12, TT env not modified) | as R1 | 17.6 MB | seconds | Not reproducible (depends on TT env internals). Probe only |
| R2. conda-forge `acts-core` 45.5.1 | Yes (2.4 MiB; deps libboost only) | **No.** The feedstock recipe builds the default CMake options: Core only, no `ACTS_BUILD_PYTHON_BINDINGS`, Fatras or Examples (`conda-forge/acts-feedstock recipe/recipe.yaml`) | 2.4 MiB + Boost | — | Useful only for a C++ plugin that links ActsCore |
| R3. Source build, deps from conda-forge (cxx-compiler, cmake, ninja, libboost-devel 1.92, eigen 5.0.1, pybind11 3.1, tbb-devel, nlohmann_json, hepmc3 3.3.1, pythia8 8.312, root 6.3x). CMake: `-DACTS_BUILD_PYTHON_BINDINGS=ON -DACTS_BUILD_FATRAS=ON -DACTS_BUILD_EXAMPLES=ON -DACTS_BUILD_EXAMPLES_PYTHIA8=ON -DACTS_BUILD_PLUGIN_ROOT=ON -DACTS_BUILD_EXAMPLES_ROOT=ON` (+ `_GEANT4`, `_DD4HEP`, `_ODD` optional) | Probably (all deps exist for osx-arm64). ACTS docs: "Building and running ACTS on your local machine is not officially supported" (docs/pages/contributing/building_acts.md, v48.0.0) | Everything, including the Pythia8 and ROOT plugins (EDM4hep: podio/edm4hep are **not** on conda-forge) | Deps: 275 packages, **511 MB** (no Geant4/DD4hep) or 310 packages, **2.29 GB** with Geant4 11.4 + data (1.55 GB) + DD4hep. Build tree ≈ 5-10 GB (ESTIMATE) | ≈ 1-3 h on 8 cores (ESTIMATE, not tried). Must wait for MadGraph to finish | Clang/libc++ availability macros (the feedstock adds `-D_LIBCPP_DISABLE_AVAILABILITY` on osx), Eigen 5 vs ACTS expectations, ROOT C++ standard (cxx23 build resolved), codegen step downloads `uv` + Python unless the source archive with `prebuilt-codegen` is used. Only needed for ROOT/Pythia8 plugins or for C++ development (a custom stepper) |
| R4. Docker `ghcr.io/acts-project/ubuntu2604` (tag 91; multi-arch, arm64 0.60 GB compressed) | Docker client 28.3.2 present, **daemon not running** (Docker Desktop not started) | Dependency image only (apt packages: compilers, cmake, python; Dockerfile in acts-project/machines). **No prebuilt ACTS**: you build inside | 0.6 GB image + build | ≈ 1-3 h inside the VM (ESTIMATE) + VM overhead | `ubuntu2404` and the older images are amd64 only (Rosetta emulation). Docker Desktop memory share competes with MadGraph |
| R5. LCG views / CVMFS | **No** (Linux x86_64/aarch64 only; ACTS stopped producing LCG containers) | — | — | — | Use on lxplus only (CMS account) |
| R6. Spack | Possible (ACTS docs offer it) | Everything | Several GB | Many hours (builds ROOT/Geant4 from source) | Not worth it on this machine |

## 3. API capabilities for the hybrid design (pyacts 48.0.0, tested unless marked)

| Need | Available in the wheel? | How / evidence |
|---|---|---|
| Custom cylinder/disc tracking geometry from Python | Yes (API present; **end-to-end build not exercised**) | Gen-3 `acts.Blueprint`, `CylinderContainerBlueprintNode`, `LayerBlueprintNode.surfaces = [...]`, `StaticBlueprintNode`, `MaterialDesignatorBlueprintNode`, then `root.construct(...)` (ACTS `Examples/Scripts/Python/blueprint.py`). Sensitive modules via `acts.json.readDetectorElementsFromJson(SurfaceJsonOptions, thickness)` → `JsonDetectorElement`. Fallback: `acts.examples.GenericDetector` (tested, 18 728 sensitive surfaces) as a stand-in. TGeo/GDML/DD4hep import is **not** in the wheel |
| Surfaces | Yes | `Surface.createCylinder/createDisc/createPlane`, `center`, `normal`, `localToGlobal`, `isOnSurface`, `insideBounds`; `TrackingGeometry.visitSurfaces`, `geoIdSurfaceMap()` (tested) |
| Intersect externally supplied trajectory points/segments with surfaces | **Partly.** No `Surface.intersect` or `globalToLocal` in Python. `DigitizationCoordinatesConverter.globalToLocal` exists | Plan: intersect T3_causal chords with the module planes in numpy (trivial for planes/cylinders; we have the 17 092 module positions), then build `acts.examples.SimHit(geoId, barcode, pos4, mom4_before, mom4_after)` and insert into a `SimHitContainer` from a Python `IAlgorithm` (**tested**: 7 injected hits/event digitised with 59 Fatras hits → 66 measurements). The hit position must lie on the surface |
| Digitisation config | Yes (tested with the smearing JSON) | `acts.examples.json.readDigiConfigFromJson`; per-volume/layer entries: **smearing** (Gauss/Uniform/Digital per local index; a 1-index entry = strip measuring loc0 only, so 2S "no z" is native) or **geometric** segmentation (bins in loc0/loc1, threshold, charge smearing, clusterisation with merging). Templates: `Examples/Configs/{generic,odd}-digi-{smearing,geometric}-config.json`. For CMS: IT 25 × 100 µm² (geometric), PS 100 µm × 1.467 mm (2D), 2S 90 µm × 1-index (or 2 bins of 50.25 mm) |
| Fatras simulation of SM particles with material | Yes (tested) | `addFatras` / `FatrasSimulation.Config` (MS, ionisation, brems, photon conversion, `pMin`). Material from a JSON material map (`JsonMaterialDecorator`) or `MaterialDesignatorBlueprintNode`. Python-side `Material`/`MaterialSlab` constructors are not exposed |
| Pythia8 minimum bias for PU-200 | Not as an ACTS plugin (`acts.examples.pythia8` raises ModuleNotFoundError) | Run conda-forge `pythia8` 8.312 (Python bindings) or the MG HEPTools Pythia8 8.313 already used in `sim/` (do not touch that env) → write HepMC3 → `acts.examples.hepmc3.HepMC3Reader` + `HepMC3InputConverter` → Fatras. Vertex smearing via `GaussianVertexGenerator` / `LumiBlockVertexGenerator` |
| Reconstruction (fakes, combinatorics) | Yes (tested) | `addSeeding` (GridTriplet, Orthogonal, Hough, ...) + `addCKFTracks` + ambiguity resolution + vertexing. 8000 pions: 4.2 s/event/thread |
| ROOT I/O | Write: no. Read: via `acts.examples.uproot` (needs `uproot`) | CSV and Parquet (Arrow) writers are available |
| Performance | — | Cold import 6.9 s. Fatras + digitisation at 8000 charged particles: 0.39 s/event/thread. Full chain with CKF: 4.2 s/event/thread (uniform-η pion gun from the origin, not real minimum bias; real PU-200 with σ_z ≈ 5 cm will differ, UNVERIFIED) |

## 4. Custom-stepper assessment

- **Python is not possible.** The Python layer exposes only concrete propagators: `EigenPropagator`, `AtlasPropagator`,
  `StraightLinePropagator`, `SympyPropagator`, each with `propagateToSurface(BoundTrackParameters, Surface, options)`.
  There is no hook for a user stepper or force. Steppers are C++20 types checked against `Acts::Concepts::StepperConcept`
  (`Core/include/Acts/Propagator/StepperConcept.hpp`, v48.0.0).
- **The causal string does not fit the propagation model.**
  - The concept is a single trajectory: one `position()`, `direction()`, `qOverP()`, `time()`, a step size, and
    `transportToCurvilinear` (Jacobian/covariance transport).
  - The navigator intersects that one state with the next surfaces.
  - The quirk pair has two endpoints at different places, hitting different modules at different times. They are coupled
    through the causal string history: the queue of null segments, with kicks propagated along the string (T3_causal).
  - `MultiStepperLoop` / `MultiEigenStepperLoop` exist, but for Gaussian-sum-filter mixtures that share one navigation
    stream, not for independent bodies.
  - The causal step is an exact piecewise-hyperbolic update with a max-boost split, not an RK4 step in a smooth field, so
    `EigenStepper` extensions (force terms added to the RK stages) would reintroduce exactly the integration error that
    T2/T3 removed.
- **What a C++ plugin would involve:**
  - (a) A source build of ACTS (R3).
  - (b) A `QuirkPairStepper` whose State holds both endpoints, the string queue and B-field caches. Each `step()` advances
    the endpoint that lags in time and exposes it as the "current" particle; alternatively, two coupled propagations share
    a string object and are synchronised by an actor.
  - (c) Navigation for two positions: two navigator states, or a custom actor that records crossings of the sensitive
    surfaces for the passive endpoint.
  - (d) Material interaction hooks reusing Fatras interactors (MS, ionisation) for both endpoints.
  - (e) pybind11 bindings and a Fatras-like simulation algorithm that emits SimHits for both.
  - (f) Validation against T3_causal: vacuum ExactPair, the B-field thickness law, MS floor.
  - Effort: **6-12 weeks** for someone fluent in ACTS internals and C++20 templates. Low confidence. Ongoing maintenance:
    the ACTS API moved v46 → v48 in six months.
- **What it would buy:** the same hits that T3_causal + injection already give, now inside one ACTS event loop.
  - It adds no physics.
  - The relevant CMS-integration target is CMSSW/Geant4 (the ATLAS/FASER precedent is a Geant4 extension,
    `Simulation/G4Extensions/Quirks`), not ACTS.
- **Recommendation: hybrid only.** Revisit the custom stepper only if a CMS-internal Geant4 implementation is planned. In
  that case write it as a Geant4 extension and reuse T3_causal as the reference.

## 5. Geometry extraction status

- **The inputs in `data/tdr_geometry/` are unusable.**
  - `idx.html` and the four `OT6xx_200_IT4025.html` files are byte-identical CERN "404 - Not found" pages
    (md5 `6a93d9c7...`).
  - `tdr.pdf` is a 7.5 KB HTML page ("Making sure you're not a bot!", the CERN CDS bot check). It is not a PDF.
  - Not edited (outside `acts/`). Suggest replacing them (decision D5).
- **Public sources obtained instead** (first into `acts/probe/geo_dl/`, 126 MB; moved on 2026-10-11 to `data/tdr_geometry/` after D5, see §8):
  - CMS-TDR-014 PDF (353 pp, 105 MB) via INSPIRE record 1614103 (`https://inspirehep.net/files/338a99fa62dec25fcbc18d806bd7fb71`).
    Text extracted with `pdftotext -layout` (`tdr.txt`).
  - tkLayout layout **OT806_IT742**: `https://cms-tklayout.web.cern.ch/cmssw/OT806_IT742/`, listed under `/cmssw/` as
    scenario **D111**, CMSSW_14_1_X, page generated 2024-04-08.
    - Files: `layout.html`, `layoutpixel.html`, `info.html`, `DetId_modules_list.csv` (17 092 modules with position, tilt,
      corners, size, sensor spacing, thickness), `DetId_sensors_list.csv`, `summary.root` (3.7 MB; it has no material
      histograms).
    - The older reference layouts (OT613_200_IT4025, OT616_200_IT620, OT800_IT6xx-8xx) are listed at `/reference/`;
      OT806_IT742/743 (2025-07-04) at `/main/`.
- **`geometry/cms_phase2_public.json` (60 kB) contains:**
  - **Module types** (sources: TDR Tables 3.1 p.29, 3.3 p.37, 9.4 p.157, 12.1-12.2 p.274; tkLayout module tables):
    - IT 25 × 100 µm² (150 µm sensors in the material model; L1 3D in D111);
    - PS: 100 µm strips 23.472 mm over 100 µm × 1.467 mm macro-pixels, spacing 1.6/2.6/4.0 mm;
    - 2S: 90 µm × 50.274 mm strips, two parallel sensors with no stereo, spacing 1.8/4.0 mm;
    - each with its binary resolution (pitch/√12) and the tkLayout parametrised resolutions (2S local y 14.5 mm; PS
      0.42 mm; IT 3-6 µm × 11-24 µm) and module masses.
  - **10 barrel layers**: TBPX L1-4 at r = 30.0/61.5/104.5/146.5 mm, |z| ≤ 200-201 mm; TBPS L1-3 at
    249.4/371.7/522.7 mm, |z| ≤ 1203 mm, with flat-part radii and the tilted rings (40-72°, 432/624/864 tilted modules);
    TB2S L1-3 at 687/860/1083 mm, |z| ≤ 1174 mm.
    - For each layer: module counts, sensor ρ range, z extent, module sizes, the TDR-2017 values side by side (TDR Tables
      9.1 p.149 and 10.1 p.236), and the T3 slab radius.
    - Layout change since the TDR: the IT barrel moved from 29.0/70.1/117.8/157.4 mm to 30.0/61.5/104.5/146.5 mm, and
      TB2S L3 from 1108 to 1083 mm. **T3's `REC_RADII` already match D111.**
  - **17 discs per side**:
    - TFPX D1-8 at z = 250-1400 mm, r 31-164 mm, 4 rings;
    - TEPX D1-4 at z = 1750-2650 mm, r 65-255 mm, 5 rings;
    - TEDD D1-5 at z = 1312-2650 mm, r 241(335)-1074 mm, 15/15/12/12/12 rings, PS inside / 2S outside;
    - per ring: r range, module type, count.
  - **Material**: there is no public per-layer x/X0 table.
    - TDR Fig. 6.2 is graphical only.
    - Measured: TBPX prototype module 0.825 % (0.72/0.95 % regions) [2407.13721].
    - The mass-based module-only ESTIMATES overestimate that measurement by ×1.6-1.9, so they are kept as upper bounds.
    - The T3 slab values (1.2 % TBPX, 2.5 % PS, 1.8 % 2S, 1.0 % service cylinder) are kept as the **UNVERIFIED** baseline,
      with an ×0.5-×2 systematic.
  - **`simplified` block**: flat cylinders and discs ready for an ACTS Blueprint or the pure-Python fallback. Tilted TBPS
    rings are approximated as flat (UNVERIFIED approximation).
- **UNVERIFIED items**:
  - material per layer;
  - the tilted-ring flat approximation;
  - OT sensor thickness (tkLayout 0.29 mm vs TDR 200 µm active);
  - the final pixel choice beyond D111.

## 6. Pure-Python fallback vs ACTS

**Fallback definition:**
- geometry from `cms_phase2_public.json`, either flat layers or the 17 092 module planes (numpy plane intersections);
- binary segmentation with pitch/√12 or the tkLayout resolutions, 2S as a 1D measurement;
- SM tracks as helices with Highland MS on the same slabs as T3;
- PU-200 as random hits drawn from the tkLayout per-module occupancies ("Hit Occ" for PU 140 in `layout.html`, scaled to
  200; UNVERIFIED);
- optionally, Pythia8 minimum-bias particles propagated as helices.

| Item | Pure-Python fallback | ACTS hybrid (R1) |
|---|---|---|
| Per-hit σ_n, IT dominance, 2S z-blindness (S-2) | Exact (analytic segmentation) | Same, plus clusterisation/merging in geometric digitisation |
| Resolution-aware coplanarity χ² on signal | Same: the finder is ours either way | Same |
| Prompt-track-pair background (helix sagitta, R2-B4) | Good (helix + Highland) | Fatras: MS + ionisation + brems + conversions with navigation through overlaps and holes |
| Random PU hits inside the plane window (occupancy combinatorics) | Parametrised (tkLayout occupancy; no correlation between hits, no loopers or secondaries) | Realistic if fed real Pythia8 minimum bias with a vertex spread: correlated hits, loopers, secondaries from conversions |
| Pattern-recognition fakes (CKF / seeding fake tracks used as plane seeds or vetoes) | **Lost** | Available (seeding + CKF, 4.2 s/event/thread at about PU-200 multiplicity) |
| Geometric inefficiency (module gaps, overlaps giving double hits per layer) | Only at module level, if the module list is used | Native |
| Material realism | Same slabs as T3 (UNVERIFIED) | **Not better unless a CMS material map is supplied**: both use our public-estimate material |
| Speed / maintenance | Fastest; no new dependency | +1 env (≈ 0.5-0.8 GB); API pinned to 48.0.0 |

**Verdict.**
- For the three deliverables the controlling effects are per-hit resolution, 2S z-blindness, hit multiplicity and
  assignment, and PU hits inside the window. The fallback gets the first three exactly and the PU occupancy approximately.
- A first Λ-edge estimate at fixed background efficiency is therefore possible without ACTS (days).
- What ACTS adds is a defensible background estimate at PU-200: correlated minimum-bias hits, secondaries, and the fake
  rate of the actual seeding. A reviewer will ask for exactly this.
- ACTS does not fix the material: that needs CMS-internal input in either route.
- Since R1 is cheap, do both: the fallback for fast scans and cross-checks, ACTS for the background numbers.

## 7. Decisions for the user

- **D1. Install route.** Approve R1? It is a new pixi env `acts/pixi.toml`:
  - py3.12, numpy, scipy, matplotlib, mplhep, uproot, pythia8, pyhepmc, numba, plus PyPI `pyacts==48.0.0`, with
    `[system-requirements] macos = "26.0"`;
  - 174 MB download + 17.6 MB, ≈ 0.5-0.8 GB on disk, minutes, no compilation;
  - it can run now, since it is light alongside MadGraph.
  - Alternative: R3 source build (0.5 GB of deps without Geant4, 1-3 h of compilation, after MadGraph), only if the
    ROOT/Pythia8 plugins are wanted.
- **D2. Custom stepper.** Accept "hybrid only" (recommended), or ask for a C++ plugin study (6-12 weeks, needs R3)?
- **D3. Geometry baseline.** tkLayout D111 (OT806_IT742, the current CMSSW export; recommended) or the 2017 TDR numbers?
  Flat-layer approximation first, module-level geometry (17 092 planes, JSON detector elements) second?
- **D4. Material.** Keep the T3 slabs with an ×0.5-×2 systematic (recommended), or seek a CMS-internal material map (CMS
  access; the user is a CMS member)?
- **D5. Broken inputs.** Replace `data/tdr_geometry/` (404/bot-check pages) with the copies in `acts/probe/geo_dl/`
  (TDR PDF 105 MB, its text 2 MB, tkLayout files 12 MB)? Move them, or delete the copies here? E5 did not touch `data/`.
- **D6. PU-200 generator.** conda-forge `pythia8` 8.312 inside the new env (recommended; independent of the MadGraph env),
  or reuse the `sim/` Pythia8 8.313 after production? Also choose the tune (CP5, as in Stage 2) and the vertex spread
  (σ_z ≈ 5 cm, UNVERIFIED).
- **D7. Fallback first?** Start the pure-Python fallback now (no install; days), in parallel with R1?

## Files and cleanup
- Written: `INSTALL_CHECK.md` (this file), `E5_session_log.md`, `geometry/cms_phase2_public.json`,
  `geometry/build_cms_phase2_public.py`, `probe_*.py`, `probe/` (scratch: downloaded docs, dry-run lock files, API stubs
  and example scripts from ACTS v48.0.0).
- Deleted after use: the pyacts wheel (17.6 MB) and the scratch venv with pyacts + uproot (92 MB). Kept: the geometry
  sources (126 MB, see D5) and the dry-run `pixi.lock` files (no environment was installed by `pixi lock`).

## 8. Installed (2026-10-11, after user approval of all recommendations)

**User decisions.** All seven recommendations were approved:
- D1: install R1;
- D2: hybrid only;
- D3: baseline D111, with the TDR-2017 numbers kept in the JSON;
- D4: T3 material with a ×0.5-×2 systematic, public information only;
- D5: move the broken files aside and install the good copies;
- D6: Pythia8 in the acts env, with a cited beam spot;
- D7: no pure-Python fallback for now.

Stage-4 physics work (finder, efficiencies) stays queued behind the Stage-2/3 checkpoints.

**Environment `acts/pixi.toml`** (separate from `../pixi.toml` and `../sim/pixi.toml`):
- Platform `{ platform = "osx-arm64", macos = "26.0" }`. This is pixi 0.72's replacement for the deprecated
  `[system-requirements] macos = "26.0"`, with the same effect.
- Installed with `nice -n 19 pixi install` in about 6 s (packages were already in the pixi cache from the dry run).
- **Disk: `acts/.pixi` = 640 MB.**
- Nothing links against the system ROOT; ROOT is not needed.

| Package | Version | Source |
|---|---|---|
| python | 3.12.15 | conda-forge |
| pyacts (ACTS) | 48.0.0 (56 MB installed) | PyPI wheel `macosx_26_0_arm64` |
| pythia8 (with Python bindings) | 8.312 | conda-forge |
| hepmc3 / pyhepmc | 3.3.1 / 2.16.1 | conda-forge |
| numpy / scipy / matplotlib / mplhep | 2.5.4 / 1.18.1 / 3.11.2 / 1.3.3 | conda-forge |
| uproot / awkward | 5.7.7 / 2.14.0 | conda-forge |

**Smoke test** (`scripts/smoke_test.py`; output `scripts/smoke_test_output.txt`). Run from `acts/` with
`nice pixi run python scripts/smoke_test.py 400 200`. 1 thread, 39 s wall. All parts PASS.

| Part | What | Result |
|---|---|---|
| A | versions | as in the table above |
| B | GenericDetector + μ gun → Fatras (3.8 T) + 7 external SimHits/event injected by a Python IAlgorithm → digitisation | 59/62/64 Fatras + 7 external → 66/69/71 measurements |
| C | Pythia8 CP5 (copy of `sim/cards/pythia8_tune_CP5.dat`), 14 TeV SoftQCD:inelastic, `ParticleDecays:limitTau0 on, tau0Max 10 mm` → full decay tree to HepMC3 with pyhepmc → `HepMC3Reader` merging 200 interactions/event with a Gaussian luminous region → charged selection (p_T > 150 MeV, \|η\| < 4) → Fatras → digitisation | Pythia: init 21 s, then 400 events in 15 s; σ_inel = 78.9 mb; ⟨N_ch(\|η\|<2.5)⟩ = 31.9 per interaction. PU-200 events: about 37 k generated particles, about 9 k selected, 93-96 k sim-hits and measurements, vertex rms z = 48-49 mm and t = 186-191 ps (input 45 mm / 190 ps). ACTS part 1.5 s/event |
| D | reads `geometry/cms_phase2_public.json` (D111 baseline, TDR-2017 and T3 radii alongside, beam spot, material baseline) | 10 layers, 17 discs per side |

**Luminous region** (`cms_phase2_public.json` → `beamspot`):
- σ_z = 45 mm: "line spread along the beam axis of about 4.5 cm rms (averaged over the length of the fill)" [CMS MTD
  TDR, CERN-LHCC-2019-003, p.2].
- σ_t = 190 ps: "rms of 180-200 ps" [ibid. p.2-3].
- Peak line density 1.9 mm⁻¹ at PU 200 [ibid. Fig. 1.1, p.3].
- σ_xy = 5.0 µm: ESTIMATE from the HL-LHC TDR CERN-2020-010, Table 2-1 p.18 (β* = 0.15 m, ε_n = 2.5 µm, at minimum β*).

**Notes:**
- Fatras raises a few benign floating-point underflows (`FLTUND` in `exp()`) at PU-200 multiplicity. The wheel's
  Sequencer aborts on unmasked FPEs by default, so the smoke test runs with `failOnUnmaskedFpe=False` (FPEs are still
  tracked).
- The GenericDetector is a stand-in. The D111 geometry builder (JSON → `JsonDetectorElement` → Blueprint) is part of the
  queued Stage-4 work.

**Data moves (D5):**
- `data/tdr_geometry/broken_downloads_2026-10-08/` now holds the six broken files.
- `data/tdr_geometry/` now holds:
  - `CMS-TDR-014_Phase2_Tracker_TDR.pdf/.txt`;
  - `tkLayout_OT806_IT742_D111/` (layout pages, module/sensor CSVs, summary.root);
  - `tkLayout_indexes/`;
  - `beamspot_sources/` (MTD TDR and HL-LHC TDR PDFs plus text).
- `data/README.md` was updated.
- `geometry/build_cms_phase2_public.py` now reads from `data/tdr_geometry/` by default.
- The proposal for the synthesis is in `acts/PROPOSED_CHANGES.md` (P1-P3).

**Superseded scratch:** the `acts/probe_*.py` scripts ran in the deleted scratch venv. `scripts/smoke_test.py` replaces
them, and they can be run in the installed env with `pixi run python probe_hybrid.py ...`.
