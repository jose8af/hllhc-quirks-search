# D5 — Stage documents digest (P1 theory, Stage 2 generation, Stage 3 string, Stage 4 ACTS chain)

Investigator: Amara (Phase 1, quirks v2), 2026-11-13. Read-only digest of v1 material.
`TT = stage2_C001_quirks/theory_track`; all paths below are relative to `TT/` unless they start with `book/`,
`publication_plan/` or `analyses/`. Plan = `publication_plan/publication_plan.tex`.

Tags (AGENT_RULES): **VERIFIED** = checked by me (or by my sub-investigation) in a second file or in code, with the
check named; **ESTIMATE** = the source itself calls it an estimate/model; **UNVERIFIED** = transcribed from one document,
not cross-checked. Every number carries file:line. Nothing was rerun; no v2 signal efficiency was looked at. v1 numbers
are quoted from the tracked record only.

Scope note: sections 2 and 4 rest partly on two sub-investigations (Stage 2+3 sim; Stage 4 ACTS) whose reports I merged;
where a sub-investigation cross-checked a number in code or a second file it is tagged VERIFIED and the check is named.

---

## 1. P1 — the plane-thickness law

### 1.1 The claim
- Mechanism (`analytic/NEAR_MISS_IMPULSE.md:13-27`, v5.1). In the pair rest frame the solenoid is a weak uniform
  E* = γβ×B. Its torque gives the pair angular momentum J_odd in one half-period and removes it in the next, so the ends
  miss by b_odd = 2ε⊥ℓ₀[γ* − asinh ρ/ρ] at every odd crossing (`:135`) and meet head-on at even ones (`:401-406`). At a
  near miss the string pulls the ends sideways with σb/(2|s| artanh β*) (`:166`); its integral gives ln(ℓ_max/b) and
  rotates the oscillation axis coherently toward E*⊥ by η = ε⊥G(γ*)[ln(ℓ_max/b_odd) + K(γ*)] per period (`:188`).
- Headline law (`:284`, P-9 at `:502`): **Δs_B = (qBR/σ)·F·[ln(1/ε_B) + C]**, ε_B = qB/σ = 2.254×10⁻⁴ (B/3.8112 T)(keV/Λ)²
  (`:35`, UNVERIFIED). Model C = 0.43/1.23/1.62 at m = 200/500/1000 GeV (`:289-293`, ESTIMATE; Λ-independent *by
  construction*, `:295-296`). Local slope c = 1/[ln(1/ε_B) + C] (`:324`); 0.104 (0.098-0.112) at 1 keV, 500 GeV
  (`:340`, ESTIMATE, model on the T3 sample). The old constant-c form "ε_B[1 + c ln(Λ²/qB)]" is withdrawn
  (`:330-334`). Local exponents d ln Δs_B/d ln B = 1 − c, d ln Δs_B/d ln Λ = −2 + 2c (`:348`).
- Novelty: C1 (mechanism, log, B non-linearity, analytic η) judged NOVEL, with framework credit to Li et al.
  2002.07503 App.A (η fitted numerically), Kang-Luty 0805.4642 Eq.5.64 and Knapen 1708.02243 Eq.8-9
  (`analytic/NOVELTY_AUDIT.md:15-23`). The logarithm itself is elementary near-radial-orbit mechanics (`:20`;
  NEAR_MISS `:226-228`). Credit sentence 10 (`NEAR_MISS_IMPULSE.md:876-879`) is the "linear in the endpoint proper
  time" wording the plan's W1 list asks to fix (plan `:249`).

### 1.2 Derivation status (what is derived and what is numerical)
| item | status | source |
|---|---|---|
| reduction to CM frame; B* gives no linear-response torque | DERIVED | `NEAR_MISS_IMPULSE.md:86-101` |
| b_odd closed form; NR limit; B*-independence | DERIVED + two-solver numerics (ratio 0.9991-0.9999) | `:132-139`, `:533` |
| intermediate-region exact NG solution, retardation factor 1/artanh β* | DERIVED; slope κ measured 0.963/0.840/0.653/0.52 vs 0.968/0.845/0.658/0.535 | `:162-174`, `:536` |
| log coefficient G(γ*) | DERIVED; measured to ≤0.1-0.3 % | `:188-190`, `:537` |
| constant K(γ*) | **numerical** (ESTIMATE) except NR limit 3 ln 2 − 2 (DERIVED) | `:196-210`, `:219` |
| accumulation (rotating yo-yo model) → Δs_B | structure DERIVED, model ESTIMATE; 1-4 % for γ* ≲ 1.6, 10-35 % off for γ* > 2 | `:251-277` |
| B* effect on η (inner region) | measured, not derived (mechanism CONJECTURE); per-event c not valid for k_B ≳ 6 | `:432-459`, `:740-742` |
| scale-free property (Λ√k, B) ≡ (Λ, B/k) | DERIVED (c15) | `:355-366` |
| NG validity (b_odd ≫ 1/Λ): safe Λ ≲ 10 keV, typical ≲ 26 keV | DERIVED condition; model uncertainty 3-8 % at 30 keV ESTIMATE | `:476-486` |
| MS part of the thickness | **not derived** (user decision 2026-10-11, option (b)); MS only as a measured floor | `:761-778` |

### 1.3 Numerics and their blind protocol
- E2's campaign (`analytic/numerics/NUMERICS.md`) §0-§10 was written without opening E1's files (`:3-4`,
  `analytic/numerics/plan.md:3`); E1's c07 predictions were timestamped before M3.json, checked by the critical reviewer
  (`NEAR_MISS_IMPULSE.md:521-523`). "Blind" means blind to the derivation, **not solver-independent**: the production
  kernel `nm_kernel.py` is a line-by-line copy of `code/T3_causal.py` (bit-identical hits on 9/9 events,
  `NUMERICS.md:28`); the second solver is the conformal-gauge copy of R1 (`:29`, `:65-85`). Two-solver vs one-solver
  provenance table at `NUMERICS.md:71-82`. FU/FIX passes (§11-§14) are post-unblinding (`:357-359`).
- Headline agreements (blind): c = 0.105 ± 0.002 vs 0.104 (500 GeV, 1 keV); 0.101 ± 0.001 vs 0.100 (1 TeV); B exponent
  0.911 ± 0.003 vs 0.914; R(1/2…1/80) = 1.073/1.147/1.320/1.460 vs 1.072/1.144/1.311/1.455
  (`NEAR_MISS_IMPULSE.md:550-558`; `NUMERICS.md:241-242`, VERIFIED: same values in both files). Median Δs_B 500 GeV:
  29.1/8.17/3.80/1.55/0.46 µm at 1/2/3/5/10 keV (`NUMERICS.md:223-227`, UNVERIFIED).
- 3 keV: blind production c (0.093) was step-biased; converged c(B₀/2) = 0.084-0.089 agrees; at B₀/4, B₀/20 an excess
  of +5-6 % / +13-16 % of c remains (`NEAR_MISS_IMPULSE.md:566-583`). FIX2 decomposition: (i) a physical, cumulative B*
  part carried by k_B ≳ 5 (floor-free Δc(4) on−off = +0.0136 ± 0.0039 / +0.0125 ± 0.0038 at s = 1), (ii) a per-period
  part with the ε⊥⁻² shape of the double-precision floor but an amplitude 3.8-3.9× the CM-frame floor coefficient
  (attribution ESTIMATE, not demonstrated) (`:632-671`; `NUMERICS.md:563-613`).
- Precision floor of both double-precision solvers: b/ℓ₀ ≈ 3×10⁻⁸ (γ* ≤ 1.3), ≈ 10⁻⁶ (γ* ≥ 2) (`NUMERICS.md:54-63`,
  `:276`).
- CPU of the Stage-1 numerics: ≈ 4.5 CPU-h (M1-M5) (`NUMERICS.md:353-355`); FU 3.8×10³ s (`:359`); FIX1 8.5×10³ s
  (`:452`); FIX2 7.2×10³ s = 2.0 CPU-h (`:550`). All UNVERIFIED. Total ≈ 9 CPU-h (my sum, ESTIMATE).

### 1.4 Validity window as measured (Stage 3, MadGraph samples, 218 571 events)
Stage 3 re-measured the law on the Stage-2 MG samples (5 points E 200/500/1000/1500, Ẽ 500; 0.45-30 keV):
`sim/stage3/VALIDATION.md:59` (218 571 events, UNVERIFIED) — this is the "2.2×10⁵ events" of plan `:150`.
- Per event (conditional median) the law holds at 1-2 keV; it fails at 0.45 keV (`VALIDATION.md:23-25`). Pooled median
  r/c_ev by k_B bin (0-2/2-4/4-6/6-10/≥10) (`sim/stage3/README.md:205-213`, UNVERIFIED):
  0.45 keV +6.0/+2.0/−2.4/−7.2/−26.3 %; 1 keV +0.2/−0.1/−0.0/+0.2/−2.0 %; 3 keV −0.4/+0.8/+2.4/+3.3/+8.9 %;
  **5 keV +2.0/+6.5/+12.9/+18.6/+56.5 %**. The plan's "+6.5 % inside the safe window at 5 keV" (plan `:153`) is the
  k_B 2-4 bin at 5 keV (README `:213`; `book/review/UNRESOLVED.md:49`), VERIFIED by reading both.
- V2b revisit over the full P1 grid: **9/30 cells pass** the gate criterion (`VALIDATION.md:42`); population excess by
  regime: 0.45 keV −1.43 ± 0.51 %; 0.6 keV +0.64 ± 0.40 %; 1-2 keV +1.71 ± 0.29 %; 3-5 keV +6.22 ± 0.45 %
  (`README.md:197-201`, same in `VALIDATION.md:42`; VERIFIED, two files agree).
- Dimensionless window: law holds for median ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4, R_IT ≈ 14.6 cm; measured Λ slopes are steeper
  than −2 + 2c by 3.9-5.9σ for 0.6→1 keV at all five points (`paper/sections/04_truth_p1.tex:49-55`, UNVERIFIED).
- Above 5 keV: paired ratio 1.016 ± 0.005 (500 GeV), 1.027 ± 0.005 (1 TeV) at 10 keV (`04_truth_p1.tex:64-66`);
  NEAR_MISS carries an unmeasured, unattributed ±5 % on Δs_B (population, sign expected positive) above ≈ 5 keV
  (`NEAR_MISS_IMPULSE.md:384-389`, ESTIMATE).

### 1.5 The failed 1.5 % population gate (V2b)
- Definition, fixed before the run (`sim/stage3/VALIDATION_GATE.md:34-47`): measured c2 = (2Δs(B₀/2)/Δs(B₀) − 1)/ln 2 per
  event; prediction c_ev = 1/[ln(ℓ_max/b_odd) + K(γ*)] from `analytic/checks/c06_rotating_yoyo.pair_params`;
  statistic Dc = median(c2) − median(c_ev), paired bootstrap (2000), criterion |Dc| ≤ 2σ **and** ≤ 1.5 % at all 5 points,
  1 keV, 300 MG events per point.
- Result (`VALIDATION_GATE.md:49-55`; `sim/stage3/VALIDATION.md:41`, VERIFIED two files): E 200 +0.70 %, E 500
  **+2.00 %** (pull 2.3), E 1000 +1.07 %, E 1500 **+2.10 %** (2.2), Ẽ 500 **+3.15 %** (2.4) → FAIL. The paired median
  of (c2 − c_ev) is within ±0.001 at every point (`VALIDATION_GATE.md:49-55`, column "paired median").
- Not numerical: 10× finer step changes median c2 by ~10⁻⁵ (`:60-64`). Interpretation (ESTIMATE): a skewed, wider
  per-event c distribution (k_B ≥ 6) makes median(c2) ≠ median(c_ev) even when the paired median difference is 0; a
  zero-median symmetric scatter model reproduces +2.04 % (`README.md:199`). The same feature is in Stage 1: on the M3
  events median c2 = 0.1053 vs same-event median c_E1 = 0.1029 (**+2.4 %**), paired 5×10⁻⁵ ± 8×10⁻⁴; Stage 1's
  "≤ 1.5 %" compared against 0.104 from a *different* sample (c07) (`VALIDATION_GATE.md:72-77`). The user decided to
  proceed past the gate and record it as a finding (`04_truth_p1.tex:48`; `VALIDATION.md:41`).

### 1.6 The failed straight-string ratio at γ* = 2
Prediction η_KL/η_NG = 0.38 × 1.68 × 0.79 = 0.50; measured converged Li/causal thickness ratio 0.75 ± 0.08 (30 events,
FIX1; R2 0.69; a 10-event subset at finer step 0.96 ± 0.10) → **failed at ≈ 3σ**, significance sample-sensitive;
candidate causes (B* in the exact string; Δs ∝ η failing at γ* = 2; b_odd ratio measured only in the CM problem), none
quantified (`NEAR_MISS_IMPULSE.md:708-721`, `:510`, `:747`; UNVERIFIED). At γ* = 1.28 the Li c is within ≈ 3 % of NG
(`:240-243`).

### 1.7 The multiple-scattering floor
Δs_MS ≈ 10 / 13-16 / 17-22 / 18-28 / 12-16 µm (E 200/500/1000/1500, Ẽ 500), nearly Λ-independent; crossover Δs_B = Δs_MS
at 1.91/1.50/1.25/1.16 keV (E) and 1.59 keV (Ẽ 500); B and MS add sub-quadrature (ratio 0.80-0.97 at 1-3 keV)
(`sim/stage3/README.md:83-85`, `:193`; `sim/stage3/DECISIONS_PENDING.md:24-27`; VERIFIED: README and DECISIONS agree).
MS scaling exponent ln[Δs(M×2)/Δs(M×0.5)]/ln 4 = 0.36-0.62 vs Highland ≈ 0.5, χ² 26.0/10 (`README.md:191`). The
material per layer itself is UNVERIFIED (×0.5/×2 variations) (`paper/sections/12_limitations.tex:15-16`). Plan `:151`
"10-28 µm, dominant above 1.2-1.9 keV" matches. The detector out-of-plane resolution 23-30 µm equals this floor, so the
law is not testable at detector level (plan `:178-179`; `book/review/UNRESOLVED.md:62` notes `acts/stage4/plan.md:496`
mislabels the resolution as the MS floor).

### 1.8 The three planned P1 tests: what they are, what they need, whether code exists
**(a) Floor tests "O-1" (plan D12).** Specified in `NEAR_MISS_IMPULSE.md:731-738` (review S1-R3), approved but
**not done** in Stage 3 (`sim/stage3/VALIDATION.md:422`; `DECISIONS_PENDING.md:20-21`).
- (a1) Extended precision on a short detector: the 3-5 events with the smallest ε⊥(B₀/20), detector scaled by s = 1/27,
  at B₀ and B₀/20, step map in double-double or mpmath (≥ 30 digits). Prediction if floor: Δc(20) drops from +0.01-0.02
  to ≲ 0.001. Cost "under ~1 CPU-h" (ESTIMATE, `:733-734`); plus "1-2 days person time for an extended-precision step
  map" (`DECISIONS_PENDING.md:20-21`, ESTIMATE).
- (a2) Reduced-precision emulation: truncate the mantissa of every Minkowski product to 44 bits (u′ ≈ 64u); prediction
  if floor: the same Δc distribution reappears at 8× larger ε⊥ (3 keV at B₀/2.5) with the ε⊥⁻² shape (`:735-736`).
- Needs: events = existing Stage-1 M3/FIX2 events (seed 777 + m, `NUMERICS.md:214-215`, `:558`) or Stage-3 P1 rows;
  code = a modified kernel. **Code status: does not exist.** `grep` for mpmath/double-double/longdouble/mantissa in all
  `*.py` under TT finds nothing relevant (VERIFIED, my grep; the only hits are unrelated ACTS/finder files and a comment
  in `FU_analysis.py:105`). Starting point: `analytic/numerics/nm_kernel.py` (277 lines, numba `@njit`; all Minkowski
  products go through `mdot()` at `nm_kernel.py:33`, used at `:64, :103, :140-141, :160`), which already takes general
  uniform E and B (FIX2, `NUMERICS.md:551`). (a2) is a change to `mdot` (mask the float64 mantissa) and is the cheaper
  of the two; (a1) requires a non-numba or double-double re-implementation of the step map (ESTIMATE). The detector
  scaling s exists in `FIX2_runs.py` (`NUMERICS.md:555-557`).
**(b) The B*-off test.** Uniform lab fields E_lab = γ²β×B, B_lab = γ²[β(β·B) − β²B] give exactly (E*, B* = 0) in each pair
frame (`analytic/numerics/nm_bstar.py:1-5, :18-24`). **It has been run twice already:** Stage-1 FIX2 at 3 keV with a
detector-scale scan (`NUMERICS.md:549-613`, 2.0 CPU-h) and Stage-3 fix R1 at 5 keV on 171 events of E 500 + E 1000
(0.84 CPU-h; `sim/stage3/scripts/fix_bstar_off.py`, output `results/FIX_bstar_off.json`; `VALIDATION.md:44`). Result:
median r/c_ev B* on/off kB[0,2) +1.5/+0.3 %, [2,4) +13.5/+0.2 %, [4,6) +1.7/+2.7 %, [6,10) +31.7/+2.9 %, ≥10
+37.5/+12.2 %, all +10.3/+1.8 % (`VALIDATION.md:44`); B* off +1.8 ± 0.7 % vs production +9.7 ± 1.3 % (5.5σ, unpaired),
but paired on−off on the same events only 2.1σ (all) / 2.3σ (k_B ≥ 6) (`DECISIONS_PENDING.md:9-12`). Code exists and
is reusable; the production kernel `T3_causal_s3` has no E-field input, so B*-off runs use `nm_kernel.run`
(`fix_bstar_off.py:4-7`). What v2 must define: which test (my reading: a pre-registered, *paired*, larger-N B*-off
comparison at 3-5 keV, plus at 1 keV on the V2b gate events to show the +2 % is not B*), its sample size and its pass
criterion. The plan (`:155`, `:390`) treats it as not run; see §7.
**(c) The population estimator for c.** The failure of V2b is an estimator choice: median(c2) − median(c_ev) is not the
median of the paired difference (`VALIDATION_GATE.md:66-77`). Candidates already computed in v1: the paired median of
(c2 − c_ev) (within ±0.001 at all 5 points, `VALIDATION_GATE.md:49-55`); the conditional median r/c_ev by k_B bin
(`README.md:203-213`); R(1/2) of the population, 1.0737 ± 0.0007 vs 1.072 (`04_truth_p1.tex:46-47`); c from medians of
Δs at B₀ and B₀/2 (the Stage-1 R_ev, `NUMERICS.md:239-241`). Needs no new events (all inputs are in Stage-3
`results/P1.json` / per-event tables; `sim/stage3/scripts/p1_results.py`, `p1_model_mg.py`); it needs a pre-registered
choice and a re-analysis of 1-5 keV cells. Cost: person time only (ESTIMATE).

---

## 0. Precondition for everything below (read first)
- **The v1 bulk data is not on this machine.** `TT/data` is 42 MB (`du -sh`, VERIFIED). There are no Stage-2 LHE/npz
  files, no Stage-3 hit npz files, and no Stage-1 M1/M3/FU/FIX raw files. `DATA_LOCATION.md:1-30` says the 46 GB
  `data/` went to an external drive, and the drive path is left as "fill in". About 200 scripts read `data/…` by
  relative path. Any re-shower, re-propagation, top-up, P1 floor test on stored events or C1 reproduction needs the
  drive or a regeneration.
- The lost frozen inputs include:
  - the Pythia MPI init file `data/acts_stage4/g1/pythia_init/`, so v1 PU events cannot be reproduced bit for bit;
  - `f1r_density_bench.json` (the Fatras per-layer densities behind top-up);
  - the Stage-2 `p0_event_budget.json`.

  Sources: sub-report, `stage4/code/s4pu.py:108-118`, `G1_REPORT.md:83-86`; VERIFIED by `ls`.
- **Every pixi manifest is osx-arm64 only:** `sim/pixi.toml:7`, `TT/pixi.toml:4`, `acts/pixi.toml:8` (VERIFIED, I read
  `acts/pixi.toml:8`). A Linux pyacts wheel exists: `acts/probe/pyacts.json` lists
  `pyacts-48.0.0-cp312-…-manylinux_2_34_x86_64.whl`, and einstein runs glibc 2.39 (sub-report, VERIFIED with `ldd`).
  `REPRODUCE.md:50, :509` wrongly says this is "not documented".

## 2. Stage 2: generation (`TT/sim/`)
- **Models.**
  - Production uses the hand-written UFO `sim/models/quirkE/`, imported as `quirkE-no_b_mass` (`sim/scripts/produce.py:26`).
  - The cross-check is the FeynRules UFO `sim/models/fr/quirkE_FR_UFO`, which is **tree level only**: there are no
    CT/R2 couplings (VERIFIED by grep in the sub-report).
  - Particles: `xe±` PDG 9000011, Dirac, (1,1)₋₁; `sxe±` PDG 9000013, complex scalar (`particles.py:390-412`,
    `parameters.py:502`).
  - The FR and hand-written UFO cross sections agree to 1.0012 (E) and 0.9989 (Ẽ) (`sim/VALIDATION.md:85-87`, UNVERIFIED).
  - N_IC = 2 multiplies σ (`VALIDATION.md:92-93`).
- **Processes.** (`produce.py:38-47`, VERIFIED)
  - LOPS: `p p > xe+ xe-`.
  - INC/TRG: MLM 0/1/2 jets with 5-flavour p and j.
  - NJ1: 0-1 jet.
  - TRG adds an ME cut pT(QQ̄) ≥ 100 GeV (`patch_ptqq_cut.py`).
  - The same set exists for `sxe`.
  - The `cards/proc_card_prod_*.dat` files are banner extracts showing only the `@0` line
    (`proc_card_prod_E-TRG.dat:21`). The full definition lives in `produce.py`.
- **Cards.** Run cards (`cards/run_card_prod_E-TRG.dat`, VERIFIED):
  - ebeam 7000 (`:38-39`);
  - lhaid 14400 = CT18NLO (`:46`);
  - dynamical scale −1 (`:56`);
  - ickkw 1 (`:67`), xqcut 30 (`:73`), and qCut 45 GeV in the Pythia card (`produce.py:175`);
  - systematics weights μR,μF ∈ {½,1,2}, CT18NLO + NNPDF23_lo (`:181`).

  Pythia cards:
  - `pythia8_quirk_common.dat:4-9` makes the quirks stable and non-resonant.
  - The CP5 card `pythia8_tune_CP5.dat:5-23` is the nominal tune, with Monash as a variation (`SAMPLES.md:14`).
  - `pythia8_quirk_common.dat:10` still says "Monash defaults", which is stale.
- **Versions.**
  - MG5_aMC 2.9.22 (`sim/README.md:4`).
  - Pythia 8.313 from MG HEPTools (`REPRODUCE.md:63`).
  - The MG5aMC_PY8_interface version is NOT documented (`REPRODUCE.md:64`).
  - LHAPDF 6.5.5 (`sim/pixi.lock:129`, VERIFIED).
  - The SM backgrounds and PU use the conda-forge **Pythia 8.312** (`acts/pixi.lock:106`, VERIFIED). This is a generator
    mismatch against the signal.
- **How samples are made** (`produce.py`, read by the sub-report). The script is a resumable stdlib driver over the
  pixi envs `mg` and `ana`. Steps:
  1. One MG output per process class.
  2. Chunks of at most 50k events, with `shower=OFF` and `set MXE m`.
  3. The LHE is copied to `data/sim/lhe/<ID>/m<m>_c<k>.lhe.gz`.
  4. The LHE is split six ways and showered by the MG5aMC_PY8_interface, with a card of tune + common (+ qedfsr).
  5. HepMC is converted to npz (`convert_hepmc.py`) and then deleted.
  6. `merge_chunks.py` writes `data/sim/npz/<ID>_m<m>.npz`.
  7. `stitch_trg.py` builds TRGS = TRG ∪ INC[pT_ME < 100].

  Supporting rules:
  - Seed rule: iseed = crc32(ID) mod 1000 × 10⁵ + 10m + chunk + 1 (`produce.py:384`). VERIFIED in the sub-report against
    five seeds in SAMPLES.md. The docstring at `:8` is wrong.
  - Linux port: `DYLD_LIBRARY_PATH` must become `LD_LIBRARY_PATH` at `produce.py:260` and `reshower.py:77`.
- **Generated grid.**
  - 47 points and 2.41 M LHE events (`VALIDATION.md:3-4`, UNVERIFIED).
  - Masses: E 200-1500 GeV in 100 GeV steps, and Ẽ at 200/500/1000 GeV.
  - Events per point (`produce.py:56-66`, VERIFIED against `SAMPLES.md:18-64`):
    - E 200/500/1000: INC and TRG 100k each, LOPS 50k;
    - fine masses: TRG 40k, INC 20k;
    - Ẽ: INC and TRG 50k.
  - Cost:
    - ≈ 27 ms CPU per LHE event (`DEFERRED.md:4-5`, ESTIMATE);
    - ≈ 18 CPU-h (`REPRODUCE.md:243`, ESTIMATE), against 23.5 CPU-h used (`VALIDATION.md:624-625`) and ~35 in
      `DATA_LOCATION.md`. These three disagree.
- **The "40-point signal grid"** is the Stage-4 A2 grid:
  - 5 species-masses (E 200/500/1000/1500, Ẽ 500) × 8 Λ values {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV;
  - **200 events per point** (`acts/stage4/run_g1b.py:49`, `run_stage4.py:98`, VERIFIED in the sub-report);
  - 40 of the 307 admissibility points (`STAGE4_RESULTS.md:656`).
  - The best v1 point rests on 9/200 (plan `:70`).
  - The full ACTS chain (A2FC) ran only at 9 points (`STAGE4_RESULTS.md:40-41`).
- **Signal cross sections and K.**
  - σ_norm = N_IC × K × σ_LO(α = 1/127.9) (`VALIDATION.md:92-93`).
  - **K is transcribed, not computed.** It comes from the LHC SUSY WG *right-selectron* (scalar) NNLOapprox+NNLL tables
    at 13.6 TeV (Resummino 3.1.1, PDF4LHC21; `research/theory_signal_model.md:158-161`) and is applied to the fermion
    as spin-independent (`:167`).
  - The 13.6 TeV K is used at 14 TeV (< 1.5 %). The 13 TeV K is used at 1200 GeV, and K is linearly extrapolated above
    that with ±2 % (`VALIDATION.md:94-97`, ESTIMATE).
  - Values: K = 1.110/1.158/1.254 at 200/500/1000 GeV, and extrapolated 1.311/1.330/1.349 at 1300-1500 GeV
    (`VALIDATION.md:111-124`). These agree with `theory_signal_model.md:178-188` (VERIFIED, two files; the values
    themselves are UNVERIFIED against the WG).
  - Nuisances:
    - ±5 % for K transfer and EW scheme;
    - PDF ±3.7/6.6/18.5 % at 200/500/1000 GeV (`SAMPLES.md:12`).
  - Omitted from σ_norm: γγ (+4 %), Sommerfeld (+5-15 %, ESTIMATE) and NLO EW.
  - Ẽ σ_norm = 19.2/0.458/0.0118 fb at 200/500/1000 GeV (`VALIDATION.md:139-140`, UNVERIFIED).
- **f₂₀₀.** This is the fraction of matched σ with pT(QQ̄) > 200 GeV after the shower (`VALIDATION.md:103-104`).
  - E 200/500/1000/1500: 0.04764/0.10418/0.14585/0.16876 (`sim/results/xsec.json`, VERIFIED by the sub-report reading
    the JSON; `LOG.md:322` quotes 0.0476/0.104, VERIFIED by me).
  - Ẽ 500: 0.1135 (`acts/stage4/investigation/INV_NORM_F200.md:59`).
  - Uncertainty: stat 0.3-2.8 %; modelling **+12…+15 % / −11…−13 %**, dominated by the ME-emission α_s
    (`VALIDATION.md:56, 105-106`, ESTIMATE).
  - History: f was first omitted from N_exp. This was a Category A bug that made the limits too strong by 1/f
    (`LOG.md:321`). It was fixed on 2026-10-16 (`LOG.md:322`), but the f uncertainty was **not propagated**
    (`LOG.md:323`, VERIFIED by me).
  - |η| < 4 issue: f_p2 uses |η_pair| < 4 to match the Stage-3 population, and that cut removes < 0.02 %
    (`INV_NORM_F200.md:49-61`). The paper text states an |η| < 4 cut that the xsec.json script does not apply
    (plan `:243`).
- **QED FSR off the quirks.** It is absent because `QEDshowerByOther` acts only on resonances and the SLHA DECAY block
  resets the flag (`cards/pythia8_quirk_qedfsr.dat:1-8`; `VALIDATION.md:63`).
  - Effect: ≈ 17 % of events radiate; the tail median ℓ_max shifts by −0.1…−1.1 ± 0.5-0.8 %.
  - A re-shower costs ≈ 15 CPU-h and reuses the LHE (`DEFERRED.md:18-23`, ESTIMATE).
  - **User decision 2026-10-11: no re-shower.** A one-sided systematic of −1.1 ± 0.8 % is carried instead
    (`LOG.md:133`, VERIFIED by me). It is implemented as the `w_qed` and `w_qed_19` tilts (`HANDOVER_STAGE4.md:63`).
  - Several files still say "pending": `sim/README.md:31-32`, `SAMPLES.md:12`, `DEFERRED.md:18-23`.
  - A v2 re-shower needs the kept LHE (absent), `sim/scripts/reshower.py` and the MG HEPTools Pythia. It must then be
    followed by a Stage-3 re-propagation, unless only a reweighting is kept.
- **Every item in `sim/DEFERRED.md`:**
  - **D-1 (`:9`)**: an NLO + FxFx point at 500 GeV.
    - It needs a loop-capable UFO: the E/Ẽ fields on `loop_sm` with UV/R2 counterterms via NLOCT.
    - Then `p p > xe+ xe- [QCD]` FxFx 0-1j, ~200k events, compared with TRGS on f(pT > 200), the pT shape and the
      median ℓ_max.
    - Cost: 1-2 person-days and 10-20 CPU-h (ESTIMATE). Due "before publication".
    - FeynRules is installed for macOS only (`sim/README.md:6`).
    - For the scalar, Resummino would give K directly.
  - **D-2 (`:10`)**: Λ-grid extension. Done in Stage 3. Its cost note ("≈ 15 s/event at 30 keV") is about 10× low; the
    record shows 154.7 s.
  - **D-3 (`:11`)**: figure restyle to the JFC/mplhep rules, 0.5-1 day, in Stage 5.
  - Non-deferred open points (`:17-29`):
    - QED FSR (since decided);
    - an interpolation closure at off-grid 450/650 GeV, ≈ 1 CPU-h each;
    - handover notes: σ_z ≈ 4-5 cm, the per-quirk fiducial denominator at |η| ≈ 4, and a pair calorimeter deposit
      ≲ 5 GeV giving ≲ 2 % MET bias (ESTIMATE).
- **SM backgrounds: the 12 processes** (`acts/stage4/analysis/inputs/normalisation.json`; σ after the MET > 200 GeV
  filter):

| process | σ [pb] | K | N_trig | sample |
|---|---|---|---|---|
| Z(νν)+j | 14.27 | 1.4 | 2.51e7 | hit level, 2000 ev |
| W(τ_ℓν)+j | 2.60 | 1.4 | 2.26e6 | hit level, 1000 |
| W(τ_hν)+j | 4.50 | 1.4 | 5.41e6 | hit level, 1000 |
| tt̄ 1ℓ | 3.50 | 1.9 | 2.38e6 | hit level, 2000 |
| W(eν)+j | 5.21 | 1.4 | 2.54e6 | proxy |
| W(μν)+j | 5.27 | 1.4 | 2.24e6 | proxy |
| tt̄ 2ℓ | 0.613 | 1.9 | 2.13e5 | proxy |
| t-channel top | 0.273 | 1.4 | 1.10e5 | proxy |
| WW | 0.165 | 1.4 | 1.26e5 | proxy |
| WZ | 0.094 | 1.4 | 1.37e5 | proxy |
| ZZ | 0.063 | 1.4 | 1.05e5 | proxy |
| tW | — | — | 2.59e5 (= 0.10 × tt̄) | proxy allowance |

  - Tags: the values are VERIFIED as file content in the sub-report; the hit-level sizes are from
    `acts/stage4/run_stage4.py:88-89`; the proxy map is `normalise.py:31-34`.
  - Total N_trig = 4.08×10⁷ ± 2.0 % (`STAGE4_RESULTS_C12v1.md:81`; matches plan `:67`, VERIFIED).
  - The 8 proxies hold 15-45 % of B_SM (`STAGE4_RESULTS.md:640-643`).
  - The σ are **computed** at LO by Pythia 8 2→2, CP5, 14 TeV: `sigmaGen` with pT-hat > 150 GeV and a truth-ν MET > 200
    filter (`s4pu.py:181-208`, `gen_d123.py:41-46`).
  - **The K-factors are neither computed nor cited.**
    - K = 1.4 is the top of an uncited "1.2-1.4" rule (`WP_RULE.md:327`), with a ±30 % nuisance.
    - K_tt = 1.9 is "conservative" (`normalise.py:27-28`).
    - tW has no Pythia process; the ratio 0.085 is rounded to 0.10 (`normalise.py:29-30`).
  - Not included: Z(ττ), lost-lepton Z(ℓℓ), fake-MET multijets (each "≲ 1-2 %", UNVERIFIED) and s-channel top.
  - Campaign C2 (`run_stage4.py:90-92`) already defines hit-level W(eν)/W(μν) at 5000 events each. It was never run.

## 3. Stage 3: string propagation (`TT/sim/stage3/`)
- **Algorithm.** `code/T3_causal_s3.py` s3.2 is a numba port of the causal null-vector Nambu-Goto string of the ATLAS
  Athena Quirks extension, with σ = Λ².
  - Fields and forces:
    - Lorentz force: a chord kick plus mass-shell renormalisation, with max-boost step splitting;
    - **uniform B₀ = 3.8112 T** in production; a field map exists but is unused.
  - Material per endpoint step:
    - Bethe mean dE/dx, Bohr straggling and Highland multiple scattering;
    - Si-equivalent slabs: TBPX 1.2 %, PS 2.5 %, 2S 1.8 %, IT service 1.0 % X₀, plus disc slabs. All of these are
      UNVERIFIED.

    Sources: `T3_causal_s3.py:46-80, 158-161`; `run_stage3.py:42`.
  - Excluded: QED radiation (only reweighted), hadronic interactions, annihilation, module planes.
  - Kernel regression: bit-identical to T3_causal on 240/240 events (`VALIDATION.md` auto table, V1).
  - Configurations: V, B, B2, M, BM, ×0.5, ×2 (`run_stage3.py:46-56`).
  - max_boost is 10⁻³ up to 5 keV and 10⁻² above (`make_jobs.py:136-139`). The plan and the docstring say ≤ 1.5 keV,
    which is a contradiction.
- **Inputs and outputs.**
  - `code/make_inputs.py` reads `<P>-TRGS_m<m>.npz` and keeps events with pT(QQ̄) > 200 GeV.
    - It unweights by hit-or-miss with seed 12345 and draws a vertex N(5 µm, 5 µm, 45 mm, 190 ps).
    - Campaigns: p2 at |η_pair| < 4, with the counting flag `in_eta25`; p1 at |η| < 1.
    - **At most 300 counting events per half.**
  - Outputs are npz files at `data/sim_stage3/out/<campaign>/<spin>_m<m>/L<Λ>_<cfg>_cNN.npz`, indexed in
    `STAGE3_INDEX.json`. That index is present (`sim/stage3/SAMPLES.md:74-79`).
  - Schema (`HANDOVER_STAGE4.md:40-90`):
    - units mm/ns/GeV, ℓ_max in cm;
    - CSR hit records over 93 surfaces; ids 83-92 are virtual T3V copies to skip;
    - weights `w`, `wvar_ratio` (106 columns) and the tilts `w_lmax_up/dn`, `w_qed`, `w_qed_19`.
- **Production totals.** 4576 jobs, 218 571 events, 583.0 CPU-h: Mac 207.5, PC 375.5 (`VALIDATION.md:59`). The plan
  estimate was ≈ 330 CPU-h (`stage3/plan.md:381`).
- **Cost per event against Λ.** Campaign p2, configuration BM, mean CPU-s per event; VERIFIED by the sub-report from
  `STAGE3_INDEX.json`:

| Λ [keV] | 0.45 | 0.6 | 0.85 | 1 | 1.5 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CPU-s/ev | 0.035 | 0.075 | 0.20 | 0.32 | 1.03 | 2.39 | 7.70 | 31.4 | 6.6 | 15.5 | 44.3 | 76.6 | 154.7 | 181.8 |

  - The cost drops at 7 keV because max_boost changes from 10⁻³ to 10⁻².
  - Scaling: ∝ Λ^2.4 and ∝ 1/max_boost (`stage3/plan.md:338-339`, ESTIMATE). The high-Λ cost comes from the
    multiple-scattering kicks.
- **Λ range needed.**
  - Detector work used only 0.45-5 keV (`run_g1b.py:49`; `STAGE4_RESULTS.md:537`).
  - Λ ≥ 15 keV cost **371.1 CPU-h, 64 % of the total** (the sub-report's sum from the index). This is consistent with
    plan `:442-443` (371 CPU-h, 64 %), so VERIFIED by two routes.
  - p2 in 0.45-5 keV cost 104.4 CPU-h for 17 species-masses.
  - S1 estimate: ≈ 43 CPU-s per event summed over the 8 Λ values, so 5 × 2000 rows need ≈ 120 CPU-h of string
    (ESTIMATE). The plan gives 12-30 (`:443`).
- **Pending decisions.** `sim/stage3/DECISIONS_PENDING.md` lists five:
  - U-1: the P1 claim above 3 keV (`:7`);
  - U-2: the B+MS combination (`:23`);
  - U-3: merged-regime toys (`:36`);
  - U-4: simplified surfaces vs module planes (`:48`);
  - U-5: digitiser merging (`:59`).

  The file says "none decided" (`:3`), but **the user decided on 2026-10-13**: U-1(a), U-2(a), U-3(a), U-4(a), U-5(b)
  `doMerge=False`, with O-1 "optional" (`LOG.md:146`, VERIFIED by me). The file is stale.
- **Handover to Stage 4** (`HANDOVER_STAGE4.md`):
  - campaign p2/BM, status 1 only; drop the 108 status-4 events (≤ 1.5 % efficiency, a one-sided bias) (`:15-36`);
  - build p4_after from `h_dE` (`:85-89`);
  - use the same simplified surfaces for quirk and PU hits (`:94-104`);
  - skip T3V (`:113`);
  - set doMerge explicitly (`:244-261`);
  - one ACTS event per physics event, untested (`:257-260`);
  - seeds are blake2b(spin, m, row, Λ, cfg), with the vertex shared across Λ (`:222-232`);
  - caveats on the B-only floor above 10-20 keV, the edges, and the f-tail normalisation nuisance (`:263-303`).

## 4. Stage 4 chain (ACTS) (`TT/acts/`)
- **Install.**
  - pyacts 48.0.0 is a PyPI wheel inside pixi, with python 3.12, pythia8 8.312, hepmc3 3.3.1 and pyhepmc 2.16.1
    (`acts/pixi.toml:15-22`; `INSTALL_CHECK.md:224-231`). There is no source build.
  - The wheel has **no ROOT, Pythia8, EDM4hep, Geant4, DD4hep, TGeo or ODD plugins** (`INSTALL_CHECK.md:13-17`).
  - The env is osx-arm64 only (§0). pyacts is not installed here, so no ACTS default could be checked at runtime.
- **Geometry and material.**
  - `geometry/build_cms_phase2_public.py` is stdlib only. It reads the tkLayout OT806_IT742 module list plus TDR-014
    numbers with page references and writes `geometry/cms_phase2_public.json` (modules, a `simplified` block of
    cylinders and discs, a beamspot block).
  - Stage 3 turned the `simplified` block into `sim/stage3/code/surfaces_s3.json` (93 surfaces).
  - `acts/stage4/code/s4geo.py` builds the ACTS Gen-3 `acts.Blueprint` from it:
    - cylinder and disc layers;
    - full cylinders and discs split into **32 φ sectors** (2561 sensitive surfaces; the sub-report counted 81
      sensitive surfaces, not the plan's 83, which include the ETL);
    - homogeneous Si-equivalent slabs (x/X₀ × 93.7 mm) via `JsonMaterialDecorator`.
  - Field: a uniform `ConstantBField(0,0,3.8112 T)` (`run_chain.py:58, 317`).
  - Layer list (from `surfaces_s3.json`, VERIFIED by the sub-report with python):
    - TBPX L1-4 at r = 30.0/61.5/104.5/146.5 mm, x/X₀ 0.012;
    - TBPS L1-3, stacked pairs at 248/251, 371/372, 522/524 mm, x/X₀ 0.025;
    - TB2S L1-3 at 686/688, 859/861, 1082/1084 mm, 0.018;
    - TFPX D1-8 at z = 250-1400 mm;
    - TEPX D1-4 at z = 1750-2650 mm;
    - TEDD D1-5 (PS and 2S rings);
    - Be beam pipe at r = 22 mm, 0.0023;
    - IT service cylinder at r = 190 mm, 0.010;
    - **BTL timing layer** at r = 1148 mm, |z| < 2600 mm, no material, σ_t = 35 ps.
  - **The ETL is absent** from ACTS because Gen-3 z-stacking failed (`s4geo.py:127-128`).
  - Tilted TBPS rings are flat. The material is entirely UNVERIFIED (×0.5/×2).
- **Fatras.**
  - Call: `addFatras(..., pMin=0.03 GeV, inputParticles='particles_input')` (`run_chain.py:326-327`, VERIFIED by me).
  - **No physics switches are passed**: the physics list is the pyacts-48 default. The plan asserts MS, ionisation,
    brems and conversions are on, and that there is **no hadronic interaction** (`stage4/plan.md:313-315`). This must be
    re-checked once pyacts is on Linux.
  - **No decays in flight**: π±, K±, μ and K⁰_L are stable. Pythia decays K⁰_S, Λ and hyperons with tau0Max = 1000 mm
    (`s4pu.py:15-16, 31-33`).
  - Particle input: charged particles and photons with pT > 50 MeV, |η| < 4 (`s4pu.py:34, 98-99`).
- **Quirk injection.** Fatras cannot carry quirks, so the Stage-3 hits are appended as `SimHit`s by a Python
  IAlgorithm `Inject` (`run_chain.py:232-263`), with vp = 4000.
  - Before injection, `hits_of` (`:503-540`):
    - drops T3V and ETL hits;
    - applies a 25 ns time window;
    - applies 99 % hit efficiency;
    - sets p4_after from a Landau dE.
- **Digitisation.** `DigitizationAlgorithm` uses a smearing config with **doMerge=False** (`run_chain.py:333-339`).
  - Gaussian σ: IT 7.2/28.9 µm; PS 28.9 µm/0.423 mm; 2S 26.0 µm/14.5 mm (a Gaussian stand-in for 50 mm strips);
    BTL 16/0.9 mm (`s4geo.py:235`). These are pitch/√12, VERIFIED in the sub-report.
  - Hit merging is done on **truth** positions in `chain_inputs.merge_pool` (|Δu| < pitch_u, |Δv| < pitch_v).
  - Inefficiency: a flat 99 % (variation 97 %) applied **to signal hits only**. PU is 100 % efficient, which is an
    asymmetry.
  - The numpy "fast path" `s4sig.digitise` runs without CKF and duplicates RES_PROD (`s4sig.py:7-12, 35`).
- **Pile-up and top-up.**
  - Pythia 8.312 CP5 `SoftQCD:inelastic` at 14 TeV, with **Poisson(200) fresh interactions per event and no pool**
    (`s4pu.py:121-147`).
  - Vertex spread: σ_z 45 mm, σ_t 190 ps.
  - No out-of-time PU.
  - Top-up (`stage4/finder/pu_inputs.py:16-17, 34-63`) adds Poisson((ratio − 1) × the event's own Fatras hits per
    layer). The ratios are:
    - TBPX L1-4: 2.77/2.26/2.81/3.72;
    - TBPS L1-3: 2.56/3.25/4.31;
    - TB2S L1-3: 4.00/5.16/7.27.

    These give the plan's "×2.3-7.3" (VERIFIED in code by the sub-report).
  - Source of the ratios: TDR-014 Fig. 6.3, read graphically (±5 %), divided by channel area × cluster size. The IT
    cluster size is ESTIMATE. The sub-report re-derived TBPX L1 at 40.8 cm⁻² against the plan's 41.
  - **Barrel only**, although `stage4/plan.md:308-309` says discs too.
  - Variations: `run_stage4.TOPUP_F`.
  - At ρ = 1 per event: Fatras barrel 48.0k hits, top-up 109.5k, CKF-removed 9.3k (`G1_REPORT.md:114-121`).
- **Seeding and CKF.**
  - Seeding: `addSeeding` GridTriplet on the TBPX and TFPX volumes only, minPt 0.9 GeV, impactMax 3 mm, r ≤ 200 mm
    (`run_chain.py:279-282, 343-352`).
  - CKF: pT > 0.9 GeV, ≥ 7 measurements, ≤ 2 holes; χ² cuts 15/25; twoWay (`:354-358`).
  - The CKF's only role is to remove helical-track hits from the finder pool: 13.9 % of measurements (`G1_REPORT.md:110`)
    against "≈ 18 %" in the plan (`:357`).
- **Plane finder F0** (`stage4/finder/finder.py`, numba; never imports ACTS).
  - Road: |Δφ(MET)| < road + asin(W_c/r), with W_c = 75 mm.
  - Seeds: TBPX (L4, L3) pairs with |Δφ| ≤ 0.3 and |Δη| ≤ 0.2, giving the plane through the PV, plus an L2 confirmation.
  - Seed score: layers with ≥ 2 crossings. A seed is kept if score ≥ T_seed.
  - Refit: 3 iterations of a PV-constrained fit with t_tol = 30 µm and collection at 3σ; N_L2 ≥ 4 is required.
  - Ranking: by (−N_L2, χ²/ndf), then de-duplication of normals within 2 mrad.
  - **Distinct-hit-set grouping**: greedy. A candidate joins a group if it shares ≥ 50 % of
    min(|H_c|, |H_leader|) (`finder/production.py:52 group_frac = 0.5`, VERIFIED by me). This is the merging rule the
    plan blames for the closure failure.
  - **Thresholds**: the code defaults are road 0.25 and T_seed 6 (`finder.py:57-62`). Production overrides them to
    **0.15 and 4** via `frozen_inputs.json` / `config_from_frozen`; T_seed went from 6 to 4 by the pre-declared G3
    action (`g3/G3_REPORT.md:150-179`). A v2 run that bypasses `config_from_frozen` silently uses 6.
  - Ladder: R01-R23 (`WP_RULE.md:279-295`):
    - layer counts;
    - widths W_c/2^k at R05-R08, down to < 4.7 mm;
    - χ²_core;
    - 2S counts;
    - helix test h (R15-17);
    - opening test (R18-20);
    - dE/dx (R21-23).
- **Trigger and MET.** There is no trigger simulation.
  - MET_true = pT(QQ̄), smeared by N(0, 25 GeV).
  - ε = 0.98 · ½[1 + erf((MET − 200)/(20√2))] (`analysis/products.py:43-45`). The parameters are ESTIMATE; the
    CMS-TDR-021 L1 thresholds were never fetched.
  - Offline: MET > 250 GeV, a jet with pT > 100 GeV, min Δφ > 0.5 (`products.py:46-52`).
  - ε_PV is 0.93 in the plan but 1 in the results.
- **Recorded costs** (Mac M3, UNVERIFIED):

| item | value | source |
|---|---|---|
| no-PU signal | ≈ 0.02-0.029 s/ev + 10 s/job | `stage4/plan.md:1548`, `G1B_REPORT.md:151` |
| PU-200 chain | 4.83 s/ev, 1 proc (CKF 2.69, Fatras + digi 0.97); 5.9 loaded; 9-10 s at 7 workers | `G1_REPORT.md:75-78`, `run_stage4.py:61-62` |
| finder ρ = 1 / ρ = 2 | 3.3-8.0 s / 20-51 s | `G2A_REPORT.md:60-62`, `run_stage4.py:63-64` |
| full-chain signal + PU (A5) | 20.9 s/ev | `G1B_REPORT.md:153` |
| A2FC, 1800 ev | 9.7 CPU-h | `A2FC_REPORT.md:46` |
| memory | chain 670 MB; finder 0.38 / 1.35 GB | `plan.md:161`, `G2A_REPORT.md:63` |

## 5. For Geant4 integration (B1)
- **Geometry.** No GDML or DD4hep exists. What does exist:
  - (i) `sim/stage3/code/surfaces_s3.json`: 93 analytic full cylinders and discs (R, z ranges, kind, sensor
    thickness, disc x/X₀);
  - (ii) the constants in `acts/stage4/code/s4geo.py`: Si and Be X₀, L₀, A, Z and density (`:37-39`), the BARREL_XX0
    table, and the beam-pipe and service positions (`:131-132, 171`);
  - (iii) `geometry/cms_phase2_public.json`, with module-level detail (17 092 modules) if a module-plane geometry is
    ever wanted.
- **Export.** A GDML writer is a new script that loops over (i) and (ii) and writes G4Tubs of thickness x/X₀ × X₀.
  This is straightforward because every element is a full tube or disc (ESTIMATE). The list of cylinders, discs and
  slabs to export is the table in §4.
  - Caveat: the material is "Si-equivalent" (X₀ 93.7 mm, λ_I 465.2 mm), but nuclear-interaction rates depend on the
    real composition (C fibre, Cu, cooling), which is not public. B1's Geant4 rates therefore inherit the UNVERIFIED
    material ×0.5/×2.
  - The pyacts wheel has no Geant4 or DD4hep plugin. Geant4 has to be standalone (conda-forge geant4 or pyg4ometry) or
    an ACTS source build, ≈ 2.3 GB of dependencies (`INSTALL_CHECK.md:41`).
- **Hand-over of secondary vertices to Fatras.** The chain already accepts displaced vertices:
  - `run_chain.ParticleSource(provider, store)` (`run_chain.py:79-112`) turns a numpy array with columns
    PCOLS = (vp, vsec, pdg, q, m, x, y, z, t, px, py, pz) into `SimParticle`s with barcodes. Each row has its own
    vertex, and vsec ≥ 1 marks a secondary vertex.
    - The v1 NI and DIF toys already inject prongs this way (`code/s4cp.py:164-195`).
    - **This is the natural hook: write the Geant4 secondary-vertex products as PCOLS rows.**
  - `run_chain.Truncate` (`:266-290`) removes the parent's Fatras hits beyond the interaction or decay radius.
  - `run_chain.Inject` (`:232-263`) inserts stored SimHits directly, if v2 prefers Geant4 to make the hits.
  - The HepMC3 reader and converter were tested but are slow, 22.8 ms per interaction (`pu_chain_interim.py:126-136`).
  - CSV/JSON/Parquet I/O exists in the wheel. EDM4hep does not.

## 6. Starting points per plan item

| item | existing code / docs (paths) | missing |
|---|---|---|
| **P1** | `analytic/NEAR_MISS_IMPULSE.md` (v5.1), `predictions.json`, `analytic/checks/c06_rotating_yoyo.py` (c_ev), `analytic/numerics/{nm_kernel,nm_bstar,FIX2_runs}.py`, `sim/stage3/scripts/{fix_bstar_off,p1_results,p1_model_mg}.py`, `sim/stage3/VALIDATION{,_GATE}.md`, paper `04_truth_p1.tex` | extended-precision or mantissa-truncated kernel for O-1 (none exists); the raw event files (on the drive); a pre-registered population estimator and a pre-registered paired B*-off criterion; corrected paper labels (W1) |
| **S1** | `sim/stage3/code/{make_inputs,make_jobs,run_stage3,T3_causal_s3}.py`, `acts/stage4/run_a2fc.py`, `run_g1b.py`, `run_chain.py sig` (A5) | the 300-event cap in `make_inputs.py`; Stage-2 TRGS npz (absent); probably new Stage-2 TRG chunks at E1500/Ẽ500, where the budget is 413-1277 per half (`stage3/plan.md:162-165`, UNVERIFIED); a 40-point ×10 manifest; the Linux port; ≈ 120 CPU-h string (ESTIMATE) + full chain at ≈ 21 s/ev |
| **S2** | `sim/scripts/{produce,reshower}.py`, `cards/pythia8_quirk_qedfsr.dat`, `sim/results/xsec.json`, `VALIDATION.md` §5.1, `DEFERRED.md` D-1, `INV_NORM_F200.md` | a loop-capable UFO (NLOCT; FeynRules macOS-only) or Resummino for the scalar; f-uncertainty propagation code; the kept LHE (absent); a Stage-3 rerun after re-shower |
| **B1** | `acts/stage4/code/s4cp.py` (NI/DIF toys), `run_chain.py` modes `cp`/`cppu`, `ParticleSource`/`Truncate`/`Inject`, `surfaces_s3.json`, `s4geo.py`, `analysis/background.py` | GDML/DD4hep writer; Geant4 env; Geant4 → PCOLS converter; P_geo × C_PU estimator; stiff-tail biased generation; a real material composition |
| **B2** | `finder/production.py` (group_frac), `finder/weights.py` (`group_sets`, `count_weights`, `subset_weights`), `finder/validate_weights.py`, `g3/G3_REPORT.md:77-90` (diagnosis), `pu_inputs.topup` | pre-merge candidate storage at ρ = 2 (the plan's "0.4 TB" in `G2A_REPORT.md:113-114` is for ρ = 1 variables without hit lists, so recompute it); semi-analytic occupancy model (no code); the R03 records |
| **B4** | `s4pu.py:181-208`, `analysis/gen_d123.py:41-46`, `normalise.py`, campaign C2 in `run_stage4.py:90-92` | tW (needs MG); Z(ττ), lost-lepton Z, multijets defined nowhere; the truth-ν MET > 200 filter (`gen_d123.py:7, 58-59`) rejects lost-lepton Z and fake-MET multijets by construction, so a reco-level MET model is needed; cited K-factors |
| **B6** | `s4geo.RES_PROD` **and** `s4sig.RES_PROD` (duplicated), `run_chain.py --mat-scale`, `s4sig.EFF`, `run_stage4.TOPUP_F` and the 'dens' job, `chain_inputs.merge_scale` | PU-hit inefficiency (signal only now); the signal material variation needs the Stage-3 `mv` campaign files; detector-level material variation A4 was deferred in v1 |
| **C2** | `finder/reference.py`, `finder/test_equivalence.py`, `probes/f1r_finder.py`, `validation/tseed4_verify.py`, `validation/g1b_regress.py`; V4-5 defined at `stage4/plan.md:1812` (0.2 mrad grid within ±0.3 rad, 5 mrad global scan, independent scipy fit, criterion \|Δn\| < 1 mrad in ≥ 95 %) | V4-5 **not run, no code** (`STAGE4_RESULTS.md:694, 858`); V4-4 only partial (T_seed = 4 bit-identity; `plan.md:1811` asks for 20 jobs); the placeholder 'val' block in `run_stage4.py:105` (15 CPU-h) |

## 7. Contradictions and open questions for the strategy
1. **The data is not here** (§0). Calendar and CPU for S1, S2, P1 and C1 depend on recovering the drive. Without it,
   C1 can only be a statistical reproduction, and the frozen PU init is lost in any case.
2. **The "B*-off test" in the plan was already run twice** (Stage-1 FIX2 at 3 keV; Stage-3 fix R1 at 5 keV,
   0.84 CPU-h). Its weakness is the paired significance (2.1σ), not the absence of a run. v2 should define the
   test as a pre-registered paired comparison with an N chosen for power, or the strategy should say what else is
   meant.
3. **The "1.5 % population gate"** compares two medians from different distributions. The Stage-1 "verified within
   1.5 %" compared against a different sample: on the same events the median is +2.4 %. The plan's "define the
   estimator in advance" is the right fix. The gate's failure is then an estimator effect (ESTIMATE), not a physics
   failure, but it must still be reported as failed (plan `:391`).
4. **Window statements:** the paper says "followed at 1-3 keV", but 9/30 cells pass. The 5 keV k_B 2-4 bin is +6.5 %.
   NEAR_MISS says "consistent at 5 keV (≲ 1 % on Δs_B(5)/Δs_B(3))" (`:25`) while Stage 3 shows a +6.2 % population
   c excess at 3-5 keV. These are different observables (a Δs ratio and the slope c), and the strategy should keep
   them apart.
5. **f_corr = 1.196** is v1's factorisation constant ("max ratio over bins", `WP_RULE.md:456`;
   `STAGE4_RESULTS.md:252`), not a "measured layer-pair correlation" as plan `:313` says. The **0.4 TB** storage figure
   is for a different object (ρ = 1 variables).
6. **The closure failure direction:** the final per-hit-set closure is anti-conservative (×1.50/1.61, fixed by ×2.41).
   The union-count closure is conservative (0.654; `g3/G3_REPORT.md:80-90`). B2's "repair" may partly be an
   accounting convention, so the strategy must fix which count is the estimator before designing the test.
7. **Fatras physics defaults** were never set explicitly in code. "No hadronic interactions" rests on the plan text,
   and pyacts could not be inspected here. Verify on Linux before B1 relies on it.
8. **Material and Geant4:** the Si-equivalent slabs are fine for MS but not for nuclear-interaction rates. B1 needs a
   public composition or an explicit ×0.5/×2 band on the Geant4 rates.
9. **B4's new processes are incompatible with the v1 MET filter** (truth-ν MET). B4 needs a reco-level MET model
   (jet mismeasurement, lost leptons), which is new physics modelling, not just "more samples".
10. **Signal statistics:** S1's ×10 rows may exceed the Stage-2 unweighted budget at E1500 and Ẽ500. New Stage-2
    chunks would then be needed. The plan's "12-30 CPU-h of string" (`:443`) and my ≈ 120 CPU-h for 2000 rows × 5
    masses × 8 Λ differ, so the row count must be fixed.
11. **Stale or inconsistent v1 records:**
    - DECISIONS_PENDING and the QED FSR "pending" texts are stale.
    - max_boost threshold: ≤ 1.5 keV in plan and docstring, ≤ 5 keV in code.
    - DEFERRED's 30 keV cost is 10× low.
    - Surface count: 83 vs 81.
    - Disc top-up is promised in the plan but absent from the code.
    - CKF removal: 18 % vs 13.9 %.
    - Code defaults T_seed 6 / road 0.25 vs frozen 4 / 0.15.
    - REPRODUCE.md says the Linux wheel is undocumented.
    - `book/review/UNRESOLVED.md:62` notes that the 23-30 µm figure is the resolution, not the MS floor.
12. **Generator mismatch:** signal uses MG + Pythia 8.313, while SM and PU use standalone Pythia 8.312 LO 2→2 with no
    ME merging. The SM K values are uncited, and B4/S2 should treat both.
13. **The P1 law above 5 keV is not needed for P2**, because MS dominates above 1.2-1.9 keV. The P1 tests are therefore
    paper-quality items, not search-critical. They are cheap if the kernel change is accepted: O-1 is ≈ 1 CPU-h plus
    1-2 person-days.
