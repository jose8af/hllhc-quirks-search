# Figure manifest (paper/figures/)

Copies of reviewed figures; never edited in place. sha256 (first 12 hex) of the copy at copy time (2026-10-16, Phase A; updated Phase B).
Labels on the plots: 'Private work (simulation)'; truth-level figures also 'truth level'. The T-figures use the default
full right label ('√s = 14 TeV, PU 200, 3 ab⁻¹'); their captions state that pile-up is not simulated at truth level.

| file in paper/figures | source | level | used in | sha256[:12] |
|---|---|---|---|---|
| schematic_nearmiss.{pdf,png} | made here: `paper/figures/src/make_schematic.py` (conceptual diagram, no data) | — | Fig. 1 (Sec. 3.3) | regenerated |
| S3_p1_dsB_c.png | `sim/stage3/figures/p1_dsB_c.png` (Stage-3 diagnostic, Stage 3 PASS R3) | truth | Fig. 2 (Sec. 4.2) | 7d4e4cebb4ac |
| T1_u2_thickness_F_m{200,500,1000,1500}.pdf | `stage5/figures/final/truth/` (Stage 5 PASS R2; full right label + 'truth level') | truth | Fig. 3 (2×2) | 67c3c5cf79f4 / 1a18bf921191 / c19e9301ac39 / 5bf50baa63a8 |
| T1_u2_thickness_S_m500.pdf | same | truth | referenced in Fig. 3 caption (not shown) | bc60748658c2 |
| T2_u2_ratio_vs_x.pdf, T3_u2_ratio_vs_lamcross.pdf | same | truth | Fig. 4 (1×2) | 97c85d69ecad / 0467a3d6d5d2 |
| S3_p2_sepIT.png | crop (pixels unchanged; `magick -crop 540x493+1100+0`) of panel 3 of `sim/stage3/figures/p2_observables.png` | truth | Fig. 9 (left) | crop |
| T4_truth_edges_vs_mass.pdf | `stage5/figures/final/truth/` | truth | Fig. 9 (right) | 9b72d1045baf (R2) |
| D3_bsum_vs_rung.pdf, D4_pfake_extrapolation.pdf | `stage5/figures/final/` | det | Fig. 5 (1×2) | c4c8e9688d84 / 8f0c57402ec9 (R2) |
| D1_eps_map_rfb.pdf, D2_eff_vs_rung_F200.pdf | same | det | Fig. 7 (1×2) | 54c45128b1f3 / eda99ada80db (R2) |
| D5_limit_mu_vs_lambda_F200.pdf, D6_limit_xsec_vs_m_L1p5.pdf | same | det (A truth) | Fig. 8 (1×2) | 9a499b25a2dc / c9ad94e3b448 (R2 + R3-NORM + paper R3) |
| D9_edges_det_vs_truth.pdf, D10_sepit_calibration.pdf | same | det + truth overlay | Fig. 10 (1×2) | 535d6b8bbbcf / 2d116c075ed3 (R2, D9 paper R3) |
| D8_mest_RA_F500.pdf, D8_mest_RA_F1500.pdf | same | det | Fig. 11 (1×2) | decdf73765e2 / 459935c5da7f (R2) |
| D7_exclusion_map.pdf | same | det (A truth) | Fig. 12 | 6d381b4dc171 (R2 + R3-NORM + paper R3/R4) |
| D11_event_display.pdf | same | det | Fig. 6 (Sec. 7.6; App. D removed) | 9bdecf9f5bf9 (R2) |

No figure comes from `stage5/figures/final/truth_sqrt_s/` (user decision: full right label only).
`S3_p2_observables.png` (full 7-panel copy) is kept in paper/figures/ but no longer used (illegible at print size; review B-9).
Not used (in the stage reports only): D1 at R_A–R_E, D2 for the other masses, D5/D6 for the other masses/Λ, D8 at r_fb.

**Fix round R2 (2026-10-16, review R2 B-4).** All D-figures above and T4 were regenerated in Stage 5 (`stage5/make_figures.py
--final --only D1,...,D11` and `--truth --only T4`) with larger in-figure text for print size (legend and tag blocks
`x-small` → `small`, map cell values and rung tick labels `xx-small` → `x-small`), shorter tag blocks, and no internal
identifiers (no "INV_A2FC_E500 open", "WP_RULE A.2b", "acceptance.json", "§8", job/trial ids, "(see D9)"; Fig. 10 right
uses the note symbol d_IT). Numbers in the figures are unchanged. The σ_th labels in D6/D7 are kept; the text defines σ_th as the figure label of σ_norm (App. A).
The copies are byte-identical to `stage5/figures/final/` (checked with `cmp`); the hashes above (R2) are of these copies.

**FIX R3-NORM (2026-10-16).** D5_F200, D6_L1p5 and D7 were regenerated in Stage 5 with N_exp = σ_norm·f₂₀₀·L·A (upstream
fix `acts/stage4/review/FIX_RESULTS_R3_NORM.md`; D6 is now a limit on the inclusive σ) and recopied here (byte-identical;
hashes above). Fig. numbers follow v0.3: the event display moved from App. D into Sec. 7.6 (Fig. 6), so the later P2
figures shifted by one.

**Paper review R3 (2026-10-16).** D6 legend "NLO K" → "K_QCD" (C-3); D7 tag "median ≥ 790 in every cell, −1σ edge ≥ 54" (R4: floor)
(C-1; min −1σ/N_exp = 54.5 at E200 1.5 keV, STAGE4_SUMMARY); D9 tag "12.8-25 keV" (C-4). Regenerated in Stage 5 (D6: 6 files,
D7, D9) and recopied; hashes above.
