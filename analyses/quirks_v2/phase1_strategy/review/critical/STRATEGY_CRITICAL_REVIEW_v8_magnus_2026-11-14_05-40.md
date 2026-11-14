# Critical review: Phase 1 STRATEGY v8 (quirks v2), review cycle 8

Reviewer: Magnus (critical), 2026-11-14 05:40. Fresh session. Role: `agents/critical_reviewer.md` (adversarial,
show your work, A/B/C).
Artifact: `phase1_strategy/outputs/STRATEGY_leopold_2026-11-14_05-00.md` ("v8"; "l." = a line of v8 unless marked),
`COMMITMENTS.md` ("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v8.txt`
("stdout v8"), `outputs/budget_stdout_v7.txt`.
Against: cycle-7 verdict `review/arbiter/STRATEGY_ARBITER_v7_lena_2026-11-14_04-30.md` ("AV7"), v7
`STRATEGY_jules_2026-11-14_03-40.md`, fix report `outputs/FIX_REPORT_cycle7_leopold.md` ("FR", claims, not evidence),
`LOG.md` 05:40 entry.
Scope (AV7 §11): verify the ordered changes; complete diff check; script; greps; my own sweep of the V1 family.
I did not re-review the design.
Computation: einstein, `nice -n 10 python3 -I`. The script was run once in my scratchpad, and one scratch script loaded
it with `runpy` (stdout suppressed) and called its own functions without modifying it (118 s, 36.5 MB). No git write,
no sub-agent, no pixi. Read-only git: `git diff HEAD~1` on COM and the script.

**Result: Category A: none. Category B: one (W1, a basis caption of the (c) grid that the fix wrote and that
contradicts the grid's own code and S17). Category C: eight.** Everything AV7 ordered is present and exact. The two
tables are byte-identical to stdout. The script is byte-identical to the ordered code. There are 32 hunks and none is
unattributed.

---

## 1. Script (task 1)

| check | evidence | result |
|---|---|---|
| inserted block = AV7 §4 item S code | I extracted AV7 l.231–283 and script l.853–905 and ran `diff` on them: empty (53 lines each) | **identical**, line by line: same functions (`_b50`, `_cls`, `_need`), same inputs (`PIL_N`, `K_PIL`, `kap_d15`, `kap_nodif`, `ALPHA`, `pmf_cache`, `U1_II`, `G_A1P`, `F_GAM`), same rows. No new physics input. |
| placement | it comes after the second `v7 (U1)` print (old l.852; unchanged in v8 at l.852) | as ordered |
| S20 f-string | `git diff HEAD~1`: only `(day-15 class limit m_H = 125)` → `(day-15 class limit: m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)` | as ordered |
| other script lines | `git diff HEAD~1 -- …/strategy_budget.py`: two hunks (`@@ -850,6 +850,59 @@`, `@@ -908,7 +961,7 @@`) | nothing else changed |
| rerun | my run: 1:30.39 wall, 35,192 kB max RSS; sha256 `dd55e38f…3f14` for both my output and `budget_stdout_v8.txt`; `cmp` silent | **byte-identical** |
| stdout v7 → v8 | `diff`: `353a354,376` (23 added lines) and `373c396` (the S20 line only) | only the additions plus the one relabelled line |
| headline figures | stdout v8 l.123 "4609.4 CPU-h; … 1.3 x 4609 = 5992"; l.205 "59.8 d … (without the pause: 57.8"; l.206 rider "4616.4 … 6001.3 (default 4609.4 / 5992.2)" | unchanged; v8 l.123, 2535, 2905–2906, 2913 quote 4,609 / 5,992 / 60 days / 57.8; the rider (l.2883–2889, "not part of the default") quotes 4,616 / 6,001 as an option only |

**Printed cells against AV7's numbers** (stdout v8 l.354–376 against AV7 §1.2, §4 "Expected output"):
- Empty pilot: 75 [38–148], below.
- Z(νν) at pilot m = 5…50: 130 / 187 / 242 / 300 / 352 / 626. m = 20 is classed "below" (≤ 300).
- (γ) at m_H = 10…100: 104 / 180 / 255 / 294 / 331 / 448 (2 / 6 / 10 / 13 / 15 / 21 pilot counts).
- (α1), no credit: 587 / ≈ 2.85e+03 / ≈ 2.84e+04 (×339) and 975 / ≈ 4.79e+03 / ≈ 4.78e+04 (×201).
- (α1′): 4.96e+04–5.09e+04 / 4.96e+05–5.09e+05.
- (c) credit: 51 / 74.
- Grid at photon rate 0.379 [0.255]:
  - f_D = 0: ×34 / ×34 (97.0 %) [×23 (95.6 %)];
  - f_D = 1/4: ×52 / ×81 [×35 / ×55];
  - f_D = e⁻¹: ×69 / ×235 (98.6 / 99.6 %) [×47 / ×159];
  - f_D = 1/2: ×110 / none [×74 / none];
  - f_D = 1: none / none.

**All equal AV7, cell by cell. VERIFIED (my rerun).** My scratch reproduces ×34 / ×69 / ×235 through `_need`'s logic,
and B₅₀ with the conversions removed is 15 (f_D = 0) and 159 / 256 (f_D = e⁻¹).

## 2. Text against the verdict (task 2)

### 2.1 S2–S19 (location, quoted phrase; each compared with AV7 §4 word for word)

| item | v8 location | phrase found | as ordered? |
|---|---|---|---|
| S2 | §0 item 3, l.60 | "(scenario (α1′), Table 4.4c) (after CKF, as v1 counted them)" | yes |
| S3 | §0 l.67–68; leading sentence l.110–111; §12.5 pt 3 l.2999–3000 | "a lower value: a term whose S_CKF is not tested stays on all own hits, ×1/(1 − ε_pair) higher" (3 hits) | yes |
| S4 | §0 l.79 | "(a result after the freeze: its Z(νν) credit comes from the B4-c test, so the day-15 rule reads the same ceilings as (γ), v8 table of script [9b])" | yes |
| S5 | §0 l.90–100; the old sentence at v7 l.101–102 is deleted (hunk `101,102c106`); "If the pause fires…is Q2." is kept (l.100–106) | "It reads every no-pile-up term at max(zero-count floor, N_t·H) on all own hits before CKF, from the pilot's counts" … "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign (Q2)." | yes; brackets filled with the printed values (5.0×10⁴–5.1×10⁵; 2.8×10³–4.8×10⁴; 75; 20; 60; 13) |
| S6 | §0 l.114–117 | "(projected B₅₀ ≈ 5×10⁴–5×10⁵ on its own-hit basis against a limit of 300); a conversion veto can count only in a Q2 (c) redesign" | yes |
| S7 | §4.4 pt 4 l.795 | "(m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 counts in the pilot, script [9b] v8 table)" | yes |
| S8 | §4.4 pt 5 l.876 | "; with the other pilot ceilings empty, the day-15 class corresponds to ≈ 20 Z(νν) pilot counts (script [9b], v8 table)" | yes, but placed inside the closing parenthesis, not after it (C-1) |
| S9 | §4.4 l.1009–1010 | "(β) is a result after the freeze: at day 15 its Z(νν) credit does not exist yet" | yes (appended at the paragraph end, v7 l.1002) |
| S10 | Table 4.4c caption l.960–962 | "These rows are the projection of the result … quoted in Q2." | yes |
| S11 | §4.4 l.1024–1027 | "**The day-15 pause (B₅₀ > 300 events; m_H ≈ 125 pool counts for Z(νν) alone, ≈ 20 in the pilot; reach ≈ 560 GeV) is the expected branch**" … "quoted in Q2." | yes; the whole span from/through is replaced |
| S12 | §11.7 l.2724 | "(used only in the test of a Q2 (c) redesign)" | yes |
| S13 | §11.7 l.2742–2744 | "never at a central zero: … at most ×n/1.14" | yes. Checked: −ln 0.32 = 1.139, the one-sided 68 % value of Gamma(1) |
| S14 | §11.7 l.2746–2747 | "reach about 560 GeV or more …; on the pilot, ≈ 20 Z(νν) ceiling counts with the other pilot ceilings empty; the reading of each branch is the v8 table of script [9b]" | yes |
| S15 | Q2 stem l.2799–2808 | caption "What the day-15 rule reads, by branch (planning EST; script [9b], v8 table; B₅₀ against the limit 300):" and six rows | yes; rows checked in §2.3 |
| S16 | Q2 l.2833–2836 | "This branch also pauses (table). Further upside, after the freeze and statistics-only: … Their day-15 readings are the (γ) and empty-ceiling rows of the table." "Existing bounds lie below …" is kept | yes |
| S17 | Q2 (c) l.2850–2856 and l.2875–2877 | "no conversion rejection suffices: with the conversions removed, B₅₀ is 401–663" … "at least ×34 (97.0 %) [×23] … ×52–81 (98.1–98.8 %) [×35–55] … ×69–235 (98.6–99.6 %) [×47–159] at ×e⁻¹" … "At v1's central size (c) cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 51–74) acts on both." | yes. 401 / 663 = stdout v8 l.347–348 |
| S18 | rider (1) l.2884 | "(expected to trigger: the day-7 reading is expected at ≈ 5×10⁴–5×10⁵)" | yes |
| S19 | Df-9 row l.2939 | "; it also sets the basis of the day-7 and day-15 projections (own hits, no S_CKF, §11.7 rule 1)" | yes |
| S20 | script l.964 / stdout l.396 | "about 20 pilot counts: v8 table" | yes |
| bookkeeping | header l.1–7; §13.7 l.3095–3107 | the required sentence "No default, criterion, CPU-h, calendar figure or expected-outcome number changed; the day-15 reading per branch and the (c) bar are now quoted from script [9b] v8 lines." is present verbatim; one V1 row and one C row, plus an O3–O5 row | yes |

### 2.2 The sweep items of AV7 §2

- **The 4 incorrect statements are corrected.** #7 by S5: the "(β) and the empty-ceiling case" list is gone. #22 by
  S16. #26 and #28 by S17. In live text "would suffice", "×31" and "avoid" give 0 hits, and "×31–52" appears only as
  the printed ASCII comparison line "x52.1 / x31.0" (l.2872).
- **All 18 "needs a label" statements are labelled:** #1 (S2), #4 (S4), #6 and #8 (S5), #9 (S6), #10 (S7), #11 (S8),
  #12 (S9), #13 (S10), #14 (S11), #15 (S12), #16 (S13), #17 (S14), #21 (S16), #30 (S17), #32 (S18), #35 (S19),
  #40 (S20). Each phrase is in §2.1.
- The 18 statements that AV7 found correct are unchanged, except where a replaced span contained them (#3, #5, #27,
  #29 are kept inside S5 and S17).

### 2.3 The tables

- **Verbatim blocks.**
  - Day-15 block, v8 l.2813–2828, against stdout v8 l.354–369: `cmp` silent, so it is **byte-identical**.
  - Grid, v8 l.2866–2872 with the leading `> ` stripped, against stdout v8 l.370–376: `cmp` silent, so it is
    **byte-identical**.
  - The verbatim blocks were not in AV7; they came from an orchestrator instruction recorded in
    `experiment_log.md` l.463–467 ([Leopold] DECISION).
- **S15 short table against the verbatim block, cell by cell:**

| S15 row | S15 cell | printed cell(s) | agree |
|---|---|---|---|
| (α1′) | ≈ 5.0–5.1×10⁴ (0.8) to 5.0–5.1×10⁵ (0.98), above | 4.96e+04–5.09e+04 / 4.96e+05–5.09e+05, above | yes |
| (α1) | 587–975 after CKF; ≈ 2.8×10³–4.8×10⁴ own hits, above | 587 / 2.85e+03 / 2.84e+04; 975 / 4.79e+03 / 4.78e+04, above | yes (2.8 is the 2-figure rounding of 2,849 by FR; the printed 2.85 is ambiguous at 2 figures, C-2) |
| (β)/(γ) | 104 / 180 / 255 / 294 / 331 / 448; below up to ≈ 60 pool (≈ 13 pilot) | same six; below at 60 (294), above at 70 (331); (beta) row "not a day-15 branch" | yes |
| Z(νν) alone | 300 at ≈ 20 pilot counts; "below under ≈ 20" | 300 at m = 20, classed **below** | yes in value. "below under ≈ 20" against §0/S8/S14 "up to ≈ 20" and the printed "below" at exactly 20 (C-3) |
| empty pilot | 75 (38–148), below | 75 [16-84 %: 38-148], below | yes |
| (c) only | 51–74, below | 51 / 74, below | yes |

**Captions.**
- The day-15 caption (l.2810) states what rule 1 measures, the threshold, the ESTIMATE label, the 1–2 counts behind
  DIF, the assumed ε_pair and the (c)-only rows. It is correct; the one non-rule-1 cell (587 / 975) is labelled in its
  own row ("after CKF (Table 4.4c)").
- **The grid caption (l.2858–2863) is not correct: W1, §6.**

### 2.4 C items (AV7 §5)

- **The 14 (i) items are applied exactly:**
  - Cr C1 / Ph C-6 (l.1668);
  - Ph C-4 (l.829);
  - Cr C4 (l.2095);
  - Cr C7 (l.2296);
  - Cr C6 (COM l.6–8);
  - Ph C-1, C-2, C-5, Cr C2, C3 and Co C1, C2, C4, which sit inside S2–S19 (§2.1).
- **The package-only and deferred items are not applied:**
  - Co C3 ("publishable but less strong": 0 hits in v7 and v8).
  - Cr C5 (the own-hit bracket at 0.255; "3.4×10⁴": 0 hits; Q2 l.2798 still says "at the 0.379 photon rate").
  - Cr C8 (fix-report wording, not the artifact).
  - The Gate-A package corrections of AV7 §7 are not in the strategy (FR §4).

## 3. Additions beyond the verdict (task 3)

| item | text | check | verdict |
|---|---|---|---|
| O3 | §0 l.62–63: "(projected B₅₀ 590–980; (α1); after CKF, as v1 counted them; the day-15 rule reads this branch on all own hits, (α1) rows of the v8 table of script [9b])" | stdout v8 l.314 / l.316 print the Table 4.4c rows 548 / **587** / 626 and 925 / **975** / 1025 (590–980 is their rounding; 570–960 = 385 + 183 and 647 + 308). Those lines do **not** themselves carry an "after CKF" label: the label is printed at l.365–366 ("after CKF (Table 4.4c)" … 587 / 975), and the S10 caption states it ("the (α) rows after CKF, as v1 counted them") | **correct** and in scope (a basis label of the family; no number changed). The LOG/FR wording "confirmed from stdout lines 314/316 and 365–366" is loose: 314/316 give the numbers and 365–366 the label (C-4, record only) |
| O4 | §11.7 l.2739, Q2 l.2799: "script [9b], U1 line" | the line cited is stdout v8 l.353 "v7 (U1): (alpha1') on the day-15 own-hit basis …", unchanged. In live text "v7 line" gives 0 hits | correct. (Two stdout lines start "v7 (U1)"; the content in both places makes the own-hit line unambiguous) |
| O5 | Code reference l.3112: "about 90 seconds, measured on einstein for version 8: 1 min 30 s wall, 35 MB" | my run: 1:30.39 wall, 35,192 kB | **correct**. The script docstring l.4 still says "about ten seconds" and names STRATEGY v4; that line may not change in this cycle (item S: "No other line changes"), so it is C-5 for later |
| COM | pointer → v8 ("version 8, after review cycle 7"); Cr C6 (doubled "and" removed, v7 appended to the list of earlier versions); new section "Changes of rows in version 8" with the TG-1 (Q2) row | `git diff HEAD~1 -- COMMITMENTS.md`: exactly these two hunks. The TG-1 row text equals AV7 §4 word for word; "no status changed" | all three are ordered by AV7 §4 (Cr C6 bullet). Correct, in scope |

## 4. Diff check, complete (task 4)

`diff v7 v8` gives **32 hunks** (count by `grep -cE '^[0-9]'`). Each hunk was read in full:

| hunk (v7→v8) | item |
|---|---|
| 1c1; 3,5c3,5; 7c7 | bookkeeping (title, fixer line, status cycle 8) |
| 60c60 | S2 |
| 62c62,63 | O3 |
| 66,67c67,68 | S3 (§0) |
| 78c79 | S4 |
| 89,95c90,100 | S5 (kept: "If the pause fires and the user chooses Q2 (b), the") |
| 101,102c106 | S5 (deletion of the day-7/15 sentence) |
| 107c111 | S3 (leading sentence) |
| 111,112c115,117 | S6 |
| 790c795 | S7 |
| 824c829 | Ph C-4 |
| 871c876 | S8 |
| 955c960,962 | S10 |
| 1002c1009,1010 | S9 |
| 1017,1019c1025,1027 | S11 |
| 1660c1668 | Cr C1 / Ph C-6 |
| 2087c2095 | Cr C4 |
| 2288c2296 | Cr C7 |
| 2716c2724 | S12 |
| 2731c2739 | O4 |
| 2734c2742,2744 | S13 |
| 2736,2737c2746,2747 | S14 |
| 2789c2799,2831 | O4 + S15 + verbatim day-15 block and caption (orchestrator); "Upside (statistics-only; …" kept |
| 2791,2796c2833,2836 | S16 (the "84 % edge (median 470–500 …)" head and "Existing bounds …" tail are kept) |
| 2810,2815c2850,2877 | S17 + verbatim grid and caption (orchestrator); "The veto's rejection has not" kept |
| 2822c2884 | S18 |
| 2877c2939 | S19 |
| 2937,2938c2999,3000 | S3 (§12.5 pt 3) |
| 3032a3095,3107 | §13.7 (bookkeeping) |
| 3037c3112 | O5 |

**Unattributed hunks: 0.** Inside each hunk I found no change other than the item's text and re-wrapping.

The same holds for COM (2 hunks: pointer + Cr C6; v8 row section) and for the script (2 hunks: item S, S20).
`git diff HEAD~1 --stat` shows nothing else changed under the artifact paths: the other files in the commit are logs,
the FR, `LOG.md` and `ORCHESTRATOR_STATE.md`. Untouched, as ordered: Table 4.4c rows (no hunk in v7 l.956–990), §11.2,
Q1, Q3, Q4, Q5 and the annex (no hunks between v7 l.2822 and l.2877, other than S19 in the Df-9 row).

## 5. My sweep of the family in v8 (task 5)

Method:
1. I grepped in v8 for the listed terms ("pause", "avoid", "suffic", "300", "×31", "×34", "×5–50", "(α1", "(β)",
   "(γ)", "S_CKF", "fit-probability", "rejection", "veto", "day-7", "day-15", "before CKF", "after CKF", "590", "980",
   "159", "256", "345", "566"). This gave 190 hit lines outside §13.
2. I read §0 (l.50–130), §4.4 points 4–5 (l.786–796, 868–879), §11.7 (l.2714–2753) and §12.1–12.5 (l.2785–3010) in
   full.
3. I discarded hits with another meaning: 300 as GeV / fb⁻¹ / rows; the lepton or vertex veto as a design; δ(β); qq̄(γ);
   sha256; PLAN l.345; the day-15 reserve as a budget line.

Out of family: "345" and "566" give 0 hits. "159" and "256" appear only as the printed grid ×159 and in unrelated
references (l.221, 632, 2072).

Columns: **agree** = consistent with the printed v8 table/grid row; **label** = basis label present where needed (n/a for
calendar or a pure threshold).

| # | location | phrase (abridged) | table row | agree | label |
|---|---|---|---|---|---|
| 1 | §0 l.60 | (α1′) ≈ 1.0×10⁴ "(after CKF, as v1 counted them)" | result basis; day-15 = (alpha1') row | yes | yes |
| 2 | §0 l.62–63 | (α1) 590–980 "after CKF …; the day-15 rule reads this branch on all own hits, (α1) rows" | (alpha1) 587 / 975 after-CKF cells | yes | yes |
| 3 | §0 l.67–68 | 0.7–1.0×10⁴ after CKF, "a lower value: … ×1/(1 − ε_pair) higher" | label | yes | yes |
| 4 | §0 l.74 | "expected to pause the study before production (§11.7, Q2)" | (alpha1') above | yes | n/a (cites) |
| 5 | §0 l.79 | (β) "a result after the freeze … reads the same ceilings as (γ)" | (beta) row | yes | yes |
| 6 | §0 l.90–91 | pause if B₅₀ > 300 or both estimators miss cap; preliminary at day 7 | threshold | yes | n/a |
| 7 | §0 l.91–95 | rule-1 basis; "×5–50 above the after-CKF figures (ε_pair assumed …)" | header; (alpha1) cells | yes | yes |
| 8 | §0 l.95–96 | "B₅₀ ≈ 5.0×10⁴–5.1×10⁵ … ((α1′)) and ≈ 2.8×10³–4.8×10⁴ … ((α1))" | (alpha1'), (alpha1) own-hit cells | yes | yes |
| 9 | §0 l.97 | "B₅₀ ≈ 75 with every pilot ceiling at zero" | empty row | yes | yes |
| 10 | §0 l.98 | "Z(νν) alone may count up to ≈ 20 pilot ceiling events" | Z row, 300 at m = 20 below | yes | yes |
| 11 | §0 l.98–99 | "every SM ceiling up to ≈ 60 pool-equivalent counts (≈ 13 in the pilot) … (β) is read as (γ)" | (gamma) 294 / 331; (beta) | yes | yes |
| 12 | §0 l.99–100 | "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" | (c) rows | yes | yes |
| 13 | §0 l.100–106 | if the pause fires / does not fire | conditional | yes | n/a |
| 14 | §0 l.110–111 | after CKF, lower value (leading sentence) | label | yes | yes |
| 15 | §0 l.114–117 | "≈ 5×10⁴–5×10⁵ on its own-hit basis …; no conversion rejection suffices without a reduction of the decays in flight" | (alpha1'); grid f_D = 1 | yes | yes |
| 16 | §0 l.129–130 | calendar "≈ 2 are the expected day-15 pause; 58 days without it" | (alpha1') above | yes | n/a |
| 17 | §4.4 l.795 | conversions m_H ≈ 1.6×10³ (≈ 3×10² pilot) "far above the day-15 class (m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 counts in the pilot" | Z row | yes | yes |
| 18 | §4.4 l.829 | C′_PU "development estimate of a Q2 (c) redesign (if the rider is taken …)" | (c) sample | yes | n/a |
| 19 | §4.4 l.874–876 | pilot expects 0.4–3.7 / 2–190; "Gamma(m + 1) of the pilot count"; 12 events; "≈ 20 Z(νν) pilot counts" | Z row | yes | yes |
| 20 | Table 4.4c caption l.960–962 | "projection of the result … The reading of the day-15 rule … is the v8 table" | whole table | yes | yes |
| 21 | Table 4.4c rows l.973–981 | (β) 24/36/79; (γ) 56/133/398; (α1) 587–975; credit 51–74; ×e^∓1 230–373 / 1,563–2,615; (α1′); (α1′) credit 580–599; (α2) | result basis by caption; (γ) here = AV7's "lower edge" basis | yes | yes (caption) |
| 22 | §4.4 l.1009–1010 | S9 | (beta) | yes | yes |
| 23 | §4.4 l.1024–1027 | "**The day-15 pause (B₅₀ > 300 events; m_H ≈ 125 pool counts …, ≈ 20 in the pilot …) is the expected branch**" | (alpha1'); Z row | yes | yes |
| 24 | §4.11 l.1667–1668 | "reading expected if the day-15 pause does not fire" | conditional | yes | n/a |
| 25 | §4.17 l.2095 | row 4 role "for the conversions, the Q2 (c) development estimate" | (c) sample | yes | n/a |
| 26 | §7 l.2296 | [L13] ≈ 10⁴ "(after CKF, as v1 counted them)" | label | yes | yes |
| 27 | §11.2 l.2534–2536 | "58.9 / 59.8 / 60.1 with the expected day-15 pause" | (alpha1') above | yes | n/a |
| 28 | §11.3 l.2573 | "every day after 15 moves by ≈ 2 in the expected branch" | (alpha1') above | yes | n/a |
| 29 | §11.4 l.2605–2606, 2610 | "60 days … in the expected branch …; 58 days if the pause does not fire" | (alpha1') above | yes | n/a |
| 30 | §11.6 l.2693–2694 | "60 days (57.8 … turnaround of the expected day-15 pause …)" | (alpha1') above | yes | n/a |
| 31 | §11.7 l.2717 | decision row 3 "without the day-15 pause" | calendar | yes | n/a |
| 32 | §11.7 l.2724 | S12 | (c) rows | yes | yes |
| 33 | §11.7 l.2737–2739 | "N_t·H on all own hits, with no S_CKF …; ×5–50 …; script [9b], U1 line" | header; U1 line l.353 | yes | yes |
| 34 | §11.7 l.2739–2744 | (c) test with conditional and S_CKF on development samples, EST; ×n/1.14 | (c) rows; grid | yes | yes |
| 35 | §11.7 l.2745–2747 | "at most 300 … reach about 560 GeV …; on the pilot, ≈ 20 Z(νν) ceiling counts" | Z row | yes | yes |
| 36 | §11.7 l.2748–2749 | "(α1′) … this is the expected branch" | (alpha1') | yes | yes |
| 37 | Q2 l.2790–2792 | 0.7–1.0×10⁴ "(after CKF, as v1 counted them; a lower value …)" | label | yes | yes |
| 38 | Q2 l.2795–2796 | "expected to pause the study before production" | (alpha1') | yes | n/a |
| 39 | Q2 l.2796–2799 | "count own hits before CKF … ×5–50 … 5.0–5.1×10⁴ … 5.0–5.1×10⁵ … U1 line" | (alpha1'); l.353 | yes | yes |
| 40–45 | Q2 S15 table l.2803–2808 (6 rows) | see §2.3 | each its row | yes (C-3 on wording) | yes |
| 46 | Q2 l.2810 + l.2813–2828 | day-15 caption + verbatim block | itself | yes (identical) | yes |
| 47 | Q2 l.2833 | "This branch also pauses (table)" | (alpha1) above | yes | yes |
| 48 | Q2 l.2833–2836 | (β), every ceiling empty "after the freeze …; Their day-15 readings are the (γ) and empty-ceiling rows" | (gamma); empty | yes | yes |
| 49 | Q2 l.2837 | question: "If the day-15 projection exceeds B₅₀ = 300" | threshold | yes | n/a |
| 50 | Q2 (a)/(b) l.2838–2840 | pause and ask; "no pause for this cause" | default (a) unchanged | yes | n/a |
| 51 | Q2 (c) l.2849–2850 | works if ≤ 300 "with the redesigned conditional and S_CKF estimated on development samples (EST" | (c) test | yes | yes |
| 52 | Q2 (c) l.2850–2851 | "no conversion rejection suffices: with the conversions removed, B₅₀ is 401–663" | grid f_D = 1; stdout l.347–348 | yes | yes |
| 53 | Q2 (c) l.2852–2854 | "at least ×34 (97.0 %) [×23] … ×52–81 … ×69–235 … at ×e⁻¹" | grid rows f_D = 0, 1/4, e⁻¹ | yes | yes (S17: "If S_CKF cannot be estimated …, ×1/(1 − ε_pair) larger" implies the grid assumes S_CKF estimated) |
| 54 | Q2 (c) l.2854–2855 | "×n/1.14 (§11.7 rule 1)" | S13 | yes | yes |
| 55 | Q2 (c) l.2855–2856 | "every factor must be ×1/(1 − ε_pair) larger (×5–50, not measured)" | grid comparison line | yes as printed | yes (C-6 on scope) |
| **56** | **Q2 (c) grid caption l.2858–2863** | "with the remaining terms read as rule 1 reads them (all own hits before CKF, no S_CKF, no credit that exists only after the freeze)" | grid code: (α1) DIF at its **after-CKF** level on **pool** κ, conversions at the after-CKF (α1′) level G_A1P, other terms at **pool** floors (`kap_nodif`) | **no** | **wrong** (W1) |
| 57 | Q2 (c) l.2866–2872 | verbatim grid | itself | yes (identical) | — |
| 58 | Q2 (c) l.2875–2877 | "(c) cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 51–74) acts on both" | grid f_D = 1; (c) rows | yes | yes |
| 59 | Q2 l.2879 | "If the projection is at most 300 events (reach ≈ 560 GeV …), production proceeds" | threshold | yes | n/a |
| 60 | rider l.2884 | "(expected to trigger: the day-7 reading is expected at ≈ 5×10⁴–5×10⁵)" | (alpha1') | yes | yes |
| 61 | Q3 l.2899 | "Reach under the default: (β) of Table 4.4c: 705–640 GeV" | post-freeze result | yes | yes (Table 4.4c) |
| 62 | Q4 l.2906–2908 | "60 days (57.8 without …; … the pause is the expected branch …)" | (alpha1') | yes | n/a |
| 63 | Q4 alt l.2916–2917 | "59 days (57 without the pause)"; "60 days (58 without)" | calendar | yes | n/a |
| 64 | Df-9 l.2939 | S19 | header | yes | yes |
| 65 | annex route 5 l.2957 | "(β) … then becomes (γ)-like" | post-freeze | yes | n/a |
| 66 | annex route 6 l.2958 | "×1/(1 − ε_pair) above H_CKF (×5–50 …)" | label | yes | yes |
| 67 | annex B4-e l.2959 | "4.6×10³ events …, by itself above the day-15 class" | threshold (4.6×10³ > 300) | yes | n/a |
| 68 | §12.5 pt 1 l.2991 | "neither is inside its cap at day 15" (the estimator half of the pause rule) | threshold | yes | n/a |
| 69 | §12.5 pt 2 l.2993–2996 | "near 600–1,000 events if decays in flight and conversions fall like the pile-up background (Table 4.4c, (α1))" | result basis (587–975) | yes | no explicit "after CKF" (C-7; not a day-15 statement; Table 4.4c's caption carries it) |
| 70 | §12.5 pt 3 l.2997–3002 | (α1′) after CKF, lower value; "The day-15 rule pauses the study (Q2)" | (alpha1') | yes | yes |
| 71 | stdout l.396 | "(day-15 class limit: m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)" | Z row | yes | yes |

**Count: 71 entries, i.e. 76 statements counting the six S15 rows separately.**
- **"no" in agreement: 1, #56 (W1).**
- **"no" in the label column: #56 (a wrong label) and #69 (a missing label; C, since it is a result-basis statement).**

**Comparison with FR's 58.**
- FR covers all my entries except the calendar statements of the expected pause (#16, #27–30, #63) and §12.5 point 1
  (#68). All of these agree, so FR missed no defect among them.
- **FR missed one defect:** its #46 ("Q2 (c) caption and verbatim grid … yes") rates the grid caption as consistent,
  but it is not (W1). The caption is the fixer's own text; FR §2 itself records "These rows use pool κ (the Table 4.4c
  basis of the (α1) terms), not pilot κ", which the caption contradicts.

## 6. Findings

### W1 (Category B): the grid caption misstates the basis of the (c) rejection grid

**Location:** v8 l.2858–2861. Text: "The conversion rejection a (c) redesign needs for B₅₀ ≤ 300 …, with the remaining
terms read as rule 1 reads them (all own hits before CKF, no S_CKF, no credit that exists only after the freeze)".

**The code says otherwise.** `_need` (script l.885–897, AV7's code) builds:
- `base = kap_nodif + [(K_DIF, d_/K_DIF)]`, where `kap_nodif = [(r[4], 0) …]` (script l.718) are the **pool** floors,
  not the pilot exposures of rule 1;
- `d_ = ALPHA[(tag, False)][0] × f_D`, the (α1) DIF of 385 / 647 events, which is v1's **after-CKF** level (Table 4.4c,
  labelled "after CKF" in stdout l.365–366 and in the S10 caption);
- conversions `G_A1P` = 9,527 events (script l.833), the after-CKF (α1′) level.

So the grid is the (c) test with S_CKF credited at v1's level, on pool floors. It is not "all own hits before CKF, no
S_CKF".

**The caption contradicts its own block and S17:**
- The last printed line of the grid (l.2872) says "without an S_CKF estimate every factor is x1/(1 - eps_pair)
  larger".
- S17 (l.2855–2856) says "If S_CKF cannot be estimated before the freeze, every factor must be ×1/(1 − ε_pair)
  larger".
- Both statements are true only if the grid assumes S_CKF.

**Why this is B, not C:**
- It is a basis label of the bar for option (c), which is exactly the V1 family that cycle 7 classed B and ordered fixed
  structurally.
- It was introduced by this fix (a regression of the fix, admissible under AV7 §11).
- It sits in the Gate-A text next to the numbers. Read literally, the decays in flight would be on all own hits.
  At f_D = e⁻¹ that is 142 / (1 − 0.8) ≈ 710 events for the ×339 case [E: 385 × e⁻¹ / 0.2], above 300 by itself, so
  "×69 suffices" would be false on the basis the caption states.
- The numbers are correct on their actual basis; only the description is wrong.

**Fix (text only, 0 CPU-h).** Replace "with the remaining terms read as rule 1 reads them (all own hits before CKF, no
S_CKF, no credit that exists only after the freeze)" with:

> on the basis of the (c) test with S_CKF estimated at v1's level: decays in flight and conversions after CKF, as v1
> counted them, and the other terms at their Table 4.4a pool floors (the Table 4.4c basis); no credit that exists only
> after the freeze; without an S_CKF estimate the factors are larger (last line)

Check after the fix: no other v8 sentence describes the grid's basis. S17's "(script [9b], v8 table; …)" and l.2855
already agree with this text.

### C items

- **C-1 (S8 placement).** The S8 clause is inside the parenthesis "(a pilot zero is a bound … ; with the other pilot
  ceilings empty, … (script [9b], v8 table))" rather than after it. The meaning is the same. No action.
- **C-2 (rounding).** In "≈ 2.8×10³–4.8×10⁴" the printed lower cell is "2.85e+03". FR's unrounded 2,849 supports 2.8,
  but a reader comparing with the printed cell may expect 2.9. Optional: print `.4g` or write "≈ 2.85×10³". I did not
  recompute 2,849 (UNVERIFIED, FR scratch).
- **C-3 (wording).** S15 row "below under ≈ 20" against §0/S8/S14 "up to ≈ 20" and the printed "below" at exactly
  m = 20 (B₅₀ = 300). Prefer "below up to ≈ 20".
- **C-4 (record).** LOG 05:40 and FR §4b say that O3's after-CKF basis is "confirmed from stdout lines 314/316 and
  365–366". 314/316 confirm the numbers; only 365–366 (and the S10 caption) print the label. Not the artifact.
- **C-5 (script docstring).** Script l.2–4 still say "STRATEGY v4" and "about ten seconds"; the measured runtime is
  90 s (O5). This could not change this cycle (item S: "No other line changes"). Fix it at the next script edit.
- **C-6 (scope of "every factor ×1/(1 − ε_pair) larger", S17 l.2855–2856 and the grid's last line; AV7 text).**
  - The statement holds if only the conversions' S_CKF is missing. The DIF S_CKF is planned to be tested (annex
    route 6: DIF R06 on the enriched overlays, P = 0.92).
  - If the DIF S_CKF were also missing, the DIF term alone on own hits exceeds 300 once f_D ≳ 0.14 (×339) or ≳ 0.09
    (×201) at ε_pair = 0.8 [E: (300 − 25) × 0.2 / 385 and / 647, sum-of-medians arithmetic]. No conversion
    rejection would then suffice.
  - Suggest "every conversion factor" and one clause for the DIF case, or leave as is: the conclusion only strengthens
    the default. For the package.
- **C-7 (§12.5 point 2).** "near 600–1,000 events … (Table 4.4c, (α1))" has no explicit "after CKF". It is not a day-15
  statement, and Table 4.4c's caption carries the basis. For consistency with O3, one could add "(after CKF, as v1
  counted them)".
- **C-8 (pool vs pilot exposures in the (c) rows; sensitivity, ESTIMATE).**
  - The grid and the (c)-credit rows (51 / 74) use pool floors; rule 1 reads the pilot-measured terms at the pilot
    exposures.
  - My scratch (runpy of the script, its own `pmf_pred`, `K_PIL`, `ALPHA`, `G_A1P`, the same bisection) recomputed the
    grid with the other terms at the pilot exposures (DIF still at its planning size). It gives ×35 / ×35 at f_D = 0
    (printed ×34) and ×75 / ×311 at f_D = e⁻¹ (printed ×69 / ×235; 98.7 / 99.7 % against 98.6 / 99.6 %). The rest of
    the terms alone reads 25 against 15 on pool floors. VERIFIED (scratch).
  - No conclusion changes: (c) needs ≥ ×34–35 in every case and is impossible at v1's central size. The bar is thus a
    slight lower edge on the rule's own basis.
  - With W1's caption stating "pool floors", the numbers are correctly labelled. Optional: one clause "on the pilot
    exposures of rule 1 the factors are slightly larger (≈ ×35; ×75 / ×311 at e⁻¹)". For the package or the next
    script edit.
  - Also note the triple parenthesis "(scenario (α1′), Table 4.4c) (after CKF, as v1 counted them) (with …" at l.60
    (S2's own text; style only).

## 7. Superseded figures (task 6)

| figure | hits (v8, COM) | status |
|---|---|---|
| 4,574 / 5,946 | v8 l.2550 ("Version 4 had … an approved figure of 4,574 and a threshold of 5,946"), l.3047, l.3066 (§13 history); COM l.76 (section "Changes of rows in version 4") | **history, labelled**. Current COM ST-1 rows: l.59 "4,609 …, threshold 5,992", l.222 "4,609 CPU-h … and 60 days (57.8 …" |
| 57.6 | v8 l.3051, l.3066 (§13 history only) | history |
| 710 / 790 GeV | l.79, l.2835 "if every no-pile-up ceiling counts zero, an upper edge" / "every ceiling empty … an upper edge"; l.967 Table 4.4c "(upper edge)"; l.2881 "helps only if the ceilings are empty" | **not an expectation**; labelled as an upper edge. Other hits are unrelated (l.190 arithmetic, μ₉₅ 790 of v1) |
| 470–500 GeV | l.75, l.2833: the median of (α1) "if decays in flight and conversions fall like the pile-up background" | conditional branch, not an expectation; correct |
| "serves only C1" | 0 hits (v8, COM) | gone |

None is live as current.

## 8. Statement on open items

- **Category A: none.**
- **Category B: one, W1:** the (c) grid caption, v8 l.2858–2861, states the wrong basis for the printed grid. It is a
  one-phrase text fix and needs no script change, no number change and no CPU-h.
- **Category C: eight (C-1 … C-8).** None blocks.

Everything else in scope is verified as applied and correct:
- item S code and stdout (byte-identical);
- S2–S20;
- the 4 incorrect and 18 label statements of AV7 §2;
- the 14 C (i) items, with the package-only and deferred items not applied;
- the verbatim tables (byte-identical);
- O3–O5 and the COM changes;
- 32 of 32 hunks attributed.

The settled items (rule 1, the (c) test with S13, the defaults Q1–Q5) and the figures 4,609 / 5,992 / 60 (57.8) days
and the rider 4,616 / 6,001 are unchanged.
