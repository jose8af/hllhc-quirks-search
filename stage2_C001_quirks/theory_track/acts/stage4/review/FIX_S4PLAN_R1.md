# Fix report R1: Stage-4 plan (`acts/stage4/plan.md`), C001 quirks theory track

Fixer R1, 2026-10-13. Inputs: `review/CRITICAL_REVIEW_S4PLAN_R1.md` (1 A, 10 B, 13 C) and
`review/CONSTRUCTIVE_REVIEW_S4PLAN_R1.md` (1 A, 8 B, 7 C). The plan was edited in place. New probe code is in
`acts/stage4/probes/f1r_*.py`; outputs are in `data/acts_stage4/fix_r1/`. No install, no change to `acts/pixi.toml`, no
production run.

## Headline: the blind signal-vs-PU margin (plan §2.4)

The search is blind and identical for signal and PU: per-crossing counting, W_c = 75 mm, t_tol = 30 µm, and every seed with
seed N_L2 ≥ 6 refitted. It covers central events with the barrel finder. The sample is 56 fresh PU-200 events × 4 roads,
plus 91 signal events overlaid row-major. Brackets are 68 % CL. Data: `data/acts_stage4/fix_r1/f1r_margin.json`.

| rung (N_IT2 ≥ 3) | PU, Fatras in-time (224 trials) | signal ≥ 1 keV, Fatras (79) | PU, OT topped up to the TDR (32 trials) | signal ≥ 1 keV, TDR-OT (14) |
|---|---|---|---|---|
| N_L2 = 10 | 0 (< 1.3 %/trial, < 5.2 %/event, 95 % CL) | 0.77 [0.72, 0.82] | 0.88 [0.79, 0.93] | 0.71 [0.55, 0.85] |
| N_L2 ≥ 9, χ²/ndf < 2 | 0.009 [0.003, 0.021] | 0.85 [0.80, 0.89] | 0.78 [0.68, 0.86] | 0.43 [0.28, 0.60] |
| N_L2 = 10, χ²/ndf < 2 | 0 (< 1.3 %) | 0.72 [0.66, 0.78] | 0.125 [0.066, 0.21] | 0.36 [0.21, 0.53] |

- **Fatras-only:** signal and PU are one layer apart. PU never reaches 10/10 (its best is 7-9), and χ² adds about ×13.
  With the R0 hit count the same PU candidates reach 10/10 in 152/224 trials.
- **At the TDR-normalised OT density (the honest case):** the layer count saturates and the separation shrinks to about ×3
  at the 10 % level (signal 0.36 vs PU 0.125 per trial). That is about 7-8 decades above the ≲ 3 × 10⁻⁹ per event needed.
  The IT top-up is not yet included and will make it worse.
- **What it means:** F0 alone cannot reach the target. The working point has to come from F1 (free-origin helix, opening
  linearity, dE/dx) and from the measured SR-T time factor. The feasibility is the main G3 question, with escalation to the
  user built into the WP rule.
- **Not separating:** |n_z| (PU 0.84-0.86 vs signal 0.77, medians) and Δw (window-filled).
- **Compute for this round:** about 5.5 CPU-h, over the ≲ 3 CPU-h asked. About 2.2 CPU-h went to 8 ρ = 2 trials, which ran
  at 400-1300 s each, and about 1 CPU-h to two discarded buggy first passes.

## Changes to approved decisions

Proposed changes need user confirmation. They are marked **PROPOSED** in the plan (§7, §10).

| # | What | Status | Recommendation |
|---|---|---|---|
| D4-10 → (a′) | Robust-shift treatment (critical B-9). Two-sided sources use max(\|up\|, \|down\|); one-sided sources stay one-sided; each family uses its own prescription (PDF, scale envelope); shifts are smoothed across Λ and ln m; the floor is max(\|shift\|, sd), never min. Worked example in §7 | **PROPOSED, needs confirmation**. Until then (a) stays nominal and (a′) is computed alongside | (a′), medium confidence |
| D4-13 (new) | P2 deliverables for m_Q and sensitivity (constructive B-6): velocity observables (β_ToF, dE/dx, M_est), `sensitivity.json` and a pyhf workspace | **PROPOSED, needs confirmation** (adds deliverables) | yes; ½-1 day, < 1 CPU-h |
| D4-14 (new) | Wide regime ℓ_max > R_IT, which lies below the F0 low edge by construction | **PROPOSED, needs confirmation** | (a) accept as a limitation now and decide after V4-3 at G2. (b), a new topology, costs about 1 week and about 40 CPU-h |

**Adopted directly** (inside the approved scope; they cut cost or risk; listed so the user can veto them):

| Change | Source | Effect |
|---|---|---|
| Layers count **crossings**: min(n_in, n_out) on stacked modules | critical B-2, constructive A-1 | a definition fix (it was an error) |
| No Δw cut. W_c = 75 mm from a physics rule. t_tol = 30 µm thickness tolerance (S-2 MS floor). The window axis is re-estimated from the hits | critical A-1, B-3 | F0 shape |
| WP rule: one ordered ladder; B₈₄ (log-normal) ≤ 0.3 for the WP rung and every tighter rung; one B sum; frozen at the start of G2 | critical B-6, constructive B-8 | implements D4-4; "+1σ" is now defined |
| Density ladder = exact interaction-count thinning. Closure tests T1-T3 with a lever-arm minimum, a factorisation test, and a failure path. ρ ∈ {2, 3 conditional} | critical B-4, B-5; constructive B-1 | implements D4-5 (a) |
| **The baseline PU density is normalised to the TDR** (top-up of ×2.3-7 per layer). Fatras-only becomes a cross-check | critical B-7 | more conservative B. The finder CPU at the normalised density is a new G2 risk |
| F1: free-origin helix, opening-linearity variable (replaces the crossing count), SR-T/SR-G timing categories, dE/dx | critical B-10, constructive B-2, B-3 | inside F1 (D4-4) |
| Row-major A2-A4 (one PU simulation per row, Λ loop in numpy) | constructive B-4 | about −100 CPU-h |
| k = 1 guns (PV pair, looper); NI toy at 3 radii; full B sum; SM extrapolation with closure | constructive B-5, critical B-8 | about +12 CPU-h |
| Gate order U-2 → G1 → G2 (freeze, then A1/V4-3) → G3 pilot (closure) → guns → production | constructive B-8 | risks fail early |

Compute: about 330 CPU-h recommended (about 365 if G3 needs ρ = 3) and about 160 lean, against R0's 450 and 210 (ESTIMATE, §6.2).
Disk: about 8 GB.

## Item-by-item

Status: RESOLVED = fixed in the plan, with evidence. PARTIAL = fixed as far as a plan can go; the rest is assigned to a named
gate. NOT ADOPTED = argued.

### Critical review

| Item | Action (plan §) | Evidence | Status |
|---|---|---|---|
| **A-1** Δw < 1 cm kills the signal | Δw cut and w_min removed (§2.2.6, §2.5.1). w_min is redundant with per-crossing counting. Δw (R0) and a robust core width are stored only. The other selection elements were re-checked | R0 probe signal Δw 11-34 mm. Truth-level fraction with Δw_old < 10 mm: 0.26 at E1000 1 keV (`review_r1/r1_truth_window.json`). Fix-R1: PU Δw 34-44 mm, signal 18-36 mm, so it does not separate (`f1r_summary.json`) | RESOLVED |
| B-1 R0 margin from a truth-assisted, asymmetric search | §0 and §2.4 re-tagged. New blind, like-for-like probe; full PU N_L2 and χ² distributions recorded | `f1r_finder.py`, `f1r_margin.json`, `f1r_summary.json` (best-N_L2 histograms, χ² quantiles) | RESOLVED |
| B-2 stacked modules counted twice | Crossings = min(n_in, n_out) on stacked layers (§2.2.5). §2.1 band occupancy re-derived per crossing. R0 count kept as a diagnostic | Fatras PU best: R0 count reaches 10/10 in 152/224 trials; per-crossing count never reaches 10 | RESOLVED |
| B-3 W_c sets the low edge | W_c = 75 mm = R_IT/2 from the physics bound \|u·n₂\| ≤ ℓ_max/2. Truth-level ε vs W_c table. V4-3 attribution to W_c/t_tol. Limitations listed; the (L3, L2, L1) "wide regime" claim withdrawn. Optional wide-regime topology → D4-14 PROPOSED | Bound holds in 95-100 % of central template events at 65 points. Acceptance ≥ f(ℓ_max ≤ R_IT) at W_c = 75 (`f1r_truth_window.json`). Signal information used: truth templates, only to verify the derivation | RESOLVED (D4-14 for the user) |
| B-4 power law; inconsistent ρ; reach | Exact interaction-count thinning, no fitted exponent; the ∝ ρ term is kept. ρ ∈ {2, 3 conditional} in §4.1, §5, §6. Reach rule plus the rung-factorisation fallback and escalation | Pilot: ρ = 2 → 1 prediction over 2.5 decades of thinning, conservative ×2.1-2.9, k ≈ 10-22 (`f1r_summary.json` → `closure_rho2_to_rho1_t0`) | RESOLVED (design). The closure is not yet passed and is assigned to G3 |
| B-5 closure gate and factorisation not falsifiable | T1/T2/T3 with a ≥ 1-decade lever arm; z statistic and pass condition; factorisation-correlation test in density bins; failure path = more statistics, then the upper envelope, then the user. No model shopping (§4.1.4) | Pilot T1 would fail at these statistics (z ≈ −3.8). The cause is identified as duplicate counting, and the convention is fixed before the freeze | RESOLVED (design). Pilot honest: PARTIAL evidence |
| B-6 WP rule and leakage | One ordered ladder; B₈₄ of the log-normal total ≤ 0.3 for the rung and every tighter rung; one B sum (planning split ≠ rule); freeze at the start of G2 before V4-3/A1; probe rows excluded (§2.5) | — | RESOLVED |
| B-7 wrong V4-2 references; density | Benchmark rebuilt from TDR Fig. 6.3 (occupancy) + §6.2.1 channel sizes + Fig. 12.3 (OT cluster size). Baseline PU topped up to the TDR; residual range as the systematic (§1.4, §8) | Fatras low by ×2.3-7 per layer; strip and macro-pixel readings agree (`f1r_density_bench.json`). The IT cluster size is not in the TDR (ESTIMATE) | RESOLVED (IT ratio ESTIMATE) |
| B-8 SM/NI/DIF closure, veto, B sum | SM uses the same thinning, closure and failure path. NI ESTIMATE at 22/30/61.5 mm: about 8/10/8 per event in the road, P(fake) ~ 10⁻⁴-10⁻³ before F1. DIF toy normalisation. Full B sum; k = 1 guns; missing samples via N_trig (§4.2) | arithmetic in §4.2 (X₀, λ_I from `s4geo.py`) | RESOLVED (rates ESTIMATE) |
| B-9 D4-10 ambiguous and anti-conservative | Rule (a′) with a worked example written as **PROPOSED** (§7, §10) | E1000 ℓ_max-edge example from `P2.json` | PROPOSED, needs the user |
| B-10 crossing count undefined | Replaced by opening linearity on IT + PS layers (resolvable by detector type); free-origin helix added (§2.3) | — | RESOLVED |
| C-1 roads not disjoint | Text corrected; per-event rate primary; n_eff from the bootstrap (§4.1.1) | n_eff ≈ 150-230 of 224 trials (`f1r_summary.json`) | RESOLVED |
| C-2 cost statements | +1 s/trial = 85 CPU-h; 4 × 10² CPU-years (§2.2, §4.1, §6.2) | — | RESOLVED |
| C-3 208 / 3 PU events / n1 counter | §0, §8 V4-6 | — | RESOLVED |
| C-4 V4-1 provenance | V4-1 status corrected; re-recorded per job at G1 | — | RESOLVED |
| C-5 φ-sector boundary gun | Added to V4-9 / G1 | — | RESOLVED (at G1) |
| C-6 SM xsec caveats | Noted in §4.1 | — | RESOLVED |
| C-7 BTL end-of-life | Cited CMS-TDR-020 l.307-308 (50-60 ps) | MTD TDR text copy | RESOLVED |
| C-8 muon veto may cut signal | Veto only after its signal efficiency is shown (§4.2) | — | RESOLVED |
| C-9 edge-fit errors | Joint row-level bootstrap across Λ (§4.1, §5) | — | RESOLVED |
| C-10 B1 summaries only | Road-hit dumps for 2 000 B1 events (+1.7 GB) | — | RESOLVED |
| C-11 merging long direction | Added to the U-5 cross-check scope (§1.5) | — | RESOLVED |
| C-12 PV of PU-only trials | Luminous-region point independent of the PU vertices; distance stored (§4.1.1) | probe median distance to nearest PU vertex 0.37 mm (`f1r_summary.json`) | RESOLVED |
| C-13 verified items | No action; the PU seed hash now includes spin\|m (§4.1) | — | RESOLVED |

### Constructive review

| Item | Action (plan §) | Evidence | Status |
|---|---|---|---|
| **A-1** N_OT2 met by one particle | Same fix as critical B-2 (§2.2.5) | as B-2 | RESOLVED |
| B-1 k decomposition | Adopted in its exact form: per-candidate thinning weights over the interaction set (§4.1.2); power law kept as the alternative | pilot table in §4.1 | RESOLVED (pilot) |
| B-2 timing category | SR-T/SR-G under one WP rule; t_min from PU only; independence test in the gate (§2.3, §4.1.4) | uses the reviewer's `r1c_pu_btl_time.json` / `r1c_signal_handles.json` | RESOLVED |
| B-3 dE/dx | F1 variable with MIP calibration and 4-bit ToT variation (§2.3) | — | RESOLVED |
| B-4 row-major A2 | Adopted (§4.1, §5, §6): A2 120 → 40, A3 18 → 7, A4 23 → 10 CPU-h; validated on the full-chain A5 | the fix-R1 signal overlays were built this way | RESOLVED |
| B-5 k = 1 guns | PV pair gun and looper gun added to C' (§4.2, §5) | — | RESOLVED |
| B-6 P2 velocity deliverables + sensitivity | **PROPOSED D4-13** (adds deliverables) | reviewer's `r1c_tof_mass.json` | PROPOSED, needs the user |
| B-7 roads overlap | = critical C-1 | — | RESOLVED |
| B-8 gate order, stronger pilot | §11 order U-2 → G1 → G2 (freeze → A1/V4-3) → G3 (T1, time independence, ρ = 3 need, T_seed) → guns → production | — | RESOLVED |
| C-1 ρ list | One list ρ ∈ {2, 3 conditional} | — | RESOLVED |
| C-2 R0 PU number is a lower bound | Re-tagged (§2.4) | — | RESOLVED |
| C-3 \|n_z\| | Stored. Measured: it does **not** separate at detector level (PU 0.84-0.86, signal 0.77) | `f1r_summary.json` | RESOLVED (no cut) |
| C-4 ε(Δt_acc) | Curve at 12.5/25/50 ns (§5) | — | RESOLVED |
| C-5 PV placement | = critical C-12 | — | RESOLVED |
| C-6 Stage-5 figure list | §11 | — | RESOLVED |
| C-7 sculpting | A3 coverage check F1 vs F0 (§11) | — | RESOLVED |

## Things found while fixing (not in the reviews)

1. **Plane thickness vs resolution.** Real quirk hits deviate 30-180 µm (median of Stage-3 `res_max_um`) from the pair's own
   best plane. A resolution-only 3σ band (21 µm in the IT) loses them. The plan adds t_tol = 30 µm, the S-2 MS floor, with
   0 and 100 µm as variations (§2.2.3).
2. **Window axis.** A seed axis from two hits can be 0.02-0.2 rad off the pair axis, which drops OT hits. It is now
   re-estimated from the collected hits at each refit iteration (§2.2.4).
3. **Ranking under PU.** At the TDR density a PU candidate often outranks the signal candidate on (N_L2, −χ²). The event-level
   selection is therefore "some candidate passes the rung", not "the top candidate passes" (§2.4).
4. **ρ = 2 finder cost** is ×50-170 the ρ = 1 cost in the unoptimised probe, not ×8. B2 costing depends on G2/G3 (§6.2).
5. **NI** is the most signal-like source that Fatras lacks: about 5-6 decades of rejection must come from F1 and timing
   (§4.2, risk 3b).

## Files

- plan: `acts/stage4/plan.md` (edited in place)
- new probes: `acts/stage4/probes/f1r_pu_gen.py`, `f1r_truth_window.py`, `f1r_density_bench.py`, `f1r_finder.py`,
  `f1r_analyse.py`
- outputs: `data/acts_stage4/fix_r1/` (`pu/` 56 PU-200 events with truth, 233 MB; total 0.6 GB; `finder/*.jsonl`; `f1r_truth_window.json`,
  `f1r_density_bench.json`, `f1r_summary.json`, `f1r_margin.json`, `f1r_tseed_check.json`; `tdr/` page renders of
  CMS-TDR-014 PDF p.101 and p.277 from the local copy in `data/tdr_geometry/`, nothing downloaded)

