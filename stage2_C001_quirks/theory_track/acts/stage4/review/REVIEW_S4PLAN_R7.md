# Critical review R7 (narrow verifier): Stage-4 plan after fix R6 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R7, a fresh critical reviewer, 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`; methodology
`03-review.md` §6.

Classification, as in R2-R6:
- **A** blocks or invalidates;
- **B** must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** is minor.

The verdict is PASS only with 0 A and 0 B. Approved decisions are not reopened.

**Scope.** This round checks whether R6's B-1 and C-1…C-4 are resolved, and whether fix R6 introduced a new A or B.

Inputs:
- `plan.md`: header R6 note (l.80-89), §1.5-1.6 (U-5 b merging, CKF removal), §2.2 steps 2-4 (σ_tot, δn), §2.5 items
  4/4a/9, §4.2 C′ bullet (l.1270-1375), the NI/DIF paragraphs (l.1376-1407), §8 V4-10, §11 item 5, §12 risk 3b;
- `REVIEW_S4PLAN_R6.md`, `FIX_S4PLAN_R6.md`;
- `fix_r6/f6r_numbers.{py,json}`, whose sha256 values match the fix report;
- the finder prototype `acts/stage4/probes/f1r_finder.py`, for how σ_tot is coded;
- `CRITICAL_REVIEW_S4PLAN_R1.md`, for where 0.22 comes from.

The finder speed-up files were not read.

**Independent checks.** `data/acts_stage4/review_r7/r7_checks.py` → `r7_checks.json`:
- sha256 (py) `d3cce4cf…a209b4`, sha256 (json) `e3941ab6…96b48d`;
- system python3 `-I`, standard library only, 0.4 CPU-s;
- no acts env, no simulation.

---

## 1. Status of the R6 items

| R6 item | Verdict | Evidence / residual |
|---|---|---|
| **B-1 (i)** n-independent σ̂_h | **Resolved for exactness. A new, separate anti-conservative gap → new B-1** | See *(i) detail* below the table. |
| **B-1 (ii)** same PV draw | Resolved | l.1285-1286 and l.1294: the smeared PV is drawn once from the toy seed in C′₀, stored, and passed to the with-PU event. No σ_PV term is needed. |
| **B-1 (iii)** stored hits | **Resolved in intent; two hand-over steps are unstated → C-1** | The stored C′₀ Fatras SimHits are merged, with no re-simulation (l.1281-1284). Not stated: the toy-PU analysis-level merge (U-5 b, §1.5) and CKF removal (§1.6) act on the toy hits in the with-PU event only. |
| **B-1 (iv)** gate V4-10 | Resolved (adequate) | §8 l.1755, §4.2 l.1303-1310, §2.5 item 9 l.807-808 and §11 item 5 l.1895-1897 agree. The test is "= 0 exactly" on the full C′₀ sample. The failure path is pre-declared: no use until fixed, otherwise f_pre × (1 + N_leak/N_attr,pre) with \|ln(1 + N_leak/N_attr,pre)\| added to σ_ln, flagged, user told. |
| C-1 NI numbers | Resolved; numbers reproduce | See *C-1 numbers* below. One conservative nit → C-3. |
| C-2 largest-M_j zero | Resolved | §2.5 item 4a l.739-750. The chosen bound depends only on the M_j. Every other zero factor enters as 1. Its coverage has the same structure as R5's accepted first-zero rule. |
| C-3 c and zero factors | Resolved | l.728-731: c is computed among the non-zero factors. A zero-branch term carries the largest c among its other factors (1 if none) and is flagged. |
| C-4 PV-line factor | **Explicit as asked, but the factor's meaning is misapplied (conservative) → C-2** | See *C-4 detail* below. |

**(i) detail: exactness.**
- σ_n(n) ≤ σ_loc,max for every n, since (n·e_u)² + (n·e_v)² ≤ 1. Checked: max σ_n/σ_loc,max = 0.99999 over 2 × 10⁵ random
  normals (`sigma_n_over_sigma_locmax_max`).
- The **attribution now uses the same σ̂_h** (l.1356-1359). So for any candidate, whatever its δn:
  - ≥ 3 toy core hits in ≥ 3 layers from ≥ 2 particles, each within 4σ̂_h, give a triple;
  - that triple has χ²₃ ≤ 48 about the same stored PV;
  - hence it passes the preselection (λ_min ≤ 48).
- The R6 combinatorial argument carries over unchanged.
- **Leak question (δn > 2 mrad).** A candidate with δn > δn_max **cannot** be attributed in a non-preselected event. The
  implication "attributed ⇒ preselected" never uses δn. So no f_pre leak exists at any δn.
- The δn > 2 mrad issue is the opposite direction: **under-attribution**. That is the new B-1 below.

**C-1 numbers.** These are recomputed independently in `C1_recheck`:
- R0 rate 0.583 + 0.06 = 0.643 and 3.111 + 0.53 = 3.641 per event;
- log₁₀(rate/3 × 10⁻⁹) = 8.33-9.08, and 9.33-10.08 against 3 × 10⁻¹⁰;
- N_pre(22 mm) = 3 × 10⁴ × (0.069-0.5) = 2 070-15 000;
- reach 1.14/N_pre = 7.6 × 10⁻⁵-5.5 × 10⁻⁴ (22 mm) and 4.2 × 10⁻⁵-1.27 × 10⁻⁴ (NI kinks).

All of these match `f6r_numbers.json` (`matches_f6r: true`). The script reads the R6 inputs correctly; it takes f_pre low
from `per_hit_4sigma` and high from `chi2_budget`. "Lower bound" is the right qualifier for the 22 mm f_pre, because σ̂_h
only loosens it.

**C-4 detail.** The NI toy places the parent at the true PV, and B_NI shows P_PV-line ≈ 0.22 explicitly (l.1398-1402).
B_DIF takes a factor of 1, which is conservative (l.1405-1407).
- *Origin of 0.22.* It is `CRITICAL_REVIEW_S4PLAN_R1.md` l.117: "≈ 0.25 expected (P ≈ 22 %) PU vertices within ±0.1 mm of
  the PV". This reproduces: the vertex density at a luminous-region PV is 200/(2√π σ_z) = 1.254 mm⁻¹, λ = 0.251, and
  1 − e^−λ = 0.222 (`PV_line`).
- So 0.22 is the **per-event probability that some PU vertex coincides with the PV**. It is not the per-NI probability
  that the parent comes from the PV line, which is how 26 NIs/event × 0.22 uses it. See C-2.

---

## 2. Category A

None.

---

## 3. Category B

### B-1 (new in fix R6). Under-attribution of candidates with δn > δn_max is anti-conservative. It is common under the plan's own definition of δn, it is counted in no term, and it has only a diagnostic with no pre-declared action.

**Evidence.**
1. **What fix R6 wrote.** Attribution requires each toy hit within ±4σ̂_h, with δn fixed at δn_max = 2 mrad.
   - For a candidate with δn > δn_max, "a toy hit within 4σ_tot but outside 4σ̂_h is not attributed; the number of such
     R0-passing candidates in C′_PU is reported as a diagnostic" (l.1368-1370). No threshold or action is attached.
   - R5's attribution used the candidate's own 4σ_tot. For δn > δn_max, fix R6 therefore narrows the frozen attribution
     relative to R5.
   - Candidates that lose attribution fall into no B term. Fatras has no NI and no DIF (§4.2 table, l.1235-1236), so
     B1/B_PU cannot contain them. The "configurations the preselection removes" argument (l.1312-1315) covers single-line
     configurations only, and these candidates can have two toy lines in band.
2. **δn is not pinned, and the 2 mrad cap is not a bound on it.**
   - §2.2 step 3 (l.459-460) defines δn as "the seed-plane error". The prototype finder codes σ_tot² = σ_n² + t_tol², with
     no δn at all (`f1r_finder.py` l.13).
   - δn_max = 2 mrad is justified as "the candidate-merge tolerance". That tolerance compares two candidates' normals. It
     does not limit any single candidate's normal uncertainty.
3. **Size under each reading** (`r7_checks.json`):
   - **Seed-plane error (literal §2.2).** For an (L4, L3) seed through the PV, δn ≈ 0.4-0.5 mrad / sin∠(u_a, u_b). That
     exceeds 2 mrad whenever the seed angle is < 0.18-0.25 rad (`seed_angle_for_dn_eq_2mrad`). The seed window
     \|Δφ\| < 0.3, \|Δη\| < 0.2 allows angles up to ≈ 0.36 rad, so this is most seeds:
     - quirk-like or near-collinear seeds give 12-49 mrad at 0.01-0.03 rad;
     - the NI-22 "prong-A line" seed gives ≈ 30 mrad.

     Under this reading the attribution is **narrower than R5's for most candidates**, and the text's "only loosens …
     conservative" is false.
   - **Refit (Fisher) normal error.**
     - With ≥ 4 in-band PU hits spread across the window, δn ≈ 0.3-0.8 mrad < 2 mrad for NI-22 and for kinks. The cap
       then holds for typical C′_PU candidates.
     - Without PU help it does not hold:
       - NI-22 line + near-vertex hit: 1.8-5.1 mrad;
       - DIF kink at 3-30 mrad: 1.7-17 mrad;
       - two close lines (1 mm apart at L4): 6.6 mrad.
     - The PS lever arm does not rescue these cases, because the weak direction is a rotation about the line.
   - **δn = 0 (as prototyped).** σ_tot ≤ σ̂_h always, and the issue vanishes.

**Why it matters.**
- The attribution rule is frozen in `WP_RULE.md` (§2.5 item 9).
- Its conservative claim rests on a quantity the plan has not defined. Under the plan's literal definition, the dropped
  fraction can be O(1) and goes into no term.
- A diagnostic with no pre-declared consequence leaves any later remedy unregistered.
- This is the R6 B-1 standard: an anti-conservative gap in a frozen rule, with no closure.

**Required fix** (text only; zero cost; choose one):
- **(a) Preferred.** In §2.2 steps 3-4, define δn in σ_tot as the current (re)fit's normal uncertainty **capped at
  δn_max**: σ_tot² = σ_n² + t_tol² + (min(δn, δn_max)·|u|)².
  - The prototype's δn = 0, used for every probe and the margin study, is a special case.
  - Then σ̂_h ≥ σ_tot,h for **every** candidate, attribution is a superset of R5's for every candidate, and the
    δn > δn_max sentence and its diagnostic can be removed.
  - Freeze the δn definition with σ̂_h (§2.5 item 9).
- **(b) Alternative.** Keep the finder's δn uncapped, and give the diagnostic a pre-declared consequence. For example, count
  the σ_tot-attributable candidates at each rung on C′₀ as well, in preselected and non-preselected events. Add them to
  the term, with the V4-10 inflation f_pre × (1 + N_leak/N_attr,pre) computed with them, flagged.
  - Also state δn_max's role honestly: it is a chosen tolerance, not a bound.

---

## 4. Category C

- **C-1. "Exactly its C′₀ hits" omits two with-PU-only steps; state how they are handled.**
  - *Merging.* §1.5 U-5 b merges every pair on a sensor, including quirk-PU pairs, so also toy-PU pairs. A merged toy hit
    moves by up to p/2, which can cross the 4σ̂_h edge.
  - *Size.* P(merge) ≈ 0.9-5 × 10⁻³ per TBPX L1 toy hit. The edge fraction is ≈ 1-3 %. The leak is therefore
    ≲ 10⁻³ relative to f_pre (`merge_leak`), which is negligible.
  - *Consequence for V4-10.* V4-10 cannot see this, because C′₀ has no PU. If V4-10's per-event hash is taken **after**
    merging, it fails on ordinary events by design, and the stop rule would block C′_PU.
  - *CKF removal.* §1.6 removal of toy prongs (pT > 0.9 GeV, \|d₀\| < 4 mm) can differ between C′₀ and the with-PU event.
    This is safe only if the preselection uses **all** stored toy measurements, before CKF removal and before merging.
  - *Fix.* Two sentences:
    - the preselection uses all stored toy measurements before CKF removal and U-5 b merging;
    - the V4-10 hash is on those pre-merge measurements, and the attribution tests each toy-linked core hit at its stored
      C′₀ position and σ (or σ̂_h is enlarged by p_max/2).
- **C-2. The 0.22 PV-line factor is a per-event vertex-coincidence probability, used as a per-NI fraction. It is
  conservative by ≈ ×15-35.**
  - The 26 in-road NIs/event come from ≈ 3.5 × 10³ in-road tracks of about 201 vertices. The fraction whose parent
    starts within ±0.1 mm of the PV is ≈ (1 + 0.25)/201 = 0.006, treating the HS like a PU vertex. It is ≈ 0.014 if the
    tolerance is taken as 0.1 mm/\|n_z\|, averaged over plane orientation (`PV_line`).
  - Not a correctness error, since it is conservative. But it adds ≈ 1.2-1.5 decades to B_NI and to the "8-9 decades"
    statements, and the WP rule could reject points needlessly.
  - *Fix.* Either label 0.22 "conservative upper value (P of a coincident PU vertex, R1 B-4 a)", or replace it before
    the freeze with the per-NI fraction:
    - (n_HS,road + 0.25 × n_PU,road per vertex)/n_road,all;
    - with the ±tolerance/\|n_z\| variation in σ_ln.

    The same normalisation would apply to B_DIF, which carries factor 1, also stated as conservative.
- **C-3 (nit).** "≈ 4 × 10⁻⁵-1.3 × 10⁻⁴ for the kink samples" (l.1268-1269) is the NI-kink reach. The DIF reach is
  1.14/(5 × 10⁴ × 0.3-0.9) = 2.5 × 10⁻⁵-7.6 × 10⁻⁵. The quoted range is conservative; add the DIF value or write "NI kinks".
- **C-4 (note, no action).** σ̂_h's δn_max·|u| term widens attribution to about ±8 mrad as seen from the PV (σ̂ ≈ 0.3 mm at
  TBPX L4, against σ_tot ≈ 42 µm).
  - Some pure-PU candidates will pick up ≥ 3 toy hits from ≥ 2 particles and be attributed. That is conservative double
    counting.
  - Order of magnitude: rate_NI × 0.22 × f_pre × O(10⁻³) × P_PU ≪ P_PU.
  - Optional: report the fraction of attributed C′_PU candidates whose in-band hits span ≥ 2 interactions.

**Global spot check.**
- The header R6 bullets (l.80-89) agree with §4.2, §2.5 item 4a/9, §8 V4-10 and §11 item 5.
- The §1 file table lists V4-1…V4-10 (l.364).
- "6-7 decades" survives only as labelled two-prong history, with the 8-9 / 9-10 update beside it (l.1388-1391, l.2026-2028,
  §2.6 l.850).
- The C′ cost, campaigns and schedule are unchanged, as claimed.

---

## Verdict

**ITERATE.** 0 Category A, 1 Category B, 4 Category C.

R6 B-1 is resolved in what it asked:
- f_pre is now exact by construction at any δn, because the attribution and the preselection share σ̂_h, the PV and the
  hits;
- the PV draw and the stored hits are handed over;
- V4-10 has a pre-declared failure path.

R6 C-1…C-4 are resolved; the numbers reproduce.

Fix R6 introduced one new B: candidates with δn > 2 mrad lose attribution with only a diagnostic, and under §2.2's "seed-plane
error" δn that is most candidates. The text-only remedy is to cap δn at δn_max inside σ_tot (option a), which costs
nothing and matches the prototype (δn = 0). C-1 (merge/CKF hand-over wording) should be fixed alongside.
