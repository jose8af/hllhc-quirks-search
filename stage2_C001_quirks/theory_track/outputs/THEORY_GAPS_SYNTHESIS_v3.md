# C001 quirks, theory track: synthesis of theory gaps and how to exploit them (v2)

Executors: S (v1, synthesis), F1 (v2, fix pass). Date: 2026-10-08.
**Status: v3, after reviews R1 and R2.**
- R1: the critical review gave ITERATE (3 A, 8 B, 9 C) and the constructive review listed 3 A, 11 B and 12 C. All were answered in v2 (§10.1).
- R2: a round-2 review confirmed the R1 fixes and gave ITERATE (1 A, 4 B, 9 C). v3 answers these (§10.2).
- v1 and v2 are kept unchanged at `outputs/THEORY_GAPS_SYNTHESIS_v1.md` and `_v2.md`.
- The investigator reports T2 and T3 now carry a dated erratum box. They are otherwise unchanged.

Inputs:
- Investigator reports T1-T6 (`theory_track/investigations/`), their code (`code/T*_*.py`) and figures.
- Reviewer code and outputs: `code/R1_*.py`, `figures/R1_*_out.txt`.
- Project documents:
  - `research/theory_signal_model.md` (TH);
  - `phase1_strategy/outputs/STRATEGY_DRAFT.md` v3 (STRAT);
  - `phase1_strategy/outputs/OPEN_QUESTIONS.md` (OQ);
  - `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md` (SREQ).

Checks:
- v1 checks: `code/S_*.py`.
- v2 checks: `code/F1_*.py`, with outputs in `figures/F1_*_out.txt`.
- Run everything from `theory_track/` with `pixi run python code/<file>`.

Conventions: **Λ ≡ √σ_string** (BRIEF §1), with σ = 50.68 GeV/cm × (Λ/keV)². Unless stated otherwise:
- benchmark E = (1,1)₋₁ Dirac fermion, N_IC = 2;
- CMS Phase-2: 3.8 T, PU 200, 3 ab⁻¹.

Tags:
- `[T3 §3.2]` is a section of an investigator report.
- `[1911.02223 Eq.III.12]` is a primary paper.
- `[R1: file]` is the critical reviewer's independent code.
- `[F1: file]` or `[S: file]` is a check run for this synthesis.
- `ESTIMATE` is our own calculation.
- `UNVERIFIED` means not checked against a primary source.
- Gap IDs are **S-n**. Cross-report tensions are now **X-n**; they were "T-n" in v1, which clashed with the investigator names T1-T6.

**What changed in v3 (after R2):**
1. **The stopped-pair recast is not new.** Evans-Luty [1811.08903] already recast CMS 1801.00359 for this very benchmark (E′, SU(2)_IC). They computed the lifetime-dependent trigger fraction from the real 2016 fill schemes and gave 300 fb⁻¹ projections (S-8). What remains is an *update*: full Run-2+3 data, f_stop from the causal string, and an HL-LHC projection.
2. **The Li-vs-causal thickness deficit depends on γ*:** ≈ 3 % low at γ* ≈ 1.05, ≈ 15 % low at the median γ* ≈ 1.3, and 30-35 % low in the median at γ* = 2-3 (single events −47 %…+36 %) [R2]. It is ≈ 15 % at 3 keV when converged. The fixed "0.85" validation target is replaced by an event-by-event comparison over the triggered γ* spectrum (S-1, §4.1).
3. **Existing E-singlet exclusions are now stated** (Box A, §4.5): Farina-Low, Evans-Luty, D0 and FASER.
4. The Run-2+3 stopped-pair estimate is ≈ 0.15-0.35 TeV and does not beat FASER/D0 at its low end (S-8).
5. The smeared-vs-truth comparison no longer claims an edge shift: the two cuts have different background rejection (S-2).

**What changed from v1 to v2 (headline):**
1. The v1 headline "every published central-detector trajectory model is wrong at the order that matters" is **withdrawn**.
   - Its numbers (×0.04-60 thickness, 0.2-35 mm hits, fake 0.2-21 mm with MS, 140-570 µm frame dependence) came from a lab-time-slice straight string that T2 wrote as a stand-in for Li et al. No paper used it.
   - The literal Li et al. integrator, step-converged, agrees with the exact causal string within tens of per cent: ≈ 15 % low at γ* = 1.28, with a γ*-dependent deficit of 3-35 % (S-1, X-13, §3).
2. The causal (Athena-type) string is now **independently confirmed** as exact classical Nambu-Goto by a conformal-gauge solver written by R1 [R1: `R1_conformal_ng.py`]. So are the B ln(1/B) non-linearity and the Λ^−1.6…−2.0 thickness scaling.
3. All plane-thickness efficiencies are now labelled **truth level**. A first look at the effect of hit resolution shows that the coplanarity test at the Δs ≲ 100 µm scale is carried by the Inner Tracker. The PS and 2S modules measure the out-of-plane coordinate only at the ≈ 0.25 mm and ≈ 8 mm level. The event-level resolution (23-30 µm) is the size of the MS floor, Truth-level cut values therefore do not transfer to the detector (S-2) [F1: `F1_smear.py`]. (v3: no edge shift is claimed, since the smeared and truth cuts have different background rejection [R2-B4].)
4. The stopped-pair reach is revised down: 0.3-0.55 TeV for EB+HB instead of 0.65 TeV. The reasons are the sub-µs annihilation delay (as Evans-Luty already showed [1811.08903 Fig.3-4]) and a non-zero background [F1: `F1_stopped.py`].
5. Headlines are restated with their floors and caveats:
   - measurement: 1-3 % on m_Q and 0.5-1.5 % on Λ, MET-scale limited;
   - MET-strip rejection: ×13-34 against random planes only;
   - predictive χ²: an idealised upper bound.
6. New material:
   - a consolidated Λ answer (§1, box A) and an oscillation-length box (box B);
   - a recast table (§4.5);
   - a Run-3 vs Phase-2 table (§4.6);
   - short notes on PU-vertex association, HLT paths, alignment, ML features and simulation-based inference (§4.7);
   - a glossary (below).

---

## 0. Terms used, and executive summary

### 0.1 Glossary (read first)

| Term | Meaning |
|---|---|
| Λ | √σ, the square root of the string tension. σ = 50.68 GeV/cm (Λ/keV)². The cosmology paper 2512.20696 uses T_c = 0.709 √σ (SU(2)), so its "Λ = 1 keV" is √σ = 1.41 keV |
| ℓ₀ | m_Q/σ, the natural length of the problem. ℓ_max is the maximal CM separation, = 2(γ*−1)ℓ₀ = 3.95 cm (γ*−1)(m_Q/100 GeV)(keV/Λ)² [T2 §2.2] |
| N_osc | number of oscillations while the pair is inside radius R: σR/(2β*p_T) ≈ 12 (Λ/keV)² for the CMS tracker [T2 §2.2] |
| **causal string** | The Nambu-Goto (NG) string with massive point endpoints. It is built from straight null segments that each endpoint emits and that propagate at the speed of light. Field kicks act on the endpoints. This is an Artru/Lund-type construction. Implementations: the ATLAS Athena `Quirks` algorithm, T2's Python port, and the numba port `T3_causal.py` (T3/T4) used for every number here. It is exact classical NG for point masses; see X-13 for the validity limits |
| **Li method** (CM-simultaneous straight string) | The Kang-Luty endpoint force with a *straight* string. The two quirks are advanced at different lab times so that they stay simultaneous in the pair CM frame, and ŝ is built from the separation and the quirk velocity [1911.02223 Eq.III.6-10 = 2002.07503 Eq.VIII.1-4]. It is covariant by construction. It neglects string curvature and retardation |
| **labSS** (lab-time-slice straight string) | A straight segment between the two quirks at *equal lab time*. T2/T3 used it as a stand-in for the Li method. **No published paper uses it.** It is not Lorentz covariant |
| cmSS | T2's second variant: CM simultaneity obtained by linear extrapolation over the CM time offset. Not used in the literature either |
| d (formula) | 1.16 µm (m_Q/100 GeV)(keV/Λ)⁴(B/T) [1911.02223 Eq.III.12]. This is a first-order perturbative estimate. Li et al. themselves show it agrees with their numerical thickness only within an order of magnitude [2002.07503 App.C, Fig.8] |
| b_odd | the miss distance at odd crossings, ≈ 3.5 µm (keV/Λ)⁴ in 3.8 T [T2 §5.3]. Physically, this is what the formula d describes (X-2) |
| **Δs** (plane thickness) | √(smallest eigenvalue of Σ h hᵀ/(N−1)) over the hits h of both quirks, for a plane through the primary vertex [1708.02243 Eq.11; 2002.07503 Eq.C.1]. **Truth level** (true hit positions) unless stated. Δs_B, Δs_MS and Δs_B+M denote B only, MS only, and B + material. The "max residual" max\|n·h\| is the quantity for hit-association windows |
| x_B | T4's in-plane B displacement, ≈ 0.5 qBR/σ (X-1) |
| t_est (new) | the intrinsic thickness estimated from *smeared* hits with a resolution-weighted plane fit (S-2, `F1_smear.py`) |
| truth level | true hit positions, no detector resolution, known hit-to-quirk assignment, no PU |
| [indep.] / [re-run] | a check by different code or a closed form, vs. a re-run of the investigator's own code |

### 0.2 Executive summary

**Bottom line.** This track has **not derived any new exclusion**. It produced four things:
- (i) corrections to the signal model and to the coplanar-search window, plus a validated production propagator;
- (ii) two complementary channels with reach *projections* (stopped pairs; a merged-pair HSCP-like category) and a list of recasts, none of which has been performed (§4.5);
- (iii) a method to measure (m_Q, Λ) after a discovery;
- (iv) two UNVERIFIED readings of *existing* exclusions: Λ ≳ 3 MeV via dilepton resonances, and doublet quirks via monojet.

None of the findings changes the projected mass reach of the coplanar tracker search (≈ 1.1-1.2 TeV, STRAT §6.1) at a level we can compute. The truth-level window edge moves from 0.54-0.81 keV (formula) to 0.45-0.7 keV (causal string + material). With realistic hit resolution the coplanarity test becomes Inner-Tracker dominated. Truth-level cut values then do not transfer, and the lower edge is undefined until a cut is set at fixed background efficiency (S-2). The fastest route to a stronger limit is an *update* of Evans-Luty's recast [1811.08903] of the CMS stopped-particle search with full Run-2+3 data and the causal-string f_stop. It gives an estimated m_Q ≈ 0.15-0.35 TeV over Λ ≈ 0.3 keV to ≳ 10 keV (computed; plausibly to ≳ 100 keV). That beats FASER (≤ 0.18 TeV) and D0 (≈ 0.11 TeV) only if the background is cut to O(10) events (S-8).

**By the four topics of the request:**

1. **Λ** (box A in §1).
   - Convention: convert the cosmology paper's T_c-based Λ with 1/0.709 (SU(2)), not 1/0.6.
   - The tracker-sensitive window is Λ ≈ 0.45-0.7 keV (50 % edge, truth level) up to ≈ 20-30 keV, where the pair merges.
   - Outside the window only the stopped-pair and merged/HSCP channels apply, and Λ ≳ 3 MeV is probably covered by resonance searches (UNVERIFIED).
   - The only UV framework that predicts the window (the SUSY-GUT ladder) predicts *doublets*, which are invisible to the tracker.
   - A discovery would imply T_RH ≲ 5-40 GeV.
2. **Oscillation length** (box B).
   - Exact closed forms: ℓ_max = 3.95 cm (γ*−1)(m/100 GeV)(keV/Λ)²; N_osc ≈ 12 (Λ/keV)², independent of m_Q.
   - The shorthand "1 cm (m/100 GeV)(keV/Λ)²" is wrong by ×0.4-2.7 event by event.
   - Scalars: ℓ_max ×1.7, N_osc ×0.81.
   - A fixed-p_T ISR kick biases ℓ_max by −10…−25 %.
3. **Propagation dynamics** (S-1, S-2, S-3, S-6, S-8).
   - The causal string is exact classical NG (independently confirmed to ≤ 1 % in thickness).
   - The Li method is a good approximation *when step-converged*. Its thickness deficit depends on γ*: ≈ 3 % low at γ* ≈ 1.05, ≈ 15 % low at the median γ* ≈ 1.3, and 30-35 % low in the median at γ* = 2-3 (single events −47 %…+36 %). It is Λ-independent at 0.6-3 keV. At the step printed in their paper (Eq.III.10) the Euler integration is not converged: thickness ×0.8-20, hits off by mm-cm. The step needed shrinks as Λ grows: ×10⁻³ at 2-3 keV, untested at 5 keV. Lab-time-slice straight strings are unusable (×1.5-75, median ≈ 9).
   - MS sets a truth-level floor of Δs ≈ 11/15/22 µm (200/500/1000 GeV).
   - The B thickness scales as Λ^−1.6…−2.0, is m_Q independent, and comes from a B ln(1/B) effect at near-miss crossings (independently confirmed). Li et al. already showed the formula is only order-of-magnitude.
   - Hit timing: median BTL delays 3.5/9.6/18.7 ns; ≈ 3 hits per layer for heavy pairs.
4. **Trajectory model** (S-4, S-5, S-7, S-2).
   - Degeneracy theorem: hits, times and dE/dx measure only ℓ₀ and velocities. m_Q comes from the MET recoil, giving ≈ 1-3 % on m_Q and 0.5-1.5 % on Λ for 30 events, limited by the MET scale.
   - MET-strip alignment rejects *random* planes ×13-34 at 95 % efficiency. The gain on the real Z(νν)+jets, W(ℓν)+jets and PU background is not known (S-5).
   - A 9-parameter causal global fit predicts OT hits to 15-55 µm (idealised).
   - With realistic hit resolution the coplanarity test is Inner-Tracker dominated (per-hit σ_n ≈ 17 µm IT, 0.25 mm PS, 8 mm 2S). Truth-level Δs cut values do not transfer (S-2).

**Other exploitable gaps:**
- the Athena MaxSteps killer for Λ ≳ 24 keV (S-9; do first);
- the merged pair is 9-21× MIP, not 2× (S-10);
- the doublet monojet recast (S-14);
- |q| = 2 singlets (S-17);
- the cosmology implication contour (S-15).

**Verified vs unverified headline numbers:**

| VERIFIED (independent code or closed form) | UNVERIFIED or idealised |
|---|---|
| Causal string = classical NG: thickness ratio 0.990-1.004 vs a conformal-gauge solver, 16 events [R1] | Phase-2 material per layer (≈ 19 % X0 at η = 0): drives the MS floor, f_stop and S-12 |
| Li method converged / causal = 0.84-1.05 at γ* = 1.28 (m = 500 GeV, p_T = 300 GeV; 30 events, 0.6-2 keV; 0.86 at 3 keV); γ*-dependent: 0.97/0.85/0.92/0.69/0.65 at γ* = 1.05/1.28/1.6/2/3 [R2]; labSS / Li = 1.6-73 on T2's own events [R1; F1; R2] | Knapen-Papucci / Sha et al. GNN code: prescription and step unknown |
| B ln(1/B) non-linearity, 1 + 0.10 ln(B₀/B) [R1; S] | PUPPI MET resolution at PU 200 (σ⊥ = 15-35 GeV scanned) and the 1-3 % MET scale |
| Degeneracy theorem (dimensional analysis) [R1] | Gain of the MET-strip cut against real backgrounds; predictive χ² with PU and alignment |
| ℓ_max, N_osc closed forms; Λ conventions; doublet cτ = 7.8 mm; T_RH^{21/4} freeze-in scaling [S; R1] | Stopped-pair live fraction at HL-LHC, background, endcap empty-BX trigger |
| Timing medians 3.5/9.6/18.7 ns (closed form on the same kinematic cache) [S] | Λ ≳ 3 MeV "excluded to 0.8-1 TeV"; doublet monojet limits (not opened) |
| MS thickness ∝ √(x/X0) (scaling of the same code, exponent 0.517) [S] | Δs efficiencies: truth level only; hit resolution and 2S z-blindness change the observable (S-2) |

---

## 1. Ranked list of distinct gaps

### Box A. What is known about Λ after this track (consolidated answer to "Λ")
| Question | Answer | Source / status |
|---|---|---|
| Convention | Λ ≡ √σ. The cosmology paper's "Λ" is T_c = 0.709√σ (SU(2)) or 0.646√σ (SU(3)), so its 1 keV is √σ = 1.41 keV (SU(2)). TH's 1/0.6 is 18 % off. Λ_MS-bar/√σ = 0.581/0.542. m₀(0⁺⁺)/√σ = 3.78/3.41 (SU(2)/SU(3)). For a non-fundamental IC representation or N_IC ≥ 4, σ_k/σ_1 follows Casimir scaling k(N−k)/(N−1) or the sine law sin(kπ/N)/sin(π/N) (UNVERIFIED, [T5 G-T5-8]), so Λ must be defined per representation | T1 G-T1-1; S check 5 (indep.); S-11 |
| **Existing exclusions (E singlet, fermion (1,1)₋₁, N_IC = 2)** | **Farina-Low** recast of CMS HSCP + monojet (12.9 fb⁻¹): m_Q > 650 GeV at Λ = 1 eV, > 150 GeV at 100 eV, none at 1 keV [1703.00912 Tab.II] (scalar: 350/60 GeV). **Evans-Luty** recast of CMS out-of-time (38.6 fb⁻¹): weak, m ≲ 0.1 TeV at Λ ≲ 0.15 keV (R2's reading of [1811.08903 Fig.5]). **D0**: 107 GeV (N = 2), Λ = 10 keV-1 MeV [1008.3547 abstract]. **FASER** (186 fb⁻¹, 13.6 TeV): the first exclusion above the weak scale for 300 eV < Λ < 100 keV, up to 179 GeV at 10 keV [2607.26195 abstract, text] (≈ 0.11-0.18 TeV across the range, R2's reading of Fig.5). Nothing above ≈ 0.18 TeV in the 0.3-100 keV window | 1703.00912; 1811.08903; 1008.3547; 2607.26195 |
| Where the tracker is sensitive | 50 % edge of the Δs < 100 µm finder at Λ_low ≈ 0.5/0.45/0.55→0.7 keV (200/500/1000 GeV) at **truth level**. Full efficiency (≥ 90 %) from ≈ 1 keV (200-500 GeV) or ≈ 2 keV (1 TeV). Upper edge set by merging of the pair at ≈ 20-30 keV. With realistic hit resolution (S-2) the coplanarity test is IT dominated; the lower edge is undefined until a cut is set at fixed background efficiency | T3 §9; S-2, S-3 |
| Below / above the window | Λ < 0.3 keV (< 1 oscillation in the tracker for 44-47 % of triggered pairs at 0.3 keV) and Λ ≳ 30 keV: only the stopped-pair (S-8) and merged-pair HSCP-like (S-10) channels. At Λ ≲ 0.1 keV the HSCP and monojet recasts already exclude 0.15-0.65 TeV (Farina-Low, row above). Λ ≳ 3 MeV: the pair annihilates promptly; dilepton/diphoton resonance searches probably exclude m_Q ≲ 0.8-1 TeV (UNVERIFIED). 0.1-3 MeV: displaced annihilation, no search (S-16) | T2 §3; T6 G-T6-5 |
| Theory prior | The SUSY-GUT ladder [0805.4642 Sec.2.5] gives SU(2) n_S = 3: √σ ≈ 0.8/2.6/6.4/15 keV at 0.2/0.5/1/2 TeV (×/÷3.9); SU(3) n_S = 9: 1.5/5.9/16 keV. But its EW quirks are *doublets*, which decay to the neutral member (cτ = 7.8 mm) before the first pixel layer: no coplanar signature (S-14). Neutral naturalness predicts GeV, not keV. The E-singlet coplanar search is motivated by generic hidden sectors (log-flat prior: ≈ 6 % of a ×2 prior in α⁻¹ lands in the window) | T1 G-T1-2, G-T1-3, G-T1-6 |
| Cosmology | If the IC sector ever thermalised, the whole window is excluded (Ω_G h² ≈ 2-10 (√σ/keV)). A discovery implies UV freeze-in with T_max ≲ m_Q/25 and T_RH ≲ 5-40 GeV (0.2-1 TeV). Glueballs are stable; no BBN/CMB decay bound | T1 G-T1-4; S-15 |
| Measuring Λ after a discovery | Hits measure only ℓ₀ = m_Q/σ. With the MET recoil: σ(Λ)/Λ ≈ 0.5 % (statistical, 30 events), 0.5-1.5 % including the MET scale. The B-only route works for Λ ≲ 2 keV | T4 §4; S-4 |
| N_IC = 3 instead of 2 | rate ×1.5; T_c/√σ 0.646; m₀/√σ 3.41; ΔN_eff (thermal) 0.57 instead of 0.21; GUT ladder SU(3) above | T1; S-11 |

### Box B. Oscillation length (consolidated answer to "quirk oscillation length")
- **Exact closed forms** for point-produced pairs [T2 §2.1-2.2; S check 1, indep.]:
  - ℓ_max = 3.947 cm (γ*−1)(m_Q/100 GeV)(keV/Λ)²;
  - full period T* = 4p*/σ;
  - N_osc(r < R) = σR/(2β*p_T) ≈ **12 (Λ/keV)² inside the CMS tracker, independent of m_Q**;
  - number of crossings ≈ 24 (Λ/keV)².
  - In the lab the vacuum string is straight with a fixed direction. Li's lab closed form [2002.07503 Eq.II.4-8] is exact in vacuum.
- **Typical values** (p_T(QQ̄) > 200 GeV, medians [T2 Tab.3.1]):
  - ℓ_max = 5.4 cm (500 GeV, 1 keV), 0.54 mm (10 keV), 60 cm (0.3 keV);
  - 44-47 % of triggered pairs make < 1 oscillation in the tracker at 0.3 keV.
- **Literature shorthands:**
  - "2 cm (γ−1)" is ×0.5 off (systematic);
  - "1 cm (m/100 GeV)(keV/Λ)²" [2404.13814; 2607.26195; 2512.20696] is right on average for E near 500 GeV but wrong by ×0.4-2.7 event by event.
- **Scalars Ẽ** (P-wave, sin²θ decay): ℓ_max is ×1.70-1.73 larger (median) and N_osc ×0.81 smaller at all three masses [T2 §3, l.127; verified in the T2 report]. These are two different ratios: ×1.7 is scalar vs fermion, and ×1.9 is scalar vs the "1 cm (m/100)" rule [T2 table]. The Ẽ alternate therefore needs its own window: longer arcs and fewer crossings.
- **ISR modelling:** a fixed-p_T ISR kick biases ℓ_max by −10…−25 % and N_osc by +20 % (S-13). Generate with a V+jet matrix element.
- **What it decides:**
  - the hit multiplicity (≈ 3 hits per layer for heavy pairs, S-6);
  - the seeding regime (resolved arcs for Λ ≲ 1 keV, aliased zig-zag band for Λ ≳ 3 keV, S-7);
  - the Athena step budget (S-9).

### Ranked table
Ranking criterion: (impact on the CMS search or on constraints) × confidence ÷ remaining effort.

Type:
- **C**: correction to the existing plan (erratum);
- **N**: new capability;
- **Ch**: new or complementary channel;
- **D**: documentation.

Verdicts: EXPLOIT / WORTH A CHECK / NOT A GAP. IDs are unchanged from v1; the Rank column changed.

| Rank | ID | Type | Gap (short) | Best number(s) | Remaining effort | Conf. | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | S-1 | N + C | Trajectory model: causal NG string validated; Li method 3-35 % low if converged (γ*-dependent); printed step not converged; lab-slice straight strings unusable | causal vs independent NG: 0.990-1.004; Li/causal 0.97 (γ* 1.05), 0.85 (1.28), 0.65-0.69 (2-3); labSS/causal 1.5-75 | days (adopt `T3_causal.py`) | high | **EXPLOIT** |
| 2 | S-6 | C | Timing: medians, late-hit losses, multiple hits per layer | BTL median 3.5/9.6/18.7 ns; 2S lost 7-33 % (500 GeV), 44-68 % (1 TeV) | done | high | **EXPLOIT** |
| 3 | S-3 | C + N | Thickness physics: Λ^−1.6…−2.0, m_Q-independent, B ln(1/B) at crossings; revised window | 32-38 µm at 1 keV; Λ_low(50 %, truth) 0.45-0.7 keV (realistic resolution: undefined until set at fixed background) | 1-2 weeks (analytic theory) | medium-high | **EXPLOIT** (window, V2); WORTH A CHECK (analytic) |
| 4 | S-2 | C + N | MS floor (truth level) and realistic hit resolution: the coplanarity test is IT dominated | Δs_MS 11/15/22 µm; per-hit out-of-plane resolution IT ≈ 17 µm, PS ≈ 0.25 mm, 2S ≈ 8 mm | days (resolution-aware finder, real material) | medium | **EXPLOIT** |
| 5 | S-4 | N | Degeneracy theorem and (m_Q, Λ) measurement | 1-3 % (m_Q), 0.5-1.5 % (Λ), 30 events, MET-scale limited | days (write-up); weeks (real fit) | high (theorem), medium (numbers) | **EXPLOIT** |
| 6 | S-5 | N | MET-strip alignment | ×13-34 rejection of *random* planes at 95 % eff.; real-background gain unknown | days | high (geometry), low (real gain) | **EXPLOIT** |
| 7 | S-9 | C | Athena step-count killer | MaxSteps 2×10⁶ kills quirks for Λ ≳ 24 keV | hours (do first) | medium | **EXPLOIT** (config) |
| 8 | S-8 | Ch | Stopped-pair delayed annihilation | f_stop(EB+HB) 1.0 ± 0.3 %; HL-LHC reach 0.3-0.55 TeV (EB+HB), ≲ 0.65 TeV (B = 0, long delay); Run 2+3 update of Evans-Luty's recast 0.15-0.35 TeV | weeks | medium-low | **EXPLOIT** (complementary, Λ edges; update of [1811.08903]); WORTH A CHECK (Run-2/3 update) |
| 9 | S-10 | C + Ch | Merged pair is 9-21× MIP; HSCP-like category | median 9× (500 GeV), 21× (1 TeV) MIP | days | medium | **EXPLOIT** (correction); WORTH A CHECK (recast) |
| 10 | S-7 | N | Causal 9-parameter global fit; predictive χ²; two-regime seeding | idealised prediction 15-55 µm per OT hit (1 keV) | weeks | medium (idealised) | **EXPLOIT** (approach); numbers are upper bounds |
| 11 | S-11 | D | Λ conventions and closed-form kinematics (boxes A, B) | T_c/√σ = 0.709; ℓ_max, N_osc closed forms; scalar ×1.7 / ×0.81 | hours | high | **EXPLOIT** |
| 12 | S-12 | C | Mean energy loss is a first-order trajectory effect | 40 µm-1.5 mm OT shifts; ±10 % material ⇒ 4-150 µm | days | medium | WORTH A CHECK |
| 13 | S-13 | C | Production modelling of the ISR tail | fixed-p_T trick: ℓ_max −10-25 %; 37 % reach spread between groups | weeks (experimental) | high | EXPLOIT (already in STRAT §12) |
| 14 | S-14 | Ch | GUT-ladder Λ strip (doublets); doublet invisibility ⇒ monojet + soft pions | doublet cτ 7.8 mm; rate ×14 of E | days | medium (ladder), low-med (recast) | EXPLOIT (lines); WORTH A CHECK (recast) |
| 15 | S-15 | N | Cosmology: discovery ⇒ reheating bound; 2512.20696 normalisation | T_max ≲ m_Q/25; T_RH ≲ 5-40 GeV; Ω ∝ T_RH^{21/4} not T⁷ | days | medium | EXPLOIT (figure); WORTH A CHECK (note) |
| 16 | S-16 | Ch | Λ ≳ 3 MeV prompt resonance; 0.1-3 MeV displaced band | σ×BR(ℓℓ) = 1.1 fb at 500 GeV; probably excluded to 0.8-1 TeV (UNVERIFIED) | days | low | EXPLOIT (scoping); WORTH A CHECK |
| 17 | S-17 | Ch | Multi-charged singlets \|q\| = 2 | σ ×4; reach ≈ 1.3 TeV; Λ_low ×≈1.4 | days | medium | WORTH A CHECK |
| 18 | S-18 | N | Trigger, PU-200, PU-vertex association and HLT realism (experimental) | 23-47 % of OT crossings make 2 GeV stubs at Λ ≤ 3 keV | months | medium | WORTH A CHECK (experimental) |
| 19 | S-19 | N | ε (glueball emission per crossing) depends on miss distance | ε active only for b < 1/Λ | weeks | low | WORTH A CHECK (low priority) |
| 20 | S-20 | N | Exclusive γγ → QQ̄ with PPS as a mass handle | 35 events at 500 GeV, 3 ab⁻¹ | weeks | medium | WORTH A CHECK (post-discovery) |

Ranks 2, 3, 4, 7, 9, 11, 12 and 13 are mainly **corrections** of the existing plan. Ranks 1, 5, 6 and 10 are **new capabilities**. Ranks 8, 9, 14, 16 and 17 are **channels**.

### S-1 Trajectory model: the causal Nambu-Goto string is validated; the Li method is a γ*-dependent 3-35 % approximation that needs a much finer step than printed; lab-time-slice straight strings are unusable

**What v1 claimed, and why it is withdrawn.**
- v1 claimed that "every published central-detector trajectory model is wrong at the order that matters". The numbers were thickness ×0.04-60, OT hits 0.2-35 mm off, fake MS thickness 0.2-21 mm, and 140-570 µm frame dependence.
- All of them came from T2's `LabStraightString` (labSS) and `CMStraightString` (cmSS). These were written as stand-ins for Li et al. but are *not* Li et al.'s algorithm. T2 had checked that Li's ŝ reduces to the lab-simultaneous direction *on the exact vacuum solution*. With F_ext ≠ 0 the two differ at exactly the order in question:
  - Li et al. advance the quirks at different lab times so that (x₁ − x₂)·P = 0, which is CM simultaneity and a Lorentz-invariant condition [1911.02223 Eq.III.6-7].
  - They take ŝᵢ = Δr − Δt vᵢ [Eq.III.8-9].
  - labSS uses equal lab times, a frame-dependent choice that no paper made [R1 A-1].
- The claim is therefore withdrawn.

**Evidence now available** (m_Q = 500 GeV, γ* = 1.28, p_T = 300 GeV, 3.8 T, no material unless stated, 10 barrel radii):

| Comparison | Result | Source |
|---|---|---|
| Causal port (`T3_causal.py`) vs an **independent conformal-gauge NG solver** (delay ODE for the left/right movers, massive endpoints, Lorentz force at the ends) | thickness ratio 0.990-1.004; out-of-plane hit differences ≤ 0.4 µm; all hits ≤ 8.2 µm (16 events, 0.6-3 keV); vacuum before the first crossing 6×10⁻⁴ µm; canonical momentum conserved to ≤ 2×10⁻³ GeV | [R1: `R1_conformal_ng.py`, `figures/R1_conformal_ng_out.txt`] (indep.) |
| **Literal Li integrator** (Eq.III.6-10, explicit Euler), step-converged, vs causal | thickness ratio 0.84-1.04, median ≈ 0.85, at 0.6-2 keV (18 events, seed 11). Max OT-hit difference 53-80 µm (0.6 keV) and 27-430 µm (1 keV) at 10⁻³ × the printed step. **All at one kinematic point:** m = 500 GeV, γ* = 1.28, p_T = 300 GeV | [R1: `R1_li_literal.py`, `figures/R1_li_literal_out_a/b.txt`] (indep.) |
| Same, **on T2's own events** (seed 7: the events behind v1's S-1 numbers; same γ* = 1.28 recipe) | Li(×0.003)/causal = 0.84-1.05, median 0.88 (0.6-2 keV, 12 events); labSS/causal = 1.5-75 (median 8.9) and **labSS/Li = 1.6-73 (0/12 events within ±50 %)**: labSS is not a stand-in for Li. cmSS/causal = 0.05-0.78 | [F1: `F1_standin.py`, `figures/F1_standin_out.txt`] (indep. of T2's code) |
| Li at **its printed step bound** (Eq.III.10: ε < 10⁻⁴ ns (m_Q/100 GeV)(keV/Λ)²) | thickness ×0.8-20 off at 0.6-3 keV (×10-70 at 5 keV), OT hits 6-250 mm off. This is Euler non-convergence: the error falls as the step is reduced. Eq.III.10 says the step "should satisfy" the bound, so the step Li et al. actually used is unknown | [R1]; [F1: `F1_standin.py`] |
| **Convergence worsens with Λ** (R1 final runs) | The fraction of the printed bound needed for convergence shrinks as Λ grows. At 3 keV, Li ×0.003 / causal = 0.67-1.06 (6 events) and changes by > 10 % between ×0.01 and ×0.003 in 4 of 6 events, with OT hits 0.5-9.6 mm off. **R2 ran ×0.001:** two of three events are unchanged from ×0.003 and give 0.855-0.856; the third gives 0.67 with a different hit count. So the 3 keV value is converged at ×10⁻³ (≈ 3×10⁸ steps per event) and equals the 1-2 keV value. At 5 keV, ×0.01 gives 0.9-3.4 × causal and 1-4 mm hits (finer steps not run). Explanation (ESTIMATE): the printed bound scales as ℓ₀ ∝ Λ⁻², but the step must resolve the near-miss crossing, where the miss distance b ∝ Λ⁻⁴. The required *fraction* of the printed bound therefore falls roughly as Λ⁻², and the cost grows as Λ⁴ (~10⁸ steps per event at 2 keV, ~10⁹-10¹⁰ at 5 keV). So the Li method is practical only at Λ ≲ 3 keV unless the step is adapted near crossings; 5 keV is untested below ×10⁻² | [R1: `figures/R1_li_literal_out_b.txt`, `_c.txt`]; [R2: `figures/R2_li_fine_out.txt`] |
| **γ* dependence of the converged Li deficit** (new, R2) | Λ = 1 keV, m = 500 GeV, p_T = 300 GeV, 5 events per γ*, converged steps. Median Li/causal = **0.97 / 0.85 / 0.92 / 0.69 / 0.65 at γ* = 1.05 / 1.28 / 1.6 / 2 / 3**. At γ* ≥ 2 single events span 0.53-1.36, some with different hit counts, and out-of-plane hit differences reach 30-124 µm. The trend is what neglected retardation and curvature should give: the corrections grow with the internal velocity β*. The deficit is therefore a γ* effect, not a Λ effect (the 3 keV value is the same as at 1 keV). For the triggered spectrum (median γ*−1 ≈ 0.27, 84th percentile γ* ≈ 2.0-2.5 [T2]) "≈ 15 %" describes the median event only | [R2: `code/R2_li_checks.py`, `figures/R2_li_gamma_out.txt`, `R2_li_gamma2_out.txt`] |
| **Residual mm-scale hit differences at 2 keV** (R1 saw 0.2-10 mm at ×0.003) | Also step non-convergence of the Li Euler integration, not a physics difference. At ×0.001 (6 events) the maximum hit difference falls from 0.2-9.8 mm to 0.07-0.53 mm, and the median to 5.5-18 µm. Li ×0.001 vs ×0.003 still differ by 0.14-1.1 mm, so the residual 0.1-0.5 mm at ×0.001 is consistent with being pure integration error (first-order Euler: the error falls roughly ∝ step). Monotonic convergence is not shown, so it is not a strict upper bound. Mechanism: a slow **in-plane** oscillation-phase drift. The time lag grows to 1-3 mm/c by the outer layers. At near-tangent multiple crossings of one layer the drift also changes the hit count (a crossing pair appears or disappears), and nearest-time matching then pairs different crossings, giving mm-cm "differences". Out-of-plane differences stay ≤ 10.5 µm at ×0.001 (≤ 38 µm at ×0.003) at this γ* = 1.28 point; at γ* = 2-3 the converged out-of-plane differences are 12-124 µm (R2), plane normals agree to ≤ 43 mdeg (0.75 mrad), the causal hits scatter about the Li plane by the causal thickness itself (ratio 1.00-1.03), and the Li thickness is 0.85-1.05 of causal. **No effect on the plane finder; it matters for hit-position prediction (S-7) and GNN truth hits if the integration is not converged** | [F1: `F1_li_phase.py`, `figures/F1_li_phase_out.txt`] |
| Li + MS (thin scatterers, B = 0) vs causal + MS | median 13 µm vs 30 µm (1 keV, 8 events); 11.9 vs 15 µm (3 keV, 8 events); 33 vs 22 µm (10 keV, 6 events; Li at ×0.01, which the B-only runs show is not converged at this Λ). The 16-84 % ranges overlap; no secular growth with the number of crossings; no mm-scale thickness. The "fake 0.2-21 mm" of T3 §3.1 is a labSS property | [R1: `R1_li_ms.py`, `figures/R1_li_ms_out.txt`] |
| labSS / cmSS (T2's variants) | thickness ×1.5-75, median ≈ 9 (labSS; R1 events ×4-60, T2's own events ×1.5-75) and ×0.04-0.9 (cmSS) relative to causal; frame dependence 140-570 µm; spurious work −1.6 MeV per crossing (labSS); fake MS thickness grows with the number of crossings | [T2 §5.1; T3 §3.1] (these numbers stand, but describe codes nobody else uses) |
| Knapen et al. [1708.02243] and Sha et al. GNN samples [2410.00269] | 1708.02243 Sec.II says only that "in the centre-of-mass frame v∥ lies along the displacement". The Knapen-Papucci code has not been seen by anyone on this track. **Status unknown.** If it implements CM simultaneity like Li and is step-converged, expect ≈ 15 %. If it uses lab time slices, expect labSS-like errors. If it is unconverged, expect mm-scale OT hits | — |

**What survives (the re-scoped S-1):**
- (i) **The causal string (Athena algorithm, `T3_causal.py`) is exact classical Nambu-Goto with point-mass endpoints.** Two independent formulations agree to ≤ 1 %. It is the production model. Its validity caveat is the classical NG effective theory at the near-miss crossings, where separations fall below 1/Λ (X-13, R1 B-1): negligible for Λ ≲ 3-10 keV, a 10-30 % model uncertainty on the B-thickness for Λ ≳ 10-20 keV (ESTIMATE).
- (ii) **The Li method is a good approximation** *when step-converged*. Its thickness deficit is ≈ 3 % low at γ* ≈ 1.05, ≈ 15 % low at the median γ* ≈ 1.3, and 30-35 % low in the median at γ* = 2-3 (single events −47 %…+36 %). The deficit is the same at 1, 2 and 3 keV. OT hits are within 0.03-0.4 mm at ≤ 1 keV and ≲ 0.5 mm at 2 keV (γ* = 1.28). Convergence needs ≈ 10⁻²-10⁻³ of the printed bound at 0.6-3 keV, i.e. ~10⁸-3×10⁸ Euler steps per event, and a fraction that shrinks roughly ∝ Λ⁻² (untested at 5 keV). **At the printed bound it is not converged** (×0.8-20 at 0.6-3 keV).
- (iii) **A lab-time-slice straight string, the naive choice for anyone writing a fast propagator, is badly wrong** (×1.5-75 in thickness, median ≈ 9; non-covariant; mm-scale fake thickness with MS). This is a warning, not a criticism of published work.
- (iv) **Knapen-Papucci / Sha et al.: unknown** until the code is inspected.

**Exploitation:**
- (c, e) Use `T3_causal.py` as the production propagator (W3 fast propagator, GNN training truth, trajectory fit). It is now validated by an independent solver.
- (e) Validate any external sample (Zenodo 17941765 / Sha et al., any Li-type code) against `T3_causal.py` before use: thickness ratio, OT residuals, step convergence.
  - **No fixed ratio is a valid target.** A converged CM-simultaneous code should reproduce `T3_causal.py` event by event within the γ*-dependent band (≈ 0.97 at γ* ≈ 1.05, ≈ 0.85 at 1.3, 0.5-1.4 per event at γ* ≳ 2). OT residuals should be sub-mm. Compare in bins of γ* over the triggered spectrum, not as one number.
  - mm-scale OT residuals indicate an unconverged integration or a lab-time-slice prescription.
  - The causal-vs-Li difference is *superseded*, not a systematic.
- (b) Guidance for fast propagators: never use lab-time-slice straight strings; CM simultaneity is essential; check step convergence on hit positions, not only on the thickness.
- (f) Material for P1 (re-scoped, §5).

**Effort:** days. **Confidence:** high. **Verdict: EXPLOIT** (adopt and validate). The claim "published models are wrong at O(1)" is withdrawn.

### S-2 Multiple scattering floor (truth level) and realistic hit resolution
**Statement.**
- No published quirk propagation includes stochastic material effects. Knapen neglects material [1708.02243 Sec.II]. Li et al. include only the mean dE/dx with a 10 % smear [2002.07503 Sec.VII]. Evans-Luty "have not attempted to model" the transverse kicks [1811.08903 App.B].
- T5's 50-400 µm upper bound [T5 G-T5-1] is superseded.

**Truth-level numbers** [T3 §3.2, 60 events per point for Λ ≤ 3 keV]. *All are at true hit positions*, with the reconstructed Phase-2 material (≈ 19 % X0 at η = 0, UNVERIFIED per layer).
- Median Δs_MS = 11/15/22 µm at m_Q = 200/500/1000 GeV, nearly Λ independent (84th percentile ≤ 67 µm). MS dominates the B thickness for Λ ≳ 1.5-2 keV.
- Pass fraction of Δs < 100 µm (B + material): 0.93-1.00 for Λ = 1-30 keV.
- A Δs < 30 µm cut keeps 0.92-0.93 (200 GeV), 0.68-0.83 (500 GeV) and 0.55-0.67 (1 TeV) at 3-10 keV [T3 §9 item 3].
- New-seed re-check: Δs(M) = 17.6 / 18.2 µm at 3 keV (500/1000 GeV), against T3's 17/24. That is consistent within the ±25 % MC statistics (30 events), not a precision confirmation [S check 9].
- Scaling check: Δs_MS ∝ (x/X0)^0.517 over ×0.25-×4 material [S: `S_msscale.py`]. This tests the *scaling of the same code*, not the material itself, which stays UNVERIFIED.
- **Mechanism** [T3 §3.2 items 6-7]: the kick is shared by the pair (δp/|P_QQ̄|), and the near-miss crossings convert part of it into a slow rotation of the oscillation axis.

**Realistic hit resolution (new; answers R1 B-2)** [F1: `F1_smear.py`, `figures/F1_smear_out.txt`]. Inputs:
- the same causal events (B + material, LO DY+ISR, p_T > 200 GeV, |η| < 1);
- hits smeared with binary-readout errors (uniform, width = pitch; pitches UNVERIFIED, TDR not opened):
  - IT 25 × 100 µm² (σ_rφ 7 µm, σ_z 29 µm);
  - PS 100 µm × 1.5 mm (29 µm, 0.43 mm);
  - 2S 90 µm × 5 cm, no stereo (26 µm, 14 mm).

Findings:
- **The out-of-plane resolution of one hit is σ_n = √((n·φ̂)²σ_rφ² + n_z²σ_z²)**, with n the plane normal. The median |n_z| of the fitted planes is 0.56, which gives a median σ_n of **≈ 17 µm (IT), ≈ 0.25 mm (PS) and ≈ 8 mm (2S)** (15/0.20/6.7 mm at 10 keV).
  - A 2S hit gives (r, φ) only. Every z-line intersects the plane, so it tests coplanarity only through the 5 cm strip length.
  - The coplanarity test at the 10-100 µm scale is therefore carried by the **4 IT layers** (≈ 3 hits each for heavy pairs). The PS modules contribute at the 0.25 mm level. The truth-level Δs, which is dominated by the outer layers through their lever arm, is not what a detector measures.
- An unweighted eigenvalue Δs on smeared hits is dominated by the 2S z smearing (mm-cm) and is meaningless. A plane finder must use a resolution-weighted fit, for example χ²(n) = Σ(n·hᵢ)²/σ_n,ᵢ².
- Results (60 events per point; the efficiencies have ±6 % binomial errors):

| m_Q | Λ [keV] | truth Δs (median) | truth Δs, IT+PS hits only | t_est (median) | effective resolution s_eff | χ²/ndf (median) | f(Δs_truth < 100) | **f(t_est < 100)** | f(χ² p > 1 %) | f(Δs_truth < 30) | f(t_est < 30) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 500 | 0.3 | 253 µm | 59 µm | 30 µm | 28 µm | 1.36 | 0.23 | 0.63 | 0.65 | 0.03 | 0.50 |
| 500 | 0.45 | 137 | 70 | 23 | 28 | 1.24 | 0.42 | 0.73 | 0.68 | 0.08 | 0.53 |
| 500 | 0.6 | 72 | 41 | 17 | 28 | 1.25 | 0.65 | 0.88 | 0.70 | 0.22 | 0.63 |
| 500 | 1 | 31 | 16 | 9 | 28 | 1.12 | 0.98 | 0.98 | 0.92 | 0.48 | 0.83 |
| 500 | 3 | 14.5 | 6.4 | 4 | 27 | 1.05 | 1.00 | 0.97 | 0.97 | 0.73 | 0.88 |
| 500 | 10 | 12.5 | 5.2 | 7 | 25 | 1.08 | 1.00 | 0.97 | 0.83 | 0.82 | 0.87 |
| 1000 | 0.3 | 237 | 81 | 40 | 30 | 1.30 | 0.13 | 0.60 | 0.63 | 0.03 | 0.45 |
| 1000 | 0.45 | 117 | 63 | 28 | 29 | 1.36 | 0.38 | 0.72 | 0.62 | 0.05 | 0.52 |
| 1000 | 0.6 | 83 | 41 | 17 | 27 | 1.25 | 0.67 | 0.93 | 0.67 | 0.17 | 0.67 |
| 1000 | 1 | 35 | 18 | 10 | 27 | 1.13 | 0.98 | 0.97 | 0.93 | 0.43 | 0.95 |
| 1000 | 3 | 28 | 9.6 | 4 | 27 | 1.02 | 0.93 | 1.00 | 0.97 | 0.55 | 0.93 |
| 1000 | 10 | 33 | 11 | 9 | 23 | 1.11 | 0.93 | 0.98 | 0.85 | 0.48 | 0.90 |

- **Reading the table:**
  - The event-level out-of-plane resolution is s_eff ≈ 23-30 µm. That is the same size as the MS floor, so the MS floor is not resolvable event by event (R1 B-2 confirmed).
  - The large truth-level thickness at low Λ sits mostly in the outer (2S) layers, which carry no out-of-plane information. The IT+PS truth thickness is ×2-4 smaller.
  - **t_est and the truth Δs are different observables with different background rejection, so their efficiencies must not be compared at equal cut values.** At 0.3-0.45 keV, 60-73 % of the signal pass t_est < 100 µm, against 13-42 % for truth Δs < 100 µm. This is **not** an acceptance gain: an IT-dominated test (≈ 12 hits at r ≤ 14.6 cm) also passes any pair of prompt tracks with p_T ≳ 100 GeV, which are coplanar with the PV to within the helix sagitta, ≈ 0.32 mm × (10 GeV/p_T) at r = 14.6 cm [R2-B4]. Likewise, "t_est < 30 µm keeps 83-95 %" is not comparable with "truth Δs < 30 µm loses 30-45 %".
  - The lower window edge is **undefined** until the cut is set at a fixed background efficiency (prompt-track pairs, PU fakes). For low-Λ signal the discrimination must come from the OT rφ non-helicity, the non-monotonic pair separation and the hit multiplicity, not from IT coplanarity.
  - The χ² p-value test (p > 1 %) keeps 92-97 % at 1-3 keV, 83-85 % at 10 keV and 62-70 % at ≤ 0.6 keV, where B-induced curvature is resolved by the IT.
- Caveats: pitch/√12 binary resolution, perfect alignment, no PU or noise hits, known assignment, no charge sharing (all UNVERIFIED). The real optimisation is the experimental team's (Phase 2/3).

**Exploitation:**
- (c) The plane finder (STRAT §9.1) must be resolution-aware, with IT-dominated coplanarity. The truth-level cut values (100 µm, 30 µm) do not transfer.
  - The signal efficiency of a resolution-weighted thickness cut (t_est < 100 µm) is 0.97-1.00 at 1-10 keV and still 0.60-0.73 at 0.3-0.45 keV (table above).
  - The background rejection then comes from the IT + PS out-of-plane test, the multiplicity pattern (≈ 3 hits per layer), the MET-strip alignment (S-5) and the predictive χ² in rφ (S-7), not from a 100 µm 3D thickness.
- (e) The material-budget uncertainty enters as √(x/X0) (±20 % ⇒ ±10 % on Δs_MS). That matters only for cuts near the IT resolution.
- (d) MS sets the floor below which the thickness carries no Λ information (S-4).

**Effort:** days (a resolution-aware finder and the real material, which needs CMS access). **Confidence:** medium (material UNVERIFIED; pitches UNVERIFIED; no PU, no alignment). **Verdict: EXPLOIT.**

### S-3 Plane-thickness physics: Λ^−1.6…−2.0, m_Q-independent, non-linear in B at the crossings; revised window
**Statement.**
- The literature thickness d ≈ 1.16 µm (m_Q/100 GeV)(keV/Λ)⁴(B/T) [1911.02223 Eq.III.12] sets the strategy's window edge Λ_low ∝ m_Q^{1/4} [STRAT §4.4].
- **Credit:** Li et al. themselves show that their *numerical* thickness D_N deviates from this analytic D_A by factors 10⁻³-10³ (Fig.8). They state agreement "within an order of magnitude" for n_T ~ 1-100, and their published reach uses the numerical thickness [2002.07503 App.C; 1911.02223 Fig.4]. The formula's failure is therefore a criticism of **this project's** use of it (STRAT §4.4, §9.4 V2), not of published analyses [R1 B-3].
- The causal string (B only, truth level, median) gives [T3 §3.2]:

| m_Q [GeV] | Λ [keV] | causal B-only Δs (median) | formula d |
|---|---|---|---|
| 200-1000 | 1 | 32-38 µm | 9-44 µm |
| 200-1000 | 3 | 3.9-5.2 µm | 0.1-0.55 µm |
| 200-1000 | 10 | 0.4-0.7 µm | ≤ 0.004 µm |

- **What is new** (not in Li App.C):
  - (i) local exponents Λ^−1.6…−2.0 (median ≈ −1.9; T3 table: 1.76-1.92 over 1→3 keV and 1.63-1.98 over 3→10 keV), with ~m_Q independence [T3 §3.2; R1 §2];
  - (ii) T4's in-plane x_B ≈ 0.5 qBR/σ shows the same scaling [T4 §3.2];
  - (iii) the response is **non-linear in B**. It is exactly linear before the first crossing and grows like 1 + 0.10 ln(B₀/B) after it (31-35 % at B/20). This is **independently confirmed** with the conformal-gauge solver: 0.29-0.39 at k = 20, 0.13-0.14 at k = 4, 1 + 0.10 ln [R1: `R1_Blinearity.py`], [S: `S_Bnonlin.py`, `S_Bscan.py`];
  - (iv) the correction of the project's formula-based window.
- **Interpretation (ESTIMATE, heuristic; the coefficient is fitted, not derived).** At a crossing the partner is offset transversely by b ∝ qB. The string then pulls transversely with σb/|x| while the longitudinal separation |x| → 0. The impulse ∫σb/(v|t|) dt is cut off at |x| ~ b, which gives (σb/v) ln(ℓ/b), i.e. a B ln(1/B) term.
  - With b ∝ B/Λ⁴ and ℓ ∝ 1/Λ², x ∝ ε_B[1 + c ln(Λ²/B)] with c ≈ 0.08-0.11. That predicts B^0.89-0.92 and Λ^−1.78…−1.84, matching the measured B^0.91 [T4] and Λ^−1.6…−2.0 [T3] (algebra re-checked by R1).
  - The formula d is the odd-crossing miss distance b ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] (Li's d_E [2002.07503 Eq.V.8]). It is not the thickness accumulated over the tracker.
- **NG validity at the crossings** [R1 B-1]. The odd-crossing miss distance falls below 1/Λ ≈ 2 Å (keV/Λ) only for Λ ≳ 20 keV; even crossings do so already from Λ ≈ 3 keV [T2 §6.3]. Since the impulses are ∝ b, even crossings are subdominant, so the classical-NG result is safe for Λ ≲ 10 keV. For Λ ≳ 10-20 keV it carries a model uncertainty of order ln(1/(bΛ))/ln(ℓ/b) ~ 10-30 % on Δs_B (ESTIMATE). By then Δs_B ≪ Δs_MS, so this does not affect the window.

**Revised window** [T3 §9]. *Truth level*:
- 50 % edge of the Δs < 100 µm finder: Λ_low ≈ 0.5/0.45/0.55→0.7 keV at 200/500/1000 GeV (B → B + material). That is inside the strategy's band (0.54-0.81 keV), slightly lower and flatter in m_Q.
- At 1 TeV the ≥ 90 % plateau starts at Λ ≈ 2 keV (MS).
- The upper (merging) edges are unchanged.
- With a resolution-aware finder (S-2) the truth-level edge does not transfer. The realistic edge is undefined until the cut is set at fixed background efficiency (R2-B4).

**Exploitation:**
- (b, e) Replace the formula-based edges and validation item V2 (STRAT §9.4) by causal-string efficiency curves, computed with realistic resolution.
- (c) Any analytic or perturbative fast model (including "vacuum + first-order B") must be calibrated against the full causal propagator.
- (f) The physics content of P1 (§5).

**Effort:** 1-2 weeks for an analytic theory of the crossing impulse. **Confidence:** medium-high (two independent NG solvers agree on the thickness and on the non-linearity at 0.6-3 keV; statistics 60 events per point). **Verdict: EXPLOIT** (window and V2 replacement); **WORTH A CHECK** (analytic B ln B theory).

### S-4 Degeneracy theorem and measurement of (m_Q, Λ) after discovery
**Statement.**
- Hits, hit times and dE/dx depend on (m_Q, Λ) only through ℓ₀ = m_Q/σ and the velocities. This follows exactly from the scale invariance of the NG + point-mass action. The vacuum Fisher column for ln σ is ≤ 3×10⁻⁷ of the largest [T4 §2.1, §3.1].
- Only three things break the degeneracy: the recoil (MET = p_T(QQ̄)), the B field through ε_B = qB/σ, and material (∝ 1/m_Q).
- Confirmed independently by dimensional analysis of the EoM + Highland + Bethe [R1 §3].
- This corrects the hope that dE/dx [1708.02243 App.A] or crossing spacing and timing [T2 G-T2-4; T3 §6] measure m_Q or Λ (X-8).

**Numbers** (Cramér-Rao, MS included; T4 §4.3).

| Handle | per event | N = 30 events, statistical | N = 30, with the 1-3 % MET/JES scale |
|---|---|---|---|
| +MET (σ⊥ = 25 GeV) | σ(m)/m 6-10 %, σ(Λ)/Λ 3-5 % | 0.9-1.2 % / 0.5-0.6 % | **≈ 1-3 % / 0.5-1.5 %** (systematics limited) |
| B only (no recoil) | σ(Λ)/Λ 16-20 % at 1 keV | 1.5-2.2 % at 1 keV; 17-29 % at 3 keV; not measurable at 10 keV | needs q known and the crossing physics modelled to ≲ 10 % (confirmed at 1 keV, S-3) |

**Caveats** (now in the headline):
- (i) this is a local CRB with known hit-to-quirk assignment, no PU, and the global minimum assumed (aliasing at 10 keV);
- (ii) σ⊥ at PU 200 (PUPPI) is UNVERIFIED and scanned over 15-35 GeV; Gaussian MET tails are assumed;
- (iii) γ* and (βγ)_T, which convert MET into m_Q, come from the trajectory model. A 15 % change of out-of-plane quantities between models would not move γ* at first order, but this was not tested.
- (iv) T4 assumes true MET = p_T(QQ̄), but the pair itself deposits ≲ 5 GeV in the calorimeters [1911.02223 Sec.V, via T4]. On a 200-300 GeV recoil that is a one-sided ≲ 2 % MET bias, the same size as the scale floor; it is correctable [R2-C6].
- Arithmetic check: 7-9 %/√30 ≈ 1.3-1.6 %. The quoted 0.9-1.2 % implies a benefit from high-p_T events (plausible) [R1 B-5].

**Exploitation:**
- (d) The first quantitative answer to "parameter measurement after discovery" [T5 G-T5-7].
- (f) P2.
- (e) Remove "the trajectory fit measures m_Q and Λ" and "dE/dx measures the mass" from strategy language.
- **The real fit:** the CRB is local and the likelihood is multi-modal (aliasing) with an ℓ₀ ridge. The natural tool is **simulation-based inference** (neural posterior or likelihood-ratio estimation) trained on `T3_causal.py` events. That propagator is fast enough for large training sets; MS stochasticity and the MET systematic would be included as nuisances. This is a suggestion only; not studied (R1-constructive B7).

**Effort:** days (write-up); weeks (a real fit with assignment ambiguity and PU). **Confidence:** high (theorem), medium (numbers). **Verdict: EXPLOIT.**

### S-5 MET-strip alignment (rejection against *random* planes)
**Statement.** In vacuum the strip axis is exactly φ_pair. The B wobble is ≲ 2×10⁻⁴ rad and the hit-fit error 3×10⁻⁵ rad, so Δφ(MET, strip) is set by the MET resolution alone [T4 §5.1].

**Numbers** (geometry, verified by code reading and a closed form [R1 C-5; S check 11]):
- |Δφ| < 0.15-0.25 rad keeps 95 % of the signal.
- It rejects **isotropic random planes** by π/δ₉₅ = ×13 (σ⊥ = 35 GeV) to ×34 (σ⊥ = 15 GeV).
- The φ road for seeding (÷16) is **the same wedge**. The two factors must not be multiplied as if independent.

**What is expected against the real background** (qualitative, ESTIMATE; answers R1-constructive A3 and R1-critical C-5). The background to a coplanar-plane search with MET is Z(νν)+jets, W(ℓν)+jets with a lost lepton or τ_h, and multijet with fake MET, all at PU 200.
- **Fake planes built from PU tracks or hits** are uncorrelated with the hard-scatter MET, so the geometric ×13-34 applies *per candidate plane*. If the finder produces k independent fake candidates per event, the per-event rejection is ≈ (13-34)/k.
  - If a PU jet is not removed by PUPPI, the MET it induces points *opposite* to it. A plane built from its tracks is then anti-aligned and rejected by the directed cut, so the correlation helps.
- **Hard-scatter activity in Z(νν)+jets** is concentrated opposite the MET (the recoil jets). After the standard Δφ(jet, MET) > 0.5 cleaning, the wedge around the MET is depleted of jet activity, so the rejection of UE-built planes is at least geometric.
- **W(τν)+jets and W(ℓν) with a lost lepton** are the correlated case. For a boosted W the τ_h (or the lost lepton) and the neutrinos are roughly collinear with the MET, so tracks or hits in the MET wedge are *expected*. Here the alignment cut gives little rejection (×≈1-3, ESTIMATE). Lepton and τ vetoes, and the requirement of two oscillating, non-helical, non-monotonically separating tracks (S-7), must do the work.
  - In monojet-like selections W(ℓν)+jets with lost leptons is a sizeable fraction of the background (roughly a quarter to a third, UNVERIFIED, recalled).
- **Multijet with fake MET**: the MET is (anti-)parallel to a jet. Δφ(jet, MET) cleaning removes it, and must be applied before the alignment factor is counted.
- **Net:** ×13-34 per fake candidate for the PU/UE part. For the lost-lepton/τ part the gain is small and must come from vetoes and the trajectory hypothesis. The real factor can only be measured, e.g. in a low-MET control region or with simulated backgrounds. **Do not put ×13-34 into a background estimate.**

**Other caveats:**
- the cut constrains φ only;
- a lowered L1 MET threshold (STRAT P2) brings softer pairs, and δ₉₅ ∝ 1/p_T;
- the fake-plane probability may scale like a power of the hit density in the wedge, so ×13-34 may be conservative for PU fakes [R1 C-5 (ii)].

**Verdict: EXPLOIT** (as a selection and seeding road). Days. Confidence: high (geometry), low (gain on real backgrounds).

### S-6 Timing: medians, per-layer losses, multiple hits per layer
- **Statement.** The strategy's delays (BTL 6/16/33 ns) use the median γ* at a fixed p_T(QQ̄) = 250 GeV [STRAT §4.2, §10.4]. With the real falling p_T > 200 GeV spectrum the medians are **3.5/9.6/18.7 ns**; 6.2/16.5/32.8 ns are the 84th percentiles [T3 §6; S check 3 re-derived 3.48/9.52/18.71 ns from the same kinematic cache with a closed-form toa].
- **Per-layer losses** (fraction of pair-CM crossings outside ±12.5 ns):
  - 500 GeV: 2S1/2S2/2S3 = 7/17/33 %;
  - 1 TeV: PS3 27 %, 2S 44/57/68 %;
  - per hit, including repeated crossings: 2S 21 % (500 GeV) and 70 % (1 TeV).
- **Hits per layer.** Heavy, slow pairs give ≈ 3 hits per IT/PS layer at 1 TeV and 2.8-3.2 per layer at 500 GeV [T3 §6; T4 §6], not the "10-20 % of events" of [2002.07503 Tab.I] (X-11).
  - These counts are slightly *low*: `T3_causal.py` records one hit per chord and misses grazing double crossings within one step. An independent solver found 2-6 extra hits in 3 of 16 events [R1 C-1]. Fix: solve the quadratic for two roots per chord.
- **Oscillation-induced time spread** exceeds 1 ns only for Λ ≲ 0.5 keV.
- **BTL double hits** would measure the crossing period, i.e. ℓ₀ (S-4): WORTH A CHECK (TOFHIR capability UNVERIFIED).
- **Verdict: EXPLOIT** (correct STRAT and OQ Q11). Confidence high (exact kinematics; barrel |z| acceptances UNVERIFIED).

### S-7 Causal 9-parameter global fit, quirk-hypothesis χ² and two-regime seeding
- **Statement** [T4 §2, §5.2, §6].
  - Model: 9 parameters (z₀, P_QQ̄, γ*, CM axis, m_Q, Λ) plus MS kinks, against 50-130 measurements.
  - It is linear only within 2-10 % of an oscillation cycle at the last layer, with aliasing at 10 keV. So: no Kalman filter. Use a global Gauss-Newton fit with a phase-scan seed.
  - Seeding: resolved arcs for Λ ≲ 1 keV, an aliased zig-zag band through the PV for Λ ≳ 3 keV. The pair separation is non-monotonic in r in 98-100 % of events, a discriminant against helix pairs.
- **Predictive power (idealised upper bound).** An OT hit predicted from the IT has 15-55 µm (1σ) uncertainty, against strips 0.5-24 mm wide at 1-3 keV. That is at most ×20-100 rejection per OT layer at 1 keV, ×2-10 at 3 keV, and none at 10 keV.
  - The bound assumes known hit-to-quirk assignment, no PU hits, perfect alignment and a converged propagator.
  - Phase-2 OT alignment residuals of ≈ 10-30 µm (UNVERIFIED) are comparable to the prediction error and would roughly halve the per-layer factor.
  - PU-200 hit densities and wrong assignments reduce it further: expect an order of magnitude less overall until measured.
  - **Do not quote ×20-100 in a proposal as a background reduction** [R1-constructive B9].
- **ML-friendly features from the theory** [R1-constructive B6]: per-hit residual to the causal prediction, Δφ(MET, strip), the ℓ₀ estimate, hit-time delay vs R/c, plane normal vs MET, the non-monotonic pair separation, and hits per layer. These are physics-motivated and reduce the dependence of a GNN on its training truth.
- **Verdict: EXPLOIT** (design of the reconstruction approach). Weeks. Confidence medium.

### S-8 Stopped-pair delayed annihilation (and an ISR-triggered coincidence)
- **Statement.**
  - **Prior work (credit).** Evans-Luty [1811.08903] already did this for the E′ (1,1), SU(2)_IC benchmark, i.e. this project's benchmark:
    - they recast the CMS out-of-time search 1801.00359 (38.6 fb⁻¹; abstract, Sec.4);
    - they simulated quirk stopping in a CMS cylinder model (f_stop 1-5 % in |η| < 1 at 400 GeV, ≈ ×3 for |η| < 3, about as many again in the yoke [Fig.2, Fig.6]);
    - they computed the lifetime-dependent trigger fraction from the real 2016 fill schemes [Fig.3, Fig.4 right]: ≈ 8-10 % for 300-500 GeV E′ at Λ ≳ 300 eV, against 21 % for long delays;
    - they gave 300 fb⁻¹ projections [Fig.5 left]: naive extrapolation ≈ 0.15-0.2 TeV for Λ ≳ 300 eV; optimised (|η| < 3, zero background) ≈ 0.7-0.75 TeV up to Λ ~ 1 MeV (both R2's reading of the figure). Their current limit is negligible above Λ ≈ 0.15 keV;
    - they proposed higher energy thresholds, |η| < 3, the yoke, and HGCAL timing (which could raise the triggerable fraction of forward deposits to O(90 %)) [Sec.5];
    - they warned that 8b4e-type fill schemes would leave only the abort gap for a "≥ 2 BX away" trigger [Sec.6].
  - **What is new here** (modest): (i) f_stop from the *causal* string with T3's CMS geometry (1.0 ± 0.3 % EB+HB, at the low end of E-L); (ii) f_stop for the *triggered* (ISR) sample, which enables the coincidence below; (iii) an HL-LHC (3 ab⁻¹) projection with a background bracket; (iv) a Run-2+3 update estimate. The lifetime-dependent live fraction in F1 is a cruder re-derivation of E-L's calculation, and agrees with it.
  - **Delay.** The stopped pair dissipates its internal energy in ≈ 0.07-0.2 µs (range 0.02-0.5 µs) [T6 G-T6-4, `T6_stopping.py`]. For Λ ≳ 300 eV Evans-Luty's τ_stop for 500 GeV E′ peaks at ≈ 0.5 µs (≈ 0.1-5 µs). Their 0.1-100 µs span is the low-Λ terminal-velocity regime [1811.08903 Fig.4 left; R2-C4]. The pair then annihilates with ~2m_Q of 40-65 % visible energy [1811.08903 Eq.4.3].
  - T3 computed f_stop with the causal string for the first time:
    - inclusive pairs: **1.0 ± 0.3 % in EB+HB (|η| < 1)**, 6-9 % in any calorimeter, ≈ 10 % anywhere; flat for Λ = 0.3-3 keV;
    - triggered (p_T > 200 GeV) pairs: 0 % at 200-500 GeV, 1.3-2.5 % (fiducial) at 1 TeV;
    - ×2 model band; material UNVERIFIED [T3 §7].
- **Reach, revised** (answers R1-critical B-6) [F1: `F1_stopped.py`, `figures/F1_stopped_out.txt`]. v1 quoted ≈ 0.65 TeV assuming two things:
  - **(i) the 2016 live fraction of 21 %.** That holds only for delays much longer than the bunch-train structure. 1801.00359 triggers only in BXs at least two BXs away from any filled bunch [1801.00359 Sec.3] and folds in the lifetime with the fill pattern [Sec.3.2 Stage 3]. For a schematic 25 ns scheme (2592 bunches; UNVERIFIED stand-in), the effective live fraction is 0.027 at τ = 100 ns, 0.050 at 200 ns, 0.086 at 500 ns and 0.11 at 1 µs, against 0.21 for τ ≫ orbit. This is consistent with E-L's exact-fill result (≈ 2-3 % at 0.1 µs, ≈ 10 % at 0.5 µs [Fig.3]), which should be used instead. Filling schemes with frequent short gaps raise the acceptance at τ ≲ 0.5 µs; 8b4e-type schemes lower it [1811.08903 Sec.6];
  - **(ii) zero background.** The 2016 calorimeter search had 11.4 expected background events in 586 h of trigger livetime [1801.00359 Tab.4]. Scaled by livetime this is ≈ 230 events for 3 ab⁻¹ at the 2016 selection (ESTIMATE). A 2m_Q-scale energy threshold reduces it by an unknown factor; ATLAS saw zero events above a 300 GeV leading-jet energy at 8 TeV [as quoted in 1811.08903 Sec.5]. Also, for τ shorter than an orbit 1801.00359 searches only a 1.3τ window after each collision [Sec.8]. That scales the background to ≈ 15-45 % of the full-livetime value at τ = 0.1-0.5 µs, so the **B ≈ 230 column is ≈ ×2 pessimistic** [R2-C3]. The bracket B = 0/10/230 still contains the answer.
- Expected 95 % CL reach, E singlet, N_IC = 2, BR_vis 0.4-0.65:

| Scenario | B = 0, τ ≫ 1 µs (v1 assumption) | B = 0, τ = 0.1-0.5 µs | B = 10, τ = 0.1-0.5 µs | B ≈ 230 (2016 selection), τ = 0.5 µs |
|---|---|---|---|---|
| HL-LHC 3 ab⁻¹, EB+HB, f_stop 1 % | 0.61-0.67 TeV | 0.39-0.56 TeV | 0.30-0.45 TeV | 0.28-0.32 TeV |
| HL-LHC, full calorimeter, f_stop 7.5 % (endcap empty-BX trigger UNVERIFIED) | 0.89-0.97 TeV | 0.60-0.83 TeV | 0.48-0.69 TeV | 0.47-0.52 TeV |
| Run 2 + 3 (138 fb⁻¹ at 13 TeV + ~250 fb⁻¹ at 13.6 TeV), EB+HB 1 % | 0.38-0.42 TeV | 0.22-0.34 TeV | 0.17-0.26 TeV | 0.18-0.20 TeV (B ≈ 80) |

- **So the HL-LHC EB+HB reach is ≈ 0.3-0.55 TeV, not 0.65 TeV.**
  - The full-calorimeter version could reach 0.5-0.8 TeV.
  - HL-LHC vs E-L: our EB+HB numbers (0.3-0.55 TeV) sit between E-L's naive 300 fb⁻¹ projection and their optimised one. Our full-calorimeter B = 0 case (0.6-0.8 TeV at τ = 0.1-0.5 µs) is comparable to their optimised 300 fb⁻¹ curve (0.7-0.75 TeV), which uses their own trigger fractions.
  - **Run-2+3 update** with v2's own delay assumption (τ = 0.1-0.5 µs): ≈ 0.22-0.34 TeV at B = 0, 0.17-0.26 TeV at B = 10, ≈ 0.15-0.20 TeV at B ≈ 80, i.e. **≈ 0.15-0.35 TeV**. The 0.38-0.42 TeV column needs τ ≫ 1 µs and zero background. This is an *update of Evans-Luty's recast*, not a first limit: FASER (≤ 0.18 TeV for 0.3-100 keV) and D0 (≈ 0.11 TeV for 10 keV-1 MeV) already exclude the low end. It improves on them only if the background is reduced to O(10) events with an energy threshold (ESTIMATE; use 1801.00359's Stage-3 effective luminosity or E-L's trigger fractions, not this toy).
- **Value.** ISR- and tracker-free; covers Λ < 0.3 keV and plausibly Λ > 30 keV, where the coplanar search is blind. f_stop was computed at 0.3-3 keV (E-L checked flat to 10 keV). Above ~0.1 MeV, the ε-dependent in-flight annihilation of S-16 (3 cm-10 km) can pre-empt stopping, and de-excitation reaches ms at 1 MeV [1811.08903 App.B]. So the validity is "computed to 3 keV, plausibly to ≳ 100 keV" [R2-C7].
- **ISR + delayed-deposit coincidence** for triggered 1 TeV pairs (1.3-2.5 % stop in the barrel calorimeter 0.1-0.4 µs later): WORTH A CHECK (needs delayed readout).
- **Verdict: EXPLOIT** as a complementary analysis that covers the Λ edges, framed as an extension of Evans-Luty; **WORTH A CHECK** as a Run-2/3 update (§4.5). Weeks. Confidence medium-low (f_stop ×2, live fraction, background).

### S-9 Athena step-count killer
- **Statement.** `QuirksPreInclude` attaches `MonopoleLooperKiller` with MaxSteps = 2×10⁶ (BSM_Only). The quirk stepper takes ≈ 150-200 G4 steps per crossing (ESTIMATE), and N_cross ≈ 24 (Λ/keV)² in a CMS-size tracker. So a naive port kills quirks inside the tracker for Λ ≳ 24 keV [T2 G-T2-2].
- **Status.** SREQ W1 (v) already requires an exemption from looper killers; this entry quantifies why. For FASER (≈ 10⁵ crossings at 100 keV) the impact is possible but UNVERIFIED.
- **Verdict: EXPLOIT** (configuration), hours, **do first**. Confidence medium. This is a configuration note, not a finding about CMS physics [R1 C-8].

### S-10 The merged pair is a 9-21× MIP object, not 2× MIP
- **Statement.** "≥ 2× MIP" comes from FASER (relativistic pairs) [2607.26195] and D0. For the central p_T > 200 GeV sample the merged pair (Λ ≳ 30 keV) deposits a median 9× MIP (500 GeV) and 21× MIP (1 TeV). That is 1.5-1.8× one HSCP at the same β, and 0.75-0.9 of two HSCPs at β_cm [T3 §8; R1 order-of-magnitude check PASS].
- **Exploitation.** An HSCP-like high-Λ category (IT ToT, MTD 1/β, OT HIP bit). It is distinguishable from |q| = 2 (4× at the same β) only with β.
  - A CMS HSCP recast [2410.09164] needs care: the merged pair is net neutral, so its "track" is straight (no curvature, p_T measurement at the resolution limit), and strip cluster cleaning may reject partially merged pairs (§4.5).
- **Caveat.** IT ToT saturation (UNVERIFIED range).
- **Verdict: EXPLOIT** (strategy correction); **WORTH A CHECK** (recast). Days. Confidence medium.

### S-11 Λ conventions and closed-form kinematics (documentation)
- See boxes A and B; the numbers are [T1 G-T1-1; T5 G-T5-4; T2 §2.2, §3].
- Additions in v2:
  - scalar Ẽ: ℓ_max ×1.70-1.73, N_osc ×0.81;
  - N_IC = 3 numbers;
  - a k-string caveat for non-fundamental representations.
- **Verdict: EXPLOIT**, hours, high confidence.

### S-12 Mean energy loss is a first-order trajectory effect
- **Statement.** The mean ionisation loss drifts the oscillation phase. That shifts OT hits by 40-180 µm (200-500 GeV) and 0.3-1.5 mm (1 TeV) [T4 §2.3, G-T4-7]. A 10 % material error moves OT hits by 4-150 µm.
- **Exploitation.** (e, c) The material scale is a fit nuisance and a signal-efficiency systematic for any χ²/GNN using OT positions. As a mass handle it is limited to the material precision (≈ 10 %).
- **Verdict: WORTH A CHECK.** Days. Confidence medium (thin-scatterer Bethe; material UNVERIFIED).

### S-13 Production modelling of the ISR tail
- **Statement.** The MET trigger selects the p_T(QQ̄) tail.
  - A fixed-p_T ISR kick biases ℓ_max by −10 to −25 % and N_osc by +20 % [T2 §3].
  - Two groups differ by 37 % in mass reach on the same benchmark, largely from ISR/K-factor handling [T5 I2].
  - FASER needed an ISR reweighting [2607.26195 p.3].
- **Status.** STRAT §12 already plans LO-MLM vs NLO-FxFx and ISR variations. Add: generate with a V+jet matrix element, never a fixed-p_T kick (fast scans included).
- **Verdict: EXPLOIT** (already planned). Confidence high.

### S-14 GUT-ladder Λ strip and the invisibility of doublets
- **Statement.**
  - The only UV framework that lands Λ in the CMS window is the SUSY-GUT ladder (box A) [T1 G-T1-2]. Its EW quirks are doublets L plus coloured D; a singlet E spoils unification (1-loop).
  - Doublet charged members decay with cτ = 7.8 mm, so the pair is neutral before the first pixel layer (survival to 3 cm ≤ 0.2 % at 200 GeV) [T6 G-T6-2; T3 §5; S check 7; R1 check 12 PASS].
  - For a member bound by the string the free decay rate applies in its rest frame: ΔM is pure EW and acceleration effects are ~σ/m ≪ ΔM [R1 §5].
- **Consequence.** The theory-favoured representation gives a monojet + soft displaced pions signature, not a coplanar pair, at ×14 the E rate (84 fb at 500 GeV, N_IC = 2).
- **Exploitation.**
  - Draw the ladder lines (labelled as doublet motivation).
  - A compressed-higgsino-style monojet recast with ×2N_IC rate (§4.5). Limits not opened (UNVERIFIED).
  - Drop the "2 L points as tracker topology test" (OQ Q4) or replace them with this recast.
- **Coloured quirks** (contrast, R1-constructive C): (3,1)_{2/3} quirks have ×10-100 larger rates and are the target of the existing Knapen/Li reach (≈ 2.1 TeV for fermions [T5]) and of ATLAS. The string physics of S-1 to S-3 applies unchanged; hadronisation and spin-down differ. This supports the CMS singlet choice as complementary.
- **Verdict: EXPLOIT** (lines, motivation text); **WORTH A CHECK** (recast). Days.

### S-15 Cosmology: a discovery implies a reheating bound
- **Statement** [T1 G-T1-4].
  - If the IC sector ever thermalised, the whole window is excluded: Ω_G h² ≈ 2-10 (√σ/keV) and ΔN_eff(BBN) = 0.21 (SU(2)), 0.57 (SU(3)).
  - With UV freeze-in, a discovery implies T_max ≲ m_Q/25 and **T_RH ≲ 5-40 GeV for 0.2-1 TeV** (T1's table reaches 64 GeV at 1 TeV and 1 keV, capped by m_Q/25 = 40 GeV; the SIDM-like bound gives 4.7-31 GeV) [R1 C-6].
  - Glueballs are absolutely stable in the window.
  - The abundance scales as T_RH^{21/4} (numerically T^5.0 with g*s), not T⁷, once the frozen-in gluons self-thermalise (confirmed analytically [S; R1 §4]).
  - T1 differs from 2512.20696 Fig.4 by ×2.2 in T_RH,max. That is not checkable without their code; a g*s dilution is the more plausible explanation [R1 C-6]. Do not claim an error until resolved with the authors.
- **Exploitation.** (a) An "implication" contour; (f) a modest note (contact the authors first).
- **Verdict: EXPLOIT** (figure, text); **WORTH A CHECK** (note). Confidence medium.

### S-16 Microscopic complement: Λ ≳ 3 MeV and the 0.1-3 MeV displaced band
- **Statement** [T6 G-T6-5].
  - For Λ ≳ 3 MeV the pair annihilates before the first layer, with σ × BR(ℓℓ) = 1.1 fb at m_Q = 500 GeV.
  - ATLAS dilepton limits (≈ 0.05-0.1 fb at 1.4-2 TeV; reading UNVERIFIED) probably exclude m_Q ≲ 0.8-1 TeV. **This is a reading of an existing limit, not a derived exclusion.**
  - Λ ≈ 0.1-3 MeV: displaced annihilation at 3 cm-10 km depending on ε (a guess). No search covers it.
- **Exploitation.** (a) Scoping: the CMS tracker search should not claim Λ ≳ 1 MeV. (b) A candidate new search, dependent on ε (S-19).
- **Verdict: EXPLOIT** (scoping); **WORTH A CHECK** (band). Confidence low.

### S-17 Multi-charged singlets |q| = 2
- **Statement.** σ ∝ q² exactly, plus γγ +18-21 %. The tracker reach would be ≈ 1.3 TeV, against ≈ 1.15 TeV for |q| = 1 [T6 G-T6-3]. ATLAS multi-charge limits (1060 GeV for |q| = 2 [2303.13613]) need a highly ionising, nearly helical track; applicability to quirks is UNVERIFIED.
- **Correction.** With the causal scaling (thickness ∝ qB/Λ^~1.9) Λ_low rises by ≈ 2^{1/1.9} ≈ 1.4, not 2^{1/4}: ≈ 0.65 keV at 500 GeV (ESTIMATE, truth level). The MS floor doubles (Highland ∝ |q|) to ≈ 22-44 µm. dE/dx is ×4.
- **Verdict: WORTH A CHECK** (cheap sample). Confidence medium.

### S-18 Trigger, PU-200, PU-vertex association and HLT realism (experimental; theory inputs only)
- **L1:** only 23-47 % of quirk OT crossings form 2 GeV stubs at Λ ≤ 3 keV (76-89 % at 10 keV), and they do not form consistent helices. Quirks are largely invisible to L1 tracking [T4 §5.3, §6]. The trigger is L1 MET (p_T(QQ̄) ≳ 200 GeV), which is what S-5 and S-13 depend on. A φ-road cluster-pair multiplicity aligned with L1 MET φ is an L1-scouting idea (feasibility not assessed).
- **PU 200** has never been simulated for a quirk tracker analysis [T5 G-T5-3].
- **PU-vertex association** (new note, not studied; R1-constructive B3).
  - The plane fit has a free z₀ [T4 §2]. Its precision from the IT alone is of order 30-60 µm (pixel σ_z ≈ 29 µm at r = 3 cm; MS in the beam pipe negligible at p ~ 0.3-0.5 TeV) (ESTIMATE).
  - The HL-LHC luminous region (σ_z ≈ 4-5 cm, UNVERIFIED) with 200 vertices gives ≈ 18 vertices/cm near z = 0. So a ±100 µm window around the plane's z₀ contains another PU vertex in ≈ 30 % of events.
  - This is not an ambiguity for the signal: the hard-scatter vertex is defined by the ≥ 200 GeV ISR jet, and the plane must point to it. It is a **background handle**: fake planes built from PU tracks point to their own vertex.
  - The MTD time of the hard-scatter vertex comes from the ISR-jet tracks. The quirk hits are late by 1-18 ns (S-6), so their own times cannot be used for vertex association; they are a signal feature.
- **HLT and other trigger paths** (not studied; UNVERIFIED without CMS-internal information):

| Path | Quirk subset | Works? | Reason |
|---|---|---|---|
| L1 MET / HLT MET, MHT (monojet-like) | all, through the ISR jet | yes (baseline) | p_T(QQ̄) recoil; sets the p_T > 200 GeV spectrum |
| L1 track trigger | 0.3-10 keV | no | 23-47 % stubs, no helix (S-18) |
| HSCP / high-dE/dx | merged pairs (Λ ≳ 20-30 keV) | maybe | needs a reconstructed track: the merged pair is net neutral and straight (S-10) |
| Disappearing track | doublets/triplets | no (doublets), marginal (Y = 0 triplets ≲ 300 GeV) | doublets decay inside the beam pipe; quirk tracks are not helical |
| Displaced / delayed jets, ECAL timing | — | no | quirks deposit little calorimeter energy in flight |
| Empty-BX calorimeter (stopped particles) | stopped pairs | yes | S-8; the endcap trigger at HL-LHC is UNVERIFIED |
| MTD-delayed track segment aligned with MET φ (HLT idea) | 0.3-10 keV | idea | T4 §5.3 item 3 |

- **Verdict: WORTH A CHECK** (experimental track; months).

### S-19 ε (glueball emission per crossing) depends on the miss distance
- ε = 0.1 per crossing has no derivation. Emission needs b < 1/Λ [1811.08903 App.B.1]. In 3.8 T this applies to none of the crossings for Λ ≲ 2 keV, the even crossings for 3-20 keV, and all crossings above ≈ 30 keV [T2 §6.3]. ε is irrelevant for the CMS tracker (≲ 0.1 GeV).
- An ε(b) parametrisation could relax FASER's 30-100 keV limits; that needs the J random walk in rock.
- **WORTH A CHECK**, low priority for CMS.

### S-20 Exclusive γγ → QQ̄ with PPS as a mass handle
- σ_excl = 0.012 fb at 500 GeV, i.e. ≈ 35 produced events with PPS-2 acceptance [T6 G-T6-1]. Combined with γ* from the trajectory it gives m_Q independently of the MET scale.
- PPS-2 schedule and trigger: UNVERIFIED.
- Inelastic γγ is +4.0-4.2 % of the K-corrected DY (|q| = 1).
- **WORTH A CHECK** (post-discovery only).

---
## 2. Cross-report tensions, resolved (X-n; "T-n" in v1)

### X-1 "Precession is not a Λ meter" [T3] vs "the in-plane B displacement is a recoil-free Λ meter" [T4]
**Resolution: different observables; the reports agree.**
- T3 killed the *secular rigid rotation* of the fitted plane: 3-18 µrad at 0.6-1 keV, ≤ 0.3 µrad at ≥ 3 keV, below the MS-induced 4.5-10 µrad [T3 §4.2]. Canonical-momentum conservation bounds the CM wobble [T3 §4.1].
- T4 uses the *whole non-rigid B displacement pattern*, x_B ≈ 0.5 ε_B R ≈ 120 µm at 2S3 for 1 keV, profiled inside a 9-parameter fit [T4 §3.2].
- Both B routes work for Λ ≲ 1.5-2 keV. Scalings agree: ∝ ε_B = qB/σ, Λ^−1.6…−2.0, m_Q independent.
- T2's Λ^−2.5 at 2-5 keV (4 events, fixed kinematics, causal column at max_boost 10⁻² differing from the converged causal by up to 25 % [F1: `F1_standin.py`]) is retired [R1 B-8].
- Caveat: the B route assumes the causal model at the crossings (independently confirmed at 1 keV, S-3) and a known charge q.

### X-2 B-field thickness: causal Λ^−1.6…−2.0 vs the m_Q/Λ⁴ formula [1911.02223 Eq.III.12]
**Resolution: the causal numerics are right for the plane-fit thickness. The formula describes a different quantity, the odd-crossing miss distance, and first-order perturbation theory fails at the crossings.**
- The formula's m_Q/Λ⁴ is the static polarisation of the yo-yo by E* = γβ×B: offset ≈ qE*ℓ/σ ∝ qBm_Q/σ². In the exact dynamics this is the odd-crossing miss distance b ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] (Li's d_E [2002.07503 Eq.V.8]).
- The plane-fit thickness is dominated by transverse impulses at the near-miss crossings, ∝ (σb/v) ln(ℓ/b), i.e. ∝ ε_B with a logarithm (X-3).
- The two coincide near Λ ≈ 1 keV and diverge above: ×7-50 at 3 keV, ×100+ at 10 keV [T3 §3.2].
- **Li et al. already showed** that their numerical thickness scatters by 10⁻³-10³ around the formula [2002.07503 App.C, Fig.8], and their reach uses the numerical thickness. What is new here is the scaling, its m_Q independence and its crossing origin.
- **Practical consequences:** the window edge moves little (0.45-0.7 vs 0.54-0.81 keV, truth level). Above ~2 keV any use of the formula in this project (STRAT §4.2, §5 O1, §9.1, §9.4 V2) is wrong by large factors. The realistic thickness is MS dominated anyway.
- **Is the formula "from the straight-string treatment"?** It is from linearising the straight-string EoM about the vacuum yo-yo. The converged Li straight string itself gives thicknesses within ≈ 3-35 % of the causal string, depending on γ* (S-1). So the failure is in the *perturbative expansion* at the crossings, not in the straight-string ansatz as implemented by Li et al.

### X-3 "The causal string is non-linear in B, 30-45 % beyond first order; numerical artefact not excluded" [T4 G-T4-4]
**Resolution: confirmed, by the T4 kernel (S) and by an independent conformal-gauge NG solver (R1). Generated at the crossings, consistent with B ln(1/B).**
- S (T4 kernel):
  - the metric Q68|d(B) − 20 d(B/20)|/Q68|d(B)| is 0.31-0.35 (PS, 2S) at 1 keV;
  - converged to < 1 % between max_boost 10⁻² and 10⁻³;
  - steep and near-tangent crossings show the same effect;
  - the response is exactly linear (ratio 1.000) for every hit before the first crossing;
  - the response per unit B is 1.15-1.19 / 1.32-1.38 / 1.45-1.51 / 1.83 at B/4, B/20, B/80, B/1000, consistent with 1 + (0.10-0.12) ln(B₀/B) [S: `S_Bnonlin.py`, `S_Bscan.py`].
  - At 3 keV the converged value for steep crossings is 0.27-0.34. T4's 0.36-0.65 at max_boost 10⁻² was inflated by the kernel's numerical floor.
- R1 (independent solver, 3 events, 1 keV, 500 GeV): pre-crossing metric 2×10⁻⁴-2×10⁻²; post-crossing 0.13-0.14 (k = 4) and 0.29-0.39 (k = 20); response ×1.14 and ×1.31, i.e. 1 + 0.10 ln(B₀/B) [R1: `R1_Blinearity.py`].
- The old caveat "the same algorithm in all ports" is now **closed** for B at 0.6-3 keV. Still open: an analytic derivation of the coefficient (S-3), and the Athena C++ itself.
- Practical conclusion: the fit and any fast model must run the full causal propagator. "Vacuum + first-order B" is not a controlled model.

### X-4 Λ convention: T1 (0.709), T5 (0.71, 15 %) vs theory_signal_model (1/0.6)
- T1 and T5 agree: T_c/√σ = 0.709 (SU(2)) [hep-lat/0307017 Tab.6; Teper 0912.3339 Eq.33].
- "15 %" is the error on Λ when 1/0.6 is used instead of 1/0.709; "18 %" is the same statement inverted; "28 %" is the error on σ.
- The 0.6 of 2512.20696 is the N → ∞ value.
- **Effect:** T_RH,max ∝ Λ^−0.21, so ≤ 4 % on cosmology; it matters only for overlays.

### X-5 Stopped-pair yields: f_stop 1-6 % [T6] vs 1.0 ± 0.3 % [T3]
- Different fiducial definitions; an assumed vs a computed number. T6 took Evans-Luty's 1-5 % (|η| < 1, 400 GeV) ×3 for the full calorimeter. T3 computed EB+HB 1.0 ± 0.3 %, any calorimeter 6-9 %.
- The **reach** is revised in S-8: lifetime-dependent live fraction, non-zero background.

### X-6 Timing: T3 medians vs strategy 16/33 ns
- The strategy's numbers are right for its assumption (fixed p_T = 250 GeV, median γ*). The triggered spectrum gives medians of 3.5/9.6/18.7 ns.
- Per-hit losses exceed per-pair losses, and a lower L1 MET threshold adds slower pairs.
- The digitiser quantity is t − R cosh η/c (STRAT C8); S's first attempt with t − R/c was wrong and was corrected.

### X-7 Multiple scattering: 50-400 µm [T5] vs 11-22 µm [T3]
- T3 supersedes T5's explicit upper bound. Three effects reduce it ×5-20: the plane fit, the sharing of the kick within the pair, and the string's restoring dynamics.
- Both are truth level (S-2).

### X-8 Λ measurement from crossing period / BTL double hits [T2, T3] vs the degeneracy theorem [T4]
- T4 is right: crossing spacing, period, amplitude and width measure ℓ₀ and velocities, never Λ alone. "Direct Λ measurement" in T3 §6 should read "direct ℓ₀ measurement".

### X-9 GUT-favoured Λ [T1] vs tracker visibility [T3, T6]
- A real tension in the motivation, not in the physics. The GUT ladder predicts doublets (+ coloured D), which leave no tracker trajectory. The E coplanar search is generic-hidden-sector motivated. The ladder motivates the monojet recast (S-14).

### X-10 |q| = 2 window [T6] vs causal thickness scaling [T3]
- Λ_low rises by ≈ 1.4, not 1.19 (S-17).

### X-11 Hits per layer: "10-20 % of events with > 2 hits" [STRAT §4.2 from 2002.07503 Tab.I] vs ≈ 3 hits per layer [T3, T4]
- Li et al.'s fraction is for lighter, faster pairs. For m_Q ≥ 500 GeV and Λ ≥ 1 keV the radial internal motion exceeds β_T ≈ 0.1-0.16, so 2.8-3.2 hits per layer is the norm (slightly more with the double-crossing fix, S-6).

### X-12 MET-alignment factor: ×5-10 [T5] vs ×13-34 [T4]
- T5 used generic windows; T4 computed the 95 % window. Use T4, against random planes only (S-5).

### X-13 Straight string "good to 1-4 %" [TH §3.1] vs "uncontrolled at O(F_ext)" [T2, T3] vs R1
**Resolution (revised in v2):**
- TH's 1-4 % bounds the bending angles, not the observables, which are themselves O(F_ext/σ) [T2 §5.1 "order counting"]. That argument is right in principle: a straight-string *ansatz* is not guaranteed to be accurate at O(F_ext/σ).
- But the size of the error depends on the prescription:
  - converged, CM-simultaneous (Li): −3 % (γ* ≈ 1.05), −15 % (γ* ≈ 1.3), −30…−35 % median at γ* = 2-3, with per-event spreads up to ±50 %;
  - lab-time slices (labSS): ×1.5-75, median ≈ 9;
  - Li at its printed step: ×0.8-20, an integration error.
- So TH's "few % in the core window" understates the Li-method error (3-35 %, γ*-dependent), and v1's "×0.04-60 for published codes" overstated it. **The causal string is the reference and the comparison is superseded, not a systematic** (§4.1, §12 row).
- **NG validity** (R1 B-1): "exact" means exact *classical* NG with point endpoints. At near-miss crossings with b < 1/Λ (even crossings from Λ ≈ 3 keV, odd ones from ≈ 20 keV) the effective string description is cut off at an uncontrolled scale. This is a ≲ 10-30 % uncertainty on Δs_B for Λ ≳ 10-20 keV (ESTIMATE), and negligible where Δs_B matters (Λ ≲ 3 keV).
- References for the piecewise-null construction: the Artru/Lund string literature (Artru 1974/1983; Andersson et al. 1983; UNVERIFIED as cited, not opened). The Athena implementation is a known construction, not an ATLAS invention [R1 C-9].

---
## 3. Spot checks of headline numbers

### 3.0 What the checks did and did not test (answers R1-critical A-3)
- v1 announced "35/35 PASS". That count was 30 assertions inside `S_spotchecks.py` (sections A-H) plus rows 10-14 below.
- **By type**, the 14 v1 rows were:
  - 7 independent closed-form or new-formula re-derivations (rows 1, 3, 4, 5, 7, 8, 13);
  - 4 runs of the *same* code on new samples or settings (rows 2, 9, 10, 12);
  - 3 re-runs or ratios of investigator outputs (rows 6, 11, 14).
- **What they did not test:** no row compared a *published* integrator, or an *independent* string solver, with the causal string. The premise of the v1 top-ranked gap (S-1: "the stand-in labSS represents Li et al.") was never checked. Under R1 it failed.
- v2 adds the missing tests:
  - the literal Li integrator vs labSS on T2's own events (row 15);
  - the Li phase drift (row 16);
  - R1's independent NG solver and B-linearity runs (rows 17-19);
  - resolution smearing (row 20);
  - stopped-pair live fraction and background (row 21).
- **Still untested:**
  - the Athena C++ itself;
  - the Knapen-Papucci code;
  - the Phase-2 material;
  - anything with PU;
  - the analytic coefficient of the B ln B term.

### 3.1 Table

| # | Number checked (source) | Method | Command | Result | Verdict |
|---|---|---|---|---|---|
| 1 | σ = 50.68 GeV/cm (Λ/keV)²; ℓ_max coefficient 3.947 cm [T2 §2.2] | closed form + ExactPair | `S_spotchecks.py 0` (A) | 50.68; 3.947; ratio 1.0000 | PASS (indep.) |
| 2 | N_osc ≈ 12 (Λ/keV)² [T2] | σR/(2β*p_T) on the T2 cache | same (B) | 12.1/11.6/11.9 | PASS (same cache) |
| 3 | BTL medians 3.5/9.6/18.7 ns [T3 §6] | closed-form toa on the same cache | same (C) | 3.48/9.52/18.71; 84th: 6.2/16.5/32.8 | PASS (indep. formula; same cache) |
| 4 | ΔN_eff = 0.21/0.57 [T1] | (4/7) g_d ξ⁴ | same (D) | 0.2135/0.5692 | PASS (indep.) |
| 5 | T_c/√σ = 0.709/0.646; "1 keV T_c" = 1.41 keV √σ [T1, T5] | Teper fit | same (E) | 0.7095/0.647/1.41 | PASS (indep.) |
| 6 | γγ/DY [T6] | ratio of T6 table | same (F) | 4.0-4.2 % of K-corrected DY | PASS (re-derived ratio) |
| 7 | doublet cτ = 7.9 mm [T6] | closed form | same (F) | 7.8 mm (R1: 7-8 mm) | PASS (indep.) |
| 8 | STRAT Λ_low = 0.54/0.69/0.81 keV [STRAT §4.4] | invert the formula | same (G) | 0.545/0.685/0.815 | PASS (but the formula is not the physical thickness, X-2) |
| 9 | Δs at 3 keV: M = 17/24 µm etc. [T3 §3.2] | causal, new seed, 30 events | `S_spotchecks.py 30` (H) | M 17.6/18.2; B+M 14.4/23.8 | **consistent within MC statistics (±25 %)**, same code [R1 C-3] |
| 10 | Δs ∝ √(x/X0) [T3] | material ×0.25-×4, same code | `S_msscale.py 40 500 3` | exponent 0.517 | PASS as a scaling of the code; the material is UNVERIFIED |
| 11 | MET alignment ×13-34 [T4] | re-run + π/(1.96σ⊥/p_T) | `T4_met.py` | ×12.7-34.3; ≈ 19 | PASS (geometry vs random planes only) |
| 12 | Non-linear B response [T4] | T4 kernel, step and crossing tests | `S_Bnonlin.py`, `S_Bscan.py` | 31-35 %, linear before the 1st crossing | PASS (same algorithm; see row 18) |
| 13 | Ω ∝ T_RH^5 not T⁷ [T1] | analytic | by hand | T^{21/4} | PASS (indep.; R1 agrees) |
| 14 | T_RH,max table [T1] | re-run | `T1_cosmo.py` | identical | PASS (re-run only) |
| **15** | **"labSS ≈ Li et al."** (v1 S-1) on T2's own events | literal Li (R1 kernel) at ×1/×0.01/×0.003 of Eq.III.10 vs causal vs T2's stored labSS | `pixi run python code/F1_standin.py` | Li/causal 0.84-1.05; labSS/causal 1.5-75; **labSS/Li 1.6-73** (0/12 within ±50 %) | **FAIL** for the v1 premise (labSS is not a stand-in) |
| **16** | Residual mm hit differences of converged Li at 2 keV [R1] | Li ×0.003 vs ×0.001 vs causal; decomposition into in-plane / out-of-plane; crossing log | `pixi run python code/F1_li_phase.py 2 0,1,2,3,4,5 0.003,0.001` | max \|Δhit\| 0.2-9.8 mm (×0.003) → 0.07-0.53 mm (×0.001), median 5.5-18 µm; in-plane phase drift; out-of-plane ≤ 10.5 µm; thickness 0.85-1.05 | Li step non-convergence (PASS for "Li ≈ causal when converged") |
| 17 | Causal port = exact NG [T2, S-1] | independent conformal-gauge NG solver, 16 events | `R1_conformal_ng.py` | 0.990-1.004; ≤ 0.4 µm out of plane | PASS (indep., R1) |
| 18 | B ln B non-linearity [T4, S] | conformal solver, B/4, B/20 | `R1_Blinearity.py` | 0.29-0.39 (k = 20); 1 + 0.10 ln | PASS (indep., R1) |
| 19 | "Straight string + MS gives fake mm thickness" [T3 §3.1] | Li + thin-scatterer MS vs causal + MS | `R1_li_ms.py` | 12-15 µm vs 15-30 µm medians | FAIL (holds for labSS only) |
| **20** | "Δs < 100 µm passes 93-100 %" is measurable [T3 §9] | causal B+M events, Phase-2 pitches, weighted plane fit | `pixi run python code/F1_smear.py 60` | per-hit σ_n: IT ≈ 17 µm, PS ≈ 0.25 mm, 2S ≈ 8 mm; event s_eff 23-30 µm; f(t_est < 100 µm) 0.60-0.73 at 0.3-0.45 keV vs truth 0.13-0.42 (S-2) | truth-level numbers do **not** transfer; the test is IT dominated |
| **21** | Stopped-pair reach 0.65 TeV [T6, v1 S-8] | lifetime-dependent empty-BX live fraction, CLs with B = 0/10/230 | `pixi run python code/F1_stopped.py` | 0.3-0.55 TeV (EB+HB, τ = 0.1-0.5 µs) | v1 number was an upper estimate (B-6) |
| **22** | "Li ≈ 15 % low" holds beyond γ* = 1.28 (v2 S-1) | literal Li vs causal at γ* = 1.05/1.28/1.6/2/3, Λ = 1 keV, 5 events each, converged steps | `pixi run python code/R2_li_checks.py gamma` (R2) | medians 0.97/0.85/0.92/0.69/0.65; single events 0.53-1.36 at γ* ≥ 2; out-of-plane Δhit up to 124 µm | **FAIL** as a general statement: the deficit depends on γ* (indep., R2) |
| **23** | 3 keV Li not converged (v2 S-1, §7) | Li ×0.001 on R1's 3 keV events | `R2_li_checks.py fine` (R2) | 0.855/0.856 (2 events), 0.67 (hit-count mismatch) | converged at ×10⁻³; deficit Λ-independent (indep., R2) |

Rows 22-23 were added in v3 from R2's independent runs.

**Counts (v2):**
- independent closed-form or independent-code checks: rows 1, 3-5, 7, 8, 13, 15-19 (12);
- same code on new samples or settings: rows 2, 9, 10, 12, 20 (5);
- re-runs or ratios: rows 6, 11, 14 (3);
- new-model estimates: row 21.
- Two v1 premises **fail** (rows 15, 19). Everything else passes, with the caveats stated.
- The f_stop numbers (T3 §7) were not re-run by anyone (hours of CPU).

---
## 4. Implications for the experimental track (recommendations only; no file outside `theory_track/` was edited)

Severity:
- **must**: changes a decision or a number used downstream;
- **should**: improves correctness;
- **wording**.

Read first:
- T3 §3.2 table and `figures/T3_ms_thickness.png` (thickness);
- T3 §6 and `figures/T3_timing.png` (timing);
- T4 §4.3 (measurement);
- this document, S-1 and S-2.

### 4.1 `phase1_strategy/outputs/STRATEGY_DRAFT.md`
| Section | Current text | Recommended change | Severity | Source |
|---|---|---|---|---|
| §1 item 3; §10.4 OI-1 "Facts" | "median delay at the BTL ≈ 16 ns (500 GeV), ≈ 33 ns (1 TeV)" | Medians 3.5/9.6/18.7 ns; 16.5/33 ns are the 84th percentiles. Per-layer fractions outside ±12.5 ns: 500 GeV 2S 7/17/33 %; 1 TeV PS3 27 %, 2S 44/57/68 %. Per hit: 2S 21 % / 70 % | must | S-6 |
| §4.2 bullet 1 | "Straight-string EoM … good to ≲ 1-4 %" | "Causal Nambu-Goto string (Athena algorithm; `T3_causal.py`, validated against an independent NG solver to ≤ 1 %). Never use lab-time-slice straight strings. A CM-simultaneous (Li-type) straight string is within 3-35 % on Δs (γ*-dependent; ±50 % per event at γ* ≳ 2) only when step-converged (≲ 10⁻²-10⁻³ × its printed bound)" | must | S-1 |
| §4.2 bullet 3; §4.4 lower edge; §5 O1 | thickness d ∝ m_Q/Λ⁴ (formula); Λ_low ∝ m_Q^{1/4} | Causal B thickness 32-38 µm at 1 keV, ∝ Λ^−1.6…−2.0, ~m_Q independent; MS floor 11/15/22 µm (truth level). Λ_low(50 %, truth) ≈ 0.45-0.7 keV; plateau from ≈ 1 keV (200-500 GeV), ≈ 2 keV (1 TeV). With realistic resolution the truth-level edge does not transfer; it must be re-derived with the real finder at fixed background efficiency (S-2). Credit 2002.07503 App.C for the formula's order-of-magnitude status | must | S-2, S-3 |
| §4.2 "10-20 % of events have > 2 hits per layer" | — | ≈ 3 hits per IT/PS layer for heavy pairs; accept 3-4 | must | X-11, S-6 |
| §4.2 "1-5 % stop in the calorimeters" | — | 1.0 ± 0.3 % (EB+HB, inclusive), 6-9 % any calorimeter; 0 % for triggered 200-500 GeV pairs; 1.3-2.5 % for triggered 1 TeV pairs | should | S-8 |
| §4.3 regime map; §9.1 "High-Λ category … ≥ 2× MIP" | "≥ 2× MIP" | Median 9× (500 GeV) to 21× (1 TeV) MIP for the central triggered sample | must | S-10 |
| §5 O6 | "fit … measures (m_Q, Λ)" | Hits/time/dE/dx measure ℓ₀ and velocities only. m_Q from the MET recoil: ≈ 1-3 % (m_Q), 0.5-1.5 % (Λ) for 30 events, MET-scale limited (statistical CRB 1 %/0.5 %; local, known assignment, no PU). B route only for Λ ≲ 2 keV | must | S-4 |
| §5 O7 | MET-plane alignment, no number | \|Δφ(MET, strip)\| < 0.15-0.25 rad: 95 % signal, ×13-34 rejection of *random* planes per candidate. The gain on the real background (Z(νν), lost-lepton/τ W, PU) is unknown and must be measured. Δφ(jet, MET) cleaning first. Seeding wedge = same wedge (do not multiply) | must | S-5 |
| §9.1 trajectory fit | "fit the straight-string EoM … analytic first-order solution as a fast seed" | Global Gauss-Newton fit with the full causal propagator (B and mean dE/dx inside; MS as kinks); vacuum closed form only as the IT seed; phase scan; no Kalman filter. SBI as the eventual full inference | should | S-7, S-4 |
| §9.1 plane finder | "require ≥ 2 hits in ≥ N_min layers"; "Δs scanned per Λ since d ∝ m_Q/Λ⁴" | Resolution-aware coplanarity: per-hit out-of-plane resolution IT ≈ 17 µm, PS ≈ 0.25 mm, 2S ≈ 8 mm (n_z-dependent); event-level ≈ 23-30 µm. Fit with weights 1/σ_n², test χ² or t_est; do not use truth-level Δs cut values. Accept 3-4 hits per layer | must | S-2 |
| §9.2 GNN training | "signal from the full CMS simulation" | Causal-string + material samples. The Zenodo 17941765 / Sha et al. trajectories have no material (MS floor absent: certain) and an unknown string prescription and step: **validate them against `T3_causal.py` before using them as truth** (thickness ratio, OT residuals) | must | S-1, S-2 |
| §9.4 V2 | "plane thickness vs the formula, within ×10" | Remove. A correct propagator fails it at Λ ≳ 3 keV (×7-50), as Li et al. already show [2002.07503 App.C]. Replace by the causal-thickness table (with/without material) | must | X-2 |
| §9.4 V3 | "causal vs straight-string integrator with correct ŝ simultaneity" | Keep as a cross-check, compared event by event in bins of γ*: a converged Li-type integrator gives Δs/causal ≈ 0.97 (γ* ≈ 1.05), ≈ 0.85 (1.3), 0.5-1.4 per event (γ* ≳ 2), with sub-mm OT residuals at ≤ 1 keV. Do not use a single ratio as a pass/fail target. Real validation: (i) vacuum vs ExactPair (≤ 10⁻⁸ ℓ_max); (ii) covariance test; (iii) canonical momentum conservation; (iv) comparison with `T3_causal.py` and with R1's conformal solver (B, material) | should | S-1 |
| §9.4 V4 | "≈ 2-MIP charge for merged pairs" | FASER-specific; at CMS expect 9-21× MIP | must | S-10 |
| §9.4 V5 | Zenodo trajectories comparison | Expect (i) the missing MS floor (11-22 µm) and (ii) γ*-dependent thickness differences (3-35 % median; up to ±50 % per event at γ* ≳ 2) if the code is CM-simultaneous and converged. mm-scale OT differences would indicate an unconverged integration or a lab-time-slice prescription | must | S-1 |
| §7 A2 L doublet "2 topology points" | — | Doublet pairs are neutral before the first pixel layer (cτ = 7.8 mm). Drop as a tracker benchmark; replace by the monojet recast | should | S-14 |
| §12 Signal shape (i) | "Athena causal vs straight-string … few %" | The quirk-dynamics systematic is: causal numerics (≤ 1 %, independently confirmed); classical-NG validity at near-miss crossings (negligible ≤ 3 keV; ≲ 10-30 % on Δs_B at Λ ≳ 10-20 keV, where Δs_MS dominates); material budget (Δs_MS ∝ √(x/X0); OT phase shifts 4-150 µm per ±10 %); B map (≤ 1-2 %). The straight-string comparison is superseded, not a systematic (Li-type −3…−35 % depending on γ*, if anyone needs the number) | must | S-1, S-2, S-12 |
| §12 Signal shape (iii) | material ±5-10 % | Also through the mean-energy-loss phase drift: OT hits shift 40 µm-1.5 mm; the material scale is a fit nuisance | should | S-12 |
| §3 / §6 | motivation | Add: discovery ⇒ T_max ≲ m_Q/25, T_RH ≲ 5-40 GeV (implication contour); GUT-ladder lines for doublets (labelled); the window is generic-hidden-sector motivated | wording | S-14, S-15 |
| §5/§10 (new observables) | — | BTL double hit (ℓ₀; TOFHIR capability), OT HIP bit for merged pairs, ISR + delayed calorimeter deposit at 1 TeV, ML features of S-7 | should | S-6, S-7, S-8, S-10 |

### 4.2 `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md`
- **§1 P-S1 and §6 W3** ("fast numba propagator (straight string + B + Bethe-Bloch)"), **must**: use the causal algorithm. `theory_track/code/T3_causal.py` already provides it: B, MS, mean dE/dx, straggling, hit recording, stop/exit. It is validated against ExactPair, T2 and an independent conformal-gauge solver (R1), and is ~10³× faster than Python.
  - Add the two-roots-per-chord hit fix (R1 C-1) before production.
  - If a straight-string code is wanted anyway, it must be CM-simultaneous and step-converged on hit positions.
- **§1 P-S0 (Zenodo GNN samples)**, **must**: no material, no PU, prescription unknown. Use them for plumbing; use them for physics only after validation against `T3_causal.py` (S-1).
- **§2 S1-VAL (iii)**, should: replace "causal vs straight string" with the §4.1 V3 validation set.
- **§6 W1 (v)**, must: keep the looper-killer exemption. MaxSteps 2×10⁶ kills quirks for Λ ≳ 24 keV in a CMS-size tracker (S-9). Also check the G4 `DistChord() = 0` chord error [T2 §5.1].
- **§6 W1 (ii)**, must: `G4hMultipleScattering` is required, since MS dominates the thickness for Λ ≳ 1.5-2 keV (S-2). Validate against `T3_ms_thickness.py`.
- **§6 W8 (GNN)**, must: training truth from causal + material samples. Train on 3-4 hits per layer. Use resolution-aware coplanarity features (S-2) and the physics features of S-7.
- **Grid** (STRAT §7, TH §7), wording: no change needed. Consider Λ = 0.45 keV at 500 GeV if the edge matters, once the resolution-aware finder exists.

### 4.3 `research/theory_signal_model.md`
- **§0 item 4a, §4.2 Tab.4.2b, §4.4:** causal thickness table and revised window (truth level), crediting 2002.07503 App.C.
- **§0 item (d), §1.1, §6.1 "~1.7 keV":** use 1/0.709 (SU(2)) or 1/0.646 (SU(3)). m₀ = 3.78√σ for SU(2).
- **§3.1:**
  - "straight-string approximation good to ≲ 1-4 %" → "angles controlled; Δs differs by 3-35 % (γ*-dependent) between the converged Li method and the exact causal string; lab-time-slice prescriptions are wrong by ×1.5-75" (X-13);
  - the formula → "odd-crossing miss distance; not the plane-fit thickness" (X-2);
  - "Knapen Δφ accumulates" → bounded (T3 §4.1).
- **§3.5 step 2 (i):** causal string as the production model; the CM-simultaneous straight string only as a cross-check.
- **§4.3:** timing medians; 9-21× MIP; stopping 1.0 ± 0.3 % (EB+HB); ≈ 3 hits per layer.
- **§5 string-dynamics row:** "few % in core" → "superseded (Li-type −3…−35 % on Δs, γ*-dependent)". Add the material/energy-loss phase-drift systematics (S-12).

### 4.4 `phase1_strategy/outputs/OPEN_QUESTIONS.md`
- **Q4:** recommend (b) E + Ẽ, without the "2 L points" (S-14). Ẽ needs its own window: ℓ_max ×1.7, N_osc ×0.81 (box B).
- **Q9:** three-category Λ range stays. The low-Λ boundary is ≈ 0.45-0.7 keV at 50 % efficiency *at truth level*. With realistic resolution it must be re-derived with the real finder at fixed background efficiency (S-2).
- **Q10:** strengthen. Merged pair 9-21× MIP. Stopped-particle recast of CMS 1801.00359 with f_stop(EB+HB) ≈ 1 % and a lifetime-dependent live fraction (S-8). Doublet monojet recast (S-14). See §4.5.
- **Q11:** update the medians (9.6/18.7 ns). The 30 % loss threshold is crossed at 1 TeV (2S 44-68 % per pair, 70 % per hit) and only at 2S3 at 500 GeV.

### 4.5 Recasts: existing ones and possible updates (none performed by this track)
Existing quirk recasts of these searches: Farina-Low (CMS HSCP + monojet, 12.9 fb⁻¹, for (1,1)₋₁ and (3,1)_{2/3} quirks) [1703.00912] and Evans-Luty (CMS out-of-time, 38.6 fb⁻¹, E′ and T′) [1811.08903]. FASER's Fig.5 shows both as "Reinterpreted CMS HSCP / OoT" [2607.26195].
| Existing search | Quirk subset covered | Why it may work / fail for quirks | Inputs needed | Effort | Expected |
|---|---|---|---|---|---|
| **CMS stopped particles** [1801.00359] (2015-16, 39 fb⁻¹; calorimeter + muon), and any Run-2/3 update (not checked). **Already recast for E′ quirks by Evans-Luty** [1811.08903] | stopped pairs, Λ ≈ 0.3 keV to ≳ 10 keV (computed; plausibly ≳ 100 keV) | Works: hadronic/EM annihilation of ~2m_Q in EB/HB in an empty BX. Risk: the delay of 0.1-0.5 µs (dissipation) falls where the lifetime-dependent effective luminosity is small (their acceptance curve starts at 100 ns) | f_stop (T3: 1 %), delay distribution (T6), BR_vis, ε_reco for 2m_Q deposits, the paper's lifetime-dependent effective luminosity | 1-2 weeks | Run-2(+3) update: m_Q ≈ 0.15-0.35 TeV (S-8). E-L's existing limit is negligible above Λ ≈ 0.15 keV; FASER/D0 already exclude ≤ 0.18 TeV; it beats them only with B ≲ O(10) |
| ATLAS stopped particles [2104.03050] | same | same | same | 1-2 weeks | similar |
| **CMS HSCP / large dE/dx** [2410.09164]. Farina-Low recast the 12.9 fb⁻¹ version: 650 GeV at Λ = 1 eV, 150 GeV at 100 eV, none at 1 keV for (1,1)₋₁ [1703.00912 Tab.II] | merged pairs (Λ ≳ 20-30 keV); Farina-Low cover Λ ≲ 0.1 keV, where tracks look nearly helical | The pair is net neutral, so the "track" is straight and its p_T measurement is meaningless. Strip cluster cleaning may reject partially merged pairs. The dE/dx (9-21× MIP) is very large (S-10). Track-based HSCP selections may fail; a dE/dx-only selection would work | track-reconstruction behaviour for two overlapping opposite-charge tracks (needs CMS simulation) | weeks (CMS-internal) | unknown |
| ATLAS multi-charge [2303.13613] | merged \|q\| = 2 pairs | same issue (net neutral, straight); applicability UNVERIFIED | as above | weeks | T6's "≈ 1.1 TeV" is UNVERIFIED |
| **Monojet / compressed EW** (CMS, ATLAS Run 2; not opened). Farina-Low already recast the 12.9 fb⁻¹ CMS monojet for singlets (dominant at Λ ≲ 0.2 keV) [1703.00912] | doublet (and triplet) quirks; singlets at low Λ | Works: the pair goes neutral before the first layer (cτ = 7.8 mm) and is invisible; soft pions are below tracking thresholds. σ = ×14 of E, ×2N_IC relative to a Dirac higgsino | published σ×A limits for a higgsino-like doublet (or a DM-mediator fiducial limit) | days | unknown (not opened) |
| Disappearing track (CMS, ATLAS) | Y = 0 triplets ≲ 300 GeV | doublets decay inside the beam pipe; quirk tracks are not helical | — | — | marginal |
| Dilepton / diphoton resonances [1903.06248; 2102.13405] | Λ ≳ 3 MeV (prompt annihilation) | Works if the pair annihilates promptly; BR(ee + μμ) ≈ 18.5 % | σ×BR (T6), limit curves (reading UNVERIFIED) | days | ≈ 0.8-1 TeV (UNVERIFIED) |

Updating Evans-Luty's out-of-time recast with full Run-2+3 data and the causal f_stop (P6, §5) has no solver dependency and is the most likely route to a *stronger* limit in the 0.3-30 keV range. It is better done as a CMS-internal task than as a paper.

### 4.6 Run-3 vs Phase-2: which results carry over (the user plans a Run-3 search first)
Run-3 detector facts are recalled and UNVERIFIED unless stated:
- Phase-1 pixel: 4 barrel layers at r ≈ 2.9/6.8/10.9/16 cm;
- strip tracker: 10 barrel layers to r ≈ 110 cm, some with stereo modules (z information);
- tracker material ≈ 0.4 X0 near η = 0 [1405.6569, as read by R1];
- no MTD, no L1 tracks, PU ≈ 50-60, ≈ 0.3 ab⁻¹ by the end of Run 3.

| Item | Phase-2 result | Run 3 |
|---|---|---|
| S-1 causal string, S-3 thickness physics, S-4 degeneracy | B = 3.8 T | **holds** (same field; the physics is detector independent) |
| S-2 MS floor | 11-22 µm (truth, ≈ 0.19 X0) | ≈ ×1.4 larger for ≈ 2× material (√(x/X0)): ≈ 15-30 µm (ESTIMATE). The hit-resolution conclusion changes: pixel σ_z ≈ 30-40 µm, strip stereo layers give z at the ~mm level. The coplanarity test is again pixel-dominated |
| S-3 window | Λ_low 0.45-0.7 keV (truth) | similar; recompute with Run-3 material and resolution |
| S-5 MET-strip | σ⊥ = 15-35 GeV at PU 200 | better σ⊥ at PU 50-60, so a larger geometric rejection; same caveats |
| S-6 timing | BTL delays; OT ±12.5 ns losses | no BTL/MTD. The strip APV25 readout has its own timing window (25 ns shaping; deconvolution mode), so late hits are also lost, with different fractions (not computed). ECAL timing only for deposits |
| S-7 fit | 9 parameters, OT prediction | holds qualitatively; different layers and resolution |
| S-8 stopped pairs | HL-LHC 0.3-0.55 TeV (EB+HB) | **feasible now**: Run-2+3 update of the E-L recast ≈ 0.15-0.35 TeV (S-8); same EB+HB, f_stop ≈ 1 %. Check the Run-3 filling scheme: 8b4e-type trains kill the "≥ 2 BX" trigger except in the abort gap [1811.08903 Sec.6] |
| S-9 MaxSteps | config | holds |
| S-10 merged pair | 9-21× MIP; IT ToT | holds. Run-3 strips measure charge (analog readout), so dE/dx is available in all strip layers, which is better for the HSCP-like category |
| S-18 L1 | no L1 tracks at Phase 2 for quirks either | L1 MET only; PU 50-60 reduces random planes ×3-4 in density |
| f_stop, timing medians, S-12 | — | f_stop: same calorimeters; timing medians are kinematic (same); energy loss is ≈ 2× larger with ≈ 2× material |

### 4.7 Further realism notes (not studied; flagged)
- **PU-vertex association** and **HLT paths**: see S-18.
- **Alignment**: OT residual misalignment (≈ 10-30 µm, UNVERIFIED) is comparable to the causal OT prediction (15-55 µm) and to the IT out-of-plane resolution. It enters both S-7 and the coplanarity test.
- **0 T / cosmic data**: in 0 T runs the thickness is pure MS. This is a free validation sample for the MS model (S-2), using cosmic muons as the probe of the material [R1-constructive C].
- **ML features and SBI**: S-7 and S-4.

---
## 5. Publishable outputs

A CMS member may write phenomenology papers, but none of these may use CMS-internal information. The Phase-2 material, the PU-200 MET resolution and the detector timing must come from public TDRs or generic detectors. Confirm the policy with the conveners (OQ Q2, Q13; UNVERIFIED).

| ID | Working title | Content available now | Needed for publication grade | Effort | Value |
|---|---|---|---|---|---|
| **P1** (re-scoped) | "Quirk-pair trajectories in a solenoid: exact string dynamics, crossing-generated plane thickness, and multiple scattering" | **Physics:** B-thickness ∝ Λ^−1.6…−2.0, m_Q independent (T3); its origin in a B ln(1/B) impulse at near-miss crossings, confirmed by two independent NG solvers (S-3, X-3); MS floor 10-25 µm with √(x/X0) scaling (S-2); the effect of realistic resolution (S-2). **Method:** causal string validated against a conformal-gauge solver (≤ 1 %); straight-string comparison done correctly: converged Li −3…−35 % depending on γ* (retardation and curvature grow with β*); Li at its printed step ×0.8-20; lab-time slices ×1.5-75 and non-covariant; convergence requirements on hit positions (S-1) | (i) an analytic derivation of the crossing impulse and its coefficient (c ≈ 0.10); (ii) the Athena C++ standalone on common events; (iii) the independent solver extended to MS (R1 has the B-only version); (iv) ≥ 200 events per point, public or generic material and resolution; (v) credit: Li et al. 2002.07503 App.C (formula only order-of-magnitude), the ATLAS Athena `Quirks` code (J. Black, T. Nelson and later authors [2607.26195 acknowledgements]), the Artru/Lund piecewise-null string construction, Kang-Luty, Knapen et al., Sha et al., FASER. Contact the Athena/FASER authors and Knapen-Papucci before submission | **3-5 weeks** (one figure used throughout) | **Medium.** Novelty is the thickness scaling, the crossing mechanism, the MS floor, and practical convergence guidance, *not* the causal string itself (an Athena/Lund construction already used by ATLAS/FASER). Venue risk: it could read as a code-validation note, so lead with the physics of the thickness. The claim must be "public codes", since ATLAS-internal analyses are unseen |
| **P2** | "Measuring the quirk mass and string tension: a degeneracy theorem and the recoil" | Scale-invariance theorem; CRB tables (1-3 % / 0.5-1.5 % with the MET scale); MET-strip alignment; idealised predictive χ²; linearity window and aliasing [T4] | A real fit (Gauss-Newton or SBI) with assignment ambiguity, PU hits and MS, showing the CRB is approached; public MET assumptions. Could be merged into P1 | 3-6 weeks (after P1 code) | Medium-high. First answer to a problem open since 2017 [1708.02243 Sec.IV] |
| **P3** | "Stopped quirks at the HL-LHC" | f_stop with the causal string; dissipation times; BRs; revised reach with live fraction and background (S-8); the ISR + delayed coincidence | 3D CMS geometry with field map from public sources; Λ up to 1 MeV with de-excitation times; HL-LHC filling scheme; backgrounds scaled from 1801.00359 with an energy threshold; a better low-p_T spectrum | 1-2 months | Medium-low (reach 0.3-0.55 TeV EB+HB; partly a refresh of Evans-Luty) |
| P4 | "Cosmology of the mesoscopic quirk window" (note) | T_RH,max map, T^{21/4} scaling, ×2.2 vs 2512.20696, ΔN_eff | resolve ×2.2 with the authors; re-derive the dim-8 matrix element | 2-3 weeks | Low-medium; better as a comment or a section |
| P5 | "GUT-motivated doublet quirks at the LHC: invisible pairs and monojet limits" | ladder strips; doublet cτ, rates | the monojet recast; coloured-D limits | 2-4 weeks | Low-medium |
| **P6** (update) | "Stopped quirks in full Run-2+3 data: an update of the out-of-time recast" (better a CMS-internal analysis) | f_stop from the causal string, delays, BR_vis, reach estimate (S-8, §4.5) | E-L's method [1811.08903] with 1801.00359's (or a newer search's) Stage-3 effective luminosity; selection efficiencies for a 2m_Q deposit; Λ dependence of f_stop to ≳ 100 keV; energy-threshold background | 2-4 weeks | Low-medium as a paper (an update/extension of Evans-Luty); medium as a CMS-internal result: ≈ 0.15-0.35 TeV across Λ ≈ 0.3-10+ keV, above FASER/D0 only with low background |

Recommended order:
1. **P6 as a CMS-internal update** (a stronger limit, no dependency; not a novel method).
2. **P1** (it needs the analytic crossing theory; the independent-solver step is largely done by R1).
3. **P2** (reuses P1's code).

## 6. Killed ideas (consolidated)

| Idea | Killing number | Source |
|---|---|---|
| **"Published central-detector trajectory models are wrong at O(1)" (v1 S-1 headline)** | literal Li, step-converged: Δs/causal = 0.84-1.05 at γ* = 1.28 (0.65-0.97 medians over γ* = 1.05-3); labSS/Li = 1.6-73 on the v1 events; Li + MS gives no fake mm thickness | R1 A-1; F1 `F1_standin.py`; S-1 |
| Lab-time-slice straight string (with B or material kicks) as a propagator | ×1.5-75 in Δs (median ≈ 9); 140-570 µm frame dependence; −1.6 MeV/crossing; fake 0.2-21 mm with MS | T2 §5.1; T3 §3.1 |
| Li-type Euler integration at the printed step bound | ×0.8-20 in Δs, OT hits 6-250 mm off (convergence needs ≲ 10⁻²-10⁻³ of it) | R1; S-1 |
| Plane precession in B as a Λ meter | secular rotation 3-18 µrad (0.6-1 keV), ≤ 0.3 µrad (≥ 3 keV) < MS-induced 4.5-10 µrad | T3 §4.2 |
| Thickness ∝ m_Q/Λ⁴ as the Λ (or m_Q) meter | the B term ∝ qBR/Λ² (m_Q independent); formula ×7-50 off at 3 keV (as Li App.C already shows) | T3 §3.2; T4 §3.2; X-2 |
| dE/dx (or MTD timing) as a mass handle | measures βγ only; adding IT dE/dx changes σ(m_Q) by 0 % | T4 §8 |
| "Positions alone measure m_Q and Λ" | vacuum ln σ Fisher column ≤ 3×10⁻⁷ of the largest (exact scale invariance) | T4 §3.1 |
| Vacuum + first-order-B analytic fit model in the OT | misses 30-45 % of the B effect (confirmed by an independent solver) | T4; S; R1 |
| Kalman filter with a two-point state | phase-linearity window ≤ 0.1 cycle; 3-300 oscillations between layers at ≥ 3 keV | T4 §2.4 |
| Truth-level 3D Δs as the reconstructed coplanarity observable | 2S hits give almost no out-of-plane information (σ_n ≈ 8 mm), PS ≈ 0.25 mm; event-level resolution 23-30 µm | S-2, F1 |
| Midpoint of two quirk hits as a "CM track" | deviates by 35-50 % of the half-separation | T4 §6 |
| Lab-frame "simultaneity problem" in vacuum | all methods agree to ≤ 2×10⁻⁸ ℓ_max; Li's closed form is exact | T2 §2.1 |
| Fixed-ŝ approximation | exact only in vacuum; no transverse restoring force once F_ext ≠ 0 | T2 §9 |
| Rotating component from DY spin | J/(p*ℓ_max) ≈ 3×10⁻¹⁷ | T2 §4 |
| Capture or annihilation at crossings (CMS) | J ≥ 10⁶ħ from the first crossing in 3.8 T | T2 §5.3 |
| Relativistic yo-yo formula | γ* ≤ 2.0-2.5 at the 84th percentile; formula ×3-6 off | T2 §2.4 |
| Quantum spreading, roughening, Larmor, perturbative glueball radiation | 0.5 nm; 5 Å; 1.5×10⁻⁸ eV (Λ/keV)⁴ per crossing; ~10⁻²⁰Λ | T2 §6 |
| Lüscher corrections, string breaking, quirk-quirk Coulomb | 10⁻⁸ at 1 µm; exp(−3×10¹⁶); 3×10⁻¹⁰ | T5 §7 |
| ε inside the CMS tracker | ≲ 0.1 GeV deposited | T2 §6.3 |
| Delta rays, straggling as thickness sources | recoil ≈ 0.2 MeV ≪ 5-15 MeV MS kick | T3 §11 |
| B-field non-uniformity in the barrel | B_r/B₀ ≤ 0.9 % ⇒ ≲ 1-2 % | T3 §4.3 |
| Doublet/triplet charged members as tracker quirk signatures | survival to 3 cm ≤ 0.2 % (doublet) | T3 §5; T6 |
| Internal motion enhancing the merged-pair dE/dx | 0.75-0.90 × two HSCPs | T3 §8 |
| Hit-level dE/dx phase tagging | only 4 IT layers measure charge (Phase 2) | T3 §8 |
| Inelastic γγ as a signal boost; exclusive γγ + PPS as a discovery channel | +4.0-4.2 %; 35 events at 500 GeV | T6 |
| Spin as an acceptance driver | ≤ 25 % | T6 |
| Cosmic-ray, beam-dump, MoEDAL, MATHUSLA/CODEX-b/ANUBIS/FACET | kinematics / stopping in shielding | T6 |
| Stellar cooling; Z → g′g′; light-by-light | m_Q > 1.5 GeV; BR ~ 10⁻¹²; (Λ/m_Q)⁴ | T1 §3 |
| BBN/CMB/γ-ray glueball-decay bounds; CMB-S4 ΔN_eff | τ ≥ 10³⁵ s; ΔN_eff ~ 6×10⁻⁴ | T1 §3 |
| SIDM recalibration, cannibalism as strengthening; Banks-Zaks keV; neutral naturalness keV | ≤ ×1.6; Λ/m_Q ~ 0.02; √σ ≈ 2-40 GeV | T1 |
| Electron stripping in the tracker; net-charged pairs as a benchmark | needs β ≲ 0.01; no benchmark | T5 §7; T3 §5 |

## 7. Residual uncertainties and what is UNVERIFIED
1. **Phase-2 material per layer (most important).** ≈ 19 % X0 at η = 0 is a reconstruction, plausible against public statements (Phase-1 ≈ 0.4 X0 [1405.6569]; Phase 2 "substantially reduced" [1912.02061]). The per-layer split (PS 2.5 %, 2S 1.8 %, IT 1.2 %) is a guess, and IT material is modelled only at |z| < 20 cm [R1 B-4]. The MS floor, f_stop and S-12 depend on it. The user should pull the tkLayout/TDR X0(η) curve (CMS access).
2. **Detector resolution and readout.** Pitches are pitch/√12 guesses: IT 25 × 100 µm², PS 100 µm × 1.5 mm, 2S 90 µm × 5 cm. No charge sharing, no alignment, no inefficiency, no PU hits (S-2).
3. **String model.** The causal string is confirmed as classical NG by an independent solver for B at 0.6-3 keV (thickness, hits, B ln B).
   - Not confirmed against the Athena C++ (G4 geometry, `DistChord() = 0`).
   - Not confirmed with MS by an independent *string* solver (R1 compared Li + MS, a different model).
   - Classical-NG validity at near-miss crossings for Λ ≳ 10-20 keV (X-13).
   - The hit recorder misses grazing double crossings (R1 C-1).
   - The Li-vs-causal comparison is converged at 0.6-3 keV (×10⁻³ at 3 keV, R2) and untested at 5 keV below ×10⁻². The deficit depends on γ*, not on Λ; it was measured at 5 γ* values with 5 events each (R2).
4. **Small MC statistics.** Thickness: 60 events per point (Λ ≤ 3 keV), 24 at 10 keV, 12 at 30 keV. Fisher: 16. Li comparisons: R1 24 events at 0.6-3 keV and 4 at 5 keV, F1 12 (stand-in) + 6 (phase study); Li + MS 22 events. Smearing: 60 per point. Medians carry 10-30 % statistical uncertainty.
5. **Idealisations in the measurement and reconstruction numbers (T4).** Local CRB; known assignment; no PU; thin scatterers.
6. **Experimental inputs used but UNVERIFIED.**
   - PU-200 PUPPI MET resolution and the 1-3 % JES/MET scale;
   - IT ToT range; OT stub windows; BTL σ_t and TOFHIR double hits; barrel |z| acceptances;
   - HL-LHC filling scheme and empty-BX trigger livetime; stopped-particle background at HL-LHC;
   - Run-3 luminosity and detector parameters.
7. **Kinematics.** LO DY+ISR toy, p_T(QQ̄) > 200 GeV. A lowered L1 MET threshold changes the timing and MET numbers. f_stop depends on an assumed low-p_T spectrum (×2).
8. **External limits not opened:** ATLAS dilepton/diphoton at 1.4-2 TeV; monojet/compressed-EW; CMS multi-charge; PPS-2 schedule; any Run-2 update of 1801.00359.
9. **Cosmology.** Freeze-in matrix element taken from 2512.20696 Eq.26 without re-derivation; the ×2.2 is unexplained.
10. **ε model and GUT ladder.** Heuristic ε(b). The ladder uses anchor-and-shift running, ×2-4.
11. **Knapen-Papucci / Sha et al. code** not inspected (S-1 iv).

## 8. Recommended next steps (ordered)

**Do first** (no dependency; days):
- (a) hand `T3_causal.py` to the Phase-2 team as the W3 starting point, with the two-roots-per-chord hit fix;
- (b) the S-9 looper-killer exemption in the CMS port;
- (c) define the resolution-aware coplanarity test together with the experimental team (S-2);
- (d) ask Knapen-Papucci (and Sha et al.) for the string prescription and step of their code, or the code itself.

| # | Step | Why | Effort | Needs the user's CMS access? |
|---|---|---|---|---|
| 1 | Do-first items (a)-(d) above | immediate value; removes risks | days | (c) yes (experimental team) |
| 2 | **Run-2(+3) update of Evans-Luty's out-of-time recast** (P6, CMS-internal): their trigger-fraction method or 1801.00359 Stage 3; f_stop(Λ) to ≳ 100 keV with `T3_causal.py`; energy-threshold background | the most likely route to a stronger limit (0.15-0.35 TeV) | 2-4 weeks | optional (CMS-internal is faster) |
| 3 | **Real Phase-2 material and resolution**: per-layer x/X0(η), pitches, alignment; re-run `T3_ms_thickness.py` and `F1_smear.py` at ≥ 200 events per point; deliver efficiency curves for a resolution-aware finder | the window and the Δs optimisation against PU 200 need them | 3-5 days | yes |
| 4 | **Analytic crossing theory**: derive the near-miss transverse impulse and the coefficient c ≈ 0.10 | P1 content; replaces the formula | 1-2 weeks | no |
| 5 | **Athena C++ standalone** on ~10 common events (vacuum, 3.8 T, 3.8 T + MS); extend R1's conformal solver to MS | the remaining validation of the production model | 1 week | no |
| 6 | **Write P1** | after 4-5 | 3-5 weeks | no |
| 7 | **Measurement demonstration** (Gauss-Newton and/or SBI) with assignment ambiguity, PU hits, alignment | P2; S-7 realistic rejection | 3-4 weeks | partly (PU) |
| 8 | **MET-strip gain on real backgrounds** (Z(νν), lost-lepton W, PU) | S-5 must not enter a background estimate unmeasured | experimental | yes |
| 9 | Doublet monojet recast; GUT-ladder lines | S-14 | ~1 week | no |
| 10 | \|q\| = 2 window with the causal string | S-17 | 2-3 days | no |
| 11 | Cosmology note (contact 2512.20696) | S-15 | 1-2 weeks, optional | no |
| 12 | ε(b) and J random walk for FASER | S-19, low CMS value | weeks | no |

Hand-offs that are not theory work: OI-1 timing (S-6), MET-alignment implementation and its real-background gain (S-5), PU-200 random-plane background, PU-vertex association and the L1 φ-road (S-18), HSCP recast (S-10).

## 9. Source map

| Claim in this document | Supported by |
|---|---|
| Causal port = classical NG (independent) | R1 `R1_conformal_ng.py`, `figures/R1_conformal_ng_out.txt` |
| Li method converged: γ*-dependent deficit (0.97-0.65 at γ* = 1.05-3); printed step unconverged | R1 `R1_li_literal.py`, `figures/R1_li_literal_out_a/b.txt`; F1 `F1_standin.py`, `figures/F1_standin_out.txt` |
| Residual Li hit differences = phase drift from step non-convergence | F1 `F1_li_phase.py`, `figures/F1_li_phase_out.txt` |
| Li + MS gives no fake thickness | R1 `R1_li_ms.py`, `figures/R1_li_ms_out.txt` |
| labSS/cmSS numbers (non-covariance, spurious work, ×1.5-75, fake MS) | T2 §5.1, `T2_covariance_test.py`, `T2_string_methods_B.py`; T3 §3.1 |
| Li closed form exact in vacuum; ℓ_max, N_osc closed forms; scalar ×1.7/×0.81 | T2 §2.1-2.2, §3; S checks 1-2 |
| MS floor 11/15/22 µm; pass fractions (truth level) | T3 §3.2, §9; S check 9 |
| Hit-resolution effect; per-hit out-of-plane resolution | F1 `F1_smear.py`, `figures/F1_smear_out.txt` |
| √(x/X0) scaling of the MS thickness | S `S_msscale.py` |
| Causal thickness Λ^−1.6…−2.0, m_Q independent | T3 §3.2; T4 §3.2; R1 §2 |
| Formula only order-of-magnitude (prior work) | 2002.07503 App.C, Fig.8 |
| Non-linear B response; B ln B | T4; S `S_Bnonlin.py`, `S_Bscan.py`; R1 `R1_Blinearity.py` |
| Revised window 0.45-0.7 keV (truth) | T3 §9 |
| Degeneracy theorem; CRB numbers | T4 §2.1, §3.1, §4.3; R1 §3 |
| MET alignment ×13-34 (random planes) | T4 §5.1; S check 11; R1 C-5 |
| Causal fit, predictive χ², seeding, L1 stubs | T4 §2.3-2.4, §5.2-5.3, §6 |
| Timing medians; per-layer losses; ≈ 3 hits per layer | T3 §6; S check 3; R1 C-1 |
| f_stop 1.0 ± 0.3 % | T3 §7 |
| Stopped-pair reach with live fraction and background | F1 `F1_stopped.py`, `figures/F1_stopped_out.txt`; 1801.00359 Sec.3, Tab.4; T6 G-T6-4 |
| Merged pair 9-21× MIP | T3 §8 |
| Doublet cτ, rates | T6 G-T6-2; T3 §5; S check 7; R1 |
| Λ conventions; GUT ladder; cosmology | T1; T5; S checks 4, 5, 13, 14; R1 §4 |
| MaxSteps killer | T2 G-T2-2 |
| Recast inputs | 1801.00359; 2104.03050; 2410.09164; 2303.13613; 1903.06248 (as read by T6) |

---
## 10. Response to reviews

### 10.1 Review R1

#### 10.1.1 Critical review (`review/CRITICAL_REVIEW_R1.md`)
| Item | Response | Where |
|---|---|---|
| **A-1** S-1 numbers describe T2's labSS, not Li et al. | **Accepted.** The v1 claim is withdrawn. S-1 is rewritten around four statements: causal = exact classical NG (independently confirmed); Li ≈ −15 % when converged (shown at 0.6-2 keV); printed step not converged; lab-slice unusable; Knapen/Sha unknown. Our own test on T2's events gives labSS/Li = 1.6-73 (0/12 within ±50 %). The residual mm hit differences at 2 keV are Li step non-convergence (in-plane phase drift; 0.07-0.53 mm at ×0.001). From R1's final runs: Li convergence worsens with Λ. (v3, R2: the deficit is γ*-dependent, and 3 keV converges at ×10⁻³.) labSS relabelled in T2/T3 (erratum boxes) | §0, S-1, X-2, X-13, §3 rows 15-16, §6; `F1_standin.py`, `F1_li_phase.py`; T2/T3 errata |
| **A-2** Downstream advice would mislead Phase 2 | **Accepted.** "Use the causal string" is kept. "Straight string is wrong / not a systematic / expect O(1) vs Zenodo" is replaced by: never lab-slice; Li-type ≈ 15 % if converged (superseded, not a systematic); validate any external sample against `T3_causal.py` | §4.1 (§4.2 b1, §9.2, §9.4 V3/V5, §12 (i)), §4.2 P-S0/W3/W8, §4.3 §3.1/§3.5/§5 |
| **A-3** 35/35 never tested the S-1 premise | **Accepted.** §3.0 states what the checks did and did not test, with independent vs re-run counts. New rows 15-21 include the explicit stand-in test (FAIL for the v1 premise) | §3.0, §3.1 |
| **B-1** "exact" means classical NG; cutoff at near-miss crossings | **Accepted.** "Exact classical NG with point endpoints" everywhere; a validity caveat (≲ 10-30 % on Δs_B for Λ ≳ 10-20 keV, negligible ≤ 3 keV) in S-1, S-3, X-13, §4.1 §12 row, §7 | S-1, S-3, X-13, §4.1, §7 |
| **B-2** Efficiencies are truth level; resolution and 2S z-blindness ≈ MS floor | **Accepted and quantified.** All S-2/S-3 efficiencies are labelled truth level. A smearing study with Phase-2 pitches and a weighted plane fit (`F1_smear.py`, 720 events) gives per-hit σ_n ≈ 17 µm (IT), 0.25 mm (PS), 8 mm (2S) and an event-level 23-30 µm (≈ the MS floor, as R1 expected). The test is IT dominated. A t_est < 100 µm cut keeps 60-73 % at 0.3-0.45 keV (truth 13-42 %), and a < 30 µm cut keeps 83-95 % at 1-10 keV (truth 43-82 %). (v3: R2-B4 showed these cuts have different background rejection, so no edge shift is claimed.) Not done: PU, alignment, charge sharing (left to the experimental track) | S-2 table, S-3, Box A, §0, §4.1 §9.1, §4.4 Q9, §6 |
| **B-3** ×7-50 vs formula already in Li App.C | **Accepted.** 2002.07503 App.C/Fig.8 is credited. Novelty is re-scoped to Λ^−1.6…−2.0 + m_Q independence, the B ln B origin, and the correction of the project's own window | S-3, X-2, §4.1 V2, §5 P1, §6 |
| **B-4** Material: plausible total, unverified split; √(x/X0) check internal | **Accepted.** UNVERIFIED tags on the MS floor, f_stop and S-12. Check row 10 is relabelled "scaling of the code". The user is to pull the tkLayout/TDR X0(η) (step 3) | S-2, §3 row 10, §7 item 1, §8 |
| **B-5** "1 %/0.5 %" below the MET-scale floor | **Accepted.** Headline 1-3 % (m_Q), 0.5-1.5 % (Λ), MET-scale limited; CRB local, known assignment, no PU; γ* model dependence untested | §0, S-4, §4.1 §5 O6, §5 P2 |
| **B-6** Stopped-pair live fraction and background | **Accepted and quantified** (`F1_stopped.py`): a lifetime-dependent empty-BX live fraction (0.027-0.086 at τ = 0.1-0.5 µs vs 0.21) and B = 0/10/230. HL-LHC EB+HB reach 0.3-0.55 TeV (was 0.65). The paper's own Stage-3 effective luminosity is still needed (the filling scheme is a stand-in) | S-8, §4.5, §5 P3/P6 |
| **B-7** Ranking and paper plan | **Accepted with one difference.** S-1 stays rank 1, but as "validated production propagator" (adopt + validate external samples), which is the most actionable item, not as "literature wrong". P1 re-titled and re-scoped as suggested. Types (C/N/Ch/D) added | §1 table, S-1, §5 |
| **B-8** T2's Λ^−2.5 and 4-event tables | **Accepted.** Retired (X-1) and marked superseded in the T2 erratum. We also note that T2's causal column (max_boost 10⁻²) differs from the converged causal by up to 25 % on the same events (`F1_standin.py`). **Not done:** redoing the covariance test with the Li-literal prescription. We accept R1's construction argument (CM simultaneity and ŝ are 4-vector statements) and expect frame independence up to Euler error; a numerical test would need a frame-transformed Li implementation | X-1, T2 erratum, §7 |
| C-1 double crossings per chord | Applied as a note (S-6, X-11, §4.2 W3: fix before production); code not changed (T3's file) | S-6 |
| C-2 Δs definition | Applied (glossary) | §0.1 |
| C-3 check 9 "PASS" at 25 % | Applied ("consistent within MC statistics") | §3 row 9, S-2 |
| C-4, C-5 | Applied (C-5 three points in S-5) | S-4, S-5 |
| C-6 T_RH range, ×2.2 | Applied (5-40 GeV; g*s more plausible) | S-15, Box A |
| C-7 flat-in-Λ caveat | Applied (S-8, §4.5) | S-8 |
| C-8 number mismatches | Applied (S-1 numbers moot; "verified" → scaling only; S-9 = config note) | S-2, S-9 |
| C-9 credit Artru/Lund, Li App.C | Applied (UNVERIFIED as cited) | X-13, §5 P1 |

#### 10.1.2 Constructive review (`review/CONSTRUCTIVE_REVIEW_R1.md`)
| Item | Response | Where |
|---|---|---|
| **A1** headline vs small effect on sensitivity | **Accepted.** The headline is withdrawn (it was also wrong, per critical A-1). The executive summary states the effect on reach explicitly: no change computable; truth-level edge 0.45-0.7 vs 0.54-0.81 keV; the realistic-resolution caveat | §0.2 |
| **A2** no statement that no new exclusion was derived; UNVERIFIED next to verified | **Accepted.** "Bottom line" paragraph; VERIFIED / UNVERIFIED table; Λ ≳ 3 MeV and doublets labelled as readings of existing limits | §0.2, S-16 |
| **A3** MET-strip ×13-34 vs real background | **Accepted.** "Against random planes, per candidate", with a qualitative estimate for PU (≥ geometric), Z(νν) UE after cleaning (≥ geometric), lost-lepton/τ W (×≈1-3), multijet (cleaning first). "Do not put ×13-34 into a background estimate" | S-5, §4.1 §5 O7, §8 step 8 |
| B1 consolidated Λ answer | Box A | §1 |
| B2 oscillation length; scalars | Box B (scalar ℓ_max ×1.70-1.73, N_osc ×0.81, verified in T2 §3) | §1, §0.2 |
| B3 PU-vertex / beam-spot ambiguity | Short note, flagged not studied. The plane's z₀ to ≈ 30-60 µm; ≈ 30 % of events have another PU vertex within ±100 µm. This is a *background handle* (the ISR jet defines the PV), not a signal ambiguity | S-18 |
| B4 HLT paths | Table of paths (flagged UNVERIFIED) | S-18 |
| B5 Run-3 vs Phase-2; Run-3 stopped recast | §4.6 table. Run-2+3 stopped recast (v3: 0.15-0.35 TeV, an update of Evans-Luty's recast; S-8). **Partial disagreement:** the reviewer's 0.3-0.4 TeV holds only for zero background and long delays; with τ = 0.1-0.5 µs it is 0.22-0.34 TeV | §4.6, S-8 |
| B6 ML features | List in S-7 | S-7 |
| B7 SBI | Paragraph in S-4 (suggestion only) | S-4 |
| B8 recast table | §4.5 (none performed); new P6 | §4.5, §5 |
| B9 S-7 idealised | "Predictive power (idealised upper bound)", alignment and PU caveats, "do not quote in a proposal" | S-7, §1 table |
| B10 P1 novelty | Re-framed: novelty is the thickness scaling, B ln B mechanism, MS floor and convergence guidance, not the causal string. Venue risk stated; "public codes" only | §5 P1 |
| B11 glossary and thickness definitions | §0.1 glossary (causal string, Li method, labSS, cmSS, d, b_odd, Δs, x_B, t_est, truth level) before first use | §0.1 |
| C items | Applied: correction vs capability labels (Type column); S-9 in "do first"; P1 effort unified (3-5 weeks); CMS-access column in §8; severity column in §4.1; coloured-quirk contrast (S-14); k-string and N_IC = 3 rows (Box A); T-n → X-n; "35/35" restated (§3.0); 0 T validation sample (§4.7); Λ-convention wording (glossary). Not applied: a figure pointer per §4 row (a single "read first" line instead) | various |

#### 10.1.3 Remaining disagreements and open items (after R1)
- **S-1 rank:** we keep S-1 at rank 1 (critical B-7 suggested demoting it), but re-scoped as the validated production propagator. The reason is that it is the most actionable item for the experimental track (W3, GNN truth, validation of external samples).
- **Truth-level window (critical B-2):** superseded by R2-B4. The smeared and truth cuts have different background rejection, so no edge shift is claimed; the realistic edge needs a matched-background comparison.
- **Not done in this pass:**
  - the Li covariance re-test (B-8);
  - an independent string solver with MS (R1 used Li + MS);
  - Li convergence at 3-5 keV (needs ≳ 10⁹-10¹⁰ steps per event);
  - PU and alignment in the smearing study;
  - the Athena C++ comparison.

### 10.2 Response to review R2 (`review/REVIEW_R2.md`)
| Item | Response | Where |
|---|---|---|
| **R2-A1** stopped-pair recast presented as novel; Evans-Luty already recast 1801.00359 for E′ | **Accepted.** Evans-Luty is credited for: the recast of CMS 1801.00359 for E′ / SU(2)_IC; f_stop in a CMS model; the lifetime-dependent trigger fraction from real 2016 fills (≈ 8-10 % at Λ ≳ 300 eV); the 300 fb⁻¹ naive (≈ 0.15-0.2 TeV) and optimised (≈ 0.7-0.75 TeV) projections; the HGCAL-timing and 8b4e remarks [1811.08903 abstract, Sec.3-6, Figs.3-5]. "First LHC limit" and "none performed" are removed. The proposal is reframed as an *update* (full Run-2+3, causal f_stop, triggered-sample f_stop, HL-LHC projection with a background bracket). P6 is retitled and down-rated; it is better as a CMS-internal task. Our numbers are compared with E-L's projections | §0 ("What changed in v3", Bottom line), S-8, §4.5, §4.6, §5 P6, §8 step 2 |
| **R2-B1** "Li ≈ 15 % low" measured at one γ* | **Accepted.** Everywhere it now reads γ*-dependent: ≈ 3 % (γ* ≈ 1.05), ≈ 15 % (1.3), 30-35 % median (2-3), single events −47…+36 %, out-of-plane differences up to 124 µm. The deficit is Λ-independent (0.86 at 3 keV converged). "γ* = 1.28" is added to every 0.84-1.05 quote. The fixed 0.85 validation target is replaced by an event-by-event comparison in γ* bins with `T3_causal.py`. "Superseded, not a systematic" stands | §0, VERIFIED table, S-1 (table, (ii), exploitation (e)), X-2, X-13, §3 rows 22-23, §4.1 (§4.2 b1, V3, V5, §12 (i)), §4.3, §5 P1, §6, §7 |
| **R2-B2** existing E-singlet exclusions missing | **Accepted.** New Box A row: Farina-Low (opened: 650/150 GeV at Λ = 1/100 eV, none at 1 keV, fermion (1,1)₋₁ N_IC = 2; scalar 350/60 GeV [1703.00912 Tab.II]); Evans-Luty (negligible above 0.15 keV); D0 (107 GeV, 10 keV-1 MeV, opened [1008.3547 abstract]); FASER (opened: first above-weak-scale exclusion for 300 eV-100 keV, 179 GeV at 10 keV [2607.26195 abstract]). Also in the §4.5 preamble and the HSCP/monojet rows | Box A, §4.5 |
| **R2-B3** Run-2+3 headline uses rejected assumptions | **Accepted.** Now ≈ 0.15-0.35 TeV (τ = 0.1-0.5 µs, B = 0-80). It does not beat FASER (≤ 0.18 TeV) or D0 (≈ 0.11 TeV) at its low end, and improves on them only with B ≲ O(10) | §0, §1 table, S-8, §4.5, §4.6, §5 P6, §8 |
| **R2-B4** smeared-vs-truth edge comparison at unequal background rejection | **Accepted.** No edge shift is claimed. t_est and truth Δs are different observables; an IT-dominated test passes prompt p_T ≳ 100 GeV track pairs (sagitta ≈ 0.32 mm × 10 GeV/p_T at 14.6 cm). The edge is undefined until set at fixed background efficiency; low-Λ discrimination must come from OT rφ non-helicity and multiplicity. The per-hit resolutions and "truth-level cut values do not transfer" are kept | §0, Box A, §1 table (S-3), S-2 "Reading the table", S-3 window, §4.1, §4.4 Q9, §10.1 B-2 note, §10.1.3 |
| R2-C1 number mismatches | Applied: 53-80 µm at 0.6 keV; 4 of 6 events move > 10 % at 3 keV; labSS unified as ×1.5-75 (median ≈ 9) | S-1, X-13, §4.3, §6, §9 |
| R2-C2 "not reached at 3-5 keV" | Applied: converged at 3 keV at ×10⁻³; 5 keV untested below ×10⁻² | §0, S-1, §7 |
| R2-C3 1.3τ background window | Applied: the B ≈ 230 column is ≈ ×2 pessimistic; the bracket holds | S-8 |
| R2-C4 E-L delay range | Applied: ≈ 0.1-5 µs, peak ≈ 0.5 µs for Λ ≳ 300 eV; 0.1-100 µs is the low-Λ regime | S-8 |
| R2-C5 "upper bound" wording | Applied: "consistent with pure integration error" | S-1 |
| R2-C6 pair calorimeter deposit in the MET | Applied: ≲ 5 GeV, one-sided ≲ 2 % bias, correctable | S-4 (iv) |
| R2-C7 Λ range of the recast | Applied: "computed to 3 keV (E-L flat to 10 keV), plausibly ≳ 100 keV"; ε-dependent in-flight annihilation above ~0.1 MeV | S-8, §4.5, §0 |
| R2-C8 credits and wording | Applied: T. Nelson added next to J. Black; ×1.7 vs ×1.9 scalar ratios distinguished | §5 P1, Box B |
| R2-C9 handles for the sub-µs delay | Applied: HGCAL timing (O(90 %) triggerable fraction forward); fill schemes with short gaps help, 8b4e hurts | S-8, §4.6 |

**Remaining after R2:** none of the A or B items is disputed. Still open:
- a matched-background evaluation of the resolution-aware finder (experimental track);
- γ* dependence at higher statistics and at other Λ (5 events per γ* point);
- the Li covariance test;
- the Athena C++ comparison;
- the trigger fraction for the HL-LHC filling scheme (use E-L's method).
