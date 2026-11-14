# Fix report, review cycle 8 (fixer Mireille, 2026-11-14 06:55)

Verdict: `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md` (ITERATE; 0 A, 1 B = W1). Scope: §3–§5 of the verdict and nothing else.
Artifacts: `outputs/STRATEGY_mireille_2026-11-14_06-55.md` (v9), `src/strategy_budget.py`, `src/check_day15_text.py` (new),
`outputs/budget_stdout_v9.txt`, `outputs/day15_text_check_v9.txt`, `../COMMITMENTS.md`. v8 not modified.

Method: every code block and every old/new text was copied out of the verdict file by a program (line ranges of the verdict's
fenced blocks; each fence asserted), each "old" string asserted to occur exactly once in v8. No hand-typed code or replacement text
except the bookkeeping the verdict leaves to the fixer (header, §13.8 rows, code-reference runtime, COM pointer).

## Status per item

| item | status | where (section heading) | grep phrase |
|---|---|---|---|
| W1 (B), script §3.1 (a) block A | RESOLVED | `src/strategy_budget.py` | `# v9 (W1, verdict cycle 8)` |
| W1, §3.1 (b) label of l.964 | RESOLVED | script, v5 (R1) line | `is at the limit at 12 pilot counts: v9 table` |
| W1, §3.1 (c) block B self-test | RESOLVED | script | `def d15_test` |
| W1, §4.2 text check | RESOLVED | `src/check_day15_text.py` (equals verdict l.480–627 byte for byte, `cmp`) | `Text check of the day-15 family` |
| T1 | RESOLVED | §0 item 3 | `row of the v9 table of script [9b])` |
| T2 | RESOLVED | §0 "Expected" (β) | `reads it as (γ), through the Z(νν) pilot count` |
| T3 | RESOLVED | §0 "The pause." | `One Z(νν) pilot count is 18 events` |
| T4 | RESOLVED | §0 leading sentence | `projected B₅₀ ≈ 3×10⁴–3×10⁵` |
| T5 | RESOLVED | §4.4 point 4 | `far above the day-15 limit (≈ 12 Z(νν) pilot counts` |
| T6 | RESOLVED | §4.4 point 5 | `of 21 events for all SM hard-scatter processes` |
| T7 | RESOLVED | §4.4 Table 4.4c caption | `computed on the pilot's exposures, not on these pool floors` |
| T8 | RESOLVED | §4.4 scenarios (β) and (γ) | `reads every SM process through the Z(νν) pilot count, as in (γ)` |
| T9 | RESOLVED | §4.4 what is not known | `at day 15, ≈ 12 Z(νν) pilot counts with the other pilot counts at zero` |
| T10 (rule-1 clarification, ambiguity 1) | RESOLVED | §11.7 rule 1 | `from the samples that exist at day 15,` |
| T11 | RESOLVED | §11.7 rule 1 | `5.9×10³ events after CKF by` |
| T12 (ambiguity 2) | RESOLVED | §11.7 rule 1 | `These factors multiply a counted term, never its zero-count floor.` |
| T13 | RESOLVED | §11.7 rule 1 | `the limit is at ≈ 12` |
| T14 | RESOLVED | §12.1 Q2 stem (digest table, caption, verbatim block l.354–364) | `a digest of the printed lines below` |
| T15 | RESOLVED | §12.1 Q2 upside | `Z(νν)-count and zero-count rows` |
| T16 | RESOLVED | §12.1 Q2 option (c) (bar, caption, verbatim grid l.365–370) | `at least ×44 (97.7 %) [×30]` |
| T17 | RESOLVED | §12.1 Q2 rider (1) | `day-7 reading is expected at ≈ 3×10⁴–3×10⁵` |
| T18 (critical C-7) | RESOLVED | §12.5 point 2 | `(Table 4.4c, (α1); after CKF, as v1 counted them)` |
| critical C-5 (docstring) | RESOLVED | script l.2–4 | `STRATEGY (current version: see COMMITMENTS.md)`, `about 75 seconds` |
| physics C-1/critical C-6, physics C-2, C-3, C-4, constructive C-2 | RESOLVED (contained in block A, T3, T10, T14, T16, as §6.4 states) | as listed | `decays in flight alone: B50 ≈ 545`; `88–148 at an R08 selection` |
| bookkeeping: header | RESOLVED | header | `version 9`; `for verification (cycle 9)` |
| bookkeeping: §13.8 (verdict sentence verbatim, W1 row, C row) | RESOLVED | §13.8 Changes since version 8 | `Rule 1 of §11.7 is made single-valued` |
| bookkeeping: code reference | RESOLVED | Code reference | `measured on einstein for version 9: 1 min 15 s wall, 36 MB`; `check_day15_text.py` |
| bookkeeping: COM | RESOLVED | COMMITMENTS.md header; "Changes of rows in version 9" | `STRATEGY_mireille_2026-11-14_06-55.md`; `§11.7 rule 1 made single-valued (W1)` |

## Script output

- Runs: 1 min 14.6 s (first, saved), 1 min 15.5 s and 35,676 kB max RSS (second, `/usr/bin/time -v`), `nice -n 19 python3 -I`, sequential.
- `budget_stdout_v9.txt`: 582 lines; sha256 `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d`.
  Expected (verdict §3.2): `0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d`. **Equal**; the second run gives the same hash.
- `diff budget_stdout_v8.txt budget_stdout_v9.txt`: exactly two hunks, `354,376c354,370` and `396c390,399`, as the verdict states.
  Classification: 354,376c354,370 = the two tables (v8 day-15 table and grid → v9 lines 354–370; equal to verdict §2.1 l.141–157, `cmp`);
  396c390,399 = the label line of (b) (new l.390) plus the nine self-test lines (391–399; equal to verdict l.434–443, `cmp`).
  Anything else: **nothing**. `cmp` of v8 lines 1–353, 377–395, 397–579 against v9 lines 1–353, 371–389, 400–582: identical.
- Script diff against v8 (`diff` hunks): `2c2`, `4c4` (docstring, C-5); `853,888c853,906`, `890c908`, `893c911`, `897,899c915,957`,
  `901,905c959,967` (v8 l.853–905 → block A; the split is `diff`'s alignment; verified block A equals verdict l.225–339 and the code between
  it and l.964 is unchanged); `964c1026,1092` (label (b) + block B, equals verdict l.349–414). Nothing else.

Self-test lines (stdout v9 l.391–399):

```
  v9 self-test 1: PASS: basis = pilot exposures (DIF, NI: N_t / 1e6; all SM + multijets: (sum N_t + N_MJ) / 2.3e6); no pool transfer factor used [kappa 65.13 / 0.88 / 1.12 / 1.12 / 18.13]
  v9 self-test 2: PASS: key cells equal pmf_pred(raw inputs, (PU9,), nd = D15_ND) [empty: 76.4; m_Z = 12: 299.6; m_D = 4: 331.0]
  v9 self-test 3: PASS: key cells within 2 % of an independent 100,000-draw median (seed 11) [empty: 76.3; m_Z = 11: 281.3; m_Z = 12: 299.8; m_Z = 13: 318.0; m_D = 3: 268.7; m_D = 4: 333.3]
  v9 self-test 4: PASS: B50 rises with the Z(nunu) count (0-21) and with the DIF count (0-6)
  v9 self-test 5: PASS: threshold: Z(nunu) count 11 below (<= 297), 12 at the limit (297-303), 13 above (> 303); DIF count 3 below, 4 above [281.1 / 299.6 / 317.3; 265.9 / 331.0]
  v9 self-test 6: PASS: own-hit rows = after-CKF level x 1/(1 - eps_pair) on top of the empty reading (no S_CKF, no conditional); Z(nunu) conversions = EV_GZ [(alpha1') at 0.8: 3.158e+04; smallest own-hit cell 2555, above 300]
  v9 self-test 7: PASS: grid, independent draw: each of the 24 cells passes at 1.1 x its printed factor and fails at the factor / 1.1; 'none suffices' only where B50 > 300 with the conversions removed [24 of 24]
  v9 self-test 8: PASS: grid: the factor does not fall with f_D, nor from the pilot's own rate to 0.255 to 0.379
  v9 self-test: ALL PASS (8 of 8)
```

## Text check (`python3 -I phase1_strategy/src/check_day15_text.py <v9> phase1_strategy/outputs/budget_stdout_v9.txt`)

Summary: **ALL OK (45 of 45)** on the first run on the final v9 (also ALL OK before the bookkeeping). No text correction was needed.
Full output (also `outputs/day15_text_check_v9.txt`):

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

## Diff of the strategy v8 → v9

`diff STRATEGY_leopold_2026-11-14_05-00.md STRATEGY_mireille_2026-11-14_06-55.md` (after O6): 33 hunks (3,114 → 3,136 lines).

| hunk | item |
|---|---|
| 1c1, 3,5c3,5 | bookkeeping: header |
| 7,8c7,8 | bookkeeping: header status (l.7) and O6: "ten defaults" → "eleven defaults" (l.8) |
| 63c63 | T1 |
| 79c79 | T2 |
| 91,99c91,101 | T3 |
| 115c117 | T4 |
| 139c141 | O6: §0 "Ten defaults" → "Eleven defaults" |
| 795c797 | T5 |
| 876c878 | T6 |
| 961c963 | T7 |
| 1010c1012 | T8 |
| 1025,1026c1027,1028 | T9 |
| 2728,2730c2730,2738 | T10 |
| 2738,2739c2746,2748 | T11 |
| 2744c2753 | T12 |
| 2746,2747c2755,2756 | T13 |
| 2797,2799c2806,2808; 2801c2810; 2803,2808c2812,2817; 2810c2819; 2813,2828c2822,2832 | T14 (one span, split by `diff`) |
| 2835c2839 | T15 |
| 2851,2856c2855,2862; 2858,2863c2864,2872; 2866,2872c2875,2880; 2877c2885 | T16 (one span, split by `diff`) |
| 2884c2892 | T17 |
| 2940a2949 | O6: row Df-11 in §12.1 "Defaults the user can override" |
| 2995c3004 | T18 |
| 3107a3117,3128 | bookkeeping: §13.8 (including the O6 row) |
| 3112c3133; 3113a3135,3136 | bookkeeping: code reference (runtime; check_day15_text.py line) |

Unattributed hunks: **0**. Each T-item was applied at the v8 line the verdict names (printed by the applying program).

COMMITMENTS.md diff: pointer to v9 (l.3–4), v8 added to the list of earlier versions (l.7–8), new section "Changes of rows in version 9"
with the verdict's TG-1 row (l.30–35); O6: a GA row in that section (l.36) and "ten defaults (Df-1–Df-10)" → "eleven defaults (Df-1–Df-11)" in the GA row (l.233). Nothing else.

## O6 (orchestrator-ordered, beyond the verdict's §3–§5)

Ordered by the orchestrator after the first hand-back: the strategy's own Gate-A section shows the pinned reading of rule 1.
RESOLVED: §12.1 "Defaults the user can override", new row Df-11 (grep `Df-11 (technical; pinned in review cycle 8)`). The reading is worded
from the T10/T12 sentences of §11.7 rule 1; the consequence cites the Z(νν)-count row of the v9 table (no number restated); the alternative
is "alternative readings: see the cycle-8 arbiter verdict §1", because the verdict does not say that a pool floor makes the rule stricter
(its §1.2 shows the pool-floor reading (i) is the more lenient one). Defaults count updated in: v9 header l.8, v9 §0 l.141, COM GA row
l.233 (the historical COM row l.85 "ten defaults (Df-9, Df-10 added)" left as history); §13.8 row and COM version-9 row added. Script and
its output untouched. Text check rerun: ALL OK (45 of 45); `day15_text_check_v9.txt` overwritten (its content is unchanged: the new row
contains no checked statement). The full output above is the rerun's.

## Departures from the verdict's text

None in code, text replacements, the §13.8 sentence or the COM row. Fixer-written parts (the verdict leaves their wording to the fixer):
the header sentence ("finding W1 and the C items it marks applied now"); the §13.8 intro sentence and the two table rows; the code-reference
runtime (my measurement, 1 min 15 s, 36 MB, equal to the verdict's) and the one-line description of `check_day15_text.py`.

## Neighbourhood check

The text check's (C) scanners and (D) stale list cover the family over the whole live text (outside §13 and fences): no residual. Table
4.4c and the stdout lines "v6 (T2)", "v7 (U1)" and "class limit of decision point 2" untouched, as ordered. No budget figure, default,
acceptance criterion, sample size or expected-outcome number changed (stdout byte-identical outside the two tables).

## Not done, proposed (not applied)

- The Gate-A package corrections (verdict §7) are not in §3–§5: they are the cycle-9 constructive reviewer's task. The pinned reading of
  rule 1 enters the strategy only through T10/T12 (rule text) and §13.8; the presentation to the human as an overridable default is left
  to that package.
