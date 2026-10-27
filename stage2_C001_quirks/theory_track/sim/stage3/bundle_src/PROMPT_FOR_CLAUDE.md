# Prompt for a Claude Code session on the Windows PC

First copy the bundle to `C:\quirks_sim` (RUN.md step 1). Then open PowerShell, run `cd C:\quirks_sim; claude`, and
paste everything below the line.

---

You are operating a long batch physics simulation on this Windows PC (AMD 7800X3D, 8 cores / 16 threads, win-64). The
job bundle is in `C:\quirks_sim`; it was prepared and validated on a Mac, which runs the other half of the same job grid
at the same time. Your job: **set up, smoke-test, launch, and then check progress about once per hour, cheaply**. The
user works on this PC at the same time, so the run uses **10 workers at below-normal priority**.

## Hard rules
1. **Never edit** `C:\quirks_sim\code\T3_causal_s3.py`, `code\s3_physics.py`, `code\surfaces_s3.json`, anything in
   `inputs\` or `jobs\`. The physics and the job split must match the Mac's.
2. Only Windows-specific runner problems may be fixed: paths, process start, file locking, encoding, priority. Make the
   fix in `C:\quirks_sim\code\run_stage3.py` only if the run cannot work otherwise, and never change the arithmetic,
   seeds, job definitions or output arrays. Log every change in `C:\quirks_sim\CHANGES_ON_PC.md`: date and time, the
   exact diff, the reason, and the error text that forced it. Rerun the smoke test after any change.
3. **Ask the user before anything else**: installing software, changing power settings, changing the worker count,
   deleting outputs, or any workaround not covered by rule 2.
4. **Keep token use low.** Use only the `status` command and the last 3 lines of the logs. Never print or read whole
   output files, the `out\*.npz` data, or the job lists. Each hourly report is at most 3 lines.
5. Never use the GPU, and never raise the worker count above 10 unless the user asks.

## Steps
1. Read `C:\quirks_sim\RUN.md`; it has the exact commands for every step below.
2. Environment (pixi is already installed): run the RUN.md step 2 commands. Expect `0.68.x 2.5.x`.
3. Smoke test (RUN.md step 3, about 2 minutes): it must end with `SMOKE PASS`. If it fails and the cause is
   Windows-specific in the runner, fix it under rule 2. Otherwise report the error text to the user and stop.
4. Check that sleep is off: run `powercfg /query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE` and look at the AC setting. If
   it is not 0, ask the user to allow `powercfg /change standby-timeout-ac 0`, or to set "Never" by hand.
5. Launch detached (RUN.md step 4, `$N = 10`, which gives `--workers 10 --low-priority`). After about 2 minutes, confirm
   with the RUN.md step-5 `status` command and `Get-Content C:\quirks_sim\out\run_stdout.txt -Tail 3`. The start line
   must say `593 jobs listed ... 10 workers`. Tell the user it is running.
6. **Hourly checks.**
   - If your Claude Code has the `/loop` command or a scheduled wakeup, set a check every 60 minutes, for example
     `/loop 60m Check the quirks_sim run: status + last 3 log lines, report in <= 3 lines`.
   - If you cannot schedule yourself, ask the user to send you a short message such as "check" about once per hour.
   - Each check runs only:

         pixi run --manifest-path C:\quirks_sim\env\pixi.toml python C:\quirks_sim\code\run_stage3.py status --jobs C:\quirks_sim\jobs\pc.json C:\quirks_sim\jobs\overlap.json
         Get-Content C:\quirks_sim\out\run_stdout.txt -Tail 3

     and also `Get-ChildItem C:\quirks_sim\out\_errors_*.log -ErrorAction SilentlyContinue` (it must list nothing).
   - Report in at most 3 lines: jobs done/total, ETA, and failures (none, or which).
7. **If something is wrong:**
   - Is the run dead? If `status` shows no progress for more than 2 hours and no `python.exe` from
     `C:\quirks_sim\env\.pixi` is running, relaunch with RUN.md step 4. That is safe, because finished jobs are skipped.
   - Errors in `_errors_*.log` or `run_stderr.txt`: read only the last traceback (`Get-Content <file> -Tail 30`). Fix
     the cause only if it is Windows-specific and in the runner (rule 2, log it). Otherwise tell the user with the error
     text and ask.
   - The user wants the PC lighter or faster: use RUN.md step 6 (stop with `out\STOP`, wait until it has ended,
     relaunch with a different `$N`), only when the user asks.
8. **When `status` shows 593/593 done:** run the `check` command (RUN.md step 7); it must report 0 invalid, 0 missing.
   Then copy `C:\quirks_sim\out` to the USB as `<USB>:\quirks_sim\out_pc` with the RUN.md step-7 robocopy commands,
   together with `CHANGES_ON_PC.md` if it exists. Ask the user to plug in the USB first. Finally, tell the user that
   it is finished and that the USB can be ejected and returned.

## Context (for understanding only)
- Physics: classical Nambu-Goto quirk strings propagated through the CMS Phase-2 tracker (B field and material, truth
  level). It is a sequential numba kernel, so the GPU is useless.
- Each job writes one file `out\<campaign>\<species>_m<mass>\L<Lambda>_<config>_c<chunk>.npz`, atomically (a
  `.tmp<pid>.npz` file, then a rename; leftover tmp files are removed at the next launch).
- Expected run time: about 30 h with 10 workers (ESTIMATE, 22-40 h). The longest jobs, up to about 1.5 h each, run
  first, so the job count rises slowly at the start.
- The 3 overlap jobs also run on the Mac, for a statistical cross-check; ARM and x86 results are not expected to be
  bit-identical.
