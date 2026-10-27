# REVIEW_R2: fresh round-2 review of THEORY_GAPS_SYNTHESIS v2

Reviewer: R2 (fresh; I had not seen this work before). Date: 2026-10-08.

**Under review:** `outputs/THEORY_GAPS_SYNTHESIS.md` (v2, 965 lines), with v1, both R1 reviews, T1-T6, `code/` and `figures/*_out.txt`.

**My code:** `code/R2_li_checks.py`, which reuses R1's Li-literal kernel, `make_event` and `T3_causal.run_causal`. Outputs:
- `figures/R2_li_gamma_out.txt` and `figures/R2_li_gamma2_out.txt`: Li/causal as a function of γ*;
- `figures/R2_li_fine_out.txt`: 3 keV at a finer step.

**Primary sources opened:**
- 1811.08903 (Evans-Luty), full text plus Figs. 3, 4 and 5 rendered;
- 1801.00359 Sec. 3 and 8, Tab. 4;
- 1703.00912 (Farina-Low) Tab. II;
- 1911.02223 Eq. III.6-III.10;
- 2607.26195 Fig. 5 caption and text;
- 1008.3547 model statement.

**Classes:**
- **A**: wrong or misleading claim;
- **B**: weakens a result, must fix;
- **C**: polish.

**Status:** complete. All R2 runs are finished (one 3 keV event was cut by the 15 min cap); no background processes are left running.

---

## 0. Verdict

**ITERATE.** Counts: **1 A, 4 B, 9 C.**

The v2 fix pass is substantial and mostly honest.
- The withdrawn v1 headline is gone everywhere except in explicit "withdrawn" or labSS contexts.
- Every A and B item of both R1 reviews is answered with new work or new text.
- The executive summary now says plainly that no new exclusion was derived.

Two problems remain, both on new v2 material:
1. **R2-A1.** The stopped-pair item, which v2 elevates to "the only route to a literally new exclusion", is framed as novel ("first LHC limit on singlet quirks", "none [of the recasts] has been performed", P6 "A first LHC limit …"). But Evans-Luty [1811.08903] already recast this very CMS search (1801.00359) for this very benchmark (E′, SU(2)_IC). They computed the lifetime-dependent trigger fraction that F1 re-derived, and gave 300 fb⁻¹ projections. FASER and D0 also have limits in the same Λ range. T6 knew this; the synthesis lost it.
2. **R2-B1.** The replacement S-1 number "Li ≈ 15 % low when converged" was measured only at γ* = 1.28. My runs give ≈ 3 % at γ* = 1.05 and ≈ 30-35 % (single events −47 % … +36 %) at γ* = 2-3. Out-of-plane hit differences reach 30-120 µm. It is fine as a median-event statement, but not as the validation target that v2 hands to Phase 2.

Asked explicitly by the orchestrator: does "≈ 15 % low" hold beyond 2 keV? **Yes at 3 keV** (0.855/0.856 converged at ×10⁻³; one event 0.67 with a hit-count mismatch). It is not an unconverged artefact. Its dependence is on γ*, not on Λ.

---

## 1. R1 items: are they genuinely fixed in v2?

### 1.1 Critical review (CRITICAL_REVIEW_R1)

| Item | v2 location | Fixed? | Comment |
|---|---|---|---|
| A-1: S-1 numbers are labSS, not Li | §0 "What changed" 1; S-1 (rewritten); X-2; X-13; §3 rows 15-16, 19; §6; T2/T3 erratum boxes | **Yes** | The withdrawal is explicit and complete. The withdrawn numbers survive only in "withdrawn" or labSS-attributed contexts (grep in §4.3 of this review). The erratum boxes in T2 and T3 are clear. **But** the replacement headline "Li ≈ 15 % low when converged" was measured at a single kinematic point (γ* = 1.28). See R2-B1 |
| A-2: downstream advice would mislead Phase 2 | §4.1 rows §4.2 b1, §9.2, §9.4 V3/V5, §12 (i); §4.2 P-S0/W3/W8; §4.3 | **Yes** | "Never lab-slice; validate against `T3_causal.py`; superseded, not a systematic" is the right advice. V3/V5 still tell Phase 2 to *expect* "Δs ≈ 0.85 × causal". That validation target holds only at γ* ≈ 1.3 (R2-B1) |
| A-3: 35/35 never tested the S-1 premise | §3.0, §3.1 rows 15-21, new counts | **Yes** | It is a good "did / did not test" section. Rows 15-16 are by F1 with R1's kernel ("indep. of T2's code" is right) |
| B-1: "exact" = classical NG; crossing cutoff | glossary; S-1 (i); S-3 "NG validity"; X-13; §4.1 §12 row; §7 item 3 | **Yes** | |
| B-2: truth-level efficiencies; resolution ≈ MS floor | S-2 new sub-section and table; S-3; Box A; §0.2; §4.1 §9.1; §4.4 Q9; §6 | **Yes, quantified.** Interpretation partly overreaches | The per-hit resolutions are computed correctly from the stated pitches (I re-derived them, §2.2). The new claim "the 50 % edge moves below 0.3 keV" compares cuts that have different background rejection. See R2-B4 |
| B-3: ×7-50 already in Li App.C | glossary "d"; S-3 "Credit"; X-2; §4.1 V2; P1 (v) | **Yes** | The credit is correct. 2002.07503 App.C/Fig.8 is quoted as R1 read it; I did not re-open it |
| B-4: material unverified; √(x/X0) check internal | S-2; §3 row 10; §7 item 1; §8 step 3 | **Yes** | |
| B-5: 1 %/0.5 % below the MET-scale floor | §0.2 item 4; S-4 table; §4.1 O6; P2 | **Yes** | It is consistent: δΛ/Λ = ½ δm/m at fixed ℓ₀ = m/σ, so 1-3 % gives 0.5-1.5 %. Minor: R2-C6 |
| B-6: stopped-pair live fraction and background | S-8 (new table), X-5, §4.5, P3/P6, §3 row 21 | **Partly.** The arithmetic is right (§2.3), but the item is reframed wrongly | (i) The lifetime-dependent trigger fraction was already computed by Evans-Luty with the real 2016 fill patterns [1811.08903 Fig.3, Fig.4 right]. v2 presents it as its own correction and does not credit it. (ii) The same 1801.00359 search was already recast for this very benchmark (E′, SU(2)_IC) [1811.08903 Sec.4, Fig.5]. v2 calls the recast "first" and "none has been performed": **R2-A1**. (iii) The background is not scaled to the 1801.00359 short-lifetime search window (R2-C3). (iv) The Run-2+3 headline upper end needs a delay ≫ 1 µs and zero background (R2-B3) |
| B-7: ranking and paper plan | §1 table (Type column), S-1, §5 P1, §10.3 | **Yes (disagreement argued)** | Keeping S-1 at rank 1 as "validated production propagator" is defensible |
| B-8: T2 Λ^−2.5 and the 4-event tables | X-1; T2 erratum; §7; §10.3 | **Mostly** | Λ^−2.5 retired. The Li covariance re-test is not done; this is openly declared and acceptable |
| C-1 … C-9 | §10.1 | Yes | C-8: two R1-derived numbers are still slightly off (R2-C1) |

### 1.2 Constructive review (CONSTRUCTIVE_REVIEW_R1)

| Item | v2 location | Fixed? | Comment |
|---|---|---|---|
| A1: headline vs small effect on sensitivity | §0.2 "Bottom line" and the reach paragraph | **Yes** | |
| A2: no new exclusion stated; UNVERIFIED mixed with verified | §0.2 Bottom line; VERIFIED/UNVERIFIED table; S-16 | **Yes for the original item**, but a new novelty overclaim appears | "Fastest route to a literally new limit" is fine. "First LHC limit on singlet quirks" and "none has been performed" are not (R2-A1). The VERIFIED column lists "Li/causal 0.84-1.05" without saying it was measured at one γ* (R2-B1) |
| A3: MET-strip ×13-34 vs real background | S-5 "What is expected against the real background"; §4.1 O7; §8 step 8 | **Yes** | The reasoning is sound: PU and UE fakes are uncorrelated with the MET, so the geometric factor applies per candidate; for W(τν) and lost-lepton events, MET and the visible τ/lepton are collinear, so the gain is ×≈1-3. "Do not put ×13-34 into a background estimate" is the right instruction |
| B1: consolidated Λ answer | Box A | **Mostly** | Box A omits the **existing exclusions** for the E singlet in the (m_Q, Λ) plane: Farina-Low, Evans-Luty, D0 and FASER (R2-B2) |
| B2: oscillation length; scalars | Box B; §0.2 item 2 | Yes | Numbers check against T2 (§2.5) |
| B3: PU-vertex ambiguity | S-18 | Yes (note) | Arithmetic checks: 200/(√(2π)·4.5 cm) ≈ 18 /cm; 0.35 expected in ±100 µm ⇒ P ≈ 30 % |
| B4: HLT paths | S-18 table | Yes (flagged UNVERIFIED) | |
| B5: Run-3 vs Phase-2; Run-3 stopped recast | §4.6; S-8 | Yes | The Run-3 stopped-recast number inherits R2-A1/B3 |
| B6: ML features | S-7 | Yes | |
| B7: SBI | S-4 | Yes | |
| B8: recast table | §4.5; P6 | **Table yes; content partly wrong** | It says "none has been performed" while the first row (CMS stopped particles, 1801.00359) was recast for E′ quirks by Evans-Luty, and T6 says so [T6 l.71] (R2-A1). The HSCP and monojet rows omit Farina-Low's existing recast of the same searches for (1,1)₋₁ quirks [1703.00912 Tab.II] (R2-B2) |
| B9: S-7 idealised | S-7; §1 table | Yes | |
| B10: P1 novelty | §5 P1 | Yes | |
| B11: glossary | §0.1 | Yes | |
| C items | §10.2 | Yes | |

**Summary of §1.** Every R1 A and B item is addressed in substance, not just acknowledged. The weak spots are the stopped-pair item (B-6/B8), where the fix introduced a new claim about the literature that is wrong, and the "≈ 15 %" replacement number for A-1, which is narrower than stated.

---

## 2. Scrutiny of new or changed v2 claims

### 2.1 S-1 re-scoped: Li method vs causal string

**What I checked.** R1's Li-literal kernel, against the paper text [1911.02223 Eq.III.6-III.10]:
- the CM-simultaneity step-ratio condition (Eq.III.7);
- ŝ from Eq.III.8-9;
- the Kang-Luty force;
- the printed step bound.

The kernel is a faithful transcription. I also re-read every number of the S-1 table against `figures/R1_li_literal_out_a/b/c.txt`, `F1_standin_out.txt`, `F1_li_phase_out.txt` and `R1_li_ms_out.txt`. They match, apart from R2-C1.

**Key observation.** *Every* Li-vs-causal comparison behind S-1 uses one kinematic point: m_Q = 500 GeV, γ* = 1.28, p_T = 300 GeV (`R1_conformal_ng.make_event` defaults; T2's `make_event` is the same recipe). The striking regularity of the converged ratio (most events 0.84-0.86) suggests a kinematic origin. Neglected retardation and curvature should grow with the internal velocity β*.

**R2 test 1: γ* dependence** (`R2_li_checks.py gamma`; Λ = 1 keV; m = 500 GeV; p_T = 300 GeV; 5 events per γ*, seed 23; converged causal settings as R1; Li at ×0.01 and ×0.003 of Eq.III.10, plus finer steps at γ* = 1.05):

| γ* | Li step (finest) | Li/causal per event | median | max out-of-plane hit difference (Li vs causal) | converged? |
|---|---|---|---|---|---|
| 1.05 | ×0.0003 | 0.969 / 0.970 / 0.969 / 0.969 / 0.967 | **0.97** | 0.15-5.4 µm | yes (×0.001 → ×0.0003 changes ≤ 1.5 %); ×0.003 is *not* converged here (1.00-1.04), ×0.01 gives 1.16-1.21 |
| 1.28 (R1/F1 point) | ×0.003 | 0.841 / 0.845 / 0.845 / 0.859 / 0.884 | **0.85** | 3-25 µm | yes (×0.01 = ×0.003) |
| 1.6 | ×0.003 | 0.947 / 0.943† / 0.735 / 0.741 / 0.921 | **0.92** | 2-60 µm | 4/5 (ev2 moves 0.89 → 0.735) |
| 2.0 | ×0.003 | 0.678 / 0.897† / 0.675 / 0.688 / 1.073 | **0.69** | 12-60 µm | yes |
| 3.0 | ×0.003 | 0.525 / 1.065† / 0.645 / 0.634† / 1.361† | **0.65** | 34-124 µm | yes (×0.01 = ×0.003) |

† Li and causal hit counts differ (e.g. 47 vs 58, 61 vs 94), so the thickness ratio partly reflects different hit sets.
Source: `figures/R2_li_gamma_out.txt`, `R2_li_gamma2_out.txt`; ~10-30 s per event.

**Result:**
- The converged Li thickness deficit is **not a constant 15 %**. It is ≈ 3 % at γ* ≈ 1.05 (the near-non-relativistic limit, where a straight string is nearly exact), ≈ 15 % at γ* = 1.28, and ≈ 30-35 % (median) at γ* = 2-3.
- At γ* = 2-3, single events range from −47 % to +36 %, and out-of-plane hit differences reach 30-120 µm (v2: "≤ 10.5 µm").
- The trend is what neglecting retardation and curvature should give (corrections grow with β*).
- 5 events per point is small, but the γ* = 1.05 / 1.28 / 2-3 separation is far outside the event-to-event scatter at fixed γ*.
- For the triggered spectrum (median γ*−1 ≈ 0.27, 84th percentile γ* ≈ 2.0-2.5 [T2]), "≈ 15 %" is right for the *median event*. The per-event deviation spans ≈ 3-50 % in either direction.
- This does not revive the v1 claim: these are still tens of per cent, not ×4-60, and the causal string remains the reference. But "Δs ≈ 0.85 × causal" is not a valid **validation target** for external samples (§4.1 V3/V5, S-1 exploitation (e)). A converged CM-simultaneous code compared event by event at γ* ≳ 2 would fail it, and the Phase-2 team might wrongly conclude the code is broken.

**R2 test 2: does the 3 keV ratio converge?** (`R2_li_checks.py fine`; R1's seed-11 events, Li at ×0.001 of the printed bound.)

| event (seed 11) | causal | Li ×0.01 [R1] | Li ×0.003 [R1] | Li ×0.001 [R2] | ratio at ×0.001 | max out-of-plane Δhit at ×0.001 |
|---|---|---|---|---|---|---|
| ev0 | 2.23 µm [22 hits] | 2.58 [28] | 1.91 [22] | 1.91 [22] | **0.856** | 1.8 µm |
| ev2 | 5.54 [24] | 4.85 [30] | 3.73 [22] | 3.73 [22] | **0.673**† | 3.4 µm |
| ev5 | 7.61 [28] | 6.62 [34] | 5.72 [30] | 6.51 [28] | **0.855** | 5.3 µm |
| ev1 | — | — | — | not finished (900 s cap) | — | — |

† hit count 22 vs 24.
Source: `figures/R2_li_fine_out.txt`, ≈ 3.5 min per event.

**Result:**
- At 3 keV the Li integration *does* converge at ×0.001-×0.003. Two of three events give exactly the γ* = 1.28 value, 0.855-0.856. The third is 0.67 but with a different hit count.
- So "≈ 15 % low when converged" **holds at 3 keV** for this kinematic point. It is not merely an artefact of the unconverged 3 keV runs.
- v2's "not reached at 3-5 keV" (§0.2, S-1, §7 item 3, §10.3) should read "reached at 3 keV with ×10⁻³ of the printed bound (≈ 3×10⁸ steps per event); not tested at 5 keV below ×10⁻²".

**Assessment of the other S-1 sub-claims:**
- *"Unconverged at the printed step"* (×0.8-20 at 0.6-3 keV): confirmed from R1's tables.
- *"Convergence harder at 3-5 keV"*: true in the sense that the needed fraction of the printed bound shrinks. The ESTIMATE that it falls as Λ⁻² (because b_odd ∝ Λ⁻⁴ while the printed bound ∝ Λ⁻²) is plausible. "Not reached at 3-5 keV" is wrong for 3 keV, where all three tested events converge at ×0.001-×0.003 (test 2).
- *"labSS/Li = 1.6-73"* (F1_standin, T2's seed-7 events): confirmed from `F1_standin_out.txt` (1.63-72.6; 0/12 within ±50 %).
- *2 keV mm hit differences explained as Li Euler phase drift*: the evidence supports it.
  - From ×0.003 to ×0.001 the maximum |Δhit| falls from 0.2-9.8 mm to 0.07-0.53 mm.
  - The out-of-plane component stays ≤ 10.5 µm.
  - Plane normals agree to ≤ 43 mdeg.
  - Mismatched hit counts appear exactly where the large "differences" sit.

  Caveat: "the residual 0.1-0.5 mm is an upper bound on the converged Li-causal difference" is a heuristic. With first-order error ∝ step, the ×0.001 residual is consistent with being *all* integration error. Then it is an upper bound only if the error is monotonic in step, which is not shown. The wording should be "consistent with pure integration error". C-level.
- *Li + MS*: the 10 keV row (33 vs 22 µm) uses Li at ×0.01, which v2 itself says is unconverged at that Λ. Keep it out of any "Li + MS ≈ causal + MS" statement; v2 already flags it.

### 2.2 Resolution-aware coplanarity (S-2, F1_smear)

**Method check.**
- σ_n² = (n·φ̂)²σ_rφ² + n_z²σ_z² is the correct out-of-plane variance for a point measured in (rφ, z) at known r.
- For a 2S strip, the n_z σ_z term encodes exactly the information a z-less hit carries: whether the plane-cylinder intersection z(φ) falls inside the strip.
- The resolution-weighted plane fit, iterated reweighting, and t_est defined by Σ res²/(s² + t²) = ndf are all sound.
- Uniform (binary) errors make the χ² slightly non-Gaussian; that is harmless here.

**Numbers re-derived:**
- IT: σ_rφ = 25/√12 = 7.2 µm, σ_z = 100/√12 = 28.9 µm. With |n_z| = 0.56 and |n·φ̂| ≈ 0.83 this gives σ_n ≈ √(6.0² + 16.2²) ≈ 17 µm. ✓
- PS: 0.56 × 1.5 mm/√12 = 0.24 mm. ✓
- 2S: 0.56 × 5 cm/√12 = 8.1 mm. ✓
- The pitches (IT 25 × 100 µm², PS 100 µm × ≈ 1.5 mm, 2S 90 µm × 5 cm with no stereo) agree with what I know of the Phase-2 design (UNVERIFIED here; TDR not opened by anyone). "2S has no stereo" is correct: the two sensors are parallel, for p_T stubs.
- Pixel charge sharing and ToT interpolation would improve the IT resolution below pitch/√12; the binary assumption is conservative. Fine.

**Interpretation** (see R2-B4).
- The efficiency numbers are correct as computed. The *conclusion* drawn in §0.2, Box A, the S-3 table ("realistic resolution: below 0.3 keV") and §10.3 ("we find the edge moves *down*") compares a 100 µm cut on t_est with a 100 µm cut on the truth Δs. These are different observables with different background rejection.
- An IT-only coplanarity test is weak against the most common two-track background: any two straight tracks from the PV are exactly coplanar with it.
- The rφ sagitta of a helix at r = 14.6 cm is r²qB/(8p_T) ≈ 0.32 mm (p_T/10 GeV)⁻¹. So two prompt tracks with p_T ≳ 100 GeV are coplanar with the PV to ≲ 30 µm over the IT, and pass t_est < 100 µm.
- Hence "60-73 % pass at 0.3-0.45 keV" is not, by itself, an acceptance gain. The lower edge is undefined until the cut is set at fixed background efficiency. This is where the outer-layer non-helicity (rφ) carries the discrimination.
- v2 does say "(iii) background rejection of coplanarity is correspondingly weaker" and "net effect on reach not computed". But the headline sentences state the edge shift as a finding.

### 2.3 Stopped-pair reach (S-8, F1_stopped)

**Arithmetic.**
- I reproduced the HL-LHC, f_stop = 1 %, live = 0.21, B = 0 point by hand: N = σ·3000·0.01·0.21·0.55·0.83·0.4 = 1.15 σ[fb]. Setting N = 3 gives σ_E(N_IC = 1) = 1.09 fb. Log-interpolating T6's table gives m = 609 GeV, against the code's 0.61. ✓
- The live-fraction toy (0.027/0.050/0.086/0.113 at τ = 0.1/0.2/0.5/1 µs) is consistent with Evans-Luty's exact-fill calculation [1811.08903 Fig.3: ≈ 2-3 % at t = 0.1 µs, ≈ 10 % at 0.5 µs, ≈ 21 % at ≳ 1 µs, for a fixed decay time]. It is also consistent with their trigger fraction for stopped E′ pairs at Λ ≳ 300 eV, 8-10 % at 300-500 GeV [Fig.4 right].
- BR_vis 0.4-0.65, ε_reco 0.55 and vetoes 0.83 (12.3 % DT + 5.6 % CSC) match 1811.08903 Sec.4.
- Background 11.4 events in 586 h of livetime matches [1801.00359 Tab.4]. The search lifetime range starts at 10⁻⁷ s [Sec.8], so "acceptance starts at 100 ns" is right.
- All S-8 table cells match `F1_stopped_out.txt`.

**Inputs that are wrong or uncredited:**
- (a) **The recast already exists (R2-A1).** Evans-Luty [1811.08903] "recast an existing CMS search for out-of-time decays" (abstract). The search is 1801.00359 at 38.6 fb⁻¹ [ref. 34 there]. The benchmark is *E′-like (1,1) quirks with SU(2)_IC*, i.e. exactly this project's benchmark [Fig.5 left].
  - They give the current limit (solid red), a naive 300 fb⁻¹ projection (dashed, ≈ 0.15-0.2 TeV for Λ ≳ 300 eV, read from the figure), and an optimised |η| < 3, zero-background 300 fb⁻¹ projection (dotted, ≈ 0.7-0.75 TeV up to Λ ~ 1 MeV).
  - FASER's Fig.5 shows "Reinterpreted CMS OoT" among the previously excluded regions [2607.26195].
  - T6 itself says "Evans-Luty recast CMS 1801.00359" [T6 l.71].
  - v2 nevertheless says:
    - "That would still be the first LHC limit on singlet quirks across Λ ≈ 0.3 keV to ~MeV" (S-8);
    - "Recasts … (none has been performed)" and "Expected: … the first LHC limit on singlet quirks across Λ" (§4.5);
    - P6 is titled "A first LHC limit on singlet quirks from stopped-particle searches".

  What is true: the existing E′ out-of-time limit at Λ ≳ 300 eV is negligible (the shaded region in E-L Fig.5 sits at m ≲ 0.1 TeV and Λ ≲ 0.15 keV). A full-Run-2(+3) update with the causal f_stop would therefore be a *stronger* central-detector limit in that range. "First LHC limit" is also wrong because FASER (an LHC experiment) already excludes 0.11-0.18 TeV for 0.3-100 keV, and D0 excludes ≈ 0.11 TeV for 10 keV-1 MeV [1008.3547].
- (b) **The delay.** v2 says "Evans-Luty give 0.1-100 µs [Fig.4]". That range spans all Λ, including the terminal-velocity regime at 50 eV. For Λ ≳ 300 eV, E-L's τ_stop for 500 GeV E′ peaks at ≈ 0.5 µs (range ≈ 0.1-5 µs). This is consistent with F1's τ = 0.1-0.5 µs choice but should be quoted that way (R2-C4).
- (c) **The background is not scaled to the short-lifetime search window.** For τ shorter than an orbit, 1801.00359 searches only in a window of 1.3τ after each collision and scales the cosmic and noise backgrounds by the live time inside it [Sec.8].
  - My count for a 72-bunch / 8-gap scheme: the window covers ≈ 15-20 % of the livetime at τ = 0.1 µs and ≈ 45 % at τ = 0.5 µs.
  - So the "B ≈ 230 (2016 selection), τ = 0.5 µs" column overstates the 2016-selection background by ≈ ×2.
  - The bracket B = 0/10/230 still contains the answer, so the headline range is not affected (R2-C3).
- (d) **Run-2+3 headline 0.2-0.4 TeV (R2-B3).**
  - The 0.4 end is the τ ≫ 1 µs, B = 0 column, which S-8 itself rejects as the v1 assumption.
  - With v2's own preferred τ = 0.1-0.5 µs: 0.22-0.34 TeV at B = 0, 0.17-0.26 at B = 10, ≈ 0.15-0.20 at B ≈ 80.
  - The low end sits *at or below* FASER's 0.11-0.18 TeV, and it is comparable to E-L's naive 300 fb⁻¹ projection.
  - The executive summary should quote ≈ 0.15-0.35 TeV and say that it improves on FASER/D0 only in the favourable (low-background) case.
- (e) **Missed handles worth one line (C):**
  - E-L Sec.5 note that HGCAL timing could raise the triggerable fraction for forward deposits to O(90 %).
  - The filling scheme matters a lot for τ ≲ 0.5 µs, because short gaps after every few bunches increase the short-lifetime acceptance.
  - Both bear directly on the "sub-µs delay" problem that drove the downgrade.

### 2.4 Measurement and MET-strip

- *1-3 % (m_Q) / 0.5-1.5 % (Λ), MET-scale limited*: consistent with T4 §4.3-4.4 and internally consistent: m = p_T/(2γ*(βγ)_T) gives δm/m = δMET/MET, and Λ ∝ √(m/ℓ₀) gives half of it.
  - One unlisted bias: T4 assumes "true MET = p_T(QQ̄)" because the pair deposits ≲ 5 GeV in the calorimeters [1911.02223 Sec.V via T4 l.277].
  - On a 200-300 GeV recoil that is a one-sided ≲ 2 % bias, the same size as the quoted scale floor. It is correctable but should be listed (R2-C6).
- *MET-strip vs real backgrounds*: the S-5 qualitative estimate is sound (see §1.2 A3). "Roughly a quarter to a third" for W(ℓν)/τ in monojet selections is labelled recalled/UNVERIFIED, which is fine.

### 2.5 Box A / Box B consistency with T1/T2

| Quantity | v2 | Source / my check | OK? |
|---|---|---|---|
| ℓ_max | 3.95 cm (γ*−1)(m/100 GeV)(keV/Λ)² | 2(γ*−1)m/σ with σ = 50.68 GeV/cm: 200/50.68 = 3.946 cm | ✓ |
| N_osc | ≈ 12 (Λ/keV)², m-independent; crossings ≈ 24 (Λ/keV)² | σR/(2β*p_T) (exact for the transverse boost); S check 2: 12.1/11.6/11.9 | ✓ |
| Typical ℓ_max | 5.4 cm (500 GeV, 1 keV), 0.54 mm (10 keV), 60 cm (0.3 keV) | 19.7 cm × (γ*−1) with γ*−1 ≈ 0.27; Λ⁻² scaling exact | ✓ |
| 44-47 % < 1 oscillation at 0.3 keV | | 12 × 0.09 ≈ 1.1 median | ✓ (consistent) |
| SU(2) √σ : T_c | 1 : 0.709; 1 keV T_c ⇒ 1.41 keV √σ | T1; S check 5 (0.7095) | ✓ |
| TH's 1/0.6 "18 % off" (Box A) vs "15 %" (X-4) | | X-4 reconciles both readings | ✓ |
| Scalar ℓ_max ×1.70-1.73, N_osc ×0.81; "1 cm rule underestimates scalars ×1.9" | | T2 l.137 and l.83 (×1.9 is the T2 table value vs the 1 cm rule; ×1.7 is scalar vs fermion) | ✓ (two different ratios; could be said explicitly, C) |
| T_RH ≲ 5-40 GeV; T_max ≲ m_Q/25 | | R1 C-6 applied | ✓ |
| Doublet cτ 7.8 mm (glossary, S-14) vs 7.9 mm (T6) | | S check 7.8; R1 7-8 | ✓ |

---

## 3. Overclaiming and honesty

- **The executive summary is now much closer to the body.** The "Bottom line" (no new exclusion), the four-topic structure and the VERIFIED/UNVERIFIED table are good, and they answer R1 well. Remaining discrepancies:
  - (i) "The fastest route to a literally new limit is a Run-2(+3) recast … 0.2-0.4 TeV over Λ ≈ 0.3 keV to ~MeV". It should acknowledge that E-L already recast the 2016 search, and that the realistic range is ≈ 0.15-0.35 TeV (R2-A1, R2-B3).
  - (ii) "The Li method is a good approximation, ≈ 15 % low" is a single-γ* statement (R2-B1).
  - (iii) "With realistic hit resolution a thickness cut accepts 60-73 % already at 0.3-0.45 keV, so the edge is then set by other features": the comparison is at unequal background rejection (R2-B4).
  - (iv) "Λ ≳ 3 MeV is probably covered by resonance searches (UNVERIFIED)" is correctly labelled.
- **Credits:**
  - Li et al. App.C for the formula's order-of-magnitude status: correctly credited (glossary, S-3, X-2, V2, P1).
  - Athena causal string: correctly described as a known Artru/Lund-type construction, with J. Black et al. credited. FASER [2607.26195] thanks "James Black and Timothy Nelson" for the Geant4 quirks extension, so add T. Nelson (C).
  - **Evans-Luty: under-credited.**
    - Their recast of 1801.00359 for E′ quirks is not acknowledged.
    - Their lifetime-dependent trigger fraction is re-derived by F1 without attribution.
    - Their 300 fb⁻¹ and optimised projections are not compared with S-8.
    - "P3 … partly a refresh of Evans-Luty" understates the overlap. P6 as titled would be refereed against 1811.08903 and fail on novelty.
  - **Farina-Low [1703.00912]: never cited** in v2, although they recast the CMS HSCP and monojet searches for (1,1)₋₁ fermion quirks with N_IC = 2: 650 GeV at Λ = 1 eV, 150 GeV at 100 eV, none at 1 keV [Tab.II]. That is the existing-limit context for the "Λ < 0.3 keV: only stopped-pair and HSCP-like channels" row of Box A, and for the HSCP and monojet recast rows of §4.5 (R2-B2).
- **VERIFIED vs UNVERIFIED labels:**
  - Mostly right.
  - "Li method converged / causal = 0.84-1.05 (30 events, 0.6-2 keV)" is verified *for γ* = 1.28*. That qualifier must be in the cell.
  - "Timing medians … [S]" is honestly marked "closed form on the same kinematic cache".
- **Claims about published work stronger than the evidence:**
  - None remain against Li or Knapen. The S-1 rewrite is careful ("Knapen-Papucci / Sha et al.: unknown").
  - The remaining over-statements concern the *novelty* of the project's own stopped-pair proposal (R2-A1) and the generality of the Li ≈ 15 % number (R2-B1).

---

## 4. Internal consistency

### 4.1 Summary vs body vs sources

| Statement | Where | Issue | Class |
|---|---|---|---|
| labSS/causal "×4-60" vs "1.5-75" | §0.2 item 3, S-1 (iii), X-13, §4.3, §6 vs ranked table, S-1 table row 3, §3 row 15 | Two ranges for the same quantity: R1's seed-11 events give 4-60, F1's T2 events give 1.45-75. Quote "×1.5-75 (median ≈ 9)" once | C |
| "Max OT-hit difference 27-80 µm (0.6 keV)" | S-1 table row 2 | R1 out_a at ×0.001 gives 53-80 µm at 0.6 keV (27-428 µm at 1 keV) | C |
| "Still moving between ×0.01 and ×0.003 in 2 of 6 events" (3 keV) | S-1 table row 5 | From R1 out_b, the thickness changes by > 10 % in 4/6 events (ev0 2.58→1.91, ev1 6.29→7.08, ev2 4.85→3.73, ev5 6.62→5.72) | C |
| "Out-of-plane differences stay ≤ 10.5 µm" | S-1 table row 6 | True at γ* = 1.28 and 2 keV. At γ* = 2-3 (1 keV) the converged Li-causal out-of-plane differences are 12-124 µm (R2 test 1) | part of R2-B1 |
| "Run-2+3 recast 0.2-0.4 TeV" | §0.2, §1 table, §4.5, §4.6, P6 | 0.4 needs τ ≫ 1 µs and B = 0; v2's own τ gives 0.15-0.34 | R2-B3 |
| "Evans-Luty give 0.1-100 µs" | S-8 | For Λ ≳ 300 eV, ≈ 0.1-5 µs, peak ≈ 0.5 µs | R2-C4 |
| Run-2+3 recast "across Λ ≈ 0.3 keV to ~MeV" | §0.2, S-8, P6 | f_stop was computed at 0.3-3 keV only (E-L checked flat to 10 keV). Above ~0.1 MeV, S-16's own ε-dependent in-flight annihilation (3 cm-10 km) can pre-empt stopping. Say "to ≳ 10 keV (computed), plausibly higher" | C |
| "×1.9" vs "×1.7" for scalars | Box B | Two different ratios (vs the 1 cm rule; vs the fermion). One clause each | C |

### 4.2 Withdrawn numbers (grep for ×0.04-60, 0.2-35 mm, 0.2-21 mm, 140-570 µm, 0.65 TeV)

- ×0.04-60, 0.2-35 mm and 140-570 µm appear only at l.38 and l.205 (the withdrawal notes), l.223/805/891 (attributed to labSS/cmSS, which is correct) and l.614 (as "v1 overstated it"). **No stale use.**
- 0.2-21 mm appears only as a labSS property (l.205, l.805). OK.
- 0.65 TeV appears at:
  - l.42 and l.431 (as the superseded number);
  - l.186 ("≲ 0.65 TeV (B = 0, long delay)", which is right as a bound);
  - l.420 and §3 row 21 (as the v1 value).

  **No stale use.**
- T2 and T3 still contain the withdrawn numbers in their bodies, each marked "[superseded, see erratum]". That is acceptable.

### 4.3 Other

- v2 §3.1 counts "independent" checks as rows 1, 3-5, 7, 8, 13 and 15-19 (12). Row 3 is "indep. formula; same cache", and row 8 inverts the formula, which tests the strategy's arithmetic, not physics. The counting is generous but labelled. Fine.

---

## 5. Findings (classified)

### A (wrong or misleading)

**R2-A1. The stopped-pair recast is presented as the first LHC limit and as not yet performed. Evans-Luty already recast CMS 1801.00359 for E′ quirks.**

*Where:*
- S-8 ("That would still be the first LHC limit on singlet quirks across Λ ≈ 0.3 keV to ~MeV");
- §4.5 heading ("none has been performed") and the first row ("the first LHC limit on singlet quirks across Λ");
- §5 P6 title and "the only route to a literally new exclusion";
- §0.2 Bottom line (implicitly);
- §8 step 2;
- §4.6 S-8 row.

*Evidence:*
- 1811.08903, abstract: "We recast an existing CMS search for out-of-time decays".
- Its ref. [34] = 1801.00359 (38.6 fb⁻¹).
- Its Fig.5 left shows E′-like (1,1) quirks with SU(2)_IC: the current limit, a naive 300 fb⁻¹ projection, and an optimised |η| < 3, zero-background 300 fb⁻¹ projection reaching ≈ 0.7-0.75 TeV up to Λ ~ 1 MeV.
- Its Figs. 3-4 give the lifetime-dependent empty-BX acceptance from the real 2016 fill schemes. That is the correction F1 re-derived without credit: ≈ 8-10 % trigger fraction for 300-500 GeV E′ at Λ ≳ 300 eV, against F1's 0.027-0.086 for τ = 0.1-0.5 µs.
- FASER [2607.26195 Fig.5] lists "Reinterpreted CMS OoT" and "Reinterpreted CMS HSCP" among the previously excluded regions. FASER itself excludes up to 0.18 TeV for 0.3-100 keV; D0 excludes ≈ 0.11 TeV for 10 keV-1 MeV.
- T6 l.71 states "Evans-Luty recast CMS 1801.00359".

*Fix:*
- Credit E-L for the recast, the trigger-fraction method and the projections.
- Restate the proposal as "an update of the Evans-Luty recast with full Run-2(+3) data and the causal-string f_stop". At Λ ≳ 0.3 keV it would raise the central-detector limit from ≈ none to ≈ 0.15-0.35 TeV. That is comparable to or above FASER (0.11-0.18 TeV) and D0 (≈ 0.11 TeV) only in the low-background case.
- Retitle P6, and lower its novelty to "update/extension". It is still a good CMS-internal task.
- Compare S-8's HL-LHC numbers with E-L's projections.

### B (weakens a result; must fix)

**R2-B1. "Li ≈ 15 % low when converged" is a single-kinematic-point result (γ* = 1.28).** (§2.1, test 1.)

*Where:* §0.2 item 3; S-1 table and (ii); exploitation (e) "a converged CM-simultaneous code should give ≈ 0.85"; VERIFIED column; X-13; §4.1 rows §4.2 b1, V3, V5, §12 (i); §4.3; P1.

*Evidence:* converged Li/causal medians are 0.97 / 0.85 / 0.92 / 0.69 / 0.65 at γ* = 1.05 / 1.28 / 1.6 / 2 / 3 (5 events each, 1 keV). At γ* ≥ 2, single events span 0.53-1.36 and out-of-plane hit differences reach 30-120 µm.

*Fix:*
- Quote the deviation as γ*-dependent: "≈ 3 % at γ* ≈ 1.05, ≈ 15 % at the median γ* ≈ 1.3, 30-50 % (either sign) at γ* ≳ 2".
- Add "(m = 500 GeV, γ* = 1.28, p_T = 300 GeV)" to every place that quotes 0.84-1.05.
- Replace the fixed 0.85 validation target by an event-by-event comparison with `T3_causal.py` over the triggered γ* spectrum.
- The conclusion "superseded, not a systematic" stands.

**R2-B2. Existing constraints on the E singlet are missing from the consolidated Λ answer (Box A) and from the recast table (§4.5).**

The user asked for improvements in constraints, so the baseline must be stated:
- Farina-Low [1703.00912 Tab.II]: CMS HSCP and monojet recast for fermion (1,1)₋₁ quirks, N_IC = 2: 650 GeV at Λ = 1 eV, 150 GeV at 100 eV, none at 1 keV. This paper is never cited in v2.
- Evans-Luty out-of-time recast [1811.08903 Fig.5].
- D0 [1008.3547]: ≈ 107 GeV (N = 2), 10 keV-1 MeV.
- FASER [2607.26195]: up to 0.18 TeV, 0.3-100 keV.
- Box A's row "Λ < 0.3 keV … only the stopped-pair and HSCP-like channels" should say that HSCP and monojet recasts already exclude up to 0.15-0.65 TeV at Λ ≤ 0.1 keV.
- The §4.5 HSCP and monojet rows should note Farina-Low's 12.9 fb⁻¹ recasts as the starting point.

**R2-B3. The Run-2+3 recast headline "0.2-0.4 TeV" uses the assumptions B-6 rejected.**

- The upper end 0.38-0.42 is the τ ≫ 1 µs, B = 0 column.
- With v2's own delay (τ = 0.1-0.5 µs) the range is 0.22-0.34 TeV (B = 0), 0.17-0.26 TeV (B = 10) and ≈ 0.15-0.20 TeV (B ≈ 80).
- The low end does not improve on FASER (0.11-0.18 TeV in 0.3-100 keV) and matches E-L's naive 300 fb⁻¹ projection.
- *Fix:* quote ≈ 0.15-0.35 TeV in §0.2, the §1 table, §4.5, §4.6 and P6, with "beats FASER/D0 only if the background is reduced to O(10) with an energy threshold".

**R2-B4. The resolution-aware coplanarity conclusion "the 50 % edge moves below 0.3 keV" compares cuts with different background rejection.** (§2.2.)

*Where:* §0.2 Bottom line and item 4; Box A; ranked table S-3 ("realistic resolution: below 0.3 keV"); S-2 "Reading the table" (i)-(ii); S-3 Revised window; §10.1 B-2 and §10.3 ("we find it moves *down*").

*Problem:*
- t_est < 100 µm and truth Δs < 100 µm are different observables.
- An IT-dominated test (≈ 12 hits at r ≤ 14.6 cm) passes any pair of prompt tracks with p_T ≳ 100 GeV: they are coplanar with the PV to within the helix sagitta, ≈ 0.32 mm × (10 GeV/p_T) at 14.6 cm.
- Likewise "a Δs < 30 µm cut no longer costs 30-45 %" conflates t_est with Δs.

*Fix:*
- State that the lower edge is **undefined** until the cut is set at fixed background efficiency (e.g. on prompt-track pairs and PU fakes).
- The background discrimination of low-Λ signal must come from the OT rφ non-helicity and the hit multiplicity, not from IT coplanarity.
- Keep the per-hit resolutions and the "truth-level cut values do not transfer" message, which are correct and valuable.

### C (polish)

- **R2-C1. Number mismatches.**
  - S-1 row 2: 0.6 keV OT-hit difference at ×0.001 is 53-80 µm, not 27-80 µm.
  - S-1 row 5: 4 of 6 (not 2 of 6) 3 keV events move by > 10 % between ×0.01 and ×0.003.
  - labSS/causal is quoted as ×4-60 in six places and ×1.5-75 in three; unify (×1.5-75, median ≈ 9).
- **R2-C2.** "Convergence not reached at 3-5 keV" (§0.2, S-1, §7.3, §10.3): at 3 keV it is reached at ×10⁻³ (R2 test 2); keep "not tested at 5 keV". The Λ⁻² ESTIMATE for the required step fraction is still plausible.
- **R2-C3.** Stopped-pair background: for τ < 1 orbit, 1801.00359 searches a 1.3τ window after each collision [Sec.8]. That scales the cosmic and noise background to ≈ 15-45 % of the full-livetime value at τ = 0.1-0.5 µs. The "B ≈ 230 at τ = 0.5 µs" column is ≈ ×2 pessimistic. The bracket still holds.
- **R2-C4.** "Evans-Luty give 0.1-100 µs" (S-8): for Λ ≳ 300 eV their τ_stop for 500 GeV E′ peaks at ≈ 0.5 µs (≈ 0.1-5 µs) [Fig.4 left]. The 0.1-100 µs span is the low-Λ, terminal-velocity regime. Quoting it correctly supports F1's τ choice.
- **R2-C5.** "The residual 0.1-0.5 mm is an upper bound on the converged Li-causal difference" (S-1 row 6): the evidence shows it is *consistent with pure integration error*. "Upper bound" needs monotonic convergence, which is not shown.
- **R2-C6.** S-4 caveats: add the ≲ 5 GeV calorimeter deposit of the pair itself [T4 l.277 via 1911.02223 Sec.V]. It is a one-sided ≲ 2 % MET bias, the same size as the quoted 1-3 % scale floor; correctable.
- **R2-C7.** "Recast covers Λ ≈ 0.3 keV to ~MeV": f_stop was computed at 0.3-3 keV (E-L checked flat to 10 keV). Above ~0.1 MeV, S-16's own ε-dependent in-flight annihilation can pre-empt stopping. Say "computed to 3 keV, plausibly to ≳ 100 keV".
- **R2-C8.** Credits and wording:
  - add T. Nelson next to J. Black for the Athena/Geant4 quirks extension [2607.26195 acknowledgements];
  - Box B: say that ×1.9 (scalar vs the "1 cm" rule) and ×1.7 (scalar vs fermion) are different ratios.
- **R2-C9.** Missed handles for the sub-µs delay that drove the S-8 downgrade, from E-L Sec.5: HGCAL timing could raise the triggerable fraction of forward deposits to O(90 %); filling schemes with frequent short gaps raise the acceptance at τ ≲ 0.5 µs. One line each in S-8 or P3.

### What I confirm as correct in v2 (for the record)

- The S-1 withdrawal and the T2/T3 errata.
- R1's Li kernel matches Eq.III.6-III.10.
- labSS/Li = 1.6-73 (0/12 within ±50 %).
- The 2 keV mm hit differences are Euler phase drift (the out-of-plane component is ≤ 10.5 µm at γ* = 1.28).
- Per-hit σ_n of 17 µm / 0.25 mm / 8 mm from the stated pitches.
- The S-8 table arithmetic and the BR_vis, ε_reco and veto inputs.
- The 1801.00359 background (11.4 events in 586 h) and its lifetime range.
- The measurement 1-3 % / 0.5-1.5 % logic.
- The S-5 real-background reasoning.
- Box A/B numbers: ℓ_max 3.95 cm, N_osc ≈ 12 (Λ/keV)², T_c/√σ = 0.709, scalar ×1.7/×0.81.
- The S-18 PU-vertex arithmetic.
- No stale v1 numbers remain.
