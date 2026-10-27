# T5 - Systematic assumption audit of the quirk theory / phenomenology literature

Investigator T5, 2026-10-07. Scripts: `code/T5_census.py` (INSPIRE sweep, output `outputs/T5_census.json`, `outputs/T5_queries.txt`), `code/T5_estimates.py` (ESTIMATEs, run with `pixi run python code/T5_estimates.py`).
Tags: `[id Sec./Eq./Fig.]` = checked in the cached PDF text; `[id txt:NNN]` = line NNN of `research/cache/pdf/<id>.txt` (quotes); `ESTIMATE` = own calculation (script above); `UNVERIFIED` = recalled/secondary or abstract only.
Convention used throughout: **Lambda = sqrt(sigma_string)** unless stated.

---------------------------------------------------------------------------------------------------
## 1. Executive summary

1. **The literature is small and closed: 34 papers cite Kang-Luty [0805.4642] with "quirk" in title/abstract (of 226 citers), and 31 of them were already in `bibliography.json`.** The extended INSPIRE sweep (41 theory-side queries + 22 citation queries, 484 unique records, Appendix A) found only about 6 new quirk-flavoured papers (0810.1524, 0810.3948, 1604.06180, 1112.4629, 2756876, thesis 1258080) and none that changes the picture. No lattice / effective-string paper cites any quirk-collider paper and vice versa (only Knapen cites Nambu-Goto-vs-lattice, via one reference [1708.02243 Sec.II]). No ATLAS/CMS HSCP paper (2410.09164, 2205.06013, 2601.20063) has a quirk paper in the INSPIRE reference list (as far as `inspire.py refs` shows; 55-80 references seen each).
2. **Assumptions shared by essentially all central-detector studies and never tested** (Sec. 3a): (i) no stochastic material effects (multiple scattering, straggling, delta-rays) in the quirk equation of motion; only the mean dE/dx friction in 3 of 9 studies; (ii) the instantaneous "straight string in the pair CM frame"; only the Athena code has a causal string and nobody has compared the two, although the plane thickness is hypersensitive to the string-direction model (changes by x10-80 between true and fixed s-hat, [2002.07503 Fig.6]); (iii) uniform B, no map; (iv) pile-up never above <mu>=50 and never with the quirk hits themselves in PU; (v) LO + shower production with a single ISR treatment; (vi) epsilon = 0.1 per crossing (Kang-Luty gave two extremes, ~1 and ~1e-3, [0805.4642 Sec.5.7]); (vii) primary vertex assumed known, quirk charges +-1, fermion singlet.
3. **Biggest quantified items (ESTIMATE):** (a) **multiple Coulomb scattering of a slow heavy quirk in the Phase-2 tracker is comparable to the 100 um plane-thickness cut**: out-of-plane rms at the outer layer ~ 50-400 um (upper bound; a free plane fit absorbs part) for m_Q = 500 GeV, beta_q = 0.1-0.2, x/X0 = 1-3 % per layer, and it grows as 1/(m beta^2 gamma) (G-T5-1). No published quirk propagation includes it. (b) The plane thickness is a 1e-3-1e-4 effect (10-100 um out of cm), so approximations that are "good to 1-4 % in force" can change it by O(1); causal vs straight string is untested (G-T5-2). (c) Lambda conventions differ by 15-47 % between papers (G-T5-4).
4. **Open problems that nobody followed up** (Sec. 3b): parameter measurement of (m_Q, Lambda) from hits (stated in 1708.02243 and 1911.02223, no follow-up), dE/dx pattern use, Delta-phi(MET, plane normal) cut [1708.02243], HLT / track-trigger plane finder, PU200, hit noise / misalignment / hard radiation in ML tracking [2509.08878], 0T-data search [1703.00912], high-Lambda (10 keV - 1 MeV) reach at ATLAS/CMS (D0 2010 is the only result besides FASER).
5. **Killed:** effective-string (Luscher) corrections to the propagation (1e-8 at r = 1 um); B-induced angular momentum does *not* make epsilon negligible where it matters (d_min*Lambda < 1 only for Lambda > ~10-30 keV, where B-induced L is tiny); charge exchange (beta > 0.03 always).
6. **Ranking** (value for the CMS Phase-2 target): G-T5-1 (MCS) > G-T5-2 (string causality / thickness sensitivity) > G-T5-6 (high-Lambda unresolved regime, recast of CMS HSCP + MTD) > G-T5-7 (parameter measurement) > G-T5-5 (production / ISR / K-factor) > G-T5-4 (Lambda convention, cheap hygiene) > G-T5-8 (model-space) > rest.

---------------------------------------------------------------------------------------------------
## 2. Census

- Starting point: `bibliography.json` (58 entries; I use the 33 core + adjacent ones listed below). 
- INSPIRE sweep (Appendix A): 41 abstract/title queries (quirk*, squirk*, quirkonium, infracolor, hidden valley + string/confin*, folded SUSY + quirk, quirky little Higgs, long string, macroscopic string, flux tube, hidden confining + EW, dark glueball + quirk, vector-like confinement, effective string, Nambu-Goto, monopole + Geant4, ...) and citation queries by recid for 22 key papers (0805.4642 all 226 citers over 3 pages; 1708.02243: 37; 1911.02223: 13; 2002.07503: 14; 1811.08903: 29; 2108.06748: 17; 2404.13814: 17; 2512.20696: 4; 2607.26195: 1; 1106.2569: 55; 1703.00912: 27; 2410.00269: 8; 2509.08878: 4; 1512.05782: 75; 0805.4667: 67; 2504.02940: 8; 2506.11192: 10; 2311.15486: 9; 1008.3547: 24; 0712.2681: 43; 0909.2034: 100 (cap); 0907.4932: 10).
- Total 484 unique records (405 after the first pass, 79 more from pages 2-3 of the Kang-Luty citers); 426 not in the bibliography, but after filtering for quirk/infracolor/string/confining content only the following are relevant and new:

| arXiv / recid | Paper | Why it matters |
|---|---|---|
| 0810.1524 | Cheung, Keung, Yuan, "Phenomenology of iquarkonium" (33 cit.) | uncoloured iquarks, Lambda' > MeV; bremsstrahlung rate ~ alpha_em Lambda'^4/M^3 [0810.1524 txt:335]; quirkonium radiative de-excitation, parallel to 0805.4667 |
| 0810.3948 | Harnik, Wizansky, "Signals of New Physics in the Underlying Event" (77 cit.) | quirk spin-down as "anomalous underlying event"; direct ancestor of 2506.11192 (which cites it once) and of the soft-radiation idea of 1106.2569 |
| 1604.06180 | Foot, Gargalionis, coloured scalar with confining SU(2), 750 GeV | quirkonium diphoton model, scalar spin, SU(2) with Q = 1/2..1 |
| 1112.4629 | Domenech-Garret, exotic spectroscopy | quirk mention only (UNVERIFIED relevance, not opened) |
| 2756876 (no arXiv) | Zhou, "supersymmetric vector-like quirk ... W mass and g-2" | sibling of 2306.02542 (in bibliography) |
| 1258080 (thesis) | Denk, "Quirky composite dark matter" | thesis, no new content expected |
| 1710.06437 | Li, Salvioni, Tsai, "EW-charged bound states as LHC probes of hidden forces" | not labelled quirk but same physics (EW-charged fermions with a hidden confining force, GeV-scale; resonant annihilation to W X); adjacent |
| 0912.3339 | Teper, "Large N and confining flux tubes as strings - a view from the lattice" (89 cit.) | lattice input for sigma, T_c/sqrt(sigma), Nambu-Goto accuracy; cited by 2504.02940 only |
| 2204.13123 | Yamada, Yonekura, "Cosmic strings from pure Yang-Mills" | macroscopic colour flux tubes from the deconfinement transition (cosmology of IC strings; T1) |
| 2410.09164, 2205.06013, 2601.20063 | CMS Run-2 HSCP large dE/dx; ATLAS Run-2 large ionisation; CMS HSCP with Level-1 scouting | existing HSCP/high-dE/dx searches that have **not** been recast for quirks (their INSPIRE references contain no quirk paper); 2601.20063 is a trigger idea relevant to G-T5-9 |
| 1103.3016 | Odd tracks at hadron colliders | prior art: irregular tracks missed by trigger/reconstruction |

- **Recids-based check of lineage:** all other candidates (about 340) are quantum-computing "Quirk", generic hidden-valley, twin-Higgs or LLP papers without quirk dynamics. Nothing found on: quirk simulation validation vs. full string PDE, quirk measurement, quirks in CMS/ATLAS collaboration notes.
- Not run: GitHub / indico scraping (see literature_map Appendix); I did not re-check the ATLAS repository statement.

---------------------------------------------------------------------------------------------------
## 3. Assumption audit tables

Abbreviations: NG = Nambu-Goto; CM = pair centre-of-mass frame; EoM = equation of motion; MCS = multiple Coulomb scattering; "no PU" = no pile-up; sigma-conv = definition of Lambda. All "Lambda" in the first row of each cell are converted to sqrt(sigma) only if the paper states the relation.

### 3A. Collider-signature papers with macroscopic / mesoscopic / unresolved strings (the ones relevant to the CMS target) - 19 papers

| Paper | Quirk model (spin, charges, N_IC) | Lambda convention and range studied | Production (LO/NLO, ISR) | String treatment | B field | Material and energy loss | Radiation (eps, photons) | PU / detector realism | Signature studied | Stated limitations / open problems (quotes) |
|---|---|---|---|---|---|---|---|---|---|---|
| **0805.4642** Kang-Luty | generic fermion or scalar, coloured and uncoloured, SU(N) | sigma ~ Lambda^2, no precise definition; regimes from macroscopic (< ~100 eV) to microscopic (> ~ GeV) by length l ~ m/Lambda^2 [Sec.3] | parton-level estimates only, no MC; ISR not treated | NG; "straight in CM" justified for F_ext << Lambda^2 [Eq.3.10]; "NG has no longitudinal excitations" [txt:467-470]; NG universality cited from lattice [txt:492-496] | analytic estimate only: B-induced angular momentum prevents annihilation for Lambda < ~MeV [Eq.6.3, Eq.5.64] | mean ionisation friction up to ~(100 eV)^2 [Sec.3.4]; lattice binding of stopped quirks [Sec.4] | glueballs: ~1 emission of energy ~Lambda per crossing if "efficient", or suppressed by (1/3)^6 ~ 1e-3 if glueball mass (m_0 = 3.6 sqrt(sigma)) suppresses it; "we consider the two extremes" [txt:1565-1575, 1795-1810]; Larmor photons [Sec.5.9] | none | all regimes, qualitative | "leaving a more complete investigation to future work" (cosmology); decoherence "beyond the scope" [txt gaps]; "The next step will be to produce event generators" [txt:1827] |
| **1008.3547** D0 | fermion, Q = +-1, uncoloured, N = 2, 3, 5 | "strong dynamics scale"; L ~ 1 um (m/100 GeV)(100 keV/Lambda)^2 [Eq.1]; 10 keV - 1 MeV | modified MadGraph + Pythia 6, jet pT > 75 GeV + MET (jet-trigger) | pair treated as one straight highly-ionising track (string < 100 um, net charge zero) [txt:280-287] | 2 T, not relevant | D0 Geant simulation of the pair as a unit | none | real detector, 2.4 fb^-1, muon-chamber timing gate beta > 0.3 | single high-dE/dx track + ISR jet + MET | only m_Q < 107-133 GeV excluded; the unresolved regime has had no ATLAS/CMS follow-up |
| **1106.2569** Harnik-Kribs-Martin | scalar squirks: coloured triplets, SU(2)_W triplets/singlets Y = 0; N_ic | Lambda_ic ~ GeV, alpha_ic ~ 0.2 (microscopic) | LO cross sections, Tevatron/LHC; no ISR study | microscopic (prompt de-excitation) | none | none | spin-down by infraglueball and photon emission; "rapid energy loss ... kinematic features ... for future work" [txt gaps] | efficiency estimates only | W+jj, dijet, multi-W, monojet, underlying event | no full simulation of kinematics when energy loss is rapid |
| **1703.00912** Farina-Low | fermion (1,1)_{-1}, (3,1)_{2/3} etc., N_IC = 2 | l_eff ~ 10 m (m/TeV)(100 eV/Lambda)^2 (v/0.7)^2 [Eq.3]; 1 eV - 10 keV oddly curved, 10 keV - 1 MeV single straight track; searched 1-100 eV | MG5 2.3.3, pp -> QQ + jet (pT > 200 GeV) | straight-string EoM [Eq.3-4] | 3.8 T and 0 T (proposal) | none | none | CMS tracker geometry, helix chi2 fit, 30 um; recast of CMS HSCP 12.9 fb^-1 and monojet | HSCP, monojet, 0T-data search | "would be interesting to see limits for a larger variety of quantum numbers"; "If it is possible to trigger on such anomalous tracks ..." [txt gaps]; no CMS follow-up (citers of 1703.00912 include only FPF and FASER among collaborations) |
| **1708.02243** Knapen et al. | fermion (1,1)_1 and (3,1)_{2/3}; N_IC = 2 | **Lambda^2 = string tension, "will also serve as a precise definition for Lambda"** [Sec.II]; claims 100 eV - 30 keV (abstract), 100 eV - 10 keV (text) | MG5_aMC + <= 1 jet, MLM, Pythia8; LO; pT(QQ) > 200 GeV cut for MET trigger; eps_trig ~ 0.1 (EW, DY) | NG, straight string in CM; "more general actions ... should not affect our results significantly, as long as the string tension is much larger than the Lorentz force" [Sec.II] | **uniform 2 T B_z**; B torque estimated, Delta phi ~ 1e-5 [Eq.8-9] | **no material in EoM**: ionisation torque estimated ~1e-3 rad per layer and "We therefore neglect this effect in our simulations" [Sec.II]; no MCS | glueball radiation "irrelevantly small ... changes L by a few hbar" [Sec.II] | <mu> = 50 Pythia8 min-bias in simplified detector of 1612.00850, beam spot 45 mm, **barrel pixel + SCT only (|eta| < 1.8)**, pixel-centre hits, 25 ns timing cut; PV assumed identified | coplanar hits, plane-finder, MET trigger | "dedicated trigger ... We leave this possibility for future work"; endcaps/calorimeters/TRT; HLT/track trigger "would be interesting"; dE/dx unused: "would be important to measure mass and string tension" [App.A]; no Delta phi(MET, n3) cut |
| **1811.08903** Evans-Luty | fermion (N,1,1)_1 ("E'") SU(2)_IC; also coloured | Lambda_IC; computed to 1 keV, checked to 10 keV [fn.4]; GeV-keV | modified Pythia8, coloured hadrons; LO | straight string; "retarded time corrections ... safely neglected" [Sec.2] | CMS field map | mean dE/dx (Bethe, Lindhard-Scharff, Anderson-Ziegler interpolation), continuous friction, **no Landau sampling; "individual ionization interactions will give the quirks a momentum transfer transverse ... We have not attempted to model this effect"** [App.B, txt:792-797]; cylindrical CMS zones with filling factors; nuclear interactions neglected | eps_emit = 0.1 per crossing [Eq.B.3, Sec.4] | no PU; CMS full-detector cylinders | stopped quirks, out-of-time decay | positive quirk electron-stripping "not considered here" [fn.2]; atomic de-excitation of stopped quirk "highly uncertain" [App.B]; background-free assumption "may be overly aggressive" [txt:625] |
| **1911.02223** Li-Li-Pei-Zhang | coloured (3,1)_{2/3} fermion/scalar, and E^c "(1,1,-2) in their Y-normalisation", N_IC = 2 | Lambda = sqrt(sigma) implicit; 100 eV - 10 keV, optimised at 1 keV | MG5_aMC (LO, <= 1j), UFO not public; trigger pT(j) > 200 GeV; "typical" pT(QQ) > 100 GeV | straight string with simultaneity condition [Eq.III.6-III.9] | CMS barrel B ("4 T") uniform | **mean dE/dx with BB + LS, filling factors (tracker 0.05, ECAL 0.33, HCAL 0.88), 10 % Gaussian smear**; no MCS | none (argued) | <mu> = 50 pile-up, 45 mm beam spot, CMS barrel 13 layers, 10 um hits; **adds Z(nunu)+jets with PU as background (sigma ~ 1e-2 fb after cuts)** | coplanar + dE/dx-based hit classes | dE/dx pattern for property characterisation "We leave this for future work" [Sec.V]; claims Knapen is "overoptimistic" (no Z+jets bkg) |
| **2002.07503** Li et al. "quirk trajectory" | as above, SU(3) infracolour, coloured fermion | l = 1 cm (1 keV/Lambda)^2 (m/100 GeV) [Eq.I.1]; Lambda ~ 100 eV - 10 keV | MG5_aMC LO, Pythia8 ISR | straight string, **fixed vs true s-hat compared** [Sec.VIII, Fig.6]; analytic EoM for F_ext << Lambda^2 [Eq.II.4-II.8] | "B = 4 T" CMS | mean ionisation (5 % effect on MET cut efficiency [Sec.VII]) | none | CMS detector, <mu> = 50 | analytic amplitude, period number, plane thickness, repeated layer crossing (~ 10 % of events) | analytic thickness valid "up-to one order of magnitude for 1-100 periods" [Sec.IX]; "correct direction [s-hat] is critical in coplanar quirk search" |
| **2108.06748** Li-Pei | 4 models: Etilde, E, Dtilde, D (scalar/fermion, coloured/uncoloured), N_IC = 2 | Lambda 100 eV - 100 keV | MG5_aMC, LO then K-factors for rates; ISR/FSR by Pythia [txt:201-243] | straight (Mathematica EoM) and analytic for Lambda >= 3 keV | **ignored** (dipole deflection <= 2e-5 rad) | BB + LS ionisation through TAS/TAN/concrete/rock; Gaussian smear of dE/dx ignored [txt:671]; hadronic energy loss ignored | glueball + photon radiation ignored in EoM; survival via eps [Eq.4.21-4.22] | none; FASER/FASER2 acceptance | slow quirk pair in forward detectors | "Designing specific cuts ... beyond the scope" [per literature_map] |
| **2311.15486** Li-Liao-Ni-Pei | five simplified models: E, Etilde, D, Dtilde plus a W_R scenario with two scalar quirks (V, Etilde); N_IC = 2, N_C = 3 [txt:1141-1148] | same as above | **NLO QCD** (MG5_aMC@NLO): rate x 1.2-1.4 and forward fraction up by x2-3 [txt:1144-1148, 371] | as above | no | as above | eps = 0.1 | far detectors (FASER2, MATHUSLA, ANUBIS, SND, FACET), no detector sim | timing/straight-line | no collaboration-level detail |
| **2404.13814** Feng-Li et al. | E, Etilde (uncoloured), D, Dtilde, N_IC = 2 (conservative) | Lambda 100 eV - 100 keV | NLO MG5_aMC@NLO + Pythia8; K-factors E: 1.33 (200 GeV), 1.45 (1 TeV); D: 1.54, 1.32 [txt:312-316] | analytic / Mathematica EoM through beamline | none (dipoles negligible) | BB + LS | **eps = 0.1, varied [0.03, 0.3] and [0.01, 1]; eps' = 0.01 (QCD hadron emission), varied [0.005, 0.02]** [Sec.6.4]; "These parameters are not calculable from first principles" [txt:513] | FASER/FASER2/UD parameterised acceptance | timing (DT), dE/dx | "Detailed experimental analysis of backgrounds ... beyond the scope"; "deflection ... not included" [txt:561] |
| **2607.26195** FASER | E: (1,1,-1), N_IC = 2 | 300 eV < Lambda < 100 keV (limits 57-179 GeV, HEPData) | **MG5_aMC LO** + Pythia8 (LHCb tune, Z-pT reweighting to LHCb data); fiducial theta < 0.5 mrad | Athena causal string queue ("string vectors") in Geant4 for Lambda <= 3 keV; analytic transport above; validated by track continuity, charge (~2 MIP), timing | LHC magnet field maps | Geant4 standard EM processes | **eps = 0.1** (+-30 %) survival probability; relevant for Lambda > 30 keV | **full detector sim + data, 186 fb^-1**; no PU issue | scintillator charge + timing, ellipse fit | "first search ... charge +-1 colourless only"; ISR modelling "to which acceptance is particularly sensitive" [p.3] |
| **2410.00269** Sha et al. | fermion QQ + j, SU(N) generic | Lambda = 500 eV benchmark; scan | MG5_aMC + Pythia8 | Knapen-Papucci trajectory code (straight) | uniform B | **none: "neglecting matter interactions"** [txt:270] | none | 8- and 25-layer toy cylinders; **"No noise hits are included"** [txt:259]; mu = 1 | GNN (Exa.TrkX) reconstruction, efficiency 1-30 % across plane | "Effects from pile-up remain to be studied rigorously in future work" [Sec.VII]; generalisation across (m_Q, Lambda) "left to future work" |
| **2509.08878** Condren-Whiteson | model-agnostic smooth tracks | n/a | n/a | Schwartz-function curves, not quirk-specific | uniform | none | none | **mu = 1**, no noise, no misalignment | model-agnostic GNN tracking, efficiency up to 96 % on training class | "Future work includes more realistic samples, including hit noise models, misalignments, and hard radiation" [txt:582]; short tracks; combining segments |
| **2601.09023** Cid Vidal et al. (LHCb) | coloured fermion quirk, N_c = 2 | Lambda ~ 1 keV regime | MG5, LHCb | straight | **no B in VELO** | simplified: "100 % detection efficiency", material "accounting for specific energy loss mechanisms" deferred [txt:493-495] | none | VELO geometry hit generator, no trigger sim | planar back-to-back hit patterns, software trigger | "no dedicated trigger line exists; could be developed in 2026" [txt:439-440] |
| **2504.02940** Forsyth-Low et al. | scalar squirks, SU(2)_L doublet or singlet, SU(3)_QCD' | **sigma = 3.6 Lambda'^2** [txt:201]; m_0++ = 6.8 Lambda'; Lambda' ~ GeV (microscopic) | LO, Pythia | microscopic: bound state de-excitation | none | none | "We simply assume that glueballs are not radiated in the deexcitation" (conservative) [txt:333-335]; bound-state radiates gauge bosons | parton-level + simple cuts | resonance + displaced vertex (glueball) | glueball hadronisation "beyond the scope" |
| **2506.11192** Curtin et al. | dark quarks SU(3)_D, fundamental, from a heavy scalar decay | Lambda' ~ GeV; m_GB ~ 6 Lambda' | MG5 + Pythia8.2 | microscopic (l < 1/Lambda) | none | none | pion radiation modelled isotropic | simplified Delphes-based LHC detector [txt:243]; "No pile-up events were added" [txt:195] | soft unclustered track patterns, CATHODE | pile-up not included; "normalizing flow improvement" |
| **2512.20696** Asadi-Kribs (cosmology) | fermion, SU(2) benchmark (N >= 3 discussed) | **Lambda = T_c = 0.6 sqrt(sigma)** [txt:142]; ell ~ 1 cm (m/100 GeV)(Lambda/keV)^-2 [Eq.1] | n/a | n/a | n/a | n/a | n/a | n/a | T_RH <~ O(100) GeV bound | "bounds for larger Lambda ... leave for future work"; treats glueball relic abundance with ~ an order-of-magnitude uncertainty (supercooling) [txt:846] |

### 3B. Microscopic / bound-state / model-building / cosmology papers (not directly CMS-tracker relevant, audited for assumptions that propagate) - 14 papers

| Paper | Model | Lambda | What is assumed | Relevance / open problem |
|---|---|---|---|---|
| 0712.2681 Jacoby-Nussinov | coloured quirks, relic abundance | "scale much smaller than m" | late hadronic annihilation | only cosmology; no collider; superseded by 2512.20696 for EW quirks |
| 0907.4932 Nussinov-Jacoby | TeV neutral-EW coloured quirks | Lambda' >= 10 eV | cosmic-ray production, heavy isotopes in sea water | relic/bound-state constraints on *stable coloured* quirks; not followed up for EW-only quirks |
| 0909.2034 Kribs et al. (quirky DM) | chiral quirks, scalar baryon, SU(2)-doublets | Lambda_Q ~ 100 GeV (strong below EW) | Coulomb + log potential, asymmetric DM | collider stage deferred "to future work" [txt gaps]; chiral quirks not studied in central detectors |
| 0805.4667 Burdman et al. | scalar squirks, folded SUSY, via W+- | GeV, QCD0 | prompt squirkonium | resonance/multi-photon signals; "radiation of soft photons contributes a substantial part of the energy loss" |
| 0810.1524 Cheung et al. | uncoloured iquarks | Lambda' > MeV | bremsstrahlung rate ~ alpha Lambda'^4/M^3 | new to bibliography |
| 0810.3948 Harnik-Wizansky | squirks | GeV | calorimetric "antenna" pattern | new to bibliography; precursor of 2506.11192 |
| 0812.0843 Cai et al. | quirky little Higgs, top quirk | macroscopic strings in the model | model only | no collider simulation |
| 1012.2072 Martin | SUSY + unification: SU(2), SU(3), SO(3) | astronomical for SO(3) | qualitative | benchmark for Lambda from unification |
| 1106.3101 Fok-Kribs | chiral / vector-like quirkonia, alpha_ic ~ 0.2, Lambda ~ GeV | | analytic decay widths; "fraglueballs ... beyond the scope" | quirkonium decays only |
| 1512.05753, 1512.05775, 1604.06180, 1605.01937 | diphoton-era quirk/Q-onium models | GeV | prompt annihilation | dead with the excess (the 750 GeV excess disappeared); only methodology |
| 1512.05782 Chacko et al. | top partner quirks, neutral naturalness | GeV | Pythia HV glueball showers | displaced glueball decays; no macroscopic strings |
| 1410.6409 Quirks and strings attached | coloured quirks, Lambda' << keV in crystals | | transverse waves on the string transmit information | the only paper that treats *string wave propagation* (concept, not collider) |
| 2306.02542, 2756876 | SUSY vector-like quirks and W mass / g-2 | | low-energy EFT | irrelevant to detector signatures |
| 2606.30760 review | - | - | "certain aspects such as de-excitation via dark glueball radiation are non-perturbative and thus come with non-trivial uncertainties" [txt:1792-1795] | confirms epsilon is unconstrained |

Count: 19 + 14 = 33 papers audited in detail; plus 1710.06437, 0912.3339, 2204.13123, 2410.09164, 2205.06013, 2601.20063 opened for context (Sec. 5).

Tracker-relevant cross-tabulation (which assumption is made by which of the 9 central-detector propagation studies: 1703.00912, 1708.02243, 1811.08903, 1911.02223, 2002.07503, 2410.00269, 2509.08878, 2601.09023, plus FASER-like forward 2607.26195):

| Assumption | Papers making it | Papers relaxing it |
|---|---|---|
| uniform B | 1708.02243, 1911.02223, 2002.07503, 2410.00269, 2509.08878 | 1811.08903 (CMS map), 2607.26195 (magnet maps) |
| no material in EoM | 1703.00912, 1708.02243, 2410.00269, 2509.08878, 2601.09023 | 1811.08903, 1911.02223, 2002.07503 (mean dE/dx), 2607.26195 (Geant4) |
| mean dE/dx only, no stochastic effects (MCS, straggling, delta rays) | 1811.08903, 1911.02223, 2002.07503, 2108.06748, 2404.13814 | 2607.26195 only (Geant4 standard EM, not documented as validated for the string transverse impulse) |
| instantaneous straight string in CM | all except 2607.26195 (causal Athena queue) | 2607.26195 |
| LO production | 1703.00912, 1708.02243, 1911.02223, 2002.07503, 2410.00269, 2607.26195 | 2311.15486, 2404.13814 (NLO) |
| PU simulated | 1708.02243 (mu = 50), 1911.02223 (mu = 50) | none at PU 200 |
| time of flight of hits simulated beyond a 25 ns cut | none in central-detector papers | 2607.26195 (forward) |
| trigger simulated | 1708.02243 (MET efficiency only), 1911.02223 | none with L1/HLT realism |
| Primary vertex known | 1708.02243, 1911.02223, 2410.00269, 2509.08878 | none |

---------------------------------------------------------------------------------------------------
## 4. What the table says

### 4a. Assumptions shared by (almost) all studies and never tested

| # | Assumption | Who | Why it might matter for CMS Phase-2 | Status of test |
|---|---|---|---|---|
| S1 | **No stochastic material effects in the quirk EoM** (MCS, energy-loss straggling, delta rays, large-angle scatters); at most the mean dE/dx friction | all except FASER Geant4 (and there not validated for the string impulse) | the signal is a 10-100 um effect in a plane; MCS of a slow heavy particle is ~ 0.1-1 mrad per layer (ESTIMATE below) | not tested anywhere; Evans-Luty say "We have not attempted to model this effect" [1811.08903 txt:795]; Knapen "neglect" [1708.02243 Sec.II] |
| S2 | **Instantaneous straight string in the CM frame** (3 different implementations: CM-simultaneous [1911.02223 Eq.III.6-9], fixed s-hat [as assumed in some analyses, 2002.07503 Sec.VIII], causal queue [Athena]) | all | plane thickness changes from ~100 um to up to ~8 mm between true and fixed s-hat [2002.07503 Fig.6 right]; std dev of s-hat angle up to ~0.1 rad [Fig.6 left]. The observable is hypersensitive to the string model | the three variants have never been compared head-to-head in a published paper (INSPIRE: no hit) |
| S3 | Uniform B (2 T or "4 T"), no map; no B_r/B_z variation at |eta| > 1.8 | 1708.02243, 1911.02223, 2002.07503, 2410.00269 | the thickness formula is linear in B_xy [2002.07503 Eq.V.6-9]; the CMS map in the barrel differs by ~1 % (UNVERIFIED), endcap fringe field is larger | partly tested only by Evans-Luty (map) |
| S4 | Pile-up <= 50, never at 200; PU never combined with quirk-hit merging; Z(vv)+jets only in Li et al. | all central studies | hits per layer scale ~ x4 from PU 50 to 200; Knapen: ~1e-3 of events have a 4/8-layer plane at <mu> = 50, 6e-5 for a full plane [1708.02243 Sec.IV] and the number of random planes grows with the hit multiplicity. No tracker-timing (MTD) mitigation studied | not tested; 2410.00269 argues "no reason to suspect ... sensitive to pile-up" without a study |
| S5 | LO + parton shower for production; single ISR treatment; no PDF/scale uncertainties on pT(QQ) > 200 GeV tail | 1703.00912, 1708.02243, 1911.02223, 2410.00269, 2607.26195 (LO) | the MET trigger selects a tail (fraction ~ 0.10 above 200 GeV [1911.02223 App.A]). NLO changes rates by 1.2-1.5 and forward fraction by x2-3 [2404.13814, 2311.15486] | tested for forward only (2404.13814); never for the central MET-recoil tail |
| S6 | eps = 0.1 per classical crossing, one number for all Lambda, m_Q, charge | 1811.08903, 2404.13814, 2607.26195 | irrelevant in the tracker for Lambda <= 30 keV [signal model Sec.3.3], but sets FASER's high-Lambda edge | Kang-Luty's two extremes (1, ~1e-3) never implemented; range [0.01, 1] [2404.13814 Sec.6.4] |
| S7 | Primary vertex identified, hits at the pixel centre, no noise hits / misalignment (central ML studies) | 1708.02243, 2410.00269, 2509.08878 | at PU 200 with a MET-triggered event the hard vertex relies on the ISR jet only | untested |
| S8 | Quirk charge exactly +-1, equal masses, fermion singlet (or coloured with 30 % charged fraction) | nearly all | W-mediated production (charged + neutral partner), |q| = 2, scalar, splitting not covered (Sec. 4d) | partial: 2404.13814 (scalar), 2504.02940, 1106.2569 (doublets/triplets) |
| S9 | Lambda treated as a single sharp parameter; N_IC enters only through the rate | all | sigma is a function of N_IC and the representation: for N_IC >= 4 or non-fundamental IC reps, k-string tension ratios differ (Casimir scaling vs sine law) [0912.3339] | untested; see G-T5-8 |
| S10 | Hits of the two quirks are timing-neutral: only a 25 ns cut (Knapen, Li) | central studies | slow pairs (beta_T ~ 0.14 for m_Q >= 500 GeV) arrive out of time in the OT binary readout [signal model Sec.4.3] | only the forward FASER analysis uses timing |

### 4b. Open problems explicitly stated and their follow-up status

(Quotes verified in the cached text; "none" = no INSPIRE citer of that paper addresses it, judged from titles/abstracts of all citers that appear in `T5_census.json`.)

| Problem (paper) | Quote / location | Follow-up | Verdict |
|---|---|---|---|
| Parameter measurement (m_Q, Lambda) from hits | "this would also be an obvious way to try to measure the mass and string tension" [1708.02243 Sec.IV, txt:482-483]; "dE/dx will be important to measure the mass and string tension" [App.A]; Li et al. "We leave this for future work" [1911.02223 Sec.V] | **none**: no paper fits (m_Q, Lambda) from reconstructed hits; 2410.00269 reconstructs tracks only | OPEN (T4) |
| MET-direction / plane-normal correlation | "n3 is expected to be aligned with MET ... can limit the region of interest" [1708.02243 Sec.III.C] | none | OPEN |
| Dedicated HLT / L1 track-trigger quirk trigger | "We leave this possibility for future work" [1708.02243 Sec.III.B; fn.1: "future CMS and/or ATLAS hardware track triggers"] | 2601.09023 (LHCb software trigger concept); 2601.20063 (CMS L1 scouting for HSCP, not quirk) | OPEN for CMS Phase-2 |
| Pile-up (and noise) in ML tracking | "Effects from pile-up remain to be studied rigorously" [2410.00269 Sec.VII] | 2509.08878 at mu = 1, explicitly defers noise/misalignment | OPEN |
| Larger variety of quantum numbers, 0T data | [1703.00912 txt gaps] | quantum numbers: forward papers (2108.06748, 2404.13814, 2311.15486); 0T: none | partly |
| Annihilation position / decoherence simulation | "A proper treatment ... beyond the scope" [0805.4642 Sec.5] | stopping: 1811.08903; no decoherence MC | partly |
| dE/dx pattern as signal characterisation | [1911.02223 Sec.V], [1708.02243 App.A] | none | OPEN |
| Glueball radiation rate (eps) | "not calculable from first principles" [2404.13814 txt:513]; "non-perturbative ... non-trivial uncertainties" [2606.30760 txt:1792] | none (no lattice/EFT estimate in the quirk literature) | OPEN (T1/T2) |
| Hadronic/Higgs-portal glueball decay and cosmology | 2512.20696 "larger Lambda ... future work" | none | OPEN (T1) |
| Hit noise, misalignment, hard radiation, short tracks | [2509.08878 txt:582] | none | OPEN |
| High-Lambda unresolved regime at ATLAS/CMS | D0 only [1008.3547]; Farina-Low: "single highly-ionizing straight track" [1703.00912 txt:64] | FASER covers up to 100 keV in the forward region | OPEN centrally (G-T5-6) |
| Charged-state / electron stripping of slow positive quirk | [1811.08903 fn.2] | none | killed for the tracker (Sec. 7) |
| Annihilation vs Higgs/EW quantum numbers, chiral quirks in detectors | [0909.2034], [1106.3101] "leave this to future work" | none | OPEN, low priority |

### 4c. Internal inconsistencies between papers

| # | Quantity | Values | Size | Comment |
|---|---|---|---|---|
| I1 | Definition of "Lambda" | collider papers: Lambda^2 = sigma [1708.02243 Sec.II]; cosmology: Lambda = T_c = 0.6 sqrt(sigma) [2512.20696 txt:142]; Forsyth-Low: sigma = 3.6 Lambda'^2 [2504.02940 txt:201]; D0/Kang-Luty: "sigma ~ Lambda^2" | 0.6 vs lattice T_c/sqrt(sigma) = 0.597 + 0.45/N^2 [0912.3339 Eq.33] = **0.71 for SU(2)**, 0.65 for SU(3): the 0.6 is the N -> infinity value, wrong by 15 % in Lambda (28 % in sigma) for the N_IC = 2 benchmark; Lambda' = 0.527 sqrt(sigma) (x1.90) ESTIMATE (`T5_estimates.py` item 1) | the cosmology paper's own length formula [Eq.1] keeps the collider numerical coefficient "1 cm (m/100 GeV)(keV/Lambda)^-2" while defining Lambda = T_c: if taken literally the length is larger by 1/0.6^2 = 2.8 (1/0.71^2 = 2.0); a convention trap, not a physics error |
| I2 | Same benchmark, same observable: D^c = (3,1)_{2/3}, 300 fb^-1, coplanar | 1500 GeV [1708.02243 Fig.6] vs 2050 GeV [1911.02223 App.A, Fig.9] | +37 % in mass | Li et al.: "incorrect cross section ... Dc"; the LO pp -> D D j (pT(j) > 200) cross section exceeds the pp -> D D one for m > 500 GeV, i.e. K > 2; trigger efficiency 0.24 vs 0.10 for E^c. A 37 % mass difference at the edge of reach is a large factor in rate. It shows how fragile LO + shower ISR modelling is |
| I3 | E^c (EW) reach 300 fb^-1 | "650 GeV" (3-event contour) [1708.02243 abstract/Fig.6] vs "500 GeV" [1911.02223 App.A "coincides well"] | 30 % | probably 3-event (exclusion) vs 5-event (discovery) contour; not resolved: UNVERIFIED |
| I4 | Plane-thickness / plane-rotation scale | Knapen: Delta phi ~ 1e-5 [Eq.9], Fig.3 curves reach a few 1e-4 (text: "somewhat larger than 1e-5"); Li et al.: d_min = 1.16 um (m/100 GeV)(keV/Lambda)^4 (B_xy/T) [1911.02223 Eq.III.12]; for the Knapen benchmark (m = 1.8 TeV, Lambda = 2 keV, B = 2 T) Li gives 2.6 um, Knapen's Delta phi x amplitude (4.5 cm) gives 0.45-13 um | spread x30 inside one benchmark | no common benchmark validation; ESTIMATE (arithmetic from the quoted formulas) |
| I5 | Lambda windows of validity | Knapen: 100 eV - 30 keV (abstract) vs 100 eV - 10 keV (text); Li: 100 eV - 10 keV; FASER 300 eV - 100 keV; Farina-Low 1 - 100 eV; signal model (CMS coplanar) 0.6 - 15 keV | factor 3 at the upper edge | edges are set by pixel merging at high Lambda and by plane thickness (> 100 um) at low Lambda; CMS 3.8 T moves the lower edge up by ~ B x m_Q |
| I6 | NLO K-factor for E (EW singlet) | 1.33-1.45 [2404.13814 txt:314]; "(1.2-1.4) for all scenarios" [2311.15486 txt:1145] | 5-10 % | irrelevant by itself; but the signal model's own LO + K-factors from the SUSY xsec WG [research/theory_signal_model.md Sec.2] agree to this level |
| I7 | Magnetic field value for CMS | 3.8 T (real), "4 T" [2002.07503 Sec.II.C] | 5 % | thickness linear in B |
| I8 | Hypercharge conventions | E^c "(1,1,-2) in their Y-normalisation" [1911.02223 Eq.II.4] vs (1,1)_{-1} or (1,1)_1 elsewhere | none (same physical charge +-1) | trap when comparing quantum-number tables |
| I9 | eps ranges | +-30 % [2607.26195], [0.03, 0.3] and [0.01, 1] [2404.13814] | x10-100 | no principled range (Kang-Luty extremes ~1 and ~1e-3) |

### 4d. Regions of (m_Q, Lambda, charge, spin) not covered by any paper

Coverage in Lambda (central ATLAS/CMS, any lumi; "S" = dedicated simulation + analysis proposal; "R" = recast):

| Lambda (sqrt sigma) | Central ATLAS/CMS | Forward | Gap |
|---|---|---|---|
| < 100 eV | R: 1703.00912 (monojet/HSCP, 12.9 fb^-1; 150 GeV at 100 eV). **Full-Run-2 CMS HSCP [2410.09164] and ATLAS [2205.06013] not recast** | FASER down to 300 eV | recast of 2 existing searches |
| 0.1 - 0.6 keV | S: 1911.02223 (CMS coplanar + dE/dx, optimised at 1 keV), ML 2410.00269 at 500 eV; at CMS 3.8 T the coplanar thickness exceeds 100 um [signal model Sec.4] | FASER 57-113 GeV | trajectory-fit / GNN studies at PU 200 absent |
| 0.6 - 15 keV | S: 1708.02243, 1911.02223 | FASER 113-179 GeV | PU 200, trigger, timing |
| 15 - 100 keV | **none** | FASER 173-179 GeV; Feng projection | single straight, ~2 MIP-like pair with beta < 1: central HSCP-like search with MTD/dE/dx not studied |
| 100 keV - few MeV | D0 only (10 keV - 1 MeV, m < 107-133 GeV) | - | unresolved regime; also annihilation lifetime question (10 cm (Lambda/MeV)^-3 (m/TeV)^2 [0805.4642 Eq.6.5]) |
| >= GeV | resonance / displaced glueball: 1512.05782, 2504.02940, 2506.11192 | - | out of scope |

Coverage in quantum numbers and spin:

| Region | Covered by | Not covered |
|---|---|---|
| fermion (1,1)_{-1}, N_IC = 2 | everything | N_IC > 2 only as rate factor |
| scalar (1,1)_{-1} | 2108/2311/2404 (forward), 2504 (squirks) | central coplanar: none (rate 10-18 x smaller than fermion; signal model) |
| (1,2) doublet fermion: pair production via W gives a charged + a **neutral** quirk | 1106.2569, 2504.02940 (beta-decay) | no central-detector study: pair with one neutral member leaves only half the hits (plane undefined) while beta-decay of the charged member may produce kinks [signal model Sec.1.3] |
| |q| = 2 or higher, fractional charges | none | DY rate ~ q^2, thickness ~ q, dE/dx ~ q^2 |
| chiral quirks, mass from EWSB (m ~ O(100) GeV with Higgs couplings) | 0909.2034, 1106.3101 (bound state/decay) | strings + detector: none; Higgs-portal effects on glueballs irrelevant |
| IC representation other than fundamental / N_IC >= 4 | none | k-string tensions differ; "Lambda" ambiguous |
| masses < 100 GeV | LEP excluded | - |
| masses > 1.5 TeV | tiny rates | - |

---------------------------------------------------------------------------------------------------
## 5. Adjacent theory the quirk literature has not used (concrete papers)

All items below are pointers verified to exist on INSPIRE (title, authors checked) but, unless stated, not read in detail (UNVERIFIED content).

1. **Lattice string tension, T_c/sqrt(sigma), glueball spectrum, flux-tube width, NG accuracy.**
   - M. Teper, "Large N and confining flux tubes as strings - a view from the lattice", 0912.3339 (opened): T_c/sqrt(sigma) = 0.597(4) + 0.45(3)/N^2 [Eq.33]; NG describes "remarkably well" the closed-flux-tube spectrum even for short tubes; "a significant minority of states that behave quite differently" in D = 3+1 (the pseudoscalar worldsheet state, see next item). Only 2504.02940 among quirk papers cites it, and only for sigma/Lambda'^2 = 3.6.
   - Athenodorou, Bringoltz, Teper, closed flux tubes in D = 3+1 SU(N): 1007.4720 (not opened).
   - Lucini, Teper, Wenger: deconfinement T_c / sigma, SU(N), hep-lat/0502003 (abstract checked: SU(2) second order, no numerical T_c/sqrt(sigma) on the abstract page).
   - Use: precise sqrt(sigma) <-> T_c <-> glueball mass maps for N_IC = 2, 3, 4 (fix I1), and an input for any attempt to compute eps (T1/T2).
2. **Effective string theory (Luscher term, corrections to NG, worldsheet axion).** Luscher-Weisz hep-lat/0207003 (cited by 1911.02223 as the NG justification; one reference only); Aharony-Komargodski 1302.6257 ("effective theory of long strings": deviations from NG are suppressed by high powers of 1/(sigma R^2); exponent UNVERIFIED); Dubovsky-Flauger-Gorbenko 1301.2325 (massive axion on the worldsheet), 1205.6805, 1404.0037. **Killed for propagation** (Sec. 7) but relevant for the *crossing* regime r ~ 1/Lambda (radiation), where NG fails and where the open-string-to-closed-string (glueball) emission amplitude lives.
3. **String breaking absence.** Lattice evidence with dynamical quarks: Bali et al. hep-lat/0505012 (SESAM, string breaking observed); for pure-glue (no light matter) the string cannot break by quark pair creation, and the Schwinger-type estimate Gamma ~ exp(-pi m_Q^2/sigma) in [0805.4642 Eq.3.2] is ~ exp(-1e17) (ESTIMATE for m_Q = 100 GeV, Lambda = 1 keV: pi m^2/sigma = pi 1e22 eV^2/1e6 eV^2 ~ 3e16). Nobody has asked whether *glueball emission by string pinching* (open to closed) gives a non-exponentially suppressed breaking in SU(2); the large-N counting (1/N^2) suggests rates ~ eps-like; this is exactly the eps problem.
4. **Heavy-quark physics in the QCD analogue / Lund string.** The Lund string with massive ends (yo-yo mode) is the same classical object as the quirk pair; Pythia's hadronisation code treats the causal string (Artru-Mennessier, Andersson et al.; UNVERIFIED citation details). Pythia8's Hidden-Valley module with heavy dark quarks (Carloni-Sjostrand 1006.2911, in `T5_census.json`) has the string-fragmentation machinery but no quirk transport; nobody has used Pythia's string-region (causal) bookkeeping to cross-check the straight-string approximation.
5. **Rotating strings with massive endpoints** (Regge phenomenology, Sonnenschein et al. 1602.00704, review; UNVERIFIED): conserved angular momentum and endpoint-mass corrections; relevant to G-T5-2 for the B-field-induced angular momentum (L ~ 1e12 hbar).
6. **HSCP / monopole transport and simulation** (the closest propagation analogues):
   - Heavy stable hadron interactions in matter: Kraan hep-ex/0404001; Mackeprang-Rizzi hep-ph/0612161 (R-hadron nuclear interactions; energy loss and charge flipping, relevant to coloured quirks only).
   - Monopole / multi-charged object search with full Geant4 in a magnetic field: ATLAS 1905.10130; CMS HSCP Run-2 2410.09164 (large dE/dx), ATLAS 2205.06013; CMS HSCP with L1 scouting 2601.20063 (trigger idea). The monopole equations of motion in a field are implemented in Geant4 (Mermod; UNVERIFIED reference) and in `SimG4Core`; they are the structural template for a quirk transportation in CMSSW (signal model Sec.3.5).
7. **Cosmic strings from pure Yang-Mills**, Yamada-Yonekura 2204.13123: formation of macroscopic colour flux tubes at the deconfinement transition; relevant to IC cosmology (T1) and to the 2512.20696 phase transition discussion.
8. **Glueball dark matter / dark sector cosmology** used by 2512.20696: Soni-Zhang 1602.00714, Forestell-Morrissey-Sigurdson 1605.08048 (UNVERIFIED id), Juknevich et al. 0903.0883. These give N_IC- and Lambda-dependent glueball lifetimes needed to turn the BBN/CMB bounds into constraints on (m_Q, T_RH).

---------------------------------------------------------------------------------------------------
## 6. Gap entries (ranked)

Ranking is by expected value for the CMS Phase-2 search (constraint or discovery power, publishability), weighted by confidence. Numbers marked ESTIMATE come from `code/T5_estimates.py` unless stated.

### G-T5-1  Multiple scattering / straggling of a slow heavy quirk is absent from every published quirk propagation   [rank 1; flag T3, T4]
- **Current treatment.** Central-detector studies either ignore matter entirely in the EoM [1708.02243 Sec.II "neglect"; 2410.00269 txt:270; 2509.08878; 2601.09023] or include only the mean dE/dx friction with a 10 % Gaussian smear [1911.02223; 2002.07503 Sec.VII; 1811.08903 "continuous friction approximation", App.B "momentum transfer transverse ... We have not attempted to model this effect"]. The mean friction is a force along v; MCS and delta-ray recoils kick the quirk transversally.
- **Why it is a gap.** The target observable is a plane with thickness 10-100 um, i.e. angular deviations of 1e-4 over tens of cm. A heavy quirk has small beta, so its MCS angle is large: theta_0 = 13.6 MeV/(beta c p) sqrt(x/X0)(1 + 0.038 ln(x/X0)) with beta c p = m beta^2 gamma. Knapen's own ionisation torque argument gives Delta phi ~ 1e-3 per layer and is then dropped [1708.02243 Sec.II].
- **Estimate (ESTIMATE, `T5_estimates.py` item 2).** x/X0 per layer 1-3 % is an ASSUMPTION (UNVERIFIED for the Phase-2 IT/OT; to be replaced by T3 with the real material map). One kick on a single quirk rotates the CM direction by theta/2, so later hits leave the plane through the origin by (theta/2) Delta R. Upper-bound rms at the outer layer (10 layers, R = 5-100 cm):

  | m_Q (GeV) | beta_q | x/X0 = 1 % | x/X0 = 3 % |
  |---|---|---|---|
  | 200 | 0.1 / 0.2 / 0.4 | 497 / 122 / 29 um | 905 / 223 / 52 um |
  | 500 | 0.1 / 0.2 / 0.4 | 199 / 49 / 11 um | 362 / 89 / 21 um |
  | 1000 | 0.1 / 0.2 / 0.4 | 99 / 24 / 6 um | 181 / 45 / 10 um |

  A free plane fit absorbs part of this (factor ~ 0.3 UNVERIFIED), so the effect is O(10-100 um) for beta_q ~ 0.1-0.2 and m_Q >= 500 GeV: the same size as the Knapen cut Delta s < 100 um [1708.02243 Fig.5] and as the signal's intrinsic thickness [1911.02223 Eq.III.12: ~ 1-100 um].
- **How to exploit.** (c) Reconstruction: the plane-finder cuts (thickness, hit window) and the GNN training set must include MCS, otherwise the efficiency map (Knapen Tab.I, Sha) is optimistic exactly in the slow/heavy corner that carries the reach; (e) signal systematic: MCS modelling is a new source of efficiency uncertainty; (d) measurement: m_Q ~ B l^2/d from [2002.07503 Eq.V.6] (ESTIMATE, dimensional) requires the thickness d to be known against an MCS floor, so MCS limits the (m_Q, Lambda) measurement (links to G-T5-7); (f) a short paper "multiple scattering of quirks" is publishable.
- **Effort / confidence.** Days for a Python toy (add Gaussian kicks to the straight-string propagator); weeks for a Geant4 check with the Athena `Quirks` package (which should include MCS if `G4hMultipleScattering` is attached; verify). Confidence medium (the x/X0 and the plane-fit absorption factor are the weak points).
- **Verdict: EXPLOIT** (cheap, and it can only change the efficiency map in a known direction).

### G-T5-2  The plane thickness is hypersensitive to the string-direction model; instantaneous straight string vs causal string vs fixed s-hat is untested   [rank 2; flag T2, T3]
- **Current treatment.** Straight string in the CM frame with simultaneity [1911.02223 Eq.III.6-9; 2002.07503 Eq.VIII.1-4; 1811.08903 Sec.2: "retarded time corrections ... can also be safely neglected"]. Athena `InfracolorForce` uses a queue of string vectors (causal string) and is what FASER used, but no paper compares it with the straight version. [2002.07503 Fig.6]: true s-hat varies by sigma(s-hat) up to ~ 0.1 rad along a trajectory; replacing it by a fixed s-hat changes the thickness "dramatically" from ~ 100 um up to several mm.
- **Why it is a gap.** Thickness ~ 1e-4-1e-3 of the amplitude, so the model error needed to flip the answer is tiny. Light-crossing time of the string vs the time a quirk spends in a sensor (ESTIMATE, item 4): for Lambda = 1 keV, m_Q = 500 GeV: 167 ps vs 7 ps (300 um Si, beta = 0.14); F_ion/Lambda^2 = (90 eV)^2/Lambda^2 = 0.8 % at 1 keV, 9 % at 300 eV. So the ionisation impulse in each sensor is a transient that the partner "sees" 20x later; the straight-string approximation lets it respond instantly. The Kang-Luty criterion F_ext << Lambda^2 [Eq.3.10] says nothing about the *time structure*.
- **Estimate.** First-order effect on the thickness is ~ (F_ion/Lambda^2) x (O(1) retardation factor) x the ionisation-induced thickness; negligible at Lambda >= 1 keV (<1 %), possibly 10 % at 0.3 keV. At the same time the B-field-induced thickness (the signal) is itself only 1e-3 of the string force at 1 keV (15 eV vs 1 keV: 2e-4). The ratio test must be made with a propagator, not by inspection.
- **How to exploit.** (c) A validated propagator for the trajectory fit (T4); (e) systematic on the signal efficiency at Lambda <= 0.5 keV, where ML/trajectory methods are needed anyway; (f) paper "validation of the quirk equation of motion: straight vs causal string" with the Athena code and an independent finite-difference string.
- **Effort / confidence.** 1-3 weeks (PDE for a NG string with massive ends in 1+1D plus transverse kicks); confidence medium.
- **Verdict: WORTH A CHECK** (EXPLOIT if the 0.3 keV edge turns out sensitive).

### G-T5-3  Pile-up 200 and hit-level realism have never been simulated for any quirk tracker analysis   [rank 3 on experimental side; flag T4 and Phase 2]
- **Current.** <mu> = 50 [1708.02243, 1911.02223], mu = 1 [2509.08878], none [2410.00269, 2601.09023 "100 % detection efficiency"]. Knapen's background: 1e-3 of events contain a plane with >= 1 hit in 4 of 8 layers, 6e-5 for a full plane at <mu> = 50 [Sec.IV], using "O(1000) unassociated pile-up hits per layer".
- **Gap.** Random-plane probability grows with hit density per layer (about x4 from mu 50 to 200 in the same geometry; the Phase-2 detector has a different granularity, so the real number needs a simulation: UNVERIFIED), and nobody has quantified it. The MTD and the OT BX tagging were never used as handles.
- **Estimate.** Not computed by T5 (needs hit-level MC); flagged because the claim "quirks should not be sensitive to PU" [2410.00269 Sec.VII] is an assumption, not a result.
- **Exploit.** (b)/(c): timing (MTD, 30-40 ps) to reject PU hits; require plane-hit time consistency; (e) data-driven random-plane background from rotated/reflected hits.
- **Effort / confidence.** Phase-2 sample plan; weeks; confidence high that it is needed.
- **Verdict: WORTH A CHECK** (belongs to the experimental Phase 2).

### G-T5-4  Lambda convention hygiene   [rank 6, but zero cost; flag T1]
- **Current.** Collider: Lambda^2 = sigma [1708.02243 Sec.II]; cosmology: Lambda = T_c = 0.6 sqrt(sigma) [2512.20696 txt:142]; Forsyth-Low sigma = 3.6 Lambda'^2 [2504.02940 txt:201].
- **Gap.** 0.6 is the N -> infinity value of T_c/sqrt(sigma) = 0.597 + 0.45/N^2 [0912.3339 Eq.33]; for the N_IC = 2 benchmark it is 0.71, so converting a cosmology result quoted as Lambda_cosmo = T_c to sqrt(sigma) with 0.6 instead of 0.71 mis-states Lambda by 15 % (sigma by 28 %) (ESTIMATE, item 1). Lambda' (Forsyth-Low) = 0.527 sqrt(sigma). The ell formula in 2512.20696 Eq.1 keeps the collider coefficient.
- **Exploit.** (e)/(a): state "Lambda = sqrt(sigma)" in the CMS note; give conversion table for N_IC = 2, 3, 4; use lattice-based T_c/sqrt(sigma) and m_0++/sqrt(sigma) = 3.6 (SU(3)) [0805.4642 txt:1567; 2504.02940 txt:201-202 consistent] to translate cosmology (T1).
- **Effort / confidence.** hours; high. **Verdict: EXPLOIT** (as bookkeeping).

### G-T5-5  Central production modelling: LO + shower ISR tail, K-factors, matching   [rank 5; flag T6]
- **Current.** LO + MLM (<= 1 jet) with a pT(QQ) > 200 GeV cut [1708.02243 Sec.III.A]; Li et al. LO + trigger efficiency 0.10 (EW) / 0.24 (coloured) vs their own K > 2 for coloured [1911.02223 App.A]; NLO only for forward studies [2404.13814 txt:312-316: K = 1.33-1.45 for E, forward fraction x2-3 with NLO].
- **Gap.** The MET trigger selects the tail of pT(QQ) where fixed-order + shower modelling is not under control; I2 (Sec. 4c) shows a 37 % mass-reach spread between two groups on the same model from this alone. FASER, which has data, had to reweight Pythia's ISR to LHCb Z data [2607.26195 p.3] "to which the FASER signal acceptance is particularly sensitive". Nobody has estimated the analogous uncertainty for central ATLAS/CMS.
- **Estimate.** Not recomputed (T6). Direction: the signal model already finds sigma x3 higher than Gate-4 [research/theory_signal_model.md Sec.0.2], so more events at fixed efficiency, but the MET-recoil fraction (0.10 above 200 GeV [1911.02223 App.A]) carries the largest uncertainty.
- **Exploit.** (e) reduced signal systematic: NLO+PS (FxFx / MC@NLO) vs LO MLM vs Pythia ISR for pT(QQ) in 150-400 GeV, scale/PDF envelope; a DY-like Z(vv)/Z->mumu control region to reweight ISR as FASER did.
- **Effort / confidence.** 1-2 weeks; high. **Verdict: EXPLOIT** (T6).

### G-T5-6  Unresolved high-Lambda regime (15 keV - 1 MeV) has no ATLAS/CMS result since D0 2010, and existing Run-2 high-dE/dx searches were not recast   [rank 3 for physics; flag T6]
- **Current.** D0 [1008.3547]: m_Q > 107/119/133 GeV (N = 2/3/5), Lambda = 10 keV - 1 MeV. Farina-Low [1703.00912 txt:64]: "10 keV < Lambda < 1 MeV ... a single highly-ionizing straight track". Coplanar searches stop at pixel merging (~ 5-30 keV, Knapen Tab.I). FASER excludes up to 173-179 GeV at 30 keV. CMS 2410.09164, ATLAS 2205.06013 (Run-2 large dE/dx) and CMS 2601.20063 do not cite quirk papers (INSPIRE references) and have no quirk interpretation.
- **Gap.** For Lambda >~ 15 keV the pair amplitude l = 1 cm (m/100 GeV)(keV/Lambda)^2 is below the pixel pitch (~ 0.3 mm at 30 keV for 100 GeV, 55 um for 500 GeV): the pair is a neutral, straight, ~ 2 x MIP / beta^2 track, with beta < 1 (MTD time-of-flight available at HL-LHC), without bending in B. Standard HSCP track-fit / momentum-based mass estimators assume curvature and Q = +-1; their response to a neutral pair of two charges is not documented.
- **Estimate.** No calculation by T5. The parameter region is ~ 1.5 decades of Lambda (15-500 keV) x m_Q = 150 GeV - TeV; DY rates are the same as for the coplanar case [signal model Sec.2]; B-induced angular momentum is irrelevant (ESTIMATE item 3: d_min Lambda < 1 above 10-30 keV, so glueball emission eps can matter at the upper end).
- **Exploit.** (a) new/stronger constraint from a recast of CMS 2410.09164 (Phase-1) and a Phase-2 projection with MTD + dE/dx; (b) new signature "neutral straight double-ionisation track with beta < 1"; (f) pheno paper. 
- **Effort / confidence.** 2-4 weeks for a parametric recast; medium (the HSCP selection acceptance for neutral pairs is the unknown).
- **Verdict: EXPLOIT** (as a complementary Phase-2 analysis region, upper Lambda edge).

### G-T5-7  Parameter measurement (m_Q, Lambda) after discovery was never demonstrated   [rank 4; flag T4]
- **Current.** Stated as desirable [1708.02243 Sec.IV, App.A; 1911.02223 Sec.V "leave this for future work"]. FASER/Feng: timing, dE/dx but no (m_Q, Lambda) fit. No paper quotes a resolution. 
- **Gap.** The analytic relations [2002.07503] give amplitude l ~ m_Q/Lambda^2, period number ~ L_tracker Lambda^2 / (v gamma m_Q), thickness d ~ m_Q q B/Lambda^4, hence m_Q ~ B l^2 / d and Lambda^2 ~ m_Q / l (ESTIMATE, dimensional analysis from [2002.07503 Eq.V.6, II.4]). Three observables -> two parameters plus kinematics.
- **Estimate.** Not computed; the thickness measurement competes with MCS (G-T5-1) and hit resolution; only "within one order of magnitude" analytics [2002.07503 Sec.IX]. A trajectory fit with the full EoM (T4) is the way.
- **Exploit.** (d) measurement; (b) a combined fit also improves the plane-finder (seed from the fit); (f) publishable.
- **Effort / confidence.** weeks-months; medium. **Verdict: EXPLOIT** (T4).

### G-T5-8  Model-space holes: doublet/W-production, |q| >= 2, chiral/split states, other IC representations, N_IC >= 4   [rank 7; flag T6]
- **Current.** Central tracker studies: singlet fermion and (3,1) coloured fermion only. Doublets: 1106.2569 (scalar), 2504.02940 (beta-decay formulas, App.A.1), signal-model caveat that the charged member beta-decays on mm-cm. Chiral quirks: 0909.2034, 1106.3101 (bound states, no strings).
- **Gap and estimate.** (i) W-mediated production gives a charged + a neutral quirk: only one quirk leaves hits, no plane; the string with a neutral partner still affects the charged quirk's trajectory (unstudied). (ii) |q| = 2: DY rate x4 at fixed mass, plane thickness x2 [2002.07503 Sec.V.A], dE/dx x4: a stronger-signal region studied nowhere. (iii) IC representation: k-string tension ratio vs fundamental: Casimir scaling k(N-k)/(N-1) or sine law sin(k pi/N)/sin(pi/N) (UNVERIFIED, from the lattice k-string literature cited in [0912.3339]); "Lambda" = sqrt(sigma_fund) would no longer be the force scale.
- **Exploit.** (b) new signatures; (f) pheno paper. **Effort** days (rate scaling) to weeks (neutral-partner kinematics); medium. **Verdict: WORTH A CHECK** (|q| = 2 and doublet cases are cheap).

### G-T5-9  Trigger: only the MET-from-ISR path has been considered; stub/L1 track-trigger and L1 scouting are unexplored   [rank 5 experimental; flag Phase 2]
- **Current.** MET trigger, eps_trig ~ 0.1 for DY at 800 GeV (Knapen Tab.I via C001 review); "dedicated trigger ... future work"; fn.1 mentions hardware track triggers [1708.02243]; LHCb proposes a software trigger [2601.09023 txt:431-440]; CMS L1 scouting for HSCP exists [2601.20063] but not for quirks.
- **Gap.** The trigger efficiency (0.1-0.24) is the largest single efficiency factor; at HL-LHC thresholds rise [1708.02243 Sec.III.B]. Whether OT stubs form for oscillating quirks (two quirks in the stub window) is "untested" [signal model Sec.3.5].
- **Exploit.** (b) new trigger: L1 track-trigger stubs/hit-multiplicity in a narrow rho-phi sector + muon-system late hits, or scouting; (a) the signal rate would gain up to x5-10 if the 0.1 efficiency could be raised toward 0.5-1 (upper bound, not an estimate of what is achievable; the ISR-tail fraction above 200 GeV is ~ 0.10 [1911.02223 App.A]).
- **Effort / confidence.** months (needs L1 emulation); low-medium. **Verdict: WORTH A CHECK** (experimental).

### G-T5-10  Unused kinematic correlation: strip axis aligned with MET in phi   [rank 8; flag T4]
- **Current.** Mentioned, not used: "n3 is expected to be aligned with E_T^miss ... can limit the region of interest" [1708.02243 Sec.III.C]; no follow-up.
- **Estimate.** Random PU planes have uniform strip azimuth; a |Delta phi| < delta window keeps ~ delta/pi (ESTIMATE, geometry): factor 5 for delta = 0.6, 10 for 0.3 rad, with the plane containing the pair momentum, which carries the recoil direction. Also reduces the O(N) hit-seeding region of interest [Sec.III.C], which was the algorithm-latency concern.
- **Exploit.** (c)/(b): extra background rejection, and a trigger-level seed. **Effort** days; high. **Verdict: WORTH A CHECK**.

### G-T5-11  eps prescription (glueball emission per crossing)   [rank 9 for CMS; relevant for FASER and for T1/T2]
- **Current.** eps = 0.1 per classical crossing [1811.08903 Eq.B.3; 2404.13814 Sec.4; 2607.26195 p.3]. Kang-Luty offered two extremes (1 or ~1e-3) [0805.4642 txt:1565-1575]; the 2404.13814 range [0.01, 1] brackets them.
- **Why / estimate.** Emission needs a closest approach d_min <~ 1/Lambda. With the B-induced angular momentum of the pair (Knapen scaling Eq.5-7, 3.8 T, m_Q = 500 GeV, v = 0.3, v_cm = 0.14; ESTIMATE item 3): d_min Lambda = 3.1e3 (1 keV), 1.1e2 (3 keV), 3 (10 keV), 0.11 (30 keV), 3e-3 (100 keV). So B-induced L suppresses emission only for Lambda <~ 10 keV, where eps is irrelevant (<= 3 MeV radiated in the CMS tracker [signal model Sec.3.3]); where eps matters (30-100 keV) the classical closest approach is below 1/Lambda and eps ~ O(0.1-1) is the plausible regime. One period only: accumulation of L over 480 m (FASER) not computed.
- **Exploit.** Not for the CMS tracker (irrelevant). For FASER-regime constraints a derivation of eps from the open-to-closed-string emission amplitude in large-N (1/N^2) would remove the +-x10 band (a) and produce the N_IC dependence (T1/T2).
- **Verdict: NOT A GAP FOR CMS-TRACKER (killed there); WORTH A CHECK as a theory item for T1/T2.**

### G-T5-12  Timing of hits (slow pairs out of time) is modelled only in forward searches   [rank 4 experimental; flag T4, already in signal model]
- **Current.** Knapen/Li impose a 25 ns cut; the signal model shows beta_T = 0.14 median for m_Q >= 500 GeV and pT(QQ) = 250 GeV, arrival ~ 16 ns late at the outer OT. FASER uses timing as the main discriminator.
- **Gap.** No central paper simulates per-hit time vs the bunch-crossing assignment of a binary OT and the MTD.
- **Exploit.** (b)/(c) timing seed, PU-hit rejection, and mass estimator from beta. **Verdict: EXPLOIT** (already identified; this audit confirms no literature treatment exists).

### G-T5-13  Weakly motivated lower-priority items
- **Detector geometry: only barrel**; endcaps, forward Phase-2 (|eta| < 4) never treated [1708.02243 Sec.III.A]. Verdict WORTH A CHECK (acceptance gain), low theory content.
- **Quirk-quirk Coulomb/EM interaction between opposite charges at separation d ~ 0.1-10 um**: ~ alpha/d = 1.4 eV um/d; compared with the string energy sigma d: ratio alpha/(sigma d^2) = 7.3e-3/(1e6 eV^2 x (5.07 eV^-1)^2) = 3e-10 at d = 1 um, 3e-8 at d = 0.1 um for Lambda = 1 keV (ESTIMATE) -> **NOT A GAP**.

---------------------------------------------------------------------------------------------------
## 7. Killed ideas (with the number that kills them)

| Idea | Killing number |
|---|---|
| Effective-string (Luscher) corrections change the propagation | relative correction to the linear potential pi(D-2)/(24 r) / (sigma r) = 0.26/(Lambda r)^2 (static-source formula, D = 4): 1e-8 at r = 1 um, Lambda = 1 keV; 1e-5 at r = 0.1 um, Lambda = 300 eV; 1e-9 at 3 keV (ESTIMATE, direct arithmetic). The minimum separation reached in a B field is d_min ~ 0.6 um at 1 keV (item 3). NG is exact for the purposes of propagation; the region where NG fails (r <~ few/Lambda) is only visited in the crossing, i.e. it matters for eps (G-T5-11), not for tracks |
| String breaking by q qbar creation | Gamma/L ~ sigma exp(-pi m^2/sigma) [0805.4642 Eq.3.2]: exponent pi m^2/sigma = 3e16 for m = 100 GeV, Lambda = 1 keV (ESTIMATE). Breaking by glueball emission is a separate (eps) question |
| Quirk-quirk Coulomb attraction modifies the string dynamics | alpha/(sigma d^2) = 3e-10 (1 um) to 3e-8 (0.1 um) at Lambda = 1 keV (ESTIMATE) |
| Electron stripping / charge exchange of a slow quirk [1811.08903 fn.2] | needs beta <~ 0.01 (Bohr velocity 0.0073 c); lab beta of each quirk >= beta_cm ~ 0.1 in the triggered sample; relevant only to stopped quirks (Lambda <~ 150 eV, outside the tracker target) |
| EM (Larmor) radiation from the oscillating dipole | E_EM ~ 1.7e-7 alpha (Lambda/100 eV)^4 eV over 480 m [2108.06748 Eq.4.22]; far smaller in the 1 m tracker |
| B-induced angular momentum kills glueball emission where it matters | d_min Lambda = 3 at 10 keV, 0.11 at 30 keV (item 3): the suppression exists only below ~ 10 keV where eps is irrelevant anyway (one-period estimate) |
| Missing hadronic/nuclear energy loss for uncoloured EW quirks | uncoloured singlet has no SM-strong interaction; excluded by construction [2108.06748 txt:256-260 for R-hadron coloured case] |
| Uniform vs real B in the CMS barrel | thickness is linear in B_xy; barrel field map differs from uniform by ~ 1 % (UNVERIFIED), so < 1 % effect; check only for |eta| > 2 |

---------------------------------------------------------------------------------------------------
## 8. Open questions for other workstreams

- **T1 (Lambda origin and cosmology).** (i) Use N_IC-dependent lattice conversions (T_c/sqrt(sigma) = 0.71 for SU(2), 0.65 for SU(3); m_0++/sqrt(sigma) = 3.6 for SU(3), 4.7 for SU(2)? UNVERIFIED) to restate the 2512.20696 bounds in sqrt(sigma). (ii) Is there any first-principles estimate of eps (open-to-closed string emission, 1/N^2 counting)? (iii) 2204.13123 (cosmic strings from YM) and cosmological production of IC strings: any relic macroscopic strings? (iv) Does a discovery at Lambda = 1 keV require T_RH < ~ 100 GeV in the SU(2) benchmark with the corrected 0.71?
- **T2 (vacuum string dynamics).** Implement the three string models (CM-straight with simultaneity, causal queue as Athena, fixed s-hat) in one propagator and compare thickness and hit patterns (G-T5-2). Add the stochastic transverse kicks (G-T5-1) as an optional module. Evaluate the glueball-emission amplitude eps vs d_min Lambda (G-T5-11).
- **T3 (propagation in B and matter).** Replace my x/X0 = 1-3 % per layer by the Phase-2 material map; compute MCS-induced plane thickness with a plane fit (the absorption factor 0.3 is a guess); test the Knapen Delta phi (Eq.9 vs Fig.3) and Li's thickness formula against a numerical benchmark (I4). Also ionisation-torque per layer (Knapen: 1e-3).
- **T4 (trajectory model and parameter measurement).** The relation m_Q ~ B l^2/d (G-T5-7) and its MCS floor; use Delta phi(MET, strip axis) (G-T5-10) as a seed; check which of the three parameters (l, N_periods, d) carry information about (m_Q, Lambda) at 3.8 T with 10-100 um hit resolution.
- **T6 (production and model space).** NLO+PS vs LO+MLM for the pT(QQ) > 150-250 GeV tail; K-factor discrepancy I2; |q| = 2, doublet (W-production), scalar cases (G-T5-8); parametric recast of the CMS Run-2 high-dE/dx HSCP search for the unresolved regime (G-T5-6).
- **Experimental Phase 2.** (i) PU-200 hit-level background for a plane finder with MTD timing; (ii) per-hit time vs BX assignment for slow pairs; (iii) stub formation for oscillating quirks at L1; (iv) a neutral double-ionisation straight-track category for Lambda > 15 keV; (v) which of the plane-finder cuts (thickness 100 um) must be re-derived once MCS is included.

---------------------------------------------------------------------------------------------------
## 9. References opened (arXiv ids; what was used)

Fully or substantially read (cached text): 0805.4642 (EoM, eps extremes, B field, lattice remarks, string breaking Eq.3.2); 1708.02243 (model, torque estimate, trigger, PU, results, App.A); 1911.02223 (simulation, Z+jets, comparison with Knapen App.A); 2002.07503 (Sec.I, VIII, IX; fixed vs true s-hat); 1811.08903 (straight string, App.B friction/transverse kicks, fn.2); 2108.06748, 2404.13814 (propagation, K-factors, eps ranges); 2607.26195 (FASER search description); 2410.00269, 2509.08878 (idealisations and stated future work); 2504.02940 (sigma = 3.6 Lambda'^2, glueball assumptions); 2506.11192 (Delphes, no PU); 2512.20696 (Lambda = T_c, Eq.1, lattice use); 2601.09023 (LHCb simplifications); 1703.00912 (Lambda regimes, 0T proposal); 1008.3547 (D0 regime and Lambda); 0912.3339 (Teper review: Eq.33, NG spectrum); 2606.30760 (review passage on quirks, txt:1779-1810).
Partially read / abstract and grep only: 0805.4667, 0810.1524, 0810.3948, 0812.0843, 0907.4932, 0909.2034, 1012.2072, 1106.2569, 1106.3101, 1512.05753, 1512.05775, 1512.05782, 1605.01937, 1604.06180, 1410.6409, 2311.15486, 1710.06437, 0712.2681, 2204.13123 (abstract only).
Existence verified on INSPIRE but not read: 1302.6257, 1301.2325, 1404.0037, 1205.6805, hep-lat/0207003, hep-lat/0505012, hep-lat/0502003 (abstract page only), 1602.00704, 1007.4720, 1905.10130, 2410.09164, 2205.06013, 2601.20063, hep-ph/0612161, hep-ex/0404001, 1609.08382.
Not verified (recalled): Forestell-Morrissey-Sigurdson 1605.08048; the Lund-model references; Mermod's monopole Geant4; the lattice k-string tension laws; m_0++/sqrt(sigma) for SU(2).

---------------------------------------------------------------------------------------------------
## Appendix A. INSPIRE queries and hit counts (`code/T5_census.py`, size 100, sort mostrecent; full log in `outputs/T5_queries.txt`)

| # | tag | query | hits |
|---|---|---|---|
| 1 | Q | `t quirk*` | 34 |
| 2 | Q | `a:quirk*` | 70 |
| 3 | Q | `a:squirk*` | 4 |
| 4 | Q | `a:quirkonium` | 5 |
| 5 | Q | `a:infracolor*` | 6 |
| 6 | Q | `a:"infracolour"` | 0 |
| 7 | Q | `a:"hidden valley" and a:string` | 3 |
| 8 | Q | `a:"hidden valley" and a:confin*` | 18 |
| 9 | Q | `a:"folded supersymmetry" and a:quirk*` | 5 |
| 10 | Q | `a:"quirky little Higgs"` | 3 |
| 11 | Q | `a:"long string" and a:collider` | 4 |
| 12 | Q | `a:"macroscopic string" and a:collider` | 0 |
| 13 | Q | `a:"flux tube" and a:collider` | 8 |
| 14 | Q | `a:"flux tube" and a:"new physics"` | 1 |
| 15 | Q | `a:"hidden confining" and a:electroweak` | 2 |
| 16 | Q | `a:"dark glueball" and a:quirk*` | 0 |
| 17 | Q | `a:glueball and a:"heavy fermion" and a:stable` | 0 |
| 18 | Q | `a:"stable" and a:"confining" and a:"hidden sector" and a:"LHC"` | 3 |
| 19 | Q | `a:"vector-like confinement"` | 4 |
| 20 | Q | `a:"string tension" and a:"heavy quark" and a:"dark"` | 0 |
| 21 | Q | `a:"dark QCD" and a:"heavy quark"` | 0 |
| 22 | Q | `a:"dark pion" and a:quirk*` | 0 |
| 23 | Q | `a:"neutral naturalness" and a:string` | 1 |
| 24 | Q | `a:"twin Higgs" and a:"quirk*"` | 0 |
| 25 | Q | `a:"heavy dark quark" and a:confin*` | 0 |
| 26 | Q | `a:"Nambu-Goto" and a:collider` | 1 |
| 27 | Q | `a:"effective string" and a:"LHC"` | 10 |
| 28 | Q | `a:"strongly interacting massive particles" and a:string` | 0 |
| 29 | Q | `a:"Lorentz" and a:string and a:"heavy particles" and a:detector` | 0 |
| 30 | Q | `a:monopole and a:"Geant4" and a:"magnetic field"` | 0 |
| 31 | Q | `a:"exotic" and a:"non-helical"` | 0 |
| 32 | Q | `a:"quirk*" and a:"Sommerfeld"` | 0 |
| 33 | Q | `a:"dark glueball" and a:"Higgs"` | 3 |
| 34 | Q | `a:"mesoscopic" and a:string and a:LHC` | 1 |
| 35 | Q | `a:"oscillating" and a:"heavy" and a:"infracolor"` | 0 |
| 36 | Q | `a:"hypercolor" and a:"string" and a:LHC` | 0 |
| 37 | Q | `a:"hidden sector" and a:"confining" and a:"track*" and a:"anomalous"` | 0 |
| 38 | Q | `a:"stable charged" and a:"string" and a:LHC` | 0 |
| 39 | Q | `a:"dark photon" and a:"quirk*"` | 0 |
| 40 | Q | `a:"electroweak" and a:"quirk*" and a:"W mass"` | 0 |
| 41 | cites:0805.4642 | `refersto:recid:787371` | 100 |
| 42 | cites:1708.02243 | `refersto:recid:1614773` | 37 |
| 43 | cites:1911.02223 | `refersto:recid:1763305` | 13 |
| 44 | cites:2002.07503 | `refersto:recid:1781289` | 14 |
| 45 | cites:1811.08903 | `refersto:recid:1704655` | 29 |
| 46 | cites:2108.06748 | `refersto:recid:1905711` | 17 |
| 47 | cites:2404.13814 | `refersto:recid:2779435` | 17 |
| 48 | cites:2512.20696 | `refersto:recid:3095565` | 4 |
| 49 | cites:2607.26195 | `refersto:recid:3184325` | 1 |
| 50 | cites:1106.2569 | `refersto:recid:913637` | 55 |
| 51 | cites:1703.00912 | `refersto:recid:1516007` | 27 |
| 52 | cites:2410.00269 | `refersto:recid:2836006` | 8 |
| 53 | cites:2509.08878 | `refersto:recid:2968943` | 4 |
| 54 | cites:1512.05782 | `refersto:recid:1410596` | 75 |
| 55 | cites:0805.4667 | `refersto:recid:787381` | 67 |
| 56 | cites:2504.02940 | `refersto:recid:2908013` | 8 |
| 57 | cites:2506.11192 | `refersto:recid:3103830` | 10 |
| 58 | cites:2311.15486 | `refersto:recid:2726646` | 9 |
| 59 | cites:1008.3547 | `refersto:recid:865796` | 24 |
| 60 | cites:0712.2681 | `refersto:recid:770656` | 43 |
| 61 | cites:0909.2034 | `refersto:recid:830917` | 100 |
| 62 | cites:0907.4932 | `refersto:recid:827099` | 10 |
| 63 | cites:0805.4642 | `refersto:recid:787371 pages 2-3 (size100 each)` | 126 (total 226) |

Notes: cites:0805.4642 page 1 returned 100 (cap), pages 2-3 added 126 (total 226 = INSPIRE count); cites:0909.2034 capped at 100 of 215. Unique records after merging: 484 (see `T5_census.json`). Records not in `bibliography.json` that contain quirk/infracolor in title or abstract: 4 genuine (0810.3948, 1112.4629, 2756876, 1258080 via other hits) plus quantum-computing noise.
