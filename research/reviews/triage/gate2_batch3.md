# Gate-2 triage batch 3 (C027-C039)

## C027 - HOLD (LHC-not-projected-to-HL, conf medium)
- Observable: L1-track-trigger displaced-vertex / displaced-dimuon (exotic B->K Phi, low-mass hadronic DV) and ECAL-timing displaced-jet triggers at HL-LHC; umbrella of trigger/algorithm enablers rather than one signature
- Closest: arXiv:2508.06363 (CMS); arXiv:2606.25840 (CMS); arXiv:2409.10806 (CMS); arXiv:2601.17544 (CMS)
- Gap: No CMS/ATLAS-published physics-reach projection (limits/sensitivity vs Run-3 scouting/parking) for L1-triggered low-mass displaced dimuon or hadronic DV at HL-LHC; recid:2908980 is a trigger feasibility study only. Candidate is an enabler umbrella, not a single signature; best sub-target is B->KPhi displaced dimuon/hadrons.
- Reason: Identifiable observable and strong HL link, but umbrella of three trigger/algorithm seeds, the collaboration already works on the Phase-2 DV trigger, and Run-3 parking/scouting searches cover the near-term signatures; evidence on net added physics reach unclear.

## C028 - REJECT (well-covered, conf medium)
- Observable: Higgs -> phi phi -> 4j displaced multi-jet vertices at c*tau ~ 1 cm (ggF/VBF/VH)
- Closest: arXiv:2409.10806 (CMS); arXiv:2107.06092 (ATLAS); arXiv:2203.01009 (ATLAS)
- Gap: The 2019 'blind spot at ~1 cm' (1902.10229, 1902.00134) is now addressed by CMS 2409.10806 for mS>40 GeV in ggF; residual region (mS<40 GeV, B<1%) is an incremental HL extension folded into C027.
- Reason: Positive evidence that CMS 2409.10806 covers c*tau ~1 cm for H->SS->4b/4d with ggF triggers, with limits stated in conclusions.

## C029 - PASS (theory-explored-untested, conf medium-low)
- Observable: Short/disappearing charged track followed by a displaced dilepton vertex (+MET), nested DT->DV chain, with MTD/HGTD time-of-flight delay (~200-800 ps); plus pure-higgsino ~0.3 GeV splitting DT
- Closest: arXiv:2603.08315 (ATLAS); arXiv:2309.16823 (CMS); arXiv:2410.16835 (ATLAS); arXiv:2603.01991 (ATLAS)
- Gap: No CMS/ATLAS search requires the correlated DT stub + delayed displaced dilepton vertex (nor uses MTD/HGTD delay for it); individual DT and DV searches are model-agnostic about the other leg. Benchmark is scotogenic (model-specific), higgsino part already has HL projections.
- Reason: Identifiable signature, specific gap per grep of searches, explicit HL timing relevance; confidence limited because evidence for the gap comes from pheno papers' own claims and the benchmark is niche.

## C030 - HOLD (indirectly-covered, conf low-medium)
- Observable: Neutral LLP -> gamma gamma decaying inside the HCAL: EM-like shower in HCAL, no tracks, no ECAL energy (emerging photon jet)
- Closest: arXiv:2203.01009 (ATLAS); arXiv:2209.01029 (ATLAS); recid:3186732 (CMS); arXiv:2304.12885 (ATLAS)
- Gap: No ATLAS/CMS interpretation of photon-decaying LLPs depositing energy in the HCAL; existing ECAL photon searches stop at the ECAL and CalRatio may already be partly sensitive (unchecked), so a recast/reinterpretation is the first step.
- Reason: Signature identifiable, but overlap with CalRatio-type selections is unresolved and the sole benchmark is an ultralight fermiophobic Higgs; evidence unclear.

## C031 - PASS (theory-explored-untested, conf medium)
- Observable: Sequential displaced vertices (tumblers) in one decay chain, vertex-to-vertex direction consistency, chain mass/lifetime reconstruction, with 4D vertex timing
- Closest: arXiv:2104.13474 (CMS); arXiv:2203.00587 (ATLAS); arXiv:2301.13866 (ATLAS)
- Gap: No ATLAS/CMS search or projection targeting vertex chains; INSPIRE forward citations of 2108.02204 show no collaboration follow-up (only pheno/DM papers). Second seed (generic lifetime/mass measurement) is vague and only supports this.
- Reason: Concrete new multi-DV topology with timing synergy and no collaboration search found; confidence limited because only title/abstract-level check of multi-DV searches and the model dependence of tumbler rates.

## C032 - HOLD (searched-limited-regime, conf medium-low)
- Observable: Displaced tau pairs from light long-lived pseudoscalar a (h->Za or h->aa->4tau), displaced-track tau jets
- Closest: arXiv:2409.10806 (CMS); recid:2866938 (CMS)
- Gap: GeV-scale (<15 GeV, collimated) displaced tau pair and h->Za-associated topology not covered by CMS 2409.10806 (mS>=15, ggF, tau ID); pheno paper 2408.07366 shows reach already at 300/fb, so HL-specific value is unclear.
- Reason: Signature partially searched; remaining region (low mass, Z-associated) is describable but HL-specific added value not demonstrated.

## C033 - REJECT (indirectly-covered, conf medium)
- Observable: None distinct: benchmark of main-detector LLP reach vs far detectors (GRENDEL/MATHUSLA/ANUBIS)
- Closest: arXiv:2409.10806 (CMS); arXiv:2403.15332 (ATLAS); arXiv:2606.25840 (CMS); arXiv:2609.00152 ((proposal, not CMS/ATLAS))
- Gap: n/a - not a measurable signature; the 'trigger limitations' gap is C027.
- Reason: Fails Q1: a detector-comparison framing, not a collider observable CMS/ATLAS can measure; GeV-scale LLP main-detector coverage exists (2409.10806, 2403.15332, 2606.25840). Fold into C027.

## C034 - REJECT (well-covered, conf medium)
- Observable: HSCP R-hadrons with charge flipping (dE/dx+ToF), stopped R-hadrons, gluinonium resonance
- Closest: arXiv:2410.09164 (CMS); arXiv:2502.06694 (ATLAS); arXiv:2104.03050 (ATLAS); arXiv:2601.20063 (CMS); arXiv:1801.00359 (CMS)
- Gap: Residual: gluinonium resonances at HL (theory-only, rates UNVERIFIED) - weak motivation.
- Reason: Charge-flip and stopped R-hadron modelling already treated in CMS 2410.09164 and ATLAS 2104.03050/2502.06694; remaining gluinonium piece not supported by evidence of HL-LHC reach.

## C035 - REJECT (well-covered, conf medium)
- Observable: Intermediate-lifetime RPV LSP: DV, displaced leptons/jets plus cascade MET/jets across coupling range
- Closest: arXiv:2603.15007 (ATLAS); arXiv:2402.15804 (CMS); arXiv:2603.12051 (ATLAS); arXiv:2601.05664 (ATLAS); arXiv:2110.04809 (CMS)
- Gap: Residual: electroweak-production slepton/sneutrino/higgsino LLP corners (see C038, C037); broad claim of an uncovered intermediate regime is superseded by ATLAS 2603.15007.
- Reason: Broad framing is directly covered by ATLAS 2603.15007 (+CMS DV/displaced-lepton searches); no specific uncovered signature remains in this candidate.

## C036 - HOLD (one-observable-not-another, conf low-medium)
- Observable: qqqN quark-portal: MET+jet/top/bjet, and displaced N->qqq vertex + MET; mesogenesis colour-triplet scalar to b+light quark at few TeV
- Closest: arXiv:2107.13021 (CMS); arXiv:2402.15804 (CMS); arXiv:2609.21850 (CMS); arXiv:2402.18461 (CMS)
- Gap: Displaced N->qqq + MET from quark-portal BNV not interpreted by collaborations; DV+MET searches likely sensitive, so recast needed. Second seed (DeltaB=2 same-sign tops/multijet) has no concrete uncovered signature.
- Reason: Observable identifiable and partly recast by pheno, but overlap with DV+MET and paired-dijet searches unresolved; HL value not shown beyond luminosity scaling.

## C037 - HOLD (searched-limited-regime, conf low)
- Observable: Higgsino/wino -> three jets (UDD, top-philic lambda''_3jk): multilepton + many jets + b-jets; also paired b+light dijet resonances; coloured-LSP mu-nu-SSM
- Closest: recid:2773141 (CMS); arXiv:2503.06726 (CMS); arXiv:2106.09609 (ATLAS); arXiv:2609.21850 (CMS)
- Gap: Top-philic UDD electroweakino signal region not explicitly targeted, but CMS jet-scaling and b-category searches may partly cover it; paired-dijet seed is now covered by 2609.21850; coloured-LSP seed is pheno-only.
- Reason: Three loosely related seeds; main gap partly covered by existing multilepton+many-jet searches; evidence unclear.

## C038 - HOLD (constrained-but-region-open, conf low)
- Observable: Direct slepton/sneutrino LSP pair production with LQD coupling: pair of l+jj / 4-jet resonances, or displaced dilepton from sneutrino decays
- Closest: arXiv:2608.21033 ((pheno recast)); arXiv:2601.05664 (ATLAS); arXiv:2106.09609 (ATLAS); arXiv:1811.09760 (CMS)
- Gap: Direct slepton/sneutrino LSP LQD signals unconstrained per ABC-III recast (no ATLAS/CMS search targets low-mass l+jj pairs); HL viability unproven.
- Reason: Gap exists in the cited pheno recast but tiny EW cross sections vs QCD multijet make HL relevance unclear.

## C039 - HOLD (searched-limited-regime, conf low-medium)
- Observable: Stealth SUSY: many jets (and 0-2 leptons) or gamma gamma + jets with low MET; left-handed stop/sbottom topologies, e-mu+jets, diphoton outside Higgs window
- Closest: arXiv:2310.03154 (CMS); arXiv:2506.08825 (CMS); arXiv:1411.7255 (CMS); arXiv:2401.16333 (ATLAS)
- Gap: Left-handed stop/sbottom stealth topologies and 13 TeV e-mu stealth have no dedicated search; no ATLAS stealth search found by title/abstract queries; HL benefit is incremental luminosity.
- Reason: Gap is real but model-completeness driven (arXiv:1512.05781, 2015), partly addressed by CMS 2506.08825, and no HL-specific enabler.

