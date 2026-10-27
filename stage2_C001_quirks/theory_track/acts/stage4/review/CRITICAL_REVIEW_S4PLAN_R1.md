# Critical review R1: Stage-4 plan (`acts/stage4/plan.md`, E9, 2026-10-13)

Reviewer: S4PLAN-R1-critical (fresh agent), 2026-10-13. Role: `jfc/src/agents/critical_reviewer.md`, methodology
`01-core.md` and `03-review.md`. Classification follows the caller's scheme: **A** = blocks or invalidates, **B** = must be
fixed before production, **C** = minor or optional. The user's approved decisions (U-1…U-5, D4-1…D4-12) are not
re-litigated. Findings concern how the plan implements them.

**Independent checks run** (read-only use of the E9 probe code; outputs in `data/acts_stage4/review_r1/`; about 7 CPU-min in total):
- `r1_pu_fullrefit.py` → `r1_pu_fullrefit.json`. The same 8 central E1000 1 keV signal + PU events and the same 24 PU-only
  trials as p5 (same RNG stream for the MET directions). The p5 seeding is unchanged. The difference is that **every**
  distinct (a, b) seed plane with seed N_L2 ≥ 9 (610-1862 per trial) is refitted, where p5 refitted the top 30 by seed score.
  N_L2 is also recounted per sensor.
- `r1_truth_window.py` → `r1_truth_window.json`. Stage-3 truth hits only (no PU, no smearing), template half, `in_eta25`,
  status 1, |η_pair| < 1, at E200, E1000 and Ẽ500. It evaluates the F0 collection window (|u·n₂| < 50 mm), N_IT2 and Δw on the
  true plane.
- Arithmetic: cross-section → N(3 ab⁻¹) → P_fake, the compute totals, road widths, Poisson saturation, and the reach of the
  density ladder. The TDR text in `data/tdr_geometry/` was checked for the V4-2 references and the BTL numbers.

---

## Category A

### A-1. The pre-registered F0 selection contains an upper cut Δw < 1 cm. It removes the signal, and the plan's own probe shows this.
- **Plan:** §2.2 step 6 (l.256-258) fixes the selection shape "now": "Δw > w_min … and < 1 cm (as Knapen)". §2.5 item 1
  (l.299) freezes the shape before production.
- **The plan's own probe contradicts it:** §2.4 (l.290) gives the best signal candidate as "Δw 11-31 mm".
  - Re-read from `data/acts_stage4/p4/p5_meas_sig_pu_L{1,3}_BM_c00_central.json`: all 10 signal candidates with
    10/10 layers have Δw = 11.3-25.3 mm. The weaker 1 keV candidate has 33.6 mm. **None** is below 10 mm.
  - PU-only best candidates have Δw = 14-33 mm. Δw as computed (`p4_finder_proto.refit`, `np.std(U[sel] @ n2)`) is the rms
    of *every* in-band hit inside the |u·n₂| < 50 mm window. With PU 200 it is dominated by PU hits filling the window (a
    uniform fill of ±50 mm has rms 28.9 mm). So it is neither a signal width nor a "real ribbon" discriminant.
- **Even at truth level** (no PU; `r1_truth_window.json`), the fraction of central events with Δw < 10 mm is:

  | Point | 0.6 keV | 1 keV | 2 keV | 3 keV |
  |---|---|---|---|---|
  | E1000 | 0.11 | 0.26 | 0.80 | 0.94 |
  | Ẽ500 | — | 0.12 | — | — |
  | E200 | 0.24 | 0.60 | — | — |

  These are the Λ values where the plan says the detector-level lower edge is set (l.207-209).
- **Consequence:** executed as written, ε(m, Λ) would be ≈ 0 at the low edge and suppressed in the ribbon regime. The
  main deliverable (ε, edges, yields) would be invalid. The "1 cm (as Knapen)" number is carried over from a different
  geometry and finder without justification.
- **Required fix:**
  1. Remove the Δw upper cut from the frozen shape, or re-derive it on background samples only, with Δw redefined on the
     candidate's core hits (e.g. after outlier rejection, or on IT hits only).
  2. State what w_min is supposed to reject, and show on PU-only and SM samples that the variable separates anything.
  3. Re-check every other selection element against the existing probe outputs before `WP_RULE.md` is frozen.

---

## Category B

### B-1. The "VERIFIED" signal-vs-PU separation of the finder prototype comes from an asymmetric, truth-assisted refit.
- **Plan:** §0 (l.30) and §2.4 (l.291) say that across 24 PU-only trials "the best PU candidate has N_L2 ≤ 6", against 10/10
  for the signal. §2.1 (l.230) calls PU candidates at "N_L2 ≈ 4-6" consistent with the density estimate.
- **How the probe got these numbers:** `p5_finder_triplet.py` l.111-113 refits `out[:30] + sigtrip`.
  - `sigtrip` is up to 20 seeds whose three hits are **truth-flagged signal** (`h[o, 6] > 0`).
  - PU-only trials refit only the top 30 of ≈ 10⁵ seeds by seed score.
  - The signal seeds have seed score (10, 10), while 6-8 × 10³ PU seeds per trial score ≥ 10 (score histograms in the same
    JSON). A blind top-30 selection would therefore not have refitted the signal at all.
  - So the signal candidates were found with truth help, and the PU candidates were searched far less thoroughly.
- **Blind re-run** (`r1_pu_fullrefit.json`, every seed plane with seed N_L2 ≥ 9 refitted):
  - The best PU-only N_L2 is **9 in 14/24 trials and 8 in 10/24**, not ≤ 6.
  - The signal events still give 10/10 blind in the same 5/8 events.
  - PU candidates with N_L2 ≥ 9 have χ²/ndf 2.1-3.7, against 0.9-1.9 for the signal.
  - The separation in layer count is therefore one layer, not four. It does not support "the finder separates" as VERIFIED,
    and it bears directly on how many rungs the B_PU extrapolation must span (B-4).
- **Required fix:**
  1. Re-tag the §0/§2.4 claims: the signal efficiency came from truth-selected seeds, and the PU-only search was incomplete.
  2. Before G2/G3, repeat the probe with the production ranking (no truth anywhere in seed selection), and record the full
     PU-only N_L2 and χ² distributions.
  3. Design the ladder on those distributions.

### B-2. N_L2 / N_OT2 count a single crossing of a stacked module as "≥ 2 hits".
- **Code:** `p4_finder_proto.layer_of` maps `TBPS_Lk_in/_out` and `TB2S_Lk_in/_out` (and the disc PS/2S in/out parts) to one
  counting layer. One particle crossing a stacked OT module leaves one hit on each sensor, which already satisfies "≥ 2 hits".
- **Plan:** §2.2 step 5 (l.250) defines N_OT2 the same way ("stacked pair = one layer").
- **Consequences:**
  - "10/10 barrel layers with ≥ 2 hits" (l.30, l.290) does not show that both quirks are seen in the OT.
  - A single PU track coplanar with the PV, which happens whenever the track lies in the plane, gets N_OT2 = 6.
  - The random-hit expectations of §2.1 (l.224-230) are per sensor, so the pair probability per stacked layer is mis-stated.
- **Re-derived:** with per-sensor counting, the blind best PU-only candidate drops to N_L2 = 6-8, and the signal keeps 9-10
  (`r1_pu_fullrefit.json`).
- **Required fix:** define N_OT2 as ≥ 2 distinct crossings per stacked layer, e.g. ≥ 2 stubs built from in/out pairs, or
  ≥ 2 hits on one sensor. Redo the §2.1 band-occupancy estimate per stub, and correct the probe statements.

### B-3. The fixed collection window W_c = 50 mm, not physics, sets the low-Λ efficiency edge. The second seed family does not change this.
- **Plan:** F0 keeps only hits with |u·n₂| < W_c = 50 mm (l.235-236, l.244), and the road uses the same W_c. §2.1
  (l.207-209) says the detector-level lower edge is set in the wide regime, and l.242 says the (L3, L2, L1) seed family
  "recovers the wide regime". It does not: the collection window is the same for both seed families.
- **Truth level** (`r1_truth_window.json`, central events, true plane):

  | Point, Λ | Median fraction of TBPX quirk hits inside ±50 mm | Events with N_IT2 ≥ 3 inside the window |
  |---|---|---|
  | E1000, 0.45 keV | 0.375 | 26 % |
  | E1000, 0.6 keV | 0.625 | 43 % |
  | E1000, 1 keV | 1.0 | 81 % |
  | Ẽ500, 0.45 keV | 0.375 | 9 % |
  | E200, 0.45 keV | 0.75 | 49 % |

  At Ẽ500, 0.45 keV the median fraction of L3/L4 hits inside the MET road is 0.5. The truth thickness edge is at
  0.47-0.55 keV and ℓ_max = R_IT at 0.43-0.94 keV (HANDOVER §5.3). F0 will therefore move the edge up through a finder
  parameter, most strongly for the scalar and for heavy masses.
- **Required fix:**
  1. Make W_c and the road part of the pre-registered design with an explicit justification.
  2. Report ε vs W_c (e.g. 50/100/150 mm) on background-only grounds, or add a wide-regime topology: two separate curved
     tracks, each coplanar with the PV and the MET plane.
  3. Make V4-3 attribute any shift of the low edge explicitly to W_c and the road, separately from resolution and merging.
  4. List the regimes F0 cannot reach by construction (low-Λ scalar, |η| ≳ 1.1 gaps between barrel and mixed triplets) as
     analysis limitations, not as physics edges.

### B-4. The density-ladder extrapolation model is not physically motivated, and the B2 specification is inconsistent and cannot reach the working-point rung.
- **(a) Model.** P(r; ρ) = A_r ρ^{α_r} (l.358-362) assumes one dominant mechanism per rung. In reality the fake rate is a sum
  of components with different density exponents:
  - **Single-interaction topologies scale ∝ ρ.** Conversions, V0s, loopers, and tracks from a PU vertex that coincides with
    the PV: at PU 200 the PV sees ≈ 1.25 PU vertices/mm, i.e. ≈ 0.25 expected (P ≈ 22 %) within ±0.1 mm (ESTIMATE).
  - **Random multi-hit coincidences scale ∝ ρ^k with large k.**
  - **Saturation.** For P(≥ 2 in band) in a Poisson model, the local exponent falls with ρ:
    - TBPX L1 (μ = 0.63 at ρ = 1, l.225): 1.60 at ρ = 1 → 0.96 at ρ = 3 → 0.71 at ρ = 4;
    - TB2S L1 (μ = 0.44): 1.72 → 1.22 → 1.01.
  - A single power law fitted at ρ = 2-4 is dominated by the steepest component. Extrapolated down, it **under-estimates** the
    shallow (∝ ρ) components that dominate at ρ = 1, which is anti-conservative. Saturation pulls the other way. The net
    direction is unknown, so the closure gate cannot be relied on to catch it (B-5).
- **(b) The B2 specification contradicts itself.**
  - §4.1 says "superpositions of 2, 3 and 4 independent PU-200 events", "5 × 10³ events per density point", and the closure
    "predict ρ = 2 from ρ = 3, 4" (l.358-369).
  - §5 B2 says "5 000 at ρ = 1.5 and 2; 2 000 at ρ = 3" (l.425).
  - §6.2 says "ρ is capped at 3 and only one road per event" (l.475-476).
  - ρ = 4 is never produced, so the pre-registered closure cannot be run. ρ = 1.5 is not a superposition of independent
    PU-200 events.
  - The costed 90 CPU-h matches the §5 version (re-derived ≈ 92 CPU-h assuming finder cost ∝ ρ³). The §4.1 version with
    5 000 events at ρ = 4 would add ≈ 200 CPU-h.
- **(c) Reach.** The working point needs P_WP ≈ 3 × 10⁻⁹ at ρ = 1. For about 10 counts at the WP rung itself, the exponent
  must be large:
  - ρ = 3 with 2 000 events: α ≥ 12.9;
  - ρ = 2 with 5 000 events: α ≥ 19.2.

  Otherwise the WP rate rests on a second extrapolation across rungs, which the plan does not describe. "The rates at the
  tight rungs become measurable at high density" (l.359) is therefore an unverified claim. G3 (l.630-631) checks this only
  on a pilot, and no action is specified if it fails.
- **Required fix:**
  1. Replace the free power law by a model with a physical basis. Options: a polynomial in the integer superposition number
     n with non-negative coefficients (P(n) = Σ_k c_k n^k, where k = number of independent interactions involved, and the
     n = 1 point *in* the fit), or a per-layer Poisson-occupancy model calibrated on the measured in-band occupancies.
     Explicitly include an ∝ ρ term for single-interaction topologies.
  2. Make §4.1, §5 and §6 agree on the density points and statistics, and cost them.
  3. State how the WP rung is reached when it is not measurable at the highest density, and what happens when the G3 pilot
     shows the ladder does not span it (e.g. tighten F1 variables, add ρ, or escalate to the user).

### B-5. The closure gate and the per-layer factorisation are not specified well enough to fail, and there is no fallback.
- **Plan:** "predict the PU-200 rate at the tightest measurable rung … using only the looser rungs; agree within 2σ"
  (l.366-369), and "A failure means more statistics or a different model (≥ 3 documented attempts)" (l.371).
- **Problems:**
  - **Lever arm.** No minimum lever arm is fixed. If the tested rung is one rung beyond the fitted ones, the test says
    nothing about a 4-decade extrapolation (4 × 10⁻⁵ → 3 × 10⁻⁹).
  - **Weak test.** With ≈ 10 counts at the tested rung, ±2σ is ≈ ±60 %, so the test is weak in any case.
  - **Model shopping.** "A different model" after a failure is post-hoc model selection.
  - **No end state.** Nothing says what happens after 3 failed attempts.
  - **Factorisation correlations.** P(tight) = P(loose) Π p_l (l.364-365) assumes conditional independence between layers.
    Correlations are expected from local density (PU jets, PU vertices near the PV, one looper giving several hits per layer,
    a common CKF-removal pattern) and from the band width, which depends on the fit. These make Π p_l under-estimate the
    joint probability (anti-conservative). The plan has no test of this.
- **Required fix:** pre-register in `WP_RULE.md`:
  1. the fitted rungs and the tested rung, with a minimum gap (e.g. ≥ 1 decade in rate);
  2. the test statistic and the pass criterion;
  3. a direct factorisation test, measured vs predicted for pairs and triples of layers on loose candidates, with
     conditioning in bins of local hit density;
  4. a fallback if closure fails: B_PU taken from the most conservative of the pre-declared models (upper envelope) and the
     WP tightened, or escalation to the user. No post-hoc choice of the model that passes.

### B-6. The working-point rule is not fully defined, and the freeze comes after signal efficiencies have been seen.
- **"B ≤ 0.3 at +1σ" (l.303-305).** B_PU is a multi-decade extrapolation with a model spread the plan itself expects to be
  "×10 or more" (risk 2, l.650). A symmetric +1σ is not meaningful at that scale.
  - Define the uncertainty in log space (e.g. log-normal with the model spread as width), or use an explicit upper quantile.
  - Define the ladder as a single 1-D ordered path over (k_IT, k_OT, p_min, w_min, h_min, t_min).
  - Require that the chosen rung and all tighter rungs satisfy the criterion, since an extrapolated B need not be monotonic.
- **Inconsistent budget.** §4.1 sizes P_fake for B_PU ≤ 0.1 (l.349-350); the WP rule uses total B ≤ 0.3. State the split
  between B_PU and B_SM.
- **Leakage.**
  - `WP_RULE.md` is frozen "before any signal + PU run" (l.308) at G3 (l.630). G2 (l.628) runs V4-3, the signal-only
    efficiency vs Λ on 2 masses × all Λ, before G3, and A1 also exposes signal efficiencies.
  - The finder design was already iterated on 13 E1000 c00 signal events with truth-selected seeds (B-1). Examples:
    "refit before ranking" (l.246-247), and the t_est/band discussion (l.293-295).
- **Required fix:**
  1. Freeze the ladder, the variable definitions (incl. A-1, B-2, B-10) and the B criterion before **any** signal efficiency
     is computed, or restrict V4-3 at G2 to candidate-finding efficiency without the selection variables.
  2. Record the probe rows (E1000 c00 at 0.6/1/3 keV) and exclude them from the template efficiencies, or show that the
     effect is negligible.

### B-7. The PU-density benchmark (V4-2) uses the wrong TDR numbers, and the density normalisation is the leading B_PU systematic.
- **Plan:** V4-2 (l.550) takes "TBPX L1: 3 GHz/cm² pixel-hit rate [CMS-TDR-014 PDF p.80] … divided by the cluster size
  [ibid. Fig. 12.3]".
- **Both references are wrong for this purpose:**
  - 3 GHz/cm² is the RD53 **chip specification**: TDR Table 4.4, "Pixel readout chip specifications … Hit rate < 3 GHz/cm²"
    (`CMS-TDR-014_Phase2_Tracker_TDR.txt` l.3470-3488). It is a design capability with margin, not the expected PU-200 rate.
  - Fig. 12.3 is the **Outer Tracker** cluster size (ibid. l.13776: "Simulated cluster size distributions for the Outer
    Tracker are depicted in Fig. 12.3"), not the IT.
  - The appropriate public benchmark is the hit occupancy vs η for every IT/OT layer (Fig. 6.3, tt̄ + PU 200, ibid.
    l.4336-4412). It includes 12 previous crossings (l.4286-4288, l.4331-4332).
  - The status column claims both densities are "lower than the TDR, as expected". No number supports this.
- **Why it matters:** P_fake ∝ ρ^α with α ≳ 10 at tight rungs (B-4). A density error of ×1.5 changes B_PU by 1.5^α ≈ 60
  (α = 10). The "×1.5 one-sided density systematic" (l.372-373, §7 l.521) is therefore the leading B_PU term, and the
  nominal ρ itself must be set from the benchmark, not left at the Fatras-in-time value.
- **Required fix:**
  1. Benchmark per layer against Fig. 6.3 (convert occupancy per channel to clusters/cm² with the pitch and an IT
     cluster-size reference that is cited correctly), before production.
  2. Evaluate B_PU at the benchmark-normalised density (interpolate on the ladder), with the residual as the systematic.
  3. Re-tag the V4-2 sources.

### B-8. SM, nuclear-interaction and decay-in-flight backgrounds: no closure test, an incorrect veto argument, and no stated folding into B.
- **SM reach.** §4.2 (l.400-402): 5 000 events per SM sample (direct reach ≈ 6 × 10⁻⁴) are extrapolated by "hard-scatter-
  seeded loose candidates × conditional tight probability". Each SM sample contributes O(10⁷) triggered events, so it needs
  P ≲ 10⁻⁸ per event. That is a 4-5 decade extrapolation with **no closure test**; B-5 applies here too.
- **Nuclear interactions** (l.393). "N_IT2 kills r_NI > 6 cm" leaves interactions in the beam pipe (r = 22 mm) and on
  TBPX L1 (30 mm). Their collimated forward prongs give ≥ 2 hits in TBPX L2-L4 and the OT in a narrow ribbon. Combined with
  the ≈ 22 % chance of a PU vertex within ±0.1 mm of the PV (B-4 a), the parent can point to the PV. This topology is the
  most signal-like one that Fatras lacks.
- **Folding into B.** The rule's B (l.303-304, "PU extrapolation + SM") does not state that the NI/DIF toys, conversion and
  V0 guns enter it, nor how P(fake | topology) is normalised to the in-road rate per triggered event.
- **Missing samples** (minor): tt̄ 2ℓ, single top, WW/WZ/ZZ. They matter mainly through N_presel; their own fakes are prompt
  tracks.
- **Required fix:**
  1. Pre-register the SM extrapolation with the same closure and fallback as B-5.
  2. Give the NI toy explicitly for r_NI ∈ {beam pipe, L1, L2}, with ESTIMATE rates before production.
  3. Write the full B sum used by the WP rule (PU + SM + conversions + V0 + NI + DIF + cosmics), each term with its
     normalisation and uncertainty.

### B-9. D4-10 (robust-shift treatment, flagged low confidence by the user): the rule is ambiguous, and in its plain reading it is anti-conservative.
- **Plan:** "symmetrise to max(|up|, |down|); keep shifts below 2× their sampling sd as noise-limited bounds at 1× sampling
  sd" (l.593).
- **Opinion:**
  - Symmetrising to max(|up|, |down|) is conservative and consistent with HANDOVER §5.4, which asks for the shifts to be used
    as conservative bounds.
  - The second clause, read as "replace a sub-2σ shift by 1 sd", **reduces** a 1.0-1.99σ shift (by up to ×2). That is not
    conservative and is discontinuous at 2σ. HANDOVER §5.4 counts 198/243 components below 2 sd, so this is the common case.
  - Physically one-sided sources (QED −1.1 ± 0.8 %; status-4 losses) must not be symmetrised.
  - Summing ≈ 100 PDF/scale noise-limited components in quadrature turns template noise into a systematic that grows as √N.
- **Required fix:**
  1. Use max(|up|, |down|) for genuinely two-sided sources and keep one-sided sources one-sided.
  2. For sub-2σ shifts, use max(|shift|, sd) as a bound, never min.
  3. Evaluate families with their prescription (PDF replicas → one PDF envelope/rms; scale → envelope) on paired weights.
  4. Better still, smooth each shift across Λ (and ln m), as is already done for the edges, so that template noise averages
     out rather than accumulates.
  5. Write the chosen rule into the systematics section with one worked example.

### B-10. F1's "crossing count" cannot be computed from detector-level hits as defined.
- **Plan:** "number of sign changes of the per-layer two-cluster separation" (l.271-272). F1 selection uses
  "crossings ≥ 1" (l.278).
- **Problems:**
  - **Undefined.** A *signed* separation needs the two clusters labelled consistently across layers. The hits carry no
    quirk identity (both are charge-±1 hits), so only |separation| is observable.
  - **Under-sampled.** N_osc ≈ 12 (Λ/keV)² over the tracker (LOG l.18) is sampled by 4 IT + 6 OT layers.
  - **Unresolved in 2S.** When n₂ has a large z component, the 2S long resolution (14.5 mm, §1.5) cannot resolve mm-scale
    separations.
- **Required fix:** before the freeze, redefine the variable as non-monotonicity of |separation| vs radius, using only layers
  whose resolution along n₂ (projected σ) is below the expected separation. Otherwise drop it from F1. The BTL-delay term is
  realistic as defined (35 ps vs ns delays; BTL bars along φ confirmed, MTD TDR txt l.1457).

---

## Category C

- **C-1. The PU-only roads are not disjoint.**
  - "The trials within one event share no hits (disjoint roads)" (l.356) is false for the IT. The road half-width
    0.25 + asin(min(1, 50/r)) is 1.82 rad at TBPX L1 and 1.20 rad at L2. With four roads π/2 apart, each L1 hit lies in 2.3
    roads on average and each L2 hit in 1.5.
  - The event-level bootstrap (l.357) still gives correct errors. Fix the text and quote the effective number of
    independent trials.
- **C-2. Two cost statements are wrong; the totals reproduce.**
  - "Every +1 s/trial adds ≈ 40 CPU-h" (l.263): re-derived **≈ 85 CPU-h**. That is 54 CPU-h for the 1.95 × 10⁵ non-B2
    trials plus 31 CPU-h for B2 with ρ³ scaling.
  - The ≈ 900 CPU-h at prototype speed (l.473) is reproduced (≈ 960).
  - "≳ 10⁹ PU-200 events (≈ 10⁵ CPU-years)" (l.350): 10⁹ × 13 s ≈ **4 × 10² CPU-years**. The conclusion is unchanged.
  - Totals reproduced: A2 119 CPU-h, B1 72, B2 92, total ≈ 450.
- **C-3. The CKF signal-loss probe has fewer independent events than stated.**
  - "0 of 205 quirk measurements … 6 events" (l.28, V4-6 l.554): the p3 JSONs give 35+36+38+26+36+37 = **208**.
  - The 0.6 and 1 keV runs share the same 3 PU events (pool seed 20261015, RNG 91), so there are 3 independent PU events.
  - `p3_summary_n32.json` and `p3_summary_n32_L1.json` are the same run. `p3_summary_n1.json` reports `n_meas_on_tracks = 1`
    (broken counter), so the 18 % comes from the n32 runs only.
- **C-4. Exact-count provenance for the PU overlays is missing.** `p2_summary.json` records the signal + PU exact count only
  for the 5-event 3 keV run. The "8 events" (l.26) and "13 signal + PU events" (V4-1 l.549) have no surviving JSON, because
  the summary was overwritten. Regenerate or record this at G1.
- **C-5. φ-sectoring (D4-2) is sound for the quirk hits.**
  - The quirk hits are placed by global φ (`s4geo.sector` clamps φ = π), so there is no navigation drop or duplication, and
    every sector carries the same homogeneous material.
  - For PU, n1 vs n32 with identical seeds differ by −73…+130 measurements per event (≤ 0.1 %, p3 JSONs), so Fatras navigation
    at sector edges is not exactly equivalent.
  - Add a muon gun aimed at sector boundaries to V4-9 at G1.
- **C-6. SM cross-section probe: arithmetic checks out, with caveats.**
  - 14.56 + 15.85 pb = 30.4 pb → 9.1 × 10⁷ events in 3 ab⁻¹ (VERIFIED). B_PU = 0.1 at 3 × 10⁷ gives P = 3.3 × 10⁻⁹
    (consistent).
  - Caveats: pT̂ > 150 GeV truncation (ISR can give pT(V) > 200 GeV from lower pT̂); `HadronLevel:all = off` excludes
    τ-decay neutrinos from the MET; a K-factor of 1.2-1.4 raises N. All of these push the required P_fake down slightly.
- **C-7. Tagging corrections.** The BTL end-of-life 50-60 ps is in the MTD TDR (txt l.307-308) and can be VERIFIED. The 57 mm
  bars along φ are confirmed (l.1418, l.1457). The production BTL axes in §1.5 are right; the probe had them swapped, as the
  plan says.
- **C-8. The cosmic "muon-system veto" (l.396) may cut signal.**
  - Status-1 quirks leave the tracker, and the calorimeter deposit is ≲ 5 GeV (`sim/DEFERRED.md` l.29). Whether the pairs
    reach the muon stations is not discussed.
  - Before using any muon-system veto, show its signal efficiency, or drop it. If the pairs do reach the muon stations, an
    L1-muon or HSCP-like complementary path should be noted.
- **C-9. Edge-fit errors are too small if the Λ points are treated as independent.** A2 uses the same rows **and** the same
  PU at every Λ (l.378-380). Points across Λ are therefore strongly correlated, and independent binomial errors in the
  logistic edge fit (l.434-435) are wrong. Use a row-level bootstrap applied jointly across Λ.
- **C-10. B1/B2 store summaries only** (l.375-377, §6.3). Any finder change after G3 (e.g. a closure-failure remedy) then
  means full regeneration (≈ 160 CPU-h). Consider storing road hits for a B1 subset.
- **C-11. The merging variation may not cover the long direction.** The 1 vs 2 pitch merging variation (U-5 b) ignores
  cluster elongation along the long direction with incidence angle: in the IT, about 150 µm × cot θ, i.e. several 100 µm
  pixels at |η| ≳ 1.5. Mention it in the U-5 cross-check scope.
- **C-12. The PV for PU-only trials is not specified.** State whether the PV is a random luminous-region point (as in p5,
  which used the signal vertex) or a PU vertex. The choice changes the near-PV single-interaction (∝ ρ) term of B-4.
- **C-13. Verified as claimed** (no action):
  - Fatras `pMin = 0.03 GeV` in p1/p2/p3.
  - Molar densities in mol/mm³: Si 8.31 × 10⁻⁵ against 2.329/28.0855 = 8.29 × 10⁻⁵; Be 2.051 × 10⁻⁴. X₀ and λ_I are PDG
    values.
  - HANDOVER §4 items: `doMerge = False` explicit, T3V skipped, one ACTS event per physics event (`ev_simhits[ctx.eventNumber]`),
    p4_after from `h_dE` (p2 l.90-94).
  - Counting set 61 344 / 55 921 and 69.4 % with |η_pair| > 1 (`events_p2.npz`).
  - The 7.2/28.9/423 µm, 26.0 µm and 14.5 mm pitch/√12 values.
  - The §2.1 band-occupancy arithmetic (per sensor; see B-2).
  - Template/toy disjointness in A2/A3. The PU seeds must include spin|m (as Stage-3's vertex seed does) for "different masses
    use different PU" (l.381) to hold, because row indices repeat across mass files.

---

## Verdict

**ITERATE.** 1 Category A, 10 Category B, 13 Category C.

The A item and the B items need text or design changes to the plan. The only reruns needed are cheap pre-production probes:
a blind p5 re-run, the V4-2 benchmark, and the G3 pilot. The chain and injection work (geometry contract, `doMerge`, T3V,
per-event injection, `h_dE`, units, sectoring) is sound and VERIFIED as claimed.

Category A: A-1 (the frozen F0 shape contains Δw < 1 cm, which rejects 100 % of the probe's signal candidates and 74-88 % of
truth-level central E1000/Ẽ500 events at 1 keV).
