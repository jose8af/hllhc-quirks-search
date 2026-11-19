# C′_PU attribution: v1's link rule vs the frozen own-hit rule j ≥ n/2 — result

Eskil (executor, Opus), 2026-11-19 15:47 -0500. Plan (committed before counting): `CPU_ATTRIB_PLAN_eskil_2026-11-19.md`
(ae78ae5). Commitment: STR l.752-754; advisor ruling LOG.md 2026-11-19 15:37. Script `src/cpu_attrib.py`, output
`cpu_attrib_eskil_2026-11-19.json`; run on landau, nice 19, 73 s wall, 0.02 CPU-h (two runs ≈ 0.04 CPU-h in all).
No signal file was opened.

## 1. Headline
**Almost none of v1's C′_PU-attributed candidates are attributed by the frozen rule.** v1's rule (≥ 3 core links in
≥ 3 layers from ≥ 2 toy particles) mostly selects pile-up planes that hold a few toy hits. The frozen rule asks for
≥ 4 IT/PS layers whose double crossing is made of toy hits alone.
- **DIF: 0 of 141 at R05 and 0 of 348 at R04** [VERIFIED]. Every v1-attributed DIF candidate has max_cross = 1: the DIF
  particles never make even one double-crossing layer, so the result does not depend on how merged hits are labelled.
- **γ conversions: ρ = 10/174 = 0.057 at R05 and 1/11 = 0.09 at R06** [VERIFIED counts]. All j ≥ 4 candidates come from
  **one source event** (1 of 22 v1 clusters at R05, 1 of 6 at R06).
- **V⁰: ρ = 26/612 = 0.042 at R05** (4 of 91 clusters) **and 1/11 at R06** [VERIFIED].
- **PV pair: 0 of 131 at R02 and 0 of 4 at R04** [VERIFIED].
- Not one candidate passes j ≥ 4 without also passing v1's rule: the frozen set is a strict subset here.

## 2. Inputs and checks
- C1 reproduction samples (all jobs `done` per their markers): `p2-a-c1-cppua` DIF / γ / V⁰ with 1,000 slots each,
  from 1,000 / 500 / 500 source C′₀ events (clusters); `p2-a-c1-cppub` PV pair with 2,000 slots from 500 sources.
- **The v1-rule counts reproduce c1_compare's cprime_term exactly** (`c1_compare_mattias_2026-11-19.json`):
  DIF 348 / 141, γ 420 / 174, V⁰ 1,493 / 612 at R04 / R05, and PV pair 131 at R02 [VERIFIED].
- Hit-record crossings recomputed with the layer/side map agree with the stored `cand.cross` for all 344,378 records
  (0 bad). The rung flags of `cp.cand` and `cand` agree (0 mismatches). Every v1-attributed R04 candidate is among the
  stored candidates [VERIFIED].
- **Merged hits.** A merged pool hit carries the INT of its largest-dE member (v1 `g1b_tt.assemble` l.78-83; Björn used
  the same label for the SM). Among v1-attributed candidates that have a record, the number of own-INT hits is about
  equal to the number of v1 pre-merge core links: 1,174 vs 1,173 (DIF), 2,882 vs 2,881 (γ), 8,112 vs 8,277 (V⁰). So the
  labelling hides at most ≈ 2 % of own hits [VERIFIED]. j is computed on all of the candidate's band hits.
- **Coverage.** v1 writes full hit records only for R04 candidates with w_core < 37.5 or p > 10⁻³. R05 and R06 are
  therefore complete. At R04, j is known on the recorded subset (§3 note b).

## 3. Counts (candidates; slots M as given; clustered over source C′₀ events, 4,000 bootstrap replicas)
| class (M) | rung | N_v1 | N_j (j ≥ 4) | overlap | v1 only | j only | clusters v1 / j | ρ = N_j/N_v1 | ρ bootstrap 16/50/84 % | event-level 95 % UL on ρ |
|---|---|---|---|---|---|---|---|---|---|---|
| DIF (1,000) | R04 | 348 | 0 (b) | 0 | 348 | 0 | 69 / 0 | 0 | 0 / 0 / 0 | < 3.0/69 = 0.043 |
| DIF | R05 | 141 | 0 | 0 | 141 | 0 | 47 / 0 | 0 | 0 / 0 / 0 | < 3.0/47 = 0.064 |
| DIF | R06 | 0 | 0 | — | — | — | 0 / 0 | n/a (v1: 2/500) | — | — |
| γ (1,000) | R04 | 420 | 10 (b) | 10 | 410 | 0 | 23 / 1 | 0.024 | 0 / 0.022 / 0.049 | < 4.74/23 = 0.21 |
| γ | R05 | 174 | 10 | 10 | 164 | 0 | 22 / 1 | 0.057 | 0 / 0.051 / 0.116 | < 4.74/22 = 0.22 |
| γ | R06 | 11 | 1 | 1 | 10 | 0 | 6 / 1 | 0.091 | 0 / 0.077 / 0.20 | < 4.74/6 = 0.79 |
| V⁰ (1,000) | R04 | 1,493 | 26 (b) | 26 | 1,467 | 0 | 118 / 4 | 0.017 | 0.0075 / 0.017 / 0.028 | — |
| V⁰ | R05 | 612 | 26 | 26 | 586 | 0 | 91 / 4 | 0.042 | 0.018 / 0.040 / 0.067 | < 9.15/91 = 0.10 |
| V⁰ | R06 | 11 | 1 | 1 | 10 | 0 | 5 / 1 | 0.091 | 0 / 0.077 / 0.21 | < 4.74/5 = 0.95 |
| PV pair (2,000) | R02 | 131 | n.e. (c) | — | — | — | 26 / — | — | — | — |
| PV pair | R04 | 4 | 0 | 0 | 4 | 0 | 2 / 0 | 0 | — | — |
| PV pair | R05, R06 | 0 | 0 | — | — | — | — | — | — | — |
| NI | — | **not measured: no C′_PU NI sample in C1** (only `c1cp0-ni22` at C′₀) | | | | | | | | |

**Statistics.** Counts are VERIFIED. ρ and its quantiles are VERIFIED as computed. For γ, 37 % of the bootstrap
replicas give ρ = 0. The **event-level UL** is the Poisson 95 % upper limit on the number of clusters that hold a
j ≥ 4 candidate, divided by the number of clusters with a v1 candidate (ESTIMATE: it treats each source event as one
unit).
(b) **R04 is a bracket.** The R04 numbers count j only on recorded candidates. Of the v1-attributed R04 candidates,
207 (DIF), 246 (γ) and 881 (V⁰) have no record. For DIF all have max_cross = 1, so j = 0 holds for them too
[VERIFIED]. For γ and V⁰ the R04 N_j is a lower bound. A loose upper bound from the links (max_cross ≥ 2 and ≥ 4 link
layers) is 317 (γ) and 918 (V⁰); in the complete R05 sample that same bound is 162 and 452, against 10 and 26 that
actually pass.
(c) Below R04 only a 1 % sample has hit records, so the PV pair at R02 is NOT EVALUABLE for j. At R04 its 4
v1-attributed candidates have max_cross = 1, so j = 0.

**j of the v1-attributed candidates at R05** (j = 0 / 1 / 2 / 3 / 4 / 5):
- DIF: 141 / 0 / 0 / 0 / 0 / 0.
- γ: 59 / 51 / 35 / 19 / 1 / 9.
- V⁰: 413 / 95 / 63 / 15 / 20 / 6.

Under STR l.747-751 this sorts them into pure pile-up (j = 0), mixed (1 ≤ j < 4) and attributed (j ≥ 4):

| class | pure pile-up | mixed (no term; bounded by the completeness test) | attributed |
|---|---|---|---|
| DIF | 100 % | 0 % | 0 % |
| γ | 34 % | 60 % | 6 % |
| V⁰ | 67 % | 28 % | 4 % |

## 4. What this implies (all ESTIMATE; v1 placeholder efficiencies as in Gate A)
**Gate A conversion-based range** (GATE_A.md l.12-20). The range rests on STR (α1′): conversions 9,530 of the total
9,929–10,193 (central), from v1's γ counts 86 / 13 / 2 per 500 at R05 / R06 / R07, plus DIF 385–647 from v1's 2 / 1.
- Scale factor for the conversion term as an attributed term: ρ_γ ≈ 0.06 (R05) to 0.09 (R06). The clustered 68 %
  interval is 0–0.12 at R05, and the event-level 95 % UL is ≈ 0.22. All of it rests on one source event.
- DIF: ρ ≈ 0, with an event-level UL of 0.064 at R05.
- **Attributed background ≈ 5×10²–9×10² events** (conversions 540–870 plus DIF < 40), instead of 0.7–1.0×10⁴. At the
  95 % UL it is ≈ 2.1×10³. It reaches 0 in 37 % of the replicas.
- The rung-to-rung fall under the frozen rule (γ 10 → 1 for R05 → R06) is not measurable on this sample. Whether
  conversions fall faster than pile-up stays open.
- The same factor applied to Gate A's day-15 projection (B₅₀ ≈ 3×10⁴–3×10⁵, which extrapolates the conversion counts)
  gives ≈ 2×10³–2×10⁴, still above 300. **The expected pause stands at the central value, but less firmly:** at the
  lower edge of ρ it could fall below.
- **Caveat that dominates the reading:** the scale factor shrinks the *attributed term*, not the selected background.
  60 % (γ) and 28 % (V⁰) of v1's conversion candidates become **mixed**: no term, and their size enters only through
  the completeness test (STR l.751-752). Another 34 % / 67 % become pure pile-up (B2), which the pile-up-only trials
  measure without the toy. Gate A's range carries over as an upper envelope of attributed + mixed + pure pile-up. It
  does not carry over as a term size. How much of the mixed part the completeness test lets through is not measured
  here.

**Expected test counts** (STR l.1047-1068, Table 4.4b):
- **DIF 31 at R06.** This number assumed H(R06) ≥ "the attributed fraction with pile-up, 0.004" (l.1048) from
  v1's rule. Under j ≥ 4 the attributed fraction with pile-up is 0 of 1,000 slots already at R04 and R05 (event-level
  95 % UL 3.0×10⁻³ per slot). So the **lower bound 0.004 is void**, and the expected attributed count on the 1,000
  unbiased test overlays at R06 is ≈ 0 (< 3; 31 × 0.064 ≈ 2 at the UL). The N_scan ≤ 10⁶ sizing and the 7,750-event
  fallback rest on that bound. With 0 attributed DIF expected, the DIF ceiling test at R06 has essentially no power. H
  itself (the no-pile-up own-hit ceiling) is not affected by this measurement.
- **NI 92 / 120 / 378 at R05.** NOT MEASURED: there is no NI C′_PU sample. By analogy (NI secondaries are few-prong
  like V⁰, or single tracks like DIF), ρ_NI ≈ 0–0.05, giving ≈ 0–5 / 0–6 / 0–19 attributed at R05 instead of
  92 / 120 / 378 [ESTIMATE, analogy only]. A direct measurement needs a C′_PU ni22 run on the existing C′₀ ni22
  outputs: ≈ 1,000 slots, 25 jobs of ≈ 17 min, ≈ 7 CPU-h (ESTIMATE, from the cppua job times). That is above my
  2 CPU-h limit and was not run.

## 5. Open issues / flags for the orchestrator
1. The γ and V⁰ ratios rest on 1 and 4 source events. A tighter ρ_γ needs more C′_PU γ sources: today there are 500,
   and v1 had the same sample size.
2. The NI C′_PU run (≈ 7 CPU-h) needs approval if NI test counts must be measured rather than assumed.
3. The STR §4.4 DIF and NI ceiling-test sizing (31; 92 / 120 / 378) used v1-rule counts, so it is a strategy-revision
   input in the same way as Björn's SM-tag finding. The DIF R06 test and the NI R05 test are expected to have
   ≈ 0–20 attributed events, not tens to hundreds.
4. The v1 rule sits at g1b_tt.py l.354-355 in the tree as read (the prompt cites l.356-357); the logic is as
   transcribed in the plan.
