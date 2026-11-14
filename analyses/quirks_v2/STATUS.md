# Status — quirks v2

**2026-11-14 01:25 (day 1, night).** Phase 1 (Strategy): **stopped, waiting for the user** on two matters.

1. The Phase-1 review panel ran nine cycles without a PASS. The last verdict leaves one Category B item (one stale
   word in a table row) and thirteen wording edits; nothing about the design, budget or expected outcome is open.
   Gate A has not been reached. Draft package: `gates/GATE_A_DRAFT.md`.
2. Cluster fault since about 00:47: `/nfs/cajuela` hangs on einstein and ssh to the three workers hangs. Not repaired.

| | |
|---|---|
| Schedule | not yet approved (proposed at Gate A, after the cluster benchmarks) |
| CPU-h used / planned | 0 / to be set at Gate A |
| cajuela, this project | 0 GB of 1.5 TB soft budget |
| cajuela pool free | 3.9 TB of 4.5 TB |
| software area (`~/sw`, `~/.pixi`, `~/.cache/rattler`, envs in the repo tree) | about 10 GB of 150 GB |
| last repo bundle | `repo-2026-11-13.bundle` (13 Nov 14:37). **Overdue**: cajuela is not reachable |

**Done today:** preflight (passed on re-run after the admin's cajuela fix), branch `v2-jfc`, JFC vendored, analysis
scaffolded, state and ledger files.

**Running:** three feasibility executors, resumed after the incident, one per worker (chain benchmarks; generators;
runner validation). The six investigator digests are done.

**Incident 15:12:** einstein ran out of memory; the orchestrator and the three feasibility executors were killed and
cajuela was down until 15:20. State reconciled and committed; all environments verified complete except Geant4
(removed, to be reinstalled). Lost: about 25 minutes of executor work in progress, no data. New limits in force:
10 GB cap, nothing heavy on einstein, one pixi install at a time, at most 3 subagents.

**Open risks**
- Writing environments to the shared home from a worker is slow (~1 MB/s) and slows NFS for the lab. By user
  decision the Geant4 environment (3.3 GB) is installed on each worker's local scratch instead.
- The chain has never run on Linux; pyacts 48 may need a source build on a worker.
- Geant4 is not installed; route (conda-forge package or source build) decided by the feasibility executor.
- Cluster capacity is 12 worker cores, shared with lab users; the plan's 3–8k CPU-h are M3 units, not yet converted.
- cajuela: directories must never be renamed while in use (see `PREFLIGHT.md`).
