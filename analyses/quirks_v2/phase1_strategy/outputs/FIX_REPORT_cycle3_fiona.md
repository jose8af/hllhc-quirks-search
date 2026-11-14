# Fix report, review cycle 3 (fixer Fiona, 2026-11-13 23:05)

Verdict worked from: `review/arbiter/STRATEGY_ARBITER_v3_felix_2026-11-13_22-40.md` (ITERATE; P1 (A), P2–P16 (B), the C
items of its §4, the rulings S-1 and S-3, the length cuts of its §6 (v)).
Artifacts: `outputs/STRATEGY_fiona_2026-11-13_23-05.md` ("v4", 2,842 lines; v3 is unchanged), `QV2/COMMITMENTS.md`
("COM"), `src/strategy_budget.py` ("script"; run with `python3 -I`, exit 0, about 9 s; output in the session log's
scratchpad). Section headings below are those of v4; each quoted phrase can be found with grep in the named file.

## 1. Status per finding

| # | status | what changed | where (v4 heading; grep phrase) |
|---|---|---|---|
| P1 (A) | RESOLVED | Z(ττ) (4.26×10⁵, range 10⁵–1.3×10⁶) and lost-lepton Z(ℓℓ) (2.98×10⁴, range 10⁴–10⁵) added to the pool with EST planning N_trig and written arithmetic; allocation re-run inside 665 CPU-h; both re-split and keep-11.7 options printed; multijet planning floor added to the headline sum; inventory rows 18a/18b with seed streams; Table 4.4a rows; "not in the table" deleted; Table 4.4c carries the additions in every row; rule 1 recomputes the projection for every term; re-allocation at day 12–15 | §4.4 Table 4.4a: "the N_trig of the three additions are planning values"; §4.17: "`prod.hs0.ztt`"; §4.7 point 3: "fourteen are v1's twelve and the additions"; §11.7 rule 1: "for every term of the likelihood"; rule 6: "Pool shares of the additions"; script [9]: "P1: Z(tautau) planning N_trig" |
| P2 | RESOLVED | script [9b] scenarios (α1), (α2) with and without credit, (β), (γ); m_H rows relabelled "Z(νν) enters at its ceiling (estimator not credited)" with "simulated ceiling events (… background events)"; §0 and Q2 lead with the 84 % edge and the (α) range; 790 marked as the empty-ceiling median, an upper edge; caveats (PV placement, attribution rule, 45 ms, ×1/0.87 fast path, Ph-C6 mapping); the day-15 pause a realistic branch; which number heads the abstract; EST tag inside Q2; label holds for small m_H (N-C7) | §0: "Expected (EST, v1 placeholder efficiencies, best Λ per mass):"; §0: "The abstract heads with the 84 %"; §4.4 Table 4.4c: "(α1)** DIF and conversions from v1's R06–R07 counts"; "Scenarios (β) and (γ)."; §12.1 Q2: "this is a realistic branch, not an"; script [9b]: "HEADLINE (P2)" |
| P3 | RESOLVED | definition of H with respect to CKF: table of every fixed cut and its monotonicity; default Df-9 option (a): H on all own hits, CKF removal and f_CKF as S_CKF, credited where tested (R04–R06), s_tot beyond, censored at 1; option (b) stated; "complete by construction" sentence replaced; m_H EST for Z(νν) under option (a) (10–890 depending on ε_pair) | §4.4 point 4: "for the cuts that are monotone under added hits"; "*S_CKF (Df-9).*"; Df-9 row; script [9b]: "P3/P14 EST" |
| P4 | RESOLVED | ceiling and leak tests only on unbiased samples (1,000 unbiased DIF overlays, NI overlays, hit-level halves); enriched overlays only for S/π_k; leak an implementation check; sub-topology ceiling test dropped (default (ii)), costed alternative named; development samples named (sample 13a, 1,000 unbiased Geant4 DIF overlays, +7.0 CPU-h; pilot Geant4 vertices, +6.0 CPU-h, K-C10); effective-count form for weighted samples | §4.4 point 4: "only on unbiased samples."; "it is an **implementation check**"; "*Weighted samples*"; §4.4 Scope: "They have no ceiling test"; §4.17 row 13a: "`dev.ovl.dif`" |
| P5 | RESOLVED | paired pile-up-only finder pass, 26 CPU-h (4,000 unbiased B1 test overlays + 1,000 test-half events of each supplied B4 process); mixed excess = mixed(with term) − mixed(term hits removed); 0.26 kept as a convention; after a completeness FAIL a term without credit enters at H′ = P_geo + Σ_all k f_k, eligible and flagged, ineligible only if H′ fails its ceiling test; expected mixed fraction a dated day-15 input | §4.4 point 4: "paired pile-up-only finder pass"; §4.0 point 6: "extended ceiling"; §11.7 inputs: "with the expected mixed excess" |
| P6 | RESOLVED | one ceiling verdict per term (Šidák-corrected min-p over its rungs), Bonferroni over T_c = 19 terms (α_c = 0.05/19; INVESTIGATE up to 5α_c with one re-test): family-wise 4.9 % at the boundary; sub-topology tests dropped (P4 (iii)); added to script [11], the §4.0 point 4 table, §4.0 point 6, §4.12 rule 1, Df-2 and the PREREG outline; "loses a selection" restated as 6.9–8.9 % | §4.0 point 4: "either family removes a selection"; §4.4: "One verdict per term"; §4.12 rule 1: "a false FAIL removes a selection with probability 6.9–8.9 %"; §8: "the combined ceiling test (Šidák"; script [11]: "v4 ceiling family (P6)" |
| P7 | RESOLVED | default Df-2 option (a): the occupancy comparisons at R09⊗R06, R11⊗R06, R15–R20⊗R06 are consistency checks with no distance credit; thinning and π_k crossing tests keep credit; the R07→R08 width step always counts; table row and every reading using 0.45–0.49 corrected | §4.0 point 7: "**consistency checks with no distance credit** (Df-2)"; table row "occupancy model, 2S crossing test PASS"; §4.5: "1.30 at R14 with a 2S crossing PASS"; §4.12: "usable to about R09 whatever its crossing comparisons give"; script [12]: "v4: occupancy model, only the 2S crossing test PASS" |
| P8 | RESOLVED | row "π_k tested at R06 only (expected …)": 1.41 / 1.41 / 1.41 / 2.51 (1.42 with a 2S crossing PASS); R06–R07 kept as the conditional row; §4.12 distances corrected; §0 did not use 0.73 | §4.0 point 7: "**promotion π_k tested at R06 only**"; "Checks of the new rows"; script [12]: "v4 (P8)" |
| P9 | RESOLVED | third condition of "target met" is "every leading term labelled estimate" in §4.11 point 3, COM TG-1 and §0; s_tot printed next to every label (Ph-C4) | §4.11 point 3: "**every leading term"; "each printed with the s_tot of"; COM TG-1: "every leading term is labelled estimate" |
| P10 | RESOLVED | Q3 widened to every MUST criterion ending NOT TESTED / NOT EVALUABLE / not submitted by statistics, fluctuation, cap rule or day-15 rule; annex rows for the fluctuation route (P = 0.30 from script [11]; compliance by the staged top-up, 0 CPU-h by default), the cap route, B3-a…d and B4-e, B2-c; consequence under (a) ("no credit" labels; reserve possibly spent by rule 3); §4.0 point 6 and §11.7 rule 2 aligned. The cycle-2 FR statement "No other MUST closure is planned to stay untested" (FR cycle 2, §6) is superseded by this annex | §12.1 Q3: "brief D4 exception, completed"; annex: "**route 1: fluctuation**"; §4.0 point 6: "every route by which a MUST criterion ends so"; §11.7 rule 2: "(a Q3 route)"; script [11]: "P10 fluctuation route" |
| P11 | RESOLVED | T1-c (iii) and T1-h are one family of 10 checks, 500 pseudo-experiments per (point, λ); thresholds against the convention's computed coverage c_ref (at most 0.95): FAIL below 462 of 500 at 0.95 (459 at 0.945), INVESTIGATE band and one re-test; family-wise 4.7–4.9 %; pooled alternative; Df-10; script [13]; COM T1-c/T1-h | §4.11 point 6: "**Coverage family (T1-c (iii) and T1-h; default Df-10).**"; script [13]: "v4 T1 coverage family" |
| P12 | RESOLVED | Q5 and §4.17 premise: content depends on the MET model, the trigger threshold and the generator-cut decision, frozen by day 12, but on no plane-selection choice and no T2 efficiency; "no" moves 47 + 266 CPU-h onto the critical path (+1.8 days, the script's 312 CPU-h at 174 per day) | §12.1 Q5: "premise corrected"; §4.17: "on no plane-selection choice and on no signal efficiency at any T2 candidate" |
| P13 | RESOLVED | the 156 CPU-h reserve is inside the approved figure: 4,417 + 156 = 4,574 CPU-h (exact 4,573.6), threshold 5,946; §11.2 "none of these is inside … approved in advance" contradiction removed (the reserve is a row of the budget table, not a conditional cost); §0, §11.6, Q4 and COM ST-1 updated; script [4] and [6] print the values | §11.2: "**Approved figure**"; §11.6: "4,574 CPU-h"; §12.1 Q4: "Approve **4,574 CPU-h**"; script [4]: "v4 approved figure" |
| P14 | RESOLVED | (i) no Phase-3 SM samples: v1-proxy rates (with errors) at day 15; staged 4a hit-level campaigns with top-up (§4.7, §11.7, §4.17 row 20, COM INV-1, B4-c; the Phase-3 B4 line relabelled "no SM hit-level sample"); (ii) pilot reading: Gamma(m + 1) of the pilot count, branch of rule 3 from the R06–R07 pilot counts extrapolated with the pilot's own fall (EST); "best candidate" defined; rule 1 preliminary at day 7, binding at day 15 | §4.7: "**the 4a hit-level campaigns are staged**"; §4.4 point 5: "*Reading of the pilot (fixed now).*"; §11.7 rule 1: "computed **preliminarily at day 7**"; "B₅₀ is read at the best candidate" |
| P15 | RESOLVED | per-k promotion comparison on the pilot's 1,000 near-pass overlays (sample 11), expected 2–4 qualifying classes (EST), fewer than two → "not submitted", term at H; 4a derivation overlays then refine only the post-freeze S; §8 item (2) and COM PR-1 add the ceiling test, completeness bound, c_mix and S_CKF (and the coverage family) | §4.4 point 4: "**pilot's 1,000 near-pass overlays"; §8: "for each term with a ceiling"; COM PR-1: "the ceiling test with its family of 19" |
| P16 | RESOLVED | slot table per phase (≤ 3 agents); one Phase-3 1-bot review on `SELECTION.md`; PREREG drafter as channel (iii)'s second task from day 12; sealed C1 comparison as a short separate session in channel (i)'s slot; S-1 adopted and the calendar recomputed by script [7] (57.6 days); residual: Phase-3 development is 30 channel-days against PLAN's 35–50, reported | §11.3: "**Agent slots (finding P16"; script [7]: "v4 agent-slot table (P16" |

Earlier partial items carried by the verdict (M4, M5, N1, N2, N5, N7, N14, N18) are covered through P1–P16 as mapped
in the verdict's §10.

## 2. C items (verdict §4) and adopted rulings

| item | status | where (grep phrase) |
|---|---|---|
| Ph-C1 / K-C5 one NI rate set, ×0.22 named | RESOLVED: script uses `background.json` → `cprime.ni*.rate.value` (0.0982, 0.1241, 0.1241) × the PV-line factor 0.22 (`wp.py` l.40 `P_PV_LINE`) | §4.4 point 6: "PV-line factor" |
| Ph-C2 no Geant4 conversions in B1 | RESOLVED | §4.4 point 1: "Conversion products are **not** injected into B1 samples" |
| Ph-C3 B4-c by sub-topology | RESOLVED | §4.7: "split by truth sub-topology" |
| Ph-C5 occupancy s_model out of sample | RESOLVED | §4.5: "at a development rung not used for the inputs" |
| Ph-C7 multi-vertex class per rung | RESOLVED | §2: "The multi-vertex class" |
| Ph-C8 ln-rejection distance in Df-2 | RESOLVED | Df-2: "in ln of the extrapolated rejection" |
| Ph-C9 predictive pile-up cap | RESOLVED (text and script) | §4.11 point 1: "drawn like every other zero-count term"; Table 4.4c caption: "426 × Exp(1)" |
| K-C1 re-test departure in §5.2 and Df-2 | RESOLVED (price printed by script [11]) | §5.2 row 1: "Departure from" |
| K-C2 W(τ) generation mode | RESOLVED: two forced-decay samples, costs stand (inclusive alternative +11 CPU-h, from the review, [U]) | §4.7: "two forced-decay samples" |
| K-C6 Geant4 slab yield | RESOLVED (script: floor 13.4 at c_NI = 30.6 ms) | Table 4.0, Geant4 row: "if a sixth of the vertices falls in a given slab" |
| K-C7 four labels in COM T1-c | RESOLVED | COM T1-c: "no credit / bound / low count / estimate" |
| K-C8 wording on pre-hash samples | RESOLVED | §4.17: "enters a closure verdict or a limit" |
| K-C9 C2-c family | RESOLVED (Bonferroni \|z\| < 2.73, script [11]) | §4.2 table: "Bonferroni over the 8 tests" |
| K-C11 BL-1 line in §12.3 | RESOLVED | §12.3 item 5: "selection-independent blinding exception is declared" |
| K-C12 thousands, not hundreds, in the Q3 annex | RESOLVED | annex: "hundreds (B1 overlays) to thousands" |
| K-C13 which costs checkpoint 1 fixes | RESOLVED (script [6]: 870 of the 1,378 G CPU-h) | §11.6: "The day-5 timing jobs fix the unit costs behind 870" |
| N-C2 notation true λ | RESOLVED | §4.11 T1-c (iii): "fixed true λ = 0.5, 1.14, 2, 3" |
| N-C4 mapping against `ch29_checks.py` | RESOLVED: confirmed, l.25-47 (CLs at the Poisson-median n, fixed B) and l.54-58 (best Λ per mass) | §4.4 Table 4.4c bullets: "ch29_checks.py" |
| N-C8 R-20 deadline | RESOLVED | §6.4: "R-10 and R-20 before Phase 4a" |
| N-C9 84 % point on Fig. 7 | RESOLVED | §9: "the conservative point" |
| N-C11 B4 s_model from Z(νν) | RESOLVED | §4.7: "its s_model can be derived" |
| N-C12 4a review buffer | RESOLVED via S-1 (1.5-day line in script [7]) | §11.3 row "35–36.5" |
| C1 remediation time (N Part 2.4) | RESOLVED | §11.3: "If a C1 family fails and needs remediation" |
| N-C10 (Df-1 as a question) | not adopted, by the verdict; Df-1 stays first with its reading spelled out | Df-1: "a reading of the plan" |
| K-C10 | folded into P4 (+6.0 CPU-h) | script [3]: "Geant4 vertices of the pilot's unbiased DIF and NI events" |
| S-1 | ADOPTED: B5 and the B6 signal arm in days 36–48; COM B5-a…c deadline 4a → 4b; the 4a note states that B5 and B6 are pending | §4.8: "**Schedule (S-1, adopted):**" |
| S-2 | not adopted (verdict) | — |
| S-3 | ADOPTED in part: one Phase-3 1-bot review; drafter in channel (iii) after day 12; P1 stays in Phase 2 (brief l.264-265) | §11.3 slot table |
| Rules 1 and 3 at day 7 | ADOPTED as ruled: rule 1 preliminary at day 7, binding at day 15; rule 3 stays at day 15 | §11.7 rule 1 |
| Length (verdict §6 (v)) | PARTIALLY: §13.1 deleted (pointer), §13.2 reduced to the two number corrections, eligibility logic stated once (§4.0 point 6, referred to from §4.11 point 3, §4.12 rule 1, the partial-outcome table and COM T2-a), §12.4 replaced by a pointer, Table 4.0 merged with the §11.2 provenance table. **v4 is 2,842 lines, above the ≤ 2,500 target**: the mandatory cuts remove about 140 lines and the required additions of P1–P16 add about 300. Further cuts would touch content that the verdict did not flag. The optional moves were not made | §13.1, §13.2 |

## 3. Numbers that changed (old → new, why)

All new values are printed by the script (section in brackets).

| quantity | v3 | v4 | why |
|---|---|---|---|
| summed 68 % zero-count floor | 11.7 | 12.6 (pool) + 0.46 (multijets) = 13.0; ranges 12.2–13.3 (pool), 12.2–17.8 | P1, Ph-C1 [9] |
| predictive median, 16–84 %, σ_ln of the summed floor | 9.6, 6.7–13.8, 0.36 | 10.8, 7.7–15.2, 0.34 | P1 [9] |
| DIF floor, M, κ | 2.93, 2.53×10⁷, 2.57 | 3.04, 2.44×10⁷, 2.67 | re-split [9] |
| NI N_t, floors | 9.89×10⁵ each, 0.28 | 8.83×10⁵ / 1.12×10⁶ / 1.12×10⁶; 0.28 / 0.31 / 0.31 | Ph-C1 [9] |
| Z(νν) M, κ, floor | 1.14×10⁷, 2.20, 2.51 | 1.10×10⁷, 2.28, 2.60 | re-split [9] |
| B1 and SM pool shares | 215 (3.72×10⁷), 450 (3.6×10⁷) | 208 (3.61×10⁷), 457 (3.65×10⁷) | re-split [3] |
| floor with the reserve / doubled pool | 9.5 / 5.9 | 10.2 / 6.3 | [9] |
| biased-generation gain for 1 / 0.11 events | 12 / 106 | 13 / 114 | [9] |
| CPU-h for a floor of 1 event | 7.8×10³ | 8.4×10³ | 665 × 12.6 |
| headline reach, empty ceilings | ≈ 790 (median, led) | ≈ 710 at the 84 % edge (median 790) | P2 [9b] |
| reach with v1's DIF/conversions, no credit | — (≈ 500–650 in the verdict's draft) | 470–500 GeV (84 % edge 421–455) | P2 [9b]; see §4 |
| Table 4.4c rows | 834 / 793 / 761 / 723 / 661 / 575; R08-like 527 | 830 / 790 / 761 / 720 / 657 / 576; R08-like 496 | P1, Ph-C9 [9b] |
| one Z(νν) ceiling count | 2.2 events | 2.3 events (2.28) | re-split |
| class limit of decision point 2 | m_H 130, ≈ 550 GeV | m_H ≈ 125, ≈ 560 GeV | [9b] |
| doubled-pool gain | ≈ +30 GeV | ≈ +25 GeV (814 − 790) | [9b] |
| change of the bound | 3.7–4.7 decades | 3.1–4.7 decades ((α1) to empty) | [9b] |
| MUST / reduced / full | 3,945 / 4,378 / 4,891 | 3,984 / 4,417 / 4,930 | P4, P5, K-C10 (+39.1) [4] |
| approved figure (proposed) | 4,378 | 4,574 (4,573.6) | P13 [4] |
| stop-and-ask threshold | 5,691 (5,128 / 6,359) | 5,946 (5,382 / 6,613) | P13 [4], [6] |
| envelope alternative | 6,513, threshold 8,467 | 6,720, threshold 8,736 | [6] |
| contingency; M / D / G | 2,135; 691 / 2,316 / 1,371 | 2,146; 717 / 2,322 / 1,378 | new lines [6] |
| doubled guesses | ≈ 5,750 | 5,952 | [6] |
| Phase 2 / 3 / 4a MUST CPU-h | 500 / 573 / 2,675 | 506 / 580 / 2,701 | [4] |
| B1, B4 item totals | 522, 1,131 | 542, 1,150 | [4] |
| pilot | 55 CPU-h | 61 CPU-h | K-C10 |
| calendar (proposed) | 56.6 days | 57.6 days ("58") | S-1 (−277 CPU-h off the window), N-C12 buffer (+1.5 d), reserve on the critical path (+0.9 d), P5 (+0.15 d) [7] |
| calendar MUST only / full | 54.1 / 59.6 | 56.7 / 57.9 | [7] |
| range | 46–64 days | 49–65 days | [7] |
| non-production days | 42 | 43.5 | N-C12 buffer [7] |
| 4a critical-path production | 2,548 CPU-h = 14.6 d | 2,453 CPU-h = 14.1 d | [7] |
| Gate B | ≈ day 48 | ≈ day 49 | [7] |
| [DP1] / [DP2] days | 2.1 / 0.9 | 0.2 / 0.1 (calendar of full SHOULD +0.3 d) | S-1 |
| selection lost to a false FAIL | 2–4 % | 6.9–8.9 % | P6 [11] |
| occupancy width with crossing PASS, R09–R20 | 0.45–0.49 | 0.59 / 1.29 / 1.30 / 2.47 / 3.68 | P7 [12] |
| π_k planning row (expected case) | 0.73 / 2.20 / 0.77 | 1.41 / 2.51 / 1.42 | P8 [12] |
| T1 coverage threshold | ≥ 465 of 500 per check | FAIL below 462 (c_ref 0.95), family of 10 | P11 [13] |
| C2-c threshold | \|z\| < 2 | \|z\| < 2.73 | K-C9 [11] |
| storage, no-PU full records | 845 GB | 841 GB | pool events [8] |
| fresh B3 pool slices | 71 / 83 CPU-h | 69 / 80 CPU-h | re-split [6] |

Propagation: the new values were written to every place that quoted the old ones (§0, §4.0, §4.4, §4.5, §4.7, §4.11,
§4.12, §4.17, §7, §11.2, §11.3, §11.6, §11.7, §12.1, §12.3, §12.5, §13.3 and COM). Counted occurrences of the key new
values in v4 / COM: 4,574 (7 / 2), 5,946 (6 / 2), 12.6 (7 / 0), 58 days or 57.6 (7 / 1), 6.9–8.9 % (4 / 0), 1.41 (6 /
0), 1,378 (7 / 0), 2,146 (3 / 0), 4,417 (4 / 1), 4.9 % (6 / 1); about 120 edits in total across 2 files.
**Stale-value grep** on v4 and COM for 11.7 (events), 9.6, 6.7–13.8, 0.36, 5,691, 4,378, 3,945, 4,891, 2,135, 1,371, 56.6,
"57 days", "42 days", 0.45–0.49, 7.9, 3.6×10⁷, 1.14×10⁷, "2.2 events", 450, 215, 9.5, 5.9, "eight defaults", "2–4 %",
"5–12 %", 834, 793, 723, 661, 527, 2.93, 3.72×10⁷, 522, 1,131, 573, 2,675, 2,114, 2,548, "14.6 days", "46 days",
"64 days", 1,364, 1,073, "55 CPU-h", "0.35 %", "hundreds per", "not in the table", "λ·M", "≥ 465", 845 GB, 5,750,
"day 48": hits remain only in the explicit v3 → v4 comparisons (§11.2 "Changes against version 3", §13.3), in
unrelated quantities (the 11.7 s finder trial, "§11.7" references, the S1 total of 834 CPU-h, MUST-only "57 days"),
and nowhere as a current value.

## 4. Changes not literally specified by the verdict (each needed to carry out a ruling)

1. **(α) terms enter the projection as counted ceilings** (Gamma(m + 1) on their pool share), not with the v1-based
   projection uncertainty of about a factor e as a log-normal width. With that width the hybrid limit is dominated by
   the width and the reach falls below 393 GeV; the scenario is about the size of the terms, and without credit a term
   sits at its counted ceiling with a small count width. Both readings are stated in §4.4. The resulting range,
   470–500 GeV, replaces the verdict's draft "≈ 500–650" as the verdict instructs ("the fixer replaces … with the script
   values").
2. **The 45 ms caveat**: the verdict's draft says doubling it raises the SM floor "to about 11"; the script gives 15.7
   (summed pool floor 20.8), because the allocation shifts CPU to the SM terms; the script value is quoted.
3. **Fluctuation route**: the verdict writes 1 − 0.92⁴ = 0.28; with the exact P(Poisson(31) ≥ 24) = 0.916 the script
   gives 0.30, which is quoted.
4. **Approved figure and threshold**: the verdict's "≈ 4,573" and "≈ 5,945" become the script's 4,574 (4,573.6) and
   5,946.
5. **"Best candidate"** (P14 / N-C6): the verdict's phrase "lowest projected B₅₀ × (1/G)" is implemented as N-C6 asks:
   the candidate with the lowest G computed with v1 placeholders and the projected background, with B₅₀ read there.
6. **Calendar**: the N-C12 buffer is made an explicit 1.5-day line (S-1 "provides" it), and the reserve's 0.9 day is
   now on the critical path because the reserve is spent by default (P13). Net: 56.6 → 57.6 days.
7. **Ph-C9 in the projection**: drawing the pile-up cap as 426 × Exp(1) widens the R08-like comparison row (B₁₆ 87 → 67;
   reach 527 → 496 GeV). The R09 rows move by at most 4 GeV.
8. **Script numerics**: the Poisson sums in `pmf_pred` and `s95_pmf` are now computed in log space and windowed
   (b ± 10√b + 10), and `binom_tail` uses lgamma, because the (α) rows reach backgrounds of 10³–10⁵ where exp(−b)
   underflows. Every v3 row was re-checked unchanged except through the intended inputs (regression diff of the
   script outputs in the session log).
9. **P1 point 2, multijet planning N_trig**: 4×10⁵ (1 % of N_trig, range 0.1–10 %) is my planning bracket [E]; the
   verdict asked for a range without giving one. The Z(ττ)/Z(ℓℓ) planning values follow the verdict; the
   B(Z→ττ)/B(Z→νν) ratio of 0.17 is the review's number, [U] (no branching fraction is in the repo).
10. **P5 sample choice**: the 26 CPU-h are 8,000 trials (4,000 unbiased B1 overlays + 1,000 test-half events of each of
    the four supplied B4 processes); the eleven other processes take the excess fraction of the closest supplied
    process (EST), stated in §4.4.

## 5. Neighbourhood checks

- After P6 and P11: all family-wise statements in v4 and COM (K = 10, ceiling family, C1 Bonferroni, C2-c, T1
  coverage) were grepped and aligned (§4.0, §4.4, §4.11, §4.12, §5.2, §8, Df-2, Df-10, COM header, VC-3).
- After P7/P8: every width quoted from the §4.0 point 7 table (§4.5, §4.12, Table 4.4c text, [9b] print lines, Df-2
  alternative 1.1 vs 2.5) re-checked against script [12].
- After P1: every floor-dependent number (Table 4.4a, readings, §0, rule 3, Q2, Q3 annex floors, [L13], §12.5, the
  one-bin reading (a), the G threshold of T2-f) re-checked against script [9].
- After P13: every CPU-h total and threshold in §0, §11.2, §11.6, Q4, COM ST-1 re-checked against [4], [6].
- After S-1: every statement of B5/B6 timing (§4.8, §4.9, §11.2, §11.3, §11.5, §11.6, COM B5-a…c).
- COM: 103 open rows before and after; no identifier lost (comm of the identifier lists).

## 6. Not done

- Length target (≤ 2,500 lines) not met: 2,842 (section 2).
- No retrieval outside the repo, no sample produced, no git operation (as instructed).
