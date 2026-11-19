# C1-c — container recipe and one C1 job rerun (Vidar, 2026-11-19 11:17 -0500)

Commitment C1-c (COMMITMENTS.md l.170): tracked lockfiles, container recipe, jobs ≤ 30 min through the resumable
runner. Frozen verification (STR §4.1): one C1 job rerun in the container with an identical output hash.

**Verdict: NOT TESTED.** The recipe is written and committed; the image build was refused by the permission system
(Claude Code auto-mode classifier, "Unauthorized Access") on the `ssh maxwell … build.sh` call at 11:17. Per the task
rules no workaround was attempted. No image exists, no rerun ran, no hash was compared.

## 1. Container runtime on the workers [VERIFIED, ssh landau/maxwell/schrodinger 11:12]
- apptainer, singularity, podman, buildah, charliecloud, enroot, udocker: absent on all three.
- docker 29.9.3 (buildx v0.39.0) on all three; user jdochoa is in group `docker` (gid 998): no sudo, no install.
- containerd socket (`ctr`, `crictl`): permission denied.
- Pinned study image `ubuntu@sha256:2198e4c6…` is **not** in the docker store of any worker (it is only in the
  containerd k8s.io namespace used by Argo pods). The docker stores hold `ubuntu:latest` =
  `ubuntu@sha256:e9569c25…` (22.04.3, glibc 2.35, created 2024-01-25) on maxwell and schrodinger, and
  `ubuntu@sha256:f9d633ff…` on landau.

## 2. Recipe (commit 26f4abe) — `tools/container/qv2-c1/`
- `Dockerfile`: FROM `ubuntu@sha256:e9569c25…` (local, `--pull=never`/`--pull=false`, no Docker Hub traffic);
  uid/gid 10015:10000 as on the hosts; host CA bundle copied (no apt); pixi 0.84.2 binary pinned by sha256
  `32523b4d…46bff0c` [VERIFIED, sha256sum]; `pixi install --frozen` from the tracked `envs/tt/pixi.lock` and
  `acts/pixi.lock` at their host absolute paths; then the code of one commit (`git archive`, ledger excluded,
  ≈ 29 MB). glibc 2.35 ≥ 2.34 required by the pyacts 48.0.0 wheel [VERIFIED, `ldd --version` in the base image].
- `build.sh [COMMIT]`: worker only; checks the base image is local and the pixi hash/version; build tree in
  `/var/tmp/jdochoa/qv2-ctr/ctx-<sha12>`; tags `qv2-c1:<sha12>` with the commit as OCI revision label.
- `ctr_exec.sh IMAGE CMD`: runner job command wrapper: `docker run --rm --network none --user 10015:10000
  --memory 2250m (no swap) --cpus 1`, only `/home/scratch/jdochoa` mounted, QV2_* runner variables passed through,
  nice 10 inside, `docker kill` on TERM; prints the container's CPU times and `memory.peak` (the runner's own
  cpu_s / max RSS would measure only the docker client).

## 3. Job chosen for the rerun (not run)
p2-a-c1-cp0 / c1cp0-gamma-001 (C'_0 gamma gun, 25,000 events, 68.8 CPU-s, 327 MB RSS, landau; done marker output
`c1cp0-gamma-001.npz`, 2,686,201 bytes, sha256 `0028fefeb7e4…`) [VERIFIED, ledger/markers/p2-a-c1-cp0/000/].
Code under acts/ and phase2_exploration/src last changed 2026-11-16 15:07, before that run (17:25) [VERIFIED, git log].
Planned: campaign p2-a-c1-ctr (one job, same id and arguments, command wrapped by ctr_exec.sh), SSH runner on
maxwell, `--max-per-node 1`.

## 4. Expected outcome, stated before any run (for whoever runs it)
The output npz is written by `run_g1b.finish` (acts/stage4/run_g1b.py:206–216) with `meta_json` containing
`created_utc`, `wall_s`, `cpu_s_tt`, `env.hostname` (run_stage4.env_info, l.248–251), and `np.savez_compressed`
stamps zip member times. The file sha256 will therefore differ from the original on **any** rerun, container or
host, so the frozen criterion as written cannot pass [ESTIMATE, from code reading; not run]. Under the rule "report
FAIL, do not tune", the first differing field would be expected in `meta_json`. A content-level comparison (all
arrays except meta_json) would be the informative DIAGNOSTIC; whether to amend the criterion is a question for the
orchestrator / user.

## 5. Open issues / questions
1. Permission for the docker build (and the rerun) on maxwell: needs the user's approval in the permission system.
2. Base-image deviation: the binding rule names `ubuntu@sha256:2198e4c6…`, which docker cannot see; the recipe uses
   the local `e9569c25…` with no pull. Accept, or provide a way to load the pinned image into docker.
3. The frozen "identical output hash" criterion is unattainable because of timestamps/hostname in the output (§4).
4. The install slot booked in SLOTS.md at 11:16 is released (11:17); nothing of mine runs.
