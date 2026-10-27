# Gate 3 adversarial novelty review - batch F
Reviewer: adversarial agent F. Candidates: C053 C054 C057 C061. Sources: INSPIRE (tools/inspire.py), arXiv PDFs (tools/arxiv_pdf.py). Note: "not found" is not proof of absence.

## C053 - verdict: **NARROWED** (confidence medium-high)
**Claim:** A bundle of EW-EFT observables claimed under-exploited at HL-LHC: interference-resurrection azimuthal angles for aTGC, polarisation/spin-correlation asymmetries for aQGC in ssWW, universal-SMEFT W,Y from NC+CC Drell-Yan, triboson dim-6/8 SMEFT, gauge-invariant dim-8 nTGC angular observables, gluonic dim-8 QGCs (gg->Zgamma/gammagamma), and HEFT-vs-SMEFT VBF HH/HHH.

**Surviving gap:** Most sub-ideas are already done by CMS/ATLAS. Small residual gaps remain: (i) a decay-plane azimuthal interference-resurrection fit in boosted semileptonic WV (l nu J), where only standard-parametrisation aTGC fits were found; (ii) an experimental interpretation of high-mass gamma-gamma / Z gamma spectra in terms of gluonic dim-8 QGC operators, which is recast-level (pheno 2112.06729 already uses ATLAS data; HL-LHC projection in 2512.04336); (iii) a joint NC+CC Drell-Yan universal W,Y fit with dim-8 terms; (iv) dim-8 nTGC from ZZ->4l decay angles combined with Z gamma. None is a strong standalone HL-LHC analysis.

**Bundle split:**
- S059 interference resurrection (WV/WZ azimuthal angles): **DIES (leptonic) / NARROWED (semileptonic boosted)** - CMS W gamma 2111.13948 uses the lepton azimuthal decay angle phi explicitly as 'interference resurrection' for O_3W (Abstract; Sec.2). ATLAS WZ 2507.03500 uses phi*_W, phi*_Z decay angles to revive interference for CP-odd operators (EFT section, txt ~l.1076, 1591). ATLAS WZ CP-sensitive observables are summarised in proceedings 2601.17461. Residual: boosted l nu qq.
- S060 polarisation/spin-correlation asymmetries for aQGC in ssWW/WZ: **NARROWED (weak)** - Proposal 2606.06436 finds sensitivity only 'comparable' to the m_T(WW) tail (Abstract). Polarised ssWW is already measured (CMS 2009.09429, ATLAS 2503.11317), as is WZjj-EW (ATLAS 2607.20246). aQGC from ssWW/WZ is in the ATLAS combination 2603.18630. Two neutrinos prevent rest-frame reconstruction. CMS HL-LHC VBS projection: INSPIRE 1488789.
- S064 universal SMEFT W,Y from DY: **DIES (NC and CC separately) / NARROWED (joint + dim-8)** - CMS-PAS-EXO-25-001 (INSPIRE 3181329) gives W and Y limits from high-mass ee/mumu, 207 fb-1 at 13+13.6 TeV. CMS 2202.06075 constrains the W parameter from l+MET. A joint NC+CC fit with dim-8 terms was not found.
- S067 triboson dim-6/8: **NARROWED** - aQGC limits from ATLAS WWgamma 2509.14070, CMS WZgamma 2503.21977, CMS W/Z gamma gamma 2105.12780 (scout), ATLAS VVZ 2412.15123, ATLAS QGC combination 2603.18630 (includes a triboson input). Residual: dim-6 triboson SMEFT global interpretation; rates are low.
- S068 gauge-invariant dim-8 nTGC: **DIES (Z gamma) / NARROWED (ZZ phi angles)** - ATLAS-CONF-2025-001 (INSPIRE 2909586) gives SU(2)xU(1) gauge-invariant nTGC limits from Z(ll)gamma. CMS 2512.08582 constrains dim-8 nTGC in a recent EFT framework, which it describes as 'for the first time'. CMS Z(nunu)gamma 2601.14102 also exists.
- S069 gluonic dim-8 QGC (gg->Zgamma, gammagamma): **SURVIVES (recast-level)** - No CMS/ATLAS interpretation found. Pheno already recasts ATLAS data (2112.06729 abstract) and gives HL-LHC reach (2512.04336 abstract). The signal is a high-mass tail shared with nonresonant diphoton/contact-interaction searches.
- S070 HEFT vs SMEFT in VBF HH/HHH: **DIES (HH) / showstopper (HHH)** - kappa_2V is measured (CMS 2205.06667). HEFT interpretations exist: ATLAS 2069569, ATLAS 2970397, CMS combination 2510.07527. ATLAS HL-LHC boosted VBF HH 4b projection: INSPIRE 2898243. ATLAS W+-W+-Hjj probes WWHH (2609.25153). The VBF HHH rate is far below the ggF HHH SM rate (0.079 fb at 13 TeV, 2411.02040).

**Kill evidence:**
- arXiv:2111.13948 (Abstract; Sec.2 'Interference resurrection'): CMS W gamma differential + EFT using photon pT and charged-lepton azimuthal decay angle, explicitly 'interference resurrection', giving about 10x interference sensitivity
- arXiv:2507.03500 (EFT interpretation section): ATLAS WZ: phi*_W/phi*_Z decay angles used to revive interference for CP-odd dim-6 operators
- CMS-PAS-EXO-25-001 (INSPIRE 3181329) (Abstract): CMS limits on oblique W and Y from high-mass dileptons, 207 fb-1
- ATLAS-CONF-2025-001 (INSPIRE 2909586) (Abstract): ATLAS fully gauge-invariant nTGC form factors in Z(ll)gamma, 140 fb-1
- arXiv:2512.08582 (Abstract): CMS Z gamma at 13.6 TeV with dim-8 nTGC constraints in a new EFT framework
- arXiv:2603.18630 (Abstract): ATLAS combined dim-8 (Eboli) aQGC interpretation of VBS + triboson
- arXiv:2510.07527 (Abstract (HEFT keyword match)): CMS HH combination including HEFT interpretation

**Closest existing:**
- arXiv:2111.13948 [CMS]: covers W gamma interference resurrection via phi; gap: not WV semileptonic boosted
- arXiv:2510.00118 [CMS]: covers semileptonic VBS l nu qq / ll qq aQGC; gap: aQGC via mass tails, not decay-plane angles
- INSPIRE 3181329 [CMS]: covers W,Y from NC DY; gap: no CC combination/dim-8
- INSPIRE 2909586 [ATLAS]: covers gauge-invariant nTGC from Z gamma; gap: no ZZ phi-angle dim-8

**HL-LHC projection docs:** CMS HL-LHC ssWW/WZ VBS prospects (INSPIRE 1488789); ATLAS HL-LHC boosted VBF HH 4b (INSPIRE 2898243); ATLAS HL-LHC HH projections (INSPIRE 2898222). Pheno: 2512.04336 (gluonic QGC at HL-LHC), 2008.12978 (W,Y HL).

**Showstoppers:** Neutrino ambiguity limits decay-plane reconstruction in WW and ssWW. In boosted semileptonic WV, quark/antiquark subjet identification is ambiguous (phi folded), which reduces the resurrection gain (UNVERIFIED magnitude). EFT validity in tails at dim-8. Triboson and VBF multi-Higgs rates are low.

**Notes:** This bundle should not go forward as one candidate. Interference resurrection in particular is an established experimental technique: CMS has used it since 2021 in W gamma. The best remaining HL-LHC hook is the boosted semileptonic WV azimuthal analysis, which is incremental.

<details><summary>Queries run</summary>

- `t "interference resurrection" or abstracts.value:"interference resurrection"`
- `t "triple gauge" and t azimuthal (CMS/ATLAS)`
- `abstracts.value:"azimuthal" and "triple gauge" (CMS/ATLAS)`
- `t "anomalous gauge" or "triple gauge" (CMS/ATLAS) date>2021`
- `abstracts.value:"interference" and "triple gauge" date>2019`
- `abstracts.value:"decay angle" and "effective field theory"`
- `cites 1708.07823 (collab filter)`
- `cites 2301.13663`
- `t "same-sign" and polarized W`
- `abstracts.value:"polarization" and "quartic" (CMS/ATLAS)`
- `t same-sign WW HL-LHC`
- `abstracts.value:"oblique parameters" and "Drell-Yan"`
- `abstracts.value:"W and Y" and "Drell-Yan"`
- `t "Higgs compositeness" and dilepton`
- `abstracts.value:"W parameter" (CMS/ATLAS)`
- `cites 2008.12978 (collab filter)`
- `t triboson (CMS/ATLAS) date>2019`
- `abstracts.value:"anomalous quartic" (CMS/ATLAS) date>2021`
- `cites 2112.06729`
- `abstracts.value:"gluon" and "quartic" and "photon"`
- `abstracts.value:"HEFT" (CMS/ATLAS)`
- `t VBF Higgs boson pair (CMS/ATLAS)`
- `abstracts.value:"semileptonic" and "triple gauge"`
- `pdf grep 2111.13948, 2507.03500`
</details>

## C054 - verdict: **NARROWED** (confidence medium)
**Claim:** Quantum entanglement / Bell tests (spin-density-matrix tomography) in WW, WZ, ZZ continuum production, H->ZZ*, H->WW* and tau pairs have not been measured by CMS/ATLAS and are an HL-LHC opportunity.

**Surviving gap:** (a) H->WW*->lvlv entanglement/CGLMP test: no CMS/ATLAS result found (pheno 2209.14033, 2605.19754), but it is a Run-2/3 analysis, not HL-LHC-specific; (b) full two-qutrit tomography + concurrence/Bell in continuum high-mass ZZ->4l (and WW) at HL-LHC: only polarisation fractions measured so far; (c) tau-pair (Z/H->tautau) entanglement tomography at LHC: pheno only (2504.01496). H->ZZ* entanglement is done (ATLAS 4.7 sigma; CMS density matrix). WZ entanglement is theoretically disfavoured as demonstrable (2601.09540).

**Bundle split:**
- H->ZZ*->4l entanglement / density matrix: **DIES** - ATLAS 2603.26463 (separable hypothesis disfavoured at 4.7 sigma, exp 4.9); CMS-PAS-HIG-25-011 (INSPIRE 3087935) measures polarization density matrix in H->ZZ. HL-LHC is only a precision update (ATLAS conclusions).
- H->WW* entanglement: **SURVIVES (not HL-specific)** - No CMS/ATLAS measurement found; 2209.14033 claims Run-2 sensitivity using already-measured m_ll; showstopper: two neutrinos, spin-0 SM entanglement guaranteed (QM test, weak BSM leverage)
- pp->ZZ/WZ/WW continuum entanglement & Bell: **NARROWED** - ATLAS joint-polarisation WZ (2211.09435), ZZ longitudinal (2310.04350), WZ energy dependence (2402.16365), WZjj-EW (2607.20246), CMS WZ angles (2110.11231) cover partial density-matrix information; full tomography/concurrence not done. WZ entanglement not demonstrable in realistic regimes per 2601.09540 Conclusions; Bell violation in WW/ZZ needs m_VV>900 GeV (2302.00683 abstract) -> rate-limited, HL-LHC ZZ->4l high-mass is the only plausible slice.
- tau-pair entanglement: **SURVIVES (pheno-only)** - Pheno at LHC 2504.01496 (ML neutrino reconstruction); CMS/ATLAS H->tautau CP (2110.04836, 2212.05833, CMS 13.6 TeV INSPIRE 3138184) already exploit transverse tau spin correlations (one-observable-not-another). Showstopper: two-fold/neutrino ambiguity, tau trigger thresholds.
- VBS entanglement / dim-8: **SURVIVES (theory-explored-untested)** - 2306.17247 pheno; rate in leptonic VBS very low; no experimental study found

**Kill evidence:**
- arXiv:2603.26463 (Abstract; conclusions (txt line ~444)): ATLAS first measurement of ZZ* spin entanglement in H->ZZ*->4l at 13 and 13.6 TeV; separable hypothesis disfavoured at 4.7 sigma (exp 4.9); conclusions: HL-LHC will enable more precise tests
- CMS-PAS-HIG-25-011 (INSPIRE 3087935) (Abstract): CMS H->4l with 138+62 fb-1: polarization density matrix in H->ZZ measured, CP violation in Z polarization searched
- arXiv:2601.09540 (Conclusions (quoted by scout; abstract consistent)): WZ concurrence bounds do not allow to show the WZ system is spin-entangled in realistic (incl. boosted) regimes

**Closest existing:**
- arXiv:2603.26463 [ATLAS]: covers H->ZZ* entanglement; gap: no H->WW*, no continuum ZZ
- arXiv:2211.09435 [ATLAS]: covers WZ joint polarisation fractions; gap: not full density matrix/entanglement markers
- arXiv:2310.04350 [ATLAS]: covers ZZ->4l longitudinal pair evidence + CP; gap: no tomography/Bell at high m_ZZ
- arXiv:2110.04836 [CMS]: covers H->tautau CP via tau decay-plane correlations; gap: not entanglement/Bell tomography

**HL-LHC projection docs:** None found from CMS/ATLAS for diboson/H->WW/tau entanglement (not proof of absence). Pheno: 2302.00683, 2506.16077 (pp->ZZ entanglement Run2+3/HL), 2504.01496 (tau), 2605.19754 (HWW).

**Showstoppers:** Neutrino reconstruction for WW/tau (2605.26724 two-fold ambiguity); SMEFT truncation and NLO corrections spoil qutrit interpretation (2505.12125, 2609.25217 tomography limitations in H->4l); WZ entanglement not demonstrable (2601.09540); high-m_VV Bell region statistically starved in fully leptonic modes. BSM leverage over standard angular-coefficient EFT fits is debated (entanglement markers are functions of the same coefficients).

**Notes:** The flagship part (H->ZZ*) is dead. Remaining parts are measurements (QM tests) rather than BSM searches; HL-LHC relevance strongest for continuum high-mass ZZ tomography. H->WW* entanglement is the most concrete experimental gap but could be done with Run 2+3.

<details><summary>Queries run</summary>

- `t entanglement and (collaboration:ATLAS or collaboration:CMS)`
- `t Bell and (collaboration:ATLAS or collaboration:CMS)`
- `t "spin density matrix" and (collaboration:ATLAS or collaboration:CMS) and date > 2018`
- `t "quantum" and (t WZ or t WW or t ZZ) and date > 2021`
- `t entanglement and t tau and date > 2021`
- `t quantum tomography and t Higgs`
- `t "spin correlation" and t tau and (collaboration:CMS or collaboration:ATLAS)`
- `t "quantum information" and t HL-LHC`
- `t polarization and (t WZ or t ZZ or t WW) and (collaboration:CMS or collaboration:ATLAS) and date > 2021`
- `abstracts.value:"entanglement" and (collaboration:ATLAS or collaboration:CMS) and date > 2024`
- `t "joint-polarisation" or t "longitudinally polarised" (ATLAS/CMS)`
- `t "tau polarization" (ATLAS/CMS)`
- `abstracts.value:"entanglement" and abstracts.value:"WZ"`
- `abstracts.value:"entanglement" and abstracts.value:"vector boson scattering"`
- `abstracts.value:"entanglement" and abstracts.value:"high-luminosity"`
- `t CP tau Higgs Yukawa (CMS/ATLAS)`
- `cites 2208.11723`
- `cites 2209.14033`
- `pdf grep 2603.26463`
</details>

## C057 - verdict: **NARROWED** (confidence medium)
**Claim:** Energy-correlator (EEC/E3C) observables on boosted top/W jets (top mass), EEC 'bump hunts inside jets' for light hadrophilic resonances, and QCD-instanton multi-jet searches are untested by CMS/ATLAS and suited to HL-LHC.

**Surviving gap:** Only the top/W-jet E3C measurement (m_t/m_W standard-candle method of 2311.14389/2407.12900) survives as an experimental gap: no CMS/ATLAS measurement found (only a thesis-level feasibility, INSPIRE 2853221). It is a precision measurement doable with Run 2/3, not HL-LHC-specific. The EEC bump hunt is an alternative observable for the parameter space already searched by CMS low-mass Z'->qq ISR-boosted searches (claimed only 'competitive'). The QCD-instanton part is anti-HL: the signal is low-mass and soft and needs low-pileup runs.

**Bundle split:**
- E3C/EEC on boosted top & W jets (top mass): **SURVIVES (not HL-specific)** - No CMS/ATLAS measurement found; closest are the ATLAS Lund plane in top/W jets (2407.10879), CMS EEC in inclusive jets (2402.13864), and CMS boosted-top jet-mass m_t (1911.03800, 2211.01456). Pheno feasibility already done (2311.14389 incl. HL-LHC statistics, 2407.12900, 2405.20001); thesis 2853221. Gap type: proposed-not-searched, measurement.
- EEC bump hunt inside jets (light hadrophilic Z'): **NARROWED -> indirectly-covered** - 2605.28934 recasts CMS low-mass qq search and finds sensitivity only 'competitive' (abstract; Fig.4 text). Same Z' parameter space is searched by CMS 1909.04114, 2603.21965 (50-300 GeV, ParticleNet), 1905.10331 (ISR photon). Signal ECs at particle level; detector granularity/unfolding may degrade (2605.28934 p.~3). Residual: a different observable/systematics profile, plus SM W/Z in EEC as a benchmark.
- QCD instanton multi-jet / soft-bomb: **DIES for HL-LHC** - Signal sits at low instanton mass (20-60 GeV, 2104.01861 abstract) where pileup kills it; proposals require low-luminosity runs (2104.01861); 2012.09120 Sec.5.3 already sets a recast limit from ATLAS min-bias data; CMS low-PU event-shape measurement 2505.17850 is explicitly a reference for future instanton searches (Sec.1, lines ~64-69, 147). High-mass instantons are 'highly suppressed' (2012.09120 Sec.4). Not an HL-LHC (200 PU) analysis.

**Kill evidence:**
- arXiv:2104.01861 (Abstract): Instanton search strategy for masses 20-60 GeV in diffractive events in low-luminosity runs, 'thus avoiding problems with pile-up'
- arXiv:2012.09120 (Sec.5.3; Sec.4 intro): First limit on instanton processes from recasting ATLAS charged-particle min-bias data; at high luminosity pileup 'further complicates such a search'
- arXiv:2505.17850 (Introduction): CMS low-PU (64 microb-1) event-shape measurement motivated by instantons, a reference for future instanton searches
- arXiv:2605.28934 (Abstract; Fig.4 discussion): EEC bump hunt projected LHC sensitivity for light Z' is 'competitive with existing searches', based on recast of CMS low-mass resonance search
- arXiv:2603.21965 (Abstract): CMS low-mass (50-300 GeV) qq resonance search with ISR-boosted two-prong large-R jet

**Closest existing:**
- arXiv:2402.13864 [CMS]: covers EEC/E3C in inclusive jets, alpha_s; gap: no top/W jets, no BSM interpretation
- arXiv:2407.10879 [ATLAS]: covers Lund jet plane in top and W jets (ttbar); gap: different observable; no EEC/m_t extraction
- arXiv:2603.21965 [CMS]: covers light Z'->qq 50-300 GeV boosted; gap: uses N2/ParticleNet, not EEC angular bump
- arXiv:2505.17850 [CMS]: covers low-PU event shapes vs multiplicity (instanton-sensitive); gap: no instanton limit; low-PU only

**HL-LHC projection docs:** None from CMS/ATLAS found for EEC top mass or EEC bump hunt. Pheno 2311.14389 includes HL-LHC statistical feasibility. Instanton: 2012.09120 notes prescaled jet triggers would be needed during HL-LHC for the high-mass regime.

**Showstoppers:** EEC top mass: constituent/track-level angular observable at 200 PU needs charged-track or PUPPI-type mitigation; non-perturbative and NLO theory (JEEEC at NLO is an open problem per 2201.08393 outlook) limit interpretation. EEC bump hunt: detector angular granularity at small angles and unfolding; no clear sensitivity gain over N2/ParticleNet. Instantons: pileup, trigger (soft, high-multiplicity), and large generator uncertainty in the instanton cross-section.

**Notes:** This is a heterogeneous bundle with no common HL-LHC rationale. The surviving part is a SM precision measurement. Forward-proton-tag instanton searches (2609.15252 follow-up to Tasevsky 2022) also need low pileup. CMS also measures 4-point EEC (INSPIRE 3188778) and charm-jet EEC (2504.03431, found by web search, ID not INSPIRE-verified). The EEC programme is active in CMS, so a top-jet EEC is a natural next CMS step and could be in preparation (UNVERIFIED).

<details><summary>Queries run</summary>

- `t energy correlator and (collaboration:CMS or ATLAS or ALICE or LHCb)`
- `t "energy correlators" and t top`
- `abstracts.value:"energy correlator" and abstracts.value:"top quark mass"`
- `t "energy-energy correlation" and (CMS/ATLAS) and date > 2018`
- `t "three-point energy correlator"`
- `t "top quark mass" and t boosted and (CMS/ATLAS)`
- `cites 2201.08393; cites 2311.02157`
- `WebSearch: CMS energy correlator boosted top quark jets measurement top mass PAS`
- `WebSearch: ATLAS OR CMS energy correlators top quark jets 2025 2026`
- `abstracts.value:"energy correlator" and abstracts.value:"new physics"`
- `abstracts.value:"energy correlator" and (resonance or boosted)`
- `t "low mass" and t "quark-antiquark" and collaboration:CMS`
- `t "dark photon" or leptophobic boosted (CMS/ATLAS)`
- `t instanton and (CMS/ATLAS/TOTEM/H1)`
- `t instantons and t LHC and date > 2018`
- `t "QCD instanton" and date > 2022`
- `abstracts.value:"instanton" and abstracts.value:"forward proton"`
- `WebSearch: CMS search QCD instanton induced events multiplicity 13 TeV`
- `pdf read: 2605.28934, 2012.09120, 2104.01861, 2505.17850`
</details>

## C061 - verdict: **NARROWED** (confidence medium-high)
**Claim:** Triple/quadruple Higgs production beyond the 6b final state (bbbb tautau, bbbb WW, 4b gamma gamma, multilepton, resonant X->SH->HHH, 8b HHHH, quartic coupling) is not covered by CMS/ATLAS.

**Surviving gap:** Only non-6b, non-4b2gamma HHH channels (chiefly 4b+tautau, possibly 4b+multilepton/WW) and a multi-channel HHH (6b+4b2gamma+4btautau) combination with an HL-LHC projection survive; no CMS/ATLAS result found for these. 8b HHHH has only phenomenology (2608.16998) and is SM-rate-dead; only meaningful as resonant S->hhhh / h3->h2h2 cascades. Gap type: searched-limited-regime. The 6b (non-resonant + resonant TRSM cascades), 4b2gamma, kappa3/kappa4 constraints and 6b HL-LHC projection are already done.

**Bundle split:**
- HHH->6b nonresonant/kappa3-kappa4: **DIES** - ATLAS 2411.02040, CMS 2607.05145 (CMS-PAS-HIG-24-012), ATLAS HL-LHC projection ATL-PHYS-PUB-2025-003 (recid 2893567)
- HHH->4b2gamma: **DIES** - CMS-PAS-HIG-24-015 (recid 2945642): Run-2 138 fb-1, limits on HHH xsec and lambda3/lambda4
- Resonant X->SH->HHH cascades: **DIES (6b) / NARROWED (other channels)** - ATLAS 2411.02040 Resonant + Heavy-resonant searches (TRSM 325<=mX<=575, 200<=mS<=350 GeV, plus generic X,S); recast/HL projections 2606.01966, 2501.14866
- HHH->4b tautau / multilepton: **SURVIVES (weakly)** - No CMS/ATLAS result or HL projection found; pheno exists only at 100 TeV (2504.04037; 1704.04298)
- HHHH 8b / quartic: **NARROWED to BSM-resonant** - Pheno HL-LHC study 2608.16998 already gives c3,d4 and resonant S->hhhh; SM rate unobservable

**Kill evidence:**
- arXiv:2411.02040 (Abstract; Sec.1 (lines on TRSM/DM-CPV); Sec.3 signal samples): ATLAS HHH->6b, 126 fb-1, nonresonant + resonant (TRSM, DM-CPV, generic heavy X,S) interpretations; SM xsec 0.079 fb at 13 TeV used
- arXiv:2607.05145 (Abstract): CMS nonresonant HHH->6b, 138 fb-1, boosted/resolved topologies, limit 44 (43) fb = 588 (572) x SM; -177<kappa4<185
- CMS-PAS-HIG-24-015 (INSPIRE 2945642) (Abstract): CMS HHH->4b2gamma Run 2, limit 244 (152) fb, interpreted in lambda3, lambda4
- ATL-PHYS-PUB-2025-003 (INSPIRE 2893567) (Abstract): ATLAS HL-LHC projection of HHH->6b, 1-3 ab-1 at 14 TeV, kappa3/kappa4 constraints
- arXiv:2608.16998 (Abstract): HL-LHC phenomenology of HHHH 8b with c3,d4 constraints and resonant S->hhhh, h3->h2h2 cascades

**Closest existing:**
- arXiv:2411.02040 [ATLAS]: covers 6b nonres + resonant cascades; gap: no tau/lepton/photon HHH channels
- arXiv:2607.05145 [CMS]: covers 6b nonres all boost regimes; gap: nonresonant only; 6b only
- CMS-PAS-HIG-24-015 [CMS]: covers 4b2gamma HHH; gap: no HL-LHC projection seen; no combination with 6b seen

**HL-LHC projection docs:** ATL-PHYS-PUB-2025-003 (ATLAS HHH 6b HL-LHC); pheno: 2312.04646 (GNN HHH HL-LHC), 2606.01966 (recast + HL TRSM), 2501.14866, 2608.16998 (HHHH). No CMS HHH HL-LHC projection found (not proof of absence).

**Showstoppers:** SM sigma(HHH)=0.079 fb at 13 TeV (2411.02040 Sec.3) -> O(few hundred) events at 3 ab-1 before BR; 4b-tautau BR fraction of order 6% (estimate from standard Higgs BRs, UNVERIFIED) -> O(10) produced SM events before efficiency: SM HHH is unobservable in any channel; only large kappa4 (O(100)) or resonant BSM enhancement is testable. Tau trigger/ID plus 4b in 200 PU is hard. HHHH: SM rate effectively zero.

**Notes:** Scout's 'open' list was largely already done: 4b2gamma (CMS PAS) and resonant HHH (ATLAS 6b) exist. ATLAS thesis INSPIRE 3073505 also documents the 6b search and BSM models. Remaining channel novelty is marginal: an incremental channel addition to an HHH combination with very low SM rate; value lies in BSM-resonant HHH in tau channels and the combination.

<details><summary>Queries run</summary>

- `t triple Higgs or t HHH`
- `t "three Higgs" and date > 2023`
- `abstracts.value:"triple Higgs" and collaboration:CMS`
- `abstracts.value:"HHH" and (collaboration:CMS or collaboration:ATLAS)`
- `t "quartic Higgs" or t "quartic self-coupling" and date > 2022`
- `t triple Higgs and (t tau or t lepton or t multilepton)`
- `t four Higgs or t quadruple Higgs or t HHHH`
- `t "triple Higgs" and t HL-LHC`
- `abstracts.value:"triple Higgs" and abstracts.value:"HL-LHC" and date > 2023`
- `abstracts.value:"triple Higgs" and abstracts.value:"tau"`
- `abstracts.value:"HHH" and abstracts.value:"leptons" and date > 2022`
- `t HL-LHC and t "Higgs boson pair" and date > 2024 and (collaboration:CMS or collaboration:ATLAS)`
- `abstracts.value:"X -> SH" or t "scalar particle and a Higgs"`
- `abstracts.value:"6b" and abstracts.value:"resonant" and date > 2023`
- `cites arxiv:2407.03015 / 2411.02040 / 2312.04646 (mostrecent, 100 each)`
- `pdf grep 2411.02040`
</details>
