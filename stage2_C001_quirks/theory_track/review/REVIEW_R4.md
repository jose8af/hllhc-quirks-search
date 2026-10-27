# REVIEW_R4: fresh round-4 verification of THEORY_GAPS_SYNTHESIS v4

Reviewer: R4 (verification only). Date: 2026-10-08. Under review: `outputs/THEORY_GAPS_SYNTHESIS.md` (v4, 1067 lines).
Opened: REVIEW_R3.md, BRIEF.md, v4 in full where relevant (header, §0, Box A, S-2/3/4/5/7/8/10/15, §1 table, §3 rows 22-23, §4.5, §5, §10.2-10.3), `figures/R3_lit_numbers_out.txt`.
Primary texts checked in `research/cache/pdf/`: 2002.07503 (§V, §V.A), 1708.02243 (§IV, Eq.8-9), 2410.00269 (§V), 2108.06748 (§4.3, §5, Eq.4.18), 2512.20696 (abstract, l.785), 2607.26195 (abstract, App.A; **Fig.5 re-rendered at 170 dpi**), 1008.3547, 1811.08903 §2, 0805.4642 §3.2.
Classes: A wrong/misleading; B weakens a result or missing credit; C polish.

## Verdict: PASS (0 A, 0 B, 7 C)

All six R3 B items and all nine R3 C items are fixed in v4. The credit statements match the cited texts. No withdrawn v1-v3 statement is in live use. The executive summary agrees with the body on every item I checked. The v4 edits add no A or B issue. The C items are wording and housekeeping.

## 1. R3 items

| Item | v4 location | Fixed? | Comment |
|---|---|---|---|
| **R3-B1** FASER Λ-dependent | Box A, §0.2 Bottom line, "What changed in v4", S-8 (l.479), §4.5 row 1, P6, §10.3 | **Yes** | Contour quoted per Λ (57/72/105/135/150/165/179/175/155/65 GeV). My re-render of Fig.5 gives ≈ 57 (0.3 keV), 70, ≈ 110 (1 keV), ≈ 150 (3 keV), ≈ 180 (10 keV), ≈ 65-70 (100 keV): consistent within the stated ±5-10 GeV. D0 107 GeV (10 keV-1 MeV) is included in "best existing" (so the 100 keV comparison is against 107, not 65, as in R3's table). The restated conclusion (beats at Λ ≲ 2 keV and near 100 keV even with B ≈ 80; 3-50 keV only with B ≲ O(10)) matches `R3_lit_numbers_out.txt` §2. "FASER ≤ 0.18 TeV; nothing above ≈ 0.18 TeV" is right. Residual: C3, C4 |
| **R3-B2** Li §V/Fig.4 credit | S-3 (credit bullet + narrowed "new"), S-17, P1 novelty sentence, "What changed in v4" | **Yes** | Text check: §V "thickness dependence on m and p_T is mild" (l.657); Fig.4 left shows m = 100/500 GeV curves; §V.A "linearly proportional to each of the quirk charges" (l.669). The new list is narrowed to the converged exponent, B ln(1/B) at crossings, MS floor and corrected window. Li's "linear in q" is correctly placed beside the B-nonlinearity (≈ 10 %). Residual: C2 (executive summary item 3 still lists m_Q independence without credit) |
| **R3-B3** Knapen Δφ | S-5 first bullet, §1 table row 6 (C + N), §10.3 | **Yes** | Quote verified: "can easily be removed through either a ∆φ requirement between E̸_T and n₃" [1708.02243 §IV]. KLN §4.1 added. Novelty = quantification, correctly scoped |
| **R3-B4** Sha χ² / Knapen fit | S-7 first bullet, §1 table row 10, §10.3 | **Yes** | Verified against 2410.00269 §V: quirk vs helix fits, ln(χ²q/χ²h) < −1 and Δϕ > 2.8 vetoes, 94 % at m = 500 GeV, Λ = 500 eV, removes all SM tracks in sample. "Their straight-string propagator" is acceptable (§III propagator). Knapen "fitting a quirk trajectory to the hits" verified |
| **R3-B5** MS statement | S-2 Statement, P1 | **Yes** | Now "no published phenomenology study includes MS, none quantifies it"; Athena G4 extension uses "standard Geant4 electromagnetic processes" [2607.26195 App.A, verified at l.433]; "probably includes MS (UNVERIFIED which processes)". Knapen detector-level Δs credited |
| **R3-B6** 2512.20696 | S-15 credit, §0.2 item 1, Box A cosmology row, §1 row 15 (D + C) | **Yes** | Abstract quote verified ("T_RH ≲ O(100) GeV … far-reaching implications for cosmology"); T_RH ≲ m_Q/25 verified at l.785 ("must also assume … m_Q/25 to avoid equilibrating the quirks"). Additions (window numbers, SU(2) conversion, T^{21/4}, ×2.2) correctly labelled as the track's |
| R3-C1 | §0.2 (ii), Q10, P3, title | Yes | Title is "(v4)". "Status: v3" in l.4 remains: C1 |
| R3-C2 | S-10 | Yes | D0 "≳ 15 MeV/cm" verified (1008.3547 l.335); "single highly ionizing track" verified (l.286) |
| R3-C3 | §4.5 monojet row, Box A | Yes | ATLAS 3.2 fb⁻¹ scaled to 12.9; HSCP drives Λ ≲ 0.2 keV; HSCP limits stop at 300 eV |
| R3-C4 | §3 row 22 | Yes | All four caveats present. The S-1 table row (l.242) was not updated: C2 |
| R3-C5 | S-1 (e) l.258-259, §4.1 V3/V5 | Yes | γ* caveat, (γ*−1) scaling, "suggest", match by index |
| R3-C6 | S-4 (d) | Yes, one wording point | 2108.06748 §5 quote is verbatim (l.1120-1121). Check of the context (§4.3, Eq.4.18): the crossing time scales as (m/100 GeV)(keV/Λ)² × f(E/m), and the amplitude as m/Λ² (γ*−1). Both carry only m/Λ² and velocity, so this supports the degeneracy theorem. "Refutes"/"incorrect" is slightly strong for a concluding remark about Δl_Q, Δt_Q distributions in FASER 2: C5 |
| R3-C7 | various | Yes | Li §IV n_T (Box B l.170), Li Tab.I 37 % (X-11), KLN/E-L retardation (S-1; E-L l.229 "retarded time corrections … neglected" and KLN l.542 "useful to check this by direct simulation" verified), Knapen Eq.8-9 (killed list l.861), Li §VIII (l.870), HKM (l.528), 0 T (l.832) |
| R3-C8 | S-16 | Yes | KLN §5 Eq.5.59; E-L Eq.4.4 |
| R3-C9 | S-2 (c) | Yes | |

## 2. Regression scan

| Search | Result |
|---|---|
| ×0.04-60, 0.2-35 mm, 0.2-21 mm, 140-570 µm | Only in the v1 withdrawal paragraph (l.56), the killed-list and labSS rows (l.226, 245, 859), all labelled as v1 or labSS values. No live use |
| 0.65 TeV | Only as "revised from" (l.60, 465-476), an upper bound for B = 0 with long delay (l.205), and Farina-Low's 650 GeV at 1 eV (l.157-159). No live use |
| "first LHC limit" / "none performed" | Removed. Remaining "none performed by this track" (l.99, 794) is correctly qualified |
| "≈ 15 % low" | Every instance is γ*-qualified (l.49, 57, 120, 250, 660, 715, 974 + §10.2). l.57 adds "at γ* = 1.28" |
| 0.11-0.18 TeV FASER | Only in the "misreading" statement (Box A) and the superseded R2-B3 row (l.1029, tagged "superseded by R3-B1") |
| "only if B ≲ O(10)" | Now only at 3-50 keV (S-8, §4.5, §0.2, §10.3). l.1029 is a historical row, annotated |
| Exec summary vs body | Consistent: FASER per-Λ numbers, 0.15-0.35 TeV, γ* deficit, T_RH credit, window edge. Two items less carefully qualified than the body (C2, C3) |

## 3. New issues from v4 edits

No A or B. Checks that could have failed and did not:
- The "beats existing limits" statement against FASER/D0 (per-Λ table): consistent with R3's table, including "partly" at 3-30 keV for B ≈ 80 and the D0 107 GeV floor at 100 keV.
- The credit paragraphs make no claim stronger than the cited text.
- The track's "new" lists are still new after the credits: converged-Li γ* dependence, B ln(1/B), MS numbers, degeneracy theorem, quantified MET window, causal global fit.
- No internal number changed in v4; the §10.3 mapping to locations is accurate.

## 4. C items

- **C1.** Housekeeping: l.4 "Status: v3, after reviews R1 and R2" should be v4 after R3; l.3 "Executors: S (v1), F1 (v2…)" omits the v3/v4 passes; l.720 "Counts (v2)".
- **C2.** Exec §0.2 item 3 states "~m_Q independent" and "Λ^−1.6…−2.0" without the Li §V/Fig.4 credit (only "Li et al. already showed the formula is order-of-magnitude"), and "Λ-independent at 0.6-3 keV" (also the S-1 table row l.242, "a γ* effect, not a Λ effect") lacks the R3-C4 qualifier that Λ-independence was tested only at γ* = 1.28 and the γ* dependence only at 1 keV. Add one clause each.
- **C3.** Exec §0.2 and §4.5 say the update beats existing limits "near 100 keV", but f_stop was computed only to 3 keV (E-L flat to 10 keV). The S-8 body flags this; the exec summary and the §4.5 "Expected" cell should say "extrapolated" (and note the in-flight annihilation caveat above ≈ 0.1 MeV already in S-8 Value).
- **C4.** "What changed in v3" item 4 (l.51, "does not beat FASER/D0 at its low end") is now partly superseded and carries no tag (the v4 list above it is right). Add "(superseded by v4: per Λ)".
- **C5.** S-4/§10.3: soften "refutes/incorrect" for 2108.06748 §5 to "is not supported by the theorem (amplitude and period carry only m/Λ² and velocities; Eq.4.18)". This is accurate and stronger evidence than the bare assertion.
- **C6.** l.430 attributes "10-20 % of events" to Li Tab.I, while X-11 (correctly) says Tab.I gives 37 % at 500 GeV and the strategy took the lighter points. Harmonise to "the strategy's reading of Tab.I".
- **C7.** FASER numbers are by-eye readings (my re-read of the 1 keV point is ≈ 110 vs 105, within the stated error). Keep the HEPData instruction; consider marking the table UNVERIFIED until HEPData is read.

## 5. Files

`review/REVIEW_R4.md` (this file). No code was needed. The Fig.5 render was made in the session scratchpad only.
