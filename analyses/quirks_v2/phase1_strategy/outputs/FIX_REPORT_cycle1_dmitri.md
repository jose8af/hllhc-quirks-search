# Fix report — Phase 1 STRATEGY, review cycle 1

Fixer: Dmitri (session label 2026-11-13 19-25). Role: `agents/fixer.md`.
Work list: `review/arbiter/STRATEGY_ARBITER_dagmar_2026-11-13_19-00.md` (11 Category A: M1–M11; 24 Category B: M12–M35;
C items of its §6).
Produced:
- `outputs/STRATEGY_dmitri_2026-11-13_19-25.md` ("v2"; 2,391 lines). v1 (`STRATEGY_brigitte_2026-11-13_17-55.md`) is
  unchanged (`git status` shows no modification).
- `QV2/COMMITMENTS.md` ("COM"): one identifier set, a table of old → new identifiers, 102 rows with status `open`,
  nothing removed.
- `src/strategy_budget.py` ("script"; standard library, about 1 s): every CPU-h, storage, calendar, floor and
  test-power number of v2. Printed sections [1]–[13].
- `QV2/retrieval_log.md`: two entries added.
Line numbers "l." refer to v2.

**Counts (35 merged findings).** RESOLVED 24; PARTIALLY RESOLVED 3 (M5, M11, M24); CANNOT RESOLVE 0; DEFERRED TO
GATE A, with the fix prepared and the options costed, 8 (M2, M6, M13, M16, M20, M23, M28, M30). Several RESOLVED
findings also have a default that the user confirms (M4, M15 → GA-4; M19 → GA-8; M31 → GA-7); they are marked.

**Numbers after the fixes** (script [4], [7], [8]): MUST 3,968 CPU-h; MUST + SHOULD reduced 4,401; MUST + SHOULD full
4,915 (v1: 2,950 / 3,275 / 3,798). Calendar 55.5 / 57.9 / 60.8 days (v1: 42). Capacity 174 core-h per day in
production (v1: 200). Storage 413 GB, 613 at the pre-merge cap (v1: 360 / 560).
**Propagation:** 91 instances of 26 changed budget, calendar and storage numbers across 2 files (90 in v2, 1 in COM;
counted by string search after the last script run). A search of v2 for 17 superseded values (2,950 … 407 CPU-h)
finds them only where v2 quotes v1 for comparison.

---

## 1. Category A

| # | status | what changed | where in v2 |
|---|---|---|---|
| M1 zero counts in the likelihood | **RESOLVED** | (a) Generation hypothesis fixed for Asimov data and every toy: each counted rate drawn from Gamma(m + 1) (flat-prior posterior), auxiliary observations fixed at the observed counts; derivation in four steps (posterior; identity with the classical upper limit by integration by parts; substitution m = 0 → 1.139; large-m limit); alternatives (fitted value, fixed 1.14/M, Jeffreys, fully frequentist) with the reason each is not primary; two of them reported at the best point. (b) "estimate", "bound", "no credit", "leading", B₈₄, total σ_ln and f₀ defined from the predictive distribution. (c)–(e) tests T1-c (i)–(iv) and T2-e. (f) f₀ with the reading "sample-size limited" above 0.5. Added beyond the arbiter's list: "one zero per term" (a product of empty factors would again reward depth); a one-bin analytic table computed in the script (limit 27.8 [9.4, 70.0] at κ = 35 against 3.0 if the term is dropped and 14.3 at a fixed 1.14 κ); exact one-bin coverage 0.945–1.000 | §4.11 points 1–4 and 6 (l.1091-1281); §4.12 (l.1340); script [9], [10] |
| M2 C1 blinding exception | **DEFERRED TO GATE A (GA-1)**, text corrected | Disclosure corrected to six (R07 × 3, fallback × 3 = family F). Default: sealed tier (4 open, 6 PASS/FAIL only, counts sealed to Gate B, dedicated agent). R07 and family F fixed in the T2 list in every option. States that the exception takes effect only with the user's approval. Options (a)–(e) with their cost in validation power; CPU equal (14 CPU-h) | §4.1 (l.435-465); GA-1 (l.2179); COM C1-d |
| M3 same-rung closure | **RESOLVED** | Derivation and test on disjoint rungs and disjoint samples for every closure (B1: derive R04–R05 on derivation overlays, test R06–R07 on test overlays; B2 occupancy: development sample against the direct sample; B3, B4-c: halves by seed parity; B5: sideband roads against the signal road). Same-rung comparisons relabelled "consistency check". Promotion of failers: the estimator now has an explicit promotion term Σ f_k·π_k over near-pass classes; a directly measured ceiling H = P_geo + Σ f_k is the no-credit value. I did not adopt "overlay random failers at depth": with 2,000 overlays it bounds the promoted rate at 1.14/2,000 per event, a floor far above v1's | §4.0 point 1 (l.274); §4.4 points 3–4 and "Closure design" (l.553-680); §4.17 |
| M4 extrapolation width | **RESOLVED**; convention confirmed in GA-4 | s_tot(r)² = s_model² + (b̂² + σ_b²)·d_in² + b₀²·d_out², always in the likelihood; derivation of the form, limiting cases, substitution (pile-up 0.45 at R09, 1.23 at R11, 2.44 at R14). Rule for the pile-up factors of B1 at depth: survival S = 1, promotion from the occupancy model with the width. Conditionals measured after ≥ 3 preceding rungs with a stability test (B3-d). Table of last tested rung and distances per T2 candidate. Held-out test as in M3 | §4.0 point 7 (l.336-366); §4.4; §4.6 (l.840-858); §4.12 (l.1348); script [12] |
| M5 testability, NOT TESTED | **PARTIALLY RESOLVED**; policy in GA-4 | Done: evaluable-rung rule σ_tot ≤ ln F/3 (false fail 0.27 %; power 93 % at F^1.5); expected-count table per topology and rung from the v1 record; four verdict classes; NOT TESTED earns no credit by default; "leading" decided with no-credit values. Not achieved: the brief's D4 ("a MUST item gets the statistics its criterion needs") cannot be guaranteed for PV pairs, NI and loopers. An unbiased sample with 24 PV-pair counts at R05 would need about 48,000 events (about 340 CPU-h at the rate implied by the v1 record), and R05 is a derivation rung: at the held-out R06 v1 has no PV-pair count at all, so no unbiased size can be computed. I did not add such a sample; the test overlays are enriched instead, and whether the enrichment (10²–10³ needed) exists is known only after the Phase-2 pilot. v2 states the expected verdict NOT TESTED for these terms now | §4.0 points 3, 5, 6 (l.283-334); Table 4.4b (l.663); §4.7 (B4-c); §4.12 rule 1 |
| M6 floors and central target | **DEFERRED TO GATE A (GA-3)**, redesign done | Floor table per term (Table 4.4a). One pool of 600 CPU-h for all no-pile-up samples, allocated as √(N_t/c_t): summed 68 % floor 45.3 events (single interaction 28.9, SM 16.4; predictive median 35.8, σ_ln 0.41) against 150.5 + 46.5 in v1. No ×100 growth and no ρ = 3. Biased generation: gain stated as unmeasured; kinematic ceiling 20.9 from road multiplicity; Phase-2 pilot (27 CPU-h) measures it; planning value G = 1. Outcome said plainly in §0: "middle" in size and "bounded" in kind unless the pilot or the conditionals change it. σ_ln and f₀ as reported outcomes (COM TG-1). Options: pool 315 / 600 / 1,200 CPU-h; three message options | §0 (l.36-50); §4.4 (l.604-655); §4.7; GA-3 (l.2199); script [9] |
| M7 injection, pulls, units | **RESOLVED** | Injection at 0, 1, 2, 5 × μ₉₅^exp of each of three points, 200 fluctuated pseudo-experiments per level, 20 % of the injected μ, absolute criterion at zero. Pulls on fluctuated pseudo-data; Asimov kept for constraints only. T1-b in stated units (μ₉₅ = 789.7 = 1.2458×10⁷ events before selection / 15,775) | §4.11 point 6: T1-b, T1-d, T1-e (l.1235-1268); §5.2 |
| M8 T1-g, toy budget | **RESOLVED** | Old self-consistency test removed; T1-h = coverage at a known injected signal, computed from stored test-statistic distributions (0.5 CPU-h; possible because the auxiliary observations are fixed in the toys). Both toy passes budgeted (145 + 174 CPU-h; pass 1 with five selections). Toy cost on a 60–100-parameter workspace measured in Phase 2. The 1,449 CPU-h nested-toy figure is reproduced in the script and not incurred | §4.11 points 5–6 (l.1222-1279); §11.2; script [3], [7] |
| M9 MET validation | **RESOLVED** (execution depends on retrieval R-3) | Soft term from the public source only; the tuning to v1's 25 GeV removed. New external validation against a published Phase-2 MET performance figure at pile-up 200, tolerance fixed before any multijet sample exists; no figure → "not validated" and the fail branch. (a) relabelled a continuity check with no verdict; (c) an order-of-magnitude comparison with the reference's √s and pile-up stated | §4.7 (l.910-941); COM B4-b |
| M10 stop rule | **RESOLVED** | Brief §7 (all six conditions) and D6 quoted verbatim; "approved schedule" defined; a projected overrun above 30 % stops the study and asks the user; three checkpoints; "the schedule is corrected" removed from §4.13 and "is reported" from §11.6. New COM row ST-1 | §11.6 (l.2131-2157); §4.13 risks; §12.5 item 8 |
| M11 variation sizes | **PARTIALLY RESOLVED** | Done: round-number variations are robustness tests only; nuisances take a public size (R-15, R-16, R-17) scaled linearly from the measured shift, with a linearity check; no public size → no nuisance, named as a limitation; B1-c no longer uses the ×0.5–×2 band; composition variation is a nuisance only with a sourced range. Not done: no size is sourced yet (the head node has repo access only); the retrieval is a Phase-2 task, and a nuisance may end up absent | §4.9 (l.1019-1030); §4.4 B1-c; §5.1; §6.4 |

## 2. Category B

| # | status | what changed | where in v2 |
|---|---|---|---|
| M12 nuisance propagation | **RESOLVED** | Table: each shared nuisance × {pile-up, single interaction, SM hard scatter, signal} with the sample used; P_geo and H re-measured under each variation (51 CPU-h); pile-up shifts carried to depth through the occupancy model with the width | §4.9 (l.1032-1044); §4.11 point 1 |
| M13 [DP2] | **DEFERRED TO GATE A (GA-7)** | Reduced set now E 200/1.5, E 500/3, E 500/5, E 1000/3 keV (+29 CPU-h); interpolation rule with a width for unvaried points; paired design; six-point paired alternative costed | §4.9 (l.1058-1070); §11.5 |
| M14 thinning reach | **RESOLVED** | K = 64 thinned subsets per trial; N_eff from the event bootstrap; projection from v1's bootstrap errors (gain ×19 at R06): reach R07, probably not R08; B2-c expected NOT EVALUABLE at most deep rungs, so the deep pile-up term is declared a one-estimator extrapolation with the M4 width; B2-g measures N_eff before the freeze; source of the occupancy model's fit-probability input named (finder candidates), independence claimed only for counting and width rungs. No ρ ≥ 3 | §4.5 (l.739-800) |
| M15 closure statistics | **RESOLVED**; tolerances in GA-4 | Full covariance with s_model² in every element; s_model a number fixed before the freeze from development samples; thresholds counted after the cut; size and power per test; family-wise rule (FAIL at p < 0.05/K, one fresh re-test in between): 7.5–10 % false rejection of a correct analysis at K = 12 against 46 %; retroactive v1 thinning test reported. F not loosened | §4.0 points 3–5 (l.283-327); §8 content (2); script [11] |
| M16 time tag | **DEFERRED TO GATE A (GA-9)**, design done | Timing model with collision-time spread, sourced non-Gaussian tail, out-of-time and noise occupancy; hit-level prediction; closure by moving the window edge on R04 candidates (five edges); independence from the rung at R04–R06; credit never below the sourced tail fraction; nothing sourced → no credit | §4.6 (l.860-879) |
| M17 undeclared signal quantities | **RESOLVED** | Complete list of pre-verdict signal quantities (COM BL-1): the C1 tier; A, f₂₀₀ and the migration fraction as a declared selection-independent exception; threshold change decided before A; B6 nominal ε from its own partner rows, after the verdicts; C2 optimality count moved to Phase 4c | §4.1 (l.467-485); §4.2; §4.9 "Blinding"; §4.14 (d) |
| M18 MVA argument | **RESOLVED** | The false claim removed; the three reasons that hold (blinding forbids pre-verdict training; no independent cross-check for a score; no training background beyond R08); hybrid candidate excluded for the blinding reason; working point at equal total counted background | §3.2 (l.203-232) |
| M19 costs and schedule | **RESOLVED**; schedule in GA-8 | Unit costs with a provenance column (M/D/G); no-PU hard scatter 45 ms; multijet 23.4 ms; P1 on maxwell timing (51 CPU-h) and the v1 configuration to be resolved first; QGSP_BERT and composition variations costed (52); capacity with 10 off-hours slots (1,625 slot-h per week, 174 per day in production); contingency from provenance (1,989 CPU-h) plus the 403 CPU-h reserve; table of unmeasured costs with the Phase-2 measurement for each; ITERATE allowance per panel review and Gate-B turnaround; development effort; the wrong "1,000 CPU-h" sentence replaced; per-finding delta table; non-MUST levers | §4.0 Table 4.0; §4.15; §11.1–§11.3, §11.6 |
| M20 S1 "×10" | **DEFERRED TO GATE A (GA-2)** | Stated as ×10 in total and ×5 on the limit half; 14.6 % against 10.3 % at ε = 0.045; 4,000 rows = +827 CPU-h, +4.7 days | §4.13 (l.1392-1399) |
| M21 C1 chain per point | **RESOLVED** | v1 path per point; full-chain twins of the two fast-path points (5.6 CPU-h) with the declared expectation ×0.832 / ×0.871; fallback ratio sealed | §4.1 (l.429-433); COM C1-e |
| M22 attribution | **RESOLVED** | Rule: at least half of the double-crossing layers from the topology's particles; v1's coded rule transcribed in Phase 2 and compared | §4.4 point 3 (l.553-561) |
| M23 K validations | **DEFERRED TO GATE A (GA-5)**, criteria fixed | Validation 2: fixed-order NLO against fixed-order NLO at 3 % (or resummation removed, or NOT EVALUABLE, stated); validation 3: differential K(M), 2 % or 3σ; parity argument written; resummed normalisation implemented as cross-check and quoted beside every limit | §4.14 (l.1455-1483) |
| M24 Herwig, DPs in the paper | **PARTIALLY RESOLVED** | Done: [DP5] rewritten as attempt first (conda-forge install on a worker, then one source-build attempt, then published data with the failure documented); how each DP is carried into the paper. Not done: the install itself (workers and install slots are outside the fixer's remit) and a quantified expected impact (no number in the repo; retrieval R-19) | §11.5 (l.2101-2108); §7; §5.1 |
| M25 identifiers | **RESOLVED** | COM is the master; v2 quotes its identifiers; COM has the old → new table | all of §4; COM |
| M26 background list | **RESOLVED** | Table 2.1 rows and a reading for pile-up-vertex secondaries (upper estimate ~10³ vertices per crossing; density covered by the top-up, correlation not; 1,000-event test with a 10 % threshold and a conditional cost of +160 CPU-h), noise and out-of-time hits (R-18 against the top-up), δ-rays and merged clusters (limitation L8) | §2 (l.147-170); COM B1-g |
| M27 signal detector response | **RESOLVED** (two parts depend on retrieval) | Same MET model for signal, nuisances correlated; migration measured on a 150 GeV sample (7 CPU-h) with a 5 % rule; calorimeter, muon-system and lepton-veto assumption stated as L11 with the limit quoted against an assumed veto survival; tracker hit-time window from R-14 as a systematic at ≥ 1 TeV (L12 if not sourced) | §4.13 (l.1417-1438); §1 |
| M28 infracolour correction | **DEFERRED TO GATE A (GA-5)** | Formula with substituted values (α_IC = 0.045; +3.3 / +6.3 / +13.3 % at β = 0.7 / 0.5 / 0.3) reproduced in the script; averaged over the generated β per mass in Phase 2; default one-sided band; retrieval R-12 for its treatment in the literature. The formula is taken from the review and the arbiter, tagged as such, not as a literature value | §4.14 (a′) (l.1484-1496); script [13] |
| M29 T2 background-side bias | **RESOLVED** | 50 bootstrap replicas of the background inputs for the five best candidates (14.5 CPU-h); frequency of the same winner and shift of B₈₄; rule if the winner wins in fewer than half | §4.12 (l.1354-1359) |
| M30 dE/dx | **DEFERRED TO GATE A (GA-6)** | Forgone-gain ratio ε(R_k + dE/dx)/ε(R_k) after Gate B; the modelling option costed at about +390 CPU-h and a week | §4.12 [SD9]; GA-6 |
| M31 B5 | **RESOLVED**; [DP1] in GA-7 | Closure on the truth-attributed hard-scatter component; T(Δφ) on no-pile-up hard-scatter samples (10 CPU-h, both variants); pile-up sample kept for independence; [DP1] loss restated including R07 (7.7 counts) | §4.8 (l.970-1010) |
| M32 weighted samples | **RESOLVED** | One auxiliary channel per weight class; effective counts where weights vary; zero counts with the class weight | §4.11 point 1 (model table) |
| M33 multijets | **RESOLVED** | Factorisation from a looser population (10⁶ events, 12.5 CPU-h), tested on Z(νν) and W in MET bins; fallback stated | §4.7 (l.943-949); COM B4-e |
| M34 failure after the freeze | **RESOLVED** | Three-branch protocol; one reserved fresh direct sample (403 CPU-h), fresh test overlays from the contingency | §8 (l.1820-1836); COM FP-1 |
| M35 sample inventory | **RESOLVED** | 24 samples: size, seed stream, role (development / derivation / test / production / reserve), independence, phase, CPU-h | §4.17 (l.1564-1604); COM INV-1 |

## 3. Category C items

| item | status | where |
|---|---|---|
| P-C3 top five with toys | applied | §4.12 rule 4; script |
| P-C4 PDF4LHC21 | applied (nominal if it installs; CT18NLO as variant) | §4.14 [SD11] |
| P-C5 FxFx at 1,500 GeV | applied (+20 CPU-h) | §4.14 (b) |
| P-C6 like-for-like efficiency breakdown; 300 fb⁻¹ label | applied | §6.2; COM REF-1 |
| P-C7 B7 threshold; beam gas, satellites | applied | §4.10 |
| P-C8 literature retrieval | scheduled as R-20 (not done by the fixer: repo access only) | §6.4 |
| K-C1 tags | partly: the cited cases corrected ("34 ms" as derived; D4-sourced values as [U]); I did not re-audit every [V] tag of the text kept from v1 | Table 4.0; §4.1; §4.13 |
| K-C2 citation slips | applied (halo l.321; PLAN l.166; union closure is the T_seed = 6 pilot) | §4.10; §2; §4.5 |
| K-C3 [DP4] cost | applied: trials are 78 % of a four-road event; S4 ≈ 700 CPU-h | §4.16; script [6] |
| K-C4 software size | applied | §11.4 |
| K-C5 dump storage; ρ = 2 at 4.0 MB | applied (10,000 dumps; 16 GB) | §11.4; script [8] |
| K-C6 ρ = 2 at 5 GiB | applied | §4.5 |
| K-C7 Geant4 vertex yield | applied and found larger than a wording issue: v1's 10⁸ guns gave 5×10⁶ vertices for more than 2×10⁷ events; resized to one distinct vertex per event (+60 CPU-h) | §4.4 risks (4) |
| K-C8 pruning policy | applied | §4.11 T1-f |
| K-C9 binomial chain | applied: nested chains collapse to one count; Poisson for m/M < 0.1 | §4.11 point 1 |
| K-C10 σ_ln target as reported outcome | applied | §4.11 point 3; COM TG-1 |
| 4-fermion comparison for tt̄ and dibosons | stated as a limitation (no second generator) | §4.7 item 4; §5.1 |
| N-C-1 Gate-A sheet | applied as §12.1 (GA-1…GA-10); it is three pages, not one: the orchestrator's `GATE_A.md` should condense it | §12.1 |
| N-C-2 paired B6 | applied | §4.9 |
| N-C-3 G from v1 row arrays before the freeze | applied | §4.12 rule 4 |
| N-C-4 baseline and partial-outcome matrix | applied | §4.12 |
| N-C-5 supporting figures | applied | §9 |
| N-C-6 idle capacity, early starts | applied (100 CPU-h of development samples; Phase-2 starts listed) | §11.3 |
| N-C-7 Geant4 on three workers | applied | §4.4; [A7] |
| N-C-8 dump storage | applied | §11.4 |
| N-C-9 R2 background as sanity comparison; R-10 before 4a | applied | §4.7; §6.4 |
| N-C-10 levers | applied | §11.6 |
| N-C-11 §0 carries the outcome and the largest decisions; length | §0 done; the document is longer, not shorter (2,391 lines) | §0 |
| Arb-C1 efficiency estimator | applied: (k + ½)/(n + 1) at every point, sensitivity reported | §4.12 rule 3 |

## 4. Decisions prepared for Gate A (v2 §12.1)

GA-1 C1 comparison and blinding; GA-2 signal rows; GA-3 paper message and pool size; GA-4 tolerances, eligibility,
NOT TESTED, extrapolation convention; GA-5 σ_norm and the infracolour correction; GA-6 dE/dx; GA-7 downscopes;
GA-8 schedule and approved compute; GA-9 time tag; GA-10 endcap wording. Each has a default, alternatives and costs.
None was decided here.

## 5. Checks made (protocol steps 4, 6, 7)

**Verify.** Every formula added was checked with substituted values and a limiting case, in the script where it is
arithmetic: the geometric marginal (normalisation and mean), the Gamma quantiles (1.139 at 68 %), the one-bin limits
(3.00 at κ → 0 for all three conventions), the evaluable-rung thresholds, the family-wise rates, the extrapolation
widths, the allocation rule (reproduces the constructive review's 150.6 → 67.5 on v1's four topologies: 150.5 →
67.4), the infracolour numbers (reproduce the reviewer's +3 / +6 / +13 %).
**Regression.** Script exit code 0; two full runs after the last edit to it give identical output (fixed random seed). v1 strategy file not modified.
COM: all 102 plan and strategy rows `open`; S3 `dropped (user)`, S4/S5 `undecided`, NA-1 `n/a`, as before. Fixed
user decisions not reopened: no endcap, no cloud, no pile-up scan, no Open Data, no ρ = 3, no ×100 growth, no string
at Λ ≥ 15 keV; C1 subset unchanged; the freeze stays before any production sample.
**Neighbourhood.**
1. After M19 (one unit cost below its own ingredient): every unit cost of Table 4.0 compared with the feasibility
   lines I read. Found: the Geant4 gun budget too small for the events it feeds (fixed); multijet and P1 (arbiter);
   "34 ms" tagged as measured (fixed). Not re-checked: costs whose source I did not open (FEAS_C lines).
2. After M17 (undeclared signal quantities): every place where a signal number is formed. Found: B6 needs nominal
   partner rows that were not budgeted (+18.5 / +38 CPU-h, added); the V4-5 event selection could reveal a pass
   fraction through the number of rows scanned (output restricted); the tracker hit-time loss is a signal quantity
   (formed after the verdicts).
3. After M5 and M15 (thresholds): all "≥ 20" and "≥ 30" thresholds of v1 (B1-a, B3, B4-c, B5-a) replaced by the
   evaluable-rung rule; the B2-c band (which allowed a factor e² = 7.4) replaced by the common criterion; v1's
   listed lever "B2 direct at 12,000 events" withdrawn because R07 would no longer be evaluable.
4. After M3 (same-sample derivation): all closure tests checked for a disjoint test sample; B4-c needed a parity
   split of the hit-level samples (halves the Z(νν) test count to about 200, still evaluable).
5. After M1 (a term vanishing at a boundary): the product of two empty factors and the signal points with zero
   passing rows have the same structure; "one zero per term" and the single efficiency estimator address them.
6. After M10: the document was searched for other softened rules; the second instance (§4.13) and the failure list
   (§12.5) were corrected.
7. Self-check: my first draft of the eligibility rule let a term with a FAILED estimator enter at its no-credit
   value with the selection still eligible. That is looser than v1's [SD8]; restored (FAIL → not eligible where the
   term is leading; only NOT TESTED / NOT EVALUABLE → no credit). Logged in the session log.
8. One attribution of mine was wrong while drafting ("the conventions' 10 % threshold"; it is the arbiter's) and was
   corrected before finishing.

## 6. What a re-reviewer may contest

1. **b₀ = ln F per rung, coherent, in cut families with no tested rung** (§4.0 point 7). It is a convention, anchored
   only to v1's 0.36 per rung. It makes extrapolated factors nearly worthless beyond R11. Alternative in GA-4.
2. **The promotion model and the ceiling H** (§4.4) are a new estimator design, larger than a minimal fix. I judged
   that the arbiter's own remedy (overlay random failers) would leave an unusable bound at depth. The size of the
   near-pass classes, hence of H against P_geo, is unknown until the pilot.
3. **Flat prior**: exact one-bin coverage dips to 0.945 at small κ·λ; the coverage criterion is "≥ 0.93 on 500
   pseudo-experiments", which a reviewer may find loose.
4. **Auxiliary observations fixed in the toys** (Cousins–Highland style) rather than redrawn. It is what makes T1-h
   cheap; the coverage tests redraw them.
5. **M5 / brief D4**: PV pairs, the largest floor, are expected NOT TESTED, and the default lets the term in at H.
6. **Floors**: 45 events is a sum of 68 % upper values of 20 terms at G = 1; the "middle, bounded" outcome is the
   expected one, and the paper's planned message ("estimated, not bounded") is at risk. The 600 CPU-h pool is my
   choice among 315 / 600 / 1,200.
7. **Calendar of 8 weeks** against a 2–4 week target, with 44 days outside production; the ITERATE allowances are
   2 days each.
8. **Contingency of 1,989 CPU-h** by a 10 / 30 / 100 % rule of mine; the stop rule may trigger at day 7.
9. **Pieces that rest on retrieval not yet done** (M9, M11, M16, M27, M28): if a public number is not found, the
   item falls back to "not validated / no nuisance / no credit", which is stated but weakens the result.
10. **Length**: v2 has 2,391 lines against 1,248.
