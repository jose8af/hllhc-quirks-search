# Fix report, review cycle 4 (fixer Gunnar, 2026-11-14 00:50)

Work list: `review/arbiter/STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md` (ITERATE, 0 A, 5 B: R1–R5, and the C items
of its §6). Artifacts: `outputs/STRATEGY_gunnar_2026-11-14_00-50.md` (v5, from a `cp` of v4, which is unchanged),
`QV2/COMMITMENTS.md`, `src/strategy_budget.py`; script outputs `outputs/budget_stdout_v4.txt` (the unmodified script)
and `outputs/budget_stdout_v5.txt`. Rules: files and `python3 -I` only, no git, no sub-agents, nothing outside
`phase1_strategy/` and `COMMITMENTS.md`. Every grep phrase below is a literal substring of v5 (or COM / the script).

## 1. Status per finding

| item | status | where (section) | grep phrase |
|---|---|---|---|
| **R1** honest headline | **RESOLVED** | §0 point 3, "Expected", leading sentence; §4.4 point 4 (Df-9 EST), point 5 (pilot reading); Table 4.4c; scenario text; "What is not known"; §4.11 point 3; §11.7 rule 1; Q2; §12.5 points 2–3; script [9b] | "≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge"; "(α1′) therefore takes the conversions at their own fall"; "this is the expected branch; what follows is Q2"; "**Q2, the deliverable if the background is large (the expected case).**"; "no fit-probability credit"; "m_H ≈ 1.6×10³ for Z(νν)"; "Read as a log-normal width instead"; "statistics-only: at σ_ln = 0.2"; "(1e5, 243.0)" (script) |
| **R2** Q3 annex | **RESOLVED** | Q3 answer text and annex | "**route 5: promotion model not submitted**"; "**route 6: S_CKF NOT TESTED**"; "**B4-e, size** (in route 3)"; "a B4-e failure alone sets a floor of ≈ 4.6×10³ events"; "Reach under the default: (β) of Table 4.4c" |
| **R3** pilot before its code | **RESOLVED** | §4.4 point 5; §4.4 point 4 (per-k comparison); B1 storage; §11.3 row 5–17; §11.4; §11.7 inputs and rule 1; §0 storage; script [8] | "The pilot's no-pile-up jobs keep the full hit records"; "classified provisionally by day 7 and finally by day 12"; "at the latest by day 14"; "classification of the pilot's records (by day 7)"; "the v1-based EST pile-up rows of Table 4.4c" |
| **R4** S_CKF samples | **RESOLVED** | §4.4 point 4 *S_CKF (Df-9)*; Df-9; COM B1-f | "test overlays with their weights, derivation R04–R05, test R06 and R07 where evaluable"; "the restriction to unbiased samples applies to the ceiling and leak tests only"; "DIF R06 on the enriched overlays, NI R05 by the rung split, SM R06" |
| **R5** eleven processes | **RESOLVED** | script [3], [5″]; §0 cost; §4.0 point 6; §4.4 point 4 (ii); §4.7 cost; §4.17 row 20; §11.1; §11.2; §11.3; §11.6; Q4; COM B1-f, B4-c, ST-1 | "each of the fifteen SM processes"; "For SM processes H′ may exceed H by orders of magnitude"; "**4,609 CPU-h, the approved figure proposed in Q4**"; "**5,992 CPU-h**"; "57.8 days = 8.3 weeks" |
| G-C1 | RESOLVED | §0 Cost | "MUST items: **4,019 CPU-h**"; "4,966 CPU-h (5,123 with the reserve)" |
| G-C2 | RESOLVED | Df-10; COM T1-h | "family-wise 4.7–4.9 %"; COM "family-wise false FAIL 4.7–4.9 %" |
| G-C3 | RESOLVED | COM REF-2 | "R-10 and R-20 before Phase 4a" |
| G-C4 | RESOLVED | §4.7 statistics | "Of the four\nterms sized at an expected 31 counts" (grep "terms sized at an expected 31 counts") |
| G-C5 / Ph-C4 | RESOLVED | §4.4 after Table 4.4a | "(planning number, [U])"; "with the multijets at 1 % it is 2.1 %" |
| G-C6 | RESOLVED | §4.4 after Table 4.4a | "`n_trig.not_included` [U]" |
| G-C9 | RESOLVED | §4.7 (B4-c); §11.7 rule 4; COM B4-c | "on its derivation parity half" / "derivation parity half (so the test half is not looked at" |
| G-C11 | RESOLVED | COM S1-a (deadline 4a → 4b) | COM row S1-a ends "| 3 (string) / 4a (chain) | 4b | open |" |
| G-C14 | RESOLVED | §2 (B1-g paragraph); script [13] label | "`s4cp.py` l.115"; "1.5687 for WZ"; script "1.5687 (WZ; v5, G-C14)" |
| N-C1 | RESOLVED | Q4 | "43.5 days have no\ncritical-path production" (grep "critical-path production: development and freeze 19") |
| N-C4 | RESOLVED (in Q2) | Q2 option (a) | "≈ 2 days of turnaround" |
| N-C6 | RESOLVED | Df-8 | "chosen up front: +156 CPU-h" |
| N-C11 | RESOLVED | §11.3 table | "| 51.8–57.8 | 5 |" |
| Ph-C7 | RESOLVED | §4.7 multijets | "a FAIL is charged to the factorisation first" |
| Ph-C1, Ph-C2, Ph-C5, G-C10, N-C7 (in R1); N-C5 (in R2); N-C9 (this report) | RESOLVED | Table 4.4c, §0, Q2, Q3 | "(at its floor); conditional on the promotion model"; "m_H = 1000 (≈ 2,300 events)"; "v1's **pile-up** fit-probability fraction 2/35"; "fixed B, an upper edge of the reach"; "the search for newer results, R-20," |

Not adopted by the verdict and not touched: G-C7, G-C8, G-C12, N-C3, G-C13, G-C15, Ph-C6, N-C2, N-C10, N-C8.

**Leading headline sentence (§0, as it now stands):** "**Expected (ESTIMATE, v1 placeholder efficiencies): by v1's own
counts the default plan's background at R08–R09 is led by hard-scatter conversions, ≈ 10⁴ events, with a reach of
≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if the background were known exactly), and the day-15 rule is
expected to pause the study before production.**"

Wording note: the verdict's text says "EST, v1 placeholder efficiencies"; the orchestrator required every reach figure
to carry "ESTIMATE, v1 placeholder efficiencies". I wrote "ESTIMATE" (the long form of the same tag, §0 "Tags") in the
leading sentence, the "Expected" paragraph, Q2, the Q3 reach clause, §12.5 and the scenario text; otherwise the §5.1,
§5.2 and §7 texts are verbatim except for printed values.

## 2. Script values against the verdict's drafts (script binds)

All agree within rounding except as marked.

| quantity | verdict draft | printed (v5) | used |
|---|---|---|---|
| (α1′) no credit B₅₀ | 9.9×10³–1.02×10⁴ | 9,929–10,193 | ≈ 10⁴ |
| (α1′) s₉₅ median [84 %] | 352–361 [495–505] | 352.2–360.6 [494.7–505.3] | 352–361 |
| (α1′) reach median [84 % edge] | 317–314 [273–270] | 317–314 [273–270] | ≈ 315 [≈ 270] |
| (α1′) fixed B | 394 / 391 | 394 / 392 | ≈ 390 (394–392) — **differs by 1 GeV in the ×201 case** |
| (α1′) with credit | B₅₀ 580–600, 332–331 [250] | 580–599, 332–331 [250] | as printed |
| (α1) × e^(−1) / e^(+1), median | 571–535 / 437–400 | 571–535 / 437–400 | as printed |
| (α1) × e^(+1), 84 % edge | "below 393" | **390 / 355** (the 10⁵ column now maps it) | 390–355 |
| (α1) log-normal reading | "[printed value]" | median 262 (×339) / < 243 (×201); 84 % edge < 243 | as printed |
| m_H = 1000 with count width | B₅₀ 2,299, s₉₅ 168, 415 | B₅₀ 2,299 (2,229 / 2,373), s₉₅ 168.1 [118.6, 236.7], 415 [369] | as printed |
| (α2) no credit (fixed B) | "printed value" | 262 GeV | 262 |
| (α2) with credit | — | < 243 | "below 243" |
| P(≥ 2 at R07 \| pile-up fall from 13) | 7.2×10⁻⁴ / 2.0×10⁻³ | 7.2×10⁻⁴ / 2.0×10⁻³ | as printed |
| P(≥ 13 at R06 \| from 86) | < 10⁻¹⁴ | 2.3×10⁻¹⁸ / 1.7×10⁻¹⁵ | not quoted in v5 text |
| P(≥ 1 DIF) | 0.6 / 1.0 % | 0.59 / 0.99 % | "≈ 1 %" |
| Z(νν) conversion m_H at R08 | ≈ 1.6×10³ (pilot ≈ 3×10²) | 1.56×10³ (pilot 326) | as verdict |
| R5 row | 35.75 | 35.78 (11,000 × 11.71 s) | 35.8 |
| approved (reduced + reserve) | 4,609.4 | 4,609.4 → **4,609** | 4,609 |
| threshold 1.3× | 5,992; MUST only 5,429; full 6,660 | 5,992; 5,429; 6,660 | as printed |
| all guesses doubled | 5,987 | 5,987 | 5,987 ("just below" the threshold; v4 said "just above") |
| critical path, calendar | 2,489 CPU-h = 14.3 d; 57.8 / 56.9 / 58.1 d | same | as printed |
| contingency; envelope | — | 2,150; 4,609 + 2,150 = 6,759, threshold 8,787 | as printed |
| storage | "if rounding moves" | 417 → 469 GB (617 → 669) | "≈ 470 (670)" |

## 3. Changed numbers (old → new, why)

| number | old (v4) | new (v5) | why |
|---|---|---|---|
| leading reach | 710 [84 %] (790) | ≈ 270 [84 %] (315; ≈ 390 fixed B) | R1 |
| pessimistic branch | 470–500 (median, unlabelled) | 420–455 (470–500) as an upper branch | R1 (a) |
| m_H = 1000 row | ≈ 96 (fixed B), ≈ 490 | 168 [119, 237], 415 [369] | R1 / Ph-C2 |
| (α2) reach | "below 393" | 262 (fixed B, upper edge); below 243 | R1 (h) |
| MUST / reduced / full | 3,984 / 4,417 / 4,930 | 4,019 / 4,453 / 4,966 | R5 |
| approved (reduced / full / MUST only) | 4,574 / 5,087 / 4,140 | 4,609 / 5,123 / 4,176 | R5 |
| thresholds | 5,946 / 6,613 / 5,382 | 5,992 / 6,660 / 5,429 | R5 |
| Phase 4a MUST; B4 | 2,701; 1,072 (1,150 total) | 2,737; 1,108 (1,186) | R5 |
| 4a totals | 3,648 / 3,135 | 3,684 / 3,171 | R5 |
| critical path | 2,297 / 2,453 / 2,507 CPU-h = 13.2 / 14.1 / 14.4 d | 2,333 / 2,489 / 2,542 = 13.4 / 14.3 / 14.6 d | R5 |
| calendar | 56.7 / 57.6 / 57.9 d; 8.2 weeks | 56.9 / 57.8 / 58.1 d; 8.3 weeks ("58 days", "57 days", "≈ 8 weeks", "49", "65" unchanged) | R5 |
| §11.3 day markers | 35, 36.5, 39.5, 41.5, 44.5, 48.5, 51.5, 57.5 | 35.3, 36.8, 39.8, 41.8, 44.8, 48.8, 51.8, 57.8 | R5 + N-C11 |
| provenance M; contingency | 717; 2,146 | 753; 2,150 | R5 (M-provenance row) |
| guesses doubled | 5,952 ("just above") | 5,987 ("just below") | R5 |
| envelope | 4,574 + 2,146 = 6,720 (8,736) | 4,609 + 2,150 = 6,759 (8,787) | R5 |
| §11.6 "about 5,950" | 5,950 | 5,990 | R5 |
| production days in §11.6 | 13.2–14.4 | 13.4–14.6 | R5 |
| Argo jobs | ≈ 11,000, 52 slot-h | ≈ 11,100, 53 slot-h | R5 |
| storage | ≈ 420 (620) GB | ≈ 470 (670) GB | R3 (+51.7 GB pilot records) |
| review additions in Q4 | 39 CPU-h | 39 + 36 = 75 CPU-h | R5 |
| B4 paired pass cost | 13 (4,000 events) | 49 (15,000 events) | R5 |
| B1-g DIF minimum | 1.569 (Z(νν) in the script label) | 1.5687 (WZ) | G-C14 |
| T1 family-wise | 4.7 % (Df-10), ≈ 5 % (COM) | 4.7–4.9 % | G-C2 |

Propagation counts: 4,574 → 4,609: 7 current-value instances in v5 (§0, §11.2 table ×2, §11.2 contingency, §11.6,
Q4 ×2 incl. the envelope) plus the §13.4 row, and 2 in COM (ST-1 row, v5 change table); 5,946 → 5,992: 5 current-value
instances in v5 (§0, §11.2 table, §11.2 contingency, §11.6, Q4) plus §13.4, and 2 in COM; 57.6 → 57.8: 1 current
value (§11.2 variants table) plus the §11.3 table end (57.8) and §13.4 (§0, §11.3 text and Q4 say "58 days").
Superseded values remaining (all history, §11.2 "Changes against version 4", §13.3, §13.4 and the COM v4 change
table): 4,574 — v5 3, COM 1; 5,946 — v5 3, COM 1; 57.6 — v5 2, COM 0; 710 as a leading figure — 0 (2 remaining
occurrences are the "every ceiling empty" upper branch, §0 and Q2; 1 unrelated v1 arithmetic in §1); 790 — only as
that branch's median and unrelated v1 numbers; 470–500 as the pessimistic branch — 0 (2 remaining are the (α1) upper
branch median, §0 and Q2); "realistic branch" — 1 (§13.3 history); "no promotion credit" — 0; "below 393" — 0.

## 4. Diff v4 → v5

`git diff --no-index --stat`: STRATEGY 355 lines changed (228 insertions, 127 deletions); COMMITMENTS.md 35 (+
change table); strategy_budget.py 73 (+66 / −7).

**Strategy, 64 hunks (v4 line numbers), all attributed:**

| v4 lines | attribution |
|---|---|
| 1, 3–5, 7 | new version (verdict §6 general rule: new `STRATEGY_<fixer>` file) |
| 38 | R1 (§0 heading no longer calls the projection "bounded"; aligns with the expected branch) |
| 55–75 | R1 (§5.1, §5.2 texts and the leading sentence) |
| 78–80 | R5 + G-C1 (§0 cost) |
| 88 | R3 (storage 420 → 470) |
| 91–93 | R5 (threshold 5,992); R1 (Q2 bullet) |
| 209–211 | G-C14 |
| 413 | R5 (H′ sentence, Ph-C3) |
| 734–736 | R4 |
| 743 | R1 point 4 (Df-9 EST) |
| 768–771 | R5 (paired pass, borrowing sentence deleted) |
| 788 | R3 (per-k comparison by day 14) |
| 817 (insert) | R3 (pilot records) |
| 819 | R1 point 4 (pilot reading) |
| 862–863, 865 | G-C5/Ph-C4, G-C6 |
| 907–908 | R1 (m_H = 1000, Ph-C2); R1 (β) label (Ph-C1, G-B2) |
| 911–913 | R1 (credit labels Ph-C5; e^(±1) rows; (α1′) rows; (α2) printed values, G-C10) |
| 920 | R1 point 3 (first sentence) |
| 923–925 | R1 point 3 (second and third sentences, log-normal reading, statistics-only) |
| 943 | R1 point 8 ("realistic" → "expected" in §4.4, alignment) |
| 1023 | R3 (B1 storage sentence, alignment with the pilot records) |
| 1280 | Ph-C7 |
| 1298 | G-C9 |
| 1300 | G-C4 |
| 1312, 1315 | R5 (B4 cost) |
| 1579 | R1 (alignment of §4.11 point 3 "reading expected") |
| 2024 | R5 (inventory row 20) |
| 2404 | R5 (Argo jobs) |
| 2424, 2429, 2433, 2435, 2443–2445 | R5 (§11.2 tables) |
| 2456 (insert) | R5 (changes against v4) |
| 2473, 2475–2477 | R5 (provenance, contingency, doubled guesses) |
| 2484 | R3 (§11.3 row 5–17) |
| 2487–2494 | R5 + N-C11 (§11.3 day markers) |
| 2505 | R5 (slot table 4a window end) |
| 2535 (insert), 2539 | R3 (§11.4) |
| 2572, 2596–2597, 2599, 2606 | R5 (§11.6) |
| 2611 | R3 (storage 470–670) |
| 2620 | R5 (decision point 3 days) |
| 2623–2624 | R3 (§11.7 inputs) |
| 2633 | R3 (§11.7 rule 1 day-7 pile-up input) |
| 2639–2640 | R1 point 6 |
| 2652 | G-C9 |
| 2679–2687 | R1 point 7 (Q2, §7 text; N-C4) |
| 2694 | R2 (Q3 route list and (β) clause, N-C5) |
| 2699–2701, 2703–2705 | R5 (Q4) + N-C1 |
| 2726–2728 | N-C6 (Df-8), R4 (Df-9), G-C2 (Df-10) |
| 2744 (insert) | R2 (three annex rows) |
| 2780–2781, 2783 | R1 (alignment of §12.5 "how this study could fail" with the expected branch) |
| 2834 (insert) | §13.4 change table (orchestrator deliverable A) |

**Unattributed strategy hunks: 0.** COM (8 hunks): header (new version), v5 change table, B1-f (R4, R5), B4-c (R5,
G-C9), TG-1 (R1 alignment with §4.11 point 3), T1-h (G-C2), S1-a (G-C11), REF-2 (G-C3), ST-1 (R5): 0 unattributed.
Script (17 hunks): docstring (version), [3] R5 row and N_PAIRED, [4] v3 → v4 line kept identical by subtracting R5
plus a v4 → v5 line, [5″] block, [8] R3 storage line, [9b] mapping, conversion-fall test, (α1′) tags and rows with
`pred=True`, fixed-B line, m_H = 1000 row, e^(±1) and log-normal lines, HEADLINE v5 line, conversion m_H line (all R1),
[13] G-C14 label: 0 unattributed.

## 5. Script stdout diff v4 → v5 (`diff budget_stdout_v4.txt budget_stdout_v5.txt`)

Every changed line is an R1, R3, R5 or G-C14 line or a total that follows from R5; all other printed values are
identical (the v3 → v4 history line and the v4 HEADLINE (P2) line are unchanged).

```
60a61
> | 4a | B4 | MUST | paired pile-up-only finder pass on 1,000 test-half events of each of the eleven other SM processes (incl. Z(tautau), lost-lepton Z(ll), multijets) | 35.8 | 11000 x 11.7 s | M | R5 |
95c96
<   phase 4a: MUST 2701 | SHOULD full 947 | SHOULD reduced 434
---
>   phase 4a: MUST 2737 | SHOULD full 947 | SHOULD reduced 434
99c100
<   MUST-only 3984; MUST + SHOULD reduced 4417; MUST + SHOULD full 4930
---
>   MUST-only 4019; MUST + SHOULD reduced 4453; MUST + SHOULD full 4966
109c110
<   B4: MUST 1150 | SHOULD full 0 | reduced 0
---
>   B4: MUST 1186 | SHOULD full 0 | reduced 0
119c120
<   Phase 4a: background and T1 MUST 2140; S1 chain 561; SHOULD reduced 434; SHOULD full 947
---
>   Phase 4a: background and T1 MUST 2176; S1 chain 561; SHOULD reduced 434; SHOULD full 947
121,123c122,124
<     MUST only: 3983.6 + 156.5 = 4140.1 CPU-h; stop-and-ask threshold 1.3 x 4140 = 5382
<     MUST + SHOULD reduced: 4417.1 + 156.5 = 4573.6 CPU-h; stop-and-ask threshold 1.3 x 4574 = 5946
<     MUST + SHOULD full: 4930.4 + 156.5 = 5086.9 CPU-h; stop-and-ask threshold 1.3 x 5087 = 6613
---
>     MUST only: 4019.4 + 156.5 = 4175.9 CPU-h; stop-and-ask threshold 1.3 x 4176 = 5429
>     MUST + SHOULD reduced: 4452.9 + 156.5 = 4609.4 CPU-h; stop-and-ask threshold 1.3 x 4609 = 5992
>     MUST + SHOULD full: 4966.2 + 156.5 = 5122.7 CPU-h; stop-and-ask threshold 1.3 x 5123 = 6660
124a126
>   v4 -> v5: review addition (R5) 35.78 CPU-h; MUST 3983.6 -> 4019.4; reduced 4417.1 -> 4452.9; full 4930.4 -> 4966.2; approved (reduced + reserve) 4573.6 -> 4609.4, threshold 5946 -> 5992
151a154,157
> [5''] deltas v4 -> v5, per finding (CPU-h; days on the Phase-4a critical path at the production capacity)
>     +35.78 CPU-h  +0.21 d   R5: paired pile-up-only finder pass on 1,000 test-half events of each of the eleven other SM processes (incl. Z(tautau), lost-lepton Z(ll), multijets) (phase 4a)
>   R1, R2, R4: text, table and [9b] rows only (0 CPU-h); R3: the pilot keeps its no-pile-up hit records (0 CPU-h; storage in [8])
> 
153c159
<   provenance M: 717 CPU-h, carried at 10% -> 72
---
>   provenance M: 753 CPU-h, carried at 10% -> 75
156,159c162,165
<   contingency from provenance 2146 CPU-h; fresh-sample reserve (one B2 direct sample) 403 CPU-h
<   approved figure (reduced + day-15 reserve) 4574 CPU-h; with contingency and the fresh-sample reserve: 7123; stop-and-ask threshold 1.3 x 4574 = 5946
<   thresholds for the other variants (each with the reserve): MUST only 1.3 x 4140 = 5382; full 1.3 x 5087 = 6613; envelope alternative (Q4): 4574 + 2146 = 6720, threshold 8736
<   if every guessed (G) unit cost doubled: 4574 + 1378 = 5952 CPU-h against the threshold 5946
---
>   contingency from provenance 2150 CPU-h; fresh-sample reserve (one B2 direct sample) 403 CPU-h
>   approved figure (reduced + day-15 reserve) 4609 CPU-h; with contingency and the fresh-sample reserve: 7162; stop-and-ask threshold 1.3 x 4609 = 5992
>   thresholds for the other variants (each with the reserve): MUST only 1.3 x 4176 = 5429; full 1.3 x 5123 = 6660; envelope alternative (Q4): 4609 + 2150 = 6759, threshold 8787
>   if every guessed (G) unit cost doubled: 4609 + 1378 = 5987 CPU-h against the threshold 5992
195,198c201,204
<   MUST-only: 4a production on the critical path 2140 - 0 (S-1) + 156 (day-15 reserve, P13) = 2297 CPU-h = 13.2 days; S1 chain 561 + moved 0 + toys pass 1 101 = 662 CPU-h run between the end of production and Gate B (2350 core-h available); total 56.7 days = 8.1 weeks; at utilisation 0.50 in production: 63.3 days
<   MUST + SHOULD reduced: 4a production on the critical path 2574 - 277 (S-1) + 156 (day-15 reserve, P13) = 2453 CPU-h = 14.1 days; S1 chain 561 + moved 277 + toys pass 1 101 = 940 CPU-h run between the end of production and Gate B (2350 core-h available); total 57.6 days = 8.2 weeks; at utilisation 0.50 in production: 64.6 days
<   MUST + SHOULD full: 4a production on the critical path 3087 - 737 (S-1) + 156 (day-15 reserve, P13) = 2507 CPU-h = 14.4 days; S1 chain 561 + moved 737 + toys pass 1 101 = 1399 CPU-h run between the end of production and Gate B (2350 core-h available); total 57.9 days = 8.3 weeks; at utilisation 0.50 in production: 65.1 days
<   range: every review passes at once and MUST only: 48.7 days; two ITERATE cycles per panel review: +8 days
---
>   MUST-only: 4a production on the critical path 2176 - 0 (S-1) + 156 (day-15 reserve, P13) = 2333 CPU-h = 13.4 days; S1 chain 561 + moved 0 + toys pass 1 101 = 662 CPU-h run between the end of production and Gate B (2350 core-h available); total 56.9 days = 8.1 weeks; at utilisation 0.50 in production: 63.6 days
>   MUST + SHOULD reduced: 4a production on the critical path 2610 - 277 (S-1) + 156 (day-15 reserve, P13) = 2489 CPU-h = 14.3 days; S1 chain 561 + moved 277 + toys pass 1 101 = 940 CPU-h run between the end of production and Gate B (2350 core-h available); total 57.8 days = 8.3 weeks; at utilisation 0.50 in production: 64.9 days
>   MUST + SHOULD full: 4a production on the critical path 3123 - 737 (S-1) + 156 (day-15 reserve, P13) = 2542 CPU-h = 14.6 days; S1 chain 561 + moved 737 + toys pass 1 101 = 1399 CPU-h run between the end of production and Gate B (2350 core-h available); total 58.1 days = 8.3 weeks; at utilisation 0.50 in production: 65.4 days
>   range: every review passes at once and MUST only: 48.9 days; two ITERATE cycles per panel review: +8 days
208a215
>   v5 (R3): pilot no-PU full hit records, classified in Phase 3 ((4e6 + 2.3e+06) x 8.2 kB; more for the hard-scatter events): 51.7 GB
214c221
<   storage total 417 GB (with the pre-merge cap of 400 GB: 617 GB)
---
>   storage total 469 GB (with the pre-merge cap of 400 GB: 669 GB)
216c223
<   jobs: reduced total / 0.4 h per job = 11043; Argo overhead 17 s each = 52 slot-h
---
>   jobs: reduced total / 0.4 h per job = 11132; Argo overhead 17 s each = 53 slot-h
270c277
<   mapping s95 -> reach (PLAN l.121, sigma_ln = 0 row; fixed B, median expected limit): [(3.0, 1026), (4.1, 971), (8.1, 866), (12.6, 799), (21.4, 717), (63.7, 548), (197.7, 393)]
---
>   mapping s95 -> reach (PLAN l.121, sigma_ln = 0 row; fixed B, median expected limit): [(3.0, 1026), (4.1, 971), (8.1, 866), (12.6, 799), (21.4, 717), (63.7, 548), (197.7, 393), (621.5, 243)]
277a285
>   v5 (R1) conversion fall test: v1 measured x6.6 (R05->R06, 86 -> 13) and x6.5 (R06->R07, 13 -> 2); with a pile-up-like fall from 13 at R06: mu(R07) = 0.038 / 0.065 counts (x339 / x201), P(>= 2) = 7.2e-04 / 2.0e-03; from 86 at R05: mu(R06) = 0.25 / 0.43, P(>= 13) = 2.3e-18 / 1.7e-15; DIF from 2 at R06: P(>= 1 at R07) = 0.59% / 0.99%
283a292,295
>     alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339), no fit-probability credit at R09: DIF 385, conversions 9.53e+03
>     alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339), with fit-probability credit at R09: DIF 22, conversions 544
>     alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201), no fit-probability credit at R09: DIF 647, conversions 9.53e+03
>     alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201), with fit-probability credit at R09: DIF 37, conversions 544
292a305
>   | v5 (Ph-C2): R09-like, Z(nunu) enters at its ceiling (estimator not credited): m_H = 1000 simulated ceiling counts (2282 events), with the count width | 2229 / 2299 / 2373 | 0.03 | 168.1 [118.6, 236.7] | 415 [369, 463] |
303,304c316,325
<   | alpha2 (own R06->R07 fall: DIF x2, conversions x6.5), no credit (R09 = R08): DIF 6.51e+04 + conversions 9.53e+03 | ≈ 74675 (sum of medians; fixed-B limit, an upper edge of the reach) | | 537 | < 393.0 |
<   | alpha2 (own R06->R07 fall: DIF x2, conversions x6.5), fit-probability credit at R09: DIF 3.72e+03 + conversions 544 | 3004 / 4407 / 6516 | 0.39 | 2231.5 [1146.2, 4179.3] | < 393.0 [< 393.0, < 393.0] |
---
>   | alpha2 (own R06->R07 fall: DIF x2, conversions x6.5), no credit (R09 = R08): DIF 6.51e+04 + conversions 9.53e+03 | ≈ 74675 (sum of medians; fixed-B limit, an upper edge of the reach) | | 537 | 262 |
>   | alpha2 (own R06->R07 fall: DIF x2, conversions x6.5), fit-probability credit at R09: DIF 3.72e+03 + conversions 544 | 3004 / 4407 / 6516 | 0.39 | 2231.5 [1146.2, 4179.3] | < 243.0 [< 243.0, < 243.0] |
>   | alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339), no credit (R09 = R08): DIF 385 + conversions 9.53e+03 | 9784 / 9929 / 10085 | 0.02 | 352.2 [251.6, 494.7] | 317 [273, 361] |
>     v5 (R1): the same at fixed B = B50 9929 (background known exactly): s95 196.6, reach 394 GeV
>   | alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339), fit-probability credit at R09: DIF 22 + conversions 544 | 391 / 580 / 874 | 0.40 | 314.4 [162.0, 587.7] | 332 [250, 420] |
>   | alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201), no credit (R09 = R08): DIF 647 + conversions 9.53e+03 | 10042 / 10193 / 10352 | 0.02 | 360.6 [258.2, 505.3] | 314 [270, 358] |
>     v5 (R1): the same at fixed B = B50 10193 (background known exactly): s95 199.3, reach 392 GeV
>   | alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x201), fit-probability credit at R09: DIF 37 + conversions 544 | 407 / 599 / 892 | 0.39 | 317.5 [164.9, 589.1] | 331 [250, 418] |
>   v5 (R1) alpha1 (pile-up fall x339), no credit: B x e^-1: B50 230, median reach 571, 84 % edge 519; B x e^+1: B50 1563, median reach 437, 84 % edge 390; log-normal reading (not used): B16/B50/B84 331 / 700 / 1584, median reach 262, 84 % edge < 243.0 GeV
>   v5 (R1) alpha1 (pile-up fall x201), no credit: B x e^-1: B50 373, median reach 535, 84 % edge 486; B x e^+1: B50 2615, median reach 400, 84 % edge 355; log-normal reading (not used): B16/B50/B84 543 / 1167 / 2656, median reach < 243.0, 84 % edge < 243.0 GeV
305a327
>   HEADLINE v5 (R1): (alpha1') no credit: B50 9929-10193, median reach 317-314 GeV, 84 % edge 273-270, fixed B 394-392; (beta) m_H = 10 / 30 / 100: median 767 / 749 / 695, 84 % edge 706 / 684 / 641; Z(nunu) m_H = 1000 with the count width: B50 2299, median reach 415
319a342
>   v5 (R1) P3/P14 EST with the conversions' own fall: Z(nunu) conversion part at R08 = 2.51e+07 x 0.2306 x (2/500) / 6.5 = 3.56e+03 events in 3 ab^-1; m_H = 1.56e+03 in 1.1e+07 pool events, 326 in the pilot's 2.3e+06 events (day-15 class limit m_H = 125)
502c525
<   DIF rate per triggered event by process (background.json -> cprime.dif.rate.per_process): 1.569 (Z nunu) to 1.5945 (tt 2l): spread 0.016
---
>   DIF rate per triggered event by process (background.json -> cprime.dif.rate.per_process): 1.5687 (WZ; v5, G-C14) to 1.5945 (tt 2l): spread 0.016
```

## 6. Verification, regression and neighbourhood checks

- Script run with `nice python3 -I` (≈ 17 s), rc 0, 525 lines. Line-by-line comparison with v4: only the lines above.
- R1: every reach number of §0, Table 4.4c, Q2, Q3 and §12.5 checked against `budget_stdout_v5.txt`; "84 % edge
  (median)" order used for every branch in §0 and Q2; "expected branch" now in §0, §4.4, §11.7 rule 1, Q2, §12.5; no
  section calls the pause "realistic" (only the §13.3 history row).
- R5 neighbourhood: every total of §11.2 (both tables), §11.3, §11.6, Q4, §0 and COM ST-1 re-read against [4], [6],
  [7]; rounding of "58 days", "57 days", "49 days", "65 days", "≈ 8 weeks" unchanged; the §11.3 table now sums to
  57.8.
- R3: the occupancy model date. Its R04–R05 inputs are the ρ = 1 development sample of the Phase-2 C1 campaigns (§4.4
  "The occupancy inputs come from the ρ = 1 development sample"; script [3] "PU rho = 1, 4000 events", phase 2); the
  model itself is built in channel (ii) of Phase 3 (days 5–16, §11.3). I wrote "evaluated with it by day 14 at the
  latest" (the verdict's date for the per-k comparison) and kept the day-7 projection on the v1-based EST rows.
- Values VERIFIED this session: `background.json` → `cprime.gamma.rows` (153 / 86 / 13 at R04–R06, conditionals 2/13
  at R07, 0/13 at R08), `cprime.dif.rows` (166 / 81), `cprime.gamma.rate.per_process.Znunu_j` = 0.2306,
  `cprime.dif.rate.per_process` (minimum WZ 1.5687, maximum tt̄ 2ℓ 1.5945); `bsum_wp.json` → `n_trig.not_included`;
  `s4cp.py` l.115 `pv = vtx[:3] + rng.normal(...)`; PLAN l.121 (10⁵ column 243) and l.122 (σ_ln = 0.2 row).

## 7. Not done, proposed (not changed, outside the verdict)

1. §4.4 "The change of the bound": "3.1 ((α1) without credit) to 4.7 (ceilings empty) decades" names (α1) correctly,
   but the table now also has (α1′) at B₈₄ ≈ 10⁴, i.e. ≈ 2.1 decades below v1's 1.2×10⁶ (log₁₀(1.2346×10⁶/10,085) =
   2.09, ESTIMATE from the printed B₈₄). Adding it needs a script print line; proposed for the next fix if wanted.
2. §0 point 2 and Table 4.4c still quote the abstract bracket of the bounded outcome ("the reach at the 84 % edge ...
   and 1,026 GeV"); consistent as written ("In the bounded outcome"), but the Gate-A package (N-C2, orchestrator
   task) should restate it for the expected branch.
3. Code reference says "about ten seconds"; the v5 script takes ≈ 17 s.
4. §12.2 still names "[Fiona] for this version" as the source of judgment calls; the one v5 judgment call (the
   occupancy-model date wording and "ESTIMATE" wording) is logged under [Gunnar] in `experiment_log.md`.
