# P3B critical re-review, cycle 3 (1-bot, Phase 3; last cycle before escalation): work package p3-b (B2 pile-up)

Reviewer Oddvar (Opus, critical reviewer, fresh to this artifact). Session 15:32-15:4x -0500 (`date`); session log
`phase3_selection/logs/reviewer_oddvar_2026-11-24_15-32.md`. I opened no signal sample. No job on a worker, no git.

**Artifact:** `outputs/P3B_PILEUP_v3_ivar_2026-11-24.md` ("v3"), read in full (540 lines). Also read: LIV
(`review/critical/P3B_CRITICAL_REVIEW_v2_liv_2026-11-24_15-24.md`, `liv_ischeck.json`), ADV + Addendum 1, KET, the
binding rules (AGENT_RULES, CLAUDE.md overrides, PHASE3_BRIEF, `agents/critical_reviewer.md`, 06-review §6.3-6.4),
`src/p3b/is_check_c2.py`, the cycle-2 parts of `src/p3b/pileup_term.py` (l.15-30, l.70-130),
`outputs/p3b/{pileup_term,is_check_c2,is_check,is_check_stats}.json`, `SCHEMA.md`, the fixer log (cycle-2 part),
`experiment_log.md` l.225-240, the frozen projection script `phase1_strategy/src/strategy_budget.py` l.60-72,
l.568-625, l.655-690, and STR l.950-956, l.1012-1020, l.1170-1200, l.1584-1590, l.1870-1882, l.2350-2355, l.2757-2761,
COM l.36-39.

Tags: [V] I re-derived it (command or file cited); [U] taken over without a check; [E] estimate.

## 0. Verdict

**ITERATE (narrow, text only).**
- **B-new-1: RESOLVED** as LIV specified it (a)-(e). The script reproduces its JSON bit for bit, and the text, JSON and
  SCHEMA agree (§1).
- **A1** is stated with the binding status and nothing more. It stays deferred to the rule-2 process (§3).
- **New findings: A 0, B 1, C 6.**
- **B-new-2** comes from the cycle-2 fix itself. v3 says the frozen script "censors the term" at 485 events and that
  without credit every R08+ candidate "carries ≥ 485 events". The frozen script does neither. It takes the minimum of
  the term and a random draw (N_trig/96,000)·Exp(1), whose mean is 426 and whose 68 % value is 485.
  - The fix is a text edit at six places, with no compute and no new number beyond the four of §2.1.
  - The C items can go into the same edit.
- This is cycle 3 of a 1-bot review, so by CLAUDE.md ("1-bot: … escalate after 3") the ITERATE escalates.
- **What the escalation is about:** one text correction of how a frozen mechanism acts. The correct reading
  strengthens v3's conclusion (with or without credit, the R08 term sits at the no-credit scale). Every number, flag
  and decision route in the artifact stands.

## 1. B-new-1 — RESOLVED (evidence)

| LIV fix | v3 | check [V] |
|---|---|---|
| re-run | — | `is_check_c2.c2_errors()` re-run on einstein (`nice -n 19 python3 -I`, wrapper in the scratchpad, without `--patch`, so the artifact's file is not overwritten): 0.06 s user, max RSS 18 MB; the output dict **equals** `outputs/p3b/is_check_c2.json` (Python `==` True). |
| durable inputs (C-4) | `is_check_inputs/ischeck-{0,1,2}.npz` | sha256 `e7043195…`, `b929491b…`, `5a124e5a…` = SCHEMA.md l.71. `rel_toy_fresh(R08)` from the copies = 0.0686813816494104 = `liv_ischeck.json` (computed from the maxwell originals), so the copies hold the same data. |
| (a) 8.7 % a lower bound; ≈ 22 % | §4.2 l.261-273 | rel_toy stored 0.08636, fresh 0.06868, per-toy variance ratio 6.3247, rel_stored_c2 = 0.06868·√10 = **0.2172**; R07 ratio 1.952, 0.0571 (JSON). The configuration-sampling sentence of v2 is withdrawn (l.271-273). |
| (b) direction | l.23, l.279-292 | plain/stored 1.0456 / 1.0803 / 1.1349 at R06/R07/R08 (JSON) = "+4.6 / +8.0 / +13.5 %"; fresh/stored 1.034 (`is_check.json`). |
| (c) 22 % / 26 %, ±75 / ±96 | §0 l.88, §4.2 l.293-295, §6.1 l.378-379, §8.8, §11.7 | √(0.2172² + 0.1450²) = 0.2611 (JSON 0.261143); 347 × 0.217 = 75.3, 443 × 0.217 = 96.3; R09 4.11 × 0.261 = 1.07, 5.25 × 0.261 = 1.37. All as quoted. |
| (d) no-credit crossing | l.25, l.88, l.296-297, l.380-381, l.435-437, §8.8 | 443.31 × 1.1349 = 503.1, 346.95 × 1.1349 = 393.7: **arithmetic right, wording wrong → B-new-2** |
| (e) JSON | `mc_rel_error_c2` | present on R08, R08x2S>=3 (0.21719) and R09, R09x2S>=3 (0.26114) of `pileup_term.json`. The v2 keys are unchanged against LIV §4's v2 table: `mc_rel_error` 0.0722, `mc_rel_error_b3` 0.149, events 346.95 / 443.31 / 4.11 / 5.25, s_model 0.3548 / 0.5058 / 0.5357. I take the "4 added, 0 changed" diff from the fixer log [U]; without git I can only check it against LIV's v2 values, which match. SCHEMA.md l.65-71 documents the key and marks `mc_rel_error_b3` superseded. |
| C-7 ESS | l.267-268 | per seed 11.4–43.1, total 195.2 (JSON); 800 × 200 = 160,000 toys per seed. |

**Propagation.** I grepped v3 for 15 %, 21 %, ±52, ±66 and 0.149. They appear only in the two history rows (l.47 and
l.64, both marked "superseded in v3") and in §4.2 l.301 (named as the superseded key). The "7 instances" of l.36 are
l.47, l.64, l.88, l.293-295, l.378-379, l.486 and l.536. Nothing stale remains.

**Other v2 → v3 changes, checked:**
- C-1: l.103-105 is verbatim STR l.2759-2760, and COM l.38 is Q3.
- C-2: reading (iii) gives 443.31 × 1.0305 = 456.8 ("457"). C(R06)/C(R05) = 1.2436 / 1.2068 = 1.0305.
- C-3: §7 l.460-465 carry the KET qualifier at both places, and v3 nowhere calls `dev.pu1` "statistically
  independent" (grep "independent": no hit on `dev.pu1`).
- C-5: l.428-432 match the STR §4.12 table rows l.1877-1878; the case is flagged, not chosen.
- C-6: carried as open issue 9 (deferred by ruling, not counted).

## 2. New findings

### Category A
None.

### Category B

**B-new-2. The frozen censoring of the pile-up term is mis-stated, in the summary that decision point 2 reads.**

Where: change table l.25; §0 l.88; §4.2 l.296-297; §6.1 l.380-381; §6.3 l.433-437; §8.8 l.486.

What v3 says:
- "reading (ii) at the plain central value is 503 events, above the no-credit value 485, **where the frozen script
  censors the term**";
- "under either no-credit reading every R08+ candidate carries **≥ 485 events** of pile-up";
- "Even with a credit, reading (ii) reaches the no-credit value within its MC error".

What the frozen texts say [V, read]:
- `strategy_budget.py` l.585-587: `x = min(x, … -capv * rnd.expovariate(1.0))`, with `PU_CAP = -NTRIG/96000` (l.678),
  used for every pile-up term (`PU9`, l.690, l.749-750). `PU_NC` = 485 (l.677) is only printed.
- STR l.1586-1588: "bounded … by its no-credit value …, drawn like every other zero-count term: N_trig·λ/96,000 with
  λ ~ Gamma(1) in each pseudo-experiment (68 % value 485 events)".
- STR l.953-954 and l.2353: "censored at the predictive draw of its no-credit bound, 426 × Exp(1)".

So no threshold sits at 485. The censoring acts in every pseudo-experiment, against a draw with mean 425.5 and median
295. Without credit the term is that draw. It is not "≥ 485" (485 is its 68 % value, as v3's own l.416-417 says).

What it changes [V: own toy, Python standard library, 4×10⁵ draws, width 0.822; width 0.885 or 0.427 changes the
numbers by ≤ 2 %]:

| R08 median | 347 (i) | 394 (i, plain) | 443 (ii) | 503 (ii, plain) | no credit |
|---|---|---|---|---|---|
| fraction of pseudo-experiments censored | 0.565 | 0.600 | 0.635 | 0.670 | — |
| mean contribution, events | 241 | 256 | 270 | 286 | 425.5 |

- The censoring already binds in most pseudo-experiments at the **stored** central values, under both readings.
- The +13 % plain shift moves the censored mean by only +6 %. It does not "reach" a threshold.
- The credited term is worth ≈ 0.57–0.67 of the no-credit term, not 347/485–443/485 = 0.72–0.91 as the text implies.
- The 22 % MC error therefore matters less than §0 suggests, and the gap between reading (i) and reading (ii) is
  ≈ 12 % in the projection, not 28 %.
- The headline does not change: the R08 term is at the no-credit scale with or without a credit.

Why B and not C: the sentence states how a frozen rule acts, sits in the §0 table that decision point 2 reads, and is
the stated consequence of the cycle-2 fix. In the notice or the daily report it would tell the user that a threshold
exists where the frozen projection has none. (LIV's fix (d) used the same words, so the cycle-2 reviewer carries part
of this.)

Fix (text only):
- Replace "where the frozen script censors the term" by the per-pseudo-experiment description, with STR l.1586-1588
  and `strategy_budget.py` l.585-587, l.678 cited.
- Replace "carries ≥ 485 events" by "enters as the predictive draw N_trig·λ/96,000, λ ~ Gamma(1) (mean 426, 68 % value
  485)".
- Optionally quote the four censored means above, tagged [E, toy], or have p3-a quote them from the frozen script.
- Check SCHEMA.md l.37-38 ("censored at the no-credit value as the frozen script does") for the same ambiguity.
  `pileup_term.json`'s `no_credit_value.note` is already correct.

### Category C

**C-1. The plain interval is mis-computed.**
- Where: l.23, l.24, l.88, l.279-280, l.292, l.294, l.380, l.536.
- 45 passes give a relative error of 1/√45 = 0.149 on plain. On truth/stored that is ±1.135 × 0.149 = **±0.169**.
- The interval is therefore **[0.97, 1.30]** (Gauss), or [0.966, 1.330] (Garwood 68 %), i.e. **+30 % / −3 %** (Garwood
  +33 %). v3 has "1.13 ± 0.15", "[0.99, 1.28]" and "+28 % / −1 %" [V arithmetic]: the relative error was applied as an
  absolute one. LIV's text has the same slip, but `liv_ischeck.json` has `rel_err_plain_over_stored` = 0.172.
- l.294 calls the symmetric ±22 % and the plain interval "equivalent". They are not. Say "or, from the plain check
  alone".

**C-2. The fresh IS also under-samples the tail; v3 states this only as a condition ("if", l.266).**
Own check [V, scratchpad `oddvar_rank.py`, standard library, on the durable npz]:
- The 64 configurations with the largest **stored** R08 values hold 51.1 % of the stored sum, but only 1.4 % of the
  fresh sum and **0 of the 45 plain passes**.
- The fresh top 64 hold 31.6 % of the fresh sum and **1** plain pass, where ≈ 13 would be expected (Poisson
  P(≤ 1) = 3×10⁻⁵).
- The per-configuration correlations are 0.014 (stored–fresh) and 0.023 (fresh–plain) (`liv_ischeck.json`).
- Conclusions:
  - The 22 % is a lower bound, not "possibly" one.
  - At R08 the per-configuration IS values are noise. The "top 1 % carry 51 %" and "effective number of
    configurations 129" (l.268-269) describe the toy noise of the stored run, not the configurations.
  - The 0–1.6 % configuration-sampling figure, which comes from covariances of these noisy estimates, has little
    power.
- Suggested wording: the only unbiased constraint on the stored value is the plain one, truth/stored = 1.13 ± 0.17.
  Put `plain_over_stored` and its error next to `mc_rel_error_c2` in the JSON or SCHEMA.
- No compute is needed. IS stays primary (frozen 10:56).

**C-3. Pulls are quoted with the lower-bound errors.**
- l.282: R07 plain/stored is "1.9σ with the toy-level errors". That uses the 4.1 % that v3 itself now calls a lower
  bound. With v3's 5.7 % it is **1.4σ** [V: 0.0803/√(0.0122² + 0.0571²)].
- l.289: "Each pull alone is below 2σ". R06 is 1.046 ± 0.019, which is **2.4σ** with the plain error alone, and 1.5σ
  with the stored 2.4 % added.
- State which errors enter each pull.

**C-4. JSON coverage of the new key.**
- (a) `mc_rel_error_c2` sits under `occupancy_day15` (reading (i)) only. §0 says both readings scale with it, but
  `occupancy_B2b_model` (reading (ii)) has no error key. SCHEMA's main table (l.30) still presents `mc_rel_error`
  (0.072) as "the" MC error, without a pointer to the cycle-2 section.
- (b) The R08x2S>=3 and R09x2S>=3 values are the R08 value copied over (`is_check_c2.py` l.104-106). The paired check
  was not run with the 2S requirement, so tag this as a transfer [E].
- (c) Neither text nor SCHEMA says whether p3-a adds the MC error to the projection width. The frozen s_tot has no MC
  term (STR §4.0 point 7). Under B-new-2's numbers it hardly matters, but say it.

**C-5. `pileup_term.py` with the c2 import has not been run.** The fixer log 15:30 says "syntax-checked; not run". The
JSON key came from `is_check_c2.py --patch`. Run it once at the next worker job (`pileup_term.py` + diff of the JSON);
no new job is needed for this.

**C-6. Numbering of §11:** the items run 1–7, 9, 8. Cosmetic.

**(Deferred, not counted: LIV C-6, figure style.** It is carried as v3 open issue 9. It is neither A nor B: the caption
disclaimer stands, and the R08/R09 error bars are labelled as hypothetical bookkeeping.)

## 3. A1 — binding status only [V, read]

- §0.1 (l.92-116) states:
  - the failure plainly: thinning (b) 4,839/14; occupancy pull 10.6σ = 0.3548/0.03354;
  - "blocks B2 until rule 2 has run";
  - rule 1 "Not met now", with the ADV point 1 status as updated by ADV-A A5 ("PRELIMINARY, reviewed: …; rule 2
    running");
  - thinning in ADV-A A3 wording, occupancy in ADV-A A1 wording ("no cause demonstrated"; never "identified");
  - "Who resolves A1: the orchestrator … it does not close A1".
- §8 l.472-481 repeats the same routes. JSON: `both_estimators_above_cap: true`, `above_cap: true` for both
  estimators.
- No reframing, no closure claim, no remedy of v3's own. ADV point 8 "must not" list: nothing is launched, PREREG and
  COM are untouched, and nothing is chosen on the development R06/R07.

## 4. Full pass: other checks with no finding [V]

- §0 / §3.2 / §4.3 / §6.2 numbers against the JSON:
  - e^0.773 = 2.17, e^0.355 = 1.43;
  - 4,839/14 = 346 and 3,392/14 = 242 (§10 "242–346");
  - R07 σ_tot √(1/42 + 1/683) = 0.159 and v1's √(1/70 + 1/683) = 0.126;
  - widths √(0.135² + 4·0.405²) = 0.822 and √(0.355² + 4·0.405²) = 0.885;
  - 4.0848×10⁷ × 1.14 / 16,000 = 2,910.4; 16,000 + 5,960 × 4 = 39,840 trials;
  - R09 (i) 346.95 × 0.011851 = 4.11; f = 47/3,966 = 0.011851 and √((1 − f)/47) = 0.1450;
  - no-credit `events_zero_count_68` = 485.07 and `events_mean` = 425.5.
- Quotations checked against STR: l.2759-2760 (C-1); l.1177 "485 events … no selection beyond R07 is then eligible
  ([SD8])"; l.1878 "both pile-up estimators FAIL". All verbatim.
- Blinding: `is_check_c2.py` reads only the p3b JSONs, the check npz and `p3-b-occmod`, so no signal input [V, read].
- CPU: cycle 2 adds ≈ 0 (my re-run took 0.06 s), so the total stays ≈ 5.8 of 15 CPU-h. My own use: < 1 s on einstein
  (nice 19), plus two standard-library toys under 10 s.

## 5. What a competing group would have

A competing group would have a pile-up term that closes. That is A1, owned by rule 2 and outside this cycle. Within
this cycle's scope: an IS error at R08 backed by a check that does not rely on IS. v3 has that check (45 plain
passes). C-1 and C-2 ask only that it be quoted as the primary constraint and with the right arithmetic.
