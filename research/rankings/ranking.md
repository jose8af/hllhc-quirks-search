# Ranking of the ten fully reviewed candidates (Gate 5, arbiter)

Date: 2026-10-06. Inputs: Gate 3 adversarial reviews (`reviews/adversarial/gate3_batch*.md`), Gate 4 experimental, feasibility and theory reviews (`reviews/{experimental,feasibility,theory}/<id>.md`), and `candidates/gate4_targets.json`. Machine-readable version: `rankings/ranking.json`. Every reference ID below was checked against INSPIRE (`reports/citation_audit.json`).

**This ranking is decision support. It does not choose for you.**

## Bottom line

After a broad search (74 candidate directions, 27 adversarial reviews, 10 full Gate 4 reviews), **no candidate survives intact**. Every one was narrowed, most often by a CMS/ATLAS result that the scouts missed. Two candidates still have a gap that needs a new ATLAS/CMS analysis, not just a reinterpretation (Tier A: C001, C005). Five are worth a recast, feasibility or projection study first (Tier B). Three are weak (Tier C). None of the surviving gaps is new phenomenology: in every case a published pheno study already proposes the analysis. What is left to contribute is a **novel experimental analysis** or projection.

## Scoring key

Criteria are scored 0-5: TI theoretical importance; PR phenomenological richness; EN experimental novelty; HL HL-LHC relevance; FE experimental feasibility; SI potential sensitivity improvement; SD signature distinctiveness; LG current literature gap; TR theoretical robustness; PI potential publication impact.

**Cap rule.** EN and LG are capped at 2 whenever any reviewer found coverage that leaves only a recast, reinterpretation or projection. The cap was applied to C044, C015, C040 and C066.

**How the order was set.** The veto check (is there a covering result in the relevant region?) comes first, then judgement. The sum is shown but is not the ranking key.

## Table

| Rank | ID | Tier | TI | PR | EN | HL | FE | SI | SD | LG | TR | PI | Sum/50 | Conf. | Cap | Surviving gap (one line) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C001 | A | 3 | 4 | 4 | 4 | 2 | 3 | 5 | 4 | 3 | 4 | 36 | Medium | no | ATLAS/CMS coplanar non-helical-track search, EW quirks, m_Q>~180 GeV, Lambda~0.3-30 keV |
| 2 | C005 | A | 3 | 4 | 3 | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 32 | Medium | no | Higgs-portal hadronic dark showers, c*tau 1-100 mm in tracker, VH-tagged multi-DV (CMS side) |
| 3 | C019 | B | 4 | 4 | 3 | 4 | 3 | 3 | 5 | 3 | 3 | 3 | 35 | Medium | no | Same-sign / charge-2-parent displaced vertex from long-lived H++ (recast CMS 2110.04809 first) |
| 4 | C044 | B | 4 | 4 | 2 | 4 | 4 | 3 | 4 | 2 | 3 | 3 | 33 | Medium | yes | Dedicated TT->6t search above ~1.6 TeV (recast already 1.65 TeV); SSL+photon X5/3 |
| 5 | C015 | B | 3 | 3 | 2 | 4 | 4 | 3 | 4 | 2 | 2 | 2 | 29 | Medium | yes | t->qa, light ALP in HCAL/MS: add top-decay signal to existing lepton-triggered LLP searches |
| 6 | C051 | B | 3 | 3 | 3 | 3 | 4 | 2 | 3 | 3 | 3 | 3 | 30 | Medium | no | Unfolded A5-A7 / l=3 null tests above Z peak; sin2theta running (PDF-limited) |
| 7 | C003 | B | 3 | 4 | 3 | 3 | 2 | 2 | 3 | 3 | 2 | 3 | 28 | Low | no | Isotropic displaced hadronic SUEP (no PV handle); prompt-SUEP HL projection |
| 8 | C008 | C | 2 | 3 | 3 | 2 | 3 | 2 | 4 | 3 | 2 | 3 | 27 | Medium | no | Photon-enriched SVJ (Run-3-type); photon-ISR benchmark excluded by ATLAS 2403.08547 |
| 9 | C040 | C | 3 | 2 | 2 | 4 | 3 | 2 | 2 | 2 | 3 | 2 | 25 | Medium | yes | Collaboration HL projection of compressed direct stau (ATLAS 2609.37215 already did the analysis) |
| 10 | C066 | C | 2 | 2 | 2 | 3 | 3 | 1 | 2 | 2 | 4 | 2 | 23 | Medium | yes | e/mu + c-tag resonant LQ = flavour-rotation reinterpretation of existing results + HL projection |

## Why the order differs from the sums

- **C019 (sum 35) is ranked below C005 (sum 32) and placed in Tier B.** C019's high sum comes from its distinctive signature and its motivation (type-II seesaw). But a charge-agnostic CMS displaced-lepton search (2110.04809) may already cover part of its displaced regime, and nobody has checked. That makes a recast the necessary first step. C005's surviving region has no such ambiguity: the only overlapping results are for a different signal topology (two-body H->SS).

- **C001 is ranked first despite FE = 2.** It is the only candidate with no covering ATLAS/CMS result and no visible sign of being pre-empted. The low feasibility score is a cost, not a veto, and the right first step is a detector-level feasibility study.

- **C051 (sum 30) is ranked below C015 (sum 29).** C051 is a precision measurement whose BSM leverage the reviewers judged marginal: QCD-limited for A0-A2, no SM-level sensitivity for A5-A7 above the peak, and a PDF-limited running measurement. C015 is a cheap extension that would close a defined parameter region.

- **C008 (sum 27) is in Tier C.** Its photon-ISR half is excluded through visible Z' decays. Its photon-enriched half is a Run-3 idea with a weak HL-LHC-specific case and plausible pre-emption.

## Per-candidate justification

### 1. C001: Quirks: coplanar non-helical tracks from EW-charged quirks (mesoscopic string regime) (Tier A, confidence Medium)

- **Status labels:** proposed-not-searched (ATLAS/CMS), LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis.
- **Surviving gap:** Central-detector ATLAS/CMS search for coplanar, non-helical hit patterns from colour-neutral EW-charged quirks with m_Q > ~180 GeV and Lambda ~0.3-30 keV (stated 0.1-100 keV is too wide: >30 keV gives a single straight HIP-like track; <~300 eV is covered by the HSCP recast).
- **Veto check:** No covering search: FASER 2607.26195 (forward, <=179 GeV at 10 keV) is the only LHC quirk search; HSCP/monojet recast 1703.00912 gives no bound for (1,1)_-1 at 1 keV.
- **Justification:** All four reviews agree that no ATLAS/CMS quirk search exists (FASER 2607.26195 is the only LHC-experiment result; 2606.30760 and 1903.04497 state no dedicated LHC searches; 1812.07831 has no quirk projection). The phenomenology is already published (1708.02243 coplanar-hit method, 2410.00269 GNN tracking), so the novelty is a novel experimental analysis, not novel phenomenology. The signature is the most distinctive in the set (two coplanar, mutually curving, slow, ~2x-ionising tracks; 1708.02243). Feasibility is the weakest point (2/5): no study exists at PU 140-200; a Z(nunu)+jets+pileup coplanar background of ~1e-2 fb already at mu=50 (1911.02223) means 'background-free' is unproven; the only trigger is ISR-MET with ~10% efficiency (1708.02243) and the Phase-2 L1 track finder assumes helices (2110.02826). Luminosity buys only ~+200 GeV in mass (feasibility reviewer ESTIMATE). FASER2/FPF (2404.13814) and LHCb VELO (2601.09023) compete for the same (m_Q, Lambda) plane, but are not approved/running at the relevant level. Motivation is signature-driven (keV Lambda is log-flat natural, 0805.4642) and a discovery would imply low reheating temperature (2512.20696). Ranked first on judgement because it is the only candidate whose gap is a genuine new ATLAS/CMS analysis with no covering result and no visible pre-emption, despite the lowest feasibility score.
- **Disagreements adjudicated:**
  - Lambda window: target said 0.1-100 keV; experimental and theory reviewers independently narrow to ~0.3-30 keV. Adopted the narrower window.
- **Key references:** arXiv:2607.26195, arXiv:1703.00912, arXiv:1708.02243, arXiv:2410.00269, arXiv:1911.02223, arXiv:2404.13814, arXiv:2601.09023, arXiv:0805.4642, arXiv:2512.20696, arXiv:2110.02826, arXiv:1903.04497, arXiv:2606.30760

### 2. C005: Higgs-portal dark showers with hadronic GeV dark mesons decaying in the tracker (multi-DV, VH/VBF tags) (Tier A, confidence Medium)

- **Status labels:** constrained-but-region-open, searched-limited-regime, LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis.
- **Surviving gap:** Hadronic Higgs-portal dark showers with c*tau ~1-100 mm (tracker) and m ~5-20 GeV (natural core), in lepton-tagged VH (robust trigger) and, with a Phase-2 displaced L1 seed, ggF/VBF; multi-DV counting. CMS-side; ATLAS has a prospect study (INSPIRE 3201494).
- **Veto check:** Not vetoed: CMS MDS 2402.01898 covers Higgs-portal dark showers only at long c*tau (muon system, ggF); CMS 2409.10806 and ATLAS 2107.06092 cover the tracker region only for two-body H->SS (m_a >= 16 GeV for ATLAS ZH). A recast of these could close part of the gap.
- **Justification:** The adversarial review killed the scout's headline ('dark pions above a few GeV largely unconstrained', from 2203.09503) with CMS 2402.01898, which already sets Higgs-portal dark-shower limits down to B ~2e-3 for five decay portals; the theory reviewer adds that the Snowmass quote referred to flavour bounds on t-channel models. What survives is the short-lifetime, tracker-contained, hadronic regime: CMS 2409.10806 and ATLAS 2107.06092 probe the same volume but only for two-body H->SS, and no official result interprets tracker DVs in a many-LLP dark-shower model. A pheno HL-LHC projection exists (2512.24814), so this is a novel experimental analysis only. The feasibility reviewer finds that projection optimistic (no pileup, LO bbbar background only, a 70/40 GeV dijet trigger that is not a realistic Phase-2 path, no systematics); the realistic route is VH(lepton), giving O(100) selected events at B=1e-3 and 3 ab-1 (ESTIMATE from 1902.00134 cross sections), i.e. reach ~1e-3, not 1e-4. The theory reviewer's evaluation of the lifetime bounds in 2103.01238 places the natural region at m >~ 4-8 GeV for c*tau 1-100 mm; the 2-4 GeV mm corner needs tuning. Risks: ATLAS pre-emption (INSPIRE 3201494 is a Delphes prospect, not an approved analysis) and large dark-hadronisation uncertainty (2203.09503, 2505.03058).
- **Disagreements adjudicated:**
  - Scout/Snowmass 'largely unconstrained' claim overturned by CMS 2402.01898 (adversarial) and reinterpreted by theory reviewer as a flavour-bound statement.
  - 2512.24814 reach O(1e-4): accepted only as an upper bound; feasibility reviewer's critique (no PU, LO bkg, unrealistic trigger) is documented in the source itself and is adopted.
  - Mass range: target 2-20 GeV; theory reviewer's evaluation of 2103.01238 Eq. 4/15 (their own numerical evaluation of published formulae) shows 2-4 GeV at mm lifetimes is unnatural. Adopted as a motivation caveat, not an exclusion.
- **Key references:** arXiv:2402.01898, arXiv:2409.10806, arXiv:2107.06092, arXiv:2512.24814, arXiv:2203.09503, arXiv:2103.01238, arXiv:2110.10691, arXiv:2307.04847, arXiv:1902.00134, INSPIRE:3201494, INSPIRE:2908980, arXiv:1705.04321, arXiv:2505.03058

### 3. C019: Doubly charged scalars: displaced (charged-parent, same-sign) DVs; compressed cascades; hadronic taus (Tier B, confidence Medium)

- **Status labels:** proposed-not-searched (displaced same-sign DV), indirectly-covered/not reinterpreted, searched-limited-regime (tau_h), theory-explored-untested (compressed). **Novelty kind:** experimental-analysis.
- **Surviving gap:** (i) Long-lived H++ (c*tau ~0.1-100 mm) giving a charge-2 parent track ending in a same-sign/high-mass DV; TeV-scale only in the fermiophobic (GM-like) case, 100-150 GeV in neutrino-mass type-II. (iii) tau_h H++ channels with full Run 2/3 and HL data. (ii) compressed soft same-sign leptons is systematics-limited (~1/5 feasibility).
- **Veto check:** Not vetoed, but a recast is required first: CMS 2110.04809 (displaced leptons, no charge or vertex requirement) and ATLAS 2410.16835 have partial acceptance that nobody has quantified; ATLAS 2601.05664 requires opposite charge.
- **Justification:** Prompt W+W+ (ATLAS 2101.11961) and stable/HSCP (2303.13613) parts die. The adversarial review's key argument (the only displaced-dilepton vertex search requires opposite charge, 2601.05664) is correct but incomplete: the experimental reviewer found CMS 2110.04809, which has no charge requirement, so the displaced regime is indirectly covered to an unknown degree. Phenomenology 2608.27251 argues those searches 'cannot be reliably reinterpreted' and projects ~0.01 fb sensitivity at 3 ab-1, but with statistically meaningless background MC (weights ~1e7) and an ideal displaced trigger (feasibility review). The signature (charge-2 parent + same-sign DV) is highly distinctive and near background-free, so reach scales ~1/L; cross sections are 1.60 fb at 500 GeV and 0.15 fb at 800 GeV (2608.27251 Table 1). Theory: type-II seesaw is well motivated (4/5), but long-lived Yukawa-coupled H++ exists only for M ~100-150 GeV (1808.00943), and the TeV reach needs the fermiophobic assumption, which drops the neutrino-mass link. The tau_h channel is a legacy Run-2/3 gap (CMS only 12.9 fb-1, INSPIRE 1510936; ATLAS e/mu only, 2211.07505), and a CMS-group MSc thesis (INSPIRE 3063898) suggests internal work. Tier B because the decisive first step is a recast of 2110.04809/2410.16835.
- **Disagreements adjudicated:**
  - Adversarial/target: 'ATLAS displaced-dilepton search requires opposite charge => no coverage'. Experimental reviewer: CMS 2110.04809 is charge-agnostic => partial coverage. Adjudication: both statements are true; the gap is 'not reinterpreted', so a recast precedes any claim.
  - CMS 12.9 fb-1 tau tau limit quoted as 535 GeV (2305.06889) vs 396 GeV (thesis INSPIRE 3063898): unresolved, marked UNVERIFIED; does not affect ranking.
- **Key references:** arXiv:2608.27251, arXiv:2110.04809, arXiv:2601.05664, arXiv:2410.16835, arXiv:2211.07505, arXiv:2101.11961, arXiv:2303.13613, arXiv:1808.00943, arXiv:2410.19561, arXiv:2603.15882, arXiv:2305.06889, INSPIRE:1510936, INSPIRE:3063898, INSPIRE:2084511, arXiv:2608.03988

### 4. C044: VLQ exotic decays to new scalars: dedicated TT -> (tS0)(tS0) -> 6t; X5/3 -> t phi+ (W+ gamma) (Tier B, confidence Medium)

- **Status labels:** searched-limited-regime, indirectly-covered (recast to 1.65 TeV). **Novelty kind:** experimental-analysis (optimisation of existing multilepton strategy).
- **Surviving gap:** A dedicated high-S_T multilepton/multi-b search optimised for TT -> 6t above ~1.6 TeV (recast already excludes 1.65 TeV at BR=1, 2609.00127), and an SSL + hard photon channel for X5/3 -> t W+ gamma (recast 1907.05894 says it is already constrained at the level of the standard channel).
- **Veto check:** Not vetoed in mass reach above ~1.6 TeV, but the region below is covered by recasts of SS2L/3L searches (2609.00127); diphoton S modes are directly covered (ATLAS 2607.28381, CMS 2610.03489); X5/3 -> tH+ covered (CMS-PAS-B2G-24-005).
- **Justification:** The adversarial review corrected the scout's physics (X5/3 cannot decay to t + neutral a; it is t phi+) and found that diphoton and charged-Higgs exotic channels are already searched (ATLAS 2607.28381, CMS 2610.03489, CMS-PAS-B2G-24-005). The recasting atlas 2609.00127 states no direct 6t search exists but recasts it to 1.65 TeV (BR=1) or 1.30 TeV (BR 50%), so experimental novelty and literature gap are capped at 2. The case for HL-LHC is real but incremental: above ~1.6 TeV the 6t region is near background-free and reach scales ~1/L, but sigma(TT) is ~0.13 fb at 2 TeV (derived from 2508.14960) and an effective BR of 25% leaves ~1 signal event (feasibility ESTIMATE). The 2.5 TeV 6t discovery claim of 1812.11286 is stat-only Delphes. Theory motivation is good (top-philic pNGB generic in gauge-fermion composite Higgs; 2609.00127) but every rate depends on BRs. Unchecked: CMS 2606.30862 (BSM in 3t/4t events) may already populate the 6t signal regions.
- **Disagreements adjudicated:**
  - Theory reviewer could not verify the content of CMS-PAS-B2G-24-005 (marks the tH+-only claim UNVERIFIED); experimental and feasibility reviewers read its public page/abstract. Adopted the E/F reading, flagged as abstract/public-page level.
- **Key references:** arXiv:2609.00127, arXiv:1907.05894, arXiv:2607.28381, arXiv:2610.03489, INSPIRE:3157006, arXiv:1812.11286, arXiv:2508.14960, arXiv:2203.13753, arXiv:1908.07524, arXiv:2506.08825, arXiv:2402.13808, arXiv:2606.30862

### 5. C015: Long-lived light ALPs from exotic top decays t -> q a (HCAL / muon system, lepton-triggered ttbar) (Tier B, confidence Medium)

- **Status labels:** searched-limited-regime, constrained-but-region-open (as interpretation), LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis (signal reinterpretation / added signal regions).
- **Surviving gap:** t -> q a with m_a ~1-35 GeV decaying in HCAL or muon system, presented model-independently as BR(t -> qX) vs (m_X, c*tau). ATLAS 2403.15332 covers only m_a = 40, 55 GeV in the ID.
- **Veto check:** Partial coverage: ATLAS 2403.15332 directly covers m_a 40-55 GeV (ID); ATLAS CalRatio+W 2407.09183 has a lepton-triggered selection that a t->qa event could pass but treats ttbar as background. Gap is largely an interpretation of existing analyses (rule 4).
- **Justification:** ATLAS 2403.15332 probes long-lived t -> aq directly (m_a = 40, 55 GeV, BR > 0.1% excluded for 1.6-130 mm), contradicting the scout. The surviving light-mass HCAL/MS region is, on the adversarial, experimental and feasibility reviewers' own wording, best met by adding a top-decay signal to ATLAS CalRatio+W/Z (2407.09183), the ATLAS ID-DV 1-lepton region and a lepton-triggered CMS MDS selection; a wholly new trigger is not needed, so the cap applies. Feasibility is high (4/5): ~2.4e9 ttbar at 3 ab-1 (ESTIMATE) with a lepton trigger from the other top; but the HCAL category is background-limited, and the 1e-7 to 1e-8 reach of 2202.09371 assumes zero background. Theory: the visible decay pattern for 1 GeV < m_a < 2m_c differs between 2202.09371 and 2110.10698, so the displaced mu mu / gamma gamma sub-target is not robust; prompt a -> gamma gamma needs an extra photon coupling (a different model). The theory reviewer's argument that generic UV flavour structures imply BR(t->qa) <~ 1e-6-1e-8 for cm-m lifetimes is the reviewer's own derivation, not in the literature; it is recorded as a caveat (it lowers the theoretical-robustness score but does not change the recommended model-independent presentation).
- **Disagreements adjudicated:**
  - Coupling-structure bound (FN positive-semidefinite c_uR => small BR) is the theory reviewer's own derivation (marked as such in reviews/theory/C015.md). Not used as evidence; kept as a stated caveat.
  - Visible-channel BRs for 1 GeV < m_a < 2m_c: 2202.09371 (hadrons dominate) vs 2110.10698 (leptons dominate). Literature disagreement, unresolved; displaced mu mu/gamma gamma sub-target downgraded.
- **Key references:** arXiv:2403.15332, arXiv:2202.09371, arXiv:2404.06126, arXiv:2407.09183, arXiv:2402.01898, arXiv:2301.03902, arXiv:2110.10698, arXiv:2101.07803, arXiv:2306.08686

### 6. C051: High-mass Drell-Yan angular coefficients (A0-A2, T-odd A5-A7, l=3 harmonics) and sin2theta_W running (Tier B, confidence Medium)

- **Status labels:** one-observable-not-another, well-covered (high-mass A_FB part). **Novelty kind:** experimental-analysis (precision measurement).
- **Surviving gap:** Unfolded, phi-dependent A_i above the Z peak vs m_ll and pT_ll, narrowed (theory reviewer) to the null tests A5-A7 and the l=3 basis of 2003.11615; A0-A2 off-peak only as a QCD test. Experimental MSbar sin2theta_W(mu) extraction is PDF-limited and degenerate with contact interactions.
- **Veto check:** Partial veto: high-mass A_FB and pT/y-integrated A0 already measured (CMS 2202.12327); that sub-idea is dead. Full A0-A7 only at the Z peak (CMS 2604.25678, ATLAS 1606.00689).
- **Justification:** The scouts missed CMS 2202.12327 (A_FB and A0 vs mass above 170 GeV), which kills the A_FB part. What remains is a measurement gap: no full A0-A7 above 101 GeV and no A5-A7 off-peak. Value as a BSM probe is limited: SM Lam-Tung violation at the Z peak is O(0.1) and under-predicted by NNLO-matched MC (2604.25678), dipole operators are better constrained by the pT_ll spectrum (2412.13014), A0 is already systematics-limited in Run 2 (2202.12327 Table 3), and A5-A7 cannot be measured at SM level above the peak (feasibility ESTIMATE); the dim-8 A6/A7 projection 2511.19617 is stat-only and has EFT-validity questions. sin2theta running reaches ~2 sigma per high-mass bin at HL-LHC and is mostly an absolute cross-section measurement, PDF-limited (2302.10782). The theory reviewer notes the l=3 harmonics of 2003.11615 (omitted by the target) as the cleanest smoking gun. Low cost: clean dilepton trigger and existing machinery.
- **Disagreements adjudicated:**
  - Seed premise 'angular coefficients only at Z peak' overturned by CMS 2202.12327 (adversarial, confirmed by E/F/T).
- **Key references:** arXiv:2202.12327, arXiv:2604.25678, arXiv:1606.00689, arXiv:2511.19617, arXiv:2003.11615, arXiv:2412.13014, arXiv:2405.04069, arXiv:2302.10782, arXiv:1609.08157, arXiv:2512.05018

### 7. C003: Displaced, hadronic, isotropic SUEP (plus an HL-LHC projection of the prompt SUEP programme) (Tier B, confidence Low)

- **Status labels:** searched-limited-regime, constrained-but-region-open (displaced hadronic), LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis.
- **Surviving gap:** Isotropic soft displaced-track/vertex SUEP with c*tau ~1 mm to a few cm from ggF/VH mediators; all SUEP searches use PV-associated tracks and prompt signals. Plus a collaboration HL-LHC projection of prompt SUEP.
- **Veto check:** Prompt SUEP well covered (CMS 2403.05311, 2607.09621, 2604.05996; ATLAS 2605.20015); displaced muonic covered (CMS 2511.11888); metre-scale by MDS. CMS states displaced SUEP 'would result in an emerging jet signature' (2403.05311).
- **Justification:** All reviewers agree the displaced hadronic isotropic regime has no search and no recast, and that no HL-LHC SUEP projection exists (only truth-level trigger studies 2211.05720/2203.07314). But feasibility is poor (2/5): displacement removes primary-vertex association, the only demonstrated SUEP-vs-pileup handle, and soft tracks fall below the 2 GeV Phase-2 L1 track threshold (2211.05720 Sec. 2.2). Theory squeezes the natural region: m_D ~1-3 GeV gives c*tau >~ m (beyond the tracker; 2103.01238 Eq. 4/15), while m_D ~5-10 GeV at cm lifetimes gives only ~10-25 mesons from a 125 GeV mediator, overlapping C005; the Higgs tadpole issue (1612.00850 Sec. II.C) and a likely beam-dump-excluded long-lived A' route (2005.01515, overlap UNVERIFIED) add tension. Best pursued jointly with C005 (shared VH multi-DV strategy) rather than as a standalone search.
- **Disagreements adjudicated:**
  - Theory (displacement is the generic expectation for gluon/Higgs portals) vs theory-consistency (natural mm-cm high-multiplicity corner is squeezed): both from the same reviewer; adopted as 'motivated but narrow'.
- **Key references:** arXiv:1612.00850, arXiv:2403.05311, arXiv:2607.09621, arXiv:2604.05996, arXiv:2605.20015, arXiv:2511.11888, arXiv:2211.05720, arXiv:2203.07314, arXiv:2107.12379, arXiv:2103.01238, arXiv:2203.09503

### 8. C008: Photon-enriched semi-visible jets; photon-ISR-tagged low-mass Z' -> SVJ SVJ (Tier C, confidence Medium)

- **Status labels:** proposed-not-searched (SVJ-gamma), proposed-not-searched with partial indirect coverage (photon-ISR), LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis.
- **Surviving gap:** (i) SVJ-gamma: high neutral-EM-fraction jets with non-isolated photons, vetoed by existing CMS SVJ selections (f_gamma > 0.7 veto). (ii) photon-ISR low-mass SVJ survives only for B(Z'->chi chi) -> 1 and small g_q.
- **Veto check:** (ii) benchmark of 2409.04741 (g_q = 0.25) is excluded through its visible Z'->qq decays by ATLAS 2403.08547 (g_q < 0.06-0.1 for 200-650 GeV). (i) not covered.
- **Justification:** Lepton- and tau-enriched SVJ are taken (CMS 2608.05323; PAS INSPIRE 3136606), as is t-channel SVJ (ATLAS 2305.18037). For (i) the experimental reviewer confirms both CMS s-channel SVJ searches veto high photon-fraction jets (2112.11125, 2608.05323), so SVJ-gamma is proposed-not-searched (pheno 2407.08276). But it relies on an ad hoc second portal (ALP + vector-like lepton) with no independent motivation for BR_gamma, it is already testable with Run-2/3 data (the pheno claims Run-2 reach to 5 TeV), and removing the jet-ID cut readmits instrumental fakes; the HL-specific case is weak. For (ii) the theory reviewer shows the published benchmark is excluded through its visible decays (see disagreement). Pre-emption is plausible: the same authors' lepton/tau proposals became CMS searches, and a jet-ISR SVJ search is in a CMS thesis (INSPIRE 2751239).
- **Disagreements adjudicated:**
  - Photon-ISR (ii): adversarial and experimental reviewers call it proposed-not-searched; theory reviewer shows ATLAS 2403.08547 excludes the 2409.04741 benchmark (g_q = 0.25) through visible Z'->qq. The ATLAS bound (g_q < 0.06-0.1, B(qq)=1) is in the source; the reviewer's rescaling to B(qq)=0.53 (g_q <~ 0.08-0.14) is their own arithmetic, but g_q = 0.25 exceeds both. Adjudicated: benchmark excluded; only a reduced-rate corner survives.
- **Key references:** arXiv:2407.08276, arXiv:2409.04741, arXiv:2112.11125, arXiv:2608.05323, arXiv:2403.08547, arXiv:2505.01634, arXiv:2305.18037, INSPIRE:2751239, arXiv:1503.00009

### 9. C040: Compressed direct stau pairs (stau-bino coannihilation corridor): collaboration HL-LHC projection (Tier C, confidence Medium)

- **Status labels:** searched-limited-regime, LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis (projection only).
- **Surviving gap:** A collaboration-level Phase-2 projection for direct stau pairs with soft tau_h + ISR/VBF + MET. Physics-motivated and reachable overlap is roughly Delta m ~15-30 GeV, m(stau) ~100-200 GeV.
- **Veto check:** Not vetoed in reach, but the analysis concept is already executed by ATLAS 2609.37215 (Run 2+3, ISR channel, no combined exclusion) and CMS 1910.01185; CMS review 2510.17971 says compressed-stau analyses are in preparation. Surviving gap is a projection (rule 4).
- **Justification:** The adversarial review found that ATLAS 2609.37215 (Sep 2026) runs exactly this strategy (ISR-only exclusion 115 GeV at Delta m = 30 GeV; no combined exclusion; 2.1-2.4 sigma local deviations) and that the g-2 motivation has gone (2505.21476). The HL-LHC YR projections cover only Delta m > 100 GeV (1812.07831 Sec. 2.3), so the open item is the projection itself; pheno projections exist (2403.18991, 2308.05723, 1704.04669). Feasibility 3/5: current searches are statistics-limited, so ~15x luminosity is real, moving the Delta m ~30 GeV exclusion from ~115 to ~150-200 GeV (feasibility ESTIMATE), with little reach below Delta m ~15 GeV and fake-tau systematics at PU 200 as the cap. Novelty and gap capped at 2 (projection-only).
- **Disagreements adjudicated:**
  - Delta m window: target and feasibility use 5-60 GeV; theory reviewer (from 2308.05723) restricts the relic-motivated window to Delta m <~ 30 GeV (stau_L-like) and <~ 10 GeV (stau_R), noting that 30-60 GeV needs mixed LSPs excluded by LZ for m_chi <~ 300 GeV, and that the ATLAS excess (Delta m = 50) lies outside the pure-bino strip. Feasibility finds little reach below Delta m ~15 GeV. Adjudication: both are evidence-based; the motivated-and-reachable overlap is only ~15-30 GeV, and the stau_R coannihilation strip (<~10 GeV) is effectively out of reach. This lowers the physics value of the projection.
- **Key references:** arXiv:2609.37215, arXiv:1910.01185, arXiv:1812.07831, arXiv:2403.18991, arXiv:2308.05723, arXiv:1704.04669, arXiv:1606.08878, arXiv:2505.21476, arXiv:2601.06358, arXiv:2510.17971, INSPIRE:1704284

### 10. C066: Resonant lepton-PDF single leptoquark with charm-tagged jets; collaboration HL projection (Tier C, confidence Medium)

- **Status labels:** one-observable-not-another, indirectly-covered, LHC-not-projected-to-HL. **Novelty kind:** experimental-analysis (reinterpretation + projection).
- **Surviving gap:** e/mu + c-tagged jet category in resonant lepton-quark fusion; in practice a flavour-rotation reinterpretation of the existing light-jet results plus a collaboration HL-LHC projection.
- **Veto check:** Indirectly covered: ATLAS 2507.03650 states u/c couplings are kinematically indistinguishable and reinterpretable by flavour rotation; CMS 2608.28377 states s/c sensitivity is bracketed by its u and b benchmarks. Third-generation sub-ideas (b tau, beta_R, excess follow-up) die (ATLAS 2503.19836, CMS 2208.02717, 2308.06143, 2308.07826).
- **Justification:** The third-generation bundle dies (ATLAS 2503.19836 excludes the CMS 2.8 sigma b-tau benchmark; beta_R benchmarks in CMS 2208.02717; tau-quark scattering in CMS 2308.06143). The surviving c-tag idea is already indirectly covered (ATLAS 2507.03650 Sec. 1; CMS 2608.28377 Sec. 1), and the review 2505.08738 that listed charm as an opportunity predates both searches. The c-mu rate is ~28x below u-mu at 2.5 TeV (2012.02092 Table 1, feasibility ESTIMATE), so matching the u reach needs y_c ~3 (Gamma/M ~0.24, broad); TeV-scale c-tagging is inefficient and poorly calibrated. Motivation is weak (2/5: g-2 has faded per 2608.28377; no anomaly points to e/mu-c). Theory robustness is high (lepton PDFs known to <5%, 2005.06477). The most useful deliverable is a reinterpretation plus a collaboration HL projection of the existing channels.
- **Disagreements adjudicated:**
  - Misquote corrected: the target text said 2005.06475 gives an 'HL reach of ~5.7 (4.2) TeV'. Experimental, feasibility and theory reviewers independently found that these are the masses up to which the HL resonant bound would surpass the atomic-parity-violation (Q_W) bound for lambda_eu (lambda_ed), not a mass reach. Corrected throughout.
- **Key references:** arXiv:2507.03650, arXiv:2608.28377, arXiv:2005.06475, arXiv:2005.06477, arXiv:2012.02092, arXiv:2505.08738, arXiv:2503.19836, arXiv:2208.02717, arXiv:2308.06143, arXiv:2308.07826, arXiv:2012.11474

## Not ranked (insufficiently reviewed)

C017, C061, C009, C047, C048 and C021 had only a Gate 3 adversarial review. They had no independent theory, experimental or feasibility review, so they are not ranked alongside the ten above. See `TOP_CANDIDATES.md`, section 'Promising but insufficiently reviewed'.

## Caveats

- Coverage searches were INSPIRE title/abstract-level plus selective full-text reads; CMS/ATLAS internal work is invisible.
- Gate 4 reviews were single-pass (one opus reviewer per role); no second adversarial round on survivors (lean budget).
- Cross sections and yields marked ESTIMATE in reviews are reviewer back-of-envelope values.
- Rankings are decision support, not a decision.
