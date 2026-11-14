# Arbiter verdict: Phase 1 STRATEGY v3 (quirks v2), review cycle 3

Arbiter: Felix, 2026-11-13 22:40. I am fresh to this panel and arbitrated neither earlier cycle. I followed the
Prompt Template of `agents/arbiter.md` in full: adjudication cases 1–5, the structured table, the dismissal rules
(§6.5.1), the regression check (§6.7), the motivated-reasoning check and reviewer-pressure protection.

**Artifact.** `phase1_strategy/outputs/STRATEGY_emeric_2026-11-13_21-10.md` ("v3", 2,674 lines), `COMMITMENTS.md`
("COM"), `phase1_strategy/src/strategy_budget.py` ("script") and `outputs/FIX_REPORT_cycle2_emeric.md` ("FR").

**Earlier verdicts.** Cycle 1: Dagmar (M1–M35). Cycle 2: Eloise (N1–N18; Gate-A list Q1–Q5 plus 8 defaults).

**Cycle-3 reviews** (all dated 2026-11-13 22:00):
| reviewer | role | A | B | C | ids used below |
|---|---|---|---|---|---|
| Estelle | physics | 0 | 6 | 9 | Ph-B1…B6, Ph-C1…C9 |
| Fabian | critical | 0 | 7 | 13 | K-F1…F7, K-C1…C13 |
| Fabiola | constructive | 1 | 6 | 12 | N-A1, N-B1…B6, N-C1…C12, S-1…S-3 |

There is no plot validator, because Phase 1 has no figures.

**What I read.**
- In full: `agents/arbiter.md`, `AGENT_RULES.md`, the study and phase `CLAUDE.md`, `FRAMING.md`, the cycle-2 verdict,
  the three cycle-3 reviews.
- In part: methodology `06-review.md` §6.5–6.5.1, brief `prompt.md` §3 and l.254–270, and the FR header and §2.
- My own reading of v3: l.1–130, 140–870, 1055–1205, 1380–1530, 1773–1790 and 2195–2564.
- I also read the pool and allocation code of the script (l.55–100, 385–395).

**My own arithmetic.** Standard-library `python3 -I`, run in the scratchpad and logged in the session log. It covers:
- the floor with Z(ττ) and lost-lepton Z added to the pool;
- the T1 binomial family rates;
- the ceiling-test family rates;
- the π_k width for a term tested at R06 only;
- the extrapolation of v1's R07 decay-in-flight count;
- the reserve-inclusive threshold.

**Rules followed.** No sub-agents and no git commands were used.

**Verdict: ITERATE.**
- **One Category A item (P1)** and **15 Category B items (P2–P16)** are new.
- Of the seven cycle-1 items still partial after cycle 2, 5 are now RESOLVED and 2 PARTIALLY RESOLVED (M4 and M5, both
  carried into P-findings).
- Of N1–N18, 12 are RESOLVED and 6 PARTIALLY RESOLVED (N1, N2, N5, N7, N14, N18), all carried into P-findings.

Nothing needs the user beyond the normal Gate-A decisions, so the verdict is not ESCALATE. Every fix is text, table
or script work. About 40 CPU-h are added, and the 156 CPU-h reserve moves inside the approved figure.

---

## 1. Overall assessment

v3 is a sound and largely correct answer to the cycle-2 work list. All three reviewers reproduced, independently and
with their own code, the following:
- the budget (3,945 / 4,378 / 4,891 CPU-h);
- the 11.7-event floor, term by term;
- every width of §4.0 point 7;
- the size and power of the closure rule at the cap;
- the censored means;
- the B4 sample sizes;
- the reach mapping.

The critical reviewer's stale-value grep is clean. No discarded item has come back: ρ ≥ 3, ×100 growth, cloud,
Λ ≥ 15 keV, endcap and Open Data are all still out, and F is unchanged. The one-route accounting (N8) is physically
right, and the honest label "target not met: sample-size limited" is in place.

What remains has the same shape as in the last two cycles, but it is smaller and almost entirely about **what the user
is shown**:
1. The headline. It leaves out two B4 terms that, as planned, have no no-pile-up sample at all (P1, the A item). It
   leads with the empty-ceiling edge, against v3's own quoting rule and against v1's non-zero R06–R07 counts for decays
   in flight and conversions (P2).
2. The ceiling H, now load-bearing. Its CKF treatment is undefined (P3). Some of its tests pass by construction (P4,
   and P7 for the crossing credit). Its completeness numerator is ill-posed (P5). Its false-fail rate is outside the
   rate quoted to the user (P6).
3. Several rates, widths and premises the user reads are right for a subset only: P8–P13.
4. Executability: inputs of the day-15 rules without a sample, the B1 trace, and the agent cap (P14–P16).

**Trend.** 11 A → 4 A → 1 A, with the numbers reproduced every time. No finding calls for a redesign. I judge that the
fixes below are mechanical enough for cycle 4 to be a pure verification (§9).

---

## 2. Facts settled from sources

| question | evidence (opened by me) | ruling |
|---|---|---|
| Do Z(ττ) and lost-lepton Z(ℓℓ) have a no-pile-up sample? (N-A1) | §4.7 point 3 (l.1068–1074) promises P_geo, f_k and H "on no-pile-up hard-scatter events of each process". The same lines give the pool as "3.6×10⁷ events over the twelve processes". Script l.69–81: `SM_NTRIG` has the 12 old processes only, and `terms` is built from it. Cost line l.1146–1148: hit level "eleven new processes × 2,000"; the multijets alone get a 10⁶-event loose population (12.5 CPU-h). Table 4.4a l.766: "not in the table". | **No.** Beyond the hit-level reach their term is a direct bound, N_t × 1.14/2,000. My recomputation: 57 / 228 / 741 events at N_trig = 10⁵ / 4×10⁵ / 1.3×10⁶ (Z(ττ)), and 6–57 for lost-lepton Z. N-A1 is correct. |
| Cost of putting them in the pool | My allocation code (same rule M_t ∝ √(N_t/c_t), 45 ms per event) | Re-split inside the 665 CPU-h: the summed floor rises from 11.7 to 12.1–13.2 events. Z(ττ) takes 9–31 CPU-h, with a floor of 0.16–0.61. Keeping 11.7 instead needs 689–750 CPU-h, i.e. +24–85 CPU-h. |
| Does v1 count decays in flight and conversions at R06–R07 with pile-up? (Ph-B1) | Table 2.1 l.145–147; Table 4.4b l.838–840 (DIF 166/81/2/1, γ 153/86/13/2 per 500). Projection l.804–805: "DIF 1.3×10⁵ at v1's 1 attributed count in 500". | **Yes, non-zero counts.** DIF at R07 is N_t/500 = 1.30×10⁵ events. With the pile-up fall per width step (×201–339, l.794) this gives 380–650 at R08 (mine; the physics reviewer gives 440–750). An untested conditional is 1 (l.673–675), so R09 equals R08 for an uncredited term. Table 4.4c keeps DIF at its floor of 2.9 in every row. Ph-B1 stands. Its caveats (v1 placed every vertex at the PV; the attribution rule is not yet transcribed) are real, and they are reasons to label the row EST, not to omit it. |
| Is π_k "tested at R06–R07" the expected case? (K-F4) | l.432 against l.838 (DIF at R07 only if the enrichment is ≥ 4) and l.1131–1133 (B4-c at R06, "R07 where evaluable"). My formula: n = 1, b̂ = 0, σ_b = b₀ = ln 2, s_model 0.231, d_in = 2 | s_tot is **1.41** at R08–R11 and 2.51 at R14 (1.42 with a 2S crossing PASS), against 0.73 / 2.20 / 0.77 in the table. K-F4 is correct. The physics reviewer called c2-B3 RESOLVED because the table follows the rule *for the row as labelled*. Both are right: the row is computed correctly but is the wrong planning row (Case 4). |
| T1 coverage family size (K-F5) | l.1467–1471 (≥ 0.93 of 500, 4 λ × 2 points); l.1497–1502 (T1-h, 2 points); l.1424–1429 (analytic coverage 0.945 at κ = 1, λ = 0.5); l.1505 (FAIL blocks every quoted limit). Binomial: | P(< 465 of 500) = 0.0196 at a true coverage of 0.95, 0.063 at 0.945 and 0.150 at 0.94. Family of 8 / 10: 14.7 / 18.0 % at 0.95, 40 / 48 % at 0.945. K-F5 is correct. |
| Ceiling-test family (Ph-B6, K-F2) | l.676–685: "at every rung with attributed direct counts", the size 0.35 % at the boundary, no family rule. K = 10 (l.339–341) excludes these tests. | 1 − 0.9965ⁿ = 5.5 / 10.0 / 17.5 % for n = 16 / 30 / 55. Both reviewers are correct. |
| The 156 CPU-h (K-F7, N-C1) | Q2 l.2476 ("spent at day 15"); §11.2 l.2272 ("None of these is inside the approved figure") against l.2277 ("approved in advance, with Q2"); Q4 l.2489 (4,378; threshold 5,691) | **Contradiction confirmed.** The default plan spends 4,534 CPU-h, and 1.3 × 4,534 = 5,894. |
| Q5 premise (K-F6) | Q5 l.2498 ("which no analysis choice influences") against §4.1 l.567–571: A, the MET threshold and the generator cut are decided before the propagation of the accepted events | **Premise inaccurate.** These choices are pre-registered and selection-independent, but they are analysis choices. |
| Phase-3 slots (N-B6) | l.2204 (at most three agents); l.2310 (three channels, plus "1-bot review per channel" and `PREREG_v2.md` "drafted alongside"); l.540–541 (a dedicated sealed-comparison agent in Phase 2, next to three agents) | **The cap is exceeded** in both phases as written. |
| Does the brief fix P1 in Phase 2? (bears on S-3) | `prompt.md` l.264–265: "Phase 2 … P1 tests" | **Yes.** Moving P1 into the production window would contradict the brief's phase list. That part of S-3 is not adopted (§7). |
| CKF in H (Ph-B2) | l.99 (CKF removes helical tracks before the finder); l.115 (fixed cut f_CKF < 0.2); l.656–675 (classification "on subsets of the term's own hits", with no statement on CKF; "complete … whatever the finder chose") | **The definition is missing.** The subset argument holds only for cuts that are monotone under added hits; CKF removal and f_CKF are not. Ph-B2 stands. |

---

## 3. Earlier findings: final status after cycle 3

Statuses: R = RESOLVED, P = PARTIALLY RESOLVED (carried into the named P-finding), GA = at Gate A.

### 3a. The seven cycle-1 items left partial after cycle 2

| # | Ph / K / N | final | reason |
|---|---|---|---|
| M4 extrapolation width | P / P / R | **P → P7, P8** | The rule is now applied as written; all reviewers reproduce the table. Two things remain: the π_k planning row is the wrong case (K-F4, verified §2), and the crossing-test credit in the fit-probability and shape families is earned by a consistency check (Ph-B5). Case 4: N's "RESOLVED" covers the arithmetic, not these two points. |
| M5 testability / NOT TESTED | — / P / — | **P → P4, P10** | Q3 omits NOT TESTED routes that v3 itself creates (K-F1). The ceiling test on the sub-topologies is undefined (K-F3). |
| M11 variation sizes | R (Df-7) / R / — | **R** | Df-7 applies the cycle-2 default word for word. |
| M12 nuisance propagation | — / R / R | **R** | Both sentences are present (l.1233–1237). |
| M15 closure statistics | — / R / R | **R** | The rates are reproduced by all three reviewers. The ceiling family is a new item (P6), not this residual. |
| M24 Herwig attempt | — / R / — | **R** | A dated commitment (l.2366–2373). |
| M26 background list | R / R / — | **R** | The premise is corrected from `normalise.py`. Ph-C7 (count the multi-vertex class per rung) is a C item. |

The M25 residual is also R (COM B4-c wording).

### 3b. N1–N18

| # | Ph / K / N | final | reason |
|---|---|---|---|
| N1 ceiling H | P / P / — | **P → P3, P4, P5, P6** | Points (a)–(e) are written. Still missing: the CKF definition, tests that cannot fail on enriched samples, an ill-posed mixed count, and no family rule. |
| N2 MUST NOT TESTED / D4 | — / P / — | **P → P10** | W(τ_h), W(τ_ℓ) and tt̄ 1ℓ are supplied, and NI uses a rung split. Q3 is incomplete (K-F1). |
| N3 "target met" by bounds | R (C4) / R / R | **R** | Implemented as ruled. The neighbouring low-count hole is new finding P9. |
| N4 (a) against (c); rates | R / R / R | **R** | The ceiling-test family is new finding P6. |
| N5 widths | R / P / R | **P → P8** | Case 4, settled in §2. |
| N6 censoring, T1 gaps | R / R / R | **R** | — |
| N7 projection | P / R (C3) / P | **P → P1, P2** | Case 2. I side with Ph and N: the projection omits terms (P1) and leads with the optimistic edge (P2). K's C3 is the same defect seen from the Z-only rows. |
| N8 one route per origin | R / R / R | **R** | The floor of 11.72 is reproduced three times. |
| N9 secondaries | R / R / — | **R** | — |
| N10 "estimate" | R / R / — | **R** | — |
| N11 π_k correlations | R / R (C4) / — | **R** | The sample naming for the per-k comparison is carried as P15 (N-B5 (i), K-C4). |
| N12 envelope | — / R / — | **R** | The new reserve inconsistency is P13. |
| N13 retrieval fallbacks | R / R / — | **R** | — |
| N14 D7 reading | — / GA / — | **P → P12** | Posed at Gate A, but on an inaccurate premise. |
| N15 order of A | — / R / — | **R** | — |
| N16 time tag | — / R / R | **R** | — |
| N17 overlay sourcing | — / R / — | **R** | — |
| N18 Phase-3 staffing | — / R / P | **P → P16** | Case 3, verified (§2). The cap is exceeded by reviews, the drafter and the sealed-comparison agent. |

**Counts.**
- The seven M items: 5 R, 2 P.
- N1–N18: 12 R, 6 P.
- Every P has a successor P-finding below.

**The fixer's departures from the cycle-2 ruling are accepted.** The critical reviewer reproduced each one from its
source:
- +65 / +40 / +153 CPU-h, against +61 / +210 / +115;
- −156, against −191 CPU-h;
- 2.3×10⁶ pilot events, against 10⁷;
- checkpoint 1 at day 5, against day 7.

---

## 4. Structured adjudication table: new findings (cycle 3)

Fix type:
- **(T)** text or table;
- **(S)** a number recomputed in `strategy_budget.py`;
- **(G)** a Gate-A line;
- **(R)** a dated decision rule (the outcome is a Phase-2/3 measurement; the rule, not the outcome, is the fix now).

| # | finding | source | their cat | final | type | rationale |
|---|---|---|---|---|---|---|
| **P1** | **Z(ττ) and lost-lepton Z(ℓℓ) have no no-pile-up pool share.** §4.7 point 3 promises one. Without it their term is a 2,000-event direct bound of 57–740 events, larger than the whole projection shown in §0 and Q2. Rule 1 of §11.7 recomputes "Table 4.4c", which does not contain them. | N-A1; Ph Part 2 check 1 (the additions, and multijets, are absent from the headline); K: Q3 annex row "no N_trig" | A, (B), — | **A** | S+T | Case 3, verified from the script and the text (§2). This is a design inconsistency that an executor would hit at day 12, and it sits under the headline the user decides Q2 on. That meets "framing that hides a problem". The physics reviewer flagged the omission from the headline but not the missing sample. I confirm A. |
| **P2** | **The headline leads with the optimistic edge and omits the terms expected at H.** (a) §0 and Q2 lead with "≈ 790 GeV if every ceiling is empty", although v3 says m_H = 0 "is not the expectation" (l.801–802) and quotes the 84 % edge first when f₀ > 0.5 (l.1399–1401). (b) DIF and hard-scatter conversions sit at their zero-count floors in every row, against v1's own non-zero R06–R07 counts; by v3's own extrapolation rule they reach O(10²–10³) events at R08–R09. (c) Only the Z(νν) ceiling is varied; Z(νν) is the term v3 expects to *test*, and the eight proxied processes and the additions, expected at H, are not projected. (d) The multijet floor has no planning range. (e) The day-15 pause (B₅₀ > 300) is presented as an exception. | Ph-B1; N-B1; N-B2; K-C3; Ph-C6; N-C3, C5, C7 | B, B, B, C… | **B** | S+T+G | Cases 1 and 3. Verified (§2: DIF at R07 is 1.3×10⁵ events; a pile-up-like fall gives 380–650 at R08; the R09 value equals R08 without credit). I keep B and not A because v3 does label m_H as unknown and does carry a day-15 rule, but this is the top B item. |
| P3 | **H is undefined with respect to CKF removal and f_CKF**, which are not monotone under added hits. The "complete by construction" sentence is too strong. Either choice changes m_H by large factors. | Ph-B2 | B | **B** | T (+ a technical default) | Case 3, verified (§2). A definition, not a measurement: it must exist before the pilot measures m_H. |
| P4 | **The ceiling and completeness tests have the wrong or unnamed samples.** (i) On the enriched DIF test overlays (drawn only from passing and near-pass events) the ceiling and leak tests pass by construction. (ii) The leak count is zero for any correct implementation of the attribution rule: it is a code check. (iii) The sub-topology ceiling test (γ, V⁰, prompt pairs) has no H sample; the comparison is paired, not two independent Poisson counts, and no term is charged with a FAIL. (iv) The development ceiling and completeness tests have no named sample. (v) The ceiling test on weighted overlays needs the effective-count form. | Ph-B3; K-F3; N-B5 (ii), (iv) | B, B, B | **B** | T (+7 CPU-h) | Case 1. These are tautological validations (a regression-check item, §8). |
| P5 | **The mixed numerator is ill-posed.** "Mixed" counts any pile-up candidate that picked up one term layer, with no pile-up-only baseline. At R06 a 7 % pick-up already gives mixed/attributed > 1 for hard-scatter terms, so a FAIL is likely. What an untested term enters at after a completeness FAIL is undefined. | Ph-B4 | B | **B** | T + S (26 CPU-h) + R | Case 3. The paired pile-up-only finder pass that the fixer declined (FR §2 N1) is the clean estimator of the excess. |
| P6 | **The ceiling tests have no family-wise control, and the false-loss rate shown to the user leaves them out.** About 16–55 one-sided tests can each remove selections; at the boundary that gives 5.5–17.5 % at least one false FAIL, against the "2–4 %" in Df-2 and §4.12 rule 1. | Ph-B6; K-F2 | B, B | **B** | S+T+G | Case 1. This is the N4 defect pattern again. |
| P7 | **The occupancy crossing tests in the fit-probability and shape families are consistency checks** (the same quantity on two samples of the same construction at the same rung). Yet a PASS removes those families from d_out: the width at R11–R20 falls from 1.29–4.88 to 0.45–0.49 without the width-transfer assumption ever being tested. | Ph-B5 | B | **B** | T+S | Case 3, verified against v3's own definition (l.310–312). A width earned by construction. |
| P8 | **The π_k planning row "tested at R06–R07" applies to no term in the expected case.** At R06 only, s_tot is 1.41, not 0.73. | K-F4 | B | **B** | S+T | Case 4, settled in §2. |
| P9 | **"Target met" can still be read when every leading term is a "low count" (m = 1–3)**: σ_ln = 0.26 and f₀ = 0, with no term an estimate. | N-B3; Ph-C4 | B, C | **B** | T | Case 2. I side with N: this is the N3 twin, a pre-declared label that passes in a case it should flag. |
| P10 | **Q3 does not name every route to NOT TESTED for a MUST criterion.** Missing: the cap route ("not submitted"); the fluctuation route (P ≈ 0.28 that at least one of the four supplied terms ends untested); B3-a/b/c/d and B4-e; and B2-c NOT EVALUABLE at depth. FR l.237 contradicts its own rows. | K-F1; N Part 2.8 (Q3 remarks) | B | **B** | T+G | Case 1. Brief D4; the cycle-2 ruling that NOT TESTED for a MUST criterion "is not a default". |
| P11 | **The T1 coverage checks (T1-c (iii), T1-h) false-fail a correct likelihood in 15–48 % of cases** (8–10 checks at ≥ 0.93 of 500, against a true coverage of 0.945–0.95), and a FAIL blocks every quoted limit. | K-F5 | B | **B** | S+T | Case 3, verified (§2). |
| P12 | **The Q5 premise ("which no analysis choice influences") is inaccurate.** | K-F6; N Part 2.8 (Q5: say where the 1.8 days come from) | B | **B** | T+G | Case 3, verified (§2). The user would grant an exception to a fixed decision on a premise the strategy contradicts. |
| P13 | **The default plan spends 156 CPU-h outside the figure the user approves** (4,534 against 4,378), and the stop threshold is keyed to the lower figure. | K-F7; N-C1 | B, C | **B** | S+T+G | Case 2. I side with K: an approval the strategy expects to exceed is the N12 pattern. |
| P14 | **Two day-15 rule inputs have no sample.** (i) The R06 rates of the eleven small SM processes: no Phase-3 SM sample exists, and the 50 CPU-h "development" line gives 2–10 counts per process. (ii) The pilot ceiling at the R09 width: 0.4–3.7 expected counts, with no stated reading of a pilot count of 0, 1 or 2. Also: "B₅₀ at the best candidate" is undefined before unblinding (N-C6), and the mixed-fraction expectation has no date (Ph-B4 point 2). | N-B4; N-C6; Ph-B4 (2) | B, C, B | **B** | T+R | Case 1. An executability gap in a dated rule. |
| P15 | **B1 trace gaps.** (i) The per-k promotion comparison is assigned to the 4a derivation overlays, but s_model must be fixed before the freeze; only the pilot's 1,000 overlays (sample 11) exist then. (ii) The PREREG outline (§8 item 2, COM PR-1) omits the ceiling test, the completeness bound and c_mix, although they decide eligibility. | N-B5 (i), (iii); K-C4 | B, C | **B** | T | Case 1 (K-C4 is the same contradiction). |
| P16 | **Agent concurrency in Phases 2–3 exceeds the cap of three**: three channels plus per-channel reviews, the PREREG drafter and the sealed-comparison agent. | N-B6 | B | **B** | T (+ schedule) | Case 3, verified (§2). The cycle-2 fix (N18) is incomplete. |

**Case 5 (items all reviewers missed).** I raise no new A or B item.
- I checked conventions coverage (the critical reviewer's table is complete; the only gap is K-C1), the regression
  triggers (§8) and the competing-group question.
- Two C items are promoted *into* existing findings because they are inputs of a dated rule: N-C6 into P14, and K-C10
  into the P4 cost line. The pilot's DIF/NI no-pile-up events need the Geant4 vertices, about +6 CPU-h.

**Category C (apply without re-review, unless they touch a P item).** All are adopted except as noted.
- Ph-C1 / K-C5: one NI rate set, name the ×0.22 factor. Ph-C2: no Geant4 conversions in B1. Ph-C3: B4-c split by
  sub-topology as a consistency check. Ph-C5: s_model of the occupancy model at a rung not used for its inputs.
  Ph-C7: count the multi-vertex class per rung. Ph-C8: offer the ln-rejection distance in Df-2. Ph-C9: the pile-up cap
  as the predictive draw of the no-credit bound.
- K-C1: state the re-test threshold departure in §5.2 row 1 and Df-2. K-C2: the W(τ) generation mode. K-C6: name the
  Geant4 slab yield (D) in §11.2. K-C7: four labels in COM T1-c. K-C8: "no closure verdict and no limit". K-C9: C2-c
  family (combined χ² or Bonferroni). K-C11: one line on BL-1 in §12.3. K-C12: "thousands", not "hundreds", in the
  Q3 annex. K-C13: say which costs checkpoint 1 can fix.
- N-C2: notation "true λ". N-C4: confirm the mapping against `book/checks/ch29_checks.py`. N-C8: R-20 deadline before
  4a. N-C9: mark the 84 % point on Fig. 7. N-C11: s_model of the B4 estimator from Z(νν) only. N-C12: absorbed by S-1.
  The C1 remediation-time sentence (N Part 2.4).
- **Not adopted:** N-C10 (promote Df-1 to a question). It is a matter of taste, and Df-1 stays first in the defaults,
  with the reading spelled out.

**Dismissals: none.** Every A and B item of every review is accepted (mapping in §10).

**Reviewer-pressure protection.** FR §2 N1 declined the 26 CPU-h paired pass and counted the mixed class "as an upper
value". That is the executor's explanation, not independent evidence, and Ph-B4 shows that the upper value makes the
test ill-posed. P5 therefore stands.

---

## 5. The Category A item, P1: confirmation and exact fix

**Confirmed A.**
- The method text (§4.7 point 3) promises no-pile-up P_geo, f_k and H for "each process". The pool, the inventory and
  the budget hold no such events for Z(ττ) and lost-lepton Z(ℓℓ).
- With the planned samples their term beyond the hit-level reach can only be 1.14 × N_t/2,000. At any plausible
  N_trig that is 57–740 events. It would set the projection, the day-15 class and the headline, and none of those
  currently contains it.
- The reclassification argument does not hold. One could say that N_trig is unknown and that rule 1 would catch it.
  But rule 1 recomputes "Table 4.4c", which omits the terms, so the safety net does not exist as written.

**Exact fix.**
1. **Script.** Add `Z(tautau)` and `Z(ll) lost` to `SM_NTRIG`, with labelled EST planning values. Recommended: Z(ττ)
   4×10⁵ (range 10⁵–1.3×10⁶) and Z(ℓℓ) 3×10⁴ (range 10⁴–10⁵), with the arithmetic of N-A1 written out (branching
   ratio relative to Z(νν), MET > 250 GeV fraction after the lepton veto) and tagged [E].
   - Re-run the allocation **inside the 665 CPU-h pool** (default, 0 CPU-h). The summed floor becomes ≈ 12.1–13.2
     events (≈ 12.5 at the planning values). The alternative of keeping 11.7 costs +24–85 CPU-h.
   - Print both, and the new per-term rows.
2. **Multijets.** Their loose population (12.5 CPU-h) stays. Add a planning range for their floor
   (N_MJ × 1.14/10⁶ via the factorisation, labelled EST) to the headline sum (Ph check 1).
3. **Text and tables.**
   - Add the inventory rows for the two new pool shares, with seed streams (for example `prod.hs0.ztt`, `prod.hs0.zll`).
   - Table 4.4a: add two rows, and delete "not in the table".
   - Table 4.4c: carry the additions in every row at the planning N_trig.
   - §0 and Q2: say so.
   - Q3 annex row: give their floors.
   - §4.7 l.1071–1072: "fourteen processes".
4. **Rule.** The shares are re-allocated at day 12–15, when the MET model gives N_trig (dated rule in §11.7). Rule 1
   recomputes the projection **for every term of the likelihood**, not "Table 4.4c".

---

## 6. Work list for the fixer (priority order)

**General rules.**
- Write `STRATEGY_<fixer>_<timestamp>.md` and update COM, the script and a fix report.
- Trace every change to a P number.
- Do not reopen brief §3, reintroduce any discarded item, or loosen any F.
- Every number shown to the user (§0, Q1–Q5, Df) must come from a printed script section.
- **Numbers to recompute via `strategy_budget.py` are marked [S]**; the rest is wording [T].

### (i) What the user is shown (highest priority)

1. **P1 (A).** As in §5. [S] and [T].
2. **P2, the honest headline.**
   - [S] Add to script [9b], and to Table 4.4c, three EST scenarios beside the Z(νν) rows:
     - **(α)** DIF and the conversion part of B4 extrapolated from v1's R06–R07 attributed counts, (α1) with the
       pile-up fall per width step (×201–339) and (α2) with their own observed R06→R07 fall; each with and without
       fit-probability credit at R09, the uncredited case being R09 = R08.
     - **(β)** "Z(νν) tested and credited; the eight proxied processes and the additions at H", with H per event as for
       Z(νν) (N-B2).
     - **(γ)** The non-Z SM ceilings scaled with N_trig rather than N_Z (K-C3).
   - Relabel the m_H rows "Z(νν) enters at its ceiling (estimator not credited)". Write "100 simulated ceiling events
     (≈ 220 background events)" (N-C5).
   - [T] In §0 and Q2, **lead with the range, not 790**: give the conservative 84 % edges and the medians across the
     rows (expected wording in §7), mark 790 as the empty-ceiling median (upper edge), and print the multijet planning
     range.
   - State the two caveats of (α): v1 put the pile-up vertices at the PV, and its attribution rule is not yet
     transcribed.
   - State that the **day-15 pause is a realistic branch**.
   - Say once which number heads the abstract: the 84 % edge, by l.1399. Put "EST, v1 placeholder efficiencies, best Λ
     per mass" inside the Q2 cell (N Part 2.7). Add the C-3 sentence (v1 fast-path bias) and the Ph-C6 caption
     sentence. Say that the label holds for small m_H only (N-C7).
3. **P13, the reserve inside the approval.** [S] The approved figure becomes 4,378 + 156 = 4,534 CPU-h, plus the
   additions of P4, P5 and K-C10 (≈ 39 CPU-h), so ≈ 4,573. The threshold is 1.3× that (≈ 5,945).
   - The script prints the exact values in [4] and [6]. Update §0, §11.2 (delete "none of these is inside", and list
     the reserve as part of the approved figure), §11.6 and Q4.
4. **P10, Q3 complete.** [T] Widen Q3 to "every MUST closure criterion that ends NOT TESTED, NOT EVALUABLE or not
   submitted, by planned statistics, by a fluctuation, by the cap rule, or by a day-15 rule".
   - Add one annex row per route, with its expected probability ([S] for the fluctuation route, 1 − 0.92⁴ = 0.28),
     the cost of compliance where defined, and the default. Routes: (1) the cap route; (2) the fluctuation route of
     the four supplied terms; (3) B3-a/b/c/d and B4-e; (4) B2-c.
   - For route (2) the compliance is the staged top-up of P14 (0 CPU-h by default).
   - State the consequence under (a): the terms are labelled "no credit" in the paper and in the ladder figure, and the
     reserve may already be spent by rule 3 (N Part 2.8).
   - Align §4.0 point 6, §11.7 rule 2 and the FR statement.
5. **P6, the ceiling family.** [S] One ceiling verdict per term: the combined one-sided test over its evaluable rungs
   (or the min-p over rungs with Šidák), with a family rule over the terms (Bonferroni, so that the family-wise size
   at the boundary is about 5 %).
   - Each sub-topology test is assigned to the B4 term of its origin, or dropped under P4 (iii).
   - Add the family to the eligibility rates in script [11], the §4.0 point 4 table, §4.12 rule 1, Df-2 and the
     PREREG outline. Restate "loses a selection with probability x %" with the new x.
6. **P9.** [T] The third condition of "target met" becomes "**every leading term labelled estimate**" in §4.11 point 3,
   COM TG-1 and §0. Print s_tot next to every label (Ph-C4).
7. **P12.** [T] Q5 and §4.17: "whose content depends on the MET model, the trigger threshold and the generator-cut
   decision, all frozen by day 12 before the propagation, but on no plane-selection choice and on no signal efficiency
   at any T2 candidate". Add that "no" moves 266 CPU-h onto the critical path.

### (ii) The ceiling H and its tests

8. **P3, CKF in H.** [T] Define H's treatment of CKF removal and f_CKF. **Default (technical, Df-9): option (a).** H is
   classified on all own hits; CKF removal and f_CKF < 0.2 enter as a survival-type factor S_CKF. S_CKF is credited only
   where tested (overlays and hit-level halves, R04–R06), carries s_tot beyond, and is censored at 1. This keeps H a
   true ceiling.
   - Option (b), CKF at its pile-up-200 efficiency with a width, is the stated alternative.
   - Replace the "by construction" sentence with a table of every fixed cut and its monotonicity under added hits.
   - [S] Project m_H for Z(νν) under the chosen definition (planning, EST) in Table 4.4c's scenarios.
9. **P4, the samples of the ceiling and completeness tests.** [T]
   - Ceiling and leak tests run **only on unbiased samples**: the 1,000 unbiased DIF events, the NI overlays and the
     hit-level halves. The enriched DIF overlays serve only the S/π_k closure.
   - Label the leak fraction an implementation check.
   - Sub-topologies (K-F3): **default (ii)**. Drop their ceiling test and keep them as completeness and diagnostic
     populations (no CPU). Option (i) is a costed paired test.
   - Name the development samples. [S] Add 1,000 unbiased Geant4 DIF overlays in Phase 3 (≈ 7 CPU-h, development; it
     replaces C′_PU, which has no Geant4). The pilot's 10⁶ unbiased DIF/NI no-pile-up events get their Geant4 vertices
     (K-C10, ≈ +6 CPU-h).
   - Write the effective-count form of the ceiling test for weighted samples (l.1301).
10. **P5, the mixed numerator.** [S] Adopt the paired pile-up-only finder pass on the completeness samples (26 CPU-h,
    re-analysis): mixed excess = mixed(with term) − mixed(term hits removed).
    - Keep the 0.26 bound as a declared convention.
    - State what an untested term enters as after a completeness FAIL. Default: the promotion sum extended to k > k_max
      at π_k = 1 (no credit), i.e. **the term enters at the extended ceiling H′ = P_geo + Σ_all k f_k**, eligible and
      flagged; ineligible only if H′ itself fails its ceiling test.
    - [R] The expected mixed fraction from the C1 development samples is a dated day-15 input.
11. **P7, crossing credit.** [T][S] **Default (Df-2 addition): option (a).** The occupancy-model comparisons at
    R09⊗R06, R11⊗R06 and R15–R20⊗R06 are consistency checks with no distance credit. The thinning and π_k crossing tests
    keep their credit (they are genuine).
    - Option (b), deriving the fraction at R05 and testing at R09⊗R06 and R09⊗R07, may replace (a) if the fixer writes
      it fully. In both cases the width step from the last crossing rung to R08 counts in d.
    - Correct table row l.431 and every reading that uses 0.45–0.49.
12. **P8.** [S] Replace the row with "π_k tested at R06 only (expected for DIF at G < 4 and for every B4 term)":
    1.41 / 1.41 / 1.41 / 2.51 (1.42 with a 2S crossing PASS). Keep "R06–R07" as the conditional row. Correct
    l.1586–1587 and §0 point 3 if it relies on 0.73.

### (iii) Statistics, rules and executability

13. **P11, T1 coverage.** [S][T]
    - State the family: T1-c (iii) and T1-h, the number of checks, and whether 500 is per (point, λ).
    - Either pool the λ values into one coverage test per point, or set the per-check threshold for a family-wise size
      of about 5 % (for 10 checks at 500 pseudo-experiments: pass at ≥ 462, P = 0.46 % per check at a true 0.95; my
      binomial).
    - Compare with the convention's computed coverage at the workspace's κ, not with 0.95. Add an INVESTIGATE band
      and one re-test, as in §4.0.
    - Update script [13] and COM T1-c/T1-h.
14. **P14, day-15 inputs.** [T][R]
    - (i) No new Phase-3 SM samples. Rule 4 and the re-sizing of the four supplied terms use v1-proxy rates (labelled,
      with their errors) at day 15. The 4a hit-level campaigns are **staged**: the first half of each sample is
      produced, its R06 rate measured, and the second half sized from it (top-up from the reserve, or a reported
      conditional draw). This also answers P10 route (2). Say so in §4.7, §11.7 and the inventory (INV-1).
    - (ii) The pilot reading. H at a T2 candidate enters as Gamma(m + 1) of the pilot count. The branch of rule 3 is set
      by the R06–R07 pilot counts, extrapolated in width with the fall the pilot itself measures (EST).
    - "Best candidate" in rule 1 means the candidate with the lowest projected B₅₀ × (1/G) computed with v1
      placeholders (§4.12 rule 4) (N-C6).
    - Adopted zero-CPU change: rule 1 is computed **preliminarily at day 7** from the finished pilot and reported in
      `STATUS.md`; it becomes binding at day 15.
15. **P15.** [T] The per-k promotion comparison uses the pilot's 1,000 near-pass overlays (sample 11), with the
    expected number of classes reaching 24 promoted events stated. If too few, the promotion model is "not submitted"
    and the term enters at H; the 4a derivation overlays then refine only the post-freeze S. Add the ceiling test, the
    completeness bound, c_mix and the CKF factor (P3) to §8 item (2) and COM PR-1.
16. **P16, slots.** [T][S] Add a slot table per phase (executors + reviewers + drafter ≤ 3):
    - **one** Phase-3 1-bot review on `SELECTION.md` (the JFC tier), not one per channel;
    - the PREREG drafter as channel (iii)'s second task after day 12;
    - the sealed C1 comparison as a short, separate session run sequentially inside channel (i)'s slot.
    - Adopt S-1 (§7). Recompute the calendar (script [7]).

### (iv) Category C items

17. **The C items** of §4, as listed there.

### (v) Length (adopt now; the arbiter's ruling)

18. **Cuts.**
    - Delete §13.1 and reduce §13.2 to the two number corrections, each with a pointer to the fix reports (≈ 70 lines).
    - State the eligibility logic **once** (§4.0 point 6) and refer to it from §4.11 point 3, §4.12 rule 1, the
      partial-outcome table and COM T2-a (≈ 30 lines). This removes the five-place edit risk that produced several
      cycle-3 contradictions.
    - Replace §12.4 with a pointer to §11.7 and §6.4 (≈ 15 lines).
    - Merge Table 4.0 with the §11.2 provenance table (≈ 25 lines).
    - The statistics-justification appendix, the move of §6.1–6.2 and the move of the §8 hashes are **optional**: they
      are taste, not defects, and will not be re-reviewed.
    - Target ≤ 2,500 lines after the additions. §12.1 with its annex fits in three pages.
    - The four derived documents (task sheets, PREREG skeleton, NUMBERS register) are **an orchestrator task after
      PASS**, not fixer work. I recommend them before Phase 2.

**What is computed [S], in one list:**
- the pool with two more processes;
- the headline scenarios α, β and γ;
- the multijet range;
- the approved figure and threshold with the reserve and the +39 CPU-h;
- the fluctuation-route probability;
- the ceiling family rates;
- the crossing-credit widths;
- the π_k R06-only row;
- the T1 family thresholds;
- the calendar after S-1 and S-3.

**Everything else is wording.**

---

## 7. Rulings on the constructive reviewer's zero-CPU schedule changes, and the final Gate-A list

**Schedule changes.**

| change | ruling | reason |
|---|---|---|
| S-1: B5 (SHOULD) and the B6 signal arm out of the 4a production window, into days 36–48 | **Adopt.** COM B5-a…c deadlines move from 4a to 4b. The 4a note states that B5 and B6 are pending. | 0 CPU-h, ≈ 1.5 days on the critical path, and it provides the buffer of N-C12. No MUST criterion is touched; B5 is not in the likelihood, and the B6 ratios are read only after the verdicts anyway. |
| S-2: extend the D7 reading to generator-level *background* inputs before the hash | **Not adopted.** | It widens an exception to a fixed user decision ("before any v2 production sample exists") to background samples. Q5 already puts the narrower reading to the user; the 0.5 day does not justify a second exception. |
| S-3: one Phase-3 1-bot review; drafter in channel (iii) after day 12 | **Adopt.** | It is the P16 fix. |
| S-3: move P1 into the production window | **Not adopted.** | Brief l.264–265 places the P1 tests in Phase 2. |
| Rules 1 and 3 at day 7 | **Adopt rule 1 as preliminary at day 7, binding at day 15**; rule 3 stays at day 15. | The early projection informs the drafter and the user at no cost. The reserve routing needs the day-15 completeness inputs. |

**The honest headline (what §0 and Q2 must say).**
- **What leads.** The conservative range, not 790 GeV: *"Expected (EST, v1 placeholder efficiencies, best Λ per mass):
  a background bounded by simulation statistics; reach ≈ 720 GeV at the 84 % edge if every no-pile-up ceiling counts
  zero (median ≈ 790, an upper edge, not the expectation); ≈ 500–650 GeV if decays in flight and hard-scatter
  conversions fall from v1's own R06–R07 counts as the pile-up background does and earn no promotion credit; 1,026 GeV
  for a negligible background; existing bounds ≲ 180 GeV."*
  - The fixer replaces "≈ 500–650" and "≈ 720" with the script values of scenarios α and β.
  - P1 moves the floors slightly; the fixer prints the new values.
- **Caveats, in the same paragraph:**
  - v1 placed the pile-up DIF vertices at the PV, and v2 places them at their own z, which may lower α;
  - v1's attribution rule is not yet transcribed;
  - the SM floor rests on a guessed 45 ms per event (doubling it raises the SM floor to about 11);
  - the v1 fast-path efficiencies are ×1/0.87 high.
- **The pause.** *"The day-15 rule pauses the study and asks you if the projected B₅₀ exceeds 300 events. By v1's own
  record this is a realistic branch, not an exception."* The reviewers' evidence (§2: 1.3×10⁵ DIF events at R07 in v1;
  380–750 at R08 with a pile-up-like fall) supports this wording. It does not support "likely" as a firm prediction,
  because the own-z placement and π_k credit can remove most of α. "Realistic branch" with the α numbers is the honest
  statement.

**Questions for the human (one line each; ● = recommended default).**
- **Q1, C1 blinding exception.** May the C1 reproduction compare six v1 signal counts that are also v2 candidate
  efficiencies, before the closure verdicts? ● Yes, sealed: PASS/FAIL only until Gate B, four counts open. Other
  options: all ten open and disclosed, or the six dropped. 14 CPU-h in every option. *(unchanged)*
- **Q2, the bounded paper as the default deliverable.** Proceed to production without a pause, with the headline
  above? ● Yes: production pauses for you only if the day-15 projection (preliminary at day 7) exceeds B₅₀ = 300 events
  or both pile-up estimators miss their cap. Alternatives: always pause at day 15; or a doubled pool (+665 CPU-h,
  ≈ +3.8 days, a gain only if the ceilings are empty).
- **Q3, brief D4 exception, completed.** For every MUST closure criterion that ends NOT TESTED, NOT EVALUABLE or not
  submitted, may the factor enter at no credit (the term at its tested ceiling H), with the selection eligible,
  labelled "no credit" and reported in `STATUS.md`? The routes are the annex rows: planned statistics (eight proxied
  processes, the three additions), a fluctuation of the four supplied terms (≈ 28 %, topped up by staging), the cap
  rule, B3 and B4-e, and B2-c at depth. ● Yes. Alternatives: comply where costed (≈ +680 CPU-h, 100–1,230, ≈ +3.9 days
  for the eight processes; per-row costs in the annex); or strict, where such selections are not eligible and "closure
  fails" becomes a likely paper.
- **Q4, budget, calendar and stop rule.** Approve ≈ 4,573 CPU-h (4,378 + the 156 CPU-h day-15 reserve + ≈ 39 CPU-h
  of review additions; exact value from the script) and ≈ 57 days (against your 2–4 weeks), with [DP1], [DP2], [DP4]
  and [DP5]? ● Approve. The stop-and-ask threshold is 1.3× that (≈ 5,945). The contingency (2,135 CPU-h) and the
  conditional costs are listed, not pre-approved; every draw is reported as an overrun. The day-5 re-projection may
  trigger the stop rule. Alternatives: pre-approve the contingency envelope; MUST only; or full SHOULD.
- **Q5, the D7 reading, premise corrected.** May the truth-level S1 samples (Stage 2 and the string propagation, 47 +
  266 CPU-h) exist before the pre-registration hash? Their content depends on the MET model, the trigger threshold and
  the generator cut, all frozen by day 12, but on no plane-selection choice and no T2 efficiency. ● Yes. Alternative:
  after the hash (+47 CPU-h; 266 CPU-h move onto the critical path, +1.8 days).

**Defaults the human can override (reported, not asked).**
- Df-1 to Df-8 as in v3, with two corrections:
  - Df-2 restates the false-loss rate *including the ceiling-test family* (P6), adds the occupancy crossing comparisons
    as consistency checks without distance credit (P7), states the re-test threshold departure (K-C1), and offers the
    ln-rejection distance (Ph-C8);
  - Df-8 is unchanged.
- New **Df-9 (technical): H classified on all own hits, with CKF removal and f_CKF as a tested, censored survival
  factor** (P3). Alternative: CKF at its pile-up-200 efficiency with a width.
- New **Df-10 (technical): T1 coverage tested with a family-wise size of 5 %** against the convention's computed
  coverage (P11).
- **A line in §12.3 (FYI):** the A/f₂₀₀/m_mig selection-independent exception (BL-1, K-C11).

---

## 8. Regression and motivated-reasoning checks

**Regression triggers (§6.7).** Phase 1 has no results, so validation failures, a > 80 % systematic, GoF and bin
exclusion do not apply. **Tautological or pass-by-construction validations in planned criteria: yes, three, all fixed
in this iteration.**
- The ceiling and leak tests on enriched samples (P4).
- The occupancy crossing comparisons that earn width credit while being consistency checks (P7).
- The "complete by construction" claim for H, which ignores non-monotone cuts (P3).

There is no earlier phase to regress to.

**Motivated reasoning.** v3 is candid where it counts most: "not the expectation", "this may well happen", the
sample-size-limited label. But every remaining error still leans favourable:
- the headline at the empty-ceiling edge, with DIF and conversions at their floors (P2);
- two terms without samples absent from the projection (P1);
- a smaller π_k width (P8);
- a crossing credit earned by construction (P7);
- a false-loss rate without the ceiling tests (P6);
- an approval figure 156 CPU-h below the default spend (P13);
- a D7 premise stated more cleanly than the plan supports (P12).

None is concealment, because the strategy itself contains the facts the reviewers used. It is the pattern that the
user-facing numbers are drawn from the favourable case. The work list corrects each one.

**Competing group.** A competing group would have the leading terms tested, not bounded, and would know whether DIF
dominates at R08. v3 gets there through the pilot and the day-15 rule. After P2, the user is told in advance that the
rule may well fire.

**Brief compliance.**
- D4: completed by P10.
- D6/§7 stop rule: the base is corrected by P13.
- D7: the premise is corrected by P12.
- The brief's Phase-2 list keeps P1 there (S-3 part not adopted).
- Nothing discarded returns.

---

## 9. Convergence

This is cycle 3: the protocol's first warning (§6.5, warn at 3). The trend is 11 A → 4 A → 1 A, every reviewer
reproduces v3's numbers, and all three reviewers say the remaining work is text, tables and script lines. I agree.

**My judgment: the fix of §6 can be done in one pass, and cycle 4 should be a pure verification of P1–P16.** The
verification checks, item by item, that:
- each correction is written as specified;
- each [S] number is printed by the script and quoted identically in §0, §12.1, COM and the PREREG outline;
- nothing else changed.

Reviewers in cycle 4 should raise a new finding only if it is one of three things:
- a regression introduced by the fix;
- a factual error in a number shown to the user;
- a genuine Category A.

Everything else goes to C. This does not lower the bar. Each P item is a genuine defect and must be fixed. But the
strategy now has a stable design, and further design suggestions belong to Phase 2–3 measurements.

**Matters of taste or of Phase-2/3 measurement, turned into rules or defaults now (not to be carried into another
cycle):**

| matter | settled as |
|---|---|
| CKF option (a) or (b) for H (P3) | Df-9 default (a) |
| Occupancy crossing credit (a) or (b) (P7) | Df-2 default (a) |
| Combination method for the ceiling family (P6) | the fixer's choice of combined test with Bonferroni over terms; any family-wise-5 % rule is acceptable |
| Pooled vs Bonferroni T1 coverage (P11) | Df-10; either form is acceptable |
| Sub-topology ceiling test (P4 iii) | default: dropped; diagnostic populations |
| Magnitude of DIF and conversions at R08–R09 (P2) | Phase-2 pilot; the preliminary day-7 and binding day-15 rule 1; EST rows now |
| Magnitude of the mixed fraction (P5) | day-15 input; the paired pass measures it |
| R06 rates of the small SM processes (P14) | staged 4a production with top-up; v1-proxy rates at day 15 |
| Pilot ceiling readings (P14) | Gamma(m + 1) reading, with the branch from the R06–R07 pilot counts |
| N_trig of the additions (P1) | EST planning values now; re-allocation at day 12–15 |
| Promoting Df-1 to a question (N-C10) | not adopted (taste) |
| Length beyond the mandatory cuts; derived documents | optional; orchestrator task after PASS |
| Phase-3 calendar under the cap (P16) | recomputed by the script after S-1/S-3; the residual uncertainty is reported, not re-reviewed |

If cycle 4 finds P1–P16 fixed as specified, the arbiter should PASS. If one item is fixed only partially, a short
focused fix is preferable to a further full panel.

---

## 10. Mapping of reviewer items to merged findings (every A and B)

| reviewer item | merged | | reviewer item | merged | | reviewer item | merged |
|---|---|---|---|---|---|---|---|
| Ph-B1 | P2 | | K-F1 | P10 | | N-A1 (A) | P1 |
| Ph-B2 | P3 | | K-F2 | P6 | | N-B1 | P2 |
| Ph-B3 | P4 | | K-F3 | P4 | | N-B2 | P2 |
| Ph-B4 | P5 (+ P14 for the date) | | K-F4 | P8 | | N-B3 | P9 |
| Ph-B5 | P7 | | K-F5 | P11 | | N-B4 | P14 |
| Ph-B6 | P6 | | K-F6 | P12 | | N-B5 (i), (iii) | P15 |
| | | | K-F7 | P13 | | N-B5 (ii), (iv) | P4 |
| | | | | | | N-B6 | P16 |

C items folded into A/B findings: Ph-C4 → P9; Ph-C6, K-C3, N-C3, N-C5, N-C7 → P2; K-C4 → P15; N-C1 → P13; N-C6 → P14;
K-C10 → P4 (cost line). Partial earlier findings: M4 → P7, P8; M5 → P4, P10; N1 → P3–P6; N2 → P10; N5 → P8;
N7 → P1, P2; N14 → P12; N18 → P16.

---

## 11. Verdict

**ITERATE.**
- **Category A item that blocks: P1** (Z(ττ) and lost-lepton Z without a no-pile-up pool share).
- **All 15 B items (P2–P16) must also be fixed before PASS.** In priority order: P2 (the headline), P13, P10, P6, P9,
  P12, then P3, P4, P5, P7, P8, then P11, P14, P15, P16.
- The fixer works from §6, recomputes every [S] number in `strategy_budget.py`, and rewrites §12.1 to the list of §7.
- Cycle 4 is a verification of P1–P16 (§9). This is review cycle 3, with the first iteration warning noted.
