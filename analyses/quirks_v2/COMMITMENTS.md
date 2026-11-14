# Binding commitments

Filled by the Phase-1 strategy and frozen at Gate A. Current strategy: `phase1_strategy/outputs/STRATEGY_dmitri_2026-11-13_19-25.md`
("STR" below; version 2, after review cycle 1). The first version of this file referred to
`STRATEGY_brigitte_2026-11-13_17-55.md`.
Every MUST and SHOULD item of the publication plan is a "will implement", except S3 (endcap), dropped by the user
(brief D1) and carried as an EST outlook statement.
A status changes only through a logged `[D]` entry (JFC 12) or a user decision; never silently.

**This file is the master list of criterion identifiers.** STR quotes these identifiers and no others.

Columns: "phase" is where the work is done; "deadline" is the last phase at whose review the commitment must be
closed (fulfilled, or reported as failed as pre-declared).
"Within a factor F" is defined in STR §4.0: derivation and test on disjoint rungs and samples; a test rung is
evaluable if σ_tot = √(1/N + s_P²) ≤ ln F/3 (N counted after the cut); (a) |ln r| ≤ ln F at every evaluable test rung;
(b) χ² with the full covariance and the common s_model, p > 0.05, with the family-wise rule (FAIL at p < 0.05/K,
one re-test on a fresh sample for 0.05/K ≤ p < 0.05); (c) s_model ≤ ln F, fixed before the freeze from development
samples. Verdicts: PASS, FAIL, NOT TESTED, NOT EVALUABLE. Every extrapolated factor carries the width s_tot(r) of
STR §4.0 point 7.
Rows marked (DP) carry a downscope proposal that the user decides at Gate A; until then the full form is the commitment.
Rows marked (GA-n) contain a default that the user decides at Gate A (STR §12.1); until then the default is a proposal.

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

## Items of the publication plan

| id | priority | commitment | acceptance criterion (short; full text in STR) | phase | deadline | status |
|---|---|---|---|---|---|---|
| C1-a | MUST | Rerun the v1 code with logged port edits and the frozen configuration (T_seed 4, road 0.15) on the declared subset: pile-up ρ = 1 (4,000 events) and ρ = 2 (1,000), no-PU and C′_PU samples, Z(νν), rates, three signal points (E 200 at 1.5 and 2 keV, E 500 at 3 keV; 400 rows each) | 41 declared comparisons with `C12FC_v1`: each p > 0.05/41, global χ² below its 99th percentile, family coherence \|z\| < 3; power stated; fail → investigated, not tuned (STR §4.1) | 2 | 2 | open |
| C1-b | MUST | v2 analysis arithmetic applied to the v1 recorded counts | central values to 10⁻⁶, B₈₄ within 1 % (STR §4.1) | 2 | 2 | open |
| C1-c | MUST | Linux environment: tracked lockfiles, container recipe, jobs ≤ 30 min through the resumable runner | one C1 job rerun in the container with identical output hash (STR §4.1) | 2 | 5 | open |
| C1-d (GA-1) | MUST | Blinding rule for the C1 signal counts. **Six** of the ten are efficiencies of v2 candidate selections (R07 × 3; fallback FB2/FB3 × 3 = T2 family F). Default: R04 and R06 counts open (4); R07 and fallback counts (6) compared by a dedicated agent that reports only PASS/FAIL, counts sealed until Gate B. C1 rows are never part of S1. R07 and family F stay in the T2 list as declared. The exception to the blinding invariant takes effect only with the user's approval | tier approved by the user recorded in `PREREG_v2.md`; sealed file with sha256 in the ledger, unread before the verdicts; no other signal quantity in any Phase 2–4a artifact except those of BL-1 (STR §4.1) | 2 | 4b | open |
| C1-e | MUST | Chain per C1 signal point as in v1 (fast path at E 200 with 1.5 and 2 keV, full chain at E 500 with 3 keV); full-chain twins of the two fast-path points | twin ratio full/fast reported against the declared expectation (×0.832 at R04, ×0.871 at the fallback); fallback ratio sealed with the tier of C1-d (STR §4.1) | 2 | 2 | open |
| C2-a | MUST | V4-5 brute-force cross-check on 50 signal + PU events and 50 PU trials (new code) | \|Δn\| < 1 mrad against the brute-force optimum and against the independent fit in ≥ 48/50 and ≥ 48/50; disagreements inspected; no pass fraction readable from the output; the "optimality" count is taken in Phase 4c only (STR §4.2) | 2 | 2 (optimality count: 4c) | open |
| C2-b | MUST | V4-4 as defined in v1: reproducibility and seeds, 20 jobs | bit-identical reruns on the same node; different seeds differ; seeds recorded (STR §4.2) | 2 | 2 | open |
| C2-c | MUST | Seed-threshold stability T_seed 4 → 2 (the test the plan mislabels V4-4) | \|z\| < 2 for the pass fraction of every rung family at ρ = 1 and 2; fail → reported, T_seed not retuned (STR §4.2) | 2 | 2 | open |
| C3 | MUST | Paper corrections: all 24 items of D3 §1, the 19 label families of D2 §5, novelty wording, `ERRATA_v1.md`, disclosure of the AI workflow and CMS membership, number tags | checklist with file:line per item; zero grep hits for internal labels; two primary-source checks logged (STR §4.3) | 5 | 5 | open |
| B1-a | MUST | Geant4 (FTFP_BERT) vertices handed to Fatras; estimator P_geo·S + Σ f_k·π_k (pass and near-pass probabilities without pile-up, survival, promotion) | held-out closure per topology within a factor 2: survival and promotion derived on derivation overlays at R04–R05, tested on test overlays with other seeds at R06–R07 (attributed counts); verdict classes of STR §4.0; expected: γ, V⁰ evaluable at R06, decays in flight with an enrichment ≥ 1.5–3, PV pairs only with an enrichment of 10²–10³, NI and loopers NOT TESTED (STR §4.4, Table 4.4b) | 3 / 4a | 4a | open |
| B1-b | MUST | Extrapolation of the pile-up factors beyond the test rungs | S = 1 beyond its tested rungs; promotion carries s_tot(r), always in the likelihood; b̂, σ_b and s_tot tabulated per T2 candidate (STR §4.0, §4.4, §4.12) | 4a | 4a | open |
| B1-c | MUST | Geant4 rates cross-checked against the v1 generator rates | agreement within the combined uncertainty of the physics-list difference (measured), the sourced material uncertainty (R-17) and statistics; outside → reported as failed cross-check, Geant4 rate kept (STR §4.4) | 3 | 4a | open |
| B1-d | MUST | Geant4 geometry identical to ACTS; active Fatras physics list recorded | \|Δ(x/X₀)\| ≤ 1 % per layer, positions to 1 µm; no double counting of hadronic interactions (STR §4.4) | 3 | 3 | open |
| B1-e | MUST | Biased generation of the stiff tail with weights; soft bulk excluded by an analytic sagitta bound; Phase-2 pilot measuring the gain | weights closure biased against unbiased at R05 within a factor 1.5; bound written with its scattering allowance and checked at R05–R06; gain per topology recorded before the freeze; fail → unbiased generation (STR §4.4) | 2 / 3 / 4a | 4a | open |
| B1-f | MUST | Attribution rule for candidates; promotion term; no-credit ceiling H = P_geo + Σ f_k measured directly at every T2 candidate | rule in `PREREG_v2.md` (v1's coded rule transcribed and compared); H tabulated; per-layer promotion probabilities tested against near-pass overlays at R06 where evaluable (STR §4.4) | 2 / 3 / 4a | 4a | open |
| B1-g | MUST | Sources not in v1's list: secondaries of pile-up vertices; noise and out-of-time hits; δ-rays and merged clusters | pile-up-vertex secondaries test on 1,000 events: \|ln ratio\| < 0.10 at R04–R06 → stated and left out, else included in every overlay (cost re-projected); noise and out-of-time occupancy from R-18 against the top-up; δ-rays under limitation L8 (STR §2) | 3 | 3 | open |
| B2-a | MUST | Repaired thinning: pre-merge candidates stored at ρ = 2 (N_IP2 ≥ 6), 64 thinned subsets per trial, grouping re-applied per subset | reproduces direct counts within a factor 1.5 at R04–R07; no scale-factor patch (STR §4.5) | 2 / 3 / 4a | 4a | open |
| B2-b | MUST | Independent semi-analytic occupancy estimator (new code); inputs derived on development samples at R04–R05 | reproduces direct counts within a factor 1.5 at the held-out R06–R07; its dependence on finder candidates for the fit-probability and shape rungs stated (STR §4.5) | 3 / 4a | 4a | open |
| B2-c | MUST | Agreement of the two estimators beyond R07 | within a factor 1.5 (STR §4.0 criterion with r = B_thin/B_occ) at every rung where thinning is evaluable; elsewhere NOT EVALUABLE, and the pile-up term is declared a one-estimator extrapolation (STR §4.5) | 4a | 4a | open |
| B2-d | MUST | Direct ρ = 1 sample of 24,000 events (96,000 trials), independent of development samples | ≈ 70 expected counts at R07 (σ_ln ≈ 0.12, evaluable for F = 1.5) | 4a | 4a | open |
| B2-e | MUST | ρ = 2 memory and pre-merge storage measured before any campaign | RSS against events per job recorded; job packing and storage threshold set from it; cap 400 GB (STR §4.5) | 2 | 2 | open |
| B2-f | MUST | Extrapolation width of both pile-up estimators | b̂, σ_b, s_tot(r) per estimator and T2 candidate; in the likelihood always (STR §4.0, §4.5) | 4a | 4a | open |
| B2-g | MUST | Thinning reach | N_eff per rung measured on the 1,000-event development sample; deepest evaluable rung written into `PREREG_v2.md` (STR §4.5) | 2 / 3 | 3 | open |
| B3-a | MUST | Conditionals for the shape rungs (h, o) per topology on the no-PU samples | each within a factor 1.5 in the stability test of B3-d, counts after the cut; failed or untested → no credit (STR §4.6) | 3 / 4a | 4a | open |
| B3-b | MUST | Displaced-vertex veto, designed on background samples only | same criterion; selections with and without it both in T2 (STR §4.6) | 3 / 4a | 4a | open |
| B3-c (GA-9) | MUST | Time-tag (late-hit) fraction for prompt terms, measured at hit level with a timing model that has sourced tails | closure on R04 candidates of the direct sample at five widened window edges within a factor 1.5; independence from the rung at R04–R06; credit never below the sourced tail fraction; tails not sourced → no credit (STR §4.6) | 2 / 3 / 4a | 4a | open |
| B3-d | MUST | Transfer of each conditional from the rung where it is measured to the rung where it is applied | measured after ≥ 3 preceding rungs; derivation on the first two, test on the deepest, on disjoint halves; width s_tot(r) from the distance (STR §4.6) | 3 / 4a | 4a | open |
| B4-a | MUST | Hit-level samples for the eight proxied processes | proxy fraction of B_SM = 0 at every rung (STR §4.7) | 3 / 4a | 4a | open |
| B4-b | MUST | Z(ττ), lost-lepton Z(ℓℓ), multijets with a reconstruction-level MET model built from cited public parametrisations (soft term from the public source only) | external validation against a published Phase-2 MET performance figure at pile-up 200 within the pre-declared tolerance; multijet yield stable within a factor 2 under bias changes; comparison with v1 and with a published multijet fraction reported without verdict; tail variation as nuisance; not validated → full variation as width, stated (STR §4.7) | 3 / 4a | 4a | open |
| B4-c | MUST | Hard-scatter tracks with the estimator of B1; no-PU samples from the common pool (1.74×10⁷ events by √N_trig) | closure within a factor 2: derivation half at R04–R05, test half at R06; expected: Z(νν) evaluable, the other processes NOT TESTED at 2,000 events and entering at H (STR §4.7) | 4a | 4a | open |
| B4-d | MUST | Cited K-factors; generator comparison for Z(νν)+jet and W+jet rates | every K has a citation; generator difference is the normalisation nuisance; no second generator for tt̄ and dibosons, stated (STR §4.7) | 2 / 3 | 4a | open |
| B4-e | MUST | Multijet plane probability from a looser population | factorisation tested on Z(νν) and W in MET bins within a factor 1.5; not flat → passing events only, floor stated (STR §4.7) | 3 / 4a | 4a | open |
| B5-a (DP1) | SHOULD | Road-rotation sideband: flatness of the hard-scatter component | sideband prediction of the signal-road count within a factor 1.5 at the evaluable rungs of R04–R07, on truth-attributed hard-scatter candidates. Full: 20 roads on 8,000 SM events; proposed reduced: 8 roads on 6,000 (R07 then not evaluable with pile-up) (STR §4.8) | 3 / 4a | 4a | open |
| B5-b | SHOULD | Non-flat part quantified | T_meas/T_flat − 1 per process with its error, on the no-PU hard-scatter samples (STR §4.8) | 4a | 4a | open |
| B5-c | SHOULD | Independence of roads | pair correlation \|ρ\| < 0.1 at R05 and R06 on samples with pile-up, or an effective-trials factor (STR §4.8) | 4a | 4a | open |
| B6-a (DP2) | SHOULD | Seven detector-model variations (resolution ×1.5, inefficiency 97 % incl. pile-up hits, material ×0.5 and ×2, top-up low and high, alternative tune) run as robustness tests, paired with nominal partner samples | every variation evaluated with error on ln(B_var/B_nom) < 0.1 at R06 and on ε_var/ε_nom < 10 %. Full: 6 signal points; proposed reduced: 4 (E 200/1.5, E 500/3, E 500/5, E 1000/3 keV) with the interpolation rule (STR §4.9) | 3 / 4a | 4b | open |
| B6-b | SHOULD | Classification | robust / not robust by the pre-declared thresholds; "not robust" items in the limitations (STR §4.9) | 4a | 4b | open |
| B6-c | SHOULD | Every shared detector nuisance evaluated on every term: pile-up, single-interaction, SM hard scatter, signal | table of STR §4.9 filled; P_geo and H re-measured under each variation | 4a | 4b | open |
| B6-d | SHOULD | Sizes of the detector nuisances from public Phase-2 numbers (R-15 to R-17); round-number variations are not nuisances | each nuisance has a cited size; effect scaled linearly from the measured shift, linearity checked on material; no public number → no nuisance, named as a limitation (STR §4.9) | 2 / 4a | 4a | open |
| B7 | SHOULD | Cosmic, beam-halo and beam-gas background as a number from public rates, pointing and timing | number with derivation; below 10 % of the 1σ uncertainty of the total background → stated, else a term of the likelihood (STR §4.10) | 3 | 4a | open |
| T1-a | MUST | pyhf workspace: Poisson auxiliary channel per simulated count (zero counts included; one per weight class), correlated nuisances, one route per term, closure-derived systematics; published | schema-valid (STR §4.11) | 3 | 4a | open |
| T1-b | MUST | v1 mode | reproduces the v1 best-point hybrid-toy limit μ₉₅ = 789.7 (1.2458×10⁷ events before selection / 15,775) within 10 % (STR §4.11) | 3 | 4a | open |
| T1-c | MUST | Zero-count convention: expected limits generated with each counted rate drawn from Gamma(m + 1), auxiliary observations fixed; one zero per term; terms labelled estimate / bound / no credit; f₀ reported | (i) one-bin m = 0 workspace reproduces the analytic limits within toy error; (ii) m = 100, 1000 reproduces the standard toy limit; (iii) coverage ≥ 0.93 on 500 pseudo-experiments with true λ·M = 0.5, 1.14, 2, 3; (iv) limit at the best point under the fixed-1.14 and Jeffreys alternatives reported (STR §4.11) | 3 / 4a | 4a | open |
| T1-d | MUST | Signal injection (conventions check 2) | at 0, 1, 2, 5 × μ₉₅^exp of three points, 200 fluctuated pseudo-experiments each: \|⟨μ̂⟩ − μ_inj\| ≤ 0.20 μ_inj; at 0: within 3 standard errors of the mean (STR §4.11) | 4a | 4a | open |
| T1-e | MUST | Pulls and constraints (check 3) | pulls on fluctuated pseudo-data (mean within 0.21); constraints on Asimov data, any below 0.5 of the prior explained (STR §4.11) | 4a | 4a | open |
| T1-f | MUST | Impact ranking (check 4) and pruning policy | ranking compared with expectation; pruning only below 1 % impact each and 5 % of the leading systematic in total (STR §4.11) | 4a | 4a | open |
| T1-g | MUST | Asymptotic against toy limits | tabulated at every point (STR §4.11) | 4b / 4c | 4c | open |
| T1-h | MUST | Coverage at a known signal (replaces the version-1 "toy self-consistency 50 ± 4.5 %", which was true by construction) | 500 pseudo-experiments at two points with μ_true = μ₉₅^exp, limits from stored distributions: fraction with μ₉₅ ≥ μ_true at least 0.93 (STR §4.11) | 4c | 4c | open |
| T1-i | MUST | Toys primary for every quoted limit | pass 1 at 4b (five best selections, 20 window points); pass 2 at 4c (chosen, runner-up, v1 fallback at 40 points); toy cost measured on a 60–100-parameter workspace in Phase 2 (STR §4.11) | 2 / 4b / 4c | 4c | open |
| T2-a | MUST | Selection rule: 16 declared candidates (R07 and family F fixed), eligibility ([SD8]: FAIL of a leading term's estimator → not eligible; NOT TESTED → no credit, GA-4), figure of merit G on the optimisation half with ε̂ = (k + ½)/(n + 1), split by a salted hash | rule, list, G, estimator and salt in the hashed pre-registration before S1 production (STR §4.12) | 3 | 3 | open |
| T2-b | MUST | Reproducible choice | second run from frozen inputs gives the same selection; else Gate B is not requested (STR §4.12) | 4b | 4b | open |
| T2-c | MUST | Optimisation-to-evaluation shift | reported per point; mean shift above 2σ reported as selection bias (STR §4.12) | 4c | 4c | open |
| T2-d | MUST | Background-side bias of the choice | 50 bootstrap replicas of the background inputs: frequency of the same winner and shift of its B₈₄ reported; tie rule if the winner wins in fewer than half (STR §4.12) | 4b | 4b | open |
| T2-e | MUST | Robustness against empty simulation | for the deepest candidate G under the convention is not better than with zero-count terms fixed at 1.14·N/M (within toy error), on v1 counts before the freeze (STR §4.12) | 3 | 3 | open |
| T2-f | MUST | "Background-free" (B₈₄ ≤ 0.11 per category, B₈₄ from the predictive distribution) reported as a flag only | flag in the results table (STR §4.12) | 4b | 4c | open |
| T2-g | MUST | Always-eligible baseline "R07-direct" (direct attributed counts and direct bounds only) | evaluated in every outcome; partial-outcome matrix of STR §4.12 followed | 4b | 4c | open |
| S1-a (GA-2) | MUST | 2,000 rows at each of the 40 points through the full chain (×10 rows in total, ×5 on the evaluation half that sets the limit; 4,000 rows if the user chooses so) | ≥ 99 % of jobs complete with ingestion closure (STR §4.13) | 2 (string) / 4a (chain) | 4a | open |
| S1-b | MUST | No fast path | no fast-path number in any result (STR §4.13) | 4a | 4c | open |
| S1-c | MUST | Efficiencies blind until the closure verdicts; evaluation half aggregated only after Gate B | first aggregation logged at 4b (optimisation) and 4c (evaluation) (STR §4.13) | 4b / 4c | 4c | open |
| S1-d | MUST | Statistical quality stated in advance, reported, never tuned | binomial error per point in the results table (STR §4.13) | 4c | 4c | open |
| S1-e | MUST | Optimisation/evaluation split by the frozen salted hash, independent of Λ | salt in `PREREG_v2.md`; two campaigns, two directories (STR §4.12, §4.13) | 3 / 4a | 4a | open |
| S1-f | MUST | Signal detector response consistent with the backgrounds: same MET model; migration across the 200 GeV generator cut measured on a 150 GeV sample; lepton-veto and calorimeter assumption stated; tracker hit-time window from a public source | m_mig quoted (≤ 5 % neglected, else generator cut lowered before the freeze); limitation L11 with the limit as a function of veto survival unless R-13 gives a number; hit-time loss as a systematic at ≥ 1 TeV or limitation L12 (STR §4.13) | 2 / 4c | 4c | open |
| S2-a | MUST | NLO K-factors computed with `loop_quirkE`, used only after three validations | model identity \|z\| < 3 and 0.5 %; fixed-order NLO against fixed-order NLO slepton reference within 3 % (or NOT EVALUABLE if no such reference, stated); differential K(M) against Drell–Yan within 2 % or 3σ; fail → v1 transcription labelled as such (STR §4.14) | 2 | 2 | open |
| S2-b (GA-5) | MUST | K(m) with scale and PDF errors for all masses; PDF4LHC21 and CT18NLO; resummed normalisation implemented as cross-check | table of σ_norm(m) with both PDF sets; every limit also quoted with σ_NLO × (NLO+NLL)/NLO (STR §4.14) | 2 | 4c | open |
| S2-c | MUST | f₂₀₀ recomputed with one definition (no η cut) and its uncertainty rebuilt and propagated into the limits | one script, one definition in text; scale, PDF, merging-scale, tune and FxFx (500 and 1,500 GeV) comparisons; nuisance in T1 (STR §4.14) | 2 | 4a | open |
| S2-d | MUST | QED-FSR shower is the nominal signal; FSR-off kept for C1 and for the quoted shift | nominal samples showered with the QED-FSR card (STR §4.14) | 2 | 2 | open |
| S2-e | MUST | Trigger turn-on from a public Phase-2 curve, with a nuisance; any threshold change decided before A is computed | cited figure and page; else reported "parametrised, not sourced" with the pre-declared wide nuisance (STR §4.14) | 2 | 4a | open |
| S2-f (GA-5) | MUST | Infracolour Coulomb correction to the production cross section, per mass, from the generated β distribution | number per mass with its source (R-12) or the label "not sourced"; default: one-sided band on the theory line (STR §4.14) | 2 | 4a | open |
| P1-a | MUST | Floor tests: extended-precision step map and mantissa-truncation kernel (both new code) | executed and read against the pre-declared table (floor / physical / inconclusive) (STR §4.15) | 2 | 2 | open |
| P1-b | MUST | B*-off as a paired test with power (≈ 970 events at 5 keV) and at 1 keV; the configuration of v1's test resolved first | pre-declared reading at 3σ (5 keV) and 2σ (1 keV) (STR §4.15) | 2 | 2 | open |
| P1-c | MUST | Population estimator for c defined in advance (paired median) and evaluated on new events; original gate reported as failed | \|median\|/median(c_ev) ≤ 1.5 % and ≤ 2σ at five points on 300 new events each (STR §4.15) | 2 | 2 | open |
| P1-d | MUST | Validity window stated as measured; failed straight-string ratio kept visible; Linux difference of one Stage-1 run followed up | table per (point, Λ, k_B bin) from the tracked results; text follows it (STR §4.15) | 2 | 5 | open |
| S3 | SHOULD | **dropped by user decision (brief D1)**; barrel-only paper; endcap gain stated as an EST outlook exactly as fixed in the brief | n/a | 5 (text) | 5 | dropped (user) |
| S4 | COULD | optional; strategy recommends not including it (DP4): ≥ 1 week and ≈ 700 CPU-h, delays the freeze | — | — | — | undecided, pending Gate A |
| S5 | COULD | optional; strategy recommends not including it (DP4): negative result stated instead | — | — | — | undecided, pending Gate A |

## Commitments from the strategy that are not plan items

| id | commitment | acceptance criterion (short) | phase | deadline | status |
|---|---|---|---|---|---|
| PR-1 | `PREREG_v2.md` hashed and committed before any v2 production sample; contents of STR §8 (including the number s_model per estimator, derivation and test rungs, power per test, K, the zero-count convention); analysis code frozen before production | 4-bot review PASS; sha256 in git before the first production marker; user notified | 3 | 3 | open |
| PR-2 | v1 kept by hash in an appendix, with the lost files listed and the freeze timing of the v1 analysis code stated | appendix text matches STR §8 | 5 | 5 | open |
| MVA-1 (DP3) | BDT cross-check with a pre-registered recipe, at equal total directly counted background; dE/dx forgone-gain ratio | ε_BDT/ε_R07 with one alternative architecture, and ε(R_k + dE/dx)/ε(R_k) for the chosen selection, both on the evaluation half (STR §3.2, §4.12) | 4c | 4c | open |
| REF-1 | Reference analyses R1–R4 tabulated; comparison targets of STR §6.2 overlaid on the limit and reach figures; "3 and 5 events at B = 0" reach quoted with v2 efficiencies; like-for-like efficiency breakdown against R1 Table I | present in the Phase-4a note (placeholders) and final in 4c | 4a / 4c | 4c | open |
| REF-2 | Retrieval tasks R-1 to R-20 (STR §6.4) from public sources, logged; nothing quoted from memory; R-10 closed before Phase 4a | each closed with a citation, or its dependent commitment reported as not sourced | 2 / 3 | 3 | open |
| FIG-1 | The seven flagship figures, the supporting figures and the seven diagrams of STR §9 | all present in the paper and the note | 4a–5 | 5 | open |
| RQ-1 | The 25 referee questions answered with a pointer to the text (STR §10) | adversarial review at Phase 5 | 5 | 5 | open |
| TG-1 (GA-3) | Central target as a reported outcome: total σ_ln = ½ ln(B₈₄/B₁₆) per category, f₀, the floor table and the outcome class (good / middle / real background / closure fails; estimated or bounded) | reported at the chosen selection with the pre-declared reading: "target met" if σ_ln ≤ 1 in both categories; "sample-size limited" if f₀ > 0.5, with the conservative band edge quoted (STR §4.4, §4.11) | 4a / 4c | 4c | open |
| ST-1 | Stop rules of brief §7 and D6, as quoted in STR §11.6: every overrun of the approved schedule reported; a projected compute overrun above 30 % stops the study and the user is asked; cajuela 2.0 TB / 1.0 TB free | re-projection with measured costs at day 7, at the freeze, weekly in production and when a conditional cost triggers; record in `STATUS.md` | 2–5 | 5 | open |
| INV-1 | Sample inventory with roles (development / derivation / test / production / reserve), seed streams and independence (STR §4.17) | every produced sample matches a row; no development sample enters a verdict; `DATA_MANIFEST.md` carries the stream names | 2–4a | 4a | open |
| BL-1 | Complete list of signal quantities that exist before the closure verdicts: the C1 tier approved in GA-1; A, f₂₀₀ and the migration fraction (selection-independent) | no other signal quantity in any artifact before the verdicts; B6 efficiency ratios and the tracker hit-time loss formed only after them (STR §4.1) | 2–4a | 4b | open |
| FP-1 | Failure protocol after the freeze: ticket always; bug → dated addendum and one re-test on a fresh sample; no bug → reported as failed, [SD8] | each FAIL or INVESTIGATE closed along one of the three branches; the second direct sample used at most once (STR §8) | 4a | 4a | open |
| GA | The ten decisions requested at Gate A (STR §12.1, GA-1 … GA-10) | each answered by the user and recorded in `LOG.md`; rows marked (GA-n) updated by a logged entry | 1 | 1 | open |

## Systematic plan (STR §5; every "will implement")

| id | source or check | how | phase | deadline | status |
|---|---|---|---|---|---|
| SY-1 | Signal cross-section theory: scales, PDF; infracolour Coulomb correction | 7-point envelope and PDF uncertainty on σ_NLO(m); band on the theory line; S2-f | 2 | 4a | open |
| SY-2 | Signal acceptance and ISR (one nuisance): f₂₀₀ and A; migration across the generator cut | S2-c; S1-f | 2 | 4a | open |
| SY-3 | Category migration (timing resolution and its tails) | variation within the public value (R-7) | 4a | 4a | open |
| SY-4 | Irreducible SM background: generator comparison and K | B4-d | 2 / 3 | 4a | open |
| SY-5 | Background normalisation of single-interaction terms: Geant4 against v1 rates; physics list (measured difference); material and composition only with a sourced size | B1-c; QGSP_BERT and composition variations (composition as a robustness test unless R-17 gives a range) | 3 / 4a | 4a | open |
| SY-6 | Extrapolation along the cuts (in place of "background shape") | closure nuisances with the extrapolation width that is always added: B1-b, B2-f, B3-d | 4a | 4a | open |
| SY-7 | Soft-QCD modelling of pile-up: tune; hadron species, string against cluster hadronisation at generator level after an install attempt (DP5) | B6 tune variation; Herwig or, after a documented failure, published data (R-19) | 2 / 3 / 4a | 4a | open |
| SY-8 | Monte Carlo statistics | T1-a auxiliary channels with the convention of T1-c; bootstrap | 4a | 4a | open |
| SY-9 | Detector model: resolution, inefficiency, material (sourced sizes), top-up density, evaluated on every term | B6-c, B6-d | 4a | 4b | open |
| SY-10 | Object calibration: MET model (signal and background), trigger, vertex identification, timing, tracker hit-time window | B4-b, S1-f, S2-e, R-8, R-7, R-14 | 3 / 4a | 4a | open |
| SY-11 | Luminosity (projection at 3 ab⁻¹; also 300 fb⁻¹) | public target (R-9) | 4a | 4a | open |
| SY-12 | Pile-up at fixed ⟨μ⟩ = 200: density and timing spread; no μ scan (user decision) | B6 | 4a | 4a | open |
| SY-13 | Study-specific: QED FSR shift, dropped status-4 string events, frozen admissibility transcription, seed-threshold convergence, signal MC statistics, lepton-veto assumption | quoted or as nuisances in T1 | 4a | 4a | open |
| SY-14 | Heavy-flavour decay vertices: check whether they are a separate topology; add to B1 if so | Phase-2 inventory | 2 | 3 | open |
| VC-1 | Closure tests (conventions check 1) | all closure criteria above with the definitions of STR §4.0; alarm bands χ²/ndf < 0.1 or > 3 | 4a | 4a | open |
| VC-2 | Signal injection (check 2), pulls and constraints (3), impact ranking (4) | T1-d, T1-e, T1-f | 4a | 4a | open |
| VC-3 | Goodness of fit (5) and look-elsewhere (6): not applicable to data; closure p-values reported; Bonferroni in C1; family-wise rule for the closure battery | STR §5.2, §4.0 | 4a | 4a | open |
| NA-1 | Declared not applicable (STR §5.1): beam energy; background shape as written; data/MC detector comparison as written; dE/dx calibration; b-tagging heavy-flavour treatment | justification in STR §5.1 | — | 4a (re-check) | n/a |
