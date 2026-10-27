# Gate 3 adversarial novelty review - batch D (C029, C031, C040, C044)

Reviewer: adversarial agent D. Sources: INSPIRE via tools/inspire.py, PDFs via tools/arxiv_pdf.py. "Not found" is not proof of absence.

## C029 - NARROWED (part b DIES; part a narrowed to a low-priority correlated-topology/reinterpretation niche)

**Claim:** Bundle: (a) a nested disappearing-track -> displaced-dilepton-vertex cascade (compressed scotogenic, eta+- DT then long-lived N2 -> DV, optionally MTD-timed) is not targeted by any search; (b) pure-higgsino (loop-split ~0.3 GeV) disappearing tracks lack an HL-LHC/Phase-2 projection.

**Surviving gap:** Only (a) survives, narrowly: an event-level DT + collinear downstream dilepton DV (+MTD delay) selection for a charged parent with ~0.2 GeV splitting to a long-lived neutral; each leg individually is searched (DT incl. charged-scalar/stau interpretation; displaced opposite-sign dilepton DVs), so the gap is a combined-selection/acceptance study, best done first as a recast of ATLAS 2603.08315 + ATLAS 2601.05664, not as a stand-alone HL-LHC analysis. Part (b) residual is at most an UPDATED ITk/Phase-2 projection using 3-layer tracklets + soft-pion tagging (methods of 2603.08315), a projection refresh rather than a new analysis.

**Kill / narrowing evidence:**
- `ATL-PHYS-PUB-2018-031 (INSPIRE recid 1795267)` (abstract): ATLAS HL-LHC (3 ab-1, 14 TeV) disappearing-track prospects for winos AND higgsinos with highly compressed spectra - directly contradicts 'HL projection not located' for part (b)
- `arXiv:1812.07831` (Sec. 4.1.1 (Figs. 4.1.2, 4.1.3), Sec. 4.1.3 (Fig. 4.1.5, Table 4.1.2)): HL/HE-LHC Yellow Report WG3: Sec. 4.1.1 ATLAS DT projection with pure-higgsino cross sections (Fig. 4.1.2 right), Fig. 4.1.3 exclusion in (m, Delta m) plane reaching Delta m ~0.2-0.4 GeV; Sec. 4.1.3 (Han, Mukhopadhyay, Wang) higgsino-like DT reach at HL-LHC; text also lists ITk improvements (3-4 hit tracklets) as expected enhancements
- `arXiv:2603.08315` (abstract; Sec. 1 (lines on 3-hit tracklets and 250-350 MeV pions)): ATLAS Run-2 DT search with 3-pixel-hit tracklets plus ML soft-pion reconstruction, explicitly targeting pure-higgsino charginos with loop-induced splitting (lifetimes < 0.03 ns) and also tau-slepton (charged scalar) DTs - the exact 'pure-higgsino short track' regime
- `arXiv:2401.14046 / arXiv:2511.20042` (titles/abstracts (INSPIRE 2751400, 3086532)): ATLAS searches for nearly mass-degenerate higgsinos using low-momentum mildly displaced tracks - covers the Delta m region between DT and soft leptons, overlapping the 'ultra-compressed' soft-displaced sub-idea

**Closest existing results:**
- `arXiv:2603.08315` [ATLAS]: covers DT (3/4 pixel layers) + jet + MET, wino/higgsino/stau interpretations, 0.01-10 ns. Region gap: No requirement/use of a downstream DV; acceptance for events where the invisible daughter later decays to leptons inside tracker not evaluated (possible loss via lepton veto/isolation)
- `arXiv:2601.05664` [ATLAS]: covers Displaced vertices of oppositely charged leptons (140 fb-1). Region gap: No DT association; lepton pT thresholds may be high for compressed N2->N1 ll
- `arXiv:2309.16823` [CMS]: covers Disappearing tracks full Run 2, wino/higgsino. Region gap: Same as ATLAS: single-leg
- `ATL-PHYS-PUB-2018-031 / arXiv:1812.07831 Sec 4.1` [ATLAS]: covers HL-LHC DT projection for wino and higgsino. Region gap: Pre-dates 3-hit tracklet + soft-pion methods; no nested-LLP model

**HL-LHC projection docs:** ATL-PHYS-PUB-2018-031 (recid 1795267); arXiv:1812.07831 Sec 4.1.1-4.1.3; CMS Phase-2 higgsino note recid 1704585 is a soft-dilepton (not DT) projection; CMS MTD TDR (recid 1819664) for LLP timing physics case. No collaboration projection for the nested DT->DV topology found.

**Showstoppers:** (a) Model relies on two hierarchically small Yukawa entries (~1e-3 and ~1e-6) and Delta M ~200 MeV; with such splitting eta+- -> N2 + e (muon barely open), and any eta0/eta+- splitting must be arranged so eta+- -> eta0 pi is closed - fine-tuned benchmark. N2 is nearly collinear with the DT, so the DV sits near the DT extrapolation where the DT search's isolation/calorimeter veto may already be affected - a modest acceptance effect, not a new discovery handle. Yields: inert-doublet EW pair production is small (scalar, ~1/4-1/10 of fermion rates; UNVERIFIED numerically). Trigger is MET+ISR as in DT searches - OK. Single-author 0-1 citation preprints (2609.28334, 2608.29275, INSPIRE 3188833) without detector-level simulation.

**Confidence:** high for (b) DIES; medium for (a) NARROWED

**Notes:** Scout's pure-higgsino seed cited 1703.09675 and 2311.17149 but missed ATL-PHYS-PUB-2018-031 and YR 1812.07831 Sec 4.1. The stau-DT interpretation in 2603.08315 (charged scalar -> soft charged particle + invisible) is the closest experimental analogue of the eta+- DT leg. 2608.29275's 'ultra-compressed Delta M~2 GeV soft displaced' overlaps with ATLAS low-momentum displaced-track higgsino searches (2401.14046, 2511.20042) and the INSPIRE 3189809 soft-displaced-lepton pheno study.

<details><summary>Queries run (16)</summary>

- `t disappearing and (collaboration:CMS or collaboration:ATLAS)`
- `t disappearing and (t HL-LHC or t "high-luminosity" or t phase-2)`
- `abstracts.value:"disappearing track" and abstracts.value:higgsino and date > 2021`
- `t "highly compressed" and collaboration:ATLAS`
- `t higgsino and (t HL-LHC or t "high luminosity") and date > 2017`
- `refersto:recid:1704585`
- `abstracts.value:"disappearing track" and abstracts.value:"displaced vertex"`
- `abstracts.value:"kinked track"`
- `abstracts.value:"disappearing track" and abstracts.value:"displaced" and (collaboration:CMS or collaboration:ATLAS)`
- `abstracts.value:"long-lived" and abstracts.value:"inert doublet" and date > 2018`
- `cites 1911.09037; cites 2609.28334; cites 2007.03708`
- `collaboration:ATLAS and t "displaced tracks"`
- `collaboration:CMS and abstracts.value:timing and abstracts.value:"long-lived" and date > 2021`
- `abstracts.value:"MIP timing detector" and abstracts.value:"long-lived"`
- `(collaboration:CMS or collaboration:ATLAS) and t displaced and (t dilepton or t "lepton pairs" or t leptons) and date > 2019`
- `grep 'disappearing' in arXiv:1812.07831 full text; grep higgsino/stau/pion in arXiv:2603.08315 full text`

</details>

## C031 - NARROWED (both parts reduce to post-discovery characterization; (b) largely DIES as an HL-LHC projection already exists)

**Claim:** Bundle: (a) sequential displaced vertices in one decay chain ('tumblers', LLP -> LLP' -> SM) with vertex-to-vertex pointing and event-by-event mass reconstruction are not targeted by CMS/ATLAS multi-DV searches; (b) LLP mass/lifetime (beta-gamma) determination with HL-LHC timing is not done experimentally (only (m, c tau) limits).

**Surviving gap:** A tumbler-vs-independent-DV discriminant (DV2 lying on the DV1->DV2 flight line, consistent PV-DV1-DV2 timing with MTD/ETL, 3-step mass reconstruction) layered on top of inclusive multi-DV displaced-jet selections - i.e. a characterization/model-discrimination study for a post-discovery scenario or an add-on signal region, not a discovery-reach gap. For (b), only an extension of the existing CMS MTD LLP mass-reconstruction study to lifetime extraction / hadronic DVs and to ATLAS HGTD acceptance survives.

**Kill / narrowing evidence:**
- `arXiv:2108.02204` (Sec. V end / Sec. VI intro (text around 'a significant excess of DV-class events would be observed at the HL-LHC for all of our benchmarks')): The tumbler paper itself states the benchmarks would first appear as an excess in existing displaced-jet/multi-DV searches (background 0.1-0.7 events at 137 fb-1, scaled to HL-LHC) and that the tumbler-specific mass reconstruction is needed to distinguish tumblers from non-tumbler multi-DV events after an excess - i.e. discovery is indirectly covered by inclusive DV searches
- `arXiv:1903.04497` (Sec. 5.1.3.7, Fig. 5.25): LHC LLP community white paper, Sec. 5.1.3.7 'LLP Searches with Precision Timing at CMS': CMS (Preliminary, MTD) study of full kinematic LLP mass reconstruction from PV-SV space-time displacement (beta measurement), GMSB chi0 -> Z G~ benchmark and a higgsino scenario, mass resolution vs MTD resolution (Fig. 5.25)
- `CMS MTD TDR, CERN-LHCC-2019-003 (INSPIRE recid 1819664)` (physics-case chapter (UNVERIFIED exact section; not on arXiv, read via white-paper quote only)): Source of the CMS MTD LLP physics case (LLP velocity/mass reconstruction with timing) quoted in 1903.04497

**Closest existing results:**
- `arXiv:2104.13474` [CMS]: covers Pair-produced LLPs decaying to jets with displaced vertices (multi-DV selections in tracker). Region gap: Treats DVs as independent; no requirement that DV2 lies on the DV1 flight direction; chained LLP signal not interpreted
- `arXiv:1808.03078` [CMS]: covers Two displaced vertices in multijet events. Region gap: Same; independent vertices
- `arXiv:2203.00587` [ATLAS]: covers Pair of displaced vertices in the muon spectrometer. Region gap: Large-radius only; independent DVs
- `arXiv:2301.13866` [ATLAS]: covers DV + multiple jets (inclusive >=1 DV). Region gap: Inclusive; would capture tumbler events but not identify the chain

**HL-LHC projection docs:** arXiv:1903.04497 Sec 5.1.3.7 (CMS MTD LLP mass reconstruction); CMS MTD TDR recid 1819664; ATLAS/CMS HL-LHC BSM YR arXiv:1812.07831 (LLP chapter, not specifically for tumblers); CMS Phase-2 L1 displaced-vertex track trigger proceedings (recid 2908980). No collaboration projection for sequential DV chains found.

**Showstoppers:** Tumblers need two macroscopic lifetimes (both DVs inside the tracker volume and resolvable) - a doubly tuned spectrum; the paper's benchmarks give a much larger population of non-tumbler multi-DV events, so the generic multi-DV searches reach discovery first. Event-by-event mass reconstruction requires good DV position + timing for displaced hadronic vertices; MTD/ETL timing applies to charged tracks reaching the timing layer, displaced-track timing association is UNVERIFIED in performance terms. Lifetime/mass measurement (b) is conditional on an observed signal - not a stand-alone search proposal.

**Confidence:** medium

**Notes:** No CMS/ATLAS paper interpreting a chained LLP->LLP topology was found, but 'not found' is not proof of absence. The surviving piece is phenomenology/characterization (novelty_kind: phenomenology), weak as a new HL-LHC analysis. The 2608.27868 VBF timing-reference preprint (0 cites) is not experimental.

<details><summary>Queries run (12)</summary>

- `cites 2108.02204 (all 16 citing papers; none experimental)`
- `cites 1912.06669 (none experimental)`
- `cites 1903.05825 (none experimental)`
- `t "Searching for long-lived particles beyond the Standard Model at the Large Hadron Collider"`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"two displaced vertices"`
- `abstracts.value:"long-lived" and (abstracts.value:"mass reconstruction" or abstracts.value:"mass measurement") and (abstracts.value:timing or abstracts.value:"time of flight") and date > 2016`
- `abstracts.value:"sequential" and abstracts.value:"displaced vertices"`
- `abstracts.value:"long-lived" and abstracts.value:"decay chain" and abstracts.value:"displaced" and date > 2018`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"long-lived" and (abstracts.value:"HL-LHC" or abstracts.value:"Phase-2") and date > 2017`
- `abstracts.value:"long-lived" and abstracts.value:lifetime and abstracts.value:determin and abstracts.value:LHC and date > 2018`
- `abstracts.value:"MIP timing detector" and abstracts.value:"long-lived"`
- `full-text grep of arXiv:2108.02204 (CMS/ATLAS/existing searches) and arXiv:1903.04497 (characterization/timing)`

</details>

## C040 - NARROWED (a survives narrowly as an HL-projection/Phase-2 analysis gap; b, c, d DIE as distinct proposals)

**Claim:** Bundle of four: (a) direct stau pair production in the coannihilation corridor m_tau < Delta m(stau, LSP) < ~60 GeV lacks LHC/HL-LHC sensitivity; (b) light right staus in natural SUSY are not in HL projections; (c) g-2-motivated light sleptons/EWkinos lack HL coverage; (d) Z'(B-L) -> slepton/sneutrino pairs are unsearched.

**Surviving gap:** (a) only: a collaboration-level HL-LHC/Phase-2 projection (and eventual Phase-2 analysis) for DIRECT stau pair production with Delta m(stau, chi0_1) ~ 5-60 GeV using ISR/VBF recoil + soft tau_h (Phase-2 tau trigger/ID, e.g. low-pT tau_h at L1). Run-2/3 searches exist but are weak there: ATLAS 2609.37215 (ISR channel excludes only up to m(stau)=115 GeV at Delta m=30 GeV; combined: no exclusion); CMS 1910.01185 (77 fb-1, interpreted for chargino/neutralino with intermediate stau). The HL-LHC YR stau projections are sensitive only for Delta m > 100 GeV. Status: searched-limited-regime + LHC-not-projected-to-HL. Phenomenology projections for this corridor already exist (e.g. 1704.04669, 2308.05723, 2403.18991), so novelty is experimental-analysis/projection only.

**Kill / narrowing evidence:**
- `arXiv:2609.37215` (abstract; Sec. 6 (direct stau ML analysis)): ATLAS Run 2+3 (140+53 fb-1) search explicitly targeting compressed direct stau (and EWkino->stau) production with ISR, 1 tau_h + lepton and >=2 tau_h; excludes direct stau only up to 115 GeV at Delta m=30 GeV in ISR channel; no exclusion when combined (2.1-2.4 sigma local deviations) - region is actively searched, not unsearched
- `arXiv:1910.01185` (abstract): CMS soft tau_h + ISR jet + MET search motivated by stau-neutralino coannihilation
- `arXiv:2601.17576 / arXiv:2603.08315` (abstracts): Delta m < m_tau limit (long-lived stau) covered by CMS displaced-tau GNN search and ATLAS DT search with tau-slepton interpretation
- `arXiv:1812.07831` (Sec. 2.3.3 (text), Sec. 3.3.4): YR WG3: Sec. 2.3.1-2.3.3 ATLAS/CMS HL stau projections (sensitive for Delta m > 100 GeV) - shows projection exists for non-compressed only; Sec. 3.3.4 HL projection for singlet DM with slepton-like coannihilation partners notes the low-Delta gap could be closed with ISR
- `arXiv:2505.21476` (Introduction (line ~226 of text) and Conclusions): Muon g-2 Theory Initiative WP25: 'no tension between the SM prediction and the experimental world average' - removes the (c) motivation
- `arXiv:2402.01888 / arXiv:2508.13900` (abstracts; 2508.13900 Sec. on signal models (slepton pair with Delta m < 10 GeV)): CMS combined EW (winos/binos/higgsinos/sleptons) and CMS general compressed-spectra search (ISR recoil, selectron/smuon and EWkino-via-slepton interpretations) cover (c)
- `arXiv:2603.11035` (abstract; Sec. 1): CMS search for Z' -> chargino pairs in 2 OS leptons + MET (U(1)' extended MSSM) - same final state and resonant-SUSY topology as (d); Z'->slepton pairs is a reinterpretation of this 2l+MET resonance-shaped search
- `arXiv:2608.18321` (Sec. 2, Eqs. (2.13)-(2.14)): Seed paper of (d) itself admits benchmark viability needs a suppressed effective leptonic coupling (g ~0.1) for M_Z'=3 TeV to evade dilepton resonance bounds - fragile model-dependent corner

**Closest existing results:**
- `arXiv:2609.37215` [ATLAS]: covers Compressed direct stau and EWkino->stau with ISR, 1-2 tau_h, Run 2+3. Region gap: Weak/no exclusion for direct stau at Delta m ~ 10-60 GeV; no HL projection
- `arXiv:1910.01185` [CMS]: covers Soft tau_h + ISR jet + MET, 77 fb-1. Region gap: Partial Run-2 dataset; interpreted for EWkino with intermediate stau, not pure direct stau
- `arXiv:2207.02254` [CMS]: covers Direct stau pairs, 2 tau_h + MET, 138 fb-1. Region gap: Large Delta m
- `CMS-PAS-FTR-18-010 (INSPIRE 1704284)` [CMS]: covers HL-LHC direct stau projection (tau_h tau_h, tau_l tau_h), mass-degenerate L/R. Region gap: Non-compressed only

**HL-LHC projection docs:** CMS Phase-2 stau projection INSPIRE 1704284; arXiv:1812.07831 Sec. 2.3 (ATLAS+CMS stau HL/HE), Sec. 3.3.4 (slepton-like coannihilation partners); pheno HL studies 2403.18991, 1704.04669, 2308.05723, 2411.13837 (VBF compressed EWkinos), 2102.10194 (VBF higgsino compressed).

**Showstoppers:** (a) Direct stau cross sections are small (YR: <1 fb above 400 GeV at 14 TeV), soft tau_h ID efficiency/fake rates at pT ~ 10-20 GeV and HL pileup 140-200 are the dominant obstacles; trigger must rely on ISR-MET; ATLAS Run 2+3 already gets no combined exclusion, so HL reach may be limited to m(stau) ~ 100-200 GeV (UNVERIFIED estimate). (c) Motivation removed by WP25 g-2 consensus. (d) Requires suppressed Z' leptonic coupling to survive dilepton bounds; Z'->slepton BR small.

**Confidence:** medium-high

**Notes:** ATLAS 2609.37215 appeared 29 Sep 2026 and is the decisive closest result; scout flagged it as unread. Its observed 2.1-2.4 sigma local deviations make an HL follow-up arguably MORE interesting, but it also shows the collaboration is already on this target (ATLAS likely to extend with Run 3 full data). CMS 2508.13900 general compressed search does not include direct staus (grep found no stau signal model), so a CMS compressed-direct-stau Run-3/Phase-2 analysis is the concrete residual. For (b), natural-SUSY light right staus give the same tau-tau+MET final state as direct-stau simplified models -> reinterpretation, not new analysis.

<details><summary>Queries run (13)</summary>

- `(collaboration:CMS or collaboration:ATLAS) and (t stau or t "tau slepton" ...) and date > 2018`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"tau slepton" and abstracts.value:compressed`
- `(collaboration:CMS or collaboration:ATLAS) and (abstracts.value:"tau slepton" or stau or staus) and date > 2020`
- `collaboration:CMS and t tau and t supersymmetry and date > 2020`
- `abstracts.value:stau and abstracts.value:coannihilation and (HL-LHC or high-luminosity or 3000) and date > 2014`
- `collaboration:CMS and (abstracts.value:"soft tau" ...) and date > 2019`
- `collaboration:CMS and abstracts.value:"vector boson fusion" and abstracts.value:compressed and date > 2018`
- `cites 1910.01185`
- `t "anomalous magnetic moment of the muon in the Standard Model" and date > 2024`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"Z prime" and abstracts.value:slepton`
- `(collaboration:CMS or collaboration:ATLAS) and Z' and (sleptons or supersymmetric or dark matter) and missing transverse and date > 2015`
- `(collaboration:ATLAS or collaboration:CMS) and abstracts.value:slepton and (HL-LHC or 3000)`
- `full-text grep: 2609.37215 abstract/Sec.6; 2508.13900 (stau/slepton coverage); 1812.07831 (stau, slepton, coannihilation); 2603.11035; 2608.18321; 2505.21476`

</details>

## C044 - NARROWED (several sub-claims die; residual channel-specific gaps remain: X5/3 -> t phi+(W+ gamma) SSL+gamma; TT -> 6t; T -> t S(gg/WW) and B -> b Phi with m_Phi != 125 GeV)

**Claim:** Bundle of four: (a) charge-5/3 top partners with exotic decays (X5/3 -> t phi+ -> t W+ gamma; multi-top) are not searched, needing SSL + hard photon / multi-top searches; (b) VLQ -> t/b + S with S -> gg/WW/ZZ/tautau/long-lived remains open beyond S -> bb and gamma gamma; (c) fully hadronic B -> b Phi (Phi -> gg/bb) 2b4j/6b pair topology is unsearched; (d) recasts show exotic VLQ channels (notably TT -> tS0 tS0 -> 6t) only indirectly bounded and deserve a dedicated search.

**Surviving gap:** (1) Dedicated pair-production search for T T -> (t S0)(t S0) -> 6 top (or tS0 + tZ/th mixed), which the 2026 recasting atlas states has no direct search yet and recasts already to ~1.65 TeV at BR=100% - a high-ST multi-lepton/multi-b search; HL-LHC suitable. (2) X5/3 -> t phi+ -> t W+ gamma (SSL + hard photon): not targeted; the CMS X5/3 single-lepton search (CMS-PAS-B2G-24-005) covers only X5/3 -> t H+(-> tb). (3) T -> t S with S -> gg/WW (no S->gamma gamma/bb) and B -> b Phi(gg/bb) with Phi mass away from 125 GeV: no VLQ interpretation found, but final states are partially covered by stealth/RPV multijet searches (tt + many light jets; pair-produced trijet resonances) and by B -> bH fully hadronic - a reinterpretation-first gap. Status overall: searched-limited-regime / indirectly-covered.

**Kill / narrowing evidence:**
- `INSPIRE 3157006 (CMS-PAS-B2G-24-005)` (abstract): CMS Run-2 X5/3 pair search in single-lepton final state with BSM decay X5/3 -> t H+ (H+ -> tb) in addition to tW: exotic X5/3 decays are already searched by a collaboration (contradicts the scout note 'X5/3 decays to ALP not seen')
- `arXiv:1907.05894` (abstract): Seed paper itself: 'We use existing same-sign lepton searches to show that the new final states are constrained at the same level as the standard one' - exotic X5/3 channels are indirectly covered; only SSL+photon and top-rich channels are offered as improvements. Also clarifies the decay is X5/3 -> t phi+ (charged scalar), not X5/3 -> t a as the seed text implies (charge conservation)
- `arXiv:2607.28381` (abstract): ATLAS pair T -> tS, S -> gamma gamma, model-independent fiducial limits, explicitly 'targets cascade decays into final states with electroweak bosons or ttbar' - covers S->gamma gamma and partially WW/ZZ/tt cascades with one S->gamma gamma
- `arXiv:2610.03489` (abstract): CMS pair T -> t phi with phi -> gamma gamma, boosted all-hadronic tops (138 fb-1); 2.7 sigma local excess
- `arXiv:2510.25874 / arXiv:2604.10729` (abstracts): CMS single T -> t phi(bb) lepton+jets and heavy resonance -> t phi(bb) fully hadronic boosted - covers S->bb
- `arXiv:2402.13808` (abstract): CMS B-pair fully hadronic and dileptonic (B -> bH/bZ/tW): 6-jet/6b-like fully hadronic topology at m_Phi = m_H is searched
- `arXiv:2506.08825 / arXiv:2102.06976` (abstracts): CMS stealth/RPV top-squark searches in tt + many light-flavour jets with low MET - same final state as T T -> (t a)(t a), a -> gg; not interpreted for VLQs
- `arXiv:1810.10092 / arXiv:2401.16333` (abstracts): CMS pair-produced three-jet resonances (35.9 fb-1) and ATLAS RPV many-jets: cover B -> b Phi(gg) as a three-jet resonance pair (not interpreted for VLQ)
- `arXiv:2609.00127` (Sec. on exotic channels, Figs. 3-4 and text after Fig. 4): Recasting atlas: X X -> tS+ tS- -> ttbttb is 'the only exotic channel with top-philic decays that has been targeted so far' (ref [8] = CMS-PAS-B2G-24-005); TT -> 6t recast-excluded up to 1.65 TeV for BR=100%; 'a dedicated search ... can test VLQ masses well above 1.5 TeV' - identifies the 6t channel as the surviving one

**Closest existing results:**
- `INSPIRE 3157006 (CMS-PAS-B2G-24-005)` [CMS]: covers X5/3 pair, single-lepton, tW and t H+(tb). Region gap: No phi+ -> W+ gamma (photon) channel; no SSL+gamma; no b phi++ or b pi6
- `arXiv:1810.03188` [CMS]: covers X5/3 SSL + single-lepton (35.9 fb-1), tW decay. Region gap: Standard decay only; recastable for exotic modes per 1907.05894
- `arXiv:2607.28381` [ATLAS]: covers TT -> tS tS with >=1 S->gamma gamma, high ST/MET. Region gap: Needs S->gamma gamma; S->gg/WW-only not covered
- `arXiv:2610.03489` [CMS]: covers TT -> t phi, phi->gamma gamma, boosted hadronic tops. Region gap: Same, CMS side
- `arXiv:2506.08825` [CMS]: covers tt + >=6 light jets, 0-2 leptons, low MET. Region gap: Not interpreted for T -> t a(gg); acceptance for VLQ kinematics unknown (UNVERIFIED)
- `arXiv:2402.13808` [CMS]: covers B pair fully hadronic bH/bZ. Region gap: Fixed H/Z masses; Phi mass scan absent
- `arXiv:2606.30862` [CMS]: covers BSM interpretations in 4t/3t production events (SSL/multilepton). Region gap: Signal-region overlap with TT->6t is high (SSL/3L + many b); VLQ 6t interpretation not found in title/abstract - read before claiming gap (UNVERIFIED)

**HL-LHC projection docs:** Collaboration HL projections exist only for standard VLQ decays (CMS HL T->bW/tZ/tH single-lepton, INSPIRE 2809474/2611744; ATLAS 2025 single-T b-jet projection INSPIRE 3071495; arXiv:1812.07831 VLQ section; arXiv:1902.03942). No collaboration HL projection for exotic VLQ->S or X5/3 exotic decays found. Pheno HL studies: 2203.13753 (roadmap benchmarks for HL-LHC), 2204.09005, 2606.20054, 1812.11286 (6-top), 2505.07769 (hadronic B->b Phi).

**Showstoppers:** SSL + hard photon: fake-photon (jet->gamma) and charge-flip backgrounds must be data-driven (admitted by 1907.05894); phi+ -> W+ gamma BR is model-dependent (anomaly-induced). Fully hadronic 2b4j/6b: huge QCD multijet background, combinatorics, but high-HT triggers are fine for TeV-scale VLQs; Phi mass scan multiplies the signal grid. 6t: tiny SM background but VLQ pair cross section falls steeply above 1.5 TeV - HL gain is mostly luminosity-driven; BR into exotic channel is model-dependent (recasting atlas notes full models dilute the 6t BR). Overall the exotic-decay space is a large model-dependent grid; collaborations prefer model-independent fiducial limits (as 2607.28381 does).

**Confidence:** medium

**Notes:** Scout's seed S019 mis-describes the physics (X5/3 cannot decay to t + neutral a; it is t phi+ with phi+ -> W+ gamma/a W+). The biggest correction is CMS-PAS-B2G-24-005 (X5/3 -> t H+) and the two diphoton T->t phi searches (ATLAS 2607.28381, CMS 2610.03489). CMS 2610.03489 reports a 2.7 sigma local excess (1.5 global) - an HL follow-up in S->gamma gamma is natural but is a continuation, not a gap. The 6t channel is the cleanest surviving item and is explicitly flagged by an independent recast paper; CMS 2606.30862 (BSM in 3t/4t events) and ATLAS 2609.24950 (top-philic resonance + tops) are the multi-top searches whose SRs a 6t signal would populate; their VLQ-6t interpretation was not checked in full text. S->long-lived and S->tautau channels were not checked in depth (UNVERIFIED either way).

<details><summary>Queries run (14)</summary>

- `(collaboration:CMS or collaboration:ATLAS) and (t "vector-like" or t vectorlike) and date > 2021 (50 results scanned)`
- `cites 1907.05894 (42 citing papers scanned)`
- `(collaboration:CMS or collaboration:ATLAS) and (t "charge 5/3" or t "5/3")`
- `r CMS-PAS-B2G-24-005`
- `(collaboration:CMS or collaboration:ATLAS) and (t three-jet or t "three jets" or t trijet) and t pair and date > 2017`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:stealth and abstracts.value:"top squark" and date > 2018`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"vector-like" and (pseudoscalar or "new scalar") and date > 2019`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"same-sign" and abstracts.value:photon and date > 2016`
- `collaboration:ATLAS and pair-produced and "three jets" and date > 2018`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"vector-like" and (HL-LHC or "3000 fb")`
- `inspire get: 2505.07769, 2609.00127, 1908.07524, 2203.13753, 2610.03489, 2607.28381, 2402.13808, 2604.10729, 2602.20477`
- `full-text grep of arXiv:2609.00127 (dedicated search / exotic channels / ref [8])`
- `(collaboration:CMS or collaboration:ATLAS) and ("six top" or "three top" or "multi-top" ...)`
- `(collaboration:CMS or collaboration:ATLAS) and abstracts.value:"top-philic" and date > 2020`

</details>
