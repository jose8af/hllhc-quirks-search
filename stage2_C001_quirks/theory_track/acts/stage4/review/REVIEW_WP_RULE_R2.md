# REVIEW_WP_RULE_R2: narrow verification of the fix of `REVIEW_WP_RULE_R1.md`

Fresh critical reviewer (narrow verifier), 2026-10-13. Candidate: `acts/stage4/WP_RULE.md` (FREEZE CANDIDATE, sha256
`9e48821b…2be5` = `frozen_inputs.json` → `wp_rule_sha256`). Read: `REVIEW_WP_RULE_R1.md`, `FIX_WP_RULE_R1.md`, WP_RULE
(all sections), `finder/{production.py, weights.py (dE/dx/core parts), eadm_dilution.py, chain_inputs.ckf_band_counts}`,
`run_stage4.py` (finder_configs, refusal gates, C1 manifest; G1-owned, in flux), `frozen/{frozen_inputs.json,
eadm_dilution.json}`, `wp_fix1/*`, `g1/v49/v49.json`, LOG.md (D4-12, D4-16, D4-17 entries).

**Signal-blindness.** No detector-level signal efficiency, signal toy or yield was computed. The checks use only:
- generator/truth kinematics (the δ₉₅ script re-run, plus one barrel-only δ₉₅ diagnostic);
- truth TBPX hit counts, βγ and the Bethe ratio (the e_adm model re-run);
- geometry (`surfaces_s3.json`);
- PU-free config checks.

Compute ≈ 0.01 CPU-h. Scratch: `data/acts_stage4/review_wp2/`.

## Verdict

**NOT FREEZE-READY: 0 A, 2 B, 8 C.**

Both B items are cheap. B-1 is text only. B-2 is a runner gate plus text, or the column itself. After them the rule is
freeze-ready, pending only the G1 MIP number and the hash regeneration. No further review round is needed if the
orchestrator checks the two diffs.

---

## 1. Resolution of the R1 findings

| R1 item | status | evidence |
|---|---|---|
| **A-1** road = δ₉₅ | **RESOLVED** | See A-1 below. |
| **B-1** dE/dx dilution | **RESOLVED** | See B-1 below. |
| **B-2** signal dE model / MIP | **RESOLVED** (text); value delivered by G1 | See B-2 below. |
| **B-3** D4-12 | **RESOLVED** in substance (user re-decision recorded, PC-7) | See B-3 below. |
| **B-4** δ₉₅ rule | **RESOLVED** | See B-4 below. |
| **B-5** SR-T in-job | **PARTIAL by design; the gate is not yet safe** | See B-5 below. |
| **B-6** f_CKF | **RESOLVED** | See B-6 below. |
| **B-7** composition, D6 | **RESOLVED** | See B-7 below. |
| **B-8** counting convention | **RESOLVED** | See B-8 below. |
| **B-9** density σ_ln | **RESOLVED** (option b) | See B-9 below. |
| C-1…C-9 | applied as stated | Spot-checked C-2, C-3, C-7 (`meanW_pull`) and C-9. |

**A-1 (road = δ₉₅).**
- `config_from_frozen(frozen_inputs.json)` gives road = δ₉₅ = 0.15 and η_max = 1.0.
- `process_trial` with `Config(road=0.25)` against δ₉₅ = 0.15 raises `ValueError`.
- A frozen `finder_config.road ≠ delta95` raises `RuntimeError`.
- The runner's `finder_configs` (G1) now builds both configs from `config_from_frozen` and asserts road and η_max.
- `ckf_band_counts` takes `road=cfg.road`.

**B-1 (dE/dx dilution).**
- The core estimator is the same in three places:
  - `dedx_sets`: median and MAD over IT+PS hits, TBPX hits with |u·n₂ − c| ≤ 2.5 w_core;
  - `subset_weights`: `hit_[t]` inside the core loop;
  - `subset_weights_mc`.
- `dedx_check2.json`: 0/18 mismatches at q = 1.
- e_adm model, re-run in scratch (`r2_eadm_checks.json`):
  - **deterministic**: the e_adm table is identical to the frozen JSON, and so is every key except `inputs_sha256`;
  - **signal-blind**: its inputs are truth n_q, βγ_IT, the Bethe ratio and the plan §2.1 μ_c;
  - **conservative**: PU is taken at the width bound W_{k_adm}, and the Moyal proxy is below the Fatras-model sampler by
    4.5-10 % (re-run with the current `eloss.py` reproduces `eadm_fatras_sensitivity.json` exactly).
- The consequence is stated honestly in §8, A.2b and LOG 17:46: dE/dx is admissible only with k_adm = 4, at E900-E1500
  and Ẽ1000. See C-4 and C-5 for residual notes.

**B-2 (signal dE model, MIP).**
- §1.4 freezes the Fatras-model draws and the pooled unit, with the 3 % closure.
- G1 relay and `v49.json`:
  - pooled unit 3.5582·10⁻⁴ GeV;
  - sampler/Fatras ratio = 0.99955 (PASS);
  - per-kind KS p = 0.29-0.58.
- See C-2: use the pooled value, not the track median.

**B-3 (D4-12, barrel-only).**
- The cut is applied in-job before every rung, the grouping, the DP and the IS (`aligned`, `F &= aligned`, `allsel`,
  `r4`).
- The value is geometry-only.
- The §8 "cannot claim" list covers |η_pair| ≥ 1, the 1.0-1.3 transition, the endcap and the (L3, L2, L1) family.
- ε carries the fiducial loss.
- **But the stated derivation of 1.0 does not reproduce from the geometry file (B-1 below).**

**B-4 (δ₉₅ rule).**
- `r1_inputs.py` re-run in scratch gives **content identical** to `r1_inputs.json` (max 0.1489 → 0.15). Script and JSON
  hashes equal A.3.
- road == δ₉₅ is enforced (A-1).
- Two text precisions are in C-3.

**B-5 (SR-T in-job column).**
- The definition is frozen.
- The "must exist before any C1-B2 job" gate is text only, and it collides with the hash rules (B-2 below).

**B-6 (f_CKF).**
- One function, `chain_inputs.ckf_band_counts`, is used by both `process_trial(ckf=)` and the runner fallback (l.291).
- B_PU credit is 1.
- The in-job ladders are f_CKF-free: `F` carries no f_CKF term.

**B-7 (composition, D6).** §6.2 gives the composition formulas. §1.4 gives the h/o ndf, the bounds and "undefined passes".

**B-8 (counting convention).**
- §2 and §6.4 agree: per-hit-set is governing from R04 on, union counts are diagnostics, and the lever arm is
  ⟨S_ded⟩/⟨N_grp(ρ = 2)⟩.
- The trend test runs over rungs ≥ R04 with ≥ 10 B1 counts.

**B-9 (density σ_ln, option b).** The procedure is exact (the rule at rungs with ≥ 10 counts, the deepest-rung carry,
the same 2 000 events). Feasibility is in C-7.

---

## 2. Findings

### A (blocking)

None.

### B (must change before the freeze)

**B-1. The geometric derivation of η_max = 1.0 is wrong as written, and its own rule gives 0.9.**

WP_RULE §1.2 states these barrel edges asinh(z_half/r): 1.12 (TBPX L4), 0.95 (TB2S L3), 1.33 (TB2S L1), and ≥ 1.42 for
the other IT/PS layers. It then sets η_max = "the TB2S L3 edge rounded to one decimal".

From `sim/stage3/code/surfaces_s3.json`:

| layer | edge | WP_RULE says |
|---|---|---|
| TBPX L4 | 1.123 | 1.12, correct |
| TBPX L3 | 1.411 | inside "≥ 1.42", wrong |
| TB2S L1 | 1.304-1.307 | 1.33, wrong |
| TB2S L2 | 1.117-1.119 | not listed, although it is needed by R13 |
| TB2S L3 | **0.939-0.940** | 0.95, wrong |

The "complete seeding at |z_PV| ≲ 29 mm" statement is correct (172.2 vs 201.4 mm).

Rounding 0.94 to one decimal gives **0.9**, not 1.0. So the frozen "geometry-only" provenance of 1.0 does not reproduce.

The value itself is signal-blind either way, and 1.0 needs no change.

**Fix (text only; no value change, no re-run):**
- Write the correct edges, including TB2S L2 = 1.12.
- Define η_max = 1.0 as the TB2S L3 edge (0.94) **rounded up** to one decimal.
- State the consequence: for 0.94 ≲ |η(n₃)| < 1.0 (nominal IP) the axis leaves TB2S L3 coverage, so R14 and every FB
  selection (N_2S2 ≥ 3) have reduced acceptance there, for signal and background alike.

**B-2. The B-5 sequencing (BTL-presence column "before any C1-B2 job") is stated but not safe.**

(i) **No hard gate in code.**
- `process_trial` has no `btl` parameter (checked: `'btl' in signature` is False).
- The runner passes BTL hits only `if 'btl' in PT_PARAMS`, and otherwise runs silently.
- `PU_BLOCKS['C1']` holds B1 **and** B2. Jobs are sorted by `-est_s`, so the ρ = 2 jobs would start **first** once
  `frozen = true`.
- Nothing refuses a ρ > 1 production job without the column.
- R1 B-5 explains why ρ = 2 jobs without it leave SR-T's B₈₄ at ρ = 2 depth without a method: only per-trial sums are
  stored. B2 would then have to be regenerated.

(ii) **Conflict with the freeze hashes.**
- Adding the column after the freeze changes `production.py` and `weights.py`, so it changes A.3 and
  `frozen_inputs.sha256`.
- §5.4 item 9 ("any later finder change … re-run on B1/B2 and re-reviewed") and C-3 (G3 enters the union "only if
  produced with the frozen code hashes") then make any G3 or C1-B1 output produced before the addition ambiguous. That
  is a post-hoc inclusion decision.

**Fix:** either (preferred) implement and q = 1-validate the column before `frozen = true` (G1's runner is already wired
for `btl=`), or do all three of the following:
- (a) add a runner gate: refuse ρ > 1 production (C1/C2 B2, and G3B2 only if G3 is to enter the union) unless
  `process_trial` accepts `btl` and `frozen_inputs.sr_t.in_job_btl_presence == "validated"`;
- (b) pre-declare in WP_RULE §1.4/§10 that the addition is an additive amendment:
  - new columns only;
  - all 43 existing columns bit-identical on the `regress_smoke` comparison (ρ = 1 and ρ = 2);
  - q = 1 validation of the new column;
  - a logged A.3 hash addendum;
- (c) state that outputs produced before it with the frozen hashes (B1, G3) remain valid union members. At ρ = 1 the
  BTL factor is offline-computable from S2 + S5, so B1 loses nothing.

### C (optional notes)

- **C-1. βγ_μ: keep 92 (answer to the orchestrator relay).**
  - The difference from G1's 90.7 is immaterial. With βγ_μ = 90.7, R_eff changes by ≤ 0.09 % and no e_adm cell changes.
    Even βγ_μ = 60.2 (the |η| < 1 gun median) changes R_eff by ≤ 0.4 % with 0 cell changes (`r2_eadm_checks.json`).
  - F-3 is defined at generator level: the median of the gun definition is 92.5 from 2·10⁶ draws, frozen as 92.
  - The 90.7 is a 19 475-track statistic. Plausibly the cause is that only tracks with ≥ 1 TBPX hit enter, which drops
    high-|η|, high-βγ muons.
  - Replacing 92 would only churn the eadm and WP_RULE hashes. Record 90.7 as a cross-check in the mip block of
    `frozen_inputs.json`.
- **C-2. Fill `mip_gev` from `mip_unit.mip_gev_pooled_truncated` = 3.5582·10⁻⁴ GeV** (the frozen definition).
  - Do not use `mip_gev_track_median` = 3.924·10⁻⁴, which is +10 %.
  - `v49.json` → `mip_unit.definition` still describes the DRAFT per-track median (`frozen_definition` is correct).
    Fix the string so the provenance is unambiguous.
  - Sanity: 356 keV for a 1.124 mm Si-eq slab lies between the MPV (≈ 0.32 MeV) and the mean (≈ 0.44 MeV), as a
    0.6-truncated mean should.
- **C-3. δ₉₅ text precision.**
  - "One Λ point per species-mass" is, as executed, the lexicographically first p2 key (e.g. `L0.35`, not `L0.3`). This
    is harmless because p_qp is Λ-independent, but name it.
  - Jets = the 4 stored leading truth jets.
  - The statistical base is 200 template events per species-mass. R1 had suggested the full Stage-2 samples; the fixer
    kept the executed procedure. That is acceptable for a definition, but say so.
  - Barrel-only diagnostic (|η_pair| < 1, 47-76 events per mass): max 0.1525 (`r2_delta95_barrel_diag.json`), within
    the statistical noise. It is not re-tuned (by design), and ε(Δφ) at A1 covers it.
- **C-4. e_adm model assumptions.**
  - (i) "All n_q quirk hits in the core" is not guaranteed by the MAD core for an asymmetric two-cluster ribbon: if more
    than half the hits sit in one cluster, the MAD can shrink to that cluster. In that case the PU is also far below the
    W_k bound, so the net direction is unclear. Mention it as a model assumption.
  - (ii) n_q is selected on |η_pair| < 1, while the cut is on η(n₃). This is a minor mismatch.
  - (iii) Fatras margin: the text says 4-9 %; the measured range is 4.5-10 %.
- **C-5. The PU-density update trigger (> 20 %) is coarse compared with the cell margins.**
  - At μ × 1.2, 10 cells lose a level: F_m900 at Λ 5-10, F_m1300 at 5-10, F_m1400 at 7, and Ẽ1000 at 10-40.
  - The closest margin to a level is 0.5 % (F_m1300, Λ = 10).
  - The 1.25 margin and the Fatras-conservative proxy still cover this. Consider a > 10 % trigger.
  - Give the "B1-measured in-band TBPX crossing density" an operational definition: which population, and which band.
- **C-6. PC-8/PC-9 change what the user-approved D4-17 (i) fallback delivers.**
  - The principle is unchanged; the admissible dE/dx levels shrink to the k_adm = 4 cells.
  - D4-17 was approved as a concept before the e_adm numbers existed, so this does not override a decision.
  - Annotate the PC-9 row ("affects the D4-17 (i) deliverable") and tell the user at the freeze checkpoint.
  - The other PCs: PC-7 is the recorded user re-decision. PC-4 and PC-11 refine D4-15 without changing it. None of the
    rest touches a user decision.
- **C-7. B-9 feasibility.**
  - The ≈ 18 CPU-h S6 re-run (2 000 events × 4 roads × 2 variations × ≈ 4 s per ρ = 1 trial at δ₉₅ 0.15) is not in
    the C1 cost (96-109 CPU-h). With it, C1 is ≈ 114-127 CPU-h, still inside one Mac day (≈ 170-200 CPU-h). It adds
    ≈ 2.6 h of wall time at 7 workers and moves the D4-16 "C2 ends by Thu 22:00" condition by that much.
  - There is no runner job kind yet. Add a `C1-dens` block after the B1 jobs that write S6. The top-up is TT-level, so
    no Fatras or CKF re-run is needed.
- **C-8. Text/code convention.** §1.1 item 7 says the core is |u·n₂ − c| **<** 2.5 w_core. Every kernel
  (`kernels.py`, `weights.py`, `dedx_sets`) uses **≤**, and §1.4 also says ≤. Align the text (measure-zero difference).

---

## 3. Freeze checklist (after B-1 and B-2)

1. Fill `mip_gev` = 3.5582·10⁻⁴ (pooled; C-2). Keep βγ_μ = 92 (C-1).
2. Close B-2: either implement the column, or add the runner gate and the amendment text.
3. Wait until the G1 files are final (`run_stage4.py`, `run_chain.py`, `chain_inputs.py`, `eloss.py`). Then re-run
   `wp_rule_tables` (A.3, A.4, `wp_rule_sha256`). Set `frozen = true` and copy the file to
   `acts/stage4/frozen_inputs.json`.
4. Tell the user: PC-9 consequence (C-6), C1 + 18 CPU-h (C-7).

Scratch files (`data/acts_stage4/review_wp2/`):
- `r2_eadm_checks.py/.json` (determinism, βγ_μ and μ_c sensitivity, margins) plus `eadm_*.json`;
- `r2_rerun_r1_inputs.py/.json` (δ₉₅ reproduction);
- `r2_delta95_barrel_diag.py/.json`;
- `r2_eadm_fatras_sensitivity_rerun.py/.json`.
