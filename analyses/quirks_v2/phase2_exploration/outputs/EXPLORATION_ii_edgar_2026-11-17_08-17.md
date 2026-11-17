# Phase 2 exploration, channel (ii): S2, P1, retrievals, generator spread — final (executor Edgar)

Status: **final for channel (ii)**, except the FxFx comparison of S2-c (on hold for the user's ruling). This file
supersedes `EXPLORATION_ii_sebastian_2026-11-16_11-53.md`, which is kept unchanged. That file stays the place for the
full parameter extractions of R-2/R-3 (its §1.1–1.6), the validation-2 independence facts (§2.3) and the MLM timing
detail (§2.1). Session logs: `logs/executor_sebastian_2026-11-16_11-53.md`, `logs/executor_edgar_2026-11-17_08-17.md`.
Retrievals: `retrieval_log.md` #11–#31.

Tags: VERIFIED = run or read by us, with file, page or campaign; ESTIMATE; UNVERIFIED. Times come from `date`.
Signal quantities in this file are only those COM BL-1 allows: cross sections, K, f₂₀₀, and generator-level β and p_T
distributions used for S2-f and P1. No A, no m_mig, nothing selection-dependent.

## 0. Summary of verdicts and readings

| COM row | criterion (short) | result |
|---|---|---|
| S2-a | three validations with numbers | val. 1 **PASS** (\|z\| ≤ 0.40, ≤ 0.024 %); val. 2 **PASS, with the qualifier** "reference = an independent public code (Resummino 3.1.2) run by us at the same settings; not a published number" (ratio 1.0006 / 1.0001 / 1.0018, decoupled); val. 3 **PASS** (power caveat in the upper bins) |
| S2-b | K(m) with scale and PDF errors, both PDF sets; σ_norm table; resummed cross-check beside it | **met**: K(m), σ_norm(m) for 14 E + 4 Ẽ masses with PDF4LHC21 (nominal) and CT18NLO (§2.2); resummed cross-check σ_NLO × R, R = 0.971 → 1.000 (200 → 1500 GeV) from self-run Resummino (scalar, applied to E: flagged) (§2.3) |
| S2-c | one f₂₀₀ definition and script; scale, PDF, merging, tune, FxFx; nuisance in T1 | **met except FxFx**: f₂₀₀ = 0.0484 / 0.1041 / 0.1480 / 0.1676 (E 200/500/1000/1500), 0.1142 (Ẽ 500); band +4.3/−3.2, +2.9/−2.5, +6.0/−5.2, +6.0/−5.9, +3.8/−3.6 %; κ in §2.4. **FxFx**: exception granted by the user 2026-11-17; prepared; NOT submitted (needs a runner change, §2.8) |
| S2-d | nominal signal showered with QED FSR | **met for the S2-c samples** (25/25 chunks `qedfsr: true`). Production (S1) must pass `--qedfsr` (opt-in in `s2_job.py`) |
| S2-e | turn-on from a cited public figure with page, else "parametrised, not sourced" with the wide nuisance | **curve sourced** (L1 TDR Table 4.1 p. 210, Fig. 3.125 p. 188). **No uncertainty stated** anywhere: the nuisance size needs a decision (§2.6). HLT not sourced |
| S2-f | correction per mass with source, or "not sourced" | **numbers per mass** (§2.7): +5.7 % (E 200) to +7.9 % (E 1500) at 1 keV. **Source: not sourced** (R-12, #29). One-sided band (default) |
| P1-a | floor tests read against the pre-declared table | test 2: **"not the floor pattern"** (as recorded); test 1 **not done** ([DT3]); diagnostics §3.2 |
| P1-b | paired B*-off at 3σ (5 keV), 2σ (1 keV) | 5 keV: **"B* attribution not supported at 3σ"** (+1.7σ overall, +1.3σ for k_B ≥ 6); 1 keV: **compatible with zero** at all five points |
| P1-c | \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at five points | **FAIL** (3 of 5 points) |
| P1-d | validity-window table; Linux rerun | table done (9 of 30 cells pass); Linux rerun moves no quoted number |
| REF-2 | R-1…R-20 closed with citation or "not sourced" with the STR §6.4 consequence | §5. Due by day 15 and before the freeze: all attempted. Open: R-4, R-5, R-6, R-10, R-11, R-13, R-19, R-20 (later deadlines) |
| B6-d | each detector nuisance with a cited size | R-15, R-16, R-17: values found, **no uncertainty stated** → STR §6.4 branch "no nuisance; μ₉₅ shift of the robustness test reported" |

## 1. What was run: campaigns and CPU

Source: the ledger markers (`src/s2/cpu_tally.py` → `outputs/s2/cpu_tally.json`). This reads the same marker lines
`qv2run rebuild-ledger` reads. It sums `cpu_s` over every terminal line (all attempts).

**Accounting artefact.** In aMC@NLO *event* mode (MC@NLO/FxFx), MG starts its integration processes so that they are
not waited-for children of the job. The marker's `cpu_s` (ru_children) therefore misses them. Evidence: fxfx-diag-a
recorded 88 s for 1,800 s wall while `ps` showed the integrators CPU-bound. Affected campaigns: p2-b-s2-fxfx-time,
p2-b-s2-fxfx-diag, p2-b-s2-fxfx-diag2. They are **charged at wall time × 1 core** in the "charged" column. Fixed-order
NLO, LO/MLM, shower and conversion jobs are not affected: their marker CPU ≈ wall (checked on kscan, kval, kdy, mlmtime).

Channel (ii) total, tallied 2026-11-17 17:37 -0500: **39.5 CPU-h charged** (38.3 marker CPU-h) of the 139 CPU-h of S2 + P1. The FxFx first launches (≈ 3 core-h) are not yet spent.

### 1.1 Campaign table
| campaign | purpose | jobs (final status) | nodes | marker CPU-h | wall-h | charged CPU-h |
|---|---|---|---|---|---|---|
| p2-b-hw-mb | [DP5] 10⁶ + 10⁶ MB events | 25 (25 done) | maxwell | 2.96 | 3.03 | 2.96 |
| p2-b-hw-smoke | Herwig/Pythia MB smoke; Resummino val. 2 | 7 (5 done, 2 failed) | maxwell | 0.25 | 0.26 | 0.25 |
| p2-b-p1-ev | P1 event sets | 9 (9 done) | landau | 0.01 | 0.02 | 0.01 |
| p2-b-p1-rn | P1 floor diagnostic (RN 44/47 bits) | 4 (4 done) | landau | 0.14 | 0.15 | 0.14 |
| p2-b-p1-rneval | P1 diagnostic evaluation | 1 (1 done) | landau | 0.00 | 0.00 | 0.00 |
| p2-b-p1-run | P1-a/b/c runs | 29 (29 done) | landau | 6.11 | 6.17 | 6.11 |
| p2-b-p1-time | P1 timing | 6 (6 done) | landau | 0.12 | 0.13 | 0.12 |
| p2-b-s2-fxfx-c | FxFx compile (queued) | 1 (1 running) |  | 0.00 | 0.00 | 0.00 |
| p2-b-s2-fxfx-diag | FxFx diagnosis (i) | 1 (1 timeout) | landau | 0.02 | 0.50 | 0.50 |
| p2-b-s2-fxfx-diag2 | FxFx diagnosis (ii)+(iii) | 3 (1 failed, 1 timeout, 1 done) | landau | 0.14 | 0.64 | 0.64 |
| p2-b-s2-fxfx-time | FxFx timing (killed) | 1 (1 killed) | landau | 0.02 | 0.22 | 0.22 |
| p2-b-s2-kdy | S2-a val. 3 (K(M) vs DY) | 5 (5 done) | landau | 0.38 | 0.60 | 0.38 |
| p2-b-s2-kscan | K(m) CT18NLO, 18 masses | 5 (5 done) | landau | 2.00 | 2.05 | 2.00 |
| p2-b-s2-kscan-p4l | K(m) PDF4LHC21, 18 masses | 5 (5 done) | landau | 1.52 | 1.54 | 1.52 |
| p2-b-s2-kval | S2-a val. 1 (FO-LO vs tree) | 6 (6 done) | landau | 0.30 | 0.31 | 0.30 |
| p2-b-s2-mlmtime | MLM 0–2j timing (E-TRG, E-INC, Ẽ-TRG m500) | 3 (3 done) | landau | 0.39 | 0.43 | 0.39 |
| p2-b-s2-nll | S2-b Resummino NLO+NLL, 14 masses × 2 PDF sets | 6 (6 done) | maxwell | 0.67 | 0.69 | 0.67 |
| p2-b-s2-smoke | MG local-copy smoke | 3 (1 done, 2 failed) | maxwell | 0.09 | 0.14 | 0.09 |
| p2-b-s2c-f200 | f₂₀₀ final | 1 (1 done) | maxwell | 0.01 | 0.09 | 0.01 |
| p2-b-s2c-f200t | f₂₀₀ code tests (partial data) | 3 (2 done, 1 failed) | landau | 0.01 | 0.09 | 0.01 |
| p2-b-s2c-inc | S2-c inclusive MLM, 5 × 100k LHE | 25 (25 done) | maxwell | 5.51 | 5.79 | 5.51 |
| p2-b-s2c-rs | S2-c re-showers (qCut 30/60, Monash, FSR off) | 50 (50 done) | maxwell | 17.61 | 18.44 | 17.61 |
| p2-b-s2f | S2-f β average | 1 (1 done) | landau | 0.00 | 0.01 | 0.00 |
| **total** | | | | **38.3** | 41.3 | **39.5** |

## 2. S2: theory inputs

### 2.1 S2-a (unchanged from Sebastian, verdicts as ruled)
- Validation 1 (model identity, fixed μ = m, CT18NLO): FO-LO against tree, rel. −0.021 / 0.000 / +0.024 %, z −0.40 /
  0.00 / +0.40 at 200 / 500 / 1000 GeV → **PASS** (`outputs/s2/kval.json`, p2-b-s2-kval).
- Validation 2: no published fixed-order NLO slepton number exists (WG tables are NLO+NLL, #16). Reference = Resummino
  3.1.2 self-run at our settings. Ours / Resummino NLO = 1.0006 / 1.0001 / 1.0018 (±0.12–0.16 %), squarks and gluino
  decoupled; 1.0000 / 0.9972 / 0.9919 with the example SUSY spectrum (SUSY-QCD loops). Within 3 % → **PASS with the
  qualifier** (orchestrator ruling, LOG 16:12) (`outputs/s2/kref.json`).
- Validation 3: K(M) of E, Ẽ against Drell–Yan in pair-mass bins, μ = M → **PASS**. Where the test has power,
  \|ΔK\| ≤ 0.014; in the upper bins the 3σ arm sets the tolerance (`outputs/s2/kdy.json`). K_E/K_Ẽ at equal M agree to
  ≤ 0.004 (400–700 GeV), so v1's "spin-independent K" holds at equal pair mass.

### 2.2 S2-b: σ_norm(m) with both PDF sets
`src/s2/sigma_norm_table.py` → `outputs/s2/sigma_norm.json` [VERIFIED from campaigns p2-b-s2-kscan, p2-b-s2-kscan-p4l].
σ_norm = N_IC × σ_NLO with N_IC = 2 (STR l.151). Settings: fixed-order NLO QCD, `loop_quirkE`, μ_R = μ_F = H_T/2,
14 TeV. **Nominal set PDF4LHC21_40** (68 % C.L.); CT18NLO is the variant (90 % C.L.). Scale = envelope of 9 (μ_R, μ_F)
values as printed by aMC@NLO. The 7-point envelope of [SD11] lies inside it, and the nine individual values were not
kept, so the 9-point envelope is quoted (equal or wider; deviation noted). Integration error 0.1–0.15 %.

| m [GeV] | σ_norm PDF4LHC21 [fb] | scale +/− [%] | PDF ± [%] (68 %) | σ_norm CT18NLO [fb] | CT18 PDF +/− [%] (90 %) | K (P4L / CT18) | (NLO+NLL)/NLO (scalar, P4L) | σ_norm resummed (P4L) [fb] |
|---|---|---|---|---|---|---|---|---|
| 200 | 216 | +1.5/−1.1 | 2.1 | 216.4 | +3.3/−4.3 | 1.1657 / 1.1628 | 0.9714 | 209.8 |
| 300 | 48 | +1.6/−1.3 | 2.4 | 48.28 | +3.7/−4.9 | 1.1566 / 1.1561 | 0.9752 | 46.81 |
| 400 | 15.33 | +1.7/−1.6 | 2.9 | 15.48 | +4.2/−5.6 | 1.1528 / 1.1535 | 0.9779 | 14.99 |
| 500 | 5.95 | +1.9/−1.9 | 3.4 | 6.008 | +4.8/−6.3 | 1.1535 / 1.1536 | 0.9805 | 5.834 |
| 600 | 2.622 | +2.0/−2.1 | 4.0 | 2.646 | +5.5/−7.0 | 1.1551 / 1.1545 | 0.9828 | 2.577 |
| 700 | 1.253 | +2.1/−2.3 | 4.7 | 1.266 | +6.1/−7.8 | 1.1584 / 1.1596 | 0.9851 | 1.235 |
| 800 | 0.6396 | +2.2/−2.5 | 5.5 | 0.645 | +6.9/−8.6 | 1.1659 / 1.1672 | 0.9871 | 0.6314 |
| 900 | 0.3406 | +2.3/−2.7 | 6.5 | 0.3426 | +7.8/−9.5 | 1.1664 / 1.1693 | 0.9893 | 0.3369 |
| 1000 | 0.1889 | +2.4/−2.9 | 7.9 | 0.1893 | +8.7/−10.4 | 1.1760 / 1.1781 | 0.9913 | 0.1873 |
| 1100 | 0.1078 | +2.5/−3.0 | 9.6 | 0.1075 | +9.8/−11.5 | 1.1807 / 1.1817 | 0.9935 | 0.1071 |
| 1200 | 0.06294 | +2.6/−3.2 | 11.5 | 0.06244 | +11.0/−12.6 | 1.1849 / 1.1875 | 0.9955 | 0.06266 |
| 1300 | 0.0375 | +2.7/−3.3 | 14.2 | 0.03688 | +12.4/−13.8 | 1.1905 / 1.1943 | 0.9973 | 0.0374 |
| 1400 | 0.02278 | +2.8/−3.5 | 17.3 | 0.02216 | +13.8/−15.1 | 1.1955 / 1.1997 | 0.9993 | 0.02276 |
| 1500 | 0.01402 | +2.9/−3.6 | 20.8 | 0.01347 | +15.3/−16.5 | 1.1999 / 1.2055 | 1.0005 | 0.01403 |

Ẽ (scalar), σ_norm PDF4LHC21 [fb]: 18.94 (200), 0.4504 (500), 0.011642 (1000), 0.0007296 (1500); PDF ±2.2 / 3.9 / 10.6 /
30.5 %; scale +1.5/−1.1 … +3.1/−3.9 %. CT18NLO: 19.006 / 0.455 / 0.011566 / 0.0006766 fb.
Set-to-set ratio of the central E values (PDF4LHC21/CT18NLO): 0.998 (200), 0.990 (500), 0.998 (1000), 1.041 (1500).

### 2.3 S2-b: the resummed cross-check normalisation
- **What STR asks:** σ_NLO × (NLO+NLL)/NLO "with the ratio from the public tables".
- **Why the public tables cannot supply the ratio:** they give NLO+NLL only, with no NLO column (#16).
- **What is used instead:** the ratio from Resummino 3.1.2, the code that produced those tables, run by us.
  - Process: ~e_R pairs; squarks and gluino decoupled; 14 TeV; same PDF set as the column; Resummino's central scale
    (m₁ + m₂)/2.
  - Campaign p2-b-s2-nll: 6 jobs on maxwell; masses 200–1500 GeV; CT18NLO and PDF4LHC21.
- **Assumptions, flagged:**
  - The scalar's ratio is applied to the fermion E. No public code gives NLO+NLL for this fermion pair.
  - The ratio is formed at Resummino's scale (m), but applied to our σ_NLO at H_T/2.
- Earlier by-product (example SUSY spectrum, CT18NLO): (NLO+NLL)/NLO = 0.971 / 0.980 / 0.991 at 200 / 500 / 1000 GeV
  (#21, kref).

**Result** (p2-b-s2-nll, maxwell, 6/6 done, 0.67 CPU-h; table §2.2; `outputs/s2/sigma_norm.json` → `nll_points`)
[VERIFIED run].
- **The ratio is below 1 and rises with mass.** R = (NLO+NLL)/NLO = 0.971 (200), 0.981 (500), 0.991 (1000), 1.000
  (1500 GeV) with PDF4LHC21. CT18NLO agrees to ≤ 0.002 at every mass.
- **Effect on σ_norm.** The resummed cross-check normalisation lies 2.9 % below the fixed-order nominal at 200 GeV and
  coincides with it at 1.5 TeV. It is inside the 9-point scale envelope at every mass.
- **Consistency check.** Resummino's decoupled NLO at 200 / 500 / 1000 GeV with CT18NLO (0.0097485 / 2.32972e-4 /
  5.88640e-6 pb) is identical to the kref-dec run, the validation-2 reference.
- **Effect on the reach.** At the masses that set the reach (≈ 1–1.5 TeV) the resummed cross-check moves σ_norm by
  ≤ 0.9 %.

### 2.4 S2-c: f₂₀₀ — one definition, its pieces, the T1 nuisance
**Definition (the only one, in code `src/s2/f200.py` and here):** f₂₀₀ = σ(p_T(QQ̄) > 200 GeV after the shower) /
σ(matched, inclusive), **no η cut**. Numerator and denominator come from the same inclusive MLM 0–2j sample
(p2-b-s2c-inc: 5 × 20,000 LHE events per species-mass; xqcut 30, qCut 45, CP5, QED FSR, CT18NLO). Per event, w is the
nominal merged weight.

**Pieces:**
- Statistical: weighted binomial.
- Scale: LHE weights. The 7-point envelope is nominal; 9-point is reported too.
- PDF: CT18NLO Hessian (58 members), asymmetric master formula, at 90 % C.L. as given. Converted to 68 % under a
  Gaussian assumption by dividing by Φ⁻¹(0.95) = 1.645 (computed in the script; CT18 states the rescaling but prints no
  factor, #30): ESTIMATE.
- Merging scale: re-showers with qCut 30 and 60 against 45 on the same LHE.
- Tune: Monash against CP5, symmetrised.
- FSR off: the shift is quoted but is not in the band.
- FxFx: not run.

**Shift errors:** paired. The re-showers are matched to the nominal by chunk and by the bit-identical LHE quirk
momenta, and the linearised variance of f_var − f_nom is used. The unpaired √(σ_nom² + σ_var²) is in the JSON. Band =
quadrature sum of the scale (7-point), PDF (68 %), merging, tune and statistical terms. The T1 nuisance is one
asymmetric log-normal on the signal yield: κ_up = 1 + up, κ_dn = 1 − dn.
**Result** (campaign p2-b-s2c-f200, maxwell, 2026-11-17 16:5x; `outputs/s2/f200.json`) [VERIFIED]. Inputs: all 25
nominal chunks and all 100 re-shower files, listed from done markers with sha256 re-checked. Limiting checks: the
scale-central and PDF-member-0 columns reproduce the nominal (difference ≤ 3×10⁻¹⁷), and the paired error of a sample
with itself is 0.

| point | f₂₀₀ ± stat | v1 | new/v1 | scale 7-pt +/− | PDF 68 % +/− (90 %) | qCut 30 / 60 shift (paired σ) | Monash shift (paired σ) | FSR-off shift (paired σ) | **band +/−** | **κ_up / κ_dn (T1)** |
|---|---|---|---|---|---|---|---|---|---|---|
| E 200 | 0.04836 ± 0.00091 | 0.04764 | 1.015 ± 0.019 | +3.1 / −2.2 % | +1.3 / −1.2 (+2.2 / −1.9) % | +1.9 (2.0) / −0.5 (2.0) % | −0.3 (2.1) % | −0.6 (2.0) % | **+4.3 / −3.2 %** | **1.043 / 0.968** |
| E 500 | 0.10410 ± 0.00142 | 0.10418 | 0.999 ± 0.014 | +1.1 / −0.9 % | +1.1 / −1.1 (+1.8 / −1.7) % | +1.2 (1.5) / −0.1 (1.5) % | +1.6 (1.5) % | −1.2 (1.5) % | **+2.9 / −2.5 %** | **1.029 / 0.975** |
| E 1000 | 0.14801 ± 0.00173 | 0.14585 | 1.015 ± 0.012 | +0.6 / −0.5 % | +1.7 / −1.7 (+2.9 / −2.7) % | +1.4 (1.3) / +3.0 (1.3) % | **+4.8 (1.4) %** | −1.7 (1.3) % | **+6.0 / −5.2 %** | **1.060 / 0.948** |
| E 1500 | 0.16755 ± 0.00185 | 0.16876 | 0.993 ± 0.011 | +0.4 / −0.3 % | +2.1 / −2.0 (+3.5 / −3.3) % | −0.1 (1.2) / −0.4 (1.2) % | **+5.4 (1.3) %** | **−3.2 (1.2) %** | **+6.0 / −5.9 %** | **1.060 / 0.941** |
| Ẽ 500 | 0.11424 ± 0.00150 | 0.1135 | 1.007 ± 0.013 | +1.0 / −0.8 % | +1.2 / −1.2 (+2.0 / −2.0) % | +1.1 (1.5) / +1.2 (1.4) % | +3.0 (1.5) % | −0.3 (1.4) % | **+3.8 / −3.6 %** | **1.038 / 0.964** |

Band = √(scale² + PDF₆₈² + merging² + tune² + stat²), separately up and down. Components per point are in the JSON
(`band.components_rel`).

**Readings:**
- **Agreement with v1.** f₂₀₀ agrees with v1's values within 1.5 % (≤ 1.3σ of our MC statistics) at all five
  points. The single definition reproduces v1's numbers.
- **Tune is the largest piece at high mass.** The Monash shift is +4.8 % (3.5σ) at E 1000 and +5.4 % (4.2σ) at
  E 1500. At 200–500 GeV it is within 1σ. The band is therefore +6.0 / −5.2 to −5.9 % at 1–1.5 TeV and
  +2.9 / −2.5 % to +4.3 / −3.2 % below.
- **Comparison with v1's band.** v1's estimate was +12…+15 / −11…−13 % (D5 §2 [U]). The rebuilt band is about half of
  that.
- **Merging and statistics.** Merging-scale shifts are ≤ 3.0 % (≤ 2.3σ). MC statistics (1.1–1.9 %) enter the band as
  their own term. Shifts that are not significant are still included, at their measured value: nothing is dropped.
- **QED FSR (S2-d).** The FSR-off shift is quoted outside the band: −0.6 % (E 200) to −3.2 % (E 1500, 2.7σ). Turning
  QED FSR on raises f₂₀₀ by the opposite amount.
- **FxFx not included** (§2.8). STR's rule "enlarge the band if the FxFx value lies outside" is still to be applied.

**Cross-check with channel (i) (input received, not re-derived here).** Channel (i) compared v1's stitched layout
(TRG with an ME cut p_T(QQ̄) > 100 GeV plus INC) with inclusive-only σ(p_T > 200) on 20k inclusive events:
- E 200: 1.118, at 2.3σ;
- E 500: 1.055, at 1.5σ.

Its 100k-event inclusive sample at E 200 (`p2-a-c1-s2inc`) had not been passed on when this file was written.

**What a real effect would mean:**
- If a +5 to +12 % excess of the stitched tail were real, the inclusive MLM 0–2j sample would underestimate the p_T
  tail. f₂₀₀ taken from the inclusive sample alone (the STR definition) would then be **low by 5–12 %**, and the signal
  yield with it. This is conservative for the reach, but a bias.
- A +11.8 % effect at E 200 lies far outside the band (+4.3 %); +5.5 % at E 500 lies outside +2.9 %. Neither the
  merging-scale nor the scale variations of the inclusive sample would cover it.
- v1's f₂₀₀ came from the same inclusive definition and agrees with ours within 1.5 %, so it would carry the same bias.
- **Consequence if confirmed:**
  - either the stitched σ(p_T > 200) becomes the numerator (a change of the frozen definition: decision for the
    orchestrator or user);
  - or the stitched/inclusive difference enters the band as one more one-sided piece, as STR does for FxFx.
- The FxFx sample would test the same high-p_T tail independently.
- With the 100k inclusive sample, our own E 200 f₂₀₀ statistics are 1.9 %. A 2.3σ effect at 20k events would become
  ≈ 5σ at 100k if real.

### 2.5 S2-d: QED FSR is the nominal
All 25 chunks of p2-b-s2c-inc have nominal {CP5, qCut 45, xqcut 30, `qedfsr: true`} (chunk JSONs listed by their
done markers). The card `sim/cards/pythia8_quirk_qedfsr.dat` is applied (SLHA:useDecayTable off; 9000011/9000013
isResonance on). The FSR-off re-shower exists for every chunk (p2-b-s2c-rs, `*.nofsr.npz`) for C1 and for the quoted
shift (§2.4). **For production:** `s2_job.py` makes QED FSR opt-in (`--qedfsr`), so S1's Stage-2 campaigns must pass it.
Channel (i)'s C1 campaigns correctly do not, since v1 had no QED FSR.

### 2.6 S2-e: trigger turn-on (R-2)
`src/s2/trigger_turnon.py` → `outputs/s2/trigger_turnon.json` (stdlib, einstein).
- **Sources:**
  - CMS L1 TDR CERN-LHCC-2020-004, Table 4.1 p. 210: PuppiE_T^miss seed, 50 % at 128 GeV and 90 % of the plateau at
    200 GeV, plateau 100 % (#11).
  - Same TDR, Fig. 3.125 p. 188: the full curve at the 112 GeV online threshold (18.1 kHz), read by eye from a 400 dpi
    rendering, ±0.01 (#31) [ESTIMATE].
  - Both are against **generator-level visible MET** in tt̄ at PU 200. L1 only: the HLT TDR is not retrievable.

| gen. MET [GeV] | 150 | 175 | 200 | 225 | 250 | 275 | 300 | 350 | 400 |
|---|---|---|---|---|---|---|---|---|---|
| Fig. 3.125 (interpolated) | 0.62 | 0.80 | 0.90 | 0.95 | **0.975** | 0.984 | 0.983 | 0.995 | 0.98 |
| erf through Table 4.1 (μ 128, σ 56.18 GeV) | 0.652 | 0.799 | 0.900 | 0.958 | 0.985 | 0.996 | 0.999 | 1.000 | 1.000 |
| same, 50 % point shifted by one width | 0.272 | 0.435 | 0.611 | 0.766 | 0.879 | 0.947 | 0.980 | 0.998 | 1.000 |
| v1 function 0.98·Φ((x−200)/20) | 0.006 | 0.10 | 0.49 | 0.88 | 0.974 | 0.980 | 0.98 | 0.98 | 0.98 |

Checks:
- The v1 function reproduces STR's 0.974 at 250 GeV.
- The erf reproduces 0.5 / 0.9 at 128 / 200 GeV by construction.
- The digitised curve crosses 50 % / 90 % / 97.5 % at 136 / 199 / 250 GeV. Its 90 % point agrees with Table 4.1 (200).
  Its 50 % point is 8 GeV above Table 4.1's 128; the table and the figure come from different menu studies.

**Facts for the branch decision (S2-e, decision needed):**
- (1) The curve is sourced with figure and page, so the first branch of S2-e applies to the curve.
- (2) The source states **no uncertainty**; the figure's statistical bars are ≤ 0.01 below 350 GeV. So the nuisance
  "shifted by the uncertainty read from the source" has no source.
- (3) At the offline threshold of 250 GeV the curve is at 0.975 ± 0.01. It reaches 0.98–1.0 from about 270 GeV.
  Whether this counts as "plateau reached below 250 GeV" depends on a plateau definition that STR does not fix.
- (4) The pre-declared wide nuisance of the not-sourced branch, evaluated with the 2-point erf, is −10.6 % at 250 GeV,
  −4.9 % at 275 GeV and −1.9 % at 300 GeV (absolute efficiency).
- (5) The variable is gen-level visible MET. How L1 PUPPI MET treats quirk tracks is not addressed by the source.

Options:
- (a) Nuisance from the plotted statistical bars only (≈ ±0.01).
- (b) The pre-declared wide nuisance (the "parametrised, not sourced" size) applied to the sourced curve.
- (c) Raise the offline threshold to ≈ 275–300 GeV, where (a) and (b) both become small.

The choice precedes A (§4.1), so it is not made here.

### 2.7 S2-f: infracolour Coulomb correction per mass (R-12: not sourced)
`src/s2/s2f_infracolour.py` → `outputs/s2/s2f_infracolour.json` (campaign p2-b-s2f, landau, 1 job) [VERIFIED run; form
from STR §4.14 (a′), not a literature value].
- **Form:** δ(β) = C_F α_IC (π/(2β) − 4/π), with C_F = 3/4 and α_IC(m) = 2π/(b₀ ln(m/Λ)), b₀ = 22/3.
- **Averaging:** δ is averaged with the nominal weights over β, the quirk speed in the pair rest frame from the hard
  (LHE) momenta. Inputs: all matched events of the 100k-LHE inclusive samples.
- **Substitution check:** α_IC(200 GeV, 1 keV) = 0.0448; δ = 3.26 / 6.28 / 13.32 % at β = 0.7 / 0.5 / 0.3, as in STR.
- **Limiting case:** α → 0 gives δ → 0.

| point | events | β median (16–84 %) | weight at β < 0.1 | ⟨δ⟩ at 0.45 keV | 1 keV | 5 keV | vector-current form, 1 keV |
|---|---|---|---|---|---|---|---|
| E 200 | 55,300 | 0.64 (0.41–0.83) | 0.29 % | +5.45 % | **+5.68 %** | +6.20 % | +5.90 % |
| E 500 | 46,170 | 0.60 (0.38–0.78) | 0.33 % | +5.91 % | **+6.14 %** | +6.68 % | +6.40 % |
| E 1000 | 42,296 | 0.54 (0.34–0.71) | 0.49 % | +6.77 % | **+7.03 %** | +7.62 % | +7.34 % |
| E 1500 | 40,824 | 0.49 (0.31–0.66) | 0.66 % | +7.66 % | **+7.94 %** | +8.60 % | +8.29 % |
| Ẽ 500 | 45,227 | 0.72 (0.54–0.85) | 0.01 % | +3.46 % | +3.60 % | +3.91 % | +3.73 % |

- **Source: "not sourced".** Kang–Luty–Nasri (arXiv:0805.4642, p. 8–9) state that the LO cross sections omit the
  infracolour/QCD Sommerfeld enhancement, that it "will increase the cross section near threshold", and that it needs a
  more detailed study. They give no number. Later quirk papers (2404.13814, 2108.06748) do not treat it (#29).
- **Consequence (STR §6.4):** one-sided upward band on the theory line, σ_norm not raised (the default).
- **Caveats** (stated in STR, not resolved here):
  - The Ẽ number uses the S-wave form, but the scalar is produced in a P wave and needs its own factor. The Ẽ row is
    therefore not a valid estimate of its own correction.
  - The scale of α_IC (m against m·β) is an open choice.
  - Below β ≈ 0.1 the O(α) expansion is least reliable, but that region carries ≤ 0.7 % of the weight.
- **Size comparison:** the band is larger than the NLO scale envelope at every mass (+1.5…+2.9 %) and larger than the
  PDF4LHC21 PDF error up to ≈ 700 GeV.

### 2.8 FxFx (S2-c piece): on hold
Measured (Sebastian, campaigns p2-b-s2-fxfx-*):
- Compile: 8.6 min.
- MINT step 0: ≈ 30 min of compute for 56 channels on one core (P1 channels up to 99 s each).
- First launch per mass: ≈ 70–80 min on one core [ESTIMATE].
- Lowering req_acc does not shorten step 0.
- Event batches from saved grids would fit 30 min.

**Status: exception granted by the user on 2026-11-17; prepared; NOT submitted.** The exception covers two single-core
first-launch jobs of ≈ 1.5 h, at 500 and 1,500 GeV; later event batches from the saved grids stay ≤ 30 min.

**Why not submitted:** the runner hard-codes the 30-minute limit and rejects the campaign:
- `tools/runner/qv2run/paths.py:24` sets `MAX_JOB_SECONDS = 1800`;
- `tools/runner/qv2run/campaign.py:108-110` rejects `timeout_s` > 1800 with "outside (0, 1800]".

The orchestrator makes the runner change after the pilot completes (≈ 19 Nov). Proposed change (≈ 6 lines): in
`campaign.py`, accept a per-job `timeout_exception: {max_s, source}` on the SSH mechanism, cap it at 7200 s, use it
instead of MAX_JOB_SECONDS, and write it into the marker. No channel-farming driver was built.

**Prepared:**
- `s2_job.py fxfx` gained `--save-procdir`: after the first launch, the whole node-local base dir (model, compiled
  process dir, MINT grids, stamps) is written as `<tag>.procdir.tar.gz`, which the runner publishes to cajuela.
- It also gained `--restore <tar.gz>`: it unpacks such a tarball on any worker that has no compiled dir.
- Campaign `tools/campaigns/p2-b/p2-b-s2-fxfx-c.json`: compile at E 500 and E 1500, ≤ 30 min each, valid. It is queued
  on maxwell after p2-b-s2-nll by `src/s2/queue_maxwell_fxfx.sh` (log `maxwell:/home/scratch/jdochoa/drivers/queue_maxwell_fxfx.log`).
  That script then tries p2-b-s2-fxfx, logs the runner's rejection and stops.
  The compile jobs started on maxwell at 17:37 on 2026-11-17 (≈ 9 min each; check:
  `qv2run status tools/campaigns/p2-b/p2-b-s2-fxfx-c.json`).
- Campaign `tools/campaigns/p2-b/p2-b-s2-fxfx.json`:
  - jobs `fxfx-e500-grids`, `fxfx-e1500-grids`;
  - `timeout_s` 6000, with `timeout_exception.source` = "user, 2026-11-17";
  - first launch at the default accuracy with 2,000 events, `--save-procdir`;
  - outputs timing.json, lhe.gz, npz (empty), aux.tar.gz, procdir.tar.gz.

**Commands after the runner change** (maxwell; the compiled dirs from p2-b-s2-fxfx-c are node-local there):

    R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
    ssh -x maxwell "$R/bin/qv2run status $C/p2-b-s2-fxfx-c.json"       # must be 2/2 done (else launch it first)
    ssh -x maxwell 'pgrep -fc "qv2run job"'                              # must be <= 3
    ssh -x maxwell "$R/bin/qv2run ssh launch $C/p2-b-s2-fxfx.json --nodes maxwell --max-per-node 1 --on maxwell"
    $R/bin/qv2run status $C/p2-b-s2-fxfx.json --live -v                 # ≈ 1.5 h per job, one at a time

Then event batches as a new campaign (e.g. `p2-b-s2-fxfx-gen`), each ≤ 30 min, on any worker:

    python3 -I .../src/s2/s2_job.py fxfx fxfx-e500-gen-NN E 500 <nev> --stage gen --shower \
        --restore /nfs/cajuela/jdochoa/quirks_v2/data/p2-b-s2-fxfx/000/fxfx-e500-grids.procdir.tar.gz

with `QV2_LOCAL_ENV=1`. Size `<nev>` from the grids job's timing.json: the event step after the grids.

**What the successor must read and compute:**
- f₂₀₀^FxFx = Σw[p_T(QQ̄) > 200]/Σw over the showered FxFx npz files, with signed MC@NLO weights. Same formula and
  statistical error as `f200.py` (`frac`). Target ≥ 2 % statistics at 500 and 1,500 GeV.
- Compare with the nominal ± band of §2.4. If it lies outside, enlarge the band to contain it (STR §4.14 (b)) and
  update κ for T1.
- Record the CPU at wall × 1 core: the event-mode accounting artefact of §1.

## 3. P1: thickness-law clean-ups

### 3.1 Readings (Sebastian, campaign p2-b-p1-run on new events; unchanged)
P1 runs on new events: v1's P1 event inputs and the T2 kinematics cache are not in the repo (Sebastian §3.1).
- **P1-b at 5 keV**, 969 events: paired median (on − off) of c is +0.00085 ± 0.00051 (1.7σ) overall and
  +0.0052 ± 0.0041 (1.3σ) for k_B ≥ 6. Reading: **"B* attribution not supported at 3σ"**.
- **P1-b at 1 keV**, 300 events × 5 points: all compatible with zero (≤ 2σ). Reading **met**.
- **P1-c: FAIL.** The rule fails at three of five points:
  - E 200: +1.58 % (relative rule);
  - E 1000: 2.6σ;
  - Ẽ 500: +1.96 % and 2.2σ.
- **P1-a test 2** (44-bit truncation, as pre-declared): KS p = 1.6×10⁻⁷ (E 500) and 2.8×10⁻⁶ (E 1000). Reading **"not
  the floor pattern"**. Test 1 is **not done** ([DT3]).
- **P1-d:** 9 of 30 cells pass v1's 1.5 % rule. The Linux M2 rerun agrees to ≤ 10⁻¹².
- **Cost:** 6.1 core-h against the 51 planned. The 5 keV run costs 23.8 s/event for 4 kernel runs (E 500), against
  STR's 2 × 67.8 s.

### 3.2 Floor diagnostic, round-to-nearest (labelled: **diagnostic, not a pre-declared test**)
Campaigns: p2-b-p1-rn (4 jobs, landau, 0.15 CPU-h) and p2-b-p1-rneval. Code: `src/p1/nm_kernel_rn44.py`,
`nm_kernel_rn47.py`, `p1_rn_eval.py`. Output: `outputs/p1/p1_rn_eval.json`.
- **Set-up:** the same 40 events per point, settings, fractions and estimator as the t44 runs.
- **Rounding:** mdot rounds every product and the result to nearest (ties to even). The rounding was unit-checked on
  einstein: the maximum relative error equals 2⁻⁴⁴ and 2⁻⁴⁷.

**Finding on the specification (v1 NEAR_MISS_IMPULSE.md l.735; STR §4.15):**
- The spec reads "truncate … to 44 bits (u′ ≈ 64u)". A 44-bit significand has u′ = 2⁻⁴⁴ = **512 u** (u = 2⁻⁵³).
- 64u is a **47-bit** significand.
- The prediction "the same Δc at 8× larger ε⊥" is √64 = 8, so it presumes 64u.
- The pre-declared test therefore ran at 8× the precision loss its prediction assumed: 512u with rounding, ≈ 1024u
  with truncation.

| kernel | median Δc(2) | Δc(2.5) | Δc(4) | Δc(20) | KS p: nominal Δc(20) vs kernel Δc(2.5) | paired (kernel − nominal) at k = 2.5 |
|---|---|---|---|---|---|---|
| E 500 nominal (float64) | 0.00061 | 0.00068 | 0.00070 | **0.00323** | — | — |
| E 500 t44 (truncation) | 0.0157 | 0.0199 | 0.0390 | −0.355 | 1.6×10⁻⁷ | +0.0205 ± 0.0049 |
| E 500 rn44 (nearest, 512u) | 0.0215 | 0.0262 | 0.0504 | −0.335 | 1.4×10⁻¹⁰ | +0.0265 ± 0.0059 |
| E 500 **rn47 (nearest, 64u)** | 0.0032 | **0.00425** | 0.0081 | 0.072 | **0.53** | +0.0039 ± 0.0010 |
| E 500 dd (double-double mdot) | 0.00056 | 0.00065 | 0.00068 | 0.00241 | — | −0.00009 ± 0.00001 |
| E 1000 nominal | 0.00071 | 0.00083 | 0.00126 | **0.00802** | — | — |
| E 1000 t44 | 0.0379 | 0.0521 | 0.0726 | −0.358 | 2.8×10⁻⁶ | +0.052 ± 0.012 |
| E 1000 rn44 | 0.0632 | 0.0681 | 0.106 | −0.371 | 1.2×10⁻⁷ | +0.067 ± 0.024 |
| E 1000 **rn47** | 0.0081 | **0.0109** | 0.0211 | 0.035 | **0.47** | +0.0099 ± 0.0034 |
| E 1000 dd | 0.00055 | 0.00059 | 0.00090 | 0.00564 | — | −0.00013 ± 0.00003 |

(events used: 36–40 per kernel and point; paired errors from 2,000 bootstrap resamples)

Readings of the diagnostic (no verdict change):
- **Rounding mode is not what made test 2 fail.** rn44 behaves like t44: Δc(20) ≈ −0.34, and Δc at k ≤ 4 is 20–100×
  the nominal. Sebastian's caveat (truncation bias) is therefore not the explanation.
- **The bit count is.** At u′ = 64u (rn47), the nominal Δc(20) distribution reappears at k = 2.5, i.e. at 8× larger
  ε⊥: KS p = 0.53 and 0.47 with 40 events. The medians are 1.3× and 1.4× the nominal Δc(20).
- Under the spec's own scaling the expected ratio is 1.0. With the 1/ln k of the c_k definition it is 3.3. The
  observation lies between the two.
- Reduced precision raises Δc(2.5) by +0.0039 ± 0.0010 and +0.0099 ± 0.0034, which is the size of the nominal Δc(20).
- **Supports, as a diagnostic, the floor interpretation of the nominal Δc(20):**
  - the 64u pattern matches;
  - the double-double Minkowski product removes ≈ 1/3 of Δc(20) (3–4σ, Sebastian).
- **Does not replace floor test 1:**
  - only 40 events per point;
  - KS power is limited;
  - "same distribution" at p > 0.05 is the pre-declared reading form, applied here to a test that was not
    pre-declared.
- **Decision needed:** whether the spec inconsistency (44 bits ≠ 64u) and the rn47 result are recorded beside the
  pre-declared "not the floor pattern" (§6, item 3).

## 4. Generator spread: Herwig against Pythia ([DP5]; numbers for channel (iii))
Campaign p2-b-hw-mb (maxwell, 10⁶ + 10⁶ inelastic events, 14 TeV), output `outputs/dp5/mb_compare.json` [VERIFIED;
Poisson errors]. Sebastian §4 has the full table.

**Generators:**
- Herwig 7.3.0: LHC-MB + Diffraction snippets, CT14lo.
- Pythia 8.312: CP5, SoftQCD:inelastic.

Common stable definition: cτ > 1000 mm. Selection: charged particles with p_T > 0.1 GeV.

| quantity (Herwig / Pythia) | \|η\| < 1 | 1 < \|η\| < 1.5 |
|---|---|---|
| charged multiplicity per event | 0.946 ± 0.0004 | 0.919 ± 0.0005 |
| K/π − 1, p_T 0.5–0.7 / 0.7–1 / 1–1.5 / 1.5–2 / 2–3 GeV | +23.9 / +32.7 / +34.3 / +30.5 / +23.5 % (±0.4–0.9) | +21.5 / +31.4 / +33.7 / +29.7 / +25.4 % |
| K/π − 1, 0.1–0.5 GeV | +8.5 … +12.0 % | +9.2 … +10.5 % |
| p/π − 1, 0.7–3 GeV | +41 … +54 % | (JSON) |
| charged p_T spectrum ratio, 0.5–0.7 → 3–5 GeV | 0.854 → 1.280 | 0.826 → 1.254 |

**Tune facts (#23):**
- Herwig 7.3's general tune is an e⁺e⁻ tune; its release note says the MB/UE retuning is "currently ongoing".
- CP5 is fitted to UE data including 13 TeV.

So the spread mixes the hadronisation model with tune quality. It is a **generator spread, not an uncertainty**. R-19
(published K/π differences or a measured MB K/π) is still open, so no data anchor is attached. How the spread enters
rate_DIF is channel (iii)'s decision.

## 5. Retrievals R-1…R-20 (REF-2), with STR §6.4 deadlines (day 0 = 2026-11-16)

| id | need | status | where (retrieval_log #) | consequence / note | deadline |
|---|---|---|---|---|---|
| R-1 | right-selectron NLO(+NLL) tables | closed: NLO+NLL only, no NLO column | #16 | validation 2 via self-run Resummino (qualifier) | done |
| R-2 | L1/HLT MET turn-on + uncertainty | L1 closed (Table 4.1 p. 210; Fig. 3.125 p. 188); **HLT not sourced** (CMS-TDR-022 not retrievable); **uncertainty not stated** | #11, #31 | S2-e decision (§2.6) | day 5 ✔ |
| R-3 | jet response/resolution, leptons, PU-200 MET, external MET figure | closed (ATLAS notes, CMS NOTE-2018/006 supplied by the user); **jet-response tail not sourced** | #12, #14, #15, #20 | MET hand-over §7 | day 5 ✔ |
| R-4 | multijet fraction after MET + jet (monojet-type) | open | — | B4 validation (c) | before Phase 3 use |
| R-5 | SM K-factors at 14 TeV | open | — | B4-d | before Phase 3/4a use |
| R-6 | cosmic flux, beam halo | partial (repo only, #5) | #5 | B7 | before Phase 3 |
| R-7 | timing-layer resolution, degradation, collision-time spread, tail | resolution closed: 30–40 ps at start → 50–60 ps at end, luminosity-weighted average 40–50 ps; 40 ps used for full-luminosity physics; spread rms 180–200 ps; vertex time ≈ 10 ps. **Tail: not sourced** (figure shape only) | #24 (MTD TDR p. 2, 5, 198, 207) | time-tag credit can rest on the sourced range; tail variation has no source | day 15 ✔ |
| R-8 | PV identification efficiency at ⟨μ⟩ = 200 | closed (CMS NOTE-2018/006 Fig. 6 p. 6) | #20 | ε_PV | done |
| R-9 | HL-LHC luminosity uncertainty | closed: 1 % (CMS NOTE-2018/006 Table 1 p. 29, "guidelines") | #20 | luminosity nuisance | done |
| R-10 | R3 statistical method and systematic table; R2 method | open | — | Table 6.1 | before Phase 4a |
| R-11 | Barbashov; Knapen et al. III.D | open | — | C3 | before Phase 5 |
| R-12 | infracolour Sommerfeld treatment | **not sourced** (KLN 2008 p. 8–9 names it, no number) | #29 | one-sided band (S2-f default) | freeze ✔ |
| R-13 | heavy slow / non-helical particles as muons; lepton veto | open | — | S1-f, [L11] | before S1-f |
| R-14 | tracker readout time window | partial: simulation window ±12.5 ns (one crossing), pixel "in-time threshold"; **late-hit acceptance not sourced** | #28 | limitation, limit as a function of the assumption | freeze ✔ |
| R-15 | hit resolution per layer type | partial: OT p/√12 (26.0 µm 2S, 28.9 µm PS strips; macro-pixel 1.5 mm/√12); IT pitch 25×100 µm², no hit-resolution number; **no uncertainty** | #25 | no nuisance; robustness μ₉₅ shift reported (Df-7) | day 15 ✔ |
| R-16 | hit efficiency | partial: > 99.5 % OT, ≈ 100 % IT (simulation), > 99 % MPA beam test; **no uncertainty** | #25 | as R-15 | day 15 ✔ |
| R-17 | material budget, uncertainty, composition | budget from Fig. 6.2 p. 98: x/X₀ ≈ 0.2 (η ≈ 0) to ≈ 0.4 (η ≈ 1) [ESTIMATE ±0.05]; validated by reproducing Run 1; **no uncertainty** | #26 | as R-15; B1-c, [L2] get the scale only | day 15 ✔ |
| R-18 | noise / out-of-time occupancy, tracker and timing layer | closed (specification / prototype): pixel noise < 10⁻⁶; OT no noise hits down to 10⁻⁵; BTL occupancy ≈ 7 % at PU 200; DCR cell occupancy < 2–3 %; ETL ≤ 2 % | #27 | B1-g, B3-c | day 15 ✔ |
| R-19 | published string/cluster K/π differences or measured MB K/π | open (generator spread measured instead, §4) | — | [DP5], SY-7 | before the phase that uses it |
| R-20 | ATLAS/CMS non-helical / quirk results; HL-LHC quirk projections 2020–2026 | open; by-product: 2404.13814 (FASER quirk timing, NLO K at 13 TeV) found | #29 | paper §9 | before Phase 4a |

**Access notes:**
- CDS is bot-protected, and nothing was circumvented.
- The MTD, Tracker and L1 TDRs were obtained through INSPIRE's public file links.
- The CMS HLT TDR (CMS-TDR-022) is still not obtainable that way. The user could supply it by hand, as for the CMS note.

## 6. Strategy-revision inputs

1. **MET-model validation (B4-b).**
   - **Phase 1 assumed:** a public soft-term parametrisation could be validated against an independent PU-200 figure.
   - **Phase 2 found:** the ATLAS 2013 European-Strategy formula is ×2–4 above both PU-200 full-simulation figures
     (ATL-PHYS-PUB-2019-005 Fig. 18; CMS NOTE-2018/006 Fig. 35). With the CMS note, options A–C each pair a PU-200
     parameter source with an independent PU-200 figure (§7). No source gives a non-Gaussian jet-response tail.
   - **Implications:** option D (the 2013 formula) would fail the validation. The tail variation width has to be set
     without a source before the freeze, and is labelled as such.
2. **P1 on new events.**
   - **Phase 1 assumed:** v1's events would be reused.
   - **Phase 2 found:** v1's P1 inputs are lost.
   - **Implications:** all P1 comparisons with v1 are statistical. The P1 cost fell from 51 to ≈ 6 CPU-h.
3. **Floor test 2 specification.**
   - **Phase 1 assumed** (from v1): "44 bits (u′ ≈ 64u)", with the floor pattern predicted at 8× larger ε⊥.
   - **Phase 2 found:** 44 bits is u′ = 512u. At the 64u the prediction presumes (47 bits, round-to-nearest), the
     nominal Δc(20) pattern reappears at k = 2.5 (KS p ≈ 0.5, diagnostic). Rounding mode is not the cause of the failed
     test.
   - **Implications:** the pre-declared reading "not the floor pattern" stays as recorded. Whether the inconsistency and
     the diagnostic are stated beside it in the paper is a decision for the orchestrator or the user.
4. **Trigger (S2-e).**
   - **Phase 1 assumed:** a public curve with an uncertainty.
   - **Phase 2 found:** a curve with no stated uncertainty; L1 only; against gen-level visible MET; 0.975 at 250 GeV.
   - **Implications:** the nuisance size and a possible threshold change must be decided before A (§2.6).
5. **FxFx.**
   - **Phase 1 assumed:** 2 × 20 CPU-h in 30-minute jobs.
   - **Phase 2 found:** the first launch needs ≈ 70–80 min on one core.
   - **Implications:** the user granted the exception on 2026-11-17, but the runner hard-codes 1800 s. Until the
     runner change (after the pilot, ≈ 19 Nov) f₂₀₀'s band has no FxFx term, and the runner needs a sanctioned
     exception mechanism (§2.8).
6. **Resummed normalisation (S2-b).**
   - **Phase 1 assumed:** the (NLO+NLL)/NLO ratio is taken from the public tables.
   - **Phase 2 found:** the tables have no NLO column.
   - **Implications:** the ratio comes from self-run Resummino for the scalar and is applied to E (flagged assumption).
7. **Published quirk K-factors.**
   - **Phase 2 found:** arXiv:2404.13814 (p. 6) quotes K = 1.33 / 1.45 for E at 200 / 1000 GeV, 13 TeV, settings not
     stated. Ours (validated) is 1.163 / 1.178 at 14 TeV with one PDF set for LO and NLO; v1 used 1.110.
   - **Implications:** the paper must define K explicitly (same PDF in LO and NLO) when comparing with the literature.
     This is not a validation failure.
8. **Detector nuisances (B6-d).**
   - **Phase 1 assumed:** public Phase-2 numbers would size the nuisances.
   - **Phase 2 found:** values exist but no uncertainties: hit resolution, hit efficiency and material (R-15–R-17).
   - **Implications:** STR §6.4 branch: no nuisance; the robustness μ₉₅ shifts are reported beside the limit and named
     in the abstract-level limitations if above 10 %.
9. **S2-f size.** The one-sided infracolour band (+5.7 % to +7.9 % for E at 1 keV) exceeds the NLO scale envelope at
   every mass. As a one-sided band it does not change the nominal, but it is the largest single theory band below
   ≈ 700 GeV.
10. **Unit costs.**
    - MLM 0–2j at ≈ 40 ms per LHE event (not 50).
    - Re-shower + conversion ≈ 33 ms per event (not 21 ms: STR's 21 ms is the shower alone).
    - The infracolour S2-f needs no CPU.
    - Table 4.0 rows can be updated (§8).

## 7. Hand-over for the Phase-3 MET model (no recommendation; details Sebastian §1.1–1.8)

| source | quantity | sample / PU | validity range stated | tag |
|---|---|---|---|---|
| CMS NOTE-2018/006 Fig. 25 p. 16 | jet response resolution vs p_T^Gen, 3 η bins | AK4 PF+PUPPI, PU 200 | p_T 30–500 GeV; \|η\| < 1.3, 1.3–1.7, 1.7–2.8 | ESTIMATE (±0.01) |
| CMS NOTE-2018/006 Fig. 35 p. 21 | recoil u_∥, u_⊥ widths vs PU density | Z→μμ, PUPPI, PU 200 | density 0–2 /mm (mean 1.4) | ESTIMATE (±1 GeV) |
| CMS NOTE-2018/006 Fig. 34 p. 21 | MET shape incl. tail | Z→μμ, PU 200 | 0–120 GeV | ESTIMATE (±20 %/bin) |
| CMS NOTE-2018/006 Table 1 p. 29 | JES 1–2.5 %, JER 3–5 %, unclustered ±10 %, lepton ID 0.5–2.5 % | guidelines | as stated | VERIFIED (read) |
| ATL-PHYS-PUB-2019-005 Fig. 18 p. 21 | RMS(E_x,y^reco − E_x,y^true) vs ΣE_T | tt̄, ⟨μ⟩ = 200 | ΣE_T 0.35–4.5 TeV | ESTIMATE (±0.5 GeV) |
| ATL-PHYS-PUB-2013-004 eq. 2–3, Table 6 | jet resolution N, S, C | μ ≤ 140 (μ = 200 extrapolated) | anti-k_t 0.4 | VERIFIED read; μ = 200 ESTIMATE |
| ATL-PHYS-PUB-2013-004 §8 | Gaussian MET formula | μ-dependent | Run-1 extrapolation | ×2–4 above PU-200 figures |
| CMS L1 TDR Table 4.1, Fig. 3.125 | L1 MET turn-on | tt̄, PU 200 | gen MET | §2.6 |

| option | parameter source | independent PU-200 validation figure | tolerance |
|---|---|---|---|
| A | CMS Fig. 25 (jets) + Fig. 35 u_⊥ (soft term) | ATLAS 2019-005 Fig. 18 | ±0.5 GeV reading |
| B | CMS Fig. 25 + Fig. 35 u_⊥ | CMS Fig. 35 u_∥ and Fig. 34 (same note, other figures) | ±1 GeV / ±20 % per bin |
| C | ATLAS 2013-004 jets (extrapolated) + 2019-005 Fig. 18 soft term | CMS Fig. 35 / Fig. 34 | ±1 GeV / ±20 % |
| D | ATLAS 2013-004 jets + 2013-004 §8 MET formula | ATLAS Fig. 18 or CMS Fig. 35 | would fail (×2–4) |

In every option the **jet-response tail is not sourced** (#14, #20).

## 8. Measured unit costs against STR §4.0
| unit | STR §4.0 value (prov.) | measured | basis (VERIFIED unless noted) |
|---|---|---|---|
| MLM 0–2j generation + shower (QED FSR) + conversion, per LHE event | 50 ms (G) | **39.7 ms** (production, 20k-event chunks); 41 ms (timing) | p2-b-s2c-inc: 5.51 CPU-h / 500,000 LHE; p2-b-s2-mlmtime |
| MG fixed cost per launch (MLM survey/refine) | — | 72–99 s | p2-b-s2-mlmtime |
| Pythia re-shower + npz conversion, per event and variant | 21 ms shower only (M) | **32 ms** per event and variant (shower + conversion) | p2-b-s2c-rs (2 variants × 20k events per job) |
| NLO fixed-order K at one mass (LO + NLO + PDF reweighting) | ≈ 2 CPU-min + 3 once (M) | 6.7 CPU-min (CT18NLO, 59 members), 5.1 CPU-min (PDF4LHC21) | p2-b-s2-kscan 2.00 CPU-h, p2-b-s2-kscan-p4l 1.52 CPU-h, 18 masses each |
| FxFx 0–1j first launch per mass | 20 CPU-h per mass (G) | ≈ 70–80 min on one core for the first launch [ESTIMATE]; compile 8.6 min | p2-b-s2-fxfx-diag2 (wall-charged) |
| Resummino LO+NLO / NLO+NLL per mass | — | ≈ 20 s / ≈ 130 s (example spectrum) | p2-b-hw-smoke kref jobs; p2-b-s2-nll: 2,416 CPU-s for 28 (mass, set) points = **86 s per mass** for LO + NLO + NLO+NLL (decoupled spectrum) |
| Pythia minimum bias per event | 2.0–2.5 ms (M) | 2.9 ms (incl. init, smoke) | p2-b-hw-smoke |
| Herwig 7.3 minimum bias per event | — | 11 ms (incl. init, smoke) | p2-b-hw-smoke; production p2-b-hw-mb 2.96 CPU-h for 10⁶ + 10⁶ |
| P1 paired B*-off, 4 kernel runs per event, 5 keV | 2 × 67.8 s (D) | 23.8 s (E 500), ≈ 17 s (E 1000) | p2-b-p1-run |
| P1 floor run, 5 fractions, s = 1/9, per event and kernel | — | 1.0–2.7 s (nominal ≈ 1.1 s; reduced-precision kernels ≈ 2–2.7 s) | p2-b-p1-run, p2-b-p1-rn (40 events per job) |
| f₂₀₀ evaluation (all points, all variants) | — | ≈ 11 CPU-s, 70–130 s wall (NFS read + sha256) | p2-b-s2c-f200t |
| S2-f (β average, 5 points × 8 Λ) | 0 (no extra CPU) | ≈ 1 CPU-min | p2-b-s2f |

## 9. Sample inventory (new samples of channel (ii))

| sample | campaign | content | files | schema |
|---|---|---|---|---|
| inclusive MLM 0–2j, E 200/500/1000/1500, Ẽ 500 | p2-b-s2c-inc | 5 × 20,000 LHE per point; nominal shower CP5, qCut 45, QED FSR | `data/p2-b-s2c-inc/<shard>/{f,s}inc-m<m>-c<k>.{lhe.gz, nom.npz, json, aux.tar.gz}` | npz per `sim/scripts/convert_hepmc.py` docstring: p_qp, p_qm, p_qp_hard, p_qm_hard, p_qq_hard [N,4] (E, p) GeV; vtx; recoil, recoil_eta5, nu [N,4]; jets [N,4,4]; njet, n_me; w [N] (fb/event, N_IC = 1, Σw = σ_matched); wvar [N,211] + wvar_names (9 scale, 59 CT18NLO members, merging 45/67.5/90, AUX); derived gamma_star, cstar, bg_pair, eta_pair, y_pair, pt_pair, m_pair; meta mq, spin, sigma_lhe_fb, nlhe, tag. Rows: events with non-zero weight at any merging scale (55–67 % of LHE events) |
| re-showers | p2-b-s2c-rs | same LHE; qCut 30, qCut 60, Monash, FSR off | `data/p2-b-s2c-rs/<shard>/*.{qc30,qc60,monash,nofsr}.npz` + `*.rs.*.json` | same npz schema |
| P1 event sets | p2-b-p1-ev | \|η_pair\| < 1, p_T(QQ̄) > 200, w > 0 from s2c-inc; c_ev, k_B, ε⊥, γ* | `data/p2-b-p1-ev/000/p1ev-<pt>-l<Λ>.npz` | Sebastian §3.6 |
| P1 runs | p2-b-p1-run, p2-b-p1-rn | per-event Δs per field/fraction and kernel | JSON | `src/p1/p1_runs.py` docstring |
| MB generator comparison | p2-b-hw-mb | per-job histograms (π, K, p, charged) in p_T × \|η\| | JSON | `src/herwig/mb_species.py` |

**Data quality:**
- Weights are non-trivial (MLM): w = 0 rows exist for other merging scales and are kept.
- The scale and PDF member-0 columns reproduce the nominal f₂₀₀ exactly (check in f200.json).
- The σ_LHE of the timing samples agree with v1 (Sebastian §2.1).
- No unphysical values were met in the quantities used (β ∈ (0, 1), no β = 0 rows).

## 10. Open issues
- FxFx (S2-c): exception granted; submission waits for the runner change (§2.8, commands there).
- S2-e: nuisance branch and threshold.
- P1-a test 1 not done ([DT3]).
- HLT TDR (R-2 HLT) not obtainable automatically.
- R-4, R-5, R-6, R-10, R-11, R-13, R-19, R-20: open with later deadlines.
- Ẽ needs a P-wave Sommerfeld factor (S2-f).
- The scalar → fermion assumption of the resummed ratio.
- The cross-check of f₂₀₀ against channel (i)'s stitched σ(p_T > 200), whose 100k E 200 result has not reached me
  (§2.4).
- Tune dependence of f₂₀₀ at 1–1.5 TeV (+4.8 %, +5.4 % at 3.5–4.2σ) dominates the band there.

## 11. Self-review against `phase2_exploration/CLAUDE.md`
The template checklist is written for a data analysis. The study overrides apply (simulation only, no RAG corpus,
literature from public sources). Item by item for channel (ii):

| check | status |
|---|---|
| Plan first | yes: plan in the session log before any job (08:18) |
| Sample inventory with schema | §9: every new sample with campaign, files and npz schema; event counts from markers and chunk JSONs |
| Data quality | §9: non-trivial MLM weights understood (w = 0 rows for other merging scales); central weight columns reproduce the nominal; σ_LHE against v1; no unphysical β or p_T |
| Object definitions from the corpus | not applicable: no corpus (override). Public sources are cited instead (§5, §7) |
| Data/MC comparisons | not applicable: no data. Generator against generator (§4) and code against code (§2.1) instead |
| Variable survey, baseline yields after preselection | not channel (ii)'s: no selection-dependent signal quantity may be computed (BL-1). Not done, by rule |
| Data archaeology: weights | yes (§9) |
| Data archaeology: MC parameters | yes: generator, tune, PDF, √s = 14 TeV, cards (§2, §9) |
| Data archaeology: truth level | yes: hard and showered quirk momenta, recoil, jets (§9) |
| Data archaeology: strategy-revision gate | §6, ten items in "Phase 1 assumed / Phase 2 found / Implications" form |
| Experiment log updated | yes (experiment_log.md, 2026-11-17 block) |
| Figures and plotting rules | no figures made in this session. Tables only; rendered source pages stay in `/var/tmp/jdochoa/edgar/retr/` |
| PDF build test | not channel (ii)'s (not in the brief's channel list) |
| No number from memory | every constant cited (retrieval_log, STR line, file) or computed in a script. Φ⁻¹(0.9), Φ⁻¹(0.95) and 2⁻⁴⁴ are computed, not quoted |
| Tags | VERIFIED / ESTIMATE / UNVERIFIED on each number. By-eye readings are ESTIMATE |
| No parameter tuned to a reference | none: the turn-on, MET and material numbers are readings; the f₂₀₀ band uses fixed variations; nothing dropped for size (the E 1000 Monash shift enters as measured) |
| Rules: no git, no subagents, compute through the runner, nothing heavy on einstein | kept. Einstein ran only stdlib scripts on JSON and text (nice 19) and `pdftotext`/`pdftoppm` on downloaded documents |
| Self-check of limiting cases | S2-f α → 0; f₂₀₀ identical column → 0 shift; paired error of a sample with itself = 0; erf and v1 substitution checks; rounding unit test |
