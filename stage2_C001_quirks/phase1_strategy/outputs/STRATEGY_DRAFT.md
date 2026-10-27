# C001 Phase 1 (Strategy) draft: colour-neutral EW-charged quirks in the CMS tracker

Status: **v3 — Phase-1 PASS (round 2)**, 2026-10-07. Round 1: ITERATE; round 2: PASS with 3 Category B items, applied here. See Sec. 20 "Response to review". Analysis type: **search** (convention: `jfc/src/conventions/search.md`).
Experiment: CMS (user is a CMS member). Benchmark: E = (1,1)_{-1} vector-like Dirac fermion, N_IC = 2, Λ ≡ √σ.
Reviewed: `../review/STRATEGY_CRITICAL_REVIEW.md` (R1) and `../review/STRATEGY_CRITICAL_REVIEW_R2.md` (R2). Scope decision is the user's (Sec. 6, `OPEN_QUESTIONS.md`).

---

## 0. Work plan (written before executing)

| Section | Content | Inputs that feed it |
|---|---|---|
| 1 | Executive summary and recommendation | all |
| 2 | Conventions, labels, source keys, number cross-check log | JFC `02-phases.md`, `05-practices.md`; all research files |
| 3 | Physics motivation | TH §0, §6; RV-T; LM §2-3 |
| 4 | Signal and signature, regime map vs (m_Q, Λ) | TH §1, §3, §4 |
| 5 | Discriminating observables | TH §4; EX §3.1, §4; 1708.02243; 2410.00269 |
| 6 | Scope options S1/S2/S3, novelty audit vs ATLAS, recommendation | EX §1, §1.2; ST §0, §5; RV-E; RV-F; CMSSW skim configs (checked here) |
| 7 | Benchmark and signal grid | TH §1.3, §2.3, §7; ST §3.1 |
| 8 | Sample inventory, background classification | ST §1-3; EX §4 |
| 9 | Selection/reconstruction approaches and their comparison | 1708.02243; 2410.00269; ST §1A, §2; EX §1.0 |
| 10 | Trigger strategy; late-hit / BX open item | EX §3.2-3.6; TH §4.3; CMSSW digitizer config (checked here) |
| 11 | Background estimation, control/validation regions, blinding | EX §2, §4; conventions/search.md |
| 12 | Systematic plan (every convention source) | conventions/search.md; TH §5; EX §2, §4 |
| 13 | Reference analyses and published numerical results | EX §2; cached PDFs of 2410.09164, 2601.20063, 2309.16823, 2607.26195 |
| 14 | Technique selection (statistics) | conventions/search.md; 2607.26195 |
| 15 | Competition and timeline | EX §1.0-1.2 |
| 16 | Risk register | all |
| 17 | Open questions (summary; full text in `OPEN_QUESTIONS.md`) | all |
| 18 | [A]/[L]/[D] registry; JFC self-check | — |

Method: every number below was re-read in the research report it comes from. A sample of load-bearing numbers was also re-checked against the cached primary PDFs (`../research/cache/pdf/*.txt`). Conflicts found are listed in Sec. 2.4. No new physics research was done, with three small read-only CMSSW checks (Sec. 2.4, items C7-C9) because they decide data access and the timing open item.

---

## 1. Executive summary

- **Physics.** A pair of heavy EW-charged quirks joined by a keV-scale flux tube crosses the tracker as two oscillating, non-helical, coplanar, slow, heavily ionising tracks. No SM process makes this pattern [RV-T §6; 1708.02243 Sec. II]. FASER excludes only m_Q < 57-179 GeV across Λ = 0.3-30 keV [HEPData ins3184325 t2, via TH §6.3].
- **What changed this round.**
  1. ATLAS has an active quirk search, most likely on Run-2/3 Inner Detector data, with Geant4 quirk simulation and an ML pair finder; an internal (m_Q, Λ) contour already exists [EX §1.0]. Result ESTIMATE 2028-29.
  2. The coplanar plane-finder works at 3.8 T only in a mass-dependent window, nominally **Λ ≈ 0.6-15 keV** at m_Q ≈ 500 GeV: ≈ 0.55-11 keV at 200 GeV and ≈ 0.8-19 keV at 1 TeV (Sec. 4.4) [TH §0 item 4a, §4.4].
  3. Heavy, triggerable pairs reach the outer tracker and MTD late: median delay at the BTL radius ≈ 16 ns at m_Q = 500 GeV and ≈ 33 ns at 1 TeV, for pT(QQ̄) = 250 GeV [TH Tab. 4.3; Sec. 4.2]. For 200 GeV pairs, all hits are in time. New finding here: the default CMSSW Phase-2 digitizer **drops** OT hits whose delay exceeds 12.5 ns (Sec. 2.4 C8). Default simulation would silently remove high-mass signal hits.
  4. σ(pp → EĒ) is ~3× the Gate-4 estimate: 6.11 fb at 500 GeV, 14 TeV, N_IC = 2 (ESTIMATE) [TH §2.3].
  5. Trigger efficiency (ESTIMATE): ≈ 0.1 with the MET baseline; ≈ 0.15-0.25 with a lowered L1 MET [EX §3.6]. A new slow-muon-system L1 seed is **not** ISR-independent: the bound pair must have pT(QQ̄) ≳ 60-80 GeV (m_Q = 200 GeV) to ≳ 140-190 GeV (500 GeV) to reach the muon system with β ≳ 0.15. It adds acceptance mainly at low mass: the union is ≈ 0.2-0.3 at m_Q ≈ 200 GeV and ≈ 0.17-0.28 at 300 GeV (Sec. 10.1).
  6. The only public quirk Geant4 code is Athena `Simulation/G4Extensions/Quirks` (Apache-2.0); it must be ported to CMSSW SimG4Core [ST §0 item 1, §1C].
  7. New finding here: CMSSW already defines **RAW-RECO and cluster-level MET skims** for Run 2 and Run 3 (`EXOHighMET`, `EXOMONOPOLE`; Sec. 2.4 C7). If they were produced (DAS check), a Run-3 hit-level analysis needs no RAW re-reconstruction campaign.
- **Reach depends on the background** (Sec. 6.1, expected 95% CL CLs, Λ = 3 keV, Knapen efficiencies):
  - Run 2 (2017-18) + Run 3: ≈ 0.72-0.87 TeV;
  - Phase 2 at 3 ab⁻¹: ≈ 1.2 TeV if the background is zero; ≈ 0.97 TeV with the μ = 50 background rate (B ≈ 30; 0.94 TeV with a 20% background uncertainty); ≈ 0.76 TeV if PU 200 multiplies that background by 16, falling to **0.57 TeV** with a 20% uncertainty on it.
  The Phase-2 gain over Run 2+3 therefore ranges from ≈ +0.4 TeV down to ≈ 0, depending on how well PU-200 random coplanarity is suppressed.
- **Recommendation: S3 (staged).** First build the common pieces (quirk G4 port, hit dumper, plane finder, GNN). Deliver a CMS Phase-2 sensitivity study (S1 content). In parallel, use Run-3 MET-skim and zero-bias data to *measure* the random-coplanarity background in data. Decide at month ~9 whether to launch the full Run-3 search (S2). The decision is the user's (Q1 in `OPEN_QUESTIONS.md`).
- **Novelty that survives the ATLAS effort** (Sec. 6.4): PU-200 operation; a muon-system slow-pair L1 seed (gain at low m_Q, plus an independent β tag); MTD 1/β; the late-hit / BX-acceptance problem and its fix; analog strip dE/dx on every Run-3 layer (ATLAS strips are binary); the first CMS result. **"First LHC central-detector quirk search" is very likely gone** to ATLAS.

---

## 2. Conventions

### 2.1 Labels (JFC)
- **[A] Assumption**: a physics or technical premise taken as true without proof here. It must be validated or carried as a systematic.
- **[L] Limitation**: a known shortfall of the method, data or tools, with its expected impact. It goes to the AN "Known limitations".
- **[D] Decision**: a binding choice among alternatives, with its reason. It is tracked in COMMITMENTS.md from Phase 4a. A silent change of a [D] is Category A.

Each label carries an ID (A1, L1, D1, ...). The registry is in Sec. 18.

### 2.2 Number tags
- `ESTIMATE`: a calculation by an agent of this project, with its inputs stated or referenced.
- `UNVERIFIED`: recalled or read from a secondary source, not checked against the primary source.
- `VERIFIED(api)`: read from a live public repository or API on 2026-10-07.
- Every other number carries a citation `[ID, location]`.

### 2.3 Source keys
| Key | File |
|---|---|
| TH | `research/theory_signal_model.md` |
| EX | `research/experimental_status_2026.md` |
| ST | `research/samples_and_tools.md` |
| LM | `literature/literature_map.md` (+ `bibliography.json`) |
| RV-T / RV-E / RV-F | `../research/reviews/{theory,experimental,feasibility}/C001.md` (Gate 4) |
| CONV | `jfc/src/conventions/search.md` |
| arXiv IDs | primary papers, as cited inside TH/EX/ST; cached text in `../research/cache/pdf/` |

Physics conventions [D1]:
- Λ ≡ √σ, string tension σ = Λ² [TH §1.1; 1708.02243 below Eq. 2].
- The cosmology paper's Λ is T_c ≈ 0.6√σ; convert its bounds by ×1/0.6 [TH §1.1; 2512.20696 Eq. 1].
- Oscillation length: use the exact ℓ_max = 2(γ*−1)m_Q/σ = 3.95 cm × (γ*−1)(m_Q/100 GeV)(keV/Λ)² [TH §1.1]. Do not use the literature shorthands, which differ by factors 2-4 [TH §1.1].
- Results are quoted per (m_Q, Λ) for N_IC = 2, with σ limits per unit N_IC so that N_IC = 3, 5 follow by rescaling [TH §1.3].

### 2.4 Number cross-check log (conflicts found while synthesising)
| # | Item | Finding | Resolution used here |
|---|---|---|---|
| C1 | FASER ISR vs MC-stat systematic | EX §4 item 5 and RV-F §8 attribute "~6%, up to 28% at small Λ" to the ISR/shower-scale variation. The FASER text [2607.26195 p.5, re-read in cached PDF] gives **≈25%** for the Pythia shower-scale ×0.5/×2 variation and **≈6% (up to 28%)** for finite MC statistics. TH §5 has it right. | Use ISR ≈ 25% and MC-stat 6-28% as the FASER reference values. EX/RV-F are corrected in this draft. |
| C2 | Pair velocity | EX §3.4b says "the theory agent quotes β ≈ 0.3-0.6 for m_Q ≳ 500 GeV". In TH §4.1 those numbers are the **per-quirk CM speed β*** (median 0.54-0.64), not the pair velocity. **TH Tab. 4.3 is also internally inconsistent**: its β_T medians (0.23/0.14/0.09) do not reproduce its own t_BTL medians (10.0/19.8/36.7 ns), since r/(β_T c) = 16.6/27.3/42.5 ns. An independent check with TH's γ* medians (M_QQ̄ ≈ 2γ* m_Q, pT(QQ̄) = 250 GeV, y = 0, v_T = pT/√(M² + pT²)) gives v_T = 0.43/0.20/0.10, which matches the t_BTL column (v_T = 114.8 cm/(c t_BTL) = 0.38/0.19/0.10). | Use **v_T = 0.38/0.19/0.10** (200/500/1000 GeV, pT = 250 GeV) and **0.55/0.34/0.20** (pT = 500 GeV), all derived from the TH t_BTL column (scratchpad `fix.py`). The TH β_T column is flagged as wrong upstream. Layer-by-layer delays are in Sec. 4.2. |
| C3 | Cross section | RV-F §2 gives σ(500 GeV, 14 TeV) ≈ 1.5-2 fb. TH §2.3 gives 6.11 fb (LO CT18NLO × SUSY-WG K-factor; ESTIMATE). RV-F assumed σ_F/σ_S = 4; the computed ratio is 11-18. | Use TH §2.3. RV-F yields are superseded. |
| C4 | K-factor / normalisation | ST §2 (track C step 1) says "normalise to NLO DY: K = 1.33-1.45 (2404.13814)". Those K are relative to an LO-PDF LO calculation. TH §2.2 uses K relative to CT18NLO LO, which agrees with 2404.13814 to ≤ 6%. | [D2] Normalise all signal to the TH §2.3 table (absolute σ), not to "generator LO × K". |
| C5 | ATLAS search scope | ST §0 item 2 suggests ITk-like inputs. EX §1.0 item 4 checked `DumpObjects.cxx` (Run-3 Pixel/SCT managers first, ITk fallback), the 24.0 target branch, and TRT hits in quirkviz, and concludes "most likely Run-2/3 ID", medium confidence. | Use EX (more evidence). Treat an ATLAS ITk projection as "not excluded" (risk R1b). |
| C6 | Signal grid | ST §3.1 proposes 25 points (200-1000 GeV × 0.3/1/3/10/30 keV). TH §7 proposes 48 points (200-1250 GeV × 0.3/0.6/1/2/5/10/20/30 keV), with 0.6 keV as the coplanar onset at 3.8 T. | Use the TH grid as the target and a 15-point subset of it for Phase 2 (Sec. 7). |
| C7 | Hit-level data skims (new check) | CMSSW `Configuration/Skimming/python/autoSkim.py` (master, VERIFIED(api)): Run-3 `JetMET0/1`, `JetMET` and `MET` PDs run `EXOHighMET` (data tier **RAW-RECO**, selection pfMET > 200 GeV or pfMET/caloMET > 2 with the smaller > 150 GeV, plus a good PV; `PDWG_EXOHighMET_cff.py`) and `EXOMONOPOLE` (tier USER; keeps `siStripClusters`, `siPixelClusters`, `siPixelDigis`, `generalTracks`; 2024 paths `HLT_Photon200`, `HLT_PFMET200_BeamHaloCleaned`; `PDWG_EXOMONOPOLE_cff.py`). Run 2: `MET` PD runs `HighMET+EXOMONOPOLE` (`autoSkimRunII`). | If these datasets exist in DAS (UNVERIFIED), S2 data access is far cheaper than "RAW reprocessing". First DAS check (`SAMPLE_REQUIREMENTS.md` §3). |
| C8 | OT time window in simulation (new check) | CMSSW `SimTracker/SiPhase2Digitizer` (master, VERIFIED(api)): a SimHit is digitised only if toa = tof − \|r\|/c lies in (−12.5, +12.5) ns for PS-pixel, PS-strip and 2S (`phase2TrackerDigitizer_cfi.py` `TofLowerCut/TofUpperCut`; `PSSDigitizerAlgorithm.cc` `select_hit`), and in [−5, +20) ns for IT pixels unless time-walk emulation is on (`PixelDigitizerAlgorithm.cc`). The 2S default is `HitDetectionMode = 0` (SquareWindow); Sampled and Latched modes exist. | Quirk OT hits with delay > 12.5 ns are **dropped by default** in simulation. Signal efficiencies from default-configured samples are lower bounds and model-dependent. See OI-1 (Sec. 10.4). |
| C9 | Inner Tracker radii | TH §4.1 marks TBPX L2-L3 as UNVERIFIED (≈ 6.1/10.4 cm). EX §3.1 reads Tracker TDR Tab. 10.1: 29.0, 70.1, 117.8, 157.4 mm. | Use EX (TDR value; as-built may differ). |
| C10 | Athena licence | TH §3.5 says the licence field is "Other" and QuirkTransportation carries a Geant4 header (UNVERIFIED). ST §1A reads the repo LICENSE as Apache-2.0 (VERIFIED(api)). | Apache-2.0 for the package; check the Geant4-header file before redistribution (work item W1). |

Re-verified against primary PDFs in this session:
- Knapen Tab. I: ε_trig 0.10, ε_fid 0.28, ε_reco 0.11/0.41/0.65/0.72/0.74 at Λ = 1-5 keV (800 GeV DY).
- Knapen Sec. IV: random planes 10⁻³ (4/8 layers) and 6×10⁻⁵ (all layers), O(1000) unassociated hits per layer.
- 1911.02223: "~10⁻² fb, which cannot be neglected".
- FASER systematics text (C1).
- 2410.00269: "Effects from pile-up remain to be studied". Track efficiency at m_Q = 500 GeV, Λ = 500 eV: 71.9% with 8 layers and 79.0% with 25 layers [Sec. E and Tab. I]. (v1 wrongly attributed 79.0% to 8 layers.)
- 2410.09164: τ′ (DY, Q = 1e) excluded below 1.02 TeV (ionisation method) and 1.14 TeV (mass method); Q = 2e below 1.32 / 1.41 TeV [cached PDF l.986-987 and Tab. 3] (corrected in v2; see Sec. 13).
- 2309.16823 Tab. 7: dE/dx calibration 3-8%, luminosity 1.6%.
- 2410.09164: muon-timing "as large as 30%", luminosity 2.0%, ε_trig 0.86 (stau).
- 2601.20063: 3.7 fb⁻¹, 0.15 ≲ β ≲ 0.80.

---

## 3. Physics motivation

1. **Generic hidden confinement.** A new SU(N_IC) with only heavy fundamentals (m_Q ≫ Λ) gives unbreakable flux tubes ("quirks") [0805.4642 Sec. 1-3]. Λ is log-flat in the UV coupling. The whole target window 0.3-30 keV corresponds to α_IC(m_Q) ≈ 0.040-0.052, a ~25% coupling range (ESTIMATE) [TH §6.2]. GUT-compatible examples give Λ ~ MeV, 10 keV and 100 eV [0805.4642 Sec. 2.5].
2. **Neutral naturalness** motivates quirks, but with GeV-scale Λ [RV-T §5; TH §6.2]. The mesoscopic (keV) window is therefore **signature-driven, not naturalness-driven** [A1]. The strategy says this plainly.
3. **Cosmology.** Nothing excludes the target region. A discovery would imply a low reheating temperature, T_RH ≲ O(100 GeV) [2512.20696 abstract, Sec. 4.1, Sec. 6; TH §6.1]. This adds motivation; it is not a constraint.
4. **Experimental gap.**
   - FASER, 186 fb⁻¹: observed exclusions of 57/72/113/149/163/179/173 GeV at Λ = 0.3/0.5/1/1.7/3/10/30 keV [HEPData ins3184325 t2, via TH §6.3].
   - D0: 107 GeV (N = 2) for 10 keV-1 MeV [1008.3547 abstract].
   - The HSCP/monojet recast (12.9 fb⁻¹) gives 150 GeV at 100 eV and **no bound at 1 keV** for the (1,1)_{-1} fermion with N = 2 [1703.00912 Tab. II].
   - No ATLAS/CMS publication exists [EX §1.1 item 1; LM §6]. One ATLAS search is in progress (Sec. 15).
5. **Signature distinctiveness.** Two mutually bending, coplanar, slow, ~2-10× MIP tracks. Neither an HSCP, R-hadron, monopole, multi-charge nor disappearing-track signature produces this [RV-T §6]. Once observed, a trajectory fit measures m_Q and Λ [1708.02243 App. A].

---

## 4. Signal and signature

### 4.1 Model and production
- Primary benchmark: E = (1,1)_{-1} Dirac fermion, N_IC = 2 [TH §1.3; D3]. Drell-Yan via γ*/Z.
- Cross sections, N_IC = 2, fb (ESTIMATE, LO CT18NLO × SUSY-WG K) [TH §2.3]:

| m_Q [GeV] | 13 TeV | 13.6 TeV | 14 TeV | PDF4LHC21 unc. |
|---|---|---|---|---|
| 200 | 193 | 210 | 220 | ±3.7% |
| 500 | 5.16 | 5.70 | 6.11 | ±6.6% |
| 800 | 0.525 | 0.601 | 0.660 | ±11.9% |
| 1000 | 0.148 | 0.176 | 0.197 | ±18.5% |
| 1200 | 0.0469 | 0.0576 | 0.0656 | ±25% (extrapolated) |

- NNLL scale uncertainty ≤ 1% [TH §2.3, WG json].
- Fermion/scalar ratio 11-18 [TH §2.3].
- The trigger needs ISR: the fraction of DY pairs with pT(j) > 200 GeV is ≈ 0.10 [1911.02223 App. A; 1708.02243 Tab. I].

### 4.2 Dynamics relevant for the tracker [TH §3-4]
- Straight-string EoM with Lorentz force and ionisation. External forces are ≲ 1-4% of Λ² for Λ ≥ 0.3 keV [TH §3.1].
- Glueball emission (ε) is negligible in the tracker for Λ ≤ 30 keV: < 0.1 GeV of ~100 GeV internal energy (ESTIMATE) [TH §3.3].
- Plane thickness d ≈ 1.16 µm × (m_Q/100 GeV)(keV/Λ)⁴(B_xy/T) [1911.02223 Eq. III.12]. At 3.8 T, d = 100 µm (Knapen's Δs cut [1708.02243 Sec. IV]) is reached at Λ = 0.55/0.69/0.81 keV for m_Q = 200/500/1000 GeV (ESTIMATE) [TH Tab. 4.2b]. These values were recomputed here from the formula and agree.
- **Pair transverse velocity and arrival times** (ESTIMATE; inputs: TH Tab. 4.3 t_BTL medians and TH §4.1 γ* medians; method in C2):
  - Median v_T = 0.38/0.19/0.10 for m_Q = 200/500/1000 GeV at pT(QQ̄) = 250 GeV, and 0.55/0.34/0.20 at pT(QQ̄) = 500 GeV.
  - Median BTL arrival 10.0/19.8/36.7 ns, vs 3.8 ns for β = 1 [TH Tab. 4.3].
  - Layer-by-layer delay toa = (r/c)(1/v_T − 1), at η = 0 for the median pair, in ns. This is the quantity the CMSSW digitizer cuts on (C8). Radii from Tracker TDR Tab. 9.1/10.1 via EX §3.1.

| m_Q, pT(QQ̄) | IT L4 (15.7 cm) | PS L1/L2/L3 (24.8/37.2/52.3 cm) | 2S L1/L2/L3 (68.7/86.0/110.8 cm) | BTL (114.8 cm) | OT layers lost with the ±12.5 ns default window |
|---|---|---|---|---|---|
| 200 GeV, 250 GeV | 0.8 | 1.3 / 2.0 / 2.8 | 3.7 / 4.6 / 6.0 | 6.2 | none |
| 500 GeV, 250 GeV | 2.2 | 3.5 / 5.2 / 7.3 | 9.6 / **12.0** / **15.4** | 16.0 | 2S L3 lost; 2S L2 marginal |
| 500 GeV, 500 GeV | 1.0 | 1.6 / 2.5 / 3.4 | 4.5 / 5.7 / 7.3 | 7.6 | none |
| 1000 GeV, 250 GeV | 4.5 | 7.1 / 10.6 / **15.0** | **19.7 / 24.6 / 31.7** | 32.9 | PS L3 and all 2S lost (IT window [−5, 20) ns keeps the IT) |
| 1000 GeV, 500 GeV | 2.1 | 3.3 / 4.9 / 7.0 | 9.1 / 11.4 / **14.7** | 15.3 | 2S L3 lost |

  The individual quirks oscillate about the pair centre of mass, so per-hit times scatter around these values. Pairs at |η| > 0 have longer paths. Full distributions come from OI-1 step 1.
- Per-hit dE/dx ≈ 2-10× MIP, tail ≳ 50× MIP (ESTIMATE) [TH §4.3]. ATLAS-pixel simulation reaches ~60× MIP [1708.02243 App. A, Fig. 7].
- 10-20% of events have > 2 quirk hits on at least one layer [2002.07503 Tab. I].
- Essentially no pairs stop in the tracker; 1-5% stop in the calorimeters [1811.08903 Fig. 2, 6, 7].

### 4.3 Regime map for CMS at 3.8 T (ESTIMATE unless cited) [TH §4.4]
| Λ | Topology | Primary tool | Notes |
|---|---|---|---|
| ≲ 0.2 keV | ℓ_max ≳ 1 m, nearly helical | HSCP searches | out of scope [D4] |
| 0.3 keV to Λ_low(m_Q) | 1-5 crossings, plane thicker than 100 µm (0.1-5 mm) | trajectory χ² fit / GNN | coplanar finder fails; FASER weak here (57-72 GeV) |
| **Λ_low(m_Q) to Λ_high^OT(m_Q)** (nominal "0.6-15 keV", the 500 GeV values) | 10¹-10³ crossings, d ≤ 100 µm, 2 hits/layer resolved in IT and OT | **coplanar finder** + dE/dx + timing | core window; edges in Sec. 4.4 |
| Λ_high^OT to Λ_high^IT | pair merged in OT rφ, resolved in IT | IT-only plane + dE/dx | degrading |
| ≳ Λ_high^IT (≈ 20-40 keV) | one straight, ≥ 2× MIP, "infinite-pT" track | straight-pair / HIP selection | FASER covers up to 100 keV |

### 4.4 Λ-window edges as functions of m_Q (ESTIMATE; scratchpad `fix.py`)
- **Lower edge** (plane thickness = Knapen's Δs cut of 100 µm [1708.02243 Sec. IV]):
  - From d = 1.16 µm (m_Q/100 GeV)(keV/Λ)⁴(B_xy/T) [1911.02223 Eq. III.12] with B_xy = 3.8 T: **Λ_low ≈ 0.458 keV × (m_Q/100 GeV)^¼**, i.e. 0.54/0.69/0.81 keV at m_Q = 200/500/1000 GeV.
  - The thickness formula is accurate only to about ×10 [2002.07503 App. C]. That is ×10^{±¼} ≈ ×1.8 in Λ, so the band is 0.31-0.97 / 0.39-1.22 / 0.46-1.45 keV.
  - B_xy = 3.8 T is the maximum in-plane component, which makes this a conservative (high) Λ_low.
- **Upper edge** (the two quirks merge into one hit when their separation falls below the two-hit resolution):
  - Uses ℓ_max = 3.95 cm (γ*−1)(m_Q/100 GeV)(keV/Λ)² [TH §1.1] with TH median γ* = 1.30/1.25/1.19 [TH §4.1].
  - **Λ_high = [3.95 cm (γ*−1)(m_Q/100 GeV)/s_res]^½ keV.**
  - OT rφ, s_res ≈ 200 µm (2 × the 90-100 µm pitch [TH §4.2]): **Λ_high^OT ≈ 11/16/19 keV** for 200/500/1000 GeV.
  - IT, s_res ≈ 50 µm (2 × 25 µm pitch): **Λ_high^IT ≈ 22/31/39 keV**.
  - ℓ_max is the *maximum* CM separation, and the lab transverse width is ≤ ℓ_max [TH §4.2]. Typical separations are smaller, so these are upper estimates of Λ_high.
- So **"0.6-15 keV" is the nominal window at m_Q ≈ 500 GeV**. At 200 GeV it is ≈ 0.55-11 keV; at 1 TeV it is ≈ 0.8-19 keV. W3 (fast propagator) replaces these estimates with efficiency curves in Phase 2.

[D4] Analysis Λ range: 0.3-30 keV, in three reconstruction categories (low-Λ trajectory/GNN; core coplanar; high-Λ IT-only / straight pair). Category boundaries are set **per m_Q** using Sec. 4.4, not at fixed Λ.

---

## 5. Discriminating observables

| # | Observable | Definition | Signal expectation | Main background it kills | Availability | Source |
|---|---|---|---|---|---|---|
| O1 | **Plane residual Δs** (thickness) and width Δw | RMS / maximum distance of the candidate hits from the best plane through the PV, after removing hits on good helices | Δs < 100 µm in the core window; d ∝ m_Q/Λ⁴ | random PU coplanarity (B1/B2) | all scopes; z-precision from IT + PS only (2S z ≈ 1.4 cm) [TH §4.2] | 1708.02243 Sec. III C, IV |
| O2 | **N_layers on plane** (≥ 1 and ≥ 2 hits) | count of barrel layers / disks with plane hits | up to 10 barrel layers at Phase 2 [EX §3.1]; 2 hits/layer typical | random planes fall from 10⁻³ (4/8) to 6×10⁻⁵ (8/8) at μ = 50 | all | 1708.02243 Sec. IV |
| O3 | **Curvature inconsistency** | helix-fit χ² of plane hits; fraction of plane hits already on reconstructed helices; sign-flip of local curvature between layers | helix χ² ≫ 1; hits not on helices; the two tracks bend toward each other | loopers (B5), conversions (B3), δ-rays (B6), collimated pairs (B7) | all | 1703.00912 (helix χ²); EX §4 |
| O4 | **dE/dx** | pixel 4-bit ToT (Phase 2); pixel + analog strip charge (Run 3) | 2-10× MIP per hit, tail ≳ 50× | B1-B7 (MIP-like) | Phase 2: IT only (OT binary) [EX §3.1]; Run 3: pixels + strips [2410.09164 Sec. 5, G^Strips] | 1708.02243 App. A; 1911.02223 Sec. IV.B |
| O5 | **β from MTD timing** | BTL/ETL time minus the β = 1 expectation | delay of ns ≫ 30-60 ps resolution: near-perfect slow tag *if recorded* | all prompt β = 1 backgrounds | S1 only; the ETL TDC window of 6.25 ns loses late hits; BTL window UNVERIFIED [EX §3.4b] | MTD TDR Sec. 5.4.3 (via EX §3.1) |
| O6 | **Hit-pattern / trajectory fit χ²** | fit of a quirk-pair EoM (m_Q, Λ, momenta) to all hits; or GNN/MaskFormer pair score | good χ², fitted Λ, m_Q consistent | all residual random combinations | all; CPU-heavy | 1708.02243 Sec. IV, App. A; 2410.00269 |
| O7 | **MET-plane alignment** Δφ(MET, n̂) | angle between the MET (ISR recoil) and the plane | the pair is invisible to PUPPI MET, so the MET points along the pair momentum, which lies in the plane | B2 (Z(νν)+jets ⊗ PU): random orientation | all | 1708.02243 Sec. IV |
| O8 | **Plane contains PV and beam line (3D)** | distance of plane from PV; z consistency | yes | conversions (B3), NI (B4), halo (B8), cosmics (B9) | all | EX §4 |
| O9 | **Hit-time pattern in OT** (BX vs BX+1) | presence of plane hits in the next-BX readout, ordered outward | late hits at large r for heavy pairs | prompt backgrounds | only if BX+1 is read out (OI-1) | EX §3.4b |
| O10 | **Muon-system multi-BX straight stubs** | DT/RPC stub sequence over ≥ 3 BXs, outward, straight | pair β ≈ 0.15-0.8 window [2601.20063 Sec. 3]; reached only for pT(QQ̄) ≳ 60-80 GeV (m_Q = 200 GeV) to ≳ 140-190 GeV (500 GeV) (Sec. 10.1) | in-time muons, BX misID | Run-3 L1DS (2024); Phase-2 GMT/scouting | 2601.20063 Sec. 3, 6, 7 |

[A2] The pair is invisible to the trigger MET objects, i.e. it deposits ≲ 5 GeV in the calorimeters within 25 ns [1911.02223 Sec. V]. Quirk deposits change the MET-cut efficiency by ≈ 5% [2002.07503 Sec. VII]. This is validated in signal simulation in Phase 2.

---

## 6. Analysis-scope options

### 6.1 Rate-based reach used to compare scopes (ESTIMATE)
Inputs:
- σ from the TH §2.3 table (log-interpolated).
- ε_tot = ε_trig × ε_fid × ε_reco = 0.10 × 0.28 × 0.65 = 0.018 at Λ = 3 keV, and 0.10 × 0.28 × 0.11 = 0.0031 at Λ = 1 keV [1708.02243 Tab. I, re-checked]. The trigger is P1 (ε_trig = 0.10) in every row.
- Luminosity:
  - CMS 2017-18 = 101 fb⁻¹ at 13 TeV [2410.09164].
  - CMS Run 3 (13.6 TeV) bracketed by **150-350 fb⁻¹** (UNVERIFIED). The upper value is guided by FASER at IP1 having recorded ≥ 333 fb⁻¹ by spring 2026, with Run 3 extended to mid-2026 [EX §1.1 item 4; 2604.16244 p.1; FASER LivHEP slides]. The CMS value must come from the lumi POG (`SAMPLE_REQUIREMENTS.md` §5).
- **Statistical method:** single-bin counting. Expected 95% CL CLs upper limit on the signal count s95 for observed n = median of Poisson(B), from an exact Poisson calculation (normal approximation above B = 300). Results: s95 = 3.0 (B = 0), 4.6-5.6 (B = 2.5-4.5), 8.1 (B = 10), 12.6 (B = 30), 26.6 (B = 160), 45.2 (B = 480), 174 (B = 7680). Reach = the largest m_Q with N_sig ≥ s95. Script: scratchpad `reach.py` (not committed).
- σ is interpolated **log-linearly in m_Q** between TH table points (R2 C5). Log-log interpolation changes low-mass entries by up to ±0.03 TeV, e.g. 1 keV ×256: 0.38 vs 0.41 TeV.
- **The "with B" columns are statistics-only**: the background is assumed known to √B. The δB/B = 20% table below adds a background-normalisation uncertainty, using s95 ≈ 1.96 √(B + (δB)²). Reference sizes: spurious-track systematic 5-52% [2309.16823 Tab. 7]; ABCD bias ±100% [2410.09164].
- **Background scenarios** (ESTIMATE):
  - B(μ = 50) = 10⁻² fb × L [1911.02223 App. A]. Applied unchanged to the Run 2+3 rows, i.e. assuming Run-3 pile-up is comparable to μ = 50 (UNVERIFIED). R2 C6 recalls a 2024-25 average of ~60-64 (UNVERIFIED), which would raise B somewhat.
  - Phase 2 additionally uses the R4 multipliers ×16 and ×256 for μ = 200 without new handles (MTD, dE/dx, trajectory fit).

| Data set | B | Λ = 3 keV, B = 0 | Λ = 3 keV, with B | Λ = 1 keV, B = 0 | Λ = 1 keV, with B |
|---|---|---|---|---|---|
| CMS 2017-18 + Run 3 = 150 fb⁻¹ | 2.5 | 0.78 TeV | 0.72 TeV | 0.54 TeV | 0.49 TeV |
| CMS 2017-18 + Run 3 = 250 fb⁻¹ | 3.5 | 0.83 TeV | 0.75 TeV | 0.58 TeV | 0.52 TeV |
| CMS 2017-18 + Run 3 = 350 fb⁻¹ | 4.5 | 0.87 TeV | 0.77 TeV | 0.62 TeV | 0.54 TeV |
| Phase 2, 1 ab⁻¹ | 10 / 160 (×16) | 1.03 TeV | 0.86 / 0.68 TeV | 0.74 TeV | 0.60 / 0.46 TeV |
| Phase 2, 3 ab⁻¹ | 30 | ≈ 1.2 TeV (σ-table edge; ≈ 1.24 by extrapolation) | 0.97 TeV | 0.92 TeV | 0.69 TeV |
| Phase 2, 3 ab⁻¹ | 480 (×16) | — | 0.76 TeV | — | 0.53 TeV |
| Phase 2, 3 ab⁻¹ | 7680 (×256) | — | 0.58 TeV | — | 0.38 TeV |

Caveats:
- [L1] Knapen's efficiencies are for an ATLAS-like 2 T, 8-layer, μ = 50 toy [1708.02243 Sec. III-IV]. At 3.8 T the low-Λ efficiency is worse (Sec. 4.4).
- The late-hit loss of Sec. 10.4 is **only partly** included. Knapen's ε_fid = 0.28 contains a 25 ns timing cut at ATLAS radii ≤ 0.5 m [1708.02243 Sec. IV]. The CMS ±12.5 ns OT window at r up to 1.1 m is stricter and hits m_Q ≳ 500 GeV hardest (Sec. 4.2 table).
- **Gain of Phase 2 over Run 2+3**:
  - ≈ +0.35-0.4 TeV if both are background-free;
  - ≈ +0.2 TeV with the μ = 50 background rate in both (0.97 vs 0.75-0.77 TeV);
  - ≈ 0 or negative if PU 200 multiplies the random-coplanarity rate ×16-256 without new handles.
  The S1 value therefore hinges on the PU-200 background suppression. That suppression is exactly what S3 measures in data (R4).

**Reach with a background-normalisation uncertainty** (ESTIMATE; Gaussian s95 = 1.96 √(B + (δB)²); scratchpad `syst.py`. At δB = 0 this approximation gives slightly different values from the exact-Poisson table above, e.g. 1.00 vs 0.97 TeV at B = 30):

| Data set | B | Λ = 3 keV: δB/B = 0 / 20% / 50% | Λ = 1 keV: δB/B = 0 / 20% / 50% |
|---|---|---|---|
| Phase 2, 1 ab⁻¹ | 10 | 0.91 / 0.88 / 0.81 TeV | 0.64 / 0.62 / 0.56 TeV |
| Phase 2, 1 ab⁻¹ | 160 (×16) | 0.69 / **0.56** / 0.46 TeV | 0.47 / 0.37 / 0.30 TeV |
| Phase 2, 3 ab⁻¹ | 30 | 1.00 / **0.94** / 0.82 TeV | 0.72 / 0.66 / 0.57 TeV |
| Phase 2, 3 ab⁻¹ | 480 (×16) | 0.77 / **0.57** / 0.46 TeV | 0.53 / 0.37 / 0.30 TeV |
| Phase 2, 3 ab⁻¹ | 7680 (×256) | 0.58 / **0.29** / 0.23 TeV | 0.39 / 0.18 / — |

- The ×256 row with any realistic δB falls to or below the FASER-excluded region (≤ 179 GeV). It is shown only to bound the "no new handles" scenario. The statistics-only ×256 entry in the table above is **flagged as unrealistic**.
- R2 quotes 0.32 TeV for ×256 at 20%. We get 0.29 TeV; the difference is σ interpolation below 200 GeV.
- **Conclusion (strengthened):** without PU-200 handles that keep B at the μ = 50 level *and* know it to ≲ 20%, Phase 2 does not beat Run 2+3 (0.72-0.77 TeV with B). This is the core reason for S3 (measure B in data first).

### 6.2 The three options

| | **S1: CMS Phase-2 sensitivity / design study** | **S2: CMS Run-3 (+2017-18) search on data, then Phase-2 extension** | **S3: Staged (recommended)** |
|---|---|---|---|
| Deliverable | CMS FTR-type projection PAS or DP note (route to confirm with EXO conveners, Q2): sensitivity at PU 200, trigger proposal (P2 + P5), MTD use, late-hit/BX study | CMS paper: observed limits / discovery on ~250-450 fb⁻¹ (2017-18 + Run 3); Phase-2 projection as a follow-up | Stage A (common tools) → Stage B (S1 deliverable) + Run-3 background measurement in data → **gate at month ~9** → S2 if go |
| Physics reach (ESTIMATE, expected 95% CL, Sec. 6.1) | Λ = 3 keV, 3 ab⁻¹: ≈ 1.2 TeV (B = 0), 0.94-0.97 TeV (B = 30, δB/B = 0-20%), 0.57-0.76 TeV (×16, δB/B = 20%-0), ≲ 0.3-0.58 TeV (×256) | Λ = 3 keV: ≈ 0.72-0.87 TeV; Λ = 1 keV: ≈ 0.49-0.62 TeV | both, staged |
| What is novel vs ATLAS | PU 200 (none at μ > 50 anywhere [LM §1; EX §1.2]); a muon-system slow-pair L1 seed (P5; CMS L1DS/GMT, no ATLAS counterpart [EX §3.7]): an acceptance gain at m_Q ≲ 300 GeV and an independent β tag, **not** an ISR-free trigger (Sec. 10.1); MTD 1/β; BX/late-hit acceptance; high-mass reach | First CMS result; independent confirmation; analog strip dE/dx on every layer [2410.09164 Sec. 5] while ATLAS strips are binary ("strip SPs have no charge" [EX §1.0 item 1]); L1DS muon-stub channel (2024 data) [2601.20063] | all of S1, plus a **data-measured** random-coplanarity rate that turns the S1 extrapolation from simulation-only into data-anchored; keeps the S2 option open |
| Novelty lost to ATLAS | "first central-detector search"; generic coplanar + ML reconstruction | likely "first" (ATLAS ahead by ~1 yr of tooling) | same as S1/S2 |
| Cost (ESTIMATE) | G4 port 1-3 PM [ST §1C]; analysis 6-12 PM; CPU: Phase 2 ≈ 24-34 k core-h, ≈ 8-12.5 TB; Phase 3 full grid + alternates ≈ +53 k core-h, ≈ +11-19 TB; total ≈ 77-87 k core-h, ≈ 20-32 TB (`SAMPLE_REQUIREMENTS.md` §2, single source of these numbers) | all S1 tools + Run-3 geometry signal MC + full data-driven background + CMS review: ~2-3 FTE × 2-3 yr (ESTIMATE, typical LLP search); CPU for skim processing ~10⁴-10⁵ core-h (depends on skim size, DAS) | Stage A+B ≈ S1 cost; S2 cost only after the gate |
| Time to first result (ESTIMATE) | 12-18 months (late 2027 - early 2028) | 30-40 months (2029-30) | Stage-B note 12-18 months; S2 result 2029-30 if launched |
| Data access | Phase-2 MC only: official PU-200 (TT verified; Z(νν), W, QCD, MinBias to check in DAS [ST §1C]) + private signal and PU samples | Run-2/3 data with hits: `EXOHighMET` RAW-RECO / `EXOMONOPOLE` cluster skims if produced (C7), else RAW from tape; ZeroBias RAW; NoBPTX; Cosmics; L1Scouting (2024) | S1 needs + a slice of S2 data (CRs and zero-bias only, blinded SR) |
| Main risks | ATLAS publishes first and possibly adds an ITk projection (R1b); a projection carries less weight than data; PU-200 background unknown (R4) | lose the race to ATLAS (R1); Phase-1 strip/pixel timing for late hits (UNVERIFIED); manpower (R6); a full data-driven background at 10⁻⁸ per-event fake rates | coordination overhead; gate discipline |
| Fit to a small USFQ team | good | hard without partners | good; scales with partners |

### 6.3 Recommendation [D5, PROVISIONAL until the user decides Q1]
**S3, staged.** Reasons:
1. All three scopes need the same critical-path items: quirk Geant4 in CMSSW, a hit dumper, a plane finder, a GNN, and an answer to the late-hit question. Stage A builds them once.
2. The biggest unknown is the PU-dependent random-coplanarity rate (R4) [RV-F §6; EX §4]. Run-3 zero-bias and MET-skim data can **measure** it at the Run-3 pile-up and anchor the PU-200 extrapolation. No simulation-only projection can do that.
3. A head-on Run-3 race (S2 first) starts about a year behind ATLAS. ATLAS fixed its Geant4 quirk simulation in Aug 2026 and already has an internal contour [EX §1.0 items 1, 3]. Committing CMS manpower to S2 before knowing (i) whether a CMS-internal effort exists (Q2; CDS/CADI not searched [EX §1.1 item 1]) and (ii) the measured background is premature.
4. S1 alone leaves the strongest CMS-specific asset unused: analog strip dE/dx in Run 3. It also leaves the projection unanchored by data.

Gate G-S2 criteria (month ~9; proposed, to be confirmed by the user):
- (a) the quirk G4 port is validated (Sec. 9.4 V1-V4);
- (b) the measured Run-3 random-plane rate allows an expected ≥ 3σ sensitivity at m_Q ≥ 400 GeV for Λ = 1-10 keV;
- (c) no CMS-internal duplicate effort exists, or one has been joined;
- (d) ≥ 2 FTE are secured;
- (e) no public ATLAS result that S2 could not improve on.

### 6.4 Novelty audit (plain statement)
- **Gone, or very likely gone:** "first LHC central-detector quirk search"; "first ML reconstruction of quirk pairs in a real experiment's simulation" (ATLAS MaskFormer/GNN on GNN4ITk dumps [EX §1.0]). The coplanar method itself is pheno-published [1708.02243], as is GNN tracking [2410.00269]. Neither was ever ours to claim [RV-T §5].
- **Survives (S1/S3):**
  1. the first study at μ = 200 (none above μ = 50 anywhere; the ATLAS effort has "no or low pile-up so far" [EX §1.0 item 1]);
  2. a muon-system slow-pair L1 seed (P5) on L1DS/GMT infrastructure ATLAS lacks [EX §3.5, §3.7]. It is **not** decoupled from ISR: the bound pair needs pT(QQ̄) ≳ 0.15 M_QQ̄/cosh η to reach the muon system with β ≳ 0.15 (Sec. 10.1). Its value is acceptance at m_Q ≲ 300 GeV and an independent pair-β tag;
  3. MTD 1/β tagging;
  4. the late-hit / BX acceptance analysis and a readout fix (new: no study in the literature beyond Knapen's 25 ns cut [1708.02243 Sec. IV]);
  5. mass reach beyond Run 2+3 **only if the PU-200 background is controlled**: ≈ 1.2 TeV if B ≈ 0, ≈ 0.95 TeV at the μ = 50 rate (δB/B ≤ 20%), and < 0.8 TeV (0.57 TeV with δB/B = 20%) if PU 200 scales B ×16 (Λ = 3 keV, 3 ab⁻¹, Sec. 6.1).
- **Survives (S2/S3):**
  1. the first CMS result and independent confirmation;
  2. strip analog dE/dx (CMS) vs binary strips (ATLAS), which matters most in the merged 10-30 keV regime where pixels alone give few dE/dx samples (inference);
  3. a Run-3 L1-scouting muon-stub quirk channel (P6; 2024 L1DS data [2601.20063]).
- **Disadvantage relative to ATLAS:** 3.8 T vs 2 T narrows the low-Λ end of the coplanar window (0.69 vs 0.58 keV at 500 GeV [TH Tab. 4.2b]).
- Confidence: medium. The ATLAS scope is inferred from code, not from a public statement [EX §1.0 item 4].

---

## 7. Benchmark and signal grid

[D3] Primary model E = (1,1)_{-1} Dirac fermion, N_IC = 2. It is the common benchmark of FASER, FASER2, Knapen, Li et al., Evans-Luty and Farina-Low [TH §1.2-1.3], so the CMS result overlays on all of them without reinterpretation. It has no charged-neutral splitting, and the pair is net neutral (clean coplanarity) [TH §1.3].

Alternates:
- **A1 Ẽ scalar** (spin and kinematics; σ ×1/11-1/18): 9 points.
- **A2 L doublet** (topology only: Q^± → Q^0 π^± with cτ ≈ 7 mm, ESTIMATE/UNVERIFIED): 2 points [TH §1.3, §7].
- N_IC = 3, 5 by rescaling [TH §1.3].

Target grid (Phase 3+) [TH §7]:
- m_Q ∈ {200, 350, 500, 750, 1000, 1250} GeV × Λ ∈ {0.3, 0.6, 1, 2, 5, 10, 20, 30} keV = 48 points.
- Justification:
  - 200 GeV is above every existing limit (FASER max 179 GeV);
  - 1250 GeV is the 3-event rate limit at 3 ab⁻¹ (Sec. 6.1);
  - Λ values sit on each regime boundary of Sec. 4.3: 0.3 (GNN regime / FASER gap), 0.6 (probes the coplanar transition: Λ_low = 0.54-0.81 keV for 200-1000 GeV, uncertain by ×1.8, Sec. 4.4), 1-5 (core), 10-20 (merging), 30 (single-HIP / FASER overlap).
- One LHE/GEN sample per mass, re-propagated for every Λ, since Λ enters only the transport [TH §3.5 step 1]. Λ-to-Λ differences are then free of generator fluctuations [D6].
- Events: ≥ 10k filter-passing events per point (minimum 5k; 20k at grid edges) [TH §7]. Rationale: ε ≈ 0.07 after the generator filter gives ~4% MC statistical precision; ML training needs ≥ 3k [2410.00269 Sec. IV via TH §7].
- Generator filter: pT(QQ̄) > 150 GeV [TH §3.5].

Phase-2 Exploration subset [D7]: m_Q ∈ {200, 500, 1000} × Λ ∈ {0.3, 0.6, 2, 10, 30} keV = 15 points.
- It spans every regime boundary and the timing transition (500 GeV is where the BTL arrival delay crosses 12.5 ns [TH Tab. 4.3]).
- S2 variant: masses {200, 500, 800} at 13.6 TeV, because the Run-3 reach is ≈ 0.8 TeV.

Validation samples (no PU, 5k each) [TH §7]:
- Λ = 0.05 keV (HSCP-like limit);
- Λ = 1 keV with B = 0 (analytic solution [2002.07503]);
- the causal-string (Athena) vs straight-string integrator comparison.

Stored per event [TH §7]:
- ME-scale, PDF and shower weights;
- true pair kinematics;
- **true SimHit time of every quirk hit**.

---

## 8. Sample inventory and background classification

Full per-scope tables, event counts, CPU/storage and DAS patterns are in `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md`. Summary:

### 8.1 Data
| Sample | Scope | Use | Status |
|---|---|---|---|
| Run-3 JetMET / MET PDs, `EXOHighMET` RAW-RECO skim (pfMET > 200 GeV ...) | S2/S3 | SR (blinded), CRs, random-plane rate in the MET stream | skim defined in CMSSW (C7); dataset existence **UNVERIFIED (DAS)** |
| Run-3 `EXOMONOPOLE` USER skim (pixel/strip clusters + pixel digis; paths `HLT_PFMET200_BeamHaloCleaned`, `HLT_Photon200`) | S2/S3 | lighter hit-level alternative, **with caveats**: (i) the config comment says it runs on MET/JetMET only from 2024 ("2021: on EGamma dataset only; 2024: on EGamma, MET and JetMET"), so 2022-23 MET coverage is UNVERIFIED; (ii) its MET path threshold (200 GeV) is higher than the standard `PFMETNoMu120`-type paths, so ε_trig is lower than P1 | as above |
| JetMET / MET PD **RAW** via pick-events (`edmPickEvents` on a MINIAOD/NANO pre-selection) | S2/S3 | **VR3** (offline MET 150-200 GeV, MET-triggered) and the MET 200-250 GeV transfer region; these are **not** in `EXOHighMET`, whose selection is pfMET > 200 GeV or the MET-ratio branch | PDs exist; RAW on tape (recall needed); size set by the pick list (O(10⁴-10⁵) events) |
| ZeroBias RAW and jet-triggered JetMET RAW at low MET | S2/S3 | **CR1** (MET 30-60 GeV, PU-dominated) | as above |
| Run-2 2017-18 `MET` PD `HighMET` RAW-RECO | S2 | luminosity extension (Phase-1 pixel era, as in 2410.09164) | `autoSkimRunII` (C7); DAS UNVERIFIED |
| ZeroBias RAW (Run 3) | S2/S3 | PU-hit overlay / embedding; random-plane rate vs nPV | standard PD (DAS) |
| NoBPTX (+ `EXONoBPTXSkim`), Cosmics | S2/S3 | non-collision backgrounds B8-B10 | autoSkim lists them (C7) |
| L1Scouting 2024 (DT stubs every BX) | S2/S3 | P6 muon-stub channel; P5 fake-rate measurement | used by 2601.20063; dataset name UNVERIFIED |
| Phase-2 data | — | none before ~2030 [EX §1.1 item 4] | — |

### 8.2 Monte Carlo
| Sample | Scope | Status |
|---|---|---|
| Quirk signal (E, Ẽ, L), private: Pythia8 HV `ffbar2EvEvbar` (Ngauge = 2, E_v stable, fragment off) or MG5 + home-made UFO; quirk G4 transport; FEVTDEBUG | all | **must produce**; blocked by the G4 port [ST §1A, §1C] |
| Phase-2 PU-200 ttbar GEN-SIM-DIGI-RAW-MINIAOD (`Phase2Spring24DIGIRECOMiniAOD`, D110) | S1/S3 | path VERIFIED(api) in CMSSW test configs [ST §1C] |
| Phase-2 Z(νν)+jets, W(ℓν)+jets, QCD-HT, MinBias / premix library at PU 200 | S1/S3 | DAS check; private production if missing [ST §3.1] |
| Private neutrino-gun + `AVE_{50,140,200}_BX_25ns` PU-only | S1/S3 | producible now [ST §3.1 C-B1] |
| Run-3 Z(νν)+jets, W+jets, tt̄, QCD (13.6 TeV), hit-level tier or premix-reprocessable | S2/S3 | DAS check (`SAMPLE_REQUIREMENTS.md` §3) |
| Cosmics / beam-halo generators | all | packages exist [ST §1C] |
| **Public prototype**: Zenodo 17941765 (2410.00269 quirk hits, toy detector, no PU); ColliderML R1 (ODD, PU-200 hits; 7.33 M PU-only sub-events); Pythia8/MG5 + own fast propagator | all (Stage A) | VERIFIED(api) [ST §1B] |

[L2] The public prototype geometry is not CMS: ODD has a 3 T solenoid and ITk-like layers [ST §5 item 5]. Public numbers are for method development and μ-scaling only, never for the CMS sensitivity.

### 8.3 Background classification
[A3] **No SM process gives an irreducible background in the strict sense**: none produces two coplanar, mutually bending, slow, highly ionising tracks [RV-T §6]. The MET + ISR preselection stream is irreducible *at preselection* only. Its tracker-level contamination is reducible.

| Class | ID [EX §4] | Background | Mechanism | Rate reference |
|---|---|---|---|---|
| Irreducible at preselection | — | Z(νν)+jets; W(ℓν)+jets with a lost lepton; tt̄; QCD with fake MET | genuine or fake MET; provides the event in which a fake plane is found | **σ(Z→νν, pT^νν > 200 GeV) = 3.00 (+0.18/−0.17) pb measured at 13 TeV** [CMS, arXiv:2012.09254, abstract; fiducial definition in Sec. 6: "p_T^miss > 200 GeV without any other requirements"; re-read in cached PDF]. Scaled to **≈ 3.4 pb at 14 TeV** and ≈ 3.3 pb at 13.6 TeV (ESTIMATE: ×1.14 and ×1.09, the 14/13 and 13.6/13 ratios of the TH §2.3 DY σ at m_Q = 200-300 GeV, i.e. √ŝ ≈ 0.4-0.6 TeV; the qg vs qq̄ luminosity difference is neglected; W2 refines it with MG5). ⇒ ≈ 1.0×10⁷ Z(νν) events in 3 ab⁻¹. The ST §3.0 value (0.5-1 pb) and R1's (5-20 pb) are both superseded |
| Reducible | B1 | random PU-hit coplanarity (**dominant**) | unassociated hits land on a plane through the PV | 10⁻³ (4/8 layers), 6×10⁻⁵ (all layers) per event at μ = 50 [1708.02243 Sec. IV]; unknown at μ = 200 |
| Reducible | B2 | B1 ⊗ MET stream | as B1 in Z(νν)+jets | ~10⁻² fb at μ = 50 → ~30 events in 3 ab⁻¹ [1911.02223 App. A; EX §4] |
| Reducible | B3 | photon conversions | e⁺e⁻ pair, nearby hits | ~10 fb fiducial before selection [1708.02243 Sec. IV] |
| Reducible | B4 | nuclear interactions | SV at material radii | not published |
| Reducible | B5 | loopers / low-pT helices (incl. out-of-time BX−1) | many hits in few layers | not published |
| Reducible | B6 | δ-rays, split clusters, merged close tracks | 2 hits/layer along one track | not published |
| Reducible | B7 | collimated pairs (jets, Dalitz, τ 3-prong) | 2 close tracks | part of the μ = 50 rate [1911.02223 Sec. IV] |
| Reducible | B11 | SM slow HIPs (deuterons, fragments) | high dE/dx, short | small |
| Instrumental | B8 | beam halo | hits along z at fixed (r, φ) | 2.6 ± 0.2 ev / 586 h (stopped-particle selection) [1801.00359 Tab. 4] |
| Instrumental | B9 | cosmic muons | straight, out of time | 8.8 ± 3.1 ev / 586 h (same) [1801.00359 Tab. 4] |
| Instrumental | B10 | detector noise / hot channels | random clusters | pixel noise occupancy < 10⁻⁶ (spec) [Tracker TDR Tab. 4.4 via EX §3.1] |
| Instrumental | B12 | muon-system fakes (P5/P6) | BX misID, cross-BX combinations | per-stub BX misID < 1-6% [2601.20063 Sec. 6] |
| Instrumental (new) | B13 | out-of-time PU hits / BX misassignment | hits from BX±1 enter the readout window; a quirk's own late hits move to BX+1 | to be measured (OI-1) |

---

## 9. Selection and reconstruction approaches (≥ 2, qualitatively different)

Common preselection [D8]:
- trigger path P1 (or P1 ∪ P2 ∪ P5 at Phase 2, Sec. 10);
- offline MET ≥ trigger plateau;
- ≥ 1 ISR jet;
- lepton veto;
- good PV.

Then:
1. Run standard helix tracking; remove hits on good helices (pT > ~1 GeV, χ² good).
2. Run pattern recognition on the leftover hits plus the hits on bad-χ² tracks.
3. Event-level selection.

### 9.1 Approach (a): classical coplanar plane-finder + quirk-trajectory fit
- **Plane finder** (Knapen-style [1708.02243 Sec. III C]): seed planes through the PV with hit pairs from the outer and inner layers; collect hits with distance < Δs; require ≥ 2 hits in ≥ N_min layers; then O1, O2, O7, O8. The algorithm has amortised O(N) complexity and "may be sufficiently fast for implementation at the HLT" [1708.02243 Sec. III C].
- CMS adaptation:
  - 3D precision from the IT (4 barrel layers + disks) and the 3 PS layers only; 2S gives rφ only (σ_z ≈ 1.4 cm) [TH §4.2];
  - Δs cut scanned per Λ regime, since d ∝ m_Q/Λ⁴.
- **Trajectory fit**: fit the straight-string EoM (with B and mean dE/dx) to the plane hits. Free parameters: m_Q, Λ, pair momentum, phase. Uses the analytic first-order solution as a fast seed [2002.07503 Eq. II.4-II.21]. Outputs χ² (O6) and fitted (m_Q, Λ) for the interpretation.
- **Low-Λ extension** (0.3-0.6 keV): drop the Δs cut and use the trajectory fit directly on curvature-inconsistent hit sets (O3).
- **High-Λ category** (≳ 15-20 keV): a straight, "infinite-pT", ≥ 2× MIP track with no calorimeter match. Uses standard tracking plus dE/dx (O4).
- Event selection: cuts on O1-O8, each motivated by an N−1 plot (JFC Phase 3).

### 9.2 Approach (b): ML on hits (GNN / MaskFormer)
- **GNN edge classification** (Exa.TrkX style): track efficiency 71.9% (8-layer) and 79.0% (25-layer) at m_Q = 500 GeV, Λ = 500 eV, no PU [2410.00269 Sec. E, Tab. I]. Code: acorn (public, licence UNVERIFIED) or QuirkTracking-ML (no licence: needs author permission) [ST §1A].
- **MaskFormer / hepattn** (GPL-3.0) [ST §1A]: the same family the ATLAS group uses [EX §1.0 item 1]. It predicts a quirk-pair mask plus regressions (plane normal, log10(Λ²/m)).
- Inputs per hit: position, layer, cluster size, ToT/charge, time (MTD/BX flag), "on-helix" flag.
- Training:
  - signal from the full CMS simulation over PU 200 (Phase 2) or Run-3 PU;
  - background from PU-only and Z(νν)+jets samples;
  - train/validate/test splits per (m_Q, Λ) plus a **Λ-hold-out** test for interpolation robustness.
- **Event-level classifier** (BDT or small MLP) on high-level features O1-O8 plus the GNN score. This is the MVA required by JFC. Inputs must pass the Phase-3 data/MC χ²/ndf gate.
- [L3] ML-on-hits is CPU/GPU-heavy. HLT use is only an outline [2410.00269 Sec. VII]. Offline use only, unless P5 makes an HLT path necessary.

### 9.3 How (a) and (b) are compared [D9]
Same samples, same preselection, evaluated per grid point:
1. Pair-finding efficiency vs fake rate per PU-200 crossing (ROC). Working points at a fixed fake rate of 10⁻⁴ and 10⁻⁶ per event.
2. Expected 95% CL limit and expected discovery significance (Asimov / toys), with the full background model and systematics.
3. Robustness: performance vs μ (50/140/200), vs Λ hold-out, and under a ±10% material and hit-efficiency variation.
4. CPU per event (HLT relevance).
5. Data/MC agreement of the inputs in CRs.

The primary method is chosen in Phase 3 on (2), with (3) and (5) as veto criteria. The other method is kept as a cross-check, as JFC method parity requires. Prior expectation: (a) wins in the core window, (b) at 0.3-0.6 keV and under heavy PU.

### 9.4 Signal-simulation validation (prerequisite for both)
- V1: analytic solution, B = 0 [2002.07503].
- V2: plane thickness vs the formula [1911.02223 Eq. III.12], within the stated ×10 accuracy [2002.07503 App. C].
- V3: causal-string (Athena) vs straight-string integrator with the correct ŝ simultaneity. A wrong ŝ gives mm-level errors [2002.07503 Sec. VIII, Fig. 6].
- V4: FASER-style checks: track continuity, ≈ 2-MIP charge for merged pairs, timing [2607.26195 App. A].
- V5: comparison with the Zenodo 17941765 trajectories at common (m, Λ) points.

---

## 10. Trigger strategy

### 10.1 Phase-2 (S1) paths and efficiencies (ESTIMATE, nominal coplanar window, m_Q 200-800 GeV; P1-P3 values from EX §3.6 for 300-800 GeV) [EX §3.2, §3.6]
| Path | Definition | ε_trig | New development needed |
|---|---|---|---|
| P1 | L1 PuppiETmiss 200 (128 at 50%) GeV, 18 kHz [L1 TDR Tab. 4.1] → HLT MET 140 GeV, 228 ± 20 Hz [2211.03684 Tab. 2] | 0.08-0.12 | none (baseline) |
| P1' | P1 used down to the 50% point (pT(QQ̄) ≳ 130 GeV) | 0.13-0.18 | turn-on systematic |
| P2 | lowered L1 PuppiETmiss 170 (100) GeV, +42 kHz [L1 TDR p. 209] | 0.15-0.25 | menu negotiation (shared with compressed-SUSY / disappearing-track programmes) |
| P3 | Single PuppiJet 180 GeV OR P1 | +0.01-0.02 | none (HLT single jet 520 GeV is too high) |
| P4 | TkMuon / L1-HSCP seeds | ~0 for Λ ≲ 10 keV; unknown at large Λ | requires an L1 track; the straight-pair L1-track hypothesis is UNVERIFIED |
| **P5** | **new GMT seed "trackless slow straight muon"**: barrel DT/RPC stubs over ≥ 3 BXs, outward ordering, no L1-track requirement, high fitted pT; L1A issued for the inferred collision BX within the 12.5 µs latency | **0.08-0.20 (200 GeV), 0.05-0.13 (300), 0.03-0.08 (500), 0.01-0.04 (800)**; still needs ISR recoil (Sec. 10.1a) | **new L1 algorithm** (GMT firmware); rate ESTIMATE ≪ 1 kHz, UNVERIFIED [EX §3.5 item 3] |
| P6 | L1 scouting at 40 MHz, offline muon-stub analysis (no tracker hits) | as P5 | separate analysis; also measures the P5 fake rate |
| **Best: P2 ∪ P5** | | **≈ 0.2-0.3 at m_Q ≈ 200 GeV; ≈ 0.17-0.28 at 300 GeV; ≈ P2 + ≲ 0.03 (≈ 0.15-0.28) at 500 GeV; ≈ P2 (0.15-0.25) at ≥ 800 GeV** | v1 quoted 0.2-0.35 for 300-800 GeV, which double-counted the ISR recoil (Sec. 10.1a) |

#### 10.1a Pair kinematics of the muon-system seed (ESTIMATE; scratchpad `fix.py`)
- The two quirks are bound and reach the muon system at the **pair** velocity. The L1DS/GMT-HSCP windows need β ≳ 0.15; below that, "the particles mostly get stopped" and the efficiency goes to zero [2601.20063 Sec. 3, Fig. 4 text].
- So the pair momentum must satisfy |p_pair| ≥ 0.15/√(1−0.15²) × M_QQ̄ = 0.152 M_QQ̄.
- With M_QQ̄ ≈ 2γ* m_Q (TH §4.1 median γ* = 1.30/1.25/1.19 at 200/500/1000 GeV; 1.28 and 1.21 interpolated at 300 and 800 GeV) and |p_pair| = pT cosh η for barrel pairs (|η| < 0.83):

| m_Q [GeV] | M_QQ̄ [GeV] | pT(QQ̄)_min (η = 0.83 … 0) [GeV] | f(pT > pT_min) (A4 scaling) | ε(P5) = 0.5 × f × (0.5-0.9) |
|---|---|---|---|---|
| 200 | 520 | 58-79 | ≈ 0.30-0.45 (extrapolated below 100 GeV) | 0.08-0.20 |
| 300 | 768 | 85-117 | ≈ 0.21-0.29 | 0.05-0.13 |
| 500 | 1250 | 139-190 | ≈ 0.11-0.17 | 0.03-0.08 |
| 800 | 1942 | 216-295 | ≈ 0.05-0.09 (extrapolated above 200 GeV) | 0.01-0.04 |

- Factors: 0.5 = f(|η_pair| < 0.83) and 0.5-0.9 = ε_alg [EX §3.6]. f(pT > X) uses the A4 anchors f(> 200) = 0.10 [1708.02243 Tab. I], f(> 130) ≈ 0.18 and f(> 100) ≈ 0.25 [EX §3.6, ESTIMATE].
- **Overlap with P2** (L1 PuppiETmiss 170 GeV plateau, 100 GeV at 50%): for m_Q ≳ 400 GeV the P5 region (pT ≳ 140-190 GeV) lies inside the P2 turn-on/plateau. P5 then recovers only events lost to L1-MET resolution in the turn-on: ≲ +0.03 absolute (ESTIMATE). At m_Q ≈ 200 GeV, P5 reaches pT(QQ̄) ≈ 60-80 GeV, where P2 is < 50% efficient, and adds ≈ +0.05-0.09. At 300 GeV (pT ≳ 85-117 GeV) the unique gain is only ≈ +0.02-0.03 (R2 C3).
  - Caveat: the L1 TDR "170 (100)" notation gives the offline 95% point and the **online** threshold. Treating the online threshold as the offline 50% point (inherited from EX §3.6) is an approximation; W2/W10 replace it.
- [A8] The two-quirk DT segment response (two charges ≲ 1 mm apart) and arrival within the L1DS ≤ 4-BX window are folded into ε_alg. Both are UNVERIFIED (EX §3.6 open items).
  - The β ≳ 0.15 threshold comes from single-HSCP masses [2601.20063]. A pair at β ≈ 0.15 carries only (γ−1)M ≈ 0.011 M of kinetic energy (≈ 14 GeV at m_Q = 500 GeV) and loses ≳ 10× MIP per charge in the calorimeters and solenoid. The effective threshold for the pair may be higher (R2 C7). W2/W3 compute the range-out explicitly.
- **Value of P5 (revised):** (i) acceptance gain at low m_Q; (ii) an **independent pair-β measurement** in the muon system, i.e. a second slow tag for background rejection and a trigger-efficiency cross-check; (iii) a template for the L1DS P6 analysis. The headline Phase-2 trigger gain comes from **P2** (lower L1 MET), not from P5.

Related numbers:
- HLT quirk path (needed only with P5 or P2): plane finder or GNN on L1-seeded events. ~0.6% of the farm at 18 kHz and 1 s/event/thread (ESTIMATE) [EX §3.5 item 7]. The arithmetic was re-checked: 37 MHS06 / (1680 HS06 / 128 threads) ≈ 2.8 M thread-equivalents; 18 k / 2.8 M ≈ 0.64%.
- [A4] The ISR-recoil scaling ε(pT > 130) ≈ 1.8 ε(pT > 200) and ε(pT > 100) ≈ 2.5 ε(pT > 200) is an ESTIMATE [EX §3.6]. Phase 2 replaces it with MG5/Pythia + Phase-2 L1 emulation (`L1Trigger/Phase2L1GT`).

Unavailable handles: L1 dE/dx (OT binary, pixels not in L1) and L1 MTD timing [EX §3.5 items 5-6].

### 10.2 Run-3 (S2) paths
- Unprescaled PF-MET HLT paths. Pattern names are VERIFIED(api) in the `EXODisappTrk`/`EXOMONOPOLE` skim configs: `HLT_PFMET*_PFMHT*_IDTight`, `HLT_PFMETNoMu*_PFMHTNoMu*_IDTight`, `HLT_PFMET200_BeamHaloCleaned`. Thresholds per year are UNVERIFIED.
- Expected ε_trig ≈ 0.10 (Run-2-like; 1708.02243 Tab. I).
- The 2024 L1DS data allow a P6-type muon-stub analysis on 3.7 fb⁻¹ [2601.20063].

### 10.3 What new trigger development is needed (S1/S3)
1. Quirk stub formation and L1-track behaviour (`L1TrackNtupleMaker`), especially in the large-Λ merged regime [EX §3.3].
2. A P5 GMT emulator prototype, plus its fake rate from L1DS data.
3. A P2 rate case.
4. HLT timing of the plane finder.
5. A BX+1 readout or delayed-window option (OI-1).

### 10.4 OPEN ITEM OI-1: late hits and BX assignment (explicit)

**Facts:**
- One consistent velocity set is used: median pair v_T = 0.38/0.19/0.10 (m_Q = 200/500/1000 GeV, pT(QQ̄) = 250 GeV), from the TH t_BTL column (C2).
- Median delay at the BTL radius is 6/16/33 ns. Only 2% (0%) of 500 (1000) GeV pairs have BTL delay < 12.5 ns (ESTIMATE) [TH Tab. 4.3].
- **Layer by layer** (Sec. 4.2 table, median pair, η = 0):
  - 200 GeV: everything in time;
  - 500 GeV: 2S L3 lost (15.4 ns), 2S L2 marginal (12.0 ns);
  - 1 TeV: PS L3 (15.0 ns) and all 2S layers (≥ 19.7 ns) lost, while the IT survives (IT window [−5, 20) ns, IT L4 delay 4.5 ns).
  - At pT(QQ̄) = 500 GeV the 1 TeV pattern becomes the 500 GeV one (only 2S L3 lost).
- The OT front ends are binary and BX-tagged. The sampling phase and hit-detect mode are not specified in the TDR [EX §3.4b].
- The ETL TDC window is 6.25 ns [MTD TDR Sec. 3.3.6 via EX §3.4b]. The BTL window is UNVERIFIED.
- **CMSSW simulation (C8):** OT hits with toa = tof − |r|/c outside ±12.5 ns are not digitised. IT pixels keep [−5, 20) ns.

**Consequences:**
- (i) Default-simulated high-mass signal loses outer-OT hits, i.e. the lever arm and the stubs. The loss looks like inefficiency, not like BX+1 hits.
- (ii) In real data the hits may appear in BX+1, which is not read out unless a second L1A is issued.
- (iii) MTD timing (O5) may be unavailable for exactly the slow pairs it should tag.

**Resolution plan (owner: this analysis + tracker/MTD DPG contacts):**
1. Phase 2, week 1-4: from FEVTDEBUG truth, histogram the SimHit toa per layer vs (m_Q, Λ, pT(QQ̄)). This needs no detector-model assumption.
2. Re-digitise with (a) default windows, (b) widened windows, (c) 2S `SampledMode`/`LatchedMode` (`HitDetectionMode` 1/2, which exist in the config). Quantify the efficiency vs m_Q under each.
   - In SampledMode the CBC pulse is sampled at the BX time instead of a ±12.5 ns square window (`SSDigitizerAlgorithm.cc` `select_hit_sampledMode`), so late, large-charge hits may survive.
   - The default SquareWindow is therefore probably the **pessimistic** case. The real front-end behaviour (step 3) is what counts.
3. Ask the tracker DPG for front-end delay-scan results (CBC/SSA/MPA in-time efficiency vs injected delay), and ask the MTD DPG for the BTL TOFHIR TOA range [EX §3.4b "required studies"].
4. Ask the L1/DAQ experts about the Phase-2 trigger rules for consecutive L1As (BX and BX+1) [EX §3.4b, UNVERIFIED].
5. Turn the result into (a) a time-window systematic (Sec. 12), and (b) if large, a readout proposal: BX+1 readout for P5-seeded events. This is itself an S1 novelty.
6. For S2 (Run 3), repeat the toa study for the Phase-1 pixel/strip readout (strip APV timing windows UNVERIFIED).

[L4] Until OI-1 is resolved, all efficiencies for m_Q ≳ 500 GeV are quoted with and without the late-hit loss.

---

## 11. Background estimation strategy

### 11.1 Principle
[A5] The search is **not background-free** [RV-F §4; 1911.02223 App. A]. With σ(Z→νν, pT > 200 GeV) ≈ 3.4 pb at 14 TeV (Sec. 8.3), the 3 ab⁻¹ MET stream holds ≈ 1.0×10⁷ Z(νν) events, or ~2×10⁷ including W/tt̄/QCD (ESTIMATE). The required per-event fake probability after all cuts is therefore **≲ (1.5-3)×10⁻⁸** for < 0.3 expected events (ESTIMATE). The v2 "3×10⁻⁹" branch is dropped (R2 B1). That rate cannot be simulated directly.
- [D10] Factorise: f_tot = f_plane(μ) × f_Δs × f_dE/dx × f_MET-plane × f_timing. Measure each factor on samples with ≥ 100 surviving candidates and fit the tails [ST §3.0].
- [A6] The factorisation requires the factors to be uncorrelated. This is tested in the VRs below; non-closure becomes a systematic.
- [D11] Predict B1+B2 with **two independent data-driven methods** and use their difference as a shape/normalisation systematic.

### 11.2 Methods
| Method | Targets | How | Template |
|---|---|---|---|
| M1 **Inverted coplanarity sideband + transfer factor** | B1, B2, B7 | Plane candidates with Δs (or trajectory χ²) in a sideband above the SR cut; transfer factor θ to the SR measured in a low-MET (30-60 GeV), PU-dominated region | spurious-track method [2309.16823 Sec. 8.2, Eq. 6] |
| M2 **Hit mixing / embedding from zero-bias** | B1, B2 | Overlay hits of zero-bias events (other BX, matched nPV) onto MET-stream events from which the plane-finder hits were removed; random-plane rate vs nPV; extrapolate in nPV (Phase 2: to μ = 200) | EX §4 B1(b) |
| M3 **ABCD** in (Δs, N_layers with 2 hits) or (Δs, Δφ(MET, n̂)) | B1, B2 | N_D = N_B N_C / N_A with a bias correction from VRs | mass method [2410.09164 Sec. 6.2, Eq. 9] |
| M4 **Out-of-time / non-colliding bunches** | B5 (out-of-time loopers), B8, B9, B10, B13 | bunch-train tails, empty BXs, NoBPTX PD; cosmic runs; inverted timing | 1801.00359 Sec. 6; 2601.20063 Sec. 7 |
| M5 **Material map** | B3, B4 | conversion and NI-vertex CRs (inverted SV veto); Z → µµγ conversions as a candle | EX §4 B3-B4 |
| M6 **Tag-and-probe** | B6 | Z → µµ: per-layer probability of a second nearby hit along an isolated muon | EX §4 B6 |
| M7 **Invisible-Z normalisation** | B2 | Z(µµ)+jets with muons removed ("MET-emulated"); repeat the hit search after removing muon hits | standard CMS invisible-Z technique [EX §4 B2] |
| M8 **Asynchronous ordering** | B12 (P5/P6 only) | unphysical stub-time orderings model the background; non-colliding VR | 2601.20063 Sec. 7 |

### 11.3 Control and validation regions
- CR1: low MET (30-60 GeV), PU-dominated. Sets θ for M1. **Data source:** ZeroBias RAW and jet-triggered JetMET RAW. CR1 is not in the MET skims (Sec. 8.1).
- CR2: Z(µµ)+jets with muons removed (M7).
- CR3: conversion/NI-enriched (M5).
- CR4: non-colliding BXs, NoBPTX, cosmic runs (M4).
- **VR1:** inverted Δφ(MET, n̂). Same plane quality as the SR, but the plane is misaligned with the MET; signal-depleted by O7 [1708.02243 Sec. IV].
- **VR2:** unphysical topologies: planes not containing the PV; planes with hits only in outer layers; inward time ordering [EX §4 item 4].
- **VR3:** intermediate MET (150-200 GeV, below the SR plateau), covering the interpolation between CR1 and the SR [CONV pitfall "blind spot in VR coverage"].
  - **Data source:** MET/JetMET RAW via pick-events, since `EXOHighMET` starts at pfMET > 200 GeV.
  - [D18] If RAW access for 150-200 GeV proves impractical, use a fallback VR3' = MET 200-250 GeV, **inside** the skim, with the SR moved to MET > 250 GeV. The cost of this fallback in signal ε_trig is evaluated in Phase 2 before choosing.
- **VR4:** nPV slices. Test the μ-extrapolation of M2 within Run-3 data (low vs high nPV) before trusting PU 200.

Closure requirement [CONV item 1]: VR p > 0.05. Failure is Category A.

### 11.4 Blinding [D12]
- SR = plane candidates passing the final Δs, N_layers, dE/dx and Δφ cuts in the MET stream.
- They stay hidden until the JFC Phase 4b (10% subsample) and 4c.
- Zero-bias, CR1-CR4 and VR1-VR4 are open.
- For S1 (MC only), "blinding" means that cuts are optimised on expected sensitivity only [CONV pitfall].

---

## 12. Systematic plan (every source in `conventions/search.md`)

Sizes come from citations or are "to be measured in Phase N". No arbitrary inflation.

| Convention category | Source | Decision | Planned treatment and size |
|---|---|---|---|
| Signal modelling | Signal cross-section theory (μR/μF, higher order) | **Will implement** | NNLL scale ≤ 1% [TH §2.3, WG json]; fermion K-transfer / EW-scheme ±5% (ESTIMATE) [TH §2.4]; IC Sommerfeld +5 to +15% one-sided (ESTIMATE) [TH §2.4]. [D13] Theory-σ uncertainties are shown as a band on the prediction, not in the likelihood, for σ limits; they are propagated into the mass limits. |
| Signal modelling | Signal acceptance: generator / PDF | **Will implement** | PDF4LHC21 replicas on acceptance (to be measured in Phase 3); LO-MLM(0-2j) vs NLO-FxFx at 2 masses [TH §5] |
| Signal modelling | Signal acceptance: ISR | **Will implement** | ME μR/μF ×½/×2, Pythia ISR scale ×½/×2, matching scale. Expected 10-20% (ESTIMATE) [TH §5]; reference: FASER ≈ 25% for shower-scale variation of a forward acceptance [2607.26195 p.5, re-checked; C1]. To be measured in Phase 3. |
| Signal modelling | Signal shape (alternative MC / parameter variations) | **Will implement** | (i) Quirk-dynamics modelling: Athena causal string vs straight-string integrator; few % in the core window, larger below 0.6 keV (ESTIMATE) [TH §5]. (ii) Energy-loss model: dE/dx scale ±5-10% (UNVERIFIED, HSCP-typical) [TH §5]. (iii) Material budget ±5-10% (ESTIMATE) [TH §5]. (iv) **Hit-time / readout-window modelling**: vary window edges and hit-detect mode (OI-1); potentially dominant for m_Q ≳ 500 GeV [TH §5]; to be measured in Phase 2. (v) Spin (E vs Ẽ) is a separate model, not a nuisance. (vi) B-field map: negligible (thickness ∝ B, so a 0.1% map error gives 0.1%) [TH §5]. (vii) Glueball ε: **not applicable** for Λ ≤ 30 keV (< 0.1% of the pair energy radiated, ESTIMATE [TH §3.3]); a check with ε ∈ [0.03, 0.3] is documented. |
| Background estimation | Irreducible-background normalisation (CR-constrained) | **Will implement** | Z(νν)+jets via M7 (CR2) and M1/M2 transfer factors; size from CR statistics + VR non-closure, to be measured in Phase 3. Reference sizes: spurious-track 5-52% (long), 6-28% (short) [2309.16823 Tab. 7]. |
| Background estimation | Background shape (alternative methods / forms) | **Will implement** | M1 vs M2 difference; nPV-extrapolation form (power law vs exponential) [D11]; ABCD bias correction (ref.: applied 0× or 2×, ±100% [2410.09164 Sec. 6.2]); asynchronous-subset variations for P5/P6 (ref. 5-75% [2601.20063 Tab. 2]). To be measured in Phase 3. |
| Background estimation | MC statistics (Barlow-Beeston) | **Will implement** | Barlow-Beeston-lite per bin for signal templates and any MC-derived term; target ≤ 5% with 10k events/point; reference FASER 6% (up to 28% at small Λ) [2607.26195 p.5; C1] |
| Detector & reconstruction | Object calibration: energy scale / resolution | **Will implement** | JES/JER and MET (ISR recoil). Reference 0-24% [2309.16823 Tab. 7]; to be measured in Phase 3. |
| Detector & reconstruction | Object calibration: efficiency scale factors | **Will implement** | (i) MET trigger turn-on: reference < 2% [2502.06694 Sec. 5.5], 0-4% [2309.16823 Tab. 7]. (ii) P5 muon-timing analogue: up to 30% [2410.09164 Sec. 7]. (iii) Per-layer hit efficiency and cluster position resolution (tracker DPG); to be measured in Phase 2/3. (iv) dE/dx (ToT/strip) calibration: reference 3-8% [2309.16823 Tab. 7]; F^Pix 0.5%, G^Strips < 1% [2410.09164 Sec. 7]. (v) MTD time calibration (S1): to be measured in Phase 3. (vi) Pile-up reweighting on signal: reference 0-2% [2309.16823 Tab. 7], < 1% [2410.09164]. |
| Detector & reconstruction | Luminosity | **Will implement** | 2017-18: 2.0% [2410.09164 Sec. 7]; Run 3: from the CMS lumi POG (to be looked up in Phase 4a per JFC "published-input lookup"); HL-LHC: ~1-1.5% target (UNVERIFIED) [TH §5], to be taken from the CMS projection conventions in Phase 4a |
| Detector & reconstruction | Beam energy / ISR for e⁺e⁻ | **Not applicable** because this is pp (the convention replaces it with PDF + pile-up + luminosity, all covered above) | — |
| Theory inputs | QCD scale (independent μR, μF) | **Will implement** | 7-point variation on acceptance (Phase 3); on σ ≤ 1% (NNLL) [TH §2.3] |
| Theory inputs | PDF | **Will implement** | PDF4LHC21: ±3.7% (200 GeV), ±6.6% (500), ±11.9% (800), ±18.5% (1000), ~±25% (1200, extrapolated) [TH §2.3] |
| Theory inputs | Fragmentation (string vs cluster) | **Not applicable to the quirk system** because colour-neutral quirks are not hadronised (stable E_v, `fragment = off`) [TH §3.5; ST §2]. ISR-jet fragmentation enters only through MET/JES (covered). A Herwig-vs-Pythia ISR-recoil comparison is done as a cross-check [D14]. | — |

Quirk-specific additions (beyond the convention list):
- **Λ convention and N_IC** are definitions, not nuisances [TH §5].
- **PU-200 hit-density modelling** (S1) is treated through the background method (M2 nPV scan) and through signal efficiency vs μ.

Required validation checks [CONV 1-6], committed:
1. VR closure, p > 0.05;
2. signal injection at 0, 1, 2, 5× (bias > 20% investigated);
3. NP pulls (> 2σ investigated);
4. impact ranking (expected leaders: background transfer factors, time-window modelling, ISR);
5. goodness of fit with toys;
6. look-elsewhere: SRs are fixed per Λ-regime category, so report local significance per category and a global trial factor over the categories.

---

## 13. Reference analyses (systematic programmes and published results)

Selection [EX §2]: three CMS analyses, each teaching one technique the quirk search must reproduce. Two quirk-specific results serve as physics comparison targets (§6.8 of the JFC methodology).

| | (A) CMS HSCP dE/dx, CMS-EXO-18-002, arXiv:2410.09164, 101 fb⁻¹ (2017-18) | (B) CMS HSCP with L1 scouting, CMS-EXO-25-010, arXiv:2601.20063, 3.7 fb⁻¹ (2024) | (C) CMS disappearing tracks, CMS-SUS-21-006, arXiv:2309.16823, 137 fb⁻¹ |
|---|---|---|---|
| Teaches | anomalous-track selection; data-driven pass/fail + ABCD on uncorrelated variables | multi-BX slow-particle reconstruction; "unphysical ordering" background | spurious tracks from random hit alignment (≈ random coplanar PU hits) |
| Trigger | single µ pT > 50 GeV; ε 0.86 (DY stau 557 GeV), 0.11 (gluino 1.8 TeV) [Tab. 2; re-checked] | none (L1DS, orbit prescale 15) | HLT pT^miss > 100-120 GeV (> 97%); single e/µ |
| Background method | ionisation pass/fail fit (Eq. 8); mass-method ABCD (Eq. 9) with VR bias correction | asynchronous orderings; non-colliding VR | sideband CRs with transfer factors κ (genuine) and θ (spurious) (Eq. 4, 6) |
| Systematic programme | text only (Sec. 7): muon-trigger timing up to 30% (dominant); G^Strips < 1%; F^Pix 0.5%; p resolution 10%; µ SFs < 1%; lumi 2.0%; PU < 1%; bias correction ±100% (mass method) | background shape 5-75% (Tab. 2), constrained to ~50%; signal normalisation via DY(µµ) ~2-3% | Tab. 7: signal selection 10-17%, lumi 1.6%, JES/JER 0-24%, b-tag 0-4%, scales 0-2%, ISR 0-3%, PU 0-2%, trigger 0-4%, dE/dx 3-8%; background genuine 20-104%, spurious 5-52% |
| **Published numerical results** (comparison / validation targets) | stau (GMSB SPS7) excluded up to 0.85 TeV; gluino R-hadrons up to 2.06 (ionisation) / 2.08 TeV (mass method); DY τ′ with **Q = 1e excluded below 1.02 TeV (ionisation method) and 1.14 TeV (mass method); Q = 2e below 1.32 / 1.41 TeV** [2410.09164 l.986-987 and Tab. 3, re-read; corrected in v2]. The Q = 1e τ′ has the E = (1,1)₋₁ quantum numbers, so 1.02-1.14 TeV is the natural Λ → 0 (helical-track) anchor for the Q10 reinterpretation. Two caveats (R2 C4): (i) it is a limit for N_IC = 1; the N_IC = 2 quirk has 2× the σ, so the equivalent limit is roughly +0.1 TeV higher (ESTIMATE); (ii) it applies only where ℓ_max ≫ detector size, i.e. Λ ≲ 0.1 keV, not at the 0.3 keV grid edge (ℓ_max ≈ 25-80 cm [TH Tab. 4.2a]) | fiducial σ upper limits as low as 3.5 fb for |η| < 0.83, pT > 500 GeV, in β bins; unique sensitivity at 0.15 ≲ β ≲ 0.5 [2601.20063 Sec. 10] | pure wino (higgsino) charginos excluded up to 650 (190) GeV [2309.16823 results text, re-read in cached PDF]; T6tbLL charginos to 850 (1210) GeV at cτ = 10 (200) cm |
| Lesson for C001 | ABCD on (Δs, orthogonal variable); dE/dx in strips is a Run-3 asset | P5/P6 pathway and M8 | M1 transfer-factor method for B1 |

Secondary: ATLAS dE/dx + ToF, arXiv:2502.06694, 140 fb⁻¹ [EX §2]:
- E_T^miss trigger, 20% to > 95% efficiency;
- template-correlation non-closure 5-23%;
- di-track closure 10-40%;
- E_T^miss trigger < 2%;
- β_ToF terms 3-10%.

Non-collision reference: CMS stopped particles, arXiv:1801.00359. Halo 2.6 ± 0.2 and cosmics 8.8 ± 3.1 events in 586 h (2016) [Tab. 4].

**Quirk physics comparison targets (binding for the result-comparison step):**
- FASER observed (1,1)_{-1}, N_IC = 2: 57/72/113/149/163/179/173 GeV at Λ = 0.3/0.5/1/1.7/3/10/30 keV [HEPData ins3184325 t2, via TH §6.3].
- Knapen et al. projection: EW quirks up to 650 GeV (5 events, 300 fb⁻¹, μ = 50) [1708.02243 abstract].
- Sha et al.: N > 3 for m_Q ≲ 700 GeV, Λ ≲ 5 keV, 300 fb⁻¹, no PU [2410.00269 Sec. VI].
- Farina-Low: 150 GeV at 100 eV, none at 1 keV [1703.00912 Tab. II].
- D0: 107 GeV [1008.3547].
- FASER2 projection: 1.0 TeV discovery for E at 3 ab⁻¹ [2404.13814 Sec. 7].
- **Closure test (binding, re-planned after review B7).**
  - Primary target: Knapen's **10⁻³** rate (plane with ≥ 1 hit in 4/8 layers, μ = 50) [1708.02243 Sec. IV]. Use ≥ 10⁵ independent μ = 50 crossings (≥ 100 expected fakes, ±10% statistical): the full ColliderML PU pool of 7.33 M sub-events gives 1.47×10⁵ crossings without reuse.
  - The **6×10⁻⁵** all-layer rate (only ≈ 9 expected fakes in 1.47×10⁵ crossings) is a secondary target, reached by two independent routes:
    - (i) the factorised estimate f(all) = f(4/8) × P(remaining layers | 4/8 candidate), measured on the ≥ 100 4/8 candidates (D10);
    - (ii) resampled crossings (≈ 12× pool reuse to reach 1.7×10⁶ crossings). Its validity is documented by showing that the fake rate does not depend on the sub-event overlap fraction between crossings.
  - Closure passes if both agree with Knapen within the statistical uncertainty times a geometry-transfer factor, which must be stated beforehand (ODD 3 T vs Knapen's 2 T ATLAS-like toy, L2).
  - Details in `SAMPLE_REQUIREMENTS.md` §0-§2.

**Method parity [D15].**
- References for reconstruction: Knapen (cut-based plane finder) and Sha (GNN). We implement both (Sec. 9).
- References for statistics: FASER (CLs with CMS Combine [2607.26195 p.5-6, re-read]); the disappearing-track search (counting in 49 SRs); L1DS HSCP (pT-shape fit).
- We commit to the same or better:
  - multi-category counting with toys as primary (Sec. 14);
  - a shape fit in the event-classifier score as a cross-check. A shape fit is not primary because the signal has no peaked observable and the expected background is O(0-30) events (Sec. 8.3).

---

## 14. Technique selection (statistics)

- **Framework:** CMS Combine (as used by FASER for quirks [2607.26195 p.5-6]); pyhf for public-prototype studies [ST §4].
- **Limits:** CLs [CONV] with the profile-likelihood-ratio test statistic, μ ≥ 0, one-sided.
- **Discovery:** q0 with q0 = 0 for μ̂ < 0 [CONV].
- **Model [D16]:** binned likelihood over K signal-region categories plus CR bins that constrain the background nuisances (M1, M7).
  - Categories by reconstruction regime: low-Λ (trajectory/GNN), core coplanar, high-Λ straight pair.
  - Within each, bins in N_layers and dE/dx (and β in S1).
  - Signal templates per (m_Q, Λ).
  - **Cut-and-count per category vs shape:** counting per category is primary (expected B per category O(0-10)); a shape fit in the event-classifier score is the cross-check (method parity, D15).
- **Low counts:** expected counts < 5 per bin make asymptotics invalid. [D17] Use toys (Combine HybridNew) for every quoted limit and significance, with asymptotics only for scans. The two are cross-checked at ≥ 3 grid points [CONV pitfall].
- **Signal injection:** 0, 1, 2, 5× expected; bias > 20% is investigated [CONV item 2].
- **Interpolation in (m_Q, Λ):** efficiency maps from the full-sim grid, interpolated in log Λ. The interpolation is validated at hold-out points from the fast-propagator scan [TH §7].
- **S1 projection specifics:** Asimov expected limits and 5σ discovery contours at 1 and 3 ab⁻¹. Background from the factorised PU-200 model with its systematic band; trigger scenarios P1 / P2 / P2 ∪ P5 and late-hit scenarios with/without loss shown separately.

---

## 15. Competition and timeline

Competition (ESTIMATE unless cited) [EX §1.2]:
| Who | Region | Expected |
|---|---|---|
| ATLAS Run-2/3 ID quirk search (active; Athena 24.0 G4 fixes Aug 2026; MaskFormer pair finder; internal contour) | ~0.1-5 keV, up to ~0.5-0.65 TeV | 2028-29 (ESTIMATE) [EX §1.0 item 6] |
| FASER full Run 3 (~330 fb⁻¹), then Run 4 (~770 fb⁻¹, approved) | 0.1-60 keV, up to ~0.2-0.4 TeV | 2027-28; ~2034 [EX §1.1 item 4] |
| LHCb VELO | coloured quirks only | 2028+ (UNVERIFIED) |
| FASER2 / FPF (not approved) | up to 1-1.3 TeV | ≥ 2038 [EX §1.1 item 5] |
| CMS internal | **unknown** (CDS blocked; CADI not searched) | Q2 |

Proposed S3 timeline (from 2026-10, ESTIMATE):
| Month | Milestone |
|---|---|
| 0-1 | DAS/CADI checks; contact with EXO-LLP conveners; public prototype environment; downloads (Zenodo, ColliderML subsets) |
| 1-3 | Fast propagator + CMS-like parametric geometry; reproduce Knapen μ = 50 rates on ColliderML/ODD overlays; first μ = 200 random-plane rates (public); G4 port begins |
| 3-6 | G4 port validated (V1-V5); first CMS Phase-2 signal at PU 0 and PU 200; OI-1 toa study; stub/L1 study; Run-3 zero-bias random-plane rate vs nPV (CRs only) |
| 6-9 | Phase-2 Exploration complete (JFC Phase 2); approach comparison begins; **gate G-S2** |
| 9-18 | S1 deliverable (CMS projection note); if go: S2 Run-3 analysis (Phase 3-4 on data, target 2029-30) |
| ≥ 2030 | Phase-2 data-taking; trigger (P2/P5) and readout (BX+1) proposals in place before Run 4 menus freeze (date UNVERIFIED) |

---

## 16. Risk register

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | ATLAS publishes a Run-2/3 quirk search first (2028-29) | high / high for S2 novelty | S3 staging; emphasise CMS-specific assets (strip dE/dx, P5/P6, PU 200, MTD, BX) |
| R1b | ATLAS also releases an ITk/HL projection | medium / medium for S1 | move fast on S1 Stage B; the trigger/BX/MTD content is CMS-specific |
| R2 | Quirk G4 port slips (MT safety, stacking-action integration, CMS field/stepper, looper killers) [ST §1C; TH §3.5] | medium / high (critical path) | fast propagator injecting quirk hits as a fallback; find a CMS SimG4 co-developer; port Athena's `standalone/` first |
| R3 | **Late-hit / BX loss** kills high-mass acceptance: default simulation drops OT hits > 12.5 ns late (C8). At pT(QQ̄) = 250 GeV this is 2S L3 at 500 GeV, and PS L3 + all 2S at 1 TeV (Sec. 4.2) | high / high above ~500 GeV | OI-1 plan (Sec. 10.4); report both scenarios; SampledMode check; a readout proposal is itself a result |
| R4 | Random-coplanarity rate at PU 200 too large (∝ occupancy^k; ×16-256 from μ = 50, ESTIMATE [ST §3.0]). Reach falls from ≈ 1.2 TeV (B = 0) to 0.97 / 0.76 / 0.58 TeV (B = 30 / ×16 / ×256, statistics-only), and to 0.94 / 0.57 / 0.29 TeV with δB/B = 20%, at Λ = 3 keV (Sec. 6.1) | medium / high | MTD timing, dE/dx, MET-plane alignment, trajectory χ²; data-anchored μ scan (VR4) |
| R5 | Trigger stays at ε ≈ 0.1 (P2 not adopted). P5 cannot replace P2, because it needs the same ISR recoil for m_Q ≳ 400 GeV (Sec. 10.1a) | medium / medium | baseline analysis with P1/P1'; argue for P2 jointly with the compressed-SUSY / disappearing-track programmes; P5 framed as a low-mass + β-tag study |
| R6 | Manpower / compute at USFQ (T2/T3 access UNVERIFIED [ST §4]) | medium / high | partner group; CMS group allocation; S3 gate on ≥ 2 FTE |
| R7 | Undiscovered CMS-internal quirk effort | unknown / high | CADI/CDS/conveners check in week 1 (Q2) |
| R8 | Coplanar window narrow at 3.8 T (0.6-15 keV) | certain / medium | GNN/trajectory category for 0.3-0.6 keV; straight-pair category for ≳ 15 keV |
| R9 | Unlicensed ML code (QuirkTracking-ML, Tracking_pipeline, quirk-tracking) [ST §5 item 9] | medium / low | use acorn / hepattn (GPL-3.0) or own code; ask authors |
| R10 | Phase-2 campaign/geometry churn (D110 vs D126/D128) [ST §1C] | medium / low | match the background campaign found in DAS; keep the geometry a parameter |
| R11 | IT 4-bit ToT saturation for ≳ 10× MIP hits (UNVERIFIED) [TH §4.3] | medium / medium | use hit multiplicity and cluster size; check the CROC dynamic range with the DPG |
| R12 | Public prototype (ODD, 3 T) numbers mistaken for CMS numbers | low / medium | [L2]; label all public numbers "prototype" |
| R13 | Factorisation assumption [A6] fails (correlated fake-rate factors) | medium / medium | VR non-closure → systematic; direct sampling at μ = 50 as a check |
| R14 | Λ-convention confusion in comparisons (√σ vs T_c) | low / medium | [D1] stated in every figure caption |

---

## 17. Open questions for the user (full text, options and recommendations in `OPEN_QUESTIONS.md`)
- Q1 scope (S1/S2/S3);
- Q2 CMS-internal check and convener contact;
- Q3 manpower, partners, compute;
- Q4 benchmarks (E + Ẽ + L?);
- Q5 grid size for Phase 2;
- Q6 trigger ambition (P5 proposal?);
- Q7 primary reconstruction;
- Q8 public prototype geometry;
- Q9 Λ range;
- Q10 quick-win reinterpretation of CMS HSCP results;
- Q11 engaging tracker/MTD DPG on OI-1;
- Q12 Phase-2 campaign/geometry;
- Q13 target CMS publication route for S1.

---

## 18. Label registry

**Assumptions**
- A1: the keV window is signature-driven, not naturalness-predicted (Sec. 3).
- A2: the pair is invisible to the trigger MET objects (Sec. 5).
- A3: no strictly irreducible SM background (Sec. 8.3).
- A4: the ISR-recoil scaling used for the trigger estimates (Sec. 10.1).
- A5: not background-free (Sec. 11.1).
- A6: fake-rate factors are uncorrelated (Sec. 11.1).
- A7: Geant4 CPU per quirk event is unknown and must be measured in W1 (`SAMPLE_REQUIREMENTS.md` §2).
- A8: two-quirk DT response and L1DS BX window are folded into ε_alg (Sec. 10.1a).
- A9 (retired in v3): replaced by the CMS measurement σ(Z→νν, pT > 200 GeV) = 3.00 pb at 13 TeV [2012.09254], scaled to ≈ 3.4 pb at 14 TeV (Sec. 8.3).

**Limitations**
- L1: reach estimates use Knapen's 2 T / μ = 50 efficiencies (Sec. 6.1).
- L2: the public prototype geometry is not CMS (Sec. 8.2).
- L3: ML-on-hits is offline only (Sec. 9.2).
- L4: high-mass efficiencies are quoted with and without the late-hit loss until OI-1 is resolved (Sec. 10.4).

**Decisions**
- D1: Λ ≡ √σ, exact ℓ_max, σ per unit N_IC (Sec. 2.3).
- D2: absolute σ normalisation from the TH table (C4).
- D3: benchmark E, N_IC = 2 (Sec. 7).
- D4: Λ range 0.3-30 keV in three regimes; ≲ 0.2 keV out of scope (Sec. 4.3).
- D5: S3 recommended (PROVISIONAL, user decision).
- D6: one GEN sample per mass, re-propagated per Λ (Sec. 7).
- D7: 15-point Phase-2 subset (Sec. 7).
- D8: common preselection (Sec. 9).
- D9: approach-comparison protocol (Sec. 9.3).
- D10: factorised fake rate (Sec. 11.1).
- D11: two independent data-driven methods for B1/B2 (Sec. 11.1).
- D12: blinding definition (Sec. 11.4).
- D13: theory-σ uncertainty as a band for σ limits (Sec. 12).
- D14: Herwig ISR cross-check (Sec. 12).
- D15: method parity commitments (Sec. 13).
- D16: likelihood structure (Sec. 14).
- D17: toys for all quoted results (Sec. 14).
- D18: VR3 from RAW pick-events, with VR3' = MET 200-250 GeV as the fallback (Sec. 11.3).

## 19. JFC Phase-1 self-check
- [x] ≥ 2 distinct approaches (classical plane finder + trajectory fit; GNN/MaskFormer), with an MVA (event classifier) and a comparison protocol (D9).
- [x] Systematic plan covers every convention source, as implement or N/A (Sec. 12).
- [x] Reference table with systematic programmes **and published numerical results** (Sec. 13).
- [x] Technique chosen and justified (Sec. 14).
- [x] Constants cited or tagged ESTIMATE/UNVERIFIED; [A]/[L]/[D] defined (Sec. 2, 18).
- [ ] Experiment corpus (RAG) query: no CMS RAG corpus was available in this session. CMS-internal sources (CADI, CDS, internal twikis) are **not searched** (EX §1.1 item 1); action Q2.
- [x] Critical review: R1 ITERATE (`../review/STRATEGY_CRITICAL_REVIEW.md`), R2 **PASS** (`../review/STRATEGY_CRITICAL_REVIEW_R2.md`); all A/B items applied (Sec. 20).

---

## 20. Response to review (critical review ITERATE, `../review/STRATEGY_CRITICAL_REVIEW.md`)

Abbreviations: STRAT = this file; SREQ = `SAMPLE_REQUIREMENTS.md`; OQ = `OPEN_QUESTIONS.md`. Recalculation scripts are in the scratchpad (`fix.py`, `reach.py`; not committed).

| Item | Verdict | What changed, and where |
|---|---|---|
| **A1** P5 not ISR-independent | **Agree** | The bound pair reaches the muon system at the pair velocity; β ≥ 0.15 needs pT(QQ̄) ≳ 0.152 M_QQ̄/cosh η = 58-79 / 85-117 / 139-190 / 216-295 GeV at m_Q = 200/300/500/800 GeV. **New §10.1a** derives ε(P5) = 0.08-0.20 / 0.05-0.13 / 0.03-0.08 / 0.01-0.04 and the overlap with P2: the union is ≈ 0.2-0.3 at ≲ 300 GeV and ≈ P2 + ≲ 0.03 at ≥ 500 GeV (v1 said 0.2-0.35). Updated: §1 items 5 and novelty bullet; §5 O10; §6.2 S1 novelty; §6.4 item 2; §10.1 table (P5, P6, best union); §16 R5; [A8]; OQ Q1, Q6 (recommendation changed to P2 as the main trigger case, P5 as a small study: low-m_Q gain + β tag). The S3 recommendation is unchanged; reach numbers always used P1. |
| **A2** 2410.09164 τ′ limits | **Agree** | Re-read: Q = 1e at 1.02 TeV (ionisation) / 1.14 TeV (mass); Q = 2e at 1.32 / 1.41 TeV (cached PDF l.986-987, Tab. 3). Corrected in §13 and in the §2.4 re-verified list; added as the Λ → 0 anchor in OQ Q10. |
| **B1** pair-velocity inconsistency | **Agree** | TH Tab. 4.3 β_T column is inconsistent with its own t_BTL column. v_T is re-derived from t_BTL (0.38/0.19/0.10 at pT = 250 GeV; 0.55/0.34/0.20 at 500 GeV), cross-checked with γ* kinematics (0.43/0.20/0.10). Changes: §2.4 C2 rewritten; §4.2 now has a layer-by-layer toa table; §10.4 Facts use one velocity set and state the lost layers (500 GeV: 2S L3 lost, 2S L2 marginal; 1 TeV: PS L3 + all 2S lost, IT kept); §16 R3 updated. TH Tab. 4.3 β_T is flagged as an upstream error to fix in TH. |
| **B2** Λ edges vs m_Q | **Agree** | **New §4.4**. Λ_low = 0.458 keV (m_Q/100 GeV)^¼ = 0.54/0.69/0.81 keV, with the ×1.8 band from the ×10 formula accuracy. Λ_high^OT ≈ 11/16/19 keV and Λ_high^IT ≈ 22/31/39 keV, from ℓ_max = s_res with s_res = 200 µm and 50 µm. The §4.3 regime table now uses m_Q-dependent edges; D4 sets the category boundaries per m_Q; §1 item 2 gives the mass range; the Λ = 0.6 keV grid point (§7) is described as "probing the transition". |
| **B3** GNN efficiency layers | **Agree** | 71.9% (8 layers) and 79.0% (25 layers) at 500 GeV, Λ = 500 eV. Corrected in §2.4 and §9.2. |
| **B4** reach without background | **Agree** | §6.1 rewritten: the statistical method is stated (single-bin expected CLs with n_obs = Poisson median; s95 = 3.0/4.6-5.6/8.1/12.6/45.2/174 for B = 0/2.5-4.5/10/30/480/7680). Rows with B from 10⁻² fb × L [1911.02223] and the R4 multipliers ×16/×256. Phase 2, 3 ab⁻¹, 3 keV: 1.2 / 0.97 / 0.76 / 0.58 TeV. The Phase-2 gain over Run 2+3 is now a range, from +0.4 TeV down to ≤ 0. Propagated to §1, §6.2, §16 R4 and OQ Q1. The reviewer's "≈ 10-11 events, ≈ 1.0 TeV" for B ≈ 30 agrees with our 12.6 events and 0.97 TeV. |
| **B5** Run-3 luminosity bracket | **Agree** (with nuance) | Widened to 150-350 fb⁻¹; S2 reach now 0.78-0.87 TeV (B = 0) and 0.72-0.77 TeV (with B). Nuance: the ≥ 333 fb⁻¹ figure is FASER at IP1 (ATLAS). The CMS IP5 value remains UNVERIFIED and must come from the lumi POG (SREQ §5). Changed: §6.1, §6.2, OQ Q1. |
| **B6** CPU/storage mismatch | **Agree** | One set of numbers, defined in SREQ §2 (row-by-row sum): S1 Phase 2 ≈ 24-34k core-h, 8-12.5 TB; Phase 3 ≈ +53k, +11-19 TB; total ≈ 77-87k core-h, 20-32 TB. Used identically in STRAT §6.2 and OQ Q3/Q5. S1-PU CPU was raised because μ = 50 went from 5×10⁴ to 10⁵ (B7). |
| **B7** closure test underpowered | **Agree** | Primary target is now 10⁻³ (4/8 layers) with ≥ 10⁵ crossings: the full ColliderML pool gives 1.47×10⁵ μ = 50 crossings, and CMS S1-PU now has 10⁵ at μ = 50. 6×10⁻⁵ is secondary, via factorisation and resampling with an overlap test. Geometry-transfer tolerance is stated beforehand. Changed: STRAT §13 closure bullet; SREQ §0, P-B1, S1-PU, §7 items 4 and 8. |
| **B8** skim MET coverage | **Agree** | Added CR1 sources (ZeroBias + jet-triggered JetMET RAW) and VR3 (MET/JetMET RAW via `edmPickEvents`), with a fallback VR3' = MET 200-250 GeV inside `EXOHighMET` and the SR moved above 250 GeV [D18]. EXOMONOPOLE is qualified: MET/JetMET only from 2024 per its config comment, and a 200 GeV path, hence lower ε. Changed: STRAT §8.1, §11.3, §18; SREQ S2-DATA-MET, new rows S2-CR1/S2-VR3, §5 RAW queries. |
| **B9** Z(νν)+jets σ | **Partly agree** | We cannot verify either number without a generator; no cached source gives σ(Z(νν), pT > 200 GeV). We adopt **[A9] 0.5-20 pb** until the MG5 computation in week 2 (W2, SREQ §6-§7) and propagate it: f_tot ≲ 3×10⁻⁸ to 3×10⁻⁹ (§11.1), and S1-ZNN Phase-3 sizing deferred until after the computation (SREQ §2). Factorisation (D10) is unaffected. |
| C1 Knapen 25 ns already in ε_fid | Applied | §6.1 caveat: the timing loss is only partly included. |
| C2 delay mass range | Applied | §1 item 3 now gives 16 ns (500 GeV) and 33 ns (1 TeV). |
| C3 edge-point count | **Applied, but disagree with "16"** | The stated edge set (Λ = 0.3 and 30 keV at 6 masses = 12, plus the 6 remaining Λ at 1250 GeV) is **18**, so 6.6×10⁵ events, ≈ 46k core-h, 9.9-16.5 TB. SREQ §2, OQ Q5. |
| C4 Pythia HV couplings | Applied | W2 check: vector vs chiral Z couplings, compared with an MG5 vector-like UFO (SREQ §6). |
| C5 MTD info in background tier | Applied | SREQ §2: RAWSIM has no MTD reco; use the MINIAOD/AODSIM tier or a private re-reco; check in DAS. |
| C6 SampledMode | Applied | §10.4 step 2 and SREQ W6: default SquareWindow is likely pessimistic. |
| C7 upstream date/count nits | Noted | Not used in STRAT; EX should be corrected (MR 90391 merged 2026-08-27). |
| C8 as-built radii | Applied | SREQ W3: radii configurable. |

Upstream corrections requested (research files, not edited here):
- TH Tab. 4.3 β_T column (B1);
- TH §7 edge-point count (C3);
- EX §4 item 5 / RV-F §8 FASER ISR vs MC-statistics attribution (v1 C1);
- EX §3.6 P5 efficiency (A1);
- ST §3.0 Z(νν) σ (B9).

### 20.2 Round 2 (`../review/STRATEGY_CRITICAL_REVIEW_R2.md`, verdict PASS; v3)

| Item | Verdict | What changed, and where |
|---|---|---|
| **R2-B1** Z(νν) σ | **Agree; verified** | Re-read 2012.09254: the abstract gives "total fiducial cross section for events with Z boson transverse momentum greater than 200 GeV is 3000 +180/−170 fb" (13 TeV, 35.9 fb⁻¹, combined with the charged-lepton measurement); Sec. 6 defines the fiducial region as "p_T^miss > 200 GeV without any other requirements". Scaled ×1.14 to ≈ 3.4 pb at 14 TeV (and ×1.09 to 3.3 pb at 13.6 TeV), using the TH DY σ ratio at √ŝ ≈ 0.4-0.6 TeV (ESTIMATE). Changes: §8.3 row; §11.1 now gives f_tot ≲ (1.5-3)×10⁻⁸ and drops the 3×10⁻⁹ branch; A9 retired (§18); SREQ S1-ZNN (per-event ε ≈ 3×10⁻⁶, so factorisation is mandatory) and W2/week-2 item (MG5 used only for the scaling and the sample definition). ST §3.0 (0.5-1 pb) and R1 (5-20 pb) are both superseded. |
| **R2-B2** background uncertainty in the reach | **Agree; verified** | New table in §6.1 with δB/B = 0/20/50%, Gaussian s95 = 1.96 √(B + δB²) (scratchpad `syst.py`). At 3 ab⁻¹ and 3 keV: B = 30 → 0.94 TeV; ×16 → **0.57 TeV** (R2: 0.57); ×256 → **0.29 TeV** (R2: 0.32; the difference is σ interpolation below 200 GeV, see C5). The statistics-only columns are labelled as such, and the ×256 statistics-only entry is flagged unrealistic. Propagated to §1, §6.2 S1 reach, §6.4 item 5, §16 R4 and OQ Q1. |
| **R2-B3** stale "1.0-1.2 TeV" | **Agree** | §6.4 item 5 now gives the background-dependent range. |
| R2-C1 stale text | Applied | OQ Q11 delays (16/33 ns); header "not yet reviewed" replaced; §19 review line updated. |
| R2-C2 S2 luminosity | Applied | §6.2: ~250-450 fb⁻¹ (2017-18 + Run 3). |
| R2-C3 P2 ∪ P5 at 300 GeV | Applied | 0.2-0.3 at 200 GeV and 0.17-0.28 at 300 GeV (§1, §10.1 table, §10.1a, OQ Q6). Online-vs-offline threshold caveat added. The §10.1 header mass range is fixed. |
| R2-C4 τ′ anchor | Applied | §13 and OQ Q10: the limit is for N_IC = 1 (N_IC = 2 is roughly +0.1 TeV, ESTIMATE) and is valid only for Λ ≲ 0.1 keV. |
| R2-C5 interpolation scheme | Applied | §6.1 states log-linear in m_Q, with ±0.03 TeV at low mass from the scheme choice. |
| R2-C6 Run-3 pile-up | Noted | §6.1 background bullet (UNVERIFIED ~60-64). |
| R2-C7 pair range-out at β ≈ 0.15 | Applied | Added to [A8] in §10.1a; W2/W3 compute it. |
