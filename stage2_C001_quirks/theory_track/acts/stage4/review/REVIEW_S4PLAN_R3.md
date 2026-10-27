# Critical review R3 (narrow verifier): Stage-4 plan after fix R2 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R3, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`01-core.md` and `03-review.md` §6.

Classification, as in R2:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether review R2's B-1…B-5 and the closure-residual item are genuinely resolved, and whether
the R2 edits introduced new inconsistencies.

**Orchestrator update received during the review** (taken into account):
1. D4-10 (a′), D4-13, D4-14 and D4-15 are **approved as recommended**. Plan text still marked PROPOSED is a documentation
   lag (C-1).
2. The scope choice waits for the measured G2a speed.
3. **New hard user constraint:** any production must take ≲ 24 h wall on the Mac (M3, 8 cores, ≈ 7 CPU-s per wall-s).
   That is a cap of ≈ 170-200 CPU-h in the plan's units.
4. The user's acknowledgement of the fallback deliverable is still pending.

**Inputs read:**
- `plan.md` (1384 lines; §0, §2, §4.1, §5, §6, §10-§12 in full);
- `FIX_S4PLAN_R2.md`, `REVIEW_S4PLAN_R2.md`;
- `probes/f2r_profile.py`, `f2r_cost.py`;
- `data/acts_stage4/fix_r2/*.json` and logs.

**Independent checks** (≈ 0.01 CPU-h; scratch in `data/acts_stage4/review_r3/`; no acts env use, no finder run, no ρ = 2,
no signal):
- `r3_checks.py` → `r3_checks.json`:
  - the cost formula re-derived from the §6.2 block table;
  - the 24-h cap scopes;
  - a log-normal quantile check of the budget split;
  - PU candidate counts per trial;
- `r3_chi2core_p.py` → `r3_chi2core_p.json`: PU-only pass fractions of the p(χ²_core) rungs, using the stored fix-R2
  per-candidate `chi2_core1` and `n_core1`.

---

## 1. Status of the R2 items

| R2 item | Verdict | Evidence / residual |
|---|---|---|
| **B-1** width rung + core χ² | **Resolved (design).** | See the notes below this table. Residual: C-3 and C-8. |
| **B-2** SR-T/SR-G | **Partly resolved.** | Scheme (c) is written consistently in §2.3 and §2.5 item 5. However, the joint-tightening step is the *normal* path, not an exception, and several of its branches are undefined (new **B-3**). |
| **B-3** per-family extrapolation | **Partly resolved.** | Each family's method can be computed from the stored fields (see the notes below). However, every counting rung of the ladder contains p(χ²_core) > 10⁻³, while the table handles counting rungs with counts-only thinning (new **B-4**). Storage and in-job cost: C-2. |
| **B-4** feasibility and fallback | **Feasibility statement resolved; fallback partly resolved.** | §2.6 is honest: it is tagged ESTIMATE, it states that helix and opening give ~nothing against combinatorial PU, and it states the implausible regions. The fallback is well defined, but its primary limit sits at a rung with near-zero efficiency exactly where the fallback is needed (new **B-2**). |
| **B-5** cost vs speed | **Arithmetic resolved; now superseded by the user's 24-h cap (new B-1).** | The formula and the profile reproduce (§3). §10 contradicts §6.2/§11 on when the user is asked (folded into B-1). |
| Closure residual ×1.6-1.8 | **Resolved.** | Branches are pre-registered and deterministic. A small interplay gap is noted in C-7. |

**Notes on R2 B-1.**
- **Definition.** w_core is the f1r `dw_core`: one step, IT + PS hits only. The rung thresholds are W_c/2^k = 37.5, 18.75,
  9.4 and 4.7 mm. The core-χ² definition (§2.2 item 5) matches the PU-only probe code (`f2r_profile.py::core_stats`, the
  one-step block).
- **Placement and freeze.** The family sits after N_IP2 and before the χ²_core, 2S and F1 rungs. It is listed in the G2
  freeze (§2.5 item 9).
- **Signal use is acceptable as disclosed.** The halvings of W_c are an a-priori geometric choice. Their closeness to R2's
  20/10 mm cuts is not evidence of tuning, because rungs are not working points: the B-only rule still chooses r*. The probe
  rows are excluded.
- **PU-only numbers match the JSON.**
  - `t1`, N_L2 ≥ 9: per-trial minimum 12.2/13.5/14.2 mm; 0 of 18 903 candidates < 9.4 mm.
  - `t2`, N_L2 ≥ 9: 14.6-32.2 mm.
  - N_L2 ≥ 8, `t1`: 6.3-9.2 mm, with 3 candidates < 9.4 mm and 0 < 4.7 mm.
  - n_core/n_in-band = 53/60; χ²/ndf median 2.871 vs 2.891.

**Notes on R2 B-3 (what is computable from the stored fields).**
- Counting rungs: per-hit (interaction id, layer, side).
- w_core and χ²_core: per-hit u, σ_tot and interaction id. A per-interaction pre-summed M_i is not enough when the core is
  re-centred per subset (C-2), but the per-hit storage covers it.
- dE/dx: per-hit dE.
- h and o: factorisation at ρ = 1, checked on 200 sets.
- SR-T: BTL interaction id and time.

---

## 2. Category A

None. No number in the plan is wrong in a way that invalidates a result already obtained. No closure is mis-reported: the
pilot failure is stated as a failure, and the residual is stated as unexplained.

---

## 3. Re-derivation of the cost formula and the profile (B-5 check)

**Block table at t₁ = 2 s, t₂ = 16 s** (`r3_checks.json`):

| Block | CPU-h |
|---|---|
| A1 | 2 |
| A2 | 40.2 |
| A3 | 7.1 |
| A4 | 9.6 |
| A5 | 30 |
| B1 | 70.6 |
| B2 | 57.5 |
| C + C′ | 67 |
| validation | 40 |
| **Sum** | **324** |

**Formula.**
- ρ = 1 trials: 61 344 + 9 000 + 12 000 + 4 000 + 80 000 + 25 000 = 191 344, i.e. **53.2 CPU-h per s**.
- ρ = 2 trials: 10⁴, i.e. **2.78 CPU-h per s**.
- Base: 330 − 106.3 − 44.4 = **179.3**. From the block sum it is 173.3; `f2r_cost.py` uses the rounded 330. The 6 CPU-h
  difference is immaterial.
- All §0 and §6.2 rows reproduce to ±1 CPU-h: 330, 424, 481, 556/1001, 933/2100, 1687, 5508 and 16 083. So do the lean rows
  (84 + 27 t₁ + 1.4 t₂) and the G3 pilot (12.8 / 18.4 / 388 CPU-h).
- G2b: t₂ ≤ 20.5 s ⇔ B2 ≤ 70 CPU-h. ✓

**Profile** (`f2r_profile_summary.json`, logs):
- TDR-OT, as coded: median 29.3 s, of which the merge is 21.2 s (72 %). ✓
- Full IT + OT density:
  - as coded: 3 407 / 5 472 / 6 099 s per trial (median ≈ 5 500, 96.8 % merge) ✓;
  - merge vectorised: 159 / 211 / 228 s (component sums), median 211 ✓;
  - stage medians: seeding 95.4, numba refit 30.3, numpy refit 52.0, merge 33.1 s ✓;
  - refits 2.0 × 10⁵, kept 1.1 × 10⁵, road hits 3.9 × 10⁴ ✓.
- The "as coded" figure is an extrapolation: comparisons N_fast·N_kept/2 = 1.05 × 10¹⁰ × 0.51 µs (the trial records store
  `n_cmp`). This is clearly labelled in §2.4.
- The fix-R1 "48 s" is a different 32-trial set run with 7 parallel workers. The plan states this discrepancy honestly.
- ρ = 2 Fatras shares: merge 46 %, thinning MC 27 % ✓.

**Internal coherence of the gates.** The gates are coherent internally, with one exception. §10 D4-1 says "the user is asked
if t₁ > 4 s **or t₂ > 20 s**". §6.2 and §11 G2b ask only at t₂ > 60 s; between 20 and 60 s they cut B2 and only report.
This is folded into B-1, because the gates must be rewritten for the cap anyway.

---

## 4. Category B

### B-1. No pre-defined production scope fits the user's new ≲ 24 h wall cap (≈ 170-200 CPU-h). The G2a/G2b gates and §10 are written against 330/480 CPU-h.

**Evidence** (`r3_checks.json`; cap taken as 24 h × 7 ≈ 168 CPU-h, upper end 200):

1. **The recommended scope never fits.** Its non-finder base alone is 179 CPU-h, so even at t₁ = 0 it exceeds 168 CPU-h. At
   the costed t₁ = 2 s it is 330 CPU-h (≈ 47 h wall).
2. **The lean scope fits only at t₁ ≲ 2.2 s** (with t₂ = 8 t₁): 160 CPU-h at t₁ = 2. The plan's own ESTIMATE after
   optimisation is 5-20 s, where lean is 270-850 CPU-h. The plan already says that 2 s "is not supported".
3. **G2a's middle branch breaks the cap.** "2 < t₁ ≤ 4 s → proceed" would launch ≈ 480 CPU-h (≈ 69 h wall) without asking.
4. **Other parts of the plan exceed or ignore the cap:**
   - the conditional ρ = 3 (+38 CPU-h at t₃ = 54 s, more at a realistic t₃ ≈ 3.4 t₂) has no place under the cap;
   - §11 states "production ≈ 3 days wall";
   - §6.4 states "≈ 70 h → ≈ 30 h".
5. **The gates conflict with user decision 2.** The user will pick the scope after G2a, but G2a's ≤ 2 s branch selects the
   "costed scope" automatically. In addition, §10 and §6.2/§11 disagree on when the user is asked about t₂ (§3).

**What a capped scope can look like** (reviewer ESTIMATE, same per-event inputs as §6.2; `r3_checks.json` →
`minimal_scope`). "S-cap":
- A1 in full;
- A2 on the 5 mv species-masses (E 200/500/1000/1500, Ẽ500) × 8 Λ × 200 events, row-major (1 000 rows);
- B1: 5 000 events × 4 roads;
- B2: 1 000 ρ = 2 events × 2 roads; no ρ = 3;
- A5: 5 points (≈ 1 000 events, full chain incl. V4-6);
- C: 3 samples (Z(νν)+j, W(τν)+j, tt̄ 1ℓ) × 2 000 events, plus the k = 1 guns (≈ 12 CPU-h);
- validation: 15 CPU-h;
- A3 and A4 deferred. A material check can be a 1-mass, 2-scale TT-level subset if the cap allows.

| t₁ / t₂ (s) | A2 | B1 | B2 | C + guns | A1 + A5 + validation | **total (CPU-h)** | wall (7 workers) |
|---|---|---|---|---|---|---|---|
| 2 / 16 | 6 | 18 | 12 | 23 | 26 | **84** | 12 h |
| 5 / 40 | 13 | 34 | 25 | 28 | 26 | **126** | 18 h |
| 8 / 64 | 19 | 51 | 38 | 33 | 27 | **169** | 24 h |
| 10 / 80 | 24 | 62 | 47 | 37 | 28 | **197** | 28 h |
| 20 / 160 | 46 | 118 | 92 | 53 | 31 | **339** | 48 h |

So **some meaningful production fits the cap only if G2a reaches t₁ ≲ 8 s, with t₂ ≲ 64 s** (≈ 10 s at the 200 CPU-h end).
Above that, only a further-reduced grid fits.

**What S-cap gives up, which the user must see:**
- **PU-extrapolation reach.** At ρ = 2, 2 × 10³ trials probe ⟨Σw⟩ ≈ 5 × 10⁻¹⁰ per trial. That is at the per-category
  requirement (§2.6: P_PU ≲ 5 × 10⁻¹⁰), with no margin, against ≈ 10⁻¹⁰ in the recommended B2.
- **The edges in ln m.** They come from 5 masses instead of 14.
- **The A3 toy coverage.** It is deferred.
- **The SM samples.** These are at 1.5 × 10⁻³ direct reach.

**Required fix:**
1. Add a **pre-defined capped scope** (S-cap, or the fixer's own version) with its block list, grid subset and event
   counts. Make it the default whenever the costed scopes exceed the cap.
2. **Recast G2a and G2b against the cap**, with thresholds computed from the S-cap formula. For example: G2a t₁ ≤ 8 s and
   G2b t₂ ≤ 64 s, so that S-cap fits; anything slower → ask the user (a further-reduced grid, several 1-day campaigns if
   the user allows, or stop). Per user decision 2, every G2a outcome is **reported to the user, who chooses the scope**.
3. Remove ρ = 3 from the capped scope. Make "WP rung not reachable at ρ = 2" go directly to the rung-factorisation step
   of §4.1 step 2.
4. State whether G1-G3 and C′ development runs (≈ 6 + 13-18 + 15 CPU-h) count against the cap. This is a user question.
5. Make §0, §6.2, §6.4, §10 D4-1/D4-5, §11 (gates, timeline) and §12 risk 1 consistent. The t₂ escalation threshold must be
   one number everywhere.

### B-2. The fallback limit is fixed at R_E, which has near-zero signal efficiency, by construction, in the regions where §2.6 says the fallback applies. The supplementary limits at R_A-R_D have no usage rule.

**Evidence** (plan text and physics only; no new signal look):
- §2.6 places the fallback regions at Λ ≲ 1 keV and at E200 (any Λ).
- §2.5 item 3: the ladder is cumulative, so R_E (the full F1) contains w_core < 4.7 mm. §2.5 says rung k accepts
  ℓ_max ≲ R_IT·2^−k, i.e. ≲ 9 mm at k = 4.
  - A uniform fill of ±ℓ_max/2 gives 1.4826 × MAD = 0.37 ℓ_max. So w_core < 4.7 mm means ℓ_max ≲ 13 mm.
  - At 1 keV, ℓ_max is a sizeable fraction of R_IT (E1000: f(ℓ_max ≤ R_IT) = 0.83, §2.2).
- R_E also contains e_min = 2.0 MIP. §2.6 itself gives the E200 IT βγ as 1.8, i.e. dE/dx near the MIP value.
- Consequence: the "Stage-5 limit with non-zero, uncertain background at the fixed rung R_E" is essentially empty exactly
  at low Λ and at E200.
- §2.6's "Low-Λ events are covered by R_A and R_B" is true only for the ε reporting. At R_A, the per-trial PU rate is
  ~10⁻¹ (measured), i.e. B ~ 10⁶ events, so no useful limit exists there.
- "Expected limits at R_A-R_D are supplementary" has no rule. Stage 5 could quote the best of five limits per point, which
  is a per-point choice on signal and contradicts "the rung is fixed in advance".

The user is about to acknowledge this fallback (orchestrator item 4), so it must be described correctly before the
acknowledgement.

**Required fix:**
1. State plainly in §2.6 that the fallback in the low-Λ and E200 regions is expected to deliver ε and B tables and
   observables, and essentially no limit.
2. **Forbid the per-point best-of.** If supplementary limits are shown, show all five, with R_E as the only primary limit.
   Alternatively, pre-register a per-region fixed primary rung chosen without signal (e.g. R_B for Λ-agnostic reporting,
   with its B₈₄ attached).
3. If a signal-informed rung choice is wanted, it must be a split-template rule pre-registered now (choose on half A,
   report on half B). This is a user decision, not a fixer choice.

### B-3. The budget split's joint-tightening step is the normal outcome, not an exception, and its edge branches are undefined.

**Evidence** (`r3_checks.json` → `b84_sum_two_cats_each_0p15`; 2 × 10⁶ draws, σ_ln = 2.3, both categories at B₈₄,c = 0.15):

| correlation of the two categories' log-normals | B₈₄ of the sum |
|---|---|
| independent | **0.41** |
| ρ = 0.5 | **0.38** |
| fully correlated | 0.30 |

Quantiles of heavily skewed log-normals are super-additive. Unless the shared sources dominate σ_ln completely, any pair of
categories near 0.15 fails the combined ≤ 0.3 check. Joint tightening is then routine: the effective per-category budget is
≈ 0.11, not 0.15. §2.5 item 5 calls it "possible".

Branches that a rule frozen at G2 must define:
1. one category is already at its tightest rung R when joint tightening is needed;
2. one category has no working point (item 6 → fallback) while the other has one. Is the combined check skipped, and does
   the Stage-5 two-bin likelihood mix r*_T with R_E,G?
3. the loop never reaches ≤ 0.3;
4. whether the "this rung and every tighter rung" guard also applies to the combined check after joint tightening (B is not
   monotone).

**Required fix:**
1. In §2.5 item 5, say that the combined check usually binds.
2. Define the four branches deterministically. For example:
   - a category at R stays there and the other keeps tightening;
   - a no-WP category contributes B(R_E) to the combined check and is reported under the fallback;
   - if the combined check still fails at (R, R), both categories go to the fallback;
   - the guard applies to the pair path.
3. Optionally, pre-declare the split as 0.11 + 0.11 to remove the step. That is still a convention with no signal input.

### B-4. Every counting rung contains p(χ²_core) > 10⁻³, but the §4.1 step-3b table extrapolates the counting rungs with counts-only thinning. The per-subset χ² method, and its cost, start only after N_IP2 ≥ 7.

**Evidence:**
- §2.5 item 3: the first rung is (N_IT2 ≥ 3, N_IP2 ≥ 4, **p(χ²_core) > 10⁻³**), and every later rung inherits it.
- §4.1 step 3b, counting row: "per-subset recomputation (thinning) from per-interaction (layer, side) counts". Its closure
  test T1 is defined at the tightest rung with ≥ 10 B1 counts. That rung necessarily includes the χ² requirement, which
  counts cannot evaluate.
- The w_core/χ²_core row draws subsets "conditional on the preceding count rung", i.e. after N_IP2 ≥ 7.
- **The χ² requirement is not a formality on PU** (`r3_chi2core_p.json`; PU only, one-step core, ndf = n_core − 2):

  | density | p(χ²_core) > 10⁻³ | > 0.01 | > 0.05 | per-trial counts passing 10⁻³ |
  |---|---|---|---|---|
  | full IT + OT (N_L2 ≥ 8) | **1.5 %** of PU candidates | 0.37 % | 0.07 % | 348 and 286 per trial |
  | TDR-OT (N_L2 ≥ 8) | 2.2 % | 0.76 % | 0.13 % | 7-18 per trial |

  So the χ² factor at rung 1 is a ×50-70 per-candidate rejection. It is the strongest per-candidate F0 cut, and it sits
  inside the rungs whose extrapolation ignores it. Per trial it still leaves hundreds of candidates at ρ = 1, so the trial
  level picture of §2.4 stands.
- **Cost consequence.** Treated correctly, the χ² factor needs the per-subset method (2-10 ms per set, ESTIMATE) on every
  set from rung 1 on. At ρ = 1 and full density there are already ≈ 2.5 × 10⁴ distinct candidates per trial at N_L2 ≥ 8
  (`r3_checks.json`); ρ = 2 has more. The in-job cost of §4.1 and the G2b timing then shift by orders of magnitude, and
  the f_s sub-sampling explicitly exempts N_IP2 ≥ 6 sets (C-2).

**Required fix.** Pre-register one of:
- (a) move p(χ²_core) > 10⁻³ out of the counting rungs, to the head of the χ²_core family (an ordering decision on PU-only
  grounds; the order is fixed before the freeze);
- (b) keep it, and treat the χ² factor of the counting rungs by factorisation at ρ = 1, P(χ² | count rung) measured on B1,
  with its own density-bin independence test and closure. Note that R2 B-3 argued that χ² is density-driven, so a test is
  mandatory;
- (c) apply the per-subset χ² method from rung 1, and cost it in the G2b in-job budget.

In all cases, T1 must be defined on a quantity that its method can compute. Also say that the χ²_core per-subset
recomputation re-centres the core per subset, so it needs per-hit (not per-interaction pre-summed) moments, which the
storage row already provides.

---

## 5. Category C

- **C-1. PROPOSED markers are now stale.** The user approved D4-10 (a′), D4-13, D4-14 (a) and D4-15. Update:
  - plan l.18-20, l.184, l.358, l.702 ("If D4-13 is not confirmed"), l.1181, l.1195, l.1256-1258, l.1284;
  - §11 item 4 (the D4-13 deliverables are now in scope; the fallback limit gains the pyhf workspace).

  The fallback acknowledgement and the scope (after G2a) remain pending, and should stay marked as such.
- **C-2. Storage and in-job weight load (§4.1 step 3b).**
  - "(b) a 1 % random sample of sets passing the loosest rung: ≈ 4 GB" accounts only for item (a). Item (a) is 200 sets ×
    ≈ 2 kB × 10⁴ trials ≈ 4 GB.
  - Item (b): at ≥ 10⁵ loose sets per ρ = 2 trial (ρ = 1 already has 1.1 × 10⁵), 1 % is ≥ 2 MB per trial, i.e. ≥ 20 GB.
  - Neither item is in the §6.3 total of 8 GB.
  - The f_s remedy sub-samples only below N_IP2 ≥ 6, but the weight cost is dominated by the sets at or above it. Allow a
    pre-declared stratified f_s there too, or say that G2b failure is the only outcome.
- **C-3. The §2.6 w_core cell "strong (M)"** compares PU at the full density with signal medians at Fatras density.
  - The signal w_core at the adopted density is unmeasured by design.
  - The MAD estimator breaks down at 50 % contamination. At the full IT density the in-band IT + PS PU crossings (§2.1:
    ≈ 15-17 per band) approach a heavy pair's ≈ 20 signal hits, so the signal width can inflate.
  - Tag the cell M for PU and E for signal at ρ = 1, and list the risk in §12.
- **C-4. Number nits.**
  - "≈ 560-1 700 CPU-h … plus B2 at its own t₂" (§0, §6.2, §10): the 560-1 700 already includes B2 at t₂ = 8 t₁.
  - "167-228 s" mixes one wall time with component sums; the component sums are 159-228 s.
  - §4.1 quotes "1.2 × 10⁵ distinct candidates", §2.4 quotes "1.1 × 10⁵": these are q90 vs median.
  - `n_distinct_hitsets` in the profile is a copy of `n_kept` (2-mrad distinct, not ≥ 50 % hit-set distinct). Say so
    wherever "distinct" is used.
  - The `f2r_profile.py` docstring still calls the trimmed width "the plan's new w_core".
- **C-5. Stale text beyond B-1.** `FIX_S4PLAN_R2.md` says D4-1 is "re-asked at G2a", but the plan's G2a asks only at
  t₁ > 4 s. This is now superseded by user decision 2; fix it in the B-1 rewrite.
- **C-6. Naming drift.** The T_seed stability rule (§2.2 item 4) and G3 (iv) refer to "N_L2", and all width evidence is at
  N_L2 rungs. The ladder now counts N_IP2 and N_2S2. State the mapping, or use the ladder variables in the T_seed rule.
- **C-7. Failure-path interplay.**
  - The G3 box lists three branches but not "|z| < 2 with a significant *conservative* trend". Step 4 covers that case
    (slope added to σ_ln); cross-reference it.
  - State what happens when tests of different families point in opposite directions, e.g. T1 conservative and T1w
    anti-conservative. Presumably each family's test governs its own rungs, and corrections compound along the cumulative
    ladder.
  - Otherwise the branches are deterministic and not cherry-pickable. r₁ is fixed by the ≥ 10-count and lever-arm rules,
    per-hit-set counting is fixed for all ρ, and a later cause cannot change the branch without a logged re-review.
- **C-8. The ordering justification for the χ²_core rungs** ("the core χ² barely shifts the PU distribution") compares
  core-hit with all-hit χ². It is not a statement about cut power: per candidate the p rungs reject strongly (B-4). The
  defensible PU-only statement is per trial: every full-density trial still has candidates passing p > 0.05 (14-15 per
  trial). Rephrase.
- **C-9. ρ = 3 has no timing gate.** With t₃ ≈ 3.4 t₂, ρ = 3 costs 2 000 × (14.1 + t₃) s, i.e. ≈ 47-120 CPU-h at t₂ =
  20-60 s. It is removed under B-1; if it is kept anywhere, gate it like G2b.

---

## 6. Global consistency (other checks)

- The §0 summary table, the §2.4 tables and §2.2 item 5 match `f2r_profile_summary.json` (§1, §3).
- Gate order:
  - the freeze is before V4-3/A1 ✓;
  - G2a and G2b are before any G3 ρ = 2 event ✓;
  - G3 (i)-(v) is consistent with §4.1 ✓.
- The rung count (4 + 4 + 2 + 3 + 9 = 22) matches "22 × 22 rung pairs" ✓.
- §2.6 arithmetic:
  - B₈₄,c ≤ 0.15 ⇒ median ≲ 0.015 ✓;
  - with N_trig ≈ 3.3 × 10⁷, P_PU ≲ 4.5 × 10⁻¹⁰ ≈ "5 × 10⁻¹⁰" ✓.
- NI arithmetic (R2 C-4): 26 × 0.22 × (0.3-0.5) × (10⁻³-10⁻²) = 1.7 × 10⁻³-2.9 × 10⁻² ✓.

---

## Verdict

**ITERATE.** 0 Category A, 4 Category B, 9 Category C.

| # | Item | Fix |
|---|---|---|
| B-1 | No pre-defined scope fits the user's ≲ 24 h wall cap (≈ 170-200 CPU-h). The recommended base alone is 179 CPU-h. Lean fits only at t₁ ≲ 2.2 s. G2a "2-4 s → proceed" would launch ≈ 480 CPU-h. ρ = 3, the timeline and the §10 escalation text are inconsistent | Add a capped scope. The reviewer's S-cap fits up to t₁ ≈ 8 s / t₂ ≈ 64 s: A1, A2 on 5 masses × 8 Λ, B1 5 000, B2 1 000 at ρ = 2, A5 5 points, C 3 × 2 000 + guns, no A3/A4/ρ = 3. Recast G2a/G2b on the cap, with the user choosing the scope after G2a. Align §0/§6/§10/§11/§12 |
| B-2 | The fallback's primary limit at R_E (w_core < 4.7 mm, e_min 2 MIP) has ~0 efficiency at Λ ≲ 1 keV and E200, where the fallback applies. The R_A-R_D supplementary limits have no rule (best-of risk) | State it plainly before the user's acknowledgement. Forbid a per-point best-of. Optionally pre-register a signal-free per-region primary rung or a split-template rule (user decision) |
| B-3 | The combined B₈₄ of two categories at 0.15 each is 0.41 (independent) / 0.38 (ρ = 0.5), so joint tightening is routine. Its branches (category at R, no-WP category, non-termination, guard) are undefined | Say that it binds; define the four branches; optionally pre-declare 0.11 + 0.11 |
| B-4 | Every counting rung contains p(χ²_core) > 10⁻³ (it keeps 1.5-2.2 % of PU candidates), but the counting-rung extrapolation and T1 use counts only. The per-subset χ² cost is budgeted only after N_IP2 ≥ 7 | Move the χ² cut to its family, factorise it with an independence test, or recompute it per subset from rung 1 and cost it in G2b |

The closure-residual branches and the cost arithmetic are sound. R2 B-1 is resolved in design. The remaining work is text
and design only; no production, ρ = 2 or signal run is needed. B-1 depends on the user's answer to whether G1-G3 count
against the cap, and on whether several one-day campaigns are allowed.
