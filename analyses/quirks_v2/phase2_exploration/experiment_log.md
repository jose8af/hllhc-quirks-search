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
