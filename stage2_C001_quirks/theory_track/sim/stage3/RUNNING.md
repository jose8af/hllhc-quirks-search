# Stage 3 production: what is running (E7, 2026-10-11)

The user approved going past the V2b gate (VALIDATION_GATE.md §7). The job list was regenerated with P2/MV at
max_boost 1e-3 up to 5 keV (V3 follow-up) and re-split for the PC at 10 workers.

## Mac (Apple M3, this machine)
- **Launched:** 2026-10-11 14:19:38 -05, **PID 42898** (top process, `$!` of the launch, parent 1 = detached).
  Children: 42900 (the caffeinate sleep assertion) and **42905** (the python runner), which spawned 7
  `multiprocessing.spawn` workers.
- **Confirmed running** at 14:23 (4 min): 7 workers at about 690 % CPU in total, start line `3989 jobs listed, 120
  already done, 3869 to run, 7 workers; est 207.0 CPU-h`.
- **Command** (from `theory_track/`):

      nohup nice -n 10 caffeinate -i pixi run python sim/stage3/code/run_stage3.py run --jobs sim/stage3/jobs/mac.json sim/stage3/jobs/overlap.json --workers 7 --inputs data/sim_stage3/inputs --out data/sim_stage3/out > data/sim_stage3/out/run_mac_stdout.txt 2>&1 &

- **Work:** mac.json has 3986 jobs and overlap.json 3. Of these, 120 jobs (the V2b P1 subset) were already done and are
  skipped. The remaining work is **207 CPU-h** (ESTIMATE, M3 units).
- **ETA:** about **30 h** on 7 workers, i.e. around 2026-10-12 20:00 -05. Kernel s3.2 ran at 0.86x the estimate on
  the V2b jobs, which would give about 25 h; the cost model is about ±25 %. The expensive jobs (P2 5-10 keV) run first.
- **Status** (cheap, any time, from `theory_track/`):

      pixi run python sim/stage3/code/run_stage3.py status --jobs sim/stage3/jobs/mac.json sim/stage3/jobs/overlap.json --out data/sim_stage3/out
      tail -3 data/sim_stage3/out/run_mac_stdout.txt

- **Graceful stop:** `touch data/sim_stage3/out/STOP` (no new jobs start; running jobs finish, at most about 1.5 h).
  To resume, `rm data/sim_stage3/out/STOP` and rerun the command; finished jobs are skipped.
- **Hard stop:** `pkill -P 42905; kill 42905 42898` (workers, then the runner and the top process). Check with
  `pgrep -fl multiprocessing.spawn` that no worker remains. Partial jobs leave only `*.tmp*.npz`
  files, which are removed at the next start.
- **Keep the MacBook on power with the lid open.** `caffeinate -i` prevents idle sleep, not lid-close sleep.
- **Outputs:** `data/sim_stage3/out/{p1,p2,mv,xover}/...`; progress log `data/sim_stage3/out/_progress_<host>.jsonl`;
  errors `data/sim_stage3/out/_errors_<host>.log`.

## Windows PC (AMD 7800X3D), run by the user
- **USB bundle:** `/Volumes/J8A/quirks_sim`, 36 files, 8.0 MB, MANIFEST md5-verified; env/ is unchanged, so no
  `pixi install` rerun is needed.
- **Work:** pc.json has 590 jobs (every P2 job at Lambda >= 15 keV, 453 jobs / 230.5 CPU-h, plus 137 MV jobs) and
  overlap.json 3. That is **290 CPU-h** (ESTIMATE, M3 units).
- **Settings:** `--workers 10 --low-priority` (the user works on the PC at the same time).
- **ETA:** about **30 h**, assuming PC(10 workers) = 1.4x Mac(7 workers) (ESTIMATE, unmeasured; range 22-40 h).
- **Instructions:** RUN.md (exact PowerShell commands) or PROMPT_FOR_CLAUDE.md (hourly checks).
- **When finished:** results come back on the USB as `quirks_sim/out_pc/`. Merge them into `data/sim_stage3/out_pc/`
  (keep them separate: the xover/ jobs exist on both machines).

## Split rule (`jobs/split_summary.json`)
- PC share = R/(1+R) of the remaining work with R = 1.4, which gives 58.4 %.
- Both machines are then estimated at about 29.6 h.
- Every Lambda >= 15 keV job stays on the PC, because that still balances.
- **Refine after about 3 h:** compare the job wall/estimate ratio in the two `_progress_*.jsonl` files. If the PC is much
  slower or faster, move unstarted jobs: regenerate with a different R_PC in make_jobs.py, then restart both runners.
  Finished jobs are skipped.

## Cost note (correction)
VALIDATION_GATE.md §6 estimated "+5 CPU-h" for running P2 at 2-5 keV with 1e-3. That was an arithmetic error. The
regenerated job list costs **+96 CPU-h**:
- 402 → 498 CPU-h in total;
- most of it from the 5 keV P2 points (17 species-masses × about 460 events × about 25 s per event at 1e-3), plus the
  3 keV MV points, which were also moved to 1e-3 for consistency with nominal P2.

To revert only the 5 keV points to 1e-2 (saves about 60 CPU-h), change `mb_p2` in make_jobs.py, regenerate, and restart
the Mac runner. The 5 keV jobs are all in mac.json.
