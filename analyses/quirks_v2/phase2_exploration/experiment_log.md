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
