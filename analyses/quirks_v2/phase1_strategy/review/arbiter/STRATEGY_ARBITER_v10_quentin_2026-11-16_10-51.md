# Arbiter verdict, review cycle 10: STRATEGY v10 (Oscar, 2026-11-16 10:41)

**Verdict: PASS.**

Arbiter: Quentin, fresh session, 2026-11-16 10:51 -05 (`date`). Role file `agents/arbiter.md` followed;
`methodology/06-review.md` §6.1 (categories) and §6.5 (hard cap at 10) read.
Artifact: `outputs/STRATEGY_oscar_2026-11-16_10-41.md` ("v10"; "l." is a line of v10), v9
`outputs/STRATEGY_mireille_2026-11-14_06-55.md`, `COMMITMENTS.md` ("COM"), `outputs/FIX_REPORT_cycle9_oscar.md`,
`outputs/day15_text_check_v10.txt`, `outputs/budget_stdout_v9.txt` ("stdout"), `src/check_day15_text.py` ("checker").
Review: critical (Pauline), `review/critical/STRATEGY_CRITICAL_REVIEW_v10_pauline_2026-11-16_10-47.md`.
Order of this cycle: cycle-9 verdict (`STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`, "verdict 9") §9.
Computation: einstein, `nice -n 19 python3 -I`, standard library, one process at a time; `strategy_budget.py` not run.
Scratch: `/var/tmp/jdochoa/quentin/` (`rebuild.py`, `v10_pre.md`, `check_v10.txt`, `c1.py`, `v10_c1.md`,
`check_c1.txt`). No git command, no sub-agent. Tags: VERIFIED = run or read in this session; ESTIMATE = a planning
number of the strategy; UNVERIFIED = the orchestrator's git facts, which I could not run myself.

## 0. Summary for the human

- Cycle 9 found one blocking slip: the table of what Gate A freezes said "ten defaults" where there are eleven. v10
  fixes it with the exact text the cycle-9 arbiter ordered, together with 13 wording edits that set out the pinned
  day-15 reading (Df-11) for you: it is a proxy that errs lenient, its alternative is more lenient still, and the
  limit of ≈ 12 Z(νν) pilot counts holds at an R09 candidate (≈ 6–7 at R08).
- I confirmed independently that v10 equals v9 plus those texts plus bookkeeping, byte for byte. The text checker
  passes 45 of 45, the budget script and its output have not changed, and every current statement of the count says
  eleven.
- No number shown to you is wrong. No number, criterion, default, CPU-h or calendar figure changed between v9 and
  v10. The one rule sentence that was added (E6: at least 10⁵ draws; a reading within that precision of 300 pauses) is
  yours to drop at Gate A.
- Category A: 0. Category B: 0. Category C: 2 (one wording edit ordered below, one process record).

---

## 1. Form of this cycle

Verdict 9 §9 ordered a **narrow mechanical check**: one fresh critical reviewer, then the arbiter. It did not order
the three-reviewer panel, which had run in cycles 1–9. Admissible findings were limited to a regression of this fix
or a factual error in a number shown to the user. The pinned rule 1, the two tables, Q1–Q5, Df-1–Df-11, the design
and the budget were settled.

**I find this adequate for the size of the change.** Reasons:
1. The change is 14 single-line replacements in v10 (13 hunks), one in COM, and bookkeeping. Every replacement is text
   written by the cycle-9 arbiter, who tested it against the checker before ordering it. The fixer inserted it by
   program, and the reviewer and I each confirmed the result by reconstructing it independently (§2).
2. The new text adds no design element. Its quantities fall into three groups: already-printed stdout values, numbers
   already in v9 (l.2747–2748), and one labelled non-script quantity (R08: ≈ 6–7 and 1–2 counts). The cycle-9 physics
   reviewer and arbiter verified that last quantity with two independent samplers, and the reviewer and I re-checked
   it (§4).
3. A physics or constructive reviewer could add only an opinion on settled matters, which §9 excludes. The admissible
   failure modes (an unattributed hunk, a wrong byte, a stale count, a wrong number) are mechanical, and the check
   covers each of them.
4. The methodology's re-review rule (§6.5: each A/B finding verified explicitly in a written re-review) is met for B-1
   by the critical review §f and by my §3.

One residual limit: the E-texts were written by an arbiter and, apart from their numbers, were never read by a
physics reviewer. I read each changed passage for sense (§4) and found nothing wrong.

---

## 2. Last-line confirmations (all VERIFIED in this session)

| check | result |
|---|---|
| `diff` v9 → v10 | 18 hunks: `1c1 3,5c3,5 7c7 95c95 101c101 119c119 877c877 2336c2336 2736c2736 2756,2757c2756,2757 2819c2819 2892c2892 2949c2949 2968c2968 2976c2976 2979c2979 3128a3129,3139 3136c3147`; 3,137 → 3,148 lines. Equal to the reviewer's list and the fix report |
| own reconstruction | My own `rebuild.py` parses verdict 9 §5 and applies E1–E13b to v9, asserting each old string once in v9 and once in the running text (14 of 14 found once). Result sha256 `0e509b4fdaba65a512f95e1aae9742b4f7b3901d436dbb247db603eb62326fd4` = the value of verdict 9 §5 |
| rebuilt → v10 | `diff` shows exactly the bookkeeping: header (`1c1`, `3,5c3,5`, `7c7`), §13.9 (`3128a3129,3139`), code reference (`3136c3147`). **Hunk attribution: 13 E-hunks + 5 bookkeeping hunks, 0 unattributed** |
| §13.9 | the verdict-9 sentence present verbatim (l.3133); rows B-1 (E1) and C items (E2–E14); "No number of the script, default, CPU-h or calendar figure changed" is true by the reconstruction |
| checker on v10 | `nice -n 19 python3 -I src/check_day15_text.py v10 stdout`: exit 0, "text check: ALL OK (45 of 45)", 0 MISMATCH; `cmp` with `outputs/day15_text_check_v10.txt`: identical; that file and `_v9.txt` share sha256 `9c9d48a5…252c15` |
| stdout | sha256 `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d`, equal to verdicts 8 and 9 |
| script | sha256 `548b5ba8c3cbf65682708c7c8b034d2c62b2f8c1436142156f77e9775908c634`, equal to the orchestrator's stated value (`548b5ba8…908c634`) and the fix report; mtime 2026-11-14 00:43:45.876823805, identical to the checker's |
| checker file | sha256 `0808569be42b3119a1ae782feec991a301b39794ed13abc9eae9336638c9184a` (`0808569b…9184a`, verdict 9 §1) |
| v9 | sha256 `5b708d8e…a905e1`, unchanged |
| v10 | sha256 `0428ce604d3c9a39312594e5dc66fb55ffe247d1717c6f17446ca5b1dae8a167` (= fix report) |
| COM | sha256 `f19023ad…e7d067` (= fix report "after"); 264 lines, read in full |

**COM against the orchestrator's git facts.** The orchestrator states COM changed by +12/−4 lines (UNVERIFIED by me;
no git). The fix report's four hunks predict exactly this: pointer l.3–4 (2 → 2), earlier versions l.8 → l.8–9
(1 → 2), new section l.32–38 (+7), ST-1 l.237 (1 → 1); removed 2 + 1 + 1 = 4, added 2 + 2 + 7 + 1 = 12. The
reviewer's uniform +8 shift of the cited rows agrees. Every other row I compared with verdict 9's citations (GA, the
version-4 and version-3 history rows) is unchanged in content. I regard the reviewer's two "could not verify" items
as closed: COM byte stability (by +12/−4 together with the hunk arithmetic), and the script unchanged since cycle 9
(by the orchestrator's statement that nothing under `P1/src/` changed and that `strategy_budget.py` was last changed
in the v9 commit with the hash I measured). Both rest partly on facts the orchestrator stated, which I could not
check without git. Nothing I measured contradicts them.

---

## 3. B-1 re-verified: every statement of the number of defaults

| place | text | status |
|---|---|---|
| v10 l.8 | "five questions Q1–Q5 and eleven defaults" | current, correct |
| v10 l.141 | "Eleven defaults are reported and can be overridden." | current, correct |
| v10 l.2336 | "the answers to Q1–Q5 and the eleven defaults (Df-1–Df-11, §12.1)" | current, correct (E1) |
| v10 §12.1 | 11 rows `Df-1` … `Df-11` (`grep -cE '^\| \*?\*?Df-[0-9]+'` = 11); no Df-12 or higher | correct |
| v10 l.3126, 3133, 3137 | §13 history (O6 ten → eleven; §13.9) | history, correct |
| COM l.241 (GA) | "the eleven defaults (Df-1–Df-11)" | current, correct |
| COM l.36, l.44 | version-10 and version-9 rows: eleven | correct |
| COM l.94, l.131, l.142 | "ten defaults (Df-9, Df-10 added)", "Df-1–Df-8", "eight defaults" | history rows, correct as history |

No current statement says anything other than eleven. **B-1: RESOLVED.**

---

## 4. Changed passages read for sense and numbers (admissible scope)

I read l.1–8, 95, 101, 119, 877, 2336, 2736, 2756–2757, 2819, 2892, 2949, 2968, 2976, 2979 and §13.9 in full in v10.

| number shown to the user | source (VERIFIED) | result |
|---|---|---|
| R09 pile-up median 6.7; R08 88–148, median 118 | stdout l.355, l.280, l.301 | equal |
| 0.231 / 0.255 / 0.379 | stdout l.355–366 (Z(νν) 0.231 the pilot's own; 0.255; 0.379) | equal |
| 5.9×10³ against 6.4–9.5×10³; "≈ 8 %, at most ×1.6" | v10 l.2747–2748 (unchanged from v9); 6,421/5,918 = 1.085, 9,527/5,918 = 1.610 | consistent (8.5 % written "≈ 8 %", see O-2) |
| 1.66 × Z(νν) counts; 18 events per Z(νν) count; 65 per DIF count | stdout l.355 ("18.1 (= … 1.66 x Z(nunu)'s own 10.9)", "DIF 65.1") | equal |
| 37 % | 3,559/9,527 = 0.374 | equal |
| limit ≈ 12 Z(νν), between 3 and 4 DIF counts (R09) | stdout l.359–360 (300 at 12 "at the limit"; 266 at 3, 331 at 4) | equal |
| ≈ 6–7 Z(νν), 1–2 DIF counts at R08 (labelled not script-printed) | verdict 9 §4.1 sampler: 291.6 / 310.2 at m_Z = 6 / 7; 243.0 / 306.7 at m_D = 1 / 2; ESTIMATE check (300 − 181)/18.1 = 6.6, (300 − 181)/65.1 = 1.8 | consistent; "about half as high" (12 → 6–7; 3–4 → 1–2) correct |
| "precise to about 0.3 %" at 10⁵ draws (E6) | reviewer's ESTIMATE 0.28 %; verdict 9 §4.2 seed spread 299.6–300.3 at 2×10⁴ draws (≈ 0.1–0.2 % spread there, so ≈ 0.3 % at 10⁵ is conservative) | consistent |
| rider trigger 3,000; day-7 reading ≈ 3×10⁴–3×10⁵; (α1) lower edge 2.6×10³ < 3,000 | stdout l.362–363 | E12 statement correct |
| B4-e floor 4.6×10³ "above the class B₅₀ = 300" | v10 l.2968 [E] | correct; the relabelling is accurate (a result floor, not a day-15 term) |

Sense: E6 makes the "at the limit" row (300 at m_Z = 12) a pause, and the text says "limit at ≈ 12" throughout, so
the two are consistent. E4 ("no sample of another SM process") is correct, because a Z(νν) development sample exists.
E11 states two unreconciled EST numbers and says so. E13a/E13b are factual. **No regression and no factual error in a
number shown to the user.**

---

## 5. Structured adjudication table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---|---|---|---|---|
| 1 | B-1 (cycle 9): "ten defaults" in §8 freeze table | Critical (checks a, f) | resolved | **closed** | Case 3; §3. E1 applied byte-exact; every current statement says eleven |
| 2 | E2–E14 applied as ordered | Critical (a, b, e, g) | PASS | **closed** | Case 3; §2 own reconstruction gives the same hash |
| 3 | C-1: Tags paragraph l.16 names only the first six authors | Critical | C | **C, apply (ordered, §6)** | Case 3. Pre-existing since v7 (`diff` of l.16 v9→v10 empty), so not a regression of this fix. It states no number, so it is not admissible as blocking under verdict 9 §9. But it is factually incomplete (Jules, Leopold, Mireille and Oscar wrote tagged sentences), it is the same kind of slip as E13a (rated C in cycle 9), and it costs one line. Applied before commit, no re-review |
| 4 | C-2: fixer ran one read-only `git diff` | Critical; fix report flag 2 | C (record) | **record only** | Process, not artifact. The orchestrator's own git shows no change outside the expected files; hashes consistent. The orchestrator should restate the no-git rule in future fixer prompts |
| 5 | O-1: no earlier record of the script's sha256 | Critical | observation | **closed** | §2: the orchestrator's git fact (last change in the v9 commit, `548b5ba8…908c634`) equals my measured hash; identical mtime with the checker, whose hash is recorded; stdout unchanged |
| 6 | O-2: "≈ 8 %" for 8.5 % (E7, E8; also in the Gate-A draft Df-11 row) | Critical | observation | **no category; no edit** | It is verdict 9's settled text, written with "≈", and states correctly the direction and the ×1.6 bound that matter. Not a factual error under §9. Recorded so that a reader who recomputes 1.085 is not surprised |
| 7 | Reviewer's "could not verify" on COM bytes | Critical (§e) | limit | **closed** | §2: +12/−4 matches the hunk arithmetic exactly |

Dismissals: none. Deferrals carried from cycle 9, unchanged: Physics C-4 (self-test 7 to ±5 %, more DIF draws) to
Phase 2, with the commitment in verdict 9 §4.3(iii).

**Regression triggers (§6.7).** A strategy has no validation test, fit, systematic breakdown, bin exclusion or GoF
result, so none applies. (On record: the strategy expects the conversion normalisation to carry > 80 % of the
uncertainty in the expected branch and investigates it; Gate-A risk 3.)

**Motivated reasoning.** The fixer's account matches every measurement (hashes, hunks, checker output, line counts).
Its two flags (the l.16 author list and its own `git diff`) were disclosed against its own interest. Nothing in v10
says "addressed later" about anything that could change the result. The human-facing limit now names both favourable
choices it rests on (the R09 term and the Z(νν) photon rate).

**Reviewer pressure.** No finding disputed; I lower no category.

**Last-cycle check.** I would give the same verdict at cycle 3. The blocking item is fixed exactly and verifiably,
and the only open item is a one-line pre-existing C.

---

## 6. Ordered C edit (apply before commit; **needs no re-review**)

**C-1, v10 l.16 (Tags paragraph).** File `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`.
The old string occurs exactly once (VERIFIED).

Old: `(Brigitte, Dmitri, Emeric, Fiona, Gunnar or Ingrid, whoever wrote it)`
New: `(the author of the version that introduced the sentence, §12.2)`

Tested on a scratch copy (`/var/tmp/jdochoa/quentin/v10_c1.md`): one hunk `16c16`, line count unchanged (3,148),
checker "ALL OK (45 of 45)" with output byte-identical to `day15_text_check_v10.txt`. The file's sha256 after the edit
is `d806bb362a514b3fba687ad107018be9fe42ac7e3ad665cbb98b4432e020b779`. This edit needs no re-review (Category C,
methodology §6.1 and the study's protocol). The orchestrator applies it in place, keeping the file name (it is the
version the human approves, not a new version). It records the new sha256 in `LOG.md` and in the commit message.
No change to §13.9 or COM is needed. If the edit is not applied, the PASS stands. The Gate-A record then cites
`0428ce60…a8167`.

---

## 7. Final iteration table and audit paragraph

| cycle | version reviewed | panel | merged A | merged B | verdict |
|---|---|---|---|---|---|
| 1 | v1 (Brigitte) | physics, critical, constructive, arbiter | 11 | 24 | ITERATE |
| 2 | v2 (Dmitri) | same | 4 | 14 | ITERATE |
| 3 | v3 (Emeric) | same | 1 | 15 | ITERATE |
| 4 | v4 (Fiona) | same | 0 | 5 | ITERATE |
| 5 | v5 (Gunnar) | same | 0 | 3 | ITERATE |
| 6 | v6 (Ingrid) | same | 0 | 1 (U1) | ITERATE |
| 7 | v7 (Jules) | same | 0 | 4 (one family, V1) | ITERATE |
| 8 | v8 (Leopold) | same | 0 | 1 (W1) | ITERATE |
| 9 | v9 (Mireille) | same | 0 | 1 (B-1) | ITERATE |
| 10 | v10 (Oscar) | critical (narrow, verdict 9 §9), arbiter | 0 | 0 | **PASS** |

A: 11 → 4 → 1 → 0 → 0 → 0 → 0 → 0 → 0 → 0. B: 24 → 14 → 15 → 5 → 3 → 1 → 4 → 1 → 1 → 0.

**Audit.** Cycles 1–3 rebuilt the method: a zero-count convention with a coverage test, closure on disjoint rungs
and samples, a no-credit ceiling H, an always-added extrapolation width, a sealed C1 tier and the full process list.
Cycles 4–5 made the summary honest: by v1's own counts the expected background is ≈ 0.7–1.0×10⁴ events, the reach is
below 243 GeV at the strategy's own normalisation width, and the day-15 rule is expected to pause the study. The
budget was fixed at 4,609 CPU-h. Cycles 6–8 changed no design choice. Their common root cause, found in cycle 8, was
an ambiguous rule 1, which cycle 8 pinned (Df-11), recomputed and guarded with a self-test and a 45-check text checker.
Cycle 9 confirmed this and found one stale count. Cycle 10 confirms the exact fix. The study reached the hard cap, but
not because review looped on one item. The blocking findings converged monotonically from cycle 7 on, each cycle
smaller than the last, and the last two were a single word in one table row and nothing. Process notes for the
record: the cycle-9 stop and resumption by the user (with a cluster fault and a clock correction logged in `LOG.md`),
one read-only `git diff` by the fixer (C-2), and one known deferral to Phase 2 (Physics C-4).

---

## 8. What the human decides at Gate A (v10 §12.1)

1. **Q1** C1 signal comparison and blinding (default: six counts sealed until Gate B, four open).
2. **Q2** (central) the deliverable if the day-15 projection exceeds B₅₀ = 300 (the expected case): (a) pause and ask
   (default), (b) proceed, (c) redesign before the freeze; optional rider (day-7 trigger, +7.0 CPU-h).
3. **Q3** the exception to brief D4 for MUST closure criteria that end untested (default: yes; annex routes 1–6).
4. **Q4** budget, calendar and stop rule: 4,609 CPU-h, 60 days, stop-and-ask at 5,992, with [DP1], [DP2], [DP4], [DP5].
5. **Q5** the reading of brief D7 for the truth-level signal samples (default: before the hash).
6. **Df-1–Df-11**, each overridable. Df-11 (the pinned day-15 reading) is the one to read with care: it is a lenient
   proxy, and its alternative is more lenient still. **E6** (the 10⁵-draw precision rule in §11.7 rule 1) may be
   dropped, in which case it becomes a Phase-2 obligation (verdict 9 §4.2).

The artifact of record is STRATEGY v10 (with C-1 applied) together with `COMMITMENTS.md`, `budget_stdout_v9.txt` and
`src/check_day15_text.py`.

---

## 9. Gate-A package (`gates/GATE_A_DRAFT.md`): check and required changes

**Numbers.** v10 changed no number relative to the v9 + §5 text that the draft already describes. Verdict 9 §7 found no
wrong number in it. I re-checked the items that concern this cycle against v10 and the stdout: Q2 table rows, the
76 / 281 / 300 / 317 / 266 / 331 / 109–130 / 458–718 readings, Df-11 row (≈ 8 %, ×1.6, ≈ 12 at R09, ≈ 6–7 at R08,
≈ 20 for the alternative = 12 × 1.66), risk 2 (65 per DIF count; four pause at R09, two at R08 by the 306.7 reading),
s95 2,697 against 352 (stdout l.330), ≥ 560 GeV (v10 l.1027, 2755, 2887), 4,176 / 5,429, 5,123 / 6,660, 6,759 / 8,787,
2,150, Q3 680 (100–1,230), Q5 313 / +47 / +1.8 days. **All agree. "ties pause" in the Df-11 row stays, because E6 was
applied.**

**Required changes now that v10 exists and has passed:**
1. **Banner (l.1–7):** replace the whole "DRAFT — NOT YET THE GATE-A PACKAGE …" block with:
   "> Phase-1 review PASSED in cycle 10 (`phase1_strategy/review/arbiter/STRATEGY_ARBITER_v10_quentin_2026-11-16_10-51.md`).
   > Artifact of record: STRATEGY v10 (`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`), `COMMITMENTS.md`,
   > `budget_stdout_v9.txt`, `src/check_day15_text.py`. Times in file names before 2026-11-16 are sequence labels, not
   > clock times (`LOG.md` correction of 2026-11-14 01:20)."
2. **Sources line (l.11):** "Sources: STRATEGY v10 (STR, `STRATEGY_oscar_2026-11-16_10-41.md`), `budget_stdout_v9.txt`
   (stdout). **All reach and background numbers: ESTIMATE on v1 placeholder efficiencies**."
3. **Review line (l.39–40):** "- Review: cycles 1–10, Category A 11→4→1→0→0→0→0→0→0→0, Category B
   24→14→15→5→3→1→4→1→1→0 (cycle 9: a stale count, fixed in v10; cycle 10: a mechanical check of v10, PASS).
   Cycles 4–8 turned on the day-15 reading; cycle 8 found rule 1 ambiguous and pinned it (Df-11: limit ≈ 12 Z(νν)
   pilot counts, not ≈ 20)."
4. **§9 Files (l.133–134):** "STR v10 (§0, §12.1); `budget_stdout_v9.txt`; `src/check_day15_text.py` (45 of 45 on v10);
   `COMMITMENTS.md`; `phase1_strategy/outputs/feasibility/`; `phase1_strategy/review/arbiter/` (cycle-10 verdict);
   `LOG.md`; `DEVIATIONS.md`."
5. **§3 or §4 (optional, one line):** a note that E6 (ties pause; 10⁵ draws) may be dropped. It then moves to Phase 2.
   The Df-11 row then loses "ties pause".

No other text of the package changes.

---

## 10. Verdict

**PASS.**
- Category A: 0. Category B: 0 (B-1 of cycle 9 resolved, §3). Category C: 2. C-1 is applied before commit by the
  exact edit of §6, with no re-review; C-2 is a process record.
- Observations O-1 closed, O-2 no edit. Deferred from cycle 9: Physics C-4 to Phase 2.
- Artifact of record for Gate A: STRATEGY v10 (with C-1), `COMMITMENTS.md`, `budget_stdout_v9.txt`,
  `src/check_day15_text.py`. Gate-A package: the draft with the four required changes of §9.

**Verdict: PASS.**
