# Arbiter verdict — Phase 1 STRATEGY (quirks v2), review cycle 1

Arbiter: Dagmar, 2026-11-13 19:00. Role: `agents/arbiter.md` (prompt template followed in full).
Artifact: `phase1_strategy/outputs/STRATEGY_brigitte_2026-11-13_17-55.md` ("STR"), `COMMITMENTS.md` ("COM"),
`phase1_strategy/src/strategy_budget.py`.
Reviews: physics Casimir (P; 5 A, 12 B, 8 C), critical Celeste (K; 8 A, 16 B, 10 C), constructive Cosima
(N; 1 A, 16 B, 11 C), all 2026-11-13 18:20. No plot validator (Phase 1 has no figures, 06 §6.2).
Also read: `prompt.md` (brief) in full, `LOG.md`, `FRAMING.md`, `AGENT_RULES.md`, `CLAUDE.md`, `methodology/06-review.md`
§6.1–6.5.1 and §6.7, `03-phases.md` Phase 1, `conventions/search.md` (via the reviews' row-by-row tables, spot-checked).
Fact checks were made by me on the cited sources (JSON keys, digests, plan lines, feasibility reports); they are listed
in §2 and in the session log `logs/arbiter_dagmar_2026-11-13_19-00.md`. No sub-agents were spawned (AGENT_RULES).

**Verdict: ITERATE.** 35 merged findings: **11 Category A, 24 Category B**, plus the C list of §6. No ESCALATE: every
finding can be fixed by the strategy executor; the items that need the user are collected as Gate-A decisions (§5),
for which the fixer prepares options with costs and does not decide.

---

## 1. Overall assessment

The strategy is honest, carefully sourced and arithmetically reproducible (all three reviewers re-derived its
numbers; I re-checked the ones that decide findings). Its process design is sound: hashed pre-registration before
production, no scale-factor patches, failures reported as failures, toys primary, a Λ-independent hashed signal split.

It is not yet approvable because the statistical core does not yet do what the paper will claim:
1. the expected-limit construction can make zero-count terms vanish (M1), so the "estimated, not bounded" message
   could be produced by the treatment rather than by the physics;
2. the closure tests at R04–R07 are partly tautological (M3), several cannot be evaluated at the planned statistics
   (M5), and none of them controls the extrapolation over 2–13 rungs to the working selections (M4);
3. the planned no-PU samples leave zero-count floors of ≈ 141 events (PV pairs) and ≈ 47 events (SM) before credits
   (M6), and the strategy does not say so to the user;
4. several validation criteria pass by construction (M7, M8, M9);
5. a stop condition of the brief is quoted in a weaker form (M10), and the C1 blinding exception is under-disclosed by
   a factor of two (M2).

---

## 2. Facts settled by evidence (contradictions and fact-dependent findings)

| question | evidence | ruling |
|---|---|---|
| Are 3 or 6 of the ten C1 signal quantities efficiencies of v2 T2 candidates? (K-A2 vs STR l.292) | `STAGE4_SUMMARY.json` → `fallback_points`: `A2\|F\|200\|1.5\|BM` r_fb = `FB2&h>5&o>5`, k_adm 2, e_adm None, 9/200; `A2\|F\|200\|2\|BM` FB3, 10/200; `A2\|F\|500\|3\|BM` FB3, 11/200. T2 family F (STR l.669) is "FB(k_adm)" without dE/dx = exactly these. R07 is in family L (l.668). | **Six** (3 R07 + 3 FB). STR l.292 and COM C1-d are wrong. K-A2 stands. |
| Is S1 "×10" on the statistic that sets the limit? (K-B5) | `C12FC_v1/acceptance.json` finder_note: v1 ε over "every TEMPLATE-half … row"; D4 l.298: 180–200 template-half rows; PLAN l.371: "Ten times the rows … The best point now rests on 9 events of 200"; PLAN l.362-363 also asks for the opt/eval split. | v2's limit uses 1,000 rows = **×5**. The plan is ambiguous (×10 total is a defensible reading), so this is a statement plus a Gate-A option, not a breach. |
| Can B1-a/B1-b/B3/B4-c be evaluated at the planned statistics? (P-A5, K-A4) | D4 l.185-203 (per 500 events): PV pair 1/24 at R04, 0/24 at R06; V⁰ 6/358 at R06; DIF 81 → 2 → 1 at R05–R07; NI ≈ 0 beyond R05; loopers 0/10⁵. Scaled to STR l.392 sizes: PV pair ≈ 12 at R04, ≈ 0 at R05+; V⁰ ≈ 12 at R06. | **No** for 5 of 8 topologies under "N ≥ 20". This also violates brief D4: "A MUST item gets the statistics its acceptance criterion needs." |
| Is the T1-g self-consistency test tautological or expensive? (K-A6, N-B-14, P-C2) | If the median comes from the same ensemble → 50 % by construction. If each of 500 pseudo-experiments gets a toy limit: 500 × 2 points × 8 μ × 652 s = **1,449 CPU-h** (my arithmetic, STR unit costs l.204), absent from the script (its toy line is 174 CPU-h). | Either way defective; Category A. |
| Is the no-PU hard-scatter unit cost (15 ms) plausible? (K-B2) | FEAS_B l.117: Pythia shower alone 23.41 ms for Z(νν)+j; FEAS_A l.235: a 10-µ gun through Fatras 14.1 ms. | 15 ms is below the shower alone. 1.5×10⁷ × 45 ms = 187.5 CPU-h vs 62.5 [E]. |
| Capacity with the graphical-session caps (K-B4) | `LOG.md` 14:34: landau and schrodinger capped at 3 jobs. 5 × (11 × 9 + 13 × 10) + 48 × 10 = 1,625 slot-h/week; × 0.75 / 7 = 174/day; 2,249 / 174 = 12.9 production days (vs 11.3). | Confirmed. STR lists the cap among "losses" but its slot count uses 12. |
| Does a 4-week schedule need "production near 1,000 CPU-h"? (STR l.1155, K-B4) | STR §11.3: days 0–15 and 27–42 contain no production: ≈ 30 days > 28. | The sentence is arithmetically wrong; even zero production misses 4 weeks. |
| Brief stop rule on compute (my check, K-A8) | Brief §7: "Stop and ask the user if … the projected compute overruns the approved schedule by more than 30%". STR l.1161: "is reported"; l.729-730: "the schedule is corrected". | Weakened. Category A. |
| Physics B1 proposes ρ = 3–4 for thinning; physics A4 / N-B-1 propose larger samples | PLAN l.440 ("Brute-force growth of the existing samples (×100)") and l.444 ("The ρ = 3 sample") are discarded; brief D8. | **The fixer must not use ρ ≥ 3 nor ×100 growth of direct samples.** Reallocation and biased generation of the new no-PU samples are allowed (they are new v2 samples, not growth of v1 samples). |
| P-B6 says the K validation tolerances are too loose; K-B12 says validation 2 could falsely fail at 1 TeV | `theory_signal_model.md` l.158-163 (via K-B12): implied K against CT18NLO LO rises 1.06 → 1.29 with mass; tables are NLO+NLL / NNLO_approx+NNLL. | Not a contradiction: both arise from comparing unlike quantities. Fix: compare NLO with NLO (tight), or remove the resummation explicitly. |
| K-B6 (F too loose for B2, ≈ 1 % precision) vs N-B-2 (F = 1.5 too tight at N = 20, 9.8 % false fail) | STR l.436-438, l.447-449; N's calc. | Different regimes; both correct. Tolerances must be set per test from expected precision (M15). |
| K-B1 suggests a hybrid T2 candidate (ladder + BDT as a B3 conditional) | STR l.286-288: no distribution of a variable for matched signal candidates before the verdicts; training needs v2 signal. | A pre-registered BDT candidate would breach the blinding invariant (brief §7). The fixer documents this as the reason (N-B-11 reason (i)), not adopts the hybrid. |

---

## 3. Structured adjudication table

Source abbreviations: P = physics (Casimir), K = critical (Celeste), N = constructive (Cosima), Arb = raised by me.
Fix type: **(i)** design change (method, criterion, sample size or budget); **(ii)** precise statement or definition;
**(iii)** decision for the human at Gate A (fixer presents options with costs).

| # | Finding | Source | Their Cat | Final Cat | Fix type | Rationale |
|---|---|---|---|---|---|---|
| M1 | Zero simulated counts in the likelihood: generation point for Asimov/toys undefined; at γ̂ = 0 zero-count terms vanish from the expected limit; T2 then rewards the least-counted (deepest) selections; "leading term" and v2 B₈₄ undefined | P-A1, K-A1, N-A-1 (+P-C2 non-zero-truth part, K-C9) | A, A, A | **A** | (i)+(ii) | Case 1. Verified at STR l.611-625, l.639-645, l.680-684: no generation hypothesis is stated; γ is unconstrained. |
| M2 | C1 blinding exception: 6 of 10 C1 signal quantities (not 3) are T2-candidate efficiencies; the T2 list may still shrink after they exist; the exception to a brief §7 invariant has not been put to the user | K-A2 (+Arb: user approval) | A | **A** | (ii)+(iii) | Case 3/4, verified in §2. An exception to a user invariant can only be granted by the user. |
| M3 | P_geo × C_PU closure (B1-a) and the B3/B4-c analogues are tested at the same rungs where C_PU/conditionals are derived, with physically equivalent samples (tautological); promotion of loose-rung failers by pile-up is outside C_PU | P-A3, K-A3 (part 1) | A, A | **A** | (i) | Case 1. STR l.359-361 vs l.373-375. A tautological comparison presented as validation is a regression-check item. |
| M4 | Extrapolation from the closure rungs (R04–R07) to the working rungs (R09–R20) carries no guaranteed width: s_model capped at ln F regardless of distance; trend test adds width only at 2σ (low power, discontinuous, rung index across cut families); C_PU at deep rungs undefined; conditionals measured after loose rungs, applied after deep rungs (referee Q4) | P-A2, K-A3 (part 2), N-B-3, N-B-4 | A, A, B, B | **A** | (i) | Case 2: sided with P and K. This decides whether the result is an estimate; N's own numbers (slope error 0.097/rung → 1σ extrapolation 0.68–0.97 in ln at R14–R17) show the gap is of the size of the total σ_ln target. |
| M5 | Testability: several MUST criteria cannot be evaluated at the planned statistics (PV pair, V⁰, NI, loopers; B1-b slope on 1–2 points; B4-c only Z(νν)); "not testable" earns credit; [SD8] does not say whether NOT TESTED/not evaluable counts as PASS; "leading term" decided with a failed estimator's own value (loophole) | P-A5, K-A4, N-B-12, K-A1 (leading-term part) | A, A, B, A | **A** | (i)+(ii)+(iii) | Case 1/2. Verified in §2; also breaches brief D4 (MUST statistics). COM B1-a promises a test the statistics do not allow. |
| M6 | Sample-size floors not computed; central target (total σ_ln ≲ 1, "estimated" vs "bounded") not defined; floors at planned sizes ≈ 141 (PV pair) and ≈ 47 (SM) events before credits; biased-generation enrichment not estimated; no-PU allocation not optimised (√rate: 150.6 → 67.5 at equal cost) | P-A4, N-B-1 | A, B | **A** | (i)+(iii) | Case 2: sided with P. N rated B because the fix is cheap; cost of a fix does not lower severity. It decides the paper's outcome row (PLAN l.123-131) and the user must see it before approving. Arithmetic verified (log). |
| M7 | Signal injection (T1-c) passes whatever the fit does (μ₉₅/N_exp ≈ 790; injection in σ_norm units); Asimov pulls (T1-d) are zero by construction; T1-b compares μ₉₅ in events with μ = σ/σ_norm (unit mismatch) | K-A5, K-B16, P-C2 (part), K §3 row 3 | A, B, C | **A** | (i)+(ii) | Case 2: sided with K. A required conventions check (`search.md` check 2) made vacuous. |
| M8 | T1-g is tautological or a nested-toy cost of 1,449 CPU-h; toy budget counts one pass, two are needed (4b, 4c); [L4] ×2 | K-A6, N-B-14, P-C2 (part) | A, B, C | **A** | (i)+(ii) | Case 2: sided with K; verified in §2. Either branch breaks the criterion or the budget presented to the user. |
| M9 | MET-model validation (a) tuned to pass (soft term set to reproduce v1's 25 GeV, then compared with v1); contradicts "no parameter quoted, R-3"; no external anchor; (c) at a factor 3 and different conditions | K-A7, P-B11, N-B-10 | A, B, B | **A** | (i) | Case 2: sided with K. STR l.522-528 is a parameter set to the reference then checked against it (motivated-reasoning red flag "validation that passes trivially"); it is a criterion of the binding COM B4-b. |
| M10 | Brief §7 stop rule (projected compute overrun > 30 % → stop and ask) restated as "reported" / "schedule corrected"; no COM row | K-A8, Arb | A | **A** | (ii) | Case 3, verified in §2. A user invariant may not be weakened. |
| M11 | Detector-variation sizes (resolution ×1.5, inefficiency 97 %, material ×0.5/×2, C/Si/Cu mixture, material band) are round numbers that enter the likelihood at full measured effect | P-B8 | B | **A** | (i) | Case 3, upgraded: `CLAUDE.md` "Systematic variation sizing: … '±50 % on the background' is Category A unless 50 % IS the measured uncertainty". STR §5.1 l.847 itself forbids it. |
| M12 | Correlated detector nuisances have no propagation path to the single-interaction and SM terms that lead from R07 on (B6 propagates only to pile-up at R04–R06 and to signal); transfer of pile-up shifts to depth unstated | K-B3, N-B-7 | B, B | **B** | (i) | Case 1. STR l.579-580 vs l.628-632. |
| M13 | [DP2] drops 5 keV, ≥ 1 TeV and the scalar, i.e. the points most sensitive to material and timing, and 9 of 20 G-window points; no interpolation rule | P-B9, K-B14 (+N-C-2 paired design) | B, B | **B** | (i)+(iii) | Case 1. |
| M14 | Thinning ρ = 2 → 1 has no stated deep reach (draws per trial, effective N, deepest rung); B2-b "not evaluable" branch missing; occupancy model's fit-probability conditional source unstated (independence) | P-B1, N-B-16 | B, B | **B** | (i)+(ii) | Case 1. ρ = 3–4 option barred (brief D8, §2). |
| M15 | Closure-criterion statistics: diagonal χ² ignores nested-rung and common-s_model correlations; (b) vacuous at the cap; size and power per test not stated; no family-wise statement under the AND rule (perfect analysis passes all 12 tests with p ≈ 0.54); thresholds counted before the cut (B3); s_model not fixed pre-freeze from development samples | P-B3, K-B6, N-B-2 | B, B, B | **B** | (i)+(ii); tolerances (iii) | Case 1. F must not be loosened (N). F and [SD8] are already a flagged human decision. |
| M16 | Time-tag credit [SD6]: timing tails (beam-spot spread, non-Gaussian tails, out-of-time PU, slow hadrons, noise) not modelled; closure design will be "not testable" (≈ 10⁻⁴ conditional); independence from geometric rungs untested | P-B7, K-B11, N-B-5 | B, B, B | **B** | (i) | Case 1. STR itself flags orders-of-magnitude effect on SR-T. |
| M17 | Signal quantities computed before the verdicts and not declared: A, f₂₀₀ (Phase 2), offline MET threshold change while A is known, B6 ε_nom half unspecified, C2 "optimality" count | K-B7, K-B8 | B, B | **B** | (ii) | Case 3. STR l.285 says "exactly the ten"; l.316, l.710-718, l.770-772, l.588 contradict it. |
| M18 | MVA infeasibility argument overstated ("none applies to an arbitrary score" is false for thinning and P_geo); BDT working point "equal pile-up rate" vs "equal counted background" | K-B1, N-B-11, P-C1 | B, B, C | **B** | (ii) | Case 2: sided with K and N; 03-phases requires the review to validate the infeasibility. DP3 conclusion stands with the correct reasons (§2). |
| M19 | Costs and schedule: unmeasured/underestimated unit costs (no-PU HS 15 ms, multijet 10 ms, P1 via M3 ratio, signal-row injection, uncosted QGSP_BERT and composition variations); capacity uses 12 slots; utilisation unmeasured; "4 weeks needs ≈ 1,000 CPU-h" wrong; no ITERATE or human-gate allowance; development effort (PLAN 35–50 person-days) not modelled | K-B2, K-B4, N §4 (dev effort, ITERATE allowance; N-C-6 part) | B, B, (B) | **B** | (i)+(iii) | Case 1; facts verified in §2. |
| M20 | S1 "×10" is ×5 on the evaluation half that sets the limit | K-B5 | B | **B** | (ii)+(iii) | Case 3, verified in §2. |
| M21 | C1 chain per signal point not stated (fast path at E200 1.5/2 keV vs full chain; expected shift ×0.832/×0.871) | K-B9 | B | **B** | (ii) | Case 3. STR l.257-259 labels v1's path, not the v2 C1 path. |
| M22 | B1 direct counts need a truth-attribution rule (pile-up-only planes pass R05 at 49.7 per trial) | K-B10 | B | **B** | (ii) | Case 3. |
| M23 | S2 K validations compare unlike quantities with loose tolerances; method parity (NLO+NLL vs NLO, 03-phases l.211-218) not argued for σ_norm | P-B6, K-B12 | B, B | **B** | (i)+(iii) | Case 1 (§2 settles the apparent contradiction). |
| M24 | [DP5] Herwig declines the attempt in advance (JFC 12: attempt first) and loses a required conventions source; DPs not stated as carried into the paper (method, systematics, Future Directions) | K-B13 | B | **B** | (i)+(ii) | Case 3. |
| M25 | Criterion IDs differ between STR and COM (B1, B2, T1, T2, S2) | K-B15, N-B-15 | B, B | **B** | (ii) | Case 1. |
| M26 | Background list incomplete: secondaries of pile-up vertices (nuclear interactions, decays), noise hits, out-of-time hits, δ-rays, merged clusters | P-B2 | B | **B** | (i)+(ii) | Case 3. Verified: B1 is per triggered event only (STR l.362), Fatras has no hadronic physics (l.386-388). |
| M27 | Signal-side detector response not consistent with backgrounds: signal MET through the reco model; migration across the pT(QQ̄) > 200 GeV generator cut; quirks in calorimeters/muon system and lepton veto; tracker hit-time acceptance for slow pairs | P-B4 | B | **B** | (i)+(ii) | Case 3. |
| M28 | Infracolour Coulomb (Sommerfeld) correction to σ_norm absent (P estimates +3 to +13 % at β = 0.7–0.3; comparable to or above the scale envelope) | P-B5 | B | **B** | (i) | Case 3. I re-derived α_IC(200 GeV) ≈ 0.045 at Λ = 1 keV with b₀ = 22/3; the order of magnitude stands. The β-distribution of Drell–Yan reduces the average; it must be computed, not assumed. |
| M29 | T2 picks the minimum G without splitting or bootstrapping the background inputs: selection bias on the background side | P-B10 | B | **B** | (i) | Case 3. |
| M30 | Dropping dE/dx ([SD9]) gives up a primary discriminant without quantifying the loss | P-B12 | B | **B** | (iii) (minimum: (i) forgone-gain report) | Case 3. Already flagged by STR; the missing piece is the forgone-sensitivity measurement. |
| M31 | B5 sideband closure on SM+PU samples is dominated by flat pile-up (HS share 6–10 %); a ×5 non-flatness passes F = 1.5; with [DP1] R07 drops out (7.7 counts) | N-B-6 | B | **B** | (i)+(iii) | Case 3; arithmetic checked. |
| M32 | Poisson auxiliary model for weighted samples (biased generation, p̂T slices) not specified | N-B-8 | B | **B** | (ii) | Case 3. |
| M33 | Multijets: P(r \| MJ) measured on ≈ 100 effective events → new zero-count floor | N-B-9 | B | **B** | (i) | Case 3. |
| M34 | Post-freeze closure failure: JFC regression/3-remediation rule vs "reported as failed" not reconciled; fresh-sample rule | N-B-13 | B | **B** | (ii) (+budget reserve) | Case 3. |
| M35 | No consolidated sample inventory (sample, generator, size, seed stream, development / closure / production role, independence, phase, cost) — a Phase-1 deliverable (phase CLAUDE.md "Sample inventory") and the basis for the independence demanded by M3, M4, M29, M34 | Arb | — | **B** | (ii) | Case 5. |

No finding is dismissed. Reviewer pressure protection: no executor rebuttal exists yet; every finding stands.

---

## 4. Regression and motivated-reasoning checks

**Regression triggers (§6.7).** Phase 1 has no results, so validation failures, > 80 % systematics, GoF toys and
bin exclusion do not apply. **Tautological comparisons presented as validation: yes, four, in planned criteria** —
M3 (same-rung closure), M7 (injection and Asimov pulls), M8 (T1-g), M9 (MET validation (a)). There is no earlier phase
to regress to; all four must be fixed in this iteration.

**Motivated reasoning.** The narrative "v2 replaces the bounds by estimators" (STR l.31) is not yet supported by the
design: at the planned sizes the deep terms remain zero-count (M6), the likelihood could make them vanish (M1), the
closure tests do not cover the extrapolation (M3, M4) and "not testable" earns credit (M5). The undercounted C1
disclosure (M2) and the softened stop rule (M10) both point the favourable way. To the executor's credit: the 6-week
calendar is stated plainly, the MUST-cutting levers are listed and not proposed, the v1 freeze timing is disclosed,
and the ×1.5 endcap provenance is flagged without reopening brief D1.

**Brief compliance (my own check).**
- MUST/SHOULD coverage: every item C1–C3, B1–B7, T1–T2, S1–S2, P1 has a section and a COM row. ✓ (but see M5: brief
  D4 statistics for MUST criteria).
- S3 dropped with the outlook statement quoted verbatim (STR l.801-803, COM S3). ✓
- No cloud (all compute on the lab cluster). ✓ D5 subset declared with the best point and R04–R09. ✓
- No Stage 3 at Λ ≥ 15 keV (STR l.713-714, [SD1]). ✓ No pile-up scan ([SD5]). ✓ No CMS Open Data. ✓
- Discarded items: not reintroduced by STR. **Guard for the fix:** ρ = 3 and ×100 brute-force growth must not be
  introduced by M6/M14 fixes.
- Stop conditions: the 30 % compute rule is misquoted (M10); the cajuela 2.0 TB / 1.0 TB-free rule is respected
  (projection 360–560 GB); "MUST infeasible after a real attempt" is quoted correctly (l.279-280).
- Blinding invariant: the C1 exception (M2) and the Phase-2 acceptance factors (M17) need explicit declaration and,
  for C1, user approval.
- Brief Phase-1 deliverables: schedule, [D] proposals, plan §8 decision points, 25 referee questions, 7 figures:
  present. Model policy: T1/T2 statistics design is a "go up" task (brief §4); I recommend the orchestrator runs the
  M1/M7/M8/M15 part of the fix at higher effort or model.

---

## 5. Decisions for the human at Gate A (the fixer prepares options and costs; does not decide)

| # | decision | options the fixer must cost |
|---|---|---|
| H1 | C1 signal exception (M2) | (a) keep the 10 quantities, disclose 6 as T2-candidate efficiencies, freeze family F and R07 in the T2 list from now on; (b) drop R07 and FB from C1 (4 quantities left; the FB check is "gross check only", MDE ≈ 65–75 %), keeping the best-point headline reproduction only through R04/R06; (c) as (a) at 200 rows. Cost differences in CPU-h and in what C1 can still claim. |
| H2 | S1 statistics (M20) | 2,000 rows (×10 total, ×5 on the limit half; ε = 0.045 → 15 % binomial error) vs 4,000 rows (+560 chain + 266 Stage 3 = **+827 CPU-h**, ≈ +4.8 production days at 174/day; 11 %). |
| H3 | Paper message given the floors (M6) | after reallocation/biasing, the projected floor per term and the PLAN §8 outcome row; if floors stay at tens of events: "bounded at the X-event level for terms T…" vs extra biased generation with its cost. |
| H4 | Closure tolerances F, eligibility [SD8] and the NOT TESTED policy (M5, M15) | already flagged by STR (§12.1); now with false-fail and power numbers per test and the always-eligible baseline (N-C-4). |
| H5 | σ_norm (M23) | σ_NLO alone with the resummed tables as implemented cross-check vs σ_NLO × (NLO+NLL)/NLO (FEAS_B recommendation); plus the IC Coulomb correction applied or as a one-sided theory band (M28). |
| H6 | dE/dx (M30) | exclude, with the forgone gain measured after Gate B (≈ 0 CPU-h) vs model charge straggling and keep one dE/dx candidate with its own closure (cost to be estimated). |
| H7 | [DP1], [DP2], [DP4], [DP5] restated (M13, M24, M31; K-C3 for DP4) | each with corrected saving and loss; DP2 alternative: paired design covering all six points at reduced cost (N-C-2). |
| H8 | Schedule (M19) | the corrected calendar (10-slot capacity, ITERATE and gate allowances, development effort) against the 2–4 week target. This is a Gate-A matter, not an escalation. |
| H9 | Time-tag credit (M16) | already flagged; now with the tail model and the testable design. |
| — | Endcap wording ×1.5 | already flagged by STR (§12.2 item 2); brief D1 is fixed, so the text stays unless the user changes it. |

---

## 6. Work list for the fixer (priority order)

General rules for the fix: write a new version `STRATEGY_<fixer>_<timestamp>.md` (do not overwrite); keep every
change traceable to the M-number; update `strategy_budget.py` for every CPU-h, storage or calendar change and show,
in a new table in §11, **each fix's delta in CPU-h and days** (no change is waved through); rename COM criteria to one
id set (M25) and update every touched row; do not reopen brief §3 decisions; do not use ρ ≥ 3 or ×100 brute-force
growth; do not loosen any F. Indicative deltas below are my [E] estimates; the fixer recomputes them.

### Priority 1 — Category A

1. **M1 zero counts (§4.11, §4.12, §8 item 5; COM T1-a, T1-b, T2-a, T2-b).** Fixed looks like: (a) the generation
   hypothesis for Asimov data and every toy, for every auxiliary count with m = 0 and m > 0, declared and justified —
   recommended prior-predictive (hybrid): λ drawn from Gamma(m + 1) (flat) or Gamma(m + ½) (Jeffreys), the choice
   declared, as the implementation of the brief's "Gamma constraints for zero counts"; the frequentist alternative
   reported beside it at the best point; (b) "leading term", v2 B₈₄ and the total σ_ln (½ ln(B₈₄/B₁₆) of the
   predictive distribution of B_total) defined from that distribution, not from γ̂; (c) a limiting-case test: one
   term with m = 0 of M reproduces the analytic hybrid limit within toy error; (d) a coverage test with non-zero truth
   (λM = 0.5, 1.14, 2, 3); (e) the T2 limiting-case check: an all-zero-count deep candidate must not get a better G
   than with its terms at 1.14/M; (f) the fraction of B₈₄ carried by m = 0 factors reported at the chosen selection,
   with the pre-declared reading "sample-size limited" if > 50 %. Cost ≈ 1–5 CPU-h in Phase 3.
2. **M5 testability and NOT TESTED (§4.0, §4.4, §4.6, §4.7, §4.12 [SD8]; COM B1-a, B1-b, B3-a…c, B4-c, T2-a).**
   (a) A table per topology/process × rung of expected direct counts at the planned sizes (from D4 l.185-203), with
   the rungs actually testable; (b) closure samples raised for leading terms (at least PV pairs and V⁰ so that R05–R06
   are testable), or the criterion changed and the change put to the user (brief D4); (c) verdict classes PASS / FAIL /
   NOT TESTED / NOT EVALUABLE defined for every criterion, and their consequence under [SD8] fixed now (recommended:
   a leading term NOT TESTED makes the selection ineligible unless it carries a pre-declared width ≥ the M4 rule from
   the nearest closed rung, flagged in the ladder figure); (d) "leading" for a term with a failed or untested
   criterion decided with its conservative value (direct-count bound), the same value used in the likelihood.
   Cost: each 1,000 direct events ≈ 7 CPU-h; fixer computes the sizes.
3. **M6 floors and central target (§0, §4.4, §4.7, §11.2, §12; COM B1-a, B4-c, new row for the target).** (a) Floor
   table per term × candidate family at the planned M, with s_model at its cap and expected value, and the projected
   σ_ln and PLAN §8 outcome row (v1 placeholders); (b) an enrichment estimate for biased generation per topology,
   and a Phase-2 pilot (1–2 CPU-h) that measures it, including importance sampling for PV pairs; (c) no-PU allocation
   by ≈ √rate (150.6 → 67.5 summed floor, cost-neutral) and leading SM processes ≥ 10⁷ no-PU events (Z(νν): ≈ +112
   CPU-h at 45 ms); (d) the projected outcome in §0 and in the Gate-A sheet (H3).
4. **M3 same-rung closure (§4.4, §4.6, §4.7; COM B1-a, B3-a…c, B4-c).** For each C_PU and conditional: derivation
   rungs and **disjoint** test rungs, on disjoint samples, declared now; overlay a random subset of loose-rung failers
   to measure the promoted fraction vs rung, entered as a term or bounded; any remaining same-rung comparison labelled
   "consistency check". Cost: small (overlay of failers ≈ +10–20 % of the 112 CPU-h overlay line).
5. **M4 extrapolation width (§4.0, §4.4 B1-b, §4.5 B2-c, §4.6, §5.2, §4.12; COM B1-b, B2-c, SY-6).** An extrapolation
   width **always** added, growing with distance: σ_extr = σ_slope × Δ (in quadrature with s_model), fitted within a
   cut family; the C_PU(r) extrapolation rule (functional form, inputs) written down; a held-out test (derive on
   R04–R05, predict R06–R07 blind, same F); each conditional measured after ≥ 3 preceding rungs with a stability test;
   per T2 candidate, the last closed rung of every leading term and its σ_extr tabulated. Cost: re-analysis only.
6. **M8 T1-g and toy budget (§4.11, §11.2; COM T1-b, T1-c).** T1-g redefined against an independent quantity
   (asymptotic per pseudo-experiment, or from stored test-statistic distributions, or coverage at known injected μ),
   with its cost in the script; both toy passes (4b and 4c) budgeted (+174 CPU-h, or less with the f_T-grid
   parametrisation of N-B-14, validated by exact toys at 3–5 points); [L4] scaling measured on a 60–100-parameter
   workspace in Phase 3.
7. **M7 injection and pulls (§4.11, §5.2; COM T1-b).** Injection at 0, 1, 2, 5 × μ₉₅^exp per tested point on
   fluctuated pseudo-data, bias threshold 20 % of injected μ, number of pseudo-experiments stated (at μ = 0 an absolute
   criterion in units of the fit error); pulls and constraints on fluctuated pseudo-data (Asimov kept only for
   constraints); T1-b in consistent units (μ = σ/σ_norm or events, stated).
8. **M9 MET validation (§4.7; COM B4-b).** Soft-term resolution from R-3 only; validation (a) relabelled a continuity
   check with v1; an external validation added: MET resolution vs ΣE_T or ⟨μ⟩ and the tail fraction against a
   published Phase-2 PU-200 MET performance figure with a pre-declared tolerance; (c) states the reference's √s and
   pile-up.
9. **M10 stop rule (§11.6, §4.13, §12.4; new COM row).** Quote brief §7 exactly: every overrun reported; a *projected*
   overrun above 30 % of the approved compute stops the study and asks the user; the Phase-2 re-timing of the first
   jobs is a declared checkpoint against that rule.
10. **M2 C1 exception (§4.1, §8 item 8; COM C1-d).** Disclosure corrected to six (R07 × 3, FB2/FB3 × 3 = family F);
    rule that the T2 list may not change family F or R07 after C1 numbers exist; present H1 options; state that the
    exception to the brief §7 invariant takes effect only with the user's approval at Gate A.
11. **M11 detector-variation sizing (§4.9, §4.4 B1-c and risk (1), §5.1; COM B6, SY-5, SY-9).** Each variation that
    enters the likelihood sourced from a public Phase-2 statement (new retrieval tasks); round-number variations kept
    only as robustness tests (reported, classified) and not as nuisances.

### Priority 2 — Category B (statistics and estimators)

12. **M15** (§4.0; prereg outline): full covariance for nested rungs with s_model² in all elements (or separate 1-dof
    tests for coherent shift and trend); s_model fixed pre-freeze from development samples; per test N, σ_ln,
    false-fail at r = 1 and power at r = F tabulated; thresholds in counts after the cut (e.g. ≥ 55 for F = 1.5);
    family-wise statement with a declared rule (Holm, or investigation + fresh sample for 0.05/K < p < 0.05); the
    retroactive v1 thinning test reported as the demonstration of power. F not loosened.
13. **M14** (§4.5; COM B2-a…e): draws K per ρ = 2 trial, effective N, projected deepest rung; "B2-b not evaluable"
    branch with its [SD8] consequence; if thinning stops at R07, the deep pile-up term is declared a one-estimator
    extrapolation with the M4 width; source of the occupancy model's fit-probability conditional named. More ρ = 2
    trials are allowed (recompute 206 s/event), ρ ≥ 3 is not.
14. **M16** (§4.6; COM B3-c): timing model with beam-spot time spread and a sourced non-Gaussian tail; late-hit
    conditional measured at hit level and closed by widening the time window on loose candidates (pre-registered
    scaling law); independence from the geometric rungs tested on the 96,000 direct trials. ≈ 5 CPU-h.
15. **M29** (§4.12; COM T2-a): background-side bias of the T2 choice from bootstrap replicas of the background inputs
    (frequency of the same winner, shift of its B), or reserved independent background seeds for the chosen
    selection.
16. **M32** (§4.11): one auxiliary channel per weight class; n_eff = (Σw)²/Σw² where weights vary; zero counts with the
    slice weight.
17. **M34** (§8 item 10): three-branch failure protocol (ticket always; bug → addendum + re-closure on a fresh sample,
    reserve one B2 direct sample, 403 CPU-h, inside the contingency; no bug → reported failed, [SD8]).
18. **M12** (§4.9, §4.11; COM B6, SY-9): for every shared nuisance name, the samples and rungs on which it is
    evaluated per term; P_geo of the leading topologies and SM processes rerun under each variation (≈ 20 CPU-h no-PU
    at 11.5 ms; more for SM at the corrected unit cost); transfer of pile-up shifts to depth stated.
19. **M33** (§4.7): pre-registered factorisation P(r | MJ, MET > 250) from a looser population, tested on Z(νν) and W
    in MET bins.
20. **M31** (§4.8; COM B5): B5-a/b on the truth-attributed hard-scatter component, T(Δφ) measured on the no-PU
    hard-scatter samples (≈ 10 CPU-h); PU-overlay sample kept for road independence; DP1 loss restated including R07.
21. **M22** (§4.4): truth-attribution rule for direct counts.
22. **M26** (§2 Table 2.1, §4.4): add pile-up-vertex secondaries (Geant4 on minimum-bias spectra × acceptance), noise
    and out-of-time occupancy (retrieval task), δ-rays/merged clusters, each with class, order of magnitude and either
    inclusion or a < 10 % argument.

### Priority 3 — Category B (signal, theory, blinding, statements)

23. **M27** (§1, §4.13, §4.14): signal through the same MET_reco model (nuisance correlated with background);
    migration measured on a validation sample with the generator cut lowered (e.g. 150 GeV); calorimeter/muon-system
    and lepton-veto assumption with a number or a limitation label; tracker hit-time acceptance from a public Phase-2
    readout description, at least as a systematic at the highest mass.
24. **M28** (§4.14, [SD11]): IC Coulomb/Sommerfeld correction computed per mass with the generated β distribution and
    the stated α_IC(Λ); applied or carried as a one-sided band (H5); retrieval task for its treatment in the quirk
    literature.
25. **M23** (§4.14; COM S2-a): validation 3 differential in invariant mass with ≈ 2 % (or 3σ of integration error);
    validation 2 NLO against NLO (tables' NLO column or a public NLO code), ≲ 3 %, or the resummation removed
    explicitly; parity argument per 03-phases with the resummed normalisation as implemented cross-check (H5).
26. **M17** (§4.1, §4.2, §4.13, §4.14, §4.9; COM C1-d, S1-b): declared exception for A and f₂₀₀ (selection-independent
    across the T2 list; brief Phase 2 requires f₂₀₀); any offline-threshold change logged before A is computed; B6
    ε_nom from the optimisation half or its own rows, after the verdicts; the C2 optimality count added to the declared
    list or removed.
27. **M20** (§4.13; COM S1-a): "×10 total, ×5 on the evaluation half" stated with the lost precision; H2 options.
28. **M21** (§4.1): the chain per C1 point (fast path at E200 1.5/2 keV to reproduce v1); the full-chain/fast-path
    ratio as a reported diagnostic with its expected value.
29. **M18** (§3.2, [DP3], [SD2]): infeasibility restated with the reasons that hold (blinding forbids training a
    pre-registered candidate on v2 signal; no independent pile-up cross-check for a score; no training background
    beyond R08); the hybrid excluded for the blinding reason; working point at equal total counted background.
30. **M30** (§4.12 [SD9]): forgone-gain measurement ε(R_k + dE/dx)/ε(R_k) at directly counted background after Gate B
    as the minimum; H6 options.
31. **M13** (§4.9; COM B6): reduced set keeps 5 keV and one high-mass point; interpolation rule and width for unvaried
    points; paired (common random numbers) design costed as the alternative (H7).
32. **M24** (§5.1, §11.5; COM SY-7): Herwig install attempted on a worker (one install slot) or a documented failure;
    expected impact from published K/π differences; for every DP, how it is carried into the paper.
33. **M19** (§11; script): corrected unit costs (no-PU HS ≈ 45 ms → 187.5 CPU-h; multijet ≥ 23 ms; P1 B*-off on maxwell
    numbers ≈ 36.5 CPU-h, and the configuration resolved; QGSP_BERT and composition variations costed); a provenance
    column (measured / derived / guess) and a contingency sized from it; capacity with 10 off-hours slots (1,625
    slot-h/week, 174/day in production); ITERATE allowance (≥ one per 4-bot review) and human-gate turnaround; a
    development-effort line; the "4 weeks needs ≈ 1,000 CPU-h" sentence corrected (≈ 30 non-production days already
    exceed 28); §11.6 levers replaced or complemented by non-MUST levers (toy parametrisation, paired B6, no-PU-based B5).
34. **M35** (new §4.17 or §11): consolidated sample inventory: sample, generator/tune, size, seed stream, role
    (development / closure / production / C1), independence statement, phase, CPU-h, storage.
35. **M25** (STR and COM): one criterion id set, COM as master, STR quoting it; also update `strategy_budget.py`
    labels.

**Indicative budget effect [E, mine; fixer recomputes]:** non-optional additions identified ≈ +550–650 CPU-h
(no-PU HS cost +125, Z(νν) no-PU ×10 +112, multijet +36, second toy pass +174 or less, P1 +20, physics-list and
composition variations ≈ +60, detector propagation ≈ +30, failer overlays ≈ +20) plus the closure-sample increases of
M5 (to be sized) and the fresh-sample reserve inside the contingency; option H2 adds +827. At 174 CPU-h/day this is
≈ 3–4 production days before H2. The fixer presents the new total against the 2–4 week target (H8).

### Category C items for the fixer to apply (no re-review needed)

- P-C3: re-evaluate the top five (not three) eligible selections with toys, or all at the 20 window points (≈ 29
  CPU-h each). P-C4: PDF4LHC21 as nominal or justify CT18NLO. P-C5: one FxFx point at E 1500. P-C6: like-for-like
  ε breakdown against R1 Table I; label 300 fb⁻¹ curves. P-C7: B7 threshold relative to total B or its 1σ; add
  beam-gas and satellites. P-C8: retrieval for ATLAS/CMS non-helical/quirk searches and 2020–2026 HL-LHC projections.
- K-C1: tags [V] on digest-sourced numbers → [U]; "34 ms" is derived. K-C2: citation line slips (halo l.321; PLAN
  l.166; union closure 0.654 is the T_seed = 6 pilot). K-C3: [DP4] trials share 78 %, not 45 %; recompute the S4 cost.
  K-C4: software size includes the home pixi environments. K-C5: dump storage for C2, B5, occupancy model; ρ = 2
  events 4.0 MB. K-C6: the "up to 5 GiB" ρ = 2 case leaves nothing for other jobs. K-C7: Geant4 vertex yield vs P_geo
  sample; biasing gain assumed. K-C8: nuisance pruning policy. K-C9: binomial chain or stated approximation for
  M_{t,j}. K-C10: σ_ln target as a reported outcome with a pre-declared reading. Also: 4-fermion generator comparison
  for tt̄/dibosons (K §2 table, C-level).
- N-C-1: one-page Gate-A decision sheet (use §5 above). N-C-2: paired designs in B6. N-C-3: project G from the v1 row
  arrays before the freeze. N-C-4: an always-eligible baseline (deepest fully direct-counted selection) and a
  partial-outcome matrix. N-C-5: figures for C1 pulls, C2 Δn, B5 T(Δφ), T1 pulls/impacts, B6 shifts, S2 K(m)/f₂₀₀,
  MET validation, BDT ratio, each mapped to a referee question. N-C-6: use idle pre-production capacity for larger
  development samples and pilots; start Geant4 geometry, B1-d scan, hand-over code and T1 builder in Phase 2. N-C-7:
  Geant4 is on all three workers (commit 199e166): update l.402, l.1111, [A7]. N-C-8: dump storage (as K-C5). N-C-9:
  R2's Z+jets 0.12 fb as a sanity comparison; close R-10 before 4a. N-C-10: §11.6 levers (folded into item 33).
  N-C-11: §0 carries the projected outcome and the three largest decisions.
- Arb-C1: T2 rule "a point with no passing optimisation row enters with ε = 1/n_opt" (STR l.683) biases G toward deep
  selections that empty some points; use one declared estimator at every point (e.g. (k + ½)/(n + 1)) and report the
  sensitivity of the choice to it.

---

## 7. Mapping from reviewer numbers to merged findings (every A and B item)

| reviewer item | merged | | reviewer item | merged | | reviewer item | merged |
|---|---|---|---|---|---|---|---|
| P-A1 | M1 | | K-A1 | M1, M5 | | N-A-1 | M1 |
| P-A2 | M4 | | K-A2 | M2 | | N-B-1 | M6 |
| P-A3 | M3 | | K-A3 | M3, M4 | | N-B-2 | M15 |
| P-A4 | M6 | | K-A4 | M5 | | N-B-3 | M4 |
| P-A5 | M5 | | K-A5 | M7 | | N-B-4 | M4 |
| P-B1 | M14 | | K-A6 | M8 | | N-B-5 | M16 |
| P-B2 | M26 | | K-A7 | M9 | | N-B-6 | M31 |
| P-B3 | M15 | | K-A8 | M10 | | N-B-7 | M12 |
| P-B4 | M27 | | K-B1 | M18 | | N-B-8 | M32 |
| P-B5 | M28 | | K-B2 | M19 | | N-B-9 | M33 |
| P-B6 | M23 | | K-B3 | M12 | | N-B-10 | M9 |
| P-B7 | M16 | | K-B4 | M19 | | N-B-11 | M18 |
| P-B8 | M11 | | K-B5 | M20 | | N-B-12 | M5 |
| P-B9 | M13 | | K-B6 | M15 | | N-B-13 | M34 |
| P-B10 | M29 | | K-B7 | M17 | | N-B-14 | M8, M19 |
| P-B11 | M9 | | K-B8 | M17 | | N-B-15 | M25 |
| P-B12 | M30 | | K-B9 | M21 | | N-B-16 | M14 |
| | | | K-B10 | M22 | | N §4 (dev effort) | M19 |
| | | | K-B11 | M16 | | | |
| | | | K-B12 | M23 | | | |
| | | | K-B13 | M24 | | | |
| | | | K-B14 | M13 | | | |
| | | | K-B15 | M25 | | | |
| | | | K-B16 | M7 | | | |

C items folded into A/B findings: P-C1 → M18; P-C2 → M7, M8, M1; K-C9 → M1 (kept as C in §6). All other C items are
listed in §6.

---

## 8. Verdict

**ITERATE.** Category A items that block: **M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11**. All 24 B items (M12–M35)
must also be fixed before PASS. The fixer works from §6 in priority order, records each fix against its M-number,
recomputes the budget for every fix that adds CPU-h or days, and prepares the Gate-A options of §5 without deciding
them. The re-review is a numbered artifact with a fresh reviewer added to the panel (06 §6.5); this is cycle 1 of the
4-bot cap.
