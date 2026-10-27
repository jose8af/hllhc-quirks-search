# T1: the confinement scale Λ — origin, priors, and every constraint on it

Investigator: T1 (theory track, C001 quirks). Date: 2026-10-07. Status: COMPLETE.

Conventions:
- **Λ ≡ √σ** (string tension) unless stated otherwise.
- Λ_c ≡ T_c is the convention of 2512.20696.
- Λ_MS is the MS-bar scale of pure SU(N) Yang-Mills.

Code: `theory_track/code/T1_*.py`. Run with `pixi run python code/<file>.py` from `theory_track/`, in this order:
1. `T1_lattice_conversions.py`
2. `T1_running.py`
3. `T1_cosmo.py`
4. `T1_astro_collider.py`
5. `T1_figure.py`

Shared inputs are in `T1_common.py`.

Figure: `theory_track/figures/T1_lambda_plane.png`.

---

## 1. Executive summary

1. **The literature uses three Λ conventions that are not equivalent.**
   - √σ in the collider papers; T_c in 2512.20696; Λ_MS or the 1-loop Landau pole in model building and neutral naturalness.
   - Lattice ratios √σ : T_c : Λ_MS are 1 : 0.709 : 0.581 for SU(2) and 1 : 0.646 : 0.542 for SU(3) [hep-lat/0307017 Tab.6; 2106.00364 Tab.15].
   - A 1-loop "Λ" is a further ×5 below Λ_MS [1012.2072 Tab.I].
   - 2512.20696 uses the large-N value T_c = 0.6√σ for its SU(2) benchmark. For SU(2) the correct factor is 0.709, so its "keV" is 1.41 keV √σ, not 1.67 keV (15% error), and its m₀ = 6T_c is 13% high.
   - Lattice uncertainties are small (≤ 1% on T_c and m₀; 3-10% on Λ_MS).
2. **There is a concrete theory-favoured strip inside the CMS window, but for the doublet L, not the singlet E.**
   - Framework: SUSY GUT, MSSM + N_IC copies of 5⊕5̄ quirks + n_S IC-flavoured SM singlets, with α_IC = α_GUT [Kang-Luty 0805.4642 Sec.2.5; S.P. Martin 1012.2072]. It predicts a discrete ladder of Λ values.
   - **SU(2), n_S = 3:** √σ ≈ 0.8 / 2.6 / 6.4 / 15 keV at m_Q = 0.2 / 0.5 / 1 / 2 TeV. The strip is ×/÷ 3.9 wide, and Λ ∝ m_Q^1.3.
   - **SU(3), n_S = 9:** √σ ≈ 1.5 / 5.9 / 16 keV at m_Q = 0.2 / 0.5 / 1 TeV.
   - Neighbouring rungs are 1.8 decades (SU(2)) or 1.2 decades (SU(3)) apart.
   - The EW quirks in this framework are **doublets L (1,2)_{±1/2} with coloured partners D**. An E singlet needs a 10⊕10̄, which destroys perturbative unification for N_IC ≥ 2.
3. **Naturalness: the keV band is neither predicted nor tuned.**
   - With a flat prior in 1/g²(M_GUT) within ×2 of the SM value, 13% of the prior lands in 0.1-100 keV and 6% in the CMS window 0.6-15 keV (SU(2)). For SU(3) the numbers are 3% and 0%.
   - The band needs α_IC⁻¹(M_GUT) ≈ 1.3-1.5 × α_SM⁻¹ (SU(2)).
   - "α_IC = α_SM at M_GUT" with only the E quirk gives Λ ≳ 50 MeV.
   - Every neutral-naturalness model with EW-charged quirks (folded SUSY, quirky little Higgs, natural quirks, accidental-SUSY siblings) predicts √σ ~ 2-40 GeV, not keV.
4. **Cosmology is the strongest constraint. It never excludes an (m_Q, Λ) point by itself; it turns a CMS discovery into an upper bound on the reheat temperature.**
   - If the infracolor sector was ever in equilibrium with the SM, the whole CMS window is excluded:
     - glueball Ω_G h² ≈ 2-10 × (√σ/keV) for SU(2);
     - ΔN_eff(BBN) = 0.21 for SU(2) (2.5σ) and 0.57 for SU(3) (5σ).
   - With UV freeze-in, the window needs T_RH (strictly T_max) ≲ 5-35 GeV for SU(2) at √σ = 1-15 keV and m_Q = 0.2-1 TeV.
   - My independent implementation gives T_RH,max about ×2.2 above 2512.20696 Fig.4 (33 vs 15 GeV at m_Q = 600 GeV, T_c = 1 keV). The slope in Λ agrees.
   - The freeze-in abundance scales as T_RH^5.0, not T_RH^7 as stated in 2512.20696 Sec.4.2.
   - Above m_Q ≈ 500 GeV, the binding condition is simply "never thermalise the quirks" (T_max < m_Q/25).
   - The three escape routes and the strength each needs are in G-T1-4.
   - N_eff is not a probe of the mesoscopic band at CMB-S4/SO: the dark sector confines after BBN and before recombination, so only BBN sees the radiation.
5. **Killed ideas:**
   - Stellar cooling gives at best m_Q > 1.5 GeV (SN1987A).
   - Collider-indirect probes are Λ-independent and tiny: BR(Z→g′g′) ~ 10⁻¹².

   The mesoscopic window is constrained only by direct searches and by cosmology (through T_RH).

---

## 2. Gap entries

### G-T1-1. Λ conventions and conversion uncertainties (convention table for the strategy)

**Current treatment.**
- Collider papers define σ = Λ² [1708.02243 below Eq.2; 1811.08903 Eq.2.3; 2404.13814 Eq.5.2].
- Kang-Luty write σ ~ Λ² and quote m₀ = 3.6√σ [0805.4642 l.512, l.1567].
- 2512.20696 defines Λ ≡ T_c with T_c/√σ ≈ 0.6 and m₀ ≈ 6Λ [Eq.1 and Sec.2], citing Boyd et al. and Lucini-Rago-Rinaldi.
- Neutral-naturalness papers use Λ_MS with m₀ = 6.8Λ_MS and σ ≈ 3.6Λ′² [1501.05310 fn.5 and p.24; 2504.02940 Sec.2.1-2.2].
- Kang-Luty's GUT ladder ("100 MeV, MeV, 10 keV, 100 eV") is a 1-loop Landau-pole estimate [0805.4642 Sec.2.5].

**Why it is a gap.** These quantities differ by factors of 1.2-10 and are mixed without comment. The theory_signal_model.md conversion (×1/0.6) is the large-N value, not SU(2).

**Quantitative (ESTIMATE, `T1_lattice_conversions.py`; lattice inputs from primary papers):**

| N | T_c/√σ | m₀/√σ | Λ_MS/√σ | m₀/T_c | m₀/Λ_MS |
|---|---|---|---|---|---|
| 2 | 0.7091(36) [hep-lat/0307017 Tab.6] | 3.781(23) [2106.00364 p.83] | 0.581(57) [2106.00364 Tab.15] | 5.33(4) | 6.5(6) |
| 3 | 0.6462(30) [same] | 3.405(21) [same] | 0.542(19) [same] | 5.27(4) | 6.3(2) |
| 4 | 0.634(12) | 3.271(27) | 0.522(23) | 5.16(11) | 6.3(3) |
| ∞ | 0.5949(17) [1202.6684 Eq.12] | 3.072(14) [2106.00364 Tab.31] | 0.506(25) [2106.00364 Eq.20] | 5.16 | 6.1 |

What the table implies:
- The "1-loop Λ" (Λ₁ = μ e^{−2π/(b₀α)}) is ≈ 0.21 Λ_MS for the same α. Martin's SU(2), n_S = 3 example gives Λ₁ = 0.76 keV against Λ_MS = 3.7 keV, i.e. √σ = 6.3 keV [1012.2072 Tab.I; reproduced to 1-3% by `T1_lattice_conversions.py`]. A 1-loop "Λ" read as √σ is therefore off by ×8.
- 2512.20696 for SU(2):
  - their Λ = 1 keV corresponds to √σ = 1.41 keV (lattice), not 1.67 keV (−15%);
  - their m₀ = 6T_c is 13% above the lattice value 5.33T_c.
- Effect of these errors on the cosmology: T_RH,max scales as Λ^−0.21, so the convention changes it by ≤ 4%. It matters only for overlaying plots.
- Uncertainty budget for converting a measured √σ into Λ_MS (or α_IC): ±10% (SU(2)) or ±3.5% (SU(3)) from the truncation of perturbation theory in the lattice fits [2106.00364 Eq.20-22]. T_c and m₀ are known to < 1%.

**Exploitation.** (e) and documentation:
- Adopt this table in the strategy.
- When overlaying 2512.20696, convert with 1/0.709 (SU(2)) or 1/0.646 (SU(3)).
- When comparing with model-building papers, convert Λ_MS with 1/0.581 or 1/0.542.

**Effort:** 1 hour. **Confidence:** high. **Verdict: EXPLOIT** (cheap, prevents factor 1.4-8 mistakes).

---

### G-T1-2. A theory-favoured strip inside the CMS window: the SUSY-GUT ladder (doublet quirks)

**Current treatment.**
- Kang-Luty: MSSM + SU(2)_IC with 5⊕5̄ quirks gives α_IC = α_3 above the TeV scale, so Λ ~ 100 MeV. Adding 1, 2 or 3 extra IC-fundamental pairs gives "MeV, 10 keV, 100 eV" (1-loop) [0805.4642 Sec.2.5].
- Martin did the 3-4-loop analysis with gauge unification, α_X = α_GUT, perturbativity [1012.2072 Sec.II, Tab.I]. His results at a 1 TeV threshold:

| SU(2)_X, n_S | 2 | 3 | 4 |
|---|---|---|---|
| Λ_MS | 250 keV | 3.7 keV | 55 eV |

| SU(3)_X, n_S | 8 | 9 |
|---|---|---|
| Λ_MS | 140 keV | 8.8 keV |

- SU(3)_X needs n_S ≥ 3 [1012.2072 Sec.II].
- **No collider quirk paper uses this ladder** to motivate its Λ grid. Theory_signal_model.md §6.2 calls the window "signature-driven, not naturalness-driven".

**Why it is a gap.**
- It is the only framework I found where a stated UV assumption (gauge-coupling unification plus a choice of IC flavour content) lands Λ inside 0.1-100 keV.
- Its m_Q dependence and width had not been mapped onto the collider plane.
- It changes which benchmark is "theory-motivated": doublets plus coloured partners, not the singlet E.

**Quantitative (ESTIMATE, `T1_running.py`).**

Method:
- Anchor on Martin's α_X⁻¹(1 TeV).
- Move the IC threshold (quirks, squirks, IC gauginos) to m_Q, using the SUSY 2-loop β-function above it and α_X(M_U) fixed.
- Below m_Q, use 3-loop pure Yang-Mills, then Λ_MS → √σ with the lattice ratio.
- Strip width: ±1.5 in α⁻¹(m_Q), from a factor-3 spread of IC-charged masses ((Δb/2π) ln 3 ≈ 1.6 for SU(2)) plus GUT thresholds, combined with ±10% from the lattice conversion.

| Ladder rung | √σ at m_Q = 200 GeV | 500 GeV | 1 TeV | 2 TeV | width (×/÷) | slope d ln Λ/d ln m_Q |
|---|---|---|---|---|---|---|
| SU(2), n_S = 2 | 66 keV | 190 keV | 420 keV | 0.9 MeV | 3.8 | 1.15 |
| **SU(2), n_S = 3** | **0.8 keV** | **2.6 keV** | **6.4 keV** | **15 keV** | 3.9 | 1.28 |
| SU(2), n_S = 4 | 10 eV | 36 eV | 95 eV | 250 eV | 3.9 | 1.42 |
| SU(3), n_S = 8 | 29 keV | 100 keV | 260 keV | 690 keV | 2.5 | 1.38 |
| **SU(3), n_S = 9** | **1.5 keV** | **5.9 keV** | **16 keV** | **45 keV** | 2.5 | 1.47 |

Further numbers:
- Rung spacing for one extra IC flavour pair: Δα⁻¹ = (1/2π) ln(M_U/TeV) = 4.87. That is ×65 (1.8 decades) in Λ for SU(2) and ×16 (1.2 decades) for SU(3).
- The 3-decade mesoscopic band therefore always holds 1-3 rungs.
- The central SU(2), n_S = 3 line crosses the coplanar window for m_Q ≈ 0.17-2 TeV, which is exactly the CMS mass reach.

Representation caveat:
- In this framework the EW quirks are L = (N, 1, 2, ±1/2) plus coloured D = (N, 3, 1, ∓1/3) [1012.2072 Eq.2.1-2.5].
- A singlet E needs a 10⊕10̄ (+3 to each SM b_i per IC colour). For N_IC = 2, b₃ goes from −3 to +3, and α₃⁻¹(M_GUT) = 11.4 − (3/2π)·30.6 < 0: a Landau pole below M_GUT (ESTIMATE, 1-loop).
- So a GUT-motivated search would emphasise the doublet benchmark (A2 in theory_signal_model.md) and coloured D partners. Charged-neutral splitting and D-quirk limits belong to T6.

**Exploitation.**
- (a)/(f): draw the SU(2), n_S = 3 and SU(3), n_S = 9 strips as "theory benchmark" lines on the CMS (m_Q, Λ) exclusion plot. This is cheap, gives the result a theory interpretation, and shows that a CMS limit at m_Q ~ 1 TeV directly tests the n_S = 3 GUT-quirk model.
- (d): after a discovery, a measured (m_Q, √σ) fixes α_IC(m_Q) to δα⁻¹ = (b₀/2π) δln√σ ≈ 0.12 per 10% in √σ, plus ±0.12 from the lattice conversion (SU(2)). That is ≪ the rung spacing of 4.87, so the rung n_S is identified unambiguously, given the IC-charged spectrum.

**Effort:** days (a proper 2-loop, threshold-by-threshold calculation with the MSSM spectrum would replace my anchor-and-shift). **Confidence:** medium (strip position solid to a factor ~2-4; the model is one choice among many). **Verdict: EXPLOIT** (benchmark lines and motivation text); WORTH A CHECK for the doublet-plus-coloured topology (T6).

---

### G-T1-3. Is the mesoscopic band natural? (flat prior in 1/g²)

**Current treatment.**
- "Λ = μ₀ exp(−8π²/(b g₀²)) … each decade roughly equally likely" [0805.4642 Eq.1.2].
- Theory_signal_model.md §6.2: the window is a ~25% range in α_IC(m_Q).

**Why it is a gap.** It had not been quantified against a concrete UV boundary condition.

**Quantitative (ESTIMATE, `T1_running.py`).** Setup: non-SUSY, only the quirk E above m_Q, M_UV = 10¹⁶ GeV, m_Q = 500 GeV.
- d log₁₀Λ / d α_IC⁻¹(M_UV) = −0.37 (SU(2)) and −0.25 (SU(3)). The 3-decade band therefore spans 8.1 units of α⁻¹ for SU(2) and 12.2 units for SU(3).
- Flat prior on α⁻¹(M_UV) within [0.5, 2] × ⟨α₁⁻¹, α₂⁻¹⟩ (= 42):

| | P(0.1-100 keV) | P(CMS window 0.6-15 keV) | P(band \| quirky, Λ < m_Q/10) |
|---|---|---|---|
| SU(2) | 13% | 6% | 18% |
| SU(3) | 3% | 0% | 8% |

  The band needs α_IC⁻¹(M_UV) = 53-61 for SU(2) (1.27-1.46 × the SM value) and 82-94 for SU(3) (≈ 2×).
- With "α_IC = α_SM(M_UV)" exactly, SU(2) gives √σ ≈ 0.05-40 GeV, and SU(3) confines above m_Q (no quirks).

**Verdict: NOT A GAP for constraints (informational).**
- The CMS band is ~10% of a generous log-flat prior. It is neither tuned nor predicted, except by the SUSY-GUT ladder (G-T1-2).
- Use this in the motivation section, and do not claim the band is "natural" beyond this.

**Confidence:** high (1-loop/2-loop running is robust).

---

### G-T1-4. Cosmology: what a mesoscopic-window discovery implies, and how the window escapes exclusion

**Current treatment.**
- 2512.20696 (read in full) computes UV freeze-in γγ → g′g′ through the dim-8 operator [Eq.19, 26, 31-34], then glueballs, then BBN/CMB/γ/overclosure/SIDM/ΔN_eff.
- It concludes "T_RH ≲ O(100) GeV over the entire quirky parameter space" [abstract; Fig.4; Sec.6].
- Its benchmark is an SU(2)_L vector-like quirk with Y = 0, not E. It assumes:
  - T_RH ≲ m_Q/25 [Sec.4.2];
  - instantaneous reheating that does not populate the dark sector [Sec.3];
  - glueball decay [Eq.4-5];
  - "radiation until T_dark = T_c, then matter" with an order-of-magnitude bracketing [Fig.3];
  - an SIDM bound applied to sub-components [Eq.11].
- Kang-Luty: no model-independent bound once T_RH ≲ GeV [0805.4642 Sec.2.3].

**Why it is a gap.**
- (i) The bounds were never shown in the collider (m_Q, √σ) plane at the CMS window.
- (ii) An independent check finds a ×2.2 normalisation difference and a wrong scaling exponent.
- (iii) The thermal-history numbers, the size of each escape route, and N_eff at CMB-S4 were not quantified for the window.

**Quantitative (ESTIMATE, `T1_cosmo.py`; E quirk, tr Q² = 1, lattice T_c and m₀).**

**(a) Glueball lifetime** [Eq.4-5 with α₂ → α trQ²]:
- τ = 10⁵³-10⁶⁸ s over the band (m_Q = 0.2-1 TeV, √σ = 0.1-15 keV). Even at √σ = 100 keV, τ ≥ 10³⁵ s.
- τ = t_Universe at √σ ≈ 24 MeV (m_Q = 500 GeV); τ = 1 s at √σ ≈ 2 GeV.
- ⇒ In the CMS window the glueballs are **absolutely stable dark matter**. Only overclosure and self-interaction matter. The BBN/CMB/γ-ray bounds of 2512.20696 Fig.4 start at Λ_c ≳ 1-10 MeV and are irrelevant here, as are the decay-rate uncertainties.

**(b) Thermal history** (dark sector once in equilibrium):

| Quantity | SU(2) | SU(3) |
|---|---|---|
| Decoupling T_dec (min of dim-8 and on-shell quirk exchange) at m_Q = 0.2 / 0.5 / 1 TeV | 11 / 28 / 57 GeV | 11 / 28 / 57 GeV |
| ΔN_eff at BBN | 0.21 | 0.57 |
| Tension with N_eff(BBN) = 2.895 ± 0.142 [2512.20696 fn.5] | 2.5σ | 5.0σ |

- The decoupling temperatures are set by on-shell quirk exchange; the dim-8 rate alone decouples at 17-113 GeV.
- After e⁺e⁻ annihilation, ξ = T_dark/T = 0.36. The dark sector confines at T_SM ≈ 2 keV × (√σ/keV): after BBN, before recombination. So the **CMB sees cold glueballs, not radiation**.
- Glueball abundance: Ω_G h² = 10 × (√σ/keV) with instant confinement (the 2512.20696 central assumption), or 2 × (√σ/keV) with an adiabatic cannibal phase (3→2 freeze-out at x_f ≈ 33). SU(3) is ×2.5 larger.
- Ω_G h² = 0.12 at √σ = 12-60 eV (SU(2)) or 5-26 eV (SU(3)).
- ⇒ **The whole CMS window is excluded by ×20-1300 (SU(2)) for any history in which the dark sector thermalised.**
- σ/m = 10¹¹-10¹⁴ cm²/g [Eq.11], so a sub-component bound applies as well.

**(c) UV freeze-in (T_RH < m_Q/25).** T_RH,max in GeV, SU(2) (SU(3) within 5%):

| m_Q | √σ | Overclosure, instant | Overclosure, cannibal | f < 0.025 (SIDM-like) | m_Q/25 |
|---|---|---|---|---|---|
| 200 GeV | 1 keV | 9.9 | 13 | 4.7 | 8 |
| 200 GeV | 15 keV | 5.5 | 7.4 | 2.7 | 8 |
| 600 GeV | 1 keV | 35 | 47 | 17 | 24 |
| 600 GeV | 15 keV | 20 | 27 | 10 | 24 |
| 1 TeV | 1 keV | 64 | 86 | 31 | 40 |
| 1 TeV | 15 keV | 37 | 48 | 18 | 40 |

- **Check against 2512.20696 Fig.4** (digitised; m_Q = 600 GeV, T_c = 1 keV): overclosure 15 GeV, SIDM 6.4 GeV. Mine is 33 GeV and 16 GeV. The slopes agree (−0.21 decades of T_RH per decade of Λ), but the normalisation differs by ×2.2 in T_RH (×50 in Ω).
  - One candidate is that their dark/SM temperature ratio was not corrected for SM entropy release (g*s from ≈ 80 at T_RH to 3.9 today). That would overestimate Ω by ×20, i.e. ×1.8 in T_RH, which is most of the gap. This is UNVERIFIED; their code is not public.
  - The physics conclusion ("tens of GeV at most") is unchanged.
- **Scaling.** Ω_G ∝ T_RH^5.0 in the adiabatic, self-thermalised dark sector (Ω ∝ ξ³ ∝ Z^{3/4}, Z ∝ T_RH⁷). 2512.20696 Sec.4.2 states T_RH^7, which would hold only for non-thermalised gluons. Yet the frozen-in gluons do thermalise: Γ_{2→3}/H ~ 10¹⁰ at the bound.
  - So a ×100 abundance uncertainty moves T_RH by ×2.5, not "at most ×2". This is a minor correction to their robustness claim.
- **Binding condition.** For m_Q ≳ 500 GeV, the overclosure freeze-in bound is above m_Q/25. The binding requirement is then the no-thermalisation condition itself. The SIDM-like sub-component bound binds at ≈ 0.4-0.7 × m_Q/25.
- **ΔN_eff at the bound is ~6×10⁻⁴** (ξ_RH = 0.23). CMB-S4 (σ ≈ 0.03) and SO (σ ≈ 0.05-0.07; UNVERIFIED survey numbers) **cannot probe the mesoscopic window** through N_eff.

**(d) Escape routes and how strong they must be** (SU(2), √σ = 1-15 keV):

1. **Low reheating.** T_max (not only T_RH) ≲ 3-35 GeV, depending on m_Q and Λ (table above, and the contours in the figure).
   - For non-instantaneous reheating, UV freeze-in with ⟨σv⟩ ∝ T⁶ is the marginal case: the enhancement over instantaneous reheating is only logarithmic in T_max/T_RH (UNVERIFIED recollection of the Garcia-Kaneta-Mambrini-Olive classification).
   - But on-shell quirk production turns on once T_max ≳ m_Q/20 (ESTIMATE: on-shell beats dim-8 for x = m_Q/T ≲ 20-22).
   - BBN requires T_RH ≳ 5 MeV, so 3-4 decades of T_RH remain viable.
2. **Asymmetric reheating.** The inflaton or modulus must give the dark sector ρ_d/ρ_SM ≲ 2×10⁻⁴ (√σ = 1 keV) to 5×10⁻⁶ (15 keV), i.e. ξ_RH ≲ 0.22-0.09. That is ×40 smaller in ρ with the f < 0.025 SIDM-like bound. And T_max < m_Q/25 is still required.
3. **Late entropy dilution.** After T_dec ≈ 10-60 GeV and before BBN, with D ≥ Ω_th/0.12:
   - 51 / 85 / 1270 at √σ = 0.6 / 1 / 15 keV (instant);
   - ≈ ×5 less with cannibalism;
   - ×40 more if the sub-component bound f < 0.025 applies.

   An early matter era from a 10-100 GeV-scale modulus easily provides D ~ 10²-10⁵, but it also dilutes any earlier baryon asymmetry.
4. **Invisible glueball decay** to a new massless state [2512.20696 App.B].
   - Freeze-in case: it removes the overclosure/SIDM bounds.
   - Thermal case: it fails, because ΔN_eff(CMB) = 0.39 (SU(2)) or 1.4 (SU(3)) from glueball → φ (g_φ = 1), against ACT DR6 P-ACT-LB N_eff = 2.86 ± 0.13 [2503.14454 abstract, via web search; UNVERIFIED table].
   - It is very non-minimal.

**Exploitation.**
- (a): the cosmology is not an (m_Q, Λ) exclusion. It is an *implication* map, "a CMS discovery at (m_Q, √σ) implies T_max ≲ X GeV", which the CMS paper can quote (figure contours).
- (f): a short note correcting/qualifying 2512.20696 for the E benchmark (×2.2 normalisation, T^5 scaling, T_max vs T_RH, CMB N_eff only for invisible decays) is possible but modest. Contact the authors first.

**Effort:** done (days to polish into a note). **Confidence:** medium (order-one strong-dynamics factors; freeze-in matrix element taken from 2512.20696 Eq.26 without re-derivation). **Verdict: WORTH A CHECK** (normalisation discrepancy). The overall cosmology picture is **EXPLOIT** as motivation text plus a figure overlay.

---

### G-T1-5. Self-interacting sub-component bound (assumption audit)

**Current treatment.** 2512.20696 applies σ/m ≲ 1 cm²/g to glueballs "even if they are only a sub-component" [Sec.4.1, Eq.11].
- Digitising their Fig.4 gives a red/yellow ratio in T_RH of 0.43. That is an effective f_max ≈ 1/70 (with my T^5 scaling) or 1/370 (with their T^7).

**Why it could be a gap.** With σ/m = 10¹¹-10¹⁴ cm²/g, the glueballs are a fluid. The constraint on a fluid-like fraction saturates; it does not scale as f·σ/m.

**Quantitative.** Relaxing f_max from 0.025 to 0.1-0.3 raises T_RH,max by only (4-12)^{1/5} = 1.3-1.6.

**Verdict: NOT A GAP (killed).** The effect is ≤ ×1.6 on T_RH and nothing for collider parameters.

---

### G-T1-6. Neutral-naturalness landscape: does any model predict the mesoscopic band?

**Current treatment and quantitative survey** (papers opened):

| Model | EW-charged quirks? | IC group | Predicted Λ | √σ (converted) | Regime |
|---|---|---|---|---|---|
| Folded SUSY [hep-ph/0609152 via 0805.4667] | yes (F-squarks, EW doublets) | SU(3)′ | "Λ′ ~ 10 GeV" (uses 15 GeV) [0805.4667 l.311-314] | ~20-30 GeV | microscopic |
| Quirky little Higgs [0812.0843 Sec.7] | yes (fermionic top partners) | SU(3)_I | free α_I(1/R). Bulk SU(6) would set α_I ≈ α_C, giving GeV. keV needs α_I(1/R) = 0.028 [Tab.3] | GeV natural, keV tuned ×3 in α | microscopic (meso/macro possible) |
| FSUSY/QLH generic [1512.05782 p.1] | yes | mirror SU(3) | m₀ = 10-60 GeV from RG | 3-18 GeV | microscopic |
| Twin Higgs family [1501.05310 Sec.IV.B, Fig.3] | no (top partners SM singlets) | twin SU(3) | Λ̂_MS ~ 1-20 GeV for δg₃/g₃ ∈ ±15% | 2-40 GeV | not EW quirks |
| Singlet scalar top partners / accidental SUSY [1803.03651 l.909-989] | yes (EW-charged "siblings") | SU(3)_{B,C} | Λ ≳ 4 GeV (m₀ ≳ 28 GeV), benchmark 5-10 GeV | ~8-20 GeV | microscopic |
| Natural quirks [2504.02940 Sec.2] | yes | SU(3) | Λ′ ~ few GeV, m₀ = 6.8Λ′ | ~3-10 GeV | microscopic |
| Quirky composite DM [0909.2034 Sec.6] | yes (chiral) | SU(2)_Q | normalised to Λ_Q ~ GeV (glueball BBN) | ~GeV | microscopic |
| **SUSY GUT + IC [0805.4642 Sec.2.5; 1012.2072]** | **yes (L doublets + coloured D)** | **SU(2), SU(3)** | **discrete ladder; SU(2) n_S = 3 → 3.7 keV Λ_MS** | **0.8-15 keV (m_Q = 0.2-2 TeV)** | **mesoscopic/macroscopic** |

**Verdict.**
- **Neutral naturalness does not motivate the mesoscopic band** (2-40 GeV, i.e. 5-6 decades above it). The only reason is RG: hidden and SM colour couplings are equal near the 5-10 TeV Z₂ scale and the hidden sector has fewer flavours [1501.05310 Sec.IV.B].
- Moving such a model to keV needs δg/g ≈ −40% at the Z₂ scale (ESTIMATE: Δ(1/α) ≈ 24 for SU(3)), which breaks the Z₂ that is the point of the construction.
- The band is motivated only by (i) generic hidden confining sectors with log-flat Λ (G-T1-3) and (ii) the SUSY-GUT ladder (G-T1-2).
- **Status: EXPLOIT** as honest motivation text: "the CMS window is the generic-hidden-sector / GUT-ladder target; neutral-naturalness quirks are microscopic and belong to resonance/SUEP/glueball searches".

**Confidence:** high for the NN numbers; medium for the completeness of the survey (INSPIRE: abstract:quirk* and naturalness, twin, folded, unification).

---

### G-T1-7. Λ as a measurable after discovery (UV test)

This is the (d) use of G-T1-2, kept as a separate entry because it feeds T4.
- A measured √σ to ±10% plus the lattice Λ_MS/√σ (±10% SU(2), ±3.5% SU(3)) gives α_IC(m_Q) to δα⁻¹ ≈ ±0.17 (SU(2)) or ±0.2 (SU(3)).
- A measured σ_prod gives N_IC (σ ∝ N_IC).
- Running to M_GUT with the known IC spectrum then tests "α_IC = α_GUT" to ~1%. That is far better than the rung spacing (Δα⁻¹ = 4.87).

**Verdict: WORTH A CHECK** (depends on T4's √σ resolution). **Effort:** hours. **Confidence:** medium.

---

## 3. Killed ideas

| Idea | Killing number | Code / ref |
|---|---|---|
| Stellar cooling (Sun, RG, HB, SN1987A) via γγ → g′g′ | ε(m_Q = 100 GeV) = 9×10⁻⁴¹ (Sun), 3×10⁻³³ (RG), 6×10⁻³² (HB), 2×10⁴ erg/g/s (SN) against limits of 0.2-10¹⁹. Bounds: m_Q > 1 MeV, 7 MeV, 9 MeV and 1.5 GeV (SN; Primakoff adds at most ×few). Kang-Luty quote ~10 GeV [0805.4642 Sec.2.2]. | `T1_astro_collider.py` |
| Production of keV glueballs in stars (T ~ Λ) | Rate ∝ Γ(G→γγ) ~ 10⁻⁸⁰ GeV (τ ~ 10⁵⁷ s) | `T1_cosmo.py` |
| Z → g′g′, e⁺e⁻ → γ + invisible, light-by-light | BR(Z→g′g′) ~ 1×10⁻¹² (m_Q = 100 GeV); σ(e⁺e⁻→γg′g′) ~ 10⁻¹⁴ fb at Belle II, 6×10⁻⁷ fb at LEP2. All Λ-independent; Λ enters only via (Λ/m_Q)⁴ ~ 10⁻³² | `T1_astro_collider.py` |
| BBN/CMB/γ-ray glueball-decay bounds in the CMS window | τ ≥ 10³⁵ s for √σ ≤ 100 keV. These bounds start at Λ_c ≳ 1-10 MeV [2512.20696 Fig.4] | `T1_cosmo.py` |
| CMB-S4/SO ΔN_eff as a probe of the mesoscopic band | Dark confinement at T_SM ≈ 2 keV (√σ/keV) is before recombination. Freeze-in ΔN_eff ~ 6×10⁻⁴; the thermal case is already excluded by Ω_G | `T1_cosmo.py` |
| Cannibalism makes the bounds stronger (2512.20696 Sec.3.2 says neglecting it is conservative) | It lowers Ω by ×5 (x_f ≈ 33) and raises T_RH,max by ×1.35: a small effect. Their statement is right in direction for the bracketing but not in sign for the late-time abundance | `T1_cosmo.py` |
| SIDM sub-component recalibration | ≤ ×1.6 on T_RH,max (G-T1-5) | `T1_cosmo.py` |
| Banks-Zaks fixed point above m_Q giving keV naturally (Λ ∝ m_Q) | Integer-N_F SU(2) fixed points are strong (α* ≈ 0.23 at N_F = 10), giving Λ/m_Q ~ 0.02, i.e. GeV, not keV (ESTIMATE, 2-loop BZ) | hand estimate |
| "Neutral naturalness predicts keV quirks" | NN predicts √σ ≈ 2-40 GeV (G-T1-6) | refs in G-T1-6 |

---

## 4. Open questions for other workstreams

- **T6 (production / model space):**
  - The theory-favoured ladder (G-T1-2) has **doublet L quirks plus coloured D partners**. Needed:
    - (i) the charged-neutral splitting and Q± → Q⁰π± cτ for an IC doublet (higgsino-like ~7 mm?) and how it reshapes the pair topology;
    - (ii) current LHC limits on coloured D quirks at mesoscopic Λ (these may already push m_D, and through GUT mass relations m_L, above the CMS reach).
  - Please also check whether an E singlet can come from incomplete GUT multiplets without spoiling unification.
  - Cross-reference (LOG, T6 finished): T6 finds that a pure doublet goes invisible with cτ ≈ 7.9 mm. If that holds for the IC doublet, the GUT-favoured L quirks give the T6 "disappearing / monojet + soft pions" topology rather than the coplanar one. The coplanar target then stays generic-hidden-sector (E), and the GUT ladder motivates the T6 channel instead.
- **T4 (observables):** the expected resolution on √σ from trajectories. If it is ≤ 10%, G-T1-7 (testing α_IC = α_GUT) becomes a selling point.
- **T2/T3:** none from T1, except to use Λ ≡ √σ and the conversion table in G-T1-1.
- **T5 (literature audit):** check whether any paper besides 1012.2072 and 0805.4642 derives keV Λ from a UV condition. Also check whether 2512.20696 Fig.4 includes g*s dilution (the ×2.2 discrepancy).
- **Experimental Phase 2:**
  - (i) Put the SU(2), n_S = 3 (and SU(3), n_S = 9) ladder lines and the T_RH,max contours on the (m_Q, Λ) result plot. Quote "a discovery implies T_max ≲ m_Q/25 and T_RH ≲ 3-35 GeV".
  - (ii) Consider making the doublet L (with N_IC = 2) a full benchmark rather than a 2-point topology test, since it is the GUT-motivated representation.
  - (iii) Nothing from cosmology, astrophysics or precision physics removes any part of the 0.3-30 keV grid; no grid change is needed.

---

## 5. References opened

| arXiv id | What I used |
|---|---|
| 2512.20696 (full text, Fig.4 digitised) | Eq.1-12, 19-34, Sec.4.1-4.3, App.B, fn.5, Fig.2/4/6; freeze-in formula, glueball decay, conventions, bounds |
| 0805.4642 | Sec.2.1-2.5 (dim-8 operator, star cooling, cosmology, GUT ladder), Sec.5.7 (m₀ = 3.6√σ) |
| 1012.2072 | Sec.II, Tab.I-II (SUSY-GUT ladder, 1-4-loop Λ_MS; validation of my code) |
| hep-lat/0307017 | Tab.6, Eq.28 (T_c/√σ for SU(2), SU(3), SU(4), SU(6), SU(8), SU(∞)) |
| 1202.6684 | Eq.12 (T_c/√σ = 0.5949(17) + 0.458(18)/N²) |
| 2106.00364 | Tab.15, Eq.20-22 (Λ_MS/√σ); p.83-84 tables and Tab.31 (m₀++/√σ, SU(2)-SU(12), ∞) |
| 2007.06422, hep-lat/0404008, hep-lat/0502003, 0803.1092 | downloaded; values superseded by 2106.00364 (same group), not used separately |
| 1501.05310 | Sec.IV.B, fn.5, Fig.3 (twin-QCD Λ̂ 1-20 GeV, m₀ = 6.8Λ_MS) |
| 1512.05782 | p.1 (EW-charged top partners in FSUSY/QLH; m₀ = 10-60 GeV from RG) |
| 0805.4667 | Λ₀ ~ 10-15 GeV for folded SUSY squirks |
| 0812.0843 | Sec.7, Eq.46-47, Tab.3 (QLH Λ_I vs α_I(1/R)) |
| 1803.03651 | Λ ≳ 4 GeV, m₀ ≈ 6.8Λ (accidental-SUSY siblings) |
| 2504.02940 | Sec.2.1-2.2 (σ ≈ 3.6Λ′², m₀ ≈ 6.8Λ′, Λ′ ~ few GeV) |
| 0909.2034 | Sec.6 (quirkcolor glueball decay, Λ_Q normalisation) |
| research/theory_signal_model.md | §0, §1, §3, §4, §6 (CMS window 0.6-15 keV; FASER HEPData points; conventions) |
| 2503.14454 | N_eff = 2.86 ± 0.13 (P-ACT-LB), abstract via web search only: UNVERIFIED |

Not opened (cited as UNVERIFIED where used):
- Garcia-Kaneta-Mambrini-Olive (non-instantaneous reheating);
- Forestell-Morrissey-Sigurdson 1605.08048 (σ₃₂ scaling);
- Planck 2018 (N_eff 2.99 ± 0.17), SO/CMB-S4 forecasts (σ_Neff ~ 0.05-0.07 / 0.03);
- Okun's thetons.
