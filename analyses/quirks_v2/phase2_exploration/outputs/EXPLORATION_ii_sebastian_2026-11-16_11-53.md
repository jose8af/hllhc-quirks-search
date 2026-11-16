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

## 2. S2: theory inputs
(in progress: MLM timing, validations 1 and 3, K(m) scan, f₂₀₀ samples, FxFx timing)

## 3. P1: thickness-law clean-ups
(in progress: v1 B*-off configuration resolved, re-timing next)

## 4. Herwig install attempt (DP5)
(queued on maxwell from 13:30)
