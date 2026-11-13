# Plan — Basil (feasibility executor B: generators + Geant4), Phase 1, 2026-11-13

Scope: make MG5_aMC 2.9.22 + Pythia 8.313 + MG5aMC_PY8_interface + LHAPDF (v1 PDF sets) and Geant4 usable on the
Linux workers, measure their cost on `schrodinger`. Feasibility only, no production.

## Inputs read
AGENT_RULES.md, CLAUDE.md overrides, prompt.md §5-§6, tools/PREFLIGHT.md, TT/REPRODUCE.md, TT/sim/{VALIDATION,SAMPLES,
DEFERRED}.md, TT/sim/scripts/produce.py, TT/sim/cards/, TT/sim/pixi.toml, TT/data/sim/lhapdf/ (tracked .info,
lhapdf.conf, pdfsets.index), TT/acts/stage4/code/s4pu.py (v1 minimum-bias and SM-background Pythia settings),
publication_plan B1/B4/S1/S2, JFC agents/executor.md, methodology/07-tools.md.

Key facts taken from them:
- v1 ran MG under a pixi env `mg` (Python 3.9, six, numpy 1.26, conda-forge LHAPDF 6.5.5); HEPTools LHAPDF python
  bindings were not used (macOS segfault). Each MG output gets its own `Cards/me5_configuration.txt` (`mg_configure.py`).
- CT18NLO `.info` was patched (adds `AlphaS_FlavorScheme/NumFlavors/Lambda4/Lambda5`) because LHAPDF 6.5.5 + the MG
  Fortran glue need those keys (TT/sim/plan.md l.56, REPRODUCE §2.3). NNPDF23_lo_as_0130_qed member 0 downloaded
  because the HEPTools tarballs were 0-byte.
- v1 Pythia runs were done by produce.py itself (MG re-orders the tune card). Minimum bias: s4pu.py `PY_MB` + CP5.
- v1 SM backgrounds were Pythia 2→2 (not MG); recorded LO: Z(νν)+j, pT̂>150, truth MET>200 → 14.6 pb (acts/stage4/plan.md l.1060).

## Steps (priority 1 → 2 → 3 → 5 → 4)
1. **Install (task 1).** Under `/home/users/jdochoa/sw/`:
   - `sw/mg5/MG5_aMC_v2_9_22/` from the official launchpad tarball (sha256 recorded).
   - pixi workspace `sw/envs/mg/` (linux-64): python 3.9, six, numpy 1.26, lhapdf (conda-forge), so MG's python
     and `lhapdf-config` come from one place (same choice as v1; Python 3.12 is not supported by MG 2.9.x — verify).
   - Pythia 8.313 + MG5aMC_PY8_interface via MG's HEPTools installer (`install pythia8`, `install mg5amc_py8_interface`)
     built on schrodinger. Pythia's LHAPDF linking is not needed (CP5 uses the internal pSet 20). HepMC2 comes with the
     installer. If the installer fails, fall back to a manual Pythia 8.313 build.
   - LHAPDF data dir `sw/lhapdf_data/`: copy the tracked `.info`, `lhapdf.conf`, `pdfsets.index`, add the CT18NLO members
     (59 `.dat`) and NNPDF23_lo_as_0130_qed member 0 from lhapdfsets.web.cern.ch; keep the patched `.info`.
   - Script: `tools/install/install_generators.sh` (idempotent, records versions/sha256).
2. **Test samples (task 2).** Driver in `phase1_strategy/src/generators/`: E, m=200 GeV, E-LOPS cards (p p > xe+ xe-,
   lhaid 14400, dyn −1, 14 TeV), 1000 events, showered with our own PY8 card (CP5 + quirk_common); SM: Z(νν)+j LO
   (`p p > vl vl~ j`, MET>200 via `misset`) 1000 events, showered. Compare σ_LO with v1 (E-LOPS m200: 92.26 fb,
   SAMPLES.md; probe 92.52 ± 0.20 fb VALIDATION §1.1) as a z-score; SM vs v1 Pythia 14.6 pb (different generator: ESTIMATE).
   Outputs in `data/feasibility/generators/<sample>/` (LHE.gz, HepMC; `.part`→rename; `MANIFEST.txt` sha256; ledger marker).
3. **Benchmarks (task 3)** on schrodinger, `/usr/bin/time -v`, 3 repeats, single and 3 concurrent:
   MG output+compile per process; MG event generation /1000 ev; PY8 shower /1000 ev; Pythia MB /1000 ev (v1 PY_MB+CP5,
   pythia8 standalone via a small C++ main against the HEPTools Pythia); output sizes per event (LHE.gz, HepMC, npz-like).
4. **Geant4 (task 5).** conda-forge `geant4` + data sets in pixi workspace `sw/envs/g4/`; build a minimal C++ app
   (cylinders of Si + slabs, 3.8 T solenoid field, π± gun, FTFP_BERT, record secondary vertices from hadronic inelastic
   and decay processes); time CPU/event and RSS. Write the Geant4 build/integration plan.
5. **NLO (task 4).** Check whether the quirk UFO has NLO counterterms (it does not have `CT_couplings`/`CT_vertices` →
   expect no `[QCD]`), test MG `p p > xe+ xe- [QCD]` with the loop_sm route (the quirk is colourless, so QCD corrections to
   DY-like production only need SM QCD counterterms; check whether MG accepts a model without them), time a fixed-order
   NLO if feasible (≤ 1 CPU-h); else report the obstacle and alternatives (Resummino; published tables). Time the QED-FSR
   re-shower with `pythia8_quirk_qedfsr.dat`.

## Artifacts
- `outputs/feasibility/FEAS_B_generators_basil.md` (JFC sections), `outputs/feasibility/benchmarks_generators.json`.
- `tools/install/install_generators.sh`, `tools/install/install_geant4.sh`.
- `src/generators/` drivers and benchmark scripts. Logs: `logs/executor_basil_2026-11-13_14-50.md`;
  decisions to `experiment_log.md` with `[Basil]`.
- No figures planned (benchmark tables only).
