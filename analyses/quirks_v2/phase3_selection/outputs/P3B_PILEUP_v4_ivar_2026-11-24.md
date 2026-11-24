# P3B_PILEUP v4 — Phase 3, work package p3-b: B2 pile-up (repaired thinning, occupancy model, day-15 pile-up term)

**Version 4**, fixer Ivar (Opus), 2026-11-24, after review cycle 3 of the 1-bot review. It is v3
(`outputs/P3B_PILEUP_v3_ivar_2026-11-24.md`, unchanged on disk) with the text and JSON fixes asked by
`review/critical/P3B_CRITICAL_REVIEW_v3_oddvar_2026-11-24_15-38.md` ("ODD"): B-new-2 and the text/JSON C items. The
v3 → v4 change table below lists every changed sentence verbatim. v3 was v2
(`outputs/P3B_PILEUP_v2_ivar_2026-11-24.md`, unchanged on disk) with the fixes asked by the cycle-2 review
`review/critical/P3B_CRITICAL_REVIEW_v2_liv_2026-11-24_15-24.md` ("LIV", with `liv_ischeck.py` / `.json`); the change
table v2 → v3 follows, then v2's own change table v1 → v2 (kept as history, with its superseded values marked).
v2 was based on v1
(`outputs/P3B_PILEUP_casper_2026-11-24.md`, executor Casper, session 10:19 to ≈ 14:20 -0500, corrected time; v1 is
unchanged on disk). The findings come from `review/critical/P3B_CRITICAL_REVIEW_dorte_2026-11-24_14-22.md` ("DOR") and
`review/validation/P3B_PLOT_VALIDATION_elias_2026-11-24_14-22.md` ("ELI"). The binding wording comes from
`review/advisor/ADVISOR_B2CAP_freja_2026-11-24_14-23.md` with Addendum 1 of 14:46 ("ADV", "ADV-A"). Fixer session log:
`logs/fixer_ivar_2026-11-24_14-48.md`. Code `src/p3b/`; results `outputs/p3b/` (schema `SCHEMA.md`); figures
`outputs/figures/b2_dev_*.{pdf,png}` (regenerated). **Blinding:** no signal sample was opened and no signal quantity was formed, in v1
or in this cycle.

Tags: [V] verified (file, campaign or command cited), [E] estimate, [U] transcribed, not checked.

## Changes from v3 (cycle 3), sentence by sentence (ODD B-new-2 and C items; no number, flag or route changed beyond these)

What changed and why:
- **B-new-2:** the frozen projection has no threshold at 485. It takes min(term, (N_trig/96,000)·Exp(1)) in every pseudo-experiment
  (mean 426, 68 % value 485; `strategy_budget.py` l.585-587, l.678; STR l.953-954, l.1586-1588). Every v3 sentence
  that said the term is "censored at 485" or "carries ≥ 485 events" is replaced. ODD's toy numbers are quoted as his [E].
- **C items:** C-1 (1.13 ± 0.17, interval [0.97, 1.30], +30 % / −3 %); C-2 (22 % is a firm lower bound, and the top-1 % and
  ESS figures are toy noise); C-3 (the R06/R07 pulls are flagged as computed with lower-bound errors); C-4 (the key is
  added to the reading (ii) record, the 2S transfer is tagged, and the absent MC term in s_tot is stated); C-5 (states
  that `pileup_term.py` was not rerun); C-6 (§11 numbering).
- **JSON:** `pileup_term.json` gains `occupancy_B2b_model.mc_rel_error_c2` on R08, R09, R08x2S>=3 and R09x2S>=3.
  Key diff: 4 added, 0 changed, 0 removed [V]. `is_check_c2.json` is unchanged [V]. SCHEMA.md l.37-38 is corrected in
  place and its cycle-3 section is appended.
- **Not done:** no jobs and no git. `pileup_term.py` and `plots.py` were not rerun.

**Numbers changed in v4 (propagation):**
- 1.13 ± 0.15 → 1.13 ± 0.17: rows 1, 4, 5, 9, 17, 23 (row 22 adds the value). Rows 1 and 4 are history rows, annotated rather than overwritten.
- [0.99, 1.28] → [0.97, 1.30]: row 13.
- +28 % / −1 % → +30 % / −3 %: rows 2, 9, 14.
- R07 pull 1.9σ → 1.4σ, with the 1.9σ kept as the stored-run reading: row 10.
- "≥ 485 events" / "censored at 485" → the predictive draw: rows 3, 5, 15, 17, 18, 19, 20, 21, 22.
- New numbers, all ODD's [E] or [V]: 0.169; [0.966, 1.330]; 56.5–67.0 %; 241 / 256 / 270 / 286 events; ≈ +6 %; ≈ 12 %;
  pulls 0.8 / 1.4 / 1.5 / 2.4σ; 51.1 / 1.4 / 31.6 %; ≈ 13 expected passes; correlations 0.014 / 0.023.
- No event number, ln r, s_model, N_eff, width, flag or route changed.

| # | location | finding | v3 text (verbatim) | v4 text (verbatim) |
|---|---|---|---|---|
| 0 | title and version paragraph | — | "# P3B_PILEUP v3"; "**Version 3** … review cycle 2 … It is v2" | "# P3B_PILEUP v4"; "**Version 4** … after review cycle 3 … It is v3 (…) with the text and JSON fixes asked by … ODD … v3 was v2" |
| 1 | v2→v3 table, B-new-1 (b) | ODD C-1 | truth/stored = 1.13 ± 0.15 (fresh IS 1.03). | truth/stored = 1.13 ± 0.15 (fresh IS 1.03; *corrected in v4 to 1.13 ± 0.17*). |
| 2 | v2→v3 table, B-new-1 (c) | ODD C-1 | or the plain interval +28 % / −1 %; R09 | or the plain interval +28 % / −1 % (*+30 % / −3 % in v4*); R09 |
| 3 | v2→v3 table, B-new-1 (d) | ODD B-new-2 | where the frozen script censors the term; reading (i) gives 394. \| | where the frozen script censors the term; reading (i) gives 394. *Corrected in v4: the frozen script has no threshold at 485; see the v4 change table (B-new-2).* \| |
| 4 | v1→v2 table, B3 | ODD C-1 | plain/IS = 1.13 ± 0.15: **IS confirmed to ±15 %**. | plain/IS = 1.13 ± 0.15 (*± 0.17 in v4*): **IS confirmed to ±15 %**. |
| 5 | §0 table, model MC error row | ODD B-new-2, C-1, C-2 | \| model MC error at R08 (both readings scale with it) \| **≈ 22 %** (v1: 7 %, v2: 15 %; the stored-run 8.7 % is a lower bound); R09 ≈ 26 % with the fit-probability fraction. Plain/IS = 1.13 ± 0.15 at R08, with the same sign at R06–R08 (+4.6 / +8.0 / +13.5 %): a possible IS bias. Reading (ii) at the plain value is 503 events, above the no-credit value 485. \| | \| model MC error at R08 (both readings scale with it) \| **≈ 22 %, a lower bound** (v1: 7 %, v2: 15 %; the stored-run 8.7 % is a lower bound too); R09 ≈ 26 % with the fit-probability fraction. Plain/IS = 1.13 ± 0.17 at R08 (the only unbiased constraint), with the same sign at R06–R08 (+4.6 / +8.0 / +13.5 %): a possible IS bias. Reading (ii) at the plain value is 503 events. The frozen projection takes min(term, (N_trig/96,000)·Exp(1)) in every pseudo-experiment (mean 426, 68 % value 485; no threshold at 485): this binds in ≈ 57–67 % of pseudo-experiments under both readings, and the +13 % shift moves the censored mean by ≈ +6 % [E, ODD toy]. \| |
| 6 | §4.2 item 1, 22 % bullet | ODD C-2 | This is itself a lower bound if the tail is still under-sampled at 2,000 toys. | This is itself a **lower bound**, not only possibly: the fresh IS also misses the tail. The 64 configurations with the largest stored R08 values hold 51.1 % of the stored sum but 1.4 % of the fresh sum and 0 of the 45 plain passes; the fresh top 64 hold 31.6 % of the fresh sum and 1 plain pass where ≈ 13 would be expected [ODD C-2, his V]. |
| 7 | §4.2 item 1, heavy-tail bullet | ODD C-2 | The effective number of configurations is 129 of 6,400. | The effective number of configurations is 129 of 6,400. These two figures describe the toy noise of the stored run, not the configurations: at R08 the per-configuration IS values are noise (correlations stored–fresh 0.014, fresh–plain 0.023 [LIV]). |
| 8 | §4.2 item 1, configuration-sampling bullet | ODD C-2 | the stored 8.70 % is ≈ 99 % toy noise (8.64 %). | the stored 8.70 % is ≈ 99 % toy noise (8.64 %). Those covariances come from the same noisy per-configuration estimates, so this figure has little power [ODD C-2]. |
| 9 | §4.2 item 2, R08 bullet | ODD C-1 | **truth/stored = 1.13 ± 0.15** (plain / stored IS, Poisson error of the 45), i.e. the plain 68 % interval relative to the stored value is +28 % / −1 %. | **truth/stored = 1.13 ± 0.17** (plain / stored IS; the relative Poisson error 1/√45 = 0.149 of the plain value gives ±1.135 × 0.149 = ±0.169; v3's ± 0.15 applied it as an absolute error [ODD C-1]), i.e. the plain 68 % interval relative to the stored value is [0.97, 1.30], +30 % / −3 % (Garwood 68 %: [0.966, 1.330] [ODD]). |
| 10 | §4.2 item 2, R07 bullet | ODD C-3 | plain / stored IS = 1.080 (1.9σ with the toy-level errors); plain / fresh IS = 1.028 (1.3σ). | plain / stored IS = 1.080: 1.4σ with the 5.7 % stored error of item 1 (1.9σ with the 4.1 % stored-run error); both are computed with errors that are themselves lower bounds [ODD C-3]. Plain / fresh IS = 1.028 (1.3σ, with the fresh toy-level error, also a lower bound). |
| 11 | §4.2 item 2, R06 bullet | ODD C-3 | plain / stored IS = 1.046 ± 0.019. | plain / stored IS = 1.046 ± 0.019: 2.4σ with the plain error alone, 1.5σ with the stored IS error of 2.4 % added (a lower bound too) [ODD C-3]. |
| 12 | §4.2 item 3, pulls | ODD C-3 | Each pull alone is below 2σ. But the pattern | The single pulls are ≈ 0.8σ (R08), 1.4σ (R07) and 1.5σ (R06; 2.4σ with the plain error alone), each computed with errors that are themselves lower bounds. The pattern |
| 13 | §4.2 item 3, interval | ODD C-1, C-2 | with the truth constrained to truth/stored ∈ [0.99, 1.28] (plain, 68 %). | with the truth constrained to truth/stored ∈ [0.97, 1.30] (plain, 68 %). The plain check is the only unbiased constraint on the stored value. |
| 14 | §4.2 item 3, quoted error | ODD C-1, C-2 | is **≈ 22 % [E]**: the symmetric toy-level error, or equivalently the asymmetric plain interval +28 % / −1 %. | is **≈ 22 % [E], a lower bound**: the symmetric toy-level error of the fresh run. From the plain check alone the 68 % interval is +30 % / −3 %; the two statements are not equivalent [ODD C-1]. |
| 15 | §4.2 item 3, consequence | ODD B-new-2 | - Consequence: **reading (ii) at the plain central value is 443 × 1.135 = 503 events, above the no-credit value 485, where the frozen script censors the term** (reading (i): 347 × 1.135 = 394). | - Consequence: reading (ii) at the plain central value is 443 × 1.135 = 503 events (reading (i): 347 × 1.135 = 394). **The frozen projection has no threshold at 485** (corrected in v4, ODD B-new-2). In every pseudo-experiment it takes min(term, (N_trig/96,000)·Exp(1)), a fresh draw with mean 426 and 68 % value 485: `strategy_budget.py` l.585-587 (`x = min(x, capv if capv >= 0 else -capv * rnd.expovariate(1.0))`) with l.678 (`PU_CAP = -NTRIG / 96000`); STR l.1586-1588 ("drawn like every other zero-count term: N_trig·λ/96,000 with λ ~ Gamma(1) in each pseudo-experiment (68 % value 485 events)"); STR l.953-954 ("censored at the predictive draw of its no-credit bound, 426 × Exp(1)") [V: read]. - ODD's toy [E: his, 4×10⁵ draws, width 0.822; widths 0.885 or 0.427 change the numbers by ≤ 2 %] covers R08 medians 347 (i), 394 (i, plain), 443 (ii) and 503 (ii, plain). The censoring binds in 56.5 / 60.0 / 63.5 / 67.0 % of the pseudo-experiments, and the mean contribution is 241 / 256 / 270 / 286 events, against 425.5 without credit. - So the censoring already binds in most pseudo-experiments at the stored values, under both readings. The +13 % plain shift moves the censored mean by only ≈ +6 %, and the gap between readings (i) and (ii) is ≈ 12 % in the projection. - The R08 term is at the no-credit scale with or without a credit. |
| 16 | §4.2 item 3, JSON sentence | ODD C-4 (a)-(c), C-5 | as is the v1 key `mc_rel_error` (0.072). | as is the v1 key `mc_rel_error` (0.072). - In v4 the same key is also on the reading (ii) records (`occupancy_B2b_model.mc_rel_error_c2`). - `pileup_term.py` was edited to write these keys on a rerun but has **not been rerun**: there is no numpy on einstein and cycles 2–3 allowed no jobs. The keys come from `is_check_c2.py --patch` [ODD C-5]. - The R08 ∧ N_2S2 ≥ 3 and R09 ∧ N_2S2 ≥ 3 values are the R08 value transferred, because the paired check was not run with the 2S requirement [E, ODD C-4 (b)]. - The frozen s_tot (STR §4.0 point 7) has no MC term. Whether p3-a adds the MC error to the projection width is not fixed here [ODD C-4 (c)]. |
| 17 | §6.1, plain-value sentence | ODD B-new-2, C-1 | The plain check points upward (truth/stored 1.13 ± 0.15): at the plain central value reading (ii) is **503 events, above the no-credit value 485** (§6.3), and reading (i) is 394. | The plain check points upward (truth/stored 1.13 ± 0.17): at the plain central value reading (ii) is 503 events and reading (i) 394. In the frozen projection both are censored in every pseudo-experiment by min(term, (N_trig/96,000)·Exp(1)) (mean 426, 68 % value 485; §4.2, §6.3). For these medians this binds in ≈ 57–67 % of pseudo-experiments [E, ODD toy]. |
| 18 | §6.3, not-submitted reading | ODD B-new-2 | The term is labelled "no credit" and enters at its no-credit value. | The term is labelled "no credit" and enters as the predictive draw of its no-credit bound, N_trig·λ/96,000 with λ ~ Gamma(1) in each pseudo-experiment (mean 426, 68 % value 485; STR l.1586-1588, `strategy_budget.py` l.585-587, l.678). |
| 19 | §6.3, mixed route | ODD B-new-2 | so the term is at its no-credit value (485 beyond R07). | so beyond R07 the term enters as that predictive draw (mean 426, 68 % value 485). |
| 20 | §6.3, consequence (no credit) | ODD B-new-2 | under either no-credit reading every R08+ candidate carries **≥ 485 events** of pile-up, against | under either no-credit reading the pile-up term of every R08+ candidate **enters as the predictive draw N_trig·λ/96,000, λ ~ Gamma(1) (mean 426, 68 % value 485)**, against |
| 21 | §6.3, consequence (with credit) | ODD B-new-2 | Even with a credit, reading (ii) reaches the no-credit value within its MC error: at the plain central value it is 503 > 485, where the frozen script censors the term (§4.2). | Even with a credit, the frozen projection takes min(term, (N_trig/96,000)·Exp(1)) in every pseudo-experiment. The credited R08 medians (347–503 events, plain-shifted values included) are therefore censored in ≈ 57–67 % of pseudo-experiments and contribute 241–286 events on average, against 425.5 without credit [E, ODD toy; §4.2]. The R08 term is at the no-credit scale with or without a credit. |
| 22 | §8 item 8 | ODD B-new-2, C-1 | 8. **B3 / B-new-1** (§4.2): the quoted MC error is ≈ 22 % at R08 and ≈ 26 % at R09 [E]. Plain lies above IS with the same sign at R06–R08 (a possible IS bias, ≈ 3–13 % at R08), and reading (ii) at the plain value (503) is above the no-credit value 485. Nothing to decide now; this is for the day-15 reading. | 8. **B3 / B-new-1** (§4.2): the quoted MC error is ≈ 22 % at R08 and ≈ 26 % at R09 [E], both lower bounds. Plain lies above IS with the same sign at R06–R08 (a possible IS bias, ≈ 3–13 % at R08; truth/stored 1.13 ± 0.17), and reading (ii) at the plain value is 503 events. The frozen projection censors the term in every pseudo-experiment by min(term, (N_trig/96,000)·Exp(1)) (mean 426, 68 % value 485), which binds in most pseudo-experiments under both readings (§4.2). Nothing to decide now; this is for the day-15 reading. |
| 23 | §11 item 7 | ODD C-1, C-2 | 7. B3 / B-new-1 (§4.2): the MC error at R08 is ≈ 22 % (R09 ≈ 26 %) [E], with a possible downward IS bias of ≈ 3–13 % at R08 (plain truth/stored 1.13 ± 0.15). | 7. B3 / B-new-1 (§4.2): the MC error at R08 is ≈ 22 % (R09 ≈ 26 %) [E], both lower bounds, with a possible downward IS bias of ≈ 3–13 % at R08 (plain truth/stored 1.13 ± 0.17). |
| 24 | §11 numbering, C-6 item | ODD C-6 | 9. LIV C-6, not applied in cycle 2 (it needs a plot job and none is allowed): | 8. LIV C-6, not applied in cycles 2–3 (it needs a plot job and none is allowed): |
| 25 | §11 numbering, DAILY_NOTES item | ODD C-6, C-5 | 8. The DAILY_NOTES line of 14:20 | 9. The DAILY_NOTES line of 14:20 |
| 26 | §11, new item 10 | ODD C-5 | — | 10. ODD C-5: `pileup_term.py` (edited in cycles 2–3 to write `mc_rel_error_c2`) has not been rerun; rerun it once at the next worker job and diff `pileup_term.json` (expected: no change). |

## Changes from v2 (cycle 2), finding by finding

| finding | what v2 said | what v3 does | where |
|---|---|---|---|
| **B-new-1 (a)** error of the stored IS at R08 | "8.7 % statistical estimate"; the paired check "tests the IS toy estimate, not the configuration sampling, which the 8.7 % covers" | 8.7 % is a **lower bound** (≈ 99 % toy noise: 8.64 % of 8.70 %). The fresh IS run with 10× the toys on the same configurations has a per-toy variance ×6.3 larger, so the stored R08 value has a toy-level error of **≈ 22 % [E]** (R07 ≈ 5.7 %). Configuration sampling is 0–1.6 % [E, LIV], and the paired check covers essentially the whole MC error. v2's configuration-sampling sentence is withdrawn. | §4.2 |
| **B-new-1 (b)** direction | "confirmed within ±15 %", symmetric | truth/stored = 1.13 ± 0.15 (fresh IS 1.03; *corrected in v4 to 1.13 ± 0.17*). Plain lies above IS with the same sign at R06 / R07 / R08 (+4.6 / +8.0 / +13.5 %), growing with depth. This is stated as a **possible IS bias, not noise**. | §4.2 |
| **B-new-1 (c)** quoted MC error | R08 ≈ 15 %, R09 ≈ 21 %; MC part ±52 / ±66 events | R08 **≈ 22 % [E]**, or the plain interval +28 % / −1 % (*+30 % / −3 % in v4*); R09 **≈ 26 % [E]** (with the fit-probability fraction's 14.5 %). The MC part is ±75 events on 347 and ±96 on 443. | §0, §4.2, §6.1, §8, §11 |
| **B-new-1 (d)** no-credit crossing | not stated | reading (ii) at the plain central value is 443 × 1.135 = **503 events, above the no-credit value 485**, where the frozen script censors the term; reading (i) gives 394. *Corrected in v4: the frozen script has no threshold at 485; see the v4 change table (B-new-2).* | §0, §4.2, §6.1, §6.3 |
| **B-new-1 (e)** JSON vs text | JSON R09 0.149 against text 21 % | **one new key** `occupancy_day15.mc_rel_error_c2` (R08 and R08∧2S 0.217; R09 and R09∧2S 0.261), from `src/p3b/is_check_c2.py` (standard library, no new Monte Carlo) → `outputs/p3b/is_check_c2.json`. The cycle-1 key `mc_rel_error_b3` (0.149) is kept unchanged and documented as superseded in SCHEMA.md. Key diff of `pileup_term.json`: 4 added, 0 changed, 0 removed [V]. | JSON, SCHEMA |
| C-1 rule-2 quote | truncated | full sentence, "… and its factor has no credit (a Q3 route)", plus "(Q3 granted at Gate A, COM l.38)" on the not-submitted reading | §0.1, §6.3 |
| C-2 third reading | two readings | reading (iii) listed (inputs derived using R04–R07: C(r) measured on real hits, no fit to direct counts; ≈ +3 % on (ii), R08 ≈ 457 [E]); not chosen; it is said which reading is tabled | §6.1 |
| C-3 `dev.pu1` seeds | "disjoint seeds" | "job seeds disjoint; ≈ 0.5 % interaction-seed reuse, ESTIMATE, exact count pending" (KET points 2, 5, 7) | §7 |
| C-4 durable inputs | only on maxwell scratch | copied to `outputs/p3b/is_check_inputs/ischeck-{0,1,2}.npz` (3 × 122 kB; sha256 identical to the scratch originals), with sha256 and regeneration command in SCHEMA.md | §4.2, SCHEMA |
| C-5 mixed route | missing | stated and flagged | §6.3 |
| C-6 figure style / y ranges | — | **not applied**: it needs a plot job and cycle 2 allows none. The caption disclaimer stays, and the item is carried to the next plot run. | §11 |
| C-7 toy ESS | not quoted | IS toy ESS at R08: 11–43 per seed of 160,000 toys, 195 in total | §4.2 |

**Numbers changed in v3 (propagation):**
- Updated 7 instances across 1 file (this artifact): the R08 MC error ≈ 15 % → ≈ 22 %, the R09 MC error ≈ 21 % → ≈ 26 %, and the MC parts ±52 → ±75 and ±66 → ±96 events. The locations are the v1 → v2 change-table B3 row and its "Numbers changed" line (both marked superseded), §0, §4.2, §6.1, §8.8 and §11.7.
- `pileup_term.json` gains one key, `mc_rel_error_c2`, and no existing key changed. SCHEMA.md and `experiment_log.md` record the correction (append-only).
- No event number, ln r, s_model, N_eff or width changed. New numbers: 503 / 394 (readings at the plain value), 457 [E] (reading (iii)), and the toy ESS values.

## Changes from v1, finding by finding

| finding | what v1 said | what v2 does | where |
|---|---|---|---|
| **A1** closure failure of both estimators (DOR) | reported honestly, but closed with "pause condition met" | states the failure plainly with the rule-2 status of ADV / ADV-A. **A1 is resolved by the rule-2 process, which the orchestrator owns; the fixer does not resolve it.** §0.1 gives the closing statement of which estimator takes which route. | §0.1, §8 |
| **B1** rules 1 and 2 over-read | "rule-1 pause condition met"; "not submitted … unless ordered"; "no redesign inside the frozen definition is available" | rule 1: **not met now** (status "PRELIMINARY, reviewed: both above the cap on development; rule 2 running"). Rule 2 as written: thinning "redesign identified: the re-find variant (≈ 1,200 CPU-h, waits for the user at the pause); not submitted only if the user declines". Occupancy "no cause demonstrated; cause investigation running (report by 30 Nov); one redesign only if a cause is found; otherwise not submitted". The internal contradiction (§3.3 vs §8 (a)) is removed. | §0, §3.3, §4.4, §8 |
| **B2** no-credit value missing | "no credit", no number | **485 events** [V: N_trig·1.14/96,000 = 4.0848×10⁷ × 1.14 / 96,000 = 485.07; STR l.1018 "485 events at 68 %", l.1175-1178 "N_trig × 1.14/96,000 = 485 events"; `pileup_term.json` → `no_credit_value`]. The FAIL reading and the not-submitted reading, with their consequences for R08+, are given, plus the day-15 sample-size reading (2,910 at 16,000 development trials) as a flag. | §6.3 |
| **B3** R08 rests on IS checked against one plain toy | "model MC error at R08 7 %" | IS error re-estimated (within-seed 8.7 %; weight concentration: top 1 % of the configurations carry 51 %). A paired plain-toy check with 6.4×10⁸ toys on the same 6,400 configurations gives 45 R08 passes, plain/IS = 1.13 ± 0.15 (*± 0.17 in v4*): **IS confirmed to ±15 %**. The single-toy factor 12.6 (R08 ≈ 4,400 events) is excluded. The quoted MC error at R08 becomes **≈ 15 % [E]** (R09 ≈ 21 % with the binomial error of the fit-probability fraction) in place of 7 %. *Superseded in v3: ≈ 22 % (R09 ≈ 26 %); see the v3 change table.* | §4.2, §6 |
| **B4** day-15 term under one reading | reading (i) only (one scale on R04–R07) | both readings tabled: (i) R08 347 / R09 4.1 events; (ii) the B2-b model with its R04–R05 normalisation, R08 443 / R09 5.25 (R09 newly computed). Both are **only the rule-1 projection input, "no credit"**. Reading (i) uses the held-out R06 for its normalisation; this is now stated. Not chosen: flagged for the orchestrator. | §6.1-6.2 |
| **B5** planning width assumes an R07 test rung that §3.4 says is not evaluable | planning (cap) R08 0.427, R09 0.589 | the widths follow from §3.4's evaluability under both direct rates: development rate → R06 is the last width-test rung → R08 **0.822**, R09 **0.917** (DOR's "0.83" is the same formula, rounded high); v1's rate → R07 → 0.427 / 0.589. Both columns are kept. | §6.2 |
| **B6** causes over-stated | "cause identified for both" | thinning: "localised to candidate-level thinning versus re-finding (7σ at R06 on the same trials); mechanism not isolated; R2 failed its sanity check". Occupancy: "O4 restates the closure failure; O3 localises the problem outside the occupancy arithmetic at ≈ 1.8σ (31 real R06 planes); no cause demonstrated". The occupancy cause is never called "identified". | §0, §3.3, §4.4 |
| **B7** O1–O4 called remediations | "≥ 3 remediation attempts per failing estimator" | relabelled: thinning R0 = bug search, R1 = control (it is the re-find redesign run on 400 trials), R2/R3 = remediation attempts. Occupancy O1–O4 = variants and diagnostics. **No occupancy model remediation was attempted**: under the frozen rules nothing may be chosen after seeing R06, and rule 2 places any redesign at decision point 2, after a cause investigation (ADV-A A1). Self-check corrected. | §3.3, §4.4, §10 |
| **B8** `dev.pu1` "not requested" | waived by the executor | a frozen MUST development sample (STR l.2105, ≈ 5,960 events, 100 CPU-h), **being produced now** (ADV-A A4; p3-e defined and tested it, the orchestrator launches it). Its R06-and-deeper direct counts and crossing rungs stay sealed (ADV-A A2). It does not make development R07 evaluable: 7 → ≈ 17 counts [V arithmetic], σ ≈ 0.24 > 0.135. | §7 |
| **B9** logs and times | one experiment-log entry; header "14:30" | DECISION blocks (occupancy freeze, day-15 reading, s_model rung set, R2/R3, `dev.pu1`) and **[DT2] as a [D]** appended to `experiment_log.md`. **Time correction:** v1's header end "14:30" was not read from the clock: the v1 file mtime is 14:20:23 and commit f881aa3 is at 14:21:04 -0500 [V]. The session ended ≈ 14:20. The v1 session-log "13:30" N_eff line (R08 "one passing subset") does not match the final data (4). Correction notes were appended to the executor's session log and to the experiment log; v1 was not rewritten. | header, `experiment_log.md`, Casper's log |
| ELI A (3 figures) | no x-axis labels; legends on the data (rates, neff); R07 clipped (lnr) | x labels; legends moved to empty regions; the ln r frame is widened so that R07 and every error bar are inside it; open markers mark the not-evaluable comparisons; error bars on both occupancy readings; the no-credit value is drawn. Regenerated on maxwell (1 job). | §9 |
| ELI B (captions, notation) | ⊗, 2S≥n, p undefined; missing squares / bars unexplained | the notation is defined in every caption; missing points are explained. | §9 |
| linter glob | `lint_plots.py` scans `*/src/*.py` only | **not edited**: it is `tools/jfc/src/conventions/lint_plots.py` (the `conventions` symlink), which is read-only. It was run on all 20 `src/p3b/*.py` files through its own `lint_file()`: no violations. Flagged for the orchestrator. | §10 |
| C1 | 2S credit from in-sample rungs | column labelled "hypothetical bookkeeping"; s_f from R06⊗2S only = 0.344 [V] | §6.2 |
| C2 | v2 and C1 slopes in two sign conventions | C1 converted to ln(P/N) | §5 |
| C3 | — | [L15] standing limitation added | §11 |
| C4 | — | requirement carried to the ADV-A A3 N_eff measurement (several draws per trial, hit sets stored) | §3.3, §8 |
| C5 | "reproduces the direct counts" | R05 −0.069 ± 0.035 stated as 2.0σ | §0, §3.3 |
| C6 | — | done with the ELI A items | §9 |

**Numbers changed in v2:** only the model MC error at R08 (and so R09), 7 % → **≈ 15 %** (R09 ≈ 21 %) [E]. Updated 2 instances of the old value across 1 file: v1 §4.2 "Model MC error at R08 7 %" and v1 §6 "≤ 7.3 % at every candidate", both replaced in v2 §4.2 / §6.1. `pileup_term.json` gains `mc_rel_error_b3` = 0.149; the v1 key `mc_rel_error` (0.072, the seed spread) is unchanged and documented in SCHEMA.md. No event number of §6 changed (*the 15 % / 21 % are superseded in v3 by ≈ 22 % / ≈ 26 %*). Neighbourhood check of every table number against the JSONs: one rounding fixed (thinning R05⊗p>0.01 rate 0.0139 → 0.0140, JSON 0.01397; 1 instance). No number of v1's closure (ln r, σ_tot, s_model, N_eff, N_cfg, C(r)) changed.
New numbers (no v1 counterpart): no-credit 485 / 2,910; reading (ii) R09 5.25 (and 4.55 at s = 3); widths with R06 as
the last test rung; s_f(R06⊗2S) 0.344; the IS diagnostics of §4.2.

## 0. Summary (the numbers decision point 2 reads)

**Role of everything below: development** (STR §4.17 rows 1–2, C1 ρ = 1 and ρ = 2 samples). No B2-a/B2-b *verdict* is
given here; the verdicts are read at 4a on the independent 96,000-trial test sample. What this work package fixes
before the freeze is the s_model of each estimator against its cap, N_eff, crossing-rung evaluability, and the day-15
pile-up term.

| quantity | value | tag / source |
|---|---|---|
| repaired thinning (B2-a), development ln r = ln(P/N) at R04 / R05 / R06 | +0.259 / +0.319 / +0.773 (σ_tot 0.014 / 0.016 / 0.020); R07 +1.47 (7 direct counts, not evaluable) | [V] `b2_dev_closure.json` → thinning.closure; DOR §2.1 |
| thinning development s_model (r.m.s. over the evaluable cumulative rungs; with crossing rungs) | **0.506** (0.536); every other reading 0.234–0.291, all above the cap | [V]; DOR §1 (2) |
| occupancy model (B2-b): in-sample ln r R04 / R05; **held-out R06** | +0.006 / −0.166; **+0.355 ± 0.034** (R07: +1.36, not evaluable) | [V] → occupancy |
| occupancy development s_model = max(\|ln r(R06)\|, in-sample r.m.s. 0.118) | **0.355** (trend variant 0.374; all variants 0.32–0.52) | [V]; DOR §1 (2) |
| cap ln 1.5/3 | 0.135 | STR §4.0 point 4 (c) |
| **cap status** | **PRELIMINARY, reviewed: both above the cap on development; rule 2 running** | [V] `pileup_term.json` → `both_estimators_above_cap: true`; ADV point 1, ADV-A A5 |
| thinning: localisation of the excess (control R1) | the thinned ρ = 2 pool, re-found by the frozen ρ = 1 finder, agrees with the direct counts within 1.0σ / 2.0σ / 0.5σ (ln −0.032 ± 0.032 / −0.069 ± 0.035 / +0.048 ± 0.104); the estimator exceeds the re-found count on the SAME trials by +0.306 ± 0.009 / +0.399 ± 0.011 / +0.741 ± 0.104 (7σ at R06). **Localised, mechanism not isolated.** | [V] `b2a_refind_control.json`; DOR §1 (1a) |
| occupancy: cause | **no cause demonstrated**; O3 localises the problem outside the occupancy arithmetic at ≈ 1.8σ only (C(R06)/C(R05) = 1.03 ± 0.18 against e^0.355 = 1.43); cause investigation running (report by 30 Nov) | DOR §1 (1b); ADV-A A1 |
| N_eff of thinning (1,000 ρ = 2 events) R04 / R05 / R06 / R07 / R08 | 5,142 / 4,056 / 6,861 / 228 / 4.1 | [V] |
| [DT2] | thinning has no evaluable rung beyond R06 → validated range **R04–R06**, logged as a [D] (`experiment_log.md`), user informed (RESULT notice 2026-11-24 14:47) | [V] §3.4 |
| day-15 pile-up term at N_trig = 4.0848×10⁷, **rule-1 projection input only, no credit**, two readings | (i) one scale on R04–R07: R08 347, R09 4.1 events; (ii) B2-b, R04–R05 normalisation: R08 443, R09 5.25 | [V] `pileup_term.json`; §6 |
| model MC error at R08 (both readings scale with it) | **≈ 22 %, a lower bound** (v1: 7 %, v2: 15 %; the stored-run 8.7 % is a lower bound too); R09 ≈ 26 % with the fit-probability fraction. Plain/IS = 1.13 ± 0.17 at R08 (the only unbiased constraint), with the same sign at R06–R08 (+4.6 / +8.0 / +13.5 %): a possible IS bias. Reading (ii) at the plain value is 503 events. The frozen projection takes min(term, (N_trig/96,000)·Exp(1)) in every pseudo-experiment (mean 426, 68 % value 485; no threshold at 485): this binds in ≈ 57–67 % of pseudo-experiments under both readings, and the +13 % shift moves the censored mean by ≈ +6 % [E, ODD toy]. | [E]; [V] `is_check_c2.json`, `is_check.json`; §4.2 |
| **no-credit value of the term** beyond R07 | **485 events** (68 % zero-count bound of 96,000 direct trials; mean 425.5) | [V] arithmetic; STR l.1018, l.1175-1178 |
| CPU | v1: 4.74 CPU-h in campaigns + ≈ 0.15 interactive ≈ 4.9 of 15; cycle 1: 0.886 CPU-h (B3 check) + < 0.01 (stats, combine, pileup_term, plots); total ≈ 5.8 of 15 | [V] markers; [E] tests |

### 0.1 Status of the closure failure (A1) and of rules 1–2 — the binding wording

*Phase 1 assumed* that repaired thinning ([SD4]: grouping at the target density) and an independent occupancy model
could each be brought inside s_model ≤ 0.135 on the development samples. *Phase 3 found* that both over-predict the
development direct count at the first held-out width step (R06): thinning ×2.17, the occupancy model ×1.43. **The
closure fails for both estimators on development**: thinning (b) χ²/ndf = 4,839/14 (V_boot) and R06 beyond L + 2σ_tot;
occupancy held-out pull 10.6σ (statistical). By the Phase-3 alarm rule this blocks B2 until rule 2 has run.

- **Rule 1** (STR l.2744-2745, l.2756-2757; l.3000; COM l.37) reads the cap status at the binding **day-15 reading**,
  after a redesign has been tried (STR l.396). **Not met now.** Status: "PRELIMINARY, reviewed: both above the cap on
  development; rule 2 running". The day-15 reading is already expected to pause on B₅₀.
- **Rule 2** (STR l.2759-2760): "An estimator above its cap is redesigned if a cause is found by day 15; otherwise the
  pre-registration declares it "not submitted" and its factor has no credit (a Q3 route)". Q3 was granted at Gate A
  (COM l.38).
  - **Repaired thinning — redesign identified: the re-find variant** (a full ρ = 1 re-find of each thinned subset; it
    keeps [SD4] and has no fitted parameter; ≈ 1,200 CPU-h [E] for 3,000 events at K = 64). It is an unapproved overrun
    (COM l.257), so it **waits for the user at the pause**. Thinning is "not submitted" only if the user declines. Before
    the pause, a small new run on the 400 control trials (several draws per trial, hit sets stored, no direct count)
    measures its N_eff per rung and per CPU-h (ADV-A A3; DOR C4).
  - **Occupancy model — no cause demonstrated; cause investigation running (report by 30 Nov); one redesign only if a
    cause is found; otherwise not submitted.** The investigation (ADV-A A1) is a 10× `occin` diagnostic plus one
    mechanism test on hits, with a hashed method and the "cause found" criterion written beforehand. Redesign (b) is
    **not** ordered.
- **Who resolves A1:** the orchestrator, through the rule-2 process above. This version states the routes; it does not
  close A1.

## 1. What was run

| campaign | content | jobs | CPU-h | status |
|---|---|---|---|---|
| `p3-b-thin` | repaired thinning of C1 ρ = 2 (`p2-a-c1-pu2`, 1,000 events, 2,000 trials), K = 64, q = 1/2 | 50 | 1.392 | 50/50 done |
| `p3-b-direct` | direct development counts per trial and column (C1 ρ = 1, `p2-a-c1-pu1`, 4,000 events, 16,000 trials) | 4 | 0.015 | 4/4 |
| `p3-b-occin` | occupancy inputs: replayed ρ = 1 finder pools, per-surface densities, 1,000 random planes per trial on real hits | 20 | 1.541 | 20/20 |
| `p3-b-occmod` | occupancy model on the configuration ensemble (8 seeds; occmod-000 re-run with `--force` because its first attempt started before the last occin file existed and read 19 of 20 files) | 8 (+1) | 0.478 | 8/8 |
| `p3-b-refind` | control R1: ρ = 2 events with dumps (C1 pu2 jobs 0000–0039, 200 events, 400 trials) thinned at hit level, frozen ρ = 1 finder re-run | 20 | 1.317 | 20/20 |
| interactive tests on maxwell (identity, band, replay, model, variants) | — | — | ≈ 0.15 [E] | — |
| **cycle 1 (Ivar):** B3 IS check `is_check.py` (stats + 3 interactive niced processes on maxwell, read-only, no campaign) | plain 10⁵ + fresh IS 2,000 toys on each of the 6,400 stored stage-B configurations | 3 | 0.886 | done |
| **cycle 1:** `pileup_term.py` rerun (arithmetic), `plots.py` (1 job, maxwell) | — | 2 | < 0.01 | done |
| **cycle 2:** `is_check_c2.py` (standard library, einstein, nice 19; re-analysis of existing outputs, no Monte Carlo) | — | — | ≈ 0 (0.05 s) | done |

CPU of the campaigns from the markers (one row per job attempt with a terminal status, summed) [V; DOR §2.5: 4.743]. All
on maxwell. Slot lines in `SLOTS.md`. Campaign definitions `src/p3b/campaigns/p3-b-*.json` (`make_campaigns.py`).

## 2. Definitions used as frozen (nothing chosen here)

- **Counted object [SD4]** (STR l.1128-1131): distinct hit sets after the grouping (`weights.group_sets`, rank order,
  ≥ 50 % of the smaller set shared with the group leader) applied at ρ = 1; per rung the number of groups with ≥ 1
  passing member (exactly `production.process_trial`'s `n_grp`). The union (passing candidates, no grouping) is a
  diagnostic only.
- **Thinning unit** (STR l.1135-1136, "v1's thinning unit, transcribed from the v1 code"): the interaction id INT of
  the finder pool, keep probability q = 1/ρ (`acts/stage4/finder/weights.py` l.5-8) [V: read]. One Bernoulli draw per
  interaction **shared by all candidates of the trial**, K = 64 draws per trial, plane and axis fixed at their ρ = 2
  values (v1 plan step 3b, "no refit after thinning"), all rung variables recomputed on the kept hits [V:
  `thin_core.py`; re-implemented independently, DOR §2.4].
- **Closure statistic, evaluability, tolerance, (b), s_model, cap, verdict classes, s_tot**: STR §4.0 points 2–7;
  K = 13 (COM l.340). The JFC alarm band is applied to (b) (STR l.435).
- **Rungs and columns** (`src/p3b/cols.py`; STR l.171-177): R04 = N_IP2 ≥ 7 (all seven pixel + PS barrel layers with
  ≥ 2 crossings in the plane); R05–R08 = in addition w_core < 37.5 / 18.75 / 9.4 / 4.7 mm; R09 = R08 and the
  out-of-plane fit probability p(χ²_core) > 10⁻³. Crossing rungs: R0k⊗2S≥j = R0k and N_2S2 ≥ j (2S barrel layers with
  ≥ 2 crossings); R0k⊗p>P = R0k and p(χ²_core) > P. The s = 3 family is R0k ∧ N_2S2 ≥ 3 (k = 4…9); FB0–FB4.

## 3. B2-a repaired thinning

### 3.1 Code checks [V]
1. **Identity:** with q = 1 the code reproduces the stored ρ = 2 `n_grp` **and** `n_pass` of c1pu2-0000 trials 0 and 1
   at R04–R14 exactly — `test_thin.py`; independently re-implemented by DOR: 40/40 trials exact (DOR §2.4).
2. The direct job recomputes R04–R14 from the stored candidates and raises unless they equal `trials.n_grp`/`n_pass`
   and the stored rung bits. This passed on all 200 files. DOR recounted the direct reference independently from the raw
   records with identical results (DOR §2.2).

### 3.2 Development closure (1,000 ρ = 2 events vs 4,000 ρ = 1 events)

| rung | direct rate (count) | thinning rate | ln r | σ_tot | evaluable | (a) |
|---|---|---|---|---|---|---|
| R04 | 170.9 (2,733,703) | 221.4 | +0.259 | 0.014 | yes | within ln 1.5 |
| R05 | 49.46 (791,291) | 68.06 | +0.319 | 0.016 | yes | within ln 1.5 |
| R06 | 0.2479 (3,966) | 0.5372 | **+0.773** | 0.020 | yes | beyond L + 2σ (FAIL range) |
| R07 | 4.4×10⁻⁴ (7) | 1.90×10⁻³ | +1.47 | 0.38 | no | — |
| R04⊗2S≥3 / R05⊗2S≥3 / R06⊗2S≥3 | 146.6 / 43.34 / 0.2193 | 185.2 / 57.83 / 0.4594 | +0.234 / +0.289 / +0.740 | 0.015 / 0.017 / 0.022 | yes | pass / pass / FAIL range |
| R05⊗p>10⁻³ / R05⊗p>0.01 | 0.0403 (644) / 0.0066 (106) | 0.0803 / 0.0140 | +0.690 / +0.746 | 0.041 / 0.101 | yes | FAIL range |
| R06⊗p>10⁻³ | 0.0029 (47) | 0.0067 | +0.83 | 0.151 | no | — |

Rates are groups per trial; σ_tot² = 1/N + s_P² (STR §4.0 point 2), s_P = relative bootstrap error over ρ = 2 events
(2,000 replicas). (b) over the 14 evaluable rungs: χ² = 4,839 / 14 with V_boot, 3,392 / 14 with V_boot + s_model²J
(p ≈ 0, FAIL range; JFC alarm χ²/ndf > 3) [V]. Development **s_model = 0.506** (cumulative evaluable rungs R04–R06;
0.536 with the crossing rungs). This is **above the cap 0.135** under every reading of the rung set; the frozen text does not
say which rungs, and DOR §1 (2) gives 0.234–0.536 for all of them. The union count over-predicts too (405 vs ≈ 285 passing
candidates per trial at R04, ×1.42), in the direction and at the size of v1's T_seed-6 union pilot (×1.53, STR l.1124 [U]).

Compared with v1 (STR l.1121-1123 [U]: under-prediction ×1.50 / ×1.61 at R04 / R05, over-prediction at R06–R07), the
repair moves R04–R05 from under- to over-prediction and does not remove the steepening with depth.

### 3.3 Bug search, control and remediation attempts (relabelled in v2, DOR B7)
| # | kind | attempt | result [V] | reading |
|---|---|---|---|---|
| R0 | **bug search** | q = 1 identity, direct recount identity, union against v1's pilot | all as expected (§3.1, §3.2); DOR's independent re-implementation agrees (R04 1.010 ± 0.009, R05 1.007, R06 0.967) | no code bug found |
| R1 | **control** (it is the re-find variant run on 400 trials, one draw per trial, counts only) | `refind_job.py`: each of 400 ρ = 2 trials with dumps replayed exactly (PV, phimet, trial seed checked), every interaction kept with probability ½, the frozen ρ = 1 finder re-run (`process_trial` at ρ = 1) | re-found / direct: ln −0.032 ± 0.032 (R04, 1.0σ), −0.069 ± 0.035 (R05, **2.0σ**), +0.048 ± 0.104 (R06, 104 counts, 0.5σ). Repaired thinning / re-found **on the same trials** (paired bootstrap): +0.306 ± 0.009, +0.399 ± 0.011, +0.741 ± 0.104 | **Localised to candidate-level thinning versus re-finding (7σ at R06 on the same trials); mechanism not isolated.** The sample (two independent ρ = 1 chain events per ρ = 2 trial) and the thinning unit reproduce a ρ = 1 pool within the stated errors (at R06 the test excludes a sample offset of the size of the excess, 0.77, but not one of 0.2). Why the ρ = 1 finder keeps fewer distinct sets (seeding, refit from its own seeds) is an **inference, not shown**: R2 failed its sanity check, and no seed-survival or hit-overlap matching was made (R1 stores counts only). This operational cause suffices for rule 2, because it names one redesign with no free choice (ADV-A A3). |
| R2 | **remediation attempt** | refit (finder arithmetic, 3 iterations) + finder dedup (2 mrad) of every thinned R04 passer before grouping (`thin_trial_var` mode 1; mode 2 without dedup) | fails its own sanity check: at q = 1 (no thinning) 2,361 / 2,644 groups against the stored 2,731 / 3,061; at q = ½ ≈ 96–102 groups per trial (×≈ 0.56 of the direct) | not a valid emulation; not adopted; neither supports nor excludes the refit as mechanism |
| R3 | **remediation attempt** | re-ranking the thinned sets by (−N_L2, χ²/ndf) before the grouping (mode 3) | ≤ 1 % change | the rank order is not the cause |

Conclusion for B2-a: development s_model 0.506 > 0.135. The excess is localised (R1). **A redesign inside the frozen
definition exists**: the re-find variant keeps [SD4] and has no fitted parameter (v1's sentence that none was available
is withdrawn, DOR B1). A ρ-dependent finder-efficiency factor would be a ×2.41-type patch, which STR l.1175 forbids, and
is not proposed. Status by rule 2: **redesign identified: the re-find variant (≈ 1,200 CPU-h, waits for the user at the
pause); not submitted only if the user declines.**

### 3.4 N_eff (B2-g) and crossing-rung evaluability

N_eff = 1/s_boot² on 1,000 ρ = 2 events [V]: R04 5,142; R05 4,056; R06 6,861; R07 228; R08 4.1 (four passing subsets
in 128,000); R06⊗2S≥3 5,589; R07⊗2S≥3 189; R05⊗p>10⁻³ 6,142; R06⊗p>10⁻³ 698; R06⊗p>0.05 57; FB0 505, FB1 237,
FB2 46. Compared with STR's projection (N_eff ≈ 80 at R07 for 3,000 events, ≤ 10 at R08, l.1187-1190 [E]): R07 is
better (683 projected to 3,000 events), R08 as projected (≈ 12).

**B2-g projection to the 3,000-event production (N_eff ∝ events) against the 96,000-trial direct sample at the
development direct rates** [V: `B2g_projection`]: evaluable (σ_tot ≤ 0.135) at R04 (σ 0.008), R05 (0.009), R06
(0.010), R06⊗2S≥3 (0.010), R06⊗p>10⁻³ (0.063). **Not evaluable at R07**: σ_tot is 0.159, set by the 42 expected direct
counts at the development rate 4.4×10⁻⁴, not by N_eff 683. At v1's rate 7.3×10⁻⁴ the 70 counts of STR l.1182 would
give 0.126. R07⊗2S≥3 is not evaluable either (0.187). Deepest evaluable cumulative rung for PREREG_v2: **R06**; R07 is marginal and depends on the
direct rate. **[DT2]** (STR l.1198-1200) applies: the validated range of thinning is declared R04–R06, logged as a [D]
in `experiment_log.md`, user informed (RESULT notice of 24 Nov, 14:47). With s_model above the cap the range matters only if the
re-find variant is ordered. The same evaluability sets the width bookkeeping of the day-15 term (§6.2, B5).

**B2-c (agreement at depth, R08+):** thinning N_eff at R08 is 4 (12 projected) → σ ≥ 0.29 → **NOT EVALUABLE**, as STR
expected (l.1192). For information at R07 (development, not a criterion rung): thinning / occupancy = 1.90 / 1.71
×10⁻³, ln ratio +0.10.

## 4. B2-b occupancy model

### 4.1 Model (code `occ_core.py`, `occ_model.py`, `occmod_job.py`; definition frozen at 10:56 before any comparison with a direct count, session log; now also in `experiment_log.md`)
- **Configuration ensemble θ** (a "ribbon through the vertex and along the road", STR l.1140-1142): PV from the luminous
  region (σ_xy 5 µm, σ_z 45 mm, `pu_inputs.lum_pv`), MET azimuth uniform, axis azimuth φ_MET ± 0.15 (δ95), axis
  η ∈ U(−1, 1), plane rotation ψ ∈ U(0, π) about the axis with |n_z| ≥ 0.2. Band = the finder's: |u·n| < 3σ(n),
  u·a > 0, |u·n2| < 75 mm, and the road.
- **Densities** ρ_j(z): hits per mm² per event on each of the 16 barrel surfaces, φ-averaged, 2 mm z bins, from the 4,000
  replayed ρ = 1 development pools (finder input: after CKF removal and merging, top-up included). Replay checked: PV and
  phimet of every one of the 16,000 trials bit-identical to the stored trials (the job raises otherwise) [V].
- **Expected in-band hits**: at azimuth φ on a surface of radius R the band is |z − z*(φ)| < δ(φ) with
  z*(φ) = pv_z − [n_x(R cos φ − pv_x) + n_y(R sin φ − pv_y)]/n_z and δ = 3σ/|n_z|. *Derivation:* at fixed φ,
  u·n = n_x u_x + n_y u_y + n_z(z − pv_z) is linear in z with slope n_z and vanishes at z*, so |u·n| < 3σ ⇔
  |z − z*| < 3σ/|n_z|. λ = Σ_φ R Δφ ∫ρ_j dz over the interval (0.5 mm arc steps; 1/3/9 sub-steps across the band for
  TBPX/PS/2S).
- **Layers**: TBPX: N ~ Poisson(λ), P(≥ 2) = 1 − e^{−λ}(1 + λ). Stacked: crossings are hit pairs at one (φ, z);
  pairs in both sensor bands (b), only in the inner (i), only in the outer (o) are independent Poissons,
  crossings = min(b + i, b + o) (`cand_vars`), so
  P(≥ 2) = P(b ≥ 2) + P(b = 1)P(i ≥ 1)P(o ≥ 1) + P(b = 0)P(i ≥ 2)P(o ≥ 2).
  *Checks:* λ → 0 gives P → 0 as λ²/2 (TBPX); λ_i = λ_o = 0 reduces the stacked formula to P(b ≥ 2).
  R04 = all seven IP layers ≥ 2. N_2S2: Poisson-binomial of the three 2S layers.
- **Width rungs**: w_core = 1.4826 MAD of u·n2 over the pooled IP hits (pairs twice), toys conditional on R04;
  R05–R08 by importance sampling (window of half-width W/1.4826 at a centre from a grid, mixture (1 − β)g + βg·1_win/G,
  β = 0.5; weight = g / proposal); plain Monte Carlo as the check (frozen at 10:56).
- **Measured correlation factors** C(r) = P_real(r)/E_model(r) on the **real** hits of the 16,000 development trials
  (16×10⁶ planes; `band_hits` checked against a brute-force band, 0/300 mismatches).
- **Normalisation** N_cfg: GLS fit of ln(B_dir/P_real) at R04–R05 (joint event bootstrap). Prediction beyond R05:
  B(r) = N_cfg · C(R05) · E_model(r) (C held at R05; the trend of C is the reported variant). s_model =
  max(|ln r(R06)|, in-sample r.m.s.) (STR l.1146-1148).

### 4.2 Checks of the model [V]
- Per-layer P(≥ 2 crossings) on the ensemble, model vs real hits (20 test events): TBPX 0.997/0.854/0.437/0.254 vs
  0.997/0.846/0.438/0.250; TBPS 0.337/0.141/0.052 vs 0.341/0.143/0.050; TB2S 0.950/0.857/0.656 vs 0.939/0.841/0.636.
- IS vs plain Monte Carlo in the stored runs (8 seeds × 800 stage-B configurations, 200 toys each): R05 1.845 vs 1.848
  ×10⁻⁴; R06 1.558 vs 1.629 ×10⁻⁶ (MC errors 0.9 % / 2.4 %); R07 7.54 vs 7.24 ×10⁻⁹ (12 plain passing toys against 12.5
  expected). **R08: IS 4.78×10⁻¹¹ vs plain 6.04×10⁻¹⁰ (v1 omitted this row), from one plain passing toy of 1.28×10⁶
  where IS expects 0.079** (P(≥ 1) = 7.6 %), so R08 is neither contradicted nor validated by the stored runs (DOR B3).
- **B3 re-estimate of the IS error (cycle 1, `src/p3b/is_check.py`, `outputs/p3b/is_check_stats.json`,
  `outputs/p3b/is_check.json`)**:
  1. *Statistical error of the stored IS at R08* [V, `is_check_stats.json`, `is_check_c2.json`]. The stored
     200-toy runs alone give 7.2 % (spread of the 8 seeds, v1's number), 8.7 % (within-seed spread of the 6,400
     per-configuration means) and 8.6 % (toy level, from `isr[:, 3, 1]`). DOR's ≈ 12 % [E] is not reproduced, neither
     by these nor by LIV's nine readings (7.2–8.7 %).
     - **All of these are lower bounds** (corrected in v3, LIV B-new-1). The fresh IS run with 10× the toys on the same
       6,400 configurations has a toy-level error of 6.87 %, not the ≈ 2.7 % that 8.64 %/√10 would give. Its per-toy
       relative variance is ×6.3 larger (R07: ×1.95): the 200-toy runs do not sample the tail of the weight
       distribution.
     - With the fresh per-toy variance, the stored R08 value has a toy-level error of **≈ 22 % [E]** (0.0687 × √10 =
       0.217; R07 ≈ 5.7 %). This is itself a **lower bound**, not only possibly: the fresh IS also misses the tail. The 64 configurations with the largest stored R08 values hold 51.1 % of the stored sum but 1.4 % of the fresh sum and 0 of the 45 plain passes; the fresh top 64 hold 31.6 % of the fresh sum and 1 plain pass where ≈ 13 would be expected [ODD C-2, his V].
     - The heavy tail in numbers: the **IS toy effective sample size at R08 is 11–43 toys per seed of 160,000, 195 in
       total** (DOR B3, LIV C-7). The top 1 % of the stage-B configurations carry 51 % of the R08 sum (27 % at R07), and
       the top 10 carry 20.5 %. The effective number of configurations is 129 of 6,400. These two figures describe the toy noise of the stored run, not the configurations: at R08 the per-configuration IS values are noise (correlations stored–fresh 0.014, fresh–plain 0.023 [LIV]). Fresh IS (2,000 toys) on the
       two top-ranked configurations gave R08 values ×130 and ×1,200 below the stored 200-toy values.
     - The configuration-sampling part of the error is small, 0–1.6 % [E, LIV §2, from covariances of independent
       estimates]: the stored 8.70 % is ≈ 99 % toy noise (8.64 %). Those covariances come from the same noisy per-configuration estimates, so this figure has little power [ODD C-2]. v2's sentence that "the 8.7 % covers the
       configuration sampling" is withdrawn.
  2. *Paired plain-toy check* [V, `is_check.json`]. Its inputs are durable in
     `outputs/p3b/is_check_inputs/ischeck-{0,1,2}.npz` (sha256 in SCHEMA.md). It ran in cycle 1 as 3 niced processes on
     maxwell, 0.886 CPU-h. On all 6,400 stored stage-B configurations it ran 10⁵ plain toys each (6.4×10⁸) and fresh IS
     with 2,000 toys per configuration and rung, with new seeds. Because configuration sampling is negligible, this
     paired check covers essentially the whole MC error of the stored value.
     - R08: 45 plain passing toys, in 45 different configurations [LIV]. **truth/stored = 1.13 ± 0.17** (plain / stored
       IS; the relative Poisson error 1/√45 = 0.149 of the plain value gives ±1.135 × 0.149 = ±0.169; v3's ± 0.15
       applied it as an absolute error [ODD C-1]), i.e. the plain 68 % interval relative to the stored value is
       [0.97, 1.30], +30 % / −3 % (Garwood 68 %: [0.966, 1.330] [ODD]). Plain /
       fresh IS = 1.10; fresh / stored = 1.03.
     - R07: 6,747 plain passes; plain / stored IS = 1.080: 1.4σ with the 5.7 % stored error of item 1 (1.9σ with the
       4.1 % stored-run error); both are computed with errors that are themselves lower bounds [ODD C-3]. Plain / fresh
       IS = 1.028 (1.3σ, with the fresh toy-level error, also a lower bound).
     - R06 (stored runs, 2,699 plain passes): plain / stored IS = 1.046 ± 0.019: 2.4σ with the plain error alone, 1.5σ with the stored IS error of 2.4 % added (a lower bound too) [ODD C-3].
  3. *Reading (corrected in v3).*
     - The factor 12.6 of the single stored plain toy (≈ 4,400 events) is excluded: ≈ 500 passes would be expected and
       45 were seen.
     - The unbiased plain estimate lies **above the IS estimate with the same sign at R06, R07 and R08 (+4.6 %, +8.0 %,
       +13.5 %), and the offset grows with depth**. The single pulls are ≈ 0.8σ (R08), 1.4σ (R07) and 1.5σ (R06; 2.4σ with the plain error alone), each computed with errors that are themselves lower bounds. The pattern is what a heavy-tailed
       IS sum gives in a finite sample, which falls below its mean more often than above it. It is therefore stated as a
       **possible downward bias of the IS value, not as noise**. The best reading is that the stored IS value at R08 is
       low by ≈ 3–13 %, with the truth constrained to truth/stored ∈ [0.97, 1.30] (plain, 68 %). The plain check is the only unbiased constraint on the stored value.
     - The MC error of E_model(R08), and so of every R08 number of §6 under both readings, is **≈ 22 % [E], a lower bound**: the
       symmetric toy-level error of the fresh run. From the plain check alone the 68 % interval is +30 % / −3 %; the two
       statements are not equivalent [ODD C-1]. R09 adds the binomial
       error of the fit-probability fraction, √((1 − 0.0119)/47) = 0.145, for **≈ 26 %** in total [E].
     - Consequence: reading (ii) at the plain central value is 443 × 1.135 = 503 events (reading (i): 347 × 1.135 = 394).
       **The frozen projection has no threshold at 485** (corrected in v4, ODD B-new-2). In every pseudo-experiment it
       takes min(term, (N_trig/96,000)·Exp(1)), a fresh draw with mean 426 and 68 % value 485: `strategy_budget.py` l.585-587
       (`x = min(x, capv if capv >= 0 else -capv * rnd.expovariate(1.0))`) with l.678 (`PU_CAP = -NTRIG / 96000`);
       STR l.1586-1588 ("drawn like every other zero-count term: N_trig·λ/96,000 with λ ~ Gamma(1) in each
       pseudo-experiment (68 % value 485 events)"); STR l.953-954 ("censored at the predictive draw of its no-credit
       bound, 426 × Exp(1)") [V: read].
       - ODD's toy [E: his, 4×10⁵ draws, width 0.822; widths 0.885 or 0.427 change the numbers by ≤ 2 %] covers R08
         medians 347 (i), 394 (i, plain), 443 (ii) and 503 (ii, plain). The censoring binds in 56.5 / 60.0 / 63.5 /
         67.0 % of the pseudo-experiments, and the mean contribution is 241 / 256 / 270 / 286 events, against 425.5
         without credit.
       - So the censoring already binds in most pseudo-experiments at the stored values, under both readings. The +13 %
         plain shift moves the censored mean by only ≈ +6 %, and the gap between readings (i) and (ii) is ≈ 12 % in the
         projection.
       - The R08 term is at the no-credit scale with or without a credit.
     - The frozen definition keeps IS as the primary estimator (10:56). No value is replaced; the error statement is.
       `pileup_term.json` carries `occupancy_day15.mc_rel_error_c2` = 0.217 at R08 (and R08 ∧ N_2S2 ≥ 3) and 0.261 at
       R09 (and R09 ∧ N_2S2 ≥ 3), from `src/p3b/is_check_c2.py` → `outputs/p3b/is_check_c2.json`. The cycle-1 key
       `mc_rel_error_b3` (0.149, the plain-check precision only) is superseded and kept unchanged, as is the v1 key
       `mc_rel_error` (0.072).
       - In v4 the same key is also on the reading (ii) records (`occupancy_B2b_model.mc_rel_error_c2`).
       - `pileup_term.py` was edited to write these keys on a rerun but has **not been rerun**: there is no numpy on
         einstein and cycles 2–3 allowed no jobs. The keys come from `is_check_c2.py --patch` [ODD C-5].
       - The R08 ∧ N_2S2 ≥ 3 and R09 ∧ N_2S2 ≥ 3 values are the R08 value transferred, because the paired check was not
         run with the 2S requirement [E, ODD C-4 (b)].
       - The frozen s_tot (STR §4.0 point 7) has no MC term. Whether p3-a adds the MC error to the projection width is
         not fixed here [ODD C-4 (c)].
- Correlation factor measured on real hits: **C(R04) = 1.184, C(R05) = 1.207**; post hoc (diagnostic only, not an
  input) C(R06) = 1.94×10⁻⁶/1.56×10⁻⁶ = 1.24 (31 real planes, ±18 %).

### 4.3 Development closure [V: `b2_dev_closure.json` → occupancy]
N_cfg = 1.880×10⁵ (GLS weights 0.964 R04 / 0.036 R05).

| rung | direct | model (B2-b) | ln r | σ_tot | role |
|---|---|---|---|---|---|
| R04 | 170.9 | 171.9 | +0.006 | 0.010 | derivation (in sample) |
| R05 | 49.46 | 41.87 | −0.166 | 0.019 | derivation (in sample) |
| **R06** | 0.2479 | 0.3534 | **+0.355** | 0.034 | **held out** |
| R07 | 4.4×10⁻⁴ (7) | 1.71×10⁻³ | +1.36 | 0.38 | not evaluable |
| R04 / R05 / R06 ⊗ 2S≥3 | 146.6 / 43.34 / 0.2193 | 145.0 / 35.60 / 0.3028 | −0.011 / −0.197 / +0.322 | 0.010 / 0.020 / 0.035 | 2S crossing comparisons |

R06 is within ln 1.5 (tolerance (a)) but 10σ from zero statistically: **s_model = 0.355 > cap 0.135** (trend variant
0.374). The 2S factor itself is predicted to ≤ 3 %: ln r(R0k⊗2S≥3) − ln r(R0k) = −0.017 / −0.030 / −0.032 at k = 4/5/6.
JFC band: the held-out pull with statistical errors only is 10.6σ (alarm); with s_model in V the single held-out rung
gives χ² = 1 by construction (tautological, not a test). The reference is the same 4,000 events as the model inputs,
which STR l.1145-1148 allows, handled by the joint event bootstrap (DOR §2.2).

### 4.4 Variants and diagnostics for B2-b (relabelled in v2, DOR B7) — no model remediation was attempted
| # | kind | what | held-out ln r(R06) | reading |
|---|---|---|---|---|
| O1 | **variant** (pre-declared at 10:56) | trend of C | +0.374 | above the cap |
| O2 | **variants** (diagnostic) | normalisation R04 only / diagonal weights / R05 only | +0.349 / +0.389 / +0.521 | the R06 excess does not come from the fit |
| O3 | **diagnostic** | the model's width fall replaced by the real-hit random-plane fall (N_cfg · P_real(R06)) | +0.385 | localises the problem outside the occupancy arithmetic, **at ≈ 1.8σ only**: C(R06)/C(R05) = 1.03 ± 0.18 (31 real R06 planes) against e^0.355 = 1.43 |
| O4 | **diagnostic** | random planes vs finder groups: R05/R04 = 0.244 (real planes) vs 0.289 (finder); R06/R05 = 0.0087 ± 18 % vs 0.0050 | — | **restates the closure failure**: by construction (closure.py l.236-242) "N_cfg(r) = B_dir/P_real is rung-dependent" is the in-sample R05 residual and the held-out R06 residual in other words. It is not a cause. |

**No cause is demonstrated for the occupancy model.** A candidate mechanism is that the finder refits its planes to
the hits while the model scores fixed random planes, which would give found planes a different width distribution from
random ribbons. It is a hypothesis and was not examined. Why no remediation was attempted: under the frozen rules nothing may be chosen after
R06 has been seen (PHASE3_BRIEF §2), and rule 2 places any redesign at decision point 2 and only if a cause is found.
Status by rule 2: **no cause demonstrated; cause investigation running (report by 30 Nov); one redesign only if a cause
is found; otherwise not submitted** (ADV-A A1). The investigation may use this spent C1 development sample. `dev.pu1`
stays sealed for it (ADV-A A2).

## 5. Closure-slope weights (EXP §10 item 8; options stated, none chosen)
STR §4.0 point 7 fits b̂ ± σ_b, "the fitted slope of ln r against the rung index", for n ≥ 3 evaluable rungs without
fixing the weights. Every option's outcome (sandwich σ_b, valid for any weights) [V], **all in v2's convention
ln r = ln(P/N)** (C2: C1's ln(N/P) values of v1 are sign-flipped here):

| sample | unweighted OLS | WLS, bootstrap diagonal | GLS, full bootstrap covariance |
|---|---|---|---|
| v2 repaired thinning, development R04–R06 | +0.257 ± 0.009 | +0.244 ± 0.009 | +0.082 ± 0.002 |
| C1 (v1-type thinning), R04–R06 (MAT l.127-146 [U], converted from ln(N/P)) | +0.423 | +0.365 ± 0.008 (frozen seed) | not computed |

The weight dependence is a factor 3 on v2's development points: the nested rungs are strongly correlated and the
three points are not on a line, as in C1. Options for PREREG_v2: (1) unweighted OLS with the sandwich σ_b; (2) WLS
with weights fixed before the test from the development bootstrap; (3) GLS with the test-sample covariance; (4) any of
them with σ_b enlarged by the spread between options. The choice is the orchestrator's or the user's. With both estimators
above the cap it matters only if one is redesigned and submitted.

## 6. Day-15 pile-up term per T2 candidate (`outputs/p3b/pileup_term.json`)

**Status of every R08/R09 number in this section: the rule-1 projection input of STR l.2737-2741 only, "no credit",
under both readings** (ADV point 8 (ii)). They come from a model above the cap. They are not a pile-up estimate, and the
widths below are bookkeeping that would apply only to a submitted estimator, which neither estimator is.

### 6.1 Two readings of "the development model's R04–R07 inputs" (STR l.2741; DOR B4; not chosen here)
- **Reading (i)** (v1, the executor's frozen choice of 10:56): the same model with one scale A fitted on the
  development direct counts at R04–R07 (weights 1/(σ_stat² + s_model²); residuals R04 −0.22, R05 −0.41, R06 +0.11,
  R07 +1.12). A single scale cannot fit R04–R07. This reading **uses the held-out R06 (and the 7 R07 counts) to set the
  normalisation**, so R06 no longer checks the term. It is not a ×2.41 patch, but it is a fit to the deepest direct
  counts.
- **Reading (ii):** the B2-b model with its frozen R04–R05 normalisation (STR l.1145-1146 "using rungs R04–R05 only"),
  evaluated at R07–R09. R09 = the B2-b R08 value × the fit-probability fraction 0.0119, newly computed in v2. The
  implementation holds C at its R05 value beyond R05 (`pileup_term.py`); **this is the reading (ii) that is tabled**.
- **Reading (iii)** (LIV C-2; listed, not chosen, not tabled). STR l.1145 calls the model's inputs "densities,
  correlation factors" derived "using rungs R04–R05 only". "The development model's R04–R07 inputs" can then mean the
  same inputs derived using R04–R07: C(r) measured on real hits at R06/R07, with no fit to direct counts. Neither (i)
  (a scale fitted to direct counts) nor (ii) as implemented (C held at R05) is that. With the current C(R06)/C(R05) =
  1.03 ± 0.18 it would move reading (ii) by ≈ +3 % (R08 ≈ 457 [E: 443 × 1.03]). The 10× `occin` of the occupancy cause
  investigation will give C(R06) to ±6 %. DOR B4's description of (ii) ("inputs extended to R07") fits (iii) better.
  The orchestrator chooses.
- Rates per trial; events = rate × N_trig with N_trig = 4.0848×10⁷ (`strategy_budget.py` l.68 [U]); **p3-a rescales
  to its MET-model N_trig**. The model MC error enters both readings equally: ≈ 22 % at R08 and ≈ 26 % at R09 [E] (§4.2). The MC part alone is
  ±75 events on R08 (i) = 347 and ±96 on R08 (ii) = 443 (R09: ±1.1 on 4.1 and ±1.4 on 5.25). The plain check points
  upward (truth/stored 1.13 ± 0.17): at the plain central value reading (ii) is 503 events and reading (i) 394. In the
  frozen projection both are censored in every pseudo-experiment by min(term, (N_trig/96,000)·Exp(1)) (mean 426, 68 % value 485;
  §4.2, §6.3). For these medians this binds in ≈ 57–67 % of pseudo-experiments [E, ODD toy].

### 6.2 Table: both readings, with the widths that follow from §3.4

| candidate | rate / trial (i) | events (i) | events (ii) | width: cap, last test R07 (v1 rate) | width: cap, last test R06 (dev rate) | width: measured (dev), hypothetical bookkeeping | thinning (dev) | direct dev count |
|---|---|---|---|---|---|---|---|---|
| R04 | 137.2 | 5.6×10⁹ | 7.0×10⁹ | 0.135 | 0.135 | 0.355 | 221.4 | 2,733,703 |
| R05 | 32.8 | 1.3×10⁹ | 1.7×10⁹ | 0.135 | 0.135 | 0.355 | 68.1 | 791,291 |
| R06 | 0.277 | 1.13×10⁷ | 1.44×10⁷ | 0.135 | 0.135 | 0.355 | 0.537 | 3,966 |
| R07 | 1.34×10⁻³ | 5.5×10⁴ | 7.0×10⁴ | 0.135 | 0.427 | 0.539 | 1.90×10⁻³ | 7 |
| **R08** | 8.49×10⁻⁶ | **347** | **443** | 0.427 | **0.822** | 0.885 | 3.1×10⁻⁵ (N_eff 4) | 0 |
| **R09** | 1.01×10⁻⁷ | **4.1** | **5.25** | 0.589 | **0.917** | 0.974 | 0 | 0 |
| R04 ∧ N_2S2≥3 | 115.7 | 4.7×10⁹ | 5.9×10⁹ | 0.191 (2S credit) / 1.224 | 0.191 / 1.224 | 0.419 | 185.2 | 2,345,475 |
| R05 ∧ N_2S2≥3 | 27.9 | 1.1×10⁹ | 1.5×10⁹ | 0.191 / 1.224 | 0.191 / 1.224 | 0.419 | 57.8 | 693,390 |
| R06 ∧ N_2S2≥3 | 0.237 | 9.7×10⁶ | 1.24×10⁷ | 0.191 / 1.224 | 0.191 / 1.224 | 0.419 | 0.459 | 3,509 |
| R07 ∧ N_2S2≥3 | 1.15×10⁻³ | 4.7×10⁴ | 6.0×10⁴ | 0.191 / 1.224 | 0.448 / 1.289 | 0.583 | 1.63×10⁻³ | 5 |
| **R08 ∧ N_2S2≥3** | 7.36×10⁻⁶ | **301** | **384** | 0.448 / 1.289 | **0.833 / 1.468** | 0.913 | 3.1×10⁻⁵ | 0 |
| **R09 ∧ N_2S2≥3** | 8.72×10⁻⁸ | **3.6** | **4.55** | 0.604 / 1.677 | **0.927 / 1.818** | 0.999 | 0 | 0 |

Widths: s_tot² = s_model² + Σs_f² + (b̂² + σ_b²)d_in² + b₀²d_out², b₀ = ln 1.5 (STR §4.0 point 7) [V: `pileup_term.py`].
- *Cap columns:* the convention of the frozen projection, with s_model at the cap, b̂ := 0 and σ_b := b₀. The **last
  width-test rung follows §3.4**:
  - At the development direct rate R07 is not evaluable (42 expected counts, σ_tot 0.159), so the last test rung is
    **R06** and d_in = 2 at R08: √(0.135² + 4·0.405²) = **0.822**, and R09 √(0.135² + 5·0.405²) = 0.917.
  - At v1's rate R07 would be evaluable (σ_tot 0.126) and d_in = 1: 0.427 = STR l.518 "0.43", and R09 0.589 = "0.59".
  - In the s = 3 rows the two values are with / without a 2S crossing credit (d_out = 3 without).
  - The column that applies depends on the 96,000-trial direct rate at R07, which is not known before 4a.
- *Measured (dev) column:* "hypothetical bookkeeping" (C1). It uses s_model 0.355, the width family tested at R06 only,
  and, in the s = 3 rows, a 2S credit s_f = 0.224 built from the nine development 2S comparisons. Six of these sit on
  the derivation rungs R04/R05 of the same sample and are consistency checks only. From R06⊗2S alone s_f = 0.344 [V:
  r.m.s. of +0.355, +0.355, +0.322]. R09 uses the fit-probability fraction 0.0119 (47 of 3,966 development R06 groups,
  shared input Df-2).

### 6.3 No-credit value and the eligibility readings (DOR B2)
- **No-credit value of the term** (STR l.1175-1178, l.1018, l.1586-1588): the direct count at R07 and, beyond it, the
  zero-count bound of the 96,000 direct trials, N_trig × 1.14 / 96,000 = **485 events** at 68 % (the mean, drawn as
  N_trig·λ/96,000 with λ ~ Gamma(1), is 425.5) [V: arithmetic; STR l.1018 "485 events at 68 %" and l.1177 "485 events" agree].
- **Two readings of the class**, which depend on how rule 2 ends:
  - **"not submitted" (NOT TESTED; STR §4.0 point 4 (c) l.394-396, point 6 l.463, §4.12 table l.1873):** if no
    redesign is submitted (thinning: the user declines the re-find; occupancy: no cause by 30 Nov), the factor has no
    credit from the freeze on ("a Q3 route", STR l.2760; Q3 granted at Gate A, COM l.38: "an untested MUST closure
    criterion enters at its ceiling, no credit, selection eligible"). The term is labelled "no credit" and enters as the predictive draw of its no-credit bound, N_trig·λ/96,000 with λ ~ Gamma(1) in each pseudo-experiment (mean 426, 68 % value 485; STR l.1586-1588, `strategy_budget.py` l.585-587, l.678). Selections beyond R07
    stay in the figures, flagged.
  - **"FAIL" (STR l.1175-1178, §4.12 table l.1878 "both pile-up estimators FAIL"):** if submitted estimators (a redesign)
    are tested at 4a and both fail, the plan's "closure fails" outcome for pile-up applies: R07-direct, the ladder
    shows the 485-event bound, and **no selection beyond R07 is eligible ([SD8])**.
  - If one estimator ends submitted and PASS, the term rests on it ("one estimator", l.1877).
  - **Mixed route (LIV C-5):** thinning ends "not submitted" (the user declines the re-find) while an occupancy
    redesign is submitted and FAILs at 4a. Neither the "both FAIL" row nor the "one estimator" row of the §4.12 table
    covers this case. No estimator then carries credit, so beyond R07 the term enters as that predictive draw (mean 426, 68 % value 485). The
    frozen text does not fix whether [SD8]'s "no selection beyond R07 is eligible" applies (as in "both FAIL") or the
    selections stay flagged (as in "not submitted"). Flagged for the orchestrator, not chosen.
- **Consequence for the R08/R09 candidates:** under either no-credit reading the pile-up term of every R08+ candidate **enters as
  the predictive draw N_trig·λ/96,000, λ ~ Gamma(1) (mean 426, 68 % value 485)**, against 347 / 4.1 (reading (i)) or 443 / 5.25 (reading (ii)) if a credit existed. Under the FAIL reading
  they are not eligible at all. 485 is above the 300 line by itself (ADV point 7). Even with a credit, the frozen projection takes
  min(term, (N_trig/96,000)·Exp(1)) in every pseudo-experiment. The credited R08 medians (347–503 events, plain-shifted values
  included) are therefore censored in ≈ 57–67 % of pseudo-experiments and contribute 241–286 events on average, against
  425.5 without credit [E, ODD toy; §4.2]. The R08 term is at the no-credit scale with or without a credit.
- **Which bound applies at day 15, a reading to flag and not to choose:** the frozen planning value is 485 at 96,000
  trials. Rule 1 speaks of "the samples that exist at day 15". The 16,000 development trials give N_trig·1.14/16,000 =
  **2,910 events** [V]; with `dev.pu1` added (≈ 39,840 trials [E]) it would be ≈ 1,170 [E].

## 7. Definitions for PREREG_v2 and production (written, not launched)
- **B2-d** direct sample: `src/p3b/campaigns/prod/p4a-b2-prod-pu1.json`: 24,000 events × 4 roads = 96,000 trials,
  stream `prod.pu1`, 1,200 jobs of 20 events (≈ 1,114 s each at 55.7 s/event, EXP §3.1), ≈ 371 CPU-h, `--dump 0`.
  Flag: the C1 sample kept dumps (2.64 MiB/event); nothing in B2's test needs them, and keeping them would take 63 GB.
- **ρ = 2 sample**: `p4a-b2-prod-pu2.json`: 3,000 events × 2 roads, stream `prod.pu2`, pre-merge store N_IP2 ≥ 6, 600
  jobs of 5 events (≈ 1,015 s each), ≈ 169 CPU-h, max RSS 2.1 GB → ≤ 2 jobs per node, ≈ 203 GB pre-merge store.
  Thinning afterwards with `thin_job.py` (K = 64). **Must not be launched** before the PREREG_v2 hash and the user's
  approval. The thinning definition it carries may be void if the re-find variant is ordered (ADV point 8 (i)).
- Launch (orchestrator, after the PREREG_v2 hash): `tools/runner/bin/qv2run ssh launch <abs path>.json --nodes
  landau,maxwell,schrodinger [--max-per-node N] --on <node>`. Both files load in `qv2run status` [V].
- For PREREG_v2: [SD4] object and the thinning unit as in §2; the occupancy model definition of §4.1; N_eff per rung
  and the B2-g projection (§3.4); [DT2] range R04–R06; evaluability of the crossing rungs (thinning: 2S crossings at
  R04–R06 and R05⊗p>10⁻³, R05⊗p>0.01 evaluable on development, R06⊗p not; occupancy: 2S crossings R04–R06 evaluable,
  fit-probability and shape comparisons consistency only); the slope-weight options (§5). Per ADV point 8 (v), "not
  submitted" or "pause met" are **not** written into PREREG_v2 before the rule-2 process is finished.
- **Enlarged development sample `dev.pu1` (corrected, DOR B8):** a **frozen MUST development sample** (STR §4.17 row 12,
  l.2105: ≈ 5,960 events, 100 CPU-h, role "development (decision point 2, s_model, crossing rungs)"; STR l.1146 names
  it as an input of the occupancy model). It is **being produced now** (ADV-A A4): work package p3-e has defined the campaign
  `p3-e-devpu1` (298 jobs × 20 = 5,960 events; job seeds disjoint; ≈ 0.5 % interaction-seed reuse, ESTIMATE, exact count
  pending [U: KET points 2, 5, 7]) and run its test job devpu1-0000; the full launch, with
  pre-flight and a budget check, is the orchestrator's [U: DAILY_NOTES 14:51, P3E_hilde_2026-11-24.md]. Its direct counts at R06 and deeper and its crossing rungs **stay unopened by every agent** until a
  redesign is hashed or the occupancy investigation is closed with no cause (ADV-A A2). Its roles are: the only
  held-out sample for a rule-2 redesign (job seeds disjoint; ≈ 0.5 % interaction-seed reuse, ESTIMATE, exact count
  pending; immaterial for this role by KET point 3), the day-15 R04–R07 inputs, and crossing-rung evaluability. It does not make
  development R07 evaluable: at the development rate it adds ≈ 10 R07 counts to the 7 (≈ 17 in 39,840 trials [E:
  4.375×10⁻⁴ × 39,840 = 17.4]), σ ≈ 0.24 > 0.135. v1's "not requested" is withdrawn.
- Shape crossing rungs (R15–R20 ⊗ R06) were not computed: the h/o variables need the hit records and the WP_RULE F1
  definitions, and they are consistency-only for the occupancy model. Open item.

## 8. Decisions and open routes (orchestrator / user) — rewritten in v2 (DOR B1)
1. **Rule 1:** not met now. The cap status becomes binding at the day-15 reading (STR l.2744-2745), which is already
   expected to pause on B₅₀. Status: "PRELIMINARY, reviewed: both above the cap on development; rule 2 running". The
   RESULT notice of 24 Nov 14:47 carries it.
2. **Rule 2, thinning:** redesign identified: the re-find variant (≈ 1,200 CPU-h, waits for the user at the pause); not
   submitted only if the user declines. Before the pause: the N_eff-per-CPU-h run on the 400 control trials (ADV-A A3;
   several draws per trial, hit sets stored so that thinned and re-found groups can be matched, DOR C4).
3. **Rule 2, occupancy model:** no cause demonstrated; cause investigation running (report by 30 Nov); one redesign only
   if a cause is found; otherwise not submitted. Option (b) of v1 (a measured configuration-to-group map) is **not**
   ordered (ADV-A A1, A6). v1's option (c) (a larger declared s_model) is not admissible: the cap still applies (ADV
   point 3).
4. **Day-15 reading of the term** (§6.1): reading (i) or (ii), for the orchestrator. Both are rule-1 input only, no credit.
5. **Width bookkeeping** (§6.2): it applies only if a credit remains. The last test rung then follows the 4a direct rate at R07.
6. **Zero-count bound at day 15** (§6.3): 485 (planning, 96,000 trials) or the bound of the samples that exist (2,910).
7. **Slope-weight option** (§5) for PREREG_v2.
8. **B3 / B-new-1** (§4.2): the quoted MC error is ≈ 22 % at R08 and ≈ 26 % at R09 [E], both lower bounds. Plain lies above IS with the same sign at R06–R08 (a possible IS bias, ≈ 3–13 % at R08; truth/stored 1.13 ± 0.17), and reading (ii) at the plain value is 503 events. The frozen projection censors the term in every pseudo-experiment by min(term, (N_trig/96,000)·Exp(1)) (mean 426, 68 % value 485), which binds in most pseudo-experiments under both readings (§4.2). Nothing to decide now; this is for the day-15 reading.

## 9. Figures (regenerated in cycle 1)

Notation used in all three figures: R04 = all seven pixel + PS barrel layers with ≥ 2 crossings in the plane; R05–R08 =
in addition the in-plane core width w_core < 37.5 / 18.75 / 9.4 / 4.7 mm; R09 = R08 and the out-of-plane fit
probability p(χ²_core) > 10⁻³. "R0k⊗2S≥j" = R0k and at least j of the three 2S barrel layers with ≥ 2 crossings;
"R0k⊗p>P" = R0k and p(χ²_core) > P. ρ = 1 / ρ = 2 are the C1 development samples at the target pile-up (PU 200) and at
twice it.

![Development closure of both pile-up estimators. The figure shows ln r = ln(prediction / direct development count) per rung and crossing rung (notation above) for repaired thinning (circles; 1,000 ρ = 2 events, K = 64) and the occupancy model (squares; R04 and R05 are its derivation rungs, R06 is held out). Filled markers are evaluable comparisons; open markers are not evaluable (σ_tot > ln 1.5/3), among them both R07 points (7 direct counts: +1.47 and +1.36). Error bars are σ_tot of STR §4.0 point 2. Dashed lines show the tolerance ±ln 1.5 and dotted lines the cap ±ln 1.5/3. The occupancy model has no point at the fit-probability rungs (R0k⊗p>P), because it does not predict p(χ²_core); its fit-probability fractions are taken from the finder groups (Df-2).](figures/b2_dev_lnr.pdf)

![Pile-up groups per trial against the rung. The figure shows the development direct count (C1 ρ = 1, 16,000 trials, Poisson errors; none at R08–R09), repaired thinning (C1 ρ = 2, 2,000 trials, bootstrap errors; one point at R08 from four passing subsets) and the occupancy model in the two day-15 readings: (i) one scale fitted on R04–R07, and (ii) the B2-b model with its R04–R05 normalisation. Both occupancy readings carry the same asymmetric error bar, the development-bookkeeping width s_tot of §6.2, which would apply only to a submitted estimator; both readings are above the cap, so their R08–R09 values are rule-1 projection input only, with no credit. The dashed segment at R08–R09 is the no-credit value of the term (485 events at N_trig = 4.0848×10⁷, i.e. 1.19×10⁻⁵ per trial). The R09 values use the fit-probability fraction of the development R06 finder groups.](figures/b2_dev_rates.pdf)

![Effective count N_eff = 1/s_boot² of the repaired-thinning prediction per rung and crossing rung (notation above), on 1,000 ρ = 2 events (filled) and projected to the 3,000-event production (open, ×3). The dashed line is the N_eff at which the thinning error s_P alone equals the evaluability limit ln 1.5/3; whether a rung is evaluable also depends on the direct count (§3.4). R08 has N_eff ≈ 4 (four passing subsets in 128,000). N_eff carries no error bar because it is itself the inverse squared bootstrap error.](figures/b2_dev_neff.pdf)

## 10. Self-check (corrected in v2)
- Frozen definitions used as written: [SD4], thinning unit, K = 64, §4.0 points 2–7, K = 13. No criterion is reworded, and
  every open choice is reported under each reading: s_model rung set, C trend, N_cfg weights, day-15 reading (i)/(ii),
  width bookkeeping (last test R06/R07), zero-count bound at day 15, slope weights. The model definition was frozen before
  any comparison (10:56).
- **Remediation (corrected, DOR B7):** thinning has one bug search (R0), one control (R1) and two remediation attempts
  (R2, R3). **The occupancy model has variants and diagnostics (O1–O4) and no remediation attempt.** That is fewer than
  the JFC's three, deliberately: a remediation chosen after R06 would violate the freeze, and rule 2 routes the attempt
  through a cause investigation (ADV-A A1). No scale factor was applied, and no parameter was tuned to a direct count beyond the
  declared R04–R05 (B2-b) and R04–R07 (day-15 reading (i)) normalisations.
- Formulas: z*, δ, the Poisson layer probabilities, s_tot — derived or cited, with limiting-case checks (§4.1, §6). IS
  checked against plain MC, now with power at R08 (§4.2). The same-sign offset is stated as a possible IS bias, and the
  error is quoted from the fresh run's per-toy variance (cycle 2).
- JFC alarm bands: thinning (b) χ²/ndf 242–346, alarm; occupancy held-out pull 10.6σ (statistical), alarm. Both are
  reported as closure failures (A1), not reframed. The JSON flags (`above_cap: true`, `b_verdict: FAIL`) agree with this text.
- Blinding: no signal file opened. Numbers tagged.
- JFC "≥ 2 selection approaches", MVA, cutflow, data/MC: **not this work package** (T2 / consolidation; no collider data).
- Plotting: mplhep CMS style, (10, 10), "Private work (simulation)" without experiment name, PDF + PNG, explicit yerr, no titles,
  x-axis labels, legends in empty regions. **Linter:** `conventions/lint_plots.py` resolves to
  `tools/jfc/src/conventions/lint_plots.py` (read-only; not edited). Its glob `*/src/*.py` misses `src/p3b/`. It was run
  through its own `lint_file()` on all 20 `src/p3b/*.py`: no violations [V, fixer log]. Making the glob recursive
  (`*/src/**/*.py`) needs a study copy or a tools/jfc change, which is flagged for the orchestrator.

## 11. Open issues
1. A1 / rule 2: thinning re-find variant waits for the user at the pause; occupancy cause investigation reports by
   30 Nov (§0.1, §8).
2. Shape crossing rungs (R15–R20 ⊗ R06) not computed (§7).
3. `occmod-000`'s first attempt read 19 of 20 density files; it was re-run with `--force` and its first output replaced.
4. The development direct rate at R07 (7 / 16,000) is below v1's (35 / 48,000) by 1.07σ (MAT l.64). The B2-g R07
   evaluability and the width column of §6.2 depend on it.
5. `p3-b-thin` jobs started after 10:56 record a different `thin_core.py` sha256 (column names moved to `cols.py`, no
   logic change). The remediation variants were appended to `thin_core.py` after the campaign (diagnostic code path only).
6. **[L15] standing limitation (DOR C3; COM l.351):** both estimators, the model's correlation factors and the direct
   counts come from the same chain, so no B2 closure verdict can see the half-turn limit [L15] (EXP §9 item 7).
7. B3 / B-new-1 (§4.2): the MC error at R08 is ≈ 22 % (R09 ≈ 26 %) [E], both lower bounds, with a possible downward IS bias of ≈ 3–13 % at R08 (plain truth/stored 1.13 ± 0.17). A ±5 % plain check would need ≈ 9× the plain toys (≈ 8 CPU-h [E]); it is not needed while these numbers are no-credit projection input.
8. LIV C-6, not applied in cycles 2–3 (it needs a plot job and none is allowed): draw the R08/R09 occupancy points of `b2_dev_rates` in a distinct "no credit" style (no bars, or hatched), and tighten the y ranges (rates 10⁻¹¹–10⁵, N_eff 1–10⁷). Carried to the next plot run; the caption disclaimer stands.
9. The DAILY_NOTES line of 14:20 and LOG.md l.1011 inherit v1's "cause identified for both" (DOR B6). A correction
   line was appended to DAILY_NOTES. LOG.md belongs to the orchestrator and is flagged, not edited.
10. ODD C-5: `pileup_term.py` (edited in cycles 2–3 to write `mc_rel_error_c2`) has not been rerun; rerun it once at the next worker job and diff `pileup_term.json` (expected: no change).
