# EXPLORATION — channel (i), executor Mattias: final C1 open read (2026-11-19 10:23 -05)

This file extends `EXPLORATION_i_rosalie_2026-11-16_14-43.md` (unit costs, deviations D-i-1 to D-i-5, C1-b, the V4-5
ruling) and Ignatius's results (`../logs/executor_ignatius_2026-11-18_10-46.md` §3; `C2_VERDICTS_ignatius_2026-11-18.md`,
`V45_RESTRICTED_ignatius_2026-11-18.md`, `STITCH_100k_ignatius_2026-11-18.md`). It also covers Ignatius's item d.
The session log is `../logs/executor_mattias_2026-11-19_10-07.md`.

Tags: VERIFIED means measured or re-derived here, with the file or command cited; ESTIMATE and UNVERIFIED are used as
defined in AGENT_RULES. Unless a number is tagged otherwise, it is VERIFIED from
`c1_compare_mattias_2026-11-19.json` (background) or `c1_signal_open.json` (open signal tier).

## 0. Summary
- **Inputs complete:** p2-a-c1-pu1 200/200, pu2 200/200, cp0 16/16, cppua 50/50, cppub 75/75, gen2 12/12, sm 50/50
  and smregen 2/2. Status was checked with `qv2run status` at 10:13.
- **Code:** `src/c1_compare.py` at commit **29079b758b2188d733a4b278fbdf736341fc2dfe**, committed before any real
  read of the pu1, pu2 and closure families (§1). The C′_PU rule is the one of 54610b6.
- **Background (31 entries), frozen text:** 30 PASS and 1 FAIL. The FAIL is sm.R04 under the frozen-script width,
  z +3.64. It is the same verdict already on record and was not re-derived differently; its ticket was closed by E4.
- **Background (31 entries), amended:** 31/31 PASS. Every family is coherent.
- **Open signal tier:** 4/4 PASS.
- **No new FAIL.** No new regression trigger.
- **The 6 sealed C1-d counts were not touched.**

## 1. Task 1: joint-replica coherence for pu1, pu2 and clos (commit 29079b7)
**Defect.** The frozen script's coherence for pu1, pu2 and clos used `coherence_naive`, which treats the entries of a
family as independent. That is not true here:
- pu1 R04 ⊃ R05 ⊃ R06 are nested rungs on the same trials.
- clos.T1 and clos.T1w are pu1/pu2.
- The slope is a weighted least-squares fit to the T1-type ln ratios.
- The c-factor is computed on the pu1 events.

The orchestrator decided this fix on 2026-11-18 at 12:37 (LOG.md, point (b)), before the full read.

**Fix.** This mirrors 54610b6.
- `pu_joint_stats`, `pu_joint_reps` and `pu_joint` recompute all ten entries on one set of paired event resamples:
  PUSamples `bi1`/`bi2`, with nboot_v1 = 1000. These are the same resamples that give v1's trend width.
- `cfac_event_arrays` rebuilds the c_test cell per event.
- The nominal values are recomputed from the per-event arrays. The code raises an error unless they reproduce every
  entry to 1e-9; they did.
- `joint_family` then gives the coherence: the frozen form of inverse-variance weights, with the variance taken from
  the full covariance. The v1 correlation is assumed equal to v2's (ESTIMATE).
- The individual entries are unchanged.
- The frozen independent form is kept as `families[f].frozen_script_independent`.

**Tests.** `TestPUJoint` in `src/test_c1_compare.py` is synthetic and adds three tests:
- It reproduces v1 `analyse_g3.trend_test` (slope and s_slope_boot) and `c_test` (c and s_c) to 1e-12.
- On nested rungs, the joint width matches the ensemble scatter within 15 %, while the independent width falls below
  0.85 of it.

All 14 tests pass on landau (15.8 s wall). The commit hash is logged.

**Limitation (FLAG).** In the global sum, each of pu1, pu2 and clos enters as its own d′S⁻¹d block. The cross-family
dependence (T1 = pu1/pu2 exactly in logs) is not removed. Removing it would make the joint covariance singular and
change the degrees of freedom of the frozen χ²₄₁. The frozen naive sum is reported as primary.

## 2. Background families: 31 entries
Command (landau, nice 19, 265 s wall, 29.8 CPU-s, 722 MB):
`c1_compare.py --out outputs/c1_compare_mattias_2026-11-19.json`, with defaults nboot 500, nboot_v1 1000 and
nboot_cl 2000. Bonferroni limit: p > 0.05/41 = 0.00122.

| entry | v1 | v2 | z (frozen text) | amended / note |
|---|---|---|---|---|
| pu1.R04 / R05 / R06 | 171.55 / 49.72 / 0.2470 | 170.86 / 49.46 / 0.2479 | −0.35 / −0.41 / +0.19 | same |
| pu1.R07 / R08 / R09 (cond. binomial) | 35/48000, 0, 0 | 7/16000, 0, 0 | +1.07 (p 0.28) / 0 / 0 | R08 and R09 are gross checks only |
| pu2.R04 / R05 / R06 | 114.36 / 30.96 / 0.389 | 114.37 / 30.91 / 0.3865 | +0.00 / −0.10 / −0.54 | same |
| clos.T1 / T1w | 1.5001 / 1.6061 | 1.4939 / 1.6000 | −0.21 / −0.19 | same |
| clos.slope | −0.3608 ± 0.0045 | −0.3650 ± 0.0080 | −0.46 | same; see the FLAG below |
| clos.cfac (bin 2, layers 5,6,9 in both) | 1.1964 | 1.1903 | −1.35 | same |
| cp0.dif / ni22 / pvpair (Fisher) | 47473/50000, 22778/30000, 90310/100000 | 47538, 22794, 90182 | +0.93 / +0.14 / −0.96 | same |
| cppu.dif R04 / R05 | 166/500, 81/500 | 348/1000, 141/1000 | +0.14 / −0.41 | v1 width 0: +0.25 / −0.67 |
| cppu.gamma R04 / R05 | 153/500, 86/500 | 420/1000, 174/1000 | +0.53 / +0.02 | v1 width 0: +1.03 / +0.03 |
| cppu.v0 R04 / R05 | 859/500, 358/500 | 1493/1000, 612/1000 | −0.49 / −0.47 | v1 width 0: −0.81 / −0.78 |
| cppu.pvpair R02 | 24/500 | 131/2000 | +0.19 | v1 width 0: +0.48 |
| rates.ntrig / ntrig_Z | 4.085e7 / 2.508e7 | 4.187e7 / 2.649e7 | +0.86 / +1.26 | same (Ignatius 18 Nov, reproduced) |
| rates.dif / pvpair / gamma | 1.5945 / 30.31 / 0.379 | 1.6275 / 53.52 / 0.566 | +0.41 / +2.43 (p 0.015) / +0.58 | width ESTIMATE (rates DECISION, Ignatius) |
| sm.R04 / R05 / R06 | 19.52 / 4.509 / 0.01615 | 20.03 / 4.713 / 0.01910 | frozen script: **+3.64 FAIL** / +3.00 / +0.70 | **E4:** +0.35 / +0.57 / +0.50 PASS (v1 width 0: +0.50 / +0.82 / +0.75) |

**C′_PU family (task 2): 7 entries, pre-registered rule of 54610b6.**
- Width rule: v2 width from a cluster bootstrap per source C′0 event. The primary v1 width is v1 1/√N × v2's
  (bootstrap / Poisson) ratio. The v1-width-0 results are given alongside. There is no 1/√N verdict.
- N < 10 branch: not triggered. Every C′_PU entry has N ≥ 10 on both sides, so none used the frozen conditional
  binomial.
- Inflation of v2's width over 1/√N: ×2.4 to ×7.5.
- All 7 entries are gross checks only, with 2σ detectable shifts of 77 % to 2,660 %.
- Disclosure: Ignatius's partial file `c1_compare_cprime_partial_ignatius_2026-11-18.json` (written 12:17 on 18 Nov,
  1/√N width, cppub ≈ 20/75 inputs) predates the rule commit 54610b6. It is superseded and is not a verdict. The cp0
  entries in it had complete inputs and are reproduced here exactly.

**Families** (|z| < 3 is coherent):

| family | joint replicas (in force) | frozen independent form | block χ² (dof, p) |
|---|---|---|---|
| pu1 (R04–R06) | z −0.30 (s 0.0116) | z −0.41 (s 0.0079) | 0.64 (3, 0.89) |
| pu2 | −0.25 (s 0.0138) | −0.42 (s 0.0081) | 3.24 (3, 0.36) |
| clos (T1, T1w, slope, cfac) | −1.10 (s 0.0042) | −1.30 (s 0.0036) | 2.24 (4, 0.69) |
| cp0 | +0.03 | (same form) | — |
| rates | +1.68 | (same form) | — |
| cppu | −0.31 (v1 width 0: −0.40) | none (rule pre-registered) | 6.40 (7, 0.49); v1 width 0: **22.9 (7, 0.0018)** |
| sm | +0.51 (E4; v1 width 0: +0.73) | **+4.60 NOT coherent** (frozen script, on record) | 1.53 (3, 0.67) |

## 3. Open signal tier: 4 entries
Command: `c1_signal_compare.py open` (landau, 331 s wall, 60 CPU-s, 375 MB), which writes
`outputs/c1_signal_open.json`. The `--out` option is ignored in open mode. The test is Fisher exact against v1 k/200,
with z computed here from p.

| point | v1 | v2 | p | z | verdict |
|---|---|---|---|---|---|
| E200 1.5 keV R04 | 41/200 | 73/400 | 0.51 | 0.66 | PASS |
| E200 1.5 keV R06 | 33/200 | 64/400 | 0.91 | 0.12 | PASS |
| E200 2 keV R04 | 45/200 | 90/400 | 1.00 | 0 | PASS |
| E500 3 keV R04 | 61/200 | 82/400 | **0.0082** | 2.65 (v2 lower) | PASS (p > 0.00122) |

Twin R04 ratios (diagnostic, no criterion): full/fast = 1.027 at E200 1.5 and 0.889 at E200 2, against v1's
expectation of 0.832. The six sealed quantities (R07 ×3, FB2/FB3 ×3) were neither run nor opened.

## 4. Global χ² (partial: 35 of 41; the 6 sealed counts and the final test belong to the separate session)
| form | Σz² (35 entries) |
|---|---|
| frozen naive (as amended entries) | 16.11 + 7.45 = 23.56 |
| frozen naive with the SM frozen script | 45.6 |
| joint blocks (primary v1 widths) | 25.75 + 7.45 = 33.20 |
| joint blocks, v1 width 0 for sm/cppu | 43.91 + 7.45 = 51.36 |

For comparison, the 99th percentile of χ²₄₁ is 64.95, and of χ²₃₅ it is 57.34. These are reference values only.

## 5. FLAGS and strategy-revision inputs (no tuning was done)
1. **Closure slope is weight-fragile.** The partial value was z +2.83 (−0.3335, 148/200 pu1 jobs); the full sample
   gives z −0.46 (−0.3650). The three ln-ratio points barely moved:

   | point | partial | full |
   |---|---|---|
   | R04 | 0.398 | 0.401 |
   | R05 | 0.465 | 0.470 |
   | R06 | −0.445 | −0.444 |

   The swing comes from the weighted least-squares weight of R06. Its σ went from 0.0211 to 0.0190, and this σ comes
   from the pu2-prediction bootstrap, whose random-number stream shifts with the size of the pu1 sample. A cross-check
   shows the effect: the full points with the partial weights give −0.3338, and the partial points with the full
   weights give −0.3646.

   The linear fit has χ² = 685 on 1 dof, so the three points are not on a line. The slope therefore moves by about
   4 × s_slope_boot with the weights, and s_slope_boot (which holds the weights fixed) does not include this. v1 had 4
   points (with R07); v2 has 3 (R07 has fewer than 10 counts).

   Input for the pre-registration: fix the trend weights (or use an unweighted or a covariance fit) and state the
   width of the slope including its weight dependence. The entry passes as frozen.
2. **E500 3 keV R04, open tier:** p = 0.0082 (v2 20.5 % against v1 30.5 %). It passes the Bonferroni limit and is the
   largest open-tier deviation. Reported, not investigated.
3. **C′_PU block χ² with v1 width 0** is 22.9/7. The family coherence is fine (z −0.40), the individual entries pass,
   and the primary rule gives 6.4/7. The large v1-width-0 value comes from rung pairs whose v2 replicas are almost
   fully correlated (R04/R05) while their ratios differ, the same mechanism as in Lisbet's SM note. This is not a
   criterion.
4. **rates.pvpair** has z +2.43, p 0.015, with an ESTIMATE width and the maximum taken over ttbar_2l at N_eff ≈ 15.
   It is a gross check only (as in Ignatius's report of 18 Nov).
5. **Cross-family correlation** in the global sum (§1). The 41 quantities are not independent: T1/T1w ⊂ pu1/pu2.

## 6. Campaigns and CPU
Ledger rebuilt on 19 Nov after the 10:23 signal run, deduplicated by campaign + job_id [VERIFIED, `ledger/jobs.tsv`]:

| campaign group | CPU-h | budget |
|---|---|---|
| C1 (p2-a-c1-*), total | **186.2** | 198 |
| of which pu1 | 61.9 | |
| of which pu2 | 56.4 | |
| of which cppua | 13.8 | |
| of which cppub | 20.0 | |
| of which cp0 | 1.1 | |
| C2 (p2-a-c2-*) | 22.4 | 81 |
| day-0 | 0.95 | |

This session launched no campaign. Its direct nice-19 analysis runs on landau slot B came to ≈ 0.03 CPU-h:
- tests: 5.7 CPU-s
- c1_compare: 29.8 CPU-s
- signal open tier: 60 CPU-s
- slope cross-check: under 1 CPU-s

## 7. Not done or open
- **C1-c** (container recipe and one C1 job rerun with an identical hash): not started (Rosalie item 7).
- **Sealed C1-d tier and the global χ²₄₁:** for the separate session after the advisor.
- **Day-5 decision point (21 Nov):** the C1 open read is complete.

## 8. Self-review against `phase2_exploration/CLAUDE.md` (scope: C1 comparison)
- **Inventory:** the schemas are in Rosalie's file and the campaign markers; no new sample was made.
- **Data quality:** the pathology found is the slope fragility (FLAG 1).
- **Experiment log:** the session log is kept. experiment_log.md has no new judgment call beyond the coherence fix,
  which was the orchestrator's decision. No figures were made, and the plot items do not apply.
- **Blinding:** signal files were read only through `c1_signal_compare.py open` (R01–R06 only). No sealed quantity
  was computed or opened, and no permission refusal occurred.

## STATE FOR A SUCCESSOR — 2026-11-19 10:23 -05
- **DONE:** tasks 1–4 of the orchestrator's brief to Mattias.
  - Code commit 29079b7 (joint coherence).
  - Results: `c1_compare_mattias_2026-11-19.json` (31 entries) and `c1_signal_open.json` (4 entries).
  - This file is committed with them.
- **Running:** nothing of channel (i). The slot B queue is idle (file `logs/queue_landau_B_ignatius.txt`).
- **Remaining for channel (i):**
  1. C1-c container rerun.
  2. Decide whether FLAG 1 (slope weights) goes into PREREG_v2. This is an orchestrator question.
- **Not channel (i):** the sealed tier, run by its own session with `c1_signal_compare.py sealed` (see Rosalie's
  successor section, item 3).
- **Re-run:** on landau, from $QV2:
  `PYTHONDONTWRITEBYTECODE=1 nice -n 19 envs/tt/.pixi/envs/default/bin/python -B phase2_exploration/src/c1_compare.py --out <file>`
  takes ≈ 5 min. The tests are `cd phase2_exploration/src && … -B -m unittest test_c1_compare` (14 tests).
- **Traps:**
  - The slope value depends on the bootstrap random-number stream through its weights (FLAG 1). Do not compare runs
    on different subsets without fixing the weights.
  - `c1_signal_compare.py open` ignores `--out`.
