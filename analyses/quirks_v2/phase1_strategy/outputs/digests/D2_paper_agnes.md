# D2: digest of paper v0.4, its novelty audit and ISSUES (investigator Agnes, 2026-11-13)

Scope: `TT/paper/quirks_p1p2_note.tex`, `TT/paper/sections/*.tex`, `TT/paper/P2_NOVELTY_AUDIT.md` (AUD),
`TT/paper/ISSUES.md`, against `publication_plan/publication_plan.tex` (PLAN). TT = `stage2_C001_quirks/theory_track`.
All files read in full. Section files are cited by their number prefix (for example `07:103` means
`TT/paper/sections/07_backgrounds.tex:103`; `D:` is `D_derivation.tex`, `C:` is `C_limitation_index.tex`).
Tags: **V** = VERIFIED (re-derived by arithmetic in this session, command in the log), **U** = UNVERIFIED (transcribed
from the cited line), **E** = ESTIMATE (an estimate in the source, or mine). "SUP" = superseded by v2 (item named).
Fixed decisions applied throughout: S3 dropped (barrel only), no cloud, no pile-up scans, no CMS Open Data.

## 1. Section map of v0.4 against the target structure (PLAN §3.2, :206-224)

| v0.4 file | content (one line) | target slot | status |
|---|---|---|---|
| note.tex:5-20 | title (P1+P2), "not a CMS result" box, author placeholder | title, disclosure | **rewrite**: plan title; add AI-workflow and CMS-membership disclosure (W1). There is no AI disclosure anywhere (grep) |
| 00_abstract | P1 law, then P2 "no WP, 790×, nothing excluded" | abstract | **rewrite**: lead with the v2 estimate and reach; keep the negative results |
| 00_changelog | v0.1-v0.4 log, 3 `\rep` | App. pre-registration record | **move** (or drop) |
| 01_introduction | quirks, prior work (Knapen, Li, FASER, D0), P1/P2 questions, "What is new" | §1 Introduction | **rewrite**: main result and figure on page 1; novelty wording per AUD §3.3 (AUD:362-365) |
| 02_model_samples | E/Ẽ, MG5+Pythia, σ_norm = N_IC·K·σ_LO, f_200, modelling systematics | §2 Model, samples, cross sections | **keep + rewrite**: NLO K at 14 TeV, f_200 propagated, QED FSR (S2); remove the |η|<4 (W1) |
| 03_string_dynamics | near-miss mechanism, b_odd, rotation, thickness law, numerics, validity | §3 thickness law (compact) | **rewrite/condense**: fix W1 items (0.105 vs 0.104, K_vac, "proper time") |
| 04_truth_p1 | Stage-3 truth test of the law, failed V2b gate, 3-5 keV excess, MS floor, B+MS | §3 (results part) | **rewrite** (P1): window as measured, 9/30 cells, floor tests and B*-off test |
| 05_detector_chain | ACTS geometry, PU 200 + TDR top-up, digitisation, CKF, PV/MET, samples | §4 Detector model | **keep + rewrite**: add B6 robustness; remove the 93% PV efficiency and the campaign ids |
| 06_strategy_wp | trigger, finder F0/F1, ladder R01-R23, B sum, 0.11 rule, fallback, statistics, freeze | §5 finder & selection; stats to §6-7 | **rewrite**: T2 rule, 0.11 only as a flag, C2 cross-check; the endcap clause is out (S3 dropped) |
| 07_backgrounds | PU thinning + closure ×2.41, SM, single-interaction terms, ladder, why counting fails | §6 Backgrounds | **rewrite (core)**: anatomy kept; N4 kept short; estimators B1-B4 + closure + uncertainty model are **new** |
| 08_results_p2 | no WP, V4-3 partial, ε at PU 200, A2FC, fallback limits 790, systematics | §7 Results | **rewrite**: v2 ε (S1), ladder v1-vs-v2, pyhf limits (T1); v1 fallback moves to the appendix |
| 09_mass_lambda | truth handles, detector Λ edges, sep_IT not measurable, M_est proxy | (no slot) | **move/condense** into §7 (Λ window) and §10 (negative results N7/N8); open question O5 |
| 10_bounds | FASER/D0/Farina-Low overlay; Knapen/Li comparison | §9 Comparison | **rewrite**; its key sentence (10:28-29) goes to the intro |
| 11_opendata | CMS Open Data outlook + policy caveat | — | **remove** (user decision) |
| 12_limitations | P1 (3) and P2 (6) limitations | §10 Limitations | **rewrite** after v2 |
| 13_conclusions | P1/P2 verdicts, "what would be needed" | §11 Conclusions | **rewrite** |
| — | data-driven road-rotation sideband | §8 data-driven method (B5) | **new** |
| A_notation | symbol table | appendix | **keep**, update |
| B_reproduction | stage reports and internal paths (41 `\rep`, 7 `\cmd`) | App. reproduction | **rewrite** as a Zenodo/package description |
| C_limitation_index | [A]/[L]/[D] list with internal decision ids | App. limitation index | **rewrite** without internal ids |
| D_derivation | full P1 derivation, status table | App. thickness derivation | **keep** (28 `\rep` to remove) |
| — | v1 frozen result + v2 changes; efficiency tables for recasting | appendices | **new** |

## 2. Key numbers in v0.4 (all U unless marked; SUP = superseded)

**Signal efficiency** (detector level, PU 200, barrel). SUP by S1/T2 (blind in v2).
- ε(R04) = 0.085-0.31 at 1-5 keV (08:34). ε(r_fb) = 0-0.080 over 40 points, zero at 7 points (08:34-36). Barrel cap ≈0.3 (08:23).
- Best point: E 200 GeV, 1.5 keV, FB2, ε = 9/200 = 0.045 (**V** arithmetic), 68% CP [0.030, 0.065] (08:75).
- Finder without PU (V4-3 partial): 0.90-0.97 at 1.5-2 keV, 0.75-0.90 at 1 keV, 0.58-0.84 at 5 keV (08:28-29).
- Full chain vs fast path: ×0.83 at R04, ×0.87 at r_fb; E500 3 keV FB3 0.145 → 0.055 (08:45-47). 31/40 points still on the fast path (08:50).
- Acceptance: f_200 = 0.0476/0.104/0.146/0.169 (E 200/500/1000/1500), 0.1135 (Ẽ500); N_exp(E200) = 1.55-1.58×10⁴ (08:99-103); check: 219.2·0.0476·3000·0.495 = 1.55×10⁴ (**V**). SUP by S2.
- Total ε f·A·ε ≈ 0.005 at E500, about 4× below Knapen et al. (10:22-23; AUD:245) **E**.

**Λ window.** Lower edge without PU 0.61/0.65/0.76/0.71/0.85 keV, at PU 200 1.0-1.2 keV (09:62-64). Upper edge without PU
4.7/5.4/5.9/6.1/6.6 keV, none below 5 keV at PU 200 (09:65-70). The pre-declared comparator (12.8-25 keV) is **not met** (09:65-67).
Truth edges: N_osc = 1 at 0.28-0.33 keV; median ℓ_max = R_IT at 0.43-0.78 keV (09:28-29). SUP in part by S1.

**Background ladder** (3 ab⁻¹; v1 record, kept as "v1 bounds" in v2 Fig. 4; v2 estimates SUP by B1-B4/T1).

| rung | PU central | σ_ln(PU) | B₈₄ SR-T | B₈₄ SR-G | dominant (SR-G) | src |
|---|---|---|---|---|---|---|
| R04 | 1.1×10¹⁰ | 1.94 | 2.6×10⁹ | 7.5×10¹⁰ | pile-up | 07:117 |
| R06 | 3.8×10⁷ | 1.36 | 3.8×10⁶ | 1.5×10⁸ | pile-up | 07:118 |
| R07 | 1.4×10⁵ | 1.53 | 1.4×10⁶ | 2.0×10⁶ | decays in flight | 07:119 |
| R09 | 2.5×10² (b) | 2.22 | 1.2×10⁶ | 1.2×10⁶ | DIF (b) | 07:120 |
| R14 | 2.6×10³ (b) | 5.95 | 3.3×10⁶ | 2.7×10⁶ | DIF (b) | 07:121 |
| R23 | 8.0×10² (b) | 8.12 | 8.7×10⁶ | 6.3×10⁶ | DIF (b) | 07:122 |

- Minimum B₈₄ = 1.23×10⁶ at R09, 7.05 decades above 0.11 (07:102-103; decades **V**: log10(1.23e6/0.11) = 7.05).
- PU measured over 4.9 decades R04 → R07 (07:100-101; **V** 4.90). Budget 0.11 = 0.3/2.71 (06:119-120; **V**).
- Closure: pilot 1.32 (z = +14.3) and 1.42 (+17.6) (07:38-39); production 1.500 (z = +52.8, R04) and 1.606 (+59.4, R05) → ×2.41 (07:44-46).
  Trend −0.36/rung; σ_ln: density 1.15-1.89, trend 2.0-6.3, model spread 4.76 = ln 117 (07:46, 07:53-54; ln117 = 4.76 **V**).
- Thinning reach ≈1.7×10⁻¹⁰/trial **E** against the 2.7×10⁻¹⁰ needed (07:50-51); the 2.7e-10 = 0.11·e^−2.3/4.08×10⁷ (**V**: it is the *median* requirement; per B₈₄ alone it would be 2.7×10⁻⁹).
- N_trig = 4.08×10⁷ ±2% (07:65). SM term 1.9×10⁹ at R04; Z(νν) bound 1.6×10⁴ at R09 (07:73-74).
- Single-interaction rates per triggered event: γ 0.38, V⁰ 0.052, PV pairs 30.3, loopers 0.30, NI 0.10-0.12 ×0.22, DIF 1.59 (07:83-85).
  DIF at R09 1.7×10⁵; PV pairs 1.4×10⁵ (07:89-90).
- Events needed for 0.11: 2.8×10⁹ (PV pairs), 2.2×10⁹ (DIF), 8.4×10⁸ (Z(νν)), ~10⁹ PU trials against 4.8×10⁴ (07:142-144).
- Fallback FB3: 2.0×10⁶ per category, ≈4×10⁶ combined, 7.1 decades (08:11-12). FB2 at E200: median 5.9×10⁵, B₈₄ 8.9×10⁶ (SR-G), 2.6×10⁶ (SR-T) (AUD:261-262).

**Limits** (v1 frozen record; SUP by T1/T2).
- Best μ₉₅/N_exp = 790 (E200, 1.5 keV), μ₉₅ = 1.25×10⁷, N_exp = 1.58×10⁴, S = 710, σ₉₅ = 1.7×10⁵ fb vs 219 fb (08:74-77). All four re-derived (**V**: 791, 711, 1.73×10⁵).
- 95% CP upper ε → ≈420; with the full-chain systematic ≈910-950 **E** (08:78-80). Second best 820; range 2.3×10³-6.0×10⁷ (08:81).
- Even at B = 0 only 20/40 points have S ≥ 3 (08:83-84). Asymptotic/toys = 0.32-1.07 (06:151-153).
- Earlier versions omitted f_200: 37.6 → 790 (00_changelog:9-10; AUD:208); 37.6/0.0476 = 790 (**V**).
- Break-even B for exclusion at E200: 8.3×10² (σ_ln = 1) **E** (10:24; AUD:256).

**Reach** (all **E**). B = 0: ≈1 TeV at 3 ab⁻¹; 5-event ≈0.6 TeV at 300 fb⁻¹ (10:20-21). AUD gives 560-590 (5 events) and 630-665 GeV (3 events) (AUD:241-242).
Plan/book table (PLAN:121-124 = book ch29:197-201, transcriptions agree, **U** as physics): 1026 (B=0), 866 (B=10), 717 (B=100), endcap g=1 1062 at B=10.
Endcap gain ×3.2 = 1/0.31 at g=1 (book ch29:107; **V** arithmetic); the low end ×1.5 is from PLAN:379 only (**E**, no derivation seen). SUP by the v2 reach curve (Fig. 7).

**Thickness law** (truth level; stays unless the P1 tests change it).
- ε_B = 2.254×10⁻⁴ at 3.8112 T, 1 keV (03:16). c = 0.104 predicted vs 0.105 ± 0.002 numerics (03:166, 03:194) [W1: different samples; same-event +2.4%, UNRESOLVED.md:52].
- B exponent 0.914 vs 0.911 ± 0.003 (03:195). R(f) = 1.072/1.144/1.311/1.455 vs 1.073/1.147/1.320/1.460 (03:196). K_vac 0.0794 vs 0.0791 (03:198) [W1].
- Model ΔsB medians 33.5/31.1/29.5 µm (03:145-146); measured E500 1 keV 29.5 ± 1.6 µm (04:97).
- Paired ratios 0.990-1.002 (E ≥ 500), "0.966-0.990" at 200 GeV [W1: low end 0.975 at 0.6-5 keV], scalar 0.947-0.986 (04:35-36).
- Population c excess +0.7/+2.0/+1.1/+2.1/+3.2% against the 1.5% gate (failed); pooled +1.71 ± 0.29% (04:43-45).
- 3-5 keV excess +6.2 ± 0.5% (population), up to +57 ± 11% (κ_B ≥ 10); B*-off +1.8 ± 0.7 vs +9.7 ± 1.3% (04:57-60).
- Straight-string/NG ratio at γ* = 2: 0.50 predicted, 0.75 ± 0.08 measured, ≈3σ fail (03:244-245).
- MS floor 10-28 µm; Λ_cross = 1.91/1.50/1.25/1.16 keV (E), 1.59 keV (Ẽ) (04:110-116). B+MS sub-quadrature 0.80-0.97 at 1-3 keV (04:121).
- Twist factor g ≈ 0.23 (model 0.219-0.225) **E** (D:385-391). Out-of-plane resolution 23-30 µm (12:42).
- Mass proxy (SUP only if S5 runs): M_est median 2.26 m_Q at PU 200, 19% below 0.5 m_Q (09:98-99). sep_IT is flat at 18-26 mm at PU 200 (09:73-74).

## 3. Novelty claims N1-N8 (AUD:337-346)

| # | claim | evidence (v1) | must be distinguished from | protecting plan item |
|---|---|---|---|---|
| N1 | first quirk ribbons through a full hit-level chain (ACTS/Fatras, digitisation, merging, CKF), public Phase-2-like geometry, PU 200 | 05; AUD:339 | Knapen (simplified ATLAS ID, PU 50), Li (helix-layer intersections, PU 50), Sha/Condren (µ=1); unpublished ATLAS ITk repo (AUD:145-152) | C1 (Linux reproduction), B6 (robustness), C2 (finder check), public release |
| N2 | detector-level PU fake rate along a ladder; ρ=2 thinning with pre-registered closure | 07:9-55 | Knapen's factorised extrapolation (AUD:56-57) | B2 (repair + independent occupancy estimator). The plan's asset table (PLAN:147-187) **omits N2**: in v1 it failed closure |
| N3 | single-interaction topologies + 12 SM processes as plane backgrounds | 07:76-91 | Knapen (beam-pipe conversions only), Li (Z(νν)+jets) | B1, B3, B4; W1 fix of the Knapen attribution (07:79) |
| N4 | quantified simulation-statistics barrier (10⁸-2.8×10⁹ events/process) | 07:141-146; 12:21-24 | textbook 1/N zero-count scaling | kept short in §6 (PLAN:170-173); T1 Gamma constraints |
| N5 | pre-registered WP rule + fallback | 06:160-168 | — (methodological, not physics: AUD:364) | §5 pre-registration (PLAN:396-409) |
| N6 | detector-level Λ window at PU 200 (lower edge moves 0.6-0.85 → 1.0-1.2 keV) | 09:57-76 | window existence is Knapen's (Table I) | S1 (×10 rows, full chain) |
| N7 | timing category SR-T + ToF pair-mass proxy (qualitative) | 06:69-74; 09:90-111 | Knapen App. A (proposal), Feng et al. (forward timing) | present as a proxy (PLAN:176); S5 optional |
| N8 | negative detector-level results: sep_IT not measurable; P1 thickness unresolvable (resolution ≈ MS floor) | 09:71-75; 12:42 | Li/Knapen truth-level arguments | keep (PLAN:180); Q20 |

AUD:362-365 recommends claiming only N1, N3 and N4, each with "to our knowledge". P1 novelty (the analytic log and the
B ln(1/B) law, the constants) rests on the Stage-1 audit (`analytic/NOVELTY_AUDIT.md`, not in my scope). The prior art is
Li et al. (numerical rotation) and Knapen (B/Λ² scaling) (01:50-56; 03:108-115).

## 4. ISSUES.md (12 items)

| # | issue | status | resolved by |
|---|---|---|---|
| 1 | HANDOVER labels σ_norm "N_IC=1"; the values are N_IC=2 | open (outside paper) | S2 (new σ table) / C3 |
| 2 | arXiv:0805.4642 is Kang-Luty, not "KLN" | resolved in note | W1 bib check |
| 3 | Stage-3 figures (p1_dsB_c, p2_observables) not restyled | open | required Fig. 2 remake (P1) |
| 4 | truth figures carry the label "PU 200, 3 ab⁻¹" | accepted, captions explain | W1/figures: use the truth label |
| 5 | LHCb INSPIRE metadata wrong | fixed in bib | W1 |
| 6 | N_osc formula without derivation | partly resolved by App. D (D:370-375); 02:21-22 still says "project estimate" | P1/C3 |
| 7 | D12/D13 label clash | note uses D13 | W1: remove the D13 label (12:47, C:31) |
| 8 | open P2 flags: A2FC E500 drop (closed, ×0.87), M_est bimodality (D8), PU fake along the MET direction (D11) | partly closed | S1 (full chain everywhere); B5 (flatness in angle to MET); N7 wording |
| 9 | "(see D9)" inside T4 | resolved (R2) | — |
| 10 | p2_observables crop overlaps | open | sep_IT figure remake (not one of the 7) |
| 11 | "CKF hit stealing" stated as fact | reworded (08:46) | S1/C2 |
| 12 | MET resolution, trigger turn-on, PV-ID not propagated | open (08:128-129) | B6, T1; the trigger has no owner in the plan (see §8, O3) |

## 5. Internal labels a referee cannot read (occurrences per file; `grep -oE`, see the log)

| label | occurrences | total |
|---|---|---|
| `\rep{...}` | changelog 3, 02 4, 03 10, 04 7, 05 7, 06 5, 07 4, 08 4, 09 2, 10 1, 11 1, 12 2, B 41, D 28 | 119 |
| `\cmd{...}` | B 7 | 7 |
| V4-3/V4-4/V4-5 | 08 3, 12 3, C 3 | 9 |
| C2-C | 12 1, C 1 | 2 |
| C4′ | 12 1, C 1 | 2 |
| D13 | 12 1, C 1 | 2 |
| A2FC | 05 3, 06 1, 08 2, B 1, C 1 | 8 |
| D4-12/15/17, D1 (decision ids) | C 4 | 4 |
| PC-19 | 06 1, B 1, C 1 | 3 |
| G1/G1b/G3 (gate/pilot ids) | 05 5, 06 2, 07 1, 12 1, B 3, C 1 | 13 |
| campaign ids C1a/C1b/C2B/C12FC | 05 3, 07 1, 08 3, B 7 | 14 |
| O-1, U-1…U-5, V2b, V3 | O-1: 04 1, C 1; U-x: 05 1, 07 1, A 1, C 2; V2b/V3: 04 2 | 9 |
| test ids T1/T1w (they clash with plan item T1!) | 07 4 | 4 |
| C′₀/C′_PU sample names | 05 2, 07 2 | 4 |
| "Stage N" references | 00 2, 02 5, 03 4, 04 5, 05 3, 06 2, 08 1, 09 4, 12 1, A 3, B 7, D 1 | 38 |
| WP_RULE / STAGE4_* file names | WP_RULE 9 (05,06,07,A,B), STAGE4 10 (07,08,12,B) | 19 |
| "user decision / (user, date)" | 02 1, 03 1, 04 3, 05 2, 06 1, 07 2, 09 1, 12 1, C 9 | 21 |
| LOG.md | 04 1, B 1 | 2 |

The figure file names (D1…D11, T1…T4, S3_*) are not printed and are harmless. FIGURE_MANIFEST says the in-figure ids were
removed in R2. Recommendation for C3/W1: replace "user decision" with the physics reason. The plan's W1 list (PLAN:239-240)
names only 6 of these ~19 label families.

## 6. The 7 required figures (PLAN:228-234)

| # | figure | v0.4 candidate | verdict | data for v2 |
|---|---|---|---|---|
| 1 | event display, PU 200, "best of its sample" | D11 (07:150-157): E200 at 0.45 keV (outside the window) + best PU fake | **remake** | v2 signal + PU sample at a point inside the window; labelled "best of sample". Choosing the "best" needs passing signal events, so it must wait for unblinding (O6) |
| 2 | thickness law + MS floor + crossover | S3_p1_dsB_c.png (non-JFC, 04:71) + T1_u2 ×4 (04:127-130) | **remake from existing data** | Stage-3 `sim/stage3/results/P1.json`; add the floor-test/B*-off points (P1) |
| 3 | efficiency map (m_Q, Λ) with the Λ window | D1_eps_map_rfb (08:55) | **remake** | v2 S1 (×10 rows, full chain), v2 selection; blind until the closure verdicts |
| 4 | ladder: v1 bounds vs v2 estimates, against the budget | D3_bsum_vs_rung (07:129) is v1 only | **remake** (the v1 layer is reusable) | v1 `C12FC_v1` / STAGE4_SUMMARY.json + v2 B1-B4/T1 estimates with bands |
| 5 | closure plots for each estimator | only the lower panel of D4 (thinning ratio R04-R07) (07:130) | **new** | B1 (factorised vs full PU at R05-R07), B2 (both estimators vs direct R04-R07), B3, B5 |
| 6 | expected limit vs mass + existing bounds | D6 (08:111), D7 map (10:33) | **remake** | v2 pyhf workspace; FASER HEPData, D0, Farina-Low from `stage5/EXTERNAL_BOUNDS.md` |
| 7 | reach vs assumed B, v2 estimate marked | none in v0.4 (book Table 29.2/Fig. 29 only) | **new** | book ch29 reach method (s₉₅ values ch29:187) redone in pyhf + v2 B estimate |

## 7. The 25 referee questions (PLAN:460-488): where v0.4 answers them

| # | topic | v0.4 location | answered? |
|---|---|---|---|
| 1 | zero-count bounds: what does the limit mean | 07:141-148, 08:15-18, 10:14-29, 12:21-24 | admitted, not fixed |
| 2 | Fatras without hadronic physics | 05:36-37, 07:81-82, 12:32 | stated |
| 3 | thinning closure failed | 07:35-55 | stated, patched |
| 4 | untested factorisation | 07:30-32, 07:47-49, 12:25-28 | stated |
| 5 | multijets, Z(ττ), lost-lepton Z | 07:71-72, 12:31 | not included |
| 6 | eight SM proxies | 07:63-64, 07:70-71, 12:29 | stated |
| 7 | top-up ×2.3-7.3 | 05:39-46, 07:53 | density systematic only |
| 8 | cylinders, Gaussian smearing | 05:20-24, 05:49-51, C:23-24 | stated |
| 9 | finder correct/optimal | 08:25-31; 12:37 (V4-5 not run) | **not answered** |
| 10 | 9 events; fast path | 08:41-51, 08:75, 12:34-37 | stated |
| 11 | why barrel only | 06:63-65, 12:41 ("user decision") | **not answered with a reason**; v2: scaled endcap estimate (S3 dropped) |
| 12 | rule changes after the result | 06:160-168 | answered (v1) |
| 13 | summed 68% bounds over-cover; uncorrelated categories | 08:130-132 (uncorrelated admitted) | over-coverage **not answered** |
| 14 | why 0.11 | 06:118-121 (algebra only) | **not justified** |
| 15 | cosmics, halo | 07:93-95 | argued |
| 16 | Phase-2 trigger | 06:14-16, 08:128-129 | parametrised, not propagated |
| 17 | K-factors, f_200 | 02:45-52, 02:80-83, 08:122-124 | transcribed, not propagated |
| 18 | classical NG, J = 0, no IC radiation | 03:229-232, C:12 | partly (no IC-radiation regime) |
| 19 | law validity, failed gate | 03:209-217, 04:40-55, 12:9-14 | answered, window overstated (W1) |
| 20 | law not testable at detector level | 04:159-161, 12:42 | answered (N8) |
| 21 | m_Q, Λ measurement | 09 (verdict 09:108-111) | answered (negative) |
| 22 | Knapen/Li comparison | 01:26-38, 10:18-29 | answered |
| 23 | data-driven estimate | 13:32-34 (proposal), 11 | proposal only |
| 24 | reproduce/recast | App. B (internal paths) | **not answered** for an outsider |
| 25 | CMS result? AI? | note.tex:16-20 (not CMS) | AI **not disclosed** |

## 8. Contradictions and open questions for the strategy

1. **The "decisive item" is misnamed.** The abstract and conclusions call a data-driven *pile-up* estimate decisive
   (00:33-34, 13:32-34, 13:41). From R07 on, however, the leading terms are single-interaction and SM bounds that do not
   scale with pile-up (07:102-103; AUD:283-290). v2 must say that B1/B3 matter at least as much as B2/B5.
2. **The plan predates the user decisions.** It still carries S3 (structure item 5 PLAN:213, asset table PLAN:164,
   compute PLAN:427, timeline, decision point 4), cloud (PLAN:47-49, :298, :308, :412-436) and the laptop/external drive
   (C1 PLAN:265). These must be read as: barrel only, lab cluster, cajuela storage (the 0.4 TB for B2).
3. **The trigger has no owner.** Q16 points to S2 (PLAN:479), but S2 (PLAN:374-376) has no trigger task. The same holds
   for the MET and PV-ID variations (ISSUES #12).
4. **Limit object.** v1 limits the yield, so the normalisation uncertainties "do not enter" (06:155-158). The plan wants
   f_200 propagated into the limits (S2). Decide: a σ limit in pyhf, with σ_norm and f_200 nuisances.
5. **f_200 has several values.** E200: 0.048 (02:69), 0.0476 (08:99, 06:21), 0.0485 (AUD:193, xsec.json); Ẽ500: 0.114
   (06:22), 0.1135 (08:103), 0.1119 (AUD:195, ad hoc). The |η_pair|<4 clause is printed in the definition (02:59, 06:20,
   A:50); the script does not apply it (UNRESOLVED.md:56), yet the Stage-3 tail sample has `eta_max 4.0` (AUD:187). The
   numerator and denominator may therefore differ. S2 must recompute f_200 with the same cut as the sample.
6. **PV efficiency.** 93% (05:85) against ε_PV = 1 "not modelled" (06:31, 08:93); this is a W1 item.
7. **Novelty wording.** AUD:362-365 says: claim only N1/N3/N4, and N5 is not physics. v0.4 keeps "What is new" and "the
   first to quantify" (01:50, 01:60-63). The plan's asset table promotes N5-N8 and omits N2.
8. **Reach numbers differ.** At 300 fb⁻¹ the plan gives 665/586 GeV (PLAN:182-183), the audit 630-665/560-590 (AUD:241-242)
   and the paper "≈0.6 TeV" (10:20). Fix one method (pyhf) and quote one number.
9. **Barrel fraction.** "0.19-0.28 without PU" (12:41, axis η) against 0.31 (69% outside, |η_pair|<2.5, PLAN:377) and
   the "≈0.3 cap" (08:23). The definitions differ; the endcap-gain estimate depends on which one is used.
10. **Λ range.** 0.1-100 keV (abstract, intro), 0.5-10 keV (13:3), 0.45-5 keV (detector grid). The v2 paper must state
    one search range and the regime where the classical assumptions hold (Q18; 03:229-232 gives Λ ≲ 10-26 keV).
11. **"Conservative" limits.** 08:16-18 calls them "conservative with respect to simulation statistics" but also says they
    "can bias either direction" (12:23-24). v2 should drop "conservative".
12. **The W1 list is incomplete.** UNRESOLVED.md:48-58 has further paper errors that PLAN:241-251 omits: the window
    "safe" (04:48-49), "1-3 keV" for 9/30 cells (04:76), 04:115 overstated, 03:139/195/250. C3 should use the full list.
13. **Label clash.** v1 closure tests "T1/T1w" (07:37) collide with plan item T1 (likelihood); rename them in v2.
14. **Statistics.** Asymptotic and toys disagree by 0.32-1.07 where both categories carry signal (06:151-153), and the pyhf
    cross-check was never made on the final code (06:154). T1 must validate asymptotics with toys at small B.

**Open questions (O-) for the strategy.**
- O1: Does §9 (m_Q, Λ handles) survive as its own section? The plan has no slot; Q21 only asks for the negative result.
- O2: Is the v1 "fallback" deliverable kept anywhere besides the appendix? T2 replaces it.
- O3: Who owns the trigger turn-on, MET and PV-ID systematics (B6 or S2)?
- O4: Does B6's top-up variation count as a "pile-up scan"? I read it as no: it is a density systematic at fixed PU 200. Confirm.
- O5: Should the v2 grid extend to Λ > 5 keV, where v1 had no upper edge at PU 200 (09:69-70)? That would need S4.
- O6: Blinding for Figs. 1 and 3: a "best-of-sample" signal display uses signal selection; schedule it after the closure verdicts.
