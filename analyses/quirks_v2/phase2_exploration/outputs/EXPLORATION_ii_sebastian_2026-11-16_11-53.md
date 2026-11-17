# Phase 2 exploration, channel (ii): S2, P1, retrievals, Herwig (executor Sebastian), interim

Status: **interim**. Written from 2026-11-16 12:16 -05 on and updated as items finish. Session log:
`phase2_exploration/logs/executor_sebastian_2026-11-16_11-53.md`. Retrievals: `retrieval_log.md` #11–#15.
Tags: VERIFIED (run or read by me, with file:line, page or campaign), ESTIMATE, UNVERIFIED.

## 1. Retrievals R-2 and R-3: hand-over to the Phase-3 MET-model work

R-3 is sourced from the **second public source** (STR §4.7 l.1338: the HL-LHC performance reports of the other
general-purpose experiment). CDS blocks automated access and the CMS performance note was not obtainable. Parameters
are transcribed and nothing is tuned. No value is recommended here: the choice of construction belongs to the Phase-3
MET-model work and the pre-registration review.

### 1.1 Every sourced parameter

| quantity | value as printed | document | table / figure / eq. | printed page | validity range stated by the source | tag |
|---|---|---|---|---|---|---|
| L1 MET trigger: offline (gen-level visible) MET at 90 % of plateau | 200 GeV (PUPPI MET seed, rate 18 kHz) | CMS L1 TDR CERN-LHCC-2020-004 | Table 4.1 | 210 | tt̄, ⟨PU⟩ = 200, 14 TeV; "offline" = generator-level MET from visible particles (§4.1, p. 202–203; §4.1.4, p. 206) | VERIFIED (read) |
| same, at 50 % of plateau | 128 GeV | same | Table 4.1 (value in brackets); text p. 209 | 210, 209 | same | VERIFIED (read) |
| reconstruction-efficiency plateau of the seed | 100 % | same | Table 4.1 | 210 | same | VERIFIED (read) |
| turn-on curve, online threshold 112 GeV | figure only | same | Fig. 3.125 | 188 | tt̄, 200 PU, vs gen MET | figure, not read |
| ATLAS planned HL-LHC offline E_T^miss trigger threshold | 210 GeV | ATL-PHYS-PUB-2019-005 | Table 2 | 8 (PDF p. 8) | HL-LHC baseline menu | VERIFIED (read) |
| jet resolution, functional form | σ_pT/pT = √(N²/pT² + S²/pT + C²), N = a(η) + b(η)·μ | ATL-PHYS-PUB-2013-004 | eq. (2), (3) | 11 | fitted on μ = 0–40, extrapolated linearly to μ = 140 by the source; **μ = 200 is a further extrapolation (ESTIMATE)**; anti-k_t R = 0.4 | VERIFIED (read, page rendered) |
| jet resolution parameters, event-by-event (jet-area) subtraction | \|η\| 0–0.8: a 3.2, b 0.04, S 0.74, C 0.05; 0.8–1.2: 3.0, 0.03, 0.81, 0.05; 1.2–2.8: 3.3, 0.03, 0.54, 0.05; 2.8–3.6: 2.8, 0.06, 0.83, 0.05 | same | Table 6(b) | 12 | as above; p_T range not stated | VERIFIED (read) |
| same, average-offset subtraction | b = 0.07 / 0.07 / 0.08 / 0.11 (a, S, C as above) | same | Table 6(a) | 12 | as above | VERIFIED (read) |
| pile-up jet thresholds (10 % / 1 % fake rate) and track-confirmation efficiency | Table 7 values | same | Table 7 | 13 | μ = 140 | VERIFIED (read) |
| MET resolution, European-Strategy form | σ(E_x,y^miss) = (0.40 + 0.09·√μ)·√(ΣE_T + 20·μ) GeV, Gaussian smearing of the true MET; ΣE_T of the hard scatter, 20 GeV per pile-up interaction | same | §8 | 13 | derived from Run-1 studies; μ dependence extrapolated (μ = 200: ESTIMATE) | VERIFIED (read, page rendered) |
| MET resolution at μ = 140 | Z′ fit 32.1 + 0.720·√ΣE_T for ΣE_T > 1700 GeV; min-bias interpolation below 1300; systematic ±√(σ_thresh² + σ_process²), σ_thresh = 5 GeV, σ_process = Res − 0.95·Res(Z′ fit) | ATL-PHYS-PUB-2013-009 | Table 5 | 8 | μ = 60, 80, 140 only; Run-1 calorimeter with ITK | VERIFIED (read) |
| muon reconstruction efficiency | loose 0.99; tight 0.97 (0.54 at \|η\| < 0.1; 0 at 2.5–2.7) | same | Table 1 | 3 | from 2012 data | VERIFIED (read) |
| electron efficiencies | cluster 0.995, track match 0.97, track quality 0.99; Medium ID 0.836 ± 0.004 | ATL-PHYS-PUB-2016-026 | §3 text | 3 (PDF p. 4) | ⟨μ⟩ = 200 | VERIFIED (read) |
| external-validation figure, μ = 200 | §1.3 below | ATL-PHYS-PUB-2019-005 | Fig. 18 | 21 | Powheg+Pythia8 tt̄, ⟨μ⟩ = 200, ITk, PU-jet rejection 50 | ESTIMATE (by-eye reading) |

### 1.2 The 2013 formula against the μ = 200 figure

Script: `phase2_exploration/src/s2/met_compare.py` (stdlib, no fit). Output: `phase2_exploration/outputs/s2/met_compare.json`
[VERIFIED: run 2026-11-16 12:15 -05]. Two readings of the 2013-004 ΣE_T:
- (a) ΣE_T is the hard-scatter ΣE_T, so the formula adds 20·μ;
- (b′) the figure's total ΣE_T is inserted without the 20·μ term.

Reading (b), with ΣE_T,hs = ΣE_T − 20μ, is undefined below 4,000 GeV.

| ΣE_T [GeV] | Fig. 18 "full η" [GeV] | Fig. 18 "\|η\| < 2.5" [GeV] | 2013-004 (a) | ratio (a) | 2013-004 (b′) | ratio (b′) | 2013-009 Z′ fit, μ = 140 |
|---|---|---|---|---|---|---|---|
| 1000 | 37.5 ± 0.5 | 38.5 ± 0.5 | 118.3 | 3.15 | 52.9 | 1.41 | — (below 1700) |
| 2000 | 42.0 ± 0.5 | 46.0 ± 0.5 | 129.6 | 3.09 | 74.8 | 1.78 | 64.3 |
| 3000 | 46.5 ± 0.5 | 51.5 ± 0.5 | 140.0 | 3.01 | 91.6 | 1.97 | 71.5 |
| 4000 | 50.5 ± 0.5 | 56.0 ± 0.5 | 149.6 | 2.96 | 105.8 | 2.09 | 77.6 |

### 1.3 The by-eye readings
- The Fig. 18 values above are **ESTIMATE**, read by eye.
- Reading error: ±0.5 GeV (minor ticks are 1 GeV). The source states no uncertainty.
- The rendered page (150 dpi) is kept at `/var/tmp/jdochoa/sebastian/retr/perf/f18-21.png` on einstein. The PDF is
  `/var/tmp/jdochoa/sebastian/retr/perf/atlas_pub_2019_005.pdf`, sha256 prefix c41e0d2393da108a.
- Further readings of the "full η" curve: 36.5 GeV at ΣE_T ≈ 500 and 50 GeV at 4400.

### 1.4 Not sourced
- **Non-Gaussian low tail of the jet response.** No public Phase-2 or HL-LHC source found (retrieval_log #14).
  Run-2 tail measurements were not used.
- **CMS-NOTE-2018-006** (CMS HL-LHC object performance). Not obtainable: CDS bot protection, not on INSPIRE by
  report number. The user has been asked whether they can supply it.
- **CMS Phase-2 DAQ/HLT TDR** (CMS-TDR-022). Same reason, so the HLT part of R-2 is not sourced.
- **Uncertainty of the L1 MET turn-on.** The TDR quotes none.
- **μ = 200 parametrisations.** The explicit formulas are for μ ≤ 140. Their use at μ = 200 is an extrapolation
  (ESTIMATE).

### 1.5 CMS NOTE-2018/006: the CMS performance note, supplied by the user (added 2026-11-16 13:20)

Source: CMS NOTE-2018/006, "Expected performance of the physics objects with the upgraded CMS detector at the HL-LHC".
The user supplied the file by hand: `NOTE2018_006.pdf`, sha256 28ec834e…c4ac66 (retrieval_log #20). Full simulation of
the Phase-2 detector at 14 TeV, ⟨PU⟩ = 200 unless stated. Pages below are printed page numbers. Curve readings are by
eye from 300-dpi renderings and are tagged **ESTIMATE** with the reading error given.

| quantity | document item, printed page | sample, pile-up | validity range | values | stated uncertainty / reading error |
|---|---|---|---|---|---|
| corrected jet response resolution σ(p_T/p_T^Gen)/⟨p_T/p_T^Gen⟩ vs p_T^Gen | Fig. 25, p. 16 | anti-k_t 0.4 PF+PUPPI, PU 200, two PU-density bins (0–1, 1–2 /mm) that overlap within errors | p_T^Gen ≈ 30–500 GeV; \|η^Gen\| < 1.3, 1.3–1.7, 1.7–2.8 | \|η\| < 1.3: 0.23 (30), 0.18 (50), 0.16 (60), 0.14 (80), 0.13 (100), 0.12 (130), 0.107 (170), 0.09 (250), 0.077 (350), 0.067 (480 GeV). 1.3–1.7: ≈ 0.24–0.30 (30), 0.185 (50), 0.18 (80), 0.17 (100), 0.155 (150), 0.15 (250), 0.135–0.16 (450). 1.7–2.8: 0.27 (30), 0.22 (50), 0.18 (80), 0.175 (100), 0.165 (150), 0.155 (250), 0.17 (450) | none stated; reading ±0.01 (marker statistical bars ≈ ±0.005–0.03 at low p_T) |
| same vs PU density | Fig. 26, p. 16 | AK4 PF, PFchs, PUPPI; 90 < p_T^Gen < 120 GeV | density 0–2 /mm | PUPPI ≈ 0.14 (\|η\| < 1.3), ≈ 0.17 (1.3–1.7), ≈ 0.19 (1.7–2.8), flat in density | none; ±0.01 |
| **non-Gaussian jet-response tail** | — | — | — | **not given anywhere in the note.** The note does not say how σ is defined (fit or RMS) | — |
| PU-jet rate (N jets / N matched) | Fig. 27, p. 17 | PUPPI, p_T > 30 GeV | N_PU 140–260 | ≈ 1.12–1.14 (barrel), 1.13–1.14 (endcap) | none; ±0.005 |
| MET definition | §2.9, p. 19 | — | — | "negative vector sum of the momenta of all reconstructed PF objects"; quoted value "about 25 GeV in the perpendicular component using PUPPI" at PU 200 | none (text value) |
| MET distribution (tail shape) | Fig. 34, p. 21 | Z→μμ, PUPPI p_T^miss, PU 200 vs Run 2 | 0–120 GeV, arbitrary units, log scale | shape only (no true MET in Z→μμ); the PU-200 curve falls ≈ ×10⁻³ from its peak (≈ 20 GeV) to ≈ 100 GeV | none; log-scale reading ≈ ±20 % per bin |
| recoil resolution σ(u_∥)/(u_∥/p_T^Z), σ(u_⊥)/(u_∥/p_T^Z) vs PU density | Fig. 35, p. 21 | Z→μμ, p_T^Z > 30 GeV, PUPPI, ⟨N_PU⟩ = 200 (and 140, Run 2) | density 0–2 /mm; mean density at PU 200 = 1.4 /mm (§2.4, p. 9) | ∥: 30 (0.1), 26 (0.4), 29.5 (0.75), 29.5 (1.1), 32 (1.45), 35 (1.75), 33.5 (1.9) GeV; ⊥: 26.5, 25.5, 28.5, 30, 29.5 (1.5), 31.5, 32.5 (1.9) GeV | none; ±1 GeV |
| electron reconstruction / ID efficiency | text p. 7 (92 % at \|η\| = 1.5 to 98 % at \|η\| = 3); Fig. 10 p. 8 (1.6 < \|η\| < 2.8: ≈ 0.65 at 10 GeV rising to ≈ 0.97 above 40 GeV); Fig. 13 p. 9 (\|η\| < 1.4 reco: ≈ 0.97–0.98, 50–200 GeV, 1000 fb⁻¹ ageing) | Z→ee, PU 200 | as stated | as stated | none; ±0.01 |
| muon reco + tight ID efficiency | Fig. 17, p. 11 | DY Z/γ*→μμ, PU 200, p_T > 5 GeV | **only 1.6 < \|η\| < 2.8**: ≈ 0.97 (1.6–2.0), ≈ 0.995 (2.0–2.8) for the Phase-2 muon system | as stated; the barrel is not shown | statistical bars; ±0.005 |
| single-muon tracking efficiency | Fig. 1, p. 3 | μ, p_T = 10 GeV, PU 140/200 | \|η\| < 4 | ≈ 1.0 (dips to ≈ 0.97 near \|η\| ≈ 1 and 4) | none |
| charged-track efficiency / fake rate | Fig. 2, p. 4 | tt̄, p_T > 0.9 GeV | \|η\| < 4 | efficiency ≈ 0.9 central; fake rate < 2 % (PU 140), ≈ 2–3 % at \|η\| ≈ 1.5–2.5 (PU 200) | none |
| τ_h efficiency / QCD misidentification | Fig. 21–22, p. 14 | Z→ττ, QCD, PU 0 and 200 | \|η\| < 3; p_T 20–160 GeV | ≈ 0.85, flat; misid ≈ 0.55–0.6 (working point not stated) | none |
| primary-vertex identification efficiency (R-8) | Fig. 6, p. 6 | multijet, ≥ 2 jets, PU 200 | leading-jet p_T 50–300 GeV | ≈ 0.98–0.99 (\|η\| < 1.5), ≈ 0.97–0.99 (1.5–2.5), ≈ 0.92–0.98 (2.5–3.5) | none; ±0.005 |
| systematic "floor" uncertainties for HL-LHC studies | Table 1, p. 29; §3.1–3.5, p. 22–28 | — | stated as "guidelines only" (p. 23) | e ID 0.5 % (p_T > 20), 2.5 % (10–20); γ ID 2 %; μ ID 0.5 %; τ ID 2.5 %; **JES** total 1–2.5 % (absolute 0.1–0.2, relative 0.1–0.5, PU 0–2, flavour 0.75 %); **JER 3–5 % as a function of η** (text p. 28: "half of the Run 2 values"); **p_T^miss**: propagate JEC (must) and JER (recommended), vary the unclustered energy by 10 % (recommended); b-tag 1 %, c-tag 2 %, light 5/10/15 %; luminosity 1 %; muon momentum resolution uncertainty 5 % below 200 GeV, 10–20 % at TeV (p. 25) | as given |
| tracking efficiency, material, hit resolution uncertainties (COM B6-d, R-15–R-17) | — | — | — | **not given** in the note | — |

### 1.6 The three MET sources side by side (not forced onto one axis)

Script: `src/s2/met_compare.py` → `outputs/s2/met_compare.json` (rerun 13:18).

| source | quantity | process | pile-up mitigation | x axis | value at PU ≈ 200 | tag |
|---|---|---|---|---|---|---|
| ATL-PHYS-PUB-2013-004 §8, p. 13 | Gaussian σ(E_x,y^miss) used to smear the true MET | any (parametrisation) | none specified (Run-1 extrapolation) | hard-scatter ΣE_T + 20 GeV × μ | 105.8 / 109.1 / 112.2 GeV at ΣE_T,hs = 0 / 250 / 500 GeV; 118–150 GeV at 1–4 TeV | VERIFIED arithmetic on a transcribed formula |
| ATL-PHYS-PUB-2019-005 Fig. 18, p. 21 | RMS(E_x,y^reco − E_x,y^true) | tt̄ (Powheg+Pythia8) | ATLAS PU-jet tagger (rejection 50) + track soft term | total ΣE_T | 37.5 / 42 / 46.5 / 50.5 GeV at 1 / 2 / 3 / 4 TeV (full-η tracking) | ESTIMATE ±0.5 GeV |
| CMS NOTE-2018/006 Fig. 35, p. 21 | response-corrected width of the recoil components u_∥, u_⊥ | Z→μμ, p_T^Z > 30 GeV (no true MET) | PUPPI | PU density | at the mean 1.4 /mm: u_⊥ ≈ 29.5–30, u_∥ ≈ 31–32 GeV; text "about 25 GeV" (⊥) | ESTIMATE ±1 GeV |

**Where they are not comparable:**
- The quantities differ: RMS of the E_x,y residual in tt̄ (with true MET) vs the width of the recoil components in Z→μμ
  (no true MET), response-corrected, with the parallel component also carrying the recoil response.
- The x axes differ: ATLAS uses total ΣE_T, CMS uses PU density with no ΣE_T axis, and the 2013 formula uses
  hard-scatter ΣE_T plus an assumed 20 GeV per interaction.
- Pile-up mitigation differs: PUPPI (CMS) vs PU-jet tagging plus a track soft term (ATLAS); the 2013 formula has none
  of these.
- The detectors differ.

The two μ = 200 full-simulation figures agree with each other in magnitude (≈ 25–50 GeV). Both are ≈ ×2–4 below the
2013 European-Strategy formula. No numerical agreement criterion between them is implied by the sources.

### 1.7 Hand-over for the Phase-3 MET model: options and facts, no recommendation

STR §4.7 B4-b needs (i) a parameter source and (ii) a published PU-200 MET figure that the parameters were not taken
from. The tolerance is the larger of the source's stated uncertainty and the reading error.

| option | parameter source | independent PU-200 validation figure | tolerance available | remarks |
|---|---|---|---|---|
| A | CMS NOTE-2018/006: jets from Fig. 25 (σ vs p_T in 3 η bins, PU 200), soft term from Fig. 35 (u_⊥ at the mean density) | ATL-PHYS-PUB-2019-005 Fig. 18 (tt̄, RMS E_x,y vs ΣE_T) | reading error ±0.5 GeV (no stated uncertainty) | different experiment and definition: the model would be run on tt̄ and the same RMS formed. Detector differences are not part of any stated tolerance |
| B | CMS NOTE-2018/006 Fig. 25 + Fig. 35 (u_⊥) | same note, Fig. 35 u_∥ and Fig. 34 (Z→μμ MET shape, incl. tail) | ±1 GeV (Fig. 35); ≈ ±20 % per bin (Fig. 34, log scale) | same document and same sample as the parameters; distinct figures and quantities. Whether "a different figure" in the same note satisfies STR §4.7 is a reading for the pre-registration review |
| C | ATLAS: 2013-004 jets (μ ≤ 140, extrapolated) + 2019-005 Fig. 18 as the soft-term source | CMS NOTE-2018/006 Fig. 35 / Fig. 34 (Z→μμ) | ±1 GeV / ≈ ±20 % | jets extrapolated in μ (ESTIMATE); experiments mixed |
| D | ATLAS 2013-004 jets + 2013-004 §8 MET formula | ATLAS 2019 Fig. 18 or CMS Fig. 35 | as above | the formula is ×2–4 above both PU-200 figures (§1.6), so it would fail either comparison |

With the CMS note, options A–C each pair a PU-200 parameter source with a PU-200 figure that was not used for the
parameters. The "not validated" branch is therefore no longer forced by missing sources. Whether a given pairing passes
depends on the model, which is Phase-3 work. In every option the **jet-response tail stays not sourced**. The note's
Table 1 (JES 1–2.5 %, JER 3–5 %, unclustered energy ±10 %) gives sourced sizes for the core nuisances of §4.7
"Systematic".

### 1.8 "Not sourced" list (updated)
- **Non-Gaussian jet-response tail.** Not found, including in the CMS note.
- **CMS Phase-2 DAQ/HLT TDR** (HLT MET turn-on). Not obtainable.
- **Uncertainty of the L1 MET turn-on.** None stated in the L1 TDR.
- **Tracking-efficiency, material and hit-resolution uncertainties** (R-15–R-17). Not in the CMS note or the ATLAS notes
  read so far.
- **CMS-NOTE-2018-006: now sourced** (supplied by the user). It replaces the earlier "not sourced" entry for this note
  in §1.4.

## 2. S2: theory inputs

### 2.1 Unit cost of MLM 0–2j generation (replaces the Table 4.0 guess of 50 ms)

Campaign `p2-b-s2-mlmtime`, landau, one job at a time. v1 cards: xqcut 30, qCut 45, CP5, QED-FSR card; the trigger
samples (TRG) carry v1's 100 GeV ME cut. Code: `src/s2/s2_job.py mlmtime`. VERIFIED from each job's own child rusage.

| sample (m = 500) | σ_LHE this run [fb] | v1 σ_LHE [fb] (`sim/SAMPLES.md`) | MG fixed per launch [s] | MG per event [ms] | Pythia per event [ms] | npz per event [ms] |
|---|---|---|---|---|---|---|
| E-TRG | 1.2086 ± 0.0062 | 1.213 | 99 | 3.4 | 25.1 | 9.7 |
| E-INC | 5.386 ± 0.015 | 5.389 | 72 | 4.9 | 22.6 | 9.9 |
| Ẽ-TRG | 0.09736 | 0.09734 | 89 | 3.8 | 25.5 | 10.6 |

In a 20,000-event chunk the full chain (MG + Pythia + npz) costs **≈ 41 ms per LHE event** [VERIFIED rates, chunk
arithmetic ESTIMATE], against the Table 4.0 assumption of 50 ms (G). Further measurements:
- Max RSS 214 MB.
- Node-local MG copy: 28 s once per node.
- The extra compile of the first launch: ≈ 5–8 s on top of the launch fixed cost.

### 2.2 S2-a validation 1: model identity (PASS)

Fixed-order LO of `loop_quirkE` (aMC@NLO, `fixed_order=ON, order=LO`) against the tree-level v1 UFO (MadEvent). Both
runs use μ_R = μ_F = m (fixed; banner checked), CT18NLO, 14 TeV, N_IC = 1. Campaign `p2-b-s2-kval`. Evaluation:
`src/s2/kval_eval.py` → `outputs/s2/kval.json`. The z-score includes half a unit of aMC@NLO's 4-digit summary rounding.

| m [GeV] | σ FO-LO [pb] | σ tree [pb] | rel. diff. | z | verdict (\|z\| < 3 and < 0.5 %) |
|---|---|---|---|---|---|
| 200 | 0.09342 ± 0.000039 | 0.09344 ± 0.000031 | −0.021 % | −0.40 | PASS |
| 500 | 2.654e-3 ± 1.2e-6 | 2.654e-3 ± 1.0e-6 | 0.000 % | 0.00 | PASS |
| 1000 | 8.218e-5 ± 3.7e-8 | 8.216e-5 ± 3.4e-8 | +0.024 % | +0.40 | PASS |

### 2.3 S2-a validation 2: what the reference is, and how independent it is (facts for the NOT-EVALUABLE call)

- **Public tables.** The LHC SUSY cross-section WG right-slepton tables give NLO+NLL only, with no fixed-order NLO
  column (retrieval_log #16; 13 TeV; PDF4LHC15 or CT10). By STR §4.14 (a) 2 they are not a like-with-like reference.
- **Reference used instead:** a self-run fixed-order calculation.
  - Code: Resummino 3.1.2 (conda-forge build h154ca16_2, sha256 c58d442d…; retrieval_log #18, #21), option `--nlo`
    (LO and NLO, stops before resummation). Script: `src/s2/resummino_job.py`.
  - Process ~e_R⁺ ~e_R⁻ (PDG 2000011) at 14 TeV, N_IC = 1; CT18NLO for both LO and NLO; μ_R = μ_F = (m₁ + m₂)/2 = m
    (Resummino's central scale); precision 0.1 %.
  - SM inputs set to the v1 UFO values (α⁻¹ 132.507, G_F 1.16639×10⁻⁵, M_Z 91.188, M_W = 80.419 GeV from the UFO's own
    formula). The remaining SLHA blocks are the code's example spectrum.
  - Our side: `loop_quirkE` Ẽ at the same fixed μ = m (`nlo … --fixed m`, job kref-s-fixm).
  - Both run in campaign p2-b-hw-smoke on maxwell, queued.
- **Independent of `loop_quirkE`:**
  - different authors and code base;
  - its own analytic and numerical implementation of the real and virtual NLO corrections, against MG5_aMC's FKS
    subtraction plus MadLoop;
  - its own phase-space integration;
  - its own coupling set-up from the SLHA.
- **Shared, by construction:** the PDF grid (CT18NLO through LHAPDF), the SM input values, the scale choice, √s. These
  are the "same settings" the strategy asks for, so these sources are common, not tested.
- **Known difference in content** (UNVERIFIED until checked in the code's parameter log or by a decoupling run):
  Resummino's slepton-pair NLO is SUSY-QCD. Its virtual corrections may include squark and gluino loops with the
  masses of the SLHA file; `loop_quirkE`'s NLO is pure QCD. If those loops are present, the size of the contribution
  is unknown until a decoupling run is done (squark and gluino masses raised in the SLHA). Without that run the
  comparison is not strictly like-with-like.
- **Facts for the call (not made here):** a true fixed-order NLO reference exists only in the form of this self-run
  public code. It is independent in implementation, not in inputs. It may contain SUSY-QCD terms absent from our model.
  COM S2-a allows NOT EVALUABLE "if no such reference".

**Result (2026-11-16 14:00, campaign p2-b-hw-smoke; `src/s2/kref_eval.py` → `outputs/s2/kref.json`).** Ẽ (scalar,
~e_R-like), N_IC = 1, 14 TeV, CT18NLO, μ_R = μ_F = m. Our σ_NLO is quoted to 4 digits by aMC@NLO; integration errors
are 0.1–0.16 %.

| m [GeV] | σ_NLO loop_quirkE [pb] | Resummino NLO, example SUSY spectrum [pb] | ratio | Resummino NLO, squarks and gluino at 10⁵ GeV [pb] | ratio | LO ratio (set-up check) | K ours / Resummino (decoupled) |
|---|---|---|---|---|---|---|---|
| 200 | 9.754e-3 | 9.7543e-3 | 1.0000 ± 0.0016 | 9.7485e-3 | 1.0006 ± 0.0016 | 0.9985 | 1.1743 / 1.1719 |
| 500 | 2.330e-4 | 2.3364e-4 | 0.9972 ± 0.0014 | 2.3297e-4 | 1.0001 ± 0.0014 | 1.0001 | 1.1450 / 1.1450 |
| 1000 | 5.897e-6 | 5.9449e-6 | 0.9919 ± 0.0012 | 5.8864e-6 | 1.0018 ± 0.0012 | 1.0009 | 1.1629 / 1.1618 |

- **Criterion (within 3 % at each mass): met at all three masses, with either Resummino spectrum.** The verdict label
  (PASS vs NOT EVALUABLE) depends on whether a self-run public code counts as the reference: orchestrator's call.
- The parameter log confirms the SUSY-QCD content: with the example spectrum (gluino 1298 GeV, squarks 0.94–1.30 TeV)
  Resummino is 0.3–0.8 % above ours. With squarks and gluino decoupled it agrees with ours to ≤ 0.2 %, i.e. within
  1.5σ of the integration errors. So the residual difference was the SUSY-QCD loops, and the pure-QCD NLO of the two
  codes agree.
- EW inputs are identical: Resummino's log shows x_W = 0.22225 = 1 − M_W²/M_Z² of the UFO.
- By-product for the resummed cross-check of S2-b: Resummino's (NLO+NLL)/NLO for ~e_R at μ = m (example spectrum) is
  0.971 / 0.980 / 0.991 at 200 / 500 / 1000 GeV [VERIFIED, this run]. This is for the scalar only; Resummino does not
  ship a fermion E.

### 2.4 S2-a validation 3: process independence, differential (PASS)
Campaign p2-b-s2-kdy; `src/s2/kdy_eval.py` → `outputs/s2/kdy.json`.
- Settings: aMC@NLO fixed order with loop_quirkE (DY is p p > e⁺e⁻ in the same model). μ_R = μ_F = M(pair) via MG's
  user-scale block (dynamical_scale_choice 10, patched in the job). CT18NLO.
- K(M) = (dσ_NLO/dM)/(dσ_LO/dM) in 100-GeV bins (200-GeV bins for the 500 GeV case), from a custom FO analysis
  (pair mass of particles 3 + 4).
- Criterion per bin: |K_E − K_DY| ≤ max(2 % of K_DY, 3σ), with σ from the four independent integration errors.

| comparison | bins | verdict | agreement where the test has power |
|---|---|---|---|
| E (m = 200) vs DY, M = 400–1600 GeV | 12 | PASS | 400–700 GeV: \|ΔK\| ≤ 0.014 at σ = 0.004–0.013 (K ≈ 1.168–1.186) |
| E (m = 500) vs DY, M = 1000–3000 GeV | 10 | PASS | 1000–1800 GeV: \|ΔK\| ≤ 0.012 at σ = 0.004–0.019 (K ≈ 1.20–1.24) |
| Ẽ (m = 200) vs DY | 12 | PASS | 400–900 GeV: \|ΔK\| ≤ 0.013 at σ = 0.006–0.019 |
| E vs Ẽ at m = 200 (v1's "spin-independent" assumption, reported) | 12 | PASS | 400–700 GeV: \|ΔK\| ≤ 0.004 at σ = 0.007–0.012 |

**Power caveat (stated, not a verdict change):** above the first 3–5 bins of each comparison the integration errors
grow to σ = 3–8 %, so the 3σ arm sets the tolerance and the 2 % statement is not tested there. The total K of these
runs (E 200, μ = M) is 0.1083/0.0922 = 1.175, against 1.163 at μ = H_T/2 (scale choice, not a test). **S2-a status:
validation 1 PASS, validation 2 criterion met (reference-status call open, §2.3), validation 3 PASS.**

### 2.5 K(m), CT18NLO (partial; campaign p2-b-s2-kscan)
`src/s2/kscan_eval.py` → `outputs/s2/kfactors.json`. E, μ = H_T/2, fixed order.

| m [GeV] | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 |
|---|---|---|---|---|---|---|---|---|
| K | 1.1628 | 1.1561 | 1.1535 | 1.1536 | 1.1545 | 1.1596 | 1.1672 | 1.1693 |
| NLO scale +/− [%] | 1.5/1.1 | 1.6/1.3 | 1.7/1.6 | 1.9/1.9 | 2.0/2.1 | 2.1/2.3 | 2.2/2.5 | 2.3/2.7 |
| CT18NLO PDF +/− [%] (90 % CL) | 3.3/4.3 | 3.7/4.9 | 4.2/5.6 | 4.8/6.3 | 5.5/7.0 | 6.1/7.8 | 6.9/8.6 | 7.8/9.5 |

| m [GeV] | 1000 | 1100 | 1200 | 1300 | 1400 | 1500 |
|---|---|---|---|---|---|---|
| K | 1.1781 | 1.1817 | 1.1875 | 1.1943 | 1.1997 | 1.2055 |
| NLO scale +/− [%] | 2.4/2.9 | 2.5/3.0 | 2.6/3.2 | 2.8/3.4 | 2.9/3.6 | 3.0/3.7 |
| CT18NLO PDF +/− [%] | 8.7/10.4 | 9.8/11.5 | 11.0/12.6 | 12.4/13.8 | 13.8/15.1 | 15.3/16.5 |

Ẽ (scalar), same settings: K = 1.1619 / 1.1589 / 1.1875 / 1.2187 at 200 / 500 / 1000 / 1500 GeV. NLO scale
+1.4/−1.1, +2.0/−2.1, +2.6/−3.1, +3.3/−4.0 %; PDF +3.4/−4.5, +5.3/−6.9, +10.2/−11.8, +17.9/−18.7 %.

**PDF4LHC21_40** (campaign p2-b-s2-kscan-p4l; symmetric Hessian, 68 % CL; the strategy's nominal set because it
installed). E: K = 1.1657 (200), 1.1535 (500), 1.1760 (1000), 1.1999 (1500); within ≤ 0.6 % of the CT18NLO K at every
mass.

| m [GeV] | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 1000 | 1100 | 1200 | 1300 | 1400 | 1500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PDF4LHC21 PDF ± [%] (68 % CL) | 2.1 | 2.4 | 2.9 | 3.4 | 4.0 | 4.7 | 5.5 | 6.5 | 7.9 | 9.6 | 11.5 | 14.2 | 17.3 | 20.8 |

Ẽ with PDF4LHC21: K = 1.1621 / 1.1578 / 1.1860 / 1.2095 at 200 / 500 / 1000 / 1500 GeV, PDF ±2.2 / 3.9 / 10.6 /
30.5 %. Scale envelopes are as with CT18NLO. σ_NLO per mass and set: `outputs/s2/kfactors.json`
(`results.E_93100`, `E_14400`, `S_…`).

K error ±0.002 (integration). K(200) reproduces FEAS_B's 1.165 ± 0.002. All 14 E masses and 4 Ẽ masses are done with
CT18NLO [VERIFIED, campaign p2-b-s2-kscan]. PDF4LHC21 (68 % CL) is queued (p2-b-s2-kscan-p4l). K_E/K_Ẽ = 1.0008 /
0.9954 / 0.9920 / 0.9892 at 200 / 500 / 1000 / 1500 GeV.

### 2.6 FxFx (S2-c piece): diagnosis and status; plus a CPU accounting artefact
- Measured (session log 18:55): compile stage 8.6 min; MINT step 0 ≈ 30 min of compute for 56 channels on one core
  (P1 channels up to 99 s each); the first launch per mass needs ≈ 70–80 min [ESTIMATE]. It does not fit the 30-min job
  rule; the orchestrator has asked the user for an exception (two single-core jobs of ≈ 1.5 h). Not run, pending.
- **Accounting artefact.** In aMC@NLO *event* mode (MC@NLO/FxFx), MG starts its integration processes so that they are
  not waited-for descendants of the job process. The runner's ru_children (marker user_s/sys_s) therefore misses them:
  fxfx-e500-a recorded 82 s CPU for 794 s wall, and fxfx-diag-a 88 s for 1800 s, while the process sampler showed the
  integrators CPU-bound (ps CPU ≈ elapsed).
  - **Affected campaigns:** p2-b-s2-fxfx-time, p2-b-s2-fxfx-diag, p2-b-s2-fxfx-diag2 (grids stage).
  - **Charging:** these are charged at wall time × 1 core in my tally (≈ 1.4 core-h).
  - **Not affected** (marker CPU ≈ wall checked): fixed-order NLO (kval, kscan, kscan-p4l, kdy, kref-s-fixm), LO/MLM
    (mlmtime, s2c-inc), the shower and conversion steps, and the compile stage of fxfx-diag2.

### 2.7 Pending in S2
K(m) with CT18NLO and PDF4LHC21; validation 3 (DY, μ = M_pair); validation 2 runs; S2-c inclusive samples, f₂₀₀ and its
uncertainty pieces; FxFx timing.

## 3. P1: thickness-law clean-ups

### 3.1 Deviation: P1 runs on new events, not on v1's events
Phase 1 assumed the P1 tests could be run on v1's events. Phase 2 found otherwise:
- v1's P1 event summary `data/sim_stage3/summary/events_p1.npz`, read by `sim/stage3/scripts/fix_bstar_off.py` l.63,
  is not in the repo. The Stage-2 TRGS files it came from are also absent.
- The T2 kinematics cache behind the Stage-1 M3/FIX2 events (`code/T3_propagator.py` l.517-525, about 170 MB, kept
  outside the v1 project) is absent as well.
- `results/FIX_bstar_off.json` keeps per-event c values but not the momenta.

The tests therefore run on new events: Phase-1 toy Stage-3 inputs for timing, and the S2-c inclusive samples, with v1's
P1 selection |η_pair| < 1, for the physics runs. Consequence per criterion:
- **P1-b (paired B*-off):** STR already asks for ≈ 970 new events at 5 keV plus new events at 1 keV. No change to the
  criterion. v1's 171-event result stays a separate, unpaired-in-sample reference; it cannot be extended with the same
  events.
- **P1-c (population estimator):** STR already asks for 300 *new* events per point with new seeds. No change.
- **P1-a (floor tests):**
  - The pre-declared reading of test 1 quotes v1's Δc(20) of +0.01–0.02 on v1's M3 events. On new events, "floor"
    and "physical" are read from the same events in nominal vs high precision, so the reading is unchanged in form.
    The "+0.01–0.02" is then a property of the new sample, measured in the same run in double precision, not a v1
    number re-tested.
  - Test 2 compares the two kernels on the same new events. Not affected.
- **P1-d (validity window, Linux difference):** uses tracked results (`P1.json`) and the M2 conformal run, which is
  regenerable from its inputs in `analytic/numerics/M2_single.py`. Not affected.
- **Lost:** an event-by-event re-run of v1's exact B*-off sample. The comparability of the new paired median with v1's
  171-event numbers is statistical only.

### 3.2 State
- v1 configuration resolved: 4 nm_kernel runs per event (on/off × B, B/2); 17.7 s/event on the M3.
- Timing campaign p2-b-p1-time is queued on landau: B*-off at 5 and 1 keV, and floor test 2 with the 44-bit kernel
  `src/p1/nm_kernel_t44.py`.
- Floor test 1 (≥ 30-digit step map) not started.

### 3.3 P1 unit costs (campaign p2-b-p1-time, landau; toy kinematics; VERIFIED)
| test | per-event CPU | basis |
|---|---|---|
| paired B*-off at 5 keV, 4 runs | mean 17.7 s, median 11.9 s, max 46 s (6 events; m = 500: 22.7 s, 1000: 12.7 s); numba compile 6 s once per job | `bstar-time-l5.json` |
| same at 1 keV | mean 0.66 s (10 events) | `bstar-time-l1.json` |
| floor test 2 (FIX2 'off' arm, 3 keV, s = 1/9, 5 fractions) | 0.4–10 s per event and kernel (nominal, t44, dd similar) | `floor2-time-*.json` |

**Re-projection of P1** [ESTIMATE from these costs]: 970 × 17.7 s = 4.8 CPU-h at 5 keV, plus a few CPU-min each for the
1 keV and P1-c runs and for the floor tests. That is ≈ 6 CPU-h with margin, against STR's 51. STR's 67.8 s × 2 per event
was the Stage-3 production cost, not the cost of the 4 kernel runs (the K-B2 inconsistency noted in STR §4.15). Toy
events are not production kinematics, so the cost is re-checked on the first production chunk.

### 3.4 P1-d: Linux difference of the Stage-1 M2 numerics (done)
Job p1d-m2-linux reran `analytic/numerics/M2_single.py all` (416 runs) and `M2_analysis.py` on landau, in job scratch.
`src/p1/m2_compare.py` compared the result with v1's tracked `results/M2.json` → `outputs/p1/m2_compare.json`.
- Every fitted M2 quantity (A, K, Â, K̂, tp-impulse, κ, for γ* = 1.05, 1.3, 2, 3 and all methods) agrees to ≤ 10⁻¹²
  relative [VERIFIED].
- The only differences are the counts of invalid / floor-rejected conformal runs at γ* = 2 and 3 (e.g. conf256 γ* = 2:
  17 invalid in v1, 7 on Linux), the per-row lists of those runs, and the floor-scale entries dl, whose values sit at
  the round-off floor.
- These configurations have no fit in either run.

**Reading: no quoted M2/P1 number moves; nothing goes to the errata.** FEAS_A's "2 crossings instead of 6" for
`B_g1.3_e3.162e-05_th90_conf256` is one of these floor-level runs and does not change the M2b fit at γ* = 1.3
(K_odd −2.00181 vs −2.00162, rel. 10⁻⁴).

### 3.5 P1-d: validity-window table (done, v1 numbers)
`src/p1/p1d_table.py` → `outputs/p1/p1d_table.json`. 30 (point, Λ) cells from v1's tracked P1.json (`v2b_revisit`).
9 of 30 pass v1's 1.5 % rule, as STR states. The cells that fail are at Λ = 5 keV everywhere (+9.5 to +17 %), at
Λ ≤ 0.6 keV for the heavy points (negative Dc), and around 2–3 % elsewhere.

## 4. Herwig install attempt and generator comparison ([DP5])
- **Install: succeeded.** Herwig 7.3.0 / ThePEG 2.3.0 from conda-forge, node-local on maxwell (27 s; retrieval_log #21).
  Its MB setup also needs the LHAPDF sets CT14lo and CT14nlo, kept node-local (#17, #22).
- **What the comparison is.** It is reported as a **generator spread** (string vs cluster hadronisation at generator
  level), not as an uncertainty of the decays-in-flight rate. Tune facts next to it (retrieval_log #23):
  - Herwig 7.3's general tune is an e⁺e⁻ tune (LEP, PETRA, SLAC, SLC, TRISTAN), and its release note states that MB/UE
    retuning is "currently ongoing".
  - Pythia CP5 (v1 card) is a CMS tune fitted to underlying-event data that include √s = 13 TeV.
- **Status.** Smoke run (2k events each) gave K/π (Herwig/Pythia − 1) of +28 % (0.5–1 GeV) and +37 % (1–2 GeV), with
  statistical errors only. The 10⁶ + 10⁶ event campaign p2-b-hw-mb is queued on maxwell. For channel (iii) it will give
  K/π, p/π, the charged multiplicity and the charged p_T spectrum ratio in |η| < 1, 1–1.5 (and 1.5–2.5), with errors
  (`src/herwig/mb_species.py`, `mb_eval.py`).

**Result (10⁶ + 10⁶ events; campaign p2-b-hw-mb, maxwell, 2026-11-16 19:06–22:12; `outputs/dp5/mb_compare.json`)
[VERIFIED counts; errors Poisson, statistical only].**
- Generators: Herwig 7.3.0, LHC-MB + Diffraction snippets, CT14lo, 14 TeV; Pythia 8.312 CP5, SoftQCD:inelastic,
  14 TeV.
- Stable-particle definition common to both: cτ > 1000 mm stays stable, so π±, K± and K_L are final and K_S and
  hyperons decay.
- Selection: charged particles with p_T > 0.1 GeV.

| quantity | \|η\| < 1 | 1 < \|η\| < 1.5 |
|---|---|---|
| charged multiplicity per event, Herwig / Pythia | 11.43 / 12.09 → ratio 0.946 ± 0.0004 | 5.88 / 6.40 → ratio 0.919 ± 0.0005 |

| p_T [GeV] | K/π Herwig | K/π Pythia | K/π (H/P − 1), \|η\| < 1 | same, 1–1.5 | p/π (H/P − 1), \|η\| < 1 | charged p_T spectrum H/P, \|η\| < 1 | same, 1–1.5 |
|---|---|---|---|---|---|---|---|
| 0.1–0.2 | 0.0306 | 0.0282 | +8.5 ± 0.7 % | +9.2 ± 0.9 % | −35.2 ± 0.9 % | 0.973 ± 0.001 | 0.955 ± 0.001 |
| 0.2–0.3 | 0.0520 | 0.0466 | +11.6 ± 0.5 % | +10.5 ± 0.7 % | −33.4 ± 0.6 % | 0.955 ± 0.001 | 0.935 ± 0.001 |
| 0.3–0.5 | 0.0877 | 0.0783 | +12.0 ± 0.3 % | +9.9 ± 0.4 % | −21.2 ± 0.4 % | 0.904 ± 0.001 | 0.878 ± 0.001 |
| 0.5–0.7 | 0.146 | 0.118 | +23.9 ± 0.4 % | +21.5 ± 0.6 % | +7.6 ± 0.5 % | 0.854 ± 0.001 | 0.826 ± 0.001 |
| 0.7–1.0 | 0.206 | 0.155 | +32.7 ± 0.5 % | +31.4 ± 0.6 % | +41.4 ± 0.6 % | 0.937 ± 0.001 | 0.910 ± 0.002 |
| 1.0–1.5 | 0.273 | 0.203 | +34.3 ± 0.5 % | +33.7 ± 0.7 % | +54.2 ± 0.7 % | 1.079 ± 0.002 | 1.031 ± 0.002 |
| 1.5–2.0 | 0.323 | 0.247 | +30.5 ± 0.8 % | +29.7 ± 1.1 % | +48.8 ± 0.9 % | 1.126 ± 0.003 | 1.073 ± 0.003 |
| 2.0–3.0 | 0.350 | 0.283 | +23.5 ± 0.9 % | +25.4 ± 1.3 % | +52.9 ± 1.1 % | 1.179 ± 0.003 | 1.130 ± 0.005 |
| 3.0–5.0 | 0.369 | 0.334 | +10.5 ± 1.4 % | +8.8 ± 1.9 % | +69 ± 2 % | 1.280 ± 0.006 | 1.254 ± 0.009 |
| 5–10 | 0.379 | 0.395 | −4.2 ± 2.9 % | −9.3 ± 3.9 % | +90 ± 6 % | 1.20 ± 0.01 | 1.21 ± 0.02 |
| > 10 | 0.44 | 0.43 | +3 ± 12 % | −10 ± 16 % | +80 ± 24 % | 0.77 ± 0.04 | 0.82 ± 0.06 |

(K/π values in the first two columns are for \|η\| < 1; the 1–1.5 values are in the JSON.)

**Reading (generator spread, not an uncertainty).** At p_T = 0.5–3 GeV the cluster model gives 20–34 % more K± per π±
than CP5, 5–8 % fewer charged particles per event, and a harder charged spectrum (H/P rising from 0.85 at 0.5–0.7 GeV
to 1.28 at 3–5 GeV). The tunes are not equivalent: Herwig 7.3's general tune is an e⁺e⁻ tune with MB/UE retuning
announced as ongoing, while CP5 is fitted to UE data including 13 TeV (retrieval_log #23). The spread therefore mixes
the hadronisation model with tune quality. These numbers are for channel (iii) (decays-in-flight parent mix); how they
enter rate_DIF is not decided here.
