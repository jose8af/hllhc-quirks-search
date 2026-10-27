# E2 numerics plan: crossing-resolved measurements of the near-miss transverse impulse (Stage 1, P1)

Owner: E2 (numerics executor), 2026-10-10. Blind to E1 (no reading of `analytic/NEAR_MISS_IMPULSE.md`,
`analytic/predictions.json`, `analytic/checks/` until NUMERICS.md is final).
All runs: `pixi run python analytic/numerics/<file>.py` from `theory_track/`. Units cm, GeV, c = 1.

## 0. Physics facts used to design the measurements (from the existing track, not from E1)
- Canonical momentum P_can = p1 + p2 + P_string - q(x1 - x2) x B is conserved exactly (neutral pair, uniform B).
  At a crossing x1 ~ x2 and the string is ~collapsed, so **p1 + p2 = P0 at every crossing**: one CM frame
  (boost by P0) serves all crossings of an event. Per-crossing axes can therefore be compared across crossings.
- In vacuum the causal (Athena-type) kernel is exact for piecewise-null world-sheet data: segment splitting
  composes exactly, so in a field-free CM run the only approximation is the initial data. With B or E the only
  approximation is the first-order field kick per step (max_boost, hmax). Inside a step the exact endpoint
  position for absorbed fraction λ of the incoming null vector s is
  x(λ) = x + 2λ (s·p) (p + Fλ s) / (m² + 2Fλ s·p)  — used for exact closest-approach interpolation.
- The queue convention of the kernel: quirk k's queued null vectors point (spatially) from k towards the
  partner; a static straight string of length d with x1 - x2 = d ê is Q1 = (d/2)(1, -ê), Q2 = (d/2)(1, +ê)
  (string energy F·Σ s⁰ = σ d). This allows exact "angular-momentum yo-yo" initial data.
- Classical NG with massive ends is scale free: in vacuum the CM problem depends only on (b/ℓ₀, γ*) with
  ℓ₀ = m/σ. "b below 1/Λ" is a statement about quantum validity only; classically it is reached by
  b/ℓ₀ ≲ 2×10⁻⁹ (1 keV, 500 GeV). Varying m/σ at fixed γ* changes ℓ_max and ℓ₀ together, so L = ℓ_max vs ℓ₀
  is distinguished only through the γ* dependence of K (ln(ℓ_max/ℓ₀) = ln 2(γ*-1)).

## 1. Codes (all new files in analytic/numerics/; nothing in code/ is edited)
| file | content |
|---|---|
| `nm_kernel.py` | numba copy of `T3_causal.causal_propagate`, B only (material removed), plus: uniform E field kick (q E·dx, q E dx⁰), optional initial endpoint positions + initial queues (static straight string), dense per-step record (quirk, x⁴ before step, p⁴ before step, absorbed null vector s⁴). Validation: hits bit-identical to `T3_causal.run_causal(material=False)` for E = 0, default init. |
| `nm_conformal.py` | copy of `R1_conformal_ng.solve` with the same additions (E field, initial offset string along ê, dense record of τ, X, u, w). |
| `nm_crossings.py` | analysis of a dense record → per-crossing table: crossing index k and parity, closest approach b_k (equal CM time minimum of |x1*-x2*| in the P0 frame using the exact intra-step map / Hermite for conformal), b-vector components on ê_N = unit(n̂×β̂) (normal of the lab pair plane), ê_P = ê_N×n̂ and on E*_⊥ = (γβ×B)_⊥n̂, relative speed and γ* at closest approach, separation amplitude ℓ_k (max |x1*-x2*| in the preceding half period), axis a_k = ±unit(v1*-v2*) at the crossing, axis tilt per crossing Δa_k·ê_N, Δa_k·ê_P, and the transverse impulse Δp⊥,k(τ): change of the relative transverse momentum (p1*-p2*)/2 ⊥ a_k over the window [t_k-τ, t_k+τ] for τ on a log grid up to the turning points, split into string part (F(s - s_out) summed) and Lorentz part. |
| `nm_stats.py` | bootstrap helpers (median, Q68, ratios, local exponents), JSON writer. |
| `M1_events.py`, `M2_single.py`, `M3_thickness.py`, `M4_convergence.py` | campaigns; one result file per point in `results/raw/<campaign>/` (skip if present), merged JSON in `results/M*.json`. |

## 2. Measurements (adapted from the brief; changes justified)
**M1 per-crossing diagnostics on full events.** B = 3.8112 T, no material, events from the T2 kinematics cache
(LO DY+ISR, pT(QQ) > 200 GeV, |η| < 1, the T3 recipe); Λ = 0.6, 1, 2, 3, 5, 10 keV × m = 200, 500, 1000 GeV,
≥ 60 events per point (cost permitting; the record at 10 keV is ~10⁶ steps per event, measured first).
Analysis per crossing as in `nm_crossings.py`; summary per point: b_odd, b_even (median, bootstrap error),
b·Λ⁴-scaling, orientation of b relative to ê_N and E*, impulse per unit b, axis tilt per crossing, and the
correlation Δp⊥,k vs b_k, ℓ_k, γ*_k (does the per-crossing law from M2 describe the full events?).
Solver check: conformal solver on a subset (500 GeV, Λ = 1 and 2 keV, ~5 events) with the same analysis.
Change: the window-τ profile Δp⊥(τ) is added because the heuristic impulse is a log integral over all scales
between b and ℓ; a single "before/after" number would hide where the impulse accrues.

**M2 controlled single crossings (pair CM frame).**
- M2a vacuum angular-momentum yo-yo (exact for the causal kernel): x1,2 = ±(d/2)ê, p1,2 = ±p* n̂, n̂ ⊥ ê,
  static straight string of length d. Scan d/ℓ₀ = 10⁻¹⁰…10⁻² (≥ 3 decades below and above 1/Λ-equivalent),
  γ* = 1.05, 1.3, 2, 3. Measure b at each crossing (first 4), the apsidal rotation ψ per half period, the
  deflection χ of the quirk velocity across the crossing, the transverse impulse profile Δp⊥(τ), and fit
  Δp⊥ = A b [ln(L/b) + K] / normalisations (σb/v etc.). Both solvers. Also a straight-string (Kang-Luty, CM
  frame) reference to say whether the exact NG crossing differs from the straight-string picture.
- M2b field-driven crossings: constant transverse E (and, separately, B) in the CM frame, scan |E|/σ over
  ≥ 3 decades, orientation of E relative to the axis; measure b_k, Δp⊥,k at odd/even crossings; compare with
  M2a law evaluated at the measured b. Causal + conformal.
Change: b is controlled by the initial angular momentum (exact, no field) rather than by a field switched off
before the crossing; M2b keeps the field on as in real events. "ℓ" is varied through γ* (ℓ_max/ℓ₀ = 2(γ*-1));
scale invariance makes m/σ variations trivial (checked once numerically).

**M3 thickness scans (truth level, B only).** Δs_B = plane-fit thickness through the PV of all hits on the
10 barrel layers (T3 definition). Λ = 0.45, 0.6, 1, 2, 3, 5, 10 keV × m = 200, 500, 1000 GeV, ≥ 100 events
each (same events across Λ). B scan B₀ × {2, 1, 1/2, 1/4, 1/20, 1/80, 1/1000} at Λ = 1, 3 keV (m = 500 GeV,
and 1000 GeV if cheap). Report median, Q68, bootstrap errors, local exponents d ln Δs / d ln Λ and / d ln B with
bootstrap errors (paired events), response per unit B (event-level Δs(f)/f/Δs(1) and hit-level out-of-plane
displacement per unit B, S_Bnonlin metric) split into hits before / after the first crossing, and Δs split by the
number of crossings inside the tracker. Stage 3 redoes this on MadGraph samples (README note).

**M4 convergence.** Every M1/M2b/M3 number re-run on a subset with max_boost ×1/10 and hmax ×1/10 (causal) and
N ×4…×10 (conformal); vacuum floor (B = 0 thickness, B = 0 miss distance) quoted.

## 3. Costing (to be filled after the timing slice) and safety
- Timing slice first (1 event per Λ, 500 GeV). Campaigns > 10 min run with ProcessPoolExecutor (spawn), 7 workers,
  seeds pinned per (point, event), one output file per point/event, skip-if-present; parallel outputs checked
  not bit-identical across events.
- Results > 20 MB go to `data/stage1_numerics/` (README there).

## 4. Reporting
`NUMERICS.md`: summary ≤ 15 lines; methods; M1-M4 tables; convergence; solver-independent quantities;
surprises; open issues. Tags: VERIFIED (both solvers agree within stated tolerance) / ESTIMATE (one solver);
all are truth level. Statistical errors are bootstrap (≥ 1000 resamples) unless stated.

## 5. Added by coordinator request (novelty audit): M5
**M5 straight-string B-linearity.** Re-run the B-linearity test (B₀ × {1, 1/4, 1/20, 1/80}, Λ = 1 keV, m = 500 GeV,
γ* ≈ 1.3, ≥ 30 events) with the literal Li CM-simultaneous straight-string integrator `code/R1_li_literal.py`
(imported, step-converged, ~10⁻³ of the printed step), and compare its response per unit B before/after the first
crossing with the causal string on the same events. Question: does the B ln(1/B) non-linearity need string
curvature/retardation? Lowest priority (run last). M2a already contains a vacuum straight-string reference.

## 6. Costing as executed (filled 2026-10-10)
Timing slice: 10 keV / 1 TeV event 0.4 s kernel + 1.7 s analysis (steps grow ~Λ³, 6.5e6 at 10 keV); causal steps per event far
below T2's estimate. Executed: M2 416 runs (13 s wall); M1 2008 jobs (1.0e4 s CPU; 60 events at 5-10 keV instead of 100, CPU);
M3 2700 jobs (3.2e3 s); M5 30+6 events (1.2e3 s; Li via scalarised copy nm_li.py); M4 conformal thickness 24 events (0.4e3 s).
Deviations: conformal solver unusable for exactly head-on crossings and for vacuum offset data at γ* ≥ 2 (flagged, status 7);
a double-precision floor at b/ℓ₀ ≈ 3e-8 limits the B scan to k ≤ 80 (1 keV) / 20 (3 keV).
