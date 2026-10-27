# G2a report: production finder speed (C001 quirks theory track, Stage 4)

Executor, 2026-10-13. PU-only work only, no signal looked at. Code: `acts/stage4/finder/` (README there).
Numbers: `data/acts_stage4/g2/` (`g2a_timing_table.json`, `timing_rho1.json`, `timing_rho2.json`,
`timing_rho2_chi2core.json`, `equivalence_rho1.json`, `g2a_campaigns.json`).

## 1. Result in one paragraph

The F0 finder now takes **t₁ = 3.76 s per trial (median of 32 PU-only trials; 68 % CI 3.73-3.88 s; mean
3.86 ± 0.12 s; p90 4.72 s)** at ρ = 1 and the adopted full density (IT + OT top-up), one process, one thread, on
the Mac M3. The fix-R2 profile measured 211 s with the merge vectorised (≈ 5 500 s as coded), so the gain is ×56.
The new finder **finds exactly the reference's candidates**. On 24 PU-only trials the seed sets are identical
(4 282 126 seeds), and so are the 2 514 806 candidate hit sets, their rank order, all integer variables and every
per-rung count and pass flag. Floats agree to ≤ 2·10⁻⁸ relative. **No selection rule was changed.** At ρ = 2 the
finder itself takes **t₂ = 27.0 s (median of 10 trials; mean 26.4 ± 1.2 s)**. The in-job ρ = 2 weights would cost
more than the finder unless they are sub-sampled (§5). That is a G2b question.

## 2. What changed (implementation only)

The selection is still the f1r one: road, (L4, L3) seeds with an L2 confirmation hit and seed N_L2 ≥ T_seed = 6,
PV-constrained 3-iteration refit of every kept seed, (N_L2, χ²/ndf) ranking, and the 2-mrad merge. What changed
is how the hits are visited:
- a per-trial (φ-bin × z-cell) index per barrel surface. For each bin the band |n·u| < tol of a plane through the
  PV maps to an exact z interval, so each query visits a proven superset of the hits that can pass, and every
  visited hit gets the reference's own test;
- the seed score visits only the two φ lobes allowed by the window. It stops counting a layer at 2 crossings and
  stops scoring as soon as pass/fail is decided;
- the refit gathers the hits once per seed, for every plane within δ of the seed normal (proven bound). The
  bound is checked at each iteration, with an exact re-gather if it fails. Selection is branch-free and the
  eigenvector comes from inverse iteration (LAPACK fallback);
- the merge uses a hash grid with the same greedy order and the same criterion;
- the stored variables are computed in numba, including the plan's N_IP2, N_2S2, w_core and χ²_core.

Measured stage means (32 trials): seeds 1.28 s, refit 2.21 s, merge 0.05 s, variables 0.26 s, index 0.03 s.

**Environment.** The finder runs in the theory_track pixi env, which already ships numba 0.68. That is where the
reference probe and plan §1.8 put the finder. **No package was installed, and the acts env is untouched.** The
permission to add numba to the acts env was not needed. If the production chain wants finder and chain in one
process in the acts env, `pixi add numba` there would be the only change. Not done.

## 3. Differences from the reference (all outputs; none in the selection)

1. In 0.10 % of candidates the kept member of a 2-mrad duplicate group is a different seed. These members tie in
   (N_L2, χ²/ndf) to the last bits, and the summation order differs. The hit set, rank and rung variables are
   identical. The normal differs inside the 2-mrad merge tolerance. The stored seed N_L2, a property of the seed,
   differs for 456 of 2.5·10⁶ candidates.
2. Seed N_L2 is stored as a lower bound (≥ 6) by default because of the early termination. The exact value is
   available on request (`seed_n2_exact`, costs 0.5-2 s per trial). It is a diagnostic only.
3. Production output `store='loose'` keeps only candidates passing the loosest rung (N_IT2 ≥ 3 and N_IP2 ≥ 4). No
   other candidate can pass any rung. The merge still runs over all candidates.
4. New stored variables: N_IP2, N_2S2, χ²_core, n_core and |Δφ(axis, MET)|. They follow plan §2.2 item 5 and use
   the final refit axis, like f1r's `dw_core`.
5. Float-level effects (summation order, squared band tests, eigen-solver) could flip a hit sitting exactly on a
   band edge. None was seen.

## 4. Timing (PU-only, full density; `g2a_timing_table.json`)

| quantity | value |
|---|---|
| t₁, ρ = 1, 1 process (32 trials) | median **3.76 s** [3.73, 3.88], mean 3.86 ± 0.12, p90 4.72, range 2.6-5.2 |
| t₁ with 4 processes running in parallel (same 32 trials) | median 4.21 s, i.e. ×1.12 per trial (×1.06-1.15) |
| t₂, ρ = 2 finder only (10 superposed trials) | median **27.0 s** [26.2, 27.9], mean 26.4 ± 1.2, p90 29.6 (t₂/t₁ = 6.9) |
| peak memory per process | 0.38 GB (ρ = 1), 1.35 GB (ρ = 2) |
| job start (numba compile with a cold cache) | ≈ 11 s once per job, not per trial |
| candidates per ρ = 1 trial (medians) | 1.76·10⁵ refits → 1.04·10⁵ after the merge; 8.0·10⁴ pass the loosest rung; 589 have N_IP2 ≥ 7 |

## 5. ρ = 2 in-job weights (G2b input; timing only)

Mean per ρ = 2 trial: 3.06·10⁵ sets pass the loosest rung, 1.36·10⁵ have N_IP2 ≥ 6 and 3.5·10⁴ have N_IP2 ≥ 7.
- **Counting-rung weights.** The existing f1r method (2·10⁴-subset Monte Carlo, 21.5 ms per set) would take
  ≈ 6 600 s per trial for every set. It is not usable. G2b needs the plan's fast method (DP or importance
  sampling, ≲ 1 ms per set, an ESTIMATE) plus the pre-declared sub-sampling strata (f_lo, f_hi).
- **Per-subset χ²_core** (plan §4.1 step 3b). A new numba kernel (`kernels.chi2core_subsets`, 10³ subsets per set)
  takes 2.6 ms per set. For every N_IP2 ≥ 7 set that is ≈ 91 s per trial, ×3.4 the finder; with f_hi = 0.1 it is
  ≈ 9 s. Its medians agree with an independent numpy version of the same definition.

## 6. Implications for the campaigns (plan §6.2 formula, `g2a_campaigns.json`)

These use `f3r_campaigns.blocks` unchanged: PU event without the finder 4.7 s (ESTIMATE, G1 measures it), the
measured mean t₁ = 3.86 s, and Mac capacity at 7 workers (168 CPU-h per day). The wall time at 5.5 effective
workers is shown because 4 parallel processes already cost ×1.12 per trial and 7 workers on 4P+4E cores are
unmeasured.

| t₂ assumption | C1 CPU-h (Mac h at 7 / 5.5) | C2 | C3 | C4 | C1-C4 CPU-h (Mac h at 7 / 5.5) |
|---|---|---|---|---|---|
| (a) finder only, 26.4 s | 96 (13.7 / 17.4) | 124 (17.7) | 84 (12.0) | 120 (17.1) | 423 (60 / 77) |
| (c) finder + strata weights, ≈ 51 s (ESTIMATE: f_hi = 0.1, f_lo = 0.01, counting weights at 1 ms per set) | 109 (15.6 / 19.9) | 151 (21.6) | 112 (15.9) | 120 (17.1) | 491 (70 / 89) |
| (b) finder + χ²_core on every N_IP2 ≥ 7 set, 118 s (counting weights excluded) | 146 (20.9 / 26.6) | 225 (32.2, > 1 day) | 186 (26.5, > 1 day) | 120 (17.1) | 677 (97 / 123) |
| (d) plan convention t₂ = 8 t₁ | 98 (14.0) | 129 (18.4) | 89 (12.7) | 120 (17.1) | 436 (62 / 79) |

- At this t₁ every campaign fits one Mac day under (a), (c) and (d).
- G2b criterion for C1 on the Mac at t₁ = 3.86 s: **t₂,max = 156 s**. The finder alone (26 s) passes. Including
  the weights it passes only with sub-sampling or faster per-set methods, as in (c).
- Against the Saturday deadline (≈ 4 days of Mac time in total):
  - C1 alone costs ≈ 14-20 h;
  - C1 + C2 costs ≈ 31-41 h;
  - the full C1-C4 costs ≈ 2.5-3.7 days.
  The full scope would leave essentially no time for G1/G3, the analysis and Stage 5.

## 7. Decisions for the user

1. **Scope (G2a always asks; D4-16).** The options, with walls from §6:
   - C1 only, ≈ 14-20 h;
   - C1 then C2;
   - the full C1-C4, ≈ 2.5-3.7 Mac days;
   - more optimisation first. A further ×1.2-1.3 looks possible with more work, but no ×2 without changing the
     selection: raising T_seed from 6 to 7 loses ≈ 8 % of the reference candidates at N_IP2 ≥ 7 on a probe trial,
     so it is not proposed.

   Given the deadline, the executor's reading is C1 first, then decide on C2.
2. **ρ = 2 weights (G2b).** The counting-rung MC must be replaced (DP or importance sampling) and the strata
   f_lo / f_hi fixed from this PU-only timing. Otherwise B2 dominates the cost (§5).
3. **Output volume.** ≈ 8·10⁴ loose-rung candidates per ρ = 1 trial is ≈ 5 MB of variables per trial without hit
   lists, ≈ 0.4 TB over the 8·10⁴ B1 trials of C1-C3. A storage policy is needed before production, for example:
   - per-rung counts and pass flags for every trial;
   - full records for N_IP2 ≥ 6 (≈ 8·10³ per trial) or N_IP2 ≥ 7 (≈ 600 per trial);
   - hit lists as plan §4.1 already prescribes for ρ = 2.

   This is a definition question for the plan, not a finder change.
4. Optional: keep `data/acts_stage4/g2/ref/` (524 MB of reference dumps) for re-checking later finder changes, or
   delete it.

## 8. Compute used (≤ 8 CPU-h allowed)

≈ 3.5 CPU-h in total, at most 4 parallel processes, all with nice:
- 24 reference trials (f1r logic): 2.16 CPU-h;
- development and profiling: ≈ 0.8 CPU-h;
- final timing and equivalence: ≈ 0.4 CPU-h;
- ρ = 2 trials: ≈ 0.15 CPU-h of the 1 CPU-h cap (10 timing trials, 3 χ²_core trials, 1 probe).
