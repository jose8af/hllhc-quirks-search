# Constructive review R1 of THEORY_GAPS_SYNTHESIS.md (and T1-T6)

Reviewer: R1-constructive. Date: 2026-10-08. Focus: usefulness, completeness, missed opportunities. Correctness is left to the critical reviewer.
Classes: **A** = would mislead the user's decisions; **B** = significant omission or weakness; **C** = polish.
Tally: **A = 3, B = 11, C = 12** (B1-B11 and C-items as listed in Sec. 5).

## Overall verdict
The synthesis is a strong, honest, well-sourced document. Its weakest point is the interface to the user's question: the user asked for improvements in *constraints* and named four topics. The document is organised by gap (S-1..S-20), not by those topics, and it contains almost no new constraint. The one statement that can be called a result on reach is the window edge Λ_low = 0.45-0.7 keV. The rest is "your model was wrong" and "you can measure after discovery". That is valuable, but it must be said plainly and mapped to the four topics.

---
## 1. Coverage of the request

| Topic | Where it is | Clear "improved / new constraint / exploitable"? | Verdict |
|---|---|---|---|
| Λ | S-11 (convention), S-14 (GUT ladder), S-15 (cosmology), S-16 (MeV), S-4 (measurement), S-3 (Λ_low) | Scattered over 6 entries, 3 of them in the "complementary" group. No single statement of what the allowed/targeted Λ range is, now. | **B1** |
| Oscillation length | S-11 (closed forms ℓ_max, N_osc), S-13 (ISR) | Buried in a "documentation" entry ranked 11. The scalar result (ℓ_max x1.7, N_osc x0.81 [T2 §3-ish, line 127]) and the "1 cm (m/100)" error (x0.4-2.7 per event) are not in the synthesis table at all, and the user explicitly named this topic. | **B2** |
| Propagation dynamics | S-1, S-2, S-3, S-9, S-12 | Good. | OK |
| Trajectory model | S-1, S-4, S-5, S-7 | Good, but the "model" conclusion (causal string only) is more prominent than the reconstruction conclusion (9-parameter fit) for someone choosing next steps. | OK |

**B1 (Λ).** Add a 6-line box at the top of Sec. 1, "What is known about Λ after this track":
- convention fix (1/0.709, not 1/0.6);
- tracker-sensitive window now 0.45/0.7 keV (50 % edge) to about 20 keV (merging), with the 1 TeV plateau from 2 keV;
- outside it: Λ < 0.3 keV and Λ > 30 keV are covered only by the stopped-pair and HSCP-like channels (S-8, S-10); Λ ≳ 3 MeV by resonance searches (S-16);
- GUT-motivated Λ (0.8-15 keV) belongs to doublets which are tracker-invisible (S-14);
- a discovery fixes Λ to 0.5 % (MET route) and implies T_RH ≲ 5-35 GeV.
This is the user's "Λ" answer.

**B2 (oscillation length).** Add scalar Ẽ numbers to S-11 or a new line in the exec summary: ℓ_max x1.7, N_osc x0.8 for scalars; the "1 cm (m/100 GeV)(keV/Λ)²" rule used in FASER/cosmology papers is wrong per event. Also quote the practical number (N_osc ≈ 12 (Λ/keV)², the number of crossings in the tracker) in the exec summary, since it is what decides hit multiplicity and the aliasing regime.

**A1 (the headline claim vs the evidence on sensitivity).** Exec item 1 says "Every published central-detector trajectory model is wrong at the order that matters". S-1 itself concedes that "in the core window it is probably small, because the causal pass fractions are 0.93-1.00", and S-2/S-3 conclude the window edge moves by only about 10-20 %. A reader (and a CMS convener) will take the headline to mean that published reach/efficiencies are wrong. The document never states the effect on the experimental sensitivity (events or mass reach). What is shown is that (i) the *thickness and OT-hit predictions* are wrong by large factors, (ii) the plane-finder window and the efficiency of a Δs < 100 µm cut are barely changed. These two are different and the exec summary conflates them. Suggested text: "The straight-string model mis-predicts thickness and OT-hit positions by up to x60 and mm. For the existing coplanar cut (Δs < 100 µm) the signal efficiency changes little (pass 0.93-1.00; window edge 0.45-0.7 vs 0.54-0.81 keV). The model error matters for (a) any analysis that uses hit positions beyond the plane finder (predictive χ², GNN truth, fits), (b) the thin-plane cuts (< 30 µm), (c) the interpretation of any quoted Δs distribution."

**A2 (no new constraint is stated; the reader may assume otherwise).** The request was "improvements in constraints". The synthesis never says "no new exclusion was derived". The nearest items are S-8 reach (0.65-1.0 TeV, a projection, not a limit), S-16 ("probably excluded", UNVERIFIED) and S-17 (reach 1.3 TeV, unverified applicability). Add an explicit statement at the top: "This track produced no new exclusion. It produced (i) corrections to the signal model and the window; (ii) two new channels with reach projections; (iii) two UNVERIFIED claims of existing exclusion (Λ > 3 MeV, doublet recast)". Otherwise "Λ ≳ 3 MeV is probably already excluded to 0.8-1 TeV (UNVERIFIED)" in the exec summary reads as a result.

---
## 2. Missed gaps and opportunities (judged)

| Idea | Covered? | Judgement | Reason / suggestion |
|---|---|---|---|
| Quirk pair vs PU vertices / beam-spot length | T4 uses beam spot x0,y0; z0 is a fit parameter; no PU-vertex study (T5 G-T5-3 flags PU) | **Worth adding (B3)** | The plane has a free z0 and the pair is produced at the hard-scatter vertex, but with 200 PU vertices over σ_z ≈ 3-5 cm the *vertex assignment* of a non-helical object is not defined. Which vertex does the plane point to? MTD time (BTL delay 3.5-19 ns!) is the only handle, and it is shifted by the slow pair itself. A 1-page theory note: z0 resolution from the plane-fit alone (the 9-parameter fit gives it) and the PU-vertex ambiguity with the quirk time delays. Cheap (days) with T4 code. |
| L1 track trigger and HLT displaced/disappearing paths | S-18 (L1 stubs 23-47 %); T4 line 335 mentions HLT BTL-delayed segment | **Partly covered; add an HLT line (B4)** | The synthesis stops at "L1 invisible". The important consequence is that the trigger is MET (p_T(QQ̄) > 200 GeV), which is what S-13 and S-5 depend on. Missing: whether existing HLT paths (displaced jets, disappearing track, HSCP, delayed-jet) could see a quirk at all, and a statement of the *Run-3 MET trigger threshold* effect on the p_T spectrum. Add a short table: path / why it fails or works / source. Without CMS-internal info this is UNVERIFIED but still worth listing as an open question, since the user is CMS. |
| Scalar vs fermion trajectories | T2 (ℓ_max x1.7, N_osc x0.8, P-wave, decay angle), T6 (rates x11-18) | **Worth adding (B2)** | Present in T2/T6 but absent from the synthesis. The Ẽ alternate needs different signal windows (more oscillation length, fewer crossings); say it. |
| Run-3 vs Phase-2 | Nowhere. Only OQ-level mention in T6 (PPS) | **Worth adding (B5)** | The user said "maybe Run-3 first". Most numbers are B-field and material dependent: B is the same (3.8 T), so the thickness physics (S-3) carries over; but the material is different (Run-3 tracker is the old 4-layer pixel + strip tracker, ~ 0.4-1.0 X0 total vs Phase-2 reconstruction at 19 % X0 at η=0 [UNVERIFIED]); no MTD (so S-6 timing and the BTL double-hit idea do not exist in Run 3; only ECAL timing and HCAL/TOF-like tools); no L1 tracks; PU ~ 50-60 not 200 (so the PU-200 random-plane background of S-5 is smaller); the Run-3 strip tracker has 25 ns bunch gaps and ECAL timing is the only handle. Provide one table "which S-items hold in Run 3". Also S-8 (stopped quirks) is **already feasible in Run-3 data** with CMS 1801.00359 style triggers, with 138 fb-1 at 13 TeV: reach about 0.3-0.4 TeV at f_stop = 1 % (scale from the Phase-2 numbers); this is the quickest CMS-internal result and the synthesis does not give it. |
| Both-colour-and-EW-charged quirks as contrast | T5 mentions coloured; none of T1-T6 quantifies | **Worth a short paragraph (C)** | Coloured quirks (3,1)_{2/3} have rate x10-100 and the existing Knapen/Li reach is quoted for them (2.1 TeV fermion). One line: "coloured quirks hadronise/spin down differently and have much larger rates, but the model-error conclusions S-1..S-3 apply equally (string physics is identical); coloured quirks are the target of ATLAS". It also improves the argument for the CMS singlet choice. |
| ML-friendly observables | T4 §5 touches (GNN training truth, S-1 hand-off to W8) | **Worth adding (B6)** | The synthesis gives GNN *training-sample* corrections but not *features*. Natural quirk-specific features from the theory: per-hit residual of the causal-model prediction (S-7 χ²), MET-φ alignment (S-5), ℓ₀ estimate, hit time vs R/c delay, plane-normal vs MET. These are physics-motivated and reduce dependence on the training truth. Suggest 3 lines in S-7 or §4.5. |
| Inverse problem / simulation-based inference | T4 does CRB only; no mention of SBI | **Worth adding (B7)** | The CRB is local and assumes known assignment, and the objective is multi-modal (aliasing minima, S-7). The natural next tool is SBI (neural posterior/ratio estimation) trained on the causal-propagator events, which also handles MS stochasticity and degeneracy (ℓ₀ ridge in (m_Q, Λ)). Since T3_causal.py is 10³x faster, the training set is cheap. Mention under S-4 as the "real fit" for P2; it also provides the posterior of Λ given a MET systematic. |
| Recasting existing CMS searches | S-8 (1801.00359), S-10 (2410.09164), S-14 (monojet) mention recasts but no opened limits | **Worth adding as a ranked recast table (B8)** | Four recasts are scattered: stopped particles, HSCP (2410.09164), disappearing track/monojet (doublets), multi-charge. For a CMS member these are the *fastest constraints* and the only literally-new-exclusion route. Make one table: search / quirk subset it covers / signal efficiency reason it may fail (e.g. HSCP track-quality needs a helix; quirks in the 0.5-20 keV window are non-helical) / needed inputs / effort. Call out explicitly that none has been done. |
| Flux-tube lattice theory: string width, Lüscher term | T5 §7 (Lüscher killed: 1e-8 at 1 µm); T2 (roughening 5 Å killed) | Covered, killed. | Not worth adding. |
| Baryonic junctions for N_IC = 3, k-strings | T5 S9 / G-T5-8 mention k-string tension ratios; synthesis drops them | **Mention in one line (C)** | For N_IC = 3 a QQ̄ pair is still a single fundamental string; junctions matter only for multi-quirk states (not produced). k-strings matter if quirks are in a non-fundamental IC representation (Casimir scaling vs sine law). They change the *definition* of Λ, i.e. the S-11 convention table. Add a row: "non-fundamental rep or N_IC > 3: σ_k/σ_1 = sin(kπ/N)/sin(π/N) or k(N-k)/(N-1); Λ must be defined per rep". Not worth an investigation. |
| N_IC dependence beyond SU(2) | S-11 gives SU(3) T_c/√σ; S-14 SU(3) ladder; rates ∝ N_IC | **Worth a line (C)** | Is the benchmark choice N_IC = 2 vs 3 changing yield (x1.5), glueball mass (3.41 vs 3.78 √σ), cosmology (ΔN_eff 0.57)? Put one row of N_IC = 3 numbers in the exec/Λ box. |
| Hit noise, misalignment, radiation damage in ML tracking | T5 lists as open (2509.08878) | **C** | Mention as experimental-track item; the causal prediction of 15-55 µm per OT hit (S-7) must be compared with alignment (10-30 µm?) which is the same size. This is a **realism check missing in S-7**: the ×20-100 per-layer rejection assumes a perfect geometry. Add "alignment residuals comparable to the prediction error would halve it". (B9, see §3.) |
| 0 T / low-B data | T5 lists [1703.00912] | C | Cosmics/0 T runs: the thickness is then pure MS and the model is simplest. A free validation sample for the MS floor (S-2). Mention. |
| Quirk-gluon/ISR-jet kinematics beyond DY (VBF, γγ) | T6 | covered | OK |

---
## 3. Actionability

**Ranking.** Mostly sensible. Observations:
- Rank 3 (S-6 timing) has "done (documentation)" as effort and is placed above S-5/S-3. The criterion "impact x confidence / effort" favours it, but its impact is a correction to a strategy number, not an analysis gain. Fine, but state that ranks 1, 3, 11 are corrections (errata of the existing plan) while ranks 4, 6, 7, 8 are new capabilities. A user choosing the next action wants that split. **(C)**
- S-9 (MaxSteps killer, hours) is ranked 9 but is the cheapest item that can silently invalidate the high-Λ simulation. For the user building a Geant4 workflow it should be in a "do this first" list. **(C)**
- S-14/S-16/S-17 verdicts depend on UNVERIFIED external limits; the table's confidence column is honest, but the exec summary item 5 mixes verified (f_stop) and unverified claims in one bullet list. Separate by verification status (**B**, merged into A2).
- **B9 (S-7 realism).** The "x20-100 per OT layer" rejection is an idealised CRB with known assignment, no PU, perfect alignment. This number is quoted in the ranked table and the exec summary context as an exploit. State in the table, not only in the caveat, "upper bound; expect order-of-magnitude less with PU 200 and 10-30 µm alignment" or rename to "predictive power". As written, it can mislead the user into promising a background rejection factor in a proposal. Together with A1 and A2 this is why I count A3 below.
- **A3 (S-5 MET-strip alignment).** "x13-34 random-plane rejection at 95 %" is presented as EXPLOIT with high confidence. It is a pure geometry statement given the assumed σ⊥ of 15-35 GeV and ignores that the real background is not a random plane: the dominant background (Z(νν)+jets with PU, per 1911.02223) has *real* MET aligned with a jet; the Δφ(jet, MET) cleaning caveat is there, but the gain after the cleaning is not quantified, and the cleaning itself may be correlated with the cut. A user could put x13-34 into a background-estimate. Reword: "x13-34 relative to *random* planes; the gain on the Z(νν)+jets + PU background after Δφ(jet,MET) cleaning is not yet known (likely smaller)".

**Efforts and dependencies.** Realistic overall; three issues.
- Step 1 (independent solver, 1-2 weeks) gates P1, S-3 and the B ln B claim. The document says so, which is good. But step 2 (hand T3_causal.py to Phase 2) and the S-9 fix should *not* wait for step 1; say that explicitly (they are listed as step 2, but the dependency of P1 only). **(C)**
- Effort for P1 is stated three ways: "2-4 weeks" (exec), "3-5 weeks" (Sec. 5), "3-4 weeks" (Sec. 8). Unify. **(C)**
- Step 3 needs CMS-internal material (the user). Say which steps need the user's CMS access vs not, in a column. **(C)**

**Implications list (§4).** This is the strongest part: file/section pointers, current text and replacement text, with numbers. Two gaps: (i) no priority/severity marker per row (which edits change a decision vs wording); (ii) no pointer to *which figure/table of the investigators the user should read first*. Suggest adding a "Severity" column (must / should / wording) - **C**.

**Paper proposals.**
- P1 is correctly scoped as needing an independent solver and the Athena run, and the credit/contact remark is good. The scoping risk is **novelty**: the ATLAS Athena code already implements the causal string (the synthesis says so), and ATLAS/FASER results already use it. So the paper's novelty is (i) showing the straight-string prescriptions are non-covariant and (ii) the B ln B / MS-floor numbers. State plainly: "the new physics content is the thickness scaling and the MS floor, not the causal string itself" and name the venue risk (could read as a code-validation note). **(B10)** Also confirm that the claim "every published model uses the straight string" is true for ATLAS-internal analyses, which are not public; the paper can only say "every published/public". A reviewer will test this.
- P2 (measurement) is realistic but the novelty claim "open since 2017" is fine; its value depends on a real fit with PU, which is 3-6 weeks only if P1's code is reused. OK.
- P3 stopped quirks: correctly flagged as moderate novelty (partly refresh of Evans-Luty) and better as a CMS-internal recast. Agree. P4 and P5: agree, low priority.
- Missing paper-level idea: a **short pheno note on "recasting the CMS stopped-particle and HSCP searches for quirks"** (B8). It is the most likely route to a new constraint for the least effort and has no solver dependency.

---
## 4. Clarity

- **Exec summary readability (3 min).** It is dense: 5 numbered findings with sub-bullets, about 30 numbers, internal IDs (S-x, T-x, G-T…), and no definition of terms. A CMS physicist will not know "causal vs straight string" or "plane thickness (Δs)" at first reading. **B11.** Add, before item 1, a 5-line glossary: *straight string* = string drawn instantaneously between the two quirks in some frame; *causal string* = the Nambu-Goto string built from retarded null data (ATLAS Athena algorithm); *plane thickness Δs* = rms/median out-of-plane residual of the hits to a fitted plane after refit; *b* = odd-crossing miss distance (a different quantity, S-3/T-2); *ℓ₀ = m_Q/Λ²*; *Λ = √σ*.
- **Thickness definitions.** Three different "thicknesses" circulate: the formula d [1911.02223], the plane-fit Δs (T3), the in-plane B displacement x_B (T4), and the odd-crossing miss distance b. They are reconciled only in T-1/T-2 (Sec. 2), after being used in S-3 (before). Move a 4-line definition table to the start of Sec. 1. **B (merged in B11).**
- **Λ convention** is stated at the top (good) and again in S-11. But the exec summary says "the Λ convention is 1/0.709, not 1/0.6" without saying that this is about *converting the cosmology paper's T_c-based Λ to √σ*. A new reader will not parse it. **C.**
- **Contradictions summary vs body.**
  - Exec: "Paper-ready after one more step ... about 2-4 weeks" vs Sec. 5 "3-5 weeks" and "needs three things (i)-(v)". The "one more step" is understated. **C.**
  - Exec item 1 vs S-1/S-3 (see A1).
  - Exec: "Doublets are invisible to the tracker: a monojet + soft-pion recast" and "Λ ≳ 3 MeV probably already excluded": both are in the same item as measured results, but the body labels them UNVERIFIED. **A2.**
  - Exec: "35/35 checks pass" – Sec. 3 counts 30 assertions plus 5 rows; the checks are mostly reproducibility (same code, same event cache). Say "35/35 reproducibility or closed-form checks, 9 of them independent". **C.**
  - Exec: reach for stopped pairs "0.65 TeV (EB+HB)" - the full-calorimeter 0.9-1.0 TeV needs endcap empty-BX triggers (UNVERIFIED). The exec already separates them; fine.
- The "Status: DRAFT v1, for critical review" header is fine; remove at release. The Section numbering (T-n tensions) uses the same prefix "T" as investigators T1-T6: **C** (rename "X-n" or "R-n").

---
## 5. Classified list

**A (3)**
- A1: Exec headline "every model is wrong at the order that matters" without stating the (small) effect on the existing window/efficiency; no statement of impact on reach.
- A2: No statement that no new exclusion was derived; UNVERIFIED exclusions (Λ > 3 MeV, doublets) sit in the exec summary next to verified results.
- A3: S-5 x13-34 is quoted vs random planes; the real dominant background (Z(νν)+jets with PU, real MET) is not random; the number may be used in a proposal as a background reduction.

**B (11)**
- B1: no consolidated Λ answer. B2: oscillation-length topic buried; scalar differences omitted. B3: PU-vertex / beam-spot ambiguity not studied. B4: HLT paths not assessed. B5: no Run-3 vs Phase-2 table; Run-3 stopped-particle recast not given. B6: no ML-feature view. B7: no SBI / inverse-problem mention. B8: no consolidated recast table. B9: S-7 rejection factor idealised (no alignment, PU). B10: P1 novelty framing vs ATLAS. B11: undefined terms before use.

**C (12)**: ranking-type labelling (corrections vs capabilities); S-9 priority; P1 effort stated three ways; which steps need CMS access; severity column in §4; coloured-quirk contrast line; k-string/N_IC=3 row in S-11; N_IC=3 numbers; "T-n" prefix clash; "35/35" wording; 0 T validation sample; Λ-convention wording in exec.

---
## 6. Five most valuable improvements (prioritised)
1. **Rewrite the exec summary around the user's four topics and state the net result on constraints**: one line each for Λ, oscillation length, propagation, trajectory model; one line "no new exclusion yet; here are the fastest routes to one" (A1, A2, B1, B2). Add the glossary (B11).
2. **Add a recast table** (stopped particles 1801.00359, HSCP 2410.09164, disappearing-track/monojet for doublets, multi-charge) with what is needed and why each may or may not work for non-helical quirks (B8). Include the Run-3 feasibility of the stopped-particle recast (B5).
3. **Add a "Run-3 vs Phase-2" table** (B-field, material, MTD, L1 track trigger, PU) saying which S-items hold in Run 3, because the user plans Run-3 first (B5).
4. **Downgrade or re-word the quantitative "exploit" claims that are idealised**: S-5 (x13-34 vs real background), S-7 (x20-100 per layer without alignment/PU) (A3, B9); add a verified / unverified split in the exec summary.
5. **Add the missing realism studies as cheap next steps**: PU-vertex and beam-spot ambiguity of a non-helical plane using the T4 fit (B3), SBI as the "real fit" for P2 plus quirk-specific ML features (B6, B7), HLT path assessment (B4). Reframe P1's novelty as "thickness scaling and MS floor, with the straight-string failure demonstrated", not "the causal string" (B10).
