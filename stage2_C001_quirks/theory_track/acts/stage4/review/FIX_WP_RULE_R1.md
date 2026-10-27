# FIX_WP_RULE_R1: fixer response to `REVIEW_WP_RULE_R1.md` (1 A, 9 B, 9 C)

Fixer, 2026-10-13. `WP_RULE.md` is now marked **FREEZE CANDIDATE** (not frozen). `plan.md` is not edited; the plan changes
are listed below and in WP_RULE §10.

**Signal-blindness.** No detector-level signal efficiency, signal toy or yield was computed. The signal-derived inputs
are all generator/truth level and pre-declared:
- δ₉₅: the reviewer's generator-level script; its value is adopted, not re-run.
- βγ_IT: from the existing f4r output.
- Truth TBPX quirk-hit counts n_q(m, Λ): for the dE/dx dilution model.

Compute ≈ 0.1 CPU-h, ≤ 3 processes, nice 10.

**Files.**
- Code: `acts/stage4/finder/{production.py, weights.py, validate_weights.py, wp_rule_tables.py, README.md}`, plus the new
  `finder/eadm_dilution.py`.
- Outputs: `data/acts_stage4/frozen/{frozen_inputs.json, eadm_dilution.json}` and `data/acts_stage4/wp_fix1/` (validation).
- Not touched: `finder.py` (sha unchanged), `chain_inputs.py`, `run_stage4.py`, `code/run_chain.py`, all G1-owned.

## Findings

| item | status | what was done |
|---|---|---|
| **A-1** road = δ₉₅ | **RESOLVED (finder side)** | `process_trial` raises `ValueError` unless `cfg.road == wcfg.delta95`. `cfg=None` builds `Config(road=wcfg.delta95)`. The row records road, δ₉₅ and η_max. New `production.config_from_frozen(fz)` builds both configs. This is compatible with G1's `run_stage4.finder_configs` (cfg.road = wcfg.delta95 = fz['delta95']). The smoke test confirms that a mismatched road raises. `test_equivalence` re-run at 0.25 on 4 trials: PASS, finder.py unchanged. Smoke run at 0.15 / η 1.0 for ρ = 1 and ρ = 2. A.3 hashes regenerated. |
| **B-1** dE/dx dilution | **RESOLVED** | (i) dE/dx now uses the **core** TBPX hits (\|u·n₂ − c\| ≤ 2.5 w_core). This is implemented in `weights.subset_weights`, `subset_weights_mc` and `production.dedx_sets`. (ii) Admissibility is dilution-aware: e_adm ≤ R_eff/1.25, with R_eff taken from the frozen mixture model `finder/eadm_dilution.py` (reviewer option a). The model inputs are truth n_q, the plan §2.1 μ_c with the core fraction at W_{k_adm}, and the Moyal proxy. A pre-declared PU-only update applies if the B1 density is more than 20 % above plan. New table A.2b: dE/dx is admissible only at k_adm = 4 for heavy masses (1.3 at E900-E1200 and Ẽ1000; 1.6 at E1300-E1500). The proxy is conservative relative to G1's Fatras model: R_eff is 4-9 % lower (`wp_fix1/eadm_fatras_sensitivity.json`). |
| **B-2** signal dE model / MIP unit | **RESOLVED (text); value PENDING-G1** | WP_RULE §1.4 now specifies two things. (1) Quirk deposits are draws of the Fatras Landau model over the same slab, using `code/eloss.py` (G1). (2) h_dE remains the truth record for V4-1. The MIP unit is defined as the pooled 0.6-truncated mean of all V4-9 muon-gun TBPX deposits, in the same dE convention. Closure: the sampler must reproduce the muon unit within 3 %. `mip_gev = null` (PENDING-G1) in frozen_inputs. |
| **B-3** D4-12 | **RESOLVED (user re-decision)** | The F0 selection is barrel-only, with the new fixed cut **\|η(n₃)\| < η_max = 1.0** applied in-job at every rung. The value is geometry-only: the TB2S L3 edge is 0.95 and the TBPX L4 seeding edge is 1.12 from the nominal IP. Endcap seeds, the endcap ladder and (L3, L2, L1) are future work. §8 "cannot claim" now covers \|η_pair\| ≥ 1, the 1.0-1.3 transition and the endcap; ε carries the fiducial loss. Logged as PC-7. |
| **B-4** δ₉₅ rule | **RESOLVED** | §1.3 now writes the procedure out as executed in `review_wp1/r1_inputs.py`: population, smearing, trigger and preselection weights, per-mass weighted q95, max over species-masses, rounded up to 0.01 → **0.15 rad**. The script and JSON hashes are in A.3. The σ⊥ variations are ε systematics only. |
| **B-5** SR-T | **PARTIALLY RESOLVED** | The definition is frozen: band, Δt from the earliest in-band hit, OOT overlay k ∈ {−12…+3}, the t_min rule, σ_t and Δt_acc. The in-job BTL-presence column is **not implemented**, because `process_trial` receives no BTL hits from the runner. WP_RULE states that the column **must exist and be q = 1-validated before any C1-B2 job**, and that **G3 runs without it**. |
| **B-6** f_CKF | **RESOLVED** | Formula: n_CKF,band/(n_CKF,band + n_band), using the final band. `process_trial(..., ckf=)` stores `n_ckf_band`, `n_band`, `f_ckf` through G1's `chain_inputs.ckf_band_counts`, so there is a single definition. B_PU gets a credit factor of 1 and the in-job ladders are f_CKF-free. SM, C′ and signal apply the cut. Synthetic smoke test (2 % of hits flagged CKF): median f_CKF = 0.015. Not done: the count of CKF tracks with ≥ 5 band hits, because no CKF track id is handed over. This is a diagnostic only. |
| **B-7** composition, D6 | **RESOLVED** | §6.2 gives the composition formulas for R15-R20, R21-R23, r_fb and SR-T. §1.4 freezes the h/o definitions: split at c, the per-hypothesis ndf, and the o ndf with bounds. An undefined value passes. |
| **B-8** counting convention | **RESOLVED** | §2 makes per-hit-set governing for B, T1/T1w/T1e, T3 at ≥ R04 and the trend test (rungs ≥ R04). Union counts are diagnostics. T1 lever arm = ⟨S_ded⟩/⟨N_grp(ρ = 2)⟩, also applied in §6.4. |
| **B-9** density σ_ln | **RESOLVED (option b)** | §4.1 adds a direct ρ = 1 re-run on the S6 dumps (2 000 C1 B1 events × 4 roads) at the lower and upper top-up values, ≈ 18 CPU-h. σ_ln = max \|ln ratio\| at each rung with ≥ 10 counts. Deeper rungs take the value at the deepest such rung. Option (a) was not implemented (cost and time); it may replace (b) only through a logged change before B2. |
| C-1 | applied | ε(Δφ cut) at A1/V4-3 is a diagnostic only (§1.3). |
| C-2 | applied | §6.4 adds the T_seed stability action (T_seed(ρ) := 4 on a > 2σ move, then re-time). |
| C-3 | applied | §5.4 item 11: G3 enters the union only if produced with the frozen hashes. |
| C-4 | applied (text) | §6.3 adds an nsub = 256 subsample diagnostic at G3. |
| C-5 | applied (text) | §1.4 adds the optional low-p resample variation. |
| C-6 | no change | Accepted by the reviewer. |
| C-7 | applied (code) | `row.meanW_pull`, with \|pull\| < 3 expected; smoke values 0.63 and 1.59. |
| C-8 | applied | Logged as PC-16. |
| C-9 | applied | §8 now says "both are reported wherever both exist". |

## Validation (PU-only, interim chain; `data/acts_stage4/wp_fix1/`)

- **Weights** (`weights_validation.json`, ρ = 2 trials 0-1):
  - V-a (DP vs MC, 1 280 sets): per-rung z rms 0.98-1.05, \|sum pull\| ≤ 1.32, M_max = 7.
  - V-b (vs f1r thin_weights): z rms 0.84-1.02.
  - V-c (q = 1, 2 000 sets): 0 mismatches on all 33 IS columns. The dE/dx columns are trivial here because the interim dE is 0.
  - V-d (IS vs plain MC): \|sum pull\| ≤ 1.41.
  - V-e (mean W vs DP): pull 1.50.
- **dE/dx branch** (`dedx_check2.json`): synthetic Landau deposits, with the width and χ² thresholds opened, on 300 sets
  with N_2S2 ≥ 3. The kernel at q = 1 and `dedx_sets` (core) give **0 mismatches on all 18 dE/dx columns**, with
  189/55/1 sets passing e > 1.3/1.6/2.0. `dedx_check.json`: core ≠ in-band estimator in 2-3 % of full-density PU sets,
  so the change is active.
- **Regression** (`regress_smoke.json`): new code at δ₉₅ = 0.25 with η off, compared with the pre-fix `production.py`
  (sha `2a26d00b…`, temporary copy removed). n_pass, n_grp, S_uni and S_ded are **bit-identical** on all non-dE/dx
  columns (ρ = 1 × 2, ρ = 2 × 1).
- **Smoke at the frozen values** (δ₉₅ 0.15, η_max 1.0). R04 keeps 441/737 and 309/446 (ρ = 1) and 19 318/28 890 (ρ = 2).
  t = 3-4 s (ρ = 1) and 28 s (ρ = 2), vs 37 s at δ₉₅ = 0.25 with η off. A mismatched road raises.
- **Finder equivalence** (`equivalence_rho1_wpfix1.json`, trials 0-3): PASS, with identical seeds, hit sets and rung flags.
- Reproduction: the ρ = 2 cache (318 MB) was deleted. Regenerate it with `WPV_OUT=data/acts_stage4/wp_fix1 pixi run python -m
  acts.stage4.finder.validate_weights cache 0 1` before re-running `dedx_check*.py`.

## Plan changes (logged in WP_RULE §10; plan.md not edited)

| id | change |
|---|---|
| PC-1 | Per-hit-set convention from R04 on; governing convention per test (PHASE_A §7.1, B-8). |
| PC-2 | ρ = 2 per-set weights stored only for samples (a)/(b) (PHASE_A §7.2). |
| PC-3 | Storage policy S1-S8 (PHASE_A §7.3). |
| PC-4 | Top-up carries resampled dE/t (PHASE_A §7.4). |
| PC-5 | IS nsub = 64, f_lo = f_hi = 1 (PHASE_A §7.5). |
| PC-6 | 43 in-job columns; h/o/SR-T factorised (PHASE_A §7.6). |
| PC-7 | **D4-12 re-decided: barrel-only F0, \|η(n₃)\| < 1.0; endcap and (L3, L2, L1) are future work.** |
| PC-8 | dE/dx over core TBPX hits. |
| PC-9 | Dilution-aware e_adm (R_eff/1.25). |
| PC-10 | f_CKF counted pre-removal; B_PU credit 1. |
| PC-11 | Density σ_ln from a direct ρ = 1 S6 re-run. |
| PC-12 | SR-T in-job BTL-presence column required before C1-B2; G3 without it. |
| PC-13 | MIP unit = pooled truncated mean of the muon gun. |
| PC-14 | Quirk deposits = Fatras-model draws over the same slab. |
| PC-15 | δ₉₅ population/aggregation rule; one global 0.15 rad; road = cut. |
| PC-16 | WP_RULE path `acts/stage4/WP_RULE.md`. |

## For the orchestrator / G1

1. `run_stage4.finder_configs` does not set `wcfg.eta_max`; it relies on the `WCfg` default 1.0. The runner should set
   it from `fz['eta_max']` (or use `production.config_from_frozen`) and assert equality.
2. The SR-T BTL-presence column needs the BTL hits (with INT) passed to `process_trial`. This must be implemented and
   validated before C1-B2.
3. Before setting `frozen = true` and copying the file to `acts/stage4/frozen_inputs.json`:
   - fill `mip_gev` from the V4-9 muon gun, after the B-2 sampler closure (≤ 3 %);
   - re-run `pixi run python -m acts.stage4.finder.wp_rule_tables`. This regenerates A.3 and `wp_rule_sha256`.
     G1-owned files (`run_stage4.py`, `run_chain.py`, `chain_inputs.py`, `eloss.py`) are still changing.
4. The current `frozen_inputs.json` has `frozen: false`, so the runner ignores it.
