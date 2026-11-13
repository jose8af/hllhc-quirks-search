# Job ledger

Written only by the runner in `tools/runner/` (see `phase1_strategy/outputs/feasibility/FEAS_C_runner_boris.md`).

- `markers/<campaign>/<shard:03d>/<job_id>.marker`: **one marker per job**, JSON Lines, one line per event
  (`started`, then `done` / `failed` / `timeout` / `oom` / `killed` / `lost` / `corrupt` / `verify_failed`). The
  wrapper writes a line only after the output's atomic rename on cajuela and its sha256 check; the `done` line lists
  every output (path, sha256, bytes) plus CPU s, max RSS, wall s, node and mechanism. Each marker has one writer at
  a time and is updated by rewrite-to-`.part` + rename. A file without a `done` marker does not exist for the
  analysis. `markers/<campaign>/_driver/` holds the launcher lock and state (not markers).
- `jobs.tsv`: **derived**, rebuilt from markers by one command (never appended to):
  `tools/runner/bin/qv2run rebuild-ledger`. One row per output file (jobs without outputs: one row). Columns:
  `job_id campaign mechanism node status cpu_s max_rss_mb wall_s output sha256 bytes attempts end_time`.
- Completeness comes from markers only (`qv2run status <campaign.json>`), never from listing cajuela.
- Phase-1 runner validation markers live in `phase1_strategy/outputs/feasibility/runner_ledger/` (tests), not here.
