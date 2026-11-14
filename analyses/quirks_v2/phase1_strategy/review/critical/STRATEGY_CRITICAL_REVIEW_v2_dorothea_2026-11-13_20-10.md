# Critical review: Phase 1 STRATEGY v2 (quirks v2), review cycle 2

Reviewer: Dorothea, critical reviewer ("bad cop"), 2026-11-13 20:10. I am new to the panel and did not take part in cycle 1.
Role and template: `agents/critical_reviewer.md`, prompt template followed in full. Phase 1 has no figures, so the figure
checks do not apply.
Artifact: `phase1_strategy/outputs/STRATEGY_dmitri_2026-11-13_19-25.md` ("v2", 2,391 lines, read in full),
`QV2/COMMITMENTS.md` ("COM", read in full), `phase1_strategy/src/strategy_budget.py` ("script", rerun; sections [9]–[12]
read in full).
Also read: arbiter verdict `review/arbiter/STRATEGY_ARBITER_dagmar_2026-11-13_19-00.md` (M1–M35, §5 Gate-A list),
`FIX_REPORT_cycle1_dmitri.md`, `AGENT_RULES.md`, `CLAUDE.md` STUDY OVERRIDES, `phase1_strategy/CLAUDE.md`,
`conventions/search.md` (standard configuration, required sources, validation checks, pitfalls), `prompt.md` §3 and §7,
and LOG.md 14:34. I looked up the v1 record (`STAGE4_SUMMARY.json`, `C12FC_v1/{bsum_wp,limits,acceptance}.json`,
`STAGE3_INDEX.json`), FEAS_A/B/C and digest D4 l.185-203 for the spot checks.
Line numbers "l." refer to v2 unless another file is named. No sub-agents, no git commands, only standard-library `python3`.

**Summary.** v2 is a real redesign: the zero-count likelihood is specified and checked, the closures are held-out tests
on disjoint rungs and samples, there is a floor table, and the stop rule is quoted correctly. Every number I recomputed
matches. Of the 35 merged findings: **22 RESOLVED, 5 PARTIALLY RESOLVED, 0 NOT RESOLVED, 8 DEFERRED TO GATE A**. Each
deferral is a real user decision, presented with options and costs.
I report **new findings: 3 Category A, 9 Category B, 10 Category C.** The three A items are these:
- The closure battery's false-fail rates assume an estimator with no model error (N1).
- MUST criteria are planned to stay untested without putting the conflict with brief D4 to the user (N2).
- The pre-declared reading "target met" can be earned by a background made only of zero-count bounds (N3).
**Recommendation to the arbiter: ITERATE.**

---

## Part 1 — Re-review of the merged findings M1–M35

Verdict key: R = RESOLVED; P = PARTIALLY RESOLVED; N = NOT RESOLVED; D = DEFERRED TO GATE A. For each D, "genuine" means
a human decision presented with options and costs, with the fix itself done.

| # | finding (short) | verdict | evidence in v2 / COM / script (checked by me, not taken from the fix report) |
|---|---|---|---|
| M1 | zero counts in the likelihood | **R** | Generation hypothesis fixed: λ ~ Gamma(m+1) in every pseudo-experiment, auxiliary data fixed (l.1145-1174). The derivation is shown with a substitution (1.139 at 68 %) and the large-m limit (l.1149-1157). B₈₄, total σ_ln, estimate/bound/no-credit, "leading" and f₀ are defined from the predictive distribution (l.1179-1193). Limiting-case and coverage tests: T1-c (i)–(iv) (l.1240-1252). T2 limiting check: l.1340-1346. "One zero per term": l.1122-1125. **My recomputation:** one bin, κ = 35, median n = 24 gives s₉₅ = 27.8 (script [10] 27.8). Coverage at κ = 1, λ = 0.5, s = 10 is 0.9448 (script 0.945). Remaining specification gaps are new findings N5 and N13 (B, C). |
| M2 | C1 blinding exception | **D, genuine** | The count is corrected to six (l.437-441). I verified it in `SUM` → `fallback_points`: FB2/FB3 with `e_adm` = None, 9/10/11 of 200. Sealed-tier default (l.444-461). R07 and family F frozen in the T2 list (l.462-464, l.1301-1302). "Takes effect only if approved at Gate A" (l.442). GA-1 has five options with costs (l.2179-2193). CPU is the same in every option. Residual leaks: C item N14. |
| M3 | same-rung closure | **R** | Common rule (l.274-278). Every estimator has a declared derivation and a disjoint test: B1 derives at R04–R05 on derivation overlays and tests at R06–R07 on test overlays with other seeds (l.652-659). B2-b derives on development samples at R04–R05 and tests on the 96,000-trial sample at R06–R07 (l.754-756). B2-a has no fitted parameter, so every comparison is a test (l.747-748). B3 uses parity halves with first two rungs against the deepest (l.847-850). B4-c uses parity halves, R04–R05 against R06 (l.954-956). B3-c derives on the development sample and tests on the direct sample (l.871-874). B4-e derives in low MET bins and tests in the highest (l.948). Promotion of failers is inside the estimator (l.564-570). The B5-a test uses roads of the same events: N21 (C). |
| M4 | extrapolation width | **P** | Done: s_tot(r) is always in the likelihood (l.336-348). S = 1 beyond the tested rungs (l.576-577). Conditionals are measured after at least 3 rungs with a stability test (l.845-850). A distance table per candidate (l.1348-1352). The b₀ = ln F convention is flagged and has an alternative in GA-4 (l.2227-2228). Not done: (i) The substituted widths (l.357-360, l.794-795, GA-4) use fitted slope errors of 0.029 and 0.097, but every planned test design has fewer than 3 evaluable rungs per family. The strategy's own rule (l.344-345) then sets σ_b := b₀, which gives larger widths (N4). (ii) The distance is still a rung index across cut families, including rungs that do not act on the extrapolated quantity. The arbiter named this explicitly ("rung index across cut families"). (iii) §0 still presents conditionals as a lever without their widths (N4). |
| M5 | testability, NOT TESTED | **P** | Done: the evaluable-rung rule (l.284-288; I checked N ≥ 55/64/121 and 19/20/24). Four verdict classes (l.307-314). What each earns (l.324-334). "Leading" is decided with no-credit values (l.333-334, l.1313-1314). Expected-count tables for B1 (Table 4.4b) and B4-c (l.956-960). Not done: closure samples were not raised (the arbiter's item (b)), and the conflict with brief D4 is not put to the user as such (N2, A). No expected-evaluability statement exists for B3-a/B3-b/B3-d. |
| M6 | floors and central target | **D, genuine (redesign done)** | Floor table 4.4a (l.612-629). I recomputed it independently: summed 68 % floor 45.3, single interaction 28.9, SM 16.4. The Lagrange condition holds: N_t/(M_t² c_t) is equal for all terms, 1.84×10⁻⁵. The closed form 1.139·(Σ√(N_t c_t))²/C = 45.31 matches. Pilot: l.598-601. Projected outcome in §0 (l.39-51). GA-3 has three pool sizes and three messages. The new problem is the "target met" reading (N3, A). Z(νν) gets 5.5×10⁶ events, not the arbiter's ≥ 10⁷, but this follows from the optimal allocation and is stated (l.897-899). Accepted. |
| M7 | injection, pulls, units | **R** | Injection at 0, 1, 2 and 5 × μ₉₅^exp of each point, with 200 fluctuated pseudo-experiments per level, a 20 % criterion and an absolute criterion at zero (l.1253-1260). Pulls on fluctuated data; constraints only on Asimov (l.1261-1265). Units: μ₉₅ = 1.2458×10⁷/15,775 = 789.7 (l.1237-1238). I verified 1.2458×10⁷ in `limits.json` → `points["A2\|F\|200\|1.5\|BM"].expected_toys.median` = 12,458,208. |
| M8 | T1-g, toy budget | **R** | The self-consistency test was removed. T1-h computes coverage from stored distributions (l.1272-1276). Both toy passes are budgeted: 144.9 + 173.9 CPU-h (script [3]). Scaling is measured in Phase 2 (l.1229-1230). The nested-toy cost of 1,449 CPU-h is reproduced in script [7] and not incurred. T1-h leaves its true rates unstated (N5). |
| M9 | MET validation tuned to pass | **R** (execution depends on R-3) | Tuning removed; the soft term comes only from the public source (l.918-920). External validation against a different published figure, with the tolerance fixed before multijets exist (l.925-930). (a) is relabelled with no verdict, and (c) states √s and pile-up (l.934-938). There is no fallback if R-3 gives no parameters at all (N8). |
| M10 | stop rule weakened | **R** | Brief §7 is quoted verbatim. I compared l.2133-2140 with `prompt.md` l.341-348 word for word, and l.2142 with D6 at l.79: identical. "Approved schedule" is defined, with a threshold of 5,722 CPU-h and three checkpoints (l.2145-2155). §4.13 (l.1443-1445) and §12.5 item 8 are also corrected. A grep finds no other "schedule corrected". COM ST-1 is present. The threshold sits below the strategy's own contingency: N7. |
| M11 | round-number variation sizes | **P** | Done: robustness tests and nuisances are separated, with linear scaling and a linearity check (l.1019-1030). B1-c no longer uses the ×2 band (l.686-690). Not done: no size is sourced yet. The fallback "no public number → no nuisance" makes the limit optimistic and is not put to the user (N8). Honest PARTIAL with a Phase-2 commitment (R-15…R-17, prereg content (3)). |
| M12 | nuisance propagation | **R** | Table per nuisance and term (l.1035-1040). Reruns: 4 × (2×10⁶ × 11.5 ms + 5×10⁵ × 45 ms) = 50.6 CPU-h (script [3]), in both variants. Transfer to depth runs through the occupancy model with the width (l.1041-1042). |
| M13 | [DP2] reduced set | **D, genuine** | The reduced set keeps 5 keV and E 1000 (l.1058-1063). Interpolation rule (l.1066-1068). Paired design and the six-point alternative are costed: script [13] gives +25 +4 +6…23 CPU-h, against "+35 to +55" in GA-7. |
| M14 | thinning reach | **R** | K = 64 and N_eff = 1/s_boot² (l.742-748). Reach projection (l.787-796). I checked 1/0.0077² = 16,866 against D4 l.189. The NOT EVALUABLE branch leads to a one-estimator extrapolation (l.793-795). The finder-candidate input is named, and independence is claimed only for counting and width rungs (l.757-761). No ρ ≥ 3 (l.797). |
| M15 | closure statistics | **P** | Done: full covariance V_boot + s_model²J (l.292-295). s_model fixed before the freeze (l.296-298). Counts taken after the cut (l.281). Family-wise rule; I reproduced 7.5 % at K = 12, 0.55 retests and 0.95¹² = 0.54. Retroactive v1 test (l.302-304). Not done: the sizes stated per test and for the family assume s_model = 0, which is inconsistent with (c) (N1, A). The per-test N, σ, size and power tabulation is moved to the pre-registration (l.1808-1810) and not given now except for B1, B2 and B4-c. |
| M16 | time-tag credit | **D, genuine (design done)** | Timing model with collision-time spread, tails and out-of-time and noise occupancy (l.864-868). Hit-level prediction (l.869-870). Widened-window closure (l.871-874). Independence test (l.875-876). Floor at the sourced tail fraction (l.877-879). GA-9. The extrapolation from the widened window (~10⁻²) to the nominal one (~10⁻⁴) carries no width: N11 (B). |
| M17 | undeclared pre-verdict signal quantities | **R** | Complete list (l.467-478; COM BL-1). Threshold decided before A (l.479-480). B6 nominal partners after the verdicts (l.1053-1055). C2 count moved to 4c (l.507). Ordering problem with A and the MET model: N10 (B). |
| M18 | MVA argument | **R** | False claim withdrawn (l.205-208). Three reasons that hold (l.209-218). Hybrid excluded for blinding (l.219-220). Working point at equal total counted background (l.224-226). |
| M19 | costs and schedule | **R** (schedule in GA-8) | Provenance column (Table 4.0). 45 ms for the hard scatter, built from 23.4 + 14.1 + 7.5 ms (I verified FEAS_B l.117 and FEAS_A l.235). Multijets at 23.4 ms. P1 at 36.5 CPU-h. 10-slot capacity: 1,625 slot-h per week, 232 per day, 174 per day at 0.75 (script [2]; LOG 14:34 cap verified). ITERATE allowances and Gate-B turnaround (l.2050-2054). Development effort (l.2062-2066). The wrong sentence is corrected (l.2114-2115). Levers (l.2117-2125). |
| M20 | S1 "×10" | **D, genuine** | Stated (l.1392-1398). 14.6 % against 10.3 % (script [13]). +827 CPU-h = 80,000 × 25.2 s / 3,600 + 266 (script [6]). GA-2. |
| M21 | C1 chain per point | **R** | l.429-433; COM C1-e. |
| M22 | attribution rule | **R** | l.551-558; COM B1-f. |
| M23 | K validations | **D, genuine (criteria fixed)** | Validation 2 is NLO against NLO at 3 %, or NOT EVALUABLE (l.1457-1467). Validation 3 is differential (l.1468-1472). The parity argument and an implemented resummed cross-check (l.1477-1481). GA-5. |
| M24 | Herwig attempt; DPs in the paper | **P (honest)** | [DP5] is rewritten as attempt first (l.2101-2108). How each DP is carried into the paper (l.1788-1792). The install was not attempted because the install slot is the orchestrator's (AGENT_RULES). It is scheduled in Phase 2, days 0–7 (l.2044). The expected impact is not quantified (R-19). It is a dated commitment, not an evasion. |
| M25 | identifiers | **R** | COM is the master list, with a table of old to new identifiers (COM l.23-51). The identifiers I sampled in v2 (B1-a…g, B2-a…g, B3-a…d, B4-a…e, B5-a…c, B6-a…d, T1-a…i, T2-a…g, S1-a…f, S2-a…f) all exist in COM. I cannot check that no v1 row was silently dropped without the v1 COM, which is only in git, and I did not run git. COM says "nothing removed". |
| M26 | background list | **R** | Rows and readings (l.146-149, l.163-177). B1-g has a costed conditional (+160 CPU-h). |
| M27 | signal-side detector response | **R** (two parts retrieval-dependent) | Same MET model (l.1418-1419). Migration sample (l.1420-1426). L11 with the limit given against veto survival (l.1427-1433). R-14 window (l.1434-1438). Ordering problem: N10. |
| M28 | infracolour Coulomb correction | **D, genuine** | Formula and substitution: I recomputed α_IC = 2π/((22/3) ln(200 GeV/1 keV)) = 0.0448 and δ(0.7) = 0.75 × 0.0448 × (π/1.4 − 4/π) = +3.3 %. Default is a one-sided band (conservative). GA-5. The formula is tagged as coming from the review and is to be replaced through R-12. Acceptable at Phase 1. |
| M29 | background-side bias of T2 | **R** | l.1354-1359; 5,000 × 10.4 s = 14.5 CPU-h. |
| M30 | dE/dx forgone gain | **D, genuine** | l.1297-1300; GA-6 costs +391 CPU-h (script [13]). |
| M31 | B5 dominated by pile-up | **R** | Hard-scatter shares 10.2/8.3/6.2 % (script [13]). Closure on the truth-attributed component. T(Δφ) on no-pile-up samples. R07 loss stated: 7.7 counts against 27.7 (l.978-1006). |
| M32 | weighted samples | **R** | Model table row "counted, weighted" (l.1111). |
| M33 | multijets | **R** | l.943-949; COM B4-e. |
| M34 | post-freeze failure | **R** | Three-branch protocol (l.1820-1834); COM FP-1. Fresh overlays come from the contingency: N7. |
| M35 | sample inventory | **R** | 24 rows with role, stream, independence, phase and CPU-h (l.1575-1600). Overlay sourcing is not costed: N12. |

**Counts:** R 22 (M1, M3, M7, M8, M9, M10, M12, M14, M17, M18, M19, M21, M22, M25, M26, M27, M29, M31, M32, M33, M34, M35);
P 5 (M4, M5, M11, M15, M24); N 0; D 8 (M2, M6, M13, M16, M20, M23, M28, M30), all genuine.
The fix report's own count is 24 R, 3 P, 8 D. I downgrade M4 and M15 to P. Both are about the size of the widths and
false-fail rates presented to the user, which are understated (N1, N4).

**Discarded or fixed items not reintroduced (checked).**
- ρ = 3: absent (l.797, "a ρ = 3 sample is not").
- ×100 brute force: explicitly not proposed (l.636-637).
- Cloud: absent.
- Stage 3 at Λ ≥ 15 keV: absent (l.1403-1404; only the 8 grid Λ).
- Endcap: outlook only (l.1551-1554). GA-10 offers the *user* a wording change, which is the user's right, not a reopening.
- Pile-up scan and Open Data: absent.
- F was not loosened. The 1.5/2 values are unchanged (l.299-300).

---

## Part 2 — New findings on v2

### Category A

**N1 (A). The closure battery's false-fail and family-wise rates hold only for an estimator with no model error.
Criterion (a) is inconsistent with criterion (c).**
*Location:* §4.0 points 3–5 (l.284-322); GA-4 (l.2224-2226); script [11]; COM preamble l.14-19.
*Evidence:* Criterion (a) demands |ln r| ≤ ln F at every evaluable rung. Criterion (c) declares a model width s_model,
"the r.m.s. of ln r of that estimator on the development samples", allowed up to ln F. The rates v2 quotes (0.27 % per
rung, family-wise 7.5 % / 10.4 % at K = 12, and the "7.5–10 %" given to the user in GA-4) are computed at r = 1 exactly
(script [11]: `2*Phi(-3)`; `per = 0.05/K + …`). That is an estimator with s_model = 0. For an estimator that performs
exactly as its own pre-registered s_model says, my computation (python3, same Φ) gives:
- F = 1.5 with the placeholder s_model = 0.20: P(|ln r| > ln F) = 0.043 at negligible statistics and 0.093 at the
  evaluable limit σ = 0.135.
- F = 2 with s_model = 0.35: 0.048 and 0.098.
- At s_model = ln F, which (c) allows: 0.32–0.34.
With a coherent model shift, which is what s_model²·J encodes, the failures of the rungs of one test are not
independent. The per-test rate is therefore about the per-rung rate. Over K = 12 tests, the probability that a correct
analysis fails at least one test through (a) alone is 0.41–0.71, not 0.10. Under [SD8] a FAIL of a leading term's
estimator makes the selection ineligible. N1 therefore changes the expected paper outcome ("closure fails"). The user is
asked to decide GA-4 on the wrong numbers.
*What "fixed" looks like:* Make (a) and (c) consistent. Either (i) cap s_model so that (a) has a stated size for an
estimator at its own s_model (for example s_model ≤ ln F/2.6 for about 1 % per test), or (ii) define (a) on the
statistical part only, |ln r| ≤ ln F + k·σ_stat with s_model tested by (b). Then recompute, in the script, the per-test
size and power and the family-wise rate at the planned s_model values, and put those numbers into GA-4 and the
partial-outcome matrix (l.1361-1371).

**N2 (A). MUST acceptance criteria are planned to stay untested, and the conflict with brief D4 is not presented to
the user.**
*Location:* Table 4.4b (l.663-672) and l.675-680; B4-c (l.956-960); [L1]; GA-4 (l.2220-2223).
*Evidence:* Brief D4 (prompt.md l.72-75) says "A MUST item gets the statistics its acceptance criterion needs". It is a
fixed user decision (§3, "do not reopen").
- B1-a: v2 plans B1-a to be NOT TESTED for PV pairs (the largest floor, 18.5 of 45.3 events), the NI terms and loopers.
- B4-c: v2 plans B4-c to be NOT TESTED for 11 of 12 processes, including W(τ_h) (floor 2.41).
- For W(τ_h) the fix is costed at +61 CPU-h (l.958-960) and declined "because Z(νν) carries 61 %". That is a choice
  against D4 made for 61 CPU-h, about 1.4 % of the total.
- For PV pairs the fix report computes ≈ 340 CPU-h for 24 counts at R05 and rejects it because R05 is a derivation rung.
  No alternative design is offered, for example derivation at R04 only with the held-out test at R05, or an
  importance-sampled PV-pair overlay.
GA-4 asks only what NOT TESTED earns. It does not say that the default plan breaches D4 for these MUST criteria, and it
offers no costed option to comply. The arbiter's M5 fix (b) required either raising the samples "or the criterion
changed and the change put to the user (brief D4)". Neither was done.
*What "fixed" looks like:* For every MUST criterion with expected verdict NOT TESTED, either size it to be evaluable
(W(τ_h), tt̄ 1ℓ and W(τ_ℓ) to a count of 24 or more in the test half; PV pairs through a redesigned rung split or an
enrichment target with a cost), or add a Gate-A item "D4 exception for B1-a (PV, NI, loopers) and B4-c (processes …)"
with the cost of compliance per term, the consequence (entry at H) and a recommended default.

**N3 (A). The pre-declared reading "target met" is earned by a background made only of zero-count bounds.**
*Location:* §4.11 point 3 (l.1183-1185); COM TG-1; §4.4 Readings (l.632-633); §0.
*Evidence:* "Target met" is defined as σ_ln = ½ ln(B₈₄/B₁₆) ≤ 1 at the chosen selection. With every term at its zero-count
floor, the predictive distribution of the summed floor has σ_ln = 0.41. That is script [9], 200,000 draws: 16 % 24.1,
84 % 55.2, ½ ln(55.2/24.1) = 0.41. A sum of about 20 independent exponentials of similar scale has a small relative
width. A fully bounded result (f₀ = 1) would therefore be reported as "target met" alongside "sample-size limited". The
plan's central target (σ_ln ≲ 1 for an *estimated* background) is satisfied by the treatment, not by the physics: the
motivated-reasoning pattern that M1 was raised against, moved to the outcome label.
*What "fixed" looks like:* Define "target met" as σ_ln ≤ 1 **and** f₀ ≤ 0.5 (or compute σ_ln over the estimated terms
only, with the bounded part quoted separately). State in §0, GA-3 and TG-1 that the expected zero-count outcome is
"target not met: sample-size limited".

### Category B

**N4 (B). The extrapolation widths given to the user are computed with fitted slope errors that the planned tests cannot
produce. The rung-index distance problem remains.**
*Location:* §4.0 point 7 (l.343-360); §4.5 (l.793-795); §4.12 distances (l.1348-1352); GA-4 (l.2227-2228); script [12]
(l.506-513 of the script).
*Evidence:* The rule (l.344-345) is "with fewer than three evaluable rungs in the family, σ_b := b₀". The planned tests
fall short of three rungs in every case:
- B1 tests at R06–R07: 2 rungs in the width family.
- B2-b tests at R06–R07: 2 rungs.
- B4-c tests at R06: 1 rung.
- B3 stability has one test value.
Yet the substitution and the script use σ_b = 0.029 (pile-up) and 0.097 (single interaction), taken from review N-B-3
for a different design. With σ_b = b₀, my computation gives:
- Pile-up (occupancy model, the declared one-estimator extrapolation beyond R07): 0.45 / 0.61 / 1.30 / 2.47 at
  R08 / R09 / R11 / R14, against 0.20 / 0.45 / 1.23 / 2.44 quoted.
- Single-interaction promotion: 0.78 / 1.04 / 2.22 / 4.23, against 0.36 / 0.78 / 2.11 / 4.17.
The rule is also ambiguous. A family with evaluable rungs but no fitted slope (R08) could count as d_in or d_out, and b̂
is undefined with two points. Two implementers would get different widths. The distance still counts rung indices
regardless of whether the rung acts on the extrapolated quantity. Example: π_k is a layer-promotion probability, and
R09–R11 change only the fit-probability cut, yet each adds ln F. A conditional measured at R09 at the deepest and applied
at R15 carries about 1.8 (×6 at B₈₄). Even so, §0 (l.49-51) lists "conditionals of purpose-built cuts" as one of three
things that can lower the floors, without saying that.
*What "fixed" looks like:* Substitutions and script consistent with the stated rule. d_in/d_out and b̂ defined for 1–2
evaluable rungs. The distance defined per extrapolated quantity (counting only rungs that change a cut the quantity
depends on), or this kept as an explicit, flagged convention in GA-4 with both numbers. §0 stating the conditionals'
expected widths.

**N5 (B). The statistical model is not fully specified for factors that are probabilities.**
*Location:* §4.11 point 1 model table (l.1112-1113); §4.4 (l.571-583).
*Evidence:* S, π_k, conditionals and the time-tag fraction enter as nominal × log-normal with width bootstrap ⊕ s_tot(r).
s_tot reaches 2–8 at deep rungs (script [12], and N4). Draws then exceed 1, and P(r | t) exceeds the directly measured
ceiling H in the toys and in B₈₄. Nothing states truncation, a cap at H, or a logit parametrisation. The B₈₄ of a term
with a tested estimator can then be *larger* than its no-credit value, which contradicts "an untested estimator …
never better" (l.1315-1316) and the "leading" logic. Also unspecified:
- the μ grid and CLs interpolation behind the 8 μ values per point;
- the true rates used in T1-h ("fixed true rates");
- whether T1-h redraws m.
*What "fixed" looks like:* A declared rule, for example P_t := min(P_geo·S + Σ f_k π_k, H) in every pseudo-experiment and
probability factors capped at 1, with its effect on coverage tested in T1-c. The μ grid and interpolation stated. T1-h's
true λ values stated.

**N6 (B). The single-interaction redesign is not complete: H is not shown to be a ceiling.**
*Location:* §4.4 point 4 (l.559-583); B1-f.
*Evidence:* "Law of total probability over the no-pile-up state" (l.567) partitions the no-pile-up events into "passes r"
and "passes the width cut and misses the layer count by exactly k". The partition omits two classes:
- events that fail the width cut (or the core definition) without pile-up and pass with it, because added hits change
  the plane fit and which hits form the core;
- candidates whose plane differs from the no-pile-up plane.
Nothing tests these classes, so P ≤ H is asserted, not shown. Two definitions are also missing: k is not defined per layer
type (N_IT2, N_IP2, N_2S2 have separate thresholds at R01–R04 and R12–R14), and "the rung's width" for π_k at R04 (a
counting rung) is undefined. Method, cost (294 CPU-h of overlays) and statistics (Table 4.4b) are given. The completeness
claim, which carries the no-credit default for the largest term, is not.
*What "fixed" looks like:* Either add the missing classes to the estimator, or add a criterion to B1-f: on the test
overlays, the fraction of attributed passers whose no-pile-up event lies in none of the enumerated classes is below a
stated bound, measured where evaluable. Define k per layer type and the width used for π_k at counting rungs.

**N7 (B). GA-8 asks the user to approve a compute envelope that the strategy itself expects to exceed by more than 30 %.**
*Location:* §11.2 (l.2020-2038); §11.6 (l.2145-2155); GA-8 (l.2250-2254); §8 (l.1828-1829).
*Evidence:* The default approves 4,401 CPU-h, so the stop threshold is 5,722 (I verified 1.3 × 4,401 = 5,721.3). The
strategy carries a provenance contingency of 1,989 plus a 403 reserve (script [6]: "reduced total with both: 6793"). It
also draws the following costs "from the contingency":
- fresh B1/B4 test overlays, up to 294 CPU-h;
- the +160 CPU-h of Geant4 secondaries;
- the 403 CPU-h fresh direct sample.
A draw above 1,321 CPU-h stops the study, and l.2154 says "if the guesses are low by a factor 2 … the rule triggers at
checkpoint 1". GA-8 offers no alternative that approves an envelope including the contingency. It does not say whether a
contingency draw counts as an "overrun of the approved schedule", which brief D6 requires to be reported.
*What "fixed" looks like:* Add the alternative "approve 4,401 plus the contingency of 1,989 = 6,390 as the envelope
(threshold 8,307)". State for each conditional cost whether it is inside the approved figure.

**N8 (B). The fallbacks for retrieval tasks that find nothing are not neutral, and they are not Gate-A items.**
*Location:* §4.9 (l.1029-1030); COM B6-d; §4.7 MET model (l.921-930, l.961-962); §12.4.
*Evidence:* "If no public number is found for a variation, there is no nuisance for it." A missing material, resolution
or efficiency uncertainty then contributes zero width, which makes the limit optimistic, not conservative. JFC forbids
round-number inflation. It does not license zero. The MET model has *no* parameter value (l.921-924). If R-3 returns
nothing usable, B4-b (MUST) has no model to validate: the "not validated → full variation as width" branch presumes a
model and a variation range that would not exist. The fixer lists M9, M11, M16, M27 and M28 as resting on retrieval.
M16, M27 and M28 have conservative fallbacks (no credit; limit against veto survival; one-sided band). M9 and M11 do not.
*What "fixed" looks like:* A Gate-A item on the no-source policy (zero, robustness size flagged as unsourced, or a stated
bracket from the v1 record), and a defined B4-b path if R-3 yields no parameters. Retrieval R-3 and R-15…R-17 with a
deadline before the freeze (decision point 2).

**N9 (B). The strategy reads brief D7 to allow signal "production input" before the freeze, and decides that reading
itself.**
*Location:* §4.13 cost (l.1439); §4.17 samples 7 and 10 and l.1602-1604; §11.3 (l.2044).
*Evidence:* D7 (prompt.md l.86-87) says the pre-registration "must … be hashed and committed before any v2 production
sample exists". v2 generates the S1 Stage-2 samples (47 CPU-h) and the full Stage-3 string propagation for all 40 points
(266 CPU-h) in Phase 2. It labels them "production input of S1" and exempts them because "their content does not depend
on any analysis choice". This may be harmless, since the samples are truth level and their halves are assigned at the
freeze. It is still an executor's interpretation of a fixed user decision, and the same reading was in v1 (v1 l.726,
l.1111) without being raised. Only the user can grant it.
*What "fixed" looks like:* A Gate-A line asking the user to confirm that truth-level Stage-2/3 signal samples may exist
before the hash (with the argument), or relabel them as development and move them after the freeze (calendar effect
≈ 1.5 days at 174 CPU-h per day).

**N10 (B). The acceptance A and the migration test need the MET model before it exists.**
*Location:* §4.1 item 2 (l.469-473); §4.13 S1-f (l.1418-1426); §4.7 (l.922-923); §11.3.
*Evidence:* A = ε_fid × ε_trig × ε_presel and the migration fraction m_mig are formed "in Phase 2" (l.469-470;
sample 8, phase 2). Both use the trigger and offline MET, which in v2 come from MET_reco (S1-f, l.1418-1419), with
parameters from R-3 and the model frozen at the pre-registration (end of Phase 3, l.921-924). The S1-f rule "if
m_mig > 5 %, the generator cut is lowered before the freeze" and [SD10] both depend on a model that is built in Phase 3.
Either the Phase-2 A uses another MET definition, which is then a second signal quantity, or the schedule is wrong.
*What "fixed" looks like:* An ordered list: R-3 → MET model → A and m_mig → generator-cut decision, placed in the
calendar before the freeze, with A computed once.

**N11 (B). The time-tag credit is taken at a window where it was never tested, with no width for the extrapolation.**
*Location:* §4.6 B3-c points 2–5 (l.869-879).
*Evidence:* The closure moves the window edge until p_late ≈ 10⁻² and tests at five such edges. The credit is p_late at
the *nominal* window, which is about 10⁻⁴ per the book (l.862-863). The prediction is extrapolated about two decades along
t_cut, where the non-Gaussian tail matters most. The only width mentioned is the slope "against the rung" (l.875-876),
which is a different direction. The floor "never below the sourced tail fraction" is a lower bound on p_late, not a
width.
*What "fixed" looks like:* A width on ln p_late that grows with the distance in t_cut (or in ln p_late) from the
deepest tested edge, defined as in §4.0 point 7, or the credit limited to the deepest tested edge.

**N12 (B). The no-pile-up events behind the overlays are neither sized nor costed.**
*Location:* §4.4 closure design (l.652-659); §4.17 sample 19 ("different no-pile-up events" from 11 and 17); script [3]
(overlays: 42,000 × 25.2 s only).
*Evidence:* For each leading topology, the derivation overlays need 2,000 passers and 2,000 near-pass events. The test
overlays need 4,000 enriched events, and for PV pairs at R06–R07 an enrichment of 10²–10³ (l.671). All of them must come
from no-pile-up events disjoint from the 1.2×10⁸-event pool. Finding them requires scanning a no-pile-up sample whose
size is set by P_geo and f_k at R04–R07. That sample has no line in the budget or the inventory. At 11.5 ms per event,
10⁸ events would cost 320 CPU-h. The claim that the script prints "every CPU-h number" is then incomplete, and the
PV-pair test may be unaffordable.
*What "fixed" looks like:* The scan size per topology from the pilot's f_k (as a formula now, with a planning value),
with its CPU-h in script [3] and a row in §4.17.

### Category C

- **N13.** The T2-e check (l.1343-1346; COM T2-e) compares the convention with "zero-count terms fixed at 1.14·N/M". For
  κ ≲ 3 the convention gives a *stronger* limit than the fixed value (κ = 1: 3.0 against 4.1, script [10]). The check
  can therefore fail for a correct model at shallow selections. Compare instead with the term-dropped value (3.0) and
  with the analytic one-bin limits.
- **N14.** Sealed tier (l.449-461). State that the family-coherence z (l.418-419) of the signal families and the global
  χ² include sealed quantities and are reported as PASS/FAIL only. The sealed file under
  `QV2/phase2_exploration/sealed/` is in the shared, readable repo. Keep it outside the agents' tree (or encrypted, with
  the key held by the orchestrator) rather than relying on "no agent reads it".
- **N15.** The labels overlap. A factor with m = 0 whose estimator is NOT TESTED is a "bound" by l.1186-1188, but the
  partial-outcome table labels PV pairs "no credit" (l.1366). Give an order of precedence.
- **N16.** GA-8 (l.2254) says levers "(i)–(iii), up to −420 CPU-h". (i) + (iii) = 422 and (ii) is a further −126. Say
  which are summed.
- **N17.** l.1237: the key is `limits.json` → `points["A2|F|200|1.5|BM"].expected_toys.median`. The value 12,458,208 is
  correct.
- **N18.** B1-e (MUST) commits to biased generation, while GA-3 (ii) presents biased generation as an option conditional
  on a gain ≥ 5. Reconcile: biased always, with the pool split decided by the gain?
- **N19.** Coherence and length. "v1 of this document" occurs 32 times in the body. The document reads in places as a
  diff against v1, not as the current strategy. Move the comparisons to §13 or the fix report. N-C-11 asked for a
  shorter document; v2 is 1,143 lines longer.
- **N20.** In Table 4.4b, the PV-pair R05 entry "2" is derived from the ratio of B values (0.25 per 500, script [11];
  D4 l.197 shows "(6/24)" in that cell), not a v1 count. Tag it [E].
- **N21.** The B5-a test (signal road against sideband roads of the same events, l.993) is not on disjoint samples.
  Label it as limited by B5-c (road independence), or use events not used for T.
- **N22.** K = 12 "planning value" (l.316-317). The eligibility family plausibly holds B1-a × 4–8 topologies, B4-c × the
  evaluable processes, B2-a/b/c and B3-a…d, which is more than 12. Fix K now from the list, since it sets the 0.05/K
  threshold.

---

## Part 3 — Numbers: script rerun and spot checks

**Script rerun.** `python3 -I phase1_strategy/src/strategy_budget.py`: exit 0, 300 lines. It reproduces:
- MUST 3,968; MUST + SHOULD reduced 4,401; full 4,915 CPU-h ([4]).
- 1,625 slot-h per week and 174 core-h per day ([2]).
- Calendar 55.5 / 57.9 / 60.8 days, 44 non-production days ([7]).
- Stop threshold 5,722; provenance M/D/G 1,074 / 2,066 / 1,261; contingency 1,989 ([6]).
- Storage 413 / 613 GB ([8]).
- Floors 45.3 / 86.2 / 22.7 at 600 / 315 / 1,200 CPU-h ([9]).

By hand (summing the script's own lines):
- B1 = 27 + 60 + 17.5 + 65.1 + 15 + 51.9 + 382.8 + 294.5 = 913.8.
- B4 = 266.4 + 217.2 + 65 + 12.5 + 50 = 611.1.
- T1 = 60 + 20 + 20.3 + 144.9 + 173.9 + 0.5 = 419.6.
- Phase-4a reduced production = 2,010 + 404 = 2,414 → 13.9 days.
- Calendar 7 + 9 + 2 + 2 + 13.9 + 3 + 2 + 3 + 2 + 2 + 3 + 7 + 2 = 57.9 days.
- DP savings 357 + 155 = 512 → 2.9 days.
- GA-2 +827 → 4.75 days.
All consistent with §0, §4, §11, §12.1 and COM.

**Stale-value grep.** Searched v2 and COM for 2,950 / 3,275 / 3,798 / 3,930 / 360 GB / 560 GB / 42 days / 200 core-h /
655. The old totals and 655 appear only as explicit v1 comparisons (l.53, l.1973, l.1977, l.2014, l.2038). 3,930,
360 GB, 560 GB, 42 days and "200 core-h" have no hits. No stale value found.

**Spot checks of VERIFIED numbers (20), all against the source:**

| # | v2 claim | source checked | result |
|---|---|---|---|
| 1 | min B₈₄ SR-G 1.2346×10⁶ (l.36) | `SUM` → `ladder.SR-G.min_B84` = 1,234,586 | ✓ |
| 2 | fallback FB2, 9/200 at E 200/1.5; FB3 10/200, 11/200 (l.404-406, l.440) | `SUM` → `fallback_points` `r_fb`, `k_rfb`, `n_den`, `e_adm` = None | ✓ |
| 3 | proxy share 0.147 at R04, 0.445 at R09 (l.892-893) | `SUM` → `sm_proxy_fraction_of_B_SM` 0.1472, 0.4452 | ✓ |
| 4 | N_trig 4.0848×10⁷ ± 2.0 % (l.128) | `bsum_wp.json` → `n_trig.value` 40,848,448, `rel_stat` 0.0202 | ✓ |
| 5 | Z(νν) N_trig 2.508×10⁷; W(τ_h) 5.41×10⁶ (Table 4.4a) | `n_trig.breakdown` 25,078,825; 5,407,123 | ✓ |
| 6 | v1 μ₉₅ 1.2458×10⁷ events (l.1237) | `limits.json` `points[…1.5…].expected_toys.median` 12,458,208 | ✓ (key path, N17) |
| 7 | finder ε over the TEMPLATE half; A definition (l.1393-1394, l.1400-1401) | `acceptance.json` `factors.finder_note`, `definition` | ✓ |
| 8 | Z(νν)+j shower 23.4 ms (Table 4.0) | FEAS_B l.117: 23.41 ms | ✓ |
| 9 | 34 ms per LHE event, derived (Table 4.0) | FEAS_B l.129 | ✓ |
| 10 | gun through the chain 14.1 ms | FEAS_A l.235 | ✓ |
| 11 | PU-200 event 13.5 ± 1.1 s; no-PU 11.5 ms; trial 11.7 s; B1-type 60.4 s | FEAS_A l.23, l.234, l.203, l.246 | ✓ |
| 12 | ρ = 2 event 206 s, 1.46 GiB at 1 event (D) | FEAS_A l.247: "1-event smoke 206 s **wall**", 1.46 GiB | ✓ (it is wall time; the D tag is right) |
| 13 | pyhf 0.12 / 0.52 / 10.4 / 652 s, 31 parameters | FEAS_C l.28-29, l.215 | ✓ |
| 14 | K = 1.165 ± 0.002, +1.6/−1.1 % | FEAS_B l.19-20, l.160 | ✓ |
| 15 | 12.21 ± 0.03 pb against 14.6 pb, ratio 0.84 | FEAS_B l.83 | ✓ |
| 16 | gun 0.134 ms; vertices 1.1 % decays, 4.2 % inelastic, 5.3 % total | FEAS_B l.192-194 | ✓ |
| 17 | QED-FSR shower 21.1 against 21.2 ms | FEAS_B l.118, l.127 | ✓ |
| 18 | two workers capped at 3 jobs (l.1942-1943) | LOG.md 14:34 | ✓ |
| 19 | 21,137 hits / 463 events at E 200, 1.5 keV; 0.037 s per event at F 500, 0.45 keV (l.267, l.408) | `STAGE3_INDEX.json` `points["p2/F_m200/L1.5_BM"]`; F 500 L0.45 chunk c00: 3.74 s / 100 events | ✓ |
| 20 | Table 4.4b inputs (DIF 166/81/2/1; γ 153/86/13/2; V⁰ 859/358/6/0; Z(νν) 81 raw at R06; W(τ_h) 9.0, tt̄ 1ℓ 5.2, W(τ_ℓ) 3.0); thinning s_ln 0.0077/0.0079/0.0060 | D4 l.187-198 | ✓ (PV-pair R05 derived, N20) |

Also re-derived independently, beyond the script:
- the √(N/c) allocation, by the closed form and the equal-marginal (KKT) check;
- the one-bin limit at κ = 35 (27.8);
- the coverage at κ = 1, λ = 0.5 (0.9448);
- the evaluable-count thresholds;
- the family-wise rates (7.5 % at s_model = 0; N1 for s_model > 0);
- α_IC and δ(β);
- the stop threshold.
Brief §7 and D6 are quoted exactly (prompt.md l.341-348, l.79).

---

## Part 4 — Specific questions of the brief to this review

- **Statistical model reproducible by two people?** Almost. The counted, weighted, estimator and no-credit factor kinds,
  the generation convention, the auxiliary data, the test statistic and the Asimov definition are specified. Three gaps
  would make two implementations differ: the treatment of probability factors under wide log-normals (N5), the d_in/d_out
  and b̂ rule for 1–2 evaluable rungs (N4), and the μ grid. Derivations are shown with substitutions and limiting cases.
  The coverage claim reproduces (0.9448 at κ = 1, λ = 0.5).
- **T2 protected against empty simulation?** Yes, in substance. Gamma(m + 1) generation keeps every zero term at
  N_t/M_t per unit λ, "one zero per term" stops products of bounds, and the floors are equal at deeper rungs. Residuals:
  N13 (the check can fail at small κ) and N3 (the outcome label).
- **Floor table:** recomputed (PV pairs M = 7.65×10⁷, floor 18.45; DIF 1.75×10⁷, 4.23; Z(νν) 5.5×10⁶, 5.19; WZ 0.41×10⁶,
  0.38; sum 45.3). The allocation is optimal for Σ N_t/M_t.
- **Closure scheme:** Test rungs are disjoint from derivation rungs for every estimator (M3), with B5-a a weak case
  (N21).
  - Evaluability: the thresholds are correct. False-fail and false-pass rates were checked for two tests (F = 1.5 and
    F = 2: 0.27 %, 93 % at F^1.5, 99.9 % at F²). They hold only at s_model = 0 (N1).
  - Multiple-testing arithmetic: correct as stated (0.0065 per test, 7.5 % family). It assumes independence and
    perfect estimators (N1).
  - NOT TESTED earns no credit consistently: §4.0 point 6, §4.4, §4.6, §4.7, §4.12 rule 1, COM T2-a and [SD8] agree.
  - b₀ = ln F per rung is an arbitrary convention. v2 says so (l.352-355), anchors it to v1's 0.36 per rung, and puts
    the alternative in GA-4. Flagged correctly, but its numbers are understated (N4).
- **Single-interaction estimator:** method, statistics, cost and risks are present. Completeness of the ceiling and the
  definitions of k and width are missing (N6). The overlay sourcing is not costed (N12).
- **Blinding (C1):** the sealed tier closes the practical leak of the six candidate efficiencies, since it reports only
  PASS/FAIL against already-public v1 values. Small residual channels: N14. The exception is properly left to the user.
- **Retrieval-dependent items and the Herwig install:**
  - M16, M27 and M28 are honest, with conservative fallbacks.
  - M9 and M11 are honest PARTIALs in their *design*, but their fallbacks are not neutral (N8).
  - M24 is a dated Phase-2 commitment.
  - No retrieval task has a deadline relative to the freeze, except R-10 ("before 4a").
- **Gate-A list GA-1…GA-10:** each can be answered in one line, with a default, alternatives and costs.
  - Missing: the D4 exception for untested MUST criteria (N2), the no-source policy (N8), the D7 reading (N9) and an
    envelope including the contingency (N7).
  - Should have been fixed rather than asked: the GA-4 false-fail numbers (N1) and the TG-1 definition (N3). These are
    errors, not decisions.
- **COMMITMENTS:** every plan item C1–C3, B1–B7, T1–T2, S1–S5 and P1 has a row. Every "Will implement" of §5.1 has an
  SY row. Criteria agree with v2 for the rows I compared (B1-a, B2-a/b/c, B4-c, T1-c/d/h, T2-e, S1-a, ST-1, TG-1), with
  one exception: COM B4-c says "test half at R06", v2 "R06 (and R07 where evaluable)". The old-to-new table covers every
  renamed identifier. I could not verify "nothing silently dropped" without the v1 COM from git.
- **Competing group:** "What would they have that we don't?"
  - Justified absences: full detector simulation with clusters on modules ([L8], A8, public information only);
    endcap acceptance (brief D1); a data-driven sideband in real data ([A1]); an MVA selection (blinding argument,
    [DP3]); dE/dx (GA-6).
  - Unjustified: the leading backgrounds measured rather than bounded. At the planned sizes the expected result is
    ~45 bounded events, and N2 shows that cheap steps toward testing those terms (W(τ_h) for 61 CPU-h; a PV-pair rung
    split) were not taken or not offered.
  This is what N2 and N3 make Category A.

---

## Part 5 — Conventions coverage, row by row (`conventions/search.md`, against v2 §5)

| conventions item | v2 answer | judgment |
|---|---|---|
| CLs (CL_s+b/CL_b) | T1, l.1170 | ✓ |
| Asymptotics only above ~5 events; toys otherwise | toys primary (l.1222-1228); asymptotics for ranking only (l.1175-1177) | ✓ |
| Test statistic q̃_μ, μ ≥ 0 | l.1169 | ✓ (T1-d fits μ unbounded for injection, which is correct for a bias test) |
| Signal injection 0, 1, 2, 5× | T1-d, multiples of μ₉₅^exp | ✓ |
| Signal cross-section theory | WI (S2, scales, PDF), band on the theory line | ✓ |
| Signal acceptance (generator comparison, ISR) | WI: MLM against FxFx at 500 and 1,500 GeV, qCut, tune | ✓ |
| Signal shape | translated (SR-T/SR-G migration, timing) | ✓ |
| ISR modelling | WI as f₂₀₀ | ✓ |
| 4-fermion (irreducible generator comparison) | WI, translated; no second generator for tt̄ and dibosons, stated as a limitation | ✓ (limitation acknowledged) |
| Background normalisation | WI | ✓ |
| Background shape | N/A as written; role taken by the extrapolation widths | ✓, but the widths are understated (N4) |
| qq̄(γ) modelling (2-fermion generator) | WI, translated: tune and Herwig after an install attempt [DP5] | ✓ (M24 partial) |
| MC statistics (Barlow–Beeston) | WI: Poisson auxiliary channels, weight classes | ✓ |
| Detector simulation model | translated, WI; sizes from R-15…R-17 | ⚠ fallback "no nuisance" (N8) |
| Object calibration | WI: MET, trigger, ε_PV, timing, readout window | ⚠ MET model depends entirely on R-3 (N8, N10) |
| Beam energy | N/A, with reason | ✓ |
| Luminosity | WI (R-9) | ✓ |
| PDF (pp) | WI | ✓ |
| Pile-up (pp) | WI at fixed ⟨μ⟩ = 200 (brief D8) | ✓ |
| QCD scale | WI | ✓ |
| Fragmentation (string against cluster) | WI at generator level after the install attempt | ✓ (M24) |
| Heavy flavour | N/A as written; displaced b/c vertices checked as a topology (SY-14) | ✓ |
| Check 1: closure p > 0.05; failure is Category A, fix the model | translated, with the family-wise rule (outright FAIL only at p < 0.05/K) and the failure protocol | ⚠ relaxes the conventions' per-test p > 0.05 (flagged in GA-4); stated sizes wrong (N1) |
| Check 2: injection, > 20 % bias investigated | T1-d | ✓ |
| Check 3: pulls within ±1σ; > 2σ investigated | T1-e uses a mean-pull criterion and boundary hits | ⚠ C: add the conventions' per-nuisance reading (a nuisance whose pull exceeds 2σ in more than a stated fraction of the fluctuated fits is investigated) |
| Check 4: impact ranking | T1-f | ✓ |
| Check 5: GoF | N/A (no data); closure χ² reported with JFC alarm bands | ✓ |
| Check 6: look-elsewhere | N/A, fixed grid | ✓ |
| Pitfall: VR blind spot | addressed by the widths, P_geo and H at depth, and B2-c | ✓ in kind; magnitude N4 |
| Pitfall: transfer-factor instability | b̂ reported per estimator | ✓ |
| Pitfall: pruning | T1-f, 1 % each, 5 % in quadrature | ✓ |
| Pitfall: asymptotics at low statistics | toys primary | ✓ |
| Pitfall: optimising on data | optimisation half only; evaluation half after Gate B | ✓ |

Reference-analysis table (§6.1): present, with R1–R4. R3's and R2's methods are "not extracted", with R-10 before 4a.
Acceptable at Phase 1.

---

## Verdict recommended to the arbiter

**ITERATE.** The three A items are fixes, not decisions:
- N1: recompute the closure sizes with s_model and make (a) consistent with (c).
- N2: comply with brief D4 or add the costed exception to the Gate-A list.
- N3: tie "target met" to f₀.
All nine B items can be done by the strategy executor. N7, N8 and N9 add lines to the Gate-A list.
Cycle-1 findings: no regression and no discarded item reintroduced.
