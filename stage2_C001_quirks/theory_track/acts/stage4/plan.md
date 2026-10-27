# Stage 4 plan: Stage-3 quirk hits through an ACTS CMS Phase-2-like tracker with PU 200 (C001 theory track)

E9 (executor), 2026-10-13. **Plan only. No production was started.** The user reviews this plan first.

**Revision R1 (fixer, 2026-10-13)** after `review/CRITICAL_REVIEW_S4PLAN_R1.md` and `review/CONSTRUCTIVE_REVIEW_S4PLAN_R1.md`.
The item-by-item record is `review/FIX_S4PLAN_R1.md`; new probes are in `probes/f1r_*.py` and their outputs in
`data/acts_stage4/fix_r1/`. Main changes:
- the Δw cut is removed;
- layers count crossings;
- W_c = 75 mm comes from a physics rule, with a 30 µm thickness tolerance;
- the PU density is normalised to the TDR (Fatras is low by ×2.3-7);
- the density ladder uses exact interaction-count thinning, with closure tests and a failure path;
- the WP rule is defined in log space and frozen at G2;
- F1 is revised and SR-T/SR-G timing categories are added;
- A2-A4 run row-major;
- the gates are reordered.

R1 marked D4-10 → (a′), new D4-13 and D4-14, and the TDR-normalised PU top-up (D4-15) as PROPOSED. **All four were
approved by the user on 2026-10-13 as recommended** (LOG.md); they are now plan baseline (§10).

**Revision R2 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R2.md` (0 A, 5 B, 11 C). Item record:
`review/FIX_S4PLAN_R2.md`; new probes `probes/f2r_*.py`, outputs `data/acts_stage4/fix_r2/`. Main changes:
- a pre-declared **ribbon-width rung family** (robust core width w_core) and a **core-hit χ²** enter the F0 ladder before
  the freeze (§2.2, §2.5). "F0 alone does not separate" is withdrawn: the layer count and χ² alone do not reach the target,
  but the core width separates PU from signal strongly at Λ ≳ 2 keV (review R2 evidence, §2.4);
- **SR-T and SR-G** each walk their own 1-D ladder with a pre-registered **budget split** (B₈₄ ≤ 0.15 each in R2;
  **0.11 each since R3**, §2.5);
- a per-rung-family **extrapolation method table** (per-subset recomputation vs factorisation, stored information, cost;
  §4.1);
- a plain **feasibility statement and a pre-defined fallback deliverable** (§2.6);
- **cost as a function of the finder time per trial** at the normalised density, with a finder-speed gate at ρ = 1 and a
  ρ = 2 timing gate before the G3 pilot (§6.2, §11). A profiling probe shows where the 48 s/trial goes (§2.4);
- the unexplained ×1.6-1.8 thinning-closure residual is stated as unexplained, and the closure gate decides on it (§4.1).

**Revision R3 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R3.md` (0 A, 4 B, 9 C) and the user decisions of
2026-10-13 (D4-10 (a′), D4-13, D4-14, D4-15 approved; scope chosen by the user after G2a; **every production run ≲ 1 day
of wall time**, several runs allowed, each approved by the user; development/gate runs not capped but reported; resources:
the Mac plus, optionally, a Google Cloud free-trial VM). Item record: `review/FIX_S4PLAN_R3.md`; arithmetic
`probes/f3r_campaigns.py` → `data/acts_stage4/fix_r3/f3r_campaigns.json`, `f3r_split.json`. Main changes:
- production is split into **pre-defined campaigns C1-C4 (+ optional C5 = ρ = 3)**, each sized against the one-day cap on
  the Mac alone and on Mac + cloud, as a function of t₁, t₂ (§6.2). C1 is the self-contained minimal scope. G2a always
  presents the scope choice to the user; G2b has one criterion; ρ = 3 has its own timing gate G2c (§11);
- the **fallback** gets a pre-declared, hypothesis-admissible primary rung per (m, Λ) and a ban on per-point best-of; what
  it can and cannot claim is stated (§2.6);
- the **budget split** is 0.11 + 0.11, so the combined B₈₄ ≤ 0.3 holds by construction at the planning σ_ln, and the pair
  continuation has deterministic branches for every case (§2.5 item 5);
- **p(χ²_core) > 10⁻³ moves from the counting rungs to the head of the χ²_core family**, so every rung family is
  extrapolated by a method that can compute it (§2.5, §4.1);
- an optional **cloud execution** subsection (§6.5); no account or resource was created. (Withdrawn in R4: the cloud
  was dropped by the user.)

**Revision R4 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R4.md` (0 A, 1 B, 6 C) and the user decisions of
2026-10-13 (D4-17 (i) approved; **the cloud is dropped, Mac only**; **deadline: Stage 4 production, analysis and review,
Stage 5 figures and a short Stage 6 feasibility note all finished by Saturday 2026-10-17 night**; the per-run ≲ 1-day cap
still applies; Stage-5 label approved). Item record: `review/FIX_S4PLAN_R4.md`; arithmetic `probes/f4r_deadline.py` →
`data/acts_stage4/fix_r4/f4r_deadline.json`; frozen admissibility inputs `probes/f4r_admissibility.py` →
`fix_r4/f4r_admissibility.json`. Main changes:
- **C′ (topology guns and toys) is production** and runs inside C1: a no-PU part (≈ 12 CPU-h) and a with-PU part of
  8 topologies × 500 events (4 000 × (4.7 + t₁) s). C1 now fits one Mac day up to t₁ ≈ 7.0 s (§4.2, §5, §6.2);
- §11 has a **deadline schedule** (Tue 13 → Sat 17) and a **campaign-vs-t₁ decision table**; the old timeline is
  replaced;
- the cloud material (§6.5, D4-8 (b), the Mac + cloud columns, risk 10) is withdrawn;
- §2.6: βγ_IT(m) is recomputed for all 17 species-masses by a frozen script; Λ_R(m) is the smoothed `edge_fits_in_m`
  value; corrected βγ ranges; Ẽ500 has no dE/dx level; the dE/dx unit conversion and the mixed-admissibility branch are
  stated.

**Revision R5 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R5.md` (0 A, 1 B, 3 C). Item record:
`review/FIX_S4PLAN_R5.md`; arithmetic `data/acts_stage4/fix_r5/f5r_cprime_counts.py` → `f5r_cprime_counts.json`.
Main changes:
- the NI/DIF with-PU samples overlay only C′₀ toy events that pass a PU-independent preselection, weighted by the
  preselection fraction (§4.2);
- thinning is no longer claimed as a depth mechanism for the fixed-density samples C and C′_PU: depth comes from rung
  factorisation (§4.2);
- a zero- and low-count rule is pre-declared for every B factor (§2.5 item 4a);
- the gun/toy attribution is tightened (§4.2);
- §2.6 wording fixes and §11 schedule nits.

The C′ cost, the campaigns and the schedule are unchanged.

**Revision R6 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R6.md` (0 A, 1 B, 4 C). Item record:
`review/FIX_S4PLAN_R6.md`; arithmetic `data/acts_stage4/fix_r6/f6r_numbers.py` → `f6r_numbers.json`. Main changes (text
and design only):
- the NI/DIF preselection and the attribution use one n-independent per-hit tolerance σ̂_h (≥ any candidate's σ_tot;
  σ_tot has no δn term since fix R8), the same stored PV draw and the stored C′₀ toy hits (inserted into the PU event, not
  re-simulated), so f_pre is exact; new
  zero-cost gate V4-10 (attributed candidates in non-preselected C′₀ events = 0), frozen with `WP_RULE.md` (§4.2, §8);
- NI: the 22 mm f_pre is ≈ 0.07-0.5 (line + near-vertex hit), the §4.2 two-prong estimate is not an upper bound at any
  r_NI, and the NI gap is ≈ 8-9 decades (ESTIMATE; §2.6, §4.2, §12 risk 3b);
- zero-count rule: the zero factor with the largest M_j carries the bound; c excludes zero factors (§2.5 item 4a);
- B_NI shows the PV-line factor ≈ 0.22 explicitly (the NI toy parent starts at the PV).

The C′ cost, the campaigns and the schedule are unchanged.

**Revision R7 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R7.md` (0 A, 1 B, 4 C). Item record:
`review/FIX_S4PLAN_R7.md`. Text only, nothing computed. Main changes:
- δn in σ_tot was set to the current normal's uncertainty capped at δn_max = 2 mrad (**superseded in fix R8**: σ_tot
  has δn = 0), so σ̂_h ≥ σ_tot,h for **every** candidate and the attribution is a superset of R5's for every candidate;
  the δn > δn_max diagnostic is removed; the σ_tot definition is frozen with σ̂_h (§2.5 item 9);
- the preselection and the V4-10 hash use all stored toy measurements before CKF removal and before analysis-level
  merging; the attribution tests toy-linked hits at their stored C′₀ positions (§4.2, §8);
- the PV-line factor 0.22 is labelled a conservative upper value (per-event PU-vertex coincidence, R1 B-4 (a)), not a
  per-NI fraction; the kink reach is split into NI kinks and DIF; pure-PU candidates attributed to toys are noted as
  conservative double counting.

The C′ cost, the campaigns and the schedule are unchanged.

**Revision R8 (fixer, 2026-10-13)** after `review/REVIEW_S4PLAN_R8.md` (0 A, 1 B, 2 C). Item record:
`review/FIX_S4PLAN_R8.md`. Text only, nothing computed. Main changes:
- **σ_tot² = σ_n² + t_tol², with no normal-uncertainty term (δn = 0)**, is the frozen finder definition (§2.2 step 3,
  §2.5 item 9): it is the prototype's, on which every probe, the margin study, T_seed, the §2.1 μ_c, the §4.1 storage and
  t₁ rest. Fix R7's min(δn_fit, 2 mrad), which widens the IT/PS bands ×1.6-15 after refit and more at the seed stage
  (review R8), is only a pre-declared A5/B1 variation. δn_max = 2 mrad stays **only** in σ̂_h (preselection and
  attribution); σ_tot,h ≤ σ̂_h now holds trivially, and f_pre stays exact for any δn (attribution ⇒ preselection);
- "inserted" (not "merged") for the toy hits put into the PU event; a U-5 b merged hit is tested in the attribution at
  each of its toy-linked stored C′₀ positions (§4.2).

The C′ cost, the campaigns and the schedule are unchanged.

The blind margin study (§2.4) shows that F0's layer count and χ² alone do not reach the required rejection at the
TDR-normalised density. Whether a background-free working point exists is a G3 question, and it may exist only for part of
the (m, Λ) plane (§2.6).

Scope: CMS Phase-2 phenomenology from public information only; √s = 14 TeV, PU 200, 3 ab⁻¹. Signal: colour-neutral EW
quirks E (1,1)₋₁ and the scalar Ẽ, Stage-3 truth hits (`sim/stage3/HANDOVER_STAGE4.md`). Final plots come in Stage 5 with
the label approved on 2026-10-13: left "Private work (simulation)", right "√s = 14 TeV, PU 200, 3 ab⁻¹", no CMS name or
logo, and "truth level" on truth-level figures.

Tags: **VERIFIED** = measured in this session by a probe (file named); **ESTIMATE** = my calculation, model or projection;
**UNVERIFIED** = transcribed or recalled, not checked against the primary source.

Probe code: `acts/stage4/probes/` (s4geo.py, s4pu.py, p1-p6; fix R1: f1r_pu_gen.py, f1r_truth_window.py,
f1r_density_bench.py, f1r_finder.py, f1r_analyse.py; fix R2: f2r_profile.py, f2r_analyse.py, f2r_cost.py; fix R3:
f3r_campaigns.py, arithmetic only; fix R4: f4r_deadline.py, arithmetic only, and f4r_admissibility.py, Stage-3 truth
only; fix R5: `data/acts_stage4/fix_r5/f5r_cprime_counts.py`, arithmetic only). Probe outputs: `data/acts_stage4/p0-p6/`, `data/acts_stage4/fix_r1/`, `data/acts_stage4/fix_r2/`,
`data/acts_stage4/fix_r3/`, `data/acts_stage4/fix_r4/`; review scratch `data/acts_stage4/review_r2/`, `review_r3/`, `review_r4/`.
(The `f2r_profile.py` docstring still calls the trimmed width "the plan's new w_core"; that is stale: the trimmed width is
the rejected definition, §2.2 item 5. The probe file is left unchanged as the audit record.)
Session log: `acts/stage4/E9_session_log.md`. Nothing was installed and the acts pixi env was not modified.

---

## 0. Summary

**What the probes established (VERIFIED, small samples):**

| Item | Result | Probe / output |
|---|---|---|
| Geometry contract U-4 (a) | An ACTS Gen-3 tracking geometry built from the 83 physical Stage-3 surfaces (T3V skipped), as sensitive JSON detector elements with the Stage-3 x/X₀ attached through the JSON material decorator. A muon gun gives 17/17 hits per central muon; every hit lies on its surface to < 0.1 µm. ETL cannot be Z-stacked with the r = 0 beam region and is left out of the ACTS geometry (§1.2) | `s4geo.py`, `p1_fatras_pu.py` → `data/acts_stage4/p1/p1_summary.json` |
| Two Fatras pitfalls found and fixed | (i) the default `pMin` is 0.5 GeV, which drops every looper. It is set to 30 MeV. (ii) The JSON molar density must be in mol/mm³ (ACTS native units). Entered in mol/cm³ it gives 1000× the energy loss, and 30 % of muons fail with "max steps" | same |
| PU 200 on the Stage-3 surfaces | Pythia8 CP5 minimum bias, charged + photons with pT > 50 MeV, Fatras with photon conversions: **1.33 × 10⁵ hits/event**. TBPX L1 has 15.4 hits/cm² at \|z\| < 2 cm (8.9 averaged over the layer); TBPX L4 0.89; TBPS L1 0.29; TB2S L1 0.023 cm⁻². Fatras + digitisation ≈ 1.0-1.3 s/event (1 thread) | `p1`, `data/acts_stage4/p1/density_table.json` |
| **V4-2 density benchmark (fix R1)** | Against CMS-TDR-014 Fig. 6.3 occupancies (tt̄ + PU 200, incl. out-of-time PU), converted to clusters/cm² with the TDR channel sizes and OT cluster sizes. The **Fatras in-time density is low by ×2.3-3.7 (IT; IT cluster size not in the TDR, ESTIMATE), ×2.5-4.3 (PS), ×4.0-7.3 (2S)**. The baseline PU is now topped up to the TDR (§1.4) | `f1r_density_bench.py` → `data/acts_stage4/fix_r1/f1r_density_bench.json` |
| Signal injection (HANDOVER §4) | One ACTS event per physics event; T3V skipped; p4_after from `h_dE`; `doMerge = False`. Measurement count = SimHit count **exactly** at 1, 10 and 30 keV (20 events each) and with the PU overlay (8 events, ≈ 1.4 × 10⁵ hits each); every quirk SimHit is recovered through the measurement→SimHit map | `p2_inject_digi.py` → `data/acts_stage4/p2/*.json` |
| CKF cost | One ACTS surface per full cylinder makes the CKF cost **23-60 s/event**, because every measurement on a whole layer is scanned. Splitting each surface into 32 φ-sectors (same geometric surface) brings it to **1.6-3.4 s/event**, with 0.2-0.5 s for seeding | `p3_ckf.py` → `data/acts_stage4/p3/` |
| CKF on quirk hits | With pT > 0.9 GeV seeds, about 18 % of the measurements are on tracks (n32 runs). **0 of 208** quirk measurements were taken by CKF tracks (6 signal events, E1000 at 0.6 and 1 keV, on 3 independent PU events) | `p3` |
| Finder prototype (PS-pair seeds) | About 9 × 10⁴ seeds/event. All of them pass a loose 6-layer score and the best candidate is a PU fake. **Rejected as a design** | `p4_finder_proto.py` |
| Finder prototype R0 (IT triplets + PV + MET road) | 6-10 × 10⁴ triplets/event in a ±0.25 rad road, 5-10 s/event (numba, 1 thread, unoptimised). **Re-tagged in fix R1:** the "signal 10/10 vs PU N_L2 ≤ 6" came from truth-selected signal seeds, a top-30-only PU search, and a hit count that one particle satisfies on a stacked module. A blind full refit gives PU N_L2 = 9 (critical B-1) | `p5_finder_triplet.py` → `data/acts_stage4/p4/` |
| **Blind F0 prototype (fix R1)** | Per-crossing counting, W_c = 75 mm, t_tol = 30 µm, the same blind search for signal and PU (central, barrel). **Fatras PU:** best PU N_L2 = 7-9, never 10 in 224 trials (< 1.3 %/trial at 95 % CL), against 77 % [72, 82] of signal events at ≥ 1 keV reaching 10. With χ²/ndf < 2 at N_L2 ≥ 9: PU 0.9 % vs signal 85 %. **TDR-normalised OT density:** PU reaches 10/10 in 88 % of trials. At (10, χ²/ndf < 2) PU passes 12.5 % [6.6, 21] of trials and signal 36 % [21, 53] (14 signal events, 8 of them at 1 keV; the ratio's 68 % range is ≈ ×1-8). So **the layer count and χ² alone do not reach the target at the realistic density** (§2.4) | `f1r_finder.py`, `f1r_analyse.py` → `data/acts_stage4/fix_r1/f1r_margin.json`, `f1r_summary.json` |
| **Robust core width (review R2; fix R2, PU only)** | The stored robust core width (1.4826 × MAD of u·n₂ over the IT + PS in-band hits) separates. Review R2 measured PU 0/224 trials (Fatras, N_L2 ≥ 9, < 20 mm) and 0/32 (TDR-OT, N_L2 ≥ 9, < 10 mm), against signal ≥ 2 keV 30/31 and 4/6 (probe rows, excluded from templates). Fix R2 (PU only): the per-trial minimum over PU candidates at N_L2 ≥ 9 is 14.6-32 mm (TDR-OT, 5 trials) and 12.2-14.2 mm (full IT + OT normalised density, 3 trials, 18 903 candidates, none < 9.4 mm). **An iteratively trimmed width collapses on PU (minimum 0.5-3.4 mm at N_L2 ≥ 8) and is rejected.** This became the rung family of §2.5 | `review_r2/r2_corewidth.json`; `f2r_profile.py` → `fix_r2/f2r_profile_summary.json` |
| **Interaction-count thinning pilot (fix R1; review R2 re-check)** | The ρ = 2 → ρ = 1 prediction follows the rung dependence over 2.5 decades of thinning and is conservative by ×2.1-2.9. De-duplicating per distinct hit set removes ≈ ×1.3-1.4 of that (review R2, 2 ρ = 2 trials). **An over-prediction of ≈ ×1.6-1.8 remains unexplained**, and the closure gate decides on it (§4.1). PU fakes need k ≈ 10-22 interactions | `f1r_summary.json` → `closure_rho2_to_rho1_t0`; `review_r2/r2_dupcheck_summary.json` |
| **Finder profile (fix R2, ρ = 1 only)** | At the TDR-OT density, **72 % of the prototype's time per trial is a Python duplicate-merge loop** that scales as O(N_cand²): 21 of 29 s (median of 5 trials). The same merge vectorised takes 0.16 s, which leaves 5.7-11.8 s/trial (seeding 3.8 s, numba refits 1.3 s, numpy refits 3.1 s). **At the adopted full IT + OT normalised density (3 trials, never timed before): ≈ 3 400-6 000 s/trial as coded (97 % in that loop), and 159-228 s (median 211 s, per-trial sums of the stage times) with it vectorised** (seeding 95 s, numpy refits 52 s, merge 33 s, numba refits 30 s; 2 × 10⁵ refitted seeds, ≈ 1.1 × 10⁵ candidates after the 2-mrad merge — "distinct" in the probe means 2-mrad-distinct normals, not the ≥ 50 % hit-set convention of §4.1). Stored counts attribute ≈ 46 % of the fix-R1 ρ = 2 time to the same loop and ≈ 26 % to per-candidate thinning Monte Carlo (12 ms each) | `f2r_profile.py`, `f2r_cost.py` → `fix_r2/f2r_profile_summary.json`, `f2r_cost.json` |
| Memory | Peak RSS of the full ACTS chain is 670 MB per worker | `p3` with `/usr/bin/time -l` |
| PC | The `pyacts` 48.0.0 wheels exist only for macOS arm64 and manylinux_2_34 x86_64; conda-forge `acts-core` has no win-64 build. **The PC can run the chain only under WSL2** | PyPI / anaconda.org metadata |

**Plan in one paragraph (R1, updated in R2).**
- **Simulation.** The Stage-3 hits are injected into Fatras PU-200 events simulated on the same surfaces (φ-sectored). The PU
  is topped up per layer to the TDR occupancy. Both are digitised by smearing with CMS Phase-2-like resolutions and
  `doMerge = False`, and two-hit merging is applied at analysis level (U-5 b). A standard CKF (pT > 0.9 GeV) removes the hits
  of reconstructed helical tracks. Signal rows run row-major: PU is simulated once per row, then all Λ follow in numpy.
- **Finder.** A dedicated finder then searches for a plane through the primary vertex:
  - **F0 (baseline):** IT-triplet seeds in the MET road; collection within ±3σ_tot (resolution ⊕ 30 µm thickness tolerance)
    and a 75 mm window derived from ℓ_max ≤ R_IT; a PV-constrained weighted refit of every seed above T_seed; layer
    counting per crossing; a core-hit χ²; and a ribbon-width rung family on the robust core width (fix R2). There is no
    fixed Δw cut: the width thresholds are rungs of the background-ordered ladder.
  - **F1 (one improved variant):** F0 plus quirk-hypothesis variables: a helix test with PV and free origins, opening
    linearity, dE/dx. Two categories, SR-T (late BTL hit) and SR-G.
- **Working point.** It is fixed by a pre-registered, log-space rule that uses background samples only. Each category
  walks its own ordered 1-D ladder under a pre-registered budget split. The rule is frozen before any signal efficiency is
  computed. Where the working rung does not exist or is not admissible for a hypothesis (it cuts away that hypothesis's
  signal by construction), a pre-defined fallback with a pre-declared rung per (m, Λ) and non-zero background applies
  (§2.6). It is expected to give ε, B and observables, but essentially no exclusion, at Λ ≲ 1 keV and at E200.
- **PU-only fake rate.** It cannot be measured directly at the required ≲ 3 × 10⁻⁹ per event. It is extrapolated by exact
  interaction-count thinning from superpositions of 2 normalised PU-200 events (ρ = 3 only as the optional, separately
  gated campaign C5) and by rung factorisation, with pre-registered closure tests, a lever-arm minimum and a failure path.
- **SM backgrounds.** They come from Pythia8 + Fatras samples where the physics is in Fatras (W/Z+jets, tt̄, conversions,
  V0s, loopers), from k = 1 topology guns, and from dedicated toys or arguments where it is not (nuclear interactions,
  decays in flight, cosmics, halo).

**Compute (ESTIMATE; rewritten in fix R3 for the user's one-day cap; Mac only and deadline schedule since fix R4).** The
cost depends on the finder time per trial at the normalised density, t₁ (ρ = 1), and t₂ (ρ = 2; t₂ = 8 t₁ is assumed
until G2b measures it). **Every production run must finish in ≲ 1 day of wall time**: ≈ 168 CPU-h on the Mac (7 workers;
the user quotes 170-200). The Mac is the only machine (user decision 2026-10-13;
§6.5). Production is split into **pre-defined campaigns**, each launched only with the user's approval (§6.2,
`fix_r4/f4r_deadline.json`):

| campaign | content | CPU-h at t₁ = 2 / 3 / 5 / 8 s | largest t₁ for ≲ 1 Mac day |
|---|---|---|---|
| **C1 core (self-contained; the minimal option)** | A1; A2 on 5 species-masses × 8 Λ; A5 5 points; B1 5 000; B2 1 000 at ρ = 2; C 3 × 2 000; **C′ guns and toys (no PU, + 8 topologies × 500 with PU)** | 91 / 107 / 137 / 183 | **7.0 s** |
| C2 backgrounds I | B1 → 12 000; B2 → 3 000; C → 5 × 5 000 | 88 / 110 / 154 / 220 | 5.6 s |
| C3 backgrounds II | B1 → 2 × 10⁴; B2 → 5 000 | 56 / 74 / 110 / 163 | 8.2 s |
| C4 grid + systematics | rest of A2 (all 307 points); A3; A4; A5 → 20 points + PU 140 | 80 / 101 / 144 / 209 | 6.1 s |
| (C4′ = C4 without A3, A4; a deadline variant) | rest of A2; A5 → 20 points + PU 140 | 63 / 79 / 110 / 157 | 8.7 s |
| C5 (optional, gate G2c) | ρ = 3, 2 000 events | 38 / 53 / 83 / 128 | 10.6 s |
| **C1-C4 = the recommended scope (D4-1 (a))** | | 315 / 392 / 545 / 774 | 4 one-day runs up to t₁ ≈ 5.6 s |

**Measured** at the adopted density (fix R2, 3 trials): 211 s/trial with the duplicate merge vectorised and ≈ 5 500 s as
coded. The optimisation routes of §6.2 reach ≈ 5-20 s by ESTIMATE; the finder speed-up now running targets t₁ ≈ 3 s.

**Deadline (fix R4; §11 schedule).** Everything must be finished by Saturday 2026-10-17 night. The schedule leaves a
production window of ≈ 47 h of Mac wall time (Wed 14 10:00 → Fri 16 12:00, ≈ 329 CPU-h, no rerun margin). Which campaigns
fit is fixed now as a function of the measured t₁ (§11 decision table):
- t₁ ≈ 2 s: all of C1-C4, in the order C1 → C2 → C4′ → C3 → A4 → A3 (45 h, tight);
- t₁ ≈ 3 s: C1 + C2 + C4′ (42 h);
- t₁ ≈ 5 s: C1 + C2 (42 h);
- t₁ > 5 s: C1 only (plus the B1/B2 part of C2 up to 7 s), then C1 as two sub-runs, then a reduced C1.

Deferral order: C5, A3, A4, C3.

**What the minimal option C1 gives up:**
- *PU-extrapolation reach.* The ρ = 2 thinning reach is ≈ 5 × 10⁻¹⁰ per trial, above the ≈ 3 × 10⁻¹⁰ per-category
  requirement, so the deepest rungs rest on rung factorisation. C1 + C2 reach 1.6 × 10⁻¹⁰, and C1-C3 reach 10⁻¹⁰.
- *Coverage.* Edges in ln m come from 5 masses (not 14); there are no A3 toys, no A4 material variation, and three of
  the five SM samples.

**Gates:**
- **G2a** measures t₁ and **always presents the scope choice to the user**, with this table and the §11 decision table at
  the measured t₁. No G2a branch launches production.
- **G2b** checks that the campaigns the user chose still fit at the measured t₂ (each ≲ 1 day and the set inside the
  production window).
- **G2c** times ρ = 3 before the optional C5. Under the deadline C5 is deferred in every case.

Development and gate runs (G1-G3) are not capped but are reported (§11); C′ is production since fix R4. Disk ≈ 32 GB for
the full scope (§6.3). **No install is needed on the Mac.**

---

## 1. Chain and code

### 1.1 Data flow

```
Stage-3 npz (p2/BM, mv)            Pythia8 CP5 minimum bias (fresh, seeded)    Pythia8 SM hard scatter (W/Z+j, tt̄, γ+j)
        |                                         |                                       |
        |  inject (one ACTS event / physics event; T3V skipped; h_dE; barcode vp = 4000)  |
        v                                         v                                       v
  ACTS env (acts/pixi.toml, unchanged): s4geo geometry (Stage-3 surfaces, 32 φ-sectors) -> Fatras PU-200 (+ hard scatter)
        -> SimHits (quirk + PU) -> DigitizationAlgorithm (smearing, doMerge = False) -> GridTriplet seeds + CKF (pT > 0.9 GeV)
        -> per-event compact output: measurements (global position, local σ, surface, time, CKF-used flag, truth link)
  TT env (numba): analysis-level merging (U-5 b) + hit-time window -> PV and MET model -> finder F0/F1 -> candidates
        -> selection, efficiencies, edges, P2 observables, background extrapolation -> results/*.json -> Stage 5
```

### 1.2 Geometry: the Stage-3 surfaces (user decision U-4 (a))

- The builder is `s4geo.py` (probe). Every physical Stage-3 surface (kinds IT, PS, 2S, BTL; 83 surfaces) becomes a sensitive ACTS
  surface at the D111 nominal position read from `sim/stage3/code/surfaces_s3.json`.
  - Barrel: cylinders. Endcaps: discs (TFPX, TEPX, TEDD PS/2S parts).
  - Volumes: an R-container [beam region (r < 20 mm) | beam pipe | tracker | BTL].
  - Tracker: a Z-container [fwd− | central | fwd+]. Central = [IT (TFPX−, TBPX, TFPX+) | IT service cylinder | OT barrel].
  - fwd = [(TFPX D8 | TEDD D1-2), (TEPX D1-4 | TEDD D3-5)].
- **φ-sectors.** Every cylinder and disc is split into N_φ = 32 azimuthal sectors of the **same geometric surface**, so the
  hit positions and the Stage-3 contract are unchanged. A Stage-3 hit goes to sector ⌊(φ + π)/(2π/32)⌋. This is needed only for
  CKF speed (§0). It also makes the digitisation "modules" 32× smaller, which is irrelevant with `doMerge = False`.
  - Closure with sectors: 120/120 muons give the full 17-hit pattern (VERIFIED, p3 gun check).
- **ETL** (|z| = 2920 mm, timing proxy) is not in the ACTS geometry, because Gen-3 Z-stacking with the r = 0 beam region failed
  ("Invalid inner cylinder configuration"). Quirk ETL hits stay available at analysis level from the Stage-3 file, and PU ETL
  hits are not needed: no finder variable uses the ETL. Fix later only if F1 needs endcap timing: add the ETL as a disc layer inside
  an outer R-shell (ESTIMATE ½ day).
- **Material** (UNVERIFIED baseline, user D4, ×0.5/×2 systematic): the Stage-3 kernel numbers:
  - TBPX 1.2 %, PS 2.5 %, 2S 1.8 % per layer, the disc values from `surfaces_s3.json`;
  - Be beam pipe 0.23 % at r = 22 mm; IT service cylinder 1.0 % at r = 190 mm.

  They sit as homogeneous surface material on the sensors (a stacked layer's x/X₀ is split over its two sensors).
  - Difference from Stage 3: the kernel spreads each layer over a 1-2 cm radial slab, while Fatras uses thin scatterers. The
    effect on PU tracks is negligible for this purpose (the same x/X₀ and the same Highland angle). It is irrelevant for the
    quirks, whose hits come from Stage 3.

### 1.3 Signal injection (HANDOVER §1, §4; implemented and VERIFIED in p2)

- Input: campaign `p2`, configuration `BM`, status == 1 (drop status 4 and carry ≤ 1.5 % per point as an efficiency loss,
  HANDOVER §0), all |η_pair| < 4 events.
  - The counting set is `in_eta25`: 61 344 template and 55 921 toy events (VERIFIED from `data/sim_stage3/summary/events_p2.npz`).
- **One ACTS event per physics event**: the sequencer event number maps to the physics event. The barcode is vertexPrimary =
  4000 (PU vertices are 1…200) and particle = 1 + `h_quirk`.
- **Skip kind T3V** (virtual layers). ETL hits are kept outside ACTS (§1.2).
- **Energy deposit:** E_after = E − `h_dE`, |p| rescaled on shell with the quirk mass, so that `depositedEnergy()` = `h_dE`.
- **Units:** mm, ns, GeV × `acts.UnitConstants`. Global hit positions stay as given; only the sector is chosen.
- **Vertex:** the Stage-3 smeared luminous-region vertex (HANDOVER §3). The PU vertices come from the same luminous region
  (σ_z 45 mm, σ_t 190 ps [CMS-TDR-020 PDF p.2-3, VERIFIED in E5]; σ_xy 5 µm ESTIMATE [CERN-2020-010 Tab. 2-1]).

### 1.4 PU-200 overlay on the same surfaces

- **Generator:** Pythia8 8.312 (in the acts env), 14 TeV, `SoftQCD:inelastic`, CMS CP5 (copy of `sim/cards/pythia8_tune_CP5.dat`).
  σ_inel = 78.9 mb (VERIFIED, Pythia).
  - **Decays:** Pythia decays K⁰_S, Λ and hyperons (`tau0Max = 1000 mm`), so their daughters start at the true displaced vertex.
    π±, K±, μ and K⁰_L are kept stable, because Fatras does no decays (§4.2).
- **Pile-up number:** Poisson with mean 200 per event (the probes used a fixed 200; production uses Poisson). Out-of-time pile-up
  (12 previous and 3 following crossings in the TDR simulation [CMS-TDR-014 §6.2.1, PDF p.100, text copy l.4286-4288]) and
  hadronic secondaries are **not simulated** by Fatras.
- **Density normalisation to the TDR (fix R1, critical B-7; V4-2).** The in-time Fatras PU-200 density is **below the TDR by
  ×2.3-7 per layer** (VERIFIED, 56 fresh events, `f1r_density_bench.json`; table in §8 V4-2): IT ×2.3-3.7 (cluster size not
  in the TDR: range ×1.5-5), TBPS ×2.5-4.3, TB2S ×4.0-7.3, rising with radius as expected from out-of-time loopers and missing
  secondaries. The R0 "×1.5 one-sided" systematic does not cover this. **Baseline (adopted in fix R1; approved by the
user, D4-15, 2026-10-13):** every PU-200 event (signal overlays, B1,
  B2, C) gets a TT-level **top-up** of extra random crossings per layer, (ratio − 1) × the event's own Fatras crossings on that
  layer, z resampled from the layer's hits, φ uniform; stacked OT layers get in/out pairs (one "stub" = one crossing, the
  conservative choice for the per-crossing count); discs use the same procedure with the TDR disc occupancies. Each top-up
  crossing is its own interaction in the thinning (§4.1). **Variations** (systematic on B_PU and ε): ratios at the lower and
  upper end of their ranges (IT cluster size 3 / 1.5 pixels; OT ±0.2 in cluster size and ±5 % reading), and a correlated
  top-up (pairs of crossings with the separation spectrum of in-time Fatras same-particle double crossings, i.e. looper-like
  k = 1 pairs). The IT ratio is the weakest number: a cited IT cluster-size figure is looked for at G1 (ESTIMATE until then).
  The top-up costs no simulation but raises the finder's combinatorics (fix-R1 probe: ×4-5 per trial with the OT top-up,
  §2.4; fix-R2 profile: most of that was an O(N²) merge loop, §2.4); G2 is measured at the normalised density.
- **Selection into Fatras:** charged particles and photons with pT > 50 MeV and |η| < 4. Fatras runs with `pMin` = 30 MeV,
  multiple scattering, ionisation, bremsstrahlung and **photon conversion** on. Fatras has **no hadronic interactions** in this
  build (the config has no such switch, VERIFIED).
- **Transport format:** the probes went Pythia → Python HepMC3 → `HepMC3Reader`, which costs 22.8 ms/interaction, ≈ 4.6 s per
  PU-200 event, while Pythia itself costs 1.07 ms/interaction (VERIFIED, p1).
  - Production instead builds `acts.examples.SimParticle` objects directly in a Python reader. The constructor is available
    (VERIFIED); the cost is ESTIMATE 0.1-0.3 s/event and is measured at implementation (gate G1).
  - Nothing is stored except seeds: a PU event is regenerated bit for bit from (job seed, event index).
- **Density benchmark** against public numbers: §8 V4-2 (done in fix R1; the top-up above implements it).

### 1.5 Digitisation (U-5 (b): smearing, `doMerge = False`)

Local coordinates: cylinder (loc0, loc1) = (rφ, z); disc (loc0, loc1) = (r, φ). Baseline resolutions are binary (pitch/√12),
which the TDR confirms for the OT ("the spread … corresponds … to p/√12" [CMS-TDR-014 §12.2, PDF p.277]).

| Type | Pitch (source) | σ_rφ | σ_long (z barrel, r disc) | Variation (systematic) |
|---|---|---|---|---|
| IT 25 × 100 µm² | TDR p.74; tkLayout D111 module table (`cms_phase2_public.json`) | 7.2 µm | 28.9 µm | tkLayout parametrised 3-6 µm / 11-24 µm (charge sharing; optimistic) |
| PS 100 µm × 1.467 mm | TDR Tab. 3.1 p.29, Tab. 3.3 p.37, Tab. 9.4 p.157 | 28.9 µm | 423 µm | ±20 % |
| 2S 90 µm × 50.27 mm | same | 26.0 µm | 14.5 mm (Gaussian approximation of a uniform distribution over the strip length) | uniform smearer, 1-index strips (no long measurement) |
| BTL (timing) | crystal bars 57 mm along φ, 3.12 mm wide [CMS-TDR-020 PDF p.29] | 16 mm (along bar; ESTIMATE) | 0.9 mm | σ_t 30-40 ps at start of operation, 50-60 ps at the end of HL-LHC operation [CMS-TDR-020, text copy l.307-308, VERIFIED in fix R1 (critical C-7)]; 35 ps baseline, 60 ps end-of-life variation |

Notes:
- **Disc φ:** on a full-disc (or disc-sector) surface the φ smearing is σ_rφ/r_mid, so the rφ resolution varies by up to ×2.5
  across a disc's radial range. This is an approximation that is documented. If the endcap matters at the gate (§8), the discs
  are split into their tkLayout rings (the same plane): one more JSON loop, no rerun of Stage 3.
- **The probe swapped the BTL axes** (rφ 0.87 mm, z 16 mm). This is irrelevant for the probes (no finder variable used the BTL)
  and is corrected in production as in the table.
- **Analysis-level merging (U-5 b).** After digitisation, on the TT side, any two measurements on the same sensor merge when
  |Δu| < p_u and |Δv| < p_v (u, v the local pitch directions). The merged position is the mean, the error is enlarged to
  max(σ, |Δ|/√12), and dE is summed.
  - The rule is applied to every pair (quirk-quirk, quirk-PU, PU-PU) using the **truth** positions, i.e. touching clusters
    under binary readout.
  - Variation: 2 pitches (charge spread).
  - Channelised clustering stays a later cross-check at a few points, as the user decided. Its scope includes the IT cluster
    elongation along z with incidence angle (≈ 150 µm × cot θ, i.e. several 100 µm pixels at |η| ≳ 1.5), which the 1-vs-2
    pitch variation does not cover (critical C-11).
  - Expected effect: this sets the hit-level merging edge (≈ 13-25 keV truth level, HANDOVER §5.3) at detector level.
- **Hit-time window:** drop quirk hits with t − t_vtx − d/c > Δt_acc. Baseline Δt_acc = 25 ns (one bunch crossing, the
  Knapen et al. precedent [1708.02243 Sec.IV]), variation 12.5 ns (ESTIMATE; the CMS front-end sampling window is not public at
  this level, UNVERIFIED). PU hits are in time.
- **Hit efficiency:** 99 % per hit, flat (ESTIMATE, UNVERIFIED); variation 97 %.

### 1.6 Standard tracking (CKF): what it is for

Quirk tracks are not helices, so CKF is **not** used to find the signal. It is used for three things.
1. **PU and hard-scatter hit removal.** Measurements on CKF tracks are removed from the finder's hit pool. The tracks must have
   pT > 0.9 GeV, ≥ 7 measurements, ≤ 2 holes and \|d₀\| < 4 mm (Knapen's "unassociated hits" logic [1708.02243 Sec.III.D]).
   In the probe this removed ≈ 18 % of the measurements. Low-pT PU hits stay; they are the combinatorial background the finder
   must beat.
2. **Signal-loss monitor:** the fraction of candidate quirk measurements that sit on CKF tracks is measured on every signal
   point (0/208 in the probe; V4-6). At low Λ, where a quirk segment between crossings resembles a curved track, this can be non-zero.
3. **Veto variables:** the number of CKF tracks pointing into the candidate plane, and "the candidate is two CKF tracks"
   (prompt-pair fakes, §4.2).

Configuration: GridTriplet seeds on the TBPX + TFPX spacepoints, |z₀| < 200 mm, impact < 3 mm, minPt 0.9 GeV, 3.8112 T (the
Stage-3 B₀). Variant: minPt 0.5 GeV (more hits removed, more CPU; measured at the gate).

### 1.7 What the finder receives (per event)

- Measurements: global position, local σ (u, v), surface id and type, time (BTL), CKF-used flag, merged flag, truth link
  (signal/PU/hard scatter; used only for efficiencies and diagnostics, never by the selection).
- **PV:** the true hard-scatter vertex smeared by (σ_xy, σ_z) = (10, 15) µm (ESTIMATE from the TDR Fig. 6.13 curves at ≳ 30
  tracks [CMS-TDR-014 PDF p.108], graphical reading UNVERIFIED). Correct PV identification is applied as an efficiency: 93 % at
  PU 200 for tt̄ [ibid. PDF p.108]. The ISR-jet event is assumed similar (ESTIMATE); variation 90 %.
- **MET:** the truth pair pT (= −recoil_T from Stage 2/3; the quirk calorimeter deposit is ≲ 5 GeV, `sim/DEFERRED.md`), smeared
  per component with σ⊥ = 25 GeV (variations 15 and 35 GeV; the PUPPI MET resolution at PU 200 is UNVERIFIED, synthesis S-5).

### 1.8 Code layout (new code; nothing outside `acts/stage4/` and `data/acts_stage4/`)

| Path | Env | Content |
|---|---|---|
| `acts/stage4/code/s4geo.py` | acts | geometry builder (from the probe), material, φ-sectors, digitisation-config writer |
| `acts/stage4/code/s4pu.py` | acts | Pythia8 minimum bias → `SimParticle` reader (no HepMC3); SM hard-scatter generators |
| `acts/stage4/code/run_chain.py` | acts | one job = (sample, point, chunk, seed): inject + PU + Fatras + digitisation + CKF → compact npz |
| `acts/stage4/finder/{f0.py, f1.py, common.py}` | TT (numba) | merging, time window, PV/MET model, finder, candidate variables |
| `acts/stage4/analysis/` | TT | efficiencies, detector-level edges, P2 observables, background extrapolation, systematics |
| `acts/stage4/validation/` | both | V4-1…V4-10 (§8) |
| `acts/stage4/jobs/`, `RUNNING.md` | — | job lists (Mac / optional PC), resumable runner |
| `acts/stage4/results/*.json` | — | single source of every number; `make_docs.py` generates the tables |
| `data/acts_stage4/` | — | compact per-event outputs, validation dumps, probe outputs |

Two environments, **no new packages**: the acts env (pyacts, pythia8, numpy) for simulation, and the TT env (numba) for the finder
and the analysis. The finder never imports ACTS, so it also runs natively on the Windows PC (the TT env has a verified win-64
solve, Stage 3).

---

## 2. Finder design

### 2.1 What the finder must handle (from Stage 3 and the probes)

- **Three signal regimes** (truth-level edges from `sim/stage3/results/P2.json`, HANDOVER §5.3):
  - *Wide:* median ℓ_max ≳ R_IT, at Λ ≲ 0.43-0.94 keV (mass-dependent). Hits spread over centimetres or more in the IT and
    the pair looks like two separate curved tracks. The detector-level lower edge is set here.
  - *Ribbon:* ≈ 1-10 keV. Both quirks are inside a strip of width ~ℓ_max/2 (mm-cm) around the pair axis, with ≈ 3 hits per
    layer for heavy pairs. Coplanarity is carried by the IT (σ_n ≈ 17 µm); PS adds 0.25 mm and 2S ≈ 8 mm (synthesis S-2).
  - *Merged:* the IT pair separation is < 100 µm at 13-25 keV (truth). After analysis-level merging the two quirks give one
    straight, net-neutral 9-21× MIP "track" (synthesis S-10). F0/F1 lose it by construction. It is the separate HSCP-like
    category and is **not** in this Stage-4 finder scope (decision D4-6). Toys exist only at E1000/1200 (U-3 a).
- **Plane geometry:** the plane contains the PV and the pair momentum, so its strip axis n₃ points along the MET within
  0.15-0.25 rad (95 %; synthesis S-5). In a narrow ribbon the plane's rotation about n₃ is poorly constrained by OT hits alone,
  so **the IT must define the plane**. This is what killed PS-pair seeding in probe p4.
- **PU density** (VERIFIED, p1, per PU-200 event; the counts are what the finder sees before CKF removal):

  | layer | TBPX L1 | L2 | L3 | L4 | TBPS L1 (one sensor) | TBPS L3 | TB2S L1 | TB2S L3 | TFPX D1 | TEPX D1 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | hits/event | 6686 | 4901 | 3564 | 2811 | 5715 | 2749 | 1786 | 751 | 2256 | 2033 |
  | hits/cm² at \|z\| < 2 cm | 15.4 | 4.5 | 1.7 | 0.89 | 0.29 | 0.049 | 0.023 | 0.006 | — | — |

  These are Fatras in-time densities; the TDR benchmark (V4-2, fix R1) is ×2.3-7 higher per layer (§1.4).
- **Expected random crossings inside one candidate band** (ESTIMATE; re-derived in fix R1 per **crossing**, critical B-2,
  for W_c = 75 mm and t_tol = 30 µm, §2.2). Band = ±3σ_tot wide (σ_tot² = σ_n² + t_tol², δn = 0: the frozen definition of §2.2 step 3) × the in-window length of the
  plane-layer intersection (≈ 2W_c = 15 cm for r > W_c; ≈ πr for TBPX L1/L2). On a stacked layer a crossing needs both
  sensors' hits in the band, so μ_c ≤ μ(per sensor). μ_c (Fatras) → μ_c (TDR-normalised) and the Poisson P(≥ 2 crossings):

  | layer | TBPX L1 | L2 | L3 | L4 | TBPS L1 | TBPS L3 | TB2S L1 | TB2S L3 |
  |---|---|---|---|---|---|---|---|---|
  | μ_c Fatras | 3.0 | 1.4 | 0.53 | 0.27 | ≤ 0.63 | ≤ 0.10 | ≤ 1.5 | ≤ 0.36 |
  | μ_c TDR-normalised | 8 | 3 | 1.5 | 1.0 | ≤ 1.6 | ≤ 0.45 | ≤ 6 | ≤ 2.6 |
  | P(≥ 2), Fatras → TDR | 0.80 → 1.0 | 0.41 → 0.80 | 0.10 → 0.44 | 0.03 → 0.26 | ≤ 0.13 → ≤ 0.47 | ≤ 0.005 → ≤ 0.08 | ≤ 0.44 → ≤ 0.98 | ≤ 0.05 → ≤ 0.73 |

  So TBPX L1/L2 and the 2S layers barely discriminate (at the TDR density they are nearly always "≥ 2"), the rejection
  comes from TBPX L3/L4 and the PS layers, and with the R0 hit count (≥ 2 hits on in + out) every OT layer crossed by **one**
  particle passed, i.e. P(≥ 2) ≈ P(≥ 1 particle) (constructive A-1: 99.5-99.7 % of PU OT hits come from a particle with ≥ 2
  hits in that stacked layer). The multiplicity variables stay **split by detector type** (N_IT2, N_OT2). The measured
  best-candidate distributions (§2.4) supersede these estimates.

### 2.2 F0: the transparent baseline

Input: the hit pool after CKF removal, analysis-level merging and the time window, plus the PV and MET of §1.7. Revised in
fix R1 (critical A-1, B-2, B-3; constructive A-1); prototype `acts/stage4/probes/f1r_finder.py`.
1. **Collection window and road (pre-registered, critical B-3).** W_c = **75 mm** = R(TBPX L4)/2 = 73 mm rounded up.
   - *Physics rule:* each quirk stays within ℓ_max/2 of the pair centre of mass, which moves along n₃, so every hit of an
     event with ℓ_max ≤ R_IT lies within |u·n₂| ≤ R_IT/2. F0 targets exactly that regime (the "ribbon", ℓ_max ≤ R_IT; the
     HANDOVER §5.3 edge ℓ_max = R_IT sits at 0.43-0.94 keV). *Verified at truth level* (template events only, used to check
     the derivation, not to tune): max|u·n₂| over the TBPX hits ≤ 1.1 ℓ_max/2 in 95-100 % of central events at all 65
     tested (m, Λ) points (`data/acts_stage4/fix_r1/f1r_truth_window.json`). No signal toy and no PU-vs-signal comparison
     entered the choice. The R0 value 50 mm had no derivation.
   - Road: |Δφ(u, φ_MET)| < δ_road + asin(min(1, W_c/r)), δ_road = δ₉₅(MET model) (0.25 rad at σ⊥ = 25 GeV; S-5). At W_c = 75
     mm the TBPX L4 road is ±0.79 rad (±0.60 at 50 mm): ≈ 1.3× more L4 seed hits (ESTIMATE) and 1.5× more random hits per
     OT band.
   - **Truth-level acceptance vs W_c** (central template events, no PU; fraction with N_IT2 ≥ 3 and N_OT2 ≥ 3 *crossings*
     inside the window, true plane; `f1r_truth_window.json`) — reported, not optimised; V4-3 repeats it at detector level:

     | point, Λ | f(ℓ_max ≤ R_IT) | W_c = 50 | **75** | 100 | 150 mm |
     |---|---|---|---|---|---|
     | E1000, 0.45 keV | 0.20 | 0.26 | **0.35** | 0.44 | 0.70 |
     | E1000, 0.6 keV | 0.37 | 0.43 | **0.65** | 0.76 | 0.85 |
     | E1000, 1 keV | 0.83 | 0.81 | **0.93** | 0.96 | 0.98 |
     | Ẽ500, 0.45 keV | 0.08 | 0.09 | **0.31** | 0.40 | 0.58 |
     | Ẽ500, 0.6 keV | 0.25 | 0.37 | **0.54** | 0.71 | 0.83 |
     | E1500, 0.6 keV | 0.39 | 0.48 | **0.69** | 0.76 | 0.89 |
     | E200, 0.45 keV | 0.54 | 0.49 | **0.62** | 0.75 | 0.86 |
     | all five, ≥ 2 keV | 1.0 | 0.95-1.0 | **0.95-1.0** | 0.95-1.0 | 0.95-1.0 |

     At W_c = 75 mm the acceptance is at or above the fraction of events in the ℓ_max ≤ R_IT regime at every point, i.e.
     the F0 low edge is the regime boundary (a physics statement), not a window artefact; W_c = 50 mm cut into the regime
     (E1000 0.6 keV: 0.43 vs 0.65).
   - **Limitations by construction (analysis limitations, not physics edges):** (i) the wide regime ℓ_max > R_IT (two
     separate curved tracks; e.g. Ẽ500 at 0.45 keV, where only 8 % of events have ℓ_max ≤ R_IT); (ii) the barrel-only seed
     family outside |η| ≲ 1 until the endcap and mixed triplets of item 2 are in (D4-12), and the barrel/endcap transition
     1.0 ≲ |η| ≲ 1.3 where neither family has three layers; (iii) the merged regime (§2.1). A dedicated wide-regime topology
     (two curved tracks, each coplanar with the PV and the MET plane) is D4-14 in §10. The user approved option (a): the
     wide regime is an analysis limitation now, decided again after V4-3 at G2; it is not in any campaign.
   - The R0 claim that the (L3, L2, L1) seed family "recovers the wide regime" is withdrawn: both families share W_c. That
     family stays for efficiency (missing L4 hits), not for the wide regime.
2. **Seeds:** IT triplets with the PV constraint.
   - Barrel: (a ∈ TBPX L4, b ∈ L3) with |Δφ_ab| < 0.3 and |Δη_ab| < 0.2. The plane is n = unit(u_a × u_b), skipped if
     sin∠(u_a, u_b) < 10⁻³. The pair is kept if some c ∈ L2 has |n·u_c| < 3σ_tot,c (the seed score depends only on (a, b)).
   - Endcap: the same on (TFPX D_k+2, D_k+1, D_k) and on mixed barrel/disc triplets for 1.2 < |η| < 2.5.
   - A second seed family on (L3, L2, L1) (missing-L4 efficiency).
3. **Collect:** hits with |n·u| < 3σ_tot, **σ_tot² = σ_n²(n, hit) + t_tol², with no normal-uncertainty term (δn = 0)**.
   σ_n comes from the local errors projected on n (S-2 formula). This is the prototype's definition (`f1r_finder.py`), on
   which every probe, the margin study (§2.4), T_seed, the §2.1 μ_c, the §4.1 storage column and the t₁ measurements rest;
   it is the frozen nominal (fix R8, review R8 B-1; it supersedes fix R7's δn = min(δn_fit, δn_max), which widens the
   IT/PS bands ×1.6-15 after refit and more at the seed stage). Since σ_n(n, hit) ≤ σ_loc,max,h and t_tol is common,
   σ_tot,h ≤ σ̂_h (the n-independent tolerance of §4.2 C′) holds trivially for every candidate. δn_max = 2 mrad (the
   candidate-merge tolerance of step 4) enters **only** σ̂_h, as extra preselection and attribution margin.
   *Pre-declared variation (not the default):* δn = min(δn_fit, δn_max) added in quadrature as (δn·|u|)² to σ_tot,
   with δn_fit the larger angular standard-error component of the current normal from the fit covariance (seed plane at
   collection, PV-constrained fit at each refit); run in A5/B1 beside t_tol = 0/100 µm (σ_tot,h ≤ σ̂_h still holds with
   the cap). **t_tol = 30 µm** is the intrinsic plane-thickness tolerance,
   set to the event-level multiple-scattering floor s_eff ≈ 23-30 µm of synthesis S-2 (a physics number). Without it the
   7 µm IT band rejects real quirk hits: the Stage-3 truth residuals to the pair's own best plane are 30-180 µm (median
   `res_max_um`, central, 0.6-5 keV). Variations 0 and 100 µm are part of A5/B1 (systematic and a pre-declared ladder
   check at G3). Hits must be forward of the PV (u·n₃ > 0) and within |u·n₂| < W_c.
4. **Refit (3 iterations):** the PV-constrained weighted plane fit, i.e. the smallest eigenvector of Σ wᵢ uᵢuᵢᵀ with
   wᵢ = 1/σ_tot,i² (the S-2 χ²(n)). Recollect at 3σ_tot each time. The window axis n₃ is re-estimated at each iteration as
   the mean direction (from the PV) of the collected hits projected into the plane (a two-hit seed axis is 0.02-0.2 rad off
   the pair axis, which cut OT hits in the probe). The pre-filter around the seed plane must exceed 3σ of every hit type
   (5 mm IT/PS, 60 mm 2S; a 5 mm 2S pre-filter dropped real quirk 2S hits in a first fix-R1 pass). **Every distinct (a, b)
   seed plane with seed N_L2 ≥ T_seed is refitted before ranking**; T_seed(ρ) is fixed on PU-only samples so that the
   **pass fraction of every rung family that matters** is stable when T_seed is lowered by 2: per-trial pass of the
   counting rungs (N_IP2 ≥ 4…7, N_2S2 ≥ 1…3), of the core-hit χ² rungs and of the width rungs, not only the best N_L2
   (review R2 C-5, R3 C-6; mapping of N_L2 to the ladder variables in item 5; `f1r_tseed_check.json` shows a χ²
   change in 2 of 4 trials with the best N_L2 unchanged). Fix-R1 probe: T_seed = 6. Candidates with normals within
   2 mrad are merged; ranking (N_L2, −χ²/ndf). No truth enters seeding, refit or ranking (R0's p5 refitted truth-selected
   signal seeds; critical B-1).
5. **Candidate variables** (counting per **crossing**; critical B-2, constructive A-1):
   - crossings per layer: n_hits on single-sensor layers (TBPX, TFPX, TEPX); **min(n_in, n_out)** on stacked OT layers
     (TBPS, TB2S, TEDD PS/2S; one crossing = one in/out pair, the stub definition without the pT window, which loopy slow
     quirks would fail). One particle crossing a stacked module gives one crossing, not two;
   - N_IT2: IT layers with ≥ 2 crossings (barrel TBPX L1-4; endcap the TFPX/TEPX discs crossed);
   - N_OT1, N_OT2: OT layers with ≥ 1 / ≥ 2 crossings; N_L2 = N_IT2 + N_OT2;
   - **ladder variables (review R3 C-6):** N_IP2 = IT + PS layers with ≥ 2 crossings and N_2S2 = 2S layers with ≥ 2
     crossings. Hence N_L2 = N_IP2 + N_2S2; in the barrel N_IP2 ≤ 7 (TBPX L1-4, TBPS L1-3) and N_2S2 ≤ 3, so N_L2 ≤ 10.
     The ladder (§2.5) cuts on N_IP2 and N_2S2. The probe evidence in §2.4 is quoted at N_L2 rungs because the probes
     stored N_L2; N_L2 stays a diagnostic;
   - the R0 hit count (≥ 2 hits on in + out) is kept as a diagnostic only;
   - χ²/ndf of the refit and its p-value (all in-band hits; diagnostic); t_est (weighted rms out-of-plane, S-2);
   - **robust core width w_core (rung variable, fix R2, review R2 B-1):** w_core = 1.4826 × MAD of u·n₂ over the
     candidate's in-band **IT + PS** hits, with centre c = their median. It is computed once, with no iteration. 2S hits are
     excluded: their n₂ coordinate carries the 14.5 mm strip-length error. It is the f1r `dw_core`, the variable review R2
     tested. *Physics:* a ribbon pair keeps every hit within ℓ_max/2 of the CM line (§2.2 item 1), so w_core ∝ ℓ_max for
     the signal. A combinatorial PU candidate fills the window: uniform over ±W_c gives 1.4826 × W_c/2 = 56 mm. *Rejected
     definition:* an iteratively 2.5σ-trimmed width locks onto local hit clusters inside PU candidates (per-trial minimum
     0.5-3.4 mm at N_L2 ≥ 8 on PU only; `fix_r2/f2r_profile_summary.json`), so it is not used;
   - **core-hit χ² (rung variable, fix R2):** χ²_core/ndf = λ_min(Σ_core wᵢ uᵢuᵢᵀ)/(n_core − 2), i.e. the exact
     PV-constrained refit χ² over the **core hits**. These are the IT + PS in-band hits with |u·n₂ − c| < 2.5 w_core, plus
     2S hits whose n₂ coordinate lies within that interval enlarged by 3σ of their n₂ projection. It is one step with no
     iteration, for the same reason as w_core. For a ribbon it drops the PU hits filling the rest of the window, which
     dilute the all-hit χ² at the normalised density (§2.4). For a window-filling PU candidate the core is nearly the whole
     band: PU only, TDR-OT, N_L2 ≥ 8 gives n_core/n_in-band ≈ 53/60 and an unchanged χ²/ndf distribution (median 2.87 vs
     2.89; `f2r_profile_summary.json`). It has not been evaluated on signal (deliberately, before the freeze);
   - |Δφ(n₃, MET)|; f_CKF (fraction of candidate hits on CKF tracks); the number of CKF tracks with ≥ 5 hits in the band;
   - **stored only, never cut on:** Δw (R0 definition: rms of u·n₂ of all in-band hits, dominated by PU hits filling the
     window), |n_z|, a geometrically matched stub count on stacked layers (review R2 C-10: in/out pairs with |Δ(rφ)| and
     |Δz| inside windows from the sensor spacing; a diagnostic only, because the full-cylinder geometry has no modules and
     without a pT window the match is weak), and (truth, diagnostics) the interaction composition.
6. **F0 selection** (shape fixed now; thresholds from the WP ladder of §2.5): N_IT2 ≥ 3, N_IP2 and N_2S2 thresholds
   (ladder), w_core < W_k (ladder), p(χ²_core) > p_min (ladder), |Δφ(n₃, MET)| < δ₉₅, f_CKF < 0.2. **No fixed Δw cut**
   (critical A-1). The width enters only as background-ordered rungs whose signal cost is reported vs Λ, not as a fixed
   cut chosen in advance. The R0 "Δw < 1 cm (as Knapen)" rejected 100 % of the
   probe's signal candidates (Δw 11-34 mm) and 74-88 % of truth-level central E1000/Ẽ500 events at 1 keV, and the R0
   "Δw > w_min (not a single track)" is redundant once layers count crossings (a single track never gives ≥ 2 crossings
   per layer). The other selection elements were re-checked against the probes: N_IT2 ≥ 3 keeps 0.95-1.0 of central truth
   events at ≥ 1 keV (`f1r_truth_window.json`); f_CKF: 0/208 quirk measurements on CKF tracks (p3); δ₉₅ is a generator-level
   rule; p_min and k come from the background-only ladder.

CPU: the R0 prototype took 5-10 s/event single-threaded (p5). The fix-R1 prototype (numba seeding + numba refit of every
seed with seed N_L2 ≥ 6, W_c = 75 mm, t_tol = 30 µm) takes the times quoted in §2.4 (VERIFIED); its profile is in §2.4
(fix R2). At the **TDR-normalised IT + OT** density it measures 211 s/trial with the merge vectorised. Reference speeds
under the one-day cap (§6.2, fix R3; C′ inside C1 since fix R4): t₁ ≲ 7.0 s lets the minimal campaign C1 fit one Mac
day; t₁ ≲ 5.6 s lets each of the four campaigns of the full scope fit one Mac day. That is a ×30-40 speed-up. Under the
deadline (§11), t₁ ≈ 3 s is the target and 5 s the last value at which two campaigns fit. The routes and
their ESTIMATE gains are in §6.2. G2a (§11) measures t₁ and the user then chooses the scope. Over the full scope the
cost scales as ≈ 53 CPU-h per s/trial at ρ = 1 plus ≈ 2.8 CPU-h per s of ρ = 2 trial time (§6.2).

### 2.3 F1: the one improved variant (quirk-hypothesis variables on top of F0)

F1 adds four variables on the F0 candidates, again with no signal tuning (all thresholds come from the WP rule, §2.5, on
background samples only). Revised in fix R1 (critical B-10, constructive B-2/B-3; adopted within the approved F1 scope).
- **Non-helicity:** split the candidate hits into ≤ 2 subsets by the sign of the in-plane coordinate along n₂ (a two-cluster
  split per layer) and fit each subset with a helix (a circle in rφ plus a straight line in s-z) under **two** origin
  hypotheses: (i) from the PV; (ii) from a free origin on the plane (the displaced-vertex hypothesis: conversions, V0s,
  nuclear interactions, kinks). h = min over the hypotheses of χ²_helix/ndf. Without (ii) a two-prong vertex at r = 22-60 mm
  would look non-helical from the PV, i.e. signal-like (§4.2, NI estimate).
- **Opening pattern** (replaces the R0 "crossing count", which needed a signed separation that hits cannot provide): per layer
  the |separation| s_l of the two in-plane clusters along n₂, on the **resolvable layers only**, fixed by detector type and not
  by the event: IT and PS layers (projected σ along n₂ ≤ 0.45 mm for any orientation); 2S layers are never used (14.5 mm).
  Statistic: χ²_lin of a straight-line fit s_l = a (r_l − r₀), a ≥ 0, r₀ ≤ r_min (the opening of two prongs from one point,
  which is what V0s, conversions, NIs and track pairs do), using the hit errors. Quirk pairs turn around and cross, so their
  |s_l| vs r is non-monotonic (large χ²_lin). The variable is defined for ≥ 4 resolvable layers with two clusters.
- **Late arrival (timing categories, constructive B-2):** Δt_BTL = the earliest BTL time in the candidate band relative to the
  PV time minus the straight light-speed path (σ_t 35 ps). Quirk median first-hit delays 3.1/9.0/15/27 ns at E 200/500/1000/1500
  (VERIFIED by the constructive reviewer, `r1c_signal_handles.json`); in-time PU BTL hits: > 2 ns 2.8 %, > 5 ns 7 × 10⁻⁴,
  > 10 ns 0/5610 (`r1c_pu_btl_time.json`). Two **pre-registered, disjoint categories**, combined by the budget split
  of §2.5 item 5 (review R2 B-2):
  - **SR-T:** ≥ 1 in-band BTL hit with Δt ∈ [t_min, Δt_acc]; t_min is fixed from the PU-only late-hit spectrum alone
    (the delay at which the per-hit rate in B1 falls below 10⁻⁴, a pre-declared value) and the out-of-time overlay (§1.4);
  - **SR-G:** everything else (geometry only).
  Each category walks **its own copy** of the §2.5 ladder (same rung list, same order) to its own working rung r*_T,
  r*_G. SR-G therefore usually stops at a tighter rung than SR-T, because it has no time factor. This is the intended
  effect of the timing tag, and it is now well defined.
  In SR-T the background factorises into P(F0 candidate with ≥ 1 in-band BTL hit) × P(in-band BTL hit late), the second
  factor **measured** on ~10³ BTL hits/event × 2 × 10⁴ B1 events (FASER-type ABCD). The independence is tested on the loose
  rungs (late fraction in bins of N_L2 and χ²; pass at p > 0.05).
- **dE/dx proxy (constructive B-3):** truncated-mean deposited energy of the in-band IT hits (quirks: `h_dE` with Landau
  fluctuations added at injection, HANDOVER §1; PU: Fatras `depositedEnergy`), both calibrated with one scale from the
  muon-gun MIP peak, quantised to 4-bit ToT as a variation (4-bit ToT: CMS-TDR-014 §4, text copy l.3381-3382). It is an F1
  variable and a cross-check axis, not the primary factorisation (it correlates with low-pT protons).

F1 selection = F0 ∧ (h > h_min) ∧ (χ²_lin > o_min) ∧ (dE/dx > e_min), split into SR-T / SR-G. All thresholds are rungs of
the per-category WP ladder (§2.5). Which background class each variable acts on is mapped in §2.6. The helix and
opening-linearity tests target single-interaction topologies and give little rejection of combinatorial PU. The BTL acceptance limits SR-T to |η| ≲ 1.5; ETL timing (|η| > 1.6) is added only if the endcap
matters at the gate (§1.2).

### 2.4 Combinatorics and the blind signal-vs-PU margin (fix R1; VERIFIED on small probe samples)

**R0 claims re-tagged (critical B-1, constructive C-2).** R0's "signal 10/10 barrel layers vs best PU N_L2 ≤ 6 (24 trials)"
was not a like-for-like result. The signal candidates came from **truth-selected seeds** (`p5_finder_triplet.py` refits
`out[:30] + sigtrip`), the PU search refitted only the top 30 of ≈ 10⁵ seeds, and both used the R0 hit count, which a
single particle satisfies on a stacked module. The critical reviewer's blind full refit with the R0 count gave a best PU
N_L2 of 9 in 14/24 trials (`review_r1/r1_pu_fullrefit.json`).

**Fix-R1 probe** (`acts/stage4/probes/f1r_finder.py`; summaries in `data/acts_stage4/fix_r1/f1r_summary.json`,
`f1r_margin.json`). Everything is blind and identical for signal and PU: the same seeding, the refit of every (a, b) plane
with seed N_L2 ≥ 6, ranking, and per-crossing counting; W_c = 75 mm, t_tol = 30 µm. The setup:
- **PU:** 56 fresh PU-200 events (`f1r_pu_gen.py`, Fatras in time, fixed 200 interactions, no CKF removal), 4 roads each,
  with a luminous-region PV;
- **signal:** central (|η_pair| < 1) template events of chunk c01 at E1000 {0.6, 1, 2, 3, 5} keV, Ẽ500 {1, 3}, E200 {1, 3}
  and E1500 1 keV, overlaid row-major on these PU events (numpy smearing). The finder is barrel-only, so the result applies to
  |η| < 1;
- **two densities:** "Fatras" (in time only) and "TDR-OT" (OT layers topped up to the TDR benchmark, §1.4; the IT stays at the
  Fatras density, so the IT is still under-dense by ×2.3-3.7);
- signal efficiency = fraction of events with a candidate that contains ≥ 50 % of the event's barrel quirk hits **and**
  passes the rung. The blind event-level pass fraction (any candidate) agrees within one event.

| rung (N_IT2 ≥ 3 always) | PU Fatras: trials (of 224) / events (of 56) | signal ≥ 1 keV, Fatras (of 79) | PU TDR-OT: trials (of 32) / events (of 8) | signal ≥ 1 keV, TDR-OT (of 14) |
|---|---|---|---|---|
| N_L2 ≥ 9 | 26 (11.6 %) / 19 | 0.89 [0.84, 0.92] | 32 / 8 | 0.79 [0.62, 0.90] |
| N_L2 = 10 | **0 (< 1.3 %/trial, < 5.2 %/event, 95 % CL)** / 0 | **0.77 [0.72, 0.82]** | 28 (88 %) / 8 | 0.71 [0.55, 0.85] |
| N_L2 ≥ 9, χ²/ndf < 2 | 2 (0.9 % [0.3, 2.1]) / 2 | 0.85 [0.80, 0.89] | 25 (78 %) / 8 | 0.43 [0.28, 0.60] |
| N_L2 = 10, χ²/ndf < 2 | 0 / 0 | 0.72 [0.66, 0.78] | **4 (12.5 % [6.6, 21]) / 4** | **0.36 [0.21, 0.53]** |
| N_L2 = 10, χ²/ndf < 1.5 | 0 / 0 | 0.54 [0.48, 0.61] | 0 (< 8.9 %/trial) / 0 | 0.21 [0.10, 0.38] |

(Brackets: 68 % Clopper-Pearson; percentages are per road trial.) E1000 at 0.6 keV: 3/12 at N_L2 = 10 (Fatras) and 0/2
(TDR-OT). This is consistent with the truth-level window acceptance of §2.2 plus the wide-regime loss.

**Reading (the honest margin):**
- With per-crossing counting and **Fatras-only** PU, signal and PU separate by **one layer**. The best PU candidate has
  N_L2 = 7/8/9 in 49/149/26 of 224 trials and never 10, while 77 % of signal events at ≥ 1 keV reach 10. χ²/ndf adds a
  factor ≈ 13 at N_L2 ≥ 9 (PU 0.9 % vs signal 85 %). With the **R0 hit count** the same PU candidates reach 10/10 in 152
  of 224 trials, so the definition fix is worth a lot.
- At the **TDR-normalised OT density** the layer count saturates. 2S and PS bands then hold ≥ 2 random crossings most of
  the time (§2.1), and PU reaches 10/10 in 88 % of trials. The extra in-band PU hits also raise the signal χ²: the
  all-hit χ²/ndf of the signal-matched top candidate is 1.0-2.1 (median ≈ 1.4) over the 5 events where it is the top
  candidate at TDR-OT, against Fatras-density medians of 0.9-1.5 per point (review R2 C-8; `f1r_summary.json` →
  `sig_t*.*.chi2ndf_q`). At (N_L2 = 10, χ²/ndf < 2) the measured pass fractions are **signal 0.36 [0.21, 0.53] vs PU 0.125
  [0.066, 0.21] per trial**. That is 5/14 signal events, 8 of the 14 at 1 keV, and 4/32 PU trials, so the ratio has a 68 %
  range of roughly ×1-8 (review R2 C-11). Either way it is 7-8 decades from the ≲ 3 × 10⁻⁹ per event needed (§4.1). With
  the IT also topped up (the adopted baseline), PU reaches N_L2 = 10 in 3/3 profiled trials, with 1 717 (2-mrad-merged)
  candidates in total (fix R2, `f2r_profile_summary.json` → `t1`).
- **The robust core width does separate (review R2 B-1).** The variable was stored but not used in R1. On the same blind
  outputs (`review_r2/r2_corewidth.json`; event passes if any candidate passes; signal = matched candidate):

  | density, rung | w_core cut | PU trials passing | signal 1 keV | signal ≥ 2 keV | signal 0.6 keV |
  |---|---|---|---|---|---|
  | Fatras, N_L2 ≥ 9 | none | 26/224 | 40/48 | 30/31 | 4/12 |
  | Fatras, N_L2 ≥ 9 | < 20 mm | 0/224 | 20/48 | 30/31 | 2/12 |
  | TDR-OT, N_L2 = 10 | < 15 mm | 0/32 | 1/8 | 4/6 | 0/2 |
  | TDR-OT, N_L2 ≥ 9 | < 10 mm | 0/32 | 0/8 | 4/6 | 0/2 |

  PU only, fix R2 (`f2r_profile_summary.json`). These samples are separate from the review-R2 trials above:

  | density | rung | PU candidates (trials) | per-trial min w_core | trials with a candidate < 37.5 / 18.75 / 9.4 / 4.7 mm |
  |---|---|---|---|---|
  | TDR-OT | N_L2 ≥ 9 | 530 (5) | 14.6-32 mm | 5 / 3 / 0 / 0 |
  | TDR-OT | N_L2 ≥ 8 | 3 026 (5) | 9.1-14.7 mm | 5 / 5 / 1 / 0 |
  | IT + OT normalised | N_L2 = 10 | 1 717 (3) | 16.5-19.4 mm | 3 / 2 / 0 / 0 |
  | IT + OT normalised | N_L2 ≥ 9 | 18 903 (3) | 12.2-14.2 mm | 3 / 3 / 0 / 0 |
  | IT + OT normalised | N_L2 ≥ 8 | 75 323 (3) | 6.3-9.2 mm | 3 / 3 / 3 / 0 |

  Reading: the PU minimum width falls with density (26 mm at Fatras density in review R2, 10-30 mm at TDR-OT, 6-14 mm at
  the full normalised density, 3 trials, N_L2 ≥ 8-9). The narrow rungs (< 9.4, < 4.7 mm) are PU-free in these few trials. These
  samples cannot say how many decades the narrow rungs buy; the thinning (§4.1) and G3 must measure that. A width rung is
  effectively an ℓ_max cut, so it costs efficiency at low Λ (signal 1 keV: 20/48 at < 20 mm, Fatras).
- **Consequence for the design (no threshold is set here; that is the WP rule's job):** F0's **layer count and χ²** cannot
  reach the target alone. F0 as a whole has one strong geometric handle, the ribbon width. It acts on the measured dominant
  PU class (combinatorial candidates with k ≈ 16-47 interactions) and is now a rung family (§2.5). The working point is
  therefore expected in the width rungs plus dE/dx and the SR-T time factor. The helix and opening tests act mainly on
  single-interaction topologies (§2.6). Expected consequence, separate from the W_c/t_tol attribution of V4-3: the
  background-limited low edge moves up in Λ, and a background-free WP is likely only at Λ ≳ 1.5-2 keV (ESTIMATE, §2.6).
  Because the 2S layers carry almost no rejection at the normalised density (P(≥ 2) ≈ 0.98 on TB2S L1), the 2S rungs come
  last in F0 (§2.5).
- **Composition** (truth, diagnostics only): the best PU candidates contain hits from 16-23 PU interactions (Fatras) or
  32-47 (TDR-OT), and need k_min ≈ 13-19 interactions at rung N_L2 ≥ 8 in the ρ = 2 superpositions (§4.1 box). They are
  combinatorial, high-k objects, which suits the thinning extrapolation. |n_z| does **not** separate: the best PU has a
  median of 0.84-0.86, the signal-matched candidates 0.77 (constructive C-3's truth n_plane median of 0.23-0.30 is not what
  the detector-level planes show here). Δw (R0 definition, the rms over all in-band hits) is 34-44 mm for PU and 18-36 mm
  for signal: it is window-filled and not a discriminant (critical A-1). This is **not** true of the robust core width
  w_core (above), which R1 wrongly treated as equivalent.
- **CPU (unoptimised probe, 1 thread):** 7.8 s per trial (Fatras, median), 48 s per trial (TDR-OT), and **400-1300 s per
  trial at ρ = 2** (Fatras; 31-61 × 10³ refits). **Fix-R2 profile** (`f2r_profile.py`, ρ = 1 only; `f2r_profile_summary.json`):

  | density (trials) | as coded (s/trial) | of which Python duplicate merge | merge vectorised (s/trial) | seeding / numba refit / numpy refit / merge (s) | refitted seeds, candidates after the 2-mrad merge |
  |---|---|---|---|---|---|
  | TDR-OT (5) | 14-52 (median 29) | 72 % | 5.7-11.8 | 3.8 / 1.3 / 3.1 / 0.16 | 1.3 × 10⁴, 8 × 10³ |
  | **IT + OT normalised (3)** | 3 400-6 000 | 97 % | **159-228 (median 211; per-trial sums of the stage times)** | 95 / 30 / 52 / 33 | 2.0 × 10⁵, 1.1 × 10⁵ |

  "As coded" = the measured stages plus the Python merge cost extrapolated from its measured per-comparison cost (the
  original loop was timed on the first 3 000 candidates of each trial; the merge itself was executed vectorised, with the
  same order and criterion). Fix R1 measured a 48 s median at TDR-OT on 32 other trials, run with 7 parallel workers.
  The merge compares every new candidate with every kept one in Python (O(N²), 0.53 µs per comparison). The ×4-5 TDR-OT
  slowdown of fix R1 and most of the ρ = 2 blow-up are this loop: stored ρ = 2 counts attribute ≈ 46 % of that time to it
  and ≈ 26 % to per-candidate thinning Monte Carlo (12 ms × ≈ 2 × 10⁴ candidates; `f2r_cost.json`). After vectorising it,
  the full-density cost is real combinatorics. 2 × 10⁵ seeds pass T_seed = 6, because L1/L2 and 2S bands saturate the seed
  score at the normalised density. Every seed then scans all ≈ 4 × 10⁴ road hits. The routes in §6.2 target exactly these
  terms.

| quantity | value |
|---|---|
| measurements per PU-200 event | 1.09-1.46 × 10⁵ (56 fix-R1 events, fixed 200 interactions); CKF (not applied in the fix-R1 probe) removes ≈ 18 % |
| barrel road hits per trial (W_c = 75 mm, Fatras) | 1.2-1.4 × 10⁴ (10-90 %) |
| seed pairs (a, b) with a valid c in the road | 2.3-3.5 × 10⁴ per trial (Fatras, 10-90 %) |
| refitted seeds (seed N_L2 ≥ 6) | 3.4-8.0 × 10³ per trial (Fatras); T_seed = 4 gives the same best N_L2 in 4/4 trials (`f1r_tseed_check.json`) |

### 2.5 Working point: pre-registered rule (never tuned on signal toys)

Rewritten in fix R1 (critical B-6, constructive B-8). This implements D4-4 (F0 + F1, B ≤ 0.3); "+1σ" is now defined for
an extrapolated, log-normal B.
1. The *shape* of the selection (§2.2/§2.3: variable definitions incl. per-crossing counting, W_c, the F1 variables) is fixed
   before any production. There is **no fixed Δw cut** (critical A-1, §2.2); the robust core width enters only as
   background-ordered rungs (item 3).
2. **δ₉₅** (MET alignment) is computed from the MET smearing model applied to the Stage-2 truth pair kinematics: the 95 % quantile
   of |Δφ(MET, pair)|. It is a generator-level quantity, not a finder output.
3. **One ordered 1-D ladder per category** (rewritten in fix R2 after review R2 B-1, B-2). Rungs r = 1…R; each rung
   tightens exactly one threshold of the previous rung, in this pre-declared order (barrel numbers; the endcap uses the
   fraction of crossed layers, same order):
   - F0 counting (counts only; revised in fix R3, review R3 B-4): (N_IT2 ≥ 3, N_IP2 ≥ 4) → N_IP2 ≥ 5 → 6 → 7, where
     N_IP2 = IT + PS layers with ≥ 2 crossings (7 in the barrel). Until R2 the first rung also carried p(χ²_core) > 10⁻³,
     which the counts-only thinning of these rungs cannot evaluate; that cut is now the head of the χ²_core family;
   - **F0 ribbon width (new):** w_core < 37.5 → 18.75 → 9.4 → 4.7 mm, i.e. W_k = W_c/2^k, k = 1…4. The thresholds are
     geometric: halvings of the physics window W_c = R_IT/2. Rung k accepts ribbons up to roughly ℓ_max ≲ R_IT·2^−k and is
     Λ-agnostic. They are not tuned on signal;
   - F0 core χ²: p(χ²_core) > 10⁻³ → 0.01 → 0.05;
   - F0 2S: N_2S2 ≥ 1 → 2 → 3 (N_2S2 = 2S layers with ≥ 2 crossings);
   - F1, appended: h_min ∈ {2, 3, 5} → o_min ∈ {2, 3, 5} (χ²_lin/ndf) → e_min ∈ {1.3, 1.6, 2.0} MIP.

   That makes 4 + 4 + 3 + 3 + 9 = **23 rungs** per category.

   *Ordering principle (background only).* The counting rungs come first and contain counts only: they define a candidate
   and are the base of the exact thinning (§4.1), so their extrapolation and its closure test T1 use only quantities the
   counts determine. Within F0, the remaining families are ordered by their **per-trial** effect on PU-only samples at the
   normalised density (rephrased in fix R3, review R3 C-8):
   - width: no full-density trial has a PU candidate below 9.4 mm at N_L2 ≥ 9 (3 trials, 18 903 candidates; §2.4);
   - core χ²: strong per candidate (p > 10⁻³ keeps 1.5 % of the full-density PU candidates at N_L2 ≥ 8), but weak per
     trial. Every full-density trial with stored candidates still has 286-348 candidates with p > 10⁻³ and 14-15 with
     p > 0.05 (`review_r3/r3_chi2core_p.json`). R2's "barely shifts the PU distribution" compared core-hit with all-hit
     χ²; it was not a statement about cut power;
   - the 2S layers give almost no rejection (P(≥ 2) ≈ 0.98 on TB2S L1, §2.1).

   F1 stays last and in its R1 order. The order of N_IP2 relative to the width was not measured; it follows the
   counting-first rule.
   *Signal information used (disclosed):* the decision to add the width family was prompted by review R2's
   `r2_corewidth.json`, which looked at signal pass fractions on the fix-R1 probe rows. Those rows are already excluded
   from the template efficiencies (item 10). The variable definition (the stored f1r `dw_core`), its thresholds (W_c/2^k)
   and its place in the ladder are fixed from geometry and PU-only measurements. No threshold was chosen to keep a signal
   efficiency. This is allowed under item 1 because the shape is fixed before production and before the freeze (item 9),
   and the WP rung is still chosen by B alone. *Not adopted:* narrow/wide width **categories**. They would split the budget
   four ways (with SR-T/SR-G). The low-Λ events they would protect are handled by the fallback of §2.6, whose primary
   rung per (m, Λ) admits only the width rungs that the hypothesis's ribbon passes by construction.
   - SR-T and SR-G each walk **their own copy** of this ladder; SR-T requires the time tag (item 7) at every rung.
   The B used at rung r of category c is the **total over all sources in that category**, B_c(r).
4. **One background budget.** B(r) = B_PU + B_SM,prompt + B_conv + B_V0 + B_NI + B_DIF + B_corr(k = 1 guns) + B_cosmic + B_halo
   (§4.2 gives each term's normalisation). Each term carries a central value and a log-normal uncertainty with
   σ_ln² = (stat)² + (extrapolation-model spread, §4.1 step 5)² + (density normalisation, §1.4)² + (normalisation)². B(r) is
   the Monte-Carlo sum of the log-normals; **B₈₄(r)** is its 84th percentile (= "+1σ" in log space). Every term is a
   product of measured factors (a rate, a pass fraction at a loose rung, conditionals, and for NI/DIF the preselection
   fraction of §4.2). Each factor follows the zero- and low-count rule of item 4a.
4a. **Zero- and low-count rule (pre-declared; fix R5, review R5 B-1).** It applies to every factor of every B term: the B1/B2
   rung factorisation (§4.1 step 3), the C′₀ and C′_PU factors, the NI/DIF preselection fractions, and the SM samples C.
   - *Measuring population.* Each conditional p_j (one extra requirement) is measured on the tightest population of that
     sample with **M_j ≥ 10** entries, and not necessarily on the rung just before it. The factorisation/independence test of
     §4.1 step 4 covers that substitution: its correlation factor c multiplies the product if c > 1 at 2σ. **c cannot be
     measured for a zero factor (no joint population exists), so c is evaluated among the term's non-zero factors only;
     a term in the zero branch carries the largest c measured among its other factors (c = 1 if none), and is flagged
     (fix R6, review R6 C-3).** A pass fraction at
     a loose rung (the start of the chain) is a direct count.
   - *N_j ≥ 1.* The central value is N_j/M_j, with σ_ln,stat from the event bootstrap (never below 1/√N_j).
   - *N_j = 0.* **Among the term's zero factors, the one with the largest M_j** (the strongest bound; ties → the first
     along the ladder order; fix R6, review R6 C-2, replacing "the first zero along the ladder order") enters at its
     one-sided **68 % CL Poisson upper bound
     1.14/M_j**, with a pre-declared **σ_ln = 1.0**. That term's 84th percentile is then 3.1/M_j, i.e. its B₈₄ carries the
     95 % CL bound (3.0/M_j) of that one factor.
     - It is the term's **only bounded factor**. Measured non-zero conditionals of other requirements still multiply.
     - Any other zero factor of the same term enters as 1. No rejection is credited for it.
     - *Why the largest M_j.* It is as valid as the first-zero rule: one zero factor is chosen by a pre-declared rule that
       uses only the M_j, and every other zero factor enters as 1 ≥ its true value. It avoids discarding the strongest
       available bound: e.g. an F0 zero measured on C′_PU (M ≤ 500) before an F1 zero measured on C′₀ (M up to 10⁵)
       would otherwise cost ×200 (×2 000 at M = 50) (`review_r6/r6_checks.json` → `first_zero_order`).
     - So a zero is never entered as 0, and an upper bound enters at most once per term: not once per rung, and not once
       per factor.
   - *Reporting.* A term whose value at rung r uses the zero branch is flagged in the B table.
     - If that term makes B₈₄,c(r) > 0.11 at every rung of category c, item 6 applies (the §2.6 fallback, or the
       pre-declared user-approved +50 % steps). No other remedy is allowed.
     - The rule is frozen in `WP_RULE.md` (item 9).
   - *Why this and not the alternatives:*
     - entering 0 is anti-conservative;
     - 3/M at every zero factor would put B above 0.11 for any term with one unmeasured deep factor (review R5: B_NI ≈ 10²
       events);
     - the rule credits only measured rejection, plus one bounded factor.
5. **WP per category, budget split (review R2 B-2; scheme (c); split value and branches revised in fix R3, review R3
   B-3).** For c ∈ {T, G}: r*_c = the loosest rung with **B₈₄,c(r) ≤ 0.11 events in 3 ab⁻¹ for r*_c and for every
   tighter rung** of that category (the extrapolated B need not be monotonic in r).
   - *Why 0.11.* Quantiles of skewed log-normals are super-additive. Two independent categories, each at B₈₄,c = 0.15 with
     σ_ln = 2.3, give a combined B₈₄ of 0.41 (0.38 at correlation 0.5; 0.30 fully correlated; `review_r3/r3_checks.json`).
     The combined B₈₄ is ×2.71 the per-category value for independent categories at σ_ln = 2.3 (×2.50 at correlation 0.5,
     ×2.0 fully correlated). So 0.3/2.71 = **0.11** per category keeps the combined B₈₄ ≤ 0.30 in the worst case at the
     planning σ_ln (`fix_r3/f3r_split.json`: 0.298 independent, 0.275 at correlation 0.5, 0.22 correlated; 0.13-0.22 if the
     two categories are unequal, for B₈₄,G = 5-50 % of B₈₄,T). The combined check below then binds only if σ_ln ≳ 2.4 with nearly equal categories
     (e.g. 0.32 at σ_ln = 2.5, 0.38 at 3.0, independent). The value is a convention computed from the log-normal algebra
     alone, with no signal input.
   - *Combined guard (applies when both categories have a WP).* The combined B₈₄ of B_T(r_T) + B_G(r_G) is computed by
     Monte Carlo over the log-normals, with shared sources (density normalisation, extrapolation model, K-factor) fully
     correlated between categories. A pair (r_T, r_G) is **accepted** iff the combined B₈₄ ≤ 0.3 for that pair **and for
     every component-wise tighter pair** (the item-5 guard applied to the pair, since B is not monotone). Start at
     (r*_T, r*_G).
   - *Deterministic continuation if the pair is not accepted.* Move the category with the larger B₈₄,c at the current
     pair one rung tighter (tie → SR-G). A category already at its tightest rung R stays there and the other one moves.
     Every category stays inside its own guard, because every rung tighter than r*_c satisfies B₈₄,c ≤ 0.11. Stop at the
     first accepted pair. The path has at most 2(R − 1) = 44 steps, so the loop terminates.
   - *If (R, R) is reached and not accepted,* neither category has a background-free WP. Both are reported under the
     fallback rule of §2.6.
   - *If exactly one category has a WP* (the other fails item 5), the combined check is not applied. The background-free
     claim (B₈₄ ≤ 0.11 ≤ 0.3) is made for that category alone; the other category is reported under §2.6. The Stage-5
     likelihood is still two-bin, each bin at its own pre-declared selection (r*_c or the §2.6 fallback rung) with its own
     log-normal B. A limit does not require B ≤ 0.3. The 3-event discovery statement is made only for the background-free
     category.

   *Why this scheme:* (a) a fixed rung offset needs a background-only choice of Δ that couples the two ladders and has no
   natural value before G3. (b) An interleaved 1-D path over (r_T, r_G) must fix an order over 23 × 23 rung pairs before G3
   shows which rungs PU populates. (c) is the only scheme where each category is an ordinary monotone 1-D ladder (the R1
   B-6 requirement), SR-T can stop looser than SR-G, and the result maps directly onto a two-bin counting likelihood in
   Stage 5. The equal split is a convention: no signal information is used to set it, and it is not optimised. 0.3 in
   total keeps the 95 % CL limit near the zero-background 3 events. The rule is strict: with σ_ln ≈ 2.3 (a ×10 spread),
   B₈₄,c ≤ 0.11 needs a median B_c ≲ 0.011 (B₈₄ = median × e^σ_ln). The planning split used only to size the samples (§4.1, §5) is 0.1 PU + 0.1 SM
   prompt/correlated + 0.1 rare (NI, DIF, cosmics) summed over categories; it is **not** part of the rule.
6. If no rung of category c satisfies item 5: that category has no working point. It is reported with the **fallback
   deliverable of §2.6**, which is pre-defined and not chosen after seeing the outcome. The user is told (options: more
   B1/B2 statistics, i.e. the later pre-defined campaigns C2/C3 or the +50 % steps of §4.1, each a one-day run approved
   by the user (§6.2); or accept the fallback). No re-ordering of the ladder and
   no new rung after the freeze. (Review R2 C-6: R1's "one pre-declared F1 step" was never declared and is deleted.)
7. The time threshold t_min and the in-time window come from the PU-only BTL spectrum (B1) and the out-of-time overlay only.
8. Signal **templates** are used only to report efficiencies and edges at the WP that rule fixes. Signal **toys** are used only
   for the P2 pseudo-experiments.
9. **Freeze before any signal efficiency.** The ladders, the variable definitions (incl. w_core and χ²_core), the budget
   split, the B sum, the per-family extrapolation methods and closure tests (§4.1), the zero-count rule (item 4a), the C′
   preselection and attribution rules with σ̂_h, δn_max, σ_tot with δn = 0 (§2.2 step 3; fix R8) and the shared
   PV/hit hand-over (pre-CKF, pre-merge toy measurements), and the C′₀ necessity check
   with its failure path (§4.2; gate V4-10, fix R6), the fallback deliverable with its
   admissibility rule, its frozen inputs (smoothed Λ_R, the βγ_IT table and its hash) and fallback selections (§2.6), the campaign definitions (§6.2) and this
   rule are frozen in `acts/stage4/finder/WP_RULE.md` **at the start of G2, before V4-3/A1** (the first signal efficiencies).
   G2 then measures candidate-finding efficiencies with the frozen definitions. Any later finder change (a bug fix, a CPU
   optimisation) is logged with its reason, re-run on B1/B2, and re-reviewed; it may not use signal efficiencies as input.
10. **Probe rows excluded.** The signal rows used by the plan probes (E1000 chunk-c00 event indices 7, 8, 15, 16, 24, 26, 39, 42 at 0.6/1/3
    keV; the fix-R1 rows of chunk c01 listed in `data/acts_stage4/fix_r1/f1r_summary.json` → `sig_t0.<point>.rows`) are
    dropped from the template efficiencies (≈ 0.2 % of the counting set; the effect is negligible but the rule is clean).
11. **Campaigns and the rule (fix R3).** The rule above is applied to the union of all background samples produced so
    far. After C1 the result is labelled *preliminary (C1 statistics)*. The reported r*_c is the one on the union of the
    background samples of all campaigns the user ran. Whether to run a further campaign is decided by the user on cost,
    background reach and closure results (§6.2, §11). Signal yields or efficiencies are not an input to that choice, and
    the plan never proposes one on that basis.

### 2.6 Feasibility and fallback (fix R2, review R2 B-4; fallback redefined in fix R3, review R3 B-2)

**Which variable acts on which background class.** "Combinatorial PU" is the measured dominant PU class: random hit sets
from k ≈ 16-47 interactions (§2.4). "k = 1" means single-interaction topologies from PU or the hard scatter: conversions,
V0s, loopers, prompt track pairs. Basis: M = measured in a probe; D = by construction of the variable; E = ESTIMATE, to be
measured at G3/C′.

| variable (rung family) | combinatorial PU (k ≫ 1) | k = 1 topologies | nuclear interactions (not in Fatras) | decays in flight | cosmics / halo |
|---|---|---|---|---|---|
| N_IT2, N_IP2 (crossings) | weak beyond the first rungs: saturated at the normalised density (PU N_L2 = 10 in 88 % of TDR-OT trials) (M) | strong against single tracks (one crossing per layer); a two-prong vertex gives ≥ 2 only behind the vertex (D) | weak at the normalised density: random L1/L2 crossings supply N_IT2 (§4.2) (E) | strong (one hit per layer per segment) (D) | strong (one crossing per leg) (D) |
| w_core (ribbon width) | **strong on PU (M)**: PU fills the window (per-trial min 6-32 mm over the densities and rungs probed). **Signal at the normalised density: E** (unmeasured by design): the ≥ 2 keV medians of 4-13 mm are at Fatras density. The MAD breaks down at 50 % contamination, and at the full density the in-band IT + PS PU crossings (≈ 15-17 per band, §2.1) approach a heavy pair's ≈ 20 hits, so the signal width can inflate (review R3 C-3; §12 risk 2b) | none: two prongs from one point near the PV are narrow too (D) | weak (E) | weak (E) | none (D) |
| χ²_core | moderate: ×13 at Fatras density for the all-hit χ², eroding with density; χ²_core not yet tested on signal (M) | none: two straight lines through the PV are exactly coplanar (D) | weak (E) | weak (E) | none |
| road \|Δφ(n₃, MET)\|, PV plane | measured in B1, not a separate rung (M) | same (M) | same | same | strong (d₀/z₀) (D) |
| f_CKF, CKF-track veto | weak: low-pT PU hits are not on CKF tracks (M, p3) | strong against prompt pT > 0.9 GeV tracks (D) | some (E) | some (E) | some |
| h (helix, PV + free origin) | **little or none**: a random hit set is non-helical, i.e. signal-like (review R2) (D) | strong against conversions, V0s, loopers, track pairs (D; E until the guns) | moderate with the free origin (E) | some (E) | none |
| o (opening linearity) | **little or none**: random sets are non-monotonic, i.e. signal-like (D) | strong against two-prong vertices (D; E until the guns) | moderate (E) | some (E) | none |
| dE/dx (truncated mean) | moderate for βγ ≲ 1 (IT median βγ_IT 0.92 at E500, 0.68 at E1000, 0.52 at E1500); weak at E200-E400 (1.82-1.14) and for Ẽ200/Ẽ500 (1.76/1.07) (`fix_r4/f4r_admissibility.json`); diluted by in-band PU hits (E) | same as combinatorial (MIP tracks) (E) | anti-discriminating for slow protons (E) | weak | weak |
| SR-T time tag | strong for heavy masses (median delays 9-27 ns vs PU > 5 ns 7 × 10⁻⁴ per hit); weak at E200 (3.1 ns vs PU > 2 ns 2.8 %) (M, r1c) | same (in time) | same | same | some (bottom leg late, ±3.6 ns) |

**Plain feasibility statement (ESTIMATE, order of magnitude; not demonstrated).**
- At the normalised density, F0 counting plus χ² leaves PU at ~10⁻¹ per trial (measured 0.125 at TDR-OT; the IT top-up
  makes it worse). The requirement is ≲ 3 × 10⁻⁹ per event for B_PU ≤ 0.1. Under the strict B₈₄ rule (σ_ln ≈ 2.3,
  B₈₄,c ≤ 0.11) the median per category must be ≲ 0.011 events, i.e. P_PU ≲ 3 × 10⁻¹⁰ per event even if PU took the
  whole category budget (N_trig ≈ 3.3 × 10⁷; `f3r_campaigns.json` → `reach`).
- The width rungs act on the dominant class. When the expected number of random crossings per band is small, the
  probability of ≥ 2 random crossings in a band of length W_k falls roughly as (W_k/W_c)² per layer, over ~7 IT + PS layers.
  Several decades are therefore possible at Λ ≳ 2 keV, but not measured. dE/dx and SR-T add 1-3 decades each for
  m ≳ 500 GeV. The helix and opening tests add little against combinatorial PU; they are needed for the k = 1 classes and
  for NI (§4.2: ≈ 8-9 decades needed for NI, 9-10 under the strict B₈₄ rule, once the kink and line + near-vertex-hit
  paths are included (ESTIMATE, fix R6; the two-prong-only estimate gave 6-7); not demonstrated).
- **Where a B₈₄ ≤ 0.3 WP is plausible:** heavy E (m ≳ 500 GeV) at Λ ≳ 2 keV. Ẽ500 at Λ ≳ 2 keV only if the width
  rungs and SR-T suffice: it has no admissible dE/dx level (βγ_IT 1.07; review R4 C-3).
- **Where it is uncertain:** Λ ≈ 1-2 keV, and m ≈ 300 GeV.
- **Where it is implausible:** Λ ≲ 1 keV (the 0.45-1 keV edge, where the ribbon is wide and the width rungs cut the
  signal), and E200 at any Λ (dE/dx and timing are weak there). In these regions the honest expectation is a result with
  non-zero, log-normally uncertain background, and the low-Λ detector-level edge is set by background, not by the finder.
- In every region the extrapolation must also close (§4.1). If it fails, the failure-path value applies and the plausible
  region shrinks. Finder speed under the one-day cap (§6.2) is a second, independent feasibility risk: the thinning reach
  is ≈ 5 × 10⁻¹⁰ per trial with C1 alone (above the 3 × 10⁻¹⁰ requirement), ≈ 1.6 × 10⁻¹⁰ after C2 and ≈ 10⁻¹⁰ after C3.

**Fallback deliverable (pre-defined now, frozen with `WP_RULE.md`; new in fix R2, redefined in fix R3 after review R3
B-2; option (i) approved by the user 2026-10-13, D4-17; inputs pinned in fix R4).**

*Why R2's version did not work.* R2 put the only primary fallback limit at R_E, the tightest rung (full F1). R_E contains
w_core < 4.7 mm, i.e. ℓ_max ≲ 13 mm (uniform fill: 1.4826 × MAD = 0.37 ℓ_max), and e_min = 2.0 MIP. That removes the
signal by construction exactly where the fallback is needed: at Λ ≲ 1 keV, where ℓ_max is a sizeable fraction of R_IT, and
at E200, where the IT βγ ≈ 1.8 gives dE/dx near the MIP value. It also left the R_A-R_D limits without a usage rule, so a
per-point best-of was possible.

*Hypothesis admissibility (pre-declared now; uses no detector-level signal efficiency, no toy and no limit).* Two
families remove a hypothesis's signal by construction: the width rungs (when the ribbon is wider than the threshold) and
the dE/dx rungs (when the quirks are near minimum ionising). For each hypothesis (m, Λ) the admissible thresholds are
computed from two Stage-3 truth quantities of that hypothesis: Λ_R(m), published in `sim/stage3/results/P2.json`, and
βγ_IT(m), computed from the Stage-3 truth by a frozen script (below). This is the analogue of centring a mass window on
the hypothesised mass. Both inputs are fixed now from generator/truth kinematics, before any detector-level look:
- **Width.** Λ_R(m) is the Λ at which the median ℓ_max = R_IT (HANDOVER §5.3). **The smoothed value is used**:
  `sim/stage3/results/P2.json` → `edge_fits_in_m` → `F/lower_lmax_RIT_closed` `deg2` (quadratic in ln m, as HANDOVER
  §5.3 recommends) for E, and `S/lower_lmax_RIT_closed` `deg1` (the only fit stored for the three Ẽ masses) for Ẽ;
  P2.json sha256 `e63d19d8d1ae76dee9693bfff1098bc62a457e7d6c95c02d1fab83b502442459`. The per-mass values (`edges.*.lower_lmax_RIT_closed`) are non-monotonic in m
  (E800 0.737, E900 0.652 keV; pulls vs the smoothed curve up to ±1.6σ), so they would make k_adm jump with template
  noise. Smoothed Λ_R = 0.431 (E200) … 0.741 (E1500) keV for E and 0.594 / 0.773 / 0.944 keV for Ẽ200 / 500 / 1000
  (`fix_r4/f4r_admissibility.json` → `Lambda_R`). Since ℓ_max ∝ Λ⁻² at fixed kinematics, the median ℓ_max = R_IT·2^−k
  at Λ_R(m)·2^{k/2}. Rung k (w_core < W_c/2^k) accepts ℓ_max ≲ R_IT·2^−k (§2.5 item 3). With a one-rung margin,
  **k_adm(m, Λ) = the largest k ∈ {0, …, 4} with Λ ≥ Λ_R(m)·2^{(k+1)/2}**, where k = 0 means no width cut. For
  example, k_adm = 4 needs Λ ≥ 5.66 Λ_R (2.4-5.3 keV), and k_adm = 0 below 2 Λ_R (0.86-1.9 keV).
- **dE/dx.** **βγ_IT(m)** is pre-declared as follows (review R4 C-2): Stage-3 p2 truth, configuration BM, **template
  half** (tt_split = 0), counting set in_eta25 ∧ status = 1; per event the median of |p|/m over the event's IT hits
  (both quirks); per (m, Λ) point the median over events; **βγ_IT(m) = the median over all p2 Λ points of that
  species-mass** (16-20 points). The script is `probes/f4r_admissibility.py` (output `fix_r4/f4r_admissibility.json`).
  It reproduces the R1 constructive probe `review_r1_constructive/r1c_signal_handles.json` (sha256
  `14aba918c3ba7e016b6f083da96e2a1b3e52a58f139a84ed7c5ad19f270170c7`) exactly at its 18 points, and is re-run unchanged at the freeze, with the output hash recorded in
  `WP_RULE.md`. Values: E200 1.82, E300 1.25, E400 1.14, E500 0.92, E600 0.94, E700 0.81, E800 0.81, E900 0.72,
  E1000 0.68, E1100 0.62, E1200 0.60, E1300 0.58, E1400 0.53, E1500 0.52; Ẽ200 1.76, Ẽ500 1.07, Ẽ1000 0.74. The per-point
  values are flat within a few % for Λ ≳ 0.6 keV for most species-masses (exception: Ẽ1000, +8 % at 0.7 keV; review R5
  C-2) but rise towards the smallest Λ (E500: 0.88-0.95 above 0.6 keV, 1.08 at 0.3 keV; up to +18 % over the median at
  0.3 keV across the 17 species-masses). The value used for hypothesis
  (m, Λ) is therefore **βγ_IT(m, Λ) = max(βγ_IT(m), the per-point median at that Λ)**: the median over Λ points removes
  template noise, and the max never admits a dE/dx level that the hypothesis's own βγ would not (conservative for the
  signal; it matters only at Λ ≲ 0.7 keV). **e_adm(m, Λ) = the largest e_min ∈ {1.3, 1.6, 2.0} MIP with
  e_min ≤ R(βγ_IT(m, Λ))/1.25**, else none.
  *Unit conversion (review R4 C-3):* e_min is in units of the muon-gun MIP peak (§2.3), while the PDG Bethe ratio is
  relative to the minimum of the mean loss. R is therefore pre-declared as the **restricted** energy loss in silicon
  (PDG restricted-loss formula, T_cut = 100 keV, density-effect parameters for Si) of the quirk at βγ_IT(m), divided by
  the same restricted loss for the calibration muon gun at its median βγ (the gun is pT 1-10 GeV, |η| < 2.5, as V4-9).
  It is computed at the freeze with cited constants. The factor 1.25 is a pre-declared margin for Landau fluctuations and
  the truncated mean (convention). The Si constants are those of the PDG 2024 silicon table (Atomic and Nuclear Properties,
  `pdg.lbl.gov/2024/AtomicNuclearProperties/MUE/muE_silicon_Si.txt`: I = 173.0 eV, a = 0.1492, k = 3.2546, x₀ = 0.2015,
  x₁ = 2.8716, C̄ = 4.4355, δ₀ = 0.14). The Sternheimer (1984) set in `f4r_admissibility.py` agrees with them to
  ≤ 0.05 %, and review R5 re-ran the levels with them (`review_r5/r5_checks.json` → `bethe_PDG`). K, Z/A and ρ cancel in
  R; ρ enters only through the density-effect parameters. **Expectation (ESTIMATE; `f4r_admissibility.json` →
  `bethe_ESTIMATE`, confirmed with the PDG constants by review R5):** no admissible dE/dx level at E200-E400, **Ẽ200 and Ẽ500** (R ≤ 1.56); 1.3 at E500-E600
  (in the pre-declared muon-gun unit R/1.25 = 1.34-1.44 at E500 across I ± 10 %, T_cut = 50-200 keV and βγ_μ = 10-300,
  so 1.3 is robust at the median βγ_IT. It was borderline, 1.29-1.30, only in review R4's mean-loss/minimum convention,
  which is not the pre-declared unit); 1.3-1.6 at E700-E800; 1.6 at E900 and Ẽ1000; 1.6-2.0 at E1000; 2.0 at
  E1100-E1500. These are at the median βγ_IT(m). At **Λ ≲ 0.7 keV** the max rule can lower a level by one step
  (review R5, `maxrule_level_changes`, 24 point-levels):
  - Ẽ1000 1.6 → 1.3 at 0.3-0.7 keV;
  - E1100 2.0 → 1.6 up to 0.5 keV, and E1200 up to 0.35 keV;
  - E900 1.6 → 1.3 at 0.3 keV;
  - E500 and E600 lose 1.3 at Λ ≤ 0.45 and ≤ 0.5 keV.
- The counting, χ²_core, 2S, h and o rungs and the SR-T tag are admissible everywhere: none of them removes a ribbon
  pair's signal by construction (§2.6 table).

*Fallback selection.* **r_fb(m, Λ, c)** = N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p(χ²_core) > 0.05 ∧ N_2S2 ≥ 3 ∧ (w_core < W_{k_adm}
if k_adm ≥ 1) ∧ h > 5 ∧ o > 5 ∧ (dE/dx > e_adm if any), plus the time tag for c = T. That is the tightest ladder selection
with only the inadmissible thresholds relaxed. There are at most 5 × 4 = 20 distinct fallback selections; R_E (k = 4,
e = 2.0) is one of them. Their thinning weights are computed in the job together with the 23 ladder rungs (≈ 20 × 4 B
more per set). Their B uses the per-family methods and closure tests of §4.1, and their B₈₄ the log-normal sum of §2.5
item 4.

*Primary result per (m, Λ, c), pre-declared:*
- if category c has a WP r*_c (§2.5 items 5-6) **and** r*_c is admissible at (m, Λ) (its width level ≤ k_adm and its
  dE/dx level ≤ e_adm), the primary is the background-free result at r*_c;
- otherwise the primary is the **fallback result at r_fb(m, Λ, c)**, with non-zero, log-normally uncertain B.
- *Mixed admissibility (review R4 C-4):* if both categories have a WP but r*_c is admissible at (m, Λ) for only one
  category, the primary pair is (r*_c, r_fb,c′), and the "exactly one category has a WP" branch of §2.5 item 5 applies at
  that point: the background-free claim is made for the admissible category alone, and the other bin enters the two-bin
  likelihood at r_fb,c′ with its own log-normal B (the combined guard evaluated on (r*_T, r*_G) is not used there).

Both are reported wherever both exist; which one is primary follows only from this rule. **Per-point best-of is
forbidden**: no comparison of ε, yields or limits between selections enters any reported result.

Deliverables:
1. **ε(m, Λ) and B (central value, σ_ln, B₈₄) per category** at r_fb(m, Λ, c) and at the fixed reporting rungs, at every
   point whatever r* is:
   - R_A = end of F0 counting (N_IP2 ≥ 7);
   - R_B = R_A + w_core < 18.75 mm;
   - R_C = R_A + w_core < 4.7 mm;
   - R_D = the full F0 ladder;
   - R_E = the tightest rung (full F1).

   R_A-R_E are **tables of ε and B only; no limit is computed or quoted at them**.
2. **One Stage-5 expected 95 % CL limit per (m, Λ), only for the primary selection.** It is a two-bin counting likelihood
   (SR-T, SR-G), with each bin at its primary selection and B as a log-normal nuisance (σ_ln from §2.5), built with pyhf
   (methodology §7.1), in `results/fallback_limits.json`. The D4-13 deliverables (approved: `results/sensitivity.json`,
   the pyhf workspace, discovery reach) use the same primary selections.
3. The Fatras-density (in-time only) and truth-level results are kept only as **labelled optimistic bounds**.

**What the fallback can claim:**
- at every point, ε by factor, B with its log-normal uncertainty, and the P2 observables (sep_IT^det, t_est, w_core as an
  ℓ_max observable, the D4-13 velocity observables) at a pre-declared selection that keeps that hypothesis's signal by
  construction. These are per-event templates and valid whatever B is;
- an expected exclusion with non-zero background where S ≫ B₈₄;
- where B₈₄(r_fb) ≤ 0.3 (both categories combined as in §2.5 item 5), that the point is background-free at its fallback
  selection. That statement is made on the same footing as the nominal one;
- unchanged in every case: A1/V4-3 (no-PU efficiency and detector-level edges vs the truth edges), P_fake vs rung with
  its closure, the SM/NI/DIF table, the U-2 panel.

**What it cannot claim:**
- optimality of r_fb;
- a 3-event discovery reach or "background-free" edges and yields where B₈₄ > 0.3 (those edges are labelled with their
  B₈₄);
- anything for ℓ_max > R_IT (the wide regime, D4-14 (a)) or the merged regime.

**Plain expectation (ESTIMATE).** At Λ ≲ 1 keV and at E200, r_fb has no width cut (or only k = 1) and no dE/dx cut. Its
PU rejection then rests on counting + χ²_core + 2S + h/o. Counting + χ² leave ~10⁻¹ per trial (TDR-OT, measured), and h/o
act little on combinatorial PU. So **in those regions the fallback is expected to deliver ε and B tables and the
observables, and essentially no exclusion.** Heavy masses at Λ ≈ 1-2 keV (k_adm = 0-2 with dE/dx and SR-T) are the
regions where the fallback limit can be non-trivial.

*Alternatives considered for D4-17 (the user approved (i), the rule above, on 2026-10-13):*
- (ii) strictly signal-free: R_E everywhere, as in R2. It is empty at low Λ and at E200;
- (iii) a split-template choice: choose the rung on half A of the templates, report on half B. This halves the template
  statistics and still picks per point.

The production samples and the cost (§6.2) are the same for the nominal and fallback deliverables.

---

## 3. Trigger and offline preselection

Assumed path (synthesis S-18, Knapen et al., Li et al.): **L1 MET (PUPPI) + HLT MET/MHT**, monojet-like, driven by the ISR
recoil. The L1 track trigger is **not** used, because only 23-47 % of quirk OT crossings form 2 GeV stubs at Λ ≤ 3 keV and they
form no helices (S-18).

Model (an efficiency from Stage-2 truth; no detector simulation of the trigger):
- MET_true = pT(QQ̄). The quirks are invisible to the calorimeter apart from ≲ 5 GeV deposits, which are carried as a one-sided
  ≲ 2 % MET bias (`sim/DEFERRED.md`).
- Smear MET_true per component with σ⊥ = 25 GeV (15/35 variations). Then ε_trig = ε_L1+HLT(MET_reco), an error-function turn-on
  with a 50 % point T₅₀ and width σ_T:
  - baseline T₅₀ = 200 GeV, σ_T = 20 GeV, plateau 0.98 (ESTIMATE);
  - the Phase-2 L1 TDR (CMS-TDR-021) PUPPI MET thresholds are to be **fetched and cited** at implementation (a public PDF
    download, no install). Until then the numbers are UNVERIFIED and carried as ±25 GeV on T₅₀.
- **Offline preselection:**
  - MET > 250 GeV (offline plateau; variation 200 GeV);
  - ≥ 1 jet with pT > 100 GeV, |η| < 2.4;
  - min Δφ(jet_1-4, MET) > 0.5;
  - vetoes on isolated e/μ (pT > 10 GeV), τ_h (pT > 20 GeV) and γ (pT > 15 GeV).

  The jets come from the Stage-2 `jets` record (truth, smeared 10 %/√E ⊕ 5 %, ESTIMATE). The vetoes cost the signal ≈ 0 (no
  prompt leptons), so they enter only the SM background (§4.2).
- **Efficiency chain per (m, Λ):** ε = ε_trig × ε_presel × ε_PV-ID × ε_fiducial(|η_pair| < 2.5) × ε_finder(PU 200) × ε_status.
  - Yields: N = σ_norm × L × ε. σ_norm comes from `mg_events.sigma_norm_fb` (N_IC = 2, LO × K) on the unweighted Stage-3
    events, with w_max per event.
  - Nuisances: tail rate +12…+15/−11…−13 % (Stage 2) and σ_norm ±5 %.

---

## 4. Backgrounds

### 4.1 PU-only fake rate (the finder on pile-up alone)

**Required level.** LO Pythia8 (CP5, 14 TeV, 2→2 V + parton with pT̂ > 150 GeV; truth MET > 200 GeV) gives 14.6 pb for Z(νν)+j
and 15.8 pb for W(ℓν)+j (VERIFIED as a Pythia number, `data/acts_stage4/p6/p6_xsec.json`; as a physics estimate ESTIMATE: no
K-factor, no tt̄/multijet, no vetoes). That is N ≈ 9 × 10⁷ events in 3 ab⁻¹ before vetoes, and ≈ 3-5 × 10⁷ after the lepton
vetoes and a 250 GeV threshold (ESTIMATE). PU fakes are independent of the hard scatter, so B_PU = N_trig × P_fake. B_PU ≤ 0.1
needs **P_fake ≲ 3 × 10⁻⁹ per event**. A direct measurement would need ≳ 10⁹ PU-200 events (≈ 4 × 10² CPU-years at 13 s/event;
R0 said 10⁵, corrected per critical C-2): impossible. The pT̂ > 150 GeV truncation, `HadronLevel:all = off` (no τ-decay
neutrinos in the MET) and a K-factor of 1.2-1.4 all raise N slightly (critical C-6); the 3 × 10⁻⁹ is a planning number.

**Method (pre-registered; rewritten in fix R1 after critical B-4/B-5 and constructive B-1/B-7):**

*Density convention.* ρ = 1 is the **benchmark-normalised** PU-200 event: Fatras in-time PU plus the per-layer density top-up
of §1.4 (V4-2). A density-ρ event (ρ = 2, 3) is the superposition of ρ independent normalised PU-200 events (each with its own
top-up and its own CKF removal). Non-integer ρ is not used (R0's ρ = 1.5 was not a superposition).

1. **Direct ladder (B1).** N_PU = 2 × 10⁴ independent PU-200 events (fresh Pythia seeds, Poisson(200), new vertices), each with
   K = 4 MET directions at φ₀ + kπ/2 (φ₀ random). **The roads are not disjoint in the IT.** The half-width is
   0.25 + asin(min(1, W_c/r)). At W_c = 75 mm it is ≈ 1.05 rad on TBPX L3, so roads π/2 apart share L1-L3 hits, and L4
   (0.79 rad) sits at the edge (review R2 C-1; the R1 figure "0 % of L3/L4 in > 1 road" was for W_c = 50 mm,
   constructive B-7, `r1c_pu_composition.json`). **The per-trial rate is the primary P_fake** (review R2 C-2): it is the mean
   over the 4 roads of the per-road pass indicator. A data event has exactly one MET road, so the physical fake rate is the
   single-road rate. The ≥ 1-of-4 per-event rate over-states it by up to ×4 and is kept as a diagnostic. Errors and the
   effective number of independent trials come from the event-level bootstrap (fix-R1 probe: n_eff ≈ trials,
   `f1r_summary.json` → `rungs.*.n_eff_trials`). Reach with zero counts at 95 % CL: ≈ 4 × 10⁻⁵ per trial (8 × 10⁴ trials
   after campaign C3, if n_eff ≈ trials holds at the normalised density) and 1.5 × 10⁻⁴ per event; with C1 alone
   (2 × 10⁴ trials) 1.5 × 10⁻⁴ per trial (§6.2).
   - The MET alignment is part of the road, so the per-candidate ×13-34 of S-5 is **measured**, not assumed.
   - **PV of a PU-only trial:** a luminous-region point (σ_z 45 mm, σ_xy 5 µm) drawn independently of the PU vertices; the
     distance to the nearest PU vertex is stored (critical C-12, constructive C-5). The hard-scatter vertex's own UE is
     covered by C and the k = 1 guns (§4.2).
   - Stored per candidate (truth, never used by the selection): the number of contributing interactions, particles,
     max hits per particle, secondary-generation flag, |n_z|, and the thinning weights of step 2 (constructive B-1, C-3).
     Road hits of a 2 000-event B1 subset are stored (≈ 1.7 GB) so that a post-G3 finder change does not force a full
     regeneration (critical C-10).
2. **Density ladder with interaction-count (k) thinning (B2; replaces the R0 power law A_r ρ^{α_r}).** PU-200 at density 1 is,
   exactly, a Poisson thinning of the density-ρ superposition that keeps each interaction with q = 1/ρ. For every candidate found
   at density ρ, with in-band hits from the interaction set S, the thinning weight
   w_r = Σ_{T ⊆ S passes rung r} q^{|T|} (1 − q)^{|S|−|T|}
   is computed per rung family by the method in the table after step 3 (fix R2, review R2 B-3). For the counting rungs it
   uses the stored per-interaction hit counts: exact enumeration for |S| ≤ 12; above that an exact dynamic programme over
   per-layer crossing-count states, or importance-sampled Monte Carlo with its error carried into σ_ln (review R2 C-9; the
   fix-R1 probe used plain Monte Carlo with 2 × 10⁴ subsets and one fixed seed for every candidate). Candidates are counted
   once per **distinct passing hit set** (candidates sharing ≥ 50 % of their in-band hits are one; the maximum weight of the
   set is kept), at every ρ alike. Then the ρ = 1 expected number of passing candidates per trial is
   P̂₁(r) = ⟨Σ_sets w_r⟩_trials (a union bound, conservative for a probability). A candidate that needs k specific interactions gets w = ρ^{−k}: the single-
   interaction topologies (conversions, V0s, loopers, a PU vertex on the PV) enter with ρ^{−1} and the random multi-hit
   coincidences with ρ^{−k}, k large, **with no fitted exponent**, so the ∝ ρ term the power law under-estimates is kept and
   Poisson saturation is handled per candidate (critical B-4 a). Each top-up crossing counts as its own interaction.
   - Points: ρ = 2 only in the pre-defined campaigns: 1 000 events × 2 roads in C1, 3 000 after C2, 5 000 after C3
     (§6.2). ρ = 3 (2 000 events, 1 road) is **not** in any default campaign. It is the optional campaign C5 (rule below),
     behind its own timing gate G2c (§11). One list everywhere (§5, §6).
   - **Reach (critical B-4 c).** At ρ = 2 a candidate with k_min = 20 has w = 2⁻²⁰ ≈ 10⁻⁶. 2 × N_ρ2 trials then probe
     ⟨Σ w⟩ ≈ 10⁻⁶/(2 N_ρ2) per trial if such candidates are present at ρ = 2. That is ≈ 5 × 10⁻¹⁰ with C1 alone,
     1.6 × 10⁻¹⁰ after C2 and 10⁻¹⁰ after C3, against the per-category requirement P_PU ≲ 3 × 10⁻¹⁰ (§2.6). Whether such
     candidates are present is measured at G3: the WP rung is "reachable at ρ" if ≥ 10 candidates at density ρ pass the
     rung.
     - **If the WP rung is not reachable at ρ = 2,** the rate at the WP rung is obtained directly by the **rung-to-rung
       factorisation** (step 3) from the deepest reachable rung, with that step's own closure test T3.
     - Only if T3 fails is ρ = 3 (C5) offered to the user, as an extra one-day campaign behind G2c.
     - If C5 is not run or does not help, the T3 failure path of step 4 applies and the user is told (§2.5 item 6).
   - The power law A_r ρ^{α_r} (fitted on ρ = 2, on ρ = 3 if C5 ran, and on the ρ = 1 point) is kept only as the
     alternative model in the spread.
3. **Per-layer factorisation** (Knapen et al.'s method [1708.02243 Sec.IV]): P(r+1) = P(r) × p_{r→r+1}, the conditional
   probability, measured on the candidates passing rung r, that the extra requirement is also met. With per-crossing counting
   (§2.2) "a second crossing in layer l" needs a second particle, so p is the physical coincidence probability. Below the
   deepest rung with ≥ 10 counts, each conditional is measured on the tightest population with ≥ 10 entries. Zero counts
   follow the rule of §2.5 item 4a, the same for every sample (B1, B2, C, C′).
3b. **Extrapolation method per rung family (pre-registered; fix R2, review R2 B-3).** The R1 text covered only the
   counting rungs, but at the normalised density the WP will sit in the width, χ², F1 or timing rungs. Each family gets
   one method. The width and χ²_core are both driven by the in-band PU density, so they are **not** treated as independent
   of the count: they use per-subset recomputation. Factorisation is used only where a per-subset refit is too costly, and
   its conditional is then measured at the target density ρ = 1.

   | rung family | how P₁(r) is obtained | stored per distinct hit set (ρ = 2; B1 as well) | cost per set | closure test |
   |---|---|---|---|---|
   | N_IT2, N_IP2, N_2S2 (counting; counts only since fix R3, so T1 is computable from counts) | per-subset recomputation (thinning) from per-interaction (layer, side) counts; enumeration / DP / importance sampling (step 2) | interaction id, layer, side per in-band hit (≈ 3 B/hit) | current plain MC: **12-16 ms** (VERIFIED, `f2r_profile_summary.json`); DP ≲ 1 ms (ESTIMATE) | T1 (ρ = 2 → 1), T2 |
   | w_core, χ²_core (all three p(χ²_core) rungs, incl. p > 10⁻³ since fix R3) | per-subset recomputation with the ρ-level plane and axis fixed. w_core(T) and the centre c(T) come from the stored u·n₂ of T's IT + PS hits. **The core is re-centred per subset**: core(T) = hits of T with \|u·n₂ − c(T)\| < 2.5 w_core(T) (+ the 2S rule of §2.2). χ²_core(T) = λ_min(Σ_{h ∈ core(T)} w_h u_h u_hᵀ)/(n_core(T) − 2) is summed **per hit**: per-interaction pre-summed moments are not enough, because core membership changes per subset. The per-hit records of the storage column provide it. This is the exact PV-constrained refit of the fixed hit set, so there is no "plane not refitted" bias in χ². The hit re-collection after a refit is ignored (an approximation covered by T1w). Subsets are drawn by importance sampling conditional on the last counting rung (N_IP2 ≥ 7). This now applies to every set passing N_IP2 ≥ 7 without a χ² pre-filter (the probes stored N_L2, not N_IP2, so their number per ρ = 2 trial is unmeasured; G2b times it) | per in-band hit: interaction id, layer/side, u (3 × float32), σ_tot (float32; δn = 0, §2.2 step 3): ≈ 24 B/hit, 1.5-2.5 kB per set | 2-10 ms with 10³ subsets (ESTIMATE; vectorised eigvalsh on (10³, 3, 3)) | **T1w:** the T1 statistic and lever-arm rule at the tightest width or χ²_core rung with ≥ 10 B1 counts |
   | dE/dx (truncated mean) | per-subset recomputation of the truncated mean of T's IT hits | + dE per IT hit (float32) | < 1 ms (ESTIMATE) | T1e at the first dE/dx rung if it has ≥ 10 B1 counts, else T3 |
   | h (helix), o (opening linearity) | **factorisation:** P₁(F1 rung \| last F0 rung) measured directly at ρ = 1 on B1 (the conditional is not extrapolated in density), × P₁(last F0 rung) from the rows above. Independence is tested with the conditional in 3 bins of road-hit count (density) and at the two tightest F0 rungs reachable in B1. A correlation factor c (max ratio over bins) multiplies the estimate if c > 1 at 2σ. Check: per-subset recomputation of h and o on 200 random ρ = 2 sets | hits as for the width rows, for the 200-set check only | factorisation negligible; check ≈ 1 s per set (ESTIMATE), < 0.1 CPU-h | T3 + the density-bin test + **T3s** (factorised vs recomputed on the 200 sets, \|z\| < 2) |
   | SR-T time tag | factorisation P(candidate with ≥ 1 in-band BTL hit) × P(in-band BTL hit late) (§2.3). The first factor comes from per-subset recomputation (BTL hits carry an interaction id); the late fraction includes the out-of-time overlay | in-band BTL hits: interaction id, time | negligible | time-independence test (late fraction in bins of N_IP2, w_core, χ²_core and density) |

   *Storage and in-job cost at ρ = 2.* Hit records for every candidate are not affordable: at ρ = 1 and the full normalised
   density one trial already has ≈ 1.1 × 10⁵ candidates after the 2-mrad merge (median; q90 1.2 × 10⁵;
   `f2r_profile_summary.json`, where `n_distinct_hitsets` is a copy of `n_kept`, i.e. 2-mrad-distinct, not the ≥ 50 % hit-set
   convention), i.e. ≈ 0.2-0.3 GB per trial and ≳ 2 TB over 10⁴ ρ = 2 trials.
   - The weights for all rung families are therefore computed **in the job**, and only weights are stored: 23 ladder
     rungs + ≤ 20 fallback selections (§2.6) × 4 B per set.
   - Hit records (≈ 2 kB per set) are stored for two samples (ESTIMATE, corrected in fix R3, review R3 C-2):
     - (a) sets passing N_IP2 ≥ 7, at most 200 per trial (randomly sampled and weighted if more): ≤ 0.4 MB per trial,
       ≈ 4 GB over 10⁴ trials;
     - (b) a 1 % random sample of the sets passing the loosest rung: at ≥ 10⁵ sets per ρ = 2 trial (ρ = 1 already has
       1.1 × 10⁵), ≥ 2 MB per trial, i.e. **≥ 20 GB over 10⁴ trials**.
     Together that is ≈ 24 GB at the full B2 (≈ 5 GB with C1 alone), carried in §6.3.
   - **Sub-sampling (pre-declared strata).** If the per-set weight cost makes the ρ = 2 trial fail the G2b criterion
     (§11), weights are computed on pre-declared random fractions, with weight × 1/f, unbiased and the extra variance in
     the bootstrap σ_ln:
     - f_lo for the sets below N_IP2 ≥ 6;
     - f_hi ≥ 0.1 for the sets passing N_IP2 ≥ 6, where most of the weight cost sits.
     Both fractions are fixed at G2b from the PU-only timing. Every set passing N_IP2 ≥ 7 that is in the hit-record
     sample (a) is always weighted. If f_hi = 0.1 is still too slow, G2b fails and the user is asked.
4. **Closure and factorisation tests (pre-registered gate V4-7; critical B-5):**
   - **Test T1 (thinning ρ = 2 → ρ = 1):** at the tightest rung r₁ with ≥ 10 passing candidates in B1. **Minimum lever arm:**
     the mean thinning factor at r₁, ⟨Σ w⟩ / ⟨N_pass(ρ = 2)⟩, must be ≤ 0.1 (≥ 1 decade); if not, r₁ moves to the next
     tighter rung that still has ≥ 10 B1 counts. If no such rung has a 1-decade lever arm, T1 uses ρ = 3 → ρ = 1 if C5 was
     run. Otherwise T1 is evaluated at the rung with the largest lever arm, and the missing lever arm is treated as a
     closure failure of unknown direction: B_PU takes the anti-conservative-failure value (upper envelope, below).
   - **Test T2 (thinning ρ = 3 → ρ = 2)**, only if C5 is produced: same construction at a rung with ≥ 10 counts at ρ = 2.
   - **Test T3 (rung factorisation):** predict rung r₁ from rung r₁ − 2 with step 3 on B1, compare with the direct count.
   - **Tests T1w, T1e, T3s** (fix R2): the per-family closure tests of the step-3b table.
   - **Statistic:** z = ln(N_obs / N_pred) / √(1/N_obs + σ²_ln,pred), σ_ln,pred from the event bootstrap. **Pass: |z| < 2.**
   - **Trend test** (fix R2): T1 is evaluated at every rung with ≥ 10 B1 counts, not only r₁. The slope of ln(N_obs/N_pred)
     vs rung index must be compatible with zero at 2σ. If it is not, the slope extrapolated to the WP rung is added to σ_ln
     (and to the central value if the trend is anti-conservative).
   - **Factorisation/independence test:** on B1 loose candidates, the measured joint probability of the extra requirement in
     pairs and triples of layers vs the product of the single-layer conditionals, in three bins of the event's road-hit count
     (local density). The correlation factor c = joint/product (max over bins and pairs) multiplies the step-3 estimate if any
     c is > 1 at 2σ. The SR-T time independence test (§2.3) is part of the same gate.
   - **Pre-registered failure path (no model shopping; split by direction in fix R2, review R2 §5):**
     - *Anti-conservative failure* (z > +2: the prediction is too low). The only allowed remedy is more statistics in a
       pre-declared step (+50 % B1 or B2, at most twice; each step is a separate ≲ 1-day run approved by the user, §6.2).
       If it still fails, B_PU = the **upper envelope** of {thinning,
       power law, factorisation} × N_obs/N_pred of the failed test, with σ_ln enlarged to cover the spread.
     - *Conservative failure* (z < −2: the prediction is too high, as in the pilot). No extra statistics: a stable
       conservative bias does not shrink with N. B_PU = the thinning value, uncorrected, with |ln(N_obs/N_pred)| added in
       quadrature to σ_ln. The bias is reported, and the WP rule (§2.5) is applied with that B. The cost is efficiency, not
       validity.

     - *|z| < 2 but a significant trend* (trend test above): the slope extrapolated to the WP rung is added to σ_ln. If
       the trend is anti-conservative, it is also applied to the central value; if it is conservative, it enters σ_ln only.

     In all cases, if the WP is then infeasible, the fallback deliverable applies (§2.6) and the user is told.
   - **Tests of different families pointing in different directions** (review R3 C-7). Each family's test governs its
     own rungs: T1 the counting rungs, T1w the width and χ²_core rungs, T1e the dE/dx rungs, T3s/T3 the h/o rungs. Each
     applies its own branch. Because the ladder is cumulative, the corrections compound along it: a rung inherits the
     correction factors and σ_ln terms of every family below it. For example, a conservative T1 (σ_ln enlarged) and an
     anti-conservative T1w (central value × N_obs/N_pred) both apply at every width, χ²_core, 2S and F1 rung. A
     correction is never cancelled against another family's opposite correction.
5. **Result:** P_fake(WP) = the thinning estimate (step 2) when T1 (and T2) pass, else the item-4 failure value. Its σ_ln
   combines the bootstrap error, the spread to the power law and the factorisation estimate (model spread), and the density
   normalisation uncertainty of §1.4 (evaluated by re-running the thinning with the top-up at its lower and upper values,
   TT-level, no new simulation).

**Fix-R1 pilot of steps 1-2 (VERIFIED, small statistics; Fatras-only PU, W_c = 75 mm, t_tol = 30 µm; `f1r_summary.json` →
`closure_rho2_to_rho1_t0`).** Direct ρ = 1: 56 events × 4 roads. ρ = 2: 8 trials from 8 pairs of the same events (cost-limited,
§2.4). Expected number of passing candidates per trial (any candidate, N_IT2 ≥ 3, no χ² cut):

| rung | direct ρ = 1 | thinned from ρ = 2 | thinning factor ⟨Σw⟩/N(ρ = 2) | direct / predicted | k_min at ρ = 2 (10/50/90 %) |
|---|---|---|---|---|---|
| N_L2 ≥ 6 | 215 ± 9 | 606 ± 85 | 0.053 | 0.35 | 10 / 12 / 14 |
| N_L2 ≥ 7 | 37 ± 2 | 91 ± 15 | 0.021 | 0.41 | 12 / 14 / 16 |
| N_L2 ≥ 8 | 3.5 ± 0.3 | 7.5 ± 1.4 | 0.0077 | 0.47 | 13 / 16 / 19 |
| N_L2 ≥ 9 | 0.15 ± 0.03 | 0.31 ± 0.07 | 0.0030 | 0.48 | 15 / 18 / 21 |
| N_L2 = 10 | 0 (of 224) | 0.005 ± 0.002 | 0.0029 | — | 16 / 18 / 22 |

Reading:
- The estimator follows the rung dependence over 2.5 decades of thinning (lever arm 1.3-2.5 decades). It **over-predicts by a
  stable ×2.1-2.9** (conservative), with no fitted exponent.
- The PU candidates need k ≈ 10-22 interactions: they are combinatorial, as constructive B-1 expected.
- At these statistics the pre-registered T1 (|z| < 2) would **fail** (z ≈ −3.8 at N_L2 ≥ 8; review R2 recomputes −4.0).
- **Only partly explained (review R2 C-3).** Duplicate counting is real: at ρ = 2 the same physical hit set is found as
  several candidates whose normals differ by > 2 mrad, and the union bound counts each. Review R2's re-run
  (`review_r2/r2_dupcheck_summary.json`; 32 ρ = 1 trials, only 2 ρ = 2 trials) shows that de-duplicating per distinct hit
  set at both densities removes ≈ ×1.3-1.4 of the ×2.1-2.4 at N_L2 ≥ 7-9, moving direct/predicted to ≈ 0.57-0.64. **A
  residual over-prediction of ≈ ×1.6-1.8 remains, and its cause is not known.** Candidates that the pilot cannot separate:
  - T_seed acts differently at ρ = 2;
  - the plane is not refitted after thinning;
  - the union bound;
  - the 8 ρ = 2 trials are pairs of the same 16 events used at ρ = 1;
  - the k model itself.

  R1's sentence "it is not the k model" was an untested assertion and is withdrawn.
- Design change before the freeze (G2): candidates are counted per **distinct passing hit set** (candidates sharing ≥ 50 %
  of their in-band hits are one candidate), at every ρ alike.
- **How the closure gate decides on the residual.** No closure is claimed from this pilot, and no cause is assumed. At G3,
  T1 and the trend test (step 4) are run with the per-hit-set convention on 2 000 B1 and 500 ρ = 2 events, and the gate
  decides:
  - |z| < 2 and no trend → thinning nominal;
  - z < −2 (the residual persists, conservative) → the conservative-failure branch: thinning uncorrected, with
    |ln(N_obs/N_pred)| ≈ 0.5-0.6 added to σ_ln;
  - z > +2 or an anti-conservative trend → the anti-conservative branch.

  G3 also records the stored hit sets of the ρ = 2 candidates, so that the listed causes can be tested (T_seed(ρ),
  refit-after-thinning on a subsample). A cause found that way may be cited, but it cannot change the branch already
  taken without a logged re-review.

**Statistical independence and reuse:**
- PU events are **not stored**. They are regenerated from seeds, so a "library" costs nothing and every PU-only event uses a
  fresh draw.
- For the **signal overlays**, the PU event of a physics row is fixed by hash(spin|m|row) (the mass and spin are in the hash,
  because row indices repeat across mass files; critical C-13), so the same PU sits under that row at every Λ.
- **Row-major A2 (constructive B-4, adopted in fix R1 as a cost reduction inside D4-1 (a)).** One job = one physics row:
  Pythia PU + Fatras + digitisation + CKF **once**, then a loop over the row's Λ points in the TT env: the Stage-3 quirk
  hits are smeared in numpy with the same digitisation configuration (Gaussian smearing with `doMerge = False` is exactly
  per-hit and independent of the PU, VERIFIED by the exact counts of p2), appended to the PU measurements, merged at analysis
  level (U-5 b), and passed to the finder. The Λ comparison is then exactly paired (same PU hits, same CKF output, same
  smearing seed). The quirk hits do not go through ACTS CKF in this mode, so (i) numpy vs ACTS smearing and (ii) the CKF
  stealing fraction (V4-6) are measured on the full-chain A5 subset; any point with V4-6 > 5 % reverts to the full chain.
  Fix-R1 probe: the signal overlays of the margin study were built this way (`f1r_finder.py`, mode `sig`).
- Different masses use different rows and different PU.
- Every Λ point's efficiency shares rows and PU with its neighbours, so the edge fits use a **row-level bootstrap applied
  jointly across Λ**, not independent binomial errors (critical C-9; §5).
- The density-ladder superpositions draw disjoint seed ranges.
- The PU-only seeds are disjoint from all signal seeds (a seed prefix per sample).

### 4.2 SM processes that could fake a coplanar, non-helical pattern

| Source | Mechanism | In Pythia + Fatras? | Handle | Estimate method |
|---|---|---|---|---|
| In-time low-pT loopers (PU) | repeated crossings, 2 hits per layer from one particle | **yes** (pT > 50 MeV, pMin 30 MeV) | road, helix (circle in rφ), z = const plane only from Δz ≲ 0.1 mm vertices | in the PU-only sample (§4.1) |
| Out-of-time loopers (12 BX) | the same, not in time with the PV | **no** | hit time (in-time window), road | TDR density top-up (§1.4, nominal) and its looper-pair variant; the SR-T time factor is measured with an out-of-time BTL overlay |
| Photon conversions (beam pipe, IT) | e⁺e⁻ pair from a point on a line through the PV, so **exactly coplanar with the PV** in the straight-line limit [1708.02243 Sec.III.D] | **yes** (Fatras `emPhotonConversion`; photons kept in PU and hard scatter) | F1 non-helicity, monotonic opening, missing inner hits, N_IT2 | rate in PU-only + SM samples; P(fake \| conversion) from a dedicated photon gun (pT 0.5-50 GeV, from the PV into the road, no PU, 10⁵ events, cheap), then folded with the Pythia photon spectrum in the road |
| K⁰_S, Λ (V0) | two prongs from a displaced point on a line through the PV: also coplanar with the PV | **yes** (Pythia decays, tau0Max 1000 mm) | as conversions, plus the opening angle | same: in-sample, plus a K⁰_S/Λ gun |
| Nuclear interactions in material | multi-prong vertices at r ≥ 22 mm | **no** (no hadronic physics in the pyacts Fatras) | missing hits at r < r_NI (without PU, N_IT2 ≥ 3 removes r_NI ≥ 61.5 mm; at the normalised density random L1/L2 crossings largely undo this, fix R2); F1 helix with a free origin; opening linearity; dE/dx; timing | toy for r_NI ∈ {beam pipe 22 mm, TBPX L1 30 mm, L2 61.5 mm} (rates below); PDG λ_I from `s4geo.py`; prong multiplicity from the literature (UNVERIFIED) |
| Decays in flight (π±, K± → μν kinks) | parent + daughter: a line through the PV plus a line from a point on it, so coplanar with the PV | **no** (Fatras does no decays; a Pythia decay would remove the parent's hits) | 1 hit per layer, so N_IT2/N_OT2 fail; F1 helix per segment | hit-level toy: Fatras parent hits truncated at a sampled decay radius plus a Fatras daughter from the kink point (two particles injected through the same Python reader); kaon rate from Pythia |
| Two prompt tracks (W→τν 3-prong, lost lepton + track, UE) | any two lines through the PV are coplanar with it (S-2 R2-B4) | **yes** | CKF removal (both are helices), f_CKF, F1 non-helicity (PV and free origin), F1 opening linearity | Pythia8 W(ℓν)+j (ℓ = e, μ, τ, τ forced hadronic in one subsample), Z(νν)+j, tt̄ (1ℓ) with truth MET > 200 GeV, + PU 200 |
| Cosmic muons | a straight line through the detector; legs on opposite sides | **no** | road (one leg only), d₀/z₀ to the PV, timing (the top leg is early, the bottom late, ±3.6 ns at the BTL); a muon-system veto **only** after its signal efficiency is shown (status-1 quirks may reach the muon stations; critical C-8) | argument: in-time cosmic rate × 25 ns × the d₀ < 1 mm acceptance; the CMS cosmic rate is to be cited (UNVERIFIED); expected ≪ 0.1 events |
| Beam halo | a line parallel to z at fixed r | **no** | no barrel IT pairs, (x, y) constant across discs, time ordering along z, the CMS halo filter | argument; negligible |
| Merged quirk-like objects | (signal regime, not background) | — | — | out of the F0 scope (§2.1) |

- **Statistics for the SM samples:** 5 × 10³ events each (Z(νν)+j, W(eν), W(μν), W(τν)+j, tt̄ 1ℓ), Pythia8 LO with truth
  MET > 200 GeV, each with PU 200. The direct reach is ≈ 6 × 10⁻⁴ while each sample needs P ≲ 10⁻⁸ (a 4-5 decade
  extrapolation; critical B-8). **Pre-registered, as §4.1 (depth mechanism corrected in fix R5, review R5 B-1):**
  - *Tagging.* Candidates are tagged by whether ≥ 1 in-band hit comes from the hard-scatter vertex (truth). Candidates
    made only of PU belong to B_PU and are not double-counted.
  - *Depth: rung factorisation only.* These samples exist only at ρ = 1, so k-thinning gives no depth: thinning a ρ = 1
    sample yields densities < 1, not deeper rungs at ρ = 1, and T1 is not applicable. Hard-scatter-involving candidates
    are therefore extrapolated by the rung-to-rung factorisation of §4.1 step 3:
    - it starts from the deepest rung with ≥ 10 such candidates in the sample;
    - each conditional is measured on the tightest population with ≥ 10 entries;
    - on that sample: the factorisation/independence test (correlation factor c, §4.1 step 4), T3 where the counts
      allow (r₁ predicted from r₁ − 2), and the T3 failure path;
    - zero counts follow §2.5 item 4a.
  - *Thinning here* is at most a k-decomposition diagnostic.
- **Correlated (k = 1) topologies, measured explicitly (constructive B-5, adopted in C′):** (a) a **PV pair gun**: two charged
  pions from the PV with the Pythia UE (pT, Δφ, Δη) pair spectrum into the road, 10⁵ events without PU and 500 with PU (C′ below); (b) a
  **looper gun**: π/e with pT 50-700 MeV, |η| < 0.3, from z_PV + Δz, Δz ~ U(−0.5, 0.5) mm, 10⁵ events. B_corr = Σ_topology
  (rate per event in the road from Pythia, generator level) × P(pass | topology).
- **C′ is production (fix R4, review R4 B-1).** The guns and toys give P(pass | t) for terms of the WP rule's B sum
  (§2.5 item 4), so they are physics inputs of the final result and run inside campaign C1 under the one-day cap (§6.2),
  not as development. Two parts, both pre-defined now:
  - *C′₀, no PU:* γ, K⁰_S/Λ, PV-pair and looper guns, 10⁵ events each; the NI toy, 3 × 10⁴ per r_NI; the DIF toy, 5 × 10⁴.
    A no-PU event carries ≤ 6 particles and ≤ 50 hits, so its cost is ≈ 0.02 s plus the per-job geometry build, with no
    material t₁ dependence. **≈ 12 CPU-h flat** (ESTIMATE; review R3's S-cap value). It measures the topology-only
    rejection of h, o and dE/dx. Zero counts follow §2.5 item 4a: the reach is 1.14/M, with M the measuring population
    (≈ 1.1 × 10⁻⁵ at M = 10⁵ for the guns). For NI and DIF these factors are measured on the preselected C′₀ events only
    (below), so the reach is 1.14/N_pre: ≈ 8 × 10⁻⁵-6 × 10⁻⁴ at r_NI = 22 mm, ≈ 4 × 10⁻⁵-1.3 × 10⁻⁴ for the NI kinks
    (30 / 61.5 mm) and ≈ 2.5 × 10⁻⁵-7.6 × 10⁻⁵ for DIF (1.14/(5 × 10⁴ × 0.3-0.9)) (ESTIMATE, N_pre below; fix R6,
    review R6 C-1; DIF split in fix R7, review R7 C-3; `fix_r6/f6r_numbers.json`, `review_r7/r7_checks.json`).
  - *C′_PU, with PU:* **8 topologies × 500 events = 4 000 events**: γ, K⁰_S/Λ, PV pair, looper, NI at r_NI = 22 / 30 /
    61.5 mm, DIF. Each event is a TDR-normalised PU-200 event plus the gun or toy particles, aimed into one road. The cost
    is that of an SM event, **4 000 × (4.7 + t₁) s = 7.4 / 8.6 / 10.8 / 14.1 CPU-h at t₁ = 2 / 3 / 5 / 8 s**. It
    measures the PU-assisted pass probability at the counting, χ²_core and width rungs: random crossings refill the
    missing inner hits of NI, DIF and conversions (§4.2 NI bullet).
  - *NI and DIF with PU: preselected toy events (fix R5, review R5 B-1).* Without preselection the 500 NI events per r_NI
    would give only 0.15-2.5 expected two-prong passes even at the loosest counting rung (review R5; f₂ × P(coplanar)
    per NI). The NI (× 3 r_NI) and DIF with-PU samples therefore overlay on PU **only toy events that pass a
    preselection**. The preselection is evaluated on the no-PU C′₀ event, and the same toy event is then overlaid on a PU
    event.
    - *Overlay (fix R6, review R6 B-1).* The toy's hits in the with-PU event are exactly its C′₀ hits:
      - **the stored C′₀ simulated toy hits (Fatras SimHits, with their multiple scattering and energy loss) are inserted
        into the PU event, as the signal injection does; the toy is not re-simulated in the PU job**;
      - digitisation is smearing with doMerge = False (§1.5), and smearing and hit efficiency are drawn from the toy's
        own seed, so the measurements are identical too;
      - **the PV is the same smeared PV draw in both**: it is drawn once from the toy event's seed in C′₀, stored, and
        passed to the with-PU event as its PV (the PU interactions do not move it);
      - **pre-CKF, pre-merge (fix R7, review R7 C-1):** the preselection uses **all** stored toy measurements, before
        the CKF removal of §1.6 and before the analysis-level merging of §1.5 (U-5 b), because both can act differently on
        the toy hits in the with-PU event (toy-PU merges, PU-dependent CKF tracks). The V4-10 per-event hash is taken on these pre-merge,
        pre-CKF toy measurements, and the attribution below tests each toy-linked core hit at its stored C′₀ position
        and σ (via the truth link), not at its merged position. Whatever CKF removal and merging do to the toy hits in the
        with-PU event is part of P(pass | preselected, PU), which is measured; f_pre stays exact.
    - *Preselection (PU-independent).* Some triple of toy hits in 3 distinct layers, with hits from ≥ 2 distinct toy
      particles, satisfies χ²₃ = λ_min(Σ_h u_h u_hᵀ/σ̂_h²) ≤ 48 about the stored PV, i.e. the three hits are compatible
      with one plane through the PV within ±4σ̂_h each. The test is exhaustive over triples (≤ 2 × 10⁴ per event, cheap).
      **σ̂_h is an n-independent per-hit tolerance (fix R6, review R6 B-1)**:
      σ̂_h² = σ²_loc,max,h + t_tol² + (δn_max · |u_h|)², where σ_loc,max,h is the larger of the hit's two local errors
      (the largest σ_n(n, hit) over all normals n; for 2S hits the σ along the strip, as before), t_tol = 30 µm (§2.2)
      and **δn_max = 2 mrad** (the candidate-merge tolerance of §2.2: two planes within 2 mrad are one candidate).
      Because σ_tot has no δn term (δn = 0, §2.2 step 3; fix R8, review R8 B-1) and σ_n(n, hit) ≤ σ_loc,max,h,
      σ̂_h ≥ σ_tot,h(n) for every candidate normal n and **every candidate**; the δn_max·|u_h| term is extra margin of
      the preselection and the attribution only. No σ_PV term is needed, because both
      steps use the same PV draw. A looser preselection costs nothing: N_pre only grows, and at most 500 events are
      overlaid.
    - *Why the weight is exact.* Every candidate counted for NI/DIF passes the attribution rule below (≥ 3 core toy hits
      in ≥ 3 layers from ≥ 2 toy particles, each within ±4σ̂_h of the candidate's PV plane), so it contains a triple with
      χ²₃ ≤ 3 × 16 about that plane, hence λ_min ≤ 48 with the same σ̂_h, the same PV and the same hits. The
      preselection is therefore a necessary condition, and P(pass ∧ not preselected) = 0 by construction. This uses
      only σ̂_h, the stored PV and the stored toy hits, never σ_tot, so it holds for any δn in σ_tot (review R8): f_pre
      is exact under the nominal δn = 0 and under the capped-δn variation alike.
      Then **P(pass at r | t) = f_pre,t × P(pass at r | preselected t, PU)**, where f_pre,t is measured on the full C′₀
      sample of that topology (3 × 10⁴ per r_NI, 5 × 10⁴ DIF), with its own Poisson σ_ln.
    - *Necessity check (gate V4-10, zero cost; fix R6, review R6 B-1).* The finder and the attribution run on **every**
      C′₀ event anyway (h/o/dE/dx). Per NI/DIF topology, the number of attributed candidates (any rung) in
      **non-preselected** C′₀ events must be **exactly 0**. It is reported next to f_pre. A non-zero count is a bug (in
      the preselection, the attribution, σ̂_h or the PV/hit hand-over): that topology's C′_PU events are not run, or not
      used, until it is fixed and the check passes on the full C′₀ sample. If it cannot be fixed inside C1, the weight
      becomes f_pre,t × (1 + N_leak/N_attr,pre), with N_leak and N_attr,pre the attributed C′₀ candidates in non-preselected
      and preselected events at the loosest counting rung, |ln(1 + N_leak/N_attr,pre)| is added in quadrature to its σ_ln,
      the term is flagged in the B table, and the user is told. No other remedy is allowed.
    - *Configurations the preselection removes.* Toy events whose only in-plane toy content is a single line (one prong,
      ≤ 1 crossing per layer) are single-track-plus-random-crossing configurations. These are the configurations every
      one of the ≈ 3.5 × 10³ in-road PU charged tracks forms in B1. NI and DIF add a few % to that track count (≈ 26 NIs per event × a few prongs), so they
      are covered by B_PU and its density-normalisation σ_ln (§1.4; ratios ×1.5-5).
    - *Sampling.* If a topology has N_pre ≥ 500 preselected events, the first 500 by event index are overlaid. If
      N_pre < 500, each preselected event is overlaid on ⌈500/N_pre⌉ independent PU events, and σ_ln comes from a
      two-level bootstrap (toy events, then PU events). If N_pre = 0, f_pre enters under §2.5 item 4a, the conditional is
      set to 1, and that topology's 500 with-PU events are not run (the cost only decreases).
    - *Expected counts with this design (ESTIMATE; `data/acts_stage4/fix_r5/f5r_cprime_counts.py` →
      `f5r_cprime_counts.json`).* Inputs are the plan's own factors and the §2.1 random-crossing table, with a
      half-density variant because the PS μ_c are upper bounds:

      | topology | f_pre | N_pre in C′₀ | overlays per preselected event | expected passes in 500: R0 = (N_IT2 ≥ 3, N_IP2 ≥ 4) | N_IP2 ≥ 6 | N_IP2 ≥ 7 |
      |---|---|---|---|---|---|---|
      | NI at r_NI = 22 mm (the parent leaves no hit; **dominated by prong A's line + one near-vertex prong-B hit**, fix R6) | ≈ 0.07-0.5 (lower bound: σ̂_h only loosens it) | ≈ 2 × 10³-1.5 × 10⁴ | 1 | ≈ the kink row: 250-440 | 30-180 | 3-40 |
      | kinks: DIF, and NI at r_NI = 30 / 61.5 mm (parent hits + one prong, coplanar with the PV by construction, as a DIF) | 0.3-0.9 | 9 × 10³-2.7 × 10⁴ (NI), 1.5-4.5 × 10⁴ (DIF) | 1 | 250-440 | 30-180 | 3-40 |

      *22 mm row corrected in fix R6 (review R6 C-1; ESTIMATE, `review_r6/r6_checks.json` → `NI22_line_plus_vertex_hit`,
      `fix_r6/f6r_numbers.json`).* Fix R5 counted only full two-prong coplanarity (f_pre 4 × 10⁻⁴-7 × 10⁻³, N_pre 12-200,
      70-410 at N_IP2 ≥ 7). But prong A's line and the PV always span a plane containing the NI vertex, and a prong-B hit
      on TBPX L1, ≈ 8 mm from the vertex, lies within 4σ of it whenever |θ⊥(B)| ≲ 0.017-0.03 rad (per-hit 4σ to the
      full χ²₃ budget). With f₂ = 0.3-0.5 and a 0.1-0.3 rad prong spread this gives f_pre ≈ 0.07-0.5, so the
      preselected 22 mm population is mostly "line + one near-vertex hit" and its counting-rung rates look like the
      kink row. The σ̂_h of B-1 can only raise every f_pre in this table (capped at 1). The two-prong coplanar events are a
      sub-population of it. Such candidates are attributed to B_NI (conservative).
      Every NI/DIF sample therefore has O(10²) counts at the loose counting rungs and ≥ 10 down to N_IP2 ≥ 6. That is
      enough for T3 inside the counting family and for the loose χ²_core and width conditionals. No estimate is made for
      the width and χ²_core pass fractions of toy + PU: they are measured.
    - *Note on the §4.2 NI estimate (extended to every r_NI in fix R6, review R6 C-1).* The ESTIMATE below counts only the
      full two-prong coplanar path. It is **not an upper bound at any r_NI**: at r_NI ≥ 30 mm the kink path (the parent's
      TBPX hits + one prong) is coplanar with the PV by construction, and at r_NI = 22 mm the line + near-vertex-hit path
      above dominates. With the C′ factors (PV-line factor 0.22, a conservative upper value (fix R7), f_pre, the R0 pass fraction of the kink row), the
      attributable NI rate at R0 is ≈ 0.6-3.1 per event from the kinks (30 / 61.5 mm) plus ≈ 0.06-0.5 from 22 mm, i.e.
      **≈ 0.6-3.6 per event, 1.3-3.3 decades above the 2 × 10⁻³-3 × 10⁻² of the estimate below** (ESTIMATE;
      `review_r6/r6_checks.json` → `NI_rate_at_R0_per_event`). C′ measures all paths.
  - *Depth for every C′_PU topology (corrected in fix R5, review R5 B-1).* C′_PU exists only at ρ = 1. Thinning its PU
    interactions gives densities < 1, not deeper rungs, so **it is not a depth mechanism**, and T1 is not applicable. It
    is at most a k-decomposition diagnostic. Depth comes from:
    - the rung-to-rung factorisation of §4.1 step 3 on the C′_PU sample, from the deepest rung with ≥ 10 counts, with
      the conditionals measured on populations with ≥ 10 entries, the factorisation/independence test (§4.1 step 4) and T3
      on that sample;
    - h, o and dE/dx factorised at ρ = 1 from C′₀ (topology-only rejection; the §4.1 method table), measured on the
      C′₀ events that pass the same preselection (NI/DIF) or on all C′₀ candidates (guns).

    Zero counts follow §2.5 item 4a.
  - *Attribution (fix R5, review R5 C-1).* A with-PU candidate counts for topology t only if:
    - **≥ 3 of its core hits, in ≥ 3 distinct layers (≥ 1 of them IT + PS), come from the gun/toy particles**, each
      within ±4σ̂_h of the candidate's PV plane (σ̂_h: the n-independent tolerance of the preselection above, ≥ σ_tot,h
      for every candidate, since σ_tot has no δn term; fix R6, review R6 B-1; fix R8, review R8 B-1), each tested at
      its stored C′₀ position and σ (C-1 of review R7, overlay above). A measurement that the U-5 b merging formed from a
      toy hit and a PU (or second toy) hit is tested at each of its toy-linked stored C′₀ positions, never at its merged
      position; each toy link counts as a hit of its own particle only if that link's own stored position passes (it is
      never credited to the other particles of the merged measurement); this cannot leak, since the preselection uses all
      stored toy measurements (review R8 C-2; wording per review R9 C-2);
    - and those hits come from **≥ 2 distinct gun/toy particles**. For the one-particle looper gun, the condition is
      instead ≥ 2 crossings by the looper in ≥ 1 layer.

    Candidates with fewer gun/toy hits are single-line-plus-PU or pure-PU configurations, and belong to B_PU (see above).
    R4's "≥ 1 in-band hit" admitted pure-PU candidates (≈ 1.1 × 10⁵ per trial) that contain one incidental gun hit. A
    random plane picks up three hits of the gun/toy lines in three layers only if it nearly contains them. The rule is
    applied identically to the C′₀ candidates. Using σ̂_h instead of the candidate's σ_tot (fix R6) only loosens the
    attribution for **every** candidate (σ_tot has no δn term, fix R8), i.e. the attributed set is a superset of R5's
    and more candidates count for t, which is conservative (a candidate also present in B1 is then counted twice). The
    R6 diagnostic for δn > δn_max is removed: σ_tot has no δn term (fix R8; under the capped-δn variation δn ≤ δn_max). *Note (review R7 C-4):* σ̂_h's δn_max·|u| term
    widens attribution to ≈ ±8 mrad seen from the PV, so some pure-PU candidates that pick up ≥ 3 toy hits from ≥ 2
    particles are attributed to t as well as counted in B_PU; this double counting is conservative and negligible
    (≈ rate_NI × 0.22 × f_pre × O(10⁻³) × P_PU ≪ P_PU).
  - *Sizes and the review R4 quote.* A with-PU part of 10⁴ (10⁵) events would cost 19-41 (186-408) CPU-h at
    t₁ = 2-10 s; 500 per topology is the size that fits C1 under the cap and the deadline (unchanged in fix R5: the
    preselection changes which toy events are overlaid, not how many). If a gun topology (γ, V0, PV pair, looper; not
    preselected, coplanar with the PV by construction) shows < 10 passes in 500 at the loosest counting rung, its depth
    starts from the C′₀ factors under item 4a. The +50 % step of §4.1 can be offered as a separate run approved by the user.
- **Nuclear interactions: ESTIMATE before production (critical B-8).** In-road charged hadrons per PU-200 event that cross
  r ≈ 22-62 mm: ≈ 3.5 × 10³ (TBPX L1 Fatras crossings 6.7 × 10³/event × the road fraction ≈ 0.58 at W_c = 75 mm). With x/λ_I
  ≈ 1.9 × 10⁻³ (Be beam pipe: 0.23 % X₀ × 352.8 mm / 421.0 mm) and ≈ 2.4 × 10⁻³ per TBPX layer (1.2 % X₀ Si-equivalent:
  1.124 mm / 465.2 mm; X₀, λ_I from `s4geo.py`), × ⟨cosh η⟩ ≈ 1.2: **≈ 8 (beam pipe), ≈ 10 (L1), ≈ 8 (L2) NIs per event in
  the road** (ESTIMATE). Factors, all ESTIMATE (corrected in fix R2, review R2 C-4):
  - f₂ = fraction of NIs with ≥ 2 charged prongs that reach the OT ≈ 0.3-0.5 (prong multiplicity from the literature,
    UNVERIFIED);
  - P(≥ 2 prongs coplanar with the PV-NI line within the band) ≈ 10⁻³-10⁻², from σ_n/lever arm ≈ 2 × 10⁻⁴ rad against a
    0.1-0.3 rad prong spread;
  - P(parent vertex on the PV line) ≈ 0.22, for a PU vertex within ±0.1 mm. This is the **per-event** probability that
    some PU vertex coincides with the PV (`CRITICAL_REVIEW_S4PLAN_R1.md` l.117, B-4 (a): 200/(2√π σ_z) = 1.254 mm⁻¹,
    λ = 0.251, 1 − e^−λ = 0.222), used here as a **conservative upper value** of the per-NI fraction whose parent comes
    from the PV line (fix R7, review R7 C-2). The per-NI fraction is ≈ 0.006-0.014 (≈ (1 + 0.25)/201 vertices, up to
    ×2.3 for a 0.1 mm/|n_z| tolerance; review R7 `PV_line`, ESTIMATE), so 0.22 overstates B_NI by ≈ ×15-35
    (≈ 1.2-1.5 decades). It is kept, not replaced, because the per-NI value rests on treating the HS as a PU vertex in
    the road and on an orientation average, neither validated.

  Hence P(NI fake) ≈ 26 × 0.22 × f₂ × (10⁻³-10⁻²) ≈ **2 × 10⁻³-3 × 10⁻² per event before F1**, i.e. ~10⁻³-10⁻². R1 said
  10⁻⁴-10⁻³, which did not follow from its own factors. That is 6-7 decades above the target, **but this two-prong
  estimate is not an upper bound** (fix R6, review R6 C-1; C′ note above): with the kink and line + near-vertex-hit paths
  the attributable rate at R0 is ≈ 0.6-3.6 per event, **≈ 8-9 decades above the ≲ 3 × 10⁻⁹ per event target (≈ 9-10
  under the strict B₈₄ rule's ≲ 3 × 10⁻¹⁰)** (ESTIMATE, `fix_r6/f6r_numbers.json`). NI is the most signal-like
  source Fatras lacks, and F1's free-origin helix, the opening-linearity test, dE/dx, timing and the missing inner hits
  must carry it. **Missing inner hits:** without PU, an NI at r_NI ≥ 61.5 mm (TBPX L2) fails N_IT2 ≥ 3, because its prongs
  cross only L3 and L4 and the parent gives one crossing on L1 and L2. At the normalised density, however, L1/L2 bands
  hold ≥ 2 random crossings with P ≈ 1.0/0.8 (§2.1). This protection is therefore largely lost, and the NI toy is run with
  PU overlaid. The R1 statement "N_IT2 kills r_NI > 6 cm, not the beam pipe or TBPX L1/L2" was wrong for L2 without PU
  and too optimistic with PU. The toy measures
  P(pass | NI at r_NI) per r_NI, as f_pre × P(pass | preselected, PU) (C′ bullet above, fix R5). **The NI toy places the
  parent's origin at the event's true PV** (the vertex whose smeared draw is the stored PV of the C′ bullet), so
  P(pass | r_NI) is conditional on a parent from the PV line, and the PV-line factor is explicit (fix R6, review R6 C-4):
  **B_NI = Σ_r_NI (NIs per event at r_NI) × P_PV-line × P(pass | r_NI) × N_trig, with P_PV-line ≈ 0.22** (the factor
  above, ESTIMATE; a conservative upper value, ≈ ×15-35 above the per-NI fraction 0.006-0.014, fix R7, review R7 C-2;
  varied with the PV-line tolerance in the NI σ_ln). The "8-9 decades" NI statements carry the same conservative
  factor.
- **Decays in flight (DIF):** the hit-level toy (Fatras parent truncated at a sampled decay radius + a Fatras daughter from
  the kink); B_DIF = (in-road π/K decays per event in the tracker, from Pythia with the Lorentz-boosted decay lengths) ×
  P(pass | kink) × N_trig, with P(pass | kink) = f_pre × P(pass | preselected, PU) (C′ bullet above, fix R5). The DIF toy
  also starts its parent at the true PV; B_DIF takes no PV-line factor (factor 1, conservative; fix R6 neighbourhood
  check of C-4).
- **Full B sum used by the WP rule** (§2.5 item 4): B = N_trig × [P_PU + P_SM,HS + Σ_t rate_t × P(pass | t)] + B_cosmic + B_halo,
  with t ∈ {conversion, V0, NI(r_NI), DIF, PV pair, looper}; rate_t per triggered event in the road from Pythia (generator
  level, unlimited statistics) and P(pass | t) from the guns/toys; each term log-normal (§2.5). For NI and DIF,
  P(pass at r | t) = f_pre,t × P(pass at r | preselected t, PU). For every t, the rungs below the deepest one with ≥ 10
  counts come from rung factorisation and the C′₀ h/o/dE/dx factors (C′ bullet above). Every factor of every term
  (P_PU, P_SM,HS, f_pre, the conditionals) follows the zero- and low-count rule of §2.5 item 4a (fix R5). The conversion and V0 guns
  of C′ are normalised the same way. Terms already present in B1 (in-time conversions, V0s, loopers) are counted once:
  B1 candidates whose in-band hits come from one interaction (k = 1) are assigned to B_PU, and the gun terms cover the
  hard-scatter and PV-vertex topologies only.
- **Missing samples** (minor, critical B-8): tt̄ 2ℓ, single top and WW/WZ/ZZ enter through N_presel only (their fakes are
  prompt tracks, as W/Z+jets); they are added to N_trig with Pythia cross sections, without their own hit-level samples.
- Normalisation: Pythia σ × K-factor (UNVERIFIED NNLO/LO ≈ 1.2-1.4, cited at implementation) with a ±30 % nuisance (ESTIMATE).
- **Delphes adds nothing** here: it has no hit-level tracker, and the MET, jet and veto modelling of §3 is a parametrisation
  either way. **No Delphes install is proposed.**
- **Nuclear interactions and decays in flight could only be simulated** with Geant4 (ACTS Geant4 plugin) or a source build of
  ACTS with Fatras hadronic parametrisations. Neither is in the wheel, and both mean a large install (INSTALL_CHECK R3: 1-3 h
  build, ~2 GB). **Recommendation: do not install.** Use the toys and arguments above (user decision D4-7).

---

## 5. Grid and statistics

All events are unweighted (w = w_max per event, N_eff = N; Stage-3 HANDOVER §3). Stage-3 toys are never used for working
points. The counting set is `in_eta25 & status == 1` (VERIFIED counts from `data/sim_stage3/summary/events_p2.npz`).

| Block | Points | Events | PU | Purpose |
|---|---|---|---|---|
| A1 signal-only (no PU) | all 307 p2 + 60 mv | 148 011 + ≈ 14 700 (all η, both halves) | no | V4-3 truth-only finder efficiency vs the Stage-3 edges; detector-level P2 observables without PU |
| **A2 signal + PU 200, templates** | all 307 p2 (14 E masses × 16-20 Λ, Ẽ 200/500/1000) | **61 344** (≈ 3.4 × 10³ unique rows, row-major, §4.1) | yes (one PU per row, all Λ) | ε(m, Λ), detector-level edges, P2 observables with PU, yields |
| A3 signal + PU 200, toys | 50 points: 7 measured E masses (200/300/500/700/1000/1200/1500) × Λ {0.45, 0.6, 1, 2, 5, 10} keV, plus E1000/1200 × {15, 20, 30, 40} keV | ≈ 9 000 (row-major) | yes | P2 pseudo-experiments (template ↔ toy swap where both exist), coverage |
| A4 material ×0.5/×2 | the 60 mv points (E 200/500/1000/1500, Ẽ 500 × {0.4, 0.6, 1, 3, 10, 20} keV) | 12 000 (row-major per scale) | yes, Fatras at the same material scale | material systematic on ε, edges and P2 observables |
| A5 systematics subset | 20 points (4 masses × 5 Λ) with road-hit dumps incl. truth positions | 4 000 | yes | **full chain** (quirk hits through ACTS digitisation + CKF): validates the row-major numpy smearing and measures V4-6; TT-level variations without re-simulation (resolution, merging, time window, hit efficiency, PV, MET, t_tol, density top-up); PU 140 rerun |
| B1 PU-only direct | — | 2 × 10⁴ events × 4 roads (+ road-hit dumps for 2 000 events) | yes (TDR-normalised) | §4.1 step 1 |
| B2 PU density ladder | — | 5 000 at ρ = 2 (2 roads); 2 000 at ρ = 3 (1 road) **only as the optional campaign C5** (§4.1 step 2, G2c) | ρ superposed normalised PU-200 events | §4.1 step 2 (thinning) |
| C SM + PU | Z(νν)+j, W(eν)+j, W(μν)+j, W(τν)+j, tt̄ (1ℓ) | 5 000 each | yes | §4.2 |
| C′ guns and toys (production, in C1; fix R4) | γ, K⁰_S/Λ (0.5-50 GeV into the road); kink (DIF) and NI toys at r_NI ∈ {22, 30, 61.5 mm}; **PV pair gun, looper gun** (k = 1, constructive B-5) | C′₀: ≈ 5.4 × 10⁵ without PU (guns 10⁵ each, NI 3 × 3 × 10⁴, DIF 5 × 10⁴); C′_PU: **8 topologies × 500 = 4 000 with PU** (§4.2; NI and DIF: preselected toy events, weighted by f_pre from C′₀; fix R5) | C′₀ no; C′_PU yes | P(fake \| topology) |

- **Campaigns (fix R3).** The table is the full recommended scope (D4-1 (a)). It is produced as the pre-defined one-day
  campaigns of §6.2:
  - **C1:** A1; A2 on E200/500/1000/1500 + Ẽ500 × Λ ∈ {0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0} keV (8 000 events,
    1 000 rows); A5 on 5 points; B1 5 000; B2 1 000; C Z(νν)+j, W(τν)+j, tt̄ 1ℓ × 2 000; C′₀ and C′_PU (4 000);
  - **C2:** B1 → 12 000, B2 → 3 000, C → all five samples × 5 000;
  - **C3:** B1 → 2 × 10⁴, B2 → 5 000;
  - **C4:** the rest of A2 (all 307 points), A3, A4, A5 → 20 points + PU 140 (C4′ = C4 without A3 and A4, a
    deadline variant, §11);
  - **C′ (guns and toys) is production and part of C1** (fix R4, review R4 B-1: it feeds the B sum); C5 (ρ = 3) is
    optional and deferred under the deadline.

  Seed ranges are disjoint across campaigns, so the samples of later campaigns simply add. Under the deadline (fix R4)
  only the §11 decision-table row for the measured t₁ is produced; the table above stays the full-scope reference.
- **P1 at detector level: no** (decision D4-9). P1 is a truth-level statement about B-crossing physics. The event-level
  out-of-plane resolution s_eff ≈ 23-30 µm equals the MS floor (synthesis S-2), so detector-level Δs carries no P1 information
  beyond what S-2 already says. The only P1-related Stage-4 task is the U-2 panel (§9), which is truth level.
- **Merged regime:** A2 includes the 15-40 keV points so that the efficiency drop from analysis-level merging is *measured*,
  not assumed. Merged-pair coverage tests use only E1000/1200 (U-3 a).
- **Errors:** with 200 template events per point, a 50 % efficiency is ±3.5 % (binomial). Because every Λ point of a mass
  shares rows **and** PU, the detector-level edges (logistic in ln Λ per mass, smoothed in ln m as in Stage 3,
  `edge_fits_in_m`) take their errors from a **row-level bootstrap applied jointly across Λ** (critical C-9).
- **Plane-thickness and window acceptance** (V4-3): ε is reported vs W_c (50/75/100/150 mm) and t_tol (0/30/100 µm) on A1
  (no PU) so that any shift of the low edge is attributed to W_c/t_tol separately from resolution and merging (critical B-3).
- **Hit-time window** (constructive C-4): ε(Δt_acc) is reported as a curve (12.5, 25, 50 ns) at E1000/1500; at E1500 only
  26-30 % of counting-set events have a BTL hit within 1-25 ns. The OT/BTL readout-window assumptions are UNVERIFIED.

---

## 6. Compute

### 6.1 Per-event cost (Mac M3, one thread)

| Step | VERIFIED (probe) | Production ESTIMATE |
|---|---|---|
| PU generation (Pythia 1.07 ms × 200) + transport | 0.2 s + 4.6 s (Python HepMC3) | 0.2 + 0.2 s (direct `SimParticle` reader; gate G1) |
| Fatras + injection + digitisation (32 sectors) | 0.8-1.2 s | 1.1 s |
| Seeding + CKF (pT > 0.9 GeV, 32 sectors) | 2.0-3.9 s | 3.0 s |
| Output (Python loop over measurements) | 0.9 s | 0.2 s (vectorised) |
| Finder, per road trial | 5-10 s (R0 prototype); fix-R1 prototype §2.4; **fix R2: 211 s at the normalised IT + OT density with the merge vectorised (≈ 5 500 s as coded)** | no fixed target: G2a measures t₁ and the user chooses the scope (§6.2; reference: ≤ 5.6 s for four one-day Mac campaigns, ≤ 7.0 s for C1 with C′; deadline target ≈ 3 s, §11); ESTIMATE after the §6.2 routes 5-20 s |
| **Signal + PU event (1 trial)** | ≈ 12-17 s | **≈ 7 s** full chain; **≈ 2.1 s per extra Λ** in row-major mode |
| **PU-only event (4 trials)** | ≈ 30-45 s | **≈ 13 s** |
| Signal-only event (no PU) | ≈ 0.02 s plus ≈ 10 s per job (geometry build) | negligible |

Peak memory 670 MB per worker (VERIFIED), so 7 workers use ≈ 5 GB of the 24 GB.

### 6.2 Totals and production campaigns (ESTIMATE; recomputed in fix R1; conditioned on the finder speed in fix R2; split into one-day campaigns in fix R3)

Per-event inputs: PU event (generation, Fatras, digitisation, CKF, output) ≈ 4.7 s; finder t₁ s/trial at the normalised
density (the block table below is evaluated at t₁ = 2 s and t₂ = 16 s at ρ = 2, as a reference); numpy quirk smearing +
merging ≈ 0.1 s per (row, Λ). Row-major A2-A4 (§4.1) simulate each row's PU once. **The full scope is never run as one
job:** under the user's cap it is produced as the one-day campaigns defined below, and the totals depend on t₁, t₂.

| Block | CPU-h (recommended) | CPU-h (lean) | Basis (recommended) | Lean scope |
|---|---|---|---|---|
| A1 | 2 | 2 | as R0 | same |
| A2 | **40** (R0 120) | 24 | 3.4 × 10³ rows × 4.7 s + 61 344 × 2.1 s | 7 measured E masses + Ẽ (≈ 36 000 events) |
| A3 | **7** (R0 18) | 4 | ≈ 1.4 × 10³ rows × 4.7 s + 9 000 × 2.1 s | 30 points |
| A4 | **10** (R0 23) | 4 | ≈ 2 000 rows (5 species-masses × 2 scales × 200) × 4.7 s + 12 000 × 2.1 s | E 500/1000 only |
| A5 (+ PU 140) | 30 | 15 | full chain, as R0 | 10 points |
| B1 | 72 | 36 | 2 × 10⁴ × (4.7 + 4 × 2) s | 10⁴ events |
| B2 | **58** (+ 38 for the optional C5, ρ = 3) (R0 90) | 29 | ρ = 2: 5 000 × (2 × 4.7 + 2 × 16) s (finder ∝ ρ³); ρ = 3: 2 000 × (3 × 4.7 + 54) s | ρ = 2, 2 500 events |
| C + C′ | **67** (R0 55) | 34 | C 2.5 × 10⁴ × (4.7 + 2) s ≈ 47; C′₀ ≈ 12 (no PU) + C′_PU 4 000 × (4.7 + 2) s ≈ 7 (fix R4, §4.2) | 3 samples × 3 000 + guns |
| validation + debugging | 40 | 10 | as R0 | — |
| **Total** | **≈ 330 (≈ 365 with C5)** | **≈ 160** | R0: ≈ 450 / ≈ 210 | |

The lean column is kept as the R1-R2 record only. It is **superseded** (review R4 C-6): the minimal option is the
campaign C1 (§6.2 below, D4-1 (m)), and every scope the user can choose is a set of the pre-defined campaigns.

- **Wall time on the Mac** (7 workers, low priority) at t₁ = 2 s: ≈ 47 h for the whole recommended scope, which exceeds
  the one-day cap. It is therefore split into campaigns (below), each ≲ 24 h.
- **Cost vs finder speed of the whole scope (fix R2, review R2 B-5; `probes/f2r_cost.py` → `fix_r2/f2r_cost.json`;
  reference only, superseded for planning by the campaign table).** The finder trials are
  ≈ 1.91 × 10⁵ at ρ = 1 (A2 61 344, A3 9 000, A4 12 000, A5 4 000, B1 8 × 10⁴, C 2.5 × 10⁴) and 10⁴ at ρ = 2 (B2). The
  non-finder base is ≈ 179 CPU-h. Recommended ≈ 179 + 53 t₁ + 2.8 t₂ CPU-h; lean ≈ 84 + 27 t₁ + 1.4 t₂; optional ρ = 3
  (C5): + 2 000 × (14.1 + t₃) s with t₃ ≈ 3.4 t₂ (finder ∝ ρ³). C1-C4 (below) sum to ≈ 315 CPU-h at t₁ = 2 s, against
  ≈ 330 here: validation is 30 instead of 40 CPU-h, A5 is 32 instead of 30, and the block total (326) is rounded up. The
  C′ guns and toys (≈ 19 CPU-h at t₁ = 2 s) are inside C1 since fix R4 (review R4 B-1).

  | t₁ (ρ = 1, s/trial) | t₂ (ρ = 2, s/trial) | recommended | lean | G3 pilot (2 000 B1 + 500 ρ = 2 events) |
  |---|---|---|---|---|
  | 2 | 16 | ≈ 330 | ≈ 160 | ≈ 13 |
  | 2 | 50 | ≈ 420 | ≈ 210 | — |
  | 4 | 32 | ≈ 480 | ≈ 240 | ≈ 18 (t₂ = 20) |
  | 5 | 40 / 200 | ≈ 560 / ≈ 1 000 | ≈ 270 / ≈ 500 | — |
  | 10 | 80 / 500 | ≈ 930 / ≈ 2 100 | ≈ 460 / ≈ 1 050 | — |
  | 20 | 160 | ≈ 1 690 | ≈ 850 | — |
  | 48 (fix-R1, OT-only top-up) | 1 000 | ≈ 5 500 | ≈ 2 800 | ≈ 390 |
  | **211 (fix R2, full density, merge vectorised)** | 1 700 (ρ³; not measured) | ≈ 16 000 | ≈ 8 100 | — |

  The R1 sentence "at the R0 prototype speed (8 s/trial) the recommended scope would be ≈ 840 CPU-h" is replaced by this
  table. The relevant measured speed is 211 s/trial at the adopted density.
- **Speed and the cap:** from the measured 211 s, ×30 (to 7.0 s) makes the minimal campaign C1 (with C′, fix R4) fit
  one Mac day, and ×38 (to 5.6 s) makes every campaign of the full scope fit one Mac day. Under the deadline the target
  is t₁ ≈ 3 s (×70; §11 decision table). No ρ = 2 time has been measured at the normalised density (no ρ = 2 run in
  fix R2); G2b measures it.
- **Speed-up routes** (each an ESTIMATE; factors refer to the full-density profile of §2.4):
  1. *Hash-grid duplicate merge:* quantise normals into 2 mrad cells and compare with the neighbouring cells only, O(N).
     Merge 33 s → < 1 s. (The vectorised O(N²) version is measured: 5 500 s → 33 s.)
  2. *Hit indexing by (φ, z) per layer for the seed score:* the ±3σ band of a PV plane crosses a cylinder along a thin
     curve z(φ), so a binned index visits ~10² hits per seed instead of ≈ 4 × 10⁴ road hits. Seeding 95 s → 2-5 s (×20-50).
  3. *Fewer refits:* seed score on N_IP2 (IT + PS), which does not saturate the way L1/L2 and 2S do, with T_seed(ρ) from
     the PU-only stability rule (§2.2 item 4), plus clustering of seed planes before the refit. Numba + numpy refits
     82 s → 4-16 s (×5-20).
  4. *Numpy refit → numba, and stored variables only for candidates passing the loosest rung:* a further ×2-5 on the
     remaining refit time.
  5. *Early termination:* stop the seed-score scan when the remaining layers cannot reach T_seed (×1.5-2 on seeding).
  6. *Vectorised thinning weights* (DP or importance sampling, §4.1 step 3b) for ρ = 2: 12 ms → ≲ 1-2 ms per set.

  Combined ESTIMATE: 211 s → ≈ 5-20 s/trial at ρ = 1. **2 s is not supported by this estimate.** The realistic
  recommended cost is ≈ 560-1 700 CPU-h, with B2 at t₂ = 8 t₁ included (review R3 C-4). Under the cap
  that is 4 one-day runs at 5 s and ≈ 12 at 20 s (Mac only; campaign table below). Under the deadline only the sets of
  the §11 decision table run.
- **Production campaigns under the one-day cap (fix R3, review R3 B-1; C′ added to C1 and Mac only in fix R4, review R4
  B-1; `probes/f4r_deadline.py` → `fix_r4/f4r_deadline.json`, which reuses the block costs of `probes/f3r_campaigns.py`).**
  - *Capacity per 24 h of wall time:* Mac 7 workers ≈ 168 CPU-h (Mac-M3 units; the user quotes 170-200). The Mac is the
    only machine (user decision 2026-10-13; §6.5).
  - *Contents (fixed now, frozen with `WP_RULE.md`; seed ranges disjoint, so later campaigns add to earlier ones):*
    - **C1 core (self-contained; the minimal option).** A1 (all, no PU); A2 on E200/500/1000/1500 + Ẽ500 × Λ ∈ {0.45, 0.6,
      0.85, 1.0, 1.5, 2.0, 3.0, 5.0} keV, 200 events each (8 000, 1 000 rows); A5 on 5 points (1 000 events, full chain);
      B1 5 000 × 4 roads; B2 1 000 ρ = 2 × 2 roads; C Z(νν)+j, W(τν)+j, tt̄ 1ℓ × 2 000; **C′₀ (no PU, ≈ 12 CPU-h) and
      C′_PU (8 topologies × 500 events with PU, 4 000 × (4.7 + t₁) s; §4.2)**; validation 15 CPU-h. It is review R3's
      S-cap with the k = 1 guns put back (review R4 B-1). Pre-defined sub-runs if C1 exceeds one day: **C1a** = A1, A2,
      A5, C′ (one day up to t₁ ≈ 36 s) and **C1b** = B1, B2, C (one day up to t₁ ≈ 12.3 s).
    - **C2 backgrounds I:** B1 +7 000 (→ 12 000); B2 +2 000 (→ 3 000); C → all five samples × 5 000 (+19 000); 5 CPU-h
      validation. Pre-defined sub-runs: **C2-B** = the B1 and B2 parts (the PU reach) and **C2-C** = the SM part.
    - **C3 backgrounds II:** B1 +8 000 (→ 2 × 10⁴); B2 +2 000 (→ 5 000); 5 CPU-h validation.
    - **C4 grid and systematics:** the rest of A2 (all 307 points; 53 344 more events, 2 400 rows); A3; A4; A5 → 20 points
      + the PU-140 rerun; 5 CPU-h validation. **C4′** = C4 without A3 and A4 (the deadline variant; A3 and A4 can follow
      as their own run).
    - **C5 (optional, only under the T3 rule of §4.1 step 2, behind G2c):** ρ = 3, 2 000 events × 1 road. Deferred under
      the deadline.
    - **C1r, reduced C1 (deadline fallback only, §11):** A1; A2 core at 100 events per point (4 000 events); A5 on 3 points;
      B1 2 500; B2 500; C 3 × 1 000; C′₀ and C′_PU at 250 per topology; validation 10 CPU-h. One Mac day up to
      t₁ ≈ 16.5 s. Its thinning reach is ≈ 10⁻⁹ per trial, so the background-free claim rests almost entirely on rung
      factorisation and T3.
  - *Cost per campaign (CPU-h; t₂ = 8 t₁ until G2b; Mac wall in h in brackets):*

    | t₁ (s) | C1 (with C′) | C2 | C3 | C4 | C4′ | C5 | C1-C4 | one-day runs (Mac) |
    |---|---|---|---|---|---|---|---|---|
    | 2 | 91 (13) | 88 (13) | 56 (8) | 80 (11) | 63 (9) | 38 (5) | 315 | 4 |
    | 3 | 107 (15) | 110 (16) | 74 (11) | 101 (14) | 79 (11) | 53 (8) | 392 | 4 |
    | 4 | 122 (17) | 132 (19) | 92 (13) | 123 (18) | 94 (14) | 68 (10) | 468 | 4 |
    | 5 | 137 (20) | 154 (22) | 110 (16) | 144 (21) | 110 (16) | 83 (12) | 545 | 4 |
    | 6 | 152 (22) | 176 (**25**) | 127 (18) | 166 (24) | 126 (18) | 98 (14) | 621 | 5 |
    | 8 | 183 (**26**) | 220 (**31**) | 163 (23) | 209 (**30**) | 157 (22) | 128 (18) | 774 | 7 |
    | 10 | 214 (**30**) | 264 (**38**) | 198 (**28**) | 252 (**36**) | 188 (**27**) | 158 (23) | 927 | 8 |
    | 15 | 290 (**41**) | 373 (**53**) | 287 (**41**) | 359 (**51**) | 266 (**38**) | 233 (**33**) | 1 310 | 10 |
    | 20 | 366 (**52**) | 483 (**69**) | 376 (**54**) | 466 (**67**) | 345 (**49**) | 308 (**44**) | 1 692 | 12 |

    Bold = over 24 h. C2-C5 are unchanged from fix R3; C1 includes C′ (+ 12 + 4 000 × (4.7 + t₁) s = 19-39 CPU-h at
    t₁ = 2-20 s). **Largest t₁ for one Mac day:** C1 7.0 s (8.7 s before C′ was added); C2 5.6 s; C3 8.2 s; C4 6.1 s;
    C4′ 8.7 s; C5 10.6 s; C1r 16.5 s.
  - *A campaign over one day at the measured speed* is split into its pre-defined sub-runs above, else first along its
    block boundaries and then by halving a block's seed range. Each sub-run is a separate run, ≲ 1 day, approved by the
    user. The table's last column counts these runs.
  - **PU-extrapolation reach of the minimal option (C1 alone).** B2 has 2 × 10³ ρ = 2 trials, so k_min = 20 candidates
    probe ⟨Σw⟩ ≈ 5 × 10⁻¹⁰ per trial. That is above the per-category requirement P_PU ≲ 3 × 10⁻¹⁰ (§2.6, split 0.11), so
    with C1 alone the deepest rungs rest on the rung factorisation of §4.1 step 3, with its own closure test, and not on
    direct thinning. B1 has 2 × 10⁴ trials (direct zero-count reach 1.5 × 10⁻⁴ per trial).
    - After C2 (or C2-B): 1.6 × 10⁻¹⁰ (6.3 × 10⁻⁵ direct).
    - After C3: 10⁻¹⁰ (3.7 × 10⁻⁵ direct), i.e. the recommended scope's reach.

    C1 also gives up the edges in ln m from 14 masses (it has 5), the A3 toy coverage, the A4 material variation and two of
    the five SM samples. Those come in C2 and C4.
  - **Not capped but reported** (user decision): G1 ≈ 2 CPU-h; G2 ≈ 6 + development; the G3 pilot ≈ 13 / 17 / 26 / 39
    CPU-h at t₁ = 2 / 3 / 5 / 8 s (2 000 B1 + 500 ρ = 2 events); G2c ≈ 1-3 CPU-h if C5 is ever considered. Each is logged
    with its CPU-h and wall time. In total ≈ 21 / 25 / 34 CPU-h (3.0 / 3.6 / 4.9 h of Mac wall) at t₁ = 2 / 3 / 5 s.
    C′ is no longer in this list (it is production, in C1).
- **Gates (fix R3; detail in §11).**
  - **G2a** (ρ = 1, full normalised density, median of ≥ 20 PU-only trials, 1 thread) reports t₁, the campaign table
    evaluated at it (`f4r_deadline.py` with the measured t₁) and the §11 decision-table row. It **always** stops for the
    user's scope choice: which campaigns, in which order, or more optimisation first, or stop. No outcome of G2a starts
    production.
  - **G2b** (ρ = 2, ≥ 10 trials incl. the in-job weights) has one criterion: t₂ ≤ **t₂,max**, the largest t₂ at which
    every campaign the user chose still fits ≲ 1 Mac day **and** the chosen set still fits the production window of the
    §11 schedule. t₂,max is computed from the measured t₁ and written into the G2a report. Examples
    (`f4r_deadline.json` → `g2b_t2max_C1`, `g2b_t2max_rows`): C1 alone 135 s at t₁ = 3 s and 96 s at t₁ = 5 s; the
    §11 decision-table rows 21 s at t₁ = 2 s (all of C1-C4; 27 s without A3 and A4, 68 s without C3 as well), 44 s at
    t₁ = 3 s (C1 + C2 + C4′) and 53 s at t₁ = 5 s (C1 + C2). If the measured t₂ exceeds the row's t₂,max, the row is
    trimmed from its end in the deferral order before the user is asked.
    - Pass → G3 (development).
    - Fail → the user is asked: fewer B2 events in that campaign (the reach loss is stated), splitting the campaign, more
      ρ = 2 optimisation, or no B2 beyond C1.
  - **G2c** (only if C5 is offered): ≥ 5 ρ = 3 trials. C5 must fit ≲ 1 day at the measured t₃; else the user is asked.
  - Production campaigns start only on the user's explicit approval, one campaign (or sub-run) at a time.
- **B2 is the most uncertain block.** It uses integer superpositions only. The 58 CPU-h assume t₂ = 16 s. The
  unoptimised fix-R1 probe took 400-1300 s per ρ = 2 trial at **Fatras** density (review R2 re-run: 146 s and 571 s).
  About 46 % of that is the O(N²) merge and ≈ 26 % the per-candidate thinning Monte Carlo (§2.4). At the normalised
  density the candidate count per trial is ~10× larger already at ρ = 1 (§2.4), so t₂ is unknown until G2b.
- **Fix-R1 probe compute: ≈ 5.5 CPU-h on the Mac** (7 workers, nice). That is over the ≲ 3 CPU-h asked for this round. It
  breaks down into ≈ 2.2 CPU-h for the 8 ρ = 2 trials (much slower than expected), ≈ 1 CPU-h for two discarded first passes
  (a seed-axis window and a 5 mm 2S pre-filter that dropped real quirk hits), ≈ 0.3 CPU-h of PU generation, and the rest for
  the ρ = 1, TDR-OT and signal runs.
- **Fix-R2 probe compute: ≈ 0.22 CPU-h** (1 thread, nice; ρ = 1 PU-only trials only, no ρ = 2, no signal): 3 full-density
  trials (0.17 CPU-h), 5 + 5 TDR-OT trials (one superseded set), and arithmetic.

### 6.3 Disk (ESTIMATE)

| Item | Size |
|---|---|
| compact per-event output for signal + PU (candidates, hits in the candidate bands, signal truth): ≈ 12 kB × 82 000 | 1.0 GB |
| A5 road-hit dumps with truth positions (≈ 0.85 MB × 4 000) | 3.4 GB |
| B1 road-hit dumps for 2 000 events (critical C-10; ≈ 0.85 MB each) | 1.7 GB |
| PU-only and density-ladder summaries (weights) | 0.2 GB |
| ρ = 2 hit-record samples (§4.1 step 3b, review R3 C-2): (a) ≤ 200 sets/trial ≈ 4 GB + (b) 1 % of the loose sets ≥ 20 GB, at the full B2 (≈ 5 GB with C1 alone) | ≈ 24 GB |
| SM + guns | 0.4 GB |
| validation full dumps (300 events × 2.7 MB, VERIFIED size) | 0.8 GB |
| **Total** | **≈ 32 GB** at the full scope, ≈ 10 GB with C1 alone (134 GB free) |

PU events are never stored; they are regenerated from seeds (§4.1).

### 6.4 The Windows PC (no probe run on the PC)

- **Native Windows: not possible.** `pyacts` 48.0.0 ships only `macosx_26_0_arm64` and `manylinux_2_34_x86_64` wheels (PyPI,
  VERIFIED), and conda-forge has no win-64 ACTS.
- **WSL2 (Ubuntu 24.04, glibc 2.39 ≥ 2.34) should work** with the manylinux wheel plus conda-forge linux-64 pythia8 and pyhepmc
  (ESTIMATE, untested).
  - Cost: enabling WSL2 (admin rights, a reboot), ≈ 1.5 GB for Ubuntu, ≈ 0.7 GB for the env, ≈ ½ day of setup and bundle work,
    and a cross-machine check (V4-8, ≈ 2 CPU-h).
  - Results will **not** be bit-identical to the Mac (different compiler and libm; Fatras and Pythia floating point). Equivalence
    is therefore statistical (KS and median pulls on 3 overlap jobs), unlike Stage 3's bit-identical kernel.
- The **finder** (TT env, numba) runs natively on win-64, but it needs the per-event outputs from the ACTS stage, so splitting
  ACTS (Mac) and finder (PC) work only shifts I/O.
- **Benefit:** 10 more workers at roughly M3-core speed (ESTIMATE). That is ≈ 17 Mac-equivalent workers in total, so the
  whole recommended scope at t₁ = 2 s would take ≈ 330/17 ≈ 20 h of wall time instead of ≈ 47 h on the Mac alone (R2's
  "≈ 70 h → ≈ 30 h" used the R2 t₁ = 4 s row; review R3 B-1).
- **Status (fix R4):** the user's resource list for Stage 4 is the Mac only (2026-10-13); the PC is not in it. This
  subsection is kept for reference only. If the PC is ever used, whole blocks go to one machine and V4-8 statistical
  equivalence applies.

### 6.5 Cloud execution (withdrawn in fix R4)

A Google Cloud free-trial VM was considered in fix R3 (account terms, VM type, linux-64 locks, validation, ≈ $31-120 of
the $300 credit) and **dropped by the user on 2026-10-13: Stage 4 runs on the Mac only**. No account, project, VM or lock
file was ever created. The R3 content is summarised in `review/FIX_S4PLAN_R3.md`, and its arithmetic stays in
`fix_r3/f3r_campaigns.json`.

---

## 7. Systematics

**New in Stage 4** (each gets: origin → method → impact → interpretation in the Stage-4 note):

| Source | Variation | Method | Acts on |
|---|---|---|---|
| Material | ×0.5 / ×2 (all layers; UNVERIFIED baseline) | A4 (Stage-3 `mv` hits + Fatras at the same scale); B1 subset of 5 000 at each scale | ε, edges, P2 observables, P_fake |
| Hit resolution | IT tkLayout parametrised (optimistic) / binary (baseline) / binary × 1.3; PS, 2S ± 20 % | A5 TT-level re-smearing from the stored truth positions | ε, t_est, sep_IT^det |
| Long-coordinate model | Gaussian vs uniform (PS/2S) | A5 | ε, P_fake (2S bands) |
| Merging threshold (U-5 b) | 1 vs 2 pitches | A5 + all merged-regime points (TT level on A2 outputs) | merging edge, ε at ≥ 10 keV |
| Channelised clustering | later cross-check at 3 points (U-5) | `doClusterization` with a geometric config | merging edge |
| PU level | 140 / 200 (+ density ladder ρ) | A5 PU-140 rerun; B2 | ε, P_fake |
| PU density normalisation (out-of-time PU, missing secondaries; V4-2) | top-up ratios at their lower / upper ends (IT cluster size 3 / 1.5 px; OT cluster size ±0.2, reading ±5 %); Fatras-only as a cross-check; independent vs looper-pair (k = 1) top-up | TT-level re-run of the thinning on B1/B2 and of A5 (no new simulation) | P_fake, ε |
| Plane-thickness tolerance and window | t_tol 0 / 30 / 100 µm; W_c 50 / 75 / 100 mm (reported, W_c not varied in the result) | A5 + B1 subset, TT level | ε, P_fake |
| Beam-spot σ_z | 35 / 45 / 55 mm | B1 subset (2 000 each); signal PU overlay at A5 | P_fake (vertex line density near the PV) |
| Hit-time window | 25 / 12.5 ns | TT level on A2 | ε (heavy, slow pairs) |
| Hit efficiency and module gaps | 99 % / 97 % | TT level | ε, N_IT2 |
| CKF | minPt 0.9 / 0.5 GeV | A5 + B1 subset | ε (stealing), P_fake |
| PV | resolution × 2; PV-ID 93 / 90 % | TT level | ε |
| MET | σ⊥ 15 / 25 / 35 GeV | TT level; δ₉₅ recomputed by the rule | ε, P_fake |
| Trigger turn-on | T₅₀ ± 25 GeV (until CMS-TDR-021 is cited) | Stage-2 truth reweight | ε_trig |
| Disc φ approximation | rings split (only if the endcap matters at the gate) | rerun A5 endcap points | endcap ε |
| PU-fake extrapolation model | k-thinning (nominal) vs power law vs rung factorisation; failure-path envelope if a closure test fails (§4.1 step 4) | the spread, in log space | B_PU |
| SM normalisation | K-factor ± 30 % | — | B_SM |

**Carried from Stages 2 and 3:**
- σ_norm ± 5 %.
- Tail rate +12…+15 / −11…−13 %.
- ℓ_max ± 5 % (`w_lmax_*`) and QED −1.1 ± 0.8 % one-sided (`w_qed`).
- Scale, PDF and merging (`wvar_ratio`).
- Status-4 losses ≤ 1.5 % per point (one-sided at the merging edge).
- The Stage-3 robust shifts, which are noise-limited upper bounds. HANDOVER §5.4 defers their symmetrisation and < 2σ
  treatment to Stage 4 (decision D4-10). All of these enter as per-event weights on the Stage-4 efficiencies (paired,
  bootstrap-averaged as in Stage 3).
- **Treatment of the robust shifts — revision (a′) of D4-10 (critical B-9; approved by the user 2026-10-13).** The approved
  D4-10 (a) reads "symmetrise to max(|up|, |down|); keep shifts below 2× their sampling sd as noise-limited bounds at 1×
  sampling sd". In its plain reading the second clause *reduces* a 1.0-1.99σ shift (by up to ×2), is discontinuous at 2σ
  and applies to the common case (198/243 components are below 2 sd, HANDOVER §5.4). Proposed rule (a′):
  1. two-sided sources (ℓ_max tilt, scale, PDF, merging scale): symmetrise to max(|up|, |down|); physically one-sided
     sources stay one-sided (QED −1.1 ± 0.8 %, status-4 losses, the analysis-level merging threshold);
  2. evaluate each **family** with its own prescription on paired weights: PDF replicas → one PDF uncertainty (the CT18
     prescription on the replica shifts), scale → the envelope of the scale variations, then the family enters once (no
     quadrature sum of ~100 noise-limited components, which grows like √N);
  3. smooth each family's shift across Λ (and ln m) with the same functional form as the edges, so template noise averages
     out instead of accumulating;
  4. noise floor: the assigned uncertainty is max(|smoothed shift|, sd), never smaller than the measured shift. Here sd
     is the **raw per-point sampling sd of the unsmoothed shift** (the Stage-3 bootstrap sd at that (m, Λ), e.g. 0.94 % in
     the example below), not the smaller sd of the smoothed curve, so smoothing cannot lower the floor (wording fixed in
     fix R2, review R2 C-7);
  5. worked example (E1000, lower edge ℓ_max = R_IT, `sim/stage3/results/P2.json` → `systematics.F_m1000.robust_shifts`):
     ℓ_max tilt up +1.82 % (sd 0.94 %, 1.9σ), down −1.30 % (sd 0.85 %, 1.5σ). D4-10 (a) plain reading: both < 2σ → 0.94 % /
     0.85 %. (a′): symmetric max(1.82, 1.30) = 1.82 %, floor max(1.82, 0.94) = 1.82 % before smoothing; the smoothed value
     across Λ replaces it.
  (a′) is the nominal treatment (user approval 2026-10-13). The plain reading of (a) is computed once as a cross-check
  and reported in the systematics appendix.

---

## 8. Validation (criteria fixed now)

| ID | Test | Criterion | Status from the probes |
|---|---|---|---|
| V4-1 | Ingestion closure, every production job | n_meas = n_SimHits(quirk) + n_SimHits(PU) exactly with `doMerge = False`; every quirk SimHit maps to one measurement; skipped T3V/ETL counts match the file; t ≥ r/c; on surface to 1 µm; `depositedEnergy` = `h_dE` | PASS on 1/10/30 keV × 20 events (signal only) and on the 5-event 3 keV signal + PU run (the only one with a surviving JSON, `p2_summary.json`; the "8"/"13" events of R0 have no record, critical C-4): re-recorded per job at G1 |
| V4-2 | PU density benchmark vs the public CMS Phase-2 Tracker TDR (critical B-7; **done in fix R1**) | Reference: CMS-TDR-014 Fig. 6.3 (PDF p.101): hit occupancy (fraction of channels with a digitized hit) vs η per layer, tt̄ + PU 200, incl. 12 previous + 3 following crossings (§6.2.1, PDF p.100). clusters/cm² = occupancy / channel area / ⟨cluster size⟩; channel areas as simulated in the TDR (§6.2.1: pixel 25 × 100 µm², PS-s 100 µm × 23.13 mm, PS-p 100 µm × 1446 µm, 2S 90 µm × 50.25 mm); OT cluster size from Fig. 12.3 left (PDF p.277): ≈ 1.8 (PS), ≈ 2.2 (2S); IT cluster size **not in the TDR** (1.5-3 px, ESTIMATE). The R0 references were wrong: "3 GHz/cm²" is the RD53 chip specification (TDR Tab. 4.4), and Fig. 12.3 is the OT, not the IT. Criterion: the nominal PU density is **normalised** to this benchmark per layer (top-up, §1.4); the residual (ratio range) is the density systematic | **Fatras in-time / TDR, central (\|η\| < 0.3, 56 events; VERIFIED, `f1r_density_bench.json`; TDR values graphical readings ±5 %):** TBPX L1-L4 14.7 / 4.3 / 1.6 / 0.83 cm⁻² vs 41 / 9.7 / 4.5 / 3.1 (cluster size 2; range ×0.67-1.33) → ratio 2.8 / 2.3 / 2.8 / 3.7; TBPS L1-L3 0.28 / 0.11 / 0.046 vs 0.68-0.74 / 0.35-0.37 / 0.20 (strip and macro-pixel agree) → 2.5-2.7 / 3.2-3.3 / 4.3; TB2S L1-L3 0.021 / 0.010 / 0.005 vs 0.083 / 0.053 / 0.034 → 4.0 / 5.2 / 7.3. **Fatras is low by ×2.3-7**, rising with radius (out-of-time loopers, hadronic secondaries) |
| V4-3 | Finder on truth-only (no PU) events vs the Stage-3 truth edges (runs at G2, **after** `WP_RULE.md` is frozen) | Efficiency vs Λ at every p2 point. The detector-level no-PU edges are compared with (a) N_osc = 1 at 0.28-0.33 keV, (b) median ℓ_max = R_IT at 0.43-0.94 keV, (c) the truth thickness edge at 0.47-0.55 keV and (d) the hit-level merging edge at 12.8-25 keV. Every difference is attributed to one of: W_c (ε vs W_c 50/75/100/150 mm), t_tol (0/30/100 µm), resolution, merging, the finder. Expect ε ≥ 0.9 at 1-5 keV (an expectation, not a cut) | truth-level window study done (`f1r_truth_window.json`); detector level not run |
| V4-4 | Reproducibility and seeds | 20 jobs rerun bit-identical on the same machine; parallel outputs of different seeds are not identical (methodology §7.4: spawn start method); all seeds recorded | not run |
| V4-5 | Independent cross-check of the finder | brute force on 50 signal + PU events and 50 PU-only trials. An exhaustive scan of PV-plane normals (0.2 mrad grid within ±0.3 rad of the F0 normal plus a 5 mrad global scan over the road) maximises the resolution-weighted inlier count. An independent scipy least-squares plane fit on the F0 inliers. Agreement \|Δn\| < 1 mrad in ≥ 95 % of the F0-accepted events; every disagreement is inspected | not run |
| V4-6 | CKF signal stealing | fraction of quirk measurements on CKF tracks, per point (A5 full chain; row-major A2 points revert to the full chain if > 5 %); > 5 % anywhere → investigate (minPt, seed region) | 0/208 quirk measurements in 6 events sharing 3 independent PU events (p3; R0 said 205, critical C-3). The 18 % removal fraction comes from the n32 runs only (`p3_summary_n1.json` has a broken counter) |
| V4-7 | PU-fake extrapolation closure (gate) | §4.1 step 4: T1 (thinning ρ = 2 → 1, lever arm ≥ 1 decade), T2 (ρ = 3 → 2, only if C5 is produced), T3 (rung factorisation), and per family T1w (width/χ²_core), T1e (dE/dx), T3s (F1 recomputed vs factorised), |z| < 2 each; trend test; factorisation-correlation and SR-T time-independence tests; pre-registered failure path split by direction (fix R2) | fix-R1 pilot on 56 Fatras-only events (§4.1 box): demonstration only, small statistics |
| V4-8 | Cross-machine (only if the PC is used) | 3 overlap jobs: KS p > 0.01/n_tests, \|median pull\| < 3 | — |
| V4-9 | Geometry and material | muon gun: 17-hit central pattern, on-surface < 1 µm (PASS, p1/p3 with sectors), **plus a gun aimed at φ-sector boundaries** (n1 vs n32 PU differ by −73…+130 measurements/event, ≤ 0.1 %; critical C-5). Highland check: the Fatras 1 GeV μ scattering angle behind TBPX L1 matches Highland with the decorated x/X₀ within 10 % | partly PASS |
| V4-10 | C′ preselection necessity (gate; fix R6, review R6 B-1) | Per NI/DIF topology, on the full C′₀ sample (no PU, zero extra cost: the finder and attribution run on every C′₀ event anyway): attributed candidates (§4.2 attribution with σ̂_h, any rung) in **non-preselected** events **= 0 exactly**, reported with f_pre. Also checked: the with-PU event's toy measurements, taken before CKF removal and analysis-level merging, and its PV equal the stored C′₀ ones (hash per event on the pre-merge, pre-CKF toy measurements; fix R7, review R7 C-1). Failure: a bug; that topology's C′_PU is not run or not used until fixed and re-checked; if not fixable inside C1, f_pre × (1 + N_leak/N_attr,pre) with \|ln(1 + N_leak/N_attr,pre)\| added to σ_ln, flagged, user told (§4.2) | not run (C1) |

---

## 9. The U-2 B + MS panel (small P1 task, truth level)

- **Data:** `sim/stage3/results/P1.json` → `points.<sp>.by_lambda.<Λ>.B_MS_combination` (34 cells: the median
  Δs_BM/√(Δs_B² + Δs_M²) with its error, and the median Δs_BM/(Δs_B + Δs_M)), plus `B_MS_crossover_keV`. The per-event paired
  values come from the P1 per-event table `data/sim_stage3/summary/events_p1.npz`; the B, M and BM configurations share rows.
- **Panel:**
  - Left: the median ratio to quadrature vs x = Δs_B/Δs_MS (the median per cell), with error bars, for the five species-masses
    (E 200/500/1000/1500, Ẽ 500). Reference lines at 1 (quadrature) and the linear-sum curve.
  - Right: the per-event paired ratio vs Λ/Λ_cross.
  - Reading: sub-quadrature (0.80-0.97) in the crossover region 1-3 keV, and quadrature at 0.45-0.6 keV.
- **Code and output:**
  - `acts/stage4/p1_panel/p1_bms_panel.py` (TT env, matplotlib + mplhep, the JFC plotting rules).
  - `acts/stage4/p1_panel/p1_bms_panel.{pdf,png}` with "Private work (simulation)", plus `p1_bms_panel.json` with the plotted
    numbers.
  - A 5-line text block for P1 (stated as a measured combination; no fitted rule is claimed).
- **Cost:** ≈ 1-2 h, no CPU. It runs first in the implementation turn and does not depend on any ACTS work. Stage 5 restyles it.

---

## 10. Decisions for the user

| # | Decision | Options | Recommendation | Cost | Confidence |
|---|---|---|---|---|---|
| D4-1 | Production scope | Sets of the pre-defined campaigns only (review R4 C-6): **(a) recommended = C1-C4** (§5, §6.2: A2 all 307 points, A3 50 toy points, A4 all mv, C′ in C1); **(d) deadline sets** = the §11 decision-table row at the measured t₁ (C1-C4, tight, at 2 s; C1 + C2 + C4′ at 3 s; C1 + C2 at 5 s; C1 (+ C2-B up to 7 s), C1a/C1b or C1r above 5 s); **(m) minimal = C1 alone** (5 species-masses × 8 Λ, B1 5 000, B2 1 000, 3 SM samples, C′; thinning reach ≈ 5 × 10⁻¹⁰ per trial, deepest rungs by rung factorisation). The R1-R2 options "lean" and "(a) plus all toys" are withdrawn: C1 supersedes lean, and C4 already holds all A3 toys | (a) approved in principle; **the scope is chosen by the user at G2a from the campaign table and the §11 decision table at the measured t₁, always** (user decision 2026-10-13); under the deadline the recommendation is (d); every production run ≲ 1 day of wall time, each approved | ESTIMATE (§6.2, `fix_r4/f4r_deadline.json`): C1-C4 = 315 / 392 / 545 / 774 CPU-h at t₁ = 2 / 3 / 5 / 8 s (t₂ = 8 t₁); 4 one-day runs up to t₁ ≈ 5.6 s. C1 (with C′) alone fits one Mac day up to t₁ ≈ 7.0 s. Measured now: 211 s/trial (merge vectorised); speed-up running, target ≈ 3 s. G2b criterion: t₂ ≤ t₂,max of the user's chosen set (one number, from the G2a report) | medium (cost: low) |
| D4-2 | φ-sectoring of the Stage-3 surfaces (32 sectors; positions unchanged) | yes / no | **yes** (CKF 23-60 → 1.6-3.4 s/event; same surfaces, so U-4 (a) holds) | none | high |
| D4-3 | PU/hard-scatter hit removal | (a) real CKF pT > 0.9 GeV; (b) truth-parametrised removal with the public tracking efficiency (Knapen-like); (c) none | **(a)**, with (b) as a cross-check on A5 | 3 s/event for (a) | medium |
| D4-4 | Finder and working point | F0 + F1 as in §2; WP = loosest rung with B ≤ 0.3 events at +1σ (alternative B ≤ 0.1) | **F0 + F1, B ≤ 0.3** (approved). Fix R1 defines "+1σ" as the 84th percentile of the log-normal total B, on one ordered ladder, with the monotonic guard and the freeze at G2 (§2.5); F1 gains the free-origin helix, the opening-linearity variable (replacing the undefined crossing count), the SR-T/SR-G timing categories and dE/dx — all inside the approved F1. **Fix R2:** a ribbon-width rung family (w_core) and a core-hit χ² in F0 (§2.2, §2.5), per-category ladders with a budget split (§2.5 item 5), and a pre-defined fallback deliverable (§2.6). **Fix R3:** split 0.11 + 0.11 (combined B₈₄ ≤ 0.3 by construction at σ_ln ≤ 2.3; deterministic pair continuation for every branch); p(χ²_core) > 10⁻³ moved to the χ²_core family (23 rungs); fallback with a hypothesis-admissible primary rung per (m, Λ), no per-point best-of (D4-17). The B ≤ 0.3 rule itself is unchanged | — | medium (feasibility: §2.6) |
| D4-5 | PU-only fake-rate method | (a) direct + density ladder + factorisation with the closure gate; (b) direct + factorisation only | **(a)** (approved). Fix R1 implements the density ladder as exact interaction-count thinning (no fitted exponent; the power law kept as the alternative), on TDR-normalised PU, with pre-registered closure tests, a lever-arm minimum and a failure path (§4.1). Fix R2: a per-rung-family method table (per-subset recomputation for counts, width, χ²_core and dE/dx; factorisation at ρ = 1 for h, o and SR-T), per-hit-set counting, the failure path split by direction, and a trend test. Fix R3: counting rungs are pure counts (T1 computable); χ²_core recomputed per subset with a re-centred core from per-hit records; ρ = 3 only as optional C5 (gate G2c) if the rung-factorisation test T3 fails; cross-family corrections compound | B1 + B2: 72 + 58 CPU-h at t₁ = 2 s, t₂ = 16 s for the full scope (§6.2), spread over C1-C3; C5 + 38 | medium (still the weakest point) |
| D4-6 | Merged regime (≳ 15 keV) | (a) measure the finder-efficiency drop only; the HSCP-like merged category later (Stage 5/6 note); (b) build a merged-pair selection now | **(a)** | (b) ≈ +1 week | medium |
| D4-7 | Nuclear interactions and decays in flight | (a) toys + arguments; (b) Geant4 / ACTS source build (large install) | **(a), no install** | (b) 1-3 h build + ~2 GB + integration days | high |
| D4-8 | Machines | (a) Mac only; (b) Mac + a Google Cloud free-trial VM (fix R3, §6.5); (c) WSL2 on the PC | **user decision 2026-10-13: (a) Mac only.** (b) was considered and dropped by the user; (c) is not in the resource list | — | high |
| D4-9 | P1 at detector level | no / yes | **no** (resolution ≈ MS floor; P1 stays truth level; U-2 panel only) | — | high |
| D4-10 | Stage-3 robust-shift treatment (HANDOVER §5.4) | (a) symmetrise to max(\|up\|, \|down\|); keep shifts below 2× their sampling sd as noise-limited bounds at 1× sampling sd; (b) drop shifts below 2σ; **(a′) (fix R1):** two-sided sources max(\|up\|, \|down\|), one-sided stay one-sided; per-family prescriptions (PDF, scale envelope); smoothing across Λ and ln m; floor max(\|shift\|, raw per-point sd), never min (§7, worked example; floor wording fixed in fix R2) | **(a′), approved by the user 2026-10-13** (critical B-9: (a) in its plain reading reduces 1-2σ shifts) | — | medium |
| D4-11 | Trigger numbers | fetch and cite the Phase-2 L1 TDR (CMS-TDR-021, public PDF; no install) | **yes** | minutes | high |
| D4-12 | Endcap seeds in F0 from the start | yes / barrel only first | **yes** (69 % of counting-set events have \|η_pair\| > 1) | +½ day | medium |
| D4-13 (fix R1) | P2 deliverables for m_Q and sensitivity (constructive B-6) | (a) add per-event velocity observables to the templates — MET, η_axis, β_ToF of the first in-band BTL/ETL hit, the dE/dx proxy, M_est = MET·cosh η_axis/(βγ)_ToF (the S-4 recipe; truth-level M_est vs M correlation 0.990-1.000, constructive `r1c_tof_mass.json`) — plus `results/sensitivity.json` and a pyhf counting workspace (95 % CL exclusion and 5σ/3-event discovery in (m, Λ) per SR-T/SR-G, vs FASER/D0/Farina-Low); (b) keep the R0 deliverables (sep_IT^det, t_est) | **(a), approved by the user 2026-10-13** (in scope; the deliverables use the primary selections of §2.6) | ½-1 day, < 1 CPU-h | medium-high |
| D4-14 (fix R1) | Wide regime ℓ_max > R_IT (below the F0 low edge by construction, §2.2) | (a) accept as an analysis limitation now; decide after V4-3 at G2 shows the size of the gap; (b) add a wide-regime topology now (two curved tracks, each coplanar with the PV and the MET plane) | **(a), approved by the user 2026-10-13** (fix R2 note, review R2 §5: if (b) is chosen after V4-3, the new topology is a separate category with its own background-only ladder, frozen in `WP_RULE.md` before its first signal efficiency; the existing ladders are not changed) | (b) ≈ +1 week + its own WP ladder and B1 rerun (≈ +40 CPU-h at t₁ = 2 s, ESTIMATE) | medium |
| D4-15 (fix R1) | PU density baseline (critical B-7; V4-2) | (a) Fatras in-time PU **topped up per layer to the CMS-TDR-014 occupancy** (§1.4) as the baseline, Fatras-only as a cross-check; (b) Fatras-only baseline, top-up as a one-sided systematic | **(a), approved by the user 2026-10-13**: Fatras is low by ×2.3-7 per layer (VERIFIED, `f1r_density_bench.json`), so (b) would under-state B. Cost: ≈ ×40 more refitted seeds per trial than at Fatras density (2 × 10⁵ vs 5 × 10³), hence the speed gates (§2.4, §6.2) | via the finder speed (§6.2) | medium (IT ratio ESTIMATE) |
| **D4-16 (pending: at G2a)** | Scope under the one-day cap and the deadline | which of the pre-defined campaigns, in which order (the §11 decision-table row is the default); or more optimisation first; or stop | none in advance: the user chooses from the campaign table and the §11 decision table at the measured t₁. To remove approval latency, the user may approve the decision-table row in advance at G2a; each campaign is still followed by a short report before the next starts | §6.2 table | — |
| D4-17 | Fallback primary rung (§2.6) | (i) hypothesis-admissible r_fb(m, Λ, c) from the Stage-3 truth Λ_R(m) (smoothed, `P2.json` `edge_fits_in_m`) and βγ_IT(m) (frozen script `f4r_admissibility.py`; no detector-level efficiency, no limit comparison); (ii) R_E everywhere (signal-free, empty at low Λ and E200); (iii) split-template choice | **(i), approved by the user 2026-10-13**; per-point best-of forbidden in all options; limits only at the primary selection | in-job weights for ≤ 20 extra selections (negligible) | medium |

---

## 11. Deliverables and review plan

**Deliverables** (all under `acts/stage4/` and `data/acts_stage4/`):
1. `code/`, `finder/`, `analysis/`, `validation/`, `jobs/` with pixi-free run instructions in `README.md`. The two existing envs
   are unchanged.
2. `WP_RULE.md`, frozen at the start of G2, before any signal efficiency (§2.5 item 9).
3. `results/*.json`, the single source. Each (m, Λ, category) is reported at its pre-declared primary selection: r*_c
   where it exists and is admissible, else the fallback r_fb (§2.6). The fixed-rung outputs and r_fb are produced in every
   case. Results after a partial set of campaigns are labelled with the campaigns used:
   - ε(m, Λ) with its factors (trigger, preselection, PV, fiducial, finder);
   - the detector-level edges vs the truth edges;
   - the P2 observables;
   - P_fake and B_PU with the extrapolation;
   - the SM background table;
   - yields with σ_norm;
   - the systematics table.
4. **P2 observables at detector level:**
   - **sep_IT^det:** per IT layer, the separation of the two in-plane clusters of candidate hits along n₂ (no truth assignment),
     median over layers, with analysis-level merging. Delivered with its calibration vs the Stage-3 truth `sep_IT` (the Λ⁻²
     handle) and the detector-level slope.
   - **t_est and χ²/ndf** with resolution, vs Λ and m, and the range where t_est still tracks Δs_B (above s_eff ≈ 23-30 µm).
   - the robust core width w_core (a rung variable since fix R2, §2.2), also delivered as a ribbon-width (ℓ_max) observable,
     calibrated vs truth like sep_IT.
   - **D4-13 (approved 2026-10-13, in scope):** MET, η_axis, β_ToF, dE/dx and M_est per event, `results/sensitivity.json`
     and the pyhf workspace, all at the primary selections of §2.6 (the fallback limit `results/fallback_limits.json` uses
     the same workspace).
5. `VALIDATION.md` (§0 generated from the JSON), `HANDOVER_STAGE5.md`:
   - per-point yields, efficiencies and backgrounds with uncertainties;
   - per-event detector-level templates for the P2 (m, Λ) measurement (SR-T and SR-G separately);
   - the toy sets;
   - nuisance definitions.
6. The U-2 panel (§9). The internal figures are labelled "Private work (simulation)"; the final plots are Stage 5's.

**Implementation gates, in this order** (fix R1, constructive B-8; speed gates added in fix R2, rewritten for the
one-day cap in fix R3, scheduled for the deadline in fix R4). The two real risks — finder CPU at the normalised density and the extrapolation closure — fail
early. Gate and development runs are **not capped** (user decision) but each is logged with its CPU-h and wall time. The
user is asked where marked, and **always at G2a and before every production run**.
1. **U-2 panel** (§9; no CPU).
2. **G1 (chain, ≈ 2 CPU-h):** production `run_chain.py` with the `SimParticle` PU reader, sectors, vectorised output, the
   TDR top-up (§1.4) and per-job V4-1 records. Target ≤ 5 s per PU event without the finder; V4-1 and V4-9 (incl. the
   sector-boundary gun) pass; a cited IT cluster-size number is searched for (else the ESTIMATE range stays).
3. **G2 (finder, ≈ 6 CPU-h plus development):** `WP_RULE.md` frozen **first** (§2.5 item 9). Then (fix R2, review R2 B-5):
   - **G2a, finder speed (ρ = 1) and the scope choice.** Full TDR-normalised IT + OT density, median of ≥ 20 PU-only
     trials, 1 thread, stored variables included. Measured now: 211 s (§2.4). The G2a report gives t₁, the §6.2
     campaign table evaluated at that t₁, the largest t₁ per campaign, the decision-table row below, and t₂,max for each
     option. **Outcome: always ask the user** (D4-1, D4-16). The options are:
     - the decision-table row for the measured t₁ (the default under the deadline);
     - C1 only (the minimal scope);
     - another sequence of the pre-defined campaigns, each ≲ 1 day, inside the production window;
     - more optimisation first (development, not capped; it comes out of the production window);
     - stop.

     No G2a outcome launches production. Reference speeds: C1 (with C′) fits one Mac day up to t₁ ≈ 7.0 s, and every
     campaign does up to ≈ 5.6 s.

     The speed-ups of §6.2 are CPU optimisations under §2.5 item 9: logged, checked by V4-5 and by the PU-only T_seed
     stability rule, with no signal input.
   - **G2b, ρ = 2 timing gate (before any G3 ρ = 2 event).** Normalised density, median of ≥ 10 superposed trials,
     including the in-job thinning weights for every rung family and the fallback selections (§4.1 step 3b). **One
     criterion** (the same in §6.2 and §10): t₂ ≤ t₂,max from the G2a report, i.e. every campaign the user chose at G2a
     still fits ≲ 1 Mac day at the measured (t₁, t₂) and the chosen set still fits the production window (C1 alone: 135 s
     at t₁ = 3 s, 96 s at t₁ = 5 s; decision-table rows: 21 / 44 / 53 s at t₁ = 2 / 3 / 5 s, and 27 / 68 s for the 2 s
     row trimmed by A3 + A4 / by A3 + A4 + C3).
     - Pass → report and go on to G3.
     - Fail → **ask the user**: fewer B2 events in the affected campaign (the reach loss is stated), splitting it, more
       ρ = 2 optimisation (the sub-sampling strata of §4.1 step 3b included), or no B2 beyond C1.
   - **G2c, ρ = 3 timing gate (only if C5 is offered under the T3 rule of §4.1 step 2).** ≥ 5 ρ = 3 trials. C5 must fit
     ≲ 1 day at the measured t₃; else the user is asked. C5 runs only with the user's approval. Under the deadline C5 is
     deferred in every case, so G2c is not run.
   - V4-5 brute force on 50 events; **all of A1 + V4-3** (ε vs W_c and t_tol).
4. **G3 (pilot, development; ≈ 13 / 17 / 26 / 39 CPU-h at t₁ = 2 / 3 / 5 / 8 s; launched after the user's G2a choice and a
   passed G2b):** B1 2 000 events, B2 500 at ρ = 2. It must show:
   - (i) T1/T1w and the trend test of §4.1 with per-hit-set counting and the lever-arm condition. **The gate decides on the
     unexplained ×1.6-1.8 residual** through the pre-registered branches of §4.1 step 4:
     - |z| < 2 and no trend → nominal;
     - z < −2 → conservative;
     - z > +2 → anti-conservative;
     - |z| < 2 with a significant trend → the trend rule of step 4: the slope is added to σ_ln, and also to the central
       value if the trend is anti-conservative (review R3 C-7).

     Each family's test governs its own rungs, and the corrections compound along the ladder (§4.1 step 4);
   - (ii) the SR-T time-position independence on the loose rungs;
   - (iii) which rungs are reachable at ρ = 2, and hence where the rung factorisation (T3) takes over (§4.1 step 2). C5
     (ρ = 3) is offered only if T3 fails;
   - (iv) the stability of T_seed on every rung family that matters (counting rungs N_IP2/N_2S2, χ²_core, w_core;
     review R2 C-5, R3 C-6);
   - (v) which width and χ²_core rungs PU populates at ρ = 1 and ρ = 2 (reach per rung).

   If a test fails, the §4.1 failure path applies. If neither category can reach a rung with B₈₄,c ≤ 0.11 even in
   principle, the fallback deliverable (§2.6) applies and the user is told.
5. **C′ topology guns and toys: production, inside C1** (fix R4, review R4 B-1; C′₀ ≈ 12 CPU-h + C′_PU
   4 000 × (4.7 + t₁) s; §4.2). Not a separate step any more. Fix R5: the NI/DIF with-PU events are C′₀ toy events
   that pass the §4.2 preselection, so C′₀ runs first within C1. Depth comes from rung factorisation and the C′₀ factors,
   not from thinning, and zero counts follow §2.5 item 4a. The cost is unchanged. Fix R6: the C′_PU job inserts the stored
   C′₀ toy hits and PV draw (no re-simulation), and V4-10 (attributed candidates in non-preselected C′₀ events = 0) must
   pass on C′₀ before a topology's C′_PU events are used (zero cost).
6. (Withdrawn in fix R4: the optional cloud set-up. Mac only.)
7. **Production = the user-approved campaigns, one at a time, each ≲ 1 day of wall time** (§6.2). The default order is
   the decision-table row below (without the deadline it was C1 → C2 → C3 → C4; C5 only under the T3 rule and G2c).
   Machine: the Mac, 7 workers, nice. After each campaign:
   - V4-1/V4-4 checks;
   - the WP rule is re-applied on the union of the background samples, with results labelled by campaign
     (§2.5 item 11);
   - a short campaign report to the user (CPU-h, wall time, reach, closure status), who then decides on the next one.

   Post-production: V4-2…V4-7, systematics, edges, P2 observables, docs.

**Stage-5 figure list** (constructive C-6; each with its `results/*.json` source and the approved label: left "Private
work (simulation)", right "√s = 14 TeV, PU 200, 3 ab⁻¹", no CMS name or logo, plus "truth level" on truth-level figures): event
displays (signal in PU 200 vs the best PU fake); ε(m, Λ) maps by factor; the fake-rate extrapolation with its closure
(per k); detector-level vs truth edges (incl. the W_c/t_tol attribution); the sep_IT^det calibration; (D4-13, approved) the
M_est spectra and exclusion/discovery contours vs FASER/D0/Farina-Low.

**Selection sculpting of P2** (constructive C-7): the F1 opening-pattern variable is correlated with sep_IT (the Λ⁻² handle).
That is acceptable because the templates are post-selection, but A3 checks the coverage with F1 vs F0; sep_IT itself is
never used in the selection.

**Review (JFC loop):**
1. This plan → the user.
2. Implementation with G1-G3.
3. Production.
4. Stage-4 note `STAGE4_NOTE.md` (pandoc markdown; PDF compiled for the review).
5. R1 critical + R1 constructive reviewers (fresh agents), then a fixer.
6. R2, a fresh reviewer, to PASS.
7. User checkpoint Stage 4 → 5.

**Deadline schedule (fix R4; replaces the R3 timeline).** The user's deadline is Saturday 2026-10-17 night for all of
Stage 4 (production, analysis, review), the Stage-5 figures and final summary, and a short Stage-6 feasibility note. Start:
Tuesday 2026-10-13 afternoon, i.e. ≈ 4.5 days. Times are local wall-clock targets (ESTIMATE). "Mac" = the 7-worker
production load; agent work (reviews, analysis, writing) uses few cores and **runs concurrently with Mac compute**.

| # | Block | Start → end (target) | Wall h | Mac load | Needs |
|---|---|---|---|---|---|
| 1 | Plan fix R4 → fresh narrow review R5 → **plan PASS** | Tue 13 16:00 → 21:00 | 5 | none (agents) | — |
| 2 | **G1/G2a finder speed-up** (running now; PU-only development, `acts/stage4/finder/`) | now → Tue 13 22:00 | — | light | — |
| 3 | **`WP_RULE.md` frozen** from the PASSed plan (§2.5 item 9, incl. the §2.6 frozen inputs); **G2a report** (t₁, campaign table, decision-table row, t₂,max); **user scope choice** (D4-16) | Tue 21:00 → 23:00 | 2 | none | 1, 2 |
| 4 | G1 final (≈ 2 CPU-h); G2: A1 + V4-3, V4-5 brute force, **G2b** (≈ 6 CPU-h) | Tue 23:00 → Wed 14 01:00 | 2 | full | 3 |
| 5 | **G3 pilot** (closure tests T1/T1w, trend, T_seed stability; 13 / 17 / 26 CPU-h at t₁ = 2 / 3 / 5 s) | Wed 01:00 → 05:00 | 2-4 | full | 4, G2b pass |
| 6 | G3 analysis and report; **user approves C1** | Wed 05:00 → 10:00 | 5 | light | 5 |
| 7 | **Production window**: the decision-table set below, one campaign at a time, each ≲ 1 day, a short report and the user's approval between campaigns | Wed 14 10:00 → **Fri 16 12:00** | 47 net (50 gross − 3 h for the inter-campaign reports and approvals) | full | 6 |
| 8 | **Stage-4 analysis**: U-2 panel (§9); analysis code on A1 + G3 outputs; preliminary results on C1 ("C1 statistics", §2.5 item 11); final on the union of the campaigns run; `results/*.json`, `VALIDATION.md`, `STAGE4_NOTE.md` | Wed 10:00 → Fri 20:00 | concurrent; ≈ 8 h after the production stop | light | 6, 7 |
| 9 | **Stage-4 review loop**: R1 critical + constructive (fresh agents) → fixer → R2 to PASS; user checkpoint Stage 4 → 5 | Fri 20:00 → Sat 17 14:00 | 18 | light | 8 |
| 10 | **Stage 5 figures** (label: left "Private work (simulation)", right "√s = 14 TeV, PU 200, 3 ab⁻¹", no CMS name or logo; "truth level" on truth-level figures) and the **final summary document** | scripts from Thu on C1 outputs; final Sat 08:00 → 18:00 | ≈ 10 | light | 8; regenerated after 9's fixes |
| 11 | **Stage 6 feasibility note** (short; no downloads, no analysis; CMS Open Data policy reminder) | draft Wed-Thu; final Sat 14:00 → 20:00 | ≈ 3 | none | — |
| 12 | Buffer; handover to the user | Sat 20:00 → 24:00 | 4 | — | — |

Development and gates (blocks 4-5) take ≈ 21 / 25 / 34 CPU-h, i.e. 3.0 / 3.6 / 4.9 h of Mac wall at t₁ = 2 / 3 / 5 s
(`f4r_deadline.json` → `dev_and_gates_cpu_h`); the G3 pilot grows by ≈ 0.6 h of wall per +1 s of t₁.
- *G3 slot (review R5 C-3).* The G3 pilot fits block 5's 4-h slot up to t₁ ≈ 5.4 s. Above that it overruns, by ≈ 1.0 h
  at 7 s and ≈ 4.2 h at 12 s. The overrun is a slip under the rules below, and the row margins stay positive (≈ 3.3 h at
  7 s, ≈ 8.0 h at 12 s; review R5).
- *A1 is listed once.* The A1 run of block 4 (G2, "all of A1 + V4-3") is the A1 that C1 contains. C1 reuses that output,
  and A1's 2 CPU-h stay in the C1 cost as a reserve. No row changes.
- *The production window.* Block 7 is ≈ 47 h of Mac wall, ≈ 329 CPU-h, with **no margin for a rerun**: 50 h gross
  (Wed 10:00 → Fri 12:00) minus 3 h for the reports and approvals between campaigns. `probes/f4r_deadline.py` writes the
  same 47 h as "Wed 14 13:00 → Fri 16 12:00", i.e. with the 3 h placed at the start. The probe is left unchanged as the
  audit record; its numbers use 47 h either way.

**Rules of the schedule:**
- *Production stop.* A campaign (or sub-run) starts only if its ESTIMATE wall time ends by Fri 16 12:00. If a running
  campaign overruns by > 20 %, the user is told. At the stop, completed jobs are kept and used: seed ranges are disjoint,
  so the samples simply add, and the results are labelled with the statistics actually used (§2.5 item 11).
- *Slips.* A slip before production (plan PASS, G2a, G3, approval latency) comes out of the production window through the
  deferral order. It never comes out of blocks 8-12. If a slip leaves the remaining window shorter than C1 itself (review
  R5 C-3), the next-slower row's C1 content applies:
  1. C1a → C1b. C1b is cut at the production stop, and its completed jobs are kept.
  2. Then C1r.
  3. If C1r does not fit either, the user is asked.
- *Approval latency.* Approvals can fall at night. To avoid idle Mac hours, the user may approve the decision-table row
  in advance at G2a (D4-16). Each campaign is still followed by its short report, and the user can stop the sequence at
  any report.
- *Concurrency.* Blocks 8-11 are agent work at low CPU and run while the Mac produces. Stage-5 figure scripts are written
  on C1 outputs, but the final figures are produced only from the PASSed `results/*.json`.

**Decision table: which campaigns run, as a function of the measured t₁** (Mac only, t₂ = 8 t₁ until G2b, window 47 h;
`fix_r4/f4r_deadline.json` → `deadline_sets`, `campaigns`). **Deferral order** (first dropped first): **C5, A3, A4, C3**.
C5 is deferred in every row.

| measured t₁ | campaigns, in execution order | Mac wall (h) | fits 47 h | deferred |
|---|---|---|---|---|
| ≲ 2 s | C1 → C2 → C4′ → C3 → A4 → A3 (= C1-C4, tight) | 13 + 13 + 9 + 8 + 1.4 + 1.0 = **45** | yes, ≈ 2 h margin, if t₂ ≤ 21 s | C5; then A3, A4, C3 from the end if late |
| ≈ 3 s | C1 → C2 → C4′; A4 → A3 only if ≥ 3 h ahead of schedule | 15 + 16 + 11 = **42** (+ 1.8 + 1.4) | yes, ≈ 5 h margin, if t₂ ≤ 44 s | C5, C3; A3, A4 unless ahead |
| ≈ 5 s | C1 → C2 | 20 + 22 = **42** | yes, ≈ 5 h margin, if t₂ ≤ 53 s | C5, A3, A4, C3, C4′ |
| 5-7 s | C1 → C2-B (the B1/B2 part of C2: the PU reach to 1.6 × 10⁻¹⁰) | 20-24 + 15-19 = **34-43** | yes | C2-C (2 SM samples), C3, C4, C5 |
| 7-12 s | C1 as two sub-runs, C1a (A1, A2, A5, C′) → C1b (B1, B2, C) | **24-35** | yes | everything after C1 |
| 12-16.5 s | C1r, the reduced C1 (one run) | **19-24** | yes | C1 at full size and all later campaigns |
| > 16.5 s | **ask the user**: C1r as two sub-runs (fits the window up to t₁ ≈ 37 s, minus the longer G3), or no production | — | — | — |

Intermediate t₁ use the next-slower row. If t₁ > 5 s, Stage 4 still delivers everything that does not need the deferred
samples: A1/V4-3 (no-PU efficiencies and detector-level edges), ε and B at the pre-declared selections with the C1 (or
C1r) background statistics, the closure results, the SM/NI/DIF table and the fallback deliverable (§2.6). The reduced PU
reach is stated (C1: 5 × 10⁻¹⁰ per trial; C1r: ≈ 10⁻⁹), so the deepest rungs rest on rung factorisation and T3. At the
measured 211 s/trial no row applies: the deadline then depends entirely on the speed-up of block 2.

---

## 12. Risks

1. **Finder CPU under the one-day cap** at the TDR-normalised density. Fix R2 measured 211 s/trial at the full IT + OT
   density with the O(N²) merge vectorised (§2.4). The ESTIMATE after the §6.2 routes is 5-20 s.
   - Every campaign needs t₁ ≲ 5.6 s to fit one Mac day; C1 (with C′) alone needs ≲ 7.0 s. Under the deadline, t₁ ≈ 3 s
     is the target and t₁ ≈ 5 s the last value at which two campaigns fit (§11 decision table).
   - Over the full scope, every +1 s/trial at ρ = 1 adds ≈ 53 CPU-h and every +1 s at ρ = 2 adds ≈ 2.8 CPU-h.
   - Mitigation: the §6.2 routes (hash merge, (φ, z) hit index, N_IP2 seed score with T_seed(ρ), numba refit); the G2a
     scope choice (C1 as the minimal option); campaigns split into ≲ 1-day sub-runs; the §11 decision table with its
     deferral order and the C1a/C1b and C1r fallbacks.
   - If even C1r does not fit (t₁ > 16.5 s), the user chooses between C1r as two runs and no production (§11).
2. **PU-fake extrapolation** over ≥ 4 decades: the model uncertainty could be ×10 or more. This pushes the WP tighter and costs
   low-Λ efficiency. Mitigation: exact k-thinning (no fitted exponent), the measured SR-T time factor, F1 variables, the
   closure gate with a lever-arm minimum, a trend test and a pre-registered failure path split by direction. **Fix-R1/R2
   findings:** with per-crossing counting the layer count and χ² alone do not reach the target at the TDR-normalised density.
   The robust core width does separate at Λ ≳ 2 keV and is now a rung family, so the WP will rely on the width, dE/dx and
   SR-T. The helix and opening tests act mainly on single-interaction topologies (§2.6). The pilot shows an unexplained
   ×1.6-1.8 conservative closure residual, which G3 decides on (§4.1). **A background-free WP may exist only for heavy masses
   at Λ ≳ 2 keV; elsewhere the pre-defined fallback applies (§2.6).**
2b. **Signal width at the normalised density** (review R3 C-3). w_core's power is measured on PU only; the signal values
   (≥ 2 keV medians 4-13 mm) are at Fatras density. With ≈ 15-17 in-band IT + PS PU crossings per band, against ≈ 20
   hits of a heavy pair, the MAD (breakdown point 50 %) can inflate the signal width at the normalised density. That
   would lower ε at the width rungs and shift the admissible fallback levels' effective efficiency. It is measured at G2
   (A1/V4-3 without PU) and in C1 (A2 with PU), and reported vs Λ. No threshold is changed after the freeze.
3. **Missing PU physics** (out-of-time loopers, nuclear interactions, δ-rays, noise): the Fatras in-time density is low by
   ×2.3-7 per layer against the TDR (V4-2, VERIFIED in fix R1). Mitigation: the TDR top-up as baseline, its range as a
   systematic, the looper-pair variant. The IT ratio rests on an uncited IT cluster size (ESTIMATE).
3b. **Nuclear interactions at r ≤ 62 mm** (≈ 26 per event in the road, ESTIMATE): before F1, the two-prong estimate is
   P(fake) ~ 10⁻³-10⁻² per event (§4.2, corrected in fix R2), 6-7 decades above the target. It is not an upper bound: with
   the kink (r_NI ≥ 30 mm) and line + near-vertex-hit (22 mm) paths the attributable rate at R0 may be ≈ 0.6-3.6 per
   event, **≈ 8-9 decades above the target (9-10 under the strict B₈₄ rule)** (ESTIMATE; fix R6, review R6 C-1). Fatras
   cannot simulate NIs. Mitigation: the free-origin helix, opening linearity,
   dE/dx, timing, and the NI toy; if the toy shows F1 is not enough, a Geant4-based check needs a user decision (D4-7).
4. **Idealised geometry**: full cylinders and discs, no module gaps or overlaps, flat tilted TBPS rings, ETL outside ACTS. The
   acceptance is optimistic by a few % (ESTIMATE). Mitigation: the hit-efficiency variation; noted in the handover.
5. **Smearing digitisation** (no clusters, charge sharing, Lorentz drift or dE/dx): the merged regime and any dE/dx handle are
   approximate. Channelised clustering is a later cross-check (U-5).
6. **Endcap φ resolution** on full discs varies ×2.5 across the radius. Mitigation: split into rings if the endcap matters.
7. **Trigger, MET, PV and SM normalisation** are parametrised or LO (UNVERIFIED until CMS-TDR-021 and the K-factors are cited).
8. **Rare Fatras failures:** ≈ 1-3 particles per PU event fail with "max steps" (low-p e±/γ; VERIFIED in the logs).
   Negligible; logged per job.
9. **Two simulators:** the quirks come from the Stage-3 kernel (thick slabs, causal string), PU from Fatras (thin scatterers).
   The x/X₀ is the same, so this matters only for PU multiple scattering. Accepted.
10. (Withdrawn in fix R4: cross-machine non-bit-identity of the cloud VM. Mac only; the cloud option was considered and
    dropped by the user.)
11. **Thin PU reach with the minimal scope.** With C1 alone the thinning reach (≈ 5 × 10⁻¹⁰ per trial) is above the
    per-category requirement (≈ 3 × 10⁻¹⁰), so the deepest rungs depend on the rung factorisation and its closure test
    T3. C2 brings it to 1.6 × 10⁻¹⁰ and C3 to 10⁻¹⁰; C3 is deferred under the deadline at t₁ ≳ 2.5 s (§11).
12. **Deadline** (fix R4). The whole schedule (§11) leaves ≈ 47 h of production and no rerun margin. A failed campaign
    or a late gate removes campaigns in the deferral order (C5, A3, A4, C3, then C4′, C2). If even C1 no longer fits,
    the next-slower row applies (C1a → C1b, then C1r, then ask the user; §11 slip rule). Approval latency at night is
    the main schedule risk; the user may pre-approve the decision-table row at G2a.
