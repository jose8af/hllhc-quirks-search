# [DECISION] Three Gate-A criteria fail as worded (E1-E3), answer by 20 Nov

Written 2026-11-17 09:37 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

**Three criteria frozen at Gate A fail as worded.** In each case the thing the criterion was meant to test is fine,
and the wording tests something else. A change of a frozen criterion is your decision. They bear on decision
point 1 (day 5, 21 November): by the strategy, a failed finder cross-check blocks it.

**Deadline: 20 November.** You can answer "E1–E3 as recommended".

## E1. Arithmetic check against v1's counts (C1-b)

- **Frozen:** central values to 10⁻⁶ and the 84th-percentile background within 1 %.
- **Result (VERIFIED):** central values agree to 2×10⁻¹⁶ on all 86 entries: PASS. The percentile is within 1 % on
  57 of 86; worst 3.4 %: **FAIL as frozen**.
- **Why:** v1 computed its percentile from 10⁵ random draws, which scatter by 0.1–3.6 %. Every difference is within
  1.8 standard deviations of that scatter. The tolerance is tighter than v1's own precision.
- **Proposed wording:** "within 1 %, or within 3 times v1's own Monte Carlo standard deviation". Passes as measured.

## E2. Finder cross-check (C2-a, V4-5)

- **Frozen:** the finder's plane within 1 mrad of (i) an independent fit and (ii) the best plane of an exhaustive
  scan within ±0.3 rad, in at least 48 of 50 cases, for pile-up-only trials and for signal-plus-pile-up events.
- **Result (VERIFIED):** (i) 50/50 and 50/50, worst 0.85 mrad: PASS. (ii) 0/50 and 6/50: **FAIL as frozen**.
- **Why:** at pile-up 200 the scan window holds 18–24 thousand hits, and every plane through the vertex has hits on
  nearly all layers. The scan's best plane is a different plane in all pile-up trials (median 237 mrad away).
- **Honest limit:** the executor's first alternative (the nearest local maximum of the same score) also fails,
  42/50 and 43/50. So no version of the unrestricted scan passes.
- **Proposed wording:** (i) as frozen; (ii) the same exhaustive scan restricted to the hits of the finder's own
  plane; the unrestricted scan reported without a criterion. Part (ii) is **untested**: about 1.5 CPU-h to run, and
  it may fail too.
- **Alternatives:** keep the criterion and report the cross-check as failed in the paper, lifting the block on
  decision point 1 yourself; or accept (i) alone as the accuracy test.

## E3. Likelihood check against v1's limit (T1-b)

- **Frozen:** the new likelihood with v1's inputs reproduces v1's toy limit of 789.7 within 10 %.
- **Result (VERIFIED; procedure committed before any toy was read):** 902 ± 32, outside the window by 1.5 units:
  **FAIL as frozen**, on a thin margin. Zero failed fits in 160,000 toys.
- **Why:** the likelihood agrees with v1 (asymptotic limit 828.7069 against v1's 828.7067; v1's own statistic with
  v1's seed is reproduced to 10 digits). But the limit sits on a jump of the test statistic, and the frozen toy
  recipe returns 704–963 from identical inputs. v1's own number scatters by 4.7 % between seeds.
- **Proposed wording:** (a) asymptotic limits agree within 1 %; (b) v1's statistic on the new inputs reproduces
  v1's number with v1's seed, seed scatter reported; (c) the new toy procedure's limit reported with its scatter, no
  tolerance. Passes as measured.
- **Consequence beyond this check:** the toy recipe itself needs a finer bracket and a rule for an empty tail
  before it is used for v2 limits. That goes into the pre-registration.

## My recommendation

Accept E1 and E3 as proposed. For E2, run the restricted scan (1.5 CPU-h) and decide on its result; if it also
fails, accept the independent fit as the accuracy test and report the scan as failed. In every case the frozen
verdicts stay on record as FAIL, with the amended criteria dated and labelled as amendments made after the result.

## Also still open with you

- Addendum decisions D1–D9 (notice of 16 Nov 18:33), by 18 November 14:00. The second part of the pilot is ready
  and can start the moment you answer.
- An exception to the 30-minute job rule for one generator comparison.

Files: `phase2_exploration/outputs/c1b_arith.json`, `phase2_exploration/outputs/V45_RESULT_rosalie_2026-11-17_08-13.md`,
`phase2_exploration/outputs/T1B_RESULT_flora_2026-11-17_09-35.md`.
