# Investigator Jorund — regression ticket for the C1 SM family (v) failure

Started 2026-11-18 12:23:17 -0500. Role: agents/investigator.md. No fix, no tuning, no campaign, no git.
Read: AGENT_RULES.md, CLAUDE.md STUDY OVERRIDES, agents/investigator.md, methodology/06-review.md §6.7, Ignatius log (whole),
c1_compare_sm_ignatius_2026-11-18.json, STR §4.1 (l.549-668), COMMITMENTS Amendments E1-E3 (l.286-298), Rosalie successor section (l.302-369).
Blinding: no p2-a-c1-siga* file opened or listed.

## Log
- 12:25 Lead 2 (width) VERIFIED as the cause candidate: c1_compare.py fam_sm l.350 takes s_ln_used of v1 Term.evaluate
  (background.py l.205: max(s_ln or 0, 1/sqrt(N)) with N = presel-WEIGHTED CANDIDATE sum; 1/sqrt(39032.5)=0.00506, 1/sqrt(40057.1)=0.00500),
  i.e. a Poisson error on candidates, not an event-level error. Event-level width from the 50 c1-sm outputs + smregen weights
  (landau, nice 19, script piped by stdin, ~1 min): R04 analytic 0.0510, event bootstrap (2000 replicas) 0.0505, 50-job chunk scatter 0.0478;
  R05 0.0519; R06 0.222. ~47 candidates/event, sd 57.6, max 523; 849/2000 events with w>0. z with event widths both sides
  (v1 width := v2 width, ESTIMATE since v1 per-event counts are lost): R04 +0.36, R05 +0.60, R06 +0.53.
- Lead 1 (environment): c1-sm chain step runs through 'pixi run --manifest-path acts/pixi.toml' (run_stage4.py l.267) -> activated env;
  Pythia 8.312 in both locks (v1 osx-arm64 build 7, v2 linux-64 build 107); CP5 card sha identical (3002a2a3...); s4pu.py differs only in
  mpi_init_lines directory (diff: l.22, l.112-115); gen_d123.py identical. Init file hs_Znunu_j.dat mtime 09:12:33 = created by c1sm-0000
  itself (job start 09:12:25, log), not by the failed c1-gen jobs (gen_d123 nt uses tt=None, no init file). smregen 2000/2000 MET match.
  HS generator-level checks v2 vs v1 (sm_regen.json tracked in v1): tries/event 3.264 +- 0.062 vs 3.346; mean w 0.4107 vs 0.4189 (rel se 2.6 % each);
  w>0 849 vs 865.
- 12:27 C'_PU family: same s_ln_used path (c1_compare.py l.253-254); v1 factors s_ln None, 1/sqrt(N) (v0 R04 859/500 -> 0.0341). Flagged in the ticket.
  Pilot HS scripts (p2c_hs0, p2x_hs0, p2x_hspool, p2a_hspool, p2c_b1, p2x_b1): no use of sm_term/depth_term/Term (grep). Forced tt-bar: p2c_hs0.py l.43-47, run-time injection.
  c1-sm CPU 14.51 CPU-h (50 done markers). Decision point 1 = 21 Nov (PHASE2_BRIEF l.4).
- 12:27 WROTE phase2_exploration/REGRESSION_TICKET_SM.md; replaced the placeholder line of regression_log.md with the first entry. No git, no campaign, no file on landau.

## Script run on landau (stdin, envs/tt python, nice 19)
Reads p2-a-c1-sm/000/c1sm-*.npz (cand.tag, cand.n_hs_band, cand.rungs, cand.trial, trials.ev, meta_json) and p2-a-c1-smregen/000/*.json;
mask (tag&1)>0 & n_hs_band>=1 & rung bit (cols 3,4,5) as background.sm_term l.712; x_ev = w_presel * count; analytic se, 2000-replica
event bootstrap (seed 12345) of ln mean, scatter of the 50 job means. Output numbers are in the ticket §1.
Not done: v1 event-level width (per-event counts lost); C'_PU width (inputs incomplete); joint-bootstrap family coherence (fix agent).
