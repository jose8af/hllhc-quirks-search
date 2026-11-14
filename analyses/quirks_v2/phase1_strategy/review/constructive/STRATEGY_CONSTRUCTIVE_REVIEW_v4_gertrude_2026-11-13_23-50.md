# Constructive review, cycle 4: STRATEGY v4 (quirks v2, Phase 1)

Reviewer: Gertrude (constructive), 2026-11-13 23:50. Fresh to this panel.
Role and template: `agents/constructive_reviewer.md`. "Constructive" does not mean "lenient": genuine errors are A,
and the honest-framing check applies.

**Artifact.** `phase1_strategy/outputs/STRATEGY_fiona_2026-11-13_23-05.md` ("v4", 2,842 lines, read in full,
l.1–2843) and `QV2/COMMITMENTS.md` ("COM", read in full).

**Also read.**
- In full: the cycle-3 arbiter verdict (Felix), the fix report `FIX_REPORT_cycle3_fiona.md` ("FR"; its claims are
  not evidence), `AGENT_RULES.md`, `FRAMING.md`, the study and phase `CLAUDE.md`.
- The cycle-3 constructive review (Fabiola), its part 3 only, as background.

**My own checks.**
- I ran `phase1_strategy/src/strategy_budget.py` (standard library, `python3 -I`, niced; 8.8 s, 31 MB RSS, exit 0),
  with the output in the scratchpad.
- I wrote my own independent standard-library recomputation (scratchpad `check.py`) of:
  - the pool allocation and floor;
  - the predictive distribution;
  - the approved figure and threshold;
  - both family-wise rates;
  - the T1 thresholds;
  - the fluctuation route;
  - the calendar sum.
- Both are logged in `phase1_strategy/logs/constructive_gertrude_2026-11-13_23-50.md`.

**Rules followed.** No sub-agents, no git, nothing heavy on einstein. I wrote only this file and the session log.

**Scope, as the arbiter's §9 asks.** This is a verification cycle. I raise a new finding only if it is one of three
things:
- a regression;
- a factual or framing error in what the human is shown;
- a contradiction between two binding statements that an executor would hit.

Everything else is C.

---

## Summary

v4 is a careful and almost complete execution of the cycle-3 work list.
- **Every [S] number I recomputed independently reproduces v4 and the script:**
  - the floor after the re-split;
  - the approved figure and threshold;
  - both family-wise rates;
  - the T1 thresholds;
  - the fluctuation route;
  - the calendar.
- The Category A item P1 is resolved.
- Fifteen of the sixteen P findings are RESOLVED. **P2 is PARTIALLY RESOLVED.**

**Remaining defects: two new Category B items, both text-only.**
- **B-1 (the P2 residual: the lower branch of the headline).** §0 and Q2 quote the decays-in-flight scenario (α1) as
  a median (≈ 470–500 GeV) right after an 84 %-edge number for the empty-ceiling case. They omit (α1)'s own 84 % edge
  (421–455 GeV), the (α2) rows below 393 GeV, and the log-normal reading. The fix report says that "both readings are
  stated in §4.4"; they are not.
- **B-2 (B1 trace).** The pilot is "finished by day 5" and feeds the day-7 and day-15 projections. But the code it
  needs (the own-hit classifier with k per layer type, H on all own hits, and the occupancy-model π_k for the per-k
  comparison) is scheduled in Phase 3.

**C items: 11.**

**Judgment: not yet. Close to PASS.**
- Both blockers are fixed by a few sentences, with no CPU and no design change.
- A short focused fix, checked by the arbiter, is enough. A further full panel is not needed.

| | count |
|---|---|
| P findings verified | 16: **15 RESOLVED, 1 PARTIALLY (P2), 0 NOT RESOLVED** |
| new A / B / C | **0 / 2 / 11** |

---

## Part 1. Verification of P1–P16

Each entry gives the status, the v4 location, a quoted phrase and my own check.

**P1 (A): Z(ττ) and lost-lepton Z(ℓℓ) without a no-pile-up share. RESOLVED.**

Where v4 fixes it:
- Table 4.4a (l.853–858) has the two rows with their [E] arithmetic, and the multijet row. Its total line reads
  "**12.6** (12.2–13.3)".
- §4.7 point 3 (l.1224): "The fourteen are v1's twelve and the additions … seed streams `prod.hs0.ztt`,
  `prod.hs0.zll`".
- Inventory rows 18a and 18b (l.2021–2022).
- "not in the table" is gone (grep: 0 hits).
- §11.7 rule 1 (l.2631): "recomputed **for every term of the likelihood**"; rule 6 handles the re-allocation.
- The Q3 annex row gives the floors 0.34, 0.09 and 0.46.

My check (own allocation code, M_t ∝ √(N_t/c_t), 665 CPU-h):

| quantity | my result | v4 |
|---|---|---|
| B1 pool share | 208.5 CPU-h (3.61×10⁷ events) | 208 CPU-h |
| SM pool share | 456.5 CPU-h (3.65×10⁷ events) | 457 CPU-h |
| summed pool floor | **12.60** | 12.6 |
| Z(ττ) / Z(ℓℓ) floors | 0.34 / 0.09 | 0.34 / 0.09 |
| floor at the low / high planning N_trig of the additions | 12.18 / 13.27 | 12.2–13.3 |
| floor with 822 / 1,330 CPU-h | 10.2 / 6.3 | 10.2 / 6.3 |
| floor at 90 ms per hard-scatter event | 20.79 | 20.8 |
| predictive 16 % / 50 % / 84 % (2×10⁵ draws, multijets at κ = 0.40) | 7.7 / 10.8 / 15.2 | same |
| σ_ln | 0.34 | 0.34 |

Without the additions the floor would be 11.76 against v3's 11.70. The difference comes from the corrected NI rate
set (Ph-C1), which is consistent with FR §3.

**P2: honest headline. PARTIALLY RESOLVED (residual = new B-1).**

What is in place:
- §0 l.59–71 and Q2 l.2679–2685 lead with the 84 % edge: "reach **≈ 710 GeV at the 84 % edge if every no-pile-up
  ceiling counts zero** (median ≈ 790, an upper edge, not the expectation)".
- The (α) range is given.
- (β) is given (≈ 770, edge ≈ 705).
- The four caveats are given: PV placement, the attribution rule, 45 ms (at 90 ms the floor is 20.8) and ×1/0.87.
- "The abstract heads with the 84 % edge".
- "a realistic branch, not an exception".
- The EST tag sits inside the Q2 cell.
- Table 4.4c has (α1), (α2), (β) and (γ), with rows relabelled "Z(νν) enters at its ceiling (estimator not credited)".

Script [9b] reproduces every row I checked:

| row | script [9b] |
|---|---|
| empty ceilings | 790 [712] |
| (α1) ×339, no credit | 504 [455] |
| (α1) ×201, no credit | 469 [421] |
| (β) m_H = 10 | 767 [706] |
| class limit at m_H = 125 | B₅₀ 302, 559 GeV |

What remains: see B-1. In short:
- The (α) branch is quoted as a median, with no edge, beside an edge for the other branch.
- The (α2) rows and the log-normal reading (below 393 GeV) are absent from §0 and Q2.
- (γ), the envelope with every SM ceiling at H (548 [499] GeV at m_H = 100), is not in the headline either. That
  last point is C, since (β) is the expected case.

**P3: H and CKF. RESOLVED.**
- §4.4 point 4 l.719: "complete for attributed candidates **for the cuts that are monotone under added hits**".
- The cut/monotonicity table is at l.724–731.
- "*S_CKF (Df-9).*" (l.733): credited where tested (R04–R06), carried with s_tot and censored at 1. Option (b) is
  stated.
- The m_H ranges under option (a) (10–890) match script [9b] "P3/P14 EST".
- Df-9 (l.2727) and COM B1-f agree.

**P4: samples of the ceiling and completeness tests. RESOLVED.**
- l.748: "**Ceiling test (one-sided), only on unbiased samples**", with the reason for excluding the enriched overlays.
- l.766: the leak is "an **implementation check**".
- Sub-topologies: "They have no ceiling test" (l.681).
- Development sample 13a, `dev.ovl.dif`, 7 CPU-h (l.2015).
- The pilot's Geant4 vertices: +6.0 CPU-h (script [3] l.37).
- The effective-count form is at l.759–761; I re-derived it, and N_eff = (Σw)²/Σw² with T_eff = N_eff/r̂ leaves the
  rate unchanged.

**P5: the mixed numerator. RESOLVED.**
- l.767–770: "a **paired pile-up-only finder pass** with the term's hits removed … 26 CPU-h". Script [3] has two
  13.0 CPU-h lines (4,000 × 11.7 s each).
- The 0.26 bound is kept as a convention.
- An untested term enters at H′ after a completeness FAIL (§4.0 point 6, l.409–413).
- The expected mixed fraction is a dated day-15 input (§11.7 inputs, l.2626).

**P6: the ceiling family. RESOLVED.**
- §4.4 l.754–758 gives one Šidák verdict per term, with Bonferroni over T_c = 19 terms.
- The §4.0 table row (l.376–377) and §4.12 rule 1 (l.1721) give "6.9–8.9 %"; Df-2 is consistent.
- My check: per-term 0.05/19 + 4α_c² = 0.00266, so the family-wise rate is 1 − (1 − 0.00266)¹⁹ = **0.0493**.
- Combined with the closure family: 1 − (1 − 0.021)(1 − 0.0493) = **0.069**, and with 0.042, **0.089**. Reproduced.
- The human sees this rate in Df-2: "A selection is lost to a false FAIL with 6.9–8.9 %".

**P7: crossing credit. RESOLVED.**
- l.448–452: "**consistency checks with no distance credit** (Df-2)".
- The new row is at l.470, with 1.30 at R14 and 3.68 at R20 (script [12]).
- Every reading that used 0.45–0.49 is corrected (§4.5 l.1107–1109, §4.12 l.1764).
- The v3 row survives only as "withdrawn" in the script.

**P8: the π_k R06-only row. RESOLVED.**
- l.471–472 give 1.41 / 2.51 / 1.42.
- I checked √(0.231² + (0.693·2)²) = 1.405 and √(1.405² + (0.693·3)²) = 2.509.
- The R06–R07 row is kept, labelled conditional.

**P9: "target met". RESOLVED.**
- §4.11 point 3 (l.1571–1577): "**every leading term labelled estimate** … (so a background of 'low count' terms,
  m = 1–3, with σ_ln = 0.26 and f₀ = 0, is not 'target met')".
- The label words are "each printed with the s_tot of the term's route" (l.1566).
- COM TG-1 and §0 l.74 agree.

**P10: Q3 complete. RESOLVED.**
- Q3 (l.2689–2697) names every route: "by planned statistics, by a fluctuation, by the cap rule or by a day-15 rule".
- The annex has routes 1–4 (l.2737–2744). Its fluctuation row reads "**0.30**". My value is 1 − P(Pois(31) ≥ 24)⁴
  = 1 − 0.916⁴ = 0.297.
- The consequence is stated: "Rule 3 may already have spent the reserve, so the top-up can be a reported overrun".
- §4.0 point 6 (l.417–418) is aligned with it.

**P11: T1 coverage family. RESOLVED.**
- §4.11 point 6 (l.1682–1689) and Df-10. COM T1-c and T1-h agree.
- My binomial check gives k_F = 462 at c_ref = 0.95 (P = 0.0046 per check) and 459 at 0.945 (P = 0.0048).
- Without the INVESTIGATE re-test the family-wise rate is 4.5–4.7 %. With the re-test band it is v4's 4.7–4.9 %
  (script [13]). Consistent.

**P12: Q5 premise. RESOLVED.**
- Q5 (l.2707–2713): "content depends on the MET model, the trigger threshold and the generator-cut decision, all
  frozen by day 12 … but on no plane-selection choice and on no signal efficiency at any T2 candidate".
- §4.17 l.2033–2035 says the same.
- The cost of "no" is +47 CPU-h and "+1.8 days". I checked 312/174 = 1.79 days.

**P13: reserve inside the approved figure. RESOLVED.**
- §11.2 l.2434–2435: "**day-15 redirection reserve** … spent by default, so inside the approved figure",
  "**Approved figure** … **5,087 full / 4,574 reduced**".
- Q4 (l.2699–2705), §11.6 (l.2596–2600) and COM ST-1 give 4,574 and 5,946.
- "None of these is inside the approved figure" now refers only to the conditional costs; the contradiction is gone.
- My check: 4,417.1 + 156.5 = **4,573.6**, and 1.3 × 4,573.6 = **5,945.7**.
- The other variants: MUST only 1.3 × 4,140.1 = 5,382; full SHOULD 1.3 × 5,086.9 = 6,613.

**P14: day-15 inputs. RESOLVED** (but see the new B-2 on the pilot's ordering).
- (i) §4.7 l.1296–1300: "**the 4a hit-level campaigns are staged**"; v1-proxy rates "labelled with their errors";
  inventory row 20 (l.2024).
- (ii) §4.4 point 5 l.818–822: "*Reading of the pilot (fixed now).*", Gamma(m + 1), and the rule-3 branch set by
  the R06–R07 pilot counts.
- "Best candidate": rule 1 (l.2635–2637).
- Day 7: "computed **preliminarily at day 7** … binding at day 15".

**P15: B1 trace gaps of cycle 3. RESOLVED.**
- §4.4 l.786–793: "on the **pilot's 1,000 near-pass overlays (sample 11)** … 2–4 classes are expected to qualify.
  If fewer than two qualify, the promotion model is 'not submitted' and the term enters at H".
- §8 item (2) (l.2253–2257) and COM PR-1 add the ceiling test, the completeness bound, c_mix, S_CKF and H′.
- The new trace (Part 3.2) finds a different gap: ordering, not content.

**P16: agent slots. RESOLVED, with a C residual (C-3).**
- §11.3 l.2496–2506: "**Agent slots (finding P16; executors + reviewers + drafter, at most three at a time)**".
- There is one Phase-3 1-bot review (days 16–17).
- The drafter is channel (iii)'s second task.
- The sealed C1 comparison is "run sequentially in this slot".
- My calendar sum (5 + 12 + 2 + 2 + 2,453/174 + 1.5 + 3 + 2 + 3 + 2 + 2 + 3 + 4 + 2) = **57.6 days**. The
  non-production days are **43.5**.
- At no window does the table need more than three concurrent agents for the work it lists.
- Residual (C-3): the table omits the BibTeX validator (4a, 4b), the rendering reviewer (Phase 5), and the note
  writer and typesetter of 4a–5. With three slots these must be sequenced inside the existing 3-day review windows.
  That is feasible (each role is hours of agent time), but it should be written down.

---

## Part 2. The Gate-A section read as the human will read it

I read §12.1 (l.2666–2747) without the rest of the document.

### 2.1 Questions

| Q | self-contained, one-line answer? | default sensible? | alternatives costed (CPU-h, days, reach)? | numbers equal elsewhere? |
|---|---|---|---|---|
| Q1 | yes | yes: sealed tier, 4 open | CPU-h and days yes (14 CPU-h, all options); reach n/a; the information cost ("± 16–23 % at 3 of 20 window points", script GA-1 0.16 / 0.23) is stated | yes |
| Q2 | yes | yes: the pause rule fires before production (day 15 vs production from day 21) | doubled pool: +665 CPU-h, +3.8 d (665/174 = 3.82), floor 6.3, +25 GeV (814 − 790, script [9b]); "always pause": days not given (C-4) | yes, except the B-1 omission |
| Q3 | yes, every route listed | yes | +680 CPU-h (script 682; 103–1,227), +3.9 d (680/174 = 3.91); the reach consequence of the default is not stated (C-5) | yes; 0.30 = script 0.297 |
| Q4 | yes | yes | envelope 6,720 / 8,736; MUST only 4,140 / 57 d (56.7); full 5,087 / 58 d (57.9); all match the script. "[DP1], [DP2], [DP4], [DP5]" are only labels here, and the reason for 58 days against 2–4 weeks is not in Q4 (C-1) | yes |
| Q5 | yes, premise corrected | yes: idle capacity, 0 days | +47 CPU-h, +1.8 d | yes |

### 2.2 Defaults

| Df | sensible? | alternative costed? | consistent? |
|---|---|---|---|
| Df-1 | yes | +827 CPU-h, +4.7 d (827/174 = 4.75); 15 % → 10 % error | yes (script [6], [13]) |
| Df-2 | yes | cap ln F/2.5: 15 % / 6 % (script 0.152 / 0.064); √d distance: 1.1 vs 2.5 (script 1.08) | yes |
| Df-3 | yes | qualitative (a cited treatment is needed) | +3 to +13 % = script [13] |
| Df-4 | yes | +390 CPU-h (script GA-6 391), ≈ 1 week | yes |
| Df-5 | yes | saves 10 CPU-h | yes |
| Df-6 | yes (fixed by the brief) | wording | yes |
| Df-7 | yes | qualitative | yes |
| Df-8 | yes | "+156 CPU-h". §11.2 lists "exact toys in both passes ≤ 236" as a conditional. The two are different cases (switching up front, or switching after a failed check), but a reader sees two numbers for "exact toys" (C-6) | see C-6 |
| Df-9 | yes (the arbiter's technical default) | qualitative | yes |
| Df-10 | yes | the pooled alternative | 462 / 4.7 % = script [13] |

### 2.3 The headline (§0 l.59–71 and the Q2 cell)

| question | answer |
|---|---|
| Leads with the conservative reach? | **Yes for the empty-ceiling branch** (710 at the 84 % edge first). |
| States the lower branch? | **Partly.** "≈ 470–500 GeV" is given, but as the *median* of (α1), unlabelled, directly after an 84 %-edge number. The like-for-like conservative value is **421–455 GeV** (Table 4.4c l.910; script [9b] HEADLINE). The (α2) rows (own R06→R07 fall: ≈ 7.5×10⁴ and ≈ 4,300 events, reach **below 393 GeV**, l.912–913) and the log-normal reading the fixer describes (FR §4 item 1) appear nowhere in §0 or §12.1. → **B-1** |
| 790 GeV only as an upper edge? | Yes: "an upper edge, not the expectation". |
| Day-15 pause a realistic branch? | Yes, in §0 l.71, Q2 l.2684 and §11.7 l.2640. |
| Every reach figure marked as resting on v1 placeholder efficiencies? | Yes: "EST, v1 placeholder efficiencies, best Λ per mass" in §0, in Q2, and in the §12.1 preamble l.2670–2671. |
| "Existing bounds ≲ 180 GeV" | Stated without the caveat that R-20 (the search for ATLAS/CMS non-helical results and HL-LHC quirk projections) is still open. v4 itself requires R-20 "before the paper states 'beyond existing limits'" (l.2170). → C-7 |

### 2.4 Calendar and decision points (Q4)

| question | answer |
|---|---|
| Does Q4 say the calendar is ≈ 8 weeks against 2–4? | Yes: "**58 days** (against your 2–4 weeks)". |
| Does it say *why*? | No. The reason (43.5 days without critical-path production: 19 days of development and freeze, 8 days of ITERATE allowances, Gate B, reviews and writing; compute adds 13–14 days) is in §0 l.83–87 and §11.6 l.2571–2572, not in §12.1. |
| Does it give the first decision points? | No. Day 5 (decision point 1, and stop-rule checkpoint 1 with measured unit costs), day 7 (the preliminary projection) and day 15 (the binding rule 1 pause, the rule 3 reserve routing, the Q3 routes and the redesigns) appear only as fragments in Q2 and Q4. §11.7 has them in full. |
| Classification | A human reading §12.1 alone would approve 58 days without the reason and without the decision-point card. Nothing in Q4 is wrong, so this is **C-1 / C-2**. The Gate-A package in Part 4 supplies both. |

---

## Part 3. Executability, length, and the B1 trace

### 3.1 Length: a cost, not a defect

v4 has 2,842 lines, against the arbiter's target of 2,500.

I looked for the two failure modes that would make length a defect.

*(a) Contradictions between binding statements.*
- The cycle-3 five-place eligibility logic is now stated once (§4.0 point 6, l.399), and §4.11 point 3, §4.12
  rule 1, the partial-outcome table and COM T2-a point to it.
- My numeric grep of user-facing values (4,574; 5,946; 12.6; 6.9–8.9 %; 58 / 57.6 days; 1.41; 2,146) finds them
  identical across §0, §4, §11, §12.1 and COM.
- The one contradiction I found is B-2. Two trivia are not defects:
  - the §11.3 table ends at "57.5" while the text says 57.6 / "58", because the table rounds 14.1 production days
    to 14;
  - the Df-8 / conditional-cost wording (C-6).

*(b) Is the binding statement findable?*
- COM is the master list of identifiers, and every COM row points to its STR section.
- The decision points are in one table (§11.7), the samples in one inventory (§4.17), and the CPU-h in one script.

So length is **a cost, not a defect**. The cost is real: an executor of Phase 2 needs about 15 % of the document,
scattered across §4.1, §4.2, §4.4 point 5, §4.13–4.15, §6.4, §11.3 and §11.6.

Recommendation (orchestration, C-10). After PASS, the orchestrator generates these derived documents, each with
section pointers back to v4 and COM, and each regenerated or checked when v4 changes:
1. the **Gate-A package** (Part 4 below);
2. a **Phase-2 task sheet**: three channels, with day-0 jobs, the pilot, C1/C2, S2, P1, retrievals R-2/R-3 by day 5,
   the checkpoint-1 inputs, and the sealed-tier procedure;
3. a **Phase-3 task sheet**: B1–B4 development, the decision-point-2 inputs and their owners;
4. a **decision-point card**: days 0 / 5 / 7 / 10 / 12 / 15 / 17–19 / 21, each with its inputs, its owner, the rule
   and what it can change;
5. a **NUMBERS register**: every number the human is shown, with its script section;
6. the **inventory as a machine-readable table** (stream names, roles, independence), for `DATA_MANIFEST.md`;
7. the **PREREG skeleton** from §8 and COM PR-1.

### 3.2 End-to-end trace of B1

The chain I followed:
1. per-item section (§4.4);
2. systematic plan (§5.1 rows "Background normalisation" and "Detector simulation model"; SY-5);
3. pre-registration outline (§8 item (2));
4. schedule (§11.3, §11.7);
5. COM (B1-a … B1-g, PR-1, INV-1).

*Consistent links:*
- The terms (DIF, NI × 3) and the estimator formula (l.715) match COM B1-a and B1-f.
- The sample sizes match the inventory:
  - sample 19 is 17,500 = 9,000 DIF + 4,500 NI + 4,000 sub-topologies;
  - the paired pass on "4,000 unbiased B1 test overlays" = 1,000 DIF + 3 × 1,000 NI.
- Costs: §4.4 gives 542 CPU-h, equal to §11.2 (33 + 85 + 424) and to script [4].
- The deadlines are 4a in COM, which matches §11.3.
- The PREREG content matches §8 item (2).
- The systematic rows are present in §5.1.
- The day-15 inputs list (l.2623–2630) names every B1 development output.

*Gap (B-2): the pilot is scheduled before the code it needs.*

v4 says the pilot is complete by day 5:
- §11.7 l.2623–2625: "Inputs: from the pilot (finished by day 5), the ceiling counts m_H per term at every T2
  candidate, read as Gamma(m + 1), the R06–R07 counts …".
- Rule 1 is "computed **preliminarily at day 7** from the finished pilot".
- §4.4 point 5 l.812–817: the pilot measures "f_k and H at R04–R09" and makes "1,000 overlays of near-pass events".

But the code that defines f_k, H and "near-pass" comes later:
- §11.3 l.2484 and the slot table l.2501 put "classes on hit subsets, S_CKF, ceiling and completeness tests on
  development samples, per-k promotion on the pilot's overlays" in **Phase 3, days 5–17, channel (i)**.
- Phase 2's channel (iii) lists only "pilot, T1 builder, Geant4 geometry".
- §4.4 point 2: the hand-over variants are "compared on 100 events in Phase 3 and one is frozen".

Three consequences follow.
- *Lost pilot events.* No-pile-up jobs store only per-event summaries with "the near-pass class" (l.1021–1023; [A4]).
  So either the classifier exists when the pilot runs, or the pilot's 6.3×10⁶ no-pile-up events must be re-run, or
  they must be kept as full records. At FEAS_A's 8.2 kB per minimum-bias event that is ≈ 52 GB, more for hard-scatter
  events [E].
- *Per-k comparison.* It needs the predicted π_k "from the occupancy model of B2 with its measured layer-to-layer
  correlation factors" (l.783–786). That model is built in channel (ii) until day 16 (l.2484).
- *Day-7 pile-up term.* The preliminary projection's pile-up term, "the pile-up estimate of the development occupancy
  model" (l.2633), cannot exist at day 7.

The fix is text only, with no CPU (the pilot is in idle pre-freeze capacity). Each piece needs one sentence:
- Either write the own-hit classifier (k per layer type, all own hits, Df-9) in Phase 2 channel (iii) as part of the
  pilot, or let the pilot's no-pile-up jobs keep full records (≈ 50 GB, inside the storage budget) and classify them
  when the classifier exists.
- State that the day-7 preliminary projection uses the pilot counts available then and the v1-based EST pile-up
  rows of Table 4.4c. Only day 15 uses the development occupancy model.
- State that the per-k comparison runs once the occupancy model's R04–R05 inputs exist, and give the latest day
  (≤ day 15).

This is B because it is a contradiction between two binding statements. It sits under a decision point the human is
told about ("preliminary at day 7"), and an executor at day 0 would hit it. It does not threaten the design: the
day-15 binding rule stays feasible with a pilot re-run.

---

## New findings

### Category A
None. I checked whether B-1 rises to "framing that hides a problem". It does not:
- v4 states the (α2) rows in Table 4.4c;
- v4 states the pause as a realistic branch;
- the omission is in the summary layer only.

### Category B

**B-1. The headline's lower branch is incomplete and mixes statistics.**
- *Where:* §0 l.62, Q2 l.2681–2682, FR §4 item 1.
- *The problem:*
  - The lower branch is quoted as a median, "≈ 470–500 GeV", in the same sentence as an 84 %-edge number for the
    upper branch. The abstract quotes the 84 % edge (§4.11 point 3), and (α1)'s edge is **421–455 GeV**.
  - The (α2) rows (reach below 393 GeV, l.912–913) are omitted, and so is the log-normal reading.
  - FR §4 item 1 says "Both readings are stated in §4.4". The only v4 text is "The uncertainty of these v1-based
    sizes is about a factor e" (l.924–925). Grep for "393" finds only the two table rows.
- *Why B:* the human approves Q2 on this sentence. A downside shown as "≈ 470–500" reads as a floor that v4's own
  table does not support.
- *Exact fix (text):*
  - In §0 and Q2, write "≈ 470–500 GeV median, **421–455 GeV at the 84 % edge**, if decays in flight and conversions
    fall from v1's own R06–R07 counts as the pile-up background does and earn no promotion credit".
  - Add "and below 393 GeV (beyond the plan's reach table) if they fall only as slowly as v1's own 2 → 1 and 13 → 2
    counts suggest, a weak, two-count extrapolation (α2); in both cases the day-15 rule pauses the study before
    production".
  - Add one sentence to §4.4 after l.925 stating the log-normal reading and why the counted-ceiling reading is used.
  - Optionally add (γ) at m_H = 100 (548 [499]) as the SM envelope.

**B-2. The pilot is scheduled before the code it needs.**
- *Where:* §11.7 l.2623–2625 and l.2633–2634; §4.4 point 5 l.812–822; against §11.3 l.2484 and l.2500–2501 and
  §4.4 point 4 l.783–786. Details in Part 3.2.
- *Exact fix:* the three sentences listed in Part 3.2.

### Category C (apply without re-review)

- **C-1.** Q4: add one clause giving the reason for 58 days ("43.5 of the 58 days have no critical-path production:
  development, freeze, reviews with one ITERATE each, Gate B; compute adds 13–14 days"). Give one-line meanings of
  [DP1], [DP2], [DP4] and [DP5].
- **C-2.** §12.1: add a five-line decision-point card (day 5 / 7 / 15 / 17–19 / weekly) with what each can change.
  The text is in Part 4.
- **C-3.** Slot table (§11.3): add the BibTeX validator (4a, 4b), the rendering reviewer (5), and the note writer and
  typesetter (4a–5), sequenced inside the stated review windows.
- **C-4.** Q2 "always pause at day 15 (your turnaround)": state the calendar cost. Use the Gate-B reference of 2
  days, and say that production cannot start before the answer.
- **C-5.** Q3: state the reach consequence of the default ("no credit" terms at H). (β) at m_H = 10–100 gives
  767–695 GeV [706–641]; (γ) gives 701–548 [636–499].
- **C-6.** Df-8 against §11.2: one clause saying that +156 CPU-h is choosing exact toys up front, and ≤ 236 CPU-h is
  switching after a failed f_T check.
- **C-7.** Headline and Q2: "existing bounds ≲ 180 GeV (R-20 pending: a search for ATLAS/CMS non-helical-track
  results and recent HL-LHC quirk projections)".
- **C-8.** r_ττ = 0.17 and 0.34 (Table 4.4a, l.860–862) are [U] planning numbers. Source the branching fractions
  with R-5 before day 12, when the MET model replaces the planning N_trig anyway.
- **C-9.** FR §4 item 1 states something v4 does not contain. Fixers should cite a grep phrase for every
  "stated in" claim, as FR §1 already does elsewhere.
- **C-10.** The derived documents of Part 3.1. This is an orchestrator task after PASS.
- **C-11.** §11.3 table: end the last row at 57.6 (or round the 4a row to 14.1), so that table and text agree.

### Honest-framing check

Is v4 telling the truth about what it will measure and how well? Largely yes:
- it states the bounded outcome as the expectation;
- it keeps 790 as an upper edge;
- it says that the pause may fire;
- it reports v1's failures.

The one residual is the pattern every earlier cycle saw: the summary layer picks the gentler member of a pair (B-1).
With B-1 fixed the headline is honest.

---

## Final judgment

**Not yet. One short focused fix; no new panel needed.**

Exactly what blocks:
1. **B-1:** the lower branch of the headline (§0, Q2, and one sentence in §4.4).
2. **B-2:** the pilot is scheduled before its code (§11.3, §11.7, §4.4 point 4).

Both are text-only, with 0 CPU-h and no change to any number, rule or design. Once they are applied (and the C items
where convenient), v4 is a sound, honest and executable basis for Gate A. The arbiter can verify the fix directly.

---

## Part 4. Final Gate-A package (at most 3 pages; all numbers from v4)

The text below is written as it would read after B-1 and B-2 are applied. The B-1 values are already v4's Table 4.4c
and script [9b] values.

---

### Quirks v2: Gate A (Phase 1 strategy, 2026-11-13)

**Headline (estimates; every reach number rests on v1 placeholder efficiencies, best Λ per mass)**

The expected outcome is a background **bounded by simulation statistics, not estimated**. Its label will be
"target not met: sample-size limited", and it is the default paper, not a fallback.
- **≈ 710 GeV** (84 % edge; median ≈ 790, an upper edge) if every no-pile-up ceiling counts zero.
- **≈ 705 GeV** (84 % edge; median ≈ 770) if Z(νν) is tested and the other SM terms sit at their ceilings.
- **421–455 GeV** (84 % edge; median 470–500) if decays in flight and conversions fall from v1's own counts like the
  pile-up background and earn no promotion credit.
- **Below 393 GeV** if they fall only as slowly as v1's two-count extrapolation suggests.
- **1,026 GeV** for a negligible background.
- Existing bounds are ≲ 180 GeV (search for newer results pending, R-20).

The abstract will quote the 84 % edge. The two lowest branches lie above the **day-15 pause** (projected
B₅₀ > 300 events, reach ≈ 560 GeV). By v1's own record that pause is a realistic branch, not an exception: the
study then stops before production and asks you.

**What Phase 1 established**
- **The chain.** The v1 chain runs on linux-64 with pyacts 48.0.0 and no API change. Stage-1 numerics agree with v1
  to ≤ 1.2×10⁻⁷. Geant4 11.4.3 is installed on all three workers. NLO K = 1.165 at m_E = 200 GeV from a built
  `loop_quirkE` model. MG5 Z(νν)+jet gives 12.21 pb against v1's 14.6 pb. The resumable runner passes.
- **Measured costs** (i5-7500 worker, 4 jobs per node):

  | unit | cost |
  |---|---|
  | pile-up-200 event | 13.5 s |
  | finder trial | 11.7 s |
  | four-trial event | 60.4 s |
  | no-pile-up interaction | 11.5 ms |
  | Geant4 π gun | 0.134 ms |
  | Pythia shower | 21–23 ms |
  | string event at 1 / 3 / 5 keV | 0.65 / 18.8 / 67.8 s |
  | Argo overhead | 17 s per job |

- **Not measured.** The 45 ms no-pile-up hard-scatter event is a guess, and ρ = 2 (206 s, 1.46 GiB) rests on one
  event. **1,378 CPU-h rest on unmeasured unit costs.**
- **Capacity.** 10 usable off-hours slots give 1,625 slot-h per week. Assumed effective capacity: 174 core-h per
  production day and 116 per development day (utilisation measured in week 1).
- **Why v2 cannot prove a small background by counting alone.** A zero count in every term still allows **≈ 13
  events** (12.6 for the pool terms plus 0.46 for multijets; predictive median 10.8, 16–84 % 7.7–15.2). Reaching 1
  event by sample size would need ≈ 8,400 CPU-h. So v2 adds tested estimators, tested ceilings H and the day-15 rule.

**Your five questions** (answer e.g. "Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ●"; ● = recommended)
- **Q1, C1 blinding exception.** May the v1 reproduction compare six v1 signal counts that are also v2 candidate
  efficiencies, before the closure verdicts?
  - ● Yes, sealed: PASS/FAIL only until Gate B, four counts open.
  - Alternatives: all ten open and disclosed; or the six dropped.
  - 14 CPU-h in every option.
- **Q2, the bounded paper as the default.** Proceed to production with the headline above?
  - ● Yes, pausing only if the day-15 projection (preliminary at day 7) exceeds B₅₀ = 300 events, or both pile-up
    estimators miss their cap.
  - Alternatives: always pause at day 15 (≈ 2 days of your turnaround; production waits); or a doubled pool
    (+665 CPU-h, +3.8 days, floor 6.3, ≈ +25 GeV only if the ceilings are empty).
- **Q3, brief D4 exception.** For every MUST closure test that ends untested (planned statistics: the eight proxied
  SM processes and the three additions; a fluctuation of the four supplied terms, ≈ 30 %; the cap rule; B3 and B4-e;
  B2-c at depth), may the term enter at no credit (its tested ceiling H), labelled "no credit"?
  - ● Yes. Expected reach effect: 767–695 GeV median for ceilings of 10–100 counts.
  - Alternatives: comply where costed (≈ +680 CPU-h, 100–1,230, +3.9 days); or strict, where "closure fails"
    becomes a likely paper.
- **Q4, budget, calendar, stop rule.** Approve **4,574 CPU-h** and **58 days**?
  - ● Approve. The stop-and-ask threshold is **5,946 CPU-h**.
  - Why 58 days against your 2–4 weeks: 43.5 days have no production (development and freeze 19; one ITERATE
    allowance per panel review, 8; Gate B, reviews and writing). Production adds 13–14 days.
  - The downscopes it includes:
    - **[DP1]** B5 sideband at 8 roads (−358 CPU-h; R07 not closed with pile-up);
    - **[DP2]** B6 at 4 signal points (−155 CPU-h; no scalar or 1.5 TeV variation);
    - **[DP4]** no S4/S5;
    - **[DP5]** Herwig at generator level after an install attempt.
  - The contingency (2,146 CPU-h) and the conditional costs are not pre-approved; every draw is reported. If all
    guesses double, the total is 5,952, so the stop rule may fire at day 5 or at the freeze.
  - Alternatives: the envelope 6,720 (threshold 8,736); MUST only, 4,140 CPU-h and 57 days; full SHOULD, 5,087
    CPU-h and 58 days.
- **Q5, the D7 reading.** May the truth-level signal samples (47 + 266 CPU-h) exist before the pre-registration hash?
  They depend on the MET model, the trigger threshold and the generator cut (all frozen by day 12), and on no
  selection and no efficiency.
  - ● Yes (idle capacity, 0 days).
  - Alternative: after the hash, +47 CPU-h and +1.8 days.

**Ten defaults** (reported; override any). These are v4 §12.1 Df-1…Df-10 verbatim with their costs, chiefly:
- **Df-1:** 2,000 signal rows per point (4,000: +827 CPU-h, +4.7 days).
- **Df-2:** closure rules; a correct analysis loses a selection to a false FAIL with 6.9–8.9 %.
- **Df-8:** toys parametrised in f_T (exact toys everywhere: +156 CPU-h).
- **Df-9, Df-10:** technical.

**Budget and calendar**

| variant | CPU-h approved | 1.3× stop threshold | 4a production days | calendar |
|---|---|---|---|---|
| MUST only | 4,140 | 5,382 | 13.2 | 56.7 d |
| **MUST + reduced SHOULD (proposed)** | **4,574** | **5,946** | **14.1** | **57.6 d ≈ 8 weeks** |
| MUST + full SHOULD | 5,087 | 6,613 | 14.4 | 57.9 d |

Range: 49 days (MUST only, every review passes at once) to 65 days (50 % utilisation), plus 8 days if each panel
review needs two ITERATE cycles.

Milestones: Phase 2 days 0–5; Phase 3 days 5–17; freeze and hash days 17–21; production days 21–35; 4a review
≈ day 37–40; **Gate B ≈ day 49**; **Gate C ≈ day 58**.

Storage: ≈ 420 GB (620 GB at cap) against 1.5 TB.

**First decision points after Gate A**

| day | what is decided | what it can change |
|---|---|---|
| 5 | Decision point 1 (C1 reproduction, finder checks) and stop-rule checkpoint 1 (measured unit costs fix 870 of the 1,378 guessed CPU-h) | a C1 failure moves everything day for day; the re-projection may trigger stop-and-ask |
| 7 | Preliminary day-15 projection from the pilot (H counts, R06–R07 counts), reported in `STATUS.md` | informs you early; binds nothing |
| 15 | Binding decision point 2: projection for every term with measured ceilings and MET-model N_trig | **pause and ask you** if B₅₀ > 300 or both pile-up estimators exceed their cap; routes the 156 CPU-h reserve (pool or the leading term's test); sizes the staged SM samples; estimators above their cap are redesigned (the freeze moves) or "not submitted" (Q3) |
| 17–19 | Freeze and hash of `PREREG_v2.md`; stop-rule checkpoint 2 | you are notified; no production before the hash |
| weekly | Ledger re-projection during production | any overrun is reported; > 5,946 CPU-h stops the study |

**Top risks**
1. The ceilings count, or decays in flight behave as in v1. The background is then hundreds of events and the study
   pauses at day 15.
2. Unmeasured unit costs (1,378 CPU-h) push the projection past 5,946 at day 5 or at the freeze.
3. Both pile-up estimators fail, so nothing beyond R07 is eligible ("closure fails" paper).
4. No public MET parameters from two sources. B4-b is infeasible and the study stops for you.
5. Phase-3 development needs more than 30 channel-days. Each 3 more lengthen Phase 3 by 1 day.
6. Cluster incidents, and ρ = 2 memory (one job per node in the worst case).

**Files**
- Strategy: `analyses/quirks_v2/phase1_strategy/outputs/STRATEGY_fiona_2026-11-13_23-05.md`. §0 is the summary,
  §11 the schedule, §12.1 the full questions and annex.
- Commitments: `analyses/quirks_v2/COMMITMENTS.md`.
- Every number: `python3 -I analyses/quirks_v2/phase1_strategy/src/strategy_budget.py`.
- Reviews: `analyses/quirks_v2/phase1_strategy/review/` (cycles 1–4, arbiter verdicts).
