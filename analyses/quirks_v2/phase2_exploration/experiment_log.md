# Experiment log — phase2_exploration (append-only)

## 2026-11-16 12:04 [Sebastian, channel (ii)] node-local MG copy
Attempted `cp -a` and `cp --preserve=mode` of `sw/mg5/MG5_aMC_v2_9_22` (NFS home) to `/home/scratch/jdochoa/mg5/<stamp>` on maxwell: both fail ("preserving permissions … Operation not supported", NFS4 ACLs cannot be set on ext4). Plain `cp -rd` keeps the mode bits under umask 022 and works. Two smoke job ids (smoke, smoke2) ended `failed` in the ledger for this reason (CPU 4.4 s and 1.8 s).

## 2026-11-16 12:04 [Sebastian] R-2 / R-3 retrieval route
cds.cern.ch serves a bot-protection page to WebFetch and curl, so CMS TDRs/notes cannot be fetched from CDS. INSPIRE's API returns the L1-trigger TDR full text and the ATLAS PUB-note PDFs. CERN-CMS-NOTE-2018-006 (CMS HL-LHC object performance) and the DAQ/HLT TDR were not obtainable this way.
DECISION: R-3 parameters taken provisionally from the ATLAS public notes (2013-004, 2013-009, 2016-026; STR §4.7 names the other experiment's reports as the second source) and validation figure ATL-PHYS-PUB-2019-005 Fig. 18.
ALTERNATIVES: keep searching for the CMS note (e.g. arXiv-hosted or conference copies); ask the user to download CDS documents by hand.
CONFIDENCE: MEDIUM. The 2013 parametrisations were made for μ ≤ 140, so using them at 200 is an extrapolation, and no non-Gaussian jet-response tail is given.
FLAG FOR HUMAN: YES (via the orchestrator).
