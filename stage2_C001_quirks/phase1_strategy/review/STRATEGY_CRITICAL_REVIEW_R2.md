# C001 Phase 1 (Strategy) critical review, round 2

Reviewer: fresh independent critical reviewer (JFC `agents/critical_reviewer.md`), 2026-10-07. I did not write the artifacts and did not do round 1.

Artifacts reviewed (v2):
- `phase1_strategy/outputs/STRATEGY_DRAFT.md` (STRAT), including Sec. 20 "Response to review";
- `phase2_exploration/outputs/SAMPLE_REQUIREMENTS.md` (SREQ);
- `phase1_strategy/outputs/OPEN_QUESTIONS.md` (OQ).

Checked against:
- the round-1 review `STRATEGY_CRITICAL_REVIEW.md` (R1);
- TH, EX, ST, LM and `LOG.md`;
- cached primary text for 2410.09164, 2410.00269 and 2601.20063, plus 2012.09254, downloaded for this review with `arxiv_pdf.py` (all in `../research/cache/pdf/`).

My own recomputations used pure-Python scripts in the session scratchpad (`reach_r2.py`, `reach_syst.py`). They are not committed.

## Verdict: **PASS**

**No Category A items remain open.**
- Both round-1 A items are correctly fixed.
- All nine round-1 B items are addressed. Eight are fully fixed. B9 (the Z(νν) cross section) is handled as a carried range, and a published measurement now settles it (new B1 below).
- Every recomputed number agrees with STRAT, SREQ and OQ, within interpolation rounding.

**Three new Category B items** must be fixed before Phase 2 starts. All three are text-level or one-line recalculations:
- **B1.** Replace the [A9] range of 0.5-20 pb with the CMS measurement. σ(Z→νν, pT^νν > 200 GeV) = 3.00 (+0.18/−0.17) pb at 13 TeV [2012.09254]. Two consequences:
  - the round-1 "≈ 10× low, 5-20 pb" claim was itself 2-6× too high;
  - the original stream of ~10⁷ events and the target f_tot ≲ 3×10⁻⁸ essentially stand.
- **B2.** The high-background reach rows (B = 480 and 7680) are statistics-only. With a realistic ±20% background uncertainty, the reach at 3 ab⁻¹ and Λ = 3 keV falls from 0.76 to 0.57 TeV (×16) and from 0.58 to 0.32 TeV (×256).
- **B3.** The "mass reach ≈ 1.0-1.2 TeV" novelty line in §6.4 was not updated after the round-1 B4 fix.

Upstream TH/EX/ST still carry the errors listed at the end of STRAT §20. The strategy's corrected values are the right ones. The one exception is the Z(νν) σ: neither the upstream value (0.5-1 pb) nor round 1's value (5-20 pb) is right (B1).

---

## 1. Verification of the round-1 fixes

| Item | Fix claimed (STRAT §20) | Verified? | Evidence |
|---|---|---|---|
| **A1** P5 not ISR-free | New §10.1a gives pair kinematics, ε(P5) per mass, and a union of ≈ 0.2-0.3 only at ≲ 300 GeV. Text changed in §1, §5, §6.2, §6.4, §10.1, §16 R5 and OQ Q1/Q6 | **Yes** | pT_min = βγ M/cosh η with βγ(0.15) = 0.1517 and M = 2γ*m_Q (γ* = 1.30/1.28/1.25/1.214) gives 57.8-78.9 / 85.4-116.5 / 139-190 / 216-295 GeV, matching the stated values. ε(P5) = 0.5 × f × (0.5-0.9) with the A4 anchors gives 0.075-0.20 / 0.053-0.13 / 0.028-0.077 / 0.013-0.04, also matching. The 0.15 threshold is from 2601.20063 l.137-141, 288, 298. "Not decoupled from ISR" now appears consistently in all listed locations, and OQ Q6 is re-recommended (P2 main, P5 small study). The P2 ∪ P5 gain at 300 GeV is somewhat generous (C3) |
| **A2** τ′ limits | Q = 1e: 1.02/1.14 TeV; Q = 2e: 1.32/1.41 TeV | **Yes** | 2410.09164 l.986-987 ("1.02 (1.14) TeV and 1.32 (1.41) TeV for the ionization approach (for the mass method)"); Tab. 3 l.1014-1015. The model is "neutral under SU(3)C and SU(2)L, couple only to the photon and the Z" (l.195-197), i.e. the E = (1,1)₋₁ couplings. See C4 for the N_IC = 2 factor |
| **B1** pair velocity | v_T from TH t_BTL; layer-by-layer toa table (§4.2), §10.4 Facts, R3 | **Yes** | 114.8 cm/(c t_BTL) = 0.383/0.193/0.104 (pT = 250 GeV) and 0.547/0.336/0.200 (pT = 500 GeV). Independent kinematics: v_T = pT/√(M² + pT² + pz²), with \|η\| < 1.5 ⇒ pz ≤ 2.13 pT. This gives 0.32-0.43 / 0.18-0.196 / 0.10-0.104, so the t_BTL column is right and TH's β_T column is wrong. All 15 entries of the §4.2 toa = (r/c)(1/v_T − 1) table reproduce to ≤ 0.3 ns (e.g. 500 GeV 2S L3: 3.696 ns × 4.18 = 15.4; 1 TeV PS L3: 1.745 ns × 8.62 = 15.0). The BTL delays of 6.2/16.0/32.9 ns agree |
| **B2** Λ edges vs m_Q | New §4.4; regime table and D4 per m_Q; Λ = 0.6 keV "probes the transition" | **Yes** | Λ_low = (1.16 × 3.8 × (m/100)/100)^¼ = 0.458 (m/100)^¼ keV gives 0.545/0.685/0.815 keV. The ×10^±¼ = ×1.78 band gives 0.31-0.97 / 0.39-1.22 / 0.46-1.45 keV. Λ_high = [3.95 cm (γ*−1)(m/100)/s]^½ gives 10.9/15.7/19.4 keV (s = 200 µm) and 21.8/31.4/38.7 keV (s = 50 µm). All match |
| **B3** GNN 8 vs 25 layers | 71.9% (8 layers), 79.0% (25 layers) | **Yes** | 2410.00269 l.494 (71.9%, eight layers) and l.502-503 (25-layer, 79.0%). Corrected in §2.4 and §9.2 |
| **B4** reach with background | §6.1 rewritten with an explicit CLs method, B rows and the gain as a range | **Yes** (but see new B2) | Full recomputation in §2 below; every entry reproduces to ≤ 0.01-0.03 TeV. The method is stated and the gain is a range. Remaining gap: the high-B rows are statistics-only (new B2) |
| **B5** Run-3 luminosity | 150-350 fb⁻¹; S2 reach 0.72-0.87 TeV | **Yes** | Recomputed 0.78/0.83/0.88 TeV (B = 0) and 0.72/0.76/0.78 TeV (with B). The nuance that 333 fb⁻¹ is the IP1 value is correct |
| **B6** CPU/storage | One set of numbers, defined in SREQ §2 | **Yes** | Row sums: 5.2 + 0.2-0.5 + 0.3 + 4.2-6.9 + 6.9 + 6.9 + 0-3.5(4) + 0-3.5 = 23.7-34.2 k core-h. Phase 3: 6.6×10⁵ × 250 s = 45.8 k, plus 10⁵ × 250 s = 6.9 k (Ẽ, L), = 52.8 k. Total 77-87 k core-h. Storage 8-12.5 + 11.4-19 = 19.4-31.5 TB. STRAT §6.2, OQ Q3 and OQ Q5 all agree |
| **B7** closure power | Primary target 10⁻³ with ≥ 10⁵ crossings; 6×10⁻⁵ secondary via factorisation + resampling | **Yes** | 7.33×10⁶/50 = 1.47×10⁵ crossings, i.e. 147 fakes (±8%). At μ = 200: 3.7×10⁴ crossings. All-layer: 8.8 fakes. Resampling to 1.7×10⁶ crossings is 11.6× reuse. The CMS S1-PU sample at μ = 50 is now 10⁵ |
| **B8** skim MET coverage | CR1/VR3 RAW sources, D18 fallback, EXOMONOPOLE qualified | **Yes** | STRAT §8.1 rows, §11.3, D18 in §18; SREQ S2-DATA-MET caveats and the new S2-CR1/S2-VR3 rows; §5 RAW and pick-events queries |
| **B9** Z(νν) σ | Range 0.5-20 pb carried as [A9] until MG5 (W2) | **Partly** | The procedure is sound, but a published measurement exists, and it shows both ends of the range rest on wrong estimates. See new B1 |
| C1-C8 | Applied or noted | Yes | C3: I agree with the fixer. The stated edge set is 12 + 6 = **18**, not 16 (round 1 miscounted); 18 × 10k extra gives 6.6×10⁵ events, 45.8 k core-h and 9.9-16.5 TB. C2 was applied in STRAT §1 but not in OQ Q11 (see C1 below) |

---

## 2. Independent recomputation table

| # | Quantity | Document value | My value (method) | Result |
|---|---|---|---|---|
| 1 | s95 (expected CLs, n_obs = Poisson median) for B = 0 / 2.5 / 3.5 / 4.5 / 10 / 30 / 160 / 480 / 7680 | 3.0 / 4.6-5.6 / 8.1 / 12.6 / 26.6 / 45.2 / 174 (STRAT §6.1) | 3.00 / 4.61 / 5.17 / 5.65 / 8.08 / 12.55 / 26.56 / 44.69 (exact Poisson) / 171.8-175 (1.96-2.0 √B) | OK |
| 2 | Phase 2, 3 ab⁻¹, Λ = 3 keV (ε = 0.0182), reach for B = 0 / 30 / 480 / 7680 | ≈ 1.2 (1.24 extrap.) / 0.97 / 0.76 / 0.58 TeV | 1.232 / 0.974 / 0.771 / 0.588 TeV (log-linear σ interpolation in m on the TH 14 TeV table, log-linear extrapolation above 1.2 TeV) | OK |
| 3 | Same at Λ = 1 keV (ε = 0.00308) | 0.92 / 0.69 / 0.53 / 0.38 TeV | 0.917 / 0.703 / 0.532 / 0.406 TeV (0.375 with log-log interpolation) | OK (C5: interpolation scheme) |
| 4 | Phase 2, 1 ab⁻¹, Λ = 3 / 1 keV | 1.03; 0.86 / 0.68 \| 0.74; 0.60 / 0.46 TeV | 1.032; 0.866 / 0.693 \| 0.748; 0.614 / 0.471 TeV | OK (≤ 0.015) |
| 5 | Run 2 (101 fb⁻¹ at 13 TeV) + Run 3 (150/250/350 fb⁻¹ at 13.6 TeV), Λ = 3 keV, B = 0 / with B | 0.78 / 0.72, 0.83 / 0.75, 0.87 / 0.77 TeV | 0.781 / 0.724, 0.834 / 0.756, 0.876 / 0.778 TeV | OK |
| 6 | Same at Λ = 1 keV | 0.54 / 0.49, 0.58 / 0.52, 0.62 / 0.54 TeV | 0.546 / 0.493, 0.592 / 0.520, 0.626 / 0.542 TeV | OK |
| 7 | P5: pT(QQ̄)_min for β_pair ≥ 0.15 (barrel) | 58-79 / 85-117 / 139-190 / 216-295 GeV | 57.8-78.9 / 85.4-116.5 / 139.0-189.6 / 215.9-294.6 GeV | OK |
| 8 | ε(P5) and P2 ∪ P5 | 0.08-0.20 / 0.05-0.13 / 0.03-0.08 / 0.01-0.04; union ≈ 0.2-0.3 at ≲ 300 GeV | Same ε(P5). Unique P5 gain over P2, using the A4 anchors and P2 ≈ 50% at pT 100: ≈ +0.05-0.09 at 200 GeV but only ≈ +0.02-0.03 at 300 GeV | Union at 300 GeV ≈ 0.17-0.28: slightly generous (C3) |
| 9 | Pair v_T and BTL delay | v_T 0.38/0.19/0.10; delay 6/16/33 ns | 0.383/0.193/0.104; 6.2/16.0/32.9 ns. Kinematic cross-check given in §1 (B1 row) | OK |
| 10 | Layer toa table (15 entries) | §4.2 | All reproduce to ≤ 0.3 ns | OK |
| 11 | Λ_low and Λ_high per m_Q | 0.54/0.69/0.81; 11/16/19; 22/31/39 keV | 0.545/0.685/0.815; 10.9/15.7/19.4; 21.8/31.4/38.7 keV | OK |
| 12 | CPU/storage (SREQ §2 = STRAT §6.2 = OQ Q3/Q5) | 24-34 k / 8-12.5 TB; +53 k / +11-19 TB; 77-87 k / 20-32 TB | 23.7-34.2 k; +52.8 k / +11.4-19 TB; 76.5-87 k / 19.4-31.5 TB | OK, consistent in all three files |
| 13 | S2 Phase-2 CPU | 11-16 k core-h | ≈ 10.6-13 k from the rows (the background re-digitisation of 3×10⁵ × 100 s = 8.3 k dominates) | OK (upper end generous) |
| 14 | Z(νν)+jets σ(pT > 200 GeV) | 0.5-20 pb [A9] (ST 0.5-1, R1 5-20) | **3.00 (+0.18/−0.17) pb measured at 13 TeV**, fiducial region = pT^νν > 200 GeV with no other requirement [2012.09254 abstract l.37-39, Sec. 6 l.437-440]. ≈ 3.3-3.6 pb at 14 TeV (ESTIMATE, ×1.1-1.2 energy scaling) | **New B1** |
| 15 | τ′ DY limits, 2410.09164 | 1.02 / 1.14 (Q = 1e), 1.32 / 1.41 TeV (Q = 2e) | Same (l.986-987, Tab. 3). Expected limits are 1.05 / 1.14 and 1.35 / 1.41 TeV | OK |
| 16 | Closure statistics | 1.47×10⁵ crossings; 147 fakes; ≈ 9 all-layer fakes; ≤ 12× reuse | 146,550; 147; 8.8; 11.6× | OK |
| 17 | GNN efficiency | 71.9% (8 layers) / 79.0% (25 layers) | 2410.00269 l.494, 503 | OK |

---

## 3. Category A (blocking)

None.

---

## 4. Category B (fix before Phase 2 starts)

### B1. [A9] Z(νν)+jets cross section: use the CMS measurement, not two conflicting guesses
**Where:**
- STRAT §8.3 (irreducible row), §11.1 ([A5] f_tot), §18 A9;
- SREQ S1-ZNN ("at the high end the per-event ε needed is ~10⁻⁶") and §6 W2.

**Source.** CMS measured σ(Z→νν) = **3000 (+180/−170) fb** at 13 TeV [arXiv:2012.09254 (JHEP 05 (2021) 205), abstract l.37-39]. The fiducial region is "p_T^miss > 200 GeV without any other requirements placed on the Z boson kinematics or the transverse momentum of the leading jet", where p_T^miss is the pT of the neutrino pair [Sec. 6, l.437-441]. This is exactly the quantity A9 carries.

**Consequences.**
- At 14 TeV the value is ≈ 3.3-3.6 pb (ESTIMATE).
- ST's 0.5-1 pb is 3-7× low, and round 1's 5-20 pb is 1.5-6× high.
- Z(νν) alone gives ≈ 1.0×10⁷ events in 3 ab⁻¹, i.e. ~2×10⁷ with W/tt̄/QCD in the MET stream.
- So the required f_tot is ≈ (1.5-3)×10⁻⁸. The "≲ 3×10⁻⁹" branch of §11.1 and the "ε ~ 10⁻⁶" sizing remark in SREQ do not apply.
- The B2 rate of 10⁻² fb [1911.02223] is an absolute rate, so B = 30 is unaffected.

**Fix:**
- Cite 2012.09254 in §8.3 and A9 (or retire A9).
- Remove the 3×10⁻⁹ branch.
- Keep the MG5 W2 computation only for the 14 TeV / 13.6 TeV scaling, and for the HT- or pT-binned sample definition.
- Mark the ST §3.0 value as an upstream error.

### B2. The high-background reach rows are statistics-only
**Where:** STRAT §6.1 table (B = 160, 480, 7680) and the "Gain of Phase 2" bullets; §1 reach bullet; §6.2 S1 reach; §16 R4; OQ Q1.

**The problem.**
- s95 = 45 (B = 480) and 174 (B = 7680) assume the background is known to √B, i.e. to ±4.6% and ±1.1%.
- No data-driven random-coplanarity estimate (M1/M2, an nPV extrapolation to μ = 200) will reach that precision.
- The cited reference sizes are 5-52% for the spurious-track systematic [2309.16823 Tab. 7] and ±100% for the ABCD bias correction [2410.09164].

**Recomputation** (s95 ≈ 1.96 √(B + (δB)²), Λ = 3 keV, 3 ab⁻¹; ESTIMATE):

| B | δB/B = 0 | 20% | 50% |
|---|---|---|---|
| 30 | 1.00 TeV | 0.94 TeV | 0.82 TeV |
| 480 (×16) | 0.78 TeV | **0.57 TeV** | 0.47 TeV |
| 7680 (×256) | 0.59 TeV | **0.32 TeV** | 0.24 TeV |

**Fix:**
- State that the rows are statistics-only.
- Add one background-uncertainty variant (e.g. 20%) for the B = 30 and ×16 rows, and drop or flag the ×256 statistics-only number.

The qualitative conclusion ("the S1 value hinges on PU-200 suppression"; S3 recommended) is unchanged and in fact strengthened.

### B3. Stale headline reach in the novelty audit
**Where:** STRAT §6.4 "Survives (S1/S3)" item 5: "mass reach ≈ 1.0-1.2 TeV".

**The problem.** After the B4 fix, the same document gives 0.58-1.2 TeV (§6.1, §6.2 row), or lower with B2 above. Quoting only the background-free end in the novelty list contradicts §1 and §6.1.

**Fix:** state the range, conditional on the PU-200 background (e.g. "≈ 1.2 TeV if B ≈ 0, ≈ 0.95 TeV at the μ = 50 rate, < 0.8 TeV if PU 200 scales it ×16").

---

## 5. Category C (notes)

- **C1.** Stale text:
  - OQ Q11 still says "Heavy pairs arrive ~10-20 ns late". Use 16 ns (500 GeV) and 33 ns (1 TeV) at the BTL, as STRAT §1 now does.
  - The STRAT header line 5 still says "Not yet reviewed by the critical reviewer".
  - §19 "Critical review: pending" should point to R1/R2.
- **C2.** STRAT §6.2 S2 deliverable says "~250-350 fb⁻¹". With the new bracket, Run 3 + 2017-18 is 251-451 fb⁻¹.
- **C3.** The P2 ∪ P5 union at m_Q = 300 GeV is probably overstated.
  - Folding the A4 anchors with a P2 turn-on (≈ 50% at pT 100, ≈ 85% at 130-170), the events P5 adds over P2 are ≈ +0.02-0.03 at 300 GeV, versus "+0.05-0.1" in §10.1a. The +0.05-0.1 holds at 200 GeV.
  - Related: the "170 (100)" and "200 (128)" L1 TDR notation gives the offline 95% point and the **online** threshold. Equating the online threshold with the offline 50% point (inherited from EX §3.6, used for P1′ and the P2 overlap) is an approximation.
  - The W2/W10 study replaces all of this. Say "≈ 0.2-0.3 at m_Q ≈ 200 GeV, ≈ 0.17-0.28 at 300 GeV".
  - The §10.1 header still says "m_Q 300-800 GeV" although the P5 row now starts at 200.
- **C4.** The τ′ anchor in OQ Q10 and STRAT §13 is quoted for the τ′ cross section, i.e. N_IC = 1.
  - The N_IC = 2 quirk has twice the σ. At Λ → 0 the HSCP-equivalent limit is therefore higher, roughly +0.1 TeV (σ falls ×3 per 200 GeV near 1.1 TeV).
  - The anchor applies only where ℓ_max ≫ detector size, i.e. Λ ≲ 0.1 keV, not at the 0.3 keV grid edge (ℓ_max ≈ 50 cm, TH Tab. 4.2a).
  - Note both points. It also shows that HSCP searches are already strong below the analysis window.
- **C5.** σ interpolation in the 200-500 GeV gap is ambiguous: σ(400 GeV) is 20.2 fb (log-linear) or 14.6 fb (log-log).
  - Most reach entries reproduce with log-linear. The 1 keV ×256 entry (0.38 TeV) matches log-log (log-linear gives 0.41).
  - State the scheme, or carry ±0.03 TeV at low mass. The TH table at 350 GeV would remove the ambiguity.
- **C6.** §6.1 applies the μ = 50 rate of 10⁻² fb to Run 2+3 and assumes Run-3 pile-up ≈ μ = 50. This is flagged UNVERIFIED, which is fine. Note that the 2024-25 average pile-up was ~60-64 (reviewer recollection, UNVERIFIED), which slightly favours a higher B.
- **C7.** P5 physics. A pair at β ≈ 0.15 has only (γ−1)M ≈ 0.011 M of kinetic energy (≈ 14 GeV at m_Q = 500 GeV), while it loses ≳ 10× MIP per charge in the calorimeters and the solenoid. The "β ≳ 0.15 reaches the muon system" threshold comes from 2601.20063 single-HSCP masses. For the two-charge pair (with internal motion raising the mean dE/dx), the effective threshold may be higher. W2/W3 should compute the range explicitly; [A8] could mention it.

---

## 6. Items checked and found correct in v2 (no action)
- Statistical method in §6.1 (expected CLs at the Poisson-median n_obs; the normal approximation above B = 300).
- Exec-summary reach and gain ranges.
- The §6.1 caveat on Knapen's 25 ns cut.
- The §10.4 Facts and resolution plan, including the SampledMode note.
- The §11.3 CR1/VR3 data sources and the D18 fallback.
- The §13 closure-test plan and pre-stated geometry-transfer tolerance.
- Label registry additions A8, A9 and D18.
- The 18-point edge count and all derived CPU/storage figures.
- SREQ §5 RAW and pick-events queries.
- OQ Q1, Q3, Q5 and Q6 match STRAT.

Sources consulted on the web: [CMS, Measurement of the Z boson differential production cross section using its invisible decay mode, arXiv:2012.09254](https://arxiv.org/abs/2012.09254). The PDF text is cached at `../research/cache/pdf/2012.09254.txt`.
