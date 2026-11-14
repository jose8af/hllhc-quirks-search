# Physics review, cycle 5: STRATEGY v5 (`STRATEGY_gunnar_2026-11-14_00-50.md`), Phase 1, quirks v2

Reviewer: Hana (physics reviewer, fresh to the panel), 2026-11-14 01:25.

**What I read.**
- `agents/physics_reviewer.md`, `outputs/FRAMING.md`, the artifact in full (l.1–2943, consecutive chunks), the cycle-4
  arbiter verdict (Greta), the cycle-4 physics review (Florence) and the fix report (Gunnar; used only for grep
  pointers).
- Sources I opened: `TT/data/acts_stage4/analysis/C12FC_v1/background.json` (`cprime.gamma.rows`, `cprime.dif.rows`,
  `cprime.gamma.rate`), PLAN l.105–127 (reach table) and l.494–521 (outcome table), `src/strategy_budget.py`
  l.556–800 (projection code).
- I did not read the methodology spec or the conventions.

**Own arithmetic.** I ran the script (`nice python3 -I`, rc 0). Its output is byte-identical to
`outputs/budget_stdout_v5.txt`. For checks beyond the printed rows I loaded the script's own functions with `runpy`
(`pmf_pred`, `s95_pmf`, `rfmt`, `s95_fixed`, `kap_nodif`, `PU9`, `K_DIF`, `kz`), so every number below uses the
artifact's method. Script: scratchpad `hana/hana_check.py`. The output is in the session log.

**Conventions.** "l." means a line of v5. **A** would give a wrong or indefensible result; **B** must be fixed before
approval; **C** is a suggestion.

---

## Part 1. Verification of R1–R5

| # | status | v5 location, quoted phrase | my check |
|---|---|---|---|
| **R1** honest headline | **PARTIALLY RESOLVED** (all eight ordered parts are present and reproduced; one residual, B-1) | §0 l.55–61 "The conversions fell by ×6.6 and ×6.5 per width step (86 → 13 → 2)"; l.63–94 "≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge (median ≈ 315 GeV; ≈ 390 GeV if that background were known exactly, below 200 GeV if it carries a systematic width of 0.2, PLAN l.122)"; leading sentence l.91–94; Table 4.4c l.949 "**(α1′)** … **317–314 [273–270]; ≈ 390 (394–392) at fixed B**"; scenario text l.959–974; §4.4 l.991–993 "is the expected branch"; §11.7 rule 1 l.2702–2703; Q2 l.2743–2764; §12.5 point 3 l.2867–2870 | See the detailed checks below. Every number reproduces. The leading sentence omits the one fact that makes 270 GeV a statistics-only upper edge. By the strategy's own systematic plan that fact applies (B-1). |
| **R2** Q3 annex | **RESOLVED** (physics content) | annex l.2827–2829 "**route 5: promotion model not submitted**", "**route 6: S_CKF NOT TESTED**", "**B4-e, size**"; Q3 l.2771–2774 | B4-e floor: 4×10⁵ × 1.14/100 = 4,560 events, so it alone exceeds the B₅₀ = 300 class. Correct. Route 6: H on all own hits = H_CKF/(1 − ε_pair), ×5–50 at ε_pair = 0.8–0.98. Correct. Route 5: "(β) then becomes (γ)-like" is right physically, because every credited SM term including Z(νν) then sits at H. |
| **R3** pilot records | **RESOLVED** (physics content) | §4.4 point 5 l.847–850 "keep the full hit records … provisionally by day 7 and with the frozen hand-over variant by day 12"; §11.7 l.2683–2696 | (4×10⁶ + 2.3×10⁶) × 8.2 kB = 51.7 GB. Reproduced. Classifying stored records later loses nothing physically. The day-7 projection uses the v1-based pile-up rows, which is honest because the occupancy model does not exist yet. |
| **R4** S_CKF samples | **RESOLVED** | l.757–763 "for DIF on the enriched test overlays with their weights … for NI by the rung split, derivation R04, test R05 … S_CKF is a survival factor conditional on the no-pile-up class, so the selection of the enriched overlays on that class does not bias it"; Df-9 l.2809 | The physics is correct. S_CKF is P(survive CKF and f_CKF \| class k). Enriched overlays are selected on k with known weights, so within a class the survival is unbiased. Only the ceiling and leak tests need events from outside every class, and they stay on unbiased samples (l.778–784). The NI counts at R05 are 92/120/378 (Table 4.4b), so the test is evaluable. |
| **R5** paired passes | **RESOLVED** (physics content) | l.798–800 "1,000 test-half events of **each of the fifteen SM processes**"; borrowing sentence deleted; §4.0 point 6 l.435–437 "For SM processes H′ may exceed H by orders of magnitude" | (4,000 + 15,000) × 11.7 s = 61.8 CPU-h, which matches "62". No completeness credit is borrowed any more. The H′ sentence tells the user the physical cost of a completeness not-PASS. |

### R1, detailed checks (my own)

1. **v1 counts.** From `cprime.gamma.rows` I read 153 (R04), 86 (R05) and 13 (R06) attributed conversion candidates
   per 500 full-pile-up events. R07 is the conditional 2/13 and R08 is 0/13. From `cprime.dif.rows` I read 166 / 81
   and the conditionals 2/81 and 1/81. These are identical to Table 4.4b. The two falls are 86/13 = ×6.6 and
   13/2 = ×6.5. The counts are nested, so the two steps are conditionally independent binomial measurements, and
   treating them as two independent measurements of the fall is legitimate.
2. **Test against a pile-up-like fall.** From 13 counts at R06, a fall of ×339 or ×201 gives μ = 0.038 or 0.065
   counts at R07.
   - Poisson P(≥ 2) = 7.2×10⁻⁴ / 2.0×10⁻³.
   - The exact binomial (n = 13, p = 1/339 or 1/201) gives 6.6×10⁻⁴ / 1.9×10⁻³.

   The quoted "7×10⁻⁴–2×10⁻³" is right. The independent step from 86 is decisive on its own (P < 10⁻¹⁴). For
   conversions the pile-up-like fall is excluded. For DIF (2 → 1) it is disfavoured at about 1 %.
3. **Extrapolated size, by the strategy's own rule** (the fall per width step that the sample itself measures,
   §4.4 point 5).
   - R07: 4.0848×10⁷ × 0.3786 × 2/500 = 6.19×10⁴.
   - R08 = R07/6.5 = **9.52×10³**. R09 = R08, because the untested fit-probability conditional is 1.
   - With DIF at the pile-up fall (385–647), the background is 9.9×10³–1.02×10⁴.

   All of this reproduces.
4. **Reach figures and mapping.**
   - The mapping is linear in ln s₉₅ between PLAN's σ_ln = 0 columns. s₉₅_fixed(10⁵) = 621.5 ↔ 243 GeV, and
     1.96·√10⁵ = 620, so the extension is consistent.
   - The (α1′) row has a count width of 0.02, because the conversion term is counted on the Z(νν) pool share,
     m ≈ 9,530/2.28 ≈ 4,200 counts.
   - Median s₉₅ 352–361 → 317–314 GeV. 84 % s₉₅ 491–507 → 274–270 GeV. Fixed B: s₉₅ 197–199 → 394–392 GeV.
   - Interpolation check: (ln 352 − ln 197.7)/(ln 621.5 − ln 197.7) = 0.504 → 393 − 0.504 × 150 = 317. Reproduced.
   - The step from 390 (fixed B) to 315 (median) has a physical cause. The term's simulation-count width
     (2 % of 10⁴ = 200 events) is larger than its Poisson width (100 events), so it roughly doubles the limit.
5. **Upside stated as upside.**
   - The empty-ceiling case (790 median, 712 at the 84 % edge) appears only as "an upper edge that the strategy's own
     planning estimate does not expect" (l.72–73, l.938, Q2).
   - The (α1) case is introduced as "which v1's conversion counts disfavour at p ≈ 10⁻³".
   - Both are correct.
6. **ESTIMATE labels.** The leading sentence, the "Expected" paragraph, Q2, the Q3 reach clause, the Table 4.4c
   caption, the scenario text and §12.5 point 3 all carry "ESTIMATE, v1 placeholder efficiencies" or the §12.1
   blanket statement (l.2734–2735).
7. **Consistency of the statement.** The same branch, the same numbers and the "expected" wording appear in §0,
   Table 4.4c with its "What is not known" paragraph, §4.11 point 3, §11.7 rule 1, Q2 and §12.5.
   - grep "realistic branch" finds only the §13.3 history row.
   - grep "promotion credit" and "below 393" find nothing.
   - One stale sentence remains, in [L13] (C-5).
8. **Q2 options.** The three options are physically sensible and correctly ordered:
   - (a) pause and ask, the default;
   - (b) pre-authorise the "real background" paper;
   - (c) pre-authorise a pre-freeze conversion-removing conditional.

   The ● on (a) loses only the turnaround if the pilot is kinder than v1. That is the right default. The consequence
   stated for (b) is the defect (B-1). The success condition of (c) is not stated (C-2).
9. **The conversion veto as an option.** It is physically plausible.
   - A photon conversion gives a two-prong vertex with near-zero opening angle and invariant mass, at a material
     radius (beam pipe, pixel layers), with no hits on the inner layers.
   - A quirk ribbon starts at the primary vertex.
   - The veto is defined from background samples only (B3-b, l.1200–1201). T2 keeps every selection with and without
     it (l.1762). The risk to signal is named (l.1259).
   - No rejection factor is quoted anywhere in v5 (grep "veto"), so the untested veto is **not** presented as if its
     gain were known.
   - One nuance: Q2's "Upside" sentence attaches the (α1) numbers to "a conversion-removing conditional … is tested".
     That implicitly assumes a rejection of about ×30–50 without saying so (C-2).

---

## Part 2. Did the fix break anything physical? (diff v4 → v5)

I ran `diff STRATEGY_fiona_2026-11-13_23-05.md STRATEGY_gunnar_2026-11-14_00-50.md` and read all 64 hunks. Every
hunk traces to R1–R5 or to an adopted C item:

| change | finding |
|---|---|
| header and version | — |
| §0 point 3, Expected, leading sentence; Table 4.4c rows; scenario text; §4.4 l.991–993; §4.11 point 3; §11.7 rule 1; Q2; §12.5 points 2–3 | R1 |
| storage; §4.4 point 5; §11.3–11.4; §11.7 inputs and day-7 input | R3 |
| §4.4 point 4 S_CKF; Df-9 | R4 |
| §4.0 point 6 H′; §4.4 (ii); §4.7 cost; inventory row 20; §11.1–11.3, §11.6, Q4 totals | R5 |
| G-C14 (`s4cp.py` l.115, WZ 1.5687); G-C5/Ph-C4 (0.34 [U], 2.1 %); G-C6; Ph-C7 (multijet ceiling also tests B4-e); G-C9 (derivation parity half); G-C4 (terms vs processes); N-C1, N-C4, N-C6, G-C2 (Df-10 4.7–4.9 %); the §13.4 table | adopted C items |

The physics of the C-item hunks is correct:
- Ph-C7 is the right attribution of a multijet ceiling FAIL.
- With G-C9 the test half stays unseen before its prediction exists.
- 0.34 = 2 × 0.17 for ℓ = e, μ is right.

The script's stdout changed in 22 lines, all of them R1, R3, R5 or G-C14 lines or totals that follow from R5. Every
other printed number, including the floors, the family-wise rates and the pile-up rows, is unchanged. **No
unattributed or physics-damaging change.**

---

## Part 3. New findings

### B-1. The expected-branch reach is quoted without the systematic width that the strategy itself commits to. That width makes the 270 / 315 / 390 GeV figures statistics-only upper edges, and the realistic reach is below 200 GeV (at the existing bounds). (§0 leading sentence l.91–94; Q2 l.2745–2746 and option (b) l.2757; §12.5 point 3)

1. **What the text says.**
   - The leading sentence gives "≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if the background were known
     exactly)" and nothing else.
   - The §0 paragraph and Q2 add "below 200 GeV with a 20 % systematic width". Q2 option (b) promises "the reach at
     that B (≈ 270–390 GeV as above)".
   - The arbiter's own §2 ruling said that the statistics-only nature "belongs in the headline of that branch". The
     leading sentence, which is the line for `STATUS.md` and the Gate-A package, does not carry it.
2. **The width is not hypothetical: the strategy commits to it.**
   - The conversions are inside the B4 SM terms, B_t = N_trig,t × rate_t × … (§2 route table; §4.4 l.826–827).
   - Each B4 term carries "the normalisation nuisance of the term" from the generator difference. FEAS_B measured MG5
     against Pythia for Z(νν)+jet at a ratio of **0.84** (l.1281–1282; §5.1 rows "4-fermion backgrounds" and
     "Background normalisation"; T1 "N_trig normalisation per process group (generator difference, K)", l.1554).
   - ln 0.84 = −0.17. Z(νν) carries 61 % of N_trig and the W rates get the same treatment.
   - On top of that come the K uncertainty, luminosity, and the material nuisance on every term (B6 table l.1453–1455;
     the conversion probability is proportional to x/X₀), plus, if the term is credited, its closure nuisance
     (s_model ≤ 0.231 and an extrapolation width of 0.73–1.41 at R08).
3. **What this does to the number.** My run uses the script's functions, with the (α1′) conversion term given a
   log-normal width instead of its count width, and everything else unchanged:

   | width | median s₉₅ | 84 % s₉₅ | reach, median [84 % edge] |
   |---|---|---|---|
   | 0.02 | 419 | 592 | 295 [249] GeV |
   | **0.05** | **≈ 900** | ≈ 1,300 | **below 243 GeV**: beyond the plan's 10⁵ column; linear extrapolation in ln s₉₅ gives ≈ 195 GeV |
   | 0.10 | ≈ 1,660 | | |
   | 0.20 | ≈ 3,000 | | |

   At the 0.17 that the strategy's own normalisation nuisance implies, the reach is **below 200 GeV** (PLAN l.122:
   "–" = below 200 GeV at σ_ln = 0.2 and B = 10⁴). That is at the existing bounds (≲ 180 GeV, PLAN l.115–116;
   FASER 113–179 GeV, §6.2). The threshold at which the 270 GeV figure stops holding is about 0.03–0.05, not 0.2.
4. **Why it matters for Gate A.**
   - Q2 asks the user to choose between (b), proceed to the "real background" paper, and (c), a pre-freeze
     conversion-removing redesign.
   - By the strategy's own likelihood, (b) is expected to give a reach at or below the existing limits. The FRAMING
     message, "it reaches X GeV, beyond existing limits" (FRAMING l.38–40), would then not hold.
   - (c) is the only route in the expected case to a reach beyond the existing bounds. The user should see that
     contrast in the numbers, not "≈ 270–390 GeV".
5. **Why B and not A.** No result is computed from it. The default (a) pauses and asks the user again at day 15 with
   the pilot's measured counts, so nothing irreversible follows. The facts are present in the text (§4.7, §5.1, PLAN
   l.122); they are simply not connected to the headline.

   **Why B and not C.** It is the reach of the expected deliverable put to the user in Q2. Cycle 5 admits exactly
   this kind of finding: a number shown to the user that the document's own plan contradicts.
6. **Fix (text plus one script print line, 0 CPU-h).**
   - (i) In [9b], print the (α1′) no-credit row with a log-normal normalisation width of 0.17 (ln 0.84, FEAS_B) on
     the conversion term, and at 0.05. The reach is "< 243", with the extrapolated value labelled as an extrapolation
     beyond the plan's table.
   - (ii) Leading sentence: after "≈ 390 GeV if the background were known exactly" add "; with the normalisation
     width the strategy assigns to the SM terms (generator difference 0.84, §4.7) the reach is below 200 GeV, at the
     existing bounds".
   - (iii) Q2 stem and option (b): "the reach at that B: below 200 GeV with the planned normalisation and material
     widths (≈ 270–390 GeV only if this background carried no systematic width beyond ≈ 3 %)". Say in the same
     clause that (c) is then the only route to a reach beyond the existing bounds in the expected case.
   - (iv) Replace "below 200 GeV if it carries a systematic width of 0.2" in §0, the scenario text and §12.5 point 3
     with "below 243 GeV already at a width of 0.05, below 200 GeV at the planned ≈ 0.17".

### C items

- **C-1. Which photon rate is used.** (α1′) multiplies the total N_trig by v1's maximum-over-processes photon rate,
  0.379 (tt̄ 1ℓ), which v1 chose as "conservative" (`cprime.gamma.rate.choice`). v2 counts conversions per process.
  The N_trig-weighted rate of 0.255 (`nt_weighted_mean`) gives:
  - conversions 6.4×10³, B₅₀ 6.8×10³;
  - reach 342 [298] GeV, 419 at fixed B (my run).

  This is inside the factor-e size uncertainty and does not change the pause. Label the row "(v1's max-over-process
  photon rate; ×0.67 with the N_trig-weighted rate)". The Z(νν) m_H line already uses the per-process 0.2306.
- **C-2. Q2: what the "upside" and option (c) need.**
  - (α1) without credit has B₅₀ = 587–975 > 300, so the pause fires in the first upside branch too (§4.4 l.993 says
    so; Q2 does not).
  - The DIF part alone at the pile-up fall is 385–647 without credit, so a conversion veto by itself cannot bring
    B₅₀ below 300.
  - The fit probability at v1's **conversion** conditional 2/13 leaves 9.5×10³ × 2/13 ≈ 1.5×10³ conversions
    (1.8–2.1×10³ with DIF). That is also above 300.

  Add one clause to (c): "works" means a projected B₅₀ ≤ 300. That needs a conversion rejection of about ×30–50,
  tested within two rungs (width ≈ 0.8), and fit-probability credit for DIF as well.
- **C-3. Physics expectation for the fall.** If the ribbon width of a conversion pair is set by its sagitta,
  w ∝ 1/p_T, then for dN/dp_T ∝ p_T^(−n) each halving of the width costs ×2^(n−1). v1's ×6.5 corresponds to n ≈ 3.7.
  A steepening spectrum at the R08 width (e± of order 8 GeV for 4.7 mm over ≈ 0.5 m in 3.8 T) would make the next
  step steeper than ×6.5, so the extrapolation is, if anything, conservative. One sentence would help the reader. The
  pilot's 2.3×10⁶ Z(νν) events (≈ 3×10² conversion ceiling counts at R08 if v1's fall holds) measure it by day 7, and
  that is the correct dated rule.
- **C-4. (α2) as the downside, and the DIF wording.**
  - §0 and Q2 give only upper branches beside (α1′). DIF's own fall (2 → 1) disfavours the pile-up fall at ≈ 1 %
    too, and (α2) (≈ 7.5×10⁴ events, 262 GeV at fixed B, below 243 GeV with the count width) is its downside.
  - "it is the branch the v1 record supports" (l.962) is too generous for the DIF half. "the more favourable DIF
    reading (the PV-placement and attribution caveats act on DIF)" would be exact.
- **C-5. [L13] (l.2260–2262)** still reads "… if decays in flight and conversions behave as in v1 …: the result is
  then sample-size limited". In the expected branch the result is a measured large background, not a sample-size
  limit. Align it with §12.5 points 2–3.

---

## Overall judgment

**Not yet. The one blocker is B-1**: a text fix plus one script print line, 0 CPU-h. A short focused fix verified by
the arbiter is enough; another full panel is not needed. Once it is fixed, I would **approve for execution subject
to Gate A**.

**Counts.**
- R1 PARTIALLY RESOLVED (the residual is B-1). R2, R3, R4 and R5 RESOLVED.
- The diff v4 → v5 is clean: all 64 hunks are attributed and no physics is damaged.
- New findings: A = 0, B = 1, C = 5.

**What v5 does well.** I recomputed the conversion record and the fall test, the 10⁴-event extrapolation, the
(α1′), (α1) e^(±1), m_H = 1000 and (α2) rows and the extended mapping, and all of them reproduce. The expected branch
now leads consistently in the summary, the per-outcome table, the decision rule, Q2 and the risk list. The upside is
labelled as upside. The veto is offered without an invented gain. The day-7/day-15 rule reads the pilot's own fall,
which is exactly the measurement that settles the branch.

**What remains.** The number that leads is the reach of a 10⁴-event background with no systematic width. The
strategy's own systematic plan gives that background a normalisation width of about 0.17. With it the expected
deliverable of option (b) reaches below 200 GeV, which is not beyond the existing limits. The user must see this
before answering Q2.
