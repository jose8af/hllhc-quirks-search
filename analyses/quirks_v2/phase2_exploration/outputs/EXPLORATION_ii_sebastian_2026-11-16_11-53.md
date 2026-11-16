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

(in progress: K(m) with CT18NLO and PDF4LHC21, validation 3 (DY), validation 2 (Resummino), S2-c inclusive samples
and f₂₀₀, FxFx timing)

## 3. P1: thickness-law clean-ups
(in progress: v1 B*-off configuration resolved, re-timing next)

## 4. Herwig install attempt (DP5)
(queued on maxwell from 13:30)
