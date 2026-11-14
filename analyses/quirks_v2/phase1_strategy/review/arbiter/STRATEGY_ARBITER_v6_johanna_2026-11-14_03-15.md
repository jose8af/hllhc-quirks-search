# Arbiter verdict: Phase 1 STRATEGY v6 (quirks v2), review cycle 6

Arbiter: Johanna, 2026-11-14 03:15. Fresh session. Role: `agents/arbiter.md`, prompt template followed in full
(cases 1–5, structured table, dismissal rules, regression check, motivated-reasoning check, reviewer-pressure
protection).
Artifact: `phase1_strategy/outputs/STRATEGY_ingrid_2026-11-14_02-20.md` ("v6"; "l." = a line of v6), `COMMITMENTS.md`
("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v6.txt` ("stdout"),
`outputs/FIX_REPORT_cycle5_ingrid.md`.
Reviews: physics Isolde ("Ph", 0 A, 0 B, 5 C), critical Ivan ("Cr", 0 A, 0 B, 5 C), constructive Jasper ("Co"; items
Jp-C1…C10; 0 A, 0 B, 10 C), all 2026-11-14 02:50. No plot validator (Phase 1 has no figures).
Also read: the five earlier verdicts (Dagmar, Eloise, Felix, Greta, Hugo = "AV5"), `prompt.md` §3, §6 Phase 1, §7,
`AGENT_RULES.md`, `phase1_strategy/CLAUDE.md`, `methodology/06-review.md` §6.1, §6.5, §6.5.1, §6.7,
`conventions/search.md`, `LOG.md` (incidents), FEAS_A/B (lines quoted in the package), and the cycle-5 constructive
review's item H-C2.
Computation: one standard-library run of the script (`nice -n 10 python3 -I`, 37.3 s, 34.7 MB max RSS). No sub-agents,
no git. I wrote only this file and the session log.

**Verdict: ITERATE.** Category A: none. **Category B: one, U1** (§7): the binding day-15 projection reads the
no-pile-up terms on all own hits before CKF, with no S_CKF and no conditional credit (§11.7 rule 1; Df-9), but the
Gate-A text states the day-15 expectation, the pause-avoiding branches and the success condition of Q2 (c) on the
after-CKF, credited basis. It says only the *day-7* reading is ×5–50 high. Two of Jasper's C items (Jp-C3, Jp-C4) are
this defect seen from two sides; I re-classify them as B under U1, together with Isolde's C-1 and C-5 and Jp-C1, which
sit in the same sentences. The fix is text plus two print lines, 0 CPU-h. The remaining 15 C items are adjudicated in
§8. The Gate-A package corrections are in §9.

---

## 1. Overall assessment

v6 is a sound and, apart from U1, honest strategy. The three reviewers verified T1–T3 thoroughly and independently,
the diff is fully attributed, the script reproduces byte for byte, and every number I traced in the Gate-A section is
on a printed line. After six cycles the design (closure scheme, zero-count convention, ceiling H, likelihood, stop
rules, schedule) is stable and has been reproduced three times per cycle.

U1 is not taste. Q2 is the central decision, and option (c) is the only route the strategy designs to a reach beyond
the existing bounds (l.2790). The human is told that (c) works if conversions fall by ×31–52 and the decays in flight
are reduced. By the rule that will actually judge (c) at day 15, those terms are read before CKF, so the bar is
higher by the strategy's own unmeasured factor 1/(1 − ε_pair) = ×5–50 — or (c) needs a rule admitting a pre-freeze
S_CKF estimate, which v6 does not have. The cycle-5 constructive reviewer raised this for "day-7/15" (H-C2). AV5's
prescribed sentence narrowed it to day 7, without a reason; the fixer copied it. That is the pattern of cycles 4 and
5 (the favourable basis reaching the human through the arbiter's own text), and the cycle-5 scope rules admit it as a
new finding (a factual error in text shown to the user, introduced by the fix).

The default answer to Q2 ((a), pause and ask) is not affected, and nor is the expected outcome (no reach beyond the
existing bounds; the pause becomes more certain).

---

## 2. Facts settled from sources (my own checks; VERIFIED unless tagged)

| question | evidence | result |
|---|---|---|
| Script reproduces | fresh run, `cmp` with `budget_stdout_v6.txt` silent; sha256 `3a9db8b3…8a11` | identical |
| Figures to approve | stdout l.123: 4,452.9 + 156.5 = **4,609.4**, threshold **5,992**; l.202: **57.8 d**; l.205: +2.0 d → **59.8 (60) d**; MUST-only 4,176 / 5,429 / 58.9; full 5,123 / 6,660 / 60.1; l.206 rider **4,616.4 / 6,001.3**, "if accepted at Gate A" | match §0, §11.2, §11.6, Q4, COM ST-1 |
| Expected branch | stdout l.326–356: (α1′) B₅₀ 6,825–10,193; w = 0.17 → s₉₅ 1,823–2,725 ≫ 621.5 ↔ 243 GeV; statistics-only 84 % edge 270–297, median 314–342, fixed B 392–419 | v6 l.64–72, 102–107, Q2 correct |
| T2 numbers | stdout l.352–357: (α1) 587 / 975; DIF 385 / 647; conversions removed 401 / 663; ×52.1 / ×31.0; credit 51 / 74 | correct |
| Basis of the (α) family | stdout l.286–295 and v6 l.779: v1's DIF and conversion counts "with pile-up, after CKF"; stdout l.371: Z(νν) conversion part m_H = 326 in the pilot on that basis | after CKF |
| Basis of the day-15 projection | v6 l.2716–2717 (rule 1): "max(zero-count floor, N_t·H) per term", DIF and conversions "from the pilot's counts"; l.865–866 (§4.4 pt 5): H "enters the day-7 and day-15 projections as Gamma(m + 1) of the pilot count m"; Df-9 l.2858: H on all own hits, S_CKF "credited only where tested"; S_CKF for SM is tested on the 4a hit-level halves (l.773, inventory row 20, phase 4a); the "CKF factor" input of the development overlays feeds rule 5 (redesign triggers), not the formula | **before CKF, no S_CKF, no conditional** at day 7 **and** day 15 |
| Size of the difference | v6 l.781–783: H = H_CKF/(1 − ε_pair), ε_pair "assumed 0.8–0.98, not measured" → ×5–50; route 6 (l.2877): a term whose S_CKF is not tested stays ×1/(1 − ε_pair) in the result | ×5–50, an assumption |
| What v6 tells the human | Q2 l.2775–2776: "The day-7 reading counts own hits before CKF (Df-9) and may be ×5–50 above this figure"; (c) l.2795–2797: "×31–52 … **and** the decays in flight (385–647 events) reduced"; §0 l.92–93 and Q2 l.2780: "(α1) with fit-probability credit" avoids the pause | U1 |
| Stop conditions | v6 l.2667–2674 vs `prompt.md` l.341–348; l.2676 vs D6 l.79 | word for word |
| Package length | Co §5 text: 2,590 words, 15.2 k characters | ≈ 5 pages; the brief allows 3 |

---

## 3. T1–T3: final status

| # | Ph / Cr / Co | final | reason |
|---|---|---|---|
| T1 | R / R / R | **RESOLVED** | Case 1. The width 0.17 statement, the photon-rate range, the statistics-only labels and the ESTIMATE marking are present at every location (Ph §4, Cr §4 greps, Co §1.3), on printed lines. The basis clause on the background size (after CKF) is part of U1, not a T1 residual: the reach conclusion holds a fortiori. |
| T2 | R / R / R | **RESOLVED as ordered; residual carried as U1** | Case 4: all three verified v6 against AV5's text, and v6 matches it. The first half (no (α) branch and no veto alone avoids the pause) is right at v1's central sizes. The success condition of (c), as AV5 worded it, sits on the after-CKF, credited basis, while the rule that judges (c) does not. That residual originates in AV5's text, not in the fixer's work. |
| T3 | R / R / R | **RESOLVED** | Case 1. 60 days (59.8) including the expected pause in §0, §11.2, §11.3, §11.6, Q4 and COM ST-1; 57.8 always labelled "without the pause" (Cr §3). The rider is nowhere treated as adopted. |

---

## 4. Closing ledger of the earlier findings

"c*n*" = closed by the verdict of review cycle *n* (the fix was in version *n*). "→" = carried into the named later
finding. GA = accepted as a Gate-A question; Df = accepted as an overridable default; DP = a downscope proposal in Q4.

| findings | final disposition |
|---|---|
| M1 zero counts | R c2; definition residuals N3, N6, N10 R c3 |
| M2 C1 blinding | GA **Q1** (sealed tier, §4.1 l.603–628; COM C1-d) |
| M3 same-rung closure | R c2 |
| M4 extrapolation width | → N5 → P8 (R c4); crossing credit → P7 (R c4) |
| M5 testability / NOT TESTED | → N1, N2 → P4 (R c4), P10 → R2 (R c5); the D4 exception is GA **Q3** |
| M6 floors, central target | GA **Q2**; "target met" → N3 (R c3) → P9 (R c4); projection → N7 → P1 (R c4), P2 → R1 → T1 (R c6) |
| M7, M14, M18, M21, M27, M29, M31–M34 | R c2 |
| M8 T1-g toy budget | R c2; T1-h true rates → N6 (R c3); coverage family → P11 (R c4), Df-10 |
| M9 MET validation | R c2; fallbacks → N13, ordering → N15 (R c3) |
| M10 stop rule | R c2; envelope → N12 (R c3); reserve → P13 (R c4); quoted exactly, §11.6 |
| M11 variation sizes | → N13 (R c3); Df-7 |
| M12 nuisance propagation | R c3 |
| M13 [DP2] point set | DP **[DP2]** in Q4 |
| M15 closure statistics | → N4 (R c3); ceiling family → P6 (R c4) |
| M16 time-tag credit | Df-5; design gaps → N16 (R c3) |
| M17 undeclared signal quantities | R c2; ordering → N15 (R c3); BL-1 |
| M19 costs | R c2; staffing → N18 → P16 (R c4) |
| M20 S1 ×10 | Df-1 |
| M22 attribution | R c2; mixed candidates → N1 → P5 (R c4) → R5 (R c5) |
| M23 K validations | Df-3 (σ_NLO nominal, resummed beside it) |
| M24 Herwig attempt | dated commitment, R c3; **[DP5]** in Q4 |
| M25 identifiers | R c2, residual R c3 |
| M26 background list | → N9 (R c3) |
| M28 infracolour | Df-3 (one-sided band) |
| M30 dE/dx | Df-4 |
| M35 sample inventory | R c2; overlays → N17 (R c3) |
| N1 ceiling H | → P3, P4, P5, P6 (R c4); P3 → R4, P5 → R5 (R c5); Df-9, Df-2 |
| N2 MUST NOT TESTED / D4 | → P10 → R2 (R c5); GA **Q3** |
| N3, N4, N6, N8, N9, N10, N11, N12, N13, N15, N16, N17 | R c3 (N11 sample naming → P15 R c4; N12 → P13 R c4; N16 also Df-5) |
| N5 widths | → P8 (R c4) |
| N7 projection | → P1 (R c4), P2 → R1 → T1 (R c6) |
| N14 D7 reading | → P12 (R c4); GA **Q5** |
| N18 Phase-3 staffing | → P16 (R c4) |
| P1 (A) Z(ττ), Z(ℓℓ) pool shares | R c4 (inventory rows 18a, 18b) |
| P2 headline | → R1 → T1 (R c6); basis clause in U1 |
| P3 CKF in H | R c4; sample regression → R4 (R c5); Df-9 |
| P4, P7, P8, P9, P15, P16 | R c4 |
| P5 mixed numerator | R c4; borrowing → R5 (R c5) |
| P6 ceiling family | R c4; Df-2 |
| P10 Q3 routes | → R2 (R c5); GA **Q3** annex |
| P11 coverage | R c4; Df-10 |
| P12 Q5 premise | R c4; GA **Q5** |
| P13 reserve outside the figure | R c4; Q4 figure 4,609 / 5,992 |
| P14 day-15 inputs | R c4; pilot code schedule → R3 (R c5) |
| R1 honest headline | → T1 (R c6); basis clause in U1 |
| R2, R3, R4, R5 | R c5 |

Nothing is open except U1. AV5 §6.4 left four C items for named later phases (Ph-C3, Ph-C4 downside, H-C8, Cr-C7).
Those deferrals remain valid, and Cr confirms they were not touched.

**Spot-checks against v6 (my own reading, eight dispositions):**
1. **Zero-count convention and its coverage test** (M1, N6, P11). §4.11 point 4 and T1-c (l.1717–1730) give the
   Gamma(m + 1) generation and five tests. The coverage family (l.1756–1766) has FAIL below 462 of 500 at
   c_ref = 0.95, family-wise 4.7–4.9 %, INVESTIGATE and one re-test, and a target independent of the quoted ensemble.
   COM T1-c and T1-h agree. **Confirmed.**
2. **Closure scheme: disjoint rungs and NOT TESTED** (M3, M5, N2). §4.0 point 1 (l.364–368) defines derivation and
   test as disjoint, with comparisons at the same rung being consistency checks without a verdict. Point 5
   (l.429–433) gives four verdict classes. Point 6 (l.451–456): NOT TESTED earns no credit, and every MUST route is
   in Q3 with its probability. **Confirmed.**
3. **Ceiling H: definition and tests** (N1 → P3–P6, R4, R5). H on all own hits with S_CKF (l.766–787, Df-9); one
   Šidák verdict per term (l.798); paired pile-up-only pass (l.810, l.1091, l.1390); ceiling and leak tests on
   unbiased overlays, S_CKF on enriched (l.773–776). **Confirmed.** Reading this section is where U1 arose.
4. **C1 sealed comparison** (M2). Sealed tier outside the repository, encrypted, a dedicated agent, PASS/FAIL until
   Gate B, opening needs the user (l.612–628). Q1 l.2763–2767. **Confirmed.**
5. **Stop conditions** (M10). Quoted word for word (§2), and the 1.3× rule is applied to the approved figure of Q4:
   5,992 for 4,609 (l.2683–2684), 6,001 only with the rider. **Confirmed.**
6. **Q3 annex** (P10 → R2). Routes 1–6 with probabilities, costs and the default size at H, including the promotion
   model, S_CKF and the B4-e floor of 4.6×10³ events (l.2861–2879). **Confirmed.**
7. **Reserve inside the figure** (P13). stdout l.120–125. **Confirmed.**
8. **Pool shares of Z(ττ) and lost-lepton Z(ℓℓ)** (P1, the cycle-3 A). Inventory rows 18a and 18b, re-allocated at
   day 12–15. **Confirmed.**

---

## 5. Independent last-line checks on v6

(a) **Brief items.** C1–C3, B1–B7, T1–T2, S1–S2 and P1 each have a section in §4.1–4.15. Each section heading states
the phase, and each section gives the method, a pre-fixed criterion, the statistics and a "Cost." line (script [3],
[4]; per-phase totals in stdout l.93–101). **S3** (l.2053–2058) is exactly as brief D1 fixed it: "signal ×1.5–3.2;
reach 866 → 1062 GeV at B = 10, g = 1", an EST outlook, with no endcap row as a result. **S4/S5**: a proposal not to
include them, with costs ([DP4]). ✓
(b) **COM.** Every plan item has a row with its criterion, phase and deadline. 73 item rows are "open", S3 is "dropped
(user)", and S4/S5 are "undecided, pending Gate A". The strategy rows, the systematics rows SY-1…14 and the checks
VC-1…3 are all open. ✓
(c) **Conventions enumeration.** §5.1 answers every row of the conventions systematic tables (signal 4, background 5,
detector 4, theory 3, plus the pp replacements). §5.2 answers checks 1–6 and the standard configuration. The pitfalls
(VR blind spot, transfer factor, pruning, low-statistics asymptotics) are answered (l.2160, l.1746). ✓
(d) **Blinding invariant and pre-registration outline.** "No v2 signal efficiency is computed or assumed" (l.26);
BL-1 lists the only exceptions (Q1, and the selection-independent A, f₂₀₀, m_mig); §8 freezes the criteria at Gate A
and hashes `PREREG_v2.md` before any production sample. Inventory rows 14–25 do not exist before the hash. ✓
(e) **Stop conditions** quoted correctly, and 1.3× tied to 4,609 → 5,992 (§2, spot-check 5). ✓
(f) **Nothing discarded has returned.** There is no ρ = 3 (l.1182), no pile-up scan (l.1452), no Stage 3 at
Λ ≥ 15 keV (l.1898), no cloud (l.2266), no ×100 growth, and no Open Data. The endcap is an outlook only. ✓
(g) **Expected outcome.** The statement is honest and consistent, as the three reviews show: background ≈ 0.7–1.0×10⁴
events led by hard-scatter conversions; reach below 243 GeV at the strategy's own width, at or near the existing
bounds; day-15 pause expected; upside labelled statistics-only; ESTIMATE on v1 placeholders. **One exception, U1:**
the background size is on the after-CKF basis, without saying so, and the day-15 reading is not.
(h) **Figures to approve** reproduced: 4,609 CPU-h; threshold 5,992; 60 days including the pause, 57.8 without;
rider 4,616 / 6,001 only as an option (§2). ✓

---

## 6. Structured adjudication table (cycle 6)

| # | finding | source | their cat | final | rationale |
|---|---|---|---|---|---|
| **U1** | Day-15 projection on the own-hit, uncredited basis, while the Gate-A text gives the day-15 expectation, the avoiding branches and the (c) condition on the after-CKF, credited basis | Co Jp-C3, Jp-C4; cycle-5 H-C2; arbiter (Case 5 for the consequence on (c)) | C, C | **B** | Case 3, verified §2. Jp-C3 is factually right: rule 1's formula has no S_CKF, and no SM S_CKF exists before 4a. Jp-C4 is right: rule 1 admits no conditional. Jasper drew no consequence for (c). I do: v6 states the (c) bar, on the strategy's only designed route to a reach beyond the bounds, low by the factor v6 itself puts at ×5–50, and leaves undefined on what basis a pre-freeze redesign is judged. That would mislead a human who chooses (c). Reviewer-pressure rule: AV5 narrowed H-C2 to day 7 without evidence; rule 1 (l.2716) and §4.4 point 5 (l.865) are independent evidence that H-C2 was right. |
| U1-a | T2 holds at v1's central DIF size (1–2 counts); at ×e⁻¹ a veto alone would suffice | Ph C-1 | C | **B, inside U1** | Case 3, verified on Table 4.4c's e⁻¹ row (stdout l.352: B₅₀ 230). It sits in the (c) sentence that U1 rewrites. |
| U1-b | Quote B₅₀ with the conversions removed (401–663) against the class limit | Ph C-5 | C | **inside U1** | Case 3; stdout l.353–354. Same sentence. |
| U1-c | (c) does not say whether it may target the decays in flight | Co Jp-C1 | C | **inside U1** | Case 3. The success condition needs a DIF reduction that (c) does not authorise. |
| 1 | Robustness: the conclusion holds for any width ≥ 0.05 | Ph C-2 | C | C (ii) | Package content; stdout l.328, 337, 343, 349. |
| 2 | Lower photon-rate end (Z(νν) 0.2306) | Ph C-3 | C | C (iii) | §8. |
| 3 | §4.11 point 3 "expected" wording | Ph C-4 | C | C (i) | Wording. |
| 4 | §11.3 timeline and §11.7 table on the no-pause basis, unlabelled | Cr C1 | C | C (i) | Label. |
| 5 | Range figures (49 / 65 days) on the no-pause basis | Cr C2 | C | C (i) | Label. |
| 6 | "missed by about four weeks" (written for 58 days) | Cr C3 | C | C (i) | Stale paraphrase; no computed number changes. |
| 7 | Rider part (3) vs the booked 1,000 DIF overlays | Cr C4 | C | C (i) | Wording. |
| 8 | Fix report "30 added lines" (29 + 1 changed) | Cr C5 | C | C (iii) | Not the artifact; recorded here. |
| 9 | "(c) is then the only route" too strong | Co Jp-C2 | C | C (i) | Wording. B3 credit is measured in production under every option (annex route 3). |
| 10 | "≈ 560 GeV or more" without the statistics-only label | Co Jp-C5 | C | C (i) | Label. |
| 11 | (c) omits the veto's signal-side risk | Co Jp-C6 | C | C (i), placed in the U1 text | Restates l.1276–1280 and l.1783. |
| 12 | The reserve is spent twice in the text | Co Jp-C7 | C | C (i), placed in the U1 text | Wording. |
| 13 | "irreducible" for a conversion-led background | Co Jp-C8 | C | C (i) | Wording; §2 l.199 calls only Z(νν) hard-scatter tracks irreducible. |
| 14 | Paths to a stronger paper; what remains publishable | Co Jp-C9 | C | C (ii) | Package content. |
| 15 | No single list of decision points | Co Jp-C10 | C | C (ii) | The package's §6 supplies it. |
| 16 | A latent §6.7 trigger: in the expected branch the conversion normalisation will likely exceed 80 % of the total uncertainty | arbiter (Case 5) | — | C (ii) | v6 l.2154 already commits to investigate, not accept. One line in the package risks. |

**Dismissals: none.** Every reviewer item is applied, packaged or deferred with a reason (§8). Cost check (§6.5.1):
U1 is under one agent-hour of text plus two print lines.

---

## 7. U1: finding and exact fix (fixer, 0 CPU-h)

**Finding.** Under Df-9 the day-7 and day-15 projections read every no-pile-up term as N_t·H on all own hits, before
CKF and with no conditional (rule 1, l.2716–2717; §4.4 point 5, l.865–866). Table 4.4c's (α) family (DIF and
conversions from v1's counts "with pile-up, after CKF") is on a different basis. v6 tells the human that only the
day-7 reading is high, lists "(α1) with fit-probability credit" among the branches that avoid the binding pause, and
states the (c) success condition (×31–52 and a DIF reduction) on the after-CKF, credited basis, without defining how a
pre-freeze redesign is credited in the test. In the result, processes whose S_CKF test is not evaluable stay on the
own-hit basis (annex route 6), so "≈ 0.7–1.0×10⁴" is a lower value.

**Ruling on the basis for (c).** (c) already says that the conditional is "developed and tested on the development and
pilot samples". A redesign judged before the freeze can only be judged on development estimates. The minimal
consistent rule is therefore that the (c) test multiplies by the redesigned conditional and by S_CKF, each estimated on
development samples and labelled EST. Credit in the result still comes only from the post-freeze tests. The rule for
(a) and (b) is unchanged.

**Exact changes (printed values replace my bracketed values; the fixer copies printed values).**

1. **Script, [9b] v6 block, two print lines (0 CPU-h).**
   (i) "(α1) conversions removed, DIF × e⁻¹ (both falls): B₅₀ …" — expected [E: 401 − 385 + 385/e ≈ 158; 663 − 647 +
   647/e ≈ 254].
   (ii) "(α1′) on the day-15 own-hit basis, conversions and DIF × 1/(1 − ε_pair) at ε_pair = 0.8 / 0.98: B₅₀ …" —
   expected [E: ≈ 5×10⁴ / ≈ 5×10⁵].
   No other line changes. Save `budget_stdout_v7.txt`.
2. **§11.7 rule 1**, after "and it becomes binding at day 15.", insert:
   > The projection of a no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional credit (Df-9);
   > its DIF and conversion terms are therefore expected ×1/(1 − ε_pair) above the after-CKF rows of Table 4.4c
   > (×5–50 at the assumed ε_pair = 0.8–0.98; script [9b], v7 line). Only the test of a Q2 (c) redesign multiplies
   > the leading terms by the redesigned conditional and by S_CKF, each estimated on development samples (the C′_PU γ
   > sample, the DIF overlays 13a, the pilot's near-pass overlays; with the rider, the 1,000 γ overlays) and labelled
   > EST. No credit in the result comes from these estimates.
3. **Q2 stem.**
   - "The day-7 reading counts own hits before CKF (Df-9) and may be ×5–50 above this figure." → "The day-7 and
     day-15 projections count own hits before CKF, with no S_CKF and no conditional credit (Df-9, §11.7 rule 1), and
     are expected ×5–50 above this figure [printed line]."
   - After "≈ 0.7–1.0×10⁴ background events at the R08–R09 selections", insert "(after CKF, as v1 counted them; a
     lower value, since terms whose S_CKF test is not evaluable stay on all own hits, annex route 6)".
   - "(α1) with fit-probability credit;" → "(α1) with fit-probability credit, which the day-15 projection admits only
     under (c);".
   - "so a conversion veto alone does not avoid the pause" → "so at v1's central decays-in-flight size (1–2 counts)
     a conversion veto alone does not avoid the pause".
4. **Q2 (c)**, replace from "CPU-h inside the development allowance and the reserve." to "The veto's rejection has not
   been measured." with:
   > CPU-h inside the development allowance and what remains of the reserve. Paper: the bounded "middle" outcome
   > (upper branches above) if it works, otherwise (b). It works if the projected B₅₀ is at most 300, with the
   > redesigned conditional and S_CKF estimated on development samples (EST, §11.7 rule 1). That needs the
   > conversions reduced by ×31–52 (96.8–98.1 %) **and** the decays in flight reduced: with the conversions removed,
   > B₅₀ is 401–663 at v1's central size, of which decays in flight 385–647. That size rests on 1–2 counts; at its
   > size ×e⁻¹ the conversions alone would suffice (B₅₀ [158–254], script [9b]). If S_CKF cannot be estimated before
   > the freeze, every reduction must be ×1/(1 − ε_pair) larger (×5–50, not measured). As worded, (c) targets the
   > conversions; if you choose it, say whether it may also target the decays in flight. The veto's rejection has not
   > been measured; its signal cost is known only at Gate B, and T2 keeps every selection with and without it.
5. **§0.**
   - "The pause." paragraph: "avoids it on its own." → "avoids it on its own at v1's central decays-in-flight size
     (1–2 counts)."; "as in (α1) with fit-probability credit (51–74)" → "as in (α1) with fit-probability credit (51–74;
     admitted in the day-15 projection only under Q2 (c))"; append "The day-7 and day-15 projections read own hits
     before CKF (Df-9) and are expected ×5–50 above the after-CKF figures of this summary."
   - "Expected": after "(v1's N_trig-weighted and maximum photon rates, 0.255 and 0.379 per event)" insert "(after
     CKF, as v1 counted them; a lower value where S_CKF is not tested, annex route 6)".
6. **Labels (cycle-5 H-C2 residual).** l.785, after "(≈ 3×10² in the pilot)" insert "(after CKF; ×1/(1 − ε_pair) on
   all own hits)". l.865, "≈ 3×10² if the conversions keep v1's fall" → "≈ 3×10² after CKF, ×1/(1 − ε_pair) more on all
   own hits, if the conversions keep v1's fall".
7. **COM.** No criterion changes. In the version-7 change table, one row: "§11.7 rule 1 basis of the day-15
   projection stated; Q2 (c) test on development estimates (U1); no status changed".
8. **§13.6** change table (the general rule). Nothing else is touched.

---

## 8. The C items (20): disposition

### (i) Apply before commit (wording or labels only; no number, criterion or commitment changes)

| item | location | exact change |
|---|---|---|
| Ph C-4 | §4.11 point 3, l.1654 | "**The reading expected from Table 4.4c is "target not met: sample-size limited" while the ceilings count few events**" → "**The reading expected if the day-15 pause does not fire is "target not met: sample-size limited" while the ceilings count few events**" (keep the parenthesis that follows) |
| Cr C1 | §11.3 timeline caption (heading l.2560) and §11.7 table row 3 (l.2704) | heading: append "; days without the day-15 pause, every day after 15 moves by ≈ 2 in the expected branch". Row 3: "days 36.8–48.8 (Gate B at ≈ 49)" → "days 36.8–48.8 (Gate B at ≈ 49), without the day-15 pause" |
| Cr C2 | §0 l.119–120; §11.3 l.2596 | after "65 days at 50 % utilisation" (§0) and "65 days if the production utilisation is 0.50" (§11.3), insert "(both without the day-15 pause)" |
| Cr C3 | §11.6 l.2654 | "missed by about four weeks" → "missed by four to five weeks" |
| Cr C4 | Q2 rider part (3) | "(3) 1,000 γ development overlays (seeds disjoint from 4a)" → "(3) 1,000 γ development overlays, in addition to the 1,000 DIF overlays of P4 (seeds disjoint from 4a)" |
| Jp-C2 | Q2 (b), l.2790–2791 | "(c) is then the only route in this strategy to one." → "(c) is then the route this strategy designs for one; the conditionals measured in production may add some reach, with credit not yet measured." |
| Jp-C5 | Q2, l.2798 | "(reach ≈ 560 GeV or more)" → "(reach ≈ 560 GeV or more, statistics-only)" |
| Jp-C6 | Q2 (c) | included in the U1 text (§7 item 4, last clause) |
| Jp-C7 | Q2 (c) | included in the U1 text ("what remains of the reserve") |
| Jp-C8 | Q2 (b), l.2787 | "the first measured irreducible quirk-plane background" → "the first measured quirk-plane background (led by conversions)" |

### (ii) Into the Gate-A package only

- **Ph C-2:** "The conclusion holds for any normalisation width of 0.05 or more, including the transfer-factor width a
  sideband estimate would carry (stdout [9b])."
- **Jp-C9:** paths to a stronger paper (none demonstrated) and what remains publishable. The text is in Co §5,
  amended per §9.
- **Jp-C10:** the list of decision points (Co §5 §6).
- **Arbiter item 16:** in the expected branch the conversion normalisation will probably dominate the uncertainty
  (> 80 %, a §6.7 trigger); the strategy investigates rather than accepts it (l.2154), with the sideband recipe as the
  way out.
- Isolde's C-1 caveat and Jasper's C-1 question also appear in the package, in their U1 form.

### (iii) Deferred

- **Ph C-3 (photon rate 0.2306) → Phase 2, pilot reading.** The quoted range is labelled with the two rates it uses,
  and the conclusion holds at any width ≥ 0.05 and at either rate. The pilot measures the conversions directly at
  day 7, which replaces every v1 rate. Cost if done now: < 0.2 h. It is left only to keep cycle 7 narrow; it changes
  no choice.
- **Cr C5 (fix-report line count) → no action.** It concerns a non-artifact report; the correct count (29 added + 1
  changed) is recorded here.

---

## 9. The Gate-A package (Co §5): corrections before it is presented

I checked the candidate number by number against v6 and stdout. Every number matches: the cluster-cost table against
Table 4.0; 753 / 2,322 / 1,378; FEAS_B 92.33 ± 0.07 vs 92.26 ± 0.04 fb, K = 1.165, Geant4 ≈ 3 min; the `LOG.md`
times 14:06, 15:12 and 15:20; DP1 −358 and DP2 −155 (l.2633–2634); 43.5 = 19 + 14.5 + 8 + 2; the §5 rows sum to
4,609 and the days match §11.3; Gate B ≈ 49 (51) and Gate C ≈ 58 (60). The framing is honest, with the expected
outcome before the upside. Corrections the orchestrator must make:

1. **Sources:** point to STRATEGY v7 and `budget_stdout_v7.txt` after the U1 fix.
2. **Length.** The draft is 2,590 words, about 5 pages; the brief allows 3. Cut to about 1,500 words. Suggestions:
   - compress the cluster-cost table to one line of the four costs that set the schedule (13.5 s, 11.7 s, 206 s at
     1.46 GiB, 45 ms guessed) plus a pointer to Table 4.0;
   - shorten the software paragraph to two lines;
   - list the defaults Df-1…Df-10 one short line each, without the alternatives column except Df-1 and Df-9;
   - shorten the Q3 route list to one line.
   Keep everything the brief requires.
3. **§1 headline:**
   - after the background size, add "(after CKF; the day-7 and day-15 projections read own hits before CKF and are
     expected ×5–50 higher)";
   - "Removing the conversions alone would not avoid the pause, because the decays in flight alone are 385–647
     events" → "… because, at v1's central size (1–2 counts), the background without conversions is 401–663 events,
     of which decays in flight 385–647";
   - "The often-quoted ≈ 270–300 GeV" → "The ≈ 270–300 GeV";
   - add the Ph C-2 robustness sentence.
4. **§1 "What the upside would take":** the second bullet becomes "a conditional that removes ×31–52 of the
   conversions and a reduction of the decays in flight, judged on development estimates of the conditional and of
   S_CKF (Q2 (c))".
5. **§2 "Review":** "Five review cycles reduced the must-resolve findings 11 → 4 → 1 → 0 → 0" is wrong in two ways:
   those are Category A counts only, and B items persisted. Use: "Seven review cycles (Category A 11 → 4 → 1 → 0 → 0 →
   0 → …; Category B 24 → 14 → 15 → 5 → 3 → 1 → …)". Add to the cycles 4–5 clause "and fixed the S_CKF samples and the
   mixed-excess pass (+36 CPU-h)", and add "cycle 6 corrected the basis of the day-15 projection shown to you (U1)".
   "Cycle 6 verified these changes" → the cycle-7 statement, written only after a PASS.
6. **Q2 (c):** copy the v7 text of U1 (§7 item 4) in shortened form; in particular restore "or a faster fall" in
   meaning ("reduced"), add the development-estimate basis, the 1–2 count caveat and the ×5–50 alternative. The
   draft's "reduced by a credit" alone is narrower than v6.
7. **Q2 (b):** keep "the first measured quirk-plane background (led by conversions)" and the sentence on production
   conditionals, as v7 will have them.
8. **Q2 note** ("day-7 and day-15 readings … ×5–50"): keep; it now matches v7.
9. **§6 Day 15:** add "(read on own hits before CKF; a (c) redesign is judged on development estimates)".
10. **§7 top risks:** item 1 becomes "… unless a demonstrated ≈ 97 % conversion rejection is combined with a
    reduction of the decays in flight, judged on development estimates"; add, as a short item, "the conversion
    normalisation will likely dominate the uncertainty in the expected branch (> 80 %), to be investigated, not
    accepted".
11. **Upside list:** label the (β) row "conditional on the promotion model being submitted" (already present) and
    keep "upper edge" on the empty-ceiling row. No change of numbers.

---

## 10. Regression, motivated-reasoning and competing-group checks

**Regression triggers (§6.7).** Phase 1 is the origin phase and has no results. Latent in the design:
- *> 80 % single systematic:* likely in the expected branch (the conversion normalisation at w ≈ 0.17 on ≈ 10⁴
  events). v6 commits to investigating it (l.2154), and B5 is the data-driven way out. This is to be watched at 4a;
  it is not a defect now.
- *Tautological comparison:* none. Same-rung comparisons are consistency checks without a verdict (§4.0 point 1). The
  coverage target is independent of the quoted ensemble (T1-h).
- *Closure failure, GoF, bin exclusion:* they do not apply before data; the failure protocol (FP-1) reports and does
  not patch.

No trigger is met.

**Motivated reasoning.** In every cycle since cycle 3 the gentler of two bases has reached the human: the optimistic
edge (P2), the pile-up fall (R1), statistics-only reach (T1), and now the after-CKF basis of the (c) bar (U1). Each
time the honest version changed no default, and each time it changed what the human is told about a live option. I
checked my ruling against the opposite bias:
- ε_pair 0.8–0.98 is v6's own assumption. I do not assert ×5–50 as measured, and the fix says "assumed".
- Isolde's C-1 goes the other way (DIF may be smaller). I put both directions into the (c) sentence.
- I did not lower any reach or add any CPU-h.

**Competing group.** A competing group would measure S_CKF and the veto on pile-up samples before committing. The U1
rule for (c) does exactly that on development samples, and the rider's γ overlays provide the conversion case.

**Brief compliance.** D1, D4, D6, D7 and D8 are respected, the §7 stop rules are quoted exactly, and nothing discarded
has returned (§5).

---

## 11. Iteration history (audit trail)

| cycle | version | merged A | merged B | verdict |
|---|---|---|---|---|
| 1 | v1 (Brigitte) | 11 | 24 | ITERATE |
| 2 | v2 (Dmitri) | 4 | 14 | ITERATE |
| 3 | v3 (Emeric) | 1 | 15 | ITERATE |
| 4 | v4 (Fiona) | 0 | 5 | ITERATE |
| 5 | v5 (Gunnar) | 0 | 3 | ITERATE |
| 6 | v6 (Ingrid) | 0 | 1 (U1) | ITERATE |

Merged A: 11 → 4 → 1 → 0 → 0 → 0. This is cycle 6 (strong warning at 5, cap at 10). The strong warning is noted.
Convergence is real: B has fallen 24 → 1, and the last three cycles changed only how the expectation is stated.

**What the six cycles changed in substance.**
- Cycles 1–2 rebuilt the statistical core: zero-count terms that could vanish in the expected limit were replaced by
  the Gamma(m + 1) convention with five tests and a coverage family; closure tests at the derivation rungs were
  replaced by disjoint derivation and test with four verdict classes and an extrapolation width that is always in
  the likelihood; the ceiling H was defined and then tested as a ceiling; the stop rule was restored to the brief's
  wording; and every MUST route to NOT TESTED was put to the user as a D4 exception (Q3).
- Cycle 3 completed the background pool (the Z(ττ) and lost-lepton Z(ℓℓ) shares, the only late A), fixed H with
  respect to CKF, the ceiling-test samples and family, and the coverage false-fail rate, and brought the reserve
  inside the approved figure.
- Cycles 4–6 changed what the human is told. The expected outcome went from "≈ 790 GeV if every ceiling is empty" to:
  a conversion-led measured background of ≈ 10⁴ events, no reach beyond the existing bounds at the strategy's own
  normalisation width, an expected day-15 pause included in the 60-day calendar, and (with U1) the true basis on
  which a redesign would be judged.

The CPU-h figure moved only from 4,378 to 4,609, and the design of the samples is unchanged since cycle 4.

---

## 12. Cycle 7: narrow re-review

The protocol requires a documented re-review by the Phase-1 panel: three fresh reviewer sessions and a fresh arbiter.
The scope is narrowed:

| role | verifies exactly |
|---|---|
| physics | U1: the two new print lines (method: ×1/(1 − ε_pair) on the DIF and conversion terms; DIF × e⁻¹ with the conversions removed); that rule 1's new sentence matches Df-9 and route 6; that the (c) condition and the §0 / Q2 clauses follow from the printed lines |
| critical | the v6 → v7 diff of the strategy, COM and the script: every hunk maps to §7 items 1–8 or §8 (i); stdout v7 differs from v6 only by the two new lines; greps show that "day-7 reading counts own hits" and "only route in this strategy" appear only in history rows |
| constructive | Q2 and §0 read as the human: is the (c) bar and its basis plain, and is the default answer unchanged |
| arbiter | the three reviews against U1 and §8 (i); PASS if they are resolved and the diff is clean |

New findings are admissible only as a regression of this fix, a factual error in a number shown to the user, or a
genuine A. Everything else is C, for the package.

**Settled now (not to be reopened):** the day-15 projection basis (rule 1 as written, own hits, no S_CKF, no
conditional) for (a) and (b); the (c) test on development estimates, labelled EST.

---

## 13. Verdict

**ITERATE.**
- **Category A: none.**
- **Category B, to be fixed before PASS: U1** (§7 items 1–8), which absorbs Jp-C3, Jp-C4, Ph C-1, Ph C-5 and Jp-C1.
  Priority order: rule 1 sentence → Q2 (c) → Q2 stem → §0 → labels l.785 / l.865 → script lines → COM row.
- **Apply in the same pass, without re-review beyond the diff check:** the ten (i) items of §8.
- **Gate-A package:** Co §5 with the eleven corrections of §9, and at most 3 pages.
- **Cycle 7:** narrow 4-bot re-review by fresh sessions, §12.
- **After cycle 7 PASS,** the artifact of record for Gate A is STRATEGY v7 with `COMMITMENTS.md` and
  `budget_stdout_v7.txt`. The figures to approve stay 4,609 CPU-h / 5,992 / 60 days (rider 4,616 / 6,001 optional).
