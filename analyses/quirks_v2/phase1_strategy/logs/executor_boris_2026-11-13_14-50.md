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
