# C′_PU attribution: v1's link rule vs the frozen own-hit rule — plan

Eskil (executor, Opus), 2026-11-19 15:40 -0500. Commitment: STR l.752-754 ("C1 uses v1's rule, and the difference is
measured on the C′_PU samples"); advisor ruling LOG.md 2026-11-19 15:37 (do it before Phase 3 sizes anything).
Written before any count was read.

## Samples (C1 reproduction, channel (i); all jobs done per their markers)
- `p2-a-c1-cppua`: DIF, γ conversion, V⁰ — 25 jobs × 40 slots = 1,000 slots each (PU 200 overlay of preselected C′₀
  events, slots re-use source events cyclically).
- `p2-a-c1-cppub`: PV pair — 50 × 40 = 2,000 slots.
- NI: no C′_PU sample exists in C1 (`p2-a-c1-cp0` has ni22 at C′₀ only) → NI is reported as NOT MEASURED; any NI
  statement is an ESTIMATE by analogy with the measured classes, labelled as such.
- No signal file is opened.

## The two rules, exactly
**v1 C′_PU rule** (`stage2_C001_quirks/theory_track/acts/stage4/finder/g1b_tt.py` `attribute`, l.344 and l.354-355 in
the tree as read; the prompt cites l.356-357). For a candidate with at least one toy (vp = GUN_VP = 3500) row among its
band hits: take its core hits (`core_mask`), collect the pre-merge toy measurements merged into those core pool rows
("links"), keep links with |(x − PV)·n| ≤ 4 σ̂ (NSIG_ATTR = 4). Attributed iff #links ≥ 3, #distinct layers of the
links ≥ 3, ≥ 1 link in an IT/PS layer (LC ≤ 6), and ≥ 2 distinct toy particles (not looper). Stored per candidate as
`cp.cand.attributed` (records exist for every attributed candidate and every near miss with ≥ 2 links).

**Frozen own-hit rule** (STR l.747-753). n(r) = number of double-crossing layers the rung requires: n = 7 at R04–R06
(N_IP2 ≥ 7 over the 7 IT+PS layers). j = number of the candidate's IT+PS layers with a double crossing made of own
(toy, INT mod 10⁶ = 3500) hits alone: IT layer ≥ 2 own hits; PS layer ≥ 2 own hits on each sensor side (v1's
`crossings` definition, as in Björn's `review_bjorn_v1tag.py`). Attributed iff j ≥ n/2, i.e. j ≥ 4. Computed on the
candidate's full band hit record (`hit.*`, merged pool hits; a merged hit carries one INT).

**Coverage.** v1 at ρ = 1 writes full hit records for R04 candidates with w_core < 37.5 or p(χ²) > 10⁻³
(`production.py` l.400). So R05 and R06 are complete for j; at R04 j is known only on the recorded subset → R04 is
reported as a bracket [recorded j ≥ 4, recorded j ≥ 4 + unrecorded R04 candidates], with the coverage fraction.
Self-check: recomputed crossings from the hit record must equal the stored `cand.cross` (all hits).

## Rungs
R04 (N_IP2 ≥ 7), R05 (w_core < 37.5), R06 (w_core < 18.75), from the stored rung flags (`cand.rungs` /
`cp.cand.rungs`, nested, aligned). PV pair also at R02 if counts exist (v1 used R02 for it), with the same coverage
caveat (no hit records below R04 except the 1 % sample) → PV pair j at R02: NOT EVALUABLE unless covered.

## Statistic and error
Per class t and rung r, over the M_t slots: N_v1 = candidates passing r with the v1 rule (= cprime_term's numerator),
N_j = candidates passing r with j ≥ 4, N_both = overlap, also N_v1only, N_jonly, and the number of slots with ≥ 1.
Main statistic: ρ(t, r) = N_j / N_v1 (ratio of per-slot rates on the same slots). Error: clustered bootstrap over
source C′₀ events (cluster = `cp.ev[:, 1]`, the cluster of c1_compare `cppu_clusters`), 4,000 replicas, report the
16/50/84 % quantiles of ρ and s(ln ρ); for small counts also the exact conditional binomial interval on N_both-split
(unclustered, labelled). Check: N_v1 per class and rung must equal c1_compare / cprime_term's C′_PU factor.

## Implications (to be stated, ESTIMATE)
- Gate A conversion-based range (GATE_A.md l.12-20; STR (α1′) conversions 9,530 from v1's γ 86/13/2): scale factor
  = ρ(γ, R06) (and R05, and the R05→R06 fall under each rule).
- DIF test count 31 at R06 (STR l.1033-1048, H(R06) ≥ 0.004 from v1's 2/500): × ρ(DIF, R06).
- NI 92/120/378 at R05: no C′_PU NI sample; analogy only.

## Compute
One read job on landau (nice 19, ≤ 30 min, ≈ 0.1 CPU-h), SLOTS.md line first.
