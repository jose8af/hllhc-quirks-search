# D3: corrections list, book Part VI, reach table and book checks (investigator Albert, 2026-11-13)

Scope: `book/review/UNRESOLVED.md`, `book/partVI_the_study.pdf` (ch25-29), `book/chapters/ch25-29_*.tex`,
`book/checks/`, read against `publication_plan/publication_plan.tex` (the "plan"). Read-only; nothing in `book/`,
`stage2_C001_quirks/` or `publication_plan/` was changed.

Path shorthands: `TT:` = `stage2_C001_quirks/theory_track/`; `UNR` = `book/review/UNRESOLVED.md`; `PLAN` =
`publication_plan/publication_plan.tex`; `chNN:L` = `book/chapters/chNN_*.tex` line L. PDF page = book page - 234
(e.g. book p. 291 = PDF p. 57).

Tags: **VERIFIED** = I re-derived it or read the exact text at the cited line in this session; **ESTIMATE** = an
estimate in the source (the book's `\EST` or the study's ESTIMATE), or mine; **UNVERIFIED** = transcribed, not checked.

---

## 1. Complete correction list (source: UNR:45-74, plus items the book records that UNR does not list)

Fix type: **(a)** paper text only (fixed in the v2 paper; the v0.4 files stay as they are), **(b)** a v1 frozen file
(stays frozen; v2 carries an erratum note), **(c)** code or analysis. "P§3.4-n" = the n-th of the seven errors in
PLAN:241-251. "Status" says what I checked.

| # | error | where | correct statement | how established | fix | status |
|---|---|---|---|---|---|---|
| 1 | f_200 defined with pair \|eta\|<4, which the normalisation script does not apply (P§3.4-1) | TT:paper/sections/02_model_samples.tex:59; book ch25:43, ch16:173, ch19:130 | f_200 = fraction with pT(QQ)>200 GeV, no eta cut; the cut removes <0.02% of the tail, so no number changes | UNR:56, UNR:71; TT:acts/stage4/investigation/INV_NORM_F200.md:61 ("removes < 0.02 % of the tail") | (a) | Text at 02:59 VERIFIED. Note: TT:acts/stage4/investigation/inv_norm_f200.py:3-4 computes a variant *with* \|eta\|<4 (make_inputs.py eta_max 4), while the N_exp path uses f_tail from TT:sim/results/xsec.json. Size <0.02% VERIFIED (read in the file). Simplest v2 fix: define f_200 without the cut. |
| 2 | 93% vertex identification efficiency stated; unverified (graphical TDR reading) and not applied in the acceptance (P§3.4-2) | TT:paper/sections/05_detector_chain.tex:84-85 | true vertex smeared by (10,15) um; 93% not applied, so a lost or wrong vertex is not modelled | UNR:57; book ch25:104 | (a); (c) if v2 wants to model vertex choice (ch25:104: a one-spacing error moves hits ~2 pixel-band widths, ESTIMATE) | Text VERIFIED (05:84-85, "\UNV{}" in source). "Not applied" from book, UNVERIFIED in code. |
| 3 | 0.966 quoted as the low end of the per-event thickness ratio at 200 GeV; it is the 0.45 keV entry (P§3.4-3) | TT:paper/sections/04_truth_p1.tex:35-36; TT:sim/stage3/README.md:51 (frozen) | at 0.6-5 keV, E 200: 0.975-0.990 | UNR:48, UNR:68; book ch29:218 | (a)+(b) | VERIFIED: TT:sim/stage3/results/P1.json F_m200 ratios 0.966 (0.45), 0.975 (0.6), 0.986, 0.987, 0.989, 0.990 (5 keV). |
| 4 | c-law window (median lmax/R_IT <~0.6, kB <~4) called safe; bins depart +6.5% inside it at 5 keV | 04_truth_p1.tex:48-49 (and :57 gives "+3 to +5%") | state the window as measured; E500 5 keV +6.5+-1.3% | UNR:49, UNR:70; TT:sim/stage3/README.md:206-209 | (a) | VERIFIED: README.md:209 "5 keV: +2.0 / +6.5+-1.3 % / ...". In PLAN P1 row (PLAN:153), not in the seven. |
| 5 | "prediction followed at 1-3 keV" for all five points | 04_truth_p1.tex:76 | criterion passes in 9 of 30 (point, Lambda) cells | UNR:50, UNR:69; TT:sim/stage3/VALIDATION.md:42 | (a) | VERIFIED (VALIDATION.md:42 "9/30 cells pass"). In PLAN:154, not in the seven. |
| 6 | MS-floor exponent: "the 1000 and 1500 GeV points are low by 2-2.6 sigma" overstates | 04_truth_p1.tex:115 | one of the four (F_m1500/L1, 0.46+-0.06) is 0.95 sigma low | UNR:51; TT:sim/stage3/README.md:191 | (a) | VERIFIED arithmetic: (0.517-0.46)/0.06 = 0.95; others 2.6, 1.96, 2.45 sigma. |
| 7 | c = 0.105 (blind numerics) vs 0.104 labelled "verified" / "within 1.5%"; different samples; same-event median +2.4% high (P§3.4-4) | TT:paper/sections/03_string_dynamics.tex:194, :209-210 | label "not verified at 1.5%"; same events: c2 0.1053 vs c_E1 0.1029 (+2.4%) | UNR:52, UNR:66; TT:sim/stage3/VALIDATION_GATE.md:74-77 (UNR omits the `sim/stage3/` prefix); TT:analytic/numerics/results/FU.json | (a) | VERIFIED text at 03:194 ("verified"), 03:209-210, VALIDATION_GATE.md:74-77. |
| 8 | K_vac listed among the blind numerics (P§3.4-5) | 03_string_dynamics.tex:173, :185, :198 | K_vac does not belong in the blind-numerics table | UNR:53 | (a) | Row present at 03:198 (VERIFIED). The reason it is not blind is not given in UNR: UNVERIFIED. |
| 9 | "solved only for motions linear in the endpoint proper time" (Barbashov) (P§3.4-6) | 03_string_dynamics.tex:257 | the study's audit records Barbashov's class as motions with tau = proper time of both ends (almost-periodic) | UNR:54; TT:analytic/NOVELTY_AUDIT.md:79 | (a) | Text VERIFIED; audit wording read at NOVELTY_AUDIT.md:79 (it also says "No external field" for that paper). The exact correct sentence needs a source check: UNVERIFIED. |
| 10 | coverage fractions (84-97%, 66%) quoted without naming the sample | 03_string_dynamics.tex:139 | name the sample | UNR:55 | (a) | Text VERIFIED; correct sample UNVERIFIED. |
| 11 | range label of 0.911: prediction 0.914 over B0/80..B0 printed beside a fit over B0/80..2B0 | 03_string_dynamics.tex:195 | compare over the measured range | UNR:55, UNR:67 (book ch18:171, not tracked) | (a) | Row VERIFIED at 03:195; the range of the fit UNVERIFIED. |
| 12 | "published limits" | 03_string_dynamics.tex:250 | wording (Li et al. App. C use the numerical thickness) | UNR:55 | (a) | Text VERIFIED; intended correction not stated in UNR: UNVERIFIED. |
| 13 | credits Knapen et al. Sec. III.D with the list of coplanar topologies; that paper names only beam-pipe conversions (P§3.4-7) | TT:paper/sections/07_backgrounds.tex:77-79; P2_NOVELTY_AUDIT N3 | Knapen: beam-pipe conversions; the other topologies are the study's addition | UNR:58; book ch27:82 | (a) | Citation text VERIFIED; content of Knapen Sec. III.D UNVERIFIED (paper not read). Also PLAN:169. |
| 14 | "B prevents (re-)annihilation below an MeV", unqualified | `stage2_C001_quirks/research/theory_signal_model.md:264, :486` | qualify per TT:analytic/NEAR_MISS_IMPULSE.md:401-406 | UNR:59 | (b) | Text VERIFIED; the relevance of NEAR_MISS 401-406 (even-crossing impulse) UNVERIFIED. |
| 15 | "nearly helical"; 24.7 (alpha_IC^-1); Table 4.2a 31 against 37 | theory_signal_model.md:430, :476, :368 | not stated in UNR | UNR:59 | (b) | Lines located (VERIFIED); corrections UNVERIFIED. |
| 16 | v = 0.62, v_cm = 0.25 called Knapen et al.'s benchmark | TT:analytic/NEAR_MISS_IMPULSE.md:308 | Knapen's benchmark is (2 keV, 2 T); the velocities are the study's values | UNR:60 | (b) | Text VERIFIED. |
| 17 | ATLAS quirk source "not read" | TT:analytic/NOVELTY_AUDIT.md:219 | it was read and ported (T2_string_dynamics.md); book ch25 sidenote (algorithm ported, C++ not run) | UNR:61 | (b) | Text VERIFIED ("source not read"). |
| 18 | plotted total for two events set against a per-oscillation estimate and the difference called mass dependence | NOVELTY_AUDIT.md:225 | not stated | UNR:61 | (b) | UNVERIFIED (line 225 read; the passage is long). |
| 19 | 23-30 um called the MS floor; it is the event-level out-of-plane resolution (a planning estimate, never measured) | TT:acts/stage4/plan.md:496 | resolution 23-30 um (ESTIMATE) vs floor 10-28 um | UNR:62; book ch26:23-24; ch26_numbers.csv tags it ESTIMATE | (b); and (a) for PLAN:178 / N8 | Text VERIFIED. |
| 20 | rho=3 deeper sample worth "about one decade" | study results (STAGE4_RESULTS), quoted in book Table 28.3 row 4 | 0.6 decade at R09 (0.8 at R14, 1.7 at R23), book's sum, ESTIMATE | UNR:72; ch28:267 | (a)+(b) | Book-derived, UNVERIFIED by me. PLAN:444 already uses 0.6. |
| 21 | "0-2 decades left in the late-hit category, 4-5 in the general" after the simulation steps | TT:paper/sections/13_conclusions.tex:39-41; STAGE4_RESULTS:759-761 | stale (earlier run); book cannot reproduce 0-2 | UNR:73; ch28:275 | (a)+(b) | Book-derived. |
| 22 | k_need = 1.4e7 at R08/R09 | study results report (book ch28:155 margin note) | 1.1e7 on the final run (pre-looper-fix value) | **not in UNR**; ch28:155 | (b) | VERIFIED arithmetic 1.23e6/0.11 = 1.12e7. |
| 23 | separation ruler "about 10%" | study summary (book ch26:131) | stored ratios 0.69-1.23 with 8-21% errors | **not in UNR**; ch26:131 | (a)/(b) | Book-derived. |
| 24 | full-chain rule "with pile-up" in the plan; applied without pile-up | study plan vs execution (ch26:91-92, ch25 Table 25.2) | state as applied | **not in UNR** | (a) | Book-derived; a record item more than an error. |

The seven errors of PLAN §3.4 are items 1, 2, 3, 7, 8, 9, 13: all present in UNR. UNR has 10 more frozen-file items
(4-6, 10-12, 14-19); 4 and 5 are covered by the plan's P1 row (PLAN:153-155), the rest are in no plan item. Items
22-24 come from the book text, not UNR. UNR's other content is about the book itself (C findings: Fig. 0.3, ch02 Raman
line, ch14, ch19 caption, ch25:27/ch26:142 showcase event, ch29:49 missing verb, Appendix A) and needs no v2 action.
Also note UNR:7: **no part of the book passed review**; Part VI's last panel was ITERATE (A 2, B 7), its fixes not
checked edit by edit, and UNR:78 lists ch25:104, ch26:112, ch26:142, ch28:267, ch29:218, ch29:224 as unreviewed edits.

## 2. Book chapters 25-29: what the plan relies on

**Ch25 (chain, rule; book pp. 235-247).** Defines N_exp = sigma_norm f_200 L A, S = N_exp eps_sel (ch25:40), with
A = 0.50, f_200 = 0.048 at E 200 (ESTIMATE, ch25:46). Fatras gives 1.33e5 hits/event, low by 2.3-7.3 against TDR
occupancies, hence the per-layer top-up (ch25:83-87). Finder, roads (delta_95 = 0.15 rad, W_c = 75 mm), the 23-rung
ladder (Table 25.1, ch25:148-167), and the WP rule: loosest rung with B84 <= 0.11 there and at every tighter rung
(eq. 25.x, ch25:188-194); 0.11 = 0.3/2.71 for two categories at sigma_ln = 2.3 (VERIFIED arithmetic 0.1107). Table 25.2
(ch25:214-237) is the post-freeze change record (seed threshold 6->4, N_trig set to 4.08e7, K_tt = 1.9, looper fix,
best ratio 1.1e3 -> 790). The plan relies on: the rule and 0.11 budget (PLAN:65-68), N_trig, the vertex/93% item.

**Ch26 (signal; pp. 247-254).** eps at end of counting 0.085-0.31 at 1-5 keV at PU 200, ceiling ~0.3 from the barrel
cut, fallback eps 0-0.080, zero at 7 points (ch26:64-86). Lambda window Table 26.1 (ch26:38-54): lower edge 1.03-1.22
keV at PU 200, upper edge 4.70-6.60 keV without PU. Full-chain reruns: loss 0.83 at counting, 0.87 at fallback, sign
test p = 1.6e-10 (ch26:102-108); 31 fast-path points may be high by up to 1/0.87 (ESTIMATE, ch26:115). Handles fail at
PU 200: separation flat at 18-26 mm; M_est median 2.26 m_Q with 29% below 1.5 m_Q (ch26:142). Resolution 23-30 um is a
planning ESTIMATE (ch26:24). Plan uses all of these in its "assets" table (PLAN:157-180).

**Ch27 (background; pp. 254-262).** Budget 2.7e-10 fakes per trial (ch27:27-28); R04 has 172 fakes/trial; 48,000
trials. Thinning closure failed: R04 ratio 1.500 (z=+52.8), R05 1.606 (z=+59.4), patch x2.41 from R05 (ch27:58-60);
R06 0.63, R07 0.39; trend width |1.985-0.361 r| (1.26 at R09, 6.31 at R23); route spread ln 117 = 4.76 from R11;
f_corr = 1.196 covers layers only; cross-cut factorisation test degenerate (ch27:62-75). Zero-count bound 1.14/M
(ch27:84); decays in flight 1.7e5 events from one bound in 500 (ch27:86-91). Ladder Table 27.1 (ch27:96-114), minimum
B84 = 1.23e6 at R09, 7.05 decades over budget; pile-up falls 4.9 decades R04->R07 (measured). "Nature" ratio
N_need/N_nat ~ 35 for decays in flight, 2 for vertex pairs, 7-25 others (eq. 27.x, ch27:139-144); pile-up needs ~1e9
trials vs 4.8e4, 3e6 CPU-h (ESTIMATE, ch27:146). Fallback limit: best 790 at E 200, 1.5 keV, eps = 9/200, S = 710;
mu95 = 1.25e7 (ch27:151-157); an exclusion there would need B below ~8e2 at sigma_ln = 1 (ESTIMATE, ch27:180).

**Ch28 (bottlenecks; pp. 262-277). Brute-force cost table** = Table 28.3 (ch28:122-145, book p. 269): row 7 "every
background sample x100: 3.4e4 h; 200 days; two of the seven decades"; rows 1-6 are the deferred samples (99, 163, 157,
128 h; 1.0/1.4 h wall; ~300 h for x10 signal rows). Eq. 28.x (ch28:149-156): k_need = 1.23e6/0.11 = 1.1e7, ~4e9 CPU-h
("five months of a million cores"); x100 costs "of order $1500" at 3-5 cents/vCPU-h (ESTIMATE, ch28:200). **The ranking**
= Table 28.5 (ch28:244-265, book p. 275): 1 no data anchor; 2 counting as the estimator (gun-sample conditionals 2-2.3
decades, late-hit credit up to 4 in that category, rho=3 about 1); 3 signal yield (merging-tolerant rung, endcap x3.2,
seed opening angle, more rows); 4 m_Q and Lambda at PU 200; 5 "decide rows 1 to 4 together, then freeze once"; 6 CPU
and infrastructure. **Sideband floor** = Example 28.x (ch28:212-218, book p. 273): 20 roads, T ~ 0.05, 8.2e8 trials in
data (4.08e7 x 20), empty sideband enters as 1.14 with sigma_ln = 1, transfer width 0.47 (CMS's) -> sigma_ln = 1.105,
B84 = 1.14 x 0.05 x e^1.105 = 0.17 (VERIFIED arithmetic 0.172); searching 8.2e8 roads costs 1.8e6 CPU-h; the two
untested assumptions (flat in angle to MET, roads independent). Also: 46 GB on an external drive, Linux port never
tested (ch28:203), "Mac only" cloud decision (ch28:197), Fig. 28.5 remedies sum (single-interaction conditionals stop
near 6 decades; pile-up with a deeper sample 3.7-3.8).

**Ch29 (account; pp. 277-294).** Constraint audit Table 29.1 (ch29:24-89). **Endcap estimate** Example 29.1
(ch29:106-110): 69% of pairs with |eta_pair|<2.5 lie outside the barrel; signal x(1 + (0.69/0.31) g), x3.2 at g = 1
(ESTIMATE, ours); best ratio 790 -> ~250; hard ceiling x16 (g = 6.9) at eps = 0.045; caveats (no 3-layer seeds at
1.0-1.3, timing to |eta|~1.5, disc phi resolution x2.5, own unmeasured background). **Reach** section 29.4 and Table
29.2 (§3 below). Final account (ch29:217-227): what failed (1.5% c gate at 3 of 5 points, 9/30 cells, straight-string
0.50 vs 0.75+-0.08, closure, upper-edge comparator, finder checks partial).

## 3. Table 29.2, exact transcription (ch29:189-204; book p. 291 = PDF p. 57)

Caption: "The reach in GeV against an assumed background in 3 ab^-1 (EST), from (29.2) at the best Lambda per mass. A
dash means that no stored mass reaches, so the reach would lie below 200 GeV. The last row scales the signal by 3.2, the
case g = 1 of Example 29.1, with sigma_ln = 0."

| B | 0 | 1 | 10 | 30 | 100 | 10^3 | 10^4 | 10^5 |
|---|---|---|---|---|---|---|---|---|
| sigma_ln = 0 | 1026 | 971 | 866 | 799 | 717 | 548 | 393 | 243 |
| sigma_ln = 0.2 | 1026 | 970 | 854 | 760 | 622 | 325 | -- | -- |
| sigma_ln = 1 | 1026 | 965 | 796 | 662 | 495 | -- | -- | -- |
| endcap, g = 1 | 1265 | 1200 | 1062 | 979 | 897 | 729 | 554 | 396 |

PLAN Table 2 (PLAN:117-126) matches the book cell for cell (VERIFIED by reading both).

**How it is computed** (`book/checks/ch29_checks.py:25-79`; ch29:163-175):
- s95(B, sigma_ln): one bin, observed count n = median of Poisson(B), background log-normal with median B and width
  sigma_ln integrated on a z grid; solve CLs = <P(N<=n | s+B e^{sigma z})>/<P(N<=n | B e^{sigma z})> = 0.05 (brentq).
  B = 0 gives -ln 0.05 = 3.00.
- S(m): for each E mass {200, 500, 1000, 1500} the largest stored `S_at_rfb` over Lambda in
  {0.45 ... 5 keV} from `TT:data/acts_stage4/analysis/STAGE4_SUMMARY.json` `fallback_points`, i.e. the signal at each
  point's **fallback** selection, 3 ab^-1, N_IC = 2, barrel only. ln S interpolated linearly in m.
- reach = mass where S(m) = s95; "--" if S(200) < s95. Endcap row: S x 1/0.31 = x3.226 (the caption says 3.2).
- Inputs (VERIFIED, read from the JSON): best-Lambda S = 861.2 (E200, 5 keV, k=11/200), 87.19 (E500, 5 keV, 16/200),
  3.398 (E1000, 5 keV, 12/195), 0.2947 (E1500, 3 keV, 14/200). **All four are full-chain reruns (`replaced_by_a2fc`
  = true)**, not fast-path points; the best-ratio point (E200, 1.5 keV, 9/200) is not among them.
- **Reproduced: VERIFIED.** I imported `s95`, `yields`, `reach` from `ch29_checks.py` (pointing `SUMMARY` at the repo
  path) and recomputed all 32 cells: identical to the table. Also s95 = 3.00, 4.11, 8.08, 12.55, 21.37, 63.72, 197.7,
  621.5 (sigma 0); 12.8 at B = 10, sigma 1. Script: scratchpad `reach_recompute.py`, <1 s.
- Assumptions to carry into the v2 figure: same B at every mass and Lambda although each hypothesis has its own fallback
  selection (so the curve is an envelope, not one analysis); best Lambda per mass (at fixed 1.5 keV the B = 0 reach is
  923 GeV, ch29:210); B is the **median** background of a single bin, sigma_ln its log-normal width; no signal
  uncertainty (E1000 with 12/195 gives a B = 0 reach of 972-1079 GeV at 68%, ch29:210); K-factors transcribed, f_200
  +-13%; barrel; Fig. 29.4b curves end at B = 1.92e5, 2635, 997 and 2.01e6 (endcap) (ch29_checks.py:251).
  For v2: if the v2 background is quoted as B84 or with a different selection than the fallback, the signal row must be
  recomputed at that selection, or the marked point is not on this curve.

## 4. `book/checks/`

All five scripts recompute numbers of their chapter from tracked study files and grep the chapter text and the study
records for quoted strings; each prints PASS/FAIL per test. CSV columns: `value, meaning, source_path:line`; there is
**no tag column**: tags are written into `meaning` as "ESTIMATE"/"UNVERIFIED"; untagged rows are values read from a
tracked file (the book's "measured"/"logged").

| script | checks | inputs | runs today? (VERIFIED, run with the v2 pixi env, niced, <2 s, <0.32 GB) |
|---|---|---|---|
| ch25_checks.py (346 lines) | the followed event (row, cuts, w_core, Delta t), N_exp chain, costs, Table 25.2 record | STAGE4_SUMMARY.json, STAGE3_INDEX.json, C12FC_v1/{acceptance.json, signal_obs_a2.npz, signal_rows_a2.npz, event_display.npz}, xsec.json, frozen_inputs.json, V46_REVERT_SET.json, jobs/C1a.json, P2_points.json | **Yes, as is**: 94 PASS, 0 FAIL (paths relative to the repo) |
| ch26_checks.py (492) | thickness ratios, window table, efficiencies, full-chain sign tests, handles | P1/P2/P2_points/V2b.json, STAGE4_SUMMARY, edges_det, sep_it_det, signal_eff, cmp_all.txt, npz files | Only after replacing the hard-coded `/Users/jochoafl/...` path: 147 PASS, 0 FAIL |
| ch27_checks.py (356) | budget, closure z, trend, routes, DIF bound, ladder, eq. 27-nature, limits | STAGE4_SUMMARY, C12FC_v1/{bsum_wp, background}.json | Same path fix: 139 PASS, 0 FAIL |
| ch28_checks.py (498) | CPU bill, calendar, Table 28.3, k_need, remedies (Fig. 28.5), sideband example | STAGE3_INDEX, STAGE4_SUMMARY, bsum_wp, jobs/*.json, LOG.md, plus **`book/answers/ch28.tex` and `book/figure_src/ch28/remedy_gains.py` (not tracked)** | **No**: FileNotFoundError on book/answers/ch28.tex before any test |
| ch29_checks.py (453) | s95/reach (Table 29.2), break-even, map counts, audit rows against ~90 record strings | STAGE4_SUMMARY, signal_eff, bsum_wp, P1.json, external_bounds.json, many TT .md, `stage2_C001_quirks/phase1_strategy/outputs/STRATEGY_DRAFT.md`, **`book/answers/ch29.tex`, `book/figure_src/ch29/exclusion.py` (not tracked)** | **No** as is. With the path fixed and the answers file stubbed: 52 PASS, 0 FAIL, then stops at the missing exclusion.py (test 262). The Table 29.2 tests (4) pass. |

All study inputs listed exist in the repo (VERIFIED by a path scan). Work copies are in the scratchpad only.

CSV tag counts (VERIFIED, grep of `meaning`): ch25 111 rows, 3 ESTIMATE, 2 UNVERIFIED; ch26 98 rows, 8 ESTIMATE; ch27
123, 2 ESTIMATE; ch28 147, 30 ESTIMATE, 4 UNVERIFIED; ch29 174, 17 ESTIMATE, 1 row mentions "ESTIMATE on prongs"; in all
653 rows, ~60 ESTIMATE, 7 UNVERIFIED, the rest sourced. UNVERIFIED rows: ch25 crash rate ~1/700 and the 93% vertex
efficiency; ch28 cloud trial ($300, 90 days, 8 vCPU, 110 CPU-h), cloud cost $31-120, open-data pile-up 10-60, Run-3
skims. Key ESTIMATE rows: N_trig as physics (5% veto loss); 23-30 um resolution; 1/0.87 and 910-950; 23 of 33 points;
3.2/250 and 16/6.9/48 (endcap, ours); the reach table and curve ends (ours); 0.22 nuclear factor; 0-2/4-5 decades
(stale); sideband 8.2e8/1.7e4/0.17/1.6/1.8e6 (ours); most of Table 28.3 rows 2-7.
Minor CSV/script mismatch: ch29_numbers.csv gives curve end 2633, script tests 2635 (1% tolerance).

## 5. Plan numbers traced (section of the plan -> source)

Traced and consistent (VERIFIED = I recomputed or read it in the source file; otherwise the book line is the trace):
- PLAN:66-70: 23 rungs, 0.11, N_trig 4.08e7, 2.7e-10 (VERIFIED arithmetic 0.011/4.08e7), 1.23e6 at R09, 7.05 decades
  (VERIFIED log10(1.23e6/0.11) = 7.05), 790, 9/200 (VERIFIED in STAGE4_SUMMARY), bounds < 180 GeV (FASER exp+1s 180,
  obs 172: ch29_checks.py:257).
- PLAN:75-83: 1.14/M, M = 500-2000 (ch27:84, ch29:42); closure 1.50/1.61, z +52.8/+59.4, x2.41 (VERIFIED 1.500 x 1.606
  = 2.409), factor 117 (ch27:74).
- Table 1 (PLAN:100-103): 3.4e4 CPU-h, two decades (Table 28.3 row 7); $1500 (ch28:200, ESTIMATE); 1e9 vs 4.8e4 trials,
  3e6 CPU-h (ch27:146; VERIFIED 1e9 x 42.3 s / 4 roads = 2.9e6 h); 35x (VERIFIED 1.14 x 1.196 x e^1.05 / 0.11 = 35.4);
  k_need 1.1e7, 4e9 CPU-h (ch28:152-156).
- Table 2 (PLAN:117-126): = Table 29.2, VERIFIED (§3). "B = 10 costs 160 GeV" (PLAN:366) = 1026 - 866.
- Assets (PLAN:147-187): MS floor 10-28 um, crossing 1.2-1.9 keV (ch29:125; ch29_checks.py:308-310); +6.5%, 9 of 30
  (§1 items 4-5); eps 0.085-0.31, loss 0.83, window 1.0-1.2 / 4.7-6.6 keV (Table 26.1); 4.9 decades (ch27:122);
  1e8-3e9 events, 2-35x nature (ch29:42, ch27:187); M_est 2.26 m_Q and 19% below 0.5 m_Q (VERIFIED in STAGE4_SUMMARY
  `M_est_over_mQ_pooled`: 162/850 = 0.1906; the book quotes 29% below 1.5 m_Q instead); 1026 / 665 / 586 GeV
  (VERIFIED, ch29_checks functions; 665 and 586 also ex. 29.2); Knapen 650 GeV (TT:paper/sections/10_bounds.tex:21,
  ESTIMATE; not in the book).
- Work plan: 46 GB, Linux port (ch28:203); 50+50 brute force, V4-5 NOT RUN (ch28:279, ch29_checks.py:418-419);
  1.5-12 ms/event (ch28:50); 4.7-9.4 mm (R07/R08 cuts, Table 25.1); 1.7e5 from 500 events (VERIFIED 6.2e7 x 1.14/500
  x 1.196 = 1.69e5); 0.4 TB vs 128 GB, R03 records (ch28:117); f_corr 1.196 (ch27:69); trend width "2 to 6.3" (eq.
  27.trend gives 1.99 at R11 and 6.32 at R23, VERIFIED arithmetic); 0.17 (ch28:215); 1.4 h material run (Table 28.3);
  x2.3-7.3 (ch25:84); 21 terms (ch28:156); sigma_ln 2.3 -> median 0.011 (ch27:27); 1/0.87, 9 of 200 (ch26:115, ch27:156);
  f_200 +12-15%/-11-13%, QED 15 CPU-h (ch29:53, :65); 69%, 866 -> 1062 (ch29:97, Table 29.2); 1.0-1.3 seeds, timing
  1.5 (ch29:109); merged rung ~1 week (ch28:256); 371 CPU-h, 64%, 12-30 CPU-h (ch28:45, :281); rho=3 128 h, 0.6 decade
  (Table 28.3, ch28:267); 168 CPU-h/day (ch28:111); 3-5 cents/vCPU-h (ch28:200).
- Outcomes (PLAN:502-504): "near 800 GeV" (B = 10, sigma 1: 796), "about 500 GeV at B = 100, sigma 1" (495). VERIFIED.

**Could NOT trace** (in the book or UNR):
- "signal x1.5 to 3.2" for the endcap (PLAN:379): the book gives x3.2 at g = 1 and x2.1 at g = 0.5 (ex. 29.3); the
  lower end 1.5 has no source.
- P1 numerics 0.104 / 0.105+-0.002 (PLAN:150) trace to TT:paper 03:194 (the very line UNR item 7 calls mislabelled),
  not to the book; "holds per event on 2.2e5 events" (PLAN:151) conflicts with the book: 218,571 is the whole
  production, "not the sample that tests the law" (ch26_numbers.csv:3); the law was tested on 5 points x 300 events per
  Lambda (ch26:11).
- "1.5% population gate (+2-3%)" (PLAN:154): the values +0.70/+2.00/+1.07/+2.10/+3.15 are in TT:LOG.md (string tested
  by ch29_checks.py:430); not in Part VI text.
- "M = 500 to 2000 ... nature produces 1e7 to 1e9" (PLAN:76): plausible (4.08e7 x 30.3 = 1.2e9 vertex pairs), not stated.
- All costs in pd, the CPU table (PLAN:415-431), B1 gains "4-6 decades", S1 "400-600 CPU-h" (the book: ~300 h fast path,
  ~390 h with full-chain points, ESTIMATE ch28:147), timeline: plan ESTIMATEs, no book source.
- N1 "earlier studies used PU 50 or none" is only partly traced (Knapen at PU 50, ch28:236).

## 6. Contradictions and open questions

1. **"Rows 1 to 4 of the book's ranking go into one freeze" (PLAN:408).** Table 28.5 rows are: 1 data anchor, 2 counting
   as the estimator, 3 signal yield, 4 m_Q/Lambda at PU 200. Row 1 cannot be done in a simulation-only v2 (plan's B5 is
   only its simulated stand-in); row 4 is S5 "Could, not required" (PLAN:384-386). The book's own freeze list (ch28:284)
   is "the conditionals, the late-hit credit, the merging-tolerant rung and an endcap ladder". Strategy must restate
   what goes into the single v2 freeze.
2. **Late-hit credit is missing from the plan.** Row 2 and Table 29.1 credit prompt SM/single-interaction terms with the
   pile-up late fraction (~1e-4 per window edge; "up to 4 decades in that category", ch28:277). PLAN B3 credits the shape
   rungs R15-R20 and a vertex veto, not this. Decide whether v2 includes it.
3. **B84 ~ 0.17 is not a "systematic floor" usable as a width** (PLAN:342-343). In the book it is the B84 of an *empty*
   sideband in **real data** with 8.2e8 trials and an assumed transfer width 0.47 copied from a CMS search; its width is
   sigma_ln = 1.105. A simulation closure test at R04-R07 with 20 roads on the existing samples (~1e5 trials) cannot
   reach that, and 8.2e8 simulated roads cost 1.8e6 CPU-h (ch28:217). The width that would enter the reach is ~1.1, not
   0.17. The plan's sentence needs rewording.
4. **N8 / PLAN:178 states "out-of-plane resolution (23-30 um) equals the MS floor" as a negative result**; the 23-30 um
   is a planning ESTIMATE never measured (ch26:24), and plan.md:496 mislabels it (UNR item 19). Present as an estimate.
5. **P1 "holds per event on 2.2e5 events"** contradicts ch26_numbers.csv:3 (see §5). Also the book says the slope is
   confirmed "in the median over events", while ch29_numbers.csv:173 says "agrees per event"; the paper wording must follow
   the book (ch29:218).
6. **Reach-table assumptions vs v2 use.** Table 29.2's S is the signal at each hypothesis's *fallback* selection at
   Lambda = 5 keV (3 keV for 1500), all full-chain. A v2 background estimated at a v2 selection (e.g. a deep rung or T2's
   chosen selection) is not on the same curve unless S is recomputed at that selection; also the plan marks
   "B = 0: 1026 GeV" while the best-ratio hypothesis (1.5 keV) gives 923. The v2 figure must state which B (median, not
   B84) and which selection. Blinding: recomputing S at a v2 selection is a v2 signal efficiency; it must wait for the
   closure verdicts. The v1 values used here are public to the study.
7. **Book review status.** UNR:7-16: no part passed; Part VI fixes of round 9 unchecked edit by edit. Numbers the plan
   takes from ch28:267, ch29:218, ch29:224 are in that unreviewed set (the 0.6 decade; the c-window wording; the failures
   list). I re-derived the reach table, 0.17, 35, k_need, 2.41, 7.05 and the 0.966/0.975 values; the 0.6 decade and the
   Fig. 28.5 sums I did not (they need the untracked `figure_src/ch28/remedy_gains.py`).
8. **Book checks are not reproducible from the tracked tree**: ch28 and ch29 need `book/answers/` and `book/figure_src/`,
   which README.md:13 says are not in the repository; ch26-29 hard-code a macOS path. If v2 remakes Fig. 29.4b, it
   should vendor `s95`/`yields`/`reach` (ch29_checks.py:25-79, no other dependency) into `analyses/quirks_v2/`.
9. **f_200 eta cut** (item 1): two code paths exist (inv_norm_f200.py with |eta|<4; xsec.json f_tail without); the
   difference is <0.02%, so it is wording only, but v2 should define f_200 once.
10. **Open for the strategy:** which of UNR items 4-6, 10-12, 14-24 enter C3 (the plan names only seven); whether the
    erratum for v1 frozen files (items 3, 14-19, 20-22) is one `ERRATA_v1.md` in `analyses/quirks_v2/`; whether v2
    models vertex identification (item 2); the source check needed for items 9 and 13 (Barbashov 1977, Knapen et al.
    Sec. III.D) before the paper text is rewritten.
