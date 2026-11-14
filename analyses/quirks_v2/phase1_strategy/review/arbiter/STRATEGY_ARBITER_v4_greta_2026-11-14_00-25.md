# Arbiter verdict: Phase 1 STRATEGY v4 (quirks v2), review cycle 4

Arbiter: Greta, 2026-11-14 00:25. Fresh to this panel; I arbitrated no earlier cycle. I followed the Prompt Template of
`agents/arbiter.md` in full: adjudication cases 1–5, the structured table, the dismissal rules (§6.5.1), the
regression check (§6.7), the motivated-reasoning check and reviewer-pressure protection.

**Artifact.** `phase1_strategy/outputs/STRATEGY_fiona_2026-11-13_23-05.md` ("v4", 2,842 lines), `COMMITMENTS.md`
("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/FIX_REPORT_cycle3_fiona.md` ("FR").
**Cycle-3 verdict:** Felix, P1–P16 (`STRATEGY_ARBITER_v3_felix_2026-11-13_22-40.md`).

**Cycle-4 reviews** (all 2026-11-13 23:50):

| reviewer | role | A | B | C | ids used below |
|---|---|---|---|---|---|
| Florence | physics | 0 | 1 | 7 | Ph-B1, Ph-C1…C7 |
| Gerald | critical | 0 | 4 open (2 P residuals + 2 new) | 15 | G-B1…G-B4, G-C1…C15 |
| Gertrude | constructive | 0 | 2 | 11 | N-B1, N-B2, N-C1…C11 |

There is no plot validator: Phase 1 has no figures.

**What I read.** In full: `agents/arbiter.md`, `AGENT_RULES.md`, the study and phase `CLAUDE.md`, `FRAMING.md`, the
cycle-3 verdict, the three cycle-4 reviews. Of v4: §0 l.40–95; §4.4 l.700–940; §4.6 l.1143–1182; §4.7 l.1265–1302;
§11.3 l.2479–2518; §11.7 l.2614–2661; §12.1 with its annex l.2666–2748. Script [9b] l.543–762 and its full output.
PLAN (`publication_plan/publication_plan.tex`) l.105–127 (reach table) and l.494–521 (outcome table). `06-review.md`
§6.5 (by grep). v1 record: `TT/data/acts_stage4/analysis/C12FC_v1/background.json` (`cprime.dif`, `cprime.gamma`,
`sm.<p>.proxy_of`).

**My own arithmetic.** Standard-library `python3 -I`, niced, on einstein; the script was run through `runpy` so that
every number below uses the script's own `pmf_pred`, `s95_pmf`, `s95_fixed` and reach mapping. Code and output are
in the session log `logs/arbiter_greta_2026-11-14_00-25.md` (scratchpad files `greta_check.py`, `greta_check2.py`).

**Rules followed.** No sub-agents, no git, nothing heavy. I wrote only this verdict and the session log.

**Verdict: ITERATE. 0 Category A, 5 Category B (R1–R5).** All five are text, table or script-row fixes; one (R5) adds
≈ 36 CPU-h. Not ESCALATE: nothing needs the user beyond the Gate-A questions, but R1 changes what Q2 asks (§7).

---

## 1. Overall assessment

v4 executes the cycle-3 work list well. All three reviewers reproduced, independently, the floor (13.0; 12.2–17.8),
the approved figure (4,574 CPU-h) and threshold (5,946 = 1.3×), the calendar (57.6 days), every family-wise rate
(ceiling 4.9 %, combined 6.9–8.9 %, T1 coverage 4.7–4.9 %, fluctuation route 0.30) and the T1 thresholds (462 / 459
of 500). The stale-value greps are clean. P1, the only Category A of cycle 3, is resolved. The three pass-by-construction
validations of cycle 3 (P3, P4, P7) are gone.

What remains is, once more, mostly about **what the user is shown**, and this time it is not a matter of labelling.
The physics reviewer's point is correct (verified in §2): the lower branch of the headline assumes that hard-scatter
conversions fall with width like the random pile-up background, which v1's own counts reject at p ≈ 10⁻³. With the
fall v1 measured, the background of the default plan at R08–R09 is of order 10⁴ events, the reach is well below
400 GeV, and the day-15 pause is the *expected* branch, not a "realistic" one. That turns Gate-A question Q2 into the
central decision of the study (§7). The other four B items are regressions or gaps created by the cycle-3 fixes (an
untestable S_CKF, a borrowed completeness credit, a pilot scheduled before its code, and three missing Q3 routes).

**Trend.** Merged Category A by cycle: 11 → 4 → 1 → 0. Merged B: 35-item cycle → 18 → 15 → 5. The design is stable;
no finding calls for a redesign.

---

## 2. Facts settled from sources (my own checks)

| question | evidence (opened or computed by me) | ruling |
|---|---|---|
| v1's attributed counts with pile-up (Ph-B1 premise) | `background.json` → `cprime.gamma.rows`: R04 153/500, R05 86/500, R06 13/500, R07 conditional 2/13, R08 0/13, and p(R09 \| R06) = 2/13. `cprime.dif.rows`: R04 166/500, R05 81/500, conditionals 2/81 (R06), 1/81 (R07), 0/81 (R08) | **VERIFIED**, identical to Table 4.4b. |
| Do the conversions fall like pile-up? | The pile-up fall per width step is ×201 (R05→R06) and ×339 (R06→R07) (script [9b]). From 13 counts at R06 a pile-up-like fall leaves μ = 0.065 / 0.038 counts at R07; P(≥ 2) = **2.0×10⁻³ / 7.2×10⁻⁴**. From 86 at R05 it would leave μ = 0.43 / 0.25 at R06 against 13 observed, P < 10⁻¹⁴. v1 measured ×6.6 and ×6.5 on two independent steps. For DIF (2 → 1) P(≥ 1) = 0.6–1.0 %. | **Rejected for the conversions**, on two independent steps; disfavoured for DIF at about 1 %. v4 l.920 ("measured on 2→1 and 13→2 counts and therefore weak") is wrong for the conversions. Ph-B1 point 1 stands. |
| Size with the measured conversion fall (Ph-B1 point 2) | R07: conversions N_trig × 0.379 × 2/500 = 6.19×10⁴, DIF 1.30×10⁵ (script). R08 = R07/6.5 for the conversions = **9.53×10³**; DIF at the pile-up fall 385–647. Sum with floors and the R09 pile-up term ≈ **9.9×10³–1.02×10⁴** (no credit, R09 = R08). | **VERIFIED** (my run of the script's functions). |
| Reach of that branch | Fixed B: s₉₅ = 197–200 → **394 / 391 GeV** (PLAN l.121, B = 10⁴ ↔ 393). Counted-ceiling reading (Gamma(m+1) on the pool share, the convention of every other (α) row): s₉₅ median 352–361, 84 % 495–505, i.e. beyond the 10⁴ column. With PLAN's own 10⁵ column (243 GeV, l.121) added to the mapping: **median ≈ 315 (314–317), 84 % edge ≈ 270 (270–273) GeV**. With v1's fit-probability fraction 2/35 as credit (width 0.43): B₅₀ 580–600, median ≈ 330, 84 % edge ≈ 250 GeV. | Florence's "≈ 10⁴ events, reach ≈ 390–395 GeV" is **correct as the fixed-B value**; like-for-like with the other rows of Table 4.4c the branch is **≈ 270 GeV at the 84 % edge, median ≈ 315**. Credit does not rescue it, because the credit carries its width. |
| Statistics-only nature (Case 5) | PLAN l.122: at σ_ln = 0.2 the reach is 325 GeV at B = 10³ and "below 200 GeV" at B = 10⁴. | A background of 10⁴ events with any systematic width of order 0.2 (material, conversion modelling) has a reach below 200 GeV, i.e. at the existing bounds (≲ 180 GeV). Nobody stated this; it belongs in the headline of that branch. |
| Z(νν) ceiling with the measured fall | Z(νν) conversions at R08: 2.51×10⁷ × 0.2306 × (2/500)/6.5 ≈ 3.6×10³ events, i.e. ≈ 1.6×10³ counts in the 1.1×10⁷ pool events and ≈ 3×10² in the 2.3×10⁶ pilot events. Day-15 class limit m_H ≈ 125. | The pilot will see m_H far above 125 at R08 if v1's fall holds: **the day-15 pause is the expected branch.** The Df-9 planning m_H (2–18 with CKF, 10–890 under option (a), §4.4 point 4) applies the pile-up fall ×100–300 to the hard-scatter rate and inherits the same assumption. |
| (α1) size uncertainty (G-B1) | B₅₀ × e^(−1, 0, +1): median 571 / 504 / 437 (×339), 535 / 469 / 400 (×201); 84 % edge 519 / 455 / below 393, 486 / 421 / below 393. | **VERIFIED**: the factor e moves the (α1) median between ≈ 400 and ≈ 570 GeV (Gerald: 400–570). |
| m_H = 1000 row (Ph-C2, G-C10) | With the count width: B₅₀ 2,299, s₉₅ 168, median reach ≈ 415 GeV, against ≈ 490 (fixed B) in Table 4.4c. | Ph-C2 correct. |
| FR §4 item 1 "both readings are stated in §4.4" | grep "393": only the two (α2) rows. | **Not true** (N-B1, G-B1, N-C9). |
| C-13 premise (WW, WZ proxy) | `sm.WW.proxy_of` = [Wtau_l, Wtau_h]; `sm.WZ.proxy_of` = [Wtau_l, Wtau_h, Znunu_j] | The proxy is a list, so costing WW and WZ "if W(τ_h)-like" is a stated choice, not an error. G-C13 **not adopted**. |
| B4-e default size (G-B2 point 3) | v4 §4.7 l.1275–1276: a zero count among the MET-passing events is a floor of N_MJ × 1.14/100; at the planning N_MJ = 4×10⁵ that is 4.6×10³ (460–46,000 over 0.1–10 %). | **VERIFIED.** It alone would exceed the day-15 class (B₅₀ > 300). |
| S_CKF sample (G-B3) | v4 l.734–735: "attributed candidates on the unbiased B1 overlays and on the hit-level halves, derivation R04–R05, test R06"; Table 4.4b: 4 expected DIF counts at R06 in 1,000 unbiased overlays; the cycle-3 ruling said "overlays and hit-level halves, R04–R06" | **Regression confirmed**: untestable for DIF and NI by design. S_CKF is a survival-type factor conditional on the no-pile-up class, so the enriched overlays (selected on that class, known weights) test it without bias, like S and π_k. |
| Pilot vs code (N-B2) | §11.7 l.2623 "from the pilot (finished by day 5)"; §4.4 point 5 l.812–817 (f_k, H, near-pass overlays from the pilot); §11.3 l.2484 and slot table l.2501: classes on hit subsets, S_CKF, per-k promotion in **Phase 3, days 5–17**; §4.4 point 2: hand-over variant frozen in Phase 3 | **Contradiction confirmed.** |

---

## 3. P1–P16: final status after cycle 4

| # | Ph / K / N | final | reason |
|---|---|---|---|
| P1 (A) | R / R / R | **R** | Case 1. Re-split, floors, rule 6, inventory rows, Q3 annex row all present and reproduced three times. |
| P2 | P / P / P | **P → R1** | Case 1. The structure is right, but the lower branch rests on a fall that v1's record rejects, and the sentence mixes quantiles (§2). |
| P3 | R / R / R | **R**, with regression **→ R4** | The definition and monotonicity table are right; the narrowing of the S_CKF test sample is a new defect of the fix (G-B3, verified §2). The Df-9 m_H EST is amended under R1. |
| P4 | R / R / R | **R** | — |
| P5 | R / R / R | **R**, with regression **→ R5** | The paired pass is right as specified; the borrowing for eleven processes is a fixer's choice beyond the ruling (G-B4). |
| P6 | R / R / R | **R** | 4.93 %, 6.9 / 8.9 % reproduced three times. |
| P7 | R / R / R | **R** | — |
| P8 | R / R / R | **R** | — |
| P9 | R / R / R | **R** | — |
| P10 | R / P / R | **P → R2** | Case 2. I side with the critical reviewer: the P10 fix required a "default (size at H)" per route, and the B4-e size is missing (verified §2); the P15 and P3 fixes created two further routes that the annex, by §4.0 point 6's own words ("every route … with its probability"), must list. Florence and Gertrude checked the four routes named in cycle 3, which are indeed present: both readings are right on what they checked (Case 4). |
| P11 | R / R / R | **R** | — |
| P12 | R / R / R | **R** | — |
| P13 | R / R / R | **R** | The figure changes again under R5 (fixer prints it). |
| P14 | R / R / R | **R**, with a scheduling gap **→ R3** | The rules are right; the pilot cannot produce its outputs by day 5 as scheduled (N-B2, verified §2). |
| P15 | R / R / R | **R** | The "not submitted" consequence enters the annex under R2. |
| P16 | — / R / R | **R** | Case 3 for the physics reviewer (not assessed, out of remit). The validator slots (G-C12, N-C3) are C. |

**Counts:** RESOLVED 14 (P1, P3–P9, P11–P16; P3, P5 and P14 with successor findings R4, R5, R3 for defects their
fixes introduced), PARTIALLY RESOLVED 2 (P2 → R1, P10 → R2), NOT RESOLVED 0.

---

## 4. Structured adjudication table: open findings of cycle 4

Fix type: (T) text or table; (S) a number recomputed in `strategy_budget.py`; (G) a Gate-A line.

| # | finding | source | their cat | final | type | rationale |
|---|---|---|---|---|---|---|
| **R1** | **The headline (§0, Q2) and §11.7 rule 1 rest on a conversion fall that v1's counts reject; the branch the evidence supports (≈ 10⁴ events, reach ≈ 270 GeV at the 84 % edge, median ≈ 315, ≈ 390 at fixed B; the day-15 pause expected) is absent; the remaining branches are quoted at mixed quantiles.** Parts: (a) the (α1) branch as medians (470–500) beside an 84 %-edge figure, its edge 421–455 missing; (b) (α2) and the log-normal reading missing from §0/Q2, and FR's claim that they are stated is false; (c) the factor-e size uncertainty not carried into the reach; (d) (β) at one ceiling count only and without "(Z(νν) at its floor)"; (e) "no promotion credit" where the scenario means no fit-probability credit; (f) the empty-ceiling case leads although the Df-9 planning EST (m_H = 10–890) does not expect it; (g) l.920 calls the conversion fall "weak"; (h) Case 5: the reach mapping stops at 393 GeV, so the lowest rows print "below 393", which the user cannot read; and the 10⁴-event figure is statistics-only (PLAN σ_ln = 0.2: below 200 GeV) | Ph-B1 (all points), G-B1, N-B1; Ph-C1, Ph-C2, Ph-C5, G-C10, N-C7, N-C9; arbiter (h) | B, B, B; C… | **B** | S+T+G | Cases 1 and 5. Verified in §2 from the v1 record and the script's own functions. B and not A: no result is computed from it, the binding day-15 rule uses the pilot's own counts and own fall and would catch it, and Table 4.4c contains (α2). But Q2 asks the user to approve production on this headline, so the honest number must be the one put to the user. This is the top item. |
| **R2** | **The Q3 annex misses three routes/sizes**: the promotion model "not submitted" (fewer than two classes reach 24 promoted events, P15), which sends every credited B1/B4 term to H and on which (β) is conditional; the S_CKF NOT TESTED route (P3); the B4-e default size (4.6×10³ events at the planning N_MJ, by itself above the day-15 class) | G-B2 | B | **B** | T+G | Case 3, verified (§2). D4 is put to the user; the annex is its stated consequence. |
| **R3** | **The pilot is due by day 5 but needs code scheduled in Phase 3** (own-hit classifier with k per layer type on all own hits, the near-pass flag, the occupancy-model π_k); the day-7 projection's pile-up term cannot exist at day 7 | N-B2 | B | **B** | T | Case 3, verified (§2). A contradiction between two binding statements under a decision point the user is told about. |
| **R4** | **S_CKF is testable only on enriched overlays** for DIF (4 expected counts on the unbiased ones) and NI is tested at R05 by the rung split; the "unbiased only" restriction of P4 was carried over to a survival factor where it does not apply | G-B3 | B | **B** | T (0 CPU-h) | Case 3, verified (§2). A regression of the P3 fix; it puts DIF and NI at H on all own hits (×5–50) by design. |
| **R5** | **Eleven SM processes borrow another process's mixed excess**, so their completeness verdict and c_mix (which multiplies the term always) are untested credits entering the result | G-B4; Ph-C3 (size of H′) | B; C | **B** | S+T | Case 3, verified from l.767–775. A credit without a test contradicts §4.0 point 6. Ruling in §6 R5: the 36 CPU-h paired pass. |

**Case 5 (items all reviewers missed).** Folded into R1: (i) the reach mapping truncated at the 10⁴ column although
PLAN l.121 has a 10⁵ column (243 GeV); (ii) the statistics-only nature of a 10⁴-event reach (PLAN l.122); (iii) the
Df-9 planning m_H and the pilot reading (§4.4 point 4 l.739–743, point 5 l.818–819) use the pile-up fall for the
hard-scatter rate, which the conversions' measured fall contradicts. I also note, for the fixer's label only (Ph-C5),
that v1's own conditional p(R09 | R06) for conversions is 2/13 (`cprime.gamma.rows`, R09), not the pile-up 2/35.

**Dismissals: none.** Every B of every review is accepted (mapping in §10). G-C13 is not adopted on independent
evidence (§2: `proxy_of` is a list).

**Reviewer-pressure protection.** FR §4 item 1 asserted that both readings are stated in §4.4; independent grep
shows they are not. FR l.920's "therefore weak" is the executor's reason for setting (α2) aside; v1's 86 → 13 → 2
record (opened by me) contradicts it for the conversions. Ph-B1 therefore stands in full.

---

## 5. The honest headline: ruling and exact text

**Ruling.** The branch that v1's record supports leads. It is the one in which the conversions keep the fall v1
measured on two steps, and DIF keeps the pile-up fall (the more favourable of its two readings). The number that
leads is the 84 % edge, by v4's own quoting rule (§4.11 point 3), computed like every other row (counted-ceiling
reading), with the fixed-B value beside it so the user sees the range. Every other branch is quoted as "84 % edge
(median)" and labelled. The day-15 pause is called the **expected** branch. Every reach number says that it rests on
v1 placeholder efficiencies. The numbers below are my values from the script's functions; the fixer replaces each by
the value the amended script [9b] prints (they must agree to within rounding).

### 5.1 §0, replacement of point 3 (l.54–57)

> 3. *Decays in flight and hard-scatter conversions*, which v1 counted at R06–R07 with pile-up (2 and 1 DIF, 13 and 2
>    conversions per 500 events; Table 4.4b). The conversions fell by ×6.6 and ×6.5 per width step (86 → 13 → 2), not
>    like the random pile-up background (×201–339): with a pile-up-like fall from R06, v1 would have expected
>    0.04–0.06 counts at R07, and 2 or more has probability 7×10⁻⁴–2×10⁻³ [E, script [9b]]. Extrapolated with their own
>    fall, which is the rule the pilot reading uses (§4.4 point 5), they leave ≈ 9.5×10³ events at R08–R09 without
>    fit-probability credit, and the background is ≈ 1.0×10⁴ events (scenario (α1′), Table 4.4c). If they fell like
>    the pile-up background, they would add 570–960 events (projected B₅₀ 590–980; (α1)).

### 5.2 §0, replacement of the "Expected" paragraph through "(§11.7)." and the sentence "The expected paper is … not a fallback." (l.59–75)

> **Expected (EST; every reach number rests on v1 placeholder efficiencies, best Λ per mass, PLAN l.121):** by v1's
> own counts the background of the default plan at an R08–R09 selection is led by hard-scatter photon conversions,
> **≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge (median ≈ 315 GeV; ≈ 390 GeV if that background were
> known exactly, below 200 GeV if it carries a systematic width of 0.2, PLAN l.122)**, and the day-15 rule is
> expected to pause the study before production (§11.7, Q2). The upper branches, each as 84 % edge (median):
> ≈ 420–455 GeV (470–500) if decays in flight and conversions fall like the pile-up background and earn no
> fit-probability credit (α1), which v1's conversion counts disfavour at p ≈ 10⁻³; the factor-e uncertainty of this
> v1-based size moves the median between ≈ 400 and ≈ 570 GeV; ≈ 705–640 GeV (770–695) if Z(νν) is tested and credited
> (at its floor) and the terms expected at their ceilings count 10–100 events per Z(νν)-sized sample (β), conditional
> on the promotion model being submitted; ≈ 710 GeV (790) if every no-pile-up ceiling counts zero, an upper edge that
> the strategy's own planning estimate does not expect (Df-9: m_H = 10–890 for Z(νν), §4.4 point 4); 1,026 GeV for a
> negligible background. Existing bounds lie below about 180 GeV (PLAN l.115-116; the search for newer results, R-20,
> is pending) [E, script [9b]]. The abstract heads with the 84 % edge of the branch that is realised (§4.11 point 3).
> Caveats: v1 placed the pile-up DIF vertices at the PV, and v2 places them at their own z, which may lower the DIF part
> of (α); v1's attribution rule is not yet transcribed; neither caveat applies to the conversions; the SM floor rests
> on a guessed 45 ms per event (at 90 ms the summed floor is 20.8 instead of 12.6, script [9]); the v1 fast-path
> efficiencies behind the reach numbers are ×1/0.87 high, so the v2 reach is expected somewhat lower; the plan's reach
> row assumes the selection's efficiency equals the book's best-Λ efficiency, a bias of either sign. **The pause.**
> The day-15 rule pauses the study and asks the user if the projected B₅₀ exceeds 300 events or both pile-up
> estimators miss their cap; it is computed preliminarily at day 7. By v1's conversion counts this is the expected
> branch, unless the v2 pilot measures a steeper fall or a conversion-removing conditional (the displaced-vertex veto
> B3-b, the fit probability) is tested close to where it is applied. In that case the paper is the plan's "real
> background" outcome (PLAN §9: a measured background, the reach at that B, the sideband recipe as the way out). If
> the pause does not fire, the paper is the plan's "middle" outcome with the leading terms **bounded, not
> estimated**; its pre-declared label is "target not met: sample-size limited" while the ceilings count few events
> ("target met" needs σ_ln ≤ 1, f₀ ≤ 0.5 and every leading term labelled estimate, §4.11 point 3). Which of the two
> is the default deliverable is Q2.

The leading sentence (for the abstract-level summary, `STATUS.md` and the Gate-A package) is therefore:

> **Expected (EST, v1 placeholder efficiencies): by v1's own counts the default plan's background at R08–R09 is led by
> hard-scatter conversions, ≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if the
> background were known exactly), and the day-15 rule is expected to pause the study before production.**

### 5.3 Q2: the exact text is in §7.

---

## 6. Work list for the fixer (priority order; the fix must touch nothing else)

General rules (unchanged): write `STRATEGY_<fixer>_<timestamp>.md`, update COM, the script and a fix report; trace
every change to R1–R5 or to an adopted C item below; every number shown to the user must come from a printed script
line. **For every "stated in" claim in the fix report give a grep phrase (N-C9).** [S] = printed by the script.

### R1 — the honest headline [S][T][G]

1. **Script [9b].**
   - `PLAN_REACH`: append `(1e5, 243.0)` (PLAN l.121, σ_ln = 0 row). `rfmt` then prints a number down to 243 GeV and
     "< 243" below. Rows above 393 GeV do not change (the interpolation below the 10⁴ column is identical).
   - Add to `ALPHA` the tag **"alpha1' (conversions at their own fall x6.5, DIF at the pile-up fall x339 / x201)"**:
     `fd` = 0.2470/r07 and 49.72/0.2470, `fg` = 13/2.0; with and without credit, through the same `row()` calls as the
     other (α) rows. Expected output (mine): no credit B ≈ 9.9×10³–1.02×10⁴, s₉₅ median 352–361 [84 %: 495–505],
     reach median 317–314 [84 % edge 273–270]; fixed-B s₉₅ 197–200 → 394–391; with credit B₅₀ 580–600, reach 332–331
     [250]. Print also the fixed-B s₉₅ and reach of the no-credit row (the "known exactly" figure).
   - Note: the `row()` function switches to fixed B above a median sum of 5,000; for the (α1′) no-credit row call the
     predictive branch explicitly (the pmf has ≈ 10⁴ + 10√10⁴ entries, which runs in seconds), and keep fixed B only
     for (α2) (7.5×10⁴), labelled "fixed B, an upper edge of the reach".
   - Add one line printing the (α1) median and 84 % edge at B × e^(−1) and B × e^(+1) (mine: median 571–535 / 437–400,
     edge 519–486 / below 393).
   - Compute the m_H = 1000 row with `row()` like the other m_H rows (mine: B₅₀ 2,299, s₉₅ 168, median 415 GeV)
     (Ph-C2, G-C10).
   - Print the probabilities of §2: P(≥ 2 at R07 \| pile-up fall from 13 at R06) = 7.2×10⁻⁴ / 2.0×10⁻³; P(≥ 1 \| DIF
     from 2) = 0.6 / 1.0 %.
   - Extend the HEADLINE print line with (α1′) (median, 84 % edge, fixed B) and (β) at m_H = 10 / 30 / 100.
2. **Table 4.4c** (l.899–914):
   - New row after the (α1) rows: "**(α1′)** conversions at their own measured fall (×6.5 per width step, v1's
     86 → 13 → 2), DIF at the pile-up fall, **no credit** (R09 = R08): DIF 385–647 + conversions 9,530 | B₁₆ / B₅₀ /
     B₈₄ | σ_ln | s₉₅ | **317–314 [273–270]; ≈ 390 at fixed B**", and the same with v1's pile-up fit-probability
     fraction as credit.
   - (α2) rows: replace "below 393 (beyond the plan's table)" with the printed value and "fixed B, an upper edge of the
     reach" (G-C10).
   - m_H = 1000 row: the printed predictive values.
   - The two "with credit" rows: label the credit "v1's **pile-up** fit-probability fraction 2/35; for genuine
     topologies it may differ either way (v1's conversion conditional p(R09 \| R06) is 2/13)" (Ph-C5).
   - (β) row: "Z(νν) tested and credited (at its floor) …; conditional on the promotion model being submitted (§4.4
     point 4)" (Ph-C1, G-B2).
3. **Scenario text after the table** (l.916–925):
   - Replace "(α2) uses their own R06→R07 fall, measured on 2→1 and 13→2 counts and therefore weak." by: "(α2) uses
     their own R06→R07 fall. For the conversions that fall is measured on two independent steps (86 → 13 and 13 → 2,
     ×6.6 and ×6.5) and a pile-up-like fall is rejected at p ≈ 10⁻³; for DIF it rests on 2 → 1 counts (a pile-up-like
     fall has P ≈ 1 %). (α1′) therefore takes the conversions at their own fall and DIF at the pile-up fall; it is the
     branch the v1 record supports."
   - Replace "which may lower (α); … neither applies to the conversions." by "which may lower the DIF part of (α);
     v1's coded attribution rule is not yet transcribed (§4.4 point 3), which acts on the level of the counts rather
     than on their ratio between rungs counted under the same rule; neither applies to the conversions."
   - After "about a factor e (…)": "This is a planning uncertainty of the size, not a width that v2 would carry: the
     projection uses the counted-ceiling reading (Gamma(m + 1) on the pool share), which is what v2's likelihood
     carries for a counted term; the factor e is shown as the B × e^(±1) rows (median reach ≈ 400–570 GeV for (α1)).
     Read as a log-normal width instead, it would give [printed value] GeV; that reading is not used. A reach at a
     10⁴-event background is statistics-only: at σ_ln = 0.2 the plan's table gives below 200 GeV (PLAN l.122)."
4. **§4.4 point 4, Df-9 planning EST** (l.738–743), add after "These are the m_H ranges of Table 4.4c;": "they apply
   the pile-up fall per width step to the hard-scatter rate. With the conversions' own fall (×6.5) the conversion part
   alone gives m_H ≈ 1.6×10³ for Z(νν) at R08 (≈ 3×10² in the pilot), far above the day-15 class (m_H ≈ 125) [E, script
   [9b]]." Print this in the "P3/P14 EST" line of [9b].
   **§4.4 point 5, pilot reading** (l.818–819): after "2–190 under option (a) of Df-9" add "(pile-up fall; ≈ 3×10² if
   the conversions keep v1's fall)".
5. **§0**: the texts of §5.1 and §5.2 above, verbatim except for the printed values.
6. **§11.7 rule 1** (l.2639–2640): replace "By v1's own record (scenario (α1) of Table 4.4c) this is a realistic branch."
   by "By v1's own conversion counts (scenario (α1′) of Table 4.4c) this is the expected branch; what follows is Q2."
7. **Q2**: the text of §7.
8. **Wording everywhere it occurs** (grep "promotion credit" in §0, Q2): "no fit-probability credit" (Ph-B1 3(b)).
   grep "realistic branch": §0, §11.7, Q2 → "expected branch" as above.

### R2 — Q3 annex complete [T][G]

Add three rows to the annex (l.2732–2745) and widen the Q3 route list (l.2693–2694) by the same three items:

| term or route | criterion | planned test and expected count | status (probability) | cost of compliance | default (size at H) |
|---|---|---|---|---|---|
| **route 5: promotion model not submitted** (fewer than two classes with ≥ 24 promoted events on the pilot's 1,000 near-pass overlays) | B1-a, B4-c (π_k of every credited term) | 4–8 classes of 125–250 events; a class qualifies if π_k ≳ 0.10–0.19; 2–4 expected [E] | EST, not computable before the pilot; state "unlikely if R04 occupancy is as v1's, not excluded" with the expected count of classes | more near-pass overlays from the pilot's events (7 CPU-h per 1,000, development allowance) | every credited B1 and B4 term at H; (β) of Table 4.4c then becomes (γ)-like |
| **route 6: S_CKF NOT TESTED** (after R4) | B1-f (Df-9) | DIF on the 4,000 enriched test overlays at R06 (31 expected, 24 needed); NI by the rung split at R05 (92 / 120 / 378); SM on the hit-level test halves as B4-c | DIF P = 0.92 (with route 1); NI evaluable; SM as the B4-c rows | as the B1-a / B4-c rows | term at H on all own hits, i.e. ×1/(1 − ε_pair) above H_CKF (×5–50 at ε_pair = 0.8–0.98) |
| **B4-e, size** (in route 3) | B4-e | flatness of P(r) in MET bins on Z(νν) and W | unknown until the samples exist | none (a factorisation test) | multijets from the passing events only: floor N_MJ × 1.14/100 = **4.6×10³ events** at the planning N_MJ (460–46,000 over 0.1–10 %), by itself above the day-15 class |

Q3 text (l.2693–2694): "… B3-a…d and B4-e (a B4-e failure alone sets a floor of ≈ 4.6×10³ events); B2-c at depth;
the promotion model not submitted; S_CKF not tested." Add one clause stating the reach consequence of the default:
"(β) of Table 4.4c: 705–640 GeV at the 84 % edge for ceilings of 10–100 counts, if the promotion model is submitted"
(N-C5).

### R3 — pilot before its code [T]

Ruling: **the pilot keeps the full no-pile-up records and is classified when the classifier exists**; the classifier
is not moved into Phase 2. Reason: the own-hit classification depends on the hand-over variant that §4.4 point 2
freezes in Phase 3, so a day-0–5 classifier would be provisional anyway, and records cannot be lost.
- §4.4 point 5 (after "Until then every number in this document assumes G = 1."): "The pilot's no-pile-up jobs keep
  the full hit records (≈ 52 GB at 8.2 kB per event, FEAS_A [E]; more for the hard-scatter events), not only per-event
  summaries. They are classified by channel (i) as its first Phase-3 task (own-hit classes, k per layer type, all own
  hits, Df-9), provisionally by day 7 and with the frozen hand-over variant by day 12; the 1,000 near-pass overlays
  (7 CPU-h) are made from that classification."
- §11.7 inputs (l.2623–2624): "from the pilot (generated by day 5, classified provisionally by day 7 and finally by day
  12)".
- §11.7 rule 1 (l.2633–2634): "… and the pile-up estimate of the development occupancy model (at day 7: the v1-based EST
  pile-up rows of Table 4.4c, since the occupancy model exists only from day 16 … ; at day 15: the development model's
  R04–R07 inputs)". The fixer checks the date at which the occupancy model's R04–R05 inputs exist and writes it.
- §4.4 point 4, per-k comparison (l.786): "… runs once the occupancy model's R04–R05 inputs exist, at the latest by day
  14".
- §11.3 table row 5–17 channel (i): prepend "classification of the pilot's records (by day 7)". §11.4 and script
  storage line: add the pilot records (≈ 52 GB [E]); the §0 storage figure changes only if the printed total moves its
  rounding.
- 0 CPU-h.

### R4 — S_CKF samples [T], 0 CPU-h

- §4.4 point 4, *S_CKF (Df-9)* (l.734–735): replace "(attributed candidates on the unbiased B1 overlays and on the
  hit-level halves, derivation R04–R05, test R06)" by "(attributed candidates: for DIF on the enriched test overlays
  with their weights, derivation R04–R05, test R06 and R07 where evaluable; for NI by the rung split, derivation R04,
  test R05; for each SM process on its hit-level halves, derivation R04–R05, test R06). S_CKF is a survival factor
  conditional on the no-pile-up class, so the selection of the enriched overlays on that class does not bias it; the
  restriction to unbiased samples applies to the ceiling and leak tests only."
- Df-9 (l.2727): "credited only where tested (DIF R06 on the enriched overlays, NI R05 by the rung split, SM R06)".
- COM B1-f: the same samples and rungs.

### R5 — the mixed excess of the eleven processes [S][T]

**Ruling: adopt the paired pass for all eleven processes (≈ 36 CPU-h); entry at H′ is not the default.**
Reasons: (i) the cost (11 × 1,000 × 11.7 s = 35.75 CPU-h, 0.8 % of the approved figure, measured unit cost) is far
below the dismissal threshold and turns an untested credit into a test; (ii) the test is evaluable: the SM hit-level
halves hold hundreds to thousands of attributed counts at R04–R05 per 1,000 events (annex last row); (iii) H′ = P_geo +
Σ_all k f_k may exceed H by orders of magnitude for SM events with many prompt pairs in the road (Ph-C3), so entering
eleven processes at H′ would in practice remove their selections, a much larger physics cost than 36 CPU-h; (iv) a
borrowed c_mix cannot be kept: c_mix ≤ 1.26 holds only for a passed test.
- Script [3]: add `add("4a", "B4", "MUST", "paired pile-up-only finder pass on 1,000 test-half events of each of the
  eleven other SM processes (incl. Z(tautau), lost-lepton Z(ll), multijets)", 11000 * TRIAL, "11000 x 11.7 s", "M",
  "R5")`; update `N_PAIRED` and [5′] (a v4 → v5 delta block with this row).
- **Recompute with the script and quote the printed values** in §0, §11.2, §11.3, §11.6, Q4, COM ST-1 and the script's
  own summaries: MUST / reduced / full totals; the approved figure (mine: 4,573.6 + 35.75 = **4,609.4 → 4,609**); the
  1.3× thresholds (mine: **5,992**; MUST only 1.3 × 4,175.9 = 5,429; full 1.3 × 5,122.7 = 6,660); the envelope
  (approved + contingency) and its threshold; "all guesses doubled" (mine: 4,609 + 1,378 = 5,987 against 5,992); the
  critical-path production (2,453 + 36 = 2,489 CPU-h = 14.3 days) and the calendar (mine: 57.8 / 56.9 / 58.1 days;
  "58 days", "57 days" and "≈ 8 weeks" keep their rounding); the review-addition count in Q4 ("the 39 CPU-h" → the
  printed value). My values are ESTIMATE; the script's are binding.
- §4.4 point 4 (ii) (l.767–771): "(P5, R5; 62 CPU-h: the 4,000 unbiased B1 test overlays and 1,000 test-half events of
  **each of the fifteen SM processes**, script [3])"; delete "The eleven other SM processes take the excess fraction of
  the supplied process closest in topology (same hard-scatter estimator), labelled EST."
- COM B1-f / B4-c completeness rows; inventory INV-1 if it lists the paired-pass samples.
- §4.0 point 6, after the H′ sentence: "For SM processes H′ may exceed H by orders of magnitude; an EST from the C1
  Z(νν) development sample is a day-15 input, and a completeness not-PASS of a leading SM term is then in practice a
  loss of its selections" (Ph-C3, one sentence).

### C items to apply in the same pass (quick, each removes a real ambiguity; no re-review beyond the diff check)

- **Numbers and labels:** G-C1 (§0: write the printed approved figure and full-SHOULD figure, not "≈ 4,570 / 5,090");
  G-C2 (Df-10 and COM T1-h "4.7–4.9 %"); G-C5 / Ph-C4 (tag 0.34 [U]; "the two Z additions raise N_trig by 1.1 %"; with
  multijets 2.1 %); G-C6 (cite `bsum_wp.json` → `n_trig.not_included` for the multijet bracket, [U]); G-C14 (`s4cp.py`
  l.115; DIF rate minimum is WZ 1.5687); N-C11 (§11.3 table ends at the printed calendar value).
- **Contradictions between binding statements:** G-C3 (COM REF-2: "R-10 and R-20 before Phase 4a", as §6.4); G-C11
  (COM S1-a: deadline 4b, or "job completion only at 4a"); G-C4 (§4.7 l.1300: four supplied *processes* vs four sized
  *terms*).
- **Gate-A text:** N-C1 (Q4: one clause on why 58 days: "43.5 days have no critical-path production: development and
  freeze 19, ITERATE allowances 8, Gate B, reviews and writing"); N-C4 (folded into Q2, §7); N-C6 (Df-8: +156 CPU-h is
  exact toys up front, ≤ 236 is the switch after a failed f_T check); N-C7 (folded into R1).
- **Rule clarity:** G-C9 (staging: the first-half R06 rate is read on the derivation parity half, so the test half is
  not looked at before its prediction exists); Ph-C7 (the multijet ceiling test also tests the B4-e factorisation; a
  FAIL is charged to the factorisation first).

**Not adopted now (deliberately left for later phases; why safe):**
- G-C7 (multijet loose-population re-sizing if N_MJ ≫ 1 %): rule 6 re-allocates at day 12–15 and the floor is
  reported at day 15; any re-sizing is a Phase-3 decision inside the development allowance.
- G-C8 (CPU-h of the sub-topology alternative): the alternative is not the default; costed only if chosen.
- G-C12, N-C3 (BibTeX validator, rendering reviewer slots): these run in the review windows of 4a/4b/5 in freed
  slots; scheduled when those phases are planned; no effect on Phase 2–3 or on any number.
- G-C13: premise incomplete (§2).
- G-C15 (dof of s_model with 2–4 classes): the cap 0.231 and the declared-larger option exist; Phase 3 states the
  spread with the actual class count.
- Ph-C6 (c_ref for the multi-term workspace): a T1 implementation detail fixed when the workspace exists (Phase 4a);
  the convention (compare with the computed coverage) is already binding.
- N-C2 (decision-point card), N-C10 (derived documents), N-C8 (sourcing the branching fractions by R-5): orchestrator
  tasks after PASS (the Gate-A package) and a Phase-2 retrieval; the planning N_trig is replaced at day 12 anyway.

---

## 7. Consequence for Gate A: how Q2 must be put

If the expected branch of the default plan is a large measured background (≈ 10⁴ events) with a reach of ≈ 270 GeV
at the 84 % edge (≈ 390 GeV for a background known exactly, below 200 GeV with a 20 % systematic width; all on v1
placeholder efficiencies), then "proceed to production without a pause" is no longer an honest question: the rule is
expected to fire. Q2 must ask what the user wants the study to deliver in that expected case, give the upside case,
say what the day-15 rule then offers and at what cost, and name the paper that results in each case (PLAN §9, l.497–
509). The arbiter does not decide it. The ● stays on the strategy's existing rule (pause and ask); the user may
pre-answer the expected branch now.

**Exact replacement for Q2 (l.2679–2687):**

> **Q2, the deliverable if the background is large (the expected case).** By v1's own counts (EST, v1 placeholder
> efficiencies, best Λ per mass), hard-scatter conversions leave ≈ 10⁴ background events at the R08–R09 selections;
> the reach is then ≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if that background were known exactly; below
> 200 GeV with a 20 % systematic width), and the day-15 rule (preliminary at day 7) is expected to pause the study
> before production. Upside: if the conversions fall like the pile-up background, or a conversion-removing
> conditional (vertex veto B3-b, fit probability) is tested close to where it is applied, ≈ 420–455 GeV at the 84 %
> edge (median 470–500; ≈ 400–570 for the factor-e size uncertainty); if Z(νν) is tested and the other ceilings count
> 10–100 events, ≈ 705–640 GeV; with every ceiling empty ≈ 710 GeV (median 790), an upper edge. Existing bounds lie
> below about 180 GeV (R-20 pending). (§0, Table 4.4c, §11.7)
> If the day-15 projection exceeds B₅₀ = 300 events (or both pile-up estimators miss their cap), what should happen?
> ● (a) Pause and ask you at day 15: production waits for your answer (≈ 2 days of turnaround); the 156 CPU-h
> reserve is spent by rule 3(b) on testing the leading term at R06–R07. You then choose (b) or (c).
> (b) Authorise now to proceed with the measured background: no pause for this cause, 0 extra CPU-h, no delay. Paper:
> the plan's "real background" outcome: the first measured irreducible quirk-plane background, the reach at that B
> (≈ 270–390 GeV as above), the sideband recipe as the way out.
> (c) Authorise now a redesign before the freeze: a conversion-removing conditional developed and tested on the
> development and pilot samples; the freeze and everything after move by the redesign time (not estimable now,
> reported at day 15), CPU-h inside the development allowance and the reserve. Paper: the bounded "middle" outcome
> (upper branches above) if it works, otherwise (b).
> If the projection is at most 300 events (reach ≈ 560 GeV or more), production proceeds in every option and the paper
> is the plan's "middle" outcome, labelled "target not met: sample-size limited". A doubled pool (+665 CPU-h,
> ≈ +3.8 days) helps only if the ceilings are empty (≈ +25 GeV) and does not help in the expected case.

The fixer copies this text, replacing my numbers by the printed ones; the turnaround (≈ 2 days) is the Gate-B
reference of §11.3 (N-C4). Nothing else in §12.1 changes except the R2 additions to Q3 and the N-C1 clause in Q4.

---

## 8. Regression and motivated-reasoning checks

**Regression triggers (§6.7).** Phase 1 has no results; validation failure, > 80 % systematic, GoF and bin exclusion do
not apply. Tautological or pass-by-construction validations: the three of cycle 3 are removed. Two new *untested
credits* were introduced by the fixes: a survival factor tested on samples that cannot hold its counts (R4) and a
borrowed completeness fraction (R5); both are fixed in this iteration. No earlier phase to regress to.

**Motivated reasoning.** For the fourth cycle running, the summary layer picks the gentler member of a pair. This time
the facts that contradict the headline (v1's 86 → 13 → 2) were in v4's own Table 4.4b, and the text dismissed them as
"weak" on a reason (two counts) that does not hold for the conversions; the fix report claimed a reading was stated
that is not. None of this is concealment (every number used by the reviewers is in v4), but it is the pattern the
template names: "a limitation acknowledged in prose but not reflected in the result". R1 corrects it by making the
expected branch lead. I checked my own ruling against the opposite bias: the (α1′) branch is EST, rests on 13 and 2
counts and on one more width step of extrapolation, and could be removed by the B3-b vertex veto or a steeper v2 fall;
that is why the upside is stated in the same sentence, and why the ● stays on "pause and ask", which loses only the
turnaround if the pilot is kinder than v1.

**Competing group.** A competing group would know whether conversions dominate at R08 and would have a conversion veto
with a measured rejection. v2's pilot answers the first question by day 7; the second is option (c) of Q2.

**Brief compliance.** D4: completed by R2. D6/§7 stop rule: the base moves with R5 (printed). D7: unchanged. Nothing
discarded returns; F unchanged.

---

## 9. Convergence and the scope of cycle 5

This is cycle 4 (warn at 3, strong warning at 5, hard cap at 10). Merged A: 11 → 4 → 1 → 0. Open B: 5, all of them
specified above to the sentence or the script row. The protocol (`06-review.md` §6.5) requires a documented re-review
after every ITERATE, so cycle 5 cannot be skipped, but it can and should be narrow.

**Minimal legitimate scope of cycle 5 (verification only):**
1. **R1–R5**, item by item against §6 of this verdict: each statement written as specified; every [S] number printed
   by the amended script and quoted identically in §0, Table 4.4c, §11.2, §11.3, §11.6, §11.7, §12.1 (Q2, Q3, Q4) and
   COM. The physics reviewer re-runs [9b] and checks the (α1′) rows, the e^(±1) rows, the m_H = 1000 row and the
   extended mapping; the critical reviewer checks R2–R5 and the budget/threshold/calendar chain; the constructive
   reviewer reads §0 and §12.1 as the user and checks that Q2 is answerable in one line and that each option names
   its cost and its paper.
2. **The adopted C items** of §6, as a checklist (no new findings from them unless one introduces an error).
3. **A diff check v4 → v5**: every changed hunk of the strategy, COM and the script maps to R1–R5 or an adopted C
   item; any other change is reported. The script diff is limited to [3], [5′], [9b] (mapping, (α1′), e^(±1), m_H =
   1000, probabilities, headline line), the storage line of R3 and the totals that follow from R5. All other printed
   values of the script must be unchanged (compare the two outputs line by line).

Reviewers raise a new finding in cycle 5 only if it is a regression introduced by the fix, a factual error in a number
shown to the user, or a genuine Category A. Everything else is C. If cycle 5 confirms R1–R5 and the diff is clean, the
arbiter should PASS; a partial fix of one item calls for a short focused fix verified by the arbiter, not a further
full panel. This does not lower the bar on any defect listed here; it keeps refinements of a sound design, which
belong to Phase 2–3 measurements, from blocking the gate.

**Matters settled now as rules (not to be reopened):** which branch leads the headline (R1, by the v1 record, to be
replaced by the pilot's own counts at day 7/15 under the existing rule 1); the reading used for counted terms
(counted ceiling; factor e as size rows); the S_CKF samples (R4); the eleven paired passes (R5); the pilot records (R3).

---

## 10. Mapping of reviewer items to merged findings (every B)

| reviewer item | merged | | reviewer item | merged | | reviewer item | merged |
|---|---|---|---|---|---|---|---|
| Ph-B1 (1)–(5) | R1 | | G-B1 | R1 | | N-B1 | R1 |
| Ph-C1, C2, C5 | R1 (adopted) | | G-B2 | R2 | | N-B2 | R3 |
| Ph-C3 | R5 (one sentence) | | G-B3 | R4 | | N-C5, N-C7, N-C9 | R1 / R2 |
| | | | G-B4 | R5 | | N-C4 | R1 (Q2) |
| | | | G-C10 | R1 | | | |

Partial earlier findings: P2 → R1; P10 → R2. Regressions of fixes: P3 → R4; P5 → R5; P14 → R3.

---

## 11. Verdict

**ITERATE.**
- **Category A: none.**
- **Category B, all to be fixed before PASS, in priority order: R1** (the honest headline and Q2: the
  conversion-measured branch leads, ≈ 10⁴ events, ≈ 270 GeV at the 84 % edge, median ≈ 315, ≈ 390 at fixed B, the
  day-15 pause expected; script [9b] rows and mapping), **R5** (36 CPU-h paired passes; approved figure, threshold
  and calendar recomputed), **R2** (three Q3 annex routes and the B4-e size), **R4** (S_CKF samples, 0 CPU-h), **R3**
  (pilot records and classification dates, 0 CPU-h).
- The adopted C items of §6 in the same pass.
- Cycle 5: verification of R1–R5 and the adopted C items, with a v4 → v5 diff check (§9). This is review cycle 4; the
  strong warning of cycle 5 is noted in advance.
