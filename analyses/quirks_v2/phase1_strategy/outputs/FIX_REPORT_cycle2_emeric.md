# Fix report, review cycle 2 — Phase 1 STRATEGY v3

Fixer: Emeric, 2026-11-13 21:10. Work list: `review/arbiter/STRATEGY_ARBITER_v2_eloise_2026-11-13_20-45.md` §6 (items 1–21).
Artifact: `outputs/STRATEGY_emeric_2026-11-13_21-10.md` ("v3", 2,674 lines; v2 had 2,391). v2 is unchanged on disk.
Also changed: `COMMITMENTS.md` ("COM"), `src/strategy_budget.py` ("script", rerun, exit 0, about 4 s),
`retrieval_log.md`, `experiment_log.md`, `logs/fixer_emeric_2026-11-13_21-10.md`.
"l." = line of v3. Tags: [V] read or re-derived by me this session, [E] estimate with arithmetic in the script, [U] transcribed.

## 1. Status counts

| group | RESOLVED | PARTIALLY | CANNOT | to Gate A |
|---|---|---|---|---|
| 7 partial cycle-1 findings (M4, M5, M11, M12, M15, M24, M26) | 6 | 0 | 0 | M24 accepted by the arbiter as a dated commitment (no text needed; date aligned) |
| N1–N4 (A) | 4 | 0 | 0 | N2 also has a Gate-A part (Q3) |
| N5–N18 (B) | 14 | 0 | 0 | N12 → Q4; N14 → Q5; N13 → Df-7 |
| C items (P 7, K 10, N 10) | 26 applied | 0 | 0 | 1 not adopted by the arbiter's own ruling (N C-11) |

Outcomes that only Phase-2/3 measurements can give are written as dated rules (§3 below); none is claimed as done.

## 2. Per finding

### Category A

**N1 — the ceiling H is never tested as a ceiling. RESOLVED** (v3 §4.4 points 3–4, l.648-712; §4.0 point 6, l.374-389; COM B1-f).
- (a) f_k is defined on subsets of the term's own hits by a width-only pass (l.656-663); with that definition P ≤ H holds for attributed candidates by construction, and the argument is written (l.667-671).
- (b) k per layer type, k = k_IP + k_2S with N_IT2 inside k_IP; width at counting rungs = the finder's maximum core width; at R12–R14 the R08 width (l.660-664).
- (c) One-sided ceiling test: exact conditional test for two Poisson counts; FAIL p < 0.001, INVESTIGATE p < 0.05 with one re-test; rungs and samples named (l.676-685). Substitution and limiting case in script [11].
- (d) Completeness test: leak fraction and mixed fraction by truth; bound 0.26 on the 95 % upper limit of (leak + mixed)/attributed at R04–R06; the bound is carried as c_mix so a pass cannot under-cover; rule for a non-pass before and after the freeze (l.686-697).
- (e) FAIL logic by direction: over-prediction with a valid ceiling → term at H, eligible; under-prediction → [SD8]; ceiling FAIL → not eligible (l.374-381; §4.12 rule 1, l.1531-1544).
- Dated: first on development samples, result fixed before the freeze; verdict on test samples (COM B1-f).
- Cost: 0 CPU-h (re-analysis). I did not add a paired pile-up-only finder pass (26 CPU-h); the mixed class is counted by truth as an upper value instead, and the text says so (l.695-697).

**N2 — MUST closures planned NOT TESTED; brief D4. RESOLVED, with the remainder at Gate A (Q3).**
- Supplied: W(τ_h), W(τ_ℓ), tt̄ 1ℓ hit-level samples sized for an expected 31 effective counts in the test half (24 needed; probability 0.92): 11,250, 7,662 and 23,880 events, +65, +40, +153 CPU-h (§4.7 l.1133-1146; script [3], [11]). NI at three radii: tested at R05 by a rung split, 92 / 120 / 378 expected counts on the 1,000 unbiased overlays, 0 CPU-h (§4.4 l.825-831). DIF: sized for R06, +19 CPU-h only if the enrichment is below 1.7 (l.818-824).
- Costed table for the others: annex to Q3 (l.2519-2531): eight proxied SM processes (≈ 680 CPU-h in all, 100–1,230) and the three additions.
- Dated decision rule: §11.7 rules 3 and 4 (l.2427-2452), with the arbiter's thresholds (≥ 10², 10–10², < 10) applied to whichever term's ceiling leads the projection after N8.
- Rung-split alternative of K: adopted as the default for NI, because it costs nothing.
- **Correction of a number in v2 and in the verdict** [V: `AN1/background.json` → `sm.<p>.n_class_events`, `rows`]: v1's R06 counts are 8.96 in 1,625 W(τ_h) events and 3.04 in 375 W(τ_ℓ) events, not per 2,000. At the bare threshold of 24 the costs are +47 (not +61) and +28 (not +210) CPU-h; tt̄ 1ℓ +116 is confirmed. With the margin: +65, +40, +153.

**N3 — "target met" earned by zero-count bounds. RESOLVED** (§4.11 point 3, l.1379-1403; §0 l.59-61; COM TG-1; Q2).
"Target met" needs σ_ln ≤ 1, f₀ ≤ 0.5 and no leading bound or no-credit term. One σ_ln (total); the other is the "count width w_m". The expected reading "target not met: sample-size limited" is stated in §0, §4.11 and Q2. The all-bounds case is quoted as the counter-example (σ_ln = 0.36, f₀ = 1).

**N4 — criterion (a) against (c); wrong rates shown to the user. RESOLVED** (§4.0 points 4–6, l.321-389; §4.12 rule 1; Df-2; script [11]).
- (c) cap s_model ≤ ln F/3; an estimator above the cap is not submitted (no credit), decided at day 15 (§11.7 rule 2).
- (a) INVESTIGATE band up to ln F + 2σ_tot with one fresh re-test; (b) unchanged thresholds; re-test passed if |ln r′| ≤ ln F and p′ ≥ 0.05/K. The re-test criterion is 0.05/K, not 0.05: the model bias δ is the same in a re-test, and with p′ > 0.05 an estimator at the cap would fail in about 5 % of the tests whatever the sample (computed: the v2 rule at the v3 cap gives 3.6 % per test, 36 % for twelve).
- K fixed now: 10 tests, listed.
- Rates recomputed with δ shared between test and re-test [V: script [11], numerical integration; two-rung case by Monte Carlo]: per test 0.52 % / 0.55 % / 1.07 % at s_model = 0 / cap/2 / cap (1.9 % with two rungs); battery of ten: at least one FAIL 5.1 % / 5.4 % / 10.2 % (11.8 % with two-rung pile-up tests); **a FAIL that removes a selection: 2.1 % / 2.2 % / 4.2 %**. Power: PASS with probability 98.7 / 90 / 62 / 26 / 5.9 / 0.07 % at |ln r_true| = 0.5 / 0.75 / 1 / 1.25 / 1.5 / 2 × ln F.
- The finding itself is reproduced in the script (0.043 / 0.093 and 0.048 / 0.098 per test; 0.41–0.71 over twelve).
- F is not loosened (1.5 and 2).

### Category B

**N5 (M4) — extrapolation widths. RESOLVED** (§4.0 point 7, l.391-448; §4.5; §4.6; §4.12; script [12]).
Rule applied as stated (σ_b := b₀ below three rungs; b̂ defined for one and two rungs); distance per quantity (only rungs that act on it); crossing test rungs per estimator with the same evaluable rule and verdicts; b₀ named a convention; planning table recomputed (occupancy model 0.43 / 0.59 / 1.29 / 2.47 / 3.67 / 4.88 at R08…R20 without crossing tests, 0.43–0.49 with). The reviewers' numbers (0.45 / 0.61 / 1.30 / 2.47 and 0.78 / 1.04 / 2.22 / 4.23) are reproduced in the script. Evaluability of the crossing tests: dated, Phase 3, written into the pre-registration. Storage 0.9 GB, 5 CPU-h.

**N6 — capping; T1 gaps. RESOLVED** (§4.0 l.444-448; §4.11 l.1319-1325, l.1374-1379, T1-c (v), T1-h l.1497).
Censoring φ = min(φ₀e^θ, 1) as a parameter bound in the fit and a censored draw in the generation; P ≤ H follows; pile-up estimate bounded at 485 events. μ grid (8 values around the asymptotic limit) and log-linear CLs interpolation. T1-h: λ = m + 1, m′ redrawn.

**N7 — headline without H and without the pile-up term. RESOLVED** (§0 l.40-61; Table 4.4c l.778-808; [L13]; Q2; §11.7 rule 1; script [9b]).
Projection = max(zero-count floor, N_t·H) + EST pile-up term. Reach per outcome at an R09-like selection: 834 GeV (floors only), 793 (with pile-up), 761 / 723 / 661 / 575 for m_H = 3 / 10 / 30 / 100, ≈ 495 for m_H = 1000. Bounded paper as the default deliverable; bracket for the abstract; change of the bound (3.7–4.7 decades); R07-direct ≈ 1.6×10⁵ events; pilot enlarged (+28.8 CPU-h).

**N8 — double counting. RESOLVED** (§2 l.158-178; §4.4 Table 4.4a l.743-757; §4.7; §4.17; script [9]).
One route per origin by truth; PV pairs, γ, V⁰, loopers are inside B4; B1 keeps DIF and NI. Disjointness argument and a Phase-2 route check with a fallback. Pool re-allocated with the full cost per event (Geant4 vertices inside the envelope, 600 + 65 = 665 CPU-h, the same CPU as v2): summed floor **45.3 → 11.7 events**. Every dependent number rerun.

**N9 (M26) — pile-up-vertex secondaries. RESOLVED** (§2 l.190-208; COM B1-g).
Premise corrected with the v1 sources [V: `normalise.py` l.84-110; `gen_d123.py` l.21-23; `s4cp.py` l.110-113]; both shares in rate_t; own-z placement of the pile-up share; single-counting rule; truth-attributed count at R04–R07 against the B1 prediction with a rule. The conditional "+160 CPU-h of secondaries in every overlay" is removed (it would have counted twice). Magnitude: dated, Phase 3.

**N10 — "estimate"; rule drawn to the first empty rung. RESOLVED** (§4.11 l.1386-1393; §4.12 rule 7 l.1565-1573; COM T2-h).
"Estimate" needs m ≥ 4 and PASS; new label "low count" for 1–3; precedence fixed; the estimate-only selection is reported beside the winner; abstract choice in Q2; monotone-prior sensitivity reported.

**N11 — π_k independence. RESOLVED** (§4.4 l.700-708). π_k from the correlated occupancy model; per-k comparison; its r.m.s. is the s_model and the cap rule decides. Dated, Phase 3.

**N12 — envelope. RESOLVED + Q4** (§11.2 l.2272-2286; §11.6; Q4). Conditional costs table: none inside the approved figure; each draw is a reported overrun and counts against the stop rule; the envelope alternative is offered.

**N13 (M11) — retrieval fallbacks. RESOLVED** (§4.9 l.1217-1221; §4.7 l.1098-1102; §6.4 l.1988-1995; Df-7). Default of the verdict's §7 applied; B4-b path if R-3 is empty; deadlines.

**N14 — D7 reading. GATE A (Q5)** (§4.17 l.1848-1853; §12.1).

**N15 — order of A. RESOLVED** (§4.1 l.567-571; §4.13; §11.3). A and m_mig computed once at day 12, after the MET model; the string propagation moved to days 12–19 (same CPU).

**N16 — time tag. RESOLVED** (§4.6 l.1033-1052). Test population = truth-attributed prompt candidates (5.8×10⁵ at R04); credit limited to the deepest window edge with an evaluable PASS (no extrapolation in t_cut, so no extra width formula is needed).

**N17 — overlay sourcing. RESOLVED** (§4.4 l.810-824; §4.17 row 25; script [3]). Derivation overlays from pool events (correlation carried by the joint bootstrap); disjoint scan slice for the test overlays: N_scan = 4,000/H(R06) ≤ 10⁶, 2×10⁶ budgeted, 13 CPU-h.

**N18 — Phase 3 staffing. RESOLVED** (§11.1, §11.3 l.2305-2337). Three channels, 12 days (36 channel-days); prototypes and BDT recipe in the production window; C-5 applied (Phase 2 in 5 days, Phase 5 in 4). Calendar 57.9 → 56.6 days.

### Residuals of cycle-1 findings

| finding | status | where |
|---|---|---|
| M4 | RESOLVED via N5 | §4.0 point 7 |
| M5 | RESOLVED via N1 and N2 (remainder in Q3) | §4.4, §4.7, Q3 |
| M11 | RESOLVED via N13 | §4.9, Df-7 |
| M12 | RESOLVED: the two sentences added | §4.9 l.1233-1237; COM B6-c |
| M15 | RESOLVED via N4 | §4.0 points 4–5 |
| M24 | dated commitment (accepted by the arbiter); the date now reads "days 0–5" | §11.5 |
| M26 | RESOLVED via N9 | §2 |
| M25 residual | COM B4-c reads "R06 (and R07 where evaluable)" | COM |

### C items

| item | status | where |
|---|---|---|
| P-C2 criterion on the bias of the median | applied: reading (e), tied to the 84 % edge | §4.11 point 4 |
| P-C4 infracolour refinements | applied (three refinements named, numbers in script [13]) | §4.14 l.1737 |
| P-C5 re-allocation with gains | applied, pre-registered | §4.4 point 5 |
| P-C6 categories without time-tag credit | stated | §4.6 point 5 |
| P-C7 full T2 list frozen | applied | §4.1, §4.12 l.1528 |
| P-C8 proportionality | folded into the arbiter's §5 | §11 |
| P-C9 lepton-veto argument | applied | §4.13 l.1672 |
| K-N13 T2-e criterion | applied | §4.12 l.1574 |
| K-N14 sealed file | outside the tree and encrypted; PASS/FAIL only for the family z and the global χ² | §4.1 l.537 |
| K-N15 label precedence | applied | §4.11 point 3 |
| K-N16 lever sum | the sentence is gone with the old GA-8; §11.6 lists each lever with its own number | §11.6 |
| K-N17 key path | applied | §4.11 T1-b |
| K-N18 biasing | always when its closure passes; pool split by the gains | §4.4 point 5 |
| K-N19 version diffs | "v1 of this document" removed from the body (0 hits); comparisons only in §13 | §13 |
| K-N20 PV-pair R05 entry | the derived entry is not shown any more (Table 4.4b lists counts only) | Table 4.4b |
| K-N21 B5-a | labelled as limited by B5-c | §4.8 |
| K-N22 | merged into N4 (K = 10) | §4.0 |
| conventions check 3 | per-nuisance pull reading | §4.11 T1-e, §5.2 |
| N C-1 toys | adopted: −156.5 CPU-h net of the exact-toy checks (the verdict's −191 did not cost the checks) | §4.11 point 5 |
| N C-2 overlays | adopted and extended by N8: 17,500 instead of 42,000 events | §4.4 |
| N C-3 B5 | signal road on 10,000 events; rotation inline; lever (iii) left as a Q4 option | §4.8 |
| N C-4 pool staging | day-15 rule with a 156 CPU-h reserve | §11.7 |
| N C-5 calendar | Phase 2 → 5 days, Phase 5 → 4 days, PREREG drafted in Phase 3 | §11.3 |
| N C-7 figures | four added; Fig. 7 marked directly | §9 |
| N C-8, C-9 | bracket, change of the bound, R07-direct size | §4.4 |
| N C-10 fresh B3 sample | named and costed | §8 |
| N C-11 | **not adopted**, by the arbiter's ruling: the 26 CPU-h stay, the shift is reported beside the limit | §4.4 |

## 3. Items that end in a dated rule (not claimed as done)

| what | measured by | rule written in |
|---|---|---|
| H against direct counts; completeness fractions | Phase 3 on development samples, before the freeze; verdict in 4a | §4.4 point 4 |
| m_H, enrichment, gains; projection and outcome class | pilot, days 0–5; decided at day 15 | §11.7 rules 1, 3 |
| s_model of every estimator against its cap | development samples, day 15 | §4.0 point 4 (c); §11.7 rule 2 |
| crossing-test evaluability | Phase 3 | §4.0 point 7 |
| secondaries (multi-secondary class) | Phase 3, 1,000 events | §2 |
| per-k promotion | Phase 3 | §4.4 point 4 |
| R06 rates of the small SM processes and of the three sized ones | Phase 3 | §11.7 rule 4; §4.7 |
| retrieval outcomes | days 5, 15, 17 | §6.4 |
| infracolour constant | R-12 | §4.14 |

## 4. Numbers: script rerun, propagation, stale-value grep

`python3 -I phase1_strategy/src/strategy_budget.py`: exit 0, 415 lines, about 4 s. New or rewritten sections: [5] deltas v2 → v3 per finding; [6] thresholds, envelope and conditional draws; [7] calendar; [9] floors by route; [9b] projection per outcome; [11] N4 rates and N2 statistics; [12] widths.

| quantity | v2 | v3 |
|---|---|---|
| MUST / reduced / full CPU-h | 3,968 / 4,401 / 4,915 | **3,945 / 4,378 / 4,891** |
| calendar, proposed variant | 57.9 days (44 without production) | **56.6 days (42 without production)** |
| stop-and-ask threshold (1.3 × reduced) | 5,722 | **5,691** |
| contingency listed | 1,989 | 2,135 (not pre-approved) |
| summed zero-count floor | 45.3 events | **11.7 events** (pool 665 CPU-h incl. Geant4 vertices) |
| storage | ≈ 410 / 610 GB | ≈ 420 / 620 GB |

Propagation: the changed values were written from the script output into v3 and COM. Occurrences of the new values (grep): floor 11.7 ×22 in v3 and ×1 in COM; 4,378 or ≈ 4,380 ×6; 3,945 or ≈ 3,950 ×4; 4,891 or ≈ 4,890 ×4; 57 days or 56.6 ×7; 5,691 ×4; 2,135 ×3; 1,371 ×5; 665 CPU-h ×6; K = 10 ×3 in v3 and ×3 in COM; "day 15" ×15 and ×4. After I enlarged the three SM samples (margin on the evaluable count), 59 strings of the v3 text were updated in one scripted pass with a uniqueness check on each.

Stale-value grep on v3 and COM for: 45.3, "45 events", 3,968, 4,401, 4,915, 5,722, "58 days", 57.9, 1,261, 1,989, 7.65×10, 1.74×10⁷, 1.20×10⁸, "600 CPU-h", "294 CPU", 42,000, "day 7", "six parallel", "44 days", GA-n, "K = 12", "7.5 %", "10.4 %", 0.029, 0.097, 2.44, "s_model ≤ ln F,", "placeholder s_model", 495–662, "v1 of this document". Hits: only explicit comparisons (v3 l.2252, 2259, 2270, 2594, 2603, 2647, 2667; COM l.60, the mapping of the old GA markers). No stale value in current text.

## 5. Neighbourhood checks

1. *After N8 (PV pairs)*: checked every other topology sourced from the hard-scatter vertex in v1's code (`normalise.py`: 'HS vertex only' for γ, V⁰, PV pair, looper; 'HS + 200 × min-bias' for DIF and NI). All four hard-vertex topologies moved, not only PV pairs. Also checked the heavy-flavour row of §5.1 and COM SY-14, which assumed "add to B1": now B4.
2. *After the W(τ) denominator error*: read all four `n_class_events` and all R04–R07 rows of `background.json → sm` and all eight `cprime` topologies. Found that the counts that matter are preselection-weighted (effective) counts (Z(νν) has 81 raw candidates but 32.3 effective); v2's "about 200 in the test half" for Z(νν) is 81. Table 4.4b is now [V] instead of [U].
3. *After N4*: checked the other evaluability statements with the same σ_tot² = 1/N + s_P². Found one more error in v2: thinning at R07 was called evaluable with N_eff ≈ 80, but with the 70 direct counts σ_tot = 0.164 > 0.135; it needs N_eff ≥ 252. Corrected in §4.5 (l.954) and in the width discussion of §4.0.
4. *After sizing three samples exactly at N = 24*: an expectation of 24 gives 24 or more with probability 0.53. Sizes raised to an expectation of 31 (probability 0.92) for the three SM samples and for DIF; the pile-up direct count (expectation 70) reaches 55 with probability 0.97.
5. *After N5*: recomputed every width quoted anywhere (§4.5, §4.6, §4.12, Df-2), not only the table.
6. *After the Phase-3 change*: checked every date ("day 7" → day 5; decision point 3 → days 36–48; Herwig attempt days 0–5; COM ST-1).
7. *Labels*: every GA-n reference in v3 and COM mapped to Q1–Q5 / Df-1–Df-8; §10 row 1 and §9 updated to the four labels.
8. *Not re-audited*: [V] tags of text kept unchanged from v1 and v2 (same caveat as in cycle 1).

## 6. Self-audit: every acceptance criterion of a MUST item

"False fail" = probability that a correct result gets FAIL; "false pass" = probability of PASS when the truth is outside the tolerance by F^1.5 (closure tests) or as stated. Closure tests use the rule of §4.0; their generic rates are: false fail 0.5–1.1 % per test at s_model from 0 to the cap; false pass 5.9 % at |ln r| = 1.5 ln F with σ_tot at the limit (< 0.01 % at half the limit).

| criterion | test | sample and expected counts | evaluable? false fail / false pass | verdict it can reach |
|---|---|---|---|---|
| C1-a | 41 comparisons, Bonferroni, global χ², family coherence | 4,000 ρ = 1 events etc.; 2σ detectable shift 2–6 % at R04–R06; R07 12 counts; signal 34–80 % | yes; false fail 5 % (Bonferroni) + 1 % (χ²); power stated per quantity ("gross check only" above 50 %) | PASS / FAIL |
| C1-b | arithmetic identity | v1 counts | deterministic | PASS / FAIL |
| C1-c | container hash identity | one job | deterministic | PASS / FAIL |
| C1-d | blinding tier respected | ledger | procedural | PASS / FAIL; tier = Q1 |
| C1-e | twin ratio reported | 800 rows | diagnostic, no verdict | reported |
| C2-a | ≥ 48 of 50 twice | 50 + 50 | P(pass) 1.4 % / 11 % / 92 % at true agreement 0.85 / 0.90 / 0.98 | PASS / FAIL |
| C2-b | bit identity | 20 jobs | deterministic | PASS / FAIL |
| C2-c | \|z\| < 2 per family | 2,000 + 400 trials | false fail ≈ 5 % per family | PASS / FAIL (reported, no retuning) |
| C3 | checklist closed, grep zero | paper sources | deterministic | PASS / FAIL at Gate C |
| B1-a DIF | closure F = 2 at R06 (R07) | 4,000 enriched + 1,000 unbiased overlays; 31 expected at R06 (or 7,750 unbiased) | evaluable with probability 0.92 if s_P ≤ 0.10; generic rates | PASS / FAIL (NOT TESTED 8 %) |
| B1-a NI ×3 | closure F = 2 at R05 (rung split) | 1,000 unbiased overlays each; 92 / 120 / 378 | yes; generic rates; the test is one rung beyond the derivation only | PASS / FAIL |
| B1-b | widths tabulated, in the likelihood | — | bookkeeping | PASS / FAIL |
| B1-c | rate comparison within combined uncertainty | Geant4 against v1 | cross-check; outside → "failed cross-check", Geant4 kept | PASS / FAIL (no eligibility effect) |
| B1-d | material scan 1 %, positions 1 µm, physics list | geometry | deterministic | PASS / FAIL |
| B1-e | weights closure F = 1.5 at R05 | biased against unbiased, ≥ 55 counts | yes; generic rates | PASS / FAIL (FAIL → unbiased) |
| B1-f ceiling | one-sided, p < 0.001 FAIL | attributed counts at R04–R05: hundreds per 1,000 events | yes; false fail ≤ 0.35 % at the boundary; power: direct = 4 × H with 8 counts gives p = 0.001 | PASS / FAIL |
| B1-f completeness | 95 % upper limit of (leak + mixed)/attributed ≤ 0.26 | ≥ 30 attributed passers at R04–R06 | yes at R04–R05 for every term; at R06 where counts allow; false pass bounded because the limit itself is carried as c_mix | PASS / FAIL |
| B1-g | secondary-attributed count against prediction, factor 2 | 4,000 trials: ≈ 2,100 / 1,000 / 25 / 13 at R04–R07 | R04–R06 evaluable; development sample, so it decides a design step, not a verdict | rule applied before the freeze |
| B2-a | closure F = 1.5 at R04–R07 and crossing rungs | direct 96,000 trials; thinning N_eff ≈ 17,000–28,000 at R04–R06, ≈ 80 at R07 | R04–R06 yes; R07 only if N_eff ≥ 252 (expected no) | PASS / FAIL at R04–R06 |
| B2-b | closure F = 1.5 at R06–R07 and crossing rungs | direct: 2.4×10⁴ at R06, 70 at R07 (≥ 55 with probability 0.97; ≥ 64 with 0.78) | yes; two-rung test: false fail 1.9 % at the cap; NOT TESTED if its development r.m.s. > 0.135 | PASS / FAIL / NOT TESTED |
| B2-c | agreement beyond R07 | thinning N_eff ≲ 10 at R08 | expected NOT EVALUABLE (declared) | NOT EVALUABLE; consequence stated (one-estimator extrapolation) |
| B2-d | sample exists, independent | 24,000 events | procedural | PASS / FAIL |
| B2-e | RSS and storage measured | day 0 | procedural | PASS / FAIL |
| B2-f | widths tabulated | — | bookkeeping | PASS / FAIL |
| B2-g | N_eff per rung measured | 1,000 events | procedural | PASS / FAIL |
| B3-a, B3-d | stability of each conditional, F = 1.5 | no-pile-up pool halves; ≥ 55 passes after the cut needed | unknown until the pool exists: if P_geo counts are near zero the conditional is NOT TESTED and earns no credit | PASS / FAIL / NOT TESTED (credit only) |
| B3-b | as B3-a for the vertex veto | same | same | same |
| B3-c | time-tag closure F = 1.5 on prompt candidates | 5.8×10⁵ prompt R04 candidates; ≈ 5,800 late counts at 10⁻², ≈ 58 at 10⁻⁴ | widened edges yes; nominal edge marginal (needs 55); tails must be sourced | PASS / FAIL at tested edges; no credit otherwise (Df-5) |
| B4-a | proxy fraction zero | samples exist | deterministic | PASS / FAIL |
| B4-b | external MET validation within a pre-declared tolerance; multijet stability factor 2 with ≥ 100 effective events | public figure (R-3) | only if R-3 delivers; else stop-and-ask | PASS / FAIL / infeasible |
| B4-c Z(νν) | closure F = 2 at R06 | test half 5,000 events, N_eff 81 | yes; generic rates | PASS / FAIL |
| B4-c W(τ_h), W(τ_ℓ), tt̄ 1ℓ | closure F = 2 at R06 | N_eff 31 expected each | evaluable with probability 0.92 at v1's rates (which carry 33–57 % errors; sizes recomputed at day 15) | PASS / FAIL (NOT TESTED ≥ 8 %) |
| B4-c eight proxied processes, three additions | closure F = 2 at R06 | 2,000 events; no v1 count | expected NOT TESTED | **NOT TESTED → Q3** (ceiling test evaluable) |
| B4-d | every K cited | — | deterministic | PASS / FAIL |
| B4-e | flatness in MET bins, F = 1.5 | Z(νν), W pool samples | depends on counts per MET bin; else NOT TESTED → passing events only | PASS / FAIL / NOT TESTED |
| T1-a | schema | — | deterministic | PASS / FAIL |
| T1-b | v1 limit within 10 % | v1 counts, toys | toy error ≪ 10 % | PASS / FAIL |
| T1-c | (i)–(ii) within toy error; (iii) coverage ≥ 0.93 on 500 | toys | (iii): false fail 2.0 % if the true coverage is 0.95; a true coverage of 0.90 passes in 1.2 % (script [13]) | PASS / FAIL |
| T1-d | bias ≤ 20 % of μ_inj | 200 pseudo-experiments | standard error 4 % of μ₉₅: a 20 % bias is 5σ | PASS / FAIL |
| T1-e | mean pull ≤ 0.21; ≤ 10 % of fits beyond 2σ | 200 pseudo-experiments | false flag 0.3 % per nuisance; it triggers an investigation, not a FAIL | investigated / clean |
| T1-f | ranking produced; pruning limits | — | bookkeeping | PASS / FAIL |
| T1-g | table produced | — | bookkeeping | PASS / FAIL |
| T1-h | coverage ≥ 0.93 on 500 | stored distributions | as T1-c (iii) | PASS / FAIL |
| T1-i | every limit toy-based; f_T check within 2 toy errors | 3 check points per selection | check false fail ≈ 5 % per point (then exact toys, a costed draw) | PASS / FAIL |
| T2-a | content hashed before production | — | procedural | PASS / FAIL |
| T2-b | same choice on a second run | — | deterministic | PASS / FAIL |
| T2-c, T2-d, T2-f, T2-h | reported quantities | — | no verdict | reported |
| T2-e | G worse than the B = 0 value by more than the toy error | v1 counts | yes (one-bin: 9.9 against 3.0) | PASS / FAIL |
| T2-g | baseline evaluated | — | procedural | PASS / FAIL |
| S1-a | ≥ 99 % of jobs, ingestion closure | 80,000 rows | deterministic | PASS / FAIL per point |
| S1-b, S1-c, S1-e | procedural | — | — | PASS / FAIL |
| S1-d | error reported | — | no verdict | reported |
| S1-f | m_mig ≤ 5 % rule; sourced window or limitation | 5×10⁵ LHE events | statistical error on m_mig ≪ 5 % | rule applied |
| S2-a | \|z\| < 3 and 0.5 %; 3 %; 2 % or 3σ | integration runs | false fail ≈ 0.3 % per comparison; validation 2 NOT EVALUABLE if no fixed-order reference | PASS / FAIL / NOT EVALUABLE (stated) |
| S2-b … S2-f | tables, definitions, sourced numbers | — | deterministic or "not sourced" with a fixed consequence | PASS / FAIL / not sourced |
| P1-a … P1-d | pre-declared readings | 970 paired events etc. | every outcome is reportable; B*-off sized for 5σ if the effect is as measured | reading reported |

MUST criteria expected NOT TESTED after this fix: B4-c for the eight proxied processes and the three additions (Q3), B2-c (NOT EVALUABLE, declared, with its consequence), and B3 conditionals wherever the pool has no counts (credit only). No other MUST closure is planned to stay untested.

## 7. Points a verifier is likely to contest

1. **The floor fell from 45 to 12 events without new CPU.** It follows from N8 (18.4 + 4.7 events were counted twice, and their pool share moved to the remaining terms). The open number is now the ceiling of the real SM events, m_H, which the pilot measures; the headline is given as a range (575–790 GeV for m_H from 100 to 0), not as the best case.
2. **Cap s_model ≤ ln F/3.** It may exclude a useful estimator (for example an occupancy model good to 20 %). The alternative ln F/2.5 is in Df-2 with its rates (15 % / 6 %). The cap is what makes the user-facing rates true.
3. **Re-test criterion p′ ≥ 0.05/K** instead of v2's p′ > 0.05. Justified by the shared model bias; F is unchanged.
4. **NI tested at R05 only** (rung split): a verdict, but a shallow one; the price is a width of 2.09 at R08.
5. **γ, V⁰ enriched derivation and test overlays dropped** (not only staged): they no longer belong to a term. Their 1,000 unbiased events stay for the ceiling and completeness tests, and the CPU went to the three SM samples.
6. **Completeness bound 0.26 and the truth definition of "mixed"**: a convention on the scale ln F/3, carried as c_mix; the floors and Table 4.4c do not include c_mix (between 1 and 1.26).
7. **The reach mapping**: read from the plan's σ_ln = 0 row at equal one-bin expected limit; EST, v1 efficiencies. It reproduces the constructive review's value for the v2 floors (24.1).
8. **The EST pile-up term** uses v1's conditional fractions (2/35, 32/126, 12/32) transcribed from D4 [U].
9. **Phase 2 in 5 days** and decision point 1 at day 5 (the verdict's text says day 7 for checkpoint 1, written before C-5 was applied).
10. **v3 is longer than v2** (2,674 against 2,391 lines) although superseded text was removed (old GA list, v1 comparisons, the v1 → v2 delta table). The additions are the tables the verdict asked for: size and power, Table 4.4c, the route table, the Q3 annex, the day-15 rules and the change table.
11. **Toy saving is −156.5, not −191 CPU-h**: the exact-toy checks (35 CPU-h) are now costed.
