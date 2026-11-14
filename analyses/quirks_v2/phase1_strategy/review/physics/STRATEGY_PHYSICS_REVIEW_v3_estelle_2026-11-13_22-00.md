# Physics review, cycle 3: STRATEGY v3 (`STRATEGY_emeric_2026-11-13_21-10.md`), Phase 1, quirks v2

Reviewer: Estelle (physics reviewer, fresh to the panel), 2026-11-13 22:00.
Read: `outputs/FRAMING.md`; the artifact in full (l.1-2674); the cycle-2 physics review (Dolores); the fixer's report
(claims treated as pointers only). Opened to check claims: `src/strategy_budget.py` (sections [9a], [9], [9b], read and
rerun, exit 0); D4 digest l.185-200 (v1 ladder per term); v1 `TT/acts/stage4/analysis/normalise.py` l.84-110 and
`gen_d123.py` l.150-180; PLAN l.105-125. I did not read the methodology or conventions files.
Own arithmetic: `python3 -I`, standard library (scripts in the session log). "l." = line of v3.
Classes: **A** must resolve before execution, **B** must fix before PASS, **C** suggestion.

---

## Part 1. Verification

Summary: **10 RESOLVED, 3 PARTIALLY RESOLVED, 0 NOT RESOLVED** (one resolution relies on a Gate-A default, Df-7, which
is acceptable).

| # | finding | status | v3 location and my check |
|---|---|---|---|
| c1-A2 | extrapolation width not guaranteed | **PARTIALLY** | §4.0 pt 7 (l.391-447). The rule is now applied as written. I recompute with s_model at the cap and b̂ = 0: occupancy model 0.43 / 0.59 / 1.29 / 2.47 at R08 / R09 / R11 / R14; π_k 0.73 (R08-R11) and 2.20 (R14); NI rung split 2.09; conditional 0.82 / 2.03 / 2.84 at 2 / 5 / 7 rungs. All match the table (l.430-435). Censoring added (l.444-447). **What remains:** the new "crossing test rungs" (l.406-417) can remove whole families from d_out. For the occupancy model in the fit-probability and shape families the crossing test cannot fail for a physics reason, but it removes the width all the same (new **B5**). |
| c1-A5 | NOT TESTED verdict; vacuous pass moved to H | **RESOLVED** | Four verdicts (l.365-372). No credit by default (l.383-389). "Leading" uses no-credit values (l.1393-1394). H is now tested (l.676-685). The remaining defects of the H tests are listed under c2-A1. |
| c1-B2 | background list incomplete | **RESOLVED** | Rows in Table 2.1 (l.153-155). The pile-up-secondaries premise is corrected (l.190-208, see c2-B1). Noise and out-of-time hits are compared with R-18 by a rule (l.209-211). δ-rays are a limitation [L8]. |
| c1-B4 | signal MET, trigger, calorimeter/muon, timing | **RESOLVED** (retrieval-dependent, acceptable) | l.1655-1680: same MET model with correlated nuisances; m_mig rule at 5 %; the lepton-veto physics argument is written (l.1672-1675) and given to R-13; the hit-time window comes from R-14 or is [L12]. Each branch has a dated rule. |
| c1-B8 | "no public number → no nuisance" is optimistic | **RESOLVED**; default Df-7 left to the human, acceptable | l.1219-1222, Df-7 (l.2516): the μ₉₅ shift of the robustness variation is reported beside the headline and named among the abstract-level limitations above 10 %. This is the "with and without" form Dolores asked for. The flagged-nuisance alternative is offered to the user. |
| c2-A1 | ceiling H never shown to be a ceiling | **PARTIALLY** | (iii) Hit-level definition of f_k: l.656-663, done. (i) One-sided ceiling test: l.676-685. I reproduce p_c = 0.0011 (8 counts in 4,000 events against 500 in 10⁶) and 0.547 (against 2,000 in 10⁶). The size at the boundary is 0.001 + 0.049 × 0.05 = 0.35 %. (iv) FAIL logic by direction: l.376-382, done. (ii) Completeness test: l.686-698. **What remains:** (a) the subset argument (l.668-671) holds only for cuts that are monotone under added hits; f_CKF and the CKF hit removal are not, and how H treats them is not defined (new **B2**); (b) on the enriched DIF test overlays the ceiling and leak tests pass by construction (new **B3**); (c) the "mixed" count is a raw upper value with no pile-up-only baseline, which makes a FAIL of the completeness test likely for the hard-scatter terms (new **B4**); (d) the ceiling tests carry no family-wise control (new **B6**). |
| c2-B1 | pile-up-vertex secondaries | **RESOLVED** | The premise is corrected with the v1 sources. I opened `normalise.py` l.84-110: DIF and NI are "HS + 200 × min-bias"; γ, V⁰, PV pairs and loopers are "HS vertex only". Both shares are kept in rate_t, and the pile-up share is placed at its own z (l.196-198). Single counting: Geant4 secondaries of pile-up particles appear only in B1, never in overlays (l.199-200). A truth-attributed count at R04-R07 is compared with the B1 prediction, with a fixed rule (l.201-208). The expected counts 2,100 / 1,000 / 25 / 13 = 4,000 × 1.57 × (166, 81, 2, 1)/500 are right. Only R04-R06 can reach N ≥ 24; see C7. |
| c2-B2 | PV pairs / SM double count | **RESOLVED** | One route per particle origin (l.158-178). Disjointness follows from single truth parents plus Fatras decays switched off (B1-d). A route check on Z(νν) has a fallback rule. Floor recomputed (Part 2, check 1). Residuals are C1 and C2. |
| c2-B3 | quoted widths contradict the rule | **RESOLVED** | Recomputed above: all v3 numbers follow the stated rule. b₀ is called a convention (l.418-421, [L6]). |
| c2-B4 | log-normal widths not capped | **RESOLVED** | φ = min(φ₀e^θ, 1) is a parameter bound in the fit and a censored draw in the toys (l.444-447, l.1319-1324). With it P ≤ H in every pseudo-experiment, and the pile-up estimate is capped at 485. A tested factor can no longer cost more than an untested one. |
| c2-B5 | "estimate" too weak; rule drawn to the edge | **RESOLVED** | "Estimate" now needs m ≥ 4 (w_m ≤ 0.5) and PASS (l.1391). The estimate-only selection is reported beside the winner, and the abstract choice goes to Q2 (l.1565-1572). The winner is also reported under a monotone prior. Residual wording point: C4. |
| c2-B6 | π_k assumes independent layers | **RESOLVED** | π_k comes from the occupancy model with measured layer correlations (l.700-707). A per-k comparison sets the promotion s_model, against the cap. |
| c2-B7 | projection lacks the pile-up term and H | **PARTIALLY** | Table 4.4c (l.778-791) adds the EST pile-up term and Z(νν) at its ceiling. I reproduce every row by rerunning script [9b]. Labels EST and "v1 placeholder efficiencies" are present in §0, Table 4.4c and Q2. **What remains:** the projection sets the DIF term and the hard-scatter conversions (now inside B4) at their zero-count floors at R09, against v1's own non-zero counts at R06-R07 (new **B1**, the most serious open point). |

Cycle-2 C items, briefly: C1 (one σ_ln) resolved, l.1384-1385. C2 (bias, not coverage) resolved, reading (e), l.1430-1433.
C3 (distance in ln of the rejection) not adopted; the Df-2 alternative is ln F·√d instead, still worth offering (C8). C4
(infracolour constant, scalar P wave, scale): named for R-12, l.1737-1741. C5 (re-allocation with gains) resolved, l.721-722.
C6 (categories without credit) stated, l.1050-1052. C7 (freeze the 16 candidates) resolved, l.1528. C8 (proportionality)
partly: overlays cut to 17,500, a day-15 rule added. C9 (veto argument) resolved, l.1672-1675.

---

## Part 2. Fresh judgment of v3

### Checks that pass (my own recomputation)
1. **Summed zero-count floor, 45.3 → 11.7.** Rerunning script [9] and checking it by hand:
   - DIF: N_t = 4.0848×10⁷ × 1.5945 = 6.51×10⁷; M = 2.53×10⁷; transfer factor 2.57; floor 2.93.
   - NI: 0.25 per radius, floor 0.28 each.
   - SM: Z(νν) 2.51×10⁷ / 1.14×10⁷ = 2.20 (floor 2.51); W(τ_h) 1.02 (1.16); four processes at 0.66-0.70; six at 0.14-0.22. SM sum 7.9.
   - Total 11.7. The predictive sum of exponentials gives median 9.6, 16-84 % 6.7-13.8.

   Where the drop comes from:
   - 18.4 (PV pairs) and 4.7 (γ, V⁰, loopers) are removed.
   - The SM floor falls from 16.4 to 7.9, because the 244 CPU-h of PV-pair guns go to real events.
   - DIF + NI fall from 5.8 to 3.8, because the Geant4 line is folded into the pool.

   The physics of the merge is right. One real hard-scatter event exposes all ~30 prompt pairs in the road at once, so a zero count in M real events bounds the per-event probability with no pair-multiplicity factor. The γ, V⁰, PV-pair and looper rates are "HS vertex only" in v1 (`normalise.py` l.105-108), so the same particles sit in B4's real events. I find nothing double counted between B1, B2 and B4, given B1-d (Fatras decays off) and C2 below.
   - Missing from the 11.7 (stated at l.766, but absent from the §0 headline): the three additions, Z(ττ), lost-lepton Z and multijets. The multijet floor is N_MJ × 1.14/10⁶ through the factorisation, so it could be comparable to Z(νν).
2. **False-fail rates.** I integrate the stated rule exactly: tolerance (a), χ² (b) with V = σ² + s_model², INVESTIGATE, and a re-test with the same δ at p′ ≥ 0.05/K. One rung at the evaluable limit gives a final FAIL of 0.52 / 0.55 / 1.07 % at s_model = 0 / cap/2 / cap. For the battery of 10 at the cap: at least one FAIL 10.2 %; a FAIL that removes a selection 4.2 % (8 tests at half the rate for under-prediction, plus B2-a and B2-b both failing). All match l.349-352. The 0.27 % behind the cap (P(|δ| > L) at s_model = L/3) is right. The cap and the re-test at 0.05/K are physically sound: δ is the same in a re-test, so a re-test at p′ > 0.05 would nearly double the false fail of a correct estimator at the cap. But the quoted rates leave out the ceiling tests (B6).
3. **Widths.** See Part 1, c1-A2. Two entries checked in detail:
   - R11 occupancy: √(0.135² + 0.405²·1² + 0.405²·3²) = 1.29.
   - NI π_k at R08: √(0.231² + 0.693²·3²) = 2.09.
4. **Reach versus ceiling count.** The script maps the one-bin median s₉₅ onto the plan's σ_ln = 0 row (PLAN l.121) at equal fixed-B limit. It reproduces 834 / 793 / 761 / 723 / 661 / 575 GeV, ≈ 495 at m_H = 1000, and the constructive review's 24.1 for the v2 floors. It is derived consistently and labelled EST with v1 placeholder efficiencies (l.55-57, l.778, Q2 l.2460). C6 is a caveat on the mapping.
5. **Nuclear interactions tested only at R05 (rung split).** It is a real held-out test. Survival and promotion are derived at R04, and the test is on other events at R05, with 92 / 120 / 378 expected attributed counts. The price is stated honestly: width 2.09 at R08, so NI stays near its ceiling. Acceptable.
6. **Dropped γ/V⁰ enriched overlays.** Defensible once γ and V⁰ are no longer terms. Their physics is closed through B4-c on the real hit-level test halves (Z(νν) N_eff = 32.3 × 5,000/2,000 = 81; W(τ_h), W(τ_ℓ), tt̄ 1ℓ 31 each, which I verified from the v1 per-event rates). The 1,000 unbiased events per sub-topology keep the ceiling and completeness tests. See C3 for the composition caveat.
7. **Redesigned pile-up-secondaries test.** It is now meaningful: it counts by truth the candidates attributed to secondaries and compares them with the single-vertex B1 prediction. This replaces a ratio that was swamped by 49.7 pile-up planes per trial. With own-z placement the B1 term is physically correct where v1 was not (v1 put 99 % of the DIF vertices at the PV).
8. **Labels and readings.** "Target not met: sample-size limited" is the honest expected label, and the paper's message for each outcome (l.1396-1402, l.1596-1609) is defensible. A paper whose headline is a *bounded* background with closure-tested estimators, a stated width and a reach above ≲ 180 GeV can pass a referee. But the size of that bound is what B1 questions.

### B1. The projection, and so Q2, ignores v1's non-zero deep counts for decays in flight and hard-scatter conversions (§0 l.39-61; Table 4.4c l.778-791; Q2 l.2476; [L13])
- **Evidence.** v1 measured with pile-up (D4 l.185-200; Table 2.1 l.145-147):
  - DIF attributed counts of 2 and 1 at R06 and R07, which is 3.0×10⁵ and 1.5×10⁵ events in 3 ab⁻¹.
  - Hard-scatter γ conversions of 13 and 2, which is 4.0×10⁵ and 7.4×10⁴ events.

  These are not bounds. In v3 both populations are terms: DIF in B1, the conversions inside B4. Every row of Table 4.4c still puts DIF at its zero-count floor (2.9 events) and B4 at 7.9 events, or adds only a Z(νν) ceiling of 3-100 counts. Getting from v1's R07 values to the R09 floors needs a fall of 4.5-5 decades across one width step plus the fit-probability cut.
- **The document's own extrapolation contradicts that fall.** The pile-up EST term uses the measured fall per width step of the *combinatorial* background (×201, ×339) and v1's fit-probability fraction 2/35, and gets 3.6 decades from R07 to R09. Correlated physical topologies fall more slowly than random hit combinations, and v1 shows exactly that: DIF falls ×2 and γ ×6.5 from R06 to R07, where pile-up falls ×339. The chance of seeing ≥ 1 DIF count at R07 if DIF fell like pile-up is 0.6 %.
- **What the same rule gives for these terms.** Applied to DIF and γ, the document's rule gives at R08: DIF 440-750 (pile-up-like fall) to 3,750 (DIF's own R05→R06 fall); γ 220-370 to 1,850.
  - At R09 this becomes 25-215 (DIF) and 12-105 (γ), but only if a fit-probability conditional earns credit (B3).
  - An untested conditional is 1, so these terms are then as large at R09 as at R08 (l.673-675).
- **Caveats.** v1 placed every DIF vertex at the PV, and its coded attribution rule is not yet transcribed (l.654-655). Either could make v1's DIF counts too high. Neither applies to the hard-scatter conversions.
- **Why it matters.** The user decides Q2 ("production proceeds without a pause", "≈ 790 GeV if every ceiling is empty") and the outcome class on these numbers. By v1's own record, the expected B₅₀ at R08-R09 is O(10²-10³) events. That is a reach of roughly 500-650 GeV by the same mapping, and the day-15 pause (B₅₀ > 300, l.2431-2435) is a likely branch rather than an exception. The decision rule itself is sound. The expectation offered at Gate A is not.
- **Fixed looks like.**
  1. Add to Table 4.4c, §0 and Q2 an EST row in which DIF and the γ part of B4 are extrapolated from their v1 R06-R07 counts. Do it twice: with the pile-up width-step fall (optimistic) and with their own observed fall. Show it with and without fit-probability credit, beside the Z(νν) ceiling rows.
  2. State the two caveats (PV placement, attribution rule), the expected class at day 15, and that "every ceiling empty" is the optimistic edge, not a central value.
  3. Put a planning range for the multijet floor in the headline sum.

### B2. Whether H is a ceiling depends on how it treats CKF; the subset argument ignores the non-monotone fixed cuts (§4.4 pt 4, l.656-675; §1 l.99, l.115)
- **Evidence.** The completeness claim (l.668-671) holds for cuts that can only become easier when hits are added: layer counting and the width of a hit subset. The candidate also has to pass f_CKF < 0.2 (share of its hits on CKF tracks), and CKF removes helical tracks before the finder (l.99). Neither is monotone under pile-up. Pile-up lowers the CKF efficiency for the term's own tracks, and unassociated pile-up hits dilute f_CKF. So a no-pile-up event whose prompt pair is fully reconstructed by CKF (failing, so in no H class) can pass with pile-up.
- **The definition is missing, and either choice breaks something.** The text does not say whether the no-pile-up classification "on subsets of the term's own hits" (l.656) uses all own hits or only those CKF leaves.
  - If CKF is applied, H is not a ceiling for the prompt topologies, which now dominate B4.
  - If CKF is ignored, H counts every pair of prompt stiff tracks that passes counting and width. That is plausibly orders of magnitude above the 3-100 counts of the Q2 bracket: there are ~30 prompt pairs in the road per event, v1 PV pairs.
- **What the shallow test can and cannot do.** The ceiling test at R02-R04 (prompt pairs) and R04-R06 (B4) is sharpest where pile-up is densest (π_k → 1, P ≈ H), so it would detect a large CKF effect. It cannot fix the definition, which must exist before the pilot measures m_H.
- **Fixed looks like.** Define H's treatment of CKF and f_CKF explicitly. Two defensible options:
  - (a) H uses all own hits, with f_CKF and CKF removal entering as a B3-type conditional that earns credit only when tested, so H is a true ceiling.
  - (b) H applies CKF at its pile-up-200 efficiency, measured and with a width.

  Then correct the "by construction" sentence, list every fixed cut with its monotonicity, and project m_H for Z(νν) under the chosen definition.

### B3. On the enriched DIF test overlays the ceiling and leak tests pass by construction (§4.4 l.676-698, l.817-824)
- **Evidence.** The DIF ceiling test runs at R04-R07 "on their test overlays", and the completeness leak is measured on "every overlay". 4,000 of the 5,000 DIF test overlays are drawn only from passing and near-pass no-pile-up events. An attributed candidate from an event outside every class k ≤ k_max, which is exactly the leak and the ceiling violation, cannot occur in that sample. Its weight is zero, so the weighted attributed rate is ≤ H by construction.
- Separately, by the attribution rule itself (j ≥ n/2 ⇒ k ≤ ⌊n/2⌋) the leak is zero for any correct implementation. It is a code check, not a physics test.
- **Fixed looks like.** Restrict the ceiling and leak tests to unbiased samples: the 1,000 unbiased DIF events, the NI overlays, and the hit-level halves. Use the enriched overlays only for the S/π_k closure. Label the leak fraction as an implementation check.

### B4. The completeness test counts "mixed" as a raw upper value; for the hard-scatter terms a FAIL is likely, and the consequence is undefined for untested terms (§4.4 l.686-698; Q3)
- **Evidence.** A candidate is "mixed" if it has 1 ≤ j < n/2 term layers. In events with pile-up, any pile-up plane that picks up one term layer counts. Pile-up candidates are 49.7 per trial at R05 and 0.247 at R06. Hard-scatter-attributed candidates are 4.51 and 0.0162 per Z(νν) event (C1 table, l.480, l.487). At R06, if 7 % of pile-up candidates in an SM event pick up one hard-scatter layer, mixed/attributed already exceeds 1. The bound is 0.26 on the 95 % upper limit, and the text itself calls this count an upper value (l.696-698).
- **Consequence of a FAIL.** If the test fails on development samples, the term "has no ceiling and is extrapolated like the pile-up term" (l.693-694). The eight proxied processes are expected NOT TESTED, and their Q3 default is "enter at H". Then nothing is left for them, and the text does not say whether they become ineligible.
- **Fixed looks like.**
  1. Measure the excess: the same events with the term's hits removed (paired pile-up-only finder pass, the 26 CPU-h the fixer declined, l.31 of the fix report), or the pure-pile-up rate of matched pile-up-only events subtracted.
  2. State the expected mixed fraction from the C1 development samples before Gate A, or at least as a dated day-15 rule.
  3. Fix what an untested term enters as when its completeness test fails.

  The 0.26 bound is acceptable as a declared convention, because c_mix is always applied. It needs a well-posed numerator.

### B5. Crossing tests of the occupancy model in the fit-probability and shape families are consistency checks, yet they remove those families from the width (§4.0 pt 7 l.406-417; §4.5 l.916-920; table l.431)
- **Evidence.** For R09-R11 and R15-R20 the occupancy model takes its pass probability from "the finder candidates passing R06 in the development sample" (l.917-919). The crossing test R09⊗R06 compares that prediction with the direct count at R06 + fit-probability cut in the test sample. So ln r = ln[occ(R06)/direct(R06)] + ln[frac_dev(R06)/frac_test(R06)]:
  - The first term is the cumulative R06 test already performed.
  - The second compares one quantity on two samples of the same construction at the same rung. By the document's own definition (l.310-312) that is a consistency check that "gives no verdict".
- **Yet a PASS removes the family from d_out.** The occupancy width at R11-R20 then falls from 1.29-4.88 to 0.45-0.49. The assumption that actually matters, that the fit-probability or shape pass fraction measured at an 18.75 mm width transfers to 4.7 mm, is never tested. That is a width earned by construction. Its weight in the result is moderate: the pile-up term is 5-9 events at R09 and < 1 from R11 on (Table 4.4c). It matters for every deep candidate.
- **Fixed looks like.** Either (a) declare these crossing comparisons consistency checks with no distance credit, or (b) derive the fraction at a looser width (R05) and test it at R09⊗R06 and R09⊗R07, so that the width dependence is tested. In both cases the width step from the last crossing rung to R08 still counts in d. Thinning and π_k crossing tests are genuine (thinning recomputes the variables; π_k is tested on overlays) and are unaffected.

### B6. The ceiling tests can remove selections but have no family-wise control, and the rates quoted to the user leave them out (§4.4 l.676-685; §4.0 l.339-352; Df-2 l.2511; §4.12 l.1542-1543)
- **Evidence.** A ceiling FAIL makes every selection where the term leads ineligible. The tests run per rung: DIF R04-R07, NI 3 × R04-R05, twelve SM processes at R04-R06 (small ones R04-R05), and γ, V⁰ and prompt pairs. That is about 40-55 one-sided tests.
  - At the shallow rungs, where pile-up is dense, the truth sits near the ceiling, so many of them operate near their 0.35 % boundary size.
  - With 15 / 30 / 55 near-boundary tests, at least one false ceiling FAIL occurs with probability 5 / 10 / 17 %.
  - K = 10 excludes them. Df-2 and §4.12 rule 1 tell the user that a correct analysis loses a selection with probability 2-4 %.

  It is not said which term a sub-topology ceiling FAIL (γ, V⁰, prompt pairs, not terms) is charged to.
- **Fixed looks like.** One combined ceiling test per term (for example a one-sided χ² or a min-p with Bonferroni over its rungs), included in the eligibility family. Assign each sub-topology test to its B4 terms. Restate the false-removal rate in Df-2, §4.12 and the pre-registration.

### C items
- **C1. NI rates inconsistent.** The text says 0.098 (22 mm) and 0.124 (30, 61.5 mm) × 0.22 (l.733). The script uses 0.11 × 0.22 for all three (`RATE`, script l.66-67), and Table 4.4a shows 9.89×10⁵ each. Use one set. The ×0.22 is v1's "PV-line factor" (`normalise.py` l.106-108): name it and give its source.
- **C2. Geant4 conversions in B1.** Geant4 "records every inelastic interaction, decay or conversion" (l.640-641), and γ is a primary. By the route table, conversions belong to B4/B2 (Fatras). State that Geant4 conversion products are not injected into B1, and that γ enters only for photonuclear NI, or this route double counts.
- **C3. Composition drift inside B4.** One estimator per process is closed on a mixture (prompt pairs, conversions, V⁰) at R06. In v1 the conversions fell far slower than the rest (×6.5 against ≥ ×60 for the Z(νν) total from R06 to R07). Report B4-c and the per-k promotion comparison split by truth sub-topology, as consistency checks on the same samples (no CPU).
- **C4. Wording.** "Target met" (l.1397-1398) admits leading "low count" terms (m = 1-3), while the paper's verb "estimated" is reserved for m ≥ 4. Either require "estimate" for the leading terms in "target met", or make the paper say "measured with low counts". The "estimate" label also ignores the extrapolation width (a term at s_tot = 2.09 is an "estimate"). Print s_tot next to every label.
- **C5. s_model of the occupancy model is in-sample.** Its inputs and its r.m.s. both come from the development R04-R05 (l.913-915, l.322-324). Take the r.m.s. at a development rung not used for the inputs (for example development R06), or the larger of the two.
- **C6. Reach mapping.** PLAN's σ_ln = 0 row is the book's reach at its own efficiency (best Λ per mass). Applying it to an "R09-like" background assumes the R09 efficiency equals that efficiency. Say so in the Table 4.4c caption. The bias can go either way.
- **C7. Secondaries test.** Count the multi-vertex class (candidates with ≥ 2 distinct secondary vertices) directly per rung, with its trend, rather than through a factor-2 excess on the total. Only R04-R06 reach N ≥ 24, and a factor 2 at R04 can hide a class that grows with depth.
- **C8. Distance unit.** Offer the cycle-2 alternative (distance in ln of the extrapolated rejection, anchored with v1's drift per e-fold) in Df-2 beside ln F·√d.
- **C9. Pile-up cap.** The pile-up estimate is censored at 485 events, a 68 % upper value of a zero count, used as a hard bound. Harmless in practice (the R08 median is 118). Use the predictive draw of the no-credit bound instead, for consistency with the other no-credit terms.

---

## Overall judgment

**Not yet approved.** Verification: 10 resolved, 3 partially, 0 not resolved. New: A = 0, B = 6, C = 9.

v3 is a substantial and mostly correct revision:
- The one-route accounting is physically right, and I reproduce the 11.7-event floor term by term.
- The widths now follow their rule.
- Censoring removes the "testing costs more than not testing" pathology.
- The closure size and power numbers are right for the tests they cover.
- The expected label "sample-size limited", with the bounded paper as the default, is honest.

No finding makes the execution wrong at the root, so nothing is A. Two groups block a PASS:
- **(i) The expectation shown to the user is optimistic against v1's own record (B1).** DIF and hard-scatter conversions had non-zero counts at R06-R07. The document's own extrapolation rule gives them O(10²-10³) events at R08-R09, not the zero-count floors behind "≈ 12 events" and "≈ 790 GeV".
- **(ii) The ceiling H, now the load-bearing no-credit value, is not yet a verified ceiling.** Its CKF treatment is undefined and the monotonicity argument ignores f_CKF (B2). Its tests partly pass by construction (B3, and B5 for the occupancy crossing rungs). The completeness test is ill-posed (B4). Its false-fail rate is outside the quoted family-wise rates (B6).

Each fix is a definition, a restricted sample, an added table row or one 26 CPU-h pass. None needs new production.
