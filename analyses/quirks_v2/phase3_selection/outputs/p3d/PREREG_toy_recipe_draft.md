# T1 toy recipe: text proposed for PREREG_v2 (p3-d, Gorm, 2026-11-24; draft, to be reviewed)

Status: proposal by the executor of p3-d for EXP §10 item 9 and COM l.295-296, l.356. Nothing here changes a frozen
criterion. Everything else in the toy procedure is STR §4.11 pt 2 (l.1626-1643) as frozen. Implementation:
`phase3_selection/src/p3d/p3d_toys.py` (`limit_status`, `cls_counts`, `Engine.q`).

**1. Pseudo-experiments (as frozen).** At each tested μ, one background-only and one signal-plus-background
ensemble of N = 1,000 pseudo-experiments each (2,000 each for T1-c (i)). Each counted rate is drawn from
Gamma(m + 1, 1), each constrained nuisance from N(0, 1) clipped at its censoring bound, and n_c from the Poisson
distribution. The auxiliary observations stay at m. Seeds: `SeedSequence([seed, ensemble, key(μ)])` with
key(μ) = round((ln μ + 60)·10⁶), so a given μ always gets the same pseudo-data, whatever the order of evaluation.

**2. Test statistic and fit guard.** q̃_μ = t(μ) − t(μ̂) from two pyhf fits, with q̃ = 0 if μ̂ > μ (pyhf 0.7.6,
jax backend, scipy optimiser, tolerance 10⁻¹⁰, normsys code1). A fit is accepted only if its Newton decrement is
below 10⁻⁴. The decrement is taken over the parameters that are not fixed and not active at a bound (KKT
test: within 10⁻³ of the range from a bound and the gradient pointing outward; such parameters are first projected
onto the bound, and the projection is kept if the NLL does not rise). Order of attempts:
- free fit: start from the generated values and from the previous pseudo-experiment's free minimum, SLSQP and then
  L-BFGS-B, keep the lower accepted minimum;
- fixed fit: start from the free minimum with μ set, then the previous pseudo-experiment's fixed minimum, then the
  generated values, SLSQP and then L-BFGS-B, keep the first accepted;
- if neither works, continue in μ from μ̂ to μ in four steps.
A pseudo-experiment with no accepted pair is dropped. If more than 2 % of either ensemble is dropped, that μ point
is **unresolved** and does not enter the limit. The fraction dropped is reported at every point.

**3. CLs at one μ.** For the quantile p of the expected limit (p = 0.5 for the median; 0.16, 0.84, 0.025 and
0.975 for the bands), q_obs(p) is the ⌈pN⌉-th largest background-only q̃. This is the inverse empirical CDF in limit
space. It equals the analytic convention "smallest n with P(n ≤ n | b) ≥ p" for one bin. A pseudo-experiment
counts towards the tail if q̃ ≥ q_obs − 10⁻⁵ (ties within 10⁻⁵, absolute). CLs = (k_sb/N_sb)/(k_b/N_b).
*Alternative reported beside it at the best point:* `numpy.median` of the background-only q̃ (the Phase-2 T1-b
choice) for p = 0.5.

*Quantile on a discrete edge (advisor ruling 2026-11-24, point 7; to the 4-bot PREREG review).* With discrete counts,
the background-only ECDF can sit exactly at p: one bin, m = 0, κ = 1 has P(n = 0 | b) = 1/(1 + κ) = 0.5, and the
median is then a coin flip between the n = 0 and n = 1 branches (3.0 and 5.7, STR l.1681). Rule: if, at the evaluated
points near the crossing, the background-only ECDF at q_obs(p), i.e. k_b/N_b, lies within its binomial error
√(p(1 − p)/N_b) of p, the limit is flagged **"quantile on a discrete edge"**. Both branch limits are then reported:
q_obs set to the distinct q̃ level on either side of the edge. The **weaker (larger) one is quoted**. The test
criterion of T1-c (i) is not reworded. There the κ = 1 median is judged "within the toy error" by a bootstrap that
spans both branches, together with the background-only fraction of n = 0 against 0.5.

**4. Bracket.** The grid is μ_a × {0.4, 0.55, 0.75, 1, 1.35, 1.8, 2.5, 3.5}, with μ_a the Asimov limit of STR l.1636.
μ₉₅ is bracketed by the **first crossing from low μ** over all resolved points evaluated so far: the lowest pair of
neighbouring points (μ_lo, μ_hi) with CLs(μ_lo) > 0.05 ≥ CLs(μ_hi). If no pair exists, the grid is extended by
factors of 1.5 on the open side (as frozen).

**5. Bracket refinement (new).** While μ_hi/μ_lo − 1 > 2 %, a new point at the geometric midpoint √(μ_lo μ_hi) is
evaluated with fresh ensembles (step 1), and the first-crossing bracket of step 4 is recomputed over all points. From
a grid step of 1.35 this takes four midpoints. A midpoint that comes out unresolved is redrawn once with the next
seed; if it is unresolved again, the refinement stops and the limit is reported with its bracket and the flag
"unresolved inside". At most 40 points are evaluated per limit.

**6. Interpolation and the empty tail (new).** Inside the final bracket, ln CLs is interpolated linearly in μ to
ln 0.05. If the upper end of the final bracket has an **empty signal-plus-background tail** (k_sb = 0), CLs there is
only an upper bound and the logarithm is not defined. In that case **μ₉₅ = μ_hi**. This is conservative and lies
within 2 % of any interpolated value. For the bracketing of steps 4 and 5, an empty tail counts as excluded
(CLs = 0). *Diagnostics reported beside it:* k_sb := 1.139 (the Phase-2 rule) and k_sb := 0.5.

**6a. Pile-up bound (advisor ruling, point 8).** A credited pile-up estimator: the fit bound on its closure θ is at the
68 % value of its no-credit bound (485 events = 1.139 × N_trig/96,000, STR l.1587), and the generation draws the bound
per pseudo-experiment, θ ≤ ln(N_trig λ/96,000/φ₀)/s with λ ~ Gamma(1) (STR l.1586-1588, l.953-954). The best-point
limit is also reported with the fit bound at the 95 % value (2.996 × 425.5 = 1,275 events). A pile-up term with no
credit is a counted factor with m = 0 of M = 96,000 and a free λ (STR l.1565), with no fixed bound. Implementation:
`p3d_model.v2_placeholder(pu_credit=…)`, `Explicit.clip_draw`.

**7. Bands.** Steps 4–6 apply to each quantile separately. Every evaluated point serves all quantiles. The limit is
quoted as the median with the 16–84 % and 2.5–97.5 % bands (STR l.1632, l.1694).

**8. What is recorded per limit.** Every μ with its N_b, N_sb, k_b, k_sb, q_obs, the dropped and retried counts, the
largest Newton decrement, and the CPU time. The final bracket and whether its upper end has an empty tail. The
frozen-grid value without refinement, for comparison. The toy error from a bootstrap of the stored q̃ arrays (200
resamples, same points).
