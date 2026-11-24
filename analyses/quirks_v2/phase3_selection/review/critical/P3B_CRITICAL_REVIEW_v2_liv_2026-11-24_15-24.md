# P3B critical re-review, cycle 2 (1-bot, Phase 3): work package p3-b (B2 pile-up)

Reviewer Liv (Opus, critical reviewer, fresh to this artifact). Session start 15:16 -0500 (`date`); session log
`phase3_selection/logs/reviewer_liv_2026-11-24_15-16.md`. I opened no signal sample.

**Artifact:** `outputs/P3B_PILEUP_v2_ivar_2026-11-24.md` ("v2"). I read v2 in full. I also read:
- the cycle-1 reviews DOR (`review/critical/P3B_CRITICAL_REVIEW_dorte_2026-11-24_14-22.md`) and ELI
  (`review/validation/P3B_PLOT_VALIDATION_elias_2026-11-24_14-22.md`);
- the rulings ADV (`review/advisor/ADVISOR_B2CAP_freja_2026-11-24_14-23.md`, with Addendum 1, "ADV-A") and KET
  (`ADVISOR_DEVPU1_ketil_2026-11-24_14-54.md`);
- the fixer log `logs/fixer_ivar_2026-11-24_14-48.md` and the p3-b blocks of `experiment_log.md` (l.126-215);
- the code `src/p3b/is_check.py`, `pileup_term.py`, `plots.py`, and the relevant parts of `occ_model.py`;
- `outputs/p3b/{pileup_term,b2_dev_closure,is_check,is_check_stats}.json` and `SCHEMA.md`;
- the three figures (PNG, read visually);
- the frozen texts STR §4.0 points 4 and 7 (l.380-525), §4.5 (l.1119-1228), §4.12 table (l.1870-1882), §11.7
  (l.2713-2780), COM l.38 and l.184-190, and the notice `notices/2026-11-24_1447_RESULT_…`.

**My own computation:** `review/critical/liv_ischeck.py`, output `liv_ischeck.json`. It ran on maxwell as 1 process at
nice 19, read-only, in 11 s CPU, with SLOTS lines at 15:19. It re-analyses the fixer's per-configuration B3 outputs
(`/home/scratch/jdochoa/ivar-ischeck-{0,1,2}/ischeck-*.npz`) together with the 8 stored `p3-b-occmod` files.

Tags: [V] I re-derived it (file or command cited); [U] taken from the artifact without a check; [E] estimate.

## 0. Verdict

**ITERATE (narrow).**
- **Every cycle-1 A/B item is resolved**, except that the B3 fix brings in a new error-statement problem.
- **A1 is stated with the binding status and nothing more.** It is deferred to the rule-2 process, as ordered.
- **New findings: A 0, B 1, C 7.**
- B-new-1 is a text-and-JSON correction. It needs no new production run; the numbers below come from the fixer's own
  check outputs.
- After the fix, the re-review can be limited to B-new-1. **This is 1-bot cycle 2, the warning level of §6.5;**
  cycle 3 would be the last before escalation.

## 1. Cycle-1 items: resolved or not (evidence per item)

| item | status | evidence |
|---|---|---|
| **A1** closure failure of both estimators | **deferred to rule 2, stated correctly** | See §3. |
| **B1** rules 1 and 2 over-read | **RESOLVED** | See below. |
| **B2** no-credit value missing | **RESOLVED** | See below. |
| **B3** R08 IS checked against one plain toy | **RESOLVED in substance; the error statement is wrong → B-new-1** | See below. |
| **B4** day-15 term under one reading | **RESOLVED** (with C-2) | See below. |
| **B5** planning width assumes an evaluable R07 | **RESOLVED** | See below. |
| **B6** causes over-stated | **RESOLVED** | See below. |
| **B7** O1–O4 called remediations | **RESOLVED** | See below. |
| **B8** `dev.pu1` "not requested" | **RESOLVED** (with C-3) | See below. |
| **B9** logs and times | **RESOLVED** | See below. |
| **ELI (A)** x labels, legends, R07 clipped | **RESOLVED** | See below. |
| **ELI (B)** notation, unexplained missing points | **RESOLVED** | See below. |

**B1: rules 1 and 2.**
- Rule 1 now reads "Not met now", with the status line of ADV point 1 updated to "reviewed" as ADV-A A5 allows
  (v2 l.74-76, §8.1).
- Thinning reads "redesign identified: the re-find variant … not submitted only if the user declines". This is
  verbatim ADV-A A3 (v2 l.79-83, l.164-168, §8.2).
- The occupancy model reads "no cause demonstrated; cause investigation running (report by 30 Nov) …; otherwise not
  submitted", as ADV-A A1 (v2 l.84-87, §8.3).
- v1's sentence "no redesign inside the frozen definition" is withdrawn (l.165-166).
- A grep of v2 for "pause condition", "unless ordered" and "identified" finds them only in the change table, or
  applied to the thinning redesign. The occupancy cause is never called identified (ADV-A A6).

**B2: no-credit value.**
- 485 events is in §0 and §6.3. I checked it: 4.0848×10⁷ × 1.14 / 96,000 = 485.07, and the JSON has
  `no_credit_value.events_zero_count_68` = 485.07.
- STR l.1177 says "485 events" [V, read].
- The mean 425.5 is N_trig/96,000.
- Both the FAIL reading and the not-submitted reading are given, with what each means for R08+ (§6.3).
- The development-sample bound 2,910 (JSON 2,910.42) is flagged and not chosen.
- With `dev.pu1`: 39,840 trials give 1,169 [V arithmetic].

**B3: importance sampling at R08.**
- The R08 row is now reported (l.225-226).
- A check with power at R08 now exists: 6.4×10⁸ plain toys on all 6,400 configurations.
- I confirmed the coverage: 6,400 rows, 6,400 unique (file, b) keys, 6,400 expected [V `liv_ischeck.json`].
- There are 45 passes, and plain/stored = 1.135 [V].
- The factor 12.6 is therefore excluded: about 500 passes would have been expected under it.
- The quoted error and its justification are wrong. See B-new-1.

**B4: two readings of the day-15 term.**
- Both readings are tabled (§6.1-6.2).
- Reading (ii) R09 = 5.25 is now in the JSON: `candidates.R09.occupancy_B2b_model.events` = 5.2536 [V].
- v2 states that reading (i) uses the held-out R06 and the 7 R07 counts to set the normalisation (l.315-317).
- The day-15 scale fit has residuals R04 −0.220, R05 −0.412, R06 +0.110, R07 +1.118 and weights 7.94 / 7.94 / 7.89 /
  3.71. These equal `b2_dev_closure.json → occupancy.day15_scale` [V].
- A possible third reading is not reported: C-2.

**B5: planning widths.**
- I recomputed √(0.13516² + 4·0.40547²) = 0.8221 and √(0.13516² + 5·0.40547²) = 0.9167. They equal
  `planning_cap_lastR06_*` (0.82212, 0.91667) [V].
- The s = 3 rows with and without credit are 0.833 / 1.468 (R08) and 0.927 / 1.818 (R09); they match the JSON [V].
- The R07-last-rung column (0.427 / 0.589) equals STR l.518 (0.43 / 0.59) [V, read].
- d_in = 2 with b̂ := 0 and σ_b := b₀ is the n = 1 rule of STR l.484-487 [V, read].

**B6: causes.**
- Thinning reads "Localised …; mechanism not isolated", and the reasons R2 and R1 are given (l.57, l.160).
- The occupancy model reads "O4 restates …; O3 … ≈ 1.8σ" (l.58, l.279-280).
- e^0.355 = 1.43 [V].
- The DAILY_NOTES correction line exists (DAILY_NOTES l.6) [V].
- LOG.md l.1011 is flagged for the orchestrator (§11.8). Correct: that file is not the fixer's to edit.

**B7: remediation labels.**
- §3.3 now labels R0 as bug search, R1 as control, and R2/R3 as remediation.
- §4.4 states in its heading that "no model remediation was attempted", with the reason.
- The self-check §10 is corrected, and the reason (the freeze and rule 2) is stated, not waived.

**B8: `dev.pu1`.**
- It is restated as a frozen MUST line being produced (§7, l.389-397), with the seal of ADV-A A2.
- The arithmetic holds: 4.375×10⁻⁴ × 39,840 = 17.4 counts, and 1/√17.4 = 0.24 > 0.135 [V].

**B9: logs and times.**
- `experiment_log.md` l.126-161 has DECISION / ALTERNATIVES / CONFIDENCE / FLAG blocks for: the occupancy freeze, the
  day-15 reading, the s_model rung set, R2/R3, [DT2] as a [D] (with "user informed"), `dev.pu1`, and the times [V].
- The notice that carries [DT2] exists: `notices/2026-11-24_1447_RESULT_…` says "Its validated range is R04–R06 at most
  ([DT2])" [V].
- The correction is appended to Casper's log, not rewritten (tail of `executor_casper_…`) [V].

**ELI (A): figures.** Checked visually:
- all three PNGs now have x labels ("Rung / crossing rung", "Rung");
- the rates legend is at the lower left, in empty space, with no overlap with data or tick labels;
- the N_eff legend is at the upper right, above all data (maximum ≈ 2×10⁴, legend at ≥ 10⁶);
- in the ln r figure both R07 points are inside the frame (thinning +1.47 with bars up to ≈ 1.85), drawn as open
  markers.
- `plots.py` has no `colorbar`, no `set_title`, and no numeric font sizes (grep).

**ELI (B): notation and captions.**
- The notation paragraph in §9 defines R0k, ⊗2S≥j and ⊗p>P.
- The captions explain the missing occupancy points at the p-rungs, the occupancy error bars and the no-credit segment.
- The N_eff order is now R05⊗p before R06⊗p.

## 2. The B3 importance-sampling check and DOR's "≈ 12 %" (asked by the orchestrator)

**DOR's 12 % is not reproduced: confirmed.** I computed 9 readings of the stored error at R08 from `isr[:, 3, 0..1]`
(`liv_ischeck.json → dor_12pct_readings`):

| reading | value |
|---|---|
| pooled toy-level (m2 − m1²)/n | 8.63 % |
| pooled naive √(Σm2/n)/Σm1 | 8.65 % |
| within-seed | 8.69 % |
| per-seed mean / √8 | 7.67–7.72 % |
| per-seed r.m.s. / √8 | 7.87–7.92 % |
| 1/√(total toy ESS = 195.2) | 7.16 % |

Every reading falls between 7.2 and 8.7 %. DOR's 12 % was an [E] in her log (l.9) with no script, and I cannot
reconstruct it. Ivar's "not reproduced" (v2 l.231-232) is correct.

**But DOR's concern, that the error is understated, is confirmed by Ivar's own fresh run, and by more than 12 %.**
- The fresh IS uses 10× the toys per configuration (2,000 against 200) on the same 6,400 configurations. Its
  toy-level error at R08 is **6.87 %**, not the ≈ 2.7 % that 8.63 %/√10 would give [V `rel_toy_fresh`].
- The estimated per-toy relative variance is therefore **×6.3 larger** with the larger sample: 0.0864² × 1.28×10⁶
  = 9.5×10³ against 0.0687² × 1.28×10⁷ = 6.0×10⁴ [V arithmetic].
- This is the signature of a weight distribution whose tail the 200-toy runs do not sample. The stored 8.6–8.7 % is a
  lower bound.
- With the fresh per-toy variance, the stored R08 value has a toy-level error of **≈ 22 % [E]** (√(6.0×10⁴/1.28×10⁶)).
  This is itself a lower bound if the tail is still under-sampled.
- At R07 the same ratio is ×1.95, so the stored R07 error is ≈ 5.7 % rather than 4.2 % [E].

**Configuration sampling is negligible, contrary to v2's framing.**
- v2 says the paired check "tests the IS toy estimate, not the configuration sampling, which the 8.7 % covers"
  (l.244-245). But the stored 8.70 % total error is almost all toy noise: the toy part alone is 8.64 % [V].
- The covariance of independent estimates across configurations, which estimates the variance of the true
  per-configuration probability, gives a configuration-level error of 0.9 % (stored × fresh), 1.6 % (fresh × plain) and
  0 (stored × plain, negative covariance) [V].
- The 45 plain passes fall in **45 different configurations**, one each [V], so no concentration is resolved.
- The paired check therefore covers essentially the whole MC error.

**Direction.** The unbiased plain estimate is above the IS estimate at every deep rung:

| rung | plain / stored IS | plain / fresh IS |
|---|---|---|
| R06 | 1.046 (2,699 passes, ±1.9 %; `is_check_stats.json` E_plain_mean/E_mean) | — |
| R07 | 1.080 | 1.028 |
| R08 | 1.135 | 1.097 |

- The paired pulls with toy-level errors are 1.9σ / 1.3σ at R07 and 0.8σ / 0.6σ at R08 [V].
- Each pull alone is insignificant, but the sign is the same at R06, R07 and R08, and the offset grows with depth.
- Heavy-tailed IS sums typically fall below their mean in a finite sample, so this pattern is what I would expect.
- The best reading of the evidence is that the stored IS value at R08 is low by about 3–13 %, with a ±15 % (plain)
  constraint on the truth.

**Consequence.**
- v2's "honest MC error ≈ 15 % … the larger of the 8.7 % statistical estimate and the ±15 % validated precision"
  (l.248-250) rests on an 8.7 % that the fixer's own data show to be about 2.5× too small.
- The ±15 % is the error of plain/truth, not of the stored value. The stored value sits at the low edge of the plain
  68 % interval (truth/stored ∈ [0.99, 1.28]).
- At R08 the MC part is therefore ≈ ±75 events on 347 (not ±52), and ≈ ±96 on 443 (not ±66).
- Reading (ii) at the plain central value would be 443 × 1.135 = **503 events, above the no-credit value 485**, where
  the frozen script censors the term. v2 does not say that the +1σ of reading (ii) already reaches the no-credit value.
- The frozen choice "IS primary" (10:56) is not in question, and nothing is to be replaced. The error statement is.

## 3. A1: stated with the binding status, nothing more [V]

- §0.1 (l.66-89) states:
  - the failure plainly: thinning (b) χ²/ndf 4,839/14, R06 beyond L + 2σ_tot; occupancy held-out pull 10.6σ;
  - the alarm consequence: "blocks B2 until rule 2 has run";
  - rule 1: "not met now", with the status line;
  - rule 2 per estimator, in the ADV-A A1/A3 wording;
  - "Who resolves A1: the orchestrator … This version states the routes; it does not close A1."
- It adds no closure claim, no reframing ("known limitation") and no remedy of its own. §8 repeats the same routes.
- The JSON flags agree with the text: `estimators.*.above_cap: true`, `both_estimators_above_cap: true` [V].
- Two wording points are C items: the truncated rule-2 quotation (C-1) and the missing mixed case (C-5).

## 4. Fresh pass: numbers between text, tables and JSON [V unless marked]

I checked the following against `pileup_term.json` / `b2_dev_closure.json`; all agree:

| quantity | values |
|---|---|
| §0 thinning ln r | +0.259 / +0.319 / +0.773 |
| s_model | 0.5058 / 0.5357 |
| occupancy s_model | 0.3548, trend 0.3740 |
| cap | 0.13516 |
| C(R04), C(R05) | 1.1839, 1.2068 |
| N_cfg | 1.880×10⁵ |
| N_eff | 5,142 / 4,056 / 6,861 / 228 / 4.11 |
| §6.2, every event entry | 5.6/7.0×10⁹; 1.3/1.7×10⁹; 1.13/1.44×10⁷; 5.5/7.0×10⁴; 347/443; 4.1/5.25; s = 3: 4.7/5.9×10⁹, 1.1/1.5×10⁹, 9.7×10⁶/1.24×10⁷, 4.7/6.0×10⁴, 301/384, 3.6/4.55 |
| §6.2, every width entry | all three columns |
| direct counts | 2,733,703 / 791,291 / 3,966 / 7; 2,345,475 at R04∧2S |
| thinning R08 | 3.1×10⁻⁵ (N_eff 4.1) |
| MC part on R08 | 347 × 0.149 = 51.7; 443 × 0.149 = 66.1 |
| s_f(R06⊗2S) | 0.344 = r.m.s.(0.355, 0.355, 0.322), the STR l.496-500 definition of s_f |
| CPU, cycle 1 | 3 × 1,063 s = 0.886 CPU-h (`time.txt` on maxwell) |

- The JFC alarm values in §10 (242–346) equal 3,392/14 and 4,839/14.
- **One inconsistency:**
  - v2 gives the R09 MC error as ≈ 21 % (§0, §4.2, §6.1, §8.8).
  - `pileup_term.json` carries `occupancy_day15.mc_rel_error_b3 = 0.149` on the R09 and R09x2S>=3 records too
    (`pileup_term.py` l.111-113), and v2 §4.2 says so.
  - The JSON has no key for the 15 % binomial error of the fit-probability fraction: √(0.988/47) = 0.145.
  - p3-a reads this file, so it would take 15 % at R09. This is part of B-new-1.

## 5. Findings

### Category A
None.

### Category B

**B-new-1. The R08/R09 model MC error is understated and its derivation is mis-stated (v2 §0 l.62, §4.2 items 1-3,
§6.1 l.320-321, §8.8, §11.7; `pileup_term.json → mc_rel_error_b3`).**

What is wrong (evidence in §2):
1. The "8.7 % statistical estimate" is about 99 % toy noise (8.64 % of 8.70 %) and is a lower bound. The fixer's own
   fresh IS (10× toys) shows a ×6.3 larger per-toy variance, which puts the stored R08 error at ≈ 22 % [E].
2. "This tests the IS toy estimate, not the configuration sampling, which the 8.7 % covers" is backwards. The
   configuration-sampling part is 0–1.6 % [E]; the paired check covers essentially the whole MC error.
3. "1.13 ± 0.15" is correct as an estimate of truth/stored. But quoting ±15 % symmetric about the stored value hides
   that the only unbiased estimate is +13 % above it. Plain exceeds IS with the same sign at R06 (+4.6 %), R07 (+8.0 %)
   and R08 (+13.5 %).
4. The R09 value in the JSON (0.149) differs from the text (21 %).

Fix (text and JSON only, no compute; the numbers are in `liv_ischeck.json` and can be recomputed from the fixer's
scratch files):
- (a) Quote the stored-IS toy-level error from the fresh run, ≈ 22 % [E] at R08 (≈ 5.7 % at R07). Call 8.7 % a lower
  bound, and drop the configuration-sampling sentence.
- (b) State the plain constraint as truth/stored = 1.13 ± 0.15 (fresh IS: 1.03), with the same-sign pattern at R06–R08.
- (c) Give the R08 MC error as ≈ 22 % [E], or as the asymmetric plain interval (+28 % / −1 %). Give R09 as
  √(0.22² + 0.145²) ≈ 26 % [E]. Update ±52 / ±66 events accordingly.
- (d) Say that within this error reading (ii) at R08 reaches the no-credit value 485 (443 × 1.135 = 503), where the
  frozen script censors the term.
- (e) In `pileup_term.json`, set the R08/R09 key to the corrected value, and either add a separate
  `fitprob_rel_error` (0.145) at R09 or put the R09 total in the key. Document it in SCHEMA.md.
- IS stays the primary estimator (frozen 10:56). Nothing is replaced.

### Category C

**C-1. Rule 2 is quoted truncated (v2 l.77-78).**
- STR l.2759-2760 ends: "… declares it 'not submitted' and its factor has no credit (a Q3 route)".
- For the MUST items B2-a/B2-b, "not submitted" is the exception to brief D4 that only the user grants (STR
  l.463-466; §4.12 table l.1873 "accepted under Q3").
- The user granted Q3 at Gate A (COM l.38), and the cap route is in the Q3 annex (STR l.3053). So no decision is
  missing.
- Quote the full sentence, and add "(Q3 granted at Gate A, COM l.38)" to the not-submitted reading of §6.3.

**C-2. A third reading of "the development model's R04–R07 inputs" (STR l.2741).**
- STR l.1145 defines the model's "inputs" as "densities, correlation factors" derived "using rungs R04–R05 only".
- The day-15 phrase can therefore mean: the same inputs derived using R04–R07, i.e. C(r) measured on real hits at
  R06/R07, with no fit to direct counts. Neither (i), which is a scale fitted to direct counts, nor (ii), which is
  implemented as C held at R05 (`pileup_term.py` l.114-121), is that.
- With the current C(R06)/C(R05) = 1.03 ± 0.18, it moves reading (ii) by ≈ +3 % (R08 ≈ 455). The p3-f 10× `occin`
  will give C(R06) to ±6 %.
- List it as reading (iii) for the orchestrator. Do not choose it.
- DOR B4's description of reading (ii) ("inputs extended to R07") also fits (iii) better than what was implemented;
  say which one is tabled.

**C-3. The seed wording for `dev.pu1` (v2 l.392, "disjoint seeds").**
- KET points 2, 5 and 10: the job seeds are disjoint, but ≈ 0.5 % of interaction seeds are shared [E, not yet
  measured]. This must be stated, not hidden.
- Write "job seeds disjoint; ≈ 0.5 % of interaction seeds shared [E, KET point 2]" where `dev.pu1` is described as
  the held-out sample.

**C-4. The B3 evidence is not durable.**
- The per-configuration inputs of `is_check.json` (3 × ≈ 120 kB `ischeck-*.npz`) exist only in maxwell's
  `/home/scratch/jdochoa/ivar-ischeck-*`, with no marker.
- Both the fixer's numbers and this review's depend on them.
- Copy them to `outputs/p3b/` (they are small) or to cajuela with a marker line, and cite the path in §4.2.

**C-5. The mixed route is missing from §6.3.** Thinning could end "not submitted" (the user declines the re-find)
while an occupancy redesign is submitted and FAILs at 4a. That is neither the "both FAIL" row nor the
"one estimator" row of the §4.12 table. State what the term becomes then (no estimator → no-credit value).

**C-6. Figures (physics presentation; the ELI format items are fixed).**
- (a) `b2_dev_rates`: the R08/R09 occupancy points carry the "hypothetical bookkeeping" measured-dev width as error
  bars. Visually this reads as a credited estimate band, which ADV point 8 (ii) warns against. Consider a distinct
  style (no bars, or hatched "no credit"); the caption disclaimer is there.
- (b) The y ranges are far from tight: rates 10⁻¹¹–10⁵ against data within 4×10⁻⁸–2×10²; N_eff 1–10⁷ against
  data ≤ 2.1×10⁴.

**C-7. The IS toy ESS asked for by DOR B3 is not quoted in the text.**
- It is per seed 11–43 toys of 160,000, and 195 in total [V `is_check_stats.json` `ess_toys`, `liv_ischeck.json`].
- Add it to §4.2 item 1. It is the number that makes the heavy tail concrete.

## 6. Checks with no finding (beyond §1, §4)

- **Coverage of the paired check:** the three jobs (`--first 0/2134/4268`, `--ntop 2134`, seeds 777100/1/2, `--all`)
  cover each of the 6,400 configurations exactly once, unranked, so there is no selection effect [V `time.txt`,
  `liv_ischeck.json`].
- **Plain and IS kernels** (`occ_model.py` l.277-380) [V, read]:
  - the plain pass fraction accumulates 1/ntoy, so passes = plain × 10⁵;
  - the IS weight is 1/mean_m Π_u[(1 − β) + β·1_win/G], with units of G = 0 categories drawn from g and given
    factor 1;
  - the mixture keeps full support.
- **Blinding:** `is_check.py`, `pileup_term.py` and `plots.py` read only `p3-b-occmod`, `p3-b-occin` and the p3b JSONs
  [V, read]. My script reads only `p3-b-occmod` and the fixer's scratch outputs.
- **Process:** the cycle-1 CPU (0.886 CPU-h) plus v1 (≈ 4.9) gives ≈ 5.8 of 15 CPU-h. The B3 jobs and the plot job
  have SLOTS lines (l.17, 19, 21, 22) and a RELEASED line.
- **Frozen texts quoted, not reworded.** Each quotation checked against STR is verbatim or a faithful truncation:
  - l.396 "after trying a redesign";
  - l.1145-1146 "using rungs R04–R05 only";
  - l.1177-1178 "485 events … no selection beyond R07 is then eligible ([SD8])";
  - l.1198-1200 [DT2];
  - l.1878 "both pile-up estimators FAIL";
  - l.2741.
  The only exception is C-1.
- **ADV point 8 "must not" list:** v2 launches nothing, writes no "not submitted" or "pause met" into PREREG_v2 or COM
  (§7, l.387-388), uses no "more likely high" credit, and makes no choice on development R06/R07.

My own CPU: 11 s on maxwell (1 process, nice 19). The slot is released (SLOTS.md l.24-25).
