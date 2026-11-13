# Open items for the user: "From Fields to Quirks"

State at the end of the run of 2026-11-07, after the whole-book panel of the endgame (`review/ADAPTER.md`, "Endgame of 2026-11-07"). Paths are relative to `book/`; `TT:` is `stage2_C001_quirks/theory_track/`. Closed items have been removed; the round files keep the history.

## The state, plainly

**No part has passed, and neither has the whole book.** No arbiter of any part or of the whole book returned PASS in any round. A pass needs a full panel's PASS with no A or B on unchanged text, so no part has a clean final reading.

| Part | Last full panel | Its verdict | After it |
|---|---|---|---|
| I (ch 0-5) | r7 | ITERATE, A 0, B 2, C 18 | Fixed. r8 delta check of the edits only: A 0, B 0, C 4. |
| II (ch 6-10) | r7 | ITERATE, A 0, B 3, C 18 | Fixed. r8 delta check: the three B fixed, but the fix at ch09:37 introduced a new B. That was fixed in r8, and no reviewer has checked the new fix by itself. |
| III (ch 11-14) | r7 | ITERATE, A 0, B 4, C 15 | Fixed. r8 delta check: A 0, B 0, C 8. |
| IV (ch 15-18) | r9 (the guard) | ITERATE, A 1, B 5, C 24 | All fixed, with the 10 C marked fact. Not checked edit by edit. |
| V (ch 19-24) | r9 (the guard) | ITERATE, A 2, B 1, C 24 | A1, B1 and 15 C fixed; A2 open (below). Not checked edit by edit. |
| VI (ch 25-29) | r9 (the guard) | ITERATE, A 2, B 7, C 18 | All fixed, with the starred C. Not checked edit by edit. |

- **Whole-book panel** (`review/final/r3`: references, rendering, cross-part), read the 333-page book after all the part fixes. Reviewers: bibtex A 0, B 0, C 9 (no wrong or misattributed reference); rendering A 0, B 2, C 8; cross-part A 0, B 3, C 7. Arbiter: ITERATE, A 2, B 6, C 21. Fixed except A1 (the figure below). One delta check of those fixes (`final/r3/delta1.txt`): A 0, B 0, C 3. No second delta check ran, and none was needed for A or B.
- The cross-part reviewer looked at seams between parts, not at the physics of each passage, so the Part IV to VI fixes and the Part II r8 fix have been read since only in that sense.
- The earlier 264-page book was read twice by a whole-book panel on 6 November (`final/r1`, `r2`): ITERATE both times (A 4, B 43; then A 2, B 32).
- `tools/gates.py --all`: ALL GATES PASS. The gates passed while every A above stood, so they say little about correctness.
- `tools/check_validated.py --all`: 120 of 120. Fig. 19.3 (ch19/event_anatomy) was validated after the run by a separate plot validator (`final/r3/plot_event_anatomy.txt`): pass, no findings.
- Length: 334 pages against section 11's "about 290 in total is a sensible upper limit". Your decision.
- The preface's account of the review and the notice were rewritten from these facts at the end of the run.

## A or B findings not fixed

None. Fig. 19.3 (Part V r9 A2, whole-book r3 A1) was validated after the run, which closes the last one.

## Logged C findings worth your time

- **Fig. 0.3, the road map**: six question subtitles ("What is a particle?" and so on), the register you objected to, and a Part VI box ("Signal, background, bottlenecks, limits") that does not name Chapter 29's audit, money plots and final account. A change needs a new validator's mark.
- **Overture, ch00:94**: "A pre-set validation test failed and one prediction failed too" leaves out the six lesser pre-set checks that failed as written (Chapter 18). Cross-part C1.
- **Textbook parallels** (Example 4.3 and Zee, Exercises 4.5 and 5.4, Section 4.1, Example 11.4): nobody has compared them with the books.
- **ch04:109**: says the real and imaginary parts of a charged field are the observables; for a gauged charge they are not, and ch06:225 takes the other line.
- **ch02:133, :196, :297**: the silicon Raman line is 64.5 to 64.6 meV (about 65), printed 64.
- **ch19:189 caption** still says "not the flow of charge of Chapter 7's rules", a phrase Chapter 7 no longer uses. `checks/ch07_checks.py` cites equation numbers that do not exist.
- **ch14:128** "as in Creutz's scan" is not verified at source; dropping the clause loses nothing. **ch14:130**: 1.32 and 0.76 come from the unrounded 0.0174, not the printed 0.017. Sidenote 5 of ch13 ends 8 pt from the paper edge.
- **ch22:121**: applies n_lay = 4 zeta to longer tracks on the strength of one summarised fetch.
- **Showcase event (ch25:27, ch26:142)**: whether it really swings little cannot be decided from the stored files (no hit times); the text now says so.
- **Whole-book delta C1 to C3**: ch18:177 "each event of the grid" should read "each event of the grid up to 5 keV" (the 7 and 10 keV events ran at B0 only); ch29:49 table cell has no verb for "estimates"; Appendix A's row for c omits Chapter 24's local use.
- **Appendix A** does not list g, f and alpha among the overloaded symbols (cross-part C6(e)).
- Style: stock openers and closers, bare `\eqref` against "eqn", long sentences, margin notes below the text block on three pages.

## Errors found in the frozen study files (read only; not edited)

Corrections the study's paper and notes would need. The book follows the evidence in each case.
- TT:`paper/sections/04_truth_p1.tex:35-36` and TT:`sim/stage3/README.md:51`: 0.966 is the 0.45 keV entry; at 0.6 to 5 keV the low end is 0.975.
- TT:`paper/sections/04_truth_p1.tex:48-49`: the c-law window is stated as safe; the study's own bins depart by +6.5% inside it at 5 keV (README.md:206-209; 04_truth_p1.tex:57 gives +3 to +5%).
- TT:`paper/sections/04_truth_p1.tex:76`: "followed at 1-3 keV" for all five points; the criterion passes in 9 of 30 cells (VALIDATION.md:42).
- TT:`paper/sections/04_truth_p1.tex:115` overstates README.md:191: one of the four points is 0.95 sigma low.
- TT:`paper/sections/03_string_dynamics.tex:194, :209-210`: 0.105 against 0.104 listed as verified within 1.5%; the two come from different samples, and on the same events the median is +2.4% high (VALIDATION_GATE.md:74-77; `analytic/numerics/results/FU.json`).
- TT:`paper/sections/03_string_dynamics.tex:173, :185, :198`: K_vac listed among the blind numerics.
- TT:`paper/sections/03_string_dynamics.tex:257`: "linear in the endpoint proper time", against the study's own audit.
- TT:`paper/sections/03_string_dynamics.tex:139`: coverage fractions quoted without naming the sample; `:195` range label of 0.911; `:250` "published limits".
- TT:`paper/sections/02_model_samples.tex:59`: an |eta| < 4 cut on f_200 that the script does not apply.
- TT:`paper/sections/05_detector_chain.tex:84-85`: a 93% vertex efficiency, unverified, that the acceptance does not apply.
- TT:`paper/sections/07_backgrounds.tex:77-79`: credits Knapen et al. Sec. III.D with a list of coplanar topologies; that paper names only beam-pipe conversions.
- `stage2_C001_quirks/research/theory_signal_model.md`: :264 and :486 (B prevents re-annihilation below an MeV, unqualified, against NEAR_MISS_IMPULSE.md:401-406); :430 ("nearly helical"); :476 (24.7); Table 4.2a :368 (31 against 37).
- TT:`analytic/NEAR_MISS_IMPULSE.md:308` calls v = 0.62, v_cm = 0.25 Knapen et al.'s benchmark.
- TT:`analytic/NOVELTY_AUDIT.md:219` says the ATLAS quirk source was "not read" (T2_string_dynamics.md records it read and ported); `:225` sets a plotted total for two events against a per-oscillation estimate and calls the difference mass dependence.
- TT:`acts/stage4/plan.md:496` calls the 23 to 30 um the multiple-scattering floor; it is the event-level out-of-plane resolution (THEORY_GAPS_SYNTHESIS_v4.md:296, :314, :713).

## Disagreements between the book and the study's paper or reports, stated in the book

- ch18:169, Table 18.1 row three: the paper lists it as verified; the book says the two numbers are from different samples and gives the same-event +2.4%.
- ch18:171: the paper prints a prediction of 0.914 over B0/80 to B0 beside a measurement fitted over B0/80 to 2B0; the book computes over the measured range.
- ch18:179: the paper's 0.966 is its 0.45 keV entry.
- ch18:229: the paper says the prediction is followed at 1 to 3 keV; the book shows it holds at some points only (9 of 30).
- ch18, window and Table 18.2: the paper calls the window safe; the book reports the 5 keV departure inside it.
- ch16:173, ch19:130, ch25:43: the paper adds pair |eta| < 4 to f_200; the script does not.
- ch28:267: the study's "about one decade" from a deeper sample is 0.6 at R09 by the book's sum (0.8 at R14, 1.7 at R23).
- ch28:275: the study's conclusions give 0 to 2 decades left in the late-hit category; the book cannot reproduce this from the final stored terms, and the results report flags the figure as stale.
- ch16:189 (not the study's paper): the bound regions drawn disagree with Farina and Low's table at 1 eV and 1 keV; cause unresolved.

## What a human should check first

1. The Part IV to VI fixes of round 9, which carry the study's claims and which no reviewer has checked edit by edit: ch18 (the window, Tables 18.1 and 18.2, the sample at :175-177), ch25:104, ch28:267, ch26:142 with ch25:27, ch26:112, ch29:218 and :224.
2. ch09:37 and its margin note (Part II r8 fix).
3. The frozen-file errors above, for a corrected version of the study's paper, starting with 04_truth_p1.tex:48-49 and :76 and 03_string_dynamics.tex:194, :257.
4. Length and the road map's question subtitles: your decisions.
5. `tools/check_pages.py` ignores margin word boxes taller than 30 pt, so a clash involving only a tall glyph would go unseen, and it misses margin text low on the page (the ch13 sidenote is one such case).
