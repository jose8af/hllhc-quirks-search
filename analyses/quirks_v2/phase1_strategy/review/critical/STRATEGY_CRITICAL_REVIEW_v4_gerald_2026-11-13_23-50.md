# Critical review, STRATEGY v4 (quirks v2, Phase 1), review cycle 4

Reviewer: Gerald (critical, fresh to the panel), 2026-11-13 23:50. Role and template: `agents/critical_reviewer.md`
(adversarial stance; evidence for every "verified"; A/B/C). Rules: `AGENT_RULES.md` (light stdlib arithmetic on
einstein only; no sub-agents; no git).

**Artifact.** `phase1_strategy/outputs/STRATEGY_fiona_2026-11-13_23-05.md` ("v4", 2,842 lines, read in full),
`COMMITMENTS.md` ("COM", read in full), `phase1_strategy/src/strategy_budget.py` (run, output read in full).
**Context read.** Cycle-3 verdict `STRATEGY_ARBITER_v3_felix_2026-11-13_22-40.md` (in full; it defines "fixed" for
P1–P16), `FIX_REPORT_cycle3_fiona.md` (in full; claims treated as claims), `diff` v3 → v4 (1,276 changed lines,
every hunk mapped), brief `prompt.md` §3 D1–D10, §7 l.338–348 and the Phase-2 list l.260–272, phase `CLAUDE.md`
self-check, `conventions/search.md` tables. v1 JSON under `TT/data/acts_stage4/analysis/` read for spot checks.

**Cycle-4 discipline.** As the verdict (§9) asks, a new finding is raised only if it is a regression introduced by
the fix, a factual error in a number shown to the user, or a genuine A. Everything else is C.

**Verdict of this review.** P1–P16: **14 RESOLVED, 2 PARTIALLY RESOLVED (P2, P10), 0 NOT RESOLVED.**
New findings: **0 A, 2 B (G-B3, G-B4, both regressions introduced by the cycle-3 fixes), 15 C.** Open A/B items at
the end of this review: **4 B** (P2 residual = G-B1, P10 residual = G-B2, G-B3, G-B4). All four are text or a
script line; none needs a redesign or more than ≈ 36 CPU-h.

---

## 1. Verification of P1–P16 against the verdict's definition of "fixed"

| # | status | where in v4 (quoted phrase) | my check |
|---|---|---|---|
| **P1 (A)** | **RESOLVED** | Table 4.4a rows "Z(ττ) [E: 0.17 × 0.1 × N_Z(νν); range 10⁵–1.3×10⁶] \| 4.3×10⁵ \| 45 \| 1.43×10⁶ \| 0.30 \| 0.34 (0.16–0.61)" and "lost-lepton Z(ℓℓ) … 0.09 (0.05–0.17)"; §4.7 point 3 "The fourteen are v1's twelve and the additions"; §4.17 rows 18a/18b "`prod.hs0.ztt`", "`prod.hs0.zll`"; §11.7 rule 1 "recomputed **for every term of the likelihood**"; rule 6 "Pool shares of the additions" | Script [9] l.245–258 prints both terms inside the 665 CPU-h pool, the low/planning/high re-splits (12.16 / 12.59 / 13.25) and the keep-11.7 option (691 / 715 / 753 CPU-h). My arithmetic: 0.17 × 0.1 × 2.5079×10⁷ = 4.26×10⁵, 0.34 × 3.5×10⁻³ × 2.5079×10⁷ = 2.98×10⁴ (match). Multijet planning floor 0.46 (0.05–4.56) in the headline sum 13.0 (12.2–17.8) (script l.257–258). "not in the table": 0 hits in v4. Q3 annex row "floors 0.34, 0.09, 0.46". Every element of verdict §5 points 1–4 is present. |
| **P2** | **PARTIALLY** | §0 "reach **≈ 710 GeV at the 84 % edge if every no-pile-up ceiling counts zero** (median ≈ 790, an upper edge, not the expectation); **≈ 470–500 GeV if decays in flight …**"; Table 4.4c rows (α1), (α2), (β), (γ); "**The day-15 pause** … is a realistic branch"; caveats (PV placement, attribution rule, 45 ms, ×1/0.87, best-Λ mapping) | Scenarios α1/α2 with and without credit, β, γ printed by [9b] l.277–305; relabelled m_H rows; "m_H = 100 (≈ 230 events)" (script: 228); caveats, abstract rule, EST tag inside Q2, N-C7 sentence all present. **What remains (G-B1, §4):** the verdict asked §0/Q2 to "give the conservative 84 % edges and the medians across the rows". The (α) number in §0 and Q2 is the **median only** (470–500; its 84 % edge 421–455, script l.305, is in neither §0 nor Q2), while the empty-ceiling number next to it is the 84 % edge. β in §0 is quoted at its most favourable row only (m_H = 10). |
| **P3** | **RESOLVED** (definition) | §4.4 point 4 table "CKF removal … **no** … **default Df-9, option (a):** H is classified on **all own hits**"; "*S_CKF (Df-9).*"; "for the cuts that are monotone under added hits"; Df-9 row | Table of every fixed cut with monotonicity present; S_CKF credited only where tested, s_tot beyond, censored at 1; option (b) stated; m_H EST under (a) = 10–90 / 20–180 / 100–890 for ε_pair 0.8 / 0.9 / 0.98 (script l.316–319). **But** the sample on which S_CKF is tested makes it untestable for every B1 term (new G-B3). |
| **P4** | **RESOLVED** | §4.4 point 4 "**Ceiling test (one-sided), only on unbiased samples.**"; "it is an **implementation check**"; "*Weighted samples*"; §4.4 Scope "They have no ceiling test"; §4.17 row 13a `dev.ovl.dif` | (i)–(v) all present. Effective-count form checked: for equal weights N_eff = N and T_eff = T/w (stated, correct). Substitution re-computed: 8 counts in 4,000 vs 500 / 2,000 counts in 10⁶ give p = 0.00115 / 0.547 (v4: 0.0011 / 0.55). +7.0 and +6.0 CPU-h in script [3] l.37, l.44. (C: the "costed alternative" for sub-topologies has no CPU-h.) |
| **P5** | **RESOLVED** as specified | §4.4 point 4 "(ii) The *mixed excess*: … **paired pile-up-only finder pass** … 26 CPU-h"; §4.0 point 6 "extended ceiling H′ = P_geo + Σ_{all k} f_k"; §11.7 inputs "the completeness fractions with the expected mixed excess" | 26 CPU-h = 2 × 4,000 × 11.7 s (script l.59–60). 0.26 kept as convention; H′ default as ruled. **But** eleven of fifteen SM processes get no paired pass and borrow the excess of another process (new G-B4). |
| **P6** | **RESOLVED** | §4.0 point 4 "one combined verdict per term for the **T_c = 19 terms**"; table row "**either family removes a selection** \| **6.9 %** \| **7.0 %** \| **8.9 %**"; §4.4 "**One verdict per term**"; §4.12 rule 1; Df-2; §8 | Šidák per term, Bonferroni over 19 (1 + 3 + 14 + 1 = 19, list in script l.390). My arithmetic: 1 − (1 − 0.05/19·(1 + 4·0.05/19))¹⁹ = 0.0493; 1 − 0.979 × 0.9507 = 0.069; 1 − 0.958 × 0.9507 = 0.089 (match). Sub-topology tests dropped. |
| **P7** | **RESOLVED** | §4.0 point 7 "are **consistency checks with no distance credit** (Df-2)"; "the width step from the last crossing rung to R08 always counts in d"; table row "occupancy model, 2S crossing test PASS … 0.43 \| 0.59 \| 1.29 \| 1.30 \| 2.47 \| 3.68" | Script [12] l.449 identical. The withdrawn 0.45–0.49 appears only in §13.3. §4.5 "1.30 at R14 with a 2S crossing PASS"; §4.12 "usable to about R09 whatever its crossing comparisons give". |
| **P8** | **RESOLVED** | §4.0 point 7 "**promotion π_k tested at R06 only** (expected …) … 1.41 \| 1.41 \| 1.41 \| 2.51"; "1.42" with 2S PASS; R06–R07 row kept as "(conditional: DIF at an enrichment of 4 or more)" | √(0.231² + 0.693²·2²) = 1.405; √(1.41² + 0.693²·3²) = 2.51 (script l.453). All four remaining "0.73" hits are the conditional row or its reading (l.473–474, l.1766). |
| **P9** | **RESOLVED** | §4.11 point 3 "**every leading term labelled estimate**"; "(so a background of "low count" terms, m = 1–3, with σ_ln = 0.26 and f₀ = 0, is not "target met")"; COM TG-1 "every leading term is labelled estimate"; §0 "every leading term labelled estimate" | Same in three places; s_tot printed with each label (l.1566–1567). |
| **P10** | **PARTIALLY** | §12.1 Q3 "**brief D4 exception, completed.** For every MUST closure criterion that ends NOT TESTED, NOT EVALUABLE or not submitted (by planned statistics, by a fluctuation, by the cap rule or by a day-15 rule)"; annex rows "route 1: fluctuation … **0.30**", "route 2: the cap", "route 3", "route 4: B2-c"; "Rule 3 may already have spent the reserve" | The four routes the verdict named are present; P(Poisson(31) ≥ 24) = 0.9156, 1 − 0.9156⁴ = 0.297 (mine; script l.413). **What remains (G-B2):** the annex, which §4.0 point 6 itself says lists "every route … with its probability", misses two not-submitted/not-tested routes created by the same fix cycle (promotion model with fewer than two qualifying classes, P15; S_CKF untestable for B1, P3/G-B3), and the B4-e route has no default size although it is ≈ 4.6×10³ events at the planning N_MJ. |
| **P11** | **RESOLVED** | §4.11 point 6 "**Coverage family (T1-c (iii) and T1-h; default Df-10).** … FAIL below k_F … (462 of 500 at c_ref = 0.95, 459 at 0.945)"; Df-10; COM T1-c/T1-h | My binomial: P(X < 462 \| 500, 0.95) = 0.0046; P(X < 459 \| 500, 0.945) = 0.0048; one-check 5 % points 467 and 464, so INVESTIGATE 462–466 / 459–463 (match); family-wise 4.8 % / 5.0 % (script 4.7 / 4.9 %). Pooled alternative stated. 500 per (point, λ) stated. |
| **P12** | **RESOLVED** | Q5 "Their content depends on the MET model, the trigger threshold and the generator-cut decision, all frozen by day 12 before the propagation, but on no plane-selection choice and on no signal efficiency at any T2 candidate"; same in §4.17 | "No" → "+47 CPU-h (a second Stage 2), and the 47 + 266 CPU-h move onto the critical path after the freeze: +1.8 days": 312/174 = 1.79 (script [6] l.171). |
| **P13** | **RESOLVED** | §11.2 "**day-15 redirection reserve** (… spent by default, so inside the approved figure) \| 156"; "**Approved figure** … **5,087 full / 4,574 reduced**"; §11.6 "4,574 CPU-h (4,417 + the 156 CPU-h day-15 reserve …)"; Q4 "Approve **4,574 CPU-h**"; COM ST-1 | 4,417.1 + 156.5 = 4,573.6; 1.3 × 4,573.6 = 5,945.7 → 5,946 (script l.122, mine). §11.2 "None of these is inside the approved figure" now refers only to the conditional-cost table. Threshold is 1.3 × the figure put to the user in all three variants (5,382 / 5,946 / 6,613). |
| **P14** | **RESOLVED** | §4.7 "**the 4a hit-level campaigns are staged**"; §4.4 point 5 "*Reading of the pilot (fixed now).* … Gamma(m + 1) of the pilot count m"; §11.7 rule 1 "computed **preliminarily at day 7** … B₅₀ is read at the best candidate: the candidate with the lowest G"; rule 4; INV-1 row 20 "**Staged** (P14)" | (i) v1-proxy rates at day 15 and staging; (ii) pilot reading and branch from R06–R07 pilot counts; "best candidate" defined; day-7 preliminary rule; mixed-excess date. (C: staging rule does not say on which parity half the R06 rate is measured.) |
| **P15** | **RESOLVED** | §4.4 point 4 "*Per-k comparison (Phase 3, rule fixed now):* on the **pilot's 1,000 near-pass overlays (sample 11)** … 2–4 classes are expected to qualify. If fewer than two qualify, the promotion model is "not submitted""; §8 item (2) "for each term with a ceiling: … S_CKF … the combined ceiling test … c_mix … H′"; COM PR-1 | Expected-class arithmetic checked: 24/250 = 0.096, 24/125 = 0.19 ("0.10–0.19"). The "not submitted" consequence is not in the Q3 annex (part of G-B2). |
| **P16** | **RESOLVED** | §11.3 "**Agent slots (finding P16; executors + reviewers + drafter, at most three at a time).**"; "the one Phase-3 1-bot review of `SELECTION.md`"; "`PREREG_v2.md` drafter (channel (iii)'s second task)"; "the sealed C1 comparison (a separate short session, run sequentially in this slot)" | Three slots in every window; S-1 adopted (B5 and the B6 signal arm in days 36–48; COM B5-a…c deadline 4b). Calendar 57.6 d = 43.5 + 2,453/174 (mine: 57.598). (C: the BibTeX and rendering validators of the 4a/4b/5 panels have no slot.) |

**Counts:** 14 RESOLVED, 2 PARTIALLY RESOLVED, 0 NOT RESOLVED.

---

## 2. Scope control: changes not required by the verdict

All 1,276 changed lines of the v3 → v4 diff were mapped to P1–P16, the adopted C items, S-1/S-3 or the length cuts.
Changes that the verdict did not literally prescribe:

| # | change | source | judgment |
|---|---|---|---|
| S-a | Explicit 1.5-day closure/note buffer before the 4a review (script [7] l.184) | Verdict §7, S-1: "provides the buffer of N-C12" | **Justified.** S-1 removes 277 CPU-h = 1.6 production days from the window; the buffer re-spends them. Net calendar effect of S-1 + buffer ≈ 0. |
| S-b | Reserve counted on the critical path (+0.9 d) | Logical consequence of P13 ("spent by default") and rule 3 (both branches spend it in 4a production) | **Justified**, script [5′] l.149 (156.5/174 = 0.90 d). |
| S-c | Multijet planning N_MJ = 1 % of N_trig (0.1–10 %) | Fixer's own bracket [E] | **Harmless, labelled, planning-only**, and replaced at day 12 by rule 6 / the MET model. Not "unsourced": v1's `bsum_wp.json` → `n_trig.not_included` says "QCD multijet fake MET … UNVERIFIED <~1-2 % each" (read this session) — cite it (C-6). Gap: the 10⁶-event loose population has no re-sizing rule if N_MJ comes out near 10 % (floor 4.6) (C-7). |
| S-d | r_ττ = B(Z→ττ)/B(Z→νν) = 0.17 [U] | Verdict §5 point 1 (planning value of N-A1) | **Harmless.** Planning-only, tagged [U], and the real N_trig comes from the generator (Pythia BRs) and the MET model at day 12 (rule 6). The sister constant 0.34 (B(Z→ℓℓ)/B(Z→νν)) in the same sentence is **untagged** (C-5). |
| S-e | (α) reach 470–500 instead of the verdict's "≈ 500–650" | Script [9b] l.299–305 | **Justified by the script, which the verdict told the fixer to use.** But FR §4 item 1 says "Both readings are stated in §4.4"; the factor-e reading (reach < 393 GeV) is **not** in v4 (`393` occurs only in the α2 rows). And the factor-e size uncertainty the fixer quotes (l.925) is not carried into the reach: my √B estimate with the same count width gives a median reach of roughly 400–570 GeV for B₅₀ × e^(±1) [ESTIMATE, mine, not printed by the script]. Part of G-B1. |
| S-f | Fluctuation route 0.30 instead of 0.28 | Exact Poisson, script l.413 | **Justified** (mine: 0.297). |
| S-g | SM floor 15.7 (summed pool floor 20.8) at 90 ms, instead of "about 11" | Script l.259 | **Justified.** Analytic check: with pool shares ∝ √(N c) the summed floor scales as (A + √2·B)²/(A + B)² with A = 3.9, B = 8.6 → 20.6, SM part 15.6 (match to rounding). |
| S-h | Approved figure 4,574 / threshold 5,946 instead of "≈ 4,573 / ≈ 5,945" | Script [4] l.122 | **Justified** (rounding of 4,573.6). |
| S-i | R08-like comparison row 527 → 496 GeV | Ph-C9 (adopted C item): pile-up cap drawn as 426 × Exp(1) | **Justified**; script l.287 "496 [435, 566]". R09 rows moved by ≤ 4 GeV (830/790/761/720/657/576 against v3 834/793/761/723/661/575). |
| S-j | Script numerics in log space (Poisson windows, lgamma) | FR §4 item 8 | **Harmless.** I reproduced every printed value; the v3 → v4 row shifts are of the size the P1/Ph-C9 inputs explain. |
| S-k | "Best candidate" = lowest G with v1 placeholders and projected background | N-C6 wording | **Harmless**; the verdict's "B₅₀ × (1/G)" is not a well-defined ordering anyway. |
| S-l | **P5 sample choice: eleven SM processes borrow the mixed-excess fraction of "the supplied process closest in topology", labelled EST** (§4.4 point 4) | Fixer's choice (FR §4 item 10) | **Problem: an untested credit that enters a result** → G-B4. |
| S-m | **S_CKF tested only on "the unbiased B1 overlays"** (the verdict said "overlays and hit-level halves, R04–R06") | Fixer's narrowing, apparently by carrying P4's "unbiased only" from the ceiling test to S_CKF | **Problem** → G-B3. |
| S-n | Ceiling verdict per term with Šidák over rungs | Verdict §9 allows "any family-wise-5 % rule" | Justified. |

**Guessed or unverified inputs: are they planning-only, labelled and tied to a replacement rule?**

| input | label | planning only? | replacement rule |
|---|---|---|---|
| N_trig of Z(ττ), Z(ℓℓ), multijets (0.17, f_MET = 0.1, 0.34, f_lost, 1 %) | [E]/[U] (0.34 untagged) | yes (pool shares, floors, headline) | MET model at day 12; re-allocation rule 6 before any pool event |
| 45 ms per no-PU hard-scatter event | G | yes | day-0/day-5 timing job; checkpoint 1 |
| ε_pair = 0.8–0.98 (m_H EST under Df-9) | "assumed …, not measured" | yes (Table 4.4c rows) | pilot H at day 5–7, S_CKF test (see G-B3) |
| (α) v1 counts and fall factors | [E from v1 numbers] | yes (headline scenario) | pilot R06–R07 counts, rule 1 at day 7/15 |
| v1-proxy R06 rates for staging | "labelled with their errors" | yes (sample sizing) | first-half measurement (staging) |
| **borrowed mixed-excess fraction for eleven processes** | EST | **no: c_mix multiplies the term in the result** | **none** → G-B4 |

Only the last one fails the test "planning only, labelled, replaced before it enters a result".

---

## 3. Numbers

### 3.1 Script rerun
`python3 -I phase1_strategy/src/strategy_budget.py`: exit 0, 503 lines. Every figure below matches v4 and COM:

| quantity | script | v4 / COM |
|---|---|---|
| MUST / reduced / full | 3,983.6 / 4,417.1 / 4,930.4 (l.99, l.121–123) | 3,984 / 4,417 / 4,930 (§11.2); "≈ 3,980 / 4,420 / 4,930" (§0) |
| approved figure, reduced + reserve | 4,573.6 (l.122) | 4,574 (§11.2, §11.6, Q4, COM ST-1); "≈ 4,570" in §0 (C-1) |
| stop-and-ask thresholds | 5,382 / 5,946 / 6,613 (l.121–123) | identical in §11.2 table, §11.6, Q4, COM ST-1, §0 |
| envelope alternative | 6,720, threshold 8,736 (l.158) | Q4 identical |
| contingency; M / D / G | 2,146; 717 / 2,322 / 1,378 (l.153–156) | §11.2, Q4 identical |
| all guesses doubled | 5,952 against 5,946 (l.159) | §11.2, Q4 identical; §11.6 "about 5,950" |
| phase totals | 506 / 580 / 2,701 / 118 / 68 / 10 (l.93–98) | §11.2 "506 / 580 / 2,701 / 196" (196 = 118 + 68 + 10) |
| item totals B1, B4, S1, T1 | 542, 1,150, 834, 263 (l.106–110) | §4.4, §4.7, §4.13, §4.11 identical; I re-summed B1 (541.5) and B4 (1,150.5) from their text components |
| calendar | 57.6 / 56.7 / 57.9; 48.7; 64.6 at 0.50 (l.195–198) | §0 "58 days; 49 …; 65"; §11.2 table identical; Q4 "57 days" MUST only (56.7) and "58 days" full (57.9) — rounding |
| non-production days | 43.5 (l.193) | §0, §11.3, §11.6 identical |
| critical-path production | 2,453 CPU-h = 14.1 d (l.196) | §11.2, §11.3 identical |
| storage | 417 / 617 GB (l.214) | "≈ 420 (≈ 620 at the pre-merge cap)" |
| summed floor | 12.59 pool + 0.46 = 13.0; 12.2 / 17.8; median 10.8, 7.7–15.2, σ_ln 0.34 (l.258, l.263) | §0, Table 4.4a, §4.4 readings identical |
| false-loss rate | 6.9–8.9 % (l.394–397) | §4.0 table and point 6, §4.12 rule 1, Df-2 (4 places) |
| T1 coverage | 462 / 459 of 500; family 4.7 / 4.9 % (l.479–480) | §4.11 point 6 identical; Df-10 "4.7 %"; COM T1-h "≈ 5 %" (C-2) |
| pilot one count | 10.9 events (l.261) | §4.4 point 5 identical |

My own arithmetic (stdlib, scratchpad) agrees: 1.3 × 4,573.6 = 5,945.7; 43.5 + 2,453/174 = 57.60; 43.5 + 2,297/174 =
56.70; 43.5 + 2,507/174 = 57.91; N_t(NI 22) = 4.0848×10⁷ × 0.09823 × 0.22 = 8.83×10⁵; N_t(DIF) = 6.51×10⁷;
P(Poisson(58) ≥ 55) = 0.671 (v4 0.67); P(Poisson(70) ≥ 55) = 0.972 (COM B2-d 0.97).

### 3.2 Stale-value grep (v4 and COM)
Searched for 2,950; 3,275; 3,798; 3,968; 4,401; 4,915; 5,722; 3,945; 4,378; 4,891; 5,691; 56.6; 11.7; 790; 0.73;
2,135; 4,534; 5,894; 5,945; 4,573; 0.28; 500–650; 527; "2–4 %"; 465; 0.45–0.49; "≈ 720"; "42 days".
- **COM: zero hits** for every value (the one "11.7" hit is "§11.7").
- **v4:** every hit is (i) a historical comparison (§11.2 "Version 3 had 3,945 / 4,378 / 4,891 … 5,691", §13.1
  "2,950 → 3,968", §13.3 rows), (ii) an unrelated quantity (11.7 s finder trial, "§11.7", 790 = v1's μ₉₅ and the
  empty-ceiling median, explicitly "an upper edge"; 0.28 = NI floors and R1 ε_fid; 0.73 = the conditional π_k row),
  or (iii) "the version-3 summed floor of 11.7" as the comparison it is. **No stale current value.** 790 is not the
  leading figure anywhere (§0 and Q2 lead with 710 at the 84 % edge).

### 3.3 Spot checks of VERIFIED numbers (20; new-in-v4 first)
| # | claim in v4 | source opened | result |
|---|---|---|---|
| 1 | NI rates 0.098 / 0.124 / 0.124 × 0.22 (§4.4 point 6, new) | `AN1/background.json` → `cprime.ni22/ni30/ni61.rate.value` = 0.098230 / 0.124079 / 0.124079, `.rate.pv_line_factor` = 0.22 | match (the key is under `.rate`, v4 writes `.pv_line_factor`; trivial) |
| 2 | `S4/analysis/wp.py` l.40 `P_PV_LINE = 0.22` (new) | l.40 "P_PV_LINE = 0.22 # WP_RULE §4.1 l.318-320" | match |
| 3 | `book/checks/ch29_checks.py` l.25-47 CLs at fixed B, l.54-58 best Λ per mass (new, N-C4) | l.25–30 `cls_value`, l.45–47 brentq on CLs; l.54–58 `yields` = max over LAMBDAS | match |
| 4 | DIF 166/81/2/1, γ 153/86/13/2, V⁰ 859/358/6/0, NI 127/46, 173/60, 553/189 per 500 (Table 4.4b) | `cprime.<t>.rows[].factors`: R04/R05 attributed N with M = 500; R06/R07 as conditionals 2/81, 1/81 (DIF), 13/500, 2/13 (γ) | match |
| 5 | v1 Z(νν) generator rates γ 0.231, V⁰ 0.026 (§2 route check) | `cprime.gamma.rate.per_process.Znunu_j` 0.2306, `cprime.v0…` 0.02605 | match |
| 6 | DIF rate 1.569–1.594 per process (§2) | `cprime.dif.rate.per_process` 1.5687 (WZ) … 1.5945 (tt̄ 2ℓ) | match (min is WZ 1.5687, not Z(νν) 1.5691 — script l.502 says "(Z nunu)"; trivial) |
| 7 | v1 R06 counts Z(νν) 32.3/2,000, W(τ_h) 8.96/1,625, W(τ_ℓ) 3.04/375, tt̄ 1ℓ 5.19/2,000 (§4.7) | `sm.<p>.rows` R06 factor N/M and `n_class_events` | match |
| 8 | N_trig 4.0848×10⁷ ± 2.0 %, Z(νν) 2.508×10⁷ | `bsum_wp.json` → `n_trig.value` 40,848,448, `rel_stat` 0.0202, `breakdown.Znunu_j.N_trig` 25,078,825 | match |
| 9 | v1 best B₈₄ 1.2346×10⁶ | `STAGE4_SUMMARY.json` → `ladder.SR-G.min_B84` 1,234,586 | match |
| 10 | μ₉₅ = 1.2458×10⁷/15,775 = 789.7 | `limits.json` → `points["A2|F|200|1.5|BM"].expected_toys.median` 12,458,208 | match |
| 11 | proxy share 0.147 (R04), 0.445 (R09) | `SUM` → `sm_proxy_fraction_of_B_SM` 0.14716, `R09_p>1e-3` 0.44523 | match (R09 is in SUM too, not only in D4) |
| 12 | `AN1/acceptance.json` → `finder_note` | key present: "A2 finder eps = matched & rung & f_CKF < 0.2 over every TEMPLATE-half …" | match |
| 13 | frozen T_seed 4, road 0.15 (`frozen_inputs.json` l.17, l.37–38) | l.17 `"t_seed": 4`, l.37 `"road": 0.15`, l.38 `"tseed": 4` | match |
| 14 | PLAN l.115–116 bounds ≲ 180 GeV; l.121 reach row | l.115–116 caption "below about 180 GeV"; l.121 "1026 & 971 & 866 & 799 & 717 & 548 & 393" | match |
| 15 | MG5 Z(νν)+jet 12.21 ± 0.03 pb vs 14.6, ratio 0.84 | `benchmarks_generators.json` → `xsec.ZNN_J_met200` 12.21 / 0.0277 / 14.6 / 0.836 | match |
| 16 | shower 21 / 23.4 ms, QED-FSR 21.1 ms | `derived.py8_shower_ms_per_event` 21.2 / 23.4 / 21.1 | match |
| 17 | pyhf 0.12 / 0.52 / 10.4 / 652 s | `benchmarks_runner.json` → `pyhf…mle_fit.cpu_s` 0.116, `asymptotic_cls_mu1` 0.517, `ul_scan_20pt` 10.436, `toys_1000_mu1` 651.8 | match |
| 18 | Argo / SSH overhead 16.8 / 2.4 s | `cpu60q.argo.overhead_per_job_s` 16.8, `cpu60q.ssh…` 2.4 | match |
| 19 | Geant4 primary-mode gun 0.134 ms | `benchmarks.g4_primary_20k.single.cpu_s.mean` 2.86 s / 20k = 0.143 ms incl. start-up; `derived.g4_cpu_h_per_1e6_vertex_events.primary_mode` 0.71 → 2.56 ms per vertex event = 0.134 ms / 0.053 | consistent |
| 20 | v1 places pile-up vertices at the PV (`s4cp.py` l.110–113) | l.110–113 are a docstring and beam-spot σ; the placement is l.115 `pv = vtx[:3] + rng.normal(…)` | supports the claim, line range off by two (C-14; pre-existing) |

Also found while spot-checking (pre-existing, C-13): v1's `sm.WW.proxy_of` and `sm.WZ.proxy_of` are **Wtau_l**, but
the Q3 annex and script l.430–431 cost WW and WZ compliance "if W(τ_h)-like" (+65 each); with v1's own proxy it is
+40 each, so the annex sum is ≈ 632, not 682 CPU-h.

---

## 4. Open B items

### G-B1 (P2 residual; number shown to the user) — B
**Where.** §0 l.59–64 and Q2 l.2680–2682.
**What.** The headline quotes two scenarios on **different bases**: "≈ 710 GeV at the 84 % edge" (empty ceilings)
and "≈ 470–500 GeV" for (α), which is the **median** (script l.305: "median reach 469-504 GeV, 84 % edge 421-455").
v4's own quoting rule ("The abstract heads with the 84 % edge", §0; §4.11 point 3) and the verdict's definition
("give the conservative 84 % edges and the medians across the rows") require the α 84 % edge next to it. In §0 the
(β) scenario is quoted only at m_H = 10 ("≈ 770 GeV (84 % edge ≈ 705) … count 10 events"), although Table 4.4c gives
767 / 749 / 695 [706 / 684 / 641] for m_H = 10 / 30 / 100 and §4.4 point 4 gives the strategy's own EST under its
default Df-9 as m_H = 10–890. And the factor-e uncertainty of the v1-based α size, stated in §4.4 (l.925), is not
propagated: at B₅₀ × e^(±1) the median reach spans roughly 400–570 GeV (my √B estimate with the same count width;
fixed-B values from the script's own `s95_fixed`: 661 GeV at B = 216, 483 GeV at B = 2,650). FR §4 item 1's claim that
"both readings are stated in §4.4" is not borne out (no "< 393" for the factor-e reading in v4).
**Why B.** The user decides Q2 on this paragraph; each omission leans favourable (the pattern verdict §8 names).
**Fix (text + one print line in [9b]).** §0 and Q2: "≈ 470–500 GeV (84 % edge ≈ 420–455)"; β as "≈ 770–695 GeV
(84 % edge 705–640) for m_H = 10–100"; one clause "the v1-based size of (α) is uncertain by a factor e, which moves
the reach by about ±80 GeV" with the number printed by the script.

### G-B2 (P10 residual; Q3 annex incomplete) — B
**Where.** §12.1 annex to Q3 (l.2730–2747), against §4.0 point 6 ("every route by which a MUST criterion ends so is
listed in Q3 (§12.1) with its probability").
**What is missing.**
1. **Promotion model "not submitted" because fewer than two classes reach 24 promoted events** (§4.4 point 4,
   introduced by the P15 fix). The promotion model is shared by every B1 and B4 term, so this route sends **every**
   credited term (Z(νν) included) to H; scenario (β) of Table 4.4c ("Z(νν) tested and credited") is conditional on it.
   "2–4 classes are expected to qualify" [E] gives no probability for "fewer than two".
2. **S_CKF untestable for the four B1 terms** (G-B3): a route "by planned statistics".
3. **B4-e default without a size.** Route 3 says "for B4-e the passing events only, floor stated", but the floor is
   not stated: by §4.7 (l.1275) it is N_MJ × 1.14/100 ≈ **4.6×10³ events** at the planning N_MJ (460–46,000 over the
   0.1–10 % bracket), which by itself triggers the day-15 pause (B₅₀ > 300).
**Why B.** D4 is put to the user, but the question's annex — the stated cost and default per route — is missing for
three routes; one of them (1) can change the whole projection.
**Fix (text).** Three annex rows with EST probability, consequence (size at H or floor) and compliance cost; one
sentence in Table 4.4c's (β) row "conditional on the promotion model being submitted".

### G-B3 (new; regression from the P3 fix) — B
**Where.** §4.4 point 4, "*S_CKF (Df-9).* … credited only where it is tested (attributed candidates on the
**unbiased** B1 overlays and on the hit-level halves, derivation R04–R05, test R06)".
**What.** The verdict's P3 fix said "overlays and hit-level halves, R04–R06". Restricting the B1 test to the unbiased
overlays makes it untestable by design: the 1,000 unbiased DIF overlays hold **4** expected attributed counts at R06
(Table 4.4b), the NI overlays 0–2, against ≥ 19–24 needed for F = 2 (§4.0 point 3). NI is moreover tested at R05 by
the rung split, which the S_CKF rung choice ignores. So S_CKF is expected NOT TESTED for DIF and all three NI radii,
and those terms carry H on all own hits **before** CKF — larger by 1/(1 − ε_pair) (×5–50 in the Z(νν) EST of the same
paragraph) — exactly where (α) says DIF may be counted. The restriction "unbiased only" is needed for the ceiling and
leak tests (P4), not for a survival factor, which the enriched overlays (known weights, 31 expected at R06) test
like S and π_k.
**Fix (0 CPU-h).** Test S_CKF for DIF on the enriched test overlays with their weights (R06, R07 where evaluable) and
for NI by the rung split (derive R04, test R05); COM B1-f and Df-9 accordingly. Then route 2 of G-B2 disappears.

### G-B4 (new; regression from the P5 fix choice) — B
**Where.** §4.4 point 4 (ii): "The eleven other SM processes take the excess fraction of the supplied process closest
in topology (same hard-scatter estimator), labelled EST."
**What.** The paired pile-up-only pass runs only on the four supplied B4 processes and the B1 overlays. For eleven of
the fifteen SM terms the mixed excess, and therefore the completeness verdict and c_mix (which multiplies the term
"always", l.774–775), comes from another process. That is a credit without a test: by v4's own §4.0 point 6 the
no-credit value of a term without a completeness PASS is the extended ceiling H′. Nothing replaces the borrowed value
before it enters the likelihood (§2 table above).
**Why B.** It weakens a MUST criterion (B1-f/B4-c completeness) and contradicts the single eligibility statement the
verdict asked for; it is new in v4.
**Fix.** Either run the paired pass on the 1,000 test-half events of each of the eleven processes (11,000 × 11.7 s ≈
36 CPU-h, re-analysis; script [3] and the approved figure updated, threshold × 1.3), or state that those terms enter
at H′ (no credit), and add the route to the Q3 annex.

---

## 5. Consistency and completeness of v4 as the executed document

### 5.1 Contradictions between sections (both locations)
| # | quantity | location 1 | location 2 | class |
|---|---|---|---|---|
| 1 | approved figure | §0 l.79 "≈ 4,570 CPU-h, the approved figure"; "5,090 with the reserve" | §11.2, Q4, COM: 4,574; 5,087 | C-1 |
| 2 | T1 coverage family-wise size | §4.11 point 6 "4.7–4.9 %" | Df-10 "family-wise 4.7 %"; COM T1-h "≈ 5 %" | C-2 |
| 3 | R-20 deadline (N-C8) | §6.4 "R-10 and R-20 before Phase 4a" | COM REF-2 "R-10 before Phase 4a" (R-20 absent) | C-3 |
| 4 | "four supplied" set | §4.7 l.1300 "The four supplied processes carry 86 % of N_trig" (Z(νν), W(τ_h), W(τ_ℓ), tt̄ 1ℓ) | same sentence "at least one of DIF, W(τ_h), W(τ_ℓ) and tt̄ 1ℓ" (four supplied *terms*) | C-4 |
| 5 | S1 chain vs S1-a deadline | §11.3: S1 chain runs during and after the 4a review (ends day 39.5–41.5) | COM S1-a deadline "4a" (pre-existing in v3) | C-11 |
| 6 | "additions raise N_trig by 1.1 %" | §4.4 l.865 ("the additions", after "All three") | script l.249: the two Z additions only; with multijets at 1 % it is 2.1 % | C-5 |
No contradiction found in the eligibility logic (stated once in §4.0 point 6 and referenced from §4.11, §4.12,
the partial-outcome table, COM T2-a), the stop rule, the thresholds, the false-loss rate, the widths or the floors.

### 5.2 Brief and methodology checks
- **MUST/SHOULD coverage.** Every plan item has method, pre-fixed criterion, statistics, CPU-h and phase in §4 and a
  COM row (C1-a…e, C2-a…c, C3, B1-a…g, B2-a…g, B3-a…d, B4-a…e, T1-a…i, T2-a…h, S1-a…f, S2-a…f, P1-a…d; SHOULD
  B5-a…c, B6-a…d, B7). Cost lines re-summed for B1, B4 (above).
- **S3** as fixed in D1: §4.16 "signal ×1.5–3.2; reach 866 → 1062 GeV at B = 10, g = 1" — identical to `prompt.md`
  l.66–68; COM S3 "dropped (user)". Df-6 offers only a wording alternative. ✓
- **D4.** Put to the user in Q3 with alternatives and cost ✓; annex incomplete (G-B2).
- **Stop conditions.** §11.6 quote compared line by line with `prompt.md` l.341–347 and l.79: identical. ✓
- **Blinding.** No new signal quantity in v4; rule 1 at day 7 uses v1 placeholders; BL-1 list unchanged except the
  §12.3 FYI line. ✓
- **Discarded items.** No ρ = 3, pile-up scan, ×100, Λ ≥ 15 keV, Open Data, cloud or endcap result. The doubled pool
  (×2) is an alternative, not ×100. ✓
- **Conventions.** §5.1 answers all 17 source rows of `conventions/search.md` (l.64–94) plus the PDF and pile-up
  replacements; §5.2 answers the six validation checks, with the K-C1 departure now stated. ✓
- **Phase-1 self-check** (`phase1_strategy/CLAUDE.md`): corpus substitute logged (§6.3, deviation V8); backgrounds
  classified (Table 2.1); ≥ 2 approaches with the MVA infeasibility as [DP3]; systematic enumeration; reference
  table R1–R4 with programmes; method parity (§6.1); [A]/[L]/[SD] labels (§7); flagship figures (§9). ✓
- **Agent cap.** Slot table respects three (C-12 for the validators).

---

## 6. Category C (apply without re-review)
- **C-1** §0: write 4,574 and 5,087 (not ≈ 4,570 / 5,090), as everywhere else.
- **C-2** Df-10 and COM T1-h: "4.7–4.9 %".
- **C-3** COM REF-2: add "R-20 before Phase 4a".
- **C-4** §4.7 l.1300: distinguish the four supplied *processes* (N_trig share) from the four sized *terms* (route 1).
- **C-5** Tag 0.34 = B(Z→ℓℓ)/B(Z→νν) [U] like 0.17; write "the two Z additions raise N_trig by 1.1 %".
- **C-6** Cite `bsum_wp.json` → `n_trig.not_included` ("<~1-2 % each", [U]) for the multijet bracket.
- **C-7** Multijet loose population: a re-sizing rule (or a stated "no") if the MET model gives N_MJ ≫ 1 %.
- **C-8** P4 (iii) "costed alternative" for the sub-topology test: give the CPU-h.
- **C-9** P14 staging: say that the first-half R06 rate is read on the derivation parity half (or on R05), so that
  the test half is not looked at before its prediction exists; note the small two-stage bias.
- **C-10** Table 4.4c rows "m_H = 1000" and (α2) "no credit" use a fixed-B limit (no count width), unlike every
  other row; mark them "upper edge of the reach" in the row, as the script does.
- **C-11** COM S1-a deadline "4a" while the S1 chain ends after the 4a review (pre-existing): move to 4b or state
  that only job completion is checked at 4a.
- **C-12** Slot table: the BibTeX validator (4a, 4b) and the rendering reviewer (5) run in freed slots like the
  arbiter; say so. No ITERATE allowance is planned for the Phase-3 1-bot review.
- **C-13** WW, WZ compliance in the Q3 annex: v1's `proxy_of` is W(τ_ℓ), giving +40 each (annex sum ≈ 632, not 682).
- **C-14** §2: the PV-placement citation is `s4cp.py` l.115 (`pv = vtx[:3] + …`), not l.110–113; and the DIF rate
  minimum is WZ (1.5687), not Z(νν) (script l.502).
- **C-15** P15: with 2–4 qualifying classes, the r.m.s. that becomes s_model is a 1–3 degree-of-freedom estimate;
  state its expected spread next to the cap 0.231 (or use the declared-larger option of §4.0 point 4 (c)).

---

## 7. Answer to the template's closing questions
- **Tautological validations introduced by the fix?** None new; the three of cycle 3 (P3, P4, P7) are removed.
- **Motivated reasoning.** The remaining slant is in the user-facing headline (G-B1) and in two untested credits
  created by the fixes (G-B3, G-B4); none is concealment, all facts are in the document.
- **"What would a competing group have that we don't?"** The same as in cycle 3: measured, not bounded, leading
  terms. v4 now tells the user in advance that the day-15 pause is realistic. Nothing new.

## 8. Summary
- P1–P16: **14 RESOLVED, 2 PARTIALLY (P2, P10), 0 NOT RESOLVED.** P1 (the only A) is resolved.
- New: **0 A, 2 B (G-B3, G-B4), 15 C.**
- **Open A/B items: none A; four B** — G-B1 (P2: α 84 % edge, β range and α size uncertainty missing from §0/Q2),
  G-B2 (P10: three Q3 annex routes/sizes missing), G-B3 (S_CKF untestable on the unbiased B1 overlays), G-B4
  (borrowed mixed excess for eleven SM processes). All are text or one script line, ≤ 36 CPU-h; a short focused fix
  and verification would suffice (verdict §9).
- Numbers: every CPU-h, threshold (1.3 × the approved 4,574 = 5,946), calendar (57.6 d), floor (13.0) and false-FAIL
  (6.9–8.9 %) figure reproduced; stale-value grep clean; 20 VERIFIED numbers spot-checked, all consistent.
