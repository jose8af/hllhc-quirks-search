# REVIEW_PAPER_R2: critical review of the complete note `paper/quirks_p1p2_note.pdf` (v0.2, 35 pp)

Reviewer: fresh critical reviewer (JFC loop), 2026-10-16. Nothing edited except this file.

Scope: the whole note. The P2 sections (7–10, 12, 13), the abstract and the conclusions are new and get the most attention.
The Phase-A sections were re-checked only for the R1 fixes. User decisions respected:
- concise note of ≤ 35 pp (it has 35 pp);
- √s = 14 TeV throughout;
- author block left as a placeholder;
- figure labels "Private work (simulation)".

Sources used:
- Stage 4: `acts/stage4/STAGE4_RESULTS.md` (all 846 lines), `data/acts_stage4/analysis/STAGE4_SUMMARY.json`,
  `C12FC_v1/{bsum_wp,background}.json`, `REVIEW_RESULTS_R3.md`, `INV_STATS_BKG.md` (spot), `WP_RULE_PC19.md`,
  `g3/G3_REPORT.md`;
- Stage 5: `stage5/EXTERNAL_BOUNDS.md`, `FIGURES_FINAL.md`;
- `analytic/NOVELTY_AUDIT.md`, `sim/stage3/{README,VALIDATION}.md`, LOG.md.

The PDF is current: it was built at 14:01, after the newest `.tex` file. The log has 0 overfull boxes and 0 undefined
references. Every page with a figure (7, 12, 13, 21, 23–28, 35) was rendered at 110 dpi, which is print size, and
inspected.

## Verdict: **ITERATE** (3 A, 6 B, 10 C)

Most of the note is in good shape:
- The P2 outcome is stated honestly, and every number on the headline chain matches the final run.
- All prior-round findings are resolved except one figure-text item that cannot be fixed from `paper/`.
- The bibliography is real.

Three items block, and each is cheap to fix (text only, no rerun):
- A-1: one block of stale input numbers.
- A-2: an inconsistent definition of the quantities that make up the headline ratio 37.6.
- A-3: a factual misdescription of the published central-detector reach studies, which the P2 result contradicts without
  any discussion.

---

## 1. What was verified (evidence)

### 1.1 Prior round (REVIEW_PAPER_A_R1 → FIX_PAPER_A_R1)

**A-1 is resolved.** The failed V2b gate is now disclosed consistently in:
- the abstract (l.17–19: "+2–3 % … above a pre-set 1.5 % validation gate, which therefore failed … estimate");
- §3.7 (new paragraph "Population-level status of c"), with +1.71 ± 0.29 % and +2.04 %, which match
  `sim/stage3/VALIDATION.md` l.42 and README l.67;
- §4.2 and §4.4;
- §12 item 1;
- §13.

**B items, all checked in the .tex and the PDF:**
- B-1: oscillation scale (intro l.15–17, "≈ 5 m … 5 µm").
- B-2: tilt × lever arm.
- B-3: 4.1/4.5σ and 3.0/3.4/3.9σ (04 l.52–53).
- B-4: pyhf claim restricted to the pre-R6 dry run, with asymptotic/toys 0.32–1.07 (06 l.136–141). This matches
  `STAGE4_SUMMARY.json → outcome.asym_over_toys_range` [0.3196, 1.0705].
- B-5: logged changes (06 §6.6).
- B-6: 13.9 % (05 l.78).
- B-7: 2.3–5.2 %.
- B-8: κ, K_QCD and 𝓡(f) introduced; App. A updated.
- B-10: below Λ_cross(m_Q), tagged EST.
- B-11: the `.bst` now prints the collaboration, the report number and the eprint (rendered refs [7], [11], [12], [15],
  [25]).
- B-12: "Li et al.".
- B-13: FASER wording.
- B-14: step-convergence statement.
- B-15: MIP unit.

**B-9 is resolved except one item.** Fig. 5 was replaced. The "(see D9)" text inside the T4 plot is still there (p. 25,
Fig. 8 right) and is logged in ISSUES.md item 9 as not editable from `paper/`. This is acceptable.

**C items:** C-1 to C-9 and C-11 were applied. C-10 was not changed (user-approved label).

### 1.2 Numbers checked against the sources (P2 ≈ 70, P1/abstract ≈ 10; all match except A-1)

**Ladder and backgrounds** (Tab. 8 and §7 vs STAGE4_RESULTS §1.2–1.3 and §3 and `STAGE4_SUMMARY.json → closure, ladder,
n_trig`):
- PU central 1.1e10 / 3.8e7 / 1.4e5 / 2.5e2 / 2.6e3 / 8.0e2;
- σ_ln 1.94 / 1.36 / 1.53 / 2.22 / 5.95 / 8.12;
- B₈₄ T/G at R04, R06, R07, R09, R14 and R23 (all 12 cells);
- dominant terms;
- min 1.23e6 at R09, 7.05 decades;
- FB3 2.0e6 per category, ≈ 4e6 combined, 7.1 decades;
- SR-T PU ×(0.6–3)×10⁴ smaller;
- 4.9 decades from R04 to R07.

**Closure and the pile-up reach:**
- G3: 127/130 jobs, 1.32 (z +14.3) and 1.42 (z +17.6) (G3_REPORT l.40–41).
- Production: B1 48 000 / B2 6 000 trials; T1 1.500 (z +52.8) at R04; T1w 1.606 (z +59.4) at R05 (lever arm fails at
  R06); compounded ×2.41; trend −0.36 per rung; c = 1.196.
- Reach: R06 at ρ = 2 and R07 for B1; thinning reach 1.7e-10 against 2.7e-10.
- σ_ln components: density 1.15–1.89, trend 2.0–6.3, model 4.76.

**SM normalisation** (`bsum_wp.json → n_trig.breakdown`):
- N_trig = 4.08e7 ± 2.0 %;
- Z(νν) 2.51e7;
- W(τ) 2.26e6 + 5.41e6 = 7.7e6;
- W(eν) + W(μν) 4.8e6;
- tt̄1ℓ 2.38e6;
- 1–3e5 for the rest;
- K 1.4 ± 30 %, K_tt̄ 1.9, veto 5 %;
- proxy fraction 15–45 % (`sm_proxy_fraction_of_B_SM`: 0.147–0.445);
- SM term 1.9e9 at R04;
- Z(νν) 0/81 HS candidates, giving 1.6e4 at R09.

**Single-interaction (C′) terms and statistics:**
- f_pre 0.949, 81/500, 1.14/81, c = 1.196, giving 1.7e5 (recomputed: 1.6868e5, the same as the JSON 168 683.86);
- PV pair 1.4e5;
- events needed 2.8e9 / 2.2e9 / 8.4e8, and ≈ 1e9 PU trials, median ≲ 0.02;
- 10⁸–3×10⁹ per sample.

**Efficiency:**
- V4-3 table: 0.90–0.97, 0.75–0.90, 0.83–0.97, 0.58–0.84, and 0.64–0.77 with R04;
- ε(R04) 0.085–0.31;
- ε(r_fb) 0–0.080, with the maximum at E500 2 and 5 keV and Ẽ500 5 keV;
- the 7 zero points;
- 180–200 events per point.

**A2FC:**
- 9-point set;
- R04 5–30 % lower;
- ×0.83 (84/20, p 1.6e-10) and ×0.87 at r_fb (recomputed in REVIEW_RESULTS_R3);
- E500 3 keV 0.145 → 0.055 (11/200, CP [0.039, 0.076]);
- 25–50 % noise flips;
- global p 1e-4–1e-3.

**Limits** (`STAGE4_SUMMARY.json → outcome, fallback_points`):
- 37.62 at E200 1.5 keV, FB2, 9/200;
- CP68 [0.030, 0.065], CP95 [0.021, 0.084];
- μ₉₅ 1.25e7, ±1σ [8.6e5, 1.9e8], asym/toys 1.05;
- ≈ 20 at the CP95 edge (37.6 × 0.045/0.084 = 20.1);
- ε ≈ 1.7 for an exclusion (37.6 × 0.045);
- 43.2 / 45.3;
- 39.1; 109; 1.0e7;
- 33/40 points with a limit, 7 with ε = 0;
- 1.7 events at E1500;
- discovery 2.2e8–1.0e9;
- −2σ toy edge below N_exp exactly at E200 0.45–1.5 keV (lo2/N_exp = 0.17 / 0.17 / 0.08 / 0.11 / 0.16; at 2 keV it
  is 2.5);
- the Fig. 11 tag claim "≥ 37.6 also at the −1σ edge" holds (min lo1/N_exp = 2.6).

**Table 9:** all 25 cells match STAGE4_RESULTS §4.4.

**Mass and Λ handles** (§6.1–6.3):
- edges 0.61/0.65/0.76/0.71/0.85, 1.0–1.2, and 4.7/5.4/5.9/6.1/6.6;
- ×2.7–3.5;
- E500 2 keV 6.9 vs 7.0 mm;
- 20–45 mm; 18–26 mm; 23 → 0.6 mm;
- 0/9551, 1.69, 2.46, 2.26, N = 850;
- 29 % and 19 %; 6–41 %;
- 483 / 1113 / 2070 / 3137; q16 155–332;
- β_ToF 0.23–0.53 → 0.39–0.68;
- dE/dx 1.8–7.1 → 1.5–2.7;
- w_core 13.1 / 5.5 / 2.4 / 1.3, and 10–12 mm.

**PC-19:**
- [5.955, 24.035] ns;
- σ_t,PV 190 ps (150/230);
- 10⁻⁴ per edge.

**External bounds** (`EXTERNAL_BOUNDS.md`):
- FASER 179 GeV near 10 keV, 57/66 GeV at the ends, ≤ 172 GeV within 0.45–5 keV;
- FL Table II 650/150 and 350/60 GeV;
- D0 107 GeV, a probable match;
- two FL/FASER discrepancies;
- "all ≲ 180 GeV, below the lightest grid mass".

**P1 and abstract:**
- +1.71 ± 0.29 %, +2.04 % and +0.70/+2.00/+1.07/+2.10/+3.15 % (VALIDATION l.41–42);
- c = 0.104;
- Λ^{−1.8}B^{0.9} (1 − c = 0.896, −2(1 − c) = −1.79);
- 0.50 vs 0.75 ± 0.08 (3.1σ, stated as "≈ 3σ");
- floor 10–28 µm;
- Λ_cross 1.2–1.9 keV.

### 1.3 Honesty checklist (the outcome as stated)

| item | where | status |
|---|---|---|
| No WP → pre-registered §8 fallback | abstract, §6.5, §8.1, §13 | ✓ |
| Deep-rung B = zero-count simulation bounds; limited by simulation statistics | abstract, §7.6, §8.1, §12 item 4, Fig. 5/7/11 captions | ✓ (but see B-3 on "conservative") |
| Best σ₉₅/σ_th 37.6 at E200 1.5 keV with ε CIs, and the ≈ 43–45 EST systematic not applied | §8.3 (full), §13 (43–45), abstract (37.6 only) | ✓ (C-1) |
| Nothing excluded; existing bounds not extended | abstract, §8.3, §10, §13 | ✓ |
| V4-3 PARTIAL, with a post-hoc match | §8.2, §12, App. C | ✓ |
| Post-hoc comparators labelled | §9.2, Fig. 9 caption | ✓ |
| sep_IT not measurable at PU 200 | abstract, §9.2, §13, App. C | ✓ |
| M_est is a pair-mass proxy (≥ 2 m_Q) | abstract, §9.3, Fig. 10, §13 | ✓ |
| V2b gate failed | abstract, §3.7, §4.2, §4.4, §12, §13 | ✓ |
| Not a CMS result | status box, §11, §13, figure labels | ✓ |
| Comparison with published central-detector *reach* (Knapen et al., Li et al.) | — | **missing / misdescribed (A-3)** |

### 1.4 Bibliography: INSPIRE API spot-check of 12 entries new or changed since R1, all real and correctly identified

Every entry below matches INSPIRE in texkey, title, first authors, journal, volume and year:
- Junk:1999kv (hep-ex/9902006)
- Read:2002hq (doi 10.1088/0954-3899/28/10/313)
- Cowan:2010js (1007.1727)
- Heinrich:2021gyp (doi 10.21105/joss.02823)
- Ai:2021ghi (2106.13593)
- Farina:2017cts (1703.00912)
- CMS:2017kku (1801.00359)
- Feng:2024zgp (2404.13814)
- CMS:2024nhn (2410.09164)
- Li:2023jrt (2311.15486)
- ParticleDataGroup:2024cfk (doi 10.1103/PhysRevD.110.030001)
- Bierlich:2022pfr (2203.11601)

The R1 review had already checked 22 other entries. Rendering nits are in C-6.

---

## 2. Findings

### Category A (must fix before PASS)

**A-1. §7.4: the generator-level single-interaction rates are stale and do not match the final run.**
- **Where.** 07_backgrounds.tex l.84–86 (p. 20): "0.43 (photons), 0.050 (V⁰), 31.1 (PV pairs), 0.22 (loopers), 0.10–0.12 per
  nuclear-interaction radius … and 1.57 (decays in flight)".
- **Evidence.** These are the values of the intermediate fix R2 (LOG.md l.259, 2026-10-14 08:10: "D2 rate_t … gamma 0.43,
  V0 0.050, PV pairs 31.1, loopers 0.22, … DIF 1.57"). The final run, which §7 says it reports (l.7, "numbers are from the
  final run C12FC_v1"), uses `STAGE4_SUMMARY.json → cprime.*.rate_t`:

  | topology | final run | note | deviation |
  |---|---|---|---|
  | γ | 0.379 | 0.43 | −12 % |
  | V⁰ | 0.052 | 0.050 | +4 % |
  | PV pairs | 30.3 | 31.1 | −2.6 % |
  | loopers | 0.302 | 0.22 | +37 % |
  | NI | 0.098 / 0.124 / 0.124 | 0.10–0.12 | ✓ |
  | DIF | 1.59 | 1.57 | +1.6 % |

  STAGE4_RESULTS_C12v1 l.140 gives the same final values (30.3, 1.59, 0.38, 0.30, 0.124, 0.052).
- **Proof that the final run uses the JSON value.** The note's own DIF chain reproduces the JSON central value exactly
  only with 1.5945: 0.94946 × 1.14 × 1.19636/500 × 1.5945 × 4.0848×10⁷ = 1.6868×10⁵, which is the JSON 168 683.86.
- **Why A.** These are body numbers that disagree with the latest machine output by more than 1 %, i.e. stale numbers
  (03-review §6.4 Ph4b, critical_reviewer "numbers that don't match").
- **Fix.** Quote 0.38 / 0.052 / 30.3 / 0.30 / 0.10–0.12 / 1.59 from `STAGE4_SUMMARY.json → cprime`. Add "(max over
  processes)", as in the source. Re-grep the note for 0.43, 31.1, 0.22 and 1.57.

**A-2. The quantities in the headline ratio 37.6 are defined inconsistently.** One symbol stands for two quantities,
and one quantity has two names.
- **Where.**
  - Eq. (11)/`eq:effchain` (06 l.20–22, p. 16) defines ℰ as the full chain ℰ_trig ℰ_presel ℰ_PV ℰ_fid ℰ_finder ℰ_status,
    and N_exp = σ_norm L ℰ.
  - §8.3 l.69–70 and Tab. 9 (p. 23–24) instead define N_exp = σ_norm L A, with A = ℰ_fid ℰ_trig ℰ_presel. Throughout §8,
    ℰ means the selection efficiency alone (0–0.080, with A applied separately). §12 item 7 calls it ℰ_finder and writes
    ℰ_tot = A × ℰ_finder.
  - The predicted cross section is σ_norm in §2, §6 and §8.3, but σ_th in the headline ratio σ₉₅/σ_th (§8.3 l.74, §10,
    Fig. 11). σ_th is never defined.
  - Eq. (11) has ℰ_presel, while Tab. 9 has ℰ_presel|trig.
  - ℰ_status is never defined. In the source it means that a row with status ≠ 1 counts as a failure.
  - FB_k, r_fb, R_A–R_E, S, A, σ₉₅, k_adm, Λ_R, M_est and β_ToF are missing from App. A. FB_k is never defined at all,
    yet "FB2" and "FB3" carry the headline (§8.1, §8.3).
- **Consequence.** A reader who takes N_exp from Eq. (11) gets μ₉₅/N_exp = 1.25×10⁷/(σ_norm L A ℰ) = 1.25×10⁷/1.5×10⁴
  ≈ 830, not 37.6. The completeness test (reproducing the headline from the note alone) fails on notation. 04-output
  makes "one symbol per quantity" a Category-A rule.
- **Fix (text only).**
  - In Eq. (11), write ℰ_tot = A · ℰ_sel with A = ℰ_fid ℰ_trig ℰ_presel|trig ℰ_PV, and S = σ_norm L A ℰ_sel.
  - Define N_exp ≡ σ_norm L A (the predicted yield in the acceptance) and μ₉₅ as the limit on that yield, so that
    σ₉₅/σ_norm = μ₉₅/N_exp.
  - Replace σ_th by σ_norm in the text, or define σ_th ≡ σ_norm once. Fig. 11's colour bar may keep σ_th if it is defined.
  - Define ℰ_status in one clause.
  - In §6.5, add "FB_k denotes the fallback selection with k_adm = k (FB0: no width cut)".
  - Add the missing symbols to App. A.

**A-3. P2 misdescribes the published central-detector reach studies and never confronts its result with them.**
- **Where.**
  - Intro l.31–33 (p. 2): "the published central-detector reach estimates rest on truth-level hit patterns and on assumed,
    not simulated, pile-up rejection".
  - §10 compares only with exclusions.
  - §1 "What is new" presents the P2 set-up alongside the P1 novelty.
- **Evidence (checked in the primary sources).**
  - Knapen, Lou, Papucci and Setford, arXiv:1708.02243.
    - §III "Backgrounds" says: "we assume an average of ⟨µ⟩ = 50 pileup interactions … We model pile-up by randomly
      selecting minimum bias events from a sample of 125×10³ events generated by Pythia8, processed by the simplified
      detector". Converted photons are overlaid with pile-up and passed through their reconstruction.
    - §IV reports a signal efficiency "as high as ∼ 73 %", with the background extrapolated from looser
      one-hit-per-layer planes and the residual argued removable.
    - Abstract: EW quirks "as heavy as … 650 GeV may be discovered" with 300 fb⁻¹.
  - Li et al., arXiv:1911.02223 (abstract, INSPIRE): "the Z(→νν)+jets process overlaid by pileup events is the dominant
    background … color neutral fermion (scalar) quirks with masses up to 450 (150) GeV" at ∼ 100 fb⁻¹.
  - Both studies therefore simulate the pile-up overlay, so the intro sentence is factually wrong.
  - This note finds no sensitivity at 3 ab⁻¹: the best point is 37.6× above the prediction at 200 GeV, and E500 is
    ≥ 1.4×10³×. That is many orders of magnitude from those projections.
  - The note never mentions or discusses that contrast. `analytic/NOVELTY_AUDIT.md` covers only P1, and
    STAGE4_RESULTS l.27 says "plan.md has no novelty audit, so this report makes no 'first' or 'new' claim".
- **Why A.**
  - A false statement about prior work in the final deliverable is a credit/novelty error.
  - A headline result grossly inconsistent with the directly relevant published reference, with no explanation,
    falls under 03-review §6.8 (Tier 1, "investigate and explain") and the 04-output requirement of a quantitative
    comparison to prior results.
- **Fix (text only; keep ≤ 35 pp by condensing §6.6 or the A2FC paragraph of §8.2).**
  1. Correct the intro sentence. For example: "Knapen et al. and Li et al. estimated the reach with simulated pile-up
     overlays (⟨µ⟩ = 50 and LHC Run-2-like conditions) on simplified detectors, finding efficiencies up to ≈ 70 % and
     discovery reach for colour-neutral quirks up to 450–650 GeV with 100–300 fb⁻¹."
  2. Add a short paragraph in §10, "Comparison with published reach projections". It should list the differences that
     can plausibly explain the gap (all EST):
     - PU 200 normalised to the TDR occupancy, against ⟨µ⟩ = 50, with combinatorial fakes growing like ρ^{n_int} (§7.1);
     - the Phase-2 IT geometry and the barrel-only ε ceiling ≈ 0.3, against 73 %;
     - single-interaction topologies (PV pairs, decays in flight), which dominate here from R07 and were not
       considered there;
     - pre-registered zero-count bounds 1.14/M with σ_ln, the ×2.41 closure factor and the trend term, against an
       extrapolation from looser planes with residual events argued away;
     - different benchmarks and luminosities.
  3. State that this note does not show those projections to be wrong. It shows that a pre-registered, simulation-only
     background estimate at PU 200 cannot confirm them.
  4. Remove the P2 sentences from the "What is new" paragraph, or re-label it "What this note does for P2". There is no
     P2 novelty audit.

### Category B (advisory; should be fixed)

**B-1. §7.3: contradictory SM-sample statements and a wrong proxy count.**
- **The contradiction.** 07 l.59–61 says the SM backgrounds are "estimated from Pythia 8 samples of Z(νν)+jet,
  W(ℓν)+jet (ℓ = e, μ, and τ split by decay class) and tt̄". But l.71–72 (correctly) says W(eν) and W(μν) "have no
  hit-level sample". `background.json → sm.Wenu_j.flag` reads "CONSERVATIVE PROXY (no hit-level sample) … max over
  Wtau_l/Wtau_h".
- **The count.** §12 item 6 says "Six SM processes enter through flagged proxies". The source has 8 of 12: W(eν), W(μν),
  tt̄2ℓ, t-channel top, WW, WZ, ZZ and tW (STAGE4_RESULTS §1.3 and caveat 4).
- **Fix.** Write "W(τν)+jet (split by τ decay class)". Write "eight SM processes (… dibosons counted separately)".

**B-2. §13, "Even with (ii)–(iv)", mislabels the source estimate and drops its staleness flag.**
- **The source.** STAGE4_RESULTS §10 item 8 bases the "≈ 0–2 (SR-T) and 4–5 (SR-G) decades" on its items 2 + 3 + 4. In
  the note's numbering those are (ii) deeper pile-up and (iii) C′ conditionals plus time-tag credit.
- **The mislabel.** The note's (iv) is a signal-efficiency item and does not reduce the background.
- **The staleness.** The source also marks the estimate "C12_v1 estimate … stale, not re-derived on C12FC_v1 … ≤ 0.13
  decades".
- **Fix.** Write "Even with (ii) and (iii) … (estimate from the previous run; order of magnitude unchanged)".

**B-3. The limits are called "conservative" without the qualifier that the note itself requires.**
- **The claim.** §8.1 l.16–17 says the limits "are conservative; they would move in proportion to the bounds", and §12
  item 4 says the same.
- **The contradictions in the note itself.**
  - §12 item 5 says the factorised deep-rung background "could be off in either direction by an unknown factor".
  - §8.4 (iv) treats SR-T and SR-G as uncorrelated, although the same SM/C′ terms enter both. Source caveat 19 calls this
    "anti-conservative where both bins carry signal", and that is the case at 23 of the 33 limit points (asym/toys mostly
    0.32–0.72). The note says only that it is irrelevant at the headline point.
- **Fix.** Write "conservative with respect to simulation statistics (the bounds); the untested factorisation can bias
  them either way". In §8.4 (iv), add "anti-conservative where both categories carry signal (not at the headline
  point)".

**B-4. Figure legibility and stale text inside figures.**
- **Legibility.** The P2 composites are 1×2 at a height of 0.37 lw: Figs. 5, 6, 7, 9 and 10. Fig. 11 is at 0.52 lw. At
  print size their legends and in-plot text blocks render at about 3–4 pt (pp. 21, 23, 24, 26, 27, 28). Examples:
  - the Fig. 5 legend and rung labels;
  - the Fig. 6 right legend;
  - the Fig. 11 tag block, which holds the list of external bounds the caption refers to ("listed in the figure").
- **Stale text in Fig. 11.** Its in-plot text says "numpy-A2 ε (31/40 points) carries an unassigned full-chain
  systematic (INV_A2FC_E500 open)". The investigation is closed and the systematic is quantified (×0.87; §8.2 of the
  note). The paper copy is identical to `stage5/figures/final/D7_exclusion_map.pdf` (sha 3747fb811e54), so the stale text
  comes from Stage 5.
- **Internal identifiers inside plots.**
  - Fig. 7: "acceptance.json".
  - Fig. 11: "WP_RULE A.2b".
  - Fig. 12: "B1_00201, trial 28".
  - Fig. 9 right: the axis "sep_IT^det", whereas the text symbol is d_IT.
- **Fix.**
  - Regenerate D7 with the corrected tag. If that is impossible from `paper/`, state the correct status in the caption
    and log it in ISSUES.md.
  - Move the external-bound list into the Fig. 11 caption.
  - Where the page budget allows, raise the most important P2 panels to height ≈ 0.45 lw. Figs. 5 and 11 are the
    priority.

**B-5. §7.2: the reach numbers are given without their meaning.** "The thinning reach is ≈ 1.7×10⁻¹⁰ per trial,
against ≈ 2.7×10⁻¹⁰ that the pile-up term alone would need." Read literally, this says the reach suffices. Yet the next
sentences say that the estimate beyond R06 rests on untested factorisation. Add one clause: "the reach would suffice in
principle, but the deepest rung with ≥ 10 ρ = 2 counts is R06".

**B-6. §1 l.33 and §5: the unaudited P2 framing (part of A-3) also appears in the conclusions' first paragraph.** That
paragraph opens with "We studied …" and is fine. Ensure that nothing in §13 or the abstract implies a first study of
pile-up for this signature.

### Category C (optional)

- **C-1. Abstract.** The abstract quotes 37.6 without the ε statistical uncertainty (×1.5 at 68 % CL) and without the
  ≈ 43–45 estimate. One parenthesis would make it match the body: "(efficiency statistically uncertain by ×1.5; ≈ 43–45
  with the full-chain systematic, not applied)". "Stage-3 hits" (abstract l.24) is project jargon. Write "truth-level
  quirk hits".
- **C-2.** The Fig. 6 caption says "nine cells at 3 and 5 keV use the full ACTS chain". The D1 map shows only E, so it has
  eight full-chain cells; Ẽ500 at 5 keV is not in the map (FIGURES_FINAL l.76).
- **C-3.** §8.2 l.27 says "0.90–0.97 at 1.5–2 keV for all five (species, mass) points". Ẽ500 has no 1.5 keV entry. Also,
  "The SR-T share is 30–70 %" is "typically 30–70 % (range 0–100 %)" in the source (§4.4).
- **C-4.** §7.3 l.69 uses a bare K = 1.4 for the SM K-factor. That collides with the rotation constant K(γ*) (App. A),
  which R1 B-8 had freed by renaming the signal K-factor to K_QCD. Use K_SM.
- **C-5.** Internal process labels are back in the P2 body: C12FC_v1, C1a/C1b/C2B, R1–R6, "analysis fix R6", D13, V4-3,
  V4-5, A2FC and "numpy". Each is either defined once (Tab. 6) or replaceable by plain words ("the final run", "the
  analysis reviews"). This is low priority.
- **C-6. Bibliography rendering.**
  - [12] FASER prints "Phys. Rev. Lett., 7 2026" (the month as a number, no volume or pages). Use "(2026), in press" or
    add the volume when it is known.
  - [13] The HEPData title is lower-cased and has typographic quote errors (”exclusion contours” of ”first search … lhc
    with faser”). Protect it with braces.
- **C-7.** The Fig. 11 caption says "stopped-quirk recast", while the figure says "Evans–Luty out-of-time recast". Use one
  name.
- **C-8.** §12 does not mention V4-4 PARTIAL (STAGE4_RESULTS caveat 22). Add it in a few words to item 7.
- **C-9.** In §9.3 / Fig. 10, "upper cluster starts at the pair-mass threshold 2m_Q" is fine at PU 200. Without pile-up the
  minimum is 1.69 m_Q, so "near 2m_Q" is more accurate.
- **C-10.** §7.4: the PV-pair chain "(0 of 24) gives 1.4×10⁵" cannot be reproduced from the stated generic chain. With
  f_pre · (24/500) · (1.14/24) · c · rate · N_trig it would give ≈ 3×10⁶. The PV-pair bound sits on a different
  conditional (p(R08 | R02), INV_STATS_BKG l.226). Name that conditional, or drop "(0 of 24)".

---

## 3. Checklist summary

| Check | Result |
|---|---|
| Numbers vs sources (≥ 25; ≥ 15 in P2) | ≈ 80 checked (≈ 70 in P2). All match except the stale C′ rates (A-1). The headline chain (1.23e6, 7.05, 37.6, 9/200, CP intervals, 1.25e7, 43–45, 33/40, 7 zero points, Tab. 8 and Tab. 9) is exact. |
| Physics correctness | Thinning weight (Eq. 13), zero-count bound 1.14/M, the log-normal rule constants, the M_est pair-mass reading, and μ₉₅·ε ≈ B_median for σ_ln ≈ 1.5 (consistent with "∝ the bounds") are all correct. The only issue is the inconsistent yield definition (A-2). |
| Outcome stated honestly | Yes on every listed item (§1.3), except that the published reach is not confronted (A-3) and "conservative" is unqualified (B-3). |
| No overclaiming (abstract, conclusions) | Abstract and §13 are sober: "nothing is excluded", "neither m_Q nor Λ is measured". The intro's characterisation of prior work is wrong (A-3). |
| Credit and novelty (NOVELTY_AUDIT) | P1 credit as in R1 (✓). P2 has no audit, and the intro statement about prior pile-up treatment is false (A-3). |
| References real | 12 new INSPIRE checks pass (§1.4). Rendering nits in C-6. |
| One symbol per quantity | ℰ, N_exp and σ_th/σ_norm violate it on the headline chain (A-2). K is reused (C-4). d_IT vs sep_IT^det in Fig. 9 (B-4). |
| Figures | All 12 figure pages inspected. Labels: "Private work (simulation)" with √s = 14 TeV, PU 200, 3 ab⁻¹, plus "truth level" on the P1 and truth figures. No CMS logo. Captions are complete, 2–5 sentences. In-plot text ≈ 3–4 pt on the P2 composites. Fig. 11 has stale text and internal IDs (B-4). |
| Completeness test | Fails only on the A-2 notation (FB_k undefined, two N_exp). Otherwise every choice is motivated and points to a stage report (App. B). |
| Abstract ↔ body ↔ conclusions | Consistent on every number and verdict. C-1 concerns the abstract's ε-uncertainty qualifier; B-2 concerns the conclusions' item labels. |
| Prose and logical flow | Clear structure: rule → backgrounds → outcome → efficiency → limits → handles → bounds. The P2 paragraphs are dense with process detail (§6.6, §8.2 A2FC), which is where to cut to make room for the A-3 paragraph. |
| Length | 35 pp, at the user's limit. The fixes must not exceed it. |

## Verdict: **ITERATE**

Category-A items to fix:
- **A-1:** stale C′ rates in §7.4.
- **A-2:** inconsistent ℰ / N_exp / σ_th definitions behind 37.6; FB_k undefined.
- **A-3:** false description of the Knapen et al. and Li et al. pile-up treatment, and no comparison of the null P2
  result with their published reach.

All three are text-only fixes.
