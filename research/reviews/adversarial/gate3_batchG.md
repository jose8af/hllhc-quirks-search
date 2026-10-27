# Gate 3 adversarial novelty review: batch G

Reviewer: adversarial novelty reviewer (independent). Candidates: C064, C066, C069. Source of truth is gate3_batchG.json.

## C064: NARROWED

**Claim.** Bundle: (a) A->ZH (lltt, nunubb) as FOEWPT smoking gun lacks a CMS counterpart and VBF/V-associated X->Zh CP-violation probes are unexplored; (b) light H+ (m<mt) in t->bH+ with H+->WZ has no dedicated search; (c) heavy->light scalar cascades X->YY->4b / X->SH lack coverage and HL-LHC projections.

**Surviving gap.** (a) DIES as stated: CMS has an A->Z(ll)H(tt) result (138/fb, trilepton + all-hadronic combination, INSPIRE recid 3188772, 2026) and the ATLAS lltt/nunubb paper (2311.04033); a pheno HL-LHC lumi-rescaled projection exists (2309.17431 Sec. 3.3/App. B). V-associated Ha->Zh is rate-killed in the C2HDM (2507.05942 Sec. III, Fig. 3: 'impossible to probe at the HL-LHC with 3 ab-1'); VBF set aside by the same authors because ggF contamination needs better q/g tagging. Residual: an official ATLAS/CMS HL-LHC projection of A->ZH (lltt/nunubb), not in the 2025 ATLAS+CMS HL BSM-scalar projections (2504.00672 cover S->HH/ZZ). (b) NARROWED: a dedicated t->bH+, H+->WZ(*) search with an explicit m(H+) reconstruction (3l/4l + b), motivated only in triplet/Georgi-Machacek models (loop-suppressed in 2HDM); currently only a ttZ-differential recast (2509.07094) sets sub-permille BR limits, and existing GM H+->WZ searches are VBF and m>=200 GeV. (c) NARROWED: X->SH/YH is well covered (CMS 4b 2605.02848 & 2204.12413, bbgg 2508.11494; ATLAS 2307.11120, 2405.20926); the open piece is X->YY->4b with both daughters non-SM, m_Y ~20-120 GeV and m_X in the few-hundred-GeV range (resolved/boosted), plus Vh2, h2->h1h1->4b with m(4b) != 125 GeV (ATLAS 2507.01165 fixes the parent to the 125 GeV H). Pheno HL projections exist for the latter (2603.29395, 2608.23183).

**Confidence:** medium

**Kill / narrowing evidence**

- INSPIRE recid 3188772 (CMS note, 2026, no arXiv) (Abstract): CMS search for A->Z(ll)H(tt semileptonic), 138/fb, three-lepton events, combined with an all-hadronic tt search; kills 'no CMS counterpart'
- arXiv:2311.04033 (Title/abstract): ATLAS A->ZH in lltt and nunubb, 140/fb
- arXiv:2309.17431 (Sec. 3.3 (text ~p.17) and App. B): HL-LHC projections (300-3000/fb) for A->ZH lltt by rescaling the ATLAS expected limits with sqrt(L), plus a comparison to earlier CMS-based projections
- arXiv:2507.05942 (Sec. II-III, Fig. 3 and footnote 2; discussion of VBF in Sec. I): W/Z-associated Ha->Zh->llbb cross sections in the C2HDM are 'very suppressed, and impossible to probe at the HL-LHC with 3 ab-1'; VBF left aside because ggF contamination requires better quark/gluon tagging
- arXiv:2509.07094 (Abstract; Sec. III, Fig. 2): Recast of CMS+ATLAS ttZ differential measurements gives sub-permille limits on Br(t->H+b)xBr(H+->WZ) for m_H+ < m_t (with a ~2 sigma preference); the light-H+->WZ phase space is therefore already indirectly constrained
- arXiv:2605.02848; arXiv:2204.12413; arXiv:2508.11494; arXiv:2307.11120 (Abstracts): X->YH/SH extensively searched (4b resolved m_X 400-1600 GeV, m_Y 60-1400 GeV; 4b boosted; bbgg; ATLAS l/ll+tautau)

**Closest existing results**

| id | collab | covers | region gap |
|---|---|---|---|
| recid:3188772 | CMS | A->Z(ll)H(tt), 3l + hadronic combination, 138/fb | no nunubb counterpart verified in CMS; no HL projection |
| arXiv:2311.04033 | ATLAS | A->ZH in lltt and nunubb, 140/fb | Run 2 only; HL extrapolation only in pheno (2309.17431) |
| arXiv:1911.03781 | CMS | H->ZA->llbb, 35.9/fb | partial Run 2; reversed hierarchy only |
| arXiv:2104.04762 / arXiv:2207.03925 / arXiv:2407.10798 | CMS/ATLAS | VBF H+->WZ (Georgi-Machacek), m_H+ >= 200 GeV | m_H+ < m_t from top decays not covered |
| arXiv:2412.17584 | ATLAS | Light and heavy H+ from top decays / tH+ association, H+->tau nu, 140/fb | WZ decay not considered |
| arXiv:2605.02848 | CMS | X->YH->4b, m_X 400-1600, m_Y 60-1400 GeV | requires one daughter = SM H; X->YY (both new) not covered |
| arXiv:2507.01165 | ATLAS | ZH, H->aa / a1a2 -> 4b/6b | parent fixed to the 125 GeV Higgs |
| arXiv:2206.09997 / arXiv:2507.17884 | CMS | paired dijet resonances (4j), m_jj>0.2 TeV, m_4j>1.6 TeV (broad-mediator reinterpretation) | high masses, no b-tag; light-Y/intermediate-X 4b not covered |

**HL-LHC projection docs.** ATL-PHYS-PUB-2025-018 / CMS-HIG-25-002, summarized in arXiv:2504.00672 (Sec. 5 and 7: heavy scalar S->HH, ZZ; singlet). No A->ZH, H+->WZ or X->YY HL projection found there. Pheno: arXiv:2309.17431 (A->ZH lltt rescaled to 3000/fb), arXiv:1812.05640 (H->hh, H/A->tt, bbH/A; not A->ZH), arXiv:2507.05942 (W-AP sets), arXiv:2603.29395 and arXiv:2608.23183 (TRSM Vh2, h2->h1h1->4b at 300 and 3000/fb). CMS-PAS-FTR-13-024 (A->Zh->llbb projection, per web search; not verified)

**Showstoppers.** (a) V-AP Ha->Zh is rate-killed in the C2HDM (2507.05942); VBF Ha separation from ggF needs q/g tagging beyond the present state of the art (same ref). (b) In a 2HDM, H+->WZ is loop-induced (tiny BR), so only triplet/GM models motivate it; its signature is ttZ-like with large irreducible ttZ/tWZ background and an off-shell W or Z for m_H+ < m_W+m_Z; the existing recast is already at sub-permille BR. (c) The 4b + low-mass Y regime has heavy QCD multijet background and is trigger-limited at low m_X; Vh2 production of a light h2 is suppressed by mixing (UNVERIFIED magnitude).

**Queries run**

- `collaboration:CMS and t pseudoscalar and t "Z boson" and t heavy and date > 2018`
- `collaboration:ATLAS and (t "A -> ZH" or abstracts.value:"A \to ZH") and date > 2019`
- `collaboration:CMS and abstracts.value:"A to ZH" and date > 2015`
- `collaboration:CMS and t "neutral Higgs" and (t "Z boson" or t ZA) and date > 2015`
- `cites arxiv:2311.04033 (forward citations; found CMS recid 3188772 and thesis recid 2936838)`
- `(A->ZH or H->ZA) and HL-LHC/3000 in abstracts`
- `(CMS or ATLAS) and Zh and vector boson fusion`
- `cites arxiv:2507.05942`
- `(CMS or ATLAS) and t "charged Higgs" and WZ`
- `(CMS or ATLAS) and t "charged Higgs" and t "top quark decays" and date>2019`
- `(CMS or ATLAS) and Georgi-Machacek`
- `cites arxiv:2509.07094`
- `(CMS or ATLAS) and abstracts X \to YH / X \to SH`
- `(CMS or ATLAS) and X->YY / X->SS / pair of light scalars`
- `(CMS or ATLAS) and t "pairs of dijet resonances"`
- `(CMS or ATLAS) and triple Higgs / HHH`
- `cites arxiv:1910.08574; cites arxiv:2209.10996`
- `WebSearch: HL-LHC projection A->ZH ATL-PHYS-PUB OR CMS-PAS-FTR`

**Notes.** The CMS A->ZH->lltt result (recid 3188772) seems to be a CMS public note without arXiv; its PAS number was not retrieved (UNVERIFIED). The CMS UIC thesis (recid 2936838, DOI 10.25417/uic.29049977.v1) is its precursor. The H+->WZ sub-gap depends on the 152 GeV / GM motivation. Of the three, the best-surviving sub-part is (c) X->YY->4b with non-SM daughters, but it is model-dependent (TRSM/NMSSM).

## C066: NARROWED

**Claim.** Bundle of six LQ ideas: (a) resonant single LQ via lepton PDFs, extended to c/s/top-flavoured jets, vector LQ, LFV and HL-LHC; (b) third-generation resonant b+tau, mono-top and mono-jet; (c) U1 with right-handed coupling beta_R and non-minimal kappa; (d) a joint pair+single+t-channel fit with interference at large coupling; (e) HL-LHC follow-up of the CMS 2.8 sigma b-tau excess; (f) photon-PDF uncertainties for vector-LQ limits.

**Surviving gap.** The only clean experimental remnant is resonant lepton-PDF single-LQ production with charm-tagged jets (e/mu + c-jet), and possibly vector-LQ or e-mu-LFV interpretations of the lepton+jet resonance. ATLAS (2507.03650) and CMS (2608.28377, mu only) use light-jet and b-jet categories without c-tagging; the ATLAS+CMS review 2505.08738 (Sec. 4) lists e/mu + light- or charm-flavoured jets as remaining opportunities. A collaboration-level HL-LHC projection of the resonant lepton-quark channel is also missing, but a pheno HL projection exists (2005.06475 Figs. 3-4: HL reach to ~5.7 (4.2) TeV for the u (d) couplings) and 2005.06475 states that s/c couplings are harder to constrain because of PDF suppression. Sub-ideas (b), (c), (e) and (f) DIE. (d) is reduced to reinterpretation level.

**Confidence:** high

**Kill / narrowing evidence**

- arXiv:2503.19836 (Sec. on LQ interpretation, text after Fig. 11 (p.21); coupling scenarios in the model section (around Eq. for U1, p.~19)): ATLAS high-mass tautau measurement with b-jet multiplicity: 'This analysis excludes these benchmark parameter values' (the CMS 2.8 sigma excess benchmark m_LQ = 2 TeV, lambda = 2.5) for scalar and vector LQs. It also includes beta_R = -beta_L and pure right-handed U1 scenarios. This kills (e) and most of (c).
- arXiv:2208.02717 (Sec. 2 (model), Eq. (2) and text below it): CMS tautau vector-LQ interpretation with two benchmarks, beta_R = 0 (BM1) and beta_R = -1 (BM2, Pati-Salam-like); the 'neglected beta_R' claim is already covered experimentally
- arXiv:2308.06143 (Abstract; Sec. 2-4 (btag category, Fig. 3-4)): CMS LQ via tau-quark scattering (lepton PDF), with a btag category and lambda_b-tau interpretation; together with CMS 2308.07826 (single+pair+nonresonant b-tau) this covers the b+tau resonant signature of 2012.11474
- arXiv:2012.11474 (Sec. 7 Conclusions; Figs. 6, 7, 10): The seminal paper itself states that the mono-top and mono-jet final states 'have been targeted at the LHC', and finds b+tau generically stronger than mono-top. It is already an HL-LHC (3 ab-1) projection study.
- arXiv:2606.02067 (Introduction (p.2); results p.14): ATLAS tau+MET(+b) resonant and t-channel U1 search, scanning beta_L^23 and g_U; covers the b-tau-nu / c-nu topology
- arXiv:1812.07831 (Sec. 5.2.1-5.2.3): HL-LHC Yellow Report already contains LQ->tau b at HL-LHC (CMS, single+pair), U1/Z' for B anomalies at HL/HE-LHC, and LQ->t tau / t mu projections
- arXiv:2005.06475 (Sec. on results, Figs. 3-4, Conclusions): Pheno HL-LHC projection for resonant lepton-quark LQ across first/second-generation flavour combinations

**Closest existing results**

| id | collab | covers | region gap |
|---|---|---|---|
| arXiv:2507.03650 | ATLAS | Resonant scalar LQ via lepton PDF: e+light, mu+light, e+b, mu+b; 140/fb 13 TeV + 55/fb 13.6 TeV | no c-tag category; scalar only (no vector interpretation found in model section); no tau |
| arXiv:2608.28377 | CMS | Resonant scalar LQ via muon-quark scattering, mu + u or b jet, 138/fb | muon only; no CMS e-quark result found (UNVERIFIED absence) |
| arXiv:2308.06143 | CMS | LQ via tau-quark scattering, tau + jet + MET, btag/no-btag | scalar only |
| arXiv:2308.07826 | CMS | b-tau LQ single+pair+nonresonant combined; 2.8 sigma local excess | excess benchmark excluded by ATLAS 2503.19836 |
| arXiv:2503.19836 | ATLAS | high-mass tautau vs b-jet multiplicity; U1 (beta_L, beta_R, beta^23_L) and S1 non-resonant constraints | non-resonant only |
| arXiv:2402.16561 / arXiv:2503.20033 | ATLAS / CMS | mono-top (top + MET) searches | no resonant-LQ (b tau -> t nu) interpretation; reinterpretation possible |
| arXiv:2503.20023 | CMS | t-channel scalar and vector LQ in high-mass ee/mumu | not jointly fit with pair/single production |

**HL-LHC projection docs.** arXiv:1812.07831 (HL/HE-LHC YR BSM) Sec. 5.2.1-5.2.4; CMS-PAS-FTR-18-028 (INSPIRE recid 1710497: CMS LQ->tau b prospects; PAS number from memory, UNVERIFIED). Pheno: arXiv:2005.06475 (resonant lepton-quark, 3 ab-1), arXiv:2012.11474 (b+tau, mono-top, mono-jet at 300/fb and 3 ab-1). ATLAS thesis recid 3183811 (resonant LQ + HL muon detectors).

**Showstoppers.** c/s-initiated resonant LQ is PDF-suppressed (2005.06475 Conclusions), and c-tagging at TeV jet pT has limited efficiency (UNVERIFIED numbers). Lepton-PDF signal rates scale as lambda^2 times alpha-suppressed lepton luminosities. (f) is a theory-systematics study, not an experimental analysis. (d) needs a model-specific coherent signal (interference depends on the LQ representation), which suits reinterpretation better than a new HL analysis.

**Queries run**

- `(CMS or ATLAS) and t leptoquark and date > 2023`
- `(CMS or ATLAS) and abstracts lepton-quark / electron-quark / lepton content of the proton / lepton PDF`
- `(CMS or ATLAS) and t leptoquark and charm`
- `(CMS or ATLAS) and (single top / mono-top) and MET/dark matter, date > 2017`
- `(CMS or ATLAS) and abstracts leptoquark and monojet`
- `(CMS or ATLAS) and abstracts leptoquark and single top`
- `cites arxiv:2012.11474 (collaboration papers)`
- `t leptoquark and (HL-LHC or high-luminosity)`
- `(CMS or ATLAS) and t leptoquark and (prospects or projection or HL-LHC)`
- `arxiv_pdf 2503.19836 grep CMS/excess/beta_R`
- `arxiv_pdf 2208.02717 grep beta_R benchmarks`
- `arxiv_pdf 2606.02067 intro`
- `arxiv_pdf 2507.03650 grep vector/charm/HL`
- `arxiv_pdf 2505.08738 grep charm/opportunities`
- `arxiv_pdf 1812.07831 grep leptoquark`
- `arxiv_pdf 2012.11474 conclusions`

**Notes.** Per-part ratings: (a) NARROWED, surviving with c-tag/vector/LFV extensions, moderate promise and incremental. (b) DIES: b+tau is done by CMS 2308.06143 and 2308.07826; mono-top/mono-jet are covered as final states and only lack an LQ reinterpretation; HL pheno exists. (c) DIES: beta_R benchmarks are in CMS 2208.02717 and ATLAS 2503.19836; kappa = 0/1 pair-production benchmarks are standard (not re-verified here). (d) NARROWED to reinterpretation: CMS 2308.07826 already combines single+pair+nonresonant for b-tau. (e) DIES: ATLAS 2503.19836 excludes the CMS excess benchmark. (f) DIES as an experimental idea (theory systematics).

## C069: NARROWED

**Claim.** Bundle: (a) scalar LQ (R2~) -> N j with a Majorana RHN gives same-sign dimuon + multijet LNV signatures that existing searches leave unconstrained; (b) mono-LQ / LQ-mediated DM (lepton + jet + MET) was searched only with partial Run 2 data; (c) LQ + vector-like lepton cascades give multi-tau/b final states that no single search targets.

**Surviving gap.** (a) NARROWED: there is no dedicated LQ->Nj search, but the final state is already probed inclusively by SS-dilepton + jets SUSY searches (ATLAS gluino SS search recast in 2603.01903, Fig. 4; CMS 2001.10086), by CMS Z'->NN (2307.06959: two same-flavour leptons + >=2 jets, boosted-N categories) and by CMS W_R->lN (2112.03949). The HL-LHC pheno projection is the seed paper itself (2603.01903). The residual gap is a dedicated multi-TeV single-production regime (mu N j -> mu+- mu+- + >=4 jets with H_T > 2 TeV), where 2603.01903 Sec. VII says the SUSY-search constraints no longer bite, and a boosted/light-N (m_N ~ 50 GeV) channel with a non-isolated muon inside the N jet. This is model-specific and phenomenology-level. (b) NARROWED to a full-Run-2/HL update of CMS EXO-17-015 (1811.10151, 77.4/fb, mu + jet + MET with an m(mu j) peak); there is no gap evidence, and the topology overlaps LQ-pair l-nu-jj channels. (c) DIES: ATLAS 2503.22581 and CMS 2208.09700 search pair-produced VLL decaying via a U1 vector LQ (4321 model) into multi-tau + b final states, and an HL pheno study of LQ-mediated VL-tau production exists (2508.18047).

**Confidence:** medium

**Kill / narrowing evidence**

- arXiv:2503.22581 (Abstract): ATLAS pair-produced VLL -> third-generation quark + U1 vector LQ (4321), tau + b-jet final states, 140/fb; m_VLL > 910 GeV observed
- arXiv:2208.09700 (Title/abstract): CMS pair-produced VLL in >=3b + N tau final states (third-generation 4321-type VLL)
- arXiv:2508.18047 (Abstract): HL-LHC prospects for VL tau production enhanced by LQ-mediated processes (mono- and di-lepton final states)
- arXiv:2603.01903 (Fig. 4 and caption; Sec. VII Results; Conclusions (final paragraph)): The seed paper is itself the HL-LHC projection. Existing ATLAS direct LQ, ATLAS SS gluino SUSY and CMS t-channel LQ constraints already exclude parts of the (Y12, Z11) plane at m_LQ = 1 TeV. The benchmark is m_N = 50 GeV, so N is highly boosted. The paper admits the SS dimuon + multijet signature 'is not unique' (Z', type-II seesaw).
- arXiv:2307.06959 (Abstract): CMS Z'->NN search, two same-flavour leptons + >=2 jets, m_Z' 0.4-4.6 TeV, 138/fb: the same NN -> l l + jets decay topology
- arXiv:2001.10086 (Abstract): CMS SS-dilepton/3l + jets search with 168 SRs, including RPV interpretations: inclusive coverage of SS + multijet
- arXiv:1811.10151 (Abstract): CMS LQ + DM search (mu + jet + MET, m(mu j) peak), 77.4/fb, already exists; a MadAnalysis5 recast implementation exists (INSPIRE recid 1842797)

**Closest existing results**

| id | collab | covers | region gap |
|---|---|---|---|
| arXiv:2001.10086 | CMS | SS 2l / >=3l + jets inclusive, 137/fb | requires isolated leptons; no LQ->Nj interpretation |
| arXiv:2307.06959 | CMS | Z'->NN->ll+jets (incl. boosted N), 138/fb | s-channel Z' production; LQ pair/single production not interpreted |
| arXiv:2112.03949 | CMS | W_R -> l N -> l l j j | different production; recastable |
| arXiv:1806.10905 | CMS | heavy Majorana N in SS dilepton + jets (mixing-produced) | low jet multiplicity, single N via W |
| arXiv:1811.10151 | CMS | LQ pair, LQ->mu j and LQ->DM + soft SM, 77.4/fb | partial Run 2, muon only; full Run 2 only in thesis recid 2162343 (not published) |
| arXiv:2503.22581 / arXiv:2208.09700 | ATLAS / CMS | VLL -> q + U1 (4321), multi-tau + b | vector LQ only; scalar-LQ + VLL (2206.11718-type g-2 model) not interpreted |

**HL-LHC projection docs.** Pheno only: arXiv:2603.01903 (R2~ + RHN, SS dimuon, HL-LHC 3 ab-1), arXiv:2412.19751 (RHN via first-generation LQ, all scalar/vector LQ), arXiv:2508.18047 (VL tau via LQ, HL). No collaboration HL projection found for LQ->Nj, mono-LQ or LQ+VLL.

**Showstoppers.** (a) With m_N << m_LQ (benchmark 50 GeV), N->mu jj is collimated: the muon is non-isolated, and backgrounds from heavy-flavour non-prompt muons and charge mis-ID dominate. 2603.01903 applies only a pT > 20 GeV muon cut with no specific isolation treatment (Sec. V selection), so the background estimate is likely optimistic (UNVERIFIED quantitatively). For small V_muN, N may also be long-lived (decay via mixing or an off-shell LQ), which pushes the signature to displaced vertices (same authors' earlier study is ref [34]). The model requires an R2~ Yukawa to N of order 1 while respecting 0vbb and low-energy constraints (the paper fixes the flavour structure). (b) The DM-LQ model is non-minimal and no gap evidence is cited. (c) Is already searched.

**Queries run**

- `(CMS or ATLAS) and t leptoquark and (t neutrino or abstracts right-handed/heavy neutrino)`
- `(CMS or ATLAS) and (heavy neutrinos / heavy Majorana neutrino) and (Z' or pair), date > 2017`
- `t leptoquark and (right-handed / sterile / heavy neutrino), date > 2016, mostcited`
- `(CMS or ATLAS) and abstracts same-sign and jets and leptoquark`
- `(CMS or ATLAS) and t Majorana neutrinos and t same-sign`
- `collaboration:CMS and (heavy Majorana neutrinos / heavy neutral leptons / heavy neutrinos), date > 2021`
- `cites arxiv:2412.19751; cites arxiv:2603.01903; cites arxiv:1210.5622`
- `(CMS or ATLAS) and abstracts leptoquark and dark matter`
- `cites arxiv:1811.10151`
- `(CMS or ATLAS) and t vector-like leptons, date > 2019`
- `arxiv_pdf 2603.01903 grep recast/isolation/lifetime and Results/Conclusions`

**Notes.** Per-part ratings: (a) NARROWED, phenomenology-level and model-specific; a realistic HL study would need non-isolated-muon/boosted-N backgrounds and displaced-N handling. (b) NARROWED, low novelty (an update of an existing CMS search). (c) DIES for the 4321 vector-LQ realisation; the scalar-LQ + VLL g-2 model (2206.11718) has no experimental interpretation, but no gap evidence was given and it is a recast-level item. The ATLAS thesis recid 2622762 covers W_R boosted N and single LQ as separate searches, not LQ->N.
