# Arbiter verdict: Phase 1 STRATEGY v2 (quirks v2), review cycle 2

Arbiter: Eloise, 2026-11-13 20:45. I am fresh to this panel and did not arbitrate cycle 1. I followed the Prompt
Template of `agents/arbiter.md` in full.
Artifact: `phase1_strategy/outputs/STRATEGY_dmitri_2026-11-13_19-25.md` ("v2"), `COMMITMENTS.md` ("COM"),
`phase1_strategy/src/strategy_budget.py` ("script") and `outputs/FIX_REPORT_cycle1_dmitri.md` ("FR").
Cycle-1 verdict: `review/arbiter/STRATEGY_ARBITER_dagmar_2026-11-13_19-00.md` (M1–M35).
Cycle-2 reviews:
- physics, Dolores (P): 1 A, 7 B, 9 C;
- critical, Dorothea (K): 3 A, 9 B, 10 C;
- constructive, Edmund (N): 1 A, 7 B, 11 C.
All three are dated 2026-11-13 20:10. There is no plot validator, because Phase 1 has no figures.
Also read: `AGENT_RULES.md`, the study and phase `CLAUDE.md`, `FRAMING.md`, `prompt.md` §3 (D1–D10) and §7, and
`ORCHESTRATOR_STATE.md` l.20.
I read these parts of v2 myself: l.1-180, 268-367, 540-720, 950-962, 1032-1044, 1100-1375, 1598-1606 and 2015-2275.
I opened v1's `TT/acts/stage4/analysis/gen_d123.py` and `TT/acts/stage4/code/s4cp.py` to settle the factual points.
Arithmetic was done with standard-library `python3 -I` (session log). No sub-agents and no git commands were used.

**Verdict: ITERATE.** There are 18 new merged findings, **4 Category A (N1–N4) and 14 Category B (N5–N18)**.
For M1–M35 the final status is:
- 20 RESOLVED;
- 7 PARTIALLY RESOLVED (M4, M5, M11, M12, M15, M24, M26);
- 8 DEFERRED TO GATE A, all of them accepted as genuine human decisions or as defaults.

Nothing needs the user outside the normal Gate-A decisions, so the verdict is not ESCALATE.

---

## 1. Overall assessment

v2 is a real redesign, and all three reviewers confirm it independently. The zero-count convention is specified and
derived, and every number of its one-bin table and its coverage was reproduced by three people. Closures are now
held out, on disjoint rungs and samples. The stop rule is quoted word for word. The floor table is optimal and the
reviewers reproduced it. The expected outcome is stated with unusual honesty: "middle in size, bounded in kind".

It is not yet approvable. Every remaining A item has the same structure: **a number or label that the user or the
paper will read passes, or looks better, by construction.**
1. The ceiling H carries the expected headline for the largest terms. It is called "measured directly", but nothing
   tests that it is a ceiling (N1).
2. MUST closures are planned to stay NOT TESTED, and the conflict with brief D4 is not put to the user (N2).
3. "Target met" is earned by a background made only of zero-count bounds (N3).
4. The closure false-fail rates shown to the user in GA-4 assume estimators with no model error. A correct-as-declared
   analysis would fail at least one test with probability 0.41–0.71, not 0.10 (N4).

The B items correct numbers that all lean the same, favourable way:
- the extrapolation widths are understated against v2's own rule (N5);
- probability factors are not capped (N6);
- the headline omits H and the deep pile-up term (N7);
- the floor double counts the prompt hard-vertex tracks (N8);
- the premise of the pile-up-secondaries test is factually wrong (N9).

They also add several schedule and procedure gaps.

**Proportion.** None of these needs new production. The net CPU effect of my rulings is about −100 CPU-h (§5). The
fix is text, test design and re-analysis rules, and it can be done in one pass. I have written the work list (§6) so
that cycle 3 can be a verification pass.

---

## 2. Facts settled from sources

| question | evidence (opened by me) | ruling |
|---|---|---|
| What does v1 call a "PV pair"? (P-B2) | `gen_d123.py` l.159-160: `ch_phi` collects **prompt charged final-state particles of the hard-scatter event**, pT > 0.05, \|η\| < 1.2. l.172-179 `pvpairs()` counts pairs whose mean φ is in the road. l.253 `R['pvpair'] += w * pvpairs(...)` runs on the preselected SM events. The *gun kinematics* of the P_geo sample come from one minimum-bias interaction (`s4cp.py` l.13). | The rate of 30.3 per triggered event counts pairs of prompt hard-scatter tracks of the same SM events that B4 simulates as real events. The overlap is real. P-B2 stands, and so does the double count (≤ 18.5 of 45.3 events). The P_geo of the term is a proxy: it uses pair kinematics from minimum bias, not from the hard scatter. |
| Do the other v1 topologies overlap with B4 too? (my check, Case 5) | `gen_d123.py` docstring l.21-23: "gamma/V0/PV-pair/looper from the HS vertex". γ, V⁰ (Pythia decays) and loopers (prompt soft tracks) of the hard-scatter event are also present in B4's Fatras simulation of real SM events. Fatras converts photons. | The overlap question applies to **every** topology sourced from the hard-scatter vertex, not only to PV pairs. It is folded into N8. |
| Did v1 already include pile-up decays and nuclear interactions? (P-B1) | `gen_d123.py` l.22-23: "NI parents and DIF from the HS event + Poisson(200) minimum-bias interactions (per-interaction rates x 200)"; l.286-287 `per_PU200_event = 200 × …`. `s4cp.py` l.110-113: the gun vertex is the event's drawn PV. | **Yes.** v1 counts pile-up NI and DIF, but places them at the PV, not at the pile-up vertex's own z. v2 Table 2.1 l.147 ("B1 treats the triggered event only") is factually wrong. P-B1 stands. |
| Is the false-fail rate of GA-4 computed at s_model = 0? (K-N1, N-B5) | v2 l.284-286 and l.320-322 (r = 1 exactly); script [11]. My recomputation: P(\|ln r\| > ln F) = 0.043 / 0.093 (F = 1.5, s_model 0.20, at σ_stat = 0 / at the evaluable limit 0.135), 0.048 / 0.098 (F = 2, s_model 0.35). Over 12 tests, 1 − (1 − p)¹² = 0.41–0.71. | **Yes.** K-N1 is correct. |
| Do the quoted widths follow v2's own rule? (P-B3, K-N4, N-B2) | v2 l.344-345 (σ_b := b₀ with fewer than 3 evaluable rungs in the family). l.656-658, 755-756, 955-956: tests at R06–R07 only. Script l.507 hard-codes σ_b = 0.029 and 0.097. My recomputation for pile-up, R08 / R09 / R11 / R14: 0.45 / 0.61 / 1.30 / 2.47 (v2 quotes 0.20 / 0.45 / 1.23 / 2.44). | **No.** All three reviewers are correct. |
| Does H include the fit-probability and shape cuts? (bears on N1, N7) | v2 l.573-575: "H applies the counting and width cuts only". The fit-probability and shape cuts enter only through B3 conditionals, and an untested conditional is 1. | For an untested term, H is flat from R08 through R11 and across R15–R20. The headline at deep candidates is set by H at the R08 width and the 2S counting rungs. This sharpens N1 and N7. |
| Is the B4-c W(τ_h) fix really 61 CPU-h? (K-N2) | v2 l.956-960. My check: 24 counts in a test half at 9.0 per 2,000 means 5,333 per half, so +8,667 events × 25.2 s = 61 CPU-h. With the same unit cost, tt̄ 1ℓ is ≈ +115 CPU-h and W(τ_ℓ) ≈ +210 CPU-h. | Confirmed. The fixer recomputes the last two. |
| Phase-3 parallelism (N-B6) | `ORCHESTRATOR_STATE.md` l.20: "at most 3 at a time". v2 l.2064: "six parallel channels". | N-B6 stands. |
| M12 depth (N, Part 1 B-7) | v2 l.1037-1038: P_geo and H re-measured on 2×10⁶ events per variation "at every T2 candidate". The nominal floors need 10⁷–10⁸ events. | At T2 candidates the reruns count zero. N is right and K's RESOLVED is too generous. M12 is PARTIALLY. |
| What does v2 say about the D7 reading? (K-N9) | v2 l.1602-1604: samples 7 and 10 exist before the hash as "inputs whose content does not depend on any analysis choice". Brief D7: hashed "before any v2 production sample exists". | It is an executor interpretation of a fixed user decision, and only the user can confirm it. It becomes a Gate-A line. |

---

## 3. Cycle-1 findings M1–M35: final status after cycle 2

Statuses: R = RESOLVED; P = PARTIALLY RESOLVED (what remains); D = DEFERRED TO GATE A (accepted, or not).
Reviewer verdicts are listed as P / K / N where a reviewer gave one.

| # | finding | P / K / N | final | what remains, or the reason |
|---|---|---|---|---|
| M1 | zero counts in the likelihood | R / R / R | **R** | Residual definition issues are new findings N3, N6 and N10. |
| M2 | C1 blinding exception | — / D / — | **D, accepted** | Gate-A question Q1. Also: freeze the full 16-candidate list at Gate A (P-C7), and keep the sealed file outside the agents' tree (K-N14). Both are C items. |
| M3 | same-rung closure | R / R / — | **R** | B5-a uses roads of the same events (K-N21, C). |
| M4 | extrapolation width | P / P / P | **P** | The widths contradict the rule, the distance is still a rung index, and no crossing tests are used. Carried as N5. |
| M5 | testability, NOT TESTED | P / P / R | **P** | The closure samples were not raised and the D4 conflict was not put to the user (N2). The ceiling H is untested (N1). P and K outweigh N, whose item B-12 covered only the "leading" loophole, which is resolved. |
| M6 | floors and central target | R+D / D / P+D | **D, accepted** (pool size and message, Q2) | The redesign is done. Two errors remain and are new findings, not decisions: the "target met" label (N3) and the projection without H or pile-up (N7). |
| M7 | injection, pulls, units | R / R / — | **R** | — |
| M8 | T1-g, toy budget | R / R / R | **R** | T1-h true rates unstated (N6, part). |
| M9 | MET validation | R / R / R | **R** | Execution depends on R-3. The fallback if R-3 is empty is N13, and the ordering is N15. |
| M10 | stop rule | — / R / — | **R** | Envelope against contingency: N12. |
| M11 | variation sizes | P / P / — | **P** | "No source → no nuisance" is optimistic. Carried as N13. |
| M12 | nuisance propagation | — / R / P | **P** (Case 4, §2) | Add the two sentences N asked for: the shift is measured at the deepest rung with counts and carried with s_tot, and for bounded terms the detector nuisances act only through H and the conditionals. |
| M13 | [DP2] point set | R / D / — | **D, accepted** | It goes in the downscope bundle of Q4. |
| M14 | thinning reach | R / R / R | **R** | — |
| M15 | closure statistics | R / P / R (for r = 1) | **P** | The sizes assume s_model = 0, and criterion (a) has no INVESTIGATE route. Carried as N4. I side with K, because N itself raised the same defect as N-B5. |
| M16 | time-tag credit | R / D / R+D | **D, accepted** (default, §4) | Two design gaps (test population; extrapolation in t_cut) are new finding N16. |
| M17 | undeclared signal quantities | — / R / — | **R** | Ordering of A and the MET model: N15. |
| M18 | MVA argument | R (C1) / R / R | **R** | — |
| M19 | costs and schedule | — / R / — | **R** | Phase-3 channel count: N18 (new). |
| M20 | S1 ×10 | — / D / — | **D, accepted as default** (2,000 rows; the user may override) | — |
| M21 | C1 chain per point | — / R / — | **R** | — |
| M22 | attribution rule | — / R / — | **R** | Mixed candidates (topology plus pile-up majority) fall in neither term: N1. |
| M23 | K validations | R / D / — | **D, accepted as default** | — |
| M24 | Herwig attempt; DPs in the paper | — / P / — | **P, the remainder accepted as a dated commitment** | Install attempt in Phase 2, days 0–7, with the stated fallback chain. No further strategy text is needed. |
| M25 | identifiers | — / R / R | **R** | Fix the one COM/v2 mismatch (B4-c "R06" against "R06 (and R07 where evaluable)", K Part 4). |
| M26 | background list | P / R / — | **P** (Case 4, §2) | The premise about v1 is wrong, and the test is blind at depth. Carried as N9. |
| M27 | signal-side detector response | P (acceptable) / R / — | **R** | The design is complete. The retrieval deadlines are under N13, and the ordering is under N15. |
| M28 | infracolour correction | R+D / D / — | **D, accepted as default** (one-sided band) | P-C4 (constant term, scalar P-wave, scale m_Q β) is a C item. |
| M29 | T2 background-side bias | R / R / — | **R** | — |
| M30 | dE/dx forgone gain | R / D / — | **D, accepted as default** | — |
| M31 | B5 dominated by pile-up | — / R / R | **R** | N-C-3 (count the signal road on all 10,000 Z(νν) events) is adopted (§5). |
| M32 | weighted samples | — / R / R | **R** | — |
| M33 | multijets | — / R / R | **R** | — |
| M34 | post-freeze failure | — / R / R | **R** | Name the fresh B3 sample (N-C-10). |
| M35 | sample inventory | — / R / — | **R** | Overlay sourcing: N17. |

**Counts:** R 20, P 7, D 8 (all 8 accepted, either as Gate-A questions or as defaults the user may override).
**Discarded items not reintroduced** (checked by K and by me): ρ = 3, ×100 growth, cloud, Stage 3 at Λ ≥ 15 keV, endcap
(outlook only), pile-up scan, Open Data. F is not loosened. **The fix must keep it that way.**

---

## 4. Structured adjudication table: new findings

Fix type: **(i)** design change; **(ii)** definition or statement to correct; **(iii)** Gate-A human decision.
"Dated commitment" marks items where a strategy cannot settle the outcome before Phase-2 or Phase-3 measurements
exist. For those, the right fix is: what is measured, by when, and what happens for each result. More design now is
not the fix.

| # | finding | source (reviewer ids) | their cat | final | fix type | rationale |
|---|---|---|---|---|---|---|
| **N1** | **The ceiling H is never tested as a ceiling.** P ≤ H is asserted. Three classes are missing: events that fail the width cut without pile-up and pass with it (re-fit, new core); candidates with a topology seed but a pile-up majority, which are in neither B1 nor B2 (B2 is measured on pile-up-only events); events whose f_k is built from finder output rather than hit subsets. Also undefined: k per layer type (N_IT2/N_IP2/N_2S2) and the width for π_k at counting rungs. PV pairs (or their B4 replacement, N8), NI, loopers and most SM processes enter at H, so the expected headline rests on it. | P-A1; K-N6; N-B1 (part iii, leak test) | A, B, B | **A** | (i)+(ii); outcome a dated commitment | Case 2: I side with P. The counts needed to test it exist (PV pairs 24/500 at R02, D4 l.197; DIF, γ, V⁰ to R06–R07). The claim "measured directly, needs no extrapolation" (l.572) is a validation that passes by assertion. That is a regression-check item, so it blocks now. |
| **N2** | **MUST closures are planned to stay NOT TESTED** (B1-a: PV pairs, NI, loopers; B4-c: 11 of 12 processes, including W(τ_h) for 61 CPU-h). Brief D4's conflict is not put to the user. | K-N2; P Part 1 A5; N C-2 / C-9 (context) | A | **A** | (i)+(iii) | Case 3, verified (§2). The brief says D4 "A MUST item gets the statistics its acceptance criterion needs". Per my instructions, NOT TESTED for a MUST criterion is not a default: the fix either supplies the statistics or asks the user, item by item, with costs. |
| **N3** | **"Target met" is earned by zero-count bounds**: σ_ln = 0.41 with every term a bound (sum of about 20 exponentials). σ_ln also has two definitions (sd ln λ = 1.28 against ½ ln(B₈₄/B₁₆) = 1.18 at m = 0). | K-N3; N-A1; P-C1 | A, A, C | **A** | (ii) | Case 1. A pre-declared outcome label that passes by construction in exactly the case it should flag is a tautological validation and a motivated-reasoning red flag. |
| **N4** | **Criterion (a) is inconsistent with (c).** The false-fail and family-wise rates (0.27 %, 7.5–10 %, shown in GA-4) hold only at s_model = 0. At the declared s_model, per test 4–10 %; for K = 12, 41–71 %. Criterion (a) has no INVESTIGATE route. K is a planning value (12); the real family is plausibly larger (K-N22). | K-N1; N-B5; K-N22 | A, B, C | **A** | (i)+(ii) | Case 2: I side with K. The user is asked to decide GA-4 on wrong numbers, and under [SD8] the error changes the expected paper outcome ("closure fails"). This is an error, not a decision. |
| N5 | **Extrapolation widths contradict the strategy's own rule** (σ_b := b₀ for < 3 rungs). R08 widths are understated by ×2.2. d_in/d_out are ambiguous for 1–2 evaluable rungs. The distance counts rung indices even for rungs that do not act on the quantity. b₀ = ln F is a convention, not a measurement. Crossing test rungs (deep-family cuts applied on top of the R05/R06 widths, 10⁴–10⁶ candidates) can replace it for about 5 CPU-h. | P-B3; K-N4; N-B2; N-B3; P-C3 | B, B, B, B, C | **B** | (i)+(ii); Phase-3 evaluability a dated commitment | Case 1, verified (§2). The crossing tests turn an arbitrary width into a measurement, as `CLAUDE.md` "Systematic variation sizing" requires. |
| N6 | **Log-normal widths on probability factors are not capped** at their no-credit value. S, π_k, the conditionals and p_late exceed 1, and a term can exceed H, so a PASS can cost more than NOT TESTED. Also unspecified: the μ grid and CLs interpolation, the true rates in T1-h, and whether T1-h redraws m. | P-B4; K-N5; N-B4 | B, B, B | **B** | (ii) | Case 1. A two-implementer reproducibility gap in a T1 MUST item. |
| N7 | **The headline projection omits N_t·H and the deep pile-up term.** "45 events, 495–662 GeV" is too low if H is empty (≈ 700 GeV) and too high if H counts (m_H = 3 gives ≈ 560 GeV; m_H = 10 gives < 495 GeV). There is no EST of the pile-up term at R09–R14. The bounded paper should be presented as the default deliverable, not as a fallback. | P-B7; N-B1 (i, ii); N C-8, C-9 | B, B, C | **B** | (ii) now, plus a dated commitment (pilot) | Case 1. A strategy cannot know m_H before the pilot. The fix is a stated projection formula, an EST range and a decision rule at decision point 2 (day 15). It does not need more design. |
| N8 | **The prompt hard-vertex tracks are counted twice**: as PV pairs (a gun proxy with minimum-bias pair kinematics) and inside the B4 real SM events. By my check, the same applies to γ, V⁰ and loopers from the hard-scatter vertex. The floor double counts up to 18.5 events, and 7.65×10⁷ pool events (244 CPU-h) go to the proxy. | P-B2; Arb extension (Case 5) | B | **B** | (i) | Verified in the source (§2). It is conservative, but not neutral: it inflates the headline, wastes 40 % of the pool and creates the largest NOT TESTED term. |
| N9 | **Pile-up-vertex secondaries.** The premise misreads v1, which already includes ×200 minimum-bias NI and DIF, at the PV z. The R04–R06 ratio test against a combinatorial rate of 49.7 per trial cannot see a correlated term that leads only from R07 on. Including Geant4 secondaries in the overlays while the B1 rates keep ×200 minimum bias would count twice. | P-B1 | B | **B** | (i)+(ii); magnitude a dated commitment (Phase 3) | Case 3, verified (§2). |
| N10 | **T2 is drawn to the first empty rung, and "estimate" is too weak.** Under Gamma(m + 1), going from m = 2 to m = 0 lowers the predictive mean from 3κ to κ whatever the physics did, and the protections stop T2 only *beyond* the first all-zero rung. "Estimate" at m ≥ 1 (sd ln λ 0.80) does not separate measured from bounded. | P-B5 | B | **B** | (ii)+(i) | Case 3. It is the outcome-label twin of N3: a selection can win because its M is small. Monotone prior: report the sensitivity only (C level). |
| N11 | **π_k treats the missing layers as independent**, although promotion at pile-up 200 is dominated by correlated multi-layer hits. The occupancy model already needs layer-to-layer correlations. | P-B6 | B | **B** | (i); magnitude a dated commitment | Case 3. The design fix (use the occupancy model's correlated multi-layer probabilities) is settleable now. The per-k comparison on derivation overlays is a Phase-3 measurement with a stated rule. |
| N12 | **GA-8 asks for an envelope that the strategy expects to exceed by > 30 %.** The contingency is 1,989 + 403, and conditional draws (overlays 294, secondaries 160, fresh sample 403) come "from the contingency". It is not said whether a contingency draw is a reportable overrun (D6). | K-N7; N C-6 | B, C | **B** | (ii)+(iii) | Case 1. It becomes part of Q4. |
| N13 | **The fallbacks for retrievals that find nothing are not neutral.** "No public number → no nuisance" gives zero width. If R-3 yields nothing, B4-b (MUST) has no model to validate. There are no retrieval deadlines against the freeze. | K-N8; P Part 1 B8 | B, (P) | **B** | (ii); default (§7) | Case 1. JFC forbids round-number inflation (`CLAUDE.md`), so a zero cannot pass silently either. The default is settled in §7. The empty-R-3 branch maps to the brief's stop rule "a MUST item is infeasible after a real attempt". |
| N14 | **The D7 reading**: S1 Stage-2/3 truth samples (47 + 266 CPU-h) exist before the hash, by the executor's own interpretation. | K-N9 | B | **B** | (iii) | Case 3, verified (§2). Only the user can interpret a fixed decision. One line in Gate A. |
| N15 | **A and m_mig need the MET model before it exists.** A and m_mig are formed in Phase 2, but MET_reco is built in Phase 3 from R-3. | K-N10 | B | **B** | (ii) | Case 3. It is an ordering fix in §4.1, §4.13 and §11.3. |
| N16 | **Time-tag closure.** It is tested on pile-up candidates instead of prompt ones, and the credit is extrapolated about two decades in t_cut with no width. | K-N11; N-B7 | B, B | **B** | (i) | Cases 1 and 3. A prompt population exists (Z(νν) hit level, 1.95×10⁵ R04 candidates, and the B1 test overlays), with an evaluable direct check at the nominal window (N's arithmetic). 0 CPU. |
| N17 | **The no-pile-up events behind the derivation and test overlays are neither sized nor costed**, and must be disjoint from the derivation pool. | K-N12 | B | **B** | (ii)+(i) | Case 3. The claim "the script prints every CPU-h" is incomplete without it. |
| N18 | **Phase 3 is staffed with six channels; the cap is three.** 54 channel-days take 18 days, which is +9 days on the critical path. | N-B6 | B | **B** | (ii)+(i) | Case 3, verified (§2). |

**Category C (apply without re-review).**
- From P: C2 (pre-declare a criterion on the ratio of true to quoted median limit, or tie the f₀ rule to the 84 % edge,
  which v2 already does); C4 (Coulomb constant; scalar P-wave; scale m_Q β); C5 (re-allocation M_t ∝ √(N_t/(c_t G_t))
  after the pilot, pre-registered); C6 (no-credit SR-T and SR-G both carry the full term: state it, or merge the
  categories); C7 (freeze the full T2 list at Gate A); C8 (folded into §5); C9 (lepton-veto physics argument, R-13).
- From K: N13 (the T2-e comparison must use the term-dropped value and the analytic limits, because at κ ≲ 3 the
  convention is stronger than a fixed 1.14 κ); N14 (sealed file outside the agents' tree, or encrypted); N15 (order of
  precedence of the labels bound / no-credit); N16 (GA-8 lever sum); N17 (JSON key path); N18 (B1-e against GA-3 (ii):
  biasing always, with the pool split set by the gain); N19 (move the "v1 of this document" diffs to §13); N20 (tag
  the PV-pair R05 entry [E]); N21 (label B5-a as limited by B5-c); N22 is merged into N4 (fix K now from the list).
  Also the conventions check 3 per-nuisance pull reading.
- From N: C-1, C-2, C-3, C-4, C-5, C-11 are ruled in §5. C-6 is in N12. C-7 (four figures; mark the v2 reach directly
  instead of on a σ_ln = 1 curve). C-8 (message bracket and the v1 → v2 change of the bound, 4.4 decades) is in N7.
  C-9 (print the size of R07-direct) is in N7. C-10 (fresh B3 sample).

**Dismissals: none.** Every A and B item of every review is accepted. The mapping is in §8.
**Reviewer-pressure protection.** The fixer's report flags several of these points as contestable (FR §6 items 1, 2,
5, 6, 8). Flagging a weakness is not evidence against it, so all the related findings stand.

---

## 5. Proportion: simplifications, stagings, cuts and additions

The MUST budget rose from 2,950 to 3,968 CPU-h and the calendar to about 58 days. Most of the rise is real
correction: unit costs, the second toy pass and the pool. My rulings are below. Each must appear in a new
`strategy_budget.py` section with its CPU-h and days delta.

**Adopt (they cost no MUST criterion):**
| item | effect | condition |
|---|---|---|
| N C-1: toy parametrisation in f_T for both passes | −191 CPU-h | exact toys at 3–5 points as the check. If the check fails, exact toys are used, and their cost (≤ 191) is a declared conditional draw (N12). T1-i is reworded as "toy-based for every quoted limit". |
| N C-3 (part): count the B5 signal road on all 10,000 Z(νν) hit-level events, with road rotation **inline** in the pool jobs | 0 CPU-h | R06 becomes evaluable. Lever (iii) (−137) touches the SHOULD item B5 and stays a GA-7 option (Q4), not a default. |
| N8 resolution (one route for hard-vertex tracks) | frees up to 244 CPU-h of the pool | the fixer re-runs the √(N/c) allocation. The freed CPU stays in the pool (floor falls), not a cut. |
| N C-5: draft `PREREG_v2.md` during Phase 3; draft note sections 1–6 and 8–10 during the 4a production | about −5 days | — |
| N C-4 / P-C8: stage the pool beyond 600 CPU-h and the enriched overlay campaigns on the pilot, by a **pre-declared redirection rule** at decision point 2 | 0 by default | the rule is written now (see N7, N2) |
| N C-2: overlays only for topologies whose test is evaluable | up to −105 CPU-h | **only** for terms that the user accepts at H under Q3. The 1,000 unbiased full-pile-up events per topology stay, because they serve the N1 ceiling test. |

**Not adopted.** N C-11 (composition variation only after R-17): under the N13 default the robustness shift is
reported beside the limit, so the 26 CPU-h stay.

**Required additions:**
| item | cost | why |
|---|---|---|
| N1 ceiling and completeness (leak) tests | ≈ 0 CPU-h | They run on the planned unbiased test overlays, C′_PU and SM hit-level samples. They are re-analysis. The fixer states any extra. |
| N_t·H measured before the freeze for the largest term (PV pairs or the B4 replacement): pilot enlarged from 10⁶ to 10⁷ events | +29 CPU-h | Uses idle pre-freeze capacity, so no calendar effect. |
| B4-c W(τ_h) to an evaluable test half | +61 CPU-h | D4. It is the second-largest SM floor. tt̄ 1ℓ (≈ +115) and W(τ_ℓ) (≈ +210) are either supplied or listed in Q3. |
| N5 crossing test rungs | ≈ 5 CPU-h, plus a storage check | Keep the fit-probability, 2S and shape variables of the R05–R06 candidates in the trial records. |
| N9 truth-attributed secondaries test at R04–R07 | inside the 17.5 CPU-h sample, or the fixer states the extra | — |
| N16 prompt-population time-tag closure | 0 CPU-h | — |
| N17 overlay source | either a disjoint seed-stream slice of the pool (0 CPU-h, with the correlation statement) or a costed scan line | — |

**Indicative net effect [E, mine; the fixer recomputes]:** −191 + 29 + 61 + 5 ≈ **−96 CPU-h** before the Q3 options.
The calendar moves by −5 days (C-5) against 0 to +9 days (N18). The fixer presents the net change. The calendar stays
a Gate-A matter (Q4). It is not an escalation, because the brief has no hard deadline.

---

## 6. Work list for the fixer (priority order)

General rules:
- Write a new version `STRATEGY_<fixer>_<timestamp>.md`.
- Trace every change to an N or M number.
- Update `strategy_budget.py` for every number and add a per-fix delta table.
- Update the COM rows that change.
- Do not reopen brief §3, introduce ρ ≥ 3 or ×100 growth, or loosen any F.
- Correct the numbers in GA-4 and §0 wherever they changed.
- Keep §12.1 to the final list in §7: at most 3 pages, one line per question.
- Shorten the document where possible: move the v1 diffs to §13 (K-N19).
- Brief §4 lists statistics and likelihood design as a "go up" task. The orchestrator should run the fix of N3, N4,
  N6 and N10 at higher effort.

### (i) Design changes

1. **N1, the ceiling H** (§4.4 point 4, B1-f, §4.0 point 6, §4.12; COM B1-f, B4-c).
   - (a) Define f_k on subsets of the topology's own hits (or with the finder run on the width cut only), not on the
     finder's single no-pile-up candidate.
   - (b) Define k per layer type, and the width used for π_k at counting rungs.
   - (c) Add a one-sided **ceiling test**: direct attributed count ≤ H at a stated confidence, at every rung with
     attributed counts. That is R02–R04 for PV pairs, and R06–R07 for DIF, γ and V⁰, on the disjoint test overlays and
     the 1,000 unbiased events. Its FAIL means that H cannot be the no-credit value, and the term is not eligible.
   - (d) Add a **completeness (leak) test**: the attributed passers whose no-pile-up event is in no enumerated class,
     and the sum rule of total direct counts in topology-plus-pile-up events against the B2 rate plus Σ attributed
     terms, at R04–R06. The residual measures the mixed class. Pre-declare the bound.
   - (e) FAIL logic: an over-predicting estimator leaves H valid; direct > H invalidates H.
   - The outcome is a dated Phase-3 commitment, with the result fixed before the freeze.
2. **N2, MUST closures expected NOT TESTED** (Table 4.4b, B4-c, [L1], GA-4).
   - Supply W(τ_h) (+61 CPU-h).
   - For every other MUST criterion still expected NOT TESTED after N8 and the pilot, make a table: term, criterion,
     cost of compliance (statistics to reach N ≥ 24 in the test half, or an enrichment target), and the consequence of
     entering at H under the N1 ceiling test. That table is Gate-A question Q3.
   - For PV pairs, or for whatever term replaces them after N8, write the **dated decision rule** at decision point 2
     (day 15):
     - pilot enrichment ≥ 10²: the test overlays are sized for N ≥ 24 at R06;
     - 10 to 10²: overlay CPU moves from the untested topologies to this term;
     - < 10: the term is NOT TESTED and enters at H, subject to Q3.
   - Offer the rung-split alternative K proposed (derive at R04 only, test at R05).
3. **N8, one route per particle origin** (§2, §4.4, §4.7, Table 4.4a).
   - Declare, for prompt hard-vertex tracks and for γ, V⁰ and loopers from the hard-scatter vertex, which term counts
     them. Recommended: B4 on real events. PV pairs are then dropped, or defined as the remainder after B4
     attribution.
   - Show disjointness by truth origin of the hits.
   - Re-run the allocation and the floor table, and update §0, GA-3 and [L13].
4. **N5, widths** (§4.0 point 7, §4.5, §4.12 distances, script [12], GA-4).
   - Correct the substitution and the script to the stated rule.
   - Define d_in, d_out and b̂ for 1–2 evaluable rungs.
   - Define crossing test rungs per estimator (B2 occupancy, B1 promotion, B3 conditionals), with the same
     evaluable-rung rule and verdict classes.
   - Keep b₀ only where no crossing test is evaluable, and say in the paper that b₀ is a convention.
   - Define the distance per extrapolated quantity: only rungs that change a cut the quantity depends on.
   - Recompute the widths the user sees in §0 and GA-4.
   - Whether the crossing tests are evaluable is a dated Phase-3 commitment.
5. **N9, pile-up-vertex secondaries** (Table 2.1 l.147, §2, B1-g).
   - Correct the premise: v1 includes ×200 minimum-bias NI and DIF, placed at the PV.
   - State whether v2's rate_t includes them, and place them at their own z (or show that the PV placement is
     conservative).
   - Replace the ratio test with truth-attributed counting of secondary-induced candidates at R04–R07, extrapolated
     with the B1 estimator.
   - State a rule that counts each secondary once.
6. **N11, π_k from correlated multi-layer probabilities** (the occupancy model).
   - Write a per-k comparison on the derivation overlays now, with a rule for a mismatch (a wider s_model, or the
     term at H).
7. **N16, time tag** (§4.6 B3-c).
   - The test population is the prompt, truth-attributed candidates.
   - Add a nominal-window direct check on the prompt candidates.
   - Add a width that grows with the distance in ln p_late from the deepest tested edge, or limit the credit to that
     edge.
8. **N17, overlay sourcing.**
   - Size the no-pile-up scan per topology as a formula with a planning value, or take it from the pool by seed
     stream, with the correlation statement.
   - Put its CPU-h in script [3] and its row in §4.17.
9. **N18, Phase 3.**
   - Three critical channels (B1 + B3; B2; T1 + T2 + B4), with the B5 and B6 prototypes and the BDT recipe moved into
     the production window, or state Phase 3 at 14–18 days.
   - Restate decision point 2. Apply C-5.

### (ii) Definitions and statements to correct

10. **N4** (§4.0 points 3–5, GA-4, the partial-outcome matrix, script [11]).
    - Make (a) consistent with (c), either by capping s_model so that (a) has a stated size at the estimator's own
      s_model, or by defining (a) on the statistical part (|ln r| ≤ ln F + k σ_stat).
    - Give (a) the INVESTIGATE / one-fresh-re-test route of (b) for violations below 2σ_tot.
    - Fix K now from the actual eligibility list.
    - Recompute, in the script, the per-test size, the power at |ln r| = 0.5 ln F and ln F, and the family-wise rate
      at the planned s_model values, and put them into GA-4.
    - F is not loosened.
11. **N3** (§4.11 point 3, COM TG-1, GA-3, §0).
    - "Target met" requires σ_ln ≤ 1, **and** f₀ ≤ 0.5, **and** no leading term that is a bound or no-credit.
      Otherwise the label is "width small, background bounded (f₀ = …)".
    - Give one σ_ln definition, and rename the other.
    - State now that the expected outcome reads "target not met: sample-size limited".
12. **N10** (§4.11 point 3, §4.12).
    - "Estimate" requires sd(ln λ) ≤ 0.5 (m ≥ 4) and a PASS for every estimator used.
    - Report, beside the T2 winner, the best selection whose leading terms are all estimates, with its G and reach.
    - Declare in GA-3 which of the two the abstract headlines (default: the winner, with the estimate-only selection
      beside it).
    - Report the winner's sensitivity to a monotone prior.
13. **N6** (§4.11 point 1, T1-c, T1-h).
    - Every probability factor is truncated at its no-credit value: min(φ, 1), and the term at min(term, H), in every
      pseudo-experiment.
    - Test the effect on coverage in T1-c.
    - State the μ grid and CLs interpolation.
    - State T1-h's true λ values and whether m is redrawn.
14. **N7** (§0, §4.4 readings, [L13], GA-3, decision point 2).
    - The projection is max(zero-count floor, N_t·H) for every term expected at H, plus an EST pile-up B₅₀/B₈₄ at R09,
      R11 and R14 (labelled, from v1 occupancy-type numbers or development samples).
    - Correct the reach range, and correct the one-bin 28 against the summed predictive 24.
    - Present the bounded paper as the **default deliverable**, with the C-8 bracket and the 4.4-decade change of the
      bound, and print the size of R07-direct.
    - Decision point 2 computes N_t·H at the T2 candidates from the pilot.
15. **N13** (§4.9, COM B6-d, §4.7, §6.4).
    - Apply the default of §7.
    - Define the B4-b path if R-3 yields no parameters: attempt a second source, then declare B4-b infeasible after a
      real attempt, which is the brief §7 stop-and-ask.
    - Set deadlines: R-3, R-7 and R-15…R-18 by decision point 2 (day 15), R-12 and R-14 before the freeze.
16. **N15**: an ordered list R-3 → MET model → A and m_mig → generator-cut decision, placed in the calendar before the
    freeze, with A computed once.
17. **N12** (GA-8, §11.2, §11.6): for each conditional cost, state whether it is inside the approved figure. State that
    a contingency draw is a reported overrun under D6. The envelope choice goes into Q4.
18. **M12 residual**: the two sentences of §3.
19. **M25 residual**: COM B4-c wording.
20. **The C items** of §4.

### (iii) Gate A

21. Replace §12.1 with the list in §7: five questions, one line each with a default and the cost, followed by the
    defaults list. Present the N2 table as the annex to Q3. Total length three pages or less.

**Items where reviewers ask for more than a strategy can settle** (the fix is the dated commitment written in the item,
not more design now):
- N1 outcome (H against direct counts): Phase 3, before the freeze.
- N2 / N7: the PV-pair enrichment and N_t·H come from the pilot at days 0–7, with the rule applied at day 15.
- N5: whether the crossing tests are evaluable is known in Phase 3.
- N9: the magnitude of the secondaries is known in Phase 3.
- N11: the per-k π_k comparison is done in Phase 3.
- N13: the retrieval outcomes are known by day 15.
- The s_model values come from the development samples, and the N4 cap rule decides what follows.
- P-C4: the Coulomb constant comes from R-12.
- P-B5 (iv): monotone prior, a sensitivity report only.

Cycle 3 should verify that each rule is written and costed. It must not ask for these outcomes.

---

## 7. Gate A: final list (decided here; the human package is three pages or less)

I adjudicated N's proposal of five decisions plus five defaults. I accept it with three changes:
- The D4 exception (N2) is added as a real question. It absorbs the user-level part of GA-4, because "NOT TESTED
  enters at H" and "D4 exception for that criterion" are one choice.
- The D7 reading (N14) is added.
- GA-2 becomes a default, and GA-7 and GA-8 are merged into one budget question.

**Questions for the human (one line each; ● = recommended default):**
- **Q1 (GA-1, C1 blinding exception).** May the C1 reproduction compare six v1 signal counts that are also v2
  candidate efficiencies, sealed and reported only as PASS/FAIL until Gate B (four open)? ● Yes, sealed. Other
  options: all ten open and disclosed, or the six dropped. 14 CPU-h in every option.
- **Q2 (GA-3, message and pool).** The expected paper is a background *bounded* by simulation statistics at the level
  of the corrected projection (N7). Is that the default deliverable? ● Yes, with the 600 CPU-h pool raised by the
  freed CPU (N8, C-1) and staged by the day-15 rule, and production proceeding without a pause unless the pilot
  changes the outcome class. Alternative: pause at day 15 for the user.
- **Q3 (new, brief D4 exception, with the N2 table as annex).** For the listed MUST closure criteria that remain
  untestable at the planned statistics, may the term enter at its ceiling H (ceiling test passed; selection eligible,
  flagged), or do you order the stated compliance CPU per term? ● Entry at H for the listed terms; W(τ_h) supplied
  (+61 CPU-h).
- **Q4 (GA-7 + GA-8, budget, calendar, stop rule).** Approve the corrected total (CPU-h) and calendar (days, against
  your 2–4 weeks) with [DP1], [DP2], [DP4] and [DP5]? ● Approve. The contingency is listed but not pre-approved: if
  measured costs project above 1.3× at checkpoint 1 (day 7), you are asked again. Alternative: pre-approve the
  contingency as the envelope.
- **Q5 (new, brief D7 reading).** May the truth-level S1 Stage-2/3 signal samples, which no analysis choice
  influences, exist before the pre-registration hash? ● Yes. Alternative: produce them after the freeze (about
  +1.8 days).

**Defaults the human can override (reported, not asked):**
- GA-2: 2,000 signal rows per point (4,000 = +827 CPU-h, +4.7 days).
- GA-4, technical: F = 1.5 and 2 unchanged; the N4-corrected criteria and family-wise rule; crossing tests, then the
  coherent ln F × d convention where no crossing test is evaluable.
- GA-5: σ_NLO nominal with the resummed cross-check beside every limit; the infracolour correction as a one-sided band.
- GA-6: dE/dx excluded; the forgone gain is measured (2 CPU-h).
- GA-9: time-tag credit only if its prompt-population closure passes and the tails are sourced.
- GA-10: endcap wording as fixed by brief D1 (FYI).
- N13, no-source policy: a variation with no public size gets no nuisance (JFC sizing rule). Its robustness-test
  shift of μ₉₅ is reported beside the headline limit, and is named in the abstract-level limitations if above 10 %.
  An empty R-3 triggers the brief's "MUST infeasible after a real attempt" stop-and-ask.
- Toys: the f_T parametrisation with an exact-toy check (C-1).

---

## 8. Mapping of reviewer items to merged findings (every new A and B)

| reviewer item | merged | | reviewer item | merged | | reviewer item | merged |
|---|---|---|---|---|---|---|---|
| P-A1 | N1 | | K-N1 (A) | N4 | | N-A1 | N3 |
| P-B1 | N9 | | K-N2 (A) | N2 | | N-B1 | N7 (+ N1 iii) |
| P-B2 | N8 | | K-N3 (A) | N3 | | N-B2 | N5 |
| P-B3 | N5 | | K-N4 | N5 | | N-B3 | N5 |
| P-B4 | N6 | | K-N5 | N6 | | N-B4 | N6 |
| P-B5 | N10 | | K-N6 | N1 | | N-B5 | N4 |
| P-B6 | N11 | | K-N7 | N12 | | N-B6 | N18 |
| P-B7 | N7 | | K-N8 | N13 | | N-B7 | N16 |
| | | | K-N9 | N14 | | | |
| | | | K-N10 | N15 | | | |
| | | | K-N11 | N16 | | | |
| | | | K-N12 | N17 | | | |

C items folded into A/B findings: P-C1 → N3; P-C3 → N5; K-N22 → N4; N C-6 → N12; N C-8 and C-9 → N7; N C-2 → §5 and
N2. Arbiter (Case 5): the γ, V⁰ and looper overlap → N8.

---

## 9. Regression and motivated-reasoning checks

**Regression triggers (§6.7).** Phase 1 has no results, so validation failures, the > 80 % systematic, GoF and bin
exclusion do not apply. **Tautological or pass-by-construction validations in planned criteria: yes, three.**
- The "target met" label (N3).
- The ceiling H asserted rather than tested (N1).
- The false-fail sizes computed for a perfect estimator and presented to the user (N4).

There is no earlier phase to regress to. All three are fixed in this iteration.

**Motivated reasoning.** v2 is honest where it matters most: §0 says plainly that "estimated, not bounded" is unlikely.
But every remaining error leans favourable:
- smaller widths (N5);
- uncapped credits (N6);
- a projection without H (N7);
- an outcome label that passes (N3);
- lower false-fail rates (N4);
- a D4 conflict resolved by default rather than by the user (N2).

The fixer flagged several of these as contestable. That is to its credit, but it is not a fix. "Will be addressed
later" appears only where a measurement must come first, and each such item now carries a decision rule (§6).

**Competing group.** A competing group would have the leading backgrounds tested, not only bounded. The cheap steps
toward that (W(τ_h) for 61 CPU-h, the PV-pair overlap fix, the ceiling test, the crossing tests) are now required or
put to the user.

**Brief compliance.** Brief D4 (N2) and D7 (N14) are brought to the user. Brief §7 stop rules are quoted correctly. No
D8 item is reintroduced. No cloud, endcap or Open Data. The cajuela projection is 410–610 GB, against 2.0 TB.

**Iteration.** This is cycle 2 of the 4-bot cap (the protocol warns at 3). Every finding above is either a
text or rule change or one of the costed additions of §5. If the fixer addresses §6 items 1–21 as written, cycle 3 is a
verification pass.

---

## 10. Verdict

**ITERATE.** These Category A items block: **N1, N2, N3, N4.** All 14 B items (N5–N18) and the residuals of the seven
PARTIALLY RESOLVED cycle-1 findings (M4 → N5, M5 → N1/N2, M11 → N13, M12 → §3, M15 → N4, M26 → N9; M24 is accepted as
a dated commitment) must also be fixed before PASS. The fixer works from §6 in priority order, shows each budget
effect via `strategy_budget.py`, and rewrites §12.1 to the list of §7. The re-review is a numbered artifact with a
fresh reviewer added to the panel (06 §6.5). This is cycle 2.
