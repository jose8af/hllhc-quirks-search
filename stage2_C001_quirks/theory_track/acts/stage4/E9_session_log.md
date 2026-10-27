# E9 session log: Stage-4 plan (ACTS CMS-like tracker + PU 200), plan only

- 2026-10-13 start. Read executor.md, 01-core.md, TT README/LOG/BRIEF, synthesis v5 (S-2, S-5, S-18, §5), stage3 README,
  VALIDATION §0, HANDOVER_STAGE4, DECISIONS_PENDING, acts README/INSTALL_CHECK/PROPOSED_CHANGES, smoke test, val_v8*.py,
  sim README/DEFERRED, Knapen 1708.02243 §III.C-IV (plane finder, PU and conversion backgrounds).
- Inventory: p2 = 307 points, 148 011 events (all |eta_pair| < 4); mv = 60 points; Stage-3 data 1.1 GB; disk free 134 GB.
- probes: s4geo.py builds a Gen-3 geometry from the 83 physical Stage-3 surfaces (T3V skipped; ETL dropped: Z-stacking with
  the r=0 beam region fails) as sensitive JsonDetectorElements + JSON material decorator (T3 x/X0, beam pipe, IT service).
  Bugs found and fixed: Fatras pMin default 0.5 GeV (kills loopers) -> 30 MeV; molar density must be mol/mm3 (x1000 error
  gave 30 % 'max steps' failures with energy loss).
- p1: muon gun closure 17 hits/central muon, all on surface (< 0.1 um); PU-200 (charged+photons, pT>50 MeV): 133 k hits/event,
  Fatras 1.3 s/event; TBPX L1 15.4 hits/cm2 at |z|<2 cm. Pythia 1.07 ms/interaction, Python HepMC3 conversion 22.8 ms.
- p2: injection one ACTS event per physics event, h_dE p4_after, doMerge=False: n_meas = n_SimHits exactly at 1/10/30 keV
  (20 events each) and with PU overlay (5 events); signal+PU 2.1 s/event incl. Fatras.
- p3 CKF (GridTriplet seeds on TBPX+TFPX, pT>0.9 GeV): 1 surface per cylinder -> CKF 23-60 s/event (measurement scan per
  whole-cylinder surface); 32 phi sectors (same geometric surfaces) -> 1.6-3.4 s/event, seeding 0.2-0.5 s; ~18 % of the
  ~125-144 k measurements on tracks; 0/205 quirk measurements on CKF tracks (6 events, 1 and 0.6 keV). Muon closure with
  sectors 120/120 x 17 hits. Peak RSS of the chain 670 MB.
- p4 finder proto (PS-pair seeds): ~93 k seeds/event, all pass a loose >= 6-layer score, best candidate = PU fake (0 signal
  hits); slow (50 s/event) -> PS seeds too imprecise. KILLED as a design.
- p5 IT-triplet seeds + PV + MET road (+-0.25 rad): road keeps ~30 k hits, 0.6-1.1e5 triplets, 5-10 s/event (numba,
  1 thread, not optimised); after 3x PV-constrained weighted refit: signal cand N_L1 = N_L2 = 10/10 barrel layers, chi2/ndf
  0.9-1.9 in 5/8 (1 keV) and 5/5 (3 keV) central E1000 events; PU-only best N_L2 <= 6 in 24 independent trials (8 PU events x 3 MET directions; the 3 keV file reuses the same PU events) [corrected: was 39 trials (24 at 1 keV file + 15
  at 3 keV file; same PU events). Ranking by seed score alone misses the signal: refit before ranking.
- First central-file pass picked forward pairs (|eta| 1.6-2.4) with no TBPX L3/L4 hits -> p2 re-run with |eta_pair| < 1.
- pyacts 48.0.0 wheels: macosx_26_0_arm64 + manylinux_2_34_x86_64 only (PyPI); conda-forge acts-core has no win-64 -> PC
  only via WSL2. SimParticle constructible from Python (HepMC3 bypass possible).
- Counting set p2: template 61 344, toy 55 921 (in_eta25 & status 1); mv 12 000. 31 % of counting-set events |eta|<1.
- plan.md §0-§4 written.
- 2026-10-13 finished: plan.md complete (§0-§12); stale probe files removed; LOG.md line written.
