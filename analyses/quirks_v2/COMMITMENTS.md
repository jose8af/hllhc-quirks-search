# Binding commitments

Filled by the Phase-1 strategy (`phase1_strategy/outputs/STRATEGY_brigitte_2026-11-13_17-55.md`, "STR" below) and frozen
at Gate A. Every MUST and SHOULD item of the publication plan is a "will implement", except S3 (endcap), dropped by
the user (brief D1) and carried as an EST outlook statement.
A status changes only through a logged `[D]` entry (JFC 12) or a user decision; never silently.

Columns: "phase" is where the work is done; "deadline" is the last phase at whose review the commitment must be
closed (fulfilled, or reported as failed as pre-declared). "Within a factor F" is defined in STR §4.0: |ln r| ≤ ln F at
every rung with ≥ 20 direct counts, χ² p > 0.05 with the declared systematic, and that systematic ≤ ln F.
Rows marked (DP) carry a downscope proposal that the user decides at Gate A; until then the full form is the commitment.

## Items of the publication plan

| id | priority | commitment | acceptance criterion (short; full text in STR) | phase | deadline | status |
|---|---|---|---|---|---|---|
| C1-a | MUST | Rerun the v1 code with logged port edits and the frozen configuration (T_seed 4, road 0.15) on the declared subset: pile-up ρ = 1 (4,000 events) and ρ = 2 (1,000), no-PU and C′_PU samples, Z(νν), rates, three signal points (E 200 at 1.5 and 2 keV, E 500 at 3 keV; 400 rows each) | 41 declared comparisons with `C12FC_v1`: each p > 0.05/41, global χ² below its 99th percentile, family coherence \|z\| < 3; power stated; fail → investigated, not tuned (STR §4.1) | 2 | 2 | open |
| C1-b | MUST | v2 analysis arithmetic applied to the v1 recorded counts | central values to 10⁻⁶, B₈₄ within 1 % (STR §4.1) | 2 | 2 | open |
| C1-c | MUST | Linux environment: tracked lockfiles, container recipe, jobs ≤ 30 min through the resumable runner | one C1 job rerun in the container with identical output hash (STR §4.1) | 2 | 5 | open |
| C1-d | MUST | Blinding rule for the C1 signal counts: only the ten declared v1-rule counts are computed; C1 rows are never part of S1 | declared exception written into `PREREG_v2.md`; no other signal quantity in any Phase 2–4a artifact (STR §4.1) | 2 | 4b | open |
| C2-a | MUST | V4-5 brute-force cross-check on 50 signal + PU events and 50 PU trials (new code) | \|Δn\| < 1 mrad against the brute-force optimum and against the independent fit in ≥ 48/50 and ≥ 48/50; disagreements inspected (STR §4.2) | 2 | 2 | open |
| C2-b | MUST | V4-4 as defined in v1: reproducibility and seeds, 20 jobs | bit-identical reruns on the same node; different seeds differ; seeds recorded (STR §4.2) | 2 | 2 | open |
| C2-c | MUST | Seed-threshold stability T_seed 4 → 2 (the test the plan mislabels V4-4) | \|z\| < 2 for the pass fraction of every rung family at ρ = 1 and 2; fail → reported, T_seed not retuned (STR §4.2) | 2 | 2 | open |
| C3 | MUST | Paper corrections: all 24 items of D3 §1, the 19 label families of D2 §5, novelty wording, `ERRATA_v1.md`, disclosure of the AI workflow and CMS membership, number tags | checklist with file:line per item; zero grep hits for internal labels; two primary-source checks logged (STR §4.3) | 5 | 5 | open |
| B1-a | MUST | Geant4 (FTFP_BERT) vertices handed to Fatras; factorised estimator P_geo × C_PU; biased generation with weights | closure against direct full pile-up samples within a factor 2 at R05–R07 per topology; biased against unbiased closure at R05 (STR §4.4) | 3 / 4a | 4a | open |
| B1-b | MUST | Trend of the closure ratio along the rungs | slope compatible with zero at 2σ, or its extrapolation added to the width in full (STR §4.4) | 4a | 4a | open |
| B1-c | MUST | Geant4 rates cross-checked against the v1 generator rates | within a factor 2 per topology; outside → reported as failed cross-check, Geant4 rate kept (STR §4.4) | 3 | 4a | open |
| B1-d | MUST | Geant4 geometry identical to ACTS; active Fatras physics list recorded | \|Δ(x/X₀)\| ≤ 1 % per layer, positions to 1 µm; no double counting of hadronic interactions (STR §4.4) | 3 | 3 | open |
| B2-a | MUST | Repaired thinning: pre-merge candidates stored at ρ = 2 (N_IP2 ≥ 6), grouping re-applied per thinned subset | reproduces direct counts within a factor 1.5 at R04–R07; no scale-factor patch (STR §4.5) | 2 / 3 / 4a | 4a | open |
| B2-b | MUST | Independent semi-analytic occupancy estimator (new code) | same criterion as B2-a (STR §4.5) | 3 / 4a | 4a | open |
| B2-c | MUST | Agreement of the two estimators at the deeper rungs; trend test | \|ln(B_thin/B_occ)\| ≤ 2 × combined declared width, and that width ≤ 1.0, up to the chosen selection (STR §4.5) | 4a | 4a | open |
| B2-d | MUST | Direct ρ = 1 sample of 24,000 events (96,000 trials), independent of development samples | ≈ 70 expected counts at R07 (σ_ln ≈ 0.12) | 4a | 4a | open |
| B2-e | MUST | ρ = 2 memory and pre-merge storage measured before any campaign | RSS against events per job recorded; job packing and storage threshold set from it; cap 400 GB (STR §4.5) | 2 | 2 | open |
| B3-a | MUST | Conditionals for the shape rungs (h, o) per topology on the no-PU samples | each closes within a factor 1.5 against the direct full-PU conditional where ≥ 30 counts; failed → no credit (STR §4.6) | 3 / 4a | 4a | open |
| B3-b | MUST | Displaced-vertex veto, designed on background samples only | same criterion; selections with and without it both in T2 (STR §4.6) | 3 / 4a | 4a | open |
| B3-c | MUST | Time-tag (late-hit) conditional for prompt terms | same criterion (STR §4.6) | 3 / 4a | 4a | open |
| B4-a | MUST | Hit-level samples for the eight proxied processes | proxy fraction of B_SM = 0 at every rung (STR §4.7) | 3 / 4a | 4a | open |
| B4-b | MUST | Z(ττ), lost-lepton Z(ℓℓ), multijets with a reconstruction-level MET model built from cited public parametrisations | Z(νν) yield within 10 % of the v1 selection; multijet yield stable within a factor 2 under bias changes; comparison with a published multijet fraction; tail variation as nuisance (STR §4.7) | 3 / 4a | 4a | open |
| B4-c | MUST | Hard-scatter tracks with the factorised estimator | closure within a factor 2 at R05–R06 per process with ≥ 20 counts (STR §4.7) | 4a | 4a | open |
| B4-d | MUST | Cited K-factors; generator comparison for Z(νν)+jet and W+jet rates | every K has a citation; generator difference is the normalisation nuisance (STR §4.7) | 2 / 3 | 4a | open |
| B5 (DP1) | SHOULD | Road-rotation sideband closed in simulation: flatness in the angle to the MET and independence of roads | sideband prediction within a factor 1.5 at R04–R06 (R07 if ≥ 20 counts); non-flat part quantified per process; road correlation \|ρ\| < 0.1 or an effective-trials factor (STR §4.8). Full: 20 roads on 8,000 SM events; proposed reduced: 8 roads on 6,000 | 3 / 4a | 4a | open |
| B6 (DP2) | SHOULD | Seven detector-model variations (resolution ×1.5, inefficiency 97 % incl. pile-up hits, material ×0.5 and ×2, top-up low and high, alternative tune) propagated to background and signal | every variation evaluated with stated precision; classified robust / not robust by the pre-declared thresholds; measured shifts enter the likelihood uncapped (STR §4.9). Full: 6 signal points; proposed reduced: 4 | 3 / 4a | 4b | open |
| B7 | SHOULD | Cosmic and beam-halo background as a number from public rates, pointing and timing | number with derivation; below 10 % of the smallest term → stated, else a term of the likelihood (STR §4.10) | 3 | 4a | open |
| T1-a | MUST | pyhf workspace: Poisson auxiliary channel per simulated count (zero counts included), correlated nuisances, one route per term, closure-derived systematics; published | schema-valid; reproduces the v1 best-point toy limit within 10 % in v1 mode (STR §4.11) | 3 | 4a | open |
| T1-b | MUST | Validation checks of `conventions/search.md` | signal injection at 0/1/2/5×: bias ≤ 20 %; Asimov pulls and constraints; impact ranking; toy self-consistency 50 ± 4.5 % (STR §4.11, §5.2) | 4a | 4a | open |
| T1-c | MUST | Toys primary for every quoted limit; asymptotic tabulated beside them | 1000 toys per μ point at every grid point for the chosen selection, the runner-up and the v1 fallback (STR §4.11) | 4b / 4c | 4c | open |
| T2-a | MUST | Selection rule: 16 declared candidates, eligibility by closure verdicts, figure of merit G on the optimisation half, split by a salted hash | rule, list, G and salt in the hashed pre-registration before S1 production; choice reproducible; optimisation-to-evaluation shift reported (STR §4.12) | 3 / 4b | 4b | open |
| T2-b | MUST | "Background-free" (B₈₄ ≤ 0.11 per category) reported as a flag only | flag in the results table (STR §4.12) | 4b | 4c | open |
| S1-a | MUST | 2,000 rows at each of the 40 points through the full chain; no fast path | ≥ 99 % of jobs complete with ingestion closure; no fast-path number in any result (STR §4.13) | 2 (string) / 4a (chain) | 4a | open |
| S1-b | MUST | Efficiencies blind until the closure verdicts; evaluation half aggregated only after Gate B | first aggregation logged at 4b (optimisation) and 4c (evaluation) (STR §4.13) | 4b / 4c | 4c | open |
| S2-a | MUST | NLO K-factors computed with `loop_quirkE`, used only after three validations (model identity, slepton matching limit, Drell–Yan independence) | \|z\| < 3 and 0.5 %; within 10 % of the published slepton tables; within 5 % of the Drell–Yan K; fail → v1 transcription labelled as such and the criterion reported failed (STR §4.14) | 2 | 2 | open |
| S2-b | MUST | f₂₀₀ recomputed with one definition (no η cut) and its uncertainty rebuilt and propagated into the limits | one script, one definition in text; scale, PDF, merging-scale, tune and FxFx comparisons; nuisance in T1 (STR §4.14) | 2 | 4a | open |
| S2-c | MUST | QED-FSR shower is the nominal signal; FSR-off kept for C1 and for the quoted shift | nominal samples showered with the QED-FSR card (STR §4.14) | 2 | 2 | open |
| S2-d | MUST | Trigger turn-on from a public Phase-2 curve, with a nuisance | cited figure and page; else reported "parametrised, not sourced" with the pre-declared wide nuisance (STR §4.14) | 2 | 4a | open |
| P1-a | MUST | Floor tests: extended-precision step map and mantissa-truncation kernel (both new code) | executed and read against the pre-declared table (floor / physical / inconclusive) (STR §4.15) | 2 | 2 | open |
| P1-b | MUST | B*-off as a paired test with power (≈ 970 events at 5 keV) and at 1 keV | pre-declared reading at 3σ (5 keV) and 2σ (1 keV) (STR §4.15) | 2 | 2 | open |
| P1-c | MUST | Population estimator for c defined in advance (paired median) and evaluated on new events; original gate reported as failed | \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at five points on 300 new events each (STR §4.15) | 2 | 2 | open |
| P1-d | MUST | Validity window stated as measured; failed straight-string ratio kept visible; Linux difference of one Stage-1 run followed up | table per (point, Λ, k_B bin) from the tracked results; text follows it (STR §4.15) | 2 | 5 | open |
| S3 | SHOULD | **dropped by user decision (brief D1)**; barrel-only paper; endcap gain stated as an EST outlook exactly as fixed in the brief | n/a | 5 (text) | 5 | dropped (user) |
| S4 | COULD | optional; strategy recommends not including it (DP4): ≥ 1 week and ≥ 600 CPU-h, delays the freeze | — | — | — | undecided, pending Gate A |
| S5 | COULD | optional; strategy recommends not including it (DP4): negative result stated instead | — | — | — | undecided, pending Gate A |

## Commitments from the strategy that are not plan items

| id | commitment | acceptance criterion (short) | phase | deadline | status |
|---|---|---|---|---|---|
| PR-1 | `PREREG_v2.md` hashed and committed before any v2 production sample; contents of STR §8; analysis code frozen before production | 4-bot review PASS; sha256 in git before the first production marker; user notified | 3 | 3 | open |
| PR-2 | v1 kept by hash in an appendix, with the lost files listed and the freeze timing of the v1 analysis code stated | appendix text matches STR §8 | 5 | 5 | open |
| MVA-1 (DP3) | BDT cross-check with a pre-registered recipe, at a directly counted background rate | ε_BDT/ε_R07 at equal counted pile-up rate reported, with one alternative architecture (STR §3.2) | 4c | 4c | open |
| REF-1 | Reference analyses R1–R4 tabulated; comparison targets of STR §6.2 overlaid on the limit and reach figures; "3 and 5 events at B = 0" reach quoted with v2 efficiencies | present in the Phase-4a note (placeholders) and final in 4c | 4a / 4c | 4c | open |
| REF-2 | Retrieval tasks R-1 to R-11 (STR §6.4) from public sources, logged; nothing quoted from memory | each closed with a citation, or its dependent commitment reported as not sourced | 2 / 3 | 3 | open |
| FIG-1 | The seven flagship figures and seven diagrams of STR §9 | all present in the paper and the note | 4a–5 | 5 | open |
| RQ-1 | The 25 referee questions answered with a pointer to the text (STR §10) | adversarial review at Phase 5 | 5 | 5 | open |

## Systematic plan (STR §5; every "will implement")

| id | source or check | how | phase | deadline | status |
|---|---|---|---|---|---|
| SY-1 | Signal cross-section theory: scales, PDF | 7-point envelope and CT18NLO eigenvectors on σ_NLO(m); band on the theory line | 2 | 4a | open |
| SY-2 | Signal acceptance and ISR (one nuisance): f₂₀₀ and A | S2-b | 2 | 4a | open |
| SY-3 | Category migration (timing resolution) | variation within the public value (R-7) | 4a | 4a | open |
| SY-4 | Irreducible SM background: generator comparison and K | B4-d | 2 / 3 | 4a | open |
| SY-5 | Background normalisation of single-interaction terms: Geant4 against v1 rates, material band, composition, physics list | B1-c; QGSP_BERT and composition variations | 3 / 4a | 4a | open |
| SY-6 | Extrapolation along the cuts (in place of "background shape") | closure nuisances and trend tests of B1–B3 | 4a | 4a | open |
| SY-7 | Soft-QCD modelling of pile-up: tune; hadron species (Herwig at generator level if installable, DP5) | B6 tune variation; generator-level comparison | 3 / 4a | 4a | open |
| SY-8 | Monte Carlo statistics | T1-a auxiliary channels; bootstrap | 4a | 4a | open |
| SY-9 | Detector model: resolution, inefficiency, material, top-up density | B6 | 4a | 4b | open |
| SY-10 | Object calibration: MET model, trigger, vertex identification, timing | B4-b, S2-d, R-8, R-7 | 3 / 4a | 4a | open |
| SY-11 | Luminosity (projection at 3 ab⁻¹; also 300 fb⁻¹) | public target (R-9) | 4a | 4a | open |
| SY-12 | Pile-up at fixed ⟨μ⟩ = 200: density and timing spread; no μ scan (user decision) | B6 | 4a | 4a | open |
| SY-13 | Study-specific: QED FSR shift, dropped status-4 string events, frozen admissibility transcription, seed-threshold convergence, signal MC statistics | quoted or as nuisances in T1 | 4a | 4a | open |
| SY-14 | Heavy-flavour decay vertices: check whether they are a separate topology; add to B1 if so | Phase-2 inventory | 2 | 3 | open |
| VC-1 | Closure tests (conventions check 1) | all closure criteria above; alarm bands χ²/ndf < 0.1 or > 3 | 4a | 4a | open |
| VC-2 | Signal injection (check 2), pulls and constraints (3), impact ranking (4) | T1-b | 4a | 4a | open |
| VC-3 | Goodness of fit (5) and look-elsewhere (6): not applicable to data; closure p-values reported; Bonferroni in C1 | STR §5.2 | 4a | 4a | open |
| NA-1 | Declared not applicable (STR §5.1): beam energy; background shape as written; data/MC detector comparison as written; dE/dx calibration; b-tagging heavy-flavour treatment | justification in STR §5.1 | — | 4a (re-check) | n/a |
