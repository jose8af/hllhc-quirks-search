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
