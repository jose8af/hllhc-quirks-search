# Critical review R8 (narrow verifier): Stage-4 plan after fix R7 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R8, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`03-review.md` §6.

Classification, as in R2-R7:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether R7 B-1 and C-1…C-4 are resolved, and whether fix R7 introduced a new A or B.

Inputs read:
- `plan.md`: header R6/R7 notes (l.80-104), §2.1 band (l.411-414), §2.2 steps 2-5 (l.466-520), §2.5 item 9 (l.820-830),
  §4.2 C′ bullet, preselection, attribution, NI and DIF (l.1278-1445), §8 V4-10 (l.1792), §11 item 5 (l.1929-1934);
- `REVIEW_S4PLAN_R7.md`, `FIX_S4PLAN_R7.md`, `review_r7/r7_checks.json`;
- the prototype `acts/stage4/probes/f1r_finder.py` docstring (σ_tot² = σ_n² + t_tol², with no δn).

The finder speed-up files were not read.

**Independent check.** `data/acts_stage4/review_r8/r8_checks.py` → `r8_checks.json`:
- sha256 (py) `071fd343…5beeb40`, sha256 (json) `c572bf7b…7cc99`;
- system python3 `-I`, standard library only, < 1 CPU-s.

It computes how much wider σ_tot gets under the frozen capped δn than in the δn = 0 prototype, per barrel layer, at
η = 0 and η = 1. Inputs:
- σ_n,min from the pitch/√12;
- t_tol = 30 µm;
- δn = 2 mrad (the seed stage), and 0.77 and 0.27 mrad (the R7 `refit_dn_rad` values with PU help).

---

## 1. Status of the R7 items

| R7 item | Verdict | Evidence |
|---|---|---|
| **B-1** δn capped inside σ_tot | **Resolved as asked. A new B-1 is raised on what is frozen** | See *B-1 logic* below. |
| C-1 pre-CKF / pre-merge hand-over | Resolved | See *C-1 detail* below. |
| C-2 0.22 label | Resolved | 0.22 is labelled a "conservative upper value" and its origin is given (R1 l.117, B-4 (a), λ = 0.251, 1 − e^−λ = 0.222). It is labelled wherever it is used: l.1368, l.1414-1420 and the B_NI formula (l.1436-1439). The ×15-35 overstatement and the "8-9 decades carry the same factor" note are both present. |
| C-3 DIF reach | Resolved | l.1286-1288. 1.14/(5 × 10⁴ × 0.9) = 2.53 × 10⁻⁵ and 1.14/(5 × 10⁴ × 0.3) = 7.6 × 10⁻⁵. Both reproduce. |
| C-4 double-count note | Resolved | l.1396-1399. Its wording and order of magnitude match R7. |

**B-1 logic.**
- *Attribution ⇒ preselection holds without exception, and it does not depend on δn.*
  - An attributed candidate has ≥ 3 toy core hits in ≥ 3 layers from ≥ 2 particles. Each hit is within ±4σ̂_h of the
    candidate's PV-constrained plane, evaluated at its stored C′₀ position.
  - So a triple exists with one hit from a second particle plus hits in two further layers. That triple has
    Σ(n·u)²/σ̂_h² ≤ 48 about the candidate's own normal, hence λ_min ≤ 48.
  - The PV is the same stored draw, σ̂_h is the same, and the hits are the same pre-CKF, pre-merge measurements.
  - So f_pre is exact for any δn.
- *The cap is needed only for the "superset of R5" claim.* That claim needs σ_tot,h ≤ σ̂_h, which follows from three
  facts:
  - σ_n ≤ σ_loc,max (R7 checked this, 0.99999);
  - t_tol is the same in both;
  - min(δn_fit, δn_max) ≤ δn_max, with the same |u| about the same PV.
- That claim is now unconditional (l.476-477, l.1319-1320, l.1384-1386, l.1393-1396). It is frozen in §2.5 item 9
  (l.824) and is consistent with the header (l.95-97).

**Side effect on efficiency.** The task asked whether the cap makes the tolerance too tight for poorly constrained seeds.
- It does not. The cap clips δn only relative to an uncapped δn_fit.
- Every signal-efficiency datum comes from the δn = 0 prototype, which is tighter still. With the pre-filter (5/60 mm)
  and 3 refits, that prototype collects the quirk hits.
- So the cap cannot cause an efficiency loss relative to the evidence.

The real side effect runs the other way: the bands become wider than the prototype's. That is new B-1.

**C-1 detail.**
- l.1306-1312 states the following, as asked:
  - the preselection uses all stored toy measurements, before the CKF removal of §1.6 and before the U-5 b merging;
  - the V4-10 hash is taken on those measurements;
  - the attribution tests each toy-linked core hit at its stored C′₀ position and σ;
  - what CKF and merging do in the with-PU event goes into the measured P(pass | preselected, PU).
- The V4-10 row (l.1792) and §2.5 item 9 (l.825) match.
- §11 item 5 (l.1932-1934) is unchanged but compatible.

---

## 2. Category A

None.

---

## 3. Category B

### B-1 (new in fix R7). The frozen σ_tot is ambiguous between δn = 0 and min(δn_fit, 2 mrad). The two differ materially in every rung variable, and every number in the plan is for δn = 0.

**Evidence.**
1. **The text allows two readings.**
   - §2.2 step 3 (l.473-476) *defines* δn = min(δn_fit, δn_max), with δn_fit the seed-plane error at collection and the
     fit error at each refit. §2.5 item 9 (l.824) freezes "the capped δn of σ_tot".
   - The same passage, and header l.96, says "the prototype's δn = 0 satisfies the cap". The fix report adds that the §2.1
     band and the §4.1 storage column "are the δn = 0 prototype case, consistent with the cap".
   - But δn = 0 is not an instance of min(δn_fit, δn_max), because δn_fit > 0 for every plane. It only satisfies the
     *inequality* δn ≤ δn_max.
   - So `WP_RULE.md` could be written either way, and only one of the two is backed by evidence.
2. **The capped δn_fit is large exactly where it matters** (R7 `r7_checks.json`; R8 `r8_checks.json`).
   - **At the seed stage**, δn_fit = 0.4-0.5 mrad / sin∠ exceeds 2 mrad for seed angles below 0.18-0.25 rad, which is
     most seeds. So δn = 2 mrad there. At η = 0-1, σ_tot is then wider than the prototype's by:
     - ×4-6 on TBPX L2 (the L2 seed confirmation, and the seed N_L2 compared with T_seed);
     - ×10-15 on L4;
     - ×11-38 on PS.
   - **After refit with PU help**, δn_fit = 0.27-0.77 mrad. σ_tot is then wider by:
     - ×1.6-5.7 on TBPX L4;
     - ×1.8-15 on PS;
     - ×5-32 nominally on 2S. The 2S figures are upper values, because the 2S σ_n can be far larger than pitch/√12
       after projection.
3. **Each frozen rung variable depends on it.**
   - *Counting rungs (N_IP2, N_2S2).* μ_c, the random crossings per band (§2.1), scales with the band width. So the PU pass
     rates at a given rung rise by a large factor, and the ladder depth the margin study (§2.4) found adequate does not
     carry over.
   - *χ²_core.* Its weights are wᵢ = 1/σ_tot,i² (l.513). Squared ratios of 3-200 on L4/PS lower the PU χ²_core. The
     variable also gains an anti-rejection feedback: a worse-constrained PU candidate gets a larger δn_fit, hence a
     smaller χ². The margin-study χ² evidence (median 2.87 PU-only) was taken at δn = 0.
   - *Refit and ranking.* Outer hits are down-weighted by those same factors, so the plane is driven by the IT hits.
   - *Cost.* The l.682 combinatorics ("2 × 10⁵ seeds pass T_seed = 6") and the T_seed = 6 choice (l.491) were measured
     with δn = 0 bands. Seed-stage bands ×4-15 wider in IT push more seeds over T_seed, which raises t₁.
   - The plan nonetheless states that C1 fits one Mac day only up to t₁ ≈ 7 s, and that "the C′ cost, the campaigns and
     the schedule are unchanged".
4. **Why this is B and not A or C.**
   - No result is wrong yet: B1/B2 and G2 would measure whatever finder is frozen.
   - But the rule frozen at the start of G2 would contain a finder that no probe, margin study, T_seed tuning, μ_c table
     or t₁ estimate has used. Under one reading it could change C1 feasibility and whether the ladder reaches the target.
   - That decision belongs in the plan before the user decides, not after the freeze. "No new rung after the freeze"
     (§2.5 item 6) makes a mismatch found later expensive.

**Required fix** (text only, zero cost; choose one):
- **(a) Preferred.** Freeze **δn = 0 in σ_tot**, i.e. σ_tot² = σ_n² + t_tol², the finder every probe, the margin study,
  T_seed, the §2.1 μ_c and t₁ rest on.
  - σ_tot,h ≤ σ̂_h then holds trivially. σ̂_h keeps its δn_max·|u| term as extra preselection and attribution margin, so
    the B-1 R7 logic and f_pre exactness are unchanged.
  - Optionally move min(δn_fit, δn_max) to a pre-declared A5/B1 variation beside t_tol = 0/100 µm.
  - Edit §2.2 step 3, §2.5 item 9 (l.824), header l.95-97, and the "superset" sentences at l.1319-1320, l.1384-1386 and
    l.1393-1396 ("σ_tot has no δn term").
- **(b) Alternative.** Keep the capped δn_fit as nominal, and state explicitly that it is a finder change relative to the
  prototype:
  - T_seed, the §2.1 μ_c table, the t₁ entering the campaign decision table, and the PU χ²_core/counting margins are
    re-measured with it before the freeze and before the C1 cost decision;
  - the §2.1/§4.1 numbers and the cost lines are marked as δn = 0 values not yet valid for the frozen finder;
  - the user is told that C1 feasibility may move.

  Either way, delete "the prototype's δn = 0 satisfies the cap" as a statement about the frozen definition.

---

## 4. Category C

- **C-1 (wording).** Header R6 bullet l.84: "the stored C′₀ toy hits (merged, not re-simulated)". Here "merged" means
  *inserted into the PU event*. Since fix R7, "merging" in §4.2 also means the U-5 b analysis-level hit merging, which
  the preselection is explicitly *before*.
  - *Fix:* say "inserted, not re-simulated" in the header (and in §11 item 5, l.1932, "merges the stored C′₀ toy hits").
- **C-2 (note, no action).** The attribution's truth link for a U-5 b-merged toy + PU cluster is not stated: which stored
  position is tested if a merged hit links to two particles?
  - It cannot create a leak, because the preselection uses all stored toy measurements and the attribution tests stored
    positions only.
  - It can only change which with-PU candidates are attributed, and that is measured.
  - Optional one-liner: "a merged hit is tested at each of its toy-linked stored positions."

**Global spot check of the touched passages.**
- The header R7 bullets (l.94-104) match §2.2 step 3, §2.5 item 9, §4.2 (overlay, preselection, attribution, NI and
  DIF), §8 V4-10, and the FIX_S4PLAN_R7 item list.
- §1 lists V4-1…V4-10 (l.377).
- 0.22 is unlabelled only at l.785 and l.1675. Both are unrelated numbers (a σ_ln and a CPU-h value).
- No numeric value changed in fix R7, and the reach numbers reproduce.
- The only inconsistency found is B-1: the frozen δn definition against the δn = 0 numbers.

---

## Verdict

**ITERATE.** 0 Category A, 1 Category B, 2 Category C.

R7 B-1 is resolved as asked:
- attribution ⇒ preselection holds for every candidate at any δn;
- with the cap, the attributed set is a superset of R5's for every candidate.

R7 C-1…C-4 are resolved, and their numbers reproduce.

Fix R7 introduced one new B. It froze a σ_tot whose δn is min(δn_fit, 2 mrad), while calling the δn = 0 prototype a
special case of it, which it is not. The capped δn_fit widens the IT/PS bands by ×1.6-15 after refit (more at the seed
stage), and it enters μ_c, the counting and χ²_core rungs, T_seed and t₁, none of which has been measured with it. The
zero-cost remedy (a) is to freeze δn = 0 in σ_tot, keeping δn_max only inside σ̂_h.
