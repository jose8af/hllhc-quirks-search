# Session log: investigator Jorunn (Opus), p3-f (B2 occupancy cause investigation + thinning re-find yield)

Started 2026-11-24 14:55 -0500 (`date`), on einstein (editing/launch only); compute on maxwell (1 job until 19:00,
up to 3 after 19:00 and at weekends). Budget 25 CPU-h (A 15-20, B <= 5), stop before 32.
Read: AGENT_RULES.md, CLAUDE.md STUDY OVERRIDES, PHASE3_BRIEF.md, agents/investigator.md, P3B (all), DOR §0-§2,
ADVISOR_B2CAP_freja (incl. Addendum 1), STR l.340-548, l.1119-1228, l.2713-2760; code src/p3b/{occ_core,occin_job,
occ_replay,closure,cols}.py, chain finder.py, kernels.py (seeds, refit, dedup, cand_vars), production.py
(full_set_flags, process_trial grouping), weights.group_sets.
Seal: dev.pu1 is NOT opened by this session (no read of p3-e-devpu1 outputs).

## 14:55 start
- maxwell: load 3.07, 5 users, p3-d-pyhf running 2 jobs (Gorm). My cap: 1 job now.
- 14:57 orchestrator correction: maxwell cap 4 jobs IN TOTAL shared with Gorm (p3-d, <= 2). Before 19:00: 1 job.
  After 19:00: up to 4 - (running `qv2run job` count on maxwell), checked with
  `ssh maxwell 'pgrep -u jdochoa -f "qv2run job" -c'` before each launch. dev.pu1 campaign starts this evening elsewhere.

## 15:00 method hashed (before any p3-f job)
- `outputs/p3f/CAUSE_METHOD_jorunn.md` sha256 99dfcafb6c477bf11606b0716321170157c33cf4be0bbac00b8df50d99c60d83 (2026-11-24 15:00:57 -0500)
- Note: the method header says "15:00-15:25"; the file was in fact complete and hashed at 15:00:57 (header end time
  was written ahead; not edited to keep the hash). Before the hash only one read-only look at p3-b outputs was run
  (14:56, maxwell, nice 19: layer-mask multiplicities of `p3-b-occin/occin-000.npz`, no direct count, no rung ratio
  beyond the R04/R05/R06 plane counts of that file already in P3B): IP2>=6&IT2>=3 = 1.5 % of configurations, R04 0.09 %.

## 15:05-15:12 code and smoke tests (maxwell, 1 process, nice 10; scratch /home/scratch/jdochoa/p3f-test, not cajuela)
- Code `src/p3f/occx_core.py`, `occx_job.py` (imports p3b occ_core/occ_replay/thin_core unchanged).
- Smoke (1-2 trials, 2,000-20,000 configurations): runs; at 2x10^4 configurations per trial R04 fixed/refit 14/12 and
  13/9, 263/253 refit-eligible. Timing ~0.22 ms per configuration (fixed band), refit only on eligible ones.
- **Code defect found and fixed before any campaign (method A.2 "box" rule):** with the uniform box + doubling rule the
  local sampler found few members (median 3 of 64) and V = 0 for some configurations (an HT term 1/0); cause: the R04
  neighbourhood is often far smaller than the geometric initial box (a configuration passing R04 marginally loses R04
  under a shift of a fraction of a sigma) and elongated along hit-geometry directions. Fix (same estimand, unbiased
  for any covering proposal): proposal = equal mixture of 11 nested uniform boxes (half-widths base x 2^s,
  s = -6..4) in coordinates aligned with the eigenvectors of the band-constraint matrix Q = sum g g^T,
  g_i = (-w_i, rho_i)/sigma_i (Delta d_i = -omega_a w_i + omega_2 rho_i), weight w/q(c); the edge rule acts on the
  largest box; boost x4 of N_loc once if a rung the configuration passes has < 3 members. N_loc = 256 (1,024 for R06
  passers) instead of 64/256 (precision; changed once, before the campaign, from the smoke test, as A.2 allows).
  After the fix: members median 88-106 of 256, no V = 0 (2 trials). Only R04 volumes were looked at.
- 15:10 validation run started (V1: 4 trials of c1pu1-0001 at 2x10^5 configurations; V2: 2 trials of c1pu1-0002 at
  10^6), maxwell 1 process nice 10, outputs in scratch. First V1 trial: 89 s, R04 fixed/refit 191/158, 3,239 eligible.
- 15:13 campaigns written (`src/p3f/campaigns/p3-f-occx.json` 100 jobs x 2 files; `p3-f-refind.json` 20 jobs x 2
  files, 3 draws); occx dry-run loads (100 jobs). Analysis scripts occx_ana.py, val_ana.py, refind3_ana.py written.

## 15:16-15:27 validation V1/V2 (R04 only) — V1 FAILED
- V1 (4 trials, 2x10^5 configurations) + V2 (2 trials, 10^6): recapture/expected 2350/2855 = 0.82 (fixed), 2376/1661
  = 1.43 (refit); per (trial, map) 0.33-6.9; single configurations carry up to 75 % of an expected sum (heavy-tailed
  V-hat). Greedy distinct classes of R04 configurations 27/73/159 and 25/71/173 (fixed), 21/49/107 and 20/47/120
  (refit) at 10^5/3x10^5/10^6: not saturating, far above the finder's 171 groups per trial. HT G(R04) per trial
  5x10^3-4x10^4 (unreliable). CPU of the validation: 330 + 624 s.
- Not a code bug fixable inside the method -> amendment A1 (verdict measurement M_T = per-configuration refit transfer;
  criterion unchanged; C2 folded into the campaign), written before any campaign and before any R05/R06 quantity.
- Code: occx_job.py mode 'counts' (no volumes); scan_trial stores refit counts of fixed N_IP2 = 5 configurations.

## 15:30 amendment A1 hashed (before the campaign)
- `outputs/p3f/CAUSE_METHOD_jorunn_A1.md` sha256 7f0e545a950582f347299d78d47f3cbcf9a05e92d332886e07119b20fa368b34 (2026-11-24 15:30:28 -0500)
- 15:31 timing (counts mode, N_IP2 >= 5 eligibility, 10^4 configurations): 3.4 s per trial -> campaign ~15 CPU-h
  ESTIMATE (16,000 trials), 100 jobs of ~9-10 min CPU.
- 15:32 **p3-f-occx launched** (A1 hash recorded above first): `qv2run ssh launch .../src/p3f/campaigns/p3-f-occx.json
  --nodes maxwell --max-per-node 1 --on maxwell` (driver pid 205840 on maxwell; Gorm had 1 qv2run job running).
- 15:42 occx-000 done: 551 s CPU, 563 s wall, max RSS 522 MB -> 100 jobs ~15.3 CPU-h; serial at 1 job ~16 h.
  Plan at 19:00: restart the driver with the allowed slots (4 - running qv2run jobs on maxwell); refind3 smoke test
  then p3-f-refind in one slot, occx in the other(s).
