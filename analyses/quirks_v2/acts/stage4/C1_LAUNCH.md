# C1 launch (C1a → C1b → C2B), 2026-10-14

Executor (C1 launch). Authority: orchestrator instruction after G3 (`g3/G3_REPORT.md` §4, §6, §8), plan §11 row
"7-12 s", WP_RULE §6.4 (not modified), user decision C2-B after C1 (LOG 2026-10-14 ~00:40).

## 1. What changed

1. **G1b patches applied** (`validation/g1b_post_g3.sh`, 00:16): run_stage4.py 85b978f5… → 1258e82a…, run_chain.py
   b1130b40… → bdea0e27… (shas confirmed). The PU/SM/dens regression on the applied files is bit-identical
   (97/86/82 keys). C1.json was regenerated.
2. **T_seed := 4** (WP_RULE §6.4 pre-declared action, both ρ), 00:18:48. `frozen_inputs.json` (both copies) changed
   from 7574e0b5… to 2adc8f9d…:
   - `t_seed` 6 → 4;
   - `finder_config.tseed = 4`, which `config_from_frozen` applies to every job kind.

   WP_RULE.md is unchanged (1b2ea9bd…). Details are in `HASH_ADDENDUM.md` §5.
3. **run_stage4.py → 0d122cfc…**:
   - **Re-timing.** T1_S 3.26 → 8.02 s, T2_S 20.1 → 50.6 s, PU_S 4.83 → 10.2 s, and PU_S_RHO2 = 9.3 s is new. These
     are G3 values under load, so `est_s` ≈ job wall and the `status` throughput ≈ the number of busy workers (no
     longer 3.6–3.8).
   - **Sub-run campaigns.** `C1a` (a1/a2/a5/cp0/cppu, 875 jobs), `C1b` (pu/sm/dens, 760 jobs, plus the `val`
     placeholder) and `C2B` (C2 pu only, 480 jobs). They use the same job dicts, seeds and output paths as C1/C2, under
     `prod/C1/` and `prod/C2/`.
   - **C1_val** reads all C1 outputs and is a non-runnable placeholder (kind g1, as before). It is listed last, in C1b.

## 2. Verification: PASS

G3B1_00000 was run through `run_stage4.run_pu_job` with no override (`validation/tseed4_verify.py`, output
`data/acts_stage4/tseed4_verify/`).
- **Against the stored T_seed = 4 rerun:** 85/85 arrays are bit-identical.
- **Against the T_seed = 6 production file:** 57/85 arrays differ (negative control).
- **Meta:** `finder_cfg.tseed` = 4.
- **C1a outputs:** the first ones also record tseed 4 and run_stage4 0d122cfc….

## 3. Running processes (started 2026-10-14 00:28:59)

| what | PID | log |
|---|---|---|
| C1a runner (`nice 10 caffeinate pixi … run --campaign C1a --workers 7 --mem-gb 19`) | 82794 | `data/acts_stage4/prod/C1/run_stdout_C1a.txt` |
| chain `validation/chain_c1.sh 82794` (C1a → C1b → C2B, polls with `kill -0` every 120 s) | 82813 | `data/acts_stage4/prod/C1/chain_log.txt`, `chain_stdout.txt` |

C1b logs to `prod/C1/run_stdout_C1b.txt` and C2B logs to `prod/C2/run_stdout_C2B.txt`. Their PIDs are written to
`chain_log.txt`.

**Stopping.**
- A `STOP` file in `prod/C1/` stops C1a/C1b gracefully and also prevents the next launch.
- `prod/C2/STOP` stops C2B.

**Note on priority.** The launching shell was at nice 5, so the runner shows NI 15 and its workers run at about 19.
Under G3 this probably made no difference to throughput.

## 4. Cost and ETA (ESTIMATE)

The walls come from simulating the runner's scheduler: 7 workers, a 19 GB memory budget, 4 GB per B2 job, and `est_s`
as the job wall. The range is ×1.00 to ×1.15.

| sub-run | jobs | est (per-worker h, loaded) | ≈ 1-process CPU-h | wall | end |
|---|---|---|---|---|---|
| C1a | 875 | 52.9 | ≈ 29 | 7.6–8.7 h | Wed 14 ≈ 08:00–09:15 |
| C1b | 760 | 162.4 | ≈ 88 | 23.4–26.9 h | Thu 15 ≈ 07:30–12:10 |
| C2B | 480 | 148.8 | ≈ 80 | 28.4–32.6 h | Fri 16 ≈ 12:00–21:00 |

**Flag for the orchestrator.** The plan's production stop is Fri 16 12:00. C2B's ESTIMATE end is at or after that.
- One option is to put B2 ahead of B1 in C2B (sort by est only). B2 jobs would then run 4 at a time, with 2 B1 jobs
  alongside them. This is a one-line change before C2B starts. The simulated wall is 23.7–27.2 h.
- The other option is a STOP at the production stop. Completed jobs are kept.

Both C1b and C2B also exceed the 1-day cap (the user accepted about 27–30 h per campaign on 2026-10-13).

**Decided 2026-10-14 00:35.** Option (a) is applied: C2B is ordered longest-first, run_stage4 e371c2b2…, and only
the order changes. The C2B ESTIMATE is now 23.7–27.2 h, ending about Fri 16 06:00–15:00.
Option (b) is also in place: `validation/prodstop_fri.sh` (PID 83550) creates `prod/C2/STOP` at Fri 12:00 -05. It
also creates `prod/C1/STOP` if C2B has not started by then.
HASH_ADDENDUM is accepted as part of A.3 for admission.

## 5. Commands (from the theory_track root)

```
pixi run python -m acts.stage4.run_stage4 status --campaign C1a     # likewise C1b, C2B, C1
pixi run python -m acts.stage4.run_stage4 check  --campaign C1a     # V4-1 (+ V4-10 for C')
cat data/acts_stage4/prod/C1/chain_log.txt
```
