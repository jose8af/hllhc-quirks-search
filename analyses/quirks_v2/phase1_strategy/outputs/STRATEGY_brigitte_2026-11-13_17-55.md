# STRATEGY — HL-LHC electroweak quirks, study v2 (Phase 1, JFC)

Executor: Brigitte, 2026-11-13 17:55. Plan: `plan_brigitte_2026-11-13_17-55.md`. Arithmetic: `../src/strategy_budget.py`.
Status: for the 4-bot review and then the user's Gate A. Nothing here has been produced yet except the feasibility benchmarks.

**Paths.** `REPO` = `/home/users/jdochoa/hllhc-quirks-search`; `QV2` = `analyses/quirks_v2`;
`TT` = `stage2_C001_quirks/theory_track`; `S4` = `TT/acts/stage4`; `AN1` = `TT/data/acts_stage4/analysis/C12FC_v1`;
`SUM` = `TT/data/acts_stage4/analysis/STAGE4_SUMMARY.json`; PLAN = `publication_plan/publication_plan.tex`;
D1…D6 = the digests in `outputs/digests/`; FEAS_A/B/C = the reports in `outputs/feasibility/`.

**Tags.** **[V]** VERIFIED: I read the number at the cited file:line or JSON key in this session, or re-derived it
(the script line is given). **[E]** ESTIMATE, with the arithmetic. **[U]** UNVERIFIED: transcribed from a digest or a
v1 document and not opened by me. A number without a tag in a table inherits the tag in the table caption.

**Labels.** Constraints are **[A1…]**, limitations **[L1…]**, strategy decisions **[SD1…]**. The prefix SD is used
because "D1–D10" are the user's fixed decisions in the brief (written here as "brief D1") and "V1–V13" are the
deviations in `DEVIATIONS.md`. Downscope proposals that need the user's approval at Gate A are **[DP1…]**; downscopes that
would only be triggered later by a failed attempt are **[DT1…]**. All labels are indexed in §7.

**v1 efficiencies.** No v2 signal efficiency is computed or assumed anywhere in this document. Where a signal
efficiency is needed for planning, it is a v1 number from the tracked record and is written "v1 placeholder".

---

## 0. Summary

- **What v2 is.** A simulation-only search projection for electroweak quirks in a Phase-2-like barrel tracker at
  pile-up 200 and 3 ab⁻¹. The final result is the expected 95 % CL limit on the signal strength on the 40-point
  (m_Q, Λ) grid and the mass reach as a function of the background, with the v2 background *estimate* marked on it.
  v1 ended with zero-count bounds 7.05 decades above its budget [V: `SUM` → `ladder.SR-G.min_B84` = 1.2346×10⁶,
  log₁₀(1.2346×10⁶/0.11) = 7.05, script]. v2 replaces the bounds by estimators with closure tests fixed in advance.
- **Cost.** All MUST items at the statistics their criteria need cost **≈ 2,950 CPU-h** on the lab cluster [E, §11];
  the SHOULD items add 848 CPU-h in full or 326 CPU-h in the reduced form proposed here. Total **≈ 3,280 CPU-h**
  (≈ 3,930 with a 20 % contingency), against the plan's 3–8k M3/cloud CPU-h, which cannot be converted (FEAS_A §3.2
  measured maxwell/M3 ratios from 0.67 to 3.35 depending on the code [V]).
- **Calendar.** With 12 worker cores (9 on weekday daytime) and a realistic utilisation the cluster gives about
  **160 effective core-h per day** (130 in development phases, 200 in production) [E, §11.1]. The study then takes
  **about 6 weeks from Gate A to Gate C (range 5–8)**. **The 2–4 week target of brief D6 is not reachable at the
  statistics the MUST criteria need**; §11.6 lists what a 4-week schedule would cost.
- **Storage.** About **360 GB** on cajuela, 560 GB if the pre-merge candidate store reaches its cap, against the 1.5 TB
  soft budget [E, §11.4].
- **Proposals for Gate A.** [DP1] B5 with 8 roads on 6,000 events instead of 20 roads on 8,000; [DP2] B6 on a reduced
  point set; [DP3] no MVA as the primary selection (a BDT cross-check in the regime where the background can be
  counted); [DP4] S4 and S5 not included; [DP5] Herwig comparison only at generator level and only if it installs
  without a source build. Decisions flagged for the human are in §12.

---

## 1. Physics motivation, model, signature, observable

**Question.** Can a central tracker at the HL-LHC (14 TeV, 3 ab⁻¹, ⟨μ⟩ = 200) find electroweak quirks, and up to which
mass, once the background is estimated instead of bounded?

**Model.** The benchmark is E = (1,1)₋₁: a vector-like Dirac fermion, SU(2)_L singlet with hypercharge −1, in the
fundamental of an SU(2) infracolour group (N_IC = 2), pair-produced by Drell–Yan. The alternate is the scalar Ẽ with
the same charges (FRAMING l.13-17). With no light infracoloured matter the pair stays bound by a string of tension
σ = Λ². For Λ of 0.5–10 keV the pair oscillates over mm to cm and its hits lie in a thin plane through the primary
vertex (a "ribbon") instead of on helices.

**Grid.** The v1 detector grid is kept: {E 200, E 500, E 1000, E 1500, Ẽ 500} × Λ ∈ {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV
= 40 points [V: `S4/run_g1b.py` l.12, l.48]. **[SD1]** No point is added: a grid change would need new admissibility
tables, which rest on Stage 3 at Λ ≥ 15 keV (D4 I4), excluded by brief D8.

**Signature and trigger.** Missing transverse momentum from initial-state radiation: pT(QQ̄) > 200 GeV at generator
level, then an offline requirement MET > 250 GeV, one jet with pT > 100 GeV and min Δφ > 0.5 (D5 §4, [U]
`S4/analysis/products.py` l.43-52). Standard tracking (CKF) removes helical tracks; the plane finder then searches the
remaining hits for a plane through the primary vertex aligned with the missing-momentum direction.

**Observable and discriminating variables.** The search is a counting experiment in two categories per selection:
SR-T (a late hit in the barrel timing layer) and SR-G (the rest). The candidate-level variables are those of the v1
ladder [V: `S4/WP_RULE.md` §3 as transcribed in D4 §1.2, and l.106 fixed cuts]:

| variable | meaning | rungs |
|---|---|---|
| N_IT2, N_IP2, N_2S2 | number of pixel / pixel+PS / 2S barrel layers with at least two crossings in the plane | fixed cut, R01–R04, R12–R14 |
| w_core | in-plane width of the core hits | R05–R08 (37.5 → 4.7 mm) |
| p(χ²_core) | out-of-plane fit probability | R09–R11 |
| h, o | "not a helix" and "not two straight lines" χ²/ndf | R15–R20 |
| dE/dx | truncated pixel charge | R21–R23 (not used in v2, [SD9]) |
| Δφ(n₃, MET), η(n₃), f_CKF | plane–MET alignment (< 0.15 rad), barrel (\|η\| < 1), share of hits on CKF tracks (< 0.2) | fixed cuts |
| late BTL hit | time tag | category |

**Final statistical result.** (i) Expected CLs upper limits on μ = σ/σ_norm at each grid point, from a pyhf
profile-likelihood model (T1) at the selection chosen by the pre-registered rule (T2). (ii) The expected mass reach as
a function of an assumed background B and its width (the curve of book Table 29.2 redone in pyhf), with the v2 estimate
marked. (iii) The background ladder: v1 bounds against v2 estimates with their closure verdicts. There is no observed
limit: there is no data [A1].

**Analysis type.** Search, simulation only. Blinding (STUDY OVERRIDES): no v2 signal efficiency is looked at before
the background closure verdicts are recorded.

**Signal yield formula.** N_exp = σ_norm · f₂₀₀ · L · A and S = N_exp · ε_sel (book ch25:40 via D3 §2 [U]).
Substitution check with v1 numbers [V: `SUM` → `fallback_points.A2|F|200|1.5|BM` via D4 §4.3; script]:
219.2 fb × 0.04764 × 3000 fb⁻¹ × 0.5035 = 15,774 events; × 9/200 = 710; μ₉₅/N_exp = 1.2458×10⁷/15,775 = 789.7.
Limiting case: ε_sel → 0 gives S → 0 and no limit, as at the seven v1 points with ε = 0.

---

## 2. Backgrounds

v1 model [V: `S4/WP_RULE.md` l.313]: **B = N_trig × [P_PU + P_SM,HS + Σ_t rate_t × P(pass | t)] + B_cosmic + B_halo**,
with N_trig = 4.0848×10⁷ ± 2.0 % triggered events in 3 ab⁻¹ (D4 §2.1, `AN1/bsum_wp.json` → `n_trig` [U]).

Table 2.1. Classification, v1 size (SR-G, events in 3 ab⁻¹; all from D4 §2.3, which read `AN1/bsum_wp.json` [U by me];
"b" = zero-count bound) and the v2 estimator.

| term | class | R04 | R06 | R07 | R09 | v2 estimator (item) |
|---|---|---|---|---|---|---|
| Pile-up random planes | instrumental (combinatorial) | 1.05×10¹⁰ | 3.8×10⁷ | 1.35×10⁵ | 252 b | repaired thinning + independent occupancy model, both closed against direct counts (B2) |
| Decays in flight (π, K kinks) | reducible | 2.1×10⁷ | 3.0×10⁵ | 1.5×10⁵ | 1.7×10⁵ b | Geant4 vertices → Fatras; P_geo × C_PU; conditionals (B1, B3) |
| Prompt pairs from the hard vertex ("PV pairs") | reducible | 3.0×10⁶ | 1.4×10⁵ b | 1.4×10⁵ b | 1.4×10⁵ b | P_geo × C_PU on large no-PU samples; "not two straight lines" conditional (B1, B3) |
| Photon conversions, V⁰ | reducible | 4.7×10⁶, 3.7×10⁶ | 4.0×10⁵, 3.1×10⁴ | 7.4×10⁴, 5.8×10³ b | 6.5×10³ b, 5.8×10³ b | same, plus displaced-vertex veto (B1, B3) |
| Nuclear interactions (r = 22, 30, 61.5 mm) | reducible | 1.7×10⁵–1.2×10⁶ | ≈ 2–3×10³ | ≈ 3×10³ b | ≈ 3×10³ b | Geant4 (real hadronic physics), vertex veto (B1, B3) |
| Loopers | reducible | 168 b | 168 b | 168 b | 168 b | no-PU sample ×100 (B1) |
| Z(νν)+jets hard-scatter tracks | **irreducible** (real MET, tracks in the road) | 1.2×10⁹ | 9.6×10⁵ | 1.6×10⁴ b | 1.6×10⁴ b | hit-level sample ×5; factorised hard-scatter estimator (B4) |
| W(τν), tt̄ 1ℓ | irreducible/reducible | 1–2.4×10⁸ | 0.5–1×10⁵ | ≈ 10⁴ b | 0.2–9×10³ b | hit-level samples; same estimator (B4) |
| 8 proxied processes (W(eν), W(μν), tt̄ 2ℓ, t-channel, tW, WW, WZ, ZZ) | irreducible/reducible | 2.8×10⁸ | 2.2×10⁵ | 2.3×10⁴ b | 2.1×10⁴ b | own hit-level samples (B4) |
| Z(ττ), lost-lepton Z(ℓℓ), multijets with fake MET | reducible / instrumental (fake MET) | absent | absent | absent | absent | new, with a reconstruction-level MET model (B4) |
| Cosmic muons, beam halo | instrumental (non-collision) | argued, not in the sum | | | | number from public rates × pointing × timing (B7) |
| **B₈₄ total SR-G** | | 7.5×10¹⁰ | 1.5×10⁸ | 2.0×10⁶ | 1.2×10⁶ | pyhf model (T1) |

Readings that shape v2:
- The pile-up term dominates down to R06. From R07 on the leading terms are single-interaction and SM bounds that do
  not scale with pile-up (D2 §8.1). B1/B3/B4 therefore matter at least as much as B2; the v0.4 statement that a
  data-driven *pile-up* estimate is "the decisive item" is not repeated.
- The bounds are not "1.14/M with M = 500–2000" (PLAN l.76). They are applied to conditional populations of
  M = 13 (γ), 24 (PV pair), 35 (PU), 81 (DIF, Z(νν)) up to 2,000 (D4 I6 [U]). The paper wording follows the record.
- "Measured down 4.9 decades from R04 to R07 by direct count" (PLAN l.167) is the patched central value. The direct
  count falls 5.37 decades (171.55 → 7.29×10⁻⁴ per trial), and at R06 and R07 it lies ×3.8 and ×4.5 *below* the
  patched value (D4 I7 [U]). v2 quotes the direct counts.
- SR-T and SR-G carry identical SM and single-interaction terms in v1: no time-tag credit was given
  (D4 §2.3 [U] `STAGE4_RESULTS.md` l.172). v2 measures this credit as a conditional ([SD6], item B3).

---

## 3. Technique justification and selection approaches

**3.1 Why a cut ladder with estimators, and not template shapes.** The signal is defined by layer-multiplicity and
geometric quantities of one candidate per event. The backgrounds that matter have rates of 10⁻⁹–10⁻⁴ per trial, far
below what direct simulation can count (direct counts stop near 7×10⁻⁴ per trial at R07). Any selection is therefore
only as good as the *extrapolation* of its background. Counting cuts on layers, a width cut and a fit-probability cut
are quantities for which independent extrapolations exist: exact thinning of a denser sample acts on hit counts; an
occupancy model predicts the probability of two unassociated hits per layer in a ribbon; a geometric probability
without pile-up can be measured on 10⁷ events at 11.5 ms each [V: FEAS_A §3.6]. This is the technical reason for the
ladder.

**3.2 Approaches that will be compared (JFC: at least two, one MVA-based, or a documented infeasibility).**

| # | approach | status | figure of merit |
|---|---|---|---|
| A | v1 ladder rungs and the v1 fallback, as fixed selections | candidates of T2 | expected μ₉₅ on the optimisation half |
| B | sensitivity-based choice among the declared selections with a vertex veto and a time-tag split (T2) | primary | same |
| C | BDT on candidate-level variables | **cross-check only** [DP3] | signal efficiency at equal *directly counted* background rate |

A and B share their variables, so they are parametric variants and count as one approach under JFC. The qualitatively
different approach is C.

**[DP3] MVA not used as the primary selection; implemented as a cross-check.**
- *Inputs available:* N_IT2, N_IP2, N_2S2, w_core, χ²_core, h, o, Δφ(n₃, MET), f_CKF, the time tag, hits per layer.
- *Constraint.* A cut on a classifier score needs a background estimate at a rate of 10⁻⁹ per trial or below. The
  three estimators of v2 are built on the structure of the cuts (thinning acts on per-layer hit counts; the occupancy
  model on per-layer probabilities; P_geo × C_PU on conditionals of named cuts). None of them applies to an arbitrary
  score, and a score cut can be closure-tested only where direct counts exist, i.e. down to about 10⁻³–10⁻⁴ per trial
  (R06–R07), five to six decades short of the working region. The training sample has the same problem: in v1 no
  background event survives beyond R08 in any sample [U: D4 §2.3], so there is nothing to train on in the region that
  decides the limit.
- *What is done instead (binding).* After the closure verdicts and Gate B, a gradient-boosted classifier is trained on
  the signal optimisation half against the directly counted background candidates passing R06, with a recipe fixed in
  the pre-registration (inputs above, default hyper-parameters, one alternative architecture as JFC asks). Its
  working point is the score cut whose *directly counted* pile-up rate equals that of R07. The comparison quantity is
  ε_BDT/ε_R07 on the evaluation half at equal counted background.
- *What is foregone.* That ratio is the measured gain an MVA could give in the regime where it can be validated; it
  is reported in the paper as the estimate of the sensitivity not used. It cannot be converted to a limit, because
  the BDT background at the working region cannot be estimated.
- *Deviation from JFC Phase 3.* JFC compares approaches in Phase 3. Here Phase 3 is signal-blind, so the comparison
  moves to Phase 4c. This is recorded as [SD2] and needs the reviewers' validation.

**3.3 Channels (JFC 09).** One channel (barrel), two orthogonal categories (SR-T, SR-G) split by the time tag. Shared
nuisances are listed in T1. The endcap is not a channel (brief D1).

---

## 4. Per-item strategy

### 4.0 Unit costs and conventions used in every item

Table 4.0. Measured unit costs on a worker (i5-7500), at 4 jobs per node. [V] = measured in the feasibility phase;
the JSON keys are in `benchmarks_chain.json`, `benchmarks_generators.json`, `benchmarks_runner.json`.

| unit | cost | max RSS | output | source, tag |
|---|---|---|---|---|
| PU-200 event through the chain (Pythia overlay, Fatras, digitisation, seeding, CKF) | 13.5 ± 1.1 s (12.9 s alone) | 0.46 GiB | 0.52 MB with 4 trials | FEAS_A §3.3 [V] |
| plane-finder trial at ρ = 1, road 0.25, all per-trial work | 11.7 ± 1.1 s (find alone 10.8 s; 9.4 s with 1 job) | same job | — | FEAS_A §3.4 [V]; at the frozen road 0.15 perhaps ×0.77 [E, not measured] |
| "B1-type" event = chain + 4 trials | 60.4 s | 0.46 GiB | 0.52 MB | FEAS_A §1 [V] |
| ρ = 2 event (2 crossings, 2 trials) | 206 s | **1.46 GiB at 1 event** | 4.0 MB with dumps | FEAS_A §3.1, §3.7: one smoke event [E] |
| signal row, full chain + 1 trial | 25.2 s = 13.5 + 11.7 | 0.46 GiB | ≈ 0.5 MB | sum of measured parts [E]; the injection mode itself is not benchmarked (FEAS_A open issue 6) |
| no-PU single-interaction event | 11.5 ms | grows 12.6 kB/event | 8.2 kB | FEAS_A §3.6 [V] |
| Stage-3 string event, F 500, Λ = 1 / 3 / 5 keV | 0.65 / 18.8 / 67.8 s | 0.21 GiB | 4–8 kB | FEAS_A §3.5 [V], toy kinematics |
| Stage-3 event summed over the 8 grid Λ | 95.6 s | | | measured anchors (91 % of the sum) + v1 index shape × 2.14 for the other five Λ [E, script] |
| MG5 LO + Pythia shower + conversion | 34 ms per LHE event | 0.2 GiB | 0.72 + 1.05 kB | FEAS_B summary 6 [V]; MLM 0–2 jets **not benchmarked**: 50 ms assumed [E] |
| Pythia (re-)shower | 21 ms per event | 29 MB | — | FEAS_B Task 3 [V] |
| NLO fixed-order K at one mass | ≈ 2 CPU-min (+ 3 CPU-min once per process) | 1.0 GiB | — | FEAS_B Task 4 [V], single runs |
| Geant4 π± gun, primary mode | 0.134 ms | 71 MB | — | FEAS_B Task 5 [V] |
| pyhf: fit / asymptotic CLs point / 20-point scan / 1000 toys | 0.12 / 0.52 / 10.4 / 652 s | 105 MB | — | FEAS_C R9 [V], toy workspace with 31 parameters |
| Argo overhead per job / SSH | 16.8 s / 2.4 s | — | — | FEAS_C R2 [V] |

"CPU-h" below means slot-hours at these costs. The Stage-3 number for unmeasured Λ uses the v1 per-event CPU of the
tracked index (F 500, p2/BM: 0.037, 0.080, 0.212, 1.07, 2.53 s at 0.45, 0.6, 0.85, 1.5, 2 keV [V: `STAGE3_INDEX.json`,
read this session]) times the ratio measured at the three anchors (87.3 s / 40.8 s = 2.14). These five Λ values carry
9 % of the sum, so the interpolation is not what limits the estimate; the toy kinematics and the ×5–10 event-to-event
spread are (FEAS_A §3.5).

**Common definitions for closure criteria.** For a prediction P and a direct count N with exposure T, r = P·T/N and
z = ln r / √(s_P² + 1/N), with s_P from the event bootstrap. A closure criterion of the form "within a factor F" means
all of: (a) |ln r| ≤ ln F at every rung where N ≥ 20; (b) the χ² of the ln r values against zero, with variance
s_P² + 1/N + s_model², has p > 0.05, where s_model is the systematic width *declared for that estimator in the
pre-registration and used unchanged in the likelihood*; (c) s_model ≤ ln F. Condition (b) is the conventions'
p > 0.05 closure test. Condition (c) forbids passing by inflation. Limiting cases: s_model → 0 reduces (b) to a pure
statistical compatibility test; N → ∞ with r = 1 gives χ² = 0, and JFC's alarm band applies (χ²/ndf < 0.1 is
investigated as a possible tautology). A failed criterion is reported as failed. The estimator is then not used for a
selection that depends on it ([SD8]); it is not patched by a scale factor as v1 did with ×2.41.

### 4.1 C1 — port and reproduction of v1 (MUST, Phase 2)

**Method.** The chain already runs on linux-64 with the pyacts 48.0.0 wheel and no API change (FEAS_A §2.3 [V]).
C1 reruns the v1 code with the logged port edits (FEAS_A §2.4; `QV2/CHAIN_PROVENANCE.md`) and the operative frozen
configuration, T_seed = 4 and road 0.15 [V: `S4/frozen_inputs.json` l.17, l.37-38], on the subset below, and compares
with the tracked `C12FC_v1` numbers.

**Corrections to the plan and to D4.**
- PLAN l.265 "bring the 46 GB back": the data are lost (brief §0). C1 is a regeneration.
- D4 §5.1 proposed bit-level Stage-3 comparisons and "the same 200 rows". Neither is possible: the Stage-2 events
  must be regenerated, the v1 LHE files are lost, and nothing shows that MG5 reproduces the same event stream on
  another platform. ACTS random streams also differ between libc++ and libstdc++ (FEAS_A §3.2 [V]). **Every C1
  comparison is statistical and unpaired** [A2]. The kernel-level identity is already covered: Stage-1 numerics agree
  with v1 to ≤ 1.2×10⁻⁷ relative except one conformal run (FEAS_A §3.2 [V]).
- Lost frozen inputs (D4 I4): the admissibility tables and δ₉₅ = 0.15 are used as the frozen transcriptions in
  `WP_RULE.md` A.1/A.2b and `frozen_inputs.json`. They cannot be regenerated without Stage 3 at Λ ≥ 15 keV [A3].
- The probe-row exclusion file `fix_r1/f1r_summary.json` is lost (D1 §5). The ported code now raises instead of
  silently skipping it (FEAS_A §2.4). Phase 2 must decide, from the tracked row arrays `AN1/signal_rows_a2.npz`,
  whether the exclusion can be reconstructed; if not, C1 states that its signal denominators include probe rows that
  v1 excluded, and the comparison uses the v1 counts over the v1 denominators as recorded.

**Declared comparison subset (brief D5).** v1 values from D4 §5.2 (read there from the JSON; [U] by me except where
marked). N = 41 scalar comparisons.

| family | quantity | v1 value | v2 sample | n |
|---|---|---|---|---|
| PU ρ = 1 | groups per trial at R04, R05, R06; count at R07 | 171.55, 49.72, 0.2470; 35/48,000 | 4,000 events, 16,000 trials | 4 |
| PU ρ = 2 | ⟨S_ded⟩ per trial at R04, R05, R06 | 114.36, 30.96, 0.389 | 1,000 events, 2,000 trials | 3 |
| PU closure | the failed ratios T1 (R04), T1w (R05); trend slope; c-factor | 1.5001, 1.6061; −0.3608; 1.1964 | same | 4 |
| PU R08, R09 | zero counts: v2 count against v1's 0/48,000 | 0, 0 | same (conditional binomial) | 2 |
| C′₀ (no PU) | f_pre for DIF, NI at 22 mm, PV pair | 0.9495, 0.7593, 0.9031 | v1 sizes | 3 |
| C′_PU | attributed counts at R04 and R05 for DIF, γ, V⁰; PV pair at R02 | 166/81, 153/86, 859/358 per 500; 24/500 | 1,000 events each; PV pair 2,000 | 7 |
| rates | per triggered event: DIF, PV pair, γ; N_trig total and Z(νν) share | 1.5945, 30.31, 0.379; 4.0848×10⁷, 2.508×10⁷ | generator level | 5 |
| SM | Z(νν) hard-scatter candidates per event at R04, R05, R06 | 19.52, 4.51, 0.0162 | 2,000 events | 3 |
| signal E 200, 1.5 keV (fast path) | pass counts at R04, R06, R07; FB2 | 41, 33, 18; 9 of 200 [V: D4 §4.2-4.3] | 400 rows | 4 |
| signal E 500, 3 keV (full chain) | R04, R07; FB3 | 61, 48; 11 of 200 | 400 rows | 3 |
| signal E 200, 2 keV (fast path) | R04, R07; FB3 | 45, 31; 10 of 200 | 400 rows | 3 |
| arithmetic (exact, not in N) | v2 code on the v1 recorded counts reproduces B, σ_ln per term and B₈₄ per rung | `AN1/bsum_wp.json` → `ladder` | — | — |
| Stage 3 (diagnostic, not in N) | hits per event and status fractions at the three points | e.g. 21,137 hits / 463 events at E 200, 1.5 keV [V: `STAGE3_INDEX.json`] | 463–492 events | — |

Rungs R04–R09 of the dominant terms are covered as far as counts exist. From R07 (SM, C′) or R08 (PU) on, the v1
entries are zero-count bounds; there the only possible tests are the zero-count compatibility and the arithmetic row.

**"Within statistical errors" (fixed now).**
1. Per quantity: counts ≥ 10 use z = (ln x₂ − ln x₁)/√(s₁² + s₂²), with the event bootstrap for pile-up quantities
   (trials within an event are correlated); smaller counts and efficiencies use an exact test (conditional binomial
   for two Poisson counts with known exposures; Fisher for k/n). Each gives a two-sided p_i.
2. Individual pass: p_i > 0.05/41 (Bonferroni; |z| < 3.2). Global pass: Σ z_i² below the 99th percentile of χ²₄₁.
   Family coherence: in each family the inverse-variance mean of ln(x₂/x₁) has |z| < 3 (this catches a common drift
   of a few per cent that individual tests miss).
3. Arithmetic row: central values identical to 10⁻⁶ relative; B₈₄ (a Monte Carlo sum) within 1 %.
4. Power is stated with the verdict. With 4,000 ρ = 1 events the detectable shift (2σ) is about 2 % at R04–R05 and
   6 % at R06; R07 has 12 expected counts (σ_ln = 0.29 [E, script]) and is a gross check only; the signal counts
   detect only shifts of 30–70 % (D4 §5.2 [U]). Quantities with a detectable shift above 50 % are labelled "gross
   check only": they can catch a bug, they cannot validate the port.
5. Fail: the family is investigated through a regression ticket, with no tuning. A family failure blocks decision
   point 1. If three documented remediation attempts do not resolve it, C1 is reported as failed for that family and
   the user is asked (brief §7: a MUST item infeasible after a real attempt).

**C1 and blinding (precise statement).** The C1 signal counts are pass counts of *v1 selections* (R04, R06, R07 and
the v1 fallback column) at the three declared points, on about twice the v1 statistics. They are part of the v1
reproduction record, not of the v2 result.
- *May be looked at, in Phase 2:* exactly the ten signal quantities in the table, written by one comparison script.
- *May not be computed or looked at before the closure verdicts:* any other rung count for signal, any distribution
  of a variable for matched signal candidates, the response of the vertex veto or the time-tag split to signal, any
  efficiency at a v2 candidate selection that is not one of the ten, and any signal quantity at the other 37 points.
- *Separation.* The C1 rows use their own seed stream and are never part of the S1 sample. The T2 candidate list and
  figure of merit are fixed in this document, before any C1 number exists, and the pre-registration may only shrink
  that list for a background-method reason.
- *Disclosure.* Three of the ten quantities (the R07 counts) are also efficiencies of a v2 candidate selection. The
  paper states this. Their precision (400 rows) is close to that of the v1 record (200 rows), which is public to the
  study. This is the reason the C1 signal sample is kept at 400 rows and not at the 1,000 proposed in D4 [SD3].

**Other criteria.** (i) Linux reproducibility of the environment: lockfiles tracked, container recipe built and one
C1 job rerun inside it with identical output hash. (ii) Jobs ≤ 30 min, resumable, through `tools/runner` (FEAS_C PASS).
(iii) Pythia pinned to 8.312 for pile-up and SM, 8.313 for the signal shower, as v1 (D1 §2).

**Statistics and cost.** 192 CPU-h [E]: ρ = 1 4,000 × 60.4 s = 67; ρ = 2 1,000 × 206 s = 57; C′_PU 5,000 × 25.2 s = 35;
Z(νν) 2,000 × 25.2 s = 14; signal 1,200 × 25.2 s = 8; Stage 3 at three points 3.6; no-PU 1.7; generator level 5.
The ρ = 2 jobs also write the pre-merge candidates (an addition that does not change the v1 outputs), so the same
1,000 events are the development sample of B2. **Storage:** 13,200 PU events × 0.52 MB ≈ 7 GB.
**Dependencies:** Stage 2 at three mass points; runner. **Risks:** ACTS navigation assertion (about 1 in 700 events in
v1, D6 §5 [U]) → the v1 per-event seed replacement is kept; ρ = 2 memory (see B2).

### 4.2 C2 — finder cross-checks (MUST, Phase 2)

The plan's "seed-threshold regression (V4-4)" conflates two v1 items (D4 §6). I opened the v1 plan:
V4-4 is "Reproducibility and seeds", V4-5 is the brute-force cross-check [V: `S4/plan.md` l.1811-1812]; the
seed-threshold stability rule is a third item [V: `S4/plan.md` l.503-510]. C2 runs all three.

| test | definition | pass criterion | fail leads to |
|---|---|---|---|
| **V4-5** brute force | 50 signal + PU events and 50 PU-only trials. For each: an exhaustive scan of plane normals through the primary vertex on a 0.2 mrad grid within ±0.3 rad of the F0 normal, plus a 5 mrad global scan over the road, maximising the resolution-weighted inlier count; and an independent least-squares plane fit on the F0 inliers. Signal events: the first F0-accepted events of the C1 signal rows, in file order, 17/17/16 from the three C1 points. PU trials: the first 50 trials of the C1 ρ = 1 sample with an F0 candidate at R04. | \|Δn\| < 1 mrad between F0 and the brute-force optimum **and** between F0 and the independent fit, in ≥ 48 of 50 signal events and ≥ 48 of 50 PU trials (the v1 "≥ 95 %"); every disagreement inspected and described | reported as failed in §5 of the paper; decision point 1 blocked; regression ticket on the finder; no change of the finder without a new freeze |
| V4-5 optimality (reported, not a pass criterion) | in 50 further signal rows where F0 has no R04 candidate, does the global scan find a plane that would pass the R04 counting? | number reported; answers "near optimal?" (referee Q9) | — |
| **V4-4** reproducibility | 20 production-type jobs rerun on the same node; the same 20 on a second node; two jobs with different seeds | outputs bit-identical on the same node; cross-node identity reported (same CPU model); different seeds give different outputs; all seeds in the markers | failure on the same node blocks production (non-determinism) |
| **T_seed stability** (4 → 2) | the G3 metric of v1: per-trial pass fraction of each rung family (counting R04, width R05–R06, χ², 2S) at T_seed = 4 and 2, on 500 ρ = 1 events (2,000 trials) and 200 ρ = 2 events, from stored hit dumps | \|z\| < 2 for every family at both densities | T_seed stays 4 (no retuning in v2); the paper reports "seed threshold not converged, pass fraction changes by x %" as a limitation; the same finder is applied to signal and background, so this is an efficiency statement, not a bias |

Power of V4-5 [E, script]: if the true agreement were 85 %, 48 of 50 would be reached with probability 1.4 %; at 90 %,
11 %; at 98 %, 92 %. The test can therefore reject agreement below about 85–90 % and no better; this is stated with
the verdict. Blinding: V4-5 uses only F0-accepted events of the declared C1 rows and reports a direction difference;
no efficiency is formed (the "optimality" count is taken on C1 rows and concerns the v1 rung R04 only).

**Code status.** No V4-5 code exists (D4 §6, D5 §6 [U]). It must be written: a numba scan and a scipy fit, independent
of `finder.py`. **Cost:** 81 CPU-h [E]: V4-5 100 events × 0.3 CPU-h (9×10⁶ normals × hits in the road; to be timed on
one event first); T_seed 44; V4-4 7. **Dependencies:** C1 samples with dumps for 700 events.

### 4.3 C3 — paper corrections (MUST, Phase 5; list frozen now)

**Method.** The plan names seven errors (PLAN l.241-251). The binding list is longer: all 24 items of D3 §1
(`book/review/UNRESOLVED.md` l.45-74 plus three book-only items), the 19 internal-label families of D2 §5, the
novelty wording of the audit (claim N1, N3, N4 only, each "to our knowledge"; D2 §3), and the statements corrected in
this strategy (§2 readings; the 23–30 µm out-of-plane *resolution* is a planning estimate, not a measurement and not
the scattering floor, D3 §1 item 19).
**Criterion.** (i) A checklist `C3_CHECKLIST.md` with one row per item, each closed with the file:line of the new
text. (ii) A grep of the v2 paper sources for every label family of D2 §5 returns zero hits. (iii) Items on frozen v1
files are listed in one `ERRATA_v1.md`; the frozen files are not edited. (iv) Two items need a primary-source check
before the text is rewritten (Barbashov's solution class; the content of Knapen et al. Sec. III.D): done from the
papers and logged in `retrieval_log.md`. For Knapen et al. the audit already records, from the PDF, that the paper
treats beam-pipe conversions and not the other topologies (`TT/paper/P2_NOVELTY_AUDIT.md` §1.1 [V: read this session]).
(v) Every number in the paper carries a measured / estimated / unverified tag. **Fail:** an open row at Gate C blocks
the gate. **Cost:** no CPU. **Dependencies:** all results.

### 4.4 B1 — single-interaction topologies with hadronic physics (MUST, Phases 3 and 4a)

**Method.**
1. *Physics.* Geant4 11.4.3 with FTFP_BERT on the same cylinders, discs and slabs as the ACTS geometry, generated from
   the one tracked source `TT/acts/geometry/cms_phase2_public.json` (FEAS_B "Geant4 build and integration plan").
   Geant4 tracks each primary (π±, K±, p, K⁰_L, n, γ) in 3.8 T and records every inelastic interaction, decay or
   conversion with all products. Geant4 runs per worker from local scratch (deviation V13).
2. *Hand-over.* The products are written as rows of the v1 particle array (vp, vsec, pdg, q, m, x, y, z, t, px, py,
   pz), which v1's `ParticleSource` already injects into Fatras with their own vertex (D5 §5 [U] `run_chain.py`
   l.79-112). The parent's hits up to the vertex come from Fatras with v1's `Truncate`. The finder therefore sees the
   same detector model as everywhere else. Two hand-over variants (Fatras-truncated parent; Geant4 parent crossings
   converted to hits) are compared on 100 events in Phase 3 and one is frozen.
3. *Estimator.* For topology t and selection r: **P(r | t) = P_geo(r | t) × C_PU(r | t)**. P_geo is the pass
   probability of the topology without pile-up, measured on large samples (4×10⁷ events in total). C_PU is the ratio
   of the pass probability with pile-up overlaid to that without, measured by overlaying no-PU events that pass a
   loose rung on independent pile-up events (2,000 per topology), at rungs where both have counts.
   Check by limiting case: with no pile-up C_PU = 1 and the estimator is the direct no-PU count.
   The background term is B_t = N_trig × rate_t × P(r | t), as in v1.
4. *Biased generation.* Only stiff configurations can pass a ribbon width of 4.7–9.4 mm. Primaries are sampled with a
   known weight that favours high pT and directions inside the road, and Geant4 cross-section biasing (factor k,
   weight 1/k) is used in the tracker volumes. The soft bulk is covered by an analytic sagitta bound: a prong of
   transverse momentum pT leaves a sagitta larger than the width cut over the lever arm unless pT exceeds a threshold;
   the bound is *validated* on the unbiased sample at R05–R06, where counts exist, before it is used. The bias
   weights are checked by a closure of biased against unbiased generation at R05 (same criterion as below).
5. *Rates.* rate_t per triggered event is recomputed from Geant4 on the Pythia particle spectra and compared with
   the v1 generator rates (DIF 1.59, NI 0.10–0.12 × 0.22, γ 0.38, V⁰ 0.052 per triggered event, D2 §2 [U]).

**Acceptance criteria.**
- **B1-a closure.** For each of the eight topologies, the factorised prediction closes against the direct count on
  full pile-up samples of that topology **within a factor 2** (definition of §4.0, F = 2) at each of R05, R06, R07
  where the direct count is ≥ 20. The factor 2 is chosen because the central target is a total width σ_ln ≲ 1
  (PLAN l.129-131) and ln 2 = 0.69 leaves room for the rate and material terms.
- **B1-b trend.** The slope of ln r against the rung index over the rungs with counts is compatible with zero
  (|slope| < 2σ) or its extrapolation to the chosen selection is added to the width in full. v1's thinning had a
  slope of −0.36 per rung (D4 §3.3 [U]); a stable transfer is what the conventions' "transfer factor instability"
  pitfall asks for.
- **B1-c rates.** Geant4 and v1 rates agree within a factor 2 per topology, the size of the material band (×0.5–×2).
  Outside it the cross-check is reported as failed and the Geant4 rate is used with the difference as a nuisance; the
  v1 number is not restored.
- **B1-d geometry.** Material scan Geant4 against the ACTS material map: |Δ(x/X₀)| ≤ 1 % per layer; radii and
  z-extents equal to 1 µm.
- **B1-e Fatras physics.** Before B1 relies on "Fatras has no hadronic interactions", the physics list actually
  active in pyacts 48 is printed and recorded (it was never set explicitly, D5 §7.7). If hadronic interactions are
  on, they are switched off for B1 so that nothing is counted twice.
- **Fail** of B1-a for a topology: its term is reported as failed; selections for which that term is among the
  leading ones are not eligible in T2 ([SD8]).

**Statistics.** Direct closure samples: 6,000 events each for DIF, PV pairs and γ, 1,000 for the other five. v1 had
1–2 counts at R07 in 500 events for DIF and γ (D4 §2.3), so 6,000 events give about 12–24; R07 is therefore at the
edge of the ≥ 20 rule and R05–R06 carry the test [L1]. P_geo: with 10⁷ events per leading topology a zero count
bounds P_geo at about 10⁻⁷, i.e. about 8 events for decays in flight (6.5×10⁷ in 3 ab⁻¹ × 1.2 × 10⁻⁷) before C_PU and
the conditionals of B3, against 1.7×10⁵ now [E from D4 §2.3 values].
**Cost.** 481 CPU-h [E]: development 60; Geant4 20 (10⁸ guns × 0.134 ms = 3.7 CPU-h, ×5 for realistic spectra, discs
and I/O); no-PU 4×10⁷ × 11.5 ms = 128; overlays 16,000 × 25.2 s = 112; direct 23,000 × 25.2 s = 161.
**Storage.** No-PU events cannot be stored in full (8.2 kB × 5.5×10⁷ = 451 GB [E]); jobs write a per-event summary
(rung flags and key variables, about 50 B) and full records only for events passing R04: ≈ 18 GB [A4]. No-PU jobs
are limited to 80,000 events by memory (FEAS_A §3.7).
**Dependencies.** Geant4 installed on landau and maxwell from the tracked lock (one install slot each); C1 chain.
**Risks and fallbacks.** (1) Material composition: the slabs are Si-equivalent in X₀, but nuclear interactions scale
with λ_I (FEAS_B) → a composition variation (Si against a C/Si/Cu mixture at equal x/X₀) is run and enters as a
nuisance [L2]. (2) Hand-over of the parent's hits → two variants compared. (3) If the zeros do not persist in the
large samples, the paper reports the measured irreducible single-interaction background (plan outcome "real
background"); that is a result, not a failure. [DT1] If Geant4-to-Fatras hand-over fails after three documented
attempts: Geant4 is used for the vertex kinematics only, with Fatras propagating all products from the vertex and no
parent truncation, documented with its bias.

### 4.5 B2 — pile-up: repaired thinning and an independent occupancy estimator (MUST, Phases 2–4a)

**What failed in v1.** The thinning prediction (ρ = 2 → 1) under-predicted the direct per-hit-set counts by 1.50 at
R04 and 1.61 at R05, and over-predicted them at R06 and R07 (ln r = −0.455, −0.954) (D4 §3 [U]). The diagnosis is the
candidate grouping: candidates sharing at least half their hits form one group (`group_frac = 0.5`), and at double
density sets merge that are distinct at ρ = 1. In *union* counts the same thinning over-predicts (closure 0.654 at
R04) [V: `S4/g3/G3_REPORT.md` l.77-90]. So the failure is in the definition of what is counted.

**[SD4] The counted object is fixed first.** The estimator of v2 is the per-trial rate of **distinct hit sets after
grouping applied at the target density**. For thinning this means: store the pre-merge candidates at ρ = 2, draw
thinned subsets, and apply the grouping to each subset, so that the grouping always acts at ρ = 1. A
density-independent count (union) is computed as a diagnostic only.

**(a) Repair.** Pre-merge candidates with their hit lists are stored at ρ = 2 for every candidate with N_IP2 ≥ 6
(the R03 level, which the R05 factorisation test needs and v1 did not keep).
**(b) Independent estimator.** A semi-analytic occupancy model: per layer, the probability that a ribbon of given
width and thickness through the vertex and along the road contains at least two unassociated hits, measured from the
hit densities of the ρ = 1 events as a function of radius and η; combined over layers with measured layer-to-layer
correlation factors; and the measured conditional for the fit-probability rungs. It uses no candidate from the
finder, so its systematics are independent of the grouping. v1's 1.196 is *not* such a correlation: it is the largest
ratio over bins of a factorisation test (D5 §7.5 [U] `WP_RULE.md` l.456), so the correlations are measured anew.
No code exists (D5 §6).
**(c) Direct counts.** 24,000 ρ = 1 events × 4 roads = 96,000 trials, independent of the development sample.

**Acceptance criteria.**
- **B2-a.** Each estimator reproduces the direct counts at R04, R05, R06 and R07 **within a factor 1.5** (§4.0,
  F = 1.5). The tolerance is tighter than for B1 because the statistical precision is at the per-cent level at
  R04–R06 and because the pile-up term must be extrapolated furthest.
- **B2-b.** At every deeper rung up to the chosen selection the two estimators agree within twice their combined
  declared width, |ln(B_thin/B_occ)| ≤ 2√(σ₁² + σ₂²), and that combined width is ≤ 1.0.
- **B2-c.** Trend as B1-b.
- **Fail.** No ×2.41-type patch. If one estimator fails B2-a it is dropped and reported as failed; the term then
  rests on the other alone, and B2-b cannot be evaluated, which is itself reported as "pile-up not cross-validated
  beyond R07". If both fail, the pile-up term is validated only up to R07 by direct count and no deeper selection is
  eligible ([SD8]); this is the plan's "closure fails" outcome.

**Statistics.** At the v1 rate 7.29×10⁻⁴ per trial (35/48,000, D4 §2.3), 96,000 trials give about 70 counts at R07:
σ_ln = 0.12, which resolves a factor 1.5 (ln 1.5 = 0.41) at 3σ [E, script]. 12,000 events would give 35 counts
(σ_ln = 0.17). ρ = 2: 3,000 events as in v1, where the bootstrap error at R04–R06 was already below 1 % (D4 §3.1).
**Whether thinning reaches R07** with 6,000 ρ = 2 trials is not known: v1 could not (D4 §2.2). This is tested on the
development sample; if it does not, [DT2] the validated range of the repaired thinning is declared as R04–R06 in the
pre-registration, logged as a [D] with the user informed, and R07 rests on the occupancy model and the direct count.

**ρ = 2 memory: plan to measure, and fallback.** One ρ = 2 event used 1.46 GiB (FEAS_A [V]); v1 recorded 3.9–4.0 GB
at production size (D1 §1 [U]). Workers have 7.5 GiB, no swap, and pods get a limit of 1.5 × the measured RSS.
1. First job of Phase 2: RSS against events per job for 1, 2, 4 and 8 events, one job alone on a node (about 1 CPU-h).
2. If RSS ≤ 1.6 GiB at ≥ 4 events per job: 4 jobs per node. If ≤ 2.5 GiB: 2 per node (2 × 1.5 × 2.5 = 7.5 GiB).
   If up to 5 GiB: one ρ = 2 job per node with two light jobs beside it (7.5 − 1.5 × 3.9 = 1.65 GiB left) [E].
3. Code fallback, to be tried before accepting one job per node: flush candidates to local scratch after every
   trial (needed anyway for the pre-merge store), so that RSS does not grow with events.
4. Schedule effect of the worst case: 3 slots for ρ = 2 → 172 CPU-h take 57 h of wall time while 6 slots stay
   available for light jobs. This is included in the utilisation factor of §11.1.

**Storage, redone.** The plan's "0.4 TB" is a different object: 8×10⁴ loose candidates per ρ = 1 trial × ≈ 5 MB of
variables without hit lists × 8×10⁴ trials [V: `S4/G2A_REPORT.md` l.113-114]. For the object v2 needs, the estimate
is [E]: about 8×10³ candidates per ρ = 1 trial have N_IP2 ≥ 6 [V: same file, l.116]; at ρ = 2 an assumed factor 4–16
(pair seeds scale as ρ², more for confirmations) gives 3×10⁴–1.3×10⁵ per trial; a record of variables plus a hit list
is about 224 B raw, about 110 B compressed; so 3.6–14 MB per trial and **21–86 GB for 6,000 trials**, twice that with
the development sample. Planning value 200 GB, hard cap 400 GB. The factor 4–16 is a guess: the bytes per trial are
**measured on the first 10 ρ = 2 events** before any campaign. If the projection exceeds the cap, the threshold is
raised to N_IP2 ≥ 7 (the R03 records are then lost and the R05 factorisation test is reported as not possible), by a
logged [D].
**Cost.** 594 CPU-h [E]: direct 24,000 × 60.4 s = 403; ρ = 2 3,000 × 206 s = 172; development and measurements 20.
**Dependencies.** C1 (same code), dumps for the occupancy model. **Risks.** As above; the ρ = 2 unit cost rests on
one event.

### 4.6 B3 — conditionals for purpose-built cuts, vertex veto, time tag (MUST, Phases 3 and 4a)

**Method.** In v1 the rungs "not a helix" (R15–R17) and "not two straight lines" (R18–R20) earned no credit against
prompt pairs and kinks, because the single allowed bound per term was spent earlier (D4 §1.3). In v2 each such cut is
a measured conditional probability on the large no-PU samples of B1: P(pass cut | topology, passes the preceding
rungs). Three conditionals are added:
1. the shape rungs h and o, per topology;
2. a **displaced-vertex veto**: no two-prong vertex at transverse radius above a threshold reconstructed from the
   candidate's hits. Its threshold and vertex-quality cut are fixed in Phase 3 from background samples only;
3. **[SD6] the time tag** (late-hit credit, D3 §6.2: missing from the plan). For prompt terms the probability that a
   candidate carries a late barrel-timing hit is measured on the same samples with pile-up; in v1 it was set to 1.
**Criterion (each conditional separately).** The conditional measured without pile-up, times its C_PU, agrees with
the conditional measured directly on the full pile-up sample of that topology at the loosest rung where the direct
sample has ≥ 30 counts before the cut, within a factor 1.5 (§4.0). A conditional that fails earns no credit (it
enters as 1) and is reported as failed. A conditional whose direct sample has no counts is "not testable" and earns
credit only as a measured no-PU number with its statistical (Gamma) constraint, flagged in the ladder figure.
**Blinding.** The veto is designed without v2 signal. Its signal efficiency is unknown until unblinding; for that
reason T2 contains every selection with and without the veto.
**Statistics and cost.** No sample beyond B1 and B4; 30 CPU-h of re-analysis [E]. **Dependencies:** B1.
**Risk.** A quirk pair may itself form two-prong vertices; if the veto removes signal, T2 will not choose it.

### 4.7 B4 — complete the Standard Model background (MUST, Phases 3 and 4a)

**Method.**
1. *Hit-level samples for the eight proxied processes* (W(eν), W(μν), tt̄ 2ℓ, t-channel top, tW, WW, WZ, ZZ): 2,000
   events each, as v1's three real samples. tW has no Pythia 2→2 process (D5 §2) and is generated with MG5 (LO, as
   Z(νν)+jet in FEAS_B Task 2). The proxy share of B_SM was 0.147 at R04 and 0.445 at R09 [V: `SUM` →
   `sm_proxy_fraction_of_B_SM`, R04 value read; R09 from D4 §2.2].
2. *Three additions:* Z(ττ), lost-lepton Z(ℓℓ), multijets with fake missing energy.
3. *Hard-scatter tracks with the factorised estimator* instead of zero-count bounds: P_geo on 10⁶ no-PU events per
   process, C_PU from the hit-level samples, conditionals from B3.
4. *Normalisation.* v1's K = 1.4 (1.9 for tt̄) is neither computed nor cited (D5 §2 [U]). v2 takes each K from a cited
   public calculation (retrieval task R-5, §6.4) and cross-checks the leading Z(νν)+jet rate with MG5: FEAS_B found
   12.21 ± 0.03 pb (MG5 LO, MET > 200 GeV) against v1's 14.6 pb (Pythia 2→2), ratio 0.84 [V: FEAS_B Task 2]. The
   difference between the two generators enters as the normalisation nuisance of the term (conventions: generator
   comparison for the irreducible background).

**The missing-energy model (why and what).** v1 selects events with a truth-neutrino MET > 200 GeV filter
(D5 §6 [U] `S4/analysis/gen_d123.py` l.7, l.58-59). Lost-lepton Z(ℓℓ) and multijets have little or no neutrino MET,
so the filter removes them by construction. v2 therefore defines the trigger and offline MET at reconstruction level:

  MET_reco = | −Σ_jets R_j·p⃗_T,j − Σ_leptons in acceptance p⃗_T − p⃗_T(soft term) |,

with (i) a per-jet response R_j drawn from a public Phase-2 parametrisation with a Gaussian core and a non-Gaussian
low tail, as a function of jet pT and η; (ii) leptons outside the acceptance or failing identification counted as
lost, with public efficiencies; (iii) a soft term representing pile-up, with a resolution that reproduces v1's
25 GeV smearing for events without hard jets mismeasured. Check by limiting case: R_j ≡ 1, no lost leptons and no
soft term give MET_reco = neutrino MET, i.e. the v1 filter. **No parameter value is quoted here**: the jet response,
its tail, the lepton acceptance and the pile-up soft-term resolution are retrieval tasks (R-3, §6.4), to be taken
from public Phase-2 documents with page references, and the model is frozen in the pre-registration.
- *Validation (criteria).* (a) On Z(νν)+jets the reco-MET selection reproduces the yield of the v1 selection
  (truth MET with 25 GeV smearing) within 10 %. (b) The multijet yield after MET > 250 GeV, a jet above 100 GeV and
  min Δφ > 0.5 is stable within a factor 2 when the generation bias (p̂T slicing and weights) is changed, with ≥ 100
  effective events passing. (c) The model's multijet share of the triggered sample is compared with a published
  monojet-type analysis (retrieval task R-4); a disagreement beyond a factor 3 is reported as a failed validation.
- *Systematic.* The tail fraction and the core resolution are varied within the range of the public source; the
  resulting change of N_trig per process is a nuisance correlated across processes. For multijets this is expected
  to be the dominant uncertainty of the term [E].

**Acceptance criteria.** (B4-a) every process of the list has its own hit-level sample; the proxy fraction of B_SM is
zero at every rung. (B4-b) the three additions are in N_trig with the model above and its validations (a)–(c)
recorded. (B4-c) the factorised hard-scatter prediction closes against the direct hit-level count within a factor 2
at R05 and R06 for each process with ≥ 20 direct counts (Z(νν): 81 raw candidates at R06 in 2,000 events in v1, so
about 400 in 10,000). (B4-d) every K-factor has a citation. **Fail:** a process without a sample stays a proxy and is
named as such; a failed MET validation means the three additions are quoted with the full variation as width and
the failure is stated.
**Statistics and cost.** 407 CPU-h [E]: hit level (11 × 2,000 + Z(νν) 10,000 + W(τ_ℓ), W(τ_h), tt̄ 1ℓ 2,000 each) =
38,000 × 25.2 s = 266; no-PU hard scatter 1.5×10⁷ × 15 ms = 63 (the 15 ms is a guess: hard-process generation with a
filter is not benchmarked); multijet generator level 10⁷ × 10 ms = 28; development 50.
**Dependencies.** B1/B3 estimator; MG5 for tW. **Risk.** Multijets need biased generation in p̂T with weights; a few
events with large weights can dominate. Fallback: finer p̂T slices; the effective sample size is reported.

### 4.8 B5 — road-rotation sideband, closed in simulation (SHOULD, Phases 3 and 4a)

**Method.** The data-driven recipe for an experiment: rotate the road away from the missing-momentum direction,
keep every cut, and predict the signal-road count from the sideband roads with a transfer factor T. The simulation
tests the two assumptions never tested: the fake rate is flat in the angle to the MET, and roads in one event are
independent. For pile-up-only candidates flatness holds by symmetry (pile-up does not know the MET direction); the
informative samples are the SM hit-level samples, where jets recoil against the MET and hadronic τ decays lie near it.
**Corrected statement.** PLAN l.342-343 calls the book's B₈₄ ≈ 0.17 "the systematic floor … the width used in the
reach". In the book it is the B₈₄ of an *empty sideband in real data* with 8.2×10⁸ trials and a transfer width copied
from a published search; the width of that estimate is σ_ln = 1.105, and 1.14 × 0.05 × e^1.105 = 0.172 [V: script;
D3 §2, §6.3]. What v2 can deliver is the measured non-flatness and non-independence at R04–R07; the width that enters
the reach curve as "the data-driven scenario" is about 1.1 plus the measured non-closure [L3].
**Acceptance criteria.** (B5-a) Flatness: per process and for the sum, the sideband prediction of the signal-road
count closes within a factor 1.5 (§4.0) at R04, R05, R06, and at R07 if ≥ 20 counts. (B5-b) the non-flat part is
quantified per process as T_meas/T_flat − 1 with its error. (B5-c) Independence: the pair correlation of pass
indicators between roads of the same event is |ρ| < 0.1 at R05 and R06, or an effective-trials factor is quoted.
**Fail:** the paper presents the recipe as a proposal that does not close in simulation, with the measured numbers.
**Statistics and cost.** Full: 20 roads on 2,000 events of each of the four leading SM samples and on 500 pile-up
events: (8,000 × 19 + 500 × 16) trials × 11.7 s = 520 CPU-h. **[DP1] Reduced (proposed): 8 roads on 1,500 events of
each of the four SM samples, 20 roads on 500 pile-up events: (6,000 × 7 + 500 × 16) × 11.7 s = 163 CPU-h** [E].
*Lost with the reduction:* the angular granularity goes from 18° to 45°, so structure narrower than 45° (hadronic τ
near the MET, the jet axis opposite to it) is averaged, not resolved; the number of sideband trials per process falls
from 38,000 to 10,500, so the non-flatness is measured to about ×1.9 worse precision (√(38,000/10,500)). The
criteria are unchanged. **Dependencies.** B4 samples with dumps. **JFC 12.** This is a compute-envelope limit, not a
failed attempt; it needs the user's approval at Gate A.

### 4.9 B6 — detector-model robustness (SHOULD, Phases 3 and 4a)

**Method.** Seven variations: hit resolution × 1.5; hit inefficiency 99 % → 97 %, now applied to pile-up hits as
well (v1 applied it to signal hits only, D5 §4); material × 0.5 and × 2; top-up factors at their low and high limits;
an alternative soft-QCD tune for the pile-up at fixed density (conventions row "qq̄ modelling" translated). Each is
propagated to the pile-up rate at R04–R06 and to the signal efficiency. The material variation of the signal needs
Stage-3 reruns with the scaled material.
**[SD5]** The top-up variation is a density systematic at fixed ⟨μ⟩ = 200; it is not a pile-up scan (brief D8) (D2 O4).
**Criterion.** B6 is a measurement of sensitivity to assumptions, so its criterion has two parts. (a) Completeness:
every variation is evaluated on background and signal, with a statistical error on ln(B_var/B_nom) below 0.1 at R06
and on ε_var/ε_nom below 10 % (pooled over the points). (b) Classification fixed in advance: a variation is "robust"
if |ln(B_var/B_nom)| ≤ ln 2 at R04–R06 and |ε_var/ε_nom − 1| ≤ 0.2; otherwise "not robust". In both cases the measured
shift enters the likelihood at its measured size; nothing is capped. "Not robust" items are named in the limitations.
**Blinding.** The signal ratios are v2 efficiencies; they are computed only after the closure verdicts.
**Statistics and cost.** Full: background 7 × 1,000 events × 60.4 s = 117; signal 6 points × 500 rows × 6 variations
× 25.2 s = 126; Stage 3 with scaled material 49; total 293 CPU-h. **[DP2] Reduced (proposed): background 7 × 600
events; signal at 4 points (E 200 and E 500 at 1.5 and 3 keV) × 300 rows; 128 CPU-h** [E]. *Lost:* no variation is
measured at 5 keV, at 1,000–1,500 GeV or for the scalar; the per-variation error on the efficiency ratio rises from
about 6 % to about 10 % [E: binomial, pooled, v1 placeholder ε ≈ 0.2 at R04]. **Dependencies:** S1 code path; B2.

### 4.10 B7 — cosmic muons and beam halo (SHOULD, Phase 3)

**Method.** Rate per bunch crossing from public measurements × probability that a through-going straight track gives
a candidate in the road pointing to the primary vertex (a toy acceptance on the v2 geometry) × timing acceptance of
the tracker and timing layer × number of triggered crossings. The repo holds one public lead: 8.8 ± 3.1 cosmic and
2.6 ± 0.2 halo events in 586 h of live time in a stopped-particle search (`stage2_C001_quirks/research/
experimental_status_2026.md` l.147 and l.322, quoting arXiv:1801.00359 Table 4) [U]. That is a calorimeter/muon
selection, not a tracker rate; the cosmic flux at the detector depth and the halo rate are retrieval tasks (R-6).
**Criterion.** A number with its derivation for B_cosmic + B_halo in 3 ab⁻¹ at the chosen selection. If it is below
10 % of the smallest term of the sum it is stated and left out of the likelihood; otherwise it enters as a term.
**Fail:** if no public rate can be sourced, the item is reported as "argued, not quantified", as in v1. **Cost:** 5 CPU-h.

### 4.11 T1 — the likelihood (MUST, Phases 3–4c)

**Model.** For each selection, two counting bins c ∈ {T, G}:

  n_c ~ Pois( μ·S_c·Π_k φ_k^S + Σ_t B_{t,c} ),  B_{t,c} = N_t · Π_j (λ_{t,j} / M_{t,j}) · w_{t,c} · Π_k φ_k^t,

with one auxiliary measurement per simulated count, m_{t,j} ~ Pois(λ_{t,j}), where m_{t,j} is the number of simulated
events (or candidates) passing factor j of term t out of M_{t,j}; N_t the normalisation (N_trig × rate_t); w a fixed
weight; φ_k log-normal factors of constrained nuisances shared across terms and categories. Source: the on/off
(Poisson auxiliary) construction of Barlow–Beeston type named in PLAN l.356-358; references in
`conventions/search.md` (Cowan et al.; pyhf).
- *Zero counts.* m = 0 is an ordinary observation: the auxiliary term is e^(−λ). The 68 % upper value of λ is
  −ln 0.32 = 1.14, which is v1's bound [V: arithmetic], but here it is a constraint with its Poisson shape and not a
  log-normal centred on 1.14 with σ_ln = 1. Limiting case: M → ∞ at fixed m/M gives a fixed rate with no nuisance.
- **[SD7] Implementation in pyhf.** Each simulated count is its own single-bin *auxiliary channel* with observed
  count m and expectation λ = γ (an unconstrained normalisation factor), and the same γ scales the corresponding
  sample in the signal-region channels. pyhf's built-in `shapesys` fixes the auxiliary observation at its nominal
  value and cannot represent an observed zero; the feasibility toy used a "one event with τ = 1" stand-in and said so
  (FEAS_C R9). With auxiliary channels, toys fluctuate the simulated counts too.
- *Estimator outputs that are not counts* (thinning, occupancy model) enter as a nominal rate with a log-normal
  statistical nuisance from the bootstrap and the declared closure nuisance s_model of §4.0.
- *Correlated nuisances (shared names).* Luminosity; N_trig normalisation per process group (generator difference,
  K); pile-up density (top-up) across the pile-up term and every C_PU; material across NI/DIF rates and signal;
  hit resolution and inefficiency across signal and backgrounds; the MET model across SM terms; one closure nuisance
  per estimator, correlated across the two categories and across the terms that use the estimator; signal: f₂₀₀,
  trigger, QED FSR, vertex identification, Monte Carlo statistics (binomial, as an auxiliary channel).
- *No route double counting.* Each term has exactly one factorisation route, declared in the pre-registration (the
  one whose factors are measured on the largest populations). The other route is a cross-check with its own closure
  number. There is no envelope and no ln 117 width (D4 §3.4, I12).
- *What is limited.* μ = σ/σ_norm. Uncertainties of σ_norm itself (scale, PDF) are drawn as a band on the theory
  line; acceptance-type uncertainties (f₂₀₀ modelling, trigger, detector) are profiled (D2 §8.4).

**Asymptotics or toys.** The expected counts are small and many auxiliary counts are zero, so the conventions'
condition for asymptotics (more than about 5 expected events per bin) fails; v1 found asymptotic/toy ratios of
0.32–1.07 (D2 §2 [U]). **Toys are primary** for every quoted limit; asymptotic values are used for the T2 ranking and
are validated against toys. Cost [V unit, E total]: 1000 toys at one μ cost 652 s on the 31-parameter toy model;
40 points × 8 μ values × 1000 toys = 58 CPU-h per selection; three selections (chosen, runner-up, v1 fallback) =
174 CPU-h. The scaling with the number of parameters is not measured (FEAS_C); the v2 model will have about 60–100
parameters, so this number may double [L4]. pyhf 0.7.6 needs numpy 2.2 (FEAS_C O5).

**Acceptance criteria (the conventions' validation checks, §5.2).** (T1-a) The workspace validates against the pyhf
schema and is published. (T1-b) Re-fed with the v1 counts and v1 treatment switched on, it reproduces the v1 toy
limit at the best point (μ₉₅ = 1.2458×10⁷) within 10 %; with the v2 treatment the change is reported. (T1-c) Signal
injection at 0, 1, 2 and 5 × σ_norm on pseudo-data: fitted μ within 20 % of the injected value (the conventions'
threshold) or within its fit uncertainty where that is larger. (T1-d) On Asimov data no constrained nuisance is pulled, none sits at
a boundary, and any nuisance constrained to below 0.5 of its prior is explained. (T1-e) Impact ranking produced; the
leading nuisances are named and compared with the expectation (closure nuisances and zero-count constraints).
(T1-f) Asymptotic against toy limits tabulated at every point. (T1-g) Self-consistency of the toy
limit: at two points, in 500 background-only pseudo-experiments with fluctuated auxiliary counts, the fraction whose
limit lies below the quoted median expected limit is 50 % within twice its binomial error (± 4.5 %;
√(0.25/500) = 2.2 %). **Fail:** T1 is not used for a quoted limit until
fixed; a failure of (T1-b) is a regression on the v1 reading.
**Cost.** 224 CPU-h [E] (30 development, 20 expected results in 4a, 174 toys). **Dependencies:** B1–B4 outputs.

### 4.12 T2 — the selection rule (MUST, Phase 3 definition, Phase 4b application)

**Declared candidate selections.** All share the v1 fixed cuts (N_IT2 ≥ 3, |Δφ(n₃, MET)| < 0.15, |η(n₃)| < 1,
f_CKF < 0.2) and the SR-T/SR-G split.

| family | members | count |
|---|---|---|
| L (cumulative ladder rungs) | R07, R08, R09, R11, R14, R17, R20 | 7 |
| F (v1 fallback without dE/dx, width cut W_c/2^k from the frozen admissibility table per hypothesis) | FB(k_adm) | 1 |
| each with and without the displaced-vertex veto of B3 | ×2 | 16 in total |

**[SD9]** The dE/dx rungs R21–R23 and the dE/dx fallback columns are not candidates: the v1 admissibility for dE/dx
rests on dilution tables that cannot be regenerated [A3], and the pixel charge tail of the backgrounds is not
modelled by the Gaussian digitisation. This is a background-method reason. The pre-registration may remove
candidates from this list, with a logged reason of the same kind; it may not add any.

**Rule.**
1. *Eligibility* **[SD8]**: a selection is eligible only if every closure or agreement criterion that applies to its
   leading terms (those above 10 % of its total background) has the verdict PASS.
2. *Figure of merit:* G = mean of ln μ₉₅^exp over the 20 window points (the four E masses × Λ ∈ {1, 1.5, 2, 3, 5} keV;
   the v1 lower edge of the window at pile-up 200 is 1.0–1.2 keV, D2 §2 [U]), with μ₉₅^exp the median expected CLs
   limit from T1 (asymptotic), the efficiencies from the **optimisation half**, and the full background model. A
   point with no passing optimisation row enters with ε = 1/n_opt. Lower G is better.
3. *Choice:* the eligible selection with the lowest G. If another eligible selection has G within one bootstrap
   standard deviation of the best (bootstrap over optimisation rows), the one with fewer cuts is chosen. The three
   best by asymptotics are re-evaluated with toys and the toy values decide between them.
4. *If no selection is eligible:* this is the plan's "closure fails" outcome. G is still reported for all 16,
   labelled "background not validated", and the paper is the method and anatomy paper of PLAN §8.
5. *Background-free flag:* B₈₄ ≤ 0.11 events per category (the v1 budget, 0.3/2.71 = 0.1107 [V: arithmetic]) is
   reported as a yes/no flag for the chosen selection. It is not a requirement.

**Optimisation/evaluation split.** Each generated signal event gets the half h = parity of
blake2b(salt ‖ species ‖ mass ‖ event index) (the hash family v1 used for seeds, D5 §3). The half does not depend on
Λ, so one physical event is in the same half at all eight Λ. The salt is chosen at the freeze and recorded in
`PREREG_v2.md`; before that the mapping does not exist. The two halves are produced as separate campaigns with
separate directories. The aggregation script takes the half as an argument; its invocation on the evaluation half is
a logged step that requires the Gate B approval record.
**Acceptance criteria.** (T2-a) rule, list, figure of merit and salt in the hashed pre-registration before S1
production. (T2-b) the choice is reproduced by a second run of the script from the frozen inputs. (T2-c) the
optimisation-to-evaluation shift of ln μ₉₅ at the chosen selection is reported per point; a mean shift above 2σ of
its bootstrap error is reported as evidence of selection bias. **Fail** of (T2-b): Gate B is not requested.
**Cost.** 16 × 40 scans × 10.4 s = 2 CPU-h [E]. **Dependencies.** T1, S1, verdicts of B1–B4.

### 4.13 S1 — signal ×10, full chain at all 40 points (MUST, Phases 2, 4a, 4b, 4c)

**Method.** 2,000 rows per point (v1: 180–200 [V: D4 §4.1]), every row through the full chain (Stage 3 → injection →
digitisation → CKF → finder), at all 40 points. The fast path (numpy digitisation without CKF, 31 of 40 points in v1)
is retired; v1 measured it high by 1/0.87 at the fallback (D4 §4.3 [U]). Rows are split 1,000/1,000 by the T2 hash.
**[SD10]** Only events inside the counting acceptance (|η_pair| < 2.5) are propagated: the acceptance
A = ε_fid × ε_trig × ε_presel is formed from generator-level quantities [V: `AN1/acceptance.json` → `definition`,
`factors`], so the events outside need no string propagation. v1 propagated 463–519 events per (mass, Λ) for 200
rows [V: `STAGE3_INDEX.json`].
**Λ range of Stage 3.** Exactly the eight grid values, 0.45–5 keV. Nothing at 7–10 keV and nothing at Λ ≥ 15 keV
(brief D8). The cost is dominated by 5 keV (67.8 s per event, 71 % of the sum) and 3 keV (18.8 s) [V: FEAS_A §3.5].
**Stage 2.** New MG5 + Pythia samples for the five species-masses, 250,000 LHE events each (v1: 100,000 TRG at
E 200/500/1000, 40,000 at E 1500, 50,000 for Ẽ). The yield of unweighted, in-acceptance events per LHE event is
taken from the first chunk in Phase 2 and the sample size is adjusted; v1 reported a budget of only 413–1,277 events
per half at E 1500 and Ẽ 500 (D5 §6 [U]), so those two may need more than 250,000 [L5].
**Acceptance criteria.** (S1-a) 2,000 rows per point through the full chain, ≥ 99 % of jobs complete, ingestion
closure (v1's V4-1: every quirk hit maps to one measurement) passing in every job. (S1-b) no fast-path number in any
result. (S1-c) the efficiencies are first aggregated at Phase 4b (optimisation half) and 4c (evaluation half), not
before. (S1-d) statistical quality, stated in advance and only reported, never tuned: at a point with ε = 0.045
(v1 placeholder, the v1 best point) the binomial error on the evaluation half is 15 %; at ε = 0.03, 18 %; at ε = 0.2,
6 % [E, script]. (S1-e) the split is the frozen hash. **Fail** of (S1-a) at a point: the point is reported with the
rows it has and flagged; it is not filled with fast-path rows.
**Cost.** 827 CPU-h [E]: Stage 3 10,000 events × 95.6 s = 266 (Phase 2, truth level, no efficiency involved);
chain 80,000 rows × 25.2 s = 561 (Phase 4a, after the freeze). The plan's "12–30 CPU-h of string" (PLAN l.443) is not
compatible with 2,000 rows at 5 keV. **Storage.** 80,000 × 0.52 MB ≈ 42 GB. **Dependencies.** S2 (nominal shower),
freeze. **Risks.** The signal-injection chain mode is not benchmarked; the Stage-3 timing is on toy kinematics; both
are re-timed on the first Phase-2 jobs and the schedule is corrected if they differ by more than 30 %.

### 4.14 S2 — theory inputs (MUST, Phase 2)

**(a) NLO K-factors, computed.** FEAS_B built `loop_quirkE` (MG5's `loop_sm` plus the v1 quirk states; the quirks are
colour singlets, so the NLO QCD counterterms are those of the q q̄ γ*/Z* vertex already in `loop_sm`) and obtained
K = σ_NLO/σ_LO = 1.165 ± 0.002 at m_E = 200 GeV (CT18NLO, μ = H_T/2; NLO scale envelope +1.6/−1.1 %) [V: FEAS_B
Task 4]. v1's K = 1.110 at 200 GeV was transcribed from slepton NNLO_approx+NNLL tables and is defined differently
(D5 §2), so the two are not expected to be equal. **The model is trusted only after three validations:**
1. *Model identity.* Fixed-order LO of `loop_quirkE` against the tree-level v1 UFO at the same fixed scale and PDF:
   agreement within the integration error (|z| < 3) and 0.5 %. (FEAS_B found 0.6 % at *different* scales, which is not
   yet this test.)
2. *Published matching limit.* The scalar Ẽ has the quantum numbers of a right-handed slepton. σ_NLO(Ẽ, N_IC = 1)
   from `loop_quirkE` at the collision energy and PDF set of the LHC SUSY cross-section working-group right-selectron
   tables is compared with those tables at 200, 500 and 1,000 GeV. The repo records which tables v1 used and that
   the implied K against a CT18NLO LO rises from 1.06 to 1.29 (`stage2_C001_quirks/research/theory_signal_model.md`
   l.158-163 [U]); the table values themselves are a retrieval task (R-1). Criterion: within 10 % at each mass, the
   difference being the resummation the tables contain and MG5 does not. Outside: the computed K is not used.
3. *Process independence.* K for `p p > e+ e-` at NLO in a window of invariant mass around 2m_E agrees with K_E
   within 5 % (the QCD correction acts on the initial state only), and K_E/K_Ẽ is reported as the test of v1's
   "spin-independent" assumption.
**[SD11]** σ_norm = N_IC × σ_NLO(MG5, CT18NLO), with the 7-point scale envelope and the CT18NLO eigenvector
uncertainty computed for each mass. The NNLL/NLO ratio from the public tables is reported as an alternative
normalisation, not applied. If validation 1 or 2 fails, the fallback is the v1 transcription, labelled as such, and
the criterion "computed K" is reported as failed.
**(b) f₂₀₀, one definition.** f₂₀₀ = σ(pT(QQ̄) > 200 GeV after the shower) / σ(matched, inclusive), **with no η cut**.
The |η_pair| < 4 clause printed in v0.4 is not applied by the normalisation script (D3 §1 item 1); the fiducial
factor (|η_pair| < 2.5) belongs to A. One script computes f₂₀₀ for the five species-masses from the new samples; v1
values 0.04764, 0.10418, 0.14585, 0.16876 (E) and 0.1135 (Ẽ 500) are the comparison (D5 §2 [U] `TT/sim/results/xsec.json`).
Its uncertainty is rebuilt from: scale weights in the LHE files; PDF members; the merging scale (qCut 30 and 60
against 45: re-showers); the tune (Monash against CP5); and the comparison with one NLO-merged (FxFx, 0–1 jet)
sample at 500 GeV. v1's estimate was +12…+15 % / −11…−13 % (D5 §2 [U]). If the FxFx value lies outside the band, the
band is enlarged to contain it. The result is one asymmetric log-normal nuisance on the signal yield in T1.
**(c) QED final-state radiation.** v1 dropped it and carried −1.1 ± 0.8 % on ℓ_max (D5 §2 [U]). **[SD12]** v2 showers
the nominal signal with the QED-FSR card (same LHE; 21.1 against 21.2 ms per event [V: FEAS_B Task 3]); the FSR-off
sample is kept for C1 and for quoting the shift. This is a physics completion decided before any v2 efficiency.
**(d) Trigger turn-on (referee Q16).** v1 used ε = 0.98 · ½[1 + erf((MET − 200)/(20√2))] with estimated parameters and
no propagation (D5 §4 [U] `products.py` l.43-45). Substitution: at the offline threshold of 250 GeV the function gives
0.98 × ½[1 + erf(1.77)] = 0.98 × 0.994 = 0.974 [E: erf(1.77) = 0.988]. v2 takes the turn-on from a public Phase-2
Level-1 / high-level-trigger MET curve (retrieval task R-2; none is in the repo) and defines the nuisance as the
envelope between the nominal curve and the curve shifted by the uncertainty read from the source. If the public
curve reaches its plateau above 250 GeV, the offline threshold is raised before the freeze; that is a trigger-physics
reason, not a signal-efficiency reason.
**Acceptance criteria.** (S2-a) validations 1–3 recorded with numbers; (S2-b) K(m) with scale and PDF errors for all
masses of the reach curve; (S2-c) one f₂₀₀ definition in code and text, uncertainty propagated into T1; (S2-d) QED-FSR
sample is the nominal; (S2-e) the turn-on comes from a cited public figure with page, or the item is reported as
"parametrised, not sourced" with the v1 function and a nuisance equal to the full difference between plateau and
the 50 % point shifted by one width.
**Cost.** 67 CPU-h [E]: Stage 2 1.25×10⁶ × 50 ms = 17; K scan 0.7; FxFx 20; four re-showers 4 × 1.25×10⁶ × 21 ms = 29.
**Risks.** MLM cost not benchmarked; FxFx event generation not yet run (StdHEP did not compile, FEAS_B Task 4);
MG5 writes into its install directory → jobs use a per-node local copy (FEAS_B open issue 1).

### 4.15 P1 — thickness-law clean-ups (MUST, Phase 2)

P1 is not needed by the search (scattering dominates above 1.2–1.9 keV, D5 §7.13). It decides what the paper may say.
| sub-item | status and what must be written | pre-declared reading |
|---|---|---|
| Floor test 1: extended precision | no code exists (D5 §1.8; grep confirmed there). A step map in ≥ 30-digit arithmetic for the 3–5 events with the smallest ε⊥ at B₀/20, detector scaled by 1/27, at B₀ and B₀/20 | v1's prediction (`TT/analytic/NEAR_MISS_IMPULSE.md` l.731-738 [U]): if the excess is the double-precision floor, Δc(20) falls from +0.01–0.02 to ≲ 0.001. Reading: "floor" if \|Δc\| ≤ 0.003 in every event; "physical" if ≥ 0.007 in every event; otherwise "inconclusive". All three are reportable outcomes |
| Floor test 2: reduced precision | a change of the Minkowski product `mdot` in `nm_kernel.py` to truncate the mantissa to 44 bits | if floor: the same Δc distribution reappears at 8× larger ε⊥ with the ε⊥⁻² shape; reading by a two-sample test at p > 0.05 |
| B*-off | **already run twice** (Stage-1 at 3 keV; Stage-3 at 5 keV on 171 events: unpaired 5.5σ, paired only 2.1σ, D5 §1.8 [U]). What remains: a paired test with power. N = 171 × (5/2.1)² ≈ 970 events at 5 keV for 5σ if the effect is as measured [E, script]; plus the same test at 1 keV on new gate events | "B* attribution supported" if the paired median of (on − off) is positive at ≥ 3σ overall and for k_B ≥ 6; at 1 keV the paired difference must be compatible with zero (≤ 2σ), which shows the +2 % gate excess is not B* |
| Population estimator for c | defined now: the **paired median of (c₂ − c_ev)** over events, with a paired bootstrap (2,000); criterion \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at all five points at 1 keV | v1 already knows this estimator on the old gate events (within ± 0.001, D5 §1.5). It is therefore evaluated on **300 new events per point** with new seeds. The original gate (difference of medians, +0.7 to +3.2 %) stays reported as failed |
| Validity window | from the tracked `TT/sim/stage3/results/P1.json`: a table per (point, Λ, k_B bin) | text follows the table: 9 of 30 cells pass; +6.5 ± 1.3 % in the k_B 2–4 bin at 5 keV; the straight-string ratio 0.50 predicted against 0.75 ± 0.08 stays visible as failed (D3 §1, D5 §1.6) |
| Linux difference | one conformal run gives 2 crossings instead of 6 on Linux (FEAS_A §3.2) | the Stage-1 analysis is rerun; if a quoted P1 number moves, it is corrected and listed in the errata |
**Criterion for the item.** All five rows executed and reported with their pre-declared reading, whatever the
outcome; the paper's P1 claims are limited to what the table supports ("in the median over events", not "per event
on 2.2×10⁵ events", D3 §6.5). **Cost.** 30 CPU-h [E] (v1: 0.84 CPU-h for 171 events on the M3; numba codes ran 0.7–3.4
times the M3 time here). **Risk.** The extended-precision map is 1–2 person-days of new code (D5 §1.8 [U]); if it is
not finished, [DT3] floor test 2 alone is reported and floor test 1 is listed as not done.

### 4.16 S3, S4, S5

**S3 (dropped, brief D1).** The paper stays barrel-only and states the endcap gain as an outlook, tagged EST, from plan
S3: signal ×1.5–3.2; reach 866 → 1062 GeV at B = 10, g = 1. That statement answers referee question 11. The endcap row
of the reach table does not appear as a result. (Provenance note for the paper: ×3.2 = 1/0.31 at g = 1 is in the
book, ch29 l.106-110; the lower end 1.5 has no derivation in the book or the plan, D3 §5; see §12.)
**S4 (COULD) — recommendation: not included [DP4].** A merging-tolerant rung and a lower seed opening-angle cut change
the finder or add a selection, so every background estimator would have to be closed again for it: about one more
week of development (PLAN l.382; book ch28 l.256 [U]) and a rerun of the finder on all background samples, at least
the trial part of B2 + B1 + B4 ≈ 600 CPU-h [E: trials are ≈ 45 % of a B1-type event]. It would also delay the freeze.
**S5 (COULD) — recommendation: not included [DP4].** A pile-up-robust separation estimator is method R&D with no bound
on its duration; the paper states the negative result (sep_IT flat at 18–26 mm at pile-up 200; M_est a proxy), as
PLAN l.384-385 allows. Estimated cost if requested: about a week and ≈ 50 CPU-h [E].

---

## 5. Systematic plan and the conventions enumeration (binding at Phase 4a)

`conventions/search.md` was read in full. Its tables are written for e⁺e⁻ searches and say that pp searches replace
the beam rows by PDF and pile-up and add luminosity. Each row is answered below; "WI" = will implement.

### 5.1 Required systematic sources

| conventions row | answer | how, where |
|---|---|---|
| Signal cross-section theory (scales, higher orders) | WI | 7-point scale envelope and CT18NLO eigenvectors on σ_NLO(m) (S2, Phase 2); drawn as a band on the theory line, not profiled |
| Signal acceptance (generator comparison, ISR variations) | WI | f₂₀₀ and A from MLM against FxFx at 500 GeV, scale weights, qCut 30/60, CP5 against Monash (S2); profiled in T1 |
| Signal shape | WI, translated | no fitted shape: two counting categories. The "shape" is the SR-T/SR-G migration: timing resolution of the barrel timing layer varied within the public value (R-7), Phase 4a |
| ISR modelling | WI | this is the pT(QQ̄) > 200 GeV tail: the f₂₀₀ nuisance above. One nuisance, not counted twice with the acceptance row |
| 4-fermion backgrounds (generator comparison) | WI, translated | the pp analogue is the irreducible MET + jets background: Z(νν), W, top, dibosons. Pythia 2→2 against MG5 for the leading Z(νν)+jet and W+jet rates (measured ratio 0.84 for Z(νν)+jet, FEAS_B); cited K-factors (B4) |
| Background normalisation | WI | per process group: generator difference ⊕ K uncertainty from the cited source; single-interaction rates: Geant4 against v1 generator, material band (B1); Phase 4a |
| Background shape | Not applicable as written: there is no discriminant distribution; each selection is a counting experiment. Its role (extrapolation of the background along the cuts) is taken by the closure nuisances of B1–B3 and the trend tests (B1-b, B2-c), which are implemented | |
| qq̄(γ) modelling (2-fermion generator comparison) | WI, translated | soft-QCD modelling of pile-up: alternative tune at fixed top-up density (B6); hadron species fractions Pythia against Herwig at generator level if Herwig installs without a source build, otherwise against published minimum-bias data [DP5] (Phase 3) |
| MC statistics | WI | Poisson auxiliary channel per simulated count (T1, [SD7]); bootstrap errors for estimator outputs |
| Detector simulation model (data/MC) | Not applicable as written: there is no data. Translated and WI: Fatras against Geant4 for hadronic physics (B1); resolution, inefficiency, material, top-up variations (B6); physics list variation FTFP_BERT against QGSP_BERT (B1) | |
| Object calibration | WI | MET response and resolution (the B4 model parameters); trigger turn-on (S2); primary-vertex identification efficiency, set to 1 in v1 although v0.4 quotes 93 % (D3 §1 item 2) → a factor and nuisance from a public source (R-8) or, if none is found, the limitation is stated with ε_PV = 1; timing resolution. dE/dx scale: not applicable, dE/dx is not used [SD9] |
| Beam energy | Not applicable: pp at a fixed nominal 14 TeV; all cross sections are computed at 14 TeV. Replaced by the PDF and pile-up rows as the conventions instruct | |
| Luminosity | WI | the result is a projection at 3 ab⁻¹; the luminosity nuisance for HL-LHC comes from a public target (R-9) and applies to signal and to every background normalised to L; limits are also shown at 300 fb⁻¹ |
| PDF (pp replacement) | WI | CT18NLO eigenvectors on σ, f₂₀₀ and A (weights in the LHE files) |
| Pile-up (pp replacement) | WI at fixed ⟨μ⟩ = 200 | density (top-up limits), tune, timing spread. No scan in μ (brief D8) [A5] |
| QCD scale variations | WI | signal as above; SM backgrounds through the K uncertainty |
| Fragmentation model | WI in part | tune variation everywhere; string against cluster hadronisation only at generator level and only if Herwig installs [DP5]. It matters through the K/π ratio, which sets the decay-in-flight rate |
| Heavy-flavour treatment | Not applicable as written (no b-tagging). Displaced b/c decay vertices are a topology: Phase 2 checks whether v1's eight topologies contain them (Pythia decays with τ₀ < 1000 mm are in the particle list, D5 §4); if they are a separate class they are added to B1 | |

Study-specific sources (all WI): thinning and occupancy closure (B2); P_geo × C_PU closure and bias weights (B1);
conditionals (B3); Geant4 material composition and physics list (B1); the MET model tail (B4); f₂₀₀ (S2); QED FSR
(nominal on, shift quoted); trigger (S2); status-4 Stage-3 events dropped (≤ 1.5 %, one-sided, D5 §3 [U]); the
frozen admissibility transcription [A3]; signal Monte Carlo statistics; finder seed-threshold convergence (C2).
Every variation is sized by a measurement, a closure result or a cited public number; no round-number inflation
(JFC Phase 4a). No single nuisance may exceed 80 % of the total without investigation (regression trigger).

### 5.2 Required validation checks

| conventions check | answer |
|---|---|
| 1. Closure tests in validation regions, p > 0.05 | WI, translated: the "validation regions" are the loose rungs R04–R07 where direct simulation counts exist; the "signal region" is the chosen deep selection. Criteria in §4.0, B1-a, B2-a, B3, B4-c, B5-a. The conventions' pitfall "blind spot in VR coverage" applies in full: the loose rungs are not between a control region and the signal region. Answers: two independent pile-up estimators compared at the deep rungs (B2-b); P_geo measured directly at the deep rungs (B1); trend tests [L6] |
| 2. Signal injection at 0, 1, 2, 5 × | WI (T1-c), Phase 4a, on pseudo-data with v1 placeholder efficiencies |
| 3. Nuisance pulls and constraints | WI on Asimov and pseudo-data (T1-d). There is no observed fit |
| 4. Impact ranking | WI (T1-e) |
| 5. Goodness of fit | Not applicable to data (none). The estimator closure χ² values and p-values are reported in its place, with JFC's alarm bands (χ²/ndf < 0.1 or > 3) |
| 6. Look-elsewhere effect | Not applicable: no observed excess can occur; hypotheses are a fixed grid. The multiple-comparison correction of C1 (Bonferroni over 41) is the only trials factor |
| Standard configuration: CLs, q̃_μ, toys below ≈ 5 expected events | WI (T1) |

---

## 6. Reference analyses and comparison targets

Sources: the repo only. `AUD` = `TT/paper/P2_NOVELTY_AUDIT.md` (which read the arXiv PDFs and gives pages),
`EXT` = `TT/stage5/EXTERNAL_BOUNDS.md`, `EXP` = `stage2_C001_quirks/research/experimental_status_2026.md`. I read these
files this session; I did not open the papers, so every entry is **[U] for the paper content, [V] for "the repo file
says so"** at the line given. Look-ups are logged in `QV2/retrieval_log.md`.

### 6.1 Methods and systematic programmes

| | R1 Knapen, Lou, Papucci, Setford, arXiv:1708.02243 | R2 Li, Li, Pei, Zhang, arXiv:1911.02223 | R3 FASER quirk search, arXiv:2607.26195 | R4 CMS disappearing tracks, arXiv:2309.16823 (method reference) |
|---|---|---|---|---|
| type | phenomenology, central tracker | phenomenology, central tracker | experiment, forward | experiment, spurious tracks from random hit alignment |
| model | (1,1)₁ fermion, N = 2 (same as E) and coloured | E-like, N_IC = 3 (N_IC = 2 in App. A) | (1,1,−1) fermion, N_IC = 2: exact match to E | — |
| detector, pile-up | simplified ATLAS barrel, 2 T, 8 layers, ⟨μ⟩ = 50 | CMS-like 13 barrel layers, helix intersections, ⟨μ⟩ = 50 | forward detector, 13.6 TeV, 186.3 fb⁻¹ | CMS, 137 fb⁻¹ |
| backgrounds | pile-up hits; beam-pipe conversions; no Z(νν)+jets | Z(νν)+jets + pile-up dominant | (not extracted in the repo) | genuine and spurious tracks, sideband control regions with transfer factors |
| background estimate | factorised: distribution from a looser (1 hit per layer) selection × efficiency of the tight one; reach "assuming negligible irreducible backgrounds" | cut flow on simulated Z+jets: 3600 → 0.12 fb | (not extracted) | data-driven transfer factors |
| statistical method | counting: contours of 3 and 5 signal events at B = 0 | 95 % CL exclusion from S and B after cuts (method details not extracted) | (not extracted) | binned likelihood (not extracted) |
| systematic programme | none quoted | none extracted | shower scale ≈ 6 %, up to 28 % at small Λ (EXP l.335); the rest not extracted | Table 7: signal selection 10–17 %, luminosity 1.6 %, jet energy 0–24 %, scales 0–2 %, ISR 0–3 %, pile-up 0–2 %, trigger 0–4 %, dE/dx 3–8 %; spurious background 5–52 % (long), 6–28 % (short) (EXP l.132) |
| source lines | AUD §1.1 | AUD §1.2 | EXT l.58; EXP l.51-56, l.335 | EXP l.127-132 |

**Method parity.** R1 and R2, the two studies closest in observable, use event counting at zero or small simulated
background and quote no systematic programme. v2 uses a profile-likelihood CLs model with constrained nuisances and
toys, which is more sophisticated; parity is met without a cross-check obligation. As a comparison in their own
terms, v2 also quotes the "3 and 5 signal events at B = 0" reach with the v2 efficiencies (Phase 4c). R4 is the
closest experimental method for the dominant instrumental background; its transfer-factor uncertainties (5–52 %)
are the scale against which the B5 sideband closure is read. The systematic coverage of §5 contains every source R4
lists that exists in a simulation-only tracker study (selection efficiency, luminosity, scales, ISR, pile-up,
trigger); jet energy scale enters only through the MET model.

### 6.2 Published numbers recorded as comparison targets

| quantity | value | source in the repo |
|---|---|---|
| R1 discovery reach, EW quirks, 300 fb⁻¹ (5 events, B = 0) | 650 GeV | AUD §1.1 "Claimed reach" (abstract, p. 1) |
| R1 efficiencies at 800 GeV: ε_trig, ε_fid, ε_reco at Λ = 1…5 keV | 0.10, 0.28, 0.11 / 0.41 / 0.65 / 0.72 / 0.74 | AUD §1.1 (Table I, p. 8) |
| R1 fraction of background events with a plane (≥ 1 hit in 4 of 8 layers; in every layer) | ∼10⁻³; 6×10⁻⁵ | AUD §1.1 (p. 7) |
| R2 background after cuts, 13 TeV | 0.12 fb (Z+jets), ≈ 12 events at 100 fb⁻¹ [E in AUD] | AUD §1.2 (Table II, p. 8) |
| R2 exclusion, 100 fb⁻¹, N_IC = 3, fermion (scalar) | 450 (150) GeV | AUD §1.2 (abstract) |
| R2 App. A, N_IC = 2, 300 fb⁻¹ | ≈ 400 GeV; R1's method redone: below 500 GeV | AUD §1.2 (p. 9-10) |
| R3 observed mass limit at Λ = 1 / 3 / 5 / 10 keV | 113 / 162.6 / 172 / 179 GeV (19 Λ values from 0.3 to 105 keV in HEPData ins3184325) | EXT l.58, l.80 |
| D0, Λ = 10 keV–1 MeV | 107 GeV | EXT l.59, l.83 |
| Farina–Low recast, E at Λ = 1 eV / 100 eV / 1 keV | 650 / 150 GeV / no limit | EXT l.60 |
| v1, this study: reach at B = 0, 3 ab⁻¹; 3-event and 5-event reach at 300 fb⁻¹ | 1026 GeV; 665 and 586 GeV [E, v1 efficiencies] | D3 §3, §5 (recomputed there from `SUM`) |
| v1 total efficiency f·A·ε at E 500 against R1 | ≈ 0.005 against ≤ 0.021 | AUD l.245, `TT/paper/sections/10_bounds.tex` l.22-23 [V] |

The three reach numbers for 300 fb⁻¹ in the plan, the audit and the paper differ (665/586, 630–665/560–590,
"≈ 0.6 TeV"; D2 §8.8). v2 quotes one number per definition, computed with pyhf.

### 6.3 Corpus queries
The phase template asks for queries to an experiment corpus; none exists here (deviation V8). The equivalent
look-ups in the repo's literature cache are logged in `retrieval_log.md` (five entries).

### 6.4 Retrieval tasks for Phase 2 (numbers not in the repo; nothing is quoted from memory)

| id | needed | for |
|---|---|---|
| R-1 | right-selectron cross-section tables at NLO(+NLL) with their PDF set | S2 validation 2 |
| R-2 | public Phase-2 Level-1 / HLT MET turn-on curve with its uncertainty | S2 (d) |
| R-3 | public Phase-2 jet response and resolution, lepton acceptance, pile-up MET resolution | B4 MET model |
| R-4 | multijet fraction after a MET + jet selection in a published monojet-type analysis | B4 validation (c) |
| R-5 | cited K-factors for V+jets, tt̄, single top, dibosons at 14 TeV | B4-d |
| R-6 | cosmic-muon flux at detector depth, beam-halo rate | B7 |
| R-7 | barrel timing-layer resolution and its degradation | timing nuisance (v1 used 35 ps, D5 §4 [U]) |
| R-8 | primary-vertex identification efficiency at ⟨μ⟩ = 200 | ε_PV |
| R-9 | HL-LHC luminosity uncertainty target | luminosity nuisance |
| R-10 | R3's statistical method and full systematic table; R2's limit-setting method | completing Table 6.1 |
| R-11 | Barbashov's solution class; Knapen et al. Sec. III.D text | C3 |

---

## 7. Label index

**Constraints.** [A1] No collision data: expected limits only; "observed" quantities and data/MC checks do not exist.
[A2] v1 cannot be reproduced event by event (lost inputs, different random streams): all comparisons are statistical.
[A3] Admissibility tables and δ₉₅ are frozen transcriptions; six hashed v1 inputs are lost. [A4] No-PU samples are
stored as summaries, not events. [A5] Pile-up is fixed at 200. [A6] Cluster: 12 worker cores (9 on weekday daytime),
7.5 GiB per node, jobs ≤ 30 min, no cloud. [A7] Geant4 runs only on nodes whose local install matches the tracked lock.
[A8] Public information only; material composition and many detector parameters are not public.

**Limitations.** [L1] Direct closure at R07 for single-interaction terms has only ≈ 12–24 expected counts.
[L2] Nuclear-interaction rates carry the unknown material composition. [L3] The sideband width usable in the reach is
≈ 1.1, not 0.17. [L4] Toy cost for the real workspace is not measured. [L5] The Stage-2 yield of in-acceptance
events at E 1500 and Ẽ 500 is uncertain. [L6] Closure regions are the loose rungs, not a region between control and
signal regions. [L7] Barrel only. [L8] Hits are Gaussian-smeared on cylinders, not clusters on modules. [L9] The
string is classical Nambu–Goto without infracolour radiation; stated validity Λ ≲ 10–26 keV (D2 §8.10 [U]).
[L10] Stage-3 and ρ = 2 unit costs rest on toy inputs and on one event.

**Strategy decisions.** [SD1] grid unchanged. [SD2] approach comparison with the MVA moved to Phase 4c. [SD3] C1 signal
at 400 rows per point. [SD4] the counted pile-up object is the hit set after grouping at the target density.
[SD5] top-up variation is a density systematic. [SD6] time-tag conditional for prompt terms included. [SD7] zero
counts as auxiliary Poisson channels. [SD8] only selections whose leading terms passed closure are eligible.
[SD9] no dE/dx selections. [SD10] string propagation only for events in the counting acceptance. [SD11] σ_norm from
computed NLO. [SD12] QED FSR on in the nominal signal. [SD13] v2 single freeze content (§8). [SD14] evaluation-half
aggregation only after Gate B.

**Downscope proposals for Gate A.** [DP1] B5 reduced. [DP2] B6 reduced. [DP3] MVA as cross-check only. [DP4] S4, S5 not
included. [DP5] Herwig comparison at generator level, conditional on installation.
**Downscopes triggered only by a failed attempt.** [DT1] Geant4 hand-over fallback. [DT2] thinning validated to R06
only. [DT3] floor test 1 not done. [DT4] ρ = 2 pre-merge threshold raised to N_IP2 ≥ 7 if storage exceeds the cap.

---

## 8. The v2 pre-registration (`PREREG_v2.md`): outline

**What is frozen when.**
| moment | frozen | by |
|---|---|---|
| Gate A (this document + `COMMITMENTS.md`) | item criteria and tolerances of §4; C1 subset; T2 candidate list and figure of merit; systematic enumeration | 4-bot review, user |
| end of Phase 3 (the freeze; not a human gate, brief D7) | `PREREG_v2.md`, hashed and committed **before any v2 production sample exists**; user notified | 4-bot review |
| Gate B | closure verdicts shown first, then selection and expected sensitivity from the optimisation half | user |

**Content of `PREREG_v2.md`** [SD13]. (1) The v1 record by hash (below). (2) For each estimator of B1–B4 and each
conditional of B3: definition, code hash, the single factorisation route, the declared s_model, the closure statistic
and tolerance of §4 (these may be made stricter, never looser, than at Gate A), the samples with seeds and sizes,
and the consequence of failure. (3) B5 and B6 test definitions. (4) The MET model with its sourced parameters.
(5) The T1 workspace schema and nuisance list; toys as primary. (6) T2: the list (possibly shortened with reasons),
the figure of merit, the split salt, the eligibility rule. (7) The BDT cross-check recipe. (8) The declared
exception for the C1 signal counts (§4.1). (9) The analysis-code freeze: sha256 of every analysis module, taken
**before** production. (10) Failure handling: a failed criterion is reported as failed; no scale-factor patch; a
change after the freeze needs a dated addendum with a background-method or physics reason and is listed in the paper.
(11) A change log from v1 to v2, each change with its reason; none is a signal efficiency.

**Correction to PLAN l.408** ("rows 1 to 4 of the book's ranking go into one freeze"). The book's rows are: 1 a data
anchor, 2 counting as the estimator, 3 signal yield, 4 m_Q and Λ at pile-up 200 (D3 §6.1). Row 1 cannot exist in a
simulation-only study (B5 is its simulated stand-in) and row 4 is S5. The single v2 freeze holds: the estimators
(B1–B4), the conditionals including the time-tag credit, the sideband and robustness tests, the likelihood, the
selection rule and the signal split.

**v1 kept by hash** (verified by D4 §1.6 on 2026-11-13 with `sha256sum`; [U] by me).
- `analysis_freeze.json` (sha256 b42aef4d…): 32 of 32 listed files match.
- `frozen_inputs.json` (21 files): 13 match; 2 differ as documented in `HASH_ADDENDUM.md`; **6 are lost** with the bulk
  data. `WP_RULE.md` 1b2ea9bd… matches; its header still reads "not yet frozen" by design, and the operative T_seed is
  4, not the 6 of its text; the governing record is WP_RULE + HASH_ADDENDUM + the PC-19 amendment.
- The five `C12FC_v1` output files match the hashes in `STAGE4_SUMMARY.json`. Three helper scripts differ from the
  hashes recorded "at writing"; they are not production code.
The v2 appendix prints these hashes and the list of lost files.

**How the paper states the v1 freeze timing.** PLAN l.186 says "frozen before any signal efficiency". That holds for
the rule, the ladder and the fallback (2026-10-13). The analysis code was frozen again on 2026-10-16, after a first
complete run had produced signal efficiencies and limits; the fixes between the two runs lowered the fallback
background bounds (FB0/FB1 by ×4–8 in SR-G and ×50 in SR-T) and moved the best ratio from 1.1×10³ to 790, and a
normalisation fix (the f₂₀₀ factor; 37.6 → 790) followed the result review [V: `S4/STAGE4_RESULTS.md` l.115-117 and
§11.2; D4 I5]. The appendix says exactly this. v2 freezes rule **and** analysis code before production.

---

## 9. Flagship figures and methodology diagrams

| # | figure (PLAN §3.3) | data source | produced |
|---|---|---|---|
| 1 | event display of a quirk ribbon at pile-up 200, "best of its sample" | S1 evaluation half + pile-up, a point inside the window; choosing it uses passing signal events | Phase 4c (after Gate B), final in 5 |
| 2 | thickness law with scattering floor and crossover | tracked `TT/sim/stage3/results/P1.json` + P1 floor and B*-off points | Phase 2, final in 5 |
| 3 | efficiency map on the (m_Q, Λ) grid with the Λ window | S1 evaluation half at the chosen selection | Phase 4c |
| 4 | background ladder: v1 bounds and v2 estimates with bands, against the budget | `AN1/bsum_wp.json` (v1 layer) + B1–B4, T1 | Phase 4a |
| 5 | closure plots for every estimator at R04–R07 | B1, B2 (two estimators), B3, B4, B5 against direct counts | Phase 4a (development versions in Phase 3) |
| 6 | expected limit against mass with existing bounds | T1 toys; `TT/stage5/external_bounds.json` (FASER, D0, Farina–Low) | Phase 4b (optimisation half, for Gate B), 4c final |
| 7 | reach against an assumed background, v2 estimate marked | the book's method (`book/checks/ch29_checks.py` l.25-79, vendored into QV2) redone in pyhf; signal at the **chosen** selection, background as the *median* with its width | placeholder version with v1 efficiencies in 4a, final in 4c |

For Fig. 7 the v2 point lies on the curve only if the signal yield is recomputed at the v2 selection (D3 §6.6); the
Phase-4a version is therefore labelled "v1 efficiencies (placeholder)". All figures carry "Private work (simulation)".

**Diagrams (figure-scrolling test).** (a) the chain: generation → string propagation → injection → Fatras/Geant4 →
digitisation → CKF → plane finder; (b) the geometry of a ribbon: plane through the vertex, road around the MET
direction, w_core and thickness; (c) the ladder as a cut-flow strip with the two categories; (d) the background
estimators: thinning with re-grouping, the occupancy model, P_geo × C_PU with the Geant4 hand-over; (e) the blinding
and freeze timeline with the two signal halves and the three gates; (f) the likelihood: signal-region bins and
auxiliary channels; (g) the road-rotation sideband.

---

## 10. The 25 referee questions

| # | question (short) | item(s) | paper section |
|---|---|---|---|
| 1 | limit from zero-count bounds | B1–B4, T1 | 6, 7; v1 in App. |
| 2 | no hadronic physics in Fatras | B1 | 4, 6 |
| 3 | thinning closure failed | B2 | 6 |
| 4 | factorisation untested | B1-a, B3, B2-b | 6 |
| 5 | multijets, Z(ττ), lost-lepton Z missing | B4 | 6 |
| 6 | eight proxies | B4-a | 6 |
| 7 | top-up ×2.3–7.3 | B6 | 4, 10 |
| 8 | cylinders, Gaussian smearing | B6, [L8] | 4, 10 |
| 9 | finder correct and near optimal | C2 | 5 |
| 10 | 9 events; fast path | S1 | 7 |
| 11 | why barrel only | S3 statement (brief D1) | 10 (outlook, EST) |
| 12 | rules changed after the result | §8; v1 by hash | App. pre-registration |
| 13 | summed 68 % bounds, uncorrelated categories | T1 | 6, 7 |
| 14 | why 0.11 | T2 (flag only) | 5, 7 |
| 15 | cosmics, halo | B7 | 6 |
| 16 | trigger at Phase 2 | S2 (d) | 2, 5 |
| 17 | K-factors, f₂₀₀ | S2 (a), (b) | 2 |
| 18 | classical string, no infracolour radiation | [L9]; text | 3, 10 |
| 19 | law validity and failed gate | P1 | 3, App. derivation |
| 20 | law not testable at detector level | text; resolution stated as an estimate (C3) | 3, 10 |
| 21 | m_Q, Λ measurable? | negative result; S5 not included | 7, 10 |
| 22 | comparison with Knapen et al., Li et al. | §6; reach at B = 0 and against B | 9 |
| 23 | data-driven estimate possible? | B5 | 8 |
| 24 | reproduce or recast | C1, package (workspace, efficiency tables, container) | App. reproduction |
| 25 | CMS result? AI used? | C3 disclosure | title page, acknowledgements |

Q16 had no owner in the plan (D2 §8.3); it is S2 (d) here. The MET and vertex-identification variations of v0.4's open
issue 12 are owned by B4 (MET model) and §5.1 (object calibration).

---

## 11. Schedule — the Gate-A proposal

### 11.1 Capacity model
- Slots: 12 worker cores; at most 9 on weekdays 08:00–19:00 (brief §5.3). Per week:
  5 × (11 h × 9 + 13 h × 12) + 2 × 24 h × 12 = **1,851 slot-hours, 264 per day** [E, script].
- Losses: nodes with a graphical session are capped at 3 jobs (two of three had one at preflight, `LOG.md` 14:34);
  other lab users; ρ = 2 jobs may need one node each (§4.5); ≤ 500 steps per workflow and gaps between campaigns;
  failed and retried jobs; Argo overhead 17 s per job (about 8,200 jobs → 39 slot-hours, 1.2 %) [E, script]; cold
  NFS starts (minutes per node and environment, FEAS_A §3.8).
- **Effective capacity assumed: 0.60 × 264 ≈ 160 core-h per day on average; 0.50 (130) in development phases, 0.75
  (200) in production phases with campaigns queued continuously** [E]. The unit costs already contain the slowdown of
  4 jobs per node. If the cluster gave only 0.40 (105 per day), every compute duration below grows by half.

### 11.2 CPU-h budget (from §4; script table)

| item | priority | Phase 2 | Phase 3 | Phase 4a | 4b/4c, 5 | total |
|---|---|---|---|---|---|---|
| C1 | MUST | 192 | | | | 192 |
| C2 | MUST | 81 | | | | 81 |
| P1 | MUST | 30 | | | | 30 |
| S2 (incl. Stage 2 base) | MUST | 67 | | | | 67 |
| S1 | MUST | 266 (string) | | 561 (chain) | | 827 |
| B1 | MUST | | 60 | 421 | | 481 |
| B2 | MUST | 10 | 10 | 574 | | 594 |
| B3 | MUST | | 10 | 20 | | 30 |
| B4 | MUST | | 50 | 357 | | 407 |
| T1, T2, BDT cross-check | MUST | | 30 | 20 | 181 | 231 |
| figures, package | MUST | | | | 10 | 10 |
| **MUST total** | | **646** | **160** | **1,953** | **191** | **2,950** |
| B5 | SHOULD | | 20 | 520 full / 163 reduced | | 540 / 183 |
| B6 | SHOULD | | 10 | 293 full / 128 reduced | | 303 / 138 |
| B7 | SHOULD | | | 5 | | 5 |
| **Total** | | 646 | 190 | 2,771 / 2,249 | 191 | **3,798 full / 3,275 reduced** |

With a 20 % contingency for reruns and regressions the reduced total is 3,930 CPU-h. C3 costs no CPU.
Largest single uncertainties: ρ = 2 cost (one event), signal-row cost (not benchmarked as such), MLM generation,
hard-scatter no-PU generation, toy cost for the real workspace.

### 11.3 Order, critical path, parallel campaigns (days after Gate A)

| days | phase | critical path | in parallel |
|---|---|---|---|
| 0–6 | 2 | ρ = 2 memory and storage measurement (day 0); Geant4 installs on two nodes; Stage 2 for C1 points; C1 campaigns (192 CPU-h); C2 (81); **decision point 1 at day 6** | S2 (K, f₂₀₀, re-showers), P1, Stage-2 full samples; then S1 string propagation (266 CPU-h) as low-priority filler until day ≈ 12 |
| 6–13 | 3 | B1 hand-over and estimator on development samples; B2 re-grouping and occupancy model on the C1 pile-up samples; B4 MET model; T1 on v1 counts; **decision point 2 at day 12** (do the estimators close at R04–R06 on the existing samples? if not, redesign before the freeze) | B3, B5 and B6 prototypes; T2 script; retrieval tasks; 1-bot review per channel |
| 13–15 | freeze | `PREREG_v2.md`, 4-bot review, hash, commit, user notified | — |
| 15–27 | 4a | production, 2,249 CPU-h at 200 per day = 11.3 days: order B2 direct and ρ = 2 → B1 → B4 → S1 chain (both halves, not aggregated) → B6, B5 | closure analysis as each campaign ends; T1 expected results with v1 placeholders; note writing |
| 27–30 | 4a review | 4-bot + bib on the compiled note; **decision point 3a: closure verdicts recorded** | — |
| 30–33 | 4b | T2 on the optimisation half; toys (181 CPU-h); 4-bot + bib; **Gate B** (verdicts first) | — |
| 33–35 | 4c | evaluation half: efficiencies, limits, reach; BDT cross-check; 1-bot review | — |
| 35–42 | 5 | note, paper (C3 list), package; 5-bot + adversarial review against §10; **Gate C** | — |

**Calendar estimate: about 6 weeks from Gate A (range 5–8)**, of which 11–12 days are production wall time. The
critical path is C1/C2 → estimator development → freeze → B2/B1/B4 production → closure verdicts → Gate B. S1 string
propagation, S2, P1, B6 and B7 are off the critical path. A review that returns ITERATE adds 1–2 days each time.

### 11.4 Storage (cajuela, soft budget 1.5 TB)

| what | GB [E] |
|---|---|
| PU-200 chain and trial records: 208,600 events × 0.52 MB | 106 |
| hit dumps for 5,000 events (≈ 2.4 MB each) | 12 |
| ρ = 2 pre-merge candidates (planning value; cap 400) | 200 |
| no-PU summaries and R04 passers | 18 |
| Stage 2 (LHE and five shower variants), Stage 3 | 8 |
| Geant4 vertices, logs, pyhf outputs, repo bundles | 15 |
| **total** | **≈ 360 (≈ 560 at the pre-merge cap)** |

Software on the NFS home is 0.58 GB of 150 GB (FEAS_B [V]); Geant4 takes 6.6 GB of local scratch per worker.

### 11.5 Proposals that need the user's approval at Gate A, and later triggers

| label | proposal | saves | lost |
|---|---|---|---|
| [DP1] | B5 with 8 roads on 6,000 SM events | 357 CPU-h (1.8 days) | 45° instead of 18° granularity; non-flatness ×1.9 less precise |
| [DP2] | B6 on 4 points, 300 rows, 600 background events per variation | 165 CPU-h (0.8 day) | no variation at 5 keV, at ≥ 1 TeV, or for the scalar |
| [DP3] | no MVA as primary selection; BDT cross-check at counted background | — | the gain is measured, not used |
| [DP4] | S4 and S5 not included | ≥ 1 week, ≥ 600 CPU-h (S4) | efficiency above 3 keV; m_Q, Λ handles |
| [DP5] | Herwig only at generator level and only if it installs without a source build | an install and a chain port | hadronisation-model systematic limited to tunes |

[DP1] and [DP2] are compute-envelope proposals, not failed attempts; JFC 12 requires an attempt first, so they are
put to the user rather than taken. If the user declines them the calendar grows by about 2.6 days.
Triggered later, only after a documented failed attempt: [DT1]–[DT4] (§7).

### 11.6 What risks the 2–4 week target (brief D6)

The target is missed by about two weeks. The cause is production CPU: 1,953 CPU-h of MUST production is 10 days at
200 core-h per day, before reviews. A 4-week schedule would need production near 1,000 CPU-h. The only levers of that
size touch MUST statistics, so they are **not proposed**, only listed for the user:
(i) S1 at 500 rows instead of 2,000 at the 15 points below 1 keV, where v1 found ε ≤ 0.1 (saves 158 CPU-h of chain);
(ii) B2 direct sample at 12,000 events (saves 201 CPU-h; R07 precision 0.17 instead of 0.12);
(iii) B4 hit-level samples at 1,000 events for the eight small processes (saves 56 CPU-h).
Together these save about 415 CPU-h, two days: not enough to reach four weeks. The schedule above is therefore the
proposal. Any overrun of more than 30 % of the approved compute is reported (brief §7).

### 11.7 Decision points of PLAN §8

| # | question | when | if "no" |
|---|---|---|---|
| 1 | is the v1 chain reproducible on Linux (C1) and does the finder pass (C2)? | day 6 | regression; Phase 3 does not start on the failed family |
| 2 | do the estimators close on existing samples at the loose rungs? | day 12 | redesign before the freeze; the freeze moves; user informed |
| 3 | after production: background verdicts, then signal | days 27–33 (Gate B at ≈ 33) | failed terms reported; eligibility rule [SD8] |
| 4 | include the endcap? | — | void: dropped by brief D1 |

---

## 12. Open issues, items for the human, and how this study could fail

### 12.1 Judgment calls (also in `experiment_log.md`)

DECISION: closure criteria are "within a factor F" with F = 1.5 (pile-up, conditionals, sideband) and 2 (single
interaction, hard-scatter tracks), each with a p > 0.05 test that uses the declared systematic and a cap on that
systematic.
ALTERNATIVES: a pure p > 0.05 test without a model width (cannot pass at per-cent statistics for an extrapolation
method; would fail by construction); a looser factor 3 (would allow σ_ln > 1, against the plan's target).
CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES — these numbers decide pass or fail of the paper's core.

DECISION: C1 signal comparison at 400 rows per point, declared outside the blind, restricted to ten v1-rule counts.
ALTERNATIVES: 1,000 rows (D4; more precise than the v1 record, hence a larger look at three R07 efficiencies);
no signal comparison in C1 (brief D5 asks for signal points).
CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES.

DECISION: σ_norm from the NLO computed here; resummation tables as a cross-check only.
ALTERNATIVES: computed NLO × tabulated NNLL/NLO ratio (FEAS_B's recommendation); v1 transcription.
CONFIDENCE: MEDIUM (model validation pending). FLAG FOR HUMAN: YES — it changes every cross section relative to v1.

DECISION: QED FSR on in the nominal v2 signal.
ALTERNATIVES: v1 treatment (off, with a one-sided tilt). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO.

DECISION: the time-tag credit for prompt backgrounds is measured and used if its closure passes.
ALTERNATIVES: no credit, as v1 and as the plan (which omits it). CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES — it can
move the SR-T background by orders of magnitude and was not in the plan.

DECISION: dE/dx selections excluded from T2.
ALTERNATIVES: keep R21–R23 with the frozen tables. CONFIDENCE: MEDIUM. FLAG FOR HUMAN: YES.

DECISION: no MVA as primary selection; the approach comparison moves to Phase 4c.
ALTERNATIVES: BDT as a T2 candidate (its background cannot be estimated). CONFIDENCE: HIGH. FLAG FOR HUMAN: NO
(reviewers must validate the infeasibility argument).

### 12.2 Flagged for the human
1. **The 2–4 week target is not met (≈ 6 weeks).** §11.6.
2. **The endcap wording fixed in brief D1 contains "×1.5", which has no derivation** in the book or the plan (the
   book gives ×3.2 at g = 1 and ×2.1 at g = 0.5; D3 §5). The statement is used as fixed, tagged EST; the user may
   want "×2.1–3.2".
3. **v1 freeze timing** (§8): the paper will say that the v1 analysis code was re-frozen after efficiencies existed.
4. [DP1], [DP2], [DP4], [DP5] and the three MUST levers of §11.6.
5. The tolerances F and the eligibility rule [SD8]: if no selection is eligible, the paper is the "closure fails"
   paper of PLAN §8.
6. The CMS-internal cross-check listed as open work in v1 (D1 §6) is outside the plan and is not done (public
   information only).
7. Book Part VI did not pass its own review (D3 §6.7); every number taken from it is recomputed from the tracked
   JSON before it enters the paper.

### 12.3 Not resolved in Phase 1
- ρ = 2 memory and cost at production size; pre-merge bytes per trial (measured on day 0 of Phase 2).
- Whether the probe-row exclusion of v1 can be rebuilt from the tracked row arrays (§4.1).
- The active Fatras physics list (B1-e).
- Parameters of the MET model, the trigger curve, the timing and vertex efficiencies, the K-factors of the SM
  processes, the cosmic and halo rates: retrieval tasks R-1 to R-11. None is in the repo.
- Finder cost at the frozen road 0.15; cost of MLM and FxFx generation; toy cost for the real workspace.
- R3's and R2's statistical methods (Table 6.1 has "not extracted" cells).

### 12.4 What would make this study fail
1. Both pile-up estimators fail B2-a, or they disagree at the deep rungs: no validated pile-up term beyond R07.
2. The large no-PU samples show passing single-interaction events at a rate that leaves B ≫ 10³: the result is then
   a measured background and a reach below the existing bounds at low mass (plan outcome "real background").
3. The Geant4 → Fatras hand-over cannot be made consistent (parent hits, geometry identifiers).
4. C1 fails for the pile-up family: nothing built on the chain can be trusted until it is understood.
5. The finder fails V4-5: every efficiency and rate is in doubt.
6. The MET model cannot be sourced from public documents: the three additions of B4 stay unquantified.
7. Infrastructure: NFS or cajuela outages (two incidents on day one, `LOG.md`), memory limits for ρ = 2, or a
   production cost above the estimate by more than 30 %.
8. A blinding breach: any v2 signal efficiency seen before the verdicts. The C1 exception is the place to watch.

---

## Code reference
- `python3 -I analyses/quirks_v2/phase1_strategy/src/strategy_budget.py` prints every CPU-h, storage and sample-size
  number of §4 and §11 from the measured unit costs (standard library; milliseconds).
- No pixi task was run and no sample was produced for this document.
