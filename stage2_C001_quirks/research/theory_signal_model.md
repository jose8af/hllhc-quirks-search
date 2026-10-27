# C001 Stage 2: theory and signal model for EW quirks in the CMS Phase-2 tracker

Author: theory/signal-modelling agent (Stage 2). Date: 2026-10-07.
Scope: this file feeds the Phase-1 STRATEGY (benchmarks, signal model, signal systematics) and the Phase-2 sample plan.
**Experiment: CMS Phase-2.** The user is a CMS member, so CMS (B = 3.8 T, Phase-2 IT/OT, MTD) is the primary target. ATLAS ITk numbers are secondary.

Tagging conventions:
- Every number carries a reference and location such as `[arXiv:id, Sec./Eq./Tab./line]`.
- `ESTIMATE` marks my own calculation, with the inputs stated.
- `UNVERIFIED` marks a value recalled or read from a secondary source and not checked against the primary document.

Scratch code is reproducible from the scratchpad and was **not** put in the project:
- `dy_xsec.py`: LO Drell-Yan with an LHAPDF-grid reader.
- `sigmap.py`: kinematics toy.

The full code and outputs are quoted in App. A so they can be re-created.

## 0. Executive summary (read this first)

1. **Recommended primary benchmark: `E` = vector-like Dirac fermion, (1,1)_{-1}, N_IC = 2.** It is the exact model of:
   - the only LHC quirk search, FASER [2607.26195 p.2; HEPData ins3184325];
   - the FASER/FASER2 projection [2404.13814 Eq.2.1];
   - the Knapen et al. coplanar proposal [1708.02243 Fig.6, "(1,1)_1, N_Q=2"];
   - Evans-Luty [1811.08903 Eq.2.1, "E' ~ (N,1,1)_1", SU(2)];
   - Farina-Low [1703.00912 Tab.II];
   - Li et al. App.A [1911.02223, "E^c (1,1)_{-2}, N_IC=2" in their Y-normalisation].

   Alternates:
   - **A1 = scalar `Ẽ`**, same quantum numbers, N_IC = 2. It checks spin and kinematics and gives a 10-18x smaller rate.
   - **A2 = `L` doublet fermion (1,2)_{-1/2}**, N_IC = 2. This is a topology alternate with an important caveat (Sec. 1.3): the charged member may beta-decay to the neutral member on a ~cm scale. That would turn the signature into a disappearing, kinked quirk pair.

   N_IC = 3 or 5 is a pure rate rescaling (sigma ∝ N_IC), so it needs no extra samples.

2. **Cross sections: the prior Gate-4 estimate was too low by about x3.**
   - Method: my LO calculation (CT18NLO), validated against the LHC SUSY xsec WG right-selectron tables for the scalar, times K-factors extracted from those tables (spin-independent DY QCD correction).
   - Result for sigma(pp → E Ē) at 14 TeV, N_IC = 2: **220 fb at 200 GeV, 6.1 fb at 500 GeV, 0.66 fb at 800 GeV, 0.20 fb at 1 TeV, 0.066 fb at 1.2 TeV** (all ESTIMATE, table in Sec. 2).
   - The fermion/scalar ratio is 11-18, not the 4 assumed in `research/reviews/feasibility/C001.md`. DY pairs are produced near threshold, so the beta^3 suppression of the scalar matters.
   - PDF uncertainty grows from ±3.7% (200 GeV) to ±18.5% (1 TeV) with PDF4LHC21 [SUSY xsec WG 13.6 TeV NNLL table].
   - With Knapen-like efficiencies (~1.8%) the 3-event reach at 3 ab^-1 is m_Q ≈ 1.1-1.2 TeV, comparable to FASER2's 1.0 TeV [2404.13814 Sec.7]. This is conditional on the timing issue in point 4.

3. **Minimal simulation chain for CMS:**
   1. MG5_aMC (any vector-like-lepton UFO, ×N_IC), with a pT(QQ̄) generator filter. Pythia8 CP5 shower.
   2. A quirk-pair Geant4 transport process: string force + 3.8 T field + standard EM energy loss.
   3. Standard CMSSW Phase-2 SimHits → Phase2TrackerDigitizer + MTD digitisation with PU200 premixing.

   **What is missing publicly:**
   - **No quirk physics exists in CMSSW** (checked `SimG4Core/CustomPhysics/src`).
   - The only public, collaboration-validated Geant4 quirk transport is **ATLAS Athena `Simulation/G4Extensions/Quirks`** (used by FASER [2607.26195 App.A]). It includes a standalone Geant4 version.
   - `PreFASERQuirkSim` (public C++) handles only forward transport to FASER.
   - The Knapen-Papucci central-detector trajectory code was shared privately [2410.00269 Ack.].

   Porting the Athena package to `SimG4Core` is the critical-path item (Sec. 3.5).

4. **Findings that reshape the target:**
   - **(a) The coplanar window is narrower at CMS than at ATLAS.** The plane thickness scales as ∝ B·m_Q/Λ^4 [1911.02223 Eq.III.12; 2002.07503 Eq.V.6-V.9]. At 3.8 T the thickness exceeds Knapen's 100 µm cut for Λ ≲ 0.55-0.8 keV (m_Q = 0.2-1 TeV; ESTIMATE). The coplanar plane finder therefore works for **Λ ≈ 0.6-15 keV** at CMS. Below that a trajectory fit or GNN is needed; above ~20-30 keV the two quirks merge into one straight, ~2×MIP track.
   - **(b) Heavy, triggerable pairs are slow.** For m_Q ≥ 500 GeV with pT(QQ̄) = 250 GeV, the pair transverse velocity is β_T ≈ 0.14 (median). The pair reaches the outer OT/BTL radius ~16 ns *after* a β = 1 particle (ESTIMATE, Sec. 4.3). The OT is a binary, bunch-crossing-tagged readout [2210.07766 Sec.2]. Out-of-time hits, and the next-BX readout, can therefore dominate the efficiency above ~500 GeV. The sample plan must simulate hit times faithfully, and this is a new item for the experimental team.
   - **(c) Glueball emission (ε) is irrelevant inside the tracker** for Λ ≤ 30 keV. Less than 0.1 GeV of the ~100 GeV internal energy is radiated (ESTIMATE, Sec. 3.3). The ε systematic used by FASER is therefore not needed for the central search.
   - **(d) Λ conventions differ by a factor 1/0.6 = 1.67.** The collider literature uses Λ ≡ √σ_string. The cosmology paper uses Λ ≡ T_c = 0.6 √σ [2512.20696 Eq.1 and text below it]. The strategy must state "Λ ≡ √σ".
   - **(e) A public ATLAS repository describes an "ATLAS quirk search" using GNN4ITk dumps** (github.com/burzynski-lab/quirk-tracking; UNVERIFIED as to its status). This is possible competition from ATLAS.

5. **Recommended Phase-2 grid (Sec. 7):**
   - m_Q ∈ {200, 350, 500, 750, 1000, 1250} GeV × Λ ∈ {0.3, 0.6, 1, 2, 5, 10, 20, 30} keV for the primary `E`.
   - Generate **one** LHE sample per mass with a pT(QQ̄) filter and re-propagate it for each Λ, because Λ enters only in the transport.
   - Use ≥ 10k filter-passing events per (m_Q, Λ) point for efficiency maps, plus 3 masses × 3 Λ points for `Ẽ` and 2 points for `L`.

---

## 1. Model space and benchmark choice

### 1.1 Minimal model and parameters

The model has:
- a new SU(N_IC) gauge group with confinement scale Λ;
- vector-like quirks Q in the fundamental of SU(N_IC) and in some SM representation;
- no IC-charged state lighter than Λ.

String breaking is suppressed by ~exp(−π m_Q²/Λ²) [0805.4642 Eq.3.1-3.3]. The pair is joined by a flux tube of tension σ.

- **Definition used here: σ ≡ Λ².** This is the "precise definition" adopted by Knapen et al. [1708.02243 below Eq.2]. Farina-Low also take T = Λ² for simplicity and note T ≈ 1.6Λ² for QCD [1703.00912 below Eq.1]. Evans-Luty, Li/Pei, FASER and 2404.13814 all write the force as Λ² [1811.08903 Eq.2.3; 2002.07503 Eq.II.2; 2404.13814 Eq.5.2].
- **Warning.** Asadi-Kribs-Luty define Λ ≡ T_c with T_c/√σ ≈ 0.6 [2512.20696 Eq.1 and line below]. So Λ_cosmo ≈ 0.6 Λ_collider. Their 0^{++} glueball mass "≈ 6Λ" [2512.20696 Sec.2] is ≈ 3.6 √σ, consistent with the lattice value quoted by Kang-Luty [0805.4642 Sec.5.7]. The strategy should quote Λ ≡ √σ and convert cosmology bounds by ×1/0.6.

Free parameters:
- m_Q;
- Λ;
- the SM representation and spin;
- N_IC.

The rate scales as σ_prod ∝ N_IC [0805.4642 Sec.3.2; 2404.13814 Sec.2]. The trajectory physics does not depend on N_IC, except through the non-perturbative ε and annihilation rates [2404.13814 Eq.4.11], which are irrelevant here (Sec. 3.3).

Characteristic length. The maximum CM separation of a back-to-back pair is ℓ_max = 2(γ*−1) m_Q/σ = **3.95 cm × (γ*−1)(m_Q/100 GeV)(keV/Λ)²**. This is exact for the straight string with no external force. It is derived from energy conservation [1703.00912 Eq.2, "ℓ_eff = 2m_Q(γ−1)/Λ²"], with ħc = 1.973×10⁻¹⁴ GeV·cm.

The literature's shorthands differ by factors 2-4:
- "d_cm ~ 2 cm (γ−1)(m/100 GeV)(keV/Λ)²" [1708.02243 Eq.1; 2410.00269 Eq.1];
- "ℓ ~ 1 cm (m/100 GeV)(keV/Λ)²" [2404.13814 Eq.2.6; 2607.26195 p.2; 2512.20696 Eq.1];
- "ℓ ~ 10 cm (m/TeV)(keV/Λ)²" [1811.08903 Eq.1.1].

Use the exact expression in the strategy.

### 1.2 Benchmarks used by existing studies (for comparability)

| Study | Representation / spin | N_IC | √s, L | Role |
|---|---|---|---|---|
| FASER search [2607.26195 p.2; HEPData ins3184325 t1-t2] | (1,1,−1) fermion "E" | 2 | 13.6 TeV, 186 fb⁻¹ | **only LHC exclusion**: 179 GeV at Λ = 10 keV; 113 GeV at 1 keV; 57 GeV at 300 eV; 173 GeV at 30 keV; 71 GeV at 100 keV (observed, HEPData t2) |
| FASER/FASER2 pheno [2404.13814 Eq.2.1-2.4] | E, D (fermions); Ẽ, D̃ (scalars) | 2 | 13 TeV (σ), 3 ab⁻¹ (FASER2) | FASER2 discovery up to 1000 GeV (E), 600 GeV (Ẽ) [Sec.7] |
| Knapen et al. [1708.02243 Sec.II, Fig.6] | (1,1)_1 vector-like fermion (EW); (3,1)_{2/3} (coloured) | 2 | 13 TeV, 300 fb⁻¹ | EW quirks to 650 GeV (5 events), 100 eV-30 keV [abstract] |
| Li, Li, Pei, Zhang [1911.02223 Eq.II.1-II.4, App.A] | D^c, E^c fermions; D̃^c, Ẽ^c scalars | 3 (main), 2 (App.A) | 13 TeV, ~100 fb⁻¹ | neutral fermion (scalar) to 450 (150) GeV |
| Farina-Low [1703.00912 Tab.II] | (3,1)_{2/3}, (1,1)_{−1}, fermion and scalar | 2, 5 | 13 TeV, 12.9 fb⁻¹ | uncoloured fermion N=2: 650/150/− GeV at Λ = 1 eV/100 eV/1 keV |
| Evans-Luty [1811.08903 Eq.2.1] | E' (N,1,1)_1, T' (N,3̄,1)_{−2/3} | 2 | 13 TeV | OoT stopped-quirk recast |
| Sha et al. GNN [2410.00269 Sec.III] | charge ±1, "e.g. s-channel Drell-Yan" (N_IC not stated) | − | 13 TeV, 300 fb⁻¹ | N > 3 for m_Q ≲ 700 GeV, Λ ≲ 5 keV [Sec.VI] |
| LHCb VELO [2601.09023 Sec.2, Fig.2] | (3,1)_{2/3} fermion, 30% charged hadrons | 2 | 300 fb⁻¹ | coloured only, so not directly comparable |
| D0 [1008.3547 abstract] | charged EW fermion | 2/3/5 | Tevatron | m_Q > 107/119/133 GeV for 10 keV < Λ < 1 MeV |
| Asadi-Kribs-Luty cosmology [2512.20696 Sec.2] | SU(2)_L vector-like, Y = 0 | 2 | − | cosmology only; bounds claimed robust to SM quantum numbers [Sec.6] |

### 1.3 Recommendation

**Primary: `E` = (1,1)_{−1} Dirac fermion, N_IC = 2.**
- It is the common denominator of FASER, FASER2, Knapen, Li/Pei, Evans-Luty and Farina-Low (table above). The CMS result can then be overlaid on all of them without reinterpretation.
- It has only γ*/Z couplings. There is no charged-neutral splitting, and the pair is always ±1 ⇒ electrically neutral overall. This is the clean coplanar case: the thickness is linear in the quirk charge for a neutral pair, and multiplied by the number of periods for a non-neutral pair [2002.07503 Sec.V.A].
- It has no renormalisable mixing with SM leptons, because the IC charge forbids E·L·H. The quirk is therefore automatically stable, as the lightest IC-fundamental state [0805.4642 Sec.1].
- N_IC = 2 is the conservative (smallest) rate [2404.13814 Sec.2; 1811.08903 Sec.2]. Report σ×BR-free limits on σ/N_IC so that N_IC = 3, 5 follow by rescaling.

**Alternate A1: `Ẽ` scalar, (1,1)_{−1}, N_IC = 2.**
- It has the same couplings, but σ is lower by ×11-18 (Sec. 2).
- The scalar is P-wave: β³ threshold behaviour versus β(3−β²)/2 for the fermion. Scalars are therefore produced faster in the pair CM frame: median γ* = 1.43 versus 1.25 at m_Q = 500 GeV (ESTIMATE, Sec. 4.1, App. A). This gives larger ℓ_max and different hit topologies.
- The angular distribution also differs (sin²θ* versus 1+cos²θ*). It tests the spin dependence of acceptance, and it is the model for which SUSY-WG NLO+NLL σ tables exist directly (right-handed selectron).
- Used by 2404.13814, 1911.02223 and 1703.00912.

**Alternate A2: `L` = (1,2)_{−1/2} Dirac doublet fermion, N_IC = 2.** This is a topology test, not a rate test.
- σ is larger. Per unit N_IC, the charged pair is ≈ σ(χ̃⁺χ̃⁻) for a higgsino, 0.28 pb at 200 GeV and 13.6 TeV, versus 0.105 pb for E. Q^±Q^0 via W adds ≈ 1 pb per unit N_IC (≈ 2 pb for N_IC = 2) [SUSY xsec WG 13.6 TeV higgsino NNLL tables, fuenfundachtzig/xsec `pp13600_hino_deg_*`; the doublet-to-higgsino mapping is my ESTIMATE].
- **Caveat (my ESTIMATE, not in the quirk literature I found).** For a pure doublet, the EW loop splitting is Δm ≈ 340 MeV. The charged quirk then decays Q^± → Q^0 π^± with cτ ≈ 7 mm, as for a pure higgsino (UNVERIFIED: standard higgsino value, not re-derived here).
  - Inside the tracker, a charged-charged L pair becomes charged-neutral and then neutral-neutral, i.e. it disappears.
  - The charged-neutral pair (W-mediated) gives a single charged quirk dragged by an invisible partner [0805.4642 Sec.4.3, Fig.7]. Its net charge also breaks coplanarity [2002.07503 Sec.V.A].
  - Generate 2 points only, to demonstrate the topology. Do not use it as a headline benchmark.
  - The EW-precision constraint of 2504.02940 (Δ < 43 GeV, quoted in `research/reviews/theory/C001.md`) applies to split doublets.

**Not recommended as benchmarks:**
- Coloured quirks: these are QCD-produced R-hadron-like states, the LHCb benchmark [2601.09023], outside the "EW-charged" target.
- The Y = 0 SU(2) model of 2512.20696: its charged and neutral states split as for a wino, Δm ≈ 165 MeV and cτ ≈ 6 cm (UNVERIFIED standard wino value). The same disappearing issue arises.

---

## 2. Cross sections σ(pp → QQ̄)

### 2.1 What exists in the literature

- 2404.13814 gives LO and NLO σ at 13 TeV for E, D, Ẽ, D̃ **only as a figure** [Fig.1]. Its K-factors for E are 1.33 at 200 GeV and 1.45 at 1 TeV, and for Ẽ 1.34 and 1.43 [Sec.3, below Fig.1]. It says 13.6 and 14 TeV are "slightly larger" (not tabulated).
- 1911.02223 gives LO σ (13 TeV) for E^c Ē^c and E^c Ē^c j (pT(j) > 200 GeV) only as figures [Fig.2, Fig.9 lower]. It reports that the trigger efficiency, i.e. the fraction with a 200 GeV jet, is 0.10 [App.A, consistent with 1708.02243 Tab.I].
- 2410.00269 gives "σ_QQj ≈ 1 fb for m_Q = 500 GeV" at 13 TeV [Sec.III]. The jet cut and N_IC are not stated.
- FASER assigns a 2-4% scale+PDF uncertainty [2607.26195 p.5]. This is valid for m_Q ≲ 200 GeV only (see below).
- The FASER HEPData record (ins3184325, doi:10.17182/hepdata.181308.v1) contains σ_fid^eff limits (t1) and contours (t2) only. It has **no inclusive σ prediction table** (checked 2026-10-07).
- **There is no published tabulated σ for E at 14 TeV.** Hence the calculation below.

### 2.2 Method (ESTIMATE, reproducible; App. A)

1. **LO calculation.** I wrote a pure numpy/scipy implementation of LO qq̄ → γ*/Z → QQ̄. The quirk is a vector-like SU(2) singlet: v_E = −Q s_W/c_W, a_E = 0, Q = −1.
   - Fermion partonic σ ∝ β(3−β²)/2; scalar ∝ β³/4.
   - Inputs: α = 1/127.9, s_W² = 0.2222 (MG5 `sm` defaults), M_Z = 91.1876 GeV, Γ_Z = 2.4952 GeV, five light flavours, μ_F = μ_R = √ŝ.
   - PDFs: LHAPDF grids read directly, CT18NLO central (primary) and NNPDF23_lo_as_0130_qed (the MG5 default LO set, as a cross-check).
2. **Validation.** The scalar LO × (NLO+NLL K) reproduces the LHC SUSY-xsec-WG right-selectron tables smoothly:
   - 13 TeV: NLO+NLL, PDF4LHC15 [json `pp13_slep_R_NLO+NLL_PDF4LHC.json`];
   - 13.6 TeV: NNLOapprox+NNLL, PDF4LHC21, Resummino 3.1.1 [json `pp13600_sleptons_2000011_-2000011_NNLL.json`].
   
   Both tables come from github.com/fuenfundachtzig/xsec/json (WG tables) [read 2026-10-07]. The implied K = σ_WG/σ_LO^CT18 rises smoothly from 1.06 (100 GeV) to 1.29 (1.2 TeV), as expected for qq̄ DY with an NLO PDF.

   Independent consistency check: 2404.13814's MG5 K (relative to an LO-PDF LO) = my K × (σ_LO^CT18/σ_LO^NNPDF23LO):
   - 1.10 × 1.149 = 1.26 at 200 GeV, versus 1.33-1.34 quoted;
   - 1.26 × 1.114 = 1.40 at 1 TeV, versus 1.43-1.45 quoted.
   
   This agrees to ≤ 6%.
3. **Fermion prediction.** σ_E = σ_LO^CT18(F) × K_WG(m, √s). QCD corrections to colour-singlet DY are initial-state and approximately spin-independent (assumption).
   - At 14 TeV, K is taken equal to the 13.6 TeV value. K changes by < 1.5% between 13 and 13.6 TeV.
   - At 1200 GeV, the 13 TeV K is used, because the 13.6 TeV table stops at 1 TeV.

### 2.3 Table: σ(pp → QQ̄) for N_IC = 2, in fb (ESTIMATE, method above)

| m_Q [GeV] | K(13) | K(13.6) | **E: 13 TeV** | **E: 13.6 TeV** | **E: 14 TeV** | LO scale var. (14 TeV, μ×½ / ×2) | PDF unc. (PDF4LHC21, WG scalar 13.6) | Ẽ: 13 | Ẽ: 13.6 | Ẽ: 14 | σ_E/σ_Ẽ (14) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 150 | 1.083 | 1.101 | 534 | 580 | **605** | −1.2/+0.7% | ±3.3%* | 47.6 | 51.9 | 54.3 | 11.1 |
| 200 | 1.098 | 1.110 | 193 | 210 | **220** | +0.5/−0.8% | ±3.7% | 16.7 | 18.3 | 19.2 | 11.5 |
| 250 | 1.112 | 1.118 | 85.3 | 92.8 | **97.5** | +1.7/−1.9% | ±4.2%* | 7.18 | 7.86 | 8.29 | 11.8 |
| 300 | 1.125 | 1.127 | 42.7 | 46.5 | **49.0** | +2.7/−2.7% | ±4.5% | 3.49 | 3.83 | 4.06 | 12.1 |
| 400 | 1.149 | 1.142 | 13.5 | 14.8 | **15.7** | +4.2/−4.0% | ±5.5% | 1.04 | 1.15 | 1.23 | 12.7 |
| 500 | 1.171 | 1.158 | 5.16 | 5.70 | **6.11** | +5.3/−4.9% | ±6.6% | 0.380 | 0.424 | 0.458 | 13.3 |
| 600 | 1.191 | 1.175 | 2.24 | 2.49 | **2.69** | +6.3/−5.8% | ±7.9% | 0.157 | 0.177 | 0.192 | 14.0 |
| 700 | 1.209 | 1.192 | 1.05 | 1.19 | **1.29** | +7.1/−6.3% | ±9.7% | 0.0702 | 0.0804 | 0.0883 | 14.6 |
| 800 | 1.226 | 1.211 | 0.525 | 0.601 | **0.660** | +7.9/−6.9% | ±11.9% | 0.0335 | 0.0390 | 0.0432 | 15.3 |
| 1000 | 1.259 | 1.254 | 0.148 | 0.176 | **0.197** | +9.1/−7.9% | ±18.5% | 0.00865 | 0.0105 | 0.0118 | 16.6 |
| 1200 | 1.292 | (1.292) | 0.0469 | 0.0576 | **0.0656** | +10.2/−8.8% | ±25%* | 0.00251 | 0.00316 | 0.00364 | 18.0 |

`*` marks interpolation or extrapolation of the WG PDF uncertainty (ESTIMATE).

How to read the uncertainty columns:
- The LO scale variation is shown only to show that LO μ-dependence is small for DY. After NNLL resummation the WG scale uncertainty is < 1% at all masses [WG 13.6 TeV json `unc_scale_*`]. **Use the WG scale uncertainty (≤ 1%) and the PDF4LHC21 PDF uncertainty in the column above.**
- The 13 TeV PDF4LHC15 table gives much smaller PDF errors (±2.5% at 500 GeV, ±5.6% at 1 TeV [WG 13 TeV json]). The 13.6 TeV PDF4LHC21 numbers are the current recommendation and are the conservative ones to use.

Other numbers:
- **Ratio 14/13.6 TeV (LO, CT18NLO):** 1.07 at 500 GeV and 1.12 at 1 TeV. This is the "√s scaling" asked for. It is computed, not assumed.
- **Validity checks:**
  1. Knapen's 300 fb⁻¹ 5-event discovery at 650 GeV with ε = 0.10×0.28×0.65 [1708.02243 Tab.I] implies σ(13 TeV) ≈ 0.9 fb. My 13 TeV N_IC = 2 value at 650 GeV is ≈ 1.5 fb with K, ≈ 1.3 fb at LO. Knapen used LO MG5 and an LO PDF, which is ~15% lower (my NNPDF23LO/CT18 ratio = 0.85-0.92). This is consistent within the ~factor 1.5 implied by their rounding.
  2. 1911.02223 states that scalar σ is ">1 order of magnitude" below the fermion [Sec.II]. This agrees with my ratio of 11-18.
- **Correction to the Gate-4 feasibility review.** That review (`research/reviews/feasibility/C001.md` §2) used σ_F ≈ 4σ_S and got ≈ 1.5-2 fb at 500 GeV, 14 TeV. The correct value is ≈ 6.1 fb. The factor 4 holds only at β → 1, while DY quirk pairs have median β* ≈ 0.6 (Sec. 4.1).
- **Doublet `L` (A2), 13.6 TeV, N_IC = 2 (ESTIMATE, higgsino proxy):**
  - σ(L⁺L⁻) ≈ 2 × 0.282 pb = 0.56 pb at 200 GeV; 2 × 7.35 fb = 14.7 fb at 500 GeV; 2 × 0.219 fb = 0.44 fb at 1 TeV [`pp13600_hino_deg_1000024_-1000024_NNLL.json`].
  - σ(L^±L^0) ≈ 2 × Σ(χ̃₁⁰χ̃₁^±) ≈ 2 × 2 × (0.505, 0.0133, 0.00041) pb at (200, 500, 1000) GeV [`..._1000022_±1000024_NNLL.json`]. The second factor of 2 is the neutral Dirac = 2 Majorana mapping (ESTIMATE).

### 2.4 Corrections not included anywhere in the literature (flag for systematics)

- **IC Sommerfeld enhancement** (attractive, colour-singlet IC channel). Kang-Luty say it "need[s] to be included in a more detailed study" [0805.4642 Sec.3.2].
  - Estimate: S = X/(1−e^{−X}), X = πC_F α_IC/β*, with C_F = 3/4 (SU(2)) and α_IC(m_Q) ≈ 0.04-0.05 (Sec. 6.2).
  - Result: S ≈ 1.09 at β* = 0.6 and ≈ 1.18 at β* = 0.3. **Net +5-15% on σ** (ESTIMATE). QED attraction adds ~+2%.
  - Recommendation: do not include it in the nominal value. Quote it as a one-sided theory systematic.
- **EW input scheme / NLO EW.** σ ∝ α², so α(M_Z) = 1/127.9 versus G_µ (≈ 1/132.5) differs by 7%. The K-factor extraction absorbs this only to the extent that the WG tables use the same scheme (UNVERIFIED). NLO EW corrections for TeV DY are typically −few % (UNVERIFIED, not computed for quirks).
  - Recommendation: a ±5% "EW scheme" nuisance, or adopt the WG convention verbatim.
- **Pair kinematics with ISR.** The cross-section times trigger acceptance is driven by pT(QQ̄) ≳ 200-300 GeV. 1911.02223 finds σ(QQ̄j, pT(j) > 200 GeV)/σ(QQ̄) ≈ 0.10 for E at 13 TeV [App.A]. NLO matched generation (MG5_aMC [QCD] + FxFx or MLM 0-2j) is needed for this fraction (Sec. 5).

---

## 3. Dynamics needed for simulation

### 3.1 Equations of motion

The action is the Nambu-Goto string with massive endpoints plus external forces [0805.4642 Eq.3.7; 1708.02243 Eq.2]:

  S = −m_Q Σ_i ∫dτ_i − σ∫dA + S_ext,  with σ = Λ².

Each endpoint obeys [0805.4642 Eq.3.8; 1708.02243 Eq.3; 1911.02223 Eq.III.1-III.3; 2002.07503 Eq.II.1-II.3]:

  d(m_Q γ v)/dt = −Λ² [ √(1−v⊥²) ŝ + v∥ v⊥ / √(1−v⊥²) ] + q v×B − ⟨dE/dx⟩(βγ, material) v̂ (+ radiation terms).

Here ŝ is the unit vector along the string at the endpoint, pointing outward, and v∥ and v⊥ are measured with respect to ŝ.

- **Straight-string approximation.** In the pair CM frame the string stays straight if F_ext ≪ Λ² [0805.4642 Eq.3.10]. Then ŝ ∥ (x₁ − x₂) evaluated at CM-simultaneous times. The lab-frame implementation requires the simultaneity condition t₁ − t₂ = β·(r₁ − r₂) and the matched time steps of [1911.02223 Eq.III.6-III.9; 2002.07503 Eq.VIII.1-VIII.4].
  - Fixing ŝ instead changes the plane thickness by up to mm. "Choosing the correct ŝ direction is critical in coplanar quirk search" [2002.07503 Sec.VIII, Fig.6]. This is a **validation item** for any propagator.
- **Size of the external forces relative to Λ² in the CMS tracker** (my ESTIMATE; inputs: eBc = 0.2998 GeV/m per T = (7.7 eV)² per T; Si MIP dE/dx = 3.9 MeV/cm):
  - Lorentz force at 3.8 T: (15 eV)². That is 2.5×10⁻³ Λ² at Λ = 300 eV and 2×10⁻⁴ Λ² at 1 keV.
  - Ionisation inside a silicon sensor: (8.8 eV)² at MIP and ≲ (60-90 eV)² for βγ ~ 0.1. The maximum ionisation force is ~(100 eV)² [0805.4642 Sec.3.4]. Averaged over the tracker the filling factor is ~0.05 [1911.02223 Sec.III.A; 1811.08903 Tab.1].
  - ⇒ The straight-string approximation is good to ≲ 1-4% of the string force over the whole target window, Λ ≥ 0.3 keV. It fails only for Λ ≲ 100 eV and in dense calorimeter/yoke material [0805.4642 Sec.3.4; 1811.08903 Sec.2].
- **Analytic solution** (F_ext = 0) [2002.07503 Eq.II.4-II.8]: the crossing time is t_p = 0.0658 ns × (ρ₁−ρ₂)/√(1−h²) × (m/100 GeV)(keV/Λ)². The first-order B-field correction gives the out-of-plane displacement z±(g) [2002.07503 Eq.II.20-II.21, App.A]. This gives **fast, event-by-event estimates** of the amplitude, the number of periods and the thickness, but it is valid only to within a factor ~10 for 1-100 periods [2002.07503 App.C, Fig.8].
- **Plane thickness** [1911.02223 Eq.III.12; derivation in 2002.07503 Eq.V.6-V.9]:
  - d_min ≈ 1.16 µm × (m_Q/100 GeV)(keV/Λ)⁴(|q|/e)(B_xy/T), where B_xy is the field component in the plane.
  - It scales as d ∝ m_Q q E_z ρ sinh⁻¹ρ / Λ⁴ for a neutral pair.
  - It is linear in the quirk charge for a neutral pair, and enhanced by the number of periods for a charged pair [2002.07503 Sec.V.A].
  - Knapen's torque estimate gives the plane-rotation angle Δφ ~ 10⁻⁵ (v_cm²/v²)(B/2 T)(2 keV/Λ)⁴ [1708.02243 Eq.8-9]. The ionisation torque gives ~10⁻³ per layer [1708.02243 Sec.II].

### 3.2 Ionisation energy loss

- Bethe-Bloch with the density effect for βγ ≳ 0.06 [1911.02223 Eq.III.4-III.5; 2108.06748 Eq.3.4-3.6].
- Lindhard-Scharff ∝ β for βγ ≲ 0.004 [2108.06748 Eq.3.7].
- An Anderson-Ziegler interpolation in between [1811.08903 Fig.1].
- Fluctuations: Landau-Vavilov or Bichsel in thin Si [1911.02223 Sec.III.A]. Li et al. use only a Gaussian 10% smear.
- In Geant4 the standard `G4hIonisation` (Bragg/BetheBloch models) with `G4hMultipleScattering` provides this natively for a heavy charged particle. The Athena quirk extension uses "standard Geant4 electromagnetic processes" [2607.26195 App.A].
- The low-velocity regime (β ≲ α) matters only for stopping and terminal velocity, i.e. Λ ≲ 150 eV [1811.08903 Sec.2]. It is **outside the target window**.

### 3.3 Radiation: glueballs (ε) and photons

- **Glueball emission.** Glueballs are emitted only when the quirk separation is ≲ Λ⁻¹. The acceleration Λ²/m_Q ≪ Λ suppresses emission at large separation [0805.4642 Sec.3.3, Eq.3.6; 1708.02243 Sec.II]. It is parameterised as probability ε per crossing to radiate energy ~Λ: dE/dt = −εΛ/T [1811.08903 Eq.B.3; 2404.13814 Eq.4.1]. The convention is ε = 0.1 [1811.08903 Sec.4; 2404.13814 Sec.4; 2607.26195 p.3], varied over [0.03, 0.3] or [0.01, 1] [2404.13814 Sec.6.4], or ±30% [2607.26195 p.5].
- **ESTIMATE for the CMS tracker** (inputs from Sec. 4, Tab. 4.2): the energy radiated is E_IC ≈ ε N_cross Λ.
  - Λ = 10 keV, N_cross ≈ 3×10³: ≈ 3 MeV.
  - Λ = 30 keV, N_cross ≈ 3×10⁴: ≈ 0.1 GeV.
  - Both are compared with E_int ~ 50-300 GeV.
  - The vacuum distance needed to radiate all of E_int, L_ann = (βγ)₀(βγ)_cm m_Q E_int/(εΛ³) [1811.08903 Eq.4.4], is ~km at Λ = 30 keV, m_Q = 500 GeV.
  - ⇒ **ε does not affect the tracker signature for Λ ≤ 30 keV.** The same conclusion is reached for 480 m by 2108.06748 (Eq.4.21, E_IC ~ 2(Λ/100 eV)²Λ). FASER finds the ε uncertainty relevant only for Λ ≳ 30 keV, because their flight path is 480 m [2607.26195 p.5].
- **EM (Larmor) radiation:** E_EM ~ 1.7×10⁻⁷ α_EM (Λ/100 eV)⁴ eV over 480 m [2108.06748 Eq.4.22]. This is negligible.
- **Pre-beam-pipe annihilation:** only for microscopic strings. For uncoloured quirks cτ ~ 10 cm (Λ/MeV)⁻³(m_Q/TeV)² [0805.4642 Eq.6.5]. The B field prevents annihilation for Λ ≲ MeV [0805.4642 Eq.6.3], and matter interactions randomise ℓ [0805.4642 Eq.4.2]. Annihilation is irrelevant for keV Λ.
- **Brown-muck deflection** of the pair by emission is negligible for colour-neutral quirks [2404.13814 Eq.4.9].

### 3.4 How existing studies generated and propagated events (and validated range)

| Study | Generator | Propagation | External forces / material | Geometry, PU | Validated range / caveats |
|---|---|---|---|---|---|
| Knapen et al. [1708.02243 Sec.III.A, IV] | MG5_aMC vector-like fermion + ≤1j, MLM-matched to Pythia8 | numerical EoM (Eq.3), straight string | uniform 2 T B_z; **no material in EoM** (torque argued negligible) | simplified ATLAS pixel+SCT **barrel only** (\|η\| ≲ 1.8); pixel-centre hits; 45 mm beam-spot smearing; 25 ns timing cut; ⟨µ⟩ = 50 Pythia8 min-bias via simplified detector of 1612.00850 | straight string valid for Λ ≫ 100 eV; ε_reco degrades for Λ ≳ 5 keV (pixel merging) and Λ ≲ 1 keV (Δw cut) [Tab.I]. Code later shared privately [2410.00269 Ack.] |
| Li, Li, Pei, Zhang [1911.02223; 2002.07503] | FeynRules UFO → MG5_aMC + Pythia8 | Euler EoM with simultaneity condition, step < 10⁻⁴ ns (m/100 GeV)(keV/Λ)² [Eq.III.10]; stops at 25 ns or exit from HCal | B (CMS, "4 T" in 2002.07503 Sec.II.C); mean dE/dx BB+LS+interpolation, material by filling factors (tracker 0.05, ECAL 0.33, HCAL 0.88); 10% Gaussian dE/dx smear | CMS barrel, 13 layers; 10 µm hit resolution; ⟨µ⟩ = 50 (Pythia8 A3) | optimised for Λ ~ 1 keV; analytic thickness within ×10 for n_T ≈ 1-100 [2002.07503 App.C]. No public code found (UNVERIFIED) |
| Farina-Low [1703.00912] | MG5 2.3.3 | straight-string EoM | CMS B = 3.8 T (and 0 T); no material | CMS tracker geometry [App.A]; helix χ² fit, 30 µm | HSCP/monojet recasts; long strings (Λ ≲ 1 keV) |
| Evans-Luty [1811.08903 Sec.2, App.A] | modified Pythia8 (coloured quirk hadrons) | straight string, continuous mean dE/dx (BB/LS/AZ) | B matched to the CMS map; cylindrical CMS material zones with fill factors ζ (Tab.1); ε_emit = 0.1 lifetime | CMS full detector for stopping | computed to Λ = 1 keV, checked to 10 keV (footnote 4); atomic-scale de-excitation "highly uncertain" (App.B) |
| Feng et al. FASER/FASER2 [2404.13814; 2108.06748] | FeynRules → MG5_aMC **NLO**, Pythia8 | Mathematica EoM through TAS/TAN/concrete/rock with BB+LS ionisation; analytic for Λ ≳ 3 keV | no B (the dipole changes the direction by ≤ 2×10⁻⁵ rad); ε, ε′ survival weights | far forward | Λ ∈ [100 eV, 100 keV] |
| **FASER search** [2607.26195 p.3, App.A] | MG5_aMC **LO** + Pythia8 (LHCb tune, Z-pT reweighting to LHCb data) | `PreFASERQuirkSim` (public C++, E. Welch) to the FASER front face, then **Geant4 with the Athena `Quirks` extension** inside FASER | LHC magnet field maps; analytic transport for Λ > 3 keV; ε = 0.1 survival probability | FASER full sim + digitisation | validated by track continuity, scintillator charge (≈ 2 MIP) and timing vs a straight-line reference [App.A] |
| Sha et al. GNN [2410.00269 Sec.III] | MG5_aMC QQ̄+j, Pythia8 | Knapen-Papucci trajectory code | B only; **no material, no PU, no noise** | 8- and 25-layer toy cylinders (r = 3.1-100 cm, \|z\| < 40-75 cm) | "Effects from pile-up remain to be studied" [Sec.VIII] |
| LHCb VELO [2601.09023 Sec.4] | toy, coloured quirk | standalone toy | no B in VELO; 100% hit efficiency, 10 µm | VELO geometry | coloured only |

### 3.5 Minimal correct simulation chain for CMS Phase-2, and what exists publicly

**Step 1: Generator (exists).**
- Process: pp → QQ̄ + 0, 1, 2 jets with MG5_aMC, MLM matched, or NLO [QCD] with FxFx/MC@NLO for the ISR spectrum.
- Model: any UFO with a vector-like charged Dirac lepton singlet with a custom stable PDG id (e.g. a heavy-lepton/VLL UFO, or a 4-line FeynRules model). N_IC enters only as an overall σ factor, set by the normalisation to the Sec. 2 table, since the kinematics are N_IC-independent. Li et al. built exactly such a UFO [1911.02223 Sec.IV]; it is not public (UNVERIFIED).
- Shower: Pythia8 CP5, with the quirks stable and not hadronised.
- Use a **generator filter pT(QQ̄) > 150-200 GeV**. The trigger requires ISR, and the fraction above 200 GeV is ≈ 0.10 [1911.02223 App.A].
- **Reuse each mass sample for all Λ**, because Λ does not enter production (beyond the < 15% Sommerfeld factor, Sec. 2.4).

**Step 2: Quirk-pair transport through the 3.8 T field and material (the missing piece in CMS).**
- Required physics:
  - (i) the string force with correct CM simultaneity, or the causal-string equivalent;
  - (ii) the Lorentz force in the full CMS field map;
  - (iii) standard Geant4 EM energy loss and multiple scattering of a charge-1 heavy particle;
  - (iv) **correct global time** of every step, needed for the OT/IT/MTD time windows (Sec. 4.3).
- ε and annihilation can be omitted for Λ ≤ 30 keV (Sec. 3.3). Annihilation after stopping in the calorimeter is irrelevant to the tracker analysis.
- Public options:
  - **(a) ATLAS Athena `Simulation/G4Extensions/Quirks`.** Public at gitlab.cern.ch/atlas/athena; file list checked 2026-10-07.
    - Contents: `Quirk` G4ParticleDefinition; `InfracolorForce` (a queue of "string vectors" carrying momentum F_string×length, i.e. a causal string rather than an instantaneous straight one); `QuirkTransportation` (a fork of G4Transportation, J. Black 2014, Geant4-9.4 era header, kept compiling in current Athena); `HyperbolaStepper`; `QuirkStackingAction` (alternating propagation of the two partners); `QuirkWatcher`; a debug stepping action; a **`standalone/` Geant4 example** (ExN03 physics list, test detector).
    - Configuration: MASS, CHARGE, PDGID, STRINGFORCE, plus numerical controls (first-string length 10⁻⁶ mm, maximum boost 10⁻², merge tolerances) [`python/QuirksConfig.py`]. The configuration adds a looper-killer user action.
    - Used and validated by FASER [2607.26195 App.A].
    - Licence: Athena project, licence field "Other"; QuirkTransportation carries the Geant4 licence header. Check before redistribution (UNVERIFIED).
  - **(b) `PreFASERQuirkSim`** (github.com/eliwelch17/PreFASERQuirkSim). Public C++17 port of the 2404.13814 Mathematica code: ionisation, LHC magnets, ε weights, fast analytic mode for Λ ≳ 3 keV. It is **forward-beamline specific** (TAS/TAN/rock). Its string and ionisation stepping core could be reused for a standalone CMS toy. No licence is stated.
  - **(c)** The Knapen-Papucci and Li-Pei central-detector codes are not public.
- **CMSSW integration (`SimG4Core`) would need:**
  1. Particle-table entries for the quirk PDG ids, in the HepPDT table used by `SimGeneral/HepPDTESSource`, so that the gen-to-G4 conversion keeps them. This is analogous to the existing HSCP/`CustomPhysics` path.
  2. A physics constructor that attaches `QuirkTransportation` (replacing G4Transportation for quirks only) plus `G4hIonisation` and `G4hMultipleScattering`. `SimG4Core/CustomPhysics/src` contains R-hadron, SIMP, dark-photon and SQ processes but **no quirk code** (directory listing checked 2026-10-07). The CMS monopole implementation (custom equation of motion in a field) is the closest structural analogue (UNVERIFIED location in `SimG4Core`).
  3. Stacking. Athena's `QuirkStackingAction` forces the two partners to be stepped alternately. CMS has its own `StackingAction` (`SimG4Core/Application`), so the quirk logic must be merged there, or implemented as a G4 sub-event or suspend mechanism.
  4. Field. CMS uses its own field manager and stepper (`SimG4Core/MagneticField`). The quirk transport carries its own stepper (`HyperbolaStepper`/`DummyEquation`), so the CMS field must be accessible to it, with tracker-volume step limits.
  5. Exempt quirks from looper or step-number killers and from short `MaxTrackTime` cuts. A pair makes up to ~10⁴ crossings in the tracker (Sec. 4.2), and at m_Q ≥ 500 GeV the transit time to the muon system is ≫ 25 ns.
  6. Keep `SimHit` time of flight exact.
  7. Validate against the analytic solution [2002.07503] and the plane-thickness formula, plus the FASER-style checks (continuity, ~2 MIP charge for merged pairs, timing) [2607.26195 App.A].
- A fast standalone propagator, e.g. the Athena standalone version or my own straight-string code, is recommended **in parallel** for Λ- and m-scans, using a parameterised CMS geometry (Tab. 4.1).

**Step 3: Hits per layer.** Standard CMSSW tracker sensitive detectors for the Phase-2 geometry (IT TBPX/TFPX/TEPX, OT TBPS/TB2S/TEDD), and the MTD BTL and ETL sensitive detectors. The physics needs nothing beyond correct times.

**Step 4: Digitisation (exists, but its behaviour for slow, heavily ionising hits must be checked).**
- `Phase2TrackerDigitizer`: IT pixel with ToT charge; OT PS/2S binary.
- MTD digitisation; PU200 premixing.
- Issues specific to quirks:
  - the time window / BX assignment of late hits (Sec. 4.3);
  - IT ToT saturation for hits with ≳ 10× MIP (UNVERIFIED dynamic range);
  - stub formation in OT modules for quirk hit pairs (whether two quirks within the module stub window form stubs is untested [`research/reviews/feasibility/C001.md` §5]).

**Step 5:** reconstruction (plane finder, GNN, trajectory fit) is outside the theory scope.

---

## 4. Signature map vs (m_Q, Λ) for the CMS Phase-2 tracker (ATLAS ITk secondary)

### 4.1 Geometry and inputs

| Item | CMS Phase-2 (primary) | Source / status |
|---|---|---|
| Solenoid field | **3.8112 T** | CMSSW `L1Trigger/TrackFindingTracklet/interface/Settings.h` `bfield_` (read 2026-10-07) |
| IT barrel (TBPX), 4 layers | r ≈ 2.8-3.0 cm (L1) … 14.6 cm (L4) | the L1 radius is quoted as 28 mm in 2023 and 30 mm in earlier documents; L2-L3 ≈ 6.1/10.4 cm are UNVERIFIED (CMS-TDR-014; CDS was not reachable) |
| IT pixel pitch | 25×100 µm² | UNVERIFIED (Phase-2 IT TDR) |
| OT barrel, 6 layers | **r = 24.9, 37.2, 52.3 (PS); 68.8, 86.0, 108.3 cm (2S)** | CMSSW tracklet `irmean_` × 120/4096 cm; PS < 60 cm < 2S [2210.07766 Sec.2] |
| OT endcap disks (TEDD) | \|z\| ≈ 131, 155, 185, 222, 265 cm | CMSSW tracklet `izmean_` × 120/2048 cm |
| OT 2S module | strips 5 cm × 90 µm (two sensors), **binary readout (CBC), BX-tagged** | [2210.07766 Sec.2, lines 99-109] |
| OT PS module | strips 2.35 cm × 100 µm + macro-pixels 1.5 mm × 100 µm, binary (SSA/MPA) | [2210.07766 Sec.2] |
| MTD BTL | inner r = 114.8 cm, \|η\| < 1.45-1.48, LYSO+SiPM, σ_t ≈ 30-60 ps over lifetime | design talks (LIP 2021 seminar; CERN detector seminar); TDR CERN-LHCC-2019-003 not re-read: UNVERIFIED |
| MTD ETL | z ≈ ±3.0 m, 1.6 < \|η\| < 3.0, LGAD, ~35-40 ps/track | same: UNVERIFIED |
| ATLAS ITk (secondary) | B = 2 T; pixel barrel r ≈ 3.4, 9.9, 16.0, 22.8, 29.1 cm; strip barrel r ≈ 40.5, 56.2, 76.2, 100 cm | UNVERIFIED (ITk TDRs not re-read); Sha et al. toy r = 3.1-100 cm [2410.00269 Sec.III] |

**Kinematics toy** (ESTIMATE, `sigmap.py`, App. A):
- LO DY (M_QQ̄, y_QQ̄) sampled from CT18NLO at 14 TeV.
- The pair is then given a fixed ISR recoil pT(QQ̄) of 250 or 500 GeV, as a proxy for a Phase-2 MET/jet trigger.
- Pair |η| < 1.5 is required for "central" quantities.
- No external forces in the transport.

CM velocity of each quirk at production:

| | m_Q = 200 | 500 | 1000 GeV |
|---|---|---|---|
| fermion E: γ* (16/50/84%) | 1.10/1.30/1.77 | 1.08/1.25/1.60 | 1.07/1.19/1.43 |
| fermion E: β* median | 0.64 | 0.60 | 0.54 |
| scalar Ẽ: γ* (16/50/84%) | 1.23/1.55/2.18 | 1.19/1.43/1.90 | 1.15/1.32/1.63 |

Cross-check: Sha et al. quote mean quirk γ̄ = 1.8 (500 GeV) and 1.4 (1 TeV) for QQ̄+j samples in the lab frame [2410.00269 Tab.I]. This is consistent once the lab boost is included.

### 4.2 Amplitude, number of oscillations, coplanarity (CMS, 3.8 T)

**Table 4.2a.** Maximum CM separation ℓ_max = 2(γ*−1)m_Q/Λ² (median and 16-84%) and number of string crossings inside the tracker, for central pairs with pT(QQ̄) = 250 GeV. Fermion `E`; ESTIMATE from App. A. The tracker boundary is r < 108 cm, |z| < 265 cm, with no time cut.

| Λ [keV] | m_Q = 200 GeV: ℓ_max | N_cross | m_Q = 500 GeV: ℓ_max | N_cross | m_Q = 1000 GeV: ℓ_max | N_cross |
|---|---|---|---|---|---|---|
| 0.3 | 25 cm (8-63) | 2.5 (1.4-4.6) | 51 cm (16-127) | 2.8 (1.6-5.2) | 80 cm (29-182) | 3.1 (2.0-5.4) |
| 1 | 2.2 cm (0.7-5.7) | 28 | 4.6 cm (1.4-11) | 31 | 7.2 cm (2.6-16) | 35 |
| 3 | 2.5 mm | 250 | 5.1 mm | 275 | 8.0 mm | 310 |
| 10 | 220 µm (70-570) | 2.8×10³ | 460 µm (140-1140) | 3.1×10³ | 720 µm (260-1630) | 3.5×10³ |
| 30 | 25 µm (8-63) | 2.5×10⁴ | 51 µm (16-127) | 2.8×10⁴ | 80 µm (29-182) | 3.1×10⁴ |

- At pT(QQ̄) = 500 GeV, N_cross is about halved and ℓ_max is unchanged.
- The scalar Ẽ has ℓ_max larger by ×1.7-1.8 (larger γ*−1).
- The lab-frame transverse width is ≤ ℓ_max: it is the projection perpendicular to the pair boost, L in [2002.07503 Eq.III.1].
- The scaling agrees with 1911.02223 Fig.5 (CMS, 100 GeV, Λ = 1-2 keV), and with Li et al. Ncross ~ 20(Λ/100 eV)² per 480 m for FASER [2108.06748 Eq.4.20].

**Table 4.2b.** Expected plane thickness d ≈ 1.16 µm (m_Q/100 GeV)(keV/Λ)⁴ (B_xy/T) [1911.02223 Eq.III.12]. The column headers give the CMS value for B_xy ≈ 3.8 T. ATLAS (2 T) values are ×0.53. Analytic accuracy is a factor ~10 [2002.07503 App.C], and the formula *over*estimates d when n_T ≲ 1 (Λ ≲ 0.3 keV). ESTIMATE.

| Λ [keV] | m_Q = 200 | 500 | 1000 GeV |
|---|---|---|---|
| 0.3 | ~1.1 mm | ~2.7 mm | ~5.4 mm |
| 0.5 | 140 µm | 350 µm | 700 µm |
| 0.6 | 68 µm | 170 µm | 340 µm |
| 1 | 9 µm | 22 µm | 44 µm |
| 2 | 0.6 µm | 1.4 µm | 2.8 µm |
| **Λ where d = 100 µm** (Knapen's Δs cut is 100 µm [1708.02243 Sec.IV]) | **0.55 keV** (ATLAS 0.46) | **0.69 keV** (0.58) | **0.81 keV** (0.69) |

Numerical cross-check: 2002.07503 Fig.4 shows d ~ O(10-100) µm for m = 100 GeV, Λ = 632 eV, 4 T. Li et al. find d ≲ O(100) µm for Λ ∈ [O(100) eV, O(1) keV] at m = 100 GeV [1911.02223 Sec.III.C].

Hit resolution versus separation (ESTIMATE):
- IT: 25 µm pitch, so two quirks merge below ~50 µm separation.
- OT rφ: 90-100 µm pitch, so they merge below ~200 µm.
- OT z: **2S modules give only 5 cm strip-length z information (σ_z ≈ 1.4 cm)**, and PS macro-pixels give 1.5 mm (σ_z ≈ 0.43 mm). The 3D plane fit at CMS therefore relies on the IT (4 layers + disks) and the 3 PS layers. The 2S layers constrain only rφ.
- This differs from the ATLAS-SCT-based assumption of Knapen et al. (stereo strips, "twice the intrinsic accuracy" [1708.02243 Sec.III.A]). It needs an experimental check.

### 4.3 Velocity, timing (MTD), dE/dx, reach of outer detectors

**Table 4.3.** Pair transverse velocity β_T and arrival time at the BTL (r = 114.8 cm) for central pairs. A β = 1 particle arrives at 3.8 ns. ESTIMATE from App. A; fermion E, values for the scalar similar within 10%.

| m_Q | pT(QQ̄) = 250 GeV: β_T (16/50/84) | t_BTL median [ns] | frac. delay < 12.5 ns | pT(QQ̄) = 500 GeV: β_T | t_BTL | frac. delay < 12.5 ns |
|---|---|---|---|---|---|---|
| 200 GeV | 0.11/0.23/0.39 | 10.0 | 0.97 | 0.19/0.38/0.62 | 7.0 | 1.00 |
| 500 GeV | 0.09/0.14/0.19 | **19.8** | **0.02** | 0.18/0.27/0.36 | 11.4 | 0.95 |
| 1000 GeV | 0.07/0.09/0.11 | **36.7** | **0.00** | 0.14/0.17/0.21 | **19.1** | **0.02** |

Consequences:
- The pair moves at β_T ~ 0.1-0.4. The ns-scale delays at the BTL are ≫ the MTD resolution of 30-60 ps, so **MTD timing is a near-perfect slow-pair tag** *if the hit is recorded*.
  - Literature cross-checks: Li et al. find v_T ~ 0.1 for the pair and a 10-20 ns tracker transit time [1911.02223 Sec.IV]. Knapen et al. apply a 25 ns cut that "causes a slight drop in ε_fid for heavier quirks" [1708.02243 Sec.IV].
- **Threat (new, ESTIMATE).** For m_Q ≳ 500 GeV and trigger-level ISR (pT ~ 250 GeV), most pairs reach the outer OT layers (r ≈ 0.7-1.1 m) **≳ 10-15 ns late**. The OT front ends are binary and BX-tagged [2210.07766 Sec.2]. If hits outside the triggered-BX sampling window are lost or assigned to BX+1, high-mass acceptance collapses unless the analysis reads out adjacent BXs.
  - The same applies to the BTL (TOFHIR) and to L1 muon-trigger timing. The muon system at r ≳ 4 m is reached after ≳ 70-150 ns for β_T = 0.1-0.2, so an L1 muon trigger is not viable above ~500 GeV. Compare the 25 ns caveat in [1708.02243 Sec.III.B].
  - The exact OT/IT/BTL time-acceptance windows are UNVERIFIED. This must go to the experimental-status agent.
  - The 12.5 ns figure in Table 4.3 is an illustrative half-BX threshold, not a CMS parameter.
- **Velocity of the individual quirks.** In the linear potential the momentum falls linearly in time, so the **time-weighted p is uniform on [0, p*]**. The CM βγ of each quirk is therefore spread from 0 to β*γ* (median ≈ 0.75 at 500 GeV).
  - Combined with β_T ~ 0.15-0.4, the lab βγ per hit is typically 0.2-1. This gives dE/dx ≈ 2-10× MIP per hit, with a tail to ≳ 50× MIP near turning points (ESTIMATE from Bethe-Bloch).
  - Literature: the ATLAS-pixel dE/dx of an 800 GeV EW quirk extends to ~100 MeV cm²/g (≈ 60× MIP), with βγ from 10⁻³ to 10 [1708.02243 App.A, Fig.7]. Li et al. cut at dE/dx > 3 MeV/cm and use S_p ≥ 50 MeV/cm [1911.02223 Sec.IV.B].
  - **At CMS, only the IT (ToT) measures charge; the OT is binary.** So dE/dx comes from ≤ 4 barrel layers plus disks. ToT saturation for ≳ 10× MIP is UNVERIFIED.
- **Merged regime** (Λ ≳ 20-30 keV): two collinear charges give ≥ 2× MIP. D0 required "large ionization (≳ 15 MeV/cm)" [1008.3547, line 335 of text]. FASER uses "approximately twice the measured charge of a single muon" [2607.26195 p.4].
- **Reaching the calorimeter and muon system; stopping.**
  - Within 25 ns, O(10)% of pairs do not reach the ECAL and ≳ 50% do not reach the HCAL (CMS, m_Q = 100-700 GeV, pT > 100 GeV) [1911.02223 Sec.IV, Fig.6]. Energy deposited in the calorimeters within 25 ns is ≲ 5 GeV [1911.02223 Sec.V].
  - Effect on MET: quirk energy deposits change the MET-cut efficiency by ≈ 5% [2002.07503 Sec.VII].
  - Stopping fraction: 1-5% of E-like pairs (400 GeV) stop in the CMS ECAL+HCAL at |η| < 1, flat for Λ ≳ 300 eV, and a similar number stop in the iron yoke. **Essentially none stop in the tracker** [1811.08903 Fig.2, Fig.6, Fig.7].
  - Most heavy pairs therefore exit the tracker, cross the calorimeters slowly and leave the detector. This is the MET + ISR topology.
- **Multiple hits per layer.** 10-20% of events have > 2 quirk hits on at least one CMS layer, rising with Λ and m/pT [2002.07503 Tab.I]. More than 2 hits per layer occur when the layer radius lies between the projected D′ and L′ [2002.07503 Sec.VI, App.D].

### 4.4 Regime map for CMS (summary; ESTIMATE unless cited)

| Λ range | Topology in CMS Phase-2 tracker | Coplanar plane-finder | Better tool |
|---|---|---|---|
| ≲ 0.1-0.2 keV | ℓ_max ≳ 1 m; ≤ 1 crossing; tracks nearly helical | n/a | HSCP searches (fermion E N=2: 650 GeV at 1 eV, 150 GeV at 100 eV [1703.00912 Tab.II]); OoT stopped [1811.08903] |
| **0.3-0.6 keV** (low edge) | ℓ_max 10 cm-1 m, 1-5 crossings; thickness 0.1-5 mm at 3.8 T | **fails** (Δs > 100 µm) | trajectory χ² fit / GNN (79-83% track eff. at 500 eV [2410.00269 Tab.I]); a **genuine gap**, since FASER is weak here (57 GeV at 300 eV, 72 GeV at 500 eV [HEPData t2]) |
| **0.6-10 keV** (core) | ℓ_max 0.2 mm-10 cm, 10¹-10³ crossings, thickness ≤ 100 µm, 2 hits/layer, slow pair | **works** (ε_reco up to 0.65-0.74 for 3-5 keV at 800 GeV [1708.02243 Tab.I]) | add dE/dx (IT), MTD timing, MET-plane alignment |
| 10-20 keV | ℓ_max 70 µm-1.6 mm: resolved in IT, partly merged in OT | degrading (pixel/strip merging; ε_reco 0.58 at 10 keV for 1.8 TeV coloured [1708.02243 Tab.I]) | IT-only plane + dE/dx |
| ≳ 20-30 keV (high edge) | ℓ_max ≲ 100 µm: one straight, very-high-pT, ≥ 2× MIP track | **fails** (unresolved) | D0-type HIP straight-track search [1008.3547]; FASER covers up to 100 keV |

---

## 5. Signal systematics (search convention: signal-normalisation and acceptance nuisances)

| Source | Recommended treatment | Size | Reference / status |
|---|---|---|---|
| σ: PDF | PDF4LHC21 envelope from WG-style tables, mass-dependent | ±3.3% (150 GeV), ±6.6% (500), ±11.9% (800), ±18.5% (1000), ~±25% (1200) | SUSY xsec WG 13.6 TeV right-selectron NNLL json (`unc_pdf_*`); FASER used 2-4% for m_Q ≲ 200 GeV [2607.26195 p.5] |
| σ: scale | NNLL-resummed scale variation | ≤ 1% (13.6 TeV WG); LO would be 1-10% | WG json `unc_scale_*`; Sec. 2.3 |
| σ: scalar→fermion K transfer and EW input scheme | flat nuisance | ±5% (ESTIMATE; the K cross-check vs 2404.13814 agrees within 6%; α(M_Z) vs G_µ differs by 7% in σ) | Sec. 2.2, 2.4 |
| σ: IC Sommerfeld / threshold | one-sided theory uncertainty (or include as a correction) | +5 to +15% (ESTIMATE) | [0805.4642 Sec.3.2] flags it, no calculation exists |
| ISR modelling → MET/jet-trigger acceptance | vary ME μ_R, μ_F (×½, ×2), Pythia ISR shower scale (×½, ×2) and the matching scale; compare LO-MLM(0-2j) with NLO-FxFx | 10-20% expected (ESTIMATE); FASER saw ≈ 25% from shower ×0.5/×2 for its forward acceptance [2607.26195 p.5]; NLO raises acceptance-sensitive fractions [2404.13814 Sec.3] | trigger fraction pT(j) > 200 GeV ≈ 0.10 [1911.02223 App.A; 1708.02243 Tab.I] |
| Glueball radiation ε | **no nuisance needed** for Λ ≤ 30 keV in the tracker; document a check with ε ∈ [0.03, 0.3] | < 0.1% of the pair energy (ESTIMATE, Sec. 3.3) | FASER: 1-20%, relevant only for Λ ≳ 30 keV over 480 m [2607.26195 p.5] |
| Energy-loss model (dE/dx scale, straggling) | data-driven dE/dx calibration of the IT ToT (as in HSCP searches); ±scale on Geant4 BB | ±5-10% on the dE/dx scale (UNVERIFIED, HSCP-typical); trajectory effect negligible (F_ion ≪ Λ²) | [0805.4642 Sec.3.4; 1708.02243 Sec.II]; low-β (LS/AZ) region only matters for stopping, Λ ≲ 150 eV [1811.08903] |
| Material description | vary the tracker material budget ±5-10% | small for signal (Δφ ~ 10⁻³ per layer [1708.02243 Sec.II]); larger for conversion backgrounds (experimental) | ESTIMATE |
| B-field map | use the official CMS map in Geant4 | negligible (thickness ∝ B, so a 0.1% map error gives a 0.1% thickness change) | ESTIMATE; Evans-Luty used a data-matched map [1811.08903 Sec.2] |
| String-dynamics modelling | compare the causal-string Athena transport with a straight-string integrator (correct ŝ simultaneity) on thickness and efficiency | few % expected in the core; possibly larger at Λ ≲ 0.6 keV (ESTIMATE). A wrong ŝ gives mm-level errors [2002.07503 Fig.6] | validation item |
| Hit-time / readout-window modelling | propagate exact SimHit times; vary the time-window edges | **potentially dominant acceptance effect for m_Q ≳ 500 GeV** (Sec. 4.3) | ESTIMATE; experimental owner |
| Pile-up overlay (PU200) | experimental | − | no quirk study above ⟨µ⟩ = 50 [1708.02243; 1911.02223]; none with PU [2410.00269] |
| Luminosity | HL-LHC value | ~1-1.5% (UNVERIFIED target); FASER Run 3: 2.2% [2607.26195 p.5] | − |
| MC statistics | set by Sec. 7 sample sizes | FASER: ≈ 6%, up to 28% at small Λ [2607.26195 p.5] | − |

The Λ convention (√σ vs T_c) and N_IC are **definitions or model parameters, not nuisances**. Results should be quoted per (m_Q, Λ ≡ √σ) for N_IC = 2, and σ-limits normalised per N_IC.

---

## 6. Theory consistency

### 6.1 Cosmology [2512.20696]
- The UV freeze-in of dark gluons (γγ → g′g′ through a dimension-8 operator), followed by long-lived 0^{++} glueballs decaying to γγ, gives several constraints: BBN, CMB, γ-ray, overclosure, SIDM and ΔN_eff. **Together they require T_RH ≲ O(100 GeV)** over the "entire quirky parameter space", in the range T_RH ≲ O(10⁻¹-10³) GeV depending on (m_Q, Λ) [abstract; Sec.4.1, Fig.4; Sec.6].
- The bounds are insensitive to the SM quantum numbers and to Higgs Yukawas [Sec.4.3.1-4.3.2, Sec.6]. For macroscopic strings they survive even if glueballs decay invisibly, because ΔN_eff from BBN is unchanged [Sec.4.3.3, App.B, Sec.6].
- The assumptions include T_RH ≲ m_Q/25 and a reheating sector that does not populate the dark sector [Sec.4.2].
- If the dark sector ever thermalises with the SM, ΔN_eff at BBN "marginally rules out" N = 2 and rules out N ≥ 3 [Sec.4.1, footnote 5]. This applies above the equilibrium line in Fig.4.
- Glueball dark matter requires m_Q ≳ 10 TeV and Λ ≳ 40 MeV [Sec.5], so it is **incompatible** with collider-accessible quirks.
- Λ conversion: their Λ = T_c ≈ 0.6√σ (Sec. 1.1). Their keV corresponds to ~1.7 keV in our convention.
- Kang-Luty: there is no model-independent cosmological constraint once T_RH ≲ GeV [0805.4642 Sec.2.3].
- **Verdict:** nothing excludes the target region. A discovery would imply non-standard, low-reheat cosmology, in tension with leptogenesis and EW baryogenesis [2512.20696 Sec.6]. This **adds motivation** ("a discovery has far-reaching cosmological implications"); it is not a constraint. State it in the strategy introduction, not as a limit.

### 6.2 Naturalness of keV Λ
- Λ = µ₀ exp(−8π²/(b g₀²)) is log-flat: "each decade of energy is roughly equally likely" [0805.4642 Eq.1.2].
- A GUT-compatible example [0805.4642 Sec.2.5]: MSSM + SU(2)_IC with 5⊕5̄ quirks gives Λ ~ 100 MeV. Adding 1, 2, 3 extra IC-fundamental pairs above a TeV gives Λ ~ MeV, 10 keV, 100 eV.
- ESTIMATE (1-loop, pure SU(2) YM below m_Q, b₀ = 22/3): α_IC⁻¹(m_Q = 500 GeV) = (b₀/2π) ln(m_Q/Λ) = 24.7, 23.4, 19.4 for Λ = 0.3, 1, 30 keV. **The whole target window is a ~25% range of the IC coupling at the quirk mass**, α_IC(m_Q) ≈ 0.040-0.052. Numerically this is not fine-tuned, but nothing predicts it either.
- Neutral-naturalness top partners prefer GeV-scale Λ (folded SUSY, quirky little Higgs, twin Higgs) [`research/reviews/theory/C001.md` §5; 2601.09023 Sec.1, "few GeV"]. **The mesoscopic window is signature-driven** (generic hidden confining sector), not naturalness-driven. This is unchanged from Gate 4.

### 6.3 EW precision, LEP and other direct limits on charged EW states
- **EWPT.** A vector-like singlet with an EW-preserving mass has no tree-level effect, and S = T = 0 because there is no EWSB mass splitting [0805.4642 Sec.2.4]. One-loop universal W, Y parameters scale as ∝ N_IC α m_W²/(4π m_Q²) ≲ 10⁻⁴ for m_Q ≥ 200 GeV and N_IC = 2 (ESTIMATE). They matter only at large N [2512.20696 Sec.4.2 mentions the W parameter for large N]. Split doublets are constrained to Δ < 43 GeV [2504.02940 Sec.3.1, via `research/reviews/theory/C001.md`].
- **LEP II.** EW-charged squirks at 80 GeV are "essentially ruled out" by the LEP II hadronic σ (±0.5 pb). Charged states > 100 GeV are beyond LEP II sensitivity [1106.2569 Sec.I item 5, Sec.III.B]. A generic LEP-II kinematic bound for pair-produced charged states is ≈ √s/2 ≈ 100-104 GeV (UNVERIFIED for quirks specifically).
- **D0:** m_Q > 107 GeV (N = 2) for 10 keV < Λ < 1 MeV [1008.3547 abstract].
- **FASER (observed):** 57/72/113/149/163/179/173 GeV at Λ = 0.3/0.5/1/1.7/3/10/30 keV [HEPData ins3184325 t2].
- **Farina-Low:** HSCP/monojet recasts, 12.9 fb⁻¹, fermion (1,1)_{−1}, N = 2: 150 GeV at Λ = 100 eV, nothing at 1 keV [1703.00912 Tab.II]. **No full-Run-2 or Run-3 recast exists** (UNVERIFIED). The strategy should note that a Run-2 monojet recast could reach ~200-300 GeV (no calculation; flag only).
- **Higgs couplings:** the singlet E has no renormalisable Higgs coupling (no Yukawa, by IC charge), so h → γγ is unmodified.
- **In-flight annihilation:** none, since a single ionisation changes ℓ by ∆ℓ ~ m_e L ≫ 1 [0805.4642 Eq.4.2], and B prevents re-annihilation for Λ ≲ MeV [Eq.6.3].
- **Doublet/triplet states:** the charged→neutral β-decay on the mm-cm scale (Sec. 1.3) **reshapes** the topology for non-singlet representations. This is why the singlet E is primary.

**Net effect on the target:**
- Nothing kills it.
- The lower mass edge is set by FASER, D0 and LEP: ≈ 110-180 GeV depending on Λ.
- The usable Λ window for the *coplanar* method at CMS is ≈ 0.6-15 keV (Sec. 4.4). A GNN/trajectory method is needed for 0.3-0.6 keV.
- High-mass acceptance is threatened by slow-pair timing (Sec. 4.3).
- FASER2 (if built) projects discovery to 1.0 TeV for E at 3 ab⁻¹ [2404.13814 Sec.7], comparable to the CMS ESTIMATE in Sec. 7. FASER2 is not approved [2601.09023 Sec.2].

---

## 7. Recommended Phase-2 signal grid and event counts

**Rate-based reach** (ESTIMATE): N = σ₁₄ × 3 ab⁻¹ × ε_tot, with ε_tot = 0.10 × 0.28 × 0.65 ≈ 0.018 (Knapen 800 GeV, Λ = 3 keV [1708.02243 Tab.I]).

| m_Q | N |
|---|---|
| 500 GeV | 330 |
| 750 GeV | ~50 |
| 1000 GeV | 11 |
| 1250 GeV | ~3 |

⇒ The 3-event (background-free) reach is ≈ 1.2 TeV, **before** any loss from the hit-timing effects of Sec. 4.3. The grid must extend to 1.25 TeV.

**Primary `E` (N_IC = 2):**
- m_Q ∈ {200, 350, 500, 750, 1000, 1250} GeV × Λ ∈ {0.3, 0.6, 1, 2, 5, 10, 20, 30} keV, giving 48 points. The Λ values cover:
  - 0.3 keV: low-edge GNN regime and the FASER gap;
  - 0.6 keV: coplanar onset at 3.8 T;
  - 1, 2, 5 keV: core;
  - 10, 20 keV: merging onset;
  - 30 keV: single-HIP regime and FASER overlap.
- 200 GeV sits above all existing limits at every Λ (FASER max 179 GeV). 1250 GeV is the rate limit.
- **Generation strategy:**
  - One MG5_aMC sample per mass with a pT(QQ̄) > 150 GeV filter, 0-2j MLM, or NLO FxFx at 2 masses for the ISR systematic.
  - Store the LHE and GEN output, and propagate the *same* events at each Λ in the quirk-transport step. Λ enters only there, so Λ-to-Λ differences are free of generator fluctuations.
- **Events per point:** ≥ 10k filter-passing events per (m_Q, Λ) with full Phase-2 simulation and PU200. **Minimum 5k.** **20k at the grid edges** (Λ = 0.3 and 30 keV, m_Q = 1250 GeV), where ε_tot drops to ≲ 1%.
  - Rationale: after the pT filter, ε_fid × ε_reco × ε_trigger|filter ≈ 0.28 × 0.5 × 0.5 ≈ 0.07 (ESTIMATE from [1708.02243 Tab.I]). 10k events then give ≈ 700 selected, i.e. ~4% statistical precision. At ε ≈ 1%, 20k give ~7%. This matches FASER's 6% MC-stat for typical points [2607.26195 p.5].
  - ML trackers need ≥ 3k events per point for training (2k/400/400 in [2410.00269 Sec.IV]), which is covered.
- **Total:** ≈ 48 × 10k + 8 edge points × 10k extra ≈ 0.56 M events (full sim, PU200).
- **A fast-propagator scan** (standalone transport plus parameterised CMS geometry, no PU) on a fine grid of 10 masses × 15 Λ values, 0.2-50 keV log-spaced, with 50k events each, maps the regime boundaries (Tables 4.2-4.3) cheaply before full simulation.

**Alternate A1 `Ẽ`** (spin and kinematics): m_Q ∈ {200, 500, 750} × Λ ∈ {0.6, 3, 10} keV, 9 points × 10k. The rate is lower by ×11-18, so the reach is ≲ 600 GeV (cf. FASER2 Ẽ reach 600 GeV [2404.13814 Sec.7]).

**Alternate A2 `L` doublet** (topology): m_Q = 500 GeV × Λ ∈ {1, 5} keV, including both QQ̄ (γ/Z) and Q^±Q^0 (W). 2 points × 5k. A Q^± → Q^0π^± decay with cτ as a free parameter (default 7 mm, ESTIMATE) must be implemented in the transport.

**Validation samples (no PU, 5k each):**
- (i) Λ = 0.05 keV at 500 GeV: HSCP-like limit, checks the transport against standard tracking.
- (ii) Λ = 1 keV at 500 GeV with B = 0: pure string dynamics, compared with the analytic solution [2002.07503].
- (iii) the same point propagated with the straight-string integrator and with the Athena causal-string code (Sec. 5).

**Signal-model weights to store per event:**
- ME scale (×½, ×2);
- PDF4LHC21 replicas or Hessian members;
- Pythia ISR/FSR shower-scale weights;
- the true pair kinematics (M_QQ̄, pT, y, γ*, opening angle);
- the true SimHit time of every quirk hit.

---

## Appendix A. Reproducibility of the ESTIMATE numbers

1. **Cross sections:** `dy_xsec.py` in the agent scratchpad (not committed).
   - LHAPDF lhagrid1 reader using scipy bicubic splines in (ln x, ln Q²); sets CT18NLO_0000 and NNPDF23_lo_as_0130_qed_0000 downloaded from lhapdfsets.web.cern.ch.
   - Partonic qq̄ → γ*/Z → QQ̄ for a vector-like singlet; colour average 1/3; five flavours; μ = √ŝ (×½, ×2); quad integration over ln τ and trapezoid over ln x₁.
   - Validated against the WG scalar tables (Sec. 2.2).
   - Raw LO output per N_IC = 1 (CT18NLO, fermion, μ = √ŝ) in fb at 13/13.6/14 TeV:
     - 200 GeV: 88.0/94.6/99.1;
     - 500 GeV: 2.205/2.460/2.636;
     - 1000 GeV: 0.0588/0.0703/0.0785.
   - Scalar at 13 TeV: 7.63 (200), 0.162 (500), 0.00344 (1000).
2. **Kinematics toy:** `sigmap.py`.
   - Weighted sampling of (τ, x₁) with the LO integrand; 60k events per (spin, m_Q); 14 TeV.
   - Fixed pT(QQ̄) of 250 or 500 GeV added to the LO pair; central = |η_QQ̄| < 1.5.
   - ℓ_max = 2(γ*−1)m_Q/Λ²; crossings = CM proper time to leave (r < 108.3 cm, |z| < 265 cm) divided by the CM half-period 2γ*β*m_Q/Λ²; t_BTL = 114.8 cm/(β_T c).
   - No energy loss, no B-field effect on the CM motion, no time cut, no ISR-angle correlation. These are order-of-magnitude regime boundaries, not efficiencies.

## References used (all opened or downloaded in this session unless marked)
- 0805.4642 Kang, Luty: Macroscopic strings and quirks (read in full).
- 1106.2569 Harnik, Kribs, Martin: Quirks at the Tevatron and beyond (LEP II, EWPT appendix).
- 1703.00912 Farina, Low: HSCP/monojet recasts (read in full).
- 1708.02243 Knapen, Lou, Papucci, Setford: coplanar hits (read in full).
- 1811.08903 Evans, Luty: stopping quirks (read in full).
- 1911.02223 Li, Li, Pei, Zhang: energy loss in the tracker (read in full).
- 2002.07503 Li, Li, Pei, Zhang: the quirk trajectory (read in full).
- 2108.06748 Li, Pei, Ran, Zhang: FASER/FASER2 (energy-loss and radiation sections).
- 2404.13814 Feng, Li, Liao, Ni, Pei: FASER/FASER2 timing (read; Sec.2-7).
- 2410.00269 Sha et al.: GNN quirk tracking (read in full).
- 2509.08878 Condren, Whiteson: unexpected non-helical tracks (abstract only).
- 2512.20696 Asadi, Kribs, Luty: Quirks live in cool universes (Sec.1-6).
- 2601.09023 Cid Vidal et al.: LHCb VELO (read in full).
- 2607.26195 FASER: first quirk search (read in full); HEPData ins3184325, doi 10.17182/hepdata.181308.v1, tables t1 and t2 (downloaded).
- 1008.3547 D0 quirk search (abstract and limits).
- 2210.07766 CMS Outer Tracker for HL-LHC (module types, readout).
- LHC SUSY xsec WG tables via github.com/fuenfundachtzig/xsec/json: `pp13_slep_R_NLO+NLL_PDF4LHC.json`, `pp13600_sleptons_2000011_-2000011_NNLL.json`, `pp13600_hino_deg_*_NNLL.json` (downloaded).
- CMSSW `L1Trigger/TrackFindingTracklet/interface/Settings.h` (OT radii, disk z, B); CMSSW `SimG4Core/CustomPhysics/src` listing (no quirk code).
- ATLAS Athena `Simulation/G4Extensions/Quirks` (gitlab.cern.ch/atlas/athena, file tree, `QuirksConfig.py`, `InfracolorForce.h`, `QuirkTransportation.h`).
- github.com/eliwelch17/PreFASERQuirkSim (README); github.com/burzynski-lab/quirk-tracking (README; mentions an "ATLAS quirk search").
- Not re-read (UNVERIFIED values flagged in text): CMS-TDR-014 (Phase-2 tracker; CDS blocked by anti-bot), CMS MTD TDR (CERN-LHCC-2019-003), ATLAS ITk TDRs, higgsino/wino mass-splitting literature.
