# Status — quirks v2

**2026-11-13 (day 1).** Phase 1 (Strategy) started. No production yet; nothing runs before Gate A.

| | |
|---|---|
| Schedule | not yet approved (proposed at Gate A, after the cluster benchmarks) |
| CPU-h used / planned | 0 / to be set at Gate A |
| cajuela, this project | 0 GB of 1.5 TB soft budget |
| cajuela pool free | 3.9 TB of 4.5 TB |
| software area (`~/sw`, `~/.pixi`, `~/.cache/rattler`) | 0 GB of 150 GB |
| last repo bundle | `repo-2026-11-13.bundle` |

**Done today:** preflight (passed on re-run after the admin's cajuela fix), branch `v2-jfc`, JFC vendored, analysis
scaffolded, state and ledger files.

**Running:** six investigators (digests of the v1 study) and two feasibility executors (environments, generators,
runner, benchmarks on a worker).

**Open risks**
- The chain has never run on Linux; pyacts 48 may need a source build on a worker.
- Geant4 is not installed; route (conda-forge package or source build) decided by the feasibility executor.
- Cluster capacity is 12 worker cores, shared with lab users; the plan's 3–8k CPU-h are M3 units, not yet converted.
- cajuela: directories must never be renamed while in use (see `PREFLIGHT.md`).
