# Gate-2 triage batch 2 (C014-C026)

## C014 - HOLD (proposed-not-searched, conf low)
- Observable: ttbar (lepton+jets) with one top -> u/c + invisible massless dark photon (t->q gammabar): MET + single b-jet/lepton topology; also dark-photon -> ll for massive Z_D.
- Closest: arXiv:2503.20033 (CMS): DM + single top production (mono-top MET), not top decay to q+invisible; arXiv:2312.08229 (CMS): top FCNC t->q gamma (visible photon); arXiv:2403.15332 (ATLAS): t->aq with LONG-LIVED hadronic ALP, not invisible
- Gap: No CMS/ATLAS search or interpretation for t->u/c + invisible (massless dark photon) found via INSPIRE (2 collab queries empty, refersto 1477224 returns no CMS/ATLAS paper); sensitivity to BR not quantified.
- HL-LHC: Huge ttbar sample (ttbar ~1e9 at 3/ab) but SM-like MET + lepton+jets background; realistic model BR far below plausible sensitivity.
- Reason: Signature is measurable and un-searched, but model BR is predicted 1e-8-1e-7 (1607.05928) and no sensitivity estimate exists; needs a quick recast/sensitivity feasibility check before PASS.

## C015 - PASS (searched-limited-regime, conf medium)
- Observable: ttbar event (lepton+jets tag) with t->a q, a long-lived GeV-scale ALP decaying to jets/mumu/gamma gamma in tracker/calorimeter/muon system (displaced vertex or calorimeter deposit).
- Closest: arXiv:2403.15332 (ATLAS): first limits on t->aq: hadronic ID displaced vertex, 1-lepton region, BR>0.1% excluded for 1.6<ctau<130 mm and 40<m_a<55 GeV; arXiv:2407.09183 (ATLAS): neutral LLP displaced jets in calorimeter; no top-tagged interpretation seen; arXiv:2409.10806 (CMS): light LLP displaced jets 13.6 TeV, not top-tagged
- Gap: ATLAS 2403.15332 sets t->aq limits only for m_a 40-55 GeV, ctau 1.6-130 mm (hadronic ID DV); region m_a ~2-10 GeV, cTau 0.006-10 m (2202.09371 gap quote), and leptonic/photonic ALP decays and calorimeter/muon-system decays in ttbar have no CMS/ATLAS result found.
- HL-LHC: Huge ttbar statistics; lepton from other top gives trigger; calorimeter/ MS decays, timing (MTD/HGTD) for intermediate ctau; BR reach 1e-4 vs ATLAS 1e-3.
- Reason: Experimental signature exists, first result covers a narrow corner; clear untested parameter window with HL-LHC-relevant statistics.

## C016 - HOLD (well-covered, conf low)
- Observable: low-mass dimuon/dielectron resonances (scouting), lepton-jets prompt/displaced, H->gamma+Z_D; residual: single displaced lepton-jet and electron lepton-jets.
- Closest: arXiv:2309.16003 (CMS): prompt GeV-scale dimuon resonance via scouting, Run 2 96.6/fb; recid:3157005 (CMS): prompt low-mass dimuon 13.6 TeV, 175/fb (2022-2024); arXiv:2606.25840 (CMS): LLP->muons via scouting 13.6 TeV, low-pT dimuon triggers, displaced; arXiv:2407.09168 (ATLAS): prompt dark photon -> collimated e/mu pairs from ggF Higgs, 140/fb; arXiv:2601.21361 (ATLAS): dimuon 35-75 GeV 140/fb; arXiv:2406.01656 (ATLAS): H->gamma + massless dark photon combination
- Gap: Only residual: one displaced lepton-jet recoiling against ISR/MET (gap quote is from a 2018 MATHUSLA document, arXiv:1806.07396, i.e. stale) and displaced electron lepton-jets; not verified either way.
- HL-LHC: Scouting / L1 scouting at HL-LHC extends low-pT reach; but Run 3 scouting already exploits it.
- Reason: Umbrella of signatures that are individually covered by Run 2/Run 3 CMS and ATLAS results (prompt dimuon scouting, prompt lepton-jets, displaced dimuon scouting). Kept as HOLD only for the narrow single displaced lepton-jet residual; recommend splitting or dropping.

## C017 - PASS (one-observable-not-another, conf medium)
- Observable: Ratio of same-sign (LNV) to opposite-sign (LNC) prompt+displaced lepton pairs from pseudo-Dirac HNL as function of mass splitting / decay length (HNL-antiHNL oscillation), W->l N and heavier N production.
- Closest: arXiv:2204.11988 (ATLAS): displaced dilepton vertex in W->N l; limits only in 'Dirac limit' and 'Majorana limit' (equal LNC/LNV); LNC/LNV separated only with charge cut in mu-mu-e, e-e-mu channels; arXiv:2503.16213 (ATLAS): leptonic+semileptonic displaced HNL, Dirac-like and Majorana-like (1SFH, 2QDH models; Majorana limit = small mass splitting enabling oscillations); arXiv:2201.05578 (CMS): displaced 3-lepton HNL with LNV/LNC charge categories in mixed-flavour (mu mu e etc.); arXiv:2508.20929 (ATLAS): prompt SS dilepton/trilepton HNL LNV scenario
- Gap: CMS/ATLAS HNL results give Dirac or Majorana limit only; none reports LNV/LNC fraction as a function of HNL mass splitting or oscillation (decay-length) for the pseudo-Dirac regime, where 2606.25982 shows LNV is suppressed.
- HL-LHC: 3/ab statistics, timing/precision vertexing for oscillation patterns; charge ID in displaced vertices.
- Reason: Observable well defined, existing searches categorise LNV/LNC but do not scan the splitting; HL-LHC relevance plausible but not yet quantified in a projection.

## C018 - HOLD (searched-limited-regime, conf low)
- Observable: Grab-bag: muon-system displaced showers from RHN (B-L / Higgs-portal) with prompt lepton; tau-flavoured HNL/type-III; boosted N fat jets; VBF+displaced.
- Closest: arXiv:2402.01898 (CMS): LLP showers in muon detectors, twin-Higgs interpretation 0.4-55 GeV; arXiv:2407.20676 ((theory recast)): RHN reinterpretation of CMS MS shower search, 'motivates dedicated search' with optimisation for 3-body decays; arXiv:2202.02039 (ATLAS): type-III seesaw 3-4 leptons, 139/fb; arXiv:2407.10717 (CMS): long-lived HNL lepton + jet displaced vertex 1-16.5 GeV; recid:3186740 (CMS): WR -> tau N, N-> tau qq (merged/resolved) Run 2; arXiv:2112.03949 (CMS): WR->l N merged/resolved ee/mumu qq
- Gap: Best residual: HNL (RHN from W/Higgs) interpreted in CMS muon-system displaced-shower analyses with a prompt-lepton requirement; other sub-themes (type-III, WR->tau N, boosted N) have dedicated Run 2 searches.
- HL-LHC: Muon-system shower and HNL timing at HL-LHC; VBF-triggering of neutral LLP.
- Reason: Heterogeneous merge; majority of sub-signatures already searched; one narrow sub-direction (muon-system showers for HNL) is a recast-level theory proposal needing check of CMS 2402.01898/3181328 for HNL interpretation.

## C019 - PASS (theory-explored-untested, conf medium)
- Observable: Long-lived doubly charged scalar H++ (triplet) with ctau 0.1-100 mm: displaced same-sign lepton/W*W* vertex, multi-charged track, disappearing/kinked track; plus compressed H++/H+ soft same-sign dilepton.
- Closest: arXiv:2211.07505 (ATLAS): prompt H++ -> l l, 400-1300 GeV in 2-4 lepton, 139/fb; arXiv:2101.11961 (ATLAS): H++/H+ -> VV multilepton (prompt); arXiv:2410.09164 (CMS): HSCP large dE/dx stable-regime; INSPIRE:2084511 (CMS): HL-LHC projection prompt H++->ll: expected exclusion 1400 GeV (Phase-2 Delphes)
- Gap: No CMS/ATLAS search found for H++ with proper decay length 0.1-100 mm (neither prompt multilepton nor stable HSCP cover it, per 2608.27251 survey of existing searches); compressed low-m_ll same-sign pair also untested (2305.06889).
- HL-LHC: 3/ab reach for DY pair production with displaced vertex; tracker timing (MTD) and L1 track trigger could help displaced leptons/tracks.
- Reason: Clear signature (displaced same-sign vertex), existing experiment results prompt-only or stable-only, HL-LHC prospects exist at pheno level only.

## C020 - REJECT (indirectly-covered, conf medium)
- Observable: Disappearing tracks from charged dark-meson 3-plet; diphoton/diboson/same-sign WW resonances from 5-plet eta_5 via chiral anomaly.
- Closest: arXiv:2201.02472 (ATLAS): disappearing track (recast in 2507.13430 Sec.3.1, bound ~1.2 TeV); arXiv:2507.13430 ((theory)): recasts ATLAS/CMS diphoton, ZZ, WW semileptonic, same-sign W searches for eta_5; Fig.7-8 contain existing and projected resonance constraints
- Gap: None distinct: signatures reduce to standard diphoton/diboson resonance and disappearing-track searches already recast; only the G-violating vector-meson decay is open, with no distinct collider observable specified.
- HL-LHC: Standard VBF/diboson/diphoton resonance and disappearing-track searches already scale with luminosity.
- Reason: Model-specific interpretation of existing signatures (authors recast them themselves); no new observable. Not a literal experimental result for the model, hence status indirectly-covered.

## C021 - PASS (indirectly-covered, conf medium)
- Observable: Fully merged ALP (0.1-6 GeV): a+gamma at very high pT seen as single photon candidate with two-photon substructure; VBF dijet + merged diphoton using Run-3 parking / HL-LHC L1 scouting.
- Closest: arXiv:2603.03250 (CMS): diphoton 10-70 GeV via new diphoton trigger, ggF, 54.4/fb 2018; arXiv:2211.04172 (ATLAS): boosted diphoton 10-70 GeV, 138/fb; arXiv:2601.00183 (CMS): H->AA->4gamma semi-merged 1<m_A<15 GeV (Higgs decay topology); arXiv:2312.03306 (ATLAS): H->aa->4gamma incl. collimated photons
- Gap: Only an indirect bound exists (2607.12004 recast of ATLAS high-mass diphoton search, no dedicated experiment analysis); no CMS/ATLAS search for single merged-photon ALP with substructure for 0.1-6 GeV or for VBF+merged photon in scouting/parking.
- HL-LHC: Phase-2 L1 scouting, tracker-based merged photon reconstruction, high granularity; 3/ab.
- Reason: Identifiable signature, closest experimental searches stop at 10 GeV, two recent theory proposals incl. Phase-2 scouting.

## C022 - HOLD (searched-limited-regime, conf low)
- Observable: (a) gamma gamma + 1-2 forward protons with m_gg < 150 GeV; (b) UPC Pb-Pb exclusive diphoton, ALP 1-5 GeV with lower trigger thresholds; (c) monopole in UPC.
- Closest: arXiv:2304.10953 (ATLAS): AFP-tagged diphoton ALP 150-1600 GeV, 14.6/fb; arXiv:2311.02725 (CMS/TOTEM): exclusive diphoton with PPS, m_gg>350 GeV, 103/fb; arXiv:2412.15413 (CMS): LbL and BW in PbPb, 1.7 nb-1, ALP m>5 GeV; arXiv:2008.05355 (ATLAS): LbL PbPb with ALP 6-100 GeV (scout note; range UNVERIFIED); arXiv:2408.11035 (ATLAS): monopole pair in UPC Pb+Pb
- Gap: Proton-tagged diphoton below 150 GeV (single-tag acceptance 0.02<xi<0.12 per 2208.10526) and UPC LbL ALP below 5 GeV have no CMS/ATLAS result found; ATLAS pilot LbL trigger optimisation (recid 2751571) suggests the UPC low-mass effort is under way.
- HL-LHC: Run 4 PbPb luminosity for UPC; proton tagging in HL-LHC pileup is doubtful (combinatorial background).
- Reason: Specific gaps exist but proton-tag sensitivity is Run-3-bound and pile-up-limited at HL-LHC; UPC low-mass gap is plausible but already an active experimental programme.

## C023 - PASS (one-observable-not-another, conf medium)
- Observable: h->aa with mixed decays: (mu mu)(gamma gamma) / ll gamma gamma with m_ll != m_Z (2mu4gamma-type), h->A A->(gg)(gamma gamma) wide-jet + diphoton, ALP pair in HH; h->Za with a->hadrons.
- Closest: arXiv:2312.01942 (ATLAS): h->Za, a->gamma gamma, ll=Z, 0.1-33 GeV, 139/fb; recid:2646011 (CMS): h->Z a, a->gamma gamma, 1-30 GeV, 138/fb; arXiv:2601.00183 (CMS): H->AA->4gamma semi-merged; arXiv:2508.06947 (CMS): 4tau and 2mu2tau, 4-15 GeV; arXiv:2503.05463 (ATLAS): H->aa->4tau boosted 4-15 GeV (single Higgs)
- Gap: Searches cover h->Za(ll on Z, gamma gamma), 4gamma, 4tau, 2mu2tau, 4b; none found for h->aa->(mu mu)(gamma gamma)/ll gamma gamma with ll off-Z, or (gg)(gamma gamma) wide-jet+photon pair (2608.18506 'no dedicated search yet'; WebSearch also found none).
- HL-LHC: 3/ab with ~1e8 Higgs bosons; merged-photon reconstruction with granular HGCAL/ timing.
- Reason: Multiple mixed channels untested, exotic-Higgs BR reach scales with statistics; some sub-ideas (HH 4tau) are weak.

## C024 - REJECT (well-covered, conf medium)
- Observable: m_ttbar peak-dip lineshape from heavy spin-0 (radion/ALP/A,H) interfering with gg->tt; ttbar+MET and 4-top for top-philic ALP.
- Closest: arXiv:2507.05119 (CMS): A/H->tt, 365-1000 GeV, widths 0.5-25%, interference with SM tt included (peak-dip), 1/2-lepton, 138/fb; reports excess near threshold; arXiv:2304.01678 (ATLAS): top-philic heavy resonance 1-3.2 TeV in ttbar/tttt; arXiv:2608.10148 (CMS): four-top resonance, vector/scalar/pseudoscalar top-only boson; arXiv:2505.05300 (CMS): DM + t/tt with MET (handle on ALP-top coupling per 2303.17634)
- Gap: None: peak-dip lineshape for spin-0 resonances already built into CMS 2507.05119; radion is a special case of a gluon-fusion scalar.
- HL-LHC: n/a (covered)
- Reason: Positive evidence of experiment-level interference-aware search over 365-1000 GeV; remaining radion-specific details are interpretation only.

## C025 - HOLD (indirectly-covered, conf low)
- Observable: (a) VBS high-mass tails via off-shell ALP; (b) mu mu peak in Z->mumugamma; (c) leptophilic/LFV ALP: l l' resonances, 3l+gamma.
- Closest: arXiv:2202.03450 ((theory)): reinterprets CMS Run 2 public VBS measurements for ALP couplings; arXiv:1912.04776 (CMS): narrow dimuon resonance <200 GeV (scouting + standard); arXiv:2609.12683 (CMS): boosted mumu+tautau light pseudoscalar; arXiv:2508.06947 (CMS): 4tau, 2mu2tau
- Gap: No CMS/ATLAS ALP-specific VBS interpretation or Z->mumugamma dimuon-bump search found, but evidence is thin and the VBS part is an EFT reinterpretation of existing measurements.
- HL-LHC: VBS statistics at HL-LHC; Z->mumugamma with scouting.
- Reason: Heterogeneous, scout gap evidence weak, partial indirect coverage; promising only as a feasibility check of Z->mumu gamma / VBS ALP.

## C026 - PASS (LHC-not-projected-to-HL, conf medium)
- Observable: Delayed displaced vertices / displaced tracks with late arrival at MTD/HGTD relative to hard-scatter time (VBF-tag reference), delayed leptons/photons; late slow-HSCP via MTD ToF.
- Closest: arXiv:2212.06695 (CMS): out-of-time trackless jets with ECAL timing, Run 2; arXiv:1909.06166 (CMS): delayed photons ECAL timing; arXiv:2409.10806 (CMS): light LLP displaced jets, spatial DV; arXiv:2410.09164 (CMS): HSCP large dE/dx
- Gap: Pheno literature exists, but no CMS/ATLAS full-simulation Phase-2 study of delayed displaced vertex/tracks with MTD/HGTD reference-time (VBF tag) was found; experiment-level physics performance only generic.
- HL-LHC: Direct: MTD (30-60 ps) and HGTD only exist at HL-LHC; time-of-flight resolves 70-700 ps delays.
- Reason: Intrinsically HL-LHC detector capability; pheno-level studies abound, so value is in an experiment-realistic analysis rather than a new idea.

