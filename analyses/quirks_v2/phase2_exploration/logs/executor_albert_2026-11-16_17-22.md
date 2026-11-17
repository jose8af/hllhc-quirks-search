# Phase 2, channel (iii) — executor Albert (successor of Xavier and Tatiana) — plan and session log

Started 2026-11-16 17:20 -05 (`date`). `AN` = `analyses/quirks_v2`, `P2` = `AN/phase2_exploration`, `ADD3` =
`AN/phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v3_yvonne_2026-11-16_15-04.md` (v4 by session Zoe not on disk at 17:22),
`G` = `tools/runner/examples/p2x`. Tags: [V] verified (campaign or file:line), [E] estimate, [U] unverified.
**I never launch pilot campaigns** (`p2-c-pilot-*`): the orchestrator does, on the user's approval.

Read in full before planning: PHASE2_BRIEF, AGENT_RULES, agents/executor.md, ledger/README, FEAS_C §5–7 (runner how-to);
Xavier's log (all) and his five result files; Tatiana's "State for a successor"; ADD3 (all); STR §4.4 l.724-903, §4.17,
§11.7 rule 1, Df-9 / Df-11 rows; code `src/p2x_{pilot_campaigns,g4prod,b1,common,validate,hspool,hs0,mbgen}.py`,
`src/p2c_{g4vtx,handover,b1,validate,common}.py`, `p2c_campaigns.py` l.1-60, `p2x_queue.sh`; PLAN_p2-c-pilot_mb-znn.json
(frozen list).

## State for a successor (kept current; last update at the end of the file's log, see "LAST UPDATE" line)

See the section of the same name at the END of this file (rewritten at every milestone).

## 1. Plan (written 17:22–17:24 by `date`, before any code or job)

### Task A — looper gun rerun
`p2-c-px-lpd` (40 jobs) + `p2-c-px-lpds` (summary) run unattended on my one lane (queue log
`schrodinger:/home/scratch/jdochoa/drivers/p2x_lpd.log`; 3 of 40 dispatched at 17:20 [V]). A background wait of mine
watches that log. When done: read `data/p2c/px_validation/p2-c-px-lpds/000/p2-c-px-lpds-0.json`, APPEND a dated section
to `outputs/LOOPER_GUN_xavier_2026-11-16_16-38.md` (funnel next to the first run's, events recovered, seed/candidate
statement); any candidate at any rung → report at once. Corrected Geant4 fractions for the half-turn note only if cheap
(it needs `p2-c-px-htg` rerun with the fixed g4hv: 3 jobs, 0.16 CPU-h [V: Xavier's log]; decide after A).

### Task B — B1 production launch-ready (not launched)

**Design (every item a campaign parameter).**
- **B-a Code changes, all optional arguments with the default path unchanged** (noted in CHAIN_PROVENANCE.md):
  - `p2x_g4prod.py` (Xavier's; not frozen): trailing options `sel=ptlo:pthi:etalo:etahi` (pool selection window, for the
    wider `xpool_*` of pilot.mb) and `draw=weighted` (draw ∝ pool weight, for the hard-scatter pool); meta gets the
    selection, the draw mode, the number of distinct parents fired and the firings per parent. Regression: a rerun of
    `p2-c-px-g4-all-r0`'s arguments must reproduce its content hashes.
  - `p2x_b1.py` (Xavier's; not frozen): seam window as an optional argument (default 0.005 ns = validated), recorded in
    meta with the hand-over mode; two new per-event arrays `ev_mode` (0 radius, 1 time+Geant4 crossings) and
    `n_parent_inj`; the parent phase space of the vertex file copied into meta.
  - `p2x_validate.py` (Xavier's; not frozen): the check "no parent hit beyond the vertex radius" applied to the events
    whose parent has the radius cut only (it is not defined for a parent that has turned); parent phase space and road
    offset checked against the phase space recorded in the file; new mode for my pool files.
  - Nothing frozen is touched (`p2x_common.py`, `p2x_hs0.py`, `p2x_mbgen.py`, `p2x_queue.sh`, `p2c_*`, chain files).
- **B-b New files**: `src/p2a_hspool.py` (H1 pool builder: reads finished Z(νν) pilot files read-only, `had` + `evt`;
  pool = pool-phase-space hadrons/photons produced within 1 mm, inside the road of their own event, with the true offset
  and the event weight w_v1; second pool `opool_*` = the same outside the road, for the optional off-road campaign);
  `src/p2a_b1_campaigns.py` (generator: `slices`, `b1`, `preflight`, `yields`, `defaults`; python3 -I on einstein;
  reuses the job builders of `p2x_pilot_campaigns.py`, which is not modified).
- **B-c Samples** (defaults = ADD3 sizes): seven class samples dif(+k0l) 4×10⁶, difc 4×10⁶, ni22 / ni30 / ni61 10⁶ each,
  nix 4×10⁶, nic 2×10⁶; hard-scatter sample H1 2×10⁶ vertices (natural mixture, parents drawn ∝ w_v1 from the Z(νν)
  pilot's `had` lists, true road offset). Optional, each its own switch and its own campaigns: `lowpt` (0.3–0.5 GeV,
  |η| < 1), `fwd` (p_T > 0.5, 1 < |η| < 1.5), `offroad` (hard-scatter hadrons outside the road).
  "Independent parents": the pool of H1 is the distinct hadrons of the pilot events (ADD3 P2: 8.3×10⁵ parents, 19 firings
  each [E]); the number of distinct parents and firings per parent is recorded per vertex file, so the statement is
  checkable. A parent is never fired from the old generator-level slice pool (2,100 firings each).
- **B-d Hand-over modes**: first-arc class samples radius (v1); difc, nic hybrid; mixed samples autoh; seam 0.005 ns;
  β cut 0.1 (the validated variant) — all parameters; 21 road orientations recorded.
- **B-e Sizes without knowing outcomes**: Xavier's layout (usable vertices per file from measured yields with margins;
  +3 % firings in the 'all' pass; ≤ 2×10⁶ firings per Geant4 job). Yields file: `outputs/b1_yields_albert.json`
  from the partition file + the validated g4 slices (px-g4 and my pa-g4), separately for mb pool, hs, lowpt, fwd, offroad.
- **B-f Separation**: slices = campaigns `p2-c-pa-*`, streams `pa.*`, data prefix `p2c/pa_validation`; production =
  `p2-c-pilot-{g4a,g4n,hsp,g4h,c0-*,…}`, streams `pilot.g4`, `pilot.c0.*`, data prefix `pilot`. Slices READ pilot.mb and
  Z(νν) pilot files (read-only inputs) and write only under the validation prefix.

**Slice campaigns (schrodinger, ONE lane, `p2x_queue.sh schrodinger 1 …`; budget ≈ 5 CPU-h).**
| campaign | jobs | content | CPU-h [E] |
|---|---|---|---|
| `p2-c-pa-val0` | 1 | validation job on Xavier's `p2-c-px-g4` (10 jobs' vertex files) and `p2-c-px-b1` (24 files, radius cut): never validated | 0.1 |
| `p2-c-pa-hsp` | 3 | H1 pool from the Z(νν) pilot files done so far: r0, r1 (same inputs), d (other files) | 0.02 |
| `p2-c-pa-g4` | ≈ 12 | regression of the default path (= px-g4-all-r0); 'all' 2×10⁶ and 'ni' 1.25×10⁷ at full job size from REAL pilot.mb pools; hs weighted r0/r1/full; lowpt, fwd, offroad 10⁶ each | 1.3 |
| `p2-c-pa-b1` | ≈ 45 | every sample type (7 class samples, hs, lowpt, fwd, offroad) in its production mode: r0/r1/other seed at 2,000 events and one job at full job size (25,000; 50,000 for two, to size jobs) | 0.9 |
| `p2-c-pa-val1` | 1–2 | validation of all pa files: hard checks, parent crossings with multiplicity ≤ 2 %, reruns, sizes | 0.2 |
| `p2-c-pa-lt-*` | ≈ 10 | launch test of the generated LAUNCH/STATUS on a dummy set (needs 2 and 3 lanes: only when a node has room; ask the orchestrator) | 0.05 |
| **sum** | | | **≈ 2.6** (ceiling 5) |

**Checks per sample type**: Xavier's hard checks; one class per vertex/event (asserted in the jobs, recomputed in the
validation); parent crossings with multiplicity ≤ 2 %; same seed → same content hash, other seed differs; CPU and max
RSS from markers → events per job for ≤ 30 min (target ≤ 20) and RSS request; bytes per event.

**Deliverables**: campaign files `G/b1/p2-c-pilot-*.json`, `PLAN_*.json` with `frozen_from_launch`, LAUNCH (2, 3 lanes) /
STATUS scripts, preflight, `outputs/B1_READY_albert_<stamp>.md`, lines in SLOTS.md / DAILY_NOTES.md / experiment_log.md.

**Order**: (1) val0 now behind lpd on the same lane; code while it runs; (2) report A when lpd ends; (3) hsp, g4, b1,
val1; (4) yields, generator, campaign files, preflight, launch test; (5) B1_READY. Deadline 18 Nov midday.

## 2. Log
- 2026-11-16 17:20 start. schrodinger: 3 `qv2run job` (pilot mb, pilot znn-00, p2-c-px-lpd) [V: pgrep]; pilot markers
  mb 2 done, znn-00 3 done, 0 failed [V]. Reading. Background wait on p2x_lpd.log started.
- 2026-11-16 17:24 plan written (an earlier wording of this line carried an estimated time; corrected from `date`).
- 2026-11-16 17:24–17:33 Code (jobs not started; nothing of mine runs yet besides Xavier's `p2-c-px-lpd` queue): `p2x_g4prod.py`
  (+ `sel=`, `draw=weighted`), `p2x_b1.py` (+ seam argument, `ev_mode`, `n_parent_inj`), `p2x_validate.py` (per-mode
  parent checks, recorded phase space, mode `hspool-x`), new `p2a_hspool.py`, `p2a_b1_campaigns.py` (slices, yields, b1,
  preflight). CHAIN_PROVENANCE.md entry written. Slice campaign files written by
  `python3 -I src/p2a_b1_campaigns.py slices` → `tools/runner/examples/p2x/slices_pa/p2-c-pa-{val0,hsp,g4,b1,val1}.json`
  (they will be regenerated once, just before the launch, to take the Z(νν) files finished by then into the big pool);
  `p2-c-pa-htg.json` written inline (copy of `p2-c-px-htg`, jobs znn and mb, new ids: the Geant4 reference of the
  half-turn note with the transportation-ended tracks). Generator dry run with provisional yields in my scratchpad:
  class block 45 CPU-h in 656 jobs, hs 5.1, lowpt 0.5 [E; to be replaced by the plan made from measured yields].
  Design change against the plan: a Geant4 pass is cut into campaigns of 16 jobs and each class sample into one chain
  campaign per part (parameter `g4.files_per_part`), so that 2 or 3 lanes share the work (3 lanes: 20 h instead of ≈ 24).

- 2026-11-16 17:59 **Task A done [V: p2-c-px-lpd 40/40 (0.55 CPU-h), p2-c-px-lpds].** Rerun against first run: events recovered 985 (nat) /
  1,003 (flat); finder trials 96,153 → 97,137 / 96,147 → 97,149; seed triple 72,105 → 72,773 / 73,756 → 74,446; seed ≥ T_seed
  33 → 33 / 34 → 34; candidates 0 / 0; every rung 0. Section "Rerun with the transportation-ended tracks included" appended
  to outputs/LOOPER_GUN_xavier_2026-11-16_16-38.md. No candidate → no immediate alarm. Addendum v4 (Zoe, 17:26) read
  (§0.3, §3): sizes, class list, lowpt alarm 2×10⁵, hand-over per stream as my defaults; it asks for the class-aware radius
  check in the validator (done in p2x_validate.py) and "one validated job per stream".
- 17:58 Slice queue started on my one lane (pgrep before: 2 = the pilot lanes; SLOTS.md line):
  p2-c-pa-val0, -htg, -hsp, -g4, -b1, -val1; log schrodinger:/home/scratch/jdochoa/drivers/p2a_slices_1.log. The slice
  campaign files were regenerated at 17:58 before the launch (hsp-big = 6 finished Z(νν) files).
- 2026-11-16 18:13 **val0 read [V: p2-c-pa-val0-0.json; 28.4 CPU-s].** Xavier's vertex files (p2-c-px-g4, 40 group files): every hard check
  passes, classes recomputed equal, yields against the partition within |z| ≤ 1.6, reruns identical. p2-c-px-b1 (24 files,
  radius cut): first-arc streams pass everything, parent crossings without a hit 0.00–0.18 %; difc / nic / hs / lowpt fail
  the ≤ 2 % criterion as known (58.5 / 66.5 / 37.9 / 60.2 %). **NEW: in the 25,000-event files the hard check "no product
  hit before the vertex time" fails: 6 hits in nix-big, 1 in nic-big (0 in dif-big and in every 2,000-event file).** Not seen
  before because no file of that size had been validated. Diagnostic job p2-c-pa-dg1 (src/p2a_diag_early.py) written;
  queue 1 stopped by its STOP file after p2-c-pa-htg; queue 2 (log p2a_slices_2.log, started 18:12, pgrep before: 2):
  p2-c-pa-dg1, -hsp, -g4. The chain slices p2-c-pa-b1 wait for the diagnosis.
- 2026-11-16 18:13 Half-turn reference corrected [V: p2-c-pa-htg 2/2, 0.20 CPU-h]: section appended to
  outputs/HALF_TURN_xavier_2026-11-16_16-08.md (crossings 958 → 965 per Z(νν) event, missing 209 → 210; 312 → 314, 91.0 → 91.5
  per minimum-bias interaction; no statement changes).
- 18:13–20:11 Slices [V; markers]: queue 2 (p2-c-pa-dg1, -hsp 4/4, -g4 12/12, 0.91 CPU-h), queue 3 (p2-c-pa-b1 51/51, 0.65 CPU-h;
  p2-c-pa-val1 2/2), queue 4 (p2-c-pa-dg2). Regressions pass (g4-reg = px-g4-all-r0 hashes; b1 reg-difc sha_hits = px-hy-difc-r0).
  val1-g4: 48 of 48 files pass. val1-b1: 47 of 51 pass; 4 fail only "product hit before its own production time" (nix-full,
  offroad-full, nix-b15, nix-b20): slow protons / deuteron, β 0.13–0.21, Fatras hits 12–35 ns before production; 4 events in
  4.3×10⁵; β scan 0.1 / 0.15 / 0.2 / 0.3 → 2 / 1 / 2 / 0 events of 25,000. Parent-crossing criterion: ≤ 0.26 % in all 11 sample types.
  Added after dg1: `n_early_prod` per event in p2x_b1.py, own-production-time check in p2x_validate.py, β and seam in its rerun key,
  β-scan and nix-xl jobs in the b1 slice file (edited while no job read these scripts).
- 20:11 `yields` → outputs/b1_yields_albert.json; costs into DEFAULTS; `b1` → tools/runner/examples/p2x/b1/ (39 campaigns, 762 jobs,
  48.4 CPU-h, 90.8 GB; 26.3 h on 2 lanes, 19.1 h on 3); preflight 0 failed checks. Optional plans → …/p2x/b1_optional/ (fwd, offroad).
- 20:12–20:23 Launch test on ONE lane (p2-c-pa-lt-*, 33 jobs; SLOTS.md line): first attempt died at once (relative --outdir → relative
  campaign paths on the worker; fixed: the generator resolves the path); then launch, double-launch guard, STOP, resume, completion,
  relaunch, STATUS, preflight-on-finished all behave as intended. p2-c-pa-val2 on its 48 outputs: all hard checks pass.
  The real plan was regenerated after the last generator edit (hashes in the PLAN are the final ones) and preflighted again.
- 2026-11-16 20:27 outputs/B1_READY_albert_2026-11-16_20-24.md written. CPU of my campaigns [V: markers]: 1.90 CPU-h (p2-c-pa-*), plus Xavier's
  p2-c-px-lpd 0.55. Pilot markers at 20:24: mb 14 done, znn-00 19 done, 0 failed.

## State for a successor (LAST UPDATE 2026-11-16 20:27)

**Rules that bind (besides Xavier's list, his log l.149).** I NEVER launch `p2-c-pilot-*` (the orchestrator does). ONE lane on
schrodinger while the pilot runs (`p2x_queue.sh schrodinger 1 …`), never two queues of mine at once; check
`ssh -x schrodinger "pgrep -u jdochoa -af '[q]v2run job' | wc -l"` (≤ 2) and append a line to SLOTS.md. Never edit a script or
campaign file a running queue reads. Give the generator ABSOLUTE paths. `date` for every time. No git, no subagents.
Frozen (pilot part 1): list in tools/runner/examples/p2x/pilot/PLAN_p2-c-pilot_mb-znn.json. **Once the B1 plan is launched, the
files of its `frozen_from_launch` are frozen too (p2x_g4prod.py, p2x_b1.py, p2a_hspool.py, …): do not regenerate or edit.**

**Nothing of mine is running.** Task A is done (LOOPER_GUN and HALF_TURN notes have their appended sections).

**Task B: launch-ready except two points.** Read outputs/B1_READY_albert_2026-11-16_20-24.md (it has every number and command).
1. DECISION PENDING (orchestrator / user): the slow-proton residue (§2 of B1_READY): keep β_min 0.1 with events flagged by
   `n_early_prod` (as generated), or another cut (regenerate: `--set beta_min=… --set unvalidated_ok=true`, then a full-size NI
   slice + validation), or a hit filter (new code).
2. TO DO on the morning of 17 Nov: 2- and 3-lane launch test. Ask the orchestrator for 3 slots for 20 min, then
   `python3 -I src/p2a_b1_campaigns.py b1 --params <abs>/launch_test_b1/params_lt.json --set name=t2 --outdir <abs>/launch_test_b1_t2`,
   preflight, `bash …/LAUNCH_p2-c-pa-lt-t2_b1_2slots.sh NODE` (then a third set, name=t3, for the 3-lane script), STATUS, and a
   validation job as tools/runner/examples/p2x/slices_pa/p2-c-pa-val2.json. Record the result in B1_READY §6.
3. If addendum v4's review changes sizes / populations: B1_READY §7 (regenerate; preflight). After ANY regeneration the PLAN,
   campaign files and scripts in tools/runner/examples/p2x/b1/ are rewritten: tell the orchestrator.
4. After the launch (by the orchestrator): validate one job per stream (B1_READY §5 step 6).

**Files.** Code: src/p2a_hspool.py, p2a_b1_campaigns.py, p2a_diag_early.py (mine); p2x_g4prod.py, p2x_b1.py, p2x_validate.py
(Xavier's, extended; CHAIN_PROVENANCE.md). Yields: outputs/b1_yields_albert.json. Campaign files: tools/runner/examples/p2x/
{b1, b1_optional, launch_test_b1, slices_pa}. Slice data: data/p2c/pa_validation/<campaign>/000/; validation JSONs
p2-c-pa-val0-0.json, p2-c-pa-val1-{g4,b1}.json, p2-c-pa-val2-0.json; diagnostics p2-c-pa-dg{1,2}-0.json.
Queue logs: schrodinger:/home/scratch/jdochoa/drivers/p2a_slices_{1..5}.log, p2-c-pa-lt_b1_1slots_lane0.log.
- 2026-11-17 08:38 (17 Nov) **Multi-lane launch test done on the orchestrator's instruction of 08:15** (one lent slot on each of schrodinger,
  landau, maxwell; SLOTS.md lines at start and release): sets p2-c-pa-lt-t3 (3 lanes, 3 nodes), -t2 (2 lanes, 2 nodes), -t4 (wait
  across nodes), validation p2-c-pa-val3 (96 files pass); 0.22 CPU-h. Every item PASS (table in B1_READY §9). Generator change: LAUNCH
  scripts take NODECAPS (per-lane node cap; maxwell needs 4); real plan + optional plans regenerated 08:37, the 39 campaign files
  byte-identical (b72b6fd5…), preflight 0 failed. Decision received: residue handled as option (a), β stays 0.1, no regeneration.
  **State for a successor, update:** point 1 (decision) and point 2 (multi-lane test) of the section above are CLOSED. Nothing of
  mine runs. Remaining: after the orchestrator's launch, one validation job per stream (B1_READY §5 step 6); regenerate only if the
  addendum review changes a parameter (B1_READY §7), and never once the B1 plan is launched.
