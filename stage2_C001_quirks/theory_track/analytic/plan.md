# E1 plan: analytic near-miss impulse and the coefficient c (Stage 1, P1)

Written 2026-10-10 before any derivation. Executor E1. Files: see analytic/README.md.

## Goal
From the Nambu-Goto (NG) string with massive endpoints in a uniform B, derive
(i) the transverse impulse at a near-miss crossing, (ii) its accumulation into the plane-fit thickness Δs_B,
(iii) c in Δs_B ∝ ε_B [1 + c ln(Λ²/qB)], the response per unit B vs B, and local exponents in Λ and B.
Compare with the fitted c ≈ 0.08-0.11 only at the end; do not tune.

## Inputs already read
BRIEF; synthesis §0, S-1, S-3, X-2, X-3, X-13, §5 P1; T2 §2, §5-6; T3 §3; T4 §3; T3_causal.py (partly).
Still to read: R1_conformal_ng.py header, T2_crossing_missdist.py, S_Bscan/S_Bnonlin/R1_Blinearity + outputs,
0805.4642 §3, 1911.02223 Eq.III.6-12, 2002.07503 §V + App.C.

## Steps (each ends with a log line in E1_session_log.md and a section appended to NEAR_MISS_IMPULSE.md)
1. Skeleton of NEAR_MISS_IMPULSE.md (sections 0-11) on disk.
2. §1-2 Setup + vacuum yo-yo in the pair CM frame (closed forms, checked by sympy: energy, ℓ_max, period,
   velocity at crossing; boost of lab B to E* = γβ×B, B*). Check script checks/c01_yoyo.py.
3. §3 Linear response. Conformal gauge: worldsheet coordinates (τ,σ), transverse displacement y(τ,σ)
   obeys the free wave equation; endpoint BCs m d/dτ(γ ẏ) = ±σ y' + q(E*+v×B*)⊥. Solve for the
   first half-period (static polarisation + driven transients), compare with Li d / d_E and b_odd.
   Identify the breakdown: at the crossing the string length → 0 and the transverse angle y/|x| is not small.
   Check: checks/c02_linear.py (sympy + small numeric comparison with T3_causal before 1st crossing).
4. §4 Inner problem. Near the crossing: two massive endpoints with relative longitudinal velocity v_rel and
   transverse offset b, joined by a short string; the string force on each endpoint is σ along the
   (causal) string direction. Compute Δp⊥ = ∫σ sinθ dt with θ = angle of the string; outer region
   (|x| ≫ b) gives σ b/|x|, inner region regularises; include retardation (null-segment construction).
   Get A, argument L of the log and constant K. Check by sympy (integrals) and a numeric
   toy (two endpoints + causal string, from T3_causal imported) on one or two configurations.
5. §5 Accumulation: per-crossing impulse → out-of-plane (and in-plane) displacement of hits; sign pattern
   (coherent vs alternating) over N_osc crossings; plane-fit Δs; c, response per unit B, exponents.
   m_Q independence argument.
6. §6 Odd vs even crossings, γ*, angle; §7 NG validity cutoff and model uncertainty.
7. §8 Predictions table + predictions.json (DERIVED/ESTIMATE/CONJECTURE tags). §9 placeholder.
8. §10 open issues with LOW/MEDIUM flags; §11 references opened. Final LOG.md line.

## Rules I follow
- Every formula: derivation steps or cited source; sympy check + limiting case (B→0, b→0, v→0, m→∞),
  outputs saved as checks/*.txt.
- Numerics only small and targeted (E2 does the campaign). No edits outside the allowed files.
- If the derived c disagrees with 0.08-0.11, report it honestly with candidate causes.

## Risks / decisions to watch
- The "impulse" may be mostly in-plane (T4 says the B displacement is mostly rφ) — the thickness is
  out-of-plane; I must separate the two carefully. MEDIUM risk.
- The log may come from a different mechanism (e.g. the even-crossing geometry or the transverse-mode
  transient) than the heuristic; follow the derivation, not the heuristic.
