# Phase 2, channel (iii) — executor Xavier (successor of Tatiana) — plan and session log

Started 2026-11-16 14:19 -05 (`date`). Task: make the pilot campaigns **ready to submit** (code, slice tests, campaign
files, dry checks). **The pilot is NOT submitted by me.** `AN` = `analyses/quirks_v2`, `P2` = `AN/phase2_exploration`,
`ADD` = `AN/phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v2_tatiana_2026-11-16_14-14.md` (in re-review; not edited),
`STR` = `AN/phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`. Tags: [V] verified (file:line or campaign),
[E] estimate, [U] unverified.

Read in full before planning: PHASE2_BRIEF, AGENT_RULES, CLAUDE.md overrides, agents/executor.md, ledger/README, FEAS_C §7
(runner how-to) and `tools/runner/qv2run/{campaign,cli,paths}.py`; Tatiana's log (all) and EXPLORATION_iii; ADD and its
fix report; `outputs/partition_p2-c-part-0.json`; STR §4.4, §4.7, §4.17, §11.7, §12.1 rows Df-9 and Df-11; code
`src/p2c_{common,g4vtx,mbgen,b1,handover,hs0,validate,campaigns}.py`, `src/g4/{g4hv.cc,g4hv.sh}`,
`acts/stage4/code/{run_chain.py l.1-300, s4pu.py l.1-152, l.200-296}`, `acts/stage4/analysis/gen_d123.py l.40-190`.

## 1. Plan (written before any code or job)

### 1.1 Design decisions (each is a parameter, none hard-coded in a job script)
- **D-a Vertex production, one mechanism for every parent pool.** New `p2x_g4prod.py`: reads a parent pool from pool
  files (`pool_pdg/pt/eta` arrays: the minimum-bias files of `p2x_mbgen.py`, their low-pT pool, or the hard-scatter
  pool of `p2x_hspool.py`), fires through `p2c_g4vtx.fire` (unchanged: uniform azimuth, luminous-region vertex, pool
  sampled with replacement, slab-exit hand-over), classifies with `p2c_g4vtx.classify` + `first_arc` (unchanged) into
  ten exclusive classes (dif, difc, k0l, ni22, ni30, ni61, nix, nic, conversion, other), **asserts one class per
  vertex**, and writes one vertex file per *group* (group = the classes of one pilot sample, e.g. `dif=dif+k0l`), so a
  chain job reads only the vertices of its own sample (≈ 1/5 of the bytes; no multi-GB file streamed by many jobs).
  Every vertex keeps its pool provenance (pool file, pool row, source interaction/event, source weight, road offset if
  the pool has one). Conversions and "other": counted in the partition, products not stored (STR §4.4 pt 1).
- **D-b Chain job with a class list.** New `p2x_b1.py` (p2c_b1.py unchanged): sample = list of classes (DIF sample =
  dif OR k0l), events = vertices `[first, first+n)` of ONE group file in file order; fails loudly if the file holds
  fewer. Adds per event: class code, parent pT/η/φ at origin, road offset (stored draw), vertex radius, z, layer
  name code, vertex time, pool provenance, source weight.
- **D-c A-priori exact sample sizes.** The campaign generator computes, per class, events per vertex file from the
  measured yields with a safety margin (yield error and 5σ Poisson), so every job reads one file, M is exact, and no
  campaign file depends on the outcome of an earlier campaign.
- **D-d Road offset.** N_t of ADD P2 counts parents inside a road of half-width 0.15. The stored uniform `phimet`
  draw of p2c_b1 puts the parent in the road in only 4.8 % of the events. p2x_b1 stores in addition
  `road_dphi` ~ U(−0.15, 0.15) and `phi_road = phi_parent(origin) − road_dphi` (hard-scatter pool: the true offset to
  the event's road axis instead of a draw). Phase 3 remains free to choose (plan O8 of Tatiana); nothing is cut.
- **D-e `pilot.c0.hs`** comes from the same mechanism: `p2x_hspool.py` generates Z(νν) events at generator level
  (s4pu.HardScatter unchanged, v1 preselection weight stored), keeps the pool-phase-space parents inside the road of
  the event (|Δφ(parent, φ_MET,reco v1)| < 0.15, as `gen_d123.road_objects`), → `p2x_g4prod` → `p2x_b1` with all eight
  classes in their natural mixture, class recorded per event.
- **D-f `pilot.c0.lowpt`**: `p2x_mbgen.py` (wrapper; `p2c_mbgen.generate` unchanged, its module constant POOL_PT set
  at run time to (0.3, 20)) writes the main pool (pT > 0.5, identical rows to p2c_mbgen) and a `lowpt_*` pool
  (0.3 < pT ≤ 0.5) with its rate per interaction (the N_t input ADD asks for).
- **D-g Z(νν)**: `p2x_hs0.py` (p2c_hs0.py unchanged, its `gen_summary` reused): adds a generator summary for the v2 MET
  model (scalar and vector sums of the visible final state in |η| < 5 and < 3, jets down to 15 GeV, τ_h candidates)
  and a truth table of the particles that have written hits (pdg, pT, η, φ, production point), needed to attribute
  own-hit candidates to prompt pairs / conversions / V⁰ (STR §4.7 B4-c split). Size impact measured on the slice.
- **D-h Reproducibility**: every job stores `content_sha256` (hash of all physics arrays, timing excluded) in `meta`
  and in a small side file `<job>.sha.json`; the slice campaigns run each sample type twice with the same seed and
  once with another chunk.
- **D-i Separation**: slices use streams `px.*`, campaigns `p2-c-px-*`, data prefix `p2c/px_validation`; the pilot
  uses streams `pilot.*`, campaigns `p2-c-pilot-*`, data prefix `pilot`. No slice file is readable by a pilot job
  (paths are generated; the pilot generator refuses any input path containing `px_validation`).

### 1.2 Scripts (all new files in `P2/src/`, logging not print; none of Tatiana's files is modified)
| script | env | purpose |
|---|---|---|
| `p2x_common.py` | — | class codes, content hash, pool readers, input hashes |
| `p2x_mbgen.py` | acts | minimum bias with main + low-pT pools |
| `p2x_hspool.py` | acts | hard-scatter parent pool (generator level) |
| `p2x_g4prod.py` | acts + g4 | production vertex files per group, partition assert |
| `p2x_b1.py` | acts | chain job for a class list |
| `p2x_hs0.py` | acts | Z(νν) pilot job with the extended summary |
| `p2x_validate.py` | acts | hard checks (p2c_validate.one reused), partition, reproducibility, yields against the partition file, sizes |
| `p2x_pilot_campaigns.py` | python3 -I (einstein) | campaign generator: `slices` and `pilot` from a parameter set |

### 1.3 Slice campaigns (schrodinger only; ≤ 2 concurrent jobs of mine; node ≤ 3; budget ≈ 4 CPU-h)
| campaign | jobs | content | CPU-h [E] |
|---|---|---|---|
| `p2-c-px-mb` | 4 | mbgen 2×10⁴ interactions ×(r0, r1 same seed, d other chunk) + one job at 1.25×10⁵ (time, RSS) | 0.25 |
| `p2-c-px-hsg` | 3 | Z(νν) generator-level pool, 2,000 events × (r0, r1, d) | 0.08 |
| `p2-c-px-g4` | 9 | 'all' pass 2×10⁵ firings × (r0, r1, d) + 2×10⁶ (half job size); 'ni' pass 10⁶ × (r0, r1) + 10⁷; hs pool; low-pT pool | 0.7 |
| `p2-c-px-b1` | ≈ 22 | 2,000 events of each of the 9 samples × (r0, r1), d for two, one 25,000-event job | 0.3 |
| `p2-c-px-znn` | 4 | 500 events × (r0, r1, d) + 5,000 (job size) | 0.25 |
| `p2-c-px-val` | 1–2 | validation of everything above | 0.02 |
| **sum** | | | **≈ 1.6** (ceiling 4) |

### 1.4 Checks per slice
Hard checks of Tatiana's hand-over validation (V4-1 closure, no NaN, offsets, distinct seeds, no parent hit beyond the
vertex radius, no product hit before its production time); one class per vertex / event and class ∈ sample; same
seed → identical `content_sha256`; other chunk → different; yields per firing against the partition file
(compatibility, not a tuned number); CPU and max RSS per job from the markers → job sizes for ≤ 30 min (target ≤ 20 min).

### 1.5 Deliverables
Campaign files `tools/runner/examples/p2x/p2-c-pilot-*.json` (not launched), `P2/outputs/PILOT_READY_xavier_<stamp>.md`,
this log, lines in SLOTS.md, DAILY_NOTES.md, experiment_log.md.

## 2. Log
- 2026-11-16 14:19 start; reading.
- 2026-11-16 14:23 schrodinger: load 0.62, graphical login screen of another user (node cap 3), one job of mine-user
  running (`p2-c-toy-jax`, session Viktor) [V: ssh pgrep]; cajuela 3.9 T free; /home/scratch 514 G free. Plan written.
- 2026-11-16 14:34 Code written (all new files, none of Tatiana's modified): src/p2x_{common,mbgen,hspool,g4prod,b1,hs0,validate,pilot_campaigns}.py, src/p2x_queue.sh.
  Correction to plan D-f: the main pool is split from the low-pT pool on the stored float32 pT (> 0.5), so a parent within 3e-8 GeV of the edge may fall on the other side than in p2c_mbgen: not "identical rows", identical up to that edge effect.
  Change to plan §1.3: reruns for reproducibility are separate job ids with the same stream and chunk (r0, r1); "d" = another chunk; "big" = half or full pilot job size.
- 2026-11-16 14:34 Slice campaign files written by `python3 -I src/p2x_pilot_campaigns.py slices` -> tools/runner/examples/p2x/slices/p2-c-px-{mb,hsg,znn,g4,b1,val}.json. pgrep count on schrodinger before launch: 1 (Viktor). SLOTS.md line appended. Queue started 14:32 on schrodinger (2 slots): mb, hsg, znn, g4, b1; log schrodinger:/home/scratch/jdochoa/drivers/p2x_slices_1.log.
- 14:33 p2-c-px-mb-r0 / -r1 (same stream and chunk): content_sha256 identical 3cb20284… [V: data/p2c/px_validation/p2-c-px-mb/000/*.sha.json]; 70.7 / 71.2 CPU-s for 2×10⁴ interactions.
- 2026-11-16 14:37 Process note: I edited src/p2x_queue.sh (added the wait for the campaigns listed under "after") while my slice queue was running that script; bash reads a script by byte offset, so the running queue (pid 1935414) was killed by pid before it could read on, its driver for p2-c-px-mb left to finish, and the queue restarted with the new script once that driver exits (log p2x_slices_2.log). No job was affected. Rule for myself: never edit a queue script while a queue runs.
- 2026-11-16 14:44 **Orchestrator message received (re-review of addendum v2 by Wanda: ITERATE, 2 A / 5 B / 12 C; read in full: phase1_strategy/review/critical/ADDENDUM_1_v2_CRITICAL_REVIEW_wanda_2026-11-16_14-37.md).** New order of work: (1) Z(νν) pilot and pilot.mb launch-ready first (review C-8 added to the Z(νν) summary), slice-verified, campaign files appendable; STOP and report; (2) A-1: time truncation for DIF-C / NI-C with a before/after table; (3) B-4: B1 production code (independent hard-scatter parents, β cut as a campaign parameter, ≤ 2×10⁶ firings, +3 % NI-X, road orientations). The pilot is launched by nobody but on the orchestrator's go.
- Slice results so far [V: markers ledger/markers/p2-c-px-{mb,hsg}/000]: p2-c-px-mb-big 1.25×10⁵ interactions 452.3 CPU-s = 3.60 ms per interaction, max RSS 236 MB, 142 B per interaction; hsg r0 / r1 76.4 / 76.8 CPU-s for 2,000 generated Z(νν) events.
  **Bug found by the slice and fixed:** p2x_mbgen (first version) set p2c_mbgen.POOL_PT at run time; that constant also enters the v1 road rates, which came out at 0.0164 (dif) instead of ≈ 0.0080 [V: log of p2-c-px-mb-big]. p2x_mbgen.py rewritten with its own loop (copy of p2c_mbgen.generate l.48-103, v1-rate cuts as fixed numbers, pool rows by the float64 cuts of p2c_mbgen l.88, a wider second pool `xpool_*`: 0.3 < pT < 20, |η| < 1.5 outside the main pool, which also serves review B-2). The p2-c-px-mb files are superseded; new slice p2-c-px-mbb. The validation now compares the v1 rate with the partition file (hard check, 15 %).
- p2x_hs0.py extended before the Z(νν) slice started (14:43): `had` (final hadrons and photons, |η| < 1.5, pT > 0.3: pdg, pT, η, φ, production r and z), `nu` (every neutrino), gsum + ΣE_T (|η| < 5, < 3), p̂T, generator weight.
- Queue: STOP file set for the first queue after p2-c-px-znn; second queue (log p2x_slices_3.log) runs p2-c-px-mbb, p2-c-px-val1 (mb + Z(νν) validation), then the B1 slices p2-c-px-g4, p2-c-px-b1 (old mb pool files; they serve steps 2 and 3 as the "before" state).
- 2026-11-16 14:44 p2-c-px-znn: 4 jobs FAILED at the first event (my bug: a variable named `had` in the τ loop of p2x_hs0.extra_summary overwrote the hadron list; TypeError). Fixed (renamed); new slice p2-c-px-znnb (failed jobs are never rerun under the same id). 0.01 CPU-h lost. Queue 3 stops after p2-c-px-mbb (STOP file); queue 4 (log p2x_slices_4.log): p2-c-px-znnb, p2-c-px-val1b, then p2-c-px-g4, p2-c-px-b1.
- 2026-11-16 15:06 p2-c-px-val1b failed in 0.5 s (my validator read meta['bytes'], which is not stored inside the file); fixed (file size from the file system); rerun as p2-c-px-val1c; queue 5 (log p2x_slices_5.log): val1c, g4, b1, tr (truncation test, 27 jobs), val2. pgrep before launch: 1 1 .
- 2026-11-16 15:10 **Step 1 slices done and validated [V: p2-c-px-mbb, p2-c-px-znnb, p2-c-px-val1c].** Validation: all hard checks pass on 9 files, reruns identical (mb 1a1ce790…, Z(νν) 8c911f8e…), other chunks differ, stored hash = recomputed hash. Minimum bias: 3.56 ms per interaction, 215 B per interaction with the wider pool (83 without), RSS 329 MB at 1.25×10⁵; 200 × v1 DIF rate 1.58–1.61. Z(νν): 665.8 CPU-s for 5,000 events = 133.2 ms per event all-in, 33.56 kB per event, RSS 1,252 MB at 5,000; mean v1 weight 0.430; 160 Fatras step-limit particles in 5,000 events. The slice files' code_sha256 equal the hashes of the current scripts (p2x_hs0 464e23a3…, p2x_mbgen 4bca79a2…, p2x_common 076b36af…).
- Pilot campaign files for step 1 written, NOT launched: tools/runner/examples/p2x/pilot/{p2-c-pilot-mb, p2-c-pilot-znn-00…15}.json, PLAN_p2-c-pilot_mb-znn.json, LAUNCH_*_{2,3}slots.sh, STATUS_*.sh. `qv2run status --json` on schrodinger: 500 jobs pending, no marker or data directory created. `p2x_pilot_campaigns.py preflight`: 0 failed checks. 95.0 CPU-h, 79.4 GB, 47.5 h on 2 slots, 32.2 h on 3.
- Geant4 production slice: p2-c-px-g4-all-r0 = -r1 (7 group files, identical hashes), 32,861 vertices in 2×10⁵ firings, each in one class; 68 CPU-s, RSS 400 MB.
- outputs/PILOT_READY_xavier_2026-11-16_15-09.md written (step 1).
- Queue 5 is asked to stop after p2-c-px-g4 (STOP file) so that the generated LAUNCH script can be tested on a 7-job test set (tools/runner/examples/p2x/launch_test, prefix p2-c-px-lt, streams px.lt.*, validation data prefix) without exceeding 3 jobs on the node; b1, tr, val2 are requeued after it.
- 2026-11-16 15:27 p2-c-px-g4 complete (10 of 10) [V: markers]: all-big 2×10⁶ firings 675.6 CPU-s, RSS 1,060 MB; ni-big 10⁷ firings 538.1 CPU-s, RSS 263 MB; hs 3×10⁵ firings 91 CPU-s; lowpt 128 CPU-s, RSS 875 MB. Queue 5 ended at its STOP file.
- 15:25 p2x_queue.sh patched while no queue was running (retry of a campaign whose driver left without a failed job; untested branch). Pilot plan regenerated (hash of p2x_queue.sh 1ba0ddf7…), preflight 0 failed checks.
- 15:25–15:27 **Launch test** of the generated LAUNCH / STATUS scripts on tools/runner/examples/p2x/launch_test (p2-c-px-lt-mb, -znn-00, -znn-01; 7 jobs, 0.02 CPU-h; pgrep before: 1; SLOTS.md line): 7 of 7 done on 2 lanes, at most 3 jobs on the node; second LAUNCH: "already runs"; LAUNCH after completion: "already complete"; preflight on the finished set: 4 FAIL (clashes, as intended); appended part (chunk0 = 4): 0 failed.
- 15:26 Queue 6 started (2 slots): p2-c-px-b1 (24 jobs, v1 radius truncation = the "before" state), p2-c-px-tr (27 jobs: 9 samples × radius / time / both, same events and seeds), p2-c-px-val2 (validation of the tr files with the parent-crossing comparison of review A-1). Log schrodinger:/home/scratch/jdochoa/drivers/p2x_slices_6.log. SLOTS.md line appended.
- CPU of my campaigns so far [V: markers p2-c-px-*]: 1.24 CPU-h.

## State at the step-1 report (2026-11-16 15:27)
- **Step 1 (pilot.mb, Z(νν)): launch-ready, not launched.** outputs/PILOT_READY_xavier_2026-11-16_15-09.md. Launch only on the orchestrator's go and only after queue 6 has ended.
- **Step 2 (A-1):** code in p2x_b1.py (trunc radius | time | both | auto), test queued (p2-c-px-tr, p2-c-px-val2). To read the table when val2 is done: data/p2c/px_validation/p2-c-px-val2/000/p2-c-px-val2-0.json, per file `trunc_mode`, `a1_g4_without_fatras`, `a1_both`, `a1_frac_g4_without_fatras`, `parent_hits_later_than_vertex_time`, `ab_only_geant4` (the reviewer's number, first 100 events). p2-c-px-b1 is not in val2's file list: validate it with a new campaign (`p2x_pilot_campaigns.py slices --ver val=3 --val b1,tr --sub slices_step2b`).
- **Step 3 (B-4):** first versions exist (p2x_g4prod.py, p2x_b1.py, p2x_hspool.py, generator block 'b1'); NOT done: hard-scatter sample from INDEPENDENT parents (pool = the `had` lists of the Z(νν) pilot files; needs a loader, in a new file because p2x_common.py is frozen once the pilot runs), low-pT sample from `xpool_*` (the generator still passes the old prefix 'lowpt'; p2x_g4prod needs a pool selection by pT and η), yields file outputs/pilot_yields_xavier.json (`p2x_pilot_campaigns.py yields <val.json>` after a validation that includes the g4 files), B1 campaign files, costs of the b1 block from the b1 slice.
- Files that must not be edited once the pilot runs: list `frozen_from_launch` in tools/runner/examples/p2x/pilot/PLAN_p2-c-pilot_mb-znn.json.

## After the step-1 report
- 2026-11-16 15:41 Orchestrator: step 1 committed; GO for pilot.mb and Z(νν) on conditions (queue 6 complete, preflight, pgrep ≤ 1, SLOTS line, 2-slot script, first markers, resume test); A-1 table into outputs/A1_TRUNCATION_*.md; then step 3 in the terms of addendum v3 (read in full: phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v3_yvonne_2026-11-16_15-04.md).
- 15:37 Queue 6 "all complete" [V: p2x_slices_6.log]: p2-c-px-b1 24 of 24 done (25,000-event jobs: 98.7 / 105.3 / 111.5 CPU-s for dif / nix / nic = 3.9–4.5 ms per event all-in, max RSS 520–608 MB; dif-r0 = dif-r1 hash fe4194b1…), p2-c-px-tr 27 of 27 done, p2-c-px-val2 done.
- 15:38 **A-1 result [V: p2-c-px-val2]: the time cut does not repair DIF-C / NI-C.** Geant4 pre-vertex crossings without a Fatras parent hit (all events, with multiplicity): difc 58.5 % (radius) → 40.4 % (time); nic 66.5 % → 45.2 %; first-arc streams 0.00–0.11 % (radius), 0.25–3.29 % (time). Diagnostic p2-c-px-a1d (src/p2x_diag_a1.py): the Fatras parent has NO hit beyond 0.50 turn in any stream (0 hits against 19,669 Geant4 crossings beyond half a turn in difc), the vertex of these classes is at a median of 1.0 turn. Diagnostic p2-c-px-a1e (src/p2x_diag_turns.py) on the 5,000 Z(νν) slice events: 231 of 3.94×10⁶ hits of generated charged particles beyond 0.5 turn, sharp edge at 0.5: the chain as a whole leaves no hits after half a turn. No loop setting in run_chain.py (grep): ACTS default [U].
  Written: outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md (table, cause, recommendation: radius cut for first-arc streams; no cut passes for the after-turn streams; options).
- **DECISION: the pilot launch is HELD by me although the orchestrator gave the go.** Reason: brief §3 "stop and report at once" (a result contradicts a Phase-1 assumption in a way that may change the plan): the half-turn limit also shapes the Z(νν) hit record; the go was given without it. ALTERNATIVES: launch as told and report (the lanes can be stopped; cost ≈ 2 CPU-h per hour of delay in a decision). CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES. State: nothing launched; preflight was 0 failed checks at 15:26 (mine) and 15:28 (orchestrator); node has 1 job (Viktor); to launch: the commands of PILOT_READY §5.
- Note for the addendum fixer: v3 P1 says "Jets are stored down to 15 GeV"; p2x_hs0.py stores `jets10` with pT > 10 GeV, |η| < 5 (and `jets` > 20 GeV).
- CPU of my campaigns [V: markers p2-c-px-*]: see the report (≈ 1.5 CPU-h).
- 2026-11-16 15:42 Orchestrator: hold confirmed as right; launch pilot.mb now (Z(νν) stays held); quantify the half-turn limit tonight → outputs/HALF_TURN_xavier_<stamp>.md. mb-only plan generated (tools/runner/examples/p2x/pilot/PLAN_p2-c-pilot_mb.json, LAUNCH_p2-c-pilot_mb_1slots.sh; campaign file byte-identical to the committed one, sha a9c456f3…), preflight 0 failed checks (17 ok), pgrep 1. **The launch command itself was refused by the session's permission system (my original task says I do not submit the pilot; an agent's go is not the user's approval). I did not try another way. Nothing launched, no SLOTS line written.** The orchestrator or the user can run: bash tools/runner/examples/p2x/pilot/LAUNCH_p2-c-pilot_mb_1slots.sh (after the SLOTS.md line).
- 2026-11-16 15:58 Half-turn study started. (a) Mechanism, installed pyacts 48.0.0 wheel (no headers in the env): `FatrasSimulation.Config` exposes only the four EM switches, generateHitsOn{Sensitive,Material,Passive}, inputs/outputs, averageHitsPerParticle, pMin [V: acts/examples/ActsExamplesPythonBindings.pyi l.2599-2630]; `addFatras` passes nothing else [V: acts/examples/simulation.py l.481-535]; libActsExamplesFatras.so holds the actor list SimulationActor<…NoDecay, InteractionList<PhotonConversion>…> + Acts::PathLimitReached and the loop-protection messages "Path aborter limit set to … (full helix = …" [V: strings]. No Python knob → not configurable without a rebuild; no slice with the limit lifted (orchestrator: stop there).
  (d) v1: plan.md l.1267 lists in-time loopers ("repeated crossings, 2 hits per layer from one particle") as simulated "yes"; l.149 only the pMin pitfall; looper gun 0/10⁵ (C′₀) and 0/500 (C′_PU) [INV_STATS_BKG.md l.247-249]; no mention of a loop or path limit in stage2_C001_quirks, book, publication_plan or CHAIN_PROVENANCE.md (grep for loop protection / loopFraction / half turn / path limit: only the ACTS file listing acts/probe/src/tree.json).
  (b) Measurement: src/g4/g4hv.cc gets the option 'allx' (every primary recorded with all its crossings, pseudo-processes LeftWorld / TimeLimit; 18 changed lines, default behaviour unchanged; Tatiana's file, sha before fd10a890…); src/p2x_ht_chain.py (chain events with the full input particle table: 2,000 Z(νν), 20,000 single minimum-bias interactions), src/p2x_ht_g4.py (every charged input particle through Geant4, crossings against Fatras hits per particle and layer). Campaigns p2-c-px-ht, p2-c-px-htg (tools/runner/examples/p2x/slices_ht), queue log p2x_ht.log; pgrep before launch 1; SLOTS.md line.
- 2026-11-16 16:09 **Half-turn measurement done [V: p2-c-px-ht 3/3, p2-c-px-htg 3/3].** Geant4 reference for every charged Fatras input particle: Z(νν) 958 crossings of counting surfaces per event, 204 (21.3 %) after half a turn, 209 without a Fatras hit (25 % of the 833 written hits); minimum-bias interaction 312, 88.8 (28.5 %), 91.0 (37 % of 244); TBPS layers + 34–58 %. Central particles with pT < 0.63 GeV: 77 % still alive after one turn (decay 28 %, inelastic 14 %, stopped 3 %, left 33 %, circulating at 25 ns 21 %). Chain job costs: Z(νν) 2,000 events 251 CPU-s; 20,000 single minimum-bias events 701 CPU-s (35 ms per event, RSS 1,843 MB: sequencer overhead per event); Geant4 0.32–0.35 ms per particle.
  Written: outputs/HALF_TURN_xavier_2026-11-16_16-08.md (statement, mechanism, size, v1 search, options (a)–(d), what I would do for DIF-C / NI-C: (a)). Item (c) of the request (slice with the limit lifted) not done: not configurable from Python, no build attempted.
- State: nothing of the pilot launched (pilot.mb launch refused by the permission system at 15:42; Z(νν) held by the orchestrator). No job of mine running. CPU of all my campaigns [V: markers p2-c-px-*]: 1.89 CPU-h.
