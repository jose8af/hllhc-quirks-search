# REVIEW_ANALYSIS_R6: critical review of FIX_ANALYSIS_R6 (Stage-4 analysis pipeline, freeze b42aef4d…)

Reviewer: fresh critical reviewer, 2026-10-16. I wrote only this file and did not edit anything else.

**Compute used:**
- the selftest, at nice 15 with 2 threads (about 1 min);
- one single-core asymptotic sanity check;
- JSON scans of the stored outputs.

**Evidence base:**
- the fixer's background-only dev run on C12 inputs, made with the R6 code (`background.py` mtime 10:23 < run 10:29), at `scratchpad/bkg_r6/background.json`;
- the frozen `data/acts_stage4/analysis/C12_v1/background.json`;
- `data/acts_stage4/investigation/fixR6_*.json`;
- the code under `acts/stage4/analysis/`.

## Verdict: **PASS** (0 A, 0 B, 6 C)

## Freeze and selftest

- **Independent re-hash.** I re-hashed all 32 entries of `inputs/analysis_freeze.json` and found 0 mismatches. The freeze file's sha256 is `b42aef4d7b8df2b8…`.
- **Changes against the R5 freeze** (`bce02b6f`, saved copy). Exactly 12 files changed:
  - `background`, `common`, `hitrec`, `products`, `run_all`, `selftest`, `signal`, `stats`, `wp`;
  - `ambiguities.json`;
  - 2 new frozen inputs: `V46_REVERT_SET.json` and `jobs/A2FC.json`.

  No other file changed. This matches the fix list.
- **Selftest:** `SELFTEST PASS`, `freeze: true`. All R6 tests are true, and so are all earlier tests (R1-R4, including the R4 e2e).

## Item-by-item

**(1) `stats.py` saturated offset: correct.**
- `nll` subtracts `n − n ln n`, which is a data-only constant. It does not change q̃, and the toy calculator does not use `_model`.
- **Independent check (single bin).** With the exp(σα) model, the Asimov limit has the closed form μs/b = 1 − exp(−1.96σ).
  - b = 10⁸, σ = 0.9: the code gives 8.286 × 10⁷, and the closed form gives 0.829·b. ✓
  - b = 10⁶: the ratio to b is identical (scale-invariant). The relative-ftol stall is therefore gone.
  - b = 10⁸, σ = 0.05: 9.33 × 10⁶, which matches the closed form. ✓
- The selftest gives asymptotic/toys = 1.018 at E200 0.45 keV (FB0), where the frozen code gave 2.7 × 10⁻⁴.

**(2) A28 merge population restricted to `pops[:first[v]]`: correct reading, not anti-conservative.**

*Code.*
- `first[v]` is the length of `pops` when v's first cut is added. So `pops[:first[v]]` are exactly the populations that carry no added cut of v.
- `VAR_OF_REQ` is monotone in the requirement index and `todo` is sorted, so each variable's cuts are contiguous. Only cuts of v lie between `first[v]` and the current step.
- The merged factor N(P∧q)/N(P), with P the tightest v-free population with ≥ 10 entries, is therefore exactly the A28 "whole tail beyond P is one joint factor".
- All earlier factors of v are dropped. Later variables are measured on populations that contain the full v tail. A later cut of v after a merge also merges (N(P∧q₂) < 10 for every P implies the same for q₃ ⊂ q₂). So there is never more than one factor per v-tail, and no nested tail is multiplied twice.

*Scan of every chain* (567 chains, 585 merged factors; script logic: a merged factor's population must contain no added cut of its own variable, and no other factor of that variable may sit beside it):
- R6 run: **0 violations**.
- Frozen C12_v1: **32 violations**, all in the INV list:
  - `columns_T` FB2 and FB2e× (main and fact routes);
  - Z(νν), W(τ_h) and tt̄1ℓ at FB0, FB1 and their e variants.
- Frozen C1_v1: 24 violations.
- No ladder rung and no FB3/FB4 row is affected.

*Diff of the 24 changed base SM rows (frozen vs R6).*
- In every row, the **only** factor that differs is the merged χ² tail: its population loses the "& R09" cut and M becomes the start population.
- No zero-bound flag moved to another factor in any row.
- So the ×3000 drops come purely from restoring the factor that the frozen code had deleted, p(R09 | start) = 29/93 404. The fixed value equals the alternative product reading, 29/93 404 × 1.14/29 = 1.14/93 404, so it is not a new credit.

*Hand recomputation, SM row Z(νν) FB0 (R6 run).*

  19.5163 [P(R04), presel-weighted, 39 032.5/2000] × 1.14/93 404 × 1 × 28/29 × 19/28 × c 1.19636 × f_CKF 93 215/93 404

  = 1.8633 × 10⁻⁴ per event.
- σ·K·L = 14.272 pb × 1.4 × 3 × 10⁶ pb⁻¹ = 5.9944 × 10⁷.
- B = **11 169**, which equals the stored `B_new` (11 169.14). The ratio to the frozen value, 3.1048 × 10⁻⁴, equals 29/93 404 exactly.

*Hand recomputation, PU row SR-T FB2 (main route).*

  0.0653256 × 1.14/1874 × 1 × 15/16 × 11/15 × 1.19636 = **3.2685 × 10⁻⁵**
- This equals the stored `P_main`.
- The ratio to the frozen value is 16/1874 = 0.008538, which equals the stored ratio for all 4 FB2(e) T columns.
- The fact route gives 1.9534 × 10⁻⁵ with the same structure.

*Is it anti-conservative anywhere?* No.
- The fixed bound is the natural statistical reach of the sample: 1.14·f_presel/N_events = 1.14 × 0.419/2000 = 2.39 × 10⁻⁴ per event, the same number as the per-candidate form 19.52 × 1.14/93 404.
- No per-candidate clustering credit is taken.
- See C-1 for the remaining non-monotonicity.

**(3) Looper "low gun counts" (§7): implemented as written.**
- `gun_low` is true only for gun topologies with fewer than 10 C′_PU events containing an R01 attributed candidate.
- **R6 run:** only the looper qualifies (0 events). PV pair (14), γ (33) and the others are not affected.
- **Looper rows:** `P(R01) direct 0/100 000` (bound 1.14 × 10⁻⁵). The deeper requirements are "no population → 1" with σ_ln 1, and c is applied.
  - For example, R08 and R09 = 1.364 × 10⁻⁵, which matches the selftest's 1.14/10⁵ × c.
- The C′₀ bootstrap uses its own RNG stream, so the other topologies' draws are unchanged.
- See C-2 for a note on the rule itself.

**(4) D11 conservative C′ dE/dx and h/o: implemented per row as a maximum over two complete readings, with no mixing inside a chain.**

*dE/dx.* `row_term(col, False)` and `row_term(col, True)` each build one complete §4.2 Term:
- **Reading A:** the full C′_PU chain, including the dE/dx cut.
- **Reading B:** the C′_PU depth for the base column (`E_BASE_COL`), times the C′₀ attributed conditional p(e > x | tightest superset population with M ≥ 10), else 1 with σ_ln 1.

Each reading applies the one-bound rule internally. The selection is the tuple maximum `(P, σ_ln)`.

R6 run checks:
- 126 rows (7 topologies × 18). The looper is excluded because it is `gun_low`, and its C′₀ chain already gives the dE/dx factor no credit.
- In every row, `P_given_t == max(P_A, P_B)` holds exactly.
- The C′₀ reading is used in 121 rows and the C′_PU chain in 5 (ni30).

*h/o.*
- `cp_terms` compares `_f1_on_row` (B1-PU F1) against factor 1 (C′₀ has no hit records; this is recorded in `ho_c0`).
- Factor 1 is always ≥ F1. On a tie, the A reading wins because its σ_ln is larger. Both readings are recorded in `ho_reading`.

**(5) sep_IT^det core-only and the PU-200 flag: correct.**
- `hitrec.sep_it` masks with `cm`, and `signal.py:144` passes `cm`.
- `products.sep_it_det` sets `measurable = false` and the flag "NOT MEASURABLE AT PU 200 …" for every non-A1 key. A2, A5 and the A2FC replacements are all keyed `A2|…`, so they are all PU.
- `fixR6_sepit_E500.json`: median 41-48 mm → 19.3-34.2 mm. Prose nit in C-4.

**(6) A2FC substitution of the 9 revert points: mechanics correct.**

*Pre-declared.*
- `V46_REVERT_SET.json` was written at 10:19:30 by `v46_revert.py`, from the production A1 outputs. Its rule is "mean_f > 5 % OR pooled_f > 5 %".
- After that: `jobs/A2FC.json` at 10:20:25, `prod/A2FC/runner.pid` at 10:20:30, and the first A2FC output at 10:23:01.
- So the set was fixed before any A2FC output existed, and it is derived from different data (A1). There is no circularity.

*Pairing.*
- 180 A2FC jobs, 20 per point for each of the 9 points.
- For every job, `rows` and `seed` are identical to its `paired_a2_id` C1 A2 job (0 mismatches).
- A2 exists only in C1/C1a. C1b and C2B carry no A2 jobs, so the A2 accumulator for a revert point is exactly those 20 jobs.

*Exact row matching.*
- `apply_a2fc` replaces an entry only if three things hold: the sorted rows are identical, `probe_excluded` is equal, and `status_ne1` is equal.
- A missing A2 entry, a missing A2FC output or partial rows go to `missing`. That gives a `SystemExit` REFUSED unless `--dev`.
- The selftest covers the replace, missing and partial cases. On real files it covers both "without A2FC → REFUSED" and "C1a + A2FC → `A2|F|200|3|BM` replaced, no A2FC key in A5".

*Wiring.*
- `take()` excludes A2FC from every kind by default. It is taken only via `only=('A2FC',)` for the revert.
- The replaced entries flow into `signal_rows_a2` / `signal_obs_a2`, so SR-T ε and sep_IT use the same replaced records.

*Provenance.* Each replaced point records:
- the revert-set sha256, `replaced_by`, the job ids and `n_den`;
- ε R04/R14 for both numpy and full chain;
- `replaced_by_a2fc` per point.

## Category C (advisory)

- **C-1: B is not monotone across the FB columns, which the rule allows.**
  - After the fix, Z(νν) FB0 = 1.12 × 10⁴ < FB2 = 1.41 × 10⁴, although FB0's requirement set is contained in FB2's.
  - Both rows are zero-bounded at the same per-event reach (2.38 vs 2.27 × 10⁻⁴). They differ only through the 2S factors, measured on R04∧R09 (29 candidates, 0.655) versus R06 (81 candidates, 0.877).
  - This is statistical. The rule says explicitly that B need not be monotone (INV §3).
  - Optional: report it, or envelope FB_k ≥ FB_{k+1}.
- **C-2: the §7 low-gun rule takes a no-PU sample as the depth.**
  - The rule credits the looper 1.14/10⁵ from C′₀ (no PU), while C′_PU alone can only bound 1.14/500.
  - PU-assisted looper passes are not constrained at the 10⁻⁵ level.
  - The implementation is faithful to the pre-registered rule. The effect is −15-30 % on the B₈₄ rungs, and no conclusion changes. Worth a sentence in the report.
- **C-3: the V4-6 metric comes from A1 (no PU), not from the A5-with-PU wording of plan l.1254.**
  - INV §4's paired with-PU re-runs give ⟨f⟩ at or below the A1 value at all three checked points: 0.030 vs 0.052, 0.102 vs 0.135, 0.108 vs 0.141.
  - The union criterion adds margin. The set is plausibly complete.
  - State this substitution in the report.
- **C-4: the sep_IT prose numbers disagree.**
  - FIX says "19-24 mm". The stored file gives 19.3-34.2 mm (0.6 keV: 34.2, n = 29).
  - The code comment says "13-20 mm vs 1-7 mm truth", while FIX says "truth 1-29 mm".
  - This is text only. The flag makes the values non-results.
- **C-5: a missing revert-set file means no revert, silently.**
  - `a2fc_revert_set()` returns `[]` if `V46_REVERT_SET.json` is missing, which means no revert and no refusal.
  - The file is in the freeze, so a missing file breaks the freeze match and forces `--dev`. That makes this benign.
  - Raising an error explicitly would be cleaner.
- **C-6: D11 chooses the reading per row, so neighbouring rows can use different readings.**
  - For example, ni30 uses the C′_PU chain in 5 rows and C′₀ in 13.
  - This is by design under D11, and each row is internally consistent. Record the per-row choice in the results table, which `dedx_readings` already makes possible.

## Note for the orchestrator

The A2FC run was at 61 of 180 files at review time. The `C12_v2` run must use `--campaigns C1a,C1b,C2B,A2FC` without `--dev`. It will refuse until all 180 files are present.
