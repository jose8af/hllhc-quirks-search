# FEAS_C — resumable job runner, Argo vs SSH, pyhf benchmark (session Boris, 2026-11-13)

Executor C of Phase 1 (feasibility only, no production samples). Plan: `plan_boris.md`. Numbers:
`benchmarks_runner.json` (machine-readable). Everything in the tests is **TEST ONLY**: outputs under
`data/feasibility/runner/`, markers under `outputs/feasibility/runner_ledger/markers/` (production
`ledger/markers/` untouched). Session interrupted once by the 15:12 einstein OOM incident; resumed 15:38 under the
revised rules (nothing heavy on einstein; drivers on workers; one marker file per job on NFS home).

## 1. Summary

- **Verdict: PASS.** `tools/runner/` (Python standard library only, run from the minimal pixi env
  `tools/runner/.pixi`, copied once per node to local scratch) provides campaign files, a job wrapper identical
  under Argo and SSH, a markers-only ledger, an Argo backend that writes §5.3 workflows, a resumable SSH backend, a
  bash watcher, and manifest, usage and bundle tools. 21 unit tests pass (run on landau).
- **Argo vs SSH (landau, quiet server, ~60 s CPU job, 3 runs each, one at a time):** CPU time identical
  (58.79 ± 0.10 s vs 58.95 ± 0.02 s). Overhead per job: **Argo 16.8 s, SSH 2.4 s**. The Argo overhead is ~5 s from
  pod start to wrapper start, ~1–2 s teardown, and a 10 s controller gap between pods. That is ~1% of a 30-min job.
  While the NFS server was saturated (14:59–15:09) the same test gave 44.4 s vs 23.3 s, dominated by Python import
  over NFS (10–25 s). That is now removed by a node-local interpreter cache: /home metadata calls per job start
  went from 687 to 28. (VERIFIED, R2)
- **Robustness:** I killed the driver, a single job (SIGTERM / kill -9), a pod (deleted), and the wrapper at each of
  four stages, and corrupted an output. Every case converged on resume with no stale `.part` files, scratch dirs or
  orphan processes. Files on cajuela are `10015:10000 644`; no directory was renamed. Memory limits (200 MB) are
  enforced under both mechanisms without disturbing the node. Cajuela/NFS I/O errors are retried with back-off;
  finished work is stashed, never discarded, and no marker is written for an unverified output. (VERIFIED, R3–R8)
- **Marker writes** (O_APPEND + fsync on the sync /home export): median 153 ms and max 560 ms with 12 concurrent
  writers. No consolidated collector is needed at the 12-job scale. (VERIFIED, R6)
- **pyhf** (toy, 31 parameters, landau, one core): fit 0.12 s, asymptotic CLs point 0.52 s, 20-point scan 10.4 s,
  1000 toys at one point 652 s; RSS ≈ 105 MB. (VERIFIED, R9)

## 2. Method

**Campaign file (JSON, stdlib, valid YAML for argo).** `campaign`, `tier` (final/regenerable/scratch/test),
optional `data_prefix`, `ledger`, `regenerate`, `expected_hours`, `defaults`, `jobs[]` with `id`, `shard`,
`command`, `outputs` (bare names), `max_rss_mb` (measured; request = it, limit = 1.5×), `cpu`, `timeout_s`
(≤ 1800). Validated: unique ids `[a-z0-9._-]`, outputs unique per shard, ≤ 10,000 per shard, markers never on
cajuela. Final dir `data/<prefix>/<campaign>/<shard:03d>/`, logs `logs/<prefix>/<campaign>/<shard:03d>/`.

**Wrapper (`bin/qv2-job` → `qv2run job`), identical in pods and over SSH.**
1. `bin/qv2-job` (bash) uses the node-local interpreter cache `/home/scratch/jdochoa/cache/runner/<stamp>/`
   (stamp = sha256 of env history + `qv2run/*.py`; built once under flock; temp dir renamed into place on local
   ext4; keeps 3 versions; falls back to NFS).
2. Idempotency: if the marker says `done` and every output has the recorded size and sha256, skip.
3. Node-local flock `/home/scratch/jdochoa/.locks/<job>.lock`. Stop orphan `qv2-<job>-*` systemd scopes of earlier
   attempts. Reuse a valid **stash** (command already finished, outputs hashed) or wipe scratch. Create the final dir
   under its final name, remove stale `name.part`, append `started`.
4. Run `bash -c COMMAND` in `/home/scratch/jdochoa/<job>` with niceness ≥ 10 and umask 022, in its own session.
   SSH: inside `systemd-run --user --scope -p MemoryMax=1.5×RSS -p MemorySwapMax=0 -p RuntimeMaxSec=timeout+60`.
   Argo: the pod's cgroup limit.
5. Accounting: `os.wait4` rusage (CPU = utime + stime; `ru_maxrss` over the child and its waited-for descendants,
   the same semantics as `/usr/bin/time -v`, which the pod image lacks). Pods also record cgroup `memory.peak`.
6. Limits: a 1800 s timer sends SIGTERM to the process group, then SIGKILL after 30 s. SIGTERM to the wrapper kills
   the group and records `killed`.
7. Success: hash the outputs in scratch → write the stash → per output copy to `<final>/name.part`, fsync, rename
   (`atomic_rename_file` refuses directories and cross-directory renames), re-read, verify sha256 → ship the job log
   to cajuela (`.part` + rename) → append `done` (outputs with path/sha256/bytes, CPU s, max RSS, wall s, node,
   mechanism, timings) → delete scratch.
8. Every cajuela and marker operation retries on OSError with back-off 5, 10, 20 … 120 s within 480 s
   (1800 + 480 < pod deadline 2400). If that is exhausted the job ends `io_error` (retryable) and keeps its stash.
9. Statuses: `done`; `failed`/`timeout`/`oom`/`verify_failed` (never retried); `killed`/`lost`/`corrupt`/`io_error`
   (retried ≤ 2×).

**Markers.** One JSON Lines file per job, `<ledger>/<campaign>/<shard:03d>/<job>.marker`, appended with O_APPEND +
fsync (single writer at a time; a torn last line is ignored). Completeness comes from markers only.
`rebuild-ledger` (one writer) writes `jobs.tsv` with one row per output.

**Argo backend.** `render` writes the §5.3 template exactly (unit-tested field by field): name
`jdochoa-qv2-<campaign>-c<k>-…`, labels `owner/study/qv2-campaign/qv2-chunk` on the workflow and pods,
`securityContext 10015/10000`, the three volumes at host paths, the pinned image with `IfNotPresent`,
`nice -n 10` + `umask 022`, requests cpu 1 + memory = RSS, limit 1.5×, `activeDeadlineSeconds 2400`, `retryStrategy
{limit 2, OnError}`, `podGC OnPodSuccess`, `ttlStrategy 86400`, ≤ 500 steps per workflow. There is one container
template per resource class, because templated quantities fail `argo lint`. Parallelism = min(12; 9 if
[now, now + expected_hours] touches a weekday 08–19 America/Guayaquil; Σ node caps). Node cap = 4, or 3 with a
graphical session (`who`: seat/`:N`/login screen), minus the rounded foreign load. Nodes with our SSH jobs are
excluded. Equal caps give a pooled workflow with node affinity; unequal caps give one pinned workflow per node with
its own parallelism. The driver submits chunk by chunk, waits (`argo wait`), and on restart finds our running
workflows by label. After each workflow it reconciles markers from pod status (OOMKilled → `oom`, other → `lost`),
resubmits retryable jobs once, and deletes Succeeded workflows.

**SSH backend.** Driver (one per campaign: POSIX lock on /home) probes nodes, dispatches `ssh -x node 'setsid
nohup nice -n 10 qv2-job …'` (detached: survives connection and driver loss), re-reads only active jobs' markers
(full scan once at start), checks liveness (pid + boot id via ssh) every 30 s, marks dead wrappers `lost`, retries.

**Drivers and watcher (after the incident).** `--on <worker>` starts a driver detached on a worker (RSS 21.7–22.0 MB,
measured). It rewrites `_driver/driver.json` (status, counts, `heartbeat`) only on change or every 60 s. The einstein
watcher `bin/qv2-watch` is bash (RSS 3.7 MB, measured): it reads only that file, exits 0 when complete, 2 on
failures, 4 when the heartbeat is older than 300 s. It makes no marker scans and no cluster calls.

**Tests.** Payload `examples/payload.py` (deterministic sha256 stream, known digests; memory allocator; sleep; fail).
Scenarios `examples/scenario_*.sh` run on landau. Allocation respected: landau ≤ 2 concurrent jobs; Argo test pods
on landau only, ≤ 2 at a time, CPU request 1. Argo tests ran at 14:58, 14:59–15:04, 15:46–15:48, 15:55–16:02, 16:03
and 16:16–16:20, and every workflow was saved to `argo_status/` and deleted (0 left). The marker-latency test used
12 sleep-dominated writer processes for ~10 s.

## 3. Results

### R1 Accounting check (landau, 14:56–14:58)
| quantity | wrapper (SSH) | `/usr/bin/time -v` (host) | wrapper (Argo pod) |
|---|---|---|---|
| CPU s | 8.96 | 8.94 | 9.00 |
| max RSS MB | 321.1 | 321.0 | 321.1 (cgroup `memory.peak` 338.5) |
| output sha256 | 4010dc83… | 4010dc83… | 4010dc83… |
VERIFIED: markers `runner_ledger/markers/feas-acct-{ssh,argo}/000/*.marker`. The pod image has no `/usr/bin/time` and
no `python3` (VERIFIED: job log `logs/feasibility/runner/feas-acct-argo/000/acct-argo.a1.log`). `ru_maxrss` has a
floor of roughly the forking process's RSS, because Linux carries the pre-exec high-water mark across exec. That is
irrelevant at the study's 0.1–1.6 GB scale.

### R2 CPU-bound ~60 s job, 3× Argo + 3× SSH on landau, one at a time
| | Argo, quiet (16:16–16:23) | SSH, quiet | Argo, NFS saturated (14:59–15:09) | SSH, NFS saturated |
|---|---|---|---|---|
| CPU s (mean ± sd) | 58.79 ± 0.10 | 58.95 ± 0.02 | 58.88 ± 0.08 | 58.96 ± 0.09 |
| command wall s | 58.84 | 59.01 | 62.3 | 60.4 |
| max RSS MB | 19.5 | 20.0 | 19.8 | 20.0 |
| wrapper start-up s | 0.74 | 0.78 | 16.8 (10–25) | 15.9 (4–25) |
| makespan, 3 jobs, s | 227.0 | 184.2 | 320.0 | 251.1 |
| **overhead per job s** (makespan/3 − wall) | **16.8** | **2.4** | 44.4 | 23.3 |
| pod start → wrapper start s | 5.6, 4.9, 5.0 | — | 11.0, 7.2, 6.6 | — |
| pod duration − command wall s | 7.3, 7.2, 6.0 | — | 31.4, 28.7, 41.0 | — |
| gap between sequential pods s | 10.0, 10.0 | 0.4, 0.5 (next job start) | 10.0, 10.0 | 2.9, 3.8 |
| last pod end → workflow Succeeded s | 10.0 | — | 10.0 | — |
VERIFIED: `benchmarks_runner.json` (`cpu60`, `cpu60q`), from markers `runner_ledger/markers/feas-cpu60{,q}-*` and
`data/feasibility/runner/argo_status/jdochoa-qv2-feas-cpu60{,q}-argo-*.json`, driver times
`cpu60{,q}_driver_times.json`. The quiet runs use the node-local interpreter cache. CPU time does not depend on the
mechanism. ESTIMATE for production: each Argo slot loses ~17 s per job (pod start + controller gap), i.e. ~1% for
30-min jobs and ~3% for 10-min jobs. The SSH runner loses ~2 s.

### R3 Wrapper start-up, re-measured on a quiet server and reduced (post-incident constraint b)
| | interpreter on NFS | node-local cache |
|---|---|---|
| metadata calls on `/home/users` per job start (`strace -f`) | 687 | 28 |
| skip-path wrapper, warm, s | 0.07–0.10 (cold 0.84) | 0.07–0.10 |
| process start → wrapper ready s (quiet) | — | 0.72–0.78 |
| same, NFS saturated s | 10–25 | not re-measurable on demand |
| one-off cache fill per node and code version | — | 24.5 s, 130 MB local |
VERIFIED: strace on landau 15:40 (Code reference), `t_wrapper − t_proc_start` in markers. Rejected alternatives:
`PYTHONPYCACHEPREFIX` (every `.py` is still stat'ed on NFS); bash-only accounting (no exact child-tree `ru_maxrss`
without a helper binary). The study's own payload environments still import from NFS (O1).

### R4 kill -9 of the wrapper at every stage, then resume (constraint c), landau 15:44
| stage killed | state after kill -9 | `status --live` | resume | rerun |
|---|---|---|---|---|
| during command | marker `started`; payload orphaned in its systemd scope | dead 1 | orphan scope stopped, scratch wiped, command re-run → done | skip |
| before copy | stash in scratch; nothing on cajuela | dead 1 | resumed from stash (command not re-run) → done | skip |
| during copy | `kill-during_copy.dat.part` on cajuela | dead 1 | stale `.part` removed; resumed from stash → done | skip |
| after rename, before marker | final file present but no `done` line (does not exist for the analysis) | dead 1 | resumed from stash, re-copied → done | skip |
After the run there were no `.part` files, no scratch dirs and no scopes; `verify` found 0 corrupt; the four outputs
have identical sha256 `444e029a5e2606d4…`, as expected for the deterministic payload. VERIFIED: rerun with
`ssh -x landau tools/runner/examples/scenario_kill_stages.sh`; markers `runner_ledger/markers/feas-kill/`. Simulated
cajuela EIO (unit tests `TestIOResilience`): a transient outage is retried and succeeds; a long outage ends
`io_error` with the stash kept and no output published, and the next attempt publishes without re-running the
command.

### R5 Memory limit 200 MB, job allocating 400 MiB (constraint d), landau 15:46–15:48
| mechanism | guard | outcome | RSS at kill | node after |
|---|---|---|---|---|
| SSH | `systemd-run --user --scope -p MemoryMax=200M -p MemorySwapMax=0` | killed after 192 MiB allocated; `oom`; not retried | 209.6 MB | avail. 5640 → 5560 MB; load 0.33 |
| Argo | pod `limits.memory: 200Mi` | `OOMKilled (exit code 137)`; `oom` written by the driver from pod status; not retried | — | load 0.44 |
VERIFIED: markers `runner_ledger/markers/feas-mem-{ssh,argo}/`, `argo_status/jdochoa-qv2-feas-mem-argo-c0-1zr7n.json`.
Finding fixed during the test: Kubernetes kills the whole container on OOM, wrapper included. A first run left only
`started` and was resubmitted once (2 OOMs); the driver now reconciles from pod status.

### R6 Marker-write latency on `/home/users` (sync NFS export), landau 15:48
| method | writers | events | median ms | p90 ms | max ms |
|---|---|---|---|---|---|
| O_APPEND + fsync (runner) | 1 | 10 | 108.5 | 162.1 | 162.1 |
| O_APPEND + fsync (runner) | 12 | 120 | 152.9 | 360.3 | 560.4 |
| read + `.part` + fsync + rename (first version) | 1 | 10 | 215.9 | 285.5 | 285.5 |
| read + `.part` + fsync + rename (first version) | 12 | 120 | 1557.8 | 2056.6 | 2410.9 |
VERIFIED: `data/feasibility/runner/marker_latency.jsonl`. Its first row (382 ms, 1 writer) was taken at 15:12 during
the incident and is not used. A job writes 2 marker events (≈ 0.3 s at 12 writers), so no consolidated collector is
needed. ESTIMATE: a collector would be worth it only for jobs shorter than ~1 min at full parallelism.

### R7 24-job mini-campaign, SSH backend (landau, 2 concurrent, ~10 s jobs), 15:50–15:55
| step | result |
|---|---|
| kill -9 the driver after 6 done (driver on landau, RSS 21.7 MB) | running jobs finished on their own (8 done after 30 s; none dispatched) |
| restart the driver (`--on landau`) | resumed from markers and completed |
| SIGTERM a running wrapper (mini-ssh-009) | `started killed started done` |
| kill -9 a running wrapper (mini-ssh-010; payload orphaned) | liveness → `lost`; retry stopped the orphan scope; `started lost started done` |
| completion | watcher exit 0 on landau and on einstein (bash, RSS 3.7 MB); 0 scratch dirs, 0 scopes left |
| relaunch on the complete campaign | nothing dispatched; direct `qv2-job` → `skip` |
| append 1 byte to mini-ssh-007.dat | `verify`: CORRUPT (size 1048679 ≠ 1048678); relaunch re-ran only that job; `verify` 0 |
| ownership / mode | 24 files `10015:10000 644`; dirs `755`; 0 `.part` |
| directory renames | none (code renames regular files only; unit test); `000` inode unchanged (`001` created after the first snapshot) |
| makespan | 279.6 s |
VERIFIED: `data/feasibility/runner/scenario_mini_ssh.log`, `einstein_watch_mini_ssh.log`, markers `feas-mini-ssh/`;
`MANIFEST` written (24 files, 25,168,272 B, sha256 `4c00eec70a6ce357…`).

### R8 24-job mini-campaign, Argo backend (landau, parallelism 2), 15:55–16:02; pod deletion 16:03
| step | result |
|---|---|
| kill -9 the driver after 6 done (on landau, RSS 22.0 MB) | workflow stayed `Running`; 8 done after 30 s |
| restart the driver | found the running workflow by label, waited, completed |
| delete a running pod (`feas-podkill`, 40 s job) | wrapper wrote `killed`; Argo `Error: pod deleted` → OnError retry → `started killed started done`; workflow Succeeded |
| relaunch on the complete campaign | nothing submitted |
| append 1 byte to mini-argo-013.dat | `verify` CORRUPT; relaunch submitted a 1-job workflow; `verify` 0 |
| ownership / mode | 24 files `10015:10000 644`; dirs `755`; 0 `.part`; `000` inode unchanged |
| makespan | 375.1 s |
| workflows | all saved to `argo_status/` and deleted; 0 left |
In the main scenario the pod-deletion step found no pod in phase Running at that instant (empty selector), so it was
repeated as the dedicated `feas-podkill` test. VERIFIED: `scenario_mini_argo.log`, `argo_status/*mini-argo*`,
`*podkill*`, markers `feas-mini-argo/`, `feas-podkill/`.

### R9 pyhf benchmark on landau (T1 input; TOY workspace only), 16:04–16:15, through the SSH runner
Workspace (`src/pyhf_bench/bench_pyhf.py`): 3 counting categories and 25 background terms (9+8+8), each with a
Poisson/Gamma `shapesys` constraint. tau = MC count; a zero count is represented by one event weight with tau = 1,
which is a toy convention and not a T1 choice. Plus 5 correlated `normsys` and one `normfactor` mu: 31 parameters.
pyhf 0.7.6, numpy 2.2.6, scipy, one thread.
| step | CPU s | wall s | RSS MB |
|---|---|---|---|
| one MLE fit (scipy) | 0.116 | 0.257 | 102.8 |
| one MLE fit (minuit) | 0.337 | 0.362 | 105.2 |
| one asymptotic CLs point (qtilde + expected band) | 0.517 | 0.524 | 103.0 |
| 20-point upper-limit scan (asymptotic) | 10.44 | 10.46 | 103.0 |
| 1000 toys at one point (1000 s+b + 1000 b-only) | 651.8 | 652.2 | 104.2 |
| whole job incl. imports (rusage): fit job / toys job | 13.15 / 653.56 | 23.5 / 663.1 | 107.0 / 106.6 |
VERIFIED: `data/feasibility/runner/feas-pyhf/000/pyhf-{fit,toys}.json`, markers `feas-pyhf/`. ESTIMATE: 1000 toys
cost ≈ 11 CPU-min per grid point for a 31-parameter model, so one point fits in one job; 40 points ≈ 7.2 CPU-h.
Not measured: scaling with the number of parameters.

### R10 Ledger, manifest, usage, bundle
`rebuild-ledger` on the test ledger: 66 rows. `usage`: 62 files, 73.7 MB of test data (0.005% of the budget).
`bundle` to a test destination: 73.0 MB, `git bundle verify` OK, `.sha256` sidecar, rotation unit-tested (7 +
`gate-*`), test bundles deleted. VERIFIED: `runner_ledger/jobs.tsv`, commands in Code reference.

## 4. Validation

- Unit tests (`python -m unittest`, stdlib, 21 tests, on landau): campaign validation; directory/cross-directory
  rename refusal; `.part` → rename → verify; marker states and torn lines; wrapper success/skip/corrupt/failure/
  missing output/timeout/stale debris/RSS accounting; I/O back-off and stash resume; ledger/manifest/usage; node caps,
  graphical detection, Guayaquil time cap; Argo render against every §5.3 field, chunking, parallelism bounds,
  refusal to delete foreign names; bundle rotation.
- Accounting cross-check against `/usr/bin/time -v` (R1). Deterministic payload digests identical across mechanisms,
  retries and stash resumes (R1, R4).
- Self-check against the brief: no `/tmp` (tests under `/var/tmp/jdochoa/runner_tests` on landau, removed); no
  directory renamed on cajuela; no lock files, envs or caches on cajuela (cache and locks on node-local scratch);
  only `jdochoa-qv2-*` objects with our labels created and deleted; einstein used only for editing, ssh/argo launch
  lines and the bash watcher after the incident.

## 5. Open issues

- **O1 NFS home latency.** When the /home NFS server is saturated (15:00–15:10: load 11, all 8 nfsd threads and
  jbd2 in D state), every Python start from NFS costs 10–25 s. The runner now avoids this; the study's payload
  environments do not, so their per-job start-up depends on NFS load. nfsd thread count is an admin matter.
- **O2 Argo OOM.** Kubernetes kills the whole container, so the job's max RSS at the OOM is not recorded; the driver
  writes `oom` from pod status and removes the dead job's scratch dir on its node over ssh. That clean-up was added
  after the tests: the R5 run left `/home/scratch/jdochoa/mem-argo` on landau, removed by hand; this clean-up path is
  not yet exercised by any test. The 1.5× limit must come from a measured RSS.
- **O3 Weekday cap.** It is computed at submission over `expected_hours`. A running workflow is not re-capped if it
  overruns into 08:00 (possible fix: patch `spec.parallelism`; not implemented). Set `expected_hours` honestly.
- **O4 Pinned mode** (unequal node caps) splits a chunk statically across nodes: no rebalancing if one node is
  slower.
- **O5 numpy pin.** pyhf 0.7.6 toy CLs fails with numpy ≥ 2.4 (`np.percentile(interpolation=)`); the bench env pins
  numpy 2.2.*. T1 must pin likewise.
- **O6 Stash locality.** A stash is reused only on the same node. If an Argo retry lands elsewhere, the command is
  re-run, and a stash left on the first node stays until that job runs there again. A periodic `clean-scratch`
  command is not implemented. A `done` job's stash is never read, so this costs only disk.
- **O7 Argo per-job latency** ≈ 17 s (R2). Prefer jobs of 10–30 min; the SSH runner is better for many short jobs.
- **O8 Ledger format mix.** Markers written by other executors in `ledger/markers/feasibility_*/` are flat files,
  not in the runner's `<campaign>/<shard>/<job>.marker` layout; `rebuild-ledger` skips them.
- **O9 Timestamps.** Pods run in UTC, so marker `t` strings from pods carry `+0000`; the epoch `ts` fields are
  canonical.
- Left on landau: `/home/scratch/jdochoa/cache/runner/` (130 MB, intended), `drivers/*.log`, `.locks/` (tiny).

## 6. Code reference (exact commands)

```bash
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner; E=$R/examples/feas
# unit tests (on a worker)
ssh -x landau "cd $R && nice -n 10 .pixi/envs/default/bin/python -m unittest discover -s tests"
# test campaigns
$R/.pixi/envs/default/bin/python $R/examples/make_feas_campaigns.py
# R1 accounting
ssh -x landau "$R/bin/qv2run ssh launch $E/feas-acct-ssh.json --nodes landau --max-per-node 1"
ssh -x landau "$R/bin/qv2run argo launch $E/feas-acct-argo.json --nodes landau --max-parallel 1 --keep"
# R2 Argo vs SSH (quiet re-measurement; the first run used feas-cpu60-*.json the same way)
ssh -x landau $R/examples/scenario_cpu60q.sh
# R3 start-up metadata count
ssh -x landau "strace -f -e trace=stat,openat,newfstatat,statx,access,readlink,execve -o s.txt $R/bin/qv2-job \
  --campaign $E/feas-kill.json --job kill-before-copy --mechanism ssh; grep -c home/users s.txt"   # QV2_NO_CACHE=1 for NFS
# R4 kill -9 at every stage
ssh -x landau $R/examples/scenario_kill_stages.sh
# R5 memory
ssh -x landau "$R/bin/qv2run ssh launch $E/feas-mem-ssh.json --nodes landau --max-per-node 1"
ssh -x landau "$R/bin/qv2run argo launch $E/feas-mem-argo.json --nodes landau --max-parallel 1 --keep"
# R6 marker latency
ssh -x landau "cd /home/users/jdochoa/hllhc-quirks-search && $R/.pixi/envs/default/bin/python $R/examples/marker_latency.py \
  --writers 12 --events 10 --method append --dir analyses/quirks_v2/phase1_strategy/outputs/feasibility/runner_ledger/latency_tmp"
# R7, R8 mini-campaigns and pod deletion (run on landau, detached)
ssh -x landau "setsid nohup $R/examples/scenario_mini_ssh.sh > …/scenario_mini_ssh.log 2>&1 &"
ssh -x landau "setsid nohup $R/examples/scenario_mini_argo.sh > …/scenario_mini_argo.log 2>&1 &"
ssh -x landau $R/examples/scenario_podkill.sh
# R9 pyhf
ssh -x landau "$R/bin/qv2run ssh launch $E/feas-pyhf.json --nodes landau --max-per-node 2 --on landau"
# R10 ledger / manifest / usage / bundle
ssh -x landau "$R/bin/qv2run rebuild-ledger"          # production ledger → analyses/quirks_v2/ledger/jobs.tsv
ssh -x landau "$R/bin/qv2run manifest $E/feas-mini-ssh.json"
ssh -x landau "$R/bin/qv2run usage"
ssh -x landau "$R/bin/qv2run bundle"                  # --gate A at gates; --dest for tests
# summary JSON
ssh -x landau "$R/.pixi/envs/default/bin/python /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase1_strategy/src/runner_feas/summarize_runner.py"
```
Files: `tools/runner/{pixi.toml,bin/{qv2run,qv2-job,qv2-watch},qv2run/*.py,tests/test_runner.py,examples/*}`,
`analyses/quirks_v2/phase1_strategy/src/{pyhf_bench/{pixi.toml,bench_pyhf.py},runner_feas/summarize_runner.py}`.

## 7. How to launch, watch, resume and account a campaign (one page, for the orchestrator)

`R=/home/users/jdochoa/hllhc-quirks-search/tools/runner`. On einstein run only the launch lines (they ssh to a worker)
and the bash watcher; everything else runs as `ssh -x landau "$R/bin/qv2run …"`.

1. **Describe** the campaign in JSON (templates: `tools/runner/examples/feas/*.json`):
   `{"campaign": "b4-zll-r05", "tier": "regenerable", "regenerate": "<command>", "expected_hours": 6,
   "defaults": {"max_rss_mb": 1600, "timeout_s": 1800}, "jobs": [{"id": "b4-zll-r05-0001", "shard": 0,
   "command": "<writes NAME.npz into $QV2_OUT_DIR>", "outputs": ["NAME.npz"]}, …]}`.
   - The job writes outputs into its scratch dir `$QV2_OUT_DIR`; the wrapper publishes them to
     `data/<campaign>/<shard:03d>/`.
   - `max_rss_mb` = the measured max RSS (request); limit = 1.5×.
   - Commands call their pixi env's python by absolute path.
   - ≤ 10,000 outputs per shard; ids `[a-z0-9._-]`; jobs ≤ 30 min.
2. **Launch.** The driver runs detached on a worker, never on einstein.
   - Argo (default): `$R/bin/qv2run argo launch CAMP.json --on landau`. Parallelism and node caps are automatic
     (12, or 9 on weekdays 08–19 over `expected_hours`; 4 per node, 3 with a graphical session; minus load; nodes
     with our SSH jobs excluded). ≤ 500 steps per workflow.
   - SSH (fallback, benchmarks): `$R/bin/qv2run ssh launch CAMP.json --nodes landau,maxwell --on landau
     [--max-per-node N]`.
3. **Watch** from einstein in the background: `$R/bin/qv2-watch CAMP.json 60 300`.
   - 0 = complete;
   - 2 = finished with failures or no capacity;
   - 4 = driver dead (heartbeat > 300 s) → step 5;
   - 5 = no driver state.
4. **Status** (markers only): `ssh -x landau "$R/bin/qv2run status CAMP.json --live -v"` → done / failed / running /
   retryable / pending / dead.
5. **Resume** after any death (driver, worker, einstein, cajuela outage): rerun the step-2 launch line. It rebuilds
   state from markers, waits for running workflows, and retries `killed/lost/io_error/corrupt` (≤ 2×). It never
   retries `failed/timeout/oom`, and skips `done` jobs whose outputs still verify. Jobs killed after their command
   finished resume from their stash.
6. **Verify** before use: `ssh -x landau "$R/bin/qv2run verify CAMP.json"`. Mismatches become `corrupt` and are
   re-run by the next launch.
7. **Account:**
   - `qv2run rebuild-ledger` → `ledger/jobs.tsv`;
   - `qv2run manifest CAMP.json` → `data/<campaign>/MANIFEST` and the printed `DATA_MANIFEST.md` row;
   - `qv2run usage` → the storage table for `STATUS.md` (from markers, no `du`);
   - `qv2run bundle` daily, `--gate A` at gates (keeps 7 + all `gate-*`).
8. **Failures:** the last marker line names the job log (`logs/<campaign>/<shard>/<job>.a<N>.log` on cajuela).
   `oom` → re-measure RSS and raise `max_rss_mb`; `timeout` → split the job; `io_error` → it is retried
   automatically; if it persists, check cajuela and stop per the brief.
9. **Clean-up:** drivers delete Succeeded workflows. Failed ones expire after 24 h or are removed with
   `argo delete jdochoa-qv2-…` after inspection.
