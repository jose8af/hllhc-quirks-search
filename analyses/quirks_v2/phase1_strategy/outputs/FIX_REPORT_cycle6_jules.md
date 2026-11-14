# Fix report, review cycle 6 (fixer Jules, 2026-11-14 03:40)

Verdict: `review/arbiter/STRATEGY_ARBITER_v6_johanna_2026-11-14_03-15.md` (ITERATE; 0 A, 1 B = U1; ten C items "apply
before commit", §8 (i)). Artifact: `outputs/STRATEGY_jules_2026-11-14_03-40.md` (v7) = `cp` of
`STRATEGY_ingrid_2026-11-14_02-20.md` (v6, unchanged) plus the edits below. Script: `src/strategy_budget.py` (+7 lines:
two print lines and their arithmetic). Output: `outputs/budget_stdout_v7.txt`. `COMMITMENTS.md`: header pointer and
one change row (verdict §7 item 7). 0 CPU-h of production; one `nice -n 10 python3 -I` run, 37.5 s, 34.9 MB max RSS.

Script values replace the verdict's draft numbers where they differ: **B₅₀ 159 / 256** (verdict draft [158–254]);
own-hit basis **4.96–5.09×10⁴ at ε_pair = 0.8, 4.96–5.09×10⁵ at 0.98** (draft ≈ 5×10⁴ / ≈ 5×10⁵).

## 1. Status per finding

| finding | status | section heading (v7) | grep phrase |
|---|---|---|---|
| **U1** item 1, script | RESOLVED | script [9b], after the "avoided only with B50 <= 300" line | `v7 (U1): (alpha1) conversions removed, DIF x e^-1`; `v7 (U1): (alpha1') on the day-15 own-hit basis` |
| U1 item 2, rule 1 | RESOLVED | §11.7 "Decision point 2", point 1 *Projection* | `The projection of a no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional credit` |
| U1 item 3, Q2 stem | RESOLVED | §12.1 "Q2, the deliverable if the background is large" | `day-15 projections count own hits before CKF, with no S_CKF and no conditional credit`; `(after CKF, as v1 counted them; a lower value, since terms whose S_CKF test is not evaluable`; `which the day-15 projection admits only under (c)`; `so at v1's central decays-in-flight size (1–2 counts)` |
| U1 item 4, Q2 (c) (incl. Jp-C6, Jp-C7, U1-a/b/c) | RESOLVED | §12.1 Q2 option (c) | `with the\n> redesigned conditional and S_CKF estimated on development samples (EST, §11.7 rule 1)`; `B₅₀ 159–256`; `say whether it may also target the decays in flight`; `its signal cost is known only at Gate B`; `what remains of the reserve` |
| U1 item 5, §0 | RESOLVED | §0 "Expected" and "The pause." | `avoids it on its own at v1's central decays-in-flight size (1–2 counts)`; `51–74; admitted in the day-15 projection` (line-wrapped: `only under Q2 (c)`); `The day-7 and day-15 projections read own hits before CKF (Df-9) and are expected`; `(after\n  CKF, as v1 counted them; a lower value where S_CKF is not tested, annex route 6)` |
| U1 item 6, labels | RESOLVED | §4.4 point 4 (planning EST for Z(νν)); §4.4 point 5 *Reading of the pilot* | `(≈ 3×10² in the pilot) (after CKF; ×1/(1 − ε_pair) on all own hits)`; `≈ 3×10² after CKF, ×1/(1 − ε_pair) more on all own hits` |
| U1 item 7, COM | RESOLVED | COM "Changes of rows in version 7" | `§11.7 rule 1 basis of the day-15 projection stated` |
| U1 item 8, §13.6 | RESOLVED | §13.6 "Changes since version 6" | `U1 basis of the day-15 projection` |
| Ph C-4 | RESOLVED | §4.11 point 3 | `The reading expected if the day-15 pause does not fire is "target not met:` |
| Cr C1 | RESOLVED | §11.3 heading; §11.7 table row 3 | `days without the day-15 pause, every day after 15 moves by ≈ 2`; `(Gate B at ≈ 49), without the day-15 pause` |
| Cr C2 | RESOLVED | §0 Calendar; §11.3 calendar estimate | `65 days at 50 % utilisation (both without the day-15 pause)`; `is 0.50 (both without the day-15 pause)` |
| Cr C3 | RESOLVED | §11.6 | `missed by four to five weeks` |
| Cr C4 | RESOLVED | §12.1 Q2 rider part (3) | `in addition to the 1,000 DIF overlays of P4` |
| Jp-C2 | RESOLVED | §12.1 Q2 (b) | `(c) is then the route this strategy designs for` |
| Jp-C5 | RESOLVED | §12.1 Q2 | `(reach ≈ 560 GeV or more, statistics-only)` |
| Jp-C6 | RESOLVED (in U1 item 4) | §12.1 Q2 (c) | `its signal cost is known only at Gate B, and T2 keeps every selection with and without it` |
| Jp-C7 | RESOLVED (in U1 item 4) | §12.1 Q2 (c) | `what remains of the reserve` |
| Jp-C8 | RESOLVED | §12.1 Q2 (b) | `the first measured quirk-plane background (led by conversions)` |

Ten C items applied (Ph C-4, Cr C1, Cr C2, Cr C3, Cr C4, Jp-C2, Jp-C5, Jp-C6, Jp-C7, Jp-C8). Not applied, as the
verdict rules: Ph C-2, Jp-C9, Jp-C10, arbiter item 16 (Gate-A package only); Ph C-3, Cr C5 (deferred / no action).
Default (a), the expected-outcome numbers, every acceptance criterion, CPU-h and calendar figures: unchanged.

Verifier greps (cycle-7 critical scope): `day-7 reading counts own` → 0 hits; `only route in this strategy` → 0 hits;
`irreducible quirk-plane` → 0 hits. The v6 phrases survive only in the §13.5 history row ("H-C2 (×5–50 day-7
clause)", "a credit or faster fall for DIF"), which records v6 and is not edited.

## 2. Where the U1 statements stand in v7 (heading + phrase)

| statement | locations |
|---|---|
| day-7 **and** day-15 read own hits before CKF, ×5–50 above the after-CKF figures | §0 "The pause." (`The day-7 and day-15 projections read own hits before CKF (Df-9)`); §11.7 rule 1 (`expected ×1/(1 − ε_pair) above the after-CKF rows of Table 4.4c`); §12.1 Q2 stem (`The day-7 and\nday-15 projections count own hits before CKF`) |
| no S_CKF, no conditional credit in the projection; only the (c) test uses development estimates (EST) | §11.7 rule 1 (`Only the test of a Q2 (c) redesign multiplies`; `No credit in the result comes from these estimates`); Q2 (c) (`estimated on development samples (EST, §11.7 rule 1)`); consistent with Df-9 (`credited only where tested`, unchanged) and annex route 6 (unchanged) |
| (α1) with fit-probability credit admitted only under (c) | §0 "The pause." (`admitted in the day-15 projection only under Q2 (c)`); Q2 stem (`which the day-15 projection admits only under (c)`) |
| veto / conversions alone do not avoid the pause **at v1's central DIF size (1–2 counts)** | §0 "The pause."; §0 leading sentence; §4.4 Table 4.4c "What is not known"; Q2 stem; Q2 (c) (`That size rests on 1–2 counts; at its\n> size ×e⁻¹ the conversions alone would suffice`) |
| background size after CKF, a lower value | §0 "Expected" (`(after\n  CKF, as v1 counted them; a lower value where S_CKF is not tested, annex route 6)`); Q2 stem; §4.4 point 4 and point 5 labels |
| bar for (c) on the rule's basis | Q2 (c) (`If S_CKF cannot be estimated before\n> the freeze, every reduction must be ×1/(1 − ε_pair) larger (×5–50, not measured)`) |

Neighbourhood check: grepped v7 for `×5–50`, `(α1)`, `fit-probability credit`, `S_CKF`, `day-7`, `day-15`, `alone`,
`only route`, `irreducible`. The two further copies of the U1-a claim (§0 leading sentence, §4.4 "What is not known")
were given the same "at v1's central decays-in-flight size (1–2 counts)" qualifier (propagation of U1 item 3/5;
hunks 8 and 13 below). Df-9, §12.5 and the annex rows were read and agree with rule 1 as written; not edited. The
other `(α1)` and `fit-probability credit` mentions are Table 4.4c rows and scenario text on the after-CKF basis that
the table's own caption/§4.4 point 4 now label; not edited.

## 3. Diff v6 → v7

`git diff --no-index --stat`: `STRATEGY_ingrid_… => STRATEGY_jules_… | 99 ++++++++++++++-------- ; 64 insertions(+),
35 deletions(-)` before O1/O2; after O1/O2: `71 insertions(+), 38 deletions(-)`, 28 hunks (`diff` normal format, v6 line numbers):

| # | hunk | attribution |
|---|---|---|
| 1 | 1c1 title "version 7" | §7 item 8 (version bookkeeping) |
| 2 | 3,5c3,5 fixer line, replaced version, verdict | §7 item 8 |
| 3 | 7c7 "verification (cycle 7)" | §7 item 8 |
| 4 | 66c66,67 §0 "Expected" after-CKF clause | U1 item 5 |
| 5 | 92,93c93,95 §0 "The pause." central-size qualifier, (α1) credit only under (c) | U1 item 5 |
| 6 | 99c101,102 §0 ×5–50 day-7 and day-15 sentence | U1 item 5 |
| 7 | 103c106,107 §0 leading sentence after-CKF label | **O2** (orchestrator-ordered) |
| 8 | 107c111,112 §0 leading sentence central-size qualifier | U1 propagation (U1-a, items 3/5) |
| 9 | 120c125 §0 "(both without the day-15 pause)" | Cr C2 |
| 10 | 785c790 §4.4 point 4 label | U1 item 6 |
| 11 | 819c824 §4.4 point 4 C′_PU use | **O1** (orchestrator-ordered) |
| 12 | 865c870 §4.4 point 5 label | U1 item 6 |
| 13 | 1014c1019 §4.4 "What is not known" central-size qualifier | U1 propagation (U1-a) |
| 14 | 1654,1655c1659,1660 §4.11 point 3 | Ph C-4 |
| 15 | 2560c2565 §11.3 heading | Cr C1 |
| 16 | 2597c2602 §11.3 "(both without the day-15 pause)" | Cr C2 |
| 17 | 2654c2659 §11.6 "four to five weeks" | Cr C3 |
| 18 | 2704c2709 §11.7 row 3 | Cr C1 |
| 19 | 2724c2729,2734 rule 1 sentence | U1 item 2 |
| 20 | 2771c2781,2782 Q2 stem after-CKF clause | U1 item 3 |
| 21 | 2775,2776c2786,2789 Q2 stem day-7 and day-15 sentence (printed v7 values) | U1 item 3 |
| 22 | 2779,2780c2792,2794 Q2 stem central size; (α1) credit only under (c) | U1 item 3 |
| 23 | 2787c2801 Q2 (b) "led by conversions" | Jp-C8 |
| 24 | 2790,2791c2804,2805 Q2 (b) route sentence | Jp-C2 |
| 25 | 2794,2798c2808,2817 Q2 (c) text and "statistics-only" | U1 item 4 (with Jp-C6, Jp-C7) + Jp-C5 |
| 26 | 2807c2826 rider part (3) | Cr C4 |
| 27 | 2918c2937,2938 §12.5 point 3 after-CKF label | **O2** (orchestrator-ordered) |
| 28 | 2998a3019,3031 §13.6 change table (incl. O1, O2 rows) | §7 item 8; O1/O2 rows |

**Unattributed hunks: 0.**

Script: one hunk, `@@ -845,0 +846,7 @@` (3 comment lines, 2 arithmetic lines `U1_I`, `U1_II`, 2 print lines) → U1
item 1. `pmf_pred` seeds its own `random.Random(7)` per call, so the new call does not shift any other value.
COM: 3 hunks (header pointer to v7, version-6 file added to the earlier list, version-7 change table with the TG-1
row) → U1 item 7.

## 4. Script outputs

`diff budget_stdout_v6.txt budget_stdout_v7.txt`:
```
351a352,353
>     v7 (U1): (alpha1) conversions removed, DIF x e^-1 (both falls): B50 159 / 256 (x339 / x201) -> at or below 300
>     v7 (U1): (alpha1') on the day-15 own-hit basis, conversions and DIF x 1/(1 - eps_pair) at eps_pair = 0.8 / 0.98 (assumed, not measured; photon rate 0.379): B50 ≈ 4.96e+04-5.09e+04 / 4.96e+05-5.09e+05 (sum of medians)
```
Only added lines; every v6 value is unchanged. Line (ii) is the sum of medians (the fixed-B reading the script's
`row()` uses above 5,000 events), at the 0.379 photon rate of the (α1′) rows.

## 5. Orchestrator-ordered additions O1, O2 (beyond the arbiter's verdict; source: this fixer's own proposal)

| item | status | section heading | grep phrase |
|---|---|---|---|
| O1 C′_PU use | RESOLVED | §4.4 point 4, *Development samples (Phase 3, results fixed before the freeze)* | `C′_PU has no Geant4 and serves C1 and, for the conversions, the development estimate of a Q2 (c) redesign` |
| O2 basis label | RESOLVED | §0 **Leading sentence**; §12.5 point 3 | `maximum photon rates; after CKF, as v1 counted them, a`; `v1 placeholder efficiencies; after CKF, as v1 counted them, a lower value where` |

O1 checks: C′_PU (inventory row 4) holds v1-gun background topologies (DIF, γ, V⁰) and no signal, so a development
estimate on it raises no blinding issue (BL-1 untouched); the inventory row already lists development uses; no
acceptance criterion, sample size or CPU-h changes.
O2 wording: I used "after CKF, as v1 counted them, a lower value where S_CKF is not tested" (the U1 wording of §0 and
Q2). I did **not** write "credited": the 0.7–1.0×10⁴ figure is the (α1′) **no-credit** row (stdout "(alpha1') no
credit"), so a "credited" label would be false. No number changed.

## 6. Not done, proposed

- The Q2 stem's ×5–50 sentence quotes the own-hit values at the 0.379 photon rate only (the printed line has no
  0.255 row); a second print at the N_trig-weighted rate would give the full range, not added (scope).
