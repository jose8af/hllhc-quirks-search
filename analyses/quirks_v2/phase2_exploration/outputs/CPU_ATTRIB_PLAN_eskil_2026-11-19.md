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

## Addendum (2026-11-19 15:55 -0500, before generation): NI C′_PU sample — approved by the orchestrator (≈ 7 CPU-h, hard limit 9)
- **Definition.** v1's C′_PU NI as used by cprime_term: topology `ni22` (NI at 22 mm; the only NI radius with C′₀ in C1,
  `p2-a-c1-cp0` c1cp0-ni22-000/001, 30,000 events, v1 CP_N). Run with `c1_cp_job.py --kind cppu --topo ni22 --sources auto`
  (v1 `run_g1b.run_cppu_job` unchanged, frozen configuration; stream c1.cpu; seed hash "qv2|c1.cpu|cppu|ni22|<chunk>").
  Sources = the preselected C′₀ ni22 events (v1 rule for preselected topologies), slots cycle over them.
- **Size.** 1,000 slots (as DIF/γ/V⁰ in C1; v1 had 500), 25 jobs × 40 slots, campaigns `p2-a-c1-cppuni-a` (jobs 0–12)
  and `p2-a-c1-cppuni-b` (13–24), split only so the halves can run on whichever node has room. ≈ 0.29 CPU-h per job
  (DIF cppu jobs: 1,033 s per 40 slots) → ≈ 7.2 CPU-h. Stop rule: after the first jobs finish, project; if the
  projection exceeds 9 CPU-h, stop the drivers (no new jobs) and ask.
- **Nodes.** SSH runner, absolute campaign paths, ≤ 2 jobs of mine per node on landau/schrodinger and ≤ 3 jobs in total
  on a node (Cecilie, Ulrika share them); maxwell not used. SLOTS.md line first.
- **Read.** The same `cpu_attrib.py` (topology glob extended to the new campaigns), same rules, same rungs; the
  statistic of the main plan (ρ = N_j/N_v1, clustered bootstrap over source C′₀ events, event-level Poisson UL).
  Main rung **R05** (the NI test rung, STR l.1059-1062); R04 bracket and R06 also reported.
- **γ from more source events: not possible at no extra cost.** v1's gun topologies make only C′₀ events g < CPPU_N = 500
  eligible as sources (`run_g1b.py` l.534); C1's 1,000 γ slots already use all 500 (two pile-up repeats each). More γ
  slots would only re-overlay the same 500 events, so the γ ratio stays on its current source events; this is stated,
  not run.
