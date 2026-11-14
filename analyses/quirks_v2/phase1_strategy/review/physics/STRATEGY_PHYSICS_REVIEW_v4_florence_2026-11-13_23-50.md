# Physics review, cycle 4: STRATEGY v4 (`STRATEGY_fiona_2026-11-13_23-05.md`), Phase 1, quirks v2

Reviewer: Florence (physics reviewer, fresh to the panel), 2026-11-13 23:50.

**What I read.**
- In full: `agents/physics_reviewer.md`, `outputs/FRAMING.md` and the artifact (l.1-2842, in consecutive chunks).
- The cycle-3 physics review (Estelle), the cycle-3 arbiter verdict (Felix, P1-P16) and the fixer's report. I treated
  the fixer's claims as pointers only.
- Opened to check claims: `src/strategy_budget.py` l.545-760 (projection code). I reran it in full (exit 0, output
  saved in the scratchpad), and also `COMMITMENTS.md` rows TG-1, T1-c, T1-h.
- I did not read the methodology or conventions files.

**Own arithmetic.** `python3 -I`, standard library. For the (α) variants and the m_H = 1000 row I imported the
script's own `pmf_pred` / `s95_pmf` / `reach_of`, so the method is the same as the artifact's. Scripts are in the
session log.

**Conventions.** "l." = line of v4. Classes: **A** would give a wrong or indefensible result; **B** must be fixed
before approval; **C** suggestion.

---

## Part 1. Verification of the P findings with physics content

Summary:
- **14 RESOLVED, 1 PARTIALLY RESOLVED (P2), 0 NOT RESOLVED.**
- P16 is agent scheduling, not physics, and I did not assess it.
- P13 is checked as arithmetic only.

| # | status | v4 location, quoted phrase | my check |
|---|---|---|---|
| **P1** Z(ττ), lost-lepton Z without pool share | **RESOLVED** | Table 4.4a l.853-858; l.860-868 "All three are guesses until the MET model gives N_trig at day 12; **the pool shares are then re-allocated**"; §11.7 rule 6; §4.17 rows 18a/18b `prod.hs0.ztt`, `prod.hs0.zll`; rule 1 "for every term of the likelihood" | Independent re-allocation, M_t ∝ √(N_t/c_t) inside 665 CPU-h, with my own code. Results: pool floor **12.60** (DIF 3.04, Z(νν) 2.60, Z(ττ) 0.34, Z(ℓℓ) 0.09); low/high planning N_trig 12.18 / 13.26. Multijets 1.14 × f × N_trig/10⁶ = 0.05 / 0.47 / 4.66 at f = 0.1 / 1 / 10 %. Headline 12.6 + 0.46 = **13.0**, range 12.2-17.8 (13.25 + 4.56 = 17.8). Everything reproduced. **Planning inputs:** both are tagged and used only for planning and the Q3 annex floors: the multijet 1 % (0.1-10 %) is [E], and r_ττ = 0.17 is [U] (l.861). The replacement rule exists and is dated: the MET-model N_trig at day 12 replaces all three (l.863-864; §11.7 inputs, l.2627-2628), and the shares are re-allocated before any pool event exists (rule 6). Once the MET model runs on generated Z(ττ), the ratio 0.17 is no longer used at all. For the record, 0.17 agrees with the ratio of the PDG Z→ττ and invisible widths (≈ 3.37 %/20.0 % = 0.168). That is my recollection, not a citation, and [U] is the right tag. Small wording slip: C4. |
| **P2** honest headline | **PARTIALLY** | §0 l.54-71; Q2 l.2679-2687; Table 4.4c l.899-914; l.916-925 | The structure is now right: the 84 % edge first, 790 called "an upper edge, not the expectation", (α), (β), (γ), the caveats, and "a realistic branch, not an exception". I reproduce every row: (α1) DIF 384/648, conversions 183/308, B₅₀ 587-975, median 469-504, 84 % edge 421-455. **What remains** is a defect in the pessimistic number itself, plus two labelling errors in the same sentence. See **B-1** below. On the two readings asked about: the counted-ceiling reading (Gamma(m+1) on the pool share) is the physically correct one for what v2's likelihood would carry. The factor-e is a planning uncertainty on the *size*, not a width that v2 would carry, and the script labels it so (l.683). The log-normal reading giving < 393 GeV is not stated in v4 (grep: "393" appears only in the α2 rows), but nothing is lost, because it is not the right reading. The physics problem is not which width to use. It is which *fall* is used (B-1). |
| **P3** CKF in H | **RESOLVED** | §4.4 point 4, cut table l.724-731, "*S_CKF (Df-9)*" l.733-743; Df-9 l.2727; §8 l.2253-2254 | Each monotonicity entry is correct. Layer counts and the widest-holding ribbon are monotone under a superset of hits. The road and barrel conditions enter as the search region of a supremum. Fit probability, shapes, CKF removal and f_CKF are not monotone. With H classified on all own hits before CKF, and S_CKF ≤ 1 censored, P ≤ H holds for every cut, so H is a true ceiling. The limiting cases (no pile-up: P = P_geo·S_CKF; saturation: P = H) are right. The m_H EST (2-18 with CKF; 10-890 under option (a)) is reproduced from script [9b]. Note that this new estimate bears on the headline (B-1, point 3). |
| **P4** ceiling/completeness samples | **RESOLVED** | l.748-763 "**only on unbiased samples**"; l.765-766 "an **implementation check**"; l.681-683 sub-topologies "have no ceiling test"; row 13a l.2015; "*Weighted samples*" l.759-761 | The enriched overlays now serve only S/π_k, so the by-construction pass is gone. Effective-count form checked: with N_eff = (Σw)²/Σw² and T_eff = N_eff/r̂, the rate is r̂ and the precision is N_eff; for equal weights T_eff = T/w (correct). The substitution p = 0.0011 / 0.55 is reproduced by the script. |
| **P5** mixed numerator | **RESOLVED** | l.767-781 "**paired pile-up-only finder pass**"; §4.0 pt 6 l.409-413 "extended ceiling H′"; §11.7 inputs l.2626 | The subtraction mixed(with term) − mixed(term hits removed) is a well-posed estimator of the candidates that need the term's hits. The 0.26 bound is declared a convention, c_mix is always applied, and the post-FAIL entry H′ is defined. See C3 on the size of H′. |
| **P6** ceiling family | **RESOLVED** | l.754-759 "One verdict per term … Šidák"; l.362-364 T_c = 19; table l.376-377; §4.12 rule 1 l.1721; Df-2 | Re-derived: α_c = 0.05/19, per-term size at the boundary α_c(1 + 4α_c), family 1 − (1 − ·)¹⁹ = **4.93 %**. Combined: 1 − 0.979·0.951 = 6.9 %, 1 − 0.958·0.951 = 8.9 %. Šidák over nested rungs is conservative, as stated. The term count 1 + 3 + 14 + 1 = 19 is correct. |
| **P7** crossing credit | **RESOLVED** | §4.0 pt 7 l.447-454 "**consistency checks with no distance credit** (Df-2)"; table row l.470; §4.5 l.1107-1109 | Recomputed: 0.43 / 0.59 / 1.29 at R08 / R09 / R11; 1.30 at R14 with a 2S PASS (√(1.29² + 0.135²)); 2.47 / 3.68 at R17 / R20 (d_out = 6, 9). The width-step from the last crossing rung to R08 is kept. The by-construction credit is gone. |
| **P8** π_k R06-only row | **RESOLVED** | table l.471-474; checks l.478-482; §4.12 l.1765-1766 | √(0.231² + (2·0.693)²) = **1.405**; at R14 √(1.405² + 9·0.693²) = **2.509**; with a 2S PASS √(1.405² + 0.231²) = 1.424. The text draws the right conclusion: a promotion credit is "useful only if π_k itself is small". |
| **P9** "target met" | **RESOLVED** | §4.11 pt 3 l.1571-1577 "**every leading term labelled estimate**", including the low-count example; COM TG-1 l.188; l.1566-1567 "each printed with the s_tot" | Correct. A low-count background with σ_ln = 0.26 and f₀ = 0 is now explicitly not "target met". |
| P10 Q3 routes | **RESOLVED** (physics part) | annex l.2730-2747; route 1 "**0.30**" | P(Pois(31) ≥ 24) = 0.9156; 1 − 0.9156⁴ = **0.297** (reproduced). Every route has a stated consequence. |
| **P11** T1 coverage family | **RESOLVED** | §4.11 pt 6 l.1682-1689; Df-10; COM T1-h l.147 | Exact binomial (my code): the largest k with P(X < k \| 500, 0.95) ≤ 0.005 is **462** (P = 0.46 %), and 459 at c_ref = 0.945. The INVESTIGATE band runs to the one-check 5 % point (462-466 / 459-463). With one re-test the per-check size is 0.48 / 0.50 %, so the family of 10 is **4.7 / 4.9 %**. A true coverage of 0.90 passes with 0.6 / 2.7 %. All reproduced. Comparing with c_ref (the convention's own computed coverage) is an implementation test, not a coverage claim. That is acceptable, because the 0.945 under-coverage is itself reported (l.1604-1608). See C6. |
| P12 Q5 premise | **RESOLVED** | Q5 l.2707-2710; §4.17 l.2033-2035 | The premise now names the MET model, the trigger threshold and the generator-cut decision as inputs. It is accurate. |
| P13 reserve inside approval | **RESOLVED** (arithmetic) | §11.2 l.2434-2435; Q4 | 4,417 + 156 = 4,573 ≈ 4,574; × 1.3 = 5,946. |
| P14 day-15 inputs | **RESOLVED** | §4.4 pt 5 l.818-822 "*Reading of the pilot (fixed now)*"; §4.7 l.1296-1300 staging; §11.7 rule 1 l.2631-2640 | One pilot count is 10.9 events, so a pilot zero is 1.14 × 10.9 = 12.4 events (correct). The branch is set by the pilot's R06-R07 counts with **the pilot's own fall**, which is physically the right extrapolation. Note that the headline does not use it (B-1). |
| P15 B1 trace | **RESOLVED** | l.786-794 "**pilot's 1,000 near-pass overlays (sample 11)**"; §8 l.2253-2257 | 24/250 = 0.096 and 24/125 = 0.19, so the "π_k above 0.10-0.19" threshold for a qualifying class is right. The "not submitted" fallback is defined. |
| P16 | not assessed | §11.3 slot table | Process and scheduling, outside the physics remit. |

---

## Part 2. Final physics sanity pass

### Checks that pass (recomputed)
- **Floor and its re-split.** See P1. The predictive median 10.8 and the 16-84 % range 7.7-15.2 (script [9]) are
  consistent with 19 summed exponentials. σ_ln = 0.34 is described honestly as "small because nineteen independent
  bounds are summed, not because anything was measured".
- **(α) inputs.** I recomputed the DIF and conversion values at R07 from N_t × count/500. DIF: 6.51×10⁷/500 =
  1.30×10⁵. Conversions: 4.0848×10⁷ × 0.379 × 2/500 = 6.19×10⁴. The R08 values follow at ×339 / ×201.
- **Ceiling, coverage and closure family rates.** See P6 and P11.
- **Pile-up cap.** The pile-up cap is drawn as 426 × Exp(1) (Ph-C9). Its effect on the R08-like row (527 → 496 GeV)
  is the expected direction.
- **Regression check of this cycle's fixes against each other.** π_k, the occupancy widths and the ceiling family are
  propagated consistently into §4.0, §4.5, §4.12, Df-2 and §8. No stale value is used as a current one. The only
  cross-fix tension I find is in B-1 point 3: the new Df-9 m_H estimate against the headline.

### B-1. The pessimistic number of the headline rests on a fall that v1's own counts reject for the conversions; the sentence also mislabels its numbers (§0 l.54-64; Q2 l.2680-2682; Table 4.4c l.910-913, l.916-925). This is the residual of P2.

1. **The (α1) assumption is contradicted by v1's record, and the text's reason for setting (α2) aside is wrong for
   the conversions.**
   - (α1) lets DIF and the conversions fall from R07 to R08 by the random pile-up factor (×201-339 per width step).
     v1 measured the conversions' own fall twice, on the same attributed full-pile-up samples (Table 4.4b, γ
     153/86/13/2 per 500):
     - ×6.6 from R05 to R06, on 86 → 13 counts;
     - ×6.5 from R06 to R07, on 13 → 2.
   - If the conversions fell like pile-up from R06, v1 would have expected 13/339 to 13/201 = 0.04-0.06 counts at
     R07. P(≥ 2 counts) = **7×10⁻⁴ to 2×10⁻³**.
   - For DIF (2 → 1 counts) the corresponding probability is 0.6-1.0 %.
   - l.920 calls (α2) weak because it is "measured on 2→1 and 13→2 counts". For the conversions the R05→R06 fall on
     86 → 13 is an independent and statistically solid measurement that agrees with ×6.5.
   - The two caveats that could lower (α) (PV placement, attribution rule) do not apply to the hard-scatter
     conversions, as l.924 itself says. The attribution rule acts mainly on the level of the counts, not on the ratio
     between two rungs counted under the same rule.
2. **What the document's own rules give.**
   - Physics: under "no credit" a term enters at its ceiling H. The width dependence of H is the term's own
     no-pile-up physics, not the combinatorial fall. The pilot reading of §4.4 point 5 and rule 3 correctly use "the
     fall per width step that the pilot itself measures". The headline should use the same logic.
   - My recomputation, with the script's own functions: DIF at (α1) plus conversions at their own measured fall
     gives about **9.5×10³ conversion events and B ≈ 1.0×10⁴ in total at R08-R09 without credit**. s₉₅ is about 200,
     so the reach is **≈ 390-395 GeV**, at the bottom edge of the plan's table.
   - With v1's pile-up fit-probability fraction as credit (width 0.43) I get B₅₀ ≈ 580-600 and a median reach still
     **below 393 GeV**, because the credit carries its width.
   - By the same token the conversion part of H for Z(νν) alone would be of order 10³ simulated counts at R08 (0.23
     road photons per event × 0.004/6.5 per photon × 1.1×10⁷ events). That is far above the day-15 class limit of
     m_H ≈ 125.
   - So for the conversions, by v1's own record, the day-15 pause is the **expected** branch, not only a realistic
     one.
3. **The sentence mislabels its numbers.**
   - (a) §0 quotes the empty-ceiling case at the 84 % edge (710) but the (α) case as medians (470-500, whose 84 % edges
     are 421-455). In one sentence this reads as like-for-like and understates the spread.
   - (b) §0 says (α1) means "earn no promotion credit". But falling at the pile-up rate *is* promotion-type behaviour
     (the candidates are pile-up-completed). The scenario's "no credit" is the fit-probability conditional (l.56,
     l.919, script label). The phrase is self-contradictory.
   - (c) P3's new planning estimate (Df-9 option (a), the default: m_H = 10-890 for Z(νν), pilot 2-190 counts) means
     the empty-ceiling case at the head of §0 is not expected even by the strategy's own planning. The headline should
     say so in one clause.
4. **Why B and not A.** No result is computed from this. The binding day-7/day-15 rule uses the pilot's own counts and
   own fall, and it would catch it. Table 4.4c shows (α2). But Q2 asks the user to approve "production without a
   pause" on this headline, so the numbers put to the user must be the honest range. This is exactly the defect P2 was
   meant to close.
5. **What "fixed" looks like (text and one script row, 0 CPU-h).**
   - (i) Add to [9b] and Table 4.4c the row "DIF (α1), conversions at their own measured fall (×6.5 per width step,
     86 → 13 → 2)", without and with credit.
   - (ii) In §0 and Q2 give the pessimistic edge as that row: "≈ 390 GeV or below if the conversions fall as v1
     measured them; ≈ 470-500 (84 % edge 420-455) if they fall like the pile-up background, which v1's counts
     disfavour (p ≈ 10⁻³)". State that the day-15 pause is then the expected branch.
   - (iii) Quote every number at the same quantile, or label each.
   - (iv) Replace "no promotion credit" by "no fit-probability credit".
   - (v) Add the clause that Df-9 planning puts Z(νν) at m_H = 10-890 (reach 720 → ≈ 410-490, median), so the
     empty-ceiling row is an upper edge.
   - (vi) Correct l.920 ("therefore weak") for the conversions.

### C items
- **C1. (β) premise in §0.**
  - §0 quotes "≈ 770 GeV (84 % edge ≈ 705) if Z(νν) is tested" without saying that (β) puts Z(νν) at its
    *zero-count floor* (script label "tested and credited (at its floor)").
  - Under Df-9, a credited Z(νν) still carries S_CKF and π_k at s_tot = 1.41 from R08 on.
  - Add "(Z(νν) at its floor)".
- **C2. The m_H = 1000 row is fixed-B.**
  - With the count width, as in the other rows, I get B₅₀ = 2,300, s₉₅ ≈ 171 and a median reach ≈ 410 GeV. Table
    4.4c quotes ≈ 490.
  - The row is labelled "fixed B", but quoting it as ≈ 490 overstates the reach by ~80 GeV. Compute it like the other
    rows.
- **C3. Size of H′.**
  - H′ = P_geo + Σ_all k f_k extends to every deficit. For SM events with ~30 prompt pairs in the road it may be
    orders of magnitude above H.
  - Give an EST (from the C1 Z(νν) development sample). Then the user knows that "eligible, flagged" after a
    completeness not-PASS of a leading term is in practice a loss of that selection.
- **C4. Wording.** "the additions raise it by 1.1 %" (l.865): the two Z additions do; with the multijets at 1 % it is
  2.1 %.
- **C5. Fit-probability credit for the (α) terms.** v1's 2/35 is the *pile-up* conditional fraction. For genuine
  topologies (kinks, conversion pairs) the out-of-plane fit probability can differ in either direction. Label the
  "with credit" (α) rows accordingly.
- **C6. c_ref for the multi-term workspace.** State how c_ref is computed for the actual workspace: the one-bin
  analogue at the leading term's κ with the other terms fixed, or by exact enumeration. Otherwise a FAIL could reflect
  the analogue, not the implementation.
- **C7. Multijet ceiling test.**
  - The ceiling test sets the MET-selected, weighted hit-level sample against H from the loose (no-MET) population.
  - It therefore also tests the B4-e factorisation. Say so, and charge a FAIL to the factorisation first.

---

## Overall judgment

**Not yet. The only blocker is B-1, a text-and-one-row fix with no CPU. A short focused fix is enough; another full
panel is not needed.**

**Verification counts.**
- 14 RESOLVED, 1 PARTIALLY (P2), 0 NOT RESOLVED; P16 not assessed.
- New findings: A = 0, B = 1 (B-1, the P2 residual), C = 7.

v4 resolves the cycle-3 work list well:
- P1's re-split and floor reproduce exactly. The planning inputs are labelled and have a dated replacement rule.
- H is now a true ceiling by an explicit monotonicity argument (Df-9).
- The tests that passed by construction are gone: the enriched-overlay ceiling tests, the occupancy crossing credit,
  and "complete by construction".
- The mixed count is well posed.
- Every family-wise rate I recomputed (ceiling 4.9 %, combined 6.9-8.9 %, T1 coverage 4.7-4.9 %, fluctuation route
  0.30) matches.
- Nothing in the design is wrong at the root, and the decision rules are physically sound. The pilot reads its own
  fall, which is the point B-1 asks the headline to follow.

What remains is the number put to the user at Q2:
- Its pessimistic edge assumes the conversions fall like random pile-up. v1's own counts reject that at p ≈ 10⁻³.
- With their measured fall, the no-credit background is ≈ 10⁴ events and the reach ≈ 390 GeV. That is still above
  the existing bounds (≲ 180 GeV), but well below the 470-500 GeV quoted.
- Once B-1 is fixed as specified, I would approve for execution subject to Gate A.
