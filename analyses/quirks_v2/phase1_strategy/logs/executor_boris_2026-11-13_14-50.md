# Session log — executor Boris (feasibility C: runner), started 2026-11-13 14:42 -05

- 14:45 Read AGENT_RULES, CLAUDE.md overrides, prompt §5, tools/PREFLIGHT.md (note: it lives in tools/, not
  analyses/quirks_v2/), preflight workflow, ledger README, DATA_MANIFEST, executor.md, 11-coding.md.
- 14:45 Checks: 4 nodes Ready; no workflows of ours; landau load 0.00, graphical session jochoaf seat0;
  /usr/bin/time on hosts; systemd-run --user --scope works on landau (cgroup controllers cpu memory pids).
- 14:45 Plan written: outputs/feasibility/plan_boris.md.
- 15:02 tools/runner package written (paths, fsops, campaign, markers, wrapper, ledger, nodes, driver, ssh,
  argo, watch, manifest, bundle, cli); 19 unit tests pass on einstein.
- 14:56 T1 accounting: SSH acct job matches /usr/bin/time -v (CPU 8.96 vs 8.94 s, RSS 321.1 vs 321.0 MB). Bug found
  and fixed: ssh dispatch held the channel until job end (backgrounded && list).
- 14:58 T1 in pod: no /usr/bin/time, no python3 in the image; wrapper via runner pixi env works, CPU 9.0 s, RSS
  321.1 MB, cgroup peak 338.5 MB; identical output sha256. Templated resource quantities fail argo lint -> one
  template per resource class.
- 15:02 pyhf env: numpy 2.5 breaks pyhf 0.7.6 toys; pinned numpy 2.2.*. Smoke test OK (31 params).
- 14:59-15:04 T2 Argo cpu60 x3 on landau done (workflow jdochoa-qv2-feas-cpu60-argo-c0-np3x2, saved + deleted).
- 15:05 FINDING: wrapper start-up 10-25 s (proc start -> ready) on both mechanisms. strace: ~570 stat + 134 open on
  NFS during Python import, each up to 0.1-0.2 s. einstein load 11, all 8 nfsd threads + jbd2/sda4 in D state,
  vmstat wa 8-19%: the /home NFS server is I/O-bound (not caused by the runner; concurrent installs/builds likely).
- 15:06 bundle tool tested to data/feasibility/runner/backup_test (73.0 MB, verified), test bundles removed.
- 15:12 KILLED by einstein OOM (all agents). Resumed 15:38 under new rules: nothing heavy on einstein; tests on landau.
- 15:40 Quiet-server start-up 0.07-0.84 s; node-local interpreter cache in bin/qv2-job: /home metadata calls 687 -> 28.
- 15:42 Wrapper: I/O back-off (480 s budget), stash resume, test pause hooks; markers O_APPEND+fsync; 21 unit tests OK on landau.
- 15:44 kill -9 at 4 stages: all converge (scenario_kill_stages.sh). Driver: heartbeat file, incremental marker
  reads, runs on a worker (--on NODE); bash watcher bin/qv2-watch.
- 15:55 SSH mini scenario PASS (scenario_mini_ssh.log). 15:46-48 memory tests PASS after Argo OOM reconciliation fix. 15:48 marker latency (R6).
- 16:02 Argo mini scenario PASS; 16:04 pod-deletion test PASS (OnError retry). pyhf campaign launched on landau 16:04.
- 16:15 pyhf benchmark done (R9). cpu60q re-measurement started on landau.
- 16:23 quiet-server Argo vs SSH re-measured: overhead 16.8 s vs 2.4 s per job, CPU identical.
- 16:30 FEAS_C_runner_boris.md final (JFC sections + orchestrator guide); benchmarks_runner.json regenerated on
  landau. 0 workflows left; no runner processes left on landau. Session end.
