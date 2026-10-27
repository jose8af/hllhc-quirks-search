# E7 executor session log: Stage 3 production (2026-10-11)
- Read plan.md (all), probes p0-p7, T3_causal.py, T3_propagator material model, mg_events.py, Stage-1 M3/FU scripts and JSON,
  acts geometry JSON, USB env (pixi.toml/lock, SETUP_WINDOWS.md). User approved all D1-D16 as recommended.
- Code written: code/{make_surfaces.py, surfaces_s3.json (93 surfaces, 22 disc slabs), T3_causal_s3.py (s3.1), s3_physics.py,
  run_stage3.py, make_inputs.py, make_jobs.py}; validation/{vcommon.py, val_v1.py}.
- V1 PASS: 240/240 runs (20 MG ev x V/B/BM/M x 0.6/3/10 keV) bit-identical to code/T3_causal.run_causal (hits, status,
  nsteps, X, P, eacc). V1b(a) PASS: legacy barrel hits reproduced on T3V surfaces to 1.1e-13 cm, 0 missing, 0 extra (180 runs).
  V1b(b) PASS: 431 vacuum hits (298 on discs) within 2.4e-4 cm of ExactPair; per-surface crossing counts = independent
  numpy scan (0 mismatches). results/V1.json.
- Inputs extracted (data/sim_stage3/inputs, 22 files): p2 693-802 ev/file (300+300 counted in |eta|<2.5), p1 325-400.
- make_jobs: 4098 jobs, 218571 events, 402 CPU-h (ESTIMATE, M3 units): mac 148 / pc 253 (63.0 %), overlap 3 jobs.
- Kernel s3.2 (11:23): the s3.1 recorder (93 surfaces looped every step) cost 142-146 ns/step vs 65-70 legacy (B config);
  s3.2 = binary search of candidate surfaces, processed in table order -> 74 ns/step, outputs bit-identical to s3.1
  (2 test jobs + 21 archived s3.1 V2b files, 0 differing arrays). s3.1 V2b outputs archived in data/sim_stage3/validation/v2b_s31.
- V8 PASS (ACTS env, pyacts 48.0.0) on the Mac smoke P2 output: 430/430 physical hits isOnSurface (1 um), 573 SimHits ->
  573 measurements (generic 2D smearing re-keyed to the Stage-3 surfaces), t >= r/c for all hits.
- Bundle staged in data/sim_stage3/bundle/quirks_sim (36 files, 7.9 MB); verified in scratch: pixi install (osx-arm64,
  numpy 2.5.4) + smoke PASS, outputs bit-identical to the TT env. NOT copied to the USB (gate).
- V2b (11:34) GATE FAIL as pre-registered (difference of population medians, |Dc| <= 2 sigma AND <= 1.5 %, all 5 points):
  F200 +0.70 % PASS, F500 +2.00 % (2.3 sigma) FAIL, F1000 +1.07 % PASS, F1500 +2.10 % (2.2 sigma) FAIL, S500 +3.15 % (2.4 sigma) FAIL.
  Paired median(c2 - c_ev) at 1 keV: -0.0010..+0.0005 (all points). STOP: production not launched, USB not written.
  Diagnostic V2b_diag (1e-4 steps, F500/S500) and the validation chain (V2a, V1 rerun on s3.2, V4, V6, V3) still run.
- V2a PASS after matching FU_analysis's exclusions (status != 1 events; NaN==NaN): 960/960 Delta_s bit-identical, medians = FU.json.
- V1 rerun on s3.2 PASS (240/240). V6 PASS (50 jobs, 4329 events; the first comparison flagged NaN ds_barrel as different
  -> fixed to equal_nan). V4 FAIL literally (R1 N=256 unconverged, gauge breakdowns); diag N=1024/4096 median ratios
  1.0003-1.0011. V2b_diag: max_boost 1e-4 changes median c2 by -1.8e-5 / -1.5e-5 -> the V2b excess is not numerical.
- V3 (8.0 CPU-h): hits converged at all production settings except 2 B-only cells (3 keV ds +1.8 % at 1e-2, 1000 GeV;
  30 keV in-plane 5.5 um); replica floor spread 1-7 % median at 10-30 keV; 3/1368 runs status 5.
- STOP per instructions: VALIDATION_GATE.md written; no production, USB untouched. LOG.md line appended.
- User approval (coordinator): proceed past the gate; V3 -> P2/MV 1e-3 to 5 keV (+96 CPU-h, my +5 estimate was wrong); V4
  accepted at N>=1024; PC 10 workers low priority. make_jobs: R_PC = 1.4 -> PC 58.4 %, mac 207 / pc 290 CPU-h remaining,
  ~29.6 h each. RUN.md / PROMPT_FOR_CLAUDE.md / SETUP_WINDOWS.md rewritten; bundle on USB (36 files md5 OK, env unchanged,
  dotfiles removed, USB-copy smoke PASS). Mac launched 14:19:38, PID 42898 (runner 42905), confirmed 7 workers busy.
