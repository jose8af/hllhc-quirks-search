# Rule-1 validation, items (a)/(a2), (c), (d): results

Ingvild (Fable 5.2, executor, rule 1(c)), successor of Cecilie (session lost in the power cut of 19 Nov 17:54).
Written 2026-11-23 15:13 -05 (`date`). Frozen plan: `RULE1_VALID_PLAN_cecilie_2026-11-19.md` (518cdab) and its addendum
(a2) (6013748), both committed before the data they describe. I changed no statistic and no classifier code.
Tags: VERIFIED = computed in this session from the file named (file:line); ESTIMATE; UNVERIFIED = transcribed.
Files: `C` = `outputs/rule1_valid_c_ingvild_2026-11-23.json`, `B` = `outputs/rule1_valid_b50_ingvild_2026-11-23.json`,
`A2` = `outputs/rule1_valid_a2_ingvild_2026-11-23.json`, `A` / `D` = `outputs/rule1_valid_{a,d}_cecilie_2026-11-19.json`.
No signal file was read; no efficiency was formed. PRELIMINARY: the binding reading is day 15.

## 1. Result

**The preliminary "above 300" reading stands, with the subset-pass count as well as with the finder count.**

| count m at R08 = R09 = R11 (4.7 mm, n = 7, k ≤ 3) | m_Z (full-weight class) | Z 0.05 class | every B1 class, HS, lowpt | B₅₀ at R09 [16–84 %] | B₅₀ at R08, pile-up 88 / 118 / 148 |
|---|---|---|---|---|---|
| subset pass, reading (S) (primary of the plan) | **1,501** | 13 | 0 | **63,170** [61,578–64,802] | 63,246 / 63,271 / 63,294 |
| subset pass, reading (F) (N_IT2 ≥ 3 required) | 1,474 | 13 | 0 | 62,037 [60,460–63,654] | 62,113 / 62,138 / 62,161 |
| finder near-pass (N), Tove (for comparison) | 253 | 2 | 0 | 10,777 | 10,855 / 10,878 / 10,901 |

- Counts: VERIFIED, `C:351-362` (S), `C:751-762` (F); by deficit k = 0 / 1 / 2 / 3: 26 / 80 / 318 / 1,077 (S, `C:364-369`).
  Tove's row: UNVERIFIED here (`RULE1_PRELIM_tove_2026-11-19.md` l.61; re-derived by Björn).
- B₅₀: VERIFIED as arithmetic, `B:109,146,183,220` (S), `B:529,566,603,640` (F); `p2t_rule1_prelim.py` unchanged
  (sha256 8b26f06b…, the hash Björn reviewed); empty-pilot check reproduced first (160.8; 238.3 / 262.3 / 283.8).
  ESTIMATE as physics, for Tove's reasons (v1 preselection, pile-up term from v1-based rows, M = 993,887 → 41.96
  events per count). Monte-Carlo error of the median 6–7 events (`B`, `mc_err`); three other seeds 63,170–63,180.
- **With and without flagged events: identical** (S 63,169.7 both, `B:109` and `B:319`; F 62,036.8, `B:529` and `B:739`).
  No row of a flagged event enters any count (`C` tables `*_with` = `*_without` at every width and s).
- **Advisor ruling (i)–(iii):** (i) m = the subset-pass count: 1,501 (S). (iii) G is not available, so B₅₀ is read at
  every T2 candidate that has a pile-up estimate (R09; R08 at 88 / 118 / 148): all four are above 300 (limit 299.1,
  `B` `limit`) and agree to 0.2 %. For the N_2S2 ≥ 3 candidates (R14 type, FB; n = 10, k ≤ 5) no pile-up estimate exists
  in the script and no B₅₀ is formed (as planned); their counts are m_Z = 969 (S) / 846 (F) (`C:389-400`, `C:789-800`;
  Tove 147), i.e. ≈ 4×10⁴ events from the Z term alone (ESTIMATE: 969 × 41.96) against a pause level of 4 counts.
  (ii) The classifier has **not** been reviewed by a second agent. Until it is, the binding stand-in remains the
  finder near-pass count as a lower bound (253 → 10,777). Both give "above"; nothing here is "below" or near 300.
- The subset-pass count is itself **exact or a lower bound** (plan S4: every subset found is a witness; the search
  inside a plane is not proven maximal; synthetic test T7 was not met as planned, 2 of 200 trials at 4.7 mm,
  Cecilie's log 15:40). Valid for "above" only.

## 2. (c) Subset-pass classification [VERIFIED]

Script `p2w_subset.py`, sha256 c68b7b69… in all 139 job outputs (`C` `script_sha256`), = commit 6d2c6f5.
1,083 pilot files, each classified exactly once and completely; event and flagged-event totals per term equal Tove's
(`p2w_valid_summary.py` part c stops otherwise); Z full-weight class 994,446 events. 0 job errors (`C:5`),
6.02×10⁶ (event, orientation) roads past the prefilter, 8.48×10⁹ seeds, 5.95×10⁵ aligned planes (`C:3-13`).

| width | m_Z (S), s = 0 | m_Z (F), s = 0 | Tove (N) | m_Z (S) / (F), s = 3 | B1, HS, lowpt |
|---|---|---|---|---|---|
| R04 (none) | 13,923 | 13,532 | 5,179 | 7,052 / 6,645 | DIF-C 1 |
| R05 (37.5 mm) | 11,566 | 11,220 | 4,881 | 6,224 / 5,870 | DIF-C 1 |
| R06 (18.75 mm) | 7,202 | 6,981 | 2,884 | 4,113 / 3,802 | DIF-C 1 |
| R07 (9.4 mm) | 3,781 | 3,668 | 1,076 | 2,212 / 1,964 | 0 |
| **R08 (4.7 mm)** | **1,501** | **1,474** | 253 | 969 / 846 | **0** |

(`C` tables `sub{S,F}_R0x_s{0,3}_with`.) The single non-Z row is the DIF-C event Tove found (file …c0-difc-0076, event
22,673, orientation 20: k = 3 at R04–R06, 4 at R07–R08; `C` `lists.non_Z_rows`): an off-road orientation, not flagged.

**Acceptance (fixed in the plan): k_sub(F) ≤ k_finder for every (event, orientation) of Tove's stored variant-0
candidates, four widths and R04, s = 0 and s = 3: violations = 0 of 22,790 comparisons** (`C:1112`; R08: 255 finder
near-passes at s = 0, 148 at s = 3, 0 violations, the subset k lower in 44 and 42; `C:1067-1078`). `p2w_partial_check.py`
on the full set gives the same table. Expected consequence holds: m_sub(F) ≥ Tove's (N) at every width.

What the factor 5.8 (1,474 against 253 at R08, reading F) is made of was not planned and is not decomposed here. The
two differences of the classifier from the finder are those of the plan: every IP-layer hit pair seeds a plane (the
finder: L4–L3 pairs with an L2 hit), and a narrower subset of a wide plane counts. Reading (S) adds 27 events (1.8 %).

## 3. (a) and (a2): positive control of the B1 path of `p2t_classify.py` (sha256 0d721341…, unchanged)

- **(a) as planned: NO POWER (not PASS, not FAIL).** D = 0 at every rung for DIF (47,538 events) and NI 22 (22,794),
  but v1's own C′₀ output has no R04 candidate (reference events with a candidate: DIF 0; NI 22 17 at R01, 0 at R04);
  the criterion needed ≥ 100 (`A:756-820`; read by Cecilie on 19 Nov, VERIFIED by me from the file only).
- **(a2) injection control (addendum, committed before the run): PASS.** Campaign p2-c-r1v-zb1 ran on 23 Nov (it had
  not run before the power cut). 43,498 re-packed Z(νν) events of 20 pilot files through the non-Z (B1) branch;
  reference = Tove's stored Z-branch candidates. **D2 = 0 with 350 candidate-holding events (≥ 100 required)**; 553
  candidate rows at orientation 0 on both sides, 14 columns compared, 0 finder errors (`A2:44-55`). Of the 350 events,
  14 hold an R04 pass and 25 an R08 near-pass. Information: the 20 other orientations hold 548,332 candidate rows
  (jets off the MET road); they are not part of the statistic.
- What this shows: the B1 branch (event record, PV, orientation loop, storage) returns the Z branch's candidates
  exactly, on events that have candidates at R04–R08; the link to v1 is exact where v1 has candidates (17 events,
  loose rungs). What it does not show: agreement with v1 at R04–R05 on a B1 topology (no such sample exists in C′₀).
  The zero of the B1 classes at R08 is therefore not an artefact of the branch.

## 4. (d) Power of the exact shortcut: PASS (Cecilie, 19 Nov; VERIFIED by me from the file only)

n_lost = 0; Z(νν): 350 candidate-holding (event, orientation), tables identical to Tove's; control: 49, tables with
and without the option identical (`D:123-130`). Criterion: n_lost = 0 with ≥ 300 → met on the Z sample (95 % upper
limit on the lost fraction 3/350 = 0.9 %); the control alone (49) would not meet it.

## 5. Deviations and incidents (none changes a statistic or the classifier)

1. **36 of 139 (c) jobs failed at start on 23 Nov and were rerun as p2-c-r1v-s3a / s3b.** All nic / nix jobs: numba
   `ReferenceError: underlying object has vanished` when saving the cache index of `subset_road`, at its first call,
   before any classification (log `…/logs/p2c/rule1_valid/p2-c-r1v-s2a/000/r1v-s2-nix-01.a1.log` l.4-48). Every job
   adds one entry to that index (the key holds the dispatcher of `refit_packed`); after 51 entries the save fails on
   both nodes. The runner does not retry a failed job, so the 36 were rerun with the same script and arguments and a
   new, empty `NUMBA_CACHE_DIR` (numba_s5); 36/36 done. The script hash is the same in all 139 outputs.
   For later campaigns of this script: one cache directory holds at most 51 jobs (or drop `cache=True` on `subset_road`).
2. `p2w_valid_summary.py` (part c) and `p2w_partial_check.py`: the input glob `s2[ab]` widened to `s[23][ab]`, before
   any (c) number was read. Nothing else changed (sha256 of the summary script now 26b6407a…).
3. The power cut killed 4 (c) jobs mid-run (2 + 2); the runner retried them (attempt 2), outputs verified by the
   '1083 files, none twice, none partial' guard.
4. Inherited from Cecilie (her log): first classifier version de-duplicated equal hit sets and lost one finder
   near-pass in the first 40 Z files; fixed in 6d2c6f5 before these campaigns; T7 not met (see §1).

## 6. Compute [VERIFIED from the markers, cpu + sys of every done / failed line]

| campaigns | when | CPU-h |
|---|---|---|
| ctl, ctlp, ctlq, zp, suba, subb, s2a/s2b (first 23 jobs) | 19 Nov (Cecilie) | 2.57 |
| s2a/s2b (rest), zb1 (1.17), s3a/s3b (0.13) | 23 Nov | 2.36 |
| **total rule-1 validation (a), (c), (d)** | | **4.93** (plan 2.8–7.6; stop level 10) |

Not in the markers (ESTIMATE): the 4 jobs killed by the power cut and the jobs stopped by Cecilie, ≤ 0.8 CPU-h (her log:
≈ 0.5 + 0.2); summaries on schrodinger ≈ 0.01. zb1 cost 1.17 against 0.2 planned (the 20 off-road orientations).

## 7. Open

- Second-agent review of `p2w_subset.py` (ruling (ii)); until then 253 / 10,777 is the stand-in lower bound.
- Readings S1–S5 of the plan are Cecilie's readings of text the strategy does not fix; they go to PREREG_v2.
- No pile-up estimate for the N_2S2 ≥ 3 candidates; G / best candidate not available (Tove A3).
- Björn's D4 (weighted m), D9 (54 of 253 with a secondary-product hit): not re-evaluated on the subset count.
- `qv2run rebuild-ledger` not run by me. Nothing of mine is running; node slots released.
