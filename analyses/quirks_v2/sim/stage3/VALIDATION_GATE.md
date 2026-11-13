# Stage 3 validation gate: result

E7 (executor), 2026-10-11. Plan: `plan.md` §5 (criteria fixed there; the user approved D1-D16 as recommended).
Tags: VERIFIED = measured here; ESTIMATE = model or extrapolation. Everything is truth level. Result JSONs:
`results/V*.json`; scripts: `validation/val_*.py`; run products: `data/sim_stage3/validation/`, `data/sim_stage3/out/p1/`.

## Verdict
**GATE FAILED: V2b (the c law on the MadGraph sample, plan §5) does not pass its pre-registered criterion.**
Following the instruction ("if V1 or V2b fails, STOP"):
- **no production was launched** on either machine;
- **nothing was written to the USB**: `/Volumes/J8A/quirks_sim` still holds only `env/` and `SETUP_WINDOWS.md`, unchanged.

V1 (kernel regression), the other blocking test, passes. The failure is a reportable physics finding: it is not a step
effect (it survives 10x finer steps), and the criterion was not changed. The bundle is built and verified locally
(`data/sim_stage3/bundle/quirks_sim/`), so production can start within minutes if the user decides to proceed
(§5 below).

## 1. Summary table

| Test | Criterion (plan §5) | Result | Verdict |
|---|---|---|---|
| **V1** kernel regression | s3 `legacy=True` bit-identical to `code/T3_causal.run_causal` (hits, status, nsteps) | 240/240 runs bit-identical (20 MG events x V/B/BM/M x 0.6/3/10 keV), including final X, P, eacc; repeated on the final kernel s3.2 | **PASS** |
| V1b new recorder | legacy hits reproduced < 1e-9 cm; disc hits checked independently | 180 runs: max diff 1.1e-13 cm, 0 missing, 0 extra; 431 vacuum hits (298 on discs) within 2.4e-4 cm of the exact solution (ExactPair; chord-interpolation error, same as T3's 5e-4 tolerance), crossing counts per surface = independent numpy scan (0 mismatches) | PASS |
| V2a Stage-1 numbers | M3/FU per-event values and medians reproduced exactly | 960/960 per-event Delta_s bit-identical (500/1000 GeV, 1 keV M3-prod and 3 keV FU-fine settings, B0 and B0/2, 120 T2-cache events); median c2 = FU.json exactly: 0.10531 / 0.08903 / 0.10119 / 0.08410 | **PASS** |
| **V2b** c law on MG (GATE) | at 1 keV, per point: abs(median c2 - median c_ev) <= 2 sigma AND <= 1.5 %; all 5 points | E200 +0.70 % PASS; **E500 +2.00 % (2.3 sigma) FAIL; E1000 +1.07 % PASS; E1500 +2.10 % (2.2 sigma) FAIL; Etilde500 +3.15 % (2.4 sigma) FAIL** | **FAIL** |
| V3 step convergence / floor | Delta_s change < 1 % (<= 5 keV); hits < 1 um out of plane / < 5 um in plane (median over events of the per-event max) at the production settings | 30 of 32 production-setting cells pass. Out of plane <= 0.76 um everywhere; in plane <= 0.70 um up to 10 keV. Fails: E 1000, 3 keV, B, 1e-2: Delta_s +1.8 % (P1 B runs at 1e-3: +0.07 %); E 1000, 30 keV, B, 1e-2: in-plane 5.5 um (6 events; BK 3.2 um) | **FAIL** (2 cells, literal); §3 |
| V4 independent solver (R1) | median Delta_s ratio 0.99-1.01 and max hit distance <= 8 um (R1 N = 256; 1024 on 2 events) | median ratio 1.0010 (500 GeV, 1 keV), 1.0011 (1000 GeV, 1 keV), **1.112 (500 GeV, 2 keV)**; max hit distance 505-3631 um (grazing crossings, and R1 gauge breakdown events) | **FAIL** (literal); §4 |
| V6 seeds / reproducibility | 50 random jobs rerun bit-identical; different events never identical; spawn | 50 jobs (p1/p2/mv; B, B2, V, M, BM, BMx0.5, BMx2, Mx0.5), 4329 events: 0 differing arrays between 7- and 3-worker runs; 0 duplicate events | **PASS** |
| V8 ACTS ingestion | hits on their surface, units right, measurements produced | ACTS env (pyacts 48.0.0), 10 P2 events: 430/430 physical hits `isOnSurface` (1 um), 573 SimHits -> 573 measurements (generic 2D Gaussian smearing re-keyed to the Stage-3 surfaces), t >= r/c for all hits | **PASS** |

Not run in this session (the plan schedules them, but they do not gate): V5 (T2-cache continuity), V-scale, V9 (weighted
vs unweighted), V7 (production sanity: production did not start).

## 2. V2b in detail (THE GATE)

**Inputs.** Production P1 jobs through `code/run_stage3.py` (kernel s3.2) are used. Settings: B0 = 3.8112 T and B0/2,
max_boost 1e-3, hmax 0.2 cm, |eta_pair| < 1, vertex at the origin. The sample is 300 MG events per point (TRGS,
pT(QQ) > 200 GeV, unweighted, template; both halves at E 1500). Delta_s_B is the plane through the vertex on the 10 T3
barrel radii (the Stage-1 definition).
- Measured c per event: c2 = (2 Delta_s(B0/2)/Delta_s(B0) - 1)/ln 2 (Stage-1 convention, FU_analysis).
- Prediction per event: c_ev = 1/[ln(l_max/b_odd) + K(gamma*)], from `analytic/checks/c06_rotating_yoyo.pair_params`
  (imported, read only) on the same events.
- Statistic: the plan says "median measured c vs the analytic per-event prediction ... <= 2 sigma and <= 1.5 % at
  1 keV (P-10)", where P-10 is a statement about the population median. It was implemented before the run as
  Dc = median(c2) - median(c_ev), with a paired-bootstrap sigma (2000 resamples), and the condition that all 5 points
  pass.
- All 3000 events per Lambda ended with status 1 (left the volume), and all have finite Delta_s.

| point (1 keV) | median c2 | median c_ev | Dc | rel. | pull | paired median(c2 - c_ev) | k_B < 6: c2 / c_ev (n) | k_B >= 6: c2 / c_ev (n) |
|---|---|---|---|---|---|---|---|---|
| E 200 | 0.1135 +- 0.0014 | 0.1127 | +0.0008 +- 0.0014 | +0.70 % | 0.6 | -0.0010 | 0.1151 / 0.1134 (276) | 0.0798 / 0.0992 (24) |
| E 500 | 0.1064 +- 0.0009 | 0.1043 | +0.0021 +- 0.0009 | **+2.00 %** | 2.3 | +0.0002 | 0.1074 / 0.1063 (229) | 0.0953 / 0.0974 (71) |
| E 1000 | 0.0996 +- 0.0008 | 0.0986 | +0.0011 +- 0.0008 | +1.07 % | 1.3 | -0.0003 | 0.1038 / 0.1031 (149) | 0.0934 / 0.0950 (151) |
| E 1500 | 0.0983 +- 0.0010 | 0.0963 | +0.0020 +- 0.0009 | **+2.10 %** | 2.2 | -0.0000 | 0.1024 / 0.1021 (133) | 0.0941 / 0.0925 (167) |
| Etilde 500 | 0.1063 +- 0.0013 | 0.1031 | +0.0033 +- 0.0014 | **+3.15 %** | 2.4 | +0.0005 | 0.1072 / 0.1063 (189) | 0.0997 / 0.0971 (111) |

The E1 polynomial K(gamma*) of FU_analysis gives the same medians of c_ev to 1e-4 (0.1128/0.1043/0.0986/0.0963/0.1031).
At 0.6 and 2 keV (reported, not gating), Dc ranges from -0.0015 to +0.0037.

**Diagnostic: step size** (`validation/val_v2b_diag.py`, `results/V2b_diag.json`). The same 300 events at E 500 and
Etilde 500 were rerun at max_boost 1e-4, 10x finer.
- Median c2 changes by -1.8e-5 and -1.5e-5, and Delta_s_B by -0.08 % and -0.04 %.
- Dc stays at +0.0020 +- 0.0008 (+1.93 %) and +0.0033 +- 0.0013 (+3.17 %).
- **The excess is not numerical** (VERIFIED).

**What the numbers say (interpretation; ESTIMATE).**
1. Per event, the law holds on typical events. The paired median of (c2 - c_ev) is within +-0.001 (<= 1 %) at every
   point, and for k_B < 6 (where the per-event law is claimed valid, predictions.json `c`) the subset medians agree
   within +0.3 to +1.5 %.
2. The *population* median of the measured c lies 1-3 % above the median of the per-event predictions at 3 of 5 points.
   The measured per-event c has a wider and skewed distribution (the k_B >= 6 events scatter strongly in both
   directions, the B* effect of NEAR_MISS §6.4), so the median of c2 is not the median of c_ev, even when the median of
   the differences is about 0.
3. The same feature is already in the Stage-1 data. On the M3 events (FU1a m500_L1_prod) the median c2 is 0.1053 against
   a same-event median c_E1 of 0.1029 (+2.4 %), while the paired median difference is 5e-5 +- 8e-4. Stage 1 quoted
   "<= 1.5 %" against the population prediction 0.104 of a different sample (c07). The V2b test compares on the same
   events, so the 1.5 % population claim of P-10 is not supported on the MG sample at E 500, E 1500 or Etilde 500.
4. The size grows with the fraction of hard-gamma* and high-k_B events: Etilde (harder gamma* spectrum) +3.2 %, and
   E 500 / E 1500 +2 %.

**Other V2b items (reported, not gating).**
- P-13: R(1/2) at E 500, 1 keV = 1.0737 (median) vs predicted 1.072. Agrees.
- P-15: the median Delta_s_B at 1 keV is flat in m: 31.1 +- 1.7, 29.5 +- 1.6, 28.7 +- 1.5 and 30.4 +- 1.1 um at
  200/500/1000/1500 GeV. The slope d ln/d ln m is -0.02. The T3-sample model medians (33.5/31.1/29.5) are 5-7 % higher,
  which is a sample effect.
- P-24: Etilde 500 / E 500 Delta_s_B = 1.149 vs model 1.161. Agrees.
- P-11 exponents d ln Delta_s_B/d ln Lambda (per-event medians):
  - 1 -> 2 keV: -1.807 +- 0.017 / -1.807 +- 0.015 / -1.831 +- 0.013 / -1.856 +- 0.009 / -1.861 +- 0.012, against
    -2 + 2c = -1.79 / -1.805 / -1.815 / -1.819 / -1.807 (E 1500 and Etilde 500 at 4-4.5 sigma);
  - 0.6 -> 1 keV: -1.88 to -1.95 against -1.76 to -1.80. That is 4-6 sigma, in the range where the plan expected the
    secular law to start failing (non-secular b_odd ~ m/Lambda^4 terms, §1.2).
- C re-derived on the MG sample (C = 1/median c2 - ln(1/eps_B)): 0.41 / 1.01 / 1.64 / 1.78 (E 200/500/1000/1500) and
  1.01 (Etilde 500). The medians of the per-event C on the same events are 0.48 / 1.19 / 1.75 / 1.99 / 1.30. The
  predictions.json values on the T3 sample are 0.43 / 1.23 / 1.62. A difference from the T3 values is a sample effect.

## 3. V3 step convergence and floor
`validation/val_v3.py`, `results/V3.json`.
- **Setup:** 1368 runs, 8.0 CPU-h (69 min wall); P2 selection, vertex at the origin, all surfaces; deterministic
  configurations B, BE and BK (J != 0 as from MS).
- **Event counts:** 20 events per mass (200, 1000 GeV) at 1, 3 and 10 keV. At 20 and 30 keV only 6 events and B/BK
  only: the plan's 20 events would cost about 8 CPU-h more (budget reduction, stated here).
- **Run status:** 3 of 1368 runs ended in a queue overflow (status 5, qcap 2^19; production reruns status 3/5 once
  with qcap 2^21), and 2 ran to t_end (status 0).

Metrics are medians over events of the per-event maximum hit displacement for hits matched by (quirk, surface, crossing
index), and the median per-event Delta_s ratio (all tracker surfaces, plane through the vertex):

| setting tested (production) | out of plane [um] | in plane [um] | Delta_s change | worst event in plane [um] | verdict |
|---|---|---|---|---|---|
| 1 keV, 1e-3 vs 1e-4 (P2 <= 1.5 keV; B/BE/BK, 200 and 1000 GeV) | 0.03-0.09 | 0.05-0.21 | +0.03 to +0.08 % | <= 1.5 | PASS |
| hmax 0.2 vs 0.05 cm (0.3 and 1 keV, 1e-3) | <= 0.22 | <= 0.34 | 0.00 % | 21.8 (one grazing hit, 0.3 keV) | PASS |
| 3 keV, 1e-2 vs 1e-3 (P2 >= 2 keV) | 0.13-0.23 | 0.10-0.70 | B **+0.85 % / +1.82 %**, BE +0.9/+1.0 %, BK +0.2/+0.7 % | <= 6.7 | B at 1000 GeV FAILS the 1 % Delta_s criterion |
| 3 keV, 1e-3 vs 1e-4 (P1 B / B2) | 0.02 | 0.02-0.03 | +0.11 % / +0.07 % | <= 0.24 | PASS |
| 10 keV, 1e-2 vs 1e-3 | 0.06-0.19 | 0.06-0.55 | -1.6 to +2.5 % (B-only, floor noise) | <= 12 | PASS (hits) |
| 20 keV, 1e-2 vs 1e-3 | 0.09-0.27 | 0.27-1.24 | -9 to +2 % (B-only, floor) | <= 4.4 | PASS (hits) |
| 30 keV, 1e-2 vs 1e-3 | 0.14-0.76 | 1.1-3.2; **B 1000 GeV 5.5** | -13 to +3 % (B-only, floor) | <= 13 | B at 1000 GeV FAILS in plane (BK passes) |

Floor replicas: per-event relative round-off spread of the B-only Delta_s, from 3 replicas with initial momenta
x (1 + 1e-14 N(0,1)) at 1e-2:

| Lambda | median spread (200 / 1000 GeV) | max spread | events with spread > 1 % |
|---|---|---|---|
| 10 keV | 1.6 % / 2.3 % | 26-57 % | 60 % |
| 20 keV | 3.4 % / 2.1 % | | 67-83 % |
| 30 keV | 7.3 % / 0.9 % | | 50-100 % |

B-only thickness above about 10 keV is therefore set by round-off at the per-cent to tens-of-per-cent level per event
(VERIFIED; it confirms plan §1.1 and the `floor_flag` rationale).

Reading (ESTIMATE):
- **Hit positions:** converged below the IT resolution (3-13 um) at every production setting (worst-cell median 5.5 um
  in plane, in the B-only 30 keV cell, where the B-only dynamics are at the floor).
- **The two literal failures concern B-only quantities at max_boost 1e-2:** the +1.8 % Delta_s step bias at 3 keV
  (the Stage-1 "1e-2 bias" already seen in plan §6.3, and the reason P1 B runs at 1e-3), and the floor-dominated
  30 keV in-plane spread.
- **Production impact:** neither affects the B+M production configuration at the hit level (BK, the J != 0 proxy,
  passes: 3.2 um at 30 keV). The production settings (D8) are kept, but V3 is reported as a literal FAIL.

## 4. V4 independent solver
The specified test (R1 conformal solver, `code/R1_conformal_ng.py`, N = 256 on all events and 1024 on 2 per set, against
s3 configuration B at max_boost 1e-3) fails literally:
- median Delta_s ratios: 1.0010 (500 GeV, 1 keV), 1.0011 (1000 GeV, 1 keV), 1.112 (500 GeV, 2 keV);
- maximum matched hit distance: 505-3631 um.

**Diagnostic** (`val_v4.py --diag`, `results/V4_diag.json`): R1 at N = 1024 and 4096 on all 30 events.
- **Median ratio:** 1.0007-1.0011 (1 keV) and 1.0003 (2 keV) at both N, inside 0.99-1.01.
- **Events with equal hit counts:** they agree to ratio 0.999-1.002 and 0.1-2 um, with two stable outliers. One E 500
  1 keV event has ratio 0.952 and 12.4/12.6 um at N = 1024/4096; one E 500 2 keV event shows 76 um at N = 4096.
- **Events with unequal hit counts:** these are runs where the original R1 code continues through the conformal-gauge
  breakdown. The Stage-1 copy `nm_conformal.py` aborts such runs (status 7) and excludes them.
- **N = 256:** R1 is not converged there (Stage 1 used N up to 4096).

Reading (ESTIMATE): the kernel agrees with R1 as R1 converges. The failures come from R1's discretisation and its known
gauge breakdown, plus a few events with per-event sensitivity at grazing crossings. The pass criterion is unchanged
and V4 stays FAIL; it does not gate.

## 5. State of the production setup (ready, not launched)
**Code** (`sim/stage3/code/`; `code/T3_causal.py` untouched):
- `T3_causal_s3.py`, kernel s3.2. It contains the plan §4.1 items 1-7: generic surfaces with all roots, hit 4-momenta,
  vertex, disc material, the vacuum fast path, the s3 defaults and `legacy=True`.
- s3.2 = s3.1 plus a binary-search candidate-surface lookup in the recorder. s3.1 cost 142-146 ns/step against 65-70
  for T3_causal (B config); s3.2 costs 74 ns/step. Outputs are bit-identical to s3.1 (verified on 23 job files).
- `surfaces_s3.json`: 93 surfaces (D111 simplified block, stacked OT sensors, TEDD PS/2S split, BTL, ETL proxy and 10
  virtual T3 barrel layers) and 22 disc-material slabs.
- `s3_physics.py`: analytic truth, plane fits, sensor dE.
- `run_stage3.py`: the runner (spawn-safe, atomic writes, restartable, per-event blake2b seeds, md5/platform/versions in
  every output, `run`/`status`/`smoke`/`check`, STOP file).
- `make_inputs.py`, `make_jobs.py`, `make_bundle.py`.

**Inputs** (`data/sim_stage3/inputs/`, 22 files, 7.3 MB): P2 693-802 events per file (300 template + 300 toy counted in
|eta| < 2.5), P1 325-400.

**Jobs** (`sim/stage3/jobs/`): 4098 jobs, 218 571 events, **402 CPU-h** (ESTIMATE in M3 units, from the probe cost
model; s3.2 runs at 0.86x the estimate on the V2b jobs).
- `mac.json`: 3616 jobs, 148 CPU-h (P1 41, P2 <= 10 keV 63, MV 44.5). About 21 h on 7 workers.
- `pc.json`: 482 jobs, 253 CPU-h, 63.0 % (every P2 job at Lambda >= 15 keV, 230.5 CPU-h, plus the 29 most expensive MV
  jobs). About 19 h at 14 workers if the PC runs at about 1.9x the Mac (ESTIMATE, unmeasured).
- `overlap.json`: 3 cheap clones (P1 E500 1 keV B, P2 E500 1 keV BM, P2 E1000 3 keV BM) that run on both machines.
- The 120 V2b jobs (P1 B/B2 at 0.6/1/2 keV) are already done and sit in `data/sim_stage3/out/p1/`; a Mac run skips them.

**Bundle**: `data/sim_stage3/bundle/quirks_sim/` (36 files, 7.9 MB, MANIFEST.json with md5s).
- Contents: code, all inputs, pc/overlap/smoke job lists, `RUN.md` (exact PowerShell commands),
  `PROMPT_FOR_CLAUDE.md`, the updated `SETUP_WINDOWS.md`, and `env/` unchanged.
- Verified in a scratch copy: `pixi install` from the bundle's own env (osx-arm64, numpy 2.5.4, numba 0.68.0), then the
  smoke test PASSED in 36 s, with output bit-identical to the TT env.

**If the user decides to proceed** (two commands from `theory_track/`):

    pixi run python sim/stage3/code/make_bundle.py usb /Volumes/J8A/quirks_sim
    nohup nice -n 10 caffeinate -i pixi run python sim/stage3/code/run_stage3.py run --jobs sim/stage3/jobs/mac.json sim/stage3/jobs/overlap.json --workers 7 --inputs data/sim_stage3/inputs --out data/sim_stage3/out > data/sim_stage3/out/run_mac_stdout.txt 2>&1 &

Then follow RUN.md on the PC.

## 6. Decision needed from the user
1. Treat V2b as the physics finding it is: the per-event c law holds on typical events (paired <= 1 %; k_B < 6 subset
   <= 1.5 %), but the population-median statement P-10 ("<= 1.5 %") fails on the MG sample by +2.0 / +2.1 / +3.2 % at
   E 500 / E 1500 / Etilde 500. The same +2.4 % offset is in the Stage-1 data. Then:
   - (a) **proceed with production** as planned (the simulation itself does not depend on the c law) and revise P-10
     in the theory documents to "per-event (paired) agreement <= 1 %; population-median excess +1-3 % on the MG
     sample"; or
   - (b) investigate first, for example with more events per point, the k_B >= 6 population with the c14/B* tools, or
     the 2-5 keV P1 points, before any production.
2. Note V3: 2 literal cell failures, both B-only quantities at max_boost 1e-2 (3 keV Delta_s +1.8 % at 1000 GeV;
   30 keV in-plane 5.5 um, which is floor dominated). The production hit positions are converged (§3). Keep D8, or run
   P2 at 2-5 keV with 1e-3 (cost x10 at those points; "about +5 CPU-h" was written here, an arithmetic error: the real
   cost is about +96 CPU-h, see §7).
3. Note V4: the literal R1 criterion fails because R1 at N = 256 is not converged and has gauge breakdowns. Accept the
   N >= 1024 diagnostic, or run the Stage-1 `nm_conformal` (status-7 abort) cross-check.

## 7. User decision (2026-10-11, via the coordinator) and what was done
- **Approved: go past the gate.** V2b is recorded as a **finding**: per-event agreement <= 1 % (paired median),
  population-median excess +1-3 % on the MG sample (E 500 +2.0 %, E 1500 +2.1 %, Etilde 500 +3.2 % at 1 keV; not a step
  effect). P-10 will be revised later through review; `analytic/` is not edited now.
- **V3:** P2 at 2-5 keV now runs at max_boost 1e-3 (`make_jobs.mb_p2`). The MV points at 3 keV moved with it, for
  consistency with nominal P2. **Cost correction:** this adds about **+96 CPU-h** (total 402 -> 498 CPU-h, ESTIMATE),
  not the +5 CPU-h written in §6, which was an arithmetic error. Most of it is the 5 keV P2 points: 17 species-masses
  x about 460 events x about 25 s per event. Reverting only 5 keV to 1e-2 would save about 60 CPU-h (RUNNING.md).
- **V4: accepted** with R1 at N = 1024/4096 as the independent-solver cross-check. Median Delta_s ratio 1.0003-1.0011
  in all 3 sets; events with matching hit counts agree to 0.1-2 um, with two stable per-event outliers (ratio 0.952 /
  12.6 um; 76 um). N = 256 is not converged. The literal N = 256 criterion is recorded as failed and superseded by this
  decision.
- **PC constraint:** 10 workers at below-normal priority. The split was rebalanced with R = PC/Mac = 1.4 (ESTIMATE;
  `jobs/split_summary.json`).
  - Mac: 3986 jobs, 207 CPU-h remaining (120 V2b jobs already done).
  - PC: 590 jobs, 290 CPU-h (every Lambda >= 15 keV job plus 137 MV jobs).
  - Overlap: 3 jobs.
  - About 30 h on each machine.
- **Bundle:** written to the USB `/Volumes/J8A/quirks_sim`, 36 files, md5-verified against MANIFEST.json. env/ is
  byte-identical, so no pixi reinstall is needed. A copy of the USB passed the smoke test, and no `._` or `.DS_Store`
  files remain.
- **Mac production:** launched 14:19:38 -05, PID 42898 (RUNNING.md).
