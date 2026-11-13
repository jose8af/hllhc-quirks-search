# Session log — executor Basil (feasibility B: generators + Geant4), 2026-11-13

- 14:50 Read binding docs, v1 sim docs/cards/LHAPDF files, plan items. Plan written: outputs/feasibility/plan_basil.md.
- 15:05 MG 2.9.22 + Pythia 8.313 + PDF tarballs downloaded (sha256 recorded); LHAPDF data dir built with v1 patched .info; pixi envs mg/g4 installing (cache-lock contention).
- 15:38 RESUMED after 15:12 OOM interruption; tarballs, MG tree, LHAPDF data re-verified (see experiment_log).
- 15:42 Geant4 11.4.3 env installed node-locally on schrodinger (install_g4_local.sh); later re-locked 3x to add header packages expat, zlib, freetype (Geant4Config.cmake find_dependency; system versions too old). g4sv app builds and runs (200 pions OK).
- 15:47 HEPTools (Pythia 8.313 + PY8 interface) built on /var/tmp, installed as one tarball (925 files) from schrodinger with ionice.
- 15:55 MG E_LOPS output + launch OK after two fixes (conda libgfortran in LD_LIBRARY_PATH; auto_update string). Run card == v1 E-LOPS card except nevents/iseed.
- 15:58 PY8 interface fixes: -DGZIP (LHEF gz read) and HepMC named-weight patch + -DHEPMC2HACK (one HepMC file, not 20). Rebuilding.
- 16:14 Task 2 done: E_LOPS_m200 and ZNN_J test samples (1000 showered events each) on cajuela data/feasibility/generators/, MANIFEST + 6 markers. sigma E200 = 92.33 +- 0.07 fb vs v1 92.26 +- 0.04 (z = 0.91).
- 16:25 Task 4: loop_quirkE (loop_sm + quirks) runs p p > xe+ xe- [QCD] fixed order; K(200) = 1.165 +- 0.002 (mu = HT/2, CT18NLO); ~2 CPU-min per point. Stopped an MG auto-build of OneLOop inside the NFS install (removed).
- 16:30 Task 3 benchmark suite started on schrodinger (bench_all.sh). FEAS_B draft written (tasks 1, 2, 4, Geant4 plan).
- 16:55 Task 3 benchmark suite complete (13 benchmarks x 6 runs, 0 failures after fixes); Task 5 Geant4 benchmark done (0.134 ms/gun primary mode, 5.3 % vertex fraction).
- 17:05 FEAS_B and benchmarks_generators.json final. Scratch kept on schrodinger: basil_samples (699 MB, compiled E_LOPS/ZNN_J dirs), basil_nlo (182 MB, E_NLO dir); benchmark scratch deleted. No processes left.
