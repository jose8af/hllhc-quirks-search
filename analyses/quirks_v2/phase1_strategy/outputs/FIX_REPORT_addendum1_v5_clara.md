# Fix report — strategy addendum 1, version 4 → version 5 (fixer: Clara, 2026-11-16 18:21, `date`)

Task: apply the exact replacement texts of the third critical review
(`phase1_strategy/review/critical/ADDENDUM_1_v4_CRITICAL_REVIEW_bruno_2026-11-16_18-17.md`, verdict ITERATE, 0 A, 4 B,
12 C) to version 4. Nothing else changed.
Result: `STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` ("v5"). v4 unchanged. COMMITMENTS.md: only the section
"Changes of rows by addendum 1" changed. Script and stdout not touched, not re-run. No git command, no subagent, no
job, nothing on a worker. Scratch `/var/tmp/jdochoa/clara/` (`apply.py`, `hunks.py`, `apply_log.json`, `hunks.out`,
copies `v4_copy.md`, `COMMITMENTS_before.md`, `sha_before.txt`). Session log `logs/fixer_clara_2026-11-16_18-21.md`.

## Method

`apply.py` (pure Python, einstein, `nice -n 19`, `/usr/bin/python3 -I`). For each item, old text → new text, or
"the same followed by" text added after the old text, or deletion. The review says "line breaks inside quoted old text
are to be ignored", so old texts are matched with any whitespace run equal to any other. Each old text must occur
**exactly once** in v4 (COM: in the addendum section) or the item is not applied. The new text is inserted as one
line, with whitespace runs made single spaces. As a guard against copying mistakes, every old and new string is also
checked to appear verbatim in the review file (whitespace-normalised); the run stops if one does not. All passed.
One run was restarted from the copies: the first run's change table had labels with `|` in them (row labels only,
same text otherwise). COM was restored from the copy and its sha256 rechecked (de819209…) before the rerun.

## Items: applied / not applied

**All 16 items applied (B-1…B-4, C-1…C-12); 0 not applied.** Every old text occurred exactly once.

| item | places (v5 line) | mode |
|---|---|---|
| B-1 | §3 P6 paragraph after the option-(a) table (l.481); §3 P6 (v) → new (vi) (l.494); §0.3 D9 (l.109) | 3 replacements |
| B-2 | §1.5 What (l.281, addition); Pre-declared reading (l.308, addition); Effect robust (l.315, replacement); sentence "Whether a measured two-simulation difference … next bullet." deleted (l.317); Effect not robust (l.318); When (l.304 replacement, l.305 addition); §0.3 D2 (l.102) | 8 edits |
| B-3 | §0.1 item 1 (l.33); item 2 (l.36); item 3 (l.40-41: main replacement, then "It matters because the" → "It matters because") | 4 replacements |
| B-4 | §0.3 D6 (l.106); §7.1 point 2 (l.763) | 2 |
| C-1 | §0.1 item 6 (l.56); COM B1-a | 2 |
| C-2 | §0.1 item 7 (l.58) | 1 |
| C-3 | §0.2 R08 row (l.77); §0.1 item 5, 41 → 40 (l.52) | 2 |
| C-4 | §4.3 superseded list (l.613, l.615) | 2 |
| C-5 | §1.1 point 5 (l.190) | 1 |
| C-6 | §7.1 point 1 (l.759) | 1 |
| C-7 | §3 P6 (ii) (l.488, addition) | 1 |
| C-8 | §3 P7 (l.510) | 1 |
| C-9 | §0.3 D1 (l.101) | 1 |
| C-10 | §0.3 D6 (l.106) | 1 |
| C-11 | §0.2 expected-outcome row (l.92) | 1 |
| C-12 | COM: three rows | 3 insertions |

Not part of the B/C lists and so not applied: the review's "Item g" (12 lines for the user). It is a summary for the
orchestrator and gives no place in the addendum.

## Hunk → item map, `diff -U0` v4 → v5: 27 hunks, 27 attributed, 0 unattributed

Attribution by `hunks.py`: each item's new text is found again in v5 (exactly once). Its line span must overlap the
hunk's v5 range.

| hunk | v4 lines | v5 lines | item(s) |
|---|---|---|---|
| 1 | 1 | 1-3 | header (version 5) |
| 2 | 31 | 33 | B-3 (§0.1 item 1) |
| 3 | 34 | 36 | B-3 (§0.1 item 2) |
| 4 | 38-39 | 40-41 | B-3 (§0.1 item 3, both parts) |
| 5 | 50 | 52 | C-3 (§0.1 item 5) |
| 6 | 54-55 | 56 | C-1 (§0.1 item 6) |
| 7 | 57 | 58 | C-2 (§0.1 item 7) |
| 8 | 76 | 77 | C-3 (§0.2 row R08) |
| 9 | 91 | 92 | C-11 (§0.2 expected-outcome row) |
| 10 | 100-101 | 101-102 | C-9 (§0.3 D1); B-2 (§0.3 D2) |
| 11 | 105 | 106 | B-4 (§0.3 D6); C-10 (§0.3 D6) |
| 12 | 108 | 109 | B-1 (§0.3 D9) |
| 13 | 189-191 | 190 | C-5 (§1.1 point 5) |
| 14 | 282 | 281 | B-2 (§1.5 What) |
| 15 | 305-306 | 304-305 | B-2 (§1.5 When, two edits) |
| 16 | 309 | 308 | B-2 (§1.5 Pre-declared reading) |
| 17 | 316-318 | 315 | B-2 (§1.5 Effect robust) |
| 18 | 320-323 | 317-318 | B-2 (deletion of the [SD17] sentence); B-2 (§1.5 Effect not robust) |
| 19 | 486 | 481 | B-1 (§3 P6, paragraph after the option-(a) table) |
| 20 | 493-494 | 488 | C-7 (§3 P6 (ii)) |
| 21 | 500 | 494 | B-1 (§3 P6 (v) → (vi)) |
| 22 | 516 | 510 | C-8 (§3 P7) |
| 23 | 619 | 613 | C-4 (§4.3, first part) |
| 24 | 621 | 615 | C-4 (§4.3, second part) |
| 25 | 765-766 | 759 | C-6 (§7.1 point 1) |
| 26 | 770 | 763 | B-4 (§7.1 point 2) |
| 27 | after 808 | 802-842 | table "Changes since version 4" |

## Hunk → item map, COMMITMENTS.md: 4 hunks, 4 attributed, 0 unattributed

Lines 1-285 (48,675 bytes, everything above the section heading at l.286) are byte-identical: `cmp -n 48675` against
the copy taken first, no difference.

| hunk | before | after | item(s) |
|---|---|---|---|
| 1 | 288 | 288 | pointer v4 → v5 (orchestrator's instruction): the addendum path in the section's first sentence |
| 2 | 302 | 302-303 | C-12 (row C3 (l.176) inserted); C-1 COM part (B1-a: "missed the fault" → "understated the fault and would have passed the time cut") |
| 3 | after 308 | 310 | C-12 (row B2-a, B2-b, B2-c (l.184-186) inserted) |
| 4 | after 310 | 313 | C-12 (row B6-d (l.206, Df-7) inserted) |

## sha256

| file | before | after |
|---|---|---|
| v4 `STRATEGY_ADDENDUM_1_v4_zoe_2026-11-16_17-26.md` | e4ff647a6d34909aa7c3330e50875edd8e200ba42df505b330731b7337a0f09f | the same |
| v5 `STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` | — | 00df2c65a9018f4e203e49b3f0b8bb5a57b75c0d108c88601900cb6c1709923a |
| `phase2_exploration/src/p2z_addendum1.py` | 5639c6a024bfe09ec56e8c709717b8531501deee11881cd6746f0d793708f6bd | the same |
| `phase1_strategy/outputs/addendum1_v4_stdout.txt` | 6b265bbf9b7e559ba7759002f65c964b285607a006eae72e1bb234d0b693fd52 | the same |
| `COMMITMENTS.md` | de819209a7a81f539a88d2de6a7897dfd7951e354384e3a2361c3876f06d7f1c | 31eae02f8e182b58dba761aca4ca227ba36869c7f28f82b193aaf90c1b5f749b |

## Neighbourhood check (C-6): other occurrences of "25 %", "37 %", "≥ 25", "≥ 37" in v5, all unchanged

C-6 was applied only at §7.1 point 1 (v5 l.759), as the review says. Other occurrences:

| v5 line | place | text | which quantity |
|---|---|---|---|
| 28-29 | §0.1 item 1 | "at least 25 % of the hits of a Z(νν) event and 37 % of the hits of a pile-up interaction" | half-turn fraction (lower bound) |
| 74 | §0.2 row "does the simulation follow curling particles?" | "≥ 25 % of the written hits (Z(νν)), ≥ 37 % (minimum bias)" | half-turn fraction |
| 140 | §1.1 table | "209 = 25 % of the written hits", "91.0 = 37 % of the written hits" | half-turn fraction (incomplete reference) |
| 254-255 | §1.4 [L15] draft text | "at least 25 % … at least 37 % in a minimum-bias interaction" | half-turn fraction |
| 176 | §1.1 point 2 | "37 % of the Fatras hits per interaction" | half-turn fraction |
| 101 | §0.3 D1 | "hits + 25–37 %" | half-turn fraction (range) |
| 42 | §0.1 item 3 | "were 25 % higher" | pile-up shift (not the fraction) |
| 77 | §0.2 R08 row | "if pile-up is 25 % above" | pile-up shift |
| 552 | §4.1 closing paragraph | "a pile-up estimate 25 % higher" | pile-up shift |
| 281 | §1.5 (B-2 text) | "about 37 % more hits" | chain-stage hit increase (review text) |
| 447 | §3 P6 table | "47 (0.25 %)" | regex hit only, unrelated |

Related, found with these and also unchanged: v5 l.147-150 (§1.1, "lower bounds, twice over: … 0.97 % of the low-p_T
particles had no Geant4 record …"). The review says the "1 % without a record" caveat is closed by the complete
reference (section b). Only §7.1 point 1 was edited, as instructed. COMMITMENTS.md, unchanged: l.300 ([L15] row,
"at least 25 % … 37 %") and l.318 (ST-1, "25 % (50 %) higher": pile-up shift).

## Flags (no action taken)

1. **COM pointer sentence.** It now reads "Version 4, drafted 2026-11-16 by Zoe from `…v5_clara…md` ("ADD4"; fix
   report `FIX_REPORT_addendum1_v4_zoe.md`)". Only the path was changed, as instructed. The label "ADD4" was kept
   because the review's C-12 rows cite "ADD4 §1.1 point 2", "ADD4 §1.5" and "ADD4 D1 (a)". Those sections are the same
   in v5. "Version 4 … by Zoe" and the fix-report pointer are now stale. The orchestrator should decide on the wording.
2. **C-12 row position.** The review says "three rows to add to the section" and names no row to insert them after.
   The table is ordered by the line of COMMITMENTS.md, so each row was inserted after the row with the next lower line
   (C3 l.176 after C1-a l.168; B2 l.184-186 after B1-g l.183; B6-d l.206 after B6-a/B6-c l.203/205). The text of the
   rows is verbatim. This was a placement choice; it is flagged.
3. **COM B6-a/B6-c row (l.312 after)** still says "effect within ln 2 → carried by the pile-up estimate as a nuisance
   of the measured size". This contradicts B-2 (v5 §1.5 now has a one-sided correction). The review gives no COM text
   for that row, so it is unchanged.
4. **Header wording "no table number changed"** (the orchestrator's words) holds for the §4 tables and the script
   output. Text cells of the §0.2 and §0.3 tables do change (C-3, C-11, B-4, C-9, C-10, B-1, B-2), and §0.1 item 5
   changes 41 → 40 (C-3).
5. **Trailing space** at v5 l.317, left by the exact deletion in B-2 ("… at R08 [E; 17]. ").
6. **Long lines.** Each replaced passage is one line in v5. The surrounding text keeps v4's wrapping. Markdown
   rendering is unaffected.
7. The review mentions "C-13" (section f, "C3 (C-13)"). No C-13 exists in its findings. The C3 row is C-12's third
   row, which was applied.
8. Rule note: one short helper (a string edit of my own `apply.py` labels) ran as `python3` without `nice`. It took
   under a second and touched only the scratch directory.
