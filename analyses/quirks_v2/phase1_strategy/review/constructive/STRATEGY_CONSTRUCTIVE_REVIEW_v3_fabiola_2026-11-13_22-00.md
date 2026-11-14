# Constructive review, cycle 3: Phase 1 STRATEGY v3 (quirks v2)

Reviewer: Fabiola (constructive, new to the panel; I saw neither earlier cycle), 2026-11-13 22:00. I followed the role file
`agents/constructive_reviewer.md` and its Prompt Template in full, including the honest-framing check.

**What I reviewed.** `phase1_strategy/outputs/STRATEGY_emeric_2026-11-13_21-10.md` ("v3", 2,674 lines), read in full in
nine consecutive chunks, and `COMMITMENTS.md` ("COM", 193 lines), read in full.

**What I also read.**
- `AGENT_RULES.md`, the study `CLAUDE.md` and the phase `CLAUDE.md`, and `FRAMING.md`.
- The cycle-2 arbiter verdict (Eloise, N1–N18), the cycle-2 constructive review (Edmund) and the fix report (Emeric). I
  treated the fix report's claims as claims to check, not as evidence.
- `prompt.md` §2–§5, the `LOG.md` constraints, and PLAN l.100–131 and l.494–545.

**How I checked the numbers.**
- I ran `python3 -I src/strategy_budget.py` with standard-library Python only, writing its output to my scratchpad. It
  exits with 0 and takes about 4 s.
- My own arithmetic is in two standard-library scratch scripts. I cite them as **[R]**.
- I re-derived independently the following: the floors-only one-bin limits, the s₉₅→reach mapping, the widths of
  §4.0 point 7, the per-test FAIL rate at the cap, the censored mean and the B4 sample sizes.

**Rules followed.** No sub-agents were spawned and no git commands were run.

**Tags and categories.**
- Tags: [V] means I read the number at the cited line or re-derived it; [E] means an estimate, with its arithmetic.
- "l." is a line of v3.
- Categories: **A** = genuine error, a criterion that cannot work, or framing that hides a problem; **B** = must be
  fixed before PASS; **C** = improvement.

---

## Summary

v3 is a careful and largely successful fix. Every number I recomputed is right:
- the widths;
- the size and power of the closure rule;
- the B4 sample sizes;
- the summed floor and its predictive distribution;
- the s₉₅ → reach mapping.

The "target met" loophole for bounds is closed. The headline is stated before anything runs, with the right label
("target not met: sample-size limited"). The decision rules for day 5 and day 15 exist and are mostly evaluable. Of
the 11 items I had to verify, 8 are RESOLVED, 2 are PARTIALLY RESOLVED and 1 is properly at Gate A.

What remains is of two kinds.

**1. One genuine gap in the headline (A).** Two of the three new B4 terms, Z(ττ) and lost-lepton Z(ℓℓ), are required by
§4.7 point 3 to have their P_geo and H counted "on no-pile-up hard-scatter events of each process". But the no-pile-up
pool, Table 4.4a, Table 4.4c and the budget cover only the twelve old processes. On their 2,000 hit-level events
alone, a zero count leaves a floor of 57–740 events for an N_trig of 10⁵–1.3×10⁶ [R, E]. That is larger than the
whole projection that §0 and Q2 put in front of the human. The fix is cheap: a pool share of about 10–40 CPU-h, plus
one EST row in each table.

**2. The headline and the decision rules lean optimistic, or are hard to execute (B).**
- §0 and Q2 lead with "about 790 GeV". That is the median for the case where every ceiling is empty. v3's own rules
  say two things against it: the empty-ceiling case is "not the expectation" (l.801–802), and for f₀ > 0.5 the 84 %
  edge is quoted first as the conservative value (l.1399–1401, l.806–809). That edge gives about 720 GeV.
- The ceiling scenario of Table 4.4c is computed for Z(νν). That is the one large term v3 expects to *test*. The terms
  v3 expects to enter at H are the eight proxied processes and the additions, and they are not projected.
- TG-1 can still read "target met" when every leading term is "low count" (1–3 counts).
- Two inputs of the day-15 rules have no sample that can deliver them. One is the R06 rates of the eleven small SM
  processes. The other is a pilot ceiling count that is resolvable at the R09 width.
- The Phase-3 plan fills the cap of three agents with three channel executors, and then also schedules the reviews,
  the PREREG drafter and (in Phase 2) the sealed-comparison agent inside it.

**Proportion.** None of these needs a redesign. The total fix is about half a day of text and at most about 50 CPU-h.
The length (2,674 lines) is itself a risk for Phases 2–3: three of the end-to-end traces below found contradictions
between sections. I propose cuts of about 300 lines, and four short derived documents that the orchestrator should
produce from v3 before Phase 2 starts.

**Counts.**

| | count |
|---|---|
| Verification: RESOLVED | 8 |
| Verification: PARTIALLY RESOLVED | 2 |
| Verification: NOT RESOLVED | 0 |
| Verification: GATE A | 1 |
| New findings: A | 1 |
| New findings: B | 6 |
| New findings: C | 12 |

---

## Part 1. Verification of the cycle-2 constructive items and the three cycle-1 items left partly resolved

The merged numbers are the arbiter's, Edmund's ids are in brackets, and the location column gives the v3 location.

### N3 [N-A1]: "target met" earned by bounds

**Status: RESOLVED.**

**Location:** §4.11 point 3, l.1384–1402; COM TG-1 l.165; §0 l.58–59; Q2 l.2476.

**My check:**
- The reading needs σ_ln ≤ 1, f₀ ≤ 0.5 and no leading bound or no-credit term.
- The all-bounds case has σ_ln = 0.36 and f₀ = 1, so it reads "target not met: sample-size limited" [V: script [9] and
  my convolution, which gives B₁₆/B₅₀/B₈₄ = 6.7/9.6/13.8].
- The expected R09-like case has f₀ = 10.3/17.3 = 0.60 [R], which also reads "not met: sample-size limited".
- σ_ln now has one definition (l.1384), and w_m is named separately.
- A neighbouring hole remains, with "low count" terms. It is new finding F-B3.

### N7 [N-B1]: the projection omits H and the pile-up term

**Status: PARTIALLY RESOLVED.**

**Location:** §0 l.39–62; Table 4.4c l.778–809; §11.7 rule 1 l.2431–2435; Q2 l.2476; pilot l.725–730.

**What is done:**
- The projection is max(floor, N_t·H), with an EST pile-up term (88–148 / 5.0–8.5 / 0.48–0.81 events at R08 / R09 /
  R11, [V: script [9b]]).
- I reproduced the floors-only row exactly by convolving the sixteen geometric marginals: s₉₅ = 6.5 / 9.9 / 15.0.
- I reproduced the mapping: a fixed B = 17 gives s₉₅ = 9.9, and so 834 GeV.
- I checked the m_H = 100 row: B ≈ 101 × 2.2 + 8 + 7 ≈ 237 events, and s₉₅ ≈ 1.96 × √(237 + (0.1 × 237)²) ≈ 53,
  against 53.5 in v3 [R].
- The other requested pieces are all present: the bounded paper as the default deliverable, the bracket, the change of
  the bound (3.7–4.7 decades), the R07-direct size (1.6×10⁵) and the enlarged pilot (2.3×10⁶ Z(νν), 28.8 CPU-h).
- The leak test of N-B1 (iii) is now the completeness test (l.686–698).

**What remains (three new findings):**
- F-A1: two terms are missing from the projection.
- F-B1: the headline leads with the optimistic edge.
- F-B2: the ceiling scenario is applied to a term that is expected to be tested.

### N5 [N-B2]: widths contradict the strategy's own rule

**Status: RESOLVED.**

**Location:** §4.0 point 7, l.391–447; table l.428–435.

**My check, by hand from s_tot² = s_model² + Σs_f² + (b̂² + σ_b²)d_in² + b₀²d_out², with s_model at the cap:**
- Occupancy model: 0.135² + 0.405² gives 0.43 at R08. Adding d_out = 1, 3, 6, 9, 12 gives 0.59, 1.29, 2.47, 3.67 and
  4.88 at R09, R11, R14, R17 and R20 [V].
- π_k: 0.231² + 0.693² gives 0.73. With d_out = 3 in the 2S family it is 2.20. With d_in = 3 (NI tested at R05) it is
  2.09 [V].
- Conditionals at 2, 5 and 7 rungs: 0.82, 2.03, 2.84 [V].
- The thinning evaluability at R07 was corrected as well (N_eff ≥ 252, l.953–954) [V: script [11]].

### N5 [N-B3]: the width in untested families is a convention

**Status: RESOLVED.**

**Location:** crossing rungs l.406–417; b₀ called a convention at l.418–421 and in [L6] l.2012–2014.

**My check:**
- The expected crossing-rung counts are 1,355 at R09⊗R06 and 129 at R11⊗R06 [V: script [11]].
- The 5 CPU-h and the 0.9 GB are costed (§11.4).
- Whether the crossing rungs are evaluable is a dated commitment (l.439–440) with a rule. That is the correct form for
  something only Phase 3 can measure.

### N6 [N-B4]: probability factors are not capped

**Status: RESOLVED.**

**Location:** l.444–447, l.1319–1324, T1-c (v) l.1473, T1-h l.1497–1501.

**My check:**
- The censored mean for φ₀ = 0.1 and s = 2.47 is 0.306 by Monte Carlo, against 0.31 in v3 [R]. The uncensored value
  is 2.11.
- The μ grid and the log-linear CLs interpolation are given (l.1374–1378).
- T1-h is generated at λ = m + 1, with m′ redrawn.

### N4 [N-B5]: criterion (a) has no re-test route, and the rates were computed at s_model = 0

**Status: RESOLVED.**

**Location:** §4.0 points 4–5, l.321–372; Df-2 l.2511.

**My check:**
- I simulated the rule at the cap with a shared δ (10⁶ draws) and got a per-test final FAIL of 0.0106, against 0.0107
  in v3 [R].
- At s_model = 0 the analytic value is 0.0050 + 0.045 × 0.005 = 0.0052 [R].
- K = 10 is listed (l.339–341), and the power table is in place.
- F is unchanged.

### N18 [N-B6]: Phase 3 staffed with six channels against a cap of three

**Status: PARTIALLY RESOLVED.**

**Location:** §11.3 l.2310, l.2326–2330.

**My check:**
- There are now three channels for 12 days. But in the same rows, 1-bot reviews per channel and the PREREG drafting
  run "alongside" inside the same cap.
- In Phase 2 a "dedicated agent" for the sealed comparison (l.540–541) is also needed beside the three Phase-2 agents.
- New finding F-B6.

### N16 [N-B7]: the time-tag closure is tested on the wrong population

**Status: RESOLVED.**

**Location:** §4.6 l.1033–1052; COM B3-c.

**My check:**
- The test population is now the prompt, truth-attributed candidates.
- There are 5.77×10⁵ such candidates at R04, which give 58 late counts at a fraction of 10⁻⁴ (55 are needed) [V].
- The credit is limited to the deepest window edge that passes.
- The nominal-window check is "marginal", and v3 says so honestly.

### M6 [B-1]: central target, floors and the measured projection

**Status: GATE A (Q2), with a residual.**

**Location:** §0; Tables 4.4a and 4.4c; Q2.

**My check:**
- The definitions and the allocation are done. I reproduce (Σ√(N_t c_t))²/C = 2.49×10⁷ s / 2.39×10⁶ s = 10.4, against
  a sum of means of 10.3 [R].
- What the user decides (pool size and message) is in Q2.
- The measured projection is still pilot-dependent, which is correct for a dated rule. Its gaps are F-A1, F-B2 and F-B4.

### M4 [B-3]: the trend rule and the rung index across families

**Status: RESOLVED** (through N5).

**Location:** §4.0 point 7.

**My check:** the distance is now counted per quantity (l.397–400), so the rung index is no longer used across families.

### M12 [B-7]: nuisance propagation to the deep rungs

**Status: RESOLVED.**

**Location:** §4.9 l.1233–1237; COM B6-c l.114.

**My check:** both sentences Edmund asked for are there, word for word in substance.

---

## Part 2. Findings on v3

### 2.1 Category A

#### F-A1 (A). Z(ττ) and lost-lepton Z(ℓℓ) have no no-pile-up sample, so the headline projection omits terms that could dominate it

**Evidence.**
- §4.7 point 3 (l.1068–1074) states that "P_geo, f_k and the ceiling H are counted on no-pile-up hard-scatter events of
  each process".
- The pool is "3.6×10⁷ events over the twelve processes" (l.1071–1072).
- Table 4.4a (l.743–757) and the script's pool allocation have twelve SM rows. The three additions are "not in the
  table" (l.766).
- The multijet term has its own 10⁶-event looser population (l.1120–1126, 12.5 CPU-h). **Z(ττ) and lost-lepton Z(ℓℓ)
  have only their 2,000 hit-level events** (sample 20, l.1841). No inventory row and no budget line gives them
  no-pile-up events.

**Consequence.**
- Beyond R07 their term can only be a direct bound, N_t × 1.14/2,000.
- N_trig for these two is not known before day 12. For an N_trig of 10⁵, 4×10⁵ and 1.3×10⁶, this floor is **57, 228 and
  741 events** [R, E].
- The planning range is my estimate:
  - Z(ττ): about 0.17 of the Z(νν) branching fraction × 0.1–0.3 for MET > 250 GeV after the lepton veto, times
    N_Z(νν) = 2.5×10⁷, giving 4×10⁵–1.3×10⁶.
  - Lost-lepton Z: about 10⁴–10⁵.
- That is 3 to 40 times the whole projection that §0 and Q2 present (B₅₀ ≈ 17).
- It could also trip the day-15 pause (B₅₀ > 300), but only if someone adds the terms to Table 4.4c: rule 1 recomputes
  "Table 4.4c", which does not contain them.
- §0, Table 4.4c, Q2 and the Gate-A reach numbers carry no caveat about these terms.

**Why A.** The headline the human decides Q2 on leaves out terms that, as planned, could set it. The method text
(§4.7) promises samples that the budget and the inventory do not contain. That is framing that hides a problem, and a
design inconsistency that an executor would hit at day 12.

**What "fixed" looks like.**
1. Put Z(ττ) and lost-lepton Z(ℓℓ) into the pool now, with EST planning N_trig and the √(N_t/c_t) rule.
   - With pool shares they cost about 9–32 CPU-h and about 3 CPU-h, and their floors fall to about 0.2–0.6 [R].
   - State that the shares are re-allocated at day 12–15, when the MET model gives N_trig.
   - Add their inventory rows (seed streams `prod.hs0.ztt`, `prod.hs0.zll`).
2. Add one EST row for the additions to Table 4.4a and Table 4.4c, and state in §0 and Q2 that the projection includes
   them at the planning N_trig.
3. Let rule 1 of §11.7 recompute the projection "for every term of the likelihood", not "Table 4.4c".

**Effort:** about 1–2 h of text plus a script line, and at most about 40 CPU-h (or a re-split inside the 665 CPU-h,
which raises the summed floor by about 3 %).

### 2.2 Category B

#### F-B1 (B). The headline leads with the optimistic edge and contradicts v3's own rule for quoting the conservative value

**Evidence.**
- §0 l.55–56 and Q2 l.2476 read "about 790 GeV if every ceiling is empty".
- (a) v3 itself says that m_H = 0 "is not the expectation" (l.801–802).
- (b) For f₀ > 0.5, which is the expected reading, v3 pre-declares that the paper quotes "the limit at the 84 % edge of
  the band as the conservative value" (l.1399–1401). The abstract bracket puts "the conservative number, quoted first"
  (l.806–809).

**My numbers.**
- For the R09-like, empty-ceiling row, the 84 % edge of s₉₅ is 20.8, which gives **721 GeV** [V: script [9b]].
- I made an EST of m_H from v1 [R, E]. v1's attributed Z(νν) hard-scatter rate falls ×278 from R05 to R06 (4.51 →
  0.0162 per event). With a fall of ×100–300 per further width step, H(R08) ≈ 1.6×10⁻⁶–1.8×10⁻⁷ per event, so
  m_H ≈ 2–18 in 1.14×10⁷ events. That corresponds to the rows giving 760–723 GeV.
- **The honest single-line headline is therefore about 720–760 GeV (median), with about 720 GeV conservative if the
  ceilings are empty, falling to about 525–575 GeV if a ceiling counts 100.** "About 790" is the upper edge.

**Fixed looks like.**
- In §0 and Q2:
  - give the range first;
  - mark 790 as the empty-ceiling median;
  - quote the 84 % edge that the abstract will carry;
  - add one line with the v1-based EST of m_H, labelled with its large uncertainty.
- State once which number heads the abstract: the 84 % edge, by l.1399.

**Effort:** 1 h.

#### F-B2 (B). The ceiling scenario of Table 4.4c is built on the one large term that v3 expects to test; the terms expected at H are not projected

**Evidence.**
- Table 4.4c (l.778–791), §0 point 1 (l.48–50) and Q2 vary "the Z(νν) ceiling".
- But Z(νν) has an evaluable B4-c test (81 expected counts, l.1136; annex l.2525).
- If that test passes, the Z(νν) term at R09 is P_geo + Σ f_k π_k (S = 1 beyond R06, π_k carried with s_tot 0.73 and
  censored), not H (§4.4 point 4, l.699–711). It enters at H only if its estimator FAILs high, is above its cap, or is
  NOT TESTED.
- v3's own partial-outcome table says the terms expected at H are "the eight proxied SM processes" (l.1601), plus the
  three additions (annex l.2529). None of these is in Table 4.4c with a counted ceiling.
- My EST [R]: if their H per event were like the Z(νν) value above (about 1.6×10⁻⁶), the eight proxied processes (14 %
  of N_trig) would add about 0.14 × 4.08×10⁷ × 1.6×10⁻⁶ ≈ 9 events at H. That is small next to Z(νν) at its
  ceiling (≈ 40), but it is the scenario v3 actually expects.

**Why B.** The table is a correct no-credit envelope. But the human reads it as "the reach drops with m_H". In fact,
under a B4-c PASS it depends on m_H only weakly, and the expected driver is whether π_k at R08–R09 is small and
credited. So Gate A shows the wrong sensitivity, in a pessimistic direction for Z(νν) and an unquantified one for the
proxied processes.

**Fixed looks like.**
- Relabel the m_H rows "Z(νν) enters at its ceiling (estimator not credited)".
- Add one row "Z(νν) tested and credited; eight proxied processes and the additions at their ceilings, H per event as
  for Z(νν)".
- State in Q2 which row is the expected one.

**Effort:** 1 h plus one script scenario.

#### F-B3 (B). TG-1 still reads "target met" when every leading term is a low count

**Evidence.**
- "Target met" requires σ_ln ≤ 1, f₀ ≤ 0.5 and "no leading term labelled bound or no credit" (l.1397–1398; COM TG-1
  l.165).
- f₀ counts only zero-count factors (l.1395). The label "low count" (1–3 counts, w_m 0.53–0.80, l.1390) is therefore
  allowed.
- With the sixteen terms of Table 4.4a each at m = 1, B₁₆/B₅₀/B₈₄ = 15.3/19.9/25.7, σ_ln = 0.26 and f₀ = 0 [R]. The
  label is then "target met", although no term is an estimate in v3's own sense (m ≥ 4, PASS; l.1391).
- The plan's target is to "turn every leading zero-count bound into an estimate" (PLAN l.129–130).
- This is the N3 twin at m = 1–3. It is not the expected outcome, which is why it is B and not A, but it is a
  plausible one if the large samples count a few events.

**Fixed looks like.** Replace the third condition with "**every leading term labelled estimate**" in §4.11 point 3,
COM TG-1 and §0. The f₀ condition can then stay as it is.

**Effort:** 15 min.

#### F-B4 (B). Two inputs of the day-15 rules have no sample that delivers them

**(i) The R06 rates of the eleven small SM processes.**
- Rule 4 (l.2445–2447), B4-c (l.1138–1139: "sizes recomputed at day 15 from the rates measured on the Phase-3
  samples") and §12.4 need these rates by day 15.
- The inventory (§4.17, samples 1–13) has no Phase-3 hit-level sample of any SM process other than Z(νν) (sample 5).
- The only trace is the script's Phase-3 B4 line "MET model, biased multijet generation, small hit samples", 50 CPU-h
  of guessed cost (script l.140).
- At 25.2 s per event, even all 50 CPU-h give about 7,100 events, i.e. about 650 per process. At R06 rates of
  0.003–0.016 per event that is 2–10 counts per process, a rate error of 30–70 %.
- So the "≤ 40 CPU-h" test of rule 4 and the re-sizing of W(τ_h), W(τ_ℓ) and tt̄ 1ℓ would be decided on noise. The
  samples also break INV-1 ("every produced sample matches a row").

**(ii) The pilot ceiling at the R09 width.**
- The pilot "measures H of the largest term at every T2 candidate" (l.728–729) on 2.3×10⁶ events.
- At my EST H(R08) = 1.8×10⁻⁷–1.6×10⁻⁶, the pilot expects **0.4–3.7 counts** [R].
- Rule 3 branches on whether "its ceiling is empty in the pilot" (l.2439–2440), and rule 1 uses "the measured
  ceilings". It is not stated what number a pilot count of 0, 1 or 2 enters as. A pilot zero is a bound of 12.4 events
  for Z(νν), five times its full-pool floor.

**Fixed looks like.**
1. Add an inventory row for the Phase-3 SM development samples, with size per process chosen so that R06 has about 20
   expected counts (or say that rule 4 uses v1-proxy rates and is applied again at the 4a closure).
2. Specify the pilot reading:
   - H at the R09 width enters as Gamma(m + 1) from the pilot count;
   - the branch of rule 3 is set by the **R06–R07 pilot counts** (which will be populated), extrapolated in width
     with the fall that the pilot itself measures, and labelled EST.

**Effort:** 1 h; up to about 50 CPU-h is already in the budget.

#### F-B5 (B). The B1 trace finds four executability gaps

Trace: §4.4 → §4.0 → §8 → §11.3 → COM B1-a and B1-f.

**(i) The per-k promotion comparison is assigned to a sample that does not exist yet.**
- It is "Phase 3 … on the derivation overlays of near-pass events" (l.703–704).
- The derivation overlays are built from pool events (l.812–816): sample 19, phase 4a, after the freeze.
- The only pre-freeze near-pass overlays are the pilot's 1,000 (l.729, sample 11).
- The s_model of the promotion model must be fixed before the freeze (§4.0 point 4 (c)).
- So the text should name sample 11, and state whether 1,000 events give classes with at least 24 promoted events.

**(ii) The development ceiling and completeness tests have no named sample.**
- B1-f requires them "first on development samples (results fixed before the freeze)" (l.861–862).
- For DIF and NI, the only pre-freeze samples with pile-up are:
  - C′_PU (sample 4: v1 **guns without Geant4**, a different physics generator);
  - the pilot's biased near-pass overlays (sample 11), which are not unbiased and so cannot give a leak fraction.

**(iii) The pre-registration outline omits the ceiling test, the completeness bound and c_mix.** §8 item (2) l.2061–2067
and COM PR-1 l.158 do not mention them, although they decide eligibility (§4.0 point 6).

**(iv) The ceiling test is applied to enriched test overlays with sampling weights (l.817–819)**, while the test is
defined as "the exact conditional test for two Poisson counts" (l.677). It needs the effective-count form of l.1301.

**Fixed looks like.**
- Name the samples for (i) and (ii) in §4.4 and §4.17. If none is adequate, add 1,000 unbiased Geant4 DIF overlays
  in Phase 3: about 7 CPU-h, as development.
- Add the three items to the §8 outline and to PR-1.
- Write one sentence on effective counts.

**Effort:** 1 h; about 7 CPU-h.

#### F-B6 (B). The schedule exceeds the three-agent cap in Phases 2 and 3

**Evidence.**
- Phase 3 is three channel executors for 12 days (l.2310), which is exactly the cap. The same row runs a "1-bot review
  per channel" and "`PREREG_v2.md` … drafted alongside".
- JFC requires one 1-bot review of the Phase-3 artifact, not one per channel (study `CLAUDE.md`, phase table).
- Phase 2 has three agents, plus the "dedicated agent that has no other role" for the sealed C1 comparison (l.540–541).

**Estimate [E].**
- Three reviews of about 0.5 day each, plus fixes, come to about 3 agent-days.
- PREREG drafting is about 2–3 agent-days.
- So Phase 3 needs about 41 agent-days against 36, which is about +1.7 calendar days at three concurrent agents.

**Fixed looks like.**
- Add a slot table per phase (executors + reviewers + drafter ≤ 3).
- Have one Phase-3 1-bot review on SELECTION.md.
- Make the PREREG drafter channel (iii)'s second task after day 12.
- Make the sealed comparison a short job inside channel (i)'s slot. A different agent session is still needed, but it
  runs sequentially.
- Or state Phase 3 as 14 days.

**Effort:** 30 min of text.

### 2.3 Category C

- **C-1** *The approved figure and the reserve.* §11.2 l.2272 says that "none of these is inside the approved figure of
  Q4", while the next row calls the 156 CPU-h reserve "approved in advance, with Q2". Say whether the stop-rule base
  is 4,378 or 4,534 CPU-h, i.e. a threshold of 5,691 or 5,894.
- **C-2** *Notation.* T1-c (iii) and COM T1-c have "true λ·M = 0.5, 1.14, 2, 3" (l.1468). λ is already the expected
  count (l.1300), so this should read "true λ".
- **C-3** *Placeholder bias.* Every reach uses v1 efficiencies. 31 of 40 v1 points used the fast path, which v1 measured
  ×1/0.87 high (l.1629). Say this once next to the headline: the v2 reach is expected a little lower, roughly 10–20 GeV
  [E]. Also say "best Λ per mass".
- **C-4** *Reach mapping.* It assumes that the book's reach at B used the same s₉₅ definition (the median expected CLs
  at fixed B, script l.496–514). The two agree at B = 0 (3.0 → 1026). Confirm this once against `book/checks/
  ch29_checks.py`.
- **C-5** *Wording of the ceiling counts.* "If the Z(νν) ceiling counts 100 events" (§0, Q2) is easy to misread as 100
  background events. Write "100 simulated ceiling events (≈ 220 background events)".
- **C-6** *Rule 1 at day 15.* "B₅₀ at the best candidate" is undefined before unblinding. Use the candidate with the
  lowest G computed with the v1 placeholders (§4.12 rule 4).
- **C-7** *The label depends on m_H.* With a counted Z(νν) ceiling, f₀ falls below 0.5 (for example m_H = 10 gives
  f₀ ≈ 0.2), and the label becomes "width small, background bounded", not "sample-size limited". Say that the
  expected label holds for small m_H.
- **C-8** *R-20 deadline.* The claim "beyond existing limits" needs R-20 (l.1985), which has no deadline. Set it to
  before Phase 4a.
- **C-9** *Fig. 7.* Mark the conservative (84 %) point as well as the median point (§9 l.2129–2132).
- **C-10** *Df-1 is a reading of the user's own plan.* The plan's "×10" is a MUST statistic, and v3 reads it as ×10 in
  total and ×5 on the limit half. Consider showing Df-1 as a sixth one-line question, as Q5 does for D7. Otherwise keep
  it first in the defaults, as now.
- **C-11** *One s_model per estimator for B4.* The four B4-c tests use one hard-scatter estimator. Its s_model can only
  be derived on the Z(νν) development sample (sample 5 plus the pilot). Say so.
- **C-12** *The 4a review start.* The 4a review starts the day production ends (l.2313–2314). The closure analysis of the
  last campaign, T1 expected results, the note and the PDF need about 1–2 days. Schedule change S-1 below provides it.

### 2.4 Executability: three items traced end to end

The path for each trace is: per-item section → systematic plan (§5) → PREREG outline (§8) → schedule (§11.3/§11.7) →
COM row.

**B1: the DIF closure and the ceiling** (§4.4 → §5.1 "study-specific" → §8 item (2) → §11.3 channel (i), §11.7 rule 5 →
COM B1-a, B1-f).
- The per-item text is complete on method.
- Four gaps (F-B5):
  - the per-k comparison sample is a 4a sample;
  - there is no development sample for the ceiling and completeness tests;
  - the PREREG outline omits the ceiling, completeness and c_mix entries;
  - the weighted-count form of the ceiling test is missing.
- COM B1-a and B1-f agree with §4.4. B1-a gives phases "3 / 4a" and B1-f "2 / 3 / 4a", and both are consistent with
  §11.3.

**T1: the likelihood and the zero-count tests** (§4.11 → §5.1 MC statistics, §5.2 → §8 item (5) → §11.3 channel (iii)
→ COM T1-a … T1-i).
- This is the cleanest trace. The model, generation convention, toy procedure, grid, interpolation, censoring and
  acceptance numbers are all in one place and agree with COM.
- There is one notation slip (C-2).
- The risk is load. Channel (iii) carries the MET model and its external validation (by day 10), A and m_mig (day 12),
  the T1 tests, the T2 script and the v1-placeholder G with its bootstrap, all in 12 days. Brief §4 marks T1 as a
  "go up" task.
- Suggestion: move the T2 script and the G bootstrap to channel (ii) after the occupancy model is built, or to the
  PREREG drafter.

**C1: the reproduction** (§4.1 → §5.2 check 6 (Bonferroni) → §8 item (8) → §11.3 days 0–5, §11.7 decision point 1 →
COM C1-a … C1-e).
- Complete and consistent. The 41 comparisons add up: 4+3+4+2+3+7+5+3+4+3+3 = 41 [V].
- Two gaps:
  - The sealed-comparison agent needs a slot (F-B6).
  - The remediation route ("three documented attempts … then the user is asked", l.510–512) is not given a time. If C1
    fails, Phase 2 cannot end at day 5. Write that a failed family moves decision point 1 and the calendar day for day,
    and is reported under D6.
- Phase 2 uses 4.3 of its 5 days of CPU at 116 core-h per day (script [7]). Any slip in the day-0 timing jobs
  propagates directly.

### 2.5 Length, and what to cut or move

The 2,674 lines are a risk for Phases 2–3. In three traces I found statements in one section that another section
contradicts:
- the overlays: a sample named as Phase 3 is produced in 4a;
- the small SM samples: no inventory row;
- the agent slots.

The eligibility logic also appears five times: §4.0 point 6, §4.11 point 3, §4.12 rule 1, the partial-outcome table and
COM T2-a. I found them consistent today, but every future edit must touch all five.

Concrete cuts (≈ 300 lines, with no content lost):

| section, lines | action | saves |
|---|---|---|
| §13.1, l.2590–2632 | delete; it is fully in `FIX_REPORT_cycle1_dmitri.md`; keep a two-line pointer | ≈ 40 |
| §13.2, l.2633–2667 | keep only the two number corrections (l.2664–2667) and a pointer to the fix report | ≈ 30 |
| §4.11 point 2 "Why this prior" and "Alternatives" (l.1345–1360) and point 4 table and readings (l.1404–1433); §4.0 point 4 size/power discussion (l.343–363) | move to a "Statistics justification" appendix; keep the rules in place | ≈ 70 |
| Table 4.0 (l.276–304) and the §11.2 provenance table (l.2286–2303) | merge into one appendix table of unit costs | ≈ 25 |
| §6.1–6.2 (l.1915–1957) | appendix (binding for Phase 4a/5 reviews, not for Phases 2–3) | ≈ 45 |
| §8 v1 hashes and freeze timing (l.2099–2113) | move to the PR-2 appendix | ≈ 15 |
| §4.1 blinding detail (l.520–552) | keep the rule; the options are in Q1 and COM C1-d | ≈ 15 |
| §12.4 (l.2549–2566) | replace with a pointer to §11.7 and §6.4 | ≈ 15 |
| §11.5 [DP5] paragraph (l.2366–2373) | merge with §5.1 | ≈ 8 |
| eligibility logic in five places | state it once (§4.0 point 6) and refer to it from the other four | ≈ 30 |

**Derived documents.** These are an orchestration suggestion, not a defect of the strategy. Before Phase 2, the
orchestrator should produce four compact files from v3 plus COM, each checked back against v3 by a mechanical
(lower-effort) agent:
1. **Phase-2 task sheet** (≤ 2 pages), one block per agent channel (i)–(iii). Each block gives the COM ids, the
   inventory sample numbers with size and seed stream, the outputs, the day-0 timing jobs, the retrieval deadlines
   (R-2, R-3 by day 5), and the inputs of decision point 1 and checkpoint 1.
2. **Phase-3 task sheet**, per channel, ending in a **day-15 input table**: input → producing sample → owner → rule of
   §11.7. This table would have exposed F-B4 at once.
3. **PREREG skeleton**: one section per COM estimator or criterion, with blanks for s_model, rungs, sizes, expected
   counts, size and power, and the ceiling and completeness entries.
4. **NUMBERS register**: every number shown to the user (§0, Q1–Q5, Df), with its script section. STATUS and the
   gate packages quote only from it.

### 2.6 The schedule

**Credibility.** The arithmetic is right: 42 non-production days = 21 before production + 13 + 8 + 2 days at Gate B,
and the 46-day and 64-day ranges both check [V: script [7]]. The two utilisation factors are labelled as assumptions
and are measured in week 1 (l.2215–2217). That is the right treatment.

Under the cap of three agents, two things are optimistic:
- Phase 3 (F-B6: about +1.7 days);
- the 4a review starting on the last production day (C-12: about +1–2 days).

A realistic central value is about **59–60 days**, with the 46–64 range shifted by about +2.

**Critical path.** Phase-3 development (12 days, agent-bound) → freeze review → background production (14.6 days,
CPU-bound) → 4a review → 4b → Gate B → 4c → Phase 5. Inside production the order B2 direct → ρ = 2 → pool → overlays → B4
→ B6 → B5 is sensible. ρ = 2 memory can cost up to 400 slot-hours (l.973–975), and this sits inside the 0.75 factor.

**The dated rules are placed well.**
- Checkpoint 1 at day 5 comes after the timing jobs that fix most of the guessed unit costs:
  - the 45 ms no-pile-up event, from the day-0 timing job;
  - injection-mode rows, from the C1 signal rows;
  - the 5 keV Stage-3 cost, from P1 B*-off.
  So the stop rule can still redirect the whole production.
- The day-15 rules act on what production does from day 21, so they can still move CPU.
- One improvement: the pilot is finished by day 5. Rules 1 and 3 (projection and reserve routing) could be applied at
  **day 7**, leaving only rules 2, 4 and 5 for day 15. That gives the PREREG drafter a week more with the outcome class
  known.

**The three cheapest changes that shorten the calendar without touching a MUST criterion:**

| # | change | CPU-h | days saved [E, R] |
|---|---|---|---|
| S-1 | Move B5 (SHOULD; reduced production and prototype, 183 CPU-h) and the B6 **signal** arm (about 77 CPU-h of rows plus the scaled-material Stage 3; its ratios are read only after the verdicts anyway) out of the 4a production window into days 36–48. In that window the cluster carries only the S1 chain and the toys (922 of 2,088 core-h). B5 is not in the likelihood. COM B5-a…c deadlines move from 4a to 4b; B6 is already 4b. | 0 | **≈ 1.5** on the critical path. It also provides the C-12 buffer before the 4a review |
| S-2 | Extend the Q5 reading to generator-level background inputs that no analysis choice influences (multijet biased generation 10⁷ events, 65 CPU-h; Geant4 spectra and discs, about 15 CPU-h), and run them in the 1,364 idle pre-freeze core-h | 0 | **≈ 0.5** (one more line in Q5) |
| S-3 | One Phase-3 1-bot review (as JFC requires) instead of one per channel; the PREREG drafter takes channel (iii)'s slot after day 12; P1 (51 CPU-h, plus 1–2 person-days of new code that feeds only the paper) moves from Phase 2 into the production window, where the agents have slack | 0 | avoids the **≈ 1.7–2** days of F-B6 and protects the 5-day Phase 2 |

Together these recover about 3.5–4 days. The calendar comes back to about 56–57 days, now credible under the cap.
Reviews that pass at once remain the only other lever (up to 8 days), and they cannot be planned.

### 2.7 The honest headline, outcome by outcome (against PLAN §8)

| outcome | what v3 would show | paper message | honest? publishable? |
|---|---|---|---|
| bounded, ceilings small (expected) | B₅₀ ≈ 17–40, f₀ ≈ 0.2–0.6, σ_ln ≈ 0.25–0.35 | "bounded by simulation statistics; conservative reach ≈ 720 GeV (84 % edge), median ≈ 760–790; 1,026 GeV if negligible" | honest once F-B1 is fixed and F-A1 is added. Publishable: about 4× the existing bounds of about 180 GeV, with a closure-tested method and a 3.7–4.7-decade improvement of the bound over v1 (which v3 labels "bounded"). Better than PLAN's "middle" row in reach, worse in kind (bounded, not resolved); v3 says so (l.58–59) |
| a ceiling counts (no credit) | B₅₀ ≈ 80–240 | the same, with the term labelled "no credit, ceiling counted" | honest; ≈ 575–660 GeV median. Still above the existing bounds |
| additions unpooled (today's plan, F-A1) | B ≈ 60–740 from Z(ττ) alone | would read like "real background", but it is an artefact of sample size | **misleading if unfixed**: a bound on 2,000 events would be read as a measured term |
| real background | counts in the large samples | measured irreducible background | honest; v3 l.881–882 treats it as a result |
| closure fails | R07-direct ≈ 1.6×10⁵ events (l.804–805) | method and anatomy paper | honest; weaker but publishable (P1, efficiencies, anatomy) |

**Placeholders.** The v1 placeholder efficiencies are stated at §0 l.56–57, in Table 4.4c's caption, in the
preamble of §12.1 (l.2459–2460) and on Fig. 7. They are **not** stated inside the Q2 cell (l.2476) or at l.809
("1,026 GeV at B = 0"). The 3-page Gate-A package quotes the Q2 cell, so the tag should be in the cell (C-3).

**The floor reduction from 45.3 to 11.7.** §2 (l.158–178) and §13.2 (l.2667) explain it correctly as re-accounting,
and §0 never compares against 45. My decomposition [R]:
- 23.1 events of the 45.3 were double counts (PV pairs 18.4; γ, V⁰ and loopers 4.7);
- the rest falls by a factor of 1.9, because one real event tests all its prompt particles at once, and the freed CPU
  goes to fewer terms.

This is not overclaimed. One caveat belongs next to the headline floor: the SM part (7.9 of the 11.7 events) rests on
the guessed 45 ms per no-pile-up event (G, l.289). At a fixed CPU the floors scale as √c, so a doubled cost raises the
SM floor to about 11.

### 2.8 Gate A, read as the human would (§12.1 alone)

**Q1.** Self-contained, with a sensible default and a cost for each option. The one thing a human might miss is why
seeing early matters: two of the 16 candidates would become known early. The (b) row says this.

**Q2.** Self-contained, but it leads with the optimistic number (F-B1). The ceiling sensitivity is for a term expected to
be tested (F-B2), and the additions are absent (F-A1). The default (no pause unless B₅₀ > 300) is sensible. The
"larger pool" cost (+665 CPU-h, +3.8 days, about +30 GeV) is given. Missing: what "R09-like" means, in half a line.

**Q3.** Good. The annex gives per-term costs. One missing consequence for the human: under (a) those terms are labelled
"no credit" in the paper and in the ladder figure. Q3 (a) also promises supply "from the reserve", which rule 3 spends
first, so in practice nothing may remain. Say so.

**Q4.** Good and candid ("this may well happen"). The ambiguity of C-1 should be removed.

**Q5.** Good. Add that the "no" option moves 266 CPU-h onto the critical path. That is where the 1.8 days come from.

**The eight defaults.** Df-2 to Df-8 are proper technical defaults with alternatives and costs. **Df-1** is a reading of
the user's own plan statistic (C-10) and is the one I would promote to a question. Df-6 is not overridable (brief D1)
and is an FYI, as v3 says.

**Length.** §12.1 is about 2.5 pages, but it is not the whole Gate-A package: brief D7 asks for the strategy, the
benchmarks and the schedule. Part 3 below is the 3-page text.

### 2.9 Paper readiness

**The seven flagship figures.** Each one maps to a named source, a phase and a COM item (§9 l.2119–2133; FIG-1):
- Fig. 1 is chosen from passing signal events only in Phase 4c, which is blinding-consistent.
- Fig. 2 comes from P1 (Phase 2).
- Figs. 4 and 5 come from the background inputs and T1 in 4a.
- Figs. 6 and 7 are drafts at 4b and placeholders at 4a, final at 4c.

**The 14 supporting figures** cover C1, C2, B5, T1, B6, S2, MET, the BDT/dE/dx ratios, the floors, the B1
decomposition, s_tot, the time tag and the T2 ranking.

**Figure-scrolling gaps (C level):**
- Fig. 7 should mark the conservative point (C-9).
- There is no figure for the projection against m_H. One is not needed in the paper, but it would help the Gate-B
  package.
- The weights closure of biased generation (B1-e) has no figure, and referee Q4 could ask for it.

**The 25 referee answers.** They map to items and paper sections (§10 l.2166–2192), with no orphans. Q22 and the claim
"beyond existing limits" depend on R-20, which needs a deadline (C-8). Q1's honest answer depends on F-B1 and F-B3.

---

## Part 3. Draft text for the Gate-A package (≤ 3 pages)

*Numbers are taken from v3 and its script. Two lines are marked ⟨after fix⟩: they change when F-A1 and F-B1 are
applied, and the orchestrator should take their final values from the fixed strategy. All reach numbers are ESTIMATES
from the plan's reach table with v1 signal efficiencies as placeholders (best Λ per mass, barrel, 3 ab⁻¹).*

### Quirks v2: Gate A, decision package

**Headline.**
- v2 is a simulation-only projection: can a Phase-2-like barrel tracker at pile-up 200 find electroweak quirks, and up
  to which mass?
- The strategy predicts, before anything runs, that the leading backgrounds will be **bounded by simulation
  statistics, not estimated**.
- The pre-declared label of the expected paper is **"target not met: sample-size limited"**.
- ⟨after fix⟩ Expected reach (EST, v1 placeholder efficiencies):
  - **≈ 720 GeV conservative** (84 % edge) and ≈ 760–790 GeV median, if the no-pile-up ceilings count few events;
  - ≈ 525–575 GeV if the largest ceiling counts about 100 simulated events;
  - 1,026 GeV for a negligible background.
- Existing limits in this Λ range lie below about 180 GeV.
- The bound improves on v1 by about 4–5 decades (v1: B₈₄ = 1.2×10⁶ events).

**What Phase 1 did.**
- Feasibility benchmarks on the lab cluster: chain, generators, Geant4, runner, pyhf. 691 CPU-h of the plan rest on
  measured unit costs, 2,316 on derived costs and 1,371 on guesses.
- A strategy reviewed in three cycles by fresh physics, critical and constructive reviewers and an arbiter. The
  redesigns were:
  - zero simulated counts kept in the expected limit;
  - closure tests on held-out rungs and samples, with an extrapolation width that is always added;
  - a tested ceiling for untestable pile-up factors;
  - one accounting route per particle origin (removes a double count found in v1);
  - false-fail rates computed at the declared model widths.
- Binding commitments: `COMMITMENTS.md`, one row per criterion.

**Decisions for you (one line each; ● = recommended default).**
- **Q1, blinding exception for the C1 reproduction.** Six of the v1 signal counts being reproduced are also
  efficiencies of v2 candidate selections. May they be compared before the background verdicts?
  - ● Yes, sealed: only PASS/FAIL is reported until Gate B, and four other counts are open.
  - Alternatives: all ten open and disclosed in the paper; or drop the six (v1's best-point count is then not
    reproduced).
  - 14 CPU-h in every option.
- **Q2, the bounded paper as the default deliverable.** Proceed to production without pausing, unless the day-15
  projection exceeds B₅₀ = 300 events (reach below about 555 GeV) or both pile-up estimators miss their precision cap?
  - ● Yes. The 156 CPU-h freed by the toy parametrisation are spent at day 15 by a pre-written rule.
  - Alternatives: always pause at day 15; or a doubled no-pile-up pool (+665 CPU-h, +3.8 days, about +30 GeV, and only
    if the ceilings are empty).
- **Q3, exception to brief D4.** Your brief requires the statistics each MUST criterion needs. For the eight small SM
  processes (14 % of the triggered events) and the three new ones, the closure test is not affordable at the planned
  statistics. May these terms enter at their measured, tested ceiling, labelled "no credit" with the selection still
  eligible?
  - ● Yes. DIF, NI, Z(νν), W(τ) and tt̄ 1ℓ are supplied (+258 CPU-h).
  - Alternatives: comply everywhere (≈ +680 CPU-h, range 100–1,230, ≈ +3.9 days); or strict (such selections are not
    eligible, and "closure fails" becomes a likely paper).
- **Q4, budget and calendar.** Approve 4,378 CPU-h and about 57 days (8 weeks; your target was 2–4 weeks) with the
  downscopes DP1 (reduced sideband), DP2 (reduced detector variations), DP4 (S4 and S5 not done) and DP5 (Herwig at
  generator level after an install attempt)?
  - ● Approve. The stop-and-ask threshold is 5,691 CPU-h. Contingency (2,135 CPU-h) and conditional draws are
    reported, not pre-approved. **The day-5 re-projection may trigger the stop rule**, because 1,371 CPU-h rest on
    guessed costs.
  - Alternatives: pre-approve 6,513 CPU-h; MUST only (3,945 CPU-h, 54 days); full SHOULD (4,891, 60 days).
- **Q5, reading of brief D7.** May the truth-level signal samples (Stage 2 and the string propagation, 47 + 266 CPU-h),
  which no analysis choice influences, be produced before the pre-registration hash?
  - ● Yes.
  - Alternative: produce them after the hash (+47 CPU-h; 266 CPU-h move onto the critical path, +1.8 days).

**Defaults you can override (reported, not asked).**
- Df-1: 2,000 signal rows per point (×10 rows in total, ×5 on the half that sets the limit; 15 % error at the best
  point). 4,000 rows: +827 CPU-h, +4.7 days.
- Df-2: closure tolerances F = 1.5 / 2 as in v1, with the model width capped. A correct analysis loses a selection to a
  false FAIL with probability 2–4 %.
- Df-3: computed NLO normalisation as nominal, with the resummed value quoted beside every limit, and the infracolour
  correction (+3 to +13 %) as a one-sided band.
- Df-4: dE/dx not used; the efficiency forgone is measured.
- Df-5: time-tag credit only where its closure passes and the timing tails are sourced.
- Df-6: endcap outlook wording as fixed by brief D1.
- Df-7: no public size → no nuisance, with the shift reported beside the limit. No public MET parameters → the study
  stops and asks you.
- Df-8: toys parametrised, with exact checks.

**Schedule and budget (proposed variant; CPU-h at 174 core-h per production day, an assumption measured in week 1).**

| days | phase | CPU-h | gate or checkpoint |
|---|---|---|---|
| 0–5 | 2: reproduction of v1, finder checks, theory inputs, P1, pilot, timing jobs | 500 | decision point 1 and stop-rule checkpoint 1 (day 5) |
| 5–17 | 3: estimator development (three channels), pre-registration drafted | 573 | decision point 2 (day 15): outcome class, caps, reserve |
| 17–21 | pre-registration freeze: 4-bot review, hash (no human gate) | — | you are notified; checkpoint 2 |
| 21–36 | 4a: background production; closure analysis | 3,109 (2,548 on the critical path) | weekly re-projection |
| 36–48 | 4a review, 4b selection on the optimisation half | 196 | **Gate B (≈ day 48)**: closure verdicts first, then the selection |
| 48–57 | 4c limits; 5 paper and package | — | **Gate C** |
| **total** | | **4,378** | 42 of 57 days have no production on the critical path |

The range is 46 days (all reviews pass at once, MUST only) to 64 days (production utilisation 0.5). ⟨after fix⟩
Reviewers estimate about +2 days for agent concurrency, recoverable by the schedule changes S-1 to S-3.

**Top risks.**
1. The stop rule triggers at day 5 on measured unit costs. 1,371 CPU-h are guessed, and if they double, the projection
   is about 5,750 CPU-h.
2. Both pile-up estimators fail, or miss their caps: no validated pile-up term beyond R07, and the "closure fails"
   paper.
3. A no-pile-up ceiling counts many events: the reach falls toward about 550 GeV. The day-15 rule pauses the study
   above B₅₀ = 300.
4. No public MET parameters from two sources: a MUST item is infeasible, and the study stops for you.
5. Schedule: Phase-3 development is the critical path and is bounded by three agents.

**Pointers.**
- Strategy: `phase1_strategy/outputs/STRATEGY_<final>.md` (§0 summary, §11 schedule, §12.1 the full question tables
  and the Q3 annex).
- `COMMITMENTS.md`.
- Budget script: `phase1_strategy/src/strategy_budget.py`.
- Reviews and arbiter verdicts: `phase1_strategy/review/`.
- Feasibility reports: `phase1_strategy/outputs/feasibility/`.

---

## Verdict input for the arbiter

PASS is not yet possible. One A item remains (F-A1) and six B items (F-B1 … F-B6), together with the residuals of the two
PARTIALLY RESOLVED items (N7 through F-A1, F-B1, F-B2 and F-B4; N18 through F-B6). Every fix is text or a sample row.
The added CPU is at most about 50 CPU-h (pool shares of the two additions, and Geant4 DIF development overlays). None of
the fixes reopens a brief §3 decision, loosens an F, or adds ρ ≥ 3 or ×100 samples. The total fixer effort is about
half a day. This can be a short fix pass followed by a verification by the arbiter, without a new full panel, if the
arbiter judges the fixes mechanical.
