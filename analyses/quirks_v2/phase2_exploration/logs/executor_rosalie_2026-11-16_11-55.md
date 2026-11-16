# Executor Rosalie — Phase 2, channel (i): C1 (port and reproduction of v1), C2 (finder cross-checks), day-0 measurements

Session log and plan (crash-resilient notebook). Started 2026-11-16 11:55:04 -05 (`date`). Day 0 = 2026-11-16.
Budget (STR §11.2 [V: STRATEGY_oscar l.2509-2510]): C1 198 CPU-h, C2 81 CPU-h. Day-0 timing and ρ = 2 memory jobs are
booked on the MUST row "enlarged development samples; timing jobs" (Phase 2: 5 CPU-h, STR l.2520) and reported separately.
Stop and report if the projected spend of C1 or C2 exceeds its budget by > 30 % (C1 257, C2 105 CPU-h).

## 0. Read (all with the Read tool)
PHASE2_BRIEF.md; AGENT_RULES.md; CLAUDE.md (overrides); agents/executor.md; phase2_exploration/CLAUDE.md;
methodology/03-phases.md "Phase 2"; methodology/11-coding.md; STR §0, §4.0, §4.1, §4.2, §4.5, §4.17, §11.1-11.7, §12.1;
COMMITMENTS rows C1-a…e, C2-a…c, B2-e, BL-1 and "Gate A answers"; FEAS_A (full), FEAS_C (full), FEAS_B (summary, task 1-3);
CHAIN_PROVENANCE.md; PREFLIGHT.md; ledger/README.md; runner campaign.py/paths.py; v1 `acts/stage4/{C1_LAUNCH.md,
run_stage4.py, finder/production.py}`, `frozen_inputs.json` (frozen = true, delta95 = 0.15, t_seed = 4).

## 1. Blinding rules I apply (COM C1-d, BL-1, Gate-A Q1)
- Open tier: signal pass counts at R04 (three points) and R06 (E 200, 1.5 keV). Sealed: R07 (three points), fallback
  FB2/FB3 (three points), the fallback twin ratio. I never open, count, print or summarise selected signal rows at R07 or
  any FB column, and never at any other rung beyond those four. Signal outputs are written by the jobs without being read.
- The comparison script reads, for signal, only the four open columns, and is tested on them only. The sealed branch of
  the script (exact test → PASS/FAIL, encrypted counts file) is tested on **synthetic** inputs (fake counts I generate),
  never on the real files. The orchestrator's separate session runs it on the sealed quantities.
- C2 V4-5: takes the first F0-accepted signal events in file order, prints no row count and no pass fraction.
- Background (PU, SM, C′) outputs are not signal and are read freely.

## 2. Code (all in `phase2_exploration/src/`, logging not print; chain-code edits logged in CHAIN_PROVENANCE.md)
1. **Chain edit (minimal, additive, bit-identical when unused):**
   - `acts/stage4/finder/production.py::process_trial(..., premerge_min_nip2=None)`: when set, also returns `res['pre']`,
     the pre-merge candidate records (every loose candidate with N_IP2 ≥ 6, aligned flag kept as a column) with a CSR hit
     list into a per-trial road-hit union table (xyz, sid, s01, dE, INT, t, gen, particle). No RNG draw is added, so all
     other outputs are unchanged (checked by a bit-identity test on one ρ = 2 event with and without the option).
   - `acts/stage4/run_stage4.py::run_pu_job(job, allow_interim, premerge=None)`: passes the threshold and hands each
     trial's `pre` to a streaming writer at once (not kept in memory: STR §4.5 fallback 3 for the store).
2. `c1_pu_job.py` — one PU job (ρ = 1 or 2; also `sm` later) through `run_stage4.run_pu_job` with the frozen v1
   configuration, job seed = blake2b("qv2|<stream>|<chunk>") via v1 `hash_seed` (STR §4.17), output in `$QV2_OUT_DIR`:
   `<id>.npz` (v1 schema) and, if requested, `<id>.premerge.npz` (zip of per-trial npy entries, written incrementally).
   Refuses to run if `WP_RULE.md` sha256 ≠ `frozen_inputs.json` → `wp_rule_sha256`. Node-local caches (numba, pyc,
   Pythia init); `PYTHONDONTWRITEBYTECODE=1` (no `__pycache__` in the trees).
3. `make_campaigns.py` — writes the runner campaign JSONs to `tools/runner/campaigns/p2-a-*.json` (data prefix `phase2`).
4. `day0_summary.py` — reads markers + outputs of the day-0 jobs: RSS vs events per job, CPU per event, chain and
   finder per-stage times (`chain.timing`, `trials.times`), pre-merge bytes per trial → `outputs/day0_measurements.json`.
5. Later (C1/C2): `c1_compare.py` (41 comparisons, statistics of STR §4.1; sealed branch → PASS/FAIL + encrypted file,
   tested on synthetic data only); `c1b_arith.py` (v2 arithmetic on v1 counts); `v45_bruteforce.py` (numba scan + scipy
   fit, independent of `finder.py`); `tseed_stability.py` (T_seed 4 vs 2 on stored dumps); `v44_repro.py`.

## 3. Campaigns (names `p2-a-*`; data under `data/phase2/<campaign>/`; markers `ledger/markers/<campaign>/`)
Unit costs used for planning (STR Table 4.0, to be replaced by the day-0 numbers): ρ = 1 event with 4 trials 60.4 s,
ρ = 2 event 206 s, PU-200 row with one trial 25.2 s.

| campaign | content | events | jobs (planned) | CPU-h (plan) | item | when |
|---|---|---|---|---|---|---|
| p2-a-day0-pu1 | ρ = 1 timing at the frozen road 0.15 / T_seed 4, 4 roads, stream `p2a.day0.pu1` | 2 × 5 | 2 (one alone on landau, then 4 concurrent? no: one alone + the C1 jobs give the 3-concurrent number) | 0.2 | timing | day 0 |
| p2-a-day0-pu2 | ρ = 2 memory: 1, 2, 4, 8 events per job, each **alone on maxwell** (announced in SLOTS.md), pre-merge store on, stream `p2a.day0.pu2` | 15 | 4 | ≈ 0.9 | B2-e / timing | day 0 |
| p2-a-c1-pu1 | ρ = 1, 4 roads, 4,000 events, stream `c1.pu1`, hit dumps for all events (C2 T_seed needs 500; B2 occupancy development 2,800; +0 CPU-h, ≈ 9.6 GB) | 4,000 | ≈ 200 (size from day-0) | 67 | C1 | day 0 → |
| p2-a-c1-pu2 | ρ = 2, 2 roads, 1,000 events, stream `c1.pu2`, pre-merge store on, dumps for the first 200 events | 1,000 | from day-0 RSS/time | 57 | C1 (+B2 dev) | after day-0 ρ = 2 |
| p2-a-c1-sm | Z(νν)+j hit level + PU, 1 road, 2,000 events, stream `c1.sm` | 2,000 | 100 | 14 | C1 | day 1 |
| p2-a-c1-cp0 | C′₀ no-PU topologies at v1 sizes, stream `c1.c0` | 5.4×10⁵ | ≈ 10 | 1.7 | C1 | day 1 |
| p2-a-c1-cppu | C′_PU: DIF, γ, V⁰ 1,000 each, PV pair 2,000 (+v1 others as listed), stream `c1.cpu` | 5,000 | ≈ 250 | 35 | C1 | day 1-2 (after cp0) |
| p2-a-c1-gen | generator-level rates (DIF, PV pair, γ per triggered event; N_trig) | — | few | 5 | C1 | day 1 |
| p2-a-c1-sig | three points × 400 rows (v1 path) + 800 twins; Stage 3 at the three points (3.6) | 2,000 rows | ≈ 30 | 14 + 3.6 | C1 | needs Stage 2 at E 200 / E 500 (dependency, see §6) |
| p2-a-c2-v45 | V4-5 brute force, 50 signal + 50 PU trials; one event timed first | 100 | ≈ 100 | 30 (to be timed) | C2 | day 2-4 |
| p2-a-c2-tseed | T_seed 2 re-run of 500 ρ = 1 + 200 ρ = 2 events from dumps | 700 | ≈ 60 | 44 | C2 | after pu1/pu2 |
| p2-a-c2-v44 | 20 production-type jobs × (same node twice, second node) + 2 different-seed jobs | — | 62 | 7 | C2 | day 3 |
| **total** | | | | **C1 ≈ 198, C2 ≈ 81, day-0 ≈ 1.1** | | |

Slots (brief §3): weekdays 08:00–19:00 at most 3 concurrent jobs of this channel; otherwise 4; ≤ 4 per node (3 on
landau and schrodinger, graphical session `who` 11:54). ρ = 2 jobs: node announced in `SLOTS.md`.
Mechanism: SSH runner for the day-0 jobs (`--max-per-node 1`, one node each); Argo or SSH for C1 with an explicit cap
(`--max-parallel 3` weekdays; relaunch with 4 after 19:00).

## 4. Checks
- Day-0: V4-1 pass flag in every chain meta; `frozen_inputs` echoed in output meta (road 0.15, tseed 4); RSS from the
  runner's `ru_maxrss` (= `/usr/bin/time -v` semantics, FEAS_C R1).
- Bit-identity: one event with and without `premerge_min_nip2` gives identical v1-schema arrays.
- C1 campaigns: `qv2run status` / `verify`; parallel outputs not identical (different seeds); V4-1 check per job.
- Resumability: kill one running job / the driver once on the first campaign and relaunch (FEAS_C procedure).

## 5. Order and deliverables by day 5 (2026-11-21)
1. Day 0: plan (this file) → code (§2.1-2.4) → day-0 jobs → day-0 summary (RSS, ρ = 2 job packing, bytes per trial,
   unit costs vs Table 4.0) → c1-pu1 submitted and verified resumable → report.
2. Day 0-1: c1-pu2 sized from day-0; sm, cp0, gen; c1_compare.py on the open background families as outputs arrive.
3. Day 1-3: cppu; V4-5 code + one-event timing; V4-4; T_seed when dumps exist; container recipe + one job rerun (C1-c).
4. Day 3-5: signal (if Stage 2/3 inputs exist), open-tier comparison; c1b arithmetic; `EXPLORATION_i_rosalie_<stamp>.md`
   with campaign table, unit costs, C1/C2 verdicts (PASS / FAIL / NOT TESTED), inventory, self-review.

## 6. Known dependencies and risks (from reading)
- **Signal inputs:** C1 signal needs Stage 2 (MG + Pythia) at E 200 and E 500 and Stage 3 at (E200, 1.5 keV),
  (E200, 2 keV), (E500, 3 keV); v1 Stage-3 data are lost. Who produces Stage 2 at these points (channel ii's S2 sample
  or me) must be settled with the orchestrator → asked in the first report.
- The probe-row exclusion file `fix_r1/f1r_summary.json` is lost (STR §4.1): decide from `AN1/signal_rows_a2.npz`.
- ρ = 2 memory: nodes show ≈ 2.0–2.5 GB used by the system at rest (`free -m` 11:54), so ≈ 5.3–5.8 GB is available,
  not 7.5 GiB.
- The chain step calls `pixi run --manifest-path acts/pixi.toml` per job (NFS manifest check; FEAS_A open issue 9).

## 7. Log
- 11:55 plan written.
- 11:56 chain edit (pre-merge store hook) in production.py / run_stage4.py; logged in CHAIN_PROVENANCE.md.
- 11:56 code: src/c1_pu_job.py, src/make_campaigns.py; campaigns tools/runner/campaigns/p2-a-day0-pu{1,2}.json.
- 11:57 SLOTS.md: maxwell to myself ≈ 1.5 h. Launched (SSH runner, one job per node):
  p2-a-day0-pu2 on maxwell (n = 1, 2, 4 + n1 without store), p2-a-day0-pu1 on landau (5 events rho = 1).
- 11:58 p2-a-day0-pu2 jobs d0pu2-n1/n2/n4 FAILED at start (scratch work dir created after the writer opened its file:
  my bug in c1_pu_job.py, fixed). Failed jobs are never retried by the runner → new campaign p2-a-day0-pu2b (same
  seeds/chunks, ids d0pu2b-*). d0pu2-n1-nopm (no store) ran: done, 179.6 CPU-s, max RSS 1076.8 MB, maxwell (VERIFIED,
  marker ledger/markers/p2-a-day0-pu2/000/d0pu2-n1-nopm.marker).
- 12:02 p2-a-day0-pu2b launched on maxwell (one at a time).
- 12:04 p2-a-day0-pu1 done (landau, alone, first job on the node, cold Pythia-init and numba caches): 5 events,
  314.6 CPU-s (62.9 s/event incl. fixed start), max RSS 626.8 MB, chain 12.3 s/crossing in stages (ckf 7.1, fatras+digi
  2.5), finder per trial 11.27 ± 7.33 s (find 10.6 s) at road 0.15 / T_seed 4 [VERIFIED, outputs/day0_measurements.json].
  The ×0.77 road-0.15 saving assumed in Table 4.0 is not seen at this N (one job).
- 12:05 seen: channel (ii) MG job on maxwell (my announced node) and three channel (iii) jobs on schrodinger.
- 12:05 c1-pu1 sized 20 events/job (≈ 21 min at ≈ 63 s/event), 200 jobs, RSS request 1000 MB; launched SSH runner
  on landau, 2 per node (my 3rd weekday slot is the maxwell rho = 2 job).
- 12:08 resumability test on p2-a-c1-pu1: driver killed with kill -9 on landau while c1pu1-0000/0001 ran; jobs kept
  running (detached); relaunch 12:09 adopted both running jobs from markers (driver log: "our ssh jobs 4 … cap 3").
  PASS. Relaunched with landau --max-per-node 1 because channel (iii) started 2 jobs on landau (p2-c-t-g4) at ≈ 12:08:
  landau then carried 4 jobs against its cap of 3 (graphical session); mine drop to 1 as they finish.
  Check: ssh -x landau "$R/bin/qv2run status $R/campaigns/p2-a-c1-pu1.json --live -v"   (R=$REPO/tools/runner)
- 12:25 p2-a-day0-pu2b done (maxwell, one job at a time; a channel (ii) MG job shared the node part of the time).
  [VERIFIED, outputs/day0_measurements.json, markers ledger/markers/p2-a-day0-pu2{,b}/]
  | job | events | CPU s | CPU s/event | max RSS MB | pre-merge cand/trial | pre-merge MB/trial |
  | d0pu2-n1-nopm | 1 | 179.6 | 179.6 | 1076.8 | (store off) | — |
  | d0pu2b-n1 | 1 | 194.1 | 194.1 | 1597.8 | 115,311 | 32.6 |
  | d0pu2b-n2 | 2 | 329.2 | 164.6 | 1585.2 | 102,621 | 28.2 |
  | d0pu2b-n4 | 4 | 715.6 | 178.9 | 1738.4 | 110,094 | 30.7 |
  Finder per ρ = 2 trial 64–76 s (find 52–63 s, IS weights 4.6–5.8 s); chain 12.6–14.4 s per crossing incl. start.
  Bit identity with/without the pre-merge store (same seed): 105 of 106 keys identical, only `job_id` differs → PASS.
  The store adds ≈ 0.5 GB RSS (1.08 → 1.60 GB at 1 event); RSS grows slowly with events (1.59 → 1.74 GB, 2 → 4).
  Storage: ≈ 31 MB per trial (110 hits per stored candidate on average), above the STR §4.5 guess of 3.6–14 MB.
  Projection: c1-pu2 2,000 trials → 62 GB; with 3,000 production events (6,000 trials) 248 GB in all: below the
  400 GB cap, above the 200 GB planning value. No [DT4] (threshold stays N_IP2 ≥ 6).
- 12:26 p2-a-day0-pu2c (8 events, chunk 3) launched on maxwell alone.
- 12:55 p2-a-day0-pu2c (8 events, maxwell alone) done: 1688.9 CPU-s (211 s/event), max RSS 2120.8 MB, wall 1694 s
  (28 min: 8 events per job is too close to the 30-min limit), pre-merge 127,797 cand/trial, 37.0 MB/trial.
  ρ = 2 summary [VERIFIED, 15 events]: CPU 195 s/event mean (2928 s / 15; Table 4.0: 206 s); max RSS 1.60 / 1.59 / 1.74
  / 2.12 GB at 1 / 2 / 4 / 8 events → STR §4.5 rule 2 (≤ 2.5 GiB): **2 ρ = 2 jobs per node**; pre-merge store
  33.8 MB/trial on average (1,015 MB / 30 trials) → c1-pu2 ≈ 68 GB; with the 4a ρ = 2 sample ≈ 270 GB < 400 GB cap.
  ρ = 1 at 3–4 jobs per node (c1pu1-0000/0001, landau): 1140.9 / 1172.0 CPU-s for 20 events = 57–59 s/event (Table
  4.0: 60.4 s), RSS 575–579 MB, 55 MB per job.
- 12:56 p2-a-c1-pu2 written (5 events/job, 200 jobs, RSS request 2100 MB, dumps for events 0–199) and launched on
  maxwell, 2 per node (SLOTS.md updated). Channel slots now: landau 1 (c1-pu1), maxwell 2 (c1-pu2) = 3 (weekday cap).
  Plan for 19:00: relaunch c1-pu1 with one more slot (channel cap 4 off-hours).
- 12:58 Orchestrator answers (after the interim report): (1) I produce the C1 signal inputs (Stage 2 at E 200, E 500
  with v1 cards, FSR off, then Stage 3 at the three points; reuse channel (ii)'s src/s2/s2_job.py by copying);
  (2) fixed node shares (SLOTS.md ORCHESTRATOR RULING 12:58): mine = landau 2, maxwell 2; C2 and signal inside them;
  (3) 34 MB/trial store accepted (deviation from STR's 3.6–14 MB to be stated in EXPLORATION); (4) the ρ = 2 timing
  node was shared ≈ 11 min with a channel (ii) MG job: timing caveat, memory stands; (5) next report gives projected
  C1 + C2 CPU-h with measured costs and corrected Table 4.0 unit costs.
- 12:58 p2-a-c1-pu1 driver restarted with landau --max-per-node 2 (old driver pid 1689413 stopped; c1pu1-0004
  dispatched, 2 running). p2-a-c1-pu2 runs 2 on maxwell.
- 13:00 C1 signal plan (orchestrator answer 1). Pipeline, each step a runner campaign, code in src/:
  1. p2-a-c1-s2: c1_s2_job.py c1gen = COPY of channel (ii)'s src/s2/s2_job.py (sha256 d3eb2b8a…1deef5 at copy time)
     + a `c1gen` command: v1 F_TRG (pT_ME ≥ 100, produce.py PTCUT) and F_INC MLM 0–2j, v1 cards, CP5 + quirk card,
     qCut 45, QED-FSR OFF; seeds stream c1.s2. First pass: 1 chunk × 20,000 LHE per (TRG|INC, m 200|500) = 4 jobs.
  2. c1_s3_inputs.py (one job per mass): merge → stitch TRGS (v1 stitch_trg rule) → v1 make_inputs 'p2' extract →
     F_m<m>_p2.npz. Needs ≥ 200 |eta| < 2.5 unweighted events per split (v1 p2_lists); top-up chunks if short.
  3. c1_s3_job.py: v1 run_stage3.run_job, chunks of the p2 lists (template + toy up to the 200th each = 400 rows).
  4. c1_s3_index.py → outputs/c1_s3/STAGE3_INDEX.json (absolute cajuela paths, from done markers).
  5. c1_sig_job.py: v1 run_g1b.run_signal_job: a2 (fast path) E 200 at Λ = 1.5, 2 keV row-major; a5 (full chain) E 500
     3 keV; twins = a5 at E 200 1.5 and 2 keV. Rows: all counting rows of both splits.
  DECISION: probe-row exclusion off (QV2_ALLOW_NO_F1R=1): v1's f1r_summary.json is lost and its rows refer to v1's
  Stage-2 rows, which do not exist in the regenerated sample; C1 compares against v1's counts over v1's denominators
  as recorded (STR §4.1). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.
  SEALED OUTPUTS (orchestrator answer 1): the signal job outputs p2-a-c1-sig*/000/*.npz (on cajuela, with done markers)
  hold sig.eff / sig.eff_fckf / sig.eff_T / sig.eff_fckf_T packed bits for all 43 rungs and the per-trial rung tables.
  Nobody in channel (i) opens them except c1_compare.py, which reads only the R04 and R06 columns. A later session reads
  R07 and the FB columns from the same files (keys and rung order in meta_json → rungs).
- 13:05 slot management (ORCHESTRATOR RULING 12:58): landau slot A = p2-a-c1-pu1 driver (max 1 per node); landau slot B =
  queue_slot.sh with queue file phase2_exploration/logs/queue_landau_B.txt (p2-a-c1-s2 → p2-a-c1-cp0 → p2-a-c1-sm;
  re-read after each campaign, so later campaigns are appended there); maxwell 2 slots = p2-a-c1-pu2.
  Transient 13:00–≈13:08: 3 of my jobs on landau (pu1 0003/0004 + s2) until c1pu1-0003 ends.
  New code: src/c1_s2_job.py, c1_s3_inputs.py, c1_s3_job.py, c1_s3_index.py, c1_sig_job.py, c1_cp_job.py, queue_slot.sh;
  campaigns p2-a-c1-cp0 (16 jobs × 25,000 events: DIF 5e4, NI22 3e4, PV pair / γ / V⁰ 1e5) and p2-a-c1-sm (50 × 40).
- 13:11 C2 defined (code + campaigns; production sizes of T_seed and V4-5 follow from the two timing jobs):
  * C2-b V4-4: p2-a-c2-v44a (20 rho = 1 jobs × 5 events, stream c2.v44, landau), p2-a-c2-v44b (the same 20 again on
    landau: bit-identical expected), p2-a-c2-v44c (the same 20 on maxwell + 2 jobs of stream c2.v44x: different seeds).
  * C2-c T_seed 4 → 2: DECISION: regenerate the events from the job seed with the finder T_seed overridden (v1's own
    g3_rerun.py pattern; c1_pu_job.py --tseed 2) instead of re-reading the S6 dumps (STR §4.2 wording): the pairing with
    the stored T_seed = 4 jobs is then exact (same events, PV, roads, trial seeds) and needs no new reconstruction code;
    the chain costs ≈ 13 s per crossing more. Timing first: p2-a-c2-tstime (rerun of d0pu1-n5-a and d0pu2b-n1 at T_seed 2).
    CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.
  * C2-a V4-5: src/v45_bruteforce.py (numba scan 3001 × 3001 normals at 0.2 mrad within ±0.3 rad of n_F0 with a
    resolution-weighted inlier score; 5 mrad half-sphere global scan; scipy least_squares fit on the F0 inliers; hit pool
    rebuilt from the S6 dumps with the job's seed streams, checked by n_road and PV against the stored trial). PU mode
    written; signal mode added when the full-chain C1 outputs exist. Timing: p2-a-c2-v45time (one PU trial).
  * C1 rates: p2-a-c1-gen = v1 gen_d123.py nt unchanged, one job per SM process (v1 NPROC sizes) + minimum bias 1e5,
    seed tag qv2-c1-gen.
  * c1_compare.py (PU families; smoke-tested on the first 80 rho = 1 events: R04 174.9 vs v1 171.55, p = 0.80).
  Queue landau B now: s2 → c2-tstime → c2-v45time → c1-gen → c1-cp0 → c1-sm → c2-v44a → c2-v44b.
