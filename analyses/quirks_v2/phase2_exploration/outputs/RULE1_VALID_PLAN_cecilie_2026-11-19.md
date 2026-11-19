# Plan: validation of the preliminary rule-1 reading, items (a), (c), (d)

Cecilie (Fable 5.2, executor, rule 1(c)), written 2026-11-19 15:32 -05 (`date`), **before any pilot or C1 array was
opened** (read so far: documents, code, directory listings, campaign JSONs, Tove's counts JSON). Björn does the
independent code review and the ceiling cross-check (b, e); not duplicated here.
`STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`; `TOVE` = `RULE1_PRELIM_tove_2026-11-19.md`.

## (a) Positive control of the B1 path of `p2t_classify.py` (unchanged, sha256 recorded in the result)

- **Sample:** the C′₀ no-pile-up events of campaign p2-a-c1-cp0 whose hit rows were stored (`cp.toyev.<g>`,
  `cp.toytru.<g>`): DIF (preselected events of 50,000), NI 22 mm (preselected of 30,000), and the first 500 events of
  the γ, V⁰ and PV-pair guns. A converter (`p2w_cp0_to_pilot.py`, new) only re-packs those rows into the pilot record
  layout (`hits`, `hit_off`, `tru`, `evt` with `cls`, `phi_road` = the event's `phimet`, `pv_*`; stream name
  `ctl.cp0.<topo>`, 21 road orientations, `n_early_prod` = 0), float64 as stored. The files go through the non-Z
  branch of `p2t_classify.py`, i.e. the code path of the seven B1 classes, with `--ckf-pass-all` (an existing option).
- **Known counts:** the same files hold the output of v1's unchanged path (`run_g1b.run_cp0_job` →
  `production.process_trial`, after CKF, channel (i)'s campaign): `trials.n_pass[:, r]` = number of aligned candidates
  passing rung r, per event. Link to channel (i)'s published numbers: n_pre must reproduce 47,538 (DIF) and 22,794
  (NI 22) of `c1_compare_mattias_2026-11-19.json`.
- **Statistic (fixed now).** Per event, the number of candidates passing R04 and R05 from `p2t_classify.py` (variant 1
  = CKF-flagged rows removed, orientation 0; rung logic of `production.full_set_flags`: N_IT2 ≥ 3, N_IP2 ≥ 7, w_core <
  37.5 mm) against `trials.n_pass` at R04, R05. D = number of events where either differs.
  **PASS iff D = 0 for DIF and for NI 22, and the reference has ≥ 100 events with an R04 candidate in each** (otherwise
  "no power", not PASS). R01–R03 and R06–R08 and the gun topologies are compared the same way and reported
  (information). Any D > 0 is FAIL and the events are listed; I do not tune anything to remove a difference.
- Information only: the same with the rows stored as float32 (the pilot's storage precision) on one DIF slice; the
  variant-0 (before CKF) counts next to variant 1. C′_PU is **not** run: its known counts are attributed counts under
  pile-up with top-up, which `p2t_classify.py` has no code for; a comparison would test my additions, not the script.

## (c) Width-only subset-pass classifier (STR l.755-761), new script `p2w_subset.py`

**What the frozen text fixes:** own hits of the term, all of them, before CKF (Df-9); planes ("ribbons") through the
PV; search region = road (|Δφ(n₃, MET)| < 0.15) and barrel (|η(n₃)| < 1); for rung r the subset of the width of r
with the most double-crossing layers; k_IP = max(0, n_IP − N_IP2), k_2S = max(0, n_2S − N_2S2), k = k_IP + k_2S;
m counts events (× orientation) with k ≤ k_max = ⌊n/2⌋; the finder's seeding and grouping are not used.

**What it does not fix, and what I code (my readings, listed for the orchestrator; none is an amendment):**
- S1 *plane and membership*: the finder's own (README step 3, kernel `kernels.refit_packed` called unchanged with the
  full pre-filter scan): hits within 3σ_tot of a PV-constrained plane, forward of the PV, |u·n₂| < W_c = 75 mm, 3 refit
  iterations, alignment cuts on the final axis.
- S2 *which planes*: every pair of road hits on two different IP layers (sin∠ ≥ 10⁻³) is a seed; no seed score, no
  Δφ/Δη seed cut, no merge of near-equal planes. (The finder: L4–L3 pairs with an L2 hit and seed N_L2 ≥ 4.)
- S3 *"width of r"*: the rung variable itself, w_core = 1.4826 × MAD of u·n₂ over the IP hits of the subset (same
  formula as `kernels.cand_vars`), required < W_r, maximised over subsets of the plane's hits; 2S hits do not enter
  w_core and are all kept. This is the only reading under which the finder near-pass count is a lower bound (advisor's
  reading (ii)) and under which the cut is monotone under added hits (STR l.776). A hard window is NOT coded.
- S4 *subset search inside a plane*: the full hit set first (the finder's choice); else for every window centre (each
  IP hit and each midpoint of neighbours) the hits inside ±W/1.4826, then layers completed with outside hits, cheapest
  layer first, each addition kept only if the actual w_core of the subset stays < W. Every subset found is a witness;
  the search is not proven maximal, so **m_sub is exact or a lower bound** (valid for "above", like Tove's).
- S5 *N_IT2 ≥ 3* (Tove's A2): primary **(S)** no separate requirement: at n_IP = 7 a missing IT layer is a missing IP
  layer and is in k_IP ("is part of k_IP"); cross-check **(F)** N_IT2 ≥ 3 required of the subset (the finder's
  loose-store convention, comparable with Tove's (N)).
- Pool, PV, weights, M, flagged events, orientations: exactly Tove's (merged pool, variant 0), so that only the
  classifier differs.

**Outputs:** per (event, orientation) the smallest k at W = 37.5, 18.75, 9.4, 4.7 mm for s = 0 (n = 7, k_max = 3:
R05…R08 = R09 = R11) and s = 3 (n = 10, k_max = 5: R14 = R17 = R20, FB), readings (S) and (F). m_sub per term; B₅₀
with `p2t_rule1_prelim.py` unchanged (R09, R08 at 88/118/148), where a pile-up estimate exists (s = 0), with/without
flagged events. Exact event-level prefilter (in numba): a road needs ≥ 4 double IP layers, or ≥ 5 double layers.

**Tests before the real read (synthetic, committed with the script):** T1 two straight lines in a plane, all layers
→ k = 0 at every width and variables equal to `kernels.cand_vars`; T2 removed layers → exact k (s = 0, s = 3); T3
narrow pair plus wide in-plane hits: finder fails the width, subset passes; T4 no L3/L4 hits (no finder seed) → found;
T5 axis outside road or barrel → not counted; T6 noise only → no pass; T7 adding random hits never raises k (200
trials); T8 on synthetic events every aligned loose finder candidate has k_sub(F) ≤ k_finder.
**Acceptance on real data (fixed now):** for every (event, orientation) of Tove's stored variant-0 candidates,
k_sub(F) ≤ k_finder at each of the four widths, s = 0 and s = 3. Violations = 0, else the classifier is reported as
FAILED and its m is not offered as binding. Expected then: m_sub(F) ≥ Tove's (N) per term and width (R08: Z 253).

## (d) Power of the exact shortcut (≥ 4 IP layers with ≥ 2 road hits)

`p2t_classify.py --check-prefilter` (existing option: finder on every orientation with ≥ 3 road hits) on samples that
produce candidates: (1) the control files of (a); (2) the 20 Z(νν) pilot files with the most stored candidates in
Tove's outputs. Statistic: n_lost = stored aligned loose candidates in orientations the shortcut skips, and the
candidate table with and without the option must be identical. **PASS iff n_lost = 0 with ≥ 300 candidate-holding
orientations checked** (95 % upper limit on the lost fraction 3/N ≤ 1 %); quoted per sample.

## Compute (ESTIMATE; workers through the runner, nice 10, ≤ 2 jobs per node on landau and schrodinger, jobs packed
by event count, ≤ 15 min target; SLOTS.md line first; no signal file; nothing installed)

| step | basis | CPU-h |
|---|---|---|
| timing slices (a), (c) | ≤ 3 min each | 0.1 |
| (a) 70,000 control events × 2 variants | finder ≈ 17 ms per call (Tove) | 0.3–0.8 |
| (d) control with the option; 20 Z files | 20/460 of Tove's 4.7 CPU-h | 0.5–1.0 |
| (c) Z(νν) 1.0×10⁶ events, 5–15 ms each | own numba kernel, to be timed | 1.4–4.2 |
| (c) B1, hs, lowpt 1.9×10⁷ events | prefilter in numba; I/O bound | 0.5–1.5 |
| **total** | | **2.8–7.6** |

**If a timing slice projects the total above 10 CPU-h I stop and ask.** If only the exhaustive seeding of S2 is too
slow, I do not restrict it silently: I stop and ask. Result file: `RULE1_VALID_cecilie_2026-11-19.md`.

## Addendum, 2026-11-19 15:54 -05 (after the read of (a), before the run it describes)

(a) as planned came out **NO POWER** at R04–R05: v1's own C′₀ output has no R04 candidate at all (DIF 0 loose
candidates in 47,538 events; NI 22: 17 events with a loose candidate, none at R04; guns 0), D = 0 at every rung. The
criterion stays as written (not PASS). To have a control of the B1 branch with candidates at R04–R08 I add **(a2), an
injection**: the w > 0 events of the 20 Z(νν) pilot files of (d) are re-packed, unchanged, as a B1-layout file
(`p2w_znn_to_b1.py`: stream `ctl.znn.b1`, `phi_road` = the stored `phimet_reco_v1`, `pv_*` = the PV p2t_classify
draws for the Z branch, 21 orientations) and run through the non-Z branch of `p2t_classify.py` (unchanged,
`--no-ckf-pass`). Reference: Tove's stored variant-0 candidates of the same events (Z branch).
**Statistic: D2 = events whose candidate rows at orientation 0 (N_IT2, N_IP2, N_2S2, N_L2, w_core, p(χ²), n_core,
n_hit, Δφ, η, and the four hit-content counts) differ. PASS iff D2 = 0 with ≥ 100 candidate-holding events.**
This tests the B1 branch (event record, PV, orientation loop, storage) against the Z branch of the same script, not
against v1; the link to v1 is (a) (exact at the loose rungs, 17 events). ≈ 0.2 CPU-h.
