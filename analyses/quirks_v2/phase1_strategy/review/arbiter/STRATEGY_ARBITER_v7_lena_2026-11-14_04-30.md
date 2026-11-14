# Arbiter verdict: Phase 1 STRATEGY v7 (quirks v2), review cycle 7

Arbiter: Lena, 2026-11-14 04:30. Fresh session. Role: `agents/arbiter.md`, prompt template followed in full
(cases 1–5, structured table, dismissal rules, regression check, motivated-reasoning check, reviewer-pressure
protection).
Artifact: `phase1_strategy/outputs/STRATEGY_jules_2026-11-14_03-40.md` ("v7"; "l." = a line of v7), `COMMITMENTS.md`
("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v7.txt` ("stdout"),
`outputs/FIX_REPORT_cycle6_jules.md`.
Reviews: physics Katya ("Ph", 0 A, 2 B, 6 C), critical Kenji ("Cr", 0 A, 0 B, 8 C), constructive Klaus ("Co", 0 A,
0 B, 4 C), all 2026-11-14 04:05. There is no plot validator, since Phase 1 has no figures.
Also read: cycle-6 verdict (Johanna, "AV6") in full, `AGENT_RULES.md`.
Computation: standard-library only, on einstein as permitted, with `nice -n 10 python3 -I`. I ran four scratch scripts
that load the script with `runpy` (stdout suppressed) and call its own `pmf_pred`, `rows`, `ALPHA`, `kap_nodif`, `PU9`,
`kz`, `K_DIF`, `G_A1P` and `F_GAM` without modifying it. Each run took ≈ 56 s at 36 MB max RSS. The scratch files are
in the session scratchpad and are not part of the record. Everything I computed is **VERIFIED (scratch run, script
functions)** unless tagged. I used no sub-agents and ran no git commands.

**Verdict: ITERATE.** Category A: none. **Category B: four, one family (V1, §3):** the description, in the text shown
to the human, of how the binding day-15 rule reads each branch and of the Q2 (c) bar.
- V1-a = Ph B-1: (β) is listed as passing.
- V1-b = Ph B-2: "conversions alone would suffice" at DIF ×e⁻¹.
- V1-c, new (case 5): the bar "×31–52 **and** the decays in flight reduced" cannot be met at its ×31 end. At the photon
  rate 0.379 the text uses, ×31 leaves B₅₀ = 324 even with the decays in flight removed entirely.
- V1-d = Ph C-3, promoted: the fit-probability credit that makes (α1) pass acts on the decays in flight, which (c) as
  worded does not target.

I rule for the simpler formulation the task suggests:
- one statement of what rule 1 measures;
- one script-printed day-15 table, branch → B₅₀ under rule 1 → above/below 300, plus the (c) rejection grid;
- the text cites the table and does not paraphrase it.

That removes the family and does not patch its members one by one. It is text plus one script block, 0 CPU-h.

---

## 1. B-1 and B-2: my own computation (case 3)

### 1.1 What rule 1 admits at day 15 (v7 l.2712–2739; Df-9 l.2877; §4.4 point 5 l.869–871)

- Every term enters at max(zero-count floor, N_t·H).
- H is counted on all own hits before CKF, as Gamma(m + 1) of the **pilot** count m.
- No S_CKF, no conditional (veto, fit probability), and no credit that exists only after the freeze. The B4-c test of
  Z(νν) and the S_CKF tests run in 4a.
- Only the test of a Q2 (c) redesign multiplies by a redesigned conditional and by S_CKF estimated on development
  samples (EST).
- Pilot exposures (§4.4 point 5): Z(νν) 2.3×10⁶ events, i.e. 10.9 events per count (script `SM_NTRIG/PILOT_HS`). DIF
  and each NI radius 10⁶ unbiased events: DIF 65.1 events per count (N_t = 6.51×10⁷, script `rows`); NI ≈ 0.9–1.1.
  The Table 4.4c rows use the **pool** exposure instead, 2.28 events per Z(νν) count.

### 1.2 Day-15 B₅₀ by branch (VERIFIED, scratch run; the proposed print block of §4 item S reproduces every line)

| branch | basis | B₅₀ | vs 300 |
|---|---|---|---|
| every pilot ceiling zero (DIF, NI, Z(νν) at their pilot exposures, the others at their Table 4.4a floors) | rule 1 | **75** (16–84 %: 38–148) | below |
| Z(νν) alone at pilot count m = 5 / 10 / 15 / 20 / 25 / 50 (others as above) | rule 1 | 130 / 187 / 242 / **300** / 352 / 626 | below up to **≈ 20 pilot counts** |
| (γ) every SM ceiling at H per event as Z(νν), m_H = 10 / 30 / 50 / 60 / 70 / 100 pool counts (2 / 6 / 10 / 13 / 15 / 21 pilot counts), DIF and NI empty at their pilot exposures | rule 1 | 104 / 180 / 255 / 294 / 331 / 448 | below up to **≈ 60 pool counts (≈ 13 pilot)** |
| the same with DIF and NI at their pool floors (the printed [9b] (γ) row basis; Katya's basis) | lower edge | 56 / 133 / … 284 (70) / 303 (75) / 323 (80) / 398 (100) | below up to ≈ 74 |
| (β) Z(νν) tested and credited | not admissible at day 15 | it becomes (γ) at the same m_H | as (γ) |
| (α1) no credit | after CKF / own hits at ε_pair = 0.8 / 0.98 | 587–975 / ≈ 2.8×10³–4.8×10³ / ≈ 2.8×10⁴–4.8×10⁴ | above |
| (α1′) no credit (expected) | own hits at ε_pair = 0.8 / 0.98 (stdout l.353) | 4.96–5.09×10⁴ / 4.96–5.09×10⁵ | above |
| (α1) with fit-probability credit on DIF **and** conversions | (c) test only, EST | 51 / 74 | below, only if (c) may target DIF |
| (α1′) with fit-probability credit | (c) test only | 580 / 599 (stdout l.351) | above |
| (α1) DIF, conversions removed | (c) test only | 401 / 663 | above |
| (α1) DIF × e⁻¹, conversions removed | (c) test only | 159 / 256 (stdout l.352) | below |

**(a), B-1.** Under rule 1 as written, the branches **below** 300 at day 15 are only these:
- every pilot ceiling (near-)empty;
- Z(νν) alone up to ≈ 20 pilot counts;
- (γ) up to ≈ 60 pool-equivalent counts.

Every (α) branch is above 300, (α1′) by a factor of ≈ 170–1,700. (α1) with credit and the DIF-reduced rows exist only
in the (c) test.

(β) cannot be claimed as avoiding the pause. Its defining credit (Z(νν) "tested and credited", §4.4 l.997, from B4-c
in 4a) is post-freeze. At day 15 the same ceilings are (γ), and (γ) at the stated 10–100 counts gives 104–448: it
crosses 300 at ≈ 60 counts on the rule's own pilot exposures, or ≈ 74 with DIF/NI at pool floors.

**B-1 stands, Category B** (case 3; Katya's 56 / 133 / 398 and "≈ 75" reproduced; my rule-basis crossing is a little
lower). It is a statement shown to the human, on the central Gate-A question, about which branches avoid the pause.

**(b), B-2.** I computed the conversion rejection needed for B₅₀ ≤ 300 by bisection on `pmf_pred`. The conversion term
is the (α1′) level of 9,527 events at the photon rate 0.379; the 0.255 rate is shown in brackets. (α1) DIF is taken at
the ×339 / ×201 fall.

| decays-in-flight size f_D (× v1's central 385 / 647) | rejection needed, rate 0.379 | [rate 0.255] |
|---|---|---|
| 0 (removed entirely) | ×34 / ×34 (97.0 %) | [×23 (95.6 %)] |
| 1/4 | ×52 / ×81 (98.1 / 98.8 %) | [×35 / ×55] |
| e⁻¹ | **×69 / ×235 (98.6 / 99.6 %)** | [×47 / ×159] |
| 1/2 | ×110 / none suffices | [×74 / none] |
| 1 (v1's central) | **none suffices** (401 / 663 with conversions removed) | [none] |

Spot values:
- f_D = e⁻¹ with ×52.1 / ×31.0: B₅₀ 345 / 566.
- ×70: 299.
- ×250 (×201 fall): 298.

All of these reproduce Katya. At v1's central size, with the conversions removed entirely, the decays in flight must
fall by ≥ ×1.36 / ×2.29.

- The v7 sentence "at its size ×e⁻¹ the conversions alone would suffice (B₅₀ 159–256)" is true only for a 100 %
  removal. At the stated ×31–52 it is false (345 / 566). **B-2 stands, Category B.**
- The stated bar itself, "×31–52 (96.8–98.1 %) **and** the decays in flight reduced" (l.2810–2811), is also wrong at
  its ×31 end. At the 0.379 rate, conversions at ×31 give B₅₀ = 324 with the decays in flight at zero, so no DIF
  reduction can complete it. The bar is a curve, ≥ ×34 at f_D = 0; it is not an interval of conversion factors.
  ×31–52 are the (α1) scenario levels, not a bar. **V1-c, new, Category B** (case 5: a factual error in a number shown
  to the user, on the only designed route to a reach beyond the bounds. It is admissible under AV6 §12).
- **Ph C-3 → V1-d, Category B.** The credit that makes (α1) pass (51–74) multiplies DIF 385 → 22 and 647 → 37 as well.
  The text says it is "admitted only under (c)", but (c) "as worded targets the conversions". The pass claim is
  therefore incomplete in the same way as B-1. It is the same sentence (§0 l.94, Q2 l.2794), so it takes the same
  category.

### 1.3 Was the inherited fix text incomplete? Yes.

AV6 §7 items 3c and 5b re-labelled (α1) with credit and left (β) in the list of pause-avoiding branches unchanged. AV6
§7 item 4 wrote "at its size ×e⁻¹ the conversions alone would suffice" and kept "×31–52 **and** the decays in flight
reduced" as the bar. The fixer applied that text verbatim (Cr §1), and Kenji and Klaus verified the application, not
the content.

The defect therefore came from the arbiter's own prescribed text, for the fourth cycle running (P2, R1, U1, now V1).
The lesson for this verdict: the replacement text below cites script-printed rows and claims nothing that is not
printed.

---

## 2. Sweep of the family: every statement in §0, §4.4, §11.7, the defaults and §12 (Gate-A section) that says a branch passes or triggers the pause, gives a suppression factor or bar, or states the basis of a day-7/day-15 number

"Correct" means correct under rule 1 by §1.2. "Label" means correct in substance, but the basis is not stated and a
reader could compare it on the wrong basis.

| # | location | statement (abridged) | status | action (§4) |
|---|---|---|---|---|
| 1 | §0 l.59–61 | (α1′) ≈ 9.5×10³ / ≈ 1.0×10⁴ "the projection contains them" | label (after CKF unstated) | S2 |
| 2 | §0 l.66–67 | 0.7–1.0×10⁴ "(after CKF …; a lower value where S_CKF is not tested)" | correct (two parentheses side by side) | S3 |
| 3 | §0 l.73 | "The day-15 rule is expected to pause the study" | correct | — |
| 4 | §0 l.76–78 | (β) 705–640 GeV, "conditional on the promotion model" | correct as a post-freeze reach; no basis stated | S4 |
| 5 | §0 l.88–90 | pause if B₅₀ > 300 or both estimators miss their cap; preliminary at day 7; expected | correct | S5 (kept) |
| 6 | §0 l.91–93 | (α1) without credit pauses; "neither a steeper fall nor a conversion-removing conditional avoids it on its own at v1's central size" | correct, but it implies that a conditional enters the day-15 projection (it does so only under (c)), and the qualifier is unneeded for the steeper fall (345/566 at ×e⁻¹) | S5 |
| 7 | §0 l.93–95 | avoided "as in (α1) with credit (51–74; only under (c)), (β) and the empty-ceiling case" | **incorrect**: (β) (V1-a), (α1) credit incomplete (V1-d); empty ceilings correct (75) | S5 |
| 8 | §0 l.101–102 | "day-7 and day-15 projections … expected ×5–50 above" | correct; "assumed" missing (Ph C-1) | S5 |
| 9 | §0 l.110–112 | leading sentence: "removing the conversions alone would not avoid the pause" at v1's central size | correct, but implies a veto enters at day 15 | S6 |
| 10 | §4.4 l.790 | conversion part m_H ≈ 1.6×10³ (≈ 3×10² in the pilot) "far above the day-15 class (m_H ≈ 125)" | label: 125 is a pool count for Z(νν) alone; the pilot class is ≈ 20 counts. The conclusion holds a fortiori | S7 |
| 11 | §4.4 l.869–871 | pilot expects Z(νν) 0.4–3.7 (CKF) / 2–190 (option (a)); H enters day 7/15 as Gamma(m + 1) of the pilot count; pilot zero = 12 events | correct; the pilot-count class is not stated | S8 |
| 12 | §4.4 l.997–999 | "(β) and (γ)": Z(νν) has an evaluable B4-c test, so (β) | correct for the result; day-15 reading not stated | S9 |
| 13 | Table 4.4c caption | rows on the result basis, with no statement that the day-15 reading differs | label | S10 |
| 14 | §4.4 l.1016–1019 | "day-15 pause (B₅₀ > 300, i.e. m_H ≈ 125 …) expected; (α1) above; removing conversions alone does not … at central size" | correct; "m_H ≈ 125" label as #10 | S11 |
| 15 | §11.7 l.2716 | inputs include "S_CKF on the development overlays" | label (used only in a (c) test; Co C4) | S12 |
| 16 | §11.7 l.2729–2734 | rule-1 basis sentence; (c) test on EST | correct; how a zero-survivor development fraction enters is undefined (Ph C-2) | S13 |
| 17 | §11.7 l.2735–2737 | "≤ 300 (bounded class: m_H ≈ 125 for Z(νν), reach ≈ 560)" | label as #10 | S14 |
| 18 | §11.7 l.2738–2739 | "By v1's own conversion counts … expected branch" | correct | — |
| 19 | Q2 l.2779–2782 | 0.7–1.0×10⁴ after CKF, a lower value | correct (Ph C-5 short-form remark applies elsewhere) | — |
| 20 | Q2 l.2786–2789 | expected pause; "own hits … ×5–50 … 5.0–5.1×10⁴ / ×10⁵, assumed" | correct | S15 (table added after it) |
| 21 | Q2 l.2791–2793 | (α1) "also pauses … so at v1's central size a conversion veto alone does not avoid" | correct, but implies a veto enters at day 15 | S16 |
| 22 | Q2 l.2793–2796 | "Only branches with B₅₀ ≤ 300 do: (α1) with credit … only under (c); (β) …; every ceiling empty" | **incorrect**: (β) (V1-a); (α1) credit incomplete (V1-d) | S16 |
| 23 | Q2 (a) l.2798 | pause and ask | correct | — |
| 24 | Q2 (b) l.2800 | "no pause for this cause" | correct | — |
| 25 | Q2 (c) l.2809–2810 | works if projected B₅₀ ≤ 300 with conditional and S_CKF on development samples (EST) | correct | — |
| 26 | Q2 (c) l.2810–2812 | "needs the conversions reduced by ×31–52 (96.8–98.1 %) **and** the decays in flight reduced" | **incorrect** at ×31 (V1-c) | S17 |
| 27 | Q2 (c) l.2812 | "with the conversions removed, B₅₀ is 401–663 … of which 385–647" | correct | S17 (kept) |
| 28 | Q2 (c) l.2812–2813 | "at its size ×e⁻¹ the conversions alone would suffice (159–256)" | **incorrect** (V1-b) | S17 |
| 29 | Q2 (c) l.2813–2814 | "If S_CKF cannot be estimated … every reduction ×1/(1 − ε_pair) larger" | correct | S17 (kept) |
| 30 | Q2 (c) l.2814–2815 | "(c) targets the conversions; say whether it may also target the decays in flight" | correct, but does not say that (c) cannot work at v1's central size otherwise | S17 |
| 31 | Q2 l.2817 | "If the projection is at most 300 (≈ 560 GeV or more, statistics-only), production proceeds" | correct | — |
| 32 | rider (1) l.2822 | day-7 B₅₀ ≥ 3,000 puts (b)/(c) to you at day 7 | correct; that it is expected to fire is not said (Co C1) | S18 |
| 33 | Q3 l.2837 | "Reach under the default: (β) 705–640 GeV" | correct (a post-freeze result) | — |
| 34 | Q4 l.2844–2846 | pause the expected branch, ≈ 2 days | correct | — |
| 35 | Df-9 row l.2877 | "S_CKF credited only where tested" | correct for the result; the day-7/15 basis it sets is not stated (Co C2) | S19 |
| 36 | annex route 5 l.2895 | "(β) … then becomes (γ)-like" | correct (post-freeze) | — |
| 37 | annex route 6 l.2896 | "×1/(1 − ε_pair) above H_CKF (×5–50)" | correct | — |
| 38 | annex B4-e l.2897 | 4.6×10³ events "by itself above the day-15 class" | correct (comparison) | — |
| 39 | §12.5 pt 3 l.2936–2940 | after-CKF label; "The day-15 rule pauses the study" | correct | S3 (label form) |
| 40 | script stdout l.373 | "326 in the pilot's 2.3e+06 events (day-15 class limit m_H = 125)" | label: it compares a pilot count with a pool-count limit (pilot ≈ 20) | S20 |

**Result: 40 statements.**
- **4 are incorrect:** #7, #22, #26 and #28. They carry six wrong claims: (β) twice, the (α1) credit twice, the ×31 bar
  once, and ×e⁻¹ "suffice" once.
- **18 need a label or a qualification:** #1, 4, 6, 8–17, 21, 30, 32, 35 and 40.
- **18 are correct as written.**

After §4, no live sentence states a day-15 pass or fail except by citing the v8 table.

---

## 3. Structured adjudication table (cycle 7)

| # | finding | source | their cat | final | rationale |
|---|---|---|---|---|---|
| **V1-a** | (β) listed as avoiding the pause; its Z(νν) credit is post-freeze; under rule 1 it is (γ), above 300 beyond ≈ 60–74 counts | Ph B-1 | B | **B** | Case 3; §1.2 reproduces it. Kenji and Klaus checked that AV6's text was applied, not whether it was right; that is no contradiction on the substance (case 4 does not arise). |
| **V1-b** | "at ×e⁻¹ the conversions alone would suffice" holds only for 100 % removal; ×31–52 gives 345–566; ×69–235 needed | Ph B-2 | B | **B** | Case 3; reproduced (299 at ×70, 298 at ×250). |
| **V1-c** | the (c) bar "×31–52 and DIF reduced" is infeasible at ×31 (324 with DIF = 0); minimum ×34; the bar is a curve in (f_D, rejection) | arbiter | — | **B** | Case 5; §1.2. Katya called ×31–52 "the bar stated two lines earlier" without testing it. |
| **V1-d** | (α1) credit acts on DIF; (c) as worded does not target DIF, so "admitted only under (c)" is incomplete | Ph C-3 | C | **B** | Case 3. The same sentence and the same kind of claim as V1-a. |
| 1 | §0 l.101 "expected ×5–50" without "assumed"; possibly larger | Ph C-1 | C | C (i), inside S5 | |
| 2 | how a zero-survivor development fraction enters the (c) test | Ph C-2 | C | C (i), inside S13 | Closes an undefined case of the (c) rule AV6 fixed. No result criterion changes. |
| 3 | O1: name the rider's γ overlays as the preferred veto sample | Ph C-4 | C | C (i) | wording |
| 4 | short O2 form could be misread | Ph C-5 | C | C (i), S3 | label |
| 5 | §0 l.92–93 qualifier on "steeper fall"; duplicated "if the day-15 pause does not fire" | Ph C-6 | C | C (i): S5 and Cr C1 | |
| 6 | duplicate parenthesis l.1659–1660 | Cr C1 | C | C (i) | |
| 7 | two parentheses side by side l.66–67 | Cr C2 | C | C (i), S3 | |
| 8 | §0 l.59–61 unlabelled; "1–2 counts" copies | Cr C3 | C | C (i), S2; copies replaced by S5/S6/S11 | |
| 9 | §4.17 row 4 role column | Cr C4 | C | C (i) | |
| 10 | own-hit bracket at 0.379 only | Cr C5 | C | C (iii) | §5 |
| 11 | COM doubled "and" | Cr C6 | C | C (i) | |
| 12 | [L13] "≈ 10⁴" unlabelled | Cr C7 | C | C (i) | |
| 13 | fix report says §12.5 not edited | Cr C8 | C | C (iii) | not the artifact |
| 14 | rider expected to fire | Co C1 | C | C (i), S18 | |
| 15 | Df-9 sets the day-7/15 basis | Co C2 | C | C (i), S19 | |
| 16 | "publishable but less strong" misattributed | Co C3 | C | C (ii) | already removed from the package |
| 17 | rule-1 inputs list S_CKF | Co C4 | C | C (i), S12 | |

**Dismissals: none.** Cost check (§6.5.1): V1 is ≈ 1 agent-hour of text plus one script block that I have already
prototyped (≈ 1 min run).

---

## 4. Work list for the fixer (v8). Exact text; nothing else is touched

General rules:
- Numbers in brackets [ ] below are my scratch values; the fixer copies the **printed** v8 values where they differ.
- "Insert" keeps the surrounding text.
- The new version is `STRATEGY_<fixer>_<date>.md` ("v8"); v7 stays unchanged.

**S. Script, [9b] (0 CPU-h).**
- Insert after script l.852 (the second `v7 (U1)` print) the block below, verbatim. It uses only names defined above
  l.852.
- Change the f-string text at l.911 from `(day-15 class limit m_H = 125)` to
  `(day-15 class limit: m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)`.
- No other line changes. Save `outputs/budget_stdout_v8.txt`. It must equal stdout v7 plus the new lines, with the one
  changed l.373.

```python
# v8 (V1, verdict cycle 7 §4 item S): day-15 reading under §11.7 rule 1: every no-pile-up term at max(zero-count floor,
# N_t x H) on all own hits, no S_CKF, no conditional, no credit that exists only after the freeze; pilot exposures for
# the terms the pilot measures (Z(nunu) 2.3e6 events, DIF and each NI radius 1e6 events); every other term at its
# Table 4.4a floor. Rows marked (c) are the Q2 (c) test only: conditional and S_CKF estimated on development samples (EST).
PIL_N = {"Z(nunu)+j": PILOT_HS, "DIF": 1e6, "NI 22 mm": 1e6, "NI 30 mm": 1e6, "NI 61.5 mm": 1e6}
K_PIL = {r[0]: max(r[4], r[1] / PIL_N[r[0]]) for r in rows if r[0] in PIL_N}
kap_d15 = [(K_PIL.get(r[0], r[4]), 0) for r in rows] + [MJK]
def _b50(gam):
    return pmf_pred(gam, (PU9,))[1][1]
def _cls(b):
    return "below" if b <= 300 else "above"
print("  v8 (V1): day-15 reading under §11.7 rule 1 (own hits before CKF, no S_CKF, no conditional, no post-freeze credit; class limit B50 <= 300)")
print("  | branch | basis | B50 at day 15 | vs 300 |")
pz = pmf_pred(kap_d15, (PU9,))[1]
print(f"  | every pilot ceiling zero (DIF, NI, Z(nunu) at their pilot exposures; others at their floors) | rule 1 | {pz[1]:.0f} [16-84 %: {pz[0]:.0f}-{pz[2]:.0f}] | {_cls(pz[1])} |")
kd15_noz = [(K_PIL.get(r[0], r[4]), 0) for r in rows if r[0] != "Z(nunu)+j"] + [MJK]
kzp = K_PIL["Z(nunu)+j"]
zr = [(mp, _b50(kd15_noz + [(kzp, mp)])) for mp in (5, 10, 15, 20, 25, 50)]
print("  | Z(nunu) at its pilot ceiling count m (others as row 1), m = " + " / ".join(str(m) for m, _ in zr) + " | rule 1 | "
      + " / ".join(f"{b:.0f}" for _, b in zr) + " | " + " / ".join(_cls(b) for _, b in zr) + " |")
for mh in (10, 30, 50, 60, 70, 100):
    gam_g = [(K_PIL.get(r[0], r[4]), 0) for r in rows if r[0] not in SMSET] + [(r[4], mh * r[2] / MZ) for r in rows if r[0] in SMSET] + [(MJ_PLAN / MJ_LOOSE, mh * MJ_LOOSE / MZ)]
    b_ = _b50(gam_g)
    print(f"  | (gamma) every SM ceiling at H per event as Z(nunu), m_H = {mh} pool counts (= {mh * PILOT_HS / MZ:.0f} pilot counts); DIF, NI empty at their pilot exposures | rule 1 | {b_:.0f} | {_cls(b_)} |")
print("  | (beta) | not a day-15 branch: its Z(nunu) credit (B4-c) exists only after the freeze; at day 15 it is the (gamma) row with the same m_H | — | — |")
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    d_, g_ = ALPHA[(tag, False)]
    own = [sum(k * (m + 0.67) for k, m in kap_nodif) + pu9 + (d_ + g_) / (1 - e_) for e_ in (0.8, 0.98)]
    print(f"  | {tag}, no credit | after CKF (Table 4.4c) / own hits at eps_pair 0.8 / 0.98 | {pmf_cache[(tag, False)][1]:.0f} / ≈ {own[0]:.3g} / ≈ {own[1]:.3g} | above |")
print(f"  | (alpha1'), no credit (expected branch) | own hits at eps_pair 0.8 / 0.98 | ≈ {U1_II[0.8][0]:.3g}-{U1_II[0.8][1]:.3g} / {U1_II[0.98][0]:.3g}-{U1_II[0.98][1]:.3g} | above |")
for tag in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)"):
    print(f"  | (c) only: {tag} with fit-probability credit on DIF and conversions (needs (c) to target DIF) | (c), EST | {pmf_cache[(tag, True)][1]:.0f} | below |")
def _need(dfac, tag, fr=1.0):
    d_ = ALPHA[(tag, False)][0] * dfac
    base = kap_nodif + ([(K_DIF, d_ / K_DIF)] if d_ > 0 else [])
    if _b50(base) > 300:
        return None
    lo, hi = 1.0, 1e4
    for _ in range(16):
        mid = math.sqrt(lo * hi)
        if _b50(base + [(kz, G_A1P * fr / mid / kz)]) > 300:
            lo = mid
        else:
            hi = mid
    return hi
print("  | (c) only (EST): conversion rejection needed for B50 <= 300, by the decays-in-flight size (factor f_D on v1's central size; (alpha1) DIF at fall x339 / x201) |")
for fd_, fl_ in ((0.0, "0 (removed)"), (0.25, "1/4"), (math.exp(-1), "e^-1"), (0.5, "1/2"), (1.0, "1 (v1's central size)")):
    cells = []
    for fr_, rl_ in ((1.0, "0.379"), (F_GAM["N_trig-weighted rate 0.255"], "0.255")):
        nn = [_need(fd_, t_, fr_) for t_ in ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)")]
        cells.append(f"photon rate {rl_}: " + " / ".join("none suffices" if x is None else f"x{x:.0f} ({1 - 1 / x:.1%})" for x in nn))
    print(f"  |   f_D = {fl_} | " + "; ".join(cells) + " |")
print("  |   (alpha1) conversion levels for comparison: x52.1 / x31.0 (98.1 % / 96.8 %); without an S_CKF estimate every factor is x1/(1 - eps_pair) larger (x5-50, assumed) |")
```

Expected output, from my prototype (VERIFIED, same seeds):
- every pilot ceiling zero: 75 [38–148], below;
- Z(νν) pilot m = 5 … 50: 130 / 187 / 242 / 300 / 352 / 626;
- (γ) m_H = 10 … 100: 104 / 180 / 255 / 294 / 331 / 448;
- (α1) no credit: 587 / ≈ 2.85e+03 / ≈ 2.84e+04 (×339) and 975 / ≈ 4.79e+03 / ≈ 4.78e+04 (×201);
- (α1′): ≈ 4.96e+04–5.09e+04 / 4.96e+05–5.09e+05;
- (c) credit: 51 / 74;
- rejection grid:
  - f_D = 0: ×34 / ×34 [×23 / ×23];
  - f_D = 1/4: ×52 / ×81 [×35 / ×55];
  - f_D = e⁻¹: ×69 / ×235 [×47 / ×159];
  - f_D = 1/2: ×110 / none [×74 / none];
  - f_D = 1: none / none.

Below, "the v8 table" means these printed lines.

**S2. §0 item 3** (l.60–61): after "and the background is ≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c)" insert
"(after CKF, as v1 counted them)".

**S3. Short after-CKF label (Ph C-5, Cr C2).**
- §0 l.66–67: "per event) (after CKF, as v1 counted them; a lower value where S_CKF is not tested, annex route 6)" →
  "per event; after CKF, as v1 counted them, a lower value: a term whose S_CKF is not tested stays on all own hits,
  ×1/(1 − ε_pair) higher, annex route 6)".
- In the leading sentence l.106–107, and in §12.5 point 3 l.2937–2938: "a lower value where S_CKF is not tested" → "a
  lower value: a term whose S_CKF is not tested stays on all own hits, ×1/(1 − ε_pair) higher".

**S4. §0 upper branches** (l.78): after "(β), conditional on the promotion model being submitted" insert "(a result
after the freeze: its Z(νν) credit comes from the B4-c test, so the day-15 rule reads the same ceilings as (γ), v8
table of script [9b])".

**S5. §0 "The pause." paragraph.** Replace this span:
- from: "The day-15 rule pauses the study and asks the user if the projected B₅₀ exceeds 300 events or both pile-up
  estimators miss their cap; it is computed preliminarily at day 7."
- through: "the empty-ceiling case."

with:

> The day-15 rule (§11.7 rule 1) pauses the study and asks the user if the projected B₅₀ exceeds 300 events or both
> pile-up estimators miss their cap; it is computed preliminarily at day 7. It reads every no-pile-up term at
> max(zero-count floor, N_t·H) on all own hits before CKF, from the pilot's counts, with no S_CKF, no conditional (no
> veto, no fit-probability credit) and no credit that exists only after the freeze; its DIF and conversion terms are
> therefore expected ×5–50 above the after-CKF figures of this summary (ε_pair assumed 0.8–0.98, not measured, and not
> bounded above). The expected reading is B₅₀ ≈ [5.0×10⁴–5.1×10⁵] by v1's conversion counts ((α1′)) and ≈ [2.8×10³–4.8×10⁴]
> even if decays in flight and conversions fell like the pile-up background ((α1)): the pause is the expected branch.
> The reading is below 300 only if the pilot's ceilings are nearly empty: B₅₀ ≈ [75] with every pilot ceiling at zero;
> Z(νν) alone may count up to ≈ [20] pilot ceiling events, or every SM ceiling up to ≈ [60] pool-equivalent counts (≈ [13]
> in the pilot) if they scale with Z(νν) ((γ); (β) is read as (γ) at day 15) (script [9b], v8 table). A conversion veto
> or a fit-probability credit enters only the test of a Q2 (c) redesign (Q2).

Then delete the sentence "The day-7 and day-15 projections read own hits before CKF (Df-9) and are expected ×5–50 above
the after-CKF figures of this summary." at l.101–102; S5 contains it. The sentences from "If the pause fires and the
user chooses Q2 (b)" to "Which of the two is the default deliverable is Q2." stay as they are.

**S6. §0 leading sentence** (l.110–112): "The day-15 rule is expected to pause the study before production, and at
v1's central decays-in-flight size (1–2 counts) removing the conversions alone would not avoid the pause." → "The
day-15 rule is expected to pause the study before production (projected B₅₀ ≈ [5×10⁴–5×10⁵] on its own-hit basis
against a limit of 300); a conversion veto can count only in a Q2 (c) redesign, and at v1's central decays-in-flight
size (1–2 counts) no conversion rejection suffices without a reduction of the decays in flight."

**S7. §4.4 point 4** (l.790): "far above the day-15 class (m_H ≈ 125)" → "far above the day-15 class (m_H ≈ 125 pool
counts for Z(νν) alone; ≈ [20] counts in the pilot, script [9b] v8 table)".

**S8. §4.4 point 5** (l.871): after "(a pilot zero is a bound of 12 events for Z(νν))" insert "; with the other pilot
ceilings empty, the day-15 class corresponds to ≈ [20] Z(νν) pilot counts (script [9b], v8 table)".

**S9. §4.4 "Scenarios (β) and (γ)"** (l.999): append "(β) is a result after the freeze: at day 15 its Z(νν) credit
does not exist yet, and the rule reads the same ceilings as (γ) (§11.7 rule 1; script [9b], v8 table)."

**S10. Table 4.4c caption**, after "m_H = 100, 454 GeV.", insert: "These rows are the projection of the result (after
the freeze, with the credits stated per row; the (α) rows after CKF, as v1 counted them). The reading of the day-15
rule, which admits none of these credits, is the v8 table of script [9b], quoted in Q2."

**S11. §4.4 "What is not known"** (l.1016–1019): from "**The day-15 pause" to "decays in flight 385–647 events)." →
"**The day-15 pause (B₅₀ > 300 events; m_H ≈ 125 pool counts for Z(νν) alone, ≈ [20] in the pilot; reach ≈ 560 GeV)
is the expected branch** by v1's conversion counts; the reading of each branch under §11.7 rule 1 is the v8 table of
script [9b], quoted in Q2."

**S12. §11.7 inputs** (l.2716): "S_CKF on the development overlays" → "S_CKF on the development overlays (used only in
the test of a Q2 (c) redesign)".

**S13. §11.7 rule 1** (l.2734): after "and labelled EST." insert "A development survival or conditional fraction enters
that test at its 68 % upper value (Gamma(m + 1) on its m survivors, as H does for the pilot), never at a central zero:
a sample with no survivor among n attributed candidates demonstrates a rejection of at most ×n/1.14."

**S14. §11.7 rule 1** (l.2735–2737): "(the bounded class of Q2: m_H ≈ 125 for Z(νν), reach about 560 GeV or more by the
computation of Table 4.4c)" → "(the bounded class of Q2: reach about 560 GeV or more by the computation of Table 4.4c;
on the pilot, ≈ [20] Z(νν) ceiling counts with the other pilot ceilings empty; the reading of each branch is the v8 table
of script [9b])".

**S15. Q2 stem.** After "…assumed, not measured; script [9b], v7 line)." (l.2789) insert:

> What the day-15 rule reads, by branch (planning EST; script [9b], v8 table; B₅₀ against the limit 300):
>
> | branch | day-15 B₅₀ (rule 1) | vs 300 |
> |---|---|---|
> | (α1′), v1's conversion counts (expected) | ≈ [5.0–5.1×10⁴] (ε_pair 0.8) to [5.0–5.1×10⁵] (0.98) | above |
> | (α1), decays in flight and conversions falling like pile-up, no credit | [587–975] after CKF; ≈ [2.8×10³–4.8×10⁴] on own hits | above |
> | (β) / (γ): SM ceilings at H as for Z(νν), 10 / 30 / 50 / 60 / 70 / 100 pool counts ((β)'s Z(νν) credit exists only after the freeze) | [104 / 180 / 255 / 294 / 331 / 448] | below up to ≈ [60] pool counts (≈ [13] in the pilot) |
> | Z(νν) alone at its ceiling, the other pilot ceilings empty | [300] at ≈ [20] pilot counts | below under ≈ [20] |
> | every pilot ceiling empty | [75] (16–84 %: [38–148]) | below |
> | only in the test of a (c) redesign (EST): (α1) with fit-probability credit on decays in flight and conversions | [51–74] | below |

**S16. Q2 stem**, replace "This branch also pauses at day 15 (B₅₀ 587–975, of which decays in flight 385–647), so at
v1's central decays-in-flight size (1–2 counts) a conversion veto alone does not avoid the pause. Only branches with
B₅₀ ≤ 300 do: (α1) with fit-probability credit, which the day-15 projection admits only under (c); (β), Z(νν) tested and
the other ceilings at 10–100 simulated counts, conditional on the promotion model being submitted, ≈ 705–640 GeV; and
every ceiling empty, ≈ 710 GeV (median 790), an upper edge." with:

> This branch also pauses (table). Further upside, after the freeze and statistics-only: (β), Z(νν) tested and the
> other ceilings at 10–100 simulated counts, conditional on the promotion model being submitted, ≈ 705–640 GeV; every
> ceiling empty, ≈ 710 GeV (median 790), an upper edge. Their day-15 readings are the (γ) and empty-ceiling rows of
> the table.

"Existing bounds lie below …" stays.

**S17. Q2 (c)**, replace from "That needs the conversions reduced by ×31–52" to "(×5–50, not measured)." with:

> At v1's central decays-in-flight size (385–647 events, resting on 1–2 counts) no conversion rejection suffices:
> with the conversions removed, B₅₀ is 401–663. The conversion rejection needed (script [9b], v8 table; photon rate
> 0.379, with 0.255 in brackets) is at least ×[34] ([97.0] %) [×[23]] even if the decays in flight vanished, ×[52–81]
> ([98.1–98.8] %) [×[35–55]] at a quarter of v1's size, and ×[69–235] ([98.6–99.6] %) [×[47–159]] at ×e⁻¹. A development
> sample with no surviving conversion among n attributed ones demonstrates at most ×n/1.14 (§11.7 rule 1). If S_CKF
> cannot be estimated before the freeze, every factor must be ×1/(1 − ε_pair) larger (×5–50, not measured).

Then "As worded, (c) targets the conversions; if you choose it, say whether it may also target the decays in flight." →
"As worded, (c) targets the conversions; if you choose it, say whether it may also target the decays in flight. At
v1's central size (c) cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 51–74) acts on both."

**S18. Rider (1)** (l.2822): after "at least 3,000 events (10× the class)" insert "(expected to trigger: the day-7
reading is expected at ≈ [5×10⁴–5×10⁵])".

**S19. Df-9 row** (l.2877), default column: after "censored at 1 (§4.4 point 4)" insert "; it also sets the basis of
the day-7 and day-15 projections (own hits, no S_CKF, §11.7 rule 1)".

**S20.** The script l.911 print change (item S); §4.4 l.790 is covered by S7.

**C (i) items, applied in the same pass:**
- **Cr C1 / Ph C-6** (l.1660): "(if the day-15 pause does not fire; by v1's conversion counts the expected branch is a
  measured background, §0, Q2)" → "(by v1's conversion counts the expected branch is a measured background, §0, Q2)".
- **Ph C-4** (l.824): "C′_PU has no Geant4 and serves C1 and, for the conversions, the development estimate of a Q2 (c)
  redesign, §11.7 rule 1" → "C′_PU has no Geant4 and serves C1 and, for the conversions, the development estimate of a
  Q2 (c) redesign (if the rider is taken, its 1,000 γ overlays on the v2 chain are the preferred sample), §11.7 rule 1".
- **Cr C4** (l.2087, role column): "C1; development (attribution rules compared; completeness classes)" → "C1;
  development (attribution rules compared; completeness classes; for the conversions, the Q2 (c) development estimate,
  §11.7 rule 1)".
- **Cr C7** ([L13] l.2288): "a counted background of ≈ 10⁴ events" → "a counted background of ≈ 10⁴ events (after CKF,
  as v1 counted them)".
- **Cr C6** (COM l.6–7): "`STRATEGY_fiona_2026-11-13_23-05.md` (version 4) and `STRATEGY_gunnar_2026-11-14_00-50.md`
  (version 5) and" → "`STRATEGY_fiona_2026-11-13_23-05.md` (version 4), `STRATEGY_gunnar_2026-11-14_00-50.md`
  (version 5) and". Also update the COM pointer to v8 and add the version-8 table with one row: "TG-1 (Q2) | day-15
  reading by branch stated from the script table (V1); (c) rejection bar corrected; the (c) test's treatment of a
  zero-survivor development fraction stated; no status changed".
- **Ph C-1, Ph C-2, Ph C-5, Cr C2, Cr C3, Co C1, Co C2, Co C4** are inside S2–S19.

**Bookkeeping.**
- Header and status of v8.
- §13.7 "Changes since version 7": one row for V1 (S, S2–S19) and one row for the C items. It must state: "No default,
  criterion, CPU-h, calendar figure or expected-outcome number changed; the day-15 reading per branch and the (c) bar are
  now quoted from script [9b] v8 lines."
- Nothing else is touched. In particular: Table 4.4c rows, §11.2, Q1, Q3, Q4, Q5 and the annex.

---

## 5. The C items (18): disposition

**(i) Apply before commit** (wording, labels, and one closing sentence of an existing rule), 14 items:
- Ph C-1, C-2, C-4, C-5, C-6;
- Cr C1, C2, C3, C4, C6, C7;
- Co C1, C2, C4.

The exact text is in §4. Ph C-2 is a rule sentence. It is (i) because it closes an undefined case of the (c) test that
AV6 fixed, it is conservative, and it touches no criterion of the result.

**(ii) Gate-A package only**, 1 item: **Co C3** ("publishable but less strong" is the plan's rating of "Closure fails",
PLAN l.508–509). It has already been removed from the package.

**(iii) Deferred**, 2 items:
- **Cr C5** (own-hit bracket at 0.379 only). It is safe: the rate is labelled; at 0.255 the reading is ≈ 3.4×10⁴ [E: 6.8×10³ ×
  5], still ≫ 300, so no choice depends on it. Cost if done now: < 0.1 h. Left out to keep cycle 8 narrow.
- **Cr C8** (fix-report wording). Not the artifact. Recorded here: hunk 27 edited §12.5 point 3 (O2).

**Promoted to B:** Ph C-3 (V1-d).

---

## 6. U1, O1, O2, the "1–2 counts" caveat: final status

- **U1: RESOLVED as to the basis and its statement; residual carried as V1.**
  - The basis (own hits, no S_CKF, no conditional, ×5–50 assumed) is stated correctly in rule 1, §0, Q2, the §4.4 labels
    and route 6 (Ph §2, Cr §1, Co §1; my sweep #8, #15–20, #37).
  - What U1's text left wrong is its consequence for which branches pass and for the (c) bar. That is V1.
- **O1: accepted**, with Ph C-4 applied (S/C list).
- **O2: accepted.** The label is correct (Cr §3) and the long form is ordered (S3).
- **"1–2 counts" caveat: accepted in substance.** Its live copies are replaced by S5, S6, S11 and S17, which state the
  same fact through the rejection grid.

---

## 7. The Gate-A package (Co §3): corrections

I checked the package against v7 and stdout v7. The numbers outside the V1 family match (cluster costs, 753 / 2,322 /
1,378, FEAS_B, incidents, budget table, DP savings, decision points). The corrections:

1. **Sources:** STRATEGY v8, `budget_stdout_v8.txt`.
2. **§1 headline**, last sentence: "At v1's central decays-in-flight size (1–2 counts), the background without
   conversions is 401–663 events, of which decays in flight 385–647, so removing conversions alone would not avoid
   the pause." → "The rule reads own hits before CKF and is expected at B₅₀ ≈ 5×10⁴–5×10⁵ (table in §3). A
   conversion veto counts only in a Q2 (c) redesign, and at v1's central decays-in-flight size (1–2 counts) no
   conversion rejection suffices: without conversions B₅₀ is 401–663."
3. **Upside paragraph:**
   - "(310–370 at width 0.17; still pauses, B₅₀ 587–975)" → "(310–370 at width 0.17; still pauses: B₅₀ 587–975 after
     CKF, ≈ 2.8×10³–4.8×10⁴ as the rule reads it)".
   - After "conditional on the promotion model being submitted" insert "(after the freeze; at day 15 these ceilings read
     as (γ), below 300 only under ≈ 60 pool counts)".
4. **Paths to a stronger paper:** "under (c), a conditional removing ×31–52 of the conversions plus a reduction of the
   decays in flight" → "under (c), a conversion rejection of at least ×34 (×69–235 if the decays in flight are e times
   below v1's central size; none suffices at that size) together with a reduction of the decays in flight".
5. **§2 Review line:** "seven cycles; Category A 11 → 4 → 1 → 0 → 0 → 0, B 24 → 14 → 15 → 5 → 3 → 1 (cycles 1–6);
   [cycle 7: …]" → "eight cycles; Category A 11 → 4 → 1 → 0 → 0 → 0 → 0 → [c8], B 24 → 14 → 15 → 5 → 3 → 1 → 4 →
   [c8]". Append to the cycles sentence: "; 7 corrected which branches pass the day-15 rule and the (c) rejection bar".
6. **Q2 stem:** after "Crossing 300 is therefore expected." insert the S15 table in short form: (α1′) 5×10⁴–5×10⁵
   above; (α1) 587–975 after CKF / 2.8×10³–4.8×10⁴ own hits, above; (β)/(γ) 104–448 at 10–100 pool counts, below up to
   ≈ 60; Z(νν) alone below ≈ 20 pilot counts; all pilot ceilings empty 75, below; (c) only: (α1) with credit 51–74.
7. **Q2 (c):** replace "conversions ×31–52 lower **and** decays in flight reduced (their size rests on 1–2 v1 counts; at
   ×e⁻¹ conversions alone suffice, B₅₀ 159–256). Without an S_CKF estimate every reduction must be ×5–50 larger." with
   "at v1's central decays-in-flight size (1–2 counts) no conversion rejection suffices, so (c) must also reduce the
   decays in flight. The rejection needed is at least ×34 (97.0 %) even if they vanished, and ×69–235 (98.6–99.6 %)
   at ×e⁻¹ (photon rate 0.379). A sample with no surviving conversion among n demonstrates at most ×n/1.14. Without
   an S_CKF estimate every factor is ×5–50 larger."
   Then "Say whether (c) may also target decays in flight." → "Say whether (c) may also target the decays in flight;
   at v1's central size it cannot work otherwise."
8. **§7 risk 1:** "unless a demonstrated ≈ 97 % conversion rejection is combined with a reduction of decays in flight"
   → "unless a demonstrated conversion rejection of 98.1–99.6 % (97.0 % only if the decays in flight vanished) is
   combined with a reduction of the decays in flight".
9. **§8 Files:** "the six arbiter verdicts" → "the eight arbiter verdicts" (after cycle 8).
10. **Notes for the orchestrator:** the "[cycle 7: …]" placeholder becomes "[c8]". All V1 numbers are to be re-checked
    against stdout v8 lines, not v7.
11. **Length:** the package is 1,499 words. The corrections add ≈ 120. That is acceptable for the 3-page limit if the
    Q2 table is a 6-row table. Otherwise cut the §2 incident sentence to one line.

Items 2–8 must quote v8's printed numbers. Where the fixer's printed values differ from my brackets, the printed values
win.

---

## 8. Regression, motivated-reasoning and competing-group checks

**Regression triggers (§6.7).** Phase 1 has no results.
- *> 80 % single systematic:* latent in the expected branch, and committed to investigation (v7 l.2159); not a defect
  now.
- *Tautological comparison:* none. The (c) test on development estimates is pre-freeze only, and rule 1 keeps it out of
  the result.
- *Validation failure, GoF, bin exclusion:* not applicable.

No trigger is met.

**Motivated reasoning.** For the fourth cycle running, the gentler reading reached the human through the arbiter's own
prescribed text. Here it took three forms: a credited branch listed as passing, a 100 %-removal number standing for a
finite veto, and a scenario level standing for a bar. Each time the default ((a), pause) and the expected outcome
survive. What changes is how attractive the live alternative (c) looks: it is harder than v7 says (≥ ×34 in every case,
×52–235 at plausible decays-in-flight sizes, and impossible at v1's central size without a DIF reduction).

I checked myself against the opposite bias:
- I did not make (c) look harder than the script says. The 0.255 rate gives lower factors, and I print them.
- The f_D = e⁻¹ row is kept.
- The (γ) crossing is reported on both bases (≈ 60 and ≈ 74).

**Competing group.** A competing group would ask exactly what the v8 table answers: what pilot count passes the rule,
and what veto rejection a development sample can demonstrate. S13's ×n/1.14 makes the second question answerable.

---

## 9. Judgment for the audit trail and the orchestrator (Gate A)

The remaining defects are confined to the **description of the day-15 decision** in the human-facing text: which
branches pass the rule, and the (c) bar. I found nothing that suggests the design is unsettled.
- **Rule 1 itself** is unchanged and correct as a rule. V1 adds no criterion except S13, which closes a zero-count case
  conservatively.
- **Criteria, samples, budget and calendar** (4,609 / 5,992 / 60 days) are untouched; stdout v7 is byte-identical to
  the reviewers' runs.
- **The expected outcome** is unchanged: ≈ 10⁴ events after CKF, reach at or near the existing bounds, an expected pause.
- **The default** (Q2 (a)) is unchanged.

Two observations for the human, neither of them a defect:
1. On the rule's own pilot exposures, an all-empty pilot already reads B₅₀ ≈ 75 (16–84 %: 38–148). One DIF pilot count
   is ≈ 65 events, so a handful of DIF pilot counts alone approaches 300. The day-15 reading is therefore sensitive to
   pilot statistics, not only to physics. The planned DIF enrichment and the reserve (rule 3(b)) address this after
   day 15.
2. (c) is now shown to need a demonstrated 98–99.6 % rejection plus a decays-in-flight reduction. That is a fair input
   to the human's choice, and it strengthens the case for the default.

---

## 10. Iteration history

| cycle | version | merged A | merged B | verdict |
|---|---|---|---|---|
| 1 | v1 (Brigitte) | 11 | 24 | ITERATE |
| 2 | v2 (Dmitri) | 4 | 14 | ITERATE |
| 3 | v3 (Emeric) | 1 | 15 | ITERATE |
| 4 | v4 (Fiona) | 0 | 5 | ITERATE |
| 5 | v5 (Gunnar) | 0 | 3 | ITERATE |
| 6 | v6 (Ingrid) | 0 | 1 (U1) | ITERATE |
| 7 | v7 (Jules) | 0 | 4 (one family, V1) | ITERATE |

This is cycle 7 of the hard cap of 10. The B count rose from 1 to 4 because I counted the members of one family
separately, and because the sweep looked for every member, not because the artifact regressed.

---

## 11. Cycle 8: form

A fresh fixer applies §4 (S, S2–S19, the C (i) list, bookkeeping) and nothing else. It writes v8,
`budget_stdout_v8.txt`, COM v8 and `FIX_REPORT_cycle7_<name>.md`, with the hunk → item map.

A narrow 4-bot re-review follows, with fresh sessions:

| role | verifies exactly |
|---|---|
| physics | Re-run the script. Check that the v8 block implements rule 1 as stated: pilot exposures for Z(νν)/DIF/NI; no S_CKF, no conditional; (c) rows only as EST. Recompute independently at least four values: the empty-pilot row, the Z(νν) pilot crossing, the (γ) crossing, and the f_D = 0 and e⁻¹ rejection cells. Check each of the 40 sweep statements (§2) in v8 against the printed table. |
| critical | `diff` v7 → v8 (strategy, COM, script): every hunk maps to an item of §4. stdout v8 = stdout v7 + the v8 block lines, with exactly one changed line (old l.373). Greps on live text (excluding §13 history): "avoid" only in S5/S6/S17 forms; "×31–52" only as the (α1) comparison level; "suffice" only as "no … suffices"/"none suffices"; "m_H ≈ 125" only with "pool"/"Z(νν) alone"; every number of S5/S6/S15/S17/S18 equals a printed v8 line. |
| constructive | Q2 and §0 read as the human: is it plain what the rule reads, that the pause is expected, what (c) must achieve, and that the default is unchanged? Apply §7 to the package and give the final text. |
| arbiter | PASS if the three reviews confirm §4 is applied and correct and the diff is clean. |

New findings are admissible only as one of these: a regression of this fix; a factual error in a number shown to the
user; or a genuine A. Everything else is C, for the package. **Settled (not to be reopened):** rule 1 as written; the
(c) test on development estimates (with S13); the default answers Q1–Q5.

---

## 12. Verdict

**ITERATE.**
- **Category A:** none.
- **Category B (fix before PASS):** V1-a (β), V1-b (×e⁻¹ "suffice"), V1-c (×31 bar), V1-d (fit-probability credit on
  DIF). Fixed by §4 items S and S2–S19. Priority: S (script table) → S17 (Q2 (c)) → S15/S16 (Q2 stem) → S5/S6 (§0) →
  S13/S14 (rule 1) → S7–S11 (§4.4 labels) → S12, S18, S19, S2–S4.
- **In the same pass:** the 14 C (i) items (§5), with no re-review beyond the cycle-8 checks.
- **Gate-A package:** Co §3 with the 11 corrections of §7.
- **After a cycle-8 PASS,** the artifact of record for Gate A is STRATEGY v8 with `COMMITMENTS.md` and
  `budget_stdout_v8.txt`. The figures to approve stay 4,609 CPU-h / 5,992 / 60 days (rider 4,616 / 6,001 optional).
