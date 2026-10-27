# Narrow verification S3-R3: Stage 3 fix pass R2 (C001 quirks theory track)

Reviewer: fresh narrow verifier, round 3, 2026-10-13. Protocol: `methodology/03-review.md` §6.1 (only Category A blocks).
Scope: are the R2 items (B-1, C-1…C-8 of `REVIEW_S3_R2.md`) resolved, and did the fix (`FIX_S3_R2.md`) break anything?
Scratch: `review/r3_checks/`. CPU used: ≈ 0.05 CPU-h (p2 sandbox rerun 157 s, the rest seconds).

## Verdict: **PASS** (0 A, 0 B, 3 C)

## 1. B*-context script rerun (check 1)

- `r3_checks/run_ctx.py` imports `scripts/fix_r2_bstar_context.py` unchanged. It reads the inputs from `results/` and
  writes to `r3_checks/res/`. Output: `run_ctx.out`.
- The sandbox `FIX_R2_bstar_context.json` is **byte-identical** to the delivered file (`cmp`; the seeded RNG gives this).
- Numbers confirmed:
  - B* off, all 160 events: +1.76 ± 0.70 %. Production, all 600 E 500 + E 1000 events: +9.74 ± 1.27 %.
  - Difference +7.98 ± 1.45 %, i.e. **5.50σ**.
  - Against the disjoint 440-event production complement: +7.97 ± 1.40 %, i.e. **5.68σ**.
- **Method.** The errors are bootstraps of the median (20 000 resamples, `bmed`). The paired on − off error resamples the
  event index jointly in both arms (`arm_diff`), which is correct for the same-event comparison. Production vs off adds
  the two independent bootstrap errors in quadrature.
  - The overlap concern is handled by the complement comparison (disjoint samples, independent). It gives a slightly
    larger significance, so the overlap did not inflate the 5.5σ.
  - The 5.5σ rests on the on-arm control (the `nm_kernel` arm reproduces production: same-event medians +10.3 vs
    +11.2 %, median |Δc| 1.4×10⁻⁵), not on pairing. The text says this correctly: it calls the 5.5σ "against
    production" and gives the paired 2.1σ separately.
  - Composition check (mine, `check_json.out`): the off sample is stratified at 32 events per k_B bin, and production is
    not (83/167/128/123/99). Reweighting the off arm to the production k_B composition gives +1.65 ± 0.64 %, against
    +1.76 % unweighted. The "all" comparison is therefore not biased by the stratification (see C-3).
  - Sound.

## 2. B*-attribution statements (check 2)

- **Table.** The VALIDATION §8.5 table matches `FIX_bstar_off.json` `bins.pooled`: on, off and paired rows, all values
  and errors, including −1.1 ± 4.4 (−0.2σ) at k_B 4-6. The <4, ≥6 columns and the production, per-event and floor rows
  match `FIX_R2_bstar_context.json`. The production-row significances are 0.9 / 3.7 / 2.3 / 2.3 / 2.8 / 3.7 / 4.0 /
  5.5σ. The per-event k_B ≥ 10 entry is +8 ± 19 %, IQR −30…+112 %. The floor at the sample's ε⊥ is 6.9-18.2 %.
- **Documents.** These all carry the same numbers and an explicit ESTIMATE on the attribution:
  - VALIDATION §0 preface and the auto row;
  - VALIDATION §8.5 "Reading";
  - README headline 4;
  - PROPOSED_CHANGES §1 (table and attribution bullet) and P-10;
  - DECISIONS_PENDING U-1.

  Each quotes 5.5σ against production, 2.1σ (all) and 2.3σ (k_B ≥ 6) paired, k_B < 4 "consistent with removal, 1.8σ",
  and the per-event widening sentence. PROPOSED_CHANGES §1 now has the same-event B*-on row next to the B*-off row.
- **Search over `*.md`, `scripts/*.py` and `results/FIX*.json`.**
  - "removes the bulk in every bin" appears only in VALIDATION:352, where it is quoted as withdrawn.
  - No "VERIFIED" tag is attached to the attribution. The JSON tags are "VERIFIED (measured, truth level); attribution
    remains ESTIMATE".
  - E8_session_log.md:40 keeps the historical "physical (B*)" line. It is a log, as accepted at R2.
- HANDOVER has no B* statement.

## 3. C-1…C-8 (check 3)

| item | status | evidence |
|---|---|---|
| C-1 control in c | OK | 5/160 events with \|Δc\| > 0.01, max 0.0907, Δs_B 0.027-0.11 µm (`control_c`, reproduced) |
| C-2 floor at subsample ε⊥ | OK | 6.9-18.2 % at k_B ≥ 10, every bin in the table (reproduced) |
| C-3 sep_IT slope errors | OK | sandbox rerun of `fix_r2_notes.py`: `FIX_R2_notes.json` byte-identical; ± 0.017-0.044, F_m1000 −1.985 ± 0.023 (R2 event bootstrap −1.987 ± 0.025, consistent); central slopes are P2.json's; in README headline 6, README auto block and HANDOVER §5.3 |
| C-4 robust totals | OK | 198/243 recounted independently from P2.json (components all ≥ 0, so the `<` test is valid); "upper bounds" in VALIDATION §9.12, HANDOVER, README |
| C-5 interpolated edges | OK | "fit (stat) only, 0.40-0.58 keV; neighbouring-mass systematic in Stage 4" in VALIDATION §9.8 and HANDOVER |
| C-6 c06 model zero | OK | **4** events (independent: the `paired_ratio_n_model_zero` leaves in P1.json sum to 4; the script lists the same 4 rows); none at 7-10 keV; VALIDATION §9.11, HANDOVER §5 |
| C-7 figures | OK | see §5 |
| C-8 one ACTS event | OK | "requirement not yet tested" in HANDOVER §4 action 3 and VALIDATION §5 (V8) |

## 4. Regression (check 4)

- **md5 values.** P1.json b25f18ed…, P2.json df1b7c68…, P2_points.json 1eb173be…. These are:
  - equal to the values recorded in FIX_S3_R2.md;
  - equal to R2's sandbox reproductions (`r2_checks/repro/results/`).
- **Script changes.** The only differences between `p1_results.py` / `p2_results.py` and R2's copies are figure code and
  the `--figures-only` switch.
- **Sandbox rerun.** I reran the current scripts in a sandbox (`r3_checks/repro/`, with RES, FIG and the numba cache
  redirected; 11 s + 157 s). The output reproduces all three md5s exactly.
- **Delivered files.** The delivered `results/` md5s are unchanged after my checks.

## 5. Figures (check 5)

- **`p2_observables.png`.** The top-row x labels no longer collide with the bottom-row tags. All 7 panels carry "Private
  work (simulation) -- truth level". It is readable.
- **`p1_v2b_revisit.png`.** The identity check is now in its own right panel, with its own x label ("median shift from
  stratified permutation [%] (identity check, not a model)"). The README caption is updated. Both panels carry the
  truth-level label. It is readable.
- **Labels.** `fig_label` writes only the private-work / truth-level label. No CMS, ATLAS or Preliminary string appears
  in `p1_results.py`, `p2_results.py` or `s3common.py`.

## 6. Findings

**A:** none. **B:** none.

**C-1 (wording).** PROPOSED_CHANGES §1, after the 5 keV table: "The first three rows pool the 5 points". Only the first
two data rows do; the third row is the B*-off block header. This is harmless.

**C-2 (error quoted twice).** k_B ≥ 6 paired on − off is +27.6 ± 12.1 % (the R2 reviewer's rebuild) in the prose of
README, PROPOSED_CHANGES, P-10 and U-1. The table and JSON give ± 11.8 %. VALIDATION explains the difference, and it is
2.3σ either way. Optionally, use the JSON value everywhere.

**C-3 (optional sentence).** The "all" B*-off median comes from a k_B-stratified sample, and the production median from
the natural population. Reweighted to the production composition, the off median is +1.65 ± 0.64 % (unweighted
+1.76 %), so the 5.5σ stands (`r3_checks/check_json.out`). One sentence could record this.

**R2 status:** B-1 and C-1…C-8 are resolved. The fix introduced no regression.
