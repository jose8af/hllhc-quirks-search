# REGRESSION TICKET — C1 SM family (v), Z(νν) hard-scatter candidates per event

Investigator Jorund, 2026-11-18 12:27 -0500. Trigger: STR §4.1 item 5 (`phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`
l.605-607) after the FAIL in `phase2_exploration/outputs/c1_compare_sm_ignatius_2026-11-18.json` (Ignatius log,
12:17 entry). Nothing was fixed, tuned, launched or committed. Tags: VERIFIED = measured or re-derived here (source
given); ESTIMATE; HYPOTHESIS. Session log: `phase2_exploration/logs/investigator_jorund_2026-11-18_12-23.md`.

**Summary.** The FAIL comes from the width used in the z-score, not from the hard-scatter chain. The comparison
takes s_ln = 1/√(weighted candidate count) (0.5 % at R04), which treats ≈ 47 candidates per event as independent.
The event-level width, measured three ways on the v2 sample, is 5.0 % at R04, ten times larger. With event-level
widths the differences are +0.36σ (R04), +0.60σ (R05), +0.53σ (R06). No difference was found in the generator
(same Pythia version, card, settings; init file created by the first c1-sm job). Confidence in this cause: high
(about 95 %). The frozen FAIL stays on record; how the corrected verdict is recorded is a user decision (§3).

## 1. Origin

**What is wrong (VERIFIED).**
- `phase2_exploration/src/c1_compare.py` l.350-351 (`fam_sm`) passes `s_ln_used` of the factor "HS cand P(R)
  direct (presel-weighted)" as s₁ and s₂. That value is set in v1's `acts/stage4/analysis/background.py` l.205:
  `s = max(x['s_ln'] or 0.0, 1.0 / np.sqrt(x['N']))`; `depth_term` (l.656-657) adds the direct factor with no
  s_ln, and N is the preselection-weighted candidate sum. Check: 1/√39032.5 = 0.005062 and 1/√40057.1 = 0.004996,
  the two s_ln values in the JSON, to all digits. This is a Poisson error on candidates.
- The statistic is a mean over 2,000 events of w_event × n_candidates. Measured on the 50 `p2-a-c1-sm` outputs
  with the `p2-a-c1-smregen` weights (landau, nice 19, about 1 CPU-min; script in the session log): candidates
  per event at R04 mean 47.27, standard deviation 57.6, maximum 523; 849 events with w > 0, 1,151 with w = 0.
  The script's mean reproduces Ignatius's values (20.02853; 94,537 unweighted).

| rung | ln(v2/v1) | s_ln used (each side) | event-level s_ln, v2: analytic / bootstrap (2,000 replicas) / scatter of the 50 job means | z as frozen script | z with event bootstrap on both sides |
|---|---|---|---|---|---|
| R04 | +0.0259 | 0.0051 / 0.0050 | 0.0510 / 0.0505 / 0.0478 | +3.64 | +0.36 |
| R05 | +0.0442 | 0.0105 / 0.0103 | 0.0527 / 0.0519 / 0.0483 | +3.00 | +0.60 |
| R06 | +0.1675 | 0.176 / 0.162 | 0.221 / 0.222 / 0.218 | +0.70 | +0.53 |

  The last column sets v1's width equal to v2's (ESTIMATE: v1's per-event candidate counts are lost; v1's weight
  part is tracked and agrees, see below). With v1's error set to zero the values are +0.51, +0.85, +0.76: the
  conclusion does not depend on the assumption. The variance is underestimated by a factor ≈ 100 at R04
  (effective sample ≈ 384 events of 2,000).
- Family coherence z +4.6 uses the same widths and treats R04, R05, R06 as independent although they are nested
  counts on the same events. With event-level widths the same formula gives ≈ +0.8 (ESTIMATE, my arithmetic; still
  an overstatement because of the correlation).
- The decomposition quoted in the finding is inside the event-level errors: unweighted candidates +1.2 % against a
  relative standard error of 2.7 % per sample; mean preselection weight 0.4107 vs 0.4189 (−2.0 %) against 2.6 % per
  sample (v1: 2.59 % from the tracked `C12FC_v1/sm_regen.json`, v2: 2.63 %); events with w > 0: 849 vs 865.
  Correlation of weight and multiplicity in v2: +0.022; candidates per event 48.6 ± 2.1 (w > 0) vs 46.3 ± 1.6
  (w = 0). No covariance effect is visible.

**Origin phase.** Phase 2 comparison code (Rosalie's design note in her successor section item 1 (v), implemented by
Ignatius), inheriting a v1 convention. Contributing gap in Phase 1: STR §4.1 item 1 (l.594-596) names the event
bootstrap only "for pile-up quantities" and item 4 (l.601-604) states no power for the SM row, so nothing flagged a
quoted 2σ sensitivity of 1.4 % (`mde_2sigma` in the JSON) as implausible for 849 weighted events. The true 2σ
detectable shift is about 15 % at R04 and R05 and about 87 % at R06 ("gross check only" under item 4) (ESTIMATE
from the measured widths).

**Leads that were checked and ruled out (VERIFIED unless marked).**
1. Environment of the hard-scatter generation. The c1-sm chain step runs through `pixi run --manifest-path
   acts/pixi.toml` (`acts/stage4/run_stage4.py` l.267), so the environment is activated; the missing-PYTHIA8DATA
   failure of c1-gen (bare interpreter) does not apply. Pythia is 8.312 in both lock files (v1 `TT/acts/pixi.lock`:
   osx-arm64 build 7; v2 `acts/pixi.lock`: linux-64 build 107): same version, different platform, as STR §4.1
   already assumes (unpaired comparison). CP5 card sha256 identical (3002a2a3…ddc7). `gen_d123.py` identical
   (2bb94cfb…b3de, also in the smregen provenance). `s4pu.py` differs only in the directory of the MPI init file
   (diff: l.22 and l.112-115; v1 0d2a773f…8e21, v2 75e2f06c…8438); process lines, pTHatMin 150, MET filter unchanged.
2. MPI init file. `/home/scratch/jdochoa/cache/pythia_init/mpi_cp5_14tev_hs_Znunu_j.dat` (2,078 B, sha256
   81ff6a4a…2070) has mtime 17 Nov 09:12:33; job c1sm-0000 started at 09:12:25 (its log). It was created by that
   job through the normal path (`s4pu.mpi_init_lines`, reuseInit = 1, then renamed), not by the failed c1-gen jobs
   (`gen_d123.py` mode nt builds `HardScatter(..., tt=None)`, l.229: no init file). smregen in the ACTS
   environment reproduces the stored truth MET of 2,000/2,000 events. v1's own init file is lost, so a byte
   comparison is not possible (the v1 note in `s4pu.py` l.110 says events are identical to ~1e-11 with or without it).
3. Generator-level agreement. MET-filter tries per accepted event 3.264 ± 0.062 (v2) vs 3.346 (v1, same size):
   −0.9σ. Mean weight and pass count as above.
4. Pile-up part: PU-only families agree (Ignatius: R04 −0.7 %, z −0.55, partial pu1).

**Residual (HYPOTHESIS, not supported by any check).** A real hard-scatter shift below about 10 % cannot be excluded
by this row: v1's sample is fixed at 2,000 events, so no v2 sample size brings the 2σ sensitivity below ≈ 10 %.

## 2. Impact trace

- **C1 verdicts.** SM family: frozen-script verdict FAIL (on record). With event-level widths: 3 of 3 individual
  pass, coherent, R06 gross check only. Global χ²₄₁: the SM rows contribute 22.8 as scripted, about 0.8 with
  event-level widths (ESTIMATE).
- **C′_PU family (iii), 7 entries, not yet evaluated.** `c1_compare.py` l.253-254 uses the same `s_ln_used`;
  v1's stored factors have s_ln = None and 1/√N (e.g. V⁰ R04 859/500: 0.0341 = 1/√859, VERIFIED in
  `C12FC_v1/background.json`), although the docstring (l.26) says "bootstrap s_ln (clustered by source C′0
  event)". Counts above one per slot (V⁰ 859/500, 358/500) are clustered. Expect inflated z there too; the width
  must be corrected before that family is read, otherwise a second ticket follows. Size not measured (inputs incomplete).
- **Other families.** PU ρ = 1, ρ = 2 and closure use the event bootstrap (l.97-112, l.179-193): unaffected. C′₀
  f_pre (binomial k/n per event) and rates: unaffected by this defect.
- **Decision point 1 (21 Nov).** The block is formal (STR item 5), not physical: no evidence of a port defect in
  the hard-scatter chain. It is lifted once the user rules on how the corrected width is recorded (§3). Nothing
  has to be regenerated for it.
- **v2 terms on the same hard-scatter chain** (pilot hard-scatter block hph / g4h / c0-hs; forced-tt̄ lines injected
  at run time in `phase2_exploration/src/p2c_hs0.py` l.43-47, `s4pu.py` itself unchanged): the generation is not
  implicated, no rerun. What does carry over is the error model: any v2 hard-scatter or C′ term that takes its
  Monte Carlo width from `Term.evaluate` / `depth_term` direct factors inherits 1/√(candidates). At R04 that is
  ×10 too small; at deep rungs with few candidates in different events it converges to the right value. The
  pilot scripts p2c_hs0 / p2x_hs0 / p2x_hspool do not call these functions (grep, VERIFIED); the Phase 3-4 estimator
  code must use event-level counts (STR §5 "bootstrap errors for estimator outputs"). Input for PREREG_v2.
- **v1 record (read-only).** v1's σ_ln of the SM hard-scatter probability at R04-R06 (0.006 at R04) understates the
  Monte Carlo error by the same factor; v1 central values are unaffected. To be stated when v1 widths are quoted.

## 3. Scope of the fix (for the fix agent; not done here)

1. `c1_compare.py` `fam_sm`: v2 width from an event bootstrap of Σ w·n over the 2,000 events (events with no
   candidate included), all three rungs from the same replicas; family coherence from the joint replicas. v1 width:
   not recomputable (per-event counts lost). Options to put to the user: (a) v1 relative width := v2's (stated
   ESTIMATE); (b) v1 width := 0, which is the stricter test and also passes (+0.51, +0.85, +0.76). Report the power
   (≈ 15 %, 15 %, 87 %) with the verdict.
2. Same change for the C′_PU entries (cluster by source C′₀ event) before family (iii) is read.
3. Keep the scripted output `c1_compare_sm_ignatius_2026-11-18.json` unchanged; write the corrected result to a new
   file; record both in the EXPLORATION artifact.
4. Recording. The change is made after the result is known. Following the handling of E1–E3 (`COMMITMENTS.md`
   l.286-296), my recommendation is an amendment "E4" approved by the user: frozen verdict FAIL stays on record,
   the amended criterion (event-level widths for every quantity counted per candidate) is labelled after-the-result.
   The alternative reading, "implementation bug of the frozen text, no amendment", is defensible (item 1 defines s as
   the statistical error) but the text does not name the SM row, so I do not recommend deciding it below the user.
5. No change to the chain, seeds, samples or any threshold.
Cost: about 2 agent-hours (code 1, rerun and write-up 1), under 0.1 CPU-h (the full compare runs in ≈ 4 min on a worker).

**Second-seed rerun of c1-sm: not recommended.** Cost 14.5 CPU-h (VERIFIED: 50 jobs, ledger markers of
`p2-a-c1-sm`), which would take channel (i) past the C1 budget (projected ≈ 190 of 198 CPU-h, Ignatius). It cannot
separate fluctuation from cause: a second sample has the same 5 % width, and the 50 job means of the existing sample
already give an independent replication of the width (4.8 %). It would be justified only if the user wants the
residual hypothesis tested at about 7 % (two v2 samples against each other), which says nothing about v1.

## 4. Downstream cascade

- Re-run: `c1_compare.py --families sm` and, when cppua/cppub are complete, `--families cprime`, both with the
  corrected widths; then the full 41-entry run and the global χ² (dedicated session for the sealed part, unchanged).
- Skip: p2-a-c1-sm, p2-a-c1-smregen, c1-gen2, pu1, pu2, cp0, cppu generation, all C2 items, the pilot campaigns,
  stitch: their inputs are unaffected.
- Later phases: none run yet. Carry the error-model note into PREREG_v2 and the Phase 3 estimator code.

## 5. Regression triggers met (methodology §6.7)

- Met formally: validation failure under a frozen criterion (STR §4.1 item 5: family FAIL → ticket, blocks decision
  point 1). This is remediation attempt 1 of the 3 that item 5 allows.
- Not met after investigation: no disagreement on an observable beyond statistical error, no closure failure, no
  > 3σ deviation from a reference once the width is the statistical error.
- Classification: local Phase 2 code defect in the comparison (CLAUDE.md "Not regression: current-phase code
  bugs"), with a wording gap in STR §4.1 items 1 and 4. No earlier phase has to be re-run; Phase 1 text needs the
  amendment of §3 point 4 only.

## For the user

1. Approve recording the corrected SM verdict as amendment E4 (recommended), or rule it an implementation bug.
2. Choose the v1 width: equal to v2's (ESTIMATE) or zero (stricter; also passes).
3. Confirm no second-seed rerun (14.5 CPU-h).
