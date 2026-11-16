# Pilot readiness, channel (iii) — executor Xavier, 2026-11-16 15:09 (step 1 of 3: `pilot.mb` and `pilot.hs0.znn`)

**Nothing of the pilot is launched.** This file covers the two parts that the re-review of addendum 1 v2 leaves
untouched (`review/critical/ADDENDUM_1_v2_CRITICAL_REVIEW_wanda_2026-11-16_14-37.md`, C-1): the generator-level minimum
bias and the Z(νν) pilot. The single-interaction (B1) part is **not ready** (§7): its truncation (review A-1) and its
production code (B-4) are steps 2 and 3. Tags: [V] measured, campaign named (markers `ledger/markers/<campaign>/000/`,
data `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/px_validation/<campaign>/000/`, logs `…/logs/p2c/px_validation/…`);
[E] estimate. Session log: `logs/executor_xavier_2026-11-16_14-23.md`. Background only; no signal sample touched.

## 1. What is ready

| item | state |
|---|---|
| `src/p2x_mbgen.py` (stream `pilot.mb`) | written, slice-tested [V: p2-c-px-mbb] |
| `src/p2x_hs0.py` (stream `pilot.hs0.znn`) | written, slice-tested [V: p2-c-px-znnb] |
| `src/p2x_validate.py`, `src/p2x_common.py`, `src/p2x_queue.sh`, `src/p2x_pilot_campaigns.py` | written; used for the slices |
| campaign files `tools/runner/examples/p2x/pilot/p2-c-pilot-mb.json`, `p2-c-pilot-znn-00.json` … `-15.json` | written by the generator, 500 jobs, runner status = all pending [V: `qv2run status --json` on schrodinger, 15:08], pre-flight 0 failed checks [V] |
| `PLAN_p2-c-pilot_mb-znn.json`, `LAUNCH_…_2slots.sh`, `LAUNCH_…_3slots.sh`, `STATUS_….sh` (same directory) | written; **not run**. The same generator output was run end to end on a 7-job test set (campaigns `p2-c-px-lt-*`, streams `px.lt.*`, validation data prefix; 15:25–15:27): LAUNCH on 2 lanes → 7 of 7 done, 3 jobs on the node at most (Viktor's 1 + 2); a second LAUNCH while running answers "already runs"; STATUS reads the markers; LAUNCH after completion skips everything ("already complete"); `preflight` on the finished set reports the clashes (4 FAIL), on an appended part 0 [V] |

None of Tatiana's files was modified. `p2x_hs0.py` imports her `p2c_hs0.py` (same generator, filter, chain and event
seeds); `p2x_mbgen.py` repeats the loop of her `p2c_mbgen.generate` with a second pool.

## 2. Slice results [V]

| check | minimum bias (p2-c-px-mbb, 5 jobs) | Z(νν) (p2-c-px-znnb, 4 jobs) |
|---|---|---|
| hard checks (validation job p2-c-px-val1c: `all_hard_checks_pass: true`, 9 files) | pools inside their phase space, no NaN, species, wider pool disjoint from the main pool, v1 road rate within 15 % of the partition file | V4-1 closure, no NaN, offsets, distinct event seeds, truth MET ≥ 200 GeV (min 200.004), p̂T ≥ 150 GeV, every written hit has a row in the particle table (0 without), Σ neutrinos = stored MET vector |
| same stream and chunk run twice → identical content hash | -r0 = -r1 = 1a1ce790… | -r0 = -r1 = 8c911f8e… |
| other chunk → different | 4 jobs, 4 hashes | 3 jobs, 3 hashes |
| stored hash = hash recomputed from the file | yes (9 of 9) | |
| CPU | 3.56 ms per interaction (447.5 CPU-s for 1.25×10⁵; STR 2.0–2.5, Tatiana 3.6) | **133.2 ms per event all-in** (665.8 CPU-s for 5,000; event loop 130.7 ms: generation 46.1, Fatras + digitisation 38.3, seeding 7.8, CKF 14.8, dump 17.3; Tatiana's p2c_hs0: 127) |
| max RSS | 110 MB at 2×10⁴, 329 MB at 1.25×10⁵ → ≈ 590 MB at 2.5×10⁵ [E, linear] | 234 MB at 500, **1,252 MB at 5,000 events** |
| size | 215 B per interaction with the wider pool, 83 B without | **33.56 kB per event** (hits 20.0, truth positions 9.7, particle table 2.2, hadron list 1.25; p2c_hs0: 30.2) |
| physics cross-checks (no selection quantity) | 200 × v1 DIF rate 1.58–1.61 (v1 1.59; partition file 1.61); pool 7.03–7.10 per interaction (partition 7.13 on 2.5×10⁴) | v1 preselection weight mean 0.430, full-weight class 43.9 % (5,000 events; Tatiana 0.4308); 3.29 tries per kept event; 0.032 Fatras step-limit particles per event (160 in 5,000 [V: summary line of the job log]; known pathology, Tatiana's log 13:48) |

Failed attempts on the way (all in `experiment_log.md`): p2-c-px-mb (first p2x_mbgen changed a constant of the imported
module that also enters the v1 rates; rates doubled; found by the slice, rewritten, superseded by p2-c-px-mbb);
p2-c-px-znn (4 jobs failed at the first event, variable-name bug); p2-c-px-val1b (validator bug). CPU of all step-1
slices: 0.71 CPU-h [V: markers; p2-c-px-mb 0.185, -hsg 0.063, -znn 0.011, -mbb 0.205, -znnb 0.241, -val1c 0.002].

## 3. What a pilot file contains

One compressed npz per job plus `<job>.npz.sha.json` (content hash). `meta` (JSON) in every file: mode, stream, chunk,
job seed = blake2b("qv2|stream|chunk"), number of events, column names of every array, sha256 of every script and
chain file the job executed and of the geometry, surface and tune inputs, `content_sha256`.

**`pilot.hs0.znn`** (`p2x_hs0.py`), per event `i`:
- `hits[hit_off[i]:hit_off[i+1]]` (n, 13) float32: every measurement on the barrel counting surfaces and the BTL,
  columns sid, x, y, z, s0, s1, flag (bit 0 = on a selected CKF track), vp, particle, gen, vsec, dE, t. No pile-up, so
  every hit is an own hit; the CKF flag allows the classification on all own hits before CKF (Df-9) and an after-CKF
  comparison from the same record. `tru` truth position of each hit; `vz` the hard-scatter vertex; `v41`; `timing`.
- `evt` (19 columns, as p2c_hs0): truth MET vector (neutrinos), generator tries, σ_gen, hard-scatter vertex (x, y, z,
  t), number of particles given to Fatras, v1's preselection weight `w_v1` and its inputs (smeared MET, φ_MET,reco,
  trigger weight, MET > 250, jet > 100, min Δφ, number of veto objects), event seed.
- `jets` (anti-kT 0.4 on the visible final state, pT > 20, |η| < 4.7) and **`jets10`** (pT > 10, |η| < 5): pT, η, φ, m.
- `lep`: e and μ with pT > 5 GeV, photons with pT > 10 GeV, |η| < 5: pdg (flavour and charge), pT, η, φ, isolation
  (Σ visible pT in ΔR < 0.3), prompt flag. **`tau`**: every decayed τ with its visible decay momentum and a hadronic flag.
- **`nu`**: every final neutrino (pdg, pT, η, φ).
- **`gsum`** (17 columns): scalar Σp_T, vector Σp_x, Σp_y and scalar ΣE_T of the visible final state in |η| < 5 and
  |η| < 3; numbers of charged particles, visible particles, jets, τ; **p̂T**; **generator weight** (1 for every event:
  unweighted generation; checked on the slice).
- **`had`** (review C-8): every final hadron and photon of the hard scatter with |η| < 1.5 and pT > 0.3 GeV: pdg, pT,
  η, φ, production radius and z (79 per event). It is also the pool of independent hard-scatter parents for the
  single-interaction sample of review A-2 (each parent used once), with the event's own road axis and weight in
  `evt`.
- **`part`**: truth table of the generated particles that own at least one written hit (106 per event): barcode
  (vsec, particle), pdg, charge, pT, η, φ, production point and time, mother pdg, number of hits. With `gen` of the
  hit (≥ 1 = made by Fatras, e.g. a conversion leg of a photon row) it gives the truth attribution of own-hit
  candidates to prompt pairs, conversions and V⁰ (STR §4.7, B4-c split).

Check against the list "recompute the preselection weight under a reco-level MET model made of jets, leptons in
acceptance and a soft term": jets (pT > 10 GeV, with mass) yes; leptons with flavour, pT, η, isolation, promptness yes
(e, μ > 5 GeV; τ with visible momentum); neutrinos yes; ΣE_T and Σp_T for a soft-term or resolution model yes;
generator weight, σ_gen, tries, p̂T yes. **Not stored:** the full particle list (only hadrons and photons with
|η| < 1.5, pT > 0.3 GeV). A model that needs jets with another radius or another clustering input, or leptons below
5 GeV, needs the events regenerated at generator level from the stored seeds (event i of a job is reproducible from
sample, job seed and i; ≈ 46 ms per event, ≈ 29 CPU-h for 2.3×10⁶ [E]).

**`pilot.mb`** (`p2x_mbgen.py`): `hist`, `hist_prompt` (9 species × pT × |η| spectra of final-state particles),
`pool_*` (interaction index, pdg, pT, η, φ of the parents of addendum v2 P2: π±, K±, p, K⁰_L, n, γ within 1 mm,
0.5 < pT < 20 GeV, |η| < 1) and **`xpool_*`** (the same species outside that phase space, inside 0.3 < pT < 20 GeV,
|η| < 1.5: parents for the low-pT and 1 < |η| < 1.5 check samples of review B-2, 11.5 per interaction); `meta` holds
the v1 road rates and the numbers per interaction of every pool.

## 4. Campaigns (parameters of `p2x_pilot_campaigns.py`; defaults shown)

| campaign | stream | size | jobs × size | max RSS request / limit | CPU-h [E from V] | storage |
|---|---|---|---|---|---|---|
| `p2-c-pilot-mb` | `pilot.mb`, chunks 0–39 | 10⁷ interactions | 40 × 2.5×10⁵ (14.9 min) | 700 / 1,050 MB | 10.0 | 2.2 GB |
| `p2-c-pilot-znn-00` … `-15` | `pilot.hs0.znn`, chunks 0–459 | 2.3×10⁶ generated events (STR l.869) | 460 × 5,000 (11.1 min) in 16 campaigns of 29 (last 25) | 1,500 / 2,250 MB | 85.0 | 77.2 GB |
| **sum** | | | 500 jobs | | **95.0** | **79.4 GB** |

Wall time [E, wall = CPU as measured]: **47.5 h on 2 slots, 32.2 h on 3 slots** (lanes balanced by the generator:
2 slots 47.5 / 47.5 CPU-h; 3 slots 31.5 / 32.2 / 31.4). Against addendum v2: Z(νν) 81.1 → 85.0 CPU-h (+5 %: the added
summaries and tables), 70 → 77 GB. Outputs: `data/pilot/<campaign>/000/`; markers `ledger/markers/<campaign>/000/`.

**Appending more events later** (new shards, new seeds, nothing existing touched): job id = chunk number, so
```
python3 -I src/p2x_pilot_campaigns.py pilot --set 'only=["znn"]' --set znn.chunk0=460 --set znn.part0=16 \
        --set znn.events=1200000 --set plan_suffix=add1
```
writes `p2-c-pilot-znn-16…` with chunks 460… and its own PLAN / LAUNCH / STATUS files; `preflight` refuses a plan in
which any job id already has a marker. Same for `mb` (`mb.chunk0=40`, `mb.part0=1`). Other sizes: `--set
znn.events=…`, `--set znn.per_job=…` (≤ 5,000 at the measured RSS), `--set znn.parts=…`.

## 5. Commands (from einstein; `G=…/tools/runner/examples/p2x/pilot`, `S=analyses/quirks_v2/phase2_exploration/src`)

```
# 0. pre-flight (read-only): free space, markers directory, name and job-id clashes, hashes of scripts and inputs
python3 -I $S/p2x_pilot_campaigns.py preflight $G/PLAN_p2-c-pilot_mb-znn.json
# 1. node: must leave room (the queues wait by themselves while other jobs + 1 > 3)
ssh -x schrodinger "pgrep -u jdochoa -af '[q]v2run job' | wc -l"
#    and a line in phase2_exploration/SLOTS.md
# 2. launch: ONE of the two (one queue per slot, 1 job each, drivers detached on schrodinger)
bash $G/LAUNCH_p2-c-pilot_mb-znn_2slots.sh        # or  LAUNCH_p2-c-pilot_mb-znn_3slots.sh
# 3. status (markers only) and queue logs
bash $G/STATUS_p2-c-pilot_mb-znn.sh
# 4. resume after any stop or death: the same LAUNCH script again (complete campaigns and done jobs are skipped)
# 5. pause a lane after its running campaign: on schrodinger, touch /home/scratch/jdochoa/drivers/STOP.<first campaign of that lane>
# 6. after completion
ssh -x schrodinger "for f in $G/p2-c-pilot-*.json; do \$R/bin/qv2run verify \$f; \$R/bin/qv2run manifest \$f; done; \$R/bin/qv2run rebuild-ledger"   # R=…/tools/runner
```
A lane stops at the first campaign that does not end complete. A `failed`, `timeout` or `oom` job is never rerun by
the runner: replace it by generating the same chunk under a new job id, e.g. `--set 'only=["znn"]' --set name=r1
--set znn.chunk0=<chunk> --set znn.events=5000 --set znn.parts=1` (same stream and chunk, hence the same events).
Use one LAUNCH script consistently (their pid files differ); to change from 2 to 3 slots, pause the lanes first.

**Pre-flight checklist.** (1) `preflight` prints 0 failed checks (run now: cajuela 4,234 GB free against 79 GB; markers
directory writable; no campaign or job-id clash; 8 scripts and 9 inputs unchanged; streams `pilot.mb`,
`pilot.hs0.znn`). (2) pgrep count and SLOTS.md line. (3) The files listed under `frozen_from_launch` in the PLAN
(`p2x_hs0.py`, `p2x_mbgen.py`, `p2x_common.py`, `p2x_queue.sh`, `p2c_hs0.py`, `p2c_mbgen.py`, `p2c_common.py`,
`p2c_campaigns.py`, the chain files, `gen_d123.py`, geometry, tune, `acts/pixi.lock`) are not edited until the last
job is done: every job records their hashes, and a mixed set is a defect. I will put B1 changes into other files.
(4) The slices ran exactly the scripts hashed in the PLAN [V: `code_sha256` in the slice files' meta = PLAN hashes].

**Limits of what was tested.** (i) In `p2x_queue.sh` the branch "driver left without a failed job (no capacity because
of foreign load on the node): launch the same campaign again every 5 minutes, up to 4 hours" was added at 15:25 and
has not been exercised (no foreign load occurred); every other branch ran in the slices and the launch test.
(ii) A queue checks the node (other jobs + 1 ≤ 3) only before each campaign. Two pilot lanes plus Viktor's job keep
the node at 3. **Do not start the pilot lanes while my slice queue is running** (queue 6: p2-c-px-b1, -tr, -val2, 2
slots, to ≈ 15:55; `ssh -x schrodinger "tail -2 /home/scratch/jdochoa/drivers/p2x_slices_6.log"` must show "all
complete" or "queue stops"): its driver holds 2 slots and could dispatch on top of a lane (4 jobs). (iii) The 3-slot
script reaches 4 jobs on the node while Viktor's toy job runs: its third lane waits by itself, but then idles.
(iv) Full pilot job sizes were measured for Z(νν) (5,000 events); the minimum-bias job was measured at half size
(1.25×10⁵; 2.5×10⁵ is a linear extrapolation: 14.9 min, ≈ 590 MB against a limit of 1,050 MB).

## 6. Assumptions that a decision could still change, and what it would cost

| assumption | if changed |
|---|---|
| Z(νν) size 2.3×10⁶ generated events | append parts (§4); nothing regenerated |
| 5,000 events per job | parameter; ≤ 5,000 at 1,252 MB |
| summary content (§3) | a quantity not stored needs the generator-level regeneration from seeds (≈ 29 CPU-h), not the chain |
| v1 preselection weight stored as a labelled v1 quantity; the v2 MET model is applied in Phase 3 | nothing regenerated if the model uses what §3 lists |
| generator cut p̂T > 150 GeV and filter MET > 200 GeV of v1 (1.7 % of kept events within 10 GeV of the cut, Tatiana) | a lower cut is a new sample |
| `pilot.mb` 10⁷ interactions; wider pool stored by all 40 jobs (2.2 GB instead of 0.8) | `--set mb.xpool_jobs=…`; more interactions by appending |
| node share: 2 lanes + Viktor's job fill schrodinger (cap 3) | my remaining B1 slices (steps 2–3, < 1 CPU-h) then need a lane paused or a fourth slot when the graphical session ends |

## 7. Not ready (steps 2 and 3, in progress)

B1 code exists as a first version (`p2x_g4prod.py`: production mode reading pool files, one class per vertex asserted,
vertex files per sample; `p2x_b1.py`: class list, DIF = dif or k0l, parent kinematics, road offset, class, radius,
layer, Geant4 crossings, truncation by radius / time / both / auto, β cut as an argument with the validated 0.1 as
the campaign default, number of road orientations recorded; `p2x_hspool.py`). First Geant4 slice jobs
[V: p2-c-px-g4-all-r0/-r1]: identical hashes for the same seed, 7 vertex files, 32,861 vertices in 2×10⁵ firings, one
class each. The truncation test of review A-1 (campaign p2-c-px-tr, 27 jobs) and the rest are queued behind it.
First numbers for step 3 [V: p2-c-px-g4, 10 jobs done]: 'all' pass 2×10⁶ firings 675.6 CPU-s (0.338 ms per firing all-in), max RSS 1,060 MB,
226 MB of vertex files; 'ni' pass 10⁷ firings 538 CPU-s, RSS 263 MB; class counts in 2×10⁶ firings: dif 70,444,
difc 68,004, k0l 3,883, ni22 / ni30 / ni61 3,375 / 4,658 / 4,572, nix 66,868, nic 34,943, conversion 70,503, other 47
(sum = number of vertices, asserted). No B1 campaign file is written. CPU of all my slices so far: 1.24 CPU-h
[V: markers p2-c-px-*] of the ≈ 4 allowed.
