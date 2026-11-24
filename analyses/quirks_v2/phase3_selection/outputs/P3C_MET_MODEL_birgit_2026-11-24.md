# Phase 3, work package p3-c: the reconstruction-level MET model of B4-b and its inputs to decision point 2

Executor Birgit (Fable 5.2), 2026-11-24. Session log `phase3_selection/logs/executor_birgit_2026-11-24_10-16.md`
(the plan and every pre-declaration, written 10:16 before any model number existed). Code `phase3_selection/src/p3c/`.
Machine-readable results `phase3_selection/outputs/p3c/` (`model.json`, `validation.json`, `p3c_results.json`,
`SCHEMA.md`). Simulation only; public information only. Tags: VERIFIED [V] (run or read by me, with file or
campaign), ESTIMATE [E], UNVERIFIED [U]. No signal sample was opened and no signal quantity was computed.

## 0. Summary

- **Construction.** Parameters from CMS NOTE-2018/006 (jets Fig. 25, soft term Fig. 35 u_⊥, leptons Fig. 10/13/17);
  chosen before any yield because it is the plan's first source, is full simulation at pile-up 200 and needs no
  extrapolation in pile-up (§2.1). The jet-response tail is **not sourced** after three search rounds; it was set
  before any result as 1.5 % per jet with a low-side shape of width 3σ, with the variation 0 to (3 %, 5σ) (§2.2).
- **External validation of B4-b: NOT VALIDATED, under both allowed readings** (§3). Against the other figures of the
  same note the resolution agrees (u_∥ 31.1 against 31.8 ± 1.0 GeV) but the tail fractions of the MET distribution do
  not (model/figure 1.49, 1.13, 0.78 above 60, 78, 90 GeV; tolerance 20 %). Against the other experiment's tt̄ figure
  the model is 34.6 against 36.5 ± 0.5 GeV at ΣE_T = 0.5 TeV and 42.5 against 37.5 ± 0.5 GeV at 1 TeV. Four
  remediation variants were tried without touching any yield; none passes. The fail branch of STR l.1387-1388
  applies: the three additions carry the full variation as width.
- **Internal check (b): PASS.** Multijet yield from a weighted sample and from unweighted p̂_T slices: ln ratio
  −0.004 ± 0.028, 4,054 and 1,927 effective passing events (§4.1).
- **N_trig of the additions (3 ab⁻¹, nominal model)** [E]: Z(ττ) **1.27×10⁵** (full variation 1.10–1.58×10⁵);
  lost-lepton Z(ℓℓ) **1.09×10⁵** (0.62–1.24×10⁵; 0.62×10⁵ if unidentified electrons stay in the calorimeter sum);
  multijets **4.28×10⁷** (3.0×10⁵–7.3×10⁸).
- **The multijet number is set by the unsourced tail, not by any source** (§4.2). Gaussian response only: 7.1×10⁵
  (1.7 % of the triggered sample). Declared nominal tail: 4.28×10⁷ (51 %), 92 % of it from jets whose response falls
  below 0.1. Declared upper tail: 4.8×10⁸. A published monojet analysis at 13 TeV and pile-up 23 has at most 1.0–1.4 %.
  Phase 1 planned 4×10⁵ (range 4×10⁴–4×10⁶). Nothing was tuned; **a decision is needed** (§8, item 1).
- **Events per Z(νν) pilot count** (replaces the provisional 41; M = 1,023,164 with the v2 weights against 993,885.9):
  **81.9** with the declared nominal tail; **40.5** with a Gaussian-only response; 519 with the upper tail
  (STR-literal reading; the two other readings give 85.2 and 87.3 at nominal). Z(νν) alone: 24.5.
- **Step (3).** The offline threshold stays at MET_reco > 250 GeV: the user's decision of 19 Nov (COM l.366) is
  binding and nothing found here conflicts with it (§5).
- **Pool shares (rule 6).** Z(ττ) 10.3 → 5.6 CPU-h, lost-lepton Z(ℓℓ) 2.7 → 5.2 CPU-h; summed SM zero-count allowance
  169.4 → 167.8 events inside the same 457 CPU-h (§6.3).
- **Step (4)** is written (`src/p3c/step4_acceptance.py`), refuses to run on signal without an approval record, and
  was tested on background files only (§7).
- CPU: 11.3 CPU-h in the ledger plus about 0.4 CPU-h of short analysis steps over ssh, of the 50 budgeted.

## 1. What was run

Node schrodinger, generator-level Pythia 8.312 (CP5, 14 TeV, MPI and hadronisation on, the chain's decay settings),
no truth-MET filter, no detector chain. CPU from the done markers (`ledger/markers/p3-c-*`) [V].

| campaign | content | events | jobs done | CPU-h |
|---|---|---|---|---|
| p3-c-val | inclusive Z→μμ (m > 60 GeV) 640,000; inclusive tt̄ 320,000 | 960,000 | 12/12 | 3.04 |
| p3-c-pw | v2 weights of the Z(νν) pilot (reads `evt`, `jets`, `lep`, `gsum` of the 460 pilot files) | 2,300,000 rows | 23/23 | 0.06 |
| p3-c-pw2 | the same with the azimuth of MET_reco added (the road axis under v2, needed by the pilot classification); weights identical to p3-c-pw, checked | 2,300,000 rows | 23/23 | 0.06 |
| p3-c-zx | Z(νν), Z(ττ), Z(ℓℓ) + parton, p̂_T > 80 GeV, biased p̂_T⁴, 400,000 each | 1,200,000 | 15/15 | 4.56 |
| p3-c-ap-zx | model and variations on p3-c-zx, 50 throws per event | — | 3/3 | 0.43 |
| p3-c-mjw | multijets (HardQCD), p̂_T > 100 GeV, biased p̂_T⁵ | 240,000 | 4/20 (stopped by me, see below) | 1.10 |
| p3-c-mjs2 | multijets, unweighted slices 100–200–400–800–1600–∞ GeV, 60,000 each | 300,000 | 5/5 | 1.41 |
| p3-c-ap-mjw4, p3-c-ap-mjs2 | model on the multijets, 100 throws per event, tail state importance-sampled | — | 2/2, 5/5 | 0.60 |
| **total** | | | | **11.3** |

Departures from the plan of 10:16, with reasons (log 15:12): the weighted multijet campaign was stopped after 4 of
20 jobs and the sliced one reduced from 20 to 5 jobs, because the first file already gave 414 effective passing
events and showed the finding of §4.2, which the brief asks to report promptly. I stopped the p3-c-mjw driver by
hand; its fifth job was killed after 17 CPU-s (marker `killed`); 15 jobs were never run. For about 30 s at 15:56
four of my processes ran, and I held one yield job (SIGSTOP) for 8 minutes to stay at two. The validation script
(4 minutes) and a few short aggregation steps ran over ssh at nice 15 outside the runner (≈ 0.4 CPU-h [E]).
The 20-job campaign file `p3-c-mjs` and `p3-c-ap-mjw`, `p3-c-ap-mjs` were written and never launched.

## 2. The model (deliverable 1)

### 2.1 Construction choice and why (decided 10:16, before any yield)

The parameters come from **CMS NOTE-2018/006** (public; supplied by the user; retrieval_log #20), which is the
parameter set common to options A and B of EXP §4.6. The reasons are in the sources and in the plan's text:

1. STR l.1337-1339 orders the sources: the Phase-2 documents of R-3 first, the performance reports of the other
   general-purpose experiment second. The note is full simulation of the Phase-2 detector at ⟨PU⟩ = 200 with PUPPI,
   which is also the pile-up mitigation of the trigger curve of S2-e (L1 PUPPI MET).
2. Option C would take the jets from ATL-PHYS-PUB-2013-004 (fitted at μ = 0–40, extrapolated to 140 by the source
   and to 200 by us) and the soft term from ATLAS Fig. 18, a tt̄ RMS that already contains the jets. Option D is
   known to be ×2–4 above both PU-200 figures (EXP §9 item 14).
3. Options A and B differ only in the validation figure. STR l.1343-1345 asks for "a different figure from the ones
   the parameters are taken from"; both allowed readings were computed and each has its own verdict (§3).

### 2.2 Definition

MET_reco = | −( Σ_jets R_j p⃗_T,j + Σ_reconstructed prompt e, μ p⃗_T + U⃗_true + S⃗ ) |, all at generator level
(`src/p3c/metmodel.py`; this is the formula of STR l.1327 with its soft term split into the true unclustered sum
U⃗_true and the pile-up noise S⃗).

| piece | definition | source (CMS NOTE-2018/006, printed page) | tag |
|---|---|---|---|
| jets | anti-k_T 0.4 on the visible final state, p_T,gen ≥ 30 GeV, \|η\| < 4.7, up to 12 per event; prompt e, μ above 10 GeV are subtracted from a jet within ΔR < 0.4 | lower edge of Fig. 25 | — |
| core of R_j | Gaussian, mean 1, width σ(p_T,gen, η): readings of Fig. 25 in three η bins (SEB §1.5), linear in ln p_T between the read points, constant below 30 GeV and above the last point (0.067 above 480 GeV in the barrel); the 1.7–2.8 bin is used up to 4.7 | Fig. 25 p. 16 | [E] reading ±0.01; 2.8–4.7 extrapolated |
| **tail of R_j** | with probability f_tail the response is 1 − \|N(0, k·σ)\| (low side only); nominal f_tail = 1.5 %, k = 3 | **NOT SOURCED** (retrieval_log #14, #20, #32–#36). Size anchored on a Run-1 statement, order of magnitude only: CMS, JINST 12 (2017) P02014 §8.3 (98.5 % of the dijet-asymmetry events in the Gaussian core, 97 % as variation). k has no anchor | not sourced |
| leptons | prompt e, μ above 10 GeV are reconstructed with probability ε: e 0.975 for \|η\| < 1.4; 0.65 at 10 GeV rising linearly to 0.97 at 40 GeV for 1.4–3.0; μ 0.97 for \|η\| < 2.0, 0.995 for 2.0–2.8; 0 outside. A reconstructed lepton enters the sum exactly and vetoes the event if \|η\| < 2.5 and isolated (v1's definition). **A lepton that is not reconstructed is left out of the sum** (STR l.1329-1333, literal) | e: Fig. 13 p. 9, Fig. 10 p. 8 (stated for 1.6–2.8), text p. 7; μ: Fig. 17 p. 11 (1.6–2.8 only; the barrel is not shown, 0.97 used) | [E] ±0.01; barrel muon and 1.4–1.6 / 2.8–3.0 electron values are extrapolations |
| U⃗_true | true vector sum of everything visible in \|η\| < 5 that is not a model jet or a prompt lepton above 10 GeV; not smeared | — | — |
| S⃗ (soft term) | Gaussian, σ_soft = 29.03 GeV per component, the same for every event. From σ_soft² = (29.8 GeV)² − V_⊥, where 29.8 GeV is the u_⊥ width of Fig. 35 (right) at the mean PU density 1.4 /mm and V_⊥ = 45.4 GeV² is the variance the model's jets add perpendicular to the Z in generated Z→μμ events with p_T(Z) > 30 GeV | Fig. 35 p. 21; mean density §2.4 p. 9 | [E] ±1 GeV; V_⊥ [V: `model.json`, 71,147 events] |
| trigger | ε_trig(MET_reco) from the digitised L1 curve, linear interpolation | CERN-LHCC-2020-004 Fig. 3.125 p. 188 (`phase2_exploration/outputs/s2/trigger_turnon.json`) | [E] ±0.01 |
| preselection | MET_reco > 250 GeV; ≥ 1 reconstructed jet above 100 GeV in \|η\| < 2.4; min Δφ(four leading reconstructed jets above 30 GeV, MET_reco) > 0.5; lepton veto as above; photon veto as v1 (prompt isolated photon above 15 GeV, \|η\| < 2.5, weight 0.05: v1's value, not sourced); no τ_h veto (as v1). Event weight = ε_trig × pass × vetoes | v1 `gen_d123.presel`; the same selection as the published monojet analyses (retrieval_log #37, #38) | — |

Not modelled, stated: pile-up jets (Fig. 27: 12–14 % extra jets above 30 GeV); any dependence of S⃗ on the PU
density or on ΣE_T; a jet response different from 1; calorimeter cracks and dead cells (they would be part of the
unsourced tail).

**Formula checks** (`src/p3c/test_metmodel.py`, all pass [V]):
- *Limiting case of STR l.1334.* R_j ≡ 1, no lost lepton, S⃗ = 0 gives the visible sum in \|η\| < 5 to 4×10⁻¹⁵ GeV.
  This is an identity by the construction of U⃗_true and is stated as such; the physical content is the next line.
- *Against the neutrino MET.* \|visible(\|η\| < 5) + neutrinos\| has a median of 5.0 GeV and a 95 % quantile of 14.5 GeV
  (particles beyond \|η\| = 5; 300 Z(νν) events), so in this limit MET_reco is the v1 neutrino MET within that.
  All visible particles plus neutrinos sum to zero transverse momentum (0.000 GeV).
- *Substitution.* One 100 GeV jet at η = 0: width of the smeared p_T 0.1301 (table 0.13). Fraction below 1 − 3σ with
  the nominal tail 0.0063, expected 0.985 × 0.00135 + 0.015 × 0.3173 = 0.0061.
- *Variation → 0.* Identical random numbers give identical weights; ε_trig(250 GeV) = 0.975 (EDG §2.6), the shifted
  erf gives 0.879 at 250 GeV (EDG §2.6 table: 0.879).

### 2.3 Systematic variations (declared 10:16; "within the range of the public source", STR l.1361)

| name | change | source of the size |
|---|---|---|
| core up / down | σ → 1.05 σ + 0.01 / 0.95 σ − 0.01 | Table 1 p. 29 (JER 3–5 %) and the reading error of Fig. 25 |
| JES up / down | jet scale ×1.025 / ×0.975 | Table 1 p. 29 (JES 1–2.5 %) |
| soft up / down | u_⊥ target 32.5 / 25 GeV (σ_soft 31.79 / 24.08 GeV) | highest-density point of Fig. 35 / the note's text p. 19 ("about 25 GeV") |
| tail up / down | f_tail 3 %, k = 5 / f_tail = 0 | **not sourced** (wide, declared) |
| soft mix | two-Gaussian soft term fitted to the Fig. 34 shape: 22 % at 38 GeV, 78 % at 21 GeV | Fig. 34 p. 21 used as a source |
| lost e kept | an electron that is not identified stays in the sum (muons stay lost) | the other reading of STR l.1329 |
| all up / all down | core, soft and tail moved together | corners |

The **full variation** of the fail branch (STR l.1387-1388) is the envelope over all rows.

## 3. External validation of B4-b (deliverable 2): NOT VALIDATED

Rules, readings and tolerances were fixed at 10:16 (log §P0, §P4). Tolerance as frozen: the larger of the source's
stated uncertainty (neither source states one) and the reading error; the Monte Carlo error of the model point is
added in quadrature. Results: `outputs/p3c/validation.json` [V: `p3c_validate.py` on campaign p3-c-val].

### 3.1 Reading R-B: the other figures of the same note (Fig. 35 left, Fig. 34)

Sample: 640,000 generated Z→μμ events; 366,059 with two prompt muons above 10 GeV in \|η\| < 2.8; 71,147 with
p_T(Z) > 30 GeV.

| quantity | model (nominal) | figure | tolerance | result |
|---|---|---|---|---|
| σ(u_∥), p_T(Z) > 30 GeV (r.m.s. of u_∥ + p_T(Z)) | 31.10 ± 0.09 GeV | 31.8 GeV (Fig. 35 left at 1.4 /mm) | 1.0 GeV | inside |
| σ(u_⊥) (the source point; reproduced by construction) | 29.89 ± 0.08 GeV | 29.8 GeV | — | not a test |
| fraction of the MET distribution above 60 GeV | 0.128 | 0.0859 | 20 % | **outside** (×1.49) |
| above 78 GeV | 0.0312 | 0.0276 | 20 % | inside (×1.13) |
| above 90 GeV | 0.0098 | 0.0126 | 20 % | **outside** (×0.78) |

**R-B: FAIL** (the declared rule needs the resolution and all three thresholds). I knew before declaring the rule
that a single threshold of 78 GeV would pass and 60 or 90 GeV would fail (hand arithmetic on my reading of Fig. 34,
log §P0); that is why three thresholds were declared. The 20-bin shape is in Figure 1: the model's distribution
peaks about 6 GeV higher and falls faster in the far tail than the published one (largest \|ln(model/figure)\| 1.17,
in the last bin).

![MET distribution in Z→μμ events. Points: my by-eye reading of the public Phase-2 full-simulation figure at pile-up 200, with the 20 % reading error. Lines: the model with the nominal single-Gaussian soft term, with the two-Gaussian soft term fitted to this figure, and with the lower soft-term target of 25 GeV. The lower panel is the ratio to the figure. The nominal model is too wide in the core and too narrow in the far tail.](figures/p3c_met_shape_zmm.pdf)

### 3.2 Reading R-A: the other experiment's figure (ATL-PHYS-PUB-2019-005 Fig. 18)

Sample: 320,000 inclusive tt̄ events; RMS of E_x,y(reco) − E_x,y(true) in windows of ±20 % around the read points.

| ΣE_T | events | model (nominal) | figure (full η) | tolerance | result |
|---|---|---|---|---|---|
| 0.5 TeV | 149,794 | 34.64 ± 0.07 GeV | 36.5 GeV | 0.5 GeV | **outside** (−1.9 GeV) |
| 1 TeV | 31,025 | 42.48 ± 0.21 GeV | 37.5 GeV | 0.5 GeV | **outside** (+5.0 GeV) |
| 2 TeV | 620 (below the declared 1,000) | 64 ± 3 GeV | 42.0 GeV | — | not counted |
| 3, 4 TeV | 37, 1 | — | 46.5, 50.5 GeV | — | not populated |

**R-A: FAIL.** The model's ΣE_T is the visible hard scatter alone (5–95 % range 323–928 GeV); the figure's is the
reconstructed total at μ = 200 in another detector. That mismatch was named at 10:16 as outside any tolerance; it
explains the different slope (Figure 2) but does not change the verdict under the frozen criterion.

![Width of the MET residual in tt̄ events against the scalar sum of transverse energy. Squares: the public figure of the other general-purpose experiment at pile-up 200, read by eye (±0.5 GeV). Lines: the model with the nominal soft term, the upper soft-term target and the two-Gaussian soft term. The model's horizontal axis is the hard scatter alone, the figure's is the reconstructed total including pile-up, so the two slopes are not comparable; the model fails the declared comparison at both populated points.](figures/p3c_met_rms_ttbar.pdf)

### 3.3 Remediation attempts (no yield involved; the nominal was not changed)

| attempt | u_⊥ / u_∥ [GeV] | tails ×(60 / 78 / 90 GeV) | tt̄ RMS at 0.5 / 1 TeV | R-B / R-A |
|---|---|---|---|---|
| nominal (σ_soft 29.03 GeV) | 29.9 / 31.1 | 1.49 / 1.13 / 0.78 | 34.6 / 42.5 | FAIL / FAIL |
| 1. soft term scaled with the PU density along Fig. 35's own line (density drawn for a Gaussian luminous region of mean 1.4 /mm) | 29.8 / 31.2 | 1.51 / 1.19 / 0.85 | — | FAIL / — |
| 2. two-Gaussian soft term fitted to Fig. 34 (22 % at 38 GeV, 78 % at 21 GeV) | 26.6 / 28.1 | 0.96 / 1.02 / 1.02 (fitted) | 31.9 / 40.3 | FAIL (u_∥) / FAIL |
| 3. best single Gaussian for Fig. 34 (30 GeV) | 30.8 / 32.1 | 1.69 / 1.39 / 1.03 | — | FAIL / — |
| 4. source range: target 25 / 32.5 GeV | 25.0 / 26.6; 32.5 / 33.8 | 0.62 / 0.27 / 0.12; 2.07 / 1.95 / 1.58 | — ; 36.9 / 44.3 | FAIL / FAIL |

Cause found: Fig. 35 is response-corrected (the width is divided by the recoil response) and is for p_T(Z) > 30 GeV;
Fig. 34 is the raw MET of all events. Their r.m.s. per component differ (29.8 GeV against 26.1 GeV from my reading of
Fig. 34), and a soft term with unit recoil response cannot meet both. A recoil response below one is not a quantity
of the frozen model (STR l.1327) and has no number in the note, so it was not added.

### 3.4 Consequence

Both allowed readings fail, so the question which reading binds does not arise. **B4-b external validation: FAIL →
"MET model not validated: the three additions carry the full variation; stated limitation"** (STR l.1387-1388 and the
table at l.1880; COM B4-b). This is the strategy's own branch, not the stop of l.1881: parameters exist from public
sources (ruling of LOG 2026-11-16 12:15).

## 4. Internal check, the tail, and the items reported without verdict

### 4.1 Internal check (b): stable under the generation bias — PASS

Multijet yield after MET_reco > 250 GeV, a jet above 100 GeV and min Δφ > 0.5 (with vetoes and trigger weight):

| sample | generated | N_trig (3 ab⁻¹, K = 1) | effective passing events | σ_ln |
|---|---|---|---|---|
| weighted (p̂_T⁵ bias, p̂_T > 100 GeV) | 240,000 | 4.270×10⁷ | 4,054 | 0.016 |
| five unweighted slices | 300,000 | 4.288×10⁷ | 1,927 | 0.023 |

ln(weighted/sliced) = −0.004 ± 0.028: inside the factor 2, both samples above 100 effective events and σ_ln ≤ 0.1.
**PASS** [V: `p3c_results.json` → `checks.b_multijet_bias`]. Effective events are (Σ w p)²/Σ (w p)² over generated
events, p being the mean weight over 100 response throws; the tail state was drawn with probability 0.25 per jet and
weighted back (exact; the Z(ℓℓ) test file gave consistent results with and without it). Per variation the two samples
agree within 0.06 in ln, except the two Gaussian-only variations (0.24 and −0.30, with 56 and 72 effective events in
the weighted sample: statistics). Figure 3 shows the two samples per p̂_T bin. The p̂_T < 100 GeV region is not
generated; the lowest bin (100–150 GeV) holds 4–6 % of the yield, so the truncation is of that order (not corrected).

![Multijet cross section after the preselection per bin of the hard-process transverse momentum, for the weighted sample and for the five unweighted slices. The two generation biases agree bin by bin within their statistics; the yield peaks at 200–300 GeV, where a single jet of 250–300 GeV that is almost completely lost gives a missing momentum above the threshold.](figures/p3c_multijet_pthat.pdf)

### 4.2 The unsourced tail sets the multijet yield (finding; nothing tuned)

| response model (all declared at 10:16) | multijet N_trig | share of the triggered sample | effective events (weighted sample) |
|---|---|---|---|
| Gaussian only (`tail_dn`) | 7.1×10⁵ | 1.7 % | 56 |
| nominal tail, 1.5 %, width 3σ | **4.28×10⁷** ± 1.3 % (MC) | 51 % | 4,054 |
| upper tail, 3 %, width 5σ (`tail_up`) | 4.83×10⁸ | 92 % | 12,524 |
| everything down / up | 3.0×10⁵ / 7.3×10⁸ | | 72 / 15,701 |

- Mechanism [V: `nominal_notrig_S1_by_min_response` of the yield records]: 92 % of the nominal yield comes from
  throws in which one jet has a response below 0.1, and 97 % below 0.2. Such a jet drops below 30 GeV and out of the
  min Δφ list, so the cut that removes ordinary mismeasurement does not see it. Cut flow of the weighted sample in
  events per 3 ab⁻¹ without trigger weight: generated 3.9×10¹², MET_reco > 250 GeV 1.68×10⁸, + jet 1.61×10⁸, + min Δφ
  4.44×10⁷, + vetoes 4.42×10⁷. The probability of a response below 0.1 for a 250 GeV jet in the declared shape is
  0.015 × P(\|N(0,1)\| > 0.9/(3 × 0.09)) ≈ 1.3×10⁻⁵ per jet: a number that follows from the two unsourced parameters
  and from nothing else.
- The core alone also matters: core up / down moves the multijets by ×1.72 / ×0.52 (sourced range).
- **Phase 1 assumed** N_MJ ≈ 4×10⁵, 1 % of N_trig, range 0.1–10 % (STR Table 4.4a). **Phase 3 found** 1.7 % to
  1,180 % of the v1 N_trig depending only on the unsourced tail; the declared nominal is ×107 above the planning
  value. **Implications:** the multijet N_trig is not determined by B4-b as frozen; through N_SM it moves the events
  per pilot count between 40 and 760 (§6.2), the multijet zero-count allowance of B4-e between 0.35 and 830 events
  (1.14 × N_MJ/10⁶; 48.7 at the nominal), and the multijets become the largest SM term of rule 1 if the nominal tail
  is kept.
- Two statements about the tail existed before any result and disagree: retrieval_log #14 (16 Nov) recorded as the
  consequence of "not sourced" that "the model is then Gaussian-core only, the missing tail is stated as a
  limitation, and the size of a tail variation has to be set as an unsourced width"; my declaration of 10:16 today set
  a non-zero nominal with zero as the lower variation. Both sets of numbers are in the JSON (`ratio_to_nominal.
  tail_dn` gives the Gaussian-only reading). I do not choose between them after seeing the result.

### 4.3 Reported, no verdict (STR l.1356-1360)

- **(a) Continuity with v1, Z(νν)+jets.** On the unfiltered sample (400,000 events, p̂_T > 80 GeV): σ after the
  v2 selection 7.10 pb against 6.25 pb for v1's selection emulated on the same events (truth MET + 25 GeV smearing,
  truth MET > 200 GeV filter, v1 trigger function): **ratio 1.136 ± 0.004**. 7.4 % of the v2 yield comes from truth
  MET below 200 GeV, which the v1 filter and the pilot do not contain; 2.0 % from p̂_T below 150 GeV. On the pilot
  itself Σw_v2/Σw_v1 = 1.0505, and 1.0505/(1 − 0.0738) = 1.134 agrees with the direct ratio. 28 % of the pilot's v2
  weight sits on events with zero v1 weight and 25 % of its v1 weight on events with zero v2 weight (different random
  smearing and a wider resolution). Absolute scale: v1-like N on my sample 2.63×10⁷ against v1's frozen 2.51×10⁷
  (+4.7 %; different jet thresholds in the emulation and 12 throws per event; not investigated further).
- **(c) Multijet share against a published monojet analysis.** CMS, arXiv:1712.02345 Table 8 (13 TeV, 35.9 fb⁻¹,
  mean pile-up 23; the same selection as here): "other" backgrounds (QCD multijet and γ+jets together) are 1.4 % of
  the total at 250–280 GeV and 1.0 % at 370–400 GeV, so the multijet share is at most that [U: transcribed through the
  fetch tool, retrieval_log #38]. Model: 51 % (nominal tail), 1.7 % (Gaussian only), 92 % (upper tail). Order of
  magnitude only, as the plan says: the reference is at pile-up 23 and cannot test the soft term; it does say that a
  per-jet probability of 10⁻⁵ for losing a jet completely is not what that detector showed after its event cleaning.

## 5. Step (3): the offline MET threshold (deliverable 3)

**Decision recorded: the offline threshold stays at MET_reco > 250 GeV.** The user decided this on 2026-11-19 (COM
l.366, option (b): threshold kept, wide nuisance of −10.6 % absolute efficiency at 250 GeV, −4.9 % at 275, −1.9 % at
300, from the erf through L1 TDR Table 4.1 with its 50 % point shifted by one width). I confirm it against what the
MET model adds, on background samples only, and find no conflict:
- The public curve (CERN-LHCC-2020-004 Fig. 3.125 p. 188) is at 0.975 ± 0.01 at 250 GeV and its 90 % point is at
  199 GeV (EDG §2.6); STR §4.14 (d) raises the threshold only "if the public curve reaches its plateau above 250 GeV",
  which the user's decision settled.
- The curve's axis is generator-level visible MET; the model evaluates it at MET_reco (declared at 10:16; v1 did the
  same with its smeared MET). With the trigger weight removed N_trig changes by +1.5 % (Z(νν)), +2.5 % (Z(ττ)), +0.2 %
  (Z(ℓℓ)), +2.3 % (multijets): the selection sits on the plateau.
- With the user's nuisance curve instead of the nominal one: N_trig × 0.977 (Z(νν)), 0.965 (Z(ττ)), 0.943 (Z(ℓℓ)),
  0.98 (multijets); pilot M 1,002,357 instead of 1,023,164 (−2.0 %). These are the sizes the option-(b) nuisance has
  on the backgrounds; the signal's size is a step-(4) number.
- For information (no proposal): N_trig at other thresholds is in `n_trig.<p>.N_trig_by_met_cut`; from 250 to 300 GeV
  Z(νν) falls ×0.46, Z(ττ) ×0.35, Z(ℓℓ) ×0.31, multijets ×0.34.

## 6. Numbers for decision point 2 (deliverable 4)

`outputs/p3c/p3c_results.json` (schema: `outputs/p3c/SCHEMA.md`). L = 3 ab⁻¹. All [E]: generator-level Pythia 8 at
leading order; K = 1.4 for the Z processes is v1's K_V [U: `normalise.py`; R-5 is open, B4-d]; multijets K = 1.

### 6.1 N_trig of the three additions

| process | N_trig (nominal) | MC error | core dn / up | JES dn / up | soft dn / up | tail dn / up (not sourced) | soft mix | lost e kept | **full variation** (the not-validated width) | planning (STR Table 4.4a) |
|---|---|---|---|---|---|---|---|---|---|---|
| Z(ττ) | **1.272×10⁵** | 1.4 % | 0.948 / 1.065 | 0.880 / 1.137 | 0.911 / 1.065 | 0.990 / 1.072 | 0.949 | 0.885 | **1.10–1.58×10⁵** (half-width in ln 0.18) | 4.3×10⁵ (1×10⁵–1.3×10⁶) |
| lost-lepton Z(ℓℓ) | **1.089×10⁵** | 2.1 % | 0.939 / 1.039 | 0.855 / 1.138 | 0.893 / 1.066 | 1.000 / 0.991 | 0.933 | 0.571 | **0.62–1.24×10⁵** (0.34) | 3.0×10⁴ (1×10⁴–1×10⁵) |
| multijets | **4.28×10⁷** | 1.3 % | 0.520 / 1.716 | 0.897 / 1.134 | 0.894 / 1.109 | 0.0167 / 11.3 | 0.962 | 0.998 | **3.0×10⁵–7.3×10⁸** (3.9) | 4×10⁵ (4×10⁴–4×10⁶) |
| Z(νν), for reference | 2.982×10⁷ | 0.3 % | 0.984 / 1.019 | 0.911 / 1.096 | 0.952 / 1.033 | 1.009 / 0.987 | 0.971 | 1.000 | 2.72–3.27×10⁷ (0.09) | v1: 2.51×10⁷ |

Entries are ratios to the nominal. The multijet value is the inverse-variance mean of the two samples of §4.1.
Figure 4 shows the ratios.
- Z(ττ): generator cross section 39.6 pb (p̂_T > 80 GeV); 0.031 pb after the selection without trigger weight; 28 % of
  the yield has no hadronic τ, 55 % one, 17 % two; 33 % comes from true neutrino MET below 200 GeV. No τ_h veto is
  applied (as v1): with one, the number would be lower.
- Lost-lepton Z(ℓℓ) (e and μ): 79.4 pb generated; after MET_reco > 250 GeV 0.063 pb, after jet and min Δφ 0.053 pb,
  after the lepton veto 0.026 pb. All of it has true neutrino MET below 200 GeV, so v1's filter contained none of it.
  Under the literal reading of the plan a lepton that fails identification is removed from the sum and becomes MET;
  if unidentified electrons are kept as calorimeter energy the yield is ×0.571. It is above the planning range
  (1×10⁴–1×10⁵) under the literal reading and inside it under the other.
- Correlation across processes and with the signal acceptance (STR l.1361-1362): each named variation is one
  nuisance; the same variation names are computed by the step-(4) script for the signal.

![Ratio of the triggered yield under each declared variation to the nominal, for the three additions and for Z(νν). Core, energy-scale and soft-term variations move every process by at most a few tens of per cent; the unsourced tail moves the multijets by a factor 60 down and 11 up, and the choice of what happens to an unidentified electron moves the lost-lepton Z(ℓℓ) yield by a factor 0.57.](figures/p3c_ntrig_variations.pdf)

### 6.2 Events per Z(νν) pilot count (replaces the provisional 41; TOV l.86)

Pilot with the v2 weights (campaign p3-c-pw; one throw per event seeded from the pilot file's job seed, the same
random numbers for every variation; per-event weights **and the azimuth of MET_reco (the road axis under v2)** in
`data/p3c/p3-c-pw2/000/`, format in SCHEMA.md) [V]. Note for the pilot classification (p3-a): the v2 model changes the
weight of a pilot event and its road axis; both are in these files, for the same throw:

| quantity | value |
|---|---|
| M with v1's weights, recomputed from the stored `w_v1` | 993,885.93 (frozen 993,885.9: reproduced) |
| **M with the v2 weights**, full class (no vetoable photon), w_max = 1 | **1,023,164** (1,037,905 events with non-zero weight; mean of 20 throws: 1,023,550) |
| M under the variations | 946,304 (JES down) to 1,100,152 (JES up); soft 1,003,132–1,034,310; tail 1,008,989–1,032,719; trigger nuisance curve 1,002,357 |
| low-weight class (photon veto weight 0.05), Σw/0.05 | 7,969 |

| reading (fixed at 10:16, log §P6) | N_SM | events per count | Z(νν) alone |
|---|---|---|---|
| **primary, STR-literal**: v1's N_trig of the twelve processes kept (STR l.936), plus the three additions | 8.385×10⁷ | **81.9** | 24.5 |
| secondary: Z(νν) rescaled by v2/v1 = 1.134 (pilot ratio and the 7.4 % migration from below 200 GeV) | 8.721×10⁷ | 85.2 | 27.8 |
| tertiary: all twelve rescaled by the Z(νν) ratio (proxy) | 8.932×10⁷ | 87.3 | — |
| primary, Gaussian-only response (`tail_dn`) | 4.180×10⁷ | **40.5** | — |
| primary, upper tail (`tail_up`) | 5.24×10⁸ | 519 | — |
| primary, range over all variations (the not-validated width) | | 40.5–756 | — |

The provisional value was 41.96 (4.170×10⁷/993,885.9). Without the multijets the primary reading would be 40.2: the
change from 41 comes from the multijets alone. Caveat for the reading of rule 1 (ADD §4.3: every SM process and the
multijets at the H per event of the Z(νν) pilot): with the nominal tail half of N_SM is multijet events, whose track
content the Z(νν) pilot stands in for; whether that proxy is acceptable at that share is not a question this work
package can answer.

### 6.3 Pool shares (rule 6 of §11.7; rule of §4.4, M_t ∝ √(N_t/c_t))

SM part of the pool, 456.6 CPU-h as allocated by the frozen script; unit costs and full-weight fractions of ADD §4.4
"as timed" (Z-type 0.127 s per generated event and 0.4396). My script reproduces the addendum's summed allowance
169.4 with the planning N_trig [V].

| process | N_t planning → MET model | M_t (full-weight events) | CPU-h | zero-count allowance (68 %) |
|---|---|---|---|---|
| Z(ττ) | 4.26×10⁵ → 1.27×10⁵ | 127,738 → 70,120 | 10.3 → 5.6 | 3.80 → 2.07 |
| lost-lepton Z(ℓℓ) | 2.98×10⁴ → 1.09×10⁵ | 33,796 → 64,880 | 2.7 → 5.2 | 1.01 → 1.91 |
| Z(νν) | 2.51×10⁷ (kept) | 979,703 → 984,405 | 78.6 → 79.0 | 29.17 → 29.03 |
| the eleven others | kept | +0.5 % each | +0.5 % | −0.5 % each |
| **sum of fourteen** | | | 456.6 | **169.4 → 167.8** |

With the v2 full-weight fraction of Z(νν) (1,023,164/2.3×10⁶ = 0.4449) in place of 0.4396 the sum is 167.4. The
re-allocation is inside the 665 CPU-h and no pool event exists yet. Two things are **not** settled by it:
(i) the unit cost and weight fraction of the two additions are the Z-type proxies of the addendum; their production
needs its own generator-level filter, because v1's truth-MET > 200 GeV filter removes all of Z(ℓℓ) and a third of
Z(ττ) (§8 item 5); (ii) the multijets have their own loose population of 10⁶ events (STR l.1365-1372): their
allowance through the B4-e factorisation is 1.14 × N_MJ/10⁶ = 48.7 events at the nominal tail (0.81 Gaussian only,
550 with the upper tail) against the planned 0.46.

## 7. Step (4): procedure for A and m_mig (deliverable 5; not executed)

**Not computed, and no signal sample was opened.** Script: `src/p3c/step4_acceptance.py`.

1. Preconditions: the MET model reviewed and frozen (`outputs/p3c/model.json`, sha256 2bf6d28b…95c0, and
   `src/p3c/metmodel.py`), the tail decision of §8 item 1 taken, and an approval record written by the orchestrator.
   The script exits without `--approve <record>` and refuses to overwrite an existing output (computed once, STR §4.1).
2. Inputs: the S1 Stage-2 files of one species-mass (`sim/scripts/convert_hepmc.py` layout: `recoil_eta5`, `jets`,
   `njet`, `p_qp_hard`, `p_qm_hard`, `eta_pair`, `w`) and, for m_mig, the files of the sample with the generator cut
   at 150 GeV. **Requirement:** the conversion must store all jets above 20 GeV; `convert_hepmc.py` keeps four. With
   four, jets beyond the fourth stay unsmeared; the output records the fraction of events affected.
3. Command, once per species-mass:
   `<acts python> step4_acceptance.py --approve <record> --model outputs/p3c/model.json --out <dir>/A_<point>.json --point <label> --s2 <files> --mig <150 GeV files> --gen-cut 200`
4. Definitions (v1's `products.acceptance_point` with the model in place of the 25 GeV smearing; 20 throws per event):
   ε_fid = Σw·F/Σw with F = \|η_pair\| < 2.5; ε_trig = Σw·F·⟨ε_trig⟩/Σw·F; A = Σw·F·⟨ε_trig × presel⟩/Σw;
   ε_presel = A/(ε_fid ε_trig); m_mig = the part of Σw·F·⟨ε_trig × presel⟩ with p_T(QQ̄) before the shower below the
   generator cut, divided by the whole, on the 150 GeV sample. The pair is invisible to the model (STR §4.13, [L11]).
5. Output: one JSON per point with A, the three factors, m_mig and the effective counts for the nominal and for
   every variation of §2.3 (the nuisances correlated with the backgrounds), and A under the trigger nuisance curve.
   Then the m_mig ≤ 5 % rule of STR §4.13 is applied by the session that runs it.
6. Test on background only [V: `outputs/p3c/step4_test_background.json`, labelled "TEST ON BACKGROUND (not a signal
   quantity)"]: one Z(νν) file through the Stage-2 adapter, the neutrinos playing the pair. It gives 0.0303 where the
   yield script gives f_presel = 0.0301 for the same process through a separate code path (which also applies the
   lepton and photon vetoes), and a fraction below 200 GeV of 0.076 against 0.074.

## 8. Open issues and decisions asked for

1. **The jet-response tail (decision needed before the model is frozen and before rule 1 is read).** No public
   Phase-2 source exists (retrieval_log #14, #20, #32–#36). The multijet N_trig is 7.1×10⁵, 4.28×10⁷ or 4.8×10⁸ for
   the three declared settings and the events per pilot count 40.5, 81.9 or 519. Options, all defined before the
   result: (A) the declared nominal with the full variation as width (what the fail branch gives literally: a
   multijet term with half-width 3.9 in ln); (B) the Gaussian-only reading recorded on 16 Nov in retrieval_log #14,
   with the missing tail stated as a limitation and the declared tail as the one-sided upward variation; (C) ask the
   user for a source or a number. Choosing after seeing these numbers is itself a choice made with the result in
   hand; I recommend the orchestrator's advisor call and, if (B) or a new value is taken, that it be recorded as a
   decision with these numbers shown. I have not changed the model.
2. **B4-b external validation FAIL** (both readings; §3): the three additions carry the full variation; limitation
   to be stated in PREREG_v2. No further remediation is possible without a recoil-response parameter that the frozen
   model does not have.
3. **Lost-lepton reading**: literal (unidentified leptons removed from the sum) or electrons kept as calorimeter
   energy (×0.571 for Z(ℓℓ), ×0.885 for Z(ττ)). Flagged at 10:16; for PREREG_v2.
4. **Trigger argument**: the L1 curve evaluated at MET_reco, not at the true MET. Flagged at 10:16.
5. **Production of the additions (Phase 4a)**: Z(ℓℓ), Z(ττ) and the multijets cannot be generated with v1's truth-MET
   filter; they need a filter on the model MET at generator level (the event weight of `metmodel.apply`), with its
   efficiency. Not designed here. The multijets also need p̂_T < 100 GeV checked (4–6 % of the yield sits in the
   lowest generated bin) and a K-factor (K = 1 used).
6. **Step (4) input format**: all jets must be stored in the S1 Stage-2 conversion (§7 item 2).
7. Extrapolations in the model, each stated in §2.2: jet resolution above \|η\| = 2.8 and above 480 GeV; barrel muon
   efficiency; electron efficiency at 1.4–1.6 and 2.8–3.0; no τ_h veto; photon veto weight 0.05 from v1.
8. K_V = 1.4 for the Z processes is v1's uncited value (R-5 open; B4-d is not this work package).
9. R-4 numbers (arXiv:1712.02345 Table 8) were transcribed through the fetch tool, not read on the PDF [U].
10. The scripts are not registered as pixi tasks (`pixi.toml` is outside my write scope); commands are in each
    script's docstring. No git commit was made (brief).

## 9. Self-check

- Strategy commitments of B4-b: model built from cited public parametrisations with the soft term from the public
  source only (§2); external validation executed as frozen and failed, fail branch applied (§3); multijet stability
  under bias changes PASS (§4.1); comparison with v1 and with a published multijet share reported without verdict
  (§4.3); tail and core variation as nuisances (§2.3, §6.1); "no parameters from two public sources" did not occur.
- Decisions implemented as stated: the threshold of S2-e/COM l.366 is unchanged; N_trig of the twelve v1 processes is
  kept in the primary reading (STR l.936); nothing frozen was reworded. One frozen criterion **failed** (B4-b
  validation) and is reported as failed.
- No circularity: σ_soft is derived from Fig. 35 right; the validation uses Fig. 35 left, Fig. 34 and the other
  experiment's figure. The reproduced u_⊥ value is marked "not a test". The limiting-case check is an identity by
  construction and is marked as such.
- Anti-fabrication: every parameter, variation, threshold and verdict rule was written at 10:16 before the first
  number (the log states what I had already seen: the figures and one piece of hand arithmetic). The tail was not
  adjusted when its consequence appeared at 15:10; no variation was dropped for being large; the diagnostic added
  after that look changes no number. The campaign reduction at 15:12 is recorded with its reason.
- Remediation: four attempts for the failed validation (§3.3), with the cause identified.
- Formulas: every formula of §2.2 and §7 has its source or derivation and a substitution or limiting-case check
  (§2.2 "Formula checks"; step-(4) cross-check in §7 item 6).
- Blinding: no signal sample opened; `step4_acceptance.py` ran only with `--test-background`.
- Figures: four, each referenced; "Private work (simulation)", no experiment name or logo; plotting code separate
  (`p3c_plots.py`). The JFC items "two selection approaches", MVA, cut-flow optimisation and closure alarm bands are
  not this work package (T2 and the consolidation).
- Budget: 11.7 CPU-h of 50.

