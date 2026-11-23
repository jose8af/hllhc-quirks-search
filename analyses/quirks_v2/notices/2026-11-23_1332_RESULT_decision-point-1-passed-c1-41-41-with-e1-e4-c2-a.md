# [RESULT] Decision point 1 passed: C1 41/41 (with E1-E4), C2 as amended; study continues

Written 2026-11-23 13:32 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

Written 2026-11-23 by the orchestrator. Decision point 1 was due on day 5 (Sat 21 Nov); the power loss (separate PROBLEM notice) delayed this report. **No action is needed from you for decision point 1 itself.**

**Verdict: decision point 1 is passed.** The v2 chain reproduces v1 where the frozen criteria require it (with amendments E1–E4, which you approved). The study continues as planned. All entries below are VERIFIED in `analyses/quirks_v2/LOG.md` (18–19 Nov).

**C1, the v1 reproduction: 41 of 41 comparisons PASS under amendments E1–E4.**
- Open comparisons: 35 of 35 pass (31 background, 4 open signal). The coherence check passes for every family.
- Sealed comparisons: 6 of 6 PASS, run blind by a separate agent. No number was decrypted or reported. The encrypted file's checksum is recorded (`ledger/sealed/`).
- Under the frozen text, one FAIL stays on record: the SM family at rung R04 (z +3.64). The cause was the error model, not the physics chain, and amendment E4 (approved 18 Nov) corrects it. Under E4 the SM family passes 3 of 3.
- Disclosure: the closure slope passes at the frozen seed (z −0.46). A 10-seed diagnostic scan gives z between −1.04 and +0.32, none beyond the 3.23 alarm. The fit's sensitivity to the R06 weight goes into PREREG_v2.

**C2, the v2 changes:**
- C2-a: part (i) PASS (50/50, 50/50). The restricted scan, part (ii), FAILED (46/50), so per amendment E2, (i) alone stands.
- C2-b: PASS.
- C2-c: PASS as frozen, but without power, since every family's pass fraction is exactly 0 or 1 (flagged).

**Still open, not blocking:**
- **C1-c container rerun: NOT TESTED.** The docker-build permission (DECISION notice of 19 Nov 11:19) still needs your answer; there is no default. The deadline is the Phase-5 review.

**Reach outlook vs the last report (19 Nov RESULT): equally promising.** No new background or reach number has been computed since 19 Nov (ESTIMATE, v1 placeholder efficiencies; no v2 signal efficiency looked at). The day-15 reading remains PRELIMINARY, not binding: B₅₀(R09) = 10,777, near-pass inclusive. This is a lower bound, valid only for an "above 300" verdict, and the validation (a)–(e) is not complete. It is a ceiling, not a background estimate. A pause is expected.

**Coming next:** a DECISION notice on shifting the calendar by the time lost to the power loss, once the compute checkpoint (also due day 5) is in.
