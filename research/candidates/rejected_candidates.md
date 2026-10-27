# REJECTED_CANDIDATES (Gate 2 triage)

Rejection requires a positive covering reference or a physical showstopper. Provenance: scout seeds in `candidates/raw_seeds.json`; full triage in `reviews/triage/gate2_batch*.json`. Status: triage-level (sonnet); rejections of high-profile items should still be spot-checked if the user disagrees.


## C010 — Compressed / inelastic-DM soft displaced leptons and tracks
- Status label: well-covered
- Confidence: medium
- Reason: Positive evidence of broad coverage by 8+ CMS/ATLAS results over iDM, higgsino, VBF-compressed variants, plus HL-LHC projections. If re-raised, narrow to small-splitting (1-5%) iDM.
- Covering/closest searches:
  - arXiv:2305.11649 (CMS): iDM: two displaced muons + MET, 138 fb-1, mass splitting scenarios (Delta/m1 = 0.1 and 0.4 shown) [abstract; Fig. (text lines 223,452)]
  - recid3186741 (CMS): iDM with low-momentum displaced electrons + MET, 138 fb-1 [abstract]
  - arXiv:2511.20042 (ATLAS): Compressed higgsinos with low-momentum tracks, splittings 0.3-1 GeV and further range [abstract]
  - arXiv:2401.14046 (ATLAS): Nearly degenerate higgsinos, mildly displaced soft tracks [abstract]

## C020 — Electroweak-charged dark mesons (5-plet)
- Status label: indirectly-covered
- Confidence: medium
- Reason: Model-specific interpretation of existing signatures (authors recast them themselves); no new observable. Not a literal experimental result for the model, hence status indirectly-covered.
- Covering/closest searches:
  - arXiv:2201.02472 (ATLAS): disappearing track (recast in 2507.13430 Sec.3.1, bound ~1.2 TeV) [2507.13430 abstract, Sec.3.1]
  - arXiv:2507.13430 ((theory)): recasts ATLAS/CMS diphoton, ZZ, WW semileptonic, same-sign W searches for eta_5; Fig.7-8 contain existing and projected resonance constraints [Sec.3.2, Figs.7-8]

## C024 — Top/gluon-philic ALP and heavy (pseudo)scalar tt lineshape/interference
- Status label: well-covered
- Confidence: medium
- Reason: Positive evidence of experiment-level interference-aware search over 365-1000 GeV; remaining radion-specific details are interpretation only.
- Covering/closest searches:
  - arXiv:2507.05119 (CMS): A/H->tt, 365-1000 GeV, widths 0.5-25%, interference with SM tt included (peak-dip), 1/2-lepton, 138/fb; reports excess near threshold [abstract; text lines 45,85,337]
  - arXiv:2304.01678 (ATLAS): top-philic heavy resonance 1-3.2 TeV in ttbar/tttt [abstract]
  - arXiv:2608.10148 (CMS): four-top resonance, vector/scalar/pseudoscalar top-only boson [abstract]
  - arXiv:2505.05300 (CMS): DM + t/tt with MET (handle on ALP-top coupling per 2303.17634) [abstract]

## C028 — ~1 cm lifetime blind spot (H->phi phi->4j, L1 track trigger)
- Status label: well-covered
- Confidence: medium
- Reason: Positive evidence that CMS 2409.10806 covers c*tau ~1 cm for H->SS->4b/4d with ggF triggers, with limits stated in conclusions.
- Covering/closest searches:
  - arXiv:2409.10806 (CMS): H->SS (ggF), S->bb/dd/tautau, mS 15-55 GeV, HLT displaced-jet triggers; B(H->SS)>1% excluded for mS>40 GeV and c*tau 1.5-370 mm (b b) / 1.3-380 mm (d d) [Conclusions; Fig.6; abstract]
  - arXiv:2107.06092 (ATLAS): ZH, H->aa->4b, displaced vertices in ID; sensitivity ~1 mm to 0.1 m per its Introduction (also cites CMS 1 mm-1 m) [Introduction lines ~118-124; abstract]
  - arXiv:2203.01009 (ATLAS): CalRatio displaced hadronic jets, 139/fb, c*tau from 20 mm to 10 m for BR>10% [abstract]

## C033 — Main-detector vs far-detector complementarity (GeV LLPs)
- Status label: indirectly-covered
- Confidence: medium
- Reason: Fails Q1: a detector-comparison framing, not a collider observable CMS/ATLAS can measure; GeV-scale LLP main-detector coverage exists (2409.10806, 2403.15332, 2606.25840). Fold into C027.
- Covering/closest searches:
  - arXiv:2409.10806 (CMS): Light LLP displaced jets, mS 15-55 GeV [abstract]
  - arXiv:2403.15332 (ATLAS): Light LLPs 5-55 GeV decaying hadronically in ID, 140/fb [abstract]
  - arXiv:2606.25840 (CMS): Scouting low-mass displaced dimuon [abstract]
  - arXiv:2609.00152 ((proposal, not CMS/ATLAS)): GRENDEL far detector proposal; motivation sentence only [abstract]

## C034 — R-hadrons, gluinonium, mini-split displaced/stopped signatures
- Status label: well-covered
- Confidence: medium
- Reason: Charge-flip and stopped R-hadron modelling already treated in CMS 2410.09164 and ATLAS 2104.03050/2502.06694; remaining gluinonium piece not supported by evidence of HL-LHC reach.
- Covering/closest searches:
  - arXiv:2410.09164 (CMS): HSCP dE/dx, 101/fb, gluinos/stops/staus, includes charge-suppressed R-hadron model [abstract; Sec. around line 338 (charge-suppressed model)]
  - arXiv:2502.06694 (ATLAS): dE/dx + ToF HSCP, 140/fb, 200 GeV-3 TeV, lifetimes >3 ns [abstract]
  - arXiv:2104.03050 (ATLAS): Stopped gluino R-hadrons, 579 h live time, m up to 1.4 TeV for tau 1e-5-1e3 s; robust against charge flips [abstract; Sec.1 lines ~51-54]
  - arXiv:2601.20063 (CMS): HSCP with L1 trigger scouting, 13.6 TeV [abstract]

## C035 — RPV with intermediate-lifetime displaced LSP
- Status label: well-covered
- Confidence: medium
- Reason: Broad framing is directly covered by ATLAS 2603.15007 (+CMS DV/displaced-lepton searches); no specific uncovered signature remains in this candidate.
- Covering/closest searches:
  - arXiv:2603.15007 (ATLAS): Reinterpretation of 13 ATLAS SUSY searches over variable RPV coupling (prompt to long-lived): gluino (Gqq+LQD, Gqq+UDD, Gtt), stop, stau, higgsino/EW; abstract gives gluino limits 1.0-1.7 TeV at low/intermediate coupling vs 1.8 TeV prompt [abstract; Sec. 2 models]
  - arXiv:2402.15804 (CMS): DV + MET, c*tau 0.1-1000 mm, 137/fb [abstract]
  - arXiv:2603.12051 (ATLAS): DV + MET incl. fuzzy vertexing, 137/fb [abstract]
  - arXiv:2601.05664 (ATLAS): OS displaced lepton-pair DV with RPV neutralino benchmarks, c*tau 1-1e4 mm [abstract]

## C067 — Mixed-decay third-gen LQ (b nu t tau)
- Status label: well-covered
- Confidence: high
- Reason: Scout seed's premise ('no search for the mixed b nu t tau final state') is contradicted by CMS 2012.04178 which names this exact signature. S3/mixed t-mu / b-nu cases are covered by ATLAS 2401.11928 and CMS 3159754. Seed claims came from 2018-2020 theory text only.
- Covering/closest searches:
  - arXiv:2012.04178 (CMS): Single + pair production of LQ -> t tau or b nu (equal couplings, i.e. BR~50%): explicitly probes the 't tau nu b' signature; abstract states these signatures had not previously been explored in a dedicated search [Abstract; Sec. 1 line ~100 ('tau nu(b) signatures analyzed for the first time'); Sec. 2 coupling assumption]
  - arXiv:2401.11928 (ATLAS): Statistical combination of pair-produced LQ searches over all decays to 3rd-gen quarks + charged/neutral leptons of any generation (BR scan) [Abstract]
  - recid:3159754 (CMS): 13.6 TeV, 220 fb-1: LQ -> t l or b nu, BR depends on coupling type, 1st/2nd-gen leptons [Abstract]
  - arXiv:2306.17642 (ATLAS): LQ pair -> t e / t mu multilepton [Abstract]

## C070 — Charm- and strange-flavoured leptoquarks
- Status label: well-covered
- Confidence: medium
- Reason: Scout statement 'ATLAS has a c-tag + MET search; l+c-tag resonance not seen' is true only for single/resonant; pair-production l+c-tag is in ATLAS 2006.05872 and LQ->c nu in ATLAS 2410.17824. Remaining gap is a duplicate of C066 sub-direction. Strange tagging is a detector limitation, not a search gap.
- Covering/closest searches:
  - arXiv:2006.05872 (ATLAS): Pair LQ -> e/mu + quark with c-tag and b-tag categories (signal regions 'LQLQ -> c e c e / c mu c mu c-tag') [Abstract ('including jets identified as arising from c- or b-quarks'); control/SR tables]
  - arXiv:2410.17824 (ATLAS): c-tagged jets + MET with LQ -> c nu interpretation (scalar LQ excluded up to 0.9 TeV, vector 1.5 TeV per review arXiv:2505.08738 Sec. 3.1) [Abstract; arXiv:2505.08738 Sec. 3.1]
  - arXiv:2303.09444 (ATLAS): tau tau + jets LQ coupling to charm or lighter quark and tau [Abstract]
  - arXiv:2608.28377 (CMS): Resonant mu + u/b jet; text notes s/c couplings bracketed [Sec. benchmark scenarios]

## C073 — Unparticles / mass-gapped conformal sector
- Status label: well-covered
- Confidence: medium
- Reason: Positive evidence of CMS unparticle interpretations (1408.3583, 1701.02042, r925365) and hidden-valley coverage; no distinct observable left; theory interest low (no post-2019 INSPIRE hits). Caveat: Run 2 full-dataset unparticle monojet reinterpretation not verified.
- Covering/closest searches:
  - arXiv:1408.3583 (CMS): Monojet search with explicit limits on unparticle parameter Lambda_U (8 TeV) [Abstract]
  - arXiv:1701.02042 (CMS): Z + MET: dark matter and unparticles (13 TeV, 2.3 fb-1) [Abstract]
  - recid:925365 (CMS): Scalar/tensor unparticles in diphoton (10 TeV sensitivity study, 2009) [Abstract]
  - arXiv:2403.05311 (CMS): SUEP: hidden valley with confinement (mass-gapped unparticle models are hidden valleys per Strassler arXiv:0801.0629) [Abstract]
