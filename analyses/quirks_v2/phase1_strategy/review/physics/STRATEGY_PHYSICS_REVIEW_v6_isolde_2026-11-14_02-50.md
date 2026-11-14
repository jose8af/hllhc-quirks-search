# Physics review: Phase 1 STRATEGY v6 (quirks v2), review cycle 6

Reviewer: Isolde (physics), 2026-11-14 02:50. Fresh session; I saw no earlier cycle. I followed the Prompt Template of
`agents/physics_reviewer.md`. As that template requires, I did not read the methodology spec or the conventions.

**Artifact.** `phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("v6"; "l." means a line of v6). Compared
against v5, `STRATEGY_gunnar_2026-11-14_00-50.md`.
**Inputs.** FRAMING; arbiter verdict v5 (Hugo), "AV"; physics review v5 (Hana); `FIX_REPORT_cycle5_ingrid.md`;
`src/strategy_budget.py` [9b], l.575–876; v1 `C12FC_v1/background.json` → `cprime.gamma.rate`;
`publication_plan/publication_plan.tex` l.112–124 (PLAN reach table).
**Scope (AV §9 and the task).** T1, the physics of T2, consistency of the expected-outcome statement, and a physics
reading of the v5→v6 diff. Phase 1 has no figures, so figure inspection does not apply.

## Verdict

- **T1: RESOLVED.**
- **T2: RESOLVED.**
- **New findings: 0 A, 0 B, 5 C.**
- **Judgment: approve for execution subject to Gate A.** Nothing blocks.

---

## 1. Reproduction

- **Script.** `nice python3 -I src/strategy_budget.py` ran on einstein with exit code 0. Its output is
  **byte-identical** to `outputs/budget_stdout_v6.txt` (`diff` is empty apart from my own exit-code marker).
- **Method of the v6 block** (script l.786–845), read in full:
  - (α1′): DIF enters counted, as `(K_DIF, d/K_DIF)`. The conversion term enters `lnn` as
    `(g, sqrt(w² + 1/(m+1)), None)` with m = g/kz. `kap_nodif` and `PU9` are unchanged. The photon-rate factor is
    0.25518676537664065 / 0.3786327036399709.
  - (α1) upside: DIF and conversions are both log-normal with the same width form.
  - Z(νν) m_H = 100: the term is centred on kz(m+1).
  - This is the method AV §6.1 ordered, and it is the physically right one: a counted term times a normalisation
    nuisance that no data can constrain. A log-normal is the standard choice for that nuisance.
- **v1 record.** `cprime.gamma.rate.value` = 0.3786 (choice "max over SM processes (conservative)"; it is the ttbar_1l
  rate). `nt_weighted_mean` = 0.2552. Both match the values in the script and in the text.
- **PLAN table** (`publication_plan.tex` l.120–121). The σ_ln = 0 row gives 393 GeV at B = 10⁴ and 243 GeV at
  B = 10⁵. The σ_ln = 0.2 row has a dash at B = 10⁴, which the caption defines as "below 200 GeV". It also says
  "Existing bounds … lie below about 180 GeV". The statements "< 243 GeV" and "below 200 GeV by its σ_ln = 0.2 row" are
  therefore sourced correctly.
- **Independent check, not using the script's Monte Carlo.** I used a lower-tail approximation. At the
  Poisson-median count, CLs = 0.05 requires P(n ≤ B_med | s+b) ≈ 0.025, so s₉₅ ≈ √[(g(1 − e^(−1.96 σ)))² +
  (1.96√B)²], with σ = √(w² + 1/(m+1)). The reach is read log-linearly between s₉₅(10⁴) = 196.6 (393 GeV) and
  s₉₅(10⁵) = 621.5 (243 GeV).

| case | w | script s₉₅ median → reach | my approximation |
|---|---|---|---|
| max rate, ×339 (B₅₀ 9,929) | 0 | 352 → 317 | 346 → 319 |
| | 0.03 | 641.1 → < 243 | 641 → < 243 |
| | 0.05 | 944 → < 243 | 949 → < 243 |
| | **0.17** | **2,697 → < 243** | 2,716 → < 243 |
| N_trig-weighted, ×339 (B₅₀ 6,825) | 0 | 292 → 342 | 284 → 345 |
| | 0.03 | 464.3 → **281** (84 %: 662.9 → < 243) | 461 → 282 |
| | 0.05 | 658 → < 243 | 659 → < 243 |
| | **0.17** | **1,822.5 → < 243** | 1,836 → < 243 |

The two agree to within 1–3 %. At w = 0.17, s₉₅ is 3–4.4 times the 243-GeV value (621.5), so "< 243 GeV" is not
marginal. The ×201 rows behave the same way (script: 2,725 / 1,838 at w = 0.17; 644 / 468 at w = 0.03).

**T2 numbers.** Taken from stdout [9b] and recomputed:
- (α1) without credit: B₅₀ 587 / 975.
- DIF: 385 / 647.
- B₅₀ with the conversions removed entirely: 401 / 663.
- Rejection needed to reach the (α1) conversion level: 9,527/183 = ×52.06 (98.08 %) and 9,527/308 = ×30.93 (96.77 %).
- (α1) with credit: B₅₀ 51 / 74. (α1′) with credit: 580 / 599.

The class limit is B₅₀ ≤ 300 (§11.7 rule 1, l.2726). Every T2 number in v6 matches.

---

## 2. T1: the expected outcome with the strategy's own normalisation width

| check | v6 text | evidence | status |
|---|---|---|---|
| Background ≈ 0.7–1.0×10⁴ | l.66, 103, 2771, 2918 | B₅₀ 6,825–7,087 (weighted rate) and 9,929–10,193 (max rate) | correct |
| Reach < 243 GeV at w = 0.17, at or near ≈ 180 GeV | l.68–69, 104–105, 993, 2773, 2788, 2919 | s₉₅ 1,823–2,725 ≫ 621.5; PLAN 0.2 row "below 200"; bounds "below about 180" | correct |
| Statistics-only 84 % edge ≈ 270–300 GeV | l.70, 105, 2774, 2919 | 270–297 | correct |
| Statistics-only median ≈ 315–340 GeV | l.71 | 314–342 | correct |
| Background known exactly ≈ 390–420 GeV | l.71, 105, 2774 | 392–419 | correct |
| "Already below 243 at 0.03" | l.69–70 and l.993–994 "its 84 % edge"; caption l.949 "(84 % edge)"; table cell l.966 "(already at 0.03)" | At w = 0.03 the weighted-rate median is 281/280 GeV and the 84 % edge is < 243. At the max rate both are < 243. The unqualified cell is in the max-rate row, where it is true. | correct, neither overstated nor understated |
| Counting width ≈ 0.02 | l.71 | 1/√(m+1), m = 9,527/2.3 ≈ 4,140 → 0.016; table σ_ln 0.02 | correct |
| Upside rows with w = 0.17 | l.79–81, caption l.949–950, Q2 l.2776 | (α1) edge 312–372 (statistics-only 421–455), median 369–429; m_H = 100: 454 vs 523 | correct |
| 710–790 GeV presented as an upside | l.76–78 "an upper edge that the strategy's own planning estimate does not expect"; Q2 l.2781 "an upper edge" | — | clear |
| ESTIMATE marking | §0 "Expected (ESTIMATE, v1 placeholder efficiencies…)" l.64; leading sentence l.102; Table 4.4c (caption and "reach, EST" column); scenario text l.989–990; Q2 stem l.2770 and §12.1 preamble l.2760 "Every reach number is EST"; §12.5 point 3 l.2918 | — | present everywhere |
| Q2 (b) honest | l.2787–2791 | — | yes: "expected below 243 GeV, at or near the existing bounds … In the expected case this paper reports no mass reach beyond the existing bounds; (c) is then the only route" |

**Leading sentence (l.102–107).** I read it as a referee would. It is an honest and physically correct statement of
the expectation:
- It gives the background with the source of its range.
- It states the width and where that width comes from (§4.7, generator difference 0.84 for Z(νν)+jet).
- It gives the reach that results.
- It labels the more favourable figures as statistics-only.
- It does not mention the upside, which is right for an expectation statement. The upside is placed in §0 "Expected"
  and in Q2, clearly marked.
- The width is called "≈ 0.17", and §0 l.68 adds "before K, luminosity and material". A width of 0.17 is therefore a
  lower value, not an inflation. A larger width would only lower the reach further.

**Physics of the claim.** In a simulation-only study, no control region constrains a generator normalisation. The
width therefore stays in the result, and AV §9 records this as settled. A referee might object that a real HL-LHC
analysis would take this background from a sideband. That objection does not change the conclusion: at w = 0.05 the
median and the 84 % edge are both below 243 GeV at both photon rates (table above). A transfer-factor width of a few
per cent therefore gives the same answer (C-2).

**T1: RESOLVED.**

---

## 3. T2: no (α) branch and no conversion veto alone avoids the day-15 pause

| location | text | numbers | status |
|---|---|---|---|
| §0 "The pause." l.90–95 | "The pause fires in the first upper branch too ((α1) without credit, B₅₀ 587–975, of which decays in flight 385–647), so neither a steeper conversion fall nor a conversion-removing conditional … avoids it on its own … only if the projected B₅₀ is at most 300, as in (α1) with fit-probability credit (51–74), (β) and the empty-ceiling case" | 587/975, 385/647, 51/74 | correct |
| Leading sentence l.107 | "removing the conversions alone would not avoid the pause" | — | correct |
| §4.4 "What is not known" l.1013–1014 | "removing the conversions alone does not bring B₅₀ below 300 (decays in flight 385–647 events)" | — | correct |
| Q2 stem l.2778–2781 | "This branch also pauses at day 15 (B₅₀ 587–975, of which decays in flight 385–647), so a conversion veto alone does not avoid the pause. Only branches with B₅₀ ≤ 300 do …" | — | correct |
| Q2 (c) l.2795–2797 | "It works if the projected B₅₀ is at most 300. That needs the conversions reduced by ×31–52 (96.8–98.1 %) **and** the decays in flight (385–647 events) reduced by a credit or a faster fall. The veto's rejection has not been measured." | ×30.9–52.1, 96.8–98.1 % | correct |

The ratio ×31–52 does not depend on the photon rate: the (α1′) and (α1) conversion terms both scale with
RATE["gamma"]. The success condition is therefore the same at both rates. The "and" in Q2 (c) is the physically
correct conjunction at v1's central sizes. The qualifier "at v1's central sizes" is the subject of C-1.

**T2: RESOLVED.**

---

## 4. Consistency of the expected-outcome statement across locations

I checked every location the fix report lists in its §3, and I grepped v6 for `270`, `315`, `390`, `10⁴`,
`existing bounds`, `avoid`, `expected branch`, `real background` and `statistics-only`.

| location | consistent? |
|---|---|
| §0 point 3 l.60–61 (rate clause; 6.4×10³; B₅₀ 6.8–7.1×10³) | yes |
| §0 "Expected" l.64–81 | yes |
| §0 "The pause." l.87–98 | yes |
| §0 leading sentence l.102–107 | yes |
| Table 4.4c caption l.946–950 and (α1′) row l.966 | yes |
| Scenario (α) l.979–994 | yes |
| §4.4 "What is not known" l.1009–1014 | yes |
| §4.4 B1 risks (3) l.1098 (no number) | yes |
| §4.11 point 3 l.1654–1657 (no number) | yes in substance; wording C-4 |
| §7 [L13] l.2282–2284 ("≈ 10⁴", a measured background) | yes |
| §11.7 rule 1 (decision rule) l.2726–2729 (no number) | yes |
| §12.1 Q2 stem, (a), (b), (c), rider | yes |
| §12.1 Q4 l.2825–2836 ("the pause is the expected branch"; 60 / 59 / 60 days) | yes |
| §12.5 point 3 (risk list) l.2916–2920 | yes |
| §13.4 l.2980 (old "≈ 270 GeV" headline) | a history row, correctly kept as history |

**No location contradicts the statement.** The same numbers and the same caveats (normalisation width, statistics-only
label, ESTIMATE on v1 placeholder efficiencies) appear everywhere a reach is quoted. The superseded phrases (`systematic
width of 0.2`, `270–390 GeV as above`, `20 % systematic width`, `0.04–0.06`) are gone from the text outside history.

---

## 5. Diff reading (v5 → v6, strategy)

I read all 30 hunks of `diff v5 v6` for their physics content. Each maps to T1–T3, an item of AV §6.3, the rider of
AV §7, or the general rules, as the fix report's §5 states.

| hunk | physics content | traceable to |
|---|---|---|
| 1–4, 28, 30 | headers, author lists, the §13.5 change table | general rule; Cr-C2 |
| 5 | 0.04–0.07 (printed μ 0.038 / 0.065) | T1-c (Cr-C4); correct |
| 6–10 | the T1/T2 text checked above | T1-a/b/c, T2-a |
| 11, 18–20, 26–27 | calendar 60 / 59.8 / 58.9 / 60.1 days. Out of my scope; the arithmetic +2.0 d matches the script [7] v6 line | T3 |
| 12–15 | Table 4.4c caption, the (α1′) row, the scenario text | T1-d/e; Ph-C4 wording |
| 16 | §4.4 "What is not known" | T2-b |
| 17 | [L13] re-worded: zero-count result → sample-size limited; v1-like behaviour → measured background | Ph-C5; physically correct (the earlier text called a 10⁴ counted term "sample-size limited", which was wrong) |
| 21 | §11.7 rule 1: the day-7/15 projection is conditional on C1 PASS for C′₀, with re-read or re-run (61 CPU-h) | H-C10; sound: a projection built on an unvalidated chain should not bind |
| 22–25 | Q2 stem, (b), (c), last sentence (790 → 814 GeV, matching stdout "R09-like with the pool at 1330 CPU-h … reach 814"), rider | T1-f/g, T2-c/d, H-C6, AV §7 |
| 29 | §12.5 point 3 | T1 (Cr-C1) |

**Nothing is untraceable, and no hunk changes the design or a number outside T1–T3 and the listed C items.** The only
departure from the literal order is hunk 18: the §11.2 MUST-only and full rows also receive 58.9 and 60.1. These are
AV §6.1 item 2's own values, so the change is traceable to T3. I also read the script's v6 hunk (l.786–876; §1). It
adds print lines only and changes no earlier value: the stdout diff shows one relabelled line and added lines only.

---

## 6. New findings

None is A or B. All of the following are C, offered for the Gate-A package.

**C-1. The T2 statements hold at v1's central DIF size. The strategy's own size uncertainty allows the opposite case.**
- The DIF numbers rest on 1 count (R07) and 2 counts (R06) in 500 events.
- Table 4.4c's own "(α1) no credit, size × e^(−1)" row gives B₅₀ **230** (×339) and 373 (×201). The first is below 300.
- With the conversions removed and DIF at ×e^(−1), B₅₀ ≈ 401 − 385 + 142 = **158** (×339) and ≈ 254 (×201). Both are
  below 300.
- §0 l.85 and the scenario text add that the v2 PV-placement change "may lower the DIF part".
- So "a conversion veto alone does not avoid the pause" and the "**and**" in Q2 (c) are true at the central size, not
  within the stated factor-e band.
- Suggested fix: add "at v1's central size (DIF rests on 1–2 counts; at ×e⁻¹ a veto alone would suffice)" where T2 is
  stated.
- This changes no default. Q2 (a) reads the measured counts at day 7 and day 15, and the rider's part (2) splits the
  ceiling counts by truth origin. It is a refinement, not an error: every number shown is correct.

**C-2. State the robustness of the T1 conclusion.**
- At w = 0.05, both the median and the 84 % edge are below 243 GeV at both photon rates (s₉₅ 658–948 > 621.5).
- One sentence in the Gate-A package would pre-empt the objection that the conclusion rests on the generator
  difference specifically, or that a sideband-based estimate would remove it. For example: "the conclusion holds for
  any normalisation width ≥ 0.05, including the transfer-factor width a sideband estimate would carry".

**C-3. Lower end of the photon-rate range.**
- The script enters the conversion term with the Z(νν) κ.
- v1's own Z(νν)+jet photon rate is 0.2306 (`cprime.gamma.rate.per_process.Znunu_j`), below the N_trig-weighted
  0.2552. If the conversions are Z(νν)-dominated, this gives ≈ 5.8×10³ conversions, ≈ 10 % below the quoted lower end.
- The conclusion does not change (< 243 GeV at any w ≥ 0.05). "≈ 0.7–1.0×10⁴" may stay, or become "≈ 0.6–1.0×10⁴".

**C-4. §4.11 point 3 (l.1654–1657, unchanged text).**
- "**The reading expected from Table 4.4c is 'target not met: sample-size limited'** while the ceilings count few
  events" uses "expected" for the branch that v6 itself calls not expected. The parenthesis that follows does qualify
  it.
- Suggested wording: "The reading expected if the day-15 pause does not fire is …".

**C-5. Which DIF figure to quote against the class limit.**
- The quantity compared with the class limit of 300 is B₅₀ with the conversions removed: 401–663 (floors + pile-up +
  DIF; stdout [9b] v6 (T2)). The text quotes the DIF term alone, 385–647.
- Both are above 300 and the conclusion is unchanged. Quoting 401–663 in Q2 (c) would be more precise.

---

## 7. Answer to the template question

Strip away the framing. Does the strategy state a correct expectation with honest uncertainties? **Yes.**
- On v1's counts, with v1's placeholder efficiencies, the default plan is expected to end at a measured
  hard-scatter-conversion background of ≈ 0.7–1.0×10⁴ events.
- With the strategy's own normalisation width, that background leaves no reach beyond the existing bounds.
- The statistics-only numbers are labelled as such.
- The day-15 pause is the expected branch, and the calendar includes it.
- The human is told, in Q2 (b), that the pre-authorised paper reports no reach beyond the existing bounds, and, in
  Q2 (c), what a redesign must achieve.

The open choices are posed with honest numbers. The remaining choice is the human's, at Gate A.

**Overall: approve for execution subject to Gate A.** There is no blocking item. C-1 and C-2 are worth one clause each
in the Gate-A package.
