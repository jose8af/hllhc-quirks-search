# Fix report, review cycle 9 (fixer Oscar, 2026-11-16 10:41)

Verdict: `review/arbiter/STRATEGY_ARBITER_v9_odette_2026-11-14_07-55.md` (ITERATE; 0 A, 1 B = B-1). Scope: §5 of the verdict (E1–E14 and
"Bookkeeping") and nothing else. Artifacts: `outputs/STRATEGY_oscar_2026-11-16_10-41.md` (v10), `outputs/day15_text_check_v10.txt`,
`../COMMITMENTS.md`. v9 not modified. Script, stdout and checker not modified (sha256 below).

Method: `/var/tmp/jdochoa/oscar/apply_v10.py` parses the old/new strings of E1–E13b out of verdict §5 (backtick lines and the two
`~~~~` blocks of E8; the list of names asserted to be E1…E13b), asserts that each old string occurs exactly once in v9 and exactly
once in the running text, and replaces it. No replacement text was typed by hand. E14 and the bookkeeping were applied with the Edit
tool, wording of the COM rows and the §13.9 sentence copied from §5.

## sha256

| file | before | after |
|---|---|---|
| v10 after E1–E13b, before bookkeeping | — | `0e509b4fdaba65a512f95e1aae9742b4f7b3901d436dbb247db603eb62326fd4` (expected, §5: same value; **equal**) |
| v10 final (`STRATEGY_oscar_2026-11-16_10-41.md`, 3,148 lines) | — | `0428ce604d3c9a39312594e5dc66fb55ffe247d1717c6f17446ca5b1dae8a167` |
| v9 (`STRATEGY_mireille_2026-11-14_06-55.md`, 3,137 lines) | `5b708d8e1753e7a0dcbed7723429d8307a5c7f67f1464d040e214fa246f905e1` | same (unchanged) |
| `src/strategy_budget.py` (not run) | `548b5ba8c3cbf65682708c7c8b034d2c62b2f8c1436142156f77e9775908c634` | same |
| `outputs/budget_stdout_v9.txt` | `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d` | same |
| `src/check_day15_text.py` | `0808569be42b3119a1ae782feec991a301b39794ed13abc9eae9336638c9184a` | same (it takes both paths as arguments; no change needed) |
| `COMMITMENTS.md` | `e0b9d01d05211bab663cadc9ff2de40ee80a8a92adc36915a59981d8f6d504aa` | `f19023ad6c265fb2b41279847b13e5f91e520bc864b6fc0f9f58e10e7e07d067` |
| `outputs/day15_text_check_v10.txt` | — | `9c9d48a50017eb4fb3b734f26146cdf05dab85b947086d044d7100a95b252c15` |

`diff v9 → (v10 before bookkeeping)`: 13 hunks, `95c95 101c101 119c119 877c877 2336c2336 2736c2736 2756,2757c2756,2757 2819c2819
2892c2892 2949c2949 2968c2968 2976c2976 2979c2979`, equal to the list of §5; no line added or removed (3,137 lines).

## Status per item

| item | status | where | grep phrase |
|---|---|---|---|
| E1 (B-1) | RESOLVED | §8 freeze table, l.2336 | `the eleven defaults (Df-1–Df-11, §12.1)` |
| E2 | RESOLVED | §0 "The pause.", l.95 | `is an overridable default, Df-11` |
| E3 | RESOLVED | §0 "The pause.", l.101 | `v9 table; at the R09 pile-up estimate` |
| E4 | RESOLVED | §11.7 rule 1, l.2736 | `since no sample of another SM process exists before the freeze. The reading` |
| E5 | RESOLVED | §11.7 rule 1, l.2756 | `both at the R09 pile-up estimate` |
| E6 | RESOLVED (applied; the verdict says it may be dropped by the human) | §11.7 rule 1, l.2757 | `The binding B₅₀ is the median of at least 10⁵ draws` |
| E7 | RESOLVED | §12.1 Q2 caption of the day-15 table, l.2819 | `not a script-printed number` |
| E8 | RESOLVED | §12.1 row Df-11, l.2949 | `This is more lenient, not stricter` |
| E9 | RESOLVED | §12.1 annex, B4-e size, l.2968 | `by itself above the class B₅₀ = 300 (a floor in the result` |
| E10 | RESOLVED | §0 leading sentence, l.119 | `(Basis of the last statement: Q2 (c)` |
| E11 | RESOLVED | §4.4 point 5, l.877 | `the two estimates are not reconciled, both EST` |
| E12 | RESOLVED | §12.1 Q2 rider, l.2892 | `expected to trigger in the expected branch (α1′)` |
| E13a | RESOLVED | §12.2, l.2976 | `(one entry per version, under the name of its author)` |
| E13b | RESOLVED | §12.2, l.2979 | `pinned in review cycle 8 (Df-11); the Phase-3 slot table` |
| E14 | RESOLVED | COM ST-1 row (l.237) | `| ST-1 (Q4, Df-11) | Stop rules of brief §7` |
| Bookkeeping: header | RESOLVED | v10 l.1, l.3–5, l.7 | `version 10`; `finding B-1 and the C items it orders`; `Status: for verification and then the user's Gate A` |
| Bookkeeping: §13.9 | RESOLVED | v10 l.3129–3139 | `### 13.9 Changes since version 9`; the verdict sentence verbatim; rows B-1 (E1) and C items (E2–E14) |
| Bookkeeping: code reference | RESOLVED | v10 l.3147 | `outputs/day15_text_check_v10.txt` |
| Bookkeeping: COM | RESOLVED | COM l.3–4 (pointer, version 10), l.8–9 (v9 among earlier versions), l.32–37 (new section with the two rows) | `Changes of rows in version 10` |

## Text check (`nice -n 19 python3 -I src/check_day15_text.py outputs/STRATEGY_oscar_2026-11-16_10-41.md outputs/budget_stdout_v9.txt`)

ALL OK (45 of 45) on the final v10, and also on the state before bookkeeping. The output is byte-identical to `day15_text_check_v9.txt`
(same statement counts, as §5 states). Full output (`outputs/day15_text_check_v10.txt`):

```
OK       script self-test line :: v9 self-test: ALL PASS (8 of 8)
OK       (A) fenced blocks equal the printed table, line for line :: 17 quoted lines, 17 printed
OK       (B) §0 pause, §0 leading sentence, rider: expected reading :: '≈ 3×10⁴–3×10⁵' found 3, expected 3
OK       (B) §0 pause: (alpha1) reading :: '≈ 2.6×10³–4.2×10⁴' found 2, expected 2
OK       (B) §0 pause: empty reading :: 'B₅₀ ≈ 76 with every pilot count at zero' found 1, expected 1
OK       (B) §0, §4.4 (three places), §11.7: Z(nunu) limit :: '≈ 12 Z(νν) pilot counts' found 5, expected 5
OK       (B) §0, §11.7: DIF limit :: 'between 3 and 4 decays-in-flight pilot counts' found 2, expected 2
OK       (B) Q2 digest: (alpha1') row :: '≈ 3.2–3.3×10⁴ (ε_pair 0.8) to 3.2–3.3×10⁵ (0.98)' found 1, expected 1
OK       (B) Q2 digest: Z(nunu) row :: '281 at 11, 300 at 12, 317 at 13 | below up to 11, at the limit at 12, above from 13' found 1, expected 1
OK       (B) Q2 digest: DIF row :: '266 at 3, 331 at 4 | below up to 3, above from 4' found 1, expected 1
OK       (B) Q2 digest: empty row :: '76 (16–84 %: 37–152) | below' found 1, expected 1
OK       (B) Q2 digest: (c) credit row :: '| 109–130 | below' found 1, expected 1
OK       (B) Q2 (c): credit route :: 'B₅₀ 109–130) acts on both' found 1, expected 1
OK       (B) Q2 (c): conversions removed at the central size :: 'B₅₀ is 458–718' found 1, expected 1
OK       (B) Q2 (c): bar at f_D = 0 :: 'at least ×44 (97.7 %) [×30]' found 1, expected 1
OK       (B) Q2 (c): bar at f_D = 1/4 :: '×75–150 (98.7–99.3 %) [×51–101]' found 1, expected 1
OK       (B) Q2 (c): bar at f_D = e^-1 :: '×114 (99.1 %) [×77] at ×e⁻¹ with the pile-up fall ×339; at ×e⁻¹ with the fall ×201 none suffices' found 1, expected 1
OK       (B) Q2 (c): without S_CKF :: '×219–2,186' found 1, expected 1
OK       (C) pilot-count limits: 7 statements
OK       (C) rejection factor with its percentage: 2 statements
OK       (C) rejection factor in brackets: 3 statements
OK       (C) 'at least xN' / 'xN-M' rejection statements in Q2 (c): 2 statements
OK       (C) day-15 reading in powers of ten: 3 statements
OK       (C) B₅₀ ranges in 'The pause' and in Q2: 2 statements
OK       (D) no 'v8 table'
OK       (D) no 'budget_stdout_v8'
OK       (D) no '≈ 20\s+(?:Z\(νν\)\s+)?(?:pilot|counts in the pilot|in the pilot|ceiling)'
OK       (D) no '≈ 13\s+in the pilot'
OK       (D) no 'pool-equivalent'
OK       (D) no 'pilot ceiling'
OK       (D) no '5(?:\.0)?×10⁴–5(?:\.1)?×10⁵'
OK       (D) no '5\.0–5\.1×10[⁴⁵]'
OK       (D) no '2\.8×10³–4\.8×10⁴'
OK       (D) no '401–663'
OK       (D) no 'B₅₀ 51–74'
OK       (D) no '×34\b'
OK       (D) no '×23\]'
OK       (D) no '×52–81'
OK       (D) no '×69–235'
OK       (D) no '×35–55'
OK       (D) no '×47–159'
OK       (D) no 'U1 line'
OK       (D) no 'read as rule 1 reads them'
OK       (D) no 'would suffice'
OK       (D) no '×31\b'
text check: ALL OK (45 of 45)
```

## Diff of the strategy v9 → v10

`diff STRATEGY_mireille_2026-11-14_06-55.md STRATEGY_oscar_2026-11-16_10-41.md`: 18 hunks (3,137 → 3,148 lines).

| hunk | item |
|---|---|
| 1c1 | bookkeeping: header (version 10) |
| 3,5c3,5 | bookkeeping: header (fixer, time, replaced version, ninth verdict) |
| 7c7 | bookkeeping: header status ("for verification and then the user's Gate A") |
| 95c95 | E2 |
| 101c101 | E3 |
| 119c119 | E10 |
| 877c877 | E11 |
| 2336c2336 | E1 (B-1) |
| 2736c2736 | E4 |
| 2756,2757c2756,2757 | E5 (l.2756), E6 (l.2757) |
| 2819c2819 | E7 |
| 2892c2892 | E12 |
| 2949c2949 | E8 |
| 2968c2968 | E9 |
| 2976c2976 | E13a |
| 2979c2979 | E13b |
| 3128a3129,3139 | bookkeeping: §13.9 (heading, pointer sentence, verdict sentence verbatim, table with the B-1 and C-item rows) |
| 3136c3147 | bookkeeping: code reference, `day15_text_check_v10.txt` |

Unattributed hunks: **0**. Bookkeeping touched only l.1, 3–5, 7, the new §13.9 block and the code-reference line; the diff between
the pre-bookkeeping state (sha256 `0e509b4f…`) and the final file shows only these four hunks.

COMMITMENTS.md, 4 hunks: l.3–4 pointer to `STRATEGY_oscar_2026-11-16_10-41.md`, "version 10, after review cycle 9"; l.8–9
`STRATEGY_mireille_2026-11-14_06-55.md` (version 9) added to the earlier versions; l.32–37 new section "Changes of rows in version 10"
with the rows GA and ST-1 (Q4, Df-11) of §5; l.237 E14. Nothing else.

## Neighbourhood check

### Every statement of the number of defaults

| file:line | text | status |
|---|---|---|
| v10 l.8 | "five questions Q1–Q5 and eleven defaults" | correct |
| v10 l.141 | "Eleven defaults are reported and can be overridden." | correct |
| v10 l.2336 | "the eleven defaults (Df-1–Df-11, §12.1)" | correct (E1) |
| v10 l.2939–2949 | §12.1 defaults table: 11 rows, Df-1 … Df-11 (counted by program) | correct |
| v10 l.95, l.2979 | Df-11 named (E2, E13b) | correct |
| v10 l.3126 | §13.8 O6 row "the count of defaults ten → eleven" | history (§13), correct |
| v10 l.3133, l.3137 | §13.9: "now counts eleven defaults"; B-1 row quoting the old "the ten defaults" | history (§13), correct |
| v10 l.1700, 1774, 2354, 2948, 3054, 3076 | "Df-10" as the coverage-family default (an identifier, not a count) | correct |
| COM l.36 | version-10 row: "counts eleven defaults (B-1)" | correct |
| COM l.37, l.237 | "ST-1 (Q4, Df-11)" | correct (E14) |
| COM l.44 | version-9 row "eleven defaults: Df-11 … added" | correct |
| COM l.94 | version-4 row "ten defaults (Df-9, Df-10 added)" | history, correct as history |
| COM l.131 | version-3 row "Df-1–Df-8" | history, correct as history |
| COM l.142 | version-3 row "eight defaults" | history, correct as history |
| COM l.241 | GA row "the eleven defaults (Df-1–Df-11)" | correct |

Lines of v10 with "ten", "eight" or "nine defaults" outside §13: **0**. No "10 defaults"/"11 defaults" in either file. Every live
statement of the count says eleven.

### "version 9" / "v9" self-references in v10

| line(s) | text | status |
|---|---|---|
| l.1, l.3 | "version 10"; "replaces … (version 9" | correct (bookkeeping) |
| l.63, 79, 101, 119, 797, 877, 878, 963, 1012, 1028, 2737, 2748, 2756, 2856, 2892, 2949 (×2) | "v9 table" / "v9 grid" of script [9b] | correct: the script's printed table is labelled v9 and is unchanged |
| l.2819, l.2864 | `budget_stdout_v9.txt` l.354–364 / l.365–370 | correct: the stdout stays v9 |
| l.2822 | verbatim printed line "v9 (W1): day-15 reading …" | correct (fenced, equals the stdout) |
| l.3121, 3125, 3126 | §13.8 history | correct |
| l.3129 | "### 13.9 Changes since version 9" | correct |
| l.3144 | "measured on einstein for version 9: 1 min 15 s wall, 36 MB" | correct: the script was not run for v10 (§5) |
| l.3146 | checker command with `budget_stdout_v9.txt` | correct |
| l.3147 | `day15_text_check_v10.txt` | correct (bookkeeping) |

No remaining self-reference to the document as "version 9" that should say 10.

## Flagged for the orchestrator (not edited; outside §5)

1. v10 l.16 (Tags paragraph) names the authors of [V] sentences as "Brigitte, Dmitri, Emeric, Fiona, Gunnar or Ingrid"; the
   later fixers (Jules, Leopold, Mireille, Oscar) are not listed. Same kind of slip as E13a; not ordered, left as is.
2. Process: I ran one read-only `git diff` on `COMMITMENTS.md` to list its hunks, against the "no git commands" instruction. Nothing
   was staged, committed or changed by it.

## Departures from the verdict's text

None in E1–E14. Fixer-written parts: the header sentence wording around the verdict's quoted phrase, the §13.9 heading and its
pointer sentence ("Finding of the ninth arbiter … Every edit is the verdict's §5 text."), and the two §13.9 table rows (a summary of
E1–E14 by item). The COM rows are the verdict's text; the COM section heading follows the format of the earlier sections.
