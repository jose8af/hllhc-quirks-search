# Plan — feasibility executor C (Boris): resumable job runner

Session Boris, 2026-11-13. Scope: build and validate `tools/runner/` (no production samples), plus a pyhf benchmark.
Spec: brief §5.2–5.4, `tools/PREFLIGHT.md`, `AGENT_RULES.md`. Allocation: landau, at most 2 concurrent jobs; Argo
test pods ≤ 3 at a time, CPU request 1, a few seconds each; einstein light only (`nice -n 19`).

## 1. Package layout (standard library only)

```
tools/runner/
  pixi.toml            # minimal env: python 3.12 only — the pod image has no Python; this env (on /home) is
                       # the interpreter for the wrapper both in pods and over SSH (same absolute path)
  bin/qv2run           # bash entry: picks tools/runner/.pixi/envs/default/bin/python, falls back to
                       # /usr/bin/python3 on hosts; runs `python -I -m qv2run "$@"`
  bin/qv2-job          # bash entry used by pods and SSH: `umask 022; exec nice … qv2run job …`
  qv2run/
    paths.py           # constants: REPO, QV2, DATA, LOGS, SCRATCH, default ledger, pinned image digest
    campaign.py        # load + validate campaign JSON
    markers.py         # marker read/append (atomic rewrite on /home), job state from markers
    fsops.py           # atomic_rename_file (refuses directories), fsync, sha256, safe makedirs
    wrapper.py         # the job wrapper (`qv2run job`)
    ledger.py          # `rebuild-ledger`, `status`, `verify`
    argo.py            # workflow generation, parallelism, pre-launch node check, resumable driver
    ssh.py             # resumable SSH dispatcher
    watch.py           # blocking watcher
    manifest.py        # MANIFEST, DATA_MANIFEST line, usage report
    bundle.py          # git bundle rotation
    cli.py, __main__.py
  tests/               # python3 -m unittest (stdlib), temp dirs under /var/tmp/jdochoa/runner_tests
  examples/            # test campaigns + payload generator
```

JSON, not YAML, for campaign files: no dependency, and JSON is valid YAML for `argo submit`.

## 2. Campaign file (JSON)

```json
{"campaign": "feas-runner-mini", "tier": "scratch|regenerable|final|test",
 "data_prefix": "feasibility/runner",          // optional; final dir = data/<prefix>/<campaign>/<shard:03d>/
 "ledger": "analyses/quirks_v2/…/markers",     // optional; default analyses/quirks_v2/ledger/markers
 "regenerate": "command that regenerates the campaign",
 "defaults": {"cpu": 1, "max_rss_mb": 100, "timeout_s": 1800, "shard": 0},
 "jobs": [{"id": "mini-000", "shard": 0, "command": "…", "outputs": ["mini-000.dat"],
           "max_rss_mb": 120, "cpu": 1}]}
```
Validation: ids `[a-z0-9][a-z0-9._-]{0,62}` and unique; outputs are bare file names (no `/`), unique across the
campaign shard; timeout ≤ 1800 s; ≤ 10,000 outputs per shard directory.

## 3. Job wrapper (`qv2run job --campaign F --job ID --mechanism argo|ssh`)

1. Idempotency: if the marker's last result is `done` and every output exists with the recorded size and sha256 →
   log "skip", exit 0. Size/hash mismatch → append `corrupt` line, rerun.
2. Lock `/home/scratch/jdochoa/.locks/<job_id>.lock` (local disk, `flock`); remove stale scratch; create
   `/home/scratch/jdochoa/<job_id>`; remove stale `name.part` on cajuela; append `started` line (node, pid, boot id).
3. Run `bash -c "<command>"` in the scratch dir, new session, niceness raised to ≥ 10, umask 022, env
   `QV2_JOB_ID, QV2_OUT_DIR(=scratch), QV2_SHARD, QV2_CAMPAIGN`; stdout/stderr to a scratch log. Memory limit under
   SSH: `systemd-run --user --scope -p MemoryMax=…` when available (tested), otherwise an RSS watchdog. Under Argo the
   pod cgroup limit applies.
4. Accounting: `os.wait4` on the child → `ru_utime+ru_stime` (CPU s) and `ru_maxrss` (max RSS over the child and
   its waited-for descendants, = `/usr/bin/time -v` semantics); also cgroup `memory.peak` when readable. Validated
   against `/usr/bin/time -v` on the host and inside a pod.
5. Timeout: 1800 s (campaign value ≤ 1800) → SIGTERM to the process group, SIGKILL after 30 s, status `timeout`.
   SIGTERM/SIGINT to the wrapper → kills the group, cleans up, status `killed`.
6. On success: for each output: sha256 on scratch → copy to `<final>/<name>.part` → fsync → rename (file only;
   `atomic_rename_file` refuses directories) → re-read and verify sha256 → append `done` line with outputs (path,
   sha256, bytes), CPU s, max RSS, wall s. Log copied to `logs/<prefix>/<campaign>/<shard:03d>/<job>.a<N>.log`
   (`.part` + rename). Delete scratch. On failure: delete scratch and own `.part` files, append the failure line.
7. Exit code: 0 done/skip; 1 failed; 2 timeout; 3 killed; 4 verify failure; 5 setup error.

**Markers** (on `/home`, one writer per job): `<ledger>/<campaign>/<shard:03d>/<job_id>.marker`, JSON Lines, one
line per event (`started`, `done`, `failed`, `timeout`, `killed`, `oom`, `corrupt`, `verify_failed`). Appended by
rewriting `marker.part` + fsync + rename on `/home` (never concurrent appends to a shared file). Sharded by the
campaign's shard number (≤ 10,000 jobs per shard by rule).

## 4. Ledger
`qv2run rebuild-ledger [--ledger DIR] [--out jobs.tsv]`: one writer, scans markers, writes `jobs.tsv.part` →
rename. Columns: `job_id campaign mechanism node status cpu_s max_rss_mb wall_s output sha256 bytes attempts
end_time` (one row per output; jobs without outputs get one row). `status` prints done/failed/running/pending from
markers only. `verify` re-hashes outputs of done jobs against markers.

## 5. Argo backend (`qv2run argo submit|launch|render`)
- Workflow per chunk of ≤ 500 jobs; `metadata.name = jdochoa-qv2-<campaign>-c<k>-<rand>`, labels `owner=jdochoa,
  study=quirks-v2, qv2-campaign, qv2-chunk`, podMetadata with the same labels; spec exactly as §5.3 + PREFLIGHT
  (securityContext 10015/10000, 3 volumes at host paths, pinned image IfNotPresent, `nice -n 10`, `umask 022`,
  requests cpu 1 + memory = max RSS, limit 1.5×, `activeDeadlineSeconds: 2400`, `retryStrategy {limit: 2,
  retryPolicy: OnError}`, `podGC OnPodSuccess`, `ttlStrategy 86400`); node name passed by the downward API.
- Parallelism: 12, or 9 if a weekday 08:00–19:00 America/Guayaquil (zoneinfo; fallback UTC−5) at launch or within
  the campaign's expected duration; then the pre-launch check: per node `ssh -x node 'cat /proc/loadavg; who'` →
  node cap 4 (3 if a graphical session) minus round(load1) and minus our own running SSH jobs; nodes with an
  SSH campaign of ours are excluded. If all caps are equal: one pooled workflow with node affinity and parallelism
  = Σcaps; otherwise **pinned mode**: one workflow per node (nodeSelector, parallelism = node cap) so the per-node
  cap (e.g. 3 with a graphical session) is enforced exactly.
- Driver (`launch`, run with nohup): submits chunks one after another, each with only the jobs not done by
  markers; on restart it finds our running workflows by label and waits for them (`argo wait`), so killing the
  driver never kills jobs. Deletes Succeeded workflows of the campaign at the end (keeps failed for inspection).

## 6. SSH backend (`qv2run ssh launch`)
Driver holds `flock` on `<ledger>/<campaign>/.ssh_driver.lock` (on /home NFS) → one driver per campaign. Jobs are
started detached on the node: `ssh -x node 'setsid nohup qv2-job … &'`; the driver polls markers (every 5 s) and
checks liveness of `started` jobs (`ssh node ps -p pid -o args=`, boot id). Per-node slots 4 (3 graphical) or the
`--max-per-node` value; a node with a running Argo pod of ours is skipped. Lost/killed jobs are retried up to 2
times (Argo OnError analogue); `failed`/`timeout`/`oom` are not retried. A restarted driver reconstructs everything
from markers + liveness, so it resumes after dying.

## 7. Watcher / status
`qv2run watch <campaign> [--interval 60] [--timeout …]`: blocks, rereads markers each interval (cheap), exits 0
when all jobs `done`; exits 2 when no driver/workflow is active and jobs remain not done or any job is in a
terminal failure; exits 3 on timeout. One process, no tight loop.

## 8. Manifest / usage / bundle
- `qv2run manifest <campaign>`: `MANIFEST` (path, bytes, sha256 from markers; `--verify` re-hashes) written in the
  campaign dir on cajuela as `.part` → rename; prints the `DATA_MANIFEST.md` row (size, file count from markers,
  manifest sha256, tier, regenerate command).
- `qv2run usage`: per-campaign and total bytes from all markers (no `du`/`df` over NFS), Markdown for `STATUS.md`.
- `qv2run bundle [--gate X] [--dest DIR]`: `git bundle create <dest>/repo-<date>.bundle.part --all` → `git bundle
  verify` → rename → sha256 → keep last 7 `repo-*` + all `gate-*`.

## 9. Test plan (outputs under `data/feasibility/runner/`, test ledger in
`phase1_strategy/outputs/feasibility/runner_ledger/markers/` so the production `ledger/jobs.tsv` stays clean)
| # | test | mechanism | node / concurrency |
|---|---|---|---|
| T0 | unit tests `python3 -m unittest` | local | einstein, nice 19 |
| T1 | accounting check: wrapper CPU/RSS vs `/usr/bin/time -v` (host) and vs cgroup `memory.peak` (pod) | ssh + argo | landau, 1 |
| T2 | CPU-bound ~60 s hashing job, known digest, 3× Argo + 3× SSH; CPU, wall, RSS, overhead | both | landau, 1 at a time |
| T3 | 24-job mini-campaign; kill launcher midway + resume; kill one job midway; corrupt one output → verify; owner/mode 644; no dir renamed | both | landau, 2 |
| T4 | memory test, limit 200 MB, job allocates > 200 MB | both | landau, 1 |
| T5 | pyhf benchmark (own pixi env in `phase1_strategy/src/pyhf_bench/`), via the SSH runner | ssh | landau, 1–2 |
| T6 | manifest, usage, ledger rebuild, bundle (test dest under data/feasibility/runner/backup_test) | local | einstein |
Every test workflow is deleted after its results are recorded.

## 10. Artifacts
`FEAS_C_runner_boris.md` (Summary, Method, Results, Validation, Open issues, Code reference, how-to page),
`benchmarks_runner.json`, experiment log entries `[Boris]`, session log `logs/executor_boris_2026-11-13_14-50.md`.
