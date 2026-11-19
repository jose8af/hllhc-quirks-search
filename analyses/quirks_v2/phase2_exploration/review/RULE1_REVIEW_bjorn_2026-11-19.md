# Independent review of the PRELIMINARY rule-1 reading (items (b) and (e) of the advisor ruling)

Björn (Fable 5.2, reviewer, rule 1(c)), 2026-11-19 15:34 -05 (`date`). I did not write the code reviewed.
Reviewed: `src/p2t_classify.py` (sha256 0d721341…, the hash stored in the job outputs), `src/p2t_counts.py`
(b71a1c24…), `src/p2t_rule1_prelim.py` (8b26f06b…), `outputs/RULE1_PRELIM_tove_2026-11-19.md` and its two json files.
Frozen text: `STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`; `COM` = `COMMITMENTS.md`.
My scripts (none imports a p2t function): `src/review_bjorn_rederive.py`, `src/review_bjorn_zdenominator.py`,
`src/review_bjorn_v1tag.py`; their outputs are the three `review/review_bjorn_*_2026-11-19.json` files.
Tags: VERIFIED = measured or re-derived by me (file or command given); ESTIMATE; UNVERIFIED = transcribed.
Compute: about 0.01 CPU-h on schrodinger and landau, nice 19, read-only. No signal file was read; no efficiency formed.

## Verdict

1. **m_Z = 253 near-passes and 11 passes at R08 are reproduced exactly** from the stored rows by an independent
   script, at every rung and for both layer requirements (table in §1). The denominator is reproduced from the 460
   pilot files directly. The preliminary reading B₅₀(R09) = 10,777 is correct arithmetic on correct counts.
2. **No discrepancy that I found lowers m_Z by more than 0.06 %.** Every material difference between the code and
   the frozen definition makes the code count fewer events than the frozen H (lower bound). The "above 300" reading
   therefore stands; the size is a lower bound, as the advisor ruled.
3. **The ceiling paradox (e) is not a bug in the pilot or in p2t_\*.** v1's 0.0162 per event is not an attributed
   rate in the sense of STR l.747-753. v1 counted every candidate with at least ONE hard-scatter hit among its hits.
   On v2's own reproduction of that sample, 92 candidates carry the v1 tag at R06 and **none** of them is attributed
   by the frozen rule (j ≥ 4); 90 of the 92 have no hard-scatter double-crossing layer at all. The ceiling is not
   violated. Details in §3.
4. Consequence outside my brief, for the orchestrator: the sentence "v1 used attributed counts" (STR l.753, marked
   [U]) is wrong for the SM term, and every planning number derived from 0.0162 (STR l.789-797: m_H = 2–18 and the
   ranges of Table 4.4c; the Gate A range) describes tagged pile-up candidates, not own-hit configurations. §4.

## 1. Re-derivation of the counts (item (b), second half) [VERIFIED]

`review_bjorn_rederive.py` reads `meta` and `cand` of the 61 outputs, keys an event by (pilot file path, event index),
and applies: pass = N_IT2 ≥ 3, N_IP2 ≥ 7, w_core < W; near-pass = N_IT2 ≥ 3, w_core < W,
k = max(0, 7 − N_IP2) + max(0, s − N_2S2) ≤ ⌊(7 + s)/2⌋. 1,083 pilot files, none classified twice; 7,605 Z(νν) rows.

| rung (width) | pass | near-pass (k ≤ 3) | k = 0 / 1 / 2 / 3 | with N_2S2 ≥ 3: pass / near (k ≤ 5) | 0.05 class near | Tove |
|---|---|---|---|---|---|---|
| R04 (none) | 149 | 5,179 | 149 / 589 / 2,025 / 2,416 | 21 / 3,041 | 50 | same |
| R05 (37.5 mm) | 138 | 4,881 | 138 / 549 / 1,910 / 2,284 | 19 / 2,868 | 49 | same |
| R06 (18.75 mm) | 93 | 2,884 | 93 / 286 / 1,050 / 1,455 | 16 / 1,645 | 34 | same |
| R07 (9.4 mm) | 42 | 1,076 | 42 / 98 / 349 / 587 | 7 / 597 | 11 | same |
| **R08 (4.7 mm)** | **11** | **253** | 11 / 26 / 68 / 148 | 2 / 147 | 2 | **same** |

After CKF (variant 1, information only): 0 passes at every rung; near-passes 528 / 513 / 307 / 90 / 17: same as Tove.

Denominator, from `evt` of the 460 Z(νν) pilot files (`review_bjorn_zdenominator.py`): 2,300,000 generated;
994,446 events with w_v1 ≥ 0.5 (weights 0.9739–0.98); 8,095 with 0 < w < 0.5; 1,297,459 with w = 0;
Σw (full class) = 974,008.21, w_max = 0.98, **M = 993,885.9** (Tove: 993,887.3, from weights rounded to four
decimals; difference 1.4×10⁻⁶). Pile-up setting in every file: `mu = 0.0`.

Projection, checked by hand, not re-run [ESTIMATE]: median of Gamma(254) = 253.67; × 41.96 events per count =
10,644; plus the mean of the floors and the pile-up term (≈ 135) gives ≈ 10,780, against 10,777. For the passes:
median of Gamma(12) = 11.67; × 41.96 = 489.6, against the Z term median 489.5 in the result file.

What the 253 are [VERIFIED, best candidate per event]: 138 are made of 2 particles, 75 of 3; in 121 every hit is on a
selected CKF track and in 230 at least half; 54 contain a hit of a secondary-vertex product; 10 contain a Fatras-made
hit. 148 of the 253 are at the largest allowed deficit (N_IP2 = 4).

## 2. Code against the frozen text (item (b), first half)

Ranked by effect on the day-15 verdict. "Up" = the frozen definition would count more than the code.

| # | where | frozen text | code | effect on m_Z |
|---|---|---|---|---|
| D1 | `p2t_classify.py:136` (`store='loose'`, one finder pass), `p2t_counts.py:93` (width cut on the finder's w_core) | H is counted on a width-only subset pass: the ribbon of the rung's width that holds the most double-crossing layers; "the subset definition replaces the finder's choice" (STR l.755-757, l.777) | the finder's candidates, each with its own core width; a narrower subset of a wide candidate, or a ribbon the finder never seeded (t_seed 4), is not counted | **up, size not measurable from the stored rows.** Known (plan A1). The count is a lower bound |
| D2 | `p2t_counts.py:102` (`nit2 >= 3` required), `p2t_classify.py:136` (the loose store drops N_IT2 < 3) | "the fixed cut N_IT2 ≥ 3 … is part of k_IP" (STR l.758-759): a missing inner layer is a deficit, not a veto | an event whose best ribbon has N_IP2 ≥ 4 but N_IT2 ≤ 2 is absent | **up, not measurable from the stored rows.** Known (plan A2) |
| D3 | `p2t_classify.py:125` (`merge_pool` before the finder) | not frozen for v2 (plan A5) | two hits within the merging pitch become one, which removes double crossings of close pairs, the dominant topology here (138 of 253 are two-particle candidates) | up or none; not measured. Provisional choice, to be frozen in the pre-registration |
| D4 | `p2t_counts.py:84` against `:103` | H = Gamma(m + 1)/M with M = Σw/w_max | M is weighted, m is an unweighted event count. Weighted m = Σw_pass/w_max = 252.85 (R08), 2,882.4 (R06) | **down 0.06 %** (10,777 → ≈ 10,771) [VERIFIED] |
| D5 | `p2t_classify.py:168`, `p2t_counts.py:55-61` | — | Σw is formed from weights rounded to 4 decimals | M 993,887.3 instead of 993,885.9: 1.4×10⁻⁶ [VERIFIED] |
| D6 | `p2t_rule1_prelim.py:27` with `p2t_counts.py:84` | 0.05 class at 2.10 events per count (addendum) | N_t(Zlow) = k_low × M_planned is divided by the measured M: 2.13 per count | up 1.7 % on a term of 2 counts (≈ 0.1 event) |
| D7 | `p2t_counts.py:114` | B₅₀ is read at the lowest-G candidate (STR l.2753-2754) | a B₅₀ is formed only for R08 with s = 0; none for the N_2S2 ≥ 3 candidates (R14 type, FB) | none on the verdict: the count there is 147 (reproduced), ≈ 6,200 events from the Z term alone [ESTIMATE: 147 × 41.96], against a pause level of about 4 counts |
| D8 | `p2t_classify.py:120` | — | the after-CKF pass runs only for events that have a before-CKF candidate | information only; stated in the result |
| D9 | Z term and `pilot.c0.hs` term | one count m_Z for the SM processes "their conversions included" (STR l.2735); B1 hard-scatter share on its own sample | the Z(νν) pilot is a full Fatras event: 54 of the 253 best candidates contain a secondary-product hit. If such configurations are also what the hard-scatter B1 term stands for, they are counted in two terms | down at most 54 of 253 (21 %) if all were removed: 199 counts, same verdict. Not a code error; a question of term definition [observation] |

Checked and found consistent with the frozen text [VERIFIED by reading, file:line]:
- Rung widths 37.5 / 18.75 / 9.4 / 4.7 mm (`p2t_counts.py:27`) = v1 `eadm_dilution.W_K` and `production.full_set_flags`
  l.172-173; strict `<` as in v1. R04 is coded as w_core < 75 mm: no stored row has w_core ≥ 75 or NaN, and my count
  without any width cut is the same 5,179 / 149.
- k_max: n(r) = 7 at R04–R11 gives 3; n = 10 with N_2S2 ≥ 3 gives 5 (`p2t_counts.py:99`) = ⌊n(r)/2⌋ of STR l.759-760,
  with deficits per layer type added as in l.757-758. N_IP2 never exceeds 7, so 7 − N_IP2 needs no clipping.
- Own hits: the Z(νν) pilot has no pile-up (`p2x_hs0.py:124`, `:204` `mu=0.0`; `meta.mu` = 0.0 in all 460 files), so
  every hit is an own hit; variant 0 keeps the CKF-flagged rows (`p2t_classify.py:122`), which is Df-9 option (a).
- Preselection and classes: events with w_v1 > 0 only (`p2t_classify.py:110`); full class w ≥ 0.5, low class
  0 < w < 0.5 (`p2t_counts.py:57-61`, `:75`). The weight is v1's preselection weight (trigger efficiency × pass), the
  same weight v1's SM term uses (`background.py` l.685-712).
- Fixed cuts |Δφ(n₃, MET)| < 0.15 and |η(n₃)| < 1 (`p2t_classify.py:147`): largest stored values 0.14999 and 0.9995.
- One orientation for Z(νν) (all stored rows have orientation 0), 21 for the B1 streams, one for hs
  (`p2t_classify.py:90`, `:99`).
- The shortcut (`p2t_classify.py:116`, `:131`) is a necessary condition: N_IP2 ≥ 4 needs four IT+PS layers with at
  least two road hits each (a PS double crossing needs four). It is applied before and after merging, both weaker than
  the finder's own requirement. I did not test it numerically (item (d) is Cecilie's).
- Projection (`p2t_rule1_prelim.py:38-44`): unit exponential of the addendum's stream plus an independent Gamma(m)
  draw = Gamma(m + 1); × N_t/M; N_t and the pile-up streams are imported from the approved `p2z_addendum1.py`, and the
  empty-pilot row must reproduce before any count is used. I did not re-audit `p2z_addendum1.py` itself.
- Denominators agree: N_t(Z) = all triggered SM events in 3 ab⁻¹ (41.25 × 1.011×10⁶ = 4.17×10⁷ [UNVERIFIED,
  addendum]) and M = preselected pilot events, so H is per preselected event on both sides.

Not reviewed by me: the B1 path of the classifier (no candidate exists to re-count; positive control (a) is
Cecilie's), the finder itself, the pilot writers.

## 3. Ceiling cross-check (item (e))

The question: pilot H(R06) before CKF = 2,884/994,446 = 2.90×10⁻³ per event; v1's "attributed rate with pile-up,
after CKF" = 0.0162 per event at R06 (STR l.582, l.791). A ceiling cannot lie below what it bounds.

**(i) Denominators [VERIFIED].** The two numbers do not have the same denominator, and the true gap is larger, not
smaller. v1's 0.0162 = 32.3 preselection-weighted candidates / 2,000 **generated** events (81 raw candidates;
`background.json` → `sm.Znunu_j`: `n_class_events` 2000, `f_presel_class` 0.4189; D4 l.196). The pilot number is per
**preselected** event. Like for like: per generated event the pilot gives 2,884/2,300,000 = 1.25×10⁻³; per
preselected event v1 gives 0.0162/0.419 = 0.0387. The gap is ×13, not ×5.6. Also, v1 counts candidates and the pilot
counts events (v2 reproduction: 92 candidates in 77 events, ×1.2).

**(ii) v1's rule [VERIFIED: `stage2_C001_quirks/theory_track/acts/stage4/analysis/background.py` l.685, l.712;
`run_stage4.py` l.423-426; `finder/chain_inputs.py` l.153-179].** v1's SM term counts candidates with
`n_hs_band >= 1`: at least one hard-scatter hit (interaction id 3000) in the candidate's band. No layer count, no
fraction. The frozen attribution needs j ≥ n/2 double-crossing layers made of hits of one origin class (STR l.747-750):
j ≥ 4 at R04–R11, i.e. at least 8 hard-scatter hits (16 in PS layers).

**(iii) Direct measurement [VERIFIED: `review_bjorn_v1tag.py` on `data/phase2/p2-a-c1-sm/000/c1sm-*.npz`, the v2 C1
reproduction of v1's sample: Z(νν) + jets, pile-up 200, after CKF, 2,000 generated events, 50 files; every R05
candidate has a full hit record; my crossing counts equal the stored `cand.cross` for all 22,250].**

| | all candidates | v1 tag (≥ 1 hard-scatter hit) | hard-scatter hits in the tagged candidates | j of the tagged candidates | frozen-attributed (j ≥ 4) |
|---|---|---|---|---|---|
| R05 | 160,499 | 22,250 in 1,805 events | 1 hit: 13,074; 2: 7,109; 3: 1,220; ≥ 4: 847 | j = 0: 21,886; 1: 350; 2: 11; 5: 3 | **3 candidates in 1 event** |
| R06 | 654 | 92 in 77 events (v1: 81) | 1 hit: 54; 2: 32; 3: 4; 4: 2 | j = 0: 90; 1: 2 | **0** |

So v1's 0.0162 is the rate of pile-up candidates that happen to contain one or two hard-scatter hits (14 % of all
R06 candidates carry the tag). This also explains its fall R05 → R06 of ×278, which is the pile-up fall (×201 for
pile-up alone: 49.72 → 0.2470 groups per trial, STR l.576), against ×1.7 for own-hit configurations in the pilot (4,881 → 2,884).

**(iv) Is the ceiling respected for the frozen-attributed counts? [ESTIMATE, low power.]** Ceiling per generated
event: R05 4,881/2.3×10⁶ = 2.12×10⁻³, R06 1.25×10⁻³; in 2,000 generated events that allows 4.2 events at R05 and 2.5
at R06. Observed with pile-up, after CKF, frozen attribution: 1 event at R05, 0 at R06. Both are below the ceiling.
The pilot's own after-CKF near-pass rate (513 and 307 per 994,446) predicts 0.43 and 0.26 events in this sample,
compatible with 1 and 0. With one event the test cannot show that the finder count is a sufficient ceiling; it shows
no violation.

**(v) Pile-up [VERIFIED].** The pilot is hard scatter only (`mu = 0.0`), v1's sample has pile-up 200. Pile-up is the
whole of the difference, but through the tag of (ii), not through promotion of own-hit configurations: promotion is
bounded by H by construction (π_k ≤ 1) and the measured attributed counts respect it.

**(vi) Finder against subset pass.** Not needed to explain the paradox, and not quantified here (D1, D2 of §2).
The R05 event with j = 5 would be the first place to test it: the subset classifier should find it in class k ≤ 2.

**Answer: the attribution rule explains it (×13 at R06 like for like; measured ×∞ at R06, 92 → 0, and ×7,400 at R05,
22,250 → 3). Not a bug in the pilot, the classifier or the counting.**

## 4. Consequences for the day-15 reading (for the orchestrator; I change nothing)

1. The preliminary reading 10,777 (m_Z = 253, lower bound) stands. Nothing in §2 or §3 moves it toward 300.
2. STR l.752-753 says "v1 used attributed counts (D4 l.196 [U])". For the SM term this is not so: the unverified
   tag was transcribed as an attribution. The same passage commits "its coded rule is transcribed in Phase 2 and
   printed in the pre-registration … the difference is measured". This review supplies the transcription and the
   measurement for the SM term (§3 (ii), (iii)).
3. The planning estimates built on 0.0162 (STR l.789-797: H_CKF(R08) = 0.0162/100²–300², m_H = 2–18, the m_H ranges
   of Table 4.4c; the Gate A range 3×10⁴–3×10⁵) extrapolate a pile-up-tag rate with the pile-up fall. They are not
   predictions of the own-hit H, and their disagreement with the pilot is not evidence against the pilot. Whether
   the Gate A statement to the user needs a correction is the orchestrator's call.
4. The ceiling tests of STR l.800 ff. for the SM processes must use the frozen attribution (j ≥ n/2). With v1's tag
   they would fail by construction at R04–R06 (19.5 tagged candidates per event against H = 5×10⁻³).
5. Still open before day 15, unchanged by this review: the subset-pass classifier or the lower-bound statement
   (D1, D2), the positive control of the B1 path, the power of the shortcut, the freezing of merging and PV choices.

## 5. Limits of this review

- The classifier's finder pass was not re-run; I re-counted its stored rows. An error upstream of the stored rows
  (pool construction, PV, road axis) would not be seen by §1. The fixed cuts, the orientation and the stored value
  ranges were checked on the rows.
- §3 (iii) uses raw candidate counts (no preselection weights) on v2's reproduction, not on v1's own files, which
  are not in this checkout. v2's 92 against v1's 81 is the C1 comparison's subject, not mine.
- §3 (iv) rests on one event and zero events.
- `SLOTS.md` carries my two lines but is not in my commit (it holds other agents' uncommitted lines).
