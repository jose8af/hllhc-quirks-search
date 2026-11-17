# Phase 2 — executor Flora — T1 builder in v1 mode and check T1-b — plan and session log

Started 2026-11-17 08:14 -05 (`date`). Plan written 08:21–08:22 (`date`), **before any job, any toy and any code run**.
`AN` = `analyses/quirks_v2`, `STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`, `P2` = `AN/phase2_exploration`.
Tags: [V] VERIFIED (file:line or campaign), [E] ESTIMATE, [U] UNVERIFIED.

Read in full before planning: PHASE2_BRIEF, AGENT_RULES, CLAUDE.md overrides, agents/executor.md, ledger/README, runner
(`tools/runner/bin/*`, `qv2run/{cli,campaign,paths}.py`, greps of `wrapper.py`, `ssh.py`, `nodes.py`), STR §4.11
(l.1545–1787) and §0 l.183–200, COM rows T1-a…T1-i (COMMITMENTS.md l.208–216, l.316), Tatiana's log (all) and
EXPLORATION file (all), `src/p2c_t1.py`, Viktor's TOY_COST file and `src/p2v_toys.py`, `p2v_campaigns.py`,
`acts/stage4/analysis/stats.py`, v1's `limits.json` entry of the best point, `outputs/c1b_arith.json` (keys, best-point
rows, `T1_input_schema`), `src/v2arith/__init__.py`, LOG.md entries of 16 Nov 22:47, 22:55 and 17 Nov 08:14, SLOTS.md.

## 1. Inputs (v1's public record; no v2 signal quantity is formed, no v2 signal sample is opened)
[V: `stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1/limits.json` → `points["A2|F|200|1.5|BM"]`]
- efficiencies s = (0, 0.045) (SR-T, SR-G); N_exp per unit μ = 15,775 events (STR l.192, l.1729) → S = (0, 709.875);
- background medians b = (451,026.88, 591,129.31); log widths σ_ln = (1.74809, 2.70891), one log-normal per
  category, no shared nuisance ("log-normal bounds, uncorrelated categories", STR l.1727–1728);
- v1 hybrid-toy limit 12,458,208.17 events = **μ₉₅ = 789.744**; v1 asymptotic 13,072,848.6 events = 828.707.
- Window of T1-b: 789.744 × [0.9, 1.1] = **[710.769, 868.718]** (STR l.1727–1730: "within 10 %", comparison on μ₉₅).
- b_G/S_G = 832.723: the value of μ at which μ·S_G equals the median background of SR-G.

## 2. Task A — the procedure, fixed in advance

Rulings that bind (LOG.md 16 Nov; Tatiana's log 13:47): T1-b is read literally; "v1 mode" = v1's background treatment
with the T1 procedure's own statistic; v1's number-count statistic is a diagnostic with no verdict.

### 2.1 What the strategy fixes (taken as written)
| element | value | STR line |
|---|---|---|
| model | n_c ~ Pois(μ S_c + B_c·e^{σ_c θ_c}), c ∈ {T, G}; in v1 mode no counted λ, one log-normal factor per category | l.1550–1557, l.1727–1728 |
| generation (hybrid) | every constrained nuisance drawn from its constraint density (θ_c ~ N(0, 1), no censoring bound in v1 mode); n_T, n_G Poisson at those values and at the tested μ (0 for the b-only ensemble); auxiliary observations fixed (here: the Gaussian auxiliary data stay at 0) | l.1626–1629 |
| statistic | q̃_μ from two pyhf fits of the workspace | l.1629–1631 |
| CLs | p_(s+b)/(1 − p_b) from the two ensembles | l.1631 |
| expected limit | median over the background-only ensemble | l.1631–1632 |
| what is pyhf's | likelihood, fits, test statistic; only the generation point is outside pyhf | l.1632–1634 |
| asymptotic | Asimov data at the nominal (no counted rate here: n = b, auxiliary 0) | l.1636–1638 |
| μ grid | μ_a × {0.4, 0.55, 0.75, 1, 1.35, 1.8, 2.5, 3.5}, μ_a = the asymptotic limit, computed first | l.1639–1641 |
| interpolation | ln CLs linear in μ between the two grid values that bracket ln 0.05 | l.1641–1642 |
| no bracket | grid extended by factors 1.5 on that side | l.1642–1643 |
| toys | 1000 s+b and 1000 b at each μ | l.1708–1709 |
| pyhf | 0.7.6 with numpy 2.2 | l.1723 |
| criterion | reproduces 789.7 within 10 % | l.1727–1730 |

### 2.2 What the strategy leaves open, and my choice (each chosen once, now)
1. **Implementation of the fits** (STR silent). pyhf 0.7.6, jax backend (float64), `scipy_optimizer()` (SLSQP,
   autodiff gradient, default tolerance), merged channel layout (one channel, two bins), fixed-μ fit with
   `do_stitch=True` (Viktor §5). **Not** Viktor's warm start from the previous toy: in this workspace consecutive
   toys differ by e^{2.7θ} in the counts, so the previous optimum is not a near start. Start values instead from
   closed forms of the data of the toy (Tatiana's hand-over plan, her log l.242–244):
   θ_T⁰ = ln(n_T/b_T)/σ_T; fixed-μ fit: θ_G⁰ = ln(max(n_G − μS_G, 0.5)/b_G)/σ_G; free fit: if n_G ≥ b_G then
   μ⁰ = (n_G − b_G)/S_G, θ_G⁰ = 0, else μ⁰ = 0, θ_G⁰ = ln(max(n_G, 0.5)/b_G)/σ_G; all θ⁰ clipped to ±4.9. pyhf
   bounds: θ ∈ [−5, 5] (pyhf default), μ ∈ [0, 10⁵] (as Tatiana's builder). q̃ = pyhf's own formula on the two
   fitted values (clip at 0; 0 if μ̂ > μ), as in `p2v_toys.q_direct`.
2. **Failed fits** (rule fixed by the orchestrator's ruling of 16 Nov 13:47, kept): a pseudo-experiment whose fits
   raise is retried once with the nuisances started at their generated values; if it fails again it is dropped from
   its ensemble (numerator and denominator). **Maximum tolerated fraction: 2 % dropped per ensemble at a μ point**;
   above it the point is NOT RESOLVED and is not used for the crossing. Added by me (quality control, stated now): a
   fit that pyhf reports as converged but whose q̃ differs from an independent exact evaluation by more than
   max(10⁻³, 10⁻⁴·q̃) counts as failed (same retry, same drop, same 2 %). The exact evaluation: each category has
   one nuisance, so each profile is a one-dimensional bounded minimisation (grid + bisection on the derivative),
   evaluated in pyhf's normalisation of the likelihood; it is checked against pyhf's `twice_nll` at start. The
   verdict statistic is pyhf's; the exact value only accepts or rejects a fit. The result is also reported with
   exceptions only (no accuracy rule) and with the exact q̃ on all toys, as diagnostics.
3. **Ties** (Viktor §4): "q ≥ q_obs" is evaluated as q ≥ q_obs − 10⁻⁵, in both ensembles.
4. **q_obs of the median**: `numpy.median` of the b-only q̃ values (mean of the two central order statistics for an
   even count; the convention of pyhf's own toy calculator, which interpolates percentiles linearly). The two
   central order statistics taken separately are reported as a sensitivity.
5. **μ_a**: root of CLs_asym(μ) = 0.05 with CLs_asym = 2·(1 − Φ(√q̃_A)) (median expected, the formula of pyhf's
   asymptotic calculator and of v1 `stats.py` l.193–197), q̃_A from the same two pyhf fits on the Asimov data,
   brentq to 10⁻³ in μ. Computed **once** in the set-up job and passed to every toy job, so that all replicas use the
   same grid. (Tatiana's 828.67 was a linear interpolation on a 4-unit grid; it is reproduced the same way as the
   set-up check and the root is reported beside it.)
6. **A grid point with zero s+b toys beyond q_obs** (ln 0 is undefined; STR silent). Kept literal: the eight-point
   grid and the ln interpolation are not changed. The count 0 of N is replaced, for the interpolation only, by
   1.139 (the 68 % upper value of a zero count, the study's own zero-count central value, STR l.1615), i.e.
   p_(s+b) = 1.139/N, and the point is flagged. Sensitivity reported with 0.5/N and 1/N, with linear interpolation
   of CLs, and with a bisection refinement of the bracket (six extra μ values, 1000 + 1000 toys each): all three
   "diagnostic, no verdict".
7. **Which pair brackets** if CLs is not monotone on the grid: the first pair, from low μ, with
   CLs_i > 0.05 ≥ CLs_{i+1}, among resolved points. If the first point is ≤ 0.05 or the last > 0.05: extension by
   1.5 on that side (STR l.1642), at most four times.
8. **Random numbers**: `numpy.random.default_rng([seed, round(1000 μ), e])`, e = 0 (b-only), 1 (s+b); per
   ensemble θ = standard_normal((N, 2)) in the order (T, G), then n = poisson(λ). Independent ensembles at each μ
   (STR l.1634–1635: "computed once per (selection, point, μ)").
9. **Seed list** (10 replicas of the complete frozen procedure, 8 μ × (1000 + 1000) each):
   2026111701, 2026111702, …, 2026111710, in this order. Smoke jobs (code paths only, ≤ 50 toys, no CLs read from
   them) use seeds 999001… and are not part of any result.

### 2.3 Reading of PASS / FAIL / NOT RESOLVED (fixed now)
- **The T1-b number** is μ₉₅ of **replica 1** (seed 2026111701): one run of the procedure exactly as frozen. If
  replica 1 is not resolved by rule 2, the first resolved replica in seed order takes its place; if fewer than 8
  of the 10 replicas are resolved the verdict is NOT RESOLVED (numerics) and nothing further is read.
- **Its toy error** σ_toy = the larger of (i) the standard deviation (ddof = 1) of μ₉₅ over the resolved
  replicas, and (ii) the binomial errors of CLs at the two bracketing points propagated through the interpolation
  (Tatiana's definition, her log 13:47). (i) is the measured scatter of the frozen procedure; it contains what (ii)
  cannot see (on which side of a jump of q̃ the b-only median falls).
- **PASS** if [μ₉₅ − σ_toy, μ₉₅ + σ_toy] lies inside [710.769, 868.718]; **FAIL** if it lies entirely outside;
  otherwise the interval **straddles** a boundary.
- **If it straddles:** one escalation, defined now, no further toys: the ten replicas are pooled (10,000 + 10,000
  per μ; same grid), μ₉₅ recomputed by the same rules, error = bootstrap standard deviation (500 resamples of the
  toys of each ensemble). Same reading. If the pooled interval still straddles, the verdict is **NOT RESOLVED:
  the frozen procedure does not determine μ₉₅ to better than the 10 % window at this point**; the number of
  replicas inside and outside the window is reported, and the finding is written in the "Phase 1 assumed / Phase 2
  found / Implications" form with a proposed rewording (not applied).
- The criterion is not redefined in any branch. Every diagnostic below carries "no verdict".

### 2.4 What I expect, from the algebra alone (written before any toy; it did not drive the choices above)
In v1 mode the SR-T bin has no signal and cancels in q̃. In SR-G a b-only toy has n = b·e^{σθ}. If n < μS the
fixed-μ fit cannot absorb the deficit (q̃ of order 10³–10⁴, the "jump" Tatiana saw); the fraction of such toys is
p_jump(μ) = Φ(ln(μS/b)/σ) = 0.367, 0.412, 0.457, 0.4993 at μ_a × {0.4, 0.55, 0.75, 1} and 0.543 at 1.35 μ_a [E:
closed form, python stdlib, 08:21]. With the median below the jump, CLs(μ) = 2Φ(ln(1 − μS/b)/σ) = 0.85, 0.77, 0.61,
0.049 at the first four grid points (the toy and asymptotic curves coincide); above 832.7 every b-only median is on
the jump and no s+b toy reaches it (it would need a Poisson deficit of tens of σ), so CLs = 0 exactly. Consequences
I expect: (a) at μ_a the b-only median falls on the jump in about 47 % of 1000-toy ensembles; then CLs(μ_a) = 0 and
the interpolation runs from 0.75 μ_a with the zero-count rule (μ₉₅ ≈ 700, ratio ≈ 0.89, outside the window);
otherwise μ₉₅ ≈ 827–835 (ratio ≈ 1.05, inside). (b) The replicas would then be bimodal with a scatter of about
65, the interval of 2.3 would straddle, and pooling does not help because μ_a sits by construction at the edge
(p_jump = 0.4993 needs > 10⁶ toys to resolve). So **NOT RESOLVED is the outcome I expect**, with the diagnostics
(refined bracket, exact-q̃ large ensemble) near 828. If the toys show something else, that is the result.
The alternatives of 2.2 item 6 would change this (linear CLs ≈ 812, refinement ≈ 828: both inside); they were not
chosen as primary because they change the frozen grid or interpolation, which the ruling forbids; they are the
material for the rewording proposal.

## 3. Task B — campaigns (schrodinger only, ONE job at a time, `--max-per-node 1`, pgrep ≤ 2 before each launch)
Code: `P2/src/p2f_t1.py` (builder + modes), `P2/src/p2f_campaigns.py` (campaign files →
`tools/runner/examples/p2f/`). Outputs `data/p2c/<campaign>/000/*.json`; markers `ledger/markers/<campaign>/`.
Environments: jax = `schrodinger:/home/scratch/jdochoa/envs/pyhf_toys` (Viktor; lock in `tools/install/pyhf_toys/`);
numpy backend check = `phase1_strategy/src/pyhf_bench` (existing). No install.

| campaign | jobs | content | CPU [E] |
|---|---|---|---|
| `p2-c-t1f-smoke<N>` | 1–4 | every code path on ≤ 50 toys, seeds 999001…; repeated under new names until clean | < 0.1 h |
| `p2-c-t1f-setup` | 3 | (1) `setup`: schema validation (T1-a) of both layouts, generation and likelihood-normalisation checks against pyhf, asymptotic scan 780–900 in steps of 4 (**check 1: 828.67**), μ_a root, pyhf `hypotest` cross-check; (2) `vcheck`: Viktor's `p2v_toys.py` unchanged in his best configuration at 31 parameters, μ = 5, 1000 + 1000, tie-tolerant CLs (**check 2a: 0.1372**); (3) `pair`: v1 workspace at μ = 0.75 μ_a, 300 + 300 identical pseudo-experiments on the jax and numpy backends, paired q̃ and CLs (**check 2b**) | 0.1 h |
| `p2-c-t1f-prod` | 10 | one job per seed: the frozen procedure (8 μ, extensions if needed) + the six-step refinement diagnostic; all q̃ stored | 10 × ≈ 5–10 min ≈ 1–1.7 h |
| `p2-c-t1f-diag` | 2 | `v1stat`: v1's number-count statistic, v1's exact random-number order, 5000 toys, v1's seed + 11 others (and Tatiana's four numbers reproduced in her order); `ref`: exact q̃ of the T1 statistic on 2×10⁵ + 2×10⁵ toys at 17 μ values (the large-ensemble CLs curve) | 0.3 h |
| `p2-c-t1f-sum` | 1 | verdict assembly from the stored q̃ (rules of §2), variants, pooled bootstrap, timing | < 0.05 h |
Total ≈ 2–2.5 CPU-h [E] against ≈ 6 allowed. Stop and report if the projection exceeds 6.
Set-up checks pass if: check 1 |μ − 828.67| ≤ 0.05; check 2a CLs = 0.1372 ± 0.0005 (same seed and configuration:
expected identical); check 2b max |Δq̃| ≤ max(10⁻³, 10⁻⁴ q̃) on paired toys and the same CLs within one toy count.

## 4. Tasks C–E
C: verdict by §2.3 with σ_toy and the dropped fractions; diagnostics (no verdict): v1 statistic over 12 seeds (mean,
sd), v1 asymptotic against mine, variants of §2.2; finding and rewording proposal if not PASS. D: T1-a schema
validation in the set-up job, workspace JSON written to `P2/outputs/`; builder documented in `p2f_t1.py` (inputs,
`v1_mode` switch, tie tolerance, backend, where `v2arith` enters). E: `P2/outputs/T1B_RESULT_flora_<stamp>.md` (≤ 3
pages), `experiment_log.md` entry, two lines in `DAILY_NOTES.md` per report, SLOTS.md lines.

## 5. Log
- 2026-11-17 08:14 start; reading. 08:16 schrodinger: load 4.4, graphical login screen (cap 3), my-user runner jobs 2
  (the pilot lanes); Albert holds the third slot ≈ 08:14–08:35 (SLOTS.md) → nothing launched before his release.
  Toy env present (`/home/scratch/jdochoa/envs/pyhf_toys/INSTALLED`). No numpy in einstein's system python: every
  numerical step, including the summary, runs as a runner job on schrodinger.
- 2026-11-17 08:22 plan written (this file, §1–§4). Nothing has run.
- 2026-11-17 08:27 code written: `src/p2f_t1.py` (builder with the v1-mode switch, exact one-dimensional profile,
  modes setup / pt / pair / vcheck / t1b / v1stat / ref / summary), `src/p2f_campaigns.py`. pyhf 0.7.6 source read
  (`optimize/opt_jax.py`): the fixed POI value is a traced argument of the jitted objective, so a new μ does not
  recompile. 08:27 pgrep on schrodinger 3 (Albert's test in the third slot) → waited; ≤ 2 on four checks 08:29–08:31.
- 2026-11-17 08:31 SLOTS.md line appended; launched `p2-c-t1f-smoke1` (1 job, every code path, ≤ 30 toys, seeds
  999001/2; no result is read from it). pgrep before: 2.
- 2026-11-17 08:31 first launch refused by the driver ("no capacity": load 4.70 during Albert's burst); relaunched
  08:35 (pgrep 2, load 2.2). `p2-c-t1f-smoke1` done 08:35 (27 CPU-s): every mode runs; nothing read from it.
- 2026-11-17 08:37 **`p2-c-t1f-setup` done (3 jobs, 55 CPU-s)** [V: data/p2c/p2-c-t1f-setup/000/]:
  - **Check 1 PASS:** asymptotic scan 780–900 step 4 with Tatiana's interpolation 828.6672 (hers 828.6677; v1 828.7067).
    Root of CLs_asym = 0.05 from the pyhf fits: **μ_a = 828.7069**; exact one-dimensional profile 828.7068; v1's own
    asymptotic 828.7067 (agreement 2×10⁻⁴). With v2arith's medians and widths: 828.662. T1-a: both layouts
    schema-valid; expected counts agree with pyhf to 3×10⁻¹⁶, twice-NLL to 2×10⁻⁸ (relative).
    Side finding: pyhf's own `hypotest` (asymptotic, default start values) returns CLs = 0.0 at μ = 780, 820, 828
    without raising (true values 0.31, 0.12, 0.057): the default-start fit stops at a wrong point. Start values
    matter in this workspace even for the asymptotic number.
  - **Check 2a PASS:** Viktor's script unchanged, best configuration, 31 parameters, μ = 5, 1000 + 1000: CLs 0.13718
    tie-tolerant (raw 0.132), his 0.1372; 34.1 s per unit (his 30.5).
  - **Check 2b FAIL by my criterion:** v1 workspace, μ = 621.5, 300 + 300 identical toys: on the 298 toys kept by both
    backends max |Δq̃| = 1.2×10⁻⁵ (s+b) and 1.06 on values of 10⁴ (b), none beyond tolerance; but 4 toys per backend
    were first fitted **above the exact minimum** (q̃ − exact = 0.07, 0.10, 3.5, 3.8; identical in jax and numpy to
    10⁻⁷), the jax retry recovered 3 and dropped 1, the numpy retry recovered none (4 dropped), so the counts differ
    (k_sb 110/300 vs 114/298; CLs 0.731 vs 0.765). Cause (reasoned, to be tested): SLSQP's default tolerance 10⁻⁶ on
    the change of the objective, with curvatures of 10⁶ (SR-T nuisance) beside 1–40: the first line search is cut to a
    step of 10⁻⁶ and the improvement falls below the tolerance, so SLSQP reports success after one iteration.
    The accuracy rule of plan §2.2 item 2 caught it; without it these toys would have entered with wrong q̃.
  - **Change to plan §2.2 item 1, made before any production toy and because check 2b failed:** the SLSQP tolerance
    is tightened (Viktor's accuracy-reference setting `tol = 1e-10`), optionally with one Newton step on the SR-T
    start value. Variants a (`tol=1e-10`), b (`tol=1e-10,newton_t=1`), c (`tol=1e-12,newton_t=1`) are run on the same
    300 + 300 toys at μ = 621.5 (both backends) and on 300 + 300 at μ_a and 1.35 μ_a (jax), campaign
    `p2-c-t1f-setup2` (seed 2026111700, not a production seed; no limit is read from it). Selection rule, fixed now:
    the variant with the fewest first-attempt failures (exception or inaccurate) summed over the three μ; ties → the
    smaller change (a before b before c). Nothing else of §2 changes.
- Timing seen so far [V]: ≈ 9–12 s per 1000 + 1000 on the v1 workspace (3 parameters), numpy and jax alike.
- 2026-11-17 08:41 **`p2-c-t1f-setup2` done (3 jobs, 93 CPU-s)** [V: data/p2c/p2-c-t1f-setup2/000/]. Fit-quality
  counters only were read (no limit). jax, 300 + 300 toys at each of μ = 621.5, 828.7069, 1118.754:
  variant a (`tol=1e-10`): **0 first-attempt failures in 1,800 toys (3,600 fits)**, max |q̃ − exact| = 1.5×10⁻⁷;
  variant b: 1 inaccurate first attempt (recovered); variant c: 0. **Selected by the rule fixed at 08:38: variant a**
  (`tol=1e-10`, start values as in plan §2.2 item 1). 12.9–13.2 s per 1000 + 1000 (11.5 with the Newton start).
  Check 2b repeated with variant a: paired q̃ agree (max |Δq̃| 2.4×10⁻⁶ on s+b, 1.8×10⁻⁴ on b-only values of 10⁴; none
  beyond tolerance), but the **numpy backend** (finite-difference gradient) raises in 5 of 600 toys at this
  tolerance and drops 2 after the retry, so k_sb is 108/300 (jax) against 106/298 (numpy), k_b 150/150: the "within
  one toy count" clause of my criterion is **not met (2 counts)**; the q̃ clause is met. Reading: the jax
  configuration is validated against the exact profile on every toy (stronger than the comparison with numpy) and
  by check 2a; the numpy backend is not usable for T1 toys at this tolerance (0.3–0.8 % failed fits, 31 s per unit).
  The set-up requirement of the task (828.67 and Viktor's CLs, "or an equivalent check") is met by checks 1 and 2a.
- 2026-11-17 08:42 production defined: `p2-c-t1f-prod`, μ_a = 828.7069115492852, conf `tol=1e-10`, seeds as §2.2.
- 2026-11-17 08:42 launched `p2-c-t1f-prod` (10 jobs, one at a time; pgrep before: 2). First job started 08:42.
  **No output of the production has been read by me** (not even the job log): the interim report goes to the
  orchestrator first, so that the plan can be reviewed before any toy result is looked at. `outputs/
  t1_v1mode_workspace_flora.json` = copy of the schema-valid v1-mode workspace (sha256 ef09b0ee…, T1-a).
  CPU so far [V: markers of p2-c-t1f-smoke1, -setup, -setup2]: 175 CPU-s.

## State for a successor (written 2026-11-17 08:43)
- **Plan and rules:** §2 of this file (fixed 08:22, before anything ran) + the one logged change (SLSQP `tol=1e-10`,
  entries 08:37–08:42). Nothing else may change before the verdict is read.
- **Running:** `p2-c-t1f-prod` on schrodinger (driver detached there, log
  `schrodinger:/home/scratch/jdochoa/drivers/p2-c-t1f-prod.ssh.log`), 10 jobs × a few minutes, one at a time.
  Status: `R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; ssh -x schrodinger "$R/bin/qv2run status $R/examples/p2f/p2-c-t1f-prod.json -v"`.
- **Next, in this order** (pgrep ≤ 2 before each launch; `--nodes schrodinger --max-per-node 1 --on schrodinger`):
  1. `p2-c-t1f-diag` (file written): v1 statistic over 12 seeds, exact-q̃ large ensemble.
  2. `python3 -I src/p2f_campaigns.py sum 828.7069115492852` → `p2-c-t1f-sum` → `data/p2c/p2-c-t1f-sum/000/
     p2-c-t1f-sum-verdict.json`: key `verdict` is the T1-b reading by §2.3; `primary`, `replicas`, `variant_stats`
     (diagnostics, no verdict), `pooled`, `fits`, `timing`.
  3. Write `outputs/T1B_RESULT_flora_<stamp>.md`, experiment_log entry, DAILY_NOTES, SLOTS release line.
- **Files:** code `src/p2f_t1.py`, `src/p2f_campaigns.py`; campaign files `tools/runner/examples/p2f/`; outputs
  `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/p2-c-t1f-*/000/`; job logs `/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/…`.
- **Traps:** einstein's python has no numpy (every numerical step is a runner job); the driver refuses to start when
  the node's 1-minute load is high ("no capacity"): relaunch the same campaign; done/failed jobs are never rerun
  (new campaign name or job id); pyhf's default-start fits are wrong in this workspace without raising (use
  `Fitter` with the closed-form starts and `tol=1e-10`); the numpy backend fails 0.3–0.8 % of fits at that tolerance.
- 2026-11-17 09:09 `p2-c-t1f-prod` finished (10 jobs, 1,595 CPU-s, 0 failed). Orchestrator accepted the plan as
  committed before any read; first read of production outputs 09:33 through `p2-c-t1f-post` (verdict, v1stat, ref,
  hypo; replaces the planned `-diag` and `-sum`, whose files were written but never launched).
- 2026-11-17 09:33 **T1-b: FAIL as frozen.** Replica 1: 937.6 ± 113.8 (ratio 1.187) straddles 868.72 → pooled
  escalation 902.0 ± 31.9 (ratio 1.142), interval [870.2, 933.9] outside the window (margin 1.5). Replicas: 937.6,
  941.2, 953.1, 704.3, 717.4, 957.1, 717.5, 929.6, 963.3, 951.3; 2 inside. 0 failed fits in 160,000 toys; max
  |q̃ − exact| 1.2e-5 over 560,000 fits. My §2.4 expectation was right on the mechanism and the low branch, wrong on
  the high branch (CLs(μ_a) is 0.26–0.73 when the median is below the jump, not 0.05), hence wrong on the reading.
  Diagnostics: v1 statistic reproduces 789.7438 to 7e-10 with v1's seed; 12 seeds mean 815.4, sd 38.1; exact-q̃
  ensemble of 2e5 toys non-monotone between 810 and 833, first crossing 825.0. 10.7 ± 0.4 s per 1000 + 1000 toys.
- 2026-11-17 09:35 `p2-c-t1f-guard`: pyhf trap reproduced (hypotest default → CLs 0.0 without raising; fit returned
  at its start, 3.3e5 above the minimum); `newton_decrement` guard 1.8e5 on the false fits, ≤ 2e-7 on converged ones.
- 2026-11-17 09:36 -0500 result file `outputs/T1B_RESULT_flora_2026-11-17_09-35.md` written. CPU of the item 0.51 CPU-h in 22 jobs
  [V: markers p2-c-t1f-*]. Nothing of mine runs. SLOTS release line appended.

## State for a successor (rewritten 2026-11-17 09:36 -0500; replaces the section above)
- **Done:** T1-b verdict (FAIL as frozen, thin; cause = toy recipe at a discontinuity, not the likelihood), T1-a
  schema validation, diagnostics, pyhf-trap reproduction and guard, result file. Nothing is running.
- **Waiting on the user (through the orchestrator):** rewording of T1-b (proposal in the result file §7, not
  applied) together with C1-b and C2-a; whether the toy recipe of STR §4.11 pt 2 gets a bracket refinement and an
  empty-tail rule (strategy-revision input).
- **Not done:** cost of SLSQP tol 1e-10 and of the guard at 60–100 parameters; start-value rule for the v2 builder;
  the guard is tested on the 3-parameter workspace only. `p2-c-t1f-diag.json` (campaign file) was never launched.
- **Reproduce:** `python3 -I src/p2f_campaigns.py setup|setup2|prod <mu_a>|post <mu_a>|guard` then the launch line in
  that file's docstring; μ_a = 828.7069115492852; all results in `data/p2c/p2-c-t1f-post/000/` (verdict, v1stat, ref,
  hypo) and `data/p2c/p2-c-t1f-prod/000/` (every q̃ of every toy, exact values beside them).
- **Traps:** as listed in the earlier section (no numpy on einstein; driver "no capacity" at high load; done jobs
  never rerun; pyhf default starts; numpy backend at tight tolerance).
