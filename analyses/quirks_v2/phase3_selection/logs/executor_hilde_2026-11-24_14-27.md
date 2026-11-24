# executor hilde (Opus), p3-e: campaign `p3-e-devpu1` (STR §4.17 row 12, `dev.pu1`)

## 14:27 Plan
- Sources read: AGENT_RULES.md, CLAUDE.md STUDY OVERRIDES, PHASE3_BRIEF §2, ledger/README.md, CHAIN_PROVENANCE.md,
  STR l.2081-2132 (§4.17), runner `tools/runner/qv2run/{cli,campaign,ssh,wrapper}.py`, c1.pu1 campaign
  `tools/runner/campaigns/p2-a-c1-pu1.json`, Casper's template `phase3_selection/src/p3b/campaigns/prod/p4a-b2-prod-pu1.json`,
  job script `phase2_exploration/src/c1_pu_job.py`, p3-b readers `direct_job.py` (job_counts), `occ_replay.py` (open_job, replay).
- c1.pu1 measured (VERIFIED, 200 done markers `ledger/markers/p2-a-c1-pu1/000/*.marker`, all landau, attempt 1):
  CPU/job mean 1115 s, median 1117, max 1318 s; wall max 1329 s; max RSS max 702.6 MB, median 574.4; output mean 55.3 MB,
  max 62.9 MB; total 61.9 CPU-h (4,000 events, 20 per job). Unit cost 55.8 CPU-s per event (= 13.9 s per trial).
- Definition: `--stream dev.pu1`, 20 events/job (as c1.pu1; max c1.pu1 job 1318 s = 73 % of the 1800 s cap),
  5,960 events = 298 jobs (chunks 0..297, ev0 = 20·chunk), `--rho 1 --roads 4 --dump 20 --kind pu` (same output schema
  as c1.pu1: the dumps are read by occ_replay), per-job NUMBA_CACHE_DIR/pyc/Pythia-init under `$QV2_SCRATCH_DIR`
  (the job's scratch, set by the wrapper), data_prefix `p3e`, tier final, shard 0 (298 < 10,000 entries), timeout 1800.
  max_rss_mb set to the measured max RSS (wrapper memory limit = 1.5 ×).
- Generator `src/p3e/make_campaign.py` (writes `src/p3e/campaigns/p3-e-devpu1.json`); seed check `src/p3e/seed_check.py`
  -> `outputs/p3e/seed_disjoint.json` (first/last chunk seeds of c1.pu1, c1.pu2, prod.pu1, prod.pu2, reserve.pu1, dev.pu1,
  plus full-set disjointness over chunks 0..99,999 of every stream).
- Test: job devpu1-0000 only, on maxwell (1 slot, SLOTS.md line), through `qv2-job --mechanism ssh` (same command line the
  ssh driver dispatches, nice 10), output kept as part of the campaign (done marker -> the full launch skips it).
  Checks: marker done + sha256 of the file, CPU, max RSS vs c1.pu1, p3-b readers load it (direct_job.job_counts,
  occ_replay.replay of event 0 with PV check), on maxwell niced.
- Budget: STR row 12 100 CPU-h; projected 298 × ~1115 s ≈ 92 CPU-h (ESTIMATE) + per-job numba compile (measured in the test).
- Deliver: campaign JSON, launch command, CPU-h / wall at 4/6/9 jobs, memory request, pre-flight checklist in
  `outputs/P3E_hilde_2026-11-24.md`. No full launch.

## 14:28 Campaign written, seeds checked, test job dispatched
- `src/p3e/campaigns/p3-e-devpu1.json`: 298 jobs × 20 = 5,960 events; `qv2run status` parses it (298 pending).
- `outputs/p3e/seed_disjoint.json`: dev.pu1 disjoint from c1.pu1, c1.pu2, prod.pu1, prod.pu2, reserve.pu1 over the
  actual chunk ranges and over chunks 0..99,999 of every stream (0 common seeds in all 15 pairs).
- devpu1-0000 dispatched on maxwell 14:28:08 via `qv2-job --mechanism ssh` (nice 10, memory limit 1054 MB).
  Note: my ssh call backgrounded a `&&` list, so the ssh channel stays open until the job ends (harmless; the job is
  setsid/nohup). The ssh driver itself dispatches each command separately and does not have this.

## 14:47 Test job done; checks
- devpu1-0000 done (maxwell, attempt 1): CPU 1077.9 s, wall 1144.4 s, max RSS 685.7 MB, 52.5 MB, sha256 5e0958c0…
  (sha256sum on maxwell equals the marker; qv2run verify 0 corrupt).
- reader_check.json ok: same 329 keys (job_id <U11 vs <U10 only), seeds equal the formula, direct_job.job_counts identity
  checks pass, occ_replay PV/phimet equal for events 0 and 19; code_sha256 (16 files) and configs equal to c1pu1-0000.
- Driver dry run: 297 would-dispatch, devpu1-0000 skipped. Output kept as part of the campaign.
- Per-job Pythia MPI init ≈ +70 s (t_chain 331 vs c1.pu1 262 ± 17). Concurrency factors from jobs.tsv.
- Projection ≈ 98–100 CPU-h (budget 100). Slot RELEASED 14:48.
## 14:55 Hand-over written: outputs/P3E_hilde_2026-11-24.md, outputs/p3e/{seed_disjoint,reader_check,launch_plan}.json
