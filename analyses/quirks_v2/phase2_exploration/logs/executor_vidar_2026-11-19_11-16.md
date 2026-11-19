# Vidar (executor, Opus) — C1-c container recipe + one job rerun — 2026-11-19

- 11:16 Read AGENT_RULES, Rosalie's plan (C1-c item), campaigns. Runtime check on the workers: no apptainer /
  singularity / podman; docker 29.9.3 on landau, maxwell, schrodinger, user jdochoa in group docker (no sudo needed).
  The pinned base `ubuntu@sha256:2198e4c6…` is NOT in the docker image store of any worker (it lives in the
  containerd k8s.io namespace, socket not readable). Local `ubuntu@sha256:e9569c25…` (22.04.3, glibc 2.35) is present
  on maxwell and schrodinger → used with --pull=never (no Docker Hub traffic). Logged as DECISION in experiment_log.
- 11:16 Job chosen: p2-a-c1-cp0 / c1cp0-gamma-001 (C'_0 gamma gun, 25000 events, 68.8 CPU-s, landau, done marker
  sha256 0028fefeb7e4…). Code (acts/, phase2_exploration/src) unchanged since 2026-11-16 15:07 (< run at 17:25).
  Expectation noted BEFORE running: the npz carries meta_json with created_utc, wall_s, cpu_s_tt, hostname and the
  zip member timestamps, so a byte-identical file is unlikely even on the host; the frozen criterion is applied as is.
- 11:17 Recipe committed (26f4abe). `ssh maxwell build.sh` REFUSED by the permission system → stopped, no workaround. Artifact written, slots released. C1-c NOT TESTED.
