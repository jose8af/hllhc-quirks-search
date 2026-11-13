# Constructive review — Phase 1 STRATEGY (quirks v2)

Reviewer: Cosima (constructive reviewer, 4-bot panel), 2026-11-13 18:20.
Artifact: `phase1_strategy/outputs/STRATEGY_brigitte_2026-11-13_17-55.md` ("STR", 1,248 lines, read in full) and
`COMMITMENTS.md` (read in full).
Also read: `agents/constructive_reviewer.md`; `AGENT_RULES.md`; `FRAMING.md`; `methodology/06-review.md` §6.1–6.4.1;
`methodology/03-phases.md` "Analysis Philosophy" and "Phase 1"; `methodology/12-downscoping.md`; `conventions/search.md`;
`prompt.md` §2, §3, §6, §7; `LOG.md` (user decisions); `publication_plan/publication_plan.tex` (PLAN) l.105–131,
l.192–236, l.276–368, l.451–543; digests D3 §6, D4 §4–5, D6 §1–2; FEAS_C R9 (grep); `experiment_log.md` (grep).
There is no RAG corpus (deviation V8). I did not spawn sub-agents (AGENT_RULES). All my arithmetic is in a standard-library
script (`python3 -I`, scratchpad `calc.py`; outputs quoted below as **[R: calc]**).

Classification (JFC 06 §6.1): **A** must resolve (blocks), **B** must fix before PASS, **C** suggestion.

---

## 0. Summary

The strategy is careful, honest and unusually well quantified. Its strongest parts: one definition of
"within a factor F" with an anti-inflation cap (STR l.213–221); the explicit refusal of scale-factor patches; the C1
design (41 declared comparisons, Bonferroni, family coherence, stated power, l.266–280); the precise blinding exception
for C1 (l.282–294); the correction of the plan where it was wrong (B₈₄ ≈ 0.17 is not a width, l.556–560; the
"4.9 decades" quote, l.128–130; V4-4/V4-5 mix-up, l.309–311); and a CPU budget that sums correctly (I re-added §11.2:
MUST 2,950; Phase 4a 1,953; reduced total 3,276 ≈ 3,275; weekly slots 5×(11×9+13×12)+2×24×12 = 1,851 [R: calc]).

What it does not yet do is show that the plan **can reach the central target** (PLAN l.129–131: every leading
zero-count bound turned into an estimate, total σ_ln ≲ 1). Three issues decide this, and none needs much work:

1. **[A-1] The expected-limit construction with zero auxiliary counts is not specified, and the natural pyhf
   construction sets every zero-count term to zero background.** That would make the bounds disappear from the
   expected limit by construction, which is the opposite of the paper's message.
2. **[B-1] The central target has no operational definition and no projection.** A term resting on one zero count has an
   intrinsic log-width of π/√6 = 1.28 > 1. At the planned no-PU sample sizes the zero-count floors are ≈ 141 events (PV
   pairs) and ≈ 47 events (SM, all processes) before any credit. That is the plan's "middle" outcome unless biased
   generation enriches by ≥ 10², and the strategy does not quantify that enrichment. Reallocating the same no-PU CPU
   halves the floor, and the no-PU samples are the cheapest lever in the whole budget.
3. **[B-2] The battery of closure tests is not designed for size and power as a whole.** Under the AND rule of [SD8],
   an analysis whose estimators are all perfect has a probability of about 0.5 of being declared "closure fails"
   (12 independent p > 0.05 tests: 0.95¹² = 0.54). Single F = 1.5 tests at N = 20 fail falsely 9.8 % of the time.

Counts: **A = 1, B = 16, C = 11.**

---

## 1. Findings table

| id | cat | topic | one line | effort to fix |
|---|---|---|---|---|
| A-1 | A | T1 | Expected limits with m = 0 auxiliary counts: the background-only generation point is undefined; at the MLE (λ̂ = 0) zero-count terms vanish | 0.5 day of design text + a 1 CPU-h limiting-case test in Phase 3 |
| B-1 | B | central target | Define "estimate" and "total σ_ln"; floor table per term at the planned M; enrichment of biased generation; reallocate no-PU samples | 0.5 day of arithmetic; 1–2 CPU-h of enrichment pilot in Phase 2; ≤ +150 CPU-h |
| B-2 | B | closure statistics | Family-wise size and per-test power of the closure battery; criterion (a) at low N; B3 "≥ 30 before the cut" | 0.5 day |
| B-3 | B | trend tests | Rule "slope compatible with zero → nothing added" has no power for B1 and is discontinuous; rung index across cut families | 2 h |
| B-4 | B | B3 | Conditionals measured after a loose rung and applied after deep rungs: the factorisation (referee Q4) is not tested | 2 h of text; 0 CPU (re-analysis) |
| B-5 | B | B3-c time tag | As designed the late-hit conditional (≈ 10⁻⁴) will be "not testable"; it is the largest single lever for SR-T | 0.5 day of design; ≈ 5 CPU-h |
| B-6 | B | B5 | Sideband closure on SM+PU samples is dominated by flat pile-up candidates (hard-scatter share 6–10 %): a ×5 non-flatness passes F = 1.5 | 2 h of text; ≈ 10 CPU-h on existing no-PU samples |
| B-7 | B | B6 | Detector variations propagated only to the pile-up term at R04–R06, not to single-interaction and SM terms that lead from R07 on | 2 h; ≈ 20 CPU-h of no-PU reruns |
| B-8 | B | T1 + B1/B4 | Poisson auxiliary model for *weighted* samples (biased generation, p̂T slices) not specified | 1 h |
| B-9 | B | B4 multijets | P(r \| multijet) population: ~100 effective events would give a new zero-count floor | 2 h |
| B-10 | B | B4 MET model | Validation (a) partly circular (soft term set to reproduce v1's 25 GeV smearing vs. sourced R-3); no external MET-resolution anchor | 1 h |
| B-11 | B | DP3 / MVA | Infeasibility argument overstated: thinning and P_geo × C_PU *are* selection-agnostic; the valid reasons are not stated | 1 h of text |
| B-12 | B | [SD8] | "Leading term" decided with the failed estimator's own (possibly too low) value — loophole | 30 min |
| B-13 | B | failure path | Post-freeze closure failure: JFC regression / remediation vs. "reported as failed" not reconciled | 1 h |
| B-14 | B | toys / schedule | Toy budget counts one pass; two are needed (T2 at 4b, final at 4c), T1-g is a nested-toy test; [L4] ×2 | 1 h; may save ≥ 100 CPU-h (C-level suggestion inside) |
| B-15 | B | COMMITMENTS | Sub-item labels differ between STR and COMMITMENTS (B1, B2, T1, T2, S2) | 1 h |
| B-16 | B | B2 | Deep reach of repaired thinning not specified (draws per trial, effective N); occupancy model's fit-probability conditional source | 1 h |
| C-1 … C-11 | C | various | Gate-A sheet; paired designs for B6; use of v1 row arrays; always-eligible baseline; figures; idle pre-freeze capacity; stale Geant4 text; dump storage; comparison targets; §11.6 levers; length | — |

---

## 2. Focus 1 — will the plan deliver the central target?

### A-1 (A) Zero auxiliary counts in the expected-limit construction

*Evidence.* STR l.618–625: "m = 0 is an ordinary observation: the auxiliary term is e^(−λ)"; each count is an
auxiliary channel with an unconstrained γ ([SD7]); "toys fluctuate the simulated counts too". STR l.639–645: toys are
primary. Nowhere does STR say **at which background value the background-only pseudo-experiments (or the Asimov data
set) are generated**. There is no collision data, so in pyhf the signal-region "observation" must itself be built from
the model. If it is generated at the profiled maximum-likelihood point, every term with m = 0 has γ̂ = 0, and so it
contributes **zero** expected background. Toys that "fluctuate the simulated counts" around λ̂ = 0 always give m = 0.
The expected limit then becomes the B = 0 limit at every deep selection, whatever the sample sizes. v1 avoided this by
using hybrid toys with the nuisances sampled (D4 l.333: "μ₉₅ (hybrid CLs toys)"). The FEAS_C toy used a stand-in "one
event with τ = 1" (FEAS_C l.206), so the feasibility run did not test this either.
None of the planned checks would catch it. T1-b runs in "v1 mode" (l.649); T1-c signal injection and T1-g
self-consistency (l.654–657) are internally consistent at B = 0. Fig. 7 marks the background "as the median with its
width" (l.1020), and the median of λ given m = 0 is not even defined for a profile-likelihood point estimate.
*Why A.* This is a genuine method error waiting to happen. It would give a result that looks like the "good" outcome
and present bounds as if they were zeros. That is the tautology the honest-framing check exists for.
*Fixed looks like.* STR §4.11 states the construction. Recommended: background-only pseudo-experiments with each
auxiliary rate drawn from its posterior given m (Gamma(m + 1) with a flat prior, or Gamma(m + ½) with Jeffreys; the
choice is declared), i.e. the prior-predictive (hybrid) construction v1 used. The fully frequentist alternative, if
retained, is reported beside it with the choice of generation point stated. Add a limiting-case test to T1: a model
with one background term with m = 0 of M must reproduce the analytic hybrid limit for B ~ Gamma(1, M) to within toy
error. Add the dependence on the generation point (MLE vs. posterior mean (m + 1)/M) as a reported number at the best
point. Effort: half a day of text; ≈ 1 CPU-h in Phase 3.

### B-1 (B) The central target needs a definition, a floor table and a sample allocation

*Evidence.*
- The target is σ_ln ≲ 1 for the *total* background (PLAN l.129–131). STR never defines how the total width is computed
  from the T1 model, nor when a term counts as "estimated" rather than "bounded". Fig. 7 needs both (l.1020).
- Width of a single zero-count term: if λM ~ Gamma(1) (exponential), then sd(ln λ) = π/√6 = **1.28**. For m = 1, 2, 3, 5
  it is 0.80, 0.63, 0.53, 0.43 [R: calc]. **A deep selection whose leading term is one zero count cannot meet σ_ln ≲ 1
  by construction.**
- Floors at the planned sizes, before C_PU, conditionals and time-tag credit, at 1.14/M:
  PV pairs N_trig × 30.31 = 1.24×10⁹ (STR l.102, l.255) at M = 10⁷ (l.394) → **141 events**; DIF 7.4; γ 1.8; V⁰ 0.24.
  SM at 10⁶ no-PU events per process (l.506–507) → N_trig × 1.14×10⁻⁶ = **47 events** summed over all processes
  (Z(νν) alone 28.6) [R: calc]. These floors apply in *each* category unless the time tag gives credit.
  This is the plan's "middle" outcome (B ≈ 10², σ_ln = 1 → 495 GeV, PLAN l.123, l.504), not the "good" one.
- Biased generation (l.363–368) could change this by orders of magnitude: road ±0.15 rad alone is a factor
  2π/0.3 ≈ 21 [E]. But STR never estimates the enrichment factor. Its only floor statement (l.394–396) is the
  unbiased one.
- Allocation: STR spends 128 + 63 = 191 CPU-h on the no-PU samples that set the deep-rung floors (l.398, l.544). That is
  6.5 % of MUST, against 403 CPU-h for the B2 direct sample. For zero counts, the summed floor Σ rate_t/M_t at fixed
  ΣM_t is minimised by M_t ∝ √rate_t. For the four leading topologies that takes the summed floor from **150.6 to
  67.5 events** at the same 4×10⁷ events [R: calc]. Z(νν) at 10⁷ instead of 10⁶ costs +38 CPU-h at the assumed 15 ms
  and takes its floor from 28.6 to 2.9.
- The factor-2 tolerance is said to "leave room" in a σ_ln ≲ 1 budget (l.375–376). But B1-c also allows a factor-2
  rate band (l.381). One B1 term at both caps has √(2 ln²2) = 0.98, and 1.61 with a zero-count P_geo [R: calc]. The
  room is not there unless the declared widths are well below their caps.
*Fixed looks like.* (i) A definition in §4.11: total σ_ln ≡ ½ ln(B₈₄/B₁₆) of the background-only predictive
distribution of B_total under the A-1 construction. A term is "estimated" if its leading factor rests on m ≥ 1
(or on a closure-tested estimator with declared s_model), and "bounded" otherwise; the ladder figure and the paper
label each term. (ii) A floor table (term × selection family) at the planned M, with the expected enrichment of biased
generation, s_model at its cap and its expected value, and the projected σ_ln and outcome row of PLAN §8. With v1
efficiencies as placeholders this gives a pre-registered expected outcome (see C-3). (iii) A Phase-2 pilot (1–2 CPU-h)
that measures the enrichment per topology. (iv) Reallocate the no-PU budget to equalise floors (≈ √rate allocation;
SM leading processes to ≥ 10⁷ events). This is cheap (≤ +150 CPU-h) and has the largest payoff per CPU-hour in the
whole plan.

### B-4 (B) Conditionals measured after loose rungs, applied after deep rungs

*Evidence.* B3 measures P(cut | topology, passes the preceding rungs) on no-PU samples (l.480–482). It is closed "at
the loosest rung where the direct sample has ≥ 30 counts before the cut" (l.488–491). If P_geo is zero beyond R08–R09
in 10⁷ events, the population "passing the preceding rungs" does not exist at the deep rungs. The conditional for
h, o (R15–R20) is then necessarily measured after a looser rung and assumed to transfer. That transfer is exactly
referee Q4, "factorisation across kinds of cut is untested" (STR l.1041). STR does not name the assumption or test it.
*Fixed looks like.* State the assumption. For each conditional, measure it after ≥ 3 different preceding rungs
(e.g. R05, R06, R07, and R09 where populated) on the no-PU samples. Pre-register a stability test on that sequence,
with the slope rule of B-3. Re-analysis only (inside the 30 CPU-h of l.495).

### B-5 (B) The time-tag (late-hit) credit as designed will be "not testable"

*Evidence.* [SD6] measures "the probability that a candidate carries a late barrel-timing hit … on the same samples
with pile-up" (l.486–487). It is closed against a direct conditional with ≥ 30 counts before the cut (l.488–492). The
book's late fraction is ≈ 10⁻⁴ per window edge (D3 l.216–217, "up to 4 decades in that category"). With 2,000 overlays
per topology (l.360) the direct conditional has 0 expected passes. The rule then gives "credit only as a measured
no-PU number" (l.491–492), but the late hit comes from pile-up, so a no-PU number does not exist. The likely outcome is
no credit. Yet with the floors of B-1 this credit is the single largest lever: it could take the SR-T floor from about
10² to below 10⁻¹. STR itself flags that it "can move the SR-T background by orders of magnitude" (l.1198–1199).
*Fixed looks like.* Measure the conditional at hit level: the late-hit density in the BTL from all pile-up BTL hits
(thousands per event, so per-cent precision from the existing C1 events), times the candidate's BTL footprint. Close
it on loose candidates (R04: 171.55 groups per trial, l.249) by **widening the time window** until the direct fraction
is ≈ 10⁻². Pre-register the scaling law in the window width as the closure statistic. Then apply it at the nominal
window. Cost ≈ 5 CPU-h of re-analysis. This also answers D3 §6 item 2.

### B-16 (B) Thinning: deep reach, and the independence of the occupancy model

*Evidence.* "Whether thinning reaches R07 with 6,000 ρ = 2 trials is not known" (l.450–452). The reach of thinning is
set by the number of thinned draws per stored ρ = 2 candidate set and their correlation, not by the trial count alone.
STR does not specify the draws, the effective sample size (bootstrap over events), or the deepest rung expected to
have ≥ 20 effective counts. If thinning stops at R06 ([DT2]), B2-b (the agreement at deep rungs that is the only
cross-validation beyond R07) cannot be evaluated (l.442–445). Separately, the occupancy model is called independent
of the finder (l.429–430) but uses "the measured conditional for the fit-probability rungs" (l.429) without saying
from which population. If that population is finder candidates, the independence is partial.
*Fixed looks like.* Specify K draws per trial, effective N and the projected deepest rung (from the v1 ρ = 2 rates at
R04–R06, l.250). Name the source of the fit-probability conditional; if it comes from finder candidates, say that the
occupancy model is independent "for the counting and width rungs".

### B-9 (B) Multijets: the population on which P(r | multijet) is measured

*Evidence.* Multijets are generated with p̂T-biased weights at generator level (10⁷ × 10 ms, l.545), and validation
asks for "≥ 100 effective events passing" (l.530). The track-plane probability P(r | process) needs no-PU or hit-level
events *of that process passing the trigger and offline MET selection*. For multijets these are the ≈ 100 effective
events, so the term would be a zero-count bound at M ≈ 100: N_trig,MJ × 1.14×10⁻². That could become a new leading
floor. STR does not say how this is avoided.
*Fixed looks like.* Pre-register a factorisation P(r | MJ, MET > 250) ≈ P(r | MJ, looser MET or jet-pT-matched
population). Test it on Z(νν) and W samples (P in MET bins, which needs no new sample), with its closure criterion.

### Opportunities the strategy leaves unused

- **Late-hit credit:** included ([SD6]) but not in a testable form (B-5).
- **Paired comparisons on signal rows:** not used where they matter most, in B6 (C-2). STR is right that C1 cannot be
  paired against v1 (l.232–236).
- **v1 per-row records** (`AN1/signal_rows_a2.npz`: rows × 23 rungs × 20 FB columns, D4 l.306–308) are public to the
  study. They can project T2 before the freeze (C-3).
- **No-PU hard-scatter samples for B5** (B-6) and for B6 propagation (B-7): cheap, already planned, reusable.

---

## 3. Focus 2 — resolving power and honest framing

### B-2 (B) Size and power of the closure battery

*Evidence.*
- Criterion (a) is applied to the point estimate (l.215). For a perfect estimator (true r = 1) with s_P = 0.1, the
  false-fail probability is **9.8 % at N = 20 and 5.1 % at N = 30 for F = 1.5**; for F = 2 it is 0.5 % at N = 20
  [R: calc]. F = 1.5 is used for B3 (≥ 30 counts *before* the cut, l.490), B5 (R07 "if ≥ 20", l.562–563) and B2.
- B3's threshold counts the population before the cut. For a conditional of 0.1, n = 30 means k = 3 after the cut and
  sd(ln) ≈ 0.58 [R: calc]. A factor-1.5 test is then meaningless in both size and power.
- [SD8] makes a selection eligible only if *every* applicable criterion passes (l.678–679). At p > 0.05 per test, the
  probability that a perfect analysis passes all tests is 0.66 for 8 tests, 0.54 for 12 and 0.36 for 20 [R: calc].
  C1 uses Bonferroni (l.270); the closure battery has no family-wise statement at all.
- Positive: applied retroactively to v1's broken thinning (ln r = 0.406, 0.474, −0.455, −0.954; l.413–414, l.251),
  criterion (a) fails at all four rungs. So the battery *does* reject the known-broken estimator. Criterion (b) alone
  would not: with s_model at its cap ln 1.5 it gives χ² = 9.2 on 4 dof, p = 0.057, a pass [R: calc]. The resolving
  power therefore lives in (a) and in the cap (c). That is worth saying in the prereg and in the paper (it is a
  ready-made answer to referee Q3).
*Fixed looks like.* For each closure test, the prereg lists: N expected, σ_ln expected, probability of a false fail
at r = 1, and power to detect r = F. Thresholds are set in counts *after* the cut (e.g. N ≥ 55 for F = 1.5 so that
ln 1.5 ≥ 3σ, N ≥ 20 for F = 2). Add a family-wise statement: the expected number of false fails over the battery
relevant to the chosen selection, with a rule (e.g. Holm over that family, or "a failure with 0.05/K < p < 0.05
triggers investigation and a pre-reserved fresh closure sample, not immediate ineligibility"; see B-13). Do not loosen
F. Report the retroactive v1 test as the demonstration of power.

### B-3 (B) Trend tests: low power for B1, discontinuous rule

*Evidence.* B1-b: slope "compatible with zero (|slope| < 2σ) or its extrapolation … added to the width in full"
(l.377–378); B2-c is the same. With the expected precision at R05–R07 for DIF (≈ 970 / 150 / 18 direct counts,
s_P 0.05–0.1) the slope error is **0.097 per rung**. A slope of 0.19 per rung passes, yet extrapolated to R14 it is
1.3 and to R17 1.9 in ln. The 1σ extrapolation alone is 0.68 (R14) and 0.97 (R17) [R: calc]. For B2 the slope error
is 0.029, so the test has power there. The rule adds nothing below 2σ and everything above it, which is discontinuous.
Rung index is also not a physical variable across families (width R05–R08, χ² R09–R11, 2S R12–R14, shape R15–R20,
l.75–79); v1's trend produced the 1.26–6.31 widths the plan wants to remove (D4 l.255–256).
*Fixed looks like.* Always add σ_slope × Δrung (in quadrature) for the factor that is actually extrapolated; that is
C_PU, since P_geo is measured directly at depth. Fit the trend within a cut family, not across families. State the
resulting width at each T2 candidate in the floor table of B-1. This is honest in both directions: it is small for
B2 and real for B1.

### B-6 (B) The road-rotation sideband test is dominated by flat pile-up candidates

*Evidence.* B5 closes the sideband prediction on SM samples with pile-up (l.561–563). In those samples the hard-scatter
share of candidates is 19.52/(19.52+171.55) = 10 % at R04, 8 % at R05 and 6 % at R06 (l.249, l.256) [R: calc]. Pile-up
candidates are flat by symmetry (l.554). A hard-scatter non-flatness of ×2 moves the total by 1.06–1.10, and ×5 by only
1.25–1.41. **Both pass F = 1.5.** The test cannot detect the effect it exists to measure. Also, with [DP1] the
expected R07 count per process falls to 10,500 × 7.29×10⁻⁴ = **7.7** (full: 27.7), so R07 drops out of B5-a under its
own ≥ 20 rule. STR's statement of the loss (l.569–572) misses this [R: calc].
*Fixed looks like.* Define B5-a/b on the **truth-attributed hard-scatter component** (v1 already attributes counts;
C′_PU, l.254). Measure the hard-scatter T(Δφ to MET) on the **no-PU hard-scatter samples** already planned for B4
(10⁶ per process, l.506; road rotation costs only the finder on a few hits). This recovers far more than DP1 loses.
Keep the PU-overlay sample for road independence (B5-c) and PU flatness. Restate the DP1 loss including R07.

### B-12 (B) [SD8] "leading term" loophole

*Evidence.* Eligibility looks at closure verdicts of terms "above 10 % of its total background" (l.678–679). For B1
"selections for which that term is among the leading ones are not eligible" (l.389–390). The size used to decide
"leading" is not specified. A failed estimator that *under*-predicts can make its own term non-leading, and the
selection then becomes eligible on the strength of a failed method.
*Fixed looks like.* For terms with a failed criterion, decide "leading" with their conservative value: the direct-count
bound at that selection, or the v1-style bound. Use the same value in the likelihood if the selection is shown.

### B-13 (B) What happens when a closure fails after the freeze

*Evidence.* STR: "A failed criterion is reported as failed … not patched by a scale factor" (l.220–221); changes after
the freeze need "a dated addendum with a background-method or physics reason" (l.982–983). JFC lists "closure test
failure (p < 0.05)" as a concrete regression trigger, with ≥ 3 documented remediation attempts (CLAUDE.md, Phase
Regression; 03-phases "Accept a limitation ONLY when …"). STR does not say how these combine. Concretely: is a code bug
found in the failing estimator fixed? If so, is the fix re-tested on the same closure sample, which has now been used
for diagnosis?
*Fixed looks like.* A three-branch protocol in §8 item 10. (i) A regression ticket and investigation always.
(ii) If a bug is found, an addendum, and the corrected estimator is re-closed on a **fresh** independent sample;
reserve this in the 20 % contingency (one fresh B2 direct sample is 403 CPU-h, l.473; the contingency is ≈ 655 CPU-h,
l.1103). (iii) If no bug is found, it is reported as failed and [SD8] applies. This makes "reported as failed, not
patched" concrete and JFC-compliant.

### Outcome table: does the paper stand in each case?

Yes in outline (l.687–688, l.405–407, l.1231–1241). Two improvements are in C-4: an always-eligible baseline, and an
outcome-to-paper matrix for *partial* failures (e.g. B2 passes, PV-pair B1 fails, which removes every deep selection
because PV pairs lead from R06 on, Table 2.1 l.111).

Framing points that are fine as written: DP3 is called a cross-check, not an approach; v1 freeze timing is disclosed
(l.1001–1006); the T_seed non-convergence is called an efficiency statement (l.318); the endcap ×1.5 provenance is
flagged (l.1210–1211) without reopening brief D1.

---

## 4. Focus 3 — prioritisation and schedule

- **Critical path is right in order** (C1/C2 → estimator development → freeze → B2/B1/B4 → verdicts → Gate B,
  l.1120–1121). The day-0 ρ = 2 memory and storage measurement (l.456, l.1111) is the right first job.
- **Cheapest high-value items are not all early.** The no-PU floor measurements (B-1), the enrichment pilot and the
  time-tag hit-level measurement (B-5) are cheap and decide the outcome row. They belong in Phase 2–3 development, so
  that decision point 2 (l.1112) can also ask "is the target reachable?".
- **Idle capacity before production.** At the strategy's own 130 core-h per day in development (l.1078–1079): Phase 2
  offers 6 × 130 = 780 core-h against 646 planned, Phase 3 offers 7 × 130 = 910 against 190, and the freeze offers
  2 × 130 = 260. That leaves **≈ 1,100 core-h idle**, about 5.5 production days [R: calc]. Brief D7 forbids
  production samples before the hash, and I do not propose reopening it. Within D7 this capacity can (i) make the
  development samples 5–10× larger, so decision point 2 has real power at R05–R06 (a failure after the freeze is the
  most expensive outcome), and (ii) run the B-1/B-5/B-7 pilots. See C-6.
- **Levers "listed, not proposed" (l.1154–1161):** I agree with not proposing them. Lever (ii) (B2 direct at 12,000)
  takes the R07 σ_ln from 0.12 to 0.17 (l.449). That pushes the B2-a test toward the false-fail regime of B-2, for a
  saving of 1 day. Levers that shorten the critical path *without* touching a MUST criterion exist: toy parametrisation
  (B-14) and paired B6 (C-2). These should replace the listed ones in §11.6.
- **DP1 / DP2 loss quantification.** DP1 misses the loss of R07 (B-6) and overstates the importance of road
  granularity once the hard-scatter non-flatness is measured on no-PU samples. DP2 quotes the unpaired binomial error
  (6 % → 10 %; I reproduce ≈ 5.2 % → 8.2 % pooled at ε = 0.2 [R: calc]). With common-random-number pairing the reduced
  sample would likely be better than the unpaired full one (C-2), so DP2's stated loss is conservative rather than
  understated. That is acceptable, but it should be said.
- **Development effort is not modelled.** PLAN puts B1–B4, T1 and T2 at about 35–50 person-days (PLAN l.298, l.317 and the B3–T2 entries to l.366); STR
  gives them 7 calendar days (l.1112) and models CPU only. v1 moved fast with agents (D6 §1: Stage 4 plan to result in
  about 4 days), so 7 days is not impossible, but it is the real schedule risk, together with ITERATE cycles. STR says
  "1–2 days each" but does not include any in the 6 weeks (l.1122). See C-6.

### B-14 (B) Toy budget and the nested T1-g test

*Evidence.* The budget has 174 CPU-h of toys (l.643–644, l.1095: 181 in 4b/4c). One pass is 40 × 8 × 652 s = 58 CPU-h
per selection [R: calc]. But T2 re-evaluates "the three best by asymptotics … with toys" on the optimisation half at
4b (l.685–686), and T1-c/COMMITMENTS demand toys for chosen, runner-up and v1 fallback at 4c. That is **two passes**.
T1-g asks for the limit of each of 500 pseudo-experiments (l.654–657). If those limits are toy-based, it is a nested
toy computation (≈ 200 CPU-h per point at the FEAS_C unit cost). [L4] may double everything. The 4b and 4c windows are
3 and 2 days (l.1116–1117). So 4b/4c toys could be 350–700 CPU-h on the critical path.
*Fixed looks like.* Count both passes. Specify T1-g as asymptotic per pseudo-experiment, or as computed from the stored
test-statistic distributions without new toys. Then consider the saving: at one selection the background model is
identical at all 40 points, and the points differ only through S, its SR-T fraction f_T and the signal nuisances. Toy
limits can therefore be computed on a grid of f_T (e.g. 11 values), interpolated, and checked by exact toys at 3–5
points. That is a ≈ 4× saving, i.e. ≥ 100 CPU-h, about half a day on the critical path.

---

## 5. Focus 4 — statistics design (T1, T2)

Clear and largely adequate: on/off auxiliaries with no route double counting (l.633–635); correlations named
(l.628–632); toys primary and asymptotics validated (l.639–645); a T2 rule with a salted hash split that is
Λ-independent (l.692–697), a reproducibility check (T2-b) and a bias check (T2-c). What a referee would send back,
beyond A-1, B-2 and B-14:

### B-8 (B) Weighted samples in the Poisson auxiliary model

*Evidence.* B1 uses weighted primaries and Geant4 cross-section biasing with weight 1/k (l.363–368). Multijets use
p̂T slices with weights (l.546–547). T1 models "one auxiliary measurement per simulated count, m ~ Pois(λ)"
(l.613–614). A sum of unequal weights is not Poisson. A zero count in a weighted sample has a bound that depends on the
weight of the slice that would have contributed.
*Fixed looks like.* One auxiliary channel per generation slice (or weight class) of constant weight, which is exact.
Where weights vary within a class, use the effective-count (Barlow–Beeston-lite) form with n_eff = (Σw)²/Σw². For
zero counts, use the per-slice bound with the slice weight. State this in §4.11 and in prereg item (5).

Smaller T1/T2 points (C level): the G figure of merit uses asymptotic limits (l.682). With many zero-count auxiliaries
the asymptotic ranking may be unreliable. The "three best re-evaluated with toys" rule helps; state how often the
asymptotic top 3 contains the toy best (v1 ratios 0.32–1.07, l.641, suggest it may not).

---

## 6. Focus 5 — paper-readiness

**Flagship figures (l.1012–1020)** all have a data source and a phase. Fig. 6 and Fig. 7 depend on A-1 and B-1
(definition of the marked background and its width).
**Figure-scrolling test.** Planned outputs with no figure or diagram: C1 (41 comparisons; a pull summary is the
natural AN/appendix figure); C2 (Δn distribution, the answer to Q9); B6 (shift per variation, Q7/Q8); T1 pulls,
constraints and impact ranking (conventions checks 3–4, l.856–857; mandatory in the AN); S2 K(m) and the f₂₀₀ band
(Q17); the MET-model validation (B4 (a)–(c)); the BDT cross-check (the JFC approach comparison, [SD2]). Paper §8
(the data-driven recipe, PLAN l.218) has no dedicated figure: B5 is folded into Fig. 5. A T(Δφ) per process figure
should carry that section. See C-5.
**Referee questions (l.1036–1062):** all 25 mapped to items and sections. Q4's answer depends on B-4. Q3's best
answer is the retroactive v1 test of B-2. Q13 needs the v1-mode against v2-mode comparison at the best point (T1-b
provides it; make it a table in §7).
**Comparison targets (§6.2)** are sufficient for the limit and reach figures (FASER with HEPData, D0, Farina–Low, R1,
R2). See C-9 for one more and for R-10.

### B-10 (B) MET model validation (a) is partly circular

*Evidence.* The soft term is defined "with a resolution that reproduces v1's 25 GeV smearing" (l.522–523). Two lines
later its resolution is said to be a retrieval task from public Phase-2 documents (l.524–526). Validation (a) then
asks that the Z(νν) yield reproduce the v1 selection within 10 % (l.527–528). If the soft term is set from v1, (a) is
largely a consistency check of the model with its own input. The only external anchor is (c), a factor 3 on the
multijet share (l.530–531).
*Fixed looks like.* Fix the soft-term resolution from R-3 (sourced) only. Call (a) a consistency check. Add an
external validation: the model's MET resolution against a published Phase-2 MET-resolution curve (from the same R-3
source), with a pre-declared tolerance.

### B-11 (B) The MVA infeasibility argument is overstated

*Evidence.* "None of [the estimators] applies to an arbitrary score" (l.160–163). Repaired thinning re-groups thinned
ρ = 2 candidate subsets and can apply *any* candidate-level selection, including a score cut, to the thinned
candidates. P_geo is a pass probability of any selection on no-PU candidates; C_PU is selection-agnostic. Only the
occupancy model and the B3 conditionals are tied to named cuts. JFC requires the reviewers to validate this argument
(03-phases Phase 1; STR l.1206). As written, it would not survive a referee who knows thinning.
*Fixed looks like.* Restate the constraint with the reasons that hold. (i) Blinding: training on v2 signal before the
closure verdicts is forbidden (l.286–288, "any distribution of a variable for matched signal candidates"), so a
trained classifier cannot be a pre-registered candidate. (ii) The independent cross-validation of the pile-up term
(B2-b, the occupancy model) cannot be evaluated for a score, so a BDT selection would be ineligible under [SD8].
(iii) There is no training background beyond R08 (l.164–166). The conclusion (DP3) stands.

### B-7 (B) Detector variations do not reach the terms that lead the result

*Evidence.* B6: "Each is propagated to the pile-up rate at R04–R06 and to the signal efficiency" (l.579–580). From R07
on the leading terms are single-interaction and SM terms (l.123–125). The T1 nuisance list correlates resolution,
inefficiency and material "across signal and backgrounds" (l.629–630), but no item measures the background response to
resolution ×1.5 or material ×2 at the deep rungs. How a pile-up shift at R06 transfers to the chosen selection is also
not said.
*Fixed looks like.* Rerun P_geo for the leading topologies and SM processes under resolution ×1.5, inefficiency 97 %
and material ×0.5/×2: 10⁶ no-PU events per variation is ≈ 3.2 CPU-h at 11.5 ms (l.197), about 20 CPU-h in all. State
how the pile-up shift is carried to depth (through the occupancy model's per-layer response, which is analytic in
resolution).

### B-15 (B) Sub-item labels differ between STR and the binding COMMITMENTS

*Evidence.* STR B2-a = closure of each estimator, B2-b = agreement at depth, B2-c = trend (l.436–441). COMMITMENTS
B2-a = repaired thinning, B2-b = occupancy estimator, B2-c = agreement + trend, B2-d = direct sample. STR T1-a … T1-g
(l.647–657) against COMMITMENTS T1-a (schema + v1), T1-b (checks), T1-c (toys). STR B1-a … B1-e (l.373–388) against
COMMITMENTS B1-a … B1-d (B1-d merges geometry and Fatras physics). The same pattern holds for S2 (a–e against a–d) and
T2 (a–c against a–b). STR §5.1 cites "B2-c" as the trend test (l.830); in COMMITMENTS B2-c is the agreement test.
Phase 4a reviews against both documents (06 §6.4.1), so ambiguous labels make commitments unauditable.
*Fixed looks like.* One label set, with COMMITMENTS as the master and STR quoting its ids.

---

## 7. Category C suggestions

- **C-1 Gate-A decision sheet (one page).** The human needs: the 6-week calendar against the 2–4 week target and its
  cause (l.1154); DP1–DP5 with saving and loss (l.1140–1146, corrected per B-6); the seven judgment calls flagged
  YES/NO (l.1178–1206); the tolerances F and [SD8] with the false-fail numbers of B-2; the projected outcome row from
  B-1; the time-tag decision; the ×1.5 endcap wording; the v1 freeze-timing disclosure. Each item gets a default,
  the alternative and the consequence. §12.2 is close to this but mixes in non-decisions.
- **C-2 Paired designs in B6.** Run each variation on the same Stage-3 events, the same pile-up events and the same seeds
  for every unaffected component (common random numbers). The ratio error then scales with the discordant fraction
  rather than with ε. At R04 (ε ≈ 0.2) even a 10 % discordance gives ≈ 4.6 % on 1,200 rows, against 8 % unpaired
  [R: calc-level estimate, E]. That would let B6 cover all six points at the DP2 cost, removing DP2's loss (no
  5 keV, no ≥ 1 TeV, no scalar).
- **C-3 Use the public v1 row arrays before the freeze.** With `signal_rows_a2.npz` (pass flags per rung, D4
  l.306–307) and the floor table (B-1), compute G for the 16 candidates with v1 placeholders and its bootstrap spread.
  This checks that the "fewer cuts within 1σ" rule (l.684–685) is not decided by noise, and gives an expected T2-c
  shift. No v2 efficiency is involved.
- **C-4 An always-eligible baseline and a partial-outcome matrix.** Declare the deepest selection at which every
  leading term is directly counted (no extrapolating estimator; likely R06). It is eligible in every outcome, so the
  paper has a validated, if weak, limit even in "closure fails". Add a matrix: which estimator fails → which selections
  remain → which figures and abstract sentence change.
- **C-5 Figures.** Add to §9 (AN and/or paper appendix): C1 pull summary; C2 Δn histogram; B5 T(Δφ) per process (paper
  §8); T1 pulls/impacts; B6 shifts; S2 K(m) with scale/PDF band and f₂₀₀ band; MET validation; BDT ε_BDT/ε_R07.
  Map each to a referee question.
- **C-6 Schedule.** Use the ≈ 1,100 idle pre-production core-h (§4 above) for larger development samples and the B-1,
  B-5 and B-7 pilots. Start the B1 Geant4 geometry, B1-d material scan and hand-over code in Phase 2: they depend only
  on the ported chain and the installed Geant4. Start the T1 workspace builder on v1 counts (T1-b) in Phase 2 as well.
  Put an explicit ITERATE allowance (e.g. one per 4-bot review, +5 days) into the 6-week range.
- **C-7 Stale text.** "Geant4 installed on landau and maxwell … (one install slot each)" (l.402) and "Geant4 installs
  on two nodes" at day 0 (l.1111). Commit 199e166 records the Geant4 environment on all three workers, which gives more
  scheduling freedom. Update both, and [A7].
- **C-8 Dump storage.** Storage has hit dumps for 5,000 events (l.1129). B5 needs dumps of the B4 samples (l.572):
  8,500 events in full, 6,500 reduced (≥ 16–20 GB). C2 needs 700 and the occupancy model needs more. Either budget
  them or run the road rotations inline in the B4 jobs.
- **C-9 Comparison targets.** Add R2's Z+jets background after cuts (0.12 fb at 13 TeV, l.900) as a sanity comparison
  for the v2 SM term at the most similar selection, with the differences stated. R-10 (R2/R3 statistical methods and
  systematics, l.929) should close before Phase 4a, because Table 6.1's "not extracted" cells are binding inputs.
- **C-10 §11.6 levers.** Replace the three MUST-touching levers with the non-MUST levers found here (toy
  parametrisation, paired B6, no-PU-based B5). Keep the honest statement that four weeks is not reachable.
- **C-11 Length and duplication.** §4 and COMMITMENTS repeat criteria with different wording (B-15). The prereg should
  quote one source. The 1,250 lines are justified for a binding strategy, but §0 should carry the projected outcome
  (B-1) and the three decisions with the largest consequence (F and [SD8], time tag, σ_norm from NLO).

---

## 8. Checks I made that passed (evidence)

| claim | STR line | my check |
|---|---|---|
| 7.05 decades | l.30–31 | log₁₀(1.2346×10⁶/0.11) = 7.05 |
| N_exp 15,774, μ/N_exp 789.7 | l.94 | 219.2 × 0.04764 × 3000 × 0.5035 = 15,774; 1.2458×10⁷/15,775 = 789.7 |
| V4-5 power 1.4 %, 11 %, 92 % | l.320–321 | P(≥ 48/50) = 0.014, 0.112, 0.922 at p = 0.85, 0.90, 0.98 [R: calc] |
| B2 R07: 70 counts, σ_ln 0.12, resolves ln 1.5 at 3σ | l.447–448 | 96,000 × 7.29×10⁻⁴ = 70; 1/√70 = 0.12; 0.405/0.12 = 3.4 |
| B5 cost 520 / 163 CPU-h; ×1.9 | l.567–571 | (152,000 + 8,000) × 11.7 s = 520 h; (42,000 + 8,000) × 11.7 s = 162.5 h; √(38,000/10,500) = 1.90 |
| S1-d 15 % at ε = 0.045 | l.723 | √(0.045 × 0.955/1000)/0.045 = 14.6 % |
| T1-g ± 4.5 % | l.656–657 | 2√(0.25/500) = 4.47 % |
| Trigger 0.974 | l.768 | 0.98 × ½[1 + erf(2.5/√2)] = 0.9739 |
| Toys 58 CPU-h per selection | l.643 | 40 × 8 × 652 s = 57.96 h |
| §11.6 savings 158 / 201 / 56 | l.1157–1159 | 15 × 1,500 × 25.2 s = 157.5 h; 12,000 × 60.4 s = 201 h; 8 × 1,000 × 25.2 s = 56 h |
| Weekly slots 1,851 | l.1073 | 5 × 255 + 576 = 1,851 |
| Conventions enumeration | §5.1–5.2 | every row of `conventions/search.md` has WI or a reason; "background shape" and "data/MC detector" are translated with a stated replacement. Complete (06 §6.4.1). |
| Reference analyses | §6.1 | four tabulated (R1–R4) with source lines; method parity argued (l.884–891). Meets Phase 1. |

---

## 9. What "PASS-ready" looks like (for the arbiter)

1. A-1 resolved in the §4.11 text, with the limiting-case test added to T1.
2. B-1: definitions, floor table, enrichment pilot and no-PU reallocation in §4.4/§4.7/§11.2; projected outcome in §0.
3. B-2/B-3: size and power per closure test, family-wise statement, thresholds counted after the cut, and the
   continuous trend width, all in §4.0 and the prereg outline.
4. B-4 … B-16: text changes of 0.5 h to 0.5 day each, with small CPU (≤ 50 CPU-h in total) for B-5, B-6 and B-7.
5. COMMITMENTS relabelled to one id set, and the changed criteria propagated.
None of these reopens a fixed user decision (brief §3) or touches a MUST statistic downward.
