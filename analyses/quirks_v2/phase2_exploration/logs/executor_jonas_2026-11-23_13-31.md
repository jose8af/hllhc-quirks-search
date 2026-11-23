# Session log: Jonas (executor, Opus), D2 "later arcs restored" completion — 2026-11-23

Successor of Ulrika (session died in the 19 Nov 17:54 power loss). Plan: outputs/D2_PLAN_ulrika_2026-11-19.md (frozen, not changed).

- 13:31 -0500 started. Read AGENT_RULES, PHASE2_BRIEF, D2 plan, Ulrika's log and experiment_log entry (19 Nov 11:26),
  p2u_d2_{chain,find,sum}.py, campaigns tools/runner/examples/d2/*.json, LOG.md 23 Nov 13:30.
  State 13:30 [V: markers]: p2-c-d2-find 28/60 done; 0014-a/b 'lost' (landau, power loss), 0015-a/b started 13:25 on maxwell;
  driver on einstein (pid 33544, driver.json todo 30, caps maxwell 2). Background wait on the markers started (exits at 60 done,
  any 'failed', or driver not running).
- 13:33 -0500 acceptance checks not involving r (scripts /var/tmp/jdochoa/jonas_d2/check_ctl_chain.py, check_dz.py, run on maxwell nice 19, seconds):
  control p2-c-d2-ctl-{a,b} vs c1pu1-0000: 80 trials, all 31 per-trial arrays equal (n_grp, n_pass, n_pass_T, n_grp_T 43 cols, seeds, PV, phimet, ...)
  except trials.times / t_total (timings) and dz_nearest_pu (|diff| ≤ 3e-6 mm: uz rounded to 1e-6 in the dump path; diagnostic only) [V].
  chain 30 files / 600 events: V4-1 ok all; nominal_match_all FALSE: 9 events (not 8 as Ulrika's log says) differ by ±1 written
  hit (6 events −1, 3 events +1); injected written measurements 10,777,255 vs injected SimHits on written surfaces 10,777,258:
  the 3 missing ones = the 3 "+1" events (an injected measurement not recognised by truth position and counted as nominal part).
  Effect on the finder input: 3 injected hits missing in 10.8 M (finder uses the dumps for the nominal part) [V]. Negligible.
  CPU so far (markers, dedup on campaign/job/attempt, script /var/tmp/jdochoa/jonas_d2/cpu.py): chain 29,415 s, ctl 893 s,
  smoke 244 s, find 28 done 12,791 s (457 s/job) [V].
- 13:34 -0500 orchestrator message: worker DNS fixed; p2-c-d2-find driver moved to maxwell (pid 163711, log
  maxwell:/home/scratch/jdochoa/drivers/resume_d2_find.log), einstein driver stopped. Checked: driver.json host maxwell,
  status running, 29 done; 0014-a re-dispatched to maxwell 13:34:18. My marker watcher still running. p2-c-d2-sum driver may run on a worker.
- 15:25 -0500 p2-c-d2-find 60/60 done (qv2run status; driver on maxwell finished 15:25:09). SLOTS line written; p2-c-d2-sum launched
  15:25 on maxwell (driver on maxwell, --max-per-node 1, log maxwell:/home/scratch/jdochoa/drivers/p2-c-d2-sum.log); done 15:27
  (13 CPU-s, 96 s wall).
- 15:28 -0500 read: r = 0.766 / 0.759 / 0.720 at R04/R05/R06, paired σ(ln r) 0.003 / 0.004 / 0.061, trend z −1.02; re-derived with
  /var/tmp/jdochoa/jonas_d2/rederive.py (identical B, r; widths agree). Verdict "effect, robust", r(R06) < 1: no correction.
  CPU total 15.83 CPU-h measured [V], + ≤ 0.06 lost attempts [E].
- 15:29 -0500 wrote outputs/D2_RESULT_jonas_2026-11-23.md, experiment_log entry, DAILY_NOTES lines. Committing my files.
