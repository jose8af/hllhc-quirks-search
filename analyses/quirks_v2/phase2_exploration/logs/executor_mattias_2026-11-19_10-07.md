# Executor Mattias — Phase 2, channel (i) successor of Ignatius (C1 final read)

Started 2026-11-19 10:07:04 -05 (`date`). Compute: landau slot B only (line in SLOTS.md before use). No new campaigns.
Read: AGENT_RULES.md; PHASE2_BRIEF.md; Ignatius's log (§2-3, successor section); Rosalie's successor section
(2026-11-17 08:15); SM_FIX_lisbet_2026-11-18.md; COMMITMENTS "Amendment E4"; LOG.md 2026-11-18 12:22-12:44.
Settled (not redone): rates 5/5, V4-5, C2-b, C2-c, stitch, SM family under E4.

## PLAN
1. c1_compare.py: joint-replica coherence for pu1, pu2, clos (T1, T1w, slope, c-factor). One set of event resamples
   (PUSamples bi1/bi2, nboot_v1 = 1000, the same that give the slope width) for all ten entries; nominal values
   recomputed from the per-event arrays and checked against the entries (raise on mismatch); individual entries
   unchanged; the frozen independent-entry coherence kept beside it. Synthetic tests in test_c1_compare.py; tests on
   landau; COMMIT code before any real run of these families; hash logged here.
2. C'_PU (7 entries) with the 54610b6 rule; disclose that Ignatius's 12:17 partial C'_PU file is superseded.
3. Full run (31 background entries) + c1_signal_compare.py open (4 entries); frozen vs amended verdicts.
4. outputs/EXPLORATION_i_mattias_2026-11-19.md with STATE FOR A SUCCESSOR; commit (no push).
CPU ESTIMATE: < 0.5 CPU-h (analysis runs only, nice 19 on landau).

## Log
- 2026-11-19 10:12:03 task 1 code: c1_compare.py pu_joint/pu_joint_reps/pu_joint_stats/cfac_event_arrays (joint replicas for pu1, pu2, clos on PUSamples bi1/bi2; nominal recomputed and checked against each entry; frozen independent coherence kept as frozen_script_independent; global block per family, cross-family correlation of T1 with pu1/pu2 not removed: FLAG). test_c1_compare.py TestPUJoint (3 tests: reproduces v1 trend_test slope and s_slope_boot to 1e-12, c_test c and s_c to 1e-12, nested-rung coherence width vs ensemble). landau: 14/14 pass (15.8 s wall, 5.7 CPU-s, 149 MB). No real data read by these families yet.
- 2026-11-19 10:12:08 task 1 COMMITTED 29079b758b2188d733a4b278fbdf736341fc2dfe (c1_compare.py sha256 90c02fde…5128, test a3fe41d0…97c1), before any real read of pu1/pu2/clos.
- 2026-11-19 10:17:34 full c1_compare run (commit 29079b7) on landau: 265 s wall, 29.8 CPU-s, 722 MB → outputs/c1_compare_mattias_2026-11-19.json. 31/31 entries pass individually (frozen and amended); families all coherent; no individual fail. Closure slope −0.36495 ± 0.0080 vs −0.3608 ± 0.0045, z −0.46 (partial +2.83): points ln_r almost unchanged (R04 0.398→0.401, R05 0.465→0.470, R06 −0.445→−0.444); the swing is the WLS weight of R06 (σ 0.0211→0.0190 from the pu2-prediction bootstrap, a different rng stream): full points with the partial's weights give −0.3338, partial points with the full weights −0.3646. Linear-fit χ² 685/1 dof: the 3 points are far from a line, so the slope depends on the weights by ≈ 4 × s_slope_boot. FLAG (diagnostic, no tuning).
- 2026-11-19 10:25:07 task 2 (C'_PU, rule of 54610b6): 7/7 pass, coherent z −0.31 (v1 width 0 −0.40); all N ≥ 10, no N < 10 branch; all gross checks only. Ignatius's 12:17 partial C'_PU file (1/√N, cppub ≈ 20/75) predates 54610b6: superseded.
- 2026-11-19 10:25:07 task 3 open signal tier (c1_signal_compare.py open, landau 331 s wall, 60 CPU-s): 4/4 PASS; E500_3 R04 61/200 vs 82/400 p 0.0082 (largest). Output outputs/c1_signal_open.json (--out ignored in open mode). Frozen-text: 34/35 (sm.R04 z +3.64, the FAIL on record, E4); amended 35/35.
- 2026-11-19 10:25:07 ledger rebuilt: C1 186.2 CPU-h / 198, C2 22.4 / 81. Task 4: outputs/EXPLORATION_i_mattias_2026-11-19.md written; committing.
