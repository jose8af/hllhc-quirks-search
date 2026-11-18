# Executor Ignatius — Phase 2, channel (i) successor of Rosalie (C1 reproduction, C2 finder checks)

Session log (crash-resilient notebook). Started 2026-11-18 10:46:19 -05 (`date`). Compute share: landau slot B only
(1 concurrent job; queue `src/queue_slot.sh` with `logs/queue_landau_B.txt`). Leave alone: landau slot A
(p2-a-c1-pu1), maxwell (c1-cppua, c1-cppub). No pilot/production campaigns, no runner code changes, nothing heavy on
einstein, no git, no subagents.

## 0. Read (Read tool)
AGENT_RULES.md; CLAUDE.md STUDY OVERRIDES; agents/executor.md; PHASE2_BRIEF.md; Rosalie's log §1 and the successor
section of 2026-11-17 08:15 to the end; EXPLORATION_i_rosalie; V45_RESULT_rosalie; COMMITMENTS "Amendments E1–E3"
and rows C1-a…e, C2-a…c; STR §4.1–§4.2 (l.549–707). v1 normalise.py (rates/N_trig definitions), gen_d123.py.

## 1. Blinding (as Rosalie §1, unchanged)
siga2/siga5 outputs opened only through `c1_signal_compare.py open`; never `sealed`; no signal efficiency outside
R01–R06. V4-5 restricted scan on signal: direction differences and scores only, first F0-accepted events in file
order (the code already does this), no counts of scanned rows.

## 2. PLAN (written before any code or job)

### D1. c1-gen (rates family (iv))
- Diagnosis (done while planning, VERIFIED): the c1-gen command runs `$QV2/acts/.pixi/envs/default/bin/python`
  directly; the conda activation script `etc/conda/activate.d/activate-pythia8.sh` (which exports PYTHIA8DATA =
  $CONDA_PREFIX/share/Pythia8/xmldoc) never runs, and `pythia8.Pythia("")` finds no XML ("in XML 0.000").
  c1-sm runs `envs/tt` python → `c1_pu_job.py`, a different route. Channel (iii)'s `p2c_campaigns.py:20` already
  exports CONDA_PREFIX/PYTHIA8/PYTHIA8_DIR/PYTHIA8DATA for the same env. Fix: no code change; new campaign
  `p2-a-c1-gen2` (same 12 jobs, ids `c1gen2-*`, same args and seed tag qv2-c1-gen) with those four variables
  exported in the command. Test one job's init before queueing? The runner path is the test: first job's log checked.
- Cost ESTIMATE: v1 R2 "~64 CPU-min" for all processes (v1 LOG.md l.259) → ≈ 1–2 CPU-h; each job < 30 min expected.
- Then `c1_compare.py` family (iv): rates per triggered event DIF, PV pair, γ (v1 normalise.build: value = max over
  SM processes of the per-preselected-event rate; DIF adds 200 × min-bias), N_trig total and N_trig(Z(νν)).
  v2 values by running v1's `normalise.build` (QV2 copy) on the merged per-process JSONs; errors: N_trig rel_stat as
  v1 (rel_stat per process, quadrature); for the rate maxima, bootstrap over events is not possible from the JSON →
  error from the per-process objects count. Decide after seeing what the JSON holds (DECISION block).
- Queue fix: `queue_slot.sh` prints the runner's exit code, which is 0 even when all jobs failed; add a
  `qv2run status` line after each campaign and print "FAILED JOBS: n" when n > 0. Recorded here and in experiment_log.

### D2. E2 part (ii) restricted V4-5 scan
- Read `src/v45_bruteforce.py`; add a `--restrict` mode: hit set = F0's inliers ∪ hits within 3σ of the F0 plane
  (σ per hit as in the score); same exhaustive 0.2 mrad grid ±0.3 rad; |Δn| < 1 mrad criterion in ≥ 48/50 per half.
- Campaigns `p2-a-c2-v45rpu`, `p2-a-c2-v45rsig` (3 jobs each, same event selection as v45pu/v45sig), slot B,
  ≈ 1.5 CPU-h total (Rosalie's ESTIMATE). Result file `outputs/V45_RESTRICTED_ignatius_<date>.md`, PASS/FAIL as worded.

### D3. C2-b (V4-4) and C2-c (T_seed) verdicts
- C2-b: c2v44-NN-a vs -b (same node, bit identical), vs -c (maxwell, reported), c2v44x-* differ; seeds in meta.
  Using `day0_summary.identical()`. Script `src/c2_verdicts.py` (both C2-b and C2-c).
- C2-c: pair c2ts2-pu1-NNNN↔c1pu1-NNNN (0000–0024) and c2ts2-pu2-NNNN↔c1pu2-NNNN (0000–0039); check evstats/PV
  identical; per-trial pass fraction per rung family (counting R04, width R05–R06, χ² R09–R11, 2S R12–R14) at T_seed
  4 vs 2; paired event bootstrap; |z| < 2.73 for 8 tests. v1 metric from `acts/stage4/g3/analyse_g3.py`.
  Output `outputs/C2_VERDICTS_ignatius_<date>.md` + json.

### D4. Stitch ratio from 100k INC (p2-a-c1-s2inc)
- TRG c00 vs INC c00..c05 at m 200, σ(pT>200 & pT_ME≥100), √Σw², merge by N_LHE as merge_chunks.py; snippet in
  Rosalie's log ~14:4x. Output `outputs/STITCH_100k_ignatius_<date>.md` with f₂₀₀ implication. Light: run on landau
  nice 19 (light read of LHE-derived files) or through the runner if heavy.

### D5. smregen + remaining c1_compare families
- smregen on c1-sm through a runner job on landau (slot B) with the scratch-TT wrapper (trap in Rosalie's log).
- Families (i) trend slope / c-factor (v1 background.py G3 trend_test / c_test), (ii) C′0 f_pre, (v) SM per-event
  candidates (presel-weighted), (iii) C′_PU when cppua/cppub complete.

### D6. All 41 comparisons and `outputs/EXPLORATION_i_ignatius_<date>.md` when c1-pu1 and c1-cppub complete
  (pu1 ≈ 53 jobs × 20 min ≈ 18 h from 10:50 → ≈ 19 Nov 05:00; may fall outside this session: then STATE FOR A
  SUCCESSOR).

CPU-h budget check: C1 72.1/198 and C2 1.33/81 at Rosalie's 08:14 ledger; this session adds ESTIMATE ≈ 1.5 (gen) +
1.5 (V4-5 restricted) + ≈ 1 (smregen) ≈ 4 CPU-h. Far below the 30 % stop rule.

## 3. Log
- 2026-11-18 10:48:06 D1 fix: campaign `tools/runner/campaigns/p2-a-c1-gen2.json` written (inline python: copy of
  p2-a-c1-gen.json; ids c1gen2-*; command exports CONDA_PREFIX/PYTHIA8/PYTHIA8_DIR/PYTHIA8DATA = acts env, as
  p2c_campaigns.py:20). No chain-code change. Init test on landau: `pythia8.Pythia("",False)` with PYTHIA8DATA
  set → version 8.312 [VERIFIED]. queue_slot.sh edited: after each campaign prints `qv2run status` and
  "WARNING …: FAILED JOBS n" when n > 0 (driver exit code is 0 even when jobs fail). Old queue (pid 1819718, idle
  since 10:05, file queue_landau_B.txt) stopped by PID; new queue started with the edited script and a new file
  `logs/queue_landau_B_ignatius.txt` (the seen-set is in memory, reusing the old file would relaunch 19 finished
  campaigns). Log /home/scratch/jdochoa/drivers/queue_landau_B_ignatius.log. c1gen2-znunuj dispatched 10:47:26 and
  past Pythia init.
  Restart: ssh -x landau "setsid nohup $QV2/phase2_exploration/src/queue_slot.sh landau $QV2/phase2_exploration/logs/queue_landau_B_ignatius.txt > /home/scratch/jdochoa/drivers/queue_landau_B_ignatius.log 2>&1 < /dev/null &"
- 2026-11-18 10:52:23 D2 code: v45_bruteforce.py --restrict added (sha256 before 2943f816…2529; backup
  /var/tmp/jdochoa/v45_bruteforce.rosalie.py): hit set = window hits with |u·n_F0| ≤ 3 s_i(n_F0) ∪ pool hits matching
  the F0 candidate's stored hit record (hit.* CSR, tag&4, position within 1e-3 mm); no global/sphere scan in that mode;
  signal R04 bits now read with bit() (only the R04 bit is unpacked; same values as unpackbits[:, 3]). Campaigns
  p2-a-c2-v45rtest (1 PU trial + 1 signal event), p2-a-c2-v45rpu (3 jobs, same trials as v45pu), p2-a-c2-v45rsig
  (3 jobs, same events as v45sig). v45rtest queued behind c1-gen2; the two real ones are queued after the test passes.
- 2026-11-18 10:52:23 D4 DONE: outputs/STITCH_100k_ignatius_2026-11-18.md. Ratio TRG/INC(120k) = 1.0001 ± 0.0252
  (z 0.00); 20k c00 value 1.118 reproduced (606 rows), it was a fluctuation; chunk χ² 11.07/5 (p 0.050).
- 2026-11-18 10:55:38 D3 DONE: outputs/C2_VERDICTS_ignatius_2026-11-18.md (src/c2_verdicts.py → outputs/c2_verdicts_ignatius.json).
  C2-b PASS (20/20 same-node identical, 20/20 cross-node identical, other seeds differ, seeds recorded). C2-c PASS as
  frozen, no power (families saturated or empty); mean_grp diagnostic +0.32 % at R04 ρ=1 (paired z +28). FLAG.
- 2026-11-18 10:58:36 D5 smregen: src/c1_smregen_job.py (wrapper: gen_d123.TT → $QV2_OUT_DIR/ttroot with links
  data/acts_stage4/g1/pythia_init → $QV2_PYTHIA_INIT_DIR and acts → $QV2/acts; v1 code unchanged); campaign
  p2-a-c1-smregen (2 jobs × 25 c1-sm files, ACTS env + Pythia vars) queued in slot B after v45rtest. The node-local
  init file /home/scratch/jdochoa/cache/pythia_init/mpi_cp5_14tev_hs_Znunu_j.dat (2078 B, 17 Nov 09:12) is on landau.
- 2026-11-18 11:02:32 c1_compare.py extended (sha256 before 8673ba2d…24c3, backup /var/tmp/jdochoa/c1_compare.rosalie.py):
  families closure (slope, c-factor via BG.closure / G3.c_test), cprime (cp0 f_pre, cppu attributed via BG.cprime_term),
  rates (normalise.build on c1-gen2), sm (BG.sm_term with smregen); --families and --out options. Test of cprime on
  partial data (landau, 43 s): cp0 f_pre dif 47538/50000 (z +0.93), ni22 22794/30000 (+0.14), pvpair 90182/100000
  (−0.96) — complete inputs (cp0 16/16 done) [VERIFIED, /home/scratch/jdochoa/ign_c1cmp_test.json on landau];
  cppu partial (cppua 47/50, cppub 20/75): not final. Rates-width DECISION in experiment_log. src/v45r_summary.py written.
- 2026-11-18 11:05:15 closure family test (pu1 148/200 jobs = 11,840 trials, pu2 complete; landau 157 s, 515 MB): slope
  v2 −0.3335 ± 0.0085 vs v1 −0.3608 ± 0.0045 (z +2.83, p 0.0046 > 0.05/41: individual pass, PROVISIONAL); v2 trend has
  3 points (R04–R06; R07 < 10 B1 counts), v1 had 4 (R07: 35); v1 refitted on R04–R06 only: −0.3594 ± 0.0065 (WLS), so the
  point set does not explain the difference. c-factor v2 1.1919 ± 0.0049 at the same cell (bin 2, layers 5,6,9) as v1
  1.1964 ± 0.0022 (z −0.84). Final numbers need pu1 complete.
- 2026-11-18 12:14:00 D1 DONE. p2-a-c1-gen2 12/12 done (10:47–12:13; ttbar_1l 1,549 s, ttbar_2l 993 s: inside 1,800 s).
  Rates family (iv) [VERIFIED, outputs/c1_compare_rates_ignatius_2026-11-18.json; c1_compare.py --families rates]:
  N_trig 4.187e7 vs 4.085e7 (z +0.86); N_trig(Z) 2.649e7 vs 2.508e7 (z +1.26); DIF 1.6275 vs 1.5945 (z +0.41, max = ZZ;
  v1 ttbar_2l); PV pair 53.52 vs 30.31 (z +2.43, p 0.015 > 0.00122: pass; max = ttbar_2l with N_eff 14.9 → width
  ESTIMATE s_ln 0.165); γ 0.566 vs 0.379 (z +0.58, ttbar_2l, s_ln 0.49). Family coherence z +1.68: coherent. All 5 pass.
  Diagnostic (no verdict): N_trig-weighted mean rates v2/v1 = DIF 1.035, PV pair 1.007, γ 1.067; the max-over-
  processes statistic is driven by ttbar_2l (presel-weighted N_eff ≈ 15 of 400 events) in v2 — power of the PV-pair
  and γ entries is poor (2σ detectable shift ≈ ×1.6 and ×3.9): gross checks only.
- 2026-11-18 12:14:44 p2-a-c2-v45rtest done (2/2; 12:12–12:13): PU trial: restricted set 72 hits = 3σ band (72); F0 stored
  record 70 hits, 70/70 matched, 0 outside the band; Δn(F0, restricted opt) 0.28 mrad, Δn(F0, fit) 0.20; selfcheck
  2.7e-5. Signal event: band 151 hits; F0 stored record NOT found (n_f0_record 0) → hit set = band only; Δn 0.00 mrad.
  PERMISSION REFUSED (auto-mode classifier, "Unauthorized Access"): listing the key NAMES of one siga5 npz to see whether
  signal outputs carry hit records. Not worked around. Consequence: the signal half uses the 3σ band only; the PU half
  measures whether the finder's record ⊂ band. Queued p2-a-c2-v45rpu, p2-a-c2-v45rsig after p2-a-c1-smregen.
- 2026-11-18 12:14:44 p2-a-c1-smregen-0 done (42 s wall; 25 jobs × 40 events, hs_met 40/40 each per the job log).
- 2026-11-18 12:17:30 D5 SM family (v) [VERIFIED, outputs/c1_compare_sm_ignatius_2026-11-18.json]: smregen 2/2 done, hs_met
  reproduced 2000/2000. Z(νν) HS cand per event (presel-weighted, factor "HS cand P(R) direct"): R04 20.03 vs 19.52
  (+2.6 %, z +3.64, p 2.7e-4 < 0.05/41 → INDIVIDUAL FAIL), R05 4.713 vs 4.509 (+4.5 %, z +3.00, p 0.0027: pass),
  R06 0.0191 vs 0.0162 (z +0.70). Family coherence z +4.60 → NOT COHERENT (FAIL). Decomposition: unweighted R04 HS cands
  94,537 vs 93,404 (+1.2 %); mean presel weight 0.4107 vs 0.4189 (−2.0 %); events with w > 0: 849/2000. PU-only
  families on 152/200 pu1 + pu2 agree (pu1 R04 −0.7 %, z −0.55; pu2 R04 0.0 %; T1 −0.7 %) → the shift is in the
  hard-scatter (+ weight correlation) part, not the PU chain. STR §4.1 item 5: family failure → regression ticket, no
  tuning; blocks decision point 1. NOT investigated further in this session (see successor section).
- Partial (not final) family outputs saved: outputs/c1_compare_{pu,closure,cprime}_partial_ignatius_2026-11-18.json.
- 2026-11-18 12:21:08 D2 DONE: outputs/V45_RESTRICTED_ignatius_2026-11-18.md (+ outputs/v45r_summary_ignatius.json).
  E2 (ii): PU 46/50, signal 46/50 → FAIL as amended; (i) fit 50/50 + 50/50 → C2-a rests on (i), scan reported failed.
  F0 records found 9 PU / 28 sig, all inside the 3σ band (union = band everywhere).

## STATE FOR A SUCCESSOR — 2026-11-18 12:21 -05
Read first: this log from §2, Rosalie's successor section (2026-11-17 08:15), PHASE2_BRIEF.md, AGENT_RULES.md.
CPU (ledger rebuilt 12:21, dedup campaign+job+attempt): this session 1.49 CPU-h (gen2 1.40, v45r* 0.06,
smregen 0.02) + ≈ 0.15 CPU-h of direct nice-19 analysis runs on landau (stitch, c2_verdicts, c1_compare tests).
Channel (i) to date: p2-a-c1-* 158.6 CPU-h (C1 budget 198; pu1 and cppub still running, projected ≈ 190), p2-a-c2-* 22.5 (81).

DONE (result files in outputs/):
 1. c1-gen: root cause PYTHIA8DATA (no conda activation); rerun p2-a-c1-gen2 12/12; rates family (iv) 5/5 pass,
    coherent → c1_compare_rates_ignatius_2026-11-18.json. queue_slot.sh now prints status + FAILED JOBS warning.
 2. V45_RESTRICTED_ignatius_2026-11-18.md: E2 (ii) FAIL 46/50 + 46/50 → (i) alone (50/50, 50/50), scan reported failed.
 3. C2_VERDICTS_ignatius_2026-11-18.md: C2-b PASS; C2-c PASS as frozen but no power (FLAG).
 4. STITCH_100k_ignatius_2026-11-18.md: ratio 1.0001 ± 0.0252 (z 0.00): no f₂₀₀ bias.
 5. smregen done (p2-a-c1-smregen 2/2, hs_met 2000/2000). SM family (v): **FAIL** (R04 z +3.64, coherence z +4.6) →
    c1_compare_sm_ignatius_2026-11-18.json. C′0 f_pre (ii) 3/3 pass (complete inputs). Closure (i) code works; partial.
RUNNING (leave alone): landau slot A p2-a-c1-pu1 (≈152/200 at 12:20, ≈20 min/job → ≈ 19 Nov 04:30);
 maxwell p2-a-c1-cppua (≈48/50), p2-a-c1-cppub (≈20/75, 2 queues?) → check: ssh -x landau "$R/bin/qv2run status $R/campaigns/<c>.json".
Slot B queue: running and idle (file logs/queue_landau_B_ignatius.txt; log /home/scratch/jdochoa/drivers/queue_landau_B_ignatius.log;
 restart command in §3 above). Append a campaign name to run it.

WHAT REMAINS:
 a. SM family FAIL (STR §4.1 item 5): open a regression ticket (orchestrator decision), investigate without tuning.
    Leads: unweighted HS cands +1.2 %, mean presel weight −2.0 %, weighted +2.6 % → weight–multiplicity covariance;
    PU-only families agree (−0.7 %). Checks to make: (1) per-event P(R04) vs w_presel scatter v1 vs v2 (v1 per-event
    rows are not tracked; only aggregates) ; (2) Pythia version/settings of the HS in c1-sm (meta code hashes vs v1
    s4pu, MPI init file regenerated 17 Nov 09:12 vs v1's); (3) bootstrap width sanity: the s_ln 0.5 % at R04 with 849
    weighted events; (4) rerun of c1-sm with a second seed stream (2,000 events ≈ 14 CPU-h) to see whether it repeats.
 b. When cppua/cppub complete: c1_compare.py --families cprime (C′_PU (iii), 7 entries; dif/gamma/v0 R04-R05, pvpair R02).
 c. When pu1 completes: full run on a worker (≈ 4 min, ≈ 0.6 GB):
    ssh -x landau "cd $QV2 && PYTHONDONTWRITEBYTECODE=1 nice -n 19 envs/tt/.pixi/envs/default/bin/python -B phase2_exploration/src/c1_compare.py"
    (all families; writes outputs/c1_compare.json) + the open signal tier (c1_signal_compare.py open, Rosalie's item 2);
    then 41 = 31 background (this script) + 4 open signal + 6 sealed (separate session). Closure slope partial z +2.83:
    watch it (v2 trend has 3 points, v1 4; v1 refit on R04–R06 gives −0.3594, so not the cause).
 d. outputs/EXPLORATION_i_ignatius_<date>.md (extend Rosalie's): campaign table, D-i-6 (gen2 rerun), the verdicts
    above, rates-width DECISION (experiment_log), C2-c and V4-5 strategy-revision inputs, self-review.
 e. Not started: C1-c container rerun (Rosalie item 7). E 500 stitch at 100k (not asked).
TRAPS (new): the acts env python needs CONDA_PREFIX/PYTHIA8/PYTHIA8_DIR/PYTHIA8DATA exported in runner commands;
 smregen must run on landau (node-local MPI init file); listing key names of signal npz files was refused by the
 permission system — do not retry; signal files are read only by v45_bruteforce sig mode / c1_signal_compare.py.
