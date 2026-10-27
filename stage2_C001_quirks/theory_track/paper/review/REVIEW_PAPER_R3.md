# REVIEW_PAPER_R3: critical review of `paper/quirks_p1p2_note.pdf` (v0.3, 35 pp)

Reviewer: fresh critical reviewer (JFC loop, round 3), 2026-10-16. Nothing edited except this file.

**Inputs read:**
- the note: all `sections/*.tex`, `quirks_p1p2_note.tex`, `references.bib`, `FIGURE_MANIFEST.md`, `P2_NOVELTY_AUDIT.md`;
- the review history: `REVIEW_PAPER_R2.md` and `FIX_PAPER_R2.md` (with its addendum);
- the numbers: `data/acts_stage4/analysis/STAGE4_SUMMARY.json` (v2, 14:33, R3-NORM);
- the primary sources: arXiv:1708.02243v2 (Knapen et al.) and arXiv:1911.02223 (Li et al.), full text fetched from arXiv
  and read with pdftotext.

**Build state:**
- The PDF (14:48:02) is newer than every `.tex` file (latest 14:47:46).
- 35 pages.
- The log has 0 overfull boxes and 0 undefined references.
- All 10 figure pages (pp. 7, 12, 13, 21–24, 26–28) were rendered at 110 dpi (print size) and inspected.

## Verdict: **ITERATE** (1 A, 0 B, 7 C)

**What is resolved:**
- The normalisation change is applied consistently across the abstract, body, tables, figures and conclusions.
- The headline 790 can be reproduced from the note's own equations.
- No stale numbers remain.
- Every R2 A, B and C item is resolved.

**What blocks:** one item. The new prior-work text (A-3 fix) states in two places that the two reference studies did not
consider background classes that they did consider. One of those statements contradicts the note's own introduction.
The fix is text only (two clauses).

---

## 1. R2 findings: status (verified)

| R2 item | status | evidence |
|---|---|---|
| A-1 stale C′ rates | **resolved** | 07 l.83–85: 0.38/0.052/30.3/0.30/0.10–0.12/1.59 = JSON `cprime.*.rate_t` 0.3786/0.0524/30.31/0.3017/0.098–0.124/1.5945. |
| A-2 one N_exp/σ definition | **resolved** | See §1.1 below. |
| A-3 prior work | **partly resolved; new A-1** | The ⟨µ⟩ = 50, 73 %, ≈ 2 %, 650 GeV/300 fb⁻¹ (Knapen) and 450 GeV/100 fb⁻¹, N_IC = 3, Z(νν)+jets with ⟨µ⟩ = 50 (Li) claims are correct (§1.2). Two sentences about which backgrounds they considered are wrong (A-1). |
| B-1 SM samples / 8 proxies | resolved | 07 l.59, l.63, l.70; 12 item 6. |
| B-2 (ii)–(iii) + staleness | resolved | 13 l.39–41. |
| B-3 "conservative" qualified | resolved | 08 l.16–18; 12 item 4; 08 (iv): "23 of the 33". JSON recount: 23 points with 0 < ε_SRT < ε. |
| B-4 figures | resolved | All 11 D-figure copies are byte-identical to `stage5/figures/final/` (sha256[:12] match FIGURE_MANIFEST, including the R3-NORM D5 9a499b25a2dc, D6 9f2592a43ce4 and D7 b3098f9cc677). No internal IDs are visible. The D7 tag is clean, and its bound list is in the caption. |
| B-5 reach meaning | resolved | 07 l.50–52. |
| B-6 no "first pile-up study" in the abstract or §13 | resolved | — |
| C-1 … C-10 | resolved | C-1 is partial by design: the abstract gives 790 without the ε uncertainty, which is acceptable. K_SM, the Fig. 7 caption ("eight cells"), "Ẽ 500: 2 keV only", "typically 30–70 % (range 0–100 %)", the Evans–Luty name, V4-4 and the p(R08\|R02) chain were all checked in the PDF. |

### 1.1 Headline recomputed from the note alone (A-2 check)

The definitions are:
- Eq. (11): N_exp = σ_norm f₂₀₀ L A.
- §6.5 and §8.3: σ₉₅ = μ₉₅/(L f₂₀₀ A), so σ₉₅/σ_norm = μ₉₅/N_exp.

The note prints σ_norm = 219.2 fb (Tab. 2), f₂₀₀ = 0.0476 and A = 0.49–0.50 (Tab. 9), L = 3000 fb⁻¹, and μ₉₅ = 1.25×10⁷
(§8.3). From these:
- **N_exp** = 219.2 × 0.0476 × 3000 × 0.5035 = 1.576×10⁴. The note prints 1.58×10⁴.
- **μ₉₅/N_exp** = 1.25×10⁷/1.58×10⁴ = **791**. The note prints 790; the JSON has 789.74.
- **S** = 1.58×10⁴ × 9/200 = 711. The note prints 710.
- **σ₉₅** = 1.25×10⁷/(3000 × 0.0476 × 0.5035) = 1.74×10⁵ fb. The note prints 1.7×10⁵ fb; the JSON has 173 114.
- **CP95 edge:** 790 × 0.045/0.084 = 423. The note prints ≈ 420.
- **ε needed for an exclusion:** 790 × 0.045 = 35.6. The note prints ≈ 36.
- **Full-chain systematic:** 790/0.87 = 908. The note prints ≈ 910–950.
- **Erratum factor:** 1/f₂₀₀ = 5.9–21. The note prints 6–21. Also 37.6 × 21.0 = 790.

The notation is consistent:
- one ℰ_sel, one N_exp, one σ_norm;
- σ_th is defined once as the figure label (§6.5, App. A, Fig. 12 caption);
- FB_k, r_fb, k_adm, e_adm and ℰ_status are defined (06 l.136–139, l.34).

**Physics check of μ₉₅ vs N_exp.** The yield limit μ₉₅ is correctly unchanged by the fix. Only N_exp scales with f₂₀₀,
which matches the JSON `normalisation.erratum`.

### 1.2 Prior-work claims checked against the papers

**Knapen et al., 1708.02243v2:**
- "on average 50 pile-up vertices" (abstract): ✓
- pile-up modelled by overlaying Pythia 8 minimum-bias events through a simplified detector (§III.D): ✓
- an 8-layer ATLAS-like barrel: ✓
- "as high as ∼73 %" (§IV): ✓
- total efficiency: Tab. I, DY 800 GeV, gives 0.10 × 0.28 × 0.74 = 2.1 %, so "about 2 %" ✓
- "assuming negligible irreducible backgrounds", discovery = 5 events, 300 fb⁻¹, EW quirks up to 650 GeV, benchmark
  (1,1)₁ (abstract and p. 8): ✓

**Li, Li, Pei and Zhang, 1911.02223:**
- "Z(→νν)+jets process overlaid by pileup events is the dominant background" (abstract): ✓
- ⟨µ⟩ = 50 (p. 10): ✓
- N_IC = 3 (Eq. 1 ff.): ✓
- 450 (150) GeV colour-neutral fermion (scalar) at ∼100 fb⁻¹: ✓
- Knapen's selection applied to Z(νν)+jets+PU leaves ∼10⁻² fb, which they call "overoptimistic" (p. 10, App. A):
  the note's "non-negligible" is fair.

---

## 2. Independent review of v0.3

### 2.1 Numbers vs `STAGE4_SUMMARY.json` (31 spot-checks, all match)

**Outcome (§8.1):**
- 790 (789.74) at A2|F|200|1.5;
- r_fb = FB2&h>5&o>5;
- ε = 9/200;
- CP68 [0.0304, 0.0649];
- CP95 [0.0208, 0.0837];
- μ₉₅ 1.2458×10⁷;
- toy ±1σ band [8.60×10⁵, 1.85×10⁸];
- asymptotic/toys 1.049;
- ε_SRT = 0 at the headline point.

**Ratios, yields and counts (§8.3):**
- second best 820 (E200, 2 keV);
- range 2.3×10³ (2295) to 6.0×10⁷ (5.99×10⁷);
- best per mass 1.3×10⁴ / 3.8×10⁵ / 3.8×10⁶ / 2.8×10⁵, all at 3 keV;
- 33 points with a limit and 7 with ε = 0, the 7 points listed correctly;
- S ≥ 3 at 20/40 points;
- E1500 S_max = 0.295;
- μ_5σ/N_exp from 1.9×10⁴ (2.94×10⁸/1.545×10⁴) to 2.4×10⁸ (1.03×10⁹/4.235).

**Table 9:**
- N_exp 1.545–1.578×10⁴, 1081–1093, 55.0–55.9, 4.21–4.24, 85.0–86.2;
- A 0.493–0.504, 0.565–0.572, 0.639–0.649, 0.580–0.584, 0.545–0.553;
- f₂₀₀ 0.0476 / 0.1042 / 0.1459 / 0.1688 / 0.1135.

**Efficiency (§8.2 and the Fig. 7 left map):**
- ε max 0.080 at E500 2 and 5 keV and Ẽ500 5 keV;
- SR-T share ≤ 27 % at 200 GeV (0.015/0.055);
- all 26 map cell values for E200 and E500 checked.

**Fig. 12 (D7):** all 30 cell values match `mu95_over_Nexp` (for example 7.9×10², 8.2×10², 1.3×10⁴, 3.8×10⁵, 3.8×10⁶ and
6.0×10⁷).

**Table 8:**
- B₈₄ SR-T 2.6×10⁹ / 3.8×10⁶ / 1.4×10⁶ / 1.2×10⁶ / 3.3×10⁶ / 8.7×10⁶;
- B₈₄ SR-G 7.5×10¹⁰ / 1.5×10⁸ / 2.0×10⁶ / 1.2×10⁶ / 2.7×10⁶ / 6.3×10⁶;
- the dominant terms;
- minimum 1.232×10⁶ at R09, 7.05 decades;
- FB3 B₈₄ 2.03 / 1.98×10⁶.

**§7:**
- N_trig 4.08×10⁷ ± 2.0 %;
- C′ DIF 1.69×10⁵, PV pair 1.41×10⁵ and Z(νν) 1.61×10⁴ at R09;
- SR-T window [5.955, 24.035] ns.

**§10:**
- headline SR-G B_median 5.9×10⁵, quoted as "∼ 6×10⁵";
- the B ≈ 8×10² break-even. For log-normal σ_ln = 1, an exclusion needs s > B(1 − e^{−1.64}) = 0.81 B. With S = 710 this
  gives B < 880 ✓.
- the zero-B reach of 1.03 TeV (3 events at 3 ab⁻¹) and 0.59 TeV (5 events at 300 fb⁻¹), log-linear in the JSON S;
- f₂₀₀ A ε(E500, 2 keV) = 0.104 × 0.567 × 0.08 = 0.0047, about 4.4 times below Knapen's 2.1 %.

**Stale-value grep** of `sections/*.tex` for 37.6, 43–45, 43.2, 45.3, 3.3×10⁵, 39.1 and "109": the only hit is the
change-log "37.6 → 790" (intended).

### 2.2 Consistency of abstract ↔ body ↔ conclusions

The following are stated identically in the abstract, §1, §8, §10 and §13:
- 790 at E200, 1.5 keV;
- nothing excluded;
- no WP, with 1.2×10⁶ and 7 decades;
- the f₂₀₀ erratum clause;
- ≈ 910–950 (§8.3 and §13);
- the m_Q/Λ verdict;
- the "background method, not a tension" statement.

The Fig. 8 and Fig. 12 captions say "at least 790" and "every cell above one". This is consistent with the JSON
(min −1σ/N_exp = 54.5 and min −2σ/N_exp = 1.72, so there is no ±1σ or ±2σ contour either).

### 2.3 Honesty

These all hold:
- "No working point" is stated as such.
- The deep-rung B values are labelled as zero-count bounds.
- "Conservative" is qualified.
- Nothing is claimed as excluded.
- The null result is attributed to the background method (§1 and §10).
- The novelty statement is prefixed "to our knowledge".
- The status box says "not a CMS result".
- The labels read "Private work (simulation)" / "√s = 14 TeV, PU 200, 3 ab⁻¹" (+ "truth level").

The single exception is A-1.

### 2.4 Figures

- All D-figures are the corrected copies (hash-identical to Stage 5; D5/D6/D7 carry the R3-NORM legend
  N_exp = σ_norm·f·L·A and an inclusive-σ axis).
- Fig. 8 left: the predicted yield is 1.6×10⁴ and the median is 1.25×10⁷ at 1.5 keV, as in the text.
- Fig. 8 right: σ_th = 219 fb at 200 GeV, and the limit is ≈ 1.7×10⁵ fb.
- The captions match the content.
- In-plot text is small (≈ 5–6 pt) but legible at print size. The rung tick labels of Figs. 5 and 7 (right) are the
  smallest, which is acceptable.

### 2.5 Length and references

- 35 pp, which is within the ≤ 35 pp limit.
- The Knapen and Li bib entries match arXiv (title, authors, PRD 96 115015 and PRD 102 056006).

---

## 3. Findings

### Category A (must fix)

**A-1. The new prior-work text says that Knapen et al. and Li et al. did not consider background classes they did
consider. One instance contradicts the note's own introduction.**

- **Where.**
  - (a) `01_introduction.tex` l.38 (p. 2): "Neither study simulated pile-up 200, hit-level tracking **or single-interaction
    fakes from material**."
  - (b) `10_bounds.tex` l.24–25 (p. 28): the deep-rung bound is "set by single-interaction **and SM terms** that do not
    scale with pile-up **and that neither study considered**."
  - Related: the novelty sentence in `01_introduction.tex` l.56–58 ("the first such study … with single-interaction
    backgrounds from material").
- **Evidence from the primary sources.**
  - Knapen et al. (1708.02243v2, §III.D "Backgrounds") simulate isolated photon conversions in the beam pipe. They
    generate Z(νν)+γ+j with MadGraph, apply the PDG conversion probability, pass the e⁺e⁻ pair through their simplified
    detector, overlay pile-up and run the reconstruction (their Fig. 5, "Converted γ").
    - A beam-pipe conversion is a single-interaction fake from material.
    - The note itself cites exactly this section for the single-interaction idea (`07_backgrounds.tex` l.79,
      `\cite[Sec.~III.D]{Knapen:2017kly}`).
    - `P2_NOVELTY_AUDIT.md` l.166–167 and item N3 say so as well: "Knapen et al. include only beam-pipe conversions".
  - Li et al. (1911.02223, abstract and p. 10) simulate the SM Z(→νν)+jets background with ⟨µ⟩ = 50 and call it the
    dominant background. The note's own intro l.35–37 states this, so statement (b) contradicts the note.
    - In this note's background sum, Z(νν)+jet is the leading SM term (2.5×10⁷ of N_trig = 4.08×10⁷; 1.6×10⁴ at R09).
    - At the headline point the SM class contributes a central value of 3.9×10⁴ against 1.6×10⁵ for C′
      (`fallback_B["FB2&h>5&o>5"].G.central_by_class`).
- **Why A.** The R2 review classed a factual misstatement of the directly relevant prior work as A (R2 A-3). This is the
  same class of error, introduced by its fix, and it supports a novelty claim. Statement (b) also makes the note
  internally inconsistent.
- **Fix (text only, about two lines; keeps 35 pp).**
  - (a) Write: "Neither study simulated pile-up 200 or hit-level tracking, and neither treated single-interaction fakes
    beyond beam-pipe photon conversions (Knapen et al.) and SM backgrounds beyond Z(νν)+jets (Li et al.)."
  - (b) Write: "… set by single-interaction topologies (PV pairs, decays in flight, nuclear interactions, loopers) that
    neither study treated, and by SM terms estimated here at the zero-count level" (or equivalent).
  - The novelty sentence (l.56–58): restrict it to the audit's N3 wording, for example "with the full set of
    single-interaction topologies as backgrounds (beyond the beam-pipe conversions of Knapen et al.)".

### Category B

None.

### Category C (optional)

- **C-1.** The Fig. 12 in-plot tag "no expected exclusion: all cells ≥ 790 (also at −1σ)" can be read as "≥ 790 at −1σ".
  The actual minimum of the −1σ edge is 55 × the prediction (JSON). Consider "(no exclusion also at the −1σ edge)".
  This is a Stage-5 figure, so a caption clause would also do.
- **C-2.** Tab. 2 N₂₀₀ does not equal σ_norm f₂₀₀ L ε_fid of Tab. 9 by −2 to +4 %:
  - E200: 2.71×10⁴ in Tab. 2, against 219.2 × 0.0476 × 3000 × 0.847 = 2.65×10⁴;
  - E1000: 67.3 against 70.2.

  The two |η_pair| < 2.5 fractions come from different samples (Stage-2 inclusive, Stage-3 template half). N₂₀₀ is not
  used in any limit. One clause in the Tab. 2 caption would remove the apparent inconsistency.
- **C-3.** The Fig. 8 right legend says "σ_th (E, N_IC = 2, NLO K, PDF unc.)". The text (Eq. 3) uses K_QCD from
  NNLO_approx+NNLL with a ±5 % nuisance. The legend wording comes from Stage 5. Mention it in the caption or leave it.
- **C-4.** The truth hit-merging comparator is "12.8–25 keV" in §9.2 and "13–25 keV" in the Fig. 10 caption and tag.
  Pick one.
- **C-5.** Intro l.37: "they also showed that the first selection leaves …". Write "that the selection of Knapen et al.
  leaves …"; "first" is ambiguous.
- **C-6.** The definition of f₂₀₀ (App. A, §2.3) omits the |η_pair| < 4 condition of the tail sample
  (JSON `normalisation.f_tail_definition`). §6.1 states it for the samples. Add it once to App. A.
- **C-7.** §10 compares the 0.6 TeV zero-B reach with Knapen's 650 GeV. Knapen's study used a 2 T field, √s = 13 TeV
  conditions and an 8-layer detector. The EST tag covers this, and "close to" is fair.

## 4. Checklist

| check | result |
|---|---|
| R2 A-1 / A-2 / A-3 | resolved / resolved / partly (new A-1) |
| R2 B-1…B-6, C-1…C-10 | resolved |
| 790 recomputed from the note's own equations | 791 (μ₉₅/N_exp), 1.74×10⁵ fb, S = 711. ✓ |
| Stale numbers (37.6, 43, 45, 3.3e5, 39.1, 109) | only the change-log "37.6 → 790" ✓ |
| Numbers vs JSON (≥ 20) | 31 checked, plus 56 map cells; all match |
| Abstract ↔ body ↔ conclusions | consistent ✓ |
| Figures (10 pages at print size) | correct copies, captions match, legible ✓ (C-1, C-3, C-4) |
| Honesty (no WP, nothing excluded, background-method null, hedged novelty) | ✓ except A-1 |
| References | real; Knapen and Li claims verified in the full text |
| Pages ≤ 35 | 35 ✓ |

## Verdict: **ITERATE**

One Category-A item: **A-1**, which misstates the background classes treated by Knapen et al. (beam-pipe conversions)
and by Li et al. (Z(νν)+jets) in intro l.38 and §10 l.24–25, with the related novelty clause. The fix is text only.
After it, the note is PASS-ready: no other A or B items are open.
