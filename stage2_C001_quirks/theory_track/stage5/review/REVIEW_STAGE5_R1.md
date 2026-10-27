# Stage 5 final figures — critical review R1 (fresh reviewer, 2026-10-16)

Scope: stage5/figures/final/ (38 det + 8 truth ×2 label variants), make_figures.py, plotting.py, FIGURES_FINAL.md,
external_bounds.json, EXTERNAL_BOUNDS.md. Inputs read-only: data/acts_stage4/analysis/C12FC_v1, STAGE4_SUMMARY.json,
acts/stage4/STAGE4_RESULTS.md.

Status: COMPLETE. Verdict at the end.

## Findings

### Verified so far (evidence)
- D1 rfb cell values = limits.json `s_T + s_G` = STAGE4_SUMMARY `fallback_points.eps_rfb` (e.g. E500 1.5 keV 0.045+0.025 = 0.070;
  E200 1.5 keV 0.045). SR-G bin is the complement of SR-T (eps_rfb = eps_SRT + s_G), so the sum is not a double count. OK.
- D1 R_A/R_D/R_E cells agree with D2 rung curves (E200 2 keV: R04 0.225, R08 0.055 = R_C, R14 0.025 = R_D, R23 0.005 = R_E). OK.
- D5/D6/D7 best ratio recomputed: E200 1.5 keV mu95_toys = 1.2458e7, N_exp = 14901.1/0.045 = 3.311e5 -> 37.62 (STAGE4_SUMMARY 37.6226). E200 2 keV 39.07;
  E1500 3 keV 1.613e7/24.95 = 6.46e5; S500 3 keV 3.15e4; E1500 0.85 keV map cell 1.01e7; E1000 0.6 keV 2.97e5. All match the figures.
- D4 B1_per_trial R01 = 3.25e4, R04 = 171.6 (background.json columns); closure T1 ratio 1.500, R05 1.606 (ratio panel). OK.
- External bounds spot-checks (downloaded fresh into scratchpad):
  - HEPData ins3184325 t2 (FASER): observed m_max 57.32/113/162.58/172/179 GeV at 0.3/1/3/5/10 keV, expected 56.33/160.46 — identical to
    external_bounds.json. Header N_IC = 2, 13.6 TeV, 186.3 fb^-1. FASER abstract: charge ±1, no QCD colour, 300 eV < Lambda < 100 keV. OK.
  - Farina–Low 1703.00912 Table II: fermion (1,1)_-1 Nc=2 650 / 150 / – GeV; scalar 350 / 60 / –; Nc=5 fermion 30 GeV at 1 keV. Matches JSON
    and the md cross-check text. OK.
  - D0 1008.3547 abstract: 107 GeV, Lambda 10 keV – 1 MeV, charged quirk. Matches. ("probable" match to E is an honest tag.)

- D7: min sigma95/sigma_th = 37.6 (E200 1.5 keV); min over the -1 sigma toy edge = 2.6 (same cell) > 1, so "no crossing at the -1 sigma edge" holds;
  mu_5sigma non-null at exactly 13 E cells, mu_5sigma/N_exp = 9.1e2 ... 4.1e7. Matches the in-figure text.
- D9 truth upper comparator recomputed from STAGE4_SUMMARY cited_investigations.truth_degeneracy (linear in ln Lambda at f = 0.5):
  F500 4.875, F200 5.142, F1000 4.478 keV. Matches the sidecar. A1 upper edges 4.70 (E200) to 6.60 (Etilde500) keV. Legend says "post hoc". OK.
- D10: 77 A1 points + 45 PU-200 points (sidecar), PU 200 labelled "NOT MEASURABLE (flag)" and kept out of the ratio panel. OK.
- D8: no (key, row) collisions across src_file in signal_obs_a2.npz (so one-entry-per-event dedup is right). First entry per row = lowest cand index (100 %).
- Bookkeeping: 38 det PNG + 8 + 8 truth PNG; 54 sidecars with 0 stamps, 0 missing inputs and experiment_name_or_logo = false; index.json all 11 ids OK,
  final_checks pass, freeze_match = true. Truth vs truth_sqrt_s sidecars differ only in the right label; both carry the truth-level tag.
- Labels: every PNG viewed shows "Private work (simulation)" and the approved right label; no CMS name/logo as experiment label; every truth figure
  has the "truth level" tag. No figure shows a WP, an exclusion contour or a discovery claim; D3/D5/D6/D7 state "no WP / §8 fallback" in-figure.

PNGs viewed: all 38 detector-level, all 8 in final/truth/, and 2 of 8 in final/truth_sqrt_s/ (T1_F_m500, T4; the other 6 were checked through
their sidecars: same inputs and code, only the right label differs).

## Executor's open questions

### (1) D8 M_est bimodality — the figure is honest about the data, but the caption misreads the cause
The gap near m_Q is not an anomaly: it is the kinematic threshold of the estimator. In acts/stage4/analysis/signal.py l.203,
M_est = |MET| cosh(eta) / (beta gamma)_ToF, which is |P_pair| / (beta gamma) — a pair-mass proxy with M_QQ >= 2 m_Q. In the plots the upper cluster
starts sharply at 2 m_Q (clearest in D8_mest_RA_F1500: nothing between ~1.2 and 3.0 TeV; the cluster starts at 3.0 TeV). Without PU it never goes below
about 2.3 m (STAGE4_RESULTS §6.3: A1 q16 = 467/1046/2026/3101 GeV for E200–E1500). The low cluster (0.1–0.4 m) appears only with PU and comes from
in-time PU BTL hits giving beta near 1. So the figure has two clusters (PU-faked low beta gamma, and pair mass >= 2 m) and nothing at m_Q by construction.
The current text ("gap around m_Q is not investigated") and the prominent "true m_Q" reference line suggest that M_est should peak at m_Q. See B1.

### (2) D11 fake along the signal's MET direction — by construction along ITS OWN road, so the overlap is a coincidence, not a bug
- B1 trials (acts/stage4/run_stage4.py l.379–380, 402–403): phi_MET(trial) = phi0 + road * 2 pi/roads with phi0 = rs.uniform(-pi, pi) per event.
  The finder searches a road of half-width delta95 = 0.15 rad (acts/stage4/frozen_inputs.json) around that phi. So any PU-only fake candidate
  lies along its own trial's MET direction by construction.
- The fake's own direction is stored: data/acts_stage4/prod/C2/B1/B1_00201.npz trials.phimet[28] = 2.2974 rad (ev 5032, road 0). The signal MET is
  phi = 2.3146 rad (event_display.npz met_phi). The fake hits' median azimuth (r > 100 mm) is 2.284 rad. So delta phi(fake road, signal MET) = 0.017 rad.
  The two directions are independent random draws (B1 phi0 uniform; signal MET from hseed('sig-pvmet', ...)). The near-alignment is a chance
  coincidence (a few per cent for "looks aligned" within about 0.1 rad), not a property of the figure code. products.event_display()
  (acts/stage4/analysis/products.py l.191–206) dumps the fake hits in the lab frame with no rotation, so there is no hidden re-alignment.
- Why met_phi = null for the fake: products.py l.205–206 looks up dj['tr']['trials_phimet'], but the tr dict built by background.to_g3_job()
  (background.py l.33, 40) holds keys without the "trials." prefix, and TR_KEYS does not include 'phimet'. The key can never be found
  (upstream Stage-4 cosmetic bug; read-only here). See B2.

## Category A
None. No number in the figures or the catalogue differs from STAGE4_SUMMARY / limits.json / background.json / edges_det.json / external sources by
more than rounding (all spot-checks above). Nothing implies a WP, an exclusion or a discovery. The D11 alignment is not a bug.

## Category B (should fix before the figures go into the final note; all cheap, no re-run of Stage 4)

**B1 — D8 (all 10 files) + FIGURES_FINAL.md §D8: the M_est caption/reference lines misread the bimodality, and one statistic is at the wrong level.**
- Problem 1: "The gap around m_Q is not investigated here" and a "true m_Q" line drawn as the first reference imply M_est estimates m_Q.
  M_est is a pair-mass proxy with a hard threshold M_QQ >= 2 m_Q (see (1)). The emptiness near m_Q is expected.
- Problem 2: the catalogue quotes "20 of 8 934 entries (0.2 %) in 1.3–1.7 m_Q, median 2.23". That is candidate-level (all matched candidates at R04,
  about 10.9 per event). The figure plots one entry per event: N = 850, median 2.26, 3 events (0.35 %) in 1.3–1.7 m_Q, 19 % below 0.5 m_Q.
- Problem 3: for Etilde500 the 3 m_Q range puts 50–70 % of entries in the overflow bin (D8_mest_RA_S500, D8_mest_rfb_S500). The "pair-mass" cluster is
  mostly invisible there.
- Fix:
  - Relabel the 2 m_Q line "2 m_Q (M_QQ threshold)". Either drop the m_Q line or label it "m_Q (not the M_est scale)".
  - Replace the caveat with: "M_est = |P_T^miss| cosh eta / (beta gamma)_ToF estimates the pair mass M_QQ >= 2 m_Q (A1, no PU: q16 ≈ 2.3 m). The low
    cluster at 0.1–0.4 m appears only at PU 200 (in-time PU BTL hits, beta → 1). Nothing near m_Q is expected."
  - Quote the event-level numbers that match the plot, or say "candidate-level" explicitly.
  - Use hi = 4 m_Q (or a log x axis) for Etilde, or for all panels.

**B2 — D11 + FIGURES_FINAL.md §D11: the caveat "not determined" can be resolved, and the overlay misleads without the fake's own road.**
- Problem: the reader sees a single MET line and concludes that the fake follows the signal MET.
- Fix:
  - Read phi = trials.phimet[28] = 2.297 rad from data/acts_stage4/prod/C2/B1/B1_00201.npz (read-only), or take the fake hits' azimuth.
  - Draw it as "MET road of the fake trial (±0.15 rad)", for example dotted in the fake's colour.
  - Replace the caveat with: "The fake lies along its own trial's MET road by construction (road ±δ95 = 0.15 rad around a uniformly random φ).
    Its road is 0.017 rad from the signal MET: a chance coincidence of two independent events."
  - Optionally report the upstream key mismatch (products.py looks for 'trials_phimet'; TR_KEYS omits 'phimet') in UPSTREAM_FEEDBACK.

**B3 — D2 (5 files), D3, D4: the rung axis has no rung numbers, but the in-figure text, the catalogue and the report refer to rungs by number**
(R04, R08, R09, R14, R23). For example, the D3 tag "minimum B84 … at R09" and the D4 tag "rungs ≥ R08" cannot be located on the axis without counting
ticks.
- Fix: use rung_label(name, short=False) (it already exists in plotting.py) so the ticks read "R04 N_IP2≥7". Alternatively add R-numbers at the
  family boundaries.

**B4 — D9: the right-aligned tag block runs out of the axes.** The line "A1 upper edges ×2.7–3.5 lower): not drawn, STAGE4_RESULTS §6.1" starts left
of the y-axis spine and overprints the frame.
- Fix: break the lines shorter, or move the block to 'upper left' below the legend (the 10–100 keV band is empty).

**B5 — D4: "factorisation model" ≡ "B1 direct" at R01–R07 by construction.** background.json columns show P_fact == B1_per_trial exactly wherever
B1_groups > 0 (e.g. R04 171.554). The diamonds sit on the dots, which reads as independent agreement (a tautological-comparison look, JFC 03-review
§6.4). The closure panel correctly uses the thinning prediction (N_pred = P_thin × 48 000 = 5.49e6 at R04).
- Fix: label it "factorisation model (= direct where B1 > 0; extrapolation from R08)", or draw it only for rungs ≥ R08. Say the same in FIGURES_FINAL §D4.

**B6 — EXTERNAL_BOUNDS.md is stale relative to the final set.**
- l.7 says the output figure is figures/placeholder/D7_exclusion_map, stamped PLACEHOLDER.
- Caveat 1 (l.89) speaks of "the C1 placeholder grid".
- The overlay is now in the final D7 (real C12FC_v1 grid, frame about 126–1840 GeV / 0.39–6.5 keV; the numbers are still right).
- Fix: point to figures/final/D7_exclusion_map and drop "placeholder". The data content (external_bounds.json) is correct; see the spot-checks.

## Category C (optional)
- C1 D5/D6: the y ranges carry 4–6 empty decades below the data (ylim = min/1e4 … max·1e6; D6 min/1e5). Tighter limits would make the gap to
  N_exp / sigma_th easier to read. The legend needs only about 2 decades of headroom.
- C2 D5/D6 (E200 and the 0.6–1.5 keV slices): the −2σ toy band edge drops below N_exp / sigma_th. That is correct and not an exclusion, but a
  caption sentence ("the −2σ edge crossing is not an expected exclusion; the median is ≥ 37.6×") would pre-empt misreading.
- C3 D4 tag prints a Python bool ("trend significant: True"). Write "yes", or quote z.
- C4 D10 carries the "PU 200" right label while the coloured content is A1 (no PU). The in-figure tag says A1 = no PU; acceptable under the approved
  convention.
- C5 D7 tag names "CMS HSCP recast" and "CMS out-of-time recast" as external limits. This is correct citation practice, not an experiment label.
  Consider "HSCP recast (Farina–Low)" to avoid any visual association with the "no CMS name" rule.
- C6 T1_F_m200: Δs_B is absent at ≥ 7 keV, and the quadrature/linear curves stop at 5 keV (data-limited). Add one caption line.
- C7 D2: the lower 1.5 decades are empty (ylim = ymin/300). Harmless.
- C8 EXTERNAL_BOUNDS.md: "PRL 2026" for arXiv:2607.26195 could not be confirmed (the arXiv abstract page confirms the title, the 186 fb^-1,
  charge ±1, no colour and 300 eV < Λ < 100 keV). Cite as the arXiv e-print unless the journal reference is checked.
- C9 Truth figures: the full right label "PU 200, 3 ab^-1" on truth-level quantities remains the default until the user chooses. The √s-only
  variant is ready and correct.

## Verdict
**ITERATE** — 0 Category A, 6 Category B (B1–B6), 9 Category C. No correctness error was found. All spot-checked numbers match their sources, and the
labelling, the no-WP state, the toy-primary bands, D9 "post hoc" and D10 "NOT MEASURABLE" are as required. The B items are presentation and
documentation fixes (D8 interpretation text and range, D11 road overlay and caveat, rung numbers, D9 text overflow, D4 tautology note, stale
EXTERNAL_BOUNDS.md). The verdict rule for this loop is PASS only with C findings alone. A re-review after the fixes can be light (visual check of D2–D4,
D8, D9, D11 + the two .md files).
