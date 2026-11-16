# STRATEGY — HL-LHC electroweak quirks, study v2 (Phase 1, JFC) — version 10

Fixer: Oscar, 2026-11-16 10:41, review cycle 9. This version replaces `STRATEGY_mireille_2026-11-14_06-55.md` (version 9,
kept unchanged) after the ninth arbiter verdict ITERATE (`review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`:
finding B-1 and the C items it orders). Comparisons with earlier versions are made
only in §13. Arithmetic: `../src/strategy_budget.py` ("script [n]" below points to its printed section n).
Status: for verification and then the user's Gate A. Nothing here has been produced yet except the
feasibility benchmarks. The user's decisions are in §12.1: five questions Q1–Q5 and eleven defaults.

**Paths.** `REPO` = `/home/users/jdochoa/hllhc-quirks-search`; `QV2` = `analyses/quirks_v2`;
`TT` = `stage2_C001_quirks/theory_track`; `S4` = `TT/acts/stage4`; `AN1` = `TT/data/acts_stage4/analysis/C12FC_v1`;
`SUM` = `TT/data/acts_stage4/analysis/STAGE4_SUMMARY.json`; PLAN = `publication_plan/publication_plan.tex`;
D1…D6 = the digests in `outputs/digests/`; FEAS_A/B/C = the reports in `outputs/feasibility/`; COM = `QV2/COMMITMENTS.md`.

**Tags.** **[V]** VERIFIED: the number was read at the cited file:line or JSON key by the author of the sentence
(the author of the version that introduced the sentence, §12.2), or re-derived (the script section is given). **[E]** ESTIMATE,
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
- **Projected outcome, stated before anything is run** (the expected branch is in "Expected" below: by v1's own
  counts the hard-scatter conversions are a large counted term, not a bound). v2 measures
  each background term on samples large enough to count it where that is possible, and closes each correction on
  rungs and samples it was not derived from. Where the simulation still counts zero, the term stays a bound and the
  likelihood keeps it (§4.11). Each particle origin is counted by one term (§2): the tracks of the hard-scatter
  vertex are in the real SM events of B4, and the single-interaction terms of B1 are the decays in flight and nuclear
  interactions that need Geant4. With the no-pile-up samples the cluster can produce (665 CPU-h, 7.3×10⁷ events over
  DIF, NI and **fourteen** SM processes, Z(ττ) and lost-lepton Z(ℓℓ) included), a zero count in every term still
  allows **about 13 events in 3 ab⁻¹**: the 68 % upper values sum to 12.6 for the pool terms and 0.46 for the
  multijets at their planning N_trig (13.0; 12.2–17.8 over the planning ranges of the three additions); predictive
  median 10.8, 16–84 % range 7.7–15.2 [E, script [9]]. Three things come on top of this floor, and the projection
  contains them (Table 4.4c, script [9b]):
  1. *The ceiling H.* A term whose pile-up factors cannot be tested enters at its no-credit ceiling H (§4.4). H
     counts near-pass events and is expected to be non-zero. The projection of a term is max(zero-count floor,
     N_t·H). For Z(νν)+jets one counted ceiling event is 2.3 events in 3 ab⁻¹. H is not known before the Phase-2 pilot.
  2. *The pile-up term at depth*, a one-estimator extrapolation beyond R07: EST median 90–150 events at R08, 5–9 at
     R09 and below 1 from R11 on, with B₈₄/B₅₀ = 1.5–1.8 at R08–R09 [E from v1 numbers, script [9b]].
  3. *Decays in flight and hard-scatter conversions*, which v1 counted at R06–R07 with pile-up (2 and 1 DIF, 13 and 2
     conversions per 500 events; Table 4.4b). The conversions fell by ×6.6 and ×6.5 per width step (86 → 13 → 2), not
     like the random pile-up background (×201–339): with a pile-up-like fall from R06, v1 would have expected
     0.04–0.07 counts at R07, and 2 or more has probability 7×10⁻⁴–2×10⁻³ [E, script [9b]]. Extrapolated with their own
     fall, which is the rule the pilot reading uses (§4.4 point 5), they leave ≈ 9.5×10³ events at R08–R09 without
     fit-probability credit, and the background is ≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c) (after CKF, as v1 counted them) (with v1's maximum-over-process photon
     rate; ≈ 6.4×10³ conversions and B₅₀ ≈ 6.8–7.1×10³ with its N_trig-weighted rate). If they fell like
     the pile-up background, they would add 570–960 events (projected B₅₀ 590–980; (α1); after CKF, as v1 counted them; the day-15 rule reads this branch on all own hits, (α1)
     row of the v9 table of script [9b]).

  **Expected (ESTIMATE, v1 placeholder efficiencies; every reach number rests on them, best Λ per mass, PLAN l.121):**
  by v1's own counts the background of the default plan at an R08–R09 selection is led by hard-scatter photon
  conversions, **≈ 0.7–1.0×10⁴ events (v1's N_trig-weighted and maximum photon rates, 0.255 and 0.379 per event; after
  CKF, as v1 counted them, a lower value: a term whose S_CKF is not tested stays on all own hits, ×1/(1 − ε_pair) higher, annex route 6). The
  strategy gives this background the normalisation nuisance of its SM terms (§4.7: the generator difference 0.84 for
  Z(νν)+jet, |ln 0.84| = 0.17, before K, luminosity and material). With a width of 0.17 the reach is below the plan's
  table (< 243 GeV; below 200 GeV by its σ_ln = 0.2 row, PLAN l.122), i.e. at or near the existing bounds, and its
  84 % edge is already below 243 GeV at a width of 0.03. The statistics-only values, ≈ 270–300 GeV at the 84 % edge
  (median ≈ 315–340; ≈ 390–420 GeV for a background known exactly), hold only for the counting width of ≈ 0.02** [E,
  script [9b], v6 lines]. The day-15 rule is expected to pause the study before production (§11.7, Q2). The upper branches, each as 84 % edge (median):
  ≈ 420–455 GeV (470–500) if decays in flight and conversions fall like the pile-up background and earn no
  fit-probability credit (α1), which v1's conversion counts disfavour at p ≈ 10⁻³; the factor-e uncertainty of this
  v1-based size moves the median between ≈ 400 and ≈ 570 GeV; ≈ 705–640 GeV (770–695) if Z(νν) is tested and credited
  (at its floor) and the terms expected at their ceilings count 10–100 events per Z(νν)-sized sample (β), conditional
  on the promotion model being submitted (a result after the freeze: its Z(νν) credit comes from the B4-c test, so the day-15 rule reads it as (γ), through the Z(νν) pilot count, v9 table of script [9b]); ≈ 710 GeV (790) if every no-pile-up ceiling counts zero, an upper edge that
  the strategy's own planning estimate does not expect (Df-9: m_H = 10–890 for Z(νν), §4.4 point 4); 1,026 GeV for a
  negligible background. These upper branches are statistics-only in the same sense: with the width 0.17 on the
  counted terms the (α1) 84 % edge is ≈ 310–370 GeV instead of 420–455, and the m_H = 100 row is 454 instead of 523 GeV;
  they stay above the existing bounds [E, script [9b], v6 lines]. Existing bounds lie below about 180 GeV (PLAN l.115-116; the search for newer results, R-20,
  is pending) [E, script [9b]]. The abstract heads with the 84 % edge of the branch that is realised (§4.11 point 3).
  Caveats: v1 placed the pile-up DIF vertices at the PV, and v2 places them at their own z, which may lower the DIF part
  of (α); v1's attribution rule is not yet transcribed; neither caveat applies to the conversions; the SM floor rests
  on a guessed 45 ms per event (at 90 ms the summed floor is 20.8 instead of 12.6, script [9]); the v1 fast-path
  efficiencies behind the reach numbers are ×1/0.87 high, so the v2 reach is expected somewhat lower; the plan's reach
  row assumes the selection's efficiency equals the book's best-Λ efficiency, a bias of either sign. **The pause.**
  The day-15 rule (§11.7 rule 1) pauses the study and asks the user if the projected B₅₀ exceeds 300 events or both
  pile-up estimators miss their cap; it is computed preliminarily at day 7. It reads every term from the pilot's
  own-hit counts before CKF, at max(zero-count floor, N_t·H) on the samples that exist at day 15: decays in flight and
  nuclear interactions on their own pilot samples, and every SM hard-scatter process and the multijets at the H per
  event of the Z(νν) pilot, with no S_CKF, no conditional (no veto, no fit-probability credit), no credit that exists
  only after the freeze and no pool floor (this reading of the rule was pinned in review cycle 8 and is an overridable default, Df-11; for the processes without a sample it is a proxy that errs on the lenient side, Q2 caption). One Z(νν) pilot count is 18 events and one decays-in-flight pilot count is
  65. Its decays-in-flight and conversion terms are therefore ×5–50 above their after-CKF sizes (ε_pair assumed
  0.8–0.98, not measured, and not bounded above). The expected reading is B₅₀ ≈ 3×10⁴–3×10⁵ by v1's conversion counts
  ((α1′)) and ≈ 2.6×10³–4.2×10⁴ even if decays in flight and conversions fell like the pile-up background ((α1)): the
  pause is the expected branch. The reading is below 300 only if the pilot's counts are nearly zero: B₅₀ ≈ 76 with
  every pilot count at zero; the limit is at ≈ 12 Z(νν) pilot counts, which is also how the rule reads (β) and (γ), or
  between 3 and 4 decays-in-flight pilot counts (script [9b], v9 table; at the R09 pile-up estimate, and at fewer counts at an R08 candidate, Q2 caption). A conversion veto
  or a fit-probability credit enters only the test of a Q2 (c) redesign (Q2). If the pause fires and the user chooses Q2 (b), the
  paper is the plan's "real background" outcome (PLAN §9: a measured background, the reach at that B, at or near the
  existing bounds with the planned width, the sideband recipe as the way out). If
  the pause does not fire, the paper is the plan's "middle" outcome with the leading terms **bounded, not
  estimated**; its pre-declared label is "target not met: sample-size limited" while the ceilings count few events
  ("target met" needs σ_ln ≤ 1, f₀ ≤ 0.5 and every leading term labelled estimate, §4.11 point 3). Which of the two
  is the default deliverable is Q2.

  **Leading sentence** (for the abstract-level summary, `STATUS.md` and the Gate-A package): **Expected (ESTIMATE, v1
  placeholder efficiencies): by v1's own counts the default plan's background at R08–R09 is led by hard-scatter
  conversions, ≈ 0.7–1.0×10⁴ events (v1's N_trig-weighted and maximum photon rates; after CKF, as v1 counted them, a
  lower value: a term whose S_CKF is not tested stays on all own hits, ×1/(1 − ε_pair) higher). With the normalisation
  uncertainty this strategy itself assigns to that background (≈ 0.17, the generator difference of §4.7) the reach is
  below 243 GeV, at or near the existing bounds of ≈ 180 GeV; the ≈ 270–300 GeV at the 84 % edge (≈ 390–420 GeV for a
  background known exactly) hold only for its counting width alone. The day-15 rule is expected to pause the study
  before production (projected B₅₀ ≈ 3×10⁴–3×10⁵ on its own-hit basis against a limit of 300); a conversion veto can
  count only in a Q2 (c) redesign, and at v1's central decays-in-flight size (1–2 counts) no conversion rejection
  suffices without a reduction of the decays in flight.** (Basis of the last statement: Q2 (c) and the v9 grid of script [9b].)

  Three things can improve the bounded outcome: biased generation (gain measured by the pilot, §4.4);
  conditionals of purpose-built cuts and the time tag (§4.6; a conditional applied more than two rungs beyond where it
  was measured has a width above 0.8, §4.0 point 7); and counts in the large samples (the terms are then estimates).
- **Cost.** MUST items: **4,019 CPU-h**; with the SHOULD items in the reduced form proposed here 4,453 CPU-h, and
  with the 156 CPU-h day-15 reserve that the default plan spends, **4,609 CPU-h, the approved figure proposed in Q4**;
  with the full SHOULD items 4,966 CPU-h (5,123 with the reserve) [E, §11.2, script [4]]. 1,378 CPU-h of the
  reduced total rest on unit costs that were never measured; they are listed with the Phase-2 measurement that fixes
  each (§11.2).
- **Calendar.** With 10 usable off-hours slots the cluster gives about **174 effective core-h per day in production**
  and 116 in development [E, §11.1]. With at most three agents at a time (slot table, §11.3), one ITERATE allowance per
  panel review and the Gate-B turnaround, the study takes **about 8.5 weeks from Gate A to Gate C (60 days, of which ≈ 2 are the expected day-15 pause; 58 days without it;** 49 days if
  every review passes at once and only MUST items run; 65 days at 50 % utilisation (both without the day-15 pause); +8 days with two ITERATE cycles per
  review**)**. **The 2–4 week target of brief D6 is not reachable**: the days without production alone are 43.5 (§11.3).
- **Storage.** About **470 GB** on cajuela, 670 GB if the pre-merge candidate store reaches its cap, against the
  1.5 TB soft budget [E, §11.4].
- **Stop rules (brief §7, quoted in §11.6).** A projected compute overrun of more than 30 % of the approved schedule
  (5,992 CPU-h for the proposed variant) stops the study and the user is asked.
- **Decisions for the user (§12.1).** Q1 the C1 signal comparison and blinding; Q2 the deliverable if the background is
  large (the expected case); Q3 the exception to brief D4 for every MUST closure criterion that ends untested; Q4 budget, calendar
  and stop rule with the proposals [DP1], [DP2], [DP4], [DP5]; Q5 the reading of brief D7 for the truth-level signal
  samples. Eleven defaults are reported and can be overridden.

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
with N_trig = 4.0848×10⁷ ± 2.0 % triggered events in 3 ab⁻¹ (D4 §2.1, `AN1/bsum_wp.json` → `n_trig` [V]).

Table 2.1. Classification, v1 size (SR-G, events in 3 ab⁻¹; from D4 §2.3, which read `AN1/bsum_wp.json` [U by me];
"b" = zero-count bound) and the v2 estimator.

| term (as v1 lists it) | class | R04 | R06 | R07 | R09 | v2 estimator (item) |
|---|---|---|---|---|---|---|
| Pile-up random planes | instrumental (combinatorial) | 1.05×10¹⁰ | 3.8×10⁷ | 1.35×10⁵ | 252 b | repaired thinning + independent occupancy model, both closed against direct counts (B2) |
| Decays in flight (π, K kinks) | reducible | 2.1×10⁷ | 3.0×10⁵ | 1.5×10⁵ | 1.7×10⁵ b | Geant4 vertices → Fatras; pass and near-pass probabilities without pile-up × survival and promotion, with the tested ceiling H (§4.4); conditionals (B1, B3) |
| Nuclear interactions (r = 22, 30, 61.5 mm) | reducible | 1.7×10⁵–1.2×10⁶ | ≈ 2–3×10³ | ≈ 3×10³ b | ≈ 3×10³ b | same, with real hadronic physics and a vertex veto (B1, B3) |
| Prompt pairs from the hard vertex ("PV pairs"); photon conversions; V⁰; loopers | reducible | 3.0×10⁶; 4.7×10⁶; 3.7×10⁶; 168 b | 1.4×10⁵ b; 4.0×10⁵; 3.1×10⁴; 168 b | 1.4×10⁵ b; 7.4×10⁴; 5.8×10³ b; 168 b | 1.4×10⁵ b; 6.5×10³ b; 5.8×10³ b; 168 b | **no separate terms in v2**: these particles come from the hard-scatter vertex and are in the real SM events of B4 (one route per origin, below) |
| Z(νν)+jets hard-scatter tracks | **irreducible** (real MET, tracks in the road) | 1.2×10⁹ | 9.6×10⁵ | 1.6×10⁴ b | 1.6×10⁴ b | hit-level sample ×5; 1.1×10⁷ no-pile-up events; the estimator of §4.4 on every candidate made by hard-scatter-vertex particles (B4) |
| W(τν), tt̄ 1ℓ | irreducible/reducible | 1–2.4×10⁸ | 0.5–1×10⁵ | ≈ 10⁴ b | 0.2–9×10³ b | hit-level samples sized for an evaluable closure; same estimator (B4) |
| 8 proxied processes (W(eν), W(μν), tt̄ 2ℓ, t-channel, tW, WW, WZ, ZZ) | irreducible/reducible | 2.8×10⁸ | 2.2×10⁵ | 2.3×10⁴ b | 2.1×10⁴ b | own hit-level samples (B4) |
| Z(ττ), lost-lepton Z(ℓℓ), multijets with fake MET | reducible / instrumental (fake MET) | absent | absent | absent | absent | new, with a reconstruction-level MET model (B4) |
| Cosmic muons, beam halo, beam gas | instrumental (non-collision) | argued, not in the sum | | | | number from public rates × pointing × timing (B7) |
| Several pile-up-vertex secondaries in one candidate; own-z placement of pile-up secondaries | instrumental | not in v1 (one vertex at a time, placed at the PV) | | | | own-z placement in B1; test B1-g, below |
| Noise hits; hits from neighbouring bunch crossings | instrumental | inside the top-up at first order | | | | public occupancy and readout window (R-18); B3-c for the timing layer |
| δ-rays, merged clusters | instrumental | not modelled [L8] | | | | bracketed by the resolution and inefficiency tests of B6; limitation |
| **B₈₄ total SR-G** | | 7.5×10¹⁰ | 1.5×10⁸ | 2.0×10⁶ | 1.2×10⁶ | pyhf model (T1) |

**One accounting route per particle origin [SD18].** In v1 the "PV-pair" rate of 30.3 per triggered event is the
number of pairs of prompt charged particles **of the hard-scatter event** whose mean φ lies in the road
[V: `S4/analysis/gen_d123.py` l.159-160, l.172-179, l.253], and the γ, V⁰ and looper rates are also "HS vertex only"
[V: `S4/analysis/normalise.py` l.84-110]. The same particles are in the real SM events that B4 simulates, so a term
for each would count them twice. v2 assigns every candidate to one term by the truth origin of the hits that make
its double-crossing layers (attribution rule, §4.4 point 3):

| origin of the hits | term | measured on |
|---|---|---|
| particles of the hard-scatter vertex that Fatras traces: prompt charged tracks (pairs, loopers), photon conversions, V⁰ and other Pythia decays | B4, one term per SM process | real SM events: no-pile-up pool and hit-level samples (§4.7) |
| products of a Geant4 vertex (decay in flight or nuclear interaction) of a hadron of the hard-scatter event or of a pile-up interaction | B1: DIF, NI at three radii | Geant4 vertex → Fatras: no-pile-up pool and overlays (§4.4) |
| particles of pile-up interactions that Fatras traces (their prompt tracks, conversions, V⁰, loopers) | B2 pile-up | pile-up-only events (§4.5) |
| fewer than half of the layers from any one origin ("mixed") | none; bounded by the completeness test of §4.4 | truth classes on overlays and hit-level events |

The classes are disjoint because every simulated hit has one truth parent. Fatras produces no hadronic interaction;
whether it decays charged pions and kaons is recorded with the physics list (B1-d) and switched off if on, so the
real events of B4 contain no B1 vertex, and Geant4 vertices are injected only into B1 samples. *Route check
(Phase 2, on the C1 Z(νν) hit-level sample, no extra CPU):* the truth conversions and V⁰ decays in the road per
preselected event are compared with v1's generator rates for Z(νν), 0.231 and 0.026 [V: `AN1/background.json` →
`cprime.<t>.rate.per_process`]. If Fatras real events lack a class (ratio below 0.5), that class goes back to a
B1-type gun term with its hard-scatter rate, and the pool is re-allocated before the freeze.

Readings that shape v2:
- The pile-up term dominates down to R06. From R07 on the leading terms are single-interaction and SM bounds that do
  not scale with pile-up (D2 §8.1). B1/B3/B4 therefore matter at least as much as B2.
- The bounds are not "1.14/M with M = 500–2000" (PLAN l.76). They are applied to conditional populations of
  M = 13 (γ), 24 (PV pair), 35 (PU), 81 (DIF, Z(νν)) up to 2,000 (D4 I6 [U]). The paper wording follows the record.
- "Measured down 4.9 decades from R04 to R07 by direct count" (PLAN l.166) is the patched central value. The direct
  count falls 5.37 decades (171.55 → 7.29×10⁻⁴ per trial), and at R06 and R07 it lies ×3.8 and ×4.5 *below* the
  patched value (D4 I7 [U]). v2 quotes the direct counts.
- SR-T and SR-G carry identical SM and single-interaction terms in v1: no time-tag credit was given
  (D4 §2.3 [U] `STAGE4_RESULTS.md` l.172). v2 measures this credit as a conditional ([SD6], item B3).
- **Pile-up-vertex secondaries (COM B1-g).** v1 already counts the decays in flight and nuclear interactions of
  pile-up particles: its DIF and NI rates are "HS + 200 × min-bias" [V: `normalise.py` l.84-110; `gen_d123.py`
  l.21-23, l.286-287], and the DIF rate differs by only 1.6 % between SM processes (1.5687 for WZ to 1.5945 for tt̄ 2ℓ
  per triggered event [V: `background.json` → `cprime.dif.rate.per_process`]), so the pile-up part dominates it. What
  v1 does not do: it places every such vertex at the primary vertex (`TT/acts/stage4/code/s4cp.py` l.115, `pv = vtx[:3]
  + …` [V]) and treats one
  vertex at a time. v2 therefore:
  1. keeps both shares in rate_t, recomputed with Geant4 and tabulated separately, and generates the pile-up share
     with its vertex displaced along z by the luminous-region spread relative to the PV of the plane hypothesis
     (the hard-scatter share stays at the PV);
  2. counts each secondary once: Geant4 secondaries of pile-up particles enter only through the B1 terms and are
     never added to the pile-up overlays or to the B2 samples, whose hit density stays normalised by the top-up;
  3. tests what one vertex at a time can miss, **in Phase 3 on 1,000 pile-up events with the Geant4 secondaries of
     all pile-up particles (17.5 CPU-h, a development sample)**. Candidates are classified by truth. The count
     attributed to secondaries at R04–R07 is compared with the B1 prediction N_trials × rate × P(r | t) for the
     pile-up share. Expected counts from v1: about 2,100 / 1,000 / 25 / 13 at R04 / R05 / R06 / R07 [E: 4,000 trials
     × 1.57 × (166, 81, 2, 1)/500, script [13]]. The multi-vertex class (candidates whose layers come from two or more
     distinct secondary vertices) is counted directly at every rung, with its trend in depth, not inferred from an
     excess on the total (only R04–R06 reach N ≥ 24). Rule, fixed now: if that class exceeds a factor 2 of the B1
     prediction for one vertex at a rung with N ≥ 24, or its share of the attributed count rises with depth beyond its
     error, it becomes a B1 term before the freeze, with its rate from this sample and the B1 estimator for its
     extrapolation; otherwise the B1 terms stand. The result is recorded before the freeze.
- *Noise and out-of-time hits:* v1's top-up (×2.3–7.3) scales the hit density to public occupancies from full
  simulation; the public noise occupancy and readout window are retrieved (R-18) and compared with the top-up; if
  they exceed it by more than 10 % the top-up is raised before the freeze, a detector-model reason. *δ-rays and
  merged clusters* are part of limitation [L8].

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
  factors of B1 are pass probabilities of any selection.
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

Table 4.0. Unit costs on a worker (i5-7500), at 4 jobs per node, with the CPU-h of the reduced variant that rest on
each and the Phase-2/3 measurement that fixes it (this table also serves §11.2). Provenance: **M** = measured in the
feasibility phase (JSON keys in `benchmarks_chain.json`, `benchmarks_generators.json`, `benchmarks_runner.json`);
**D** = derived from measured parts, or measured on one event or on toy inputs; **G** = guess, not benchmarked. The
contingency of §11.2 is sized from this column: 10 % of M, 30 % of D, 100 % of G.

| unit | cost | max RSS | output | source | prov. | CPU-h on it; fixed by |
|---|---|---|---|---|---|---|
| PU-200 event through the chain (Pythia overlay, Fatras, digitisation, seeding, CKF) | 13.5 ± 1.1 s (12.9 s alone) | 0.46 GiB | 0.52 MB with 4 trials | FEAS_A §3.3 [V] | M | — |
| plane-finder trial at ρ = 1, road 0.25, all per-trial work | 11.7 ± 1.1 s (find alone 10.8 s; 9.4 s with 1 job) | same job | — | FEAS_A §3.4 [V]; at the frozen road 0.15 perhaps ×0.77 [E, not measured] | M | all trials; day-0 timing at road 0.15 |
| "B1-type" event = chain + 4 trials | 60.4 s | 0.46 GiB | 0.52 MB | FEAS_A §1 [V] | M | — |
| ρ = 2 event (2 crossings, 2 trials) | 206 s | **1.46 GiB at 1 event** | 4.0 MB with dumps | FEAS_A §3.1, §3.7: one smoke event | D | 229; day-0 job with 1, 2, 4, 8 events per job |
| PU-200 row with one trial (signal row, overlay, hit-level SM event) | 25.2 s = 13.5 + 11.7 | 0.46 GiB | ≈ 0.5 MB | sum of measured parts; the injection mode itself is not benchmarked (FEAS_A open issue 6) | D | ≈ 1,350 (S1 561, hit level 524, overlays 123, C1 63, B6 59, pilot 7, development overlays 7); first injection and overlay jobs |
| no-PU single minimum-bias interaction | 11.5 ms | grows 12.6 kB/event | 8.2 kB | FEAS_A §3.6 [V] | M | — |
| no-PU hard-scatter event (generation with filter, shower, chain) | **45 ms** | — | — | 23.4 ms shower (FEAS_B l.117 [V]) + 14.1 ms for a 10-track gun through the chain (FEAS_A l.235 [V]) + 7.5 ms margin; the generation filter efficiency is not measured | G | ≈ 523 (pool share 457, pilot 29, multijet population 12.5, B6-c 25); day-0 timing job, 10⁴ events of Z(νν), W, tt̄ with the filter |
| Stage-3 string event, F 500, Λ = 1 / 3 / 5 keV | 0.65 / 18.8 / 67.8 s | 0.21 GiB | 4–8 kB | FEAS_A §3.5 [V], toy kinematics | D | 306 (+ 36 in B6); first Stage-3 chunk at 3 and 5 keV |
| Stage-3 event summed over the 8 grid Λ | 95.6 s | | | measured anchors (91 % of the sum) + v1 index shape × 2.14 for the other five Λ [E, script [1]] | D | (in the row above) |
| MG5 LO + Pythia shower + conversion | 34 ms per LHE event | 0.2 GiB | 0.72 + 1.05 kB | FEAS_B l.129, listed there as derived [E]; MLM 0–2 jets **not benchmarked**: 50 ms assumed | D / G | 24 (MLM, G); first chunk |
| Pythia (re-)shower, signal / Z(νν)+jet | 21 / 23.4 ms per event | 29 MB | — | FEAS_B Task 3 [V] | M | — |
| Pythia minimum bias | 2.0–2.5 ms per interaction | 25 MB | — | FEAS_B Task 3 [V] | M | — |
| NLO fixed-order K at one mass | ≈ 2 CPU-min (+ 3 CPU-min once per process) | 1.0 GiB | — | FEAS_B Task 4 [V], single runs | M | — |
| Geant4 π± gun, primary mode | 0.134 ms | 71 MB | — | FEAS_B Task 5 [V] | M | vertices at the measured yield (D): 98; spectra, I/O and two variations (G): 67; Phase-3 hand-over tests. The NI cost uses the all-tracker inelastic yield of 4.2 % per gun for a vertex at one radius; if a sixth of the vertices falls in a given slab, c_NI = 30.6 ms and the summed floor is 13.4 instead of 12.6 [E, script [9]] |
| pyhf: fit / asymptotic CLs point / 20-point scan / 1000 toys | 0.12 / 0.52 / 10.4 / 652 s | 105 MB | — | FEAS_C R9 [V], toy workspace with 31 parameters; the v2 workspace will have 60–100 [L4] | D (toys: G) | 183 (toys); timing on a 60–100-parameter workspace built from v1 counts |
| Argo overhead per job / SSH | 16.8 s / 2.4 s | — | — | FEAS_C R2 [V] | M | — |
| FxFx 2 × 20 CPU-h; V4-5 brute force and T_seed regression; development and re-analysis allowances | — | — | — | not benchmarked | G | 40; 74; 442 (allowances, fixed by no measurement) |

"CPU-h" below means slot-hours at these costs. The Stage-3 number for unmeasured Λ uses the v1 per-event CPU of the
tracked index (F 500, p2/BM: 0.037, 0.080, 0.212, 1.07, 2.53 s at 0.45, 0.6, 0.85, 1.5, 2 keV [V: `STAGE3_INDEX.json`])
times the ratio measured at the three anchors (87.3 s / 40.8 s = 2.14). These five Λ values carry 9 % of the sum, so
the interpolation is not what limits the estimate; the toy kinematics and the ×5–10 event-to-event spread are
(FEAS_A §3.5).

**Closure tests: common definitions (binding for B1–B5).**

*1. Derivation and test are disjoint.* Every closure test names (i) the sample and the rungs on which a correction,
a conditional or a model parameter is **derived**, and (ii) a **test** sample with different generator and pile-up
seeds, read at rungs that were not used for the derivation. A comparison at the derivation rungs, or between two
samples of the same construction at the same rung, is called a **consistency check**: it is reported, it can reveal a
bug, and it gives no verdict. The sample roles are in the inventory, §4.17.

*2. Statistic.* For a prediction P and a direct count N with exposure T: r = P·T/N. N is counted **after** the cut
under test (for weighted samples N is the effective count). σ_tot² = 1/N + s_P², with s_P from the event bootstrap of
the prediction (trials within an event are correlated).

*3. Evaluable rungs.* A test rung is **evaluable** for a tolerance F if σ_tot ≤ ln F / 3. In counts: N ≥ 55, 64, 121
for F = 1.5 and N ≥ 19, 20, 24 for F = 2, at s_P = 0, 0.05, 0.10 [V: script [11]].

*4. "Within a factor F" means all of the following (L = ln F).*
 (c) **Model width, fixed before the freeze and capped.** s_model is one number per estimator: the r.m.s. of ln r of
     that estimator on the development samples (Phases 2–3), or a larger declared value. It is the constant term of
     the closure nuisance (point 7) and is not changed after the freeze. **Cap: s_model ≤ L/3** (0.135 for F = 1.5,
     0.231 for F = 2). An estimator that performs as declared at the cap is truly outside the tolerance with
     probability 0.27 %. An estimator whose development r.m.s. is above the cap is **not submitted** to the test: by
     its own evidence it is not within a factor F, its factor has the no-credit value from the freeze on, and the
     pre-registration says so. Decision point 2 applies this rule after trying a redesign (§11.7).
 (a) **Tolerance, at every evaluable test rung:** |ln r| ≤ L passes; L < |ln r| ≤ L + 2σ_tot is INVESTIGATE;
     |ln r| > L + 2σ_tot is FAIL.
 (b) **Compatibility with the declared width:** the χ² of the vector of ln r over the evaluable test rungs against
     zero, with the covariance V = V_boot + s_model²·J, gives p_b. V_boot is the joint bootstrap covariance of the
     nested counts and the prediction; J is the all-ones matrix (s_model is one common width per estimator).
     p_b ≥ 0.05 passes; 0.05/K ≤ p_b < 0.05 is INVESTIGATE; p_b < 0.05/K is FAIL.
 **INVESTIGATE** opens a regression ticket, and the test is repeated **once** on the reserved fresh sample (§8). The
 fresh sample alone gives the verdict: PASS if |ln r′| ≤ L at every evaluable rung and p_b′ ≥ 0.05/K, otherwise FAIL.
 F is not a free choice per test: 1.5 for the pile-up estimators, the conditionals, the time tag and the sideband;
 2 for the single-interaction and hard-scatter estimators (v1's values, unchanged).
 **K = 10** is the number of tests whose FAIL can remove a selection (the eligibility family, fixed now): B1-a for
 DIF and for the three NI radii; B4-c for Z(νν), W(τ_h), W(τ_ℓ) and tt̄ 1ℓ; B2-a; B2-b. A test that the user orders
 under Q3 adds one to K. The ceiling tests of §4.4 form a second family that can remove selections: one combined
 verdict per term for the **T_c = 19 terms** with a ceiling (DIF, NI at three radii, fourteen SM processes,
 multijets), Bonferroni level α_c = 0.05/19 (§4.4 point 4).

 *Size and power of this rule at the declared widths* [V: script [11]]. Model: ln r = δ + ε, where δ is the model
 bias of the estimator at the test rung (the same in a re-test) and ε the statistical error (new in a re-test). An
 estimator that performs as declared has δ drawn from N(0, s_model²).

 | probability for an analysis whose estimators perform as declared | s_model = 0 | s_model = cap/2 | s_model = cap |
 |---|---|---|---|
 | one test, one evaluable rung at the evaluable limit: final FAIL | 0.52 % | 0.55 % | 1.07 % |
 | one test, two rungs with a common δ: final FAIL | | | 1.9 % |
 | battery of the 10 tests: at least one FAIL | 5.1 % | 5.4 % | 10.2 % (11.8 % with two-rung pile-up tests) |
 | battery: at least one FAIL that removes a selection (point 6) | 2.1 % | 2.2 % | 4.2 % |
 | ceiling family, every term at its boundary P = H: at least one false FAIL | 4.9 % | 4.9 % | 4.9 % |
 | **either family removes a selection** | **6.9 %** | **7.0 %** | **8.9 %** |
 | expected number of re-tests on fresh samples (closure family) | 0.45 | 0.45 | 0.45 |

 Power for a fixed true bias (one rung at the evaluable limit, s_model at the cap): the test is passed with
 probability 98.7 %, 90 %, 62 %, 26 %, 5.9 % and 0.07 % for |ln r_true| = 0.5, 0.75, 1, 1.25, 1.5 and 2 × ln F; with
 σ_tot at half the limit, 33 %, 0.8 % and below 0.01 % at 1, 1.25 and 1.5 × ln F. So an estimator at the edge of the
 tolerance passes in about half of the cases and one wrong by F^1.5 in 6 % or less.
 Limiting cases: s_model → 0 reduces (b) to a statistical compatibility test with a family-wise size of 5 %; σ_tot → 0
 makes the verdict a statement on δ alone. Check on a known failure: v1's thinning (ln r = +0.406, +0.474, −0.455,
 −0.954 at R04–R07 with σ_tot ≈ 0.01, D4 l.390 [U]) is beyond L + 2σ_tot = 0.425 at three rungs, which is FAIL, and
 its r.m.s. of 0.61 is above the cap, so it would not have been submitted [V: script [11]]. The paper reports this
 retroactive test. JFC's alarm band applies to (b): χ²/ndf < 0.1 is investigated as a possible tautology.

*5. Verdicts (four classes).*

| verdict | definition |
|---|---|
| PASS | at least one evaluable test rung; (a) and (b) pass, directly or in the one re-test; (c) holds |
| FAIL | (a) or (b) in its FAIL range, or the re-test of an INVESTIGATE case does not pass |
| NOT TESTED | no test rung is evaluable at the produced statistics (including "no direct count"), or the estimator was not submitted because its s_model is above the cap |
| NOT EVALUABLE | the test could not be executed: an input is missing, a [DT] downscope removed it, or one of the two quantities compared does not exist (for example B2-c when thinning has no effective counts) |

*6. What a verdict earns (the eligibility logic; stated only here, and §4.11 point 3, §4.12 rule 1, the
partial-outcome table of §4.12 and COM T2-a refer to it).*
- PASS: the estimator is used, with the closure nuisance of point 7.
- FAIL: the estimator is not used, and no scale factor patches it. If the failure is an **over-prediction** (ln r > 0)
  and the term's ceiling verdict (§4.4) is PASS, the ceiling H is still a valid no-credit value: the term enters at H
  and the selection stays eligible, flagged. If the failure is an **under-prediction**, a selection for which the
  term is leading is not eligible in T2 ([SD8], v1's rule). For the pile-up term both estimators must fail (§4.5).
- A failed conditional or time-tag fraction only loses its credit (it enters at 1).
- **Ceiling FAIL** (the term's combined ceiling test, §4.4 point 4): H is not a ceiling. The term has no valid
  no-credit value, and a selection for which it is leading is not eligible.
- **Completeness not PASS** (§4.4 point 4): on the development samples, a term whose estimator is to be credited gets
  its promotion sum extended to every deficit k > k_max with the correlated π_k (a decision-point-2 redesign).
  Otherwise, and on the test samples after the freeze, the term enters at the **extended ceiling
  H′ = P_geo + Σ_{all k} f_k** (π_k = 1 for every deficit, no credit), eligible and flagged; it is ineligible only if
  H′ itself fails its ceiling test. For SM processes H′ may exceed H by orders of magnitude; an EST from the C1
  Z(νν) development sample is a day-15 input, and a completeness not-PASS of a leading SM term is then in practice a
  loss of its selections.
- NOT TESTED, NOT EVALUABLE or not submitted (s_model above the cap): **no credit.** The untested factor enters at its
  no-credit value (a survival or promotion probability at 1, a conditional at 1, a time-tag fraction at 1; the term
  at its ceiling H if its ceiling verdict is PASS). The selection stays available in that form and is flagged "no
  credit" in the ladder figure and the result tables. **For a MUST criterion this is an exception to brief D4 that
  only the user grants: every route by which a MUST criterion ends so is listed in Q3 (§12.1) with its probability.**
- A term is never "leading or not" on the strength of a failed or untested estimate: "leading" (§4.11 point 3) is
  decided with the no-credit value, the same value that enters the likelihood. An untested estimator therefore makes
  a selection worse, by the credit it loses, and never better.
- For an analysis whose estimators and ceilings perform as declared, the probability that a false FAIL of either
  family removes a selection is **6.9–8.9 %** (point 4 table; closure family 2.1–4.2 %, ceiling family 4.9 % with every
  term at its boundary, less when the terms lie below their ceilings) [V: script [11]].

*7. Extrapolation width, always added.* For every quantity q that is carried beyond its last evaluable test rung
(thinning, the occupancy model, the promotion probability π_k, every conditional), the log-normal closure nuisance
at rung r has the width

  s_tot(r)² = s_model² + Σ_f s_f² + (b̂² + σ_b²)·d_in² + b₀²·d_out² .

 - *Distance.* Only rungs that change a cut on which q depends are counted. π_k and S depend on the counting cuts
   (R01–R04, R12–R14) and on the width (R05–R08); the fit-probability (R09–R11) and shape (R15–R20) cuts do not act on
   them and enter through conditionals. Thinning, the full occupancy prediction and a conditional (whose population
   changes at every rung) depend on every cut.
 - *Cumulative test rungs* are the held-out ladder rungs. d_in is the number of counted rungs between the last
   evaluable cumulative test rung and r inside the same cut family (counting R01–R04, width R05–R08, fit probability
   R09–R11, 2S R12–R14, shape R15–R20). With n evaluable cumulative test rungs in that family: for n ≥ 3, b̂ ± σ_b is
   the fitted slope of ln r against the rung index; for n = 2, b̂ is the two-point slope and σ_b := b₀; for n = 1,
   b̂ := 0 and σ_b := b₀.
 - *Crossing test rungs.* The cut of a deeper family f can be applied on top of a loose width, where candidates are
   plentiful: "R09⊗R05" is R05 plus the fit-probability cut of R09, and likewise for the 2S and shape cuts on top
   of R05 and R06. The direct sample has 4.8×10⁶ candidates at R05 and 2.4×10⁴ at R06; with v1's fit-probability
   fractions about 1,400 remain at R09⊗R06 and 130 at R11⊗R06 [E, script [11]]. A crossing rung is a test rung like
   any other: another sample than the derivation, the evaluable-rung rule, the tolerance F of the estimator and the
   verdict classes of point 5. It is defined for thinning (prediction against the direct count, B2), for the
   occupancy model **in the 2S family only**, for π_k (2S family, on overlays and hit-level events, B1 and B4) and for
   the conditionals (the stability test B3-d is one). The occupancy comparisons at R09⊗R06, R11⊗R06 and R15–R20⊗R06
   are **consistency checks with no distance credit** (Df-2): for those cuts the model takes its pass fraction from
   the finder candidates passing R06 in the development sample (§4.5), so the comparison sets one quantity against
   itself on two samples of the same construction at the same width, and the transfer of that fraction from an R06
   width to an R08 width is not tested. If the crossing test of family f is an evaluable PASS, the rungs of f are not
   counted in d_out, and the measured term s_f, the r.m.s. of ln r over the evaluable crossing rungs of f, is added
   once; the width step from the last crossing rung to R08 always counts in d. If it is a FAIL, the estimator is not used beyond the last rung before f. The trial records keep the
   fit-probability, 2S and shape variables of every candidate passing R05 (0.9 GB, §11.4). Cost: 5 CPU-h of
   re-analysis.
 - *d_out* is the number of counted rungs in families with no evaluable test rung of either kind, and b₀ = ln F of
   that estimator. **b₀ is a convention, not a measurement**: one tolerance per rung, coherent (linear in d_out). Its
   only anchor is the drift of v1's failed thinning, 0.36 per rung from R04 to R07 (D4 §3.3 [U]), against
   ln 1.5 = 0.405. It is used only where no crossing test is evaluable, and the paper says so.
 - *Where the form comes from.* Inside a tested family the tested rungs constrain a linear trend ln r = a + b·d. The
   prediction is not corrected by the fitted line (that would be a patch), so the possible bias b̂·d is carried as a
   width and the slope error σ_b·d is added in quadrature; the constant term is covered by s_model.
 - *Checks.* d_in = d_out = 0 and no crossing term give s_model. Planning values with s_model and every s_f at the
   cap [E, script [12]]:

   | quantity | R08 | R09 | R11 | R14 | R17 | R20 |
   |---|---|---|---|---|---|---|
   | occupancy model, no crossing test evaluable | 0.43 | 0.59 | 1.29 | 2.47 | 3.67 | 4.88 |
   | occupancy model, 2S crossing test PASS (no credit from the fit-probability and shape comparisons) | 0.43 | 0.59 | 1.29 | 1.30 | 2.47 | 3.68 |
   | **promotion π_k tested at R06 only** (expected: DIF at an enrichment below 4, every B4 term), no crossing test | 1.41 | 1.41 | 1.41 | 2.51 | 2.51 | 2.51 |
   | promotion π_k tested at R06 only, crossing test PASS in the 2S family | 1.41 | 1.41 | 1.41 | 1.42 | 1.42 | 1.42 |
   | promotion π_k tested at R06–R07 (conditional: DIF at an enrichment of 4 or more), no crossing test | 0.73 | 0.73 | 0.73 | 2.20 | 2.20 | 2.20 |
   | promotion π_k tested at R06–R07, crossing test PASS in the 2S family | 0.73 | 0.73 | 0.73 | 0.77 | 0.77 | 0.77 |
   | promotion π_k tested at R05 only (rung split, NI) | 2.09 | 2.09 | 2.09 | | | |
   | a conditional applied 2 / 5 / 7 rungs beyond where it was measured | 0.82 / 2.03 / 2.84 | | | | | |

   Checks of the new rows: R06 only means n = 1 (b̂ = 0, σ_b = b₀ = ln 2) and d_in = 2 (R07, R08), so
   √(0.231² + 0.693²·2²) = 1.41, and at R14 √(1.41² + 0.693²·3²) = 2.51; for d_in → 0 the width falls to s_model.
   In the expected case a promotion factor therefore carries 1.41 from R08 on, above the 0.8 beyond which a credit is
   worth little (§4.6); it is useful only if π_k itself is small. The pile-up term from the occupancy model is usable
   to about R09 whatever the crossing tests give.
   The R08 width is dominated by b₀ for the one untested width step. It falls towards s_model only with three
   evaluable cumulative rungs in the width family, which thinning can have if its R07 rung is evaluable (§4.5) and
   the held-out estimators cannot. Whether each crossing test is evaluable is measured in Phase 3 on the development sample and
   written into the pre-registration.
 - Two more things shorten a distance: an evaluable **agreement of two independent estimators** at a rung (B2-c)
   makes that rung the origin for both, with max(s_model, |ln ratio|) as the constant term; and a quantity that is
   **counted directly** at the deep rung (P_geo, f_k and H on no-pile-up samples) is not extrapolated.
 - *Censoring.* Every factor that is a probability (S, π_k, a conditional, the time-tag fraction) is censored at its
   no-credit value, φ = min(φ₀·e^θ, 1), in the fit and in every pseudo-experiment (§4.11 point 1). A credit can then
   never cost more than "no credit": for φ₀ = 0.1 and a width of 2.47 the mean is 0.31 with censoring and 2.1
   without [V: script [12]].

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
| signal E 200, 1.5 keV (fast path, as v1) | pass counts at R04, R06 (open tier); R07, FB2 (sealed tier, Q1) | 41, 33, 18; 9 of 200 [U: D4 §4.2-4.3; the arbiter read 9/200 and FB2 in `SUM`] | 400 rows | 4 |
| signal E 500, 3 keV (full chain, as v1) | R04 (open); R07, FB3 (sealed) | 61, 48; 11 of 200 | 400 rows | 3 |
| signal E 200, 2 keV (fast path, as v1) | R04 (open); R07, FB3 (sealed) | 45, 31; 10 of 200 | 400 rows | 3 |
| arithmetic (exact, not in N) | v2 code on the v1 recorded counts reproduces B, σ_ln per term and B₈₄ per rung | `AN1/bsum_wp.json` → `ladder` | — | — |
| Stage 3 (diagnostic, not in N) | hits per event and status fractions at the three points | e.g. 21,137 hits / 463 events at E 200, 1.5 keV [V: `STAGE3_INDEX.json`] | 463–492 events | — |
| route check (diagnostic, not in N; §2) | truth conversions and V⁰ decays in the road per preselected Z(νν) event | 0.231, 0.026 (v1 generator rates) | the Z(νν) hit-level sample | — |

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

**C1 and blinding (precise statement).**
The C1 signal counts are pass counts of *v1 selections* (R04, R06, R07 and the v1 fallback column) at the three
declared points, on twice the v1 statistics. **Six of the ten are also efficiencies of a v2 candidate selection**
(cycle-1 arbiter §2): the three R07 counts (R07 is in T2 family L),
and the three fallback counts, because the v1 fallback at these points is FB2/FB3 with no dE/dx, which is exactly T2
family F [V by the arbiter: `SUM` → `fallback_points`, `r_fb`, `e_adm = null`]. All three points lie in the 20-point
window of the T2 figure of merit. Looking at them before the closure verdicts is an exception to the blinding
invariant of brief §7. **Only the user can grant it; it takes effect only if approved at Gate A (Q1).**

*Default that this strategy follows if Q1 is approved as recommended: a sealed comparison.*
- **Open tier (4 quantities):** the pass counts at R04 (three points) and at R06 (E 200, 1.5 keV). R04 and R06 are
  not T2 candidates. They are still efficiencies of v2-generated signal and are correlated with every candidate
  (R07 ⊂ R06 ⊂ R04), so they too are part of the exception; their precision is 34 % (2σ detectable shift at R04,
  400 rows against v1's 200 [E, script [13]]).
- **Sealed tier (6 quantities):** R07 (three points) and the fallback (three points). One comparison script computes
  the pre-declared exact test for each (§ "Within statistical errors", item 1) and writes to the C1 report **only
  PASS or FAIL per quantity** (two-sided, no sign, no z-value, no count). The counts and p-values go to one file
  **outside the repository tree** (`/nfs/cajuela/jdochoa/quirks_v2/data/sealed/`), encrypted with a key that only
  the orchestrator holds (all agents run under one account, so file permissions alone would not protect it); its
  sha256 is recorded in the ledger. The family-coherence z of the signal families and the global χ², which contain
  sealed quantities, are reported as PASS/FAIL only. The script is run by a dedicated
  agent that has no other role in Phases 2–4a; no agent or log reads the sealed file before the closure verdicts are
  recorded (it is opened at Gate B and printed in the paper's reproduction appendix). The twin-ratio diagnostic at
  the fallback is sealed in the same way; at R04 it is open.
- **If a sealed quantity returns FAIL**, the family is investigated first with the open tier and with the background
  families. Opening the sealed file before the verdicts needs the user's decision at that moment.
- *What this costs in validation power:* none in the statistical test (the same exact test on the same counts). What
  is lost before Gate B is the reading of the numbers: a FAIL cannot be diagnosed from its size or sign, and the
  "gross check only" label of the fallback counts (detectable shift 80 %, script [13]) is all the reader has. The
  global χ² over the 41 comparisons is computed by the same script and reported as one PASS/FAIL.
- **Frozen from Gate A on, in every option:** the full list of 16 T2 candidates (§4.12). The pre-registration may
  not add, remove or re-define a candidate; a background-method reason to do so goes to the user.
The options the user is asked to choose from, with what each costs, are in Q1 (§12.1).

*Signal quantities that exist before the closure verdicts (complete list; COM BL-1).*
1. The C1 quantities above, under the tier approved in Q1.
2. **The acceptance A = ε_fid × ε_trig × ε_presel, f₂₀₀ and the migration fraction m_mig** (S1-f), per species-mass.
   They do not depend on the plane selection: they are the same numbers for all 16 T2 candidates, so they cannot
   steer the choice. They are declared here as a second, selection-independent exception and listed in
   `PREREG_v2.md`. f₂₀₀ is a generator-level ratio and is computed in Phase 2 (brief Phase 2 requires it). A and
   m_mig need the trigger and offline MET, which in v2 come from the MET model, and S1 needs A to decide which
   events to propagate [SD10]; they are computed **once**, in the order given below.
3. Nothing else. In particular: no other rung count for signal; no distribution of a variable for matched signal
   candidates; no response of the vertex veto or the time-tag split to signal; no efficiency at any v2 candidate
   selection outside item 1; no signal quantity at the other 37 points; no B6 efficiency ratio (its nominal ε comes
   from B6's own nominal rows, paired with the varied ones, and is formed after the verdicts, §4.9); and no "V4-5
   optimality" count on signal rows (moved to Phase 4c, §4.2).
- *Order (days after Gate A; no step is repeated after a later one).* (1) retrievals R-3 and R-2, days 0–5;
  (2) MET model built and externally validated (§4.7), by day 10; (3) decision on the offline MET threshold from the
  public trigger curve (§4.14 (d)); (4) A and m_mig computed once on the Stage-2 samples, day 12; (5) decision on
  the generator cut, 200 or 150 GeV (§4.13); (6) Stage-3 string propagation of the accepted events, days 12–19;
  (7) the freeze.
- *Separation.* The C1 rows use their own seed stream and are never part of the S1 sample. The T2 candidate list and
  figure of merit are fixed in this document, before any C1 number exists.
- The C1 signal sample stays at 400 rows per point and not the 1,000 proposed in D4 [SD3].

**Other criteria.** (i) Linux reproducibility of the environment: lockfiles tracked, container recipe built and one
C1 job rerun inside it with identical output hash. (ii) Jobs ≤ 30 min, resumable, through `tools/runner` (FEAS_C PASS).
(iii) Pythia pinned to 8.312 for pile-up and SM, 8.313 for the signal shower, as v1 (D1 §2).

**Statistics and cost.** 198 CPU-h [E, script [3]]: ρ = 1 4,000 × 60.4 s = 67; ρ = 2 1,000 × 206 s = 57; C′_PU 5,000 × 25.2 s = 35;
Z(νν) 2,000 × 25.2 s = 14; signal 1,200 × 25.2 s = 8; full-chain twins 800 × 25.2 s = 5.6; Stage 3 at three points 3.6;
no-PU 1.7; generator level 5. The cost is the same in every option of Q1.
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
| **T_seed stability** (4 → 2) | the G3 metric of v1: per-trial pass fraction of each rung family (counting R04, width R05–R06, χ², 2S) at T_seed = 4 and 2, on 500 ρ = 1 events (2,000 trials) and 200 ρ = 2 events, from stored hit dumps | \|z\| < 2.73 for every family at both densities (Bonferroni over the 8 tests, family-wise 4.9 %; \|z\| < 2 each would call a converged finder "not converged" in 31 % of the cases, script [11]) | T_seed stays 4 (no retuning in v2); the paper reports "seed threshold not converged, pass fraction changes by x %" as a limitation; the same finder is applied to signal and background, so this is an efficiency statement, not a bias |

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

### 4.4 B1 — decays in flight and nuclear interactions; the estimator and its tested ceiling (MUST, Phases 2, 3 and 4a)

**Scope.** After the one-route rule of §2, the *terms* of B1 are decays in flight (DIF) and nuclear interactions at
r = 22, 30 and 61.5 mm (NI), each with a hard-scatter share and a ×200 minimum-bias share. The *estimator* of point 4
is also the estimator of the hard-scatter terms of B4. The v1 gun topologies PV pair, γ, V⁰ and looper are not terms
any more; 1,000 unbiased full-pile-up events of each are kept as completeness and diagnostic populations, because
they are enriched in candidates of the hard-scatter kind. They have no ceiling test: no no-pile-up sample of their
own exists, and a comparison with the same events' no-pile-up states would be paired, i.e. the leak count (default of
the verdict, P4 (iii); the costed alternative is a paired test on a small no-pile-up gun sample per sub-topology).

**Method.**
1. *Physics.* Geant4 11.4.3 with FTFP_BERT on the same cylinders, discs and slabs as the ACTS geometry, generated from
   the one tracked source `TT/acts/geometry/cms_phase2_public.json` (FEAS_B "Geant4 build and integration plan").
   Geant4 tracks each primary (π±, K±, p, K⁰_L, n, γ) in 3.8 T and records every inelastic interaction, decay or
   conversion with all products. Conversion products are **not** injected into B1 samples: by the route table of §2
   conversions belong to B4 and B2, where Fatras makes them; a primary γ enters B1 only through a photonuclear
   interaction, which counts as NI. Geant4 runs per worker from local scratch (deviation V13); the environment is
   installed on all three workers (commit 199e166).
2. *Hand-over.* The products are written as rows of the v1 particle array (vp, vsec, pdg, q, m, x, y, z, t, px, py,
   pz), which v1's `ParticleSource` already injects into Fatras with their own vertex (D5 §5 [U] `run_chain.py`
   l.79-112). The parent's hits up to the vertex come from Fatras with v1's `Truncate`. The finder therefore sees the
   same detector model as everywhere else. Two hand-over variants (Fatras-truncated parent; Geant4 parent crossings
   converted to hits) are compared on 100 events in Phase 3 and one is frozen.
3. *Which candidates belong to a term (attribution rule, COM B1-f).* Pile-up-only planes pass R05 at 49.7 per trial
   (§4.1 table), so direct counts on samples with pile-up are attributed by truth. Let n(r) be the number of
   double-crossing layers that rung r requires and j the number of the candidate's double-crossing layers whose two
   hits come from particles of one origin class of §2. The candidate is **attributed** to that class if j ≥ n/2,
   **mixed** if 1 ≤ j < n/2 for every class, and **pure pile-up** if j = 0 for the hard-scatter and Geant4 classes.
   Attributed candidates are the term, pure pile-up candidates are B2, and mixed candidates belong to no term: the
   completeness test below bounds them. v1 used attributed counts (D4 l.196 [U]); its coded rule is transcribed in
   Phase 2 and printed in the pre-registration. C1 uses v1's rule, and the difference is measured on the C′_PU samples.
4. *Estimator.* The no-pile-up state of an event of term t is classified **on subsets of the term's own hits**, not
   on the finder's single no-pile-up candidate. For rung r, a width-only pass over those hits finds the ribbon
   through the PV in the road, of the width of r, that holds the most double-crossing layers. The deficits are
   counted per layer type: k_IP = max(0, n_IP(r) − N_IP2), k_2S = max(0, n_2S(r) − N_2S2), k = k_IP + k_2S (the fixed
   cut N_IT2 ≥ 3 is a cut on a subset of the IP layers and is part of k_IP). f₀(r) = P_geo(r) is the probability of
   k = 0, and f_k(r) that of a deficit k, for k = 1 … k_max = ⌊n(r)/2⌋ ("near-pass"). At the counting rungs R01–R04,
   where the ladder has no width cut yet, the width is the finder's maximum core width (frozen configuration,
   transcribed in Phase 2); at R12–R14 it is the R08 width. With pile-up,

     P(r | t) = [P_geo(r)·S(r) + Σ_{k=1…k_max} f_k(r)·π_k(r)] · S_CKF(r) ,

   where S is the probability that a passing event still passes when pile-up hits are added (survival), and π_k the
   probability that pile-up supplies the missing layers (promotion). This is the law of total probability over the
   no-pile-up classes. It is complete for attributed candidates **for the cuts that are monotone under added hits**:
   the term's own hits of an attributed candidate lie inside its ribbon and make at least n − k_max of its layers, so
   the event is in a class k ≤ k_max by the subset definition, whatever the finder chose without pile-up. The fixed
   cuts and their behaviour when pile-up hits are added:

   | cut | monotone under added hits? | how H treats it |
   |---|---|---|
   | layer counts N_IT2, N_IP2, N_2S2 (R01–R04, R12–R14) | yes: added hits can only add double-crossing layers to a ribbon | applied in the classes (k per layer type) |
   | core width w_core (R05–R08) | yes: the widest-holding ribbon of a superset of hits is at least as good | applied in the classes |
   | road (Δφ(n₃, MET) < 0.15) and barrel (\|η(n₃)\| < 1) | yes for the subset search, which runs only over ribbons inside road and barrel | applied as the search region |
   | finder seeding and grouping | not used: the subset definition replaces the finder's choice | — |
   | fit probability (R09–R11), shapes h, o (R15–R20) | no | not in H; conditionals of B3, at 1 when untested |
   | CKF removal of helical tracks before the finder; f_CKF < 0.2 | **no**: pile-up lowers the CKF efficiency for the term's own tracks and dilutes f_CKF, and can also absorb own hits into fake tracks | **default Df-9, option (a):** H is classified on **all own hits**, before CKF; CKF removal and f_CKF < 0.2 enter as a survival-type factor S_CKF(r) |

   *S_CKF (Df-9).* S_CKF(r) is the probability that a candidate of the own-hit classification survives CKF removal
   and the f_CKF cut with pile-up. It is credited only where it is tested (attributed candidates: for DIF on the
   enriched test overlays with their weights, derivation R04–R05, test R06 and R07 where evaluable; for NI by the rung
   split, derivation R04, test R05; for each SM process on its hit-level halves, derivation R04–R05, test R06). S_CKF
   is a survival factor conditional on the no-pile-up class, so the selection of the enriched overlays on that class
   does not bias it; the restriction to unbiased samples applies to the ceiling and leak tests only. It carries
   s_tot(r) of §4.0 point 7 beyond, and is censored at 1. H classified on all own hits is then a true ceiling for every cut of the table, at the price of a
   larger H: it counts own-hit configurations that CKF would remove. The alternative (option (b)) applies CKF at its
   pile-up-200 efficiency inside H, measured on the same samples, with a width. Planning EST for Z(νν) at R08
   [E, script [9b]]: v1's attributed hard-scatter rate with pile-up, after CKF, is 0.0162 per event at R06 (4.51 at
   R05, a fall of ×278); two more width steps at ×100–300 each give H_CKF(R08) = 1.8×10⁻⁷–1.6×10⁻⁶, m_H = 2–18 in the
   1.1×10⁷ pool events. Under option (a), H = H_CKF/(1 − ε_pair), where ε_pair is the probability that CKF removes a
   passing own-hit configuration (assumed 0.8–0.98, not measured): m_H = 10–90 at ε_pair = 0.8, 20–180 at 0.9 and
   100–890 at 0.98. These are the m_H ranges of Table 4.4c; they apply the pile-up fall per width step to the
   hard-scatter rate. With the conversions' own fall (×6.5) the conversion part alone gives m_H ≈ 1.6×10³ for Z(νν) at
   R08 (≈ 3×10² in the pilot) (after CKF; ×1/(1 − ε_pair) on all own hits), far above the day-15 limit (≈ 12 Z(νν) pilot counts, script [9b] v9 table; in the result, the class B₅₀ = 300 is m_H ≈ 125 pool counts if Z(νν) alone sat at its ceiling) [E, script [9b]]. S_CKF then decides how much of
   H the term keeps.
   - **No-credit ceiling.** Since S ≤ 1, π_k ≤ 1 and S_CKF ≤ 1: P(r | t) ≤ **H(r | t) = P_geo(r) + Σ_k f_k(r)**,
     classified on all own hits (Df-9). H is counted on the no-pile-up sample at every rung. It applies the counting
     and width cuts only; the fit-probability and shape cuts enter through the conditionals of B3, and an untested
     conditional is 1, so for an untested term H is flat from R08 to R11 and from R14 to R20.
   - **Ceiling test (one-sided), only on unbiased samples.** At every rung with attributed direct counts, the hypothesis
     "attributed rate ≤ H" is tested with the exact conditional test for two Poisson counts (N_d attributed counts in
     the exposure T against m_H ceiling counts in M no-pile-up events), giving p_r. Samples: DIF at R04–R07 on its
     **1,000 unbiased test overlays** (the 4,000 enriched overlays are drawn from passing and near-pass events only, so
     a candidate from outside every class cannot occur in them; they serve only the S and π_k closure); NI at R04–R05
     on their unbiased test overlays; each SM process at R04–R06 on its hit-level test half (R04–R05 at 1,000 events);
     multijets at R04–R05 on theirs. The test does not use S or π_k, so R04–R05 are valid test rungs for it. **One
     verdict per term** (P6): p_t = 1 − (1 − min_r p_r)^n_r over its n_r evaluable rungs (Šidák; conservative for
     nested rungs). With T_c = 19 terms and α_c = 0.05/19 = 0.0026: p_t < α_c is FAIL (§4.0 point 6); α_c ≤ p_t < 5α_c
     is INVESTIGATE, with one re-test on a fresh unbiased sample (§8), FAIL if p_t′ < α_c; otherwise PASS. A true
     ceiling at its boundary fails with probability 0.27 % per term, and at least one of the 19 with 4.9 % [V: script
     [11]]. *Weighted samples* (p̂T-sliced multijets, preselection-weighted SM counts): N_d is replaced by the effective
     count N_eff = (Σw)²/Σw² and T by T_eff = N_eff/r̂ with r̂ = Σw/T, so the rate is unchanged and the Poisson test
     sees the right precision; for equal weights w, N_eff = N and T_eff = T/w. Substitution: 8 counts in 4,000 events
     against H = 5×10⁻⁴ (500 counts in 10⁶) give p_r = 0.0011; against H = 2×10⁻³, p_r = 0.55. Limiting case: a very
     large H always passes [V: script [11]].
   - **Completeness test.** On the same unbiased samples at R04–R06, by truth: (i) the *leak* fraction, attributed
     passers whose own no-pile-up event is in no class k ≤ k_max. By the attribution rule (j ≥ n/2 implies k ≤ ⌊n/2⌋)
     the leak is zero for a correct implementation: it is an **implementation check**, not a physics test.
     (ii) The *mixed excess*: on the same events a **paired pile-up-only finder pass** with the term's hits removed
     (P5, R5; 62 CPU-h: the 4,000 unbiased B1 test overlays and 1,000 test-half events of **each of the fifteen SM
     processes**, script [3]); mixed excess = mixed(with the term) − mixed(term hits removed), over attributed
     candidates. Pre-declared bound (a convention): the one-sided 95 % upper limit of
     (leak + mixed excess)/attributed is at most 0.26 (= 2^(1/3) − 1, the scale ln F/3 of the tolerance F = 2) at the
     deepest rung of R04–R06 with at least 30 attributed passers, and the ratio does not rise with depth beyond its
     error. PASS: the term is multiplied by c_mix = 1 + that upper limit (between 1 and 1.26), always, so a passed
     test cannot under-cover. Not PASS: §4.0 point 6 (a redesign on the development samples; otherwise the extended
     ceiling H′). *Development samples (Phase 3, results fixed before the freeze):* DIF on 1,000 unbiased Geant4 DIF
     overlays (sample 13a, 7 CPU-h; C′_PU has no Geant4 and serves C1 and, for the conversions, the development estimate of a Q2 (c) redesign (if the rider is taken, its 1,000 γ overlays on the v2 chain are the preferred sample), §11.7 rule 1), NI at R04–R05 on the pilot's unbiased
     no-pile-up NI events with the same overlay procedure inside the development allowance, and the hard-scatter
     estimator on the C1 Z(νν) hit-level sample (sample 5); the paired pass on them runs inside the Phase-3
     development allowance. The expected mixed fraction from these samples is a dated input of decision point 2
     (§11.7). The pure-pile-up rate in these events against the B2 rate is a consistency check only.
   - **Survival.** S is used as a measured number only at rungs where it passes its test; beyond them **S = 1**.
   - **Promotion.** π_k(r) is the joint probability that pile-up supplies the k_IP and k_2S missing layers inside a
     ribbon of the rung's width. It is taken from the occupancy model of B2 **with its measured layer-to-layer
     correlation factors**, not as a product of independent layers: one soft or looping pile-up track crosses
     several adjacent layers. *Per-k comparison (Phase 3, rule fixed now):* on the **pilot's 1,000 near-pass overlays
     (sample 11)**, the only pre-freeze overlays of near-pass events, split by k, the observed promoted fraction is
     compared with π_k at R04–R05; it runs once the occupancy model's R04–R05 inputs exist, at the latest by day 14. The r.m.s. of ln(observed/predicted) over the classes with at least 24 promoted
     events is the s_model of the promotion model. Expected [E]: 4–8 classes (k ≤ k_max per layer type), 125–250 events
     each; a class reaches 24 promoted events if its π_k is above 0.10–0.19, which the dense R04 occupancy makes likely
     for the small deficits, so 2–4 classes are expected to qualify. If fewer than two qualify, the promotion model is
     "not submitted" and the term enters at H; the 4a derivation overlays (sample 19) then refine only the post-freeze
     S. Above the cap of 0.231 the model is not submitted either (§4.0 point 4 (c)). Beyond the test rungs π_k carries
     s_tot(r) and is censored at 1.
   - Limiting cases: no pile-up gives S = 1, π_k = 0 and P = P_geo·S_CKF, the direct no-pile-up count after CKF;
     pile-up so dense that every layer is filled and CKF is blind gives P = H.
   The background term is B_t = N_t × c_mix × min(P(r | t), H(r | t)), with N_t = N_trig × rate_t (for a B4 term, the
   N_trig of the process).
5. *Biased generation (COM B1-e).* Only stiff configurations can pass a ribbon width of 4.7–9.4 mm. Primaries are
   sampled with a known weight that favours high p_T and directions inside the road, and Geant4 cross-section
   biasing (factor k, weight 1/k) is used in the tracker volumes. The soft bulk is excluded by an **analytic**
   bound: a track of transverse momentum p_T in the field B has radius R = p_T/(0.3·B) (m, GeV, T) and a sagitta
   L²/(8R) over a lever arm L, so below a threshold p_T its hits cannot lie inside the width cut; the threshold
   includes a stated allowance for multiple scattering. The bound is a geometric statement about helices, not a
   measured zero. It is *checked* on the unbiased sample at R05–R06, where counts exist, and the weights are checked
   by comparing biased with unbiased generation at R05 (criterion of §4.0, F = 1.5, on disjoint samples). Residual
   leakage through non-Gaussian scattering tails is a declared limitation of the Fatras scattering model.
   Biased generation is used for every term whose weights closure passes; the pool is then re-allocated as
   M_t ∝ √(N_t/(c_t·G_t)) with the measured gains G_t, a rule fixed here and printed in the pre-registration.
   **The gain is not measured yet.** If the generated interaction has no preferred direction with respect to the
   road, testing every non-overlapping road orientation multiplies the exposure by at most 2π/0.30 = 20.9 [E,
   script [9]]; the stiffness gain needs the particle spectra. The **Phase-2 pilot** (61 CPU-h) measures: 10⁷
   minimum-bias interactions at generator level (6.9 CPU-h: spectra, rates, stiffness gain); 10⁶ unbiased
   no-pile-up events each for DIF and the three NI radii, each with its Geant4 vertex (12.8 + 6.0 CPU-h: f_k and H at
   R04–R09, the check of the bound, the enrichment 1/H); **2.3×10⁶ no-pile-up Z(νν)+jets events (28.8 CPU-h): H of
   the largest term at every T2 candidate, one count being 10.9 events in 3 ab⁻¹**; and 1,000 overlays of near-pass
   events (7 CPU-h: the per-k promotion comparison). Until then every number in this document assumes G = 1.
   The pilot's no-pile-up jobs keep the full hit records (≈ 52 GB at 8.2 kB per event [E, script [8]]; more for the
   hard-scatter events), not only per-event summaries. They are classified by channel (i) as its first Phase-3 task
   (own-hit classes, k per layer type, all own hits, Df-9), provisionally by day 7 and with the frozen hand-over variant
   by day 12; the 1,000 near-pass overlays (7 CPU-h) are made from that classification.
   *Reading of the pilot (fixed now).* At the R08–R09 widths the pilot expects few counts (Z(νν): 0.4–3.7 at R08 with
   CKF, 2–190 under option (a) of Df-9 (pile-up fall; ≈ 3×10² after CKF, ×1/(1 − ε_pair) more on all own hits, if the conversions keep v1's fall) [E, script [9b]]; for the pile-up-fall case the conversion counts alone give a different expected pilot count, the (α1) row of the v9 table of script [9b]: the two estimates are not reconciled, both EST). H at a T2 candidate enters the day-7 and day-15 projections
   as Gamma(m + 1) of the pilot count m (a pilot zero is a bound of 12 events for Z(νν) itself and of 21 events for all SM hard-scatter processes and the multijets, which the day-15 rule reads through the same count; with the other pilot counts at zero the day-15 limit is at ≈ 12 Z(νν) pilot counts (script [9b], v9 table)). The branch of rule 3 of
   §11.7 is set by the populated **R06–R07 pilot counts**, extrapolated in width with the fall per width step that
   the pilot itself measures between R05, R06 and R07, labelled EST.
6. *Rates.* rate_t per triggered event is recomputed from Geant4 on the Pythia particle spectra, separately for the
   hard-scatter share and the ×200 minimum-bias share (§2), and compared with the v1 generator rates: DIF 1.59;
   NI 0.098 (22 mm) and 0.124 (30 and 61.5 mm), each × 0.22, v1's "PV-line factor" (the probability that the
   interaction lies on the line of the plane hypothesis) [V: `AN1/background.json` → `cprime.<t>.rate.value` and
   `.pv_line_factor`; `S4/analysis/wp.py` l.40 `P_PV_LINE = 0.22`, citing `WP_RULE.md` §4.1 l.318-320]. These are
   the rates of Table 4.4a and of the script (one rate set).

**Sample sizes and the floor they leave.** For a term with normalisation N_t and M_t simulated events, a zero count
allows N_t/M_t × 1.14 events at 68 % (§4.11). Table 4.4a gives this for every term, with M_t from one pool of
665 CPU-h shared between the B1 samples and the fourteen SM hard-scatter samples of B4 (the twelve processes of v1
and the two additions Z(ττ) and lost-lepton Z(ℓℓ); multijets have their own loose population, §4.7). The pool is
allocated as
M_t ∝ √(N_t/c_t), which minimises Σ N_t/M_t at fixed cost (Lagrange condition); c_t is the full cost per event: 45 ms
for a hard-scatter event, and 11.5 ms of chain plus the Geant4 guns for one distinct vertex per event for the B1
terms (a gun gives a decay vertex in 1.1 % and an inelastic vertex in 4.2 % of the cases, 0.134 ms each, FEAS_B
Task 5 [V]).

Table 4.4a. Zero-count floors, events in 3 ab⁻¹, before any pile-up factor, conditional, time-tag credit or
completeness allowance, at G = 1 [E, script [9]; N_trig and its breakdown from `AN1/bsum_wp.json` → `n_trig` [V];
rates as in point 6; the N_trig of the three additions are planning values, E].

| term | N_t | cost per event (ms) | M_t planned | transfer factor N_t/M_t | floor at 68 % (1.14·N_t/M_t) |
|---|---|---|---|---|---|
| decays in flight | 6.51×10⁷ | 23.7 | 2.44×10⁷ | 2.67 | 3.04 |
| NI at 22 / 30 / 61.5 mm | 8.83×10⁵ / 1.12×10⁶ / 1.12×10⁶ | 14.7 | 3.61 / 4.06 / 4.06×10⁶ | 0.24 / 0.27 / 0.27 | 0.28 / 0.31 / 0.31 |
| **DIF and NI, sum (B1)** | | | 3.61×10⁷ | | **3.9** |
| Z(νν)+jets | 2.51×10⁷ | 45 | 1.10×10⁷ | 2.28 | 2.60 |
| W(τ_h) | 5.41×10⁶ | 45 | 5.10×10⁶ | 1.06 | 1.21 |
| W(eν), tt̄ 1ℓ, W(τ_ℓ), W(μν) (each) | 2.2–2.5×10⁶ | 45 | 3.3–3.5×10⁶ | 0.68–0.73 | 0.78–0.83 |
| tW, tt̄ 2ℓ, WZ, WW, t-channel, ZZ (each) | 1.0–2.6×10⁵ | 45 | 0.71–1.12×10⁶ | 0.15–0.23 | 0.17–0.26 |
| Z(ττ) [E: 0.17 × 0.1 × N_Z(νν); range 10⁵–1.3×10⁶] | 4.3×10⁵ | 45 | 1.43×10⁶ | 0.30 | 0.34 (0.16–0.61) |
| lost-lepton Z(ℓℓ) [E: 0.34 × 3.5×10⁻³ × N_Z(νν); range 10⁴–10⁵] | 3.0×10⁴ | 45 | 3.8×10⁵ | 0.08 | 0.09 (0.05–0.17) |
| **SM hard scatter, sum (B4 pool)** | | | 3.65×10⁷ | | **8.6** |
| **all pool terms** | | | 7.3×10⁷ | 11.0 (sum of means) | **12.6** (12.2–13.3) |
| multijets, own loose population [E: N_MJ = 4×10⁵, 1 % of N_trig; range 0.1–10 %] | 4×10⁵ | 45 | 10⁶ | 0.40 | 0.46 (0.05–4.6) |
| **all terms** | | | | 11.4 | **13.0** (12.2–17.8) |

The planning N_trig of the additions [E]: Z(ττ) = r_ττ × f_MET × N_Z(νν), with r_ττ = B(Z→ττ)/B(Z→νν) = 0.17 (the
review's planning number, [U]: no branching fraction is in the repo) and f_MET = 0.1 (0.024–0.3) the fraction with
MET_reco > 250 GeV after the lepton veto; lost-lepton Z(ℓℓ) = 0.34 × f_lost × N_Z(νν), with 0.34 = 2 × 0.17 =
B(Z→ℓℓ)/B(Z→νν) for ℓ = e, μ (planning number, [U]) and f_lost = 3.5×10⁻³
(1.2×10⁻³–1.2×10⁻²); multijets 1 % of N_trig (0.1–10 %; v1 lists them as "UNVERIFIED <~1-2 % each", `AN1/bsum_wp.json`
→ `n_trig.not_included` [U]). All three are guesses until the MET model gives N_trig at
day 12; **the pool shares are then re-allocated** by the same rule (§11.7). N_trig itself is kept at v1's 4.0848×10⁷;
the two Z additions raise it by 1.1 % at the planning values; with the multijets at 1 % it is 2.1 % [E: 1.1 % +
4×10⁵/4.08×10⁷ = 1.0 %]. Without a pool share the two Z additions would be direct
bounds on 2,000 hit-level events: 243 and 17 events (57–741 and 6–57); with it they cost 18 and 5 CPU-h of the
same 665 CPU-h. Keeping the version-3 summed floor of 11.7 instead would need 715 CPU-h (+50; +26 to +88 over the
ranges), which is not proposed [E, script [9]].

Readings.
- The sum of 68 % upper values over-covers. The predictive distribution of the summed floor (each term N_t/M_t times
  an exponential variable, §4.11) has median 10.8 and 16–84 % range 7.7–15.2 [E, script [9]]. Its total σ_ln is 0.34:
  small because nineteen independent bounds are summed, not because anything was measured (§4.11 point 3).
- The floor falls as 1/CPU: 10.2 events for the pool terms with the day-15 reserve added to the pool (822 CPU-h,
  §11.7) and 6.3 at twice the pool. Reaching 1 event by size alone would need about 8.4×10³ CPU-h, which is the
  brute-force growth the plan discards (brief D8) and is not proposed.
- The SM part rests on the guessed 45 ms per no-pile-up event: at 90 ms the summed pool floor is 20.8 (SM 15.7)
  [E, script [9]].
- These floors apply to **both categories** unless the time-tag fraction of B3 passes its test. They apply to a
  term that enters at its ceiling H only if H also counts zero; otherwise Table 4.4c applies.
- Biased generation divides the floor of a term by its gain G. A summed pool floor of 1 and 0.11 events needs G = 13
  and 114 applied to every term [E, script [9]]. Conditionals with counts multiply a zero-count P_geo (§4.11 allows
  one zero per term); their values do not exist yet.

**Projection per outcome (findings N7, P1, P2).** The projection of **every term of the likelihood** is
**max(zero-count floor, N_t·H)** if it is expected at its ceiling, and the pile-up term is added with its
extrapolation width. Table 4.4c gives the one-bin expected CLs limit on the signal yield for the summed predictive
distribution and the reach read from the plan's table at equal expected limit.

Table 4.4c. Projection at an R09-like selection [E, script [9b]; reach: PLAN l.121, σ_ln = 0 row, EST, v1
placeholder efficiencies, best Λ per mass]. Every row contains the floors of Table 4.4a, the multijets at their
planning floor and, from the second row on, the EST pile-up term (median 7 events at R09, s_tot 0.59, censored at the
predictive draw of its no-credit bound, 426 × Exp(1)). m_H is the number of **simulated** ceiling counts of Z(νν) in its
1.1×10⁷ pool events; one count is 2.3 background events in 3 ab⁻¹. *Caption caveats:* the plan's reach row is the
book's reach at its own efficiency (best Λ per mass, v1 fast-path efficiencies that v1 measured ×1/0.87 high), so
applying it to an R09-like background assumes that the R09 efficiency equals that efficiency, a bias of either sign;
the reach is the median, then the 84 % edge of the band (the conservative value) in brackets. *Statistics-only:* the
rows carry the counting widths and the pile-up width, not the normalisation nuisances of §4.7 (generator difference
≈ 0.17 for the SM terms, K, luminosity, material), which act on every counted term. Script [9b] v6 lines give the
effect: (α1′) below 243 GeV already at a width of 0.03 (84 % edge); (α1) without credit, 84 % edge 372–312 GeV;
m_H = 100, 454 GeV. These rows are the projection of the result (after the freeze, with the credits stated per row; the
(α) rows after CKF, as v1 counted them). The reading of the day-15 rule, which admits none of these credits and is computed on the pilot's exposures, not on these pool floors, is the v9
table of script [9b], quoted in Q2.

| outcome | B₁₆ / B₅₀ / B₈₄ (events) | total σ_ln | one-bin s₉₅: median [16 %, 84 %] | reach, EST (GeV): median [84 % edge] |
|---|---|---|---|---|
| every count zero, every ceiling empty, no pile-up term | 8 / 11 / 15 | 0.33 | 10.2 [6.2, 15.2] | 830 [769] |
| **the same with the EST pile-up term: every no-pile-up ceiling empty** (upper edge) | 13 / 18 / 25 | 0.32 | 13.3 [8.6, 22.0] | **790 [712]** |
| Z(νν) enters at its ceiling (estimator not credited): m_H = 3 (7 events) | 19 / 25 / 33 | 0.28 | 16.1 [10.1, 25.5] | 761 [690] |
| m_H = 10 simulated ceiling events (23 background events) | 33 / 41 / 51 | 0.23 | 21.0 [13.9, 31.8] | 720 [655] |
| m_H = 30 (68 events) | 73 / 87 / 101 | 0.16 | 31.5 [21.7, 46.8] | 657 [596] |
| m_H = 100 (≈ 230 events) | 224 / 245 / 269 | 0.09 | 53.2 [36.7, 76.2] | 576 [523] |
| m_H = 1000 (≈ 2,300 events) | 2,229 / 2,299 / 2,373 | 0.03 | 168 [119, 237] | 415 [369] |
| (β) Z(νν) tested and credited (at its floor); conditional on the promotion model being submitted (§4.4 point 4); the eight proxied processes, the additions and multijets at H, H per event as for Z(νν) with m_H = 10 / 30 / 100 | 24 / 36 / 79 (B₅₀) | 0.24 / 0.19 / 0.11 | 15.4 / 17.4 / 24.7 | 767 / 749 / 695 [706 / 684 / 641] |
| (γ) every SM ceiling at H per event as for Z(νν), i.e. scaled with N_trig (×1.66), m_H = 10 / 30 / 100 | 56 / 133 / 398 (B₅₀) | 0.18 / 0.11 / 0.07 | 23.7 / 36.6 / 63.9 | 701 / 634 / 548 [636 / 578 / 499] |
| **(α1)** DIF and conversions from v1's R06–R07 counts with the pile-up fall per width step (×339–×201), **no credit** (R09 = R08): DIF 385–647 + conversions 183–308 | 548–925 / **587–975** / 626–1,025 | 0.05–0.07 | 88–114 | **504–469 [455–421]** |
| (α1) the same with v1's **pile-up** fit-probability fraction 2/35 as credit at R09; for genuine topologies it may differ either way (v1's conversion conditional p(R09 \| R06) is 2/13) | 40–57 / 51–74 / 65–97 | 0.25–0.27 | 25.5–35.4 | 690–639 [619–562] |
| (α1) no credit, size × e^(−1) / × e^(+1) (the factor-e planning uncertainty of the v1-based size) | B₅₀ 230–373 / 1,563–2,615 | | | 571–535 / 437–400 [519–486 / 390–355] |
| **(α1′)** conversions at their own measured fall (×6.5 per width step, v1's 86 → 13 → 2), DIF at the pile-up fall, **no credit** (R09 = R08): DIF 385–647 + conversions 9,530; v1's maximum-over-process photon rate 0.379 (with its N_trig-weighted 0.255: conversions 6.4×10³, B₅₀ 6,825–7,087, reach 342–338 [297–293], 419–416 at fixed B) | 9,784–10,042 / **9,929–10,193** / 10,085–10,352 | 0.02 | 352–361 | **317–314 [273–270]; ≈ 390 (394–392) at fixed B; < 243 with the planned normalisation width 0.17 (already at 0.03)** |
| (α1′) the same with v1's **pile-up** fit-probability fraction 2/35 as credit at R09 (it may differ either way for genuine topologies, as above) | 391–407 / 580–599 / 874–892 | 0.39–0.40 | 314–318 | 332–331 [250] |
| (α2) their own R06→R07 fall (DIF ×2, conversions ×6.5), no credit: ≈ 7.5×10⁴ events | ≈ 75,000 | | ≈ 540 (fixed B, an upper edge of the reach) | 262 (fixed B, an upper edge of the reach) |
| (α2) with v1's **pile-up** fit-probability fraction as credit (as above): ≈ 4,300 events | 3,000 / 4,400 / 6,500 | 0.39 | ≈ 2,200 | below 243 (beyond the plan's table) |
| for comparison, an R08-like selection (EST pile-up median 118, s_tot 0.43), ceilings empty | 67 / 113 / 172 | 0.47 | 93 [57, 145] | 496 [435] |

- *Scenario (α)* [E from v1 numbers]: v1 counted with pile-up, per 500 events, 2 and 1 attributed DIF candidates at
  R06 and R07, and 13 and 2 hard-scatter conversions (Table 4.4b), i.e. 1.3×10⁵ DIF and 6.2×10⁴ conversion events at
  R07 (N_t × count/500; the γ R06 value 4.0×10⁵ matches Table 2.1). These are counts, not bounds. (α1) applies the
  pile-up fall per width step (×339, ×201) once to reach R08; an untested fit-probability conditional is 1, so R09 =
  R08 without credit. (α2) uses their own R06→R07 fall. For the conversions that fall is measured on two independent
  steps (86 → 13 and 13 → 2, ×6.6 and ×6.5) and a pile-up-like fall is rejected at p ≈ 10⁻³; for DIF it rests on 2 → 1
  counts (a pile-up-like fall has P ≈ 1 %) [E, script [9b]]. (α1′) therefore takes the conversions at their own fall
  and DIF at the pile-up fall; it is the branch the v1 conversion record supports, with the more favourable DIF
  reading (the PV-placement and attribution caveats act on DIF). In the
  projection the terms enter as counted ceilings (Gamma(m + 1) with m = B/κ on their pool share, like the Z(νν) rows),
  with credit as a conditional of width 0.43. Caveats: v1 placed the pile-up DIF vertices at the PV, and v2 places them
  at their own z (§2), which may lower the DIF part of (α); v1's coded attribution rule is not yet transcribed (§4.4
  point 3), which acts on the level of the counts rather than on their ratio between rungs counted under the same
  rule; neither applies to the conversions. The uncertainty of these v1-based sizes is
  about a factor e (√(w_m² + ln² 2) = 1.06 and 0.94 for one and two counts). This is a planning uncertainty of the
  size, not a width that v2 would carry: the projection uses the counted-ceiling reading (Gamma(m + 1) on the pool
  share), which is what v2's likelihood carries for a counted term; the factor e is shown as the B × e^(±1) rows
  (median reach ≈ 400–570 GeV for (α1)). Read as a log-normal width instead, it would give a median reach of 262 GeV
  (pile-up fall ×339) and below 243 GeV (×201) [E, script [9b]; ESTIMATE, v1 placeholder efficiencies, like every
  reach of this table]; that reading is not used. A reach at a 10⁴-event
  background is statistics-only. The term carries the normalisation nuisance of its SM processes (§4.7, ≈ 0.17); with
  it the reach of (α1′) is below 243 GeV (below 200 GeV by PLAN l.122), and its 84 % edge is so already at a width of
  0.03 [E, script [9b], v6 lines].
- *Scenarios (β) and (γ).* Z(νν) has an evaluable B4-c test, so the terms expected at H are the eight proxied
  processes and the additions (β); (γ) is the envelope in which every SM process sits at its ceiling. The Z(νν)-only
  rows are therefore an upper edge of the reach when H counts. (β) is a result after the freeze: at day 15 its Z(νν) credit
  does not exist yet, and the rule reads every SM process through the Z(νν) pilot count, as in (γ) (§11.7 rule 1; script [9b], v9 table).
- *The pile-up estimate* [E from v1 numbers]: the direct rate at R07 is 2.98×10⁴ events (35 in 48,000 trials [V]).
  The fall per width step measured between R05, R06 and R07 (×201, ×339) gives 88–148 events at R08. v1's conditional
  fit-probability fractions (2/35, 32/126, 12/32, D4 l.266 [U]) give 5.0–8.5 at R09 and 0.5–0.8 at R11. There is no
  v1 number for the 2S step; R14 is at most the R11 value. B₈₄ = B₅₀·e^(s_tot): 135–227 at R08, 9–15 at R09, 1.7–2.9
  at R11 and at most 5.7–9.5 at R14 (1.7–2.9 with a 2S crossing PASS; the fit-probability and shape comparisons earn
  no credit, §4.0 point 7). The no-credit value of the term is 485 events at 68 % (§4.5).
- *Mapping check.* The same computation on the sixteen-plus-four floors of version 2 gives s₉₅ = 24.1, the value of
  the constructive review. Dropping the zero-count terms would give 3.0 in every row. The mapping uses the same s₉₅
  definition as the book: the CLs limit at the Poisson-median count for a fixed background (`book/checks/ch29_checks.py`
  l.25-47, with the best-Λ signal per mass at l.54-58 [V: read this session]); both give 3.0 → 1,026 GeV at B = 0.
- *What is not known.* The ceilings H, and whether DIF and the conversions behave like (α). H counts every
  hard-scatter event with a near-pass set of own hits, so m_H = 0 is not the expectation (Df-9 makes H larger, §4.4
  point 4). The pilot measures H on 2.3×10⁶ Z(νν) events before the freeze; decision point 2 recomputes the projection
  for every term of the likelihood, preliminarily at day 7 and bindingly at day 15 (§11.7). **The day-15 pause
  (B₅₀ > 300 events: at day 15, ≈ 12 Z(νν) pilot counts with the other pilot counts at zero; in the result, m_H ≈ 125 pool counts if Z(νν) alone sat at its ceiling, reach ≈ 560 GeV) is the expected
  branch** by v1's conversion counts; the reading of each branch under §11.7 rule 1 is the v9 table of script [9b],
  quoted in Q2.
- *The always-eligible baseline* R07-direct (§4.12) is of order 1.6×10⁵ events from v1 counts (pile-up direct
  3.0×10⁴, DIF 1.3×10⁵ at v1's 1 attributed count in 500, SM direct bounds near 10⁴ each): about v1's level.
- *The change of the bound, and the bracket for the abstract.* v1's best B₈₄ was 1.2×10⁶. The rows above correspond
  to 3.1 ((α1) without credit) to 4.7 (ceilings empty) decades less, quotable only with the label "bounded". In the
  bounded outcome the abstract quotes a bracket: the reach at the 84 % edge with the background as large as the
  simulation allows (the conservative number, quoted first) and the reach for a negligible background (1,026 GeV at
  B = 0, PLAN l.121, EST with v1 placeholder efficiencies).

**Closure design (COM B1-a).**
- *Derivation.* f_k, P_geo and H on the pool. The s_model of the promotion model is fixed before the freeze on the
  pilot's 1,000 near-pass overlays (sample 11, point 4). S, and after the freeze a refinement of the promotion
  comparison, on **derivation overlays** built from pool events: for DIF every passer at R04–R05 up to 2,000 and
  2,000 near-pass events stratified in k, read at R04–R05; for each NI radius 500 events, read at R04. The occupancy inputs come from the ρ = 1 development
  sample. Pool events used in overlays are also counted in f_k; the event bootstrap resamples them jointly, so this
  correlation is inside s_P.
- *Test, DIF.* **Test overlays** with other seeds, read at the held-out rungs **R06–R07**, attributed counts: 4,000
  passing and near-pass events with known sampling weights, taken from a **disjoint scan slice** of no-pile-up
  events (seed stream `prod.c0.dif.tst`, never counted in M_t), plus 1,000 unbiased full-pile-up events. The slice
  needs N_scan = 4,000/H(R06) events; H(R06) is at least the attributed fraction with pile-up, 0.004, so
  N_scan ≤ 10⁶. 2×10⁶ events are budgeted (13 CPU-h), the second half as the reserve of the day-15 rule. The ceiling
  and leak tests use only the 1,000 unbiased events (point 4); the enriched 4,000 serve the S and π_k closure. The test is
  sized for an expected count of 31 at R06, which gives the 24 needed with probability 0.92: if the pilot's
  enrichment 1/H(R06) is below 1.7, the test sample becomes 7,750 unbiased events (+19 CPU-h, a conditional draw of
  §11.2).
- *Test, NI (rung split).* v1 has 0, 1 and 1 attributed counts per 500 events at R06 for the three radii, so a test
  at R06 would need 12,000 unbiased events per radius (84 CPU-h each) or an unknown enrichment. Instead S and the
  promotion width are derived at **R04** only, and the test is on 1,000 unbiased full-pile-up events at the
  held-out **R05**, where v1's counts give 92, 120 and 378 attributed candidates. The criterion gets a verdict at no
  extra cost. The price is a longer extrapolation (width 2.09 at R08, §4.0), so the NI terms stay close to their
  ceiling.
- Tolerance F = 2. The R04–R05 comparison on the DIF test sample is a consistency check.

Table 4.4b. Attributed direct counts per 500 full-pile-up events in v1 [V: `AN1/background.json` →
`cprime.<t>.rows[].factors`] and what the planned test samples are expected to hold [E, script [11]].

| population | v1 per 500 events: R04 / R05 / R06 / R07 | planned test events | expected at the test rungs | status |
|---|---|---|---|---|
| DIF (term) | 166 / 81 / 2 / 1 | 4,000 enriched + 1,000 unbiased (or 7,750 unbiased) | R06: 4 per 1,000 unbiased; 31 expected with an enrichment ≥ 1.7 or with 7,750 unbiased events | evaluable at R06; at R07 if the enrichment is ≥ 4 |
| NI 22 / 30 / 61.5 mm (terms) | 127/46/0/0; 173/60/1/0; 553/189/1/0 | 1,000 unbiased each | R05: 92 / 120 / 378 | evaluable at R05 (rung split) |
| γ; V⁰ (hard-scatter sub-topologies, not terms) | 153/86/13/2; 859/358/6/0 | 1,000 unbiased each | R04 / R05 / R06: 306/172/26; 1,718/716/12 | completeness and diagnostic populations (no ceiling test) |
| prompt pairs (not a term) | 24 at R02; 1 at R04 | 1,000 unbiased | R02: 48; R04: 2 | diagnostic population (no ceiling test) |
| loopers (not a term) | 0 in 10⁵ no-pile-up guns | 1,000 unbiased | — | completeness diagnostic (mixed class) |

**Acceptance criteria (identifiers of COM).**
- **B1-a closure.** Held-out test as above for DIF and for each NI radius, with the verdict classes of §4.0.
- **B1-b extrapolation.** b̂, σ_b, s_f and s_tot(r) of the promotion term are tabulated for every T2 candidate
  (§4.12); the width of §4.0 point 7 is in the likelihood whatever the size of b̂, and every probability is censored.
- **B1-c rates.** Geant4 and v1 rates are compared per term and per share. The comparison passes if they agree
  within the combined uncertainty of: the FTFP_BERT against QGSP_BERT difference (measured, below), the material
  uncertainty from a public Phase-2 source (R-17), and statistics. Outside it the cross-check is reported as failed
  and the Geant4 rate is used; the v1 number is not restored.
- **B1-d geometry and Fatras physics.** Material scan Geant4 against the ACTS material map: |Δ(x/X₀)| ≤ 1 % per
  layer; radii and z-extents equal to 1 µm. The physics list actually active in pyacts 48 is printed and recorded
  (it was never set explicitly, D5 §7.7). If hadronic interactions or decays of charged pions and kaons are on, they
  are switched off, so that nothing is counted twice (§2).
- **B1-e biased generation.** Weights closure at R05; the analytic bound written with its scattering allowance; the
  pilot's gain per term recorded before the freeze; the re-allocation rule of point 5. If the weights closure fails,
  generation is unbiased (G = 1).
- **B1-f attribution, classes, CKF factor, promotion, ceiling and completeness.** The rule of point 3 in the
  pre-registration; the classes on hit subsets with k per layer type, on all own hits (Df-9), with S_CKF as a tested,
  censored factor; H(r | t) tabulated at every T2 candidate; the per-k promotion comparison on the pilot's overlays;
  one combined ceiling verdict per term in the family of 19 (α_c = 0.05/19), on unbiased samples only; the leak
  fraction as an implementation check and the mixed excess from the paired pile-up-only pass, bound 0.26, c_mix;
  first on development samples (results fixed before the freeze), then on the test samples for the verdict.
- **B1-g** the placement and the single counting of pile-up-vertex secondaries, and the truth-attributed test of §2.
- **Fail and not tested:** §4.0 point 6.

**Physics-list and composition variations.** The Geant4 vertices are regenerated with QGSP_BERT and with a C/Si/Cu
mixture at equal x/X₀, and P_geo is re-measured on 5×10⁶ no-pile-up events each (52 CPU-h). The physics-list
difference is a measured two-model difference and enters as a nuisance on rate_t and P_geo. The composition
variation enters as a nuisance only if R-17 gives a public composition range; otherwise it is a robustness test
whose shift of μ₉₅ is reported beside the limit (the no-source default of §4.9) [L2].
**Cost.** 542 CPU-h [E, script [3], [4]]: pilot 33 (Phase 2, with 6 for the Geant4 vertices of its unbiased DIF
and NI events; the 29 CPU-h hard-scatter part of the pilot is booked under B4); development 60, the secondaries test
17.5 and 1,000 unbiased Geant4 DIF development overlays 7 (Phase 3); Geant4 spectra, discs and I/O 15; variations 52;
pool share 3.61×10⁷ events = 208 (chain 115, Geant4 vertices 92); overlays 17,500 × 25.2 s = 123 (DIF 9,000, NI
3 × 1,500, four sub-topologies × 1,000); scan slice 13; paired pile-up-only pass on the 4,000 unbiased test overlays 13.
**Storage.** No-pile-up events cannot be stored in full (8.2 kB × 1.0×10⁸ = 841 GB [E]); jobs write a per-event
summary (rung flags, the near-pass class and key variables, about 50 B) and full records only for passers and
near-pass events at R04: ≈ 30 GB [A4]; the pilot's no-pile-up events are kept in full (≈ 52 GB, point 5). No-pile-up jobs are limited to 80,000 events by memory (FEAS_A §3.7).
**Dependencies.** Geant4 on the three workers; C1 chain; occupancy inputs of B2 for π_k.
**Risks and fallbacks.** (1) Material composition: the slabs are Si-equivalent in X₀, but nuclear interactions scale
with λ_I (FEAS_B) [L2]. (2) Hand-over of the parent's hits → two variants compared. (3) If the zeros do not persist in
the large samples, the paper reports the measured irreducible background (plan outcome "real background"); that is
a result, not a failure. (4) Cross-section biasing lowers the Geant4 share of the cost per event; its factor is
recorded with the weights. [DT1] If the Geant4-to-Fatras hand-over fails after three documented attempts: Geant4 is
used for the vertex kinematics only, with Fatras propagating all products from the vertex and no parent truncation,
documented with its bias.

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
development sample (the 4,000 C1 events and the enlarged development sample) using rungs R04–R05 only. Its s_model
is the r.m.s. of ln r at a development rung not used for the inputs (development R06), or the in-sample R04–R05
value if that is larger. The test is on the independent 96,000-trial sample at **R06–R07**; R04–R05 there is a
consistency check.
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
  The crossing test rungs of §4.0 point 7 are tested with the same criterion: for thinning in the fit-probability,
  2S and shape families, for the occupancy model in the 2S family only (its fit-probability and shape comparisons
  are consistency checks, Df-2); their verdict decides whether the estimator is used in that family and with which
  width. An estimator
  whose development r.m.s. is above the cap of 0.135 is not submitted (§4.0 point 4 (c)).
- **B2-c agreement at depth.** At each rung beyond R07 where thinning has an evaluable precision
  (σ_tot ≤ ln 1.5/3 = 0.135 with N = N_eff), the two estimators agree within a factor 1.5 by the same criterion, with
  r = B_thin/B_occ. An evaluable PASS at a counting or width rung moves the origin of the extrapolation
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
  [E]:** if the R06 gain holds with pre-merge candidates, N_eff ≈ 80 at R07 and of order 10 or less at R08 (the direct
  rate there is below 2.4×10⁻⁵). With the 70 direct counts, σ_tot at R07 is then 0.16, above the limit of 0.135:
  thinning is evaluable at R04–R06, and at R07 only if N_eff reaches about 250 (B2-g measures it). So thinning is
  expected to be tested to R06, perhaps R07, and not R08, and
  **B2-c is expected to be NOT EVALUABLE at most deep rungs.** In that case the pile-up term beyond R07–R08 is a
  **one-estimator extrapolation** (the occupancy model) with the width of §4.0: 0.43 at R08, 0.59 at R09, 1.29 at R11
  and 2.47 at R14 without crossing tests, 1.30 at R14 with a 2S crossing PASS (the fit-probability and shape
  comparisons earn no credit) [E, script [12], s_model at its cap].
  Its projected size is in Table 4.4c. This is said to the user now (§12.1), not discovered at Phase 4a.
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
**Cost.** 599 CPU-h [E, script [3]]: direct 24,000 × 60.4 s = 403; ρ = 2 3,000 × 206 s = 172; measurements 10 (Phase 2);
occupancy development 10 (Phase 3); crossing rungs 5 (re-analysis). A second direct sample of the same size (403 CPU-h) is reserved, not planned
(§8, failure protocol).
**Dependencies.** C1 (same code), dumps for the occupancy model. **Risks.** As above; the ρ = 2 unit cost rests on
one event.

### 4.6 B3 — conditionals for purpose-built cuts, vertex veto, time tag (MUST, Phases 2, 3 and 4a)

**Method.** In v1 the rungs "not a helix" (R15–R17) and "not two straight lines" (R18–R20) earned no credit against
prompt pairs and kinks, because the single allowed bound per term was spent earlier (D4 §1.3). In v2 each such cut is
a measured conditional probability on the large no-pile-up samples of B1 and B4: P(pass cut | term, passes the
preceding rungs). Three conditionals are added:
1. the shape rungs h and o, per term (COM B3-a);
2. a **displaced-vertex veto** (B3-b): no two-prong vertex at transverse radius above a threshold reconstructed from
   the candidate's hits. Its threshold and vertex-quality cut are fixed in Phase 3 from background samples only;
3. **[SD6] the time tag** (B3-c; late-hit credit, D3 §6.2: missing from the plan). In v1 the probability that a
   prompt candidate carries a late barrel-timing hit was set to 1 for the single-interaction and SM terms.

**The assumption behind every conditional, named (COM B3-d; finding M4, referee Q4).** If P_geo counts zero beyond
R08–R09, the population "passes the preceding rungs" does not exist at the deep rungs. The conditional is then
measured after a looser rung and **assumed to transfer** to the deep one. That is a factorisation across kinds of
cut. It is tested and given a width, as follows.
- Each conditional is measured after at least three different preceding rungs on the no-pile-up samples (R05, R06,
  R07, and R09 where populated), each with ≥ N_min passes **after** the cut (§4.0 point 3).
- *Stability test:* the values after the first two preceding rungs are the derivation; the value after the deepest
  populated rung is the test, on a disjoint half of the sample (events split by seed parity). Criterion "within a
  factor 1.5" of §4.0.
- *Width:* the conditional applied at rung r carries s_tot(r) of §4.0 point 7, with the distance counted from the
  deepest rung at which it was measured: 0.82, 2.03 and 2.84 for 2, 5 and 7 rungs at the cap. A conditional is
  therefore worth little unless it is measured within about two rungs of where it is applied; it is censored at 1.
- *Pile-up:* the conditional measured without pile-up is compared with the one measured on the test overlays of B1
  at R06 (attributed candidates), where evaluable; at the derivation rungs R04–R05 the comparison is a consistency
  check.
- A conditional that fails earns no credit (it enters as 1) and is reported as failed. A conditional that is NOT
  TESTED earns no credit.

**The time-tag fraction (B3-c; default Df-5 of §12.1).** The late hit of a prompt background candidate is a
pile-up or noise hit in the timing layer inside the candidate's footprint, so a no-pile-up measurement does not
exist, and a direct count at the nominal window is at the limit of what the samples hold (the book's late fraction
is about 10⁻⁴ per window edge, D3 l.216-217 [U]). The design is therefore at hit level:
1. *Timing model.* Hit time = time of flight + collision time + resolution. The collision-time spread of the
   luminous region, the resolution of the barrel timing layer with its non-Gaussian tail fraction, the readout
   window and the occupancy from neighbouring bunch crossings and noise are taken from public Phase-2 documents
   (retrieval R-7, extended). v1 used one Gaussian of 35 ps (D5 §4 [U]). A Gaussian alone would overstate the
   rejection by orders of magnitude if the true tail fraction is at the per-cent level (review P-B7).
2. *Prediction.* p_late(t_cut) = (density of timing-layer hits later than t_cut per unit area, measured from all
   pile-up hits of the C1 events, thousands per event) × (the candidate's footprint in the timing layer).
3. *Closure on prompt candidates.* The credit is for prompt candidates (single-interaction and SM terms): their own
   timing hit is prompt, and their late hit is an unrelated pile-up or noise hit in the footprint. The test
   population is therefore the **truth-attributed hard-scatter candidates at R04** of the SM hit-level samples
   (5.8×10⁵ in the four large samples, 1.95×10⁵ of them in Z(νν) [E, script [11]]) and the attributed candidates of
   the B1 test overlays. Derivation: the footprint definition, on the development sample. Test: ln r of the
   predicted over the counted late fraction at five window edges t_cut, from a predicted fraction of about 10⁻² down
   to the nominal window, with the criterion "within a factor 1.5" and the evaluable-rung rule (N ≥ 55 late
   candidates). A late fraction of 10⁻⁴ at the nominal window would give about 58 counts in the four large samples
   and about 80 with the other eleven, so the nominal edge is evaluable only if the fraction is not smaller. The pile-up
   candidates of the direct sample, whose own timing hits come from many vertices, are a consistency check and not
   the test.
4. *Independence from the geometric rungs.* The late fraction of the prompt candidates at the widened window is
   measured at R04, R05 and R06; its slope enters the width of §4.0 for the deeper rungs.
5. *What the credit can be.* **The credit is p_late at the deepest window edge with an evaluable PASS on prompt
   candidates**: the nominal window if the test is evaluable there, otherwise the tightest tested edge. Nothing is
   extrapolated in t_cut. The credit is never below the sourced tail fraction of the timing resolution. If the tail
   fraction or the out-of-time occupancy cannot be sourced (R-7, R-18, by day 15), **no credit is taken** and SR-T
   carries the same single-interaction and SM terms as SR-G, as in v1. Each such term then enters both categories
   at its full value with one shared rate parameter; in the combination this counts the term twice, which is
   conservative, and the paper says so.

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
3. *Hard-scatter terms with the estimator of §4.4* instead of zero-count bounds. A B4 term holds every candidate
   attributed to particles of the hard-scatter vertex (§2): prompt pairs, loopers, conversions and V⁰ are inside it.
   P_geo, f_k and the ceiling H are counted on no-pile-up hard-scatter events of each process; survival and
   promotion as in §4.4; conditionals from B3. The no-pile-up samples come from the common pool of §4.4: **3.65×10⁷
   events over fourteen processes, allocated as √N_trig** (Z(νν) 1.10×10⁷), at 45 ms per event = 457 CPU-h. The
   fourteen are v1's twelve and the additions Z(ττ) and lost-lepton Z(ℓℓ) at their planning N_trig (Table 4.4a; seed
   streams `prod.hs0.ztt`, `prod.hs0.zll`), whose shares are re-allocated at day 12–15 when the MET model gives their
   N_trig (§11.7). Multijets use their own loose population (below). Their zero-count floors are in Table 4.4a: 8.6
   events summed, 2.6 for Z(νν). The pilot's 2.3×10⁶ Z(νν) events (29 CPU-h, Phase 2) measure the ceiling of the
   largest term before the freeze.
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
source only** (R-3). Check by limiting case: R_j ≡ 1, no lost leptons and no soft
term give MET_reco = neutrino MET, i.e. the v1 filter. **No parameter value is quoted here**: the jet response, its
tail, the lepton acceptance and the soft-term resolution are retrieval tasks (R-3), taken from public Phase-2
documents with page references, and the model is frozen in the pre-registration. The same model is applied to the
signal (§4.13, S1-f). **If R-3 yields no usable parameters** by day 5, a second public source is tried (the HL-LHC
performance reports of the other general-purpose experiment; logged in `retrieval_log.md`). If that fails too, B4-b
is a MUST item that is infeasible after a real attempt: the study stops and the user is asked (brief §7, §11.6).
Nothing is filled from v1's unsourced smearing or from memory.
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
If it is not flat, the multijet term uses the passing events only and its floor is stated. The multijet ceiling test
(the MET-selected, weighted hit-level sample against H from the loose population) therefore also tests the B4-e
factorisation, and a FAIL is charged to the factorisation first. Planning value of the
floor through the factorisation [E]: N_MJ × 1.14/10⁶ = 0.46 events at N_MJ = 4×10⁵ (1 % of N_trig), 0.05–4.6 over
0.1–10 %; it is part of the headline sum (§0, Table 4.4a).

**Acceptance criteria (identifiers of COM).** (B4-a) every process of the list has its own hit-level sample; the proxy
fraction of B_SM is zero at every rung. (B4-b) the three additions are in N_trig with the model above; its external
validation and internal check recorded. (B4-c) the hard-scatter estimator closes against the direct hit-level
attributed count within a factor 2. The hit-level sample of each process is split by seed parity: survival and the
promotion width are derived on one half at R04–R05, and the test is on the other half at the held-out R06 (and R07
where evaluable). **Statistics (brief D4).** The count that matters is the preselection-weighted (effective) count.
v1 has at R06 [V: `AN1/background.json` → `sm.<p>.rows`, `n_class_events`]: Z(νν) 32.3 in 2,000 events; W(τ_h) 8.96 in
1,625; W(τ_ℓ) 3.04 in 375; tt̄ 1ℓ 5.19 in 2,000. An evaluable test half needs N_eff ≥ 24. The samples are sized for
an expected 31 in the test half, which gives at least 24 with probability 0.92: **Z(νν) 10,000 events (81 expected),
W(τ_h) 11,250, W(τ_ℓ) 7,662 and tt̄ 1ℓ 23,880 (31 each)**: +65, +40 and +153 CPU-h over 2,000 events each [E, script
[11]]. W(τ_h) and W(τ_ℓ) are two forced-decay samples (τ decays forced to hadronic or to leptonic modes in Pythia),
so these costs stand; one inclusive W(τν) sample of 20,430 events would give both classes for about +11 CPU-h.
v1's three small counts carry errors of 33–57 %. No SM hit-level sample exists before the freeze other than the C1
Z(νν) sample, so **the 4a hit-level campaigns are staged** (P14): the first half of each sample is produced, its R06
rate is measured on its derivation parity half (so the test half is not looked at before its prediction exists), and
the second half is sized from it, by a top-up from the reserve or a conditional draw reported
as an overrun (§11.2, §11.7). Until then the sizes and the rule-4 decisions of §11.7 use v1-proxy rates, labelled
with their errors. The four supplied processes (Z(νν), W(τ_h), W(τ_ℓ), tt̄ 1ℓ) carry 86 % of N_trig. Of the four
terms sized at an expected 31 counts (route 1 of the Q3 annex), with P = 0.92 each, at least one of DIF,
W(τ_h), W(τ_ℓ) and tt̄ 1ℓ ends NOT TESTED with probability 0.30 before staging [V: script [11]]; staging is the
compliance route (Q3). The hard-scatter estimator is one estimator for all processes; its s_model can be derived
before the freeze only on the Z(νν) development sample (sample 5) and the pilot, and is fixed there. B4-c and the
per-k promotion comparison are also reported split by truth sub-topology (prompt pairs, conversions, V⁰) as
consistency checks on the same samples (conversions fell far slower than the rest in v1). The eight proxied processes have
no v1 count; at 2,000 events they are expected NOT TESTED and enter at their ceiling H, whose ceiling test is
evaluable at R04–R05 on the 1,000-event test half. That is the exception to brief D4 put to the user in Q3, with the
cost per process in the annex of §12.1 and the day-15 rule of §11.7. (B4-d) every K-factor has a citation. (B4-e) as
above.
**Fail:** a process without a sample stays a proxy and is named as such; a MET model that is not validated means the
three additions are quoted with the full variation as width and the failure is stated.
**Statistics and cost.** 1,186 CPU-h [E, script [3]]: hit level 74,790 events × 25.2 s = 524 (eleven new processes ×
2,000, Z(νν) 10,000, W(τ_h) 11,250, W(τ_ℓ) 7,662, tt̄ 1ℓ 23,880); no-pile-up pool share 457; pilot 29; multijet generator
level 10⁷ × 23.4 ms = 65; multijet loose population 12.5; development (MET model and its validation, multijet
generation tests; no SM hit-level sample) 50; paired pile-up-only pass on 15,000 hit-level test-half events (1,000 of
each of the fifteen SM processes; R5) 49.
**Dependencies.** B1/B3 estimator; MG5 for tW. **Risk.** Multijets need biased generation in p̂T with weights; a few
events with large weights can dominate. Fallback: finer p̂T slices; the effective sample size is reported, and the
likelihood treats each slice as its own weight class (§4.11).

### 4.8 B5 — road-rotation sideband, closed in simulation (SHOULD, runs in days 36–48, deadline 4b; definition in Phase 3)

**Method.** The data-driven recipe for an experiment: rotate the road away from the missing-momentum direction,
keep every cut, and predict the signal-road count from the sideband roads with a transfer factor T. The simulation
tests the two assumptions never tested: the fake rate is flat in the angle to the MET, and roads in one event are
independent. For pile-up-only candidates flatness holds by symmetry (pile-up does not know the MET direction); the
part that can be non-flat is the hard-scatter component, where jets recoil against the MET and hadronic τ decays lie
near it.
**Why the test is defined on the hard-scatter component.** In an SM sample with pile-up
the hard-scatter share of the candidates is 10 % at R04, 8 % at R05 and 6 % at R06 [E, script [13], from the C1 table].
A hard-scatter non-flatness of ×2 moves the total by 6–10 % and one of ×5 by 25–41 %: both would pass a factor 1.5 on
the total (review N-B-6). The test on the total cannot see the effect it exists to measure. Therefore:
- T(Δφ) of the hard-scatter component is measured on the **no-pile-up hard-scatter samples** of B4 (the pool of §4.4,
  10⁶–10⁷ events per process). The road rotation runs **inline in the pool jobs**, because the pool keeps summaries
  only (10 CPU-h in all);
- on the samples with pile-up the closure is evaluated on the **truth-attributed hard-scatter candidates** (rule of
  §4.4 point 3) and, separately, on the pile-up candidates.
**Corrected statement.** PLAN l.342-343 calls the book's B₈₄ ≈ 0.17 "the systematic floor … the width used in the
reach". In the book it is the B₈₄ of an *empty sideband in real data* with 8.2×10⁸ trials and a transfer width copied
from a published search; the width of that estimate is σ_ln = 1.105, and 1.14 × 0.05 × e^1.105 = 0.172 [V: script
[13]; D3 §2, §6.3]. What v2 can deliver is the measured non-flatness and non-independence at R04–R07; the width that
enters the reach curve as "the data-driven scenario" is about 1.1 plus the measured non-closure [L3].
**Acceptance criteria (identifiers of COM).** (B5-a) Flatness of the hard-scatter component: per process and for the
sum, the sideband prediction of the signal-road count closes within a factor 1.5 (§4.0) at the evaluable rungs among
R04–R07. Derivation: T from the sideband roads; test: the signal road, which the derivation does not use. The
signal road is counted on **all 10,000** Z(νν) hit-level events produced for B4 (162 weighted hard-scatter
candidates at R06), so R06 is evaluable for Z(νν) in both variants. Sideband and signal roads belong to the same
events, so B5-a holds only as far as B5-c holds, and is labelled so. (B5-b) The
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
any evaluable threshold. What limits the loss: the non-flatness of the
hard-scatter component, the quantity of interest, is now measured on the no-pile-up samples at full granularity in
both variants. **Dependencies.** B4 samples with dumps. **JFC 12.** This is a compute-envelope limit, not a
failed attempt; it needs the user's approval at Gate A (Q4). A further lever on this SHOULD item is offered in Q4
and not taken by default: the sideband with pile-up on the 500 pile-up events only (−137 CPU-h, off the critical path; B5-c on
the SM samples is lost). **Schedule (S-1, adopted):** the B5 prototype and production (183 CPU-h reduced; the
10 CPU-h of road rotation stay inline in the pool jobs) run after the 4a production window, in days 36–48 beside the
S1 chain and the toys; B5 is not in the likelihood, and the 4a note states that B5 is pending. The test definition
is in the pre-registration. **In the paper:** the method section states the number
of roads and events; the limitation index states that R07 was not closed with pile-up; Future Directions names the
full 20-road test.

### 4.9 B6 — detector-model robustness (SHOULD, Phases 4a–4b; definition in Phase 3)

**Method.** Seven variations: hit resolution × 1.5; hit inefficiency 99 % → 97 %, now applied to pile-up hits as
well (v1 applied it to signal hits only, D5 §4); material × 0.5 and × 2; top-up factors at their low and high limits;
an alternative soft-QCD tune for the pile-up at fixed density (conventions row "qq̄ modelling" translated).
**[SD5]** The top-up variation is a density systematic at fixed ⟨μ⟩ = 200; it is not a pile-up scan (brief D8) (D2 O4).

**Robustness test and nuisance are two different things.** ×1.5, 97 %, ×0.5 and ×2 are
the plan's round numbers (PLAN l.345-346). JFC forbids a round-number variation as a nuisance. Therefore:
- The seven variations above are run as **robustness tests**: measured, reported and classified (criterion B6-b).
  They do not enter the likelihood at their measured size.
- The **nuisance** for resolution, inefficiency and material is sized from a public Phase-2 statement (retrieval
  tasks R-15 hit resolution per layer type, R-16 hit efficiency, R-17 material budget and its uncertainty). Its
  effect is the measured log-shift scaled linearly to the sourced size: Δ_nuis = Δ_meas × δ_sourced/δ_varied (in
  ln of the varied quantity). The linearity is checked where two sizes exist (material ×0.5 and ×2 give two points
  on either side). The top-up limits and the alternative tune are already defined by sources (the public occupancies
  the top-up is normalised to, and a published tune) and enter at their measured size.
- If no public number is found for a variation, there is **no nuisance** for it (JFC sizing rule: nothing is
  invented). The gap is not left silent: the shift of μ₉₅ under that robustness variation is **reported beside the
  headline limit**, and it is named in the abstract-level limitations if it exceeds 10 % (default Df-7 of §12.1,
  which the user can override). R-15 to R-18 close by decision point 2 (day 15).

**Where each variation is evaluated (COM B6-c).** From R07 on the leading terms are single-interaction and SM
terms, so every variation is evaluated on every term.

| nuisance (shared name) | pile-up term | single-interaction terms | SM hard-scatter terms | signal |
|---|---|---|---|---|
| hit resolution, hit inefficiency | 600 (1,000 full) ρ = 1 events per variation, R04–R06; carried to depth through the occupancy model, which is analytic in resolution and per-layer efficiency | P_geo and H re-measured on 2×10⁶ no-pile-up events per variation, at every T2 candidate | same on 5×10⁵ no-pile-up events of Z(νν) and W | rows through the full chain |
| material (rates and scattering) | as above (through hit density) | rate_t from Geant4 with scaled material; P_geo, H as above | as above | Stage-3 reruns with scaled material |
| top-up density, tune | as above | through π_k and S only (occupancy inputs re-derived) | same | pile-up hits around the ribbon: rows through the full chain |
The no-pile-up reruns cost 4 × (2×10⁶ × 11.5 ms + 5×10⁵ × 45 ms) = 51 CPU-h [E, script [3]], in both variants.
At a T2 candidate where these reruns count zero, the shift is measured at the deepest rung with counts and carried
to the candidate with the width s_tot of §4.0, the distance counted from that rung. For a term that is a bound or
enters at its ceiling, the detector nuisances act only through H and the conditionals: the nuisance is the shift of
ln H at its deepest counted rung and of each conditional. Beyond R06 the pile-up shift is carried by the occupancy
model with the same width.

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
prototype (10, in the production window): 391 CPU-h. **[DP2] Reduced (proposed): background 7 × 600 events; signal
at 4 points × 300 rows: E 200 at 1.5 keV, E 500 at 3 keV, E 500 at 5 keV, E 1000 at 3 keV; nominal partners 18;
236 CPU-h in all** [E, script [4]]. **Schedule (S-1, adopted):** the background arm runs in the 4a production
window; the signal arm (varied rows, their nominal partners and the scaled-material Stage 3, 95 CPU-h reduced) runs in
days 36–48, and its ratios are read only after the verdicts anyway; the 4a note states that the B6 signal arm is
pending. The set keeps 5 keV and a mass above 500 GeV, the points most sensitive to
material (the ribbon thickness is scattering-dominated above 1.2–1.9 keV, D5 §7.13) and to timing (the slowest pairs).
*Lost with the reduction:* no variation is measured for the scalar or at 1,500 GeV; the unpaired error on the pooled
efficiency ratio is 8.2 % instead of 5.2 % [E, script [13]: binomial, v1 placeholder ε ≈ 0.2 at R04].
*Rule for points without a variation (pre-registered).* The log-shift of a point is that of the nearest varied point
in (ln m_Q, ln Λ); its uncertainty is increased by half the spread (maximum minus minimum) of the shifts over the
varied points, added in quadrature.
*Alternative offered in Q4:* the paired design at all six points of the full set with 300 rows (signal 76 CPU-h
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
Beam-gas interactions and satellite bunches are added as one line each, with a public rate or an argument.
**Criterion.** A number with its derivation for B_cosmic + B_halo (+ beam gas) in 3 ab⁻¹ at the chosen selection. If
it is below 10 % of the 1σ uncertainty of the total background (B₈₄ − B₅₀ of §4.11) it is stated and left out of the
likelihood; otherwise it enters as a term.
**Fail:** if no public rate can be sourced, the item is reported as "argued, not quantified", as in v1. **Cost:** 5 CPU-h.

### 4.11 T1 — the likelihood (MUST, Phases 2–4c)

This section specifies the statistical model completely, including the background rate at which the expected limits
are generated when a simulated count is zero.

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
| estimator output | thinning, occupancy model, survival S, promotion π_k, a conditional carried from another rung, time-tag fraction | nominal value | — | — | log-normal nuisance θ of width (bootstrap error ⊕ s_tot(r) of §4.0), **censored at the no-credit value** (parameter bound) | θ drawn from its constraint and censored at the same bound |
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
- *Censoring at the no-credit value.* For a probability factor with nominal value φ₀ and width s the nuisance is
  bounded at θ_max = ln(1/φ₀)/s, so that φ = min(φ₀·e^(sθ), 1): a parameter bound in the pyhf fit, and in the
  generation a draw above θ_max is set to θ_max. S ≤ 1 and π_k ≤ 1 then hold in every fit and every
  pseudo-experiment, and with them P(r | t) ≤ H(r | t) (both are built from the same counted rates). The pile-up
  estimate is bounded in the same way by its no-credit value, the zero-count bound of the 96,000 direct trials, drawn
  like every other zero-count term: N_trig·λ/96,000 with λ ~ Gamma(1) in each pseudo-experiment (68 % value 485 events,
  §4.5). A tested factor can therefore
  never cost more than an untested one.
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
selection rule would prefer them.
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
to a Gaussian of mean m and width √m, the standard Monte Carlo statistical uncertainty; the **count width**
w_m = sd(ln λ) is 1.28, 0.80, 0.63, 0.53, 0.43, 0.10 for m = 0, 1, 2, 3, 5, 100 [V: script [9]].
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
statistic is q̃_μ from two pyhf fits of the workspace (auxiliary channels with free γ: pyhf's `shapesys` cannot
represent an observed zero, FEAS_C R9). CLs = p_(s+b)/(1 − p_b) from the two ensembles. The
expected limit is the median over the background-only ensemble, with the 16–84 % and 2.5–97.5 % bands. Only the
sampling of the generation point is outside pyhf's built-in toy calculator; the likelihood, the fits and the test
statistic are pyhf's. Consequence used below: the two test-statistic distributions depend on μ and on the observed
m, not on the pseudo-data, so they are computed once per (selection, point, μ) and stored.
*Asymptotic numbers.* Where an asymptotic limit is used (T2 ranking, the comparison table T1-g), the Asimov data
set is built at λ = m + 1 with the auxiliary Asimov observation m + 1, the mean of the same posterior. No quoted
limit is asymptotic.
*Grid and interpolation.* For each selection and point the asymptotic limit μ_a is computed first. The toys are run
at the eight values μ_a × {0.4, 0.55, 0.75, 1, 1.35, 1.8, 2.5, 3.5} (v1's asymptotic-to-toy ratios were 0.32–1.07,
D2 §2 [U], so the grid reaches 3.5 μ_a). μ₉₅ is the value at which ln CLs, interpolated linearly in μ between the two
grid values that bracket it, equals ln 0.05. If the grid does not bracket 0.05 it is extended by factors of 1.5 on
that side (inside the T1 allowance).

**3. Definitions that follow from the model (binding wording for the paper).**
- *Predictive distribution of the background:* the distribution of B_c = Σ_t B_{t,c} when every counted λ and every
  nuisance is drawn as in the toy procedure. B₁₆, B₅₀, B₈₄ are its percentiles.
- **B₈₄** (for the background-free flag and the ladder figure): its 84th percentile, per category.
- **Total σ_ln** = ½ ln(B₈₄/B₁₆). This is the only quantity called σ_ln. The width of one counted rate is the count
  width w_m of point 2 (1.28 at m = 0; ½ ln(q₈₄/q₁₆) of the same Gamma(1) is 1.18).
- **Label of a term** at a selection: the first of these that applies.
  1. **no credit**: a factor of its route is at its no-credit value (verdict FAIL, NOT TESTED or NOT EVALUABLE, or
     s_model above the cap). The label adds whether the ceiling is counted or empty.
  2. **bound**: a counted factor has m = 0.
  3. **low count**: a counted factor has 1 ≤ m ≤ 3 (w_m > 0.5).
  4. **estimate**: every counted factor has m ≥ 4 (w_m ≤ 0.5) and every estimator it uses has the verdict PASS.
  The ladder figure, the tables and the text use these four words and no others, each printed with the s_tot of
  the term's route (an "estimate" carried at s_tot = 2.09 says so).
- A term is **leading** for a selection and category if the 84th percentile of its own predictive distribution
  exceeds 10 % of B₈₄, computed with no-credit values for every factor that is not PASS (§4.0 point 6).
- **f₀** = (sum of the predictive means of the terms with a zero-count factor) / (predictive mean of B).
- **Reading of the central target (COM TG-1).** The plan's target is an *estimated* background with σ_ln ≲ 1.
  "**Target met**" requires all three: total σ_ln ≤ 1 in both categories; f₀ ≤ 0.5; and **every leading term
  labelled estimate**. If σ_ln ≤ 1 and one of the other two fails, the reading is "**target not met: width small,
  background bounded (f₀ = …)**", naming the labels of the leading terms (so a background of "low count" terms, m =
  1–3, with σ_ln = 0.26 and f₀ = 0, is not "target met"). If f₀ > 0.5 the paper adds "sample-size limited" and
  quotes, beside the median expected limit, the limit at the 84 % edge of the band as the conservative value; the
  abstract heads with that edge. A small σ_ln alone is not a result: the sum of the nineteen zero-count floors of
  Table 4.4a has σ_ln = 0.34 with f₀ = 1. **The reading expected if the day-15 pause does not fire is "target not met:
  sample-size limited" while the ceilings count few events** (by v1's conversion counts the
  expected branch is a measured background, §0, Q2); with a counted ceiling (for example m_H = 10 for Z(νν)) f₀ falls to
  about 0.2 [E] and the reading becomes "target not met: width small, background bounded".
  The eligibility consequences of every verdict are those of §4.0 point 6.

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

Readings. (a) Dropping the term gives 3.0 at any κ: at the summed floor of this strategy (Σκ ≈ 11, §4.4: 10.2 against
3.0, script [9b]) that would be optimistic by a factor 3.4. (b) The convention is weaker than a fixed 1.14 κ for κ ≳ 5, because it
carries the full width of an unmeasured rate. (c) The last column is what the same procedure returns, in the median,
if the true rate is λ and the simulation still counted zero (probability e^(−λ) = 61 %, 32 %, 14 %, 5 %). At κ = 35
the quoted median is too strong by 1.6 if the truth sits at the 68 % upper value, by 2.7 at λ = 2 and by 4.0 at
λ = 3; the 16–84 % band contains the first case and not the other two. **A zero-count expected limit is therefore
quoted with its band, never as a single number**, and with the f₀ statement of point 3.
(d) Coverage, computed exactly for this model with the simulation redone in every pseudo-experiment and a true
signal of 10 events: 0.945–0.956 at κ = 1 and 0.982–1.000 at κ = 10 for true λ between 0.5 and 3; given m = 0 it is
0.950–1.000. The lowest value, 0.945 at κ = 1 and λ = 0.5, comes from the cases m ≥ 1, where the flat-prior
posterior (mean m + 1) over-estimates a background of 0.5 events. This small under-coverage is a known property
of the flat prior at small counts; it is reported, and it is the reason the coverage checks below are compared
with the convention's computed coverage, not with 0.95 (Df-10).
(e) Coverage is not the figure of merit of a projection: an under-estimated background makes the limit
conservative. What matters is the bias of the quoted median when the true rate is larger (the last column: a factor
1.4 at κ = 10 if the truth sits at the 68 % upper value). The pre-declared answer is the f₀ rule of point 3, which
ties the headline to the 84 % edge of the band whenever f₀ > 0.5.

**5. Asymptotics or toys.** The expected counts are small and many auxiliary counts are zero, so the conventions'
condition for asymptotics (more than about 5 expected events per bin) fails; v1 found asymptotic/toy ratios of
0.32–1.07 (D2 §2 [U]). **Every quoted limit and the final T2 choice are toy-based.** Cost [unit V on a 31-parameter
workspace, total E]: 1000 s+b and 1000 b toys at one signal value cost 652 s. Two passes are needed: pass 1 at
Phase 4b (the five best selections at the 20 window points, optimisation half) and pass 2 at Phase 4c (the chosen
selection, the runner-up and the v1 fallback at 40 points, evaluation half).
*Parametrisation in f_T (default Df-8 of §12.1).* The background model of a selection is the same at all points. A
point enters only through its total signal yield S_tot, its SR-T fraction f_T and its signal nuisances. The toys are
therefore run per selection on a grid of 11 values of f_T and 8 values of the signal yield s, with the signal
nuisances of the point that has the largest signal uncertainty in the pass (conservative);
μ₉₅(point) = s₉₅(f_T)/S_tot, with s₉₅ interpolated linearly in f_T. Cost: pass 1, 5 × 11 × 8 × 652 s = 80 CPU-h; pass 2,
3 × 11 × 8 × 652 s = 48 CPU-h. *Check:* exact toys at three points per selection (the smallest f_T, the largest f_T
and the best point): 22 + 13 CPU-h. If a check point differs from the parametrised limit by more than twice the toy
error, exact toys at every point are used for that pass and the next; their extra cost, at most 236 CPU-h, is a
conditional draw of §11.2. The scaling of the toy cost with the number of parameters is not measured; the v2
workspace will have 60–100, so these numbers may double [L4]. The scaling is **measured in Phase 2** on a
60–100-parameter workspace built from v1 counts, and the budget is corrected against the stop rule of §11.6.
pyhf 0.7.6 needs numpy 2.2 (FEAS_C O5).

**6. Acceptance criteria (identifiers of COM; the conventions' validation checks, §5.2).**
- **T1-a** The workspace validates against the pyhf schema and is published.
- **T1-b** v1 mode: re-fed with the v1 counts and with v1's treatment switched on (log-normal bounds, uncorrelated
  categories), it reproduces the v1 hybrid-toy limit at the best point within 10 %. Units: v1's number is
  1.2458×10⁷ **events before selection** (`AN1/limits.json` → `points["A2|F|200|1.5|BM"].expected_toys.median`), i.e. μ₉₅ = 1.2458×10⁷/15,775
  = 789.7 in units of σ_norm [V: script [13]]; the comparison is made on μ₉₅ = 789.7. With the v2 treatment the
  change is reported.
- **T1-c Zero-count convention, five tests** (Phase 3, on workspaces built from v1 counts; test (iii) is repeated in
  Phase 4a on the v2 workspace, 20 CPU-h for the stored distributions at m′ = 0…6):
  (i) *limiting case, zero count:* a one-bin workspace with one term, m = 0 and κ = 1, 10, 35 reproduces the
  analytic limits of the table within the toy error (2,000 toys per μ);
  (ii) *limiting case, large count:* the same workspace with m = 100 and m = 1000 reproduces the limit of pyhf's
  standard toy calculator with a Poisson-constrained `shapesys` within the toy error;
  (iii) *coverage with a non-zero true rate:* at two points of the v1-count workspace, 500 pseudo-experiments per
  (point, λ) with a fixed true λ = 0.5, 1.14, 2, 3 for the leading zero-count term, the simulated count redrawn
  (m′ ~ Pois(λ)) and a true signal at μ₉₅^exp; the fraction with μ₉₅ ≥ μ_true passes the coverage-family rule below;
  the ratio of the median limit to the quoted median is reported for each λ (the analogue of the last column above);
  (iv) *dependence on the convention:* the limit at the best point under alternatives (ii) and (iii) of point 2;
  (v) *effect of the censoring:* test (iii) with the censoring of point 1 on (the model) and off; both coverages
  are reported.
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
  nuisance with a mean pull beyond that, with |pull| > 2 in more than 10 % of the fits (4.6 % expected; 10 % is 3.7
  binomial errors above, script [13]), or at a boundary in more than 5 % of the fits (censoring bounds excepted),
  is investigated. On Asimov
  data only the **constraints** are read (pulls are zero there by construction): any nuisance constrained to below
  0.5 of its prior is explained.
- **T1-f Impact ranking and pruning** (check 4; conventions pitfall "pruning"). Ranking produced; the leading
  nuisances are named and compared with the expectation (closure nuisances and zero-count constraints). No nuisance
  is pruned unless the fit time requires it; then a nuisance may be dropped only if its impact on μ₉₅^exp is below
  1 % at the three test points, and the quadrature sum of all dropped impacts stays below 5 % of the leading
  systematic.
- **T1-g Asymptotic against toy limits** tabulated at every point (Asimov as defined in point 2).
- **T1-h Coverage at a known signal.** At two points, 500 pseudo-experiments with a true signal at
  μ_true = μ₉₅^exp and **fixed true rates λ = m + 1 for every counted factor** (the posterior mean, as in T1-d). The
  simulated counts are redrawn in each pseudo-experiment, m′ ~ Pois(λ). Each pseudo-experiment gets a toy-based
  limit from the **stored** test-statistic distributions at m′ = 0…6 (two fits per μ value, 0.5 CPU-h in all, script
  [3]); the fraction with μ₉₅ ≥ μ_true passes the coverage-family rule below. The target (0.95 at a known injected
  signal) is independent of the ensemble that defines the quoted median. (A nested-toy version would cost
  1,449 CPU-h, script [7].)
- **Coverage family (T1-c (iii) and T1-h; default Df-10).** The two are one family of 10 checks (4 λ × 2 points, and
  2 points). Each check is compared with c_ref, the convention's computed coverage at the workspace's κ and true λ
  (the exact sums of point 4 (d) for the one-bin analogue), at most 0.95. FAIL below k_F, the count with
  P(X < k_F | 500, c_ref) ≤ 0.05/10 (462 of 500 at c_ref = 0.95, 459 at 0.945); INVESTIGATE from k_F to the
  one-check 5 % point (462–466 and 459–463); one re-test on 500 new pseudo-experiments, FAIL below k_F. Family-wise
  false FAIL 4.7–4.9 %; a true coverage of 0.90 passes with 0.6–2.7 % [V: script [13]]. (The single threshold 0.93
  of version 3 failed a correct likelihood in 15–48 % of the cases.) Alternative, equally acceptable: pool the four
  λ values into one check per point (2,000 pseudo-experiments, FAIL below 1,878 at c_ref = 0.95).
- **T1-i** Every quoted limit is toy-based: parametrised in f_T with the exact-toy check, or exact. Both passes of
  point 5 are run.
- **Fail:** T1 is not used for a quoted limit until fixed; a failure of T1-b is a regression on the v1 reading.
**Cost.** 263 CPU-h [E, script [4]]: 60 development and tests (Phase 3; the workspace builder starts in Phase 2 on v1
counts), 20 expected results and 20 coverage toys (4a), 101 (4b), 61 + 0.5 (4c).
**Dependencies:** B1–B4 outputs.

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
(model the charge deposit and keep one dE/dx candidate) is given with default Df-4 (§12.1).
**The list of 16 is frozen at Gate A**: the pre-registration may not add, remove or re-define a candidate (§4.1).

**Rule.**
1. *Eligibility* **[SD8]**. For each candidate, each term enters the likelihood under its label of §4.11 point 3,
   and eligibility follows the single statement of §4.0 point 6 (closure FAIL by direction, ceiling FAIL,
   completeness, NOT TESTED / NOT EVALUABLE / not submitted, "leading" with no-credit values). For an analysis whose
   estimators and ceilings perform as declared, a false FAIL removes a selection with probability 6.9–8.9 %.
2. *Always-eligible baseline (COM T2-g).* R07 with **every term from direct attributed counts or direct bounds** and
   no estimator at all ("R07-direct") is evaluated in every outcome. It gives the paper a limit that depends on no
   extrapolation, however weak.
3. *Figure of merit:* G = mean of ln μ₉₅^exp over the 20 window points (the four E masses × Λ ∈ {1, 1.5, 2, 3, 5} keV;
   the v1 lower edge of the window at pile-up 200 is 1.0–1.2 keV, D2 §2 [U]), with μ₉₅^exp the median expected CLs
   limit under the generation convention of §4.11, the efficiencies from the **optimisation half**, and the full
   background model. The signal efficiency at every point is the one estimator ε̂ = (k + ½)/(n + 1) for k passing of
   n rows. The choice is repeated with ε̂ = k/n (points with k = 0 dropped) and the change of
   winner, if any, is reported. Lower G is better.
4. *Choice:* all 16 candidates are ranked with asymptotic limits (Asimov of §4.11 point 2). The **five best** are
   re-evaluated with toys at the 20 window points, and the toy values decide. If another
   candidate has a toy G within one bootstrap standard deviation of the best (bootstrap over optimisation rows), the
   one with fewer cuts is chosen. With the public v1 row arrays (`AN1/signal_rows_a2.npz`) and the floor table, G and
   its bootstrap spread are computed for the 16 candidates **before the freeze**, with v1 placeholders, to check that
   the tie rule is not decided by noise; no v2 efficiency is involved.
5. *If only the baseline is eligible:* this is the plan's "closure fails" outcome. G is still
   reported for all 16, labelled with their verdicts, and the paper is the method and anatomy paper of PLAN §8.
6. *Background-free flag (COM T2-f):* B₈₄ ≤ 0.11 events per category (the v1 budget, 0.3/2.71 = 0.1107 [V: script
   [13]]), with B₈₄ as defined in §4.11, is reported as a yes/no flag for the chosen selection. It is not a
   requirement. With the floors of Table 4.4a it cannot be met unless the gain G of biased generation exceeds about
   110 (script [9]).
7. *The estimate-only selection (COM T2-h).* Under Gamma(m + 1) the predictive mean of a term falls from 3κ to κ
   when its count goes from 2 to 0, whatever the physics did, so the rule is drawn to the first rung at which the
   leading terms are empty; the protections below stop it from going further, not from going there. The paper
   therefore reports two selections: the **T2 winner**, and beside it the best candidate (lowest G) **whose leading
   terms are all labelled "estimate"**, with its G and reach. If no candidate qualifies, R07-direct is shown in
   that place and the paper says so. The abstract headlines the winner with its labels and quotes the
   estimate-only selection beside it (part of Q2). The winner's G is also recomputed with a prior that enforces
   λ(r + 1) ≤ λ(r) for nested rungs of one sample; the change is reported and decides nothing.

**Robustness of the rule against empty simulation (COM T2-e).** A selection must not win because the simulation has
no events there. Three protections: the generation convention keeps every zero-count term in the expected limit at
N_t/M_t per unit λ; "one zero per term" (§4.11) stops deeper cuts from multiplying bounds; and a deeper rung with the
same zero-count terms has the same background and less signal, so its G is worse. **Check (Phase 3, pre-freeze, on
v1 counts):** for the deepest candidate, G under the convention must be worse than G with every zero-count term
dropped (the B = 0 value) by more than the toy error, and its one-bin analogue must reproduce the analytic limits
of §4.11 point 4 at the candidate's κ. A comparison with the terms fixed at 1.14·N_t/M_t is reported but is not the
criterion, because for κ ≲ 3 the convention gives the stronger limit (3.0 against 4.1 at κ = 1).

**Table of extrapolation distances (COM B1-b, B2-f).** For every candidate the pre-registration lists, per leading
term and per factor: the counted rungs (§4.0 point 7), the last evaluable cumulative test rung, the crossing test
rungs with their verdicts and s_f, d_in, d_out and s_tot. The planning widths are in the table of §4.0 point 7: the
pile-up factor of the occupancy model is usable to about R09 whatever its crossing comparisons give (only the 2S
crossing test earns credit); a promotion factor tested at R06 only, the expected case, carries 1.41 from R08 on (2.51
at R14, 1.42 with a 2S crossing PASS), and one tested at R06–R07 (DIF at an enrichment of 4 or more) 0.73 to R11.

**Background-side bias of the choice (COM T2-d; finding M29).** Choosing the minimum of G over 16 candidates also
selects downward fluctuations of the background inputs. The choice is repeated on 50 bootstrap replicas of all
background inputs (counts redrawn from their posteriors, estimator outputs from their bootstrap) for the five best
candidates (asymptotic, 14.5 CPU-h). Reported: how often the same candidate wins, and the mean shift of its B₈₄
between the replicas in which it wins and all replicas. If the nominal winner wins in fewer than half of the
replicas, the tie rule (fewer cuts) is applied among the candidates that win in more than 20 %.

**Partial outcomes.** Which selections stay eligible in each case is the rule of §4.0 point 6; this table gives only
what the paper shows.

| what fails or is untested | what the paper shows |
|---|---|
| nothing | chosen selection and the estimate-only selection; reading of the target by §4.11 point 3; outcome "good", "middle" or "real background" by the size of B |
| a MUST closure NOT TESTED, NOT EVALUABLE or not submitted, accepted under Q3 (expected: the eight proxied SM processes, the additions; possibly one of the four supplied terms) | same figures; term labelled "no credit", ceiling counted or empty; Table 4.4c applies to its ceiling |
| closure FAIL by over-prediction, ceiling PASS | term labelled "no credit (estimator failed)" |
| completeness not PASS | term at its extended ceiling H′, labelled "no credit" |
| closure FAIL by under-prediction, or ceiling FAIL, for a leading term | R07-direct; G for all 16 with verdicts; "closure fails" |
| one pile-up estimator FAIL | pile-up labelled "one estimator" |
| both pile-up estimators FAIL | R07-direct; the ladder shows the 485-event direct bound; "closure fails" for pile-up |
| a conditional or the time tag FAIL / NOT TESTED | the factor at 1; SR-T equal to SR-G for the term if the time tag has no credit |
| MET model not validated | the three additions carry the full variation; stated limitation |
| no MET parameters from two public sources | B4-b infeasible: the study stops and the user is asked (brief §7) |

**Optimisation/evaluation split.** Each generated signal event gets the half h = parity of
blake2b(salt ‖ species ‖ mass ‖ event index) (the hash family v1 used for seeds, D5 §3). The half does not depend on
Λ, so one physical event is in the same half at all eight Λ. The salt is chosen at the freeze and recorded in
`PREREG_v2.md`; before that the mapping does not exist. The two halves are produced as separate campaigns with
separate directories. The aggregation script takes the half as an argument; its invocation on the evaluation half is
a logged step that requires the Gate B approval record.
**Acceptance criteria (identifiers of COM).** (T2-a) rule, list, figure of merit, estimator ε̂ and salt in the hashed
pre-registration before S1 production. (T2-b) the choice is reproduced by a second run of the script from the frozen
inputs. (T2-c) the optimisation-to-evaluation shift of ln μ₉₅ at the chosen selection is reported per point; a mean
shift above 2σ of its bootstrap error is reported as evidence of selection bias. (T2-d), (T2-e), (T2-f), (T2-g),
(T2-h) as above. **Fail** of (T2-b): Gate B is not requested.
**Cost.** 16 CPU-h [E, script [3]]: 16 × 40 scans × 10.4 s = 2; bootstrap 14.5. Toys are in T1.
**Dependencies.** T1, S1, verdicts of B1–B4.

### 4.13 S1 — signal ×10, full chain at all 40 points (MUST, Phases 2, 3, 4a, 4b, 4c)

**Method.** 2,000 rows per point (v1: 180–200 [U: D4 §4.1]), every row through the full chain (Stage 3 → injection →
digitisation → CKF → finder), at all 40 points. The fast path (numpy digitisation without CKF, 31 of 40 points in v1)
is retired; v1 measured it high by 1/0.87 at the fallback (D4 §4.3 [U]). Rows are split 1,000/1,000 by the T2 hash.
**What "×10" means here (default Df-1 of §12.1).** 2,000 rows are ten times v1's rows in total. The limit is
set on the 1,000-row evaluation half, and v1's limits used its 180–200 template-half rows
(`AN1/acceptance.json` → `finder_note`, read by the arbiter), so **the statistic that sets the limit grows by ×5**.
The plan asks both for "ten times the rows" (PLAN l.371) and for the optimisation/evaluation split (PLAN l.362-363)
and does not say which half the factor refers to. This strategy follows 2,000 rows unless the user overrides
default Df-1 with 4,000: at ε = 0.045 (v1 placeholder) the binomial error on the limit half is 14.6 % with 2,000 rows and 10.3 % with
4,000, against 33 % in v1; 4,000 rows cost +827 CPU-h, 4.7 production days [E, script [6], [13]].
**[SD10]** Only events inside the counting acceptance (|η_pair| < 2.5) and accepted by A are propagated: the acceptance
A = ε_fid × ε_trig × ε_presel is formed from generator-level quantities [V: `AN1/acceptance.json` → `definition`,
`factors`] and the MET model of §4.7, so the other events need no string propagation. v1 propagated 463–519 events per (mass, Λ) for 200
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
  The sample is generated in Phase 2; m_mig is computed once, with the frozen MET model, at step (4) of the order
  in §4.1. If m_mig ≤ 5 %, the migrated events are neglected, which lowers the signal and is conservative for a
  limit, and m_mig is quoted. If m_mig > 5 %, the generator cut of the S1 samples is lowered to 150 GeV before the
  string propagation; the extra Stage-2 and Stage-3 cost is then re-projected against the stop rule of §11.6.
- *Calorimeters, muon system, lepton veto.* The chain stops at the tracker and timing layer. A quirk pair is a pair
  of heavy charged particles that reaches the calorimeters and the muon system; whether its non-helical trajectory
  would be reconstructed as a muon and vetoed, or enter a particle-flow MET differently, cannot be simulated here.
  v2 assumes that the pair is not identified as an isolated lepton and that its calorimeter deposits do not change
  the MET beyond the model's response. No public efficiency for this exists in the repo: retrieval R-13 looks for
  one; without it the assumption is limitation [L11], and the paper gives the limit as a function of an assumed
  veto survival probability (a rescaling of μ₉₅, no extra compute). The physics argument that R-13 should support:
  a non-helical trajectory gives no tracker track, so the pair cannot form a particle-flow or global muon; it can at
  most leave a stand-alone track in the muon system, which monojet-type vetoes do not normally use, and slow pairs
  arrive there out of time.
- *Tracker hit-time acceptance.* Slow pairs at high mass arrive late. Late hits in the timing layer define SR-T;
  the tracker's own readout window is not modelled in v1. The window is taken from a public Phase-2 readout
  description (R-14) and applied to the quirk hits from their Stage-3 times. The fraction of hits lost is a signal
  quantity: it is formed after the closure verdicts, and enters as a systematic at 1,000 and 1,500 GeV (and as a
  correction if it exceeds 5 %). If no window can be sourced: limitation [L12].
**Cost.** 834 CPU-h [E, script [4]]: Stage 3 10,000 events × 95.6 s = 266 (Phase 3, days 12–19, after A is fixed;
truth level, no selection efficiency involved; whether it may precede the hash is Q5); chain 80,000 rows × 25.2 s
= 561 (Phase 4a, after the freeze); migration sample 7 (Phase 2). The plan's "12–30 CPU-h of string" (PLAN l.443) is not
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
2. *Published matching limit, like with like.* The scalar Ẽ has the quantum numbers of
   a right-handed slepton. σ_NLO(Ẽ, N_IC = 1) from `loop_quirkE`, at the collision energy and PDF set of the
   reference, is compared at 200, 500 and 1,000 GeV with a **fixed-order NLO** number: the NLO column of the LHC SUSY
   cross-section working-group right-selectron tables if they give one, otherwise a public NLO slepton-pair code run
   at the same settings (R-1 identifies which). Criterion: within 3 % at each mass. A comparison with the NLO+NLL /
   NNLO_approx+NNLL tables themselves would mix unlike quantities: their implied K rises to 1.29 at 1 TeV
   (`stage2_C001_quirks/research/theory_signal_model.md` l.158-163 [U]). If no fixed-order
   reference can be obtained, the comparison is made against the resummed tables with the tables' own NLL/NLO ratio
   removed where the source gives it, and otherwise validation 2 is reported as NOT EVALUABLE (the computed K is
   then used on the strength of validations 1 and 3, and this is stated).
3. *Process independence, differential.* The QCD correction acts on the initial state only, so at equal invariant
   mass the K-factor of a colour-singlet pair does not depend on the final state. K(M) for `p p > e+ e-` at NLO is
   compared with K_E(M) in bins of the pair invariant mass; criterion: agreement within 2 % or within 3σ of the
   integration error in each bin, whichever is larger. K_E/K_Ẽ
   is reported as the test of v1's "spin-independent" assumption.
**[SD11]** (default Df-3 of §12.1) σ_norm = N_IC × σ_NLO(MG5), with the 7-point scale envelope and the
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
conservative for the mass reach; the alternative (apply it) is given with default Df-3. Three refinements are left
to R-12, all small against the band: the constant term (the vector-current threshold factor quoted in the physics
review, C_F α_IC [π/(2β) − (3 + β)/(4π)·(π²/2 − 3/4)], gives +3.4 %, +6.6 %, +13.9 % at the same β, script [13]); the
scalar Ẽ, which is produced in a P wave and needs its own factor; and the scale of the coupling (m_Q β instead of
m_Q).
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
The v1 record is inconsistent: it quotes 0.84 M3 CPU-h for the 171-event test, while 171 × 2 × 32.3 s (v1's own Stage-3 time at
5 keV, `STAGE3_INDEX.json`) is 3.1 h (review K-B2). **Which configuration the v1 test ran (event subset, step
size, B* switch in the kernel or in the analysis) is resolved from the v1 code before the test is launched**, and
the cost is re-projected then. **Risk.** The extended-precision map is 1–2 person-days of new code (D5 §1.8 [U]); if it is
not finished, [DT3] floor test 2 alone is reported and floor test 1 is listed as not done.

### 4.16 S3, S4, S5

**S3 (dropped, brief D1).** The paper stays barrel-only and states the endcap gain as an outlook, tagged EST, from plan
S3: signal ×1.5–3.2; reach 866 → 1062 GeV at B = 10, g = 1. That statement answers referee question 11. The endcap row
of the reach table does not appear as a result. (Provenance note for the paper: ×3.2 = 1/0.31 at g = 1 is in the
book, ch29 l.106-110; the lower end 1.5 has no derivation in the book or the plan, D3 §5; see default Df-6 in §12.1.)
**S4 (COULD) — recommendation: not included [DP4].** A merging-tolerant rung and a lower seed opening-angle cut change
the finder or add a selection, so every background estimator would have to be closed again for it: about one more
week of development (PLAN l.382; book ch28 l.256 [U]) and a rerun of the finder on all background samples: the trial
part of B2, B1 and B4 is ≈ 740 CPU-h [E, script [6]: trials are 78 % of a four-road event and 46 % of a one-road row].
It would also delay the freeze.
**S5 (COULD) — recommendation: not included [DP4].** A pile-up-robust separation estimator is method R&D with no bound
on its duration; the paper states the negative result (sep_IT flat at 18–26 mm at pile-up 200; M_est a proxy), as
PLAN l.384-385 allows. Estimated cost if requested: about a week and ≈ 50 CPU-h [E].

### 4.17 Sample inventory (COM INV-1)

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
| 4 | C′_PU topologies (v1 guns) | 5,000 events | `c1.cpu` | C1; development (attribution rules compared; completeness classes; for the conversions, the Q2 (c) development estimate, §11.7 rule 1) | 19 | 2 | 35 |
| 5 | Z(νν)+jets hit level | 2,000 events | `c1.sm` | C1; development (B4, B5 prototypes; route check of §2) | 20 | 2 | 14 |
| 6 | signal at the three C1 points, v1 path, and full-chain twins | 3 × 400 rows + 800 | `c1.sig` | C1 only (tiers of §4.1); never part of S1 | 22 | 2 | 14 |
| 7 | Stage 2 signal, five species-masses, with four re-showers | 5 × 250,000 LHE | `s2.nom`, `s2.var.*` | production input of S1; f₂₀₀ (Phase 2); A and m_mig (Phase 3, once) | — | 2 | 47 |
| 8 | migration sample (generator cut 150 GeV) | 5 × 100,000 LHE | `s2.mig` | S1-f measurement | — | 2 | 7 |
| 9 | FxFx 0–1 jet at 500 and 1,500 GeV | 2 points | `s2.fxfx` | S2-c uncertainty | — | 2 | 40 |
| 10 | Stage 3 truth propagation, 40 points | 2,000 rows per point | `s3.sig` | production input of S1 (truth level; events accepted by A; halves assigned by the hash at the freeze) | 6 | 3 (days 12–19; Q5) | 266 |
| 11 | pilot: generator-level minimum bias; unbiased no-pile-up DIF and NI with their Geant4 vertices; no-pile-up Z(νν)+jets; near-pass overlays | 10⁷; 4 × 10⁶; 2.3×10⁶; 1,000 | `pilot.*` | development (gain G, f_k, H and N_t·H, enrichment, check of the analytic bound); the near-pass overlays fix the s_model of the promotion model (per-k comparison) before the freeze | 17, 18, 19, 25 | 2 | 61 |
| 12 | enlarged development closure sample, ρ = 1 | ≈ 5,960 events | `dev.pu1` | development (decision point 2, s_model, crossing rungs) | 14 | 3 | 100 |
| 13 | pile-up events with the Geant4 secondaries of all pile-up particles | 1,000 events | `dev.g4pu` | development (truth-attributed test B1-g) | — | 3 | 17.5 |
| 13a | unbiased Geant4 DIF overlays (development ceiling and completeness tests, with the paired pile-up-only pass) | 1,000 events | `dev.ovl.dif` | development | 19, 25 | 3 | 7 |
| 14 | pile-up ρ = 1 direct | 24,000 events (96,000 trials) | `prod.pu1` | **test** for B2-a and B2-b, cumulative and crossing rungs; consistency check of B3-c; production (direct counts R04–R07) | 1, 12 | 4a | 403 |
| 15 | pile-up ρ = 2 with pre-merge candidates | 3,000 events | `prod.pu2` | production (thinning estimator) | 2, 14 | 4a | 172 |
| 16 | second direct sample | 24,000 events | `reserve.pu1` | reserve (INVESTIGATE or bug re-test only) | 1, 12, 14 | 4a | (403) |
| 17 | no-pile-up pool, DIF and three NI radii, one Geant4 vertex per event (Table 4.4a) | 3.61×10⁷ | `prod.c0.<term>` | production (P_geo, f_k, H); conditionals of B3 with derivation and test halves by seed parity; source of the derivation overlays | 11, 25 | 4a | 208 |
| 18 | no-pile-up SM hard-scatter pool, v1's twelve processes | 3.46×10⁷ | `prod.hs0.<process>` | production (P_geo, f_k, H); B5 T(Δφ) inline; B4-e flatness test | 11 | 4a | 434 |
| 18a | no-pile-up pool share of Z(ττ) at its planning N_trig (re-allocated at day 12–15) | 1.43×10⁶ | `prod.hs0.ztt` | production (P_geo, f_k, H of Z(ττ)) | 11 | 4a | 18 |
| 18b | no-pile-up pool share of lost-lepton Z(ℓℓ) at its planning N_trig (re-allocated at day 12–15) | 3.8×10⁵ | `prod.hs0.zll` | production (P_geo, f_k, H of lost-lepton Z(ℓℓ)) | 11 | 4a | 5 |
| 19 | overlays: DIF derivation (≤ 2,000 passers + 2,000 near-pass) and test (4,000 enriched + 1,000 unbiased); NI 3 × (500 derivation + 1,000 unbiased test); γ, V⁰, prompt pairs, loopers 4 × 1,000 unbiased | 17,500 events | `prod.ovd.<t>` (derivation), `prod.ovt.<t>` (test) | derivation (DIF R04–R05, NI R04); **test** (DIF R06–R07, NI R05); ceiling and completeness tests on the unbiased events only (DIF 1,000, NI 3 × 1,000), with the paired pile-up-only pass; sub-topologies: completeness and diagnostic populations | each other; 4, 11, 14 (other pile-up events); test no-pile-up events from 25, not from 17 | 4a | 123 |
| 20 | SM hit level, fifteen samples (Z(νν) 10,000; W(τ_h) 11,250; W(τ_ℓ) 7,662; tt̄ 1ℓ 23,880; eleven × 2,000) | 74,790 events | `prod.smhit.<process>` | derivation half and **test** half by seed parity (B4-c, ceiling, completeness, paired pass on 1,000 test-half events of each of the fifteen SM processes, R5); **test** population of B3-c; B5 with pile-up. **Staged** (P14): the first half of each sample is produced and its R06 rate measured, then the second half is sized from it | 5 | 4a | 524 |
| 21 | multijets: generator level, biased; loose population through the no-pile-up chain | 10⁷; 10⁶ | `prod.mj.*` | production (N_trig of the addition; B4-e) | — | 4a | 77 |
| 22 | signal, full chain, 40 points | 2 × 1,000 rows per point | `prod.sig.opt`, `prod.sig.eval` (two campaigns, two directories) | production; blind until 4b / 4c | 6 | 4a | 561 |
| 23 | Geant4 spectra, discs, I/O; QGSP_BERT and composition variations | 2 × 5×10⁶ no-pile-up events | `prod.g4`, `prod.c0.var.*` | production input; SY-5 | — | 4a | 67 |
| 24 | B6 samples: nominal partners and varied, background and signal (paired) | reduced: 8 × 600 events, 4 × 300 × 7 rows, 4 × 2.5×10⁶ no-pile-up | `prod.b6.*` | robustness and nuisances; signal part read after the verdicts | 22 | 4a | 226 |
| 25 | no-pile-up scan slice behind the DIF test overlays (second half: reserve of the day-15 rule) | 2×10⁶ | `prod.c0.dif.tst` | source of test overlays; never counted in M_t | 17 | 4a | 13 |

Samples 14–25 do not exist before the pre-registration is hashed (brief D7). Samples 1–13a exist before it. None of
them enters a closure verdict or a limit (the C1 samples give the C1 verdict, and the development samples fix each
s_model before the freeze), except 7 and 10: generator-level and truth-level signal samples whose content depends on
the MET model, the trigger threshold and the generator-cut decision, all frozen by day 12 before the propagation, but
on no plane-selection choice and on no signal efficiency at any T2 candidate. Whether they may exist before the hash
is a reading of brief D7 that only the user can confirm (Q5). If not, the S1 input is generated again after the freeze with new seeds (a
second Stage 2 of 47 CPU-h, and +1.8 production days), and the Phase-2 samples serve S2 and C1 only.

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
| Detector simulation model (data/MC) | Not applicable as written: there is no data. Translated and WI: Fatras against Geant4 for hadronic physics (B1); resolution, inefficiency and material nuisances sized from public Phase-2 numbers (R-15 to R-17) and evaluated on every term (B6-c, B6-d), the round-number variations being robustness tests only (a variation without a public size has no nuisance; its μ₉₅ shift is reported beside the limit, Df-7); top-up and tune variations (B6); physics list variation FTFP_BERT against QGSP_BERT (B1) | |
| Object calibration | WI | MET response and resolution (the B4 model parameters); trigger turn-on (S2); primary-vertex identification efficiency, set to 1 in v1 although v0.4 quotes 93 % (D3 §1 item 2) → a factor and nuisance from a public source (R-8) or, if none is found, the limitation is stated with ε_PV = 1; timing resolution and its tails (R-7, B3-c); tracker hit-time window (R-14, S1-f). The MET model applies to signal and background alike (S1-f). dE/dx scale: not applicable, dE/dx is not used [SD9] |
| Beam energy | Not applicable: pp at a fixed nominal 14 TeV; all cross sections are computed at 14 TeV. Replaced by the PDF and pile-up rows as the conventions instruct | |
| Luminosity | WI | the result is a projection at 3 ab⁻¹; the luminosity nuisance for HL-LHC comes from a public target (R-9) and applies to signal and to every background normalised to L; limits are also shown at 300 fb⁻¹ |
| PDF (pp replacement) | WI | CT18NLO eigenvectors on σ, f₂₀₀ and A (weights in the LHE files) |
| Pile-up (pp replacement) | WI at fixed ⟨μ⟩ = 200 | density (top-up limits), tune, timing spread. No scan in μ (brief D8) [A5] |
| QCD scale variations | WI | signal as above; SM backgrounds through the K uncertainty |
| Fragmentation model | WI at generator level | tune variation everywhere; string against cluster hadronisation at generator level after the Phase-2 install attempt [DP5]. It matters through the K/π ratio, which sets the decay-in-flight rate: the nuisance on rate_DIF is the relative difference of the charged-kaon and pion yields in the relevant p_T range, weighted by their decay probabilities |
| Heavy-flavour treatment | Not applicable as written (no b-tagging). Displaced b/c decay vertices are Pythia decays of hard-scatter particles (decays with τ₀ < 1000 mm are in the particle list, D5 §4), so by the route rule of §2 they are inside the real SM events of B4; Phase 2 checks on the tt̄ sample that they are present | |

Study-specific sources (all WI): thinning and occupancy closure (B2); closure of the single-interaction estimator,
promotion model and bias weights (B1);
conditionals (B3); Geant4 material composition and physics list (B1); the MET model tail (B4); f₂₀₀ (S2); QED FSR
(nominal on, shift quoted); trigger (S2); status-4 Stage-3 events dropped (≤ 1.5 %, one-sided, D5 §3 [U]); the
frozen admissibility transcription [A3]; signal Monte Carlo statistics; finder seed-threshold convergence (C2).
Every nuisance is sized by a measurement, a closure result or a cited public number; a variation with a round-number
size is a robustness test and not a nuisance (§4.9; JFC Phase 4a). Additional study-specific sources in v2: the
infracolour Coulomb correction (band on the theory line, S2-f); signal migration across the generator cut and the
lepton-veto assumption (S1-f); pile-up-vertex secondaries (B1-g); the completeness allowance c_mix (B1-f). No single nuisance may exceed 80 % of the total without investigation (regression trigger).

### 5.2 Required validation checks

| conventions check | answer |
|---|---|
| 1. Closure tests in validation regions, p > 0.05 | WI, translated: the "validation regions" are the loose rungs R04–R07 where direct simulation counts exist; the "signal region" is the chosen deep selection. Criteria in §4.0 (derivation and test on disjoint rungs and samples; four verdict classes; family-wise rule), B1-a, B2-a, B2-b, B3-a…d, B4-c, B5-a. The conventions' pitfall "blind spot in VR coverage" applies in full: the loose rungs are not between a control region and the signal region. Answers: an extrapolation width that grows with the distance from the last tested rung and is always in the likelihood (§4.0 point 7); crossing test rungs that bring a test into each deep cut family; P_geo and the ceiling H counted directly at the deep rungs, the ceiling tested as a ceiling (B1-f); two pile-up estimators compared at depth where both are evaluable (B2-c), which is expected at few rungs [L6]. The pitfall "transfer-factor instability" is answered by the reported slopes b̂ per estimator. **Departure from "passes at p > 0.05":** an INVESTIGATE case is re-tested once on a fresh sample and passes at p′ ≥ 0.05/K, because the model bias δ is shared between the test and the re-test, so a re-test at p′ > 0.05 would nearly double the false fail of a correct estimator at the cap. Its price (one rung at the evaluable limit, s_model at the cap): P(final PASS) = 0.622 against 0.584 with a re-test at 0.05 for a true bias of ln F, 0.260 against 0.233 at 1.25 ln F, 0.059 against 0.053 at 1.5 ln F (0.41 / 0.16 / 0.04 with no re-test); the criterion still fails an estimator wrong by F^1.5 in 94 % of the cases [V: script [11]] |
| 2. Signal injection at 0, 1, 2, 5 × | WI (T1-d), Phase 4a: multiples of the expected limit of each tested point, 200 fluctuated pseudo-experiments per level, bias threshold 20 % of the injected μ; v1 placeholder efficiencies |
| 3. Nuisance pulls and constraints | WI (T1-e): pulls on fluctuated pseudo-data (mean pull, and per nuisance the fraction of fits with a pull beyond 2σ), constraints on Asimov data. There is no observed fit |
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
look-ups in the repo's literature cache are logged in `retrieval_log.md` (seven entries of version 1, one of version 2, one of version 3).

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
pile-up-200 MET performance figure for the external validation of §4.7. **Deadlines (days after Gate A):** R-3 and
R-2 by day 5 (the MET model and the trigger threshold precede A, §4.1); R-7 and R-15 to R-18 by decision point 2
(day 15); R-12 and R-14 before the freeze (day 17); R-10 and R-20 before Phase 4a; the others before the phase that uses
them. **A retrieval that finds nothing** leaves its dependent item "not sourced", with the consequence fixed here:
no credit (time tag, R-7); no nuisance, with the μ₉₅ shift of the robustness test reported beside the limit (R-15 to
R-17, Df-7); a limitation with the limit given as a function of the assumption (R-13, R-14); a one-sided band
(R-12); and for R-3 a second source and then the stop-and-ask of brief §7 (§4.7). Nothing is filled from memory.

---

## 7. Label index

**Constraints.** [A1] No collision data: expected limits only; "observed" quantities and data/MC checks do not exist.
[A2] v1 cannot be reproduced event by event (lost inputs, different random streams): all comparisons are statistical.
[A3] Admissibility tables and δ₉₅ are frozen transcriptions; six hashed v1 inputs are lost. [A4] No-PU samples are
stored as summaries, not events. [A5] Pile-up is fixed at 200. [A6] Cluster: 12 worker cores (9 on weekday daytime;
10 usable off-hours while two workers carry a graphical session), 7.5 GiB per node, jobs ≤ 30 min, no cloud.
[A7] Geant4 runs on a node only if its local install matches the tracked lock; it is installed on all three workers
(commit 199e166). [A8] Public information only; material composition and many detector parameters are not public.

**Limitations.** [L1] Direct closure of the single-interaction and hard-scatter estimators reaches R06 (DIF, four
SM processes) or R05 (NI); the eight proxied SM processes are expected NOT TESTED and enter at their ceiling (Q3). [L2] Nuclear-interaction rates carry the
unknown material composition. [L3] The sideband width usable in the reach is ≈ 1.1, not 0.17. [L4] Toy cost for the
real workspace is not measured. [L5] The Stage-2 yield of in-acceptance events at E 1500 and Ẽ 500 is uncertain.
[L6] Closure regions are the loose rungs, not a region between control and signal regions; beyond R07–R09 every
extrapolated factor carries a width that grows with the distance unless a crossing test reaches its cut family;
the width per untested rung, ln F, is a convention. [L7] Barrel only. [L8] Hits are Gaussian-smeared on
cylinders, not clusters on modules; δ-rays and merged clusters are not modelled. [L9] The string is classical
Nambu–Goto without infracolour radiation; stated validity Λ ≲ 10–26 keV (D2 §8.10 [U]). [L10] Stage-3 and ρ = 2 unit
costs rest on toy inputs and on one event. [L11] The response of the calorimeters, the muon system and the lepton
veto to a quirk pair is an assumption. [L12] The tracker readout time window is applied only if a public value is
found. [L13] With zero counts in the large samples the leading terms are bounds of about 13 events in total, more if a
ceiling H counts (Tables 4.4a, 4.4c): the result is then sample-size limited. If decays in flight and conversions
behave as in v1, the leading term is a counted background of ≈ 10⁴ events (after CKF, as v1 counted them) and the result is a measured background
(§12.5 point 3). [L14] The gain of biased generation is not measured.

**Strategy decisions.** [SD1] grid unchanged. [SD2] approach comparison with the MVA moved to Phase 4c. [SD3] C1 signal
at 400 rows per point. [SD4] the counted pile-up object is the hit set after grouping at the target density.
[SD5] top-up variation is a density systematic. [SD6] time-tag fraction for prompt terms measured at hit level and
used only if its closure passes. [SD7] zero counts as auxiliary Poisson channels; expected limits generated with
λ ~ Gamma(m + 1). [SD8] FAIL by under-prediction of a leading term's estimator, or a failed ceiling test, makes a selection
ineligible; NOT TESTED earns no credit.
[SD9] no dE/dx selections; the forgone gain is measured. [SD10] string propagation only for events in the counting
acceptance. [SD11] σ_norm from computed NLO; resummed normalisation as implemented cross-check; infracolour
correction as a one-sided band. [SD12] QED FSR on in the nominal signal. [SD13] v2 single freeze content (§8).
[SD14] evaluation-half aggregation only after Gate B. [SD15] every closure test has disjoint derivation and test
rungs and samples; four verdict classes; s_model capped at ln F/3; an extrapolation width that is always added;
crossing test rungs; probabilities censored at their no-credit value (§4.0). [SD16] one pool of no-pile-up CPU
allocated as √(N_t/c_t) and re-allocated with the measured gains (§4.4). [SD17] robustness variations and nuisances
are separated (§4.9). [SD18] one accounting route per particle origin (§2). [SD19] term labels no credit / bound /
low count / estimate and the three-part reading of the central target (§4.11).

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
| Gate A (this document + `COMMITMENTS.md`) | item criteria and tolerances of §4; the verdict classes and what each earns; the zero-count convention; C1 subset and its tiers; the T2 list of 16 candidates and the figure of merit; systematic enumeration; the answers to Q1–Q5 and the eleven defaults (Df-1–Df-11, §12.1) | 4-bot review, user |
| end of Phase 3 (the freeze; not a human gate, brief D7) | `PREREG_v2.md`, hashed and committed **before any v2 production sample exists**; user notified | 4-bot review |
| Gate B | closure verdicts shown first, then selection and expected sensitivity from the optimisation half | user |

**Content of `PREREG_v2.md`** [SD13]. (1) The v1 record by hash (below). (2) For each estimator of B1–B4 and each
conditional of B3: definition, code hash, the single factorisation route, the **number** s_model fixed from the
development samples and its comparison with the cap, the derivation rungs and samples, the cumulative and crossing
test rungs and samples, the closure statistic and tolerance of §4.0 (these may be made stricter, never looser, than
at Gate A), the expected count and σ_tot per test rung with the false-fail probability at the declared s_model and
the power at |ln r| = 0.5, 1 and 1.5 × ln F, the number K of the eligibility family (10, plus tests ordered under
Q3), the sizes and seed streams (§4.17), and the consequence of each verdict; for each term with a ceiling: the
definition of H on all own hits and the CKF factor S_CKF with its test rungs (Df-9), the combined ceiling test (Šidák
over its rungs; family of T_c = 19 terms at α_c = 0.05/19; INVESTIGATE band and re-test), the completeness test (leak
as an implementation check; mixed excess from the paired pile-up-only pass; the bound 0.26) and the factor c_mix, and
the extended ceiling H′ that a term enters at if completeness does not pass. (3) B5 and B6 test definitions; the
sourced sizes of the detector nuisances. (4) The MET model with its sourced parameters and the tolerance of its
external validation. (5) The T1 workspace schema and nuisance list; the generation convention for zero counts; the
weight classes; the censoring bounds (the pile-up term at the predictive draw of its no-credit bound); the toy grid;
the coverage family of T1-c (iii) and T1-h with its thresholds against the computed coverage (Df-10). (6) T2: the list of 16, the figure of merit, the efficiency estimator, the split salt, the eligibility rule, the baseline, the table of
extrapolation distances. (7) The BDT cross-check recipe and the dE/dx forgone-gain ratio. (8) The declared
pre-verdict signal quantities (§4.1: the C1 tiers as approved in Q1; A, f₂₀₀ and the migration fraction).
(9) The analysis-code freeze: sha256 of every analysis module, taken **before** production. (10) Failure handling
(below). (11) A change log from v1 to v2, each change with its reason; none is a signal efficiency.

**Failure protocol after the freeze (COM FP-1).** JFC lists a closure failure as a regression trigger
with at least three documented remediation attempts; this document says "reported as failed, not patched". The two
are combined as follows.
1. *Always:* a failed criterion (FAIL or INVESTIGATE) opens a regression ticket, and an investigator looks for a
   cause in the code, the samples and the configuration. Up to three documented attempts to find one.
2. *If a bug is found:* it is fixed under a dated addendum to the pre-registration that states the bug and the
   fix (a background-method reason; never a tolerance, an s_model or a sample choice). The corrected estimator is
   re-tested **once, on a fresh sample that was not used for the diagnosis**: the reserved second direct sample
   for the pile-up tests (403 CPU-h, sample 16 of §4.17); freshly generated test overlays for B1 (up to 123 CPU-h);
   fresh hit-level test halves for B4 (up to 163 CPU-h); or, for a B3 conditional, a new pool slice by seed stream
   of half the term's sample (`reserve.c0.<t>`, `reserve.hs0.<p>`; up to 71–83 CPU-h). Each is a conditional draw of
   §11.2: it is reported as an overrun and counts against the stop rule. The verdict of the fresh test is final. The first result stays in the record and in the paper.
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

For Fig. 7 the signal yield is recomputed at the v2 selection (D3 §6.6); the Phase-4a version is labelled "v1
efficiencies (placeholder)". The v2 result is marked directly at (B₅₀, reach computed with the v2 predictive
distribution), with the band B₁₆–B₈₄ and its equivalent σ_ln stated, and the conservative point (the reach at the
84 % edge of the expected-limit band, the number the abstract heads with) is marked beside the median point; it is
not placed on a σ_ln = 1 curve, because a
sum of zero-count terms is not log-normal. Each term of Fig. 4 carries its label of §4.11 point 3.
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
| B1 decomposition P_geo, f_k and H against the rung, per term, with the ceiling-test points | B1-f | 1, 4 |
| s_tot against the rung per estimator, with cumulative and crossing test rungs marked | B1-b, B2-f, B3-d | 4 |
| time-tag closure: ln r against t_cut on prompt candidates | B3-c | 4 |
| G of the 16 T2 candidates with verdict flags, the estimate-only selection and the bootstrap winner frequency | T2-d, T2-h | 12, 14 |

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
| 1 | limit from zero-count bounds | B1–B4, T1-c; terms labelled no credit / bound / low count / estimate; f₀ and the three-part reading of the target (§4.11) | 6, 7; v1 in App. |
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

Every CPU-h number is printed by the script, sections [2]–[8].

### 11.1 Capacity model
- Agents: at most three at a time (`ORCHESTRATOR_STATE.md` l.20), so every phase is planned with three channels.
- Slots: 12 worker cores; at most 9 on weekdays 08:00–19:00 (brief §5.3). Two of the three workers carried a
  graphical session at preflight and are capped at 3 jobs (`LOG.md` 14:34), so **10 slots** are usable off-hours. Per
  week: 5 × (11 h × 9 + 13 h × 10) + 2 × 24 h × 10 = **1,625 slot-hours,
  232 per day** [E, script [2]] (1,851 with 12).
- Losses inside the utilisation factor: other lab users; ρ = 2 jobs that may need a node each (§4.5: up to 400
  slot-hours); ≤ 500 steps per workflow and gaps between campaigns; failed and retried jobs; Argo overhead 17 s per
  job (about 11,100 jobs → 53 slot-hours, 1.2 %) [E, script [8]]; cold NFS starts (minutes per node and environment,
  FEAS_A §3.8).
- **Effective capacity assumed: 0.75 × 232 = 174 core-h per day in production phases with campaigns queued
  continuously; 0.50 × 232 = 116 in development phases** [E]. The unit costs already contain the slowdown of 4 jobs
  per node. **The two utilisation factors are assumptions, not measurements.** They are measured in the first week of
  Phase 2 as delivered slot-hours over available slot-hours, and the calendar is re-projected then (§11.6). At 0.50
  in production every production duration below grows by half.

### 11.2 CPU-h budget (from §4; script [3], [4])

| item | priority | Phase 2 | Phase 3 | Phase 4a | 4b / 4c / 5 | total |
|---|---|---|---|---|---|---|
| C1 | MUST | 198 | | | | 198 |
| C2 | MUST | 81 | | | | 81 |
| P1 | MUST | 51 | | | | 51 |
| S2 | MUST | 88 | | | | 88 |
| S1 | MUST | 7 (migration) | 266 (string) | 561 (chain) | | 834 |
| B1 | MUST | 33 (pilot) | 85 | 424 | | 542 |
| B2 | MUST | 10 | 10 | 579 | | 599 |
| B3 | MUST | 5 | 10 | 25 | | 40 |
| B4 | MUST | 29 (pilot) | 50 | 1,108 | | 1,186 |
| T1 | MUST | | 60 | 40 | 101 / 61 | 263 |
| T2, BDT and dE/dx ratio | MUST | | | | 16 / 7 | 23 |
| enlarged development samples; timing jobs | MUST | 5 | 100 | | | 105 |
| figures, package | MUST | | | | 10 | 10 |
| **MUST total** | | **506** | **580** | **2,737** | **196** | **4,019** |
| B5 | SHOULD | | | 550 full / 193 reduced (days 36–48, S-1) | | 550 / 193 |
| B6 | SHOULD | | | 391 full / 236 reduced (signal arm in days 36–48, S-1) | | 391 / 236 |
| B7 | SHOULD | | | 5 | | 5 |
| **Total** | | 506 | 580 | 3,684 / 3,171 | 196 | **4,966 full / 4,453 reduced** |
| **day-15 redirection reserve** (rule 3 of §11.7; spent by default, so inside the approved figure) | | | | 156 | | **156** |
| **Approved figure** | | | | | | **5,123 full / 4,609 reduced** |

C3 costs no CPU. The no-pile-up pool of 665 CPU-h (chain and Geant4 vertices) is split between B1 (208) and B4 (457).

**Three variants.** The approved figure of each is its total plus the 156 CPU-h day-15 reserve [E, script [4], [7]].

| variant | approved CPU-h | production of Phase 4a on the critical path | calendar (§11.3) | stop-and-ask threshold (1.3×) |
|---|---|---|---|---|
| MUST only | 4,019 + 156 = 4,176 | 2,333 CPU-h = 13.4 days | 56.9 days = 8.1 weeks (58.9 with the expected day-15 pause) | 5,429 |
| MUST + SHOULD reduced ([DP1], [DP2]) — **proposed** | 4,453 + 156 = **4,609** | 2,489 CPU-h = 14.3 days | **57.8 days = 8.3 weeks (59.8 with the expected day-15 pause)** | **5,992** |
| MUST + SHOULD full | 4,966 + 156 = 5,123 | 2,542 CPU-h = 14.6 days | 58.1 days = 8.3 weeks (60.1 with the expected day-15 pause) | 6,660 |

The critical-path production is the 4a total minus what S-1 moves to days 36–48 (B5 and the B6 signal arm: 277 CPU-h
reduced, 737 full) plus the reserve; the S1 chain, the moved work and the pass-1 toys (940 CPU-h reduced) run between
the end of production and Gate B, where 2,350 core-h are available [E, script [7]].

**Changes against version 3 [E, script [4], [5′]]:** +6.0 CPU-h for the Geant4 vertices of the pilot's unbiased DIF
and NI events and +7.0 for 1,000 unbiased Geant4 DIF development overlays (P4; idle pre-freeze capacity); +26.0 for the
paired pile-up-only finder pass (P5; +0.15 day on the 4a critical path); the 156 CPU-h reserve moved inside the
approved figure (P13; +0.9 day); 0 for the pool shares of Z(ττ) and lost-lepton Z(ℓℓ) (P1, inside the 665 CPU-h).
Version 3 had 3,945 / 4,378 / 4,891 CPU-h, an approved figure of 4,378 and a threshold of 5,691; the earlier
increases are itemised in the fix reports of cycles 1 and 2.
**Changes against version 4 [E, script [4], [5″]]:** +35.8 CPU-h for the paired pile-up-only finder pass on 1,000
test-half events of each of the eleven other SM processes (R5; +0.21 day on the 4a critical path). Version 4 had
3,984 / 4,417 / 4,930 CPU-h, an approved figure of 4,574 and a threshold of 5,946.

**Conditional costs (finding N12).** None of these is inside the approved figure of Q4. Each is reported as an
overrun when drawn (brief D6) and counts in the projection against the stop rule (brief §7) [E, script [6]].

| conditional cost | CPU-h | trigger |
|---|---|---|
| exact toys in both passes | ≤ 236 | the f_T check of §4.11 point 5 fails |
| DIF test sample of 7,750 unbiased events | 19 | pilot enrichment below 1.7 (§4.4) |
| second direct pile-up sample | 403 | INVESTIGATE or a bug in a pile-up test (§8) |
| fresh test overlays; fresh hit-level test halves; fresh pool slice for a B3 conditional | ≤ 123; ≤ 163; ≤ 69–80 | INVESTIGATE or a bug (§8) |
| second halves of the staged hit-level samples beyond their planned size | at the measured R06 rate | the first half's rate is below the v1-proxy rate (P14; top-up first from what is left of the reserve) |
| processes of the Q3 annex sized for an evaluable test | ≈ 680 (100–1,230) | only if the user orders it in Q3 |
| S1 generator cut at 150 GeV | costed at day 12 | m_mig > 5 % (§4.13) |
| S1 at 4,000 rows; Stage 2 and 3 after the freeze | +827; +47 (and +1.8 days) | the user overrides Df-1; the user answers "no" to Q5 |

**Unit costs that were never measured, and the contingency listed for them.** Provenance of the reduced total
[E, script [6]]: 753 CPU-h on measured unit costs (M), 2,322 on derived ones (D), 1,378 on guesses (G); the CPU-h per
unit cost and the measurement that fixes each are the last column of Table 4.0. The contingency sized this way (10 %
of M, 30 % of D, 100 % of G) is **2,150 CPU-h**. It is an exposure, not a plan, and it is not pre-approved (Q4): if
every guess doubled, the projection would be 4,609 + 1,378 = 5,987 CPU-h, just below the stop-and-ask threshold of
5,992 [E, script [6]].

### 11.3 Order, critical path, parallel channels (days after Gate A; proposed variant; days without the day-15 pause, every day after 15 moves by ≈ 2 in the expected branch)

| days | phase | critical path | in parallel |
|---|---|---|---|
| 0–5 | 2 | three agents (slot table below): (i) C1 campaigns (198 CPU-h) and C2 (81), with the sealed C1 comparison as a short separate session inside this slot; (ii) S2, P1, the retrieval tasks (R-3 and R-2 first), the Herwig install attempt; (iii) the pilot (61), the T1 workspace builder on v1 counts, Geant4 geometry, material scan (B1-d) and hand-over code. Day 0: ρ = 2 memory and storage, unit-cost timing jobs, first measurement of the utilisation. **Decision point 1 and stop-rule checkpoint 1 at day 5** | — |
| 5–17 | 3 | three channels: (i) B1 + B3: classification of the pilot's records (by day 7), classes on hit subsets, S_CKF, ceiling and completeness tests on development samples, per-k promotion on the pilot's overlays, conditionals, secondaries test; (ii) B2: re-grouping, N_eff per rung, occupancy model with correlations, crossing rungs (to day 16), then the one Phase-3 1-bot review of `SELECTION.md` (days 16–17); (iii) T1 + B4: MET model and its validation (by day 10), A and m_mig (day 12), zero-count tests (days 5–12), then the `PREREG_v2.md` drafter with the T2 script and G from the v1 row arrays (days 12–17). **Rule 1 of decision point 2 preliminary at day 7, binding at day 15** (§11.7) | S1 string propagation (266 CPU-h, days 12–19); enlarged development samples (100 CPU-h); development overlays (7 CPU-h) |
| 17–19 | freeze | 4-bot review of `PREREG_v2.md`, hash, commit, user notified; **stop-rule checkpoint 2** | — |
| 19–21 | | allowance for one ITERATE of the freeze review | |
| 21–35.3 | 4a | production of the background samples, 2,489 CPU-h at 174 per day = 14.3 days: B2 direct and ρ = 2 → no-pile-up pool (with the day-15 reserve by rule 3) → overlays → B4 hit level in two stages → B6 background arm | closure analysis as each campaign ends; the BDT recipe; T1 expected results with v1 placeholders; note sections 1–6 and 8–10 drafted |
| 35.3–36.8 | 4a | closure analysis of the last campaign, T1 expected results, note and PDF (bought by S-1) | — |
| 36.8–39.8 | 4a review | 4-bot + bib on the compiled note (B5 and B6 stated as pending); **decision point 3a: closure verdicts recorded** | S1 chain, both halves, not aggregated (561 CPU-h); B5 (183) and the B6 signal arm (95), moved by S-1; none needs a verdict and no verdict needs them |
| 39.8–41.8 | | allowance for one ITERATE of the 4a review | S1 chain, B5 and B6 end |
| 41.8–44.8 | 4b | T2 on the optimisation half; toys pass 1 (101 CPU-h, 0.6 day); B5 and B6 read; 4-bot + bib | — |
| 44.8–48.8 | | allowance for one ITERATE (2 days); **Gate B** turnaround (2 days; verdicts first) | — |
| 48.8–51.8 | 4c | evaluation half: efficiencies, toys pass 2 (61 CPU-h, 0.3 day), limits, reach; BDT and dE/dx ratios; 1-bot review | — |
| 51.8–57.8 | 5 | note and paper completed (results section, abstract, C3 list), package; 5-bot + adversarial review against §10; allowance for one ITERATE (2 days); **Gate C** | — |

**Agent slots (finding P16; executors + reviewers + drafter, at most three at a time).**

| window | slot 1 | slot 2 | slot 3 |
|---|---|---|---|
| Phase 2, days 0–5 | channel (i): C1, C2; then the sealed C1 comparison (a separate short session, run sequentially in this slot) | channel (ii): S2, P1, retrievals, Herwig | channel (iii): pilot, T1 builder, Geant4 geometry |
| Phase 3, days 5–12 | channel (i): B1 + B3 | channel (ii): B2 | channel (iii): T1 + B4 |
| Phase 3, days 12–16 | channel (i) | channel (ii) | `PREREG_v2.md` drafter (channel (iii)'s second task) |
| Phase 3, days 16–17 | channel (i) | the one 1-bot review of `SELECTION.md` (JFC tier) | drafter |
| freeze review; 4a, 4b and Phase-5 reviews | physics reviewer | critical reviewer | constructive reviewer; the arbiter after them, in a freed slot |
| 4a production, days 21–36.8 | closure analysis (B1, B3) | closure analysis (B2, B4) | T1 expected results and note drafting |
| 4c | executor | 1-bot reviewer | — |

Campaigns that run during a review (the S1 chain, B5, the B6 signal arm) are queued before it and need no agent
until they are read in 4b.

**Calendar estimate: 60 days from Gate A in the expected branch (57.8 days plus the ≈ 2-day turnaround of the day-15
pause under Q2 (a)); 58 days if the pause does not fire.** 43.5 of these days contain no production on the
critical path: 19 days of development and freeze before production, 14.5 days of analysis, reviews and writing after
it (with the 1.5-day closure buffer before the 4a review), 8 days of ITERATE allowances (one per panel review, as this
phase itself shows is realistic) and 2 days for the user at Gate B [E, script [7]]. Range: 49 days if every review passes at once and only MUST items run; 65 days if the production utilisation
is 0.50 (both without the day-15 pause); +8 days if each panel review needs two ITERATE cycles. If a C1 family fails and needs remediation, decision
point 1 and the whole calendar move day for day, and the delay is reported under brief D6.
**Development effort.** PLAN estimates B1–B4, T1 and T2 at about 35–50 person-days (PLAN l.298-366). The slot table
gives 30 channel-days of development, 5 of drafting and 1 of review in Phase 3 (36 = 3 × 12), below the lower end of
that range; the Geant4 hand-over, the T1 builder and the B1-d scan start in Phase 2, and the B5 and B6 prototypes
and the BDT recipe are out of Phase 3 (their definitions are in the pre-registration; prototype runs are not needed
for it). This is the largest schedule risk that CPU does not measure: each 3 channel-days more lengthen Phase 3 by
one day, and decision point 2 moves the freeze if the estimators are not ready.
**Idle capacity before the freeze.** Phases 2 and 3 and the freeze offer 21 days × 116 = 2,440 core-h and use 1,086
[E, script [7]]. Brief D7 forbids production samples before the hash, so the remaining ≈ 1,350 core-h cannot shorten
the production; 100 CPU-h of it enlarge the development samples and 29 CPU-h the pilot.

### 11.4 Storage (cajuela, soft budget 1.5 TB)

| what | GB [E, script [8]] |
|---|---|
| PU-200 chain and trial records: 230,450 events × 0.52 MB | 117 |
| ρ = 2 events with dumps: 4,200 × 4.0 MB | 16 |
| hit dumps for 10,000 events (C2 700; B5 6,500; occupancy model and time tag 2,800; ≈ 2.4 MB each) | 23 |
| ρ = 2 pre-merge candidates (planning value; cap 400) | 200 |
| no-pile-up summaries (1.0×10⁸ events × 50 B) and full records of R04 passers and near-pass events | 30 |
| the pilot's no-pile-up full hit records, classified in Phase 3 (6.3×10⁶ events × 8.2 kB; more for the hard-scatter events; R3) | 52 |
| Stage 2 (LHE and five shower variants), Stage 3 | 11 |
| Geant4 vertices, logs, pyhf outputs, stored toy distributions, repo bundles | 18 |
| crossing-test variables of every candidate passing R05 (fit probability, 2S, shape) | 1 |
| **total** | **≈ 470 (≈ 670 at the pre-merge cap)** |

Geant4 takes 6.6 GB of local scratch per worker. `sw/` on the NFS home is 0.58 GB (FEAS_B [V]); this does not include
the pixi environments under the home (`.pixi`, the workspace `.pixi` directories and the rattler cache), whose size
is reported in `STATUS.md` against the 150 GB software budget. The project stays far from the brief's 2.0 TB
stop-and-ask line.

### 11.5 Proposals that need the user's approval at Gate A (Q4), and later triggers

| label | proposal | saves | lost | carried into the paper |
|---|---|---|---|---|
| [DP1] | B5 with 8 roads on 6,000 SM events with pile-up; hard-scatter T(Δφ) on no-pile-up samples in both variants | 358 CPU-h (0.2 day: after S-1 B5 runs off the critical path) | 45° instead of 18° granularity with pile-up; non-flatness with pile-up ×1.9 less precise; R07 not closed with pile-up (7.7 counts) | §4.8 |
| [DP2] | B6 at 4 points (E 200/1.5, E 500/3, E 500/5, E 1000/3 keV), 300 rows, 600 background events per variation; paired design | 155 CPU-h (0.1 day; the signal arm runs off the critical path) | no variation for the scalar or at 1,500 GeV; unpaired precision 8.2 % instead of 5.2 %; other points by the interpolation rule | §4.9 |
| [DP3] | no MVA as primary selection; BDT cross-check at equal counted background | — | the gain is measured, not used | §3.2 |
| [DP4] | S4 and S5 not included | ≥ 1 week, ≈ 740 CPU-h (S4) | efficiency above 3 keV; m_Q, Λ handles | limitations |
| [DP5] | string against cluster hadronisation at generator level only (K/π and the species fractions that set the decay-in-flight rate), **after an install attempt** | a port of the full chain to a second generator | hadronisation-model systematic on pile-up kinematics limited to tunes | below |

[DP1] and [DP2] are compute-envelope proposals, not failed attempts; they are put to the user, not taken. If the user
declines both, the approved figure grows by 513 CPU-h and the calendar by 0.3 day (S-1 moves B5 and the B6 signal arm
out of the production window).
**[DP5] follows JFC 12 (attempt first).** In Phase 2 (days 0–5) the Herwig installation is attempted on a worker
with the conda-forge package, in the one install slot, to local scratch as for Geant4. If it installs: 10⁶
minimum-bias events at generator level, and the K/π and proton fractions against Pythia in the p_T and η range of
the decays-in-flight term; the difference is the nuisance on rate_DIF (§5.1). If it does not: the failure is
documented with the error, a second route (source build on a worker in `/var/tmp`) is tried once, and only then the
comparison falls back to published minimum-bias data (R-19). The expected size of the effect cannot be quoted from
the repo; R-19 retrieves published differences. In the paper: the systematics table states which comparison was
made; Future Directions names a full-chain second generator.
Triggered later, only after a documented failed attempt: [DT1]–[DT5] (§7).

### 11.6 The 2–4 week target (brief D6) and the stop rules (brief §7)

**The target is missed by four to five weeks, and compute is not the main reason.** 43.5 days of the schedule contain
no critical-path production; this already exceeds 28 days. The production adds 13.4–14.6 days.
*Already taken:* toys parametrised in f_T (the 156 CPU-h they free are the day-15 reserve); Phase 2 and Phase 5
shortened with three agents and early drafting; B5 and the B6 signal arm moved out of the production window (S-1).
*Levers that do not touch a MUST criterion* (offered in Q4): (i) B5 with pile-up on the 500 pile-up events only, the
SM part from the no-pile-up samples alone: −137 CPU-h, no day after S-1; B5-c on SM samples is lost; (ii) reviews that pass at
once save their allowances (up to 8 days); this cannot be planned.
*Levers that touch MUST statistics* (listed for completeness, **not proposed**): S1 at 500 rows at the 15 points
below 1 keV (−158 CPU-h); a smaller pool (the summed floor of Table 4.4a scales as 1/CPU). The B2 direct sample
cannot shrink: at 12,000 events R07 has 35 counts and is no longer evaluable (σ_ln = 0.17 against the limit 0.135).

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
- *Approved schedule* = the variant and the calendar the user approves in Q4. For the proposed variant: 4,609 CPU-h
  (4,453 + the 156 CPU-h day-15 reserve that the default plan spends) and 60 days (57.8 days plus the ≈ 2-day
  turnaround of the expected day-15 pause; a redesign under Q2 (c) is not included and is reported as an overrun). **Every** overrun of either, of any size, is reported in `STATUS.md` and in the next gate package. A
  draw on a conditional cost of §11.2 or on the contingency is such an overrun.
- *Projected overrun above 30 %*: when the projected total exceeds 1.3 × the approved CPU-h (5,992 for the proposed
  variant), **the study stops and the user is asked**.
- *Checkpoints at which the projection is recomputed with measured costs:* (1) day 5, after the Phase-2 timing jobs
  and the first utilisation measurement; (2) at the freeze, before any production; (3) weekly during production,
  from the ledger; and at once whenever a conditional cost of §11.2 is drawn.
- *"A MUST item is infeasible after a real attempt"* applies in particular to B4-b if no MET parameters can be
  sourced from two public documents (§4.7), and to C1 after three remediation attempts (§4.1).
- *Stated risk:* 1,378 CPU-h rest on guesses. If the guesses are low by a factor 2, the projection is about 5,990,
  at the threshold. The day-5 timing jobs fix the unit costs behind 870 of the 1,378 CPU-h (the 45 ms no-pile-up event,
  MLM, FxFx, V4-5 and T_seed, the toy scaling); the Geant4 spectra and variations (67, G), the Geant4 vertex yield
  (98, D) and the 442 CPU-h of allowances are fixed only at checkpoint 2 or later [E, script [6]]. The rule may
  therefore trigger at checkpoint 1 or 2. The user should expect that this may happen (Q4).
- The storage rule is far from binding (470–670 GB against 2.0 TB); the pool's free space is checked before each
  campaign.

### 11.7 Decision points of PLAN §8

| # | question | when | if "no" |
|---|---|---|---|
| 1 | is the v1 chain reproducible on Linux (C1) and does the finder pass (C2)? | day 5 | regression; Phase 3 does not start on the failed family |
| 2 | are the estimators inside their caps on the development samples, and what do the pilot and the development samples say about the outcome class? (rules below) | day 15 | redesign before the freeze; the freeze moves; user informed |
| 3 | after production: background verdicts, then signal | days 36.8–48.8 (Gate B at ≈ 49), without the day-15 pause | failed terms reported; eligibility rule [SD8] |
| 4 | include the endcap? | — | void: dropped by brief D1 |

**Decision point 2: what is measured by day 15 and what follows (fixed now).** Inputs: from the pilot (generated by
day 5, classified provisionally by day 7 and finally by day 12), the ceiling counts m_H per term at every T2 candidate, read as Gamma(m + 1), the R06–R07 counts with the fall
per width step the pilot measures, the enrichment 1/H(R06) and the gains G_t (§4.4 point 5); from the development
samples, the r.m.s. of ln r of every estimator, the completeness fractions with the expected mixed excess (§4.4 point
4), S_CKF on the development overlays (used only in the test of a Q2 (c) redesign), the per-k promotion comparison on the pilot's overlays, the evaluability of the
crossing rungs and the secondaries test; from the MET model (day 12), the N_trig of Z(ττ), lost-lepton Z(ℓℓ) and the
multijets; for the eleven small SM processes, v1-proxy R06 rates labelled with their errors (no Phase-3 SM sample
exists, §4.7); the retrievals.
1. *Projection.* The projection is recomputed **for every term of the likelihood** from the samples that exist at day 15,
   with max(zero-count floor, N_t·H) per term: H is Gamma(m + 1)/M for the own-hit count m of the pilot sample of M
   events, and the zero-count floor is its m = 0 case on that sample, not the Table 4.4a floor of a pool that does not
   exist yet. Decays in flight and each nuclear-interaction radius are read on their own pilot samples (10⁶ events
   each). Every SM hard-scatter process and the multijets (the three additions at their MET-model N_trig) are read at
   the H per event of the Z(νν) pilot (2.3×10⁶ events; one count m_Z for all of them, their conversions included),
   since no sample of another SM process exists before the freeze. The reading is therefore a function of the pilot counts alone
   (script [9b], v9 table: one Z(νν) pilot count is 18 events, one decays-in-flight pilot count 65). The pile-up term
   is the estimate of the development occupancy model (at day 7:
   the v1-based EST pile-up rows of Table 4.4c, since the occupancy model is developed in channel (ii) of Phase 3,
   days 5–16, and its R04–R05 inputs, the ρ = 1 development sample of the Phase-2 C1 campaigns, are evaluated with it
   by day 14 at the latest; at day 15: the development model's R04–R07 inputs). It is
   computed **preliminarily at day 7** from the finished pilot and reported in `STATUS.md`; it is conditional on C1
   PASS for the no-pile-up family (C′₀), and if that family fails, the pilot is re-read (or re-run, 61 CPU-h in idle
   capacity) after remediation; and it becomes binding at
   day 15. The projection of a no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional credit
   (Df-9); its DIF and conversion terms are therefore expected ×1/(1 − ε_pair) above their after-CKF sizes
   (×5–50 at the assumed ε_pair = 0.8–0.98; the conversions as the Z(νν) pilot counts them, 5.9×10³ events after CKF by
   v1's Z(νν) photon rate against the 6.4–9.5×10³ of Table 4.4c; script [9b], v9 table). Only the test of a Q2 (c) redesign multiplies
   the leading terms by the redesigned conditional and by S_CKF, each estimated on development samples (the C′_PU γ
   sample, the DIF overlays 13a, the pilot's near-pass overlays; with the rider, the 1,000 γ overlays) and labelled
   EST. A development survival or conditional fraction enters that test at its 68 % upper value (Gamma(m + 1) on its
   m survivors, as H does for the pilot), never at a central zero: a sample with no survivor among n attributed
   candidates demonstrates a rejection of at most ×n/1.14. These factors multiply a counted term, never its zero-count floor. No credit in the result comes from these estimates. B₅₀ is read at the best candidate: the candidate with the lowest G (§4.12 rule 3), computed before the
   freeze with v1 placeholder efficiencies and this projected background (§4.12 rule 4). If B₅₀ is at most 300
   events (the bounded class of Q2: reach about 560 GeV or more by the computation of Table 4.4c; on the pilot, the limit is at ≈ 12
   Z(νν) pilot counts with the other pilot counts at zero, or between 3 and 4 decays-in-flight pilot counts, both at the R09 pile-up estimate (at fewer counts at an R08 candidate, Q2 caption); the reading of each branch is the v9 table of script [9b]), production proceeds and the user is informed in `STATUS.md`. If it is larger, or if both pile-up estimators
   are above their cap, the outcome class has changed: the study pauses and the user is asked. The binding B₅₀ is the median of at least 10⁵ draws (precise to about 0.3 %), and a reading within that precision of 300 counts as larger. By v1's own conversion
   counts (scenario (α1′) of Table 4.4c) this is the expected branch; what follows is Q2.
2. *Cap on s_model* (§4.0 point 4 (c)). An estimator above its cap is redesigned if a cause is found by day 15;
   otherwise the pre-registration declares it "not submitted" and its factor has no credit (a Q3 route).
3. *Redirection reserve: 156 CPU-h* (inside the approved figure, §11.2). (a) If the largest term of the projection is
   a zero-count floor (its ceiling empty by the pilot's R06–R07 counts extrapolated with the pilot's own fall, EST),
   the reserve goes to the pool, re-allocated as √(N_t/(c_t·G_t)); at G = 1 the summed pool floor falls from 12.6 to
   10.2 events. (b) If a counted ceiling leads the projection, more pool events do not lower it, and the reserve goes
   to testing that term's estimator at R06–R07, by its enrichment E = 1/H(R06): E ≥ 10², enriched test overlays (or
   enriched hit-level events) sized for N ≥ 24; 10 ≤ E < 10², the same, paid by the reserve and then by the unbiased
   sub-topology overlays down to 500 events each; E < 10, the term stays at its ceiling, which Q3 covers.
4. *Untested SM processes and the four supplied terms (Q3).* The sizes of W(τ_h), W(τ_ℓ) and tt̄ 1ℓ and the test of
   any annex process whose evaluable test half would cost at most 40 CPU-h use v1-proxy R06 rates at day 15. The 4a
   hit-level campaigns are **staged**: the first half of each sample is produced and its R06 rate measured (on its
   derivation parity half, so the test half is not looked at before its prediction exists); the
   second half is sized from it, topped up from what remains of the reserve (in decreasing order of N_trig) or by a
   conditional draw reported as an overrun. The others enter at H if Q3 is approved as recommended, or are supplied
   at the stated cost if the user orders it.
5. *Completeness, promotion, CKF factor, secondaries, crossing rungs:* the rules of §4.4 point 4, §2 and §4.0 point 7.
   A redesign moves the freeze and the user is informed.
6. *Pool shares of the additions:* re-allocated at day 12–15 from the MET-model N_trig by the rule of §4.4 (inside
   the 665 CPU-h, before any pool event is produced).
7. *Retrievals:* the consequences of §6.4.

---

## 12. Decisions for the user, open issues, and how this study could fail

### 12.1 Decisions requested at Gate A

Five questions, one line each as an answer (for example "Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ●"). ● marks the recommended
default, which this strategy follows if it is approved. CPU-h and days are from the script (days at 174 core-h per
production day). Every reach number is EST: the plan's reach table with v1 placeholder efficiencies, best Λ per mass
(Table 4.4c, §0).

**Q1, C1 blinding exception.** May the C1 reproduction compare six v1 signal counts that are also v2 candidate
efficiencies, before the closure verdicts? (brief §7; §4.1)
> ● Yes, sealed: PASS/FAIL only until Gate B, four counts open; a sealed FAIL cannot be diagnosed from its size.
> Alternatives: all ten open and disclosed (two candidates known to ± 16–23 % at 3 of 20 window points before the
> verdicts); or the six dropped (v1's best-point count is not reproduced). Cost: 14 CPU-h in every option.

**Q2, the deliverable if the background is large (the expected case).** By v1's own counts (ESTIMATE, v1 placeholder
efficiencies, best Λ per mass), hard-scatter conversions leave ≈ 0.7–1.0×10⁴ background events at the R08–R09
selections (after CKF, as v1 counted them; a lower value, since terms whose S_CKF test is not evaluable stay on all own
hits, annex route 6). v1 counted 86 → 13 → 2 conversions per 500 events at R05–R07, a fall of ×6.5 per width step against
×200–340 for the pile-up background, and a pile-up-like fall is rejected at p ≈ 10⁻³. With the normalisation width
this strategy assigns to that background (≈ 0.17, §4.7) the reach is below 243 GeV, at or near the existing bounds;
the statistics-only values are ≈ 270–300 GeV at the 84 % edge and ≈ 390–420 GeV for a background known exactly. The
day-15 rule (preliminary at day 7) is expected to pause the study before production. The day-7 and
day-15 projections read the pilot's own-hit counts before CKF, with no S_CKF and no conditional credit (Df-9, §11.7 rule 1);
their decays-in-flight and conversion terms are ×5–50 above the after-CKF sizes (ε_pair = 0.8–0.98, assumed, not
measured). What the day-15 rule reads (planning EST; a digest of the printed lines below; B₅₀ against the limit 300):

| pilot counts (branch) | day-15 B₅₀ (rule 1) | vs 300 |
|---|---|---|
| (α1′), v1's conversion counts (expected) | ≈ 3.2–3.3×10⁴ (ε_pair 0.8) to 3.2–3.3×10⁵ (0.98) | above |
| (α1), decays in flight and conversions falling like pile-up, no credit | ≈ 2.6×10³–4.2×10⁴ | above |
| Z(νν) pilot count, the others zero; (β) and (γ) are read through this count | 281 at 11, 300 at 12, 317 at 13 | below up to 11, at the limit at 12, above from 13 |
| decays-in-flight pilot count, the others zero | 266 at 3, 331 at 4 | below up to 3, above from 4 |
| every pilot count zero | 76 (16–84 %: 37–152) | below |
| only in the test of a (c) redesign (EST): (α1) with fit-probability credit on decays in flight and conversions | 109–130 | below |

*Day-15 table, printed lines (script [9b], `budget_stdout_v9.txt` l.354–364, verbatim).* Rule 1 (§11.7) reads every term at max(zero-count floor, N_t·H) from the pilot's own-hit counts before CKF, on the samples that exist at day 15 (decays in flight and nuclear interactions on their own pilot samples; every SM hard-scatter process and the multijets at the H per event of the Z(νν) pilot), with no S_CKF, no conditional credit (no veto, no fit-probability credit), no credit that exists only after the freeze and no pool floor; threshold: the study pauses if B₅₀ > 300 events. ESTIMATE, v1 placeholder inputs; the decays-in-flight term rests on 1–2 v1 counts; the ×5–50 between the before-CKF reading and the after-CKF size rests on an assumed pair efficiency (ε_pair = 0.8–0.98, not measured); the pile-up term is the R09 estimate (median 6.7 events; 88–148 at an R08 selection, Table 4.4c), so the limits in pilot counts hold at an R09 candidate; at an R08 candidate the pile-up term alone takes 88–148 of the 300 events and the limits are about half as high (≈ 6–7 Z(νν) or 1–2 decays-in-flight counts at the R08 median of 118 events: physics review and arbiter verdict of cycle 9, not a script-printed number). Reading every other SM process and the multijets at the Z(νν) H per event is a proxy, not a measurement: by v1's photon rates (0.231 for Z(νν), 0.255 N_trig-weighted, 0.379 at most) the pilot's count under-reads their conversions (5.9×10³ events against 6.4–9.5×10³, that is by ≈ 8 % and at most ×1.6; §11.7 rule 1), and the other near-pass rates of busier processes (tt̄, W) are not measured, so the rule errs on the lenient side; the (c) bar below is quoted at 0.255 and 0.379 for this reason. The pilot is small: four decays-in-flight counts alone pause the study. Rows marked (c) exist only in the test of a Q2 (c) redesign (conditional and S_CKF estimated on development samples, EST).

```
  v9 (W1): day-15 reading under §11.7 rule 1, a function of the pilot counts alone (own hits before CKF, no S_CKF, no conditional, no post-freeze credit; the study pauses if B50 > 300)
  basis: events in 3 ab^-1 per pilot count: DIF 65.1 (1e6 events); NI 0.88 / 1.12 / 1.12 (1e6 events per radius); every SM hard-scatter process and the multijets through the Z(nunu) pilot count: 18.1 (= (sum N_t + N_MJ) / 2.3e+06 = 1.66 x Z(nunu)'s own 10.9); pile-up R09 EST median 6.7; no pool floor enters; medians of 20000 draws (seed 7)
  (the v6 (T2) and v7 (U1) lines above are on the Table 4.4c basis: pool floors, conversions of all processes at the photon rate 0.379; they are not the day-15 reading, which is this table)
  | pilot counts (branch) | B50 at day 15 | vs 300 |
  | every pilot count zero | 76 [16-84 %: 37-152] | below |
  | Z(nunu) pilot count m_Z, DIF and NI counts zero; m_Z = 2 / 5 / 8 / 10 / 11 / 12 / 13 / 15 / 20 | 115 / 170 / 226 / 263 / 281 / 300 / 317 / 353 / 445 | below / below / below / below / below / at the limit / above / above / above |
  | DIF pilot count m_D, Z(nunu) and NI counts zero; m_D = 1 / 2 / 3 / 4 / 5 | 138 / 202 / 266 / 331 / 397 | below / below / below / above / above |
  | (gamma), and (beta) at day 15 (its Z(nunu) credit exists only after the freeze): the Z(nunu)-count row; m_H = 10 / 30 / 60 / 100 pool-equivalent counts = m_Z 2.1 / 6.3 / 12.6 / 20.9 | 117 / 195 / 309 / 462 | below / below / above / above |
  | (alpha1), no credit: decays in flight and conversions falling like pile-up; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 31-53, m_D 30-50 | ≈ 2.6e+03-4.3e+03 / 2.5e+04-4.2e+04 (sum of medians) | above |
  | (alpha1'), no credit (expected branch): conversions at their own fall; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 1632, m_D 30-50 | ≈ 3.2e+04-3.3e+04 / 3.2e+05-3.3e+05 (sum of medians) | above |
  | (c) only (EST): (alpha1) with fit-probability credit 2/35 (v1's central pile-up fraction; the test takes its 68 % upper value) on decays in flight and conversions (photon rate 0.379), after CKF; x339 / x201 | 109 / 130 | below / below |
```

Upside (statistics-only; with the width 0.17 the (α1) edge
is ≈ 310–370 GeV): if the conversions and decays in flight fall like the pile-up background, ≈ 420–455 GeV at the
84 % edge (median 470–500; ≈ 400–570 for the factor-e size uncertainty). This branch also pauses (table). Further upside, after the freeze and statistics-only: (β), Z(νν) tested and the
other ceilings at 10–100 simulated counts, conditional on the promotion model being submitted, ≈ 705–640 GeV; every
ceiling empty, ≈ 710 GeV (median 790), an upper edge. Their day-15 readings are the Z(νν)-count and zero-count rows of
the table. Existing bounds lie below about 180 GeV (R-20 pending). (§0, Table 4.4c, §11.7)
If the day-15 projection exceeds B₅₀ = 300 events (or both pile-up estimators miss their cap), what should happen?
> ● (a) Pause and ask you at day 15: production waits for your answer (≈ 2 days of turnaround); the 156 CPU-h
> reserve is spent by rule 3(b) on testing the leading term at R06–R07. You then choose (b) or (c).
> (b) Authorise now to proceed with the measured background: no pause for this cause, 0 extra CPU-h, no delay. Paper:
> the plan's "real background" outcome: the first measured quirk-plane background (led by conversions), the reach at that B,
> expected below 243 GeV, at or near the existing bounds, with the planned normalisation width (≈ 270–420 GeV only
> for a background with no width beyond its counting width), and the sideband recipe as the way out. In the expected
> case this paper reports no mass reach beyond the existing bounds; (c) is then the route this strategy designs for
> one; the conditionals measured in production may add some reach, with credit not yet measured.
> (c) Authorise now a redesign before the freeze: a conversion-removing conditional developed and tested on the
> development and pilot samples; the freeze and everything after move by the redesign time (not estimable now,
> reported at day 15), CPU-h inside the development allowance and what remains of the reserve. Paper: the bounded "middle" outcome
> (upper branches above) if it works, otherwise (b). It works if the projected B₅₀ is at most 300, with the
> redesigned conditional and S_CKF estimated on development samples (EST, §11.7 rule 1). At v1's central decays-in-flight size (385–647 events,
> resting on 1–2 counts) no conversion rejection suffices: with the conversions removed, B₅₀ is 458–718. The
> conversion rejection needed (script [9b], v9 table; v1's maximum photon rate 0.379, with its N_trig-weighted rate
> 0.255 in brackets) is at least ×44 (97.7 %) [×30] even if the pilot counted no decay in flight, ×75–150
> (98.7–99.3 %) [×51–101] at a quarter of v1's size, and ×114 (99.1 %) [×77] at ×e⁻¹ with the pile-up fall ×339; at
> ×e⁻¹ with the fall ×201 none suffices. A development sample with no surviving conversion among n attributed
> ones demonstrates at most ×n/1.14 (§11.7 rule 1). These factors assume S_CKF estimated for both terms. If S_CKF
> cannot be estimated before the freeze, the factor is ×219–2,186 with no decay in flight in the pilot, and no
> conversion rejection suffices from a quarter of v1's decays-in-flight size on (ε_pair = 0.8–0.98, not measured).
>
> *(c) rejection grid, printed lines (script [9b], `budget_stdout_v9.txt` l.365–370, verbatim).* The smallest conversion
> rejection with which the (c) test reads B₅₀ ≤ 300 (the pause threshold), by the size of the decays in flight (f_D × v1's
> central size; (α1) decays in flight at the pile-up fall ×339 / ×201). Basis: the pilot's transfer factors of rule 1
> (no pool floor); decays in flight and conversions after CKF, as v1 counted them (the (c) test with S_CKF estimated at
> v1's level), their zero-count floors kept without credit; no credit that exists only after the freeze; the rejection
> itself is the (c) test's conditional (EST). The photon rate sets the size of the conversions: v1's maximum over
> processes (0.379), its N_trig-weighted mean (0.255), and v1's Z(νν) rate (0.231), which is what the pilot's count
> would read. ESTIMATE, v1 placeholder inputs; the decays-in-flight term rests on 1–2 v1 counts; a factor is precise
> to about 3 %.
>
> ```
>   | (c) only (EST): smallest conversion rejection with B50 <= 300, by the decays-in-flight size f_D x v1's central size ((alpha1) DIF at fall x339 / x201), decays in flight and conversions after CKF (S_CKF estimated), the zero-count floors kept; conversions at v1's photon rate; a factor is precise to about 3 % |
>   |   f_D = 0 (pilot count zero) | B50 with the conversions removed 76 / 76 | 0.379: x44 (97.7%) / x44 (97.7%); 0.255: x30 (96.7%) / x30 (96.7%); Z(nunu) 0.231 (the pilot's own): x28 (96.4%) / x28 (96.4%) |
>   |   f_D = 1/4 | B50 with the conversions removed 168 / 233 | 0.379: x75 (98.7%) / x150 (99.3%); 0.255: x51 (98.0%) / x101 (99.0%); Z(nunu) 0.231 (the pilot's own): x47 (97.9%) / x93 (98.9%) |
>   |   f_D = e^-1 | B50 with the conversions removed 213 / 309 | 0.379: x114 (99.1%) / none suffices; 0.255: x77 (98.7%) / none suffices; Z(nunu) 0.231 (the pilot's own): x71 (98.6%) / none suffices |
>   |   f_D = 1 (v1's central size) | B50 with the conversions removed 458 / 718 | 0.379: none suffices / none suffices; 0.255: none suffices / none suffices; Z(nunu) 0.231 (the pilot's own): none suffices / none suffices |
>   |   without an S_CKF estimate (own hits; eps_pair 0.8 / 0.98, assumed): f_D = 0: x219 / x2186 at 0.379; f_D >= 1/4: none suffices (decays in flight alone: B50 ≈ 545 or more) |
> ```
>
> As worded, (c) targets the
> conversions; if you choose it, say whether it may also target the decays in flight. At v1's central size (c)
> cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 109–130) acts on both. The veto's rejection has not
> been measured; its signal cost is known only at Gate B, and T2 keeps every selection with and without it.
> If the projection is at most 300 events (reach ≈ 560 GeV or more, statistics-only), production proceeds in every option and the paper
> is the plan's "middle" outcome, labelled "target not met: sample-size limited". A doubled pool (+665 CPU-h,
> ≈ +3.8 days) helps only if the ceilings are empty (median 790 → 814 GeV, script [9b]) and does not help in the
> expected case.
> *Optional rider (recommended by the cycle-5 review, not part of the default; answer "Q2 ● + rider" to accept):*
> (1) if the day-7 preliminary B₅₀ is at least 3,000 events (10× the class) (expected to trigger in the expected branch (α1′): the day-7 reading is expected at ≈ 3×10⁴–3×10⁵; in the (α1) branch the lower edge of the reading is below this trigger, v9 table), the choice between (b) and (c) is put to
> you at day 7 instead of day 15, and the day-15 rule stays binding; (2) channel (i) reports by day 12, as a
> development number and not a credit, the pilot's ceiling counts split by truth origin and the fraction of
> conversion-attributed configurations at R05–R07 with a reconstructed two-prong vertex (0 CPU-h, on the stored
> records); (3) 1,000 γ development overlays, in addition to the 1,000 DIF overlays of P4 (seeds disjoint from 4a) check v1's ×6.6 fall with pile-up on the v2
> chain by day 12 (+7.0 CPU-h: approved 4,616, threshold 6,001; script [7], rider line). Gain: under (c), up to ≈ 8
> days earlier [E: day 15 − day 7]. Cost of declining: those days, nothing else.

**Q3, brief D4 exception, completed.** For every MUST closure criterion that ends NOT TESTED, NOT EVALUABLE or not
submitted (by planned statistics, by a fluctuation, by the cap rule or by a day-15 rule), may the factor enter at no
credit (the term at its tested ceiling H), with the selection eligible, labelled "no credit" in the paper and in the
ladder figure, and reported in `STATUS.md`? (annex below)
> ● Yes. Routes (annex): planned statistics (the eight proxied processes, the three additions); a fluctuation of the
> four supplied terms (≈ 30 %; compliance by the staged top-up, 0 CPU-h); the cap rule; B3-a…d and B4-e (a B4-e
> failure alone sets a floor of ≈ 4.6×10³ events); B2-c at depth; the promotion model not submitted; S_CKF not tested.
> Reach under the default: (β) of Table 4.4c: 705–640 GeV at the 84 % edge for ceilings of 10–100 counts, if the
> promotion model is submitted (ESTIMATE, v1 placeholder efficiencies).
> Rule 3 may already have spent the reserve, so the top-up can be a reported overrun.
> Alternatives: comply where costed (≈ +680 CPU-h, 100–1,230, ≈ +3.9 days for the eight processes; per-row costs in
> the annex); or strict: such selections are not eligible, and "closure fails" becomes a likely paper.

**Q4, budget, calendar and stop rule.** Approve **4,609 CPU-h** (4,453 + the 156 CPU-h day-15 reserve; the 39 + 36 =
75 CPU-h of review additions of cycles 3 and 4 included) and **60 days** (57.8 without the day-15 pause; under the
recommended Q2 (a) the pause is the expected branch and costs ≈ 2 days of turnaround, so the approved calendar
includes it; a redesign under Q2 (c) adds its own time, reported at day 15) (against your 2–4 weeks; 43.5 days have no
critical-path production: development and freeze 19, ITERATE allowances 8, Gate B, reviews and writing), with [DP1]
(B5 sideband reduced, §4.8), [DP2] (B6 detector variations reduced, §4.9), [DP4] (S4, S5 not included) and [DP5]
(second hadronisation model at generator level after an install attempt)? (§11; the stop conditions of brief §7 are
quoted in §11.6)
> ● Approve. The stop-and-ask threshold is 1.3× that, **5,992 CPU-h**. The contingency (2,150 CPU-h; 1,378 rest on unit
> costs never measured) and the conditional costs of §11.2 are listed, not pre-approved; every draw is reported as an
> overrun. The day-5 or freeze re-projection may trigger the stop rule (all guesses doubled: 5,987 CPU-h).
> Alternatives: pre-approve the envelope 4,609 + 2,150 = 6,759 (threshold 8,787); MUST only, 4,176 CPU-h and 59 days (57 without the pause);
> or full SHOULD (decline [DP1], [DP2]), 5,123 CPU-h and 60 days (58 without).

**Q5, the D7 reading, premise corrected.** May the truth-level S1 samples (Stage 2 and the string propagation, 47 +
266 CPU-h) exist before the pre-registration hash? Their content depends on the MET model, the trigger threshold and
the generator-cut decision, all frozen by day 12 before the propagation, but on no plane-selection choice and on no
signal efficiency at any T2 candidate. (§4.1, §4.17)
> ● Yes: they run in idle pre-freeze capacity (days 0–5 and 12–19); 0 days.
> Alternative: after the hash: +47 CPU-h (a second Stage 2), and the 47 + 266 CPU-h move onto the critical path after
> the freeze: +1.8 days.

**Defaults the user can override (reported, not asked).**

| # | default | alternative and its cost |
|---|---|---|
| Df-1 | 2,000 signal rows per point, a reading of the plan's "×10": ×10 rows in total, ×5 on the half that sets the limit (15 % error at ε = 0.045) | 4,000 rows: 10 %; +827 CPU-h, +4.7 days |
| Df-2 | closure rules of §4.0: F = 1.5 / 2; s_model ≤ ln F/3; one re-test at p′ ≥ 0.05/K (a stated departure from "p > 0.05", §5.2); K = 10; one ceiling verdict per term, Bonferroni over 19; occupancy crossing comparisons in the fit-probability and shape families are consistency checks without distance credit; ln F per untested rung. A selection is lost to a false FAIL with 6.9–8.9 % | cap ln F/2.5 (closure family 15 % / 6 %); distance as ln F·√d (pile-up width at R14 1.1 instead of 2.5) or in ln of the extrapolated rejection; crossing credit by deriving the fraction at R05 and testing at R09⊗R06 and R09⊗R07 |
| Df-3 | σ_NLO computed here as nominal, the resummed normalisation beside every limit; infracolour correction as a one-sided band (+3 to +13 %) | resummed nominal; correction applied (needs a cited treatment) |
| Df-4 | dE/dx is not a candidate; the forgone efficiency ratio is measured (2 CPU-h) | model the charge deposit: ≈ +390 CPU-h, about one week, a later freeze |
| Df-5 | time-tag credit only at a window edge where its closure on prompt candidates passes, with sourced timing tails | no credit, as in v1 (saves 10 CPU-h) |
| Df-6 | endcap outlook "signal ×1.5–3.2" as fixed by brief D1, EST (the lower end has no derivation in the book) | the wording "×2.1–3.2" |
| Df-7 | a detector variation with no public size gets no nuisance; its μ₉₅ shift is reported beside the limit and named above 10 %. No MET parameters from two public sources: stop and ask | the robustness-test size as a flagged, unsourced nuisance |
| Df-8 | toys parametrised in f_T, with an exact-toy check at three points per selection | exact toys everywhere, chosen up front: +156 CPU-h (the conditional ≤ 236 CPU-h of §11.2 is the switch after a failed f_T check) |
| Df-9 (technical) | H classified on all own hits; CKF removal and f_CKF < 0.2 enter as a survival factor S_CKF, credited only where tested (DIF R06 on the enriched overlays, NI R05 by the rung split, SM R06), carried with s_tot, censored at 1 (§4.4 point 4); it also sets the basis of the day-7 and day-15 projections (own hits, no S_CKF, §11.7 rule 1) | CKF inside H at its pile-up-200 efficiency, with a width |
| Df-10 (technical) | T1 coverage checks (T1-c (iii), T1-h) as one family of 10 against the convention's computed coverage: FAIL below 462 of 500 at 0.95, family-wise 4.7–4.9 %, INVESTIGATE band and one re-test (§4.11 point 6) | the λ values pooled into one check per point (2,000 pseudo-experiments) |
| Df-11 (technical; pinned in review cycle 8) | the reading of §11.7 rule 1: every term is read from the samples that exist at day 15, H is Gamma(m + 1)/M for the own-hit count m of the pilot sample of M events, and the zero-count floor is its m = 0 case on that sample, not the Table 4.4a floor of a pool that does not exist yet; every SM hard-scatter process and the multijets are read at the H per event of the Z(νν) pilot (one count m_Z for all of them, their conversions included), since no sample of another SM process exists before the freeze; the (c) factors multiply a counted term, never its zero-count floor. Consequence: the day-15 threshold is crossed at the Z(νν) pilot count that the Z(νν)-count row of the v9 table of script [9b] (Q2) marks "at the limit" (at the R09 pile-up estimate; at fewer counts at an R08 candidate). The reading is a proxy for the processes without a sample and errs on the lenient side: by v1's photon rates the Z(νν) count under-reads their conversions by ≈ 8 % (at most ×1.6; Q2 caption). Needed because rule 1 as previously written did not say what those processes contribute, so the same pilot result could read as proceed or pause | the other SM processes at the planned pool floors of Table 4.4a, with the Z(νν) count standing for Z(νν) alone. This is more lenient, not stricter: the limit is at about 1.66 times as many Z(νν) counts (the ratio in the basis line of the v9 table), the pilot then sees only the Z(νν) share of the conversions (37 %), and option (c) looks easier. No cost in CPU-h or days (cycle-8 arbiter verdict §1.2, `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`) |

**Annex to Q3: every route by which a MUST closure criterion ends untested** [E, script [11]; v1 counts [V]].

| term or route | criterion | planned test and expected count | status (probability) | cost of compliance | default (size at H) |
|---|---|---|---|---|---|
| DIF | B1-a | R06, 4,000 enriched + 1,000 unbiased overlays: 31 expected (24 needed) | supplied (P = 0.92) | ≤ +19 CPU-h, conditional | — |
| NI at 22 / 30 / 61.5 mm | B1-a | R05 on 1,000 unbiased overlays (rung split): 92 / 120 / 378 | supplied at R05 | 0 (a test at R06: 84 CPU-h per radius) | — |
| Z(νν), W(τ_h), W(τ_ℓ), tt̄ 1ℓ | B4-c | R06 on the hit-level test half: N_eff = 81 / 31 / 31 / 31 expected (24 needed) | supplied (P = 1.00 / 0.92 / 0.92 / 0.92) | +0 / +65 / +40 / +153 CPU-h (in the total) | — |
| **route 1: fluctuation** of DIF, W(τ_h), W(τ_ℓ), tt̄ 1ℓ | B1-a, B4-c | as above | at least one NOT TESTED: **0.30**, before the 33–57 % errors of v1's rates | staged top-up (§11.7 rule 4): 0 CPU-h by default, from the reserve or a reported conditional draw | at H after the ceiling test (floors 3.04, 1.21, 0.78, 0.80) |
| W(eν), W(μν) | B4-c | none evaluable at 2,000 events (no v1 count) | NOT TESTED expected | ≈ +40 CPU-h each if W(τ_ℓ)-like | floors 0.83, 0.78; 6.2 %, 5.5 % of N_trig |
| tW, tt̄ 2ℓ, t-channel | B4-c | as above | NOT TESTED expected | ≈ +153 CPU-h each if tt̄-like | floors 0.26, 0.24, 0.17 |
| WW, WZ; ZZ | B4-c | as above | NOT TESTED expected | ≈ +65 CPU-h each if W(τ_h)-like; ≈ +13 if Z-like | floors 0.18, 0.19; 0.17 |
| Z(ττ), lost-lepton Z(ℓℓ), multijets | B4-c | 1,000-event test half each, planning N_trig only, no v1 count | NOT TESTED expected | known at day 15 from the MET model and v1-proxy rates | floors 0.34, 0.09, 0.46 (Table 4.4a) |
| **route 2: the cap** | every estimator of B1–B4 | development r.m.s. of ln r above ln F/3: not submitted | not computable before Phase 3 (depends on the true model bias) | a redesign before the freeze (decision point 2; the freeze moves) | factor at no credit, term at H |
| **route 3: conditionals and the multijet factorisation** | B3-a, B3-b, B3-d; B3-c at the nominal window; B4-e | B3: unknown until the pool exists; B3-c: 58 late counts expected, 55 needed | B3-c evaluable with P = 0.67; the others unknown | none defined (each is a credit; a tighter window edge is used for B3-c) | factor at 1; for B4-e the passing events only, floor stated |
| **route 4: B2-c at depth** | B2-c | thinning N_eff ≈ 80 at R07, of order 10 at R08 | NOT EVALUABLE expected at most deep rungs | more ρ = 2 events only where B2-g shows they buy a rung (206 s each); ρ = 3 is excluded (brief D8) | one-estimator extrapolation with its width |
| **route 5: promotion model not submitted** (fewer than two classes with ≥ 24 promoted events on the pilot's 1,000 near-pass overlays) | B1-a, B4-c (π_k of every credited term) | 4–8 classes of 125–250 events; a class qualifies if π_k ≳ 0.10–0.19; 2–4 expected [E] | EST, not computable before the pilot: unlikely if R04 occupancy is as v1's, not excluded (2–4 qualifying classes expected) | more near-pass overlays from the pilot's events (7 CPU-h per 1,000, development allowance) | every credited B1 and B4 term at H; (β) of Table 4.4c then becomes (γ)-like |
| **route 6: S_CKF NOT TESTED** | B1-f (Df-9) | DIF on the 4,000 enriched test overlays at R06 (31 expected, 24 needed); NI by the rung split at R05 (92 / 120 / 378); SM on the hit-level test halves as B4-c | DIF P = 0.92 (with route 1); NI evaluable; SM as the B4-c rows | as the B1-a / B4-c rows | term at H on all own hits, i.e. ×1/(1 − ε_pair) above H_CKF (×5–50 at ε_pair = 0.8–0.98) |
| **B4-e, size** (in route 3) | B4-e | flatness of P(r) in MET bins on Z(νν) and W | unknown until the samples exist | none (a factorisation test) | multijets from the passing events only: floor N_MJ × 1.14/100 = **4.6×10³ events** at the planning N_MJ (460–46,000 over 0.1–10 %) [E: 4×10⁵ × 1.14/100], by itself above the class B₅₀ = 300 (a floor in the result; the day-15 rule reads the multijets through the Z(νν) pilot count) |
| every term | B1-f ceiling and completeness tests | attributed counts at R04–R05: hundreds (B1 overlays) to thousands (SM hit-level halves) per 1,000 events | evaluable | 0 | a ceiling FAIL removes the term's selections |

Under the default, every term of these routes is labelled "no credit" in the paper and in the ladder figure.

### 12.2 Judgment calls

Judgment calls are recorded as DECISION / ALTERNATIVES / CONFIDENCE / FLAG FOR HUMAN blocks in `experiment_log.md`
(one entry per version, under the name of its author). Those of this version that
reach the user: the planning N_trig of the three additions and their pool shares (Q2; Table 4.4a); how scenario (α)
enters the projection, as counted ceilings (Q2; Table 4.4c); the ceiling family with one Šidák-combined verdict per
term (Df-2); the T1 coverage family (Df-10); H on all own hits with S_CKF (Df-9); the reading of §11.7 rule 1 pinned in review cycle 8 (Df-11); the Phase-3 slot table and the 1.5-day
closure buffer bought by S-1 (Q4).

### 12.3 Other items the user should know
1. **v1 freeze timing** (§8): the paper will say that the v1 analysis code was re-frozen after efficiencies existed.
2. The CMS-internal cross-check listed as open work in v1 (D1 §6) is outside the plan and is not done (public
   information only).
3. Book Part VI did not pass its own review (D3 §6.7); every number taken from it is recomputed from the tracked
   JSON before it enters the paper.
4. The stop rule on compute may trigger at the first or second checkpoint (§11.6): 1,378 CPU-h rest on guessed unit
   costs.
5. **A second, selection-independent blinding exception is declared, not asked** (BL-1, §4.1): the acceptance A, f₂₀₀
   and the migration fraction m_mig exist before the closure verdicts; they are the same for all 16 T2 candidates.

### 12.4 Not resolved in Phase 1
The open inputs and the day on which each is measured are the inputs of decision point 2 (§11.7) and the retrieval
tasks with their deadlines (§6.4). Three further items: v1's coded attribution rule and thinning unit, and whether
v1's probe-row exclusion can be rebuilt (read from the code in Phase 2, §4.1, §4.4); which configuration v1's B*-off
test ran (§4.15); the two utilisation factors (week 1 of Phase 2, §11.1).

### 12.5 What would make this study fail
1. Both pile-up estimators fail B2-a/B2-b, or neither is inside its cap at day 15: no validated pile-up term beyond
   R07.
2. The large no-pile-up samples count zero, biasing gives no gain and the conditionals give no credit: the result is
   bounded by sample size at about 13 events, or at tens to hundreds if a ceiling counts, and near 600–1,000 events
   if decays in flight and conversions fall like the pile-up background (Table 4.4c, (α1); after CKF, as v1 counted them). This is the outcome to
   expect only if the conversions fall faster than v1 measured (point 3); it is a weaker paper, not a failed study.
3. The large samples show passing single-interaction events at a rate that leaves B ≫ 10³: a measured background
   (plan outcome "real background"). By v1's conversion counts this is the expected branch ((α1′) of Table 4.4c:
   ≈ 0.7–1.0×10⁴ events, ESTIMATE, v1 placeholder efficiencies; after CKF, as v1 counted them, a lower value: a term whose
   S_CKF is not tested stays on all own hits, ×1/(1 − ε_pair) higher, annex route 6). With the planned normalisation width (≈ 0.17) the
   reach is below 243 GeV, at or near the existing bounds; it is ≈ 270–300 GeV at the 84 % edge statistics-only.
   The day-15 rule pauses the study (Q2).
4. The Geant4 → Fatras hand-over cannot be made consistent (parent hits, geometry identifiers).
5. C1 fails for the pile-up family: nothing built on the chain can be trusted until it is understood.
6. The finder fails V4-5: every efficiency and rate is in doubt.
7. The MET model cannot be sourced from two public documents: B4-b is infeasible and the study stops for the user.
   The timing tails cannot be sourced: the time tag earns no credit.
8. Infrastructure: NFS or cajuela outages (two incidents on day one, `LOG.md`), memory limits for ρ = 2. A projected
   compute overrun above 30 % of the approved schedule **stops the study until the user decides** (brief §7).
9. A blinding breach: any v2 signal efficiency seen before the verdicts outside the list of §4.1. The C1 comparison
   is the place to watch; the sealed tier exists for that reason.

---

## 13. Changes

### 13.1 Changes since version 1
The findings M1–M35 of the first arbiter and their resolution are in `FIX_REPORT_cycle1_dmitri.md`, with the CPU-h
increase from version 1 to version 2 (2,950 → 3,968 MUST).

### 13.2 Changes since version 2
The findings N1–N18 of the second arbiter and their resolution are in `FIX_REPORT_cycle2_emeric.md`. Two numbers of
version 2 were corrected from the v1 record: the W(τ) counts at R06 are per 1,625 and 375 events, not per 2,000 (at the
bare threshold of 24 the evaluable samples would cost +47 and +28 CPU-h, not +61 and +210; with the margin adopted,
31 expected, they cost +65 and +40); and version 2's headline floor of 45 events contained 18.4 (PV pairs) and 4.7
(γ, V⁰, loopers) counted twice with the SM events.

### 13.3 Changes since version 3 (`STRATEGY_emeric_2026-11-13_21-10.md`)

Findings of the third arbiter (`STRATEGY_ARBITER_v3_felix_2026-11-13_22-40.md`). Details, the old → new numbers and
the neighbourhood checks: `FIX_REPORT_cycle3_fiona.md`.

| finding | what changed | sections |
|---|---|---|
| P1 (A) Z(ττ), lost-lepton Z(ℓℓ) without a pool share | pool shares at EST planning N_trig inside the 665 CPU-h; floor 11.7 → 12.6 (+ multijets 0.46 = 13.0); inventory rows 18a, 18b; re-allocation at day 12–15; rule 1 for every term | §0, §4.4 (Table 4.4a, 4.4c), §4.7, §4.17, §11.7, Q2, Q3 annex |
| P2 headline | scenarios (α), (β), (γ); the headline leads with the 84 % edge and the (α) range; caveats; the day-15 pause a realistic branch; m_H rows relabelled; multijet range | §0, §4.4 (Table 4.4c), §11.7, Q2 |
| P3 CKF in H | table of fixed cuts and monotonicity; H on all own hits with S_CKF (Df-9); m_H EST under option (a) | §4.4 point 4, Df-9, §8 |
| P4 ceiling and completeness samples | unbiased samples only; leak an implementation check; sub-topology ceiling test dropped; development samples named (13a, +7 CPU-h); pilot Geant4 vertices (+6 CPU-h); effective-count form | §4.4, §4.17, §11.2 |
| P5 mixed numerator | paired pile-up-only pass (+26 CPU-h); extended ceiling H′; dated day-15 input | §4.0 point 6, §4.4, §11.7 |
| P6 ceiling family | one Šidák-combined verdict per term, Bonferroni over 19 terms (4.9 %); selection lost 2–4 % → 6.9–8.9 % | §4.0 points 4 and 6, §4.4, §4.12, Df-2, §8 |
| P7 crossing credit | occupancy fit-probability and shape crossing comparisons are consistency checks; occupancy widths 0.45–0.49 → 0.59–3.68 | §4.0 point 7, §4.5, §4.12, Table 4.4c, Df-2 |
| P8 π_k row | "tested at R06 only" row 1.41 / 2.51 (1.42); the R06–R07 row kept as conditional | §4.0 point 7, §4.12 |
| P9 "target met" | every leading term labelled estimate; s_tot printed with each label | §0, §4.11 point 3, COM TG-1 |
| P10 Q3 complete | Q3 covers every route; annex rows for the fluctuation (0.30), cap, B3/B4-e and B2-c routes; consequence under (a) | §4.0 point 6, §11.7, Q3 and annex |
| P11 T1 coverage family | one family of 10 checks against the computed coverage (Df-10) | §4.11 point 6, Df-10, §8, COM T1-c, T1-h |
| P12 Q5 premise | content depends on the MET model, trigger threshold and generator cut, not on any plane selection | §4.17, Q5 |
| P13 reserve | the 156 CPU-h inside the approved figure: 4,378 → 4,574; threshold 5,691 → 5,946 | §0, §11.2, §11.6, Q4 |
| P14 day-15 inputs | no Phase-3 SM samples: v1-proxy rates and staged 4a hit-level production; pilot reading; "best candidate"; rule 1 preliminary at day 7 | §4.4, §4.7, §4.17, §11.7 |
| P15 B1 trace | per-k comparison on the pilot's overlays (sample 11); PREREG outline with ceiling, completeness, c_mix, S_CKF | §4.4, §8, COM B1-f, PR-1 |
| P16 slots | slot table; one Phase-3 1-bot review; drafter in channel (iii) from day 12; sealed comparison inside channel (i) | §11.3 |
| S-1, S-3 (adopted) | B5 and the B6 signal arm in days 36–48 (COM B5 deadlines 4a → 4b); 1.5-day closure buffer; calendar 56.6 → 57.6 days | §4.8, §4.9, §11.2, §11.3, Q4 |
| C items | Ph-C1/K-C5 one NI rate set; Ph-C2 no Geant4 conversions in B1; Ph-C3 B4-c by sub-topology; Ph-C5 occupancy s_model out of sample; Ph-C7 multi-vertex class per rung; Ph-C8 and K-C1 in Df-2 and §5.2; Ph-C9 predictive pile-up cap; K-C2 W(τ) forced-decay samples; K-C6 slab yield; K-C7 four labels in COM; K-C8 wording of §4.17; K-C9 C2-c Bonferroni; K-C11 BL-1 line; K-C12 "thousands"; K-C13 checkpoint coverage; N-C2 "true λ"; N-C4 mapping confirmed; N-C8 R-20 deadline; N-C9 Fig. 7; N-C11 B4 s_model; C1 remediation time | §2, §4.2, §4.4, §4.5, §4.7, §4.11, §4.17, §5.2, §6.4, §9, §11.3, §11.6, §12.3, Q3 annex, COM |
| length (arbiter §6 (v)) | §13.1 and §13.2 reduced to pointers; eligibility logic stated once (§4.0 point 6); §12.4 a pointer; Table 4.0 merged with the §11.2 provenance table | §4.0, §4.11, §4.12, §11.2, §12.4, §13 |

### 13.4 Changes since version 4 (`STRATEGY_fiona_2026-11-13_23-05.md`)

Findings of the fourth arbiter (`STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md`). Details, the old → new numbers, the
diff attribution and the grep phrases: `FIX_REPORT_cycle4_gunnar.md`.

| finding | what changed | sections |
|---|---|---|
| R1 headline | (α1′) leads: conversions at their own fall, ≈ 10⁴ events, ≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 at fixed B); day-15 pause the expected branch; branches quoted as 84 % edge (median); "no fit-probability credit"; reach mapping extended to the 10⁵ column (243 GeV); (α1) × e^(±1) rows; log-normal reading; m_H = 1000 with the count width; (β) at its floor and conditional on the promotion model; conversion m_H of Z(νν) with v1's fall; Q2 rewritten as the deliverable in the expected case | §0, §4.4 (points 4 and 5, Table 4.4c, scenario text), §4.11 point 3, §11.7 rule 1, Q2, §12.5 |
| R2 Q3 annex | routes 5 (promotion model not submitted) and 6 (S_CKF not tested) and the B4-e size; Q3 route list and the (β) reach clause | Q3 and annex |
| R3 pilot records | the pilot keeps its full no-pile-up records (≈ 52 GB), classified by day 7 / day 12; per-k comparison by day 14; day-7 pile-up input | §4.4 points 4 and 5, B1 storage, §11.3, §11.4, §11.7, §0 storage |
| R4 S_CKF samples | DIF on the enriched test overlays, NI by the rung split, SM on the hit-level halves | §4.4 point 4, Df-9, COM B1-f |
| R5 paired passes | +35.8 CPU-h for the eleven other SM processes; no borrowed mixed excess; H′ size sentence; approved 4,574 → 4,609, threshold 5,946 → 5,992, calendar 57.6 → 57.8 days | §0, §4.0 point 6, §4.4 point 4, §4.7, §4.17, §11.1, §11.2, §11.3, §11.6, Q4, COM |
| C items | G-C1 §0 printed figures; G-C2 Df-10 4.7–4.9 %; G-C3 COM REF-2; G-C4 processes vs terms; G-C5/Ph-C4 0.34 [U], 1.1 % and 2.1 %; G-C6 `n_trig.not_included`; G-C9 derivation parity half; G-C11 COM S1-a; G-C14 `s4cp.py` l.115, WZ minimum; N-C1 Q4 clause; N-C4 Q2 turnaround; N-C6 Df-8; N-C11 §11.3 table end; Ph-C7 multijet ceiling and B4-e; Ph-C1, Ph-C2, Ph-C5, G-C10, N-C5, N-C7, N-C9 within R1/R2 | §2, §4.4, §4.7, §11.3, §11.7, §12.1, COM |

### 13.5 Changes since version 5 (`STRATEGY_gunnar_2026-11-14_00-50.md`)

Findings of the fifth arbiter (`STRATEGY_ARBITER_v5_hugo_2026-11-14_01-55.md`). Details, the diff attribution and the
grep phrases: `FIX_REPORT_cycle5_ingrid.md`. Script values bind where they differ from the verdict's draft numbers.

| finding | what changed | sections |
|---|---|---|
| T1 normalisation width | the expected-branch reach stated with the strategy's own normalisation width ≈ 0.17 (< 243 GeV, at or near the existing bounds); the 270–300 / 390–420 GeV values labelled statistics-only; photon-rate range ≈ 0.7–1.0×10⁴ events; upper branches with the same width (α1 edge ≈ 310–370, m_H = 100 454 GeV); script [9b] v6 lines | §0 point 3, "Expected", leading sentence; §4.4 Table 4.4c caption and (α1′) row, scenario (α) text; §12.1 Q2 stem and (b); §12.5 point 3 |
| T2 pause | no (α) branch and no conversion veto alone avoids the day-15 pause (DIF 385–647 events); success condition of Q2 (c): ×31–52 on the conversions and a credit or faster fall for DIF | §0 "The pause."; §4.4 "What is not known"; §12.1 Q2 stem and (c) |
| T3 calendar | approved calendar 60 days (57.8 + ≈ 2-day turnaround of the expected day-15 pause; 58.9 MUST only, 60.1 full); script [7] v6 line | §0 Calendar; §11.2 table; §11.3; §11.6; §12.1 Q4; COM ST-1 |
| H-C1 rider | optional Gate-A rider to Q2 (not default): day-7 decision at B₅₀ ≥ 3,000, veto fraction on the pilot records, 1,000 γ overlays +7.0 CPU-h (4,616 / 6,001); script [7] rider line | §12.1 Q2 |
| C items | Cr-C1, Cr-C3, Cr-C4 (0.04–0.07), Cr-C5 (Q4 pointer to §11.6), Cr-C6, Ph-C1, Ph-C2, H-C2 (×5–50 day-7 clause), H-C3, H-C4, H-C5, H-C7 (Q4 label gloss): folded into T1–T3; Ph-C4 wording (scenario text); Ph-C5 ([L13]); H-C6 (790 → 814 GeV); H-C9 (script label "approved figure"); H-C10 (§11.7 rule 1, C1 C′₀ condition); Cr-C2 (author lists, header and §12.2) | header; §4.4; §7 [L13]; §11.7; §12.1 Q2, Q4; §12.2 |

### 13.6 Changes since version 6 (`STRATEGY_ingrid_2026-11-14_02-20.md`)

Findings of the sixth arbiter (`STRATEGY_ARBITER_v6_johanna_2026-11-14_03-15.md`). Details, the diff attribution and the
grep phrases: `FIX_REPORT_cycle6_jules.md`. Script values bind where they differ from the verdict's draft numbers
(B₅₀ 159–256, not 158–254). No default, criterion, CPU-h, calendar figure or expected-outcome number changed.

| finding | what changed | sections |
|---|---|---|
| U1 basis of the day-15 projection | rule 1 states the basis (N_t·H on all own hits, no S_CKF, no conditional credit; DIF and conversions ×1/(1 − ε_pair) = ×5–50 above the after-CKF rows) and that only the test of a Q2 (c) redesign uses the redesigned conditional and S_CKF estimated on development samples (EST, no credit in the result); the day-7 **and** day-15 projections ×5–50 above the after-CKF figures; "(α1) with fit-probability credit" admitted only under (c); the veto-alone statement at v1's central decays-in-flight size (1–2 counts); the background size labelled after CKF, a lower value (annex route 6); the (c) bar on the rule's basis (B₅₀ 401–663 without conversions, 159–256 at DIF ×e⁻¹, ×1/(1 − ε_pair) if S_CKF cannot be estimated), whether (c) may target the decays in flight, the veto's signal cost; pilot m_H labels (after CKF); script [9b] two v7 lines | header; §0 "Expected", "The pause.", leading sentence; §4.4 point 4, point 5, "What is not known"; §11.7 rule 1; §12.1 Q2 stem, (c) |
| O1 (orchestrator-ordered, beyond the verdict) | C′_PU use stated as C1 and the rule-1 development estimate of a Q2 (c) redesign (agreement with §11.7 rule 1); no sample, size or CPU-h changed | §4.4 point 4 |
| O2 (orchestrator-ordered, beyond the verdict) | after-CKF basis label on the background size | §0 leading sentence; §12.5 point 3 |
| C items | Ph C-4 (§4.11 point 3 reading "if the day-15 pause does not fire"); Cr C1 (§11.3 heading, §11.7 row 3 "without the day-15 pause"); Cr C2 (49 / 65 days "both without the day-15 pause"); Cr C3 ("four to five weeks"); Cr C4 (rider part (3) "in addition to the 1,000 DIF overlays of P4"); Jp-C2 ("the route this strategy designs for one"); Jp-C5 ("statistics-only"); Jp-C6, Jp-C7 (inside the U1 text of (c)); Jp-C8 ("led by conversions") | §0 Calendar; §4.11; §11.3; §11.6; §11.7; §12.1 Q2 |

### 13.7 Changes since version 7 (`STRATEGY_jules_2026-11-14_03-40.md`)

Findings of the seventh arbiter (`STRATEGY_ARBITER_v7_lena_2026-11-14_04-30.md`). Details, the diff attribution, the
sweep and the grep phrases: `FIX_REPORT_cycle7_leopold.md`. Every value printed by script [9b] v8 lines equals the
verdict's draft numbers. No default, criterion, CPU-h, calendar figure or expected-outcome number changed; the day-15
reading per branch and the (c) bar are now quoted from script [9b] v8 lines.

| finding | what changed | sections |
|---|---|---|
| V1 (V1-a (β) listed as avoiding the pause; V1-b "at ×e⁻¹ the conversions alone would suffice"; V1-c the (c) bar "×31–52 and the decays in flight reduced"; V1-d the fit-probability credit acts on the decays in flight) | script [9b] prints the day-15 table (branch → B₅₀ under rule 1 → above/below 300) and the (c) rejection grid (item S); the text cites them: one statement of what rule 1 reads (S5), (β) read as (γ) at day 15 (S4, S9, S15, S16), the (c) bar as the printed grid (S17), the after-CKF and pool/pilot labels (S2, S3, S7, S8, S10, S11, S14), the S_CKF input used only in a (c) test (S12), the zero-survivor rule of the (c) test (S13), the rider expected to trigger (S18), the Df-9 basis (S19); the earlier statements of these points in versions 6–7 ("avoided … as in (α1) with credit, (β) and the empty-ceiling case", "×31–52 and the decays in flight reduced", "at its size ×e⁻¹ the conversions alone would suffice") are history | §0; §4.4 points 4, 5, scenarios, Table 4.4c caption, what is not known; §11.7 inputs and rule 1; §12.1 Q2 stem, (c), rider; Df-9 row; §12.5 point 3 |
| O3–O5 (orchestrator-ordered, beyond the verdict; from the fixer's own proposals) | O3: after-CKF basis label on the (α1) "projected B₅₀ 590–980" with a pointer to the v8 table (no number changed); O4: "v7 line" → "U1 line" for the ×5–50 / (α1′) own-hit line; O5: measured runtime in the code reference | §0 item 3; §11.7 rule 1; §12.1 Q2 stem; code reference |
| C items (14) | Ph C-1, C-2, C-5, Cr C2, C3, Co C1, C2, C4 (inside S2–S19); Cr C1 / Ph C-6 (duplicated parenthesis in §4.11 point 3 removed); Ph C-4 (rider's γ overlays named as the preferred (c) development sample); Cr C4 (§4.17 row 4 role column); Cr C7 ([L13] after-CKF label); Cr C6 (COM: doubled "and"; pointer to version 8; version-8 row) | §4.4 point 4; §4.11; §4.17; §7 [L13]; COM |

### 13.8 Changes since version 8 (`STRATEGY_leopold_2026-11-14_05-00.md`)

Finding of the eighth arbiter (`STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`). Details, the diff attribution, the
sha256 of the script output, the self-test lines and the output of the text check: `FIX_REPORT_cycle8_mireille.md`.
Rule 1 of §11.7 is made single-valued: every SM hard-scatter process and the multijets are read through the Z(νν) pilot count, and no pool floor enters; the day-15 limit in pilot counts is therefore ≈ 12 Z(νν) counts, not ≈ 20. No default, CPU-h, calendar figure or expected-outcome number changed; the day-15 table and the (c) grid are recomputed on that basis and quoted from script [9b] v9 lines.

| finding | what changed | sections |
|---|---|---|
| W1 (the day-15 table, the (c) credit rows and the (c) grid were not on the basis their captions stated; root cause: rule 1 did not say how a term without a day-15 sample is read, nor whether (c) factors multiply a zero-count floor) | rule 1 clarified (T10: samples that exist at day 15, every SM process and the multijets through the Z(νν) pilot count, no pool floor; T12: factors multiply a counted term, never its floor); script [9b] block A (day-15 table and (c) grid on the pilot's transfer factors, 20,000 draws, smallest integer factor that passes) and block B (8-check self-test), label line of the v5 (R1) line; text check `src/check_day15_text.py`; the text cites the v9 table (T1–T9, T11, T13–T17) | §0 item 3, "Expected", "The pause.", leading sentence; §4.4 point 4, point 5, Table 4.4c caption, scenarios (β) and (γ), what is not known; §11.7 rule 1; §12.1 Q2 stem, upside, (c), rider |
| O6 (orchestrator-ordered, beyond the verdict) | Df-11 added to the defaults of §12.1: the reading of rule 1 pinned in cycle 8 (wording from the §11.7 rule-1 clarification), its consequence by reference to the v9 table, why it was needed, that it can be overridden; the count of defaults ten → eleven | header; §0; §12.1 defaults; COM GA |
| C items | T18 (critical C-7: §12.5 point 2 "after CKF, as v1 counted them"); critical C-5 (script docstring: current version, runtime); physics C-1 / critical C-6, physics C-2, C-3, C-4 and constructive C-2 applied inside block A, T3, T10, T14 and T16 | §12.5 point 2; script docstring |

### 13.9 Changes since version 9 (`STRATEGY_mireille_2026-11-14_06-55.md`)

Finding of the ninth arbiter (`STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`). Details, the diff attribution, the
sha256 values and the output of the text check: `FIX_REPORT_cycle9_oscar.md`. Every edit is the verdict's §5 text.
The freeze table of §8 now counts eleven defaults. Df-11, §0 and the caption of the day-15 table state that the pinned reading is a proxy that errs lenient, that its alternative is more lenient still, and that the limit in pilot counts holds at an R09 candidate. Rule 1 states the precision of the binding median and that a reading within it pauses. No number of the script, default, CPU-h or calendar figure changed.

| finding | what changed | sections |
|---|---|---|
| B-1 (the freeze table of §8 said "the ten defaults"; there are eleven) | E1: "the eleven defaults (Df-1–Df-11, §12.1)" | §8 |
| C items (physics C-1, C-2, C-3; critical C-1 to C-6, C-8; constructive C-1 to C-4; arbiter item 17) | E2: the reading is pinned, overridable (Df-11) and a lenient proxy; E3, E5: the limits in pilot counts hold at the R09 pile-up estimate; E4: "no sample of another SM process"; E6: the binding B₅₀ is the median of at least 10⁵ draws, a reading within that precision of 300 pauses; E7: the limits at an R08 candidate and the direction and size of the proxy; E8: Df-11 consequence, proxy and its more lenient alternative; E9: B4-e floor labelled as a result floor; E10: basis of the leading sentence; E11: two estimates not reconciled; E12: rider expected to trigger in (α1′); E13a, E13b: §12.2 log entries, Df-11 among the judgment calls; E14: COM ST-1 marked Df-11 | §0 "The pause.", leading sentence; §4.4 point 5; §11.7 rule 1; §12.1 Q2 caption, rider, Df-11, annex B4-e; §12.2; COM ST-1 |

---

## Code reference
- `python3 -I analyses/quirks_v2/phase1_strategy/src/strategy_budget.py` prints every CPU-h, storage, calendar, floor,
  projection and test-power number of this document (standard library; about 75 seconds, measured on einstein for version 9: 1 min 15 s wall, 36 MB). Its sections [1]–[13] are
  cited in the text as "script [n]".
- `python3 -I analyses/quirks_v2/phase1_strategy/src/check_day15_text.py <STRATEGY> analyses/quirks_v2/phase1_strategy/outputs/budget_stdout_v9.txt`
  checks every statement of the day-15 table and the (c) grid in this document against the printed lines of script [9b] (standard library; output in `outputs/day15_text_check_v10.txt`).
- No pixi task was run and no sample was produced for this document.
