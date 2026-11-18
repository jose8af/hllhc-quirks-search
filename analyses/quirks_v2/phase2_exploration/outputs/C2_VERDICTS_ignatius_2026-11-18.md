# C2-b (V4-4) and C2-c (T_seed stability) verdicts — executor Ignatius (channel (i)), 2026-11-18

Code `src/c2_verdicts.py` (definitions fixed in its docstring before it was run); output
`outputs/c2_verdicts_ignatius.json`; run on landau, nice 19, 47 s wall, 2026-11-18 ≈ 11:00. All campaigns complete with
done markers (checked by the script): p2-a-c2-v44a/b (20 + 20, landau), p2-a-c2-v44c (20 + 2, maxwell),
p2-a-c2-tseed1 (25), p2-a-c2-tseed2 (40), p2-a-c1-pu1 jobs 0000–0024, p2-a-c1-pu2 jobs 0000–0039. All numbers VERIFIED
from that JSON unless tagged.

## C2-b — V4-4 reproducibility and seeds (STR §4.2; COM C2-b): **PASS**

| criterion (frozen) | result |
|---|---|
| outputs bit-identical on the same node (20 jobs, -a vs -b, landau) | **20 / 20 identical** in all 89 npz keys except `job_id` (the job's name) and the timing keys skipped by `day0_summary.identical()` (`meta_json`, `chain.timing`, `trials.times*`, `trials.t_total`) |
| cross-node identity reported (-a landau vs -c maxwell) | **20 / 20 identical** (same exclusions). Both nodes: Intel Core i5-7500 @ 3.40 GHz, 4 CPUs (`lscpu`) |
| different seeds give different outputs | c2v44x-00 / -01 (stream c2.v44x) vs c2v44-00-a / -01-a: seeds differ (e.g. 20255362876062 vs 26379247137091) and the outputs differ in the trial, candidate and chain keys |
| all seeds recorded | job seed present in `meta_json` of every output; equal across -a/-b/-c of each job |

Power: bit identity is exact; there is no statistical element. Not covered: identity across CPU models (both nodes
have the same model, so cross-node identity says nothing about other hardware).

## C2-c — T_seed 4 → 2 (STR §4.2; COM C2-c; deviation D-i-4 regeneration): **PASS as frozen — but the test has no power**

Pairing: ρ = 1 500 events / 2,000 trials, ρ = 2 200 events / 400 trials (the STR sizes); in all 65 job pairs the chain
`evstats` are identical, the trial events identical, the trial PVs bit-identical, the job seeds equal, T_seed = 2 vs 4
read from `finder_cfg`. Metric: v1 `analyse_g3.tseed_test` "pass_frac" (a trial passes a rung if its per-hit-set count
g > 0); family statistic = fraction of trials passing at least one rung of the family; paired event bootstrap (2,000).

| density | family (rungs) | f(T_seed 4) | f(T_seed 2) | z (paired) | \|z\| < 2.73 |
|---|---|---|---|---|---|
| ρ = 1 | counting (R04) | 1.0000 | 1.0000 | 0.00 | yes |
| ρ = 1 | width (R05, R06) | 0.9995 | 0.9995 | 0.00 | yes |
| ρ = 1 | χ² (R09–R11) | 0 | 0 | 0 (untestable) | yes |
| ρ = 1 | 2S (R12–R14) | 0 | 0 | 0 (untestable) | yes |
| ρ = 2 | counting (R04) | 1.0000 | 1.0000 | 0.00 | yes |
| ρ = 2 | width (R05, R06) | 1.0000 | 1.0000 | 0.00 | yes |
| ρ = 2 | χ² (R09–R11) | 0 | 0 | 0 (untestable) | yes |
| ρ = 2 | 2S (R12–R14) | 0 | 0 | 0 (untestable) | yes |

**Verdict as frozen: PASS (0 of 8 tests with |z| ≥ 2.73).** Power, stated with the verdict: **none.** Four tests are
empty (no trial passes any χ² or 2S rung at either T_seed: the deep rungs are unpopulated in 2,000 / 400 trials) and the
other four are saturated (every trial passes R04 and R05 at PU 200), so a change of the finder's seed threshold cannot
move these fractions. The only rung with an unsaturated, non-empty pass fraction is R06 (a width rung): ρ = 1 0.2060 →
0.2070 (z +1.38), ρ = 2 0.5350 → 0.5375 (z +1.00), i.e. no detectable change.

**Diagnostic (v1's conservative reading, `mean_grp` = mean number of passing distinct hit sets per trial; no verdict):**
T_seed = 2 finds slightly more passing hit sets, consistently: ρ = 1 R04 163.5 → 164.0 (+0.32 %, paired z +28), R05
+0.33 % (z +15), R06 +0.41 % (z +1.4); ρ = 2 R04 +0.01 % (z +5.4), R05 +0.02 % (z +6.7), R06 +0.94 % (z +1.75). The
paired error is tiny (the events are identical), so a 0.3 % shift is many σ. Reading: the finder is not exactly
converged in T_seed — lowering the seed threshold adds ≈ 0.3 % (ρ = 1) more passing hit sets at R04–R05 — but the size
is far below every closure tolerance in STR (the B-term widths are tens of per cent). By STR's own fail wording the
paper would state "pass fraction changes by 0.0 % (R04–R06, ρ = 1 and 2); passing hit sets per trial change by
+0.3 % (R04, ρ = 1)".

**Phase 1 assumed** that the per-trial pass fraction of each rung family lies strictly between 0 and 1 at ρ = 1 and 2,
so that the 8-test Bonferroni rule can detect a change. **Phase 2 found** that at PU 200 it is 1 for R04–R05 and 0 for
R07–R14 at both densities (2,000 and 400 trials); only R06 is informative. **Implications:** C2-c as frozen cannot fail
and therefore does not test convergence; the informative statistics are the R06 pass fraction (no change) and the mean
number of passing sets (+0.3 %, significant, small). Proposed (NOT applied; for the orchestrator and the user): report
the mean-passing-sets shift at R04–R06 with its paired error as the T_seed statement, with no tolerance, or a tolerance
tied to the closure widths.

DECISION / ALTERNATIVES / CONFIDENCE / FLAG: in `experiment_log.md` (2026-11-18, Ignatius, C2-c family statistic).
