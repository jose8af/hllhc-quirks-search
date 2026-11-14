# Critical review, cycle 7: STRATEGY v7 (quirks v2, Phase 1)

Reviewer: Kenji (critical), 2026-11-14 04:05. A fresh session that saw no earlier cycle.
Artifact: `phase1_strategy/outputs/STRATEGY_jules_2026-11-14_03-40.md` (v7, 3,039 lines), `COMMITMENTS.md`,
`phase1_strategy/src/strategy_budget.py`, `budget_stdout_v6.txt`, `budget_stdout_v7.txt`.
Reference: verdict `review/arbiter/STRATEGY_ARBITER_v6_johanna_2026-11-14_03-15.md` §7 (U1), §8 (C items), §12 (scope).
Scope (verdict §12): the U1 fix and the §8(i) items, the full diff, the script outputs and the greps. Under §12 a
new finding counts only if it is a regression of this fix, a factual error in a number shown to the user, or a
genuine A.

Method: `diff` v6 against v7 in normal format (28 hunks); `git diff HEAD~1` on COM and the script; a fresh run of
the script; greps on v7, each hit read in context. Line numbers are v7 lines unless marked v6.

---

## 1. U1 against verdict §7, item by item

| item | v7 location | quoted text present | ordered text present? |
|---|---|---|---|
| 1 (i) script line | stdout v7 l.352 | "v7 (U1): (alpha1) conversions removed, DIF x e^-1 (both falls): B50 159 / 256 (x339 / x201) -> at or below 300" | **Yes.** The verdict's draft gave [158 / 254]. My arithmetic, 401 − 385 + 385/e = 157.6 and 663 − 647 + 647/e = 254.0, reproduces the draft. The script instead counts the Poisson medians (`pmf_pred`, l.849 of the script), which gives 159 / 256. The verdict says printed values replace bracketed ones. VERIFIED (my run). |
| 1 (ii) script line | stdout v7 l.353 | "(alpha1') on the day-15 own-hit basis … at eps_pair = 0.8 / 0.98 (assumed, not measured; photon rate 0.379): B50 ≈ 4.96e+04-5.09e+04 / 4.96e+05-5.09e+05 (sum of medians)" | **Yes.** Expected ≈ 5×10⁴ / ≈ 5×10⁵. Check: (9,527 + 385) × 5 ≈ 4.96×10⁴, so the ×5 holds. No other stdout line changed (§5). |
| 2 rule 1 | §11.7 l.2729–2734, directly after "and it becomes binding at / day 15." | "The projection of a no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional credit (Df-9); … No credit in the result comes from these estimates." | **Verbatim** (word-for-word against §7 item 2), at the ordered position. |
| 3a Q2 stem | l.2786–2789 | "The day-7 and day-15 projections count own hits before CKF, with no S_CKF and no conditional credit (Df-9, §11.7 rule 1), and are expected ×5–50 above this figure (at the 0.379 photon rate B₅₀ ≈ 5.0–5.1×10⁴ at ε_pair = 0.8 and ≈ 5.0–5.1×10⁵ at 0.98, assumed, not measured; script [9b], v7 line)." | **Yes.** "[printed line]" was filled in with the printed values: 4.96–5.09e4 rounds to 5.0–5.1×10⁴. The old v6 sentence "The day-7 reading counts own hits … may be ×5–50" is gone (0 hits). |
| 3b Q2 stem | l.2780–2782 | "(after CKF, as v1 counted them; a lower value, since terms whose S_CKF test is not evaluable stay on all own hits, annex route 6)" | **Verbatim**, after "…at the R08–R09 selections". |
| 3c Q2 stem | l.2794 | "(α1) with fit-probability credit, which the day-15 projection admits only under (c);" | **Verbatim.** |
| 3d Q2 stem | l.2792–2793 | "so at v1's central decays-in-flight size (1–2 counts) a conversion veto alone does not avoid the pause" | **Verbatim.** |
| 4 Q2 (c) | l.2808–2816 | from "CPU-h inside the development allowance and what remains of the reserve." to "…T2 keeps every selection with and without it." | **Verbatim**, with one equivalent change: "(B₅₀ 159–256, script [9b], v7 line)" in place of "[158–254], script [9b]", which is the script value. The bar figures in the text match stdout: 401 / 663 (stdout l.347–348), ×52.1 (98.1 %) and ×31.0 (96.8 %) (l.349–350). |
| 5a §0 "The pause." | l.93 | "avoids it on its own at v1's central decays-in-flight size (1–2 counts)." | **Verbatim.** |
| 5b §0 "The pause." | l.94–95 | "(51–74; admitted in the day-15 projection only under Q2 (c))" | **Verbatim.** 51 / 74 = stdout l.351. |
| 5c §0 "The pause." | l.101–102 | "The day-7 and day-15 projections read own hits before CKF (Df-9) and are expected ×5–50 above the after-CKF figures of this summary." | **Verbatim**, as the paragraph's last sentence. |
| 5d §0 "Expected" | l.66–67 | "(… 0.255 and 0.379 per event) (after CKF, as v1 counted them; a lower value where S_CKF is not tested, annex route 6)" | **Verbatim**, at the ordered position. The two parenthesis groups sit side by side ("…event) (after…"); see C2. |
| 6a label l.785 (v6) | l.790 | "(≈ 3×10² in the pilot) (after CKF; ×1/(1 − ε_pair) on all own hits)" | **Verbatim.** |
| 6b label l.865 (v6) | l.870 | "≈ 3×10² after CKF, ×1/(1 − ε_pair) more on all own hits, if the conversions keep v1's fall" | **Verbatim.** |
| 7 COM | COM l.30–34 | "TG-1 (Q2) \| §11.7 rule 1 basis of the day-15 projection stated; Q2 (c) test on development estimates (U1); no status changed" | **Verbatim**, one row. No criterion row is changed (§4). |
| 8 §13.6 | l.3020–3031 | "### 13.6 Changes since version 6 …" with rows for U1, O1, O2 and the C items | **Present.** It states that no default, criterion, CPU-h, calendar or expected-outcome number changed, which matches the diff (§4). |

**U1: fully applied.** Every item carries the ordered text, verbatim or with the script's printed values in place
of the draft figures.

## 2. The ten §8(i) C items

| item | v7 location | check |
|---|---|---|
| Ph C-4 | l.1659–1660 | "**The reading expected if the day-15 pause does not fire is "target not met: sample-size limited" while the ceilings count few events**". Exact. The parenthesis that follows was kept, as ordered, so "if the day-15 pause does not fire" now appears twice in a row (C1). |
| Cr C1 heading | l.2565 | "…proposed variant; days without the day-15 pause, every day after 15 moves by ≈ 2 in the expected branch)". Exact. The ≈ 2 matches stdout l.205, "+ 2.0 d day-15 pause turnaround". |
| Cr C1 row 3 | l.2709 | "days 36.8–48.8 (Gate B at ≈ 49), without the day-15 pause". Exact. |
| Cr C2 §0 | l.125 | "65 days at 50 % utilisation (both without the day-15 pause)". Exact. |
| Cr C2 §11.3 | l.2602 | "is 0.50 (both without the day-15 pause)". Exact. |
| Cr C3 | l.2659 | "missed by four to five weeks". Exact. |
| Cr C4 | l.2826 | "(3) 1,000 γ development overlays, in addition to the 1,000 DIF overlays of P4 (seeds disjoint from 4a)". Exact. |
| Jp-C2 | l.2804–2805 | "(c) is then the route this strategy designs for one; the conditionals measured in production may add some reach, with credit not yet measured." Exact. |
| Jp-C5 | l.2817 | "(reach ≈ 560 GeV or more, statistics-only)". Exact. |
| Jp-C6 | l.2815–2816 | "its signal cost is known only at Gate B, and T2 keeps every selection with and without it". Applied inside the U1 text. |
| Jp-C7 | l.2808 | "what remains of the reserve". Applied inside the U1 text. |
| Jp-C8 | l.2801 | "the first measured quirk-plane background (led by conversions)". Exact. "irreducible quirk-plane" has 0 hits. |

**§8(ii) and (iii) were not applied to the strategy.** Greps, v6 → v7 counts:
- "width of 0.05 or more" (Ph C-2): 0 → 0.
- "none demonstrated" / "stronger paper" (Jp-C9): 0 → 0.
- "0.2306" (Ph C-3): 0 → 0.
- "80 %" (arbiter item 16): 3 → 3.
- "transfer-factor": 2 → 2.

The diff is conclusive in any case: all 28 hunks are attributed in §4, and none of them is a §8(ii)/(iii) item
(that also covers Jp-C10).

## 3. Additions beyond the verdict

**O1 (l.824).** The new text: "C′_PU has no Geant4 and serves C1 and, for the conversions, the development estimate
of a Q2 (c) redesign, §11.7 rule 1".
- Nothing else changes. The same hunk alters no sample size, CPU-h, criterion or seed stream. C′_PU stays 5,000
  events, 35 CPU-h (l.668; inventory row 4, l.2087).
- C′_PU is background only. Inventory row 4 is "C′_PU topologies (v1 guns)", with v1-gun DIF, γ and V⁰ (Table l.573).
  It contains no signal, so the blinding invariant (no v2 signal efficiency before the closure verdicts, l.180) is
  not touched.
- Its role already includes "development" (row 4: "C1; development (attribution rules compared; completeness
  classes)"). §4.17 l.2073 defines a development sample as one that "may be looked at freely before the freeze and is
  never used for a verdict". Rule 1 adds "No credit in the result comes from these estimates" (l.2734). The pre-freeze
  development estimate is therefore within the rules.
- O1 removes a real contradiction. v6 l.819 said "serves only C1", while v7 rule 1, as ordered by the verdict, names
  "the C′_PU γ sample" as a development sample. "serves only C1" now has 0 hits.
- Residual: the inventory row's role column does not name the new use (C4).
- **Verdict: in scope, correct, no A/B.**

**O2 (l.106–107, §0 leading sentence; l.2937–2938, §12.5 point 3).** The label added: "after CKF, as v1 counted
them, a lower value where S_CKF is not tested".
- It copies the label the verdict ordered for §0 "Expected", so the three summary copies of the 0.7–1.0×10⁴ figure
  now carry the same basis.
- The fixer's refusal to write "credited" is correct. Stdout l.320 / l.323 give the (α1′) **no credit (R09 = R08)**
  rows with B₅₀ 9,929 / 10,193, and l.358 gives "HEADLINE v6 (T1): (alpha1') no credit, photon rate 0.255-0.379: B50
  6825-10193". The credited rows are l.322 / l.325, with B₅₀ 580 / 599. Calling 0.7–1.0×10⁴ "credited" would have
  been false.
- **Verdict: in scope, correct.**

**"1–2 counts" caveat on two more copies** (l.111–112, §0 leading sentence; l.1018–1019, §4.4 "What is not known").
- The fixer applied the qualifier of §7 items 3d and 5a to the remaining copies of the same claim. Without it, the
  leading sentence would state unconditionally what the Q2 (c) text now limits: "at its size ×e⁻¹ the conversions
  alone would suffice".
- The stated condition matches stdout l.347–348 and l.352.
- **Verdict: a proper propagation of U1, needed to avoid a live contradiction. No A/B.**
- A finer point: on the day-15 own-hit basis, DIF × e⁻¹ without an S_CKF estimate would still be ≈ ×5 above 300.
  That is said only in Q2 (c), not at these copies (C3).

**COM change.**
- Three hunks: the pointer to v7, the v6 file added to the history list, and the version-7 change table with the
  single TG-1 row.
- Ordered by §7 item 7 (the row) and routine version bookkeeping (the pointer).
- The history sentence now reads "…(version 5) and `STRATEGY_ingrid…` (version 6)", with two "and"s (C6).
- No criterion row changed: the diff touches l.3–7 and adds l.30–35 only.

## 4. Diff check (complete)

**Strategy v6 → v7: 28 hunks (normal-format `diff`). Each is attributed below.**

| # | v6 hunk | content | attribution |
|---|---|---|---|
| 1 | 1c1 | title "version 7" | version bookkeeping (§7 item 8) |
| 2 | 3,5c3,5 | fixer, replaced version, verdict | bookkeeping |
| 3 | 7c7 | "verification (cycle 7)" | bookkeeping |
| 4 | 66c66,67 | §0 Expected label | U1 5d |
| 5 | 92,93c93,95 | §0 pause: central size; (α1) credit only under (c) | U1 5a, 5b |
| 6 | 99c101,102 | §0 ×5–50 sentence | U1 5c |
| 7 | 103c106,107 | leading sentence label | O2 |
| 8 | 107c111,112 | leading sentence central size | declared caveat |
| 9 | 120c125 | "(both without the day-15 pause)" | Cr C2 |
| 10 | 785c790 | pilot label | U1 6a |
| 11 | 819c824 | C′_PU use | O1 |
| 12 | 865c870 | pilot label | U1 6b |
| 13 | 1014c1019 | "What is not known" central size | declared caveat |
| 14 | 1654,1655c1659,1660 | §4.11 reading | Ph C-4 |
| 15 | 2560c2565 | §11.3 heading | Cr C1 |
| 16 | 2597c2602 | §11.3 range | Cr C2 |
| 17 | 2654c2659 | "four to five weeks" | Cr C3 |
| 18 | 2704c2709 | §11.7 row 3 | Cr C1 |
| 19 | 2724c2729,2734 | rule 1 sentence | U1 2 |
| 20 | 2771c2781,2782 | Q2 stem label | U1 3b |
| 21 | 2775,2776c2786,2789 | Q2 stem day-7 and day-15 sentence | U1 3a |
| 22 | 2779,2780c2792,2794 | Q2 stem central size, (α1) credit | U1 3d, 3c |
| 23 | 2787c2801 | "led by conversions" | Jp-C8 |
| 24 | 2790,2791c2804,2805 | route sentence | Jp-C2 |
| 25 | 2794,2798c2808,2817 | Q2 (c) text; "statistics-only" | U1 4 (with Jp-C6, Jp-C7); Jp-C5 |
| 26 | 2807c2826 | rider part (3) | Cr C4 |
| 27 | 2918c2937,2938 | §12.5 point 3 label | O2 |
| 28 | 2998a3019,3031 | §13.6 | U1 8 (rows for U1, O1, O2, C items) |

**Unattributed hunks: 0.**
- No hunk changes a number, except the newly printed values, which are cited to the v7 script lines.
- Replaced text inside each hunk: I compared the `<` and `>` sides. Each hunk changes only the ordered phrase and
  re-wraps lines.

**COM (`git diff HEAD~1`).** Three hunks:
- l.3–7: pointer and history list.
- l.30–35: the version-7 table with the TG-1 row.

All attributed (U1 7 and bookkeeping).

**Script.** One hunk, `@@ -843,6 +843,13 @@`, adding 7 lines:
- 3 comment lines;
- the `U1_I` and `U1_II` arithmetic;
- 2 prints.

All attributed to U1 1. No existing line was edited. `pmf_pred` has its own seed (fix report), and the
byte-identical v6 lines (§5) confirm that the new call shifted no other value.

## 5. Script

- **Run.** `python3 -I src/strategy_budget.py`, standard library only (`import math, random`), on einstein as allowed
  for light arithmetic: rc 0, empty stderr.
- **Against the saved v7 output.** sha256 `82ab05e6…02bd19` both for my run and for `budget_stdout_v7.txt`.
  **Byte-identical.** VERIFIED.
- **Against v6.** `diff budget_stdout_v6.txt budget_stdout_v7.txt` gives `351a352,353`, the two added lines only
  (554 → 556 lines). VERIFIED.
- **Figures** (stdout v7):

| figure | stdout v7 | check |
|---|---|---|
| approved CPU-h | l.123 and l.163: "4452.9 + 156.5 = 4609.4 CPU-h"; "approved figure … 4609 CPU-h" | ✓ |
| threshold | "1.3 x 4609 = 5992" | ✓ |
| calendar | l.205: 59.8 d with the pause (text: "60 days"); 57.8 without (text l.124: "58 days without it") | ✓ |
| rider | l.206: "approved 4616.4 CPU-h, threshold 1.3 x 4616.4 = 6001.3", presented as an option only | text l.2827 "approved 4,616, threshold 6,001", inside "*Optional rider … not part of the default*" ✓ |

## 6. Greps for live contradictions (v7)

| pattern | hits in context | status |
|---|---|---|
| ×5–50 applying to day 7 only ("day-7 reading counts own", "day 7 only") | 0 / 0. Every ×5–50 statement says "day-7 and day-15" (l.101, l.2786) or states the basis generally (l.2731, l.2814). The only other hit is l.3018, the §13.5 history row "H-C2 (×5–50 day-7 clause)". | history only |
| "(α1)" or "fit-probability credit" as a branch avoiding the pause | l.94 and l.2794 both carry "admitted … only under (c)". l.969 is a Table 4.4c row with no pause claim. l.75 says "earn no fit-probability credit". | no live contradiction |
| "serves only C1" | 0 | removed |
| (c) bar on v1's credited basis | ×31–52 appears at l.2811 (on the rule-1 development basis, with ×1/(1 − ε_pair) if S_CKF is not estimable) and at l.3015 (§13.5 history row, "a credit or faster fall for DIF") | history only |
| unlabelled background size in a leading position | §0 "Expected", leading sentence, Q2 stem and §12.5 point 3 are labelled. Two unlabelled sizes remain: §0 floor list item 3, l.59–61 ("≈ 9.5×10³ … ≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c)", under "the projection contains them", with basis only "with pile-up", l.55); and [L13] l.2288 ("≈ 10⁴ events"). §0's blanket sentence l.101–102 ("×5–50 above the after-CKF figures of this summary") covers l.59–61; [L13] is not a leading position. | C3, C7 |
| 4,574 / 5,946 | l.2542 "Version 4 had … 4,574 … 5,946"; l.2985 and l.3004, §13 rows | history only |
| 57.6 | l.2989 and l.3004, §13 rows "57.6 → 57.8" | history only |
| 710 / 790 GeV as expectation | l.78 "≈ 710 GeV (790) if every no-pile-up ceiling counts zero, an upper edge that the strategy's own planning estimate does not expect"; l.2795 "every ceiling empty, ≈ 710 GeV (median 790), an upper edge"; l.960 "(upper edge)"; l.2819 "helps only if the ceilings are empty". Other "790" hits are unrelated (74,790 events; v1's μ₉₅ ≈ 790; history). | labelled as an upper edge, not an expectation |
| 470–500 GeV | l.74 and l.2791: the conditional (α1) upper branch, "if decays in flight and conversions fall like the pile-up background", "statistics-only" (l.80, l.2789), and "disfavour[ed] at p ≈ 10⁻³" | labelled conditional branch, not the expectation |

**No live contradiction found.**

## 7. Findings

**Category A: none.**

**Category B: none.**

**Category C** (wording; none affects a number, criterion or choice):
- **C1.** l.1659–1660: "if the day-15 pause does not fire" now appears twice in a row (bold sentence and kept
  parenthesis). Shorten the parenthesis to "(by v1's conversion counts the expected branch is a measured background,
  §0, Q2)".
- **C2.** l.66–67: two parenthesis groups side by side ("…per event) (after CKF…"). Merge with "; ".
- **C3.** §0 floor list item 3, l.59–61, quotes ≈ 9.5×10³ / ≈ 1.0×10⁴ under "the projection contains them" without
  the after-CKF label. The l.101–102 blanket sentence covers it 40 lines later. Adding "(after CKF)" there, and at the
  two "1–2 counts" copies (l.111, l.1018) "on the after-CKF basis", would remove any reading that conversions alone
  could avoid the day-15 projection at DIF × e⁻¹ without an S_CKF estimate. That reading is excluded by Q2 (c),
  l.2813–2814.
- **C4.** §4.17 row 4, l.2087: the role column could add "Q2 (c) development estimate (rule 1)" to match O1.
- **C5.** l.2788: the bracket gives own-hit values at the 0.379 photon rate only. At 0.255 the range starts near
  3.4×10⁴ (ESTIMATE: 6.8×10³ × 5). The rate is labelled, so the bracket is not wrong. The fixer already notes this.
- **C6.** COM l.6–7: "(version 5) and `…ingrid…` (version 6)" has a doubled "and"; make it "…(version 4),
  `…gunnar…` (version 5) and `…ingrid…` (version 6)".
- **C7.** [L13] l.2288: "≈ 10⁴ events" has no basis label. Not a leading position.
- **C8** (non-artifact). The fix report §2 says "§12.5 … not edited", but O2 edited §12.5 point 3 (hunk 27). The
  report's own §5 lists that edit correctly.

## 8. Conclusion

- U1 (§7 items 1–8) is applied as ordered. The only change is that the script's printed 159–256 and 4.96–5.09×10⁴ /
  ×10⁵ replace the draft figures, as the verdict instructs.
- The ten §8(i) items are applied exactly; no §8(ii)/(iii) item reached the strategy.
- O1, O2, the caveat and the COM row are in scope and correct.
- 28 + 3 + 1 hunks, all attributed.
- The script output is byte-identical to `budget_stdout_v7.txt` and differs from v6 by the two added lines only. The
  approved figures are unchanged: 4,609 / 5,992 / 60 days (57.8 without the pause); the rider's 4,616.4 / 6,001.3 is
  an option only.

**No Category A or Category B item remains open.** 8 Category C items (C1–C7 on the artifact, C8 on the fix report).
