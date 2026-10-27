# C001 quirks, theory track: synthesis of theory gaps and how to exploit them

Executor: S (synthesis). Date: 2026-10-08. Status: DRAFT v1, for critical review.
Inputs: investigator reports T1-T6 (`theory_track/investigations/`), their code (`theory_track/code/T*_*.py`) and
figures, `theory_track/LOG.md`, `research/theory_signal_model.md` (TH), `phase1_strategy/outputs/STRATEGY_DRAFT.md`
v3 (STRAT), `phase1_strategy/outputs/OPEN_QUESTIONS.md` (OQ), `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md` (SREQ).
Synthesis checks: `theory_track/code/S_*.py` (run from `theory_track/` with `pixi run python code/<file>`); their
outputs are copied to `theory_track/figures/S_*_out.txt`.

Conventions: **Λ ≡ √σ_string** throughout (BRIEF §1). σ = 50.68 GeV/cm × (Λ/keV)². Benchmark E = (1,1)₋₁ Dirac
fermion, N_IC = 2, CMS Phase-2 (3.8 T, PU 200, 3 ab⁻¹) unless stated.

Tags: `[T3 §3.2]` = section of an investigator report; `[1911.02223 Eq.III.12]` = primary paper, as cited by the
investigator; `[S: S_Bnonlin.py]` = a check run for this synthesis; `ESTIMATE` = own calculation;
`UNVERIFIED` = not checked against a primary source. Gap IDs of this document are **S-n**. Each one lists the
investigator gaps it merges (G-T1-…, …, G-T6-…).

---

## 0. Executive summary

The six reports form a coherent picture. My cross-checks pass 35/35 (Sec. 3), after correcting two convention errors of my own.

1. **Every published central-detector trajectory model is wrong at the order that matters (S-1).**
   - The instantaneous straight string (Knapen, Li, and the GNN samples of Sha et al.) is not covariant at O(F_ext/σ), which is the order of the plane thickness.
   - In 3.8 T: thickness ×0.04-60 off, OT hits 0.2-35 mm off [T2 §5.1]. With MS kicks: fake 0.2-21 mm, against 2-25 µm for the exact string [T3 §3.1].
   - The ATLAS Athena causal string is exact Nambu-Goto (covariant to 0.05 µm). It must be the only signal model, including the fast propagator and the GNN training samples.
2. **The thickness physics differs from the literature formula, and MS sets a floor (S-2, S-3).**
   - Causal B thickness: 32-38 µm at 1 keV, ∝ Λ^−1.9, ~m_Q independent. The m_Q/Λ⁴ formula is ×7-50 low at 3 keV [T3 §3.2].
   - The B response is non-linear (B ln B), generated at the near-miss crossings. Confirmed: exactly linear before the first crossing, 31-35 % non-linear after it [S: S_Bnonlin.py].
   - MS floor: 11/15/22 µm at 200/500/1000 GeV, ∝ √(x/X0) (verified).
   - The window survives: Δs < 100 µm passes 93-100 % at 1-30 keV; the 50 % edge is at Λ ≈ 0.45-0.7 keV. A Δs cut below ~30 µm costs 30-45 % of heavy signal.
3. **Hits measure only ℓ₀ = m_Q/Λ² (S-4, S-5).**
   - The MET recoil gives σ(m_Q)/m_Q ≈ 1 % and σ(Λ)/Λ ≈ 0.5 % with 30 events (floor: the 1-3 % MET scale). The B field gives Λ only for Λ ≲ 2 keV [T4 §4.3].
   - MET-strip alignment rejects random planes ×13-34 at 95 % signal efficiency [T4 §5.1].
4. **The strategy's timing numbers describe the slow third of the sample (S-6).** Median BTL delays are 3.5/9.6/18.7 ns; 6/16/33 ns are the 84th percentiles. At 1 TeV, 44-68 % of 2S crossings fall outside ±12.5 ns, with ~3 hits per layer [T3 §6].
5. **Complementary channels, now quantified (S-8, S-10, S-14, S-16).**
   - Stopped pairs: f_stop(EB+HB) = 1.0 ± 0.3 %, reach ≈ 0.65 TeV (EB+HB) or ≈ 0.9-1.0 TeV (full calorimeter).
   - The merged pair is 9-21× MIP, not 2×.
   - Doublets are invisible to the tracker: a monojet + soft-pion recast.
   - Λ ≳ 3 MeV is probably already excluded to 0.8-1 TeV (UNVERIFIED).
   - Housekeeping: the Λ convention is 1/0.709, not 1/0.6 [T1]. Cosmology turns a discovery into T_max ≲ m_Q/25 [T1].

**Paper-ready after one more step (Sec. 5):** "Quirk trajectories need the causal string" (S-1 to S-3). It needs an independent Nambu-Goto solver or a run of the Athena C++, about 2-4 weeks.

---

## 1. Ranked list of distinct gaps

Ranking criterion: (impact on the CMS search or on the constraints) × confidence ÷ effort, judged per entry.
"Effort" is the remaining work, not what has been done. Verdicts: EXPLOIT / WORTH A CHECK / NOT A GAP.
The IDs S-n follow the order of discussion below; the Rank column gives the ranking.

| Rank | ID | Gap (short) | Merges | Best number(s) | Route | Remaining effort | Conf. | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | S-1 | Straight string is invalid at O(F_ext); causal string is the only valid model | G-T2-1, G-T3-2, G-T5-2, part of G-T4-1 | thickness ×0.04-60, OT hits 0.2-35 mm (B); fake 0.2-21 mm (MS) vs 2-25 µm | signature model, systematic, reconstruction, paper | days (adopt `T3_causal.py`); weeks (paper) | high (qual.), med-high (quant.) | **EXPLOIT** |
| 2 | S-2 | MS floor on the plane thickness; Δs cut floor | G-T3-1, G-T5-1 | Δs_MS = 11/15/22 µm; pass(100 µm) 0.93-1.00; ≤ 30 µm cut loses 30-45 % | reconstruction, systematic | days (real material) | medium | **EXPLOIT** |
| 3 | S-6 | Timing: medians, late-hit losses, multiple hits per layer | G-T3-3, G-T5-12 | BTL median 3.5/9.6/18.7 ns; 2S lost 7-33 % (500 GeV), 44-68 % (1 TeV) | reconstruction, readout (OI-1) | done (documentation) | high | **EXPLOIT** |
| 4 | S-5 | MET-strip alignment | G-T4-5, G-T5-10 | ×13-34 random-plane rejection at 95 % eff.; seeding wedge ÷16 | signature / background | days | high (geometry) | **EXPLOIT** |
| 5 | S-3 | B-field thickness physics: Λ^−1.9, m_Q-independent, non-linear (B ln B) at crossings; revised window | T3 §3.2 + §9, G-T4-3 (thickness part), G-T4-4, T2 §5.1 | 32-38 µm at 1 keV; formula ×7-50 low at 3 keV; non-linearity 31-35 %; Λ_low(50 %) 0.45-0.7 keV | signature, systematic, paper | 1-2 weeks (independent solver) | medium | **EXPLOIT** (window, validation); WORTH A CHECK (theory) |
| 6 | S-4 | Degeneracy theorem and (m_Q, Λ) measurement | G-T4-2, G-T4-3, G-T5-7, G-T2-4, G-T1-7 | MET route 1.0 % / 0.5 % (N = 30); B route 1.5-2.2 % on Λ at 1 keV, dead ≥ 3 keV | measurement, paper | days (write-up); weeks (real fit) | high (theorem), medium (numbers) | **EXPLOIT** |
| 7 | S-7 | Causal 9-parameter global fit; predictive χ²; two-regime seeding | G-T4-1, G-T4-6 | prediction 15-55 µm per OT hit ⇒ ×20-100 per layer (1 keV), ×2-10 (3 keV), none at 10 keV | reconstruction | weeks | medium | **EXPLOIT** |
| 8 | S-8 | Stopped-pair delayed annihilation (+ ISR-triggered coincidence) | G-T6-4, G-T3-4 | f_stop(EB+HB) 1.0 ± 0.3 % (×2); reach ≈ 0.65 TeV (EB+HB), 0.9-1.0 TeV (full calo.); 1.3-2.5 % of triggered 1 TeV events | new channel, constraint, paper | weeks | medium | **EXPLOIT** |
| 9 | S-9 | Athena step-count killer | G-T2-2 | MaxSteps 2×10⁶ kills quirks inside the tracker for Λ ≳ 24 keV | systematic (simulation config) | hours | medium | **EXPLOIT** (config) |
| 10 | S-10 | Merged regime is 9-21× MIP; HSCP-like category | G-T3-5, G-T5-6 | median pair deposit 9× (500 GeV), 21× (1 TeV) MIP | signature, recast | days | medium | **EXPLOIT** (correction); WORTH A CHECK (recast) |
| 11 | S-11 | Λ conventions and closed-form kinematics | G-T1-1, G-T5-4, G-T2-3 | T_c/√σ = 0.709 (SU(2)); ℓ_max = 3.95 cm (γ*−1)(m/100)(keV/Λ)²; N_osc ≈ 12 (Λ/keV)² | documentation | hours | high | **EXPLOIT** |
| 12 | S-12 | Mean energy loss shifts OT hits; material is a fit nuisance | G-T4-7 | 40 µm-1.5 mm OT shifts; ±10 % material ⇒ 4-150 µm | systematic | days | medium | WORTH A CHECK |
| 13 | S-13 | Production modelling of the ISR tail | G-T5-5, T2 §3 | fixed-p_T trick: ℓ_max −10-25 %, N_osc +20 %; 37 % reach spread between groups | systematic | weeks (experimental) | high | EXPLOIT (already in STRAT §12) |
| 14 | S-14 | GUT-ladder Λ strip (doublets) and doublet invisibility ⇒ monojet + soft displaced pions | G-T1-2, G-T1-6, G-T6-2, G-T3-7 | SU(2) n_S = 3: √σ ≈ 0.8/2.6/6.4/15 keV at 0.2/0.5/1/2 TeV; doublet cτ = 7.9 mm; rate ×14 of E | constraint, motivation | days | medium (ladder), low-med (recast) | EXPLOIT (lines); WORTH A CHECK (recast) |
| 15 | S-15 | Cosmology: discovery ⇒ reheating bound; 2512.20696 normalisation | G-T1-4, G-T1-3, G-T1-5 | T_max ≲ m_Q/25; T_RH ≲ 5-35 GeV; ×2.2 vs 2512.20696; Ω ∝ T_RH⁵ not T⁷ | constraint (implication), note | days | medium | EXPLOIT (figure); WORTH A CHECK (note) |
| 16 | S-16 | Microscopic complement: Λ ≳ 3 MeV prompt resonance, 0.1-3 MeV displaced band | G-T6-5 | σ×BR(ℓℓ) = 1.1 fb at 500 GeV; probably excluded to 0.8-1 TeV (UNVERIFIED) | scoping, new channel | days | low | EXPLOIT (scoping); WORTH A CHECK |
| 17 | S-17 | Multi-charged singlets |q| = 2 | G-T6-3, G-T5-8 | σ ×4; reach ≈ 1.3 TeV; Λ_low ×≈1.4 (corrected here) | constraint | days | medium | WORTH A CHECK |
| 18 | S-18 | Trigger and PU-200 realism (handed to experiment) | G-T5-3, G-T5-9, G-T4-6 (L1) | only 23-47 % of OT crossings make 2 GeV stubs at Λ ≤ 3 keV | trigger | months | medium | WORTH A CHECK (experimental) |
| 19 | S-19 | ε (glueball per crossing) depends on miss distance | G-T2-5, G-T5-11 | ε active only where b < 1/Λ: none (≲ 2 keV), even crossings (3-20 keV), all (≳ 30 keV) | constraint (FASER) | weeks | low | WORTH A CHECK (low priority) |
| 20 | S-20 | Exclusive γγ → QQ̄ with PPS as a mass handle | G-T6-1 | 35 events at 500 GeV, 3 ab⁻¹ (before efficiency) | measurement | weeks | medium | WORTH A CHECK (post-discovery only) |

### S-1 The straight string is invalid at first order in F_ext; the causal Nambu-Goto string must be the only signal model
**Statement.**
- Every central-detector trajectory study integrates the Kang-Luty endpoint equation with an *instantaneous straight string* [1708.02243 Sec.II; 1911.02223 Eq.III.6-9; 2002.07503 Eq.VIII.1-4]. So do the public GNN samples [2410.00269 Sec.III], via the same Knapen-Papucci code.
- The analytic thickness formula is derived in that approximation [1911.02223 Eq.III.12].
- The usual justification, F_ext ≪ σ [0805.4642 Eq.3.10], controls angles, not the out-of-plane observables, which are themselves O(F_ext/σ).

**Evidence.**
- *Covariance.* The two straight-string prescriptions have 140-570 µm of frame dependence on a 150-190 µm signal. The causal null-vector string (the Athena algorithm) is covariant to 0.05 µm [T2 §5.1 table].
- *Energy.* The lab straight string does spurious work of −1.6 MeV per crossing in a pure B field [T2 §5.1].
- *Realistic events, 3.8 T.* Thickness ratios straight/causal are 0.04-60, and OT hits move by 0.2-35 mm [T2 §5.1, 4 events per Λ].
- *Material.* With MS kicks and B = 0, the lab straight string gives a fake thickness that grows with the number of crossings: 220-580 µm at 3-10 keV and 2.5-21 mm at 30 keV. The causal string gives 2-25 µm on the same events [T3 §3.1, G-T3-2].
- *Vacuum.* All methods are exact, and Li's closed form [2002.07503 Eq.II.4-8] is exact (≤ 3×10⁻¹⁴ ℓ_max) [T2 §2.1]. This is why the problem went unnoticed.

**Exploitation.**
- (c, e) Use the causal string everywhere: the CMSSW Geant4 port (W1, already planned), the fast propagator (W3, which is currently specified as a straight string), the GNN training samples, and the trajectory fit. A numba version exists and is validated: `T3_causal.py`, ~10³× faster than the Python port, 1-1.5 % step convergence [T3 §3.1].
- (e) Any recast of Knapen or Li efficiencies carries an unquantified O(1) model error in thickness-dependent cuts. In the core window it is probably small, because the causal pass fractions are 0.93-1.00 [T3 §3.2].
- (f) Paper (Sec. 5, P1).

**Effort:** days to adopt; 2-4 weeks for a paper. **Confidence:** high that the straight string fails; medium-high on the causal numbers, which are not yet cross-checked against the Athena C++ (Sec. 7). **Verdict: EXPLOIT.**

### S-2 Multiple scattering sets a 10-25 µm floor on the plane thickness
**Statement.**
- No published quirk propagation includes stochastic material effects. Knapen neglects material [1708.02243 Sec.II]. Li et al. include only the mean dE/dx with a 10 % smear [2002.07503 Sec.VII]. Evans-Luty "have not attempted to model" the transverse kicks [1811.08903 App.B].
- T5's upper bound of 50-400 µm [T5 G-T5-1] is superseded by the causal-string calculation with the reconstructed Phase-2 material.

**Numbers** [T3 §3.2, Tab.; 60 events per point for Λ ≤ 3 keV].
- Median Δs from MS alone: 11/15/22 µm at m_Q = 200/500/1000 GeV, nearly Λ independent (84th percentile ≤ 67 µm).
- MS dominates the B-field thickness for Λ ≳ 1.5-2 keV.
- Pass fraction of Δs < 100 µm (B + material): 0.93-1.00 for Λ = 1-30 keV.
- A Δs < 30 µm cut keeps 0.92-0.93 (200 GeV), 0.68-0.83 (500 GeV) and 0.55-0.67 (1 TeV) at 3-10 keV, and only 0.28-0.48 at 1 keV [T3 §9 item 3].
- Re-checked here:
  - Δs(M) = 17.6 µm (500 GeV) and 18.2 µm (1 TeV) at 3 keV with a new seed (quoted: 17 and 24) [S: S_spotchecks.py H].
  - √(x/X0) scaling verified: exponent 0.517 over material ×0.25-×4. Doubling the material gives ×1.41 (MS only) or ×1.45 (full material, 3.8 T) [S: S_msscale.py]. T3 had flagged this scaling as "untested numerically".
- **Mechanism** [T3 §3.2 items 6-7]. The kick is shared by the pair, so the pair direction turns by δp/|P_QQ̄|. In addition, the near-miss crossings convert part of the kick into a slow rotation of the oscillation axis, which makes the response non-linear in δp.

**Exploitation.**
- (c) The signal model, the Δs optimisation against PU 200, and the hit-association windows (max residual 35-65 µm at 3 keV) must include MS.
- (e) Material-budget uncertainty: ±20 % in x/X0 gives ±10 % on Δs (verified scaling). It matters only for cuts ≲ 50 µm.
- (d) MS sets the floor below which the thickness carries no Λ information (S-4).

**Effort:** days, once the real per-layer material is available. **Confidence:** medium, because the per-layer x/X0 is reconstructed (≈ 19 % X0 at η = 0, UNVERIFIED). **Verdict: EXPLOIT.**

### S-3 Plane-thickness physics: Λ^−1.9, m_Q-independent, non-linear in B at the crossings; revised window
**Statement.**
- The literature thickness d ≈ 1.16 µm (m_Q/100 GeV)(keV/Λ)⁴(B/T) [1911.02223 Eq.III.12] sets the strategy's lower window edge Λ_low ∝ m_Q^{1/4} [STRAT §4.4].
- The causal string gives a different scaling:

| m_Q [GeV] | Λ [keV] | causal B-only thickness (median) | formula |
|---|---|---|---|
| 200-1000 | 1 | 32-38 µm | 9-44 µm |
| 200-1000 | 3 | 3.9-5.2 µm | 0.1-0.55 µm |
| 200-1000 | 10 | 0.4-0.7 µm | ≤ 0.004 µm |

  - In words: ∝ Λ^−1.9 and nearly m_Q independent [T3 §3.2 item 3].
- T4 finds the same scaling for the *in-plane* B displacement, x_B ≈ 0.5 qBR/σ, i.e. Λ^−1.8…−2 and m_Q independent [T4 §3.2]. T2's 4-event study gave Λ^−2.5 at 2-5 keV [T2 §5.1], superseded by T3's statistics.
- T4 found the response non-linear in B: vacuum + linear-in-B misses 30-45 % of the effect [T4 G-T4-4]. This synthesis confirms it and locates its origin (Sec. 2, T-3):
  - the response is exactly linear (ratio 1.000) for every hit recorded before the first crossing;
  - after the first crossing the non-linearity is 31-35 % (PS/2S, 1 keV), for steep and near-tangent crossings alike, in rφ and out of plane;
  - it is converged between max_boost 10⁻² and 10⁻³ to < 1 %;
  - the response per unit B grows like 1 + 0.11 ln(B_CMS/B) between B/1000 and B [S: S_Bnonlin.py, S_Bscan.py].
- **Interpretation (ESTIMATE, heuristic).** At a crossing the partner is offset transversely by b ∝ qB, so the string pulls transversely with σb/|x| while the longitudinal separation |x| → 0. The impulse ∫σ b/(v|t|) dt is log-divergent and is cut off at |x| ~ b. That gives (σb/v) ln(ℓ/b), i.e. a B ln(1/B) term.
  - With b ∝ B/Λ⁴ and ℓ ∝ 1/Λ², the log argument scales as Λ²/B. Write x ∝ ε_B[1 + c ln(Λ²/B)], with the measured relative coefficient c ≈ 0.08-0.11 [S: `S_Bscan.py`]. Then the local exponents are x ∝ B^{1−c} = B^0.89-0.92 and x ∝ Λ^{−2+2c} = Λ^−1.78…−1.84. These match the measured B^0.91 [T4 §3.2] and Λ^−1.76…−1.98 (median ≈ −1.9) [T3 §3.2; T4 §3.2].
  - First-order perturbation theory in F_ext/σ is therefore singular at the crossings. The formula captures the odd-crossing miss distance b ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] (Li's d_E [2002.07503 Eq.V.8]), not the plane thickness accumulated over the tracker.

**Revised window** [T3 §9].
- 50 % edge of the Δs < 100 µm finder: Λ_low ≈ 0.5/0.45/0.55→0.7 keV at 200/500/1000 GeV (B → B + material). That is inside the strategy's ×1.8 band, slightly lower, and flatter in m_Q.
- At 1 TeV the ≥ 90 % plateau starts only at Λ ≈ 2 keV, because of MS.
- The upper (merging) edges are unchanged.

**Exploitation.**
- (b, e) Replace the formula-based edges and the validation item V2 (STRAT §9.4) by causal-string efficiency curves.
- (c) Any analytic or perturbative fast model, including "vacuum + first-order B", must be calibrated against the full causal propagator.
- (f) Theory content for P1 (Sec. 5).

**Effort:** 1-2 weeks for an independent Nambu-Goto check through the crossings. **Confidence:** medium, since all causal numbers come from one algorithm, but three independent ports agree [T2, T3, T4 kernels]. **Verdict: EXPLOIT** (window and validation change); **WORTH A CHECK** (independent solver, analytic B ln B theory).

### S-4 Degeneracy theorem and measurement of (m_Q, Λ) after discovery
**Statement.**
- Hits, hit times and dE/dx depend on (m_Q, Λ) only through ℓ₀ = m_Q/Λ² and the velocities. This follows exactly from the scale invariance of the Nambu-Goto + point-mass action. The vacuum Fisher column for ln σ is ≤ 3×10⁻⁷ of the largest [T4 §2.1, §3.1].
- Only three things break the degeneracy: the recoil (MET = p_T(QQ̄)), the B field through ε_B = qB/σ, and material (∝ 1/m_Q).
- This corrects the literature hope that dE/dx [1708.02243 App.A] or crossing spacing and timing [T2 G-T2-4; T3 §6 item 4] measure m_Q or Λ.

**Numbers** (Cramér-Rao, MS included; T4 §4.3).

| Handle | per event | N = 30 events |
|---|---|---|
| +MET (realistic full set) | σ(m)/m 6-10 %, σ(Λ)/Λ 3-5 % | 0.9-1.2 % / 0.5-0.6 %, at every (m_Q, Λ) of the 3×3 grid |
| B only (no recoil) | σ(Λ)/Λ 16-20 % at 1 keV | 1.5-2.2 % at 1 keV; 17-29 % at 3 keV; unmeasured at 10 keV |

- With the MET, the systematic floor is the MET/JES scale (1-3 %, UNVERIFIED): δm/m ≈ δ_s and δΛ/Λ ≈ δ_s/2.

**Exploitation.**
- (d) The first quantitative answer to the open problem "parameter measurement after discovery" [T5 G-T5-7].
- (f) A paper (P2).
- (e) Remove "the trajectory fit measures m_Q and Λ" and "dE/dx measures the mass" from strategy language.
- For T1's GUT test (G-T1-7), a 1 % Λ measurement resolves the rung spacing Δα⁻¹ = 4.87 trivially. But see T-9: the GUT-favoured doublet leaves no tracker trajectory.

**Effort:** days to write up; weeks for a real fit with hit assignment and PU. **Confidence:** high (theorem), medium (CRB numbers: local bound, known assignment, no PU). **Verdict: EXPLOIT.**

### S-5 MET-strip alignment
- **Statement.** In vacuum the strip axis is exactly φ_pair. The B wobble is ≲ 2×10⁻⁴ rad and the hit-fit error 3×10⁻⁵ rad, so Δφ(MET, strip) is set by the MET resolution alone [T4 §5.1].
- **Numbers.**
  - |Δφ| < 0.15-0.25 rad keeps 95 % of the signal and rejects random planes by ×13 (σ⊥ = 35 GeV) to ×34 (σ⊥ = 15 GeV).
  - It also cuts the plane-seeding combinatorics by π/0.2 ≈ 16.
  - Re-run here: identical table [S: `T4_met.py`]. Independent estimate: π/(1.96 σ⊥/⟨p_T⟩) ≈ 19 for σ⊥ = 25 GeV, p_T ≈ 300 GeV.
- **Caveats.**
  - Apply the Δφ(jet, MET) cleaning first [T4 §5.1].
  - The rejection constrains φ only.
  - A lowered L1 MET threshold (STRAT P2) brings softer pairs, so δ₉₅ grows as 1/p_T.
  - The PU-200 PUPPI resolution is UNVERIFIED.
- **Verdict: EXPLOIT.** Days. Confidence high.

### S-6 Timing: medians, per-layer losses, multiple hits per layer
- **Statement.** The strategy's delays (BTL 6/16/33 ns) use the median γ* at a fixed p_T(QQ̄) = 250 GeV [STRAT §4.2, §10.4]. With the real falling p_T > 200 GeV spectrum the medians are **3.5/9.6/18.7 ns**. The quoted values are the 84th percentiles [T3 §6]. Re-derived here: 3.48/9.52/18.71 ns, with 84th percentiles 6.2/16.5/32.8 ns [S: S_spotchecks.py C].
- **Per-layer losses** (fraction of pair-CM crossings outside ±12.5 ns):
  - 500 GeV: 2S1/2S2/2S3 = 7/17/33 %;
  - 1 TeV: PS3 27 %, 2S 44/57/68 %;
  - per hit, including repeated crossings: 2S 21 % (500 GeV) and 70 % (1 TeV).
- **Hits per layer.** Heavy, slow pairs give ≈ 3 hits per IT/PS layer (1 TeV), and 2.8-3.2 per layer at 500 GeV [T3 §6; T4 §6]. That is the norm, not the "10-20 % of events" of [2002.07503 Tab.I] quoted in STRAT §4.2.
- **Oscillation-induced spread.** The oscillation spreads hit times by > 1 ns only for Λ ≲ 0.5 keV.
- **BTL double hits.** These would measure the crossing period Δt_c. Per S-4 that is ℓ₀, not Λ: WORTH A CHECK (TOFHIR double-hit capability).
- **Verdict: EXPLOIT** (correct STRAT and OQ Q11). Confidence high (exact kinematics; barrel |z| acceptances UNVERIFIED).

### S-7 Causal 9-parameter global fit, quirk-hypothesis χ² and two-regime seeding
- **Statement** [T4 §2, §5.2, §6].
  - Model: 9 parameters (z₀, P_QQ̄, γ*, CM axis, m_Q, Λ) plus MS kinks, against 50-130 measurements.
  - Linear only within 2-10 % of an oscillation cycle at the last layer, with an aliasing minimum at 10 keV. So: no Kalman filter. Use a global Gauss-Newton fit with a phase-scan seed.
  - Prediction of each OT hit after the IT: 15-55 µm (1σ), against strips 0.5-24 mm wide at 1-3 keV. That is ×20-100 rejection per OT layer at 1 keV (×10⁵-10⁸ for 4 layers), ×2-10 at 3 keV, and none at 10 keV.
  - Seeding: resolved arcs for Λ ≲ 1 keV, an aliased zig-zag band through the PV for Λ ≳ 3 keV. Separation is non-monotonic in r in 98-100 % of events.
- **Caveat.** Idealised: known hit-to-quirk assignment, no PU. The rejection must be measured with real assignment (Phase 2/3).
- **Verdict: EXPLOIT** (design of approach (a)). Weeks. Confidence medium.

### S-8 Stopped-pair delayed annihilation (and an ISR-triggered coincidence)
- **Statement.**
  - The stopped pair dissipates its internal energy in ≈ 0.07-0.2 µs (range 0.02-0.5 µs), then annihilates with ~2m_Q of mostly visible energy [T6 G-T6-4]. Evans-Luty recast this for 38.6 fb⁻¹ [1811.08903].
  - T3 computed f_stop with the causal string for the first time:
    - inclusive pairs: **1.0 ± 0.3 % in EB+HB (|η| < 1)**, 6-9 % in any calorimeter, ≈ 10 % anywhere; flat for Λ = 0.3-3 keV;
    - p_T > 200 GeV (triggered) pairs: 0 % at 200-500 GeV, and 1.3-2.5 % (fiducial) / 10-12 % (anywhere) at 1 TeV.
    - ×2 model band [T3 §7, §7.1].
- **Reach (3 ab⁻¹, 3 events, T6 yield model).** This resolves T-5:
  - EB+HB only: ≈ 0.65 TeV;
  - full calorimeter: ≈ 0.9-1.0 TeV, assuming the Phase-2 endcap can be used in empty-BX triggers (UNVERIFIED).
  - Compare the tracker reach of ≈ 1.1-1.2 TeV for 0.6-15 keV (zero background) [STRAT §6.1].
- **Value.** The search is ISR-free and tracker-free. It covers Λ < 0.3 keV, and plausibly Λ > 30 keV, where the coplanar search is blind. Flat stopping above 1-3 keV is not computed (Sec. 7).
- **New coincidence channel.** At 1 TeV, 1.3-2.5 % of the MET-triggered events stop in the barrel calorimeter 0.1-0.4 µs later: a prompt ISR+MET event followed by a delayed deposit at the extrapolated position. WORTH A CHECK (needs delayed readout).
- **Verdict: EXPLOIT** (complementary analysis / pheno paper P3). Weeks. Confidence medium.

### S-9 Athena step-count killer
- **Statement.** `QuirksPreInclude` attaches `MonopoleLooperKiller` with MaxSteps = 2×10⁶ (BSM_Only). The quirk stepper takes ≈ 150-200 G4 steps per crossing, and N_cross ≈ 24 (Λ/keV)² in a CMS-size tracker. So a naive port kills quirks inside the tracker for Λ ≳ 24 keV [T2 G-T2-2].
- **Status.** SREQ W1 item (v) already requires an exemption from looper killers. This entry quantifies why. For FASER (≈ 10⁵ crossings at 100 keV) the impact is possible but UNVERIFIED.
- **Verdict: EXPLOIT** (configuration), hours. Confidence medium.

### S-10 The merged pair is a 9-21× MIP object, not 2× MIP
- **Statement.** "≥ 2× MIP" comes from FASER (relativistic pairs) [2607.26195] and D0. For the central p_T > 200 GeV sample the merged pair (Λ ≳ 30 keV) deposits a median 9× MIP (500 GeV) and 21× MIP (1 TeV). That is 1.5-1.8× one HSCP at the same β, and 0.75-0.9 of two HSCPs at β_cm [T3 §8].
- **Exploitation.** An HSCP-like high-Λ category (IT ToT, MTD 1/β, OT HIP bit). It is distinguishable from |q| = 2 (4× at the same β) only with β. A CMS HSCP recast [2410.09164] is possible, but strip cluster cleaning rejects partially merged pairs.
- **Caveat.** IT ToT saturation (UNVERIFIED range).
- **Verdict: EXPLOIT** (strategy correction); **WORTH A CHECK** (recast). Days. Confidence medium.

### S-11 Λ conventions and closed-form kinematics (documentation)
- **Λ convention** [T1 G-T1-1, T5 G-T5-4].
  - Lattice T_c/√σ = 0.709 (SU(2)) and 0.646 (SU(3)); m₀/√σ = 3.78 / 3.41; Λ_MS/√σ = 0.581 / 0.542 [T1 Tab.].
  - The cosmology paper's "Λ = 1 keV" (T_c) is √σ = 1.41 keV for SU(2), not 1/0.6 = 1.67 keV (TH §0(d), §1.1, §6.1).
  - A 1-loop "Λ" read as √σ is off by ×8.
- **Closed forms** [T2 §2.2].
  - ℓ_max = 3.947 cm (γ*−1)(m/100 GeV)(keV/Λ)²;
  - N_osc = σR/(2β* p_T) ≈ 12 (Λ/keV)², m_Q independent;
  - the shorthands "2 cm (γ−1)" (×0.5) and "1 cm (m/100)" (×0.4-2.7 per event) should not be used.
- Re-derived here (Sec. 3). **Verdict: EXPLOIT**, hours, high confidence.

### S-12 Mean energy loss is a first-order trajectory effect
- **Statement.** The mean ionisation loss drifts the oscillation phase. That shifts OT hits by 40-180 µm (200-500 GeV) and 0.3-1.5 mm (1 TeV) [T4 §2.3, G-T4-7]. A 10 % material error therefore moves OT hits by 4-150 µm.
- **Exploitation.** (e, c) The material scale is a fit nuisance and a signal-efficiency systematic for any χ²/GNN using OT positions. As a mass handle it is limited to the material precision (≈ 10 %).
- **Verdict: WORTH A CHECK.** Days. Confidence medium (thin-scatterer Bethe; straggling not in the phase study).

### S-13 Production modelling of the ISR tail
- **Statement.** The MET trigger selects the p_T(QQ̄) tail.
  - A fixed-p_T ISR kick biases ℓ_max by −10 to −25 % and N_osc by +20 % [T2 §3].
  - Two groups differ by 37 % in mass reach on the same benchmark, largely from ISR/K-factor handling [T5 I2].
  - FASER needed an ISR reweighting [2607.26195 p.3].
- **Status.** STRAT §12 already plans LO-MLM vs NLO-FxFx and ISR variations. Add: generate with a V+jet matrix element, never a fixed-p_T kick (fast scans included).
- **Verdict: EXPLOIT** (already planned). Confidence high.

### S-14 GUT-ladder Λ strip and the invisibility of doublets
- **Statement.**
  - The only UV framework that lands Λ in the CMS window is the SUSY-GUT ladder [0805.4642 Sec.2.5; 1012.2072] [T1 G-T1-2]:
    - SU(2), n_S = 3: √σ ≈ 0.8/2.6/6.4/15 keV at m_Q = 0.2/0.5/1/2 TeV, ×/÷3.9;
    - SU(3), n_S = 9: 1.5/5.9/16 keV.
  - Its EW quirks are doublets L plus coloured D. A singlet E spoils unification (T1, 1-loop).
  - Neutral naturalness predicts √σ ~ 2-40 GeV, not keV [T1 G-T1-6].
  - Doublet charged members decay with cτ = 7.9 mm, so the pair is neutral before the first pixel layer (survival to 3 cm ≤ 0.2 % at 200 GeV) [T6 G-T6-2; T3 §5; cτ re-derived here: 7.8 mm].
- **Consequence.** The theory-favoured representation gives a monojet + soft displaced pions signature, not a coplanar pair. Its rate is ×14 that of E (84 fb at 500 GeV, N_IC = 2). The coplanar search's motivation is the generic hidden sector (log-flat Λ: 6 % of a ×2 prior in α⁻¹ lands in the window, SU(2)) [T1 G-T1-3].
- **Exploitation.**
  - (a) Draw the ladder lines on the (m_Q, Λ) plot, labelled as doublet motivation.
  - (a) A compressed-higgsino-style monojet/soft-track recast with ×2N_IC rate. Limits not opened (UNVERIFIED).
  - Drop the "2 L points as tracker topology test" (OQ Q4) or replace them with this recast.
- **Verdict: EXPLOIT** (lines, honest motivation text); **WORTH A CHECK** (recast). Days. Confidence medium (ladder position ×2-4), low-medium (recast).

### S-15 Cosmology: a discovery implies a reheating bound
- **Statement** [T1 G-T1-4].
  - If the IC sector ever thermalised, the whole window is excluded: Ω_G h² ≈ 2-10 × (√σ/keV) and ΔN_eff(BBN) = 0.21 (SU(2)), 0.57 (SU(3)).
  - With UV freeze-in, a discovery implies T_max ≲ m_Q/25 and T_RH ≲ 5-35 GeV.
  - Glueballs are absolutely stable in the window (τ ≥ 10³⁵ s), so the BBN/CMB decay bounds do not apply.
  - T1's implementation differs from 2512.20696 Fig.4 by ×2.2 in T_RH,max (same slope). The abundance scales as T_RH^5, not T_RH^7, once the frozen-in gluons self-thermalise.
- **Checks here.**
  - ΔN_eff re-derived analytically (0.2135 / 0.5692).
  - The T⁵ exponent re-derived analytically: Z ∝ T⁷ and ξ³ ∝ Z^{3/4} give T^{21/4} = T^5.25, against T1's numerical 4.99, which includes the g*s(T) dependence.
  - T1's script re-run gives the same T_RH table.
  - The ×2.2 normalisation is NOT independently checked: it needs 2512.20696's code, which is not public.
- **Exploitation.** (a) An "implication" contour on the result plot. (f) A modest note correcting 2512.20696 for the E benchmark; contact the authors first.
- **Verdict: EXPLOIT** (figure, text); **WORTH A CHECK** (note). Confidence medium.

### S-16 Microscopic complement: Λ ≳ 3 MeV and the 0.1-3 MeV displaced band
- **Statement** [T6 G-T6-5].
  - For Λ ≳ 3 MeV the pair annihilates before the first layer. The spin-averaged BR(ee+μμ) is ≈ 18.5 %, so σ × BR(ℓℓ) = 1.1 fb at m_Q = 500 GeV.
  - Existing ATLAS dilepton limits (≈ 0.05-0.1 fb at 1.4-2 TeV; reading UNVERIFIED) probably exclude m_Q ≲ 0.8-1 TeV.
  - Λ ≈ 0.1-3 MeV gives displaced annihilation at 3 cm-10 km, depending on ε (which is a guess). No search covers it.
- **Exploitation.** (a) Scoping statement: the CMS tracker search should not claim Λ ≳ 1 MeV. (b) The displaced-annihilation band is a candidate new search, but it depends on ε and the J random walk (S-19).
- **Verdict: EXPLOIT** (scoping); **WORTH A CHECK** (band). Confidence low (UNVERIFIED limits; ε).

### S-17 Multi-charged singlets |q| = 2
- **Statement.**
  - σ ∝ q² exactly, plus γγ +18-21 %. The tracker reach would be ≈ 1.3 TeV, against ≈ 1.15 TeV for |q| = 1 [T6 G-T6-3].
  - ATLAS multi-charge limits (1060 GeV for |q| = 2) cover only merged straight tracks. Applicability is UNVERIFIED.
- **Correction (this synthesis).** T6 scaled Λ_low with the formula (d ∝ q/Λ⁴ ⇒ ×2^{1/4} = 1.19). With the causal scaling (thickness ∝ qB/Λ^1.9) Λ_low rises by ≈ 2^{1/1.9} ≈ 1.4, i.e. ≈ 0.65 keV at 500 GeV instead of 0.45 keV (ESTIMATE). The MS floor doubles (Highland ∝ |q|) to ≈ 22-44 µm, still below 100 µm. dE/dx is ×4, so expect more IT ToT saturation.
- **Verdict: WORTH A CHECK** (cheap sample). Confidence medium.

### S-18 Trigger and PU-200 realism (experimental; theory inputs only)
- **Theory inputs.**
  - Only 23-47 % of quirk OT crossings form 2 GeV stubs at Λ ≤ 3 keV (76-89 % at 10 keV), and the stubs do not form consistent helices. Quirks are largely invisible to L1 tracking [T4 §5.3, §6].
  - A φ-road cluster-pair multiplicity aligned with L1 MET φ is an L1-scouting idea (hardware feasibility not assessed) [T4 §5.3].
  - PU 200 has never been simulated for a quirk tracker analysis [T5 G-T5-3].
- **Verdict: WORTH A CHECK** (experimental track; months).

### S-19 ε (glueball emission per crossing) depends on the miss distance
- **Statement.** ε = 0.1 per crossing has no derivation. Emission needs b < 1/Λ [1811.08903 App.B.1]. In 3.8 T: none of the crossings for Λ ≲ 2 keV, the even crossings for 3-20 keV, all crossings above ≈ 30 keV [T2 §6.3]. This agrees with T5's estimate [T5 G-T5-11]. ε is irrelevant for the CMS tracker (≲ 0.1 GeV).
- **Exploitation.** An ε(b) parametrisation could relax FASER's 30-100 keV limits. That needs the J random walk in rock (T3 machinery).
- **Verdict: WORTH A CHECK**, low priority for CMS. Confidence low.

### S-20 Exclusive γγ → QQ̄ with PPS as a mass handle
- **Statement.** σ_excl = 0.012 fb at 500 GeV, i.e. ≈ 35 produced events with PPS-2 acceptance (S² = 0.8) [T6 G-T6-1]. Combined with γ* from the trajectory (0.03-3 % per event [T4 §4.2]) it gives m_Q independently of the MET scale. PPS-2 schedule and trigger are UNVERIFIED. Inelastic γγ is a +4.5-5.2 % correction relative to LO DY (4.0-4.2 % relative to the K-corrected DY; re-derived here).
- **Verdict: WORTH A CHECK** (post-discovery only).

---
## 2. Cross-report tensions, resolved

### T-1 "Precession is not a Λ meter" [T3] vs "the in-plane B displacement is a recoil-free Λ meter" [T4]
**Resolution: these are different observables, and the two reports agree.**
- T3 killed the *secular rigid rotation* of the fitted plane along the flight: the slope of the out-of-plane residual vs r. It is 3-18 µrad at 0.6-1 keV, ≤ 0.3 µrad at ≥ 3 keV, and below the MS-induced 4.5-10 µrad [T3 §4.2]. Canonical-momentum conservation makes the CM wobble bounded, so there is no first-order secular rotation [T3 §4.1].
- T4 uses the *whole non-rigid B displacement pattern*, mostly in plane: x_B ≈ 0.5 ε_B R ≈ 120 µm at 2S3 for 1 keV. It is profiled against the pair direction (which absorbs any rigid rotation) inside a 9-parameter fit [T4 §3.2].
- T3's own B-field *thickness* (the out-of-plane, non-rigid part) is listed by T3 as a surviving Λ handle for Λ ≲ 1.5 keV [T3 §4.2 "Λ handles that survive" (i)]. T4's B-only route works for Λ ≲ 2 keV and dies at ≥ 3 keV [T4 §3.2]. The two validity statements coincide.
- **Scalings agree.**
  - T3 thickness ∝ Λ^−1.9 and m_Q independent; T4 x_B ∝ Λ^−1.8…−2 and m_Q independent.
  - Both are ∝ ε_B = qB/σ. This is what the scale-invariance argument of T4 §2.1 requires: the B effect on positions enters only through ε_B R.
  - T2's Λ^−2.5 at 2-5 keV came from 4 events at fixed kinematics, and T2 called it "roughly". It is superseded.
- **Measured here** [S: S_Bnonlin.py, 1 keV]:
  - Q68 of the B displacement at the 2S layers: 68-137 µm in rφ and 66-124 µm along the vacuum-plane normal (before refit). After a refit the residual thickness is 32-38 µm [T3].
  - T4's "mostly in-plane" is therefore true after profiling, not before.
- **Remaining caveat.** T4's B-only Λ resolution assumes the causal model is right at the per-cent level at the crossings, where the response is non-linear (T-3), and that the charge q is known (ε_B measures q/σ). Both are acceptable for a post-discovery cross-check. Neither makes the B route a primary Λ measurement.

### T-2 B-field thickness: causal Λ^−1.9 vs the m_Q/Λ⁴ formula [1911.02223 Eq.III.12]
**Resolution: the causal numerics are right for the plane-fit thickness. The formula describes a different quantity, and its derivation (first-order perturbation of a straight string) fails at the crossings.**
- The formula's m_Q/Λ⁴ is the static polarisation of the yo-yo by the CM-frame field E* = γβ×B: offset ≈ qE*ℓ/σ ∝ qB m_Q/σ².
- This quantity exists in the exact dynamics as the **odd-crossing miss distance** b ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] (Li's d_E [2002.07503 Eq.V.8]).
- The plane-fit thickness over 10 layers is instead dominated by the accumulated transverse impulses at the near-miss crossings. These scale as (σb/v) ln(ℓ/b), i.e. as ε_B with a logarithm (T-3).
- The two coincide by accident near Λ ≈ 1 keV (T3: 32-38 µm vs formula 9-44 µm) and diverge as Λ grows: ×7-50 at 3 keV, ×100+ at 10 keV [T3 §3.2].
- **Practical consequences.**
  - The lower window edge is set where the two agree within ×2-4, so it moves little: 0.45-0.7 vs 0.54-0.81 keV.
  - Above ~2 keV, any analysis or validation item that uses the formula (STRAT §4.2, §5 O1 "d ∝ m_Q/Λ⁴", §9.1 "Δs scanned per Λ since d ∝ m_Q/Λ⁴", §9.4 V2) is wrong by large factors. Above ~1.5-2 keV the realistic thickness is MS dominated anyway (S-2).
- **Is the formula "from the straight-string treatment"?** Yes: 1911.02223 and 2002.07503 derive it by linearising the straight-string EoM about the vacuum yo-yo [T2 §5.1; T3 §13]. T2 shows that the straight-string prescriptions themselves give thicknesses ×0.04-60 off the causal value. So both the approximation and the perturbative expansion are uncontrolled at this order.

### T-3 "The causal string is non-linear in B, 30-45 % beyond first order; numerical artefact not excluded" [T4 G-T4-4]
**Checked here with the T4 kernel. Result: not a step-size or hit-matching artefact, generated at the crossings, and consistent with a B ln(1/B) term.**
- Code and outputs: `code/S_Bnonlin.py`, `code/S_Bscan.py`, plus an inline per-hit script; outputs in `figures/S_Bnonlin_out.txt`.
- **Reproduction.** T4's metric Q68|d(B) − 20 d(B/20)| / Q68|d(B)| at 1 keV is 0.31-0.35 (PS, 2S) and 0.16-0.19 (IT, which includes pre-crossing hits), for 500 and 1000 GeV, 6 events each. T4 quoted 30-45 %.
- **Step convergence.** max_boost 10⁻² → 10⁻³ with the step cap 0.01 → 0.002 cm changes the metric by < 1 % at 1 keV.
  - At 3 keV the converged value for steep crossings is 0.27-0.34.
  - T4's "all hits" numbers at 3 keV (0.36-0.65 at max_boost 10⁻²) are inflated by near-tangent crossings and by the 0.04-0.2 µm vacuum noise floor of the kernel, which matters because the B effect there is only 1-17 µm. Use ≈ 30 % as the 3 keV value.
- **Not a hit-matching artefact.** Steep crossings (|v_r|/|v_T| ≥ 0.5) show the same non-linearity as near-tangent ones. The out-of-plane component is equally non-linear (0.32-0.39).
- **Origin: the crossings.** Every hit recorded before the pair's first crossing has a response per unit B identical at B/10⁴, B/10³, B/20 and B (ratio 1.000, 3 events). Every later hit shows the effect.
- **Shape.** The response per unit B, relative to 3.8 T, is 1.15-1.19 / 1.32-1.38 / 1.45-1.51 / 1.83 at B/4, B/20, B/80, B/1000 (2S layers, 500 GeV, 1 keV). That is consistent with 1 + (0.10-0.12) ln(B_CMS/B), or B^−(0.08-0.09).
  - At B/10⁴ the displacement (~0.01 µm) is below the kernel's numerical floor and the ratio is erratic. Not usable.
- **Interpretation and cross-check of scalings.** See S-3. The B ln(1/B) term predicts the observed B^0.91 [T4] and Λ^−1.78…−1.84 [vs T3's −1.76…−1.98] from one logarithmic coefficient. That is a non-trivial consistency check.
- **Still open.**
  - The check uses the same algorithm (Athena port), so an algorithmic defect common to all ports at near-miss crossings is not excluded.
  - What argues against such a defect: T2's linearised-NG solution agrees with all methods up to the first crossing [T2 §5.1]; the causal string is covariant to 0.05 µm through several crossings [T2 §5.1]; momentum is conserved identically.
  - An independent Nambu-Goto solver through the crossings (e.g. a discretised world sheet) is the decisive test (Sec. 8, step 1).
- **Verdict.** G-T4-4 is upgraded from "WORTH A CHECK" to "**confirmed numerically, physical interpretation plausible (medium confidence)**". The practical conclusion stands: the fit and any fast model must run the full causal propagator; "vacuum + first-order B" is not a controlled model.

### T-4 Λ convention: T1 (0.709), T5 (0.71, 15 %) vs theory_signal_model (1/0.6)
**Resolution: T1 and T5 agree; theory_signal_model is wrong for SU(2) by 18 % (1.67 vs 1.41).**
- T1 uses the lattice value T_c/√σ = 0.7091(36) for SU(2) [hep-lat/0307017 Tab.6]. T5 uses Teper's fit 0.597 + 0.45/N² = 0.7095 [0912.3339 Eq.33]. Same number (re-derived here).
- The phrasing differs:
  - "15 %" [T1, T5] is the error on Λ when 1/0.6 = 1.67 is used instead of 1/0.709 = 1.41 (1.41/1.67 = 0.85);
  - "18 %" is the same statement the other way round (1.67/1.41 = 1.18);
  - "28 %" [T5] is the error on σ.
- The 0.6 of 2512.20696 is the N → ∞ value. Its m₀ = 6T_c is 13 % high for SU(2) (lattice 5.33 T_c = 3.78√σ) [T1 G-T1-1].
- **Effect on physics:** T_RH,max ∝ Λ^−0.21, so ≤ 4 % on the cosmology [T1]. Matters only for overlays.
- **Fix:** convert 2512.20696's Λ by 1/0.709 (SU(2)) or 1/0.646 (SU(3)); convert Λ_MS by 1/0.581 or 1/0.542.

### T-5 Stopped-pair yields: f_stop 1-6 % [T6] vs 1.0 ± 0.3 % [T3]
**Resolution: no contradiction in physics; different fiducial definitions and an assumed vs a computed number.**
- T6 took 1-6 % from Evans-Luty: 1-5 % in |η| < 1 at 400 GeV, ×3 for the full calorimeter [1811.08903 Fig.2, 6]. T6 did not compute it; its 1D toy failed [T6 G-T6-4].
- T3 computed it with the causal string, Evans-Luty material, and a simplified CMS field:
  - inclusive pairs: EB+HB |η| < 1 = 1.0 ± 0.3 %, at the lower end of Evans-Luty;
  - any calorimeter: 6-9 %;
  - anywhere: ≈ 10 %.
  - Model band ×2, dominated by the assumed low-p_T spectrum (⟨p_T⟩ = 30 GeV) and the outer geometry [T3 §7.1].
- **Updated reach.** Linear in f_stop; T6's yield model: σL × f_stop × 0.21 × 0.55 × 0.83 × BR_vis(0.4-0.65).
  - **CMS 1801.00359-like (EB+HB) Phase-2 search: f_stop ≈ 1 %**, i.e. 7-11 events at 500 GeV and 0.8-1.2 at 800 GeV. The 3-event reach is **≈ 0.65 TeV** (×2 band in f_stop: ≈ 0.55-0.75 TeV).
  - **Full-calorimeter search: f_stop ≈ 6-9 %**, reach **≈ 0.9-1.0 TeV**. This is only if HGCAL/HE empty-BX triggers are usable (UNVERIFIED), and the 21 % live fraction is the 2016 fill pattern (UNVERIFIED at HL-LHC).
  - The triggered (ISR) sample does not feed this channel at 200-500 GeV (0 % stop), but does at 1 TeV (S-8 coincidence).
- **Λ range of validity.** T3 found Λ independence between 0.3 and 3 keV. Evans-Luty is flat above 0.3 keV, computed to 1 keV. Extending "flat" to 30 keV-1 MeV, where the tracker search is blind, is plausible (the CM stops first) but not computed. De-excitation times grow to ms at 1 MeV [1811.08903 App.B].

### T-6 Timing: T3 medians vs strategy 16/33 ns
**Resolution: the strategy's numbers are correct for its stated assumption (fixed p_T = 250 GeV, median γ*), but that assumption does not represent the triggered sample.**
- With the falling p_T > 200 GeV spectrum the median BTL delay is 3.5/9.6/18.7 ns; 6.2/16.5/32.8 ns are the 84th percentiles [T3 §6; re-derived here, Sec. 3 C].
- STRAT C2 also noted that TH Tab.4.3 was internally inconsistent.
- **Two more effects push the loss up:**
  - per-hit losses exceed per-pair losses, because repeated crossings are later: 2S 70 % per hit at 1 TeV;
  - a lowered L1 MET threshold (P2) adds softer, slower pairs.
- The OI-1 conclusion ("2S lost at ≥ 500 GeV") is qualitatively right for the slow third of the sample; at 500 GeV the median pair loses only 2S3 at the 33 % level.
- Note: my first re-derivation used toa = t − R/c and disagreed by ~2 ns. The correct digitiser quantity is t − |r|/c with |r| = R cosh η (STRAT C8), and with it the numbers agree. T3 used the right definition.

### T-7 Multiple scattering: 50-400 µm [T5] vs 11-22 µm [T3]
**Resolution: T3 supersedes T5.**
- T5's number was an explicit upper bound: one kick turning the CM by θ/2, no plane fit, x/X0 1-3 % per layer assumed [T5 G-T5-1].
- T3's calculation brings three effects that reduce it ×5-20: the plane fit, the sharing of the kick within the pair (δp/|P_QQ̄|, not δp/p_quirk), and the string's restoring dynamics.
- Both used similar material, ≈ 19 % X0 at η = 0 in T3.

### T-8 Λ measurement from crossing period / BTL double hits [T2 G-T2-4; T3 §6 item 4, §4.2 handles (ii)-(iii)] vs the degeneracy theorem [T4]
**Resolution: T4 is right. Crossing spacing D, period Δt_c, amplitude and width all measure ℓ₀ = m_Q/Λ² and velocities, never Λ alone.**
- T2 itself notes that "the recoil p_T then gives m_Q", so T2 and T4 agree.
- T3 §6's phrase "direct Λ measurement" should read "direct ℓ₀ measurement". The BTL double-hit idea still has value: it fixes ℓ₀ independently of hit positions.

### T-9 GUT-favoured Λ [T1] vs tracker visibility [T3, T6]
**Resolution: real tension in the motivation, not in the physics.**
- The only UV framework that predicts the window (SUSY-GUT ladder) has doublet L quirks plus coloured D [T1 G-T1-2].
- Doublets go neutral before the first pixel layer (cτ = 7.9 mm) [T6 G-T6-2; T3 §5]. So the theory-favoured model gives no coplanar signature, and T1's G-T1-7 (testing α_IC = α_GUT through a measured Λ) cannot be realised with doublets: no trajectory, no ℓ₀.
- The singlet E coplanar search is motivated by generic hidden sectors (log-flat Λ). The GUT ladder motivates the monojet/soft-pion recast and the coloured-D searches (S-14).

### T-10 |q| = 2 window [T6] vs causal thickness scaling [T3]
- T6 raised Λ_low by 2^{1/4} using the formula. With the causal scaling and the doubled MS (Highland ∝ |q|), Λ_low rises by ≈ 1.4 (S-17). This is a minor correction to a WORTH-A-CHECK item.

### T-11 Hits per layer: "10-20 % of events with > 2 hits" [STRAT §4.2 from 2002.07503 Tab.I] vs ≈ 3 hits per layer [T3 §6, T4 §6]
- Li et al.'s fraction is for lighter, faster pairs. For m_Q ≥ 500 GeV and Λ ≥ 1 keV, T4 finds 2.8-3.2 hits per layer at 500 GeV and T3 ≈ 3 per IT/PS layer at 1 TeV.
- The radial component of the internal motion exceeds the radial CM velocity β_T ≈ 0.1-0.16. Plane finders must accept 3-4 hits per layer.

### T-12 MET-alignment factor: ×5-10 [T5 G-T5-10] vs ×13-34 [T4]
- T5 used generic windows of 0.3-0.6 rad. T4 computed the 95 %-efficiency window, 0.1-0.25 rad, from the MET resolution. Use T4.

### T-13 Straight string "good to 1-4 %" [TH §3.1] vs "uncontrolled at O(F_ext)" [T2, T3]
- TH compares the external force to σ (1-4 %). That bounds the bending angles, not the error on observables that are themselves O(F_ext/σ) [T2 §5.1 "order counting"].
- TH §5's "few % in the core window" for causal vs straight is therefore wrong. The numbers are ×0.04-60 on thickness and mm on OT hits.

---
## 3. Spot checks of headline numbers

All commands are run from `theory_track/`. "Independent" means a closed-form re-derivation or a new random sample;
"re-run" means the investigator's own script, which tests reproducibility only. Raw output:
`figures/S_spotchecks_out.txt`, `figures/S_Bnonlin_out.txt`, `figures/S_msscale_out.txt`.

| # | Number checked (source) | Method | Command | Result | Verdict |
|---|---|---|---|---|---|
| 1 | σ = 50.68 GeV/cm (Λ/keV)²; ℓ_max coefficient 3.947 cm [T2 §2.2] | closed form + ExactPair max separation | `pixi run python code/S_spotchecks.py 0` (A) | 50.68; 3.947; ExactPair/closed form = 1.0000 | PASS (indep.) |
| 2 | N_osc ≈ 12 (Λ/keV)², m_Q independent [T2 Tab.3.1] | N = σR/(2β* p_T) on the T2 LO DY+ISR cache, barrel or endcap exit | same (B) | 12.1 / 11.6 / 11.9 at 200/500/1000 GeV | PASS (semi-indep.: same event cache) |
| 3 | BTL median delays 3.5/9.6/18.7 ns; strategy 6/16/33 = 84th pct [T3 §6] | pair-CM toa = R/(β_T c) − R cosh η / c | same (C) | 3.48/9.52/18.71 ns; 84th: 6.2/16.5/32.8 ns | PASS (indep. formula; same cache). First attempt with t − R/c gave 5.4/11.5/20.7: my error, see T-6 |
| 4 | ΔN_eff(BBN) = 0.21 (SU(2)), 0.57 (SU(3)); ξ = 0.36 [T1 G-T1-4] | (4/7) g_d ξ⁴, ξ = (10.75/86.25)^{1/3} | same (D) | 0.2135 / 0.5692 / 0.3565 | PASS (indep.) |
| 5 | T_c/√σ = 0.709 (SU(2)), 0.646 (SU(3)); "1 keV T_c" = 1.41 keV √σ [T1, T5] | Teper fit 0.597 + 0.45/N² | same (E) | 0.7095 / 0.647 / 1.41 / ratio 1.18 | PASS (indep.) |
| 6 | γγ/DY = 4.5/4.6/5.2 % [T6] | ratio from `figures/T6_xsec_table.txt` | same (F) | LO/LO: 4.5/4.6/5.2 %; relative to K-corrected DY: 4.1/4.0/4.2 % | PASS (T6 ratio is LO/LO; the physically relevant fraction is 4.0-4.2 %) |
| 7 | Doublet cτ = 7.9 mm, Y = 0 triplet 6 cm [T6 G-T6-2] | Γ = c² G_F²|V_ud|² f_π² ΔM³ √(1 − m_π²/ΔM²)/π | same (F) | 7.8 mm; 57 mm | PASS (indep.) |
| 8 | Strategy Λ_low = 0.54/0.69/0.81 keV from the formula [STRAT §4.4] | invert 1.16 µm (m/100)(keV/Λ)⁴ × 3.8 = 100 µm | same (G) | 0.545/0.685/0.815 | PASS (but see T-2: the formula is not the physical thickness) |
| 9 | MS floor and B thickness at 3 keV: M = 17/24 µm, B+M = 15/25 µm, B = 4.9/3.9 µm (500/1000 GeV) [T3 §3.2] | causal string, Phase-2 material, **new seed and new events** (30 per point) | `pixi run python code/S_spotchecks.py 30` (H) | M 17.6/18.2; B+M 14.4/23.8; B 4.4/3.3 µm | PASS (indep. sample; same code) |
| 10 | Δs ∝ √(x/X0) ("×1.4 for ×2 material, untested") [T3 G-T3-1] | material ×0.25…×4, MS only, aligned random streams; plus ×2 with full material | `pixi run python code/S_msscale.py 40 500 3` | exponent 0.517; ×2 → ×1.41 (MS only), ×1.45 (full, 3.8 T) | PASS (new). Section H's per-event ratio of 0.83 used unaligned random streams: statistical, not physical |
| 11 | MET-strip alignment ×13-34 at 95 % eff. [T4 §5.1] | re-run, plus closed-form π/(1.96 σ⊥/p_T) ≈ 19 at σ⊥ = 25 GeV | `pixi run python code/T4_met.py` | identical table (×12.7-34.3) | PASS (re-run + order-of-magnitude indep.) |
| 12 | Non-linear B response, 30-45 % [T4 G-T4-4] | T4 kernel, B/80…B, two step sizes, steep vs shallow crossings, before vs after first crossing | `pixi run python code/S_Bnonlin.py 6 500,1000 1,3`; `pixi run python code/S_Bscan.py 3 500 1` | 31-35 % (1 keV), ≈ 30 % (3 keV, steep), converged < 1 %; linear before 1st crossing | PASS (confirmed; origin identified, T-3) |
| 13 | Freeze-in Ω ∝ T_RH^5.0 (not T⁷) [T1 G-T1-4] | analytic: Z ∝ T⁷, thermalised dark sector ⇒ n ∝ ξ³ ∝ Z^{3/4} ⇒ T^{21/4} | by hand | 5.25 vs T1 numerical 4.99 (g*s variation) | PASS (indep.) |
| 14 | T_RH,max table (e.g. 35.2 GeV at 600 GeV, 1 keV) [T1] | re-run `T1_cosmo.py` (output file restored) | `cd code && pixi run python T1_cosmo.py` | identical numbers | PASS (re-run only; the ×2.2 vs 2512.20696 is not independently checked) |

Count: sections A-H of `S_spotchecks.py` contain 30 individual assertions, all PASS. With rows 10-14 this gives
**35/35**. The f_stop numbers (T3 §7) were **not** re-run (hours of CPU). They are consistent with Evans-Luty at the
low end, and T3's 80-event and 400-event runs agree.

---
## 4. Implications for the experimental track (recommendations only; no file outside `theory_track/` was edited)

### 4.1 `phase1_strategy/outputs/STRATEGY_DRAFT.md`
| Section | Current text | Recommended change | Source |
|---|---|---|---|
| §1 item 3; §10.4 OI-1 "Facts" | "median delay at the BTL ≈ 16 ns (500 GeV), ≈ 33 ns (1 TeV)" | Medians 3.5/9.6/18.7 ns for the p_T > 200 GeV spectrum; 16.5/33 ns are the 84th percentiles. Per-layer fractions outside ±12.5 ns: 500 GeV 2S 7/17/33 %; 1 TeV PS3 27 %, 2S 44/57/68 %. Per hit: 2S 21 % (500 GeV), 70 % (1 TeV) | S-6; T3 §6 |
| §4.2 bullet 1 | "Straight-string EoM … good to ≲ 1-4 %" | "Causal Nambu-Goto string (Athena algorithm). Instantaneous straight strings are wrong at O(F_ext), the order of the thickness" | S-1 |
| §4.2 bullet 3; §4.4 lower edge; §5 O1 | thickness d ∝ m_Q/Λ⁴ (formula); Λ_low ∝ m_Q^{1/4} | Causal thickness 32-38 µm at 1 keV, ∝ Λ^−1.9, ~m_Q independent; MS floor 11/15/22 µm. Λ_low(50 %) ≈ 0.45-0.7 keV; ≥ 90 % plateau from ≈ 1 keV (200-500 GeV), ≈ 2 keV (1 TeV) | S-2, S-3; T3 §9 |
| §4.2 "10-20 % of events have > 2 hits per layer" | — | ≈ 3 hits per IT/PS layer for heavy pairs (1 TeV), 2.8-3.2 per layer at 500 GeV; accept 3-4 | T-11 |
| §4.2 "1-5 % stop in the calorimeters" | — | 1.0 ± 0.3 % (EB+HB, inclusive), 6-9 % any calorimeter, ≈ 10 % anywhere; 0 % for triggered 200-500 GeV pairs; 1.3-2.5 % (fiducial) for triggered 1 TeV pairs | S-8 |
| §4.3 regime map, last row; §9.1 "High-Λ category … ≥ 2× MIP" | "≥ 2× MIP" | Median 9× (500 GeV) to 21× (1 TeV) MIP for the central triggered sample; 1.5-1.8× one HSCP at the same β | S-10 |
| §5 O6 | "fit … measures (m_Q, Λ)" | Hits/time/dE/dx measure ℓ₀ = m_Q/Λ² and velocities only; m_Q from MET recoil (≈ 1 % with 30 events), B route only for Λ ≲ 2 keV | S-4 |
| §5 O7 | MET-plane alignment, no number | |Δφ(MET, strip)| < 0.15-0.25 rad: 95 % signal, ×13-34 random-plane rejection. Use it in the factorised background (f_MET-plane, D10), measurable in the low-MET CR, and as the seeding wedge (÷16 combinatorics). Apply Δφ(jet, MET) cleaning first | S-5 |
| §9.1 trajectory fit | "fit the straight-string EoM … analytic first-order solution as a fast seed" | Global Gauss-Newton fit with the full causal propagator (B and mean dE/dx inside; MS as broken-line kinks); vacuum closed form only as the IT seed; phase scan over ±1/N_osc; no Kalman filter | S-7; T4 §2.4 |
| §9.1 plane finder | "require ≥ 2 hits in ≥ N_min layers"; "Δs scanned per Λ since d ∝ m_Q/Λ⁴" | Accept 3-4 hits per layer. Do not scan Δs below ≈ 30 µm (MS floor; −30-45 % heavy signal); optimise Δs against PU-200 with MS in the signal | S-2 |
| §9.2 GNN training | "signal from the full CMS simulation" | Must be causal-string + material samples. The Zenodo 17941765 / Sha et al. trajectories are straight-string, no material: use them only for software plumbing, not as physics reference or training truth | S-1 |
| §9.4 V2 | "plane thickness vs the formula, within ×10" | Remove. A correct propagator fails it at Λ ≳ 3 keV (×7-50). Replace by the T3 causal-thickness table (with/without material) | T-2 |
| §9.4 V3 | "causal vs straight-string integrator with correct ŝ simultaneity" | Keep only as a demonstration that straight is wrong. Real validation: (i) vacuum vs ExactPair (≤ 10⁻⁸ ℓ_max); (ii) covariance test `T2_covariance_test.py`; (iii) momentum conservation; (iv) comparison with `T3_causal.py` (B and material) | S-1; T2 §10 |
| §9.4 V4 | "≈ 2-MIP charge for merged pairs" | FASER-specific (relativistic). At CMS expect 9-21× MIP | S-10 |
| §9.4 V5 | Zenodo trajectories comparison | Expect O(1) disagreement in thickness and mm in OT positions in B (straight string); agreement only in vacuum-like in-plane features | S-1 |
| §7 A2 L doublet "2 topology points" | — | Doublet pairs are neutral before the first pixel layer (cτ = 7.9 mm). Drop as a tracker benchmark; replace by a monojet + soft displaced pion recast (S-14). Keep E primary | S-14; T-9 |
| §12 Signal shape (i) | "Athena causal vs straight-string … few %" | Not a systematic: the straight string is wrong. The quirk-dynamics systematic is: causal-string numerics (≤ 1-1.5 %), NG validity (none at ≤ 30 keV), material budget (Δs ∝ √(x/X0), ±20 % ⇒ ±10 %; OT hit phase shifts 4-150 µm per ±10 %), B map (≤ 1-2 % at |η| < 1) | S-1, S-2, S-12; T3 §4.3 |
| §12 Signal shape (iii) | material ±5-10 % | Also through the mean-energy-loss phase drift: OT hits shift 40 µm-1.5 mm; the material scale is a fit nuisance | S-12 |
| §3 / §6 | motivation | Add: discovery ⇒ T_max ≲ m_Q/25, T_RH ≲ 5-35 GeV (implication contour); GUT-ladder lines for doublets (labelled); the window is generic-hidden-sector motivated, not neutral-naturalness | S-14, S-15 |
| §5/§10 (new observables) | — | BTL double hit (period ⇒ ℓ₀; TOFHIR capability), OT HIP bit for merged pairs, ISR + delayed calorimeter deposit at 1 TeV | S-6, S-8, S-10 |

### 4.2 `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md`
- **§1 P-S1 and §6 W3** ("fast numba propagator (straight string + B + Bethe-Bloch)"): use the causal algorithm. `theory_track/code/T3_causal.py` already provides it, with B, MS, mean dE/dx, straggling, hit recording and stop/exit, validated against ExactPair and T2, and ~10³× faster than Python. Offer it as the W3 starting point (licence: project-internal). This saves 1-2 weeks and removes an O(1) model error.
- **§1 P-S0 (Zenodo GNN samples):** straight-string, no material, no PU. Use them only as plumbing, never for efficiency or thickness numbers (S-1).
- **§2 S1-VAL (iii):** replace "causal vs straight string" with the validation set of §4.1 V3. Add a covariance check with a boosted pair in a pure E field (`T2_covariance_test.py`).
- **§6 W1 (v):** keep the looper-killer exemption. Quantified: MaxSteps 2×10⁶ kills quirks for Λ ≳ 24 keV in a CMS-size tracker (S-9). Also check the G4 `DistChord() = 0` chord error [T2 §5.1 table].
- **§6 W1 (ii):** `G4hMultipleScattering` is required. MS is the dominant thickness source for Λ ≳ 1.5-2 keV (S-2). Validate the MS thickness against `T3_ms_thickness.py` at 3 and 10 keV.
- **§6 W8 (GNN):** training truth must come from causal + material samples (S-1, S-2). Train on 3-4 hits per layer.
- **Grid (STRAT §7, TH §7):** no change needed. 0.3/0.6/1/2 keV bracket the revised edge. Consider adding Λ = 0.45 keV at 500 GeV if the edge matters for the limit.

### 4.3 `research/theory_signal_model.md`
- **§0 item 4a, §4.2 Tab.4.2b, §4.4:** replace the formula thicknesses with the causal table (T3 §3.2) and the revised window (T3 §9).
- **§0 item (d), §1.1 "Warning", §6.1 "~1.7 keV":** use 1/0.709 (SU(2)) or 1/0.646 (SU(3)), so their keV is √σ = 1.41 keV (S-11, T-4). m₀ = 3.78√σ for SU(2) (3.6 is SU(3)).
- **§3.1:**
  - "straight-string approximation good to ≲ 1-4 %" → controlled only for angles, uncontrolled for the thickness (T-13);
  - the thickness formula → "odd-crossing miss distance; not the plane-fit thickness" (T-2);
  - "Knapen Δφ … accumulates" → bounded (T3 §4.1-4.2).
- **§3.5 step 2 (i):** "the string force with correct CM simultaneity, *or* the causal-string equivalent" → causal string only.
- **§4.3:**
  - Tab.4.3 timing → T3 medians and 84th percentiles;
  - merged "≥ 2× MIP" → 9-21× MIP;
  - stopping 1-5 % → 1.0 ± 0.3 % (EB+HB) etc.;
  - "> 2 hits per layer in 10-20 %" → ≈ 3 per layer for heavy pairs.
- **§5, string-dynamics row:** "few % in core" → not a systematic (T-13). Add material/energy-loss phase-drift systematics (S-12).

### 4.4 `phase1_strategy/outputs/OPEN_QUESTIONS.md`
- **Q4:** recommend (b) E + Ẽ, without the "2 L points" (S-14).
- **Q9:** the three-category Λ range stays. The low-Λ boundary is ≈ 0.45-0.7 keV at 50 % efficiency, and the 1 TeV plateau starts at ≈ 2 keV.
- **Q10:** strengthen. The merged pair is 9-21× MIP, a strong HSCP-recast handle. Add the stopped-particle recast of CMS 1801.00359 with f_stop(EB+HB) ≈ 1 % (S-8), and a doublet monojet recast (S-14).
- **Q11:** update the medians (9.6/18.7 ns). The 30 % loss threshold is crossed at 1 TeV (2S 44-68 % per pair, 70 % per hit) and only at 2S3 at 500 GeV.

### 4.5 New complementary channels (ranked by value/effort for CMS)
1. **Stopped-pair delayed annihilation** (Phase-2 projection; Run-2/3 recast of 1801.00359): ≈ 0.65 TeV (EB+HB) to ≈ 0.9-1.0 TeV (full calorimeter). It is ISR- and tracker-free, so it covers the Λ edges (S-8).
2. **High-Λ HSCP-like category** (merged pair, 9-21× MIP, MTD 1/β, OT HIP bit): covers 20 keV to ≳ 100 keV, which FASER covers only to ≈ 180 GeV (S-10).
3. **Doublet monojet + soft displaced pions** (compressed-higgsino-like, ×14 the E rate): the GUT-motivated representation (S-14).
4. **ISR + delayed deposit coincidence** for 1 TeV triggered pairs (1.3-2.5 %): needs delayed readout (S-8).
5. **Displaced annihilation band** Λ ≈ 0.1-3 MeV, plus a statement that Λ ≳ 3 MeV is a dilepton/diphoton-resonance target (S-16).

---
## 5. Publishable outputs

A CMS member may write phenomenology papers, but none of these may use CMS-internal information: the Phase-2 material, PU-200 MET resolution and detector timing must come from public TDRs or generic detectors. Confirm the policy with the conveners (OQ Q2, Q13; UNVERIFIED).

| ID | Working title | Content available now | Needed for publication grade | Effort | Value |
|---|---|---|---|---|---|
| **P1** | "Quirk trajectories need the causal string: straight-string propagation fails at first order in external forces" | Covariance test (0.05 µm vs 140-570 µm) [T2 §5.1]; spurious work per crossing; thickness ×0.04-60 and OT hits 0.2-35 mm in B [T2]; fake MS thickness 0.2-21 mm [T3 §3.1]; causal thickness ∝ Λ^−1.9 vs formula Λ^−4; B ln(1/B) non-linearity from near-miss crossings (S-3, T-3); MS floor 10-25 µm with √(x/X0) scaling (S-2); revised coplanar window | (i) An **independent Nambu-Goto solver through the crossings** (discretised world sheet or Artru-type piecewise-linear string with exact field kicks). (ii) A run of the **Athena C++ standalone** on common events (port fidelity). (iii) An analytic derivation of the crossing impulse (σb/v) ln(ℓ/b) and its coefficient. (iv) ≥ 200 events per point; a generic detector or public Phase-2 material. (v) Cite and credit the ATLAS Athena `Simulation/G4Extensions/Quirks` code (Apache-2.0; authors from its headers, J. Black 2014 for QuirkTransportation) and FASER [2607.26195]; Kang-Luty [0805.4642]; Li et al. [1911.02223, 2002.07503]; Knapen et al. [1708.02243]; Sha et al. [2410.00269]. Contact the Athena/FASER quirk authors before submission | 3-5 weeks | **High.** It changes every central-detector quirk prediction and the GNN training practice |
| **P2** | "Measuring the quirk mass and string tension: a degeneracy theorem and the recoil" | Scale-invariance theorem; Fisher/CRB tables (MET route 1 %/0.5 %, B route ≤ 2 keV); MET-strip alignment (×13-34); predictive χ² (×20-100 per OT layer); linearity window and aliasing [T4] | A real fit (Gauss-Newton) on simulated events with hit-assignment ambiguity, PU hits and MS, to show the CRB is reached. Public MET-resolution assumptions. Optionally the exclusive-γγ PPS mass handle. Could be merged into P1 as a long paper | 3-6 weeks (after P1 code) | Medium-high. First answer to a problem open since 2017 [1708.02243 Sec.IV] |
| **P3** | "Stopped quirks at the HL-LHC" | f_stop with the causal string (inclusive 1.0 ± 0.3 % EB+HB; triggered 1 TeV 1.3-2.5 %) [T3 §7]; dissipation times; annihilation BRs and yields [T6 G-T6-4]; the ISR + delayed coincidence | 3D CMS geometry with field map, from public sources; Λ up to 100 keV-1 MeV, including de-excitation times [1811.08903 App.B]; HL-LHC bunch structure and live fraction; backgrounds (cosmics, halo, noise) from 1801.00359 scaled; a better low-p_T spectrum (NLO+PS) | 1-2 months | Medium. A clean complement; partly a refresh of Evans-Luty, so novelty is moderate. Could instead become a CMS-internal recast |
| P4 | "Cosmology of the mesoscopic quirk window" (note) | T_RH,max map, T⁵ scaling, ×2.2 vs 2512.20696, escape routes, ΔN_eff [T1 G-T1-4] | Resolve the ×2.2 with the 2512.20696 authors (g*s dilution suspected); re-derive the dim-8 freeze-in matrix element | 2-3 weeks | Low-medium. Best as a comment/erratum request or a section of P1/P3 |
| P5 | "GUT-motivated doublet quirks at the LHC: invisible pairs and monojet limits" | GUT-ladder strips (SU(2) n_S = 3: 0.8-15 keV) [T1 G-T1-2]; doublet cτ, rates [T6 G-T6-2] | A recast of current compressed-higgsino monojet/soft-track limits (not opened); coloured-D limits; check whether the string modifies the soft-pion kinematics | 2-4 weeks | Low-medium |

Recommended order: P1 first; then P2 (it reuses P1's code). P3 only if the experimental team does not take the stopped-particle recast in-house.

---

## 6. Killed ideas (consolidated)

| Idea | Killing number | Source |
|---|---|---|
| Plane precession in B as a Λ meter | secular rotation 3-18 µrad (0.6-1 keV), ≤ 0.3 µrad (≥ 3 keV), below the MS-induced 4.5-10 µrad | T3 §4.2 |
| Thickness ∝ m_Q/Λ⁴ as the Λ (or m_Q) meter | the informative B term is ∝ qBR/Λ² (m_Q independent); formula ×7-50 off at 3 keV | T3 §3.2; T4 §3.2 |
| dE/dx (or MTD timing) as a mass handle | measures βγ only; adding IT dE/dx changes σ(m_Q) by 0 % (Fisher rows M2 → M3) | T4 §8 |
| "Positions alone measure m_Q and Λ" | vacuum ln σ Fisher column ≤ 3×10⁻⁷ of the largest (exact scale invariance) | T4 §3.1 |
| Vacuum + first-order-B analytic fit model in the OT | misses 30-45 % of the B effect (confirmed: 31-35 % at 1 keV, converged) | T4 G-T4-4; S T-3 |
| Kalman filter with a two-point state | string memory; phase-linearity window ≤ 0.1 cycle while 3-300 oscillations occur between layers at ≥ 3 keV | T4 §2.4 |
| Midpoint of two quirk hits as a "CM track" | deviates by 35-50 % of the half-separation | T4 §6 |
| Instantaneous straight string with material kicks | fake thickness 0.2-21 mm (3-30 keV) vs 2-25 µm causal (the model is killed, not the effect) | T3 §3.1 |
| Lab-frame "simultaneity problem" in vacuum | all four methods agree to ≤ 2×10⁻⁸ ℓ_max; Li's closed form is exact | T2 §2.1 |
| Fixed-ŝ approximation | exact only in vacuum; no transverse restoring force once F_ext ≠ 0 | T2 §9 |
| Rotating component from DY spin | J ≤ 2.45ħ ⇒ J/(p*ℓ_max) ≈ 3×10⁻¹⁷ | T2 §4 |
| Capture or annihilation at crossings (CMS) | J ≥ 10⁶ħ from the first crossing in 3.8 T; Coulomb Born regime η ≈ 0.05 | T2 §5.3 |
| Relativistic yo-yo formula | γ* ≤ 2.0-2.5 at the 84th percentile; formula ×3-6 off | T2 §2.4 |
| Quantum spreading, string roughening, Larmor radiation, perturbative glueball radiation | 0.5 nm; 5 Å; 1.5×10⁻⁸ eV (Λ/keV)⁴ per crossing; ~10⁻²⁰Λ per crossing | T2 §6 |
| Effective-string (Lüscher) corrections, string breaking, quirk-quirk Coulomb | 10⁻⁸ at 1 µm; exp(−3×10¹⁶); α/(σd²) = 3×10⁻¹⁰ | T5 §7 |
| ε inside the CMS tracker | ≲ 0.1 GeV deposited | T2 §6.3; TH §3.3 |
| Delta rays, energy-loss straggling as thickness sources | recoil ≈ 0.2 MeV ≪ 5-15 MeV MS kick; force ∥ v ⊂ plane (B+E = B within statistics) | T3 §11 |
| B-field non-uniformity in the barrel | B_r/B₀ ≤ 0.9 % at |η| < 1 ⇒ ≲ 1-2 % on the thickness | T3 §4.3 |
| Doublet/triplet charged members as tracker quirk signatures | survival to 3 cm ≤ 0.2 % (doublet); to 15 cm ≤ 1.5 % (triplet, 200 GeV) | T3 §5; T6 G-T6-2 |
| Internal motion enhancing the merged-pair dE/dx | pair = 0.75-0.90 × two HSCPs at β_cm | T3 §8 |
| Hit-level dE/dx phase tagging | only 4 IT layers measure charge | T3 §8 |
| Inelastic γγ production as a signal boost | +4.0-4.2 % of the K-corrected DY (|q| = 1) | T6 G-T6-1; S check 6 |
| Exclusive γγ + PPS as a discovery channel | 35 events at 500 GeV before efficiency (~3 % of the main analysis) | T6 G-T6-1 |
| Spin as an acceptance driver | ≤ 25 % on the pair-axis acceptance | T6 G-T6-3 |
| Cosmic-ray, beam-dump, MoEDAL, MATHUSLA/CODEX-b/ANUBIS/FACET | kinematics or stopping in shielding | T6 G-T6-6 |
| Stellar cooling bounds | best m_Q > 1.5 GeV (SN1987A) | T1 §3 |
| Z → g′g′, e⁺e⁻ → γ + inv., light-by-light | BR ~ 10⁻¹²; Λ enters as (Λ/m_Q)⁴ ~ 10⁻³² | T1 §3 |
| BBN/CMB/γ-ray glueball-decay bounds in the window | τ ≥ 10³⁵ s for √σ ≤ 100 keV | T1 §3 |
| CMB-S4/SO ΔN_eff as a probe of the window | freeze-in ΔN_eff ~ 6×10⁻⁴ | T1 §3 |
| SIDM sub-component recalibration; cannibalism as a strengthening | ≤ ×1.6 and ×1.35 on T_RH,max | T1 G-T1-5, §3 |
| Banks-Zaks fixed point giving keV naturally | Λ/m_Q ~ 0.02 ⇒ GeV | T1 §3 |
| Neutral naturalness predicting keV quirks | predicts √σ ≈ 2-40 GeV | T1 G-T1-6 |
| Electron stripping / charge exchange in the tracker | needs β ≲ 0.01; triggered β_cm ≳ 0.1 | T5 §7 |
| Net-charged pairs as a current benchmark | no benchmark has a stable net-charged pair; the helicoidal sheet costs 1 parameter | T3 §5 |

---

## 7. Residual uncertainties and what is UNVERIFIED

1. **Phase-2 material per layer (most important).** The ≈ 19 % X0 at η = 0 is a reconstruction. The TDR and tkLayout pages could not be opened [T3 §2]. Only the TBPX module (0.72-0.95 %) comes from a primary source [2407.13721].
   - The MS floor scales as √(x/X0) (verified, S-2), so ×2 material gives ×1.4.
   - The energy-loss phase drift (S-12) and f_stop also depend on it.
2. **One algorithm behind all exact-string numbers.** T2 (Python), T3 (numba) and T4 (numba) are ports of the same Athena algorithm. They agree with each other to < 0.1 µm and with the exact vacuum solution.
   - Never cross-checked against the Athena C++ itself (G4 geometry, chord error with `DistChord() = 0`).
   - Never cross-checked against an independent Nambu-Goto solver after the first crossing.
   - The B ln B non-linearity and the Λ^−1.9 scaling rest on this.
3. **Small MC statistics.**
   - Thickness: 60 events per point (Λ ≤ 3 keV), 24 at 10 keV, 12 at 30 keV.
   - Window efficiencies: the 1 TeV, 1 keV value is 0.79 (24 events) vs 0.93 (60 events).
   - Fisher: 16 events per point.
   - Precession: 24 events.
   - Stopping: 80-400 events.
   - S checks: 6-40 events.
   - All "medians" carry 10-30 % statistical uncertainty.
4. **Idealisations in the measurement and reconstruction numbers (T4).** Local Cramér-Rao bounds; known hit-to-quirk assignment; no PU or noise hits; thin scatterers; no straggling in the fit; finite-difference noise of ±10 % at 10 keV.
5. **Experimental inputs used but UNVERIFIED.** PU-200 PUPPI MET resolution (σ⊥ = 15-35 GeV scanned) and JES/MET-scale floor (1-3 %); IT pitch, ToT range and saturation; OT sensor spacings and stub windows; BTL σ_t and TOFHIR double-hit capability; barrel |z| acceptances; the HL-LHC empty-BX live fraction (21 % is 2016).
6. **Kinematics.**
   - LO DY+ISR toy (CT18NLO), p_T(QQ̄) > 200 GeV, |η| < 1 or 1.5.
   - A lowered L1 MET threshold changes the timing and MET-alignment numbers (softer pairs).
   - f_stop depends on an assumed inclusive low-p_T spectrum (⟨p_T⟩ = 30 GeV): ×2.
7. **External limits not opened.** ATLAS dilepton limits at 1.4-2 TeV and diphoton limits (S-16); compressed-higgsino monojet/disappearing-track limits (S-14); CMS multi-charge HSCP limits (S-17); PPS-2 schedule (S-20).
8. **Cosmology.** Freeze-in matrix element taken from 2512.20696 Eq.26 without re-derivation. The ×2.2 discrepancy is unexplained (g*s suspected). O(1) strong-dynamics factors.
9. **ε model.** No derivation exists. ε(b) is a heuristic (S-19).
10. **GUT ladder.** Anchor-and-shift running, not a full threshold calculation; strip position ×2-4 [T1 G-T1-2].
11. **Recalled values.** Highland and Bohr formulas (PDG, recalled) [T3]; some glueball masses [T2 §6.3]; the Garcia-Kaneta-Mambrini-Olive reheating classification [T1].

---

## 8. Recommended next steps for the theory track (ordered)

| # | Step | Why | Effort |
|---|---|---|---|
| 1 | **Independent string check.** Run the Athena C++ standalone (`standalone/` app) on ~10 common events (vacuum, 3.8 T, 3.8 T + MS). Write an independent Nambu-Goto solver valid through crossings: discretised world sheet with massive endpoints, or the Artru piecewise-linear construction with exact field kicks. Compare thickness, B-linearity and the B ln B coefficient | Everything in S-1/S-2/S-3 and P1 rests on one algorithm | 1-2 weeks |
| 2 | **Hand `T3_causal.py` to the Phase-2 team as the W3 fast propagator.** Agree the hit/time output schema (SREQ §1 P-S1) | Removes the straight-string W3 plan; immediate value | 2-3 days |
| 3 | **Real Phase-2 material.** Get the per-layer x/X0 vs η (TDR, tkLayout; needs CMS access, i.e. the user) and re-run `T3_ms_thickness.py` at ≥ 200 events per point. Deliver the Δs-cut efficiency curves (20-150 µm) vs (m_Q, Λ) | The Δs optimisation against PU 200 needs them | 3-5 days |
| 4 | **Analytic crossing theory.** Derive the near-miss transverse impulse and the thickness coefficient (B ln B, Λ^−1.8). Predict the thickness without simulation | P1 content; replaces the wrong formula | 1-2 weeks |
| 5 | **Write P1** (S-1 + S-2 + S-3) | Highest-value publication | 3-4 weeks |
| 6 | **Stopped pairs for the Phase-2 projection.** T3_causal with the field map; full calorimeter including endcaps; Λ = 0.3-100 keV; triggered and inclusive samples; ISR + delayed coincidence | S-8; feeds OQ Q10 | 2-4 weeks |
| 7 | **Measurement demonstration.** Gauss-Newton fit on simulated hits with assignment ambiguity plus random PU hits, at 1/3/10 keV; compare with the CRB | P2; quantifies S-7 rejection realistically | 3-4 weeks |
| 8 | **Doublet monojet recast and GUT-ladder lines** | S-14; cheap motivation and constraint | ~1 week |
| 9 | **|q| = 2 window** with the causal string (thickness, MS, ToT) | S-17 | 2-3 days |
| 10 | **Cosmology note:** contact 2512.20696 authors about ×2.2 and T⁵ | S-15 | 1-2 weeks, optional |
| 11 | **ε(b) and J random walk in rock for FASER** (Λ ≥ 30 keV) | S-19; low CMS value | weeks, low priority |

Hand-offs that are not theory work: OI-1 timing (S-6), MET-alignment implementation (S-5), PU-200 random-plane background and L1 φ-road feasibility (S-18), HSCP recast (S-10).

---

## 9. Source map

| Claim in this document | Supported by |
|---|---|
| Straight string not covariant; spurious work; ×0.04-60; 0.2-35 mm | T2 §5.1 (tables), `T2_covariance_test.py`, `T2_string_methods_B.py` |
| Athena algorithm = exact NG for piecewise-null data; port validation 33/33 | T2 §5.1, §7; `T2_test_propagator.py` |
| Li closed form exact in vacuum; ℓ_max, N_osc closed forms | T2 §2.1-2.2; S check 1-2 |
| Straight string with MS: fake 0.2-21 mm; causal 2-25 µm | T3 §3.1, G-T3-2 |
| MS floor 11/15/22 µm; pass fractions; Δs < 30 µm losses | T3 §3.2, §9 item 3; S check 9 |
| √(x/X0) scaling of the MS thickness | S: `S_msscale.py` (check 10) |
| Causal thickness Λ^−1.9, m_Q independent, formula ×7-50 at 3 keV | T3 §3.2 item 3; T4 §3.2 |
| Odd-crossing miss distance 3.5 µm (keV/Λ)⁴ | T2 §5.3, §6.3 |
| Non-linear B response; origin at crossings; B ln B | T4 §3.2, G-T4-4; S: `S_Bnonlin.py`, `S_Bscan.py` (T-3) |
| Revised window 0.45-0.7 keV; 1 TeV plateau at 2 keV | T3 §9 |
| Degeneracy theorem; CRB numbers | T4 §2.1, §3.1, §4.3 |
| MET alignment ×13-34 | T4 §5.1; S check 11 |
| Causal fit, prediction 15-55 µm, linearity window, seeding regimes, L1 stubs 23-47 % | T4 §2.3-2.4, §5.2-5.3, §6 |
| Mean energy-loss phase drift 40 µm-1.5 mm | T4 §2.3, G-T4-7 |
| Timing medians 3.5/9.6/18.7 ns; per-layer losses; ≈ 3 hits per layer | T3 §6; S check 3 |
| f_stop 1.0 ± 0.3 % etc. | T3 §7, §7.1 |
| Stopped-pair yields and reach | T6 G-T6-4 table, rescaled with T3 f_stop (T-5) |
| Merged pair 9-21× MIP | T3 §8 |
| Doublet/triplet cτ, rates ×14/×37 | T6 G-T6-2, §2 table; T3 §5; S check 7 |
| γγ fraction, PPS exclusive | T6 G-T6-1; S check 6 |
| |q| = 2 rates and limits | T6 G-T6-3; correction in S-17 / T-10 |
| Λ ≳ 3 MeV resonance; 0.1-3 MeV band | T6 G-T6-5 |
| Λ conventions | T1 G-T1-1 (table); T5 G-T5-4, I1; S check 5 |
| GUT ladder; naturalness fractions; NN landscape | T1 G-T1-2, G-T1-3, G-T1-6 |
| Cosmology: thermal exclusion, freeze-in T_RH, T⁵, ×2.2, escape routes | T1 G-T1-4; S checks 4, 13, 14 |
| MaxSteps killer | T2 §5.1 table item 3, G-T2-2 |
| ε(b) | T2 §6.3, G-T2-5; T5 G-T5-11 |
| Literature census and assumption audit | T5 §2-4 |
| ISR-modelling sensitivity | T2 §3; T5 G-T5-5, I2 |
| Strategy, SREQ, TH, OQ pointers | the files and sections named in Sec. 4 |
