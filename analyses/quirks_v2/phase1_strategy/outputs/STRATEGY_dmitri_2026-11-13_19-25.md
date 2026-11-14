# STRATEGY — HL-LHC electroweak quirks, study v2 (Phase 1, JFC) — version 2

Fixer: Dmitri, 2026-11-13 19:25, review cycle 1. This version replaces `STRATEGY_brigitte_2026-11-13_17-55.md` (v1 of
this document, kept unchanged) after the arbiter verdict ITERATE (`review/arbiter/STRATEGY_ARBITER_dagmar_2026-11-13_19-00.md`,
findings M1–M35). The table "Changes since v1" is §13. Arithmetic: `../src/strategy_budget.py` ("script [n]" below
points to its printed section n).
Status: for re-review (cycle 2) and then the user's Gate A. Nothing here has been produced yet except the feasibility
benchmarks. The decisions that belong to the user are collected in §12.1, numbered GA-1 to GA-10.

**Paths.** `REPO` = `/home/users/jdochoa/hllhc-quirks-search`; `QV2` = `analyses/quirks_v2`;
`TT` = `stage2_C001_quirks/theory_track`; `S4` = `TT/acts/stage4`; `AN1` = `TT/data/acts_stage4/analysis/C12FC_v1`;
`SUM` = `TT/data/acts_stage4/analysis/STAGE4_SUMMARY.json`; PLAN = `publication_plan/publication_plan.tex`;
D1…D6 = the digests in `outputs/digests/`; FEAS_A/B/C = the reports in `outputs/feasibility/`; COM = `QV2/COMMITMENTS.md`.

**Tags.** **[V]** VERIFIED: the number was read at the cited file:line or JSON key by the author of the sentence
(Brigitte for text kept from v1, Dmitri for new text), or re-derived (the script section is given). **[E]** ESTIMATE,
with the arithmetic. **[U]** UNVERIFIED: transcribed from a digest, a review or a v1 document and not opened. A number
without a tag in a table inherits the tag in the table caption.

**Labels.** Constraints are **[A1…]**, limitations **[L1…]**, strategy decisions **[SD1…]**. The prefix SD is used
because "D1–D10" are the user's fixed decisions in the brief (written here as "brief D1") and "V1–V13" are the
deviations in `DEVIATIONS.md`. Downscope proposals that need the user's approval at Gate A are **[DP1…]**; downscopes that
would only be triggered later by a failed attempt are **[DT1…]**. All labels are indexed in §7.
**Criterion identifiers** (B1-a, T1-c, …) are those of COM, which is the master list; this document quotes them.

**v1 efficiencies.** No v2 signal efficiency is computed or assumed anywhere in this document. Where a signal
efficiency is needed for planning, it is a v1 number from the tracked record and is written "v1 placeholder".

---

## 0. Summary

- **What v2 is.** A simulation-only search projection for electroweak quirks in a Phase-2-like barrel tracker at
  pile-up 200 and 3 ab⁻¹. The final result is the expected 95 % CL limit on the signal strength on the 40-point
  (m_Q, Λ) grid and the mass reach as a function of the background, with the v2 background marked on it.
  v1 ended with zero-count bounds 7.05 decades above its budget [V: `SUM` → `ladder.SR-G.min_B84` = 1.2346×10⁶,
  log₁₀(1.2346×10⁶/0.11) = 7.05, script [13]].
- **Projected outcome, stated before anything is run.** v2 measures each background term on samples large enough
  to count it where that is possible, and closes each correction on rungs and samples it was not derived from. Where
  the simulation still counts zero, the term stays a bound, and the likelihood keeps it (§4.11). With the no-pile-up
  samples that the cluster can produce (600 CPU-h, 1.4×10⁸ events), a zero count in every term still allows **about
  45 events in 3 ab⁻¹** (sum of the 68 % upper values; predictive median 36, 16–84 % range 24–55) before credits from
  purpose-built cuts and timing [E, script [9]]. The v1 plan would have left 150 + 47. If the zeros persist and no
  credit or biased generation lowers them, the paper's result is therefore **the plan's "middle" outcome with the
  leading terms bounded, not estimated**: a background of order 10¹–10², limited by sample size, and a reach between
  the plan's table entries for B = 100 and B = 30 at σ_ln = 1, i.e. 495–662 GeV (PLAN l.119-123, EST, built on v1
  efficiencies, which are placeholders here). The one-bin
  expected limit at such a floor is about 28 signal events, against 3.0 if the zero-count terms were dropped (script
  [10]). Three things can move this: biased generation (gain not measured; a Phase-2 pilot measures it, §4.4),
  conditionals of purpose-built cuts and the time tag (§4.6), and passing events in the large samples (then the terms
  are estimates, the plan's "real background" outcome). What the paper says in each case is decision GA-3.
- **Cost.** MUST items: **≈ 3,970 CPU-h**; with the SHOULD items in the reduced form proposed here **≈ 4,400 CPU-h**;
  with the full SHOULD items ≈ 4,915 CPU-h [E, §11.2, script [4]]. v1 of this document had 2,950 / 3,275 / 3,798; the
  difference per finding is in §11.2. 1,261 CPU-h of the reduced total rest on unit costs that were never measured;
  they are listed with the Phase-2 measurement that fixes each (§11.2).
- **Calendar.** With 10 usable off-hours slots (two workers carry a graphical session) the cluster gives about
  **174 effective core-h per day in production** and 116 in development [E, §11.1]. With one ITERATE allowance per
  panel review and the Gate-B turnaround, the study takes **about 8 weeks from Gate A to Gate C (58 days; 7 weeks if every review passes at
  once and only MUST items run, 10–11 weeks at 50 % utilisation or with two ITERATE cycles per review)**. **The 2–4 week target of brief D6 is not reachable**: the days without production alone are 44
  (§11.3).
- **Storage.** About **410 GB** on cajuela, 610 GB if the pre-merge candidate store reaches its cap, against the
  1.5 TB soft budget [E, §11.4].
- **Stop rules (brief §7, quoted in §11.6).** A projected compute overrun of more than 30 % of the approved schedule
  stops the study and the user is asked.
- **Three decisions with the largest consequence** (all in §12.1): GA-3 (paper message and size of the no-pile-up
  pool), GA-4 (closure tolerances, eligibility and what an untested term earns), GA-1 (the C1 signal comparison and
  blinding). Proposals: [DP1] B5 reduced; [DP2] B6 on a reduced point set that keeps 5 keV and 1 TeV; [DP3] no MVA as
  the primary selection; [DP4] S4 and S5 not included; [DP5] Herwig comparison at generator level after an install
  attempt.

---

## 1. Physics motivation, model, signature, observable

**Question.** Can a central tracker at the HL-LHC (14 TeV, 3 ab⁻¹, ⟨μ⟩ = 200) find electroweak quirks, and up to which
mass, once the background is estimated instead of bounded?

**Model.** The benchmark is E = (1,1)₋₁: a vector-like Dirac fermion, SU(2)_L singlet with hypercharge −1, in the
fundamental of an SU(2) infracolour group (N_IC = 2), pair-produced by Drell–Yan. The alternate is the scalar Ẽ with
the same charges (FRAMING l.13-17). With no light infracoloured matter the pair stays bound by a string of tension
σ = Λ². For Λ of 0.5–10 keV the pair oscillates over mm to cm and its hits lie in a thin plane through the primary
vertex (a "ribbon") instead of on helices.

**Grid.** The v1 detector grid is kept: {E 200, E 500, E 1000, E 1500, Ẽ 500} × Λ ∈ {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV
= 40 points [V: `S4/run_g1b.py` l.12, l.48]. **[SD1]** No point is added: a grid change would need new admissibility
tables, which rest on Stage 3 at Λ ≥ 15 keV (D4 I4), excluded by brief D8.

**Signature and trigger.** Missing transverse momentum from initial-state radiation: pT(QQ̄) > 200 GeV at generator
level, then an offline requirement MET > 250 GeV, one jet with pT > 100 GeV and min Δφ > 0.5 (D5 §4, [U]
`S4/analysis/products.py` l.43-52). Standard tracking (CKF) removes helical tracks; the plane finder then searches the
remaining hits for a plane through the primary vertex aligned with the missing-momentum direction. In v2 the MET of
signal and backgrounds is computed with one reconstruction-level model (§4.7, §4.13); what the pair does beyond the
tracker (calorimeters, muon system, lepton veto) is an assumption stated in §4.13 [L11].

**Observable and discriminating variables.** The search is a counting experiment in two categories per selection:
SR-T (a late hit in the barrel timing layer) and SR-G (the rest). The candidate-level variables are those of the v1
ladder [V: `S4/WP_RULE.md` §3 as transcribed in D4 §1.2, and l.106 fixed cuts]:

| variable | meaning | rungs |
|---|---|---|
| N_IT2, N_IP2, N_2S2 | number of pixel / pixel+PS / 2S barrel layers with at least two crossings in the plane | fixed cut, R01–R04, R12–R14 |
| w_core | in-plane width of the core hits | R05–R08 (37.5 → 4.7 mm) |
| p(χ²_core) | out-of-plane fit probability | R09–R11 |
| h, o | "not a helix" and "not two straight lines" χ²/ndf | R15–R20 |
| dE/dx | truncated pixel charge | R21–R23 (not used in v2, [SD9]) |
| Δφ(n₃, MET), η(n₃), f_CKF | plane–MET alignment (< 0.15 rad), barrel (\|η\| < 1), share of hits on CKF tracks (< 0.2) | fixed cuts |
| late BTL hit | time tag | category |

**Final statistical result.** (i) Expected CLs upper limits on μ = σ/σ_norm at each grid point, from a pyhf
profile-likelihood model (T1) at the selection chosen by the pre-registered rule (T2). (ii) The expected mass reach as
a function of an assumed background B and its width (the curve of book Table 29.2 redone in pyhf), with the v2 estimate
marked. (iii) The background ladder: v1 bounds against v2 estimates with their closure verdicts. There is no observed
limit: there is no data [A1].

**Analysis type.** Search, simulation only. Blinding (STUDY OVERRIDES): no v2 signal efficiency is looked at before
the background closure verdicts are recorded.

**Signal yield formula.** N_exp = σ_norm · f₂₀₀ · L · A and S = N_exp · ε_sel (book ch25:40 via D3 §2 [U]).
Substitution check with v1 numbers [V: `SUM` → `fallback_points.A2|F|200|1.5|BM` via D4 §4.3; script [13]]:
219.2 fb × 0.04764 × 3000 fb⁻¹ × 0.5035 = 15,774 events; × 9/200 = 710; μ₉₅/N_exp = 1.2458×10⁷/15,775 = 789.7.
Limiting case: ε_sel → 0 gives S → 0 and no limit, as at the seven v1 points with ε = 0.

---

## 2. Backgrounds

v1 model [V: `S4/WP_RULE.md` l.313]: **B = N_trig × [P_PU + P_SM,HS + Σ_t rate_t × P(pass | t)] + B_cosmic + B_halo**,
with N_trig = 4.0848×10⁷ ± 2.0 % triggered events in 3 ab⁻¹ (D4 §2.1, `AN1/bsum_wp.json` → `n_trig` [U]).

Table 2.1. Classification, v1 size (SR-G, events in 3 ab⁻¹; all from D4 §2.3, which read `AN1/bsum_wp.json` [U by me];
"b" = zero-count bound) and the v2 estimator.

| term | class | R04 | R06 | R07 | R09 | v2 estimator (item) |
|---|---|---|---|---|---|---|
| Pile-up random planes | instrumental (combinatorial) | 1.05×10¹⁰ | 3.8×10⁷ | 1.35×10⁵ | 252 b | repaired thinning + independent occupancy model, both closed against direct counts (B2) |
| Decays in flight (π, K kinks) | reducible | 2.1×10⁷ | 3.0×10⁵ | 1.5×10⁵ | 1.7×10⁵ b | Geant4 vertices → Fatras; pass and near-pass probabilities without pile-up × survival and promotion, with the ceiling H (§4.4); conditionals (B1, B3) |
| Prompt pairs from the hard vertex ("PV pairs") | reducible | 3.0×10⁶ | 1.4×10⁵ b | 1.4×10⁵ b | 1.4×10⁵ b | same estimator on the largest no-pile-up sample (7.65×10⁷ events); "not two straight lines" conditional (B1, B3) |
| Photon conversions, V⁰ | reducible | 4.7×10⁶, 3.7×10⁶ | 4.0×10⁵, 3.1×10⁴ | 7.4×10⁴, 5.8×10³ b | 6.5×10³ b, 5.8×10³ b | same, plus displaced-vertex veto (B1, B3) |
| Nuclear interactions (r = 22, 30, 61.5 mm) | reducible | 1.7×10⁵–1.2×10⁶ | ≈ 2–3×10³ | ≈ 3×10³ b | ≈ 3×10³ b | Geant4 (real hadronic physics), vertex veto (B1, B3) |
| Loopers | reducible | 168 b | 168 b | 168 b | 168 b | no-pile-up sample of 7.6×10⁶ events in the common pool (B1) |
| Z(νν)+jets hard-scatter tracks | **irreducible** (real MET, tracks in the road) | 1.2×10⁹ | 9.6×10⁵ | 1.6×10⁴ b | 1.6×10⁴ b | hit-level sample ×5; 5.5×10⁶ no-pile-up events; the estimator of B1 applied to hard-scatter tracks (B4) |
| W(τν), tt̄ 1ℓ | irreducible/reducible | 1–2.4×10⁸ | 0.5–1×10⁵ | ≈ 10⁴ b | 0.2–9×10³ b | hit-level samples; same estimator (B4) |
| 8 proxied processes (W(eν), W(μν), tt̄ 2ℓ, t-channel, tW, WW, WZ, ZZ) | irreducible/reducible | 2.8×10⁸ | 2.2×10⁵ | 2.3×10⁴ b | 2.1×10⁴ b | own hit-level samples (B4) |
| Z(ττ), lost-lepton Z(ℓℓ), multijets with fake MET | reducible / instrumental (fake MET) | absent | absent | absent | absent | new, with a reconstruction-level MET model (B4) |
| Cosmic muons, beam halo, beam gas | instrumental (non-collision) | argued, not in the sum | | | | number from public rates × pointing × timing (B7) |
| **Not in v1's list (added in v2, finding M26):** | | | | | | |
| Secondaries of pile-up vertices (nuclear interactions, decays and conversions of pile-up particles) | instrumental (hits not on helices from the beam line) | absent: Fatras has no hadronic interactions, and B1 treats the triggered event only | | | | test B1-g, below |
| Noise hits; hits from neighbouring bunch crossings | instrumental | inside the top-up at first order (below) | | | | public occupancy and readout window (R-18); B3-c for the timing layer |
| δ-rays, merged clusters | instrumental | not modelled [L8] | | | | bracketed by the resolution and inefficiency tests of B6; limitation |
| **B₈₄ total SR-G** | | 7.5×10¹⁰ | 1.5×10⁸ | 2.0×10⁶ | 1.2×10⁶ | pyhf model (T1) |

Readings that shape v2:
- The pile-up term dominates down to R06. From R07 on the leading terms are single-interaction and SM bounds that do
  not scale with pile-up (D2 §8.1). B1/B3/B4 therefore matter at least as much as B2; the v0.4 statement that a
  data-driven *pile-up* estimate is "the decisive item" is not repeated.
- The bounds are not "1.14/M with M = 500–2000" (PLAN l.76). They are applied to conditional populations of
  M = 13 (γ), 24 (PV pair), 35 (PU), 81 (DIF, Z(νν)) up to 2,000 (D4 I6 [U]). The paper wording follows the record.
- "Measured down 4.9 decades from R04 to R07 by direct count" (PLAN l.166) is the patched central value. The direct
  count falls 5.37 decades (171.55 → 7.29×10⁻⁴ per trial), and at R06 and R07 it lies ×3.8 and ×4.5 *below* the
  patched value (D4 I7 [U]). v2 quotes the direct counts.
- SR-T and SR-G carry identical SM and single-interaction terms in v1: no time-tag credit was given
  (D4 §2.3 [U] `STAGE4_RESULTS.md` l.172). v2 measures this credit as a conditional ([SD6], item B3).
- **Sources added in v2 (COM B1-g).** *Secondaries of pile-up vertices.* A crossing has about 200 interactions with
  about 100 particles each (FEAS_B Task 3 [V]); with the 5.3 % vertex probability measured for 1–10 GeV pions at
  |η| < 1 this is at most ~10³ secondary vertices per crossing [E, script [13]; an upper estimate, most pile-up
  particles are softer or forward]. Their hits are not on helices from the beam line and feed the combinatorial
  term. v1's top-up (×2.3–7.3) scales the hit density to public occupancies that come from full simulation, so the
  *density* of such hits is covered at first order; their *spatial correlation* (several hits pointing to one
  displaced vertex) is not. **Test (Phase 3, 17.5 CPU-h):** 1,000 pile-up events with Geant4 secondaries of the
  pile-up particles injected and the top-up re-normalised to the same occupancy; the ratio of the pile-up plane
  rate at R04–R06 with and without them. If |ln ratio| < 0.10 (10 %, the threshold the arbiter set for an argument in
  place of inclusion, verdict §6 item 22) with a statistical error below 0.03, the source is stated and left out. Otherwise Geant4 secondaries
  are included in every pile-up overlay: about 2.7 s of Geant4 per pile-up event, +160 CPU-h on 216,000 events [E],
  which is re-projected against the stop rule of §11.6. *Noise and out-of-time hits:* the same density argument;
  the public noise occupancy and readout window are retrieved (R-18) and compared with the top-up; if they exceed
  it by more than 10 % the top-up is raised before the freeze, a detector-model reason. *δ-rays and merged
  clusters* are part of limitation [L8].

---

## 3. Technique justification and selection approaches

**3.1 Why a cut ladder with estimators, and not template shapes.** The signal is defined by layer-multiplicity and
geometric quantities of one candidate per event. The backgrounds that matter have rates of 10⁻⁹–10⁻⁴ per trial, far
below what direct simulation can count (direct counts stop near 7×10⁻⁴ per trial at R07). Any selection is therefore
only as good as the *extrapolation* of its background. Counting cuts on layers, a width cut and a fit-probability cut
are quantities for which independent extrapolations exist: exact thinning of a denser sample acts on hit counts; an
occupancy model predicts the probability of two unassociated hits per layer in a ribbon; a geometric probability
without pile-up can be measured on 10⁷–10⁸ events at 11.5 ms each [V: FEAS_A §3.6]. This is the technical reason for the
ladder.

**3.2 Approaches that will be compared (JFC: at least two, one MVA-based, or a documented infeasibility).**

| # | approach | status | figure of merit |
|---|---|---|---|
| A | v1 ladder rungs and the v1 fallback, as fixed selections | candidates of T2 | expected μ₉₅ on the optimisation half |
| B | sensitivity-based choice among the declared selections with a vertex veto and a time-tag split (T2) | primary | same |
| C | BDT on candidate-level variables | **cross-check only** [DP3] | signal efficiency at equal *directly counted* background rate |

A and B share their variables, so they are parametric variants and count as one approach under JFC. The qualitatively
different approach is C.

**[DP3] MVA not used as the primary selection; implemented as a cross-check.**
- *Inputs available:* N_IT2, N_IP2, N_2S2, w_core, χ²_core, h, o, Δφ(n₃, MET), f_CKF, the time tag, hits per layer.
- *What does not prevent it.* Two of the three estimators would work for a score. Repaired thinning redraws hit
  subsets and recomputes every candidate variable, so it can apply any candidate-level cut. P_geo and the pile-up
  factors of B1 are pass probabilities of any selection. v1 of this document said "none applies to an arbitrary
  score"; that was wrong (reviews K-B1, N-B-11, P-C1).
- *The three constraints that hold.*
  1. **Blinding.** A classifier that is a pre-registered T2 candidate must be trained before the freeze, on v2 signal.
     Training looks at the distributions of every input for matched signal candidates, which the blinding invariant
     forbids before the closure verdicts (brief §7; §4.1 "may not be computed"). Training on v1 signal is not
     possible: the v1 hit-level data are lost and the tracked row arrays hold pass flags, not the variables.
  2. **No independent cross-check for a score.** The occupancy model, the only pile-up estimator that does not use
     finder candidates, is built on per-layer probabilities of named cuts and cannot predict a score. A score cut
     would rest on thinning alone, with no B2-c agreement test.
  3. **No training background where the limit is decided.** In v1 no background event survives beyond R08 in any
     sample [U: D4 §2.3]; the classifier would be trained five to six decades above the working rate.
  For the same blinding reason a hybrid candidate (ladder rung, then a score treated as a B3 conditional), suggested
  in review K-B1, is not adopted: it needs the same pre-verdict training on v2 signal.
- *What is done instead (binding, COM MVA-1).* After the closure verdicts and Gate B, a gradient-boosted classifier is
  trained on the signal optimisation half against the directly counted background candidates passing R06, with a
  recipe fixed in the pre-registration (inputs above, default hyper-parameters, one alternative architecture as JFC
  asks). Its working point is the score cut whose **total directly counted background** (pile-up plus attributed
  single-interaction and hard-scatter candidates, the same samples as for R07) equals that of R07. The comparison
  quantity is ε_BDT/ε_R07 on the evaluation half at equal counted background.
- *What is foregone.* That ratio is the measured gain an MVA could give in the regime where it can be validated; it
  is reported in the paper as the estimate of the sensitivity not used. It cannot be converted to a limit, because
  the BDT background at the working region cannot be estimated with a cross-check.
- *Deviation from JFC Phase 3.* JFC compares approaches in Phase 3. Here Phase 3 is signal-blind, so the comparison
  moves to Phase 4c. This is recorded as [SD2] and needs the reviewers' validation.

**3.3 Channels (JFC 09).** One channel (barrel), two orthogonal categories (SR-T, SR-G) split by the time tag. Shared
nuisances are listed in T1. The endcap is not a channel (brief D1).

---

## 4. Per-item strategy

### 4.0 Unit costs and conventions used in every item

Table 4.0. Unit costs on a worker (i5-7500), at 4 jobs per node. Provenance: **M** = measured in the feasibility
phase (JSON keys in `benchmarks_chain.json`, `benchmarks_generators.json`, `benchmarks_runner.json`); **D** = derived
from measured parts, or measured on one event or on toy inputs; **G** = guess, not benchmarked. The contingency of
§11.2 is sized from this column.

| unit | cost | max RSS | output | source | prov. |
|---|---|---|---|---|---|
| PU-200 event through the chain (Pythia overlay, Fatras, digitisation, seeding, CKF) | 13.5 ± 1.1 s (12.9 s alone) | 0.46 GiB | 0.52 MB with 4 trials | FEAS_A §3.3 [V] | M |
| plane-finder trial at ρ = 1, road 0.25, all per-trial work | 11.7 ± 1.1 s (find alone 10.8 s; 9.4 s with 1 job) | same job | — | FEAS_A §3.4 [V]; at the frozen road 0.15 perhaps ×0.77 [E, not measured] | M |
| "B1-type" event = chain + 4 trials | 60.4 s | 0.46 GiB | 0.52 MB | FEAS_A §1 [V] | M |
| ρ = 2 event (2 crossings, 2 trials) | 206 s | **1.46 GiB at 1 event** | 4.0 MB with dumps | FEAS_A §3.1, §3.7: one smoke event | D |
| PU-200 row with one trial (signal row, overlay, hit-level SM event) | 25.2 s = 13.5 + 11.7 | 0.46 GiB | ≈ 0.5 MB | sum of measured parts; the injection mode itself is not benchmarked (FEAS_A open issue 6) | D |
| no-PU single minimum-bias interaction | 11.5 ms | grows 12.6 kB/event | 8.2 kB | FEAS_A §3.6 [V] | M |
| no-PU hard-scatter event (generation with filter, shower, chain) | **45 ms** | — | — | 23.4 ms shower (FEAS_B l.117 [V]) + 14.1 ms for a 10-track gun through the chain (FEAS_A l.235 [V]) + 7.5 ms margin; the generation filter efficiency is not measured. v1 of this document assumed 15 ms, which is below the shower alone (arbiter §2) | G |
| Stage-3 string event, F 500, Λ = 1 / 3 / 5 keV | 0.65 / 18.8 / 67.8 s | 0.21 GiB | 4–8 kB | FEAS_A §3.5 [V], toy kinematics | D |
| Stage-3 event summed over the 8 grid Λ | 95.6 s | | | measured anchors (91 % of the sum) + v1 index shape × 2.14 for the other five Λ [E, script [1]] | D |
| MG5 LO + Pythia shower + conversion | 34 ms per LHE event | 0.2 GiB | 0.72 + 1.05 kB | FEAS_B l.129, listed there as derived [E]; MLM 0–2 jets **not benchmarked**: 50 ms assumed | D / G |
| Pythia (re-)shower, signal / Z(νν)+jet | 21 / 23.4 ms per event | 29 MB | — | FEAS_B Task 3 [V] | M |
| Pythia minimum bias | 2.0–2.5 ms per interaction | 25 MB | — | FEAS_B Task 3 [V] | M |
| NLO fixed-order K at one mass | ≈ 2 CPU-min (+ 3 CPU-min once per process) | 1.0 GiB | — | FEAS_B Task 4 [V], single runs | M |
| Geant4 π± gun, primary mode | 0.134 ms | 71 MB | — | FEAS_B Task 5 [V] | M |
| pyhf: fit / asymptotic CLs point / 20-point scan / 1000 toys | 0.12 / 0.52 / 10.4 / 652 s | 105 MB | — | FEAS_C R9 [V], toy workspace with 31 parameters; the v2 workspace will have 60–100 [L4] | D (toys: G) |
| Argo overhead per job / SSH | 16.8 s / 2.4 s | — | — | FEAS_C R2 [V] | M |

"CPU-h" below means slot-hours at these costs. The Stage-3 number for unmeasured Λ uses the v1 per-event CPU of the
tracked index (F 500, p2/BM: 0.037, 0.080, 0.212, 1.07, 2.53 s at 0.45, 0.6, 0.85, 1.5, 2 keV [V: `STAGE3_INDEX.json`])
times the ratio measured at the three anchors (87.3 s / 40.8 s = 2.14). These five Λ values carry 9 % of the sum, so
the interpolation is not what limits the estimate; the toy kinematics and the ×5–10 event-to-event spread are
(FEAS_A §3.5).

**Closure tests: common definitions (binding for B1–B5; changed in v2, findings M3, M4, M5, M15).**

*1. Derivation and test are disjoint.* Every closure test names (i) the sample and the rungs on which a correction,
a conditional or a model parameter is **derived**, and (ii) a **test** sample with different generator and pile-up
seeds, read at rungs that were not used for the derivation. A comparison at the derivation rungs, or between two
samples of the same construction at the same rung, is called a **consistency check**: it is reported, it can reveal a
bug, and it gives no verdict. The sample roles are in the inventory, §4.17.

*2. Statistic.* For a prediction P and a direct count N with exposure T: r = P·T/N. N is counted **after** the cut
under test. σ_tot² = 1/N + s_P², with s_P from the event bootstrap of the prediction (trials within an event are
correlated).

*3. Evaluable rungs.* A test rung is **evaluable** for a tolerance F if σ_tot ≤ ln F / 3. Then a correct estimator
(r = 1) violates |ln r| ≤ ln F with probability 0.27 %, and an estimator wrong by F^1.5 or F² is caught with
probability 93 % or 99.9 % (at the limiting precision; at r = F exactly the probability is 50 %, by symmetry).
In counts: N ≥ 55, 64, 121 for F = 1.5 and N ≥ 19, 20, 24 for F = 2, at s_P = 0, 0.05, 0.10 [V: script [11]].
v1's threshold "N ≥ 20" gave a 9.8 % false-fail rate for F = 1.5 (script [11]).

*4. "Within a factor F" means all of:*
 (a) |ln r| ≤ ln F at every evaluable test rung;
 (b) the χ² of the vector of ln r over the evaluable test rungs against zero has p_b > 0.05, with the covariance
     V = V_boot + s_model²·J. V_boot is the joint bootstrap covariance of the nested counts and the prediction
     (the rungs are cumulative, so the off-diagonal elements are not zero). J is the all-ones matrix: s_model is one
     common systematic width per estimator and enters every element;
 (c) s_model ≤ ln F, and s_model is a **number fixed in the pre-registration**: the r.m.s. of ln r of that estimator
     on the development samples (Phases 2–3), or a larger declared value. It is not changed after the freeze and it
     is the width used in the likelihood (with the extrapolation term of point 7).
 F is not a free choice per test: 1.5 for the pile-up estimators, the conditionals and the sideband; 2 for the
 single-interaction and hard-scatter estimators (decision GA-4). Limiting cases: s_model → 0 reduces (b) to a
 statistical compatibility test; with s_model at its cap, (a) implies a small χ², so the resolving power is in (a)
 and in the cap (c). Check on a known failure: v1's thinning (ln r = +0.406, +0.474, −0.455, −0.954 at R04–R07) fails
 (a) at all four rungs for F = 1.5, while a diagonal χ² with s_model at the cap gives 9.2 on 4 degrees of freedom,
 p = 0.057, which would pass [V: script [11]; review N-B-2]. The paper reports this retroactive test as the
 demonstration of power. JFC's alarm band applies to (b): χ²/ndf < 0.1 is investigated as a possible tautology.

*5. Verdicts (four classes).*

| verdict | definition |
|---|---|
| PASS | at least one evaluable test rung; (a) holds; p_b > 0.05; (c) holds |
| FAIL | (a) violated at an evaluable rung; or p_b < 0.05/K; or the re-test of an INVESTIGATE case fails |
| NOT TESTED | no test rung is evaluable at the produced statistics (including "no direct count") |
| NOT EVALUABLE | the test could not be executed: an input is missing, a [DT] downscope removed it, or one of the two quantities compared does not exist (for example B2-c when thinning has no effective counts) |

 K is the number of (b) tests in the *eligibility family*: all closure criteria that can apply to a leading term of
 any T2 candidate. K is fixed in the pre-registration; the planning value is 12. A (b) test with
 0.05/K ≤ p_b < 0.05 is **INVESTIGATE**: a regression ticket is opened, and the test is repeated **once** on the
 reserved fresh sample (§8, failure protocol); the fresh sample alone gives the verdict, with p_b > 0.05 and (a).
 Family-wise size of this rule for a correct analysis: 7.5 % for K = 12 (10.4 % including criterion (a) at 0.27 %
 per test), with 0.55 expected re-tests; v1's rule (every test at p > 0.05) passed a correct analysis with
 probability 0.54 [V: script [11]].

*6. What a verdict earns (default; the user decides at Gate A, GA-4).*
- PASS: the estimator is used, with the closure nuisance of point 7.
- FAIL: the estimator is not used for any selection, and a selection for which the term is leading is not eligible
  in T2 ([SD8], unchanged from v1; a failed conditional or time-tag fraction only loses its credit). Where the term
  is shown, it is at its **no-credit value** (defined per item: the direct count, or the direct zero-count bound, or
  the ceiling H of §4.4). No scale-factor patch.
- NOT TESTED or NOT EVALUABLE: **no credit.** The untested factor enters at its no-credit value (a survival or
  promotion probability at 1, a conditional at 1, a time-tag fraction at 1). The selection stays available in that
  form and is flagged "not tested" in the ladder figure and the result tables.
 A term is never "leading or not" on the strength of a failed or untested estimate: the size used to decide it is
 the no-credit value, the same value that enters the likelihood (§4.12).

*7. Extrapolation width, always added (finding M4).* The working selections lie 1–13 rungs beyond the last rung
with direct counts. For every quantity that is carried beyond its last evaluable test rung (thinning, the occupancy
model, the promotion probability of B1, every conditional, the time-tag fraction), the log-normal closure nuisance
at rung r has the width

  s_tot(r)² = s_model² + (b̂² + σ_b²)·d_in² + b₀²·d_out² .

 - b̂ ± σ_b is the slope of ln r against the rung index, fitted on the evaluable test rungs **inside one cut family**
   (counting R01–R04, width R05–R08, fit probability R09–R11, 2S R12–R14, shape R15–R20). With fewer than three
   evaluable rungs in the family, σ_b := b₀.
 - d_in is the number of rungs between the last evaluable test rung and r inside a family that has a fitted slope;
   d_out is the number of rungs in families with no evaluable test rung.
 - b₀ = ln F of that estimator.
 *Where the form comes from.* Inside a tested family the tested rungs constrain a linear trend ln r = a + b·d. The
 prediction is not corrected by the fitted line (that would be a patch), so the possible bias b̂·d is carried as a
 width, and the slope error σ_b·d is added in quadrature; the constant term is covered by s_model. In a family with
 no tested rung nothing constrains the trend, and the width cannot be derived from the data; the convention is one
 tolerance per rung, coherent (linear in d_out). Its scale is tied to the one cross-family trend in the record:
 v1's thinning drifted by 0.36 per rung from R04 to R07 (D4 §3.3 [U]), against ln 1.5 = 0.405. The alternative
 (independent steps, b₀·√d_out) is in GA-4.
 *Checks.* d_in = d_out = 0 gives s_model. A perfect, well-measured estimator (b̂ = σ_b = 0) inside its family gives
 s_model at any distance. Substitution with the slope errors expected at the planned counts (0.029 per rung for
 pile-up, 0.097 for decays in flight, review N-B-3 [U]) and placeholder s_model of 0.20 and 0.35: pile-up 0.20 at R08,
 0.45 at R09, 1.23 at R11, 2.44 at R14; single-interaction promotion 0.36 at R08, 0.78 at R09, 2.11 at R11 [E, script
 [12]]. So an extrapolated factor is worth little beyond R09–R11 unless a test reaches the family. Two things
 shorten the distance: an evaluable **agreement of two independent estimators** at a rung (B2-c) makes that rung the
 new origin of d_out for both, with max(s_model, |ln ratio|) as the constant term; and a quantity that is **measured
 directly** at the deep rung (P_geo and the ceiling H of §4.4, on no-pile-up samples) carries no extrapolation at all.

*8. Trend as a diagnostic.* b̂ and σ_b are reported for every estimator. There is no separate pass/fail on the
slope: its effect is the width above, continuous in b̂.

A failed criterion is reported as failed. Nothing is patched by a scale factor as v1 did with ×2.41.

### 4.1 C1 — port and reproduction of v1 (MUST, Phase 2)

**Method.** The chain already runs on linux-64 with the pyacts 48.0.0 wheel and no API change (FEAS_A §2.3 [V]).
C1 reruns the v1 code with the logged port edits (FEAS_A §2.4; `QV2/CHAIN_PROVENANCE.md`) and the operative frozen
configuration, T_seed = 4 and road 0.15 [V: `S4/frozen_inputs.json` l.17, l.37-38], on the subset below, and compares
with the tracked `C12FC_v1` numbers.

**Corrections to the plan and to D4.**
- PLAN l.265 "bring the 46 GB back": the data are lost (brief §0). C1 is a regeneration.
- D4 §5.1 proposed bit-level Stage-3 comparisons and "the same 200 rows". Neither is possible: the Stage-2 events
  must be regenerated, the v1 LHE files are lost, and nothing shows that MG5 reproduces the same event stream on
  another platform. ACTS random streams also differ between libc++ and libstdc++ (FEAS_A §3.2 [V]). **Every C1
  comparison is statistical and unpaired** [A2]. The kernel-level identity is already covered: Stage-1 numerics agree
  with v1 to ≤ 1.2×10⁻⁷ relative except one conformal run (FEAS_A §3.2 [V]).
- Lost frozen inputs (D4 I4): the admissibility tables and δ₉₅ = 0.15 are used as the frozen transcriptions in
  `WP_RULE.md` A.1/A.2b and `frozen_inputs.json`. They cannot be regenerated without Stage 3 at Λ ≥ 15 keV [A3].
- The probe-row exclusion file `fix_r1/f1r_summary.json` is lost (D1 §5). The ported code now raises instead of
  silently skipping it (FEAS_A §2.4). Phase 2 must decide, from the tracked row arrays `AN1/signal_rows_a2.npz`,
  whether the exclusion can be reconstructed; if not, C1 states that its signal denominators include probe rows that
  v1 excluded, and the comparison uses the v1 counts over the v1 denominators as recorded.

**Declared comparison subset (brief D5).** v1 values from D4 §5.2 (read there from the JSON; [U] by me except where
marked). N = 41 scalar comparisons.

| family | quantity | v1 value | v2 sample | n |
|---|---|---|---|---|
| PU ρ = 1 | groups per trial at R04, R05, R06; count at R07 | 171.55, 49.72, 0.2470; 35/48,000 | 4,000 events, 16,000 trials | 4 |
| PU ρ = 2 | ⟨S_ded⟩ per trial at R04, R05, R06 | 114.36, 30.96, 0.389 | 1,000 events, 2,000 trials | 3 |
| PU closure | the failed ratios T1 (R04), T1w (R05); trend slope; c-factor | 1.5001, 1.6061; −0.3608; 1.1964 | same | 4 |
| PU R08, R09 | zero counts: v2 count against v1's 0/48,000 | 0, 0 | same (conditional binomial) | 2 |
| C′₀ (no PU) | f_pre for DIF, NI at 22 mm, PV pair | 0.9495, 0.7593, 0.9031 | v1 sizes | 3 |
| C′_PU | attributed counts at R04 and R05 for DIF, γ, V⁰; PV pair at R02 | 166/81, 153/86, 859/358 per 500; 24/500 | 1,000 events each; PV pair 2,000 | 7 |
| rates | per triggered event: DIF, PV pair, γ; N_trig total and Z(νν) share | 1.5945, 30.31, 0.379; 4.0848×10⁷, 2.508×10⁷ | generator level | 5 |
| SM | Z(νν) hard-scatter candidates per event at R04, R05, R06 | 19.52, 4.51, 0.0162 | 2,000 events | 3 |
| signal E 200, 1.5 keV (fast path, as v1) | pass counts at R04, R06 (open tier); R07, FB2 (sealed tier, GA-1) | 41, 33, 18; 9 of 200 [U: D4 §4.2-4.3; the arbiter read 9/200 and FB2 in `SUM`] | 400 rows | 4 |
| signal E 500, 3 keV (full chain, as v1) | R04 (open); R07, FB3 (sealed) | 61, 48; 11 of 200 | 400 rows | 3 |
| signal E 200, 2 keV (fast path, as v1) | R04 (open); R07, FB3 (sealed) | 45, 31; 10 of 200 | 400 rows | 3 |
| arithmetic (exact, not in N) | v2 code on the v1 recorded counts reproduces B, σ_ln per term and B₈₄ per rung | `AN1/bsum_wp.json` → `ladder` | — | — |
| Stage 3 (diagnostic, not in N) | hits per event and status fractions at the three points | e.g. 21,137 hits / 463 events at E 200, 1.5 keV [V: `STAGE3_INDEX.json`] | 463–492 events | — |

Rungs R04–R09 of the dominant terms are covered as far as counts exist. From R07 (SM, C′) or R08 (PU) on, the v1
entries are zero-count bounds; there the only possible tests are the zero-count compatibility and the arithmetic row.

**"Within statistical errors" (fixed now).**
1. Per quantity: counts ≥ 10 use z = (ln x₂ − ln x₁)/√(s₁² + s₂²), with the event bootstrap for pile-up quantities
   (trials within an event are correlated); smaller counts and efficiencies use an exact test (conditional binomial
   for two Poisson counts with known exposures; Fisher for k/n). Each gives a two-sided p_i.
2. Individual pass: p_i > 0.05/41 (Bonferroni; |z| < 3.2). Global pass: Σ z_i² below the 99th percentile of χ²₄₁.
   Family coherence: in each family the inverse-variance mean of ln(x₂/x₁) has |z| < 3 (this catches a common drift
   of a few per cent that individual tests miss).
3. Arithmetic row: central values identical to 10⁻⁶ relative; B₈₄ (a Monte Carlo sum) within 1 %.
4. Power is stated with the verdict. With 4,000 ρ = 1 events the detectable shift (2σ) is about 2 % at R04–R05 and
   6 % at R06; R07 has 12 expected counts (σ_ln = 0.29 [E, script [13]]) and is a gross check only; with 400 rows
   against v1's 200 the signal counts detect only shifts of 34 % (R04) to 80 % (fallback) [E, script [13]]. Quantities with a detectable shift above 50 % are labelled "gross
   check only": they can catch a bug, they cannot validate the port.
5. Fail: the family is investigated through a regression ticket, with no tuning. A family failure blocks decision
   point 1. If three documented remediation attempts do not resolve it, C1 is reported as failed for that family and
   the user is asked (brief §7: a MUST item infeasible after a real attempt).

**Chain used per signal point (COM C1-e; finding M21).** C1 reproduces v1, so each point runs the path v1 used:
the fast path (numpy digitisation, no CKF) at E 200 with 1.5 and 2 keV, the full chain at E 500 with 3 keV
[U: D4 l.317-322]. The same 400 rows of the two fast-path points are also run through the full chain ("twins",
5.6 CPU-h). The twin ratio full/fast is a diagnostic with a declared expectation, v1's paired aggregate over eight
other points: ×0.832 at R04 and ×0.871 at the fallback [U: D4 l.342-343]. It is not one of the 41 comparisons.

**C1 and blinding (precise statement; corrected in v2, findings M2 and M17).**
The C1 signal counts are pass counts of *v1 selections* (R04, R06, R07 and the v1 fallback column) at the three
declared points, on twice the v1 statistics. v1 of this document said that three of the ten are also efficiencies of
a v2 candidate selection. **The correct number is six** (arbiter §2): the three R07 counts (R07 is in T2 family L),
and the three fallback counts, because the v1 fallback at these points is FB2/FB3 with no dE/dx, which is exactly T2
family F [V by the arbiter: `SUM` → `fallback_points`, `r_fb`, `e_adm = null`]. All three points lie in the 20-point
window of the T2 figure of merit. Looking at them before the closure verdicts is an exception to the blinding
invariant of brief §7. **Only the user can grant it; it takes effect only if approved at Gate A (GA-1).**

*Default that this strategy follows if GA-1 is approved as recommended: a sealed comparison.*
- **Open tier (4 quantities):** the pass counts at R04 (three points) and at R06 (E 200, 1.5 keV). R04 and R06 are
  not T2 candidates. They are still efficiencies of v2-generated signal and are correlated with every candidate
  (R07 ⊂ R06 ⊂ R04), so they too are part of the exception; their precision is 34 % (2σ detectable shift at R04,
  400 rows against v1's 200 [E, script [13]]).
- **Sealed tier (6 quantities):** R07 (three points) and the fallback (three points). One comparison script computes
  the pre-declared exact test for each (§ "Within statistical errors", item 1) and writes to the C1 report **only
  PASS or FAIL per quantity** (two-sided, no sign, no z-value, no count). The counts and p-values go to one file
  under `QV2/phase2_exploration/sealed/`, whose sha256 is recorded in the ledger. The script is run by a dedicated
  agent that has no other role in Phases 2–4a; no agent or log reads the sealed file before the closure verdicts are
  recorded (it is opened at Gate B and printed in the paper's reproduction appendix). The twin-ratio diagnostic at
  the fallback is sealed in the same way; at R04 it is open.
- **If a sealed quantity returns FAIL**, the family is investigated first with the open tier and with the background
  families. Opening the sealed file before the verdicts needs the user's decision at that moment.
- *What this costs in validation power:* none in the statistical test (the same exact test on the same counts). What
  is lost before Gate B is the reading of the numbers: a FAIL cannot be diagnosed from its size or sign, and the
  "gross check only" label of the fallback counts (detectable shift 80 %, script [13]) is all the reader has. The
  global χ² over the 41 comparisons is computed by the same script and reported as one PASS/FAIL.
- **Frozen from Gate A on, in every option:** the membership of R07 and of family F (each with and without the
  vertex veto) in the T2 list. The pre-registration may not remove or re-define these four candidates; a
  background-method reason to do so goes to the user.
The options the user is asked to choose from, with what each costs, are in GA-1 (§12.1).

*Signal quantities that exist before the closure verdicts (complete list; COM BL-1).*
1. The C1 quantities above, under the tier approved in GA-1.
2. **The acceptance A = ε_fid × ε_trig × ε_presel and f₂₀₀**, per species-mass, computed in Phase 2 at generator level
   (brief Phase 2 requires f₂₀₀; S1 needs A to decide which events to propagate, [SD10]). They do not depend on the
   plane selection: they are the same number for all 16 T2 candidates, so they cannot steer the choice. They are
   declared here as a second, selection-independent exception and listed in `PREREG_v2.md`. The migration fraction of
   §4.13 (S1-f) is of the same kind.
3. Nothing else. In particular: no other rung count for signal; no distribution of a variable for matched signal
   candidates; no response of the vertex veto or the time-tag split to signal; no efficiency at any v2 candidate
   selection outside item 1; no signal quantity at the other 37 points; no B6 efficiency ratio (its nominal ε comes
   from B6's own nominal rows, paired with the varied ones, and is formed after the verdicts, §4.9); and no "V4-5
   optimality" count on signal rows (moved to Phase 4c, §4.2).
- *Order of decisions.* Any change of the offline MET threshold that the public trigger curve may require (§4.14 (d))
  is decided and logged **before** A is computed on the v2 samples.
- *Separation.* The C1 rows use their own seed stream and are never part of the S1 sample. The T2 candidate list and
  figure of merit are fixed in this document, before any C1 number exists.
- The C1 signal sample stays at 400 rows per point and not the 1,000 proposed in D4 [SD3].

**Other criteria.** (i) Linux reproducibility of the environment: lockfiles tracked, container recipe built and one
C1 job rerun inside it with identical output hash. (ii) Jobs ≤ 30 min, resumable, through `tools/runner` (FEAS_C PASS).
(iii) Pythia pinned to 8.312 for pile-up and SM, 8.313 for the signal shower, as v1 (D1 §2).

**Statistics and cost.** 198 CPU-h [E, script [3]]: ρ = 1 4,000 × 60.4 s = 67; ρ = 2 1,000 × 206 s = 57; C′_PU 5,000 × 25.2 s = 35;
Z(νν) 2,000 × 25.2 s = 14; signal 1,200 × 25.2 s = 8; full-chain twins 800 × 25.2 s = 5.6; Stage 3 at three points 3.6;
no-PU 1.7; generator level 5. The cost is the same in every option of GA-1.
The ρ = 2 jobs also write the pre-merge candidates (an addition that does not change the v1 outputs), so the same
1,000 events are the development sample of B2. **Storage:** 13,000 PU events × 0.52 MB ≈ 7 GB, plus 1,000 ρ = 2 events
at 4.0 MB ≈ 4 GB.
**Dependencies:** Stage 2 at three mass points; runner. **Risks:** ACTS navigation assertion (about 1 in 700 events in
v1, D6 §5 [U]) → the v1 per-event seed replacement is kept; ρ = 2 memory (see B2).

### 4.2 C2 — finder cross-checks (MUST, Phase 2)

The plan's "seed-threshold regression (V4-4)" conflates two v1 items (D4 §6). I opened the v1 plan:
V4-4 is "Reproducibility and seeds", V4-5 is the brute-force cross-check [V: `S4/plan.md` l.1811-1812]; the
seed-threshold stability rule is a third item [V: `S4/plan.md` l.503-510]. C2 runs all three.

| test | definition | pass criterion | fail leads to |
|---|---|---|---|
| **V4-5** brute force | 50 signal + PU events and 50 PU-only trials. For each: an exhaustive scan of plane normals through the primary vertex on a 0.2 mrad grid within ±0.3 rad of the F0 normal, plus a 5 mrad global scan over the road, maximising the resolution-weighted inlier count; and an independent least-squares plane fit on the F0 inliers. Signal events: the first F0-accepted events of the C1 signal rows, in file order, 17/17/16 from the three C1 points. PU trials: the first 50 trials of the C1 ρ = 1 sample with an F0 candidate at R04. | \|Δn\| < 1 mrad between F0 and the brute-force optimum **and** between F0 and the independent fit, in ≥ 48 of 50 signal events and ≥ 48 of 50 PU trials (the v1 "≥ 95 %"); every disagreement inspected and described | reported as failed in §5 of the paper; decision point 1 blocked; regression ticket on the finder; no change of the finder without a new freeze |
| V4-5 optimality (reported, not a pass criterion; **moved to Phase 4c**, finding M17) | in 50 signal rows where F0 has no R04 candidate, does the global scan find a plane that would pass the R04 counting? This count is a signal quantity, so it is formed only after the closure verdicts and Gate B, on stored events of the S1 optimisation half | number reported; answers "near optimal?" (referee Q9) | — |
| **V4-4** reproducibility | 20 production-type jobs rerun on the same node; the same 20 on a second node; two jobs with different seeds | outputs bit-identical on the same node; cross-node identity reported (same CPU model); different seeds give different outputs; all seeds in the markers | failure on the same node blocks production (non-determinism) |
| **T_seed stability** (4 → 2) | the G3 metric of v1: per-trial pass fraction of each rung family (counting R04, width R05–R06, χ², 2S) at T_seed = 4 and 2, on 500 ρ = 1 events (2,000 trials) and 200 ρ = 2 events, from stored hit dumps | \|z\| < 2 for every family at both densities | T_seed stays 4 (no retuning in v2); the paper reports "seed threshold not converged, pass fraction changes by x %" as a limitation; the same finder is applied to signal and background, so this is an efficiency statement, not a bias |

Power of V4-5 [E, script [13]]: if the true agreement were 85 %, 48 of 50 would be reached with probability 1.4 %; at 90 %,
11 %; at 98 %, 92 %. The test can therefore reject agreement below about 85–90 % and no better; this is stated with
the verdict. Blinding: V4-5 uses only F0-accepted events of the declared C1 rows and reports a direction difference;
no efficiency is formed. The script takes the first F0-accepted events in file order and does not print or store how
many rows it scanned to find them, so no pass fraction can be read from its output. The "optimality" count is not
taken in Phase 2.

**Code status.** No V4-5 code exists (D4 §6, D5 §6 [U]). It must be written: a numba scan and a scipy fit, independent
of `finder.py`. **Cost:** 81 CPU-h [E]: V4-5 100 events × 0.3 CPU-h (9×10⁶ normals × hits in the road; to be timed on
one event first); T_seed 44; V4-4 7. **Dependencies:** C1 samples with dumps for 700 events.

### 4.3 C3 — paper corrections (MUST, Phase 5; list frozen now)

**Method.** The plan names seven errors (PLAN l.241-251). The binding list is longer: all 24 items of D3 §1
(`book/review/UNRESOLVED.md` l.45-74 plus three book-only items), the 19 internal-label families of D2 §5, the
novelty wording of the audit (claim N1, N3, N4 only, each "to our knowledge"; D2 §3), and the statements corrected in
this strategy (§2 readings; the 23–30 µm out-of-plane *resolution* is a planning estimate, not a measurement and not
the scattering floor, D3 §1 item 19).
**Criterion.** (i) A checklist `C3_CHECKLIST.md` with one row per item, each closed with the file:line of the new
text. (ii) A grep of the v2 paper sources for every label family of D2 §5 returns zero hits. (iii) Items on frozen v1
files are listed in one `ERRATA_v1.md`; the frozen files are not edited. (iv) Two items need a primary-source check
before the text is rewritten (Barbashov's solution class; the content of Knapen et al. Sec. III.D): done from the
papers and logged in `retrieval_log.md`. For Knapen et al. the audit already records, from the PDF, that the paper
treats beam-pipe conversions and not the other topologies (`TT/paper/P2_NOVELTY_AUDIT.md` §1.1 [V: read this session]).
(v) Every number in the paper carries a measured / estimated / unverified tag. **Fail:** an open row at Gate C blocks
the gate. **Cost:** no CPU. **Dependencies:** all results.

### 4.4 B1 — single-interaction topologies with hadronic physics (MUST, Phases 2, 3 and 4a)

**Method.**
1. *Physics.* Geant4 11.4.3 with FTFP_BERT on the same cylinders, discs and slabs as the ACTS geometry, generated from
   the one tracked source `TT/acts/geometry/cms_phase2_public.json` (FEAS_B "Geant4 build and integration plan").
   Geant4 tracks each primary (π±, K±, p, K⁰_L, n, γ) in 3.8 T and records every inelastic interaction, decay or
   conversion with all products. Geant4 runs per worker from local scratch (deviation V13); the environment is
   installed on all three workers (commit 199e166).
2. *Hand-over.* The products are written as rows of the v1 particle array (vp, vsec, pdg, q, m, x, y, z, t, px, py,
   pz), which v1's `ParticleSource` already injects into Fatras with their own vertex (D5 §5 [U] `run_chain.py`
   l.79-112). The parent's hits up to the vertex come from Fatras with v1's `Truncate`. The finder therefore sees the
   same detector model as everywhere else. Two hand-over variants (Fatras-truncated parent; Geant4 parent crossings
   converted to hits) are compared on 100 events in Phase 3 and one is frozen.
3. *Which candidates belong to the term (attribution rule, COM B1-f; finding M22).* Pile-up-only planes pass R05 at
   49.7 per trial (§4.1 table), so direct counts on samples with pile-up are dominated by pile-up unless candidates
   are attributed. A candidate is **attributed to topology t** if at least half of its double-crossing layers (the
   layers counted by N_IP2 and N_2S2 for the rung in question) are made of hits from particles of the topology's
   vertex. All other candidates are pile-up candidates and belong to the B2 term. v1 used attributed counts
   (D4 l.196 [U]); its coded rule is transcribed in Phase 2 and printed in the pre-registration. If it differs from the
   rule above, C1 uses v1's rule (it reproduces v1) and v2 uses the rule above, and the difference is measured on the
   C′_PU samples.
4. *Estimator (changed in v2; findings M3, M4).* Split the no-pile-up events of topology t by what they lack for
   rung r: f₀(r) = P_geo(r) is the probability that the event passes r without pile-up; f_k(r), k = 1 … k_max, is the
   probability that it passes the width cut of r and misses the layer-count cut by exactly k double-crossing layers
   ("near-pass"). With pile-up,

     P(r | t) = P_geo(r)·S(r) + Σ_{k=1…k_max} f_k(r)·π_k(r) ,

   where S is the probability that a passing event still passes when pile-up hits are added (survival), and π_k the
   probability that pile-up supplies the k missing layers (promotion). This is the law of total probability over the
   no-pile-up state of the event; by the attribution rule k_max is half the number of layers the rung requires, so
   the sum is complete for attributed candidates. v1 of this document wrote P_geo × C_PU with C_PU measured only on
   passers, which left promoted candidates outside the estimator (review P-A3).
   - **No-credit ceiling.** Since S ≤ 1 and π_k ≤ 1: P(r | t) ≤ **H(r | t) = P_geo(r) + Σ_k f_k(r)**. H is measured
     directly on the no-pile-up sample at every rung, deep ones included, and needs no extrapolation. H applies the
     counting and width cuts only: a subset of hits inside a ribbon stays inside it, but its fit probability and
     shape variables can differ from those of the full candidate, so the fit-probability and shape cuts enter only
     through the conditionals of B3.
   - **Survival.** S is used as a measured number only at rungs where it passes its test; beyond them **S = 1** (it
     is a probability, so this is its no-credit value and no extrapolation rule is needed).
   - **Promotion.** π_k(r) = product over the k missing layers of the per-layer probability that a ribbon of the
     rung's width contains two unassociated pile-up hits. These probabilities are the ones the occupancy model of B2
     measures from hit densities; they do not use finder candidates. Beyond the test rungs π_k carries the width
     s_tot(r) of §4.0 point 7.
   - Limiting cases: no pile-up gives S = 1, π_k = 0 and P = P_geo, the direct no-pile-up count; pile-up so dense that
     every layer is filled gives P = H.
   The background term is B_t = N_trig × rate_t × P(r | t), as in v1.
5. *Biased generation (COM B1-e).* Only stiff configurations can pass a ribbon width of 4.7–9.4 mm. Primaries are
   sampled with a known weight that favours high p_T and directions inside the road, and Geant4 cross-section
   biasing (factor k, weight 1/k) is used in the tracker volumes. The soft bulk is excluded by an **analytic**
   bound: a track of transverse momentum p_T in the field B has radius R = p_T/(0.3·B) (m, GeV, T) and a sagitta
   L²/(8R) over a lever arm L, so below a threshold p_T its hits cannot lie inside the width cut; the threshold
   includes a stated allowance for multiple scattering. The bound is a geometric statement about helices, not a
   measured zero. It is *checked* on the unbiased sample at R05–R06, where counts exist, and the weights are checked
   by comparing biased with unbiased generation at R05 (criterion of §4.0, F = 1.5, on disjoint samples). Residual
   leakage through non-Gaussian scattering tails is a declared limitation of the Fatras scattering model.
   **The gain of the biasing is not measured.** Two kinematic statements can be made now: (i) if the generated
   interaction has no preferred direction with respect to the road, testing every non-overlapping road orientation
   multiplies the exposure by at most 2π/0.30 = 20.9 [E, script [9]]; whether v1's generation already orients the
   topology in the road must be read from the code in Phase 2; (ii) the stiffness gain is the inverse of the
   fraction of events with a stiff pair in a road, which needs the particle spectra. The **Phase-2 pilot** measures
   both: 10⁷ minimum-bias interactions at generator level (6.9 CPU-h), 10⁶ unbiased no-pile-up events for each of the
   four leading topologies (f_k at R04–R07 and the check of the bound, 12.8 CPU-h), and 1,000 overlays of near-pass
   events (7 CPU-h). Until then every number in this document assumes a gain G = 1.
6. *Rates.* rate_t per triggered event is recomputed from Geant4 on the Pythia particle spectra and compared with
   the v1 generator rates (DIF 1.59, PV pairs 30.3, loopers 0.30, NI 0.10–0.12 × 0.22, γ 0.38, V⁰ 0.052 per triggered
   event, D2 l.69 [U]).

**Sample sizes and the floor they leave (finding M6).** For a term with normalisation N_t = N_trig × rate_t and M_t
simulated events, a zero count allows N_t/M_t × 1.14 events at 68 % (§4.11). Table 4.4a gives this for every term,
with M_t from one pool of 600 CPU-h shared between the single-interaction samples (11.5 ms per event) and the SM
hard-scatter samples of B4 (45 ms). The pool is allocated as M_t ∝ √(N_t/c_t), which minimises Σ N_t/M_t at fixed
cost (Lagrange condition; c_t is the cost per event).

Table 4.4a. Zero-count floors, events in 3 ab⁻¹, before any pile-up factor, conditional or time-tag credit, at
G = 1 [E, script [9]; N_trig and the SM breakdown read in `AN1/bsum_wp.json` → `n_trig` [V]; rates [U] as above].

| term | N_t | M_t planned | transfer factor N_t/M_t | floor at 68 % (1.14·N_t/M_t) |
|---|---|---|---|---|
| PV pairs | 1.24×10⁹ | 7.65×10⁷ | 16.2 | 18.5 |
| decays in flight | 6.51×10⁷ | 1.75×10⁷ | 3.71 | 4.23 |
| γ conversions | 1.55×10⁷ | 8.55×10⁶ | 1.81 | 2.06 |
| loopers | 1.23×10⁷ | 7.61×10⁶ | 1.61 | 1.84 |
| V⁰ | 2.12×10⁶ | 3.17×10⁶ | 0.67 | 0.76 |
| NI at 22, 30, 61.5 mm (each) | 9.89×10⁵ | 2.16×10⁶ | 0.46 | 0.52 |
| **single interaction, sum** | | 1.20×10⁸ | | **28.9** |
| Z(νν)+jets | 2.51×10⁷ | 5.50×10⁶ | 4.56 | 5.19 |
| W(τ_h) | 5.41×10⁶ | 2.55×10⁶ | 2.12 | 2.41 |
| W(eν), tt̄ 1ℓ, W(τ_ℓ), W(μν) (each) | 2.2–2.5×10⁶ | 1.6–1.8×10⁶ | 1.36–1.45 | 1.55–1.65 |
| tW, tt̄ 2ℓ, WZ, WW, t-channel, ZZ (each) | 1.0–2.6×10⁵ | 3.6–5.6×10⁵ | 0.29–0.46 | 0.34–0.53 |
| **SM hard scatter, sum (B4)** | | 1.74×10⁷ | | **16.4** |
| **all terms** | | 1.37×10⁸ | 39.8 (sum of means) | **45.3** |

Readings.
- The sum of 68 % upper values over-covers. The predictive distribution of the summed floor (each term N_t/M_t times
  an exponential variable, §4.11) has median 35.8, 16–84 % range 24.1–55.2 and σ_ln = 0.41 [E, script [9]].
- The v1 plan (10⁷ events for four topologies, 10⁶ per SM process) left 150.5 (PV pairs alone 141) + 46.5 events
  [V: script [9]; arbiter §1]. The same 315 CPU-h (v1 sizes at the corrected 45 ms) allocated by the rule above give
  86.2; 600 CPU-h give 45.3; 1,200 CPU-h give 22.7. The floor falls as 1/CPU: reaching 1 event by size alone would
  need 2.7×10⁴ CPU-h, which is the brute-force growth the plan discards (brief D8) and is not proposed.
- Loopers and the NI terms were not in v1's large-sample plan; they are in the pool. The three additions of B4
  (Z(ττ), lost-lepton Z, multijets) have no N_trig yet and are not in the table (§4.7).
- These floors apply to **both categories** unless the time-tag fraction of B3 passes its test, and to the ceiling H
  as well as to P_geo if H also counts zero.
- Biased generation divides the floor of a topology by its gain G. A summed floor of 10, 1 and 0.11 events needs
  G = 4.5, 45 and 412 applied to every term [E, script [9]]. Conditionals with counts multiply a zero-count P_geo
  (§4.11 allows one zero per term); their values do not exist yet.
- **Consequence, stated plainly.** If the large samples count zero and neither biasing nor conditionals lower the
  floors, the leading terms of the deep selections are bounds of about 45 events in total: the plan's "middle"
  outcome in size, "bounded" in kind. If the large samples count events, the terms are estimates (σ_ln = 0.80, 0.63,
  0.53 for 1, 2, 3 counts, script [9]) and the outcome is "middle" or "real background" according to their size.
  The "good" outcome (1–10 events, σ_ln ≲ 1) needs a measured gain G of order 5–50 or conditional credits of that
  size. What the paper says in each case, and the pool size, is GA-3.

**Closure design (COM B1-a; findings M3, M5).**
- *Derivation.* f_k and P_geo on the no-pile-up pool. S and the per-layer promotion probabilities on **derivation
  overlays** (2,000 passers and 2,000 near-pass events per leading topology, overlaid on pile-up) read at
  **R04–R05**, and on the ρ = 1 development sample for the occupancy inputs.
- *Test.* **Test overlays** with different no-pile-up and pile-up seeds (4,000 per leading topology, enriched in
  passers and near-pass events with known sampling weights, plus 1,000 unbiased full-pile-up events per topology),
  read at the held-out rungs **R06–R07**, attributed counts. The prediction uses S from R04–R05 (or 1) and π_k from
  the model. Tolerance F = 2 (§4.0). The R04–R05 comparison on the test sample is a consistency check.
- *Is the test evaluable?* Table 4.4b gives the expected attributed counts without enrichment, from v1's C′_PU
  record. An evaluable rung needs N ≥ 24 (F = 2, s_P = 0.1).

Table 4.4b. Expected attributed direct counts in 4,000 unbiased full-pile-up events of the topology [E: v1 counts
per 500 events, D4 l.196-200 [U], × 8; script [11]].

| topology | R04 | R05 | R06 | R07 | unbiased events needed for N = 24 at R06 / R07 | status of the R06–R07 test at 4,000 test events |
|---|---|---|---|---|---|---|
| decays in flight | 1,328 | 648 | 16 | 8 | 6,000 / 12,000 | needs an enrichment ≥ 1.5 (R06), ≥ 3 (R07) |
| γ conversions | 1,224 | 688 | 104 | 16 | 923 / 6,000 | R06 evaluable unbiased; R07 needs ≥ 1.5 |
| V⁰ | 6,872 | 2,864 | 48 | 0 | 2,000 / no count in v1 | R06 evaluable; R07 unknown |
| PV pairs | 8 | 2 | 0 | 0 | no count in v1 | not evaluable unbiased even at R04; needs an enrichment of order 10²–10³, unknown until the pilot |
| NI (three radii), loopers | ≈ 0 beyond R05 (D4 l.200-201) | | | | — | expected NOT TESTED |

 The enrichment of a test overlay is the inverse of the fraction of no-pile-up events that are passers or near-pass
 at the rung; the Phase-2 pilot measures it. **Expected verdicts, stated now:** γ and V⁰ testable at R06; decays in
 flight testable if the enrichment is at least 1.5–3; PV pairs, the term with the largest floor, testable only if
 the pilot finds an enrichment of order 10²–10³; NI and loopers NOT TESTED. Under the default of §4.0 point 6 a
 NOT TESTED topology enters at its ceiling H: no survival credit and no promotion model, a number that is still
 measured on 10⁶–10⁸ events. v1 of this document promised "closure at R05–R07 per topology", which the planned
 statistics did not allow for five of eight topologies (arbiter §2); this table replaces that promise.

**Acceptance criteria (identifiers of COM).**
- **B1-a closure.** Held-out test as above, per topology, with the verdict classes of §4.0.
- **B1-b extrapolation.** b̂, σ_b and s_tot(r) of the promotion term are tabulated for every T2 candidate (§4.12);
  the width of §4.0 point 7 is in the likelihood whatever the size of b̂.
- **B1-c rates.** Geant4 and v1 rates are compared per topology. The comparison passes if they agree within the
  combined uncertainty of: the FTFP_BERT against QGSP_BERT difference (measured, below), the material uncertainty
  from a public Phase-2 source (R-17), and statistics. Outside it the cross-check is reported as failed and the
  Geant4 rate is used; the v1 number is not restored. v1 of this document used "a factor 2, the size of the material
  band"; that band was a round number and is not used as a criterion or as a nuisance (finding M11).
- **B1-d geometry and Fatras physics.** Material scan Geant4 against the ACTS material map: |Δ(x/X₀)| ≤ 1 % per
  layer; radii and z-extents equal to 1 µm. Before B1 relies on "Fatras has no hadronic interactions", the physics
  list actually active in pyacts 48 is printed and recorded (it was never set explicitly, D5 §7.7). If hadronic
  interactions are on, they are switched off for B1 so that nothing is counted twice.
- **B1-e biased generation.** Weights closure at R05; the analytic bound written with its scattering allowance; the
  pilot's gain per topology recorded before the freeze. If the weights closure fails, generation is unbiased (G = 1).
- **B1-f attribution, promotion and ceiling.** The rule of point 3 in the pre-registration; H(r | t) tabulated at
  every T2 candidate; the per-layer promotion probabilities compared with overlays of near-pass events at R04–R05
  (consistency) and R06 (test, where evaluable).
- **B1-g sources not in v1's list** (finding M26; Table 2.1): the pile-up-vertex secondaries test of §2.
- **Fail** of B1-a for a topology: the term is reported as failed and shown at H; selections for which it is leading
  are not eligible ([SD8], §4.12). NOT TESTED: the term enters at H and the selection stays eligible, flagged.

**Physics-list and composition variations (finding M19).** The Geant4 vertices are regenerated with QGSP_BERT and with
a C/Si/Cu mixture at equal x/X₀, and P_geo is re-measured on 5×10⁶ no-pile-up events each (52 CPU-h). The
physics-list difference is a measured two-model difference and enters as a nuisance on rate_t and P_geo. The
composition variation enters as a nuisance only if R-17 gives a public composition range; otherwise it is reported as
a robustness test [L2].
**Cost.** 914 CPU-h [E, script [3], [4]]: pilot 27 (Phase 2); development 60 and the secondaries test 17.5 (Phase 3);
Geant4 vertices 65 + 15 (below); variations 52; no-pile-up pool, single-interaction share 1.20×10⁸ × 11.5 ms = 383; overlays 42,000 × 25.2 s
= 294 (four leading topologies × 9,000, four others × 1,500). v1 of this document: 481.
**Storage.** No-pile-up events cannot be stored in full (8.2 kB × 1.6×10⁸ = 1.3 TB [E]); jobs write a per-event
summary (rung flags, the near-pass class and key variables, about 50 B) and full records only for passers and
near-pass events at R04: ≈ 33 GB [A4]. No-pile-up jobs are limited to 80,000 events by memory (FEAS_A §3.7).
**Dependencies.** Geant4 on the three workers; C1 chain; occupancy inputs of B2 for π_k.
**Risks and fallbacks.** (1) Material composition: the slabs are Si-equivalent in X₀, but nuclear interactions scale
with λ_I (FEAS_B) [L2]. (2) Hand-over of the parent's hits → two variants compared. (3) If the zeros do not persist in
the large samples, the paper reports the measured irreducible single-interaction background (plan outcome "real
background"); that is a result, not a failure. (4) Geant4 vertex yield: a gun gives a decay vertex in 1.1 % and an
inelastic vertex in 4.2 % of the cases (FEAS_B Task 5 [V], π± of 1–10 GeV at |η| < 1). v1 of this document budgeted
10⁸ guns, i.e. about 5×10⁶ vertices, fewer than the no-pile-up events they feed. v2 budgets **one distinct vertex per
event** without biasing: 1.75×10⁷/0.011 + 6.5×10⁶/0.042 = 1.7×10⁹ guns × 0.134 ms = 65 CPU-h, plus 15 CPU-h for
photon conversions, realistic spectra, discs and I/O [E, script [3]]. Cross-section biasing lowers this; its factor
is recorded with the weights. [DT1] If Geant4-to-Fatras hand-over fails
after three documented attempts: Geant4 is used for the vertex kinematics only, with Fatras propagating all products
from the vertex and no parent truncation, documented with its bias.

### 4.5 B2 — pile-up: repaired thinning and an independent occupancy estimator (MUST, Phases 2–4a)

**What failed in v1.** The thinning prediction (ρ = 2 → 1) under-predicted the direct per-hit-set counts by 1.50 at
R04 and 1.61 at R05, and over-predicted them at R06 and R07 (ln r = −0.455, −0.954) (D4 §3 [U]). The diagnosis is the
candidate grouping: candidates sharing at least half their hits form one group (`group_frac = 0.5`), and at double
density sets merge that are distinct at ρ = 1. In *union* counts a thinning pilot over-predicted (closure 0.654 at
R04; this was the T_seed = 6 pilot, not the v1 production) [V: `S4/g3/G3_REPORT.md` l.77-90; D4 l.289]. So the
failure is in the definition of what is counted.

**[SD4] The counted object is fixed first.** The estimator of v2 is the per-trial rate of **distinct hit sets after
grouping applied at the target density**. For thinning this means: store the pre-merge candidates at ρ = 2, draw
thinned subsets, and apply the grouping to each subset, so that the grouping always acts at ρ = 1. A
density-independent count (union) is computed as a diagnostic only.

**(a) Repaired thinning.** Pre-merge candidates with their hit lists are stored at ρ = 2 for every candidate with
N_IP2 ≥ 6 (the R03 level, which the R05 factorisation test needs and v1 did not keep). Each ρ = 2 trial is thinned
K = 64 times (v1's `nsub`, D4 l.154 [U]) with independent keep/drop draws of v1's thinning unit (transcribed from
the v1 code in Phase 2 and printed in the pre-registration), and the grouping and
all rung cuts are re-applied to each subset. The statistical error is the bootstrap over ρ = 2 events, so the
correlation between the 64 subsets of one trial is included; the effective count is N_eff = 1/s_boot². Thinning has
no fitted parameter, so nothing is derived: every comparison with direct counts is a test.
**(b) Independent estimator.** A semi-analytic occupancy model: per layer, the probability that a ribbon of given
width and thickness through the vertex and along the road contains at least two unassociated hits, measured from the
hit densities of ρ = 1 events as a function of radius and η; combined over layers with measured layer-to-layer
correlation factors. v1's 1.196 is *not* such a correlation: it is the largest ratio over bins of a factorisation
test (D5 §7.5 [U] `WP_RULE.md` l.456), so the correlations are measured anew. No code exists (D5 §6).
*Derivation and test.* All inputs of the model (densities, correlation factors) are derived on the Phase-2/3
development sample (the 4,000 C1 events and the enlarged development sample) using rungs R04–R05 only. The test is
on the independent 96,000-trial sample at **R06–R07**; R04–R05 there is a consistency check.
*How independent it is (finding M14).* For the counting and width rungs (R01–R08, R12–R14) the model uses hits only
and no finder candidate. For the fit-probability rungs (R09–R11) and the shape rungs (R15–R20) it needs the
probability that a random hit set passes the cut, and no population other than finder candidates exists to measure
it: it is taken from the finder candidates passing R06 in the development sample. For those rungs the model shares
its input with thinning, and an agreement of the two there is **not** an independent cross-check; it is labelled so.
**(c) Direct counts.** 24,000 ρ = 1 events × 4 roads = 96,000 trials, independent of the development sample.

**Acceptance criteria (identifiers of COM).**
- **B2-a** repaired thinning and **B2-b** occupancy model: each reproduces the direct counts **within a factor 1.5**
  (§4.0): thinning at R04–R07, the model at the held-out R06–R07. The tolerance is tighter than for B1 because the
  statistical precision is at the per-cent level at R04–R06 and because the pile-up term is extrapolated furthest.
- **B2-c agreement at depth.** At each rung beyond R07 where thinning has an evaluable precision
  (σ_tot ≤ ln 1.5/3 = 0.135 with N = N_eff), the two estimators agree within a factor 1.5 by the same criterion, with
  r = B_thin/B_occ. v1 of this document accepted "twice the combined width, width ≤ 1.0", which allowed a factor
  e² = 7.4 (review K-B6). An evaluable PASS at a counting or width rung moves the origin of the extrapolation
  distance to that rung (§4.0 point 7). Where thinning is not evaluable the verdict is NOT EVALUABLE.
- **B2-d direct sample** of 24,000 events, independent of all development samples.
- **B2-e** ρ = 2 memory and pre-merge storage measured before any campaign (below).
- **B2-f extrapolation width.** b̂, σ_b and s_tot(r) per estimator and T2 candidate; in the likelihood always.
- **B2-g thinning reach.** N_eff per rung measured on the 1,000-event development sample before the freeze, and the
  deepest evaluable rung projected for 3,000 events and written into the pre-registration.
- **Fail.** No ×2.41-type patch. If one estimator fails B2-a/b it is dropped and reported as failed; the term rests
  on the other alone. If both fail, the pile-up term has its no-credit value: the direct count at R07 and, beyond
  it, the zero-count bound of the 96,000 trials, N_trig × 1.14/96,000 = **485 events** [E, script [13]]; no selection
  beyond R07 is then eligible ([SD8]). This is the plan's "closure fails" outcome for pile-up.

**Statistics, and how deep each estimator can be tested.**
- Direct: at the v1 rate 7.29×10⁻⁴ per trial (35/48,000, D4 §2.3), 96,000 trials give about 70 counts at R07:
  σ_ln = 0.120, inside the evaluable limit 0.135 for F = 1.5 [E, script [11]]. 12,000 events would give 35 counts
  (σ_ln = 0.17), not evaluable. At R08 and beyond v1 counted 0 in 48,000 trials, so no direct test is expected there.
- Thinning: v1's bootstrap errors at R04, R05, R06 (0.0077, 0.0079, 0.0060 on 6,000 ρ = 2 trials, D4 l.189) correspond
  to N_eff = 16,900, 16,000, 27,800; the direct count in the same number of ρ = 1 trials is 1,482 at R06 and 4.4 at
  R07 [E, script [11]]. The gain of thinning over direct counting is therefore ×19 at R06 and grows with depth
  between R04 and R06. v1 nevertheless had no ρ = 2 count at R07 (D4 l.240), with merged candidates. **Projection
  [E]:** if the R06 gain holds with pre-merge candidates, N_eff ≈ 80 at R07 (evaluable) and of order 10 or less at
  R08 (the direct rate there is below 2.4×10⁻⁵); so thinning is expected to reach R07 and probably not R08, and
  **B2-c is expected to be NOT EVALUABLE at most deep rungs.** In that case the pile-up term beyond R07–R08 is a
  **one-estimator extrapolation** (the occupancy model) with the width of §4.0: about 0.45 at R09, 1.2 at R11, 2.4 at
  R14 for a placeholder s_model of 0.20 [E, script [12]]. This is said to the user now (GA-4), not discovered at
  Phase 4a.
- More ρ = 2 events are allowed if B2-g shows that they buy a rung (206 s each); a ρ = 3 sample is not (brief D8).
- **[DT2]** If repaired thinning has no evaluable rung beyond R06 on the development sample, its validated range is
  declared as R04–R06 in the pre-registration, logged as a [D] with the user informed, and R07 rests on the
  occupancy model and the direct count.

**ρ = 2 memory: plan to measure, and fallback.** One ρ = 2 event used 1.46 GiB (FEAS_A [V]); v1 recorded 3.9–4.0 GB
at production size (D1 §1 [U]). Workers have 7.5 GiB, no swap, and pods get a limit of 1.5 × the measured RSS.
1. First job of Phase 2: RSS against events per job for 1, 2, 4 and 8 events, one job alone on a node (about 1 CPU-h).
2. If RSS ≤ 1.6 GiB at ≥ 4 events per job: 4 jobs per node. If ≤ 2.5 GiB: 2 per node (2 × 1.5 × 2.5 = 7.5 GiB).
   At v1's 3.9 GiB: one ρ = 2 job per node with one light job beside it (7.5 − 1.5 × 3.9 = 1.65 GiB left). At 5 GiB
   the limit 1.5 × 5 = 7.5 GiB takes the whole node: one ρ = 2 job per node and nothing else [E].
3. Code fallback, to be tried before accepting one job per node: flush candidates to local scratch after every
   trial (needed anyway for the pre-merge store), so that RSS does not grow with events.
4. Schedule effect of the worst case: 3 slots for ρ = 2 → 172 CPU-h take 57 h of wall time, during which the other
   slots of those nodes are idle (up to 7 × 57 = 400 slot-hours lost); this is the largest single item inside the
   utilisation factor of §11.1.

**Storage, redone.** The plan's "0.4 TB" is a different object: 8×10⁴ loose candidates per ρ = 1 trial × ≈ 5 MB of
variables without hit lists × 8×10⁴ trials [V: `S4/G2A_REPORT.md` l.113-114]. For the object v2 needs, the estimate
is [E]: about 8×10³ candidates per ρ = 1 trial have N_IP2 ≥ 6 [V: same file, l.116]; at ρ = 2 an assumed factor 4–16
(pair seeds scale as ρ², more for confirmations) gives 3×10⁴–1.3×10⁵ per trial; a record of variables plus a hit list
is about 224 B raw, about 110 B compressed; so 3.6–14 MB per trial and **21–86 GB for 6,000 trials**, twice that with
the development sample. Planning value 200 GB, hard cap 400 GB. The factor 4–16 is a guess: the bytes per trial are
**measured on the first 10 ρ = 2 events** before any campaign. If the projection exceeds the cap, the threshold is
raised to N_IP2 ≥ 7 (the R03 records are then lost and the R05 factorisation test is reported as NOT EVALUABLE), by a
logged [D] ([DT4]). The ρ = 2 event records themselves are 4.0 MB each with dumps (16 GB for 4,200 events).
**Cost.** 594 CPU-h [E, script [3]]: direct 24,000 × 60.4 s = 403; ρ = 2 3,000 × 206 s = 172; measurements 10 (Phase 2);
occupancy development 10 (Phase 3). A second direct sample of the same size (403 CPU-h) is reserved, not planned
(§8, failure protocol).
**Dependencies.** C1 (same code), dumps for the occupancy model. **Risks.** As above; the ρ = 2 unit cost rests on
one event.

### 4.6 B3 — conditionals for purpose-built cuts, vertex veto, time tag (MUST, Phases 2, 3 and 4a)

**Method.** In v1 the rungs "not a helix" (R15–R17) and "not two straight lines" (R18–R20) earned no credit against
prompt pairs and kinks, because the single allowed bound per term was spent earlier (D4 §1.3). In v2 each such cut is
a measured conditional probability on the large no-pile-up samples of B1: P(pass cut | topology, passes the preceding
rungs). Three conditionals are added:
1. the shape rungs h and o, per topology (COM B3-a);
2. a **displaced-vertex veto** (B3-b): no two-prong vertex at transverse radius above a threshold reconstructed from
   the candidate's hits. Its threshold and vertex-quality cut are fixed in Phase 3 from background samples only;
3. **[SD6] the time tag** (B3-c; late-hit credit, D3 §6.2: missing from the plan). In v1 the probability that a
   prompt candidate carries a late barrel-timing hit was set to 1 for the single-interaction and SM terms.

**The assumption behind every conditional, named (COM B3-d; finding M4, referee Q4).** If P_geo counts zero beyond
R08–R09, the population "passes the preceding rungs" does not exist at the deep rungs. The conditional is then
measured after a looser rung and **assumed to transfer** to the deep one. That is a factorisation across kinds of
cut. It is tested and given a width, as follows.
- Each conditional is measured after at least three different preceding rungs on the no-pile-up samples (R05, R06,
  R07, and R09 where populated), each with ≥ N_min passes **after** the cut (§4.0 point 3; v1 of this document counted
  30 events before the cut, which for a conditional of 0.1 leaves 3 after it).
- *Stability test:* the values after the first two preceding rungs are the derivation; the value after the deepest
  populated rung is the test, on a disjoint half of the sample (events split by seed parity). Criterion "within a
  factor 1.5" of §4.0.
- *Width:* the conditional applied at rung r carries s_tot(r) of §4.0 point 7, with the distance counted from the
  deepest rung at which it was measured.
- *Pile-up:* the conditional measured without pile-up is compared with the one measured on the test overlays of B1
  at R06 (attributed candidates), where evaluable; at the derivation rungs R04–R05 the comparison is a consistency
  check.
- A conditional that fails earns no credit (it enters as 1) and is reported as failed. A conditional that is NOT
  TESTED earns no credit by default (GA-4). v1 of this document gave an untested conditional credit "as a measured
  no-PU number"; that is withdrawn.

**The time-tag fraction (B3-c; finding M16; decision GA-9).** The late hit of a prompt background candidate is a
pile-up or noise hit in the timing layer inside the candidate's footprint, so a no-pile-up measurement does not
exist and a direct count at the nominal window has no events (the book's late fraction is about 10⁻⁴ per window
edge, D3 l.216-217 [U], against 2,000–4,000 overlays). The design is therefore at hit level:
1. *Timing model.* Hit time = time of flight + collision time + resolution. The collision-time spread of the
   luminous region, the resolution of the barrel timing layer with its non-Gaussian tail fraction, the readout
   window and the occupancy from neighbouring bunch crossings and noise are taken from public Phase-2 documents
   (retrieval R-7, extended). v1 used one Gaussian of 35 ps (D5 §4 [U]). A Gaussian alone would overstate the
   rejection by orders of magnitude if the true tail fraction is at the per-cent level (review P-B7).
2. *Prediction.* p_late(t_cut) = (density of timing-layer hits later than t_cut per unit area, measured from all
   pile-up hits of the C1 events, thousands per event) × (the candidate's footprint in the timing layer).
3. *Closure with counts.* The window edge t_cut is moved inward until the predicted fraction is about 10⁻²; on the
   R04 candidates of the direct sample (171.55 per trial × 96,000 trials) the direct late fraction is then counted at
   five values of t_cut. Derivation: the footprint definition on the development sample. Test: the direct sample;
   statistic: ln r at each t_cut, criterion "within a factor 1.5" with the evaluable-rung rule.
4. *Independence from the geometric rungs.* The late fraction at the widened window is measured against the rung at
   R04, R05 and R06 (2.4×10⁴ candidates at R06); its slope enters the width of §4.0 for the deeper rungs.
5. *What the credit can be.* p_late at the nominal window, but never below the sourced tail fraction of the timing
   resolution. If the tail fraction or the out-of-time occupancy cannot be sourced, **no credit is taken** and SR-T
   carries the same single-interaction and SM terms as SR-G, as in v1.

**Blinding.** The veto is designed without v2 signal. Its signal efficiency is unknown until unblinding; for that
reason T2 contains every selection with and without the veto.
**Statistics and cost.** No sample beyond B1, B2 and B4; 40 CPU-h [E]: 5 (hit-level timing measurement, Phase 2), 10
(development), 25 (re-analysis and time-tag closure in 4a). **Dependencies:** B1, B2 direct sample, R-7.
**Risk.** A quirk pair may itself form two-prong vertices; if the veto removes signal, T2 will not choose it.

### 4.7 B4 — complete the Standard Model background (MUST, Phases 3 and 4a)

**Method.**
1. *Hit-level samples for the eight proxied processes* (W(eν), W(μν), tt̄ 2ℓ, t-channel top, tW, WW, WZ, ZZ): 2,000
   events each, as v1's three real samples. tW has no Pythia 2→2 process (D5 §2) and is generated with MG5 (LO, as
   Z(νν)+jet in FEAS_B Task 2). The proxy share of B_SM was 0.147 at R04 and 0.445 at R09 [V: `SUM` →
   `sm_proxy_fraction_of_B_SM`, R04 value read; R09 from D4 §2.2].
2. *Three additions:* Z(ττ), lost-lepton Z(ℓℓ), multijets with fake missing energy.
3. *Hard-scatter tracks with the estimator of B1* instead of zero-count bounds: P_geo, f_k and the ceiling H on
   no-pile-up hard-scatter events of each process; survival and promotion as in §4.4; conditionals from B3. The
   no-pile-up samples come from the common pool of §4.4: **1.74×10⁷ events over the twelve processes, allocated as
   √N_trig** (Z(νν) 5.5×10⁶), at 45 ms per event = 217 CPU-h. Their zero-count floors are in Table 4.4a: 16.4 events
   summed, 5.2 for Z(νν) (v1 of this document: 10⁶ per process, 46.5 summed, 28.6 for Z(νν)).
4. *Normalisation.* v1's K = 1.4 (1.9 for tt̄) is neither computed nor cited (D5 §2 [U]). v2 takes each K from a cited
   public calculation (retrieval task R-5, §6.4) and cross-checks the leading Z(νν)+jet rate with MG5: FEAS_B found
   12.21 ± 0.03 pb (MG5 LO, MET > 200 GeV) against v1's 14.6 pb (Pythia 2→2), ratio 0.84 [V: FEAS_B Task 2]. The
   difference between the two generators enters as the normalisation nuisance of the term (conventions: generator
   comparison for the irreducible background). For tt̄ and the dibosons no second generator is run; their
   normalisation nuisance is the uncertainty of the cited calculation, and this is stated as a limitation of the
   generator-comparison row of §5.1.
5. *Sanity comparison.* The v2 Z(νν)+jets term at the selection most similar to R2's is compared with R2's 0.12 fb
   after cuts at 13 TeV (§6.2), with the differences in detector, pile-up and selection stated.

**The missing-energy model (why and what).** v1 selects events with a truth-neutrino MET > 200 GeV filter
(D5 §6 [U] `S4/analysis/gen_d123.py` l.7, l.58-59). Lost-lepton Z(ℓℓ) and multijets have little or no neutrino MET,
so the filter removes them by construction. v2 therefore defines the trigger and offline MET at reconstruction level:

  MET_reco = | −Σ_jets R_j·p⃗_T,j − Σ_leptons in acceptance p⃗_T − p⃗_T(soft term) |,

with (i) a per-jet response R_j drawn from a public Phase-2 parametrisation with a Gaussian core and a non-Gaussian
low tail, as a function of jet p_T and η; (ii) leptons outside the acceptance or failing identification counted as
lost, with public efficiencies; (iii) a soft term representing pile-up, with a resolution taken **from the public
source only** (R-3). v1 of this document set the soft term "to reproduce v1's 25 GeV smearing" and then validated the
model against v1; that tuning is removed (finding M9). Check by limiting case: R_j ≡ 1, no lost leptons and no soft
term give MET_reco = neutrino MET, i.e. the v1 filter. **No parameter value is quoted here**: the jet response, its
tail, the lepton acceptance and the soft-term resolution are retrieval tasks (R-3), taken from public Phase-2
documents with page references, and the model is frozen in the pre-registration. The same model is applied to the
signal (§4.13, S1-f).
- *External validation (criterion of B4-b).* The model's MET resolution as a function of ΣE_T (or of ⟨μ⟩) and its
  tail fraction above a stated threshold are compared with a **published Phase-2 MET performance figure at pile-up
  200** (part of R-3; a different figure from the ones the parameters are taken from). Tolerance: the larger of the
  uncertainty the source states and the reading error of the published curve, both recorded with the retrieval and
  written into the pre-registration before any multijet sample exists. If no such figure can be sourced, the model
  is **not validated**, and the fail branch below applies.
- *Internal checks.* (b) The multijet yield after MET > 250 GeV, a jet above 100 GeV and min Δφ > 0.5 is stable within
  a factor 2 when the generation bias (p̂T slicing and weights) is changed, with ≥ 100 effective events passing
  (σ_ln ≤ 0.1, so the factor 2 is resolved).
- *Reported, with no verdict.* (a) Continuity with v1: the Z(νν)+jets yield of the reco-MET selection against the v1
  selection (truth MET with 25 GeV smearing). The v1 smearing has no source, so agreement or disagreement validates
  nothing; the ratio is reported. (c) The model's multijet share of the triggered sample against a published
  monojet-type analysis (R-4), with that analysis's √s and pile-up stated; an order-of-magnitude comparison only,
  because fake MET at ⟨μ⟩ = 200 is driven by the soft term, which a lower-pile-up reference cannot test.
- *Systematic.* The tail fraction and the core resolution are varied within the range of the public source; the
  resulting change of N_trig per process is a nuisance correlated across processes and with the signal acceptance.
  For multijets this is expected to be the dominant uncertainty of the term [E].

**Multijets: which events measure the plane probability (COM B4-e; finding M33).** The events that pass the MET
selection are a few hundred effective events; a zero count among them would be a floor of N_trig,MJ × 1.14/100.
v2 pre-registers the factorisation P(r | multijet, MET_reco > 250) = P(r | multijet, looser population), where the
looser population has the same leading-jet p_T range and no MET requirement (10⁶ events through the no-pile-up
chain, 12.5 CPU-h). The factorisation is **tested where it can be**: on Z(νν) and W samples, P(r) is measured in bins
of MET and must be flat within a factor 1.5 (§4.0 criterion, derivation in the lower MET bins, test in the highest).
If it is not flat, the multijet term uses the passing events only and its floor is stated.

**Acceptance criteria (identifiers of COM).** (B4-a) every process of the list has its own hit-level sample; the proxy
fraction of B_SM is zero at every rung. (B4-b) the three additions are in N_trig with the model above; its external
validation and internal check recorded. (B4-c) the hard-scatter estimator closes against the direct hit-level
attributed count within a factor 2. The hit-level sample of each process is split by seed parity: survival and
promotion are derived on one half at R04–R05, and the test is on the other half at the held-out R06 (and R07 where
evaluable). Expected evaluability from v1 (D4 l.191-194 [U]): Z(νν) has 81 raw candidates at R06 in 2,000 events, so
about 200 in the 5,000-event test half: evaluable. W(τ_h) 9.0, tt̄ 1ℓ 5.2 and W(τ_ℓ) 3.0 weighted counts at R06 in 2,000 events: **NOT TESTED at the
planned 2,000 events**, as are the eight small processes. By §4.0 point 6 they enter at their ceiling H. Raising
W(τ_h) to an evaluable count in a test half would need about 10,700 events (+61 CPU-h); this is not done by default
because Z(νν) carries 61 % of N_trig and the others are covered by H. (B4-d) every K-factor has a citation. (B4-e) as above.
**Fail:** a process without a sample stays a proxy and is named as such; a MET model that is not validated means the
three additions are quoted with the full variation as width and the failure is stated.
**Statistics and cost.** 611 CPU-h [E, script [3]]: hit level (11 × 2,000 + Z(νν) 10,000 + W(τ_ℓ), W(τ_h), tt̄ 1ℓ 2,000
each) = 38,000 × 25.2 s = 266; no-pile-up pool share 217; multijet generator level 10⁷ × 23.4 ms = 65 (the measured
shower alone; v1 of this document assumed 10 ms); multijet loose population 12.5; development 50. v1: 407.
**Dependencies.** B1/B3 estimator; MG5 for tW. **Risk.** Multijets need biased generation in p̂T with weights; a few
events with large weights can dominate. Fallback: finer p̂T slices; the effective sample size is reported, and the
likelihood treats each slice as its own weight class (§4.11).

### 4.8 B5 — road-rotation sideband, closed in simulation (SHOULD, Phases 3 and 4a)

**Method.** The data-driven recipe for an experiment: rotate the road away from the missing-momentum direction,
keep every cut, and predict the signal-road count from the sideband roads with a transfer factor T. The simulation
tests the two assumptions never tested: the fake rate is flat in the angle to the MET, and roads in one event are
independent. For pile-up-only candidates flatness holds by symmetry (pile-up does not know the MET direction); the
part that can be non-flat is the hard-scatter component, where jets recoil against the MET and hadronic τ decays lie
near it.
**Why the test is defined on the hard-scatter component (changed in v2; finding M31).** In an SM sample with pile-up
the hard-scatter share of the candidates is 10 % at R04, 8 % at R05 and 6 % at R06 [E, script [13], from the C1 table].
A hard-scatter non-flatness of ×2 moves the total by 6–10 % and one of ×5 by 25–41 %: both would pass a factor 1.5 on
the total (review N-B-6). The test on the total cannot see the effect it exists to measure. Therefore:
- T(Δφ) of the hard-scatter component is measured on the **no-pile-up hard-scatter samples** of B4 (the pool of §4.4,
  10⁵–10⁶ events per process; rotating the road costs the finder on a few hits, 10 CPU-h in all);
- on the samples with pile-up the closure is evaluated on the **truth-attributed hard-scatter candidates** (rule of
  §4.4 point 3) and, separately, on the pile-up candidates.
**Corrected statement.** PLAN l.342-343 calls the book's B₈₄ ≈ 0.17 "the systematic floor … the width used in the
reach". In the book it is the B₈₄ of an *empty sideband in real data* with 8.2×10⁸ trials and a transfer width copied
from a published search; the width of that estimate is σ_ln = 1.105, and 1.14 × 0.05 × e^1.105 = 0.172 [V: script
[13]; D3 §2, §6.3]. What v2 can deliver is the measured non-flatness and non-independence at R04–R07; the width that
enters the reach curve as "the data-driven scenario" is about 1.1 plus the measured non-closure [L3].
**Acceptance criteria (identifiers of COM).** (B5-a) Flatness of the hard-scatter component: per process and for the
sum, the sideband prediction of the signal-road count closes within a factor 1.5 (§4.0) at the evaluable rungs among
R04–R07. Derivation: T from the sideband roads; test: the signal road, which the derivation does not use. (B5-b) The
non-flat part is quantified per process as T_meas/T_flat − 1 with its error, from the no-pile-up samples. (B5-c)
Independence: the pair correlation of pass indicators between roads of the same event is |ρ| < 0.1 at R05 and R06
on the samples with pile-up, or an effective-trials factor is quoted.
**Fail:** the paper presents the recipe as a proposal that does not close in simulation, with the measured numbers.
**Statistics and cost.** Full: 20 roads on 2,000 events of each of the four leading SM samples and on 500 pile-up
events: (8,000 × 19 + 500 × 16) trials × 11.7 s = 520 CPU-h. **[DP1] Reduced (proposed): 8 roads on 1,500 events of
each of the four SM samples, 20 roads on 500 pile-up events: (6,000 × 7 + 500 × 16) × 11.7 s = 163 CPU-h** [E]. Both
variants add the 10 CPU-h of no-pile-up road rotation and the 20 CPU-h prototype: 550 full, 193 reduced.
*Lost with the reduction:* (i) the angular granularity on the samples with pile-up goes from 18° to 45°; (ii) the
number of sideband trials per process falls from 38,000 to 10,500 (×1.9 less precise); (iii) **R07 drops out of the
closure on the samples with pile-up**: the expected count per process is 7.7 instead of 27.7 [E, script [13]], below
any evaluable threshold (v1 of this document did not state this). What limits the loss: the non-flatness of the
hard-scatter component, the quantity of interest, is now measured on the no-pile-up samples at full granularity in
both variants. **Dependencies.** B4 samples with dumps. **JFC 12.** This is a compute-envelope limit, not a
failed attempt; it needs the user's approval at Gate A (GA-7). **In the paper:** the method section states the number
of roads and events; the limitation index states that R07 was not closed with pile-up; Future Directions names the
full 20-road test.

### 4.9 B6 — detector-model robustness (SHOULD, Phases 3 and 4a)

**Method.** Seven variations: hit resolution × 1.5; hit inefficiency 99 % → 97 %, now applied to pile-up hits as
well (v1 applied it to signal hits only, D5 §4); material × 0.5 and × 2; top-up factors at their low and high limits;
an alternative soft-QCD tune for the pile-up at fixed density (conventions row "qq̄ modelling" translated).
**[SD5]** The top-up variation is a density systematic at fixed ⟨μ⟩ = 200; it is not a pile-up scan (brief D8) (D2 O4).

**Robustness test and nuisance are two different things (changed in v2; finding M11).** ×1.5, 97 %, ×0.5 and ×2 are
the plan's round numbers (PLAN l.345-346). JFC forbids a round-number variation as a nuisance. Therefore:
- The seven variations above are run as **robustness tests**: measured, reported and classified (criterion B6-b).
  They do not enter the likelihood at their measured size.
- The **nuisance** for resolution, inefficiency and material is sized from a public Phase-2 statement (retrieval
  tasks R-15 hit resolution per layer type, R-16 hit efficiency, R-17 material budget and its uncertainty). Its
  effect is the measured log-shift scaled linearly to the sourced size: Δ_nuis = Δ_meas × δ_sourced/δ_varied (in
  ln of the varied quantity). The linearity is checked where two sizes exist (material ×0.5 and ×2 give two points
  on either side). The top-up limits and the alternative tune are already defined by sources (the public occupancies
  the top-up is normalised to, and a published tune) and enter at their measured size.
- If no public number is found for a variation, there is **no nuisance** for it; the robustness result is reported
  and the missing uncertainty is named in the limitation index. Nothing is invented.

**Where each variation is evaluated (COM B6-c; finding M12).** v1 of this document propagated the variations only to
the pile-up rate at R04–R06 and to the signal. From R07 on the leading terms are single-interaction and SM terms.

| nuisance (shared name) | pile-up term | single-interaction terms | SM hard-scatter terms | signal |
|---|---|---|---|---|
| hit resolution, hit inefficiency | 600 (1,000 full) ρ = 1 events per variation, R04–R06; carried to depth through the occupancy model, which is analytic in resolution and per-layer efficiency | P_geo and H re-measured on 2×10⁶ no-pile-up events per variation, at every T2 candidate | same on 5×10⁵ no-pile-up events of Z(νν) and W | rows through the full chain |
| material (rates and scattering) | as above (through hit density) | rate_t from Geant4 with scaled material; P_geo, H as above | as above | Stage-3 reruns with scaled material |
| top-up density, tune | as above | through π_k and S only (occupancy inputs re-derived) | same | pile-up hits around the ribbon: rows through the full chain |
The no-pile-up reruns cost 4 × (2×10⁶ × 11.5 ms + 5×10⁵ × 45 ms) = 51 CPU-h [E, script [3]], in both variants.
Beyond R06 the pile-up shift is not measured directly; the occupancy model carries it and the shift has the
extrapolation width of §4.0.

**Criterion.** B6 is a measurement of sensitivity to assumptions, so its criterion has four parts. (B6-a)
Completeness: every variation is evaluated on every column of the table, with a statistical error on
ln(B_var/B_nom) below 0.1 at R06 and on ε_var/ε_nom below 10 % (pooled over the points). (B6-b) Classification fixed
in advance: a variation is "robust" if |ln(B_var/B_nom)| ≤ ln 2 at R04–R06 and |ε_var/ε_nom − 1| ≤ 0.2; otherwise "not
robust". "Not robust" items are named in the limitations. (B6-c) The table above filled. (B6-d) Every detector
nuisance in the likelihood has a cited source for its size.
**Paired design (review N-C-2).** Each variation is run on the same Stage-3 events, the same pile-up events and the
same seeds for every component it does not change, so that the efficiency ratio is measured on discordant rows
only. The quoted errors below are the unpaired ones and are upper values.
**Blinding (finding M17).** The signal ratios are v2 efficiencies. ε_nom comes from B6's own nominal rows (the paired
partners of the varied rows; they are not S1 rows of either half), and both ε_nom and ε_var are formed only after the
closure verdicts.
**Statistics and cost.** Full: background 7 × 1,000 events × 60.4 s = 117; signal 6 points × 500 rows × 6 variations
× 25.2 s = 126; Stage 3 with scaled material 49; nominal partner samples 38; with the no-pile-up reruns (51) and the
prototype (10): 391 CPU-h. **[DP2] Reduced (proposed, changed in v2; finding M13): background 7 × 600 events; signal
at 4 points × 300 rows: E 200 at 1.5 keV, E 500 at 3 keV, E 500 at 5 keV, E 1000 at 3 keV; nominal partners 18;
236 CPU-h in all** [E, script [4]]. v1's reduced set had
neither 5 keV nor a mass above 500 GeV, i.e. none of the points most sensitive to material (the ribbon thickness is
scattering-dominated above 1.2–1.9 keV, D5 §7.13) and to timing (the slowest pairs), and 9 of the 20 window points
had no variation; the new set costs 29 CPU-h more for the Stage-3 material reruns at 5 keV.
*Lost with the reduction:* no variation is measured for the scalar or at 1,500 GeV; the unpaired error on the pooled
efficiency ratio is 8.2 % instead of 5.2 % [E, script [13]: binomial, v1 placeholder ε ≈ 0.2 at R04].
*Rule for points without a variation (pre-registered).* The log-shift of a point is that of the nearest varied point
in (ln m_Q, ln Λ); its uncertainty is increased by half the spread (maximum minus minimum) of the shifts over the
varied points, added in quadrature.
*Alternative offered in GA-7:* the paired design at all six points of the full set with 300 rows (signal 76 CPU-h
instead of 50, plus Stage 3 for the two extra points), which removes most of the loss.
**Dependencies:** S1 code path; B2; R-15 to R-17. **In the paper:** the method section lists the variations and
which are nuisances; the systematics table gives the sourced sizes; the limitation index lists every "not robust"
item and every variation without a public size.

### 4.10 B7 — cosmic muons and beam halo (SHOULD, Phase 3)

**Method.** Rate per bunch crossing from public measurements × probability that a through-going straight track gives
a candidate in the road pointing to the primary vertex (a toy acceptance on the v2 geometry) × timing acceptance of
the tracker and timing layer × number of triggered crossings. The repo holds one public lead: 8.8 ± 3.1 cosmic and
2.6 ± 0.2 halo events in 586 h of live time in a stopped-particle search (`stage2_C001_quirks/research/
experimental_status_2026.md` l.321, quoting arXiv:1801.00359 Table 4) [U]. That is a calorimeter/muon
selection, not a tracker rate; the cosmic flux at the detector depth and the halo rate are retrieval tasks (R-6).
Beam-gas interactions and satellite bunches are added as one line each, with a public rate or an argument (review
P-C7). The halo number is at `experimental_status_2026.md` l.321.
**Criterion.** A number with its derivation for B_cosmic + B_halo (+ beam gas) in 3 ab⁻¹ at the chosen selection. If
it is below 10 % of the 1σ uncertainty of the total background (B₈₄ − B₅₀ of §4.11) it is stated and left out of the
likelihood; otherwise it enters as a term. (v1 of this document compared with "the smallest term", which is
arbitrary.)
**Fail:** if no public rate can be sourced, the item is reported as "argued, not quantified", as in v1. **Cost:** 5 CPU-h.

### 4.11 T1 — the likelihood (MUST, Phases 2–4c)

This section was rewritten in v2 (findings M1, M7, M8, M32; C items K-C8, K-C9, K-C10). It specifies the statistical
model completely, including what v1 of this document left open: at which background rate the expected limits are
generated when a simulated count is zero.

**1. The model.** For each selection, two counting bins c ∈ {T, G}:

  n_c ~ Pois( μ·S_c·Π_k φ_k^S + Σ_t B_{t,c} ),  B_{t,c} = N_t · w_{t,c} · Π_j (λ_{t,j} / M_{t,j}) · Π_k φ_k^t .

N_t is the normalisation of term t (N_trig × rate_t); w_{t,c} a fixed weight; φ_k log-normal factors of constrained
nuisances shared across terms and categories; μ = σ/σ_norm. Source of the construction: the on/off (Poisson
auxiliary) model of Barlow–Beeston type named in PLAN l.356-358 and in brief §6 ("Gamma constraints for zero
counts"); CLs and the test statistic q̃_μ as in `conventions/search.md` (Read; Cowan et al.; pyhf).

Each background factor is one of four kinds:

| kind | examples | rate parameter | auxiliary measurement | transfer factor | in the fit | in the generation of expected limits |
|---|---|---|---|---|---|---|
| counted | P_geo, f_k and H on no-pile-up samples; direct counts; conditionals measured as counts | λ ≥ 0, the expected simulated count | m ~ Pois(λ), m passing events out of M | N_t·w/M events per unit λ | λ free, constrained only by the Poisson term of m | λ drawn from Gamma(m + 1) (point 2) |
| counted, weighted | biased generation, p̂T slices | one λ per weight class of constant weight w_s | m_s ~ Pois(λ_s) per class | N_t·w_s/M_s | as above, per class | as above, per class; where weights vary inside a class, m and M are replaced by the effective counts (Σw)²/Σw² and the class is flagged |
| estimator output | thinning, occupancy model, survival S, promotion π_k, time-tag fraction | nominal value | — | — | log-normal nuisance: bootstrap error ⊕ s_tot(r) of §4.0 | nuisance drawn from its log-normal |
| no credit | a factor whose test is FAIL, NOT TESTED or NOT EVALUABLE | fixed at its no-credit value (1 for a probability; H; a direct bound treated as "counted") | | | | |

Rules that keep the product well defined:
- *Nested chains collapse.* Successive cuts measured in the **same** sample are not separate factors: the product of
  the ratios m_j/m_{j−1} is m_last/M_first, one count. Separate factors exist only where different samples are
  multiplied (no-pile-up count × overlay factor × conditional from another population × rate). This answers review
  K-C9: no conditional has a denominator that is itself a fluctuating count of the same chain.
- *Poisson for binomial.* m ~ Pois(λ) is used where m/M < 0.1. A factor with a larger pass fraction (and so m ≥ 0.1·M,
  large) enters as a nominal value with a log-normal nuisance of its binomial error.
- *One zero per term.* If the route of a term contains more than one counted factor with m = 0, only the first in
  the order of the cuts keeps its Gamma constraint; the later ones enter at 1. Two empty factors cannot be tested
  for independence where both are empty, and a product of two zero-count bounds would reward a selection for adding
  cuts that the simulation cannot populate.
- *No route double counting.* Each term has exactly one factorisation route, declared in the pre-registration (the
  one whose factors are measured on the largest populations). The other route is a cross-check with its own closure
  number. There is no envelope and no ln 117 width (D4 §3.4, I12).
- *Correlated nuisances (shared names).* Luminosity; N_trig normalisation per process group (generator difference,
  K); pile-up density (top-up) across the pile-up term and every S and π_k; material across NI/DIF rates and signal;
  hit resolution and inefficiency across signal and backgrounds, each evaluated per term as in the table of §4.9;
  the MET model across SM terms and the signal acceptance; one closure nuisance per estimator, correlated across
  the two categories and across the terms that use the estimator; signal: f₂₀₀, trigger, vertex identification,
  Monte Carlo statistics (binomial, as an auxiliary channel).
- *What is limited.* μ = σ/σ_norm. Uncertainties of σ_norm itself (scale, PDF, the infracolour correction of §4.14)
  are drawn as a band on the theory line; acceptance-type uncertainties are profiled (D2 §8.4).

**2. Zero counts: the generation convention [SD7, revised].**
*The problem.* With λ free, m = 0 has its maximum-likelihood value at λ̂ = 0. pyhf's standard expected limits
(Asimov data, or toys generated at the fitted nuisance values; behaviour of pyhf 0.7.6 to be confirmed in Phase 3
[U]) would then generate the term at exactly zero:
Pois(0) never fluctuates, and every term with one empty factor would vanish from the expected limit, whatever M is.
The deepest selections, where the simulation counts nothing, would get the B = 0 limit (2.996 signal events) and the
selection rule would prefer them. All three reviewers found this (P-A1, K-A1, N-A-1).
*The convention.* In every pseudo-experiment used for an expected limit, each counted rate is drawn from the
posterior of a flat prior, **λ ~ Gamma(shape m + 1, scale 1)**; for m = 0 this is an exponential with mean 1. This
is the prior-predictive ("hybrid") construction that v1 used for its toy limits (D4 l.333) and the reading of the
brief's "Gamma constraints for zero counts".
*Why this prior.* Step 1: the likelihood of m is λ^m e^(−λ)/m!; with a flat prior the posterior is the same function
of λ, i.e. Gamma(m + 1). Step 2: integrating by parts m times,
 ∫_{λ_up}^∞ λ^m e^(−λ)/m! dλ = Σ_{k=0…m} e^(−λ_up) λ_up^k/k! ,
so the posterior probability that λ exceeds λ_up equals the Poisson probability of observing m or fewer at λ_up. The
upper quantiles of this posterior are therefore exactly the classical upper limits, which cover for every true λ.
Step 3, substitution: m = 0 gives P(λ > 1.139) = e^(−1.139) = 0.32, v1's 1.14; the 16 %, 50 %, 68 %, 84 % and 95 %
quantiles are 0.174, 0.693, 1.139, 1.833, 2.996 [V: script [9]]. Step 4, limiting case: for large m, Gamma(m + 1) tends
to a Gaussian of mean m and width √m, the standard Monte Carlo statistical uncertainty; the width of ln λ is 1.28,
0.80, 0.63, 0.53, 0.43, 0.10 for m = 0, 1, 2, 3, 5, 100 [V: script [9]].
*Alternatives considered.* (i) Generation at λ̂ (pyhf default): rejected, the term vanishes. (ii) A fixed rate at
the 68 % upper value 1.14/M with no uncertainty (v1's central value): rejected as primary, because it has no shape
and gives a *stronger* expected limit than the convention once the transfer factor exceeds a few events (table
below). (iii) The Jeffreys posterior Gamma(m + ½): its upper quantiles lie below the classical limits, so it
under-covers as an upper bound on a background; not chosen. (iv) A fully frequentist construction with λ profiled in
every toy needs a generation point too, and has none that is not one of the above. (ii) and (iii) are **reported
beside the result at the best point**, as the sensitivity of the limit to the convention.
*The toy procedure, exactly.* For each pseudo-experiment: draw every counted λ from its Gamma(m + 1) and every
constrained nuisance from its constraint density; generate n_T and n_G from the model at those values and at the
tested μ (0 for the background-only ensemble). The auxiliary observations stay at their observed values m: they are
the fixed record of the simulation, not a quantity that a repetition of the experiment would redraw. The test
statistic is q̃_μ from two pyhf fits of the workspace (auxiliary channels with free γ, as in v1 of this document:
pyhf's `shapesys` cannot represent an observed zero, FEAS_C R9). CLs = p_(s+b)/(1 − p_b) from the two ensembles. The
expected limit is the median over the background-only ensemble, with the 16–84 % and 2.5–97.5 % bands. Only the
sampling of the generation point is outside pyhf's built-in toy calculator; the likelihood, the fits and the test
statistic are pyhf's. Consequence used below: the two test-statistic distributions depend on μ and on the observed
m, not on the pseudo-data, so they are computed once per (selection, point, μ) and stored.
*Asymptotic numbers.* Where an asymptotic limit is used (T2 ranking, the comparison table T1-g), the Asimov data
set is built at λ = m + 1 with the auxiliary Asimov observation m + 1, the mean of the same posterior. No quoted
limit is asymptotic.

**3. Definitions that follow from the model (binding wording for the paper).**
- *Predictive distribution of the background:* the distribution of B_c = Σ_t B_{t,c} when every counted λ and every
  nuisance is drawn as in the toy procedure. B₁₆, B₅₀, B₈₄ are its percentiles.
- **B₈₄** (for the background-free flag and the ladder figure): the 84th percentile of that distribution, per category.
- **Total σ_ln** = ½ ln(B₈₄/B₁₆). This is the quantity the plan's central target refers to (σ_ln ≲ 1). It is a
  **reported outcome** with a pre-declared reading: "target met" if σ_ln ≤ 1 at the chosen selection in both
  categories, "not met" otherwise (COM TG-1).
- A term is an **estimate** at a selection if every counted factor of its route has m ≥ 1 and every estimator it
  uses has the verdict PASS; it is a **bound** if a counted factor has m = 0; it is **no-credit** otherwise. The
  ladder figure, the tables and the text use these three words and no others.
- A term is **leading** for a selection and category if the 84th percentile of its own predictive distribution
  exceeds 10 % of B₈₄, computed with no-credit values for every factor that is not PASS (§4.0 point 6).
- **f₀** = (sum of the predictive means of the terms that are bounds) / (predictive mean of B). If f₀ > 0.5 at the
  chosen selection, the paper states that the result is **sample-size limited** and quotes, beside the median
  expected limit, the limit at the 84 % edge of the band as the conservative value.

**4. What the convention does, in one bin (analytic, script [10]).** One bin, one term with m = 0 and transfer factor
κ = N/M, no other uncertainty. Marginalising, P(n | s = 0) = ∫ Pois(n | κλ) e^(−λ) dλ = κ^n/(1 + κ)^(n+1) (the n-th
moment integral gives n!/(1 + κ)^(n+1)); it sums to 1 and has mean κ (checked numerically for κ = 0.5 and 10). With
signal, n is the sum of a Poisson(s) and this geometric variable. 95 % CLs limits on s:

| κ = N/M | term dropped (λ̂ = 0) | fixed B = 1.14 κ | convention: median [16 %, 84 %] | median limit if the true λ is 0.5 / 1.14 / 2 / 3 |
|---|---|---|---|---|
| 0.1 | 3.00 | 3.0 | 3.0 [3.0, 3.0] | 3.0 / 3.0 / 3.0 / 3.0 |
| 1 | 3.00 | 4.1 | 3.0 [3.0, 5.7] | 3.0 / 4.4 / 5.7 / 7.1 |
| 10 | 3.00 | 8.2 | 10.8 [4.2, 23.9] | 8.6 / 15.1 / 25.0 / 36.1 |
| 35 | 3.00 | 14.3 | 27.8 [9.4, 70.0] | 20.6 / 44.2 / 75.2 / 111.7 |
| 124 | 3.00 | 24.9 | 88.0 [24.2, 229.9] | 64.3 / 142.6 / 250.0 / 375.7 |

Readings. (a) Dropping the term gives 3.0 at any κ: at the summed floor of this strategy (κ ≈ 35–40, §4.4) that
would have been optimistic by a factor 9. (b) The convention is weaker than a fixed 1.14 κ for κ ≳ 5, because it
carries the full width of an unmeasured rate. (c) The last column is what the same procedure returns, in the median,
if the true rate is λ and the simulation still counted zero (probability e^(−λ) = 61 %, 32 %, 14 %, 5 %). At κ = 35
the quoted median is too strong by 1.6 if the truth sits at the 68 % upper value, by 2.7 at λ = 2 and by 4.0 at
λ = 3; the 16–84 % band contains the first case and not the other two. **A zero-count expected limit is therefore
quoted with its band, never as a single number**, and with the f₀ statement of point 3.
(d) Coverage, computed exactly for this model with the simulation redone in every pseudo-experiment and a true
signal of 10 events: 0.945–0.956 at κ = 1 and 0.982–1.000 at κ = 10 for true λ between 0.5 and 3; given m = 0 it is
0.950–1.000. The lowest value, 0.945 at κ = 1 and λ = 0.5, comes from the cases m ≥ 1, where the flat-prior
posterior (mean m + 1) over-estimates a background of 0.5 events. This small under-coverage is a known property
of the flat prior at small counts; it is reported, and it is the reason the coverage criterion below is stated
with its statistical tolerance.

**5. Asymptotics or toys.** The expected counts are small and many auxiliary counts are zero, so the conventions'
condition for asymptotics (more than about 5 expected events per bin) fails; v1 found asymptotic/toy ratios of
0.32–1.07 (D2 §2 [U]). **Toys are primary** for every quoted limit and for the final T2 choice. Cost [unit V on a
31-parameter workspace, total E]: 1000 s+b and 1000 b toys at one μ cost 652 s. Two passes are needed (v1 of this
document budgeted one): pass 1 at Phase 4b, the five best selections at the 20 window points on the optimisation
half, 5 × 20 × 8 × 652 s = 145 CPU-h; pass 2 at Phase 4c, the chosen selection, the runner-up and the v1 fallback
at 40 points on the evaluation half, 3 × 40 × 8 × 652 s = 174 CPU-h. The scaling with the number of parameters is not
measured; the v2 workspace will have 60–100, so these numbers may double [L4]. The scaling is **measured in Phase 2**
on a 60–100-parameter workspace built from v1 counts, and the budget is corrected against the stop rule of §11.6.
pyhf 0.7.6 needs numpy 2.2 (FEAS_C O5).

**6. Acceptance criteria (identifiers of COM; the conventions' validation checks, §5.2).**
- **T1-a** The workspace validates against the pyhf schema and is published.
- **T1-b** v1 mode: re-fed with the v1 counts and with v1's treatment switched on (log-normal bounds, uncorrelated
  categories), it reproduces the v1 hybrid-toy limit at the best point within 10 %. Units: v1's number is
  1.2458×10⁷ **events before selection** (`AN1/limits.json` → `expected_toys.median`), i.e. μ₉₅ = 1.2458×10⁷/15,775
  = 789.7 in units of σ_norm [V: script [13]]; the comparison is made on μ₉₅ = 789.7. With the v2 treatment the
  change is reported.
- **T1-c Zero-count convention, four tests** (Phase 3, on workspaces built from v1 counts; test (iii) is repeated in
  Phase 4a on the v2 workspace, 20 CPU-h for the stored distributions at m′ = 0…6):
  (i) *limiting case, zero count:* a one-bin workspace with one term, m = 0 and κ = 1, 10, 35 reproduces the
  analytic limits of the table within the toy error (2,000 toys per μ);
  (ii) *limiting case, large count:* the same workspace with m = 100 and m = 1000 reproduces the limit of pyhf's
  standard toy calculator with a Poisson-constrained `shapesys` within the toy error;
  (iii) *coverage with a non-zero true rate:* at two points of the v1-count workspace, pseudo-experiments with a
  fixed true λ·M = 0.5, 1.14, 2, 3 for the leading zero-count term, the simulated count redrawn (m′ ~ Pois(λ)) and a
  true signal at μ₉₅^exp; the fraction with μ₉₅ ≥ μ_true is at least 0.93 on 500 pseudo-experiments (0.95 minus two
  binomial errors of 0.0097, script [13]); the ratio of the median limit to the quoted median is reported for each λ
  (the analogue of the last column above);
  (iv) *dependence on the convention:* the limit at the best point under alternatives (ii) and (iii) of point 2.
  The fraction f₀ is reported at every selection shown.
- **T1-d Signal injection** (conventions check 2). At three points (v1's best point, one at 500 GeV, one at
  1,000 GeV, v1 placeholder efficiencies in Phase 4a), signal is injected at 0, 1, 2 and 5 × μ₉₅^exp **of that
  point** (not in units of σ_norm: at v1's best point μ₉₅ ≈ 790, so an injection of 1–5 σ_norm would be invisible).
  200 fluctuated pseudo-experiments per level, generated at fixed true rates λ = m + 1 with the simulated counts
  redrawn; μ unbounded in the fit. Criterion: |⟨μ̂⟩ − μ_inj| ≤ 0.20 μ_inj at 1, 2, 5 × μ₉₅^exp; at zero injection
  |⟨μ̂⟩| ≤ 3 standard errors of the mean (0.21 sd(μ̂) for 200 pseudo-experiments, script [13]). The standard error of
  the mean is 4 % of μ₉₅^exp, so a 20 % bias is resolved at 5σ. A failure is investigated (ticket); T1 is not used
  for a quoted limit until it is understood.
- **T1-e Pulls and constraints** (check 3). On the same fluctuated pseudo-experiments: for every constrained
  nuisance the mean pull is compatible with zero (|mean| ≤ 3/√200 = 0.21) and the pull width is reported; any
  nuisance with a mean pull beyond that, or at a boundary in more than 5 % of the fits, is investigated. On Asimov
  data only the **constraints** are read (pulls are zero there by construction): any nuisance constrained to below
  0.5 of its prior is explained.
- **T1-f Impact ranking and pruning** (check 4; conventions pitfall "pruning"). Ranking produced; the leading
  nuisances are named and compared with the expectation (closure nuisances and zero-count constraints). No nuisance
  is pruned unless the fit time requires it; then a nuisance may be dropped only if its impact on μ₉₅^exp is below
  1 % at the three test points, and the quadrature sum of all dropped impacts stays below 5 % of the leading
  systematic.
- **T1-g Asymptotic against toy limits** tabulated at every point (Asimov as defined in point 2).
- **T1-h Coverage at a known signal** (replaces v1's "self-consistency", which was 50 % by construction or a
  1,449 CPU-h nested-toy computation, script [7]). At two points, 500 pseudo-experiments with fixed true rates and a
  true signal at μ_true = μ₉₅^exp; each gets a toy-based limit from the **stored** test-statistic distributions
  (two fits per μ value, 0.5 CPU-h in all, script [3]); the fraction with μ₉₅ ≥ μ_true is at least 0.93. The target
  (0.95 at a known injected signal) is independent of the ensemble that defines the quoted median.
- **T1-i** Toys are primary for every quoted limit; both passes of point 5 are run.
- **Fail:** T1 is not used for a quoted limit until fixed; a failure of T1-b is a regression on the v1 reading.
**Cost.** 420 CPU-h [E, script [4]]: 60 development and tests (Phase 3; the workspace builder starts in Phase 2 on v1
counts), 20 expected results and 20 coverage toys (4a), 145 (4b), 174 + 0.5 (4c). v1 of this document: 224.
**Dependencies:** B1–B4 outputs. A non-MUST lever on the toy cost is in §11.6.

### 4.12 T2 — the selection rule (MUST, Phase 3 definition, Phase 4b application)

**Declared candidate selections.** All share the v1 fixed cuts (N_IT2 ≥ 3, |Δφ(n₃, MET)| < 0.15, |η(n₃)| < 1,
f_CKF < 0.2) and the SR-T/SR-G split.

| family | members | count |
|---|---|---|
| L (cumulative ladder rungs) | R07, R08, R09, R11, R14, R17, R20 | 7 |
| F (v1 fallback without dE/dx, width cut W_c/2^k from the frozen admissibility table per hypothesis) | FB(k_adm) | 1 |
| each with and without the displaced-vertex veto of B3 | ×2 | 16 in total |

**[SD9]** The dE/dx rungs R21–R23 and the dE/dx fallback columns are not candidates: the v1 admissibility for dE/dx
rests on dilution tables that cannot be regenerated [A3], and the pixel charge tail of the backgrounds is not
modelled by the Gaussian digitisation. This is a background-method reason. dE/dx is the standard handle against
minimum-ionising backgrounds for slow heavy particles, so **what is given up is measured** (finding M30; COM MVA-1):
after Gate B, the ratio ε(R_k + dE/dx cut)/ε(R_k) is reported on the evaluation half for the chosen selection R_k,
with the v1 dE/dx cut, next to the statement that its background rejection could not be estimated. The alternative
(model the charge deposit and keep one dE/dx candidate) is GA-6.
The pre-registration may remove candidates from this list, with a logged background-method reason; it may not add
any, and it may not touch R07 or family F (§4.1).

**Rule.**
1. *Eligibility* **[SD8, completed in v2]**. For each candidate, each term enters the likelihood as an estimate
   (verdicts PASS), as a bound (zero count), or at its no-credit value, as defined in §4.0 point 6 and §4.11 point 3.
   - **FAIL** of the closure of a term's estimator (B1-a, B4-c; both of B2-a and B2-b): a selection for which that
     term is leading is **not eligible**. This is v1's rule, unchanged. A failed conditional or time-tag fraction
     only loses its credit (it enters as 1), also as in v1.
   - **NOT TESTED / NOT EVALUABLE**: the selection stays eligible with the untested factor at its no-credit value
     (H for single-interaction and hard-scatter terms; 1 for a survival, a promotion, a conditional or the time
     tag), flagged. v1 of this document was silent on this case, so an untested term could count as passed.
   - "Leading" is decided with the no-credit values (§4.11 point 3), so a failed or untested estimator that
     under-predicts cannot make its own term non-leading (review N-B-12).
   An untested estimator therefore makes a selection worse, by the credit it loses, and never better. The default
   for NOT TESTED is decision GA-4.
2. *Always-eligible baseline (COM T2-g).* R07 with **every term from direct attributed counts or direct bounds** and
   no estimator at all ("R07-direct") is evaluated in every outcome. It gives the paper a limit that depends on no
   extrapolation, however weak.
3. *Figure of merit:* G = mean of ln μ₉₅^exp over the 20 window points (the four E masses × Λ ∈ {1, 1.5, 2, 3, 5} keV;
   the v1 lower edge of the window at pile-up 200 is 1.0–1.2 keV, D2 §2 [U]), with μ₉₅^exp the median expected CLs
   limit under the generation convention of §4.11, the efficiencies from the **optimisation half**, and the full
   background model. The signal efficiency at every point is the one estimator ε̂ = (k + ½)/(n + 1) for k passing of
   n rows (v1 of this document used k/n, and 1/n only where k = 0, which treats the empty points differently from
   the others; arbiter C item). The choice is repeated with ε̂ = k/n (points with k = 0 dropped) and the change of
   winner, if any, is reported. Lower G is better.
4. *Choice:* all 16 candidates are ranked with asymptotic limits (Asimov of §4.11 point 2). The **five best** are
   re-evaluated with toys at the 20 window points (v1 of this document: three), and the toy values decide. If another
   candidate has a toy G within one bootstrap standard deviation of the best (bootstrap over optimisation rows), the
   one with fewer cuts is chosen. With the public v1 row arrays (`AN1/signal_rows_a2.npz`) and the floor table, G and
   its bootstrap spread are computed for the 16 candidates **before the freeze**, with v1 placeholders, to check that
   the tie rule is not decided by noise; no v2 efficiency is involved.
5. *If only the baseline is eligible:* this is the plan's "closure fails" outcome. G is still
   reported for all 16, labelled with their verdicts, and the paper is the method and anatomy paper of PLAN §8.
6. *Background-free flag (COM T2-f):* B₈₄ ≤ 0.11 events per category (the v1 budget, 0.3/2.71 = 0.1107 [V: script
   [13]]), with B₈₄ as defined in §4.11, is reported as a yes/no flag for the chosen selection. It is not a
   requirement. With the floors of Table 4.4a it cannot be met unless the gain G of biased generation exceeds about
   400.

**Robustness of the rule against empty simulation (COM T2-e; finding M1).** A selection must not win because the
simulation has no events there. Three protections: the generation convention keeps every zero-count term in the
expected limit at N_t/M_t per unit λ; "one zero per term" (§4.11) stops deeper cuts from multiplying bounds; and a
deeper rung with the same zero-count terms has the same background and less signal, so its G is worse. **Check
(Phase 3, pre-freeze, on v1 counts):** for the deepest candidate, G computed under the convention must not be better
than G computed with each zero-count term fixed at 1.14·N_t/M_t, minus the toy error, and must be far from the B = 0
value. The one-bin table of §4.11 shows the expected ordering (27.8 against 14.3 against 3.0 at κ = 35).

**Table of extrapolation distances (COM B1-b, B2-f; finding M4).** For every candidate the pre-registration lists,
per leading term: the last evaluable test rung of each estimator and conditional it uses, d_in, d_out, and s_tot.
With the expected test rungs (R06–R07) the distances are d_in = 0–1 and d_out = 0, 1, 3, 6, 9, 12 for R07/R08, R09,
R11, R14, R17, R20. A candidate beyond R11 therefore carries extrapolated factors with widths above 1 unless a test
reaches its cut family (§4.0 point 7); in practice its terms rest on the directly measured P_geo and H.

**Background-side bias of the choice (COM T2-d; finding M29).** Choosing the minimum of G over 16 candidates also
selects downward fluctuations of the background inputs. The choice is repeated on 50 bootstrap replicas of all
background inputs (counts redrawn from their posteriors, estimator outputs from their bootstrap) for the five best
candidates (asymptotic, 14.5 CPU-h). Reported: how often the same candidate wins, and the mean shift of its B₈₄
between the replicas in which it wins and all replicas. If the nominal winner wins in fewer than half of the
replicas, the tie rule (fewer cuts) is applied among the candidates that win in more than 20 %.

**Partial outcomes (review N-C-4).**

| what fails or is untested | selections affected | what the paper shows |
|---|---|---|
| nothing | — | chosen selection with estimates; "target met / not met" by σ_ln; outcome "good", "middle" or "real background" by the size of B |
| PV-pair closure NOT TESTED (expected unless the pilot finds a large enrichment) | all: PV pairs enter at H | same figures; PV pairs labelled "no credit"; the floor of Table 4.4a applies to H |
| PV-pair (or another leading topology's) closure FAIL | every selection where the term is leading at H: not eligible | R07-direct; G for all 16 with verdicts; "closure fails" |
| one pile-up estimator FAIL | all beyond R07: pile-up rests on the other, B2-c NOT EVALUABLE | pile-up labelled "one estimator" |
| both pile-up estimators FAIL | no selection beyond R07 is eligible; the ladder shows the 485-event direct bound | R07-direct; "closure fails" for pile-up |
| a conditional or the time tag FAIL / NOT TESTED | selections using it lose that factor | SR-T equal to SR-G for the term if the time tag has no credit |
| MET model not validated | none removed; the three additions carry the full variation | stated limitation |

**Optimisation/evaluation split.** Each generated signal event gets the half h = parity of
blake2b(salt ‖ species ‖ mass ‖ event index) (the hash family v1 used for seeds, D5 §3). The half does not depend on
Λ, so one physical event is in the same half at all eight Λ. The salt is chosen at the freeze and recorded in
`PREREG_v2.md`; before that the mapping does not exist. The two halves are produced as separate campaigns with
separate directories. The aggregation script takes the half as an argument; its invocation on the evaluation half is
a logged step that requires the Gate B approval record.
**Acceptance criteria (identifiers of COM).** (T2-a) rule, list, figure of merit, estimator ε̂ and salt in the hashed
pre-registration before S1 production. (T2-b) the choice is reproduced by a second run of the script from the frozen
inputs. (T2-c) the optimisation-to-evaluation shift of ln μ₉₅ at the chosen selection is reported per point; a mean
shift above 2σ of its bootstrap error is reported as evidence of selection bias. (T2-d), (T2-e), (T2-f), (T2-g) as
above. **Fail** of (T2-b): Gate B is not requested.
**Cost.** 16 CPU-h [E, script [3]]: 16 × 40 scans × 10.4 s = 2; bootstrap 14.5. Toys are in T1.
**Dependencies.** T1, S1, verdicts of B1–B4.

### 4.13 S1 — signal ×10, full chain at all 40 points (MUST, Phases 2, 4a, 4b, 4c)

**Method.** 2,000 rows per point (v1: 180–200 [U: D4 §4.1]), every row through the full chain (Stage 3 → injection →
digitisation → CKF → finder), at all 40 points. The fast path (numpy digitisation without CKF, 31 of 40 points in v1)
is retired; v1 measured it high by 1/0.87 at the fallback (D4 §4.3 [U]). Rows are split 1,000/1,000 by the T2 hash.
**What "×10" means here (finding M20; decision GA-2).** 2,000 rows are ten times v1's rows in total. The limit is
set on the 1,000-row evaluation half, and v1's limits used its 180–200 template-half rows
(`AN1/acceptance.json` → `finder_note`, read by the arbiter), so **the statistic that sets the limit grows by ×5**.
The plan asks both for "ten times the rows" (PLAN l.371) and for the optimisation/evaluation split (PLAN l.362-363)
and does not say which half the factor refers to. This strategy follows 2,000 rows unless the user chooses 4,000 in
GA-2: at ε = 0.045 (v1 placeholder) the binomial error on the limit half is 14.6 % with 2,000 rows and 10.3 % with
4,000, against 33 % in v1; 4,000 rows cost +827 CPU-h, 4.7 production days [E, script [6], [13]].
**[SD10]** Only events inside the counting acceptance (|η_pair| < 2.5) are propagated: the acceptance
A = ε_fid × ε_trig × ε_presel is formed from generator-level quantities [V: `AN1/acceptance.json` → `definition`,
`factors`], so the events outside need no string propagation. v1 propagated 463–519 events per (mass, Λ) for 200
rows [V: `STAGE3_INDEX.json`].
**Λ range of Stage 3.** Exactly the eight grid values, 0.45–5 keV. Nothing at 7–10 keV and nothing at Λ ≥ 15 keV
(brief D8). The cost is dominated by 5 keV (67.8 s per event, 71 % of the sum) and 3 keV (18.8 s) [V: FEAS_A §3.5].
**Stage 2.** New MG5 + Pythia samples for the five species-masses, 250,000 LHE events each (v1: 100,000 TRG at
E 200/500/1000, 40,000 at E 1500, 50,000 for Ẽ). The yield of unweighted, in-acceptance events per LHE event is
taken from the first chunk in Phase 2 and the sample size is adjusted; v1 reported a budget of only 413–1,277 events
per half at E 1500 and Ẽ 500 (D5 §6 [U]), so those two may need more than 250,000 [L5].
**Acceptance criteria.** (S1-a) 2,000 rows per point through the full chain, ≥ 99 % of jobs complete, ingestion
closure (v1's V4-1: every quirk hit maps to one measurement) passing in every job. (S1-b) no fast-path number in any
result. (S1-c) the efficiencies are first aggregated at Phase 4b (optimisation half) and 4c (evaluation half), not
before. (S1-d) statistical quality, stated in advance and only reported, never tuned: at a point with ε = 0.045
(v1 placeholder, the v1 best point) the binomial error on the evaluation half is 15 %; at ε = 0.03, 18 %; at ε = 0.2,
6 % [E, script [13]]. (S1-e) the split is the frozen hash. (S1-f) the signal passes the same detector-response model
as the backgrounds, as specified below. **Fail** of (S1-a) at a point: the point is reported with the rows it has
and flagged; it is not filled with fast-path rows.
**Signal-side detector response (COM S1-f; finding M27).**
- *MET.* The signal's trigger and offline MET are computed with the same MET_reco model as the backgrounds (§4.7),
  and the model's nuisances are correlated between signal acceptance and SM terms in T1.
- *Migration across the generator cut.* Events with p_T(QQ̄) below the 200 GeV generator cut can pass MET_reco > 250 GeV
  through the response tails; the cut removes them by construction. A validation sample with the cut lowered to
  150 GeV (5 × 10⁵ LHE events, 7 CPU-h) measures, at generator level with the MET model, the fraction m_mig of the
  accepted signal that comes from below 200 GeV. This is an acceptance-level number of the kind declared in §4.1.
  If m_mig ≤ 5 %, the migrated events are neglected, which lowers the signal and is conservative for a limit, and
  m_mig is quoted. If m_mig > 5 %, the generator cut of the S1 samples is lowered to 150 GeV before the freeze; the
  extra Stage-2 and Stage-3 cost is then re-projected against the stop rule of §11.6.
- *Calorimeters, muon system, lepton veto.* The chain stops at the tracker and timing layer. A quirk pair is a pair
  of heavy charged particles that reaches the calorimeters and the muon system; whether its non-helical trajectory
  would be reconstructed as a muon and vetoed, or enter a particle-flow MET differently, cannot be simulated here.
  v2 assumes that the pair is not identified as an isolated lepton and that its calorimeter deposits do not change
  the MET beyond the model's response. No public efficiency for this exists in the repo: retrieval R-13 looks for
  one; without it the assumption is limitation [L11], and the paper gives the limit as a function of an assumed
  veto survival probability (a rescaling of μ₉₅, no extra compute).
- *Tracker hit-time acceptance.* Slow pairs at high mass arrive late. Late hits in the timing layer define SR-T;
  the tracker's own readout window is not modelled in v1. The window is taken from a public Phase-2 readout
  description (R-14) and applied to the quirk hits from their Stage-3 times. The fraction of hits lost is a signal
  quantity: it is formed after the closure verdicts, and enters as a systematic at 1,000 and 1,500 GeV (and as a
  correction if it exceeds 5 %). If no window can be sourced: limitation [L12].
**Cost.** 834 CPU-h [E, script [4]]: Stage 3 10,000 events × 95.6 s = 266 (Phase 2, truth level, no efficiency
involved); chain 80,000 rows × 25.2 s = 561 (Phase 4a, after the freeze); migration sample 7. The plan's "12–30 CPU-h of string" (PLAN l.443) is not
compatible with 2,000 rows at 5 keV. **Storage.** 80,000 × 0.52 MB ≈ 42 GB. **Dependencies.** S2 (nominal shower),
freeze. **Risks.** The signal-injection chain mode is not benchmarked; the Stage-3 timing is on toy kinematics. Both
are re-timed on the first Phase-2 jobs. That re-timing is a declared checkpoint of the brief's stop rule (§11.6):
the total is re-projected with the measured costs, and if the projection exceeds the approved compute by more
than 30 % the study stops and the user is asked. Every smaller overrun is reported.

### 4.14 S2 — theory inputs (MUST, Phase 2)

**(a) NLO K-factors, computed.** FEAS_B built `loop_quirkE` (MG5's `loop_sm` plus the v1 quirk states; the quirks are
colour singlets, so the NLO QCD counterterms are those of the q q̄ γ*/Z* vertex already in `loop_sm`) and obtained
K = σ_NLO/σ_LO = 1.165 ± 0.002 at m_E = 200 GeV (CT18NLO, μ = H_T/2; NLO scale envelope +1.6/−1.1 %) [V: FEAS_B
Task 4]. v1's K = 1.110 at 200 GeV was transcribed from slepton NNLO_approx+NNLL tables and is defined differently
(D5 §2), so the two are not expected to be equal. **The model is trusted only after three validations:**
1. *Model identity.* Fixed-order LO of `loop_quirkE` against the tree-level v1 UFO at the same fixed scale and PDF:
   agreement within the integration error (|z| < 3) and 0.5 %. (FEAS_B found 0.6 % at *different* scales, which is not
   yet this test.)
2. *Published matching limit, like with like (changed in v2; finding M23).* The scalar Ẽ has the quantum numbers of
   a right-handed slepton. σ_NLO(Ẽ, N_IC = 1) from `loop_quirkE`, at the collision energy and PDF set of the
   reference, is compared at 200, 500 and 1,000 GeV with a **fixed-order NLO** number: the NLO column of the LHC SUSY
   cross-section working-group right-selectron tables if they give one, otherwise a public NLO slepton-pair code run
   at the same settings (R-1 identifies which). Criterion: within 3 % at each mass. v1 of this document compared
   NLO with NLO+NLL / NNLO_approx+NNLL tables at 10 %: a comparison of unlike quantities that was both too loose to
   catch a model error of 5–8 % and able to fail a correct calculation at 1 TeV, where the implied K of the tables
   rises to 1.29 (`stage2_C001_quirks/research/theory_signal_model.md` l.158-163 [U]; arbiter §2). If no fixed-order
   reference can be obtained, the comparison is made against the resummed tables with the tables' own NLL/NLO ratio
   removed where the source gives it, and otherwise validation 2 is reported as NOT EVALUABLE (the computed K is
   then used on the strength of validations 1 and 3, and this is stated).
3. *Process independence, differential.* The QCD correction acts on the initial state only, so at equal invariant
   mass the K-factor of a colour-singlet pair does not depend on the final state. K(M) for `p p > e+ e-` at NLO is
   compared with K_E(M) in bins of the pair invariant mass; criterion: agreement within 2 % or within 3σ of the
   integration error in each bin, whichever is larger (v1 of this document: 5 % on an integrated window). K_E/K_Ẽ
   is reported as the test of v1's "spin-independent" assumption.
**[SD11]** (default; the user decides in GA-5) σ_norm = N_IC × σ_NLO(MG5), with the 7-point scale envelope and the
PDF uncertainty computed for each mass. *PDF set:* the K scan is run with CT18NLO (the set of the feasibility run)
and with PDF4LHC21 (the usual recommendation for BSM cross sections, review P-C4; the set must be installed, one
install slot); the nominal is PDF4LHC21 if it installs, with CT18NLO as the variant, otherwise CT18NLO with this
stated. *Method parity (03-phases l.207-218 names "NLO+NLL vs NLO" as a parity case).* The published slepton
numbers contain soft-gluon resummation; v2's nominal is fixed order because the plan's S2 asks for a computed, not
a transcribed, normalisation, and no resummation code is part of the chain. The resummed normalisation,
σ_NLO × (NLO+NLL)/NLO with the ratio from the public tables, is **implemented as the cross-check**: every limit and
the reach are also quoted with it. If validation 1 or 3 fails, or validation 2 fails against a fixed-order
reference, the fallback is the v1 transcription, labelled as such, and the criterion "computed K" is reported as
failed.
**(a′) Infracolour Coulomb correction (COM S2-f; finding M28).** The pair is produced in an infracolour singlet and
feels the attractive infracolour Coulomb potential at production; the QCD K-factor does not contain this. Form used
for the estimate (from review P-B5 and the arbiter's re-derivation; to be replaced by a cited treatment, R-12):
one-loop coupling of pure SU(2), α_IC(μ) = 2π/(b₀ ln(μ/Λ)) with b₀ = 22/3, and the O(α_IC) correction
δ(β) = C_F α_IC (π/(2β) − 4/π) with C_F = 3/4. Substitution: α_IC(200 GeV, Λ = 1 keV) = 0.045; δ = +3.3 %, +6.3 %,
+13.3 % at β = 0.7, 0.5, 0.3; the dependence on Λ and mass over the grid is weak (0.043–0.045) [V: script [13]].
Limiting case: α_IC → 0 gives δ = 0. This is comparable to or larger than the NLO scale envelope (+1.6/−1.1 %). It
is **computed per mass in Phase 2** by averaging δ(β) over the generated β distribution of each sample (no extra
CPU). Default: σ_norm is **not** raised; the correction is drawn as a one-sided upward band on the theory line and
quoted per mass, because the identification of the string scale Λ with the scale of the running coupling is itself
uncertain and no treatment in the quirk literature has been retrieved yet. Not applying a positive correction is
conservative for the mass reach. The alternative (apply it) is in GA-5.
**(b) f₂₀₀, one definition.** f₂₀₀ = σ(pT(QQ̄) > 200 GeV after the shower) / σ(matched, inclusive), **with no η cut**.
The |η_pair| < 4 clause printed in v0.4 is not applied by the normalisation script (D3 §1 item 1); the fiducial
factor (|η_pair| < 2.5) belongs to A. One script computes f₂₀₀ for the five species-masses from the new samples; v1
values 0.04764, 0.10418, 0.14585, 0.16876 (E) and 0.1135 (Ẽ 500) are the comparison (D5 §2 [U] `TT/sim/results/xsec.json`).
Its uncertainty is rebuilt from: scale weights in the LHE files; PDF members; the merging scale (qCut 30 and 60
against 45: re-showers); the tune (Monash against CP5); and the comparison with one NLO-merged (FxFx, 0–1 jet)
sample at 500 GeV and one at 1,500 GeV, the mass that sets the reach (review P-C5). v1's estimate was
+12…+15 % / −11…−13 % (D5 §2 [U]). If the FxFx value lies outside the band, the
band is enlarged to contain it. The result is one asymmetric log-normal nuisance on the signal yield in T1.
**(c) QED final-state radiation.** v1 dropped it and carried −1.1 ± 0.8 % on ℓ_max (D5 §2 [U]). **[SD12]** v2 showers
the nominal signal with the QED-FSR card (same LHE; 21.1 against 21.2 ms per event [V: FEAS_B Task 3]); the FSR-off
sample is kept for C1 and for quoting the shift. This is a physics completion decided before any v2 efficiency.
**(d) Trigger turn-on (referee Q16).** v1 used ε = 0.98 · ½[1 + erf((MET − 200)/(20√2))] with estimated parameters and
no propagation (D5 §4 [U] `products.py` l.43-45). Substitution: at the offline threshold of 250 GeV the function gives
0.98 × ½[1 + erf(1.77)] = 0.98 × 0.994 = 0.974 [E: erf(1.77) = 0.988]. v2 takes the turn-on from a public Phase-2
Level-1 / high-level-trigger MET curve (retrieval task R-2; none is in the repo) and defines the nuisance as the
envelope between the nominal curve and the curve shifted by the uncertainty read from the source. If the public
curve reaches its plateau above 250 GeV, the offline threshold is raised before the freeze; that is a trigger-physics
reason, not a signal-efficiency reason. The decision is taken and logged before the acceptance A is computed on the
v2 samples (§4.1).
**Acceptance criteria (identifiers of COM).** (S2-a) validations 1–3 recorded with numbers; (S2-b) K(m) with scale and
PDF errors for all masses of the reach curve, and the resummed cross-check normalisation beside it; (S2-c) one f₂₀₀
definition in code and text, uncertainty propagated into T1; (S2-d) QED-FSR sample is the nominal; (S2-e) the
turn-on comes from a cited public figure with page, or the item is reported as "parametrised, not sourced" with the
v1 function and a nuisance equal to the full difference between plateau and the 50 % point shifted by one width;
(S2-f) the infracolour correction per mass, with its source or the label "not sourced".
**Cost.** 88 CPU-h [E, script [4]]: Stage 2 1.25×10⁶ × 50 ms = 17; K scans with two PDF sets 1.3; FxFx at two masses
40; four re-showers 4 × 1.25×10⁶ × 21 ms = 29.
**Risks.** MLM cost not benchmarked; FxFx event generation not yet run (StdHEP did not compile, FEAS_B Task 4);
MG5 writes into its install directory → jobs use a per-node local copy (FEAS_B open issue 1).

### 4.15 P1 — thickness-law clean-ups (MUST, Phase 2)

P1 is not needed by the search (scattering dominates above 1.2–1.9 keV, D5 §7.13). It decides what the paper may say.
| sub-item | status and what must be written | pre-declared reading |
|---|---|---|
| Floor test 1: extended precision | no code exists (D5 §1.8; grep confirmed there). A step map in ≥ 30-digit arithmetic for the 3–5 events with the smallest ε⊥ at B₀/20, detector scaled by 1/27, at B₀ and B₀/20 | v1's prediction (`TT/analytic/NEAR_MISS_IMPULSE.md` l.731-738 [U]): if the excess is the double-precision floor, Δc(20) falls from +0.01–0.02 to ≲ 0.001. Reading: "floor" if \|Δc\| ≤ 0.003 in every event; "physical" if ≥ 0.007 in every event; otherwise "inconclusive". All three are reportable outcomes |
| Floor test 2: reduced precision | a change of the Minkowski product `mdot` in `nm_kernel.py` to truncate the mantissa to 44 bits | if floor: the same Δc distribution reappears at 8× larger ε⊥ with the ε⊥⁻² shape; reading by a two-sample test at p > 0.05 |
| B*-off | **already run twice** (Stage-1 at 3 keV; Stage-3 at 5 keV on 171 events: unpaired 5.5σ, paired only 2.1σ, D5 §1.8 [U]). What remains: a paired test with power. N = 171 × (5/2.1)² ≈ 970 events at 5 keV for 5σ if the effect is as measured [E, script]; plus the same test at 1 keV on new gate events | "B* attribution supported" if the paired median of (on − off) is positive at ≥ 3σ overall and for k_B ≥ 6; at 1 keV the paired difference must be compatible with zero (≤ 2σ), which shows the +2 % gate excess is not B* |
| Population estimator for c | defined now: the **paired median of (c₂ − c_ev)** over events, with a paired bootstrap (2,000); criterion \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at all five points at 1 keV | v1 already knows this estimator on the old gate events (within ± 0.001, D5 §1.5). It is therefore evaluated on **300 new events per point** with new seeds. The original gate (difference of medians, +0.7 to +3.2 %) stays reported as failed |
| Validity window | from the tracked `TT/sim/stage3/results/P1.json`: a table per (point, Λ, k_B bin) | text follows the table: 9 of 30 cells pass; +6.5 ± 1.3 % in the k_B 2–4 bin at 5 keV; the straight-string ratio 0.50 predicted against 0.75 ± 0.08 stays visible as failed (D3 §1, D5 §1.6) |
| Linux difference | one conformal run gives 2 crossings instead of 6 on Linux (FEAS_A §3.2) | the Stage-1 analysis is rerun; if a quoted P1 number moves, it is corrected and listed in the errata |
**Criterion for the item.** All five rows executed and reported with their pre-declared reading, whatever the
outcome; the paper's P1 claims are limited to what the table supports ("in the median over events", not "per event
on 2.2×10⁵ events", D3 §6.5). **Cost.** 51 CPU-h [E, script [3]]: the paired B*-off test is 970 events × 2 (on, off) ×
67.8 s = 36.5 CPU-h at the Stage-3 cost measured on maxwell at 5 keV; floor tests 4; the 1 keV tests 0.5; margin 10.
v1 of this document had 30, from an M3 time converted with an assumed ratio, which brief §5.4 forbids. The record is
also inconsistent: v1 quotes 0.84 M3 CPU-h for the 171-event test, while 171 × 2 × 32.3 s (v1's own Stage-3 time at
5 keV, `STAGE3_INDEX.json`) is 3.1 h (review K-B2). **Which configuration the v1 test ran (event subset, step
size, B* switch in the kernel or in the analysis) is resolved from the v1 code before the test is launched**, and
the cost is re-projected then. **Risk.** The extended-precision map is 1–2 person-days of new code (D5 §1.8 [U]); if it is
not finished, [DT3] floor test 2 alone is reported and floor test 1 is listed as not done.

### 4.16 S3, S4, S5

**S3 (dropped, brief D1).** The paper stays barrel-only and states the endcap gain as an outlook, tagged EST, from plan
S3: signal ×1.5–3.2; reach 866 → 1062 GeV at B = 10, g = 1. That statement answers referee question 11. The endcap row
of the reach table does not appear as a result. (Provenance note for the paper: ×3.2 = 1/0.31 at g = 1 is in the
book, ch29 l.106-110; the lower end 1.5 has no derivation in the book or the plan, D3 §5; see GA-10 in §12.1.)
**S4 (COULD) — recommendation: not included [DP4].** A merging-tolerant rung and a lower seed opening-angle cut change
the finder or add a selection, so every background estimator would have to be closed again for it: about one more
week of development (PLAN l.382; book ch28 l.256 [U]) and a rerun of the finder on all background samples: the trial
part of B2, B1 and B4 is ≈ 700 CPU-h [E, script [6]: trials are 78 % of a four-road event and 46 % of a one-road row].
It would also delay the freeze.
**S5 (COULD) — recommendation: not included [DP4].** A pile-up-robust separation estimator is method R&D with no bound
on its duration; the paper states the negative result (sep_IT flat at 18–26 mm at pile-up 200; M_est a proxy), as
PLAN l.384-385 allows. Estimated cost if requested: about a week and ≈ 50 CPU-h [E].

### 4.17 Sample inventory (COM INV-1; finding M35)

One row per sample. "Role" is fixed here: a **development** sample may be looked at freely before the freeze and is
never used for a verdict; a **derivation** sample supplies corrections or parameters after the freeze; a **test**
sample gives closure verdicts; a **production** sample supplies the numbers of the result; **reserve** is produced
only under the failure protocol of §8. Seed streams are disjoint by construction: the job seed is
blake2b("qv2|stream|chunk") with the stream name of the table (v1's seed scheme, D4 §5.1 [U]), and every stream name
is unique. CPU-h and events are those of the script [3]; storage totals are in §11.4. Generators: pile-up and SM
with Pythia 8.312 (v1 `PY_MB` + CP5 for minimum bias), signal with MG5_aMC 2.9.22 (LO, MLM 0–2 jets) + Pythia 8.313,
Geant4 11.4.3 FTFP_BERT, ACTS/Fatras 48 (D1 §2; FEAS_A, FEAS_B).

| # | sample | size | seed stream | role | must be independent of | phase | CPU-h |
|---|---|---|---|---|---|---|---|
| 1 | pile-up ρ = 1 | 4,000 events (16,000 trials) | `c1.pu1` | C1 comparison; then development (occupancy inputs, timing-layer hit density, s_model) | 14 | 2 | 67 |
| 2 | pile-up ρ = 2, pre-merge store on | 1,000 events | `c1.pu2` | C1; then development (thinning N_eff, B2-g) | 15 | 2 | 57 |
| 3 | no-pile-up C′₀, v1 sizes | 5.4×10⁵ | `c1.c0` | C1 | — | 2 | 1.7 |
| 4 | C′_PU topologies | 5,000 events | `c1.cpu` | C1; development (attribution rules compared) | 19 | 2 | 35 |
| 5 | Z(νν)+jets hit level | 2,000 events | `c1.sm` | C1; development (B4, B5 prototypes) | 20 | 2 | 14 |
| 6 | signal at the three C1 points, v1 path, and full-chain twins | 3 × 400 rows + 800 | `c1.sig` | C1 only (tiers of §4.1); never part of S1 | 22 | 2 | 14 |
| 7 | Stage 2 signal, five species-masses, with four re-showers | 5 × 250,000 LHE | `s2.nom`, `s2.var.*` | production (S1 input; f₂₀₀, A and their uncertainties) | — | 2 | 47 |
| 8 | migration sample (generator cut 150 GeV) | 5 × 100,000 LHE | `s2.mig` | S1-f measurement | — | 2 | 7 |
| 9 | FxFx 0–1 jet at 500 and 1,500 GeV | 2 points | `s2.fxfx` | S2-c uncertainty | — | 2 | 40 |
| 10 | Stage 3 truth propagation, 40 points | 2,000 rows per point | `s3.sig` | production input of S1 (truth level; halves assigned by the hash at the freeze) | 6 | 2–3 | 266 |
| 11 | enrichment pilot: generator-level minimum bias; unbiased no-pile-up; near-pass overlays | 10⁷; 4 × 10⁶; 1,000 | `pilot.*` | development (gain G, f_k, check of the analytic bound) | 17, 19 | 2 | 27 |
| 12 | enlarged development closure sample, ρ = 1 | ≈ 5,960 events | `dev.pu1` | development (decision point 2, s_model) | 14 | 3 | 100 |
| 13 | pile-up events with Geant4 secondaries | 1,000 events | `dev.g4pu` | development (B1-g test) | — | 3 | 17.5 |
| 14 | pile-up ρ = 1 direct | 24,000 events (96,000 trials) | `prod.pu1` | **test** for B2-a, B2-b, B3-c; production (direct counts R04–R07) | 1, 12 | 4a | 403 |
| 15 | pile-up ρ = 2 with pre-merge candidates | 3,000 events | `prod.pu2` | production (thinning estimator) | 2, 14 | 4a | 172 |
| 16 | second direct sample | 24,000 events | `reserve.pu1` | reserve (INVESTIGATE or bug re-test only) | 1, 12, 14 | 4a | (403) |
| 17 | no-pile-up single-interaction pool, eight topologies (Table 4.4a) | 1.20×10⁸ | `prod.c0.<topology>` | production (P_geo, f_k, H); conditionals of B3 with derivation and test halves by seed parity | 11 | 4a | 383 |
| 18 | no-pile-up SM hard-scatter pool, twelve processes | 1.74×10⁷ | `prod.hs0.<process>` | production (P_geo, f_k, H); B5 T(Δφ); B4-e flatness test | — | 4a | 217 |
| 19 | B1 overlays: derivation (passers, near-pass) and held-out test (enriched, unbiased) | 4 × (2,000 + 2,000 + 4,000 + 1,000) + 4 × 1,500 | `prod.ovd.<t>` (derivation), `prod.ovt.<t>` (test) | derivation at R04–R05; **test** at R06–R07 | each other; 4, 11, 17 (different no-pile-up events), 14 (different pile-up events) | 4a | 294 |
| 20 | SM hit level, fifteen samples | 38,000 events | `prod.smhit.<process>` | derivation half and **test** half by seed parity (B4-c); B5 with pile-up | 5 | 4a | 266 |
| 21 | multijets: generator level, biased; loose population through the no-pile-up chain | 10⁷; 10⁶ | `prod.mj.*` | production (N_trig of the addition; B4-e) | — | 4a | 77 |
| 22 | signal, full chain, 40 points | 2 × 1,000 rows per point | `prod.sig.opt`, `prod.sig.eval` (two campaigns, two directories) | production; blind until 4b / 4c | 6 | 4a | 561 |
| 23 | Geant4 vertices; QGSP_BERT and composition variations | one vertex per event of 17; 2 × 5×10⁶ no-pile-up events | `prod.g4`, `prod.c0.var.*` | production input; SY-5 | — | 4a | 132 |
| 24 | B6 samples: nominal partners and varied, background and signal (paired) | reduced: 8 × 600 events, 4 × 300 × 7 rows, 4 × 2.5×10⁶ no-pile-up | `prod.b6.*` | robustness and nuisances; signal part read after the verdicts | 22 | 4a | 226 |

Samples 17–24 and 14–15 do not exist before the pre-registration is hashed (brief D7). Samples 1–13 exist before it;
none of them enters a verdict or a quoted number, except 7 and 10, which are generator-level and truth-level inputs
whose content does not depend on any analysis choice.

---

## 5. Systematic plan and the conventions enumeration (binding at Phase 4a)

`conventions/search.md` was read in full. Its tables are written for e⁺e⁻ searches and say that pp searches replace
the beam rows by PDF and pile-up and add luminosity. Each row is answered below; "WI" = will implement.

### 5.1 Required systematic sources

| conventions row | answer | how, where |
|---|---|---|
| Signal cross-section theory (scales, higher orders) | WI | 7-point scale envelope and CT18NLO eigenvectors on σ_NLO(m) (S2, Phase 2); drawn as a band on the theory line, not profiled |
| Signal acceptance (generator comparison, ISR variations) | WI | f₂₀₀ and A from MLM against FxFx at 500 GeV, scale weights, qCut 30/60, CP5 against Monash (S2); profiled in T1 |
| Signal shape | WI, translated | no fitted shape: two counting categories. The "shape" is the SR-T/SR-G migration: timing resolution of the barrel timing layer varied within the public value (R-7), Phase 4a |
| ISR modelling | WI | this is the pT(QQ̄) > 200 GeV tail: the f₂₀₀ nuisance above. One nuisance, not counted twice with the acceptance row |
| 4-fermion backgrounds (generator comparison) | WI, translated | the pp analogue is the irreducible MET + jets background: Z(νν), W, top, dibosons. Pythia 2→2 against MG5 for the leading Z(νν)+jet and W+jet rates (measured ratio 0.84 for Z(νν)+jet, FEAS_B); cited K-factors (B4). For tt̄ and the dibosons no second generator is run: their nuisance is the uncertainty of the cited calculation (stated limitation of this row) |
| Background normalisation | WI | per process group: generator difference ⊕ K uncertainty from the cited source; single-interaction rates: Geant4 against v1 generator, material band (B1); Phase 4a |
| Background shape | Not applicable as written: there is no discriminant distribution; each selection is a counting experiment. Its role (extrapolation of the background along the cuts) is taken by the closure nuisances of B1–B3 with the extrapolation width that is always added (§4.0 point 7; COM B1-b, B2-f, B3-d), which are implemented | |
| qq̄(γ) modelling (2-fermion generator comparison) | WI, translated | soft-QCD modelling of pile-up: alternative tune at fixed top-up density (B6); hadron species fractions Pythia (string) against Herwig (cluster) at generator level, after an install attempt in Phase 2; if the attempt fails, against published minimum-bias data, with the failure documented [DP5] |
| MC statistics | WI | Poisson auxiliary channel per simulated count, with the Gamma(m + 1) generation convention for expected limits (T1, [SD7], §4.11); one channel per weight class; bootstrap errors for estimator outputs |
| Detector simulation model (data/MC) | Not applicable as written: there is no data. Translated and WI: Fatras against Geant4 for hadronic physics (B1); resolution, inefficiency and material nuisances sized from public Phase-2 numbers (R-15 to R-17) and evaluated on every term (B6-c, B6-d), the round-number variations being robustness tests only; top-up and tune variations (B6); physics list variation FTFP_BERT against QGSP_BERT (B1) | |
| Object calibration | WI | MET response and resolution (the B4 model parameters); trigger turn-on (S2); primary-vertex identification efficiency, set to 1 in v1 although v0.4 quotes 93 % (D3 §1 item 2) → a factor and nuisance from a public source (R-8) or, if none is found, the limitation is stated with ε_PV = 1; timing resolution and its tails (R-7, B3-c); tracker hit-time window (R-14, S1-f). The MET model applies to signal and background alike (S1-f). dE/dx scale: not applicable, dE/dx is not used [SD9] |
| Beam energy | Not applicable: pp at a fixed nominal 14 TeV; all cross sections are computed at 14 TeV. Replaced by the PDF and pile-up rows as the conventions instruct | |
| Luminosity | WI | the result is a projection at 3 ab⁻¹; the luminosity nuisance for HL-LHC comes from a public target (R-9) and applies to signal and to every background normalised to L; limits are also shown at 300 fb⁻¹ |
| PDF (pp replacement) | WI | CT18NLO eigenvectors on σ, f₂₀₀ and A (weights in the LHE files) |
| Pile-up (pp replacement) | WI at fixed ⟨μ⟩ = 200 | density (top-up limits), tune, timing spread. No scan in μ (brief D8) [A5] |
| QCD scale variations | WI | signal as above; SM backgrounds through the K uncertainty |
| Fragmentation model | WI at generator level | tune variation everywhere; string against cluster hadronisation at generator level after the Phase-2 install attempt [DP5]. It matters through the K/π ratio, which sets the decay-in-flight rate: the nuisance on rate_DIF is the relative difference of the charged-kaon and pion yields in the relevant p_T range, weighted by their decay probabilities |
| Heavy-flavour treatment | Not applicable as written (no b-tagging). Displaced b/c decay vertices are a topology: Phase 2 checks whether v1's eight topologies contain them (Pythia decays with τ₀ < 1000 mm are in the particle list, D5 §4); if they are a separate class they are added to B1 | |

Study-specific sources (all WI): thinning and occupancy closure (B2); closure of the single-interaction estimator,
promotion model and bias weights (B1);
conditionals (B3); Geant4 material composition and physics list (B1); the MET model tail (B4); f₂₀₀ (S2); QED FSR
(nominal on, shift quoted); trigger (S2); status-4 Stage-3 events dropped (≤ 1.5 %, one-sided, D5 §3 [U]); the
frozen admissibility transcription [A3]; signal Monte Carlo statistics; finder seed-threshold convergence (C2).
Every nuisance is sized by a measurement, a closure result or a cited public number; a variation with a round-number
size is a robustness test and not a nuisance (§4.9; JFC Phase 4a). Additional study-specific sources in v2: the
infracolour Coulomb correction (band on the theory line, S2-f); signal migration across the generator cut and the
lepton-veto assumption (S1-f); pile-up-vertex secondaries (B1-g). No single nuisance may exceed 80 % of the total without investigation (regression trigger).

### 5.2 Required validation checks

| conventions check | answer |
|---|---|
| 1. Closure tests in validation regions, p > 0.05 | WI, translated: the "validation regions" are the loose rungs R04–R07 where direct simulation counts exist; the "signal region" is the chosen deep selection. Criteria in §4.0 (derivation and test on disjoint rungs and samples; four verdict classes; family-wise rule), B1-a, B2-a, B2-b, B3-a…d, B4-c, B5-a. The conventions' pitfall "blind spot in VR coverage" applies in full: the loose rungs are not between a control region and the signal region. Answers: an extrapolation width that grows with the distance from the last tested rung and is always in the likelihood (§4.0 point 7); P_geo and the ceiling H measured directly at the deep rungs (B1); two pile-up estimators compared at depth where both are evaluable (B2-c), which is expected at few rungs [L6]. The pitfall "transfer-factor instability" is answered by the reported slopes b̂ per estimator |
| 2. Signal injection at 0, 1, 2, 5 × | WI (T1-d), Phase 4a: multiples of the expected limit of each tested point, 200 fluctuated pseudo-experiments per level, bias threshold 20 % of the injected μ; v1 placeholder efficiencies |
| 3. Nuisance pulls and constraints | WI (T1-e): pulls on fluctuated pseudo-data, constraints on Asimov data. There is no observed fit |
| 4. Impact ranking | WI (T1-e) |
| 5. Goodness of fit | Not applicable to data (none). The estimator closure χ² values and p-values are reported in its place, with JFC's alarm bands (χ²/ndf < 0.1 or > 3) |
| 6. Look-elsewhere effect | Not applicable: no observed excess can occur; hypotheses are a fixed grid. The multiple-comparison correction of C1 (Bonferroni over 41) is the only trials factor |
| Standard configuration: CLs, q̃_μ, toys below ≈ 5 expected events | WI (T1) |

---

## 6. Reference analyses and comparison targets

Sources: the repo only. `AUD` = `TT/paper/P2_NOVELTY_AUDIT.md` (which read the arXiv PDFs and gives pages),
`EXT` = `TT/stage5/EXTERNAL_BOUNDS.md`, `EXP` = `stage2_C001_quirks/research/experimental_status_2026.md`. I read these
files this session; I did not open the papers, so every entry is **[U] for the paper content, [V] for "the repo file
says so"** at the line given. Look-ups are logged in `QV2/retrieval_log.md`.

### 6.1 Methods and systematic programmes

| | R1 Knapen, Lou, Papucci, Setford, arXiv:1708.02243 | R2 Li, Li, Pei, Zhang, arXiv:1911.02223 | R3 FASER quirk search, arXiv:2607.26195 | R4 CMS disappearing tracks, arXiv:2309.16823 (method reference) |
|---|---|---|---|---|
| type | phenomenology, central tracker | phenomenology, central tracker | experiment, forward | experiment, spurious tracks from random hit alignment |
| model | (1,1)₁ fermion, N = 2 (same as E) and coloured | E-like, N_IC = 3 (N_IC = 2 in App. A) | (1,1,−1) fermion, N_IC = 2: exact match to E | — |
| detector, pile-up | simplified ATLAS barrel, 2 T, 8 layers, ⟨μ⟩ = 50 | CMS-like 13 barrel layers, helix intersections, ⟨μ⟩ = 50 | forward detector, 13.6 TeV, 186.3 fb⁻¹ | CMS, 137 fb⁻¹ |
| backgrounds | pile-up hits; beam-pipe conversions; no Z(νν)+jets | Z(νν)+jets + pile-up dominant | (not extracted in the repo) | genuine and spurious tracks, sideband control regions with transfer factors |
| background estimate | factorised: distribution from a looser (1 hit per layer) selection × efficiency of the tight one; reach "assuming negligible irreducible backgrounds" | cut flow on simulated Z+jets: 3600 → 0.12 fb | (not extracted) | data-driven transfer factors |
| statistical method | counting: contours of 3 and 5 signal events at B = 0 | 95 % CL exclusion from S and B after cuts (method details not extracted) | (not extracted) | binned likelihood (not extracted) |
| systematic programme | none quoted | none extracted | shower scale ≈ 6 %, up to 28 % at small Λ (EXP l.335); the rest not extracted | Table 7: signal selection 10–17 %, luminosity 1.6 %, jet energy 0–24 %, scales 0–2 %, ISR 0–3 %, pile-up 0–2 %, trigger 0–4 %, dE/dx 3–8 %; spurious background 5–52 % (long), 6–28 % (short) (EXP l.132) |
| source lines | AUD §1.1 | AUD §1.2 | EXT l.58; EXP l.51-56, l.335 | EXP l.127-132 |

**Method parity.** R1 and R2, the two studies closest in observable, use event counting at zero or small simulated
background and quote no systematic programme. v2 uses a profile-likelihood CLs model with constrained nuisances and
toys, which is more sophisticated; parity is met without a cross-check obligation. As a comparison in their own
terms, v2 also quotes the "3 and 5 signal events at B = 0" reach with the v2 efficiencies (Phase 4c). R4 is the
closest experimental method for the dominant instrumental background; its transfer-factor uncertainties (5–52 %)
are the scale against which the B5 sideband closure is read. The systematic coverage of §5 contains every source R4
lists that exists in a simulation-only tracker study (selection efficiency, luminosity, scales, ISR, pile-up,
trigger); jet energy scale enters only through the MET model.

### 6.2 Published numbers recorded as comparison targets

| quantity | value | source in the repo |
|---|---|---|
| R1 discovery reach, EW quirks, 300 fb⁻¹ (5 events, B = 0) | 650 GeV | AUD §1.1 "Claimed reach" (abstract, p. 1) |
| R1 efficiencies at 800 GeV: ε_trig, ε_fid, ε_reco at Λ = 1…5 keV | 0.10, 0.28, 0.11 / 0.41 / 0.65 / 0.72 / 0.74 | AUD §1.1 (Table I, p. 8) |
| R1 fraction of background events with a plane (≥ 1 hit in 4 of 8 layers; in every layer) | ∼10⁻³; 6×10⁻⁵ | AUD §1.1 (p. 7) |
| R2 background after cuts, 13 TeV | 0.12 fb (Z+jets), ≈ 12 events at 100 fb⁻¹ [E in AUD] | AUD §1.2 (Table II, p. 8) |
| R2 exclusion, 100 fb⁻¹, N_IC = 3, fermion (scalar) | 450 (150) GeV | AUD §1.2 (abstract) |
| R2 App. A, N_IC = 2, 300 fb⁻¹ | ≈ 400 GeV; R1's method redone: below 500 GeV | AUD §1.2 (p. 9-10) |
| R3 observed mass limit at Λ = 1 / 3 / 5 / 10 keV | 113 / 162.6 / 172 / 179 GeV (19 Λ values from 0.3 to 105 keV in HEPData ins3184325) | EXT l.58, l.80 |
| D0, Λ = 10 keV–1 MeV | 107 GeV | EXT l.59, l.83 |
| Farina–Low recast, E at Λ = 1 eV / 100 eV / 1 keV | 650 / 150 GeV / no limit | EXT l.60 |
| v1, this study: reach at B = 0, 3 ab⁻¹; 3-event and 5-event reach at 300 fb⁻¹ | 1026 GeV; 665 and 586 GeV [E, v1 efficiencies] | D3 §3, §5 (recomputed there from `SUM`) |
| v1 total efficiency f·A·ε at E 500 against R1 | ≈ 0.005 against ≤ 0.021 | AUD l.245, `TT/paper/sections/10_bounds.tex` l.22-23 [V] |

The three reach numbers for 300 fb⁻¹ in the plan, the audit and the paper differ (665/586, 630–665/560–590,
"≈ 0.6 TeV"; D2 §8.8). v2 quotes one number per definition, computed with pyhf; curves at 300 fb⁻¹ are labelled
"pile-up-200 detector, luminosity scaled". The factor of about 4 between v1's total efficiency and R1's (last row)
is explained in the paper by a like-for-like breakdown into ε_trig, ε_fid and ε_reco against R1's Table I, with v2
numbers (review P-C6). R2's 0.12 fb is used as a sanity comparison for the Z(νν)+jets term (§4.7).

### 6.3 Corpus queries
The phase template asks for queries to an experiment corpus; none exists here (deviation V8). The equivalent
look-ups in the repo's literature cache are logged in `retrieval_log.md` (seven entries from v1 of this document, one
added for v2).

### 6.4 Retrieval tasks for Phase 2 (numbers not in the repo; nothing is quoted from memory)

| id | needed | for |
|---|---|---|
| R-1 | right-selectron cross-section tables at NLO(+NLL) with their PDF set | S2 validation 2 |
| R-2 | public Phase-2 Level-1 / HLT MET turn-on curve with its uncertainty | S2 (d) |
| R-3 | public Phase-2 jet response and resolution, lepton acceptance, pile-up MET resolution | B4 MET model |
| R-4 | multijet fraction after a MET + jet selection in a published monojet-type analysis | B4 validation (c) |
| R-5 | cited K-factors for V+jets, tt̄, single top, dibosons at 14 TeV | B4-d |
| R-6 | cosmic-muon flux at detector depth, beam-halo rate | B7 |
| R-7 | barrel timing-layer resolution and its degradation | timing nuisance (v1 used 35 ps, D5 §4 [U]) |
| R-8 | primary-vertex identification efficiency at ⟨μ⟩ = 200 | ε_PV |
| R-9 | HL-LHC luminosity uncertainty target | luminosity nuisance |
| R-10 | R3's statistical method and full systematic table; R2's limit-setting method | completing Table 6.1 |
| R-11 | Barbashov's solution class; Knapen et al. Sec. III.D text | C3 |
| R-12 | treatment of the infracolour Coulomb (Sommerfeld) correction to quirk pair production in the literature | S2-f |
| R-13 | reconstruction of heavy charged non-helical or slow particles as muons; lepton-veto efficiency | S1-f, [L11] |
| R-14 | Phase-2 tracker readout time window | S1-f, [L12] |
| R-15, R-16 | public Phase-2 hit resolution per layer type; hit efficiency | B6-d nuisance sizes |
| R-17 | public Phase-2 tracker material budget, its uncertainty, and composition | B6-d, B1-c, [L2] |
| R-18 | public noise occupancy and out-of-time hit occupancy of the tracker and the timing layer | B1-g, B3-c |
| R-19 | published differences of charged-kaon and pion yields between string and cluster hadronisation, or measured K/π in minimum-bias data | [DP5], SY-7 |
| R-20 | a dedicated search for ATLAS or CMS results on non-helical or quirk tracks and for HL-LHC quirk projections of 2020–2026 (review P-C8); needed before the paper states "beyond existing limits" | §6.2, paper §9 |

R-7 is extended to the collision-time spread and the non-Gaussian tail of the timing resolution; R-3 to a published
pile-up-200 MET performance figure for the external validation of §4.7. R-10 closes before Phase 4a, because the
"not extracted" cells of Table 6.1 are binding inputs of its review. A retrieval task that finds nothing leaves its
dependent item "not sourced", as stated in each section; nothing is filled from memory.

---

## 7. Label index

**Constraints.** [A1] No collision data: expected limits only; "observed" quantities and data/MC checks do not exist.
[A2] v1 cannot be reproduced event by event (lost inputs, different random streams): all comparisons are statistical.
[A3] Admissibility tables and δ₉₅ are frozen transcriptions; six hashed v1 inputs are lost. [A4] No-PU samples are
stored as summaries, not events. [A5] Pile-up is fixed at 200. [A6] Cluster: 12 worker cores (9 on weekday daytime;
10 usable off-hours while two workers carry a graphical session), 7.5 GiB per node, jobs ≤ 30 min, no cloud.
[A7] Geant4 runs on a node only if its local install matches the tracked lock; it is installed on all three workers
(commit 199e166). [A8] Public information only; material composition and many detector parameters are not public.

**Limitations.** [L1] Direct closure for single-interaction terms is evaluable at R06 for γ and V⁰ only without
enrichment; PV pairs, NI and loopers are expected NOT TESTED (Table 4.4b). [L2] Nuclear-interaction rates carry the
unknown material composition. [L3] The sideband width usable in the reach is ≈ 1.1, not 0.17. [L4] Toy cost for the
real workspace is not measured. [L5] The Stage-2 yield of in-acceptance events at E 1500 and Ẽ 500 is uncertain.
[L6] Closure regions are the loose rungs, not a region between control and signal regions; beyond R07–R09 every
extrapolated factor carries a width that grows with the distance. [L7] Barrel only. [L8] Hits are Gaussian-smeared on
cylinders, not clusters on modules; δ-rays and merged clusters are not modelled. [L9] The string is classical
Nambu–Goto without infracolour radiation; stated validity Λ ≲ 10–26 keV (D2 §8.10 [U]). [L10] Stage-3 and ρ = 2 unit
costs rest on toy inputs and on one event. [L11] The response of the calorimeters, the muon system and the lepton
veto to a quirk pair is an assumption. [L12] The tracker readout time window is applied only if a public value is
found. [L13] With zero counts in the large samples the leading terms are bounds of about 45 events in total
(Table 4.4a): the result is then sample-size limited. [L14] The gain of biased generation is not measured.

**Strategy decisions.** [SD1] grid unchanged. [SD2] approach comparison with the MVA moved to Phase 4c. [SD3] C1 signal
at 400 rows per point. [SD4] the counted pile-up object is the hit set after grouping at the target density.
[SD5] top-up variation is a density systematic. [SD6] time-tag fraction for prompt terms measured at hit level and
used only if its closure passes. [SD7] zero counts as auxiliary Poisson channels; expected limits generated with
λ ~ Gamma(m + 1). [SD8] FAIL of a leading term's estimator makes a selection ineligible; NOT TESTED earns no credit.
[SD9] no dE/dx selections; the forgone gain is measured. [SD10] string propagation only for events in the counting
acceptance. [SD11] σ_norm from computed NLO; resummed normalisation as implemented cross-check; infracolour
correction as a one-sided band. [SD12] QED FSR on in the nominal signal. [SD13] v2 single freeze content (§8).
[SD14] evaluation-half aggregation only after Gate B. [SD15] every closure test has disjoint derivation and test
rungs and samples; four verdict classes; an extrapolation width that is always added (§4.0). [SD16] one pool of
no-pile-up CPU allocated as √(N_t/c_t) (§4.4). [SD17] robustness variations and nuisances are separated (§4.9).

**Downscope proposals for Gate A.** [DP1] B5 reduced. [DP2] B6 reduced, keeping 5 keV and 1 TeV. [DP3] MVA as
cross-check only. [DP4] S4, S5 not included. [DP5] Herwig comparison at generator level, after an install attempt.
**Downscopes triggered only by a failed attempt.** [DT1] Geant4 hand-over fallback. [DT2] thinning validated to R06
only. [DT3] floor test 1 not done. [DT4] ρ = 2 pre-merge threshold raised to N_IP2 ≥ 7 if storage exceeds the cap.
[DT5] unbiased generation (G = 1) if the weights closure of B1-e fails.

**How each downscope is carried into the paper (JFC 12, step 4).** For every [DP] and every triggered [DT]: one
sentence in the method section saying what was done and at what size; one row in the systematics or limitation
table with the estimated loss; one item in Future Directions naming the full version. [DP3]: §3.2 above. [DP1],
[DP2]: §4.8, §4.9. [DP4]: the limitations state the efficiency above 3 keV left unused and the negative result on
m_Q and Λ. [DP5]: §11.5.

---

## 8. The v2 pre-registration (`PREREG_v2.md`): outline

**What is frozen when.**
| moment | frozen | by |
|---|---|---|
| Gate A (this document + `COMMITMENTS.md`) | item criteria and tolerances of §4; the verdict classes and what each earns; the zero-count convention; C1 subset and its tiers; T2 candidate list (R07 and family F fixed) and figure of merit; systematic enumeration; the answers to GA-1…GA-10 | 4-bot review, user |
| end of Phase 3 (the freeze; not a human gate, brief D7) | `PREREG_v2.md`, hashed and committed **before any v2 production sample exists**; user notified | 4-bot review |
| Gate B | closure verdicts shown first, then selection and expected sensitivity from the optimisation half | user |

**Content of `PREREG_v2.md`** [SD13]. (1) The v1 record by hash (below). (2) For each estimator of B1–B4 and each
conditional of B3: definition, code hash, the single factorisation route, the **number** s_model fixed from the
development samples, the derivation rungs and samples, the test rungs and samples, the closure statistic and
tolerance of §4.0 (these may be made stricter, never looser, than at Gate A), the expected count and σ_tot per test
rung with the false-fail probability at r = 1 and the power at r = F^1.5, the number K of the eligibility family,
the sizes and seed streams (§4.17), and the consequence of each verdict. (3) B5 and B6 test definitions; the
sourced sizes of the detector nuisances. (4) The MET model with its sourced parameters and the tolerance of its
external validation. (5) The T1 workspace schema and nuisance list; the generation convention for zero counts; the
weight classes; toys as primary. (6) T2: the list (possibly shortened with reasons; R07 and family F untouched), the
figure of merit, the efficiency estimator, the split salt, the eligibility rule, the baseline, the table of
extrapolation distances. (7) The BDT cross-check recipe and the dE/dx forgone-gain ratio. (8) The declared
pre-verdict signal quantities (§4.1: the C1 tiers as approved in GA-1; A, f₂₀₀ and the migration fraction).
(9) The analysis-code freeze: sha256 of every analysis module, taken **before** production. (10) Failure handling
(below). (11) A change log from v1 to v2, each change with its reason; none is a signal efficiency.

**Failure protocol after the freeze (COM FP-1; finding M34).** JFC lists a closure failure as a regression trigger
with at least three documented remediation attempts; this document says "reported as failed, not patched". The two
are combined as follows.
1. *Always:* a failed criterion (FAIL or INVESTIGATE) opens a regression ticket, and an investigator looks for a
   cause in the code, the samples and the configuration. Up to three documented attempts to find one.
2. *If a bug is found:* it is fixed under a dated addendum to the pre-registration that states the bug and the
   fix (a background-method reason; never a tolerance, an s_model or a sample choice). The corrected estimator is
   re-tested **once, on a fresh sample that was not used for the diagnosis**: the reserved second direct sample
   for the pile-up tests (403 CPU-h, sample 16 of §4.17), or freshly generated test overlays for B1 and B4 (their
   cost, up to 294 CPU-h, is taken from the contingency and re-projected against the stop rule). The verdict of
   the fresh test is final. The first result stays in the record and in the paper.
3. *If no bug is found:* the criterion is reported as failed and [SD8] applies. No scale factor, no change of
   tolerance, no new estimator after the freeze.
An INVESTIGATE case (§4.0 point 5) follows the same steps, with the re-test on the fresh sample also when no bug is
found. Only one fresh pile-up sample is reserved: a second request goes to the user.

**Correction to PLAN l.408** ("rows 1 to 4 of the book's ranking go into one freeze"). The book's rows are: 1 a data
anchor, 2 counting as the estimator, 3 signal yield, 4 m_Q and Λ at pile-up 200 (D3 §6.1). Row 1 cannot exist in a
simulation-only study (B5 is its simulated stand-in) and row 4 is S5. The single v2 freeze holds: the estimators
(B1–B4), the conditionals including the time-tag credit, the sideband and robustness tests, the likelihood, the
selection rule and the signal split.

**v1 kept by hash** (verified by D4 §1.6 on 2026-11-13 with `sha256sum`; [U] by me).
- `analysis_freeze.json` (sha256 b42aef4d…): 32 of 32 listed files match.
- `frozen_inputs.json` (21 files): 13 match; 2 differ as documented in `HASH_ADDENDUM.md`; **6 are lost** with the bulk
  data. `WP_RULE.md` 1b2ea9bd… matches; its header still reads "not yet frozen" by design, and the operative T_seed is
  4, not the 6 of its text; the governing record is WP_RULE + HASH_ADDENDUM + the PC-19 amendment.
- The five `C12FC_v1` output files match the hashes in `STAGE4_SUMMARY.json`. Three helper scripts differ from the
  hashes recorded "at writing"; they are not production code.
The v2 appendix prints these hashes and the list of lost files.

**How the paper states the v1 freeze timing.** PLAN l.186 says "frozen before any signal efficiency". That holds for
the rule, the ladder and the fallback (2026-10-13). The analysis code was frozen again on 2026-10-16, after a first
complete run had produced signal efficiencies and limits; the fixes between the two runs lowered the fallback
background bounds (FB0/FB1 by ×4–8 in SR-G and ×50 in SR-T) and moved the best ratio from 1.1×10³ to 790, and a
normalisation fix (the f₂₀₀ factor; 37.6 → 790) followed the result review [V: `S4/STAGE4_RESULTS.md` l.115-117 and
§11.2; D4 I5]. The appendix says exactly this. v2 freezes rule **and** analysis code before production.

---

## 9. Flagship figures and methodology diagrams

| # | figure (PLAN §3.3) | data source | produced |
|---|---|---|---|
| 1 | event display of a quirk ribbon at pile-up 200, "best of its sample" | S1 evaluation half + pile-up, a point inside the window; choosing it uses passing signal events | Phase 4c (after Gate B), final in 5 |
| 2 | thickness law with scattering floor and crossover | tracked `TT/sim/stage3/results/P1.json` + P1 floor and B*-off points | Phase 2, final in 5 |
| 3 | efficiency map on the (m_Q, Λ) grid with the Λ window | S1 evaluation half at the chosen selection | Phase 4c |
| 4 | background ladder: v1 bounds and v2 estimates with bands, against the budget | `AN1/bsum_wp.json` (v1 layer) + B1–B4, T1 | Phase 4a |
| 5 | closure plots for every estimator at R04–R07 | B1, B2 (two estimators), B3, B4, B5 against direct counts | Phase 4a (development versions in Phase 3) |
| 6 | expected limit against mass with existing bounds | T1 toys; `TT/stage5/external_bounds.json` (FASER, D0, Farina–Low) | Phase 4b (optimisation half, for Gate B), 4c final |
| 7 | reach against an assumed background, v2 estimate marked | the book's method (`book/checks/ch29_checks.py` l.25-79, vendored into QV2) redone in pyhf; signal at the **chosen** selection, background as the *median* with its width | placeholder version with v1 efficiencies in 4a, final in 4c |

For Fig. 7 the v2 point lies on the curve only if the signal yield is recomputed at the v2 selection (D3 §6.6); the
Phase-4a version is therefore labelled "v1 efficiencies (placeholder)". The marked background is B₅₀ with the band
B₁₆–B₈₄ of §4.11, and each term of Fig. 4 is drawn as "estimate", "bound" or "no credit" in the sense defined there.
Fig. 5 shows derivation rungs and test rungs with different markers. All figures carry "Private work (simulation)".

**Supporting figures (analysis note and paper appendix; review N-C-5).**

| figure | source | answers referee question |
|---|---|---|
| C1 pull summary over the 41 comparisons (sealed quantities as PASS/FAIL marks until Gate B) | C1 | 24 |
| C2 distribution of Δn between the finder and the brute-force optimum | C2-a | 9 |
| B5 transfer factor T(Δφ) per process, hard-scatter component | B5-b | 23 (carries paper §8) |
| T1 pulls, constraints and impact ranking; coverage and injection results | T1-d…T1-h | 13 |
| T1 one-bin zero-count table as a figure: limit against κ for the three conventions | T1-c | 1 |
| B6 shift per variation, background and signal, with the sourced nuisance sizes | B6 | 7, 8 |
| S2 K(M) with scale and PDF bands; f₂₀₀ band; infracolour band | S2 | 17, 18 |
| MET-model external validation | B4-b | 5 |
| BDT ratio ε_BDT/ε_R07 and dE/dx forgone-gain ratio | MVA-1 | 14, 9 |
| floor table as a figure: floor per term against simulated events | TG-1 | 1 |

**Diagrams (figure-scrolling test).** (a) the chain: generation → string propagation → injection → Fatras/Geant4 →
digitisation → CKF → plane finder; (b) the geometry of a ribbon: plane through the vertex, road around the MET
direction, w_core and thickness; (c) the ladder as a cut-flow strip with the two categories; (d) the background
estimators: thinning with re-grouping, the occupancy model, the single-interaction estimator (pass, near-pass,
survival, promotion, ceiling H) with the Geant4 hand-over; (e) the blinding
and freeze timeline with the two signal halves and the three gates; (f) the likelihood: signal-region bins and
auxiliary channels; (g) the road-rotation sideband.

---

## 10. The 25 referee questions

| # | question (short) | item(s) | paper section |
|---|---|---|---|
| 1 | limit from zero-count bounds | B1–B4, T1-c; terms labelled estimate / bound / no credit; f₀ (§4.11) | 6, 7; v1 in App. |
| 2 | no hadronic physics in Fatras | B1 | 4, 6 |
| 3 | thinning closure failed | B2; the retroactive test of v1's thinning (§4.0 point 4) | 6 |
| 4 | factorisation untested | B1-a, B1-f, B3-d, B2-c; extrapolation width (§4.0) | 6 |
| 5 | multijets, Z(ττ), lost-lepton Z missing | B4 | 6 |
| 6 | eight proxies | B4-a | 6 |
| 7 | top-up ×2.3–7.3 | B6 | 4, 10 |
| 8 | cylinders, Gaussian smearing | B6, [L8] | 4, 10 |
| 9 | finder correct and near optimal | C2 | 5 |
| 10 | 9 events; fast path | S1 | 7 |
| 11 | why barrel only | S3 statement (brief D1) | 10 (outlook, EST) |
| 12 | rules changed after the result | §8; v1 by hash | App. pre-registration |
| 13 | summed 68 % bounds, uncorrelated categories | T1; table of v1 mode against v2 mode at the best point (T1-b) | 6, 7 |
| 14 | why 0.11 | T2 (flag only) | 5, 7 |
| 15 | cosmics, halo | B7 | 6 |
| 16 | trigger at Phase 2 | S2 (d) | 2, 5 |
| 17 | K-factors, f₂₀₀ | S2 (a), (b) | 2 |
| 18 | classical string, no infracolour radiation | [L9]; S2-f (Coulomb correction at production); text | 2, 3, 10 |
| 19 | law validity and failed gate | P1 | 3, App. derivation |
| 20 | law not testable at detector level | text; resolution stated as an estimate (C3) | 3, 10 |
| 21 | m_Q, Λ measurable? | negative result; S5 not included | 7, 10 |
| 22 | comparison with Knapen et al., Li et al. | §6; reach at B = 0 and against B | 9 |
| 23 | data-driven estimate possible? | B5 | 8 |
| 24 | reproduce or recast | C1, package (workspace, efficiency tables, container) | App. reproduction |
| 25 | CMS result? AI used? | C3 disclosure | title page, acknowledgements |

Q16 had no owner in the plan (D2 §8.3); it is S2 (d) here. The MET and vertex-identification variations of v0.4's open
issue 12 are owned by B4 (MET model) and §5.1 (object calibration).

---

## 11. Schedule — the Gate-A proposal

Rewritten in v2 (findings M19, M10, M8; every CPU-h number is printed by the script, sections [2]–[8]).

### 11.1 Capacity model
- Slots: 12 worker cores; at most 9 on weekdays 08:00–19:00 (brief §5.3). Two of the three workers carried a
  graphical session at preflight and are capped at 3 jobs (`LOG.md` 14:34), so **10 slots** are usable off-hours, not
  the 12 that v1 of this document counted. Per week: 5 × (11 h × 9 + 13 h × 10) + 2 × 24 h × 10 = **1,625 slot-hours,
  232 per day** [E, script [2]] (1,851 with 12).
- Losses inside the utilisation factor: other lab users; ρ = 2 jobs that may need a node each (§4.5: up to 400
  slot-hours); ≤ 500 steps per workflow and gaps between campaigns; failed and retried jobs; Argo overhead 17 s per
  job (about 11,000 jobs → 52 slot-hours, 1.2 %) [E, script [8]]; cold NFS starts (minutes per node and environment,
  FEAS_A §3.8).
- **Effective capacity assumed: 0.75 × 232 = 174 core-h per day in production phases with campaigns queued
  continuously; 0.50 × 232 = 116 in development phases** [E]. The unit costs already contain the slowdown of 4 jobs
  per node. **The two utilisation factors are assumptions, not measurements.** They are measured in the first week of
  Phase 2 as delivered slot-hours over available slot-hours, and the calendar is re-projected then (§11.6). At 0.50
  in production every production duration below grows by half.

### 11.2 CPU-h budget (from §4; script [3], [4])

| item | priority | Phase 2 | Phase 3 | Phase 4a | 4b / 4c / 5 | total | v1 of this document |
|---|---|---|---|---|---|---|---|
| C1 | MUST | 198 | | | | 198 | 192 |
| C2 | MUST | 81 | | | | 81 | 81 |
| P1 | MUST | 51 | | | | 51 | 30 |
| S2 | MUST | 88 | | | | 88 | 67 |
| S1 | MUST | 273 (string 266, migration 7) | | 561 (chain) | | 834 | 827 |
| B1 | MUST | 27 (pilot) | 77 | 809 | | 914 | 481 |
| B2 | MUST | 10 | 10 | 574 | | 594 | 594 |
| B3 | MUST | 5 | 10 | 25 | | 40 | 30 |
| B4 | MUST | | 50 | 561 | | 611 | 407 |
| T1 | MUST | | 60 | 40 | 145 / 174 | 420 | 224 |
| T2, BDT and dE/dx ratio | MUST | | | | 16 / 7 | 23 | 7 |
| enlarged development samples; timing jobs | MUST | 5 | 100 | | | 105 | — |
| figures, package | MUST | | | | 10 | 10 | 10 |
| **MUST total** | | **737** | **308** | **2,571** | **352** | **3,968** | 2,950 |
| B5 | SHOULD | | 20 | 530 full / 173 reduced | | 550 / 193 | 540 / 183 |
| B6 | SHOULD | | 10 | 381 full / 226 reduced | | 391 / 236 | 303 / 138 |
| B7 | SHOULD | | | 5 | | 5 | 5 |
| **Total** | | 737 | 338 | 3,488 / 2,975 | 352 | **4,915 full / 4,401 reduced** | 3,798 / 3,275 |

C3 costs no CPU. The no-pile-up pool of 600 CPU-h is split between B1 (383) and B4 (217).

**Three variants.**

| variant | CPU-h | production of Phase 4a on the critical path | calendar (§11.3) |
|---|---|---|---|
| MUST only | 3,968 | 2,010 CPU-h = 11.5 days | 55.5 days = 7.9 weeks |
| MUST + SHOULD reduced ([DP1], [DP2]) — **proposed** | 4,401 | 2,414 CPU-h = 13.9 days | 57.9 days = 8.3 weeks |
| MUST + SHOULD full | 4,915 | 2,927 CPU-h = 16.8 days | 60.8 days = 8.7 weeks |

**Where the increase over v1 comes from (per finding; days at 174 core-h per day) [E, script [5]].**

| finding | change | CPU-h | days |
|---|---|---|---|
| M6 (incl. M19) | no-pile-up pool of 600 CPU-h in place of 4×10⁷ × 11.5 ms + 1.5×10⁷ × 15 ms; of this, +125 is the hard-scatter unit cost corrected from 15 to 45 ms | +410 | +2.35 |
| M6 | enrichment pilot | +27 | +0.15 |
| M8, P-C3 | second toy pass; five selections in pass 1 | +145 | +0.83 |
| M1, M7, M8 | T1 development, coverage toys, pseudo-experiments | +51 | +0.29 |
| N-C-6 | enlarged development samples (idle pre-freeze capacity, no calendar effect) | +100 | (0) |
| K-C7 | Geant4 vertices sized to one distinct vertex per event | +60 | +0.35 |
| M19 | QGSP_BERT and composition variations | +52 | +0.30 |
| M19 | multijet generation at the measured shower cost | +37 | +0.21 |
| M3, M5 | overlays 42,000 in place of 39,000 events | +21 | +0.12 |
| M19 | P1 at the measured Stage-3 cost | +21 | +0.12 |
| P-C4, P-C5 | second PDF set, FxFx at 1,500 GeV | +21 | +0.12 |
| M26 | pile-up-vertex secondaries test | +17.5 | +0.10 |
| M29 | background-side bootstrap of T2 | +14.5 | +0.08 |
| M33 | multijet loose population | +12.5 | +0.07 |
| M16 | time-tag measurement and closure | +10 | +0.06 |
| M27, M21, M19, M30 | migration sample 7; C1 twins 5.6; timing jobs 5; dE/dx ratio 2 | +20 | +0.11 |
| **MUST** | | **+1,018** | |
| M12 (SHOULD) | detector variations on single-interaction and SM terms | +51 | +0.29 |
| M13 (SHOULD, reduced) | reduced B6 keeps 5 keV and 1 TeV | +29 | +0.17 |
| M17 (SHOULD) | B6 nominal partner samples | +18.5 reduced / +38 full | +0.11 |
| M31 (SHOULD) | hard-scatter T(Δφ) on no-pile-up samples | +10 | +0.06 |
| **reduced total** | 3,275 → 4,401 | **+1,126** | |

Not in the totals, conditional: Geant4 secondaries in every pile-up overlay if the B1-g test requires it (+160);
S1 generator cut at 150 GeV if the migration exceeds 5 % (to be costed in Phase 2); the second direct sample (403);
re-generated test overlays after a bug (up to 294); S1 at 4,000 rows (GA-2, +827).

**Unit costs that were never measured, and the contingency carried for them.** Provenance of the reduced total
[E, script [6]]: 1,074 CPU-h on measured unit costs (M), 2,066 on derived ones (D), 1,261 on guesses (G).

| unit cost (provenance) | CPU-h resting on it | Phase-2 measurement that fixes it | carried |
|---|---|---|---|
| no-pile-up hard-scatter event, 45 ms (G) | 255 (pool share 217, multijet population 12.5, B6-c 25) | timing job: 10⁴ events of Z(νν), W, tt̄ with the generation filter | 100 % |
| toys on the real workspace, 652 s per 2 × 1000 on 31 parameters (G for the scaling) | 339 | timing on a 60–100-parameter workspace built from v1 counts | 100 % |
| ρ = 2 event, 206 s (D, one event) | 229 | day-0 job: 1, 2, 4, 8 events per job | 30 % |
| PU-200 row with one trial, 25.2 s (D; injection mode not benchmarked) | ≈ 1,250 (S1 561, overlays 294, SM hit level 266, C1 63, B6 59, pilot 7) | first signal-injection job; first overlay job | 30 % |
| Stage 3 per event (D, toy kinematics) | 306 (+ 36 in B6) | first Stage-3 chunk on MG5 events at 3 and 5 keV | 30 % |
| MLM generation 50 ms (G); FxFx 2 × 20 CPU-h (G) | 24; 40 | first chunk; first run | 100 % |
| V4-5 brute force, 0.3 CPU-h per event (G); T_seed regression (G) | 30; 44 | one event timed before the campaign | 100 % |
| Geant4 vertices at the measured yield (D); conversions, spectra, I/O and the two variations (G) | 65; 67 | Phase 3 hand-over tests | 30 %; 100 % |
| development and re-analysis allowances (G) | 437 | — (they are allowances) | 100 % |
| finder trial at the frozen road 0.15 (measured at 0.25) | all trials | day-0 timing; expected to lower the cost (×0.77 [E]) | — |

The contingency sized this way (10 % of M, 30 % of D, 100 % of G) is **1,989 CPU-h**, plus the reserved second direct
sample of 403 CPU-h. It is an exposure, not a plan: if every guess doubled, the reduced total would be about
6,400 CPU-h. v1 of this document carried a flat 20 % (655 CPU-h). The consequence for the stop rule is in §11.6.

### 11.3 Order, critical path, parallel campaigns (days after Gate A; proposed variant)

| days | phase | critical path | in parallel |
|---|---|---|---|
| 0–7 | 2 | day 0: ρ = 2 memory and storage, unit-cost timing jobs, first measurement of the utilisation; Stage 2 for the C1 points; C1 campaigns (198 CPU-h); C2 (81); enrichment pilot (27); **decision point 1 at day 7**; **stop-rule checkpoint 1** (re-projection with measured costs) | S2 (K, f₂₀₀, re-showers, FxFx), P1, retrieval tasks R-1 to R-20, Herwig install attempt; Geant4 geometry, material scan (B1-d) and hand-over code; T1 workspace builder on v1 counts; S1 string propagation (266 CPU-h) as low-priority filler until day ≈ 14 |
| 7–16 | 3 | B1 estimator, ceiling H and promotion on development samples; B2 re-grouping, N_eff per rung and occupancy model; B4 MET model with its external validation; T1 zero-count tests; **decision point 2 at day 15** (do the estimators close on the development samples? is the target reachable given the pilot's gain? if not, redesign before the freeze) | B3, B5 and B6 prototypes; T2 script and G from the v1 row arrays; enlarged development samples (100 CPU-h); 1-bot review per channel |
| 16–18 | freeze | `PREREG_v2.md`, 4-bot review, hash, commit, user notified; **stop-rule checkpoint 2** | — |
| 18–20 | | allowance for one ITERATE of the freeze review | |
| 20–34 | 4a | production of the background samples, 2,414 CPU-h at 174 per day = 13.9 days: B2 direct and ρ = 2 → no-pile-up pool → B1 overlays → B4 → B6, B5 | closure analysis as each campaign ends; T1 expected results with v1 placeholders; note writing |
| 34–37 | 4a review | 4-bot + bib on the compiled note; **decision point 3a: closure verdicts recorded** | S1 chain, both halves, not aggregated (561 CPU-h = 3.2 days; it needs no verdict and no verdict needs it) |
| 37–39 | | allowance for one ITERATE of the 4a review | S1 chain ends |
| 39–42 | 4b | T2 on the optimisation half; toys pass 1 (145 CPU-h, 0.8 day); 4-bot + bib | — |
| 42–46 | | allowance for one ITERATE (2 days); **Gate B** turnaround (2 days; verdicts first) | — |
| 46–49 | 4c | evaluation half: efficiencies, toys pass 2 (174 CPU-h, 1.0 day), limits, reach; BDT and dE/dx ratios; 1-bot review | — |
| 49–58 | 5 | note, paper (C3 list), package; 5-bot + adversarial review against §10; allowance for one ITERATE (2 days); **Gate C** | — |

**Calendar estimate: about 8 weeks from Gate A (58 days).** 44 of these days contain no production on the
critical path: 18 days of development and freeze before production, 16 days of reviews, analysis and writing after
it, 8 days of ITERATE allowances (one per panel review, as this cycle itself shows is realistic) and 2 days for the
user at Gate B [E, script [7]]. Range: 7 weeks if every review passes at once and only MUST items run
(44 − 8 + 11.5 = 47.5 days); 10–11 weeks if the production utilisation is 0.50 (64.8 days) or each panel review needs
two ITERATE cycles (+8 days).
**Development effort.** PLAN estimates B1–B4, T1 and T2 at about 35–50 person-days (PLAN l.298-366). The schedule gives
them 9 calendar days in Phase 3, with the Geant4 hand-over, the T1 builder and the B1-d scan started in Phase 2.
With six parallel channels this is about 54 channel-days, the same order as the plan's figure; v1 moved at a
comparable pace (Stage 4 from plan to result in about 4 days, D6 §1 [U]). It is the largest schedule risk that CPU
does not measure, and decision point 2 moves the freeze if the estimators are not ready.
**Idle capacity before the freeze.** Phases 2 and 3 and the freeze offer 20 days × 116 = 2,320 core-h and use 1,075
[E, script [7]]. Brief D7 forbids production samples before the hash, so the remaining ≈ 1,250 core-h cannot shorten
the production; 100 CPU-h of it enlarge the development samples so that decision point 2 has power at R05–R06.

### 11.4 Storage (cajuela, soft budget 1.5 TB)

| what | GB [E, script [8]] |
|---|---|
| PU-200 chain and trial records: 218,000 events × 0.52 MB | 111 |
| ρ = 2 events with dumps: 4,200 × 4.0 MB | 16 |
| hit dumps for 10,000 events (C2 700; B5 6,500; occupancy model and time tag 2,800; ≈ 2.4 MB each) | 23 |
| ρ = 2 pre-merge candidates (planning value; cap 400) | 200 |
| no-pile-up summaries (1.6×10⁸ events × 50 B) and full records of R04 passers and near-pass events | 33 |
| Stage 2 (LHE and five shower variants), Stage 3 | 11 |
| Geant4 vertices, logs, pyhf outputs, stored toy distributions, repo bundles | 18 |
| **total** | **≈ 410 (≈ 610 at the pre-merge cap)** |

Geant4 takes 6.6 GB of local scratch per worker. `sw/` on the NFS home is 0.58 GB (FEAS_B [V]); this does not include
the pixi environments under the home (`.pixi`, the workspace `.pixi` directories and the rattler cache), whose size
is reported in `STATUS.md` against the 150 GB software budget. The project stays far from the brief's 2.0 TB
stop-and-ask line.

### 11.5 Proposals that need the user's approval at Gate A (GA-7), and later triggers

| label | proposal | saves | lost | carried into the paper |
|---|---|---|---|---|
| [DP1] | B5 with 8 roads on 6,000 SM events with pile-up; hard-scatter T(Δφ) on no-pile-up samples in both variants | 358 CPU-h (2.1 days) | 45° instead of 18° granularity with pile-up; non-flatness with pile-up ×1.9 less precise; R07 not closed with pile-up (7.7 counts) | §4.8 |
| [DP2] | B6 at 4 points (E 200/1.5, E 500/3, E 500/5, E 1000/3 keV), 300 rows, 600 background events per variation; paired design | 155 CPU-h (0.9 day) | no variation for the scalar or at 1,500 GeV; unpaired precision 8.2 % instead of 5.2 %; other points by the interpolation rule | §4.9 |
| [DP3] | no MVA as primary selection; BDT cross-check at equal counted background | — | the gain is measured, not used | §3.2 |
| [DP4] | S4 and S5 not included | ≥ 1 week, ≈ 700 CPU-h (S4) | efficiency above 3 keV; m_Q, Λ handles | limitations |
| [DP5] | string against cluster hadronisation at generator level only (K/π and the species fractions that set the decay-in-flight rate), **after an install attempt** | a port of the full chain to a second generator | hadronisation-model systematic on pile-up kinematics limited to tunes | below |

[DP1] and [DP2] are compute-envelope proposals, not failed attempts; they are put to the user, not taken. If the user
declines both, the calendar grows by 2.9 days (513 CPU-h).
**[DP5] follows JFC 12 (attempt first; finding M24).** In Phase 2 the Herwig installation is attempted on a worker
with the conda-forge package, in the one install slot, to local scratch as for Geant4. If it installs: 10⁶
minimum-bias events at generator level, and the K/π and proton fractions against Pythia in the p_T and η range of
the decays-in-flight term; the difference is the nuisance on rate_DIF (§5.1). If it does not: the failure is
documented with the error, a second route (source build on a worker in `/var/tmp`) is tried once, and only then the
comparison falls back to published minimum-bias data (R-19). The expected size of the effect cannot be quoted from
the repo; R-19 retrieves published differences. In the paper: the systematics table states which comparison was
made; Future Directions names a full-chain second generator.
Triggered later, only after a documented failed attempt: [DT1]–[DT5] (§7).

### 11.6 The 2–4 week target (brief D6) and the stop rules (brief §7)

**The target is missed by about four weeks, and compute is not the main reason.** 44 days of the schedule contain no
critical-path production; this already exceeds 28 days. (v1 of this document said that a 4-week schedule "would
need production near 1,000 CPU-h"; that was wrong: its own schedule had about 30 days without production.) The
production adds 11.5–16.8 days.
*Levers that do not touch a MUST criterion* (offered; each is a line in GA-8 or GA-3):
(i) the no-pile-up pool at 315 CPU-h instead of 600: −285 CPU-h, −1.6 days; the summed floor is then 86 events
instead of 45 (GA-3);
(ii) toys of pass 2 on an 11-value grid of the SR-T signal fraction per selection, interpolated and checked by exact
toys at 3–5 points: 48 CPU-h instead of 174 (the background model of a selection is the same at all 40 points; review
N-B-14); it shortens Phase 4c by less than a day and is adopted only if the check agrees within the toy error;
(iii) B5 with pile-up on the 500 pile-up events only, the SM part from the no-pile-up samples alone: −137 CPU-h,
−0.8 day; B5-c on SM samples is lost;
(iv) reviews that pass at once save their allowances (up to 8 days); this cannot be planned.
*Levers that touch MUST statistics* (listed for completeness, **not proposed**): S1 at 500 rows at the 15 points
below 1 keV (−158 CPU-h); B4 hit-level samples at 1,000 events for the eight small processes (−56 CPU-h). v1's third
lever, the B2 direct sample at 12,000 events, is withdrawn: at 35 counts R07 is no longer evaluable (σ_ln = 0.17
against the limit 0.135).

**Stop rules.** The brief's rules are quoted exactly (`prompt.md` §7, l.341-348, and D6, l.79):

> "Stop and ask the user if:
> - admin or sudo rights are needed, the cluster method is unclear, or a cluster service (NFS, cajuela, Kubernetes,
>   Argo, LDAP) is broken. Do not try to repair cluster infrastructure; stop and report the exact error;
> - the project's cajuela usage would pass 2.0 TB, or the pool's free space would fall below 1.0 TB (§5.2);
> - a MUST item is infeasible after a real attempt;
> - an arbiter returns ESCALATE;
> - the projected compute overruns the approved schedule by more than 30%;
> - anything would publish to, or contact, an external service."

> "D6 Timebox. Target 2–4 weeks. There is no hard deadline, but every overrun of the approved schedule is reported."

How they are applied here (COM ST-1):
- *Approved schedule* = the variant and the calendar the user approves at Gate A. For the proposed variant:
  4,401 CPU-h and 58 days. **Every** overrun of either, of any size, is reported in `STATUS.md` and in the next gate
  package.
- *Projected overrun above 30 %*: when the projected total exceeds 1.3 × the approved CPU-h (5,722 for the proposed
  variant), **the study stops and the user is asked**. It does not "correct the schedule" and continue, as v1 of this
  document said in two places.
- *Checkpoints at which the projection is recomputed with measured costs:* (1) day 7, after the Phase-2 timing jobs
  and the first week's utilisation; (2) at the freeze, before any production; (3) weekly during production, from
  the ledger; and at once whenever a conditional cost of §11.2 is triggered.
- *Stated risk:* 1,261 CPU-h rest on guesses. If the guesses are low by a factor 2, the projection is about 6,400 and
  the rule triggers at checkpoint 1. The user should expect that this may happen.
- The storage rule is far from binding (410–610 GB against 2.0 TB); the pool's free space is checked before each
  campaign.

### 11.7 Decision points of PLAN §8

| # | question | when | if "no" |
|---|---|---|---|
| 1 | is the v1 chain reproducible on Linux (C1) and does the finder pass (C2)? | day 7 | regression; Phase 3 does not start on the failed family |
| 2 | do the estimators close on the development samples at the loose rungs, and what do the pilot's gain and the development floors say about the outcome class? | day 15 | redesign before the freeze; the freeze moves; user informed |
| 3 | after production: background verdicts, then signal | days 34–46 (Gate B at ≈ 46) | failed terms reported; eligibility rule [SD8] |
| 4 | include the endcap? | — | void: dropped by brief D1 |

---

## 12. Decisions for the user, open issues, and how this study could fail

### 12.1 Decisions requested at Gate A

Each item has a recommended default (marked ●) that this strategy follows if it is approved, the alternatives, and
what each costs. One line per item is enough as an answer (for example "GA-1 a; GA-2 2,000; …"). CPU-h and days
from the script; days at 174 core-h per day. Reach numbers are the plan's table (PLAN l.119-123), EST, built on v1
efficiencies, which are placeholders.

**GA-1 — The C1 signal comparison and blinding (§4.1; finding M2).** Six of the ten C1 signal counts are efficiencies
of v2 candidate selections; looking at them before the closure verdicts is an exception to the brief's blinding
invariant that only the user can grant. CPU is the same in every option (14 CPU-h).
- ● (a) Sealed comparison: R04 and R06 counts open (4 quantities); R07 and fallback counts (6) compared by a
  dedicated agent that reports only PASS/FAIL, counts sealed until Gate B. Cost: a sealed FAIL cannot be diagnosed
  from its size before Gate B without a new decision by the user. Statistical power unchanged.
- (b) All ten open, six disclosed in the paper as candidate efficiencies seen before the verdicts. Cost: the study
  knows the efficiency of two T2 candidates at 3 of the 20 window points to about ± 16–23 % (1σ on 400 rows, script
  [13]) before the verdicts.
- (c) R07 and fallback dropped from C1 (4 quantities left). Cost: the best-point count of v1 (9 of 200) is not
  reproduced at all; it was a gross check only (detectable shift 80 %).
- (d) All ten sealed, nothing open. Cost: no signal-side reading at all before Gate B; decision point 1 rests on
  PASS/FAIL marks for the signal family.
- (e) As (b) with 200 rows per point. Cost: detectable shifts 39 % (R04) and 93 % (fallback) instead of 34 % and 80 %.
In every option R07 and family F stay in the T2 list as declared.

**GA-2 — Signal rows per point (§4.13; finding M20).**
- ● 2,000 rows ("×10" in total, ×5 on the half that sets the limit): 15 % statistical error at ε = 0.045.
- 4,000 rows (×10 on the limit half): 10 %; **+827 CPU-h, +4.7 days**; storage +42 GB.

**GA-3 — The paper's message given the floors, and the size of the no-pile-up pool (§4.4; finding M6).**
With zero counts everywhere the leading terms are bounds. Pool size:
- 315 CPU-h (the v1 sizes at the corrected cost, re-allocated): summed floor 86 events; −285 CPU-h, −1.6 days.
- ● 600 CPU-h: summed floor 45 events (median of the predictive sum 36).
- 1,200 CPU-h: summed floor 23 events; +600 CPU-h, +3.4 days.
Reach for scale: 495 GeV at B = 100, 662 GeV at B = 30, 796 GeV at B = 10 (σ_ln = 1).
Message:
- ● (i) The paper reports the outcome under the labels fixed in §4.11. If more than half of the background is
  bounds (f₀ > 0.5), the abstract says that the background is **bounded at the N-event level by simulation
  statistics**, with the pile-up term estimated, and quotes the expected limit with its band and its conservative
  edge. "Estimated, not bounded" is used only if the terms have counts and passed closure.
- (ii) Aim for "estimated": after the Phase-2 pilot, if the measured gain of biased generation is at least about 5
  for the leading terms, the pool is generated biased (floors divided by the gain); if it is smaller, fall back to
  (i). No extra CPU; the freeze text depends on the pilot.
- (iii) If the pilot shows a gain below 5 and no conditional credit, pause at decision point 2 and ask the user
  whether the "middle, bounded" paper is worth the production.

**GA-4 — Closure tolerances, eligibility, what an untested term earns, extrapolation convention (§4.0, §4.12;
findings M4, M5, M15).**
- Tolerances: ● F = 1.5 (pile-up, conditionals, sideband) and 2 (single-interaction, hard-scatter), unchanged from
  v1. Tighter F needs more counts per test rung (N ≥ 55 at 1.5; N ≥ 181 at 1.25).
- NOT TESTED: ● no credit (the term enters at its directly measured ceiling, selection eligible, flagged).
  Alternatives: *not eligible* (stricter; with PV pairs expected NOT TESTED this removes nearly every deep selection
  and makes "closure fails" the likely paper); *credit with the extrapolation width* (looser; an untested promotion
  model would lower the background).
- Family-wise rule: ● outright FAIL at p < 0.05/K, one re-test on a fresh sample for 0.05/K ≤ p < 0.05 (a correct
  analysis is rejected in 7.5–10 % of the cases at K = 12; reserve of 403 CPU-h). Alternative: every test at
  p > 0.05 with no re-test (rejects a correct analysis in 46 % of the cases).
- Extrapolation in untested cut families: ● one tolerance per rung, coherent (ln F × d). Alternative: independent
  steps (ln F × √d), which gives for pile-up at R14 a width of 1.0 instead of 2.4.

**GA-5 — Signal normalisation (§4.14; findings M23, M28).**
- ● σ_NLO computed here as nominal; σ_NLO × (NLO+NLL)/NLO from the public tables as an implemented cross-check,
  quoted beside every limit. Alternative: the resummed product as nominal (FEAS_B's recommendation). No CPU either
  way; the size of the difference is known only after R-1.
- Infracolour Coulomb correction: ● drawn as a one-sided upward band on the theory line (+3 to +13 % at β = 0.7 to
  0.3 before averaging over β), not applied. Alternative: applied to σ_norm (raises the reach; needs a cited
  treatment).

**GA-6 — dE/dx (§4.12; finding M30).**
- ● Not a candidate; the forgone signal-efficiency ratio is measured after Gate B (2 CPU-h).
- Model the charge deposit with straggling and keep one dE/dx candidate with its own closure: about +390 CPU-h
  (re-digitisation of the pile-up and signal samples, 104,000 events × 13.5 s [E]), about one more week of
  development, and a later freeze.

**GA-7 — Downscope proposals (§11.5).** Approve or decline each: [DP1] B5 reduced (saves 358 CPU-h, 2.1 days);
[DP2] B6 reduced with 5 keV and 1 TeV kept (saves 155 CPU-h, 0.9 day), or the paired six-point version (about
+35 to +55 CPU-h over the reduced form [E, script [13]]); [DP4] S4 and S5 not included (S4 would cost ≥ 1 week and ≈ 700 CPU-h; S5 about
a week and 50 CPU-h); [DP5] hadronisation comparison at generator level after an install attempt. ● approve all.
([DP3], the MVA as cross-check only, is for the reviewers to validate.)

**GA-8 — Schedule and approved compute (§11).** The 2–4 week target cannot be met.
- ● Approve 4,401 CPU-h and 58 days (about 8 weeks) as the "approved schedule" against which overruns are reported
  and the 30 % stop rule is applied (threshold 5,722 CPU-h).
- MUST only: 3,968 CPU-h, 55.5 days. Full SHOULD: 4,915 CPU-h, 60.8 days.
- Levers that touch no MUST criterion: §11.6 (i)–(iii), up to −420 CPU-h and −2.4 days together with a higher floor.

**GA-9 — Time-tag credit for prompt backgrounds (§4.6; finding M16).**
- ● Measured at hit level and used only if its closure passes and the timing tails are sourced; never below the
  sourced tail fraction. It can lower the SR-T background by orders of magnitude; it was not in the plan.
- No credit, as in v1: SR-T carries the same single-interaction and SM terms as SR-G. Saves 10 CPU-h.

**GA-10 — Endcap wording.** Brief D1 fixes the outlook statement "signal ×1.5–3.2"; the lower end 1.5 has no
derivation in the book or the plan (the book gives ×3.2 at g = 1 and ×2.1 at g = 0.5; D3 §5). ● The statement is
used as fixed, tagged EST. Alternative: the user changes it to "×2.1–3.2".

### 12.2 Judgment calls made in this version (also in `experiment_log.md`)

DECISION: expected limits are generated with every counted rate drawn from Gamma(m + 1) (flat prior), auxiliary
observations fixed at the observed counts; "one zero per term".
ALTERNATIVES: generation at the fitted value (terms vanish); fixed 1.14/M; Jeffreys Gamma(m + ½); both reported at
the best point.
CONFIDENCE: MEDIUM-HIGH (analytic one-bin checks in the script; exact coverage 0.945–1.000). FLAG FOR HUMAN: YES —
it sets how a zero count appears in every limit of the paper.

DECISION: closure tests use disjoint derivation and test rungs and samples, an evaluable-rung rule (σ_tot ≤ ln F/3),
four verdict classes, and an extrapolation width that is always added.
ALTERNATIVES: v1's same-rung test with N ≥ 20; a width only when the slope is significant.
CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES (GA-4).

DECISION: the single-interaction estimator is P_geo·S + Σ f_k·π_k with the directly measured ceiling H as its
no-credit value; S = 1 beyond its tested rungs.
ALTERNATIVES: P_geo × C_PU with C_PU carried from R07 (no promotion term); overlays of random failers at depth
(a floor of N_t × 1.14/2,000).
CONFIDENCE: MEDIUM (the size of the near-pass classes is unknown until the pilot). FLAG FOR HUMAN: NO.

DECISION: one pool of 600 CPU-h for the no-pile-up samples, allocated as √(N_t/c_t); biased generation used only if
its weights closure passes.
ALTERNATIVES: v1 sizes; 315 or 1,200 CPU-h (GA-3).
CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES (GA-3).

DECISION: detector variations with round-number sizes are robustness tests; nuisances take public sizes or do not
exist.
ALTERNATIVES: measured effect of the round-number variation as nuisance (forbidden by JFC).
CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.

Kept from v1 with their flags: QED FSR on in the nominal signal (HIGH, no flag); no MVA as primary selection (HIGH;
reviewers validate the corrected argument of §3.2); C1 signal at 400 rows (GA-1); σ_norm from computed NLO (GA-5);
time tag (GA-9); dE/dx excluded (GA-6).

### 12.3 Other items the user should know
1. **v1 freeze timing** (§8): the paper will say that the v1 analysis code was re-frozen after efficiencies existed.
2. The CMS-internal cross-check listed as open work in v1 (D1 §6) is outside the plan and is not done (public
   information only).
3. Book Part VI did not pass its own review (D3 §6.7); every number taken from it is recomputed from the tracked
   JSON before it enters the paper.
4. The stop rule on compute may trigger at the first checkpoint (§11.6): 1,261 CPU-h rest on guessed unit costs.

### 12.4 Not resolved in Phase 1
- ρ = 2 memory and cost at production size; pre-merge bytes per trial; thinning N_eff per rung (day 0 and week 1 of
  Phase 2).
- The gain of biased generation and the size of the near-pass classes (Phase-2 pilot); whether v1's single-interaction
  generation orients the topology in the road.
- v1's coded attribution rule and thinning unit (read from the code in Phase 2).
- Whether the probe-row exclusion of v1 can be rebuilt from the tracked row arrays (§4.1).
- The active Fatras physics list (B1-d).
- Parameters of the MET model and its external validation figure, the trigger curve, the timing resolution with its
  tails, vertex efficiency, readout window, noise occupancy, hit resolution, hit efficiency, material budget, the
  K-factors of the SM processes, the cosmic and halo rates, the infracolour correction in the literature: retrieval
  tasks R-1 to R-20. None is in the repo. An item whose number cannot be sourced is reported as "not sourced" with
  the consequence stated in its section.
- Unit costs listed in §11.2; the two utilisation factors.
- Which configuration v1's B*-off test ran (§4.15).
- R3's and R2's statistical methods (Table 6.1 has "not extracted" cells; R-10 closes before Phase 4a).

### 12.5 What would make this study fail
1. Both pile-up estimators fail B2-a/B2-b: no validated pile-up term beyond R07.
2. The large no-pile-up samples count zero, biasing gives no gain and the conditionals give no credit: the result is
   bounded at about 45 events by sample size (the "middle" outcome as a bound). This is the outcome to expect if
   nothing else is learned; it is a weaker paper, not a failed study.
3. The large samples show passing single-interaction events at a rate that leaves B ≫ 10³: a measured background and
   a reach below the existing bounds at low mass (plan outcome "real background").
4. The Geant4 → Fatras hand-over cannot be made consistent (parent hits, geometry identifiers).
5. C1 fails for the pile-up family: nothing built on the chain can be trusted until it is understood.
6. The finder fails V4-5: every efficiency and rate is in doubt.
7. The MET model or the timing tails cannot be sourced from public documents: the three additions of B4 stay
   unquantified, and the time tag earns no credit.
8. Infrastructure: NFS or cajuela outages (two incidents on day one, `LOG.md`), memory limits for ρ = 2. A projected
   compute overrun above 30 % of the approved schedule **stops the study until the user decides** (brief §7).
9. A blinding breach: any v2 signal efficiency seen before the verdicts outside the list of §4.1. The C1 comparison
   is the place to watch; the sealed tier exists for that reason.

---

## 13. Changes since v1 (`STRATEGY_brigitte_2026-11-13_17-55.md`)

Merged findings of the arbiter (A = M1–M11, B = M12–M35). Details and the C items: `FIX_REPORT_cycle1_dmitri.md`.

| finding | what changed | sections |
|---|---|---|
| M1 zero counts in the likelihood | model table; Gamma(m + 1) generation with derivation; definitions of estimate, bound, leading, B₈₄, σ_ln, f₀; one-bin analytic table; tests T1-c; T2 robustness check | §4.11, §4.12, §5.1, §12.2 |
| M2 C1 blinding exception | six, not three; sealed tier as default; R07 and family F fixed; exception takes effect only with the user's approval | §4.1, §8, GA-1 |
| M3 same-rung closure | derivation and test on disjoint rungs and samples; survival and promotion; ceiling H; consistency checks labelled | §4.0, §4.4, §4.6, §4.7, §4.17 |
| M4 extrapolation width | s_tot(r) always added, with its derivation; S = 1 beyond tested rungs; stability of conditionals; table of distances per candidate | §4.0, §4.4, §4.5, §4.6, §4.12 |
| M5 testability, NOT TESTED | evaluable-rung rule; expected-count table; four verdicts; no credit by default; leading decided with no-credit values | §4.0, §4.4, §4.7, §4.12, GA-4 |
| M6 floors, central target | floor table; pool of 600 CPU-h by √(N/c); pilot for the biasing gain; projected outcome in §0; σ_ln as reported outcome | §0, §4.4, §4.7, §4.11, §11.2, GA-3 |
| M7 injection, pulls, units | injection in multiples of μ₉₅^exp on fluctuated pseudo-data; pulls on pseudo-data; μ₉₅ units stated | §4.11, §5.2 |
| M8 T1-g, toy budget | coverage at known signal from stored distributions; two toy passes budgeted; [L4] measured in Phase 2 | §4.11, §11.2 |
| M9 MET validation | soft term from R-3 only; external validation; (a) and (c) relabelled | §4.7 |
| M10 stop rule | brief §7 quoted verbatim; checkpoints; "schedule corrected" removed | §4.13, §11.6, §12.5 |
| M11 variation sizes | robustness tests separated from nuisances; sizes from R-15 to R-17; B1-c criterion without the ×2 band | §4.4, §4.9, §5.1 |
| M12 nuisance propagation | table: every shared nuisance evaluated on every term; no-pile-up reruns | §4.9, §4.11 |
| M13 [DP2] | reduced set keeps 5 keV and 1 TeV; interpolation rule; paired design | §4.9, §11.5, GA-7 |
| M14 thinning reach | K = 64 draws, N_eff, projected reach R07; B2-c expected NOT EVALUABLE; occupancy independence per rung family | §4.5 |
| M15 closure statistics | full covariance with common s_model; s_model a pre-freeze number; size and power per test; family-wise rule | §4.0, §8 |
| M16 time tag | timing model with tails; hit-level measurement; widened-window closure; independence test | §4.6, GA-9 |
| M17 undeclared signal quantities | complete list; A, f₂₀₀, migration declared; threshold decided before A; B6 nominal partners; C2 count moved to 4c | §4.1, §4.2, §4.9, §4.14 |
| M18 MVA argument | wrong claim removed; three reasons that hold; hybrid excluded for blinding; working point at equal total counted background | §3.2 |
| M19 costs and schedule | unit costs corrected with provenance; 10-slot capacity; contingency from provenance; ITERATE and gate allowances; development effort; wrong "1,000 CPU-h" sentence removed | §4.0, §4.15, §11 |
| M20 S1 "×10" | stated as ×10 total, ×5 on the limit half; option of 4,000 rows | §4.13, GA-2 |
| M21 C1 chain per point | v1 path per point; full-chain twins as diagnostic | §4.1 |
| M22 attribution | rule for attributed candidates | §4.4 |
| M23 K validations | NLO against NLO at 3 %; differential K(M) at 2 %; parity argument, resummed cross-check implemented | §4.14, GA-5 |
| M24 Herwig, DPs in the paper | install attempt first; how each DP is carried into the paper | §5.1, §7, §11.5 |
| M25 criterion identifiers | COM is the master; this document quotes its identifiers | all of §4; COM |
| M26 background list | pile-up-vertex secondaries (test), noise and out-of-time hits, δ-rays | §2, §4.4 |
| M27 signal detector response | MET model on signal; migration sample; lepton-veto assumption; hit-time window | §1, §4.13 |
| M28 infracolour correction | formula with substitution; per-mass average in Phase 2; one-sided band | §4.14, GA-5 |
| M29 T2 background-side bias | bootstrap of the choice | §4.12 |
| M30 dE/dx | forgone-gain ratio; option to model it | §4.12, GA-6 |
| M31 B5 | closure on the hard-scatter component; T(Δφ) on no-pile-up samples; [DP1] loss restated | §4.8 |
| M32 weighted samples | one auxiliary channel per weight class; effective counts | §4.11 |
| M33 multijets | factorisation from a looser population, tested on Z(νν) and W | §4.7 |
| M34 failure after the freeze | three-branch protocol; reserved fresh sample | §8 |
| M35 sample inventory | 24 samples with role, seed stream, independence, phase, CPU-h | §4.17 |

---

## Code reference
- `python3 -I analyses/quirks_v2/phase1_strategy/src/strategy_budget.py` prints every CPU-h, storage, calendar, floor
  and test-power number of this document (standard library; about one second). Its sections [1]–[13] are cited in
  the text as "script [n]".
- No pixi task was run and no sample was produced for this document.
