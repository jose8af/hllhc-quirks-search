# FIX_PAPER_R2: fixes for REVIEW_PAPER_R2 (3 A, 6 B, 10 C)

Fixer, JFC loop, 2026-10-16. Note v0.3: 35 pp. The build is xelatex + bibtex + 2× xelatex. It has 0 errors, 0 overfull
boxes and 0 undefined references. About 1/3 page is free on p. 35 for the A-3 paragraph.

Every changed page was rendered and inspected (pp. 1–3, 17–30, 33–35):
- at 80 dpi;
- with the 13 P2 figure files also viewed individually at full resolution;
- with the sibling Stage-5 figures viewed on contact sheets.

Sources used:
- `STAGE4_SUMMARY.json`;
- `C12FC_v1/{limits,acceptance}.json`;
- `STAGE4_RESULTS.md`;
- `INV_STATS_BKG.md`;
- `sim/stage3/HANDOVER_STAGE4.md`;
- `stage5/external_bounds.json`.

**Coordinator hold (received mid-task).** Do not settle A-2 by choosing definitions that reproduce 37.6. The reason is a
possible missing f(pT(QQ̄) > 200 GeV) in N_exp, raised in `P2_NOVELTY_AUDIT.md` item 3. I had already rewritten
Eq. (11), §6.5 and §8.3 with N_exp = σ_norm·L·A and σ₉₅/σ_norm = μ₉₅/N_exp. That rewrite was **reverted to the v0.2
wording**, and every N_exp / σ_th / σ_norm / limit-ratio passage carries a `% NORM-ANCHOR` comment. No number changed.
The anchor locations are listed at the end.

## Status per finding

| finding | status | change |
|---|---|---|
| **A-1** stale C′ rates | RESOLVED | §7.4: 0.43/0.050/31.1/0.22/1.57 → 0.38/0.052/30.3/0.30/1.59 (`STAGE4_SUMMARY.json → cprime.*.rate_t`: 0.3786, 0.0524, 30.31, 0.3017, 1.5945), with "maximum over the SM processes" added; NI 0.10–0.12 unchanged. Grep of the .tex: no 0.43/31.1/0.22/1.57 left in a C′ context (the other hits are unrelated P1 numbers). 4 instances updated in 1 file. |
| **A-2** inconsistent ε / N_exp / σ_th, FB_k undefined | PARTIAL (held) | Done: FB_k defined in §6.5 (r_fb = FB_{k_adm} ∧ h > 5 ∧ o > 5 (∧ dE/dx > e_adm); FB_k = non-width part of R14 with a single cut w_core < W_c/2^k; FB0 has no width cut; e_adm defined). ℰ_status defined in one clause after Eq. (11). App. A gains R01–R23, R_A–R_E (with definitions), h and o, FB_k, r_fb, k_adm, e_adm, Λ_R, R_eff, M_est, β_ToF and K_SM. **Held (NORM-ANCHOR):** the definitions of N_exp, A, ℰ and σ_th/σ_norm, the μ₉₅ definition, the 37.6 sentence and the Fig. 11 / Tab. 9 captions are back at v0.2 text. Verified for the coordinator: as coded, the 37.6 is μ₉₅/(σ_norm·L·A) with A = ε_fid·ε_trig·ε_presel\|trig = 0.5035 (acceptance.json), σ_norm = 219.2 fb, μ₉₅ = 1.2458×10⁷ (limits.json, s = [0, 0.045]) → N_exp = 3.311×10⁵ and ratio 37.62. A carries no f(pT > 200) factor; whether that is a bug is the open question. |
| **A-3** prior-work contrast | NOT DONE (per instruction) | Only the factually wrong sentence was corrected (intro, neutral): "The published central-detector reach estimates [Knapen, Li 2019] use simplified detector models with simulated pile-up overlays (an average of 50 interactions per crossing in Ref. [Knapen])." `% A3-ANCHOR` comments were placed in the intro (01 l.34) and after the "adds no exclusion" paragraph of §10 (10 l.18). The "What is new" paragraph is untouched (A-3 item 4). |
| B-1 SM samples / proxy count | RESOLVED | §7.3: "W(τν)+jet (split by τ decay class) and tt̄ (one lepton)". The not-simulated list now includes W(eν) and W(μν). "eight processes" added. §12 item 6: "Eight SM processes (W(eν), W(μν), tt̄ dileptonic, t-channel top, tW, WW, WZ, ZZ)". |
| B-2 §13 "(ii)–(iv)" | RESOLVED | Now reads "Even with (ii) and (iii) … (estimate, from the previous analysis run; order of magnitude unchanged)". |
| B-3 "conservative" | RESOLVED | §8.1 now reads "conservative with respect to simulation statistics … but the untested rung factorisation can bias them in either direction". §12 item 4 is qualified the same way. §8.4 (iv): "anti-conservative where both categories carry signal (23 of the 33 points with a limit; recounted from limits.json), but irrelevant at the headline point". |
| B-4 figure legibility and stale/internal text | RESOLVED | See the next section. The external-bound list moved into the Fig. 11 caption: D0, the Farina–Low benchmarks, and the HSCP, monojet and Evans–Luty out-of-time recasts with their Λ and m_Q ranges from external_bounds.json. The caption also states the fast-path ε systematic. |
| B-5 reach meaning | RESOLVED | §7.2: "the reach would suffice in principle, but the deepest rung with at least ten ρ = 2 counts is R06". |
| B-6 P2 framing | CHECKED, no change | Nothing in the abstract or §13 claims a first study of pile-up. The rest belongs to A-3. |
| C-1 abstract | PARTIAL | "Stage-3 hits" → "Truth-level quirk hits". The ε-uncertainty / 43–45 parenthesis was added and then **reverted** (limit-ratio text, NORM-ANCHOR). |
| C-2 Fig. 6 caption | RESOLVED | Now reads "eight cells … (the ninth full-chain point, Ẽ 500 at 5 keV, is not in this map)". The D1 tag also reads "8 cells full chain". |
| C-3 | RESOLVED | "(Ẽ 500: 2 keV only)". SR-T share: "typically 30–70% (range 0–100%)". |
| C-4 K collision | RESOLVED | The SM K-factor is now K_SM (§7.3, App. A). |
| C-5 internal labels | PARTIAL (cheap ones) | "C12FC_v1" is defined once (§7 intro); §8 intro and the Tab. 8 caption say "final run". "analysis fix R6" / "pre-R6" → "the last analysis fix" / "the dry run before that fix". §6.6 was condensed and drops "R1–R6". V4-x, A2FC, D13 and C1a/C1b/C2B are kept (defined in Tab. 6 / App. C). |
| C-6 bibliography | RESOLVED | FASER:2026fsy: month removed, note "in press". The HEPData title is braced with TeX quotes. Logged in BIB_PROVENANCE.md. |
| C-7 recast name | RESOLVED | "Evans–Luty out-of-time recast" is used in both the figure and the caption. |
| C-8 V4-4 | RESOLVED | §12 item 7: "the seed-threshold regression check (V4-4) is partial". |
| C-9 | RESOLVED | Fig. 10 caption: "starts near the pair-mass threshold". |
| C-10 PV-pair chain | RESOLVED | §7.4: "The PV-pair term, 1.4×10⁵, follows a different chain, bounded by the zero count of the conditional p(R08 \| R02) on 24 merged candidates" (INV_STATS_BKG). |

## Figures (B-4)

All figure changes were made in `stage5/plotting.py` and `stage5/make_figures.py`. They change text and layout only;
every number is unchanged.

**Global font changes:**
- Legend and tag block: x-small → small.
- Map cells and rung ticks: xx-small → x-small.

**Regeneration and copies:**
- Regenerated: all D1–D11 (38 files) and T4, into `stage5/figures/final/`.
- Copied: the 13 used files, into `paper/figures/` (byte-identical to the Stage-5 output).
- Records updated: `FIGURE_MANIFEST.md` (new sha) and `stage5/FIGURES_FINAL.md` (new "Paper fix round R2" section; the
  INV_A2FC_E500 status is now CLOSED).

**Removed from the figures:**
- "INV_A2FC_E500 open" and "numpy-A2 …" (D7);
- "WP_RULE A.2b" (D1);
- "acceptance.json" (D6, D7);
- "§8" (D1, D3, D5, D8);
- "(D9)" (D1 R_A, T4);
- "INV_SIGNAL_EFF §3.1" and "STAGE4_RESULTS §6.1" (D9);
- "B1_00201, trial 28" (D11; still in the sidecar).

**Notation in the figures:**
- D10 axes and tag use d_IT.
- σ_th labels in D6 and D7 are kept (held).

**Layout fixes found on inspection:**
- D2, D4, D8, D9, D10 and D11 had legend/tag overlaps at the larger font. Fixed with y-range, legend and tag-position
  changes.
- Fig. 11 is now 0.47 lw, with the long tag moved to the caption.
- Fig. 12 is now 0.34 lw.

**Lint:** 8 hits, the same documented deviations as before.

**Page budget:**
- Appendix tables and the bibliography are set in \footnotesize.
- §6.6, the A2FC paragraph of §8.2 and the G3 part of §7.2 were condensed. No fact was dropped.

## Other changes
- Change log v0.3 entry.
- Version 0.3 on the title page.
- ISSUES.md item 9 marked resolved; item 8 notes that INV_A2FC_E500 is closed.

## NORM-ANCHOR locations (`paper/sections/`)

| location | passage held |
|---|---|
| 00_abstract.tex l.29 | "at best 37.6 times the predicted cross section" |
| 06_strategy_wp.tex l.20 | Eq. (11): ℰ chain and N_exp = σ_norm L ℰ |
| 06_strategy_wp.tex l.136 | §6.5 statistical treatment: limit on the signal yield |
| 08_results_p2.tex l.68 | §8.3: conversion with A and N_exp = σ_norm L A |
| 08_results_p2.tex l.74 | §8.3: headline σ₉₅/σ_th = μ₉₅/N_exp = 37.6, all other ratios, 43–45 |
| 08_results_p2.tex l.89 | Table 9 caption: N_exp = σ_norm·3 ab⁻¹·A |
| 10_bounds.tex l.11 | §10: σ₉₅/σ_th map, "minimum 37.6" |
| 10_bounds.tex l.21 | Fig. 11 (σ₉₅/σ_th caption and D7 cell values) |
| 01_introduction.tex l.58 | "What is new": "at best 37.6 times the predicted signal" |
| 08_results_p2.tex l.114 | Fig. 7 caption: "at least 37.6 times the prediction" |
| 08_results_p2.tex l.123 | §8.4 (i): "small against the factor ≥ 37.6" |
| 12_limitations.tex l.39 | ℰ_tot = A × ℰ_finder |
| 13_conclusions.tex l.23 | "at best 37.6 times the predicted signal; ≈ 43–45" |
| A_notation.tex l.46, l.56 | ℰ row; N_exp, μ₉₅ row |

The in-figure ratios of D5, D6 and D7 carry the same numbers and must be regenerated if the normalisation changes.
`01_introduction.tex` l.34 and `10_bounds.tex` l.18 are the A3-ANCHOR comments.

**Open:**
- A-3: the paragraph goes at the A3-ANCHOR locations.
- A-2 core: the definitions and ratios, pending the normalisation verdict.

---

## Addendum (2026-10-16): normalisation fix (R3-NORM) and A-3 applied; all anchors removed

The coordinator confirmed the missing tail fraction. The fix is upstream: `acts/stage4/review/FIX_RESULTS_R3_NORM.md`
(narrow review `REVIEW_RESULTS_R4_NORM.md`, PASS). Every number below comes from the corrected
`STAGE4_SUMMARY.json` and `STAGE4_RESULTS.md` §4.4/§5 (erratum box) and from the R3-NORM before/after table.
All 14 NORM-ANCHOR and both A3-ANCHOR comments are gone. Note v0.3: **35 pp**, 0 overfull boxes, 0 undefined
references. Every page was rendered and inspected.

| item | change |
|---|---|
| **A-2 (closed)** | §6.1 Eq. (11) now defines N_exp = σ_norm f₂₀₀ L A, with A = ε_fid ε_trig ε_presel\|trig ε_PV (truth level, tail sample), S = N_exp ε_sel and ε_tot = f₂₀₀ A ε_sel. The text before it defines f₂₀₀ as the pT(QQ̄) > 200 GeV fraction of the inclusive σ_norm (0.048 / 0.104 / 0.146 / 0.169 for E; 0.114 for Ẽ500) and A_incl = f₂₀₀ A. ε_status is folded in as one clause. "ε without subscript = ε_sel from §8 on". §6.5: μ is the yield in the acceptance, σ₉₅ = μ₉₅/(L f₂₀₀ A) is a limit on the **inclusive** σ, and σ₉₅/σ_norm = μ₉₅/N_exp. σ_th is defined once as the figure label of σ_norm (§6.5, App. A). Normalisation nuisances are not in μ₉₅. |
| §8.3 headline | 37.6 → **790**. Also stated: N_exp 1.58 × 10⁴, S = 710, σ₉₅ = 1.7 × 10⁵ fb vs 219 fb; the 95 % CP edge ≈ 420; ε ≈ 36 needed. The full-chain systematic is ≈ 910–950 [EST, not applied] (was 43–45). Second best 820 (was 39.1); range 2.3 × 10³–6.0 × 10⁷. Per-mass bests: 1.3 × 10⁴ / 3.8 × 10⁵ / 3.8 × 10⁶ / 2.8 × 10⁵. S ≥ 3 at B = 0 at only 20/40 points (E1500 ≤ 0.3; replaces "1.7 events"). μ_5σ/N_exp 1.9 × 10⁴–2.4 × 10⁸. The "−2σ edge below the prediction" sentence was removed (min −2σ/N_exp is now 1.7). One erratum sentence was added. |
| Table 9 | New f₂₀₀ and A_incl columns. N_exp = 1.55–1.58 × 10⁴ / 1.08–1.09 × 10³ / 55–56 / 4.2 / 85–86. |
| Fig. 8 (D5_F200, D6_L1p5), Fig. 12 (D7) | Recopied from `stage5/figures/final/` (regenerated upstream: legend N_exp = σ_norm·f·L·A, inclusive σ, cells ≥ 790). FIGURE_MANIFEST hashes are 9a499b25a2dc / 9f2592a43ce4 / b3098f9cc677. Captions: "at least 790", "inclusive cross section"; the Fig. 12 caption says the figure labels the ratio σ₉₅/σ_th. Figures were viewed. |
| §8.4 (i), §10, §13, abstract, intro, changelog | Ratios are now 790 (and ≈ 910–950 in §13). The abstract, §13 and the change log each carry a one-clause erratum ("corrected for the pT(QQ̄) > 200 GeV tail fraction, omitted in an earlier version"). |
| §12 item 7 (coordinator, R4) | Added: "The Stage-2 tail-rate uncertainty of f₂₀₀, +12–15 % / −11–13 % from varying the matrix-element α_s in MadGraph (ESTIMATE; sim/VALIDATION.md), is not propagated into the limit ratios". Also ε_tot = f₂₀₀ A ε_sel. |
| App. A | New rows for f₂₀₀, A/A_incl, ε_sel/ε_tot, N_exp/S, μ/μ₉₅, σ₉₅ and σ_th (figure label). |
| **A-3 intro** | The "Experimental situation" paragraph now carries the audit's replacement text. Knapen et al.: ATLAS-like barrel, simulated ⟨µ⟩ = 50 overlay, reconstruction efficiency ≤ 73 % (≈ 2 % total), negligible background assumed, 650 GeV with 300 fb⁻¹. Li, Li, Pei and Zhang (authors re-checked on INSPIRE, matching references.bib): simulated Z(νν)+jets with ⟨µ⟩ = 50, 450 GeV at 100 fb⁻¹ for N_IC = 3, and a non-negligible Z(νν) background. Neither simulated PU 200, hit-level tracking or material single-interaction fakes. The other prior work follows. "What is new" now has a "to our knowledge" P2 statement restricted to audit items N1, N3 and N4, with credit to Knapen for the signature, the factorised PU estimate and the Λ window, plus "null result reflects our background method, not a tension". |
| **A-3 §10** | New paragraph "Comparison with published reach projections". It states that the null result comes from the background method, not from a physics tension. At B = 0 our efficiencies give ≈ 1 TeV (3 ab⁻¹) and a 5-event reach of ≈ 0.6 TeV (300 fb⁻¹), close to Knapen's 650 GeV [EST, with f]. Total efficiency ≈ 0.005 at E500, ≈ 4× below theirs. The break-even B ≈ 8 × 10² (σ_ln = 1) compares with a ~6 × 10⁵ zero-count bound. The deep-rung floor comes from single-interaction and SM terms that do not scale with PU. "Does not show those projections to be wrong". **Recomputed** from the R3-NORM best-Λ S (861 / 87.2 / 3.40 / 0.295), log-linear in m_Q: S = 3 at 3 ab⁻¹ → 1.03 TeV; S = 5 at 300 fb⁻¹ → 0.59 TeV; f·A·ε(E500, 2 keV) = 0.104 × 0.567 × 0.08 = 0.0047. The audit numbers hold. |
| Page budget | The event display moved from App. D into §7.6 (now Fig. 6; App. D removed, FIGURE_MANIFEST renumbered). Bibliography in two columns (`multicol`). Appendix tables in \scriptsize. Compact ToC spacing. Vertical margins 2.0 → 1.8 cm. Fig. 3 panels 0.34 lw, Fig. 2 0.40 lw, Fig. 12 0.44 lw. §7.6, §11 opening and the v0.2 change-log entry were condensed. |

**Stale-value grep.** Searched the .tex for 37.6, 43–45, 3.3 × 10⁵, 39.1, 109, "1.7 signal", ≈ 20 and σ_th. The only remaining 37.6 is the change-log "37.6 → 790". σ_th appears only where it is defined as the figure label. The PDF text has no 37.6 except the change-log line.

**Not done.** μ₉₅ does not include the signal-normalisation nuisances (stated in §6.5, §8.4 and §12). The σ_th labels inside D6/D7 were not renamed: they are Stage-5 figures, and the label is defined in the text.
