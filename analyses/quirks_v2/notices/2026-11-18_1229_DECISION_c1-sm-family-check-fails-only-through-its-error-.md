# [DECISION] C1 SM-family check fails only through its error width: approve amendment E4 by Fri 20 Nov 12:00

Written 2026-11-18 12:29 -0500 by the orchestrator. Current status: `analyses/quirks_v2/STATUS.md`.

# C1 SM-family check fails as frozen because of its error width: approve amendment E4? (reply by Fri 20 Nov 12:00)

**What happened.** The C1 reproduction of v1 compares 41 quantities. One of them failed its frozen criterion: the
Z(νν) hard-scatter candidates per event at rung R04 are 20.03 in v2 against 19.52 in v1 (+2.6 %, z = +3.64, past the
Bonferroni limit |z| < 3.2). This blocks decision point 1 (21 Nov).

**Why (regression ticket, checked by an independent advisor).** The comparison script took its error from v1's code:
1/√(number of candidates). But each event carries about 47 candidates that are not independent, so this error is
about 10× too small. Measured event by event on the v2 sample, the error is 5.0 % at R04 (three methods agree).
With that error the difference is **+0.36σ** (R05 +0.60σ, R06 +0.53σ): a pass. Even if v1's own error is set to zero,
the largest is +0.85σ. The generator was checked and ruled out: same Pythia 8.312, same CP5 card, same generation code
as v1. Details: `analyses/quirks_v2/phase2_exploration/REGRESSION_TICKET_SM.md`.

**Caveat.** The corrected test is weak: it would detect a real 15 % shift at R04–R05 only half the time (2σ). The
verdict will be quoted with that power.

**The frozen text** fixes the formula and the thresholds, not this particular error. Still, the change turns a
recorded FAIL into a PASS after the result was known, so I bring it to you, as with E1–E3.

## Questions (defaults are my recommendation)
1. **E4: approve the event-level error for quantities counted per candidate** (family coherence from joint
   replicas). The frozen FAIL stays on record, labelled "after the result". *Default: approve.* Alternative: treat it
   as a plain bug fix.
2. **v1's error**, which cannot be recomputed (v1's per-event counts are lost): take v1's relative error equal to v2's
   (an estimate), and always quote the v1-error-zero values alongside. *Default: yes.*
3. **No second-seed rerun** (14.5 CPU-h, over the C1 budget, and it cannot test v1's side). *Default: no rerun.*
4. Count this as remediation attempt 1 of 3, and put the error model into PREREG_v2. *Default: yes.*

**Without an answer** the fix is made and computed anyway, but the SM family goes to decision point 1 as "FAIL
(frozen) / corrected PASS pending E4", and the block stays.

For information: the C′_PU family (not yet read) has the same error problem. Its correction is fixed and committed
**before** its numbers are read, which needs no approval.
