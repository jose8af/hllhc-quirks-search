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
