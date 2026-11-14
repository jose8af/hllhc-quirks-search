# Fix report, review cycle 5 (fixer Ingrid, 2026-11-14 02:20)

Verdict: `review/arbiter/STRATEGY_ARBITER_v5_hugo_2026-11-14_01-55.md` (ITERATE, 0 A, 3 B: T1–T3; C items of its §6.3;
H-C1 as an optional Gate-A rider, §7).
Outputs: `outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("v6", `cp` of v5 then targeted edits; v5 unchanged),
`QV2/COMMITMENTS.md`, `src/strategy_budget.py`, `outputs/budget_stdout_v6.txt`.
Run: `nice python3 -I src/strategy_budget.py` (standard library, einstein, 38 s). No git, no sub-agents, no CPU beyond
that run.

## 1. Script values that differ from the verdict's draft numbers (script binds)

| quantity | verdict draft [E] | script (v6 lines) | used in v6 |
|---|---|---|---|
| (α1′) rate 0.255, B₅₀ ×339 / ×201 | 6,814 / 7,076 | 6,825 / 7,087 | 6,825–7,087 (Table 4.4c row); "≈ 6.8–7.1×10³" (§0 point 3) |
| (α1′) rate 0.255, 84 % edge ×201 | 294 | 293 | "[297–293]" (Table 4.4c row) |
| (α1′) rate 0.255, w = 0.17, s₉₅ median | 1,819 / 1,834 | 1,822.5 / 1,837.7 | not quoted (only "< 243") |
| (α1′) rate 0.255, w = 0.03 | median 281 / 280 [< 243] | the same | the text says "its **84 % edge** is already below 243 GeV at a width of 0.03": at rate 0.255 the median at w = 0.03 is 281 / 280 GeV, so the verdict's unqualified "already below 243 GeV at 0.03" holds only for the 84 % edge at both rates (and for the median at the maximum rate). Applied in §0 "Expected", Table 4.4c caption ("(84 % edge)") and the scenario text. |

Every other value of the verdict's §6.1 is reproduced exactly: rate 1, w = 0.03 s₉₅ 641.1 / 644.3; w = 0.17 2,697.4 /
2,725.3 (84 %: 4,193.4 / 4,204.1); rate 0.255 median 342 / 338, 84 % 297, fixed B 419 / 416; (α1) with w = 0.17
median 429 / 369 [372 / 312]; m_H = 100 513 [454]; rejection ×52.1 / ×31.0 (98.1 % / 96.8 %); calendar 59.8 / 58.9 /
60.1; rider 7.0 CPU-h, 4,616.4 / 6,001.3.

Method notes (verifiable in the script): the conversion term of (α1′) enters `lnn` as `(g, sqrt(w² + 1/(m + 1)), None)`
with m = g/kz (median g); DIF counted, `kap_nodif` and `PU9` unchanged. (α1) with w = 0.17: DIF and conversions both as
`(B_t, sqrt(0.17² + 1/(m_t + 1)), None)`, m = B/κ. Z(νν) m_H = 100: median kz (m + 1), as the verdict writes (median
kz·m gives the same 513 [454]). "Decays in flight alone" is printed both as the DIF term (385 / 647) and as the B₅₀ of
the (α1) row with the conversions removed (floors + pile-up + DIF counted: 401 / 663); the text quotes the verdict's
385–647.

## 2. Status per finding

| item | status | section heading(s) in v6 | grep phrase (unique to v6) |
|---|---|---|---|
| **T1** (a) leading sentence | RESOLVED | ## 0. Summary, "Leading sentence" | `hold only for its counting width alone` |
| T1 (b) §0 Expected | RESOLVED | ## 0. Summary, "Expected" | `hold only for the counting width of ≈ 0.02` |
| T1 (b) upper branches | RESOLVED | ## 0. Summary, "Expected" | `These upper branches are statistics-only in the same sense` |
| T1 (c) §0 point 3 | RESOLVED | ## 0. Summary, point 3 | `0.04–0.07 counts at R07`; `≈ 6.4×10³ conversions and B₅₀ ≈ 6.8–7.1×10³` |
| T1 (d) Table 4.4c | RESOLVED | ### 4.4, Table 4.4c caption and (α1′) row | `*Statistics-only:* the`; `< 243 with the planned normalisation width 0.17 (already at 0.03)`; `B₅₀ 6,825–7,087, reach 342–338 [297–293]` |
| T1 (e) scenario text | RESOLVED | ### 4.4, *Scenario (α)* | `the branch the v1 conversion record supports, with the more favourable DIF`; `The term carries the normalisation nuisance of its SM processes` |
| T1 (f) Q2 stem | RESOLVED | ### 12.1, Q2 | `≈ 0.7–1.0×10⁴ background events at the R08–R09`; `may be ×5–50 above this figure` |
| T1 (g) Q2 (b) | RESOLVED | ### 12.1, Q2 option (b) | `this paper reports no mass reach beyond the existing bounds` |
| T1 §12.5 point 3 | RESOLVED | ### 12.5, point 3 | `it is ≈ 270–300 GeV at the 84 % edge statistics-only` |
| T1 script | RESOLVED | script [9b] | stdout `v6 (T1)`, `HEADLINE v6 (T1)` |
| **T2** (a) §0 pause | RESOLVED | ## 0. Summary, "The pause." | `The pause fires in the first upper branch too` |
| T2 (b) §4.4 | RESOLVED | ### 4.4, *What is not known* | `removing the conversions alone does not bring B₅₀ below 300` |
| T2 (c) Q2 stem | RESOLVED | ### 12.1, Q2 | `so a conversion veto alone does not avoid the pause` |
| T2 (d) Q2 (c) | RESOLVED | ### 12.1, Q2 option (c) | `It works if the projected B₅₀ is at most 300` |
| T2 script | RESOLVED | script [9b] | stdout `v6 (T2) day-15 class limit` |
| **T3** §0 | RESOLVED | ## 0. Summary, Calendar | `of which ≈ 2 are the expected day-15 pause` |
| T3 §11.2 | RESOLVED | ### 11.2 table | `57.8 days = 8.3 weeks (59.8 with the expected day-15 pause)` (and 58.9 / 60.1 on the other two rows, see §5) |
| T3 §11.3 | RESOLVED | ### 11.3 | `60 days from Gate A in the expected branch` |
| T3 §11.6 | RESOLVED | ### 11.6 | `and 60 days (57.8 days plus the ≈ 2-day` |
| T3 Q4 | RESOLVED | ### 12.1, Q4 | `**60 days** (57.8 without the day-15 pause`; `59 days (57 without the pause)`; `60 days (58 without)` |
| T3 COM ST-1 | RESOLVED | COM ST-1 row | `and 60 days (57.8 days plus the ≈ 2-day turnaround` |
| T3 script | RESOLVED | script [7] | stdout `v6 (T3): expected branch under Q2 (a)` |
| H-C1 rider | RESOLVED (as optional rider, not default) | ### 12.1, Q2 | `*Optional rider (recommended by the cycle-5 review`; stdout `H-C1 rider (if accepted at Gate A)` |
| Cr-C1 | RESOLVED (in T1 §12.5) | ### 12.5 | as T1 §12.5 |
| Cr-C2 | RESOLVED | header "Tags"; ### 12.2 | `Fiona, Gunnar or Ingrid, whoever wrote it`; `(entries [Ingrid] and [Gunnar] for the last two versions` |
| Cr-C3, Ph-C1 | RESOLVED (rate range in T1) | §0, Table 4.4c, Q2 | `v1's N_trig-weighted and maximum photon rates` |
| Cr-C4 | RESOLVED (T1-c) | §0 point 3 | `0.04–0.07` |
| Cr-C5 | RESOLVED (T3 Q4) | ### 12.1, Q4 | `the stop conditions of brief §7 are` |
| Cr-C6, H-C2, H-C5 | RESOLVED (T1-f) | ### 12.1, Q2 | `a fall of ×6.5 per width step against` |
| Ph-C2, H-C4 | RESOLVED (T2-d) | ### 12.1, Q2 (c) | `conversions reduced by ×31–52 (96.8–98.1 %)` |
| H-C3 | RESOLVED (T1-g) | ### 12.1, Q2 (b) | as T1 (g) |
| Ph-C4 (wording part) | RESOLVED (T1-e) | ### 4.4 | as T1 (e) |
| Ph-C5 | RESOLVED | ## 7. Label index, [L13] | `the leading term is a counted background of ≈ 10⁴ events` |
| H-C6 | RESOLVED | ### 12.1, Q2 last sentence | `median 790 → 814 GeV, script [9b]` |
| H-C7 | RESOLVED (T3 Q4) | ### 12.1, Q4 | `[DP1]` + `(B5 sideband reduced, §4.8)` |
| H-C9 | RESOLVED | script [4] | stdout `  approved figure = total + day-15 reserve` |
| H-C10 | RESOLVED | ### 11.7, rule 1 | `it is conditional on C1` |
| Left for later (verdict §6.4) | not touched | — | Ph-C3, Ph-C4 downside, H-C8, Cr-C7 |

Superseded phrases, grep in v6 (should return only the §13.4 history row or nothing): `systematic width of 0.2` → 0;
`270–390 GeV as above` → 0; `+25 GeV` → 0; `8 weeks (58 days)` → 0; `about 8 weeks from Gate A (58 days)` → 0;
`0.04–0.06` → 0; `≈ 10⁴ events, ≈ 270 GeV` → 1 (§13.4 history row R1).

## 3. Where the expected-outcome statement appears in v6 (all aligned)

| location | phrase |
|---|---|
| ## 0. Summary, point 3 | `≈ 6.4×10³ conversions and B₅₀ ≈ 6.8–7.1×10³ with its N_trig-weighted rate` |
| ## 0. Summary, "Expected" | `With a width of 0.17 the reach is below the plan's` … `hold only for the counting width of ≈ 0.02` |
| ## 0. Summary, upper branches | `These upper branches are statistics-only in the same sense` (710–790 GeV is the upper edge) |
| ## 0. Summary, "The pause." | `The pause fires in the first upper branch too`; `at or near the existing bounds with the planned width` |
| ## 0. Summary, leading sentence | `the reach is below 243 GeV, at or near the existing bounds of ≈ 180 GeV` |
| ### 4.4, Table 4.4c (per-outcome table) caption and (α1′) row | `*Statistics-only:*`; `< 243 with the planned normalisation width 0.17` |
| ### 4.4, *Scenario (α)* | `with it the reach of (α1′) is below 243 GeV` |
| ### 4.4, *What is not known* | `**The day-15 pause` … `removing the conversions alone does not bring B₅₀ below 300` |
| ### 4.11 point 3 (unchanged; no number) | `by v1's conversion counts the expected branch is a measured background, §0, Q2` |
| ## 7, [L13] | `the result is a measured background (§12.5 point 3)` |
| ### 11.7 rule 1 (decision rules; unchanged sentence, no number) | `this is the expected branch; what follows is Q2` |
| ### 12.1 Q2 stem | `the reach is below 243 GeV, at or near the existing bounds;` |
| ### 12.1 Q2 (b) | `expected below 243 GeV, at or near the existing bounds` |
| ### 12.1 Q2 (c) | `It works if the projected B₅₀ is at most 300` |
| ### 12.1 Q4 | `under the recommended Q2 (a) the pause is the expected branch` |
| ### 12.5 point 3 (how the study could fail) | `With the planned normalisation width (≈ 0.17) the` |
| ### 13.5 (history) | `T1 normalisation width` row |
| COM TG-1 (unchanged; no number) | `by v1's conversion counts the expected branch is a measured background, STR §0, Q2` |
| COM ST-1 | `and 60 days (57.8 days plus the ≈ 2-day turnaround of the expected day-15 pause` |

Every reach figure in the changed text sits inside a paragraph, caption or question that carries "ESTIMATE, v1
placeholder efficiencies" (§0 "Expected" heading, leading sentence, Table 4.4c caption, scenario (α) text, Q2 stem,
§12.5 point 3; Q2 (b), (c) and the rider are under the Q2 stem and the §12.1 preamble "Every reach number is EST").

## 4. diff --stat

```
STRATEGY_gunnar_2026-11-14_00-50.md => STRATEGY_ingrid_2026-11-14_02-20.md | 169 ++++++++++++++-------
 1 file changed, 116 insertions(+), 53 deletions(-)
analyses/quirks_v2/COMMITMENTS.md                  | 15 ++--
.../phase1_strategy/src/strategy_budget.py         | 83 +++++++++++++++++++++-
```

## 5. Hunk-by-hunk attribution (`diff v5 v6`; 30 STR hunks, 4 COM hunks, 4 script hunks; 0 unattributed)

STR (v5 line numbers → v6):

| # | hunk | where | attribution |
|---|---|---|---|
| 1 | 1c1 | title "version 6" | general rule (§6: write v6) |
| 2 | 3,5c3,5 | fixer header, replaced file, verdict | general rule |
| 3 | 7c7 | "verification (cycle 6)" | general rule |
| 4 | 16c16 | author list | Cr-C2 |
| 5 | 58c58 | 0.04–0.07 | T1-c (Cr-C4) |
| 6 | 60c60,61 | rate clause | T1-c (Cr-C3, Ph-C1) |
| 7 | 65,67c66,72 | §0 Expected | T1-b |
| 8 | 74c79,81 | upper branches statistics-only | T1-b (arbiter Case 5) |
| 9 | 83,85c90,95 | §0 The pause | T2-a |
| 10 | 93,94c103,107 | leading sentence | T1-a |
| 11 | 106c119 | §0 Calendar | T3 |
| 12 | 933c946,950 | Table 4.4c caption | T1-d |
| 13 | 949c966 | (α1′) row | T1-d |
| 14 | 962c979,980 | scenario "v1 conversion record" | T1-e (Ph-C4 wording) |
| 15 | 974c992,994 | scenario statistics-only sentence | T1-e |
| 16 | 993c1013,1014 | What is not known | T2-b |
| 17 | 2261,2262c2282,2284 | [L13] | Ph-C5 |
| 18 | 2499,2501c2521,2523 | §11.2 table, three rows | T3 (proposed row ordered; MUST-only and full rows given 58.9 / 60.1 so that the §11.2 table agrees with the Q4 alternatives the verdict orders, "59 days (57 without)", "60 days (58 without)"; neighbourhood check) |
| 19 | 2570c2592,2593 | §11.3 calendar estimate | T3 |
| 20 | 2657c2680,2681 | §11.6 approved schedule | T3 |
| 21 | 2697c2721,2723 | §11.7 rule 1 C′₀ condition | H-C10 |
| 22 | 2744,2751c2770,2782 | Q2 stem | T1-f / T2-c (H-C2, H-C5, Cr-C6) |
| 23 | 2756,2757c2787,2791 | Q2 (b) | T1-g (H-C3) |
| 24 | 2761c2795,2797 | Q2 (c) | T2-d (H-C4, Ph-C2) |
| 25 | 2764c2800,2809 | Q2 last sentence + rider | H-C6; rider (verdict §7) |
| 26 | 2780,2782c2825,2831 | Q4 calendar, DP glosses, §11.6 pointer | T3; H-C7; Cr-C5 |
| 27 | 2786,2787c2835,2836 | Q4 alternatives | T3 |
| 28 | 2837c2886 | §12.2 entries | Cr-C2 |
| 29 | 2867,2870c2916,2920 | §12.5 point 3 | T1 (Cr-C1) |
| 30 | 2935a2986,2998 | §13.5 Changes since v5 | general rule (orchestrator: change table) |

COM: (1) l.3–4 current strategy → v6; (2) l.6 version 5 in the list of earlier versions (general rule, as in each
cycle); (3) new "Changes of rows in version 6" table (general rule); (4) ST-1 calendar clause (T3). No status changed;
nothing dropped; TG-1 unchanged (it states no changed quantity).

Script: (1) l.299 label "approved figure" (H-C9); (2) after l.432, [7] T3 line + rider line (§6.1 items 2, 3);
(3) after l.772, [9b] v6 (T1) block and v6 (T2) lines (§6.1 item 1); (4) after l.795, HEADLINE v6 (§6.1 item 1, last
bullet).

## 6. Script outputs: `diff budget_stdout_v5.txt budget_stdout_v6.txt`

One changed line (the H-C9 label; its value 156.5 is unchanged) and 30 added lines; no v5 value changed.

```
121c121
<   v4 approved figure = total + day-15 reserve 156.5 CPU-h (P13):
---
>   approved figure = total + day-15 reserve 156.5 CPU-h (P13):
204a205,206
>   v6 (T3): expected branch under Q2 (a): + 2.0 d day-15 pause turnaround (the Gate-B turnaround) -> MUST + SHOULD reduced 59.8 d = 8.5 weeks; MUST-only 58.9; full 60.1 (without the pause: 57.8 / 56.9 / 58.1)
>   H-C1 rider (if accepted at Gate A): 1,000 gamma development overlays 1000 x 25.2 s = 7.0 CPU-h, added: approved 4616.4 CPU-h, threshold 1.3 x 4616.4 = 6001.3 (default 4609.4 / 5992.2); calendar unchanged (idle pre-freeze capacity 1351 core-h); the veto measurement on the stored pilot records and the day-7 question 0 CPU-h
323a326,351
>   v6 (T1): ... (26 lines: (α1′) ×339 / ×201 at the max and N_trig-weighted rate, counted and w = 0.03 / 0.05 / 0.17;
>   (α1) and Z(νν) m_H = 100 with w = 0.17; v6 (T2) class-limit lines; see budget_stdout_v6.txt l.326–351)
327a356
>   HEADLINE v6 (T1): (alpha1') no credit, photon rate 0.255-0.379: B50 6825-10193; with the normalisation width 0.17: s95 median 1823-2725 -> reach < 243.0 GeV (already at w = 0.03: 84 % edge < 243.0); statistics-only (count width): 84 % edge 270-297, median 314-342, fixed B 392-419; (alpha1) with w = 0.17: 84 % edge 312-372, median 369-429; Z(nunu) m_H = 100 with w = 0.17: 84 % edge 454
```

## 7. Neighbourhood checks

- Every other statement of the expected-branch background or reach in v6 grepped (`10⁴`, `270`, `315`, `390`,
  `200 GeV`, `existing bounds`, `avoid`, `expected branch`, `real background`): the remaining hits are history (§13.4),
  unrelated quantities (Table 2.1 SM sizes, 200 GeV generator cut) or unchanged sentences without numbers (§4.4 B1
  risks (3), §4.11 point 3, §11.7 rule 1), which agree with the new statement.
- Calendar chain 59.8 / 58.9 / 60.1 (57.8 / 56.9 / 58.1 without): §0, §11.2 (three rows), §11.3, §11.6, Q4, COM ST-1.
- The day-7 / day-15 class limit 300 and the (α1) credit B₅₀ 51–74 in T2 text match stdout [9b].

## 8. Not done, proposed

- Code reference: "about ten seconds" is now ≈ 38 s (already noted by Gunnar; not ordered).
- The §4.4 "decades below v1" sentence does not list (α1′) (carried from cycle 4; not ordered).
- Whether Phase-3 channels continue during the day-15 pause (verdict §6.4 last row; Gate-A package).
