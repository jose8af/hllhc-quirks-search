# Critical review — Phase 1 STRATEGY (quirks v2)

Reviewer: Celeste (critical, "bad cop"), 2026-11-13 18:20. Role: `agents/critical_reviewer.md`.
Under review: `phase1_strategy/outputs/STRATEGY_brigitte_2026-11-13_17-55.md` ("STR", 1,248 lines, read in full),
`COMMITMENTS.md` ("COM"), `phase1_strategy/src/strategy_budget.py` (run with `python3 -I`).
Also read: brief `prompt.md` (§3 D1–D10, §6, §7), `LOG.md`, `DEVIATIONS.md`, `FRAMING.md`, `publication_plan.tex`
l.125-131 and l.258-395, `conventions/search.md`, `methodology/03-phases.md` (Philosophy, Phase 1), `04-blinding.md`,
`06-review.md` §6.1–6.4.1, `12-downscoping.md`, digests D4 (l.150-449), FEAS_A (full), FEAS_B and FEAS_C (cited parts),
`benchmarks_chain.json`, `STAGE4_SUMMARY.json`, `STAGE3_INDEX.json`, `C12FC_v1/acceptance.json`, and the v1 lines cited by STR.
No RAG corpus (deviation V8); literature checks used the repo files cited by STR §6.
Scope: Strategy phase, no figures exist, so the figure checks of the template do not apply.

**Overall.** The arithmetic is honest and reproducible: every CPU-h, storage and capacity number of §0, §4 and §11
is regenerated exactly by `strategy_budget.py`, and the 20 measured unit costs I traced back to the benchmark JSON or the
feasibility reports match. The coverage of the brief is complete at the level of item names. The weaknesses lie in the
statistics (T1/T2), in the independence and testability of the closure tests, and in the scope of the blinding exception.
Several criteria as written cannot fail, cannot be evaluated, or reward a lack of simulated statistics.
**Counts: 8 Category A, 16 Category B, 10 Category C.**

---

## 1. Findings

### Category A (must resolve)

**A1. T1 + T2: in the expected limit, a zero-count term is treated as zero background, and the selection rule
favours selections with the least simulated statistics.** (STR §4.11 l.611-625; §4.12 l.678-690; COM T1-a, T2-a)
- *Evidence.* [SD7] puts each simulated count m in an auxiliary channel m ~ Pois(γ), with γ an unconstrained
  normalisation that scales the background sample, B_t ∝ γ·N_t/M (l.613-623). For m = 0 the maximum-likelihood value is
  γ̂ = 0. Expected limits use Asimov data or toys generated at the fitted nuisance values ("asymptotic … for the T2
  ranking", l.641; T2 G uses "the median expected CLs limit from T1 (asymptotic)", l.681). With γ̂ = 0 both give a term
  that contributes exactly zero to the pseudo-data, and Pois(0) never fluctuates. So in "toys fluctuate the simulated
  counts too" (l.625), the toys do not fluctuate the zero counts. A selection whose leading terms are all zero-count
  therefore gets the B = 0 expected limit (about 3 events / S), whatever M is.
- v1 avoided this with hybrid toys and log-normal widths: `limits.json` bins b = 4.51e5 / 5.91e5 events, σ_ln 1.75 / 2.71
  at the best point (D4 l.338). With the auxiliary-channel construction, the 0/24 PV-pair bound that dominates SR-G there
  (D4 l.340) would contribute nothing.
- T2 picks the lowest G (l.680-684). Its candidates run down to R20 (l.668), where every B1/B3/B4 factor is expected to be
  zero-count (STR l.395: 10⁷ no-PU events bound P_geo only at ≈10⁻⁷). The rule therefore prefers the deepest selection.
- Eligibility [SD8] counts "leading terms (those above 10 % of its total background)" (l.678-679). When the fitted
  backgrounds are 0, the leading terms are not defined.
- The "background-free" flag B₈₄ ≤ 0.11 (l.689) has no v2 definition of B₈₄ in T1.
- This is the circular pattern the template warns about: the less the simulation can count, the better the expected
  sensitivity looks.
- *Fixed means:*
  - expected-sensitivity pseudo-data and toys drawn from the prior-predictive (posterior Gamma(m+1) for γ, as v1's
    hybrid), or a declared nominal at the 68 % upper value, applied the same way to all 16 candidates;
  - "leading term" and B₈₄ defined from that distribution, not from γ̂;
  - a limiting-case check in T1-b: the deepest candidate with all-zero counts must not get a better G than it would
    with those terms set at 1.14/M.
  - Because T1 is a "go up" task in the brief (§4), this needs an explicit statistics design note before Gate A.

**A2. The C1 blinding exception is larger than disclosed: 6 of the 10 signal quantities, not 3, are efficiencies of v2
candidate selections.** (STR §4.1 l.257-259, l.282-294; COM C1-d)
- *Evidence.* STR says "Three of the ten quantities (the R07 counts) are also efficiencies of a v2 candidate selection"
  (l.292).
- But T2 family F is "v1 fallback without dE/dx, width cut W_c/2^k from the frozen admissibility table per hypothesis,
  FB(k_adm)" (l.669). At the C1 points that is exactly the v1 fallback being reproduced:
  - `STAGE4_SUMMARY.json` → `fallback_points["A2|F|200|1.5|BM"]`: `r_fb = "FB2&h>5&o>5"`, `k_adm = 2`, `e_adm = null`
    (no dE/dx), `k_rfb = 9`, `n_den = 200`;
  - D4 l.317-322: FB3 at E200 2 keV and at E500 3 keV.
- So FB2/FB3 (9, 10, 11 of 200) are T2 candidate F without the veto, at 3 of the 20 G-window points (all three C1
  points lie in the window of l.680). Six of ten quantities are v2 candidate efficiencies, two of them for the
  family-F candidate that v1 actually used.
- The pre-registration may still shorten the T2 list after these numbers exist (l.290-291, l.674-675).
- *Fixed means:*
  - the disclosure corrected to six, in STR, COM C1-d and the planned paper text;
  - a rule that no T2 list change after C1 may remove or keep a candidate in family F or the R07 member;
  - or the FB columns dropped from C1 (their resolving power is "gross check only" anyway: D4 l.398-400 gives a minimum
    detectable effect ≈ 65–75 %).

**A3. The B1 closure test is close to tautological, and the estimator is undefined where it is used.** (STR §4.4
l.357-362, l.373-376; COM B1-a)
- *Evidence.* C_PU is "the ratio of the pass probability with pile-up overlaid to that without, measured by overlaying
  no-PU events that pass a loose rung on independent pile-up events … at rungs where both have counts" (l.359-361).
- The closure compares P_geo × C_PU with a direct full-PU sample at R05, R06, R07 (l.373-375), which are the same rungs
  where C_PU is measured. A topology overlaid on pile-up and a topology generated with pile-up are the same physics.
- At R05–R07 the test therefore checks the overlay technique and statistics. It does not check the factorisation.
- The working selections are R09–R20 (T2 list, l.668). At those rungs C_PU cannot be measured (no counts), and STR never
  says how C_PU(r) is obtained there: carried from R07, a fit, or a model.
- This is the conventions pitfall "blind spot in VR coverage" (`search.md` l.142-145) in its strongest form. [L6] names
  it but gives no remedy for B1. The cross-check offered for pile-up (two independent estimators, B2-b) has no B1
  analogue.
- *Fixed means:*
  - the C_PU extrapolation rule written down (functional form and inputs);
  - a closure that tests the extrapolation: C_PU measured on R04–R05 only and predicting R06–R07 direct counts,
    declared now;
  - the extrapolation uncertainty entering s_model.

**A4. Several MUST criteria cannot be evaluated with the planned statistics, and the verdict "not testable" earns
credit, which contradicts the eligibility rule.** (STR §4.4 l.373-380, l.392-394; §4.6 l.488-492; §4.5 l.441-445;
§4.7 l.539-540; [SD8] l.678)
- *Evidence, from v1's C′_PU counts per 500 events (D4 l.196-200) scaled to the B1 sample sizes (l.392):*
  - DIF at 6,000 events: R06 ≈ 24, R07 ≈ 12;
  - γ: R07 ≈ 24;
  - V⁰ at 1,000 events: R06 ≈ 12;
  - PV pair: 1 count at R04 per 500 and 0/24 at R06 → about 12 at R04 and ≈ 0 at R06;
  - NI and looper: none (looper 0/10⁵ even without PU).
- Consequences:
  - B1-a with "N ≥ 20" tests R05 only, or nothing, for 5 of 8 topologies. That includes the PV pair, which dominated
    v1's best point.
  - B1-b (a slope over the rungs with counts) has 1–2 points for those topologies, so it is undefined.
  - B3: a conditional with no direct counts is "not testable" and "earns credit only as a measured no-PU number"
    (l.491-492). So untested credits enter the likelihood. [SD8] makes a selection eligible only if every criterion of
    its leading terms has the verdict PASS; whether "not testable" or B2-b "cannot be evaluated" (l.443-444) counts as
    PASS is not stated.
  - B4-c: v1 tt̄ 1ℓ 5.2 and W(τ_ℓ) 3.0 weighted counts at R06 (D4 l.193-194) mean that only Z(νν) can be tested at R06.
- COM B1-a still states "closure … at R05–R07 per topology". COM therefore promises a test that the statistics do not
  allow.
- *Fixed means:*
  - a per-topology and per-process table of expected direct counts at each rung, from the v1 record, with the rungs
    actually testable;
  - sample sizes raised where the term is leading (PV pair, V⁰), or the lack of a test stated as a limitation;
  - a third verdict class, NOT-TESTABLE, with its consequence under [SD8] fixed now (recommended: not eligible as a
    leading term, or a declared width of at least ln F).

**A5. The signal-injection criterion passes whatever the fit does.** (STR §4.11 l.650-651; COM T1-b; conventions check 2)
- *Evidence.* T1-c injects 0, 1, 2 and 5 × σ_norm and passes if the fitted μ is "within 20 % … or within its fit
  uncertainty where that is larger".
- At v1's best point μ₉₅/N_exp = 789.74 (`STAGE4_SUMMARY.json` → `fallback_points[...].mu95_over_Nexp`). The fit
  uncertainty on μ is then of order 10²–10³, and any fitted value within that of the injected 1–5 passes. The check has
  no resolving power wherever μ₉₅^exp ≫ 5, which is every v1 point.
- Related (Category B part): T1-d checks pulls "on Asimov data", where pulls are zero by construction.
- *Fixed means:*
  - injection at fixed multiples of the expected limit at each tested point (e.g. 0, 1, 2, 5 × μ₉₅^exp), on fluctuated
    pseudo-data, with a bias threshold of 20 % of the injected μ and the number of pseudo-experiments stated;
  - pulls and constraints evaluated on fluctuated pseudo-data (the Asimov pass kept only for constraints).

**A6. T1-g is either tautological or a large unbudgeted cost.** (STR §4.11 l.654-657; COM T1-b; `strategy_budget.py`)
- *Evidence.* T1-g: "in 500 background-only pseudo-experiments … the fraction whose limit lies below the quoted median
  expected limit is 50 % within ± 4.5 %".
- If the median expected limit is taken from the same background-only ensemble, 50 % holds by definition.
- If each pseudo-experiment gets a toy-based limit as T1 requires ("toys are primary for every quoted limit", l.641),
  the cost is 500 × 2 points × 8 μ × 652 s = 5.2×10⁶ s = **1,449 CPU-h** (my arithmetic, with STR's own unit costs,
  l.204 and l.643). That is 49 % of the MUST total of 2,950, and it is absent from `strategy_budget.py` (its only toy
  line is 960 × 652 s = 174 CPU-h).
- *Fixed means:* T1-g defined as a coverage test against an independent quantity (e.g. toy-based expected band against
  the asymptotic band, or limit coverage at a known injected μ), with its cost in the script, or removed.

**A7. The MET-model validation (a) is tuned to pass.** (STR §4.7 l.522-528; COM B4-b)
- *Evidence.* The soft term is built "with a resolution that reproduces v1's 25 GeV smearing" (l.522-523). Validation
  (a) then requires that "on Z(νν)+jets the reco-MET selection reproduces the yield of the v1 selection (truth MET with
  25 GeV smearing) within 10 %" (l.527-528).
- A parameter set to reproduce v1 and then checked against v1 cannot fail. This is the "never adjust parameters to
  match" rule (03-phases l.56-70).
- It also contradicts l.524-526: "No parameter value is quoted here … retrieval tasks (R-3) … from public Phase-2
  documents".
- *Fixed means:* the soft-term resolution taken from the public source (R-3) only, and validation (a) restated as a
  comparison with an independent public number (e.g. a published Phase-2 MET resolution against pile-up), or dropped
  as a validation and kept as a reported difference from v1.

**A8. The 30 % compute rule of the brief is weakened.** (STR §11.6 l.1161, §4.13 l.729-730; brief §7 l.347, D6 l.79)
- *Evidence.* Brief §7: "Stop and ask the user if … the projected compute overruns the approved schedule by more than
  30%"; D6: "every overrun of the approved schedule is reported".
- STR l.1161: "Any overrun of more than 30 % of the approved compute is reported". STR l.729-730: re-timed costs
  differing by more than 30 % mean "the schedule is corrected".
- COM has no row for either rule.
- A user invariant has been turned into a weaker one. Given B2 below (about 1,000 CPU-h of the budget rests on guesses
  or one-event measurements), the rule is likely to trigger.
- *Fixed means:* STR and COM state: every overrun reported; a *projected* overrun above 30 % stops and asks the user;
  the re-timing on the first Phase-2 jobs is a checkpoint against that rule.

### Category B (must fix before PASS)

**B1. The MVA infeasibility argument is overstated.** (STR §3.2 l.158-176, [DP3])
- STR says "none of [the three estimators] applies to an arbitrary score" (l.161-162). That is not true for two of the
  three:
  - B3 measures P(pass cut | topology, preceding rungs) on no-PU samples for any per-candidate cut (l.481-482). A score
    cut is such a cut.
  - Thinning redraws hit subsets and re-runs the grouping (l.420-421), so candidate-level variables, and hence a score,
    are recomputed per subset; v1 already did this for width and χ² rungs.
- Only the occupancy model is tied to per-layer structure. The real constraint is therefore that a score cut loses the
  independent pile-up cross-check B2-b.
- *Fixed means:*
  - restate the constraint that way;
  - consider a hybrid T2 candidate (ladder rung, then a BDT score treated as a B3-type conditional), or document why
    not;
  - keep the measured-gain report.
- The deferral of the comparison to Phase 4c ([SD2]) is acceptable only with this corrected justification.

**B2. Unmeasured or underestimated costs are presented as known; the 20 % contingency does not cover them.**
(§4.7 l.543-545, §4.11 l.639-645, §4.15 l.795-796, §11.2)
- No-PU hard-scatter at 15 ms per event (l.544): the measured Pythia shower alone is 23.4 ms for Z(νν)+j (FEAS_B l.117),
  before Fatras and the finder (the 10-µ gun is 14.1 ms, FEAS_A l.235). A realistic ≥ 40–50 ms gives 170–210 CPU-h
  instead of 62.5.
- Multijets at 10 ms per event (l.545): also below the 21–23 ms shower.
- Toys:
  - the 174 CPU-h cover one toy campaign, but STR needs two (4b: three best on the optimisation half, l.685-686;
    4c: final limits on the evaluation half, COM T1-c);
  - [L4] says this may double.
- P1 B*-off: 970 paired events at 5 keV × 2 × 67.8 s = 36.5 CPU-h on maxwell numbers, against 16 obtained by converting
  an M3 time with the 3.4 numba ratio (l.795-796, script l.53). Brief §5.4 says "convert … with measured benchmarks,
  never by assumption". Also, v1's 0.84 M3 CPU-h for 171 events is inconsistent with v1's own 32.3 s per event at
  5 keV (`STAGE3_INDEX.json` p2/F_m500/L5_BM: 171 × 2 × 32.3 s ≈ 3.1 h). Resolve which configuration the test uses.
- Not costed at all: the B1 physics-list (QGSP_BERT, §5.1 l.833) and material-composition variations (l.403-405).
- Signal-row cost: 25.2 s per row is a sum of parts and is applied to 1,158 CPU-h of S1/B1/B4/C1 rows (script
  l.57-84); FEAS_A open issue 6 says the injection mode is not benchmarked.
- Together this is ≳ 500 CPU-h of identified extra cost (≈ 15 %) beside about 1,000 CPU-h resting on one event, toy
  kinematics or guesses.
- *Fixed means:* these lines corrected in the script; a table of each cost's provenance (measured / derived / guess);
  a contingency sized from it, or an explicit Phase-2 re-costing checkpoint tied to A8.

**B3. Correlated nuisances have no propagation path.** (§4.9 l.577-580 vs §4.11 l.628-632; §5.1 l.833)
- B6 propagates each variation "to the pile-up rate at R04–R06 and to the signal efficiency" only.
- T1 lists "material across NI/DIF rates and signal" and "hit resolution and inefficiency across signal and
  backgrounds".
- Neither the material ×0.5/×2 effect on single-interaction rates and P_geo, nor the resolution/inefficiency effect on
  B1/B4 terms, is evaluated anywhere.
- *Fixed means:* for every shared nuisance name, the samples and rungs on which it is evaluated, per term, with cost.

**B4. The schedule's driver is misattributed and the calendar is optimistic.** (§11.1, §11.3, §11.6)
- The 42-day calendar has 11.3 production days (l.1114). The remaining 30.7 days are development, freeze and reviews.
  Four weeks (28 days) cannot be reached even with zero production, so "A 4-week schedule would need production near
  1,000 CPU-h" (l.1155) is arithmetically wrong.
- No time is allotted to the expected ITERATE cycles at five review points (freeze, 4a, 4b, 4c, 5), nor to human-gate
  turnaround.
- The capacity model uses 12 slots off-hours, but `LOG.md` l.25 caps landau and schrodinger at 3 jobs (graphical
  sessions). With 10 slots: 5 × (11 × 9 + 13 × 10) + 48 × 10 = 1,625 slot-h per week = 232 per day, so 174 per day at
  0.75, and 4a production takes 2,249 / 174 = 12.9 days.
- The utilisation factors 0.50/0.60/0.75 are not measured.
- *Fixed means:* corrected statement for the user; an explicit review and iteration allowance; the lower end of the
  range justified or moved (5 weeks looks unreachable).

**B5. S1 "×10" is ×5 on the statistic that sets the limit.** (§4.13 l.706-708; PLAN l.371; COM S1-a)
- v1's limits used the 180–200 template-half rows (`C12FC_v1/acceptance.json` → `points[*].factors.finder_note`:
  "over every TEMPLATE-half … counting row"; D4 l.298).
- v2's 2,000 rows are split 1,000/1,000, and the limit uses the 1,000-row evaluation half, i.e. ×5.
- S1 has no quantitative statistical criterion tied to the limit (S1-d is "only reported").
- *Fixed means:* either 4,000 rows per point (+561 CPU-h chain, +266 Stage 3), or a logged [D] stating "×10 total, ×5 on
  the evaluation half", with the lost precision (15 % → 11 % at ε = 0.045 by the script's binomial).

**B6. The closure-criterion construction makes the p > 0.05 test vacuous at the cap.** (§4.0 l.213-221)
- With s_model = ln F, condition (a) |ln r| ≤ ln F at each rung implies χ² ≤ n_rungs, e.g. χ² ≤ 4 for 4 rungs, so
  p ≥ 0.41. Condition (b) then adds nothing.
- F is not derived from the statistical power: B2 direct precision at R04–R06 is ≈ 1 % (D4 l.389), against F = 1.5.
- B2-b's "within twice the combined width, width ≤ 1.0" accepts estimators that differ by up to e² = 7.4.
- *Fixed means:* s_model a number fixed in the pre-registration from development-sample closure before production,
  with the rule that (b) is evaluated at that value; F and the B2-b band justified from the σ_ln target and the
  expected precision at each test rung.

**B7. Signal quantities computed before the verdicts and not declared.** (§4.13 l.710-718, §4.14 (b), (d) l.755-772;
§4.9 l.588)
- The acceptance A = ε_fid × ε_trig × ε_presel and f₂₀₀ are factors of the signal efficiency
  (`acceptance.json` finder_note: "eps_total = A x eps_finder"). They are computed in Phase 2.
- The offline MET threshold may be changed before the freeze (l.770-772) while A is known.
- B6's ε_var/ε_nom does not say which half supplies ε_nom. The evaluation half before Gate B would breach [SD14].
- *Fixed means:* an explicit blinding exception for A and f₂₀₀ (selection-independent across the T2 list), the
  threshold decision logged before A is computed, and B6 nominal taken from the optimisation half or own rows.

**B8. The C2 "optimality" count is an undeclared signal quantity.** (§4.2 l.316; contradicts §4.1 l.285 "exactly the
ten signal quantities" and COM C1-d)
- *Fixed means:* the count added to the declared list, or removed.

**B9. The chain used for C1's fast-path points is not stated.** (§4.1 l.257-259)
- v1's E200 1.5 and 2 keV values come from the fast path (D4 l.317-318). The full chain shifts R04 by ×0.832 and the
  fallback by ×0.871 (D4 l.342-343), below the 400-row resolving power (STR l.276).
- If C1 runs the full chain there, the test compares two chains and is not a reproduction.
- *Fixed means:* the path stated per point, and the expected shift declared if the full chain is used.

**B10. B1 direct counts need a truth-attribution definition.** (§4.4 l.373-375)
- Pile-up-only planes pass R05 at 49.72 per trial (C1 table, l.249). Unattributed direct counts would be dominated by
  pile-up. v1 used attributed counts (D4 l.196).
- *Fixed means:* the attribution rule stated as part of B1-a.

**B11. The time-tag conditional [SD6] has no adequate closure test.** (§4.6 l.486-491)
- The B3 template (no-PU × C_PU against direct) does not fit a probability that is produced by pile-up hits.
- Applying the loose-rung late-hit fraction at deep rungs assumes independence from the geometric rungs.
- STR itself says the credit "can move the SR-T background by orders of magnitude" (l.1198-1199).
- *Fixed means:* a dedicated test of independence (late-hit fraction against rung, R04–R07, on the 96,000 direct
  trials) with its own tolerance.

**B12. S2 validation 2 compares unlike quantities, and method parity on σ_norm is not argued.** (§4.14 l.742-754, [SD11])
- MG NLO is compared with NLO+NLL/NNLL tables at 10 %. The tables v1 used are 13 TeV NLO+NLL and 13.6 TeV
  NNLO_approx+NNLL (`retrieval_log.md` entry 4). The implied K rises from 1.06 to 1.29 with mass
  (`theory_signal_model.md` l.163), so a correct NLO computation can fail at 1 TeV and wrongly trigger the
  v1-transcription fallback.
- 03-phases l.211-218 names "NLO+NLL vs NLO" as a method-parity case. [SD11] applies NLO only, against FEAS_B's
  recommendation (σ_NLO × NNLL/NLO).
- *Fixed means:* compare NLO with NLO (if the tables give it) or include the resummation in the comparison; adopt the
  ratio, or justify NLO-only as parity with the cross-check implemented.

**B13. [DP5] (Herwig) does not follow JFC 12, and the downscopes are not carried to the paper.** (§5.1 l.831, l.840;
§11.5 l.1146)
- String against cluster hadronisation is a required conventions source (`search.md` l.93). It matters here through K/π,
  hence the DIF rate, a leading term (STR l.840).
- "Only if Herwig installs without a source build" declines the attempt in advance, and the lost gain is not quantified.
- STR never states that [DP1], [DP2] or [DP5] go into the paper's method, systematics and Future Directions sections
  (JFC 12 step 4). Only [DP3] does (l.173).
- *Fixed means:* attempt the install (or record a documented failure), quantify the expected impact (published
  Pythia/Herwig K/π differences), and state for each DP how it is carried into the paper.

**B14. [DP2] leaves 9 of the 20 G-window points without any detector variation.** (§4.9 l.590-593)
- The reduced B6 covers E 200/500 at 1.5/3 keV only. 5 keV and E 1000/1500 are in the T2 window (l.680-681).
- How the shifts are applied there in T1 is not stated.
- My estimate of the pooled ε-ratio error for the reduced set is √(2 × 0.8 / (0.2 × 1,200)) = 8.2 %, against 5.2 % in
  the full form. That sits close to B6-a's own 10 % completeness limit.
- *Fixed means:* the extrapolation rule for unvaried points, and its width, stated.

**B15. Criterion IDs differ between STR and COM.** (STR B2-a/b/c and T1-a…g against COM B2-a…e and T1-a/b/c)
- The same label means different tests in the two files, which defeats the Phase-4 [D] traceability audit.
- *Fixed means:* one ID per criterion, used in both files.

**B16. T1-d checks Asimov pulls, which are zero by construction.** (§4.11 l.651-652)
- See A5. Pulls must come from fluctuated pseudo-data.

### Category C (suggestions)

- **C1.** Numbers tagged [V] whose source is a digest, against the tag rule of STR l.11-13: "FB2 9 of 200 [V: D4]"
  (l.257), "v1: 180–200 [V: D4 §4.1]" (l.706). The values are correct (SUM `k_rfb = 9`, `n_den = 200`). Also
  "34 ms … [V]" (l.200): FEAS_B l.129 lists it under "Derived (ESTIMATE …)".
- **C2.** Citation slips:
  - halo 2.6 ± 0.2 is at `experimental_status_2026.md` l.321, and l.147 is a different subject (STR l.600-601);
  - PLAN "4.9 decades" is l.166, not l.167;
  - the union closure 0.654 (G3_REPORT l.77-90) is the T_seed = 6 pilot (D4 l.289), not "the same thinning" as v1
    production.
- **C3.** [DP4] "trials are ≈ 45 % of a B1-type event" (l.808): 4 × 11.71 / 60.4 = 78 %; 45 % applies to a one-trial row.
- **C4.** "Software on the NFS home is 0.58 GB" (l.1136) counts only `sw/` (FEAS_B l.55). The pixi environments in the
  home are not included.
- **C5.** Storage:
  - dumps are budgeted for 5,000 events, but C2 (700) + B5 (6,500 reduced, 8,500 full) + the occupancy model need more,
    about 10–20 GB extra;
  - ρ = 2 events write 4.0 MB with dumps, not 0.52 MB.
- **C6.** ρ = 2 memory: the "up to 5 GiB" case is computed with 3.9 GiB (l.458). At 5 GiB, 1.5 × 5 = 7.5 GiB, so
  nothing is left for other jobs.
- **C7.** Geant4 yield: 10⁸ guns × 5.3 % = 5.3×10⁶ vertices (FEAS_B l.193), fewer than the 4×10⁷ P_geo events. State
  the biasing gain assumed. The cost is small either way.
- **C8.** There is no pruning policy for nuisances (conventions pitfall, `search.md` l.153-156).
- **C9.** The T1 auxiliary chain treats each conditional M_{t,j} as fixed, although it is the previous count. State the
  approximation, or use a binomial chain.
- **C10.** The plan's central target σ_ln ≲ 1 (PLAN l.130) is used to justify F but is never stated as a reported
  outcome with a pre-declared reading.

---

## 2. Conventions coverage (`conventions/search.md`, row by row)

| conventions row | STR answer | my verdict |
|---|---|---|
| CLs, q̃_μ, toys at low counts | WI (T1, §5.2) | covered; but see A1 (expected limits at γ̂ = 0) |
| Signal injection 0/1/2/5× | WI (T1-c) | **criterion trivial: A5** |
| Signal cross-section theory | WI, band | covered; parity issue B12 |
| Signal acceptance (generator, ISR) | WI (MLM/FxFx, qCut, tune) | covered |
| Signal shape | WI translated (SR-T/SR-G migration, timing) | acceptable |
| ISR modelling | WI (= f₂₀₀ nuisance) | acceptable |
| 4-fermion (generator comparison) | WI translated (MG vs Pythia for Z(νν)+j, W+j) | partial: no generator comparison for tt̄/diboson (C-level) |
| Background normalisation | WI | covered; propagation gaps B3 |
| Background shape | N/A, replaced by closure and trend | acceptable in principle; replacement weak (A3, A4) |
| qq̄(γ) modelling | WI (tune; Herwig conditional) | **B13** |
| MC statistics | WI (auxiliary channels) | **A1** |
| Detector simulation model | translated WI (B1, B6) | propagation incomplete (B3) |
| Object calibration | WI (MET, trigger, ε_PV, timing) | MET validation tautological (A7) |
| Beam energy | N/A (fixed 14 TeV) | justified |
| Luminosity | WI (R-9) | covered |
| PDF (pp) | WI | covered |
| Pile-up (pp) | WI at fixed μ = 200 | covered (brief D8) |
| QCD scale | WI | covered |
| Fragmentation | WI in part | **B13** |
| Heavy flavour | N/A (no b-tag); displaced-vertex check | justified |
| Check 1 closure p > 0.05 | WI translated | **A3, A4, B6** |
| Check 2 injection | WI | **A5** |
| Check 3 pulls/constraints | WI on Asimov | **B16** |
| Check 4 impact ranking | WI (T1-e) | covered |
| Check 5 GoF | N/A to data; closure p-values instead | acceptable |
| Check 6 LEE | N/A (fixed grid; Bonferroni in C1) | justified |
| Pitfalls: VR blind spot / transfer-factor instability / pruning / asymptotics | L6 + B2-b / B1-b / — / toys | blind spot unresolved for B1 (A3); pruning missing (C8) |

---

## 3. Numbers recomputed and spot-checked

**Budget script.** `python3 -I strategy_budget.py` reproduces every figure:
- MUST 2,950; SHOULD 848 / 326; totals 3,798 / 3,275 / 3,930;
- phases 646 / 160 / 1,953 / 181 / 10;
- storage 359 / 559 GB;
- capacity 1,851 slot-h per week = 264.4 per day, giving 132 / 159 / 198;
- R07 counts 12 / 35 / 70; V4-5 power 1.4 % / 11 % / 92 %; B*-off N = 969; S1 binomial errors 18 / 15 / 6 %.

Measured unit costs are used throughout. There is no global M3 → cluster factor. The exceptions are P1 (M3 × 3.4, B2)
and the Stage-3 interpolation for the five unmeasured Λ values (×2.14 from v1 M3 times, measured at three anchors; 9 %
of the sum; acceptable).

Spot checks (STR value → source → verdict):

| # | STR number (line) | source checked | result |
|---|---|---|---|
| 1 | min B₈₄ 1.2346×10⁶, 7.05 decades (l.30) | SUM `ladder.SR-G.min_B84` = 1234586.04, `decades_over_0p11_at_min` = 7.0501 | match |
| 2 | 219.2 fb, 0.04764, 0.5035, 15,774, 710, 789.7 (l.94) | SUM `fallback_points.A2\|F\|200\|1.5\|BM`: sigma_norm 219.2028, f_tail 0.047639, A 0.50355, N_exp 15775.0, S 709.88, ratio 789.74 | match |
| 3 | μ₉₅ = 1.2458×10⁷ (l.649) | same key `mu95_toys_events` = 12458208 | match, **but in events, while §1 defines μ = σ/σ_norm**: unit mismatch in T1-b (B-level, part of A5) |
| 4 | proxy share 0.147 at R04, 0.445 at R09 (l.503-504) | SUM `sm_proxy_fraction_of_B_SM`: 0.14716, 0.44523 | match |
| 5 | chain 13.5 ± 1.1 s, 12.9 alone, 0.46 GiB, 0.52 MB (l.192) | FEAS_A l.181, l.189-190 (13.53 ± 1.09; 12.94; 444–459 MiB; 0.52) | match |
| 6 | trial 11.7 ± 1.1 s, find 10.8, 9.4 alone (l.193) | FEAS_A l.201-203 (11.71 ± 1.10; 10.79; 9.44) | match |
| 7 | B1-type event 60.4 s (l.194) | FEAS_A l.25; JSON `job_sizing.rows[1].per_unit_wall_s` = 60.38 | match |
| 8 | ρ = 2 206 s, 1.46 GiB (l.195) | FEAS_A l.138, l.247 | match (N = 1, as STR says) |
| 9 | no-PU 11.5 ms, 12.6 kB/event, 8.2 kB (l.197) | JSON `cp_pvpair_n20000` conc 4: 0.011496 s; FEAS_A l.234, l.237 | match |
| 10 | Stage 3 0.65 / 18.8 / 67.8 s (l.198) | JSON `stage3_kernel` m500 conc 4: 0.6509 / 18.83 / 67.81 | match |
| 11 | v1 per-event Stage-3 CPU 0.037…2.53 s (l.208) | `STAGE3_INDEX.json` p2/F_m500: 0.037, 0.080, 0.212, 1.070, 2.528 | match (mass dependence small: E200 is 1.15× F500 at 5 keV) |
| 12 | M3 ratios 0.67–3.35 (l.35) | FEAS_A l.29-31, l.152-154 | match |
| 13 | K = 1.165 ± 0.002, +1.6/−1.1 % (l.736) | FEAS_B l.19-20 | match |
| 14 | Z(νν)+j 12.21 ± 0.03 pb vs 14.6 pb, 0.84 (l.510) | FEAS_B l.83 (FEAS_B calls it "ESTIMATE, not a validation") | match |
| 15 | shower 21 ms; QED-FSR 21.1 vs 21.2 (l.201, l.765) | FEAS_B l.116-118 (21.18 / 21.13) | match |
| 16 | Geant4 0.134 ms per gun (l.203) | FEAS_B l.192 | match |
| 17 | pyhf 0.12 / 0.52 / 10.4 / 652 s; Argo 16.8 s, SSH 2.4 s (l.204-205) | FEAS_C l.28, l.16, l.215 (652 s = 1000 s+b + 1000 b toys) | match |
| 18 | T_seed 4, road 0.15 (l.227) | `frozen_inputs.json` l.17, l.37-38 | match |
| 19 | V4-4 / V4-5 definitions; T_seed rule (l.310-311) | `S4/plan.md` l.1811-1812, l.503-506 | match |
| 20 | 8×10⁴ candidates × 5 MB, 0.4 TB; 8×10³ at N_IP2 ≥ 6 (l.465-466) | `G2A_REPORT.md` l.113-116 | match |
| 21 | union closure 0.654 (l.417) | `G3_REPORT.md` l.82 | match (but T_seed = 6 pilot, C2) |
| 22 | v1 freeze timing: 1.1×10³ → 790, FB0/FB1 ×4–8 / ×50 (l.1001-1005) | `STAGE4_RESULTS.md` l.115-117 | match |
| 23 | grid 5 species-masses × 8 Λ (l.60) | `run_g1b.py` l.12, l.48 | match |
| 24 | B model formula (l.101) | `WP_RULE.md` l.313 | match |
| 25 | R4 Table 7 systematics (l.881) | `experimental_status_2026.md` l.132 | match (R4's background terms up to 100–104 % are omitted in STR) |
| 26 | FB2 9/200 at E200 1.5 keV (l.257) | SUM `k_rfb` 9, `n_den` 200, `r_fb` FB2&h>5&o>5 | match; **proves A2** |
| 27 | "software 0.58 GB" (l.1136) | FEAS_B l.55 (`du -sh sw` only) | scope mismatch (C4) |
| 28 | halo rate source line (l.600-601) | experimental_status l.321 (not l.147/l.322) | mismatch (C2) |

No uncited constant from memory was found. Every number I sampled has a source, and the mismatches are the ones listed.

**Internal consistency.** The figures agree across §0, §4, §11.2, §11.5 and COM: 2,950, 848/326, 3,275 (§0 rounds it to
3,280), 3,930, 357 and 165 CPU-h saved, 2.6 days, 192/81/481/594/407/827 per item. Two inconsistencies:
- the criterion labels (B15);
- the μ₉₅ unit (row 3).

---

## 4. Answers to the §6.3 reviewer questions

1. **Conventions coverage.** Every row is answered (table §2). Several "WI" answers rest on criteria that cannot fail or
   cannot be evaluated: A3, A4, A5, B6, B13, B16. Not acceptable as is.
2. **Reference analyses.** R1–R4 are tabulated with numbers and line references (§6.1–6.2). Their programmes are thin,
   R1/R2 quote no systematics, and v2's coverage exceeds them. Parity holds except for σ_norm resummation (B12).
3. **What a competing group would have.**
   - (a) A full Geant4 simulation of a module-level Phase-2 geometry with cluster digitisation ([L8]: v2 keeps cylinders
     and Gaussian smearing, B6 only brackets it).
   - (b) An MVA selection (B1 above: the infeasibility argument is partly wrong).
   - (c) The endcap (excluded by brief D1; justified).
   - (d) A resummed signal normalisation (B12).
   - (e) Expected limits that do not treat untested zero counts as zero (A1).
   - Items (b), (d) and (e) are unjustified at present.
4. **Honest uncertainties in both directions.**
   - Underestimation: A1 (zero-count terms vanish in the expected limit), A4 (untested credits).
   - Inflation risk is low: s_model is capped and enters the likelihood.
   - The injection and pull checks (A5, B16) would pass whatever the model does.
   - Resolving power: C1 states its power (2 % at R04, 6 % at R06, gross check for signal). V4-5 rejects agreement below
     85–90 % only, which is stated.
5. **Limitations accepted without an attempt.** [DP5] Herwig (B13); the [DP1]/[DP2] compute-envelope proposals are
   allowed by brief D4 and quantified (DP2 only in part, B14).
6. **Context.** Comparison targets are extracted (§6.2: FASER 113–179 GeV, R1 650 GeV, R2 450 GeV) and planned as
   overlays (REF-1). Adequate.

**Other checks requested.**
- **S3** is handled exactly as fixed (l.801-803 quotes brief D1 verbatim). Flagging the underived ×1.5 for the human
  without changing it is correct.
- **MUST protection.** The MUST levers in §11.6 are listed and not proposed (good).
- **v1 freeze timing** is stated factually, with sources (row 22).
- **Pre-registration integrity** is weakened by A1, A2, A7 and B7.

---

## 5. Verdict

**ITERATE.** Gate A should not be requested until A1–A8 are resolved and the B items are fixed or explicitly accepted
by the user. The most serious are:
- A1, the statistics design, which would reward the absence of simulated statistics;
- A2, the blinding disclosure, which is wrong by a factor of two;
- A3/A4, the closure tests, which do not test the extrapolation that defines the result.
