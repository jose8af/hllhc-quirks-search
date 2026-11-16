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
