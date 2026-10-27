# Scout note: ALP and light new states (cluster alp_light)

104 papers, 18 candidate seeds, 67 query entries. Data: `scout_alp_light.json`. All recids/arXiv IDs come from INSPIRE records fetched via inspire.py; gap quotes are verbatim extractions (two-column PDFs may have interleaving; the 1708.02243 quote is short and context-dependent). Gap status labels follow methodology taxonomy; no numbers taken from memory.

## Caveats
- Shared tmp dir was clobbered by parallel agents once; outputs were rebuilt in a private scratchpad.
- Completeness of 'no CMS/ATLAS search seen' is UNVERIFIED (INSPIRE title queries only; multi-`t` conjunctions with OR returned nothing, so quoted-phrase queries were used).
- Several 2026 items (e.g. 2609.22570, 2607.12004, 2608.18506) are weeks old: no forward citations expected.

## Seeds

### 1. Fully merged (single-photon-like) ALP decays in a+gamma and VBF topologies, 0.1-6 GeV  [proposed-not-searched, phenomenology, conf medium]
For 0.1<m_a<6 GeV the two photons from a boosted ALP are collimated and reconstructed as one photon; a recast of existing high-energy photon+X data already gives the strongest current bound in this window, and the author notes a dedicated substructure analysis could improve it.
- Signature: a+gamma at very high pT with a single photon candidate showing two-photon substructure (shower shape, conversions); VBF + merged photon; HL-LHC granular calorimetry/timing
- Gap (arXiv:2607.12004, extensions/footnote 2, p.2-4): "A dedicated analysis that can resolve the substructure in the photon candidate [29, 30] may further increase the sensitivity."
- Closest search (arXiv:1808.10515): ATLAS pairs of highly collimated photon-jets (different topology: pair of ALPs)
- Closest search (arXiv:2601.00183): CMS H->AA->gamma gamma semi-merged (Higgs-decay topology, not a+gamma)
- Notes: Gap is from a theory recast; no dedicated CMS/ATLAS merged-photon a+gamma search seen in INSPIRE listings (completeness UNVERIFIED). Paper is very recent: no CMS/ATLAS forward citations.

### 2. ALP VBF with Run-3 data parking and HL-LHC L1 scouting (10 MeV-10 GeV)  [proposed-not-searched, experimental-analysis, conf medium]
Light ALPs with moderate couplings are produced via VBF but soft events fail trigger thresholds and boosted decay photons merge. Proposal: VBF-jet data parking in Run 3 plus Phase-2 trigger-level scouting plus tracker-based merged-photon reconstruction.
- Signature: VBF dijet (forward jets, large delta-eta) + merged diphoton from ALP in parked/scouted streams; diphoton pT as mass proxy in scouting
- Gap (arXiv:2609.22570, Conclusions): "Developing an invariant-mass reconstruction from the information available in the scouting stream would add the most powerful discriminant to the Phase-2 search, and we consider it a highly valuable avenue for future work."
- Gap (arXiv:2609.22570, Introduction): "We find that this approach can unlock a portion of the parameter space that has not been explored before."
- Closest search (arXiv:2603.03250): CMS diphoton resonance search 10-70 GeV (standard triggers, no VBF/scouting)
- Closest search (arXiv:2111.13669): CMS non-resonant ALP in ZZ/ZW (heavy regime)
- Notes: Projection paper (Sep 2026); no experiment follow-up yet. Existence/size of VBF parking stream should be checked in 2403.16134.

### 3. Semi-exclusive/exclusive photon-fusion ALP with proton tags below 150 GeV  [constrained-but-region-open, experimental-analysis, conf medium]
Proton tagging gives a missing-mass handle on gamma gamma -> a -> gamma gamma. ATLAS AFP searched 150-1600 GeV; theory states lower masses have unconstrained parameter space reachable with a small dataset. HL-LHC timing detectors would help pileup rejection.
- Signature: two photons + one/two forward protons (diphoton mass/rapidity matched to proton missing mass), m_gg<150 GeV
- Gap (arXiv:2208.10526, text (kinematic reach discussion)): "At lower masses, ma < 150 GeV, there exist regions of unconstrained parameter space that may be probed even with a relatively small dataset."
- Closest search (arXiv:2304.10953): ATLAS AFP ALP search, 150-1600 GeV (abstract), 14.6 fb-1
- Closest search (arXiv:2311.02725): CMS high-mass exclusive diphoton with tagged protons
- Closest search (arXiv:2603.20837): ATLAS AFP-tagged dilepton missing-mass (other final state)
- Notes: Forward-citation check on 1803.10835 found ATLAS 2304.10953 (>=150 GeV) and CMS 2311.02725 (high mass); no sub-150 GeV tagged ALP search found (completeness UNVERIFIED). CMS PPS HL-LHC EoI: 2103.02752.

### 4. Light-by-light UPC Pb-Pb: ALPs below 5 GeV, lower-threshold triggers, Run-4 projections  [LHC-not-projected-to-HL, experimental-analysis, conf low]
CMS selects m(gg)>5 GeV in its Pb-Pb LbL/ALP analysis; ATLAS (in a pp 4-photon search) notes trigger thresholds limit acceptance. Lower-mass ALPs and low-ET photon triggers in UPC need mapping.
- Signature: exclusive diphoton in UPC Pb-Pb with photon ET 2-5 GeV, ZDC neutron tags, ALP mass 1-5 GeV
- Gap (arXiv:2312.03306, Sec. 5 (pp H->aa->4gamma; indirect for UPC)): "A future reduction of the trigger thresholds could significantly improve the analysis acceptance."
- Closest search (arXiv:2412.15413): CMS LbL/BW Pb-Pb, 1.7 nb-1, m(gg)>5 GeV (abstract)
- Closest search (arXiv:2008.05355): ATLAS LbL Pb-Pb 2.2 nb-1 with ALP search
- Notes: UPC gap quote is indirect. The 2018 heavy-ion report (1812.07688) contains HL projections, so 'not projected' is NOT established.

### 5. Higgs -> aa -> (ll)(gamma gamma) / 2mu4gamma mixed ALP-pair final states  [proposed-not-searched, phenomenology, conf medium]
Asymmetric h->aa decay chains (one ALP to photons, other to muons or jets) give final states with no dedicated search.
- Signature: h -> a a -> mu mu + gamma gamma (+ gamma gamma or jj), merged photon pairs at small m_a
- Gap (arXiv:2203.14984, Sec. h->aa->2mu4gamma): "Dedicated searches for events with two leptons and more than two photons currently do not exist."
- Closest search (arXiv:2312.03306): ATLAS H->aa->4gamma prompt/long-lived
- Closest search (arXiv:2601.00183): CMS H->AA->gamma gamma semi-merged
- Closest search (arXiv:2403.10341): CMS H->aa in mumu bb / tau tau final states
- Notes: Forward-citation check: only the ATLAS review 2405.04914 among CMS/ATLAS-collab citing papers; no dedicated search found.

### 6. h -> A_h A_h -> (gg)(gamma gamma) and 4g wide-jet ALP at the 10 GeV scale  [indirectly-covered, phenomenology, conf medium]
A ~10 GeV ALP decaying mostly to gluons gives h->AA->(gg)(gamma gamma), a diphoton resonance with a wide jet, and h->4g two wide jets with 2-prong substructure.
- Signature: diphoton resonance recoiling against a wide jet from the Higgs; two wide 2-prong jets in VBF/ggF Higgs
- Gap (arXiv:2608.18506, Sec. 3 (h->(gg)(gamma gamma))): "No dedicated search has yet been performed for this final state."
- Closest search (arXiv:2211.04172): ATLAS boosted diphoton 10-70 GeV
- Closest search (arXiv:2603.03250): CMS diphoton 10-70 GeV
- Notes: Paper is Aug 2026; the claimed consistency with a CMS excess must be checked in 2603.03250 (UNVERIFIED).

### 7. Long-lived ALPs from exotic top decays (t -> q a), intermediate lifetime  [proposed-not-searched, phenomenology, conf medium]
Top decays t -> c/u + a with GeV-mass ALPs give displaced decays; single-top searches leave the intermediate-lifetime region largely unconstrained.
- Signature: lepton+jets top event with displaced vertex/jets/dimuon from ALP; timing for displaced photons at HL-LHC
- Gap (arXiv:2202.09371, Sec. 1/summary): "Single top searches leave the intermediate lifetime region (cτALP ∼ 0.006 − 1 m for ma = 2 GeV and cτALP ∼ 0.02 − 10 m for ma = 10 GeV) largely unconstrained."
- Closest search (arXiv:2403.15332): ATLAS light LLP displaced vertices in ID (not top-tagged; top interpretation UNVERIFIED)
- Closest search (arXiv:2407.09183): ATLAS displaced jets in calorimeter
- Notes: Forward citations by ATLAS found: 2403.15332 only; no top-tagged displaced ALP search seen.

### 8. Quark-flavour-violating ALPs: t -> a u/c and single-top+ALP  [theory-explored-untested, phenomenology, conf low]
ALP couplings g_{3i} induce t -> a q and single-top+ALP, complementary to meson-decay constraints.
- Signature: t -> q a with a -> gamma gamma, mu mu, jj; associated t+a production
- Closest search (arXiv:2402.11098): CMS dilepton resonance + massive vector boson (not top FV)
- Notes: No gap quote extracted; no CMS/ATLAS t->qa search identified (completeness UNVERIFIED).

### 9. Top/gluon-philic ALP: tt-bar peak-dip lineshape and measurement reinterpretation  [theory-explored-untested, phenomenology, conf medium]
ALP-top coupling modifies the tt-bar lineshape; loop-induced couplings constrained by reinterpreting measurements; HL-LHC dedicated analysis open.
- Signature: tt-bar mass peak/dip near 2 m_t; four-top; ALP + tt
- Gap (arXiv:2303.17634, Introduction): "The ALP-top coupling has not been studied in detail, and this paper aims to cover this gap, and motivate further collider studies."
- Closest search (arXiv:2608.10148): CMS four-top resonance search (ALP interpretation UNVERIFIED)

### 10. ALP pair production gg->aa non-resonant plus Higgs-resonant, lower m_a  [one-observable-not-another, phenomenology, conf medium]
Single and double ALP production in the multi-parameter ALP EFT; non-resonant gg->aa->4gamma sensitive to dim-6 operators; lower m_a left out.
- Signature: 4 photons (merged pairs) with Higgs peak plus continuum m_4gamma
- Gap (arXiv:2607.21712, Sec. 5/Conclusions): "Extending our analysis to lower values of ma is in principle possible, at the cost of dealing with reduced sensitivity and complications in the signal identification, which is beyond the scope of this work."
- Closest search (arXiv:2312.03306): ATLAS H->aa->4gamma (Higgs-resonant only)
- Notes: Non-resonant 4-photon continuum not seen in CMS/ATLAS listings.

### 11. Non-resonant ALP exchange in VBS (WW, gamma gamma, Zgamma) with higher-order operators  [one-observable-not-another, experimental-analysis, conf low]
Heavy-ALP effects as non-resonant contributions in VBS probing m_a >> sqrt(s). CMS searched ZZ/ZW semileptonic; other VBS channels reinterpretations remain.
- Signature: VBS jj + WW/ZZ/Zgamma/gamma gamma high-mass tails; dim-6 effects
- Gap (arXiv:2202.03450, Conclusions): "A systematic and more quantitative assessment of the impact of higher-order ALP operators is left for future work."
- Closest search (arXiv:2111.13669): CMS ZZ/ZW non-resonant ALP semileptonic
- Closest search (arXiv:2503.21977): CMS WZgamma with new-physics constraints (not ALP-specific)

### 12. ALP/U(1)_X in Z -> mu mu gamma radiative decay at HL-LHC  [proposed-not-searched, phenomenology, conf low]
Resonant structure in m(mumu) of Z->mumu gamma; HL-LHC statistics sufficient for leptophilic ALP and anomalous gauge boson.
- Signature: m(mumu) peak in Z -> mumu gamma, photon-tagged; scouting dimuon + photon
- Closest search (arXiv:1808.03684): CMS L_mu-L_tau Z->4mu, 5-70 GeV (abstract)
- Closest search (arXiv:1912.04776): CMS dimuon narrow resonance <200 GeV with scouting
- Notes: Abstract-only evidence for 2604.13156; CMS/ATLAS Z->mumu gamma measurement not checked.

### 13. Leptophilic/lepton-flavour-violating ALPs (mu, tau) at the LHC  [theory-explored-untested, phenomenology, conf low]
ALP explanations of a_mu probed by exotic Higgs decays and three-lepton final states; flavour-violating ALP in Higgs decays.
- Signature: 3 leptons + photon; h -> aa -> 4tau / 2mu2tau; boosted tau pairs; e-mu / mu-tau resonances
- Closest search (arXiv:2508.06947): CMS 4tau and 2mu2tau light pseudoscalar pair
- Closest search (arXiv:2503.05463): ATLAS boosted 4tau
- Closest search (arXiv:2609.12683): CMS boosted mumu+tau light pseudoscalar
- Notes: Flavour-violating (e-mu, mu-tau) ALP final states: no direct CMS/ATLAS search seen (UNVERIFIED).

### 14. Light L_mu-L_tau Z' below 5 GeV via scouting/parking multi-muon  [searched-limited-regime, experimental-analysis, conf low]
CMS Z->4mu covers 5-70 GeV; lighter Z' via 4mu/3mu with scouting dimuon triggers is a candidate.
- Signature: low-mass dimuon in Z->4mu or scouting triggers
- Closest search (arXiv:1808.03684): CMS Z->4mu, 5-70 GeV (abstract)
- Closest search (arXiv:1912.04776): CMS dimuon <200 GeV using scouting; lower edge UNVERIFIED
- Notes: No gap quote; complementary Belle II/NA64 bounds not checked.

### 15. Prompt lepton-jets / dimuon-jets at HL-LHC with scouting  [searched-limited-regime, experimental-analysis, conf low]
Collimated lepton/muon-jets from hidden sectors; ATLAS 8 TeV prompt search; HL-LHC prospects exist for displaced muon-jets. Prompt lepton-jets with scouting remain a candidate.
- Signature: >=2 collimated muons, electron-jets, prompt/displaced, scouting stream
- Closest search (arXiv:1511.05542): ATLAS 8 TeV prompt lepton-jets
- Closest search (arXiv:2606.25840): CMS LLP to muons with scouting
- Closest search (arXiv:2407.20425): CMS pair production of new bosons decaying to muons
- Notes: No gap quote; 13 TeV prompt ATLAS lepton-jet result not confirmed in listings.

### 16. Quirks: stopped/out-of-time annihilation and long-string regime  [proposed-not-searched, phenomenology, conf medium]
Quirks lose energy and annihilate out-of-time; existing out-of-time R-hadron search recast; regime with long strings left for future work.
- Signature: out-of-time energy deposits, anomalous ionisation, bent tracks
- Gap (arXiv:1708.02243, Sec. on existing HSCP-search sensitivity (garbled two-column extraction)): "We leave this possibility for future work."
- Closest search (arXiv:2104.03050): ATLAS stopped long-lived particles (cites quirk paper)
- Closest search (arXiv:1102.0459): ATLAS highly ionising particles 7 TeV
- Notes: No dedicated CMS/ATLAS quirk search in listings (D0 only, 1008.3547); exhaustive status UNVERIFIED.

### 17. Monopole/HIP: photon-fusion production with proton tags; virtual-monopole diphoton effects  [searched-limited-regime, experimental-analysis, conf low]
Monopole pair production via photon fusion in pp and Pb-Pb UPC; ATLAS UPC search and MoEDAL Schwinger search exist; virtual monopole/HECO effects in LbL proposed.
- Signature: highly ionising tracks in UPC Pb-Pb; diphoton tails; proton-tagged diphoton
- Closest search (arXiv:2408.11035): ATLAS monopole pair in UPC Pb+Pb
- Closest search (arXiv:1903.08491): MoEDAL trapping detector
- Closest search (arXiv:2402.15682): MoEDAL Schwinger
- Notes: Dyon sensitivity not checked; no gap quote.

### 18. Precision timing for light long-lived ALP/portal decays at HL-LHC  [LHC-not-projected-to-HL, phenomenology, conf low]
MTD/HGTD timing improves LLP searches; delayed photons from ALP decays and displaced diphotons.
- Signature: delayed photon/jets via timing layer; displaced vertex
- Closest search (arXiv:2209.01029): ATLAS displaced photons from exotic Higgs decays
- Closest search (arXiv:2312.03306): ATLAS long-lived a->gamma gamma
- Notes: Speculative; no gap quote.
