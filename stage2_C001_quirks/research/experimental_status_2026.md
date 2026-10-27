# C001 Quirks: experimental status, competition, reference analyses, HL-LHC trigger/detector plan (Stage 2, as of 2026-10-07)

Author: Stage-2 skeptical-experimentalist agent. Extends (does not repeat) research/reviews/experimental/C001.md, research/reviews/feasibility/C001.md, research/reviews/adversarial/gate3_batchA.md (C001).
Status: COMPLETE (round 1, 2026-10-07). CMS-first per user instruction (user is a CMS member).

## 1. Competition and novelty update (as of 2026-10-07)

**Scope note (user is a CMS member).** The target is a CMS Phase-2 analysis. ATLAS items are treated as competition only.

### 1.0 KEY NEW FINDING: an active ATLAS quirk search (public code trail, Aug-Sep 2026)
Evidence was supplied by the samples agent and the orchestrator, then re-checked here with `gh api` and the CERN GitLab API on 2026-10-07.

1. **github.com/burzynski-lab/quirk-tracking** (public; created 2026-09-09, last push 2026-09-15; 27 commits by J. C. Burzynski, U. Oklahoma group site jacksonburzynski.web.cern.ch).
   - README: "MaskFormer-based quirk-pair finding for **the ATLAS quirk search** ... Input is the `Dump_GNN4Itk.root` ntuples from the quirk reconstruction chain". Runs on the OU OSCER cluster (`/ourdisk/hpc/ouhep/...`).
   - PLAN.md: goal is to "replace the invented flat **eps_find = 0.5**" used "**in the contour**". So an internal (mQ, Lambda) sensitivity contour **already exists**.
   - Training data: an "m=100 dumps for all 10 Lambda points (~390 GB) ... ~90k events" grid and a "grid_v3" with 11 masses (one slurm task per mass).
   - Events have "~2-3k space points" (README: 150-6k hits), so **no or low pile-up so far**.
   - Planned outputs: per-(m, Lambda) pair-finding efficiency, regression of log10(Lambda²/m), the pair-plane normal, and pixel cluster charge (ToT) as a dE/dx handle. It notes that "strip SPs have no charge" (binary strips).
2. **github.com/burzynski-lab/quirkviz** (created 2026-08-25): "Event displays for **ATLAS quirk simulation**". It reads Athena HITS files, defaults to mQ = 500 GeV, Lambda = 400 eV, has an optional **TRT** hit dump, and draws to r ≤ 1100 mm, z ≤ 3000 mm.
3. **Athena** `Simulation/G4Extensions/Quirks`. The package has existed since at least 2019 in the git history and corresponds to the SLAC-era Geant4 quirk implementation (SLAC Confluence "Project Description - A Search for Quirks at the LHC", page 94178588; search snippet only).
   - MR "Fix quirk simulation" (J. C. Burzynski, merged 2026-08-25, **target branch 24.0**, "validated on a few private samples", cc @lcorpe @mvessell).
   - MR "More fixes for G4 quirks (killed quirk partner handling)" (M. Vessella, merged 2026-08-31, **target 24.0**, cc @jburzyns @lcorpe).
   - Both were swept into main on 2026-08-27 and 2026-09-02 (GitLab API, merge_requests search "quirk").
4. **Run-2/3 ID or ITk?** Assessment: **most likely a Run-2 + Run-3 Inner Detector search (pixel + SCT)**, with ITk tooling reused. Confidence medium.
   - For Run 2/3:
     - the G4 fixes target **24.0**, the Run-3 production release branch (main receives them by sweep);
     - quirkviz handles **TRT** hits, which exist only in the Run-2/3 ID;
     - the default display volume (r ≤ 1.1 m) matches the ID/TRT envelope.
   - Not decisive: the "GNN4ITk" dumper `InnerDetector/InDetGNNTracking/src/DumpObjects.cxx` (Athena main) **first retrieves the Run-3 `PixelID`/`SCT_ID` managers and falls back to `ITkPixel`/`ITkStrip`**, so the name does not imply ITk. The tree is titled "Athena Dump for GNN4ITk".
   - Pointing the other way: quirkviz suggests `asetup Athena,25.0.70` ("or any recent Athena release"); the purpose of the 25.0 branch was not verified. An HL-LHC/ITk projection is therefore not excluded.
5. **People.** J. C. Burzynski (ATLAS; 2021 ATLAS thesis award for exotic-Higgs/LLP work; now leads an Oklahoma group). M. Vessella (ATLAS; author lists). "lcorpe" = L. Corpe (ATLAS; LLP reinterpretation/CONTUR, ANUBIS, HGTD papers).
   - **No talk, note, thesis or arXiv paper on this effort was found.** Queries: INSPIRE `a Burzynski, Jackson and date > 2023`, `a Burzynski, Jackson and not collaboration:ATLAS`, `a Vessella`, `a Corpe, Louie and date > 2024 and not collaboration:ATLAS`. Web: "Burzynski quirks ATLAS search Oklahoma Corpe Vessella", "quirk ATLAS Geant4 simulation inner detector search 2026 indico talk". The effort is pre-publication and probably at the analysis-design stage, with signal MC and the reconstruction chain being built in Aug-Sep 2026.
6. **Implication.** The SLAC-page hint (Gate-4 caveat 2) is now confirmed as a **live ATLAS analysis**: full Geant4 quirk simulation, ML non-helical reconstruction, and a sensitivity contour.
   - **ESTIMATE** for a Run-2+3 ATLAS result (typical LLP-analysis cadence after signal-MC validation): 2028-2029, with ~140 (Run 2) to ~400 fb-1 (Run 2+3).
   - Expected reach: the Knapen-type 300 fb-1 sensitivity, i.e. EW quirks up to ~500-650 GeV for Lambda ~ 0.1-5 keV [1708.02243 abstract; 1911.02223 App. A: ~500 GeV without the Zjj background]. This is an ESTIMATE that ignores ATLAS-specific efficiencies.
   - That is **squarely the C001 target region**.

### 1.1 Other updates since the Gate-4 reviews
Gate-4 reviews: experimental/C001.md, feasibility/C001.md, adversarial gate3_batchA.md.

1. **No *public* ATLAS, CMS or LHCb collaboration output (paper, CONF/PAS, talk) on quirks or non-helical tracks was found.** The ATLAS activity in Sec. 1.0 is visible only through code repositories.
   - INSPIRE fulltext search: `fulltext:"quirks" and collaboration:CMS` returns only 2405.13778 (dark-sector review), 2106.10509 (hadronic Wgamma resonance) and 1210.2311 (fractional charge). All three cite quirks as model context only.
   - The same search for ATLAS returns only 2104.03050, 1309.3230 and 1112.3580, all already known. LHCb returns nothing.
   - Abstract searches return nothing for collaboration papers or theses: `abstracts.value:"quirk" and (collaboration:ATLAS or ...MoEDAL)` gives 0 hits; `abstracts.value:"quirk(s)" and tc t` gives 2 old generic BSM theses.
   - Theses that cite 1708.02243 do so as context only (INSPIRE citers, abstracts read; full text not read): Carney 2019 (INSPIRE 1755360, ATLAS DV+jets/tracking) and Adersberger 2018 (1760811, ATLAS HCLLP). The LHCb thesis Uecker 2026 (3193023, GPU track fit, HLT1) cites 2601.09023.
   - CDS could not be queried: an "Anubis" bot challenge blocked scripted access on 2026-10-07. Internal CMS/ATLAS notes therefore remain **UNVERIFIED**.
2. **The SLAC ATLAS Confluence "Quirks" page** (confluence.slac.stanford.edu/spaces/Atlas/pages/100501546/Quirks) is still not readable: WebFetch returned an empty body. The web-search snippet shows a strategy focus on *mesoscopic* quirks, an ISR photon or jet recoil requirement, out-of-time hits in the outer layers, and Pixel+SCT+TRT reconstruction. **Interpretation:** this was the origin of the Athena G4 quirk package. The effort has been **revived in 2026** (Sec. 1.0).
3. **LLP community meetings.**
   - LLP2025 (Valencia, 2-6 June 2025, indico event 1441321): **no talk mentions quirks** (timetable print view parsed by WebFetch). The relevant talks are the ATLAS HSCP dE/dx+ToF talk (Hofer), "CMS: scouting & parking" (Bainbridge) and "CMS: Anomaly Detection Triggers" (Pearkes, L1 AXOL1TL/CICADA plus future L1 tracking/timing for LLPs).
   - LLP2026 (Cambridge, 29 June-3 July 2026, indico event 1592699): the full timetable was not retrieved. The session PDFs seen contain no quirk item. **UNVERIFIED.**
4. **FASER after its first quirk result (2607.26195, 186 fb-1 of 2022-24 data, 0 events):**
   - FASER had recorded >311 fb-1 by early 2026 [2604.16244, p.1, line "accumulating more than 311 fb-1"]. A spring-2026 Liverpool HEP talk says "333 fb-1 (as of last week) recorded" [indico.ph.liv.ac.uk event 2385, FASER_LivHEP.pdf, slide text].
   - FASER is **approved for Run 4** [2604.16244, Sec. 5, "for which FASER has been approved"; same Liverpool slides]. The slides give a "Projected 2025+Run 4 luminosity ~770 fb-1".
   - Run 3 was extended to end around June-July 2026. HL-LHC start-up is planned for June 2030 (CERN schedule pages via web search; not read in full, **UNVERIFIED** in detail).
   - Pre-result projection [2404.13814, Sec. 6, text near the "full Run 3 data" sentence]: with the full Run-3 data FASER probes the colour-neutral E quirk up to **200 GeV (single-track analysis) and 400 GeV (double-track analysis)** for Lambda in [100 eV, 60 keV].
   - The actual 186 fb-1 result reached 179 GeV at 10 keV. An updated FASER quirk search with about 330 fb-1 (2022-26), and later Run-4 data, is therefore likely. It would push the forward exclusion toward about 200-300 GeV. **ESTIMATE**, based on the 2404.13814 projections and the shortfall of the first result relative to them.
5. **FPF / FASER2.**
   - The Letter of Intent is arXiv:2510.26260 (Oct 2025, published Nucl. Phys. B 2026 per web search). Its quirk panel shows "FASER2 2 ab-1" [2510.26260, Fig. near line "Quirks: Many compelling models"].
   - The LoI "conservatively assumes physics data taking starting at the beginning of Run 5 in 2036" [2510.26260, text at Fig. 4 discussion, "uncertainty on the timeline for approval"].
   - **Approval: not found.** Queries: web searches "Forward Physics Facility approved OR approval OR LHCC 2026" and "European Strategy update 2026 Council Forward Physics Facility FASER2". The CERN Council adopted the Strategy update on 22 May 2026 (web search snippet, CERN Courier/home.cern; FPF wording not retrieved, **UNVERIFIED**). 2601.09023 Sec. 2 states that FASER2 "is not an approved experiment yet".
   - FASER2 at 3 ab-1 can discover E up to 1000 (1300) GeV and Ẽ up to 600 (900) GeV over Lambda in [100 eV, 100 keV] [2404.13814, Conclusions].
6. **LHCb VELO proposal (2601.09023, JHEP06(2026)037).**
   - **Important correction to the Gate-4 framing:** the projections (Fig. 2) are for the **coloured (3,1)_{2/3} fermion, N_c=2** only, with mQ 500-3000 GeV. No colour-neutral (1,1)_{-1} projection is given (grep for "(1,1)", "colour-neutral", "Drell" finds only model-context lines).
   - The paper assumes a background-free selection ("at least five VELO stations with back-to-back hits at consistent phi") with Feldman-Cousins limits at 10 fb-1 (2026) and 300 fb-1 (Upgrade II) [Sec. 6].
   - It "strongly encourage[s] the development of dedicated trigger lines ... during the remainder of Run 3" [Sec. 6].
   - Upgrade II needs the 4D VELO [Sec. 6, ref. 53].
   - LHCb is a direct competitor for **coloured** quirks at Lambda ~ 1 keV. It is only a potential reinterpretation competitor for colour-neutral DY quirks: smaller cross section, forward acceptance 2<eta<5, ~1/10 of the CMS luminosity. Its colour-neutral reach is **UNVERIFIED (not computed by anyone)**.
7. **Far detectors** (2311.15486, Li-Liao-Ni-Pei, PRD 109 (2024) 095005; studies Lambda >~ 3 keV [text line "This work explores ... Lambda >~ 3 keV"]):
   - FACET gives the best "go-through" reach: **E up to 1000 GeV at 300 fb-1** [Sec. on exclusion bounds, Fig. 9 text]. The authors warn that "the backgrounds of the FACET detector are much heavier ... 3 signal events may not be enough" [Summary].
   - With the "decay inside" signature at 3 ab-1, FACET reaches E up to 880 GeV [Fig. 10 text].
   - FASER2 beats MATHUSLA for "go through". MATHUSLA beats FASER2 for "decay inside" [same].
   - MoEDAL-MAPP and CODEX-b: no quirk sensitivity study found (queries in App. A).
   - Status: MATHUSLA has been re-scoped to "MATHUSLA-40" near CMS (CDR arXiv:2503.20893). ANUBIS has a proANUBIS demonstrator (arXiv:2512.14942). CODEX-b has the CODEX-beta demonstrator. All are *proposed, not approved* (web search snippets of 2025 talks; no 2026 approval found). FACET approval status: not found (UNVERIFIED).
8. **Recasts.**
   - No full-Run-2 or Run-3 recast of HSCP, disappearing-track or monojet searches for quirks was found.
   - The INSPIRE citers of 1703.00912 (Farina-Low, recid 1516007), 1811.08903 (1704655) and 1911.02223 (1763305) through Oct 2026 contain no new recast. The newest citers are FASER, the reviews 2606.30760/2203.05531, the FPF papers, 2601.09023, 2506.11192, 2504.02940 and 2512.20696 (cosmology).
   - The Farina-Low numbers (12.9 fb-1, 2016) therefore remain the latest HSCP/monojet bounds.
   - Opportunity (low cost, CMS-internal): a quirk reinterpretation of CMS HSCP 2410.09164 (101 fb-1) and of CMS L1DS HSCP 2601.20063 would update the low-Lambda edge. It is not done by anyone.
9. **LEP.**
   - OPAL [hep-ex/0305031, INSPIRE 618779, abstract]: long-lived charged heavy leptons and charginos excluded below **102.0 GeV**. Model-independent sigma limits are 0.005-0.028 pb for charge ±1 scalars/fermions at sqrt(s) = 130-209 GeV.
   - That analysis assumes helical, isolated dE/dx tracks. Whether it applies to quirk pairs is **UNVERIFIED**: it is not discussed in 1703.00912, 1708.02243, 2404.13814, 2311.15486, 2601.09023 or 2607.26195 (grep "LEP").
   - Kinematically, LEP2 cannot produce mQ > ~104 GeV. LEP is irrelevant above the FASER bound (179 GeV).
10. **D0** (1008.3547): 107 GeV, unchanged. No Tevatron update.

### 1.2 Who could cover which (mQ, Lambda) region, and when
Colour-neutral (1,1)_{-1}, N_IC = 2 unless stated.

| Window | Lambda | mQ | Experiment / method | Status | Earliest result (ESTIMATE unless cited) |
|---|---|---|---|---|---|
| Now | 0.3-100 keV | < 179 GeV (at 10 keV) | FASER, slow forward pair | Published [2607.26195] | done |
| Now | < ~0.3 keV | < 150-650 GeV | HSCP/monojet recast (12.9 fb-1) [1703.00912 Table II] | Pheno recast | done (outdated data) |
| 2027-28 | ~0.1-60 keV | up to ~200-400 GeV | FASER full Run 3 (~330 fb-1) | Data in hand | 2027-28; projection 200/400 GeV [2404.13814 Sec. 6] |
| 2027-29 | ~1 keV | coloured only, up to ~TeV | LHCb VELO trigger line, 2026 data (10 fb-1) | Pheno proposal; trigger line not confirmed | 2028+ (UNVERIFIED whether LHCb implements it) |
| 2028-29 | ~0.1-5 keV (pixel-pair resolvable; Lambda grid of 10 points) | ~100 to ~500-650 GeV | **ATLAS quirk search, Run-2/3 ID** (G4 quirks + ML pair finder; Sec. 1.0) | **Active** (code trail Aug-Sep 2026; contour exists; low/no PU so far) | **ESTIMATE 2028-29.** The first central-tracker quirk result will very likely be ATLAS |
| (open) | 0.3-30 keV | ~200-600 GeV | CMS Run-2/3 coplanar search (MET trigger, Phase-1 tracker) | Not found | Only way for CMS to be contemporaneous with ATLAS (2028-29) |
| Run 4 (2030-33) | 0.1-60 keV | up to ~300-400 GeV | FASER Run 4 (~770 fb-1 for 2025+Run 4) | Approved | ~2034 |
| Run 4-5 | 0.6-15 keV coplanar (0.3-0.6 keV with GNN; >15 keV straight-pair) | ~200-900 GeV | **CMS Phase-2 coplanar/non-helical search (this project)** | Proposal | First result ~2033-35 with ~0.5-1 ab-1; 3 ab-1 ~2042 |
| Run 5 (>=2036) | 0.1-100 keV | up to 1000 (1300) GeV | FASER2 at FPF | LoI, not approved (not found) | >=2038 if approved |
| HL | >~ 3 keV | up to ~880-1000 GeV | FACET / MATHUSLA-40 / ANUBIS | Proposals | unknown |
| HL | ~1 keV | coloured, up to ~3 TeV | LHCb Upgrade II VELO | Proposal (Upgrade II) | late 2030s |

**Competition verdict (revised 2026-10-07 after Sec. 1.0).**
- **"First LHC central-detector quirk search" is no longer available to CMS Phase-2.** ATLAS has an active Run-2/3 quirk search. Its signal simulation was fixed in Athena 24.0 in Aug 2026, it has a dedicated ML pair-finder, and an internal sensitivity contour exists. It will most likely publish around 2028-29 (ESTIMATE), covering the same Drell-Yan, mesoscopic-Lambda, ~0.2-0.6 TeV region.
- FASER (Run 3 + Run 4) will push the forward limit to ~300-400 GeV. FASER2 (Run 5, not approved) nominally reaches 1-1.3 TeV.
- **What remains genuinely novel for a CMS Phase-2 analysis:**
  - (a) **PU-200 operation.** No study at μ > 50 exists anywhere, and the ATLAS effort currently has no/low PU.
  - (b) **Mass reach beyond the Run-2/3 contour.** 3 ab-1 buys about +200 GeV, to ~850-900 GeV (feasibility review ESTIMATE). It also covers the large-Lambda corner (5-30 keV, merged hits) using the finer Phase-2 pixels.
  - (c) **A trigger decoupled from ISR**: the P5 "trackless slow straight muon" GMT seed and L1 scouting (Sec. 3.5). This uses CMS-specific Phase-2 L1DS/GMT infrastructure that ATLAS lacks.
  - (d) **MTD 1/β tagging** of the slow pair (Sec. 3.4).
  - (e) **The first CMS result** and an independent confirmation.
- **Recommendation for the STRATEGY:**
  - Reposition C001 from "first quirk search" to "**CMS Run-3 quirk search now, plus a Phase-2 extension**". A CMS Run-2+3 analysis with the MET trigger and Phase-1 pixels (Knapen/Li-style) is the only way to be contemporaneous with ATLAS.
  - The Phase-2 study then becomes the PU-200, trigger (P5) and MTD extension, framed as a Phase-2 projection (FTR-style) that no one has published.
  - **Novelty label for the pure Phase-2 target: downgrade from "proposed-not-searched" to "being-searched-elsewhere (ATLAS, Run 2/3), HL extension open".** Confidence medium. The ATLAS scope (Run 2/3 vs ITk) is inferred from code, not from a public statement.
## 2. Reference-analysis table (JFC Phase-1 requirement; CMS-first)

Three CMS analyses are chosen. Each covers a technique the quirk search must reproduce:

| Analysis | What it teaches the quirk search |
|---|---|
| (A) CMS HSCP dE/dx | Anomalous-track selection with a data-driven estimate on two uncorrelated variables |
| (B) CMS L1-scouting HSCP | Multi-BX slow-particle reconstruction in the muon system and an "unphysical-ordering" background method |
| (C) CMS disappearing tracks | Estimating "spurious" tracks from random hit alignment, which is the closest analogue to random coplanar pile-up hits |

ATLAS dE/dx+ToF is listed as a secondary cross-reference. The CMS stopped-particle search is used only for the non-collision background methodology (Sec. 4).

| | (A) CMS HSCP, dE/dx (CMS-EXO-18-002, arXiv:2410.09164, 101 fb-1, 2017-18) | (B) CMS HSCP with L1 trigger scouting (CMS-EXO-25-010, arXiv:2601.20063, PLB 2026, 3.7 fb-1 effective, 2024, 13.6 TeV) | (C) CMS disappearing tracks (CMS-SUS-21-006, arXiv:2309.16823, 137 fb-1) |
|---|---|---|---|
| **Trigger** | Single muon pT > 50 GeV with an offline tight-muon match. ε_trig = 0.86 for DY stau 557 GeV and 0.11 for gluino 1.8 TeV. Very slow (β<0.5) particles fall outside the muon timing window [Sec. 5; Table 2] | **No trigger selection.** The L1 data-scouting (L1DS) demonstrator records L1 objects plus barrel muon (DT) stubs from every BX at 40 MHz, prescaled at orbit level (N=15) to 3.7 fb-1 out of about 55 fb-1 delivered [Sec. 3]. Covers unit-charge particles with 0.15 ≲ β ≲ 0.80 [Sec. 3] | Hadronic channel: HLT pT^miss > 100-120 GeV (luminosity dependent), >97% efficient. e/μ channels: single e (μ) with pT > 27 (24) GeV [Sec. 3] |
| **Key selection** | pT > 55 GeV, \|η\| < 1.0, ≥2 pixel hits, ≥10 dE/dx measurements, valid-hit fraction > 0.8, χ²/dof < 5, dz < 0.1 cm, dxy < 0.02 cm, PF mini-isolation < 0.02, I_trk < 15 GeV, E/p < 0.3, σ_pT/pT² < 0.0008, F_i^Pixels > 0.3 [Sec. 5, Table 2]. SR (ionization method): F^Pix > 0.9, G_i^Strips > 0.25, pT > 200 GeV [Sec. 6.1] | Offline modified kBMTF fit of DT stubs within ≤8 BXs. Categories by layers/BXs (BX123, BX1234, BX124/134, BX1112, ...) [Table 1]. 2-BX categories also need a second track with pT > 100 GeV, \|η\| < 0.83. Fit variable: track pT. The fiducial σ limit is quoted for pT > 500 GeV, \|η\| < 0.83 [abstract, Sec. 6] | Short (pixel-only) and long tracks with pT > 25 (40) GeV, \|η\| < 2.0, I_rel < 0.2, dxy, dz < 0.1 cm, no hits in the outer 2 strip layers. The track must not be PF-identified, and E_dep / (E_dep/p) cuts plus a BDT score are applied [Sec. 6, Table 2]. 49 SRs [Tables 3-4] |
| **Background estimation** | Fully data-driven, two methods. (i) **Ionization method:** simultaneous fit of G^Strips in PASS (F^Pix > 0.9) and FAIL (0.3-0.9) regions with a pass/fail transfer factor (Eq. 8). Validated at 50-55 and 55-200 GeV pT [Sec. 6.1]. (ii) **Mass method:** ABCD in (G^Strips, pT), N_D = N_B N_C / N_A (Eq. 9), with the mass shape from the I_h and p templates. Bias corrected from validation regions [Sec. 6.2] | **Unphysical stub time-orderings.** "Asynchronous" orderings (stub BX order not compatible with an outgoing particle) model the background pT shape. The normalisation floats per category, constrained by low-pT bins. Validation regions: (i) low-quality tracks, (ii) non-colliding BXs (earliest stub and the 5 preceding BXs are empty) [Sec. 7] | **Genuine-particle** background: sideband CRs in E_dep/BDT plus a DY "measurement CR" transfer factor κ (Eq. 4, Table 5). **Spurious-particle** background (random hit alignment from ≥2 particles): sideband CRs in low BDT score with a transfer factor θ from a QCD-enriched region (N_e=N_μ=N_b=0, 30 < pT^miss,hard < 60 GeV), Eq. 6, Table 6 [Sec. 8.1-8.2] |
| **Systematic program (sizes)** | **No systematics table** (text only, Sec. 7). Signal: muon-trigger timing (β, η) is the dominant term, "as large as 30%" (from 1.5 ns DT delay variations). G^Strips stability < 1%. F^Pix 0.5% (shape). Muon momentum resolution 10% of p. Muon trigger/ID scale factors < 1%. Luminosity 2.0% (2017-18). Pile-up < 1%. Background: statistical uncertainty of the FAIL region and R_P/F (ionization); bias correction ±100% (applied 0x or 2x) as the largest term for the mass method [Sec. 6.2, 7] | Background pT-shape nuisances from alternative asynchronous subsets [**Table 2**]: 5-60% (>2-BX categories, pT > 450 GeV), 5-30% (BX1112/BX1222), 5-75% (3-stub 2-BX). Constrained to ~50% in the fit. Signal normalisation from DY(μμ) efficiency correction (including luminosity and σ_DY): ~3% (3-stub) / 2% (4-stub). Statistically limited [Sec. 8] | **Table 7.** Signal: DTk selection efficiency 10-17%, luminosity 1.6%, JES/JER 0-24%, b-tag 0-4%, μR/μF 0-2%, ISR 0-3%, pile-up 0-2%, trigger 0-4%, dE/dx calibration 3-8%. Background: genuine showering long 20-28%, short 100-104%, genuine muon long 25-38%, spurious long 5-52%, spurious short 6-28%. Also 30%/20% residual-pT terms for spurious/genuine long tracks [Sec. 9] |
| **Lesson for C001** | ABCD/pass-fail on two independent quantities. For quirks these are coplanarity Δs (or the plane χ²) and an orthogonal variable such as hit multiplicity per layer, MET-plane Δφ or pixel ToT. The ToT handle is weak at Phase-2: the OT is binary, see Sec. 3.1 | (1) A CMS-approved pathway for **multi-BX, slow, trigger-less** muon-system signatures. (2) Background from **unphysical orderings** maps directly onto quirks: inward-going or asynchronous stub sequences, and planes not containing the beam line. (3) A neutral, straight-moving quirk pair would be assigned the maximal pT by the muon fit, which is exactly where the SR lives (inference, **UNVERIFIED**) | The spurious-track method is the **template for random coplanar pile-up hits**: sideband in plane quality, transfer factor from a low-MET region dominated by pile-up |

**Secondary cross-reference (ATLAS, competition):** ATLAS dE/dx + ToF, arXiv:2502.06694, 140 fb-1.
- Trigger: E_T^miss, HLT threshold 70-120 GeV; signal trigger efficiency 20% to >95% [Sec. 5.2].
- Background: pseudo-data from uncorrelated (pT, η, dE/dx, β_ToF) templates [Sec. 5.3].
- Systematics [Sec. 5.5]:
  - template-correlation non-closure: 5% at 200 GeV to 23% at 700 GeV (largest single term); di-track closure: 10% to 40%;
  - η-slicing < 5%; dE/dx tail < 1%; template statistics ≤ 5%;
  - E_T^miss trigger < 2%; β_ToF η-slicing ~10%; β_ToF tail 3-10%.
- No systematics table was found in the text (Tables 3-8 are yields and mass windows).

**Non-collision background reference:** CMS stopped particles, arXiv:1801.00359.
- Trigger: empty BXs ≥ 2 BX from any bunch.
- Backgrounds: cosmics from dedicated cosmic runs plus an inverted Δt_RPC extrapolation; beam halo from CSC tagging; HCAL noise from cosmic-run control samples [Sec. 3.1, 6]. Table 4 gives 2016 halo 2.6±0.2 and cosmics 8.8±3.1 events in 586 h of live time.
- Signal systematics: **Table 5** (calorimeter search: reconstruction efficiency 7.5%, luminosity 2.5%, JES 2.0%) and **Table 6** (muon search: Q/pT resolution 7.0%, trigger acceptance 2.8%, luminosity 2.5%, all 2016).

## 3. HL-LHC trigger and detector plan (CMS Phase-2 first)

Sources read in full text for this section: the CMS Phase-2 L1 TDR (CERN-LHCC-2020-004 / CMS-TDR-021, INSPIRE 1819968), Tracker TDR (CERN-LHCC-2017-009 / CMS-TDR-014, INSPIRE 1614103) and MTD TDR (CERN-LHCC-2019-003 / CMS-TDR-020, INSPIRE 1819664). PDFs were downloaded from the INSPIRE file store and converted with pdftotext. "TDR p." below means the printed page.
- The DAQ-HLT TDR (CMS-TDR-022) was **not found on INSPIRE** with the queries in App. A. Its key numbers are taken from the CMS proceeding arXiv:2211.03684 (Tomei, "The High-Level Trigger for the CMS Phase-2 Upgrade"), which summarises that TDR (its Table 1 and Table 2).
- Detector numbers are TDR baselines (2017-2020). The as-built layout may differ, for example the final Inner Tracker radii. Treat them as such.

### 3.1 Detector facts relevant to quirks (CMS Phase-2)
| Item | Value | Source |
|---|---|---|
| Inner Tracker barrel (TBPX) radii | 29.0, 70.1, 117.8, 157.4 mm; \|z\| ≤ 199.7 mm | Tracker TDR **Table 10.1** |
| IT forward | TFPX 8 double-discs at z = 250-1400 mm; TEPX 4 double-discs at z = 1750-2550 mm | Tracker TDR Table 10.1 |
| Pixel size / charge info | 25×100 or 50×50 µm²; **4-bit ToT**; hit rate up to 3 GHz/cm² (layer 1); noise occupancy < 1e-6 | Tracker TDR **Table 4.4** |
| Outer Tracker barrel radii | TBPS (PS modules): 248.1, 371.7, 522.7 mm. TB2S (2S modules): 687.0, 860.0, 1108.0 mm. \|z\| ≲ 1.2 m. TEDD 5 double-discs at z = 1312-2650 mm | Tracker TDR **Table 9.1** |
| OT granularity | 2S: 2×1016 strips of ~5 cm × 90 µm. PS: strips of ~2.4 cm × 100 µm plus macro-pixels of ~1.5 mm × 100 µm | Tracker TDR **Table 3.1** |
| OT readout | **Binary** ("All the front-end chips implement binary readout"). So there is **no analog dE/dx in the OT**; dE/dx comes only from the pixel 4-bit ToT | Tracker TDR Sec. 3.1, text after Table 3.1 |
| η coverage | Tracking up to \|η\| ≈ 4 (IT). OT / L1 track finder \|η\| < 2.4 | Tracker TDR Sec. 2 (line "efficient tracking up to about \|η\| = 4"); L1 TDR Sec. 1.3.2.1 |
| Barrel layers a central quirk crosses | 4 (TBPX) + 3 (TBPS) + 3 (TB2S) = **10** (vs 8 in Knapen's ATLAS-like model, \|η\| < 1.8 [1708.02243 Sec. III]) | Derived from the Table 9.1/10.1 values |
| Offline / online tracking | Offline: 8 iterations, all pixel-seeded or muon-seeded helices [Tracker TDR **Table 12.6**]. Online (HLT) baseline: "only two iterations" [2211.03684 Sec. 2] | as cited |
| MTD | BTL: \|η\| < 1.48, r = 1148-1188 mm. ETL: 1.6 < \|η\| < 3.0. MIP resolution 30-40 ps at start, 50-60 ps end-of-life (luminosity-weighted 40-50 ps) | MTD TDR Sec. 1 (lines on "30-40 ps ... 50-60 ps"), Sec. 2 (BTL radius), Sec. 1.x (ETL) |
| MTD HSCP use | 1/β from track time. A 5σ cut moves from 1/β > 1.25 (muon-system ToF) to 1/β > 1.05, giving ×4 signal acceptance (stau GMSB) | MTD TDR **Sec. 5.4.3**, Fig. 5.30 |
| Calorimeter timing at L1 | ECAL (HCAL) trigger primitives: 30 ps (500 ps) for objects with pT > 50 GeV | L1 TDR Sec. 1.3.2.1 |

### 3.2 L1 and HLT parameters at PU 200
- L1: latency **12.5 µs**, max accept rate **750 kHz** [L1 TDR Sec. 1, lines "latency ... extended to 12.5 µs", "750 kHz"]. The L1 track finder covers \|η\| < 2.4 with 4-5 µs latency and ~1000 tracks with pT > 2 GeV per event [L1 TDR Sec. 1.3.2.1].
- HLT: input 750 kHz, **output 7.5 kHz**, computing power 37 MHS06, event size 8.4 MB at the HLT input [2211.03684 **Table 1**, from the DAQ-HLT TDR].
  - **ESTIMATE:** the average budget is 37e6 HS06 / 750 kHz ≈ 49 HS06·s per L1-accepted event, about 3.8 s per event per logical thread on the reference node (1680 HS06, 128 threads).
  - The simplified-menu timing measured 5.3 s per event, of which tracking is 22.8% (1.2 s) and pixel reconstruction 17% [2211.03684 Sec. 3, Fig. 3 table].

Phase-2 L1 menu (simplified menu, Phase-1 thresholds kept; **L1 TDR Table 4.1, p. 210-211**), seeds relevant to quirks. "Offline threshold" means the 90/95% plateau point, with the 50% point in parentheses.

| Seed | Offline threshold [GeV] | Rate at PU 200 [kHz] | Relevance |
|---|---|---|---|
| PuppiETmiss | **200 (128)** | 18 | Main ISR-recoil path. The quirk pair is invisible to PUPPI MET (no L1 track; only ~1 + 4 GeV in ECAL + HCAL per pair [1911.02223 Sec. III]) |
| PuppiETmiss lowered | **170 (100)** | +42 | Option discussed in the L1 TDR for compressed spectra [p. 209] |
| Single PuppiJet | 180 | 70 | ISR jet; \|η\| < 2.4 |
| PuppiHT | 450 (377) | 11 | weak |
| TkMuon-PuppiJet-PuppiETmiss | 3, 100, 120 (55) | 14 | requires an L1 track-matched muon, so unlikely |
| Single TkMuon | 22 (15 option, +30 kHz) | 12 | **needs an L1 track** |
| Total simplified menu | | 346, or 450 with +30% | 50% margin to 500 kHz; room for new seeds [Sec. 4.2] |

Extended menu (**L1 TDR Table 4.6**): Displaced Single/Double Muon (22; 20, 15 GeV) and Displaced Calo-Jet (40 GeV, Δt > 1 ns, \|η\| < 1.44). These are not matched to prompt, slow, trackless quirk pairs.
- HLT simplified menu at PU 200 [2211.03684 **Table 2**]: Missing pT > **140 GeV at 228 ± 20 Hz**; single jet 520 GeV; HT 1070 GeV. The quirk search therefore cannot rely on HLT jet/HT. **The HLT MET path is not the bottleneck: L1 MET (128 GeV at 50%) is.**

### 3.3 Can quirk hits form L1 stubs or L1 tracks? (UNVERIFIED; analysis)
- **Stub mechanism.** The two sensors of a pT module are 1.6/2.6/4.0 mm (PS) or 1.8/4.0 mm (2S) apart [Tracker TDR Sec. 3.1, Table 3.2]. The front-end accepts hit pairs whose displacement is consistent with pT ≳ 2 GeV [Tracker TDR Sec. 2, Fig. 2.5]. TRIG stubs from pT > 2 GeV particles are transferred with >99% efficiency [Tracker TDR Sec. 3.3.2].
- **Geometric ESTIMATE.** In 3.8 T a 2 GeV track has R = 1.75 m. Its crossing angle to the radial direction is α = asin(r/2R) = 4.1°, 6.1°, 8.6° in TBPS L1-L3 and 11.3°, 14.2°, 18.4° in TB2S L1-L3. A quirk hit forms a stub only if its *local* direction is within roughly these angles of radial (in the bending plane).
  - The pair's centre of mass is net-neutral and moves on a straight line from the vertex.
  - Each quirk deviates by the oscillation, with relative velocities up to O(0.5c) in the pair frame [1911.02223 Sec. III; 1708.02243 Sec. II].
  - The **stub fraction is therefore Λ-, phase- and plane-orientation-dependent and is unknown.** This is the first item for the Phase-2 simulation.
- **Large-Λ corner (≳10-30 keV; inference).**
  - The oscillation amplitude ℓ ~ 1 cm × (1 keV/Λ)² × (mQ/100 GeV) [1911.02223 Eq. I.1] falls to ~50-500 µm for mQ = 500 GeV at Λ = 10-30 keV. That is comparable to the 90-100 µm strip pitch.
  - The pair would then look like **one straight, infinite-momentum track with doubled charge**. It could form stubs and **an L1 track with saturated pT**: isolated, no calorimeter deposit, and no in-time muon match. Knapen also notes merged hits for Λ ≳ 5 keV [1708.02243 Table I caption].
  - This would open an L1 "high-pT isolated trackless-calo track" seed, or the L1 HSCP seed below. It must be simulated before use.
- **L1 HSCP seed** [L1 TDR Sec. 3.3.5 item 4, p. 117]: an L1 tracker track matched to muon stubs in up to 3 subsequent BXs, with 16 β hypotheses. It reaches β down to 0.2. Rate < 10 kHz for pT > 7 (20) GeV with (without) quality cuts. Efficiency > 40-100% for 0.2 < β < 0.6. **It needs an L1 track, so it is ineffective for quirks unless the large-Λ corner above applies.**

### 3.4 Timing of the slow pair (ESTIMATE, kinematics only)
- **Centre-of-mass speed.** For central DY production M_QQ̄ ≈ 2.3 mQ (ESTIMATE). The transverse speed is β_T = pT/√(M² + pT²):
  - pT(QQ̄) = 200 GeV: β_T ≈ 0.28, 0.17, 0.11 for mQ = 300, 500, 800 GeV;
  - pT = 50 GeV: β_T ≲ 0.07.
  - 1911.02223 Sec. IV finds v_T ~ 0.1 for heavy pairs and says pairs "escape the tracker within 10-20 ns". O(10)% (≳ 50%) do not reach the ECAL (HCAL) within 25 ns [ibid.].
- **Arrival times** (radial, η = 0):
  - BTL at 1.15 m: delay vs. β=1 of 9 ns (β=0.3), 15 ns (0.2), 35 ns (0.1).
  - MB1 (~4 m): 1.8 / 2.7 / 5.3 BX.
  - MB4 (~7 m): 3.1 / 4.7 / 9.3 BX.
- **Consequences:**
  - (i) The outer-tracker hits of heavy, slow pairs can straddle BX and BX+1. Knapen's ε_fid = 0.28 already includes a 25 ns cut [1708.02243 Sec. IV]. Reading the next BX for the tracker is a DAQ/trigger-rules question (**UNVERIFIED**).
  - (ii) MTD (see Sec. 3.4b: the ETL TDC window is 6.25 ns, so slow hits are lost there): if late hits are recorded, the expected 1/β resolution is ~0.009 (35 ps / 3.8 ns; ESTIMATE). Any quirk with β < 0.9 is then separated at ≫ 5σ. Whether TOFHIR/ETROC record hits 10-35 ns late in the triggered BX is **UNVERIFIED**.
  - (iii) Muon system: most pairs arrive 2-9 BX late. Only the β ≳ 0.15-0.2 part fits the L1DS (≤ 4 BX [2601.20063 Sec. 6]) or GMT-HSCP (3 extra BX) windows.
  - (iv) Stopping: ≲ 5% of E'-like 400 GeV pairs stop in the \|η\| < 1 calorimeters (inclusive production) [1811.08903 Fig. 2]. A similar number again stop in the muon return yoke [1811.08903 Sec. 5].

### 3.4b Do the Phase-2 trackers and MTD record hits that arrive 10-20 ns late in the correct BX? (TDR specs; answer UNVERIFIED in detail)
| Sub-detector | Front-end timing spec in the TDR | Implication for a quirk hit Δt = 10-20 ns late |
|---|---|---|
| OT 2S (CBC, binary) | Peaking ~20 ns, return to baseline < 50 ns, "process hits in consecutive bunch crossings without dead time". Data sent every 3.125 ns at 320 Mb/s, up to 3 stubs/CBC/BX [Tracker TDR Sec. 3.3, text after Fig. 3.10] | The hit is BX-tagged by the 40 MHz sampling of the comparator output. The **sampling phase and hit-detect mode are not specified in the TDR** (grep "latched", "sampled mode": 0 hits). A 10-20 ns delay is a large fraction of the 25 ns BX and of the ~20 ns peaking time, so a **significant BX+1 assignment probability is expected** (ESTIMATE). The large quirk charge (slow, high dE/dx) reduces time walk, which partly helps |
| OT PS (SSA strips, MPA macro-pixels, binary) | SSA peaking 17 ns (< 50 ns to baseline) [Tracker TDR Sec. 3.3]. MPA-light prototype: peaking 24 ns, **time walk < 15 ns** [Tracker TDR Sec. 9, MPA-light paragraph] | The time-walk budget (< 15 ns) is designed for prompt in-time tagging. An extra 10-20 ns of flight delay is outside this design envelope, so **at risk of BX+1** (ESTIMATE) |
| IT pixels (CROC/RD53) | "In-time threshold < 1200 e-" (detection threshold < 600 e-), 4-bit ToT, buffer ≥ 8 for the 12.5 µs latency [Tracker TDR **Table 4.4**] | The in-time threshold is defined for prompt hits. At IT radii (≤ 16 cm barrel) the delay is only ~1-2 ns even for β_T ≈ 0.1-0.3 [r/(βc)], so **the IT is safe** |
| ETL (ETROC) | TOA/TOT TDC **measurement window 6.25 ns** per 25 ns BX (extended from 2.5 ns for ALTIROC) [MTD TDR **Sec. 3.3.6**] | A hit 10-20 ns late falls **outside the TDC window, so no timestamp**. The ETL is useless for very slow quirks unless the window phase is moved (a firmware/config question) |
| BTL (TOFHIR) | Analog processing "within 25 ns"; QDC integration window 4 clock cycles = 25 ns [MTD TDR Sec. 2.x, TOFHIR text] | The TOA range relative to the BX was **not found** in the TDR text. Whether 10-20 ns late hits are timed is **UNVERIFIED** |

**Arrival delays at the relevant radii** (ESTIMATE, δt = (r/c)(1/β - 1)):
- At TB2S L3 (r = 1.108 m): δt = 3.7 ns (β = 0.5), 8.6 ns (β = 0.3), 14.8 ns (β = 0.2).
- At the BTL (1.15 m): 3.8, 9.0 and 15.3 ns.
- The theory agent quotes β ≈ 0.3-0.6 for mQ ≳ 500 GeV (research/theory_signal_model.md). Sec. 3.4 gives β_T ≈ 0.1-0.3 for a central pair recoiling at 200 GeV. Either way the **outer two to three OT layers and the MTD see δt ≈ 4-15 ns**.

**Consequences:**
- (i) Inner-tracker and inner-OT hits are in time.
- (ii) Outer-OT hits may migrate to BX+1. This costs exactly the lever arm the plane fit needs, and it removes outer-layer stubs.
- (iii) The ETL cannot time them; the BTL is unknown.

**Required Phase-2 studies:**
- The CBC/SSA/MPA in-time efficiency vs injected delay. Lab test-pulse delay scans exist for commissioning; a CMS tracker-DPG contact is needed.
- Reading out BX and BX+1. This needs two L1As 25 ns apart, and the Phase-2 trigger rules for consecutive L1As are **UNVERIFIED**.
- Any slow-particle mode in the BTL/ETL configuration.

### 3.4c Lambda window for the coplanar method at 3.8 T (input from the theory agent)
- The plane thickness scales as ∝ B·mQ/Λ⁴. At CMS's 3.8 T the coplanar plane-finder works for **Λ ≈ 0.6-15 keV** (research/theory_signal_model.md, Sec. 4.4 and line "The coplanar window is narrower at CMS than at ATLAS", citing 1911.02223 Eq. III.12 and 2002.07503 Eq. V.6-V.9).
- Below ~0.6 keV a trajectory fit or GNN is needed. Above ~20-30 keV the pair merges into one straight ~2×MIP track.
- **This document therefore uses Λ ≈ 0.6-15 keV as the coplanar-method window** for the trigger efficiencies (Sec. 3.6) and the backgrounds (Sec. 4). Λ = 0.3-0.6 keV is assigned to an ML/trajectory extension.
- Λ ≳ 15-30 keV belongs to a separate "straight, trackless-calorimeter, 2×MIP, slow" signature. That signature is the natural home of the L1-track hypothesis in Sec. 3.3 and of the P5 trigger.
- Compared with ATLAS (2 T), the CMS field narrows the low-Λ end of the coplanar window. This is a *disadvantage* relative to the ATLAS search in Sec. 1.0 at Λ ~ 0.3-0.6 keV, and an argument for including the GNN/trajectory reconstruction (2410.00269; the ATLAS MaskFormer approach) from the start.

### 3.5 Quirk-specific trigger handles (CMS Phase-2)
1. **ISR recoil via L1 PuppiMET → HLT MET 140 GeV** (baseline; robust, standard).
2. **Lowered L1 PuppiMET** (170/100 GeV option, +42 kHz) [L1 TDR p. 209]; could be justified jointly with compressed-SUSY / disappearing-track programmes.
3. **New GMT seed: "trackless slow straight muon"** (proposal). It uses barrel DT/RPC stubs over ≥ 3 BXs with an outward time ordering (the 2601.20063 categories), *no* L1-track requirement, and saturated or very high muon-fit pT (a neutral pair does not bend).
   - The BX of the collision is inferred from the β fit. The L1A is issued for that BX within the 12.5 µs latency, which reads out the tracker hits.
   - Background reference: in 3.7 fb-1 the non-colliding validation region has O(1-10) events per category above 50 GeV [2601.20063 Fig. 7]. This implies a very low rate. **ESTIMATE ≪ 1 kHz; UNVERIFIED.**
4. **L1 scouting at 40 MHz** (Phase-2 baseline system [INSPIRE 3110965, 3157038, titles; L1 TDR Sec. 5.7]): a standalone muon-stub analysis of slow, straight, multi-BX pairs with **no tracker hits**. It is a complementary low-cost search and a background-rate measurement for handle 3.
5. **High dE/dx at L1:** not available. The OT is binary and the pixels are not in L1. **Not usable.**
6. **MTD timing at L1:** not in the L1 baseline (not found in L1 TDR text). Offline/HLT only.
7. **HLT quirk path:** needed only if handle 3 is adopted, to reduce its rate after L1. HLT tracking is helix-based (2 iterations), so a plane-finder [1708.02243 Sec. III C, "may be sufficiently fast for implementation at the HLT"] or GNN [2410.00269 Sec. VII] would run on L1-seeded events.
   - At 18 kHz (the PuppiMET seed rate) and 1 s/event/thread, it would use ~18 k threads, ~0.6% of the ~2.8 M-thread-equivalent farm (**ESTIMATE**, from Table 1 of 2211.03684).

### 3.6 Trigger efficiency per path for DY colour-neutral quirk pairs (ESTIMATE)
Scope: coplanar window Λ ≈ 0.6-15 keV (Sec. 3.4c). P4/P5 also serve Λ ≳ 15 keV.

Inputs:
- ε_trig = 0.10 for pT(QQ̄) > 200 GeV, DY mQ = 800 GeV, 13 TeV [1708.02243 Table I].
- ε ≈ 0.1 for pT(j) > 200 GeV, E^c pairs [1911.02223 App. A].
- L1 TDR Table 4.1 plateau and 50% points; HLT MET 140 GeV [2211.03684 Table 2].
- The fraction of heavy DY pairs with recoil above X is assumed to scale as ε(pT > 130) ≈ 1.8 ε(pT > 200) and ε(pT > 100) ≈ 2.5 ε(pT > 200). This is an **ESTIMATE** (typical ISR spectrum). It must be replaced by an MG5+Pythia generation, which is not available on this machine (no pythia8/mg5 found).

| Path | Offline requirement | ε_trig (mQ 300-800 GeV) | Notes |
|---|---|---|---|
| P1 L1 PuppiETmiss 200(128) + HLT MET 140 | pT(QQ̄) ≳ 200 GeV (plateau) | **0.08-0.12** | Baseline. Reproduces the Run-2 number |
| P1' same seed, analysis down to the 50% point | pT(QQ̄) ≳ 130 GeV with turn-on | 0.13-0.18 | needs a trigger turn-on systematic (cf. ATLAS < 2% [2502.06694 Sec. 5.5]) |
| P2 lowered PuppiETmiss 170(100) | pT ≳ 170 GeV plateau / 100 GeV turn-on | 0.15-0.25 | +42 kHz: needs a menu negotiation |
| P3 Single PuppiJet 180 (OR with P1) | ISR jet pT ≳ 180 GeV | +0.01-0.02 over P1 | HLT still needs MET (single-jet HLT is 520 GeV) |
| P4 TkMuon / L1-HSCP seeds | L1 track required | ~0 (Λ ≲ 10 keV); unknown at large Λ | Straight-pair L1-track hypothesis is UNVERIFIED |
| P5 New "trackless slow straight muon" GMT seed | barrel \|η\| ≲ 0.83, β_T ≈ 0.15-0.8, ≥3 stations | **0.05-0.2** | = f(\|η\|<0.83) ~0.5 × f(β window) ~0.2-0.5 × ε_alg ~0.5-0.9 [2601.20063 Sec. 3, Fig. 4]. **No ISR needed**, so it adds low-pT pairs. UNVERIFIED |
| P6 L1 scouting (offline muon-stub analysis) | as P5, without the L1 rate limit | 0.05-0.2 (L1 objects only) | No tracker hits: a separate, complementary analysis |
| **Best combination: P2 ∪ P5** | | **~0.2-0.35** | vs 0.10 in the Run-2 proposal |

**Bottom line.**
- The *safe* trigger path is P1/P1' (ε ≈ 0.1-0.18).
- The *highest-leverage R&D* item is P5. It decouples the trigger from ISR, and CMS already has the L1DS and GMT-HSCP machinery.
- The simulation must establish:
  - the fraction of DY pairs with β_T in the 0.15-0.8 window that reach ≥ 3 DT stations;
  - the DT segment response to two quirks separated by ≲ 1 mm;
  - the fake rate of trackless multi-BX straight stubs at PU 200.

### 3.7 ATLAS (competition, not extracted in detail)
ATLAS Phase-2 documents: ITk Pixel TDR (INSPIRE 2091130), HGTD TDR (INSPIRE 2091129), TDAQ TDR.
- The numerical L0/EF menu thresholds were **not extracted** in this round (UNVERIFIED).
- ATLAS has no counterpart of a CMS-style barrel-stub multi-BX scouting result. The SLAC quirk page (Sec. 1.1) targeted Pixel+SCT+TRT, which is the pre-ITk detector.

## 4. Backgrounds for a coplanar-hit search at PU 200
Scope: Λ ≈ 0.6-15 keV at 3.8 T (Sec. 3.4c). Note that B1 grows if the outer-OT hits of slow pairs migrate to BX+1 (Sec. 3.4b), because fewer layers are then available to constrain the plane.


**Published rates (all at ⟨μ⟩ = 50, ATLAS-like 8-layer geometry; no PU-200 number exists anywhere):**
- About 10⁻³ of pile-up events contain a plane with ≥ 1 hit in 4/8 layers, and 6×10⁻⁵ have hits in all layers. There are "O(1000) unassociated pile-up hits per layer" [1708.02243 Sec. IV].
- Conversions: the Z(νν)γj fiducial σ is ~1 pb, and ~10 fb after requiring a beam-pipe conversion (pT,γ > 0.5 GeV, MET > 200 GeV) [1708.02243 Sec. IV].
- Li et al. reproduce Knapen with the real ATLAS tracker (3 pixel + 4 SCT layers):
  - plane with ≥ 1 hit per layer: ~10⁻⁴;
  - five coplanar hits in the 3 outer layers: ~10⁻³;
  - "all but one layer with 2 hits": ~10⁻².
  - Final **Z(νν)+jets ⊗ PU: ~10⁻² fb, "which cannot be neglected"** [1911.02223 Sec. IV and App. A]. That is ≈ 30 events in 3 ab⁻¹ at μ = 50 (ESTIMATE).
- Phase-2 occupancy anchors:
  - pixel chip spec up to 3 GHz/cm² (layer 1) [Tracker TDR Table 4.4];
  - maximum average stub rates of 5.1 (PS) and 1.2 (2S) stubs/module/BX at PU 200, vs 4.1 / 0.8 at PU 140 [Tracker TDR **Table 12.5**].
- **ESTIMATE / UNVERIFIED:** naive combinatorics give a random-plane probability ∝ ρ^n_extra, i.e. a factor 4^n_extra from μ = 50 to 200 for n_extra hits beyond the seed. CMS Phase-2 granularity (25×100 µm² pixels, 90-100 µm strips, 1.5 mm macro-pixels, 10 barrel layers) partly compensates. **The PU-200 random-coplanarity rate is the single most important number to compute in Phase 2 of this project.**

| # | Background class | Mechanism | Published rate / scaling | Discriminants | Data-driven estimate (proposed) |
|---|---|---|---|---|---|
| B1 | **Random pile-up hit coplanarity** (dominant) | Unassociated PU hits (after removing hits on reconstructed helices) that land within Δs, Δw of a plane through the PV | 10⁻³-6×10⁻⁵ per event at μ = 50 [1708.02243 Sec. IV]; steeply rising with μ (above) | Plane thickness Δs and width Δw; ≥2 hits in ≥ N-1 of 10 layers; plane contains the PV and beam spot; MET direction in the plane (Δφ(MET, n̂) [1708.02243 Sec. IV]); hit-pair separation pattern vs radius (oscillation); trajectory χ² fit [1708.02243; 2410.00269]; pixel ToT | (a) **Spurious-track-style transfer factor** [2309.16823 Sec. 8.2]: sideband in plane quality (Δs or χ²) × θ from a low-MET, PU-dominated region. (b) **Hit-mixing / embedding:** overlay hits from zero-bias events (different BX) on MET-triggered events to build the random-plane rate vs nPV. Extrapolate in bins of nPV (or MTD-measured PU density). (c) **ABCD** in (Δs, N_layers with 2 hits) or (Δs, Δφ(MET, n̂)), cf. the 2410.09164 mass method (Eq. 9) |
| B2 | Z(νν)+jets ⊗ PU (B1 conditioned on the MET trigger) | Irreducible MET source plus random planes | **~10⁻² fb at μ = 50** [1911.02223 App. A] | as B1 | Same as B1, normalised in Z(μμ)+jets with muons removed ("MET-emulated", standard CMS invisible-Z technique), where the coplanar-hit search is repeated after removing the muon hits |
| B3 | Photon conversions | e⁺e⁻ pair: two nearby hits per layer, approximately coplanar | ~10 fb fiducial before selection [1708.02243 Sec. IV]; Phase-2 material budget differs (UNVERIFIED) | Opposite helical curvature in 3.8 T (a quirk pair is not a helix pair); a conversion vertex at material radii; hits start at beam pipe/IT layers; plane does not contain the PV in 3D; E/p and ECAL deposit | Conversion-enriched CR (inverted conversion-vertex veto); data **material map** from conversion and nuclear-interaction vertices; Z→μμγ (FSR) conversions as a standard candle |
| B4 | Nuclear interactions in material | Secondary vertex with several tracks at material radii | not published for this selection | SV at a material radius, multiplicity, helical tracks | NI-vertex CR (invert the SV veto); rate vs material radius from data |
| B5 | Loopers / low-pT helices | pT ≲ 1 GeV tracks curling (R = 0.88 m × pT/1 GeV at 3.8 T) leave many hits in few layers. Also out-of-time loopers from BX-1 | not published | Good helix χ²; low pT; plane orientation (loopers ⊥ z, not through the PV direction); hits do not progress radially | Sideband in helix-χ² (good-helix region); **non-colliding BX after a colliding one** (bunch-train tails) for the out-of-time component |
| B6 | Delta rays / split clusters / merged close tracks | A single high-pT track with δ-electrons or 2-track merging gives "2 hits per layer in a narrow strip" | not published | Correlated with a reconstructed helix; δ-rays short (few layers); pixel ToT pattern; cluster shape | **Tag-and-probe with Z→μμ muons:** measure the per-layer probability of a second nearby hit along isolated muon tracks. Apply it to the helix-veto inefficiency |
| B7 | Collimated pairs (jets, π⁰ Dalitz, τ 3-prong, boosted hadrons) | Two energetic close tracks form a narrow strip [1911.02223 Sec. IV: "two charged particles flying in a similar direction"] | part of the 10⁻³ at μ = 50 [1911.02223] | Both reconstructed as helices; calorimeter energy; isolation | Invert isolation / helix-veto; QCD-multijet CR at low MET (as 2309.16823 θ) |
| B8 | Beam halo | Muons parallel to the beam give hits at fixed (r, φ), long in z, with fake MET via bremsstrahlung | stopped-particle search: 2.6 ± 0.2 events / 586 h (different selection) [1801.00359 Table 4] | Plane containing the beam line but not the PV; early CSC hits in one endcap; MTD time; no PV association | Halo-tagged sample (CSC/endcap timing); unpaired/non-colliding bunches |
| B9 | Cosmic muons | Straight, through-going, large d0, out of time; back-to-back in the muon system | 8.8 ± 3.1 events / 586 h in the stopped search [1801.00359 Table 4] | d0/dz to the PV; MTD and DT timing (ingoing in the upper half); opposite-hemisphere matching | Cosmic-run data; **inverted timing** (as the inverted Δt_RPC method, 1801.00359 Sec. 6.2); non-colliding BXs |
| B10 | Detector noise / hot channels | Random clusters, correlated noise bursts | pixel noise occupancy < 10⁻⁶ (spec) [Tracker TDR Table 4.4] | Cluster shape, ToT, module-level occupancy, time stability | Zero-bias and empty-BX data; noisy-module masks; run-dependence checks |
| B11 | SM slow/heavily ionising particles (deuterons, nuclear fragments) | Low-β, high-dE/dx, short tracks | small, not published here | Not coplanar pairs; pixel ToT | Low-pT high-ToT CR |
| B12 | **Muon-system (P5/P6) fakes** | BX misidentification of in-time muons; combinations across BXs; slow cavern neutrons | 2601.20063: per-stub BX misID < 1% (2 RPC layers) to 6% (no RPC) [Sec. 6]. Background shape uncertainty 5-75% [Sec. 8] | Outward time ordering; straightness; ≥ 3 stations; second object | **Asynchronous-ordering templates and non-colliding VR**, exactly as in 2601.20063 Sec. 7 |

**Recommended background strategy (for the STRATEGY draft):**
1. Treat the analysis as **not background-free**. Predict B1+B2 with two independent data-driven methods: a sideband transfer factor (2309.16823-style) and hit-mixing/embedding with an nPV extrapolation. Cross-check them in an inverted-Δφ(MET, plane) VR.
2. Build B3/B4 from the data material map, and B6 from Z→μμ tag-and-probe.
3. Validate the non-collision classes (B8-B10) in non-colliding BXs and cosmic runs.
4. Use **blinded unphysical topologies** as VRs: planes not containing the PV, inward time ordering, and planes with hits only in the outer layers.
5. **Systematics expectation (ESTIMATE, by analogy):**
   - background transfer factors: 20-50% per category (cf. 2309.16823 Table 7, spurious long 5-52%; 2601.20063 5-75%);
   - signal: trigger turn-on 2-30% (2502.06694 < 2% for MET; 2410.09164 up to 30% for muon timing). For the P5 path, the muon timing is the analogue of the 30% term;
   - ISR modelling: FASER shower scale ~6%, up to 28% at small Λ [2607.26195 p.5];
   - quirk dynamics (ε glueball emission, energy-loss model): UNVERIFIED size, likely dominant;
   - luminosity: 1-2.5% (HL-LHC target UNVERIFIED);
   - pixel ToT calibration: cf. dE/dx calibration 3-8% [2309.16823 Table 7].

## Appendix A. Queries run (2026-10-07)
**INSPIRE** (via `research/tools/inspire.py`; "→" gives the outcome):
- `abstracts.value:"quirk" and date > 2025-06` → no experimental hit; 2512.20696 (cosmology), 2601.09023, 2506.11192, 2504.02940
- `t quirks and date > 2025`; `abstracts.value:"quirks" and date > 2025`; `t quirk and date > 2026` → FASER 2607.26195 is the only experimental item
- `abstracts.value:"quirky"`; `abstracts.value:"non-helical" or abstracts.value:"nonhelical"` (cosmology/MHD noise only); `abstracts.value:"anomalous tracks" or abstracts.value:"unconventional tracks"` (0)
- `abstracts.value:"quirk" and (collaboration:ATLAS or collaboration:CMS or collaboration:LHCb or collaboration:FASER or collaboration:MoEDAL)` (0)
- `abstracts.value:"quirk" and tc t`, `abstracts.value:"quirks" and tc t` (2 generic old theses)
- `fulltext:"quirks" and collaboration:CMS` (2405.13778, 2106.10509, 1210.2311 = model context); `... collaboration:ATLAS` (2104.03050, 1309.3230, 1112.3580); `... collaboration:LHCb` (0); `fulltext:"quirk" and (collaboration:CMS or collaboration:ATLAS) and date > 2023` (0)
- `abstracts.value:"kinked track" and date > 2022` (1 unrelated pheno paper)
- `abstracts.value:"quirk" and (abstracts.value:"MATHUSLA" or "ANUBIS" or "CODEX-b" or "MAPP" or "MoEDAL")` → only 2311.15486
- `refersto:arxiv:...` syntax returned unrelated records (tool limitation); replaced by `cites <recid>`
- Citations (`cites`) of: 1614773 (1708.02243), 2836006 (2410.00269), 3105000 (2601.09023), 1516007 (1703.00912), 1763305 (1911.02223), 1704655 (1811.08903) → no ATLAS/CMS/LHCb collaboration citer except FASER 2607.26195 and ATLAS 2104.03050. Theses 1755360, 1760811 and 3193023 cite as context
- `(collaboration:OPAL or DELPHI or ALEPH or L3) and t "stable" and t "charged"` → OPAL hep-ex/0305031 (618779)
- `collaboration:CMS and (t stopped or t "out-of-time" or t "empty bunch")`; `collaboration:CMS and t "disappearing" and date > 2019`; `collaboration:CMS and (t "heavy stable charged" or ... ) and date > 2019`; `collaboration:CMS and t scouting and date > 2024`; `collaboration:ATLAS and (t "large specific ionisation" or t "disappearing" or t "stopped") and date > 2022`
- TDR lookup: `get 1819968 / 1614103 / 1819664` (full texts from the INSPIRE file store); `t "Data Acquisition and High Level Trigger" and collaboration:CMS` (only the 2002 TriDAS TDR); `reportnumber:CMS-TDR-022`, `reportnumber:CERN-LHCC-2021-007` (0) → **DAQ-HLT Phase-2 TDR not found on INSPIRE**; `t "Phase-2 Upgrade of the CMS Data Acquisition"` (CMS-CR-2021-076 proceeding); `collaboration:CMS and t "Phase-2 Upgrade" and (t DAQ or t "High-Level Trigger")` → 2211.03684
- Verification `get arxiv:` for 2503.20893, 2512.14942, 2604.16244, 2510.26260, 2211.03684, 2309.16823, 2601.20063, 2410.09164, 2502.06694, 1801.00359

**Full-text greps** (research/cache/pdf): 2607.26195 (Run 3/Run 4/FASER2); 2601.09023 (approved, Upgrade II, colour-neutral, Drell, Sec. 2-6); 2311.15486 (GeV reach lines, Λ range); 2404.13814 (FASER/FASER2 reach); 2510.26260 (timeline, quirks); 2604.16244 (luminosity, Run 4); 1703.00912, 1708.02243, 2404.13814, 2311.15486, 2601.09023, 2607.26195 ("LEP"); 1708.02243 (trigger, Table I, backgrounds); 1911.02223 (pile-up, App. A, timing); 1811.08903 (stopping); 2410.09164, 2601.20063, 2309.16823, 2502.06694, 1801.00359 (trigger, selection, background method, systematics); CMS L1 TDR (Tables 4.1 and 4.6, HSCP, scouting, standalone muons); Tracker TDR (Tables 3.1, 4.4, 9.1, 10.1, 12.5, 12.6, binary readout, stubs); MTD TDR (resolution, BTL/ETL coverage, Sec. 5.4.3).

**Web** (WebSearch/WebFetch):
- "ATLAS quirks search non-helical tracks inner detector 2026" → SLAC Confluence "Quirks" snippet; no ATLAS note
- WebFetch confluence.slac.stanford.edu/.../Quirks → empty body
- "indico LLP workshop 2025 quirks tracking talk"; WebFetch indico.cern.ch/event/1441321/timetable/?print=1 → no quirk talk at LLP2025
- "LLP2026 sixteenth workshop ... timetable" → event 1592699; full timetable not retrieved
- "quirk OR quirks CMS PAS OR ATLAS-CONF OR thesis non-helical tracking HL-LHC 2025 2026 cds.cern.ch" → none
- curl to cds.cern.ch search → blocked by bot challenge (Anubis), so **CDS not searched**
- "FASER2 Forward Physics Facility approval 2026 CERN Research Board"; "Forward Physics Facility approved OR approval OR LHCC 2026"; "European Strategy update 2026 Council Forward Physics Facility FASER2 recommendation HL-LHC" → no approval found; Strategy adopted 22 May 2026 (FPF wording not retrieved)
- "FASER Run 3 2025 2026 data taking luminosity plans quirks extension 2026 run" → 2604.16244; Liverpool slides (WebFetch PDF + pdftotext): 333 fb-1, Run 4 approved, ~770 fb-1 projected
- "MATHUSLA ANUBIS CODEX-b status 2026 approval HL-LHC LHCC" → proposed only (2025 snapshots)


**ATLAS code trail (Sec. 1.0), 2026-10-07:**
- `gh api repos/burzynski-lab/quirk-tracking` (metadata, contents, README.md, PLAN.md, quirks/prep_quirks.py, commits)
- `gh api repos/burzynski-lab/quirkviz` (README, commits)
- `gh api users/burzynski-lab/repos`; `gh api orgs/burzynski-lab`; READMEs of displaced-observables, prism, svej-benchmarking, hepattn (no further quirk/ITk statements)
- GitLab API `projects/atlas%2Fathena/repository/commits?path=Simulation/G4Extensions/Quirks`; `merge_requests?search=quirk`; `repository/tree?path=InnerDetector/InDetGNNTracking/src`; raw `DumpObjects.cxx` (Pixel/SCT first, ITk fallback)
- INSPIRE `a Burzynski, Jackson and date > 2023`; `a Burzynski, Jackson and not collaboration:ATLAS`; `a Vessella`; `a Corpe, Louie and date > 2024 and not collaboration:ATLAS` (2609.16156 composite DM, not quirks)
- Web: "Burzynski quirks ATLAS search Oklahoma Corpe Vessella"; "quirk ATLAS Geant4 simulation inner detector search 2026 indico talk" (found the SLAC Confluence page 94178588 "Project Description - A Search for Quirks at the LHC")

**Not done / gaps:** CDS internal and public notes (blocked); CMS/ATLAS twiki public-results pages for EXO/LLP Phase-2 projections (FTR notes) were not browsed; CTD/Connecting-the-Dots and BOOST/LHCP 2024-26 indico agendas were not parsed (time); ATLAS TDAQ/ITk/HGTD numbers were not extracted; the CMS DAQ-HLT TDR itself was not read (proceeding used instead).

## Appendix B. Reference table (all IDs; location used)
| ID | INSPIRE recid | What | Location used |
|---|---|---|---|
| arXiv:2607.26195 | 3184325 | FASER first quirk search, 186 fb-1 | abstract; Fig. 4-5; p.5 (systematics) |
| arXiv:2604.16244 | 3146381 | FASER latest results (Moriond 2026) | p.1 (>311 fb-1); Sec. 5 (Run 4 approval) |
| indico.ph.liv.ac.uk event 2385, FASER_LivHEP.pdf | - | FASER talk, spring 2026 | slide text: 333 fb-1, Run 4 approved, ~770 fb-1 |
| arXiv:2404.13814 | 2779435 | FASER/FASER2 quirk timing projections | Sec. 6 (FASER Run-3 200/400 GeV); Conclusions (FASER2 1000/1300 GeV) |
| arXiv:2510.26260 | 3075256 | FPF Letter of Intent / CDR | abstract; Fig. 4 discussion (Run 5, 2036); quirk panel |
| arXiv:2601.09023 | 3105000 | LHCb VELO quirk proposal (coloured (3,1)_{2/3}) | Sec. 2 (FASER2 not approved), Fig. 2, Sec. 6 |
| arXiv:2311.15486 | 2726646 | Far-detector quirk sensitivities | Fig. 9-10 text; Summary |
| arXiv:2503.20893 | 2904973 | MATHUSLA CDR (MATHUSLA-40) | title (status context) |
| arXiv:2512.14942 | 3093520 | ANUBIS / proANUBIS | title (status context) |
| arXiv:1703.00912 | 1516007 | Farina-Low HSCP/monojet recast | Table II (via Gate-4); citers checked |
| arXiv:1708.02243 | 1614773 | Knapen et al., coplanar hits | Sec. III B (trigger), Sec. IV (backgrounds), Table I |
| arXiv:1911.02223 | 1763305 | Li et al., energy-loss quirk search (CMS-like EOM) | Sec. III-IV (v_T ~ 0.1, 10-20 ns), App. A (10⁻² fb) |
| arXiv:1811.08903 | 1704655 | Evans-Luty, stopping quirks | Fig. 2, Fig. 6, Sec. 5 |
| arXiv:1801.00359 | 1645630 | CMS stopped particles 2015-16 | Sec. 3.1, 6; Tables 4, 5, 6 |
| arXiv:2410.09164 | 2840007 | CMS HSCP dE/dx (CMS-EXO-18-002) | Sec. 5 (Table 2), 6.1-6.2 (Eq. 8-9), 7 |
| arXiv:2601.20063 | 3112517 | CMS HSCP with L1 scouting (CMS-EXO-25-010) | Sec. 3, 6 (Table 1), 7, 8 (Table 2) |
| arXiv:2309.16823 | 2705044 | CMS disappearing tracks (CMS-SUS-21-006) | Sec. 3, 6, 8.1-8.2, 9 (Table 7) |
| arXiv:2502.06694 | 2878503 | ATLAS dE/dx + ToF, 140 fb-1 | Sec. 5.2, 5.3, 5.5 |
| hep-ex/0305031 | 618779 | OPAL stable charged particles, 130-209 GeV | abstract (102.0 GeV) |
| arXiv:1008.3547 | - (via Gate-4) | D0 quirks | abstract |
| CERN-LHCC-2020-004 / CMS-TDR-021 | 1819968 | CMS Phase-2 L1 TDR | Sec. 1.3.2.1; Sec. 3.3.5 item 4 (p.117); Table 4.1 (p.210-211); p.209; Table 4.6 |
| CERN-LHCC-2017-009 / CMS-TDR-014 | 1614103 | CMS Phase-2 Tracker TDR | Sec. 2 (stubs, \|η\|≈4); Tables 3.1, 3.2, 4.4, 9.1, 10.1, 12.5, 12.6; binary-readout text |
| CERN-LHCC-2019-003 / CMS-TDR-020 | 1819664 | CMS MTD TDR | Ch. 1-2 (30-40 → 50-60 ps; BTL \|η\|<1.48, r = 1148-1188 mm; ETL 1.6-3.0); Sec. 5.4.3 |
| arXiv:2211.03684 | 2177374 | CMS Phase-2 HLT (summarises DAQ-HLT TDR) | Table 1, Table 2, Sec. 2-3 |
| INSPIRE 3110965, 3157038, 3065059, 2867485 | as listed | CMS L1 scouting Phase-2 system papers | titles only |
| INSPIRE 2091130, 2091129 | as listed | ATLAS ITk Pixel TDR, HGTD TDR | not read (competition context) |
| arXiv:2405.13778, 2106.10509, 1210.2311 | 2789267, 1869502, 1189819 | CMS papers mentioning quirks (context only) | INSPIRE fulltext hits |
| arXiv:2104.03050 | 1856547 | ATLAS stopped-LLP search | via Gate-4 |
| INSPIRE 1755360, 1760811, 3193023 | - | Theses citing quirk papers (Carney, Adersberger, Uecker) | abstracts only |
| github.com/burzynski-lab/quirk-tracking | - | ATLAS quirk-search ML pair finder (OU) | README, PLAN.md, prep_quirks.py, commit log (2026-09-09 to 09-15) |
| github.com/burzynski-lab/quirkviz | - | ATLAS quirk simulation event displays | README (TRT option, defaults 500 GeV / 400 eV) |
| gitlab.cern.ch/atlas/athena MRs "Fix quirk simulation" (2026-08-25), "More fixes for G4 quirks" (!90520, 2026-08-31) | - | Athena G4 quirk package fixes, target 24.0 | MR descriptions via GitLab API |
| gitlab.cern.ch/atlas/athena InnerDetector/InDetGNNTracking/src/DumpObjects.cxx | - | GNN4ITk dumper (supports the Run-3 ID and ITk) | lines ~99-127 |
| confluence.slac.stanford.edu/spaces/Atlas/pages/94178588 | - | SLAC "A Search for Quirks at the LHC" project page | search snippet only |
| confluence.slac.stanford.edu/spaces/Atlas/pages/100501546/Quirks | - | SLAC ATLAS "Quirks" page | search snippet only (content unreadable) |
| indico.cern.ch/event/1441321, /event/1592699 | - | LLP2025, LLP2026 | LLP2025 timetable parsed; LLP2026 not fully |
