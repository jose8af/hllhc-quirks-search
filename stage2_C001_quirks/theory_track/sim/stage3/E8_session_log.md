# E8 executor session log: Stage 3 post-production (2026-10-13)
- Read executor.md, plan.md (all), VALIDATION_GATE.md (incl. §7), RUNNING.md, split_summary.json, code/*.py,
  predictions.json, NEAR_MISS §0/§8/§9. Production finished: Mac 120 (V2b) + 3869 jobs (29.68 h, 0 errors);
  PC two sessions (263 jobs, STOP-file stop; then 330 jobs, 9.14 h, **15 workers** in the 2nd session, not 10), 0 errors.
- Current code md5s (T3_causal_s3 62d0f76f, s3_physics ad364ec0, run_stage3 ab0a68cd, surfaces df914b36) = bundle MANIFEST.
- Analysis code goes to sim/stage3/scripts/ (plan §9 names); figures to sim/stage3/figures/.
- merge_index.py: PASS. 4582/4582 expected files (mac 3986 + pc 590 + 3 xover x 2), all valid, job definitions in the
  files = job lists, all code md5 = current (s3.2, r1.0), input md5 = inputs/, 0 duplicate events, extras only PC _smoke.
  Envs: Mac macOS arm64 numpy 2.5.3 numba 0.68.0; PC Windows-11 AMD64 numpy 2.5.4 numba 0.68.0 (python 3.12.15 both).
  CPU (per-event process time): Mac 207.5 CPU-h (est 208.4 M3), PC 375.5 CPU-h (est 290.1 M3 units -> PC/M3 per-core 1.29x slower).
  Status: Mac 85 x status 0 (t_end), 68 x status 4; PC 40 x status 4. No 3/5 (no reruns). -> V7 follow-up.
- extract.py: per-event summary tables data/sim_stage3/summary/events_{p1,p2,mv,xover_mac,xover_pc}.npz (7 s).
- xover.py: PASS. Kernel output bit-identical in 224/225 events (P1 E500 1 keV B 100/100; P2 E1000 3 keV BM 25/25;
  P2 E500 1 keV BM 99/100: 1 event nsteps +4, max hit shift 4.4 um, ds rel 6e-5, same status). Post-processing (numpy
  eigh plane fit) differs at <= 2.4e-4 relative (LAPACK, Accelerate vs OpenBLAS); truth closed forms at 1e-14; plane
  normal sign arbitrary. All KS p = 1.0, no median pull. PC outputs accepted.
- V9 (val_v9.py, 56 CPU-s): PASS. Weighted mode (first template rows, w_orig, Kish N_eff 173 of 200) vs unweighted
  production at E500 1 keV BM: pulls -0.28 (ds_all), 0.57 (ds_itps), 0.21 (ell_max), -0.48 (n hits), 0.02 (N_osc).
- V7 status-4 follow-up (val_v7_status4.py, 0.05 CPU-h): all 108 status-4 events (Mac 68, PC 40) reproduced bit-for-bit
  on the Mac (determinism; PC events reproduced on Mac). Label-swap rerun recovers 18/108 (status 1); 90 stay status 4.
  All have gamma* - 1 <= 0.0104 (median 0.003), material configs only (M/BM/x0.5/x2), early deadlock (no tracker hits),
  endpoints coincident: kernel limitation for near-threshold pairs with material. Excluded from summaries, listed.
- p1_model_mg.py: c06 rotating-yo-yo model on the 11000 P1 MG (event, Lambda) pairs (327 s; model only).
- V5 (val_v5.py, 0.23 CPU-h): (a) PASS: T2-cache draw regenerated identically (648 rows), 84 events x 4 configs through
  s3 legacy = stored T3_ms_thickness.npy bit for bit. (b) MG - cache median shifts mostly -10..-20 % (|pull| <= 2.5).
- P1 first pass (p1_results.py): V2b revisit over 30 cells: population excess +1.85 +- 0.19 % (weighted); reproduced by a
  c_ev-decile-stratified permutation of r (zero conditional-median heteroscedastic scatter) at 0.6-2 keV; at 3 keV
  (E1000/E1500/Etilde) and 5 keV (+9..+17 %) a real conditional excess growing with k_B (5 keV: +2 % at k_B<2 to +57 %
  at k_B>10), not concentrated at small b_odd/l0. -> diagnostic val_c5kev.py (1e-4 steps + floor replicas, ~0.9 CPU-h).
- V7 hits per layer: P1 BM 1 keV, hits per T3 barrel layer (both quirks) mean 2.18/2.41/2.99 (E200/500/1000), median 2.0;
  S-6 quoted ~3 at 1 TeV, 2.8-3.2 at 500 GeV (cache sample).
- p2_results.py (template half only, |eta|<2.5; toys untouched): closed-form edges reproduce plan §1.1 (N_osc=1 at
  0.28-0.33 keV; l_max=R_IT 0.43-0.78 E / 0.59-0.94 Etilde; l_max=100 um 16.3-29.6 E / 22.7-36 Etilde); hit-level thickness
  edge ds_all=100 um at 0.47-0.55 keV (flat in m); hit-level merging f(sep_IT<100um)=0.5 at 12.8-20.4 keV (E) / 17.7-25
  (Etilde) where >=15 keV points exist. f(no visible turn-around) found Lambda-independent (kinematic) -> dropped as edge.
  Systematics on edges: l_max +-5 % -> <= ~4 %; QED <= 0.9 %; scale/PDF/merging <= ~2-6 %; material <= 4 %.
- V-scale (val_vscale.py, seconds): 4/5 events PASS (max |dx| 0.27-1.6 um, Ds ratio 0.997-1.000); 1 event (row 268) has 2
  extra hits (grazing double crossing; legacy one-root recorder + unscaled hmax) -> Ds ratio 1.056: literal FAIL.
- val_c5kev.py (0.96 CPU-h): E1000 5 keV, 12 top-r k_B>=6 events: c2 ~0.3-0.5 vs c_ev ~0.065-0.07, unchanged at
  max_boost 1e-4 (median r 0.294 vs 0.275) and in round-off replicas (median spread 0.021) -> physical (B*), not steps/floor.
  k_B<2 controls: c2 within +-0.01 of c_ev (per-event noise ~10 % at 5 keV). Total small reruns ~1.3 CPU-h.
- val_v7.py: causality PASS (min t - d/c = +0.6 ps over 218k events); vacuum hits planar to <= 5e-5 um (SVD) but stored
  eigh thickness has a 0.015 um numerical floor -> literal V7 vacuum criterion (1e-3 um) fails on the stored value only;
  status-4 literal FAIL (108). Floor-flag fractions P2: 7 % (5 keV), 31 % (10), 53 % (15), 70 % (20), 86 % (30), 99.5 % (40).
- V8 rerun on production files (V8_production.json): all physical hits on surface, units OK, t >= r/c; generic smearing
  digitiser returns fewer measurements than SimHits at >= 10 keV (491/491 at 1 keV; 463/470 10 keV Mac; 442/472 15 keV PC;
  375/448 30 keV PC) -> Stage-4 open issue (repeated crossings of one sensor by one particle, hypothesis). V8.json kept
  = gate smoke result.
- Docs: PROPOSED_CHANGES.md (P-10 proposal), VALIDATION.md (§0 auto from results), README.md (auto results block),
  SAMPLES.md (generated), HANDOVER_STAGE4.md (schema, units, surface table ids 0-92, seeds, V8). make_docs.py regenerates.
  data/README.md updated; LOG.md line appended. Checked: no file written outside sim/stage3, data/sim_stage3, data/README.md,
  LOG.md. analytic/ and code/T3_causal.py untouched. DONE.
