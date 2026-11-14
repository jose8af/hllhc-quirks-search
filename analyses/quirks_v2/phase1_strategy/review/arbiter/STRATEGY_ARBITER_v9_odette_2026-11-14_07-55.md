# Arbiter verdict, review cycle 9: STRATEGY v9 (Mireille, 2026-11-14 06:55)

Arbiter: Odette, fresh session, 2026-11-14 07:55. Role file `agents/arbiter.md` followed in full.
Artifact: `outputs/STRATEGY_mireille_2026-11-14_06-55.md` ("v9"; "l." is a line of v9), `COMMITMENTS.md` ("COM"),
`src/strategy_budget.py` ("script"), `src/check_day15_text.py` ("checker"), `outputs/budget_stdout_v9.txt` ("stdout"),
`outputs/day15_text_check_v9.txt`, `outputs/FIX_REPORT_cycle8_mireille.md`.
Reviews: physics (Nadia), critical (Nikolai), constructive (Nora), all 2026-11-14 07:25.
Computation: einstein, `nice -n 19 python3 -I`, standard library, one process at a time; the script once (1 min 15 s,
36 MB), the checker twice (on v9 and on a scratch copy with my edit list), one 100,000-draw scratch sampler (seconds).
Scratch files are in `/var/tmp/jdochoa/arbiter_odette/` (outside the repo; `AGENT_RULES.md` forbids `/tmp`). No
sub-agent, no git.
Tags: VERIFIED = run or read in this session; ESTIMATE = a planning number of the strategy (v1 placeholder inputs).

**Verdict: ITERATE.** Category A: none. Category B: one (B-1, a stale count in the freeze table). W1 and its family
are closed. No number, criterion, budget figure, default answer or expected outcome is open. The fix is one word plus
thirteen wording edits and one rule sentence, all given below as exact text and already tested against the checker.

## 0. The open list (for the human; two minutes)

1. **B-1, blocking.** The table "What is frozen when" (§8, l.2336) says Gate A freezes "the answers to Q1–Q5 and the
   ten defaults". There are eleven. The eleventh, Df-11, is the reading of the day-15 rule that review cycle 8 pinned.
   `COMMITMENTS.md` and three other places in v9 say eleven, so the binding list is right and only this row is stale.
   Fix: "the eleven defaults (Df-1–Df-11, §12.1)".
2. **What the strategy should also tell you about Df-11** (Category C, applied in the same pass):
   - the alternative reading is *more lenient*, not stricter (limit at about 20 Z(νν) pilot counts instead of 12);
   - the pinned reading is itself a proxy that probably errs lenient: by v1's photon rates it under-reads the
     conversions of the other processes by about 8 % (at most ×1.6);
   - "≈ 12 pilot counts" holds at an R09 candidate; at an R08 candidate it is about 6–7.
3. **One sentence added to rule 1** (C, edit E6): the binding B₅₀ uses at least 10⁵ draws, and a reading within that
   precision of 300 pauses. You may drop it; it is then fixed in Phase 2 before the pilot is read.
4. Nothing else. 4,609 CPU-h, threshold 5,992, 60 days (57.8 without the pause), Q1–Q5 defaults, the expected outcome
   and the expected pause are unchanged since cycle 6.

---

## 1. W1 and the family: final status RESOLVED

My own confirmations (VERIFIED):

| check | result |
|---|---|
| script run, unchanged | exit 0, 1 min 15.4 s, 35,592 kB; 582 lines; sha256 `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d` = the cycle-8 verdict §3.2 hash; `cmp` with `budget_stdout_v9.txt`: identical |
| self-test | stdout l.391–398: eight PASS lines; l.399 "ALL PASS (8 of 8)" |
| checker file | sha256 `0808569b…9184a`, the value the critical reviewer found equal to the verdict's block |
| checker on v9 | "text check: ALL OK (45 of 45)", 0 MISMATCH; identical to `day15_text_check_v9.txt` |
| rule-1 clarification (T10) | present, l.2730–2738: "from the samples that exist at day 15 … Every SM hard-scatter process and the multijets … are read at the H per event of the Z(νν) pilot (2.3×10⁶ events; one count m_Z for all of them, their conversions included) … The reading is therefore a function of the pilot counts alone" |
| floor clause (T12) | present, l.2753: "These factors multiply a counted term, never its zero-count floor." |
| stdout v8 → v9 | two hunks, `354,376c354,370` and `396c390,399`, as ordered |
| strategy v8 → v9 | 33 hunks; my list equals the critical reviewer's attribution table |
| independent sampler (own code, seed 5, 100,000 draws, R09 term) | empty 76.5; m_Z = 11 / 12 / 13 → 281.9 / 300.3 / 318.4; m_D = 3 / 4 → 267.7 / 332.7. Agrees with the printed 76; 281 / 300 / 317; 266 / 331 within 1 % |

The three reviewers agree (case 1): rule 1 is single-valued, the two tables are on its basis (38 of 38 cells
recomputed by the physics reviewer with separate code), and the text agrees with the tables (45 of 45 by the checker;
0 of 34 and 0 of 33 disagreements in the two hand sweeps). I find nothing against this. **W1: closed.**

---

## 2. B-1: the stale "ten defaults" (l.2336)

**Fact (VERIFIED).** The row reads: "Gate A (this document + `COMMITMENTS.md`) | item criteria and tolerances of §4;
the verdict classes and what each earns; the zero-count convention; C1 subset and its tiers; the T2 list of 16
candidates and the figure of merit; systematic enumeration; the answers to Q1–Q5 and the ten defaults | 4-bot review,
user". Every statement of the count:

| place | text | status |
|---|---|---|
| v9 l.8 | "five questions Q1–Q5 and eleven defaults" | correct |
| v9 l.141 | "Eleven defaults are reported and can be overridden." | correct |
| v9 l.2949 | row Df-11 | present |
| **v9 l.2336** | **"the ten defaults"** | **stale** |
| COM l.233 (row GA) | "the eleven defaults (Df-1–Df-11)" | correct |
| COM l.36 | version-9 change row: eleven | correct |
| COM l.86, l.134 | "ten defaults (Df-9, Df-10 added)", "eight defaults" | history rows, correct as history |

The fix report says the count was updated in three places. Four needed it.

**Ruling: Category B. The reviewer's category stands.** Reasoning, on the §6.1 definitions:

1. *What the row governs.* It is the only place in the strategy that lists what Gate A freezes. It does not name
   §11.7. The reading of the day-15 rule enters that list only through "the answers to Q1–Q5" (Q2) and "the defaults"
   (Df-9, Df-11). The rule is applied at day 15, before the pre-registration freeze (days 17–19). Gate A is therefore
   the only freeze that binds the reading before the pilot is read.
2. *Is the ambiguity real?* Yes, in this row. "The ten defaults" names no identifiers. A reader maps it to
   Df-1–Df-10, because Df-11 is the newest row, is tagged "pinned in review cycle 8", and COM's own history row
   (l.86) says "ten defaults (Df-9, Df-10 added)". The natural resolution of the mismatch is thus the wrong one: that
   the pinned reading is reported but not frozen. That is the state rule 1 was in before cycle 8.
3. *What limits it.* COM l.233 is binding and unambiguous, and the row itself points to COM. No number, criterion or
   commitment can change through this slip. This is why the finding is B and not A.
4. *Why not C.* C is style and clarity. This is a factual error in a statement of commitment scope, on the one item
   this cycle exists to settle, and it is a regression of an addition (O6) that no arbiter had reviewed. The role file
   lets me lower a factually correct finding only on independent evidence that it is wrong. I have none: my evidence
   (point 3) was known to the reviewer and bounds the consequence without removing the misreading.

**Corrected text (E1).** "the answers to Q1–Q5 and the ten defaults" → "the answers to Q1–Q5 and the eleven defaults
(Df-1–Df-11, §12.1)".

---

## 3. Structured adjudication table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---|---|---|---|---|
| 1 | W1 resolved | Physics, Critical, Constructive | — | closed | Case 1; §1 |
| 2 | B-1: "ten defaults" in the freeze table | Critical | B | **B** | Case 3; §2. Fix E1 |
| 3 | Df-11 gives its alternative without its effect, and its consequence only by reference | Critical C-1; Constructive C-2 | C, C | C, apply | Case 1; §4.1. Fix E8 |
| 4 | The Z(νν) reading is a proxy that errs lenient; the text does not say so | Physics C-1; Constructive C-4 | C, C | C, apply | Case 1; §4.1. Fix E2, E7, E8 |
| 5 | "≈ 12 counts" holds at the R09 pile-up estimate; 6–7 at R08 | Physics C-2 | C | C, apply | Case 3; §4.1. Fix E3, E5, E7, E8 |
| 6 | §0 does not say the reading was pinned or point to Df-11 | Constructive C-1 | C | C, apply | E2 |
| 7 | Rule 1 fixes neither the draw precision nor the case within it | Physics C-3 | C | C, apply (rule sentence, flagged) | §4.2. Fix E6 |
| 8 | Self-test 7 at ±10 %; DIF rows 0.6–1.1 % low | Physics C-4 | C | C, deferred to Phase 2 | §4.3 |
| 9 | l.876–877 and the (α1) row are two unreconciled estimates | Critical C-2 | C | C, apply | E11 |
| 10 | l.2968 "day-15 class" for a result-basis floor | Critical C-3 | C | C, apply | E9 |
| 11 | l.118–119 cites no table | Critical C-4 | C | C, apply | E10 |
| 12 | "no other SM sample exists" (a Z(νν) development sample does) | Critical C-5 | C | C, apply | E4, E8 |
| 13 | COM row not marked (Df-11) | Critical C-6 | C | C, apply | E14 |
| 14 | Record items (42 against 41; 3,136 against 3,137 lines; a fix-report bullet) | Critical C-7 | C | record only | §4.3 |
| 15 | l.2976 names the wrong authors | Critical C-8 | C | C, apply | E13a |
| 16 | Rider: "expected to trigger" is exact only for (α1′) | Constructive C-3 | C | C, apply | E12 |
| 17 | §12.2 does not list Df-11 among the judgment calls that reach the user | Arbiter (case 5) | — | C, apply | E13b |

Dismissals: none. One deferral (item 8) and one record-only item (14), justified in §4.3.

---

## 4. The 16 C items

### 4.1 The items on how the pinned reading is shown to the human

**Question.** Would the human, reading §0 and §12.1 of v9 as they stand, be misled about what Df-11 approves?

**Answer: not misled, but not fully informed. Category C stands, and the sentences go into the strategy, not only
into the package.**

- *Nothing in v9 is false.* v9 never calls the reading conservative or strict (physics §1.3). The size of the
  under-reading is already in rule 1 in numbers (l.2747–2748: 5.9×10³ against 6.4–9.5×10³), and the (c) bar is quoted
  at the stricter rates 0.255 and 0.379.
- *No decision moves.* The expected reading is 100 to 1,000 times above 300 under every reading and every candidate.
  The limit in pilot counts matters only if the pilot is nearly empty, which the strategy does not expect.
- *R09 is the document's stated basis.* Table 4.4c is "Projection at an R09-like selection" (l.951), R08 is its
  comparison row (l.984), and the printed basis line and the caption both say "R09". With nearly empty counts the
  R09-like candidate has the better reach (790 against 496 GeV, stdout l.300–301), so it is the candidate at which
  the limit would be read. "≈ 12" is therefore correct on its stated basis.
- *Why the strategy must still say it.* The direction of the alternative is easy to get wrong. `LOG.md` 07:25 records
  that the orchestrator's own brief for O6 called the pool-floor reading the stricter one, and the fixer had to
  correct it. Df-11 is the only default row whose alternative has no stated effect. Both favourable choices in "≈ 12"
  (the R09 term; the Z(νν) photon rate) are in the artifact but not where the human decides. An override decision
  needs them there.

I do not raise these to B. Three reviewers rated them C, no stated number, criterion or default changes, and the
honest-framing test (is a limitation hidden?) is met by rule 1 and the captions. They are completeness of one
overridable default.

**Sources of the numbers in the new sentences.**

| number | source |
|---|---|
| 0.231 / 0.255 / 0.379 | printed: stdout l.366 (grid columns); v9 l.2869–2870 |
| 5.9×10³ against 6.4–9.5×10³ | already in v9 l.2747–2748 (5,918; 6,421; 9,527) |
| "≈ 8 % and at most ×1.6" | 6,421/5,918 = 1.085; 9,527/5,918 = 1.610 (VERIFIED, arithmetic on the three numbers above; physics §1.3) |
| 6.7; 88–148; 118 | printed: stdout l.355, l.280, l.301 |
| "≈ 6–7 Z(νν) or 1–2 decays-in-flight counts" at R08 | **not printed by the script.** Physics §1.4 (291 / 310 at m_Z = 6 / 7; 243 / 307 at m_D = 1 / 2). VERIFIED with my own sampler: 291.6 / 310.2 and 243.0 / 306.7; empty reading 181.0. The sentence says "not a script-printed number" and names its source |
| "about 1.66 times as many Z(νν) counts" | printed: basis line, stdout l.355 ("1.66 x Z(nunu)'s own 10.9"); 20/12 (cycle-8 verdict §1.2) |
| 37 % | 3,559/9,527 = 0.374 (cycle-8 verdict §1.2 point 2) |

No new script print line is needed, so the stdout and its sha256 stay as they are. The cycle-8 guard ("a new sentence
that restates a table number goes into `req`, or cites the table and states no number") is respected: the new
sentences cite the table for "≈ 12" and restate none of its cells. The one new quantity (R08) is not a table number
and is labelled as such. If Phase 2 wants it guarded, the line to add after the DIF row of block A is:

```python
print("  | R08 candidate (pile-up median %.0f, s_tot 0.43): m_Z = 6 / 7; m_D = 1 / 2 | " % pu8 + " / ".join(f"{pmf_pred(d15_gam(*a), ((pu8, 0.43, PU_CAP),), nd=D15_ND)[1][1]:.0f}" for a in ((6,), (7,), (0, 1), (0, 2))) + " | read against 300 |")
```

It is not ordered now, because it changes the stdout that 45 checks and every citation are tied to.

### 4.2 Physics C-3: the tie

Seed dependence is real: m_Z = 12 reads 299.6 (seed 7, 20,000 draws), 299.8 (seed 11) and 300.3 (my seed 5). The
script labels 297–303 "at the limit", and rule 1 does not say what follows there. Edit E6 closes the case on the side
that costs only a question. It adds a sentence to a binding rule, so it is not wording only. I order it in this pass
on the precedent of cycle 7 (verdict §5: a rule sentence that closes an undefined case, is conservative and touches
no criterion of the result), and because this pass is checked again. **It is the only edit that touches a
criterion.** If the human or the orchestrator prefers no rule edit, E6 is dropped and becomes a Phase-2 obligation:
the day-7 projection code fixes draws, seed and the tie rule before the pilot is classified.

### 4.3 Disposition of each item

**(i) Apply in this pass, 14 items:** Physics C-1, C-2, C-3; Critical C-1, C-2, C-3, C-4, C-5, C-6, C-8; Constructive
C-1, C-2, C-3, C-4. Plus my item 17. Exact text in §5. All are wording, labels or citations except E6 (§4.2).

**(ii) Gate-A package only, none beyond §7.**

**(iii) Deferred, 1 item: Physics C-4 → Phase 2.** Tightening self-test 7 to ±5 % and raising the draws of the DIF
rows change the stdout. Cost now: about 0.3 agent-hours plus a new stdout, new hash and new citations. It is safe to
leave: no classification is near its boundary (266 or 269 against 297; 331 or 333 against 303), every factor is
within 1.4 % of an independent recomputation (physics §2.3), and the binding day-15 number is computed by new Phase-2
code on real inputs, which E6 holds to 10⁵ draws. Commitment: the Phase-2 day-7 projection script carries the
self-test with the ±5 % bracket.

**Record only, 1 item: Critical C-7.** Not the artifact. For the record: the checker reports 41 mismatched checks on
v8 (the cycle-8 verdict's "42" counted the summary line); v9 has 3,137 lines (the fix report says 3,136); the fix
report's last bullet was overtaken by O6.

---

## 5. The fix list for v10 (exact text; nothing else is touched)

Each "old" string occurs exactly once in v9 (VERIFIED: applied by a program that asserts this). Applied to a scratch
copy of v9, E1–E13b give 13 `diff` hunks (`95c95 101c101 119c119 877c877 2336c2336 2736c2736 2756,2757c2756,2757
2819c2819 2892c2892 2949c2949 2968c2968 2976c2976 2979c2979`), no line added or removed, sha256
`0e509b4fdaba65a512f95e1aae9742b4f7b3901d436dbb247db603eb62326fd4` before bookkeeping, and **the checker reports ALL OK
(45 of 45) with the same statement counts as on v9** (VERIFIED). The script and the stdout are not touched.

**E1 (B-1). §8 freeze table, l.2336.**
Old: `the answers to Q1–Q5 and the ten defaults`
New: `the answers to Q1–Q5 and the eleven defaults (Df-1–Df-11, §12.1)`

**E2 (Constructive C-1, C-4; Physics C-1). §0 "The pause", l.95.**
Old: `only after the freeze and no pool floor. One Z(νν) pilot count`
New: `only after the freeze and no pool floor (this reading of the rule was pinned in review cycle 8 and is an overridable default, Df-11; for the processes without a sample it is a proxy that errs on the lenient side, Q2 caption). One Z(νν) pilot count`

**E3 (Physics C-2). §0 "The pause", l.101.**
Old: `between 3 and 4 decays-in-flight pilot counts (script [9b], v9 table). A conversion veto`
New: `between 3 and 4 decays-in-flight pilot counts (script [9b], v9 table; at the R09 pile-up estimate, and at fewer counts at an R08 candidate, Q2 caption). A conversion veto`

**E4 (Critical C-5). §11.7 rule 1, l.2736.**
Old: `since no other SM sample exists before the freeze. The reading is therefore`
New: `since no sample of another SM process exists before the freeze. The reading is therefore`

**E5 (Physics C-2). §11.7 rule 1, l.2756.**
Old: `or between 3 and 4 decays-in-flight pilot counts; the reading of each branch is the v9 table of script [9b])`
New: `or between 3 and 4 decays-in-flight pilot counts, both at the R09 pile-up estimate (at fewer counts at an R08 candidate, Q2 caption); the reading of each branch is the v9 table of script [9b])`

**E6 (Physics C-3; the rule sentence of §4.2). §11.7 rule 1, l.2757.**
Old: `are above their cap, the outcome class has changed: the study pauses and the user is asked. By v1's own conversion`
New: `are above their cap, the outcome class has changed: the study pauses and the user is asked. The binding B₅₀ is the median of at least 10⁵ draws (precise to about 0.3 %), and a reading within that precision of 300 counts as larger. By v1's own conversion`

**E7 (Physics C-1, C-2; Constructive C-4). §12.1 Q2, caption of the day-15 table, l.2819.**
Old: `the pile-up term is the R09 estimate (median 6.7 events; 88–148 at an R08 selection, Table 4.4c). The pilot is small`
New: `the pile-up term is the R09 estimate (median 6.7 events; 88–148 at an R08 selection, Table 4.4c), so the limits in pilot counts hold at an R09 candidate; at an R08 candidate the pile-up term alone takes 88–148 of the 300 events and the limits are about half as high (≈ 6–7 Z(νν) or 1–2 decays-in-flight counts at the R08 median of 118 events: physics review and arbiter verdict of cycle 9, not a script-printed number). Reading every other SM process and the multijets at the Z(νν) H per event is a proxy, not a measurement: by v1's photon rates (0.231 for Z(νν), 0.255 N_trig-weighted, 0.379 at most) the pilot's count under-reads their conversions (5.9×10³ events against 6.4–9.5×10³, that is by ≈ 8 % and at most ×1.6; §11.7 rule 1), and the other near-pass rates of busier processes (tt̄, W) are not measured, so the rule errs on the lenient side; the (c) bar below is quoted at 0.255 and 0.379 for this reason. The pilot is small`

**E8 (Critical C-1, C-5; Constructive C-2; Physics C-1, C-2). §12.1, row Df-11, l.2949.**

Old:

~~~~
since no other SM sample exists before the freeze; the (c) factors multiply a counted term, never its zero-count floor. Consequence: the day-15 threshold is crossed at the Z(νν) pilot count that the Z(νν)-count row of the v9 table of script [9b] (Q2) marks "at the limit". Needed because rule 1 as previously written did not say what those processes contribute, so the same pilot result could read as proceed or pause | another reading of the processes without a day-15 sample; alternative readings: see the cycle-8 arbiter verdict §1 (`review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`) |
~~~~

New:

~~~~
since no sample of another SM process exists before the freeze; the (c) factors multiply a counted term, never its zero-count floor. Consequence: the day-15 threshold is crossed at the Z(νν) pilot count that the Z(νν)-count row of the v9 table of script [9b] (Q2) marks "at the limit" (at the R09 pile-up estimate; at fewer counts at an R08 candidate). The reading is a proxy for the processes without a sample and errs on the lenient side: by v1's photon rates the Z(νν) count under-reads their conversions by ≈ 8 % (at most ×1.6; Q2 caption). Needed because rule 1 as previously written did not say what those processes contribute, so the same pilot result could read as proceed or pause | the other SM processes at the planned pool floors of Table 4.4a, with the Z(νν) count standing for Z(νν) alone. This is more lenient, not stricter: the limit is at about 1.66 times as many Z(νν) counts (the ratio in the basis line of the v9 table), the pilot then sees only the Z(νν) share of the conversions (37 %), and option (c) looks easier. No cost in CPU-h or days (cycle-8 arbiter verdict §1.2, `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`) |
~~~~

**E9 (Critical C-3). §12.1 annex, row "B4-e, size", l.2968.**
Old: `[E: 4×10⁵ × 1.14/100], by itself above the day-15 class |`
New: `[E: 4×10⁵ × 1.14/100], by itself above the class B₅₀ = 300 (a floor in the result; the day-15 rule reads the multijets through the Z(νν) pilot count) |`

**E10 (Critical C-4). §0 leading sentence, l.119.**
Old: `suffices without a reduction of the decays in flight.**`
New: `suffices without a reduction of the decays in flight.** (Basis of the last statement: Q2 (c) and the v9 grid of script [9b].)`

**E11 (Critical C-2). §4.4 point 5, l.877.**
Old: `if the conversions keep v1's fall) [E, script [9b]]). H at a T2 candidate`
New: `if the conversions keep v1's fall) [E, script [9b]]; for the pile-up-fall case the conversion counts alone give a different expected pilot count, the (α1) row of the v9 table of script [9b]: the two estimates are not reconciled, both EST). H at a T2 candidate`

**E12 (Constructive C-3). §12.1 Q2 rider, l.2892.**
Old: `(expected to trigger: the day-7 reading is expected at ≈ 3×10⁴–3×10⁵)`
New: `(expected to trigger in the expected branch (α1′): the day-7 reading is expected at ≈ 3×10⁴–3×10⁵; in the (α1) branch the lower edge of the reading is below this trigger, v9 table)`

**E13a (Critical C-8). §12.2, l.2976.** `experiment_log.md` has an entry for every version (VERIFIED: [Brigitte] to
[Mireille]).
Old: `(entries [Ingrid] and [Gunnar] for the last two versions, [Fiona], [Emeric], [Dmitri] and [Brigitte] for the earlier ones)`
New: `(one entry per version, under the name of its author)`

**E13b (arbiter, item 17). §12.2, l.2979.**
Old: `H on all own hits with S_CKF (Df-9); the Phase-3 slot table`
New: `H on all own hits with S_CKF (Df-9); the reading of §11.7 rule 1 pinned in review cycle 8 (Df-11); the Phase-3 slot table`

**E14 (Critical C-6). COM, row ST-1 (the row that cites rule 1).**
Old: `| ST-1 (Q4) | Stop rules of brief §7`
New: `| ST-1 (Q4, Df-11) | Stop rules of brief §7`

**Bookkeeping (the fixer writes these).**
- New file `outputs/STRATEGY_<name>_<stamp>.md`, version 10; v9 kept unchanged. Header l.1–7: version 10, fixer and
  time, "after the ninth arbiter verdict ITERATE (`review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`:
  finding B-1 and the C items it orders)", status "for verification and then the user's Gate A".
- New §13.9 "Changes since version 9" with this sentence verbatim: "The freeze table of §8 now counts eleven defaults.
  Df-11, §0 and the caption of the day-15 table state that the pinned reading is a proxy that errs lenient, that its
  alternative is more lenient still, and that the limit in pilot counts holds at an R09 candidate. Rule 1 states the
  precision of the binding median and that a reading within it pauses. No number of the script, default, CPU-h or
  calendar figure changed." One row for B-1 (E1) and one for the C items (E2–E14).
- Code reference: the checker's output file becomes `outputs/day15_text_check_v10.txt`. The stdout stays
  `budget_stdout_v9.txt`; the script is not run for a new output.
- COM: pointer to version 10, v9 added to the earlier versions, new section "Changes of rows in version 10" with the
  rows "GA | freeze table of STR §8 counts eleven defaults (B-1); no status changed" and "ST-1 (Q4, Df-11) | marked
  with the default it depends on; rule 1 states the precision of the binding median and that a reading within it
  pauses; no status changed".
- `outputs/FIX_REPORT_cycle9_<name>.md`: the hunk → item map, the checker's full output, the sha256 of the file after
  E1–E13b and before bookkeeping (expected value above).

If an "old" string is not found exactly once, the fixer stops and reports. It does not adapt the text.

---

## 6. Independent last-line checks

| check | evidence (VERIFIED) | result |
|---|---|---|
| nothing earlier reopened | The 33 hunks of v8 → v9 lie in §0 l.63–117, l.141, §4.4 l.797–1028, §11.7 rule 1, §12.1 Q2 and Df-11, §12.5 point 2, §13.8, the header and the code reference. No hunk touches a section behind the cycle-6 ledger (M1–M35, N1–N18, P1–P16, R1–R5) or the dispositions of cycles 7–8 other than this family | confirmed |
| four of the eight cycle-6 spot-checks re-read in v9 | stop conditions (§11.6, below); Q1 sealed tier (l.2794–2796); Q3 annex with routes 1–6 and the 4.6×10³ floor (l.2955–2969); reserve inside the figure (stdout l.123) | confirmed |
| budget | stdout l.123 and l.163: 4,609.4 CPU-h, threshold 1.3 × 4,609 = 5,992; l.205: 59.8 days with the pause, 57.8 without; l.206: rider 4,616.4 / 6,001.3 "if accepted at Gate A" | unchanged; rider optional |
| stop conditions | §11.6 (l.2679–2690) quotes `prompt.md` l.341–348 word for word; the 1.3× rule is tied to the approved figure | as in the brief |
| blinding invariant | l.26 "No v2 signal efficiency is computed or assumed anywhere in this document"; l.187; COM BL-1 and C1-d list the only exceptions (Q1; A, f₂₀₀, m_mig) | intact |
| nothing discarded has returned | no ρ = 3 (l.1197), no pile-up scan (l.1467), no Stage 3 at Λ ≥ 15 keV (l.1913), no cloud (l.2281), no Open Data (0 hits), endcap as an outlook only (COM S3 "dropped (user)") | confirmed |
| COM against v9 | pointer to v9; TG-1 row equal to the cycle-8 text; GA eleven; ST-1 4,609 / 5,992 / 60 days | consistent, except that v9 l.2336 disagrees with COM (B-1) |

**Regression triggers (§6.7).** A Phase-1 strategy has no validation test, systematic, fit, bin exclusion or
goodness-of-fit result, so none of the five triggers applies. For the record, the strategy expects the conversion
normalisation to carry more than 80 % of the uncertainty in the expected branch and investigates it (cycle-6 arbiter
item 16; package risk 3).

**Motivated reasoning.** The fixer's account is accurate except "three places" for the count (four). Two choices in
the human-facing limit are the favourable ones: the R09 pile-up term and the Z(νν) photon rate. Both were in the
artifact but away from §0 and Df-11. E2, E3, E7 and E8 put them where the human decides. Nothing is "addressed later"
that could change the result.

**Reviewer pressure.** No finding was disputed. I lower no category. The physics reviewer's statement that the count
of defaults "is presented correctly" (her §1.5) is overruled by the artifact at l.2336 (case 4).

**Competing group.** A reader would ask why one Z(νν) count speaks for tt̄ and W. The answer is now in the caption
with its direction and size, and the staged 4a samples replace the proxy after the freeze.

---

## 7. The Gate-A package (constructive review, part 3): corrections

I checked the package against v9 and the stdout. Every number has its source, and I found no wrong number (spot
checks: stdout l.308–310, 327, 330, 355–370, 373, 375, 379–380; v9 l.2522–2538, l.2569). The corrections follow from
my rulings. With them the block from "# GATE A" to the end of "## 9. Files" has **1,496 words** by `wc -w` (VERIFIED;
1,499 before). The corrected text is in `/var/tmp/jdochoa/arbiter_odette/GATE_A_package_corrected.md`.

Corrections:
1. **Sources:** "Sources: STRATEGY v10 (STR), `budget_stdout_v9.txt` (stdout). **All reach and background numbers:
   ESTIMATE on v1 placeholder efficiencies**."
2. **§2 Review:** "- Review: cycles 1–9, Category A 11→4→1→0→0→0→0→0→0, Category B 24→14→15→5→3→1→4→1→1 (cycle 9: a
   stale count, fixed in v10). Cycles 4–8 turned on the day-15 reading; cycle 8 found rule 1 ambiguous and pinned it
   (Df-11: limit ≈ 12 Z(νν) pilot counts, not ≈ 20)."
3. **§3 Q2 stem:** "Every SM process is read through the one Z(νν) pilot count, a proxy, since no sample of another SM
   process exists at day 15 (stdout l.354–364)."
4. **§3 rider:** "(b)/(c) asked at day 7 if B₅₀ ≥ 3,000 (expected in the expected branch)".
5. **§4 heading:** "## 4. Eleven defaults (overridable; STR §12.1)".
6. **§4 Df-11 row:** "| **Df-11, NEW (pinned in cycle 8)** | rule 1 reads only day-15 samples: every SM process via
   the Z(νν) pilot count (a proxy, probably lenient: by v1's photon rates their conversions are under-read by ≈ 8 %,
   at most ×1.6), no pool floor; (c) factors never multiply a floor; ties pause → limit ≈ 12 counts (R09 candidate;
   ≈ 6–7 at R08) | alternative | SM at pool floors: limit ≈ 20, more lenient, blind to most conversions, (c) looks
   easier |". If E6 is dropped, delete "ties pause".
7. **§7 risk 2:** "Pilot statistics: an empty pilot reads B₅₀ 76 of 300; each decays-in-flight pilot count adds 65
   events, and four pause the study (two at R08)."
8. **§9 Files:** "STR v10 (§0, §12.1); `budget_stdout_v9.txt`; `COMMITMENTS.md`;
   `phase1_strategy/outputs/feasibility/`; `phase1_strategy/review/arbiter/`; `LOG.md`; `DEVIATIONS.md`."

Cuts that pay for the additions:
- Sources: "(best Λ per mass)" (it stays in STR §0).
- §1 Upside: ", at the limit at ≈ 12 counts" (now in §2, §3 and Df-11).
- §2: "Geant4 11.4.3 installs in ≈ 3 min. Runner tests pass." replaces "installs node-locally in ≈ 3 min. Runner:
  kill/resume, memory, I/O pass."
- §2 Incidents: "- Incidents (`LOG.md` 14:06, 15:12): stale file handle after a cajuela directory rename; einstein out
  of memory. Since: the rules of `AGENT_RULES.md`."
- §5: "(measured in week 1)".
- §8: "; plus the thickness law".

If the package goes to the human before v10 exists, it cites "STRATEGY v9 with the open list of the cycle-9 arbiter"
and the review line reads "(cycle 9: a stale count, to be fixed in v10)".

---

## 8. Iteration history and audit paragraph

| cycle | version | merged A | merged B | verdict |
|---|---|---|---|---|
| 1 | v1 (Brigitte) | 11 | 24 | ITERATE |
| 2 | v2 (Dmitri) | 4 | 14 | ITERATE |
| 3 | v3 (Emeric) | 1 | 15 | ITERATE |
| 4 | v4 (Fiona) | 0 | 5 | ITERATE |
| 5 | v5 (Gunnar) | 0 | 3 | ITERATE |
| 6 | v6 (Ingrid) | 0 | 1 (U1) | ITERATE |
| 7 | v7 (Jules) | 0 | 4 (one family, V1) | ITERATE |
| 8 | v8 (Leopold) | 0 | 1 (W1) | ITERATE |
| 9 | v9 (Mireille) | 0 | 1 (B-1) | ITERATE |

A: 11 → 4 → 1 → 0 → 0 → 0 → 0 → 0 → 0. B: 24 → 14 → 15 → 5 → 3 → 1 → 4 → 1 → 1.

**What nine cycles changed.** Cycles 1–3 rebuilt the method: a zero-count convention with a coverage test, closure on
rungs and samples disjoint from the derivation, a no-credit ceiling H for every factor that cannot be tested, an
extrapolation width that is always added, a sealed tier for the C1 signal counts, and the complete list of processes
with their pool shares. Cycles 4–5 made the summary honest: by v1's own conversion counts the expected background is
≈ 0.7–1.0×10⁴ events, the reach is below 243 GeV at the strategy's own normalisation width, and the day-15 rule is
expected to pause the study; the budget was fixed at 4,609 CPU-h with the reserve inside it. Cycles 6–8 changed no
design choice. They corrected how the day-15 decision is described to the human: on which hits it reads, which
branches pass, and what a conversion veto would have to achieve. **The root cause of cycles 4–8** was found in cycle
8: rule 1 did not say what an SM process without a day-15 sample contributes, so the same pilot counts could read as
proceed or pause, and each fix described one reading while the code or a neighbouring sentence used another. Cycle 8
pinned the reading, recomputed the tables on it, and added a self-test and a text checker. Cycle 9 confirms that this
holds. What it found is not a member of that family: an addition ordered outside the verdict (Df-11) was not carried
into the one table that says what Gate A freezes.

I do not pass because this is the ninth cycle, and I do not iterate on taste. The one blocking item is a factual
error in a statement of what is frozen, on the item this cycle settles.

---

## 9. Form of the check on v10, and what is open

A fresh fixer applies §5 and nothing else. The check is mechanical and narrow:

| step | verifies |
|---|---|
| critical reviewer (fresh) | `diff` v9 → v10: the 13 hunks of §5 plus bookkeeping, 0 unattributed; the sha256 of §5 before bookkeeping; the checker ALL OK (45 of 45) on v10 against `budget_stdout_v9.txt`; the script and the stdout untouched (same sha256); COM: pointer, two rows, E14; every statement of the number of defaults in v10 and COM says eleven |
| arbiter | PASS if the reviewer confirms; no new adjudication is expected |

Admissible new findings: a regression of this fix, or a factual error in a number shown to the user. Settled and not
to be reopened: the pinned definition of rule 1; the two tables; the defaults Q1–Q5 and Df-1–Df-11.

This would be cycle 10, the hard cap. The orchestrator has said that an ITERATE here goes to the user with this
verdict. That is consistent with the methodology: the user can order the check above, or decide otherwise at Gate A.
I see no ground for ESCALATE: nothing needs the user beyond the Gate-A questions.

**Open outside §5: nothing.**

---

## 10. Verdict

**ITERATE.**
- **Category A:** none.
- **Category B:** B-1 (l.2336, "ten defaults"). Fix E1.
- **In the same pass:** the 14 C items and my item 17, edits E2–E14. E6 is the only one that adds to a criterion and
  may be dropped by the human (it then moves to Phase 2).
- **Deferred:** Physics C-4 to Phase 2. **Record only:** Critical C-7.
- **Gate-A package:** the constructive reviewer's part 3 with the corrections of §7 (1,496 words).
- **After the check of §9,** the artifact of record for Gate A is STRATEGY v10 with `COMMITMENTS.md`,
  `budget_stdout_v9.txt` and `src/check_day15_text.py`.
