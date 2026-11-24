# Session log — Aurora (Fable 5.2, executor), work package p3-a: FINAL classification of the pilot

Started 2026-11-24 10:16 -0500 (`date`). Brief: PHASE3_BRIEF.md; task prompt of the orchestrator (24 Nov 10:08).
Abbreviations as in the brief (STR, ADD, EXP, COM); TOV, ING, CEC, BJO, NIL (Nils), YLV (Ylva) = the Phase-2 rule-1 files.
Tags: VERIFIED = measured or re-derived by me; ESTIMATE; UNVERIFIED = transcribed.

## Read before planning (all in full unless a range is given)
AGENT_RULES.md; CLAUDE.md study overrides; agents/executor.md; phase3_selection/CLAUDE.md; methodology/03-phases.md
l.358-529; EXP whole; STR §4.4 l.724-1118, §4.12 l.1789-1896, §11.7 l.2713-2780, §2 l.197-281, l.160-196; ADD §1
l.116-270, §3-§4.3 l.353-621; TOV, ING, CEC, BJO, NIL, YLV whole; PDM (first half); LOG.md l.972-1009; code
p2w_subset.py, p2t_classify.py, p2t_counts.py, p2t_rule1_prelim.py (whole), review_nils_subset.py (most),
p2z_addendum1.py / strategy_budget.py (constants only); frozen_inputs.json; production.full_set_flags.
Not read: methodology/11-coding.md in full (rules taken from CLAUDE.md "Coding Rules"), COM rows beyond those quoted in
EXP, HED and ESK beyond their EXP summary (HED's P7 verdict and ESK's counts are used as quoted in EXP §5.2, §7).

## Facts established while reading (before any pilot array was opened by me)
1. Frozen hand-over variant = ADD P6 (per stream): radius cut for DIF, NI 22/30/61.5, NI-X; option (a) "hybrid" for
   DIF-C and NI-C; `autoh` for hs and lowpt. The pilot files were generated with it (file meta `trunc_mode`,
   `handover`, `beta_min` = 0.1; seen in dif-0000 and difc-0000). So the Phase-2 classification already ran on the
   frozen variant; "final" needs no new chain run. I verify the meta of all 623 B1/hs/lowpt files in the job.
2. T2 candidates (STR l.1794-1798): L = R07, R08, R09, R11, R14, R17, R20; F = FB(k_adm), k_adm in 0..4 per hypothesis
   (wp_rule_tables.py l.72); each with/without the displaced-vertex veto (a B3 conditional: no credit in H). H applies
   counting and width cuts only (STR l.799-802): one count per (width, s): R07 = (9.4 mm, s=0); R08=R09=R11 = (4.7, 0);
   R14=R17=R20 = (4.7, 3); FB(k) = (none | 37.5 | 18.75 | 9.4 | 4.7 mm, s=3) (production.full_set_flags l.180-183:
   fb0 = R04 & p>0.05 & N_2S2>=3, FBk = fb0 & w < W_K[k-1]). So FB(0) needs the R04-width count with s = 3: Nils's
   condition on the R04 width (STR l.761-763) touches a T2 candidate, not only an information row.
3. "The finder's maximum core width (frozen configuration)" (STR l.761-762): frozen_inputs.json has w_c_mm = 75.0 (the
   collection half-window |u.n2| < W_c). No Phase-2 document transcribes a "maximum core width" (grep: none). Two
   readings: (A) w_core < 75 mm (Tove's and Bjorn's coding of R04); (B) only the collection window, i.e. no cut on
   w_core (Cecilie's coding; w_core can then reach 1.4826 x 75 = 111 mm). Both are counted; not chosen.
4. STR, ADD and COM say nothing on hit merging before the finder, nor on the PV of the Z(nunu) pilot (grep 'merg',
   'PV': only v1's clusters/[L8], and "through the PV", STR l.757). Both are open; counted under every reading.
5. The binding run needs a THIRD swap besides the two in my prompt: ADD l.607 "M = Sum w / w_max; 1.011e6 with v1's
   weights, replaced by the day-12 MET model", ADD l.360 "'41' is provisional ... recomputed with the v2 MET model at
   day 12". The Phase-2 classifiers skipped the 1,297,459 events with w_v1 = 0, so a v2 weight that is non-zero where
   w_v1 = 0 could not be counted. I therefore classify ALL 2.3e6 Z(nunu) events in the base pass and keep w per row.
6. Attribution (STR l.747-753) in the pilot: the Z(nunu) pilot has mu = 0 and no Geant4 vertex, so every hit is of the
   hard-scatter class of STR l.230 (Fatras-traced, conversions included): every counted witness is "attributed" by
   construction (j = N_L2 >= n - k_max >= n/2). In B1/hs/lowpt files the parent hadron is a Fatras particle and the
   products are the Geant4-vertex class: j per class needs the witness's hit truth; dumped for every non-Z row.

## PLAN (written before any code or job)

### Scripts (phase3_selection/src/p3a/)
- `p3a_subset.py`: the final classifier job. Imports p2w_subset.py UNCHANGED (sha256 checked = c68b7b69...) for the
  BASE reading (her plane_best, prefilter, _greedy, _eval), so the Phase-2 numbers must be reproduced row by row
  (regression: every k of her 5 widths x s x S/F equal, all rows). Adds, per aligned plane, own-code categories:
  c0 full set, finder axis; c1 full set, own axis; c2 her window heuristic (7 offsets, axes = plane's and each IP hit),
  own-axis judged, run always; c3 PLAN-S4 centres as written (each IP hit and each midpoint of neighbours, plane's
  axis); c4 hard-window witnesses (every IP hit of the subset inside one window of full width 2W/1.4826; Nils's H).
  Widths: none (collection window only), 75, 37.5, 18.75, 9.4, 4.7 mm; s = 0, 3; readings S, F; for s = 3 also k_IP of
  the best witness (k per layer type). Options: --no-merge (pool without chain_inputs.merge_pool), --pv draw|true|draw2,
  --all-w (Z events with w_v1 = 0 too). Witness of the R08/s=0 best subset: hit-truth summary per row; full hit table
  for non-Z rows. File meta (trunc_mode, beta_min, handover, mu) copied to the output.
  Readings formed downstream (none chosen): BASE (as produced in Phase 2), PLAN-S4 = min(c0, c3), OWN-AXIS =
  min(c1, c2, c3 under own axis, c4), HARD = c4, UNION = min of all (information, like Nils's 1,610).
- `test_p3a_subset.py`: Cecilie's T1-T8 run through my kernel (BASE must equal hers on every synthetic event), plus
  T9 own-axis <= full set, T10 hard-window flag on a constructed event, T11 an independent pure-numpy verifier
  (Nils's `verify`, imported unchanged, + my 2S count) accepts the dumped witness.
- `p3a_indep.py`: independent re-derivation at R05, R06, R07 and R04(75) for s = 0 and s = 3 with NILS's search and
  verifier (review_nils_subset.search_event / verify imported unchanged, W passed as argument; N_2S2 of his verified
  witness counted by me), on every event that has a row in my BASE outputs (his 'rows' mode). Addresses his condition
  "R04-R07 and s = 3 not re-derived". It gives "confirmed by an independent search" counts, not replacement numbers.
- `p3a_counts.py`: counts per term, width, s, reading, pool, PV, flagged variant, weight class; own-hit classes
  (k; (k_IP, k_2S)); falls per width step; 1/H(R06); regression against ING's JSON; -> outputs/p3a/p3a_counts.json.
- `p3a_rule1_dryrun.py`: NOT BINDING projection. Reuses p2z_addendum1.py (approved constants and streams) and the
  arithmetic of p2t_rule1_prelim.reading (regression: reproduce ING's 63,169.7 with her M first, and the empty pilot
  160.8 / 238.3 / 262.3 / 283.8), then M = 993,885.9. Inputs swapped by path only:
  outputs/p3a/inputs/pileup_rows.json (now: v1-based EST rows of strategy_budget.py l.669-685; later Casper's),
  outputs/p3a/inputs/met_ntrig.json (now: planning N_trig of Z(tautau), lost-lepton Z(ll), multijets; later Birgit's),
  outputs/p3a/inputs/z_weights.json (now: "v1"; later per-event v2 MET-model weights, see fact 5).
  B50 at every T2 candidate; where no pile-up row exists (R07 has a direct v1 rate; R14-type "at most the R11
  value"; FB none) every allowed reading is given, including "no pile-up term" (a lower bound, 'above' only).
- No figures are planned (tables only); if one is added it follows appendix-plotting.md.

### Campaigns (runner, SSH, landau, <= 3 jobs, <= 30 min each, per-job NUMBA_CACHE_DIR, prefix p3-a-)
Unit cost measured in Phase 2 (markers of p2-c-r1v-s2a/s2b/s3a/s3b, VERIFIED now): one full pass of p2w_subset.py =
2.89 CPU-h (Z 2.28 for 1.0e6 events with w > 0 in 23 jobs, longest 1,315 s wall; B1+hs+lowpt 0.61).
| campaign | what | CPU-h (ESTIMATE) |
|---|---|---|
| slices over ssh | tests, timing, regression on 2 Z files + 1 file per stream | 0.5 |
| p3-a-cls-m | BASE pass: merged pool, PV draw, all streams, ALL Z events (w = 0 too) | 2.9 x 1.3 (extra categories) + 3.0 (w = 0 events) = 6.8 |
| p3-a-cls-u | pool NOT merged, PV draw, all streams, Z with w > 0 | 3.8 x 1.2 = 4.5 |
| p3-a-cls-pv0 | merged, PV = true vertex, Z only, w > 0 | 3.0 |
| p3-a-cls-pv2 | merged, PV draw with another seed, 115 Z files (every 4th): size of the seed effect | 0.8 |
| p3-a-ind | Nils's search at 4 widths on the row events | 3.6 (his R08 pass: 0.9) |
| **total** | | **19.2** (budget 20; stop and report before 26) |
Order: tests -> timing slice -> cls-m -> counts + regression -> cls-u -> cls-pv0 -> ind -> cls-pv2. If the timing
slice projects cls-m above 9 CPU-h, the w = 0 events are moved to a separate campaign definition and reported, not run.
If the total projects above 26 I stop before the campaign that would cross it and report.

### Checks (pre-declared)
- C1 regression: my BASE rows = Ingvild's rows (all 5 widths, s, S/F) for every (file, event, orientation) with
  w > 0; m_Z(R08) = 1,501 (S) / 1,474 (F), 969 / 846 at s = 3; 1,083 files once, none partial. Any difference stops
  the work and is reported.
- C2 monotonicity by construction: k(none) <= k(75) <= k(37.5) <= ... in every category per row; OWN >= BASE where the
  base used the full set; HARD >= OWN. Violations are listed, not removed.
- C3 dry run: empty pilot reproduces 160.8 / 238.3 / 262.3 / 283.8; ING's (S) R09 reproduces 63,169.7.
- C4 independent search: every verified witness of Nils's search with k <= k_max counts as "confirmed".
- Nothing is tuned to make a check pass. No signal file is opened. No efficiency is formed.

### Deliverables
outputs/P3A_PILOT_FINAL_aurora_2026-11-24.md (date of completion), outputs/p3a/*.json, experiment_log.md entries
(DECISION blocks), SLOTS.md lines, DAILY_NOTES.md two lines, final report <= 15 lines.

## Log
- 2026-11-24 10:16 -0500 plan written. Next: SLOTS line, code.
- 2026-11-24 10:39 -0500 tests 4/4 OK (630 CPU-s); slice: BASE rows = Phase-2 rows on znn-00000 (7/7), kernel x1.33 of p2w_subset; w = 0 events cost the same per event -> separate campaign p3-a-cls-m0 (run after the variants); independent search costs 0.25 s/event -> restricted to counted events of every 2nd file. Queue launched on landau 10:37: m, u, pv0, ind, m0, pv2 (3 jobs).
- 2026-11-24 11:08 -0500 PLAN CHANGE (cost, not physics). The jobs of p3-a-cls-m were NFS-bound: wall 980 s for 12 files at 240 CPU-s; a
  169 MB pilot file read at 1.8 MB/s from landau with three of my jobs running (dd, 10:50). One read of the 77 GB of
  Z(nunu) files per variant would have taken about 3.5 h of wall each. I stopped p3-a-cls-m (5 jobs done = 60 Z files,
  kept as a cross-check; 1 failed = killed by me; 3 more killed; about 0.6 CPU-h in all, 0.37 in the markers) and wrote
  p3a_multi.py: every variant from ONE read of each file, p3a_subset.classify_pool imported unchanged.
  Slice checks (znn-00000..3, 1,200 events each): variant m of p3a_multi = p3a_subset rows (7/7 on file 0);
  variant v2 fed with (w_v1, phimet_reco_v1) = variant m (32/32 rows, all columns).
- 2026-11-24 11:08 -0500 NOT RUN: the w_v1 = 0 events (variant m0). Measured 26 ms per event against 8.3 ms for w > 0 (they hold 2.6 times
  more rows: a jet near the MET axis is what fails v1's min-dphi cut and it fills the road) -> 9.4 CPU-h for 1.3e6
  events [ESTIMATE from 2,760 events]. Above my limit; and (found while sizing it) a v2 MET model changes the road AXIS
  (phimet_reco_v1 is v1's reconstructed MET azimuth), not only the weight, so a classification of the w_v1 = 0 events on
  v1's axis would not be the input the binding run needs. Instead: variant v2 of p3a_multi.py takes (w, phimet) per
  event from a file; the campaign is defined, not launched (needs p3-c's per-event MET).
- 2026-11-24 11:08 -0500 New campaigns (definitions tools/runner/examples/p3a/): p3-a-clsxz (115 jobs x 4 Z files: m, u, pv0, pv2 on every
  4th file, ind on every 2nd), p3-a-clsxb (116 jobs: m, u on the 623 B1/hs/lowpt files). Projection [ESTIMATE]:
  Z 3 x 2.3 + 0.6 + 2.7 = 10.2 CPU-h, B1 1.6; with the 1.0 spent so far (tests 0.18, slices 0.2, p3-a-cls-m 0.6)
  about 12.8 of 20. Queue started on landau.
- 2026-11-24 11:59 -0500 p3-a-clsxz running with 3 slots since 11:10 (first two jobs were killed with the 2-slot driver and
  re-dispatched as attempt 2). 16 of 115 done at 11:59: 288 CPU-s and up to 535 s wall per job (4 files, NFS-bound).
  Mistake of mine, recorded: my first two "stop" commands used pkill -f with a pattern that matched the ssh shell
  running them, so the shell died before the driver was killed; p3-a-cls-m kept dispatching until 11:08 (6 jobs
  started in all: 5 done, 1 failed; 2 more killed at 11:08). Bracketed patterns since.
- Cross-check on the 40 pilot files that both drivers have classified: rows of p3a_subset.py (p3-a-cls-m) = rows of
  variant m of p3a_multi.py, 1,351 of 1,351, every column [VERIFIED, p3a_xcheck.py].
- Smoke test of p3a_counts / p3a_rule1_dryrun / p3a_indep_summary / p3a_tables on the first 60 files (code test, no
  result quoted): runs; dry-run checks 1 and 2 pass (empty pilot 160.8 / 238.3 / 262.3 / 283.8; Ingvild's S and F
  readings reproduced bit for bit). One ssh slice (witness check on 2 files, nice 19) ran beside the 3 jobs for a few
  minutes at 12:00: a fourth process, against my cap; not repeated.
