# TOP CANDIDATES: HL-LHC analysis ideas after Gate 5 (arbiter)

Date: 2026-10-06. Pipeline: 10 literature scouts produced 199 seeds. These were merged into 74 directions and triaged at Gate 2 (27 PASS, 37 HOLD, 10 REJECT). Gate 3 sent 27 to adversarial review: 26 were narrowed, 1 died and none came through intact. Gate 4 gave the 10 strongest separate experimental, feasibility and theory reviews. This document comes from the Gate 5 arbiter.

- Scores and machine-readable ranking: `research/rankings/ranking.{md,json}`
- Citation audit: `research/reports/citation_audit.json`
- Narrative of the search: `research/reports/literature_review.md`

Every reference ID below was resolved on INSPIRE. Experimental notes without an arXiv ID are cited as `INSPIRE:<recid>`, with the report number where known.

**Rules followed.** A finding is never called "new", "unexplored" or "first". Each gap carries a status-taxonomy label instead. Novelty is classified as theory, phenomenology or experimental analysis. **This document does not pick a candidate for you.**

## Summary of the ranking

**Honest headline.** Nothing survived intact. In every one of the ten cases a published phenomenology paper already proposes the analysis. What remains open is the experimental execution, meaning an ATLAS/CMS analysis or a collaboration-level projection. For three candidates even that reduces to a recast or a projection.

| Rank | ID | Tier | Sum/50 | Confidence | Gap type | One-line surviving gap |
|---|---|---|---|---|---|---|
| 1 | C001 | A | 36 | Medium | proposed-not-searched (ATLAS/CMS) | Coplanar non-helical-track search for EW-charged quirks, m_Q >~ 180 GeV, Lambda ~0.3-30 keV |
| 2 | C005 | A | 32 | Medium | constrained-but-region-open | Higgs-portal hadronic dark showers decaying in the tracker (c*tau 1-100 mm), VH-tagged multi-DV |
| 3 | C019 | B | 35 | Medium | proposed-not-searched / not reinterpreted | Charge-2 parent + same-sign displaced vertex from long-lived H++ (recast CMS 2110.04809 first) |
| 4 | C044 | B | 33 | Medium | searched-limited / indirectly covered (capped) | Dedicated TT -> 6t search above ~1.6 TeV; SSL + photon for X5/3 |
| 5 | C015 | B | 29 | Medium | interpretation gap (capped) | t -> q a with a light long-lived ALP in HCAL/muon system: add top-decay signal to existing searches |
| 6 | C051 | B | 30 | Medium | one-observable-not-another | Unfolded A5-A7 / l=3 null tests above the Z peak; sin2theta_W running |
| 7 | C003 | B | 28 | Low | constrained-but-region-open | Isotropic displaced hadronic SUEP; HL projection of prompt SUEP |
| 8 | C008 | C | 27 | Medium | proposed-not-searched (Run-3 type) | Photon-enriched SVJ; photon-ISR benchmark excluded via visible decays |
| 9 | C040 | C | 25 | Medium | projection only (capped) | Collaboration HL projection of compressed direct stau |
| 10 | C066 | C | 23 | Medium | reinterpretation + projection (capped) | e/mu + c-tag resonant LQ (flavour-rotation reinterpretation of existing results) |

Tier definitions:
- **A:** worth a dedicated analysis study.
- **B:** worth a feasibility, recast or projection study first.
- **C:** insufficient or weak.

The table is sorted by judgement, with the veto check applied first, and not by sum. `rankings/ranking.md` explains each place where the order differs from the sums.

## Main disagreements adjudicated

1. **C040, mass-splitting window.** The theory reviewer, using 2308.05723, finds that the relic-motivated window is Delta m <~ 30 GeV, and <~ 10 GeV for a right-handed stau. The 30-60 GeV region needs mixed LSPs that LZ excludes. The feasibility reviewer finds little sensitivity below Delta m ~ 15 GeV. **Verdict:** both are evidence-based. The window that is both motivated and reachable is only about 15-30 GeV, which lowers the value of the projection.
2. **C066, the "5.7 (4.2) TeV" figure.** The Gate 3 target text called this an HL-LHC mass reach from 2005.06475. All three Gate 4 reviewers independently found that these are the masses up to which the HL resonant bound would beat the atomic-parity-violation (Q_W) bound for lambda_eu (lambda_ed). **Verdict:** corrected in all deliverables.
3. **C008, photon-ISR benchmark.** The adversarial and experimental reviewers call it proposed-not-searched. The theory reviewer shows that ATLAS 2403.08547 limits g_q < 0.06-0.1 for 200-650 GeV, while the 2409.04741 benchmark uses g_q = 0.25 and so is excluded through its visible Z' -> qq decays. **Verdict:** the ATLAS bound is in the source, and the reviewer's rescaling for B(qq) = 0.53 is their own arithmetic. g_q = 0.25 exceeds the bound either way, so the benchmark is excluded and only a reduced-rate corner survives.
4. **C015, coupling-structure caveat.** The theory reviewer argues that generic UV flavour structures make the branching ratio small (BR <~ 1e-6 to 1e-8 for cm-m lifetimes). This is the reviewer's **own derivation, not a published result**. **Verdict:** kept as a stated caveat that lowers theoretical robustness. It is not used as evidence against the target.
5. **C019, displaced H++ coverage.** The adversarial review relied on the opposite-charge requirement of ATLAS 2601.05664. The experimental reviewer found CMS 2110.04809, which has no charge requirement. **Verdict:** the regime is "indirectly covered / not reinterpreted". A recast must come before any novelty claim.
6. **C005, the "largely unconstrained" claim.** The scout's Snowmass quote (2203.09503) was overturned by CMS 2402.01898. The theory reviewer adds that the quote concerned flavour bounds on t-channel models in the first place.

**Unresolved citations:** none of the IDs used here failed to resolve (see the audit). Two numbers are flagged UNVERIFIED:
- The CMS 12.9 fb-1 tau tau H++ limit is quoted as both 535 and 396 GeV in different sources.
- The CMS-PAS-B2G-24-005 content was read only at public-page/abstract level.

## Research lineage (top three)

### C001 Quirks
```
Foundational theory      Kang-Luty macroscopic strings / quirks (0805.4642); infracolor with heavy-only matter
  -> development         Tevatron/LHC quirk phenomenology (1106.2569); neutral-naturalness quirks (1512.05782)
  -> pheno prediction    coplanar-hit tracker method, 100 eV-30 keV, 650 GeV EW at 300 fb-1 (1708.02243);
                         GNN non-helical tracking (2410.00269); stopping quirks (1811.08903)
  -> exp. interpretation recast of HSCP + monojet (1703.00912); CMS OoT recast (1811.08903)
  -> existing searches   D0 high-ionisation (1008.3547); FASER first LHC quirk search (2607.26195)
  -> current constraints FASER: 300 eV-100 keV, m_Q <= 179 GeV at 10 keV; HSCP recast: no bound at 1 keV for (1,1)_-1
  -> remaining gap       central ATLAS/CMS, m_Q > ~180 GeV, Lambda ~0.3-30 keV (proposed-not-searched)
  -> HL-LHC analysis     Phase-2 tracker + HLT plane-finder (or GNN) + ISR-MET trigger; MTD timing for slow tracks
```

### C005 Higgs-portal dark showers in the tracker
```
Foundational theory      hidden valleys (hep-ph/0604261); exotic Higgs decays (1312.4992)
  -> development         emerging jets (1502.05409); dark-shower benchmarks and decay portals (2103.01238); dark pions (2110.10691)
  -> pheno prediction    Snowmass dark-shower report (2203.09503); EJ Higgs-portal recast (2307.04847);
                         HL-LHC tracker + MDS projection (2512.24814)
  -> exp. interpretation CMS MDS dark-shower interpretation, 5 portals (2402.01898)
  -> existing searches   CMS EJ (2403.01556), ATLAS EJ (2505.02429, 2510.12347), CMS displaced jets H->SS (2409.10806),
                         ATLAS ZH multi-DV (2107.06092), CMS muonic dark showers (2511.11888)
  -> current constraints B(H->dark) ~2e-3 at long c*tau (MDS); H->SS at 1 mm-1 m (two-body only)
  -> remaining gap       hadronic, many-LLP, c*tau 1-100 mm, VH/VBF-tagged (constrained-but-region-open)
  -> HL-LHC analysis     lepton-tagged VH multi-DV counting (~background-free); ggF/VBF needs a Phase-2 displaced L1 seed
```

### C019 Long-lived doubly charged scalars
```
Foundational theory      type-II seesaw / Higgs triplet; doubly charged Higgs bosons (INSPIRE:214561, 1985)
  -> development         H++ production and decays (hep-ph/0506176); cascades H+ -> H++ W* (1105.2209)
  -> pheno prediction    displaced H++ in type-II / LR (1808.00943); GM long-lived H5++ (2410.19561);
                         HL-LHC displaced H++ (2608.27251); compressed triplet (2305.06889, 2603.15882)
  -> exp. interpretation recast of type-II limits (2108.10952, quoted via 2305.06889)
  -> existing searches   ATLAS prompt H++ (2211.07505), H++ -> WW (2101.11961), multi-charged (2303.13613),
                         CMS displaced leptons, no charge requirement (2110.04809), ATLAS OS displaced vertices (2601.05664)
  -> current constraints prompt to ~1 TeV (ll); WW 350 GeV; stable to ~1 TeV; displaced 0.1-100 mm not reinterpreted
  -> remaining gap       charge-2 parent + same-sign DV (proposed-not-searched; indirectly covered to an unknown degree)
  -> HL-LHC analysis     recast 2110.04809/2410.16835, then a charged-parent DV search with Phase-2 displaced L1 tracking
```

## How to choose

These criteria are for the person making the decision. They are not a recommendation.

| Question | C001 | C005 | C019 | C044 | C015 | C051 | C003 | C008 | C040 | C066 |
|---|---|---|---|---|---|---|---|---|---|---|
| Needs collaboration-internal detector access (custom tracking/trigger, Phase-2 full sim)? | **Yes** (non-helical tracking, HLT) | Yes (displaced L1/DV at PU200) | Partly (DV with charged parent; trigger) | No (standard objects) | Partly (CalRatio/MDS objects) | No | Yes | Partly (jet ID without NEMF cut) | Partly (low-pT tau_h) | No |
| Can start with public tools / open data / recast? | Pheno-level Delphes only | Yes: recast H->SS DV searches | **Yes: recast 2110.04809** | **Yes: recast already exists (2609.00127)** | **Yes: add signal to public analyses** | **Yes: HEPData of 2202.12327; open data** | Truth-level only | Delphes only | Pheno projections exist | **Yes: flavour rotation** |
| Main risk | feasibility at PU200; FASER2/LHCb competition | ATLAS pre-emption; hadronisation model | recast may close the gap | small marginal reach | low novelty | small BSM leverage | squeezed theory region; no discriminant | ad hoc model; CMS pre-emption | ATLAS/CMS already on it | low motivation |
| Kind of payoff | new signature class at ATLAS/CMS | first tracker-region dark-shower limits | new charged-LLP topology | +few hundred GeV in mass | closes 1-35 GeV region | precision null tests | new topology | Run-3 search | projection | interpretation |
| Time to first result | long | medium | short (recast) then medium | medium | short | medium | long | medium | short | short |
| HL-LHC-specific? | yes (Phase-2 tracker/HLT) | yes (L1 tracking, VH stats) | yes (bkg-free 1/L scaling) | yes (luminosity -> mass) | partly | partly (stats for A5-A7; running) | speculative | weak | yes (stats) | partly |

Suggested decision criteria:
1. **No collaboration access:** start with a candidate whose first step is a recast or public-data study (C019, C015, C044, C051, C066). Among these, only C019's recast can lead on to a genuinely unsearched topology.
2. **Inside CMS or ATLAS, with Phase-2 simulation and trigger access:** C001 and C005 are the only gaps that need a new analysis. C005 is lower-risk but may be pre-empted. C001 is higher-risk and higher-novelty.
3. **Prioritising robustness of motivation:** C019 (type-II seesaw) and C044 (composite Higgs) have the best theory motivation. C008 and C066 have the weakest.
4. **Prioritising publication impact with modest effort:** a Run-2-data recast or reinterpretation (C019, C015) can become a paper within months. The Tier A items are multi-year.

## Promising but insufficiently reviewed (NOT ranked)

These candidates had only a Gate 3 adversarial review. Under the lean budget they had no independent theory, experimental or feasibility review. Treat every statement here as a single-reviewer finding.

- **C017: time-resolved heavy-neutrino oscillations (LNV/LNC ratio vs proper time) in displaced HNL decays.** *Insufficiently reviewed.*
  - Covered already: Dirac and Majorana endpoints are interpreted by ATLAS (2503.16213, 2204.11988) and CMS (2201.05578, 2403.00100).
  - Surviving gap: the intermediate mass-splitting regime, measured as R_ll versus decay time (one-observable-not-another). HL phenomenology exists (2212.00562).
  - Risk: the viable window (m_N ~5-20 GeV, |theta|^2 ~1e-7-1e-6) overlaps existing exclusions, so yields may be too small.
  - Cheap first step: reinterpret existing endpoint limits as R_ll(Delta m).
- **C061: triple-Higgs production beyond 6b (4b+tautau, multilepton), plus a multi-channel HHH combination.** *Insufficiently reviewed.*
  - Status: searched-limited-regime.
  - SM HHH is about 0.079 fb at 13 TeV (2411.02040), so it is unobservable. Only large kappa_4 or resonant BSM enhancement is testable.
- **C009: semi-dark Higgs decays h -> Z X(invisible).** *Insufficiently reviewed.*
  - Status: no dedicated search was found.
  - The physics window is small. The HL pheno reach (2206.01214) is only a few times better than the indirect H -> invisible bound (1902.00134).
- **C047: VLQ "portal matter" T -> t + dark photon (boosted or displaced lepton-jet).** *Insufficiently reviewed.*
  - Status: proposed-not-searched at ATLAS/CMS, with phenomenology in 1904.05893 and 2112.08425. Novelty is experimental-analysis only.
  - The branching ratio is model-dependent.
- **C048: colour-sextet fermionic top partners.** *Insufficiently reviewed.*
  - Pair production is mostly indirectly covered by SUSY recasts, to about 2.4-2.6 TeV.
  - Residual gaps: compressed bb+MET spectra and >= 5-6 top final states.
  - Signal modelling has no validated shower tool and no NLO cross section.
- **C021: fully merged ALP photons at high m_gamma gamma, and VBF-parked merged conversions.** *Insufficiently reviewed.*
  - Only the experimental execution survives. HL projections already exist, and Belle II may overtake it in part of the space.

---

# Candidate dossiers (12 sections each)

## 1. C001: Quirks, coplanar non-helical tracks from EW-charged quirks (Tier A, confidence Medium)

**1. Summary.** Quirks are heavy fermions charged under the SM and under a new confining group SU(N_IC) with a scale Lambda well below their mass. A produced pair stays bound by a long flux tube.
- For Lambda ~0.3-30 keV the pair oscillates on um-cm scales (1708.02243 Eq. 1). The tracks are neither helical HSCPs nor a single straight track.
- The proposal is a central ATLAS/CMS search for the resulting coplanar, mutually curving, slow, ~2x-ionising hit patterns.
- Target: colour-neutral EW quirks above the FASER reach (m_Q >~ 180 GeV).

**2. Why it matters.**
- Quirks arise generically when a hidden non-Abelian group has only heavy matter. Neutral-naturalness top partners are quirks (1512.05782).
- The signature is a hole in the trigger and reconstruction model that ATLAS/CMS use. Standard tracking assumes helices, so the signal is invisible to existing searches in this regime.

**3. Foundational literature.**
- Framework and regimes: 0805.4642 (Kang, Luty).
- Collider follow-ups: 1106.2569.
- Neutral-naturalness quirks: 1512.05782.
- Coplanar-hit tracking proposal: 1708.02243.
- Stopping quirks: 1811.08903.
- ML non-helical tracking: 2410.00269, 2509.08878.

**4. Current state of the field.** The phenomenology is mature. The 2026 FASER result is the first LHC-experiment quirk search (2607.26195). A 2026 review states "there are no dedicated LHC searches" at ATLAS/CMS (2606.30760). Competing proposals:
- LHCb VELO (2601.09023).
- FASER2/FPF timing (2404.13814).
- Quirk-SUEP for microscopic strings (2506.11192).
- Wgamma/WZ + glueball DV (2504.02940).

**5. Existing experimental coverage.**
- FASER 2607.26195 excludes 300 eV < Lambda < 100 keV up to m_Q = 179 GeV at 10 keV (Figs. 4-5).
- D0 1008.3547: >107 GeV for 10 keV-1 MeV.
- The recast of CMS/ATLAS HSCP and monojet (1703.00912 Table II) gives 650/150 GeV at 1/100 eV for (1,1)_-1, and **no bound at 1 keV**.
- The CMS stopped-particle recast (1811.08903) covers low Lambda.
- ATLAS stopped-particle (2104.03050) and recent HSCP searches (2410.09164, 2502.06694) have no quirk interpretation.
- There is no quirk projection in the HL-LHC Yellow Report (1812.07831).

**6. Remaining gap.** Central ATLAS/CMS coplanar-hit search, colour-neutral EW quirks, m_Q ~0.2-0.9 TeV, Lambda ~0.3-30 keV. Status: proposed-not-searched at ATLAS/CMS; LHC-not-projected-to-HL.
- The experimental and theory reviewers both narrow the original 0.1-100 keV band.
- Above ~30 keV the pair is unresolved and looks like a single straight HIP-like track.
- Below ~300 eV the HSCP recast applies.

**7. HL-LHC opportunity.**
- The Phase-2 all-silicon trackers (more layers, wider eta) help.
- Full tracking at the HLT makes a plane-finder or GNN path conceivable (1708.02243 Sec. III C; 2410.00269 Sec. VII).
- MTD/HGTD timing could tag slow (beta < 1) pairs.
- If the search stays background-free, reach goes from ~650-700 GeV (300 fb-1) to ~850-900 GeV at 3 ab-1. This is a feasibility-reviewer ESTIMATE.

**8. Experimental manifestation.** Events with ISR-driven MET > ~200 GeV and two tracks lying on one plane (Delta s < 100 um), curving toward each other, with anomalous dE/dx and low beta. The measurables:
- the excess count;
- a trajectory fit that gives m_Q and Lambda (1708.02243 App. A).

**9. Main obstacles.**
- **Trigger:** ISR-MET with ~10% efficiency (1708.02243 Table I). The Phase-2 L1 track finder assumes helices (2110.02826).
- **Pileup:** no study exists at PU 140-200.
- **Background:** Z(nunu)+jets with pileup gives ~1e-2 fb coplanar background already at mu = 50 (1911.02223), so the search is not automatically background-free.
- **Modelling:** a bespoke Geant4 quirk simulation is needed.
- **Competition:** FASER2 (not approved, per 2601.09023) and LHCb Upgrade II.

**10. Novelty confidence.**
- High that no ATLAS/CMS search exists.
- Medium that the region is not indirectly covered.
- The novelty is a **novel experimental analysis**. It is not new phenomenology.

**11. Recommended next step.** A Phase-2 full-simulation feasibility study inside a collaboration covering three things:
1. hit/stub formation for quirk pairs at PU 200;
2. the random-coplanar background rate;
3. the HLT CPU budget of a plane-finder.

In parallel, cross-check that no internal effort exists. The adversarial reviewer saw an ATLAS "Quirks" Confluence page title (UNVERIFIED).

**12. References.** 0805.4642; 1106.2569; 1512.05782; 1708.02243; 1703.00912; 1811.08903; 1008.3547; 2607.26195; 2104.03050; 2410.09164; 2502.06694; 2410.00269; 2509.08878; 1911.02223; 2110.02826; 2404.13814; 2601.09023; 2506.11192; 2504.02940; 2512.20696; 1903.04497; 2606.30760; 1812.07831.

## 2. C005: Higgs-portal dark showers with hadronic GeV dark mesons in the tracker (Tier A, confidence Medium)

**1. Summary.** The Higgs decays to dark quarks, which shower and hadronise into GeV-scale dark mesons. These decay hadronically after ~1-100 mm, giving several low-mass displaced vertices inside the tracker.
- The target is a CMS search using multi-DV counting in lepton-tagged VH, plus VBF and ggF if a Phase-2 displaced L1 seed exists.
- Existing Higgs-portal dark-shower limits cover the muon system (long c*tau) only.

**2. Why it matters.** Exotic Higgs decays are the most generic portal to a hidden sector (1312.4992). Confining hidden sectors with portal-suppressed decays naturally give displaced vertices (hep-ph/0604261, 2103.01238). The undetected-Higgs branching ratio still allows O(10%) (2207.00092, B_u < 0.12).

**3. Foundational literature.**
- Hidden valleys: hep-ph/0604261.
- Emerging jets: 1502.05409.
- Exotic Higgs decays: 1312.4992.
- Benchmark decay portals and lifetime bounds: 2103.01238.
- Dark pions: 2110.10691.
- Snowmass report: 2203.09503.
- Trigger studies: 2103.08620.

**4. Current state of the field.**
- CMS has set the first Higgs-portal dark-shower limits using muon-detector showers (2402.01898; five portals, 2-20 GeV, B ~2e-3).
- Muonic dark showers are covered (2511.11888; Run-3 scouting 2606.25840).
- Pheno: an EJ Higgs-portal recast (2307.04847) and an HL-LHC tracker+MDS projection (2512.24814).
- ATLAS has a Delphes prospect study for Higgs-portal dark jets (INSPIRE:3201494). It is a proceedings item, not an approved analysis.

**5. Existing experimental coverage.**
- CMS MDS 2402.01898: ggF only, long c*tau.
- CMS displaced jets 2409.10806: H -> SS only, c*tau 1 mm-1 m.
- ATLAS ZH >= 2 DVs 2107.06092: m_a 16-55 GeV, two-body b-bbar; DV mass cut m/DeltaR_max > 3 GeV.
- CMS ZH LLP 2110.13218.
- EJ searches (CMS 2403.01556; ATLAS 2505.02429, 2510.12347) target TeV mediators and are kinematically blind to H(125).
- ATLAS CalRatio + W/Z 2407.09183.
- No official HL projection exists. CMS-PAS-FTR-18-018 (INSPIRE:1704286) uses an H -> 2 LLP benchmark.

**6. Remaining gap.** Hadronic, many-LLP dark showers from H(125) with c*tau ~1-100 mm, decaying inside the tracker. Status: constrained-but-region-open; LHC-not-projected-to-HL.
- Natural mass core: m ~5-20 GeV. The theory reviewer's evaluation of 2103.01238 Eqs. 4 and 15 shows that 2-4 GeV at mm lifetimes needs tuning.
- Production tags: VH/VBF.
- Selection: multi-DV with low vertex mass.
- A recast of H -> SS results could close part of the gap.

**7. HL-LHC opportunity.**
- Statistics: ~1.9e8 Higgs bosons at 3 ab-1 (ESTIMATE, from 1902.00134 cross sections).
- The VH(lepton) >= 2 DV channel is near background-free, so it scales ~L.
- The Phase-2 L1 track trigger (pT > 2 GeV) and a displaced extension (INSPIRE:2908980, 1705.04321; simulation-level only) would open ggF/VBF.

**8. Experimental manifestation.**
- Signal: W/Z -> leptons (or VBF jets) plus >= 2 multi-track displaced vertices at 1-300 mm with masses above the B-hadron range (for m >~ 5 GeV). The total visible mass is <= m_H.
- Result: limits on B(H -> dark) per decay portal on an (m, c*tau) grid, with alternative hadronisation tunes as a systematic (2103.01238, 2203.09503).

**9. Main obstacles.**
- **Trigger for ggF/VBF:** Run-3 displaced-jet triggers keep ~0.4-1% of H -> SS (2409.10806).
- **Low-mass DV backgrounds:** K_S, Lambda, material interactions and heavy flavour for m <~ 5 GeV.
- **Pileup:** combinatorial DVs at PU 200.
- **Hadronisation-model dependence:** 2505.03058.
- **Pre-emption by ATLAS:** INSPIRE:3201494.
- **Realistic reach:** ~1e-3 in B(H -> dark), not the 1e-4 of 2512.24814. That projection has no pileup, LO bbbar-only background and no systematics.

**10. Novelty confidence.** Medium. No tracker-region dark-shower interpretation exists at either experiment, but recasts could cover part of it, and ATLAS is clearly interested. The novelty is a **novel experimental analysis**. The phenomenology exists in 2512.24814.

**11. Recommended next step.**
1. A quick recast of CMS 2409.10806 and ATLAS 2107.06092 for the 2103.01238 portal benchmarks at c*tau 1-100 mm, to measure what is truly open.
2. A CMS Phase-2 study of the VH(lepton) multi-DV selection with realistic low-mass DV backgrounds at PU 200.

**12. References.** hep-ph/0604261; 1502.05409; 1312.4992; 2103.01238; 2110.10691; 2203.09503; 2103.08620; 2402.01898; 2409.10806; 2107.06092; 2110.13218; 2403.01556; 2505.02429; 2510.12347; 2407.09183; 2511.11888; 2606.25840; 2307.04847; 2512.24814; 2505.03058; 1902.00134; 2207.00092; 1705.04321; INSPIRE:3201494; INSPIRE:2908980; INSPIRE:1704286.

## 3. C019: Doubly charged scalars, long-lived (same-sign displaced vertex), compressed and tau_h channels (Tier B, confidence Medium)

**1. Summary.** If the triplet vev is small, H++ can be long-lived (c*tau ~0.1-100 mm).
- When it decays to W+W+ (fermiophobic case) or to l+l+, the result is a charge-2 track that ends in a high-mass vertex whose products carry net charge +2.
- No CMS/ATLAS search reconstructs this topology.
- Secondary sub-targets: compressed-spectrum cascades with soft same-sign leptons, and hadronic-tau final states.

**2. Why it matters.** The type-II seesaw is among the best-motivated neutrino-mass models (theory motivation 4/5). Its H++ flavour pattern tests oscillation data directly (1808.00943; hep-ph/0506176). The long-lived regime is where prompt multilepton and HSCP searches both lose efficiency (2608.27251 Sec. 3).

**3. Foundational literature.**
- INSPIRE:214561 (1985, doubly charged Higgs bosons).
- H++ production: hep-ph/0506176.
- Cascades: 1105.2209.
- Displaced-vertex signatures in type-II/LR: 1808.00943.
- GM long-lived H5++: 2410.19561.
- HL-LHC displaced H++: 2608.27251.
- Compressed triplet: 2305.06889, 2603.15882.

**4. Current state of the field.**
- ATLAS prompt H++ -> ll (e/mu only): 2211.07505, limit 1080 GeV. Its 4-lepton efficiency is disputed by a recast (2608.03988).
- ATLAS H++ -> WW: 2101.11961, 350 GeV pair production.
- VBF H5 searches: 2407.10798, 2104.04762.
- Long-lived multi-charged particles: ATLAS 2303.13613, CMS 2410.09164.
- CMS has no full Run-2 H++ paper. There is only the 12.9 fb-1 PAS (INSPIRE:1510936) and Phase-2 prospects for ee/mumu (INSPIRE:2084511).

**5. Existing experimental coverage.**
- ATLAS displaced dilepton vertices require **opposite** charge (2601.05664).
- CMS displaced leptons (2110.04809, d0 0.01-10 cm) have **no charge requirement** and no vertex requirement. They have never been interpreted for H++.
- ATLAS displaced leptons Run 2+3 (2410.16835).
- Hadronic DV searches (1811.07991, 2012.01581) are tuned for neutral LLPs.

**6. Remaining gap.**
- (i) A charge-2-parent, same-sign displaced-vertex search, m ~150 GeV-1 TeV in the fermiophobic case and 100-150 GeV in neutrino-mass type-II. Status: proposed-not-searched as a dedicated topology; indirectly covered to an unknown degree by 2110.04809.
- (iii) tau_h channels with full Run 2/3. Status: searched-limited-regime. This is a legacy gap, not an HL-specific one.
- (ii) Compressed soft same-sign leptons. Status: theory-explored-untested. Systematics-limited, about 1/5 feasible.

**7. HL-LHC opportunity.**
- Drell-Yan cross sections: 1.60 fb at 500 GeV and 0.15 fb at 800 GeV (2608.27251 Table 1).
- A near-background-free DV search scales ~1/L, so HL statistics matter.
- A Phase-2 displaced L1 tracking extension (INSPIRE:2908980) would address the trigger.
- Pheno reach is ~0.01 fb at 3 ab-1 (2608.27251 Figs. 10-11), but with idealised trigger and background.

**8. Experimental manifestation.** Pair-produced H++ H-- giving one or two displaced vertices at 1-100 mm.
- Each vertex has m_DV >= 20 GeV, same-sign leptons or W*W* decay products, and an incoming short charged track with ~4x MIP dE/dx in the innermost pixel layers.
- Result: limits on sigma x BR versus (m, c*tau).

**9. Main obstacles.**
- An efficient L1/HLT path for low-HT displaced WW.
- The data-driven fake high-mass DV tail at PU 200. The pheno background MC weights are ~1e7, so its background estimate is meaningless.
- Small cross sections.
- The theory caveat that TeV-scale long lifetimes need the fermiophobic assumption (no neutrino-mass link).
- Pre-emption of the tau_h piece. A CMS-group thesis (INSPIRE:3063898) projects about 730 GeV at HL-LHC.

**10. Novelty confidence.** Medium for (i) once a recast confirms that 2110.04809 has low acceptance. Low for (iii). The novelty is a **novel experimental analysis**. The pheno exists.

**11. Recommended next step.**
1. Recast CMS 2110.04809 and ATLAS 2410.16835 for 2608.27251-type benchmarks, using public efficiency maps where available. This decides whether (i) is open.
2. If it is, build a Phase-2 study of the charged-parent DV trigger and background.

**12. References.** INSPIRE:214561; hep-ph/0506176; 1105.2209; 1808.00943; 2410.19561; 2608.27251; 2305.06889; 2603.15882; 2108.10952; 2211.07505; 2101.11961; 2407.10798; 2104.04762; 2303.13613; 2410.09164; 2110.04809; 2410.16835; 2601.05664; 1811.07991; 2012.01581; 2608.03988; 1802.00945; 1812.07831; INSPIRE:1510936; INSPIRE:2084511; INSPIRE:3063898; INSPIRE:2908980.

## 4. C044: VLQ exotic decays to new scalars: dedicated TT -> 6t; X5/3 -> t W+ gamma (Tier B, confidence Medium)

**1. Summary.** In composite-Higgs models the top partners (T, X5/3) can decay to a top plus a pNGB scalar instead of to bW/tZ/th. Two cases:
- If the neutral S0 is heavier than 2m_t, TT pair production gives six tops: same-sign or three leptons, many b-jets and very high S_T.
- A fermiophobic charged phi+ gives X5/3 -> t W+ gamma: same-sign leptons plus a hard photon.

**2. Why it matters.** A top-philic neutral pNGB is a generic prediction of gauge-fermion composite Higgs models (2609.00127 Sec. 4.1). Exotic decays dominate naturally when VLQ-quark mixing is small (2203.13753 Sec. IV). They weaken the standard VLQ limits by about 300-500 GeV (2203.13753 Fig. 3).

**3. Foundational literature.** 1211.5663 (top-partner hunter's guide); 1506.05110; 1907.05894 (X5/3 exotic decays); 1907.05929; 1908.07524; 2203.13753 (roadmap); 1812.11286 (six-top); 2508.14960 (multi-top VLQ); 2609.00127 (recasting atlas).

**4. Current state of the field.** The diphoton routes are already searched:
- ATLAS 2607.28381: M_T < 1620 GeV in its composite benchmark, with fiducial limits that include gamma gamma + ttbar/WW/ZZ.
- CMS 2610.03489: reports a 2.7 sigma local excess.

Other routes:
- Single T -> t phi(bb): CMS 2510.25874, 2604.10729.
- X5/3 -> t H+(tb): CMS-PAS-B2G-24-005 (INSPIRE:3157006).
- Collaboration HL projections exist only for the standard decays (INSPIRE:2611744, INSPIRE:3071495).

**5. Existing experimental coverage.**
- 6t: no direct search exists. A recast of SS2L/3L searches excludes it to 1.65 TeV at BR = 1, and to 1.30 TeV at BR(tS0) = 50% (2609.00127 Fig. 4a).
- X5/3 standard decays: SSL searches 1810.03188 and 1807.11883.
- Final-state neighbours with no VLQ interpretation: stealth/RPV tt + many jets (2506.08825, 2102.06976), trijet resonances (1810.10092, 2404.02992), and B -> bH fully hadronic (2402.13808).
- Not checked in full text: CMS 2606.30862 (BSM in 3t/4t events), which may populate the 6t signal regions.

**6. Remaining gap.** Status: searched-limited-regime / indirectly-covered. Novelty and literature-gap scores are capped at 2.
- An optimised dedicated 6t search above ~1.6 TeV.
- An SSL+gamma channel for X5/3. Its recast says it is already constrained "at the same level as the standard one" (1907.05894).
- S -> gg/bb at arbitrary mass: a reinterpretation-first gap.

**7. HL-LHC opportunity.**
- Above ~1.6 TeV the 6t region is near background-free, so the excluded cross section scales ~1/L.
- The HL-LHC adds the ~1.8-2.3 TeV band. A dedicated Run-3 search would already cover ~1.6-1.9 TeV (feasibility ESTIMATE).

**8. Experimental manifestation.**
- 6t: 2SS/3L/3SS leptons, >= 5 b-tags, >= 3 large-R or top-tagged jets, H_T > 2 TeV. Result: limits on sigma(TT) x BR(tS0)^2 versus m_T.
- X5/3: a photon with pT > 200 GeV accompanying SSL+b events, with a W-gamma mass handle.

**9. Main obstacles.**
- **Rate:** sigma(TT) at 2 TeV is ~0.13 fb, derived from 2508.14960.
- **BR dilution:** at an effective BR of 25%, about 1 signal event (ESTIMATE).
- **Backgrounds:** ttW+jets modelling (large uncertainties in ATL-PHYS-PUB-2025-017, INSPIRE:2909579) and SM tttt.
- **Fake photons:** unquantified for SSL+gamma.
- **Model dependence:** every channel depends on the assumed BRs.

**10. Novelty confidence.** Medium-low. Recasts already set strong bounds, so a dedicated search is an optimisation of an existing multilepton strategy. This is incremental experimental-analysis novelty.

**11. Recommended next step.**
1. Read CMS 2606.30862 in full to check for 6t coverage.
2. Run a recast-plus-optimisation study, starting from 2609.00127, to quantify the dedicated-search gain over the recast at 300 fb-1 and 3 ab-1 with realistic BRs.
3. Ask the SSL analyses to publish the leading-photon pT spectrum, as 1907.05894 suggests.

**12. References.** 1211.5663; 1506.05110; 1907.05894; 1907.05929; 1908.07524; 2203.13753; 1812.11286; 2508.14960; 2609.00127; 2607.28381; 2610.03489; 2510.25874; 2604.10729; 1810.03188; 1807.11883; 2209.07327; 2506.08825; 2102.06976; 1810.10092; 2404.02992; 2402.13808; 2606.30862; INSPIRE:3157006; INSPIRE:2611744; INSPIRE:3071495; INSPIRE:2909579.

## 5. C015: Long-lived light ALPs from exotic top decays t -> q a (Tier B, confidence Medium)

**1. Summary.**
- **Signal:** an ALP with flavour-violating top couplings is produced in t -> q a (q = u, c) inside ttbar events. For m_a ~1-35 GeV it decays after centimetres to metres, in the HCAL or the muon system.
- **Trigger:** the other top provides a lepton trigger.
- **Gap:** existing searches cover only m_a = 40 and 55 GeV with inner-detector vertices.

**2. Why it matters.** The ALP EFT with flavour structure is well defined (2110.10698, 2101.07803). The ttbar rate is precisely known, so the top-decay channel is a clean probe of the t-q-a couplings, which complements meson-decay bounds.

**3. Foundational literature.** 1611.09355 (ALPs in FCNC); 2101.07803 (charming ALPs); 2110.10698 (flavour probes of ALPs); 2202.09371 (ALPs from the top, the original proposal); 2404.06126 (recast plus HL projection); 2306.08686 (ttbar + displaced dimuon); 2307.11154.

**4. Current state of the field.** ATLAS 2403.15332 probes long-lived t -> aq directly: m_a = 40 and 55 GeV, a -> cc/gg, BR > 0.1% excluded for 1.6-130 mm. HL phenomenology exists:
- 2202.09371 App. A: background-free lines down to BR ~1e-8.
- 2404.06126: 3 ab-1.

**5. Existing experimental coverage.**
- ATLAS 2403.15332: inner-detector displaced vertices, 1-lepton region.
- ATLAS CalRatio + W/Z (2407.09183): has a lepton-triggered selection, but treats ttbar as background and has no top-decay signal.
- CMS MDS (2402.01898): MET trigger.
- CMS displaced dimuons (2112.13769, 2205.08582, 2606.25840): no top interpretation.
- ATLAS prompt t -> qX, X -> bb (2301.03902).
- CMS ttbar + phi production (2402.11098).
- Higgs-decay ALPs: well covered (2312.03306, INSPIRE:2903120).

**6. Remaining gap.** t -> q a with m_a ~1-35 GeV decaying in the HCAL or muon system, presented model-independently as BR(t -> qX) versus (m_X, c*tau). Status: searched-limited-regime. The gap is mostly an **interpretation of existing analyses** (cap applied).
- The displaced mu mu/gamma gamma sub-target is not robust: the visible branching ratios for 1 GeV < m_a < 2m_c differ between 2202.09371 and 2110.10698.

**7. HL-LHC opportunity.**
- About 2.4e9 ttbar events at 3 ab-1 (ESTIMATE), with an unbiased lepton trigger.
- The muon-system category is low-background and scales nearly linearly with luminosity.
- Phase-2 timing helps the trackless-jet veto under pileup.

**8. Experimental manifestation.** A lepton+jets ttbar event in which one top is replaced by a prompt light jet plus a trackless, high E_had/E_em jet or a muon-system cluster, with m(LLP + jet) ~ m_t. Result: limits on BR(t -> qX) on an (m_X, c*tau) grid.

**9. Main obstacles.**
- The HCAL category is background-limited. The claimed 1e-7 to 1e-8 reach assumes zero background (2202.09371).
- The track veto degrades under PU 200.
- Very light (2 GeV) ALPs are hard to separate from neutral-hadron-rich jets.
- Theory caveat (the reviewer's own derivation, not published): generic UV flavour structures prefer BR <~ 1e-6 for cm-m lifetimes.

**10. Novelty confidence.** Low as a novel analysis. Medium that adding the signal interpretation would close an uncovered region.

**11. Recommended next step.**
1. A pheno recast of ATLAS 2407.09183 (W channel) and 2403.15332 for m_a = 2-35 GeV.
2. Then propose a top-decay signal for the next ATLAS CalRatio and CMS lepton-triggered MDS iterations.

**12. References.** 1611.09355; 2101.07803; 2110.10698; 2202.09371; 2404.06126; 2306.08686; 2307.11154; 2403.15332; 2407.09183; 2402.01898; 2112.13769; 2205.08582; 2606.25840; 2301.03902; 2402.11098; 2312.03306; INSPIRE:2903120.

## 6. C051: High-mass Drell-Yan angular coefficients and sin2theta_W running (Tier B, confidence Medium)

**1. Summary.** A full, phi-dependent, unfolded measurement of the Drell-Yan angular coefficients A0-A7 above the Z peak, in m_ll and pT_ll.
- **Narrowed target:** the T-odd A5-A7 and the l=3 harmonics, which are near-null tests in the SM.
- **Second piece:** an experimental extraction of the running of sin2theta_W(mu) from high-mass neutral-current Drell-Yan.

**2. Why it matters.** Energy-growing effects make high-mass Drell-Yan a precision probe (1609.08157). A5-A7 and the l=3 structures are tiny in the SM, so they act as clean null tests of dim-8 CP-odd and psi^4 D^2 operators (2511.19617, 2003.11615). The running of sin2theta_W above m_Z has not been measured at the LHC (2307.10737).

**3. Foundational literature.** 1609.08157; 2003.11615; 1708.00008 (precise A_i predictions); 2405.04069; 2412.13014; 2511.19617; 2512.05018; 2302.10782; 2307.10737.

**4. Current state of the field.**
- Full A0-A7 has been measured only at the Z peak: ATLAS 1606.00689, CMS 2604.25678, LHCb 2203.01602.
- At the Z peak, SM Lam-Tung violation is O(0.1) and under-predicted by NNLO-matched MC (2604.25678).

**5. Existing experimental coverage.**
- CMS 2202.12327 measures A_FB and A0 (pT/y-integrated, template-level) for m > 170 GeV. This **kills the high-mass A_FB sub-idea**.
- CMS 2408.07622: A4 up to 150 GeV.
- ATLAS 1710.05167: triple-differential up to 200 GeV.

**6. Remaining gap.** Status: one-observable-not-another.
- Unfolded A0-A7 above 101 GeV, especially A5-A7, plus the l=3 basis.
- A collaboration-level sin2theta_W(mu) extraction. Only a pheno projection exists (2302.10782).

**7. HL-LHC opportunity.**
- About 22x the Run-2 statistics in the statistics-limited high-mass, high-pT cells.
- Extended forward lepton acceptance (to |eta| ~2.8) reduces dilution and PDF uncertainty (1902.04070 Sec. 4.4.5).
- sin2theta_W precision of ~1.9% at 1 TeV at the HL-LHC (2302.10782 Table 2), which is about 2 sigma per bin on the SM running.

**8. Experimental manifestation.**
- Unfolded A_i in (m_ll, pT_ll) cells above 170 GeV, using ee and mumu with standard single-lepton triggers.
- A triple-differential fit in (m, |y|, cos theta) for sin2theta_W(mu).

**9. Main obstacles.**
- A0 is already systematics-limited in Run 2 (2202.12327 Table 3).
- A5-A7 cannot be measured at SM level above the peak, only bounded.
- The pT_ll spectrum is the stronger dipole probe (2412.13014).
- EFT validity of the dim-8 projections is unclear.
- The running is PDF-limited and degenerate with contact interactions (1609.08157).

**10. Novelty confidence.** Medium that no such measurement exists. This is a novel measurement, i.e. a novel experimental analysis, with **marginal BSM leverage**.

**11. Recommended next step.** A Run-2 feasibility study with public HEPData and open data. Estimate statistics and systematic floors for A5-A7 and l=3 in high-mass bins before going to HL projections. Separately, ask whether a sin2theta_W(mu) extraction from 2202.12327-type data is worth a pheno paper.

**12. References.** 1609.08157; 2003.11615; 1708.00008; 2405.04069; 2412.13014; 2511.19617; 2512.05018; 2302.10782; 2307.10737; 1606.00689; 2604.25678; 2203.01602; 2202.12327; 2408.07622; 1710.05167; 1902.04070.

## 7. C003: Displaced, hadronic, isotropic SUEP (Tier B, confidence Low)

**1. Summary.** Strongly coupled hidden sectors produce soft, spherical, high-multiplicity final states (SUEP). Every existing search assumes prompt decays and builds multiplicity from primary-vertex tracks.
- **Target:** SUEP whose dark mesons decay hadronically after ~1 mm to a few cm, seen as an isotropic spray of soft displaced tracks and vertices.
- **Also wanted:** a collaboration HL projection of prompt SUEP.

**2. Why it matters.** For gluon and Higgs decay portals, displaced dark hadrons are the generic expectation (2107.12379 Sec. 2.3; 2103.01238). The original soft-bomb paper explicitly deferred displaced decays (1612.00850 Sec. II.D).

**3. Foundational literature.** 1612.00850; 2107.12379; 2203.09503; 2103.01238; 2211.05720 and 2203.07314 (track triggers).

**4. Current state of the field.**
- Prompt SUEP is well covered: CMS ggF 2403.05311, CMS scouting 2607.09621, CMS VH 2604.05996, ATLAS muon-rich 2605.20015.
- CMS states that a displaced SUEP "would result in an emerging jet signature" (2403.05311).

**5. Existing experimental coverage.**
- Muonic displaced dark showers: CMS 2511.11888.
- Emerging-jet searches (2403.01556, 2510.12347, 2505.02429) need energetic jets.
- MDS searches cover metre-scale decays (2402.01898; recast 2505.03058).
- No HL-LHC SUEP projection exists. 1812.07831 has none.

**6. Remaining gap.** Isotropic, soft, hadronic displaced spray with c*tau ~1 mm to a few cm. Status: constrained-but-region-open; LHC-not-projected-to-HL. The theory reviewer finds the natural region squeezed:
- m_D ~1-3 GeV gives c*tau >~ m (beyond the tracker).
- m_D ~5-10 GeV at cm lifetimes gives only ~10-25 mesons, which overlaps C005.

**7. HL-LHC opportunity.** Phase-2 L1 tracking and scouting could help the prompt programme. For the displaced case any HL-specific gain (MTD re-association, large-d0 HLT tracking) is speculative.

**8. Experimental manifestation.** VH(lepton) events with many low-mass multi-track displaced vertices distributed isotropically, failing emerging-jet jet requirements. Result: limits on (m_D, T_D, c*tau).

**9. Main obstacles.**
- Displacement removes primary-vertex association, which is the only demonstrated SUEP-vs-pileup discriminant.
- Soft tracks fall below the 2 GeV L1 threshold, giving "negligible efficiency" (2211.05720 Sec. 2.2).
- There is no first-principles generator.
- Theory tensions: the Higgs tadpole (1612.00850 Sec. II.C), and the likely beam-dump exclusion of the long-lived A' route (2005.01515; overlap UNVERIFIED).

**10. Novelty confidence.** Medium that no search exists. Low that it is feasible as a standalone analysis.

**11. Recommended next step.** Fold it into the C005 study as an isotropic, high-multiplicity variant of the VH multi-DV selection, rather than pursuing it standalone. For the prompt part, a Phase-2 L1-track/scouting projection is a well-defined, smaller task.

**12. References.** 1612.00850; 2107.12379; 2203.09503; 2103.01238; 2211.05720; 2203.07314; 2403.05311; 2607.09621; 2604.05996; 2605.20015; 2511.11888; 2403.01556; 2510.12347; 2505.02429; 2402.01898; 2505.03058; 2005.01515; 1812.07831.

## 8. C008: Photon-enriched semi-visible jets; photon-ISR low-mass SVJ (Tier C, confidence Medium)

**1. Summary.** Two variants of semi-visible jets (SVJs) from an s-channel Z'.
- **(i) Photon-enriched SVJs.** Dark pions decay to photons through an extra ALP portal. The resulting jets have a high neutral-EM fraction and contain non-isolated photons, so they fail standard jet ID (2407.08276).
- **(ii) Low-mass Z' -> SVJ SVJ tagged with an ISR photon** (2409.04741).

**2. Why it matters.**
- Confining dark sectors are generic. SVJs give MET aligned with a jet (1503.00009).
- Variant (i) sits exactly where the current selections are blind: CMS SVJ searches veto jets with photon fraction f_gamma > 0.7.

**3. Foundational literature.**
- Seminal SVJ papers: 1503.00009 and 1712.07160.
- Dark-matter viability: 1809.10152.
- Photon-enriched SVJ proposal: 2407.08276.
- ISR-tagged SVJ proposal: 2409.04741.
- Lund-plane modelling: 2301.07732.

**4. Current state of the field.** CMS and ATLAS run a broad SVJ programme:
- CMS resonant: 2112.11125.
- CMS lepton- and tau-enriched: 2608.05323, plus INSPIRE:3136606.
- ATLAS resonant plus anomaly detection: 2505.01634.
- ATLAS t-channel: 2305.18037.
- CMS non-resonant: INSPIRE:3185627.
- A CMS thesis (INSPIRE:2751239) develops a jet-ISR boosted SVJ search.

**5. Existing experimental coverage.**
- Lepton- and tau-enriched and t-channel SVJs are covered.
- No SVJ search reaches below about 1.5-2 TeV.
- ATLAS 2403.08547 covers visible Z' -> qq + photon/jet for 200-650 GeV, with g_q < 0.06-0.1.

**6. Remaining gap.**
- **(i) SVJ-gamma:** proposed-not-searched.
- **(ii) photon-ISR:** the published benchmark (g_q = 0.25) is excluded by its visible decays. Only the corner with B(Z' -> chi chi) -> 1 and small g_q survives, at reduced rate.

**7. HL-LHC opportunity.** Weak. Variant (i) can already be tested with Run 2/3 data; the pheno paper claims Run-2 reach up to 5 TeV. The HL-LHC adds reach in g_q x BR_gamma, roughly as sqrt(L). Variant (ii) is limited by systematics.

**8. Experimental manifestation.** An m_T bump hunt using DNN-tagged high-NEMF jets with MET aligned to the jet. A further handle, from the theory reviewer's own inference: the in-jet diphoton mass peaks at m_pi.

**9. Main obstacles.**
- **Ad hoc second portal.** The ALP plus vector-like lepton portal has no independent motivation for BR_gamma.
- **Instrumental fakes.** Dropping the NEMF jet-ID cut lets them back in.
- **No calibration** exists for photon-rich jets.
- **No pileup** is simulated in the phenomenology studies.
- **Likely CMS pre-emption.** The same authors' lepton and tau proposals became CMS searches.

**10. Novelty confidence.** Medium for (i), framed as a Run-3 experimental analysis. Low for (ii).

**11. Recommended next step.** If pursued, treat (i) as a Run-3 analysis with an HL extrapolation. First check the CMS SVJ group's plans and the content of the ETH thesis INSPIRE:3131301 (UNVERIFIED). Drop (ii) unless a viable B(chi chi) ~ 1 benchmark is constructed.

**12. References.** 1503.00009; 1712.07160; 1809.10152; 2407.08276; 2409.04741; 2604.20456; 2301.07732; 2112.11125; 2608.05323; 2505.01634; 2305.18037; 2403.08547; 1905.10331; 2405.13778; 2502.11237; INSPIRE:3136606; INSPIRE:3185627; INSPIRE:2751239; INSPIRE:3131301.

## 9. C040: Compressed direct stau pairs, collaboration HL-LHC projection (Tier C, confidence Medium)

**1. Summary.** The proposal is a collaboration-level Phase-2 projection, and later an analysis, of direct stau-pair production.
- **Target region:** small mass splittings to a bino LSP (the coannihilation corridor).
- **Signature:** soft tau_h plus ISR or VBF recoil plus MET.

**2. Why it matters.** Bino dark matter with stau coannihilation is predictive, and direct detection struggles to probe it. Part of this region sits below the neutrino floor (2308.05723), so colliders are the main probe. The g-2 motivation has gone (2505.21476).

**3. Foundational literature.**
- Soft-tau + ISR strategy: 1606.08878.
- Phenomenology of the corridor: 1704.04669, 2308.05723, 2403.18991.
- Review: 2601.06358.

**4. Current state of the field.** ATLAS 2609.37215 (Run 2 + Run 3, 193 fb-1 total) runs exactly this strategy.
- The ISR channel alone excludes m(stau) up to 115 GeV at Delta m = 30 GeV.
- The combination sets no exclusion, with 2.1-2.4 sigma local deviations.
- A CMS review (2510.17971) says compressed-stau analyses are in preparation.

**5. Existing experimental coverage.**
- CMS soft tau_h + ISR: 1910.01185.
- CMS and ATLAS large-Delta m stau searches: 2207.02254, 2402.00603, 1911.06660.
- Long-lived stau for Delta m < m_tau: 2601.17576.
- HL-LHC projections exist only for Delta m > 100 GeV (1812.07831 Sec. 2.3; INSPIRE:1704284).

**6. Remaining gap.** The collaboration HL projection only; status LHC-not-projected-to-HL (cap applied). The motivated and reachable window is small:
- The relic-motivated window is Delta m <~ 30 GeV (theory review).
- There is little sensitivity below Delta m ~ 15 GeV (feasibility review).
- That leaves roughly 15-30 GeV, with m(stau) ~ 100-200 GeV.

**7. HL-LHC opportunity.** Current sensitivity is statistics-limited, so roughly 15x more data gives about a sqrt(15) gain. That moves the exclusion at Delta m = 30 GeV from ~115 GeV to ~150-200 GeV (estimate).

**8. Experimental manifestation.** A hard ISR jet, MET > 200 GeV, and one or two tau_h with pT of 15-40 GeV. The result would be an exclusion contour in the (m(stau), Delta m) plane.

**9. Main obstacles.**
- The jet -> tau_h fake rate, and its systematic uncertainty, for soft taus at pileup 200.
- The small cross section after the ISR requirement.
- Phase-2 L1 thresholds for MET and taus are unverified.
- ATLAS and CMS are already pursuing this.

**10. Novelty confidence.** Low. The novelty would be a projection only.

**11. Recommended next step.** Treat this as a low-cost projection exercise: scale ATLAS 2609.37215 to 3 ab-1 with Phase-2 tau performance. Pursue it only if the ATLAS excesses persist in full Run 3.

**12. References.** 1606.08878; 1704.04669; 2308.05723; 2403.18991; 2601.06358; 2609.37215; 2510.17971; 1910.01185; 2207.02254; 2402.00603; 1911.06660; 2601.17576; 1812.07831; 2505.21476; INSPIRE:1704284; INSPIRE:2751742.

## 10. C066: Resonant lepton-PDF single leptoquark with charm-tagged jets (Tier C, confidence Medium)

**1. Summary.** QED radiation gives the proton a lepton content (lepton PDFs). This makes resonant l q -> LQ production possible. The proposal adds an e/mu + c-tagged jet category and a collaboration HL-LHC projection.

**2. Why it matters.**
- The lepton PDFs are known to better than 5% (2005.06477), so the mechanism is robust.
- A c-tag would be the only resonance-level handle on the quark flavour of the coupling.
- The motivation is weak (2/5). No anomaly points to e/mu-c couplings, and the g-2 case has faded (2608.28377).

**3. Foundational literature.**
- Lepton PDFs: 2005.06477.
- Resonant lepton-quark production: 2005.06475.
- NLO cross sections: 2012.02092.
- Third-generation resonant signatures: 2012.11474.
- Vector-LQ high-pT signatures: 1901.10480.

**4. Current state of the field.**
- ATLAS 2507.03650: e/mu + light and b jets, Run 2 + Run 3.
- CMS 2608.28377: mu only, u and b benchmarks.
- CMS 2308.06143: tau-quark channel.
- The third-generation bundle is dead. ATLAS 2503.19836 excludes the CMS excess benchmark; the beta_R benchmark is in CMS 2208.02717; and CMS 2308.07826 already combines single, pair and non-resonant production.

**5. Existing experimental coverage.** Both collaborations already cover the charm case indirectly:
- ATLAS says u and c couplings are "kinematically indistinguishable" and can be reinterpreted by flavour rotation (2507.03650 Sec. 1).
- CMS says s and c couplings are "bracketed" by its benchmarks (2608.28377 Sec. 1).
- The review 2505.08738, which listed charm as an open opportunity, predates both searches.

**6. Remaining gap.** Status: one-observable-not-another / indirectly-covered (cap applied).
- The gap is a reinterpretation for lambda_cl plus a collaboration HL projection.
- The often-quoted "5.7 (4.2) TeV" from 2005.06475 is **not** a mass reach. It is the mass up to which the HL resonant bound beats the Q_W bound for lambda_eu (lambda_ed).

**7. HL-LHC opportunity.** The search is statistics-limited and near background-free at high mass. ITk/GN2 flavour tagging (INSPIRE:3130572) might make a TeV-scale c-tag usable. Because the rate scales as y^2, the coupling reach improves only as L^(-1/4) to L^(-1/2) (estimate).

**8. Experimental manifestation.** An m(l j) bump with low MET, a jet veto, and a forward soft lepton. The proposal adds a c-tagged category.

**9. Main obstacles.**
- **Rate.** The c-mu rate is about 28x below u-mu at 2.5 TeV (2012.02092 Table 1).
- **Width.** Matching the u-channel reach needs y_c ~ 3, which gives a broad resonance (Gamma/M ~ 0.24).
- **Tagging.** TeV-pT c-tagging has low efficiency (about 30% working point, 2211.16345) and poorly known calibration.

**10. Novelty confidence.** Low.

**11. Recommended next step.** A theory-level flavour-rotation reinterpretation of the published ATLAS and CMS light-jet limits for lambda_cl. Argue for a c-tag category only if a pheno study shows a meaningful S/B gain.

**12. References.** 2005.06475; 2005.06477; 2012.02092; 2012.11474; 1901.10480; 2507.03650; 2608.28377; 2308.06143; 2308.07826; 2503.19836; 2208.02717; 2606.02067; 2505.08738; 2211.16345; INSPIRE:3130572; 1812.07831.
