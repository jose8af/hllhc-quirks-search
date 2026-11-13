# Experiment log — phase1_strategy (append-only)

## [Anselm] 2026-11-13 14:45 feasibility A started; plan at outputs/feasibility/plan_anselm.md

## [Boris] 2026-11-13 — runner design decisions
DECISION: campaign files in JSON (stdlib only; JSON is valid YAML for argo submit); wrapper in Python run from a
minimal pixi env under tools/runner/ (pod image has no Python); accounting via os.wait4 rusage.
ALTERNATIVES: YAML (needs PyYAML); bash `times` + /proc polling (misses short RSS peaks).
CONFIDENCE: HIGH
FLAG FOR HUMAN: NO

DECISION: test markers go to phase1_strategy/outputs/feasibility/runner_ledger/markers (per-campaign `ledger`
field), not the production ledger/markers, so ledger/jobs.tsv holds production only.
ALTERNATIVES: production ledger with tier=test rows.
CONFIDENCE: HIGH
FLAG FOR HUMAN: NO

## 2026-11-13 investigator Albert (D3 corrections/book)
- Table 29.2 reproduced exactly from STAGE4_SUMMARY.json with ch29_checks.py functions (VERIFIED). Inputs are four full-chain points at 3-5 keV.
- book/checks: ch25 runs as is (94 PASS); ch26/ch27 pass after macOS path fix (147, 139 PASS); ch28/ch29 fail: need untracked book/answers/ and book/figure_src/.
- FLAG FOR HUMAN: plan's "rows 1 to 4 into one freeze" does not match the book's ranking (row 1 data anchor, row 4 mQ/Lambda); plan's B84~0.17 "systematic floor" is a data-sideband B84, width 1.105. See digest D3 §6.

### [Anselm] 2026-11-13 15:00 FINDING: pixi installs onto /home/users are metadata-bound on einstein's disk
- maxwell `pixi install` of the TT env (148 linux-64 packages): 36 packages after 11 min; maxwell NIC 50-150 kB/s; maxwell iowait 77 % (45 threads in D state).
- einstein `sda` (holds `/home`, ext4): 91 % busy at 1.3 MB/s writes (10 s `/proc/diskstats` delta) -> many small synchronous NFS commits, not bandwidth. Basil's `pixi install` (sw/envs/mg, schrodinger) ran at the same time.
- Consequence for v2: environment installs and any many-small-files output on `/home/users` are expensive and slow the whole lab; install each env once, serially, and never write small files per event to /home or cajuela.

### [Anselm] 2026-11-13 15:08 DECISION: run the remaining pixi installs on einstein (local disk), not over NFS from maxwell
DECISION: stop the maxwell-side install (46/148 packages after ~20 min) and run `nice -n 19 ionice -c3 pixi install` on einstein, serially, one workspace at a time.
ALTERNATIVES: keep installing from maxwell over NFS (estimated > 1 h per env at 91 % busy on einstein sda, blocking the whole lab's /home); install node-local under /home/scratch (violates "envs under /home/users", not shared).
REASON: the bytes land on the same disk (einstein sda = /home) either way; locally they are buffered writes, over NFS each small file is a synchronous commit. Einstein work stays niced and idle-class I/O; it is one-off.
CONFIDENCE: MEDIUM (einstein is meant for light work only; this is moderate I/O for minutes instead of heavy NFS I/O for hours)
FLAG FOR HUMAN: YES (orchestrator: informed in the artifact)
- [Anselm] 15:15 result: on einstein (local disk) `pixi install`: TT 9.6 s wall, acts 26.7 s wall (vs. 46/148 packages in ~20 min over NFS from maxwell). Installing envs on einstein is the right procedure; use it for every v2 env (one at a time, nice 19, ionice -c3).

## [Basil] 2026-11-13 — generators + Geant4 feasibility (executor B)
- [Basil] FAILED ATTEMPT: `https://launchpad.net/mg5amcnlo/2.0/2.9.x/+download/MG5_aMC_v2.9.22.tar.gz` returns an HTML 404
  page. The 2.9.x LTS files live under `.../mg5amcnlo/lts/2.9.x/+download/`; md5 bb67626ef4e607b31c4544af8fa91e7b matches
  launchpad's `+md5`.
- [Basil] FAILED ATTEMPT: `https://pythia.org/download/pythia83/pythia8313.tgz` is a 404; the release lives at
  `https://pythia.org/releases/pythia83/pythia8313.tgz`.
- [Basil] DECISION: MG5 2.9.22 runs under a pixi env with Python 3.9 (+six, numpy 1.26, conda-forge LHAPDF 6.5.x), as v1.
  ALTERNATIVES: system Python 3.12 (MG starts, but prints "python3.12 support is still experimental ... re-weighting is
  NOT working ... We do not advise python3.12 for production"; log `sw/mg5/sys_py312_test.log`); Python 3.10/3.11 (untested
  by v1). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.
- [Basil] DECISION: MG install config `input/mg5_configuration.txt`: `auto_update = 0` (the update prompt otherwise blocks
  every non-interactive start for 60 s). The release copy is kept as `sw/mg5/mg5_configuration.release.txt`. Unlike v1, this
  install is ours and is configured once; per-output `Cards/me5_configuration.txt` still carries the tool paths.
- [Basil] PDF patch kept: the official CT18NLO.info (lhapdfsets/current, sha256 of tarball c9127231…) lacks
  `AlphaS_FlavorScheme`, `AlphaS_NumFlavors`, `AlphaS_Lambda4`, `AlphaS_Lambda5`; the official NNPDF23_lo_as_0130_qed.info
  lacks `AlphaS_FlavorScheme`, `AlphaS_NumFlavors`. v1 added them because LHAPDF 6.5.5 + MG's Fortran glue need them
  (TT/sim/plan.md l.56; REPRODUCE §2.3). The tracked v1 `.info` files are used verbatim in `sw/lhapdf_data/`.
- [Basil] OBSERVATION: two concurrent `pixi install` on the shared rattler cache (mine on schrodinger + Anselm's on
  maxwell, and my own mg + g4) block each other for minutes at 0 % CPU (package-cache locks over NFS). Serialise installs.

## [Boris] 2026-11-13 — FAILED ATTEMPT: pyhf toys with numpy 2.5.4
pyhf 0.7.6 (latest on conda-forge at install) + numpy 2.5.4: toy-based hypotest fails with
`TypeError: percentile() got an unexpected keyword argument 'interpolation'` (pyhf/tensor/numpy_backend.py:347).
Fix: pin numpy 2.2.* in phase1_strategy/src/pyhf_bench/pixi.toml. T1 must pin numpy the same way (or patch pyhf).

### [Anselm] 2026-11-13 15:10 FINDING: cold start of a pixi env over NFS is minutes, not seconds
- First `pixi run python scripts/smoke_test.py` in the acts env on maxwell: the python process stayed in D state (2 s CPU after > 5 min) reading the env (28.9k files) over NFS; maxwell NFS rx 44 kB/s.
- einstein `sda` (rotational HDD, holds /home): 91 % busy, 67 write ops/s, 0.9 MB/s write, 0 reads, nfsd and jbd2/sda4 in D state; the writer is not one of my processes (not attributed: no root).
- Consequence: per-node first use of an env costs minutes; production jobs must be warmed per node (or the env staged into node-local scratch once per node, with the same path semantics settled by the runner owner). Benchmarks below separate cold and warm runs.

## [Boris] 2026-11-13 15:06 — FINDING: NFS metadata latency on /home dominates job start-up
Wrapper start-up (process start -> ready) measured 0.9 s in a quiet moment (14:58) and 10-25 s at 15:00-15:06, in
pods and over SSH alike. strace on landau: ~570 stat + 134 openat on /home/users during Python start-up; single
stat latency 0.13 s cold. At the same time einstein had load 11 with all 8 nfsd threads and jbd2/sda4 in D state.
Not a runner bug; it affects every job whose interpreter lives on /home (all pixi envs). Cost per 30-min job:
< 1.5%. Flag for orchestrator: keep heavy metadata work (pixi installs, untar, builds) off /home while campaigns run.
DECISION: accept; record per-job start-up latency in markers (t_proc_start, t_wrapper) so it is monitored.
ALTERNATIVES: copy the runner env to node scratch (python is relocatable for stdlib-only use) — deferred.
CONFIDENCE: MEDIUM
FLAG FOR HUMAN: YES (NFS server nfsd thread count / load is an admin matter)
- [Anselm] 15:09 attribution: the foreign /home writer is schrodinger (~700 kB/s NFS writes, `/proc/self/mountstats` bytes delta) = a `pixi install` in `sw/envs/mg` over NFS (executor Basil's area; not touched). Orchestrator informed (SendMessage) with the einstein-local install workaround.

### [Orchestrator] 2026-11-13 15:12 INTERRUPTION (see ../LOG.md 15:12 entry)
einstein OOM killed Anselm, Basil, Boris and the orchestrator; cajuela was down 15:12–15:20. All pixi envs verified complete except `sw/envs/g4` (deleted, to be reinstalled). The decision of 15:08 to run pixi installs on einstein is REVOKED by the user: no installs, solves, builds or benchmarks on einstein; one install at a time, from a worker, with no jobs running.
