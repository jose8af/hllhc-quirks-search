# V4-5 (C2-a) amendment E2 part (ii): restricted brute-force scan — executor Ignatius (channel (i)), 2026-11-18

Criterion (COMMITMENTS "Amendments E1–E3", row C2-a; amended by the user on 2026-11-17 AFTER the frozen results were
known; labelled as such): "(i) as frozen, F0 against the independent fit; (ii) the same exhaustive 0.2 mrad scan
restricted to F0's inlier hits and the hits within 3σ of the F0 plane, |Δn| < 1 mrad in ≥ 48 of 50 per half; the
unrestricted and global scans reported without a criterion. **If (ii) also fails: (i) alone is the accuracy test and
the scan is reported as failed.**"

Campaigns (landau slot B, all jobs done with markers): `p2-a-c2-v45rtest` (2-job code test, not in the verdict),
`p2-a-c2-v45rpu` (3 jobs: the same 50 PU-only trials as Rosalie's p2-a-c2-v45pu), `p2-a-c2-v45rsig` (3 jobs: the same
50 signal + PU events as p2-a-c2-v45sig, first F0-accepted events in file order, R04 open bit only). Code:
`src/v45_bruteforce.py --restrict` (definition in its docstring, written before the runs); summary
`src/v45r_summary.py` → `outputs/v45r_summary_ignatius.json`. All numbers VERIFIED from that JSON.

## Hit set as implemented
Window hits (the road ∩ |u·n₂| ≤ 75 mm pool of the frozen scan) with |u·n_F0| ≤ 3 s_i(n_F0) (s_i: the score's
per-hit resolution), united with the pool hits that form the finder's stored hit record of the F0 candidate (`hit.*`,
matched by position within 1 µm). Score, grid (3001 × 3001 normals, 0.2 mrad, ±0.3 rad around n_F0) and band
accumulation are those of the frozen scan; no global scan in this mode.
- Restricted set: median 70 hits (47–100) PU, 76 (42–151) signal.
- F0's stored record found in 9 / 50 PU trials and 28 / 50 signal events (the store keeps records only for some
  candidates); where found, **every record hit was in the pool and inside the 3σ band (0 outside, all halves)**, so the
  union equals the band in every event, and the events without a record are treated identically.
- Checks: hit pool reproduced 50 / 50 and 50 / 50; band vs direct sum on a 41 × 41 sub-grid: max relative difference
  3.4×10⁻⁵; optimum on the grid edge 0 / 100.
- Permission note: a direct listing of the npz key names of one signal file (to see whether signal outputs carry hit
  records) was refused by the permission system on 2026-11-18 ≈ 12:20 and not worked around; the measured result above
  (records found in 28 signal events, all inside the band) makes the question moot for this verdict.

## Result

| half | (i) F0 vs independent fit, \|Δn\| < 1 mrad | (ii) F0 vs restricted brute-force optimum, \|Δn\| < 1 mrad | (ii) as amended (≥ 48 / 50) |
|---|---|---|---|
| PU-only (50) | **50 / 50** (max 0.64 mrad) | **46 / 50** (median 0.42, max 3.60 mrad) | **FAIL** |
| signal + PU (50) | **50 / 50** (max 0.85 mrad) | **46 / 50** (median 0.42, max 2.04 mrad) | **FAIL** |

**Verdict under amendment E2: part (ii) FAILS in both halves; by the amendment's own wording, (i) alone is the accuracy
test (PASS, 100 / 100) and the brute-force scan is reported as failed.** Decision point 1 input.

Power (STR §4.2 [E, script [13]]): at a true agreement of 90 % the probability of ≥ 48 / 50 is 11 %, at 98 % 92 %; the
observed 46 / 50 (92 %) in each half is the outcome expected for a true agreement rate near 90 %.

## The 8 disagreements (inspected, as STR §4.2 asks)
PU (file, trial, |Δn(F0, opt)|, |Δn(F0, fit)|, |Δn(opt, fit)|, score F0 → opt, hits):
c1pu1-0000 t2: 3.60, 0.18, 3.61 mrad, 34.6 → 35.7, 65; t10: 1.08, 0.16, 0.92, 42.8 → 44.4, 84;
t25: 1.70, 0.11, 1.61, 49.9 → 51.7, 89; t39: 1.13, 0.01, 1.12, 44.1 → 45.0, 78.
Signal (identifiers omitted): 2.04 / 0.11 / 2.11 mrad (score 46.0 → 46.3); 1.26 / 0.06 / 1.27 (33.7 → 36.8);
1.08 / 0.33 / 0.76 (54.9 → 55.6); 1.40 / 0.85 / 0.55 (49.3 → 52.0).

Reading (no verdict change): in all 8 the independent least-squares fit agrees with F0 (≤ 0.85 mrad) and the
restricted optimum lies 0.55–3.6 mrad from BOTH F0 and the fit, at a score higher by 0.4–3 units out of 35–55. The
resolution-weighted Gaussian inlier count with t_tol = 30 µm is not smooth on the 0.2 mrad grid even on the plane's own
≈ 70 hits: a rotation of ~1–3 mrad about the PV can bring one or two hits at large radius into their ±1σ core while
losing little elsewhere, so the score maximum is not the least-squares plane. In 4 of the 8 (PU t10, t39; the third
and fourth signal events listed) the steepest-ascent local optimum from n_F0 is that same cell, so even the score's
own local maximum is ≥ 1 mrad from F0 there; in the other 4 the local optimum is 0.28–1.70 mrad from F0. The failure is a property of the score used as the reference,
not evidence of an inaccurate F0 plane (which the fit tests directly).

**Phase 1 assumed** (and amendment E2 (ii) still assumed) that restricted to the plane's own hits the maximum of the
resolution-weighted inlier count coincides with the plane to < 1 mrad. **Phase 2 found** that it does in 92 % of the
events per half; in the other 8 % it sits 1.1–3.6 mrad away from both F0 and the least-squares fit. **Implications:**
C2-a rests on (i) (100 / 100); the brute-force cross-check is reported as failed, with this explanation.
