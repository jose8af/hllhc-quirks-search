# Mechanical check of strategy addendum 1, version 5 — Dario, 2026-11-16 18:31 (`date`)

Object: was the third critical review (`ADDENDUM_1_v4_CRITICAL_REVIEW_bruno_2026-11-16_18-17.md`, "the review")
applied exactly to v4 (`STRATEGY_ADDENDUM_1_v4_zoe_2026-11-16_17-26.md`) to give v5
(`STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md`), with nothing else changed, and in COMMITMENTS.md ("COM") the
section "Changes of rows by addendum 1"? This is a mechanical gate: the content of the addendum is not reopened.
Method: my own scripts in `/var/tmp/jdochoa/dario/` (`spans.py`, `reapply.py`, `struct.py`, `hunkmap.py`,
`uniq.py`; pure Python, `nice -n 19 /usr/bin/python3 -I`, einstein, one at a time), `diff`, `cmp`, `sha256sum`. No
git command, no subagent, nothing on a worker. The fixer's scripts were not imported or run. Tags: [V] = I re-derived it
with the command named.

## Verdict: **PASS**

v5, with the C edits below applied without re-review, is the document that goes to the user. No A, no B.

| check | result |
|---|---|
| a. v4 → v5 hunks, exactness of the texts | **PASS** |
| b. sense check of the changed passages | **PASS with C-1 … C-5** (contradictions created by the application, each fixed by an exact text) |
| c. untouched files, hashes, numbers of §0 | **PASS** |
| d. COMMITMENTS.md | **PASS with C-6 … C-8** |
| e. item g against §0 | **PASS with C-9** (one line of item g is not in §0) |

## a. v4 → v5

**Independent re-application [V: `reapply.py`].** I took the 64 back-quoted strings of the review's Findings
section (review l.269-404) myself, whitespace-normalised, and applied the 29 instructions of B-1…B-4 and C-1…C-11 to
v4 as written: replace, "the same followed by" (append), or delete (B-2's [SD17] sentence), and then B-3's tail ("It
matters because the" → "It matters because" immediately before the new text). Each old text occurs exactly once in
v4 (29 × count = 1; tail count = 1). The result equals v5 with whitespace normalised, **character for character**,
once v5's header (l.1-3) is replaced by v4's l.1 and the appended section "Changes since version 4" (l.803-842) is
removed. So: every review item is applied in every place the review names, the new texts are word for word the
review's, and the only differences besides the items are the header and the bookkeeping table. Whitespace
differences are line breaks only: no markdown structure was lost (every removed v4 line that starts a list item,
table row or heading starts a line again in v5, except v4 l.1 (the replaced header) and the "*When.*" line whose
start is part of B-2's replaced text) [V: `struct.py`]; the only trailing space is at v5 l.317 (see below).

**Hunks [V: `diff -U0` v4 v5 → 27 hunks; `hunkmap.py` matches each hunk's v4 lines to the old texts].**

| hunk (v4 → v5 lines) | item | | hunk | item |
|---|---|---|---|---|
| 1 → 1-3 | header (bookkeeping) | | 15: 305-306 → 304-305 | B-2 (When: replacement + addition) |
| 2: 31 → 33 | B-3 | | 16: 309 → 308 | B-2 (Pre-declared reading) |
| 3: 34 → 36 | B-3 | | 17: 316-318 → 315 | B-2 (Effect robust) |
| 4: 38-39 → 40-41 | B-3 (both parts) | | 18: 320-323 → 317-318 | B-2 (deletion; Effect not robust) |
| 5: 50 → 52 | C-3 (41 → 40) | | 19: 486 → 481 | B-1 |
| 6: 54-55 → 56 | C-1 | | 20: 493-494 → 488 | C-7 |
| 7: 57 → 58 | C-2 | | 21: 500 → 494 | B-1 ((vi)) |
| 8: 76 → 77 | C-3 | | 22: 516 → 510 | C-8 |
| 9: 91 → 92 | C-11 | | 23: 619 → 613 | C-4 |
| 10: 100-101 → 101-102 | C-9; B-2 (D2) | | 24: 621 → 615 | C-4 |
| 11: 105 → 106 | B-4; C-10 | | 25: 765-766 → 759 | C-6 |
| 12: 108 → 109 | B-1 (D9) | | 26: 770 → 763 | B-4 |
| 13: 189-191 → 190 | C-5 | | 27: after 808 → 802-842 | "Changes since version 4" (bookkeeping) |
| 14: 282 → 281 | B-2 (What) | | | |

**Unattributed: 0.** The fixer's map (fix report l.53-81) is the same.

**Ambiguous instructions and their resolution.**
1. *C-12 row positions* (the review names no anchor): rows inserted in COM line order (C3 after C1-a; B2 after B1-g;
   B6-d after B6-a/B6-c). Consistent with the table's ordering; accepted.
2. *"C-13"* (review §f, "C3 (C-13)"): no such finding exists; the C3 row is C-12's third row, applied. Accepted.
3. *Trailing space at v5 l.317*: produced by the exact deletion in B-2; no rendering effect. No edit needed.
4. *B-3 tail* ("the words `It matters because the` before it become `It matters because`"): applied at the
   occurrence just before the new text (the only one) [V].
5. *Item g* has no place in the addendum and gives no text; the fixer did not apply it. Treated under check e.

## b. Sense check (each changed passage read in context in v5)

Read: §0.1 items 1-3, 5-7; §0.2 rows R08 and expected outcome; §0.3 D1, D2, D6, D9; §1.1 point 5; §1.5 entire;
§3 P6, P7; §4.3; §6; §7.1 points 1-2; and their neighbours. Contradictions created by the application:

- **The header's "no table number changed" is not true** [V: diff]: in §0.3, D6's factor changed (2 → 2.4 and
  2.7–3.4), D2 and D9 gained numbers; in §0.2, C-11 added "about 700" and "2.4×10⁸"; §0.1 item 5 changed 41 → 40.
  What holds is that no number of the §4 tables or of the script output changed. → **C-1.**
- **§1.1 l.147-150** still says the fractions are lower bounds "twice over", one reason being 0.97 % of particles
  without a Geant4 record, while §7.1 point 1 (C-6) now says the complete reference gives 25.2 % and 37.5 % and only
  the secondaries remain. Not a contradiction in numbers (the 25 % / 37 % are of "these runs" and "slightly higher"
  is true: 25.1 → 25.2, 37.3 → 37.5 [V: stdout [15] l.321, l.325; `LOG.md` l.679]) but the reader of §1.1 is not told
  the caveat is closed. → **C-2.**
- **§1.5 "Effect, not robust" (l.318-319)** still offers "the nuisance" while B-2 made the robust branch "a
  correction …, not a symmetric nuisance". → **C-3.**
- **§4.3 l.598-599 and §6 l.744-753** say the pile-up term is the present chain's estimate and Df-11 is unchanged;
  B-2's new text (l.315) lets the user choose with D2 that the binding reading use the corrected term ("stricter than
  the pinned Df-11"), and adds COM row B6-d. → **C-4, C-5.**
- **Header vs column label**: §0.2's last column is labelled "version 4" but now holds version-5 texts (C-3, C-11).
  Harmless for numbers; included in C-1 as a one-word fix.

Checked and not contradictory: B-3's "10 % its near-pass classes" (R04's near-pass classes, review: 10.5 %) and §1.3
l.227 "10 % … for R01" are different quantities; B-2's density wording vs the "Proposed:" sentence before it (the
addition fixes it); the trend threshold now 2σ in both bullets (l.311, l.318); D2 "before the freeze" vs §1.5 "by
day 15" (compatible); D9 vs P6 (vi) (same streams, same condition); 286 / 350 / 161 in §0.1 item 2 vs §1.3 l.236-238.

## c. Untouched files, hashes, numbers [V: `sha256sum`]

| file | sha256 | expected |
|---|---|---|
| `phase2_exploration/src/p2z_addendum1.py` | 5639c6a024bfe09ec56e8c709717b8531501deee11881cd6746f0d793708f6bd | 5639c6a0 ✓ |
| `phase1_strategy/outputs/addendum1_v4_stdout.txt` | 6b265bbf9b7e559ba7759002f65c964b285607a006eae72e1bb234d0b693fd52 | 6b265bbf ✓ |
| v4 | e4ff647a6d34909aa7c3330e50875edd8e200ba42df505b330731b7337a0f09f (= fixer's `v4_copy.md`) | e4ff647a ✓ |
| v5 | 00df2c65a9018f4e203e49b3f0b8bb5a57b75c0d108c88601900cb6c1709923a | 00df2c65…709923a ✓ |
| COM now | 460787fcd7cdcdf2c3a64e32eacf75acd1eaa279ff99a90f6f82619f6a933529 | fixer's 31eae02f… plus the orchestrator's two edits (d) |
| COM before (fixer's copy) | de819209a7a81f539a88d2de6a7897dfd7951e354384e3a2361c3876f06d7f1c | = `sha_before.txt` ✓ |

Spot check of 15 numbers in v5 §0 against the stdout (all agree) [V: read of `addendum1_v4_stdout.txt`]:
(1) pilot 142 CPU-h, (2) 167 GB, (3) part 1 95 CPU-h / 80 GB, (4) B1 part 47 CPU-h — [8] l.190-191;
(5) end 19 Nov 15:45, margin 32 h — l.193 (15:46); (6) toys 47 / 108 / 228 — [11] l.238-240; (7) total 4,663 /
4,723 / 4,844 — l.245; (8) old 7,710–18,246 as printed in v3 — l.244; (9) pool 201 / 121 — [9] l.211, l.214;
(10) reach 514 [445], 584 [514], 790 [712] — [10] l.220, l.224, l.228; (11) empty pilot 161 and 238 / 262 / 284,
frozen 76 and 156 / 181 / 204 — [13] l.268; (12) ×1.25: 256 / 283 / 308, ×1.5: 273 / 303 / 329 — [17] l.356-357;
(13) looper zero 2.2×10⁴ (2.16e4) and hard-scatter reading 286 — [16] l.336-337; (14) test 22–28 CPU-h — [17]
l.349; (15) 25 % / 37 % and 34–58 % TBPS — [15] l.321-326 (25.1 %, 37.3 %; TBPS 34–42 and 53–58). Also: "about 700"
= 717 ([12] l.263); 1,094–1,984 and 4,960–8,996 ([9] l.215); +45 / +109 ([8] l.198). Note, not a finding: §0.1
item 4 (untouched v4 text) has "70–125" decays-in-flight counts under "about", the stdout 74–125.

## d. COMMITMENTS.md [V: `cmp`, `diff` against `/var/tmp/jdochoa/clara/COMMITMENTS_before.md`]

- Above the section heading (l.286, first 48,675 bytes): `cmp -n 48675` no difference; sha256 of that prefix
  508bc8e4… in both.
- Inside the section, `diff` gives four hunks, all accounted for:
  1. l.288-289 → 288-290: pointer to v5 (fixer), then reworded by the orchestrator to "Version 5: … the label
     "ADD4" in the rows below means this addendum in its current version". Consistent and resolves the fixer's flag 1.
  2. l.302 → 303-304: C-12 row C3 inserted; C-1's COM part (B1-a "missed the fault" → "understated the fault and
     would have passed the time cut"). Verbatim with the review [V: `uniq.py`, count 1; old text gone].
  3. after 308 → 311: C-12 row B2-a/b/c, verbatim.
  4. l.310 → 313-314: B6-a/B6-c row edited by the orchestrator ("effect within ln 2 → if r(R06) > 1 the pile-up
     estimate is multiplied by r(R06) with the widths of ADD4 §1.5, no credit for r < 1 (a one-sided correction, not
     a symmetric nuisance; third review B-2)"); C-12 row B6-d inserted verbatim.
- **Orchestrator's edits judged.** The pointer is right. The B6 edit agrees with v5 §1.5 l.315 and with the review's
  ruling on design point 2 (one-sided, measured widths, source-defined); the user's sub-choice (binding or beside)
  reaches COM through B6-d's "by the reading of ADD4 §1.5". Left inconsistent in the same row: "the user chooses
  between the nuisance and a chain fix" (→ C-6).
- **Other rows against v5.** ST-1 (l.319) says "the pile-up term is the present chain's estimate" without the D2
  choice (→ C-7, same as C-4). B1-a's release condition (l.304) lacks the NI condition of v5 D9 / P6 (vi) (→ C-8).
  Checked and consistent: [L15] row (25 % / 37 % are lower bounds), B1-e (C-10's withdrawal), B1-f and INV-1
  (Geant4-gun looper overlays, C-9), B4-c, T1-i, ST-1 numbers (161; 238 / 262 / 284; 308 / 303; 142; 15:45).

## e. Item g against v5 §0

| item g line | in v5 §0? |
|---|---|
| 1 half-turn, 25 % / 37 %, 34–58 % | §0.1 item 1 ✓ |
| 2 option B, zero, 2.2×10⁴ / 286 / ≈ 350, [L15] not a term | §0.1 items 1-2 ✓ |
| 3 looper + pile-up untested; D2 22–28; binding sub-choice | §0.1 item 3, D2 ✓ |
| 4 D1, C3 item, overlays | D1 ✓ |
| 5 rule numbers, pause expected | §0.1 item 4 ✓ |
| 6 D4, D5, 24 events | D4, D5 ✓ |
| 7 D6, factor up to about 3, B1-e withdrawn | D6 ✓ |
| 8 D3, D9, code not finished, slow fragment, NI streams wait, β cut back to the user | D3, §0.1 item 7, D9 ✓ |
| 9 D7, 201 / 121, not 36–42, reach | §0.1 item 8, D7 ✓ |
| 10 D8 | D8, §0.1 item 3 ✓ |
| 11 costs, D10 | §0.1 item 7, D10 ✓ |
| 12 quirk hits not truncated; effect through the other hits not measured before the verdicts | **absent from §0** (only §1.1 point 5) → C-9 |

## Findings

No A. No B.

### C (exact old → new; each old text occurs exactly once [V: `uniq.py`])

- **C-1** v5 l.3, old: `applied as exact text; no table number changed.` → new: `applied as exact text; no number
  of the §4 tables or of the script output changed; text cells of §0.2 and §0.3 did (D6's factor is now 2.4 for one
  population and 2.7–3.4 for the three), and §0.1 item 5 now reads 40, not 41.` And v5 l.72, old: `| quantity |
  frozen at Gate A | version 3 | **version 4** |` → new: `| quantity | frozen at Gate A | version 3 | **version 5** |`
- **C-2** v5 l.150, old: `fractions are slightly higher.` → new: `fractions are slightly higher. With the complete
  Geant4 reference (p2-c-pa-htg, LOG.md 18:15) they are 25.2 % and 37.5 %; only the first reason remains (§7.1
  point 1).`
- **C-3** v5 l.319, old: `choose between the nuisance and fixing the chain` → new: `choose between the correction of
  the robust case and fixing the chain`
- **C-4** v5 l.599, old: `term is the present chain's estimate; [L15] is not a term of the rule.` → new: `term is the
  present chain's estimate, or that estimate corrected by the robustness test if D2 is accepted, it shows an increase
  and the user chooses that it enter the binding reading (§1.5); [L15] is not a term of the rule.`
- **C-5** v5 l.744, old: `the definition of rule 1 (Df-11)` → new: `the definition of rule 1 (Df-11; its pile-up term
  only as chosen with D2)`. And v5 l.753, old: `eighth row of the B6 table (COM B6-a, B6-c).` → new: `eighth row of the
  B6 table (COM B6-a, B6-c, B6-d) and, if the user so chooses with D2, its correction of the pile-up term in the
  binding day-15 reading (§1.5).`
- **C-6** COM l.313, old: `the user chooses between the nuisance and a chain fix` → new: `the user chooses between
  the correction and a chain fix`
- **C-7** COM l.319, old: `the pile-up term is the present chain's estimate)` → new: `the pile-up term is the present
  chain's estimate, or, if the user so chooses with ADD4 D2, that estimate corrected by B6-d)`
- **C-8** COM l.304, old: `(it reads false for parents that have turned) |` → new: `(it reads false for parents that
  have turned); the streams with nuclear interactions only after the slow-fragment residue of ADD4 §3 P6 (vi) is
  settled (a change of the β cut 0.1 goes to the user) |`
- **C-9** v5 l.66, old: `against 790 [712] [9], [10].` → new: `against 790 [712] [9], [10].` followed by a new line
  `9. **The signal's own hits are not truncated** (§1.1 point 5): quirk hits are injected without the fast
  simulation, and the Stage-3 propagator has no turn limit (read in the code by the third reviewer). The effect of the
  missing arcs of the other particles of a signal event and of its pile-up on the signal efficiency is not measured
  before the closure verdicts.`

Line breaks inside the quoted texts above are wrapping only (as in the review's convention); each old text is one
line in its file.

## Not checked

The content of the addendum (out of scope); the review's own numbers beyond the 15 spot checks; the per-test values
of stdout [5].
