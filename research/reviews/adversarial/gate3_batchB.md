# Gate 3 adversarial novelty review - batch B (C009, C013, C015, C017)
Reviewer: adversarial agent B. Sources verified via INSPIRE (tools/inspire.py) and PDF text (tools/arxiv_pdf.py). "Not found" is not proof of absence.

## C009 - verdict: **NARROWED** (confidence medium)
**Claim:** No CMS/ATLAS analysis targets semi-visible / semi-dark Higgs decays (h->Z(ll)X with X invisible, or non-resonant h->ll+MET / jj+MET from dark-sector EFT operators), so a dedicated HL-LHC search would fill a gap left by H->invisible and H->gamma+gamma_D searches.

**Surviving gap:** (a) h->Z X(inv) [semi-dark, resonant Z]: no dedicated CMS/ATLAS search found; it is a gap, but the physics room is small. The best published HL-LHC phenomenology study (2206.01214, ZH->4l+MET, NN) reaches BR(h->ZX)xBR(X->inv) ~ 2.8 x BR(h->Z nu nu)_SM ~ 1.5% at 2 sigma. That is only about 2-8x stronger than the indirect bound from HL-LHC H->inv (h->Z(nu nu)X counts as invisible) and from the Higgs-rate global fits. What survives is a dedicated h->Z+MET search that combines the ZH(4l+MET), VBF and boosted ggF categories and is interpreted for ALP/2HDM+a/dark photon X in m_X ~ 1-30 GeV. Its value is modest unless several production modes are combined. (b) Non-resonant h->ll+MET / jj+MET (DSMEFT, 2511.09778): no experimental search found, but the claimed HL-LHC reach is not credible as it stands (see showstoppers). It needs a re-study with the full background set before it can count as an analysis gap.

**Kill / narrowing evidence:**
- arXiv:1902.00134: The HL-LHC Yellow Report (WG2) uses a combined VBF+VH projected limit mu*BR_inv <= 2.5% (Eq. 126). Since BR(Z->nu nu) ~ 20%, h->ZX with X invisible feeds h->inv at ~0.2*BR(h->ZX). That indirectly caps BR(h->ZX) at roughly 12% (my estimate, not in the source). The Higgs-rate global fit (Table 78, values not read: UNVERIFIED) also constrains BR(h->ZX) generically. So the direct search competes with existing HL-LHC projections over only a narrow window. (Sec. 6.2.1 Eq. (126); Sec. 6.2.2 / Table 78)
- arXiv:2206.01214: The HL-LHC phenomenology for the semi-dark mode already exists: ZH, 4l+MET, NN analysis, 2 sigma reach BR x BR = 2.8 x BR(h->Z nu nu)_SM for m_X = 1 GeV at 3 ab^-1 (BR(h->Z nu nu)_SM = 5.4e-3 quoted). The seed's 'quantitative study is future work' quote (2511.09778) is therefore partly superseded for the resonant-Z case. (Sec. III, Figs. 2-3, text near Fig. 3)
- arXiv:2511.09778: Background list for ZH(Z->jj), H->ll+MET (Table II b) is only ZH-lep, ZH-W, ZZ, ZZZ, WWZ, ttZ, tWZ, tt-inc. It omits Z/gamma*->tautau+jets, WW+jets, WZ and W+jets fakes. All of these naturally give m_ll<60 GeV, MT(ll,MET)<125 GeV and modest MET, the very region the signal selects. The quoted sigma_bkg = 1.5 fb after cuts is therefore not reliable. The same region is also the SM H->WW*->l nu l nu phase space. (Sec. V.B, Table II, text after Table I)

**Closest existing results:**
- arXiv:2111.08372 [ATLAS]: covers ZH, Z->ll, H->invisible (and DM), BDT; full Run 2; gap: Leptons are from the associated Z. It does not target h->Z(ll)X, where the dilepton comes from the Higgs decay and MT(ll,MET)<m_h.
- arXiv:1908.02699 / arXiv:2212.09649 [CMS / ATLAS]: covers ZH, H->gamma + gamma_D (massless dark photon), ll+gamma+MET; gap: Photon, not Z, accompanies the invisible state. This is the closest semi-visible Higgs analysis by topology and shows the analysis strategy (MT endpoint) is standard.
- arXiv:2312.01942, arXiv:2411.16361 [ATLAS]: covers h->Za with a->gamma gamma and a->hadrons (light a); gap: a decays visibly. a->invisible (or long-lived beyond the detector) is not covered.
- arXiv:2111.01299 [CMS]: covers H->Z Z_d / Z_d Z_d -> 4l, low-mass dilepton resonances; gap: Visible Z_d only.
- arXiv:2301.10731 [ATLAS]: covers H->invisible combination, Run 2; gap: Fully invisible only; indirectly constrains h->Z(nu nu)X.

**HL-LHC projection docs:** arXiv:1902.00134 (HL-LHC YR WG2 Sec. 6: H->inv projections, indirect undetected-BR fits); arXiv:2206.01214 (phenomenology HL-LHC projection for h->ZX, 300 fb^-1 and 3 ab^-1). I found no CMS/ATLAS Phase-2 projection note specific to h->Z+invisible.

**Showstoppers:** Rate: the clean ZH->4l+MET channel has only ~1.4 fb selected signal for BR=1 (2206.01214), so ~20 events per 1% BR at 3 ab^-1 before NN. Background: ggF h->Z(ll)X has low MET (<~40 GeV), so DY+jets with fake MET under 140-200 PU dominates, and Phase-2 MET resolution is critical. Model: the DSMEFT h->ll+MET study omits the dominant tautau/WW backgrounds. The O_e phi-type operators are unitarity-limited per the paper's own Fig. 9. Competition: h->inv and coupling fits already bound the same BR at the few-percent level.

**Notes:** The ATLAS Run-2 exotic Higgs summary (2405.04914) lists h->Za only with visible a decays and H->inv; it does not list h->Z+inv. A CMS exotic Higgs proceedings item (INSPIRE 2759006) was not read. The two seeds are split here: semi-dark resonant (a) is a narrow genuine experimental gap with marginal reach; non-resonant DSMEFT (b) is a theory/phenomenology idea whose quoted sensitivity is unreliable. 2201.04658 (dark photon from semi-invisible Higgs decay, phenomenology) was not read in detail.

**Queries run:**
- `inspire: cites arxiv:2206.01214`
- `inspire: cites arxiv:2511.09778`
- `inspire: cites arxiv:2607.09344`
- `inspire: (collaboration:CMS or collaboration:ATLAS) and t higgs and t invisible and t Z`
- `inspire: (CMS or ATLAS) and abstracts.value:"Z boson" and "dark photon" and "Higgs" date>2017`
- `inspire: (CMS or ATLAS) and t higgs and t "dark photon"`
- `inspire: (CMS or ATLAS) and abstracts.value:"semi-visible" and Higgs`
- `inspire: (CMS or ATLAS) and t axion-like and t Z and t higgs`
- `inspire: (CMS or ATLAS) and t higgs and t "Z boson" and t light and (t resonance or t pseudoscalar)`
- `inspire: (CMS or ATLAS) and abstracts.value:"Z+invisible"`
- `inspire: (CMS or ATLAS) and "missing transverse momentum" and "exotic decays of the Higgs"`
- `inspire: (CMS or ATLAS) and t "Z boson" and t "missing transverse momentum" date>2019`
- `inspire: collaboration:CMS and Higgs boson + Z boson + invisible date>2018`
- `inspire: t undetected and t higgs and t HL-LHC`
- `web: CMS OR ATLAS search Higgs decay Z plus invisible dark photon MET`
- `web: HL-LHC projection Higgs untagged BR global fit 3000 fb-1`
- `pdf grep: ATLAS Run-2 exotic Higgs summary 2405.04914 for h->Za / semi-dark / invisible`

## C013 - verdict: **NARROWED** (confidence medium-high)
**Claim:** Bundle: (a) millicharged particles (~e/10-e/3) in the CMS/ATLAS main detectors with Phase-2 dE/dx and timing; (b) fractionally charged particles; (c) high-charge |z|>7 states, where ATLAS's multi-charged search stops at z=7. The claim is that these regions are left open by current searches.

**Surviving gap:** Only two small pieces survive. (1) Phase-2 strategy for FCPs (e/3 to ~0.9e) under binary outer-tracker readout: the Run-2 CMS method relies on strip dE/dx, which the Phase-2 Outer Tracker does not provide. A redesigned HL-LHC FCP search would need pixel ToT dE/dx, the pattern of hits missing below threshold, MTD timing, and the L1 track trigger. I found no HL-LHC FCP projection, so this is 'LHC-not-projected-to-HL'. (2) A residual high-charge window at |z| ~ 8-9 (between ATLAS z<=7 and MoEDAL z>=10 / ATLAS HECO z>=20), and |z| 10-19 where only MoEDAL, with 6.46 fb^-1, has results. Part (a), millicharged in the main detectors below ~e/3, is effectively dead.

**Kill / narrowing evidence:**
- arXiv:2308.04835: ATLAS Run-2 (138 fb^-1, dedicated HIP trigger) high-electric-charge objects with 20 <= |z| <= 100, spin-0 and spin-1/2, Drell-Yan AND photon-fusion. This contradicts the seed's implication that |z|>7 is uncovered and that photon fusion is not considered. (Abstract)
- arXiv:2311.06509: MoEDAL full detector, Run 2 (6.46 fb^-1): HECOs with charge 10e-400e, spins 0, 1/2 and 1, DY + photon fusion. This covers the |z|>7 region and spin-1, so the 'spin, production assumptions' gap is partly addressed. (Abstract)
- arXiv:2303.13613: The ATLAS multi-charged search (z=2-7) already uses DY (gamma+Z) plus photon-fusion production. (Sec. 1 (line ~77) and Sec. 3 (signal model))
- arXiv:2402.09932: CMS Run-2 FCP search covers charges e/3 to 0.9e (and 2e/3), with masses excluded up to 640 GeV. The method needs low-dE/dx strip hits (lower threshold 0.25 MeV/cm) and a single-muon trigger. Charges below e/3 are not accessible: ionisation scales as Q^2, so hits fall below the readout threshold (signal-loss discussion). (Abstract; Sec. 3-4 (lines ~159-164, ~300))
- arXiv:2104.07151: The milliQan HL-LHC projection already covers 0.0018e-0.3e for masses of 10 MeV-80 GeV, so the millicharged window is the territory of a dedicated detector, not CMS/ATLAS main-detector tracks. (Abstract)
- arXiv:2010.07941: FORMOSA (forward) is proposed for millicharged particles in the 10 MeV-100 GeV mass range. (Abstract)
- arXiv:1912.02061: The CMS Phase-2 Outer Tracker strips are read out by the CMS Binary Chip (binary hits, no analogue amplitude). The strip-dE/dx observable of the Run-2 FCP method therefore disappears at HL-LHC. This is a showstopper for a straight extrapolation and a reason any Phase-2 FCP search must be redesigned. (Sec. on module readout (CBC description, ~line 181 of text))

**Closest existing results:**
- arXiv:2402.09932 [CMS]: covers FCP e/3-0.9e, 138 fb^-1, tracker dE/dx; gap: No Phase-2 projection; Phase-2 OT binary readout removes the main observable; <e/3 inaccessible.
- arXiv:2303.13613 [ATLAS]: covers multi-charged z=2-7, spin-1/2, DY+PF; gap: z>7 fails muon reconstruction; spin-0 not shown here (spin-0 is covered by MoEDAL/HECO for z>=10/20).
- arXiv:2308.04835 [ATLAS]: covers HECO 20<=|z|<=100 and monopoles, DY+PF, spin 0 and 1/2; gap: 8<=|z|<=19 not covered by ATLAS.
- arXiv:2311.06509 [MoEDAL]: covers HECO 10e-400e, spins 0/1/2/1, 6.46 fb^-1; gap: Low luminosity; |z| 8-9 not covered.
- INSPIRE:2961278 [ATLAS]: covers PUB-type note: simulation and expected performance of FCPs in ATLAS (2023); gap: Suggests an ATLAS FCP search is in preparation (UNVERIFIED); it would further reduce any FCP gap.

**HL-LHC projection docs:** arXiv:2104.07151 (milliQan HL-LHC); arXiv:2010.07941 and arXiv:2504.12973 (FORMOSA / ESPPU input). I found no CMS/ATLAS HL-LHC projection for FCP or multi-charged/HECO searches by title (not proof of absence).

**Showstoppers:** (a) Millicharged in the main detector: dE/dx scales as Q^2, so e/10 deposits ~1% of a MIP, far below the pixel and strip thresholds. Tracks are not reconstructed and there is no trigger; the Run-2 FCP search needs a muon trigger and already stops at e/3. Dedicated detectors (milliQan, FORMOSA) are far more sensitive below ~0.3e. (b) Phase-2 CMS OT binary readout removes strip dE/dx; only pixel ToT (coarse) and the MTD remain. HL-LHC pileup increases the rate of fake low-dE/dx tracks. (c) High-z: the HIP-trigger and TRT-based technique already exists. Extending ATLAS multi-charged to z=8-19 is incremental, and ATLAS Phase-2 removes the TRT, which the HECO analysis relies on (TRT role in 2308.04835: UNVERIFIED in detail).

**Notes:** The bundle is split. Millicharged in the main detector: DIES (physical showstopper plus dedicated experiments). FCP e/3-0.9e: searched-limited-regime, with a real technical HL-LHC question (binary OT readout). High-charge: largely covered (ATLAS z 2-7 and 20-100, MoEDAL 10-400), leaving a tiny |z|~8-9 window. The phenomenology paper 2507.16900 (FCPs with two representations, colored FCPs) could motivate new interpretations of existing searches rather than a new analysis. The lower-z edge of MoEDAL (10e) was read from the abstract; the exact per-spin coverage was not checked.

**Queries run:**
- `inspire: (CMS or ATLAS or MoEDAL) and (t "high electric charge" or t "highly ionising/ionizing" or t "high-electric-charge")`
- `inspire: (CMS or ATLAS) and (t multi-charged or t multiply charged or t fractionally charged or t fractional charge)`
- `inspire: (CMS or ATLAS) and t monopole`
- `inspire: collaboration:ATLAS and t magnetic monopoles and t high-electric-charge and date>2022`
- `inspire: abstracts.value:"high-electric-charge" and date>2022`
- `inspire: t millicharged and (t HL-LHC or High-Luminosity or FORMOSA or milliQan or SUBMET or FPF)`
- `inspire: t "Phase-2 Upgrade of the CMS Tracker"`
- `inspire: (CMS or ATLAS) and (t heavy stable charged or t long-lived charged) and (HL-LHC or Phase-2 or timing)`
- `inspire: t millicharged and (t CMS or t ATLAS or t main detector or t general purpose)`
- `inspire: abstracts.value:"fractionally charged" and date>2023 (mostrecent)`
- `web: CMS Phase-2 outer tracker binary readout no dE/dx HSCP pixel ToT`
- `pdf grep: 2402.09932 trigger/threshold/charge range; 2303.13613 production modes`

## C015 - verdict: **NARROWED** (confidence high)
**Claim:** Bundle: (a) long-lived ALPs from exotic top decays t->q a (q=u,c) at intermediate lifetimes are claimed to be unsearched by CMS/ATLAS; (b) prompt flavour-violating t->q a (a->gamma gamma, mu mu, jj) is claimed to be untested; (c) long-lived ALPs from h->aa with displaced calorimeter deposits are claimed to be unstudied for HL-LHC.

**Surviving gap:** Long-lived t->q a with LIGHT ALPs (m_a ~ 1-35 GeV, the 2202.09371 benchmarks m_a = 2 and 10 GeV) decaying in the HCAL or muon system (c tau ~ 0.01-10 m) in lepton-triggered ttbar events. The leptonic ALP decays (displaced mu mu / gamma gamma) from top decays are also open. ATLAS has already done the ID-DV version for 40-55 GeV (2403.15332). The Higgs part (c) and generic h->aa long-lived searches are well covered. The prompt part (b) is narrowed to a->gamma gamma / mu mu from top decay (t->qX with X->bb is covered by ATLAS 2301.03902). Much of what survives could be met by adding top-decay signal interpretations to existing ATLAS CalRatio W/Z+LLP and CMS muon-detector-shower analyses. A wholly new analysis is not needed.

**Kill / narrowing evidence:**
- arXiv:2403.15332: ATLAS (140 fb^-1, ID displaced vertices, 1-lepton region) explicitly searches for long-lived ALPs from t->ac/au in ttbar with a->cc/gg. It excludes BR(t->aq) > 0.1% for 1.6 < c tau < 130 mm at 40 < m_a < 55 GeV ('Long-lived ALPs produced via t->aq are probed for the first time'). This directly contradicts the seed's 'no top-tagged displaced ALP search seen'. (Abstract; benchmark description ~lines 56-61, 117-124; 1-lepton SR ~line 140; Summary ~lines 341-344)
- arXiv:2404.06126: A phenomenology recast of the ATLAS DV+jets search for LL ALPs from top decays, with an HL-LHC (3 ab^-1) projection already provided. (Abstract; Sec. 3.1, App. A)
- arXiv:2202.09371: The original proposal already includes HL-LHC background-free 10-event lines for HCAL and muon-system decays, down to BR(t->aq) ~ 1e-8. The HL-LHC phenomenology is done; what is missing is the experimental analysis. (Sec. 4 (text before Conclusions), Fig. 7 (Appendix))
- arXiv:2301.03902: ATLAS prompt t->qX (q=u,c), X->bb search covers the prompt hadronic FCNC top->light scalar case. (Abstract)
- arXiv:2312.03306: ATLAS H->aa->4gamma with short- and long-lived ALPs. Together with ATLAS 2407.09183 (CalRatio incl. W/Z+LLP channels), the Higgs-decay long-lived ALP part of the bundle is well covered, so seed S122's Higgs component dies. (Abstract)

**Closest existing results:**
- arXiv:2403.15332 [ATLAS]: covers t->aq, a->cc/gg, ID DV, m_a 40-55 GeV, c tau 1.6-130 mm (BR>0.1%); gap: m_a < 40 GeV not interpreted for top; decays beyond the ID (c tau > ~0.2 m) not covered; leptonic/photonic a decays not covered.
- arXiv:2407.09183 [ATLAS]: covers LLP decays in HCAL, with W/Z(leptonic)+LLP channels; gap: Not interpreted for ttbar t->qa; the 1-lepton channel is likely recastable (UNVERIFIED).
- arXiv:2301.03902 [ATLAS]: covers prompt t->qX, X->bb; gap: X->gamma gamma/mu mu and light m_X (< ~20 GeV) not covered (mass range not read: UNVERIFIED).
- arXiv:2304.14247 [ATLAS]: covers ttbar + a(->mu mu) associated production (3-lepton); gap: Associated production, not t->qa decay; prompt only.
- arXiv:2112.13769 [CMS]: covers displaced dimuons via scouting, model-independent limits; gap: Not interpreted for top decays; recastable for a->mu mu.

**HL-LHC projection docs:** Phenomenology only: arXiv:2202.09371 (HL-LHC 4 ab^-1 lines, Fig. 7), arXiv:2404.06126 (HL-LHC 3 ab^-1), arXiv:2307.11154 (rare top decays to light singlets at HL-LHC, including LLP signals). I found no CMS/ATLAS Phase-2 projection for t->qa.

**Showstoppers:** The ALP with only top-flavour-violating couplings must still decay. Its decay to hadrons/photons proceeds through loop-induced or additional couplings, so the a->cc/gg/gamma gamma branching ratios are model-dependent. Low-mass ALPs (2 GeV) give highly collimated decays that are hard to vertex in the ID with 200 PU. For HCAL/MS decays, the trigger in ttbar is the lepton, so trigger is not a showstopper. Flavour constraints from B/K decays (2402.14232, 2507.19578) restrict the low-mass region for the up-type FV couplings that also induce loop-level down-type couplings (extent not checked: UNVERIFIED).

**Notes:** The seed's own exp_coverage listed 2403.15332 but marked its top interpretation UNVERIFIED. It is verified here, and it is a direct hit for m_a = 40-55 GeV. The surviving gap is mostly an interpretation/extension (lower m_a, calorimeter/MS volumes, leptonic decays), so it is low-hanging but modest in novelty. ATLAS PUB-type record INSPIRE:2903120 (LL ALP constraints from exotic Higgs searches) further covers the Higgs part.

**Queries run:**
- `inspire: (CMS or ATLAS) and t top and (t axion-like or t ALP or t pseudoscalar or t light scalar) and date>2018`
- `inspire: (CMS or ATLAS) and t top and (t long-lived or t displaced)`
- `inspire: (CMS or ATLAS) and t flavour-changing and t top and t scalar`
- `inspire: cites arxiv:2202.09371`
- `inspire: cites arxiv:2306.08686`
- `inspire: cites arxiv:2404.06126`
- `inspire: (CMS or ATLAS) and abstracts top-quark decays and (light scalar or new scalar or pseudoscalar or axion)`
- `inspire: (CMS or ATLAS) and abstracts long-lived and top quark date>2019`
- `inspire: (CMS or ATLAS or LHCb) and t axion-like and (t displaced or t long-lived)`
- `inspire: t top and t long-lived and (decays or ALP or scalar) non-collab`
- `pdf grep: 2403.15332 for top/ALP benchmark and limits`
- `pdf grep: 2202.09371 and 2404.06126 for recast/HL-LHC statements`

## C017 - verdict: **NARROWED** (confidence medium-high)
**Claim:** CMS/ATLAS HNL searches assume pure Majorana or Dirac limits and/or combine OS+SS dilepton samples. The LNV/LNC (SS/OS) ratio and the time-resolved heavy neutrino-antineutrino oscillation pattern of pseudo-Dirac HNL pairs, which encode the mass splitting, are not exploited.

**Surviving gap:** Only the intermediate mass-splitting regime survives as an experimental gap: measuring R_ll = LNV/LNC (between the Dirac 0 and Majorana 1 limits) as a function of reconstructed proper decay time in displaced-vertex W->l N events, and interpreting limits as a function of Delta m in the 2QDH/pSPSS model. HL-LHC phenomenology exists (2212.00562, CMS-like Delphes), but no experimental result does this. The window is small: resolvable oscillations need c tau_osc ~ mm-cm and long-lived N (m_N ~ 5-20 GeV, |theta|^2 ~ 1e-7-1e-6). Current ATLAS/CMS displaced HNL limits already reach that region, so the HL-LHC event yield in the surviving window may be too small to resolve oscillations. The prompt OS/SS split part of the claim is dead.

**Kill / narrowing evidence:**
- arXiv:2503.16213: ATLAS displaced HNL (140 fb^-1) interprets both 1SFH and two-quasi-degenerate-HNL (2QDH) models, separating LNC and LNV decays. The 'Dirac limit = zero mass splitting' and 'Majorana limit = small nonzero splitting enabling oscillations' are stated explicitly. Dirac-like and Majorana-like HNLs below 14.5 GeV are excluded down to mixing ~1e-7. This kills 'searches assume only Majorana or Dirac'; only the intermediate splitting is missing. (Abstract; Sec. 2 (lines ~82, 114-116, 325-341), Table 1)
- arXiv:2204.11988: Earlier ATLAS displaced-dilepton HNL search: 2QDH model, LNC-only (Dirac limit) and LNC=LNV (Majorana limit) interpretations, constrained by neutrino oscillation data for normal/inverted hierarchy. (Sec. 1 (lines ~45-46, 88-90))
- arXiv:2403.00100: CMS prompt HNL search (e, mu, tau_h final states) gives separate limits for Majorana (LNV+LNC) and Dirac (LNC only) HNLs, with same- and opposite-charge categories. The 2016 complaint (1607.05641) that 'CMS gives only combined OS+SS results' is outdated. (Abstract; Sec. 1-3 (lines ~101-109, 246))
- arXiv:2201.05578: CMS displaced HNL search gives separate Dirac and Majorana interpretations, with LNC/LNV distinguished by lepton charges. (Abstract; Sec. 2-4 (lines ~127, 168, 268-271))
- arXiv:2212.00562: A full HL-LHC phenomenology study of resolving N-Nbar oscillations with a CMS-like Delphes simulation already exists, for benchmarks m_N = 14 GeV, |theta_mu|^2 = 1e-7, Delta m = 83-743 micro-eV, c tau_osc = 1.7-15 mm. The phenomenology is done; the authors ask collaborations for DV-resolution information. The benchmark mass and mixing sit at the edge of the region ATLAS 2503.16213 reports as excluded (exact overlap UNVERIFIED). (Abstract; Table 1; Sec. 4 (lines ~422-434))

**Closest existing results:**
- arXiv:2503.16213 [ATLAS]: covers displaced W->lN, leptonic and semileptonic DV; 1SFH and 2QDH in Dirac/Majorana limits; LNC/LNV separated; gap: No intermediate-Delta m / time-dependent R_ll interpretation.
- arXiv:2201.05578 [CMS]: covers displaced HNL, Dirac and Majorana; gap: Same: endpoints only.
- arXiv:2403.00100 [CMS]: covers prompt HNL, 3l incl. tau_h, Dirac and Majorana, SS/OS categories; gap: Prompt regime: oscillations are averaged out, so only R_ll endpoints (or an intermediate R_ll reinterpretation) are possible. This is a reinterpretation, not a new analysis.
- arXiv:2204.11988 [ATLAS]: covers displaced dilepton DV HNL, 2QDH; gap: Endpoints only.

**HL-LHC projection docs:** arXiv:2212.00562 (HL-LHC, CMS-like Delphes, oscillation resolution); arXiv:2606.25982 (LHC/FCC-hh sensitivities, LN-blind vs LNV for pseudo-Dirac); arXiv:2203.08039 (HNL status review). Related phenomenology: 1709.03797, 1905.03097, 2210.10738, 2307.06208 (decoherence). I found no CMS/ATLAS HL-LHC projection note for oscillation resolution.

**Showstoppers:** Statistics: resolving an oscillation pattern needs many signal events with good proper-time reconstruction. This requires a full N reconstruction (semileptonic N->l pi / l jj; the leptonic N->l l nu loses the neutrino, degrading the boost estimate) and DV position resolution. Parameter space: the needed (m_N ~ 10-15 GeV, |theta|^2 ~ 1e-7) region overlaps with the existing ATLAS Run-2 exclusion, so the HL-LHC surviving window is narrow. Decoherence/damping effects (2307.06208, 2606.25982) modify the pattern and are model-dependent. Charge misidentification for displaced tracks dilutes LNV/LNC tagging. The trigger is fine (prompt lepton from W).

**Notes:** Bundle split: (i) the prompt SS-vs-OS / e-mu exploitation claim (seed S141, based on a 2016 paper) DIES, because the current CMS and ATLAS results separate LNC/LNV and provide Dirac and Majorana limits. (ii) Time-resolved N-Nbar oscillations and intermediate-Delta m interpretation in displaced searches survives as 'one-observable-not-another', but the phenomenology is mature and the viable parameter window is squeezed by Run-2 limits. A cheaper first step is to reinterpret the existing Dirac/Majorana endpoint limits in terms of R_ll(Delta m), which the 2QDH framework of ATLAS already supports. The 2606.25982 abstract claim about damped oscillations alleviating the LNV suppression was read from the abstract only. 2508.20929 (ATLAS prompt) targets the LNV scenario only and was not checked in detail.

**Queries run:**
- `inspire: (CMS or ATLAS) and (t heavy neutral lepton or t heavy neutrino or t Majorana neutrino) and date>2021`
- `inspire: (CMS or ATLAS or LHCb) and abstracts Dirac and (t heavy neutral or t heavy neutrino)`
- `inspire: cites arxiv:2212.00562`
- `inspire: cites arxiv:2606.25982`
- `inspire: cites arxiv:1607.05641`
- `inspire: (CMS or ATLAS or LHCb) and abstracts oscillation and heavy neutral lepton`
- `inspire: t heavy neutrino and t oscillations and (t LHC or t HL-LHC or t W boson)`
- `inspire: (CMS or ATLAS) and abstracts opposite-sign and (heavy neutrino or heavy neutral lepton)`
- `pdf grep: 2204.11988, 2503.16213, 2508.20929 for pseudo/quasi-Dirac, LNC, oscillation, mass splitting`
- `pdf grep: 2403.00100, 2201.05578 for Dirac/Majorana treatment`
- `pdf grep: 2212.00562 for benchmarks and experimental requests`
