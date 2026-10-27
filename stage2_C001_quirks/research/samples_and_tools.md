# C001 Quirks: samples and tools inventory (Stage 2, as of 2026-10-07)

**Author:** Stage-2 samples-and-tools agent.
**Status:** v1 complete (saved incrementally). No software was installed. Verification used only read-only API queries, `pixi search`, and the PDFs already cached locally.

**Target.** Colour-neutral, EW-charged quirk pairs:
- Drell-Yan production, m_Q ~ 0.2–1 TeV, Lambda ~ 0.3–30 keV.
- Signature: coplanar, non-helical HIT patterns in the CMS Phase-2 tracker or ATLAS ITk at PU 200.
- Consequence: samples must carry tracker hits, clusters or digis, not only reconstructed objects.

**Tracks.**
- **(C) CMS-internal is the PRIMARY track.** The user confirmed CMS membership on 2026-10-07.
- **(P) Fully public is the fast-prototyping chain.**

**Verification labels.**
- VERIFIED(api): the resource was queried live (GitLab / GitHub / Zenodo / HuggingFace / CERN Open Data / PyPI / anaconda API or `pixi search`).
- VERIFIED(pdf): read in a cached arXiv PDF.
- VERIFIED(doc): read on an official documentation web page.
- INFERRED: a reasoned link between two verified facts.
- UNVERIFIED: not checked, or not checkable without credentials.
- ESTIMATE: a numerical estimate made by this agent.

---

## 0. Headline findings (read first)

1. **A public Geant4 quirk transport extension exists:** Athena `Simulation/G4Extensions/Quirks` (Apache-2.0).
   - What it does: a custom `QuirkTransportation` process applies the infracolor string force; standard G4hIonisation, msc, brems and pair-production processes act on the quirk; a `QuirkStackingAction` alternates propagation between quirk and antiquirk.
   - It is the code that FASER 2607.26195 App. A, ref. [27], adapted.
   - It also ships a 2017-vintage standalone Geant4 test application (GNUmake build).
   - Its string force is set in MeV/mm. ESTIMATE: Lambda = 1 keV corresponds to sigma = Lambda^2/(hbar c) ≈ 5.07e3 MeV/mm; the default 1000 MeV/mm corresponds to Lambda ≈ 0.44 keV.
   - It is being actively modified: commits on 2026-08-27 by J. C. Burzynski ("Fix quirk simulation") and 2026-09-01 by M. Vessella ("More fixes for G4 quirks").
   - **This is the code to port into CMSSW SimG4Core for track C.**
2. **ATLAS appears to have a quirk search with ITk-like inputs in progress (COMPETITION).**
   - github.com/burzynski-lab/quirk-tracking (created 2026-09-09, no licence) states "MaskFormer-based quirk-pair finding for the ATLAS quirk search", with input "`Dump_GNN4Itk.root` ntuples from the quirk reconstruction chain". Its plan covers an m = 100 GeV grid over 10 Lambda points (~90k events), with "real low-mu SM MC later".
   - A GNN line is pursued in parallel; gitlab.cern.ch/mvessell/acorn is a fork with activity on 2026-09-11.
   - Which geometry the dumps use (Run-3 ID vs ITk) is UNVERIFIED. The GNN4ITk dumper and the pixel+strip-only volume ids suggest ITk.
   - The plan states that pile-up and background-only events had not yet been studied as of 2026-09-15.
   - **The PU-200 / CMS Phase-2 niche is still open, but the timeline matters.**
3. **The best public hit-level PU-200 resource is ColliderML Release 1** (HuggingFace `CERN/ColliderML-Release-1`, CC-BY-4.0, ODD geometry, Geant4/DD4hep + ACTS, 14 TeV).
   - It has 100k ttbar PU-200 events with tracker hits: 709 GB, ~7.1 MB/event.
   - Its `pileup_only_pu0` pool holds **7.33 M individually simulated minimum-bias sub-events with hits** (360 GB).
   - That pool lets you build PU-200 overlays at any mu, with no reuse of a sub-event up to ~36k crossings. This is the natural input for a random-coplanarity background study.
4. **The 2410.00269 signal and background hit dataset is public** (Zenodo 17941765, CC-BY-4.0, 16.4 GB, 25 (m, Lambda) points, toy 8/25-layer detector, no PU). Its quirk generator is "partially based on the code developed by Knapen et al.", but the Knapen code itself was not found publicly.
5. **CMS Phase-2 official MC carries tracker digis.**
   - CMSSW `EventContent_cff.py` adds `keep *_sim*Digis_*_*` and `keep *Phase2TrackerDigi*_*_*_*` to RAWSIM for `phase2_common`, "until packer/unpackers are done".
   - The FEVT content also keeps `TTClustersFromPhase2TrackerDigis` and `TTStubsFromPhase2TrackerDigis`.
   - So official GEN-SIM-DIGI-RAW(-MINIAOD) PU-200 samples (e.g. `Phase2Spring24DIGIRECOMiniAOD`) are hit-level background samples for track C.

---

## 1. Verified inventory

### 1A. Signal generation and quirk propagation

| Resource | URL / location | Format | Hits? | PU | Licence | Status (how verified) |
|---|---|---|---|---|---|---|
| Athena Geant4 quirk extension `Simulation/G4Extensions/Quirks` | https://gitlab.cern.ch/atlas/athena/-/tree/main/Simulation/G4Extensions/Quirks | C++ (Geant4 physics constructor, transport, stacking, `InfracolorForce`, `HyperbolaStepper`) + Athena python config + `standalone/` G4 test app | Produces G4 steps, so hits in any G4 geometry | n/a | Apache-2.0 (repo LICENSE) | VERIFIED(api): GitLab tree, raw `QuirksConfig.py`, `QuirkPhysicsTool.cxx`, `standalone/*`, commit log. Config keys MASS, CHARGE, PDGID, STRINGFORCE [MeV/mm]; default PDGID 10000100 in standalone |
| Athena Geant4 version | Athena main (`Projects/Athena/version.txt` = 25.0.75) | | | | | Geant4 version used by Athena: UNVERIFIED. The FASER adaptation (calypso) is not on calypso master (VERIFIED(api): calypso `Simulation/G4Extensions` contains only `Pythia8Decayer`) |
| FASER quirk Geant4 adaptation (2607.26195 App. A) | gitlab.cern.ch/faser/calypso (public) | | | | | Paper text VERIFIED(pdf). The adapted code is not located; it may sit in a branch or be upstreamed into the Athena commits above (INFERRED). Public: UNVERIFIED |
| Geant4 standard examples | github.com/Geant4/geant4 `examples/extended/exoticphysics` | | | | Geant4 licence | VERIFIED(api): contains channeling, dmparticle, monopole, phonon, saxs, ucn. **No quirk example.** `monopole` is the closest template. Latest tag v11.4.3 (v11.5.0.beta exists) |
| Knapen, Lou, Papucci, Setford EOM/plane-finder code (1708.02243) | none found | | | | | UNVERIFIED / not public. No availability statement in the PDF; GitHub and web searches gave nothing. Zenodo 17941765 says its data derive "partially" from this code, so it was shared privately (INFERRED) |
| Li, Pei et al. EOM solver (1911.02223, 2002.07503, 2404.13814) | none found | | | | | Not public (UNVERIFIED). 1911.02223 solves the quirk EOM by Euler's method with controlled truncation error (VERIFIED(pdf) l.240, 272). 2404.13814 wrote 4 quirk UFOs with FeynRules, not distributed (VERIFIED(pdf): "FeynRules ... four simple quirk models in UFO format"; no download link) |
| Sha et al. 2410.00269 dataset | https://zenodo.org/records/17941765 | 25 zip files, `mass_{100,500,1000,5000}_Lambda_{100..5000}_NoGap.zip` | YES: quirk and charged-particle hits + 4-vectors | none (toy, no PU; background = Pythia charged particles of the same event, no material) | CC-BY-4.0 | VERIFIED(api): 16.4 GB total, creator M. Fieg. Detector: toy 8-layer (r = 3.1–100 cm) or 25-layer; 13 TeV; pT > 100 MeV, abs(eta) < 2.5 (VERIFIED(pdf)) |
| Sha et al. GNN code | https://github.com/shaqiyu/QuirkTracking-ML | Exa.TrkX-style pipeline (embedding, filter, GNN), `Examples/QuirkTracking` | consumes hits | | **no licence** | VERIFIED(api): exists, created 2023-07-12. Link to the paper INFERRED from first author Q. Sha |
| Condren & Whiteson 2509.08878 code | https://github.com/LeviCondren/Tracking_pipeline | Same Exa.TrkX-style pipeline + `Examples/QuirkTracking/QuirkTracking.py` | consumes hits | mu = 1 in the paper | **no licence** | VERIFIED(api): exists, updated 2026-06-21. Link to the paper INFERRED from first author. The paper's own data: ttbar MG5+Pythia8, helices without material, mu = 1 (VERIFIED(pdf)) |
| LHCb 2601.09023 tooling | none found | "standalone code that generates hits according to the precise VELO geometry" | | | | Not public (UNVERIFIED). VERIFIED(pdf): toy VELO simulation, Pythia 8 background |
| burzynski-lab/quirk-tracking (ATLAS) | https://github.com/burzynski-lab/quirk-tracking | MaskFormer (hepattn fork) on GNN4ITk dumps converted to TrackML-schema parquet | yes (input data not public; on OU cluster) | low/no PU so far | no licence | VERIFIED(api): README + PLAN.md. See §0 item 2 |
| hepattn (MaskFormer tracking) | https://github.com/samvanstroud/hepattn | python / pixi | consumes hits | | GPL-3.0 | VERIFIED(api) |
| acorn (GNN4ITk / Exa.TrkX successor) | https://gitlab.cern.ch/gnn4itkteam/acorn | python | consumes hits | | licence file not found on `dev` (UNVERIFIED) | VERIFIED(api): public, active 2026-10-07 |
| Pythia 8 Hidden Valley, E_v pair production | https://pythia8.web.cern.ch/manuals/pythia8318/HiddenValleyProcesses.html | | | | GPL-2 (Pythia) | VERIFIED(doc): `HiddenValley:ffbar2EvEvbar` (code 4931, gamma*/Z* s-channel). E_v = 4900011 is the HV partner of the electron, with SM charges like a charged lepton. `HiddenValley:Ngauge` (SU(N) for N > 1) puts a factor Ngauge into fundamental-pair cross sections, which is exactly the N_IC factor. **The manual says nothing about quirks or macroscopic strings**; HV hadronisation is a microscopic Lund string ("would preclude studies with HV scales significantly below QCD"). Use: set `HiddenValley:fragment = off`, keep E_v stable, hand the E_v 4-vectors to an external propagator or Geant4. Online manual = 8.318; conda-forge = 8.312 |
| MadGraph5_aMC@NLO | conda-forge `mg5amcnlo` 3.5.7 (osx-arm64 + linux-64) | | | | UoI-NCSA (MG5) | VERIFIED(api) via `pixi search`. Built-in models are only `sm`, `loop_sm`, `MSSM_SLHA2`, `taudecay_UFO` (VERIFIED(api): GitHub `mg5amcnlo/mg5amcnlo/models`). **No public quirk / singlet-VLL UFO located** (web search). Options: (a) build a minimal UFO with one vector-like Dirac fermion of Q = -1, Y = -1, SU(2) singlet, couplings to gamma/Z only (FeynRules, or MG5's `usermod.py` add-particle API on `sm`), then multiply sigma by N_IC by hand; (b) ask the 2404.13814 / 1911.02223 / FASER authors for their UFO |
| HSCP-style custom particles in CMSSW | https://github.com/cms-sw/cmssw/tree/master/SimG4Core/CustomPhysics | C++ / python | | | Apache-2.0 | VERIFIED(api): `CustomPhysics`, `CustomParticleFactory`, `Exotica_HSCP_SIM_cfi.py` (particle file + `RHStopTracer` watcher), dark-photon, SIMP and SQ processes. `SimG4Core/PhysicsLists/src/MonopoleTransportation.cc` and `CMSMonopolePhysics.cc` exist: **a custom-transport template inside CMSSW**. `SimG4Core/Application/src/Phase2StackingAction.cc` exists. **No quirk code in CMSSW** (VERIFIED(api): GitHub code search for "quirk" in cms-sw/cmssw returned only unrelated files) |

### 1B. Public detector simulation and hit-level datasets (track P, backgrounds and overlay)

| Resource | URL | Format | Hits? | PU | Licence | Status |
|---|---|---|---|---|---|---|
| **ColliderML Release 1** | https://huggingface.co/datasets/CERN/ColliderML-Release-1 (paper arXiv:2512.15230, INSPIRE 3093591) | Parquet, one row per event, list columns; configs `<process>_<pu0/pu200>_<particles/tracker_hits/calo_hits/tracks>` | **YES**: `tracker_hits` x, y, z, true_x/y/z, time, particle_id, volume/layer/surface id. Particles carry `vertex_primary` (1 = hard scatter), so PU-only hits can be separated | **mu = 200 Poisson**, sub-events generated independently (pool ~200 M), plus finite beam spot (VERIFIED(pdf)) | CC-BY-4.0 | VERIFIED(api), HF API, last modified 2026-03-27, total repo ~28 TB. **pu200 configs:** ttbar, zee, zmumu, dihiggs, ggf. **pu0 configs:** ttbar, dihiggs, ggf, hidden_valley, higgs_portal, zprime, pileup_only. ttbar_pu200_tracker_hits: 100,000 rows, 708.6 GB; zee_pu200_tracker_hits: 100,000 rows, 700.5 GB; **pileup_only_pu0_tracker_hits: 7,327,493 rows, 359.9 GB**. Paper Table 1 also lists multijet, diphoton and susy channels that are **not** among the HF Release-1 configs (VERIFIED(api) config list). Generators: MG5 v3.5.8, Pythia 8.313. ODD solenoid 3 T. `pip install colliderml` (PyPI 0.4.2). **No Z(nunu)+jets / W+jets** |
| Open Data Detector (ODD) geometry | https://github.com/OpenDataDetector/OpenDataDetector (old gitlab.cern.ch/acts/OpenDataDetector: "Moved to GitHub") | DD4hep XML + material maps | via Geant4 (ddsim) or ACTS Fatras | user-made | MPL-2.0 | VERIFIED(api). ITk-inspired pixel + strip tracker (VERIFIED(pdf) 2512.15230) |
| ACTS | https://github.com/acts-project/acts | C++ / Python bindings, Fatras, Examples, ODD support | yes | user-made | MPL-2.0 | VERIFIED(api): latest v48.0.1 (2026-10-01). **conda-forge has only `acts-core` 45.5.1** (core library; the feedstock recipe builds `cmake -DACTS_USE_SYSTEM_LIBS=ON` with no Python/Examples/DD4hep flags, VERIFIED(api)). Fatras, Python bindings and the ODD plugin therefore need a source build or the Key4hep / LCG CVMFS stacks (Key4hep: UNVERIFIED) |
| TrackML challenge dataset | https://zenodo.org/records/4730167 (mirror of Kaggle trackml-particle-identification) | CSV per event: hits, cells, particles, truth + `detectors.csv` | YES | **mu = 200** ttbar (VERIFIED via the HAL paper summary in web search); ~1e5 hits per event | CC-BY-4.0 | VERIFIED(api): train_1..5.zip (15.9–16.0 GB each, 79.8 GB total) + detectors.csv. Event count of ~8.8k train events is UNVERIFIED. Detector: TrackML/"generic" ITk-like, 2 T, ACTS Fatras simulation (2018 vintage). No PU-only sample and no truth separation of PU vs HS beyond particle_id. Superseded by ColliderML for this purpose |
| TrackFormers datasets | https://zenodo.org/records/14386134 | tar.gz | yes (reduced TrackML, REDVID toy) | reduced | CC-BY-4.0 | VERIFIED(api), 8.2 GB. **Not useful** (reduced track multiplicity) |
| CMS Open Data with tracker hits (Run-1/2 geometry) | https://opendata.cern.ch/record/12220 ; https://opendata.cern.ch/record/12320 | 12220: custom ROOT ntuples (8 TeV QCD/tt, tracker hits), 12.8 TB, CC0. 12320: h5 pixel doublet seeds, TTbar 13 TeV **PU50**, 154 GB, GPL-3.0 | yes | 8 TeV / PU50 | CC0 / GPL-3.0 | VERIFIED(api). Old geometry; **useful only for a PU-50 cross-check of the Knapen random-plane rate in CMS-like pixel layers** (12320 has pixel seeds only) |
| CMS Open Data Phase-2 / Run4 samples | opendata.cern.ch | | | | | VERIFIED(api) **none**: queries "Phase2", "Phase2HLTTDR", "Run4", "HL-LHC", "trackml" return 0 records. Mainstream CMS OD (MiniAOD/NanoAOD) has no hits |
| ATLAS Open Data | opendata.cern.ch (e.g. records 80014–80018, DAOD_PHYSLITE 2024) | PHYSLITE | **no hits** | Run-2 | CC0 | VERIFIED(api), 12 PHYSLITE records. Not usable for hit-level work |
| Delphes HL-LHC cards | https://github.com/delphes/delphes/tree/master/cards/CMS_PhaseII | tcl | no hits (objects) | parametrised 200PU | GPL-3 | VERIFIED(api): `CMS_PhaseII_200PU_v04.tcl` (+ v02, v03, Substructure, 1000PU_MLWS), `delphes_card_HLLHC.tcl`, `delphes_card_ATLAS_PileUp.tcl`. Release 3.5.1; conda-forge `delphes` 3.5.1. **Use only for ISR-MET trigger / offline-MET acceptance and for background normalisation** |

### 1C. CMS-internal resources (track C, PRIMARY)

| Item | What is known | Status |
|---|---|---|
| Phase-2 official MC campaign naming | `/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_AllTP_140X_mcRun4_realistic_v4-v1/...` (geometry `ExtendedRun4D110`); `.../PU200_Trk1GeV_140X_mcRun4_realistic_v4-v2/...`; `/store/mc/Phase2Spring24DIGIRECOMiniAOD/DYJetsToMuMu_M-50_TuneCP5_14TeV-madgraphMLM-pythia8/ALCARECO/...noPU..._140X_mcRun4_realistic_v6_ext1-v2`; `/store/mc/Phase2Fall22DRMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2_ext1-v1`; older `Phase2HLTTDRWinter20DIGI-PU200_..._110X_mcRun4_realistic_v3` (DYToLL, muon guns) | VERIFIED(api): file paths in public CMSSW test configs (`DPGAnalysis/Phase2L1TNanoAOD/README.md`, `L1Trigger/Phase2L1GT/test/test_GT.py`, `L1Trigger/Phase2L1GMT/test/submitCrab.py`, `Alignment/OfflineValidation/.../defaultInputFiles_cff.py`). Phase2Spring23 (131X, D95) seen only in a user gist (UNVERIFIED). A later campaign (2025–26, e.g. "Phase2Spring25/26") was **not found** in CMSSW code (0 hits). **Whether ZJetsToNuNu, WJets, QCD-HT and MinBias exist in Phase2Spring24 at PU200 is UNVERIFIED. Run `dasgoclient -query="dataset=/*/Phase2Spring24*/GEN-SIM-DIGI-RAW-MINIAOD"` with a grid certificate** |
| Hit-level content of Phase-2 RAWSIM | `Configuration/EventContent/python/EventContent_cff.py`: `phase2_common.toModify(RAWSIMEventContent, ... 'keep *_sim*Digis_*_*', 'keep *Phase2TrackerDigi*_*_*_*')`, "until packer/unpackers are done". FEVT keeps `TTClustersFromPhase2TrackerDigis`, `TTStubsFromPhase2TrackerDigis` | VERIFIED(api). Official PU-200 GEN-SIM-DIGI-RAW samples therefore contain IT pixel digis (+ PixelDigiSimLinks) and OT digis. You re-run Phase-2 clusteriser and local reco to get RecHits. PSimHits are **not** in RAWSIM (FEVTDEBUG only), so signal truth must be produced privately with FEVTDEBUG(HLT) |
| Phase-2 geometries (now "Run4" in CMSSW) | `Configuration/Geometry/README.md`: D104, D110 (T35+C18+M14+I17+O9+F8), D111–D115, D120–D128. **D126 is labelled "Most up-to-date scenario"; D128 is labelled "Phase-2 baseline from CMSSW_20_1_0_pre4, for trigger studies"**. Tracker T35 = OT v8.0.0, IT v7.1.1 (3D sensors in TBPX L1). Workflow `Run4D110`: GT `auto:phase2_realistic_T35`, era `Phase2C17I13M9`. `Run4D128`: era `Phase2C26I13M9`. D88/D98 were used for 12_6 / 14_0 datasets (L1TrackNtupleMaker_cfg.py comment) | VERIFIED(api) (cms-sw/cmssw master). Recent releases: CMSSW_20_1_0_pre3 (2026-09-02), CMSSW_20_0_0_patch2, CMSSW_17_0_0_pre6, CMSSW_16_1_3 |
| Geant4 version in CMSSW | cmsdist `geant4.spec`: 11.4.1 (IB/CMSSW_17_0_X), **11.4.2 (IB/CMSSW_20_1_X)**, 11.2.2 (cmsdist default branch) | VERIFIED(api) |
| PU-200 mixing / premixing | `Configuration/StandardSequences/python/Mixing.py`: `AVE_200_BX_25ns` (Poisson, BX -3..3) and variants `_m12p3`, `_m6p6`; premix machinery `premix_stage1` / `premix_stage2` process modifiers, `SimGeneral/PreMixingModule`; Phase-2 `SimTrackerPREMIX` keeps `Phase2TrackerDigiedmDetSetVector_mix`, `Phase2OTDigiSimLink`, `simSiPixelDigis` | VERIFIED(api). **Official Phase-2 PU200 premix library dataset names are UNVERIFIED (DAS)** |
| L1 track trigger emulation | `L1Trigger/TrackTrigger` (stubs), `L1Trigger/TrackerDTC`, `L1Trigger/TrackFindingTracklet` (HYBRID, HYBRID_NEWKF, HYBRID_DISPLACED; `L1TrackNtupleMaker_cfg.py`), `L1Trigger/TrackFindingTMTT`, `L1Trigger/TrackerTFP`, `SimTracker/TrackTriggerAssociation` | VERIFIED(api). Use it to measure whether quirk hits form stubs (stub bend window) and L1 tracks, which is open in the feasibility review |
| Phase-2 offline / HLT tracking | `RecoTracker/LST` (Line Segment Tracking) present; `SimTracker/SiPhase2Digitizer`, `RecoLocalTracker/SiPhase2Clusterizer` | VERIFIED(api) |
| Cosmics / beam halo generators | `GeneratorInterface/CosmicMuonGenerator`, `GeneratorInterface/BeamHaloGenerator` | VERIFIED(api) |
| Injecting a quirk into CMSSW SimG4 | No existing code. Proposed route: port Athena `Quirks` (Apache-2.0, licence-compatible with CMSSW Apache-2.0) into a new `SimG4Core/CustomPhysics` physics constructor: (i) `CustomParticleFactory`-style G4ParticleDefinition for the PDG id (+/-), (ii) replace transport with `QuirkTransportation` (pattern: CMS `MonopoleTransportation`), (iii) partner pairing plus a stacking action alternating Q/Qbar (CMS uses its own `StackingAction` / `Phase2StackingAction`, which need a hook), (iv) a `g4SimHits.Watchers` entry in the style of `RHStopTracer` for truth. The generator gives Q/Qbar 4-vectors (Pythia8 HV E_v or MG5 LHE) with `ExternalGeneratorFilter`/Pythia8 hadronizer and E_v stable | Design INFERRED from VERIFIED(api) code. Effort: ESTIMATE 1–3 person-months for an experienced CMSSW/G4 developer. Main technical risk: multithreaded G4 (CMSSW runs G4 MT; the Athena code has `ATLAS_CHECK_THREAD_SAFETY` and is used in AthenaMT, so MT-safety is plausible: INFERRED) |
| ATLAS (for reference only) | Athena `Simulation/G4Extensions/{Quirks,Monopole,RHadrons,...}` public. ITk layouts and GNN4ITk dumps are ATLAS-internal | VERIFIED(api) for the code; layouts UNVERIFIED |

---

## 2. Recommended end-to-end chains

### Track C (PRIMARY, CMS-internal): full Phase-2 simulation
1. **Generation (GEN).**
   - Pythia8 in CMSSW (`Pythia8GeneratorFilter`), `HiddenValley:ffbar2EvEvbar = on`, `HiddenValley:Ngauge = 2`, `HiddenValley:fragment = off`, `4900011:m0 = m_Q`, E_v stable.
   - Alternative: MG5 LHE `p p > Q Q~ (+j)` with a home-made VLL UFO, sigma × N_IC by hand.
   - Bias ISR: generator-level filter on pT(QQbar) > ~150 GeV, matching the offline MET/ISR-trigger requirement (ε_trig ≈ 0.10 for pT > 200 GeV, 1708.02243).
   - Normalise to NLO DY: K = 1.33–1.45 (2404.13814).
2. **SIM.**
   - CMSSW_20_1_X (Geant4 11.4.2), geometry **ExtendedRun4D110** (matches Phase2Spring24 PU200 backgrounds, so overlays and digis are consistent) or D126/D128 if the newest campaign uses them (check DAS).
   - New `QuirkPhysics` constructor ported from Athena (§1C). Keep **FEVTDEBUG** for signal (PSimHits + SimTracks + digiSimLinks).
3. **DIGI + PU.**
   - `--pileup AVE_200_BX_25ns` with classic mixing for small validation samples.
   - Production: `--datamix PreMix` with the official Phase-2 PU200 premix library (`premix_stage2`).
   - Output: GEN-SIM-DIGI-RAW (tracker digis kept, §1C).
4. **L1 emulation.**
   - L1 TT stubs (`TTStubsFromPhase2TrackerDigis`) + tracklet emulation: check stub formation for quirk hits.
   - L1 MET / jets via Phase-2 GT for the ISR-MET seed (L1Trigger/Phase2L1GT).
5. **Local reco.** Phase-2 IT clusters + OT clusters → RecHits. Dump a flat hit ntuple per event in TrackML schema: x, y, z, layer, module, cluster charge/size, time if MTD, digiSimLink truth. Good templates: `L1TrackNtupleMaker` and `Validation/RecoTrack/plugins/TrackingNtuple.cc` (VERIFIED(api)), which already dumps hits with sim links.
6. **Pattern recognition.**
   - (a) Coplanar-plane finder à la 1708.02243 Sec. III C, run on hits left over after standard tracking (remove hits on good helices).
   - (b) GNN / MaskFormer (acorn or hepattn) trained on signal-over-PU200 digis.
   - (c) Quirk-trajectory chi2 fit + dE/dx (pixel ToT) + MTD time.
7. **Backgrounds.** Official Phase2Spring24 (or newer) PU200 GEN-SIM-DIGI-RAW-MINIAOD: TT (VERIFIED exists), plus Z(nunu)+jets, W(lnu)+jets, QCD-HT and MinBias (DAS check needed). Private production where missing (§3).

### Track P (public, fast prototyping, laptop/cluster)
1. **Generation.**
   - Pythia8 8.312 (conda-forge) HV `ffbar2EvEvbar`, Ngauge = 2, m_Q grid, plus ISR. Or MG5 3.5.7 (conda-forge) + home-made UFO + Pythia8 shower.
   - Output: HepMC3 or a direct numpy dump of the Q/Qbar 4-vectors and the SM final state.
2. **Quirk propagation, two options.**
   - **P-fast:** own numba EOM integrator: relativistic Nambu-Goto straight-string force (Lambda^2 along the string) + Lorentz force in a solenoid (3 T ODD, or 3.8 T for CMS-like) + Bethe-Bloch mean loss. Following 1708.02243 Sec. II and 2002.07503. Validate against Zenodo 17941765 trajectories (same (m, Lambda) points), the 0805.4642/1708.02243 amplitude formula, and a few Athena-Geant4 events. Intersect with ODD sensitive surfaces (layer radii/z from ODD XML or from ColliderML `volume_id/layer_id/surface_id` hit maps) → quirk hits with ODD-like smearing.
   - **P-full:** port the Athena `Quirks` extension into a standalone Geant4 11.4 app (conda-forge `geant4` 11.4.3 + `dd4hep` 1.38) loading the ODD DD4hep geometry (ddsim-style). This gives realistic material effects and delta rays. It needs the ODD repo and a C++ build. ESTIMATE: 2–4 weeks.
3. **Background hits.**
   - **ColliderML** `pileup_only_pu0_tracker_hits` (7.33 M minbias sub-events): build PU-mu crossings at mu = 50, 100, 140, 200 by Poisson sampling (with z/t beam-spot smearing as in 2512.15230).
   - For physics backgrounds with jets: `ttbar_pu200`, `zee/zmumu_pu200` (hard-scatter hits are identifiable via `vertex_primary`).
   - Z(nunu)+jets / W+jets hard scatters are **not** in ColliderML. Simulate them with ODD (ACTS Fatras or ddsim) and overlay pileup_only hits.
4. **Overlay.** Merge quirk hits (+ their event's ISR/UE hits) with PU hits per surface. Caveat: no digitisation-level merging of overlapping clusters. ESTIMATE: second-order at quirk-hit level.
5. **Reconstruction.**
   - Plane finder (1708.02243 algorithm, numba).
   - GNN via acorn (Exa.TrkX) or the QuirkTracking-ML configs (no licence, so contact authors before reuse). MaskFormer via hepattn (GPL-3.0).
   - Signal truth: hits with `particle_id` of Q/Qbar.
6. **Trigger / MET acceptance.** Delphes `CMS_PhaseII_200PU_v04.tcl` on generator output, for ISR-MET efficiency and background normalisation only.
7. **Cross-check.** Reproduce Knapen's mu = 50 numbers (10^-3 for a 4/8-layer plane, 6e-5 for all layers) in ODD with mu = 50 overlays before going to 200. This is the data-quality closure test for JFC Phase 2.

---

## 3. Samples required for JFC Phase 2 (Exploration)

### 3.0 Why these event counts (background logic)

**Trigger stream size.**
- The offline stream is ISR-MET (MET or pT(QQbar) > 200 GeV).
- Z(nunu)+jets with MET > 200 GeV at 14 TeV: ESTIMATE ~0.5–1 pb, i.e. 1.5–3 × 10^6 events in 3 ab^-1.
- W(lnu)+jets (lost lepton) and ttbar: comparable order.
- So N_stream ~ 10^7 events (ESTIMATE).
- "Background-free" (< 0.3 expected events) requires a per-event fake probability **f_tot ≲ 3 × 10^-8** after all cuts.

**Known rates.**
- Random-plane rates at mu = 50: 1e-3 (plane in 4/8 layers) and 6e-5 (all layers), per event, **before** the Delta s < 100 µm and dE/dx cuts [1708.02243 Sec. IV].
- Surviving Z(nunu)+jets + PU-50: ~1e-2 fb [1911.02223], i.e. ε ~ 1e-5 relative to ~1 pb. That is ~30 events at 3 ab^-1.
- At mu = 200 the random-plane rate grows like (occupancy)^k for k-layer coincidences: a factor 4^2–4^4 = 16–256 (ESTIMATE, UNVERIFIED). Expect ~1e-3 to 1e-2 for the all-layer plane.

**Strategy, since f_tot ~ 3e-8 cannot be sampled directly.**
- Factorise: f_tot = f_plane(mu) × f_Delta-s × f_dE/dx × f_MET-plane-alignment × f_timing.
- Measure each factor on ≥ 10^5-event samples, with ≥ 100 surviving candidates per factor, then extrapolate tails by fitting.
- Measure the mu dependence at 50 / 100 / 140 / 200 and fit a power law.
- Requirement: to see ≥ 100 plane-finder fakes at f_plane = 1e-3 (mu = 200) needs ≥ 1e5 PU-200 crossings; at mu = 50 (f = 6e-5) ≥ 1.7e6 crossings (fine for the cheap PU-only overlay).
- To reproduce the 1e-2 fb Z(nunu) number (ε ~ 1e-5) with ~10 events needs ~1e6 Z(nunu)+jets MET > 200 events with PU overlay. A **1e5** version is enough for Phase 2 if factorisation is used. The 1e6 version is for Phase 3+.

### 3.1 Track C sample list (Phase 2 Exploration)

| ID | Sample | Generator / setting | Events (Phase 2) | Hit-level content | Obtain now? | CPU / storage (ESTIMATE) |
|---|---|---|---|---|---|---|
| C-S1 | Quirk DY signal grid: m_Q = 200, 400, 600, 800, 1000 GeV × Lambda = 0.3, 1, 3, 10, 30 keV (25 points), N_IC = 2, (1,1,-1) | Pythia8 HV E_v (or MG5+UFO), gen filter pT(QQ) > 150 GeV, Phase-2 SIM with ported quirk G4, D110, PU200 premix; FEVTDEBUG | 4k/point = 1e5 (+ 5 points × 5k at PU0 for truth studies) | PSimHits + digis + digiSimLinks | **Must be produced.** Blocked by the G4 port | ~250 s/evt full chain at PU200 → ~7,000 core-h; ~15–25 MB/evt FEVTDEBUG → ~2 TB |
| C-B1 | MinBias / pure PU-200 crossings (premix library or `Neutrino_E-10_gun` + PU200) | official premix library or private Neutrino-gun + `AVE_200_BX_25ns` | 1e5 crossings (mu = 200) + 5e4 each at mu = 50, 140 (private `AVE_50/140`) | digis (RAWSIM keeps them) | Library: UNVERIFIED name (DAS). Private neutrino-gun: producible now | ~60–100 s/evt DIGI+RECO → ~3,000–5,000 core-h; ~5–8 MB/evt → ~1.5 TB |
| C-B2 | ttbar PU200 | `/TT_TuneCP5_14TeV-powheg-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_*_140X_mcRun4_realistic_v4*/GEN-SIM-DIGI-RAW-MINIAOD` | 1e5 (subset) | digis | **Yes (VERIFIED path exists)** | read-only; ~1 TB if staged |
| C-B3 | Z(nunu)+jets, HT- or pT(Z)-binned, ≥ 200 GeV | official if it exists (DAS), else private MG5 `ZJetsToNuNu_HT-*` gridpacks (CMS genproductions) + PU200 premix | 1e5 (Phase 2); 1e6 later | digis | DAS check; likely private | ~250 s/evt → ~7,000 core-h; ~1.5 TB |
| C-B4 | W(lnu)+jets, HT ≥ 200 | as C-B3 | 1e5 | digis | DAS check | as C-B3 |
| C-B5 | QCD multijet (HT-binned, MET-tail enriched) | official Phase-2 QCD (plots labelled "QCD (200 PU)" exist publicly; names UNVERIFIED) | 5e4 | digis | DAS check | read-only or ~4,000 core-h |
| C-B6 | Photon conversions / nuclear interactions | inside C-B1/B2 (Geant4 secondaries; TrackingParticles + SimVertex process type) | n/a | yes | with C-B1 | — |
| C-B7 | Cosmics / beam halo | `CosmicMuonGenerator`, `BeamHaloGenerator` (VERIFIED packages), plus data-driven later (Run-3 cosmic runs, non-colliding BX) | 1e4 each | digis | producible now | small |
| C-V1 | Validation: single-quirk-pair particle gun at fixed (pT, eta) in D110, no PU; compare against the standalone P-fast EOM | private | 1e4 | PSimHits | after the G4 port | small |

Total ESTIMATE for Phase 2 track C: ~25–30 k core-h, ~6–8 TB (T2/T3 disk). This is feasible within a CMS group allocation. The critical path is the G4 port (C-S1), not CPU.

### 3.2 Track P sample list (prototype; can mostly start NOW)

| ID | Sample | Source | Events | Obtain now? | CPU / storage (ESTIMATE) |
|---|---|---|---|---|---|
| P-S0 | Sha et al. toy-detector quirk hits | Zenodo 17941765 | 25 points (as provided) | **Yes** (16.4 GB) | download only |
| P-S1 | Quirk DY grid (same 25 points as C-S1) + ISR; Pythia8 HV; P-fast EOM through ODD surfaces | private | 2e4/point = 5e5 | Yes (code to write: ~1–2 weeks) | ms/evt for EOM; Pythia ~10 ms/evt → < 50 core-h; ~1 kB/evt quirk hits |
| P-B1 | PU-only hit pool | ColliderML `pileup_only_pu0_tracker_hits` (+ `_particles` for vertex/time) | 7.33 M sub-events → 3.6e4 independent mu = 200 crossings (more with resampling) | **Yes** | 360 GB (+359 GB particles); subset 1M sub-events ≈ 50 GB |
| P-B2 | ttbar PU200 with hits | ColliderML `ttbar_pu200_tracker_hits` | 1e5 available; use 2e4 | **Yes** | 7.1 MB/evt → 140 GB for 2e4 |
| P-B3 | Z(ll) PU200 (proxy for EW+jets recoil topology) | ColliderML `zee/zmumu_pu200` | 2e4 | **Yes** | ~140 GB |
| P-B4 | Z(nunu)+jets, W(lnu)+jets hard scatters, MET > 200 | MG5 (+0,1,2j, MLM) + Pythia8 → ODD sim (ACTS Fatras fast, or ddsim/Geant4), hard-scatter only; overlay P-B1 | 1e5 each | Must be produced | Fatras ~0.1–1 s/evt, Geant4 ~5–20 s/evt → 30–1,000 core-h; ~1 MB/evt |
| P-B5 | Conversions / nuclear interactions | contained in P-B1 (Geant4 secondaries in ColliderML particles) | — | Yes | — |
| P-T1 | TrackML (old, mu = 200) | Zenodo 4730167 | 1 zip (~1.8k evts) | Yes (16 GB) | cross-check only |
| P-T2 | CMS OD 12320 pixel seeds TTbar PU50 | CERN OD | subset | Yes (154 GB) | optional PU-50 CMS-pixel cross-check |

### 3.3 Mapping to the JFC Phase 2 tasks
- **Schema inventory:**
  - ColliderML parquet schema (verified field list in §1B).
  - Zenodo 17941765 zip contents (to inspect after download).
  - CMS RAWSIM digi collections (§1C).
  - Write one common "hit table" schema: event, hit_id, x, y, z, r, phi, layer_key, charge/ToT, time, truth_pid, truth_is_quirk, truth_vertex_is_HS.
- **Data quality:**
  - Hit multiplicities per layer vs mu.
  - Closure of the mu = 50 Knapen numbers.
  - Quirk-hit continuity / EOM validation against Zenodo trajectories and Athena-G4.
- **Variable survey, S vs B:**
  - Plane residual Delta s, N_layers on plane, plane-normal vs MET azimuth, cluster charge (dE/dx ~2× MIP for the pair).
  - Hit-time / MTD delay (beta < 1), opening angle, number of hits per layer (multiple crossings).
  - Fraction of plane hits already on standard helical tracks.
- **Baseline yields:**
  - sigma × ε_trig × ε_fid from P-S1 + Delphes.
  - Background f_plane(mu) from P-B1/P-B4.
  - Track C later replaces both.

---

## 4. Proposed pixi environment (track P)

All availability was checked with `pixi search -c conda-forge` (pixi 0.72.0) on osx-arm64; linux-64 was checked for the heavy ones. Nothing was installed.

```toml
# pixi.toml (proposal; not created)
[workspace]
name = "c001-quirks"
channels = ["conda-forge"]
platforms = ["osx-arm64", "linux-64"]

[dependencies]
python = "3.12.*"          # safer than 3.14 for torch/pyg wheels (ESTIMATE)
pythia8 = ">=8.312"        # VERIFIED 8.312 (osx-arm64, linux-64)
mg5amcnlo = ">=3.5.7"      # VERIFIED 3.5.7 (osx-arm64, linux-64)
lhapdf = ">=6.5.6"         # VERIFIED
hepmc3 = ">=3.3.1"         # VERIFIED
fastjet = ">=3.5.2"        # VERIFIED
delphes = ">=3.5.1"        # VERIFIED
geant4 = ">=11.4.3"        # VERIFIED (osx-arm64, linux-64) — for P-full only
dd4hep = ">=1.38"          # VERIFIED (osx-arm64, linux-64) — for ODD + Geant4
root = ">=6.40"            # VERIFIED 6.40.04 (osx-arm64, linux-64)
uproot = ">=5.7"           # VERIFIED 5.7.7
awkward = ">=2.14"         # VERIFIED 2.14.0
vector = "*"               # VERIFIED 1.9.0
numba = "*"                # VERIFIED 0.68.0
polars = "*"               # VERIFIED 2.0.0
pyarrow = "*"              # VERIFIED 25.0.0
datasets = "*"             # VERIFIED 5.0.1 (HF streaming of ColliderML)
hist = "*"                 # VERIFIED 2.12.0
mplhep = "*"               # VERIFIED 1.3.3
scikit-learn = "*"         # VERIFIED 1.9.1
pyhf = "*"                 # VERIFIED 0.7.6
pytorch = "*"              # VERIFIED 2.13.0
pytorch_geometric = "*"    # VERIFIED 2.8.0.post1 (also 'torch-geometric' 2.6.1)
acts-core = ">=45.5.1"     # VERIFIED, but core library only (no Python/Fatras/ODD)

[pypi-dependencies]
colliderml = ">=0.4.2"     # VERIFIED on PyPI (OpenDataDetector/ColliderML, MIT repo)
```

Not on conda-forge (VERIFIED absent):
- ACTS Python bindings / Fatras / Examples (only `acts-core`).
- `edm4hep`, `podio`, `key4hep`.
- ODD (git clone from GitHub).
- `trackml` (the PyPI `trackml` 0.1.12 is an unrelated cookiecutter, VERIFIED. The TrackML helper library is github.com/LAL/trackml-library: VERIFIED(api), updated 2026-09-28, no licence metadata).
- hepattn (pixi project from GitHub).
- acorn (CERN GitLab).

For ACTS + ODD + Fatras use a separate environment: source build, or the Key4hep stack on CVMFS (UNVERIFIED).

Track C environment: CMSSW_20_1_X (or the campaign release, e.g. 14_0_X for Phase2Spring24) on lxplus/CMSConnect or a T2/T3 with CVMFS; `dasgoclient`, CRAB. Ecuador: check access to a T2/T3 via CMS (UNVERIFIED).

---

## 5. Risks and blockers

1. **Competition / scooping (HIGH).** An ATLAS quirk search effort (burzynski-lab/quirk-tracking, Athena quirk G4 fixes Aug–Sep 2026, a GNN line in acorn forks) is active. It appears to use ITk-like dumps but no PU yet. CMS Phase-2 at PU 200 with L1/HLT feasibility is the differentiator; move quickly.
2. **No quirk transport in CMSSW (blocker for track C signal).** The Athena code must be ported and validated: G4 MT-safety, CMS stacking-action integration, PDG id table, FEVTDEBUG truth, CMS 3.8 T field map. Mitigation: start with P-fast EOM hits injected as fake PSimHits, or as a particle gun with string force in a validation geometry. ESTIMATE: 1–3 person-months.
3. **No public quirk UFO / EOM code.** Mitigation: Pythia8 HV `ffbar2EvEvbar` + Ngauge (VERIFIED) covers DY at LO with shower ISR. NLO K-factors come from 2404.13814. Write own EOM (straight-string, 1708.02243 / 2002.07503).
4. **Background tail extrapolation.** f_tot ~ 3e-8 cannot be simulated directly. The method rests on factorisation and fitted tails, and needs a data-driven strategy (Delta s sidebands, MET-plane misalignment control region). PU-200 random-plane rates have never been computed (UNVERIFIED in any source).
5. **Public geometry ≠ CMS.** ODD is ITk-like: a 3 T ColliderML field vs 3.8 T in CMS, and different layer radii and material. Track P numbers are prototypes only. Conversions and nuclear-interaction rates depend on material.
6. **Hit-level overlay realism.** Merging hits at the space-point level ignores cluster merging, readout inefficiency and out-of-time PU (ColliderML has hit times). CMS premixing at digi level solves this for track C.
7. **CMS sample availability (UNVERIFIED).**
   - Z(nunu)+jets / W+jets / QCD / MinBias at PU200 in the latest Phase-2 campaign must be checked in DAS.
   - Phase-2 MC campaigns may have moved to a newer naming (no 2025/26 campaign name found in CMSSW code).
   - Large private Phase-2 production needs a PdmV/EXO request or group CPU.
8. **Storage.** ColliderML pu200 hits are ~7 MB/evt (709 GB per 100k). Download subsets only, via streaming or `colliderml download --max-events`. Laptop disk is a constraint; use a cluster.
9. **Licences.** QuirkTracking-ML, Tracking_pipeline and quirk-tracking have **no licence**, so code reuse needs author permission (cite and contact). Athena (Apache-2.0), ACTS/ODD (MPL-2.0), hepattn (GPL-3.0) and datasets (CC-BY-4.0) are fine.
10. **Trigger.** ISR-MET thresholds at Phase-2 L1 (PU-robust track-MET) set the signal ε. Delphes gives only a rough number; the CMS L1 emulation (Phase2L1GT) is needed. Whether quirk hits form L1 stubs is untested (open question, testable with `L1TrackNtupleMaker`).
11. **Python 3.14 on the laptop.** torch/pyg wheels may lag; pin python 3.12 in pixi (ESTIMATE).

---

## Appendix: verification log (queries run, 2026-10-07)
- GitLab API:
  - `projects/atlas%2Fathena/repository/tree?path=Simulation/G4Extensions/Quirks&recursive=true`
  - raw files `QuirksConfig.py`, `QuirkPhysicsTool.cxx`, `Quirk.cxx`, `standalone/{setup.sh,GNUmakefile,test.cc,share/*.txt}`, LICENSE
  - commits `?path=Simulation/G4Extensions/Quirks`
  - `Simulation/G4Extensions` listing
  - `projects/faser%2Fcalypso` (+ tree `Simulation/G4Extensions`)
  - `projects/acts%2FOpenDataDetector`
  - `projects?search=acorn`, `projects/gnn4itkteam%2Facorn`
- GitHub (gh):
  - `search repos` quirk*
  - `search code QuirkTracking`
  - repos burzynski-lab/quirk-tracking (README, PLAN.md, prep_quirks.py), shaqiyu/QuirkTracking-ML, LeviCondren/Tracking_pipeline, samvanstroud/hepattn, acts-project/acts (release v48.0.1, LICENSE MPL-2.0), OpenDataDetector/OpenDataDetector, OpenDataDetector/ColliderML, delphes/delphes cards, Geant4/geant4 exoticphysics + tags, mg5amcnlo/mg5amcnlo models, conda-forge/acts-feedstock recipe
  - cms-sw/cmssw: SimG4Core/CustomPhysics, PhysicsLists, Application; Configuration/Geometry/README.md; PyReleaseValidation upgradeWorkflowComponents.py; StandardSequences/Mixing.py; EventContent_cff.py; SimTracker_EventContent_cff.py; L1Trigger/*; GeneratorInterface/{CosmicMuonGenerator,BeamHaloGenerator}; RecoTracker/LST; code search for Phase2Spring24/Fall22/Spring23/Spring25/Fall24/Spring26 and "quirk"
  - cms-sw/cmsdist geant4.spec on IB/CMSSW_17_0_X, IB/CMSSW_20_1_X
- Zenodo API: records 17941765, 4730167, 14386134; searches "quirk tracks", "TrackML", "ColliderML", "Open Data Detector".
- HuggingFace API: `api/datasets/CERN/ColliderML-Release-1` (+ treesize per config, README), datasets-server `/size`.
- CERN Open Data API: searches "TrackML", "Open Data Detector", "Phase-2", "Phase2", "Run4", "HL-LHC", "ColliderML", "pileup 200", "tracking machine learning", ATLAS PHYSLITE; records 12220, 12320.
- PyPI JSON: colliderml, trackml, hepattn, acts-python.
- `pixi search -c conda-forge`: pythia8, geant4, acts*, dd4hep, root, uproot, awkward, pytorch_geometric, torch-geometric, pytorch, hepmc3, lhapdf, fastjet, delphes, madgraph, madgraph5, mg5amcnlo, polars, pyarrow, datasets, numba, vector, hist, mplhep, scikit-learn, pyhf, *edm4hep*, *podio*, *opendatadetector*, *trackml*, *key4hep*; linux-64 for pythia8, geant4, mg5amcnlo, dd4hep, root.
- Pythia online manual 8.318 HiddenValleyProcesses (WebFetch).
- PDFs (cache): 1708.02243, 1911.02223, 2404.13814, 2607.26195 (App. A, ref. [27]), 2410.00269, 2509.08878, 2601.09023, 2512.15230.
- Web searches: Knapen quirk code (none), ColliderML (found), TrackML (Zenodo mirror), Phase2Spring24 (release notes + CMS plots only), singlet VLL UFO (none).
