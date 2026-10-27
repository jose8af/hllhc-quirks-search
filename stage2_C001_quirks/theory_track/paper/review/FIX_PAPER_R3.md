# FIX_PAPER_R3: fixes for REVIEW_PAPER_R3 (1 A, 0 B, 7 C)

Fixer, 2026-10-16. Note v0.3, **35 pp**. Build: xelatex + bibtex + 2× xelatex. It has 0 overfull boxes and 0 undefined
references. Changed pages 3, 5, 24, 27, 28 and 33 were rendered at 80 dpi and inspected.

| finding | status | change |
|---|---|---|
| **A-1** prior-work background classes | RESOLVED | **Intro (01 l.32–34):** "Neither study simulated pile-up 200 or hit-level tracking, and neither treated single-interaction fakes beyond beam-pipe photon conversions (Knapen et al.) or SM backgrounds beyond Z(νν)+jets (Li et al.)". **Novelty clause (01 l.59–61):** "with the full set of single-interaction topologies as backgrounds (beyond the beam-pipe conversions of Knapen et al.)". **§10 (l.24–27):** the floor is "set by single-interaction topologies (PV pairs, decays in flight, nuclear interactions, loopers) that neither study treated and by SM terms estimated here at the zero-count level, none of which scales with pile-up. Both studies assumed zero or a small background after their cuts." The main contrast is kept. |
| C-1 Fig. 12 "−1σ" | RESOLVED (figure + caption) | Verified in STAGE4_SUMMARY.json: the minimum of μ₉₅(−1σ)/N_exp is **54.5** (E200, 1.5 keV), so the reviewer's 55× is right (not 550). D7 tag now reads "median ≥ 790 in every cell, −1σ edge ≥ 55" (computed in code). Caption: "(median ≥ 790; the −1σ toy edge ≥ 55)". D7 was regenerated and recopied. |
| C-2 Tab. 2 vs Tab. 9 | RESOLVED (explained) | Tab. 2 caption: N₂₀₀ comes from the Stage-2 sample. It differs by −2 to +4 % from σ_norm f₂₀₀ L ε_fid of Tab. 9, whose ε_fid comes from the Stage-3 template half. N₂₀₀ is not used in any limit. |
| C-3 "NLO K" | RESOLVED | D6 legend now reads "σ_th (E, N_IC = 2, K_QCD, PDF unc.)" (Stage-5 regeneration, 6 files). Fig. 8 caption: "σ_norm with K_QCD, labelled σ_th". |
| C-4 merging comparator | RESOLVED | 12.8–25 keV is used everywhere: Fig. 10 caption and D9 tag (regenerated and recopied); §9.2 already used it. |
| C-5 "first selection" | RESOLVED | Now "the selection of Knapen et al." |
| C-6 f₂₀₀ definition | RESOLVED | "and \|η_pair\| < 4" added to the Tab. 2 caption and to App. A (JSON `normalisation.f_tail_definition`). |
| C-7 set-up differences | RESOLVED | §10: "their set-up differs: 2 T field, √s = 13 TeV, eight-layer ATLAS-like barrel". |

Other files updated: FIGURE_MANIFEST.md (D6 c9ad94e3b448, D7 798f24852289, D9 535d6b8bbbcf) and stage5/FIGURES_FINAL.md
(new "Paper review R3" section).

**R4 note (2026-10-16).** The D7 tag now floors the −1σ edge (54.6 → "≥ 54", was "≥ 55" by rounding). The Fig. 12 caption matches. D7 was regenerated and recopied (sha 6d381b4dc171); the note is still 35 pp with 0 overfull boxes and 0 undefined references.
