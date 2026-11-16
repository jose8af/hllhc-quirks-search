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
