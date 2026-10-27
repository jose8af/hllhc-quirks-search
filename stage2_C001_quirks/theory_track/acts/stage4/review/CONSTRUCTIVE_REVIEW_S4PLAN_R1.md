# Constructive review R1: Stage-4 plan (ACTS CMS-like tracker + PU 200), C001 quirks theory track

Reviewer: constructive R1 (fresh agent), 2026-10-13. Artifact: `acts/stage4/plan.md` (E9), with its probes
(`acts/stage4/probes/`), probe outputs (`data/acts_stage4/p0-p6/`) and `acts/stage4/E9_session_log.md`. Upstream I read:
`sim/stage3/HANDOVER_STAGE4.md`, `outputs/THEORY_GAPS_SYNTHESIS.md` (S-4, S-6) and the cached literature.

Approach: is this the best plan we can afford for a publication-grade result, and which concrete changes raise its value or cut
its risk or cost? The approved decisions (U-1…U-5, D4-1…D4-12) are **not** reopened. No finding below needs one changed:
every proposal works inside D4-1 (a), D4-3 (a), D4-4, D4-5 (a) and D4-6 (a).

Classification follows `jfc/src/methodology/03-review.md` §6.1. **A** = a correctness error (blocking). **B/C** = advisory.
B is a substantive improvement; C is minor.
Tags: **VERIFIED** = I recomputed it here (script named); **ESTIMATE** = back-of-envelope; **UNVERIFIED** = not checked
against the primary source.

**Re-computations** (≈ 3.5 CPU-min in total; acts/TT pixi env, read-only; scratch under
`data/acts_stage4/review_r1_constructive/`):

| Script | What it does | Cost |
|---|---|---|
| `r1c_pu_composition.py` (+ `.json`) | Reruns the probe-5 finder logic, imported read-only, on the 5 PU-200 events of probe p1. These SimHits carry particle ids. 4 roads per event, 20 trials. Gives the truth composition of the best PU candidates and the road overlap | 186 s |
| `r1c_pu_btl_time.py` | Delay of the PU BTL hits, and same-particle "doubles" per counting layer, from p1 | 2 s |
| `r1c_signal_handles.py` | On Stage-3 p2/BM template counting-set events (no PU): IT βγ, BTL delay and availability, plane-normal \|n_z\| | 2 s |
| `r1c_tof_mass.py` | Truth-level check of the S-4 mass recipe: BTL time of flight plus the pair momentum gives M_pair | 2 s |

---

## 0. Summary

The plan is strong and more rigorous than any published quirk phenomenology study on backgrounds (§1). The probes are honest,
and several pitfalls (Fatras pMin, molar-density units, φ-sectoring for CKF) were found and fixed before production.
I found **one Category A**:
- **A-1:** one multiplicity variable is defined so that it does not measure what the plan says it measures. VERIFIED. The fix
  takes minutes and must happen before `WP_RULE.md` is frozen.

and **eight Category B**:
- **B-1:** extrapolate in density by interaction multiplicity k, not with one fitted exponent α;
- **B-2:** a timing-tagged signal category with an ABCD-style factorisation that is measured, not extrapolated;
- **B-3:** an IT dE/dx proxy as an F1 variable;
- **B-4:** restructure A2 (≈ −80 CPU-h, exact Λ pairing);
- **B-5:** dedicated samples for correlated topologies;
- **B-6:** P2 deliverables: velocity observables and a sensitivity model;
- **B-7:** the roads are not disjoint;
- **B-8:** gate order and a stronger pilot.

There are also **seven Category C** notes. Together the B items turn the "≥ 4-decade extrapolation" from the analysis's weakest
point into a cross-checked estimate, and they free ≈ 80-120 CPU-h within the approved 450 CPU-h.

---

## 1. Literature comparison (question 1): how fake rates are estimated elsewhere

| Work | Pile-up / background treatment | Statistics, reach | What we take from it |
|---|---|---|---|
| Knapen, Lou, Papucci, Setford [1708.02243 Sec.III.D, IV] | ⟨μ⟩ = 50, minimum bias drawn from 125 × 10³ Pythia8 events. About 10⁻³ of background events have a plane with ≥ 1 hit in 4 of 8 layers, and 6 × 10⁻⁵ have one with ≥ 1 hit in every layer. The signal-region background is "derived by taking the distribution from events that are allowed to have 1-hit per layer, weighted by the overall efficiency of passing the more stringent requirement" (argued to be conservative through an anti-correlation). Conversions come from an MG Z(νν)+γ+j sample. They claim the residual can "easily be removed" with Δφ(MET, n₃) and/or dE/dx | ~10⁵ events. The SR rate is a loose-to-tight factorisation, not measured | Our §4.1 steps 1 + 3 are a strict superset (larger samples, PU 200, explicit closure). Their own suggested extra handles (MET alignment, dE/dx) are only half used here: dE/dx is missing (B-3) |
| Li, Li, Pei, Zhang [1911.02223 Sec.IV, Table I] | ⟨μ⟩ = 50 (Pythia A3). Hit pre-filter dE/dx > 3.0 MeV/cm: after the first iteration the background-hit fraction is 0.167 while signal keeps 0.965 / 0.933 / 0.910 (m = 200/500/800 GeV). Re-running Knapen's selection on Z(νν)+jets + PU, they find a ≥ 1-hit-per-layer plane in ~10⁻⁴ of events, "dominated by … two charged particles flying in a similar direction", and a conditional ~10⁻² for "all but one layer with 2 hits" | ~10⁴-10⁵ events | (i) dE/dx is the standard handle of the literature (B-3). (ii) The dominant fake is a **correlated** two-particle topology, not random hits (B-1, B-5) |
| Sha et al. [2410.00269 Sec.VI] | No PU ("Effects from pile-up remain to be studied rigorously in future work"). A χ²_quirk/χ²_helix ratio "removes all SM tracks in our samples" | small samples | A helix-vs-quirk χ² is our F1 non-helicity. Their background claim is statistics-limited |
| FASER [2607.26195, background section] | Data-driven **ABCD** on two variables taken as independent (scintillator charge QLC × timing ellipses): N_A = N_B N_C/N_D = 0.046 ± 0.010 (2022-23), 0.082 ± 0.014 (2024). The independence "was confirmed by subdividing various control regions" | data | The cleanest precedent for B-2: factorise between two **physically independent** handles (geometry × time) and test the independence in control regions |
| CMS disappearing tracks [2004.05153 §5.2, §6.1] | Spurious-track probability measured in Z→ee/μμ control samples with a d₀ **sideband** (0.05 ≤ \|d₀\| < 0.50 cm). The transfer factor ζ comes from a Gaussian + constant fit in the n_lay = 4 category and is **applied to n_lay = 5, ≥ 6** (too few events there). The ζ fit uncertainty is ±(43-52) %; the Z→ee vs Z→μμ difference (0-200 %) is a systematic | data | The experimental standard is a loose-to-tight transfer with a fitted shape and a large, explicit uncertainty. Our density ladder is the simulation analogue. Their tolerance of 50-200 % uncertainties on the spurious component is a useful benchmark for what reviewers accept |
| D0 quirk search [1008.3547] | Fake (random-hit) track background from a dE/dx **template** that "is significantly different" from real tracks | data | dE/dx shape as the fake discriminant |
| ATLAS ionisation HSCP [1808.04095] | data-driven dE/dx background (UNVERIFIED detail, not opened) | data | — |

**Verdict on question 1.**
- Our PU strategy (direct + density ladder + per-layer factorisation + pre-registered closure) is **stronger than every
  published quirk phenomenology estimate**. All of those use ≲ 10⁵ events at PU 50 and conclude "negligible".
- It is **weaker than experimental practice in one respect**. Experiments prefer factorising between independent observables,
  validated in control regions (FASER ABCD; the CMS sideband transfer), over extrapolating in a nuisance parameter (density)
  with a free exponent.
- The fix is not to replace D4-5 (a) but to:
  - give its density fit a physical form (B-1);
  - add an independent-handle factorisation where the detector allows it (B-2: BTL timing; B-3: dE/dx);
  - treat correlated topologies explicitly (B-5).
- The literature also points to the likely dominant residual: correlated particle pairs from one vertex [1911.02223], not random
  coincidences.

---

## 2. Findings

### A-1. "N_OT2 (≥ 2 hits per stacked OT layer)" is satisfied by a single particle (VERIFIED; blocking; minutes to fix)

**Evidence.**
- Plan §2.2 step 5 defines "N_OT1, N_OT2: OT layers (stacked pair = one layer) with ≥ 1 / ≥ 2 hits". The probes implement this
  literally: `p4_finder_proto.layer_of` maps `TBPS_Lk_in/_out` and `TB2S_Lk_in/_out` to one counting layer, and `refit` counts
  `nl2 = bincount(lc) >= 2`.
- A straight or curved track crosses both sensors of a stack, so **one particle already gives "≥ 2 hits"**.
  `r1c_pu_btl_time.py` on probe-p1 PU-200 SimHits shows that **99.5-99.7 %** of OT hits (TBPS L1/L3, TB2S L1/L3) come from a
  particle with ≥ 2 hits in that counting layer. The same fraction is only 0-1.1 % on TBPX L1-L4.
- In the best PU-only candidates of `r1c_pu_composition.json`, most N_L2 layers are met by one particle. Examples:
  - ev0/road0: N_L2 = 5, 3 of them single-particle;
  - ev3/road3: N_L2 = 5, 4 single-particle;
  - every top candidate has max-hits-per-particle ≤ 2 and is built from 4-16 particles from as many vertices.
- **Why it matters.** The two-particle requirement in the OT is where most of the random-coincidence rejection should come
  from. With the plan's own band occupancies (§2.1: TBPS L1 0.17, TBPS L3 0.029, TB2S L1 0.44, TB2S L3 0.115 random hits per
  band), Poisson gives (ESTIMATE):
  - P(≥ 1 particle in band) over these 4 OT layers = **1.8 × 10⁻⁴**;
  - P(≥ 2 particles in band) = **2.6 × 10⁻⁹**.

  The definition as written gives up ~5 decades of rejection, invalidates the plan's §2.1 reading ("PU N_L2 4-6 … consistent
  with" the band estimates), and puts a "second hit" that is 99.5 % the same particle into the per-layer factorisation
  (§4.1 step 3).
- It is a definition error in a variable whose *shape* §2.5 freezes before production, so it must be fixed now.

**Proposed change.** In §2.2 step 5 and §4.1 step 3, count **distinct crossings**, not hits:
- for a stacked layer, the number of in-band stubs (an in/out hit pair within a stub window), or simply the number of in-band
  hits on the *same* sensor;
- then N_OT2 = layers with ≥ 2 crossings.

The IT is unaffected. Keep the old count as a diagnostic. Check the signal efficiency of the new N_OT2 on A1 (no PU) at the
G2 gate.
**Cost:** < ½ h of code; 0 CPU.

### B-1. Density ladder: extrapolate by interaction multiplicity k, not with one fitted ρ^α (VERIFIED basis; strong)

**Evidence.**
- §4.1 step 2 fits P(r; ρ) = A_r ρ^{α_r} per rung. A single power law is the right form only if every passing candidate needs
  the same number of independent interactions.
  - The loose PU candidates are made of **4-16 particles from 4-16 distinct vertices** (`r1c_pu_composition.json`, field
    `n_vertices`).
  - The correlated topologies have k = 1: conversions, V0s, loopers, and two tracks from one vertex (the dominant source in
    [1911.02223]).
- A mixture of a k ≈ 10 combinatorial component and a k = 1 correlated one fitted with one α at ρ = 1.5-3 is dominated by the
  steep component. Scaling it down to ρ = 1 then **underestimates the linear component**, which is not conservative.
- The closure test (step 4) only probes rungs that are measurable, where the composition can differ from the tight rungs.

**Proposed change.** The chain already has full truth (`HitDump` stores vertexPrimary, particle, generation). Store per
candidate:
- the number of distinct PU interactions k contributing in-band hits;
- the number of particles, the maximal hits per particle, and a flag for the secondary generation (conversion/V0).

For a Poisson superposition of ρ × 200 interactions, the count of candidates built from k interactions scales as ρ^k (the
number of k-tuples). This holds up to competition among candidates, which shows up as a measurable deviation in the closure.
So:
- P(r; ρ = 1) = Σ_k N_k(r; ρ) ρ^{−k} from each density point separately, with **no fitted exponent**.
- Closure becomes:
  - (i) the k-spectra predicted at ρ = 1.5 from ρ = 2 (and 3) agree;
  - (ii) the reweighted ρ = 2 prediction of the loose-rung rate at ρ = 1 agrees with B1 directly.
- Keep A ρ^α as the alternative model for the systematic.

**Cost:** zero extra CPU (a few output columns); ½ day of analysis code. It may make the ρ = 3 point unnecessary (−37 CPU-h;
decide at G3, B-8).

### B-2. A timing-tagged category with a measured (not extrapolated) factorisation (VERIFIED inputs)

**Evidence (signal, truth level).** From `r1c_signal_handles.json` (template counting set, |η_pair| < 2.5, status 1):
- 45-59 % of events have a quirk BTL hit, and essentially all of them have a first-hit delay > 1 ns.
- Median first-hit delays are 3.1 / 9.0 / 15 / 27 ns at E 200/500/1000/1500 (consistent with synthesis S-6).

**Evidence (PU).** From `r1c_pu_btl_time.json` (probe p1, in-time PU 200, 1122 BTL hits/event), the fraction of PU BTL hits
with a delay (relative to a straight light-speed path from the beam line) of:
- > 1 ns: 14 %;
- > 2 ns: 2.8 %;
- > 3 ns: 0.8 %;
- > 5 ns: 7 × 10⁻⁴;
- > 10 ns: 0 of 5610.

**Why it helps.** F1 already has the BTL term but only as an "optional" add-on. Time and position of random PU hits are nearly
independent, so for candidates with BTL coverage:
- P_fake(F0 ∧ late BTL) = P(F0 candidate with ≥ 1 in-band BTL hit) × P(in-band BTL hit late).
- The second factor is measured **directly** from ~10³ BTL hits/event × 2 × 10⁴ events, down to ~10⁻⁷ per hit. That
  replaces 2-4 of the extrapolated decades with a measured factor.
- This is the FASER ABCD logic. Its independence is testable in the loose rungs: subdivide them by χ² and N_IT2 and compare the
  late fractions.

**Proposed change.**
- Pre-register two signal categories under the same WP rule:
  - **SR-T** = F0 with ≥ 1 in-band BTL hit and Δt in [t_min, 20 ns];
  - **SR-G** = the rest (geometry only, tighter rung).
- t_min is fixed from the PU-only late-hit spectrum alone, e.g. the delay at which the per-hit rate falls below a fixed value.
- Report both categories and their combination.

**Caveats to state:**
- **Out-of-time PU** is not simulated and populates the ±25 ns neighbours. The upper edge (20 ns) and the readout window are
  UNVERIFIED, so take a systematic from a toy OOT BTL hit overlay at ±25 ns.
- The **25 ns hit-time window** costs heavy quirks their BTL hits: at E1500 only 26-30 % of counting-set events have a BTL
  hit in 1-25 ns (C-4).
- Low-pT PU tracks have long helical paths, so their "delay" is partly geometric. This is fine because it is measured, not
  modelled.

**Cost:** 0 extra CPU (BTL hits are already in the geometry); ½-1 day.

### B-3. Add an IT dE/dx proxy as an F1 variable and a P2 velocity observable (VERIFIED signal availability)

**Evidence.**
- The plan has no dE/dx anywhere (risk 5 even says "any dE/dx handle approximate"), although it is the handle the literature
  relies on most:
  - Knapen et al. App. A and Sec.IV;
  - Li et al. pre-filter [1911.02223 Table I];
  - D0 [1008.3547].
- From `r1c_signal_handles.json`, the fraction of events whose median IT-hit βγ < 0.8 (well above MIP ionisation; ESTIMATE
  on the Bethe curve) is:

  | point | fraction |
  |---|---|
  | E200 | 7-9 % |
  | Ẽ500 | 24-25 % |
  | E500 | 36-41 % |
  | E1000 | 65-70 % |
  | E1500 | 82-92 % |

  So it is a strong handle exactly where the mass reach is decided (≥ 700 GeV) and nearly useless at 200 GeV.

**Proposed change.**
- Per candidate, the truncated-mean (or harmonic-2) dE/dx of the in-band IT hits, from:
  - quirk: `h_dE`, with Landau fluctuations added (HANDOVER §1 allows this);
  - PU: the Fatras SimHit `depositedEnergy`.
- Both need one common scale calibration from the muon-gun MIP peak, because Fatras deposits the loss of the whole surface
  material (x/X₀ of the decorated layer, not only the active Si).
- The threshold is set on PU candidates only (the WP rule). As an ABCD axis it is less independent than time (slow protons
  correlate with low pT), so use it in F1 and as a cross-check, not as the primary factorisation.
- The CMS IT ToT resolution (a 4-bit ToT, UNVERIFIED) should be represented by a coarse quantisation variation.

**Cost:** ½ day; 0 CPU.

### B-4. Restructure A2 row-major: simulate each PU event once, inject every Λ at the measurement level (≈ −80 CPU-h)

**Evidence.**
- §4.1 already fixes "the PU event of a physics row by hash(row) … reuses each PU event ≈ 20 times across Λ". Stage 3 uses
  the same rows at every Λ (HANDOVER §3).
- But each (row, Λ) job **re-simulates** the same PU (Pythia + Fatras + CKF ≈ 4.5 s of the 7 s per event, §6.1). The quirk
  hits are not transported by Fatras: they are injected Stage-3 hits, digitised by Gaussian smearing (U-5 b).

**Proposed change.** One job = one row:
1. generate PU, run Fatras and digitisation, and run CKF once;
2. loop over Λ: smear the quirk hits in numpy with the same digitisation config, append them to the PU measurements, apply
   analysis-level merging, run the finder.

Then:
- A2 costs ≈ 3.4 × 10³ unique rows × 4.5 s + 61 × 10³ × 2 s ≈ 4 + 34 ≈ **40 CPU-h instead of 120** (ESTIMATE, the plan's
  per-step costs). The unique-row count ≈ 61 344 / ~18 Λ per species-mass is an ESTIMATE.
- The Λ comparison becomes **exactly paired**: same PU hits, same smearing seed, same CKF output.

Validate on the A5 subset with the full chain (quirk hits through ACTS digitisation and CKF):
- (i) numpy and ACTS smearing agree (an extension of V4-1);
- (ii) the CKF-stealing fraction (V4-6) is still measured there.

Rows whose quirks could steal measurements (low Λ, "segment ≈ curved track") get a flag. If V4-6 exceeds 5 % anywhere, those
points revert to the full chain.
**Cost:** ½ day of code. Saves ≈ 80 CPU-h (≈ 12 h of wall time).

### B-5. Measure the correlated topologies explicitly (k = 1 sources), with cheap targeted samples

**Evidence.**
- [1911.02223 Sec.IV] finds the dominant Knapen-selection background is two charged particles from one vertex in a similar
  direction.
- The plan covers conversions and V0s with guns (C'). It covers PV-track pairs only through the 5 × 10³-event SM samples
  (reach ≈ 6 × 10⁻⁴, §4.2) plus a loose-to-tight factorisation, i.e. a second extrapolation of the same kind as §4.1.
- Two classes have no targeted sample:
  - loopers from PU vertices at Δz ≈ 0, whose z ≈ const circles are coplanar with the PV for small |p_z|;
  - pairs of low-pT tracks from the PV (UE) or from a PU vertex lying on the beam line, all of which sit in φ ≈ const planes
    when the tracks are near-collinear in φ.

**Proposed change.** Add to C':
- (a) a **PV pair gun**: two charged pions from the PV with the Pythia UE (pT, Δφ, Δη) spectrum, into the road, no PU and with
  PU, 10⁵ events;
- (b) a **looper gun**: π/e with pT 50-700 MeV, |η| < 0.3, from z_PV + Δz with Δz ~ U(−0.5, 0.5) mm, 10⁵ events.

Then B_corr = Σ_topology (rate per event in the road from Pythia, generator level, effectively unlimited statistics)
× P(pass | topology). This is the experimental "rate × fake probability" standard, and it turns the k = 1 term of B-1 into a
measured number.
**Cost:** ≈ 10-15 CPU-h (no PU, fast). Fund it from B-4.

### B-6. Deliverables for P2: add the velocity observables (the S-4 recipe) and a sensitivity model (VERIFIED feasibility)

**Evidence.**
- Synthesis S-4 (the degeneracy theorem): "hits, hit times and dE/dx measure only ℓ₀ and the velocities. m_Q comes from the
  MET recoil."
- Plan §11 item 4 delivers only sep_IT^det and t_est. Neither carries a velocity, so from Stage-4 output m_Q could come only
  from the *rate*, which is representation-dependent.
- `r1c_tof_mass.json` at truth level: M_est = |p_pair| / (βγ)_ToF, with β from the first quirk BTL hit (35 ps smear),
  reproduces the true pair mass with correlation **0.990-1.000** at E200-E1500 and Ẽ500 (n = 90-116 BTL-tagged events per
  point). The M/2m quantiles match truth to ≤ 0.03.
- Detector-level |p_pair| = MET·cosh η_axis adds the σ⊥ smear. ETL hits (kept at analysis level, §1.2) extend this to
  |η| > 1.5.

**Proposed change.** Add to §11 items 3-5 and to the per-event templates:
- MET (smeared), η_axis (n₃);
- BTL/ETL β_ToF of the first in-band timing hit;
- the B-3 dE/dx;
- M_est = MET·cosh η_axis / (βγ)_ToF and its lower edge vs m.

Add `results/sensitivity.json` and a pyhf counting workspace (methodology §7.1):
- expected 95 % CL exclusion and 5σ/3-event discovery contours in (m, Λ) with the full nuisance set, per category
  (SR-T/SR-G);
- overlaid on the FASER, D0 and Farina-Low limits already tabulated in synthesis §4.

Stage 5 needs this for the headline plot.
**Cost:** ½-1 day; < 1 CPU-h.

### B-7. The four "disjoint" roads share most IT hits (VERIFIED)

**Evidence.**
- §4.1 step 1 says the K = 4 roads at φ₀ + kπ/2 "share no hits (disjoint roads)". The road half-width is
  0.25 + asin(min(1, 50 mm/r)) (§2.2 step 1). It is 1.82 / 1.20 / 0.75 / 0.60 rad at TBPX L1-L4 (r = 30/61.5/104.5/146.5 mm),
  so roads separated by π/2 overlap in L1-L2.
- `r1c_pu_composition.json` (`road_overlap`):
  - 100 % of TBPX L1 hits fall in more than one road;
  - 51-54 % of TBPX L2 hits;
  - 0 % of L3 and L4 hits.
- L1-L2 hits enter N_IT2, so the 8 × 10⁴ trials are correlated. The "4 × 10⁻⁵ reach" is optimistic as an independent-trial
  count. The event-level bootstrap already in the plan gives correct errors, so this is not an A.

**Proposed change.**
- Correct the text.
- Quote the effective number of trials, from the bootstrap variance ratio.
- Report the per-event rate (the physical quantity, since data have one MET road per event) as the primary number, with the
  per-road rate as the diagnostic.

**Cost:** none.

### B-8. Order the gates so the risky items fail early and cheaply; strengthen the G3 pilot

**Evidence.** §11 orders G1 → G2 → G3 → production. That is right, but:
- A1 (no PU, 2 CPU-h) is the cheapest test of the finder against the Stage-3 edges (V4-3), and it is not in a gate;
- the pilot (G3) only "checks that the ladder spans measurable rates", while the closure (V4-7) is merely "designed" on it.

**Proposed order** (cumulative CPU-h in brackets, ESTIMATE):
1. U-2 panel (0).
2. G1 chain (≈ 2).
3. G2 finder with A-1 fixed, V4-5 brute force, and **all of A1 + V4-3** (≈ 6).
4. G3 pilot. B1 at 2000 events, B2 at 500 events with ρ = 2 **and** 500 with ρ = 1.5 (≈ 25). It must show:
   - (i) the B-1 k-decomposition closes from ρ = 2 to ρ = 1.5 on the loose rungs;
   - (ii) the B-2 time-position independence holds in the loose rungs;
   - (iii) whether ρ = 3 is needed.
5. B-5 topology guns (≈ 15).
6. A2 row-major (≈ 40), then A3-A5, C, the rest of B1/B2.

This hits the two real risks (finder CPU, extrapolation closure) for < 30 CPU-h, before ~90 % of the budget is committed.

---

### C notes

- **C-1. ρ values disagree between sections.** §4.1 says "superpositions of 2, 3 and 4 PU-200 events (PU 400-800)", §5 says
  ρ = 1.5, 2, 3, and §6.2 caps ρ at 3. State how ρ = 1.5 is built (PU 200 ⊕ PU 100?) and use one list.
- **C-2. The probe PU number is a lower bound.** The p5 PU-only "best N_L2 ≤ 6" refits only the top-30 seeds and has no
  duplicate merge (the `top3` entries in `p5_*.json` are often identical). My rerun with the top 60 seeds and a 2 mrad merge
  also gives ≤ 6 (≤ 5 in 18 of the 19 roads that had a candidate), but the plan should call it a lower bound.
- **C-3. Plane orientation.** z = const planes (|n_z| → 1) are where PU loopers from Δz ≈ 0 vertices live. Only 2-5 % of
  signal planes have |n_z| > 0.9 (`r1c_signal_handles.json`; median |n_z| 0.23-0.30). Store |n_z| as a diagnostic in B1.
  Cut only if B1 shows that population; that is a background-only decision under the WP rule.
- **C-4. Hit-time window vs heavy quirks.** At E1500 the median first BTL delay is 27 ns, and only 26-30 % of counting-set
  events have a BTL hit in 1-25 ns (vs 54-57 % with any BTL hit). Report ε(Δt_acc) as a curve (25, 12.5 and e.g. 50 ns) at
  E1000/1500. State that the OT/BTL readout-window assumptions are UNVERIFIED.
- **C-5. PV placement in the PU-only samples.** Specify that the B1/B2 "PV" is drawn from the luminous region independently
  of the PU vertices (as p5 effectively did with the Stage-3 vertex), and record the distance to the nearest PU vertex. The
  hard-scatter vertex's own UE belongs to C/B-5.
- **C-6. Stage-5 figure list.** Make it explicit in §11:
  - event displays (signal in PU 200 vs the best PU fake);
  - ε(m, Λ) maps by factor;
  - the fake-rate extrapolation with its closure (per k);
  - detector-level vs truth edges;
  - the sep_IT^det calibration;
  - the M_est spectra;
  - exclusion/discovery contours vs FASER/D0/Farina-Low.

  Each comes with its `results/*.json` source and the "Private work (simulation)" label.
- **C-7. Selection sculpting of P2.** The F1 crossing/separation pattern is correlated with sep_IT (the Λ⁻² handle).
  This is acceptable, since the templates are post-selection, but check in A3 that the coverage holds with F1 vs F0. Never use
  sep_IT itself in the selection.

---

## 3. Scope and cost (question 3)

| Block | Plan CPU-h | Proposed | Comment |
|---|---|---|---|
| A1 | 2 | 2 (moved into G2) | cheapest validation of the finder |
| A2 | 120 | ≈ 40 | B-4 row-major |
| A3 / A4 / A5 | 18 / 23 / 30 | same | A5 also hosts the full-chain checks for B-4 |
| B1 | 72 | 72 | keep: the direct ladder is the anchor; B-2 makes it more valuable |
| B2 | 90 | 50-90 | ρ = 3 (≈ 37) only if G3 shows the k-decomposition needs it |
| C + C' | 55 | ≈ 70 | + B-5 guns (≈ 15) |
| validation | 40 | 40 | |
| **Total** | **≈ 450** | **≈ 330-370** | the freed 80-120 CPU-h can go to B1 statistics (direct reach) or more A3 toys |

Physics per CPU-h, from highest to lowest:
1. A-1 / B-1 / B-2 / B-3 (≈ 0 CPU, large gain in background robustness);
2. B-5 (cheap; it measures the k = 1 term);
3. B1;
4. A2;
5. B2 at ρ = 3 (the most expensive per unit of information).

---

## 4. Deliverables (question 4)

- **Stage 5:** sufficient once C-6 lists the figures and B-6 adds the sensitivity JSON and workspace. Labels and the JSON
  single-source rule are already in place.
- **P2 m_Q:** **not sufficient as written.** It needs the B-6 per-event velocity observables (β_ToF, dE/dx) with MET and
  η_axis, the S-4 recipe (VERIFIED feasible at truth level here).
- **P2 Λ:** sufficient (sep_IT^det calibrated vs truth).

## 5. Missing validations and easy wins (question 5)

Covered above:
- the A-1 signal-efficiency check on A1;
- the B-1 k-closure;
- the B-2 independence test;
- the B-3 MIP calibration of the deposited energy;
- B-4 numpy-vs-ACTS smearing;
- B-7 effective trials;
- C-4 ε(Δt_acc).

One more easy win: a **truth-labelled B1 output** (k, particles, generation, |n_z|). It is free, and it lets every later
reviewer see what the fakes are made of.

---

**Verdict: ITERATE.** One Category A: A-1, the N_OT2 definition counts both sensors of one stacked crossing. The fix takes
minutes and must land before `WP_RULE.md` is frozen. The 8 B and 7 C items are advisory; adopting B-1, B-2, B-4 and B-6 is
strongly recommended. Counts: **A 1 / B 8 / C 7.**
