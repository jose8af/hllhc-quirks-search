# Arbiter verdict: Phase 1 STRATEGY v5 (quirks v2), review cycle 5

Arbiter: Hugo, 2026-11-14 01:55. I am fresh to this panel and arbitrated no earlier cycle. I followed the Prompt
Template of `agents/arbiter.md` in full: adjudication cases 1–5, the structured table, the dismissal rules (§6.5.1),
the regression check (§6.7), the motivated-reasoning check and reviewer-pressure protection.

**Artifact.** `phase1_strategy/outputs/STRATEGY_gunnar_2026-11-14_00-50.md` ("v5", 2,943 lines; "l." means a line of
v5), `COMMITMENTS.md` ("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v5.txt`
("stdout"), `outputs/FIX_REPORT_cycle4_gunnar.md`.

**Cycle-4 verdict:** Greta, R1–R5 (`STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md`, "AV").

**Cycle-5 reviews** (all 2026-11-14 01:25):

| reviewer | role | A | B | C | ids used below |
|---|---|---|---|---|---|
| Hana | physics | 0 | 1 | 5 | Ph-B1, Ph-C1…C5 |
| Hedwig | critical | 0 | 0 | 7 | Cr-C1…C7 |
| Hiroshi | constructive | 0 | 2 | 10 | H-B1, H-B2, H-C1…C10 |

There is no plot validator: Phase 1 has no figures.

**What I read.** In full: `agents/arbiter.md`, `AGENT_RULES.md`, the study and phase `CLAUDE.md`, the three cycle-5
reviews, AV. Of v5: §0 (l.30–117), Table 4.4c with the scenario text (l.920–1000), §4.7 normalisation (l.1275–1290,
l.1548–1560), the B6 table head (l.1448–1458), [L13] (l.2256–2264), §11.3 (l.2536–2560), §11.6–§11.7
(l.2640–2730), §12.1 (l.2730–2800), §12.2 head, §12.5. Script [7] (l.385–430) and [9b] (l.540–800), stdout [7] and
[9b]. PLAN l.105–127. `06-review.md` §6.5. v1 record `TT/data/acts_stage4/analysis/C12FC_v1/background.json` →
`cprime.gamma.rate`.

**My own arithmetic.** Standard-library `python3 -I`, niced, on einstein. I loaded the script with `runpy` so that
every number below uses the script's own `pmf_pred`, `s95_pmf`, `s95_fixed`, `rfmt` and reach mapping. I first
checked the method against the plan's table: B = 10³ with a log-normal width of 0.2 gives s₉₅ = 346 and 320 GeV,
against PLAN l.122's 325 GeV, so the method reproduces the plan's σ_ln = 0.2 row. Code and full output are in the
session log `logs/arbiter_hugo_2026-11-14_01-55.md` (scratchpad `hugo_check.py` … `hugo_check4.py`).

**Rules followed.** No sub-agents, no git, nothing heavy. I wrote only this verdict and the session log.

**Verdict: ITERATE. 0 Category A, 3 Category B (T1–T3).** All three are fixes to sentences and table cells, plus
script print lines. They need 0 CPU-h. Not ESCALATE: the open questions are exactly the Gate-A questions, and v5 must
put them to the human honestly (§8).

---

## 1. Overall assessment

v5 carries out the cycle-4 work list faithfully. All three reviewers re-ran the script and found its output
byte-identical to `budget_stdout_v5.txt`. The critical reviewer found every one of the 64 diff hunks attributed, and
all 52 grep phrases of the fix report present. The design has not moved for two cycles.

What remains is one number and two consequences of it, all at the place the human will read first. The reach of the
expected branch is quoted without the normalisation width that the strategy itself assigns to that background. With
that width the expected deliverable has no reach beyond the existing bounds. The text also suggests that the first
upside branch avoids the day-15 pause, which by v5's own numbers it does not. And the calendar put to the human does
not contain the pause that v5 calls expected.

None of this is a defect of the design, and the expected outcome is not a defect either: it is what the human must
decide on. It is a defect only while the text understates it.

**Trend.** Merged Category A by cycle: 11 → 4 → 1 → 0 → 0. Merged B: 35 → 18 → 15 → 5 → 3.

---

## 2. Facts settled from sources (my own checks; VERIFIED unless tagged)

| question | evidence | ruling |
|---|---|---|
| Does v5 assign a normalisation width to the conversion background? | The conversions are inside the SM terms of B4 (§0 point 3, "the tracks of the hard-scatter vertex are in the real SM events of B4"). §4.7 point 4 (l.1279–1283) says: "ratio 0.84 … The difference between the two generators enters as the normalisation nuisance of the term." l.1554 lists the correlated nuisances "N_trig normalisation per process group (generator difference, K)". The B6 table (l.1450–1455) puts material on every SM term, and the conversion probability scales with x/X₀. | **Yes.** \|ln 0.84\| = 0.17 is the strategy's own width for the leading Z(νν)+jet group, before K, luminosity, material and closure. The width is not hypothetical (Ph-B1 point 2 stands). There is no collider data in this study, so no control region can constrain a generator normalisation: the width stays in the result. |
| Reach of (α1′) with that width | The conversion term is entered as a log-normal of width √(w² + 1/(m+1)), with DIF counted and everything else as in [9b]. At the max photon rate 0.379 (×339 / ×201): w = 0 gives the v5 rows (median 317 / 314, 84 % edge 273 / 270). w = 0.03 gives s₉₅ 641 / 644, i.e. **< 243 GeV**. w = 0.05 gives s₉₅ 944 / 948. **w = 0.17 gives s₉₅ 2,697 / 2,725 (84 %: 4,193 / 4,204) → < 243 GeV.** s₉₅ at B = 10⁵ known exactly is 621.5 (↔ 243 GeV), and PLAN l.122 gives "below 200 GeV" at B = 10⁴, σ_ln = 0.2. | **Below the plan's table (< 243 GeV), and below 200 GeV by PLAN's σ_ln = 0.2 row: at or near the existing bounds (≲ 180 GeV, PLAN l.116).** The statistics-only figures hold only for the counting width alone (≈ 0.02): at 0.03 the 84 % edge is already below 243 GeV. Hana's threshold of "0.03–0.05" is, by my run, ≈ 0.03 for the 84 % edge and ≈ 0.03–0.05 for the median. |
| Photon rate behind "≈ 10⁴" (Cr-C3, Ph-C1) | `cprime.gamma.rate`: value 0.3786 with choice "max over SM processes (conservative)", and `nt_weighted_mean` 0.2552. With 0.2552: conversions 6.42×10³; B₅₀ 6,814 / 7,076; median 342 / 338 [84 % edge 297 / 294]; fixed B 419 / 416 GeV. With w = 0.17: s₉₅ 1,819 / 1,834, i.e. < 243 GeV. | The rate choice moves the background by ×0.67 and the statistics-only edge by ≈ 25 GeV. **It does not change the conclusion under the planned width.** Because it is the same number the human reads, it goes into the same sentence as a range (§4, T1). |
| Upside rows with the same width (Case 5) | Width 0.17 on DIF and conversions, (α1) without credit: 84 % edge **372 / 312** (statistics-only: 455 / 421), median 429 / 369. Z(νν) m_H = 100 with 0.17: 84 % edge 454 (statistics-only: 523). | Every row of Table 4.4c is statistics-only in the same sense. For the upside rows the loss is 70–110 GeV, and they stay above the existing bounds. That needs one caption clause, not a rewrite of the rows (T1(c)). |
| Does the first upside branch avoid the pause? (H-B1) | Table 4.4c l.946: (α1) without credit has B₅₀ 587–975. stdout [9b]: DIF 385 / 647 and conversions 183 / 308. The class limit is B₅₀ ≤ 300 (l.2699–2702). With credit, (α1) has B₅₀ 51–74 and (α1′) has 580–599. | **No.** Removing the conversions entirely leaves DIF at 385–647 events, above the class. The pause is avoided only by branches with B₅₀ ≤ 300: (α1) with fit-probability credit, (β), m_H ≲ 125 and the empty ceilings. To reach the (α1) conversion level a veto must remove 96.8–98.1 % (×31–52) of the conversions, and even that is not enough by itself. |
| Does the expected pause cost calendar time? (H-B2) | §11.7 rule 1: "the study pauses and the user is asked". Q2 (a): "≈ 2 days of turnaround". Script [7] FIXED (l.405–410) has no day-15 entry; the Gate-B turnaround is 2 days. | **Yes, by v5's own rule**: the study pauses, so the pause adds its turnaround. Calendar 57.8 + 2.0 = **59.8 days** (MUST only 58.9, full SHOULD 60.1). |
| H-C1 part 3 funding | The 100 CPU-h "enlarged development closure samples" are already a booked MUST item (script l.171, ≈ 5,960 B1-type events). | 1,000 γ overlays (1,000 × 25.2 s = 7.0 CPU-h) are therefore an **addition**: 4,609.4 → 4,616.4 CPU-h and threshold 5,992 → 6,001, if accepted. They cannot be taken from that allowance without displacing a MUST sample. |

---

## 3. R1–R5: final status

| # | Ph / Cr / Co | final | reason |
|---|---|---|---|
| R1 | P / R / R | **PARTIALLY RESOLVED → T1** | Case 4: both readings are right on what they checked. The fixer executed AV's work list verbatim, and Cr and Co checked exactly that. But the leading sentence that AV prescribed (AV §5.2) omits the fact that AV's own §2 said "belongs in the headline of that branch": that the reach is statistics-only. §2 above shows that the width the strategy itself commits to removes all reach beyond the existing bounds. R1's objective, an honest headline, is therefore not yet met. The residual originates in the arbiter's text, not in the fixer's work, and it is carried as T1. Every other part of R1 (the eight ordered points, the fall test, the mapping, the e^(±1) rows, the m_H = 1000 row, the Df-9 EST, rule 1, the wording greps) is resolved and was reproduced three times. |
| R2 | R / R / R | **RESOLVED** | Case 1. The three annex rows and the B4-e size (4,560 events) were reproduced. |
| R3 | R / R / R | **RESOLVED** | Case 1. The residue in H-C8 is C (§5). |
| R4 | R / R / R | **RESOLVED** | Case 1. |
| R5 | R / R / R | **RESOLVED** | Case 1. 4,609 / 5,992 / 57.8 d reproduced three times. |

---

## 4. Structured adjudication table

Fix types: (T) text or table; (S) a number printed by `strategy_budget.py`; (G) a Gate-A line.

| # | finding | source | their cat | final | type | rationale |
|---|---|---|---|---|---|---|
| **T1** | **The reach of the expected branch is quoted without the normalisation width the strategy itself assigns to that background.** With ≈ 0.17 (generator difference, §4.7) the reach is below 243 GeV, at or near the existing bounds. The leading sentence omits this entirely. §0 and Q2 give it only as a hypothetical "if … 0.2". Q2 option (b) promises "≈ 270–390 GeV". §12.5 point 3 says "below the existing bounds" beside 270 GeV (Cr-C1). The figure "≈ 10⁴" uses v1's maximum-over-process photon rate (Cr-C3, Ph-C1). The upside rows are statistics-only too (Case 5, arbiter). | Ph-B1; H-C3; Cr-C1, Cr-C3; Ph-C1; arbiter (Case 5) | B; C; C, C; C | **B** | S+T+G | Case 2. I side with the physics reviewer. This is the reach of the deliverable the human is asked to choose in Q2, and it reverses the FRAMING message ("reaches X GeV, beyond existing limits"). Cr and Co rated it C because the fact is "in the text", but it is there only as a conditional the strategy's own plan makes unconditional. That is the template's "limitation acknowledged in prose but not reflected in the result". It is B and not A: no result is computed from it, and the default (a) pauses and asks again with measured counts. The rate range (Cr-C3) is ruled into the same sentence: it is the same number, it costs no extra clause, and the weighted mean (v1's own reported mean) is the expectation, while the maximum is a conservative choice. |
| **T2** | **Q2 and §0 imply that the first upside branch, or a conversion veto, avoids the day-15 pause. By v5's own numbers it does not** ((α1) B₅₀ 587–975; DIF alone 385–647). The success condition of option (c) is not stated. | H-B1; Ph-C2; H-C4 | B; C; C | **B** | T+G | Case 3, verified (§2). This is the central question of the gate, "does anything avoid the pause?", and v5's own l.993 contradicts its own Q2. One clause in each place fixes it. |
| **T3** | **The calendar put to the human in Q4 (58 days) omits the ≈ 2 days of the day-15 pause that v5 calls the expected branch under the recommended Q2 (a).** | H-B2 | B | **B** | S+T+G | Case 3, verified (§2). The approved CPU figure already includes the reserve "that the default plan spends" (P13), so by the same rule the approved calendar includes the turnaround that the default plan expects. Otherwise the expected outcome would be reported as an overrun under D6. |

**C items, all assessed.** Each is applied in the T-pass (§6), deliberately left for later (§6, with the reason it is
safe), or ruled on separately: H-C1 (§7).

**Dismissals: none.** No B is dismissed. No C is dismissed as wrong; the C items that are left for later are listed
with their cost and the reason it is safe to leave them.

**Reviewer-pressure protection.** Ph-B1 contradicts the text that the previous arbiter prescribed. The fixer's
verbatim compliance is not evidence against it, and neither is the fact that two reviewers checked compliance. My own
run (§2) confirms Ph-B1 independently. It stands.

---

## 5. What the human must be told at Gate A (the honest statement)

> On v1's own counts and v1 placeholder efficiencies, the default plan is expected to end at a large **measured**
> background of hard-scatter photon conversions, **≈ 0.7–1.0×10⁴ events**. With the normalisation uncertainty that
> the strategy itself assigns to that background (≈ 17 %, the generator difference), this gives **no mass reach
> beyond the existing bounds** (below 243 GeV, at or near ≈ 180 GeV). The often-quoted ≈ 270–300 GeV (84 % edge) and
> ≈ 390–420 GeV (background known exactly) are statistics-only values. The day-15 rule is expected to pause the study
> before production. Removing the conversions alone does not avoid the pause; decays in flight alone are 385–647
> events. A reach beyond the existing bounds in that case needs option (c): a conversion-removing conditional that
> rejects ≳ 97 % of conversions, together with a credit or a faster fall for the decays in flight. Its rejection has
> not been measured. The pilot measures the deciding numbers by day 7 (preliminary) and day 15 (binding).

This is not a defect of the strategy. It is the decision of Q2, and the human must read it before answering.

---

## 6. Work list for the fixer (priority order; touch nothing else)

General rules (unchanged):
- Write `STRATEGY_<fixer>_<timestamp>.md` ("v6"), update COM, the script, `budget_stdout_v6.txt` and a fix report
  with a grep phrase for every "stated in" claim.
- Trace every change to T1–T3 or to an adopted C item below.
- Every number shown to the user comes from a printed script line. My values are [E]; the script's are binding, and
  they must agree with mine to within rounding (the generator seed is fixed at 7, so the agreement should be exact).
- Where my text quotes a printed value, the fixer copies the printed value.

### 6.1 Script (one block in [9b], one line in [7], one rider line; 0 CPU-h)

1. **[9b], after the two "v5 (R1): the same at fixed B" lines, a "v6 (T1)" block.**
   - For each (α1′) tag (×339, ×201) and for the photon rate factor f ∈ {1, 0.25518676537664065 / 0.3786327036399709}
     (`cprime.gamma.rate.nt_weighted_mean` / `.value`; read them from the JSON or hard-code them with the key in a
     comment), print the no-credit row in two forms:
     - (i) counted, as now: B₁₆ / B₅₀ / B₈₄, median and 84 % s₉₅ and reach, fixed-B reach;
     - (ii) with the conversion term as a log-normal of width √(w² + 1/(m + 1)), m = g/kz, for w = 0.03, 0.05 and
       **0.17**. In this form DIF stays counted, `kap_nodif` and `PU9` are unchanged, and the term is entered as
       `(g, width, None)` in `lnn`.
     - Label w = 0.17 "normalisation width of the SM terms, |ln 0.84| (generator difference, §4.7); K, luminosity and
       material not included". Where s₉₅ exceeds 621.5, print "< 243 (beyond the plan's table; PLAN σ_ln = 0.2 row:
       below 200 GeV at B = 10⁴)".
     - Expected values (mine). Rate 1: w = 0.03: s₉₅ 641 / 644; w = 0.17: s₉₅ 2,697 / 2,725 → < 243. Rate 0.255:
       conversions 6.42×10³; B₅₀ 6,814 / 7,076; median 342 / 338 [297 / 294]; fixed B 419 / 416; w = 0.03: median
       281 / 280 [< 243]; w = 0.17: s₉₅ 1,819 / 1,834 → < 243.
   - The same width 0.17 on the DIF and conversion terms of (α1) without credit, and on the Z(νν) ceiling of the
     m_H = 100 row (log-normal of width √(0.17² + 1/(m + 1)) around κ(m + 1)). Expected (mine): (α1) median 429 / 369
     [84 % edge 372 / 312]; m_H = 100: median 513 [454].
   - Required conversion rejection to the (α1) level: 9,527/308 = ×31 and 9,527/183 = ×52 (96.8–98.1 %).
   - Extend the "HEADLINE v5" line, or add "HEADLINE v6", with the w = 0.17 reach of (α1′), the rate range of B₅₀ and
     the statistics-only ranges (84 % edge 270–297; fixed B 392–419).
2. **[7], after the three CAL lines:** "v6 (T3): expected branch under Q2 (a): + 2.0 d day-15 pause turnaround (the
   Gate-B turnaround) → MUST + SHOULD reduced 59.8 d = 8.5 weeks; MUST-only 58.9; full 60.1". Expected: 59.8 / 58.9 /
   60.1.
3. **Rider line (§7):** "H-C1 rider (if accepted at Gate A): 1,000 γ development overlays 1000 × 25.2 s = 7.0 CPU-h,
   added: approved 4,616 CPU-h, threshold 6,001; calendar unchanged (idle pre-freeze capacity 1,351 core-h);
   the veto measurement on the stored pilot records and the day-7 question 0 CPU-h". Expected: 4,616.4 / 6,001.3.
4. **H-C9:** the label "v4 approved figure" (script l.299) becomes "approved figure".

### 6.2 Strategy text (exact replacements; printed values replace mine)

**T1-a. Leading sentence, §0 l.91–94.** Replace the bold text with:

> **Expected (ESTIMATE, v1 placeholder efficiencies): by v1's own counts the default plan's background at R08–R09 is
> led by hard-scatter conversions, ≈ 0.7–1.0×10⁴ events (v1's N_trig-weighted and maximum photon rates). With the
> normalisation uncertainty this strategy itself assigns to that background (≈ 0.17, the generator difference of
> §4.7) the reach is below 243 GeV, at or near the existing bounds of ≈ 180 GeV; the ≈ 270–300 GeV at the 84 % edge
> (≈ 390–420 GeV for a background known exactly) hold only for its counting width alone. The day-15 rule is expected
> to pause the study before production, and removing the conversions alone would not avoid the pause.**

**T1-b. §0 "Expected" paragraph, l.64–67.** Replace "**≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge
(median ≈ 315 GeV; ≈ 390 GeV if that background were known exactly, below 200 GeV if it carries a systematic width of
0.2, PLAN l.122)**, and the day-15 rule is expected to pause the study before production (§11.7, Q2)." with:

> **≈ 0.7–1.0×10⁴ events (v1's N_trig-weighted and maximum photon rates, 0.255 and 0.379 per event). The strategy
> gives this background the normalisation nuisance of its SM terms (§4.7: the generator difference 0.84 for
> Z(νν)+jet, |ln 0.84| = 0.17, before K, luminosity and material). With a width of 0.17 the reach is below the plan's
> table (< 243 GeV; below 200 GeV by its σ_ln = 0.2 row, PLAN l.122), i.e. at or near the existing bounds, and it is
> already below 243 GeV at a width of 0.03. The statistics-only values, ≈ 270–300 GeV at the 84 % edge (median
> ≈ 315–340; ≈ 390–420 GeV for a background known exactly), hold only for the counting width of ≈ 0.02** [E, script
> [9b], v6 lines]. The day-15 rule is expected to pause the study before production (§11.7, Q2).

At the end of the upper-branch list, before "Existing bounds lie below about 180 GeV", insert:

> These upper branches are statistics-only in the same sense: with the width 0.17 on the counted terms the (α1) 84 %
> edge is ≈ 310–370 GeV instead of 420–455, and the m_H = 100 row is 454 instead of 523 GeV; they stay above the
> existing bounds [E, script [9b], v6 lines].

**T2-a. §0 "The pause." paragraph, l.82–85.** Replace "By v1's conversion counts this is the expected branch, unless
the v2 pilot measures a steeper fall or a conversion-removing conditional (the displaced-vertex veto B3-b, the fit
probability) is tested close to where it is applied. In that case the paper is the plan's "real background" outcome
(PLAN §9: a measured background, the reach at that B, the sideband recipe as the way out)." with:

> By v1's conversion counts this is the expected branch. The pause fires in the first upper branch too ((α1) without
> credit, B₅₀ 587–975, of which decays in flight 385–647), so neither a steeper conversion fall nor a
> conversion-removing conditional (the displaced-vertex veto B3-b, the fit probability) avoids it on its own. It is
> avoided only if the projected B₅₀ is at most 300, as in (α1) with fit-probability credit (51–74), (β) and the
> empty-ceiling case. If the pause fires and the user chooses Q2 (b), the paper is the plan's "real background"
> outcome (PLAN §9: a measured background, the reach at that B, at or near the existing bounds with the planned
> width, the sideband recipe as the way out).

**T1-c. §0 point 3, l.57–61.** Change "0.04–0.06" to "0.04–0.07" (Cr-C4: the printed μ are 0.038 / 0.065). After
"the background is ≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c)", insert "(with v1's maximum-over-process photon
rate; ≈ 6.4×10³ conversions and B₅₀ ≈ 6.8–7.1×10³ with its N_trig-weighted rate)".

**T1-d. Table 4.4c.**
- Caption, append: "*Statistics-only:* the rows carry the counting widths and the pile-up width, not the
  normalisation nuisances of §4.7 (generator difference ≈ 0.17 for the SM terms, K, luminosity, material), which act
  on every counted term. Script [9b] v6 lines give the effect: (α1′) below 243 GeV already at a width of 0.03; (α1)
  without credit, 84 % edge 372–312 GeV; m_H = 100, 454 GeV."
- (α1′) no-credit row, label: append "; v1's maximum-over-process photon rate 0.379 (with its N_trig-weighted 0.255:
  conversions 6.4×10³, B₅₀ 6,814–7,076, reach 342–338 [297–294], 419–416 at fixed B)".
- (α1′) no-credit row, reach cell: "**317–314 [273–270]; ≈ 390 (394–392) at fixed B; < 243 with the planned
  normalisation width 0.17 (already at 0.03)**".

**T1-e. Scenario text.**
- l.962: "it is the branch the v1 record supports" → "it is the branch the v1 conversion record supports, with the
  more favourable DIF reading (the PV-placement and attribution caveats act on DIF)" (Ph-C4, wording part).
- l.973–974: replace "A reach at a 10⁴-event background is statistics-only: at σ_ln = 0.2 the plan's table gives
  below 200 GeV (PLAN l.122)." with "A reach at a 10⁴-event background is statistics-only. The term carries the
  normalisation nuisance of its SM processes (§4.7, ≈ 0.17); with it the reach of (α1′) is below 243 GeV (below
  200 GeV by PLAN l.122), and it is so already at a width of 0.03 [E, script [9b], v6 lines]."

**T2-b. §4.4 "What is not known", l.993.** After "(α1) without credit is above it too", insert "; removing the
conversions alone does not bring B₅₀ below 300 (decays in flight 385–647 events)".

**T1-f / T2-c. Q2 stem, l.2743–2751.** Replace from "By v1's own counts" to "(§0, Table 4.4c, §11.7)" with:

> By v1's own counts (ESTIMATE, v1 placeholder efficiencies, best Λ per mass), hard-scatter conversions leave
> ≈ 0.7–1.0×10⁴ background events at the R08–R09 selections. v1 counted 86 → 13 → 2 conversions per 500 events at
> R05–R07, a fall of ×6.5 per width step against ×200–340 for the pile-up background, and a pile-up-like fall is
> rejected at p ≈ 10⁻³. With the normalisation width this strategy assigns to that background (≈ 0.17, §4.7) the reach
> is below 243 GeV, at or near the existing bounds; the statistics-only values are ≈ 270–300 GeV at the 84 % edge and
> ≈ 390–420 GeV for a background known exactly. The day-15 rule (preliminary at day 7) is expected to pause the study
> before production. The day-7 reading counts own hits before CKF (Df-9) and may be ×5–50 above this figure.
> Upside (statistics-only; with the width 0.17 the (α1) edge is ≈ 310–370 GeV): if the conversions and decays in
> flight fall like the pile-up background, ≈ 420–455 GeV at the 84 % edge (median 470–500; ≈ 400–570 for the factor-e
> size uncertainty). This branch also pauses at day 15 (B₅₀ 587–975, of which decays in flight 385–647), so a
> conversion veto alone does not avoid the pause. Only branches with B₅₀ ≤ 300 do: (α1) with fit-probability credit;
> (β), Z(νν) tested and the other ceilings at 10–100 simulated counts, conditional on the promotion model being
> submitted, ≈ 705–640 GeV; and every ceiling empty, ≈ 710 GeV (median 790), an upper edge. Existing bounds lie below
> about 180 GeV (R-20 pending). (§0, Table 4.4c, §11.7)

(This also applies H-C2, H-C5 and Cr-C6.)

**T1-g. Q2 option (b), l.2757–2758.** Replace "the reach at that B (≈ 270–390 GeV as above), the sideband recipe as
the way out." with:

> the reach at that B, expected below 243 GeV, at or near the existing bounds, with the planned normalisation width
> (≈ 270–420 GeV only for a background with no width beyond its counting width), and the sideband recipe as the way
> out. In the expected case this paper reports no mass reach beyond the existing bounds; (c) is then the only route
> in this strategy to one.

**T2-d. Q2 option (c).** After "Paper: the bounded "middle" outcome (upper branches above) if it works, otherwise
(b).", insert:

> It works if the projected B₅₀ is at most 300. That needs the conversions reduced by ×31–52 (96.8–98.1 %) **and** the
> decays in flight (385–647 events) reduced by a credit or a faster fall. The veto's rejection has not been measured.

**Q2, last sentence (H-C6).** "(≈ +25 GeV)" → "(median 790 → 814 GeV, script [9b])".

**Q2, rider (§7).** Append after the last line of Q2:

> *Optional rider (recommended by the cycle-5 review, not part of the default; answer "Q2 ● + rider" to accept):*
> (1) if the day-7 preliminary B₅₀ is at least 3,000 events (10× the class), the choice between (b) and (c) is put to
> you at day 7 instead of day 15, and the day-15 rule stays binding; (2) channel (i) reports by day 12, as a
> development number and not a credit, the pilot's ceiling counts split by truth origin and the fraction of
> conversion-attributed configurations at R05–R07 with a reconstructed two-prong vertex (0 CPU-h, on the stored
> records); (3) 1,000 γ development overlays (seeds disjoint from 4a) check v1's ×6.6 fall with pile-up on the v2
> chain by day 12 (+7.0 CPU-h: approved 4,616, threshold 6,001). Gain: under (c), up to ≈ 8 days earlier [E: day 15 −
> day 7]. Cost of declining: those days, nothing else.

**T3. Calendar.**
- **Q4, l.2779–2787.** "and **58 days** (against your 2–4 weeks; …)" becomes:

  > and **60 days** (57.8 without the day-15 pause; under the recommended Q2 (a) the pause is the expected branch and
  > costs ≈ 2 days of turnaround, so the approved calendar includes it; a redesign under Q2 (c) adds its own time,
  > reported at day 15) (against your 2–4 weeks; 43.5 days have no critical-path production: …)

  In the alternatives: "MUST only, 4,176 CPU-h and 59 days (57 without the pause)" and "full SHOULD …, 5,123 CPU-h and
  60 days (58 without)".
  Gloss the labels in one parenthesis each (H-C7): "[DP1] (B5 sideband reduced, §4.8), [DP2] (B6 detector variations
  reduced, §4.9), [DP4] (S4, S5 not included), [DP5] (second hadronisation model at generator level after an install
  attempt)".
  Add after "(§11)": "; the stop conditions of brief §7 are quoted in §11.6" (Cr-C5).
- **§0 Calendar bullet, l.106.** "about 8 weeks from Gate A to Gate C (58 days;" → "about 8.5 weeks from Gate A to
  Gate C (60 days, of which ≈ 2 are the expected day-15 pause; 58 days without it;".
- **§11.2 proposed-variant row, l.2500.** "57.8 days = 8.3 weeks" → "57.8 days = 8.3 weeks (59.8 with the expected
  day-15 pause)".
- **§11.3, l.2570.** "**Calendar estimate: about 8 weeks from Gate A (58 days).**" → "**Calendar estimate: 60 days
  from Gate A in the expected branch (57.8 days plus the ≈ 2-day turnaround of the day-15 pause under Q2 (a)); 58 days
  if the pause does not fire.**"
- **§11.6, l.2657.** "and 58 days" → "and 60 days (57.8 days plus the ≈ 2-day turnaround of the expected day-15
  pause; a redesign under Q2 (c) is not included and is reported as an overrun)".
- **COM ST-1.** The same clause.

**§12.5 point 3 (T1; Cr-C1).** Replace the point with:

> 3. The large samples show passing single-interaction events at a rate that leaves B ≫ 10³: a measured background
>    (plan outcome "real background"). By v1's conversion counts this is the expected branch ((α1′) of Table 4.4c:
>    ≈ 0.7–1.0×10⁴ events, ESTIMATE, v1 placeholder efficiencies). With the planned normalisation width (≈ 0.17) the
>    reach is below 243 GeV, at or near the existing bounds; it is ≈ 270–300 GeV at the 84 % edge statistics-only.
>    The day-15 rule pauses the study (Q2).

### 6.3 C items applied in the same pass (quick; each removes a real ambiguity or contradiction)

- **Cr-C1, Cr-C3, Cr-C4, Cr-C5, Cr-C6; Ph-C1, Ph-C2; H-C2, H-C3, H-C4, H-C5, H-C6, H-C7:** folded into T1–T3 above.
- **Ph-C4 (wording part):** T1-e.
- **Ph-C5, [L13] l.2260–2262.** Replace the sentence from "[L13]" through "sample-size limited." with: "[L13] With
  zero counts in the large samples the leading terms are bounds of about 13 events in total, more if a ceiling H counts
  (Tables 4.4a, 4.4c): the result is then sample-size limited. If decays in flight and conversions behave as in v1,
  the leading term is a counted background of ≈ 10⁴ events and the result is a measured background (§12.5 point 3)."
- **H-C10, §11.7 rule 1.** After "reported in `STATUS.md`", insert: "; it is conditional on C1 PASS for the
  no-pile-up family (C′₀), and if that family fails, the pilot is re-read (or re-run, 61 CPU-h in idle capacity) after
  remediation".
- **Cr-C2.** l.16: add "or Gunnar" and the v6 fixer to the list of authors. §12.2 l.2837: "(entries [<v6 fixer>] and
  [Gunnar] for the last two versions, [Fiona], [Emeric], [Dmitri] and [Brigitte] for the earlier ones)".
- **H-C9:** §6.1 item 4.

### 6.4 C items deliberately left for later (why it is safe)

| item | what | why it is safe now | when |
|---|---|---|---|
| Ph-C3 | physics expectation for the conversion fall (sagitta, w ∝ 1/p_T) | explanatory only. The pilot measures the fall at R05–R09 on 2.3×10⁶ Z(νν) events by day 7, and the binding rule reads the measured fall, not an expectation. Its direction, if anything, makes the extrapolation conservative. No number or decision changes. | Phase 2 pilot write-up |
| Ph-C4 (downside part) | (α2) as the downside branch in §0 / Q2 | after T1, the expected branch already has no reach beyond the existing bounds, so a lower downside changes no choice in Q2. (α2) stays in Table 4.4c. | — |
| H-C8 (a) | hand-over variant used for the pilot's DIF/NI hits | Z(νν), and so the conversion question, is unaffected. At worst 18.8 CPU-h of DIF/NI pilot events are regenerated inside the Phase-3 development allowance, and the variant is frozen in Phase 3 anyway. | Phase 3 (date the freeze "by day 12") |
| H-C8 (b), (c) | the near-pass overlays booked in Phase 2 although made in Phase 3; classification CPU not named | bookkeeping between phases. No total and no date changes (7 CPU-h, a few ms per event). | Phase 2 plan |
| Cr-C7 | COM tags "(Q2)" on T2-h and TG-1 | a cross-reference label. COM is re-read at the start of each phase, and the binding text of both rows is unambiguous. | orchestrator, with the Gate-A package |
| (none) | whether Phase-3 channels continue during the day-15 pause, which could absorb part of the 2 days | that would be a change of the pause rule ("the study pauses"), not a text fix; the calendar is set by the rule as written. | Gate-A package may offer it |

Cost check (§6.5.1). Every item left above costs under one agent-hour as text, but none of them changes a number, a
default or a choice the human is asked to make. They are left to keep the cycle-6 verification closed, not because of
their cost.

---

## 7. Ruling on H-C1 (earlier decision point at day 7; veto measured on the pilot records; 1,000 γ overlays)

**Ruling: not adopted into the strategy as a schedule change. Recorded as an optional rider to Q2 that the human
accepts or declines at Gate A (text in §6.2), with its cost printed by the script.**

Reasons:
1. Part (1) changes when the human is asked and on what inputs: a preliminary classification and v1-based pile-up
   rows. That is the human's call about their own time, not the panel's.
2. Adopting all three parts as binding design at cycle 5 would add a new threshold (3,000), a new measurement and a
   new sample. Each would need full review, which is the opposite of closing the gate.
3. As a rider its effect is bounded and stated: 0 days and 0 CPU-h for parts (1) and (2), and +7.0 CPU-h for part (3).
   Part (3) is an addition, because the 100 CPU-h development allowance is already a booked MUST sample (§2).

**If the human accepts:** the approved figure becomes **4,616 CPU-h** and the 1.3× threshold **6,001 CPU-h** (script
rider line; expected 4,616.4 / 6,001.3), and the calendar is unchanged. The orchestrator then adds the rows to COM.

**If the human declines:** nothing changes. The default Q4 figures stay 4,609 / 5,992.

Part (2) costs nothing and produces the number on which Q2 (c) depends. I recommend it most strongly, and the rider
says so.

---

## 8. Regression, motivated-reasoning and convergence checks

**Regression triggers (§6.7).** Phase 1 has no results: validation failure, > 80 % systematic, GoF and bin exclusion
do not apply. No tautological validation is introduced by v5 (Cr §2 diff, confirmed by Ph Part 2). There is no
earlier phase to regress to. **None met.**

**Motivated reasoning.** For the fifth cycle the summary layer quotes the gentler member of a pair: statistics-only
reach, maximum rate silently, an upside "that avoids the pause". This time the gentleness was written into the
arbiter's own prescribed sentence and copied verbatim, so the critical check of compliance could not catch it.

I checked my ruling against the opposite bias:
- The width 0.17 is the strategy's own committed nuisance, not an inflation. It is measured (FEAS_B, 12.21 vs
  14.6 pb), and K, luminosity and material would only add to it. In a simulation-only study no data constrain it.
  The conclusion holds at both photon rates, and at a width of 0.03 already.
- I did not lower the upside rows below what the same width gives: they stay above the existing bounds, and the text
  says so.
- The ● stays on "pause and ask", which is right: the pilot may still measure a steeper fall than v1.

**Competing group.** A competing group would have a measured conversion rejection. That is Q2 (c), and with the rider
its handle is measured on the pilot records by day 12.

**Brief compliance.** D4 unchanged. D6: the calendar now includes the expected pause (T3). §7 stop rules: the
threshold is unchanged at 5,992, or 6,001 with the rider. Nothing discarded returns.

**FRAMING.** FRAMING l.38–40 expects "it reaches X GeV, beyond existing limits". After T1 the strategy says plainly
that the expected branch does not, which is exactly what Gate A must decide (Q2). That is not a defect.

---

## 9. Cycle 6: minimal legitimate re-review

This is review cycle 5 (warn at 3, strong warning at 5, hard cap at 10; `06-review.md` §6.5). The strong warning is
noted. Merged A by cycle: 11 → 4 → 1 → 0 → 0. The critical reviewer of this cycle found no A or B. The remaining B are
sentences, cells, three script print lines and one label; they need no CPU. The protocol still requires a documented
re-review after an ITERATE, and the Phase-1 tier is the 4-bot panel. The re-review is therefore by **three fresh,
independent reviewer sessions (physics, critical, constructive) and a fresh arbiter**. It is not an arbiter-only check,
and it does not reuse the cycle-5 sessions, which are anchored.

What can legitimately be narrowed is the scope each reviewer verifies:

| role | verifies exactly | method |
|---|---|---|
| physics | **T1** and the physics of **T2**: the v6 [9b] lines (the method of §6.1 item 1, a log-normal on the conversion term, DIF counted; values equal to mine in §6.1 within rounding); that "< 243 / below 200 GeV" follows from s₉₅ ≫ 621.5 and PLAN l.122; the leading sentence, Q2 stem, (b), (c) and §12.5 point 3 against those lines; the (c) success condition (×31–52 and DIF) | re-run the script, diff against `budget_stdout_v6.txt`, read the T1/T2 locations |
| critical | the **v5 → v6 diff** of strategy, COM and script: every hunk maps to T1–T3, an item of §6.3, or the rider; stdout differs from v5 only by the new v6 lines, the [7] line, the rider line and the H-C9 label (every other printed value identical); every number in the new text is on a printed line; greps of the superseded phrases ("systematic width of 0.2", "≈ 270–390 GeV as above", "≈ +25 GeV", "8 weeks (58 days)", "about 8 weeks from Gate A (58 days)", "0.04–0.06") return only history rows; **T3** chain (59.8 / 58.9 / 60.1 identical in §0, §11.2, §11.3, §11.6, Q4, COM ST-1) | diff, greps, fresh run |
| constructive | §0 leading sentence and §12.1 Q2 and Q4 read as the human: is it plain that the expected deliverable has no reach beyond the existing bounds; that no (α) branch avoids the pause; what (a), (b), (c) each deliver and cost; that the rider is optional, costed and answerable in the same line; that the calendar shown includes the expected pause | read as the human, nothing else |
| arbiter | the three reviews against T1–T3 and §6.3; PASS if all are resolved and the diff is clean | — |

Each reviewer raises a new finding only if it is a regression introduced by the fix, a factual error in a number shown
to the user, or a genuine Category A. Everything else is C, recorded for the Gate-A package. A partial fix of one item
in cycle 6 should again be a short focused fix with the same narrow panel. This narrows scope only: any genuine defect
found in the verified locations blocks as before.

**Settled now as rules (not to be reopened):**
- The expected-branch reach is stated with the strategy's own normalisation width.
- The photon-rate range 0.255–0.379 is quoted.
- The approved calendar includes the expected day-15 turnaround.
- H-C1 is a Gate-A rider, not default design.

---

## 10. Mapping of reviewer items

| item | merged / disposition | | item | merged / disposition |
|---|---|---|---|---|
| Ph-B1 | T1 | | H-B1 | T2 |
| Ph-C1 | T1 (rate range) | | H-B2 | T3 |
| Ph-C2 | T2 ((c) success condition) | | H-C1 | rider (§7) |
| Ph-C3 | left (§6.4) | | H-C2 | T1-f (×5–50 clause) |
| Ph-C4 | wording applied; downside left | | H-C3 | T1-g |
| Ph-C5 | [L13] applied | | H-C4 | T2-d |
| Cr-C1 | T1 (§12.5 point 3) | | H-C5 | T1-f (why clause) |
| Cr-C2 | applied | | H-C6 | applied (790 → 814) |
| Cr-C3 | T1 (range in the same sentence) | | H-C7 | T3 (Q4 gloss) |
| Cr-C4 | T1-c | | H-C8 | left (§6.4) |
| Cr-C5 | T3 (Q4 pointer) | | H-C9 | applied (script label) |
| Cr-C6 | T1-f | | H-C10 | applied (§11.7 rule 1) |
| Cr-C7 | left (§6.4) | | arbiter Case 5 | T1 (upside caption clause) |

---

## 11. Verdict

**ITERATE.**
- **Category A: none.**
- **Category B, all to be fixed before PASS, in priority order:**
  - **T1:** the expected-branch reach is stated with the strategy's own normalisation width ≈ 0.17, so the reach is
    below 243 GeV, at or near the existing bounds. The statistics-only 270–300 / 390–420 GeV are labelled as such, and
    the photon-rate range ≈ 0.7–1.0×10⁴ events is quoted. This applies to the leading sentence, §0, Table 4.4c, the
    scenario text, Q2 stem and (b), and §12.5 point 3, with script [9b] v6 lines.
  - **T2:** no (α) branch and no conversion veto alone avoids the day-15 pause, and the success condition of (c) is
    stated.
  - **T3:** the approved calendar is 60 days (59.8), including the expected pause; 57.8 without it.
- The C items of §6.3 are applied in the same pass. H-C1 goes in as an optional Gate-A rider (+7.0 CPU-h if accepted:
  4,616 / 6,001).
- **Cycle 6:** a narrow 4-bot re-review by fresh sessions, as in §9.
- **What the human must be told** is the box in §5.
