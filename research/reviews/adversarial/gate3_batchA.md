# Gate 3 adversarial review, batch A (C001 C003 C005 C008)
Reviewer: adversarial novelty reviewer A. Independent of triage/gate2 files. Evidence from INSPIRE + arXiv PDFs (cache/pdf) + web search. "Not found" is not proof of absence.

## C001 — verdict: **NARROWED** (confidence medium)
**Claim:** No ATLAS/CMS search targets quirks (pairs bound by a long infracolor string) via non-helical/coplanar tracks, stopped/out-of-time annihilation, or quirkonium resonance + soft-pion (SUEP-like) tracks; HL-LHC could open this.

**Surviving gap:** A dedicated central-detector (ATLAS/CMS) coplanar non-helical-hit search for colour-neutral EW-charged quirks with mQ above the FASER reach (FASER excludes up to ~179 GeV at Lambda=10 keV, 2607.26195 Fig.5) in the mesoscopic regime Lambda ~ 0.1-100 keV, i.e. the gap between reinterpreted HSCP/OoT (low Lambda) and monojet (high Lambda) limits; requires custom (non-helix) Phase-2 tracking/HLT. Secondary: quirkonium dijet/diboson resonance + low-pT track excess (2506.11192) is open but its HL-LHC viability under 200 PU is unproven; Wgamma/WZ resonance + displaced glueball vertex (2504.02940 Sec.4) is open but low-rate.

**Bundle split:**
- Macroscopic strings (Lambda <~ 100 eV): HSCP-like tracks: **DIES (indirectly-covered)** — Recast of CMS/ATLAS HSCP and monojet gives TeV-scale bounds on coloured quirks (1703.00912 Table I, Figs.1-2); FASER Fig.5 shows reinterpreted CMS HSCP region; HL-LHC HSCP searches will cover this automatically.
- Stopped quirks / out-of-time annihilation: **DIES (mostly)** — ATLAS stopped-LLP search 2104.03050 (Sec. signal regions, l.~470 of text) added an inclusive SR explicitly 'to preserve acceptance for ... more forward topologies [41-43]' citing the quirk papers incl. Evans-Luty 1811.08903; CMS OoT recast shown in FASER Fig.5. Residual: no quirk interpretation published.
- Mesoscopic regime, EW quirks, coplanar non-helical hits in ATLAS/CMS tracker: **SURVIVES (proposed-not-searched)** — No ATLAS/CMS/LHCb search found; review 2606.30760 (Sec. on quirks, ~p.39) states 'there are no dedicated LHC searches'; FASER 2607.26195 is the only LHC search and covers only mQ<~180 GeV forward; LHCb VELO proposal 2601.09023 is a competitor.
- Microscopic regime: quirkonium resonance + soft-pion/SUEP tracks: **NARROWED** — Plain resonance part covered by ATLAS/CMS dijet, Wgamma, WZ, gammagamma searches (2504.02940 Sec.3 Figs.4-6; 2506.11192 uses ATLAS dijet). Only the track-anomaly-tagged resonance is uncovered (2506.11192 p.5); authors state study has no pile-up and 'will have to be revisited for the HL-LHC'.
- Natural (folded-SUSY) squirks: diboson resonance + displaced glueball vertex: **SURVIVES (theory-explored-untested)** — 2504.02940 Sec.4 proposes it for HL-LHC; no experimental implementation found; rate suppressed by hard hidden-gluon emission.

**Kill / narrowing evidence:**
- arXiv:1703.00912 (abstract, Figs.1-2, Table I): Reinterprets CMS/ATLAS HSCP and monojet searches for quirks; TeV-range bounds for Lambda ~1-100 eV (abstract; Table I gives mass limits up to ~1.8 TeV for coloured fermion quirks)
- arXiv:2607.26195 (abstract, Fig.5, text near Fig.4): FASER first LHC quirk search: excludes EW quirks for 300 eV<Lambda<100 keV, masses up to 179 GeV at Lambda=10 keV; Fig.5 also shows reinterpreted ATLAS/CMS monojet, CMS HSCP, CMS OoT regions
- arXiv:2104.03050 (Sec. on signal regions (SRIncl)): ATLAS stopped-particle search includes an inclusive SR motivated by quirk topologies (cites 0805.4642, 1708.02243, 1811.08903)
- arXiv:2504.02940 (Sec.3, Figs.4-6 and HL projection text (~p.15)): Microscopic EW quirk bound states already probed by ATLAS/CMS Wgamma/WZ/gammagamma resonance searches; projected to HL-LHC by authors

**Closest existing:**
- arXiv:2607.26195 [FASER]: covers EW quirks, Lambda 0.3-100 keV, forward slow pairs, mQ up to ~179 GeV; gap: central production, mQ > ~180 GeV, coloured quirks
- arXiv:2104.03050 [ATLAS]: covers stopped LLP decays incl. quirk-motivated inclusive SR; gap: no quirk interpretation; mesoscopic tracks not targeted
- arXiv:1703.00912 (recast of CMS HSCP 12.9 fb-1 and monojet) [pheno recast of CMS/ATLAS]: covers Lambda <~100 eV and large-Lambda monojet; gap: intermediate Lambda for which tracks are neither HSCP-like nor invisible

**HL projection docs:** No ATLAS/CMS HL-LHC projection for quirks found. CERN HL/HE-LHC BSM Yellow Report 1812.07831: zero occurrences of 'quirk' in text. LLP white paper 1903.04497 Sec. on quirks: 'No dedicated searches for quirks exist at the LHC' (summary bullet ~l.4069 of text). Pheno HL projections: 2504.02940 (natural quirks, HL-LHC), 1708.02243 (tracking, 50 PU), FASER2/FPF 2203.05090, 2404.13814.

**Showstoppers:** (1) Requires non-standard (non-helical) track finding; Phase-2 L1 track trigger and offline tracking assume helices - needs custom HLT path (1708.02243 itself proposes HLT path). (2) Quirk dynamics (energy loss, glueball de-excitation) non-perturbative: large signal-modelling systematics (2606.30760 quirk section). (3) Soft-track resonance tagging degrades with 140-200 PU; 2506.11192 used no pile-up. (4) EW quirk cross sections small at mQ ~ TeV. (5) Strong competition from FASER/FASER2 and LHCb VELO (2601.09023) for low-pT quirk pairs.

**Notes:** Bundle merged 6 scout seeds. Terminology checked: quirk, quirky, quirkonium, infracolor, non-helical, kinked tracks; ATLAS/CMS HSCP and stopped-particle papers do not carry quirk interpretations but are used in recasts. ATLAS photon+jet (1309.3230, 1112.3580) and CMS fractional-charge (1210.2311) cite Kang-Luty; the photon+jet abstracts interpret only q* and QBH (read); 1210.2311 not read in full. Absence of CMS/ATLAS quirk search corroborated by 2606.30760 but CDS internal notes not checked (UNVERIFIED).

<details><summary>Queries run (19)</summary>

- `INSPIRE: t quirk and (collaboration:ATLAS or collaboration:CMS or collaboration:LHCb)`
- `INSPIRE: abstracts.value:"quirk" and (collaboration:ATLAS or collaboration:CMS)`
- `INSPIRE: abstracts.value:"quirks" and (collaboration:ATLAS or collaboration:CMS)`
- `INSPIRE: t quirks and date > 2018`
- `INSPIRE: t quirk and date > 2018`
- `INSPIRE: t quirky and date > 2008`
- `INSPIRE: t quirkonium`
- `INSPIRE: abstracts.value:"quirk" and abstracts.value:"recast"`
- `INSPIRE: abstracts.value:"quirks" and abstracts.value:"monojet"`
- `INSPIRE: abstracts.value:"quirk" and abstracts.value:"high-luminosity"`
- `INSPIRE: abstracts.value:"infracolor"`
- `INSPIRE: abstracts.value:"non-helical" or abstracts.value:"nonhelical"`
- `INSPIRE: abstracts.value:"kinked tracks" and (collaboration:CMS or collaboration:ATLAS)`
- `INSPIRE: t "underlying event" and t "new physics" and date < 2012`
- `INSPIRE: collaboration:ATLAS and t stopped`
- `INSPIRE citers (CMS/ATLAS/LHCb filter) of 0805.4642, 1106.2569, 1708.02243, 1811.08903`
- `INSPIRE all citers of 2410.00269, 2601.09023, 1911.02223, 2504.02940, 2506.11192, 1703.00912`
- `Full-text grep 'quirk' in 1812.07831 (HL-LHC YR) and 1903.04497 (LLP white paper)`
- `WebSearch: CMS OR ATLAS search quirks non-helical tracks 2025 2026`
</details>

## C003 — verdict: **NARROWED** (confidence medium)
**Claim:** SUEP searches cover only prompt, resonant (ggF/VH-produced scalar) regimes; displaced (long-lived dark meson) SUEP and non-resonant/pair-produced mediator SUEP are unsearched and could be targeted at HL-LHC with L1 tracking/scouting.

**Surviving gap:** Displaced, hadronically-decaying, isotropic (non-jet-like) SUEP with dark-meson c*tau ~ mm-m from ggF/VH-produced mediators, i.e. high-multiplicity soft displaced-track/vertex spray not passing emerging-jet jet requirements and not muon-rich; plus an HL-LHC (Phase-2 L1-track/scouting) projection of the prompt program. Pair-produced/non-resonant SUEP survives only as theory-explored-untested with no worked benchmark.

**Bundle split:**
- Prompt resonant SUEP (ggF, WH/ZH, scouting, muon-rich): **DIES (well-covered)** — CMS 2403.05311 (ggF), 2607.09621 (scouting, 'most stringent limits to date' on ggF heavy scalars), 2604.05996 (W/Z-associated, 'first time'), ATLAS 2605.20015 (muons, mS 125-750 GeV).
- Displaced SUEP, leptonic (dark photon -> mu mu) from Higgs decay: **DIES (indirectly-covered)** — CMS 2511.11888: low-mass HV dark showers with non-prompt muon pairs from Higgs decay (B-parking/non-prompt muon triggers); CMS dark QCD summary 3137923 cites B-parking results.
- Displaced SUEP, hadronic: **NARROWED** — CMS 2403.05311 (l.87-90 of text) explicitly states a displaced decay 'would result in an emerging jet signature' - i.e. collaboration regards it as covered by EJ searches (CMS 2403.01556, ATLAS 2510.12347, 2505.02429); CMS muon-detector-shower searches recast for HV (2505.03058) cover long lifetimes. Residual: isotropic soft displaced spray with low-pT tracks failing jet thresholds; no search found.
- Non-resonant / pair-produced mediators to SUEP: **SURVIVES (proposed-not-searched, weakly motivated)** — Deferred in 1612.00850 (text l.347); CMS 3185627 non-resonant search covers semivisible-jet (small 't Hooft) regime only; no SUEP benchmark for pair production found.
- HL-LHC projection: **SURVIVES (LHC-not-projected-to-HL)** — No CMS/ATLAS SUEP HL-LHC projection found; only pheno trigger studies 2203.07314 (Sec.2.2, track-trigger thresholds) and 2306.13595.

**Kill / narrowing evidence:**
- arXiv:2403.05311 (Sec.1/2 signal model (text l.87-90)): CMS: 'A prompt decay is chosen rather than a displaced decay, which would result in an emerging jet signature' - displaced SUEP mapped to EJ by the collaboration
- arXiv:2511.11888 (abstract): CMS search for low-mass hidden-valley dark showers from Higgs decay with non-prompt muon pairs (41.6 fb-1, 2018 non-prompt muon triggers)
- arXiv:2607.09621 (abstract; Sec.2 (l.100-105: 'fully visible, prompt SUEP')): CMS scouting SUEP, 127 fb-1, lower HT threshold, most stringent ggF limits; prompt dark photons only
- arXiv:2505.03058 (abstract): Pheno recast: CMS muon end-cap shower search is broadly sensitive to hidden-valley parameter variations (long-lived dark hadrons)

**Closest existing:**
- arXiv:2403.05311 [CMS]: covers prompt ggF SUEP, boosted, high-HT triggers; gap: displaced dark mesons, HL-LHC
- arXiv:2604.05996 [CMS]: covers WH/ZH -> SUEP, prompt; gap: displaced
- arXiv:2605.20015 [ATLAS]: covers prompt muon-rich SUEP, mS 125-750 GeV; gap: hadronic/displaced
- arXiv:2510.12347 / arXiv:2403.01556 [ATLAS / CMS]: covers emerging jets (multiple displaced vertices in jets); gap: isotropic, soft (non-jet) displaced spray

**HL projection docs:** None from CMS/ATLAS found (INSPIRE abstracts SUEP+HL-LHC/Phase-2 returned only 2107.12379; WebSearch found none). Pheno: 2203.07314 'Track-Based Triggers for Exotic Signatures' (SUEP benchmark, HL-LHC L1 track trigger thresholds); 2306.13595 (autoencoder real-time SUEP). CMS Phase-2 L1 TDR (INSPIRE 1819968) cites 1612.00850 - content not read (UNVERIFIED).

**Showstoppers:** (1) Pile-up: SUEP signal 'closely resembles pile-up' (1612.00850 abstract); at 140-200 PU soft-track multiplicity discrimination degrades - needs MTD timing/vertex association, unproven. (2) Displaced soft tracks: Phase-2 L1 tracking is prompt-oriented (pT>2-3 GeV, small d0), so L1 acceptance for soft displaced spray is poor (2203.07314 Sec.2.2 notes low-pT threshold is essential for SUEP). (3) Hadronization modelling of SUEP is large uncertainty. (4) Rapidly moving field: three CMS + one ATLAS SUEP results in 2024-26 - risk of being scooped by Run-3 analyses.

**Notes:** All four experimental SUEP results read at abstract level; lifetime assumptions checked in text for CMS ggF, CMS scouting and ATLAS muon SUEP (all prompt). CMS W/Z-associated paper (2604.05996) lifetime not checked (UNVERIFIED, assumed prompt). Thesis INSPIRE 3131301 has no abstract; not read.

<details><summary>Queries run (18)</summary>

- `INSPIRE: t "soft unclustered energy"`
- `INSPIRE: t SUEP or t SUEPs`
- `INSPIRE: abstracts.value:"soft unclustered energy" and (collaboration:CMS or collaboration:ATLAS or collaboration:LHCb)`
- `INSPIRE: abstracts.value:"SUEP" and abstracts.value:"displaced"`
- `INSPIRE: abstracts.value:"SUEP" and (abstracts.value:"HL-LHC" or abstracts.value:"high-luminosity" or abstracts.value:"Phase-2")`
- `INSPIRE: abstracts.value:"soft bombs"`
- `INSPIRE: abstracts.value:"SUEP" and date > 2023`
- `INSPIRE: abstracts.value:"isotropic" and abstracts.value:"dark mesons" and abstracts.value:"long-lived"`
- `INSPIRE: abstracts.value:"spherical" and abstracts.value:"hidden valley" and abstracts.value:"pair"`
- `INSPIRE: collaboration:CMS and abstracts.value:"dark showers" and date > 2022`
- `INSPIRE: collaboration:ATLAS and abstracts.value:"dark showers" and date > 2022`
- `INSPIRE: collaboration:CMS and abstracts.value:"hidden valley" and date > 2023`
- `INSPIRE: collaboration:CMS and t "muon detector" and t long-lived`
- `INSPIRE: abstracts.value:"high-multiplicity" and abstracts.value:"displaced vertices" and abstracts.value:"dark" and date > 2021`
- `INSPIRE citers of 1612.00850 (CMS/ATLAS/LHCb; +displaced; +long-lived)`
- `INSPIRE all citers of 2403.05311`
- `Full-text grep: 2403.05311, 2605.20015, 2607.09621 (lifetime/displaced), 1612.00850 (pile-up, future work), 2203.07314 (SUEP)`
- `WebSearch: soft unclustered energy patterns HL-LHC projection CMS Phase-2 displaced SUEP search`
</details>

## C005 — verdict: **NARROWED** (confidence high)
**Claim:** Dark showers / emerging jets with GeV-scale (above a few GeV) dark pions are largely unconstrained, especially for Higgs-portal production, EW pair-produced dark-quark mediators, gluon-rich long-lived dark mesons, and regions hidden by trigger blind spots - an HL-LHC opportunity.

**Surviving gap:** CMS-side (ATLAS already preparing one) Higgs-portal (ggF/VBF/VH) emerging-jet/dark-shower search with hadronically decaying dark mesons of ~2-20 GeV at short proper decay lengths (~1-100 mm, in the tracker), where CMS muon-detector-shower limits (2402.01898) lose sensitivity and CMS displaced-jet searches (2409.10806) are interpreted only for H->SS (two LLPs), using multi-displaced-vertex counting and Phase-2 displaced L1/HLT tracking. A pheno HL-LHC projection already exists (2512.24814), so the residual novelty is experimental implementation only.

**Bundle split:**
- (a) Dark pion masses above a few GeV largely unconstrained (Snowmass 2203.09503 quote): **DIES (outdated claim)** — Since 2022: CMS 2402.01898 dark-shower interpretation for LLP masses 2-20 GeV, cT 1 mm-10 m, five portals; ATLAS EJ 2505.02429/2510.12347 with dark pion 10-20 GeV, cT 1-1000 mm; CMS EJ 2403.01556; CMS 2511.11888 low-mass muonic.
- (b) EW pair production of heavy dark-quark mediators: **DIES** — Source paper 2110.10691 (Conclusions, text l.2036-2040): Higgsino-search reinterpretation gives M >~ 1.1 TeV and 'The improvement expected in the high-luminosity phase is mild ... direct production of the mediators would need to wait for a future collider'. Related EW dark-meson recasts 2507.13430 (disappearing tracks ~1.2 TeV) and ATLAS dark mesons to tb 2405.20061.
- (c) Emerging jets via Higgs portal: **NARROWED / pre-empted for ATLAS** — ATLAS proceeding INSPIRE 3201494 (Nuovo Cim. C 49 (2026) 131, DOI 10.1393/ncc/i2026-26131-3) 'reports a preliminary estimate of the exclusion reach of a search for Emerging Jets arising from a Higgs portal at the ATLAS experiment' - analysis in preparation. CMS 2402.01898 already sets 'the first LHC limits on models of dark showers produced via Higgs boson decay', B(H->dark quarks) down to 2e-3 (Sec.1, Sec. results p.24, Figs.18-22).
- (d) Trigger blind spots at Run 3 / HL-LHC: **NARROWED (infrastructure, not an analysis)** — CMS Run-3 dedicated displaced-jet triggers implemented in 2022 (2409.10806 Sec.4); CMS HL-LHC displaced-track reconstruction work (INSPIRE 3206256, 2609.26695, title only); pheno trigger studies 2103.08620, 2203.07314, 2211.05720. Trigger R&D is not a standalone physics-analysis gap.
- (e) Gluon-rich ~GeV long-lived dark mesons from Higgs decay; off-shell h*->SS: **NARROWED** — Gluon portal explicitly covered for cT 1 mm-10 m, m 2-20 GeV by CMS 2402.01898 (Fig.19); 2512.24814 already gives HL-LHC tracker+MDS projections for this exact scenario. Off-shell h*->SS not checked in detail (UNVERIFIED).

**Kill / narrowing evidence:**
- arXiv:2402.01898 (abstract; Sec.1 (p.2-3); Sec.2 signal models (p.5); Sec. results p.24, Figs.18-22): CMS muon-detector showers: dark-shower models from H decay, five portals (gluon, photon, vector, Higgs, dark-photon), LLP mass 2-20 GeV, cT 1 mm-10 m; 'first LHC limits on models of dark showers produced via Higgs boson decay', B(H->dark quarks) as low as 2e-3
- INSPIRE:3201494 (DOI 10.1393/ncc/i2026-26131-3) (abstract): ATLAS proceeding: preliminary exclusion reach of an emerging-jet search from a Higgs portal - ATLAS analysis in preparation
- arXiv:2110.10691 (Conclusions (text l.2036-2040)): EW mediators already >~1.1 TeV from Higgsino recast; HL-LHC improvement 'mild'
- arXiv:2512.24814 (abstract; Sec.III-IV (text l.453-470, 655-870)): Pheno HL-LHC (14 TeV) projection for gluon-enriched dark jets from Higgs decays in tracker (EJ) and CMS muon system, with recast of CMS EJ and MDS
- arXiv:2505.02429 (abstract): ATLAS 13.6 TeV EJ: s-channel Z' and t-channel Phi, dark pion cT 5-50 mm (abstract); Z' up to 2.5 TeV excluded

**Closest existing:**
- arXiv:2402.01898 [CMS]: covers Higgs-portal dark showers, long-lived mesons in muon system, 2-20 GeV; gap: short cT (mm-cm) inside tracker
- arXiv:2409.10806 [CMS]: covers Run-3 displaced jets, H->SS, m<60 GeV, cT<1 m, new triggers; gap: not interpreted for multi-LLP dark showers (recastable)
- arXiv:2403.01556 / arXiv:2510.12347 / arXiv:2505.02429 [CMS / ATLAS / ATLAS]: covers emerging jets, QCD-pair-produced t-channel mediators and Z'; gap: Higgs-portal production (being pursued by ATLAS, INSPIRE 3201494)
- arXiv:2511.11888 [CMS]: covers Higgs-portal dark showers with displaced dimuons (low mass); gap: hadronic decays

**HL projection docs:** Pheno: 2512.24814 (HL-LHC gluon-rich dark jets from H decay, tracker + CMS MDS); 2307.04847 (EJ probes, HL-oriented); 2110.10691 (Run3 / HL statements). No CMS/ATLAS HL-LHC projection for dark showers found (not exhaustive; CMS/ATLAS FTR/PUB notes not searched on CDS - UNVERIFIED).

**Showstoppers:** (1) Pre-emption: ATLAS Higgs-portal EJ analysis already in preparation (3201494); CMS MDS limits already reach B(H->dark quarks) ~2e-3. (2) Higgs-portal events are soft (m_H=125 GeV split into many mesons): L1 HT/jet thresholds at 200 PU are the bottleneck; needs VBF/VH tags or L1 displaced tracking. (3) Hadronization modelling uncertainty for dark showers is large (2505.03058 abstract urges caution). (4) Multi-DV fake background from material/merged vertices grows with pile-up.

**Notes:** Bundle of 7 seeds split into 5 parts. The strongest kill is the CMS MDS dark-shower interpretation (2402.01898), which the scouts did not list. Semi-visible jet variants are reviewed under C008.

<details><summary>Queries run (16)</summary>

- `INSPIRE: t "emerging jets" and (collaboration:CMS or collaboration:ATLAS or collaboration:LHCb)`
- `INSPIRE: t "dark jets" and (collaboration:CMS or collaboration:ATLAS)`
- `INSPIRE: t "dark shower" or t "dark showers"`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and abstracts.value:"dark quantum chromodynamics"`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and abstracts.value:"Higgs boson" and abstracts.value:"dark quarks"`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and abstracts.value:"hidden sector" and abstracts.value:"Higgs" and abstracts.value:"displaced jets" and date > 2020`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and abstracts.value:"dark mesons"`
- `INSPIRE: collaboration:CMS and t "displaced jets" and date > 2019`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and abstracts.value:"emerging jets" and abstracts.value:"Higgs"`
- `INSPIRE: abstracts.value:"emerging jets" and abstracts.value:"electroweak"`
- `INSPIRE citers of 2103.01238 (CMS/ATLAS)`
- `INSPIRE all citers of 2110.10691`
- `WebSearch: ATLAS "dark jets" Higgs portal search 2026 emerging jets Higgs boson decay dark quarks`
- `WebFetch: arXiv 2601.13033 (ATLAS dark-sector proceedings)`
- `WebFetch: INSPIRE record 3201494`
- `Full text: 2402.01898 (dark shower models), 2409.10806, 2512.24814, 2110.10691`
</details>

## C008 — verdict: **NARROWED** (confidence medium)
**Claim:** Semi-visible jets enriched in leptons, taus or photons, or produced with ISR (jet/photon) as recoil handle, are unsearched or under-searched at CMS/ATLAS and would gain at HL-LHC.

**Surviving gap:** (i) Photon-enriched SVJs (prompt non-isolated photons inside SVJs, high neutral-EM-fraction jets that fail standard jet ID) from s-channel Z' - proposed-not-searched (pheno only, 2407.08276); (ii) photon-ISR-tagged low-mass (~200-700 GeV) Z' -> SVJ SVJ - proposed-not-searched (2409.04741). Jet-ISR boosted SVJ appears to be in preparation at CMS (thesis INSPIRE 2751239), so only the photon-ISR variant is clean. Lepton- and tau-enriched SVJ are taken.

**Bundle split:**
- Lepton-enriched SVJ (s-channel): **DIES** — CMS 2608.05323 (EXO-24-029): resonant lepton-enriched SVJ, both SVJl (all flavours) and SVJtau, 138 fb-1, GNN tagger (abstract); earlier PAS INSPIRE 2963506.
- Tau-enriched SVJ: **DIES** — CMS 2608.05323 SVJtau scenario; CMS-PAS-EXO-26-005 (INSPIRE 3136606) dedicated tau-enriched s-channel search.
- Non-resonant / t-channel hadronic SVJ: **DIES (well-covered)** — ATLAS 2305.18037 (t-channel, mediator to 2.7 TeV at unit coupling), CMS INSPIRE 3185627 (non-resonant, GNN + autoencoder), ATLAS 2505.01634 (resonant + anomaly).
- Jet-ISR boosted SVJ (low-mass Z'): **NARROWED / likely pre-empted** — CMS dissertation INSPIRE 2751239 develops a boosted SVJ search recoiling against an ISR jet for mZ' <= 550 GeV in preparation for Run-2 data; no public CMS result found (status UNVERIFIED).
- Photon-ISR SVJ: **SURVIVES (proposed-not-searched)** — Only pheno 2409.04741 (Sec.1: 'The ISR production channel has not yet been explored in the context of dark QCD searches') and 2604.20456 (r_inv regression in photon+SVJ). No CMS/ATLAS result found.
- Photon-enriched SVJ: **SURVIVES (proposed-not-searched)** — Only pheno 2407.08276; same authors' lepton/tau proposals (2206.03909, 2212.11523) were turned into CMS searches, so pre-emption by CMS is plausible (speculative).

**Kill / narrowing evidence:**
- arXiv:2608.05323 (abstract): CMS resonant lepton-enriched SVJ search incl. tau-enriched scenario, 138 fb-1
- INSPIRE:3136606 (CMS-PAS-EXO-26-005) (abstract): CMS s-channel tau-enriched SVJ search, 138 fb-1
- INSPIRE:2751239 (abstract): CMS thesis: boosted SVJ recoiling against ISR jet, mZ' <= 550 GeV, developed for Run-2 CMS data
- arXiv:2305.18037 / INSPIRE:3185627 (abstracts): ATLAS and CMS non-resonant (t-channel) SVJ searches

**Closest existing:**
- arXiv:2608.05323 [CMS]: covers Z' -> lepton/tau-enriched SVJs, MET aligned with jets containing non-isolated leptons; gap: photons-enriched; low-mass via ISR
- arXiv:2112.11125 [CMS]: covers resonant hadronic SVJ (high-mass Z', dijet+MET triggers); gap: mZ' below trigger thresholds (needs ISR)
- arXiv:2505.01634 [ATLAS]: covers resonant SVJ + anomalous signatures; leptons vetoed (text l.603); gap: photon-rich, ISR-tagged

**HL projection docs:** No CMS/ATLAS HL-LHC SVJ projection found (INSPIRE abstracts semivisible + HL-LHC/high-luminosity/3000 returned none relevant). CONTUR study 2502.11237 constrains SVJ with existing measurements (does not treat photon variant as covered; only cites it).

**Showstoppers:** (1) Photon-enriched SVJs have high neutral-EM fraction and fail standard jet ID / photon isolation (2407.08276 abstract) - requires dedicated jet ID and trigger studies; at HL-LHC with 200 PU, non-isolated photon/jet-ID and MET-alignment variables degrade. (2) Signal efficiency in the proposed photon-SVJ selection is ~0.4-0.6% (2407.08276 cut-flow table, last rows) - small. (3) Photon-ISR channel pays alpha_em suppression and single-photon trigger thresholds (~140 GeV in Run 2 per 2409.04741 l.829; Phase-2 thresholds UNVERIFIED). (4) Model dependence: photon enrichment needs an extra light pseudoscalar (ALP) portal - ad-hoc benchmark. (5) Pre-emption: CMS group that proposed lepton/tau variants executed them; ISR-jet variant in CMS thesis.

**Notes:** WebFetch of CMS EXO pages is lossy (did not list 2112.11125), so absence of a CMS boosted/ISR SVJ PAS is UNVERIFIED. Photon-ISR + SVJ overlaps in phase space with photon+MET (monophoton) at r_inv->1 and with ISR-photon low-mass dijet resonance searches at r_inv->0; the residual gap is intermediate r_inv only.

<details><summary>Queries run (11)</summary>

- `INSPIRE: t "semivisible" or t "semi-visible"`
- `INSPIRE: (collaboration:CMS or collaboration:ATLAS) and (abstracts.value:"semivisible" or abstracts.value:"semi-visible")`
- `INSPIRE: collaboration:CMS and abstracts.value:"semivisible" and abstracts.value:"boosted"`
- `INSPIRE: abstracts.value:"semivisible" and abstracts.value:"photon" and (collaboration:CMS or collaboration:ATLAS)`
- `INSPIRE: (abstracts.value:"semi-visible" or abstracts.value:"semivisible") and (abstracts.value:"HL-LHC" or abstracts.value:"high-luminosity" or abstracts.value:"3000")`
- `INSPIRE: abstracts.value:"dark" and abstracts.value:"jets" and abstracts.value:"non-isolated photons"`
- `INSPIRE all citers of 2409.04741 and 2407.08276`
- `WebSearch: CMS search boosted semivisible jets initial state radiation low mass Z' EXO 2025 2026`
- `WebSearch: "semivisible jets" CMS "initial-state radiation" boosted search leptophobic Z' below 550 GeV`
- `WebFetch: CMS EXO public results twiki; CMS EXO publications page`
- `Full text: 2505.01634, 2409.04741, 2407.08276, 2502.11237, 2512.16343 (CMS dark-sector proceedings)`
</details>
