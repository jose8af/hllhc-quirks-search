# Critical review R1 of the C001 quirks theory track

Reviewer: R1-critical. I did not write any of the work under review. Date: 2026-10-08.

**Under review:** `outputs/THEORY_GAPS_SYNTHESIS.md` (S, DRAFT v1), `investigations/T1..T6_*.md` and `code/`.

**My code:** all scripts are in `code/R1_*.py`; their raw outputs are in `figures/R1_*_out.txt`. Run them from `theory_track/`
with `pixi run python code/<file>`. They share no propagation code with T2/T3/T4. The only exceptions:
- T2 `ExactPair` (an analytic closed form) is used as a vacuum reference;
- `T3_causal.run_causal` is used as the object under test.

**Classes:**
- **A**: makes a claim wrong or unpublishable, or misleads the experimental track.
- **B**: weakens a result; must be fixed.
- **C**: clarity or style.

---

## 0. Verdict

**ITERATE.** Counts: **3 A**, **8 B**, **9 C**.

What I independently confirmed:
- The causal (Athena-type) string is a faithful Nambu-Goto solver. An independent conformal-gauge solver agrees with it to 0.1-1 % on the
  thickness, 0.6-3 keV, 16 events.
- The B response of the exact string is non-linear after the first crossing: 29-39 % at B/20, about 1 + 0.10 ln(B₀/B).
- The causal B-only thickness scaling, the degeneracy theorem, the MET-alignment geometry, the T⁵ freeze-in scaling and the doublet cτ.

**The headline claim S-1 is not airtight. As written it is wrong for the published work it names.**
- T2's "lab-simultaneous straight string" (labSS) is labelled "≈ Li et al.", and every number in S-1 comes from it. **It is not Li et al.'s algorithm.**
- I implemented Li et al.'s algorithm literally [1911.02223 Eq.III.6-III.10 = 2002.07503 Eq.VIII.1-4]: CM-simultaneous stepping, ŝ by extrapolation along the quirk's own velocity, explicit Euler. Converged in step size, it reproduces the exact causal string to −16 %…+4 % in thickness at 0.6-2 keV.
- Including MS kicks, it gives no fake mm thickness: medians of 12-13 µm against 15-30 µm for the causal string. labSS gives 0.2-21 mm.
- So the "×0.04-60 thickness", "0.2-35 mm OT hits", "fake 0.2-21 mm with MS" and "140-570 µm frame dependence" are properties of two straight-string variants that T2 wrote. No published paper used them.
- What survives is a much weaker statement. The Li prescription is ≈ 15 % low in thickness. At the step bound Li et al. print (Eq.III.10) the Euler integration is not converged: thickness ×0.8-20 and hits off by mm to cm. We do not know the step they actually used. Knapen's code has not been seen.

---

## 1. S-1: straight string vs causal string (priority 1)

### A-1. The straight-string numbers in S-1 do not describe Li et al. (or, as far as anyone has checked, Knapen et al.). The claim that "published work is wrong at O(1)" is unsupported.

**Where:**
- Synthesis §0 item 1, S-1 (Statement and Evidence), T-2 last bullet, T-13, §4.1 rows §4.2/§9.2/§9.4 V3-V5/§12(i), §4.2 P-S0, §5 P1, §6 "Instantaneous straight string with material kicks", §9.
- T2 §1 item 3 and §5.1 (covariance table column "lab-simultaneous straight string (≈ Li et al.)", the realistic-event table, "Comparison with what the literature says").
- T3 §1 item 1, §3.1, G-T3-2.
- `T2_string_methods_B.py` docstring: "labSS … equivalent to the Li et al. prescription".

**What is wrong.** T2 checked that Li's ŝ construction [2002.07503 Eq.VIII.3-4] returns the lab-simultaneous direction *when fed the exact vacuum solution*. It then used `LabStraightString` as Li's method *with* external forces. With F_ext ≠ 0 the two prescriptions differ at exactly the order under discussion:
- Li et al. advance the two quirks at **different lab times**, kept CM-simultaneous by the step condition Eq.III.6-7: (x₁ − x₂)·P_q = 0, a Lorentz-invariant condition.
- They take ŝᵢ = Δr − Δt vᵢ. That is the lab-time-zero direction in the tangent plane spanned by uᵢ and the CM-simultaneous chord.
- So Li's prescription assumes the string is straight **in the CM frame**, and implements this covariantly.
- labSS assumes the string is straight on **lab** time slices, a frame-dependent choice no paper made.
- T2's second variant, `CMStraightString`, also differs from Li: it extrapolates positions linearly over the CM time offset, which Li avoids by co-evolving the quirks.

**Evidence (independent).**
- *Code:* `code/R1_li_literal.py`. Explicit Euler; per-quirk steps from Eq.III.7 (including dβ); ŝ from Eq.III.8-9; Kang-Luty force with lab v and ŝ, Eq.III.2; F_ext = qv×B; no dE/dx (as in T2 §5.1).
- *Events:* m = 500 GeV, γ* = 1.28, p_T = 300 GeV, 3.8 T. These are the same kinematics as T2's `make_event`, drawn with my own generator (seed 11).
- *Hits:* the 10 barrel radii.
- *Outputs:* `figures/R1_li_literal_out_a.txt`, `_b.txt` and `_c.txt` (`_c` is the 5 keV run). Thickness in µm; "Li ×f" means step = f × the Eq.III.10 bound.

| Λ | event | causal | Li ×1 (stated bound) | Li ×0.1 | Li ×0.01 | Li ×0.001 (×0.003 at 2 keV) | T2 labSS |
|---|---|---|---|---|---|---|---|
| 0.6 | 0/2/3/4/5 | 36.6/79.3/11.3/97.7/115 | 38/64.6/15.9/74.3/112 | 31.2/67.8/11.1/82.9/96.7 | 31/67.4/10.9/82.1/96.1 | 31/67.4/11.0/82.1/96.0 | 130/361/44/222/481 |
| 1 | 0/1/2/3/4/5 | 15.3/49.0/30.1/3.87/39.1/50.5 | 75/62/50/9.6/132/70 | 16.6/51.1/35.0/3.34/35.5/43.8 | 12.9/50.9/29.3/3.31/33.0/42.9 | 12.9/50.9/25.6/3.32/32.9/42.8 | 133/871/358/43/228/529 |
| 2 | 0/1/2/3/4/5 | 4.97/13.3/11.6/1.01/11.2/15.2 | 40/68/242/9.0/116/41 | 9.8/16.1/33.9/2.0/11.3/15.3 | 4.81/13.5/9.87/0.89/11.1/12.9 | 4.79/13.7/9.87/0.85/10.2/12.9 | 150/965/411/46/238/584 |

- **At 3 keV (event 0) the same pattern holds: causal 2.23, Li ×0.003 1.91 (0.86), labSS 143 µm. More 3 keV and 5 keV events
  were still running at sign-off; they append to `_b.txt` and `_c.txt`.
- **Converged Li / causal = 0.84-1.04 (median ≈ 0.85)****, apart from 2 events with a different hit count. That is about −15 %, consistent with T2's own rest-frame observation of ≈ 20 % causal-vs-straight amplitude differences at γ* = 1.3 (T2 §5.1 item 3).
- **labSS / causal = 4-60**.
- *OT hit positions:* converged Li vs causal, max over the event, is 27-80 µm at 0.6 keV and 27-430 µm at 1 keV. At 2 keV the Li hit phases are not yet converged at ×0.003 (0.2-10 mm). labSS gives 2-28 mm.
- *At Li's printed bound:* the thickness is off by ×0.8-20 and the hits by 6-250 mm. This is an Euler-convergence effect, not a covariance failure. Eq.III.10 is an upper bound ("should satisfy"), so the step Li et al. actually used is unknown.
- *With MS* (`code/R1_li_ms.py`; thin scatterers at T3's slab radii and x/X0; Highland; B = 0; 8 events; causal with T3's continuous MS and different random numbers, so only medians compare; `figures/R1_li_ms_out.txt`):
  - Li-literal + MS gives median 13 µm (1 keV) and 11.9 µm (3 keV);
  - causal + MS gives 30 µm and 15 µm (16-84 % ranges overlap);
  - there is no secular growth with crossings. T3's "fake 0.2-21 mm" (labSS) does not occur.
  - At 10 keV (first event): Li-literal + MS 15 µm vs causal + MS 28 µm, again no mm-scale thickness. The remaining 10 keV
    events were still running at sign-off and append to the same file.
- *Covariance:* every ingredient of Li's construction is a 4-vector statement. CM simultaneity is (x₁−x₂)·P = 0. ŝ is the lab-time-zero direction of the plane span(uᵢ, x₁−x₂). The converged prescription is therefore frame independent, apart from using the quirk-only P rather than quirks plus string. T2's frame-dependence column "(≈ Li et al.)" does not apply to Li.
- *Knapen et al. and Sha et al.:* 1708.02243 Sec.II says only "in the centre of mass frame, v∥ will lie along the displacement vector"; no implementation is given. Nobody on the track has seen the Knapen-Papucci code, which Sha et al. used [2410.00269 Acknowledgements]. If it implements CM simultaneity as Li does, it is ~15 % off, not O(1).

**Required fix.**
1. Rewrite S-1, §0 item 1, T-2, T-13, §4 and §6, and P1 to read: "lab-time-slice straight strings are badly wrong (×4-60); the CM-simultaneous straight string of Li et al. is a controlled approximation, ≈ 15 % low in thickness at 0.6-2 keV and ≲ 0.1-0.4 mm on OT hits at ≤ 1 keV, when step-converged; Li et al.'s printed step bound is not sufficient for convergence".
2. Remove "every published central-detector trajectory model is wrong at the order that matters".
3. Remove "Zenodo/Sha samples only for plumbing, expect O(1) disagreement" until the Knapen-Papucci code is inspected. Ask the authors; Sha et al. had it.
4. P1 as framed ("straight-string propagation fails at first order") is not publishable. A defensible note is "how good are straight-string quirk integrators: covariant CM-straight within ~15 %, lab-straight unusable, step convergence matters".
5. T2 and T3 must relabel labSS as "lab-time-slice straight string (not used in the literature)".

### A-2. The experimental-track recommendations built on A-1 would mislead Phase 2

**Where:**
- §4.1: §4.2 bullet 1 ("Instantaneous straight strings are wrong at O(F_ext)"); §9.2 ("Zenodo … use them only for software plumbing, not as physics reference"); §9.4 V5 ("Expect O(1) disagreement in thickness and mm in OT positions"); §12 Signal shape (i) ("Not a systematic: the straight string is wrong").
- §4.2 P-S0 and W8.
- §4.3 §3.1, §5.

**What is wrong.** With A-1 these become false statements to the experimental team. Comparing with the GNN samples would show ~15 % thickness differences, not O(1), and they would conclude the theory track was wrong. Conversely, the honest systematic "causal vs CM-straight ≈ 15 % on Δs" would be dropped from §12. The recommendation to use the causal string (`T3_causal.py`) as the production model stands and is good; it is now independently validated (B-confirmation below).

**Required fix.** Keep "use the causal string". Replace "straight string is wrong / not a systematic" with:
- (i) never use lab-time-slice straight strings;
- (ii) CM-straight (Li) differs from the causal string by ≈ 15 % on Δs; treat this as superseded, not as a systematic;
- (iii) validate any external sample against `T3_causal.py` before use.

### Confirmation (positive result, part (b) of the brief): the causal port IS Nambu-Goto with massive endpoints

**Code:** `code/R1_conformal_ng.py`, an independent formulation.
- The open NG string in conformal gauge, X = [A(τ+σ) + B(τ−σ)]/2, with endpoints at σ = 0, π.
- Endpoint equations, derived from the NG boundary condition:
  - dX/dτ = (u·w)u;
  - outgoing o = 2(u·w)u − w;
  - m du/dτ = T(w − (u·w)u) + qκ(u·w)(0, u⃗×B).
- Delay ODE wᵢ(τ) = o_{other}(τ − π), integrated with RK4 and 4-point Lagrange interpolation of the history.
- Canonical momentum (quirks + string − Σ qκ X×B) is monitored.

**Comparison** with `T3_causal` (max_boost 10⁻³, h 0.02 cm), same events, matched hits (`figures/R1_conformal_ng_out.txt`):

| Λ [keV] | events | thickness conformal / causal | max out-of-plane hit difference | max hit difference |
|---|---|---|---|---|
| 0.6 | 4 | 0.9992-0.9994 | ≤ 0.23 µm | ≤ 0.31 µm |
| 1 | 4 | 0.9991-1.0040 | ≤ 0.17 µm | ≤ 0.17 µm |
| 2 | 4 | 0.9935-1.0010 | ≤ 0.36 µm | ≤ 5.9 µm |
| 3 | 4 | 0.990-0.997 | ≤ 0.14 µm | ≤ 8.2 µm |

- **Vacuum:** before the first crossing it matches the exact solution to 6×10⁻⁴ µm.
- **Momentum conservation:** canonical P is conserved to ≤ 2×10⁻³ GeV at convergence. One 3 keV event is not converged at N = 9216 (drift 106 GeV), but its matched thickness still agrees to 0.3 %.
- **Formal note:** in conformal gauge a point-like crossing (b → 0) costs infinite τ. The vacuum yo-yo is therefore singular in this gauge, and that is why only the pre-crossing vacuum test is possible. This is the same singular structure that makes first-order perturbation theory fail at the crossings (S-3).
- **Verdict:** S-1 part "Athena algorithm = exact NG (port faithful)" is **confirmed** at ≤ 1 % on thickness, ≤ 0.4 µm out of plane. This answers synthesis §7 item 2 and step 1 of §8, apart from the C++ comparison.

### B-1. "Exact" means exact classical NG with point endpoints, not exact physics. The near-miss crossing physics is log-sensitive to a cutoff the EFT does not control.

**Where:** S-1 ("exact Nambu-Goto"), S-3 / T-3 interpretation, T2 §5.1.

**What is wrong.**
- The thickness comes from transverse impulses ∝ (σb/v) ln(ℓ/b) (S-3 heuristic). These involve separations down to b.
- The NG string is an EFT valid for separations ≫ 1/Λ (≈ 2 Å/(Λ/keV)). The odd-crossing miss distance b_odd ≈ 3.5 µm (keV/Λ)⁴ [T2 §5.3] is below 1/Λ only for Λ ≳ 20 keV. The even crossings have b < 1/Λ already at Λ ≥ 3 keV [T2 §6.3 table].
- Impulses ∝ b make even crossings subdominant, so the effect is probably small for Λ ≲ 10 keV. It is a model uncertainty of order ln(1/(bΛ))/ln(ℓ/b) ~ 10-30 % for Λ ≳ 10-20 keV.

**Required fix.** Write "exact classical NG with point masses" and add a one-line NG-validity caveat at the crossings for Λ ≳ 10 keV. Synthesis §6 "NG validity (none at ≤ 30 keV)" in §4.1 §12 is too strong.

### C-1. Hit recording misses double crossings within one chord

- `T3_causal.py` records a hit only when the chord endpoints straddle R. Grazing double crossings within one step are lost.
- My solver (smaller steps) finds 2-6 extra hits in 3 of 16 events. In one event this changes Δs from 49 to 61 µm.
- At the production h_max = 0.2 cm the loss is larger.
- **Fix:** test the quadratic for two roots per chord. It also affects the "≈ 3 hits per layer" counts (S-6, T-11).

---

## 2. S-2 / S-3: thickness, window, material (priority 2)

### Confirmed

1. **Non-linear B response (T-3), independently reproduced** with the conformal solver (`code/R1_Blinearity.py`, `figures/R1_Blinearity_out.txt`; 3 events, 1 keV, 500 GeV).
   - Hits before the first crossing are linear: metric 2×10⁻⁴ to 2×10⁻².
   - After the first crossing the metric Q68|d(B) − k d(B/k)|/Q68|d(B)| is 0.13-0.14 (k = 4) and 0.29-0.39 (k = 20).
   - The response per unit B is ×1.14 (B/4) and ×1.31 (B/20). That is 1 + 0.10 ln(B₀/B), identical to S's 1 + (0.10-0.12) ln.
   - So the non-linearity is not an artefact of the Athena-type algorithm. Synthesis §7 item 2 ("never cross-checked against an independent NG solver") can be closed for B at 0.6-3 keV.
2. **Λ^−1.9 scaling.** From T3 §3.2 (B column) the local exponents are 1.76-1.92 (1→3 keV) and 1.63-1.98 (3→10 keV). That is consistent with "≈ −1.9" but should be quoted as −1.6…−2.0.
3. **The S-3 heuristic arithmetic is right:** B^{1−c} with c = 0.08-0.11 gives B^0.89-0.92, and Λ^{−2+2c} gives −1.78…−1.84. It is still a heuristic; the coefficient is fitted, not derived.

### B-2. All window and Δs-cut statements are at truth-hit level. Detector resolution and the z-blindness of 2S modules are of the same size as the "MS floor".

**Where:**
- S-2 (pass fractions; "a Δs cut below ~30 µm costs 30-45 %");
- S-3 revised window;
- §4.1 rows §4.4 lower edge and §9.1 plane finder;
- §4.4 Q9.

T3 §9 says "truth-hit level, no hit resolution", but the synthesis drops this caveat.

**Evidence.**
- Phase-2 single-hit resolutions (pitch/√12) are 26-29 µm in rφ in the PS and 2S strips. In z they are 0.43 mm (PS macro-pixels) and ≈ 1.4 cm (2S, 5 cm strips, no stereo).
- The unweighted eigenvalue Δs of T3 uses true 3D points. A real plane fit must weight the 2S hits by their rφ-only information. Its Δs then contains a resolution term of ≳ 20-30 µm, comparable to or larger than the MS floor of 11-22 µm.
- So the "≤ 30 µm cut costs 30-45 % because of MS" is not the dominant effect, and the 50 % edge 0.45-0.7 keV will move.

**Required fix.**
- Label every S-2/S-3 efficiency "truth level".
- Redo the Δs efficiency with hit smearing and a strip-aware weighted plane fit (T4 already has the resolutions). Only then state cut-dependent losses.

### B-3. "×7-50 above the formula" is presented as new, but Li et al. already show it

**Where:** S-3 table, T-2, §6 "Thickness ∝ m_Q/Λ⁴ as the Λ meter … ×7-50 off".

**What is wrong.**
- 2002.07503 App.C, Fig.8, shows their *numerical* thickness D_N against the formula D_A with D_N/D_A spanning 10⁻³ to 10³. They state agreement only "within an order of magnitude" for n_T ~ 1-100.
- The published Li reach uses the numerical thickness [1911.02223 Fig.4], not Eq.III.12.
- So "the formula is off" is a criticism of the *strategy's* use of the formula (STRAT §4.4, V2), not of the published analyses.
- Given A-1, Li's numerical thickness at 1-2 keV is close to the causal one (×0.85).

**Required fix.**
- Credit 2002.07503 App.C.
- Re-scope the novelty to:
  - the Λ^−1.9 scaling and its m_Q independence;
  - the B ln B origin;
  - the correction of the project's own formula-based window.

### B-4. Material model: plausible total, unverified distribution, and the √(x/X0) check is internal only

- ≈ 19 % X0 at η = 0 is plausible against public statements. Phase-1 is ≈ 0.4 X0 near η = 0 [1405.6569 Fig. material]. "Substantially reduced in Phase 2" [1912.02061] implies ~0.2. I could not open the TDR either: web search found only the TBPX module measurement [2407.13721] and qualitative statements.
- But:
  - (i) the per-layer split (PS 2.5 %, 2S 1.8 %, IT 1.2 %) is a guess, and MS at the outer layers drives Δs through the lever arm (T3 §3.2 item 5);
  - (ii) the IT material is placed only at |z| < 20 cm, so IT hits at larger |z| are not modelled in the forward TBPX/TFPX;
  - (iii) S's "√(x/X0) verified" is a scaling test of the same code (exponent 0.517), not a validation of the material.
- **Fix:** keep UNVERIFIED in every headline number that depends on material (MS floor, f_stop, S-12). Have the user pull the Phase-2 tkLayout/TDR X0(η) curve (CMS-internal access) before P-level use.

### C-2. Δs definition

- Δs = √(smallest eigenvalue of Σhhᵀ/(N−1)), plane through the origin. This matches Knapen Eq.11 and Li Eq.C.1 and is used consistently.
- State it once in the synthesis.
- State that "max residual" is the quantity for hit-association windows (T3 gives it; S-2 quotes it).

### C-3. S spot check 9 called PASS at 25 % disagreement

Δs(M) at 1 TeV, 3 keV: 18.2 vs 24 µm, 30 events. Call it "consistent within MC statistics (±25 %)", not PASS.

---

## 3. S-4 / S-5: measurement and MET alignment (priority 3)

### Confirmed: the degeneracy theorem

Dimensional analysis of S = −m∫dτ − σ∫dA plus the Lorentz force:
- the string term gives d(γv)/dt ∝ σ/m, a single length ℓ₀ = m/σ;
- the B term ∝ qB/m, so in units of ℓ₀ it is ε_B = qB/σ;
- MS gives δp_⊥ = θ₀ p, which depends only on β (Highland), so the acceleration is ∝ 1/m;
- Bethe dE/dx = f(βγ), so ΔE/E ∝ 1/m.

At fixed ℓ₀ and velocities, (m, σ) → (λm, λσ) changes only the B, MS and dE/dx terms. T4 §2.1 and §3.1 are exactly right, and my conformal solver is manifestly built from σ/m and qκB/m only.

### B-5. The headline "1 % / 0.5 % with 30 events" is below the stated systematic floor and rests on idealisations

**Where:** synthesis §0 item 3, S-4 table, §4.1 §5 O6, P2.

**What is wrong.**
- (i) With the stated MET/JES scale uncertainty of 1-3 %, the result is systematics-limited: δm/m ≈ 1-3 % and δΛ/Λ ≈ 0.5-1.5 % (T4 §4.4 says so; the synthesis headline does not).
- (ii) Per-event σ(m)/m ≈ σ(p_T)/p_T is set by the MET resolution σ⊥ = 25 GeV, which is UNVERIFIED for PU 200. Gaussian MET tails are assumed.
- (iii) It is a local CRB with known hit assignment, no PU, and the global minimum assumed (T4 lists aliasing at 10 keV).
- (iv) The γ* and (βγ)_T that convert MET into m_Q come from the trajectory model. A model error of the size found in A-1 (≈ 15 % on out-of-plane quantities between two reasonable string models) would not affect γ* at first order, but it was not tested.
- My arithmetic check: 7-9 % per event / √30 ≈ 1.3-1.6 %. The quoted 0.9-1.2 % implies benefit from high-p_T events (plausible).

**Required fix.** Headline should read "≈ 1-3 % on m_Q and 0.5-1.5 % on Λ for 30 events, MET-scale limited; statistical CRB 1 %/0.5 %; local bound, known assignment, no PU".

### C-4. B-only Λ route

It relies on the near-crossing non-linear physics being modelled to ≲ 10 % (independently confirmed here for 1 keV) and on the charge q being known. This is already stated in T-1. Fine.

### C-5. MET alignment (S-5)

- `T4_met.py` is correct: directed Δφ ∈ [0, π], rejection π/δ, 95 % quantiles reproduced by construction.
- The "background model" is a pure geometric acceptance for isotropic fake planes.
  - (i) In Z(νν)+jet, hard-scatter and UE hits are correlated with the jet axis (anti-parallel to MET; harmless for a directed cut). Multijet topologies are not isotropic either.
  - (ii) The real gain depends on the finder: fake-plane probability scales like a power of the hit density in the wedge, so ×13-34 may be conservative.
  - (iii) The "÷16 seeding" and the "×13-34 rejection" are the same wedge and must not be multiplied as independent factors.
- **Fix:** state these three points in S-5 and §4.1 O7.

---

## 4. T1 cosmology (priority 4)

### Confirmed: Ω ∝ T_RH^{21/4}, not T^7

- The dim-8 rate density is γ ∝ T¹²/m_Q⁸. The energy injection then gives ρ_d/ρ_SM ≡ Z ∝ M_Pl T_RH⁷/m_Q⁸ (UV dominated).
- Non-thermalised gluons give n_d/s ∝ Z, i.e. T⁷.
- A self-thermalised dark sector conserves energy, not number: ξ ∝ Z^{1/4} and n_d/s ∝ ξ³ ∝ T^{21/4}. Glueball relic ∝ ξ³ for both instant confinement and cannibalism.
- Thermalisation check: Γ ~ α_d² n_d/T² with n_d ~ 10⁻⁴T³ at T ~ 10 GeV gives ~10⁻⁶ GeV ≫ H ~ T²/M_Pl ~ 10⁻¹⁶ GeV. So T1 and S are right.

### Confirmed (order of magnitude): T_max ≲ m_Q/25

- On-shell quirk production ~ (M_Pl/m) α² e^{−2m/T} must keep Z ≲ 10⁻⁴.
- With M_Pl/m ~ 5×10¹⁵ and α² ~ 10⁻³, this gives e^{−2x} ≲ 10⁻²⁵, i.e. x ≈ 25-30.
- The threshold is logarithmically robust.

### C-6. Range and the ×2.2 comparison

- §0 and S-15 quote "T_RH ≲ 5-35 GeV". T1's own table gives up to 64 GeV (1 TeV, 1 keV), capped by m_Q/25 = 40 GeV; the SIDM-like bound gives 4.7-31 GeV. Use "≈ 5-40 GeV (0.2-1 TeV)".
- The ×2.2 vs 2512.20696 is not checkable without their code. The g*s explanation is consistent: ×20 in Ω ↔ ×1.8 in T at Ω ∝ T⁵.
  - Thermalisation alone would push the opposite way (more, softer quanta ⇒ larger Ω in T1, i.e. a *lower* T1 bound). T1 is higher by ×2.2, so the g*s hypothesis is the more plausible one.
  - Keep "do not claim an error until resolved with the authors".

---

## 5. T3/T6 spot checks (priority 5)

| Item | Check | Result |
|---|---|---|
| Doublet cτ = 7.9 mm and its use | Γ = G_F²\|V_ud\|² f_π² ΔM³ √(1 − m_π²/ΔM²)/π gives the known higgsino-like cτ ≈ 7 mm at ΔM ≈ 340-355 MeV. For a member bound by the string the free decay rate applies in its instantaneous rest frame: the IC charge and the string are common to both members, so ΔM is pure EW; acceleration effects ~ σ/m ≪ ΔM. Survival uses proper time ∫dt/γ (T3 §5). | PASS |
| BTL medians 3.5/9.6/18.7 ns | toa = R/β_T − R cosh η (S re-derived on the same cache) | PASS (not independent kinematics) |
| Merged pair 9-21× MIP | Bethe at β ≈ 0.18-0.3: per quirk ≈ 8-16× MIP, × 2 × 0.75-0.9 gives ≈ 12-29× | PASS (order) |
| γγ fraction 4.0-4.5 % | consistent with the photon-PDF share for charged singlets at 0.5-1 TeV | PASS (not re-computed) |
| f_stop 1.0 ± 0.3 % (EB+HB) | not re-run (CPU) | not checked |

### B-6. Stopped-pair reach assumes a long-lifetime live fraction and zero background

**Where:** S-8, T-5, §4.5 item 1, P3.

**What is wrong.**
- (i) The pair annihilates 0.02-0.5 µs after production [T6 G-T6-4]. The 21 % "empty-BX live fraction" of the 2016 search applies to lifetimes ≫ the train structure.
  - For sub-µs decays, the fraction landing in an empty BX depends on the position in the train. Only collisions in the last ~τ/25 ns BXs before a gap contribute.
  - It must be taken from the lifetime-dependent acceptance of 1801.00359, which falls at ~100 ns (UNVERIFIED; PDF not opened by anyone).
- (ii) "3 events = reach" assumes zero background at 3 ab⁻¹ (×80 the 2016 luminosity). T6 notes background-freeness needs a high energy cut, which is not quantified.

**Fix:** both factors must be in the reach. As quoted, 0.65 TeV is an upper estimate.

### C-7. Stopping model and flat-in-Λ extrapolation

T3 states these; the synthesis keeps "covers 30 keV-1 MeV" only as "plausible". OK. But §4.5 item 2 ("covers 20 keV to ≳ 100 keV") should carry the same caveat.

---

## 6. Other findings

### A-3. The spot-check table certifies 35/35 PASS but never tested the premise of the top-ranked gap

**Where:** synthesis §0 ("My cross-checks pass 35/35") and §3.

**What is wrong.**
- No check compares a published integrator with the causal string.
- Checks 9-11 and 14 are re-runs of investigators' code, i.e. reproducibility, not validity.
- Presenting "35/35" alongside the S-1 headline gives false assurance on exactly the claim that fails (A-1).

**Fix:**
- Add the Li-literal comparison (this review) and an explicit "what was not checked" line for S-1.
- Separate "independent" from "re-run" counts in the headline.

### B-7. Ranking and paper plan

- Given A-1, S-1 cannot be rank 1 "EXPLOIT, high confidence". The genuinely new and confirmed content is:
  - the causal string as a validated production propagator (`T3_causal.py`, now cross-checked);
  - the MS floor (truth level);
  - the B ln B non-linearity and the Λ^−1.9, m_Q-independent thickness;
  - the degeneracy theorem.
- Re-rank accordingly.
- P1 should become "Quirk-pair trajectories in a solenoid: exact string dynamics, crossing-generated plane thickness, and multiple scattering". Include the straight-string comparison done correctly (Li-literal, converged and at the printed step).

### B-8. T2's "Λ^−2.5" and the 4-event realistic study

The tables of T2 §5.1 mix prescription errors with an unconverged nudge step (T3 §3.1 notes T2's labSS "nudge" artefact at 2 keV). After A-1 these tables should be removed or relabelled. The covariance test should be redone with the Li-literal prescription. I expect frame independence up to Euler error.

### C-8. Number mismatches between the synthesis and its sources

- S-1 "OT hits 0.2-35 mm": T2 §5.1 gives 0.02-35 mm (0.02-5 at 5 keV) for labSS/cmSS. Moot after A-1.
- §0 says the MS floor is "verified"; it was scaling-verified only (B-4).
- S-9 upgraded to EXPLOIT, conf. medium, while T2 called it WORTH A CHECK and the per-crossing step count (150-200) is an ESTIMATE. Fine as a config note, but it is not a finding about CMS.

### C-9. Missing references and credit

- Credit Li et al. App.C (B-3).
- For the piecewise-null string construction, cite the Artru/Lund string literature: Artru 1974/1983, Andersson et al. 1983. "Athena-type exact NG" is a known construction, not an ATLAS invention.

---

## 7. Independently reproduced numbers

| # | Number (source) | My method | Result | Pass/Fail |
|---|---|---|---|---|
| 1 | Causal port = exact NG (T2 §5.1, S-1) | conformal-gauge NG delay ODE (`R1_conformal_ng.py`), 16 events, 0.6-3 keV | thickness ratio 0.990-1.004, out-of-plane ≤ 0.4 µm | **PASS** |
| 2 | Vacuum exactness of the causal port | conformal solver vs ExactPair, pre-crossing | 6×10⁻⁴ µm | PASS |
| 3 | "Straight string (≈ Li) off ×0.04-60; hits 0.2-35 mm" (S-1, T2) | literal Li algorithm (`R1_li_literal.py`), 18 events | converged Li/causal = 0.84-1.04; hits 0.03-0.4 mm (≤ 1 keV); labSS 4-60× | **FAIL** (applies to labSS only) |
| 4 | "Straight string + MS gives fake 0.2-21 mm" (T3 §3.1) | Li-literal + thin-scatterer MS (`R1_li_ms.py`), 8 events | 12-13 µm median (causal 15-30) | **FAIL** (labSS only) |
| 5 | Non-linear B response 30-45 %, linear before 1st crossing (T4, S T-3) | conformal solver, B/4 and B/20 | 0.29-0.39 (k = 20), pre-crossing ≤ 0.02; ratio 1.14/1.31 | PASS |
| 6 | Response ∝ 1 + 0.10-0.12 ln(B₀/B) (S) | same | 1 + 0.10 ln | PASS |
| 7 | Causal thickness 15-60 µm at 1 keV, 1-15 µm at 2 keV (T2/T3 order) | conformal solver | 3.9-49 µm (1 keV), 1.0-13 µm (2 keV), 0.5-6.7 µm (3 keV) | PASS |
| 8 | Λ^−1.9 (T3) | exponents from T3 table | −1.6…−2.0 | PASS (quote range) |
| 9 | Degeneracy theorem (T4 §2.1) | dimensional analysis of EoM + MS + Bethe | exact | PASS |
| 10 | Ω ∝ T_RH^5 not T⁷ (T1) | analytic | T^{21/4} | PASS |
| 11 | T_max ≲ m_Q/25 (T1) | Boltzmann-suppressed on-shell yield estimate | x ≈ 25-30 | PASS (order) |
| 12 | Doublet cτ ≈ 7.9 mm; free decay applies when string-bound | formula + argument | ≈ 7-8 mm; yes | PASS |
| 13 | MET alignment ×13-34 (T4) | code read; π/δ₉₅ geometry | correct as geometry | PASS (model caveats C-5) |
| 14 | S-3 exponent arithmetic | algebra | B^0.89-0.92, Λ^−1.78…−1.84 | PASS |
| 15 | 19 % X0 at η = 0 | public Phase-1 value / "about half" | plausible (~0.2) | UNVERIFIED |
| 16 | "1 %/0.5 % with 30 events" headline | arithmetic + T4's own systematics | statistical only; total 1-3 % / 0.5-1.5 % | FAIL as headline (B-5) |

**Runtime notes:**
- `R1_conformal_ng.py` takes ~11 min for 16 events (3 keV needs N ≈ 9000 steps per π).
- `R1_li_literal.py` takes minutes per Λ.
- `R1_li_ms.py` takes ~5 min at 1-3 keV.
- `R1_Blinearity.py` takes ~2 min.
