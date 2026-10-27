# Outline: C001 quirks P1+P2 paper-level note (`quirks_p1p2_note.tex`)

User decision 2026-10-16: concise note, 25–35 pp incl. figures, P1 and P2 together, JFC-AN spirit (completeness via the
cited stage reports). Build: xelatex + bibtex (`unsrtnat_hep.bst`; see the header of `quirks_p1p2_note.tex`). Sections
are `sections/*.tex`.

**Status (v0.2, 2026-10-16, Phase B done): 35 pp, all sections drafted, no TODO left; clean compile (no errors, overfull
boxes or undefined references); 49 bib entries, 47 cited.** Layout choices for the page cap: margins 2.0 cm, tocdepth 1,
bibliography `\small`, 1×2 composites at height 0.37 lw, P1 table reduced to 1 and 5 keV, event display in App. D.

| # | file | section | start p. | figures / tables | sources |
|---|---|---|---|---|---|
| – | 00_abstract, 00_changelog | abstract (final), change log | 1–2 | – | all |
| 1 | 01_introduction | introduction, prior work, what is new | 2 | – | literature, NOVELTY_AUDIT |
| 2 | 02_model_samples | model, generation, σ_norm, modelling systematics | 4 | Tab. 1 | sim/VALIDATION.md, SAMPLES.md |
| 3 | 03_string_dynamics | near-miss mechanism, ϑ, thickness law, c, numerics, population-c status, validity | 5 | Fig. 1 schematic; Tabs. 2–3 | analytic/NEAR_MISS_IMPULSE.md, NUMERICS.md, NOVELTY_AUDIT.md |
| 4 | 04_truth_p1 | Stage-3 propagation, law vs simulation (failed V2b gate disclosed), 3–5 keV excess, MS floor, B+MS | 10 | Fig. 2; Tab. 4; Fig. 3 (2×2); Fig. 4 (1×2) | sim/stage3/README.md, VALIDATION.md, u2_panel |
| 5 | 05_detector_chain | ACTS geometry, PU 200 + TDR top-up, digitisation, CKF, PV/MET, samples | 14 | Tabs. 5–6 | acts/stage4/plan.md, G1/G1b/G3, C1_LAUNCH |
| 6 | 06_strategy_wp | trigger, F0/F1, ladder, B sum, WP rule, fallback, statistics, freeze | 15 | Tab. 7 | WP_RULE.md, WP_RULE_PC19.md |
| 7 | 07_backgrounds | PU extrapolation + closure (×2.41), SM, single-interaction terms, ladder, why statistics cannot give a WP | 19 | Tab. 8; Fig. 5 (D3, D4) | STAGE4_RESULTS §1–3 |
| 8 | 08_results_p2 | no WP, V4-3 partial, ε at PU 200, A2FC + E500 3 keV, fallback limits (37.6), acceptance, systematics | 22 | Fig. 6 (D1, D2); Tab. 9; Fig. 7 (D5, D6) | STAGE4_RESULTS §1, §4, §5 |
| 9 | 09_mass_lambda | truth handles; detector Λ edges, sep_IT not measurable; M_est pair-mass proxy; P2 verdict | 24 | Fig. 8 (sep_IT crop, T4); Fig. 9 (D9, D10); Fig. 10 (D8 ×2) | Stage-3 P2.json; STAGE4_RESULTS §6 |
| 10 | 10_bounds | FASER, D0, Farina–Low; no exclusion beyond existing bounds | 27 | Fig. 11 (D7) | stage5/EXTERNAL_BOUNDS.md |
| 11 | 11_opendata | Open-Data outlook + policy caveat | 27 | – | opendata/STAGE6_FEASIBILITY.md |
| 12 | 12_limitations | P1 (3) and P2 (6) limitations | 28 | – | STAGE4_RESULTS §8 |
| 13 | 13_conclusions | P1 verdict, P2 verdict, what would be needed | 29 | – | all |
| – | references | 47 printed | 30–31 | – | references.bib, BIB_PROVENANCE.md |
| A–D | appendices | notation; reproduction; limitation/decision index; event display | 32–35 | Fig. 12 (D11) | – |

Review trail: `review/REVIEW_PAPER_A_R1.md` → `review/FIX_PAPER_A_R1.md`. Phase-B sections not yet reviewed.
