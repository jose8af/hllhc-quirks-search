# Preflight — quirks v2 (2026-11-13, einstein, as `jdochoa`)

**Verdict: PASS (re-run 14:34 -05, after the admin fix to cajuela).** The first run (14:06 -05) stopped on one
failure, ESTALE on the first open after a rename on cajuela; it is kept below as history. The write-`.part`-then-rename
rule of §5.2 stands unchanged (user decision: option 1, admin fix).

## Binding storage note: cajuela inode behaviour (admin, 2026-11-13)

- Cause of the first-run failure: cajuela's mergerfs ran with `inodecalc=path-hash`, which changes a file's inode
  on rename (kernel log: "NFS: fileid changed"). It now runs with `inodecalc=hybrid-hash`.
- **Renaming files on cajuela is fine.** Re-verified: 3/3 on einstein, landau, maxwell, schrodinger; inode
  unchanged across the rename; cross-node read correct; Argo pods on all 3 workers `stale_retries=0`
  (`jdochoa-qv2-preflight-cvncx`, deleted).
- **Remaining limit: directories still get a path-based inode. Never rename a directory on cajuela while other
  nodes may be using it.** Consequences for the runner: create campaign and shard directories under their final
  name; never stage a directory as `dir.part` and rename it; reorganise a directory tree only when no campaign
  is running, and log it.

## Results

| check | result | evidence |
|---|---|---|
| Identity | PASS | `whoami`=jdochoa, uid 10015, gid 10000; cwd `/home/users/jdochoa/hllhc-quirks-search` |
| Repo | PASS | owner jdochoa; clean on `main`; HEAD `9d7a11a` contains the brief |
| Data area: mkdir | PASS | `/nfs/cajuela/jdochoa/quirks_v2/{data,logs,backup}` created, owner 10015:10000 |
| Data area: worker → einstein visibility | PASS | files written over SSH from all 3 workers visible on einstein within seconds, right content and owner |
| Data area: attribute cache | PASS | no `acdirmin=1800` in `/proc/mounts` on any node (`lookupcache=pos`, vers=4.2) |
| Data area: write → rename → read | PASS on re-run (FAIL on first run) | see the storage note and the history below |
| Node scratch | PASS | `/home/scratch/jdochoa` writable on landau, maxwell, schrodinger; local ext4 |
| SSH | PASS | BatchMode reaches all 3 workers, uid 10015 on each |
| Kubernetes | PASS | 4 nodes Ready (v1.37.2); `argo list` works; create/delete workflows allowed |
| Argo pod template (§5.3) | PASS, no retry needed on re-run | `jdochoa-qv2-preflight-cvncx`, one pod per worker: uid 10015/gid 10000, nice 10, Ubuntu 24.04, data file and repo marker owned by 10015; workflow deleted |
| Guide | PASS | PDF readable; digest below |
| Typesetting | PASS | `revtex4-2.cls`, `biblatex.sty` resolve; `latexmk`, `biber` on PATH |

## History: first-run failure, ESTALE after rename on cajuela (fixed)

Reproduced deterministically (3/3 on einstein, 3/3 on landau over SSH, 3/3 in pods):

```
f=/nfs/cajuela/jdochoa/quirks_v2/logs/x; echo a > $f.part; sync $f.part; mv $f.part $f
cat $f     # cat: ...: Stale file handle   (einstein: "`handle' de fichero en desuso")
cat $f     # a
```

Measured behaviour:
- Only the client that performed the rename is affected, and only on its first `open` of the new name.
  An immediate retry succeeds; so does a `stat` before the open.
- Another node reading the renamed file right away gets the correct content.
- The inode number is unchanged by the rename. A file written directly (no rename) reads back fine.
- The same pattern on `/home/users` (plain ext4 over NFS) works, so this is specific to the mergerfs export.
- First Argo attempt (`jdochoa-qv2-preflight-m5kz8`) failed on all 3 pods for this reason, at `sha256sum` right
  after the rename.

Resolved by the admin fix described in the storage note above.

## Other findings (not blocking)

- **`ubuntu:24.04` was not pre-pulled on any worker** (containerd had only `python:3.12-slim`). The preflight
  pulled it on all three. Pinned digest:
  `ubuntu@sha256:2198e4c65076e9cb0b3d695219df667c0e3b0072da64ca3c2648aca17dcecaf5` (Docker Hub, 2026-11-13).
- **Pods run with umask 000**: the first run created files mode 666. The template must set `umask 022`.
- Docker's local image store is separate from containerd; `crictl` is not usable as `jdochoa`. Pre-pulling
  can only be done by running a pod on each node.
- `ssh` to the workers attempts X11 forwarding by default; use `ssh -x` in the runner.
- landau and schrodinger show a graphical session (`jochoaf` on seat0): cap of 3 jobs each for now.
- With `hybrid-hash`, a new file can receive the inode number of a just-deleted one (seen in the re-run). Harmless
  for this study, since completeness is tracked by markers and sha256, never by inode.
- Memory allocatable per worker: 7.9 GiB (landau 7911136Ki); einstein carries the control-plane taint.

## Storage baseline (2026-11-13 14:07 -05)

| filesystem | size | used | free |
|---|---|---|---|
| einstein `/home` (serves `/home/users`) | 3.2 T | 111 G | 2.9 T |
| `/nfs/cajuela` | 4.5 T | 398 G | 3.9 T |
| einstein `/` | 458 G | 240 G | 195 G |
| landau `/home` (scratch) | 364 G | 1.2 G | 344 G |
| maxwell `/home` (scratch) | 364 G | 0.6 G | 345 G |
| schrodinger `/home` (scratch) | 548 G | 0.5 G | 519 G |

## Cluster guide digest (users manual rev. 2026-11-13; the brief wins where they differ)

- **§2.10 Homes.** One home area, `/home/users`, NFS from einstein (192.168.10.254), same on every node. Not
  backed up. If a worker does not show the mount, einstein has a problem: that is an admin matter.
- **§2.11 Scratch.** `/nfs/cajuela`: mergerfs union of a 1 TB and a 4 TB disk, NFS-exported, 4.5 TB, not backed
  up. `Stale file handle` or `Input/output error` on `ls /nfs/cajuela` means a problem on the main node: notify
  the administrators; files are not lost.
- **§2.12 Fair share.** No quotas on memory or disk. Keep usage minimal and run local jobs under `nice`.
- **§2.13 Installation.** User-space installs are allowed; `apt`/`snap` need sudo, requested from the admin.
- **§2.14 Docker.** Available, but Kubernetes does not use Docker's local images; containers are named with the
  username.
- **§2.15 Kubernetes.** Shared credential `/etc/kubernetes/student.conf`, full rights inside namespace `argo`
  only. Name workflows with the username, never delete other people's. Always set `resources.requests`;
  delete finished workflows. The guide's example uses `pvc-mynfs` → `/nfs/cajuela/k8s-pv/`; this study does
  not use it (brief §5.3).
- **§2.3 Help.** Administrator contact and the minicluster mailing list are listed there.

## Files

- `tools/preflight/preflight-workflow.yaml`: the workflow that passed (sets `umask 022`; it counts stale reads, 0 on the re-run).
- `tools/preflight/markers/pod_{landau,maxwell,schrodinger}.marker`: pod result lines.
- `/nfs/cajuela/jdochoa/quirks_v2/logs/preflight_*.txt`: host and pod probe files.
