# Critical review: Phase 1 STRATEGY v6 (quirks v2), review cycle 6

Reviewer: Ivan (critical), 2026-11-14 02:50. Fresh session; I saw no earlier cycle. I followed `agents/critical_reviewer.md`
(adversarial stance, show the work, A/B/C) within the narrow scope that the cycle-5 arbiter set (verdict §9). That scope
is T3, the v5 → v6 diff, the greps and the script outputs. Phase 1 has no figures, fits or validation results, so the
figure, closure and systematic-propagation checks of the template do not apply.

**Artifact.** `phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("v6", 3,006 lines; "l." means a line of v6),
`COMMITMENTS.md` ("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v5.txt` and
`budget_stdout_v6.txt`. The reference is the cycle-5 verdict `review/arbiter/STRATEGY_ARBITER_v5_hugo_2026-11-14_01-55.md`
("AV"). I read the fix report `FIX_REPORT_cycle5_ingrid.md` but did not take its claims as evidence. Each claim below was
re-checked with `diff`, `grep` or a fresh run.

**Read in full.** The role file, `AGENT_RULES.md`, AV, the fix report, the full v5 → v6 diff, the COM and script diffs
against `HEAD~1`, the v5 → v6 stdout diff. Of v6: §0 (l.28–130), Table 4.4c with its caption and scenario text
(l.940–1016), §11.2 (l.2521–2540), §11.3–§11.7 (l.2560–2750), §12.1 entire (l.2756–2882). Also brief `prompt.md` l.76–81
and l.336–350.

**Rules.** No sub-agents, no git writes, and nothing heavy. The only computation was one standard-library run of the
script (`nice -n 10 python3 -I`, 38.8 s, 34.8 MB max RSS). I wrote only this file and the session log.

---

## Verdict

**0 Category A, 0 Category B, 5 Category C.**

T1, T2 and T3 are present as ordered in every location that the fix report lists. Every hunk is attributed. The script
reproduces `budget_stdout_v6.txt` byte for byte, and no value printed in v5 has changed. The rider is nowhere treated
as adopted.

---

## 1. Diff check (complete)

### 1.1 Strategy v5 → v6: 30 hunks, all attributed (VERIFIED, `diff`)

| # | v5 → v6 lines | content | attribution | text = AV text? |
|---|---|---|---|---|
| 1–3 | 1, 3–5, 7 | title "version 6", fixer header, "cycle 6" | AV §6 general rule | — |
| 4 | 16 | "Fiona, Gunnar or Ingrid" | Cr-C2 (AV §6.3) | yes |
| 5 | 58 | 0.04–0.07 | T1-c (Cr-C4) | yes |
| 6 | 60 → 60–61 | photon-rate clause | T1-c (Cr-C3, Ph-C1) | yes, inserted at the ordered place |
| 7 | 65–67 → 66–72 | §0 "Expected" | T1-b | yes, except "**its 84 % edge** is already below 243 GeV at a width of 0.03" (departure 2, §5) |
| 8 | 74 → 79–81 | upper branches statistics-only | T1-b second insert (AV Case 5) | yes, placed before "Existing bounds lie below about 180 GeV" |
| 9 | 83–85 → 90–95 | §0 "The pause." | T2-a | yes |
| 10 | 93–94 → 103–107 | leading sentence | T1-a | yes |
| 11 | 106 → 119 | §0 Calendar | T3 | yes |
| 12 | 933 → 946–950 | Table 4.4c caption | T1-d | yes, plus "(84 % edge)" (departure 2) |
| 13 | 949 → 966 | (α1′) row label and reach cell | T1-d | label uses the script values 6,825–7,087 and [297–293] (departure 1); reach cell exact |
| 14 | 962 → 979–980 | "v1 conversion record … more favourable DIF reading" | T1-e (Ph-C4 wording) | yes |
| 15 | 974 → 992–994 | scenario statistics-only sentence | T1-e | yes, except "its 84 % edge is so already" (departure 2) |
| 16 | 993 → 1013–1014 | "removing the conversions alone does not bring B₅₀ below 300" | T2-b | yes |
| 17 | 2261–2262 → 2282–2284 | [L13] | Ph-C5 | yes |
| 18 | 2499–2501 → 2521–2523 | §11.2 table, three rows | T3 (proposed row ordered; the other two rows are the admitted extra, §1.2) | proposed row exact |
| 19 | 2570 → 2592–2593 | §11.3 calendar estimate | T3 | yes |
| 20 | 2657 → 2680–2681 | §11.6 approved schedule | T3 | yes |
| 21 | 2697 → 2721–2723 | rule 1, C′₀ condition | H-C10 | yes; ", and becomes binding" turned into "; and it becomes binding" for the grammar |
| 22 | 2744–2751 → 2770–2782 | Q2 stem | T1-f / T2-c (H-C2, H-C5, Cr-C6) | yes, word for word |
| 23 | 2756–2757 → 2787–2791 | Q2 (b) | T1-g (H-C3) | yes |
| 24 | 2761 → 2795–2797 | Q2 (c) success condition | T2-d (H-C4, Ph-C2) | yes |
| 25 | 2764 → 2800–2809 | 790 → 814 GeV; optional rider | H-C6; rider (AV §7) | yes; the rider adds "; script [7], rider line" inside its cost parenthesis, a source pointer that changes no value |
| 26 | 2780–2782 → 2825–2831 | Q4 calendar, DP glosses, §11.6 pointer | T3; H-C7; Cr-C5 | yes; the pointer sits inside "(§11; …)" rather than after it, with the same meaning |
| 27 | 2786–2787 → 2835–2836 | Q4 alternatives 59 (57) / 60 (58) days | T3 | yes |
| 28 | 2837 → 2886 | §12.2 entries | Cr-C2 | yes |
| 29 | 2867–2870 → 2916–2920 | §12.5 point 3 | T1 (Cr-C1) | yes |
| 30 | 2935a → 2986–2998 | §13.5 change table | general rule (change history) | — |

**Unattributed hunks: none.** The v6 left-for-later items of AV §6.4 (Ph-C3, the Ph-C4 downside, H-C8, Cr-C7) were not
touched (VERIFIED: no hunk in §4.4 "downside", §11.3 hand-over or COM T2-h / TG-1).

### 1.2 The extra change: 58.9 / 60.1 on the MUST-only and full rows of §11.2

**Justified.** Three reasons:
1. AV §6.2 orders the Q4 alternatives as "59 days (57 without the pause)" and "60 days (58 without)". Without the extra
   change, the §11.2 table, which Q4 cites with "(§11)", would give the same two variants only without the pause.
2. AV §9 sets the critical reviewer's check as "T3 chain (59.8 / 58.9 / 60.1 identical in §0, **§11.2**, §11.3, §11.6, Q4,
   COM ST-1)". The verdict therefore expected 58.9 and 60.1 in §11.2.
3. Both values are printed: stdout l.205, "MUST-only 58.9; full 60.1 (without the pause: 57.8 / 56.9 / 58.1)". They are
   56.9 + 2.0 and 58.1 + 2.0.

The change alters no figure and no default.

### 1.3 COMMITMENTS.md (`git diff HEAD~1`): 4 hunks, all attributed

(1) l.3–4: current strategy → v6, version 6. (2) l.5–6: version 5 added to the list of earlier versions. These two are
the general rule, as in every cycle. (3) The new table "Changes of rows in version 6", with one row for ST-1. This is the
general rule. (4) The ST-1 approved-schedule clause, which is T3 and matches AV §6.2 "COM ST-1. The same clause" word
for word: "60 days (57.8 days plus the ≈ 2-day turnaround of the expected day-15 pause; a redesign under Q2 (c) is not
included and is reported as an overrun)". No status changed and no row was removed. TG-1 is unchanged and states no
changed number. The diff adds no rider row.

### 1.4 Script (`git diff HEAD~1`): 4 hunks, all attributed

(1) l.299: "v4 approved figure" → "approved figure" (H-C9). (2) After l.432: the T3 line and the rider line (AV §6.1
items 2 and 3). `PAUSE15 = 2.0` is commented as the Gate-B turnaround. The rider line computes 1000 × SIG / H on the
existing constants. (3) After l.772: the v6 (T1) block (rates 1 and 0.25518676537664065 / 0.3786327036399709, with the
JSON keys named in a comment; w = 0.03 / 0.05 / 0.17; (α1) and Z(νν) m_H = 100 with w = 0.17) and the v6 (T2) lines (AV
§6.1 item 1). (4) After l.795: HEADLINE v6 (AV §6.1 item 1, last bullet). No existing line changed except the H-C9
label. The new block reads `pmf_cache` but does not write to it; §2 confirms empirically that nothing printed later
changed.

---

## 2. Script

- Fresh run: `nice -n 10 python3 -I src/strategy_budget.py`, imports `math`, `random` only; rc 0; 38.8 s; max RSS
  34.8 MB. **Output byte-identical to `budget_stdout_v6.txt`** (`cmp` silent; sha256 `3a9db8b3…8a11` for both). VERIFIED.
- `diff budget_stdout_v5.txt budget_stdout_v6.txt`: one changed line (l.121, the H-C9 relabel; its value 156.5 is
  unchanged), and 2 + 26 + 1 = **29 added lines** (l.205–206, l.326–351, l.356). The file grows from 525 to 554 lines.
  **Every value printed in v5 is unchanged.** VERIFIED. (The fix report says "30 added lines" because it counts the `>`
  side of the relabel too. See C5.)
- The added lines are exactly the four kinds the verdict allows: the v6 (T1)/(T2) [9b] lines, the [7] T3 line, the
  rider line and the HEADLINE v6 line.

---

## 3. T3 and the Q4 figures: every location

The printed source is stdout l.120–125 and l.202 (approved 4,609.4, threshold 5,992.2, 57.8 days), l.205 (59.8 / 58.9 /
60.1) and l.206 (rider 4,616.4 / 6,001.3).

| location | approved CPU-h | threshold | calendar | match |
|---|---|---|---|---|
| §0 Cost, l.113 | 4,609 | — | — | yes |
| §0 Calendar, l.119 | — | — | "about 8.5 weeks … (60 days, of which ≈ 2 are the expected day-15 pause; 58 days without it" | yes (59.8 / 7 = 8.5) |
| §0 Stop rules, l.125 | — | 5,992 | — | yes |
| §11.2 table, l.2521–2523 | 4,176 / **4,609** / 5,123 | 5,429 / **5,992** / 6,660 | 56.9 (58.9) / **57.8 (59.8)** / 58.1 (60.1) | yes |
| §11.2 stated risk, l.2557–2558 | 4,609 + 1,378 = 5,987 | 5,992 | — | yes (unchanged) |
| §11.3, l.2592–2593 | — | — | "60 days … in the expected branch (57.8 days plus the ≈ 2-day turnaround …); 58 days if the pause does not fire" | yes |
| §11.6, l.2679–2684 | 4,609 | 5,992 | 60 days (57.8 + ≈ 2) | yes |
| Gate A Q2 (a), l.2784 | — | — | "≈ 2 days of turnaround" | consistent with Q4 |
| Gate A Q4, l.2824–2836 | 4,609; MUST-only 4,176; full 5,123 | 5,992 | **60 days (57.8 without the day-15 pause)**; 59 (57); 60 (58) | yes |
| COM ST-1, l.209 | 4,609 | 5,992 | 60 days (57.8 + ≈ 2) | yes |
| COM v6 change row, l.34 | — | "unchanged" | 58 → 60 | yes |

**No mismatch.** The calendar shown in the summary, the schedule section, the Gate-A section and COM is 60 days with the
expected pause. 57.8 (or 58) is always stated with "without the pause" or "if the pause does not fire".

**The rider** (4,616 / 6,001, i.e. stdout 4,616.4 / 6,001.3) appears only in Q2 l.2802–2809, under the heading
"*Optional rider (… not part of the default; answer "Q2 ● + rider" to accept)*", and in the §13.5 history row. It does
not appear in §0, §11.2, §11.6, Q4 or COM (`grep rider COMMITMENTS.md` returns nothing). The Q4 default stays at
4,609 / 5,992. **The rider is nowhere treated as adopted.** VERIFIED.

---

## 4. Greps for superseded statements (v6 and COM)

| pattern | hits | classification |
|---|---|---|
| 4,574 / 5,946 | v6 l.2537 ("Version 4 had … an approved figure of 4,574 and a threshold of 5,946"), l.2965 (§13.3), l.2984 (§13.4); COM l.63 (version-5 change table) | all history, labelled "version 4 had" or change-table rows. **No live use.** |
| 57.6 | v6 l.2969, l.2984 (§13.3 / §13.4 history) | history |
| "57.8 days" | §11.2 l.2522 (with "(59.8 with the expected day-15 pause)"); §11.3 l.2592, §11.6 l.2680, COM l.34 / l.209 (all "57.8 days plus the ≈ 2-day turnaround"); §13.4 l.2984 history | never presented as the calendar to approve without the caveat. The §11.3 timeline ends at "51.8–57.8 … Gate C" without the pause, see C1 |
| 710 / 790 GeV | §0 l.77 ("≈ 710 GeV (790) if every no-pile-up ceiling counts zero, an upper edge that the strategy's own planning estimate does not expect"); Table 4.4c l.955 "(upper edge)"; Q2 l.2781 ("every ceiling empty, ≈ 710 GeV (median 790), an upper edge"), l.2800 (pool doubling, 790 → 814); l.180 is the plan arithmetic (710 events, μ₉₅/N 789.7); l.1733, l.2380–2381 are v1 μ₉₅ ratios | always an upper edge, never leading or expected. No live contradiction. |
| 470–500 | §0 l.73 and Q2 l.2778: the (α1) median, statistics-only | both sit in the "upper branches" / "Upside (statistics-only; with the width 0.17 the (α1) edge is ≈ 310–370 GeV)" context. Labelled; not the expectation. |
| "≈ 270" / "270 GeV" | l.70, l.105, l.2774, l.2788, l.2919: each followed or preceded by "statistics-only", "hold only for its counting width" or "only for a background with no width beyond its counting width"; l.2980 §13.4 history row R1 | **no live use without the normalisation-width statement** |
| "≈ 10⁴" / "10⁴ events" | l.60 (≈ 1.0×10⁴ events, a background size, with the rate clause); l.66, l.103, l.2770, l.2918 (≈ 0.7–1.0×10⁴, each followed by the width statement); l.2283 [L13] (a background size, no reach, "the result is a measured background"); l.200 (Table 2.1, SM sizes, unrelated); l.2980 history | no hit quotes the reach at 10⁴ events without the width. The [L13] and l.60 hits state a size, not a reach, and need no width clause. |
| "below the existing bounds" / "below existing" | 0 hits | the v5 §12.5 contradiction is gone. Every live statement is "at or near the existing bounds" (expected) or "stay above the existing bounds" (upper branches with w = 0.17), and these are consistent with each other |
| veto / "avoid" / "steeper" / "conversion-removing" | l.91–93, l.107, l.1013–1014, l.2779, l.2795–2797: each says that the veto or conversion removal alone does **not** avoid the pause. §4.6 l.1221 and l.1276–1280 define the veto, with no outcome claim. §4.4 B1 risk (3) l.1098 and §4.11 l.1652–1656 make no claim about the pause. | **no sentence implies that a conversion veto alone avoids the day-15 pause** |
| AV §9 list: "systematic width of 0.2", "270–390 GeV as above", "+25 GeV", "8 weeks (58 days)", "about 8 weeks from Gate A (58 days)", "0.04–0.06" | 0 hits each | clean |
| "58 days" / "57 days" | l.119 and l.2593 ("58 days without it" / "if the pause does not fire"); Q4 l.2835–2836 ("57 without the pause", "58 without") | labelled |

---

## 5. T1 and T2 wording against AV's exact text

Every location of the fix report §2 / §3 was compared word for word with AV §6.2 (see the hunk table in §1.1). The ordered
text is present in each location except for two departures. Both are justified by printed lines.

**Departure 1: script values replace AV's draft numbers.** At the N_trig-weighted rate, stdout l.331 and l.346 give the
counted B₅₀ 6,825 (×339) / 7,087 (×201) and the 84 % edges 297 / 293. AV's draft had 6,814 / 7,076 and 297 / 294. AV §6
says "My values are [E]; the script's are binding" and "Where my text quotes a printed value, the fixer copies the
printed value". The fixer did exactly that. The difference is 0.16 % in B₅₀ and 1 GeV in one edge, and it changes no
statement. AV's 6,814 equals the printed B₅₀ of the w = 0.17 row (l.335), which suggests that the draft mixed rows.
§0 point 3 rounds to "≈ 6.8–7.1×10³", which agrees with both.

**Departure 2: "already below 243 GeV at a width of 0.03" restricted to the 84 % edge.** At w = 0.03, stdout l.332 and
l.347 give a median reach of **281 and 280 GeV** at the 0.255 rate, which is above 243. The 84 % edge is "< 243.0" in all
four (tag × rate) rows (l.328, 332, 338, 347), and HEADLINE v6 (l.356) prints "already at w = 0.03: 84 % edge < 243.0".
AV's unqualified wording is therefore false for the median at the weighted rate, and the restriction is the correct
reading of the printed lines. AV §2 itself says "at 0.03 the 84 % edge is already below 243 GeV". The fixer applied the
restriction in §0 "Expected", in the Table 4.4c caption and in the scenario text. In the (α1′) reach cell (l.966) it kept
"(already at 0.03)" unqualified, and that is correct, because the row is labelled with the maximum rate 0.379, at which
the median is also below 243 (s₉₅ 641.1 / 644.3 > 621.5, l.327 / l.338). The unqualified 0.17 claim ("below 243 GeV")
holds at both rates for median and edge (l.330, 335, 340, 350). **Justified.**

**Numbers in the new T1/T2 text against printed lines** (all VERIFIED against `budget_stdout_v6.txt`):
- statistics-only 84 % edge 270–297 → "≈ 270–300";
- median 314–342 → "≈ 315–340";
- fixed B 392–419 → "≈ 390–420";
- (α1) with w = 0.17, 84 % edge 372 / 312 → "≈ 310–370" and "372–312";
- statistics-only (α1) edge 455 / 421 → "instead of 420–455";
- m_H = 100: 454 [523] (l.354);
- (α1) no-credit B₅₀ 587 / 975, DIF 385 / 647, credit 51 / 74 (l.352, l.357);
- rejection ×52.1 / ×31.0 (98.1 % / 96.8 %) → "×31–52 (96.8–98.1 %)";
- s₉₅ 621.5 ↔ 243 GeV (l.326);
- 790 → 814 (unchanged [9b] line, cited).

No number in the changed text lacks a printed source.

---

## 6. The Gate-A section (§12.1)

- **Self-contained.** The preamble states the answer format ("Q1 ●; Q2 ●; …"), what ● means, the CPU-h and days source,
  and that every reach is EST with v1 placeholder efficiencies. Each question has a stem, the default ●, the alternatives
  and their costs. Q1: 14 CPU-h in every option. Q2: (a) ≈ 2 days, the reserve spent by rule 3(b); (b) 0 CPU-h, no
  delay, no reach beyond the existing bounds in the expected case; (c) time not estimable now, CPU-h inside the
  allowance and the reserve, and the success condition ×31–52 plus DIF. The rider costs +7.0 CPU-h. Q3: ≈ +680 CPU-h,
  ≈ +3.9 days, or strict. Q4: 4,609 / 5,992 / 60 days, with the envelope, MUST-only and full alternatives. Q5: 0 days,
  or +47 CPU-h and +1.8 days. A reader can answer all five without opening another section. The cross-references
  (Table 4.4c, §11.7, the annex) are pointers to more detail, not prerequisites. Q2's stem is long, which is the
  constructive reviewer's scope; it is not a defect of completeness.
- **"One line each."** This refers to the answer ("one line each as an answer"), and every question admits a one-token
  answer. The rider is answerable in the same token ("Q2 ● + rider").
- **Pointer to the stop rules.** Present in Q4 l.2830–2831 ("the stop conditions of brief §7 are quoted in §11.6") and in
  §0 l.124.
- **Stop conditions against brief §7.** §11.6 l.2667–2674 matches `prompt.md` l.341–348 word for word, all six bullets,
  and l.2676 matches D6 at l.79 (VERIFIED, read both). The application (l.2679–2694) uses the approved CPU-h for the 30 %
  rule (5,992) and reports every overrun of either CPU-h or calendar. This is consistent with "projected compute" in the
  brief. The T3 calendar change does not alter the stop threshold, as COM l.34 states ("CPU-h and threshold unchanged").

---

## 7. Category C items (for the Gate-A package; none blocks)

- **C1. The §11.3 timeline (l.2562–2575) and the §11.7 decision-point table (l.2704, "Gate B at ≈ 49") are on the
  no-pause basis without saying so.** Gate C appears at day 57.8, while the calendar sentence directly below and Q4
  approve 60. A reader is not misled at Gate A, because the next sentence explains. One caption clause would close it:
  "days without the day-15 pause; in the expected branch every day after 15 moves by ≈ 2". This was not ordered by AV.
- **C2. The range figures are on the no-pause basis, next to a headline that includes the pause.** §0 l.119–120 and §11.3
  l.2596 give "49 days if every review passes at once and only MUST items run; 65 days at 50 % utilisation" (stdout
  l.204 48.9; l.202 64.9). With the expected pause these would be ≈ 51 and ≈ 67. Either state the basis or add 2.
- **C3. §11.6 l.2654: "The target is missed by about four weeks"** was written for 58 days. At 60 days it is 32 days
  beyond the 4-week end of D6 (≈ 4.6 weeks), so "four to five weeks" is the better reading. It changes no decision.
- **C4. Rider part (3), "1,000 γ development overlays", sits beside the already booked "1,000 unbiased Geant4 DIF
  development overlays" (+7.0 CPU-h, P4; §11.2 l.2530, §11.3 l.2565).** These have the same size, the same cost and a
  similar name. Three words would rule out the reading that the rider is already in the schedule: "in addition to the
  1,000 DIF overlays of P4".
- **C5. Fix report §6 says "30 added lines".** The stdout diff has 29 added lines plus one changed line (30 `>` lines).
  This affects the report only; the artifact is unaffected.

---

## 8. Statement

**No Category A or Category B item remains** within the scope that AV §9 assigns to the critical reviewer:
- T3 is resolved in every location: §0, §11.2, §11.3, §11.6, Q4 and COM ST-1, plus Q2 (a), which is consistent with them.
- Every v5 → v6 hunk of the strategy (30), COM (4) and the script (4) is attributed to T1–T3, an AV §6.3 C item, the
  rider or the general rules. The one extra change (58.9 / 60.1 in §11.2) is justified and was expected by AV §9.
- The script reproduces `budget_stdout_v6.txt` exactly, and every v5 value is unchanged.
- The greps find superseded figures only in labelled history rows, and no live contradiction.
- The T1/T2 text is the ordered text, with two departures that the printed lines justify.
- The Gate-A section is complete, and its stop rules match brief §7.

New items: A 0, B 0, C 5 (C1–C5).
