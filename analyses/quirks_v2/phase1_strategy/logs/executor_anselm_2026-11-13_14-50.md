# Session log: executor Anselm (feasibility A, chain port + benchmarks), 2026-11-13

- 14:43 Read AGENT_RULES, CLAUDE.md overrides, prompt §5-6, tools/PREFLIGHT.md (note: PREFLIGHT.md is in tools/, not analyses/quirks_v2/), REPRODUCE, README, INSTALL_CHECK, stage3 README, v1 pixi.toml files, JFC executor/07/11.
- 14:43 Finding: PyPI has pyacts-48.0.0 manylinux_2_34_x86_64 wheels (cp311-cp314); hosts have glibc 2.39 -> route R1 on linux-64 expected to work.
- 14:44 maxwell: load 0.2, i5-7500, 7 GiB, no swap, glibc 2.39.
- 14:45 Plan written: outputs/feasibility/plan_anselm.md.
- 14:47 Copied TT/{analytic,sim,acts,code} -> QV2 (rsync with excludes), 15.6 MB, 545 files; TT env -> envs/tt/ (QV2/pixi.toml is the JFC env). CHAIN_PROVENANCE.md written.
- 14:50 linux-64 added and solved: envs/tt, sim, acts. acts needed `{ platform = "linux-64", glibc = "2.34" }` (pyacts wheel is manylinux_2_34; pixi default 2.28 found no wheel; `[system-requirements]` is rejected when platforms carry virtual packages; key is `glibc`, not `libc`).
- 14:51 pixi install started on maxwell (NFS-bound; maxwell iowait 77 %, einstein iowait ~35 %). Killed a stray `du` over NFS of mine.
- 14:55 Linux-port edits applied (list in CHAIN_PROVENANCE.md). Stage-4 data-path overrides added (QV2_S4_DATA, QV2_S3_DATA, QV2_PYTHIA_INIT_DIR).
- 15:05 (einstein clock) envs installed on einstein locally (TT 9.6 s, acts 26.7 s, sim mg 5.2 s, ana 18.1 s). Lock diffs in outputs/feasibility/lockdiff/.
- 15:06 Toy Stage-3 inputs (T2 LO V*+jet, 60 events, F m500/m1000) on cajuela with markers. Stage-3 job lists in src/jobs/.
- 15:08 ACTS smoke_test (v1 install check) started on maxwell; cold start very slow (NFS, einstein sda saturated by a foreign writer).
- 15:12 pyacts 48.0.0 linux-64 wheel: imports and all chain components present (Blueprint, CylinderContainer/Layer/Static/MaterialDesignator nodes, json.readDetectorElementsFromJson, Fatras, addDigitization, addSeeding with GridTriplet, addCKFTracks, HepMC3); pythia8 8.312 + pyhepmc. No source build needed (R3 not attempted). TT-side Stage-4 imports OK (numpy 2.5.4, numba 0.68.1).
- 15:10 Stage-3 smoke now computing on maxwell after ~3 min cold start.
