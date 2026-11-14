# Physics review, cycle 8: STRATEGY v8 (Leopold, 2026-11-14 05:00)

Reviewer: Ludmila (physics), fresh session. I read the role file, FRAMING.md, STRATEGY v8, the v7→v8 diff, script
`src/strategy_budget.py` (blocks [9]–[9b]), `budget_stdout_v7/v8.txt`, the cycle-7 arbiter verdict, Katya's cycle-7
physics review and the cycle-7 fix report. I did not read the methodology or the conventions. Scope as ordered: the
two v8 tables, their definitions against rule 1, the family-V1 statements, and the "unchanged elsewhere" check.

My recomputations load the script with `runpy` (stdout suppressed) and call its own `pmf_pred`, `rows`, `K_PIL`,
`ALPHA`, `kap_nodif` and `PU9`, using the same seed. Scratch files are `rc.py`, `rc2.py` and `rc3.py` in the session
scratchpad; the log is `logs/physics_ludmila_2026-11-14_05-40.md`. I also opened the v1 record
(`C12FC_v1/background.json`). Its counts per 500 events with pile-up are: conversions 86 / 13 / 2 at R05 / R06 / R07
(the R07 value is the conditional 2/13), and decays in flight 81 / 2 / 1. The photon rates are 0.3786 (maximum) and
0.2552 (N_trig-weighted). The script's inputs match these.

---

## 1. The day-15 table

**What rule 1 measures (§11.7).** At day 15, every no-pile-up term enters at max(zero-count floor, N_t·H).
- H is measured on all own hits before CKF, as Gamma(m + 1) on the **pilot's** count. The exposures are Z(νν)
  2.3×10⁶ events (10.9 events per count), DIF 10⁶ events (65.1 per count), and NI 10⁶ events per radius
  (0.9–1.1 per count).
- No S_CKF, no conditional and no credit that exists only after the freeze. The pile-up term is the
  occupancy-model estimate. At day 7 this is the v1-based R09 EST row, with a median of 6.7, a width of 0.59 and a
  cap drawn at 426·Exp(1).
- The study pauses if B₅₀ > 300.

The table's caption says the same thing ("from the pilot's counts at the pilot's exposures").

### Row by row

| row | what it assumes (my words) | my recomputation | definition vs rule 1 | verdict |
|---|---|---|---|---|
| every pilot ceiling zero | Z(νν), DIF and the three NI terms are zero-count bounds at the pilot exposures. The other twelve SM terms are at their Table 4.4a pool floors; multijets at the planning floor; pile-up as above. | 75 [38–148] reproduced. By hand: Σκ = 84.85, of which the DIF pilot κ is 65.1. The sum of the Gamma(1) medians is 0.693·Σκ + 6.7 = 65.5, and the mean is 91.6. A median of 75 between these is right for a sum dominated by one Exp(1) term. | matches | below: right |
| Z(νν) at pilot count m | as row 1, with Z(νν) = 10.9·Gamma(m + 1) | m = 19 / 20 / 21 give 289 / 300 / 311. By hand at m = 20: Gamma(21) median 20.67 × 10.9 = 225, plus the rest (mean ≈ 82) gives ≈ 300. | matches | crossing at 20 pilot counts: right |
| (γ), m_H = 10…100 **pool** counts | every SM process at H per event equal to Z(νν)'s. Each process is a separate Gamma(m_t + 1) on its **pool** κ (m_t = m_H·M_t/M_Z); DIF and NI empty at the pilot exposures. | 104 / 180 / 255 / 294 / 331 / 448 reproduced. By hand, the Σ(m + 1)κ means are 121 / 197 / 273 / 311 / 349 / 462. | **does not match** (W1). At day 15 the H of this branch is the one Z(νν) pilot count, applied to all SM: a single λ ~ Gamma(m_p + 1)/2.3×10⁶ times ΣN_t + N_MJ (×1.663 N_Z). | see W1: at 13 pilot counts the reading is 318 (above), not 294 (below) |
| (β) | not a day-15 branch; read as (γ) | — | right physically: the B4-c credit exists only after the freeze. It inherits the (γ) exposure defect. | — |
| (α1) no credit | after CKF (the Table 4.4c row), and own hits = floors + PU + (DIF + γ)/(1 − ε) | By hand: (385 + 183)/0.2 + 8.8 + 6.7 = 2.85×10³ and /0.02 = 2.84×10⁴; (647 + 308)/0.2 = 4.79×10³ and /0.02 = 4.78×10⁴. | own-hit cells match. The after-CKF cell is labelled as such and is not a rule-1 reading. Pool floors instead of pilot floors change it by +11, which is negligible. | above: right |
| (α1′) no credit | as (α1) with conversions at 9,527 | By hand: (385 + 9527)/0.2 = 4.96×10⁴ and (647 + 9527)/0.2 = 5.09×10⁴; ×10 at ε = 0.98. | matches | above: right |
| (c) only: (α1) with credit | v1's pile-up fraction 2/35 on DIF and conversions (log-normal of width 0.43); S_CKF implicitly at v1's after-CKF value; pool floors | 51 / 74 reproduced. With the non-DIF terms at pilot exposures: 61 / 84. With DIF at its pilot zero-count floor (22–37 events is below that floor of ≈ 45–65): 84 / 92. | basis is mixed (W1), but the row is labelled EST and "(c) only" | below: right under every exposure choice |

**Double counting and omissions.** I see no double counting. The conversions are counted on the Z(νν) κ beside a
Z(νν) ceiling at m = 0, which is the Table 4.4c convention.

The pile-up term in every row carries v1's pile-up fit-probability fraction 2/35 (R09 = R08 × 2/35). This is not a
breach of "no conditional". Rule 1 names the occupancy-model estimate for the pile-up term explicitly, and the model
takes its R09 pass fraction from candidates passing R06 (§4.0 point 7). It is also not material at 6.7 events
(C-3 below).

The omission is W1: the rows after row 2 do not use the exposures the caption states.

---

## 2. The rejection grid for Q2 (c)

**As coded, it is reproduced exactly.**

| f_D | 0.379 | 0.255 | spot checks |
|---|---|---|---|
| 0 | ×34 | ×23 | ×33.7 exactly; ×34 → 297; ×31 → 324 |
| e⁻¹ | ×69 / ×235 | ×47 / ×159 | ×69 → 301, so the cell is ×69.4 rounded; ×235 → 300; 0.255: ×47 → 299, ×159 → 300 |
| 1 | none suffices | none suffices | DIF alone gives 401 / 663 |

The claims "none suffices at v1's central size", "minimum ×34", "324 at ×31" and "×69–235 [×47–159] at ×e⁻¹" are
the true outputs of `_need()`.

**Physical honesty.**

(i) *The qualitative content is right and honestly stated.* At v1's central decays-in-flight size no conversion
rejection suffices. Any (c) redesign must also reduce the decays in flight. The fit-probability route acts on both
the DIF and the conversions (the "(needs (c) to target DIF)" tag in the table, the Q2 text at l.2876–2877). Every
gain is an unmeasured EST: the caption, "the veto's rejection has not been measured", and the S13 zero-survivor rule
(×n/1.14) all say so.

(ii) *The basis stated in the caption is not the basis computed (W1).*
- The caption (l.2859–2861) says the remaining terms are "read as rule 1 reads them".
- `_need()` instead uses `kap_nodif`, the **pool** floors (Σκ = 8.8, against 19.7 at the pilot exposures). It counts
  DIF on the pool κ (2.67) and conversions on the pool Z(νν) κ (2.28).
- At f_D = 0 it drops the DIF term entirely, its zero-count floor included. Rule 1 keeps that floor: max(floor,
  N_t·H). On the pilot's 10⁶ DIF events the floor is 65 events per count, and a day-15 projection cannot show the
  decays in flight smaller than that.
- The fix report says this openly (l.65–67: "These rows use pool κ … not pilot κ"). The human-facing caption does not.

My recomputation on the exposures the caption names (`rc2.py`, `rc3.py`):

| f_D | as printed (0.379 [0.255]) | non-DIF terms at pilot exposures | also DIF at its pilot exposure (floor kept) and conversions on the Z(νν) pilot κ |
|---|---|---|---|
| 0 | ×34 / ×34 [×23] | ×35 [×24] (×43 [×29] with the DIF pilot floor kept) | **×46 [×31]** |
| 1/4 | ×52 / ×81 [×35 / ×55] | ×55 / ×90 [×37 / ×60] | ×80 / ×172 [×54 / ×116] |
| e⁻¹ | ×69 / ×235 [×47 / ×159] | ×75 / ×311 [×51 / ×209] | **×127 / none suffices [×86 / none]** |
| 1/2 | ×110 / none [×74 / none] | ×124 / none [×84 / none] | ×391 / none [×264 / none] |
| 1 | none | none | none |

With the DIF floor kept, the printed bar of ×34 gives B₅₀ = 358, which is above 300. The printed grid is therefore
the **lower edge** of the bar. The day-15 reading demands more: at f_D = 0, ×43–46 (97.7–97.8 %) rather than ×34;
at ×e⁻¹ with the ×201 fall, no conversion rejection suffices rather than ×235.

The direction is the same as the qualitative message, and it strengthens it. But these are numbers shown to the user
on the only designed route beyond the bounds: Q2 (c), l.2852–2854. Cycle 7 classed the same kind of error (×31 vs
×34) as B.

(iii) *"Every factor ×1/(1 − ε_pair) larger" without an S_CKF estimate* (grid footnote; Q2 l.2855–2856). This is
right only if "every factor" includes the DIF reduction f_D. DIF is also on own hits at day 15, so without S_CKF the
DIF term grows ×5–50 as well. Every f_D > 0 cell would then read "none suffices" unless f_D itself is ×1/(1 − ε)
smaller. Clarify the wording (C-1).

---

## 3. Captions and caveats

- **Day-15 table caption (l.2810).** It states what rule 1 measures (all own hits before CKF, pilot counts at pilot
  exposures, no S_CKF, no conditional, no post-freeze credit), the threshold (pause if B₅₀ > 300), ESTIMATE on v1
  placeholder inputs, that the DIF term rests on 1–2 v1 counts, the ×5–50 on an assumed ε_pair, and the (c) status.
  All of this is present and correct as a statement of rule 1. It is **not correct as a description of the rows**:
  the (γ), (c) and (α1)-after-CKF rows are not at pilot exposures (W1).
- **Grid caption (l.2858–2863).** The threshold, the EST status, the 1–2 counts and the assumed ε_pair are present.
  "Remaining terms read as rule 1 reads them" is inaccurate (W1).
- The verbatim stdout blocks match `budget_stdout_v8.txt` l.354–376 line for line.

---

## 4. Agreement of the text with the tables

I swept §0, §4.4 (l.790–796, 871–877, 955–962, 1007–1027), §11.7, Q2 with its table, grid and rider, the Df-9 row and
§12.5, for all the listed phrases. Each statement below is compared with the printed rows.

| # | place | statement | agrees with table? |
|---|---|---|---|
| 1 | §0 l.60 | (α1′) ≈ 1.0×10⁴ "(after CKF, as v1 counted them)" | yes (label correct) |
| 2 | §0 l.62–63 (O3) | "projected B₅₀ 590–980; (α1); after CKF, as v1 counted them; the day-15 rule reads this branch on all own hits, (α1) rows of the v8 table" | yes. 590–980 rounds 587–975 (Table 4.4c, statistics-only) or 589–979 (w = 0.17 log-normal); both are after-CKF v1 counts. **The O3 label is correct.** |
| 3 | §0 l.66–68, l.110–111, §12.5 l.2999–3000 | 0.7–1.0×10⁴ after CKF; an untested S_CKF term stays on own hits ×1/(1 − ε) higher | yes |
| 4 | §0 l.74, l.114 | the day-15 rule is expected to pause | yes ((α1′) row) |
| 5 | §0 l.79 | (β) is a post-freeze result; the day-15 rule reads its ceilings as (γ) | yes |
| 6 | §0 l.90–96 | rule-1 statement; ×5–50; 5.0×10⁴–5.1×10⁵; 2.8×10³–4.8×10⁴ | yes |
| 7 | §0 l.97 | B₅₀ ≈ 75 with every pilot ceiling at zero | yes |
| 8 | §0 l.98 | Z(νν) alone up to ≈ 20 pilot counts | yes |
| 9 | §0 l.98–99 | "every SM ceiling up to ≈ 60 pool-equivalent counts (≈ 13 in the pilot)" | **agrees with the printed row, but the row is mis-defined (W1).** At day 15 the crossing is at 12 pilot counts (12 → 300.0; 13 → 318). |
| 10 | §0 l.99–100 | a veto or fit-probability credit enters only a (c) test | yes |
| 11 | §0 l.115–117 | 5×10⁴–5×10⁵; no conversion rejection suffices without a DIF reduction at the central size | yes |
| 12 | §4.4 l.795 | m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 in the pilot | yes. The two are different readings (pool basis against the pilot basis; 125 pool counts ≈ 26 pilot-equivalent counts). The wording "pool counts … ; ≈ 20 in the pilot" does not claim they are equivalent. Acceptable. |
| 13 | §4.4 l.876 | pilot zero = 12 events for Z(νν); day-15 class ≈ 20 pilot counts | yes (1.14 × 10.9 = 12.4) |
| 14 | §4.4 l.960–962 | Table 4.4c rows are post-freeze projections; the day-15 reading is the v8 table | yes |
| 15 | §4.4 l.1009–1010 | (β) read as (γ) at day 15 | yes (inherits W1 for the numbers) |
| 16 | §4.4 l.1024–1027 | pause = B₅₀ > 300, m_H ≈ 125 pool / ≈ 20 pilot, ≈ 560 GeV; expected branch | yes |
| 17 | §11.7 l.2737–2739 | no S_CKF, no conditional; ×5–50 (U1 line) | yes |
| 18 | §11.7 l.2742–2744 | S13: a development fraction at its 68 % upper value; zero survivors among n → at most ×n/1.14 | yes. Physically right and conservative. |
| 19 | §11.7 l.2745–2747 | ≈ 20 Z(νν) pilot counts, other ceilings empty; each branch from the v8 table | yes |
| 20 | Q2 l.2796–2799 | ×5–50; 5.0–5.1×10⁴ / 5.0–5.1×10⁵ | yes |
| 21 | Q2 table l.2803–2804 | (α1′) and (α1) rows | yes |
| 22 | Q2 table l.2805 | (β)/(γ) "104 / … / 448 \| below up to ≈ 60 pool counts (≈ 13 in the pilot)" | **W1**: ≈ 12 in the pilot on the rule's own basis; values 113 / 189 / 264 / 318 / 353 / 462 at 2 / 6 / 10 / 13 / 15 / 21 pilot counts |
| 23 | Q2 table l.2806–2808 | Z(νν) 300 at ≈ 20; 75 (38–148); (c) 51–74 | yes (the (c) value is 61–92 at pilot exposures; still below) |
| 24 | Q2 l.2833–2836 | (α1) "also pauses (table)"; (β) and empty-ceiling readings are the (γ) and empty rows | yes |
| 25 | Q2 (c) l.2850–2851 | central DIF size 385–647 on 1–2 counts; no conversion rejection suffices; 401–663 with conversions removed | yes |
| 26 | Q2 (c) l.2852–2854 | "at least ×34 (97.0 %) [×23] even if the decays in flight vanished, ×52–81 [×35–55] at a quarter, ×69–235 [×47–159] at ×e⁻¹" | **agrees with the printed grid; the grid is not on the rule-1 basis (W1).** On that basis: ×43–46 [×29–31]; ×80–172 [×54–116]; ×127 to none suffices [×86 to none]. |
| 27 | Q2 (c) l.2854–2856 | ×n/1.14; "every factor ×1/(1 − ε) larger" | yes, if "every factor" includes f_D (C-1) |
| 28 | Q2 (c) l.2875–2877 | (c) must target DIF at the central size; the fit-probability route acts on both | yes |
| 29 | Q2 l.2879 | "at most 300 events (reach ≈ 560 GeV or more …)" | yes |
| 30 | rider l.2884 | day-7 reading expected ≈ 5×10⁴–5×10⁵, so it is expected to trigger the ≥ 3,000 rule | yes |
| 31 | Df-9 row l.2939 | own hits, no S_CKF for the day-7/15 projections | yes |
| 32 | stdout l.396 | "m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts" | yes (two readings, labelled) |

**Fixer's sweep (58 rows).** I compared the fixer's sweep with my own. Its rows 12, 17, 19, 31 and 58 are the
statements I check above, and I agree with the fixer's "yes" on every row except those that cite the (γ) row
(§0 l.98–99, Q2 table l.2805) and the grid (Q2 l.2852–2854). The fixer marked these as agreeing with the table, and
they do. The table itself is on the wrong exposure.

**Statements disagreeing with the rule-1 reading: 3** (#9, #22, #26), all of one cause (W1). **Statements with no
basis label: 0.** Every number in the list above carries "after CKF", "own hits", "pool", "pilot", "(c), EST" or a
v8-table citation.

---

## 5. Unchanged elsewhere

- **stdout.** `diff budget_stdout_v7.txt budget_stdout_v8.txt` gives 23 added lines (the v8 block, l.354–376) and one
  changed line (old l.373 → new l.396, a label only; the numbers 3.56×10³, 1.56×10³ and 326 are identical). **Every
  v7-printed value is unchanged.**
- **Strategy diff (250 lines).** The physics content is confined to the following.
  - The §0 pause paragraph (now a rule-1 statement plus table citations).
  - The basis labels ("after CKF, as v1 counted them", pool/pilot).
  - The Q2 table and grid, and the (c) paragraph.
  - S13 (the zero-survivor rule): a new, conservative criterion for the (c) test only.
  - The rider's "expected to trigger".
  - The Df-9 row.
  - The §4.17 role column.
  - The runtime note.
- **Unchanged.** Default Q2 = (a) (l.2838, "●"); background ≈ 0.7–1.0×10⁴ after CKF; reach below 243 GeV with
  w = 0.17; the counting-width-only 270–300 GeV (84 % edge), median 315–340, fixed-B 390–420; 4,609 / 5,992 CPU-h;
  60 days. No number of Table 4.4c changed.

---

## 6. Findings

### W1 (Category B): the exposures behind the (γ) rows and the (c) grid differ from the rule-1 basis that their captions state

This is a factual error in numbers shown to the user, and it is a defect of the structural fix itself, so it is
admissible under the cycle-7 rules.

- The day-15 table's caption, and the grid's "remaining terms read as rule 1 reads them", say pilot counts at pilot
  exposures. The code uses that basis only in rows 1–2.
- **(γ):** the SM processes are independent Gamma draws on **pool** κ. At day 15 the only measurement behind this
  branch is the Z(νν) pilot count. The correct reading is one λ ~ Gamma(m_p + 1)/2.3×10⁶ applied to all SM N_trig
  and the multijets. This gives 113 / 189 / 264 / **318** / 353 / 462 at 2 / 6 / 10 / 13 / 15 / 21 pilot counts. The
  crossing is at **12** pilot counts (B₅₀ = 300.0), and the printed "13 pilot counts … 294 … below" is false (318,
  above).
- **Grid:** the remaining terms are at pool floors, DIF and conversions on pool κ, and at f_D = 0 the DIF
  zero-count floor is dropped, which rule 1 keeps. On the rule's basis:
  - minimum ×43–46 (×29–31 at 0.255), not ×34 (×23). The printed ×34 reads 358, which is above.
  - at ×e⁻¹: ×127 to none suffices, not ×69–235.
  - The printed grid is the lower edge.

The qualitative conclusions are unchanged or strengthened: the pause is expected; at the central DIF size nothing
suffices; (c) needs a DIF reduction too. No default, criterion, budget or outcome is affected.

**Fix (mechanical, ≈ 30 min).** In the v8 block of script [9b]:
- (γ) rows: `gam = non_SM_at_K_PIL + [((ΣSM N_t + N_MJ)/PILOT_HS, m_p)]` for m_p = 2, 6, 10, 12, 13, 15, 21.
- `_need()`: base `kap_d15` without DIF plus `[(K_PIL['DIF'], f_D·d/K_PIL['DIF'])]`, keeping the floor at f_D = 0.
  Count the conversions on the Z(νν) pilot κ, or state that the pool κ is kept.
- Optionally the (c) credit rows on `kap_d15`.

Then quote the new printed cells in §0 l.98–99, the Q2 table l.2805 and Q2 (c) l.2852–2854. If the orchestrator
prefers not to change the numbers, the minimum acceptable fix is to change the captions. They must say that the (γ)
and grid rows use pool exposures, are a lower edge of the day-15 reading, and that on the pilot exposures the bar is
×43–46 at f_D = 0 and the (γ) crossing is at ≈ 12 pilot counts.

### C items

- **C-1.** Q2 l.2855 and the grid footnote: write "every reduction, of the conversions and of the decays in flight
  (f_D), must be ×1/(1 − ε_pair) larger". Without S_CKF the DIF term is also ×5–50, so every f_D > 0 cell otherwise
  becomes "none suffices".
- **C-2.** The f_D = e⁻¹ cell "×69" is ×69.4 rounded down: ×69 itself reads 301. Print rejection factors rounded up
  (`math.ceil`) so that each printed bar actually passes.
- **C-3.** For the human: every row's pile-up term is the R09 EST (median 6.7, with v1's pile-up fraction 2/35, as
  rule 1's occupancy-model clause admits). If the best candidate were an R08 selection, the pile-up term would be
  88–148. The empty-pilot reading would then be ≈ 185, and the Z(νν) crossing about 10 pilot counts. One sentence
  in the caption would make the R09 basis explicit.
- **C-4.** Arbiter observation 1 (l.570), restated: one DIF pilot count is 65 events. The day-15 reading is
  dominated by pilot statistics, not physics, whenever the DIF pilot count is above about 3. The text says this only
  implicitly.

---

## 7. Judgment

- **Family V1: PARTIALLY RESOLVED.**
  - Resolved: V1-a ((β) as a pause-avoiding branch), V1-b ("at ×e⁻¹ the conversions alone would suffice"), V1-d (the
    fit-probability credit acts on DIF). No live statement repeats them.
  - V1-c (the (c) bar) is resolved in form, a curve printed by the script, but its numbers are on the pool basis.
    Three statements remain: §0 l.98–99 ("≈ 13 in the pilot"), the Q2 table l.2805 ("≈ 13 in the pilot"), and Q2 (c)
    l.2852–2854 (×34 [×23] / ×52–81 / ×69–235). All come from the one cause, W1.
- **Table recomputation.** Every printed cell is reproduced exactly from the script's functions. Rows 1–2, (α1),
  (α1′) and the (c) credit verdicts are right under rule 1. The (γ) rows and the grid are not on rule 1's stated
  exposures.
- **New findings:** A 0, B 1 (W1), C 4.
- **Overall: not yet. Blocking list: W1 only.** Recompute the (γ) rows and the grid on the pilot exposures, or label
  them as pool-basis lower edges with the pilot-basis bar (×43–46 at f_D = 0; (γ) crossing ≈ 12 pilot counts).
  Then re-quote the three statements. With that done I would approve for execution subject to Gate A. Nothing
  outside the family needs to change.
