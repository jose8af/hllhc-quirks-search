# C001 Phase 2 (Exploration): sample requirements

Status: v3 — Phase-1 PASS (round 2), 2026-10-07; changes listed in STRAT §20. Companion to `phase1_strategy/outputs/STRATEGY_DRAFT.md` (referred to as STRAT). Source keys are the same as STRAT §2.3: TH, EX, ST, LM, RV-*.

Tags:
- `ESTIMATE`: own calculation, inputs stated.
- `UNVERIFIED`: not checked.
- `VERIFIED(api)`: read from a live public repository or API on 2026-10-07.

All DAS dataset-name patterns below are **UNVERIFIED** guesses at naming conventions. The user must run them with a grid certificate.

---

## 0. What JFC Phase 2 needs before it counts as complete

Phase 2 deliverable: `EXPLORATION.md` [jfc templates/phase2_claude.md; methodology 02-phases.md]. Prototype on ~1000-event slices first.

| Phase-2 item | What it means for C001 | S1 (Phase-2 MC) | S2 (Run-3 data + MC) | S3 (staged) |
|---|---|---|---|---|
| Schema inventory | Hit-level tables for every file: positions, layer/module, charge/ToT, time/BX, truth links; event-level MET, jets, nPV | Phase-2 RAWSIM digis + private FEVTDEBUG signal; common "hit table" schema [ST §3.3] | Run-3 RAW-RECO skim / cluster skim, ZeroBias RAW; Run-3 signal FEVTDEBUG | public prototype first, then both |
| Data archaeology / quality | Count vs σ×L (skim pre-selection), NaN/empty branches, hit multiplicity per layer vs μ/nPV, quirk-hit continuity | MC only: occupancy vs μ = 50/140/200 | data: occupancy vs nPV, noisy modules, skim selection efficiency | both |
| **Closure test** (binding; re-planned after review B7) | Primary: reproduce Knapen's **10⁻³** μ = 50 rate (≥ 1 hit in 4/8 layers) [1708.02243 Sec. IV] with **≥ 10⁵ independent crossings** (≥ 100 fakes, ±10%). Secondary: the 6×10⁻⁵ all-layer rate via (i) the factorised estimate f(4/8) × P(rest \| 4/8) and (ii) resampled crossings with a documented overlap test (STRAT §13). Use a Knapen-matched 8-layer subset of the geometry; state the geometry-transfer tolerance beforehand | public: full ColliderML pool (1.47×10⁵ μ = 50 crossings); CMS: 10⁵ μ = 50 crossings (S1-PU) | Run-3 zero-bias at matching nPV (≥ 10⁵ events at low nPV, from S2-ZB) | yes |
| Variable survey S vs B | O1-O10 of STRAT §5 ranked by AUC or S/√B per (m_Q, Λ) regime | signal PU 200 vs PU-only + Z(νν) | signal Run-3 vs data sidebands (blinded SR) | both |
| Baseline yields | σ × ε after preselection (trigger proxy + MET + plane ≥ N layers) for signal and each background | MC | MC + data CRs | both |
| OI-1 timing study | per-layer SimHit toa = tof − \|r\|/c distributions; efficiency with default vs widened digitizer windows | yes | Phase-1 readout version | yes |
| Strategy-revision flags | e.g. "Phase 1 assumed P1 ε ≈ 0.1; Phase 2 found X" | — | — | — |

---

## 1. Public prototype samples (start immediately; no CMS credentials)

| ID | Sample | Source | Events to use | Purpose in Phase 2 | Size / CPU (ESTIMATE) | Availability |
|---|---|---|---|---|---|---|
| P-S0 | 2410.00269 quirk + charged-particle hits; toy 8/25-layer detector, no PU, 25 (m, Λ) points | Zenodo 17941765, CC-BY-4.0 [ST §1A] | all | V5 validation of our propagator; GNN baseline; signal schema | 16.4 GB download | **exists-public** VERIFIED(api) |
| P-S1 | Own quirk DY grid: Pythia8 HV `ffbar2EvEvbar`, Ngauge = 2, E_v stable, fragment off, pT(QQ̄) > 150 GeV; fast numba propagator through (a) a CMS-like parametric geometry at 3.8 T (radii from Tracker TDR Tab. 9.1/10.1 via EX §3.1) and (b) ODD surfaces at 3 T | private [ST §3.2] | 15-point subset (STRAT §7, D7) × 2×10⁴ | regime maps (ℓ_max, N_cross, thickness, toa per layer); trigger proxy vs pT(QQ̄) threshold (replaces STRAT A4) | < 50 core-h; ~1 kB/evt [ST §3.2] | must-produce (code: W3, 1-2 weeks) |
| P-B1 | PU-only hit pool | ColliderML R1 `pileup_only_pu0_tracker_hits` (7.33 M sub-events, 359.9 GB) + `_particles` [ST §1B] | **full pool, 7.33 M sub-events** → 1.47×10⁵ independent μ = 50 crossings (≥ 100 fakes at 10⁻³) and 3.7×10⁴ at μ = 200 (≈ 37+ fakes at f ≥ 10⁻³); μ = 100/140 from the same pool; resampling (≤ 12× reuse) only for the all-layer secondary target | closure at μ = 50; random-plane rate vs μ | 360 GB hits (+ 359 GB particles, optional) | **exists-public** VERIFIED(api) |
| P-B2 | tt̄ PU 200 with hits | ColliderML `ttbar_pu200_tracker_hits` | 2×10⁴ (of 10⁵) | busy hard-scatter + PU reference | ≈ 140 GB (7.1 MB/evt) | exists-public |
| P-B3 | Z(ℓℓ) PU 200 | ColliderML `zee/zmumu_pu200` | 2×10⁴ | EW recoil proxy; B6 tag-and-probe prototype | ≈ 140 GB | exists-public |
| P-B4 | Z(νν)+jets, W(ℓν)+jets hard scatter, MET > 200 GeV | MG5 0-2j MLM + Pythia8 → ODD (Fatras or ddsim) + P-B1 overlay | 10⁵ each | B2 prototype | Fatras 0.1-1 s/evt, Geant4 5-20 s/evt → 30-1000 core-h; ~1 MB/evt [ST §3.2] | must-produce |
| P-T1 | TrackML μ = 200 (2 T) | Zenodo 4730167 | 1 zip | cross-check only | 16 GB | exists-public |
| P-T2 | CMS Open Data 12320 pixel seeds, tt̄ PU 50 | CERN OD | subset | PU-50 check in CMS-like pixels | 154 GB total | exists-public |

[L2] ODD ≠ CMS (3 T, ITk-like layout, different material) [ST §5 item 5]. Public numbers are **prototype-only**.

---

## 2. Scope S1: CMS Phase-2 (PU 200) samples for Phase 2

Assumptions:
- CPU of 250 s/event for the full GEN-SIM-DIGI-RECO chain at PU 200 [ST §3.1].
- 15-25 MB/event FEVTDEBUG [ST §3.1].
- **[A7] Quirk Geant4 CPU per event is unknown.** Up to ~3×10⁴ string crossings occur inside the tracker at Λ = 30 keV [TH Tab. 4.2a]. Small steps could make SIM ≫ 250 s/event. W1 must measure it before mass production.

| ID | Name / process | Generator & settings | PU | Tier that keeps hits | # events (justification) | CPU / storage (ESTIMATE) | Availability |
|---|---|---|---|---|---|---|---|
| S1-SIG | Quirk E, 15-point subset: m_Q ∈ {200, 500, 1000} GeV × Λ ∈ {0.3, 0.6, 2, 10, 30} keV | Pythia8 HV (W2), gen filter pT(QQ̄) > 150 GeV; quirk G4 (W1); ExtendedRun4D110 (or the DAS campaign geometry); premix PU 200; **digitizer run twice**: default windows and widened/sampled (OI-1) | 200 | FEVTDEBUG(HLT) for PSimHits + digis + digiSimLinks [ST §1C] | 5k/point = 7.5×10⁴. TH §7 minimum; ε ≈ 0.07 after the filter gives ~350 selected per point (~5% statistics) | 5.2k core-h (+ unknown G4 overhead, A7); 1.1-1.9 TB | **must-produce**; blocked by W1, W2 |
| S1-SIG0 | Same 15 points, no PU (truth, toa, stub studies) | as above | 0 | FEVTDEBUG | 1k/point = 1.5×10⁴ | ~0.2-0.5k core-h; ~0.1 TB | must-produce |
| S1-VAL | Validation: (i) Λ = 0.05 keV at 500 GeV; (ii) Λ = 1 keV, B = 0; (iii) causal vs straight string; (iv) quirk-pair gun at fixed (pT, η) [TH §7; ST C-V1] | private | 0 | FEVTDEBUG | 5k each = 2×10⁴ | small | must-produce |
| S1-PU | PU-only crossings: Neutrino_E-10 gun + `AVE_200_BX_25ns`, plus `AVE_50`, `AVE_140` | private, or the official premix library | 200 / 50 / 140 | GEN-SIM-DIGI-RAW (RAWSIM keeps `Phase2TrackerDigi`, `sim*Digis` [ST §1C]) | 10⁵ at μ = 200: ≥ 100 fakes at f_plane = 10⁻³ [ST §3.0]. **10⁵ at μ = 50** (CMS closure: ≥ 100 fakes at 10⁻³; v1 had 5×10⁴, underpowered). 5×10⁴ at μ = 140 (μ-scan for the power-law fit) | 4.2-6.9k core-h (2.5×10⁵ events × 60-100 s [ST §3.1]); 1.25-2 TB (5-8 MB/evt) | premix library: exists-CMS-check-DAS; private: producible now |
| S1-TT | tt̄ PU 200 | `/TT_TuneCP5_14TeV-powheg-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_*_140X_mcRun4_realistic_v4*/GEN-SIM-DIGI-RAW-MINIAOD` [ST §1C] | 200 | GEN-SIM-DIGI-RAW-MINIAOD (digis) | 10⁵ subset (busy-event reference) | read-only; ~1 TB if staged | **exists-CMS** (path VERIFIED(api) in CMSSW test configs); check the replica site in DAS |
| S1-ZNN | Z(νν)+jets, HT- or pT(Z)-binned, ≥ 200 GeV | official if it exists, else CMS genproductions MG5 gridpacks + premix | 200 | GEN-SIM-DIGI-RAW | 10⁵ (Phase 2), which suffices with factorisation (STRAT D10). σ(Z→νν, pT > 200 GeV) = 3.00 pb measured at 13 TeV [2012.09254], ≈ 3.4 pb at 14 TeV (STRAT §8.3). The μ = 50 B2 rate of 10⁻² fb [1911.02223] is then a per-event ε ≈ 3×10⁻⁶, so seeing ~10 events directly would need ~3×10⁶ events. Direct sampling is impractical; factorisation is mandatory. The Phase-3 size is set by the factorised-method needs, not by direct sampling | ~7k core-h; 1.5-2.5 TB (15-25 MB/evt) | exists-CMS-check-DAS, likely must-produce |
| S1-WJ | W(ℓν)+jets, HT ≥ 200 GeV | as S1-ZNN | 200 | as above | 10⁵ | ~7k core-h; ~1.5 TB | exists-CMS-check-DAS |
| S1-QCD | QCD multijet, HT-binned, MET-tail enriched | official Phase-2 QCD if present | 200 | as above | 5×10⁴ | read-only, or ~4k core-h | exists-CMS-check-DAS |
| S1-DY | DY(µµ)+jets (M7 invisible-Z CR; B6 tag-and-probe) | official `DYJetsToMuMu_M-50_TuneCP5_14TeV-madgraphMLM-pythia8` (noPU ALCARECO seen [ST §1C]); a PU-200 version must be checked | 200 | digis | 5×10⁴ | read-only or ~3.5k core-h | exists-CMS-check-DAS |
| S1-NC | Cosmics, beam halo | `CosmicMuonGenerator`, `BeamHaloGenerator` [ST §1C] | 0 | digis | 10⁴ each | small | producible now |

**Total for S1 Phase 2** (ESTIMATE, excluding the A7 overhead):
- CPU ≈ 24-34k core-h. Lower end: QCD and DY official. Upper end: all unknown samples produced privately.
  - Rows summed: S1-SIG 5.2k; S1-SIG0 0.2-0.5k; S1-VAL ~0.3k; S1-PU 4.2-6.9k; S1-ZNN 6.9k; S1-WJ 6.9k; S1-QCD 0-4k; S1-DY 0-3.5k.
- Storage ≈ 8-12.5 TB (official samples counted as staged; 15-25 MB/evt for private PU-200 samples).
- These totals replace v1's "25-30k core-h, 7-8 TB". The same numbers are used in STRAT §6.2 and OQ Q3.
- **MTD times for backgrounds (review C5):**
  - the Phase-2 RAWSIM modifier keeps only tracker `sim*Digis`/`Phase2TrackerDigi` (`EventContent_cff.py`), and MTD reco is in RECOSIM/AODSIM/FEVT;
  - so O5 (MTD β) on official backgrounds needs the GEN-SIM-DIGI-RAW-**MINIAOD** or AODSIM tier, or a private re-reco;
  - check this in DAS (§5 block 1).

**Later (Phase 3+)**, full target grid:
- 48 points × 10k + **18** edge points × 10k extra = 6.6×10⁵ events: ≈ 46k core-h, 9.9-16.5 TB (ESTIMATE, 250 s and 15-25 MB per event).
  - The edge set is Λ = 0.3 and 30 keV at all 6 masses (12) plus the 6 inner-Λ points at 1250 GeV.
  - TH said "8"; the review said 16; the stated edge set gives 18 (STRAT §20, C3).
- Ẽ (9 × 10k) and L (2 × 5k): ≈ 7k core-h, 1.5-2.5 TB.
- **S1 grand total (Phase 2 + Phase 3): ≈ 77-87k core-h, ≈ 20-32 TB.**

**Preferred route for full production:** a central request through EXO/PdmV (McM) once W1 is validated. Phase-2 exploration uses private CRAB production.

---

## 3. Scope S2: CMS Run-3 (+2017-18) samples for Phase 2

Data first. The `EXOHighMET` (RAW-RECO) and `EXOMONOPOLE` (USER with pixel/strip clusters and pixel digis) skims are defined for the Run-3 JetMET/MET PDs, and `HighMET` for the Run-2 MET PD. Source: CMSSW `Configuration/Skimming/python/autoSkim.py`, `PDWG_EXOHighMET_cff.py`, `PDWG_EXOMONOPOLE_cff.py`, VERIFIED(api) (STRAT C7). Whether they were actually produced, and for which eras, is **UNVERIFIED**.

| ID | Name / process | Content | Format / tier with hits | # events for Phase 2 (justification) | CPU / storage (ESTIMATE) | Availability |
|---|---|---|---|---|---|---|
| S2-DATA-MET | Run-3 MET-stream skim, 2022-2025 eras | pfMET > 200 GeV, or pfMET/caloMET > 2 with the smaller > 150 GeV, + good PV. **Does not contain CR1 (MET 30-60 GeV) or VR3 (MET 150-200 GeV)**; see S2-CR1 / S2-VR3 | RAW-RECO (`EXOHighMET`). Alternative USER (`EXOMONOPOLE`): MET/JetMET coverage **only from 2024** per its config comment, earlier eras UNVERIFIED; uses the higher-threshold `HLT_PFMET200_BeamHaloCleaned` path, so lower ε_trig than P1 | Phase 2: 10⁵-event slice for schema/DQ/occupancy; plane-finder output only in **sidebands** (SR blinded, STRAT D12). Full skim in Phase 3 | local-reco + plane finder 2-5 s/evt → ~0.1k core-h per 10⁵; RAW-RECO ~1.5-3 MB/evt → 0.15-0.3 TB per 10⁵. The full skim (O(10⁶-10⁷) events, O(10) TB) is UNVERIFIED: get it from DAS `summary` | exists-CMS-check-DAS |
| S2-DATA-R2 | 2017-18 MET PD `HighMET` skim (Phase-1 pixel era, as in 2410.09164) | as above | RAW-RECO | 10⁴ slice | small | exists-CMS-check-DAS |
| S2-ZB | ZeroBias (Run 3), spread over nPV and eras | random BX | RAW (re-run local reco) | 2×10⁵ (M2 embedding source; random-plane rate vs nPV, VR4) | ~0.3-1k core-h; ~0.2-0.4 TB (~1-2 MB/evt RAW, ESTIMATE) | exists-CMS-check-DAS (tape recall likely) |
| S2-CR1 | Low-MET, PU-dominated CR (MET 30-60 GeV) | ZeroBias RAW (= S2-ZB) + jet-triggered JetMET RAW via pick-events | RAW | 10⁵ (θ transfer factor for M1 with ≥ 100 sideband planes, ESTIMATE) | ~0.3-0.5k core-h; 0.1-0.3 TB | exists-CMS-check-DAS (tape) |
| S2-VR3 | Intermediate-MET VR (offline MET 150-200 GeV, `PFMETNoMu120`-type triggered) | MET/JetMET PD RAW via `edmPickEvents` on a MINIAOD/NANO pre-selection; fallback VR3' = MET 200-250 GeV inside `EXOHighMET` (STRAT D18) | RAW | 10⁵ | ~0.3-0.5k core-h; 0.15-0.3 TB | exists-CMS (RAW on tape; recall request) |
| S2-NC | NoBPTX (+ `EXONoBPTXSkim`), Cosmics | non-collision | RAW / skim | 10⁴-10⁵ | small | exists-CMS-check-DAS |
| S2-L1DS | L1 scouting 2024 (DT stubs every BX) | P6 channel; P5 fake rate | scouting format (UNVERIFIED) | as used by 2601.20063 (3.7 fb⁻¹) | UNVERIFIED | exists-CMS-check-DAS / ask the L1DS team |
| S2-SIG | Quirk E, m_Q ∈ {200, 500, 800} × Λ ∈ {0.3, 0.6, 2, 10, 30} keV at 13.6 TeV; Run-3 geometry/era, premix PU | Pythia8 HV + quirk G4 (W1 + W9) | FEVTDEBUG (+ RAW-like for reco) | 5k/point = 7.5×10⁴ (same logic as S1-SIG) | ~60-120 s/evt (UNVERIFIED, Run-3 premix) → 1.3-2.5k core-h; ~0.2-0.4 TB | must-produce |
| S2-ZNN / WJ / TT / QCD / DY | Run-3 13.6 TeV backgrounds | MC | needs a hit-level tier (GEN-SIM-RAW or GEN-SIM-DIGI-RAW); if only AODSIM/MINIAODSIM exist, re-digitise from GEN-SIM with the premix library | 10⁵ Z(νν), 10⁵ W, 5×10⁴ tt̄, 5×10⁴ DY (closure and data/MC for preselection variables; background normalisation is data-driven) | if re-digitised: ~100 s/evt → ~8k core-h total; ~1-2 TB | exists-CMS-check-DAS |

S2 Phase-2 total (ESTIMATE): ≈ 11-16k core-h and ≈ 2.5-4.5 TB (including S2-CR1/VR3), excluding the full data skim (Phase 3).

---

## 4. Scope S3 (staged): what goes in which stage
- **Stage A (months 0-3):** all of §1, plus S1-VAL, S1-SIG0 and S1-TT (read-only). Data: 10⁴ events each of S2-DATA-MET and S2-ZB (schema and occupancy only).
- **Stage B (months 3-9):** S1-SIG, S1-PU, S1-ZNN (+ WJ/QCD/DY if they exist in DAS). S2-ZB at full Phase-2 size (data-anchored random-plane rate vs nPV, VR4).
- **After gate G-S2:** S2-SIG and the S2 backgrounds, plus the full S2-DATA-MET skim.
- Stage A + B cost ≈ S1 cost + ≈ 1-2k core-h for the data slices (ESTIMATE).

---

## 5. CMS checks for the user to run (all patterns UNVERIFIED)

Run with a valid grid proxy: `voms-proxy-init -voms cms`. For every hit, record `summary` (nevents, size) and `site` (disk vs tape).

```bash
# --- 0. Is anyone in CMS already doing this? (most important, week 1)
dasgoclient -query="dataset=/*Quirk*/*/*"          ; dasgoclient -query="dataset=/*quirk*/*/*"
dasgoclient -query="dataset=/*HiddenValley*/*/*"   ; dasgoclient -query="dataset=/*Infracolor*/*/*"
#   plus: CADI and CDS search "quirk"; McM request search "quirk"/"Quirk"; ask the EXO LLP conveners.

# --- 1. Phase-2 MC campaigns available (find the newest one and its geometry)
dasgoclient -query="dataset=/TT_TuneCP5_14TeV*/Phase2*/*"
dasgoclient -query="dataset=/*/Phase2Spring24*/GEN-SIM-DIGI-RAW-MINIAOD"
dasgoclient -query="dataset=/*/Phase2Spring25*/*"  ; dasgoclient -query="dataset=/*/Phase2Fall24*/*"
dasgoclient -query="dataset=/*/Phase2Spring26*/*"
# backgrounds at PU200
dasgoclient -query="dataset=/Z*NuNu*14TeV*/Phase2*/*"     ; dasgoclient -query="dataset=/Z*To2Nu*14TeV*/Phase2*/*"
dasgoclient -query="dataset=/WJetsToLNu*14TeV*/Phase2*/*" ; dasgoclient -query="dataset=/W*LNu*14TeV*/Phase2*/*"
dasgoclient -query="dataset=/QCD*14TeV*/Phase2*/*"
dasgoclient -query="dataset=/DYJetsToMuMu*14TeV*/Phase2*/*"
dasgoclient -query="dataset=/MinBias_TuneCP5_14TeV-pythia8/Phase2*/*"
dasgoclient -query="dataset=/Neutrino_E-10_gun/Phase2*/*"        # incl. PREMIX libraries
dasgoclient -query="dataset=/*/Phase2*/PREMIX"
dasgoclient -query="dataset=/*/Phase2*/FEVT*"                     # anything with SimHits

# --- 2. Run-3 / Run-2 hit-level data skims (STRAT C7)
dasgoclient -query="dataset=/JetMET*/Run202*-EXOHighMET-*/RAW-RECO"
dasgoclient -query="dataset=/MET/Run2022*-EXOHighMET-*/RAW-RECO"
dasgoclient -query="dataset=/JetMET*/Run202*-EXOMONOPOLE-*/USER"
dasgoclient -query="dataset=/MET/Run201[78]*-HighMET-*/RAW-RECO"
dasgoclient -query="dataset=/MET/Run201[78]*-EXOMONOPOLE-*/USER"
dasgoclient -query="dataset=/JetMET*/Run202*-EXODisappTrk-*/USER"  # AOD-like, check content
# RAW for CR1 / VR3 (not in the MET skims): parent RAW datasets + pick-events
dasgoclient -query="dataset=/JetMET*/Run202*/RAW"  ; dasgoclient -query="dataset=/MET/Run2022*/RAW"
#   edmPickEvents.py "/JetMET0/Run2024*-*/MINIAOD" events.txt   (run:lumi:event list from a MINIAOD/NANO MET 150-200 selection)
dasgoclient -query="dataset=/ZeroBias*/Run2024*/RAW"
dasgoclient -query="dataset=/NoBPTX/Run202*/RAW"  ; dasgoclient -query="dataset=/NoBPTX/Run202*-EXONoBPTXSkim-*/*"
dasgoclient -query="dataset=/Cosmics/Run2024*/RAW"
dasgoclient -query="dataset=/L1Scouting*/Run2024*/*"
dasgoclient -query="summary dataset=<name>"   ; dasgoclient -query="site dataset=<name>"

# --- 3. Run-3 MC with a hit-level tier
dasgoclient -query="dataset=/Zto2Nu*13p6TeV*/Run3Summer2*/*"
dasgoclient -query="dataset=/WtoLNu*13p6TeV*/Run3Summer2*/*"
dasgoclient -query="dataset=/*13p6TeV*/Run3Summer2*/GEN-SIM-RAW"
dasgoclient -query="dataset=/Neutrino_E-10_gun/Run3Summer2*/PREMIX"
```

Other CMS-side checks:
- (a) The Run-3 integrated luminosity per era, from the lumi POG (it is UNVERIFIED in STRAT §6.1).
- (b) T2/T3 site access from USFQ, and a CRAB/CPU quota (UNVERIFIED [ST §4]).
- (c) Phase-2 OT front-end delay-scan results (tracker DPG) and the BTL TOFHIR TOA range (MTD DPG) for OI-1.
- (d) The Phase-2 trigger rules for consecutive L1As (BX and BX+1) [EX §3.4b].
- (e) The CMS route for HL-LHC projections (FTR PAS vs DP note) for S1.

---

## 6. Software work items that block sample production

| ID | Work item | Blocks | Effort (ESTIMATE) | Notes |
|---|---|---|---|---|
| **W1** | **Port Athena `Simulation/G4Extensions/Quirks` (Apache-2.0) to CMSSW `SimG4Core`**. Tasks: (i) particle entries for ±PDG id in HepPDT / `CustomParticleFactory`; (ii) physics constructor attaching `QuirkTransportation` (pattern: `MonopoleTransportation.cc`) + `G4hIonisation` + `G4hMultipleScattering`; (iii) partner pairing / alternating stacking in `StackingAction`/`Phase2StackingAction`; (iv) CMS field/stepper interface for `HyperbolaStepper`; (v) exemption from looper killers, step limits and `MaxTrackTime`; (vi) truth watcher (`RHStopTracer`-style); (vii) MT safety; (viii) **CPU/event measurement** (A7); (ix) validation V1-V5 | all CMS signal (S1-SIG*, S2-SIG) | **1-3 person-months** for an experienced CMSSW/G4 developer [ST §1C] | Port the `standalone/` app first (W4). Track the 2026 ATLAS fixes ("killed quirk partner handling") [EX §1.0 item 3]. Check the Geant4-header file licence (STRAT C10). CMSSW uses Geant4 11.4.x [ST §1C] |
| W2 | CMSSW generator fragment: Pythia8 HV `ffbar2EvEvbar`, `Ngauge = 2`, `fragment = off`, `4900011:m0 = m_Q`, E_v stable; pT(QQ̄) filter; scale/PDF/shower weights stored | all signal | 1-2 weeks | Optional MG5 UFO for NLO/FxFx at 2 masses (+1-2 weeks) [ST §1A]. **Check (review C4)** that Pythia8 `ffbar2EvEvbar` gives E_v vector-like singlet Z couplings (a_E = 0, as TH §2.2 assumes) rather than SM-electron chiral couplings: compare the cos θ* distribution with an MG5 vector-like UFO. The rate is fixed by D2 regardless. **Also refine the 13 → 14 / 13.6 TeV scaling of the measured σ(Z→νν, pT > 200 GeV) = 3.00 pb [2012.09254] with MG5, and fix the HT- or pT-binned Z(νν) sample definition (R2 B1).** |
| W3 | Fast numba propagator (straight string + B + Bethe-Bloch), CMS-like parametric geometry and ODD surfaces; per-hit toa | P-S1, regime maps, OI-1 first look | 1-2 weeks [ST §3.2] | Validate V1, V2, V5. Use the Tracker-TDR radii and keep them configurable (as-built may differ; review C8) |
| W4 | Standalone Geant4 build of the Athena quirk code (conda geant4 11.4.3) | de-risks W1; P-full on ODD | 2-4 weeks [ST §2] | can be skipped if W1 goes directly |
| W5 | Hit-ntuple dumper (from `Validation/RecoTrack/plugins/TrackingNtuple.cc` / `L1TrackNtupleMaker`): hit x, y, z, layer, module, cluster size, ToT/charge, BX/time, MTD time, sim links, on-helix flag | every CMS sample's schema inventory | 2-3 weeks | one schema for Phase-2 and Run-3 |
| W6 | Digitizer timing configurations (`TofLowerCut/TofUpperCut`, 2S `HitDetectionMode` sampled/latched) + toa study (OI-1) | S1-SIG second digitisation | 1-2 weeks | STRAT C8. SampledMode samples the CBC pulse at the BX time, so the default SquareWindow is likely pessimistic (review C6) |
| W7 | Plane finder v0 (numba) → C++/CMSSW module | variable survey, closure test | 3-6 weeks | v0 needed in week 3 for the closure test |
| W8 | GNN / MaskFormer pipeline (acorn or hepattn) on the common hit schema | approach (b) | 4-8 weeks | Phase 2 needs only a baseline; full training in Phase 3 |
| W9 | Run-3 era/geometry configuration of W1 + Run-3 premix workflow | S2-SIG | 1-2 weeks after W1 | |
| W10 | L1 emulation hooks: stubs (`TTStubsFromPhase2TrackerDigis`), L1 tracks, Phase-2 GT PuppiMET | trigger efficiencies (replaces A4) | 1-2 weeks | |
| W11 | ColliderML μ-overlay builder (Poisson sampling, beam-spot z/t smearing) | P-B1 closure and μ scan | ~1 week | |
| W12 | Zero-bias embedding / hit mixing for CMS data (M2) | Phase 3 background | 4-6 weeks | prototype only in Phase 2 |

Critical path: **W2 → W1 → (W6, W5) → S1-SIG / S2-SIG**. The public path (W3 + W11 + W7 v0) runs in parallel and does not wait for W1.

---

## 7. First 4 weeks: ordered action list

**Week 1 (decisions and access)**
1. User: CMS-internal check (CADI/CDS/McM "quirk"; DAS block 0 of §5); write to the EXO-LLP conveners (STRAT Q2). *Gate for everything else.*
2. User: run the DAS queries of §5 blocks 1-3; paste the `summary`/`site` output into `phase2_exploration/das_checks.md`.
3. User: confirm the T2/T3 site, CRAB quota and lxplus/CVMFS access; name the W1 developer or partner (Q3).
4. Agent: create the pixi environment [ST §4]; download Zenodo 17941765; download the ColliderML PU pool (P-B1, full 7.33 M sub-events, 360 GB, on cluster disk) and the P-B2/P-B3 2×10⁴-event subsets.

**Week 2 (prototype signal)**
5. W3 fast propagator + CMS-like geometry; validate against the analytic solution (V1), the thickness formula (V2) and the Zenodo trajectories (V5).
6. W2 generator fragment; GEN-only samples at 200/500/1000 GeV → pT(QQ̄) spectra; trigger-proxy efficiency vs threshold (100/130/170/200 GeV), replacing A4. Compute the P5 acceptance f(|η| < 0.83, β_pair ≥ 0.15) directly (STRAT §10.1a). MG5 13→14 TeV scaling of the measured Z(νν) σ [2012.09254]. Pythia HV coupling check (C4).
7. Start W1/W4: clone Athena `Quirks`, build `standalone/`, map its classes onto `SimG4Core` (design note).

**Week 3 (prototype background and timing)**
8. W11 + W7 v0: **closure test** on the full ColliderML PU pool (1.47×10⁵ μ = 50 crossings). Primary: Knapen's 10⁻³ (4/8 layers). Secondary: 6×10⁻⁵ via factorisation and resampling (§0). Then a μ scan at 50/100/140/200 → first public-prototype f_plane(μ).
9. OI-1 first look with W3: per-layer toa distributions vs (m_Q, Λ, pT(QQ̄)); fraction of OT hits with toa > 12.5 ns.
10. W5 prototype on 10³ events of S1-TT (official tt̄ PU 200): schema inventory of the Phase-2 RAWSIM digi collections.

**Week 4 (first CMS-geometry quirk and data slices)**
11. W1 milestone: first quirk pair through Geant4 in the CMS D110 geometry (pair gun, no PU; S1-VAL iv); compare with W3 on the same 4-vectors. Measure CPU/event (A7).
12. If S2/S3 data access exists: 10⁴ events each from S2-DATA-MET and S2-ZB → hit occupancy vs nPV, skim schema, data-quality checks (no SR plane variables).
13. Write `phase2_exploration/plan.md` (files, variables, plots); append to LOG.md; update STRATEGY_DRAFT if week-1 answers change Q1/Q2.
14. Decide on submitting S1-SIG0 and S1-PU production (once W1 passes V1-V4).
