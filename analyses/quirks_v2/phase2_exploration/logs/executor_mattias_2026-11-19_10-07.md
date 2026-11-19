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
