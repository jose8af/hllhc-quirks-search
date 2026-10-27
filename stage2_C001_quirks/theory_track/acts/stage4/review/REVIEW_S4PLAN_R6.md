# Critical review R6 (narrow verifier): Stage-4 plan after fix R5 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R6, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`03-review.md` §6.

Classification, as in R2-R5:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether R5's B-1 and C-1…C-3 are resolved, and whether fix R5 introduced a new A or B.

Inputs:
- `plan.md`: header R5 note, §0, §2.5 items 4/4a/9, §2.6 (dE/dx paragraph and feasibility), §4.1 steps 3-4, §4.2 in
  full, §5 table, §11 (item 5, schedule, rules), §12 risks 3b, 11 and 12;
- `REVIEW_S4PLAN_R5.md`, `FIX_S4PLAN_R5.md`;
- `fix_r5/f5r_cprime_counts.{py,json}`.

The finder speed-up files were not read.

**Independent checks.** `data/acts_stage4/review_r6/r6_checks.py` → `r6_checks.json`:
- sha256 `60d50226…1dec6`;
- system python3, standard library only, 0.03 CPU-s;
- no acts env, no simulation.

`f5r_cprime_counts.json` has sha256 `e39f25d3…2615fa1`, which matches the fix report ✓.

---

## 1. Status of the R5 items

| R5 item | Verdict | Evidence / residual |
|---|---|---|
| **B-1 (a)** thinning as a depth mechanism | **Resolved** | See *(a) detail* below the table. |
| **B-1 (b)** NI/DIF preselection and f_pre weight | **Design resolved; the exactness claim is not yet true as written** | See *(b) detail* below the table. Exactness → new **B-1**. The 22 mm f_pre and the stale NI statements → **C-1**. |
| **B-1 (c)** zero- and low-count rule | **Resolved; conservative** | See *(c) detail* below the table. One avoidable weakness → **C-2**. |
| C-1 attribution | Resolved | ≥ 3 core hits in ≥ 3 layers from ≥ 2 gun/toy particles, with the looper exception (§4.2 *Attribution*). It is applied identically to C′₀. Pure-PU candidates with one incidental gun hit now go to B_PU. The SM ≥ 1-hit tag is kept, conservatively, and the plan says so. |
| C-2 dE/dx wording | Resolved | §2.6 l.871-894: "Λ ≲ 0.7 keV", the Ẽ1000 +8 % exception, the PDG 2024 Si table cited with "K, Z/A and ρ cancel", "recalled, UNVERIFIED" dropped, and E500 "borderline" restricted to R4's convention. |
| C-3 schedule nits | Resolved | §11 l.1868 and l.1877-1896: "47 net (50 gross − 3 h)", the f4r docstring reconciled, the G3 overrun above 5.4 s treated as a slip, the slip-below-C1 rule (C1a → C1b → C1r → ask), and A1 listed once. §12 risk 12 is aligned (l.1972). |

**(a) detail.**
- The SM hard-scatter text (§4.2 l.1220-1231) and the C′_PU "Depth" bullet (l.1288-1298) both say:
  - k-thinning of a ρ = 1 sample gives no depth;
  - T1 is not applicable;
  - depth comes from rung factorisation, starting at the deepest rung with ≥ 10 counts, with conditionals on populations
    of ≥ 10 entries, the c test and T3 on that sample;
  - h, o and dE/dx come from C′₀.
- §4.1 step 3 (l.1062-1065) states the same rule "for every sample (B1, B2, C, C′)".
- A grep finds "thinn" outside §4.1 only:
  - in its legitimate B2/B_PU uses (§0 l.143/180, §2.5 l.688, §5 B2 row, §6.2, §12 risks 2/11);
  - in the "not from thinning" statements.

  No fixed-density sample is credited with thinning depth.

**(b) detail.**
1. *PU independence of the preselection.* The design is sound. The preselection uses toy hits only. PU hits cannot count
   toward the attribution triple. A PU-shifted candidate plane cannot create a triple that the toy alone lacks, because
   λ_min minimises over all PV planes.
2. *Combinatorics of "≥ 3 hits, ≥ 3 layers, ≥ 2 particles ⇒ a 3-distinct-layer triple with ≥ 2 particles".* This holds:
   - take a hit of particle B in layer L_B and a hit of particle A;
   - if A's hit is in another layer, add any hit from a third layer;
   - otherwise take A's hit plus any hits in two other layers.
3. *χ²₃ ≤ 48 from "each hit ≤ 4σ".* Three hits each within 4σ of a plane give a sum ≤ 3 × 16 = 48, and λ_min is ≤ the
   value for any one plane. This holds **only if the σ_h and the PV in the preselection are the same as, or looser than,
   those the with-PU candidate uses**. They are not pinned down, so this goes to new B-1.
4. *Sampling.* "First 500 by event index" and ⌈500/N_pre⌉ overlays with a two-level bootstrap are unbiased.
5. *Script spot-check.*
   - `rung_probs` implements R0 = (N_IT2 ≥ 3, N_IP2 ≥ 4) and the N_IP2 ladder over 2⁷ layer patterns correctly.
   - The kink model (one toy crossing per layer + P(≥ 1 random) = 1 − e^−μ_c) and the two-prong model (q + (1 − q)p) are
     reasonable ESTIMATEs.
   - The numbers reproduce:
     - 3 × 10⁴ × (4 × 10⁻⁴, 6.7 × 10⁻³) = 12 / 200;
     - ⌈500/12⌉ = 42;
     - 436 / 245 at R0 for kinks.
   - The 22 mm f_pre misses the dominant preselection path. The conclusion "O(10²) at the loose rungs, ≥ 10 to N_IP2 ≥ 6"
     still holds. See C-1.
6. *Kink path at r_NI ≥ 30 mm.* It is correctly measured: f_pre 0.3-0.9, overlaid, with depth from rung factorisation +
   C′₀. Its disclosure is incomplete; see C-1.

**(c) detail.**
- *Constants.* They are correct: −ln 0.32 = 1.139; 1.139 e = 3.097 ≈ −ln 0.05 = 2.996.
- *Not anti-conservative.* The rule's log-normal (median 1.14/M, σ_ln = 1) is stochastically larger than the flat-prior
  posterior for N = 0 (exponential with rate M) at every x. The maximum of F_LN − F_post over x·M ∈ [10⁻⁴, 10] is
  −10⁻⁴, i.e. ≤ 0 (`r6_checks.json` → `zero_rule_vs_posterior`). Its quantiles per M are:

  | quantile | rule (log-normal) | posterior |
  |---|---|---|
  | median | 1.14 | 0.69 |
  | 84th | 3.10 | 1.83 |
  | 95th | 5.90 | 3.00 |
  | mean | 1.88 | 1.00 |

- *"Later zeros enter as 1"* is conservative: every true factor is ≤ 1.
- *"Non-zero conditionals of other requirements still multiply"* rests on the same independence assumption as any
  conditional measured on a substituted population. It is covered by c and the extrapolation spread. The one gap is that c
  cannot involve the zero factor itself; see C-3.
- *Not paralysing by construction.* There is one bounded factor per term, and fallback (item 6) is the only remedy. It can
  be needlessly weak when two families are zero; see C-2.
- *Consistency.* The rule is referenced consistently:
  - §2.5 item 4 (l.714-715);
  - item 4a (l.716-738);
  - item 9 (freeze list, l.784: "the zero-count rule (item 4a), the C′ preselection and attribution rules (§4.2)");
  - §4.1 step 3 (l.1065);
  - §4.2 SM (l.1230), C′ (l.1271, 1298, 1313) and the B sum (l.1343);
  - §11 item 5 (l.1824);
  - §0 (l.74).

**Global spot check.**
- The §0 R5 bullets (l.70-75), §5 C′ row, §11 item 5 and §2.5 items 4/4a/9 agree with §4.2.
- The C′ cost, campaign contents and decision table are unchanged, as claimed.
- C′₀ preceding C′_PU inside C1 (and inside C1a) is a feasible ordering. The preselection needs only the toy hits
  (≈ 0.02 s/event), not the finder.

---

## 2. Category A

None.

---

## 3. Category B

### B-1. The f_pre factorisation is "exact by construction" only if the preselection uses σ_h and a PV that are at least as loose as the candidate's. The plan specifies neither, and the leak is anti-conservative.

**Evidence.**
1. **σ_tot depends on the candidate.** It is σ_tot² = σ_n²(n, hit) + t_tol² + (δn·|u|)² (§2.2 l.446). σ_n is the hit's
   local error projected on the candidate's normal n, and δn is the candidate fit's normal uncertainty. The preselection
   says only "σ_h is σ_tot" (§4.2 l.1258), with no n and no δn.
   - For PS macro-pixels (≈ 29 µm × 430 µm), σ_n(n) varies by up to ×15 with the orientation of n.
   - δn·|u| at PS radii (230-500 mm) is O(10-100) µm for δn ~ 10⁻⁴.
   - So a toy hit inside ±4σ_tot of the with-PU candidate can be well outside ±4σ_h of the preselection triple, if σ_h is
     evaluated at the triple's own n with δn = 0. The implication "attributed ⇒ preselected" then fails.
2. **The PV is not stated to be identical.** The preselection is "evaluated on the no-PU C′₀ event". The with-PU candidate
   is fitted through "the PV the with-PU event uses". The PV is the true vertex smeared by (10, 15) µm (§1.7). Unless both
   use the same smeared PV draw, every residual shifts by O(σ_PV), against a 4σ_tot ≈ 138 µm IT window.
3. **The mechanism is not stated.** "The toy's hits in the with-PU event are exactly its C′₀ hits" also requires that the
   toy's **simulated** hits (Fatras multiple scattering and energy loss) are reused at the hit level and not re-simulated
   in the PU job. Only the smearing and hit-efficiency seeding is stated.

**Why it matters.** The leak is anti-conservative: attributed passes from non-preselected toy events are never counted.
- It sits in a rule frozen in `WP_RULE.md` (§2.5 item 9).
- No closure test covers it: the non-preselected events are never overlaid.
- The size is probably small, because only marginal (≈ 4σ) configurations are affected. But it is unmeasured, and the
  plan calls the weight exact.

**Required fix** (text only; no cost change):
- (i) Define σ_h in the preselection as an **n-independent per-hit upper bound** on any candidate's σ_tot:
  - the maximum of σ_n(n, hit) over the road's admissible normals;
  - plus t_tol;
  - plus δn_max·|u| with the finder's δn cap.

  Alternatively, keep σ_tot and loosen the threshold by a pre-declared margin that provably covers it, e.g. χ²₃ ≤ 48κ²
  with κ = max σ_tot / min σ_tot per hit class. A looser preselection costs nothing: N_pre only grows, and at most 500
  events are overlaid.
- (ii) State that the preselection and the with-PU fit use **the same smeared PV draw**, seeded from the toy event. If not,
  add σ_PV to (i).
- (iii) State that the with-PU event **merges the stored C′₀ simulated toy hits** (as the signal injection does) rather
  than re-simulating the toy.
- (iv) Add a zero-cost check: on C′₀ (no PU), the number of attributed candidates in non-preselected events must be
  exactly 0. Report it with f_pre, and treat a non-zero count as a bug before production.

---

## 4. Category C

- **C-1. NI: the 22 mm f_pre misses the dominant preselection path, and the "6-7 decades" statements are now stale at
  every r_NI.**
  - *The missed path.* At r_NI = 22 mm, prong A's line plus the PV always defines a plane that contains the NI vertex,
    because the vertex is on A. A hit of prong B on TBPX L1 is only ≈ 8 mm from the vertex. It lies within 4σ_tot
    (≈ 138 µm) of that plane whenever |θ⊥(B)| ≲ 0.017 rad, compared with the ≈ 2 × 10⁻⁴ rad that full coplanarity
    (P_cop) needs.
  - *f_pre.* With the plan's own f₂ = 0.3-0.5 and prong spread 0.1-0.3 rad, this gives f_pre ≈ 0.07-0.35
    (`r6_checks.json` → `NI22_line_plus_vertex_hit`). That is ×50-170 the fix's 4 × 10⁻⁴-7 × 10⁻³, and N_pre ≈ 2 × 10³-10⁴,
    not 12-200.
  - *Expected counts.* The preselected 22 mm population is then mostly "line + one near-vertex hit", so its counting-rung
    rates look like the kink row (250-440 at R0, 3-40 at N_IP2 ≥ 7), not 70-410 at N_IP2 ≥ 7. The design conclusion
    (O(10²) at the loose rungs, ≥ 10 to N_IP2 ≥ 6) still holds.
  - *Validity.* It is not a correctness problem: the attribution sends these candidates to B_NI, which is conservative.
  - *Feasibility.* The attributable NI rate at R0 is:
    - ≈ 0.6-3.1 per event from the kink path at 30/61.5 mm;
    - ≈ 0.06-0.5 per event from this path at 22 mm (`NI_rate_at_R0_per_event`);
    - together, 1.3-3.3 decades above the §4.2 ESTIMATE of 2 × 10⁻³-3 × 10⁻² "before F1".
  - *Stale statements.* The §4.2 note limits "not an upper bound" to r_NI ≥ 30 mm. §2.6 l.827 ("6-7 decades needed for
    NI"), §4.2 l.1326 and §12 risk 3b still quote 6-7 decades unqualified.
  - *Stale reach.* The C′₀ bullet's "zero-count reach … 10⁻⁴ per r_NI" (l.1242) predates the preselection. The NI/DIF
    h/o/dE/dx factors are now measured on the preselected C′₀ events only, so the zero-branch value is 1.14/N_pre.
  - *Fix.* Correct the 22 mm row of the table (or mark it "lower bound on f_pre; dominated by line + vertex-hit
    configurations"). Extend the note to all r_NI. Update the three "6-7 decades" statements to "≈ 8-10 decades with the
    kink and line + vertex-hit paths (ESTIMATE)". Replace "10⁻⁴ per r_NI" with "1.14/N_pre under item 4a".
- **C-2. "First zero along the ladder order" can discard the strongest available bound.**
  - The ladder puts F0 families (measured on C′_PU, M ≤ 500, often tens at the deep rungs) before F1 (measured on C′₀, M up
    to 10⁵ for guns, ≈ 10⁴ for kinks).
  - If an F0 factor and an F1 factor are both zero, the term carries 1.14/M_F0, and the C′₀ bound enters as 1. The loss is
    up to ×200-2 000 (`first_zero_order`).
  - Using instead the zero factor with the **largest M_j** (smallest bound) is equally valid. Each factor is ≤ 1, M_j is
    fixed by the looser requirements, and P(N_j = 0 ∧ p_j > 1.14/M_j) ≤ 0.32 for any pre-declared choice rule that depends
    only on the M_j. It keeps "one bounded factor per term".
  - This is conservative either way, so it is not a B. Decide before the freeze.
- **C-3. The c test cannot involve a zero factor.** §2.5 item 4a says the c test "covers that substitution". For a zero
  factor, no joint population exists, so the non-zero conditionals that still multiply it are uncorrelated with it by
  assumption. One sentence suffices: for such terms, use the largest c measured among the term's other factors, or a
  pre-declared c = 1 with the term flagged (it is already flagged).
- **C-4 (nit, pre-existing).** B_NI = (NIs per event) × P(pass | r_NI) × N_trig (l.1333) does not show the P(PV line)
  ≈ 0.22 factor. R5 and §4.2 use it. State whether the NI/DIF toy samples the parent vertex from the PU vertex
  distribution, so that the factor is inside P(pass | t), or places it on the PV, so that ×0.22 is explicit.

---

## Verdict

**ITERATE.** 0 Category A, 1 Category B, 4 Category C.

R5 B-1 (a) and (c) and R5 C-1…C-3 are genuinely resolved:
- no fixed-density sample is credited with thinning depth;
- the zero-count rule is conservative against the Poisson posterior, bounded once per term, and referenced
  consistently in §2.5 items 4/4a/9, §4.1, §4.2, §11 and §0;
- the schedule and dE/dx nits are fixed.

R5 B-1 (b), the preselection design, is sound. Its claimed exactness needs σ_h and the PV pinned down to be at least as
loose as the candidate's, and the toy hits reused rather than re-simulated (new **B-1**). This is a text-only fix with a
zero-cost C′₀ check, and it changes no cost, schedule or approved decision.
