# Phase 3, work package p3-c: the reconstruction-level MET model of B4-b and its inputs to decision point 2

Executor Birgit (Fable 5.2), 2026-11-24. Session log `phase3_selection/logs/executor_birgit_2026-11-24_10-16.md`
(the plan and every pre-declaration, written 10:16 before any model number existed). Code `phase3_selection/src/p3c/`.
Machine-readable results `phase3_selection/outputs/p3c/` (`model.json`, `validation.json`, `p3c_results.json`,
`SCHEMA.md`). Simulation only; public information only. Tags: VERIFIED [V] (run or read by me, with file or
campaign), ESTIMATE [E], UNVERIFIED [U]. No signal sample was opened and no signal quantity was computed.

## 0. Summary

@@SUMMARY@@

## 1. What was run

@@CAMPAIGNS@@

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

@@REST@@
