# Session log — executor Hedda, 2026-11-18 10:46 — "one validated job per stream" of the B1 pilot (addendum P7)

Read: AGENT_RULES.md, STUDY OVERRIDES of CLAUDE.md, agents/executor.md, B1_READY_albert §2, §5, §8, §9,
PLAN_p2-c-pilot_b1.json (`frozen_from_launch`), G/slices_pa/p2-c-pa-val2.json, src/p2x_validate.py (read only).
I do not launch anything; I edit no frozen file; no signal output is opened.

## 10:46 Plan
1. Status of the pilot from the markers (STATUS script, read-only): which streams have their first chain campaign done.
2. One new runner campaign `p2-c-pilot-val-s1` in a NEW directory `tools/runner/examples/p2x/b1_val/` (not in the
   frozen list, not in `b1/` whose 39 campaign files are hashed by the PLAN): one job per eligible stream, each job =
   `p2x_validate.py <out.json> outputs/partition_p2-c-part-0.json <first two chain files of the stream>`; same
   environment line as every campaign of the pilot (acts python).
3. CPU and RSS per job estimated from the markers of `p2-c-pa-val1-b1` (the only earlier validation of full-size
   chain files) scaled with the input bytes; nothing measured on einstein.
4. Light check of the file only: the runner's own campaign loader (`qv2run status <file> --json`, stdlib python) and
   `qv2run ssh launch --dry-run` if it dispatches nothing; inputs exist with the size of their done marker.
5. Node proposal from `pgrep` counts, `uptime`, `who`; launch line in this log; final message to the orchestrator.
6. After the orchestrator's launch: read each output, write `outputs/B1_STREAM_VALIDATION_hedda_<date>.md`.

## 10:47 Status of the pilot [VERIFIED: `bash G/b1/STATUS_p2-c-pilot_b1.sh schrodinger landau maxwell`, 10:45]
All class and low-p_T campaigns are complete (not only the first parts): g4a-00..03, g4n-00..03, g4l, c0-dif-00..03,
c0-difc-00..03, c0-nix-00..03, c0-nic-00..03, c0-ni22-00..03, c0-ni30-00..02, c0-ni61-00..02, c0-lowpt: every job
`done`. Pending: hph (10), g4h (11), c0-hs (77): the landau lane prints "p2-c-pilot-hph waits for p2-c-pilot-znn-12",
the schrodinger lane "p2-c-pilot-g4h waits for p2-c-pilot-hph"; the maxwell lane ended 03:43 ("all complete").
Eligible streams (8): pilot.c0.dif, .difc, .nix, .nic, .ni22, .ni30, .ni61, .lowpt. Not eligible: pilot.c0.hs (and
its inputs pilot.c0.hs.pool, pilot.g4 chunks 2000–2010).

## 10:52 Campaign file written (NOT launched)
`tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s1.json` (new directory; sha256 7e7d7081fe94…; campaign
`p2-c-pilot-val-s1`, tier regenerable, data prefix `p2c/pilot_validation`, 8 jobs, `max_rss_mb` 1500, timeout 1800 s,
`after` empty). One job per stream, `p2-c-pilot-val-s1-<s>` → `<job>.json`, on the outputs of the first two done jobs
(`…-0000.npz`, `…-0001.npz`) of the first chain campaign of the stream:

| job | inputs (campaign) | input MB [V: marker bytes = file size] | CPU-s [E] |
|---|---|---|---|
| -dif | p2-c-pilot-c0-dif-00: 0000, 0001 | 187 | 9.5 |
| -difc | p2-c-pilot-c0-difc-00: 0000, 0001 | 291 | 14.7 |
| -nix | p2-c-pilot-c0-nix-00: 0000, 0001 | 226 | 11.5 |
| -nic | p2-c-pilot-c0-nic-00: 0000, 0001 | 357 | 18.1 |
| -ni22 | p2-c-pilot-c0-ni22-00: 0000, 0001 | 136 | 6.9 |
| -ni30 | p2-c-pilot-c0-ni30-00: 0000, 0001 | 197 | 10.0 |
| -ni61 | p2-c-pilot-c0-ni61-00: 0000, 0001 | 192 | 9.7 |
| -lowpt | p2-c-pilot-c0-lowpt: 0000, 0001 | 160 | 8.1 |
| sum | 16 files | 1,745 | 88.5 = 0.025 CPU-h |

Built by an inline stdlib script (python3 -I on einstein, JSON only): environment line and python taken from
`p2-c-pa-val2.json` and asserted equal to the one of the pilot's chain jobs; every input taken from the `done` line of
its marker (exit 0) and its size on cajuela asserted equal to the marker's bytes (16 of 16).

Cost estimate [ESTIMATE from VERIFIED markers]: `ledger/markers/p2-c-pa-val1/000/p2-c-pa-val1-b1.marker`: 51 chain
files, 1,901 MB of input (largest 166 MB), cpu_s 96.4, max_rss_mb 535.5, wall 243 s → 0.0507 CPU-s per MB; the
validator holds one file at a time, so RSS follows the largest file: 535.5 × 179 / 166 ≈ 580 MB for nic, less for the
others. Other markers for scale: val0 28.4 CPU-s / 268 MB (64 files), val2 7.0 / 81 MB, val3 13.4 / 81 MB (tiny
files). Whole campaign: **≈ 0.025 CPU-h (budget line: ≤ 0.05), RSS ≤ ≈ 0.6 GB per job (request 1,500 MB), wall ≈ 4–6
min one job at a time** (val1-b1 had wall 2.5 × CPU, cajuela reads). Output: 8 JSON files of ≈ 10 kB.

Light check of the file: `tools/runner/bin/qv2run status <file> --json` → `{"campaign": "p2-c-pilot-val-s1",
"counts": {"pending": 8}, "jobs": 8}` (the runner's loader accepts name, tier, prefix, ids, outputs, timeout). No
marker directory `p2-c-pilot-val*` existed before (ids unused). `qv2run ssh launch --dry-run` NOT run: it takes the
campaign's driver lock, probes the nodes and writes `_driver/ssh_dispatch.json` in the ledger, which is a launch-side
action and not mine. The B1 generator's `preflight` is for PLAN files, not applicable to this file.

## 10:55 Node proposal and launch line
Node counts [V, 10:46–10:47, `pgrep -u jdochoa -af '[q]v2run job' | wc -l`, `uptime`, `who | wc -l`]:
schrodinger 2 jobs (Z(νν) lanes; + the idle B1 lane waiting for hph), load 2.25, 2 logins; landau 1 job (channel (i)
p2-a-c1-pu1; + the idle B1 lane waiting for znn-12), load 1.36, 2 logins; **maxwell 2 jobs (channel (i) cppua, cppub),
load 2.12, 0 logins, cap 4, its pilot lane finished 03:43**; two `queue_slot.sh` of channel (i) hold those two jobs.
Proposal: **maxwell, one job at a time (node 2 → 3 of 4)**; the queue waits by itself if the node is at its cap.

Launch line (from einstein; the orchestrator launches; SLOTS.md line first):
```
ssh -x -o BatchMode=yes maxwell "mkdir -p /home/scratch/jdochoa/drivers; NODECAP=4 setsid nohup /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/p2x_queue.sh maxwell 1 /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s1.json > /home/scratch/jdochoa/drivers/p2-c-pilot-val-s1.log 2>&1 < /dev/null &"
```
Status: `/home/users/jdochoa/hllhc-quirks-search/tools/runner/bin/qv2run status /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s1.json --json`
Outputs: `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_validation/p2-c-pilot-val-s1/000/p2-c-pilot-val-s1-<s>.json`;
markers `ledger/markers/p2-c-pilot-val-s1/000/`.
Not covered: pilot.c0.hs (campaign c0-hs pending behind hph and g4h, which wait for the Z(νν) pilot): a second
one-job campaign `p2-c-pilot-val-s2` is to be written when `p2-c-pilot-c0-hs` has done jobs.
Stopped here; waiting for the orchestrator.

## Note on the times above
The headings "10:52" and "10:55" were written ahead of the clock: both entries were made at 10:47–10:48 (my
hand-over reached the orchestrator before its launch at 10:48). The content is unchanged.

## 10:53 Verdicts read (orchestrator: launched 10:48 on maxwell, complete 10:52)
`qv2run status` → 8 of 8 done. Read the 8 outputs and markers (stdlib python, JSON only). 16 of 16 files pass
`hard_except_early_product_hits`; strict `hard` fails in nix-0001 (13 hits, 5 events), ni30-0001 (1, 1), ni61-0001
(2, 1), lowpt-0001 (2, 1): 18 hits, 8 events of 469,318; every other hard item true in 16 of 16. Other chunk → other
hash in 8 of 8 streams. Cost 90.2 CPU-s (estimate 88.5), RSS max 549 MB (estimate ≈ 580).
Not explained: all 8 flagged events are in the 0001 files. Not investigated (would need a worker slot).

## 10:55 Artifact and second campaign file
- `outputs/B1_STREAM_VALIDATION_hedda_2026-11-18.md` written.
- `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s2.json` written, NOT launched (sha256 2836666e2cae…; 3 jobs
  -hs, -hspool, -g4h; `after` = b1/p2-c-pilot-c0-hs.json; `qv2run status` loads it: 3 pending). Input paths are
  built from the campaign files of c0-hs, hph, g4h (data prefix `pilot`, shard 000); they do not exist yet.
  Launch line (any time; the queue prints "waits for p2-c-pilot-c0-hs" every 2 min until that campaign is complete;
  NODE and its cap to be chosen then, maxwell shown):
```
ssh -x -o BatchMode=yes maxwell "mkdir -p /home/scratch/jdochoa/drivers; NODECAP=4 setsid nohup /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/p2x_queue.sh maxwell 1 /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s2.json > /home/scratch/jdochoa/drivers/p2-c-pilot-val-s2.log 2>&1 < /dev/null &"
```
  Eligibility: `qv2run status tools/runner/examples/p2x/b1/p2-c-pilot-c0-hs.json --json` shows 77 of 77 done (then
  hph 10 of 10 and g4h 11 of 11 are done too, by the plan's order). If a c0-hs job fails the queue waits for ever:
  stop it with `touch /home/scratch/jdochoa/drivers/STOP.p2-c-pilot-val-s2` on the node. Cost [E]: ≈ 30 CPU-s,
  ≤ ≈ 0.6 GB per job.

## 10:57 Pilot-wide count of flagged events: campaign prepared (NOT launched), on the orchestrator's yes
- `src/p2h_ephcount.py` (new, not in the frozen list, imports no pilot code): per file reads only the zip members
  `meta` and `n_early_prod` (and `evt` when the file has flagged events, to record those rows); one JSON with a
  record per file (stream, chunk, first_vertex, vertex file and its chunk, node, events, hits and events flagged,
  the meta sums for a cross-check) and totals. **Not run by me anywhere** (numpy of the acts environment must not be
  imported on einstein, and I hold no worker slot): syntax-checked only (stdlib `ast`). The job is its first run; it
  is read-only, so a failure costs only the job id (a rerun would need a new campaign name, e.g. `-eph2`).
- `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-eph_files.json`: manifest of the 546 done chain files (dif 111,
  difc 121, nix 123, nic 60, ni22 49, ni30 36, ni61 37, lowpt 9; 63.2 GB), each from the `done` line of its marker.
  A first version listed 667 entries (my glob `c0-dif*` also matched difc): caught by the count, rewritten with an
  assertion of 546 distinct paths.
- `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-eph.json`: campaign `p2-c-pilot-val-eph`, one job
  `p2-c-pilot-val-eph-0`, `max_rss_mb` 1000, timeout 1800 s; `qv2run status` loads it (1 pending).
- Cost [ESTIMATE, nothing measured: two small zip members per file over NFS, ≈ 0.2–0.5 s per file]: ≈ 1 CPU-min
  (≤ 0.03 CPU-h), 2–5 min wall, RSS < 0.3 GB.
- Node [V 10:55]: maxwell 2 jobs, load 2.1, 0 logins (the val-s2 queue there only waits); landau 2, schrodinger 2.
  Proposal: maxwell (2 → 3 of 4). Launch line:
```
ssh -x -o BatchMode=yes maxwell "mkdir -p /home/scratch/jdochoa/drivers; NODECAP=4 setsid nohup /home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/p2x_queue.sh maxwell 1 /home/users/jdochoa/hllhc-quirks-search/tools/runner/examples/p2x/b1_val/p2-c-pilot-val-eph.json > /home/scratch/jdochoa/drivers/p2-c-pilot-val-eph.log 2>&1 < /dev/null &"
```
  Output: `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_validation/p2-c-pilot-val-eph/000/p2-c-pilot-val-eph-0.json`.

## 11:02 Pilot-wide count read (orchestrator: p2-c-pilot-val-eph-0 done 11:00, 7.8 CPU-s; marker: 47 MB, 236 s wall)
546 of 546 files read, 0 errors, meta sums = array sums. 318 flagged events, 524 hits in 1.72×10⁷ events (1.85×10⁻⁵):
dif 0, difc 0, nix 212, nic 59, ni22 10, ni30 15, ni61 18, lowpt 4. Even / odd chunk index 157 / 161; nix first /
second half of the vertex file 106 / 106; chunk 0 / 1: 0 / 8 with 4.3 expected each; per-file counts Poisson in every
stream (nix χ² 136.4 / 122). The 0001-only pattern of the 16 validated files was chance. No code search needed, no
change. §6 added to outputs/B1_STREAM_VALIDATION_hedda_2026-11-18.md; §4 bullet marked resolved. Session ends.
