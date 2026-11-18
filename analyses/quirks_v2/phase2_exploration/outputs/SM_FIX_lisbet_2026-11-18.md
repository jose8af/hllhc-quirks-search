# SM family (v) with clustered widths: amendment E4, pending the user's approval, after the result

Fix agent Lisbet, 2026-11-18 12:40 -0500. Ticket: `phase2_exploration/REGRESSION_TICKET_SM.md` §3. Ruling: `LOG.md`
2026-11-18 12:29 (Kestrel). Code: `phase2_exploration/src/c1_compare.py` at commit
**54610b6f0df2e1f1df2a3eb0c82740524ea16570** (sha256 5305c5de…8106, unchanged since). Tests:
`src/test_c1_compare.py`, 11/11 pass on synthetic clustered data. Result:
`outputs/c1_compare_sm_v2width_lisbet_2026-11-18.json`. Command (landau, nice 19, 10 s wall, 4.3 CPU-s, 342 MB):
`c1_compare.py --families sm --out <that file>` (defaults: `--nboot-cl 2000`, seed [C.SEED, 5]). All numbers below are
VERIFIED from that file. The inputs were unchanged: p2-a-c1-sm (50 jobs) and p2-a-c1-smregen (2,000/2,000 MET match).

## Frozen verdict on record: FAIL (unchanged)
The frozen script uses the width 1/√(weighted candidate count). The same run reproduces it exactly:

- R04: z +3.64, which is below p = 0.05/41, so the entry FAILS.
- R05: z +3.00, R06: z +0.70.
- Family coherence: z +4.60, NOT coherent. Σz² = 22.76.

This is stored as `frozen_script` in the new JSON. `c1_compare_sm_ignatius_2026-11-18.json` is untouched.

## Corrected values (amendment E4, pending the user's approval, after the result)
- **v2 width:** an event bootstrap of x_e = w_presel × n_cand(R) over all 2,000 events, with events that have no
  candidate counted as zero. R04–R06 use the same 2,000 replicas and none is dropped. Σx_e reproduces sm_term's N
  exactly (the code checks this).
- **v1 width, primary:** v1's 1/√N × the v2 inflation of the same entry (ESTIMATE).
- **v1 width, alternative:** 0, the strict bound.

| rung | v1 → v2 | ln ratio | v2 s_ln (inflation vs 1/√N) | primary: v1 s_ln, z, p, 2σ shift | v1 width 0: z, p, 2σ shift |
|---|---|---|---|---|---|
| R04 | 19.52 → 20.03 | +0.026 | 0.0522 (×10.4) | 0.0529, +0.35, 0.73, 16 % | +0.50, 0.62, 11 % |
| R05 | 4.509 → 4.713 | +0.044 | 0.0538 (×5.2) | 0.0550, +0.57, 0.57, 17 % | +0.82, 0.41, 11 % |
| R06 | 0.0162 → 0.0191 | +0.167 | 0.2248 (×1.39) | 0.2445, +0.50, 0.61, 94 % (gross check only) | +0.75, 0.46, 57 % (gross check only) |

**Family coherence (joint replicas).** The v2 correlation is 0.98 between R04 and R05, and 0.14–0.17 between R06 and
the other two.

| v1 width | family mean of ln ratio | z | coherent | block χ² (3 dof) | p |
|---|---|---|---|---|---|
| primary | +0.038 ± 0.075 | +0.51 | yes | 1.53 | 0.67 |
| 0 | ± 0.053 | +0.73 | yes | 3.19 | 0.36 |

The ± values come from the joint covariance. If the rungs were treated as independent, they would be 0.053 and 0.037,
which understates them.

**Verdict under E4:**
- 3 of 3 entries pass individually, with either v1-width choice.
- The family is coherent.
- R06 is a gross check only, because its 2σ detectable shift is above 50 %.
- The SM contribution to the global χ²₄₁ is 1.53 (primary) or 3.19 (v1 width 0), against 22.76 as frozen.

**Power.** The row can detect a hard-scatter shift of about 11–17 % at R04–R05 at 2σ. It cannot validate the port
below that level. This agrees with the ticket's estimates of ≈ 15 % and ≈ 87 %.

## Notes
- The block χ² is larger than the sum of the individual z² (0.71). R04 and R05 are 98 % correlated, but their ratios
  differ by 0.018, and the decorrelated form counts that difference. This is expected, not a defect.
- The v2 bootstrap width at R04 is 0.0522. The ticket measured 0.0505 with a different seed and script. The two agree
  to 3 %, which is within the bootstrap and estimator spread.
- C′_PU (iii) was not run: its inputs are incomplete. The channel (i) successor runs it with commit 54610b6.
- The user decides whether E4 is approved (DECISION notice, reply due Fri 20 Nov 12:00) and which v1-width choice is
  quoted. Until then, the FAIL above is the verdict on record.
