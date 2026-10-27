# theory_track/analytic — Stage 1: analytic near-miss impulse coefficient (P1)

Goal: derive, from the Nambu-Goto string with massive endpoints in a uniform B field, the transverse impulse at a
near-miss crossing, the coefficient c in Δs_B ∝ ε_B [1 + c ln(Λ²/qB)] and the predicted exponents in Λ and B;
validate against the causal-string numerics and the independent conformal-gauge solver; audit novelty.

| File | Owner | Content |
|---|---|---|
| `plan.md` | E1 (analytic executor) | execution plan, written before any derivation |
| `NEAR_MISS_IMPULSE.md` | E1 | the derivation note (primary artifact) |
| `checks/` | E1 | sympy / numeric checks of every formula in the note |
| `predictions.json` | E1 | machine-readable predictions (c, exponents, per-crossing impulse law, assumptions) |
| `numerics/` | E2 (numerics executor) | crossing-resolved numerical experiments (own plan.md, scripts, results JSON, NUMERICS.md) |
| `NOVELTY_AUDIT.md` | E3 (novelty auditor) | credit / novelty audit against the classical-string and quirk literature |
| `review/` | reviewers | critical + constructive reviews, fix responses |

Rules: theory-track only; existing `code/` scripts are imported or copied, never edited. Run Python with
`pixi run python <path>` from `theory_track/`. Status and decisions are logged in `../LOG.md`.
