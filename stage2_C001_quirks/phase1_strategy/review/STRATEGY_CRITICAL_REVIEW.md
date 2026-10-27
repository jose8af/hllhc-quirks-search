# C001 Phase 1 (Strategy) critical review

Reviewer: independent critical reviewer (JFC `agents/critical_reviewer.md`, lean scope), 2026-10-07.
Artifacts reviewed:
- `phase1_strategy/outputs/STRATEGY_DRAFT.md` (STRAT)
- `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md` (SREQ)
- `phase1_strategy/outputs/OPEN_QUESTIONS.md` (OQ)

Checked against: `research/theory_signal_model.md` (TH), `research/experimental_status_2026.md` (EX), `research/samples_and_tools.md` (ST), `literature/literature_map.md` (LM), `LOG.md`, the cached primary PDFs in `../research/cache/pdf/`, the FASER HEPData record, the live CMSSW and Athena repositories, and GitHub.

## Verdict: **ITERATE**

There are two Category A items. Both are cheap to fix: a text correction plus a small recalculation.
- **A1.** The P5 muon-system trigger is claimed to need no ISR and to be "decoupled from ISR". That is physically wrong for central heavy pairs, and it inflates the headline trigger efficiency (0.2-0.35) and one novelty claim.
- **A2.** A binding published-result entry for 2410.09164 is mis-transcribed (τ′ Q = 1e / 2e limits).

The rest of the strategy is sound:
- All reach arithmetic reproduces.
- The cross sections match TH.
- The FASER values match HEPData.
- Both new CMSSW findings (C7 skims, C8 digitizer window) are confirmed in the source.
- The ATLAS code trail is confirmed.
- Every systematic source in the convention is covered or marked N/A.

Nine Category B items must be fixed before Phase 2 starts. The most important are B1 (the pair-velocity numbers are internally inconsistent), B4 (the reach assumes zero background although the strategy's own estimate is about 30 events), B7 (the binding Phase-2 closure test is statistically underpowered as planned) and B8 (the data skims do not contain the CR1/VR3 MET ranges).

---

## 1. Spot-check table

| # | Claim | Doc location | Source value (how checked) | Result |
|---|---|---|---|---|
| 1 | σ(EĒ), N_IC=2: 200/500/800/1000/1200 GeV = 220/6.11/0.660/0.197/0.0656 fb at 14 TeV (and the 13, 13.6 TeV columns) | STRAT §4.1 | TH §2.3 table, identical. TH App. A raw LO 2.636 fb ×2 × K 1.158 = 6.10 fb | OK |
| 2 | PDF unc. ±3.7/6.6/11.9/18.5/~25% | STRAT §4.1, §12 | TH §2.3 / §5 | OK |
| 3 | 3-event reach: 0.78 (0.70) / 0.83 (0.75) / 0.58 / 1.03 / ≈1.2 / 0.92 TeV | STRAT §6.1 | Recomputed: N = L × σ (TH table, log-interpolated) × ε, with ε = 0.10×0.28×0.65 = 0.0182 (3 keV) and 0.10×0.28×0.11 = 0.00308 (1 keV). Got 0.780 / 0.705, 0.834 / 0.756, 0.583, 1.032, 1.24, 0.917 TeV | OK |
| 4 | TH §7 yields 330/50/11/3.5 at 500/750/1000/1200 GeV, 3 ab⁻¹ | STRAT §6.1 | Recomputed 334/50/10.8/3.6 | OK |
| 5 | Knapen Tab. I: ε_trig 0.10, ε_fid 0.28, ε_reco 0.11/0.41/0.65/0.72/0.74 (Λ = 1-5 keV, 800 GeV DY) | STRAT §2.4, §6.1 | 1708.02243 Tab. I (PDF l.551-563) | OK |
| 6 | Random planes 10⁻³ (4/8 layers) and 6×10⁻⁵ (all layers); O(1000) hits/layer; reach "650 GeV, 300 fb⁻¹" | STRAT §2.4, §8.3, §13 | 1708.02243 Sec. IV (l.471-480); abstract l.23-24 | OK. Note: ε_fid already contains a 25 ns timing cut (l.496-498); see C1 |
| 7 | Trigger ε: P1 0.08-0.12, P1′ 0.13-0.18, P2 0.15-0.25, P5 0.05-0.2, P2∪P5 0.2-0.35 | STRAT §1, §10.1 | EX §3.6, transcribed correctly | Transcription OK; **P5 physics wrong (A1)** |
| 8 | L1 PuppiETmiss 200(128) GeV at 18 kHz; +42 kHz for 170(100); HLT MET 140 GeV at 228±20 Hz | STRAT §10.1 | EX §3.2 (L1 TDR Tab. 4.1, p. 209; 2211.03684 Tab. 2) | OK |
| 9 | HLT quirk path ≈ 0.6% of the farm | STRAT §10.1 | 37×10⁶ HS06 / (1680/128 HS06 per thread) = 2.82 M threads; 18 k / 2.82 M = 0.64% | OK |
| 10 | Λ where d = 100 µm: 0.55/0.69/0.81 keV (200/500/1000 GeV); ATLAS 0.58 keV at 500 GeV | STRAT §4.2, §6.4 | Recomputed d = 1.16 µm (m/100)(keV/Λ)⁴ × 3.8: 0.545/0.685/0.815 keV; ×(2/3.8)^¼ gives 0.584 keV | OK. But the regime table is inconsistent at m ≥ 500 GeV (B2) |
| 11 | Coplanar window upper edge 15 keV | STRAT §1, §4.3, D4 | No derivation in TH/EX (TH §4.4 says only "10-20 keV degrading"). Reviewer estimate: OT rφ merging (ℓ_max ≈ 200 µm, using TH γ* medians) at Λ ≈ 11/16/19 keV for 200/500/1000 GeV | Plausible, undocumented (B2) |
| 12 | Pair β_T median 0.23/0.14/0.09 and t_BTL 10.0/19.8/36.7 ns (pT(QQ̄) = 250 GeV) | STRAT §2.4 C2, §4.2 | Transcribed correctly from TH Tab. 4.3. **TH Tab. 4.3 contradicts itself:** t = r/(β_T c) = 114.8 cm/(β_T × 29.98 cm/ns) gives 16.6/27.3/42.5 ns. TH's own γ* medians (1.30/1.25/1.19) with pT = 250 GeV give v_T ≈ 0.19 at 500 GeV and t ≈ 20 ns. So the t_BTL column is consistent with the kinematics and the β_T column is not | Inconsistent upstream number propagated (B1) |
| 13 | δt at TB2S L3 (1.108 m): 8.6 ns (β = 0.3), 14.8 ns (β = 0.2) | STRAT §10.4 | (1.108/0.2998)(1/β − 1) = 8.62 / 14.78 ns | OK (arithmetic) |
| 14 | Phase-2 digitizer drops OT SimHits with toa = tof − \|r\|/c outside ±12.5 ns; IT keeps [−5, 20) ns unless time-walk emulation is on; 2S `HitDetectionMode = 0` | STRAT C8, §10.4 | cms-sw/cmssw master: `phase2TrackerDigitizer_cfi.py` (`TofLower/UpperCut` −12.5/12.5 in the PSP, PSS and SS blocks; −5/20 in PixelDigitizerAlgorithmCommon; `HitDetectionMode = cms.int32(0)`); `PSSDigitizerAlgorithm.cc` / `PSPDigitizerAlgorithm.cc` / `SSDigitizerAlgorithm.cc` `select_hit`; `Phase2TrackerDigitizerAlgorithm.cc` l.185 (tCorr = \|global hit position\| × c_inv); `PixelDigitizerAlgorithm.cc` l.78-81 | **VERIFIED.** See C8 for the SampledMode nuance |
| 15 | Run-3 JetMET/MET PDs run `EXOHighMET` (RAW-RECO; pfMET > 200 GeV or MET ratio > 2 with the smaller > 150 GeV, plus a good PV) and `EXOMONOPOLE` (USER; keeps siStrip/siPixel clusters, siPixelDigis, generalTracks; paths HLT_Photon200 and HLT_PFMET200_BeamHaloCleaned). Run-2 MET PD runs `HighMET` (RAW-RECO) + EXOMONOPOLE | STRAT C7, §8.1; SREQ §3 | `autoSkim.py` l.6-7, 31, 35, 61; `Skims_PDWG_cff.py` l.256-273; `PDWG_EXOHighMET_cff.py`; `PDWG_EXOMONOPOLE_cff.py`; `DPGAnalysis/Skims/python/Skims_DPG_cff.py` l.438-447 (HighMET RAW-RECO) | **VERIFIED.** Nuances in B8 |
| 16 | FASER observed limits 57/72/113/149/163/179/173 GeV at Λ = 0.3/0.5/1/1.7/3/10/30 keV | STRAT §1, §3, §13 | HEPData ins3184325 v1, `exclusion_limit_contours.yaml`: 57.32/72.5/113/149.1/162.58/179/173 | OK |
| 17 | FASER systematics: shower scale ≈ 25%, MC statistics ≈ 6% (up to 28%), luminosity 2.2% (correction C1) | STRAT §2.4 C1, §12 | 2607.26195 p.5 (PDF l.323-334, 352-358) | OK, and C1's correction of EX/RV-F is right |
| 18 | ATLAS repo `burzynski-lab/quirk-tracking`: "for the ATLAS quirk search", GNN4ITk dumps, "replace the invented flat eps_find = 0.5 ... in the contour", created 2026-09-09, last push 2026-09-15 | STRAT §1, §6.3, §15 | `gh api` (repo metadata, README, PLAN.md l.3, 60-81) | OK (30 commits now vs 27 in EX; immaterial) |
| 19 | Athena `G4Extensions/Quirks` fixes in Aug 2026 (target 24.0) | STRAT §6.3 item 3, §15 | GitLab API: MR 90391 "Fix quirk simulation" merged 2026-08-27 into 24.0; MR 90520 "More fixes for G4 quirks" merged 2026-09-01 into 24.0; swept to main 08-27 and 09-02 | OK (EX gives 08-25 for MR 90391; immaterial) |
| 20 | 2410.09164: "DY Q = 1e (2e) excluded below 1.02 (1.14) TeV (ionisation) and 1.32 (1.41) TeV (mass)" | STRAT §13 table (A) | 2410.09164 l.986-987 and Table 3 l.1014-1015: **Q = 1e: 1.02 (ionisation) / 1.14 (mass); Q = 2e: 1.32 / 1.41** | **MISMATCH (A2)** |
| 21 | 2410.09164: ε_trig 0.86 (DY stau 557 GeV), 0.11 (gluino 1.8 TeV); muon timing up to 30%; luminosity 2.0%; stau 0.85 TeV, gluino 2.06/2.08 TeV | STRAT §2.4, §13 | Table 2 l.418; l.657, 677; Table 3 | OK |
| 22 | 2309.16823: wino (higgsino) 650 (190) GeV; T6tbLL 850 (1210) GeV | STRAT §13 | l.1774-1775, l.1433 | OK |
| 23 | 1801.00359: halo 2.6±0.2, cosmics 8.8±3.1 events in 586 h | STRAT §8.3, §13 | Tab. 4 l.636-637; l.156 | OK |
| 24 | 2410.00269: "79.0% track efficiency at 500 GeV, 8 layers" | STRAT §2.4, §9.2 | Sec. E l.502-503 and Tab. I l.632: 79.0% is for the **25-layer** geometry (m = 500 GeV, Λ = 500 eV). The 8-layer benchmark is 71.9% (l.494) | **MISMATCH (B3)** |
| 25 | 2601.20063: 3.7 fb⁻¹, 0.15 ≲ β ≲ 0.80, limits down to 3.5 fb, per-stub BX misID < 1-6% | STRAT §8.3, §13 | l.137-143, 869, 359-360 | OK |
| 26 | B2 ≈ 10⁻² fb ⇒ ≈ 30 events in 3 ab⁻¹ | STRAT §8.3 | 1911.02223 l.672 ("~10⁻² fb, which cannot be neglected"); 10⁻² × 3000 = 30 | OK |
| 27 | SREQ §2 CPU/storage rows | SREQ §2 | S1-SIG 7.5×10⁴ × 250 s = 5.2 k core-h, 1.1-1.9 TB: OK. S1-ZNN/WJ 6.9 k each: OK. Full grid 5.6×10⁵ × 250 s = 38.9 k core-h, 8.4-14 TB: OK. **Totals:** the rows sum to ≈ 31 k core-h and ≈ 8.6-9.4 TB, vs the stated "25-30 k, 7-8 TB" | Minor (B6) |
| 28 | S1 cost "CPU ~30-60 k core-h, 8-15 TB (SREQ §2)" | STRAT §6.2 | SREQ §2 says ≈ 25-30 k core-h and ≈ 7-8 TB (OQ Q3 repeats SREQ) | **Inconsistent (B6)** |
| 29 | α_IC(m_Q) ≈ 0.040-0.052 (~25% range) | STRAT §3 | 1/24.7 = 0.0405, 1/19.4 = 0.0515 (TH §6.2) | OK |
| 30 | Run-3 CMS luminosity bracketed by 150-250 fb⁻¹ | STRAT §6.1 | EX §1.1 item 4: FASER (at IP1) recorded ≥ 333 fb⁻¹ by spring 2026, and Run 3 was extended to mid-2026 | Low bracket (B5) |
| 31 | Z(νν)+jets with MET > 200 GeV ≈ 0.5-1 pb at 14 TeV ⇒ stream ~10⁷ ⇒ f_tot ≲ 3×10⁻⁸ | STRAT §8.3, §11.1; SREQ S1-ZNN | ST §3.0 ESTIMATE. Reviewer order-of-magnitude estimate is ~5-15 pb (see B9) | Likely ~10× low (B9) |
| 32 | Binding closure test: reproduce 10⁻³ and 6×10⁻⁵ at μ = 50 | SREQ §0, §1 P-B1; ST §3.0 | 10⁶ sub-events / 50 = 2×10⁴ crossings ⇒ ~20 (10⁻³) and ~1.2 (6×10⁻⁵) expected fakes | Underpowered (B7) |

---

## 2. Category A (blocking)

### A1. P5 / P6 muon-system trigger: "no ISR needed" is wrong for heavy, central quirk pairs
**Where:**
- STRAT §1 bullet 5 ("≈ 0.2-0.35 with ... a new slow-muon-system L1 seed");
- §5 O10;
- §6.2 S1 "What is novel" ("P5 trigger decoupled from ISR");
- §6.4 Survives item 2 ("a CMS L1 path decoupled from ISR");
- §10.1 rows P5 ("0.05-0.2 (no ISR needed)"), P6 and "Best: P2 ∪ P5 ≈ 0.2-0.35";
- §16 R5;
- OQ Q1 (S1 novelty) and Q6 (recommendation (c), "P2 ∪ P5 could give ε ≈ 0.2-0.35").

Source of the error: EX §3.6 builds the P5 efficiency as f(|η| < 0.83) ~0.5 × f(β window) ~0.2-0.5 × ε_alg. Here f(β window) is treated as an HSCP-like, single-particle β distribution that does not depend on ISR.

**Why it is wrong.**
- The two quirks are bound by the string. They move together at the **pair** centre-of-mass velocity, and they reach the muon system at that velocity (STRAT C2 makes exactly this point for the tracker).
- For a pair in the barrel (|η| < 0.83), |p_pair| ≤ 1.37 pT(QQ̄). Being inside the L1DS/GMT window β ≳ 0.15 [2601.20063 l.137-141: "Below 0.15, the particles mostly get stopped"; efficiency → 0 for β ≲ 0.15, l.288] requires |p_pair| ≳ 0.15 M_QQ̄.
- With M_QQ̄ ≈ 2.3-2.5 m_Q [EX §3.4; TH §4.1 γ* medians], this means **pT(QQ̄) ≳ 140 GeV at m_Q = 500 GeV and ≳ 210 GeV at m_Q = 800 GeV**. That is the same ISR recoil the MET path P1/P2 already requires.
- The upstream numbers confirm this:
  - EX §3.4: pT = 50 GeV gives β_T ≲ 0.07.
  - TH Tab. 4.3: even with pT(QQ̄) = 250 GeV, the 500 GeV pairs sit around β ≈ 0.14-0.19, i.e. at the edge of the window.
- So P5 is not independent of ISR for m_Q ≳ 400 GeV, and it largely overlaps P1′/P2. A modest gain remains plausible only at m_Q ≲ 300 GeV (where pT(QQ̄) ≳ 80 GeV suffices).
- The "≈ 0.2-0.35 vs 0.10" headline and the "decoupled from ISR" novelty therefore do not hold in the mass range they are quoted for (300-800 GeV).

**Required fix:**
- Re-derive the P5/P6 acceptance as a function of (m_Q, pT(QQ̄)). The A4 scaling is enough for the strategy; the Phase-2 W3/P-S1 generator study replaces it later.
- Quote ε(P2 ∪ P5) with the overlap with P2 taken into account.
- Restate the novelty as "a muon-system slow-pair seed, useful at low m_Q and as an independent tag", not "decoupled from ISR".
- Re-evaluate the OQ Q6 recommendation and the §6.4 novelty list accordingly.
- No change to the S3 recommendation is needed: its reach numbers use P1 (ε = 0.10).

### A2. Mis-transcribed binding comparison target from 2410.09164
**Where:** STRAT §13, column (A), row "Published numerical results". These targets are binding for §6.8 per JFC 02-phases Phase 1.

STRAT says: "DY Q = 1e (2e) excluded below 1.02 (1.14) TeV (ionisation) and 1.32 (1.41) TeV (mass)".

The source says (2410.09164 l.986-987, Table 3 l.1014-1015):
- τ′ Q = 1e: **1.02 TeV (ionisation), 1.14 TeV (mass method)**;
- τ′ Q = 2e: **1.32 TeV (ionisation), 1.41 TeV (mass method)**.

The parentheses denote the method, not the charge.

**Fix:** correct the entry.

The τ′ (Q = 1e, DY) model has exactly the E = (1,1)₋₁ quantum numbers. The corrected 1.02-1.14 TeV HSCP limit is the natural Λ → 0 anchor for the Q10 reinterpretation, so it is worth stating explicitly there as well.

---

## 3. Category B (fix before Phase 2 starts)

### B1. Pair-velocity numbers are internally inconsistent (C2, §4.2, §10.4)
**The C2 correction is right in substance.** Arrival times are set by the pair velocity, not by the per-quirk β* that EX §3.4b attributed to TH. The number it propagates is not right:
- TH Tab. 4.3 quotes β_T medians 0.23/0.14/0.09 but t_BTL medians 10.0/19.8/36.7 ns. These are incompatible: r/(β_T c) = 16.6/27.3/42.5 ns.
- An independent recomputation with TH's own γ* medians (M ≈ 2γ*m_Q, pT = 250 GeV, |η| < 1.5) gives v_T ≈ 0.4/0.19/0.10 and t ≈ 9-12/20/37 ns. This reproduces the t_BTL column, not the β_T column.
- So the BTL delays (16 ns at 500 GeV, 33 ns at 1 TeV, 2% / 0% below 12.5 ns) look right, and β_T ≈ 0.14 is likely a mislabel or miscomputation.

**Do the OT 12.5 ns conclusions follow?** Yes, but they depend on the layer (reviewer estimate, η ≈ 0, CMSSW toa definition):
- At 500 GeV, only the outer 2S layer (δt ≈ 16 ns) is lost, and the middle 2S layer is marginal (≈ 12 ns).
- At 1 TeV, PS L3 and all 2S layers are lost (≥ 15 ns), and only the IT and PS L1-L2 survive.
- At 200 GeV, everything is in time.

R3 and OI-1 therefore stand. **Fix:**
- Correct or relabel the β_T values in C2 and §4.2.
- Make the §10.4 "Facts" use one consistent set. The EX β = 0.2/0.3 examples sit beside the β_T = 0.14 claim.
- State the layer-by-layer loss.

### B2. The Λ window edges are mass-dependent and not consistently stated
- The STRAT §4.3 regime table asserts "0.6-10 keV: d ≤ 100 µm". Yet §4.2 and TH Tab. 4.2b give d = 170 µm (500 GeV) and 340 µm (1 TeV) at Λ = 0.6 keV.
- The onset is 0.55/0.69/0.81 keV. The analytic thickness formula is accurate only to about ×10 [2002.07503 App. C], i.e. about ×1.8 in Λ.
- The 15 keV upper edge (exec summary, D4 SR window, R8) is never derived. The reviewer's OT-merging estimate (ℓ_max ≈ 200 µm at Λ ≈ 11/16/19 keV for 200/500/1000 GeV) supports it only at about 500 GeV.

**Fix:**
- Label 0.6-15 keV as a nominal, mass-dependent window. Give the two derivations with their m_Q dependence.
- Describe the Λ = 0.6 keV grid point (D7) as "probing the transition", not as "the coplanar onset".

### B3. 2410.00269 efficiency mis-described (STRAT §2.4 "re-verified" list, §9.2)
- 79.0% is the **25-layer** result (m_Q = 500 GeV, Λ = 500 eV). The 8-layer benchmark is 71.9% [2410.00269 l.494, 502-503, Tab. I].
- Since this appears in the "re-verified against primary PDFs" list, correct it there too.

### B4. The reach assumes zero background, contrary to the strategy's own background estimate
- §6.1 uses background-free 3-event reach for every scope, while §8.3 and A5 state B2 ≈ 10⁻² fb, i.e. ≈ 30 events in 3 ab⁻¹ at μ = 50. R4 allows ×16-256 more at μ = 200.
- With B ≈ 30 the 95% CL needs ≈ 10-11 signal events, giving σ ≈ 0.2 fb and a reach of ≈ 1.0 TeV at 3 keV, not 1.2 TeV. For Run 2+3 (B ≈ 3-4) the change is small.
- So "Gain of Phase 2 over Run 2+3 ≈ +0.35-0.4 TeV" and the S1 "reach ≈ 1.0-1.2 TeV" are optimistic. The caveat "holds only if the PU-200 background stays near zero" is present, but the numbers are presented without the alternative.

**Fix:** add a row with B = O(10-30) (and one PU-200 multiplier from R4), and quote the S1-vs-S2 gain as a range.

### B5. Run-3 luminosity bracket is below the upstream evidence
- §6.1 uses 150-250 fb⁻¹ for CMS Run 3 (UNVERIFIED).
- EX §1.1 item 4 documents ≥ 333 fb⁻¹ recorded at IP1 by spring 2026, with Run 3 extended to mid-2026. EX §1.0 item 6 assumes ~400 fb⁻¹ Run 2+3 for ATLAS.
- With ~330 fb⁻¹ (plus 101 fb⁻¹ of 2017-18) the S2 3-event reach at 3 keV is ≈ 0.87 TeV (reviewer recomputation).

**Fix:** widen the bracket (e.g. 150-350 fb⁻¹), or take the value from the lumi POG (SREQ §5 (a)). Update the S2 reach in §6.2, OQ Q1 and the ATLAS comparison.

### B6. CPU/storage numbers disagree between documents
- STRAT §6.2 (S1 cost) says "CPU ~30-60 k core-h, 8-15 TB (SREQ §2)". SREQ §2 and OQ Q3 say ≈ 25-30 k core-h and ≈ 7-8 TB.
- The SREQ §2 rows actually sum to ≈ 31 k core-h and ≈ 8.6-9.4 TB when all unknown samples are produced privately.

**Fix:** use one consistent total, and state whether it includes Phase 3.

### B7. The binding Phase-2 closure test is underpowered as planned (SREQ §0, §1 P-B1, S1-PU)
- SREQ uses 10⁶ ColliderML sub-events, i.e. 2×10⁴ μ = 50 crossings. Expected fakes: ≈ 20 at 10⁻³ (≥ 4/8 layers) and ≈ 1.2 at 6×10⁻⁵ (all layers).
- The full 7.33 M pool gives 1.5×10⁵ independent μ = 50 crossings, i.e. ≈ 9 all-layer fakes.
- ST §3.0's "≥ 1.7×10⁶ crossings at μ = 50 ... fine" requires 8.5×10⁷ sub-events, about 12× reuse of the pool.
- The CMS S1-PU plan (5×10⁴ PU-50 crossings) gives ≈ 3 all-layer fakes.

**Fix:**
- Make the 10⁻³ (4/8 layers) number the primary closure target, with ≥ 10⁵ crossings.
- Treat 6×10⁻⁵ by resampling, with a documented argument that random-plane combinatorics are independent, or by the factorised extrapolation (D10).
- Size P-B1 and S1-PU accordingly.

### B8. Data access does not cover all the planned control and validation regions (STRAT §11.3; SREQ §3, §5)
- `EXOHighMET` selects pfMET > 200 GeV (or the MET-ratio branch). It does not contain **CR1** (MET 30-60 GeV) or **VR3** (MET 150-200 GeV).
- CR1 needs ZeroBias, JetHT or SingleMuon RAW. VR3 needs MET/JetMET PD RAW, or the AOD-level `EXODisappTrk` if its content suffices. Neither is in the SREQ data table.
- `EXOMONOPOLE` runs on MET/JetMET only from 2024. The config comment reads "2021: on EGamma dataset only; 2024: on EGamma, MET and JetMET". It also uses only `HLT_PFMET200_BeamHaloCleaned`, a higher threshold than the standard `PFMETNoMu120`-type paths.
- SREQ S2-DATA-MET presents EXOMONOPOLE as a 2022-2025 alternative.

**Fix:** add the CR1/VR3 sources to SREQ §3/§5, and qualify the eras and trigger efficiency of EXOMONOPOLE.

### B9. The Z(νν)+jets MET-stream cross section is probably about 10× low (ST §3.0 → STRAT §8.3, §11.1; SREQ S1-ZNN)
The input is "≈ 0.5-1 pb at MET > 200 GeV, 14 TeV" (ESTIMATE). Reviewer cross-check (ESTIMATE, not generator-verified):
- σ(Z→ℓℓ) ≈ 1.9 nb per flavour × Γ(νν)/Γ(ℓℓ) ≈ 5.9 ≈ 11 nb;
- the fraction with pT(Z) > 200 GeV is O(0.5-2)×10⁻³;
- so σ ≈ 5-20 pb. LHC monojet signal regions with pTmiss > 200-250 GeV contain O(10⁵-10⁶) events per 36-139 fb⁻¹ (reviewer recollection, UNVERIFIED).

If confirmed:
- the 3 ab⁻¹ stream is ~10⁸ events, not ~10⁷;
- the background-free requirement tightens to f_tot ≲ 3×10⁻⁹;
- the ε ~ 10⁻⁵ used to size S1-ZNN (10⁶ events) becomes ~10⁻⁶.

The factorised method (D10) still applies. **Fix:** compute σ(Z(νν)+jets, pT(Z) > 200 GeV) with MG5 in the W2 week-2 GEN study and propagate it, before Z(νν) production is sized.

---

## 4. Category C (style, clarity, minor)

- **C1.** Knapen's ε_fid = 0.28 already includes a 25 ns timing cut [1708.02243 l.496-498]. The caveat "the timing loss of Sec. 10.4 is not included" (§6.1) should say "only partly included (Knapen's 25 ns cut, ATLAS radii ≤ 0.5 m)".
- **C2.** Exec summary item 3 ("~10-20 ns late") holds at 500 GeV. At 1 TeV the BTL delay is ≈ 33 ns (TH Tab. 4.3), so give the mass range.
- **C3.** TH §7, followed by SREQ §2 "Later", counts "8 edge points". The stated edge set (Λ = 0.3 and 30 keV at every mass, plus m = 1250 GeV) is 16 points. The full grid is then 6.4×10⁵ events (≈ 44 k core-h), not 5.6×10⁵ (39 k). OQ Q5 (a) inherits this.
- **C4.** TH §2.2 assumes a vector-like singlet (a_E = 0). Check that Pythia8 `HiddenValley:ffbar2EvEvbar` gives E_v vector-like singlet Z couplings, not SM-electron chiral couplings. This was not verifiable here: the Pythia source was unreachable and the manual is silent. The rate is fixed by D2, but the angular distribution, and so the acceptance, could differ slightly. Document it in W2.
- **C5.** O5 (MTD β) on backgrounds needs MTD information in the official background tier. CMSSW's `phase2_common` RAWSIM modifier keeps only `sim*Digis` and `Phase2TrackerDigi` (`EventContent_cff.py` l.408-411). MTD reco is added to RECOSIM/AODSIM/FEVT. SREQ should state which tier provides MTD times for the backgrounds.
- **C6.** In 2S `SampledMode`, the digitizer samples the CBC pulse at bx_time rather than applying a ±12.5 ns square window (`SSDigitizerAlgorithm.cc` l.87-96). Late hits with large charge may then survive. OI-1 step 2 already plans this. Say explicitly that the default SquareWindow is likely the pessimistic case, and that the real-detector behaviour is what counts.
- **C7.** Minor upstream date and count nits (Athena MR 90391 merged 2026-08-27, not 08-25; quirk-tracking now has 30 commits). Not used in STRAT. FASER 72.5 GeV at 0.5 keV is quoted as 72; fine.
- **C8.** §2.4 C9 notes that the Tracker-TDR IT radii (29.0-157.4 mm) differ from TH's TBPX L1 "2.8-3.0 cm ... 14.6 cm". Fine as resolved. Carry "as-built may differ" into W3's geometry.

---

## 5. Items checked and found correct (no action)
- Signal model, benchmark choice, Λ ≡ √σ convention, exact ℓ_max formula, and the T_c conversion.
- Cross-section table and the Gate-4 ×3 correction (C3); K-factor normalisation decision D2 (C4).
- FASER, D0 and Farina-Low comparison targets; Knapen and Sha projections.
- Systematic plan: every `conventions/search.md` source is listed as "Will implement" or "N/A" with a reason. Fragmentation N/A and e⁺e⁻ beam N/A are justified. Sizes are tied to citations or "to be measured".
- Two qualitatively different approaches plus an MVA, with a comparison protocol (D9); method parity (D15); toys for low counts (D17); blinding (D12).
- Background classification (irreducible at preselection / reducible / instrumental) and the CR/VR design, apart from the data-access gap in B8.
- Sample tiers: Phase-2 RAWSIM keeps tracker digis (ST-verified, and re-seen here in `EventContent_cff.py` l.408-411). Signal is produced in FEVTDEBUG with PSimHits. Run-3 MC is flagged as needing re-digitisation if only AOD/MINIAOD exist. RAW-RECO and the cluster-level USER skims contain hit-level information.
- The ATLAS competition assessment (most likely Run-2/3 ID, medium confidence) and the novelty audit, apart from the P5 item in A1.

## 6. What the fixer must do for PASS
1. **A1:** re-derive the P5/P6 (and P2 ∪ P5) efficiency with pair kinematics; correct STRAT §1, §5 O10, §6.2, §6.4, §10.1, §16 R5 and OQ Q1, Q6.
2. **A2:** correct the 2410.09164 τ′ limits in STRAT §13.
3. Address B1-B9 in the same iteration. They are textual or small recalculations, except B9, which can be a stated Phase-2 week-2 action.

The re-review will check only the changed sections.
