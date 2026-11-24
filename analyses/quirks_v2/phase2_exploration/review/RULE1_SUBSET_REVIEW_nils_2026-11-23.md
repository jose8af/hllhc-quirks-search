# Second-agent review of the subset-pass classifier `p2w_subset.py` (advisor ruling (ii), LOG 2026-11-19 15:24)

Nils (Fable 5.2, reviewer, rule 1(c)), written 2026-11-23 19:42 -05 (`date`). I did not write, run or edit the
classifier. Reviewed file: `phase2_exploration/src/p2w_subset.py`, sha256 c68b7b69… (= the hash in all 139 job
outputs, commit 6d2c6f5). `STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`; `PLAN` =
`outputs/RULE1_VALID_PLAN_cecilie_2026-11-19.md`; `J` = `review/rule1_subset_review_nils_2026-11-23.json`.
Tags: VERIFIED = measured or re-derived by me (file:line); ESTIMATE; UNVERIFIED = transcribed.
No signal file was opened, no efficiency formed, no sealed count read. I do not give the rule-1 verdict.

## Verdict: REVIEWED-PASS WITH CONDITIONS

The subset-pass count may be offered as the binding m, **as exact-or-lower-bound, for an "above" reading only**.
No reported witness fails the definition the plan states. The conditions are about what is written next to the number:

1. **Lower bound, "above" only.** The search is not maximal (measured, §2 and §3). A reading at or below the limit
   from this count would be "not shown below", as in ruling (ii).
2. **The count depends on two readings that the frozen text does not fix; both go into the day-15 text.**
   (a) Reading S3 (width = w_core, a MAD, not a hard window) sets the size of the number: only 137 of the 1,501
   events have a witness whose IP hits all lie inside one window of full width 2W/1.4826 (lower bound of my search;
   `J:24`). (b) A full set is judged with the finder's axis, a subset with its own axis (`p2w_subset.py:18-19`,
   `:222-227` against `:132-186`). At most 74 of the 1,501 Z events (4.9 %) rest on a witness that holds only under
   the finder's axis (§2). Neither changes "above 300": 137 counts is ≈ 5,700 events (ESTIMATE: 137 × 41.96, the
   events-per-count of Ingvild's result l.30; not a B₅₀).
3. **Quote 1,501 (S) / 1,474 (F) as produced; do not replace them by my numbers.** Mine are a check on a different
   search and cover R08, s = 0 only. The other widths, s = 3 (969 / 846) and the B1 / HS / low-pT zeros were **not**
   re-derived here.

## 1. Does the code implement STR l.755-761 and the plan's readings? [VERIFIED by reading, file:line]

Yes for the parts the text fixes, and for S1–S5 as the plan states them. Every difference I found:

| # | code | text | effect on m |
|---|---|---|---|
| 1 | `:322` hits are gathered once within 5 mm (IP) / 60 mm (2S) of the seed plane; the refit selects among them only (`:333`). The finder re-gathers when the normal moves. | PLAN S1 "the finder's own" plane | down only (a plane can lose hits) |
| 2 | `:132-186` a subset keeps the full set's normal; the plane is not refitted to the subset. Membership (3σ_tot) is that of the full set's final iteration (`kernels.py:464-473`). | S1 "hits within 3σ_tot of a PV-constrained plane": existential, satisfied | none (the witness is valid) |
| 3 | `:222-227` the full set is counted with the finder's axis (mean direction of the previous iteration, `kernels.py:506-510`) and without `_eval`; a subset is judged with its own axis (`:136-156`). Stated in the docstring `:18-19`, not in PLAN S1–S5. | not fixed | up to 74 events of 1,501 hold only under the finder's axis (§2). Under the finder's convention they are valid: it is how `cand_vars` judges every finder candidate. |
| 4 | `:141` own axis uses the in-plane norm, the finder `|u|` (`kernels.py:491`). | S1 | float level |
| 5 | `:256-259` every 2S hit of the plane stays in the subset (dropped only if it fails forward / window under the new axis, `:149-152`). | S3 says so | down only (restricts the subsets tried) |
| 6 | `:232-269` candidate axes are the plane's own and the directions of the IP hits; 7 window centres, step h/2, around the median (`:49`, `:251-252`); greedy completion. PLAN S4 says "every window centre (each IP hit and each midpoint of neighbours)". | S4 | down only; the code is a different heuristic from the one S4 describes |
| 7 | `:44`, `:222` R04 has no width cut. STR l.761-763: at R01–R04 "the width is the finder's maximum core width (frozen configuration)". | STR | R04 only; not R08 |
| 8 | `:505` the pool is merged (`chain_inputs.merge_pool`). STR l.755 "the term's own hits"; not frozen for v2 (Björn D3). | inherited from `p2t_classify.py:125` | down or none |
| 9 | `p2w_valid_summary.py:203,222-224`: m is an unweighted count of events with w ≥ 0.5 (Björn D4). | H = Γ(m + 1)/M with M weighted | −0.06 % (Björn, UNVERIFIED here) |
| 10 | `:330`, `:335` a plane needs N_L2 ≥ 4; `:416` a road needs ≥ 8 hits; prefilter `:387`, `:407`. | — | none: necessary for k ≤ 3 (n = 7) and k ≤ 5 (n = 10) |

Reading (S) is not a loose reading at n_IP = 7: N_IP2 ≤ N_IT2 + 3, so 7 − N_IP2 ≥ 4 − N_IT2 > 3 − N_IT2, and "N_IT2 ≥ 3
is part of k_IP" (STR l.758-759) gives k_IP = 7 − N_IP2 exactly (`:224`, `:263`). Double-crossing layers are counted as
in `kernels.cand_vars` (`:204-212` against `kernels.py:698-711`); w_core as `kernels.py:722-725` (`:52-63`, `:168-174`).
Road, alignment and barrel cuts are the frozen 0.15 / 0.15 / 1.0 (config in every output meta; my script stops otherwise).

## 2. Can it over-count? Independent re-check of the reported witnesses

**By reading:** every counted k comes either from a full set selected by `kernels.refit_packed` at its final iteration
with the returned normal and axis (`:332-340`, alignment checked) or from a subset that passed `_eval` (`:260-267`).
I found no path that stores a k without one of the two.

**By my own implementation** (`src/review_nils_subset.py`; does not import `p2w_subset`; own road selection, pair
seeding, plane fit written from the definition, own subset search over all sliding windows, and a separate pure-numpy
verifier that recomputes axis, 3σ membership, forward, window, alignment, w_core and layer counts for each witness).
R08, s = 0, all 460 Z(νν) pilot files, every event that has a row in her outputs (64,005 events classified in all):

| R08, s = 0 | hers | confirmed by my search, verified witness | not found by my search |
|---|---|---|---|
| Z full-weight class, reading (S) | 1,501 | **1,419** (1,384 at the same or a lower k) | 82 |
| Z full-weight class, reading (F) | 1,474 | 1,390 | 84 |
| Z 0.05 class, (S) | 13 | 12 | 1 |

VERIFIED, `J:15-23`, `J:55-62`. No witness of mine with k ≤ 3 failed my verifier (`J:12`).

**Her own witnesses for the events I did not find** (`src/review_nils_witness.py`: her compiled `_greedy`, `_eval`,
`refit_packed` unchanged, a recorder around her `_eval`, her seed loop transcribed; this script imports her code,
my verifier judges). 136 events done of 160 listed: all 86 that my search did not confirm in (S) or (F), 34 of the
35 where my k was higher, 16 of a random 40 where I agreed (the job hit my wall limit; the log was used).

- The instrumented rerun reproduces her stored k (S and F) in **136 / 136**.
- Her witness passes my verifier in **136 / 136** (S: 86 + 34 + 16; F: 85 + 33 + 15). `J:1762` (`table`). VERIFIED.
- Of the 86 not found by my search, 78 are full-set witnesses, judged with the finder's axis; with the set's own
  axis only 12 of the 86 still pass. So my search missed them because it uses the own-axis convention throughout,
  not because they are wrong under hers. Which cut fails with the own axis was not recorded.

**Answer: 0 over-counts in the 1,514 reported R08 (S) events** (1,431 confirmed by an independent search, 83 by her
own witness under my verifier), under the conventions the code states. Under one single own-axis convention the
count is ≥ 1,419 and at most 74 Z events (86 − 12, Z and 0.05 class together) would lose their witness. ESTIMATE for
the upper figure: a different own-axis witness may exist that neither search found.

**Full re-derivation, every w > 0 event, 23 files** (5 % of the sample; the planned 58 did not fit, see §5):
hers 77, mine 80, both 76, only hers 1, only mine 4 (all four have a row of hers with k > 3). `J:39-50`. VERIFIED.
Hard-window witnesses: 6 of the 80.

## 3. The 2 / 200 T7 failures: under-counting only [VERIFIED]

Reproduced with the test's own generator and seed (`review_nils_witness.py t7`): trials 21 and 140, 4.7 mm, by one
unit, in (S), (F), s = 0 and s = 3 (6 entries; `J:5998`). In both trials

- the k before the hits were added came from the **full set**, and that witness passes my verifier (own axis too);
- the same hits are still in the enlarged event, so the true k cannot have risen (the definition is "there is a
  plane and a subset");
- my own search on the enlarged event finds the original k with a verified witness (0 and 2).

Mechanism: the added in-plane hits join the full set and push its w_core above 4.7 mm; the code then leaves the
full-set branch (`:222`) and its window-and-fill heuristic (`:232-269`) does not get back to the original set. This is
the non-maximal search of PLAN S4. A wrong witness is not involved in either trial.

The same non-maximality on real events: among her row events, 109 Z events have k > 3 from her and a verified
k ≤ 3 from me (`J:25`), and my k is lower than hers in 30 of the 1,501 (`J:20`). So a lower bound from both searches
on the row events alone is 1,501 + 109 = 1,610 (S, mixed axis conventions), about 7 % above her count. In the
23 full files the union is 81 against 77.

## 4. Not covered

- Widths R04–R07 and s = 3 (n = 10): read, not re-derived. The code path is the same; the 2S count enters only `:224`, `:263`.
- The B1, HS and low-pT classes (0 at R08): not re-run. Their zero is a statement about the search finding nothing,
  for which a non-maximal search has no "above" protection. Out of scope of ruling (ii) as I read it; flagged.
- B₅₀ arithmetic, M, pile-up terms: not reviewed (Björn reviewed `p2t_rule1_prelim.py`).
- Why the factor 5.8 over the finder count: not decomposed. My runs say only that most R08 witnesses are not
  hard-window ones (137 / 1,501).

## 5. Compute and incidents [VERIFIED from `/usr/bin/time -v`, user + sys]

1.45 CPU-h of 1.5 (`J:6216`), one slot on schrodinger, nice 15, own `NUMBA_CACHE_DIR`.
- 0.54 CPU-h produced nothing: parts 1–3 of my first chain were killed by my own 1,750 s wall limit at file 91 of 92
  (jobs are NFS-read bound, wall ≈ 2.7 × CPU; output was written only at the end). Rerun as six rows-only jobs, which
  is why the full re-derivation covers 23 files and not 58.
- The witness job also hit the wall limit after 136 of 160 events; its per-event log lines were used.
- First T7 attempt failed at start (my recorder was in place when numba compiled her kernel); fixed in my script.

Files: `src/review_nils_subset.py` (sha256 5f29574d… in all 8 job outputs), `review_nils_witness.py`,
`review_nils_summary.py`, `review_nils_chain{,2,3}.sh`; job outputs on `schrodinger:/home/scratch/jdochoa/nils_r1s/out`.
