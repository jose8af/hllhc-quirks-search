# REVIEW_RESULTS_R3: narrow verifier of STAGE4_RESULTS.md + STAGE4_SUMMARY.json (after FIX_RESULTS_R2)

Reviewer: fresh critical reviewer (JFC), 2026-10-16. **Verdict PASS (0 A, 0 B, 2 C).** Nothing edited except this file.

## Checks
- Self-check re-run (`pixi run python acts/stage4/results/selfcheck_stage4.py`): **151/151 passed**.
- B-1 recomputed independently from `data/acts_stage4/investigation/inv_a2fc_e500_paired.json` (own script, own exact two-sided
  sign test):
  - R04, the 8 other revert points: numpy 382 -> full chain 318 (x 0.832), discordant 84 / 20, p = 1.638e-10. Matches the report,
    the JSON `paired_aggregate_other_8`, and §4.3. (A 9-key sum that includes a non-revert key gives the same 84/20.)
  - r_fb: 116 -> 101 (x 0.871), 52 / 37, p = 0.137; 7 of 8 per-point ratios <= 1; R14 50/33 (0.078); FB3 63/39 (0.022). All match.
- Estimate: 37.6 / 0.871 = 43.2 and 37.6 / 0.832 = 45.2. It is tagged "ESTIMATE (systematic on eps)" in §0, §4.3, §5, caveat 16
  and JSON `fullchain_eps_systematic`. `limits.json` is unchanged (mtime 12:29, before the fix), and every text mention says "not
  applied to limits.json". The headline numbers are unchanged: 37.6, B84 1.23e6 (7.05 decades), eps 9/200 with CP 0.030-0.065, WP
  branch fallback.
- §0 is honest and clear. It says "statistically unusual (global p ~ 1e-4 to 1e-3), no mechanism found", states the systematic
  loss at the other 8 points ("not noise"), says the null result is unaffected, and adds a plain reading. The ACTS quirk-noise
  non-replication is in §4.3 and caveat 16. The phrases "not a systematic shift" and "only genuine ... -5 %" are gone (grep clean).
  The remaining "-5 %" is correctly the net 64 -> 61 for row 268.
- C-1 to C-9 are all applied (read in §0, §4.3, §5, §6, caveat 16 and the JSON): CP is the full statistical uncertainty; the P2
  verdict leads with "no measurement"; "just above the 2 m_Q threshold (2.46 without PU)" and 29 % below 1.5 m_Q; bounds
  "1.4-1.7e5 individually, 3-4e5 together"; "gtrsim 10-11/200" with lower_bound=true; "(post hoc)" label; heading
  "What was measured at detector level"; the upper-side arithmetic (95 % CP ~20, exclusion needs eps ~1.7); "37.6 times larger".

## Category A
None.
## Category B
None.
## Category C (optional)
- C-1. §0 and §4.3 attribute the aggregate loss to "CKF hit stealing" as a fact. The investigation identified that mechanism
  directly only for row 268. For the aggregate it is an inference (one-sided R04 loss at points whose V4-6 CKF fraction exceeds
  5 %). Suggest "attributed to CKF hit stealing".
- C-2. Caveat 16 is titled "statistically fragile", and its first sentence says the E500 3 keV loss "is statistical". The same
  caveat then says "a conclusion by exclusion" and "no mechanism found". Suggest "attributed to statistics" for consistency with §0.

## Verdict: PASS
