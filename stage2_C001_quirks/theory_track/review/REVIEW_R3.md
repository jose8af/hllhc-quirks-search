# REVIEW_R3: fresh round-3 review of THEORY_GAPS_SYNTHESIS v3

Reviewer: R3 (fresh; I had not seen this work before). Date: 2026-10-08.

**Under review:** `outputs/THEORY_GAPS_SYNTHESIS.md` (v3, 1018 lines). I also used v1/v2, `review/CRITICAL_REVIEW_R1.md`, `CONSTRUCTIVE_REVIEW_R1.md`, `REVIEW_R2.md`, T1-T6 (spot reads), and `figures/R2_li_*_out.txt`.

**My code:** `code/R3_lit_numbers.py` (no simulation, < 1 s). It records the figure readings below and recomputes the R2 γ* table. Output: `figures/R3_lit_numbers_out.txt`.

**Primary sources opened**, from `../research/cache/pdf/` text plus rendered figures:
- 0805.4642 (KLN) §2.5, §3.2, §4.1, §5;
- 1703.00912 (Farina-Low) Eq.1, Tab.II, p.4;
- 1708.02243 (Knapen et al.) §II-IV, App.A;
- 1811.08903 (Evans-Luty) §2-6, Figs.3-5 (rendered);
- 1911.02223 §III, V;
- 2002.07503 §IV-VIII, App.C-D, Fig.4 (rendered), Tab.I;
- 2108.06748 §4-5;
- 2404.13814 (grep only);
- 2410.00269 (Sha et al.) §III, §V;
- 2512.20696 abstract, §4;
- 2607.26195 (FASER) full text, Figs.4-5 (rendered), App.A;
- 1008.3547 (D0) abstract and text.

**Classes:**
- **A**: wrong or misleading claim;
- **B**: weakens a result, or credit is missing for a result claimed as new; must fix;
- **C**: polish.

---

## 0. Verdict

**ITERATE.** Counts: **0 A, 6 B, 9 C.**

**The R2 fixes are genuine.** All R2 A/B items are fixed in substance, and no R1 fix has regressed (§1). The physics core is honestly stated: the causal string is validated, the Li method has a γ*-dependent deficit, no new exclusion has been derived, and truth-level and realistic numbers are kept apart.

**What keeps v3 from PASS is literature credit, which neither earlier round audited** (§2):
- **R3-B1. FASER's exclusion is misread as a flat ≈ 0.11-0.18 TeV.** The real contour is C-shaped: ≈ 57 GeV at 0.3 keV, 105 GeV at 1 keV, 179 GeV at 10 keV and ≈ 65 GeV at 100 keV. The conclusion drawn from it, "the stopped-pair update beats FASER/D0 only if B ≲ O(10)", is therefore wrong for Λ ≲ 2 keV and Λ ≳ 50 keV. There, even the pessimistic background case improves on the existing limit.
- **Four ranked items present published ideas or results as new, without credit:**
  - **R3-B2.** Li et al. already showed that the numerical thickness is roughly independent of m_Q, falls roughly as Λ⁻² at 0.2-0.6 keV, and scales linearly with q.
  - **R3-B3.** Knapen et al. already proposed the Δφ(MET, plane) cut (S-5).
  - **R3-B4.** Sha et al. already fit tracks under a quirk hypothesis and used χ²_quirk/χ²_helix (S-7).
  - **R3-B6.** "A discovery implies a reheating bound", including T_RH ≲ m_Q/25, is the headline of 2512.20696 (S-15).
- **R3-B5. Material simulation.** "No published quirk propagation includes stochastic material effects" ignores the ATLAS/FASER Athena Geant4 extension, which uses "standard Geant4 electromagnetic processes" for material interactions [2607.26195 App.A].

None of these changes a number in the physics core. All are text fixes of an hour or two. The pieces that remain genuinely new are listed in §2.

---

## 1. Task 1: are the R2 items fixed? (and R1 regression check)

### 1.1 R2 items

| Item | v3 location | Fixed? | Comment |
|---|---|---|---|
| **R2-A1**: stopped-pair recast framed as novel | "What changed in v3" 1; Bottom line; S-8 "Prior work (credit)"; §4.5 preamble and first row; §4.6; P6 (retitled "update"); §8 step 2; §10.2 | **Yes** | E-L is credited for the recast, the CMS stopping model, the lifetime-dependent trigger fraction, the 300 fb⁻¹ naive and optimised projections, the HGCAL remark and the 8b4e remark. I checked each against 1811.08903 (§3 below). "First LHC limit" is gone. Residual wording in three places (R3-C1) |
| **R2-B1**: "Li ≈ 15 % low" is a single-γ* result | §0 item 2, §0.2 item 3, VERIFIED table, S-1 table/(ii)/(e), X-2, X-13, §3 rows 22-23, §4.1 rows §4.2/V3/V5/§12, §4.3, P1, §6, §7 | **Yes** | γ* qualifier everywhere; 0.85 target replaced by an event-by-event comparison in γ* bins. Two details of R2's data were not carried over (R3-C4, R3-C5): at γ* = 3 *all 5* events have different hit counts, and the hit-residual and step-fraction guidance is still γ* = 1.28-based |
| **R2-B2**: existing E-singlet exclusions missing | Box A new row; Box A "Below/above"; §4.5 preamble, HSCP and monojet rows; §10.2 | **Yes, but one number is wrong** | Farina-Low Tab.II (650/150/–; scalar 350/60), D0 (107 GeV, 10 keV-1 MeV), FASER (179 GeV at 10 keV; "300 eV < Λ < 100 keV") and E-L (negligible above 0.15 keV) all check. **The added "≈ 0.11-0.18 TeV across the range" for FASER is a misreading of Fig.5 → R3-B1.** The Farina-Low monojet details are slightly off (R3-C3) |
| **R2-B3**: Run-2+3 headline used rejected assumptions | §0, §1 table, S-8, §4.5, §4.6, P6, §8 | **Yes** | 0.15-0.35 TeV everywhere, matching the S-8 table. The comparison with FASER/D0 built on top of it inherits R3-B1 |
| **R2-B4**: smeared-vs-truth edge shift | §0 item 3 (v2 list), Bottom line, Box A, ranked S-3, S-2 "Reading the table", S-3 window, §4.1, §4.4 Q9, §10.1.3 | **Yes** | "Edge undefined until set at fixed background efficiency" is stated consistently. S-2 exploitation (c), "still 0.60-0.73 at 0.3-0.45 keV", could drop "still" (trivial) |
| R2-C1…C9 | §10.2 | Yes | Checked C1 (53-80 µm; 4/6; labSS ×1.5-75), C2, C3 (×2 note), C4 (0.1-5 µs, peak 0.5 µs: confirmed on the rendered E-L Fig.4 left), C5, C6, C7, C8 (T. Nelson; ×1.7 vs ×1.9) and C9. All applied |

### 1.2 R1 regression spot-check

- **Withdrawn v1 numbers.** ×0.04-60, 0.2-35 mm, 140-570 µm and 0.65 TeV appear only in withdrawal, labSS or "v1 value" contexts (l.46, 214, 233, 440, 451, 686, 831). No stale use.
- **Errata.** The T2 erratum box is present. The T3 one was confirmed by R2; I did not re-read it.
- **Labels kept:** truth level (S-2, S-3, Box A), "against random planes only" (S-5), measurement 1-3 % / 0.5-1.5 % MET-scale limited (S-4), "idealised upper bound" (S-7), and the VERIFIED/UNVERIFIED table with the γ* qualifier.
- **R1-critical A-3** (§3.0 "did / did not test") is intact, with rows 22-23 added.
- **No regression found.**

---

## 2. Task 2: literature credit and novelty audit

Method: for each claimed-new result I grepped the cache, then read the relevant passages. I did this for multiple scattering, material, thickness, MET/missing, Δφ, timing, stopped, fit/χ², mass measurement, degeneracy, doublet, resonance, reheating and exclusive. Key figures were rendered.

### 2.1 Ranked gaps

| ID | Claim presented as new (v3) | Prior literature found | Status | Action |
|---|---|---|---|---|
| S-1 | Causal string validated against an independent NG solver; converged Li deficit γ*-dependent; printed Li step unconverged; labSS unusable | No published comparison of a straight-string integrator with a causal or NG string, and no convergence study. KLN §3.2 assert the CM string stays straight and say "it would be useful to check this by direct simulation" [0805.4642 l.537-541]. E-L state "retarded time corrections can also be safely neglected" [1811.08903 §2 l.229]. The causal construction is the Athena code (credited) | **NEW** | Cite KLN's call for a check and E-L's no-retardation statement as the claims S-1 tests (C7) |
| S-2 | "No published quirk propagation includes stochastic material effects"; MS floor 11-22 µm; per-hit resolution | FASER: "standard Geant4 electromagnetic processes describe material interactions" in the Athena quirk extension [2607.26195 App.A]. TH l.251 and T5 l.220 already noted that this probably includes MS. Knapen evaluated Δs on pixel-centre hits with 2× SCT resolution [1708.02243 l.286-292]. Sha et al. smear hits by 1 mm [2410.00269 §V H]. No paper quantifies MS on quirk observables | **PARTLY KNOWN** (statement too strong; quantification NEW) | **R3-B5**; Knapen's detector-level Δs in C7 |
| S-3 | "What is new (not in Li App.C): (i) local exponents Λ^−1.6…−2.0 with ~m_Q independence"; formula fails at ≳ 2 keV; thickness ∝ qB | Li et al. 2002.07503: (a) §V text: "the thickness dependence on m and p_T is mild" (numerical); (b) Fig.4 left: m = 100 and 500 GeV histograms coincide at Λ₀ = 632 eV, and the modes at 200 eV / 632 eV / 2 keV ≈ 600 / 65 / 15 µm, i.e. Λ^−1.9 (0.2→0.63 keV) and Λ^−1.3 (0.63→2 keV) [R3 reading, `R3_lit_numbers.py`]; at 2 keV their numerical thickness is ×50 the formula; (c) §V.A and conclusions: "thickness is linearly proportional to the quirk charges". Li attribute D_N/D_A to hit sampling and system rotation (App.C), not to crossings | **PARTLY KNOWN** | **R3-B2.** Still new: exponents measured with a validated propagator at 1-10 keV; the B ln(1/B) non-linearity and its near-miss crossing origin (Li's "linear in q" holds only to the ≈ 10 % level of 1 + 0.10 ln 3); the MS floor; the corrected window |
| S-4 | Degeneracy theorem; recoil-based (m_Q, Λ) measurement | No statement of the theorem found. Published claims it **refutes**: 2108.06748 §5, "after obtaining the oscillation amplitude and oscillation period … one can infer the confinement scale, quirk mass" [l.1119-1121]; Knapen, "fitting a quirk trajectory … obvious way to try to measure the mass and string tension" and "dE/dx will be important to measure the mass and string tension" [1708.02243 l.481-483, App.A] (the latter already cited in X-8) | **NEW** | Cite 2108.06748 §5 as a published claim corrected (C6); this strengthens P2 |
| S-5 | MET-strip alignment, type N | Knapen et al. §IV: residual background "can easily be removed through … a Δφ requirement between E̸_T and n₃" [1708.02243 l.471-473]. KLN §4.1: "careful examination of the signal events in the missing p_T direction can reveal the presence of 'quirky' tracks" [0805.4642 l.631-633]. Not cited in S-5 or P2 | **PARTLY KNOWN** (idea known; quantification NEW) | **R3-B3** |
| S-6 | Timing medians, per-layer losses, ≈ 3 hits per layer | Knapen applied a 25 ns timing cut [1708.02243 l.496-497]. Li App.D/Tab.I show up to 10 hits per layer and F(n_hit^max > 2) rising with m/p_T: 37 % at m = 500 GeV [2002.07503 Tab.I] | Correction of the project plan; X-11 credits Li | OK. X-11's "Li's fraction is for lighter, faster pairs" should note that Li Tab.I already gives 37 % for 500 GeV (C7) |
| S-7 | Quirk-hypothesis χ², global fit | Sha et al. §V: each track is fit under the quirk hypothesis (pair four-vectors fit with their propagator) and the helix hypothesis; χ²_quirk/χ²_helix plus a back-to-back cut keeps 94 % of quirks and removes all SM tracks in their sample [2410.00269 l.655-678]. Knapen: "fitting a quirk trajectory to the hits identified" [l.479-480]. Neither is cited in S-7 | **PARTLY KNOWN** (concept known; causal 9-parameter global fit, no-Kalman linearity window, predictive OT error, seeding regimes and non-monotonic separation NEW) | **R3-B4** |
| S-8 | Stopped-pair update | E-L 1811.08903 (now credited in full) | **KNOWN method; update** | OK |
| S-9 | Athena MaxSteps killer | — (code reading) | NEW (configuration) | OK |
| S-10 | Merged pair 9-21× MIP; "'≥ 2× MIP' comes from FASER and D0" | D0 did *not* assume 2× MIP. They integrated each quirk's deposit along its trajectory per CM displacement, giving "≳ 15 MeV/cm (≈ 4× MIP in Si) with a distribution substantially wider" [1008.3547 p.2]. That is the method of T3 §8. KLN and Farina-Low describe the merged pair as "a single highly-ionizing straight track" [1703.00912 l.64-65]. E-L fn.7 flags "a straight, highly-ionizing track" as unaddressed for monojet | **PARTLY KNOWN** (CMS-central number NEW) | R3-C2 |
| S-11 | Conventions, closed forms | Lattice ratios credited. Li §IV already computes the number of periods n_T in the CMS tracker [2002.07503 §IV]; Box B's N_osc ≈ 12 (Λ/keV)² is a cleaner closed form of the same quantity | Documentation; mostly credited | Cite Li §IV for n_T (C7) |
| S-12 | Mean energy loss as a first-order trajectory effect | Li et al. include the ionisation force in the EoM [2002.07503 l.157; 1911.02223 l.169]. 2108.06748 §4.1 computes the angular momentum induced by the ionisation force | PARTLY KNOWN (the OT-hit-shift quantification is NEW) | C7 |
| S-13 | ISR modelling | FASER ISR reweighting (cited) | Known; not claimed new | OK |
| S-14 | GUT ladder → doublets invisible; monojet | Ladder from KLN §2.5 (credited). No treatment of doublet E-W splitting or invisibility found in the 10 core papers. Harnik-Kribs-Martin treat β-decaying SU(2) quirks (triplets) [1106.2569 abstract] | **NEW** (modest, standard EW physics) | Optional HKM pointer (C7) |
| S-15 | "Cosmology: discovery implies a reheating bound", type N; T_max ≲ m_Q/25 | 2512.20696 abstract: "T_RH ≲ O(100) GeV for the entire 'quirky' parameter space … discovery of quirks at colliders can have far-reaching implications for cosmology". Their condition T_RH ≲ m_Q/25 appears at l.785. S-15 cites 2512.20696 only for the ×2.2 discrepancy | **KNOWN** (headline); PARTLY NEW (window numbers with the SU(2) conversion, T^{21/4} scaling, ×2.2 discrepancy) | **R3-B6** |
| S-16 | Λ ≳ 3 MeV prompt resonance; 0.1-3 MeV displaced band | Narrow resonance at 2m_Q: KLN §5 Eq.5.59. E-L Eq.4.4 gives L_ann(ε) | Signature KNOWN; the limit reading is labelled UNVERIFIED | Credit KLN/E-L (C8) |
| S-17 | \|q\| = 2: Λ_low ×1.4 | Uses Li's thickness ∝ q [2002.07503 §V.A] combined with the causal Λ exponent | PARTLY KNOWN | Cite Li §V.A (C7) |
| S-18 | Trigger/PU/HLT | Experimental | — | OK |
| S-19 | ε(b) | E-L App.B.1 (credited) | PARTLY KNOWN, credited | OK |
| S-20 | Exclusive γγ + PPS | None found in the 10 papers (grep "exclusive / photon fusion / PPS") | NEW | OK |

### 2.2 Papers

| Paper | Claimed novelty | Audit |
|---|---|---|
| P1 | Thickness scaling, crossing mechanism, MS floor, convergence guidance | **PARTLY KNOWN.** m_Q independence, a rough Λ⁻² at low Λ, and q-linearity are in Li 2002.07503 §V/Fig.4. The crossing (B ln B) mechanism, the γ*-dependent Li/causal comparison, convergence guidance and the MS quantification are NEW. Lead with those (R3-B2, R3-B5) |
| P2 | Degeneracy theorem; MET-strip; predictive χ² | Theorem **NEW** (and it corrects 2108.06748 §5). MET-strip and the quirk-hypothesis χ² are **PARTLY KNOWN** (Knapen §IV; Sha §V) (R3-B3, R3-B4) |
| P3 | HL-LHC stopped quirks | PARTLY KNOWN (E-L 300 fb⁻¹ naive and optimised projections). "Partly a refresh" is fair; say "extension of E-L to 3 ab⁻¹ with causal f_stop" (C1) |
| P4 | Cosmology note | PARTLY KNOWN: a comment on 2512.20696. Framed as such; fine once S-15 credits it |
| P5 | Doublet invisibility + monojet | NEW in this literature set (modest) |
| P6 | Run-2+3 update | KNOWN method (E-L), correctly reframed. Its value statement inherits R3-B1 (it is more useful at the Λ edges than v3 says) |

---

## 3. Task 3: numbers that changed in v3, checked against sources

| Number (v3) | Source checked | Result |
|---|---|---|
| Farina-Low (1,1)₋₁ fermion N=2: 650 GeV (Λ = 1 eV), 150 GeV (100 eV), none (1 keV); scalar 350/60 | 1703.00912 Tab.II (text cache) | ✓ exact. Their T = Λ² [Eq.1 text], same convention. Detail: the monojet input is ATLAS 3.2 fb⁻¹ scaled to 12.9 fb⁻¹, and **HSCP**, not monojet, "drive[s] the limits for Λ ≲ 200 eV" [p.4]; v3 §4.5 says monojet is "dominant at Λ ≲ 0.2 keV" (R3-C3) |
| E-L: current OoT limit negligible above 0.15 keV; naive 300 fb⁻¹ ≈ 0.15-0.2 TeV; optimised ≈ 0.7-0.75 TeV to Λ ~ 1 MeV | 1811.08903 Fig.5 left, rendered | ✓ (shaded red only at Λ ≲ 150 eV; dashed red ≈ 0.15-0.2 TeV; dotted red ≈ 0.7-0.75 TeV from 0.3 keV to ~1 MeV). Fig.5 also shows Knapen's planar-hit 300 fb⁻¹ projection (purple, ≈ 0.75 TeV at ~10 keV) |
| E-L trigger fraction ≈ 8-10 % (300-500 GeV, Λ ≳ 300 eV); 21 % long delays; Fig.3 2-3 % at 0.1 µs, ≈ 10 % at 0.5 µs; τ_stop peak ≈ 0.5 µs (0.1-5 µs) | Fig.3 and Fig.4 rendered at 300 dpi | ✓ (300 GeV ≈ 8-9 %, 500 GeV ≈ 10 %; Fig.3 ≈ 2 % at 0.1 µs, ≈ 11 % at 0.5 µs; the Λ = 500 eV τ_stop peak is at ≈ 0.5 µs) |
| FASER: 179 GeV at 10 keV; 300 eV < Λ < 100 keV; 186 fb⁻¹, 13.6 TeV | 2607.26195 abstract, l.390, Fig.4 | ✓ |
| **FASER "≈ 0.11-0.18 TeV across the range" (Box A, R2's reading)** | Fig.5 rendered at 200 dpi | **✗.** The observed contour reaches ≈ 57 / 72 / 105 / 135 / 150 / 165 / 179 / 175 / 155 / 65 GeV at Λ = 0.3 / 0.5 / 1 / 2 / 3 / 5 / 10 / 20 / 50 / 100 keV. "0.11-0.18" holds only at ≈ 1-50 keV → **R3-B1** |
| D0: 107 GeV (N = 2), 10 keV-1 MeV | 1008.3547 abstract | ✓ |
| γ*-dependence 0.97/0.85/0.92/0.69/0.65; single events 0.53-1.36; out-of-plane up to 124 µm; 3 keV 0.855/0.856/0.673 | `figures/R2_li_gamma_out.txt`, `_gamma2_out.txt`, `_fine_out.txt` (re-parsed by `R3_lit_numbers.py`) | ✓ as transcribed. Additional facts (R3-C4): (a) at γ* = 3, **0/5** events have equal Li/causal hit counts (R2 daggered 3), so the 0.65 median compares different hit sets; the matched-hit evidence for "30-35 % at γ* 2-3" rests on γ* = 2 (median 0.68, 4/5 matched); (b) γ* = 1.6 matched-hit median is 0.83, not 0.92; (c) at γ* = 1.05 the hits are not converged even at ×3×10⁻⁴ (max \|Δhit\| 0.1-0.4 mm, still ∝ step), and ×0.003 is 3-7 % off in thickness |

---

## 4. Task 4: overall honesty

- **The executive summary matches the body**, with one exception. "That beats FASER (≤ 0.18 TeV) and D0 (≈ 0.11 TeV) only if the background is cut to O(10) events" (§0.2; also S-8, §4.5 row 1, §10.2 R2-B3) is wrong at the Λ edges (R3-B1). For once the error makes the item look *less* useful than it is.
- **VERIFIED/UNVERIFIED labels are right.** The γ* qualifier is in the VERIFIED cell. External-limit readings (dilepton, monojet) are UNVERIFIED. The FASER row cites "R2's reading" but carries no UNVERIFIED tag; it is now checked and wrong.
- **Still overclaimed: novelty.**
  - The "What is new" lists and Type "N" labels of S-3, S-5, S-7 and S-15 (and P1/P2 content) present published ideas without credit (R3-B2/B3/B4/B6).
  - S-2's literature statement is too strong (R3-B5).
  - Nothing in the *physics* core is overclaimed. The "killed" list, the "no new exclusion" bottom line and the "superseded, not a systematic" framing are sound.
- **Positive omission.** S-4 is stronger than v3 says: the degeneracy theorem refutes an explicit published claim [2108.06748 §5] (R3-C6).

---

## 5. Findings

### A
None.

### B (must fix)

**R3-B1. FASER's exclusion is Λ-dependent (C-shaped), not ≈ 0.11-0.18 TeV across 0.3-100 keV. The "beats FASER/D0 only if B ≲ O(10)" conclusion is wrong at the Λ edges.**

*Where:* Box A ("≈ 0.11-0.18 TeV across the range, R2's reading of Fig.5"); §0.2 Bottom line; S-8 Run-2+3 bullet; §4.5 first row; P6 value; §10.2 R2-B2/B3 rows.

*Evidence:* FASER Fig.5 observed contour ≈ 57 GeV (0.3 keV), 105 (1 keV), 150 (3 keV), 179 (10 keV), ≈ 170 (30 keV), ≈ 65 GeV (100 keV), with D0 at 107 GeV over 10 keV-1 MeV. Against v3's Run-2+3 estimate (0.22-0.34 / 0.17-0.26 / 0.15-0.20 TeV for B = 0 / 10 / ≈ 80):
- the update exceeds the best existing limit **in every background case** at Λ ≈ 0.3-2 keV and around 100 keV;
- it needs B ≲ O(10) only at ≈ 3-50 keV (`figures/R3_lit_numbers_out.txt` §2).

*Fix:* quote the contour (≈ 0.06 TeV at 0.3 keV, 0.11 at 1 keV, 0.18 at 10 keV, ≈ 0.07 at 100 keV). Restate: "beats FASER/D0 at Λ ≲ 2 keV and ≳ 50 keV even with the 2016 background; at 3-50 keV only if B ≲ O(10)". Readings by eye (±5-10 GeV); use the FASER HEPData record [2607.26195 ref.36] for the final numbers.

**R3-B2. S-3/P1 "what is new" includes results already in Li et al. 2002.07503 §V.**

*Evidence:*
- "The thickness dependence on m and p_T is mild" [§V, l.654-658].
- Fig.4 left: m = 100/500 GeV coincide; modes 600 / 65 / 15 µm at 0.2 / 0.63 / 2 keV, i.e. Λ^−1.9 and Λ^−1.3 locally, ×50 above the formula at 2 keV.
- Thickness linear in each quirk charge [§V.A; conclusions].
- v3 S-3 lists "(i) local exponents Λ^−1.6…−2.0 with ~m_Q independence" as "not in Li App.C". That is true of App.C, but not of the same paper. Note also that Li's numbers come from their own integration at an unknown step (S-1), so they are evidence of the qualitative behaviour only.

*Fix:*
- Credit 2002.07503 §V/Fig.4 (and §V.A for the q-linearity used in S-17).
- Re-scope "new" to: the exponent measured with a validated, converged propagator over 1-10 keV in 3.8 T; the B ln(1/B) non-linearity and its crossing origin (Li attribute D_N/D_A to hit sampling and system rotation); the MS floor; the corrected window.
- Update P1's novelty sentence accordingly.

**R3-B3. S-5 MET-strip alignment (type N, P2 content) does not credit Knapen et al. or KLN.**

*Evidence:* Knapen §IV: background "can easily be removed through either a Δφ requirement between E̸_T and n₃" [1708.02243 l.471-473]. KLN §4.1: examine "the signal events in the missing p_T direction" [0805.4642 l.631-633].

*Fix:* say the cut was proposed qualitatively by Knapen et al. What is new is the quantification: the 95 % window 0.15-0.25 rad, ×13-34 against random planes, the B-wobble and fit-error bounds, and the real-background analysis. Change the Type to C + N.

**R3-B4. S-7 quirk-hypothesis χ² and trajectory fit do not credit Sha et al. or Knapen.**

*Evidence:* Sha et al. [2410.00269 §V, l.655-678] fit each track under quirk and helix hypotheses (pair four-vectors fit with their propagator). They use χ²_quirk/χ²_helix plus a back-to-back cut (94 % signal efficiency; all SM tracks removed in their sample). Knapen [l.479-480, l.532-533] proposes fitting a quirk trajectory to the plane-finder hits.

*Fix:* credit both. The new content is the causal-propagator 9-parameter *global* pair fit, the linearity/aliasing analysis (no Kalman), the predictive OT-hit uncertainty, two-regime seeding and the non-monotonic pair separation. Same in P2.

**R3-B5. S-2: "No published quirk propagation includes stochastic material effects" is too strong.**

*Evidence:*
- In the Athena Geant4 quirk extension used by ATLAS and FASER, "standard Geant4 electromagnetic processes describe material interactions" [2607.26195 App.A, l.430-434]. The project's own TH l.251 and T5 l.220 say this probably includes MS.
- Knapen evaluated Δs on detector-level hits (pixel centres, 2× SCT resolution) [1708.02243 l.286-292]. That is a precedent for S-2's "truth vs detector" point, for the ATLAS geometry.

*Fix:* "No published phenomenology study (Knapen, Li, Sha, Evans-Luty) includes MS, and no publication quantifies its effect on quirk observables. The Athena/FASER Geant4 extension uses standard Geant4 EM processes and probably includes MS (UNVERIFIED which processes are attached)". Also add this to P1's novelty statement.

**R3-B6. S-15 (type N; executive summary "A discovery would imply T_RH ≲ 5-40 GeV") presents the headline of 2512.20696 as a finding of this track.**

*Evidence:* 2512.20696 abstract ("T_RH ≲ O(100) GeV for the entire 'quirky' parameter space … the discovery of quirks at colliders can have far-reaching implications for cosmology") and l.785 (T_RH ≲ m_Q/25).

*Fix:* credit 2512.20696 for the implication and for the m_Q/25 condition. The track's additions are:
- the window-specific numbers 5-40 GeV, with the SU(2) T_c/√σ conversion;
- the T^{21/4} (not T⁷) scaling;
- the unresolved ×2.2;
- the observation that only overclosure and SIDM matter in the window.

Change the Type to D/C.

### C (polish)

- **R3-C1. Leftover novelty wording from R2-A1.**
  - §0.2 (ii): "a list of recasts, none of which has been performed" → "none performed by this track (Farina-Low and Evans-Luty recasts exist)".
  - §4.4 Q10: "Stopped-particle recast of CMS 1801.00359 …" needs "(update of Evans-Luty [1811.08903])".
  - P3: "extension of E-L's 300 fb⁻¹ projections to 3 ab⁻¹ with causal f_stop".
  - Title line 1 still says "(v2)".
- **R3-C2. S-10 attribution.**
  - D0 did not use "≥ 2× MIP". They integrated each quirk's deposit along the trajectory per CM displacement, giving "≳ 15 MeV/cm" (≈ 4× MIP in Si) with a wide distribution [1008.3547 p.2]. That is the same method as T3 §8; credit it.
  - "Single highly-ionizing straight track" is KLN / Farina-Low language [1703.00912 l.64-65]. FASER's 2× MIP is for relativistic pairs, which v3 states correctly.
- **R3-C3. §4.5 monojet row and Box A.**
  - Farina-Low's monojet input is ATLAS 3.2 fb⁻¹ scaled to 12.9 fb⁻¹.
  - HSCP, not monojet, dominates at Λ ≲ 0.2 keV; monojet gives a weak (~0.05-0.06 TeV) limit extending to high Λ [1703.00912 p.4; E-L Fig.5].
  - Farina-Low's HSCP/0T limits are cut at Λ = 300 eV for statistics.
- **R3-C4. γ* table details** (§3 last row):
  - say "all 5 events at γ* = 3 have different hit counts";
  - the matched-hit evidence is γ* = 2 (0.68);
  - the γ* = 1.6 matched-hit median is 0.83, so the trend is noisy, not monotonic;
  - "Λ-independent" was tested only at γ* = 1.28, and the γ* dependence only at 1 keV.
- **R3-C5. Validation guidance still at γ* = 1.28** (S-1 (ii)/(e), §4.1 V3/V5).
  - Converged Li vs causal with *matched* hits differ by up to 1.0 mm in-plane at γ* = 1.6.
  - At γ* = 1.05 even ×3×10⁻⁴ of the printed bound is not converged in hits. The required step fraction scales roughly with ℓ_max ∝ (γ*−1), not only with Λ⁻².
  - So "mm-scale OT residuals ⇒ unconverged or labSS" can misfire. Qualify by γ*, and match crossings by index, not nearest time.
- **R3-C6. S-4/P2:** cite 2108.06748 §5 ("one can infer the confinement scale, quirk mass" from amplitude and period) and Knapen's "hit patterns consistent with a common (m_Q, Λ)" as published expectations that the theorem corrects.
- **R3-C7. Precedent credits (one clause each):**
  - KLN §3.2's call for a direct simulation check, and E-L §2's "retarded time corrections can be safely neglected" (S-1, X-13);
  - Li §IV n_T (Box B), Li Tab.I 37 % at 500 GeV (X-11), Li §VIII fixed ŝ (killed list);
  - Knapen Eq.8-9 Δφ ≲ 10⁻³ (precession killed idea);
  - Knapen's detector-level Δs (S-2);
  - Li §V.A q-linearity (S-17);
  - Li/2108.06748 ionisation force in the EoM (S-12);
  - Farina-Low's 0 T search proposal (§4.7 0 T note);
  - Harnik-Kribs-Martin 1106.2569 for β-decaying EW quirks (S-14, optional).
- **R3-C8. S-16:** the prompt narrow resonance at 2m_Q is KLN §5 [Eq.5.59]; E-L Eq.4.4 gives the ε-dependent annihilation length behind the "displaced band". Credit both.
- **R3-C9. S-2 exploitation (c):** "still 0.60-0.73 at 0.3-0.45 keV" → drop "still", since an acceptance gain is not implied (consistent with R2-B4).

---

## 6. What I confirm as correct in v3 (for the record)

- All R2 A/B fixes are in place, and no R1 regression.
- Every E-L number now in v3 matches the rendered figures and text: recast, Fig.3, Fig.4 (trigger % and τ_stop), Fig.5 projections, 40-65 % visible BR, DT/CSC vetoes, 55 % reconstruction efficiency, HGCAL O(90 %), and the 8b4e remark.
- Farina-Low Tab.II, D0 107 GeV, and FASER's 179 GeV and Λ range.
- The R2 γ* numbers as transcribed.
- E-L used a CM-frame straight string [§2 l.227], so "f_stop with the causal string for the first time" (S-8) is correct.
- Genuinely NEW, as far as the 10 core papers plus D0, HKM and KLN show:
  - the validated causal propagator, and the Li-vs-causal comparison with its γ* dependence and convergence requirements;
  - the B ln(1/B) crossing non-linearity;
  - the MS-floor quantification;
  - the degeneracy theorem and the recoil-based measurement;
  - the quantified MET-strip window;
  - the causal global fit with its linearity analysis;
  - timing medians;
  - S-9, S-14 (doublet invisibility) and S-20.

## 7. Files

- `review/REVIEW_R3.md` (this file);
- `code/R3_lit_numbers.py`;
- `figures/R3_lit_numbers_out.txt`.

Figure renders for reading were made in the session scratchpad only (not project files). No background processes are left running.
