# Critical re-review of strategy addendum 1, version 2 — Wanda, 2026-11-16 14:37 (`date`)

Artifact: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v2_tatiana_2026-11-16_14-14.md` (ADD2). Also read: the fix
report, version 1, the first review (Ulrich, 13:51), `p2c_addendum1.py` and its output, the partition JSON, `STR` =
`STRATEGY_oscar_2026-11-16_10-41.md` §0, §2, §4.0, §4.4, §4.11 (points 1, 2, 5), §4.12, §4.17, §11.2, §11.7, §12.1, `COM` =
`COMMITMENTS.md` (Gate A answers, rows, "by addendum 1"). Tags: **[V]** re-derived by me in this session (file:line, or
my script); **[E]** my estimate; **[U]** transcribed, not checked. My scripts (pure Python, `nice -n 19`, one at a time,
einstein) are in `/var/tmp/jdochoa/wanda/`: `part.py` (independent re-classification of the 245,945 vertices from
`data/p2c/p2-c-part/000/p2-c-part-0.npz`), `calc.py`, `fro.py` (rule 1, own sampler, 2×10⁵ draws × 3 seeds; crossings
with 6×10⁴ draws and the tie rule), `calc2.py` (pool floors with my own allocation, reach and projection with the
functions of the untouched `strategy_budget.py`). No git command, no job on a worker, no subagent, nothing written
outside this file and the scratch directory.

## Summary for the orchestrator

**Verdict: ITERATE (2 A, 5 B, 12 C).** Version 2 is a real improvement and its arithmetic reproduces: the partition
is exhaustive and exclusive, every N_t, every row of §3.1, §3.3, the reach and the projection come out of my own code
to the printed digits. A1, A2, B1, B2, B4, B5, B6, B8, B9 of the first review are resolved. It is not ready for the user
for two reasons, both narrow:

- **A-1. The hand-over is not valid for the two "after the turn" classes.** v1's `Truncate` removes the parent's
  Fatras hits by radius (`run_chain.py` l.284: `hypot(x, y) > r_cut`). A parent that has turned was at larger radii
  before its vertex, so those hits are removed although they precede the vertex. The author's own validation shows
  it: in the first 100 events, 433 of 1,464 (DIF-C) and 514 of 1,463 (NI-C) counting-surface crossings of the Geant4
  parent have no Fatras parent hit, against 0 of 988 (DIF) and 2 of 877 (NI-X) [V: `p2-c-b1yv-val.json`,
  `ab_only_geant4`]. ADD2 P6 reports the median distances and says "validated as proposed"; it does not report this.
  The pilot would write 6×10⁶ of its 1.7×10⁷ B1 events with 30–35 % of the parent's pre-vertex crossings missing from
  the hit record, and H on own hits (Df-9) would be read low for two of the four large terms.
- **A-2. The numbers the user is asked to decide on (159; 237–283) leave out a sample that ADD2 itself says rule 1
  reads.** `pilot.c0.hs` (2×10⁵ vertices, "one count ≈ 40 events", "read in rule 1 as part of each class with its
  own weight") is not in the script or in §3.1. Read as one more zero-count term it gives an empty-pilot reading of
  **196 at R09 and 273 / 297 / 319 at R08** (pile-up 88 / 118 / 148): the pilot pauses when empty at the upper R08
  estimate and on one count anywhere otherwise. Read as one weight class per B1 term (the literal reading, and the
  convention of STR l.1564) it gives **432 / 509–555**: pause on an empty pilot everywhere [V: `calc.py`].

What truly blocks the pilot and what does not: the **Z(νν) pilot (81 of the 131 CPU-h) and `pilot.mb` (10 CPU-h) are
not touched by A-1 or A-2** and their code exists and has run (`p2c_hs0.py`, `p2c_mbgen.py`); they could be put to the
user and started first. The B1 part (≈ 40 CPU-h, 13–20 h of wall time) needs A-1 settled, and its production code is
not written yet in any case (B-4).

MUST item at risk of being infeasible inside the approved budget: **T1-i (every quoted limit toy-based)**. On the
measured numpy scaling the projection is 7,707 CPU-h at 60 parameters (9,600 at 80 and 18,200 at 100, indications),
above 5,992 [V arithmetic]. ADD2 says so. Not in ADD2, and not verified by me: the remedy executor logged at 14:11
that the jax backend gives 84 / 412–451 / 857 / 1,898 s per 1000 + 1000 toys at 31 / 60 / 80 / 100 parameters with
identical q on paired toys (`executor_viktor_…13-57.md`) [U]; if that survives its correctness run the projection is
≈ 4,730 CPU-h at 60 and ≈ 5,140 at 100 parameters, inside the threshold. No other MUST item looks infeasible: the
three new closure tests may end NOT TESTED, which Q3 covers.

## Item g: what the user must be told

Numbers shown at Gate A or since. "Corrected" is my value where it differs from version 2.

| quantity | Gate A / frozen | version 1 | version 2 | corrected (mine) |
|---|---|---|---|---|
| single-interaction (B1) vertices in 3 ab⁻¹ behind the pilot terms | 6.8×10⁷ (4 terms) | 1.6×10⁸ (5 terms, strict) | **3.66×10⁸ (7 terms)** | same [V]. The table's count "190,730" is 193,313 |
| one decays-in-flight pilot count | 65 events | 78 | 26.5 (sample 4×10⁶ instead of 10⁶; 106 at 10⁶) | same [V] |
| one count, decays after a turn | not a term | not read | 24.4 (new term) | same; see A-1 |
| one NI count at 22 / 30 / 61.5 mm | 0.88 / 1.12 / 1.12 | 4.0 / 5.1 / 5.1 | 4.9 / 6.6 / 6.6 | same [V] |
| one count, NI in other layers; NI after a turn | not terms | 74; not read | 23.7; 24.9 (new terms) | same [V] |
| one Z(νν) pilot count (all SM processes) | 18 | 41 | 41.2, plus 2.1 for a low-weight event; provisional until the day-12 MET model | same [V] |
| day-15 reading, empty pilot, R09 candidate | 76 | 120 / 191 | **159** (387 with 10⁶ per sample) | 159 without the hard-scatter sample; **196** with it as one term; 432 with it as seven weight classes |
| the same at an R08 candidate | not printed ("limits about half as high"); 181 by the same computation | 225 / 295 | **237 / 261 / 283** (465–513 with 10⁶) | 237 / 261 / 282 without; **273 / 297 / 319** with the hard-scatter sample as one term |
| pause at how many Z(νν) counts, R09; R08 | ≈ 12 (300.3 at 12; "13" only if a tie does not pause); 6–8 | 3–5; 1–2 | 4; 2 / 1 / 1 | same without the hs sample; 3; 1 / 1 / 0 with it |
| pause at how many counts in a large B1 sample, R09; R08 | 4; 2–3 | 2–3; 1–2 | 6; 3 / 2 / 1 | same; 4–5; 2 / 1 / 0 with the hs sample |
| pilot generation | 54.5 CPU-h, 52 GB | 108 CPU-h, 97 GB | **≈ 131 CPU-h, 144 GB**, 44–66 h on 2–3 slots | same [V]; the B1 production code is not written (B-4) |
| summed zero-count floor of the pool at 457 + 208 CPU-h | 12.6 (SM 8.6) | 94–101 (171–178 as timed) | **175–213 as timed, 99–137 with two measures not yet demonstrated** | SM part same [V]. B1 part 43 → ≈ 24 if one Geant4 pass serves the four large classes [E]; low-weight classes add ≈ 9 / 5 [E] |
| reach if every ceiling is empty, median [84 % edge], R09-like | 790 [712] GeV | not given | **506–597 [443–524] GeV** | same [V: 506 [442], 522 [451], 565 [503], 597 [524]] |
| the same case at an R08-like selection: B₅₀ in the result | 113 | — | not given | **288 as timed, 222 with both measures** (class limit 300) [V] |
| ceiling-test family | 19 terms | 20 | 22 terms, α_c = 0.05/22 | same; the closure family K = 10 → 13 is not stated (B-3) |
| extra CPU in 4a for the new terms | — | not given | ≈ +41 CPU-h | same [V arithmetic] |
| projected total | 4,609 approved, threshold 5,992 | "unchanged" | ≈ 4,780 at the 31-parameter toy cost; **≈ 7,700 at the 60-parameter cost** | 4,784 / 7,707 [V]; 9,600 / 18,200 at 80 / 100 parameters; ≈ 4,730 / 5,140 if the jax result holds [U] |
| expected outcome (STR §0) | pause at day 15; ≈ 0.7–1.0×10⁴ events led by hard-scatter conversions; reach below 243 GeV | unchanged | "not changed by the floors" | supported: that term is in B4 and no B1 number enters it. Not stated: the decays-in-flight part of that estimate and the Q2 (c) rejection table rest on the old N_t and the old empty reading of 76 (B-3) |

New measured fact the user has not seen: minimum-bias photons make 0.0351 conversions per fired parent, i.e. **2.4
conversion vertices per triggered event in the road, 1.0×10⁸ in 3 ab⁻¹** [V: 52,583 in 1.5×10⁶ firings], about ten
times v1's hard-scatter conversion rate (0.23–0.38 per event). By the frozen route table (STR §2, §4.4 point 1) they
belong to the pile-up term B2, where Fatras makes them in the pile-up events, so they are in a term; rule 1 reads them
only through the pile-up estimate (median 6.7 events at R09). Nothing in ADD2 is wrong here, but it should say it in
one sentence (C-5).

Decisions for the user:
1. **Seven terms or fewer.** (a) Seven classes, each with its own zero-count floor (proposed): empty pilot 159
   (R09). (b) "Lenient", four terms: 85, bought by leaving 2.4×10⁸ vertices out on no evidence. (c) Not offered: the
   same 1.7×10⁷ events read as fewer terms (for example decays; three radii; all other interactions). With one B1
   term the empty reading would be 62 [V]. The difference between 62 and 159 is the convention "one zero per term",
   not information; seven terms are the consistent reading of the frozen rule (it already had one floor per NI
   radius), and they keep the option of dropping DIF-C if the bound of B1-e is written.
2. **Pilot size.** Z(νν): 2.3×10⁶ generated (81 CPU-h, 41 per count; proposed), 3.5×10⁶ (123 CPU-h, 27), 5.23×10⁶
   (184 CPU-h, 18 as frozen). B1: 1.7×10⁷ events (≈ 49 CPU-h with minimum bias and Geant4); doubled (≈ +40 CPU-h)
   the empty reading is 101 / 178–224 and a large B1 sample pauses at 15–17 counts (R09), 6–11 (R08) [V].
3. **The hard-scatter parents** (A-2): one term on a sample large enough not to matter (2×10⁶ vertices, ≈ 10 CPU-h:
   ≈ 4 events per count, empty reading ≈ 162 / 240–286 [E]), or the 2×10⁵ sample as drafted (196 / 273–319), or not
   read in rule 1 (159 / 237–283, stated as a leniency).
4. **R08.** With any of these an R08 candidate pauses on 1–3 counts; the user may accept that or ask for more.
5. **Pool.** Keep 457 + 208 CPU-h with floors of 175–213 (nothing changed) or 99–137 (forced decays for four
   tt̄-type samples, of which one is run; preselection before the chain, which gives up re-weighting the pool under a
   varied MET model); or add CPU (SM floor 39 needs ≈ 1,090–1,980 CPU-h, 8.6 needs ≈ 4,960–9,000) [V].
6. **Toys.** The stop rule applies on the measured scaling unless the backend change is confirmed.
7. **Start order** (my suggestion): approve and start the Z(νν) pilot and `pilot.mb` now; the B1 streams after A-1.

---

## a. Regression table (evidence checked by me)

| finding | status | evidence |
|---|---|---|
| A1 curlers | **RESOLVED** as a definition; new finding A-1 on the same class | DIF-C is a term: 51,441 vertices (35,970 π, 15,471 K) [V: `part.py`], N_t 9.751×10⁷, 4×10⁶ events, 24.4 per count [V]. Both wrong statements withdrawn. The "53 %" now quoted is the first review's number for 30–1000 mm; on the v2 class it is 31,238 / 51,441 = 61 % [V] (C-2) |
| A2 interactions after a turn, species, K⁰_L | **RESOLVED** | NI-C 26,239 (24,271 / 1,185 / 783), NI-X 50,083 with all six species, K⁰_L decays 2,906 in DIF [V]. One vertex per firing: 245,945 distinct firings [V] |
| A3 hand-over validation, Fatras check | **PARTIALLY** | `p2-c-b1y` (8 streams, markers done), `p2-c-b1yv-val.json`: `all_hard_checks_pass: true`, 0 slow products, 0 product hits before the vertex time [V]. Fatras check: 99.96 / 99.975 / 99.96 % reach the last layer, p − K = −2.5×10⁻⁵ ± 7×10⁻⁴ [V: `p2-c-part-fatras.json`]. But the same file shows the parent truncation failing for DIF-C and NI-C (A-1); `pilot.c0.hs`, `pilot.c0.lowpt` and the production code paths were not run (B-4) |
| B1 N_t against the sampled population | **RESOLVED** | N_t = 4.0848×10⁷ × 200 × 0.34051 × y × 1.0221 reproduces all seven values to four digits [V] |
| B2 strict reading over the R08 range | **RESOLVED** (subject to A-2) | 387 / 465 / 491 / 514 and 159 / 237 / 261 / 282 [V] |
| B3 what the strict option changes | **PARTIALLY** | T_c = 22, α_c, +41 CPU-h, annex, inventory, T1 channels listed. Missing: K of the closure family, PR-1, T2-a and the COM header ("19"), inventory rows 17 and 19 (B-3) |
| B4 floors, forced tt̄, reach, superseded lines | **RESOLVED**; the list of lines is still incomplete (B-3) | 169.4 / 138.3 / 122.5 / 93.4; 43.1 / 5.8; reach rows; frozen 790 [712] [V]. 327 ms: 408.5 and 407.0 CPU-s for 2 × 1,250 events [V: markers] |
| B5 toys against 5,992 | **RESOLVED** | 4,609 − 183 + 3,102 + 136 + 41 = 7,705 [V] |
| B6 other lines on 45 ms | **RESOLVED** as estimates | +15.3, +45.6, +41 [V arithmetic] |
| B7 hard-scatter share | **PARTIALLY** (as the author says), and it now carries A-2 | sample named; its reading is not computable from the text; the factor 1.022 is not resolved (C-6) |
| B8 weight classes | **RESOLVED** | M = 1.011×10⁶, 41.25 and 2.10 per count [V] |
| B9 citations, script | **RESOLVED** | COM l.181, 182, 183, 216, 257, 283 are the rows cited [V]. The partition JSON on disk is not the job's output: the job (14:07) logged the classes before the radial cut was removed, `classify` was edited at 14:08 and no script writes `outputs/partition_*.json`; my recount from the npz reproduces every number (C-4) |
| B10 resolving power, lower p_T edge, η, road | **PARTIALLY** | B1-g and edge bins stated. `pilot.c0.lowpt`: no N_t, no events per count, read only if it counts (B-2). "Outside the road" is declared unmeasurable although the pilot can measure it (B-1) |
| C1, C2, C4, C5, C6, C7 | applied | tt̄-type shares 40 / 33 / 43 / 35 %; ×4.51 and ×4.34 [V] |
| C3 | not applied, reason given | acceptable |

## b. The partition and the normalisation

**Partition** [V: `part.py`, own first-arc computation from t, t₀, p₀]: conversion 52,583; dif 53,063 (26,641 /
26,422); difc 51,441; k0l 2,906; ni22 2,583; ni30 3,502; ni61 3,496; nix 50,083; nic 26,239; other 49 (23 hIoni and 23
capture at rest of protons, 3 photoelectric). Sum 245,945 = number of vertices = number of distinct firings with a
vertex. Every count and every species split of the JSON is reproduced. Exclusive and exhaustive by construction of
`classify` (l.151-153: decay / inelastic, first arc or not, three volumes or not). **The sum row of the ADD2 table is
wrong: the B1 classes sum to 193,313, not 190,730** (the difference is NI 22 mm, 2,583); 193,313 + 52,583 + 49 =
245,945. The N_t sum 3.66×10⁸ is right (it contains NI 22 mm).

**N_t, factor by factor.** N_trig 4.0848×10⁷ (STR l.200; script l.68); 200 interactions; pool in the road 7.13168 ×
0.30/2π = 0.34051 (25,000 interactions of this campaign; 7.141 in the 40,000 of `p2-c-t-g4`); class vertices per
firing from the partition (statistical error 0.4–0.6 % for the large classes, 1.7–2.0 % for the three radii); 1.0221 =
1.5945/1.560. Result: DIF 1.061×10⁸, DIF-C 9.751×10⁷, NI 4.896 / 6.638 / 6.627×10⁶, NI-X 9.494×10⁷, NI-C 4.974×10⁷, sum
3.664×10⁸ [V].

**From 6.82×10⁷ to 3.66×10⁸ (×5.37)** [V]:
- DIF 6.51×10⁷ → 8.15×10⁷ inside v1's own definition (first arc, 30–1000 mm; ×1.25: Geant4 against the straight-line
  formula and the pool against v1's parent count) → + 1.90×10⁷ for first-arc decays at r < 30 mm (1,184) and
  r > 1000 mm (8,868) → + 5.5×10⁶ K⁰_L decays = 1.061×10⁸ (×1.63).
- Three radii 3.11×10⁶ → 1.816×10⁷ (×5.84 = ×4.55 for the factor 0.22 removed × 1.28 for charged pool parents, Geant4
  yield and neutral parents; neutral parents are 12.5–13.4 % of the three classes [V]).
- New: DIF-C 9.75×10⁷, NI-X 9.49×10⁷, NI-C 4.97×10⁷ (2.42×10⁸, two thirds of the total).

**Like with like.** "1.56 against 1.59" compares 200 × the minimum-bias rate of the v1 formula on 40,000 interactions
of `p2-c-t-g4` (0.007802) with v1's rate that includes the hard-scatter share (1.5687–1.5945, STR l.255). It is
consistent, not a measurement of the share: the same formula on the 25,000 interactions of the partition campaign
gives 200 × 0.008063 = **1.613**, above v1's total [V: JSON `v1_rates`]. The two samples differ by 3.4 % on about
8,200 and 5,300 parents (≈ 2 σ); pooled, 1.580 ± 0.02 [E]. So the hard-scatter share is 0–3 %, and "1.022" and "2.2 %
of N_t" are upper-side planning values (C-6). The effect on N_t is ± 1–2 %.

**The radial cut.** Removing it is right in the strict direction: the 10,052 vertices added are decays before the
first layer or beyond 1 m, most of which cannot make candidates; they raise N_t and the sample together, so events
per count are those of the whole class. No leniency.

**Conversions.** "Not B1" follows the frozen route table and STR §4.4 point 1 (conversion products are not injected
into B1 samples; `p2c_handover.py` l.13). Hard-scatter photons: B4, real SM events, read in rule 1 through the Z(νν)
pilot count. Pile-up photons: B2, where Fatras makes the conversions in the pile-up events; in rule 1 only through
the pile-up estimate. They are therefore in a term. I did not verify the Fatras conversion switch in the pile-up
chain; ADD2 §1.6 [U] reports conversion positrons in the hard-scatter events, same chain.

## c. Rule-1 readings

Own sampler, constants typed from the strategy (R09 median 6.74, s 0.59; R08 87.9 / 117.9 / 148.0, s 0.43; cap
425.5 × Exp(1); Σ N_SM + N_MJ = 4.1705×10⁷).

| case | empty pilot R09 | R08 at 88 / 118 / 148 | m_Z: R09; R08 | large B1 sample: R09; R08 |
|---|---|---|---|---|
| frozen | 76.3 (16–84 %: 36–152) | 156.5 / 181.0 / 203.5 | 12 (300.3; 281.9 at 11, 318.5 at 13); 8 / 7 / 6 | DIF 4 (268.7 at 3, 333.7 at 4); 3 / 2 / 2 |
| seven terms, 10⁶ per sample | 387.7 | 465.7 / 490.8 / 513.8 | 0 | 0 |
| seven terms, proposed sizes | 159.2 | 236.7 / 260.6 / 282.4 | 4; 2 / 1 / 1 | 6; 3 / 2 / 1 |
| the same, Z(νν) 3.5×10⁶ | 146.1 | 223.2 / 246.9 / 268.4 | 6; 3 / 2 / 2 | 6–7; 3–4 / 2–3 / 2 |
| the same, Z(νν) 5.23×10⁶ | 137.1 | 214.0 / 237.7 / 259.1 | 9; 5 / 4 / 3 | 7; 4 / 3 / 2 |
| lenient, 10⁶; lenient, proposed sizes | 147.2; 85.2 | 227–276; 164–209 | 4; 2 / 2 / 1 and 6; 4 / 3 / 3 | DIF 2; 1 and 9; 6 / 5 / 4 |
| **proposed sizes + `pilot.c0.hs` as one term (39.6 per count)** | **195.7** | **273.0 / 297.0 / 318.8** | 3; 1 / 1 / 0 | 4–5; 2 / 1 / 0 |
| **proposed sizes + `pilot.c0.hs` as seven weight classes** | **431.7** | 508.8 / 533.1 / 555.2 | 0 | 0 |
| for information: one B1 term on the same 1.7×10⁷ events | 61.8 | 140 / 164 / 186 | 6; 4 / 4 / 3 | 11; 8 / 7 / 6 |

- **All of ADD2 §3.1 reproduces** within the Monte Carlo error. Two cells sit on the limit and move by one count with
  the tie rule: the frozen m_Z is 12, not 13 (300.3; STR l.2814 calls 12 "at the limit" and l.2757 makes a tie pause),
  and "3" for DIF at R08 / 118 with the 3.5×10⁶ pilot is 2 (299.3) (C-3).
- **Overrides against the text.** `p2c_addendum1.py` l.25-35: pilot size, M_FULL, LOW_CLASS, F_PASS, F_HS, the R08
  range, the costs, the Geant4 costs; the class counts come from the JSON. The sampler `b50` (l.48-55) is `d15_q`
  (`strategy_budget.py` l.878-888) with the pile-up term as an argument and 10⁵ draws. Nothing else enters the
  readings. The copy is byte-identical (sha256 548b5ba8… on both files [V]). What the text says and the script does
  **not** do: read `pilot.c0.hs` and `pilot.c0.lowpt` (A-2, B-2). The frozen row (76 / 181; 13 / 7; 4 / 2) is not in
  the version-2 output file; it is carried over from version 1.
- **Definition of rule 1.** Unchanged in what is pinned: every term from the samples that exist at day 15, Gamma(m + 1)
  on the sample's M, no pool floor, one Z(νν) count for all SM processes and the multijets, ≥ 10⁵ draws, ties pause,
  limit 300, pile-up term as frozen. The crossings of the script use 2×10⁴ draws and "> 300"; they are illustrations.
- **More lenient than the frozen rule without saying so:** (i) the two after-turn classes would be read on hit
  records that lack parent hits (A-1); (ii) the hard-scatter parents are in N_t (factor 1.022) but read on
  minimum-bias kinematics, while the text says they are read on their own sample (A-2); (iii) `pilot.c0.lowpt` is
  read only if it counts, and its zero bounds nothing (B-2); (iv) nothing pins that a B1 event is tested in every
  road orientation (B-1). Stated leniencies: v1's preselection weights (provisional), products with β < 0.1, the
  Fatras step limit.
- **Seven floors in one rule.** Coherent with the strategy's convention: every term of the likelihood has its own
  counted factor and its own Gamma(m + 1) (§4.11 point 2), "one zero per term" limits the zeros inside a term's route,
  not across terms (l.1575-1578), and the frozen rule already read one floor per NI radius. The price is that the
  empty reading grows with the number of terms: 62 for one term, 159 for seven, on the same events. This should be
  said to the user (decision 1); it is not an error.

## d. The pilot definition

- **Sizes and Geant4** [V]: 'all' pass 1.198×10⁸ firings (set by NI-X at 0.03339 per firing; DIF 4.47×10⁶, DIF-C
  4.11×10⁶, NI-C 2.10×10⁶ available), 'ni' pass 4.61×10⁸ firings for the three radii; 16.2 CPU-h. NI-X has no margin:
  a yield 1 % lower in the pilot's pool leaves the sample short (C-7). Chain 22.4 CPU-h; the costs of DIF-C, NI-X and
  NI-C are those of DIF and NI by proxy; the 1,000-event validation jobs took 6.9–7.4 CPU-s including start-up, so the
  proxy is not too low [V: markers]. Z(νν) 81.1; minimum bias 10.0. Total 129.7 + 1.5 = 131 CPU-h; 144 GB with 3.5 +
  0.8 kB per B1 event (validation files: 2.5–3.5 kB per event [V]) and 30.2 kB per Z(νν) event.
- **Populations.** Parents: all six species, within 1 mm, 0.5 < p_T < 20 GeV, |η| < 1, natural mixture, uniform
  azimuth (`p2c_mbgen.py` l.87-90, `p2c_g4vtx.py` l.90-94) [V]. One vertex per event. Road and PV not fixed at
  generation: `phimet` is a uniform draw unrelated to the parent (`p2c_b1.py` l.12-13, l.76) (B-1).
- **Recorded per B1 event** (`p2c_b1.py` l.125-127) [V]: hits with truth, CKF summary, Geant4 vertex row with the
  parent's initial momentum, products, the parent's Geant4 crossings before the vertex, the rows given to Fatras,
  the SimHits. This is enough for the own-hit classification before CKF (Df-9), for the overlays, and for building
  the second hand-over variant, which is what makes A-1 repairable on paper.
- **Recorded per Z(νν) event** (`p2c_hs0.py` l.39-41, l.125-128) [V]: truth MET, tries, vertex, v1's weight and its
  inputs, jets above 20 GeV, e and μ above 5 GeV and photons above 10 GeV with isolation and a prompt flag. Not
  recorded: any sum over the visible final state (ΣE_T, H_T), jets below 20 GeV, the particle list. A MET model built
  from public resolution parametrisations is usually a function of ΣE_T; if the day-12 model needs it, the summaries
  must be regenerated from the seeds (≈ 27 CPU-h at 42 ms [E]). Adding the columns costs nothing now (C-8). The same
  list would give the hard-scatter parent pool that `pilot.c0.hs` needs.
- **Hand-over**: A-1. Also: the β cut is an environment variable that defaults to 0, i.e. to the variant that failed
  validation (`p2c_handover.py` l.28) (B-4).
- **Not written** [V: executor log, "Pilot campaigns as they would be submitted"]: the production mode of
  `p2c_g4vtx.py` that reads the pool from the minimum-bias files; `load_vertices` taking `dif` or `k0l` for the DIF
  sample; the jobs of `pilot.c0.hs` and `pilot.c0.lowpt`. The log plans 'all' jobs of up to 4×10⁶ firings; the
  partition job used 2,161 MB for 1.5×10⁶ [V: marker], so 4×10⁶ would need ≈ 5.8 GB against the 3,750 MB guard (C-9).
- **Calendar.** Day 5 is 2026-11-21. 131 CPU-h on 3 slots is 44 h, on 2 slots 66 h. Started at noon on 18 November
  the pilot ends on the morning of 20 November (3 slots) or of 21 November (2 slots): no margin on 2 slots, and the
  B1 code and one smoke job per stream come first.
- **Is the rule informative with these sizes?** Probability-free facts: at R09 it pauses at 4 Z(νν) counts or 6
  counts in one large B1 sample (3 and 4–5 with the hs sample as a term). At R08 it pauses at 1–2 Z(νν) counts and 1–3
  B1 counts, and with the hs sample as drafted an empty pilot is at 273–319. So at R09 the rule distinguishes
  "empty" from "a handful"; at R08 it distinguishes "empty" from "anything".

## e. Pool, reach, budget

- **Floors** [V: `calc2.py`, own allocation]: planned split 456.6 / 208.5 CPU-h, planned floors 8.64 / 3.94 / 12.59.
  SM: 169.4 as timed, 138.3 forced tt̄, 122.5 preselection first, 93.4 both; rows Z(νν) 29.2 / 26.4 / 19.6 / 17.1,
  W(τ_h) 20.2 / 18.3 / 14.0 / 12.2, W(eν) 13.8 / 12.5 / 9.6 / 8.3, tt̄ 1ℓ 36.4 / 24.9 / 28.5 / 17.5. B1: 43.1 (9.1, 9.0,
  1.9, 2.4, 2.4, 9.7, 8.7) and 5.8. Sums 213 / 181 / 166 / 137 and 175 / 144 / 128 / 99. CPU for an SM floor of 39:
  1,094–1,984; of 8.6: 4,960–8,996. All as printed in ADD2.
- **B1 pool floor is overstated (B-5).** The script charges each large class its own Geant4 cost (l.147: 0.305 ms
  divided by that class's yield), as if four passes were run. One 'all' pass gives the vertices of DIF, DIF-C, NI-X
  and NI-C together, which is how the same script costs the pilot (l.118-122). With one pass (0.90 ms per firing
  including the chain for every vertex) 185 CPU-h give ≈ 7.4×10⁸ firings and floors of ≈ 4.4 for each large class;
  with the rest on the 'ni' pass the B1 sum is ≈ 24, not 43 [E].
- **Low-weight classes.** §3.3 counts the full-weight class only. By T1-a and STR l.1564 each weight class is its own
  counted factor; a zero in the 0.05 class adds 5.1 % of each row: ≈ +8.6 (as timed), +4.8 (both) [E]. Rule 1 has this
  term, the pool table does not (C-10).
- **Reach** [V]: frozen 790 [712]; as timed 506 [442] (seven terms), 522 [451] (four); both measures 565 [503], 597
  [524]. Predictive B₁₆ / B₅₀ / B₈₄: 143 / 189 / 246 as timed with seven terms, 96 / 125 / 159 with both measures.
- **Projection** [V]: extras 76.7 (pilot) + 15.3 + 45.6 + 41 = 178.5; 4,784 at the 31-parameter cost, 7,707 at 60. The
  header's "≈ 7,660" is the script value without the 41 (C-3). Everything ADD2 adds is in it. Not in it: a larger
  hard-scatter sample if A-2 is fixed that way (≈ +10); toys above 60 parameters although this addendum adds at least
  three auxiliary channels, more with the weight classes.
- **Preselection before the chain.** Sound for the pool: a zero-weight event contributes nothing, the smearing draw
  is seeded per event (`p2c_hs0.py` l.52), and the cost model uses the measured fractions with w > 0 (0.442, 0.315,
  0.2105). Lost, as ADD2 says in half a sentence: events failing the nominal preselection that pass under a varied
  MET model, so the MET-model nuisance on H rests on B4-e alone for them; and re-use of the pool if the preselection
  changes after the freeze. Two weight classes remain; for tt̄ the 0.05 class is 45 % of the events passing and 3.8 %
  of the weight, at full chain cost. The column needs the frozen v2 preselection as code and unmeasured weights for
  eleven processes; ADD2 says the "as timed" column stands until each measure is demonstrated, which is the right
  rule.

## f. Consequences

- **Expected background and outcome of STR §0.** ADD2 states that the expected outcome is not changed by the floors.
  Supported: the 0.7–1.0×10⁴ events are hard-scatter conversions inside the SM terms (N_trig × photon rate × v1's
  counts), no B1 normalisation enters, and the reach below 243 GeV follows from that background and its width. Not
  drawn: (i) the decays-in-flight part of scenarios (α1) and (α1′), 385–647 events, is N_t × v1's counts; with the
  first-arc N_t inside v1's own definition (×1.25) it is ≈ 480–810, and the other classes have no v1 count [E]; (ii)
  the Q2 (c) rejection table (STR l.2854-2862, l.2875-2880) is built on the pilot transfer factors and on "B₅₀ with the
  conversions removed 76": with an empty reading of 159 the room below 300 falls from 224 to 141 events, so the
  rejection needed at f_D = 0 rises from ×44 [×30] to roughly ×70 [×48] [E]; (iii) the (γ) row "m_Z 2.1 / 6.3 / 12.6 /
  20.9" (l.2829). These are what the user reads at day 15 when choosing between (b) and (c).
- **COM rows.** B1-a…g, B4-c, T1-i, ST-1, INV-1 have entries. Missing: the closure family (STR l.407-408: K = 10 counts
  B1-a for DIF and the three radii; three more B1-a tests make K = 13 and change every 0.05/K threshold, Df-2, the COM
  header l.22-25, PR-1 l.249); T2-a l.217 and PR-1 ("family of 19"); INV-1 rows 17 (pool, seven terms) and 19
  (overlays); B1-e keeps "soft bulk excluded by an analytic bound" although no bound is claimed any more.
- **Phase 3 / 4a.** Three closure designs are named, not written (1,000 unbiased test overlays, 500 derivation
  overlays, the paired pass: 41 CPU-h [V arithmetic]). No v1 count exists for the new classes, so whether their test
  rung is evaluable is unknown; NOT TESTED is covered by Q3, with a new annex row each. Acceptable at this gate if
  the K question is settled.
- **Result with empty ceilings at R08.** B₅₀ = 288 as timed and 222 with both measures, against the class limit of
  300 (113 at Gate A) [V]. The R08 candidates have little room left in the result, not only in rule 1.

## Findings

**A — must be resolved before the B1 part of the pilot is submitted**

- **A-1 Parent truncation for DIF-C and NI-C.** Evidence above. Either (i) truncate the parent by time for these two
  streams (drop parent SimHits later than the vertex time, in a copy of `Truncate`; v1 code stays unedited), rerun
  1,000 events of each (seconds of CPU) and add to `p2c_validate.py` the hard check "Geant4 pre-vertex crossings of a
  counting surface without a Fatras parent hit ≤ 2 % for every stream"; or (ii) write in P6 and in the rule-1 wording
  that the parent's hits of these two classes are taken from the stored Geant4 crossings (second variant of STR
  l.744-746), with the statement that this variant has not been validated. In both cases P6 must report the 433 /
  1,464 and 514 / 1,463, and the 8 and 88 parent hits later than the vertex time in DIF and NI-X.
- **A-2 `pilot.c0.hs` in rule 1.** Define the reading so that it can be computed, put it in the script and in §3.1,
  and show the user that row. Three consistent options with their readings are in decision 3. Also state the number
  of distinct parents: 2×10⁵ vertices from the in-road hadrons of 2×10⁴ generated events are repeated firings of
  ≈ 10⁴ parents, so "40 events per count" overstates what a zero means for the stiff tail; the hadrons of the
  2.3×10⁶ pilot events would give the pool at no cost if their list is stored (C-8). For this share the road is the
  event's own MET road and all central hadrons should be fired, not only those inside it (B-1).

**B — must be fixed before PASS**

- **B-1 The road.** N_t counts parents inside a road of ± 0.15; the events are fired at uniform azimuth with the road
  left open. For curling parents and wide-angle NI products the candidate need not lie in the road that contains the
  parent's initial direction. Pin in P2 / P7 and in §3.2: the own-hit count m of a B1 sample is the number of (event,
  road orientation) passes over the 21 non-overlapping orientations (2π/0.30, STR l.864-866), with N_t as defined.
  This is exact for the minimum-bias share, costs no CPU, and removes "nothing measures outside the road" from §6.2.
- **B-2 `pilot.c0.lowpt` and |η| > 1.** Give N_t and events per count of the low-p_T sample. My rough estimate: the
  0.3–0.5 GeV parents are about half as many as the pool and make more vertices each, N_t of order 4×10⁸, so one count
  in 2×10⁵ is of order 10³ events and a zero bounds nothing at the scale of 300 [E]. Say so, and say what rule 1 does
  with it (an alarm that pauses on one count, not a term). For 1 < |η| < 1.5 either add the same kind of check sample
  or keep the statement that it is not tested. Both need a pool outside the present phase space, i.e. their own small
  minimum-bias run: `pilot.mb` stores the pool only inside it.
- **B-3 Consequences and bookkeeping.** K = 10 → 13 (or the reason why not); PR-1, T2-a, COM header, INV-1 rows 17 and
  19; superseded lines missing from §3.2: STR l.52 and l.955 ("2.3 events per ceiling count"), l.970-976 (m_H rows on
  a 1.1×10⁷ pool), l.2104, l.2111-2114, l.2829-2832, l.2854-2862, l.2875-2880, l.2888-2889; the two sentences of item f
  on the decays-in-flight size and on the Q2 (c) table.
- **B-4 State of the pilot code.** Say in §4 that the B1 production code is not written, name the three pieces, and
  commit to one job per stream passed through `p2c_validate.py` before the bulk is released. Make the β cut an
  argument of the campaign or assert `BETA_MIN == 0.1` in the pilot mode. Give the calendar margin as in item d.
- **B-5 B1 pool floor.** Cost the four large classes on one shared Geant4 pass; reprint the B1 row and the sums
  (≈ 24 instead of 43 [E]).

**C — suggestions (exact text where possible)**

- **C-1** Offer the Z(νν) pilot and `pilot.mb` for approval and start ahead of the B1 streams.
- **C-2** Table sum row: "190,730" → "193,313" (also in the fix report, row A2). "53 % of the later decays" → "61 %
  (31,238 of 51,441)".
- **C-3** Frozen row: "13; 7" → "12 (300.3, a tie pauses); 7". Header item 5: "≈ 7,660" → "≈ 7,700". §3.1, 3.5×10⁶
  row: "3–4 / 3 / 2" → "3–4 / 2–3 / 2".
- **C-4** Add the writer of `outputs/partition_*.json` to `p2c_g4vtx.py`; note that the npz's own metadata carries
  the classes and code hash of 14:07.
- **C-5** Add: "Conversions of pile-up photons (2.4 per triggered event in the road, 1.0×10⁸ in 3 ab⁻¹) are in B2 by
  the route table; rule 1 reads them through the pile-up estimate only."
- **C-6** "hard-scatter share 2.2 %" → "0–3 %: the minimum-bias rate is 1.56 on 40,000 interactions and 1.61 on the
  25,000 of the partition campaign; 1.022 is kept as an upper-side value".
- **C-7** Fire 3 % more in the 'all' pass (≈ 0.3 CPU-h).
- **C-8** Add to the Z(νν) summary: scalar sum of visible p_T (all, and |η| < 3), jets down to 10 GeV, and the
  hard-scatter final-state hadrons with |η| < 1.5 and p_T > 0.3 GeV (≈ 1 kB per event).
- **C-9** 'all' Geant4 jobs of at most 2×10⁶ firings.
- **C-10** Add the low-weight-class floors to §3.3, or say they are left out (≈ +9 / +5).
- **C-11** Offer the user the reading with fewer terms on the same events (decision 1 (c)).
- **C-12** Quote the toy projection at 80 and 100 parameters as well, and the jax readings once their correctness
  run is done.

## Verdict

**ITERATE.** Fixes: A-1, A-2, B-1 to B-5; the C items as text. Nothing needs ESCALATE: the user decisions of item g
can be put as soon as §3.1 has the hard-scatter row and P6 says what the two after-turn classes are read on. The
Z(νν) part of the pilot is not blocked by any finding here.
