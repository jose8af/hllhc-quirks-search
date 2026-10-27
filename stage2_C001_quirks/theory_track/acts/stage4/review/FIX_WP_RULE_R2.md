# FIX_WP_RULE_R2: fixer response to `REVIEW_WP_RULE_R2.md` (0 A, 2 B, 8 C)

Fixer, 2026-10-13. `WP_RULE.md` stays a **FREEZE CANDIDATE**, with `frozen = false`. The orchestrator sets the flag after
its final hash regeneration. `plan.md` is not edited.

**Signal-blindness.** No detector-level signal efficiency, signal toy or signal yield was computed. Every new check uses
PU-only trials, geometry, or the frozen truth-level e_adm model inputs.

**Compute.** ≈ 0.15 CPU-h, ≤ 2 processes, nice 10.

**Files.**
- Code: `acts/stage4/finder/{production.py, weights.py, wp_rule_tables.py, eadm_dilution.py (docstring only), README.md}`.
- Rule: `acts/stage4/WP_RULE.md`, `WP_RULE_tables.md`.
- Frozen-input candidates: `data/acts_stage4/frozen/{frozen_inputs.json, eadm_dilution.json}`. The e_adm table in
  `eadm_dilution.json` is unchanged; only `note` and `inputs_sha256` differ.
- Validation: `data/acts_stage4/wp_fix2/`.
- No G1-owned file was edited.

## Findings

| item | status | what was done |
|---|---|---|
| **B-2** SR-T in-job column | **RESOLVED (preferred fix)**, but one runner change is still needed (see below) | See "B-2 implementation" and "B-2 validation" below. |
| **B-1** η_max derivation | **RESOLVED** (text only, no value change) | §1.2 now gives the edges recomputed from `surfaces_s3.json`: TBPX L4 1.12, TBPX L3 1.41, TB2S L1 1.30-1.31, TB2S L2 1.12 (added; needed by R13), TB2S L3 **0.94**, and ≥ 1.57 for the other IT/PS layers. η_max = 1.0 is defined as the TB2S L3 edge (0.94) **rounded up** to one decimal. Consequence stated: for 0.94 ≲ \|η(n₃)\| < 1.0, R14 and every FB selection (N_2S2 ≥ 3) lose TB2S L3 coverage, which reduces acceptance for signal and background alike; ε carries it. |
| **C-2 / F-2** mip_gev | **RESOLVED** | `mip_gev = 3.558235445283726e-4` GeV (3.5582·10⁻⁴). Source: `g1/v49/v49.json` → `mip_unit.mip_gev_pooled_truncated`. `wp_rule_tables.mip_inputs()` reads it and asserts both the closure (sampler/Fatras 0.99955) and the value. `v49.json` is added to the A.3 hashes. Updated in §1.4, §10 F-2, A.4 and the header (the "only open input" sentence is gone). G1 had already corrected the `mip_unit.definition` string. `config_from_frozen` now yields `mip_gev > 0`, so the dE/dx columns are live. |
| **C-1** βγ_μ | **applied** | 92 is kept. 90.7 is recorded as `betagamma_mu_g1_measured`, with a note in `frozen_inputs.json` and a sentence in §10 F-3: it is immaterial (R_eff ≤ 0.09 %, 0 cells change). |
| **C-3** δ₉₅ text | **applied** | §1.3 now states: the Λ point used is the lexicographically first p2 key (`L0.35`, verified for all 17 species-masses); 200 template events per species-mass (verified); the jets are the 4 stored leading truth jets; the executed statistical base is acceptable for a definition. The barrel-only diagnostic max 0.1525 is noted as not re-tuned. |
| **C-8** core boundary | **applied: text changed to match code** | §1.1 item 7 now reads \|u·n₂ − c\| **≤** 2.5 w_core (closed interval), as in every kernel and in §1.4. The code is unchanged. |
| **C-5** PU-density trigger | **applied** | (i) Operational definition: ρ_dens = the μ_c-weighted mean over TBPX L1-L4 of N̄_l(B1, S6 dumps, pre-top-up Fatras measurements per event) / N_l(plan §2.1 table: 6686, 4901, 3564, 2811). (ii) The trigger is tightened from > 20 % to **ρ_dens > 1.05** (in `frozen_inputs.pu_density_update_trigger`). (iii) Margin statement: at × 1.05, R_eff drops ≤ 3.5 % and 3 cells (F_m1300, Λ 5-10) change level; at × 1.1, ≤ 5.5 % and 7 cells (`wp_fix2/eadm_mu_1p05_summary.json`, `eadm_mu_1p1_summary.json`). Below the trigger the drop is smaller than the proxy's smallest measured conservatism relative to the Fatras model (4.5 %). |
| **C-7** B-9 cost | **applied** | §4.1 now states: ≈ 18 CPU-h on top of C1 (96-109 → ≈ 114-127 CPU-h), ≈ +2.6 h wall at 7 workers, and the D4-16 Thu-22:00 condition moves by that amount. The runner job kind exists: G1 added `dens` (`DENS_BLOCKS['C1']`, run after B1). |
| **C-4** e_adm assumptions | **applied** (text) | §8 now carries the asymmetric-ribbon MAD caveat (direction not signed) and the η_pair vs η(n₃) mismatch. The Fatras margin is corrected to **4.5-10 %**. |
| **C-6** PC-9 vs D4-17 | **applied** (text) | The PC-9 row is annotated "affects the D4-17 (i) deliverable; tell the user at the freeze checkpoint". |
| **G1 relay: scipy Landau** | **unaffected; checked** | See "G1 relay: scipy.stats.landau" below. |

## B-2 implementation

`production.process_trial(..., btl=(B, INT_B), require_btl=None)` adds the SR-T first factor
P̂₁(r ∧ ≥ 1 in-band BTL hit) as 43 further columns (`RUNGS_T` = r + "&BTL"), one for each existing in-job column.

**Band.** The band is exactly the frozen §1.4 definition, about the candidate's final plane, axis and PV:
- u·n₃ > 0;
- \|u·n₂\| < W_c;
- \|n·u\| < 3σ_tot, with σ_n taken from the BTL local errors (16 / 0.9 mm in G1) projected on n, ⊕ t_tol.

`weights.btl_band` brute-forces over all BTL hits of the trial. The definition has no road pre-filter, so the code has
none either.

**ρ = 1 (every trial).** `n_pass_T`, `n_grp_T`: the full-set flags ∧ present, with the same per-hit-set groups as §2.

**ρ > 1, counting rungs (exact).** For a candidate with interactions S, let I_B be the distinct interactions of its
in-band BTL hits. Then

w_{r∧B} = w_r(S) − (1 − q)^|I_B| · w_r(S ∖ I_B)

The second term uses the existing DP on the set with the I_B hits removed (`weights.drop_interactions`).

**ρ > 1, per-subset rungs (IS).** `weights.subset_weights_btl` uses the same draws. For each subset T it multiplies the
IS weight by

f(T) = 1 if T keeps an interaction of S ∩ I_B, else 1 − (1 − q)^|I_B ∖ S|

The BTL-only interactions are integrated analytically, so f consumes no random number. `subset_weights` is now a
wrapper of the same core, with bit-identical output.

**Stored outputs.**
- Row: `S_uni_T`, `S_ded_T`, `V_uni_T`, and the run check `meanW_pull_T` (IS ΣW·f vs the exact DP P(R04 ∧ BTL)).
- Per stored candidate: `btl_n_band`, `btl_n_int`, `btl_dt0`. `btl_dt0` is Δt of the in-band hit with the smallest
  raw t, with t_PV = 0, because a PU-only trial PV carries no time.
- Per stored set: `w_T`.

**Not in-job, by construction.** The window [t_min, Δt_acc] and the out-of-time overlay stay out of the jobs. t_min is
fixed *from* B1 + overlay, so the jobs that measure it cannot apply it. Both enter P(late) offline, as the frozen
factorisation says.

**Gate.** Without `btl=`, a ρ > 1 trial raises `RuntimeError` when:
- `require_btl=True` is passed, or
- `require_btl` is None and `WCfg.require_btl` is True. `config_from_frozen` sets `WCfg.require_btl = fz['frozen']`, so
  the gate fails closed once the inputs are frozen.

**What the runner sets.** G1's current `run_stage4.py` already does the right thing:
- it passes `btl=` (all BTL hits + `btl_INT`) for G1-chain trials;
- it passes `require_btl=True` for every ρ > 1 job outside `DEV_CAMPAIGNS`;
- it refuses ρ > 1 production when `process_trial` lacks `btl=`.

No further setting is needed for the gate. G3B2 also gets the columns, so it can enter the union under §5.4 item 11.

## Runner change still needed (G1/orchestrator, BLOCKING for usable B2 output)

`run_stage4.pack()` keeps an explicit whitelist of trial-row keys, and the whitelist omits every new row key. In the
end-to-end run (`g1_integration.json` → `runner_pack_stores_T_row_keys: false`), the per-trial SR-T sums are computed
and then **discarded**. Only the `cand.*` keys (`btl_n_band`, `btl_n_int`, `btl_dt0`, `w_T`) reach the npz.

`pack` must also store the following, each `if k in trials[0]`:
- `trials.n_pass_T` and `trials.n_grp_T` (int64, shape (n, 43));
- for ρ > 1: `trials.S_uni_T`, `trials.S_ded_T`, `trials.V_uni_T` and `trials.meanW_pull_T`;
- scalars: `n_btl`, `n_btl_int`, `n_btl_present`.

A generic "pack every scalar or fixed-length row key" also works. The same gap already drops C-7's `meanW_pull`, as well
as `n_aligned`, `road`, `delta95`, `eta_max`, `mip_gev` and `n_ckf_hits`. These should be packed too: §6.3 and §S
require `meanW_pull`. This is a `run_stage4.py` change, so the A.3 hash changes after it.

## B-2 validation

All results are in `data/acts_stage4/wp_fix2/`.

**Inputs.** PU-only interim trials (`trials.py`) with the **real interim-Fatras BTL hits** of the same PU-200 events
(≈ 1 000 per event). Their interaction ids come from the trial's own scheme. The interim chain has no time column, so
the validation appends t = \|x\|/c + N(0, 35 ps). That time is used only by `btl_dt0`.

**1. Regression** (`btl_validation.json` → `regression`; ρ = 1 trials 0 and 1, ρ = 2 trial 0, frozen δ₉₅ 0.15 / η 1.0 /
mip 3.5582·10⁻⁴). Three versions were compared: the pre-fix code (temporary copy, sha `2c9f81b4…` production /
`dfe90dc5…` weights, since removed), the new code with `btl=None`, and the new code with `btl=`.
- Every pre-existing row, cand and hit key is **bit-identical** across all three versions, including the 43 columns of
  n_pass, n_grp, S_uni, S_ded and V_uni, meanW_pull, the weights `w` and the hit records.
- `btl=None` adds no key.
- `require_btl=True` (kwarg) or `WCfg.require_btl` without `btl=` raises at ρ = 2.
- BTL cost at ρ = 2: ≈ 1.0 s on a 29.5 s trial (band 0.69 s, DP 0.34 s).

**2. q = 1 closure** (trials 0 and 1, 131 k / 88 k aligned sets, 19 k / 7 k R04 sets).
- The DP BTL columns (drop identity) and the IS BTL columns (in-kernel factor) equal the full-set flags ∧ present with
  **0 mismatches on all 43 columns**.
- **Caveat:** at interim density the rungs from R08 on are empty, so those columns are trivially 0. f(T) is common to
  all columns of a draw, so the non-trivial columns (R01-R07, the N_L2 columns, meanW) exercise it.

**3. q = 1/2.** Two trials.
- **DP BTL vs a direct plain MC** (all interactions of S ∪ I_B ~ Bernoulli(q); 600 stratified sets per trial, 2·10⁴
  draws):
  - per-set pulls: rms 0.90-1.06 and mean \|·\| ≤ 0.18 on all 13 counting columns;
  - summed pulls: \|z\| ≤ 0.74 (trial 0);
  - trial 1 had one column at −2.49 (L2 ≥ 5). A re-seeded run with 4·10⁴ draws (`btl_validation_reseed.json`) gives
    −0.60 there and a max of \|z\| = 1.66, so it was a fluctuation.
- **IS mean(W·f) vs the exact DP P(R04 ∧ BTL)** (400 R04 sets, nsub 256): summed pull −0.72 and −0.38; per-set z rms
  0.90 and 0.89.
- **IS BTL columns vs the identity w(S) − (1 − q)^\|I_B\| w(S ∖ I_B)**, evaluated with the plain-MC reference
  `subset_weights_mc`: \|summed pull\| ≤ 1.74 on every non-empty column (w < 37.5 mm: −0.42 and +1.72).
- WisT ≤ Wis and S_uni_T ≤ S_uni everywhere.

**4. End to end through the G1 runner** (`g1_integration.json`). One ρ = 2 PU event, 1 road, run through
`run_stage4.run_pu_job` with the real G1 chain. It used **real G1 BTL hits with t and INT**: 2 215 hits from 293
interactions.
- The runner passes `btl=`; `require_btl` is not passed because g1bench is a development campaign.
- All pre-existing outputs are bit-identical to the same trial with `btl=None`. The only difference is `row.road`,
  which is a harness artefact: the runner overwrites it after the call.
- R04 has 12 058 candidates, 4 521 of them BTL-present. S_ded(R04) = 104.8 for the full set and 25.3 for ∧ BTL.
  meanW_pull is 0.00 and meanW_pull_T is −1.27.
- `btl_dt0` percentiles (1/50/99) are −0.35 / 0.26 / 1.90 ns.
- This run used the pre-regeneration candidate file (`mip_gev = −1`), so its dE/dx columns are NaN. The regenerated
  file has mip filled.
- The job's npz was deleted after the check.

## Observation for the orchestrator (definition question, not changed)

The frozen factorisation is P̂₁(r ∧ present) × P(late). With the out-of-time overlay, a candidate that has **no
in-time** in-band BTL hit can still have its earliest in-band hit from a k = +1 crossing (Δt ≈ 25 ns ± spread, at the
Δt_acc edge). Such a candidate could be tagged late, and that term is not in the product.

The complement P̂₁(r ∧ ¬present) = S − S_T is available in-job from the new columns. If the rule wants the term, it is
P̂₁(r ∧ ¬present) × P(late \| overlay only), which can be computed offline. Adding it would be a definition change for
the orchestrator and the reviewer. The fixer did not add it.

## G1 relay: scipy.stats.landau

- grep over `finder/*.py` and the `wp_fix1` and `review_wp2` scripts: **no `scipy.stats.landau` anywhere**.
- The frozen e_adm model (`eadm_dilution.py`) samples only `scipy.stats.moyal(loc = R, scale = 0.12 R)`, and its MIP
  unit is the same estimator on Moyal draws. The model is therefore unaffected and the table is not regenerated for
  this reason.
- The only Landau-dependent number is the Fatras-model diagnostic (`wp_fix1/eadm_fatras_sensitivity.json`). It was
  produced at 17:44, after `code/eloss.py` gained the CERNLIB mapping at 17:39. Its sha256 `3edcb325…` equals A.3 and
  equals the file today.
- Re-run with the final `eloss.py` (`wp_fix2/eadm_fatras_sensitivity_rerun.json`): **identical**. R_eff(Fatras)/R_eff(proxy)
  = 1.045-1.100.
- The dE/dx synthetic-deposit checks (`dedx_check*.py`) use Moyal test deposits. They are code-closure tests only, so the
  deposit shape does not matter.

## Neighbourhood checks

- **Stale values.** grep of `WP_RULE.md` for PENDING, "not implemented", 4-9 %, > 20 %, 0.95/1.33 and "rounded to one
  decimal" finds only intended survivors: the PC-12 history row and B-9 option (a).
- **Docstrings.** The `eadm_dilution.py` docstring trigger was 20 %; it now reads 1.05. The table was re-run: e_adm is
  identical, and only `note` and `inputs_sha256` changed.
- **§S storage table.** It now lists the new S1/S1′/S2/S7/S8 keys.
- **PC-17 added.** The header now says PC-1…PC-17.
- **Tables and hashes.** `pixi run python -m acts.stage4.finder.wp_rule_tables` was re-run. All A.3 hashes match the
  files, and `wp_rule_sha256` = `e61a9d0e…79cb9` matches `WP_RULE.md`. `frozen = false`.
- **`config_from_frozen`** on the new file: road = δ₉₅ = 0.15, η_max 1.0, mip 3.5582·10⁻⁴, require_btl False (not
  frozen).

## For the orchestrator

1. **G1:** add the `pack` keys listed above, then do the final hash regeneration.
2. Flip `frozen = true` and copy the file to `acts/stage4/frozen_inputs.json`. With `frozen = true`,
   `config_from_frozen` also sets `require_btl` (fail-closed). The runner's kwarg already enforces it.
3. Tell the user: the PC-9 / D4-17 consequence (C-6), C1 + 18 CPU-h (C-7), and the overlay/¬present observation above.
4. Reproduction:
   - `nice -n 10 pixi run python data/acts_stage4/wp_fix2/btl_validate.py`. The regression section needs the pre-fix
     copies restored as `finder/_prod_r1_tmp.py` and `_wg_r1_tmp.py`.
   - `BTLV_RESEED=1 BTLV_TRIALS=1 …` re-runs the re-seeded check.
   - `g1_integration.py` re-runs the end-to-end check.
