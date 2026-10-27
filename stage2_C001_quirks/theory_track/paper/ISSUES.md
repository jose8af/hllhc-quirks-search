# Issues found in sources while writing the note (paper executor; not fixed: outside paper/)

1. **`sim/stage3/HANDOVER_STAGE4.md` (l.52, header table `sigma_norm_fb`)** labels σ_norm "N_IC = 1"; the stored values
   include N_IC = 2 (see `acts/stage4/review/FIX_RESULTS_R1.md`, LOG 2026-10-16). Proposed: relabel to N_IC = 2. The note
   uses σ_norm with N_IC = 2 (Table 1, Eq. 2).
2. **Author list of arXiv:0805.4642.** The paper has two authors (J. Kang, M. A. Luty). Project files and the paper brief
   call it "Kang–Luty–Nasri"/"KLN" (NOVELTY_AUDIT already notes this). The note cites "Kang and Luty".
3. **Stage-3 diagnostic figures used in the note are not restyled** to the JFC conventions (`p1_dsB_c.png`,
   `p2_observables.png`: matplotlib-stitched multi-panel, custom figsize, small fonts, PNG only). Stage 5 restyled only the
   U-2 panels and the edges (T1–T4). They carry the approved 'Private work (simulation) -- truth level' label, so they are
   used as is; a restyle (T5: Δs_B and c vs Λ; T6: P2 observables) would remove the only non-JFC figures in the note.
4. **Truth-level T-figures carry 'PU 200, 3 ab⁻¹'** in the right label (user-approved default). Not an error; every caption
   in the note says pile-up is not simulated at truth level.
5. **INSPIRE metadata of arXiv:2601.09023 (LHCb quirks)** gives year 2020 / volume 26; the DOI says JHEP 06 (2026) 037.
   Corrected in `paper/references.bib` only (logged in BIB_PROVENANCE.md).
6. **Stage-1 note: the number-of-oscillations formula** N_osc = σR/(2β*p_T) is quoted from T2 §2.2 without a derivation in
   NEAR_MISS_IMPULSE.md; the note cites it as a project estimate. Minor.
7. **Decision label clash D12** (ambiguities.json vs LOG) — already flagged in LOG (renamed D13); the note uses D13.
8. **P2 results not yet usable**: `acts/stage4/STAGE4_RESULTS.md` and `stage5/FIGURES_FINAL.md` are under review
   (Phase B). Open flags in LOG that the note will have to reflect: E500 3 keV A2FC efficiency drop (INV_A2FC_E500 OPEN; CLOSED since, ×0.87, and the stale D7 in-figure text was removed in fix R2),
   D8 M_est bimodality, D11 PU-only fake along the MET direction.
9. **(Fix A-R1 / Phase B) Internal figure ID inside a plot:** `stage5/figures/final/truth/T4_truth_edges_vs_mass` carries
   "(see D9)" in its in-figure text (Stage-5 internal figure id). Not editable from paper/; the caption explains the
   comparator. Suggest removing it at the next Stage-5 regeneration. **Resolved in fix round R2** (T4 regenerated without it).
10. **(Phase B) Stage-3 `p2_observables.png`** cannot be split cleanly into panels (the rotated y-label of one panel overlaps
   the neighbouring panel's data area); only the IT-separation panel was cropped. A restyled single-panel Stage-5 version
   (sep_IT and merging fraction vs Λ) would be cleaner.
11. **(Phase B) STAGE4_RESULTS wording vs REVIEW_RESULTS_R3 C-1/C-2:** the report states the aggregate full-chain loss as
   "CKF hit stealing" (a fact) in §0/§4.3; R3 C-1 notes it is an inference confirmed for one row. The note says "attributed
   to CKF hit stealing, confirmed directly for one event and inferred for the aggregate".
12. **(Phase B) Systematics not propagated:** the plan's MET-resolution (15/35 GeV), trigger turn-on (±25 GeV) and PV-ID
   variations are not propagated to the final limits (STAGE4_RESULTS reports them as [U] assumptions); the note says so
   (Sec. 8.4).
