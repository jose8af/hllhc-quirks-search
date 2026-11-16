# Critical review, cycle 10: STRATEGY v10 (Oscar, 2026-11-16 10:41)

Reviewer: Pauline, fresh session, 2026-11-16 10:47 -05 (`date`). Scope: the narrow check of the cycle-9 arbiter verdict
§9 (`review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`, "verdict"). "v9" =
`outputs/STRATEGY_mireille_2026-11-14_06-55.md`, "v10" = `outputs/STRATEGY_oscar_2026-11-16_10-41.md`, "COM" =
`COMMITMENTS.md`, "checker" = `src/check_day15_text.py`, "stdout" = `outputs/budget_stdout_v9.txt`.
Method: einstein, `nice -n 19`, standard-library `python3 -I`, one process at a time; scratch in
`/var/tmp/jdochoa/pauline/` (`rebuild.py`, `sent.py`, `v10_prebook.md`, `check_v10.txt`, `check_pre.txt`). No git
command, no sub-agent, `strategy_budget.py` not run. Every result below was produced in this session (VERIFIED) unless
tagged otherwise. Per the task prompt I wrote nowhere but this file and my scratch dir (so no session log in `logs/`).

## Summary

| check | result |
|---|---|
| a. diff v9 → v10: every hunk attributed, new strings exact | **PASS** (18 hunks, 0 unattributed) |
| b. reconstruction of "E1–E13b applied, before bookkeeping"; sha256; + bookkeeping = v10 | **PASS** (`0e509b4f…26fd4` reproduced) |
| c. checker on v10 against stdout | **PASS** (ALL OK, 45 of 45; byte-identical to `day15_text_check_v10.txt`) |
| d. script, stdout, checker untouched | **PASS** (with one limit: no cycle-8/9 record of the script's own sha256, see §d) |
| e. COM: pointer, earlier versions, new section, E14 | **PASS** (what could not be verified without the previous COM is listed in §e) |
| f. every statement of the number of defaults | **PASS** (all current statements say eleven; 11 Df rows) |
| g. bookkeeping: header, §13.9, code reference | **PASS** |

**Findings.** Category A: none. Category B: none. Category C: two (C-1 the Tags paragraph l.16, pre-existing; C-2
the fixer's `git diff`, process only, record). Observations without category: O-1 (no earlier record of the script's
sha256), O-2 ("≈ 8 %" for 8.5 %).

---

## a. diff v9 → v10

Command: `diff v9 v10 | grep -E '^[0-9]'` → 18 hunks:
`1c1 3,5c3,5 7c7 95c95 101c101 119c119 877c877 2336c2336 2736c2736 2756,2757c2756,2757 2819c2819 2892c2892 2949c2949
2968c2968 2976c2976 2979c2979 3128a3129,3139 3136c3147`. `wc -l`: v9 3,137, v10 3,148 (+11 = the §13.9 block).

| hunk | attribution | how verified |
|---|---|---|
| 1c1 | bookkeeping: header "version 10" | prebook → v10 diff (b) |
| 3,5c3,5 | bookkeeping: fixer, time, replaced version 9, ninth verdict, "finding B-1 and the C items it orders" | (b), (g) |
| 7c7 | bookkeeping: status "for verification and then the user's Gate A" (verdict wording) | (b), (g) |
| 95c95 | E2 | (b): line equal to my rebuilt line |
| 101c101 | E3 | idem |
| 119c119 | E10 | idem |
| 877c877 | E11 | idem |
| 2336c2336 | E1 (B-1) | idem |
| 2736c2736 | E4 | idem |
| 2756,2757c2756,2757 | E5 (l.2756), E6 (l.2757) | idem |
| 2819c2819 | E7 | idem |
| 2892c2892 | E12 | idem |
| 2949c2949 | E8 | idem |
| 2968c2968 | E9 | idem |
| 2976c2976 | E13a | idem |
| 2979c2979 | E13b | idem |
| 3128a3129,3139 | bookkeeping: §13.9 | (b), (g) |
| 3136c3147 | bookkeeping: code reference → `day15_text_check_v10.txt` | (b), (g) |

**Unattributed hunks: 0.** Character-for-character: my rebuild (b) takes every "New" string programmatically from
verdict §5 (no retyping); for each of the 14 edited lines `sed -n Np` of my rebuilt file and of v10 have the same
sha256 (14 of 14 "same"), and the whole rebuilt file equals the verdict's expected hash. So every new string in v10 is
the verdict's text byte for byte. The hunk list equals the fix report's table.

## b. Reconstruction

`/var/tmp/jdochoa/pauline/rebuild.py` (own code; parses §5 between "## 5." and "## 6." of the verdict: `Old:`/`New:`
backtick lines, and the two `~~~~` blocks of E8; asserts each old string occurs exactly once in v9 and once in the
running text, then replaces). Output: 15 items found (E1–E13b, E14); E1–E13b each "count in v9: 1, in running: 1";
result 3,137 lines, sha256 **`0e509b4fdaba65a512f95e1aae9742b4f7b3901d436dbb247db603eb62326fd4`** = the verdict's
value. `diff v9 rebuilt` gives exactly the 13 hunks of §5 (`95c95 … 2979c2979`), no line added or removed.

`diff rebuilt v10` gives exactly five hunks: `1c1`, `3,5c3,5`, `7c7`, `3128a3129,3139`, `3136c3147`, all
bookkeeping (header, §13.9, code reference). (The fix report says "these four hunks", counting the three header hunks
as one change; the content is the same.) **Rebuilt state + bookkeeping hunks only = v10: confirmed.** (The fixer's scratch
`/var/tmp/jdochoa/oscar/v10_pre.md` also hashes to `0e509b4f…`; I did not use it for the check.)

## c. Checker

Command: `nice -n 19 python3 -I src/check_day15_text.py outputs/STRATEGY_oscar_2026-11-16_10-41.md
outputs/budget_stdout_v9.txt` → exit 0, last line **"text check: ALL OK (45 of 45)"**, 45 lines "OK", 0 "MISMATCH".
`cmp` with `outputs/day15_text_check_v10.txt`: identical (sha256 `9c9d48a5…252c15` for both). The checker also gives
the same output on my rebuilt pre-bookkeeping state and on v9 (`cmp` with `day15_text_check_v9.txt`: identical);
`day15_text_check_v9.txt` and `_v10.txt` have the same sha256, as the verdict predicted ("the same statement counts as
on v9"). The checker takes both paths as arguments (`sys.argv[1:3]`, l.11), so it needed no change.

## d. Script, stdout, checker

| file | sha256 (this session) | expected / record | result |
|---|---|---|---|
| `outputs/budget_stdout_v9.txt` | `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d` | verdict §1, §9; cycle-8 fix report l.47 | equal |
| `src/check_day15_text.py` | `0808569be42b3119a1ae782feec991a301b39794ed13abc9eae9336638c9184a` | starts `0808569b`, ends `9184a` (verdict §1) | equal |
| `src/strategy_budget.py` | `548b5ba8c3cbf65682708c7c8b034d2c62b2f8c1436142156f77e9775908c634` | fix report l.19 (before = after); fixer log l.4 | equal to fix report |
| v9 | `5b708d8e…a905e1` | fix report l.18 | equal (v9 unchanged) |

mtimes (`ls --full-time`): script and checker 2026-11-14 00:43:45.876823805, stdout 00:45:10 (all before v9's own
mtime 00:52:24 and long before the cycle-10 work on 2026-11-16). Script 1,556 lines.

**Limit (O-1).** I searched every `*.md` of the study for `548b5ba8`: the only hits are the cycle-9 fix report and the
fixer's log. The cycle-8 and cycle-9 records give the stdout's sha256 (and the arbiter ran the script and obtained a
byte-identical stdout), but no record states the script's own sha256. So "script untouched since cycle 9" rests on
(i) the identical mtime shared with the checker, whose hash is recorded and matches; (ii) the fixer's before/after
values; (iii) the stdout being unchanged. Without git I cannot compare with the committed blob. Not a finding against
v10; the arbiter or orchestrator can close it with one `git` comparison against commit `25b3ff5^`.

## e. COMMITMENTS.md

COM sha256 now `f19023ad…e7d067` (= fix report "after"), 264 lines.

| item | COM text | vs verdict | result |
|---|---|---|---|
| pointer | l.3–4: "Current strategy: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` ("STR" below; version 10, after review cycle 9)" | "pointer to version 10" | present |
| earlier versions | l.8–9: "… `STRATEGY_leopold_…` (version 8) and `STRATEGY_mireille_2026-11-14_06-55.md` (version 9)." | "v9 added to the earlier versions" | present |
| new section | l.32 "## Changes of rows in version 10 (2026-11-16, fixer Oscar, review cycle 9: B-1; nothing removed)" | name per verdict; heading format as earlier sections | present |
| row GA | l.36 "\| GA \| freeze table of STR §8 counts eleven defaults (B-1); no status changed \|" | verdict text exactly | equal |
| row ST-1 | l.37 "\| ST-1 (Q4, Df-11) \| marked with the default it depends on; rule 1 states the precision of the binding median and that a reading within it pauses; no status changed \|" | verdict text exactly | equal |
| E14 | l.237 "\| ST-1 (Q4, Df-11) \| Stop rules of brief §7 and D6, …" | New of E14 | equal; the row cites "decision-point-2 rules of STR §11.7 (rule 1 …)", so the marking is apt |
| stale pointers | `grep "mireille\|oscar\|version 9\|version 10\|v9\|v10"`: only l.3, 4, 9, 32, 39 | — | none stale |

**Could verify:** the five items above, character-for-character, and that no other place names a current version.
Indirect evidence that nothing else moved: the verdict cites COM l.233 (GA), l.36 (version-9 GA row), l.86 (version-4
row), l.134 (version-3 "eight defaults"); these rows are now at l.241, l.44, l.94, l.142, a uniform +8 = 7 lines of the
new section + 1 line of the pointer paragraph, which is what the fix report's four hunks predict. **Could not verify:**
that no other byte of COM changed (no copy of the previous COM: the fixer's scratch holds none, and git is out of my
scope), nor the "before" sha256 `e0b9d01d…` of the fix report. One `git diff 25b3ff5 -- COMMITMENTS.md` by the
orchestrator closes it.

## f. Statements of the number of defaults

Searches (v10 and COM): whole words "ten", "eleven", "eight", "nine"; "defaults"; "Df-" identifiers.

v10, hits that concern defaults:

| line | text | judgement |
|---|---|---|
| 8 | "five questions Q1–Q5 and eleven defaults" | current, correct |
| 141 | "Eleven defaults are reported and can be overridden." | current, correct |
| 2336 | "the answers to Q1–Q5 and the eleven defaults (Df-1–Df-11, §12.1)" | current, correct (E1) |
| 2935–2949 | §12.1 table "Defaults the user can override": rows Df-1 … Df-11 at l.2939–2949 | **11 rows** (`grep -E '^\| \*?\*?Df-[0-9]+'`) |
| 3126 | §13.8 O6 row "the count of defaults ten → eleven" | history, correct |
| 3133 | §13.9 "now counts eleven defaults" | history (current statement), correct |
| 3137 | §13.9 B-1 row quoting the old "the ten defaults"; "there are eleven" | history, correct |

v10 hits of the count words not about defaults (checked by context): "ten" l.617, 1902, 1905 (ten times the rows),
2795 (Q1: "all ten open" = the C1 signal counts); "eleven" l.1278, 1402, 2116, 2551, 2728, 3075 (processes, rows);
"eight" l.612, 975, 1009, 1300, 1395, 1640, 1873, 1885, 1913, 2286, 2459, 2904, 2910 (proxied processes, grid values,
Λ); "nine": 0 hits. No "Df-12" or higher; "Df-1–Df-11" twice; no "Df-1–Df-10".

COM:

| line | text | judgement |
|---|---|---|
| 36 | version-10 row "counts eleven defaults (B-1)" | correct |
| 44 | version-9 row "eleven defaults: Df-11 … added" | correct |
| 94 | version-4 row "ten defaults (Df-9, Df-10 added)" | history, correct as history |
| 131 | version-3 row "replaced by Q1–Q5 and Df-1–Df-8" | history, correct as history |
| 142 | version-3 row "now five questions and eight defaults" | history, correct as history |
| 241 | GA "the eleven defaults (Df-1–Df-11)" | current, correct |
| 151, 175, 177 | "Six of the ten" (C1 counts), "eight proxied processes" | not about defaults |

Every current statement says eleven; the table has eleven rows. The fix report's list (its §"Every statement") agrees
with mine.

## g. Bookkeeping

- **Header** (l.1–8): "— version 10"; "Fixer: Oscar, 2026-11-16 10:41, review cycle 9. This version replaces
  `STRATEGY_mireille_2026-11-14_06-55.md` (version 9, kept unchanged) after the ninth arbiter verdict ITERATE
  (`review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md`: finding B-1 and the C items it orders)";
  "Status: for verification and then the user's Gate A." All as §5 orders. Facts: v9 unchanged (sha256 `5b708d8e…` =
  fix report "before"); the stamp 10:41 is consistent with v10's mtime 2026-11-16 10:42:44; "review cycle 9" follows
  v9's convention (v9 header: "review cycle 8" for the cycle-8 fix).
- **§13.9** (l.3129–3139): the verdict sentence is present verbatim as one line, count 1
  (`sent.py`: the sentence extracted from the verdict, whitespace-normalised, equals l.3133). Two rows: B-1 (E1) and the
  C items (E2–E14). Factual check of the C row against verdict §4.3(i): physics C-1–C-3, critical C-1–C-6 and C-8
  (C-7 record-only, correctly absent), constructive C-1–C-4, arbiter item 17 — exact; each E summary matches its
  edit; the sections column covers every edited place (§0 l.95/101/119, §4.4 l.877, §11.7 l.2736/2756/2757, §12.1
  l.2819/2892/2949/2968, §12.2 l.2976/2979, COM ST-1). The pointer sentence ("Every edit is the verdict's §5 text") is
  true by (b). §13.9 sits inside §13, so the checker excludes it from scans (C) and (D), as for earlier history.
- **Code reference** (l.3146–3147): checker command with `budget_stdout_v9.txt`; output in
  `outputs/day15_text_check_v10.txt` (file exists, equals my run). l.3144 "measured on einstein for version 9: 1 min
  15 s wall, 36 MB" is true (verdict §1: 1 min 15.4 s, 35,592 kB) and correctly not updated, since the script was not
  run for v10.
- **Fix report**: its hashes, line counts, hunk lists, item table and checker output all agree with my measurements.

## Spot-check of the numbers the new text shows the user (admissible scope: factual errors)

| number in v10 | source | result |
|---|---|---|
| "median 6.7 events" (l.2819) | stdout l.355 "pile-up R09 EST median 6.7" | equal |
| "88–148 at an R08 selection", "R08 median of 118" | stdout l.280 "R08 88-148", l.301 "EST pile-up median 118" | equal |
| 0.231 / 0.255 / 0.379 | stdout l.366 | equal |
| 5.9×10³ against 6.4–9.5×10³ | v10 l.2747–2748 (unchanged from v9) | equal |
| "≈ 8 % and at most ×1.6" | 6,421/5,918 = 1.0850; 9,527/5,918 = 1.6098 | consistent (see O-2) |
| "1.66 times as many Z(νν) counts" | stdout l.355 "1.66 x Z(nunu)'s own 10.9" | equal |
| "37 %" | 3,559/9,527 = 0.3736 | equal |
| "≈ 6–7 Z(νν) or 1–2 decays-in-flight counts" at R08 (labelled not script-printed) | ESTIMATE check: (300 − 181)/18.1 = 6.6 Z(νν) counts; (300 − 181)/65.1 = 1.8 DIF counts, with the verdict's R08 empty reading 181 and stdout l.355 (18.1 and 65.1 events per count) | consistent |
| "precise to about 0.3 %" (E6) | ESTIMATE: median s.e. ≈ 1.2533·σ_ln/√N; with σ_ln ≈ 0.7 (16–84 %: 37–152 around 76) and N = 10⁵: 0.28 % | consistent |
| cross-references "Q2 caption", "cycle-8 arbiter verdict §1.2" | Q2 at l.2798, caption l.2819; v8 verdict l.47 "### 1.2 Rule 1 is ambiguous …" | resolve |

No factual error found in a number shown to the user. No regression found.

---

## Findings

**Category A:** none. **Category B:** none.

**C-1. Tags paragraph names only the first six authors (v10 l.16).** "[V] VERIFIED: the number was read … by the
author of the sentence (Brigitte, Dmitri, Emeric, Fiona, Gunnar or Ingrid, whoever wrote it)". Jules, Leopold,
Mireille and Oscar also wrote tagged sentences (versions 7–10). Assessment: `diff` of l.16 between v9 and v10 is
empty, so this is pre-existing since v7 and **not a regression** of this fix; it states no number; the
verification standard it describes is unaffected, and §12.2 now says "one entry per version, under the name of its
author" (E13a), so the per-version author is recoverable. It is the same kind of slip as E13a, which the arbiter
rated C. Under verdict §9 it is not admissible as a blocking finding. **Category C.** Suggested text, if the
orchestrator applies it at Gate-A packaging: "(Brigitte, Dmitri, Emeric, Fiona, Gunnar or Ingrid, whoever wrote it)"
→ "(the author of the version that introduced the sentence, §12.2)". Not required for PASS.

**C-2. Process (record only, not the artifact).** The fixer reports one read-only `git diff` on COM against the "no
git commands" instruction (fix report "Flagged" item 2). Nothing in the files indicates a side effect; the hashes
above are consistent with no other change. Record for the orchestrator.

**Observations (no category):**
- **O-1.** No cycle-8/9 record of the sha256 of `strategy_budget.py` exists; the "untouched" claim rests on mtime,
  the fixer's values and the unchanged stdout (§d). One git comparison closes it.
- **O-2.** "≈ 8 %" (E7, E8) for 6,421/5,918 = 1.085 (8.5 %). It is the verdict's settled text, marked "≈", and
  understates by half a percent the size of a proxy whose direction is the point; not an error under §9.

**Conclusion for the arbiter.** Checks a–g all PASS. v10 equals v9 + the verdict's §5 strings + the ordered
bookkeeping, byte for byte; the checker passes 45 of 45; script, stdout and checker are unchanged as far as can be
established without git; every current statement of the defaults says eleven. Nothing admissible under §9 blocks.
