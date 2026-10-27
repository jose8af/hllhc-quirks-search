# T6: production mechanisms, model space and complementary signatures (beyond DY E Ē, N_IC = 2)

Author: T6 (Sonnet). Date 2026-10-07. Convention Λ ≡ √σ_string. All σ at 14 TeV, N_IC = 2 unless stated.
Code: `code/T6_production.py` (LO DY + photon-initiated, LHAPDF NNPDF31_nnlo_as_0118_luxqed, run with `/opt/miniconda3/envs/root_env/bin/python`; the pixi env has no lhapdf), `T6_table.py`, `T6_stopping.py`, `T6_annihilation.py`, `T6_coverage.py`.
Outputs: `figures/T6_xsec_table.txt` (raw LO table, 8 masses), `figures/T6_coverage.png`.
Validation of my LO DY code against `research/theory_signal_model.md` §2.3: E at 14 TeV, N_IC = 2, LO×K: 219 / 5.94 / 0.179 fb at 200 / 500 / 1000 GeV vs 220 / 6.11 / 0.197 (≤ 9 %, different PDF set). The W-mediated higgsino-proxy numbers also reproduce (L±L0 at 200 GeV: 0.93 pb LO per N_IC vs 1.01 pb from SUSY-WG tables quoted in §2.3).

## 1. Executive summary

1. **Photon-initiated production is a ~5 % correction, not a gap.** LUXqed γγ → EĒ adds 4.5 % (200 GeV), 4.6 % (500), 5.2 % (1000) to DY, and has no ISR (so is *less* than 5 % of the ISR-triggered sample). It is 18-21 % for |q| = 2 and ~40 % for |q| = 3. Verdict: NOT A GAP for the discovery analysis.
2. **Exclusive γγ → QQ̄ with PPS tags is real but small:** σ_excl(N_IC = 2, 0.01 < ξ < 0.2, S² = 0.8) = 0.55 / 0.012 / 1×10⁻⁴ fb at 200 / 500 / 1000 GeV, i.e. **≈ 35 produced events at 500 GeV, 3 ab⁻¹**, ≈ 370 at 300 GeV, ≈ 0 above 750 GeV. Against ≈ 330 events in the main tracker analysis at 500 GeV it is ~3 % of the statistics after any PPS efficiency. It is useful only as a clean post-discovery mass handle (M_X = 2m_Q + E_int measured to ~3 GeV), not for discovery. It also needs PPS-2, whose schedule is uncertain (see G-T6-1).
3. **Doublet L and triplet T are NOT tracker-quirk benchmarks.** Q± → Q0 π± has cτ ≈ 8 mm (doublet, ΔM = 341 MeV) or ≈ 6 cm (Y = 0 triplet, ΔM = 166 MeV). Quirks are slow (βγ ≈ 0.1-0.6) so decays occur at ≲ 5 mm and the pair becomes **neutral and invisible before the first pixel layer** (R = 3 cm). Rates are huge, though: total DY σ is ×14 (doublet) and ×37 (triplet) that of E, i.e. ≈ 84 fb (doublet, 500 GeV, N_IC = 2). The signature is monojet + soft displaced pions, Λ-independent. This is a compressed-higgsino-like recast, not a quirk-track search. Verdict: WORTH A CHECK as a separate monojet recast.
4. **Multi-charged singlet quirks:** σ ∝ q² exactly (×4.00, ×9.00 for |q| = 2, 3). The tracker plane-finder should reach ≈ 1.3 TeV for |q| = 2 (vs ≈ 1.15 TeV for |q| = 1), at the cost of a ×(2)^{1/4} higher Λ_min. ATLAS multi-charged limits (|q| = 2: 1060 GeV, DY+photon fusion [2303.13613]) cover only the *merged* straight-track regime (Λ ≳ 20-30 keV); I assess that as roughly "already excluded to ≈ 1.1 TeV" there (ESTIMATE, UNVERIFIED applicability). Multi-charged states inside SU(2) multiplets decay at the IP (cτ ≈ 0.2-1 mm) and are not useful.
5. **Stopped-pair annihilation is the most under-exploited complement (EXPLOIT / WORTH A CHECK).** Evans-Luty find 1-5 % of E′ pairs (400 GeV) stop in the |η| < 1 calorimeters, ~×3 for the full calorimeter and ~the same again in the yoke [1811.08903 Fig.2, Fig.6, Sec.5]. The stopped pair dissipates its internal energy in ≈ 0.07-0.3 µs (ESTIMATE, `T6_stopping.py`), then annihilates with ~2m_Q visible energy (40-80 % visible). ESTIMATE: **7-68 events at 500 GeV, 0.8-7 at 800 GeV, 0.2-2 at 1 TeV (3 ab⁻¹)** for f_stop = 1-6 %, with CMS-like 21 % empty-BX window, ε_reco 0.55. Reach for 3 events ≈ 0.65-0.9 TeV. It needs no ISR trigger, no tracker, and is nearly background-free with an E-threshold. The only experimental analogue to recast is CMS 1801.00359 (calorimeter ε_stopping = 0.054 for gluinos).
6. **Microscopic Λ (≳ 3 MeV):** the pair annihilates in vacuum before the first layer (L_ann ≈ 0.3 cm at 3 MeV, 9 cm at 1 MeV, 3.4 m at 0.3 MeV, ESTIMATE from E-L Eq.4.4 with ε_emit = 0.1). The S-wave BRs (ESTIMATE) give BR(ee + μμ) ≈ 18.5 %, BR(γγ) ≈ 3.4 %, BR(Zγ) ≈ 2 % at M = 2m_Q, so σ × BR(ee + μμ) = 1.1 fb at m_Q = 500 GeV and 0.24 fb at 700 GeV, against ATLAS dilepton limits of order 0.05-0.1 fb above 1.4 TeV [1903.06248 text: 0.014 fb at 6 TeV; the 1.4 TeV value is my UNVERIFIED reading]. **Existing dilepton/diphoton resonance searches therefore probably exclude m_Q ≲ 0.8-1 TeV for Λ ≳ 3 MeV**, beyond anything the tracker analysis reaches. The band Λ ≈ 0.1-3 MeV (displaced annihilation at 3 m - 10 km) has no dedicated search.
7. Cosmic-ray/telescope, beam-dump, MoEDAL, MATHUSLA, CODEX-b: killed (§6). Lepton colliders: only a future ≥ 2 TeV machine helps.

## 2. Table of production channels, σ(pp → pair) at 14 TeV, N_IC = 2, fb (ESTIMATE; DY: LO × K_DY = 1.110/1.158/1.254; photon channels: LO, no K)

Source: `figures/T6_xsec_table.txt` via `code/T6_table.py`. K_DY taken from theory_signal_model §2.3 (colour-singlet DY, spin independent). EPA = equivalent photon approximation, dipole form factors, gap survival S² = 0.8 (UNVERIFIED typical value; Harland-Lang et al. use SuperChic).

| Channel | m = 200 | m = 500 | m = 1000 |
|---|---|---|---|
| DY E (1,1)_{-1} fermion (benchmark; model-doc table: 220 / 6.11 / 0.197) | 219 | 5.94 | 0.179 |
| DY Ẽ scalar | 19.2 | 0.444 | 0.0105 |
| DY L⁻L⁺ (doublet, charged pair, γ/Z) | 584 | 15.3 | 0.455 |
| DY L⁰L̄⁰ (doublet, Z; invisible) | 572 | 14.2 | 0.415 |
| DY L^±L⁰ (doublet, W; net charge ±1) | 2060 | 54.7 | 1.73 |
| DY doublet total | 3220 | 84.2 | 2.60 |
| DY triplet Y = 0: T⁺T⁻ (two species) | 4190 | 106 | 3.12 |
| DY triplet Y = 0: T^±T⁰ (W) | 4120 | 109 | 3.47 |
| DY singlet |q| = 2 fermion | 876 | 23.8 | 0.716 |
| DY singlet |q| = 3 fermion | 1970 | 53.5 | 1.61 |
| γγ (LUXqed el+inel) → EĒ | 8.96 | 0.236 | 0.0075 |
| γγ (LUXqed) → ẼẼ* | 1.56 | 0.0447 | 0.0016 |
| γγ (LUXqed) → |q| = 2 pair | 143 | 3.78 | 0.120 |
| EPA elastic-elastic, all ξ, S² = 1 | 0.92 | 0.0258 | 8.7×10⁻⁴ |
| EPA el-el, PPS-2 (0.01 < ξ < 0.2 both), S² = 0.8 | 0.548 | 0.0118 | 9.8×10⁻⁵ |
| EPA el-el, PPS Run-3 (0.02 < ξ < 0.15), S² = 0.8 | 0.329 | 0.0072 | 1×10⁻⁶ |
| EPA semi-elastic (one proton intact), S² = 0.5 | 1.69 | 0.0476 | 0.0016 |

Ratios (per `T6_table.py`): γγ(LUXqed)/DY (E) = 4.5 / 4.6 / 5.2 % at 200 / 500 / 1000; doublet total/E = 14.7 / 14.2 / 14.6; triplet total/E = 38 / 36 / 37; L^±L⁰ / L⁺L⁻ = 3.5 / 3.6 / 3.8; |q| = 2 / |q| = 1 = 4.00; γγ/DY (|q| = 2) = 18-21 %.
Cross-check of the EPA code: scalar el-el for four degenerate sleptons at m = 120 GeV (all ξ, S² = 1) = 4 × 0.44 = 1.8 fb and 0.074 fb at 300 GeV, vs 0.8 fb and 0.03 fb quoted in [1812.04886 Sec.2, after lepton selection and SuperChic S²]. Ratio 2.2-2.5, plausibly the lepton pT > 5 GeV acceptance and S²; I treat the EPA numbers as good to a factor ~2.

## 3. Gap entries

### G-T6-1  Photon-initiated production (inelastic LUXqed and exclusive/PPS)
- **Current treatment:** none in the quirk literature. Photon-initiated slepton/chargino pairs with forward tagging: Harland-Lang, Khoze, Ryskin, Tasevsky [1812.04886; proceedings 1910.01703]. They quote σ(exclusive, 4 sleptons) = 0.03-0.8 fb for 300-120 GeV; FPD acceptance 0.02 < ξ < 0.15 ⇒ 250-1900 GeV central mass [1812.04886 Sec.1-2]; 2-3 signal events at 300 fb⁻¹ after cuts, with pile-up and semi-exclusive backgrounds comparable to signal [1812.04886 Sec.7, 1910.01703].
- **Why it might be a gap:** pT(QQ̄) ≈ 0 and zero hadronic activity, so a tagged exclusive event removes the ISR requirement (efficiency 10 %, [1911.02223 App.A]) and fixes M_X.
- **Quantitative:** (a) inelastic, `T6_production.py`: +4.5-5.2 % of DY for E; the photon component has no ISR, so < 5 % of the triggered sample. (b) Exclusive, PPS-2: see table; 35 events at 500 GeV, 370 at 300, 3.3 at 750 (before PPS efficiency, vertex-timing match at PU 200, and the unknown trigger). The PPS-2 EoI mass window is 133 GeV-2.7 TeV with the 196/220/234 m stations (43 GeV with 420 m) and timing 50-60 ps needed at PU 200 [2103.02752 abstract, Sec.1]; Run-3 PPS is 350 GeV-2 TeV. (Secondary web source says the PPS-2 project was approved in 2023 and postponed to LS4: UNVERIFIED.) The 2m_Q ≥ 133 GeV window starts at m_Q ≈ 70 GeV; the useful range m_Q = 130-600 GeV overlaps the region already excluded to 110-180 GeV by FASER.
- **Exploit:** (d) parameter measurement after discovery: M_X = 2m_Q + E_int (E_int ≈ 2(γ* − 1)m_Q, ~25 % of 2m_Q) is measured to ~3 GeV; the ξ-resolution is 3×10⁻⁴ [2103.02752 Sec.2]. No trigger exists for such events (open question). Not a discovery channel: ~3 % of the main-analysis statistics.
- **Effort / confidence:** weeks; medium. **Verdict:** inelastic: **NOT A GAP (killed, +5 %)**; exclusive: **WORTH A CHECK only as a post-discovery handle**.

### G-T6-2  Doublet L (1,2)_{-1/2}, triplets, and mass splittings
- **Current treatment:** theory_signal_model §1.3 assumes ΔM ≈ 340 MeV, cτ ≈ 7 mm (UNVERIFIED), "disappearing" quirk pair; no study.
- **Checked now:** Minimal-DM formula M_Q − M_0 = Q(Q + 2Y/cosθ_W)ΔM with ΔM = α₂M_W sin²(θ_W/2) = 166 MeV [hep-ph/0512090 Eq.8-9, Table 1]: doublet Y = 1/2 gives 341 MeV, Y = 0 triplet 166 MeV, Y = 1 triplet 540 MeV (Q = 1) and ~1.4 GeV (Q = 2). Γ(Q⁻ → Q⁰π⁻) = G_F²|V_ud|² f_π² c² ΔM³ √(1 − m_π²/ΔM²)/π with c = 1 (doublet), c² = 2 (triplet) (my derivation, `T6_annihilation.py` header comment; the paper's formula [hep-ph/0512090 Eq.25] has (n²−1)/4 which equals 1 only for triplets, giving 6 mm for a doublet vs my 8 mm). Result (ESTIMATE): **cτ = 7.9 mm (doublet), 6.0 cm (Y = 0 triplet, reproduces the known 6 cm), 0.9 mm (Y = 1 triplet, Q = 1), 0.2 mm (Q = 2)**. BR(π) = 97.7 % [hep-ph/0512090 Eq.25].
- **Topology:** a charged quirk in the lab has βγ ≈ p/m ≈ 0.6 / 0.25 / 0.13 at m = 200 / 500 / 1000 GeV for pT(pair) = 250 GeV; decay lengths ≈ 5 / 2 / 1 mm (doublet), 3.6 / 1.5 / 0.8 cm (triplet). The surviving fraction at R = 3 cm is 0.2 % / 2×10⁻⁵ / ~0 (doublet) and 40 % / 14 % / 2 % (triplet, 200 / 500 / 1000 GeV). The quirk string is irrelevant: the decay is local in the quirk rest frame. After Q⁻Q̄⁺ → Q⁰Q̄⁰ the pair is neutral (net charge ±1 for W-mediated pairs also becomes 0); the Z/γ-invisible neutral quirks leave nothing but soft displaced pions (p_π ≈ 0.3 GeV). The "helix drift of a net-charged pair" is moot.
- **Rates:** doublet total DY is ×14 that of E; triplet ×37 (table). With N_IC = 2 at 500 GeV: 84 fb (doublet). With P(pT_ISR > 200 GeV) ≈ 0.10 [1911.02223 App.A], that is ≈ 8 fb of MET + jet events, i.e. in the monojet/compressed-EW region. The doublet is the same field content as a Dirac higgsino (SUSY-WG rates reproduce, §0 above), so the compressed-higgsino monojet and disappearing-track limits apply with σ × 2N_IC/… (ESTIMATE; I did not open those papers, UNVERIFIED).
- **Exploit:** (a) a stronger/new constraint: a monojet recast for N_IC = 2 Dirac doublets could reach several hundred GeV at HL-LHC with ×14 the E rate (no number; needs the CMS monojet fiducial limits, not opened). (b) Disappearing-track search is hopeless for doublets (decays inside the beam pipe) but marginal for Y = 0 triplets at m ≲ 300 GeV.
- **Effort / confidence:** days for a recast; low-medium. **Verdict:** **WORTH A CHECK** (as a monojet recast, not as a CMS tracker benchmark; supports keeping E as the primary).

### G-T6-3  Charge and spin space
- **Charge:** σ_DY ∝ q² to 0.01 % (Z negligible), γγ ∝ q⁴. A |q| = 2 singlet fermion has σ(N_IC = 2) = 24 fb (+ 3.8 fb γγ) at 500 GeV and 0.72 + 0.12 fb at 1 TeV (table). A 3-event reach with the same 1.8 % efficiency as for |q| = 1 needs σ(N_IC = 2) ≳ 0.055 fb ⇒ m ≈ 1.3 TeV (σ = 0.72 → 0.032 fb between 1 and 1.5 TeV), vs ≈ 1.15 TeV for |q| = 1 [theory_signal_model §7]. Scalings (ESTIMATE): dE/dx ∝ q² (4× at |q| = 2, more ToT saturation in the IT, more CM stopping); Lorentz force ∝ q; the plane thickness d ∝ q [1911.02223 Eq.III.12, 2002.07503 Sec.V.A], so Λ_min(d = 100 µm) rises by 2^{1/4} = 1.19 (0.69 → 0.82 keV at 500 GeV); ℓ_max unchanged.
- **Existing limits:** ATLAS full Run 2, spin-1/2, 2 ≤ |q| ≤ 7, DY + photon fusion: m > 1060 GeV (|q| = 2) up to 1600 GeV (|q| = 6) [2303.13613 abstract]; 36 fb⁻¹ version 980-1220 GeV [1812.03673]. They need a (nearly) helical, highly ionising track. My assessment (ESTIMATE, UNVERIFIED): they cover merged quirks (Λ ≳ 20-30 keV) at |q| = 2 to ≈ 1.1 TeV; they do **not** cover the 0.3-20 keV non-helical window. CMS multi-charged HSCP limits: not checked.
- **Multi-charged inside multiplets** decay at the IP (Q = 2 of a Y = 1 triplet: cτ 0.2 mm). Only SU(2) singlets with Y = ±2, ±3 give long-lived multi-charged quirks.
- **Spin:** fermion/scalar angular distribution 1 + cos²θ* vs sin²θ*: the fraction with |cosθ*| < 0.8 is 73 % vs 94 % (analytic), a < 25 % effect on the pair-axis acceptance. The dominant spin effect is the rate (×11-18, §2 of the model doc) and γ* (1.43 vs 1.25), already in the Ẽ alternate. Nothing new.
- **Y = 0 SU(2)-charged:** the triplet (rows above): ×37 rate, but see G-T6-2.
- **Effort / confidence:** days; medium-high. **Verdict:** |q| = 2: **WORTH A CHECK** (cheap sample, +150 GeV reach, extra ~15 % of the Λ range uncovered by ATLAS); spin: **NOT A GAP**.

### G-T6-4  Quirkonium / delayed annihilation of stopped pairs
- **Current treatment:** Evans-Luty recast CMS 1801.00359 [1811.08903]: transport in a CMS cylinder (Tab.1), Bethe-Bloch with Anderson-Ziegler peak, 3.8 T. Stopping fraction in ECAL+HCAL |η| < 1: 1-5 % for E′ (400 GeV, SU(2)_IC, N_IC = 2), flat for Λ ≳ 300 eV (plot ends at 1 keV); full calorimeter (|η| < 3) ~×3; yoke ≈ same again [Sec.2, Fig.2, Fig.6, Sec.5]. τ_stop = 0.1-100 µs at 500 GeV [Fig.4]. De-excitation after stopping: τ ≲ µs for Λ < 200 keV, ≈ 3 ms at 1 MeV [App.B Eq.B.37, Fig.9]; final bound state annihilates in ~m_Q⁻¹α⁻⁵ ~ 10⁻¹⁸ s [Eq.3.2-3.3]. Annihilation products for the E′ (singlet) case: γγ : ff̄ : IC glueballs, 40-65 % visible [Eq.4.3]. Triggerable window: 21 % of the time with the 2016 fill [Fig.4 caption]; 8b4e fills would be worse [Sec.6].
- **Gaps:** (i) E-L simulated only Λ ≤ 1 keV and assumed prompt de-excitation. (ii) the 2016 21 % window and L1 settings are not HL-LHC (2760 bunches; UNVERIFIED). (iii) no HL-LHC/Phase-2 projection exists (E-L only mention the HGCAL endcap with 25 ps timing and fine granularity [Sec.5]). (iv) their reach used CMS 38.6 fb⁻¹; at 3 ab⁻¹ with an energy threshold the search is background-free.
- **Estimates (mine):**
  - Dissipation of the internal energy: with time-uniform momentum in [0, p*] and brass-like stopping power, τ_diss ≈ 73 / 147 / 213 ns at m = 200 / 500 / 1000 GeV (median γ*, E_int = 120 / 250 / 380 GeV), range 20-490 ns over γ* from −70 % to +100 % in (γ* − 1) (`T6_stopping.py`). This is ≪ the 0.1-100 µs of E-L Fig.4, which includes the CM stopping time in lower-density ECAL, so τ_tot ≈ 0.1-10 µs. Implication: the annihilation time is much longer than the 25 ns BX, uniform in the bunch pattern, so the 21 % livetime fraction applies. A 1D toy for the CM stopping fraction failed (no stable result), so the stopping fraction is taken from E-L, not computed.
  - Yield (3 ab⁻¹, N_IC = 2, DY σ of the model doc, ε_window 0.21, ε_reco 0.55 [1801.00359 Tab.1 plateau for gluinos], ε_veto 0.877 × 0.944 [Tab.1]): N = σL f_stop × 0.21 × 0.55 × 0.83 × BR_vis. At f_stop = 1 % / 3 % / 6 % and BR_vis = 0.4-0.65:

| m_Q | σ [fb] | N (f_stop = 1 %) | N (3 %) | N (6 %) |
|---|---|---|---|---|
| 200 | 220 | 250-410 | 760-1230 | 1500-2460 |
| 500 | 6.11 | 7-11 | 21-34 | 42-68 |
| 800 | 0.66 | 0.8-1.2 | 2.3-3.7 | 4.5-7.4 |
| 1000 | 0.197 | 0.2-0.4 | 0.7-1.1 | 1.4-2.2 |

  3-event reach ≈ 0.65 TeV (f_stop = 1 %) to 0.9 TeV (6 %). Compare the tracker plane-finder reach ≈ 1.1-1.2 TeV for 0.6-15 keV and the near-nothing it gives for Λ < 0.3 keV and Λ > 30 keV. The stopped search is **independent of the tracker and of ISR**, so it is a cross-check and covers the Λ ranges where the tracker search is blind (Λ < 0.3 keV; 30 keV-~1 MeV, if E-L's flat stopping extends there). It stays background-free only with a high energy cut (a single 1 TeV deposit). Annihilation energies: ~2m_Q mostly in ℓℓ (18.5 % ee + μμ), jets (54 % of the ^3S_1 state) and ~0.8 of the pairs visible (my S-wave estimate; E-L's 40-65 %).
- **Recast:** CMS 1801.00359 (calorimeter search, 721 h live time, 38.6 fb⁻¹, ε_stopping(HB+EB) 0.054 for gluino R-hadron; muon search also) and ATLAS 2104.03050 (579 h, 2017-18, gluino R-hadron to 1.4 TeV). Neither has a quirk interpretation. A Phase-2 analogue would profit from MTD/HGCAL timing (ns-scale), and from a ~PU-free empty BX.
- **Exploit:** (a) new constraint/signature; (c) needs a simple HL-LHC projection; (f) a pheno paper on "stopped quirks at HL-LHC with Λ up to MeV". **Effort:** weeks (Geant4-based stopping in 3D+B needed; T3's transport code would do it); **confidence:** medium (stopping fraction uncertain by ×3). **Verdict: EXPLOIT** (as a complementary Phase-2 analysis, not as a replacement).

### G-T6-5  Microscopic-Λ complement: prompt annihilation and the 0.1-3 MeV displaced band
- **Literature:** annihilation of colour-singlet quirkonium: Kang-Luty Sec.5 [0805.4642 Eq.5.32-5.33, 5.38-5.39, 5.59-5.62], Kilic-Okui-Sundrum [0906.0577], Harnik-Kribs-Martin [1106.2569], coloured quirkonium diphoton: Curtin-Verhaaren [1512.05753], Fok-Kribs [1106.3101] (chiral quirkonium). All coloured or Λ ≳ GeV, none for EW-only quirks at current LHC limits. UNVERIFIED which of these include explicit LHC resonance limits.
- **Estimate:** Λ ≳ 3 MeV (vacuum L_ann < 3 mm; E-L Eq.4.4 with ε_emit = 0.1; α_IC(500 GeV) = 0.043 at 1 keV, 0.065 at 1 MeV). S-wave: ^1S_0 (25 %) → γγ : Zγ : ZZ : IC gg = 0.138 : 0.079 : 0.011 : 0.77 (Γ(IC gg)/Γ(γγ) = α_IC²(N²−1)/(4N²α²) = 5.6; QCD-onium analogy: it gives 2/9 for N = 3); ^3S_1 (75 %) → ff̄ via B*: ee, μμ, ττ 12.3 % each, quarks 54 %, νν 7 % (hypercharge-weighted). Spin-averaged: BR(ee + μμ) = 18.5 %, BR(γγ) = 3.4 %, BR(Zγ) = 2.0 %, visible 81 %. These ignore hyperfine/spin-flip dynamics; the E-L number is 40-65 % visible [Eq.4.3].
- **Reach:** σ × BR(ee + μμ) = 1.1 / 0.50 / 0.24 / 0.12 fb at m_Q = 500 / 600 / 700 / 800 GeV, σ × BR(γγ) = 0.21 / 0.09 / 0.044 / 0.023 fb. ATLAS combined dilepton σ_fid × B limit is 3.6 fb at 250 GeV falling to 0.014 fb at 6 TeV [1903.06248 text, p. "limit on the fiducial cross-section times branching ratio ranges from 3.6 (13.1) fb at 250 GeV to about 0.014 (0.018) fb at 6 TeV"]; diphoton spin-0 narrow limit 1.1 fb at 400 GeV, 0.03 fb at 2.8 TeV [2102.13405, via search snippet]. For M = 1.4-2 TeV I read ≈ 0.05-0.1 fb (UNVERIFIED). ⇒ m_Q ≲ 0.8-1 TeV already excluded for Λ ≳ 3 MeV if f_annih ≈ 1. At 3 ab⁻¹ the dilepton limit improves ×~3-5 ⇒ ≈ 1.2-1.4 TeV.
- **Intermediate band 0.1-3 MeV:** L_ann = 9.3 cm × (1 MeV/Λ)³ (m = 500; ESTIMATE; cm-m scale at 1-0.3 MeV, 90 m at 100 keV). Displaced annihilation of a 2m_Q-mass state into ℓℓ, γγ, jets: no search; for Λ < 0.3 MeV stopping in calorimeters/yoke followed by delayed annihilation (G-T6-4).
- **Verdict:** **EXPLOIT** as a theory-input statement for the strategy (the Λ ≳ MeV edge of the map is *not* a CMS-tracker target; the CMS search should not claim Λ > ~1 MeV), and **WORTH A CHECK** for the displaced band (hand to T2/T3: ε_emit, J random walk, material effects).

### G-T6-6  Other probes (one line each)
- Cosmic-ray / neutrino telescope: quirk flux needs UHE collisions with σ ~ DY; IceCube/Auger rates for TeV-mass EW pairs ≪ 1 event/decade (rough ESTIMATE, not computed). Killed.
- Beam dump (SHiP, NA62): √s ≲ 30 GeV, m_Q ≥ 110 GeV is kinematically closed. Killed.
- MoEDAL (NTD/MMT): detects trapped singly/multiply charged states; a neutral pair has no net charge and Λ ≳ 0.3 keV pairs stop in material at ≪ 100 cm. No benefit. Killed.
- MATHUSLA / CODEX-b / ANUBIS / FACET: quirk pair in 25-100 m of rock/shield stops (ionisation loss of two charges at β ≲ 0.5). Killed; FASER works only for long strings (Λ ≲ 100 keV, existing).
- e+e− colliders: FCC-ee/ILC at √s = 365-500 GeV reach m_Q < 250 GeV, mostly excluded already. CLIC/muon collider ≥ 3 TeV: clean, ISR-free; relevant only beyond HL-LHC reach. Not pursued.

## 4. Killed ideas (with numbers)
- Inelastic photon-initiated production as a signal boost: +4.5-5.2 % of DY for |q| = 1 (smaller than the ±18 % PDF uncertainty at 1 TeV).
- Exclusive γγ → QQ̄ + PPS as discovery: 35 events at 500 GeV, 3 ab⁻¹ before efficiency (3 % of the main analysis); 3 events at 750 GeV.
- Doublet/triplet as a tracker-quirk benchmark: cτ = 8 mm / 6 cm; ≤ 2 × 10⁻⁵ of charged doublet quirks survive to R = 3 cm at m = 500 GeV (βγ = 0.25).
- Spin as acceptance driver: ≤ 25 % at the pair-axis level.
- Cosmic ray/dump/MATHUSLA/CODEX-b/MoEDAL: see G-T6-6.

## 5. Open questions
- **T3 (propagation):** (i) the stopped fraction in 3D with B for Λ = 1-1000 keV (E-L stops at 1 keV and assumes prompt de-excitation); my 1D toy failed. (ii) Is the tracker plane-finder efficiency for |q| = 2 affected by the larger ToT saturation and the ×2 plane thickness? (iii) τ_stop distribution at HL-LHC bunch structure.
- **T2 (string dynamics):** (i) vacuum annihilation length L_ann = (βγ)₀(βγ)_cm m E_int/(ε_emit Λ³): ε_emit = 0.1 is a guess; the 0.1-3 MeV band edges scale with it. (ii) Spin-state population of the ground-state quirkonium (singlet:triplet = 1:3 assumed).
- **T1 (Λ origin/cosmology):** if Λ ≳ MeV is cosmologically allowed with N_IC = 2, the prompt-resonance exclusion m_Q ≲ 0.8-1 TeV applies and the tracker search should not target it.
- **Experimental Phase 2:** (a) Is there any Phase-2 L1/HLT path with empty-BX calorimeter triggers and what is the HL-LHC fill livetime (21 % in 2016)? (b) Is a PPS-based trigger conceivable, and when does PPS-2 start? (c) Will CMS recast 1801.00359 for quirks (needs stopping fraction and de-excitation assumptions; no quirk model in CMSSW)?
- **Verification TODO (UNVERIFIED items above):** ATLAS dilepton limit at 1.4-2 TeV, diphoton limit at 1 TeV, compressed-higgsino monojet/disappearing-track limits, CMS multi-charged HSCP limits, S² for exclusive heavy states, PPS-2 schedule.

## 6. References opened
- 1811.08903 (Evans-Luty): stopping fraction, τ_stop, trigger window, annihilation BRs, de-excitation times (App.B), Eq.4.4.
- 0805.4642 (Kang-Luty): quirkonium annihilation widths, P_QED per crossing 1/780 (N_IC = 3), P_inv, resonance width Eq.5.59, regime summary in the abstract.
- 1812.04886 (Harland-Lang et al.): exclusive slepton σ = 0.03-0.8 fb, FPD ξ range, backgrounds; 1910.01703 (abstract only, via web).
- 2103.02752 (CMS PPS-2 EoI): mass ranges 133 GeV-2.7 TeV / 43 GeV, timing, schedule statements.
- hep-ph/0512090 (Cirelli-Fornengo-Strumia): mass-splitting formula Eq.8-9, cτ and BRs Eq.25, Table 1.
- 1801.00359 (CMS stopped LLP, 13 TeV): ε_stopping 0.054, live time, ε_reco, vetoes; 2104.03050 (ATLAS stopped, abstract).
- 2303.13613, 1812.03673 (ATLAS multi-charged): limits for DY + photon fusion.
- 1903.06248 (ATLAS dilepton): limits 3.6 fb (250 GeV) to 0.014 fb (6 TeV). 2102.13405 (ATLAS diphoton): limits from search-engine snippet only.
- 1512.05753 (abstract), 0906.0577, 1106.2569, 1106.3101, 1605.01937: titles/abstracts only; not used for numbers.
- research/theory_signal_model.md §1.3, §2.3, §4.3, §6.3.
