# Binding commitments

Filled by the Phase-1 strategy and frozen at Gate A. Current strategy: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`
("STR" below; version 10, after review cycle 9). Earlier versions of this file referred to
`STRATEGY_brigitte_2026-11-13_17-55.md` (version 1), `STRATEGY_dmitri_2026-11-13_19-25.md` (version 2),
`STRATEGY_emeric_2026-11-13_21-10.md` (version 3), `STRATEGY_fiona_2026-11-13_23-05.md` (version 4),
`STRATEGY_gunnar_2026-11-14_00-50.md` (version 5), `STRATEGY_ingrid_2026-11-14_02-20.md` (version 6),
`STRATEGY_jules_2026-11-14_03-40.md` (version 7), `STRATEGY_leopold_2026-11-14_05-00.md` (version 8) and
`STRATEGY_mireille_2026-11-14_06-55.md` (version 9).
Every MUST and SHOULD item of the publication plan is a "will implement", except S3 (endcap), dropped by the user
(brief D1) and carried as an EST outlook statement.
A status changes only through a logged `[D]` entry (JFC 12) or a user decision; never silently.

**This file is the master list of criterion identifiers.** STR quotes these identifiers and no others.

Columns: "phase" is where the work is done; "deadline" is the last phase at whose review the commitment must be
closed (fulfilled, or reported as failed as pre-declared).
"Within a factor F" is defined in STR §4.0: derivation and test on disjoint rungs and samples; a test rung is
evaluable if σ_tot = √(1/N + s_P²) ≤ ln F/3 (N counted after the cut; effective count for weighted samples);
(c) s_model ≤ ln F/3, fixed before the freeze from development samples (an estimator above the cap is not submitted
and earns no credit); (a) |ln r| ≤ ln F at every evaluable test rung (INVESTIGATE up to ln F + 2σ_tot, FAIL beyond);
(b) χ² with the full covariance and the common s_model, p ≥ 0.05 (INVESTIGATE for 0.05/K ≤ p < 0.05, FAIL below),
K = 10; INVESTIGATE → one re-test on a fresh sample, passed if |ln r′| ≤ ln F and p′ ≥ 0.05/K (a stated departure from
"p > 0.05", STR §5.2). The ceiling tests are a second family: one Šidák-combined verdict per term for the 19 terms
with a ceiling, FAIL at p_t < 0.05/19, INVESTIGATE up to 5 × 0.05/19 with one re-test (STR §4.4). Eligibility follows
the single statement of STR §4.0 point 6. Verdicts: PASS, FAIL, NOT TESTED, NOT EVALUABLE. Every extrapolated factor carries the width s_tot(r) of STR §4.0 point 7 (distance per
quantity; cumulative and crossing test rungs) and every probability is censored at its no-credit value.
Rows marked (DP) carry a downscope proposal that the user decides at Gate A; until then the full form is the commitment.
Rows marked (Q-n) depend on a question the user answers at Gate A, rows marked (Df-n) contain a default the user
can override (STR §12.1); until then the default is a proposal.

## Gate A answers (user, 2026-11-16; FROZEN)

| item | answer |
|---|---|
| Q1 | ● six v1 signal counts of C1 sealed until Gate B, four open |
| Q2 | ● (a) pause and ask at day 15 if the projection exceeds B₅₀ = 300 or both pile-up estimators miss their cap. The optional day-7 rider was **not** taken |
| Q3 | ● yes: an untested MUST closure criterion enters at its ceiling, no credit, selection eligible |
| Q4 | ● approved schedule **4,609 CPU-h**, stop-and-ask at **5,992 CPU-h**, calendar about 60 days; DP1, DP2, DP4 (S4/S5 out), DP5 accepted; contingency 2,150 CPU-h not pre-approved |
| Q5 | ● yes: truth-level signal generation before the hash |
| Df-1 … Df-11 | no override: all eleven defaults stand, including Df-11 (pinned reading of §11.7 rule 1) |
| rule 1 precision sentence (E6) | kept (the user was told twice it could be dropped and did not drop it) |

**Post-Gate-A decision (user, 2026-11-16, stop-rule projection of Phase 2):** the no-pile-up hard-scatter pool keeps
its CPU allocation (457 CPU-h within the approved 4,609; threshold 5,992 unchanged) and its event counts are reduced
to what the measured unit costs allow; the higher zero-count floors of the SM terms are accepted (`LOG.md`,
"option 1"). Rows B4-c and INV-1 and STR Table 4.4a are revised accordingly in the Phase-2 strategy addendum.

Source: the user's message "Q1 ●; Q2 ●; Q3 ●; Q4 ●; Q5 ● . Ok go ahead." (`LOG.md`, 2026-11-16). Day 0 of the
calendar of STR §11 is 2026-11-16.

## Changes of rows in version 10 (2026-11-16, fixer Oscar, review cycle 9: B-1; nothing removed)

| identifier | what happened |
|---|---|
| GA | freeze table of STR §8 counts eleven defaults (B-1); no status changed |
| ST-1 (Q4, Df-11) | marked with the default it depends on; rule 1 states the precision of the binding median and that a reading within it pauses; no status changed |

## Changes of rows in version 9 (2026-11-14, fixer Mireille, review cycle 8: W1; nothing removed)

| identifier | what happened |
|---|---|
| TG-1 (Q2) | §11.7 rule 1 made single-valued (W1): SM processes without a day-15 sample are read through the Z(νν) pilot count; day-15 limit ≈ 12 Z(νν) pilot counts; (c) factors do not multiply a zero-count floor; no status changed |
| GA | eleven defaults: Df-11 (the reading of §11.7 rule 1 pinned in cycle 8, overridable) added (O6, orchestrator-ordered) |

## Changes of rows in version 8 (2026-11-14, fixer Leopold, review cycle 7: V1; nothing removed)

| identifier | what happened |
|---|---|
| TG-1 (Q2) | day-15 reading by branch stated from the script table (V1); (c) rejection bar corrected; the (c) test's treatment of a zero-survivor development fraction stated; no status changed |

## Changes of rows in version 7 (2026-11-14, fixer Jules, review cycle 6: U1; nothing removed)

| identifier | what happened |
|---|---|
| TG-1 (Q2) | §11.7 rule 1 basis of the day-15 projection stated; Q2 (c) test on development estimates (U1); no status changed |

## Changes of rows in version 6 (2026-11-14, fixer Ingrid, review cycle 5: T1–T3 and adopted C items; nothing removed)

| identifier | what happened |
|---|---|
| ST-1 | approved calendar 58 → 60 days: 57.8 days plus the ≈ 2-day turnaround of the expected day-15 pause under Q2 (a) (T3); CPU-h and threshold unchanged |

## Changes of rows in version 5 (2026-11-14, fixer Gunnar, review cycle 4: R1–R5 and adopted C items; nothing removed)

| identifier | what happened |
|---|---|
| B1-f | S_CKF samples: DIF on the enriched test overlays, NI by the rung split, SM on the hit-level halves (R4); paired pile-up-only pass on every SM process, no borrowed mixed excess (R5) |
| B4-c | completeness from the paired pass on each of the fifteen SM processes (R5); first-half R06 rate read on the derivation parity half (G-C9) |
| T1-h | family-wise false FAIL 4.7–4.9 % (G-C2) |
| TG-1 | expected reading conditional on the day-15 pause not firing (R1) |
| S1-a | deadline 4a → 4b: the S1 chain ends after the 4a review (G-C11) |
| REF-2 | R-10 and R-20 before Phase 4a, as STR §6.4 (G-C3) |
| ST-1 | approved figure 4,609 CPU-h (+36 CPU-h paired passes, R5), threshold 5,992 |
| GA | Q2 reworded: the deliverable if the background is large (R1); Q3 routes widened (R2) |

## Changes of rows in version 4 (2026-11-13, fixer Fiona, review cycle 3: P1–P16; nothing removed)

| identifier | what happened |
|---|---|
| B1-a | ceiling and leak tests on the unbiased test overlays only; the enriched overlays serve the S and π_k closure (P4) |
| B1-f | H on all own hits with the CKF factor S_CKF (Df-9, P3); one combined ceiling verdict per term in a family of 19 (P6); leak an implementation check, mixed excess from a paired pile-up-only pass (P5); extended ceiling H′; per-k comparison on the pilot's overlays (P15); sub-topologies without ceiling test (P4) |
| B1-g | the multi-vertex class counted per rung with its trend (Ph-C7) |
| B2-b, B2-f | occupancy crossing credit only in the 2S family (P7); s_model out of sample (Ph-C5) |
| B4-c | pool shares for Z(ττ) and lost-lepton Z(ℓℓ) (P1); staged 4a hit-level production, v1-proxy rates at day 15 (P14); W(τ) forced-decay samples (K-C2); s_model from Z(νν) (N-C11) |
| B5-a, B5-b, B5-c | deadline 4a → 4b (S-1) |
| C2-c | Bonferroni over the 8 tests, \|z\| < 2.73 (K-C9) |
| T1-c, T1-h | four labels; "true λ"; one coverage family of 10 checks against the computed coverage (Df-10, P11) |
| T2-a | eligibility by STR §4.0 point 6, including the ceiling family |
| TG-1 | "target met" needs every leading term labelled estimate (P9) |
| ST-1 | approved figure includes the 156 CPU-h reserve: 4,574 CPU-h, threshold 5,946 (P13) |
| PR-1 | outline adds the ceiling test, the completeness bound, c_mix, S_CKF and the coverage family (P15, P11) |
| INV-1 | rows 13a, 18a, 18b; staged hit-level samples (P1, P4, P14) |
| GA | five questions (Q3 and Q5 reworded) and ten defaults (Df-9, Df-10 added) |
| VC-3 | the ceiling family added to the family-wise rules |

## Changes of identifiers and rows in version 2 (2026-11-13, fixer Dmitri; nothing removed)

| old identifier (version 1 of this file) | new | what happened |
|---|---|---|
| C1-a … C1-d | same | C1-d rewritten (six candidate efficiencies; sealed tier); C1-e added |
| B1-a, B1-b, B1-c | same | criteria rewritten (held-out test; width always added; no ×2 band) |
| B1-d (geometry and Fatras physics list) | B1-d | unchanged content |
| — | B1-e, B1-f, B1-g | added: biased generation; attribution, promotion and ceiling; sources not in v1's list |
| B2-a, B2-b | same | each is the closure of one estimator, as before |
| B2-c (agreement and trend) | B2-c (agreement) + B2-f (extrapolation width) | split; the "2σ trend" rule is replaced by a width that is always added |
| B2-d, B2-e | same | unchanged |
| — | B2-g | added: thinning reach measured before the freeze |
| B3-a … B3-c | same | criterion changed (counts after the cut; no credit when untested); B3-d added |
| B4-a … B4-d | same | B4-b validation changed; B4-e added |
| B5 | B5-a, B5-b, B5-c | one row split into its three criteria |
| B6 | B6-a … B6-d | one row split; B6-c and B6-d are new criteria |
| T1-a (schema and v1 mode) | T1-a (schema) + T1-b (v1 mode) | split |
| T1-b (validation checks) | T1-c … T1-h | split and redefined (zero-count tests, injection, pulls, ranking, asymptotic table, coverage) |
| T1-c (toys primary) | T1-i | renamed; two passes |
| T2-a (rule, list, G, salt; reproducible; shift) | T2-a, T2-b, T2-c | split |
| T2-b (background-free flag) | T2-f | renamed |
| — | T2-d, T2-e, T2-g | added: background-side bias; robustness against empty simulation; baseline |
| S1-a (rows and no fast path) | S1-a + S1-b | split |
| S1-b (blind aggregation) | S1-c | renamed |
| — | S1-d, S1-e, S1-f | added from STR (statistical quality reported; hash split; signal detector response) |
| S2-a (validations) | S2-a + S2-b | K(m) with errors is its own row |
| S2-b (f₂₀₀), S2-c (QED FSR), S2-d (trigger) | S2-c, S2-d, S2-e | renumbered to the STR order |
| — | S2-f | added: infracolour Coulomb correction |
| — | TG-1, ST-1, INV-1, BL-1, FP-1, GA | added (non-plan commitments) |

## Changes of identifiers and rows in version 3 (2026-11-13, fixer Emeric; nothing removed)

| identifier | what happened |
|---|---|
| GA-1 … GA-10 (markers of version 2) | replaced by Q1–Q5 and Df-1–Df-8: GA-1 → Q1; GA-3 → Q2; GA-4 → Q3 (what an untested MUST criterion earns) and Df-2 (technical rules); GA-7, GA-8 → Q4; GA-2 → Df-1; GA-5 → Df-3; GA-6 → Df-4; GA-9 → Df-5; GA-10 → Df-6; new: Q5, Df-7, Df-8 |
| B1-a | terms are now DIF and NI (three radii); PV pairs, γ, V⁰ and loopers are counted by B4 (one route per origin); NI tested at R05 by a rung split |
| B1-f | adds: classes on hit subsets, k per layer type, one-sided ceiling test, completeness test |
| B1-g | ratio test replaced by own-z placement, single counting and a truth-attributed test |
| B2-a, B2-b, B2-f, B1-b, B3-d | crossing test rungs added; widths by the corrected rule |
| B3-c | closure on prompt candidates; credit limited to the deepest tested window edge |
| B4-c | W(τ_h), W(τ_ℓ), tt̄ 1ℓ sized for an evaluable test half; wording aligned with STR (R06, and R07 where evaluable) |
| T1-c, T1-e, T1-h, T1-i | fifth test (censoring); per-nuisance pull reading; true rates stated; "toy-based for every quoted limit" |
| T2-a | all 16 candidates frozen at Gate A; eligibility by direction of the failure and the ceiling test |
| — → T2-h | added: the estimate-only selection and the monotone-prior sensitivity |
| TG-1 | "target met" needs σ_ln ≤ 1, f₀ ≤ 0.5 and no leading bound or no-credit term |
| GA | now five questions and eight defaults |

## Items of the publication plan

| id | priority | commitment | acceptance criterion (short; full text in STR) | phase | deadline | status |
|---|---|---|---|---|---|---|
| C1-a | MUST | Rerun the v1 code with logged port edits and the frozen configuration (T_seed 4, road 0.15) on the declared subset: pile-up ρ = 1 (4,000 events) and ρ = 2 (1,000), no-PU and C′_PU samples, Z(νν), rates, three signal points (E 200 at 1.5 and 2 keV, E 500 at 3 keV; 400 rows each) | 41 declared comparisons with `C12FC_v1`: each p > 0.05/41, global χ² below its 99th percentile, family coherence \|z\| < 3; power stated; fail → investigated, not tuned (STR §4.1) | 2 | 2 | open |
| C1-b | MUST | v2 analysis arithmetic applied to the v1 recorded counts | central values to 10⁻⁶, B₈₄ within 1 % (STR §4.1) | 2 | 2 | open |
| C1-c | MUST | Linux environment: tracked lockfiles, container recipe, jobs ≤ 30 min through the resumable runner | one C1 job rerun in the container with identical output hash (STR §4.1) | 2 | 5 | open |
| C1-d (Q1) | MUST | Blinding rule for the C1 signal counts. **Six** of the ten are efficiencies of v2 candidate selections (R07 × 3; fallback FB2/FB3 × 3 = T2 family F). Default: R04 and R06 counts open (4); R07 and fallback counts (6) compared by a dedicated agent that reports only PASS/FAIL, counts sealed until Gate B. C1 rows are never part of S1. All 16 T2 candidates stay in the list as declared. The exception to the blinding invariant takes effect only with the user's approval | tier approved by the user recorded in `PREREG_v2.md`; sealed file outside the repository tree, encrypted, with sha256 in the ledger, unread before the verdicts; family-coherence z and global χ² with sealed quantities reported as PASS/FAIL only; no other signal quantity in any Phase 2–4a artifact except those of BL-1 (STR §4.1) | 2 | 4b | open |
| C1-e | MUST | Chain per C1 signal point as in v1 (fast path at E 200 with 1.5 and 2 keV, full chain at E 500 with 3 keV); full-chain twins of the two fast-path points | twin ratio full/fast reported against the declared expectation (×0.832 at R04, ×0.871 at the fallback); fallback ratio sealed with the tier of C1-d (STR §4.1) | 2 | 2 | open |
| C2-a | MUST | V4-5 brute-force cross-check on 50 signal + PU events and 50 PU trials (new code) | \|Δn\| < 1 mrad against the brute-force optimum and against the independent fit in ≥ 48/50 and ≥ 48/50; disagreements inspected; no pass fraction readable from the output; the "optimality" count is taken in Phase 4c only (STR §4.2) | 2 | 2 (optimality count: 4c) | open |
| C2-b | MUST | V4-4 as defined in v1: reproducibility and seeds, 20 jobs | bit-identical reruns on the same node; different seeds differ; seeds recorded (STR §4.2) | 2 | 2 | open |
| C2-c | MUST | Seed-threshold stability T_seed 4 → 2 (the test the plan mislabels V4-4) | \|z\| < 2.73 for the pass fraction of every rung family at ρ = 1 and 2 (Bonferroni over the 8 tests, family-wise 4.9 %); fail → reported, T_seed not retuned (STR §4.2) | 2 | 2 | open |
| C3 | MUST | Paper corrections: all 24 items of D3 §1, the 19 label families of D2 §5, novelty wording, `ERRATA_v1.md`, disclosure of the AI workflow and CMS membership, number tags | checklist with file:line per item; zero grep hits for internal labels; two primary-source checks logged (STR §4.3) | 5 | 5 | open |
| B1-a | MUST | Geant4 (FTFP_BERT) vertices handed to Fatras; terms: decays in flight and nuclear interactions at three radii, hard-scatter share and ×200 minimum-bias share; estimator P_geo·S + Σ f_k·π_k (pass and near-pass probabilities without pile-up, survival, promotion) | held-out closure per term within a factor 2. DIF: survival and promotion derived on derivation overlays at R04–R05, tested on test overlays with other seeds at R06–R07 (attributed counts), sized for an expected 31 counts at R06, 24 needed (up to 7,750 unbiased events); the ceiling and leak tests use only the unbiased test overlays. NI: derived at R04, tested at R05 on 1,000 unbiased overlays per radius (rung split). Verdict classes of STR §4.0 (STR §4.4, Table 4.4b) | 3 / 4a | 4a | open |
| B1-b | MUST | Extrapolation of the pile-up factors beyond the test rungs | S = 1 beyond its tested rungs; promotion carries s_tot(r), always in the likelihood and censored at 1; b̂, σ_b, the crossing terms s_f and s_tot tabulated per T2 candidate (STR §4.0, §4.4, §4.12) | 4a | 4a | open |
| B1-c | MUST | Geant4 rates, per term and per share (hard scatter, ×200 minimum bias), cross-checked against the v1 generator rates | agreement within the combined uncertainty of the physics-list difference (measured), the sourced material uncertainty (R-17) and statistics; outside → reported as failed cross-check, Geant4 rate kept (STR §4.4) | 3 | 4a | open |
| B1-d | MUST | Geant4 geometry identical to ACTS; active Fatras physics list recorded | \|Δ(x/X₀)\| ≤ 1 % per layer, positions to 1 µm; hadronic interactions and decays of charged pions and kaons off in Fatras, so that nothing is counted twice (STR §2, §4.4) | 3 | 3 | open |
| B1-e | MUST | Biased generation of the stiff tail with weights; soft bulk excluded by an analytic sagitta bound; Phase-2 pilot measuring the gain | weights closure biased against unbiased at R05 within a factor 1.5; bound written with its scattering allowance and checked at R05–R06; gain per term recorded before the freeze; biased generation used whenever its closure passes, pool re-allocated as √(N_t/(c_t·G_t)); fail → unbiased generation (STR §4.4) | 2 / 3 / 4a | 4a | open |
| B1-f (Df-9) | MUST | Attribution rule (attributed / mixed / pure pile-up by truth); no-pile-up classes on subsets of the term's **own hits, all of them (before CKF)**, k per layer type; CKF removal and f_CKF < 0.2 as a survival factor S_CKF, credited only where tested (DIF R06, and R07 where evaluable, on the enriched test overlays with their weights; NI R05 by the rung split; each SM process R06 on its hit-level halves), carried with s_tot, censored at 1; promotion from the correlated occupancy model; no-credit ceiling H = P_geo + Σ f_k counted at every T2 candidate and **tested as a ceiling** | rule in `PREREG_v2.md` (v1's coded rule transcribed and compared); table of fixed cuts and their monotonicity; H tabulated; per-k promotion comparison on the pilot's 1,000 near-pass overlays (sample 11; its r.m.s. is the s_model of the promotion model; fewer than two classes with 24 promoted events → not submitted, term at H); one combined ceiling verdict per term (Šidák over its rungs) in a family of 19 terms, FAIL at p_t < 0.05/19, INVESTIGATE up to 5 × 0.05/19 with one re-test, on unbiased samples only, effective counts for weighted samples; sub-topologies (γ, V⁰, prompt pairs, loopers) completeness and diagnostic populations only; completeness test: leak fraction as an implementation check, mixed excess from a paired pile-up-only finder pass (term hits removed) on the unbiased B1 test overlays and on 1,000 test-half events of each of the fifteen SM processes, 95 % upper limit of (leak + mixed excess)/attributed ≤ 0.26 at R04–R06, carried as c_mix; not PASS → STR §4.0 point 6 (extended ceiling H′ = P_geo + Σ_all k f_k unless redesigned); first on development samples (sample 13a, the pilot, sample 5; fixed before the freeze), then on the test samples (STR §4.4) | 2 / 3 / 4a | 4a | open |
| B1-g | MUST | Pile-up-vertex secondaries (v1 has them in rate_t at the PV): own-z placement of the ×200 minimum-bias share; each secondary counted once (never in the pile-up overlays); noise and out-of-time hits; δ-rays and merged clusters | truth-attributed count of secondary-induced candidates at R04–R07 on 1,000 pile-up events with Geant4 secondaries against the B1 prediction; the multi-vertex class counted directly at every rung with its trend; above a factor 2 of the one-vertex prediction at a rung with N ≥ 24, or rising in share with depth → a B1 term before the freeze; noise and out-of-time occupancy from R-18 against the top-up; δ-rays under limitation L8 (STR §2) | 3 | 3 | open |
| B2-a | MUST | Repaired thinning: pre-merge candidates stored at ρ = 2 (N_IP2 ≥ 6), 64 thinned subsets per trial, grouping re-applied per subset | reproduces direct counts within a factor 1.5 at R04–R07 and at the crossing test rungs; no scale-factor patch (STR §4.0, §4.5) | 2 / 3 / 4a | 4a | open |
| B2-b | MUST | Independent semi-analytic occupancy estimator (new code); inputs derived on development samples at R04–R05 | reproduces direct counts within a factor 1.5 at the held-out R06–R07 and at the 2S crossing test rungs; its fit-probability and shape crossing comparisons are consistency checks without distance credit, because it takes those pass fractions from finder candidates (Df-2); s_model at a development rung not used for its inputs (or the in-sample value if larger); not submitted if above 0.135 (STR §4.0, §4.5) | 3 / 4a | 4a | open |
| B2-c | MUST | Agreement of the two estimators beyond R07 | within a factor 1.5 (STR §4.0 criterion with r = B_thin/B_occ) at every rung where thinning is evaluable; elsewhere NOT EVALUABLE, and the pile-up term is declared a one-estimator extrapolation (STR §4.5) | 4a | 4a | open |
| B2-d | MUST | Direct ρ = 1 sample of 24,000 events (96,000 trials), independent of development samples | ≈ 70 expected counts at R07 (σ_ln ≈ 0.12, evaluable for F = 1.5 with probability 0.97 at s_P = 0) | 4a | 4a | open |
| B2-e | MUST | ρ = 2 memory and pre-merge storage measured before any campaign | RSS against events per job recorded; job packing and storage threshold set from it; cap 400 GB (STR §4.5) | 2 | 2 | open |
| B2-f | MUST | Extrapolation width of both pile-up estimators | b̂, σ_b, s_f, s_tot(r) per estimator and T2 candidate by the rule of STR §4.0 point 7 (occupancy model: crossing credit in the 2S family only); in the likelihood always; evaluability of the crossing rungs written into `PREREG_v2.md` (STR §4.0, §4.5) | 4a | 4a | open |
| B2-g | MUST | Thinning reach | N_eff per rung measured on the 1,000-event development sample; deepest evaluable rung written into `PREREG_v2.md` (STR §4.5) | 2 / 3 | 3 | open |
| B3-a | MUST | Conditionals for the shape rungs (h, o) per term on the no-PU samples | each within a factor 1.5 in the stability test of B3-d, counts after the cut; failed or untested → no credit (STR §4.6) | 3 / 4a | 4a | open |
| B3-b | MUST | Displaced-vertex veto, designed on background samples only | same criterion; selections with and without it both in T2 (STR §4.6) | 3 / 4a | 4a | open |
| B3-c (Df-5) | MUST | Time-tag (late-hit) fraction for prompt terms, measured at hit level with a timing model that has sourced tails | closure on truth-attributed prompt candidates at R04 (SM hit-level samples, B1 test overlays) at five window edges down to the nominal one, within a factor 1.5; independence from the rung at R04–R06; credit = p_late at the deepest edge with an evaluable PASS, no extrapolation in t_cut, never below the sourced tail fraction; tails not sourced → no credit (STR §4.6) | 2 / 3 / 4a | 4a | open |
| B3-d | MUST | Transfer of each conditional from the rung where it is measured to the rung where it is applied | measured after ≥ 3 preceding rungs; derivation on the first two, test on the deepest, on disjoint halves; width s_tot(r) from the distance; censored at 1 (STR §4.0, §4.6) | 3 / 4a | 4a | open |
| B4-a | MUST | Hit-level samples for the eight proxied processes | proxy fraction of B_SM = 0 at every rung (STR §4.7) | 3 / 4a | 4a | open |
| B4-b | MUST | Z(ττ), lost-lepton Z(ℓℓ), multijets with a reconstruction-level MET model built from cited public parametrisations (soft term from the public source only) | external validation against a published Phase-2 MET performance figure at pile-up 200 within the pre-declared tolerance; multijet yield stable within a factor 2 under bias changes; comparison with v1 and with a published multijet fraction reported without verdict; tail variation as nuisance; not validated → full variation as width, stated; no parameters from two public sources → MUST infeasible after a real attempt, stop and ask (STR §4.7) | 3 / 4a | 4a | open |
| B4-c (Q3) | MUST | Hard-scatter terms (every candidate from hard-scatter-vertex particles, including prompt pairs, conversions, V⁰ and loopers) with the estimator of B1 (one s_model, derived on the Z(νν) development sample and the pilot); no-PU samples from the common pool (3.65×10⁷ events over fourteen processes by √N_trig, Z(ττ) and lost-lepton Z(ℓℓ) at planning N_trig, re-allocated at day 12–15 from the MET model) | closure within a factor 2: derivation half at R04–R05, test half at R06 (and R07 where evaluable); also reported by truth sub-topology as consistency checks. Hit-level samples sized for an expected N_eff of 31 in the test half (24 needed), with v1-proxy rates at day 15 and **staged** 4a production (first half produced, R06 rate measured on its derivation parity half, second half sized from it; top-up from the reserve or a reported conditional draw): Z(νν) 10,000, W(τ_h) 11,250, W(τ_ℓ) 7,662 (two forced-decay samples), tt̄ 1ℓ 23,880 events. Completeness of every process from the paired pile-up-only pass on 1,000 of its own test-half events (no borrowed excess). The eight proxied processes and the three additions at 2,000 events: expected NOT TESTED, entering at H after the ceiling test if the user grants the exception to brief D4 (Q3; every route of the annex), else sized at the cost of the annex (STR §4.7, §12.1) | 4a | 4a | open |
| B4-d | MUST | Cited K-factors; generator comparison for Z(νν)+jet and W+jet rates | every K has a citation; generator difference is the normalisation nuisance; no second generator for tt̄ and dibosons, stated (STR §4.7) | 2 / 3 | 4a | open |
| B4-e | MUST | Multijet plane probability from a looser population | factorisation tested on Z(νν) and W in MET bins within a factor 1.5; not flat → passing events only, floor stated (STR §4.7) | 3 / 4a | 4a | open |
| B5-a (DP1) | SHOULD | Road-rotation sideband: flatness of the hard-scatter component | sideband prediction of the signal-road count within a factor 1.5 at the evaluable rungs of R04–R07, on truth-attributed hard-scatter candidates; signal road counted on all 10,000 Z(νν) hit-level events; valid only as far as B5-c holds. Full: 20 roads on 8,000 SM events; proposed reduced: 8 roads on 6,000 (R07 then not evaluable with pile-up); runs in days 36–48 (S-1), stated as pending in the 4a note (STR §4.8) | 3 / 4a–4b | 4b | open |
| B5-b | SHOULD | Non-flat part quantified | T_meas/T_flat − 1 per process with its error, on the no-PU hard-scatter samples (STR §4.8) | 4a–4b | 4b | open |
| B5-c | SHOULD | Independence of roads | pair correlation \|ρ\| < 0.1 at R05 and R06 on samples with pile-up, or an effective-trials factor (STR §4.8) | 4a–4b | 4b | open |
| B6-a (DP2) | SHOULD | Seven detector-model variations (resolution ×1.5, inefficiency 97 % incl. pile-up hits, material ×0.5 and ×2, top-up low and high, alternative tune) run as robustness tests, paired with nominal partner samples | every variation evaluated with error on ln(B_var/B_nom) < 0.1 at R06 and on ε_var/ε_nom < 10 %. Full: 6 signal points; proposed reduced: 4 (E 200/1.5, E 500/3, E 500/5, E 1000/3 keV) with the interpolation rule (STR §4.9) | 3 / 4a | 4b | open |
| B6-b | SHOULD | Classification | robust / not robust by the pre-declared thresholds; "not robust" items in the limitations (STR §4.9) | 4a | 4b | open |
| B6-c | SHOULD | Every shared detector nuisance evaluated on every term: pile-up, single-interaction, SM hard scatter, signal | table of STR §4.9 filled; P_geo and H re-measured under each variation; where the reruns count zero the shift is measured at the deepest rung with counts and carried with s_tot; for bounded terms the nuisances act through H and the conditionals | 4a | 4b | open |
| B6-d (Df-7) | SHOULD | Sizes of the detector nuisances from public Phase-2 numbers (R-15 to R-17, by day 15); round-number variations are not nuisances | each nuisance has a cited size; effect scaled linearly from the measured shift, linearity checked on material; no public number → no nuisance, and the μ₉₅ shift of the robustness test is reported beside the headline limit and named in the abstract-level limitations above 10 % (STR §4.9) | 2 / 4a | 4a | open |
| B7 | SHOULD | Cosmic, beam-halo and beam-gas background as a number from public rates, pointing and timing | number with derivation; below 10 % of the 1σ uncertainty of the total background → stated, else a term of the likelihood (STR §4.10) | 3 | 4a | open |
| T1-a | MUST | pyhf workspace: Poisson auxiliary channel per simulated count (zero counts included; one per weight class), correlated nuisances, one route per term, closure-derived systematics with probabilities censored at their no-credit value; published | schema-valid (STR §4.11) | 3 | 4a | open |
| T1-b | MUST | v1 mode | reproduces the v1 best-point hybrid-toy limit μ₉₅ = 789.7 (1.2458×10⁷ events before selection / 15,775) within 10 % (STR §4.11) | 3 | 4a | open |
| T1-c | MUST | Zero-count convention: expected limits generated with each counted rate drawn from Gamma(m + 1), auxiliary observations fixed; one zero per term; terms labelled no credit / bound / low count / estimate; f₀ reported | (i) one-bin m = 0 workspace reproduces the analytic limits within toy error; (ii) m = 100, 1000 reproduces the standard toy limit; (iii) coverage on 500 pseudo-experiments per (point, λ) with true λ = 0.5, 1.14, 2, 3, passing the coverage-family rule of T1-h; (iv) limit at the best point under the fixed-1.14 and Jeffreys alternatives reported; (v) coverage with the censoring on and off reported (STR §4.11) | 3 / 4a | 4a | open |
| T1-d | MUST | Signal injection (conventions check 2) | at 0, 1, 2, 5 × μ₉₅^exp of three points, 200 fluctuated pseudo-experiments each: \|⟨μ̂⟩ − μ_inj\| ≤ 0.20 μ_inj; at 0: within 3 standard errors of the mean (STR §4.11) | 4a | 4a | open |
| T1-e | MUST | Pulls and constraints (check 3) | pulls on fluctuated pseudo-data (mean within 0.21; \|pull\| > 2 in at most 10 % of the fits per nuisance); constraints on Asimov data, any below 0.5 of the prior explained (STR §4.11) | 4a | 4a | open |
| T1-f | MUST | Impact ranking (check 4) and pruning policy | ranking compared with expectation; pruning only below 1 % impact each and 5 % of the leading systematic in total (STR §4.11) | 4a | 4a | open |
| T1-g | MUST | Asymptotic against toy limits | tabulated at every point (STR §4.11) | 4b / 4c | 4c | open |
| T1-h | MUST | Coverage at a known signal (replaces the version-1 "toy self-consistency 50 ± 4.5 %", which was true by construction) | 500 pseudo-experiments at two points with μ_true = μ₉₅^exp, true rates λ = m + 1, simulated counts redrawn, limits from stored distributions. **Coverage family (Df-10):** T1-c (iii) and T1-h are one family of 10 checks against c_ref, the convention's computed coverage at the workspace's κ and λ (at most 0.95): FAIL below k_F with P(X < k_F \| c_ref) ≤ 0.005 (462 of 500 at 0.95), INVESTIGATE up to the one-check 5 % point, one re-test on 500 new pseudo-experiments; family-wise false FAIL 4.7–4.9 % (STR §4.11) | 4c | 4c | open |
| T1-i (Df-8) | MUST | Every quoted limit is toy-based | pass 1 at 4b (five best selections, 20 window points); pass 2 at 4c (chosen, runner-up, v1 fallback at 40 points); toys parametrised in f_T with an exact-toy check at three points per selection, exact toys everywhere if the check fails; stated μ grid and CLs interpolation; toy cost measured on a 60–100-parameter workspace in Phase 2 (STR §4.11) | 2 / 4b / 4c | 4c | open |
| T2-a (Q3) | MUST | Selection rule: 16 declared candidates, all frozen at Gate A; eligibility by the single statement of STR §4.0 point 6 ([SD8]: FAIL by under-prediction of a leading term's estimator or a ceiling FAIL in the family of 19 → not eligible; FAIL by over-prediction with the ceiling valid → term at H; completeness not PASS → extended ceiling H′; NOT TESTED / NOT EVALUABLE / not submitted → no credit, for MUST criteria only under Q3), figure of merit G on the optimisation half with ε̂ = (k + ½)/(n + 1), split by a salted hash | rule, list, G, estimator and salt in the hashed pre-registration before S1 production (STR §4.12) | 3 | 3 | open |
| T2-b | MUST | Reproducible choice | second run from frozen inputs gives the same selection; else Gate B is not requested (STR §4.12) | 4b | 4b | open |
| T2-c | MUST | Optimisation-to-evaluation shift | reported per point; mean shift above 2σ reported as selection bias (STR §4.12) | 4c | 4c | open |
| T2-d | MUST | Background-side bias of the choice | 50 bootstrap replicas of the background inputs: frequency of the same winner and shift of its B₈₄ reported; tie rule if the winner wins in fewer than half (STR §4.12) | 4b | 4b | open |
| T2-e | MUST | Robustness against empty simulation | for the deepest candidate G under the convention is worse than with the zero-count terms dropped by more than the toy error, and its one-bin analogue reproduces the analytic limits, on v1 counts before the freeze (STR §4.12) | 3 | 3 | open |
| T2-f | MUST | "Background-free" (B₈₄ ≤ 0.11 per category, B₈₄ from the predictive distribution) reported as a flag only | flag in the results table (STR §4.12) | 4b | 4c | open |
| T2-g | MUST | Always-eligible baseline "R07-direct" (direct attributed counts and direct bounds only) | evaluated in every outcome; partial-outcome matrix of STR §4.12 followed | 4b | 4c | open |
| T2-h (Q2) | MUST | The estimate-only selection: the best candidate whose leading terms are all labelled "estimate" (m ≥ 4, estimators PASS), reported beside the T2 winner | its G and reach in the results table and quoted in the abstract beside the winner (R07-direct in its place if no candidate qualifies); the winner's G under a monotone prior for nested rungs reported (STR §4.12) | 4b | 4c | open |
| S1-a (Df-1, Q5) | MUST | 2,000 rows at each of the 40 points through the full chain (×10 rows in total, ×5 on the evaluation half that sets the limit; 4,000 rows if the user chooses so) | ≥ 99 % of jobs complete with ingestion closure; string propagation after A is fixed (days 12–19), before the hash only if the user confirms the reading of brief D7 (Q5) (STR §4.13, §4.17) | 3 (string) / 4a (chain) | 4b | open |
| S1-b | MUST | No fast path | no fast-path number in any result (STR §4.13) | 4a | 4c | open |
| S1-c | MUST | Efficiencies blind until the closure verdicts; evaluation half aggregated only after Gate B | first aggregation logged at 4b (optimisation) and 4c (evaluation) (STR §4.13) | 4b / 4c | 4c | open |
| S1-d | MUST | Statistical quality stated in advance, reported, never tuned | binomial error per point in the results table (STR §4.13) | 4c | 4c | open |
| S1-e | MUST | Optimisation/evaluation split by the frozen salted hash, independent of Λ | salt in `PREREG_v2.md`; two campaigns, two directories (STR §4.12, §4.13) | 3 / 4a | 4a | open |
| S1-f | MUST | Signal detector response consistent with the backgrounds: same MET model; migration across the 200 GeV generator cut measured on a 150 GeV sample; lepton-veto and calorimeter assumption stated; tracker hit-time window from a public source | A and m_mig computed once, after the MET model is fixed (order of STR §4.1); m_mig quoted (≤ 5 % neglected, else generator cut lowered before the string propagation); limitation L11 with the limit as a function of veto survival unless R-13 gives a number; hit-time loss as a systematic at ≥ 1 TeV or limitation L12 (STR §4.13) | 2 / 4c | 4c | open |
| S2-a | MUST | NLO K-factors computed with `loop_quirkE`, used only after three validations | model identity \|z\| < 3 and 0.5 %; fixed-order NLO against fixed-order NLO slepton reference within 3 % (or NOT EVALUABLE if no such reference, stated); differential K(M) against Drell–Yan within 2 % or 3σ; fail → v1 transcription labelled as such (STR §4.14) | 2 | 2 | open |
| S2-b (Df-3) | MUST | K(m) with scale and PDF errors for all masses; PDF4LHC21 and CT18NLO; resummed normalisation implemented as cross-check | table of σ_norm(m) with both PDF sets; every limit also quoted with σ_NLO × (NLO+NLL)/NLO (STR §4.14) | 2 | 4c | open |
| S2-c | MUST | f₂₀₀ recomputed with one definition (no η cut) and its uncertainty rebuilt and propagated into the limits | one script, one definition in text; scale, PDF, merging-scale, tune and FxFx (500 and 1,500 GeV) comparisons; nuisance in T1 (STR §4.14) | 2 | 4a | open |
| S2-d | MUST | QED-FSR shower is the nominal signal; FSR-off kept for C1 and for the quoted shift | nominal samples showered with the QED-FSR card (STR §4.14) | 2 | 2 | open |
| S2-e | MUST | Trigger turn-on from a public Phase-2 curve, with a nuisance; any threshold change decided before A is computed | cited figure and page; else reported "parametrised, not sourced" with the pre-declared wide nuisance (STR §4.14) | 2 | 4a | open |
| S2-f (Df-3) | MUST | Infracolour Coulomb correction to the production cross section, per mass, from the generated β distribution | number per mass with its source (R-12) or the label "not sourced"; default: one-sided band on the theory line (STR §4.14) | 2 | 4a | open |
| P1-a | MUST | Floor tests: extended-precision step map and mantissa-truncation kernel (both new code) | executed and read against the pre-declared table (floor / physical / inconclusive) (STR §4.15) | 2 | 2 | open |
| P1-b | MUST | B*-off as a paired test with power (≈ 970 events at 5 keV) and at 1 keV; the configuration of v1's test resolved first | pre-declared reading at 3σ (5 keV) and 2σ (1 keV) (STR §4.15) | 2 | 2 | open |
| P1-c | MUST | Population estimator for c defined in advance (paired median) and evaluated on new events; original gate reported as failed | \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at five points on 300 new events each (STR §4.15) | 2 | 2 | open |
| P1-d | MUST | Validity window stated as measured; failed straight-string ratio kept visible; Linux difference of one Stage-1 run followed up | table per (point, Λ, k_B bin) from the tracked results; text follows it (STR §4.15) | 2 | 5 | open |
| S3 | SHOULD | **dropped by user decision (brief D1)**; barrel-only paper; endcap gain stated as an EST outlook exactly as fixed in the brief | n/a | 5 (text) | 5 | dropped (user) |
| S4 | COULD | optional; strategy recommends not including it (DP4): ≥ 1 week and ≈ 740 CPU-h, delays the freeze | — | — | — | out (DP4 accepted at Gate A, 2026-11-16) |
| S5 | COULD | optional; strategy recommends not including it (DP4): negative result stated instead | — | — | — | out (DP4 accepted at Gate A, 2026-11-16) |

## Commitments from the strategy that are not plan items

| id | commitment | acceptance criterion (short) | phase | deadline | status |
|---|---|---|---|---|---|
| PR-1 | `PREREG_v2.md` hashed and committed before any v2 production sample; contents of STR §8 (including the number s_model per estimator and its comparison with the cap, derivation and test rungs, crossing rungs, size and power per test, K = 10, the censoring bounds, the zero-count convention; the ceiling test with its family of 19, the completeness bound and c_mix, the CKF factor S_CKF, the extended ceiling H′, the T1 coverage family); drafted in channel (iii) from day 12 of Phase 3; analysis code frozen before production | 4-bot review PASS; sha256 in git before the first production marker; user notified | 3 | 3 | open |
| PR-2 | v1 kept by hash in an appendix, with the lost files listed and the freeze timing of the v1 analysis code stated | appendix text matches STR §8 | 5 | 5 | open |
| MVA-1 (DP3) | BDT cross-check with a pre-registered recipe, at equal total directly counted background; dE/dx forgone-gain ratio | ε_BDT/ε_R07 with one alternative architecture, and ε(R_k + dE/dx)/ε(R_k) for the chosen selection, both on the evaluation half (STR §3.2, §4.12) | 4c | 4c | open |
| REF-1 | Reference analyses R1–R4 tabulated; comparison targets of STR §6.2 overlaid on the limit and reach figures; "3 and 5 events at B = 0" reach quoted with v2 efficiencies; like-for-like efficiency breakdown against R1 Table I | present in the Phase-4a note (placeholders) and final in 4c | 4a / 4c | 4c | open |
| REF-2 | Retrieval tasks R-1 to R-20 (STR §6.4) from public sources, logged; nothing quoted from memory. Deadlines: R-2, R-3 by day 5; R-7, R-15 to R-18 by day 15; R-12, R-14 before the freeze; R-10 and R-20 before Phase 4a | each closed with a citation, or its dependent commitment reported as not sourced with the consequence fixed in STR §6.4 | 2 / 3 | 3 | open |
| FIG-1 | The seven flagship figures, the supporting figures and the seven diagrams of STR §9 | all present in the paper and the note | 4a–5 | 5 | open |
| RQ-1 | The 25 referee questions answered with a pointer to the text (STR §10) | adversarial review at Phase 5 | 5 | 5 | open |
| TG-1 (Q2) | Central target as a reported outcome: total σ_ln = ½ ln(B₈₄/B₁₆) per category, f₀, the term labels (no credit / bound / low count / estimate), the floor and projection tables and the outcome class (good / middle / real background / closure fails; estimated or bounded) | reported at the chosen selection with the pre-declared reading: "target met" only if σ_ln ≤ 1 in both categories **and** f₀ ≤ 0.5 **and** every leading term is labelled estimate; otherwise "target not met: width small, background bounded (f₀ = …)", naming the labels; "sample-size limited" if f₀ > 0.5, with the conservative (84 %) band edge quoted first. Each label printed with its s_tot. Expected reading: "target not met: sample-size limited" while the ceilings count few events, if the day-15 pause does not fire (by v1's conversion counts the expected branch is a measured background, STR §0, Q2) (STR §4.4, §4.11) | 4a / 4c | 4c | open |
| ST-1 (Q4, Df-11) | Stop rules of brief §7 and D6, as quoted in STR §11.6. Approved schedule (default): 4,609 CPU-h (4,453 + the 156 CPU-h day-15 reserve) and 60 days (57.8 days plus the ≈ 2-day turnaround of the expected day-15 pause; a redesign under Q2 (c) is not included and is reported as an overrun); threshold 1.3 × 4,609 = 5,992 CPU-h. Every overrun of the approved schedule reported, a draw on a conditional cost or on the contingency included; a projected compute overrun above 30 % stops the study and the user is asked; a MUST item infeasible after a real attempt stops the study; cajuela 2.0 TB / 1.0 TB free | re-projection with measured costs at day 5, at the freeze, weekly in production and when a conditional cost is drawn; decision-point-2 rules of STR §11.7 (rule 1 preliminary at day 7, binding at day 15); record in `STATUS.md` | 2–5 | 5 | open |
| INV-1 | Sample inventory with roles (development / derivation / test / production / reserve), seed streams and independence (STR §4.17) | every produced sample matches a row (including 13a, 18a, 18b; the 4a hit-level samples in two stages); no development sample enters a closure verdict; `DATA_MANIFEST.md` carries the stream names | 2–4a | 4a | open |
| BL-1 | Complete list of signal quantities that exist before the closure verdicts: the C1 tier approved in Q1; A, f₂₀₀ and the migration fraction (selection-independent; A and m_mig computed once, after the MET model) | no other signal quantity in any artifact before the verdicts; B6 efficiency ratios and the tracker hit-time loss formed only after them (STR §4.1) | 2–4a | 4b | open |
| FP-1 | Failure protocol after the freeze: ticket always; bug → dated addendum and one re-test on a fresh sample; no bug → reported as failed, [SD8] | each FAIL or INVESTIGATE closed along one of the three branches; fresh samples as named in STR §8 (second direct sample, test overlays, hit-level test halves, pool slice), each used at most once and reported as an overrun | 4a | 4a | open |
| GA | The five questions (Q1–Q5) and the eleven defaults (Df-1–Df-11) of Gate A (STR §12.1) | each question answered by the user and each override recorded in `LOG.md`; rows marked (Q-n) or (Df-n) updated by a logged entry | 1 | 1 | done (2026-11-16, section "Gate A answers") |

## Systematic plan (STR §5; every "will implement")

| id | source or check | how | phase | deadline | status |
|---|---|---|---|---|---|
| SY-1 | Signal cross-section theory: scales, PDF; infracolour Coulomb correction | 7-point envelope and PDF uncertainty on σ_NLO(m); band on the theory line; S2-f | 2 | 4a | open |
| SY-2 | Signal acceptance and ISR (one nuisance): f₂₀₀ and A; migration across the generator cut | S2-c; S1-f | 2 | 4a | open |
| SY-3 | Category migration (timing resolution and its tails) | variation within the public value (R-7) | 4a | 4a | open |
| SY-4 | Irreducible SM background: generator comparison and K | B4-d | 2 / 3 | 4a | open |
| SY-5 | Background normalisation of single-interaction terms: Geant4 against v1 rates; physics list (measured difference); material and composition only with a sourced size | B1-c; QGSP_BERT and composition variations (composition as a robustness test unless R-17 gives a range; its μ₉₅ shift is then reported beside the limit, Df-7) | 3 / 4a | 4a | open |
| SY-6 | Extrapolation along the cuts (in place of "background shape") | closure nuisances with the extrapolation width that is always added: B1-b, B2-f, B3-d | 4a | 4a | open |
| SY-7 | Soft-QCD modelling of pile-up: tune; hadron species, string against cluster hadronisation at generator level after an install attempt (DP5) | B6 tune variation; Herwig or, after a documented failure, published data (R-19) | 2 / 3 / 4a | 4a | open |
| SY-8 | Monte Carlo statistics | T1-a auxiliary channels with the convention of T1-c; bootstrap | 4a | 4a | open |
| SY-9 | Detector model: resolution, inefficiency, material (sourced sizes), top-up density, evaluated on every term | B6-c, B6-d | 4a | 4b | open |
| SY-10 | Object calibration: MET model (signal and background), trigger, vertex identification, timing, tracker hit-time window | B4-b, S1-f, S2-e, R-8, R-7, R-14 | 3 / 4a | 4a | open |
| SY-11 | Luminosity (projection at 3 ab⁻¹; also 300 fb⁻¹) | public target (R-9) | 4a | 4a | open |
| SY-12 | Pile-up at fixed ⟨μ⟩ = 200: density and timing spread; no μ scan (user decision) | B6 | 4a | 4a | open |
| SY-13 | Study-specific: QED FSR shift, dropped status-4 string events, frozen admissibility transcription, seed-threshold convergence, signal MC statistics, lepton-veto assumption | quoted or as nuisances in T1 | 4a | 4a | open |
| SY-14 | Heavy-flavour decay vertices: by the one-route rule they are Pythia decays inside the real SM events of B4; check that they are present | Phase-2 check on the tt̄ sample | 2 | 3 | open |
| VC-1 | Closure tests (conventions check 1) | all closure criteria above with the definitions of STR §4.0; alarm bands χ²/ndf < 0.1 or > 3 | 4a | 4a | open |
| VC-2 | Signal injection (check 2), pulls and constraints (3), impact ranking (4) | T1-d, T1-e, T1-f | 4a | 4a | open |
| VC-3 | Goodness of fit (5) and look-elsewhere (6): not applicable to data; closure p-values reported; Bonferroni in C1 and C2-c; family-wise rules for the closure battery (K = 10), the ceiling family (19 terms) and the T1 coverage family (10 checks), with their sizes at the declared widths | STR §5.2, §4.0, §4.11 | 4a | 4a | open |
| NA-1 | Declared not applicable (STR §5.1): beam energy; background shape as written; data/MC detector comparison as written; dE/dx calibration; b-tagging heavy-flavour treatment | justification in STR §5.1 | — | 4a (re-check) | n/a |

## Amendments E1–E3 to three Gate-A criteria (user, 2026-11-17: "Use your recomended answers for the 2 open questions")

The frozen verdicts stay on record as FAIL; the amended criteria below are amendments made AFTER the results were
known and are labelled as such wherever they are quoted (notice `notices/2026-11-17_0937_DECISION_…`).
| row | frozen verdict (VERIFIED) | amended criterion (in force from 2026-11-17) | status under the amendment |
|---|---|---|---|
| C1-b | central values PASS (2.2×10⁻¹⁶); B₈₄ within 1 %: FAIL on 29 of 86 (worst 3.4 %) | B₈₄ "within 1 %, or within 3 times v1's own Monte Carlo standard deviation" | PASS as measured (largest difference 1.76σ) |
| C2-a (V4-5) | independent fit 50/50 and 50/50: PASS; brute-force optimum 0/50 and 6/50: FAIL | (i) as frozen, F0 against the independent fit; (ii) the same exhaustive 0.2 mrad scan restricted to F0's inlier hits and the hits within 3σ of the F0 plane, \|Δn\| < 1 mrad in ≥ 48 of 50 per half; the unrestricted and global scans reported without a criterion. **If (ii) also fails: (i) alone is the accuracy test and the scan is reported as failed** | (i) PASS; (ii) NOT YET RUN (about 1.5 CPU-h; channel (i) successor) |
| T1-b | 902 ± 32 against 789.7 ± 10 %: FAIL | (a) asymptotic limits agree within 1 %; (b) v1's statistic on the builder's inputs reproduces v1's number with v1's seed, seed scatter reported; (c) the T1 toy limit reported with its replica scatter, no tolerance | PASS as measured ((a) 2×10⁻⁴; (b) identical, sd 38) |
Also from T1-b, for the pre-registration: the toy recipe of STR §4.11 gets a bracket refinement (bisection to 2 %)
and a stated empty-tail rule before it is used for v2 limits.
**C2-a (ii) result (2026-11-18, Ignatius):** the restricted scan FAILED (46/50 PU, 46/50 signal), so, as amended,
(i) alone is the accuracy test (PASS 50/50, 50/50) and the scan is reported as failed (`phase2_exploration/outputs/V45_RESTRICTED_ignatius_2026-11-18.md`).

## Amendment E4 to the C1 SM family (user, 2026-11-18 12:44: "Use your recommended answers for E4")

Notice `notices/2026-11-18_1229_DECISION_c1-sm-family-check-fails-only-through-its-error-.md`; regression ticket
`phase2_exploration/REGRESSION_TICKET_SM.md`; advisor ruling Kestrel (LOG 18 Nov). Made AFTER the result for the SM
family and labelled as such wherever quoted; BEFORE the result for the C′_PU family (rule committed in 54610b6).
| row | frozen verdict (VERIFIED) | amended criterion (in force from 2026-11-18) | status under the amendment |
|---|---|---|---|
| C1 SM family (v) (STR §4.1 item 5) | frozen script (1/√N width): R04 z +3.64 FAIL; coherence z +4.60 | Q1: event-level (clustered) bootstrap width for every quantity counted per candidate (SM, C′_PU); family coherence and χ² from joint replicas. Q2: v1's relative width = v2's event-level one (ESTIMATE; v1 per-event counts lost), with the v1-width-0 values and the 2σ power always quoted alongside | PASS 3/3, coherent: z +0.35/+0.57/+0.50 (v1 width 0: +0.50/+0.82/+0.75); 2σ power 16/17/94 % (`outputs/SM_FIX_lisbet_2026-11-18.md`, code 54610b6) |
Q3: no second-seed rerun of c1-sm. Q4: counted as remediation attempt 1 of 3; the event-level error model goes into
PREREG_v2. The N < 10 conditional-binomial branch of STR §4.1 item 1 is unchanged (frozen; its clustering is flagged).

**30-minute job rule:** exception granted by the user for FxFx only: two single-core jobs of about 1.5 h (one per
mass, 500 and 1,500 GeV); later event batches from saved grids stay ≤ 30 min.

## Addendum 1: APPROVED BY THE USER on 2026-11-17 (decisions D1–D9 as recommended; IN FORCE)

User's message: "I accept all D1-D9 answers with your recomendations." Decisions as recommended in
`phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` §0.3 (sha256 dd45b3ea…da98deb):
D1 chain kept, limitation [L15], with the 25th C3 item and looper overlays from Geant4 crossings; D2 robustness test
accepted, a measured increase enters the binding day-15 reading; D3 B1 pilot sizes as proposed; D4 seven B1 terms;
D5 hard-scatter sample H1 as one term; D6 the three populations stated as untested, alarm sample only; D7 pool
confirmed at 457 + 208 CPU-h (floor 201 as timed / 121 with both measures); D8 an R08 candidate pauses on 1–3 counts,
Z(νν) top-up decided at day 7; D9 hand-over rule per stream, with the slow-fragment residue handled by keeping the
β cut at 0.1 and flagging the affected events (notice of 16 Nov 20:28). D10 for information. The rows below are in
force from this date; the phrase "pending review and user approval" in them is superseded by this paragraph.

## Changes of rows by addendum 1 (approved 2026-11-17)

Version 5: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` (version 4 drafted 2026-11-16 by Zoe,
fix report `FIX_REPORT_addendum1_v4_zoe.md`; the exact texts of the third review applied by Clara, `FIX_REPORT_addendum1_v5_clara.md`;
the label "ADD4" in the rows below means this addendum in its current version); replaces the version-3 text of this section. **Nothing in this
section is in force until the addendum has passed review and the user has approved it; no row above is altered and no
status changes.** Numbers: [V] campaigns named in ADD4; [E] script `phase2_exploration/src/p2z_addendum1.py`, output
`phase1_strategy/outputs/addendum1_v4_stdout.txt`. Row lines are those of this file. The draft is the seven-term
reading with the hard-scatter parents on their own sample (ADD4 decisions D4 (a), D5 H1); the alternatives are in ADD4
§0.3 and change the numbers below as tabulated there. Already decided by the user and not part of this proposal: the
Z(νν) pilot and `pilot.mb` run since 2026-11-16 16:39 on the chain as it is ("option B: measure first", `LOG.md` 16:36).

| identifier (line) | what the addendum proposes |
|---|---|
| header note (l.18-27) | K = 10 (l.23) becomes **K = 13**: B1-a for seven B1 terms, B4-c for four processes, B2-a, B2-b; the INVESTIGATE and re-test level 0.05/K is 0.0038. "The 19 terms with a ceiling … 0.05/19" (l.24-25) becomes **22 terms, 0.05/22 = 0.00227**. For an analysis that performs as declared a false FAIL of either family removes a selection with 7.0–9.9 % (6.9–8.9 % before) |
| **new limitation [L15]** (STR §7, l.2285-2299; no row of this file) | **No hit beyond half a turn.** The fast simulation records no hit beyond half a turn of any particle (compiled in; present and unnoticed in v1; kept in v2 by the user's option B). Against Geant4, crossings without a simulated hit are at least 25 % of the written hits in a Z(νν) event and 37 % in a minimum-bias interaction, 34–58 % in the TBPS layers [V: p2-c-px-htg; lower bounds]. Behind keeping the chain: 0 candidates in 10⁵ + 10⁵ single loopers with full Geant4 trajectories [V: p2-c-px-lpd, all 2×10⁵ events]. The zero allows 2.2×10⁴ events at 68 % and does not cover loopers outside ± 0.1 of the road axis, \|η\| > 1, displaced loopers, or a looper together with other particles (pile-up). To appear in the limitations of the paper and the note, in the description of the simulation, and at abstract level if a later test shows an effect. Text: ADD4 §1.4 |
| C1-a (l.168) | unchanged: v1 ran with the same limit; C1 reproduces v1 with v1's setting whatever is decided for v2 |
| C3 (l.176) | proposed with ADD4 D1 (a): a 25th item, "v1's looper bound measured nothing" |
| B1-a (l.177) | B1 terms become seven classes that partition every Geant4 decay and inelastic vertex of the pool parents (π±, K±, p, K⁰_L, n, γ within 1 mm of the interaction point, 0.5 < p_T < 20 GeV, \|η\| < 1): DIF (first-arc decays at any radius and K⁰_L decays; N_t 1.06×10⁸), DIF-C (decays after the first turn; 9.75×10⁷), NI 22 / 30 / 61.5 mm (first arc, no factor 0.22; 4.90 / 6.64 / 6.63×10⁶), NI-X (first arc, other layers; 9.49×10⁷), NI-C (after a turn; 4.97×10⁷); sum 3.66×10⁸ against 6.8×10⁷. Each term keeps a hard-scatter share and a ×200 minimum-bias share. Closure designs for DIF-C, NI-X, NI-C are named (1,000 unbiased test overlays each, paired pile-up-only pass, derivation overlays; ≈ + 41 CPU-h in 4a) and are written in the pre-registration; no v1 count exists for them, so NOT TESTED is possible and adds three rows to the Q3 annex. **Hand-over rule per stream** (replaces "v1's `Truncate`" and the choice between two variants, STR l.744-746): products at the exit of their vertex slab, products with β < 0.1 not handed over, Geant4 parent crossings stored; parent of **DIF, NI 22 / 30 / 61.5 mm, NI-X: Fatras, v1's radius cut** (0.00–0.11 % of the Geant4 pre-vertex crossings without a hit; the time cut is no better and fails for NI-X) [V: p2-c-px-tr]; parent of **DIF-C, NI-C and of such events in `pilot.c0.hs` and `pilot.c0.lowpt`: Fatras to half a turn plus the stored Geant4 crossings beyond it, injected as hits ("option (a)")** (0.04 % / 0.05 % without a hit, 1.5 % duplicate hits at the seam, V4-1 passes, reruns identical; 58.5 % / 66.5 % with the radius cut and 40.4 % / 45.2 % with a time cut) [V: p2-c-px-hy]. Criterion: Geant4 pre-vertex crossings of a counting surface without a parent hit ≤ 2 %, **counted with multiplicity** (the once-per-surface measure understated the fault and would have passed the time cut). The products of every vertex still stop at half a turn ([L15]). Release condition: one job of every stream through the validation, whose radius check must first be made class-aware (it reads false for parents that have turned); the streams with nuclear interactions only after the slow-fragment residue of ADD4 §3 P6 (vi) is settled (a change of the β cut 0.1 goes to the user) |
| B1-b (l.178) | unchanged; the table of extrapolation widths gets three more terms |
| B1-c (l.179) | rates per class from Geant4 on the Pythia pool; the comparison with v1 is made on first-arc π/K decays at 30–1000 mm (N_t 8.15×10⁷ against 6.51×10⁷, ×1.25) and on the three radii before the factor 0.22; the hard-scatter share is 0–3 % by v1's rates and 1.3 % by a first direct parent count |
| B1-d (l.180) | Phase-2 part done: positions and x/X₀ agree (p2-c-matscan); the running Fatras instance neither decays nor absorbs hadrons (p2-c-part-fatras). Added fact: it also records no hit beyond half a turn ([L15]) |
| B1-e (l.181) | "soft bulk excluded by an analytic sagitta bound": **no bound is claimed any more** until it is written and checked. Decays after the first turn are a term (DIF-C). Parents below 0.5 GeV (N_t 2.6–5.2×10⁸ at an unmeasured yield) and at 1 < \|η\| < 1.5 (≈ 1.9×10⁸) are untested populations: an alarm sample `pilot.c0.lowpt` for the first (one count = 1,300–2,600 events; its zero bounds nothing), no sample for the second |
| B1-f (l.182, Df-9) | "a family of 19 terms, FAIL at p_t < 0.05/19, INVESTIGATE up to 5 × 0.05/19" becomes **22 terms, 0.05/22**; seven B1 terms each with its ceiling and completeness test; the own-hit count of a B1 sample is the number of (event, road orientation) passes over 21 fixed orientations. "Sub-topologies (γ, V⁰, prompt pairs, loopers)": a looper population made with Fatras holds no repeated crossings; if kept as a diagnostic it is made from Geant4 crossings injected as hits (the gun of p2-c-px-lp) |
| B1-g (l.183) | unchanged (Phase 3); its resolving power is 4.1×10⁴ events per count: an alarm at loose rungs, not a bound; its Geant4 secondaries stop at half a turn once handed to Fatras |
| B2-a, B2-b, B2-c (l.184-186) | unchanged; noted: both estimators, the occupancy model's correlation factors and the direct counts are made on the same chain, so their closure cannot see [L15] (ADD4 §1.1 point 2) |
| B4-c (l.197, Q3) | "3.65×10⁷ events over fourteen processes": the no-pile-up pool is counted in effective preselected events (full-weight class, Σw/w_max; the 0.05-weight class of each process is a second counted factor). Table 4.4a at the approved 457 + 208 CPU-h: SM zero-count allowance 8.6 → 169 as timed, 93 with forced top decays (327 ms, measured for tt̄ 1ℓ only) and the preselection before the chain; low-weight classes + 5 to + 9; B1 3.9 → 23 (seven classes, one shared Geant4 pass); all pool terms 12.6 → **201 as timed, 121 with both measures** (about 204 as timed with the unit costs measured after version 3; not adopted, the table is re-derived at day 12). The user's decision of 2026-11-16 to keep the allocation was taken on 36–42 and is put for confirmation. "Loopers" inside the hard-scatter terms: first half turn only ([L15]) |
| **B6-a (l.203), B6-c (l.205): proposed, pending the user (ADD4 D2); not a commitment unless accepted** | an **eighth robustness row "later arcs restored"**: 600 ρ = 1 pile-up events in which the Geant4 crossings beyond half a turn of every charged particle are injected as hits (total density per layer kept at the top-up normalisation), against the same events and seeds on the present chain; read at R04–R06 with the B6-a criterion (error on ln(B_var/B_nom) < 0.1 at R06) and the pre-declared reading of ADD4 §1.5 (no effect → [L15] stated with a measured size; effect within ln 2 → if r(R06) > 1 the pile-up estimate is multiplied by r(R06) with the widths of ADD4 §1.5, no credit for r < 1 (a one-sided correction, not a symmetric nuisance; third review B-2); "not robust" → limitation at abstract level and the user chooses between the correction and a chain fix); 22–28 CPU-h [E]; before the freeze. If declined: nothing changes in B6 and [L15] rests on the single-looper zero |
| B6-d (l.206, Df-7) | only if D2 is accepted and the row shows an increase: it enters as a correction of the pile-up estimate with its measured error, a source-defined variation (STR l.1477-1478), by the reading of ADD4 §1.5 |
| T1-a (l.208) | three more B1 auxiliary channels per candidate, and one per low-weight class |
| T1-i (l.216, Df-8) | not changed. Toy cost measured: ×17 at 60 parameters with the numpy backend; with pyhf's jax backend, autodiff gradients, merged auxiliary channels, the POI removed from the fit and warm starts 30.5 / 168 / 385 / 817 s per 1000 + 1000 toys at 31 / 60 / 80 / 100 parameters, same CLs at the test point, 0 failed fits in 25,180 toys [V: p2-c-toy-*; synthetic workspace]. Toy programme 47 / 108 / 228 CPU-h against 183 (factor ≈ 1.6 either way); projection 4,663 / 4,723 / 4,844 CPU-h, below 5,992 (old backend: 7,705 / 9,591 / 18,199, above). To be re-measured on the first real v2 workspace before Phase 4b; ties of the test statistic compared within 10⁻⁵ |
| T2-a (l.217, Q3) | "a ceiling FAIL in the family of 19" becomes **the family of 22**; the list of 16 candidates and the rule are unchanged |
| PR-1 (l.249) | contents of STR §8: "K = 10" becomes **K = 13** and "its family of 19" **22**; the pre-registration also carries the seven-term list with N_t, the three new closure designs, the road-orientation rule, the hand-over rule per stream and limitation [L15] |
| ST-1 (l.257, Q4, Df-11) | rule 1 unchanged in definition (samples that exist, max(floor, N_t·H), Gamma(m + 1), no pool floor, ties pause, ≥ 10⁵ draws; the pile-up term is the present chain's estimate, or, if the user so chooses with ADD4 D2, that estimate corrected by B6-d). It reads the seven B1 classes on their own pilot samples (4, 4, 1, 1, 1, 4, 2 ×10⁶ events; 23–26 events per count for the large classes, 4.8–6.5 for the three radii), the hard-scatter share on `pilot.c0.hs` (2×10⁶ vertices, 4.0 per count, one term) and the SM processes at 41 events per full-weight Z(νν) pilot count (2.3×10⁶ generated; provisional until the day-12 MET model). Empty-pilot B₅₀: **161 at R09, 238 / 262 / 284 at R08** (389 and 467–515 with 10⁶ events per sample; 76 frozen); pause at 4 Z(νν) counts or 6 counts in a large B1 sample at R09, at 1–3 counts at R08; with a pile-up estimate 25 % (50 %) higher an empty pilot reads 308 at the upper (303 at the central) R08 estimate. Approved 4,609 CPU-h and threshold 5,992 unchanged; pilot generation **142 CPU-h** against 54.5 (reported overrun): part 1 (launched) 95.3, B1 part 47.0, to follow the Z(νν) pilot from about 18 Nov 16:15 and end about 19 Nov 15:45 on two lanes (day 5 = 2026-11-21) |
| INV-1 (l.258) | sample 11 (STR l.2104): streams `pilot.c0.{dif,difc,ni22,ni30,ni61,nix,nic,hs,lowpt}`, `pilot.mb`, `pilot.g4`, `pilot.hs0.znn`; 1.7×10⁷ B1 events, 2×10⁶ hard-scatter-parent and 2×10⁵ low-p_T events, 2.3×10⁶ generated Z(νν) events with stored preselection inputs (jets to 10 GeV, sums, leptons, neutrinos) and hadron list, no full particle list; ≈ **167 GB** (Z(νν) 78, minimum bias 2, B1 events 71, Geant4 vertex files 16). `pilot.c0.hs` takes its parents from the finished Z(νν) files. Sample 17 (l.2111): the pool has seven streams `prod.c0.<class>` from one shared Geant4 pass, the hard-scatter parents mixed in at their natural proportion, the hand-over per stream as in B1-a. Samples 18, 18a, 18b (l.2112-2114): sizes in effective events by Table 4.4a of ADD4. Sample 19 (l.2115): overlays for DIF-C, NI-X, NI-C added (3 × 1,000 unbiased test overlays and their derivation overlays); the looper overlays as in B1-f above |
| VC-3 (l.283) | "closure battery (K = 10), the ceiling family (19 terms)" becomes **K = 13, 22 terms** |

## User decisions on the two pre-freeze choices (user, 2026-11-19 11:17 -0500; notice 2026-11-19_1115)
| item | decision |
|---|---|
| S2-e trigger turn-on uncertainty | option (b): threshold kept at MET > 250 GeV; wide nuisance of −10.6 % absolute efficiency at 250 GeV (Table-4.1 erf, width 56 GeV; −4.9 % at 275, −1.9 % at 300). Recorded as a clarification of the frozen S2-e branches (sourced curve, not-sourced size; STR l.2029-2033) BEFORE any efficiency A is computed |
| P1 thickness-law diagnostic | record the rn47 diagnostic beside the pre-declared "not the floor pattern" verdict (which stays), labelled "diagnostic, not a pre-declared test"; caveats: floor test 1 not done (P1-a incomplete), 40 events per point, medians 1.3–1.4×, P1-c FAIL |
