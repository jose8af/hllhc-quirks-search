# Scout note: QCD / substructure / observable-driven cluster

22 candidate seeds, 121 papers. Details in scout_qcd_substructure.json. Statuses use the methodology taxonomy; confidence is limited by abstract-level reading for most items. Gap quotes were extracted from PDFs via arxiv_pdf.py (hyphenation/two-column artefacts possible, e.g. 2506.11192 fragment).

## Seeds

### Toponium (eta_t) beyond the ttbar threshold bump: new decay and production channels at HL-LHC
- Framework: NRQCD colour-singlet quasi-bound ttbar state (toponium); status: `one-observable-not-another`; novelty: experimental-analysis; confidence: medium
- Idea: CMS and ATLAS now report threshold enhancements compatible with a pseudoscalar colour-singlet ttbar quasi-bound state. Theory papers propose further handles: eta_t -> WW, other rare decays, and spin/quantum-information observables to extract the signal. Dedicated HL-LHC analyses of these other decays/channels are not seen in the queries run.
- Signature: Dilepton WW-like final state from eta_t->W+W- near m_tt~345 GeV; threshold-region ttbar in lepton+jets and dilepton with spin-correlation observables
- Closest existing: arXiv:2503.22382 (CMS dilepton pseudoscalar excess at ttbar threshold); arXiv:2601.11780 (ATLAS dilepton cross-section enhancement near threshold); arXiv:2608.19546 (CMS single-lepton channel excess at threshold)
- Gap sentence: "A more realistic treatment including full hadronisation and the simulation of the response of a typical LHC detector is left for future work." (arXiv:2602.23426)
- Notes: eta_t->WW rate depends on decay constant (two scenarios in 2607.24203); do not quote yields without reading the paper.

### Pseudoscalar vs vector vs toponium discrimination with spin correlations/steering
- Framework: 2HDM CP-odd A, topcolor Z', toponium; quantum-information observables; status: `theory-explored-untested`; novelty: phenomenology; confidence: low
- Idea: Contrasting a toponium state with a genuine CP-odd Higgs or spin-1 ttbar resonance requires spin-density-matrix observables. Papers propose helicity-correlation and quantum steering/Bell observables for discrimination; the experimental threshold analyses so far test toponium vs perturbative QCD, not alternative-resonance spin hypotheses in a dedicated fit.
- Signature: Spin correlation coefficients, D, steering/Bell variables vs m_tt in dilepton channel near threshold and for A/H -> tt resonances (400-800 GeV)
- Closest existing: arXiv:2507.05119 (CMS A/H -> tt search; closest resonance search); arXiv:2503.22382 (CMS threshold excess, uses angular observables)
- Notes: No verbatim gap sentence captured; lead inferred from abstracts of 2609.11641 and 2606.30768.

### Top-flavoured hadronic states (single-top mesons, toponium spectroscopy) as LHC targets
- Framework: Top-flavoured meson/hadron phenomenology beyond eta_t; status: `proposed-not-searched`; novelty: phenomenology; confidence: low
- Idea: Recent theory preprints discuss single-top hadronic states, finite-width dissolution of radial toponium excitations and top-flavoured meson masses. No LHC search targeting these states was found.
- Signature: Resonant structure in t+jet / tW or m_tt above threshold; excited toponium radial states
- Closest existing: arXiv:2503.22382 (CMS toponium threshold: only ground state pseudoscalar probed)
- Notes: Abstracts not read in detail; speculative, 2026 preprints with zero/few citations.

### Entanglement/Bell tests and tomography in H->ZZ*->4l and H->WW* at HL-LHC
- Framework: Quantum information in Higgs decays to massive vector bosons (qutrit pairs); status: `searched-limited-regime`; novelty: experimental-analysis; confidence: medium
- Idea: Proposals test entanglement and Bell inequalities in H->VV; ATLAS reported Z-boson-pair entanglement from H->ZZ*. Theory shows tomography can fail at NLO (non-positive-semidefinite operator) and that Bell violation sensitivity was weak in the original study. H->WW* and combined observables remain candidates.
- Signature: Angular spin-density-matrix observables in H->4l and H->WW*->lvlv/semileptonic; concurrence lower bounds
- Closest existing: arXiv:2603.26463 (ATLAS first measurement of ZZ entanglement in H->ZZ*->4l, 13 and 13.6 TeV); recid:3195048 (ATLAS thesis/conf. note on H->WW* semileptonic decay (title only seen))
- Gap sentence: "A combination of both observables, which is beyond the scope of this work, would improve the sensitivity." (arXiv:2209.13441)
- Notes: ATLAS result exists; HL-LHC projection and WW*/combination not verified.

### Entanglement and Bell tests in WW/WZ production and dimension-8 sensitivity
- Framework: Quantum observables in weak boson pairs; EFT dim-6/8; status: `proposed-not-searched`; novelty: experimental-analysis; confidence: medium
- Idea: Entanglement in diboson production is proposed as a probe of EFT operators including dim-8; vector boson scattering is explicitly deferred to future work. No CMS/ATLAS WW/WZ spin-density-matrix entanglement measurement was found in these queries.
- Signature: Spin density matrix of W/Z pairs in leptonic decays; VBS regime at high m_VV
- Closest existing: arXiv:2603.26463 (closest: ZZ entanglement from Higgs decays only); arXiv:2406.03976 (CMS tt entanglement, same technique)
- Gap sentence: "The study of this kind of processes, which would be phenomenologically quite different and would add considerable sensitivity on dimension-8 operators, is left for future work." (arXiv:2307.09675)
- Notes: Empty collaboration queries do not prove absence; no WW result seen in the cache.

### Tau-pair entanglement and dipole-operator constraints at the LHC
- Framework: Quantum tomography with tau leptons; tau dipole moments; status: `proposed-not-searched`; novelty: experimental-analysis; confidence: low
- Idea: Entangled two-qubit tau pairs from Z/H decays probe anomalous dipole couplings; the authors note full NLO QCD would be needed to strengthen limits. No LHC tau-pair entanglement measurement found.
- Signature: Spin correlations of tau decay products (hadronic tau polarimetry) in Z->tautau and H->tautau
- Closest existing: arXiv:2409.11067 (CMS top spin-correlation methodology only (no tau analysis))
- Gap sentence: "Therefore, the QCD contribution to the dipole operator can be neglected, as we did, but a full QCD NLO estimate, though computationally challenging, will be necessary if the limit is to be strengthened." (arXiv:2208.11723)
- Notes: Recent citing papers are mostly e+e- (STCF); LHC tau reconstruction/neutrino issues not reviewed.

### Quantum-information observables as searches for invisible mediators and EFT in tt+X at HL-LHC
- Framework: Top-philic simplified dark matter; SMEFT; quantum spin correlations; status: `theory-explored-untested`; novelty: phenomenology; confidence: medium
- Idea: Entanglement marker D and spin correlations in dileptonic ttbar are proposed as complementary probes of ttbar+MET mediators and of SMEFT operators, with an HL-LHC sensitivity study. CMS/ATLAS have measured D in SM only.
- Signature: Dilepton ttbar + MET: yield, m_vis, D-estimator, fiducial spin correlation vs mass
- Closest existing: arXiv:2406.03976 (CMS observation of tt entanglement); arXiv:2311.07288 (ATLAS observation of entanglement); arXiv:2409.11067 (CMS polarization/spin correlation measurement)
- Notes: 2609.31425 explicitly targets HL-LHC dileptonic channel.

### Quantum steering, discord and magic of top pairs: full measurement program
- Framework: Quantum resource theory applied to ttbar spin states; status: `one-observable-not-another`; novelty: experimental-analysis; confidence: low
- Idea: Beyond entanglement, steering and discord were proposed for tops; CMS has an observation of magic states. Steering/discord/Bell-nonlocality dedicated measurements were not seen among results returned by the queries.
- Signature: Spin density matrix of ttbar over m_tt and angle bins; steering ellipsoid and discord estimators
- Closest existing: recid:2902583 (CMS observation of magic states of top quark pairs); arXiv:2409.11067 (CMS full spin density matrix)
- Notes: Likely reachable already with existing Run-2 data; HL-LHC relevance is precision/boosted regime.

### Boosted ttbar entanglement and spin analysis with jet substructure
- Framework: Top spin correlations in the boosted regime with substructure-based spin analysers; status: `LHC-not-projected-to-HL`; novelty: experimental-analysis; confidence: low
- Idea: Entanglement and Bell tests extend to the boosted regime using hadronic tops; existing observations are near threshold. HL-LHC statistics at high m_tt could test Bell violation and BSM-sensitive regimes.
- Signature: Boosted ttbar, large-R jets with substructure-based top-spin analyser, m_tt > 1 TeV
- Closest existing: arXiv:2311.07288 (ATLAS entanglement, low m_tt region); arXiv:2406.03976 (CMS entanglement, threshold region)
- Notes: Regime of existing ATLAS/CMS analyses taken from titles/abstracts only.

### Three-point energy correlators on W/top decays for precision mass and boosted tagging
- Framework: Perturbative QCD energy correlators in collinear limit; status: `proposed-not-searched`; novelty: experimental-analysis; confidence: medium
- Idea: Energy correlators inside top and W jets give a hadronisation-robust top-mass observable and W standard-candle calibration; the full three-point correlator on top decays is a rich function whose shape is unexplored in the paper. CMS/ATLAS have measured EECs in inclusive jets, not on top decays.
- Signature: EEC / 3-pt EEC (projected) of large-R top-tagged jets; peak position vs m_t
- Closest existing: arXiv:2402.13864 (CMS EEC inside jets and alpha_s); arXiv:2301.09351 (ATLAS TEEC alpha_s from multijets); arXiv:2407.10879 (ATLAS Lund jet plane in top and W decays (closest substructure measurement))
- Gap sentence: "The NLO determination of JEEEC is an outstanding theoretical problem and is very involved, thus beyond the scope of this article, though a road map towards its completion has recently become available [105, 114, 115]." (arXiv:2201.08393)
- Notes: Measurement/mass, not strictly BSM; included as observable-driven lead. Follow-up 2601.20923 (2026) found via forward citations.

### Bump hunting inside jets with energy correlators (hadrophilic light resonances)
- Framework: Energy correlator scaling violation from new physics; unitarity/positivity classification; status: `proposed-not-searched`; novelty: phenomenology; confidence: medium
- Idea: New physics breaks the collinear scaling of EECs and appears as an angular bump inside jets, giving a broadband search for light hadrophilic states (e.g. Z'). Projected LHC sensitivity claimed competitive with existing searches (not read in detail).
- Signature: EEC distribution in inclusive/boosted jets; bump at angle set by resonance mass/pT
- Closest existing: arXiv:2402.13864 (CMS EEC measurement inside jets (fit for alpha_s) - raw data basis); arXiv:2502.09770 (ATLAS weakly supervised dijet resonance search, indirect); arXiv:2512.20395 (CMS ML model-independent dijet searches)
- Notes: Very recent preprint (2026); no experimental follow-up seen.

### Dark-shower radiation patterns in the Lund jet plane and EEC-based dark-sector searches
- Framework: Confining hidden sectors / dark QCD parton showers; status: `one-observable-not-another`; novelty: experimental-analysis; confidence: medium
- Idea: Dark showers imprint distinct features in the Lund jet plane; the original authors suggest designing searches that exploit these features, and later work uses deep learning on LJP to infer dark gauge groups. CMS/ATLAS dark-shower searches exist but are not built on LJP observables.
- Signature: Lund-plane density / graph-network tagger on semi-visible and emerging jets; EEC with dark hadronisation
- Closest existing: arXiv:2403.01556 (CMS emerging jets (dark QCD, incl. flavoured sector)); arXiv:2505.01634 (ATLAS semivisible jets / anomalous signatures); arXiv:2608.05323 (CMS lepton-enriched semivisible jets); arXiv:2004.03540 (ATLAS LJP measurement (SM only))
- Gap sentence: "From a phenomenological perspective, it would be very interesting to design searches that take advantage of these features (or are explicitly agnostic to them), perhaps even using machine learning." (arXiv:2301.07732)
- Notes: Follow-up partially exists on theory side (2606.25513).

### Soft unclustered energy patterns (SUEP/soft bombs): displaced, non-resonant and pair-production regimes
- Framework: Strongly coupled hidden valley; large-N / AdS-like multiplicity; soft bombs; status: `searched-limited-regime`; novelty: experimental-analysis; confidence: medium
- Idea: The original soft-bomb paper defers displaced decays and non-resonant/pair-production cases. Forward citations show CMS (ggF, W/Z-associated, scouting) and ATLAS (muons) SUEP searches; displaced SUEP and other production modes were not found in these queries.
- Signature: High-multiplicity isotropic soft tracks, with displaced vertices or pair-produced mediators; trigger via scouting or L1 tracking at HL-LHC
- Closest existing: arXiv:2403.05311 (CMS first dedicated SUEP search (ggF)); arXiv:2604.05996 (CMS W/Z-associated SUEP); arXiv:2605.20015 (ATLAS SUEP with muons); recid:3132607 (CMS SUEP with data scouting)
- Gap sentence: "We reserve a more thorough investigation of the various experimental signatures, including different final states and non-prompt decays, to future work." (arXiv:1612.00850)
- Notes: Forward citations used: the gap partially followed up. Displaced SUEP absence is not a proof.

### Quirks and SUEP: TeV-scale dijet resonance with soft pattern
- Framework: Quirk / infraparticle models with long strings; status: `proposed-not-searched`; novelty: phenomenology; confidence: low
- Idea: Quirk annihilation can produce a dijet-like resonance accompanied by soft unclustered energy; the authors state the phase space has not been probed. Related timing-based quirk search at FASER recently appeared.
- Signature: Resonance at TeV scale with high-multiplicity soft activity; pileup-robust track-based observables
- Closest existing: arXiv:2403.05311 (CMS SUEP search); recid:3184325 (FASER quirk search (timing))
- Gap sentence: "phase space that has not been probed at the LHC so far" (arXiv:2506.11192)
- Notes: Quote is a fragment from jumbled extraction; verify before use.

### QCD instanton / sphaleron-like multi-jet final states via jet-correlation observables
- Framework: Instanton-induced processes; electroweak sphalerons; status: `indirectly-covered`; novelty: phenomenology; confidence: low
- Idea: Instanton ('soft bomb'-like) events at LHC energies are proposed to be separable from perturbative scattering with jet-correlation observables. CMS searches for sphalerons/black holes in high multiplicity final states exist; QCD instanton-specific search not seen.
- Signature: High-multiplicity jets/tracks with spherical event shape; jet correlation observables in specific m_hadrons range
- Closest existing: arXiv:1805.06013 (CMS black holes and sphalerons, high multiplicity); arXiv:2604.10732 (CMS microscopic BH, string balls, sphalerons; sphaleron threshold 9 TeV)
- Notes: Instanton-specific CMS/ATLAS analysis not verified.

### Lepton-jets and dark-photon substructure with Run 3 / HL-LHC triggers
- Framework: Dark photon / hidden-sector cascades; status: `LHC-not-projected-to-HL`; novelty: experimental-analysis; confidence: low
- Idea: Lepton-jets from radiating dark matter and dark Higgs cascades; substructure helps. ATLAS prompt lepton-jet searches use 7 and 8 TeV data; CMS recent non-prompt dimuon hidden-valley search (41.6 fb^-1) uses dedicated triggers. Run-2 prompt lepton-jet substructure analyses were not found in queries.
- Signature: Collimated lepton pairs, muon/electron jets; prompt and displaced; low-pT triggers and scouting
- Closest existing: arXiv:1511.05542 (ATLAS prompt lepton-jets 8 TeV); arXiv:2511.11888 (CMS non-prompt dimuon dark showers, 2018 data only); arXiv:2601.17544 (CMS LLP trigger program)
- Notes: Run-2 ATLAS lepton-jet publications may exist beyond what INSPIRE queries returned.

### Strange-jet tagging for Higgs-strange coupling and light-quark dark sectors
- Framework: Light-quark Yukawa couplings; kaon-based strange tagging; status: `proposed-not-searched`; novelty: experimental-analysis; confidence: low
- Idea: Strange tagging at hadron colliders using kaons and track information is proposed; ATLAS/CMS flavour tagging focuses on b/c. H->ss searches were not found in the queries.
- Signature: VH(H->ss) or boosted H with kaon-rich jets; K_S/K_L identification
- Closest existing: arXiv:2407.15550 (ATLAS Hc search (charm)); arXiv:2410.19611 (ATLAS VH bb/cc direct constraints)
- Notes: CMS strange tagging in GN3/ParticleNet not verified.

### Parton distributions absorbing new physics in high-mass tails; SMEFT-PDF simultaneous fits at HL-LHC
- Framework: PDF-SMEFT interplay; status: `LHC-not-projected-to-HL`; novelty: phenomenology; confidence: medium
- Idea: PDFs at large x may absorb energy-growing EFT effects; tailored PDFs and simultaneous fits are proposed. HL-LHC Drell-Yan scenario illustrated. Experimental high-mass DY analyses do not report simultaneous PDF-EFT unfolding in the results seen.
- Signature: High-mass Drell-Yan double-differential tails; simultaneous PDF+SMEFT fits
- Closest existing: arXiv:2607.28334 (ATLAS high-mass dilepton resonance search 13.6 TeV); arXiv:2307.08567 (ATLAS high-mass dilepton LFV)
- Gap sentence: "Performing a fully realistic simulation, with acceptance cuts and detector effects, is beyond the scope of the current study" (arXiv:2307.10370)
- Notes: Experimental coverage is resonance search; non-resonant DY tails not specifically verified.

### Multi-lepton anomalies (heavy scalar H -> Sh, SS(h)) and generic multilepton anomaly detection
- Framework: Singlet scalar / 2HDM+S multilepton excesses; status: `indirectly-covered`; novelty: experimental-analysis; confidence: low
- Idea: Reported multi-lepton anomalies are interpreted with a heavy scalar decaying to SM Higgs + lighter singlet; ATLAS ran a model-independent anomaly detection in multilepton final states.
- Signature: Multilepton + b-jets, differential in lepton multiplicity and HT; anomaly-enriched regions
- Closest existing: arXiv:2508.19778 (ATLAS multilepton anomaly detection); arXiv:2606.30862 (CMS 3top/4top BSM search)
- Notes: Controversial anomaly; statistical significance not assessed here.

### Anomaly detection for hidden-valley / SUEP final states at trigger level
- Framework: Model-independent ML searches motivated by dark QCD; status: `searched-limited-regime`; novelty: experimental-analysis; confidence: low
- Idea: Community challenge defined anomaly detection; experiments applied to dijets, multileptons, and semivisible jets. Trigger-level anomaly detection and SUEP-targeted autoencoders appear in proposals; unsupervised hadronic SUEP studied.
- Signature: Autoencoder/normalising-flow scores on high-multiplicity events at L1/HLT or scouting
- Closest existing: arXiv:2502.09770 (ATLAS weakly supervised dijet); arXiv:2512.20395 (CMS ML dijet model-independent); arXiv:2508.19778 (ATLAS multilepton AD)

### Top charge asymmetry in tt+X (ttW, boosted, energy asymmetry) at HL-LHC
- Framework: QCD charge asymmetry; axigluon/Z'/SMEFT; status: `constrained-but-region-open`; novelty: experimental-analysis; confidence: low
- Idea: ATLAS reports evidence for ttbar charge asymmetry; ttW charge asymmetry measured by CMS; energy asymmetry and SMEFT constraints proposed as complementary. HL-LHC precision and differential regimes not found in projections.
- Signature: Delta|y|, energy asymmetry, leptonic asymmetry in ttbar, ttW, boosted tops
- Closest existing: arXiv:2208.12095 (ATLAS evidence charge asymmetry in ttbar); arXiv:2208.02751 (CMS ttbar charge asymmetry at 13 TeV); arXiv:2509.13512 (CMS ttW charge asymmetry)
- Gap sentence: "Often, the bounds from the differential analysis are significantly tighter than the global bounds, indicating that inclusion of these results in future global fits can improve the global result, by disentangling some of the poorly constrained combinations of operator coefficients." (arXiv:2208.12095)
- Notes: Titles for CMS 2208.02751 truncated MathML; only identification verified.

### CP-odd observables in ttH and tt-threshold spin correlations
- Framework: CP-mixed top-Higgs Yukawa; pseudoscalar couplings; status: `one-observable-not-another`; novelty: experimental-analysis; confidence: low
- Idea: ATLAS/CMS probe CP in ttH; the ATLAS paper notes CP-mixed states have not been ruled out. Spin-correlation CP-odd observables near ttbar threshold (where a pseudoscalar-like excess is seen) are a natural extension.
- Signature: CP-odd azimuthal/triple-product spin observables in ttH and threshold ttbar
- Closest existing: arXiv:2303.05974 (ATLAS ttH CP); arXiv:2208.02686 (CMS ttH/tH CP in multilepton channels); arXiv:2503.22382 (CMS pseudoscalar excess (parity-sensitive angular observables))
- Gap sentence: "But mixing of CP-odd and CP-even states has not been ruled out and is worth investigating." (arXiv:2303.05974)
- Notes: Gap sentence is generic motivation, not a specific proposal.

## Observations
- Toponium: CMS (2503.22382, 2608.19546) and ATLAS (2601.11780) threshold excesses now exist; the open items are alternative-resonance discrimination and other decay channels.
- Gaps with forward-citation checks: soft bombs 1612.00850 (followed by CMS/ATLAS SUEP searches, displaced regime not found); H->ZZ entanglement 2209.13441 (followed by ATLAS 2603.26463); LJP dark showers 2301.07732 (partial theory follow-up 2606.25513).
- Caveat: scratchpad query log was shared with other agents and partly overwritten; the first-batch queries are reconstructed manually.
- Plain-language 'no hit' results come from INSPIRE title queries and do not prove absence.