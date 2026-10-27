# quirks_sim: Windows worker setup

This USB carries a self-contained job bundle for C001 quirks Stage 3: the string-simulation code (`code\`), the
pre-selected input events (`inputs\`), this PC's share of the job list (`jobs\`), the Python environment definition
(`env\`), and the run instructions (`RUN.md`; `PROMPT_FOR_CLAUDE.md` if you want a Claude session to drive it).

**Update (bundle complete):** pixi is already installed and you already ran `pixi install` from the earlier
`env\`-only USB. `env\pixi.toml` and `env\pixi.lock` are byte-identical to that copy, so **you do not need to
reinstall anything**. Go straight to `RUN.md`: step 1 copies the new folders with robocopy and keeps your installed
environment. Steps 1-2 below are only for a fresh PC.

The run uses **10 workers at below-normal priority** by default (about 62 % of the CPU), so you can keep working on the
PC. RUN.md step 6 explains how to change the worker count at any time.

## 1. Install pixi (required)
Open **PowerShell** (normal user, not admin) and run:

    powershell -ExecutionPolicy ByPass -c "irm -useb https://pixi.sh/install.ps1 | iex"

Close and reopen PowerShell, then check:

    pixi --version

## 2. Copy to the local disk and build the environment (required)
Do not run from the USB: FAT32 is slow, and pixi puts the environment inside the project folder.

    mkdir C:\quirks_sim
    $usb = (Get-Volume -FileSystemLabel J8A).DriveLetter + ':'
    robocopy "$usb\quirks_sim" C:\quirks_sim /E
    cd C:\quirks_sim\env
    pixi install
    pixi run python -c "import numba, numpy, scipy; print('numba', numba.__version__, 'numpy', numpy.__version__)"

You should see numba 0.68.x and numpy 2.5.x. The download is about 300 MB. The Mac uses numba 0.68.0, numpy 2.5.3
and Python 3.12.15; the bundle environment was also tested on the Mac (osx-arm64, numpy 2.5.4) before shipping.

## 3. Keep the PC awake (required for the run)
Settings → System → Power & battery → Screen and sleep → "When plugged in, put my device to sleep after": **Never**.
Or, in PowerShell:

    powercfg /change standby-timeout-ac 0

Also pause Windows Update restarts for the run (Settings → Windows Update → Pause updates, 1 week).

## 4. Optional: Claude Code on the PC
The run needs only a few commands (RUN.md), so Claude is not required. If you want a Claude session there to launch the
jobs, watch them and fix Windows-specific problems, install:
- Git for Windows: https://git-scm.com/download/win (Claude Code on native Windows uses Git Bash)
- Claude Code: in PowerShell, `irm https://claude.ai/install.ps1 | iex`, then `claude` in C:\quirks_sim

`PROMPT_FOR_CLAUDE.md` is the prompt to paste. A Claude session there spends your same account usage, but launching
and monitoring a detached job is cheap.

## Notes
- The 7800X3D has 8 cores / 16 threads. The run uses 10 workers at below-normal priority by default (RUN.md
  step 4); change it with RUN.md step 6.
- The GPU is not used: the string simulation is sequential and branchy, so it does not map to CUDA.
- Results go to `C:\quirks_sim\out\`, one file per job. A rerun skips finished jobs, so stopping and restarting is safe.
  When done, copy `out\` back to the USB as `out_pc\` (RUN.md step 7).
