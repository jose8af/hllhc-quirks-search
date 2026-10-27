# A2FC: the V4-6 full-chain revert of A2 (C001 TT, Stage 4)

Executor, 2026-10-16. This is a pre-registered rule application, authorised by the orchestrator: `plan.md` l. 1254-1255 and
l. 1813 (V4-6) say that an A2 point with a CKF signal-stealing fraction above 5 % reverts to the full chain. The trigger is
`investigation/INV_SIGNAL_EFF.md` item 3 and §7.

**No frozen production file was changed.** `run_stage4.py`, `run_g1b.py`, `run_chain.py`, the finder and `s4sig.py` are
untouched, so HASH_ADDENDUM needs no §7. Every output records the same `code_sha256`, `g1b_sha256` and `frozen_inputs` as
the C1 A5 and A2 files, with T_seed = 4 [V].

## 1. Revert set (pre-declared, before any production)

The revert set was written to `investigation/V46_REVERT_SET.json` at 10:19:30, before the manifest (10:20:25) and the
launch (10:20:30); sha256 `32e1c6c3a9b9b5e4…`. The script is `investigation/v46_revert.py`.

- **Source.** Production C1 A1 (full chain, no PU).
- **Population.** As in INV §4: status 1, not probe-excluded, |η_pair| < 1.
- **Per-event quantity.** f = n_q_ckf / n_q_written.
- **Rule.** A point reverts if the event-mean ⟨f⟩ > 5 % **or** the pooled Σn_q_ckf / Σn_q_written > 5 %. Taking either
  metric is the conservative choice.

V4-6 values (⟨f⟩ / pooled, in %) at the eight A2 Λ points. Values at ≤ 1.5 keV are all ≤ 2.1 %.

| Λ (keV) | E200 | E500 | E1000 | E1500 | Ẽ500 |
|---|---|---|---|---|---|
| ≤ 1.5 | ≤ 0.5 | ≤ 2.1 | ≤ 1.4 | ≤ 1.5 | ≤ 1.3 |
| 2 | 1.9 / 1.7 | 2.0 / 2.4 | 1.8 / 1.6 | 1.8 / 1.9 | 0.3 / 0.2 |
| 3 | **5.6 / 5.4** | **5.2 / 5.1** | **7.2 / 6.3** | **5.9 / 6.9** | 0.8 / 1.9 |
| 5 | **14.1 / 14.4** | **13.5 / 13.0** | **11.7 / 13.8** | **17.4 / 20.5** | **9.6 / 12.5** |

**Revert set: 9 points.** These are {E200, E500, E1000, E1500} × {3, 5} keV plus Ẽ500 at 5 keV. **Ẽ500 at 3 keV does
not revert** (0.8 % / 1.9 %), and no point at 2 keV or below does.

## 2. Production

- **Driver.** `acts/stage4/run_a2fc.py` is a new file. It writes `jobs/A2FC.json` and calls the unchanged
  `run_stage4.cmd_run` / `cmd_check` with campaign 'A2FC' (sha256 `b4c4595b…`; manifest sha256 `6eff1bbd…`).
- **Job kind.** Frozen `a5`: `run_chain.py sig` with PU 200, quirk SimHits through ACTS digitisation and CKF. Top-up,
  PV, MET and trial seeds are the row-keyed A2 ones.
- **Jobs.** One A2FC job per (revert point, A2 job): 9 × 20 = **180 jobs, 1 800 events**.
  - `rows` = the A2 job's rows in the same order, so the ACTS event numbers match.
  - The chain `seed` = the A2 job seed.
  - Each job carries `paired_a2_id`.
- **Run.** `nohup nice -n 5 caffeinate -i pixi run python -m acts.stage4.run_a2fc run --workers 7 --mem-gb 19`
  (PID 38514).
  - Wall time 1.41 h (10:20 to 11:45). CPU **9.7 CPU-h** (sum of job walls; estimate 10.0).
  - 180 ok, 0 errors. Disk 4.37 GB. Logs are `prod/A2FC/run_stdout_A2FC.txt` and `_progress_*.jsonl`.

## 3. Checks

**`run_a2fc check --deep`** (= `run_stage4 check`): 180/180 valid, 0 missing, **V4-1: 1 failure**.

- **The failure.** `A2FC_F1000_L3_000`, event 6 (row index 6 of A2_F1000_000).
  - **3 PU SimHits of 145 007 got no measurement.** That is ACTS bounded smearing, and the G1 tolerance is ≤ max(2,
    10⁻⁵ n), so the job fails.
  - The quirk closure is exact (n_sig_simhits = n_sig_meas = 51; `sig_v41_pass` = True).
  - The same row at 5 keV loses 2 hits and passes.
  - Re-running would not change this, because the chain is deterministic.
- **Recommendation (orchestrator decision).** Admit the job with this note. The loss is PU-only, 2 × 10⁻⁵ of the event's
  PU hits, and has no bearing on the quirk hits. The analysis does not gate on `v41_pass`.

**Pairing (`investigation/a2fc_pairing.py`; `data/acts_stage4/investigation/a2fc_pairing_*.json`).** Three jobs were
checked: A2FC_F200_L3_005, A2FC_F500_L5_007 and A2FC_S500_L5_013. On all three, the following match the paired A2 job:

- the row list and order (sig.tab);
- the chain job seed;
- the A2 chain PU event seeds = hseed('sigpu', spin, m, row) of the A2FC rows;
- the PU SimHit count and the particles-in count, per event;
- the PU BTL row count.

**Re-run of the A2 PU-only chain for A2_F200_005.** Event by event, the PU measurements have **identical SimHit truth,
barcodes and surface ids** (max |Δtruth| = 0). One exception: event 3 has 1 PU measurement fewer in A2FC (bounded
smearing).

The measured positions are **re-smeared**: 0 % are identical. The median |Δxyz| is 0.029 mm (IT), 0.41 mm (PS), 13.8 mm
(2S) and 16 mm (BTL), which is resolution and strip/bar length. ACTS draws the digitisation smearing from one per-event
stream, so the injected quirk SimHits shift the PU draws. **Pairing therefore holds at the level of the PU event and its
Fatras SimHits.** The PU measurement noise is an independent draw, as it already was in A5 vs A2 at 1 keV (A5 even used a
different Fatras seed). The quirk-hit path is the intended difference.

**Results** (`investigation/a2fc_summary.py` → `data/acts_stage4/investigation/a2fc_summary.json`):

| point | V4-6 with PU, all surfaces | V4-6 with PU, barrel fid ⟨f⟩ | in-job ε_fckf(R04), all rows: A2FC / A2 | central (\|η\|<1): A2FC / A2 |
|---|---|---|---|---|
| E200 3 | 5.6 % | 9.2 % | 0.272 / 0.313 | 0.810 / 0.931 |
| E200 5 | 12.6 % | 11.5 % | 0.285 / 0.330 | 0.810 / 0.921 |
| E500 3 | 4.0 % | 2.3 % | 0.380 / 0.400 | 0.961 / 0.987 |
| E500 5 | 10.1 % | 14.3 % | 0.325 / 0.405 | 0.816 / 1.000 |
| E1000 3 | 2.3 % | 1.9 % | 0.232 / 0.242 | 0.909 / 0.955 |
| E1000 5 | 9.0 % | 11.8 % | 0.226 / 0.277 | 0.837 / 1.000 |
| E1500 3 | 2.3 % | 4.2 % | 0.290 / 0.310 | 0.871 / 0.919 |
| E1500 5 | 12.9 % | 17.9 % | 0.250 / 0.315 | 0.758 / 0.952 |
| Ẽ500 5 | 4.5 % | 6.3 % | 0.315 / 0.340 | 0.923 / 1.000 |

- The in-job ε is the run_g1b diagnostic definition, not the analysis match.
- The full chain is lower than A2 at every point:
  - by 4-13 % relative at 3 keV;
  - by 7-21 % relative at 5 keV;
  - at |η| < 1, by up to 24 % relative (e.g. E1500 5 keV, 0.758 vs 0.952).
- This confirms INV item 3.
- With PU, V4-6 at 3 keV is below 5 % for E500, E1000 and E1500. The revert decision stays as pre-declared (§1, from
  A1), and the full chain is the reference in any case.

## 4. Interface for the analysis (substitute A2FC for A2 at the revert points)

**Files.**
- Manifest: `acts/stage4/jobs/A2FC.json`. Read it with `common.manifest('A2FC')`, `job_files(['A2FC'])` or
  `collect(['A2FC'], kinds=('a5',), expect_tseed=4, …)`. It lists 180 job dicts.
  - Common fields: `kind='a5'`, `sample='A2FC'`, `campaign='A2FC'`, `point='p2/<S>_m<M>/L<Λ>_BM'`, `rows`, `seed`.
  - Pairing fields: `paired_a2_id`, `paired_a2_out`, and `lam` (float).
- Outputs: `data/acts_stage4/prod/A2FC/A2FC_<S><M>_L<Λ>_<chunk:03d>.npz`. Read them with
  `common.PROD.joinpath(*job['out'].split('/'))`. Example: `A2FC_F500_L5_007.npz` ↔ `C1/A2/A2_F500_007.npz`.

**Schema.** The schema is identical to the C1 A5 files. `signal.analyse_file` / `aggregate` handle it unchanged through
the a5 branch: `point_of(job)` parses `point`, and cfg = 'BM'.
- `sig.tab` has one row per event (SIG_COLS). `n_q_ckf` is now filled.
- The quirk BTL rows are inside `btl`, with INT % 10⁶ = 4000. There is no `sig.qbtl`; analyse_file merges both
  layouts the same way.
- The `dump.*` arrays are the chain events, about 24 MB per job. They are not needed: load with `keys` / `prefix`
  excluding `dump.` to save memory.

**Substitution rule.** For each (spin, m, Λ) in `V46_REVERT_SET.json['revert_set']`:
1. Drop the A2 entries of that point. These are C1 A2 files of that species-mass, sig.tab rows with `lam` == Λ.
2. Use the A2FC entries instead. aggregate() keys them `A2FC|<spin>|<m>|<Λ>|BM`; relabel them to the A2 key
   `A2|<spin>|<m>|<Λ>|BM` (sample 'A2').
3. Every other A2 point stays as it is.

**Why the substitution is consistent.**
- Denominators are identical. A2FC has the same 200 template counting rows per species-mass, and every row is status 1
  at 3/5 keV.
- Probe exclusion uses the same `run_g1b.probe_excluded`. Row, status and probe_excluded columns are checked equal to
  the A2 entries for all 180 jobs [V]. Excluded rows: E200 3 keV 5, E1000 3 keV 10, E1000 5 keV 5, all other points 0.
- Row IDs are shared with the A2 rows at the other Λ, so the row-level bootstrap across Λ stays paired.
- **Ẽ500 3 keV is NOT in the set: keep A2 there.**

**Admission.** The code, g1b and frozen-input hashes equal C1's, so A.3/addendum admission passes as for C1 A5. The only
flag is `A2FC_F1000_L3_000` (`meta.v41_pass = False`, §3).

## 5. Files

- New files:
  - `acts/stage4/run_a2fc.py`
  - `acts/stage4/jobs/A2FC.json`
  - `acts/stage4/investigation/{v46_revert.py, V46_REVERT_SET.json, a2fc_pairing.py, a2fc_summary.py}`
- Outputs:
  - `data/acts_stage4/prod/A2FC/` (180 npz plus logs)
  - `data/acts_stage4/investigation/{a2fc_pairing_*.json, a2fc_summary.json}`
- Nothing under `prod/C1`, `analysis/`, `WP_RULE*.md`, `frozen_inputs.json` or `HASH_ADDENDUM.md` was modified.
