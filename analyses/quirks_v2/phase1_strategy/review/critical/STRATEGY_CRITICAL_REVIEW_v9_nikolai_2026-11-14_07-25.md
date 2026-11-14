# Critical review, cycle 9: STRATEGY v9 (Mireille, 2026-11-14 06:55)

Reviewer: Nikolai, fresh session, 2026-11-14 07:25. Role file `agents/critical_reviewer.md` followed (adversarial stance,
evidence for every "verified"). Scope as ordered by the cycle-8 verdict §9: the mechanical verification plus my own sweep.
I did not re-review the design.
Files: v9 = `outputs/STRATEGY_mireille_2026-11-14_06-55.md`; v8 = `outputs/STRATEGY_leopold_2026-11-14_05-00.md`;
verdict = `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`; COM = `COMMITMENTS.md`; script =
`src/strategy_budget.py`; checker = `src/check_day15_text.py`. "l." is a line of v9 unless stated otherwise.
Computation: einstein, `nice -n 19 python3 -I`, standard library, one run at a time. Scratch files are in the session
scratchpad, outside the repo. Read-only git only. No sub-agent. All tags VERIFIED unless stated otherwise.

**Result: Category A 0, Category B 1, Category C 8.** The code, the output, the tables and T1–T18 match the verdict
exactly. The one B item is a count of defaults that O6 missed (l.2336, "the ten defaults").

---

## 1. Code against the verdict

**Text checker.** I extracted the three `~~~~python` blocks of the verdict (verdict l.224–339 block A, l.348–414 block B,
l.479–627 the checker) with a program. `diff` of the checker block against `src/check_day15_text.py`: empty. Both have
sha256 `0808569b…9184a`. **Byte-identical.**

**Budget script.** `git diff HEAD~1 -- …/strategy_budget.py` has three hunks: `@@ -1,7 +1,7 @@` (docstring),
`@@ -850,59 +850,121 @@` (block A) and `@@ -961,7 +1023,73 @@` (label (b) and block B), with 177 insertions and 49
deletions (1,428 → 1,556 lines). I rebuilt the expected file with a program. It started from
`git show HEAD~1:…/strategy_budget.py`, asserted the anchors (v8 l.853 starts `# v8 (V1, verdict cycle 7`, v8 l.905
starts `print("  |   (alpha1) conversion levels`, the old (b) string occurs once in v8 l.964 and v8 l.965 is blank),
replaced l.853–905 with block A, applied (b), put block B after l.964 and made the two docstring replacements of C-5.
`diff` of that file against the committed script: **empty**. So the script contains the three ordered changes and the
C-5 docstring, and nothing else.

**What the checker ties to printed values.** It has 45 checks:

| part | n | tied to the printed table? | hard-coded parts |
|---|---|---|---|
| self-test line | 1 | yes (the stdout line itself) | — |
| (A) fences | 1 | yes: the quoted lines must equal stdout lines i0…i1, in order | the line-prefix filter (`  v`, `  |`, `  basis`, `  (the v6`) |
| (B) required | 16 | yes: every fragment is formatted from the parsed `T` values (`sci()` for powers of ten; grid cells with their percentages) | the expected occurrence count `n`, and the wording around each number. The e⁻¹ sentence has a structural guard and fails if the row changes pattern |
| (C) scanners | 6 | yes: each hit must be a member of a set built from `T` | the regexes, and which section the B₅₀-range scan covers |
| (D) stale | 21 | no, by nature: they are fixed strings of v6–v8 | all of them. A stale list cannot go stale in the harmful direction. Three of them ("read as rule 1 reads them", "would suffice", "×31") have no hit in v8 either: they guard against v6/v7 |

None of the checks compares the strategy with a hard-coded number that could go stale. What the checker **cannot see**:
1. Qualitative claims with no number in them: "the pause is the expected branch", "(β) is read as (γ)", "nearly zero",
   "no conversion rejection suffices", "proceed/pause".
2. Numbers of the family written in any form other than the six scanned ones: "18 events" and "65" per pilot count,
   "×5–50", "21 events", "5.9×10³", "four decays-in-flight counts", "≈ 3×10² in the pilot", expected pilot counts
   ("m_Z 31–53", "2–190").
3. Mismatches of position. (C) tests membership, not location. "[×44]" in place of "[×30]", or "3 Z(νν) pilot counts", would
   pass, because 44 is in `gridset` and 3 is in `okc`. (B) counts a fragment anywhere in the live text, not at the
   location its label names.
4. B₅₀ ranges outside "The pause" and Q2.
5. §13, all code fences other than the two quoted tables, COM, the Gate-A package, STATUS and LOG.
6. Table 4.4c and every stdout line outside l.354–370 (by design).

Item 2 is covered by my own sweep (§6). It found no disagreement in a number.

## 2. Run

`/usr/bin/time -v nice -n 19 python3 -I src/strategy_budget.py > <scratch>/stdout_run.txt` took 1:17.15 wall with a
maximum RSS of 35,660 kB and exit status 0.
- sha256 `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d` = the verdict §3.2 hash = `budget_stdout_v9.txt`.
  The file has 582 lines.
- Self-test: stdout l.391–398 contain 8 PASS lines, and l.399 is `v9 self-test: ALL PASS (8 of 8)`. The bracketed values
  equal verdict §3.2 (for example `[empty: 76.4; m_Z = 12: 299.6; m_D = 4: 331.0]`, `[24 of 24]`).
- `diff budget_stdout_v8.txt` against it gives exactly two hunk headers, **`354,376c354,370`** and **`396c390,399`**.
  `cmp` of v8 l.1–353, 377–395, 397–579 against new l.1–353, 371–389, 400–582 shows them identical. So only the two table
  blocks, the label line (b) (l.390) and the nine self-test lines (l.391–399) differ.
- The figures are unchanged:
  - l.123 and l.163: approved 4,609 CPU-h, threshold 1.3 × 4,609 = 5,992;
  - l.205: 59.8 days with the pause (60 rounded), 57.8 days without;
  - l.206: rider 4,616.4 / 6,001.3 ("if accepted at Gate A", an option only).

**Checker on v9:** `text check: ALL OK (45 of 45)`. `diff` against `outputs/day15_text_check_v9.txt` is empty.
**Checker on v8 (control), against stdout v9:** `text check: MISMATCH (4 of 45)`, which means **41 mismatched checks**.
The four checks that pass are the self-test line (it reads stdout) and the three v6/v7 stale guards. The verdict says "42
mismatches". The difference is the summary line, which itself contains "MISMATCH" (`grep -c MISMATCH` = 42). Record only
(C-7). The control does discriminate: every (A), (B) and (C) check fails on v8, and so do 18 of the 21 (D) checks.

## 3. Text against the verdict

**T1–T18 and the §1.4 clarification.** I applied the 18 replacements of verdict §5 to v8 with a program. For T1–T13,
T15, T17 and T18, each "Old" block occurs exactly once, asserted. T14 is the span from "The day-7 and" to the closing
fence of the verbatim block (34 lines, as the verdict states). T16 is the span from "At v1's central decays-in-flight size
(385–647 events," to "acts on both." (28 lines, as stated). I then took `diff` of that result against v9. The **only
residual hunks** are 1c1, 3,5c3,5, 7,8c7,8, 141c141, 2948a2949, 3115a3117,3128, 3120c3133 and 3121a3135,3136: header,
O6, §13.8 and the code reference (§5 below). So every T item is applied verbatim at its location, with no deviation.
- The rule-1 clarification (T10, the sentence ordered in §1.4) is at l.2730–2738 of §11.7 rule 1, verbatim.
- The floor clause (T12), "These factors multiply a counted term, never its zero-count floor.", is at l.2753.

**Tables.**
- `diff` of v9 l.2822–2832 against stdout l.354–364: empty (11 lines).
- `diff` of v9 l.2875–2880, with the `> ` prefix removed, against stdout l.365–370: empty (6 lines).
- Captions (T14 l.2819, T16 l.2864–2872) are verbatim per the residual diff. Their line citations (l.354–364, l.365–370)
  are correct.

**C items of §6.4.**
- "Applied now":
  - Physics C-1 / critical C-6: l.2860–2862 and the last grid line, l.2880.
  - Physics C-2: block A, `math.ceil` and the integer search.
  - Physics C-3: l.2819 "R09 estimate (median 6.7 events; 88–148 at an R08 selection".
  - Physics C-4: "65" at l.95–96 and l.2737, and the DIF row.
  - Critical C-5: script docstring, verified by the rebuild.
  - Critical C-7: T18, l.3004.
  - Constructive C-2: l.2808 "a digest of the printed lines below".
- The verdict lists no package-only or deferred items. None of the Gate-A corrections of §7 appears in v9: the residual
  diff contains none.

## 4. Addition O6 (Df-11)

**Content (l.2949).**
- The reading clause matches T10 and T12 in substance and largely in wording: samples that exist at day 15;
  H = Gamma(m + 1)/M; floor = m = 0 on that sample, not the Table 4.4a floor; every SM process and the multijets through
  the Z(νν) pilot count; factors multiply a counted term, never its floor.
- It adds the clause "every term is read from the samples that exist at day 15", which T10's "from the samples that exist
  at day 15" implies.
- The consequence cites the Z(νν)-count row "at the limit" and restates no number.
- No checked statement is added: ALL OK unchanged.
- Consistent.

**Counts.** I grepped v9 and COM for "ten", "eleven", "Df-10", "Df-11", "Df-1–", "defaults" and the number words:
- v9 l.8 "eleven defaults" ✓.
- v9 l.141 "Eleven defaults" ✓.
- COM l.233 "eleven defaults (Df-1–Df-11)" ✓.
- COM l.36: new GA history row ✓.
- COM l.86 "ten defaults (Df-9, Df-10 added)" and COM l.134 "eight defaults": history rows of v5/v3, correct as history.
- **v9 l.2336, the Gate-A row of the freeze table (§10): "the answers to Q1–Q5 and the ten defaults". Now inconsistent.**
  This is B-1.
- No other top-level `.md` of QV2 states the count (grep).

The rest of the Gate-A section (§12.1–12.3) does not depend on the count. §12.2 (l.2976–2980) does not list Df-11. It does
not need to, since it lists judgment calls of the versions named there. It is stale for another reason (C-8).

## 5. Diff check (complete)

`diff v8 v9` has **33 hunks**, as the fixer reports:

| v8→v9 hunk | attribution |
|---|---|
| 1c1, 3,5c3,5, 7,8c7,8 (l.7) | bookkeeping: header (version, fixer, verdict pointer, status "cycle 9") |
| 7,8c7,8 (l.8), 139c141 | O6: ten → eleven |
| 63c63 | T1 |
| 79c79 | T2 |
| 91,99c91,101 | T3 |
| 115c117 | T4 |
| 795c797 | T5 |
| 876c878 | T6 |
| 961c963 | T7 |
| 1010c1012 | T8 |
| 1025,1026c1027,1028 | T9 |
| 2728,2730c2730,2738 | T10 (clarification, §1.4) |
| 2738,2739c2746,2748 | T11 |
| 2744c2753 | T12 (floor clause, §1.4) |
| 2746,2747c2755,2756 | T13 |
| 2797,2799c2806,2808; 2801c2810; 2803,2808c2812,2817; 2810c2819; 2813,2828c2822,2832 | T14 (one span; includes the table insertion) |
| 2835c2839 | T15 |
| 2851,2856c2855,2862; 2858,2863c2864,2872; 2866,2872c2875,2880; 2877c2885 | T16 (one span; includes the grid insertion and C items physics C-1 / critical C-6) |
| 2884c2892 | T17 |
| 2940a2949 | O6: Df-11 |
| 2995c3004 | T18 (critical C-7) |
| 3107a3117,3128 | bookkeeping: §13.8. It contains the verdict's sentence verbatim (exact-string count 1), the W1 row, the O6 row and the C row |
| 3112c3133 | bookkeeping: code reference runtime (1 min 15 s, 36 MB; my run: 1:17, 35.7 MB) |
| 3113a3135,3136 | bookkeeping: the `check_day15_text.py` line |

**Unattributed hunks: 0.** This is proven mechanically: after T1–T18 are applied, only the bookkeeping and O6 hunks remain.

**COM** (`git diff HEAD~1`) has three hunks:
- pointer to v9 and v8 added to the list of earlier versions (bookkeeping);
- the new section "Changes of rows in version 9", whose TG-1 row equals the verdict's text word for word, plus the GA row
  (O6);
- the GA row l.233 changed from ten to eleven (O6).

Nothing else changed in COM. A grep of COM for the family's stale values ("≈ 20", "×34", "5×10⁴", "401", "51–74") finds
them only in history rows that state no number.

## 6. Own sweep beyond the checker

**Method.** I grepped the live text (outside §13 l.3024–3129 and the code fences) for the 26 terms given. 426 lines
matched. I restricted these to the lines that make a claim about the day-15 or day-7 reading, the pause, the pilot counts
or the (c) test, which left 178 lines, and read every one of them. I also read the (α1, S_CKF, fit-probability and "after
CKF" lines outside that set: they are Table 4.4c / result-basis statements with their own labels, outside this family.

**Result: 33 statements of the family that no checker pattern covers.** All 33 agree with the table on the number. One
disagrees with a table cell in what it implies (U12, from a different estimator), and two lack the right basis label
(U10, U30).

| # | l. | quoted phrase | must agree with | agree | basis label |
|---|---|---|---|---|---|
| U1 | 62 | "the day-15 rule reads this branch on all own hits, (α1) row of the v9 table" | (α1) row | yes | yes |
| U2 | 74 | "The day-15 rule is expected to pause the study before production" | (α1′) row "above" | yes | yes (§11.7, Q2) |
| U3 | 79 | "the day-15 rule reads it as (γ), through the Z(νν) pilot count" | (γ)/(β) row = Z(νν)-count row | yes | yes |
| U4 | 89–91 | "pauses … if the projected B₅₀ exceeds 300 events or both pile-up estimators miss their cap; … preliminarily at day 7" | header line "pauses if B50 > 300" | yes | yes |
| U5 | 95–96 | "One Z(νν) pilot count is 18 events and one decays-in-flight pilot count is 65" | basis line 18.1, 65.1 | yes | yes (l.101) |
| U6 | 96–97 | "×5–50 above their after-CKF sizes (ε_pair assumed 0.8–0.98" | own-hit rows at 0.8 / 0.98; self-test 6 | yes | yes |
| U7 | 98–99 | "the pause is the expected branch" | (α1′) "above" | yes | yes |
| U8 | 99 | "below 300 only if the pilot's counts are nearly zero" | m_Z ≤ 11, m_D ≤ 3 below | yes | yes |
| U9 | 101–102 | "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" | (c) rows | yes | yes |
| U10 | 118–119 | "at v1's central decays-in-flight size (1–2 counts) no conversion rejection suffices without a reduction of the decays in flight" | f_D = 1 row "none suffices" | yes | **no** (no table cited in that sentence; C-4) |
| U11 | 797 | "m_H ≈ 1.6×10³ … (≈ 3×10² in the pilot) (after CKF; ×1/(1 − ε_pair) on all own hits)" | stdout l.390 "326 in the pilot"; (α1′) m_Z 1632 = 326/0.2 | yes | yes |
| U12 | 876–877 | "the pilot expects few counts (Z(νν): 0.4–3.7 at R08 with CKF, 2–190 under option (a) of Df-9 (pile-up fall" | (α1) row "expected pilot counts at 0.8: m_Z 31-53" (×10 at 0.98) | **no**, a different estimator: 2–190 = pool m_H 10–890 × 2.3/11 from the attributed hard-scatter rate (l.791–794); 31–53 is from the conversion counts with a pile-up fall. "Few counts" for the pile-up-fall branch is 31–53 (above the limit) by the table and 2–19 (below) by l.877 at ε_pair = 0.8. No decision changes. C-2 | yes ([E, script [9b]]) |
| U13 | 878 | "a bound of 12 events for Z(νν) itself and of 21 events for all SM" | 1.14 × 10.90 = 12.4; 1.14 × 18.13 = 20.7 | yes | yes |
| U14 | 963 | "computed on the pilot's exposures, not on these pool floors" | basis line "no pool floor enters" | yes | yes |
| U15 | 1011–1012 | "(β) … at day 15 … the rule reads every SM process through the Z(νν) pilot count" | (γ)/(β) row | yes | yes |
| U16 | 2731–2737 | T10: "one Z(νν) pilot count is 18 events, one decays-in-flight pilot count 65" | basis line | yes | yes |
| U17 | 2745 | "N_t·H on all own hits, with no S_CKF and no conditional credit" | header line | yes | yes |
| U18 | 2747–2748 | "5.9×10³ events after CKF by v1's Z(νν) photon rate against the 6.4–9.5×10³ of Table 4.4c" | D15_G third rate: 3,559 × 1.663 = 5,918 (verdict §1.3) | yes | yes |
| U19 | 2752–2753 | "at most ×n/1.14. These factors multiply a counted term, never its zero-count floor" | grid caption "zero-count floors kept" | yes | yes |
| U20 | 2757–2758 | "By v1's own conversion counts (scenario (α1′) …) this is the expected branch" | (α1′) above | yes | yes |
| U21 | 2805 | "day-15 rule (preliminary at day 7) is expected to pause the study before production" | (α1′) | yes | yes |
| U22 | 2807 | "×5–50 above the after-CKF sizes" | own-hit rows | yes | yes |
| U23 | 2819 | "median 6.7 events"; "four decays-in-flight counts alone pause the study" | basis 6.7; m_D = 4: 331 above | yes | yes |
| U24 | 2837 | "This branch also pauses (table)" | (α1) above | yes | yes |
| U25 | 2839 | "Their day-15 readings are the Z(νν)-count and zero-count rows" | rows 2 and 1 | yes | yes |
| U26 | 2853–2854 | "It works if the projected B₅₀ is at most 300, with the redesigned conditional and S_CKF estimated on development samples" | (c) rows | yes | yes |
| U27 | 2860 | "These factors assume S_CKF estimated for both terms" | grid caption "(S_CKF estimated)" | yes | yes |
| U28 | 2861–2862 | "no conversion rejection suffices from a quarter of v1's decays-in-flight size on" | last grid line "f_D >= 1/4: none suffices" | yes | yes |
| U29 | 2869–2872 | rates 0.379 / 0.255 / 0.231, "precise to about 3 %" | grid header | yes | yes |
| U30 | 2968 | "floor … 4.6×10³ events … by itself above the day-15 class" | not a day-15 term: at day 15 the multijets are read through the Z(νν) count (Df-11) | yes (4.6×10³ > 300) | **no**: a result-basis floor labelled "day-15 class". T5 and T9 renamed the same expression elsewhere; this sibling was missed (C-3) |
| U31 | 2892 | "at least 3,000 events (10× the class)" | threshold 300 | yes | yes |
| U32 | 2949 | Df-11 "at the Z(νν) pilot count that the Z(νν)-count row … marks 'at the limit'" | m_Z = 12 at the limit | yes | yes |
| U33 | 3011 | "The day-15 rule pauses the study (Q2)" (inside outcome 3, the expected branch) | (α1′) | yes | yes |

**Superseded values as current: none.**
- (γ) row 104/180/255/294/331/448: 294 and 448 have no hit. 104, 180 and 255 have hits only in unrelated contexts (0.10418,
  180 GeV bounds, 20–180 m_H, rate 0.255). 331 has hits only at m_D = 4 and in Table 4.4c l.981.
- "≈ 60 counts", "×34", "×69–235", "×52–81", "20 pilot counts", "4574", "5946" and "57.6": no hits.
- "4,574; 5,946": l.2552, the version-4 history sentence "Version 4 had …", correct as history.
- 710/790 GeV: l.79, l.969 and l.2839 give them as the upper edge ("ceilings empty"), not as the expectation. l.2889 is a
  median 790 → 814 for empty ceilings.
- 470–500: l.75 and l.2837 give them as the (α1) upper-branch median, not as the expectation.

---

## 7. Findings

### Category A
None.

### Category B

**B-1. The freeze table still says "ten defaults" (l.2336).** In the §10 freeze table, the row "Gate A (this document +
`COMMITMENTS.md`)" reads "the answers to Q1–Q5 and the ten defaults". With O6 there are eleven (l.8, l.141, l.2949; COM
l.233). Read as written, the row lets a reader conclude that Df-11, the pinned reading of the day-15 rule, is not among
the items frozen at Gate A. That is exactly the point this cycle settles. It is a regression of O6: the fix report claims
three places, and four needed changing. Fix: "ten defaults" → "eleven defaults" at l.2336. This is one word; the checker
is unaffected (no checked statement).

### Category C
- **C-1 (Df-11, alternative column).** Every other Df row states what the alternative costs. Df-11 says only "another
  reading … see the cycle-8 arbiter verdict §1". The human who considers an override should be told the direction. The
  verdict's §1.2 shows the readings without a day-15 sample (pool floors, or Z(νν)-only exposure) are the lenient ones:
  they move the limit to more pilot counts and make option (c) look easier. Suggested text, with no new number: "a reading
  that uses pool floors or only Z(νν)'s own exposure is more lenient: the limit falls at more pilot counts and option (c)
  looks easier (cycle-8 verdict §1.2)".
- **C-2 (l.876–877 against the (α1) row).** "Few counts (Z(νν) … 2–190 under option (a) (pile-up fall …))" and the table's
  "expected pilot counts at 0.8: m_Z 31-53" are two planning estimates of the Z(νν) pilot count under a pile-up-like
  fall. The first comes from the attributed hard-scatter rate, the second from the conversion count. They are not
  reconciled: at ε_pair = 0.8 the first is below the limit of 12 and the second above. This text is pre-existing and
  labelled EST, and no decision or expected outcome changes. Suggestion: add "(the conversion part alone: the (α1) row of
  the v9 table)".
- **C-3 (l.2968).** Replace "by itself above the day-15 class" with "by itself above the class B₅₀ = 300 (a result-basis
  floor; the day-15 rule reads the multijets through the Z(νν) pilot count)". This is the same distinction T5 and T9 make.
- **C-4 (l.118–119).** The leading sentence "no conversion rejection suffices" cites no table. Suggestion: add "(Q2 (c), v9
  grid)".
- **C-5 (T10 wording, l.2736).** "Since no other SM sample exists before the freeze" sits beside l.461 and l.1393, where a
  Z(νν) development sample exists before the freeze. The intended meaning is "no sample of another SM process". It is
  verbatim from the verdict, so this is a package or later wording matter only.
- **C-6 (COM).** Other defaults mark the rows they affect, for example "(Df-9)" and "(Df-10)". TG-1 is not marked
  "(Df-11)". Optional.
- **C-7 (record only, not the artifact).**
  - The verdict says the checker reports 42 mismatches on v8. It is 41 checks plus the summary line.
  - The fix report says v9 has 3,136 lines. `wc -l` gives 3,137.
  - The fix report's "Not done, proposed" bullet says the overridable-default presentation is left to the package, which
    O6 then did.
- **C-8 (pre-existing, l.2976).** "entries [Ingrid] and [Gunnar] for the last two versions" has been stale since v7 (the
  last two are Leopold and Mireille).

Checker blind spots (§1, items 1–6) are a limitation, not a finding: my sweep covered them for v9 and found no numeric
disagreement. If a later version restates any of U5, U6, U13 or U18 in a new form, add it to `req`, as verdict §4.2
already prescribes.

## 8. Conclusion

- Code = verdict.
- Output sha256 = expected.
- Self-test 8/8 PASS.
- Checker ALL OK 45/45 on v9, and 41 mismatches on v8.
- Tables verbatim.
- T1–T18 verbatim.
- 0 unattributed hunks.
- Figures unchanged.

**Category A: none. Category B: one (B-1, a one-word count fix at l.2336). Category C: eight.** With B-1 applied I see
nothing in this family that blocks PASS.
