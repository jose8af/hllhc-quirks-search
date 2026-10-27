# `acts/stage4/finder/` — production F0 finder (fast, G2a)

The F0 quirk finder of plan §2.2 with the selection of the reference probe
`acts/stage4/probes/f1r_finder.py` (fix R1/R2), re-implemented so that one PU-only trial at the adopted
TDR-normalised density (IT + OT top-up) takes **≈ 3.8 s instead of ≈ 211 s** (the reference with the merge
vectorised; ≈ 5 500 s as coded). The candidates are the reference's: identical seeds and identical candidate hit
sets on 24 PU-only trials (2 514 806 candidates; `test_equivalence.py`). Measured numbers are in
`../G2A_REPORT.md` and `data/acts_stage4/g2/`.

**Environment.** theory_track pixi env (`../../../pixi.toml`), which already has numba 0.68 — the same env as the
reference probe and as plan §1.8 ("finder … TT (numba)"). Nothing was installed; the acts env is unchanged.
Run everything from `theory_track/` as modules, e.g. `pixi run python -m acts.stage4.finder.bench_g2a 1 0 32`.
(The numba on-disk cache is keyed to the import path: always import as `acts.stage4.finder`.)

## Files

| file | content |
|---|---|
| `finder.py` | `find(H, sid, pv, phimet, cfg, INT, SIG, rho, store, ...)`: road, index build, seeds, refits, merge, stored variables, thinning weights of the top candidate; `Config` |
| `kernels.py` | numba kernels (index queries, seed score, gather + refit, hash merge, candidate variables) |
| `trials.py` | PU-only G2 trial set: ρ = 1 trial i = fix-R1 PU event i + top-up; ρ = 2 trial i = events (2i, 2i+1) superposed; PV, MET road from `default_rng(4 200 000 + 1000 ρ + i)` |
| `reference.py` | the reference: `f1r_finder.trial` logic with the merge vectorised (same order and criterion), outputs to `data/acts_stage4/g2/ref/` |
| `test_equivalence.py` | reference vs fast on the same trials: seeds, candidates (hit sets, order, variables), per-rung counts and pass flags; writes `data/acts_stage4/g2/equivalence_rho1.json`, exit ≠ 0 on failure |
| `bench_g2a.py` | G2a/G2b timing (one process, one thread), `data/acts_stage4/g2/timing_rho{1,2}*.json` |
| `mem_probe.py` | peak memory of one finder process |
| `g2a_campaigns.py` | plan §6.2 campaign table at the measured t₁, t₂ (`f3r_campaigns.blocks`, read-only) |
| `bench_g2b_core.py` | G2b input: per-set cost of the per-subset χ²_core recomputation (`kernels.chi2core_subsets`, plan §4.1 step 3b) on ρ = 2 sets |
| **Phase A (2026-10-13)** | |
| `weights.py` | in-job ρ > 1 thinning weights: exact counting-rung DP (`count_weights`), importance-sampled per-subset families conditional on N_IP2 ≥ 7 (`subset_weights`: w_core, χ²_core, 2S, dE/dx, fallback F0 parts), plain-MC references, distinct-hit-set grouping (`group_sets`; `group_sets_fast` is an exact prefix-filter variant, slower at this density, kept for reference) |
| `production.py` | per-trial production path: finder → groups (R04) → full-set rung flags (43 columns `RUNGS`) → ρ > 1 weights → storage policy (WP_RULE.md §S); `WCfg` (frozen nsub = 64, f = 1, δ₉₅ planning 0.25) |
| `pu_inputs.py` | production PU-only trial inputs from a chain event: interaction ids, TDR top-up with dE/t resampled, BTL hits, PV |
| `validate_weights.py` | DP vs plain MC (1 280 sets), vs f1r thin_weights, q = 1 full-set check, IS vs plain MC, mean W vs DP → `data/acts_stage4/g2b/weights_validation.json` |
| `bench_g2b.py` | G2b timing of the full production path on the G2a ρ = 2 trial set → `data/acts_stage4/g2b/timing_g2b_<tag>.json` |
| `g2b_criterion.py` | plan §6.2/§11 G2b criterion for the user's set (C1 → C2, C4′ optional) → `g2b_criterion.json` |
| `wp_rule_tables.py` | frozen-input tables and sha256s for WP_RULE.md appendix A |
| **Fix WP_RULE R1 (2026-10-13)** | |
| `production.py` | `process_trial(..., cfg, wcfg, ckf=)`: raises unless `cfg.road == wcfg.delta95` (A-1; `cfg=None` → `Config(road=delta95)`); fixed cut \|η(n₃)\| < `WCfg.eta_max` = 1.0 (barrel-only, PC-7); dE/dx over core TBPX hits (`dedx_sets`, B-1); per stored candidate `n_band`, `n_ckf_band`, `f_ckf` via `chain_inputs.ckf_band_counts` (B-6); `row.meanW_pull` (C-7); `config_from_frozen(fz)` |
| `weights.py` | `subset_weights` / `subset_weights_mc`: dE/dx buffer filled from the per-subset core IT hits (B-1) |
| `eadm_dilution.py` | frozen dilution-aware dE/dx admissibility e_adm(m, Λ) → `data/acts_stage4/frozen/eadm_dilution.json` |
| `wp_rule_tables.py` | + A.2b e_adm table, A.4 frozen inputs; pastes Appendix A into WP_RULE.md; writes `data/acts_stage4/frozen/frozen_inputs.json` |
| `validate_weights.py` | `WPV_OUT=<dir>` redirects cache/output; V-c also checks the 18 dE/dx columns against `dedx_sets` |
| **Fix WP_RULE R2 (2026-10-13)** | |
| `production.py` | `process_trial(..., btl=(B, INT_B), require_btl=None)`: SR-T in-job first factor, 43 columns r ∧ BTL-present (`RUNGS_T`): row `n_pass_T`, `n_grp_T` (every ρ), `S_uni_T`, `S_ded_T`, `V_uni_T`, `meanW_pull_T` (ρ > 1); cand `btl_n_band`, `btl_n_int`, `btl_dt0`, `w_T`. ρ > 1 without `btl=` raises if `require_btl` (kwarg; the G1 runner passes True for production) or `WCfg.require_btl` (= `frozen` via `config_from_frozen`). `btl=None`: all pre-existing outputs bit-identical, no new key |
| `weights.py` | `subset_weights` → wrapper of `_subset_core` (bit-identical); `subset_weights_btl` (same draws + per-subset BTL factor f(T)); `btl_band` (in-band BTL hits, WP_RULE §1.4); `drop_interactions` (S ∖ I_B for the exact DP identity) |
| `wp_rule_tables.py` | mip_gev from `data/acts_stage4/g1/v49/v49.json` (pooled, closure-checked); SR-T status; density trigger 1.05; v49.json hashed |

`find(..., want_csr=True)` (Phase A) returns the same candidate hit lists as `want_hits` as one CSR (`csr_off`,
`csr_hits`; kernel `kernels.csr_hits`); default behaviour unchanged, `test_equivalence` re-run and PASS
(`data/acts_stage4/g2b/equivalence_rho1_phaseA.json`).

## Algorithm (unchanged selection; reference semantics)

Per trial (one PU-only event or superposition, one MET road; PV frame u = x − PV):
1. **Road**: barrel counting surfaces (TBPX L1-4, TBPS L1-3 in/out, TB2S L1-3 in/out), |Δφ(u, φ_MET)| <
   0.25 + asin(min(1, W_c/r)), W_c = 75 mm.
2. **Seeds**: (a ∈ TBPX L4, b ∈ L3), |Δφ_ab| ≤ 0.3, |Δη_ab| ≤ 0.2, sin∠(u_a, u_b) ≥ 10⁻³; plane n = unit(u_a × u_b),
   σ_seed = 0.03/(|u_b| sin∠), axis = unit(û_a + û_b); requires some c ∈ L2 with |Δφ_bc| ≤ 0.4 and
   |n·u_c| ≤ 3 √(σ_n² + t_tol² + (σ_seed |u_c|)²); seed score = number of layers with ≥ 2 crossings (IT: hits;
   stacked OT: min(n_in, n_out)) among hits forward of the PV (u·axis > 0), |u·n₂| ≤ W_c and inside that band;
   kept if seed N_L2 ≥ T_seed = 6.
3. **Refit** (every kept seed): pre-filter |u·n_seed| < 5 mm (IT, PS) / 60 mm (2S); 3 iterations of the
   PV-constrained weighted plane fit (smallest eigenvector of Σ w u uᵀ, w = 1/σ_tot², σ_tot² = max(σ_n, 10⁻⁴)² + t_tol²,
   t_tol = 30 µm) with re-collection at 3σ_tot, forward and |u·n₂| < W_c, axis re-estimated each iteration as the
   in-plane mean hit direction; candidate if N_L2 ≥ 4.
4. **Ranking and merge**: sort by (−N_L2, χ²/ndf) (stable), drop a candidate whose normal is within 2 mrad
   (|1 − |n·g|| < 2·10⁻⁶) of an already kept one.
5. **Stored variables** (per kept candidate, from the final hit set, final normal and axis): N_IT2, N_OT2, N_L2,
   N_OT2h, N_L2h, N_L1, χ²/ndf, n_hit, Δw (rms), **w_core** (= f1r `dw_core`), **N_IP2, N_2S2, χ²_core, n_core**
   (plan §2.2 item 5 ladder variables), |n_z|, |Δφ(axis, MET)|, seed N_L2, the hit list; thinning weights
   (f1r `thin_weights`) of the top candidate.

## How it is made fast (no selection change)

| stage | reference | fast | measured ρ = 1 (mean of 24 trials) |
|---|---|---|---|
| seed score | every (a, b) pair scans all ≈ 4·10⁴ road hits | per-trial (φ-bin × z-cell) index per surface; per bin the z interval of the band follows from exact bounds of r(n_x cos φ + n_y sin φ) over the bin; only the two φ lobes \|sin(φ − φ_axis)\| ≤ (W_c + tol)/r are visited (exact: projection onto xy is a contraction); per-layer counting stops at 2 crossings and the score stops when pass/fail is decided | 95 s → 1.3 s |
| c search | linear scan of all L2 hits | same index, lobe φ_b ± 0.4 | (incl. above) |
| refit | each iteration scans all road hits | hits gathered once per seed for every plane within δ = max(2·10⁻⁴, 1.5 σ_seed) of the seed normal (proven bound \|u·n₀\| ≤ 3σ_tot(n) + δ\|u\|, σ bounded with \|n_z\| + δ); \|n_it − centre\| ≤ δ verified at every iteration, else re-gather around n_it and resume (pre-filter always w.r.t. the seed normal); branch-free selection pass, then accumulation; smallest eigenvector by inverse iteration with the adjugate (LAPACK eigh fallback); coarser second index for this gather | 30 + 52 s → 2.2 s |
| merge | Python O(N²) loop | hash grid on the normal (2.1 mrad cells, ±n), same greedy order and criterion | 5 300 s (33 s vectorised) → 0.05 s |
| variables | numpy refit per candidate | numba from the stored final hit set | → 0.26 s |

## Every difference from `f1r_finder.trial` (semantics and outputs)

1. **None in the selection.** Seeds, refits, ranking, merge criterion and the rung variables are the reference's.
   Equivalence (`test_equivalence.py`, 24 PU-only trials at the full density): identical seed sets
   (4.1·10⁶ seeds), identical candidate hit sets in identical rank order (2 514 806 candidates), identical integer
   variables, floats within 2·10⁻⁸ relative, identical per-rung counts, distinct-hit-set counts and per-trial pass
   flags for every F0 rung.
2. **Float-level only** (summation order, squared-form band comparisons d² < 9σ², inverse-iteration eigenvector):
   a hit exactly at a band edge could flip; none seen in 2.5·10⁶ candidates.
3. **Duplicate-group representative.** In 0.10 % of candidates the kept member of a 2-mrad duplicate group is a
   different seed than the reference's (the group members tie in (N_L2, χ²/ndf) to the last bits, and the summation
   order differs). Hit set, rank and all rung variables are identical; the normal differs within the 2 mrad merge
   tolerance; the stored seed N_L2 (a property of the seed) differs for 456 of 2.5·10⁶ candidates.
4. **Seed N_L2 stored as a lower bound** (≥ T_seed) by default (early termination); the exact value with
   `Config(seed_n2_exact=True)` (+0.5-2 s/trial). It is a stored diagnostic, not a rung variable.
5. **`store='loose'`** (production): only candidates passing the loosest ladder rung (N_IT2 ≥ 3 and N_IP2 ≥ 4) are
   returned, and w_core/χ²_core are computed only for them. A candidate failing it cannot pass any rung. The merge
   still runs over all candidates, so the stored ones are exactly the reference's passing ones.
   `store='all'` returns every N_L2 ≥ 4 candidate (the reference output).
6. **New stored variables** (plan §2.2 item 5, not in f1r): N_IP2, N_2S2, χ²_core (one-step core c ± 2.5 w_core of the
   IT+PS hits, 2S hits within the interval ± 3σ of their n₂ projection; λ_min/(n_core − 2)), n_core, |Δφ(axis, MET)|.
   They use the **final** refit axis, as f1r's `dw_core` does (the f2r_profile diagnostic used the seed axis).
7. **Thinning weights**: `thin_mode='top'` (default) = the f1r ρ = 1 behaviour (top candidate). `thin_mode='all'` =
   the f1r ρ > 1 behaviour (every stored candidate, 2·10⁴-subset MC) is kept for reference but is unaffordable at
   the full density (≈ 3·10⁵ sets × 23 ms per ρ = 2 trial); the production ρ = 2 weights need the plan §4.1 step 3b
   methods (G2b; see the report).
8. Hit lists are road indices sorted ascending (as the reference `hidx`).

## Implementation-only parameters (`Config`)
`arc_mm`, `arc_mm_refit` (φ-bin widths per surface, seed and refit indices), `dz_mm` (z cells), `dfac`, `dmin`
(gather margin), `seed_order`, `early`. They change the speed, never the output (checked: seed sets identical for
five layer orders; equivalence at the defaults). Speed is flat (±5 %) for ×0.5-×2 changes of the refit-index
bins; the seed index prefers the finer default bins (×2 coarser: +5-15 %).
