# PRELIMINARY rule-1 reading of the pilot (day-7 reading, done on day 3)

**PRELIMINARY. Information for the user, not a decision** (the day-7 rider was not taken, COMMITMENTS.md l.37; the
binding reading is day 15). Tove (Fable 5.2, executor, rule 1(c)), 2026-11-19 15:20 -05 (`date`).
Plan, committed before any pilot array was opened: `RULE1_PRELIM_PLAN_tove_2026-11-19.md` (commit 7648504).
Tags: VERIFIED = computed here from the files named; ESTIMATE = depends on a planning input or a provisional choice.

## 1. Result

**The preliminary B₅₀ is above the cap of 300 at every candidate, in both readings I could compute, with and without
the flagged events.** The whole excess is the Z(νν) term (the count that stands for every SM hard-scatter process and
the multijets). Every B1 class, the hard-scatter-parent sample and the low-p_T alarm sample are empty at R08.

| reading of "own-hit count" (plan A1) | m_Z (full-weight class) | B₅₀ at R09 [16–84 %] | B₅₀ at R08, pile-up 88 / 118 / 148 | vs 300 |
|---|---|---|---|---|
| (P) finder pass, k = 0 | 11 | **620** [482–784] | 697 / 721 / 743 | above |
| (N) finder near-pass, k ≤ 3 | 253 (+ 2 in the 0.05 class) | **10,777** [10,130–11,459] | 10,855 / 10,878 / 10,901 | above |
| empty pilot (reproduction check) | 0 | 160.8 | 238.3 / 262.3 / 283.8 | below |

- All B₅₀: VERIFIED as arithmetic (`rule1_prelim_tove_2026-11-19.json`; 10⁵ draws, the addendum's streams), ESTIMATE as
  physics (v1 preselection, provisional classification, pile-up term = v1-based EST rows).
- **WITH flagged events (binding variant per the D9 ruling) and WITHOUT (cross-check): identical to the printed digit**
  (620 / 10,777). No flagged event carries any stored candidate; removing the 356 flagged events changes M by at most
  212 of 4×10⁶ (VERIFIED: `M_flagged_events` NI22 10, NI30 15, NI61 18, NIX 212, NIC 59, HS 38, lowpt 4 = the counts of
  LOG.md 18 Nov 11:02 and 19 Nov 10:20).
- **Precision.** Monte-Carlo error of the median 0.55 events at 620 (0.09 %) and 2.9 at 10,777 (0.03 %); three other
  seeds give 619.3–619.9 and 10,778–10,783. Both are inside the "about 0.3 %" of STR l.2757, and 300 (tie level 299.1)
  is far outside it: the 16 % quantile of the (P) reading is already 482. The reading does not depend on the precision
  sentence. In counts: the pause level at R09 is m_Z = 4 (addendum §4.1); the pilot has 11 (P).
- Empty-pilot check: the script reproduces `addendum1_v4_stdout.txt` l.66 exactly before any count is inserted.

Term medians at R09, reading (P) [VERIFIED]: Z 489.5; DIF 18.0, DIF-C 16.6, NI-X 16.2, NI-C 16.9, NI 22 / 30 / 61.5
3.3 / 4.5 / 4.4, HS 2.8, Z low-weight 1.5 (all zero-count floors), pile-up 6.7.

## 2. Counts [VERIFIED: `rule1_prelim_counts_tove_2026-11-19.json`]

Variant 0 = all own hits before CKF (the rule-1 basis, Df-9). (P) = a finder candidate with N_IT2 ≥ 3, N_IP2 ≥ 7 inside
the width; (N) = a candidate inside the width with deficit k ≤ ⌊n/2⌋. s3 = with N_2S2 ≥ 3 required (R14 = R17 = R20, FB).

| rung (width) | Z full class P | Z full class N | Z 0.05 class N | P with N_2S2 ≥ 3 | N at n = 10 (s3) | every B1 class, HS, lowpt |
|---|---|---|---|---|---|---|
| R04 (no width cut) | 149 | 5,179 | 50 | 21 | 3,041 | 0, except DIF-C: 1 near-pass |
| R05 (37.5 mm) | 138 | 4,881 | 49 | 19 | 2,868 | DIF-C 1 near-pass |
| R06 (18.75 mm) | 93 | 2,884 | 34 | 16 | 1,645 | DIF-C 1 near-pass |
| R07 (9.4 mm) | 42 | 1,076 | 11 | 7 | 597 | 0 |
| **R08 = R09 = R11 (4.7 mm)** | **11** | **253** | 2 | 2 | 147 | **0** |

- Samples [VERIFIED from the file metadata, 1,083 pilot files each read exactly once, 0 finder errors in 1.03×10⁷
  finder calls]: DIF 4×10⁶, DIF-C 4×10⁶, NI 22 / 30 / 61.5 10⁶ each, NI-X 4×10⁶, NI-C 2×10⁶ (21 orientations each),
  HS 2×10⁶ (own road), lowpt 2×10⁵; Z(νν) 2.3×10⁶ generated, 994,446 in the full-weight class.
- **M of the Z term: Σw/w_max = 993,887 measured, against 1.011×10⁶ planned** → 41.96 events per count instead of 41.25
  (used above; with the planned M the Z term is 1.7 % lower, B₅₀ ≈ 611 for (P), ESTIMATE by scaling). 0.05 class: 8,095 events.
- Fall of the (P) count per width step: 138 → 93 → 42 → 11 (×1.5, ×2.2, ×3.8): nothing like the pile-up fall of ×200–340.
- What the 11 passes are: in 8 of the 11 events the passing candidate is made of exactly 2 particles with every hit
  on a selected CKF track (pairs of tracks); 1 event has Fatras-made hits and half its hits off CKF tracks
  (conversion-like); 2 events have hits of secondary-vertex products (vsec ≥ 1).
- **After-CKF, information only, not rule 1** (variant 1, run only for events that have a variant-0 candidate, so a
  lower bound): (P) 0 at every rung R04–R08; (N) 528 / 513 / 307 / 90 / **17** at R04 … R08. Of the first 300 stored
  before-CKF R08 near-pass candidates (the list is capped at 300 rows), 93 % have at least half of their hits on CKF tracks.
- Off-road alarm (ADD l.391-392): the single B1 candidate (DIF-C, R04–R06 near-pass) is in an orientation k ≠ 0;
  1 of 1 is not a fraction worth quoting. No event passes in more than one orientation.

## 3. What this does and does not show

1. With the frozen finder, on all own hits, the Z(νν) pilot holds 11 events at the R08 width. Read through rule 1
   this is ≈ 460 SM events in 3 ab⁻¹ before CKF, before any conditional, on top of floors of 161. This is the
   expected branch of the strategy (STR §12.1 Q2: "the day-15 rule … is expected to pause"), at the low end of it.
2. (P) and (N) are both **lower bounds on the frozen m_H** (plan A1): the frozen H is defined on a width-only subset
   pass that does not exist as code. So "above 300" is robust to that ambiguity; the size (620 or 10,777 or more) is not.
3. The seven B1 classes and the hard-scatter parents give no candidate at R07–R08 in 1.9×10⁷ events. Their
   contribution to B₅₀ is their zero-count floors (sum of their term medians ≈ 83).
4. Not a result: nothing here is a background estimate for the paper. S_CKF and the conditionals are not applied (by
   the rule). After CKF the pass count is 0 of 11, which is the kind of factor the Q2 (c) redesign test would read.

## 4. Open ambiguities (for the orchestrator / user; none resolved by me)

- **A1.** Which count is "m": (P), (N), or the subset pass of STR l.755-761 (not written; channel (i)'s first Phase-3
  task)? The verdict "above 300" does not depend on it; the number does, by ×17 or more.
- **A2.** N_IT2 ≥ 3 has no deficit rule in k_IP; the finder's loose store drops N_IT2 < 3.
- **A3.** "Best candidate" (lowest G) is not determined; R09 and R08 are both given. H with N_2S2 ≥ 3 (R14-type and FB
  candidates) is 2 (P) / 147 (N), but no pile-up estimate exists for those candidates in the script: no B₅₀ formed.
  A reading with 2 Z counts at an R09-like pile-up term would be near 240–245 (ESTIMATE from the addendum's crossing
  table: 282.5 at 3 counts, 323.5 at 4), i.e. **the verdict could depend on which candidate is "best" under reading (P)**.
- **A4.** M of the Z term: measured 993,887 or planned 1.011×10⁶ (1.7 %).
- **A5.** PV for Z(νν) (stored vertex + v1's 10/10/15 µm draw, my seed) and v1's hit merging before the finder are
  provisional choices.
- **A6.** v1 preselection ("41 per count" provisional until the day-12 MET model).
- **A7.** Binding flagged-event variant not yet frozen in PREREG_v2; here it makes no difference.
- **A8.** I used the Fable trailer on my commits, not the Opus trailer of my brief: the session ran on Fable 5.2 and
  the harness attribution rule says so; LOG.md 19 Nov 10:08 records the earlier mismatch as an error.

## 5. Compute [VERIFIED from the done/timeout markers, cpu + sys]

| campaign | jobs | CPU-h | note |
|---|---|---|---|
| p2-c-pilot-cls | 49 done, 3 timeout | 6.03 | of which 1.46 lost in three jobs that hit 1,800 s (ni22-00, ni30-00, ni61-00) |
| p2-c-pilot-cls2 | 8 done | 2.35 | rerun of ni22-00, ni30-00 in smaller jobs |
| p2-c-pilot-cls3 | 4 done | 0.87 | rerun of ni61-00 |
| slices over ssh (not in the ledger) | — | ≈ 0.07 | timing, prefilter check |
| **total** | | **9.3** | estimate before launch 8 (6–10); limit 10 |

My packing by bytes was wrong for the NI radii (≈ 100–115 CPU-s per file against ≈ 27 for DIF-C); that cost
1.46 CPU-h and about 50 minutes. The first driver gave schrodinger 0 slots because my own slice was running there
when it started. Outputs: 61 npz, 1 MB, `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_class/p2-c-pilot-cls{,2,3}/000/`.
The three timed-out jobs left no output; the ledger shows them as failed (not retried: superseded by cls2/cls3).
`qv2run rebuild-ledger` was not run by me.

## 6. Limits of the checks

- The exact shortcut (≥ 4 IP layers with ≥ 2 road hits) was checked on 6,000 NI-X events × 21 orientations (74,539
  finder calls): 0 candidates in skipped orientations, but also 0 candidates anywhere, so the check has no power; the
  shortcut rests on the argument (a loose candidate needs N_IP2 ≥ 4). Z(νν) events are barely affected by it.
- The B1 path produced one stored candidate in 1.9×10⁷ events (DIF-C). I did not run a positive control (a sample
  known to make B1 candidates, e.g. v1's C′₀ guns) through `p2t_classify.py`. **A zero in the B1 classes is therefore
  not independently validated.** It does not affect the verdict above 300; it matters for any later statement that
  B1 is small.
- The classifier was not reviewed by a second agent.

## STATE FOR A SUCCESSOR

- Code: `src/p2t_classify.py` (job; sha256 0d721341…), `src/p2t_counts.py`, `src/p2t_rule1_prelim.py`; campaigns and
  manifests `tools/runner/examples/p2t/p2-c-pilot-cls{,2,3}{,_files}.json`.
- Re-derive the numbers (worker, tt env python, ≈ 1 CPU-min):
  `p2t_counts.py $D/p2-c-pilot-cls/000,$D/p2-c-pilot-cls2/000,$D/p2-c-pilot-cls3/000 outputs/rule1_prelim_counts_tove_2026-11-19.json`
  then `python -I p2t_rule1_prelim.py <counts.json> outputs/rule1_prelim_tove_2026-11-19.json` (from `src/`),
  with `D=/nfs/cajuela/jdochoa/quirks_v2/data/p2c/pilot_class`.
- Every stored candidate (7,607 rows, both variants, columns in each file's meta) is in the npz outputs: other
  readings (other widths, other k rules) need no new finder pass. A new classifier (the subset pass) does.
- Not done: STATUS.md entry (the orchestrator's), positive control of the B1 path, subset-pass classifier, G / best
  candidate, B₅₀ at R14-type and FB candidates, after-CKF pass on all events, `rebuild-ledger`.
- Nothing of mine is running. No signal file was read; no efficiency was formed.
