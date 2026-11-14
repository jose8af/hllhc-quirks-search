# Critical review, Phase 1 STRATEGY v3 (quirks v2), review cycle 3

Reviewer: Fabian (critical, fresh to this panel), 2026-11-13 22:00. Prompt template of `agents/critical_reviewer.md`
followed: adversarial stance, evidence for every "verified", sweep after each error, A/B/C classification.

Artifact: `phase1_strategy/outputs/STRATEGY_emeric_2026-11-13_21-10.md` ("v3", 2,674 lines, read in full in six
consecutive chunks), `COMMITMENTS.md` ("COM", read in full), `phase1_strategy/src/strategy_budget.py` ("script",
rerun). Also read: the cycle-2 arbiter verdict (Eloise) in full, `FIX_REPORT_cycle2_emeric.md` ("FR") in full,
`conventions/search.md` l.20-160, brief `prompt.md` l.55-99 and l.320-359, the cycle-1 arbiter (Dagmar) on M17, and the
v2 lines on the re-test rule. "l." is a line of v3 unless stated otherwise.

Tools: Read, grep and standard-library `python3 -I` on einstein (light arithmetic only). No sub-agents, no git, no
pixi. Phase 1 has no figures, so the figure checks of the template do not apply. There is no RAG corpus (deviation V8).

**Summary.** v3 is a careful and largely complete answer to the cycle-2 work list. I reproduced the budget, the
floor and every user-facing width and rate I checked. The stale-value grep is clean. I found **no Category A
item**. I found **7 Category B items** and **13 Category C items**. The B items share one pattern with the cycle-2
findings: a number or question shown to the user is right for what it covers but leaves out a case that the
document itself creates:
- Q3 does not cover every way a MUST closure can end NOT TESTED (F1).
- The eligibility false-fail rate leaves out the new ceiling tests (F2).
- One planning width is right for no term (F4).
- The coverage criterion of T1 fails a correct likelihood in 15–40 % of the cases (F5).
- The Q5 premise is inaccurate (F6).
- The approved figure leaves out a spend that the default plan makes (F7).

Each fix is text, plus at most one hour of script work.

---

## Part 1. Verification

Status: R = RESOLVED; P = PARTIALLY (what remains); NR = NOT RESOLVED; GA = Gate A (posed correctly or not).

### 1a. The seven partial cycle-1 findings

| # | v3 location | my check | status |
|---|---|---|---|
| M4 extrapolation width | §4.0 point 7, l.391-448; script [12] | Rule as stated: σ_b := b₀ for n < 3, b̂ := 0 for n = 1 (l.401-405); distance per quantity (l.397-400); crossing rungs (l.406-417); b₀ called a convention (l.418-421). Recomputed: occupancy at R08/R09/R11/R14/R17 = 0.427/0.589/1.29/2.47/3.67 (F = 1.5, s_model = 0.135, two test rungs in the width family), equal to the table at l.430. **But the π_k row "tested at R06–R07" (l.432) applies to no term in the expected case** (F4) | **P** → F4 |
| M5 testability | §4.0 point 6 l.383-387; §4.4 l.676-698; Q3 l.2480-2531 | Ceiling and completeness tests are defined. The Q3 annex covers B1-a and B4-c. Not covered: the "not submitted" route, the 8 % fluctuation route of the four supplied terms, and B3/B2-c/B4-e (F1). The ceiling test on the sub-topologies is undefined (F3) | **P** → F1, F3 |
| M11 variation sizes | §4.9 l.1209-1222; Df-7 l.2516; §6.4 l.1991-1994 | The arbiter's default is applied word for word: no public size means no nuisance, and the μ₉₅ shift is reported beside the limit (abstract-level if above 10 %). An empty R-3 means a second source, then stop-and-ask (l.1098-1101) | **R** |
| M12 nuisance propagation | §4.9 l.1233-1237; COM B6-c l.114 | Both sentences are present: the shift is measured at the deepest rung with counts and carried with s_tot; for bounded terms the nuisance acts through ln H and the conditionals | **R** |
| M15 closure statistics | §4.0 point 4 l.321-363; script [11] | Cap (c), INVESTIGATE band for (a) and K = 10 fixed (l.339-341). Per-test FAIL at s_model = 0 re-derived analytically: 0.005 (outright, \|z\| > 2.807) + 0.045 × 0.005 = 0.52 %, equal to l.349. Family rates as in the script. The new family of ceiling tests is not in the rates (F2, a new item, not this residual) | **R** |
| M24 Herwig | §11.5 l.2366-2373 | Dated commitment: install attempt on days 0–5, one source-build retry, then R-19 | **R** |
| M26 background list | §2 l.190-208; COM B1-g | Premise corrected and the sources checked by me: `normalise.py` l.84-110 has 'HS vertex only' for γ/V⁰/PV pair/looper and 'HS + 200 x min-bias' for DIF/NI; `gen_d123.py` l.21-23; `s4cp.py` l.110-113 draws the vertex from the beam spot. Truth-attributed test with a factor-2 rule; expected 2,085/1,017/25/13 = 4,000 × 1.57 × (166, 81, 2, 1)/500 ✓ | **R** |
| M25 residual | COM B4-c l.106 | "R06 (and R07 where evaluable)" | **R** |

### 1b. N1–N18

| # | v3 location | my check | status |
|---|---|---|---|
| N1 ceiling H | §4.4 points 3–4 l.648-712; §4.0 point 6 l.374-387 | (a) f_k on subsets of own hits (l.656-671), with the completeness argument. (b) k_IP + k_2S, and the width at the counting rungs (l.658-663). (c) One-sided exact test, FAIL at p < 0.001, with INVESTIGATE (l.676-685); substitution re-derived, 8 counts against an expectation of 2 give p ≈ 0.001. (d) Completeness test with c_mix (l.686-698). The arbiter's sum rule is replaced by a direct truth count of the mixed class, which the FR §2 justifies; I accept it. (e) FAIL by direction (l.374-382). **Open:** the ceiling test on the four gun sub-topologies has no defined H sample and no consequence (F3); the ceiling-test family is not in the false-fail rates (F2) | **P** → F2, F3 |
| N2 MUST NOT TESTED / D4 | §4.7 l.1133-1143; §4.4 l.825-831; Q3 and annex l.2480-2531; §11.7 rules 3–4 | W(τ_h) is supplied, and so are W(τ_ℓ) and tt̄ 1ℓ (script: 31.0 expected each in the test half). NI uses a rung split (92/120/378 at R05 = 2 × v1's 46/60/189 per 500 ✓). The dated rule with 10², 10–10² and < 10 is at l.2441-2444. **Open:** Q3 omits the NOT TESTED routes that v3 itself creates (F1) | **P** → F1 |
| N3 "target met" | §4.11 point 3 l.1384-1402; §0 l.58-60; COM TG-1 | Three-part reading; one σ_ln (total), the other renamed "count width w_m" (l.1384-1385); expected reading stated in §0, §4.11 and Q2 | **R** |
| N4 (a) against (c); rates | §4.0 point 4 l.321-363; Df-2 l.2511 | Cap, INVESTIGATE, K = 10 and rates at the declared widths, all reproduced by the script. F is unchanged. The re-test threshold moved from v2's p′ > 0.05 (v2 l.319) to p′ ≥ 0.05/K. I computed the false PASS: 0.584 → 0.622 at \|ln r_true\| = ln F and 0.053 → 0.059 at 1.5 ln F. That is legitimate, not a loosening that cannot fail (C1) | **R** (C1; F2 is new) |
| N5 widths | §4.0 point 7; script [12] | As M4. The reviewers' numbers are reproduced (script [12]). Row error: F4 | **P** → F4 |
| N6 censoring, T1 gaps | l.444-447, l.1319-1324, l.1374-1378, T1-c (v) l.1473, T1-h l.1497-1502 | min(φ₀e^θ, 1) as a bound in the fit and in the draws; B_t = N_t·c_mix·min(P, H) (l.710); μ grid and log-linear interpolation; T1-h λ = m + 1 with m′ redrawn | **R** |
| N7 projection | §0 l.39-62; Table 4.4c l.778-809; Q2 | max(floor, N_t·H) plus the EST pile-up term at R08–R14 (88–148 / 5.0–8.5 / 0.48–0.81, script [9b]). Reach per outcome, bracket, 3.7–4.7 decades, R07-direct 1.6×10⁵ (2.98×10⁴ + 6.51×10⁷/500 = 1.6×10⁵ ✓). The one-bin check gives 24.1. Note: only the Z(νν) ceiling is varied (C3) | **R** (C3) |
| N8 one route per origin | §2 l.158-178; Table 4.4a; §4.7 point 3 | Recomputed the floor with my own code (M_t ∝ √(N_t/c_t), 665 CPU-h): **11.72 events**, per-term floors equal to Table 4.4a. Accounting: the 12 SM N_t sum to 4.088×10⁷ = N_trig (`bsum_wp.json` → `n_trig.breakdown`), so no triggered event is lost; DIF/NI exist only as Geant4 vertices (Fatras decays and hadronic physics off, B1-d), so there is no overlap with B4 or B2. 45.3 − 18.4 − 4.7 = 22.2 is the floor without the double count. The rest of the fall to 11.7 comes from the 40 % of the pool that the PV-pair proxy used to take, now re-allocated. The route check has a fallback rule (l.174-178). No double counting and no dropped term | **R** |
| N9 secondaries | §2 l.190-208 | As M26 | **R** |
| N10 "estimate" | l.1386-1392; §4.12 rule 7 l.1565-1572 | m ≥ 4 (sd ln λ of Gamma(5) = √ψ′(5) = 0.47 ≤ 0.5 ✓) and PASS; "low count" label; estimate-only selection; monotone prior reported | **R** |
| N11 π_k correlations | l.700-707 | Correlated occupancy model; per-k comparison with a cap rule. Wording conflict on which overlays (C4) | **R** (C4) |
| N12 envelope | §11.2 l.2272-2284; §11.6; Q4 | Conditional table; every draw is a reported overrun; envelope option in Q4. A new inconsistency for the day-15 reserve: F7 | **R** (F7 is new) |
| N13 retrieval fallbacks | §4.7 l.1098-1101; §6.4 l.1988-1994; Df-7 | Deadlines: R-2 and R-3 by day 5 (stricter than the arbiter's day 15); R-7 and R-15…R-18 by day 15; R-12 and R-14 by day 17 | **R** |
| N14 D7 reading | §4.17 l.1848-1852; Q5 l.2498-2504 | Posed as a question with a default and its cost (+47 CPU-h and +1.8 days; script: 312 CPU-h / 174 = 1.79 days ✓). **The premise "which no analysis choice influences" is inaccurate** (F6) | **GA, premise to correct** → F6 |
| N15 order of A | §4.1 l.567-571; §4.13 l.1662; §11.3 l.2310 | R-3 → MET model (day 10) → threshold → A and m_mig once (day 12) → generator cut → string propagation on days 12–19 | **R** |
| N16 time tag | §4.6 l.1033-1052 | Prompt, truth-attributed population; 5.77×10⁵ = 10,000 × 19.52 + 11,250 × 12.93 + 23,880 × 6.857 + 7,662 × 9.534 ✓; credit only at the deepest tested edge, with no extrapolation in t_cut | **R** |
| N17 overlay sourcing | l.811-824; §4.17 rows 19 and 25 | Disjoint stream `prod.c0.dif.tst`; 2×10⁶ × (11.5 + 12.2) ms = 13.2 CPU-h ✓; correlation of the derivation overlays with the pool inside the joint bootstrap | **R** |
| N18 Phase 3 staffing | §11.1 l.2204; §11.3 l.2310, l.2326-2330 | Three channels for 12 days (36 channel-days, the lower end of PLAN's 35–50, stated as the largest schedule risk); prototypes in 4a; `ORCHESTRATOR_STATE.md` l.20 reads "at most 3 at a time" ✓ | **R** |

**Counts:** of the seven M residuals, 5 are R and 2 are P (M4, M5); the M25 residual is also R. Of N1–N18, **14 are
R, 3 are P (N1, N2, N5) and 1 is GA (N14)**: posed correctly, but with an inaccurate premise.

### 1c. The arbiter's rulings on simplifications and additions (verdict §5)

| ruling | v3 | my check | adopted as ruled? |
|---|---|---|---|
| C-1 toys parametrised in f_T, exact-toy check, conditional draw | §4.11 point 5 l.1441-1451; Df-8 | 5 × 11 × 8 × 652 s = 79.7 and 3 × 11 × 8 × 652 s = 47.8; checks 21.7 + 13.0. Saving = 318.8 − 162.3 = 156.5. **The departure from −191 is justified**: the verdict's figure did not cost the checks (191 − 34.7 = 156). Conditional ≤ 236 = (145 − 22) + 174 − (48 + 13): pass-1 check toys reused, pass-2 parametrised toys not run ✓. T1-i reworded ✓ | yes |
| C-3 part: signal road on all 10,000 Z(νν); rotation inline | §4.8 l.1166-1180 | ✓; lever (iii) (−137) only as a Q4 option (l.1195-1197, l.2382-2383) | yes |
| N8: freed CPU stays in the pool | Table 4.4a | 665 CPU-h = v2's 600 + 65 (Geant4 now inside); allocation rerun ✓ | yes |
| C-5 PREREG in Phase 3; note drafted in 4a | §11.3 | −5 days (Phase 2 7 → 5, Phase 5 7 → 4) | yes |
| C-4/P-C8 staging by the day-15 rule | §11.7 rule 3 | ✓, 156 CPU-h reserve | yes (see F7) |
| C-2 overlays only where the test is evaluable | §4.4 | After N8, γ/V⁰/prompt pairs are no longer terms. Their enriched overlays were dropped and the 1,000 unbiased events per sub-topology kept for N1, as the ruling required. 42,000 → 17,500 events (2,000 + 2,000 + 4,000 + 1,000 + 3 × 1,500 + 4 × 1,000 = 17,500 ✓). This goes beyond "staging", but the ruling's condition (terms accepted at H under Q3) no longer applies to non-terms. Justified | yes |
| Not adopted: N C-11 | l.866-870 | composition variation kept (52 CPU-h, inside B1) ✓ | yes |
| Addition N1 tests ≈ 0 | — | re-analysis; no paired pile-up-only finder pass (FR: the 26 CPU-h saved, mixed counted by truth as an upper value) | yes |
| Addition: pilot for N_t·H, +29 CPU-h | §4.4 point 5 l.728-729 | 2.3×10⁶ Z(νν) × 45 ms = 28.8 CPU-h. The verdict's "10⁷ events" assumed 11.5 ms PV-pair guns. After N8 the largest term is Z(νν) at 45 ms, so the same CPU buys 2.3×10⁶ events (one count = 2.51×10⁷/2.3×10⁶ = 10.9 events). **Departure justified** | yes |
| Addition: W(τ_h) +61 | §4.7 l.1133-1138 | **+65**: sized for an expected 31 (P(≥ 24) = 0.92) instead of 24 (P = 0.53). Justified | yes |
| tt̄ 1ℓ ≈ +115, W(τ_ℓ) ≈ +210: supply or Q3 | §4.7; Q3 annex | Supplied at +153 and +40. **I checked the denominator correction myself.** `background.json` → `sm.Wtau_l.n_class_events` = 375 and `Wtau_h` = 1,625. R06 effective counts are 3.035 and 8.957 (`rows[R06].factors[0].N`). `sm_regen.json`: v1's W(τ_ℓ) class events are the 375 leptonic events of a 1,000-event inclusive `Wtaunu_j` sample, next to a 1,000-event forced-hadronic `Wtauhnu_j`. So 3.04/375 per τ_ℓ event is right, and the verdict's +210 (≈ 3.04/2,000) was wrong. **Departure justified by the source.** The generation mode is not stated (C2); the cost hardly depends on it | yes |
| Addition N5 crossing rungs ≈ 5 + storage | l.414-417; §11.4 | 5 CPU-h; 0.9 GB = 49.72 × 96,000 × 64 B × 3 ✓ | yes |
| N9 inside the 17.5 CPU-h sample | §2 | 1,000 × (60.4 + 2.7) s = 17.5 ✓ | yes |
| N16 0; N17 costed line | — | ✓ | yes |
| Checkpoint 1 at day 5 instead of day 7 | §11.3 l.2309, §11.6 l.2408 | This follows from C-5 (Phase 2 now lasts 5 days). The verdict's "day 7" was written for the 7-day Phase 2. Justified. Its tightness is C13 | yes |

**The fixer adopted only what was ruled in.** The four numerical departures (+65/+40/+153 against +61/+210/+115; −156
against −191; 2.3×10⁶ events against 10⁷; day 5 against day 7) each trace to a source or an arithmetic correction that I
reproduced.

---

## Part 2. New findings

### Category A
None.

### Category B

**F1 (B). Q3, the brief-D4 question, does not cover every route by which v3 makes a MUST closure NOT TESTED.**
*Location:* §4.0 point 6 l.383-387 ("For a MUST criterion this is an exception to brief D4 that only the user grants:
the terms concerned are listed in Q3") against Q3 l.2480-2487 and its annex l.2519-2531, §11.7 rule 2 l.2436-2437,
§4.6 l.1019-1020, and FR §6 l.237.
*Evidence:* v3 creates at least four NOT TESTED routes for MUST criteria that Q3 neither names nor gives a default:
1. **The cap route.** An estimator whose development r.m.s. exceeds ln F/3 is "not submitted" (l.326-328; COM B2-b
   "not submitted if its development r.m.s. is above 0.135"). Day-15 rule 2 decides this without asking the user,
   except when both pile-up estimators miss their cap.
2. **The fluctuation route.** The four "supplied" terms (DIF, W(τ_h), W(τ_ℓ), tt̄ 1ℓ) are each sized for
   P(evaluable) = 0.92 (script [11]). So P(at least one ends NOT TESTED) = 1 − 0.92⁴ = **0.28**, before the 33–57 %
   errors on v1's rates. Q3 (a) calls them "already supplied". The FR self-audit itself writes "NOT TESTED 8 %" and
   "≥ 8 %" (FR l.189, l.211).
3. **B3-a/b/d** (MUST): "unknown until the pool exists … NOT TESTED and earns no credit" (FR l.205). The same holds
   for B3-c at the nominal edge (58 expected against 55 needed) and for B4-e (FR l.214).
4. **B2-c**: "expected NOT EVALUABLE" at most deep rungs (l.956).

Under v3's own rule each of these is an exception that only the user grants. The FR concludes "No other MUST closure
is planned to stay untested" (FR l.237), which contradicts its own rows. B2-c and B3 earn "no credit", which is
conservative. Still, D4 is about statistics, and the arbiter ruled that NOT TESTED for a MUST criterion "is not a
default" (verdict N2).
*Fixed looks like:* widen Q3 to "every MUST closure criterion that ends NOT TESTED / NOT EVALUABLE / not submitted at
the planned statistics or by the day-15 rules". Add annex rows for routes 1–4, each with its expected probability, the
cost of compliance where it is defined (for example the B3-c nominal edge, or re-sizing the four terms at day 15 for
P(evaluable) = 0.99), and a default. The default can be the present one (no credit, term at H after the ceiling test,
user informed in `STATUS.md`). Align §4.0 point 6, §11.7 rule 2 and FR §6.
*Effort:* 30–45 min of text; no CPU.

**F2 (B). The eligibility false-fail rate shown to the user leaves out the ceiling tests, which also remove
selections.**
*Location:* §4.0 point 4 table l.347-353 ("at least one FAIL that removes a selection: 2.1/2.2/4.2 %"); §4.12 rule 1
l.1542-1543 ("2–4 %"); Df-2 l.2511; K = 10 (l.339-341) against the ceiling-test FAIL rule l.381-382 and l.1532-1533.
*Evidence:* a ceiling-test FAIL makes a selection with that term leading not eligible. The test runs "at every rung with
attributed direct counts" (l.676-682): DIF R04–R07 (4), NI R04–R05 × 3 (6), 12 hard-scatter terms R04–R06 (36), γ and
V⁰ R04–R06 (6), prompt pairs R02–R04 (3). That is about 55 rung-tests, with no family rule. At the boundary P = H the
false fail is 0.35 % per test (script [11]). The boundary is realistic at R02–R04: v3 l.708-709 notes that P → H when
pile-up fills the missing layers, and v1's pile-up planes pass R05 at 49.7 per trial. My computation:
1 − 0.9965ⁿ = **5.5 %** for 16 (one test per term), **10 %** for 30 and **17.5 %** for 55 independent tests (nesting
lowers the last figure). This is the N4 pattern again: a rate shown to the user that is right for a subset.
*Fixed looks like:* one ceiling verdict per term (a combined test over its rungs, or the deepest evaluable rung), a
family rule (Bonferroni over the terms, or the outright-FAIL threshold set for a family-wise 5 %), and the family added to
the eligibility rates in §4.0, §4.12 rule 1 and Df-2. Script [11] recomputed.
*Effort:* about 1 h (script and text).

**F3 (B). The ceiling test on the four gun sub-topologies is undefined.**
*Location:* l.633-635, l.681-682 ("the enriched sub-topologies on their 1,000 unbiased events"), Table 4.4b l.840-842,
§4.17 row 19.
*Evidence:* after N8, γ, V⁰, prompt pairs and loopers are not terms, and the pool holds no no-pile-up sample of these
gun topologies (rows 17 and 18 cover DIF/NI and the SM processes only). The test compares "N_d attributed counts …
against m_H ceiling counts in M no-pile-up events" with an exact test for two independent Poisson counts (l.677-679).
For the sub-topologies, the only H is that of the same 1,000 events' own no-pile-up states. That makes the comparison
paired, so the independent-Poisson test is the wrong test, and the paired version is the leak count of the
completeness test. The text also does not say which term's selections a sub-topology FAIL removes. (The same line
calls the samples "enriched" and "unbiased".)
*Fixed looks like:* either (i) define the H sample (a small no-pile-up gun sample per sub-topology, costed), the paired
test, and the term whose eligibility a FAIL affects (the B4 terms, by origin); or (ii) drop the ceiling test for the
sub-topologies and keep them as completeness and diagnostic populations, which is what their proxy kinematics
(minimum-bias pairs, verdict §2) supports.
*Effort:* 20 min.

**F4 (B). The planning width "promotion π_k tested at R06–R07" applies to no term in the expected case, and is
understated by ×1.9.**
*Location:* table l.432-433; §4.12 l.1586-1587 ("a promotion factor to R11 without and to R20 with a 2S crossing
test"); script [12].
*Evidence:* DIF reaches R07 only "if the enrichment is ≥ 4" (Table 4.4b l.838; the enrichment is unknown and every
number assumes G = 1). The B4-c terms are tested at "R06 (and R07 where evaluable)". At 31 counts at R06, R07 holds
about 1–3, so R06 alone is expected. NI has R05 only. With one evaluable width rung (n = 1: b̂ = 0, σ_b = b₀ = ln 2),
s_model = 0.231 and d_in = 2, I get **s_tot = 1.41 at R08–R11, 2.51 at R14, and 1.42 at R14 with a 2S crossing
PASS**, against 0.73 / 2.20 / 0.77 in the table. By v3's own threshold ("worth little" above about 0.8, l.1014-1015)
a promotion factor is then of little use from R08 on. This is the N5 defect class: widths understated against the
document's rule.
*Fixed looks like:* replace the row with "π_k tested at R06 only (expected for DIF at G < 4 and for every B4 term)"
and keep "R06–R07" as the conditional case. Correct l.1586-1587 and any reading that rests on it.
*Effort:* 20 min.

**F5 (B). The coverage criteria of T1 (MUST) false-fail a correct likelihood with probability 15–48 %, and their
consequence blocks every quoted limit.**
*Location:* T1-c (iii) l.1467-1471; T1-h l.1497-1502; "Fail: T1 is not used for a quoted limit until fixed" l.1505;
the analytic coverage of the convention, 0.945–0.956 at κ = 1 (l.1424-1429).
*Evidence:* each check is "≥ 0.93 of 500", per-test false fail 0.0196 at a true coverage of 0.95 (script [13], and
my binomial sum). T1-c (iii) runs 4 values of λ × 2 points = 8 checks, and T1-h adds 2. My computation: family false
fail **14.7 % (8) / 18 % (10)** at a true coverage of 0.95. At 0.945, which is v3's own analytic value at κ = 1 and
λ = 0.5 for this convention, it is **6.3 % per test and 40 % (8) / 48 % (10)**; at 0.94 it is 73 %. v3 states the
tolerance per test only (l.1428-1429). It is also unclear whether "500 pseudo-experiments" means per (point, λ) or in
total. This is the family-wise problem that N4 fixed for the closure battery, here on a T1 MUST item.
*Fixed looks like:* state the family. Set the per-check threshold for a family-wise size of about 5 %, or pool the λ
values into one coverage test per point. Compare with the convention's computed coverage at the workspace's κ (not
with 0.95), and add an INVESTIGATE band like §4.0. Script [13] recomputed; COM T1-c/T1-h aligned.
*Effort:* 30 min.

**F6 (B). The Q5 premise is inaccurate.**
*Location:* Q5 l.2498 ("which no analysis choice influences"); §4.17 l.1849-1850 ("whose content does not depend on
any analysis choice").
*Evidence:* sample 10 (Stage-3 string propagation) contains only "events inside the counting acceptance … and accepted
by A" (SD10, l.1637-1639). A uses the MET model and the offline threshold decision (§4.1 order, steps 2–4,
l.567-570), and the generator cut is set from m_mig (step 5, l.1662-1665). These are pre-registered,
selection-independent choices, but they are analysis choices. The user is asked to relax a fixed decision (brief D7,
"before any v2 production sample exists") on a premise the strategy itself contradicts. The question and its default
are otherwise correct.
*Fixed looks like:* "whose content depends on the MET model, the trigger threshold and the generator-cut decision,
all frozen by day 12 before the propagation, but on no plane-selection choice and on no signal efficiency at any T2
candidate." Same in §4.17.
*Effort:* 10 min.

**F7 (B). The default plan spends 156 CPU-h outside the figure the user approves.**
*Location:* Q2 l.2476 (the 156 CPU-h "are spent at day 15"); §11.2 l.2272-2277 ("None of these is inside the approved
figure … day-15 redirection reserve (the only one approved in advance, with Q2) 156"); Q4 l.2489-2494 (approve 4,378;
threshold 5,691); script [5] ("not in the totals").
*Evidence:* if Q2 and Q4 are both answered with their defaults, the plan spends 4,378 + 156 = 4,534 CPU-h. It then
reports the planned 156 as an "overrun", and the stop threshold stays keyed to 4,378. The headline total is 156 lower
than the default spend, which is the N12 pattern (an approval the strategy expects to exceed). It also tightens the
stated risk: "if the guesses are low by a factor 2, the projection is about 5,750" (l.2413) becomes about 5,906.
*Fixed looks like:* either put the reserve into the proposed figure (4,534 CPU-h; threshold 1.3 × 4,534 = 5,894) or
state in Q4 that the approved schedule is "4,378 + the 156 CPU-h reserve of Q2". Script [4]/[6] and §0 updated to
match.
*Effort:* 15 min.

### Category C

- **C1. The re-test threshold p′ ≥ 0.05/K** (l.336; COM l.19). It departs from v2 (p′ > 0.05, v2 l.319) and from
  conventions check 1 ("passes at p > 0.05"). It is legitimate, because δ is shared between the test and the re-test
  (FR §2 N4). Its price, which I computed (one rung, σ_tot at the limit, s_model at the cap), is P(final PASS) =
  0.622 against 0.584 under v2's re-test at \|ln r_true\| = ln F; 0.260 against 0.233 at 1.25 ln F; 0.059 against
  0.053 at 1.5 ln F. Without any re-test it would be 0.41 / 0.16 / 0.04. The criterion can still fail (94 % at
  1.5 ln F), so it is not loosened until it cannot fail. Say this in §5.2 row 1 and in Df-2.
- **C2. W(τ_ℓ) generation mode.** State whether the 7,662 W(τ_ℓ) and 11,250 W(τ_h) events are forced-decay samples
  or the classes of an inclusive W(τν) sample (v1 had both kinds: `sm_regen.json`). The cost is nearly the same
  either way: 20,430 inclusive events give 7,662 τ_ℓ and about 12,770 τ_h events, about 1,500 events (≈ 11 CPU-h)
  more than the two sized samples together.
- **C3. Only the Z(νν) ceiling is varied (Table 4.4c, Q2).** If the other SM processes have a similar H per triggered
  event, their ceilings scale with N_trig rather than N_Z (×1.63). My rough estimate, using the ratio of hybrid to
  fixed-B s₉₅ from Table 4.4c: reach about 695 / 630 / 540 GeV instead of 723 / 661 / 575 at m_H = 10 / 30 / 100. Add
  one sentence or one row, and say that the Z-only rows are an upper edge of the reach when H counts.
- **C4. Contradiction on which overlays give s_model.** COM B1-f and l.703-705 put the per-k comparison "on the
  derivation overlays", which are sample 19, produced in 4a after the freeze. l.703 ("Phase 3, rule fixed now"),
  decision point 2 and the rule that s_model is fixed before the freeze require pre-freeze overlays. Those can only be
  the pilot's 1,000 near-pass overlays (sample 11). Name sample 11.
- **C5. NI rates.** §4.4 point 6 quotes v1's 0.098 / 0.124 [V], and Table 4.4a's caption says "rates as in point 6".
  The script uses 0.11 × 0.22 (D2, [U]) for all three radii (`strategy_budget.py` RATE), which gives equal N_t =
  9.89×10⁵. The effect on the sum is below 0.05 events. Align the two.
- **C6. Geant4 vertex yield per slab.** c_t for NI uses the all-tracker inelastic yield of 4.2 % per gun (FEAS_B
  l.192-194) for a vertex at one radius. If about a sixth of the vertices fall in a given slab, c_NI ≈ 31 ms and the
  summed floor becomes 12.5 instead of 11.7 (my recomputation). It is D provenance; name it in the unit-cost table of
  §11.2.
- **C7.** COM T1-c lists the labels "estimate / bound / no credit" against the four labels of v3 l.1386-1392 (low
  count is missing).
- **C8.** l.1848-1849 says that samples 1–13 enter no "verdict or quoted number" except 7 and 10. That is false for
  the C1 samples 1–6 (the C1 verdict, the pull figure) and for sample 12 (s_model enters the likelihood). Say
  "no closure verdict and no limit".
- **C9. C2-c family.** 4 rung families × 2 densities at \|z\| < 2: a converged finder "fails" in 1 − 0.9545⁸ = **31 %**
  of the cases, and the paper would then state "seed threshold not converged". Use a combined χ² or Bonferroni.
- **C10.** The pilot's 10⁶ unbiased no-pile-up DIF and NI events are costed at 11.5 ms (12.8 CPU-h). They need the
  Geant4 vertices too (23.7 and 14.7 ms per event in the pool): about +6 CPU-h.
- **C11.** The A/f₂₀₀/m_mig exception (BL-1), which v3 calls "a second, selection-independent exception" (l.558), is
  not mentioned anywhere in the Gate-A package. The cycle-1 arbiter ruled that declaration is enough (Dagmar l.129).
  One line in §12.3 would inform the user.
- **C12. Length.** v3 is 2,674 lines (shortening was asked for). §12.1 with its annex is probably over the 3-page
  limit of verdict §6. The Q3 annex's last row says "hundreds per 1,000 events" at R04–R05, but SM hard-scatter
  candidates are 6.8–19.5 per event at R04 (`background.json` → `sm.<p>.rows[R04].P_per_event`), so thousands.
- **C13. Day-5 checkpoint and Phase 2.** Phase 2 needs 500 CPU-h, which is 4.3 days at 116 per day out of 5. Decision
  point 1 depends serially on C1 (198) and then C2 (81, which needs C1 dumps and new V4-5 code). The Geant4-vertex (96,
  D), spectra/variation (67, G) and allowance (442, G) costs are not measurable by day 5. State which G and D costs
  checkpoint 1 can and cannot fix, so that the user's "may well happen" (Q4) refers to checkpoint 2 as well.

---

## Spot checks (VERIFIED numbers, emphasis on v3-new)

| # | v3 claim | source opened | result |
|---|---|---|---|
| 1 | W(τ_h) 8.96 in 1,625; W(τ_ℓ) 3.04 in 375; Z 32.3, tt̄ 5.19 in 2,000 (l.1134-1135) | `AN1/background.json` → `sm.<p>.n_class_events`, `rows[R06].factors[0].N` | 1625 / 8.957; 375 / 3.035; 2000 / 32.300; 2000 / 5.193 ✓ |
| 2 | W(τ_ℓ) class from an inclusive sample (my check of the denominator) | `sm_regen.json` rows by `tau` | Wtaunu_j: 625 had + 375 lep; Wtauhnu_j: 1,000 had ✓ |
| 3 | DIF rate 1.569–1.594 per process (l.192-193) | `cprime.dif.rate.per_process` | 1.5687 (WZ) to 1.5945 (tt̄ 2ℓ); Z 1.5691 ✓ (v3's lower end is Z, not the minimum: C-level, negligible) |
| 4 | route check γ 0.231, V⁰ 0.026 for Z(νν) (l.176-177) | `cprime.gamma/v0.rate.per_process.Znunu_j` | 0.2306, 0.02605 ✓ |
| 5 | PV-pair rate 30.3 (l.158) | `cprime.pvpair.rate.value` | 30.31 (max over processes; Z 25.7) ✓ |
| 6 | per 500: DIF 166/81, NI22 127/46, γ 153/86/13/2, V⁰ 859/358/6/0, PV pair 24 (R02), 1 (R04) (Table 4.4b) | `cprime.<t>.rows[].factors` | ✓ (R06/R07 entries are conditional numerators, e.g. γ 2/13, V⁰ 6/358, PV pair 1/24) |
| 7 | N_trig 4.0848×10⁷ and breakdown (Table 4.4a) | `bsum_wp.json` → `n_trig` | 40,848,448; Z 2.5079×10⁷, W(τ_h) 5.407×10⁶, tW 2.593×10⁵, ZZ 1.045×10⁵ ✓ |
| 8 | Z(νν) HS candidates 19.52 / 4.51 / 0.0162 (l.487) | `sm.Znunu_j.rows[R04/R05/R06].factors[0].used` | 19.516 / 4.509 / 0.01615 ✓ (P_per_event after f_CKF: 19.48 / 4.50 / 0.01595) |
| 9 | proxy share 0.147 at R04, 0.445 at R09 (l.1065-1066) | `sm._proxy_fraction_of_B_SM` | 0.1472, 0.4452 ✓ |
| 10 | 'HS vertex only' / 'HS + 200 × min-bias' (l.160, l.191) | `S4/analysis/normalise.py` l.84-110 | present ✓ |
| 11 | v1 places the pile-up vertex at the PV (l.194) | `TT/acts/stage4/code/s4cp.py` l.110-113 | vertex from the beam-spot draw ✓ |
| 12 | gun docstring (l.192) | `gen_d123.py` l.21-23 | "NI parents and DIF from the HS event + Poisson(200) minimum-bias" ✓ |
| 13 | min B₈₄ 1.2346×10⁶ (l.37) | `STAGE4_SUMMARY.json` → `ladder.SR-G.min_B84` | 1,234,586 ✓ |
| 14 | μ₉₅ 1.2458×10⁷ events before selection (l.1458) | `AN1/limits.json` → `points["A2\|F\|200\|1.5\|BM"].expected_toys.median` | 12,458,208 ✓ |
| 15 | Geant4 0.134 ms per gun; 1.1 % decays, 4.2 % inelastic (l.740-741) | FEAS_B l.192-194 | ✓ |
| 16 | Z(νν) shower 23.4 ms; 10-track gun 14.1 ms; no-PU 11.5 ms (Table 4.0) | FEAS_B l.117; FEAS_A l.235, l.234 | 23.41; 14.1; 11.5 ✓ |
| 17 | MG5 12.21 pb against 14.6 pb, ratio 0.84 (l.1076-1077) | FEAS_B l.83 | ✓ |
| 18 | at most three agents (l.2204) | `ORCHESTRATOR_STATE.md` l.20 | "at most 3 at a time" ✓ |
| 19 | summed floor 11.7, DIF 2.93, NI 0.28 each, Z 2.51 (Table 4.4a) | my own allocation code | 11.72; 2.934; 0.285; 2.510 ✓ |
| 20 | occupancy widths 0.43 / 0.59 / 1.29 / 2.47 / 3.67 (l.430) | my formula | 0.427 / 0.589 / 1.29 / 2.47 / 3.67 ✓ |
| 21 | NI test 92 / 120 / 378 at R05 per 1,000 (l.828) | 2 × (46, 60, 189) | ✓ |
| 22 | 5.77×10⁵ prompt candidates (l.1036) | arithmetic from rows | 577,458 ✓ |
| 23 | Stop rules quoted exactly (l.2391-2400) | `prompt.md` l.79, l.341-348 | word for word ✓ |

**Budget rerun.** `python3 -I phase1_strategy/src/strategy_budget.py` (exit 0): MUST **3,945**, reduced **4,378**,
full **4,891** CPU-h; calendar **56.6** days (54.1 / 59.6); threshold **5,691** (5,128 / 6,359; envelope 8,467);
contingency **2,135** = 69 + 695 + 1,371; storage **417 GB**; floor **11.7**. All of these match v3 §0, §11.2, §11.3,
§11.4, §11.6, Q2–Q4 and Df-1…Df-8. I also checked by hand:
- the §11.2 phase sums: B1 3/4a = 77.5/417.8; B4 4a = 1,052; Phase 3 = 573.2;
- B4 hit level 74,792 events × 25.2 s = 524;
- the overlays 17,500;
- [DP1] 358 and [DP2] 155 saved;
- "46 days" = 42 − 8 + 12.1;
- doubled G costs: 4,378 + 1,371 = 5,749.

**Stale-value grep** (v3 and COM) for 2,950, 3,275, 3,798, 3,968, 4,401, 4,915, 5,722, 45.3, 55.5, 57.9, 1,989,
42,000, "day 7", "K = 12", "600 CPU-h", 0.029, 0.097, 2.44, 495–662, 1,261, "45 events", GA-n, 319, 191, 210 and 115.
Hits occur only in explicit comparisons: l.2252, 2259, 2270, 2594, 2603, 2647, 2666-2667, and COM l.30 and l.60. **No
stale value is used as current.**

---

## Contradictions (both locations)

| # | quantity | location 1 | location 2 | finding |
|---|---|---|---|---|
| K1 | which MUST NOT TESTED outcomes need the user | §4.0 point 6 l.385-387 ("only the user grants … listed in Q3") | Q3 annex l.2519-2531; §11.7 rule 2; FR l.237 (versus FR l.189, 205, 211, 214) | F1 |
| K2 | the π_k width at R08 | table l.432 (0.73, "tested at R06–R07") | Table 4.4b l.838 (DIF at R07 only if the enrichment is ≥ 4); B4-c l.1132 (R06) | F4 |
| K3 | the eligibility false-fail rate | §4.0 l.352, §4.12 l.1542, Df-2 (2–4 %) | the ceiling-test FAIL rule l.381, l.1532 (not in the family) | F2 |
| K4 | content of sample 10 | Q5 l.2498, §4.17 l.1850 ("no analysis choice") | §4.1 order l.567-571; SD10 l.1637-1639 | F6 |
| K5 | the approved spend | Q4 l.2489 (4,378); §11.2 l.2272 ("none inside") | Q2 l.2476 (156 spent at day 15 by default) | F7 |
| K6 | overlays for the per-k comparison | COM B1-f; l.703 ("derivation overlays") | l.703 ("Phase 3"); §4.17 row 19 (4a); row 11 (pilot) | C4 |
| K7 | NI rates | l.732-733 (0.098 / 0.124) | Table 4.4a (equal N_t, script 0.11 × 0.22) | C5 |
| K8 | term labels | v3 l.1386-1392 (four) | COM T1-c (three) | C7 |
| K9 | pre-hash samples in verdicts | l.1848-1849 | §4.1 (C1 verdict); §4.0 point 4 (c) (s_model from development) | C8 |
| K10 | sub-topology samples | l.681 ("enriched … unbiased") | Table 4.4b l.840-842 ("1,000 unbiased each") | F3 |
| K11 | counts in the ceiling test at R04–R05 | Q3 annex l.2530 ("hundreds per 1,000") | `background.json` R04 per event 6.8–19.5 | C12 |

I found no conflict between the per-item criteria of §4, the PREREG outline (§8) and COM for C1, B1-a/f/g, B2-a…g,
B3-c, B4-c, T1-b/h/i, T2-a/h, S1-a/f, TG-1 and ST-1. The COM header (l.14-21) states the §4.0 rule exactly.

---

## Conventions coverage (`conventions/search.md`) against v3 §5

| conventions row | v3 | assessment |
|---|---|---|
| CLs; q̃_μ; asymptotics only above about 5 events | §4.11 points 2, 5; T1-i | covered; every quoted limit toy-based ✓ |
| Signal injection 0/1/2/5 | T1-d | covered (multiples of μ₉₅^exp of each point, which is the sensible translation) ✓ |
| Blinding | STUDY OVERRIDES; §4.1 C1 tiers; BL-1 | covered (C11 for the Gate-A note) ✓ |
| Signal cross-section theory | §5.1; S2 | WI ✓ |
| Signal acceptance | §5.1; S2-c | WI ✓ |
| Signal shape | §5.1 (SR-T/SR-G migration) | WI, translated ✓ |
| ISR modelling | §5.1 (f₂₀₀, one nuisance) | WI ✓ |
| 4-fermion generator comparison | §5.1 (MET+jets, Pythia against MG5; no second generator for tt̄/dibosons, stated) | WI, translated, with a stated limitation ✓ |
| Background normalisation | §5.1 | WI ✓ |
| Background shape | §5.1 (N/A as written; closure widths in its place) | justified ✓ |
| qq̄(γ) modelling | §5.1; DP5 | WI, with an attempt first ✓ |
| MC statistics | §5.1; T1 auxiliary channels | WI ✓ |
| Detector simulation model | §5.1 (Fatras/Geant4; sourced sizes; robustness tests) | translated ✓ |
| Object calibration | §5.1 | WI ✓ |
| Beam energy | N/A, justified | ✓ |
| Luminosity | §5.1 (R-9; 300 fb⁻¹ also) | WI ✓ |
| PDF, pile-up (pp replacements) | §5.1 | WI ✓ |
| QCD scales | §5.1 | WI ✓ |
| Fragmentation | §5.1 (tune; string against cluster at generator level, DP5) | WI ✓ |
| Heavy flavour | §5.1 (inside B4 by the route rule; Phase-2 check, SY-14) | ✓ |
| Check 1: closure at p > 0.05 | §5.2 row 1; §4.0 | covered; the re-test at p′ ≥ 0.05/K departs from "p > 0.05" and is not stated in the row (C1) |
| Check 2: injection | T1-d | ✓ |
| Check 3: pulls and constraints | T1-e (per-nuisance reading on pseudo-data) | ✓ |
| Check 4: impact ranking | T1-f | ✓ |
| Check 5: GoF | N/A to data; closure χ² with alarm bands | ✓ |
| Check 6: LEE | N/A, justified | ✓ |
| Pitfalls: VR blind spot; transfer-factor instability; pruning; low-statistics asymptotics | §5.2 row 1; T1-f; §4.11 point 5 | ✓ |

The coverage is complete. The only gap is the unstated re-test threshold (C1).

---

## Blinding, Gate A and brief compliance

- **C1 sealed comparison.** The tiers are well defined: 4 open, 6 sealed. The sealed file is outside the tree and
  encrypted with an orchestrator-held key. Family z and global χ² are reported as PASS/FAIL only. The agent is
  dedicated, and opening early needs the user. The open R06 count at E 200 / 1.5 keV bounds R07 from above. v3
  declares that the open tier is part of the exception (l.530-533) ✓.
- **Q5 and brief D7.** Producing samples 7 and 10 before the hash conflicts literally with "before any v2 production
  sample exists". Putting it to the user is correct, and so are the default and the cost (+47 CPU-h, +1.8 days).
  The premise is not (F6).
- **Gate-A list.** Q1–Q5 can each be answered in one line, with a default, alternatives and costs. The costs match
  the script (Q1 14 CPU-h; Q2 +665 / 3.8 days and 5.9 events; Q3 ≈ 680 (100–1,230) / 3.9 days; Q4 thresholds; Q5).
  There are 8 defaults with costs, and the Df-2 rates (15 %/6 % at ln F/2.5; 1.08 at R14) match script [11]/[12].
  Missing: the routes of F1 and the reserve of F7. D9 (S4/S5) is handled through [DP4] in Q4 ✓. The brief's stop
  rules are quoted exactly ✓.
- **Brief D4.** Respected for the SHOULD items ([DP1]/[DP2] with the lost gain stated). For MUST items it is put to
  the user in Q3, but not completely (F1).
- **Nothing discarded has returned.** I grepped for ρ = 3 (only "is not", l.960), ×100 (none), cloud (only "no
  cloud"), Λ ≥ 15 keV (only as excluded), Open Data (none), pile-up scan (only "not", l.1207, l.1879) and endcap
  (outlook only). F = 1.5 and 2 are unchanged.

**Competing group.** With the same cluster, a competing group could hardly have more than v3 plans. The one thing it
would have is tested closures for the eight proxied processes, which v3 prices at about 680 CPU-h and puts to the
user. That is the right treatment.

---

## Verdict recommendation to the arbiter

No A items. Seven B items (F1–F7), each a text or script fix of 10–60 minutes with no new production. Once they are
fixed, I see no reason against PASS at the next check. F1 and F2 are the most important: both concern what the user
is told at Gate A about the D4 exception and about false eligibility losses.
