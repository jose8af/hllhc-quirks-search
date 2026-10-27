# C001 quirks: theory track (parallel to the Phase-2 exploration)

> **Handoff (2026-10-27):** to set up, rerun or continue this work, read [`REPRODUCE.md`](REPRODUCE.md) (environments,
> data regeneration, stage-by-stage commands, known gaps, prioritised next steps).

Started 2026-10-07 at the user's request. It runs in parallel with the experimental Phase 2 and
**does not edit** files outside `theory_track/`. Goal: find gaps in quirk theory that can be exploited
(better constraints on Λ, oscillation length, propagation dynamics, trajectory models; new
signatures; new handles for the CMS Phase-2 search).

JFC-style loop: parallel investigators → synthesis → independent critical + constructive review →
fix pass → fresh reviewer → PASS → hand to the user.

Layout
- `BRIEF.md`           shared brief every agent reads first (context, conventions, file ownership)
- `investigations/`    T1..T6 investigator reports (one file per agent)
- `code/`              reproducible numerical checks (run with `pixi run python code/<file>.py`)
- `figures/`           plots produced by the code
- `outputs/THEORY_GAPS_SYNTHESIS.md`  ranked gap list (synthesis)
- `review/`            reviewer reports
- `LOG.md`             append-only log for this track

Workstreams
| ID | Topic | Model |
|----|-------|-------|
| T1 | Λ: origin, priors, UV completions, bounds (cosmo/astro/collider) | Opus |
| T2 | Vacuum string dynamics: oscillation length, angular momentum, beyond the straight string, semiclassical validity | Opus |
| T3 | Propagation in B field + matter: plane precession, ionisation/MS torques, charged (net-charge) pairs, timing | Opus |
| T4 | Trajectory model for reconstruction; observables; measuring (m_Q, Λ) | Opus |
| T5 | Literature gap sweep: assumption audit of every quirk theory/pheno paper | Sonnet |
| T6 | Production and model space: γγ, W-mediated mixed pairs, spin, charges, quirkonium/stopped-pair annihilation, complementary signatures | Sonnet |

Python: `pixi run python ...` in this directory (numpy, scipy, sympy, matplotlib, mpmath, numba).

## Status (2026-10-08): DONE — synthesis v4, review R4 PASS
Read first (synthesis now v5, 2026-10-11, Stage-1 crossing theory folded in; v4 kept as _v4.md): `outputs/THEORY_GAPS_SYNTHESIS.md` §0 (glossary + executive summary by the four requested
topics), then §1 (ranked gaps S-1..S-20), §4 (implications for the experimental track, by file/section),
§5 (publishable outputs), §8 (next steps). Review trail: `review/` R1 critical + constructive (ITERATE) →
R2 (ITERATE) → R3 (ITERATE, credit only) → R4 (PASS); responses in synthesis §10.1-§10.4.
PDF report: `report/quirks_theory_report.pdf` (48 pp; files to read, discoveries, discrepancies, proposed modifications). Inputs: `data/`.
Earlier versions kept as `outputs/THEORY_GAPS_SYNTHESIS_v{1,2,3}.md`. T2/T3 reports carry erratum boxes
(the v1 "published straight-string propagators are wrong" headline was withdrawn after R1).

## Status (2026-10-16): P1/P2 programme, STAGE 1 PASS (analytic near-miss impulse coefficient); STAGE 2 PASS (R2, 2026-10-11); STAGE 3 PASS (R3, 2026-10-13); STAGE 4 PLAN PASS (R9, 2026-10-13; `acts/stage4/plan.md`, reviews in `acts/stage4/review/`); WP_RULE frozen; G3 pilot done (FAIL → pre-registered conservative closure, `acts/stage4/g3/G3_REPORT.md`); T_seed := 4 applied (HASH_ADDENDUM §5); **FINAL DELIVERABLE: `paper/quirks_p1p2_note.pdf`** (concise P1+P2 note, 35 pp, review R1→R4 PASS 2026-10-16). PRODUCTION DONE 2026-10-16 (C1a 875 + C1b 760 + C2B 480 + A2FC 180 jobs, 0 errors). STAGE 4 RESULTS PASS (`acts/stage4/STAGE4_RESULTS.md`, from `data/acts_stage4/analysis/C12FC_v1`; normalisation erratum f₂₀₀ applied, R4_NORM PASS): no WP → §8 fallback; best μ95/N_exp = 790 (E200, Λ = 1.5 keV); nothing excluded. STAGE 5 PASS (`stage5/figures/final/`, `stage5/FIGURES_FINAL.md`). STAGE 6 note PASS (`opendata/STAGE6_FEASIBILITY.md`). Deadline Sun 2026-10-18 afternoon — met
Six-stage plan (user, 2026-10-10): 1 analytic c → 2 MadGraph+Pythia8 → 3 ≥ 200 events/point → 4 ACTS CMS-like tracker →
5 plots (JFC conventions, non-CMS label) → 6 CMS Open Data. Work lives in `analytic/`, `sim/`, `acts/`, `opendata/`.
- **Stage 1 (`analytic/`), PASS after 4 review rounds** (R1 critical ITERATE 2A/3B + constructive 12B; R2 ITERATE 4B;
  R3 ITERATE 1B; R4 PASS 0A/0B). Read `analytic/NEAR_MISS_IMPULSE.md` §0 (v5.1), then `analytic/numerics/NUMERICS.md`
  §0 and `analytic/NOVELTY_AUDIT.md` §0. Result: the B-field plane thickness comes from log-enhanced axis rotations
  at odd near-miss crossings; Δs_B ∝ ε_B[ln(1/ε_B) + C], local slope c = 1/[ln(ℓ_max/b_odd) + K(γ*)] ≈ 0.104 at
  1 keV (blind numerics 0.105 ± 0.002), B exponent 1 − c ≈ 0.91, Λ exponent −2 + 2c. Verified near 1 keV, consistent
  to 5 keV; unattributed ±5 % above ≈ 5 keV (CM-frame B* effect + double-precision floor). One failed prediction
  (Li/exact thickness at γ* = 2: 0.50 vs 0.75 ± 0.08). Proposed edits outside `analytic/`: `analytic/PROPOSED_CHANGES.md`
  (not applied). User decision 2026-10-11: P1 scope (b), B-field crossing physics only, MS as measured floor.
- **Stage 2 (`sim/`), STAGE 2 PASS (R2, 2026-10-11)** (R1 critical + constructive ITERATE; fixer R1; R2 PASS 0A/0B/8C,
  C-1…C-7 applied, C-8 folded into the deferred figure restyle). Read `sim/VALIDATION.md` §0, then `sim/SAMPLES.md`;
  MG5_aMC 2.9.22 LO-MLM 0-2j + Pythia 8.313 CP5, E and Ẽ, 47 points, ≈ 2.41 M LHE events; loader `sim/scripts/mg_events.py`.
  - σ table normalisation: σ_norm = N_IC (2) × K_WG × LO(α(M_Z)) matches the TH §2.3 table to −0.36…+0.15 %; use
    `sigma_norm_fb` for yields (not the LO-MLM `sigma_lo_mlm_fb`); ±5 % nuisance; γγ and Sommerfeld not included.
  - Tail-rate uncertainty: f(pT(QQ̄) > 200) at LO-MLM +12…+15 % / −11…−13 % (ESTIMATE; NLO-FxFx deferred, `sim/DEFERRED.md` D-1).
  - ℓ_max bias: the fixed-pT ISR trick biases the median ℓ_max by −26 / −13 / −8 % (E, 200/500/1000 GeV, like-for-like);
    reference medians ±5 % (ESTIMATE).
  - QED FSR off the quirks is absent from the delivered samples. User decision 2026-10-11: no re-shower; carry a
    one-sided ℓ_max systematic of −1.1 ± 0.8 % (stat).
- **Stage 3 (`sim/stage3/`), STAGE 3 PASS (R3, 2026-10-13)** (R1 critical + constructive ITERATE; fixer R1 incl. B*-off
  runs; R2 ITERATE on one B (wording); fixer R2; R3 narrow verifier PASS 0A/0B/3C, Cs applied). Read
  `sim/stage3/README.md`, then `VALIDATION.md` §0. Truth-level T3_causal_s3 propagation, 218 571 events on Mac + Windows
  PC (cross-machine 224/225 events bit-identical). Handover to ACTS: `sim/stage3/HANDOVER_STAGE4.md`.
  - P1: Δs_B model within 3.4 % (E) / 5.3 % (Ẽ) per event; c law valid for median ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4;
    at 3–5 keV, a k_B-dependent c excess (size VERIFIED; B* attribution ESTIMATE, 5.5σ vs B*-off); floor test O-1 not done.
  - P2: Λ edges vs mass, plus a continuous handle (IT pair separation ∝ Λ⁻²).
  - Pending user decisions U-1…U-5: `sim/stage3/DECISIONS_PENDING.md`.
