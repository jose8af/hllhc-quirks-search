# C001 quirks: literature census, lineage and open problems

> **Correction (2026-10-07, after this census):** two statements below are outdated. (1) An ATLAS quirk-search effort *does* exist (github `burzynski-lab/quirk-tracking`; Athena `Simulation/G4Extensions/Quirks` fixes merged 2026-08-27 and 2026-09-01), see `research/samples_and_tools.md` and `research/experimental_status_2026.md`. (2) Public quirk code *does* exist: the Athena Geant4 quirk transport (Apache-2.0). The FASER HEPData tables were later read successfully (record ins3184325).

Built 2026-10-07 from INSPIRE (cached queries, see Appendix), PDF text of 40+ papers (research/cache/pdf), and web searches. Companion data: `bibliography.json` (58 entries). Citation counts are INSPIRE values on 2026-10-07. Statements marked (C001 review) are taken from `research/reviews/experimental/C001.md` and were not re-verified here. "Not found" always means "not found with the queries in the Appendix".

## 1. Summary counts

- INSPIRE candidate pool after all queries: about 590 unique records, of which most are noise (quantum-computing "Quirk", magnetohydrodynamics "non-helical", string theory "macroscopic string", generic hidden-valley). Title search `t quirk*` returns 28 records; after removing non-physics (quantum teleportation etc.) 24 are quirk-physics.
- Bibliography.json: 58 entries = **about 33 quirk-core papers** (papers whose main subject is quirks / squirkonium / quirk reconstruction / quirk cosmology) plus 25 peripheral (reviews, white papers, glueball/neutral-naturalness context, theses).
- By type (core): theory/model 11, pheno-projection 14, recast 2, experimental search 2 (D0 1008.3547, FASER 2607.26195), tools-reconstruction 3 (2410.00269, 2509.08878, 2002.07503), cosmology/DM 5.
- By regime (collider-signature papers): macroscopic/mesoscopic coplanar-track or forward-timing work: 1708.02243, 1911.02223, 2002.07503, 2108.06748, 2311.15486, 2404.13814, 2410.00269, 2509.08878, 2601.09023, 2607.26195 (10). Microscopic quirkonium/glueball work: 0805.4667, 1106.2569, 1106.3101, 1512.05753, 1512.05782, 2310.02317, 2504.02940, 2506.11192 (8). Unresolved/high-dE/dx: 1008.3547.
- Experiments studied: FASER/FASER2 (5 papers), other far detectors MATHUSLA/ANUBIS/SND@LHC/FACET (2311.15486), FPF@FCC (2409.02163), LHCb VELO (2601.09023), ATLAS/CMS tracker (1708.02243, 1911.02223, 2410.00269 generic), CMS stopped/OoT (1811.08903), CMS/ATLAS HSCP+monojet recast (1703.00912), D0 (1008.3547). **No ATLAS or CMS collaboration quirk search, note, PAS, CONF or PUB was found.** MoEDAL appears only as a physics-programme/review mention (1405.7662; 2814966), no quirk search.
- Pile-up: no quirk paper simulates HL-LHC pile-up (200). 1708.02243 uses <mu>=50; 1911.02223 overlays pile-up on Z(vv)+jets (level UNVERIFIED); 2410.00269 and 2509.08878 explicitly defer pile-up (the latter uses mu=1); 2506.11192 adds none; 2601.09023 uses "LHCb running conditions".
- Forward citations (INSPIRE): 0805.4642: 226; 1106.2569: 55; 1708.02243: 37; 1703.00912: 27; 1811.08903: 29; 1911.02223: 13; 2404.13814: 17; 2410.00269: 8; 2607.26195: 1; 2601.09023: 3; 1008.3547: 24; 2108.06748: 17; 2311.15486: 9; 2002.07503: 14; 2509.08878: 4.

## 2. Lineage (chronological, who built on whom)

```
2007  Jacoby-Nussinov 0712.2681 (relic abundance, "Quirk Model" of Luty)
2008  Kang-Luty 0805.4642  [founding: macroscopic strings, regimes by Lambda]
        |- Burdman-Chacko 0805.4667 (folded SUSY squirkonium)
        |- Cai-Cheng-Terning 0812.0843 (quirky little Higgs)
2009  Nussinov-Jacoby 0907.4932; Kribs-Roy 0909.2034 (quirky DM)
2010  D0 1008.3547 (only pre-LHC search; unresolved regime)  ; Martin 1012.2072; Zurek TASI 1001.2563
2011  Harnik-Kribs-Martin 1106.2569 (Tevatron+LHC, squirkonium); Fok-Kribs 1106.3101
2015-16  Diphoton era: 1512.05753, 1512.05775 ; Chacko-Curtin 1512.05782 (quirky neutral naturalness)
2017  Farina-Low 1703.00912 (recast HSCP/monojet, 0T idea)   --\
      Knapen-Lou-Papucci-Setford 1708.02243 (coplanar tracker)  --+--> basis of all later central-detector work
2018  Evans-Luty 1811.08903 (stopped quirks, CMS OoT recast)
2019-20  Li-Li 1911.02223 (+ionisation energy loss to coplanar search); 2002.07503 (analytic EOM)
2021  Li-Pei 2108.06748 (FASER/FASER2 propagation)  -> FPF white paper 2203.05090
2023  Li-Liao 2311.15486 (FASER2, MATHUSLA, ANUBIS, SND, FACET)
2024  Feng-Li 2404.13814 (timing at FASER) ; Sha et al. 2410.00269 (GNN reconstruction) ; FPF@FCC 2409.02163
2025  Condren-Whiteson 2509.08878 (model-agnostic non-helical tracks) ; Forsyth-Low 2504.02940 ;
      Curtin-Dreyer 2506.11192 ; Asadi-Kribs 2512.20696 (cosmology: T_RH<~100 GeV)
2026  Cid Vidal-Fernandez Gomez 2601.09023 (LHCb VELO) ; FASER 2607.26195 (first LHC search, 0 events)
```
Authors' groups: the propagation/EOM + far-detector line is Jinmian Li (+ Tianjun Li, Pei, Liao, Feng). The tracker-reconstruction line is Knapen/Papucci/Setford -> Whiteson group (2410.00269, 2509.08878). The macroscopic-string foundation is Kang-Luty; the cosmology line is Kribs/Asadi.

## 3. Open-problem statements and follow-up status

| Paper | Explicit future-work / open statement (PDF text) | Follow-up? |
|---|---|---|
| 0805.4642 | Annihilation-position distribution: "More realistic simulations should be done to check"; angular decoherence "beyond the scope" | Partly: 1811.08903 (stopping simulation), 1911.02223, 2002.07503 (EOM). No full MC of angular decoherence/glueball emission found. |
| 1106.2569 | Kinematic features when energy loss is rapid: "choice investigation ... for future work"; no full simulation | Not found with queries on citers of 1106.2569 (55, reviewed by title). |
| 1703.00912 | "interesting to see limits for a larger variety of quantum numbers"; "if possible to trigger on such anomalous tracks"; CMS 0T data proposal | Larger quantum numbers: yes in FASER papers 2108.06748 etc. 0T-data search: not found (no CMS/ATLAS item among 27 citers). |
| 1708.02243 | Dedicated trigger and extension "We leave this possibility for future work"; MET trigger only (eps_trig ~0.1 for DY at 800 GeV, Tab. I per C001 review) | Partial: 1911.02223 adds ionisation. HL-LHC (PU 200) version, HLT/L1 track trigger version: not found with queries (citers of 1708.02243 and `abstracts.value:quirk* and pile-up`). |
| 1811.08903 | Dedicated search or complementary OoT channel needed to identify quirks vs DM in monojet; extension to full calorimeter / HGCAL | Not found; ATLAS stopped-particle search 2104.03050 has no quirk interpretation (C001 review). |
| 1911.02223 | Coloured quirk simplification; "We leave this for future work" | Not found. |
| 2108.06748 / 2311.15486 | "Designing specific cuts to separate quirk tracks from muon tracks requires detailed simulation ... beyond the scope" | Partly: 2404.13814 timing analysis; 2607.26195 (data analysis with Geant4). |
| 2404.13814 | "Detailed experimental analysis of backgrounds ... beyond the scope" | Done by FASER 2607.26195 (zero events). |
| 2410.00269 | Broader "all-quirks" reconstruction and generalisation to other parameter sets; "Effects from pile-up remain to be studied rigorously in future work" | 2509.08878 addresses model-agnostic tracking (mu=1 only). Pile-up/ATLAS-CMS simulation study: not found with queries (citers of 2410.00269, 8 total, all reviewed). |
| 2509.08878 | Future work: hit noise, misalignment, hard radiation, shorter tracks, piecing several track segments | Not found (4 citers, none do this). |
| 2504.02940 | Hidden-sector glueball hadronisation "beyond the scope" | Not found. |
| 2506.11192 | Improved normalising flow, precise decay widths with glueball mass; no pile-up | Not found. |
| 2512.20696 | Bounds for larger Lambda "leave for future work" | Not found. |
| 2601.09023 | States quirks "lack feasible, dedicated searches" | No LHCb collaboration search found. |
| 2607.26195 | Statement that no dedicated LHC search existed before; only charge +-1 colourless pairs | ATLAS/CMS follow-up not found. |

## 4. Code and data releases

- FASER search 2607.26195: HEPData record 181308, DOI 10.17182/hepdata.181308.v1 (from web search snippet; the HEPData page returned HTTP 403 so contents were not read). The quirk Geant4 adaptation is described in the paper as "adaptation of the quirks physics", release status: not found.
- UFO/FeynRules quirk models: used in 1911.02223, 2002.07503, 2108.06748, 2311.15486, 2404.13814 (PDF text) but no public URL was found in any PDF or by web search ("quirk simulation code github ..." returned none).
- GNN tracking for quirks (2410.00269) is built on Exa.TrkX (public framework, hep-ml); the quirk-specific pipeline/code: not found with the web queries "Learning to reconstruct quirky tracks GNN code github Zenodo". Related public GNN tracking projects (not quirk-specific): github.com/gnn-tracking/gnn_tracking, github.com/HEPTrkX/heptrkx-gnn-tracking, GNN4ITk.
- LHCb 2601.09023: standalone VELO hit generator described; no URL found.
- Jinmian Li talk slides (FaserBSM, indico.ihep.ac.cn event 28216) describe interactive propagation code; code URL not confirmed (slide text only seen via search snippet).
- Conclusion: **no public quirk-propagation or quirk-generation code was found**; an analyst must reimplement the EOM (Kang-Luty / Knapen Eq. 2; analytic form in 2002.07503).

## 5. The 10 must-read papers (ordered)

1. 1708.02243 Knapen et al. - the coplanar-hit tracker search that is the target; trigger and background arguments, PU 50.
2. 2410.00269 Sha et al. - GNN reconstruction of quirk tracks, the only reconstruction study; pile-up explicitly open.
3. 2607.26195 FASER - first and only LHC quirk search; sets the exclusion (179 GeV at 10 keV, Fig.4/5) to be exceeded.
4. 0805.4642 Kang-Luty - physics foundation (regimes, EOM, no in-flight annihilation, decoherence).
5. 1703.00912 Farina-Low - what existing HSCP/monojet searches exclude; keV gap and 0T proposal.
6. 1911.02223 Li-Li - ionisation-energy-loss improvement of the coplanar search; most complete tracker-level sim of ATLAS/CMS-type setups.
7. 2002.07503 Li-Li - analytic quirk trajectory for fast signal generation and plane thickness.
8. 2509.08878 Condren-Whiteson - model-agnostic non-helical tracking; current ML state of the art and its listed limitations.
9. 2601.09023 Cid Vidal-Fernandez Gomez - LHCb alternative; shows planar-pattern analysis in a software trigger (relevant for HLT design).
10. 1811.08903 Evans-Luty - stopped quirks and out-of-time search; the complementary CMS/ATLAS channel and detector-simulation details of energy loss.
Next after these: 2404.13814 and 2108.06748 (propagation through magnets/materials), 2512.20696 (cosmology implications), 2504.02940 (neutral-naturalness motivated reach), 2203.05531 (neutral-naturalness review).

## 6. Surprises / flags

- No ATLAS/CMS quirk activity of any kind was found (INSPIRE abstract queries with ATLAS/CMS/trigger/high-luminosity, web search for PAS/CONF/indico). The 2606.30760 review and the 2512.20696 paper both say the single dedicated collider search is now FASER (plus D0). Absence in abstracts does not exclude internal studies.
- Two ATLAS theses (1760811 Adersberger; 1755360 Carney) cite 1708.02243 but contain no quirk search (abstracts).
- No HL-LHC (PU 200) quirk study exists. This is the gap the target addresses.
- FPF@FCC (2409.02163) quotes quirk reach to 10 TeV at 100 TeV: unrelated regime but shows timing-based follow-ups scale.
- INSPIRE record for FASER search 2607.26195 lists Phys.Rev.Lett. without volume (accepted/ in press at time of query).

## Appendix: queries run (INSPIRE via research/tools/inspire.py, size 100, sort mostrecent; counts in parentheses)

Title: `t quirk`(9) `t quirks`(16) `t quirky`(9) `t quirkonium`(1) `t quirk*`(28) `t squirk(s)`(0) `t infracolor`/`infracolour`(0) `t "macroscopic string"`(5) `t "hidden valley"`(26) `t "folded supersymmetry"`(5) `t "twin Higgs" and abstracts.value:quirk`(0) `t "detector-stable"` `t "nonhelical tracks"` `t "Tevatron" and abstracts.value:quirk*`.
Abstract: `abstracts.value:` quirk(47) quirks(38) quirk*; quirky; quirkonium(5); squirks(2); squirk(1); infracolor(6); "infracolour"(0); "folded supersymmetry"(15); "folded SUSY"(5); "quirky little Higgs"(3); "non-helical"(100, noise: magnetic fields); "non-helical tracks"(2); "anomalous track"(0); "coplanar" and track(4); "flux tube" and heavy and LHC(4); "stable heavy charged" and string(0); "hidden valley" and heavy and string(1); "mesoscopic" and string and collider(0); "quirky dark matter"(2); quirk and "dark matter"(4); quirk and cosmolog*(3); "Kang-Luty"(0); quirk and each of FASER(2) LHCb(1) MoEDAL(0) MATHUSLA(1) CODEX(0) ANUBIS(1) "forward physics facility"(1) Higgs(4) "neutral naturalness"(2) ionization(6) track(1) lattice(0) neutrino(0) glueball(1) trigger(2) "graph neural"(0) baryogenesis(3) detector(7) gravitational(0) astrophysic*(0) "cosmic ray"(0) "lepton collider"(0) "100 TeV"(0) "muon collider"(0) ATLAS CMS MoEDAL "high-luminosity" milli* displaced "hadron collider" monojet Lambda "W mass" "muon g-2" diphoton "750" mirror twin; "vector-like confinement"(with LHC, string); "string breaking" and collider; "strings attached" and LHC; "highly ionizing" and string; "stable heavy" and confining and hidden; "unresolved" and string and "high ionization"; "charged detector-stable particles"; "squirk*"; plus long-lived/tracking/ML variants of non-helical queries; "hypercolor" and string and LHC; "pair of heavy" and string and confin* and track*.
Author-based: `a Kang, J and a Luty`, Harnik+string, Kribs+quirk*, Burdman+folded, Knapen+track, Farina+quirk*, Evans+quirk*, Chacko+folded, Cheung+quirk*, Li Yiming+quirk*, Feng+quirk*.
Citations (`refersto:recid:<recid>`, all pages): 0805.4642(226) 1106.2569(55) 1708.02243(37) 1703.00912(27) 1811.08903(29) 1911.02223(13) 2404.13814(17) 2410.00269(8) 2607.26195(1) 2601.09023(3) 1008.3547(24) 2108.06748(17) 2311.15486(9) 2002.07503(14) 2509.08878(4) 2504.02940(8) 2506.11192(10) 2512.20696(4) 0805.4667(67) 1512.05782(75).
Backward references of the newest papers: not run through `inspire.py refs` (reference lists were read via PDF text/full-text grep and the citer lists above); this is a limitation.
PDF full-text scans (quirk mention counts, code/simulation keywords, future-work sentences via `arxiv_pdf.py --gaps`): 17 key papers + 23 reviews/white papers.
Web searches: "quirk simulation code github ..."; "ATLAS CMS quirks search talk indico non-helical"; "Learning to reconstruct quirky tracks GNN code github Zenodo; FASER quirk search HEPData"; "CMS OR ATLAS collaboration search for quirks 2026 ..."; "MoEDAL MAPP quirks ...; quirks ATLAS Phase-2 ITk trigger talk". Not run: CMS/ATLAS public-results page scrapes, CERN indico direct search, GitHub API search (WebFetch to HEPData got 403).
