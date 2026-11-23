# Experiment log — phase2_exploration (append-only)

## 2026-11-16 12:04 [Sebastian, channel (ii)] node-local MG copy
Attempted `cp -a` and `cp --preserve=mode` of `sw/mg5/MG5_aMC_v2_9_22` (NFS home) to `/home/scratch/jdochoa/mg5/<stamp>` on maxwell: both fail ("preserving permissions … Operation not supported", NFS4 ACLs cannot be set on ext4). Plain `cp -rd` keeps the mode bits under umask 022 and works. Two smoke job ids (smoke, smoke2) ended `failed` in the ledger for this reason (CPU 4.4 s and 1.8 s).

## 2026-11-16 12:04 [Sebastian] R-2 / R-3 retrieval route
cds.cern.ch serves a bot-protection page to WebFetch and curl, so CMS TDRs/notes cannot be fetched from CDS. INSPIRE's API returns the L1-trigger TDR full text and the ATLAS PUB-note PDFs. CERN-CMS-NOTE-2018-006 (CMS HL-LHC object performance) and the DAQ/HLT TDR were not obtainable this way.
DECISION: R-3 parameters taken provisionally from the ATLAS public notes (2013-004, 2013-009, 2016-026; STR §4.7 names the other experiment's reports as the second source) and validation figure ATL-PHYS-PUB-2019-005 Fig. 18.
ALTERNATIVES: keep searching for the CMS note (e.g. arXiv-hosted or conference copies); ask the user to download CDS documents by hand.
CONFIDENCE: MEDIUM. The 2013 parametrisations were made for μ ≤ 140, so using them at 200 is an extrapolation, and no non-Gaussian jet-response tail is given.
FLAG FOR HUMAN: YES (via the orchestrator).

## 2026-11-16 12:14 [Sebastian] R-3: the 2013 ATLAS MET parametrisation disagrees with the μ = 200 validation figure
Phase 1 assumed (STR §4.7) that public Phase-2 parameters for the soft-term resolution exist and that they can be validated against a separate μ = 200 figure. Phase 2 found the following. The only explicit public parametrisations obtainable are ATLAS 2013 notes. 2013-004 §8 gives σ(E_x,y^miss) = (0.40 + 0.09√μ)·√(ΣE_T + 20μ), which is 118–150 GeV at μ = 200 and ΣE_T,hs = 1–4 TeV. 2013-009 gives 64–78 GeV at μ = 140. The ITk-era figure ATL-PHYS-PUB-2019-005 Fig. 18 (μ = 200, tt̄) shows 37–51 GeV over ΣE_T = 1–4.4 TeV, i.e. ×1.5–3 better. Implications: a MET model built on the 2013 formulas would fail its own external validation (B4-b). The alternative is to take the resolution from Fig. 18 itself, but then no independent validation figure remains; this is the stop-and-ask branch of STR §4.7 unless a second μ = 200 figure is found. The CMS note (CMS-NOTE-2018-006) would be the natural second figure. This is a **strategy-revision input** for channel (iii) and the orchestrator. The jet-response tail is also not sourced (retrieval_log #14).
DECISION: none taken by me; reported.
CONFIDENCE: MEDIUM. The figure readings are by eye, and the 2013 formula's ΣE_T convention is read from the text.
FLAG FOR HUMAN: YES.

## 2026-11-16 12:21 [Sebastian] FxFx settings for S2-c
The Pythia side follows `HEPTools/pythia8/share/Pythia8/examples/main164fxfx.cmnd` (Pythia 8.313, local copy). The MG side uses the NLO run_card keys ickkw = 3, jetalgo = 1 (kT), jetradius = 1.0, ptj = μ_Q (`Template/NLO/Cards/run_card.dat` l.113-138).
DECISION: μ_Q = ptj = JetMatching:qCutME = 30 GeV and JetMatching:qCut = 45 GeV. These are v1's MLM xqcut/qCut (produce.py l.51), chosen so the FxFx and MLM samples share merging scales. The example card's 10/20 GeV is a demonstration for Z production.
ALTERNATIVES: qCut = 30 or 60, i.e. the STR merging-scale variations.
CONFIDENCE: MEDIUM. FxFx enters only the f₂₀₀ uncertainty band (S2-c), so this choice moves the band, not the nominal.
FLAG FOR HUMAN: NO (recorded).

## [Tatiana, channel (iii)] 2026-11-16 12:32
- Failed attempt: campaign p2-c-t-hs0s (3 jobs) failed in 1 s each: Pythia could not find its XML data because jobs call the env's python directly and conda activation is skipped. Fix: PYTHIA8DATA (and CONDA_PREFIX, PYTHIA8, PYTHIA8_DIR) exported in the job command. Relaunched as p2-c-t-hs0s2 (failed jobs are never retried by the runner).
- Process error: for about 5 minutes I had 5 concurrent jobs (cap 3 on weekdays). Stopped one driver; later drivers are launched with explicit per-node limits that sum to 3.
- Finding: no-PU hard-scatter event costs 0.127 s (Z(νν)), 0.173 s (W(τν)) against the guessed 45 ms; B1 no-PU event 3.7–5.9 ms against 11.5 ms; Geant4 on the natural spectrum 0.42 ms per firing through the tracker (0.134 ms for the 1–10 GeV gun of FEAS_B).

DECISION: none taken on the pilot definition. Open choices O1–O12 are in logs/executor_tatiana_2026-11-16_11-57.md §5 and its log, reported to the orchestrator before any pilot campaign is submitted.
ALTERNATIVES: listed per choice with a recommendation.
CONFIDENCE: MEDIUM (O1, O3, O5, O12 change numbers that rule 1 of STR §11.7 reads).
FLAG FOR HUMAN: YES

## 2026-11-16 12:58 [Sebastian] install-slot check from a worker does not work
`ssh landau` from maxwell fails ("Could not resolve hostname"). Only einstein resolves the short worker names. The pgrep check inside `queue_maxwell1.sh` therefore passed vacuously. Verified by hand from einstein that no other pixi install was running. Future install checks run from einstein.

## [Rosalie, channel (i)] 2026-11-16 14:43 -05 — deviations and decisions (detail: outputs/EXPLORATION_i_rosalie_2026-11-16_14-43.md §2)
- DECISION D-i-1: pre-merge store kept at N_IP2 ≥ 6 although it measures 33.8 MB/trial (STR planning 3.6–14);
  projection ≈ 270 GB < 400 GB cap. ALTERNATIVES: N_IP2 ≥ 7 ([DT4]). CONFIDENCE: HIGH (orchestrator agreed). FLAG FOR HUMAN: NO.
- DECISION D-i-2: V4-5 exhaustive 0.2 mrad scan computed by band accumulation (|u·n| ≤ 4σ, ≤ 3.4e-4 per hit dropped)
  with a direct-sum check on a sub-grid; global scan ±50° at 5 mrad plus a 10 mrad full half-sphere check on 10 trials.
  ALTERNATIVES: direct sum (86 CPU-h). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO. First attempt (direct sum) failed: timeout
  at 1800 s, p2-a-c2-v45time.
- DECISION D-i-3: probe-row exclusion off; v1 excluded 0 rows at the three C1 points (signal_eff.json) → no effect.
  CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.
- DECISION D-i-4: C2-c T_seed test by regeneration from seeds (v1 g3_rerun pattern), not from dumps. CONFIDENCE: HIGH.
- NOTE D-i-5: all C1 comparisons are between independent samples (lost v1 Stage 2/3; new seed streams), as STR [A2].
- FINDING (S2-c input, sent to channel (ii) via the orchestrator): stitch closure σ_TRG / σ_INC(pT_ME ≥ 100) at
  pT(QQ) > 200 = 1.118 ± 0.06 (z = +2.3) at m 200, 1.055 ± 0.037 (z = +1.5) at m 500, 20k LHE each, FSR off.
- FAILED ATTEMPT: day-0 jobs d0pu2-n1/n2/n4 failed at start (script bug, scratch dir created too late); rerun as
  p2-a-day0-pu2b.

## [Xavier, channel (iii)] 2026-11-16 14:49 pilot code slices
- Failed attempt: first p2x_mbgen changed the module constant p2c_mbgen.POOL_PT at run time to widen the pool; the same constant enters the v1 road rates, which doubled (0.0164 against 0.0080). Found on slice p2-c-px-mb (log of -big), fixed by an own loop with the v1 cuts as fixed numbers; slice redone as p2-c-px-mbb. Lesson: do not patch a constant of an imported module without reading every use of it.
- Failed attempt: p2-c-px-znn (4 jobs) failed at the first event, a local variable shadowed the hadron list in p2x_hs0.extra_summary. Fixed; slice redone as p2-c-px-znnb.
- Process error: I edited p2x_queue.sh while a queue was running it; the queue shell was killed by pid before it read on and restarted. No job affected.

## 2026-11-16 15:29 [Sebastian] FxFx (0–1j MC@NLO) does not fit a 30-minute job
Attempt 1 (fxfx-e500-a, landau, nb_core = 1, node-local process dir): process generation ≈ 80 s; the first launch had completed 17 of 56 tasks of its first queue after 13 min wall, with only 82 s of CPU. Stopped to free the slot. Not yet tried: MG gridpack mode for NLO; increasing nb_core (outside the 1-core-per-job rule); a source of the idle time (MG polling, NFS reads of HEPTools/LHAPDF). Needs an orchestrator decision before a second attempt.

## [Xavier, channel (iii)] 2026-11-16 15:41 A-1: truncation by time does not close the finding; Fatras stops at half a turn
Phase 1 assumed the chain propagates curling particles (v1 "looper" topology; hand-over "the parent's hits up to the vertex"). Phase 2 found: no hit beyond 0.5 turn of any particle (B1 parents: p2-c-px-a1d; Z(νν) slice events: 231 of 3.94×10⁶ hits, p2-c-px-a1e). Implications: DIF-C and NI-C cannot be given their parent hits by any truncation (40–45 % of the Geant4 pre-vertex crossings missing with the time cut, p2-c-px-val2); every sample lacks the later arcs of soft particles. Detail and options: outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md.
DECISION: pilot launch held and reported instead of executing the go given before this was known.
ALTERNATIVES: launch and report.
CONFIDENCE: MEDIUM
FLAG FOR HUMAN: YES

## 2026-11-16 16:34 [Viktor] T1 toy cost: remedies and projection (outputs/TOY_COST_viktor_2026-11-16_16-33.md)
Tried (campaigns p2-c-toy-*, schrodinger, 2.58 CPU-h): numpy+scipy baseline reproduced (487 / 8,814 / 67,780 s per
1000+1000 toys at 31 / 60 / 100 par; ×18 from 31 to 60 as Tatiana's ×17). Did not work: minuit on numpy (×0.21–0.33)
and on jax (×0.5) — pyhf runs hesse() in every fit; fixing negligible λ (≤ 6 %, and q̃ changes). Worked: jax autodiff
gradients with scipy SLSQP (×20–36), merged channel layout and stitched POI (identical q̃, ×1.1–1.2), warm start from
the previous toy (×2.4 more, and q̃ equal to tol = 1e-10 minima on all 200 toys at 100 par, where pyhf's default
start misses by up to 0.033). Best: 30.5 / 168 / 385 / 817 s per unit at 31 / 60 / 80 / 100 par, 0 failed fits in
25,180 toys. Programme (1,006 units, STR l.1710–1719, 1733): 47 / 108 / 228 CPU-h at 60 / 80 / 100 par vs 183.
Found: CLs ties (discrete counts) make "q ≥ q_obs" sensitive to 1e-7 minimiser noise; count ties within 1e-5.
DECISION: recommend jax + scipy + merged + stitch + start=prev for every T1 toy.
ALTERNATIVES: jax + scipy + merged + stitch with chain start (×1.4 slower at 100 par, free fits exact, fixed fits
within 0.010); procedural options O1 (shared b-only fits, ×0.78) and O2 (two-stage toys, ×0.4–0.5) not applied.
CONFIDENCE: HIGH on the measured unit costs and correctness on the synthetic workspace; MEDIUM on the projection
(synthetic structure, node and load factors: factor ≈ 1.6 either way; v2 parameter count unknown).
FLAG FOR HUMAN: YES — at 100 parameters the central projection is 228 CPU-h (> 183); options O1/O2 or a smaller
workspace would be needed there.

### 2026-11-16 18:15 channel (iii) Albert — first validation of the B1 chain at full job size: the "validated" β cut leaves a residue
What was tried: `p2x_validate.py` on Xavier's p2-c-px-g4 (vertex files) and p2-c-px-b1 (radius cut), which had never been through a validation job (campaign p2-c-pa-val0), then a diagnostic of the failing check (p2-c-pa-dg1, src/p2a_diag_early.py).
What worked: all vertex files; all first-arc streams at 2,000 events; reruns identical.
What did not: "no product hit before the vertex time" fails in 25,000-event files (nix-big 6 hits in 3 events, nic-big 1 hit). (1) 5 hits are correct hits of secondaries Geant4 made along the parent's path before the vertex (stored as products with their own earlier production point): the check was too coarse; it now compares with the product's own production time. (2) 2 hits of one event are a slow heavy fragment (β = 0.134 > cut 0.1) with Fatras hits at t = −32 ns: the pathology the β cut was made for, at ≈ 4×10⁻⁵ per NI-X event (1 event).
DECISION: keep β_min = 0.1 as the campaign default for now (it is the variant the addendum calls validated), record `n_early_prod` per event in every B1 file, measure the rate on ≈ 1.5×10⁵ NI events and scan β_min = 0.15 / 0.2 / 0.3 on the same events (p2-c-pa-b1-nix-b*).
ALTERNATIVES: raise the cut now without a measurement; filter early hits in the job (new hand-over code).
CONFIDENCE: MEDIUM — one event; the scan decides.
FLAG FOR HUMAN: YES — whether a known rate of flagged events is acceptable or the cut moves (addendum P6 names 0.1).

### 2026-11-16 20:27 channel (iii) Albert — launch test: relative output directory
Tried: `p2a_b1_campaigns.py b1 --outdir tools/runner/examples/p2x/launch_test_b1` (relative). The LAUNCH script then carried relative campaign paths and the queue on the worker died at its first status call (no job started). Fixed: the generator resolves the directory to an absolute path; test repeated and passed on one lane (p2-c-pa-lt-*, 33 of 33 jobs).

### 2026-11-17 08:43 -0500 channel (iii) Flora — T1-b: procedure fixed, set-up checks, fit accuracy
What was tried: the T1 hybrid-toy procedure in v1 mode on pyhf 0.7.6 + jax + SLSQP (code src/p2f_t1.py), with an
exact one-dimensional profile as accuracy reference; campaigns p2-c-t1f-smoke1, -setup, -setup2 (175 CPU-s).
What worked: asymptotic limit (4-unit grid interpolation 828.667 as Tatiana's 828.668; root 828.7069 = v1's own
828.7067); Viktor's CLs 0.1372 reproduced with his script; closed-form start values + SLSQP tol 1e-10 on jax: 0 failed
or inaccurate fits in 1,800 toys, q̃ equal to the exact profile to 1.5e-7.
What did not: (1) pyhf's own asymptotic hypotest with default starts returns CLs = 0.0 without raising (true 0.06–0.31);
(2) SLSQP's default tolerance stops 4 of 600 toys above the minimum (by 0.07–3.8 in q̃) and reports success: curvatures
of 1e6 beside 1–40 cut the first line search; (3) the numpy backend at tol 1e-10 raises in 0.8 % of toys.
DECISION: production with jax, closed-form starts, tol = 1e-10; failed-fit rule and 2 % limit unchanged; the change of
tolerance was made before any production toy, by a selection rule on fit-quality counters only.
ALTERNATIVES: start the pyhf fits at the exact profile solution (rejected: the reference would no longer be an
independent check); Newton step on the SR-T start (no gain); minuit (Viktor: slower; Tatiana: 3 % failed).
CONFIDENCE: HIGH on the fit accuracy (every toy is checked against the exact profile).
FLAG FOR HUMAN: NO

## 2026-11-17 channel (ii), executor Edgar
- P1 floor diagnostic: v1's spec "44 bits (u′ ≈ 64u)" is inconsistent (44-bit significand → 512u; 64u ↔ 47 bits). Round-to-nearest at 44 bits behaves like truncation (test 2 fails either way); at 47 bits the nominal Δc(20) pattern reappears at k = 2.5 (KS p 0.53 / 0.47, 40 events). Diagnostic only; the pre-declared reading is unchanged (p2-b-p1-rn, outputs/p1/p1_rn_eval.json).
- f₂₀₀ shift errors: the re-showers share the LHE events; paired errors from matching events on (chunk, LHE quirk momenta) are ≈ 25 % smaller than the unpaired ones (partial-data test). Unpaired kept in the JSON.
  DECISION: f₂₀₀ band = quadrature of 7-point scale, CT18 PDF converted 90→68 % by Gaussian Φ⁻¹(0.95), merging envelope (qCut 30/60), tune (Monash, symmetrised) and MC stat; FSR-off shift quoted outside the band; no FxFx term.
  ALTERNATIVES: PDF at 90 % as given (wider); tune one-sided; stat left out of the nuisance (it is MC precision, could go into a separate MC-stat term).
  CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES (conventions of a nuisance entering T1).
- S2-e: the L1 TDR curve is sourced (Table 4.1 p. 210, Fig. 3.125 p. 188), but no uncertainty is stated. DECISION: none taken. Options (a) statistical bars, (b) pre-declared wide nuisance, (c) raise the threshold to 275–300 GeV are left to the orchestrator before A. FLAG FOR HUMAN: YES.
- S2-b resummed: the WG tables have no NLO column; (NLO+NLL)/NLO is taken from self-run Resummino 3.1.2 (decoupled ~e_R, both PDF sets) and applied to E. CONFIDENCE: MEDIUM (scalar → fermion, scale m vs H_T/2). FLAG FOR HUMAN: YES.
- Retrievals R-7, R-12, R-14–R-18 done from INSPIRE public files and arXiv (retrieval_log #24–#31): resolution, budget and occupancy values found; no uncertainties for hit resolution, hit efficiency or material → B6-d "no nuisance" branch.

### 2026-11-17 09:36 -0500 channel (iii) Flora — T1-b verdict: FAIL as frozen; the toy recipe, not the likelihood
What was tried: ten replicas of the frozen T1 toy procedure in v1 mode (p2-c-t1f-prod), read by the rule fixed
before any toy; diagnostics p2-c-t1f-post; trap reproduction p2-c-t1f-guard. 0.51 CPU-h in all.
What worked: fits (0 failed in 160,000 toys, q̃ = exact profile to 1.2e-5); asymptotic limit = v1's to 2e-4; v1's
statistic reproduces 789.7438 exactly with v1's seed.
What did not: the limit of the recipe: 704–963 over replicas (sd 114), pooled 902.0 ± 31.9, outside 789.7 ± 10 %.
The b-only median sits on a jump of q̃ at μ_a by construction; CLs at μ_a is 0 or 0.26–0.73, and 0 at the next grid
point; the ln interpolation over a 25–35 % step lands at neither crossing. Even 2e5 exact toys give a non-monotone
CLs between 810 and 833. v1's own number scatters by 38 between seeds. My written expectation (NOT RESOLVED) was
wrong on the high branch.
DECISION: verdict recorded as FAIL, no rewording applied, no extra toys (rule fixed in advance).
ALTERNATIVES: refined bracket (mean 844, sd 73, 7 of 10 inside), linear CLs, other empty-tail values: reported as
diagnostics without verdict; proposal for the wording in the result file §7.
CONFIDENCE: HIGH that the likelihood is right and that the recipe is unstable here; MEDIUM on the FAIL/STRADDLES
label itself (margin 1.5 units against a bootstrap error of 32).
FLAG FOR HUMAN: YES — wording of T1-b, and the grid/empty-tail rule of the toy procedure used by T1-i.

### 2026-11-18 10:55 -0500 channel (iii) Hedda — per-stream validation of the B1 pilot (P7): campaign prepared, not launched
What was done: `tools/runner/examples/p2x/b1_val/p2-c-pilot-val-s1.json`, 8 jobs (dif, difc, nix, nic, ni22, ni30,
ni61, lowpt), each `p2x_validate.py` on two done chain files; ≈ 0.025 CPU-h, ≤ ≈ 0.6 GB [E from p2-c-pa-val1-b1].
DECISION: two files per stream (jobs 0000 and 0001 of the first chain campaign), not one; outputs under the data
prefix `p2c/pilot_validation`, not under `pilot`; hs left for a second campaign when its chain campaign has run.
ALTERNATIVES: one file per stream (half the cost, but then the validator's "another chunk gives another content
hash" check has nothing to compare; with two files it runs in production for the first time); every file of the
first campaign (≈ 0.5 CPU-h; more than "one validated job"); prefix `pilot` (verdict files next to the pilot data).
CONFIDENCE: HIGH (cost is 90 CPU-s; nothing of the pilot is written or changed).
FLAG FOR HUMAN: NO.
Not done: `qv2run ssh launch --dry-run` (takes the driver lock and writes driver state in the ledger: left to the launch).

## 2026-11-18 10:48:06 — Ignatius (channel (i)): p2-a-c1-gen failure, root cause and rerun
All 12 jobs of p2-a-c1-gen failed on 2026-11-17 09:12 at Pythia init ("unmatched version numbers: in code 8.312 but
in XML 0.000"). Cause: the command calls $QV2/acts/.pixi/envs/default/bin/python directly; the conda activation
(activate-pythia8.sh, which sets PYTHIA8DATA) is not run, so Pythia finds no settings XML. c1-sm succeeded because it
runs through envs/tt + c1_pu_job.py. Fix: rerun as p2-a-c1-gen2 (new ids c1gen2-*) with the four Pythia variables
exported in the command (as channel (iii)'s p2c_campaigns.py:20); no code change. The failure went unnoticed for a day
because queue_slot.sh logged the driver's exit code (0) only; it now prints the campaign status and a FAILED JOBS
warning. Lesson: check `qv2run status` (failed count) after every campaign, not the driver exit code.

### 2026-11-18 10:55 -0500 channel (iii) Hedda — per-stream validation of the B1 pilot: result
What worked: p2-c-pilot-val-s1 (8 jobs, 90.2 CPU-s): 16 of 16 files pass `hard_except_early_product_hits`; every
hard item except the early-product-hit one is true in all; other chunk → other hash in 8 of 8 streams.
What did not: strict `hard` fails in 4 files (nix, ni30, ni61, lowpt; 18 hits in 8 events of 469,318) on the known
slow-fragment residue; ni30, ni61 and lowpt show it for the first time. All 8 events are in the 0001 files, none in
the 0000 files: not explained, not investigated (needs a worker slot; `n_early_prod` of all files would settle it).
DECISION: streams reported as validated under the reading fixed on 17 Nov; the 0000 / 0001 pattern reported as an
open observation, without a cause; p2-c-pilot-val-s2 (hs, its pool and vertex files) written with `after` = c0-hs.
ALTERNATIVES: withhold the verdict of the four streams until the pattern is understood; open the event files on
einstein (refused by the rules: nothing heavy there).
CONFIDENCE: HIGH on the verdicts as defined; LOW on whether the pattern is chance (0.8 % by events, 12.5 % by streams).
FLAG FOR HUMAN: YES — the pilot-wide count of flagged events (≈ 3×10² expected [E] against "order 10²") and the pattern.

## 2026-11-18 10:55:38 — Ignatius: C2-c family statistic and the degenerate outcome
DECISION: the "per-trial pass fraction of each rung family" (STR §4.2) is computed as the fraction of trials passing
at least one rung of the family (counting R04; width R05, R06; chi2 R09–R11; 2S R12–R14), with v1's per-trial pass
rule (n_grp > 0, n_pass where n_grp < 0) and a paired event bootstrap; the v1 per-rung table (pass_frac, mean_grp) is
reported as a diagnostic.
ALTERNATIVES: one test per rung (would be 14×2 tests, not the frozen 8); the family's tightest populated rung (R06 for
width: z +1.38 / +1.00, same conclusion); v1's conservative mean_grp reading (z +28 at R04 ρ=1 for +0.32 %: would FAIL a
|z| < 2.73 rule, but it is not the frozen metric).
CONFIDENCE: MEDIUM — the verdict PASS is robust to the family reading (R04/R05 saturated, R07–R14 empty in every
reading), but the test has no power, and the mean-count reading shows a small significant shift.
FLAG FOR HUMAN: YES — C2-c as frozen cannot fail at PU 200; proposed wording in outputs/C2_VERDICTS_ignatius_2026-11-18.md.

### 2026-11-18 11:02 -0500 channel (iii) Hedda — pilot-wide count of flagged early-product-hit events
p2-c-pilot-val-eph (7.8 CPU-s): 318 flagged events (524 hits) in 17.2×10⁶ events of 546 chain files; none in dif and
difc (8×10⁶), all in nuclear-interaction classes (nix 212, nic 59, ni22 10, ni30 15, ni61 18, lowpt 4). The
"all in files 0001" pattern of the first validation was chance: even / odd chunk index 157 / 161, per-file counts
Poisson. My earlier flag on the pattern is withdrawn; the total is three times B1_READY's "order 10²" (rate
1.85×10⁻⁵ against 0.9×10⁻⁵ estimated from 4 events). FLAG FOR HUMAN: information only.

## 2026-11-18 11:01:59 — Ignatius: C1 rates family (iv) widths
DECISION: v1 recorded no statistical width for the C′ rates (normalisation.json cprime_rates.<t>.sigma_ln = 0) and v2's
gen_d123 'nt' output (v1 code, unchanged) stores only aggregates (sum_w, sum_w2, rates), so no event bootstrap is
possible. Width of ln(rate) = sqrt(D r / N_eff)/r with N_eff = (Σw)²/Σw² of the process giving the maximum; D = 1 (HS
DIF; plus the min-bias DIF term with gen_d123's own rel 1/√objects), D = 2 for γ (photons come in π⁰ pairs), D = 2√(2r)+1
for PV pairs (pairs of a Poisson multiplicity with mean √(2r)). The same width is assumed for v1 (same generator, same
sizes, same code). N_trig and N_trig(Z) use the recorded rel_stat of v1 and the same formula on v2.
ALTERNATIVES: modify a copy of gen_d123 to store per-event object counts and rerun (≈1 CPU-h, a change of the C1 code
path); treat the rates as untestable (no width); use Poisson D = 1 for all (underestimates PV-pair and γ widths).
CONFIDENCE: LOW–MEDIUM — the dispersion factors are a model (ESTIMATE); a failure of a rates entry must first be
checked against this width before it is read as a port problem.
FLAG FOR HUMAN: YES (if any rates entry fails or sits near the Bonferroni line).

## 2026-11-18 12:21:08 — Ignatius: V4-5 restricted scan (amendment E2 (ii)) — FAIL 46/50 per half
Restricted hit set = 3σ band of the F0 plane ∪ F0's stored hit record (record ⊂ band in all 37 events where stored).
8 disagreements of 1.1–3.6 mrad, all with F0 vs fit ≤ 0.85 mrad: the score maximum is not the least-squares plane at
the 0.2 mrad grid scale. Reported as failed per the amendment's wording. No re-definition attempted (would be a third
post-hoc criterion). FLAG FOR HUMAN: YES (decision point 1).

## 2026-11-18 12:36 — Lisbet (fix agent): clustered widths in c1_compare.py (SM ticket §3; advisor ruling Kestrel)
Implemented as scoped; tests on synthetic clustered data only (test_c1_compare.py, 11/11 pass on landau). Judgment calls:

DECISION: family coherence keeps the frozen form (inverse-variance mean with the DIAGONAL weights) and only its variance
  uses the full joint-replica covariance, w'Σw/(Σw)²; not a GLS mean.
ALTERNATIVES: GLS mean with Σ⁻¹ weights (minimum variance, but changes the estimator named in STR §4.1 item 2).
CONFIDENCE: HIGH (smallest change that makes the error correct). FLAG FOR HUMAN: NO

DECISION: v1 covariance between nested rungs := D1 ρ_v2 D1 (v1 widths of the primary rule, correlation taken from the v2
  replicas); v1 per-event counts are lost. With v1 width 0 only the v2 covariance enters.
ALTERNATIVES: v1 rungs independent (understates the family error, the defect being fixed).
CONFIDENCE: MEDIUM (ESTIMATE; same chain, same event structure). FLAG FOR HUMAN: NO (the v1 = 0 variant bounds it)

DECISION: global χ²₄₁ — the clustered families (sm, cppu) enter as dᵀΣ⁻¹d with Σ from the joint replicas (same number of
  dof as entries), instead of Σz² over correlated entries; sum_z2_naive also reported.
ALTERNATIVES: keep Σz² and take its null distribution from the replicas (threshold no longer χ²₄₁).
CONFIDENCE: HIGH. FLAG FOR HUMAN: NO

DECISION: C′_PU 2σ power for the frozen N < 10 binomial entries stated as ESTIMATE expm1(2√(1/N1 + 1/N2)) (Poisson,
  unclustered, labelled); a C′_PU entry whose v2 direct factor comes from C′0 (low-gun branch) is NOT TESTABLE here.
CONFIDENCE: MEDIUM. FLAG FOR HUMAN: NO

OPEN (not in scope, flagged): pu1/pu2 and clos family coherence still treat the nested rungs R04–R06 as independent
  (their per-entry widths are event-bootstrap and correct; boot_mean already has joint replicas). Same correlation issue
  as the SM coherence, opposite of the ticket's scope. FLAG FOR HUMAN: YES (orchestrator decides whether to extend).

## 2026-11-18 12:40 — Lisbet: SM family rerun with clustered widths (commit 54610b6) — amendment E4, pending approval
Frozen script FAIL reproduced and kept on record. Corrected: 3/3 pass and coherent with both v1-width choices
(outputs/SM_FIX_lisbet_2026-11-18.md). Block χ² 1.53 (primary) exceeds Σz² 0.71 because R04/R05 are 98 % correlated
but differ in ln ratio by 0.018; expected. C′_PU not run (inputs incomplete).

## 2026-11-19 11:17 — Vidar: C1-c container recipe; build refused by the permission system
DECISION: container recipe on docker (the only runtime on the workers) from the local `ubuntu@sha256:e9569c25…`
(22.04.3) with --pull=never, since the pinned `2198e4c6…` is not in any worker's docker store.
ALTERNATIVES: pull 2198e4c6 from Docker Hub (rate-limit rule); Argo pod with runtime pixi install (no image recipe).
CONFIDENCE: medium. FLAG FOR HUMAN: yes — base-image deviation; docker build refused by the permission system
(11:17), not worked around; frozen "identical hash" criterion unattainable (timestamps/hostname in meta_json).
C1-c NOT TESTED. Artifact outputs/C1C_CONTAINER_vidar_2026-11-19.md; recipe commit 26f4abe.

## 2026-11-19 11:26 -0500 — Ulrika (D2 "later arcs restored"): construction decisions
DECISION: finder input of the varied arm = the nominal job's own pre-top-up hits (S6 dumps of c1pu1-0000..0029) +
the injected measurements of the varied chain; top-up drawn as nominal on nominal hits, last n_inj(layer) crossings
dropped. Nominal partner = the existing c1pu1 outputs if a control job (injection off) reproduces them bit for bit.
ALTERNATIVES: use the varied chain's own (re-smeared) hits for the nominal part (breaks the pairing: one digitisation
stream per event, every later hit re-smeared); re-run a nominal arm on the same chain (+ ≈ 9 CPU-h, same problem).
CONFIDENCE: high for the pairing; the CKF flags of nominal hits changed by the injected hits (smoke: 224 of 48,807
per event, 0.46 %) are not propagated (measured, reported).
FLAG FOR HUMAN: the injection rule (turn > 0.5 AND later than the last Fatras SimHit + 0.005 ns) combines the frozen
wording and the validated option-(a) seam; Geant4 crossings before half a turn later than the last Fatras SimHit
(smoke: ≈ 3,090 per event, all surfaces) are not injected (plan §7 item 1).
Smoke p2-c-d2s-chain [V]: 2 events, 17,880 injected written measurements per event (= injected SimHits on written
surfaces), nominal part identical to the dumps (truth positions, order), V4-1 ok, 85 s for 2 events incl. geometry.

## 2026-11-19 14:26 -0500 — Sune (channel (ii) successor): FxFx first launch
- Runner: per-job timeout_exception (SSH only, cap 7200 s, recorded in the started marker), commit 7c31c9e, tests 23/23 on maxwell.
- p2-b-s2-fxfx on maxwell, one at a time: fxfx-e500-grids done (5,383 s wall, 5,347 CPU-s; sigma 4.695e-3 +- 1.2e-5 pb;
  procdir published). fxfx-e1500-grids FAILED: timeout at 6,000 s in MINT step 1 (35/56 channels by 13:59, one channel
  > 24 min). S2-c FxFx piece NOT MET; f200^FxFx not computed at either mass. Details and options:
  outputs/FXFX_sune_2026-11-19.md.
- 2026-11-19 14:30 -0500 Sune follow-up: E 500 FxFx shower blocked. MG5aMC_PY8_interface segfaults in its DJR histograms
  (njetNow > JetMatching:nJetMax = 1). n_lhe counting bug fixed in s2_job.py. E1500: 48/56 step-1 channels done at the
  kill, ≈ 6,900 s needed (ESTIMATE). Details: outputs/FXFX_sune_2026-11-19.md §6.

## 2026-11-19 15:48 -0500 — Eskil: C′_PU attribution, v1 link rule vs frozen j ≥ n/2 (STR l.753-754)
Result (outputs/CPU_ATTRIB_eskil_2026-11-19.md): at R05, frozen/v1 = DIF 0/141, γ 10/174 (one source event), V⁰ 26/612; at R06 γ 1/11, V⁰ 1/11; PV pair 0/4 at R04. No candidate passes j ≥ 4 without v1's rule.
DECISION: j uses the stored merged-hit INT (largest-dE member), as Björn did for the SM. ALTERNATIVES: pre-merge membership (not stored). CONFIDENCE: high (own-INT hits ≈ v1 core links within 2 %; DIF max_cross = 1 makes it label-independent).
FLAG FOR HUMAN: Gate A's conversion range does not carry over as a term size (ρ_γ ≈ 0.06, 95 % UL ≈ 0.22; most v1 candidates become mixed or pure pile-up); DIF R06 test count 31 and H(R06) ≥ 0.004 void; NI 92/120/378 not measured (NI C′_PU run ≈ 7 CPU-h needs approval).
- 2026-11-19 15:54 -0500 Sune: E500 FxFx f200 = 0.10519 ± 0.00169 (nominal 0.10410, band +2.9/-2.5 %): inside, band unchanged. E1500 not run (user decision). outputs/FXFX_sune_2026-11-19.md §7.
- 2026-11-19 17:19 -0500 Sune DECISION: rerun the user-approved E1500 grid job once as fxfx-e1500-grids3. grids2 failed at start (92 s wall,
  MG "AlreadyRunning": stale RunWeb left by the 14:23 kill; no MINT work done); s2_job then wrongly stamped READY (removed).
  The approved single 2-h computation has not run; "no retry" is read as applying to a timeout. ALTERNATIVES: record
  E1500 NOT DONE now. CONFIDENCE: MEDIUM. FLAG FOR HUMAN: yes (orchestrator to confirm this reading).

## 2026-11-23 15:14 -0500 — Ingvild (successor of Cecilie): rule-1 validation (a2), (c) read
Result (outputs/RULE1_VALID_ingvild_2026-11-23.md): (c) subset-pass m_Z at R08 = 1,501 (S) / 1,474 (F), B1/HS/lowpt 0; acceptance 0 violations of 22,790; B50(R09) 63,170 (S) / 62,037 (F), R08 63,246-63,294; with = without flagged events. (a) NO POWER as planned; (a2) PASS (D2 = 0, 350 events). (d) PASS (Cecilie). "Above 300" stands. CPU 4.93 h (markers).
FAILED ATTEMPT: 36 nic/nix jobs of p2-c-r1v-s2a/b died at start: numba cache index of subset_road cannot be saved after 51 entries (each job adds one; ReferenceError "underlying object has vanished").
DECISION: rerun the 36 as p2-c-r1v-s3a/b, same script and arguments, new NUMBA_CACHE_DIR; summary glob s2[ab] -> s[23][ab]. ALTERNATIVES: delete the cache index and edit markers to retry in place (touches the ledger); drop cache=True (changes the script hash mid-campaign). CONFIDENCE: high (script sha256 identical in all 139 outputs; file-count and event-total guards pass).
FLAG FOR HUMAN: p2w_subset.py is not reviewed by a second agent: under advisor ruling (ii) the finder count (253 -> 10,777) remains the stand-in lower bound until it is; the verdict "above" is the same.
