# Critical review R2: Stage-4 plan, revision R1 (`acts/stage4/plan.md`), C001 quirks theory track

Reviewer: S4PLAN-R2 (a fresh critical reviewer; no earlier rounds seen), 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`;
methodology `01-core.md`, `03-review.md` §6. Classification follows the caller's scheme:
- **A** = blocks or invalidates;
- **B** = must be fixed in the plan before the user decides and before `WP_RULE.md` is frozen;
- **C** = minor or optional.

The verdict is PASS only with 0 A and 0 B. Approved decisions (U-1…U-5, D4-1…D4-12) are not reopened.

**Inputs read:** `plan.md` (1030 lines), `FIX_S4PLAN_R1.md`, both R1 reviews, the `f1r_*.py` probes, everything in
`data/acts_stage4/fix_r1/`, the TDR Fig. 6.3 page render, `sim/stage3/results/P2.json`, and `r1c_signal_handles.{py,json}`.

**Independent checks** (≈ 0.25 CPU-h; scratch in `data/acts_stage4/review_r2/`; the probes are imported read-only and not
edited):
1. `r2_corewidth.py` → `r2_corewidth.json`. Re-analyses the fixer's own finder outputs (`fix_r1/finder/*.jsonl`) with no
   rerun. It asks whether the stored robust core width `dw_core` separates signal from PU.
2. `r2_dupcheck.py` → `dup_rho{1,2}_*.json`. Re-runs the fixer's F0 (via `import f1r_finder`, same W_c, t_tol and T_seed;
   Fatras-only) on 32 ρ = 1 trials and 2 ρ = 2 trials. It keeps the hit indices, so the duplicate-candidate explanation of
   the ×2.1-2.9 thinning over-prediction can be tested.
3. The TDR Fig. 6.3 readings, checked against the page render (`fix_r1/tdr/tdr014_p101-101.png`).
4. Arithmetic: the §6.2 totals, the NI estimate, the margin and pilot tables against `f1r_summary.json` and
   `f1r_margin.json`, and the D4-10 (a′) worked example against `P2.json`.

---

## 1. R1 items: resolved or only reworded? (task 1)

I checked every row of `FIX_S4PLAN_R1.md` against the plan text and the evidence. In summary:

**Genuinely resolved, with evidence:**
- critical A-1 (Δw cut removed; §2.2 item 6);
- B-1 (blind probe; R0 claims re-tagged in §0 and §2.4);
- B-2 / constructive A-1 (`score()` and `cross_from_cnt()` in `f1r_finder.py` use min(n_in, n_out));
- B-3 (W_c rule plus the truth table in §2.2);
- B-7: the Fig. 6.3 readings reproduce. My reading of the render is TBPX L1 ≈ 2.0 × 10⁻³, TBPS L1 strip ≈ 2.9 × 10⁻²,
  TB2S L4 ≈ 8.8 × 10⁻³ and L6 ≈ 3.4 × 10⁻³, against the fixer's 2.04 × 10⁻³, 2.82 × 10⁻², 8.3 × 10⁻³ and 3.34 × 10⁻³.
  Sanity check: 2.0 × 10⁻³ / (25 × 100 µm²) = 80 pixel hits/cm² per crossing, i.e. ≈ 3.2 GHz/cm² at 40 MHz, consistent with
  the RD53 design figure;
- B-9: written as PROPOSED (a′). The worked example matches `P2.json` → `systematics.F_m1000.robust_shifts.lmax_up/dn.lower_lmax_RIT_closed`:
  +1.82 % (sd 0.94 %) and −1.30 % (sd 0.85 %);
- B-10 (opening linearity on resolvable layers);
- C-1…C-13 and constructive B-1…B-8, C-1…C-7, with the exceptions noted below.

**Resolved in design only, as the fix report itself says:**
- **B-4/B-5:** the thinning and closure gate are specified, but the pilot fails T1 (z ≈ −4) and the closure is assigned to G3.
  This is acceptable at plan level. Findings B-3 and C-3 below concern how far the formalism reaches.
- **B-6:** the 1-D ladder, B₈₄ and the freeze are implemented. Adding SR-T/SR-G (constructive B-2) re-introduced an ambiguity
  (finding B-2 below).
- **B-8:** the B sum and the NI estimate are written, but the NI arithmetic does not reproduce from the factors given
  (C-4 below).

No R1 item was merely reworded. The two partial cases are the new B-2 and B-3, each created by a fix.

---

## 2. Category A

None. The fixer's headline measurement (task 2) is sound in the direction that matters (§3). I found no number in the plan
that is wrong in a way that invalidates a result or decision. The issues below are design and specification gaps and one
overstatement of feasibility. Each must be fixed before the freeze, so they are B.

---

## 3. The key new result: is the "F0 separation only ×3 at TDR density" measurement sound? (task 2)

**Verdict: sound as a statement about (N_L2, χ²/ndf). It is not a statement about F0 as a whole (B-1).** Details:

- **Top-up method.** `f1r_finder.topup()` adds, per layer, Poisson((ratio − 1) × N_Fatras hits on that layer) crossings.
  z is resampled from the layer's hits and φ is uniform. Stacked layers get an in/out pair at the same (φ, z), and each
  crossing is a separate "interaction". Mode 2 (used for TDR-OT) skips TBPX. The ratios in `TOPUP` equal the
  `f1r_density_bench.json` nominal values. I found no bug.
  - The pair at the same (φ, z) is not a PV-pointing stub. On PS layers with a tilted plane, the out hit can fall
    outside the 3σ band (Δd = ΔR·(ρ̂·n) ≈ 1 mm for ΔR = 2-4 mm), so the top-up is, if anything, slightly
    under-effective on PS. This is not a direction that makes PU look worse.
- **Signal overlay.** `smear_signal()` takes the per-surface σ from the PU rows of the same surface, smears rφ and z, drops
  disc, BTL, ETL and T3V hits, and uses the Stage-3 vertex with (10, 15) µm smearing and the MET at 25 GeV. Signal matching
  (≥ 50 % of the event's barrel quirk hits) is applied after the blind search. The blind event-level pass fraction agrees
  (`eff_blind_event`). No bug.
- **Statistics.** TDR-OT is 32 PU trials (8 events) and **14 signal events** over 10 points: E1000 1/2/3/5 keV with
  2/2/1/1 events, E200 1/3 keV with 2/1, Ẽ500 1/3 keV with 2/1, E1500 1 keV with 2.
  - The quoted 0.36 [0.21, 0.53] is 5/14 of a mix dominated by 1 keV events (8 of 14).
  - The ratio 0.36/0.125 = ×2.9 has a 68 % range of roughly ×1-8.
  - The "×3" is therefore a qualitative statement. The conclusion that 10 layers + χ² are 7-8 decades short does not depend
    on it: PU already reaches N_L2 = 10 in 28/32 trials.
- **Biases.**
  1. **T_seed = 6 under-explores PU in χ².** `f1r_tseed_check.json`: in 2 of 4 trials T_seed = 4 finds an equally ranked
     8-layer candidate with a lower χ²/ndf (2.12 vs 2.51; 2.09 vs 2.45). The PU pass rate at the χ² rungs is therefore
     under-estimated, and the true F0 (N_L2, χ²) margin is ≤ ×3.
  2. The IT is not topped up, so PU is under-dense by a further ×2.3-3.7 in the IT.
  3. The χ² dilution of the signal is real: in-band PU hits uniform within ±3σ contribute ≈ 3 per hit. With the χ² over all
     in-band hits, signal χ²/ndf drifts towards PU-like values at the normalised density.

  None of these makes PU look worse than it is or the signal worse than it is by more than a factor of order 1. The
  measurement stands, in the conservative direction.
- **What the measurement does not show.** It does not show that "F0 cannot separate". F0 already computes a variable that
  separates strongly at Λ ≳ 2 keV (B-1).

---

## 4. Category B

### B-1. The plan concludes that F0 cannot separate and that the WP must come from F1. Its own stored robust core width separates strongly at Λ ≳ 2 keV, and it is excluded from the ladder ("stored only, never cut on").

**Evidence** (`r2_corewidth.json`, from the fixer's jsonl; event passes if *any* candidate passes; signal = a matched
candidate passes):

| density, rung | dw_core cut | PU trials passing | signal 1 keV | signal ≥ 2 keV | signal 0.6 keV |
|---|---|---|---|---|---|
| Fatras, N_L2 ≥ 9 | none | 26/224 | 40/48 | 30/31 | 4/12 |
| Fatras, N_L2 ≥ 9 | < 20 mm | **0/224** | 20/48 | 30/31 | 2/12 |
| TDR-OT, N_L2 = 10 | none | 28/32 | 5/8 | 5/6 | 0/2 |
| TDR-OT, N_L2 = 10 | < 15 mm | **0/32** | 1/8 | 4/6 | 0/2 |
| TDR-OT, N_L2 ≥ 9 | < 10 mm | **0/32** | 0/8 | 4/6 | 0/2 |

- PU candidates fill the window: the minimum dw_core over passing PU candidates per trial is 26 mm (Fatras, N_L2 ≥ 9) and
  20 mm (TDR-OT, N_L2 = 10). A uniform fill of ±75 mm has 1.4826 × MAD ≈ 56 mm.
- Signal at ≥ 2 keV is a ribbon: median dw_core is 3.8-13 mm at Fatras density (`f1r_summary.json` → `sig_t0.*.dw_core_q`).
- The plan conflates the two width variables. §2.4 says "Δw (R0 definition) is 34-44 mm for PU and 18-36 mm for signal: it is
  window-filled and not a discriminant". That is true for Δw_R0, the rms over all in-band hits. It is not true for the robust
  core width, which §2.2 item 5 stores but never uses.
- **Physics.** A ribbon-width cut is effectively an ℓ_max cut. It trades low-Λ efficiency for rejection, which is why R1 A-1
  removed the old Δw cut. As a background-ordered ladder rung (thresholds fixed by the WP rule, signal efficiency reported
  vs Λ), it is legitimate and signal-blind. It is also the one geometric handle that acts on the measured dominant PU class:
  combinatorial candidates with k ≈ 16-47 interactions.
- The 32-trial TDR-OT sample cannot show how many decades it buys: the PU minimum falls from 26 to 10 mm between Fatras
  and TDR-OT density at N_L2 ≥ 9. Fewer candidates in a narrow ribbon is a strong geometric suppression (band length ∝
  window, P(≥ 2 crossings) ∝ μ² per layer). It is the realistic route to many decades at Λ ≳ 2 keV.

**Required fix:**
1. Add a pre-declared ribbon-width rung family to the §2.5 ladder before the freeze, e.g. a robust core width on IT + PS
   crossings < {40, 20, 10, 5} mm. A better-defined statistic would be the width of the ≥ 2-crossing hits after per-layer
   two-cluster assignment, with the χ² computed on the core hits so that it is not diluted by PU fill.
2. Alternatively, use Λ-agnostic narrow/wide categories, i.e. SRs split by width, walked by the same rule.
3. Correct §0, §2.4 and §12 risk 2: "F0's layer count and χ² cannot reach the target" is right; "F0 alone does not separate"
   is not.
4. State the expected consequence: the background-limited edge moves up in Λ (the WP is likely ≳ 1.5-2 keV for a
   background-free selection), separately from the W_c and t_tol attribution of V4-3.

### B-2. The SR-T / SR-G timing categories make the WP rule two-dimensional and undefined.

- §2.3 says SR-G is "everything else (geometry only, **a tighter rung**)".
- §2.5 item 3 says "SR-T and SR-G each walk the same ladder … The B used at rung r is the total for that rung (both
  categories)", and item 5 picks "the loosest rung r\*".
- If one rung index is shared, SR-G cannot sit at a tighter rung than SR-T, and the timing category buys nothing in the WP.
- If each category has its own rung (r_T, r_G), "loosest rung with B₈₄(total) ≤ 0.3 and all tighter" has no unique
  solution: many (r_T, r_G) pairs satisfy it, and nothing orders them.
- This must be fixed before `WP_RULE.md` is frozen at G2. It is exactly the 1-D-path requirement of R1 critical B-6.

**Required fix:** pre-declare how the two categories are combined. Options:
- (a) a fixed rung offset Δ (SR-G = r + Δ, Δ chosen on background only, e.g. so that B_G(r + Δ) ≈ B_T(r));
- (b) a pre-declared interleaved 1-D path over (r_T, r_G);
- (c) a per-category budget split (e.g. B₈₄,T ≤ 0.15 and B₈₄,G ≤ 0.15, each on its own monotone ladder).

Write it into §2.3 and §2.5 consistently.

### B-3. The extrapolation formalism as written covers only counting rungs. The WP will sit in χ², width, F1 and timing rungs, where "thinning from stored per-interaction hit counts" cannot be evaluated.

- §4.1 step 2: w_r is "computed exactly from the stored per-interaction hit counts". The probe (`thin_weights()`) evaluates
  only N_IT2 ≥ 3 and N_L2 ≥ L.
- Whether a thinned subset T still passes a p_χ² rung, a width rung (B-1), h_min, o_min, e_min (truncated mean) or SR-T
  depends on hit positions, energies and times, not on counts.
- At the TDR-normalised density the counting ladder is already saturated at ρ = 1 (PU N_L2 = 10 in 88 % of trials).
  So **every rung that matters for the WP is outside the stated formalism.**
- The plan's other route, rung factorisation (step 3), then carries the whole extrapolation. The pre-registered
  independence test only probes loose rungs.

**Required fix:** state, for each rung family, how P₁(r) is obtained.
1. Per-subset recomputation of the variable. This needs the candidate's hits stored with their interaction id, position,
   energy and time, and per-subset refits of χ², width, helix, opening and truncated mean; cost it.
2. Or factorisation P(F0 count rung) × P(rung | count rung), with an explicit independence test at the relevant density.
   Width and χ² are both driven by the in-band PU density, so they are *not* independent of the count.

Pre-register which one applies to which family, the closure test that covers it, and the ρ = 2 cost of storing hits.

### B-4. The plan overstates what F1 can do against the measured dominant PU background, and does not state plainly that the B ≤ 0.3 working point may not exist or what is delivered then. (task 3)

**F1 vs combinatorial fakes.** The measured PU candidates are combinatorial: 16-23 interactions (Fatras), 32-47 (TDR-OT),
k_min 13-22 (§2.4).
- The F1 non-helicity test (h = min over origins of χ²_helix) and the opening-linearity test (χ²_lin of |s_l| vs r) were
  designed against *single-interaction* topologies: conversions, V0s, NIs, track pairs.
- A random multi-particle hit set is non-helical and non-monotonic, i.e. **signal-like on both variables.** They give
  essentially no rejection against the dominant PU class.
- Only dE/dx and timing act on it:
  - dE/dx needs signal βγ ≲ 1. The median IT βγ is 1.8 at E200 against 0.9-1.0 at E500 (`r1c_signal_handles.json`), so it
    is weak at low mass. The truncated mean of a signal candidate is diluted by in-band PU hits at the normalised density.
  - SR-T: the median quirk delay is 3.1 ns at E200, where 2.8 % of in-time PU BTL hits are > 2 ns.
- §2.4 ("the working point will sit deep in the F1 part of the ladder: free-origin helix, opening linearity, dE/dx, and the
  SR-T time factor") and §0 imply all four act on PU. They do not.

**No stated fallback.** §2.5 item 6 offers "ask the user (more statistics, one pre-declared F1 step (undefined), or a result
with B > 0.3)". But §0, §5, §6.2 and §11 still present ε(m, Λ), detector-level edges and yields at a B ≤ 0.3 WP as the
deliverable, costed at 330 CPU-h.

**My order-of-magnitude reading** (ESTIMATE, for the plan to restate in its own words):
- F0 counting + χ² at the normalised density is ~10⁻¹ per event.
- A width rung (B-1) can plausibly give several decades at Λ ≳ 2 keV.
- dE/dx (heavy masses) and SR-T (heavy masses, late hits) give 1-3 decades each, with E200 and the low-Λ edge the weakest.
- 3 × 10⁻⁹ is therefore plausible for heavy masses at Λ ≳ 2 keV. It is implausible near the 0.45-1 keV edge and at E200,
  and the extrapolation must also close there.

**Required fix:** add a short "Feasibility and fallback" paragraph (§2.5 or §11) that:
1. maps each ladder variable to the background class it acts on (combinatorial PU; k = 1 PU/SM topologies; NI);
2. states plainly that a B₈₄ ≤ 0.3 WP may exist only over part of the (m, Λ) plane, and that the low-Λ detector-level edge
   may be set by background, not by the finder;
3. defines the **fallback deliverable** before production. For example:
   - (i) ε(m, Λ) and B₈₄ at a fixed set of pre-declared rungs (not only r\*);
   - (ii) a Stage-5 limit with non-zero, log-normally uncertain B in the regions without a background-free WP (it remains
     meaningful wherever S ≫ B₈₄);
   - (iii) the truth/Fatras-density result kept only as a labelled optimistic bound;
4. names which Stage-4 outputs (P2 observables, edges) survive in that case.

### B-5. The compute headline is not consistent with the measured finder speed at the density the plan adopts.

- §6.2: "At the R0 prototype speed (8 s/trial) the recommended scope would be ≈ 840 CPU-h." But the plan's baseline is now
  the TDR-normalised density, where the fix-R1 prototype measured **48 s/trial with only the OT topped up** (§2.4).
  - At that speed: 330 + 46 × 85 ≈ **4 200 CPU-h**.
  - With the IT also topped up (×2.3-3.7 hits on the seeding layers L2-L4), seed pairs scale roughly as the density product
    on L3 × L4, so it will be slower still.
- B2: the 58 CPU-h assume 16 s per ρ = 2 trial. The probe measured 400-1300 s at **Fatras** density (my re-run: 146 s and 571 s for two trials at the same
  density as the probe). B2 is defined on superpositions of *normalised* events, which have ≈ 3-5× more OT hits.
- The G3 pilot (≈ 25 CPU-h for 2 000 B1 + 500 ρ = 2 events) is affordable only after a ×25-100 speed-up, and there is no
  ρ = 2 timing gate before it.
- §6.2 does say B2 is affordable "only if G2/G3 bring the ρ = 2 trial to ≲ 20 s". But the 330 CPU-h headline (§0, §10 D4-1,
  FIX report) is presented to the user as the recommended cost without this condition.

**Required fix:**
1. In §0, §6.2 and D4-1, show the cost as a function of the finder time per trial at the *normalised* density (2 / 5 / 10 s →
   ≈ 330 / ≈ 590 / ≈ 1 010 CPU-h, plus B2 at its own measured ρ = 2 time). Replace the 8 s → 840 sentence with the measured
   48 s (OT-only) figure.
2. Add an explicit G2 sub-gate: ρ = 2 at normalised density ≤ X s/trial, with X computed from the B2 budget, before the
   G3 pilot is launched.

---

## 5. Thinning closure, duplicate explanation, WP rule, gate order (task 4)

- **Pilot numbers** reproduce from `f1r_summary.json` → `closure_rho2_to_rho1_t0`: direct/predicted = 0.35, 0.41, 0.47, 0.48
  at N_L2 ≥ 6, 7, 8, 9; thinning factors 0.053 → 0.0029; T1 z at N_L2 ≥ 8 = ln(3.53/7.46)/√(1/791 + 0.186²) ≈ −4.0 (plan
  ≈ −3.8). n_eff ≈ 151-228 of 224 trials.
- **The duplicate explanation is only partly supported.** My re-run (`r2_dupcheck.py`; same finder; greedy grouping of
  passing candidates sharing ≥ 50 % of hits) gives:

  | rung | ρ = 1 (32 trials): candidates / distinct sets | ρ = 2 (2 trials): candidates / distinct | thinning Σw reduction from de-duplication (keep max w per set) |
  |---|---|---|---|
  | N_L2 ≥ 7 | 1071 / 843 (×1.27) | 7615 / 4158 (×1.83) | ×1.76 → net ×1.38 on direct/pred |
  | N_L2 ≥ 8 | 113 / 103 (×1.10) | 1769 / 1056 (×1.68) | ×1.49 → net ×1.36 |
  | N_L2 ≥ 9 | 3 / 3 | 201 / 156 (×1.29) | ×1.25 → net ×1.25 |

  (32 ρ = 1 trials = 8 events × 4 roads; ρ = 2 = 2 superposed pairs, 1 road each, 146 s and 571 s; `r2_dupcheck_summary.json`.
  "net" = the reduction of the thinned prediction divided by the de-duplication of the direct ρ = 1 count.) Duplicates are
  real and more frequent at ρ = 2, as the fixer says. Applying the proposed per-hit-set convention at both densities moves
  direct/predicted from 0.41/0.47/0.48 to ≈ 0.57/0.64/0.60. That removes **≈ ×1.3-1.4 of the ×2.1-2.4**. A residual
  over-prediction of ≈ ×1.6-1.8 remains unexplained (2 ρ = 2 trials only, so indicative).
- **The plan's sentence "It is not the k model"** (§4.1 box) is an untested assertion; this is C-3 below.
  - Other contributors that the pilot cannot separate: T_seed acts differently at ρ = 2; the plane is not refitted after
    thinning; the union bound; the 8 ρ = 2 trials are pairs of the same 16 events used at ρ = 1.
  - T1 as pre-registered is two-sided, so a *stable conservative* bias fails it. The failure path then takes the upper
    envelope × max(1, N_obs/N_pred) = the thinning value. That is acceptable, but the plan should say explicitly that a
    conservative T1 failure leads to "use the thinning value with σ_ln covering the bias", not to "+50 % statistics twice".
- **WP rule.** B₈₄ of the MC-summed log-normal total, applied to r\* and every tighter rung, is well defined and signal-blind
  for a 1-D ladder. The remaining problem is the 2-D SR-T/SR-G issue (B-2).
  - The rule is strict: with σ_ln ≈ 2.3 (×10 spread), B₈₄ ≤ 0.3 needs a median B ≲ 0.03. Correct, but it should be said
    next to B-4's feasibility statement.
- **Gate order.** U-2 → G1 → G2 (freeze first, then F0 speed, V4-5, A1 + V4-3) → G3 (B1/B2 pilot) → guns → production is
  sound for signal-blindness: the freeze precedes the first signal efficiency. Two notes:
  1. The freeze at G2 comes **before** G3 shows which rungs the PU actually populates at the normalised density. That is the
     correct order for blindness, but it means B-1 to B-3 must be settled in the plan now, because they cannot be added
     after G3 except as the "one pre-declared F1 step", which is not defined (C-6).
  2. D4-14's "decide after V4-3 at G2" uses signal efficiency to choose whether to add a topology. Adding a category with its
     own background-only ladder is acceptable practice. State that it gets a separate frozen ladder.

---

## 6. Window, tolerance, wide regime, PROPOSED decisions, totals, IT density (task 5)

- **W_c = 75 mm.**
  - The bound is physics: for a net-neutral pair the CM moves on a straight line along n₃ through the PV, and each quirk is
    within |r|/2 ≤ ℓ_max/2 of the CM. So ℓ_max ≤ R_IT ⇒ |u·n₂| ≤ R_IT/2 = 73.25 mm (R(TBPX L4) = 146.5 mm, HANDOVER
    l.131).
  - The truth check (`f1r_truth_window.py`: wmax_IT ≤ 1.1 ℓ_max/2 in 95-100 %) uses templates only to verify. The acceptance
    table is reported, not optimised. **Not signal-tuned. OK.**
  - The margin of 75 vs 73 mm is small, and the 1.1 factor shows 0-5 % of events exceed the nominal bound. This is absorbed in
    the "acceptance ≥ f(ℓ_max ≤ R_IT)" statement.
- **t_tol = 30 µm.** Set to the S-2 event-level MS floor (23-30 µm), a physics number, with 0/100 µm variations and V4-3
  attribution. The 3σ_tot ≈ 93 µm IT band still loses the high-residual hits near the truth thickness edge (0.47-0.55 keV),
  which is the physics edge it should track. OK.
- **D4-14 (wide regime).** Correctly stated as an analysis limitation with the size shown (e.g. Ẽ500 at 0.45 keV: 0.31
  acceptance). Given B-4, the wide regime is also where background is hardest. Option (a) is reasonable.
- **D4-10 (a′).** The worked example reproduces. One ambiguity: in "max(|smoothed shift|, its sampling sd)", is the sd that
  of the smoothed shift or the raw per-point sd (C-7)?
- **D4-13.** Reasonable. It matters more after B-4: the sensitivity workspace with non-zero B *is* the natural fallback
  deliverable.
- **Totals reproduce** (recommended): A2 40.2, A3 7.1, A4 9.6, B1 70.6, B2 57.5 (+ 37.8), sum 326 ≈ 330 CPU-h. They hold
  only at 2 s/trial (B-5).
- **IT density.** The IT cluster size is uncited and tagged ESTIMATE, with a G1 search for a source. This is acceptable as a
  tag. For the record: at η ≈ 0 with 25 µm rφ pitch, 150 µm thickness and the Lorentz drift in 3.8 T, ≥ 2-3 pixels per
  cluster is plausible (ESTIMATE). That makes the nominal ×2.8 (cluster size 2) the conservative end. The occupancy
  sanity check above (≈ 3.2 GHz/cm²) supports the occupancy reading itself.

---

## 7. Category C

- **C-1. Stale road-overlap sentence.** §4.1 step 1 quotes "0 % of L3/L4 [hits in > 1 road] at W_c = 50 mm". At 75 mm the
  L3 half-width is 0.25 + asin(75/104) ≈ 1.05 rad, so roads π/2 apart overlap on L3; L4 is at the edge (0.79 rad). Update.
- **C-2. Per-event vs per-trial.** §4.1 says the per-event rate (≥ 1 of 4 roads) is primary because "data have one MET road
  per event". One road per data event makes the **per-trial** rate the physical P_fake. The ≥ 1-of-4 rate over-states it
  by up to ×4. It is conservative, but it costs efficiency under a strict B₈₄ rule. Pick one and justify it.
- **C-3. "It is not the k model"** (§4.1 box) is untested. Rephrase as "partly explained by duplicate counting (R2 test:
  ≈ ×1.3-1.4 of ×2.1-2.4); the residual ×1.6-1.8 is assigned to G3", and test it at G3 with stored hit sets.
- **C-4. NI arithmetic.** With the stated factors, 26 in-road NIs × f(≥ 2 charged prongs) × (10⁻³-10⁻²) × 0.22 ≈
  f × (6 × 10⁻³-6 × 10⁻²), i.e. ~10⁻³-10⁻² for f ≈ 0.3-0.5, not "10⁻⁴-10⁻³".
  - NIs on TBPX L2 (61.5 mm) cannot give N_IT2 ≥ 3 (prongs cross only L3 and L4), which contradicts "N_IT2 kills
    r_NI > 6 cm, **not** … TBPX L1/L2".
  - Give every factor (prong multiplicity, OT reach) and correct the range. The conclusion (F1 and the toy must carry NI)
    is unchanged, but it is ~1 decade harder.
- **C-5. T_seed stability criterion.** Fix T_seed(ρ) on the stability of the *rung that matters* (N_L2 and χ², and width if
  B-1 is adopted), not on best N_L2 only. `f1r_tseed_check.json` shows a χ² change in 2 of 4 trials.
- **C-6. "One pre-declared F1 step"** (§2.5 item 6) is not declared anywhere. Declare it, or delete it.
- **C-7. (a′) floor wording.** Say which sd is meant.
- **C-8. Signal χ² median at TDR-OT.** "≈ 2" does not reproduce from the stored top-candidate quantiles (1.0-2.1, median
  ≈ 1.4 over the 5 signal-top events). Quote what was measured and on which candidates.
- **C-9. Thinning MC.** Monte Carlo with 2 × 10⁴ subsets and a fixed seed (12345) for every candidate: estimates are
  unbiased in aggregate, but per-candidate errors are correlated across candidates of the same |S|. At the normalised
  density (|S| ≈ 40-100 incl. top-up crossings, target w ~ 10⁻⁶) importance sampling or an exact DP over layer-count
  states is better. Report the MC error in σ_ln.
- **C-10. Stub geometry.** min(n_in, n_out) counts any in-band in/out hits, not geometrically matched pairs. Requiring
  matched pairs (|Δφ| and |Δz| windows from the module geometry, without a pT window) is free and removes "A's in-hit + B's
  out-hit" coincidences. Worth a rung or a definition change before the freeze.
- **C-11. Small-sample wording.** Quote the TDR-OT margin with its uncertainty (signal 5/14 on a 1 keV-dominated mix; ratio
  68 % range ≈ ×1-8), not as "×3".

---

## 8. Tagging and internal consistency (task 6)

- Tags are used correctly in the new text:
  - VERIFIED for the probe outputs (density bench, margin, pilot, truth window);
  - ESTIMATE for the IT cluster size, NI rates, CPU targets and totals;
  - UNVERIFIED for material, trigger and K-factors.
- §2.1's μ_c re-derivation is ESTIMATE and is correctly said to be superseded by §2.4.
- Inconsistencies after the edits:
  - B-2 (SR-G "tighter rung" vs one shared rung);
  - B-5 (840 CPU-h at 8 s vs the 48 s measured at the adopted density);
  - C-1 (W_c = 50 overlap sentence);
  - C-4 (L2 NI vs N_IT2);
  - §2.4 "Δw … not a discriminant" vs the stored core width (B-1).
- §0, §6.2 and §10 agree on 330 / 365 / 160 CPU-h and ρ ∈ {2, 3 conditional}. §4.1, §5 and §6 agree on the ρ list (R1
  B-4 b resolved).

---

## Verdict

**ITERATE.** 0 Category A, 5 Category B, 11 Category C.

| # | Item | Fix |
|---|---|---|
| B-1 | The stored robust core width separates PU from signal at Λ ≳ 2 keV (PU 0/224 and 0/32 trials, signal ≥ 2 keV 30/31 and 4/6) but is excluded from the ladder; "F0 alone does not separate" is wrong | add a pre-declared width rung family (or width categories), core-hit χ²; correct §0/§2.4/§12 |
| B-2 | SR-T/SR-G make the WP rule 2-D and undefined ("tighter rung" vs one shared rung) | pre-declare the combination (offset, interleaved path or budget split) |
| B-3 | Thinning "from stored per-interaction hit counts" cannot evaluate the χ², width, F1 or timing rungs where the WP must sit | per-family method (per-subset recomputation with stored hits, or factorisation with a density-binned independence test), costed |
| B-4 | F1 helix and opening tests give ~no rejection on the measured combinatorial PU; no plain feasibility statement; no fallback deliverable | feasibility map by background class; state that a B ≤ 0.3 WP may exist only for part of (m, Λ); define the fallback deliverable |
| B-5 | The compute headline assumes 2 s/trial; the measured speed at the adopted density is 48 s (OT-only top-up; ≈ 4 200 CPU-h at that speed); no ρ = 2 timing gate before G3 | cost table vs s/trial at normalised density; ρ = 2 sub-gate |

The fixes are text and design changes. No production run or new simulation is needed; B-1 can be specified from existing
outputs.

### Assessment: is the detector-level P2 search feasible as planned?

The chain, injection and density normalisation are sound, and the fixer's blind measurement is honest. At the realistic
density, layer counting and χ² leave PU at ~10⁻¹ per event, against a requirement of 3 × 10⁻⁹. As planned, the WP rests on
F1 variables:
- two of them (the helix and opening tests) do not act on the dominant combinatorial background;
- the other two (dE/dx, timing) are weak exactly where the low-Λ edge and the light masses are.

The plan is therefore **not feasible as written for a background-free result across the whole (m, Λ) plane**. It becomes
plausibly feasible for heavy masses at Λ ≳ 2 keV once a ribbon-width rung is added (strong measured separation) and dE/dx and
timing are stacked on top. Near the 0.45-1 keV edge and at E200, the honest expectation is a result with non-negligible,
log-normally uncertain background (a limit, not a clean P2 measurement). The plan should say so now, and define that
fallback deliverable before the freeze. The finder speed at the normalised density (×25-100 from the probe) and the ρ = 2
cost are a second, independent feasibility risk that the 330 CPU-h headline hides.
