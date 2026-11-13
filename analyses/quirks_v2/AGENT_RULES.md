# Rules for every subagent of the quirks v2 study

Read this file, then the "STUDY OVERRIDES" block at the top of `analyses/quirks_v2/CLAUDE.md`. Both are binding.

`REPO=/home/users/jdochoa/hllhc-quirks-search`, `QV2=$REPO/analyses/quirks_v2`, `TT=$REPO/stage2_C001_quirks/theory_track`.
Start every shell with `. $REPO/tools/env.sh` (pixi, paths, umask).

## Where you may write
- Inside the repo: only `analyses/quirks_v2/` and `tools/`. Everything else (`stage2_C001_quirks/`, `research/`,
  `book/`, `publication_plan/`, `tools/jfc/`) is **read-only**; copy before modifying.
- Outside: `/nfs/cajuela/jdochoa/quirks_v2/{data,logs}` (bulk), `/home/users/jdochoa/sw` (software),
  `/home/scratch/jdochoa/<job_id>` on the workers (per-job work), `/var/tmp/jdochoa/` (build trees).
- Never: `/tmp`, `/home/jochoaf`, `/mnt/cajuela*`, other users' files, `sudo`, `git push`, anything that publishes.

## cajuela (bulk data) rules
- Write `name.part` in the final directory, fsync, rename to `name`, then write the marker line (sha256, bytes, CPU
  time, max RSS) under `analyses/quirks_v2/ledger/markers/`. A file without a marker does not exist.
- **Never rename a directory on cajuela.** Create directories under their final names. Renaming files is fine.
- No hard links, git repos, pixi/conda envs, caches, SQLite files or lock files on cajuela. Few large compressed
  files (10 MB or more each), at most 10,000 entries per directory.
- Stage large shared inputs into node-local scratch once; never let many jobs stream the same multi-GB file.

## Compute rules (shared lab machines)
- `einstein` is the head node (NFS, LDAP, Kubernetes control plane): at most 3 light jobs in total across all agents,
  always `nice -n 19`, nothing I/O-heavy, build trees at most 50 GB and preferably on a worker instead.
- Workers `landau`, `maxwell`, `schrodinger`: 4 cores, 7.5 GiB, no swap. Use `ssh -x <node> 'cd … && nice -n 10 …'`.
  Use only the node(s) and job count the orchestrator assigned to you. Check `uptime` and `who` first.
- Every job 30 minutes or less, idempotent, resumable. Measure CPU time and max RSS with `/usr/bin/time -v`.
- Docker Hub rate-limits the lab's IP: use only the pinned image
  `ubuntu@sha256:2198e4c65076e9cb0b3d695219df667c0e3b0072da64ca3c2648aca17dcecaf5` (already on every worker).
- In the shared `argo` namespace touch only objects named `jdochoa-qv2-*` and labelled `owner=jdochoa,study=quirks-v2`.
- If NFS, cajuela, Kubernetes, Argo or LDAP misbehaves: stop, record the exact error, report. Do not repair.

## Working rules
- Read files with the Read tool, in full. The decision logs (`LOG.md` files of v1) are long: grep them.
- Use pixi for every Python environment; never bare `pip install` or `conda`.
- Tag every number you report: VERIFIED (you measured or re-derived it, cite file:line or command), ESTIMATE, or
  UNVERIFIED (transcribed, not checked). Never quote a constant from memory.
- Public information only. No CMS data, no CMS-internal tools, no CMS name or logo on any figure.
- Blinding: do not compute or look at any v2 signal efficiency. (v1 efficiencies already in the tracked record are
  public to the study and may be read.)
- **Do not run `git add` or `git commit`** unless your prompt says so: several agents work in parallel and the
  orchestrator commits. Never `git push`, never rewrite history.
- Keep an incremental session log in your phase's `logs/{role}_{session_name}_{YYYY-MM-DD}_{HH-MM}.md`: a short
  timestamped entry at each milestone, written as you go.
- Record failed attempts and decisions in your phase's `experiment_log.md` (append-only), using the
  DECISION / ALTERNATIVES / CONFIDENCE / FLAG FOR HUMAN block for judgment calls.
- If you cannot finish: write what you have to your artifact, state exactly what is missing, and stop cleanly.
- Your final message to the orchestrator: at most 250 words, the artifact path(s), the verdict, and open issues.
  The detail belongs in the artifact, not in the message.
