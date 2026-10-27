# Fix R5: Stage-4 plan after review R5 (C001 quirks theory track)

Fixer S4PLAN-R5, 2026-10-13. Input: `review/REVIEW_S4PLAN_R5.md` (0 A, 1 B, 3 C). Only `acts/stage4/plan.md` was edited.

**Output.** `data/acts_stage4/fix_r5/f5r_cprime_counts.py` → `f5r_cprime_counts.json`:
- sha256 `e39f25d37888d01b02da49ff4989bf13ce7c76cb8fa044fdfada5a82a2615fa1`;
- arithmetic only, standard library, 0.03 CPU-s.

**Unchanged:**
- the C′ cost, every campaign and decision-table number, the schedule and the approved decisions;
- the finder speed-up files (`acts/stage4/finder/`, `data/acts_stage4/g2/`).

## B-1: RESOLVED (text and design only; cost unchanged)

**(a) Thinning is no longer a depth mechanism for fixed-density samples.**
- *SM hard-scatter sentence (§4.2, wrong since R1).* It is replaced. The SM samples exist only at ρ = 1, so thinning gives
  densities < 1, and T1 is not applicable. Depth now comes from the rung-to-rung factorisation of §4.1 step 3:
  - it starts from the deepest rung with ≥ 10 hard-scatter-involving candidates;
  - each conditional is measured on the tightest population with ≥ 10 entries;
  - the factorisation/independence test (correlation factor c), T3 and the T3 failure path run on that sample.

  Thinning stays only as a k-decomposition diagnostic.
- *C′_PU (§4.2, new "Depth for every C′_PU topology" bullet).* The same correction applies. Depth comes from:
  - the rung factorisation on C′_PU, with the independence test and T3;
  - h, o and dE/dx factorised from C′₀.
- *Pointer.* §4.1 step 3 now points to the shared rule for measuring populations and zero counts.

**(b) The NI and DIF with-PU samples are preselected (§4.2, new bullet).**
- *Preselection.* Only C′₀ toy events that pass a PU-independent preselection are overlaid on PU. The preselection: some
  triple of toy hits, in 3 distinct layers and from ≥ 2 toy particles, has a PV-constrained χ²₃ = λ_min(Σ u uᵀ/σ²) ≤ 48,
  i.e. all three hits lie within ±4σ_tot of one plane through the PV.
- *The overlay is exact.* The toy's hits are identical with and without PU: smearing uses doMerge = False, and smearing and
  hit efficiency come from the toy's seed.
- *Necessity.*
  - The attribution rule (C-1) requires ≥ 3 core toy hits in ≥ 3 layers from ≥ 2 particles, each within ±4σ_tot of the
    candidate's PV plane. Such hits always contain a triple with χ²₃ ≤ 3 × 16. So P(pass ∧ not preselected) = 0 by
    construction, and P(pass | t) = f_pre × P(pass | preselected, PU) holds exactly.
  - f_pre is measured on the full C′₀ sample: 3 × 10⁴ per r_NI, 5 × 10⁴ for DIF.
  - Single-line toy configurations are the single-track-plus-random class that every in-road PU track forms in B1. NI and
    DIF add a few % to the ≈ 3.5 × 10³ such tracks per event, so B_PU and its density σ_ln cover them.
- *Sampling.* With N_pre ≥ 500, the first 500 preselected events are overlaid. With fewer, each event is overlaid
  ⌈500/N_pre⌉ times, with a two-level bootstrap. With N_pre = 0, item 4a applies and the topology is not run.
- *Expected counts* (ESTIMATE, plan factors and the §2.1 μ_c, TDR and half-density variants):

  | sample | f_pre | N_pre | R0 = (N_IT2 ≥ 3, N_IP2 ≥ 4) in 500 | N_IP2 ≥ 6 | N_IP2 ≥ 7 |
  |---|---|---|---|---|---|
  | NI 22 mm, two-prong | 4 × 10⁻⁴-7 × 10⁻³ | 12-200 (42-3 overlays each) | 430-500 | 240-490 | 70-410 |
  | kinks: DIF; NI 30 / 61.5 mm (parent + one prong, coplanar by construction) | 0.3-0.9 | ≥ 9 × 10³ | 250-440 | 30-180 | 3-40 |

  Before preselection the NI 22 mm sample had 0.15-2.5 at R0. Now every sample has O(10²) counts at the loose counting
  rungs and ≥ 10 down to N_IP2 ≥ 6. Width and χ²_core are measured, not estimated.
- *New disclosure.* The §4.2 NI ESTIMATE counts only the two-prong path. At r_NI ≥ 30 mm the kink path is also coplanar
  with the PV, so that ESTIMATE is not an upper bound there. C′ measures the kink path.
- *Consistency.* The NI and DIF formulas in §4.2, the B-sum bullet in §4.2, the §5 table row and §11 item 5 are updated.
  Item 5 notes that C′₀ runs first within C1.

**(c) The zero- and low-count rule is new: §2.5 item 4a, frozen with `WP_RULE.md` under item 9.**
- *Scope.* It applies to every factor of every term: B1/B2, C, C′₀, C′_PU and f_pre.
- *Measuring population.* Each conditional is measured on the tightest population with M ≥ 10 entries. The independence
  test's c covers that substitution.
- *Counts N ≥ 1.* The factor enters as N/M, with the bootstrap σ_ln (≥ 1/√N).
- *Counts N = 0.* The first zero factor is the term's final factor. It enters at the 68 % CL upper bound 1.14/M with
  σ_ln = 1.0, so its 84th percentile is 3.1/M ≈ the 95 % CL bound. Other measured non-zero conditionals still multiply. A
  further zero factor enters as 1.
- *Neither 0 nor paralysing.* A zero never enters as 0, and an upper bound enters at most once per term.
- *Flagging.* Terms that use the zero branch are flagged in the B table. If such a term blocks every rung, the fallback in
  item 6 applies (or the user-approved +50 % steps).
- *Consistency of the B sum.* §2.5 item 4 says that every term is a product of factors under 4a. The §4.2 B-sum bullet
  states the f_pre factorisation and refers to 4a.

## C-1: RESOLVED

A with-PU candidate is attributed to a gun or toy only if both hold:
- ≥ 3 of its core hits, in ≥ 3 distinct layers (≥ 1 IT + PS), come from gun/toy particles, each within ±4σ_tot of the
  candidate's plane;
- those hits come from ≥ 2 distinct gun/toy particles. The looper gun needs instead ≥ 2 looper crossings in ≥ 1 layer.

Every other candidate belongs to B_PU. The rule is applied identically on C′₀ and is consistent with the preselection. The
SM samples keep their conservative ≥ 1-hit tag, because C-1 covered guns and toys only.

## C-2: RESOLVED (§2.6)

1. **Λ threshold.** The text now reads "Λ ≲ 0.7 keV" in both places. "Flat within a few %" is qualified: Ẽ1000 is +8 % at
   0.7 keV. The level changes from `maxrule_level_changes` are listed:
   - Ẽ1000 1.6 → 1.3 at 0.3-0.7 keV;
   - E1100 2.0 → 1.6 up to 0.5 keV;
   - E1200 up to 0.35 keV;
   - E900 at 0.3 keV;
   - E500 and E600 lose 1.3 at ≤ 0.45 and ≤ 0.5 keV.
2. **Citation.** The PDG 2024 silicon table is cited with its constants, together with the ≤ 0.05 % agreement of the
   Sternheimer set and the review R5 re-run. The text notes that K, Z/A and ρ cancel in R. "Recalled, UNVERIFIED" is
   dropped.
3. **E500.** In the pre-declared muon-gun unit, R/1.25 = 1.34-1.44 at E500, so 1.3 is robust at the median βγ.
   "Borderline" now applies only to R4's mean/minimum convention.

## C-3: RESOLVED (§11; §12 risk 12)

1. **Production window.** "47 net (50 gross − 3 h for the inter-campaign reports and approvals)". The `f4r_deadline.py`
   docstring ("Wed 13:00 → Fri 12:00 = 47 h") is reconciled in the plan text: it is the same 47 h with the 3 h placed at
   the start. The probe is left unchanged as the audit record.
2. **G3 slot.** The slot is exceeded for t₁ ≳ 5.4 s (+1.0 h at 7 s, +4.2 h at 12 s; checked from the plan's G3 formula).
   The overrun is treated as a slip, and the margins stay positive.
3. **Slip rule.** If a slip leaves less window than C1 itself, the next-slower row applies: C1a → C1b (cut at the stop,
   completed jobs kept), then C1r, then ask the user. Risk 12 is aligned.
4. **A1.** A1 is listed once: C1 reuses the G2 A1 output, and its 2 CPU-h stay in the C1 cost as a reserve. No row changes.

## Neighbourhood checks

- **Grep for stale text.** None of these remain: "PU interactions thinned", "same thinning", "always kept", "T1/T3",
  "≥ 1 in-band hit" (except the SM tag and the R4 quote), "Λ ≲ 0.6 keV" or "recalled, UNVERIFIED".
- **Numbers.** No numerical result of the plan changed: costs, t₁ and t₂ limits, reach and admissibility levels are the
  same.
- **Header.** It has an R5 revision note and the new probe path.

## Needs user input

None new. D4-16 at G2a stands as in R4.
