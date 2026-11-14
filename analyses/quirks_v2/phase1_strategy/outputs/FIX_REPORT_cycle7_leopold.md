# Fix report: review cycle 7 (STRATEGY v7 → v8)

Fixer: Leopold, 2026-11-14 05:00. Verdict: `review/arbiter/STRATEGY_ARBITER_v7_lena_2026-11-14_04-30.md` (ITERATE,
0 A, 4 B in one family V1, 14 C items to apply now). Physics review read for context:
`review/physics/STRATEGY_PHYSICS_REVIEW_v7_katya_2026-11-14_04-05.md`.

Files:
- `outputs/STRATEGY_leopold_2026-11-14_05-00.md` (v8; v7 `STRATEGY_jules_2026-11-14_03-40.md` unchanged)
- `src/strategy_budget.py` (item S block + the l.911 f-string)
- `outputs/budget_stdout_v8.txt`
- `QV2/COMMITMENTS.md` (Cr C6 and the version-8 row, both ordered by the verdict §4)

Computation: einstein, `nice -n 10 python3 -I src/strategy_budget.py`, 1 min 30 s wall, 35 MB max RSS
(`/usr/bin/time -v`). Two scratch checks (runpy of the script with stdout suppressed, script functions only, in the
session scratchpad, not part of the record): (i) DIF removed, conversions ×31.0 / ×34 / ×52.1 → B₅₀ 324 / 297 / 201;
(ii) (α1) own-hit sums at ε_pair 0.8 / 0.98: 2,849 / 28,381 (×339) and 4,786 / 47,751 (×201), so "≈ 2.8×10³–4.8×10⁴" is
the correct two-figure rounding of the printed 2.85e+03 … 4.78e+04. No git command, no sub-agent, no pixi.

## 1. The four B findings

| finding | status | where (section heading + grep phrase) |
|---|---|---|
| V1-a: (β) listed as avoiding the pause | **RESOLVED** | §0 Summary: "(β) is read as (γ) at day 15"; §0 upper branches: "a result after the freeze: its Z(νν) credit comes from the B4-c test"; §4.4 scenarios: "(β) is a result after the freeze: at day 15"; §12.1 Q2 stem: "((β)'s Z(νν) credit exists only after the freeze)" and "Their day-15 readings are the (γ) and empty-ceiling rows"; printed row "(beta) \| not a day-15 branch" |
| V1-b: "at ×e⁻¹ the conversions alone would suffice" | **RESOLVED** | §12.1 Q2 (c): "and ×69–235 (98.6–99.6 %) [×47–159] at ×e⁻¹"; printed grid row "f_D = e^-1". The old sentence is gone (grep "would suffice": 0 hits in live text) |
| V1-c: bar "×31–52 and the decays in flight reduced" infeasible at ×31 | **RESOLVED** | §12.1 Q2 (c): "is at least ×34 (97.0 %) [×23] even if the decays in flight vanished"; grid printed verbatim; ×31–52 survives only as the printed comparison line "(alpha1) conversion levels for comparison: x52.1 / x31.0" (grep "×31": 0 hits in live text) |
| V1-d: fit-probability credit acts on DIF, (c) as worded does not target DIF | **RESOLVED** | §12.1 Q2 (c): "At v1's central size (c) cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 51–74) acts on both"; Q2 table row "only in the test of a (c) redesign (EST): (α1) with fit-probability credit on decays in flight and conversions"; printed rows "(needs (c) to target DIF)"; §0 "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" |

## 2. Item S: the script block, and agreement with the arbiter

Inserted verbatim after script l.852 (the second `v7 (U1)` print), 53 lines, using only names defined above it; the
l.911 f-string text changed as ordered (S20). No other script line changed.

**Printed values equal the arbiter's in every cell** (no difference to explain):
- every pilot ceiling zero: 75 [38–148], below;
- Z(νν) at pilot count m = 5 / 10 / 15 / 20 / 25 / 50: 130 / 187 / 242 / 300 / 352 / 626 (m = 20 gives exactly 300, classed
  "below" by the rule's B₅₀ ≤ 300);
- (γ) at m_H = 10 / 30 / 50 / 60 / 70 / 100 pool counts (2 / 6 / 10 / 13 / 15 / 21 pilot): 104 / 180 / 255 / 294 / 331 / 448;
- (α1) no credit: 587 / ≈ 2.85e+03 / ≈ 2.84e+04 (×339), 975 / ≈ 4.79e+03 / ≈ 4.78e+04 (×201);
- (α1′): ≈ 4.96e+04–5.09e+04 / 4.96e+05–5.09e+05;
- (c) credit: 51 / 74;
- rejection grid (rate 0.379 [0.255]): f_D = 0 ×34 / ×34 [×23 / ×23]; 1/4 ×52 / ×81 [×35 / ×55]; e⁻¹ ×69 / ×235
  [×47 / ×159]; 1/2 ×110 / none [×74 / none]; 1 none / none.
- Spot value not printed, checked in scratch: ×31 with DIF removed → 324 (the arbiter's V1-c number).

**Definitions of the rows** (as implemented by the block; identical to verdict §1.1):
- *Basis "rule 1"*: every no-pile-up term at max(zero-count floor, N_t·H) with H = Gamma(m + 1) of the pilot count m
  (`pmf_pred` term (κ, m)); no S_CKF, no conditional, no post-freeze credit. Pilot exposures: Z(νν) `PILOT_HS` = 2.3×10⁶
  events, DIF and each NI radius 10⁶ events, i.e. κ = max(pool floor κ, N_t / pilot events) (`K_PIL`); every other term
  at its Table 4.4a pool floor κ with m = 0; multijets at the planning floor `MJK`; pile-up `PU9` (R09 EST, width 0.59,
  cap draw). Threshold: B₅₀ ≤ 300 → "below", else "above".
- *Empty-pilot row*: all terms m = 0 on the above κ; 16–84 % from the same predictive pmf.
- *Z(νν) pilot row*: as the empty row, Z(νν) at κ_pilot = 10.9 events per count with m pilot counts.
- *(γ) rows*: DIF and NI empty at pilot κ; every SM process (`SMSET`) at its pool κ with m = m_H × M_t / M_Z(νν)
  (H per event as Z(νν)); multijets at m_H × 10⁶ / M_Z(νν). m_H is in **pool** counts, pilot equivalent m_H × 2.3×10⁶ /
  1.1×10⁷. (The Table 4.4c (γ) row, 56 / 133 / 398, has DIF and NI at their pool floors: the "lower edge" of the
  verdict §1.2.)
- *(β) row*: not computed; text only (credit is post-freeze, read as (γ)).
- *(α1) no-credit rows*: "after CKF" = the Table 4.4c row (`pmf_cache`, counted DIF + conversions on pool κ);
  "own hits" = sum of medians of `kap_nodif` floors (m + 0.67) + pile-up median + (DIF + conversions)/(1 − ε_pair), ε_pair
  = 0.8 / 0.98 assumed.
- *(α1′) row*: the v7 U1_II line (same sum-of-medians reading, conversions at their own fall, photon rate 0.379).
- *(c) credit rows*: the Table 4.4c (α1) row with v1's pile-up fit-probability fraction 2/35 on DIF and conversions
  (EST; only in a (c) test).
- *Rejection grid*: bisection (16 steps, geometric) on `pmf_pred` for the conversion rejection x with B₅₀ ≤ 300, terms
  `kap_nodif` + DIF at f_D × (α1) DIF on pool κ_DIF + conversions G_A1P × rate factor / x on the Z(νν) κ; G_A1P = the
  (α1′) conversion level 9,527 at rate 0.379; rate 0.255 via `F_GAM`; "none suffices" when B₅₀ > 300 with the conversions
  removed. These rows use pool κ (the Table 4.4c basis of the (α1) terms), not pilot κ.

**Script outputs v7 → v8** (`diff budget_stdout_v7.txt budget_stdout_v8.txt`): `353a354,376` (23 lines added, the v8
block) and `373c396` (the one ordered label change: "(day-15 class limit m_H = 125)" → "(day-15 class limit: m_H = 125
in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)"). Every other v7 line is byte-identical; **all v7
values unchanged.** `--stat`: 24 insertions, 1 deletion.

## 3. Text items S2–S19 and the tables

All applied with the verdict's text; bracketed values replaced by the printed ones (all equal). Grep phrases:

| item | section | grep phrase in v8 |
|---|---|---|
| S2 | §0 item 3 | "(scenario (α1′), Table 4.4c) (after CKF, as v1 counted them)" |
| S3 | §0 Expected; §0 leading sentence; §12.5 point 3 | "a term whose S_CKF is not tested stays on all own hits" (3 hits) |
| S4 | §0 upper branches | "the day-15 rule reads the same ceilings as (γ), v8 table" |
| S5 | §0 "The pause." | "It reads every no-pile-up term at"; old "The day-7 and day-15 projections read own hits before CKF (Df-9)" sentence deleted |
| S6 | §0 leading sentence | "on its own-hit basis against a limit of 300" |
| S7 | §4.4 point 4 | "m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 counts in the pilot" |
| S8 | §4.4 point 5 | "the day-15 class corresponds to ≈ 20 Z(νν) pilot counts" |
| S9 | §4.4 Scenarios (β) and (γ) | "(β) is a result after the freeze: at day 15" |
| S10 | Table 4.4c caption | "These rows are the projection of the result" |
| S11 | §4.4 What is not known | "≈ 20 in the pilot; reach ≈ 560 GeV) is the expected" |
| S12 | §11.7 inputs | "(used only in the test of a Q2 (c) redesign)" |
| S13 | §11.7 rule 1 | "never at a central zero" |
| S14 | §11.7 rule 1 | "on the pilot, ≈ 20" |
| S15 | §12.1 Q2 stem | "What the day-15 rule reads, by branch" |
| S16 | §12.1 Q2 stem | "This branch also pauses (table)" |
| S17 | §12.1 Q2 (c) | "no conversion rejection suffices: with the conversions removed"; "At v1's central size (c)" |
| S18 | §12.1 Q2 rider (1) | "(expected to trigger: the day-7 reading" |
| S19 | §12.1 Df-9 row | "it also sets the basis of the day-7 and day-15 projections" |
| S20 | script l.911 | (stdout) "about 20 pilot counts: v8 table" |

**Tables (orchestrator instruction).** Both printed tables are inserted **verbatim** from `budget_stdout_v8.txt` as fenced
blocks: the day-15 table (stdout l.354–369) in the Q2 stem directly after the S15 table, the (c) rejection grid (stdout
l.370–376) inside Q2 (c) after the S17 paragraph. Each has a caption stating what rule 1 measures (own hits before CKF,
no S_CKF, no conditional credit, no credit that exists only after the freeze), the threshold (B₅₀ > 300 pauses), and
"ESTIMATE, v1 placeholder inputs; the decays-in-flight term rests on 1–2 v1 counts; the ×5–50 between the before-CKF
reading and v1's after-CKF figure rests on an assumed pair efficiency". The S15 short table is kept as the verdict
orders; every number in it equals a printed line. The verbatim blocks therefore duplicate the S15 table's content;
I kept both so that S15 is applied exactly and the printed lines are quoted unparaphrased.

## 4. C items applied (14)

| item | status | where / grep phrase |
|---|---|---|
| Ph C-1 ("assumed" on ×5–50) | RESOLVED, inside S5 | §0: "(ε_pair assumed 0.8–0.98, not measured, and not bounded above)" |
| Ph C-2 (zero-survivor development fraction) | RESOLVED, S13 | §11.7 rule 1: "never at a central zero" |
| Ph C-4 (rider's γ overlays preferred) | RESOLVED | §4.4 point 4: "its 1,000 γ overlays on the v2 chain are the preferred sample" |
| Ph C-5 (short O2 form) | RESOLVED, S3 | "a term whose S_CKF is not tested stays on all own hits" |
| Ph C-6 / Cr C1 (duplicated parenthesis) | RESOLVED | §4.11 point 3: "sample-size limited\" while the ceilings count few events** (by v1's conversion counts the" |
| Cr C2 (two parentheses side by side) | RESOLVED, S3 | §0: "per event; after\n  CKF, as v1 counted them, a lower value:" |
| Cr C3 (§0 item 3 label; "1–2 counts" copies) | RESOLVED, S2 + S5/S6/S11/S17 | "(after CKF, as v1 counted them) (with" |
| Cr C4 (§4.17 row 4 role) | RESOLVED | "completeness classes; for the conversions, the Q2 (c) development estimate, §11.7 rule 1" |
| Cr C6 (COM doubled "and") | RESOLVED | COM header: "(version 4),\n`STRATEGY_gunnar…` (version 5), `STRATEGY_ingrid…` (version 6) and\n`STRATEGY_jules…` (version 7)"; pointer to v8; version-8 row "day-15 reading by branch stated from the script table (V1)" |
| Cr C7 ([L13] label) | RESOLVED | §7: "a counted background of ≈ 10⁴ events (after CKF, as v1 counted them)" |
| Co C1 (rider expected to fire) | RESOLVED, S18 | "(expected to trigger" |
| Co C2 (Df-9 sets the basis) | RESOLVED, S19 | "it also sets the basis of the day-7 and day-15 projections" |
| Co C4 (rule-1 inputs list S_CKF) | RESOLVED, S12 | "(used only in the test of a Q2 (c) redesign)" |

Not applied, as ruled: Co C3 (package only), Cr C5 and Cr C8 (deferred). Gate-A package corrections (§7 of the verdict)
are not part of this fix.

## 4b. Orchestrator-ordered additions O3–O5 (beyond the verdict; source: this report's own "not done, proposed")

| item | status | where (section + grep phrase) |
|---|---|---|
| O3: basis label on §0 "(projected B₅₀ 590–980; (α1))" | RESOLVED | §0 Summary item 3: "(projected B₅₀ 590–980; (α1); after CKF, as v1 counted them; the day-15 rule reads this branch on all own hits, (α1)\n rows of the v8 table". Basis confirmed from printed lines, not assumed: stdout v8 l.314 / l.316 (Table 4.4c rows "alpha1 (pile-up fall x339/x201), no credit (R09 = R08): DIF 385 + conversions 183 \| 548 / 587 / 626" and "DIF 647 + conversions 308 \| 925 / 975 / 1025") and l.365–366 of the v8 table, whose basis cell reads "after CKF (Table 4.4c)" for 587 / 975. 590–980 is their rounding; the "570–960 events" in the same sentence are 385 + 183 = 568 and 647 + 308 = 955 from l.314/316. No number changed. |
| O4: "v7 line" → "U1 line" | RESOLVED | §11.7 rule 1: "script [9b], U1 line). Only the test"; §12.1 Q2 stem: "script [9b], U1 line). What the day-15". The cited line (stdout v8 l.353, "v7 (U1): (alpha1') on the day-15 own-hit basis") is unchanged. |
| O5: runtime note | RESOLVED | Code reference: "about 90 seconds, measured on einstein for version 8: 1 min 30 s wall, 35 MB" (the `/usr/bin/time -v` run of this cycle). |

Declined: none. The Q2 duplicate-table proposal was withdrawn by the orchestrator (package matter); both tables stay.
§13.7 has a new row "O3–O5 (orchestrator-ordered, beyond the verdict; from the fixer's own proposals)".

## 5. Sweep of v8 (re-run by me)

Terms grepped in v8 before §13: "pause", "avoid", "300", "×31", "×5–50", "(α1", "(β)", "(γ)", "S_CKF",
"fit-probability", "rejection", "veto", "day-7", "day-15", "before CKF", "after CKF", "suffice" — 209 hit lines.
"avoid": 0; "×31": 0 (the only x31 is ASCII "x31.0" in the printed comparison line); "suffice": only "no … suffices" /
"none suffices"; "m_H ≈ 125": only with "pool counts for Z(νν) alone" (2 hits).

Hits that are not in the family (other meaning of the word; no branch, factor, bar or day-7/15 basis): "300" as rows,
fb⁻¹, GeV values, ×100–300 width steps or 270–300 GeV (l.71, 112, 189, 789, 971, 1511, 1522, 2050, 2117, 2151,
2215–2228, 2646, 2794, 3000); "veto" as the lepton veto or the B3 design (l.162, 206, 295, 655, 917, 1226–1292, 1795,
1935–1943, 2166, 2253, 2292); "fit-probability" / "S_CKF" as definitions of cuts, rungs, widths and the Df-9 factor
(l.284, 479–516, 761–798, 846, 1012–1014, 1086, 1148–1191, 2344, 2577, 2931, 2969); "day-15" as the reserve, calendar
or deadline (l.122, 128–129, 458, 932, 1046, 1395, 2118, 2524–2535, 2572–2609, 2668, 2692–2693, 2716, 2892, 2904–2915);
"(γ)"/"(β)" as the q q̄(γ) systematic, the photon count M = 13 or δ(β) (l.244, 1999, 2002, 2146).

Family statements (v8 line numbers as of the first pass; after O3 every line from l.63 on is one higher, except rows 2, 29 and 35, which give the final numbers; "table row" = the row of the v8 day-15 table / grid it rests on):

| # | location (section + phrase) | table row cited / rested on | consistent |
|---|---|---|---|
| 1 | §0 item 3, "≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c) (after CKF, as v1 counted them)" (l.60) | result basis, labelled; day-15 reading = (alpha1') row | yes |
| 2 | §0 item 3, "they would add 570–960 events (projected B₅₀ 590–980; (α1); after CKF, as v1 counted them; the day-15 rule reads this branch on all own hits, (α1) rows of the v8 table" (l.62–63, O3) | (alpha1) rows, "after CKF (Table 4.4c)" cell 587 / 975 and own-hit cells | yes (labelled, O3) |
| 3 | §0 Expected, "after CKF, as v1 counted them, a lower value: a term whose S_CKF is not tested…" (l.66–67) | label | yes |
| 4 | §0, "The day-15 rule is expected to pause the study before production (§11.7, Q2)" (l.73) | (alpha1') row, above | yes |
| 5 | §0 upper branches, (α1) 420–455 GeV "earn no fit-probability credit" (l.74–76) | post-freeze reach; no pause claim | yes |
| 6 | §0 upper branches, "(β) … (a result after the freeze: … the day-15 rule reads the same ceilings as (γ), v8 table)" (l.77–78) | (beta) row → (gamma) rows | yes |
| 7 | §0 "(α1) 84 % edge ≈ 310–370 GeV" (l.81) | reach, no pause claim | yes |
| 8 | §0 The pause, "pauses the study … if the projected B₅₀ exceeds 300 … preliminarily at day 7" (l.89–90) | threshold | yes |
| 9 | §0 The pause, "reads every no-pile-up term … before CKF … no S_CKF, no conditional (no veto, no fit-probability credit) … after the freeze" (l.90–93) | rule-1 basis = table header | yes |
| 10 | §0 The pause, "expected ×5–50 above the after-CKF figures (ε_pair assumed …)" (l.93–94) | (alpha1) after-CKF vs own-hit cells | yes |
| 11 | §0 The pause, "B₅₀ ≈ 5.0×10⁴–5.1×10⁵ … ((α1′)) and ≈ 2.8×10³–4.8×10⁴ … ((α1)): the pause is the expected branch" (l.94–95) | (alpha1') row; (alpha1) own-hit cells | yes |
| 12 | §0 The pause, "below 300 only if … B₅₀ ≈ 75 … Z(νν) alone … ≈ 20 … ≈ 60 pool-equivalent counts (≈ 13 in the pilot) … ((β) is read as (γ) at day 15)" (l.96–98) | empty row (75); Z(nunu) row (300 at m = 20); (gamma) rows (294 at 60, 331 at 70); (beta) row | yes |
| 13 | §0 The pause, "A conversion veto or a fit-probability credit enters only the test of a Q2 (c) redesign" (l.98–99) | (c)-only rows | yes |
| 14 | §0, "If the pause fires … If the pause does not fire" (l.99–102) | conditional branches, no reading claim | yes |
| 15 | §0 leading sentence, "after CKF, as v1 counted them, a lower value: a term whose S_CKF…" (l.109–110) | label | yes |
| 16 | §0 leading sentence, "expected to pause … (projected B₅₀ ≈ 5×10⁴–5×10⁵ on its own-hit basis against a limit of 300); a conversion veto can count only in a Q2 (c) redesign … no conversion rejection suffices without a reduction of the decays in flight" (l.113–116) | (alpha1') row; grid row f_D = 1 | yes |
| 17 | §4.4 point 4, "conversion part … m_H ≈ 1.6×10³ … (≈ 3×10² in the pilot) (after CKF; …), far above the day-15 class (m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 counts in the pilot, script [9b] v8 table)" (l.793–794) | Z(nunu) row (≈ 20 pilot) | yes |
| 18 | §4.4 point 4, "C′_PU … the development estimate of a Q2 (c) redesign (if the rider is taken …)" (l.828) | (c) test sample, no reading | yes |
| 19 | §4.4 point 5, "pilot expects few counts (Z(νν): 0.4–3.7 … CKF, 2–190 option (a) …)"; "H … enters the day-7 and day-15 projections as Gamma(m + 1) of the pilot count m (… 12 events …; … the day-15 class corresponds to ≈ 20 Z(νν) pilot counts (script [9b], v8 table))" (l.873–875) | Z(nunu) row | yes |
| 20 | Table 4.4c caption, "These rows are the projection of the result … The reading of the day-15 rule, which admits none of these credits, is the v8 table of script [9b], quoted in Q2" (l.959–961) | whole table | yes |
| 21 | Table 4.4c rows (β), (γ) 56 / 133 / 398, (α1) 587–975, (α1) credit 51–74, (α1) ×e^(∓1) 230–373 / 1,563–2,615, (α1′) and (α1′) credit 580–599, (α2) (l.972–980) | result basis per S10 caption; (γ) 56/133/398 = the verdict's "lower edge" basis (pool floors), not a day-15 row | yes (caption) |
| 22 | §4.4 Scenarios (β) and (γ), "(β) is a result after the freeze: at day 15 its Z(νν) credit does not exist yet, and the rule reads the same ceilings as (γ) (… v8 table)" (l.1006–1009) | (beta) row | yes |
| 23 | §4.4 What is not known, "preliminarily at day 7 and bindingly at day 15 … **The day-15 pause (B₅₀ > 300 events; m_H ≈ 125 pool counts for Z(νν) alone, ≈ 20 in the pilot; reach ≈ 560 GeV) is the expected branch** … the reading of each branch … is the v8 table" (l.1022–1026) | (alpha1') row; Z(nunu) row | yes |
| 24 | §4.4 the change of the bound, "(α1) without credit … decades less" (l.1030) | result, no pause claim | yes |
| 25 | §4.6 B3, "rejection by orders of magnitude if the true tail fraction is at the per-cent level" (l.1264) | design statement, not a bar | yes |
| 26 | §4.11 point 3, "The reading expected if the day-15 pause does not fire is …" (l.1666–1668) | conditional; Cr C1 duplicate removed | yes |
| 27 | §7 [L13], "a counted background of ≈ 10⁴ events (after CKF, as v1 counted them)" (l.2295) | label | yes |
| 28 | §11.7 inputs, "S_CKF on the development overlays (used only in the test of a Q2 (c) redesign)" (l.2723) | (c)-only rows | yes |
| 29 | §11.7 rule 1, "N_t·H on all own hits, with no S_CKF and no conditional credit (Df-9); … ×1/(1 − ε_pair) above … (×5–50 at the assumed ε_pair = 0.8–0.98; script [9b], U1 line)" (l.2737–2739, O4) | table header; (alpha1) cells; the U1 line (stdout v8 l.353) | yes |
| 30 | §11.7 rule 1, "Only the test of a Q2 (c) redesign multiplies … EST. A development survival … at most ×n/1.14" (l.2738–2743) | (c)-only rows, grid | yes |
| 31 | §11.7 rule 1, "If B₅₀ is at most 300 events (the bounded class of Q2: reach about 560 GeV …; on the pilot, ≈ 20 Z(νν) ceiling counts …; the reading of each branch is the v8 table …)" (l.2744–2746) | Z(nunu) row | yes |
| 32 | §11.7 rule 1, "the study pauses … By v1's own conversion counts ((α1′)) this is the expected branch" (l.2747–2748) | (alpha1') row | yes |
| 33 | §11.7 decision-point row 3, "without the day-15 pause" (l.2716) | calendar | yes |
| 34 | Q2 stem, "≈ 0.7–1.0×10⁴ … (after CKF, as v1 counted them; a lower value, since terms whose S_CKF test is not evaluable stay on all own hits …)" (l.2790–2791) | label (#19 of the verdict, correct, untouched) | yes |
| 35 | Q2 stem, "expected to pause … count own hits before CKF, with no S_CKF … ×5–50 … B₅₀ ≈ 5.0–5.1×10⁴ … 5.0–5.1×10⁵ … assumed …; script [9b], U1 line)" (l.2796–2799, O4) | (alpha1') row; the U1 line | yes |
| 36 | Q2 S15 table, six rows (l.2800–2807) | each = a printed row (alpha1'); (alpha1) both cells; (gamma) ×6 + (beta); Z(nunu) m = 20 → 300; empty 75 [38–148]; (c) credit 51 / 74 | yes |
| 37 | Q2 caption and verbatim day-15 block (l.2809–2828) | the table itself | yes |
| 38 | Q2 stem, "This branch also pauses (table). Further upside, after the freeze and statistics-only: (β) … every ceiling empty … Their day-15 readings are the (γ) and empty-ceiling rows" (l.2832–2835) | (alpha1); (gamma); empty | yes |
| 39 | Q2 question, "If the day-15 projection exceeds B₅₀ = 300 events …" (l.2836) | threshold | yes |
| 40 | Q2 (a) "Pause and ask you at day 15"; (b) "no pause for this cause" (l.2837–2839) | options as ruled, default (a) unchanged | yes |
| 41 | Q2 (c), "It works if the projected B₅₀ is at most 300, with the redesigned conditional and S_CKF estimated on development samples (EST …)" (l.2848–2849) | (c) test | yes |
| 42 | Q2 (c), "At v1's central decays-in-flight size (385–647 events, resting on 1–2 counts) no conversion rejection suffices: … 401–663" (l.2849–2850) | grid f_D = 1 "none suffices"; v7 [9b] line 401/663 | yes |
| 43 | Q2 (c), "at least ×34 (97.0 %) [×23] … ×52–81 (98.1–98.8 %) [×35–55] … ×69–235 (98.6–99.6 %) [×47–159] at ×e⁻¹" (l.2851–2853) | grid f_D = 0, 1/4, e^-1 | yes |
| 44 | Q2 (c), "no surviving conversion among n … at most ×n/1.14 (§11.7 rule 1)" (l.2853–2854) | rule 1 (S13) | yes |
| 45 | Q2 (c), "If S_CKF cannot be estimated … every factor must be ×1/(1 − ε_pair) larger (×5–50, not measured)" (l.2854–2855) | grid comparison line | yes |
| 46 | Q2 (c) caption and verbatim grid (l.2857–2872) | the grid itself | yes |
| 47 | Q2 (c), "At v1's central size (c) cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 51–74) acts on both. The veto's rejection has not been measured" (l.2874–2877) | grid f_D = 1; (c) credit rows | yes |
| 48 | Q2, "If the projection is at most 300 events (reach ≈ 560 GeV or more …), production proceeds" (l.2878) | threshold | yes |
| 49 | Q2 rider (1), "day-7 preliminary B₅₀ is at least 3,000 events (10× the class) (expected to trigger: the day-7 reading is expected at ≈ 5×10⁴–5×10⁵)" (l.2883) | (alpha1') row | yes |
| 50 | Q3, "Reach under the default: (β) of Table 4.4c: 705–640 GeV" (l.2898) | post-freeze result | yes |
| 51 | Q4, "the pause is the expected branch and costs ≈ 2 days" (l.2905–2906) | (alpha1') row | yes |
| 52 | Df-9 row, "S_CKF, credited only where tested …; it also sets the basis of the day-7 and day-15 projections (own hits, no S_CKF, §11.7 rule 1)" (l.2938) | table header | yes |
| 53 | annex route 5, "(β) … then becomes (γ)-like" (l.2956) | post-freeze | yes |
| 54 | annex route 6, "S_CKF NOT TESTED … ×1/(1 − ε_pair) above H_CKF (×5–50)" (l.2957) | label | yes |
| 55 | annex B4-e, "4.6×10³ events … by itself above the day-15 class" (l.2958) | threshold comparison | yes |
| 56 | §12.5 point 2, "near 600–1,000 events if … (Table 4.4c, (α1))" (l.2993–2994) | result basis, no pause claim | yes |
| 57 | §12.5 point 3, "(α1′) … after CKF, as v1 counted them, a lower value: a term whose S_CKF is not tested …; The day-15 rule pauses the study (Q2)" (l.2997–3001) | (alpha1') row | yes |
| 58 | stdout l.396 (old l.373), "(day-15 class limit: m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)" | Z(nunu) row | yes |

**Result: 58 family statements found (the verdict's 40 plus finer splitting and the Table 4.4c rows, the §12.5 and Q4
mentions); all consistent with the v8 table.** Every statement of a day-15 pass/fail either cites the v8 table (script
[9b]) or follows from a printed row with the basis stated; the v7 forms that were wrong appear only in §13.7 as history.

## 6. Diff v7 → v8 (strategy)

After O3–O5, `diff` gives 32 hunks (the 29 below plus 62c62,63, 2731c2739, 3037c3112; hunk 2789 also carries O4). Hunk → item (v7 line numbers):

| hunk | item |
|---|---|
| 1c1, 3,5c3,5, 7c7 | bookkeeping: header, fixer line, status (cycle 8) |
| 60c60 | S2 (Cr C3) |
| 62c62,63 | O3 |
| 66,67c66,67 | S3 (Cr C2, Ph C-5) |
| 78c78 | S4 |
| 89,95c89,99 | S5 (Ph C-1, Ph C-6 qualifier) |
| 101,102c105 | S5 (deleted day-7/15 sentence) |
| 107c110 | S3 (leading sentence) |
| 111,112c114,116 | S6 |
| 790c794 | S7 |
| 824c828 | Ph C-4 |
| 871c875 | S8 |
| 955c959,961 | S10 |
| 1002c1008,1009 | S9 |
| 1017,1019c1024,1026 | S11 |
| 1660c1667 | Cr C1 / Ph C-6 |
| 2087c2094 | Cr C4 |
| 2288c2295 | Cr C7 |
| 2716c2724 | S12 (Co C4) |
| 2731c2739 | O4 (§11.7 rule 1) |
| 2734c2741,2743 | S13 (Ph C-2) |
| 2736,2737c2745,2746 | S14 |
| 2789c2799,2831 | S15 + the verbatim day-15 table with caption (orchestrator instruction); O4 (Q2 stem, same line) |
| 2791,2796c2832,2835 | S16 |
| 2810,2815c2849,2876 | S17 + the verbatim rejection grid with caption (orchestrator instruction) |
| 2822c2883 | S18 (Co C1) |
| 2877c2938 | S19 (Co C2) |
| 2937,2938c2998,2999 | S3 (§12.5 point 3) |
| 3032a3095,3107 | bookkeeping: §13.7 Changes since version 7 (incl. the O3–O5 row) |
| 3037c3112 | O5 (code reference runtime) |

**Unattributed hunks: 0.**

Script: `852a853,905` (item S block) and `911c964` (S20). COM: header pointer to v8 (3,4c3,4), Cr C6 (6,7c6,8),
version-8 row (28a30,35). Nothing else changed in any file.

Not changed (checked by the diff): the default (a) and the wording of options (a)/(b), all expected-outcome numbers,
acceptance criteria, sample sizes, CPU-h and calendar figures, Table 4.4c rows, §11.2, Q1, Q3, Q4, Q5, the annex.

## 7. Numbers: mine vs the arbiter's

Identical in every printed cell (§2). The only rounding judgment: "≈ 2.8×10³–4.8×10⁴" for the printed 2.85e+03 …
4.78e+04; the unrounded value 2,849 confirms 2.8. Z(νν) at m = 20 is exactly 300 and the block classes it "below" (≤ 300),
as the verdict's text "≈ 20" assumes.

## 8. Not done, proposed

- (Applied since as O3, O4, O5: §4b.)
- Table 4.4c caption: it now says the day-15 reading is the v8 table; the S15 table and the verbatim block duplicate
  each other in Q2. The orchestrator may prefer only one for the Gate-A package (the package uses the short form, verdict §7 item 6).
- Gate-A package corrections (verdict §7, 11 items) are for the package writer, not applied here.
