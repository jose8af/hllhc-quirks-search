# quirks_sim: how to run the PC share of Stage 3 (Windows, PowerShell)

This bundle runs this PC's share of the C001 quirks Stage-3 string simulation:
- **590 jobs plus 3 cross-machine overlap jobs**, about **290 CPU-hours in Mac-M3 units**;
- by default, **10 workers at below-normal priority**, about 62 % of the 16 hardware threads, so you can keep using
  the PC;
- the expected run time is about **30 h**, finishing at about the same time as the Mac. This is an ESTIMATE with a
  range of 22-40 h: the PC/Mac speed ratio of 1.4 has not been measured, and the cost model is about ±25 %.

One job is one simulation chunk and writes one file to `C:\quirks_sim\out\`. Finished jobs are always skipped, so you
can stop, restart and change the worker count at any time without losing finished work.

Run every command below in **PowerShell** (normal user, not admin). Each command is one line.

## 0. Bundle layout
    env\        pixi.toml + pixi.lock (Python 3.12, numpy 2.5, scipy, numba 0.68) -- unchanged since the first USB
    code\       run_stage3.py (runner), T3_causal_s3.py (string kernel), s3_physics.py, surfaces_s3.json
    inputs\     22 event files (*.npz, 7 MB)
    jobs\       pc.json (this PC), overlap.json (3 jobs run on both machines), smoke.json (2-minute self-test)
    RUN.md, PROMPT_FOR_CLAUDE.md, SETUP_WINDOWS.md, MANIFEST.json (md5 of every file)

## 1. Copy from the USB to C:\quirks_sim
The USB volume is named `J8A`. Find its drive letter and copy everything (robocopy adds and updates files; it never
deletes your installed `C:\quirks_sim\env\.pixi`):

    $usb = (Get-Volume -FileSystemLabel J8A).DriveLetter + ':'; $usb
    robocopy "$usb\quirks_sim" C:\quirks_sim /E

The first command prints the letter (for example `E:`). If it prints only `:`, look up the USB letter in File Explorer
and set it yourself, for example `$usb = 'E:'`. robocopy exit codes 0-7 mean success.

## 2. Check the environment
pixi is already installed. `env\pixi.toml` and `env\pixi.lock` are byte-identical to the first USB, so the
environment you installed is still valid. `pixi install` only checks it and returns in a second:

    cd C:\quirks_sim\env
    pixi install
    pixi run python -c "import numba, numpy; print(numba.__version__, numpy.__version__)"

Expected output: `0.68.x 2.5.x`.

## 3. Smoke test (about 2 minutes, including the one-time numba compilation)
    pixi run --manifest-path C:\quirks_sim\env\pixi.toml python C:\quirks_sim\code\run_stage3.py smoke

The last line must be `SMOKE PASS ...`. If you see `SMOKE FAIL` or a traceback, stop and send the text to the person
who gave you the USB.

## 4. Launch the production run (detached: it keeps running after you close PowerShell)
    New-Item -ItemType Directory -Force C:\quirks_sim\out | Out-Null
    Remove-Item C:\quirks_sim\out\STOP -ErrorAction SilentlyContinue
    $N = 10
    $p = Start-Process -FilePath pixi -ArgumentList 'run','--manifest-path','C:\quirks_sim\env\pixi.toml','python','C:\quirks_sim\code\run_stage3.py','run','--jobs','C:\quirks_sim\jobs\pc.json','C:\quirks_sim\jobs\overlap.json','--workers',"$N",'--low-priority' -WindowStyle Hidden -RedirectStandardOutput C:\quirks_sim\out\run_stdout.txt -RedirectStandardError C:\quirks_sim\out\run_stderr.txt -PassThru
    $p.Id | Out-File C:\quirks_sim\out\launcher_pid.txt

- If PowerShell cannot find `pixi`, replace `-FilePath pixi` with `-FilePath "$env:USERPROFILE\.pixi\bin\pixi.exe"`.
- `--low-priority` runs the workers at below-normal priority. Your own programs always come first, and the simulation
  uses whatever is left.
- Each relaunch overwrites `run_stdout.txt`; the job progress is also kept in `out\_progress_<PC name>.jsonl`.
- The process survives closing PowerShell. It does not survive a reboot, sleep or logging off, so keep the PC awake
  (SETUP_WINDOWS.md step 3). After a reboot, simply launch again.

## 5. Check progress (cheap, at any time)
    pixi run --manifest-path C:\quirks_sim\env\pixi.toml python C:\quirks_sim\code\run_stage3.py status --jobs C:\quirks_sim\jobs\pc.json C:\quirks_sim\jobs\overlap.json
    Get-Content C:\quirks_sim\out\run_stdout.txt -Tail 3

- `status` prints the jobs done out of the total (593), the estimated CPU-hours done, the throughput and an ETA.
- The most expensive jobs run first (up to about 1.5 h each), so the first hours show few finished jobs, and the early
  ETA is rough.
- Task Manager should show about N busy `python.exe` processes.

## 6. Stop, resume, change the number of workers
- **Graceful stop** (running jobs finish, which can take up to about 1.5 h; nothing is lost):

      New-Item C:\quirks_sim\out\STOP

  The run has ended when `run_stdout.txt` shows `[run_stage3] finished: ...` and Task Manager shows no busy
  `python.exe`.
- **Resume:** run the step-4 block again. It removes the STOP file, and finished jobs are skipped.
- **Change the worker count** (for example, more while you are away, fewer while you work): stop gracefully as above,
  wait until it has ended, then run the step-4 block with a different `$N`. Use 4-6 to keep the PC light, or 14 when you
  do not need it; do not exceed 15.
- **Immediate stop** (only if needed: the jobs in progress are lost and rerun later):

      Get-CimInstance Win32_Process -Filter "Name='python.exe'" | Where-Object { $_.ExecutablePath -like 'C:\quirks_sim\env\.pixi\*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }

  This kills every Python process of this bundle's environment, i.e. the runner and its workers. Do not filter on
  `run_stage3`: the workers' command lines do not contain it.

## 7. When it is finished: check, then copy the results to the USB
`status` shows `593/593 done`. Validate every file, then copy the results to the USB (plug it in first):

    pixi run --manifest-path C:\quirks_sim\env\pixi.toml python C:\quirks_sim\code\run_stage3.py check --jobs C:\quirks_sim\jobs\pc.json C:\quirks_sim\jobs\overlap.json
    $usb = (Get-Volume -FileSystemLabel J8A).DriveLetter + ':'; $usb
    robocopy C:\quirks_sim\out "$usb\quirks_sim\out_pc" /E
    if (Test-Path C:\quirks_sim\CHANGES_ON_PC.md) { Copy-Item C:\quirks_sim\CHANGES_ON_PC.md "$usb\quirks_sim\" }

- `check` must report `0 invalid, 0 missing`.
- The output is about 0.5-1 GB in about 600 files; no file is near the FAT32 4 GB limit.
- Eject the USB from the tray icon before unplugging it, then give it back.

## Troubleshooting
- `out\run_stderr.txt` holds Python warnings and errors.
- `out\_errors_<PC name>.log` lists failed jobs with their traceback. A failed job is retried at the next launch.
- After sleep or a reboot, launch again (step 4).
- Do not edit `code\` (physics) or `jobs\` (the job split). The Mac runs the other half with the same code.
