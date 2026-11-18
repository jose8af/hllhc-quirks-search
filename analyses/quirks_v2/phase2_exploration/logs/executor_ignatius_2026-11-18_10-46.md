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
