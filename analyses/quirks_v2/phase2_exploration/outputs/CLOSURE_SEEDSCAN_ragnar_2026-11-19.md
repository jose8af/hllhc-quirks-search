# DIAGNOSTIC: seed scan of the C1 closure family (clos.slope, clos coherence)

Executor Ragnar, channel (i), 2026-11-19 10:30–10:45 -05 (`date`). Asked for by the advisor ruling (Oddny, LOG.md
2026-11-19 10:28). **This is a diagnostic. It does not replace the frozen verdict**: clos.slope with seed 20261014 has
z −0.46, PASS, as on record (Mattias, `c1_compare_mattias_2026-11-19.json`).

## Method
- Code: `--closure-seed` option added to `src/c1_compare.py`. Its default is the frozen seed 20261014, and the frozen
  path is unchanged. A non-default seed is labelled DIAGNOSTIC in the output (`closure_seed`). Test
  `TestClosureSeedOption`: 16/16 tests pass on landau. **Committed in c9dfbfe before any real run.**
- Run: `c1_compare.py --families pu,closure [--closure-seed s]` on the full inputs (pu1 200/200 jobs, 16,000 B1
  trials; pu2 2,000 B2 trials), nboot_v1 = 1000, on landau slot B with `nice -n 19`, one run at a time. The seeds were
  the frozen one, then 1, 2, …, 10. The seed drives PUSamples, the closure trend bootstrap, c_test, and the joint
  replicas of the clos coherence. The pu family seed (20261116) is unchanged. No signal file was read.
- CPU: 18.7–22.0 CPU-s per run, max RSS 663 MB, 11 runs in total ≈ 3.6 CPU-min [VERIFIED, `/usr/bin/time`].
- **Frozen reproduction [VERIFIED]:** the default-seed run gives a clos.slope z of −0.4561686640330229, identical to
  the last bit of Mattias's json. `v2_closure_detail`, the families clos, pu1 and pu2, and all 10 pu1/pu2/clos entries
  are equal (Python `==`).

## Result (10 non-frozen seeds) [VERIFIED, `CLOSURE_SEEDSCAN_ragnar_2026-11-19.json`]

| quantity | frozen seed | min | max | mean | sd |
|---|---|---|---|---|---|
| σ(R04) | 0.01400 | 0.01346 | 0.01453 | 0.01388 | 0.00031 |
| σ(R05) | 0.01459 | 0.01398 | 0.01513 | 0.01444 | 0.00033 |
| σ(R06) | 0.01903 | 0.01882 | 0.01928 | 0.01902 | 0.00016 |
| slope b₂ | −0.36495 | −0.37016 | −0.35776 | −0.36297 | 0.0034 |
| s_slope_boot | 0.00804 | 0.00773 | 0.00831 | 0.00795 | 0.00018 |
| clos.slope z | −0.46 | −1.04 | +0.32 | −0.24 | 0.37 |
| clos coherence z (joint) | −1.10 | −1.21 | −1.04 | −1.15 | 0.043 |
| clos coherence z (frozen independent form) | −1.30 | −1.37 | −1.20 | −1.28 | 0.060 |
| clos block χ² (4 dof) | 2.24 | 1.87 | 3.42 | 2.14 | 0.47 |
| clos.cfac z | −1.35 | −1.47 | −1.23 | −1.30 | 0.075 |

Seed-independent values: the ln-ratio points (R04 0.4014, R05 0.4700, R06 −0.4442), T1 z −0.21, T1w z −0.19,
c = 1.190, and the unweighted slope −0.4228.

- **No seed gives |z| > 3.23** for clos.slope (largest |z| 1.04, seed 6) or for the clos coherence (largest |z|
  1.21). The DECISION-notice condition of the ruling is not met. A disclosure line at DP1 is enough.
- The frozen z (−0.46) lies inside the seed spread (mean −0.24, sd 0.37). Seed-to-seed, the slope moves by
  sd 0.0034 ≈ 0.4 × s_slope_boot.

## σ(R06): partial 0.0211 vs full 0.0190
- Seed scatter at full inputs: sd 0.00016, range 0.01882–0.01928. The partial value 0.02107 is **12.6 sd** above the
  seed mean and outside the range. **The change is not seed scatter. It comes from the 148 → 200 pu1 jobs**
  (11,840 → 16,000 B1 trials; B2 is unchanged at 2,000) [VERIFIED for the scatter].
- Size check [ESTIMATE]: assume the R06 observed count is Poisson and the prediction term is unchanged.
  σ_pred² = 0.01902² − 1/3966, so σ_pred = 0.0105. At 3966 × 11840/16000 ≈ 2935 observed groups this predicts
  σ(R06) = 0.0212 for the partial read, against 0.0211 measured. The change has the size of the pu1 sample growth.
- The slope swing between the reads (partial −0.3335, z +2.83; full −0.3650, z −0.46; Δ ≈ 0.031) is about 9× the
  seed sd of the slope (0.0034). So it also comes from the sample size, through the WLS weights (Mattias's cross-check:
  full points with the partial weights give −0.3338). The weight fragility is real and is not a random-number artefact.
  The PREREG input of EXPLORATION_i §5.1 (fixed or unweighted weights, or a covariance fit) stands. The unweighted
  slope is −0.4228, which is different again.

## Files
`outputs/CLOSURE_SEEDSCAN_ragnar_2026-11-19.json` (per-seed values, statistics, frozen-reproduction checks, partial
read values). The raw per-seed c1_compare outputs are at `landau:/home/scratch/jdochoa/ragnar_seedscan/seed_*.json`
(scratch, not kept). Session log: `logs/executor_ragnar_2026-11-19_10-30.md`.
