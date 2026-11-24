# P3-A — FINAL classification of the pilot and the rule-1 counts it gives (inputs to decision point 2)

Aurora (Fable 5.2, executor, work package p3-a), 2026-11-24. Plan written before any code or job:
`phase3_selection/logs/executor_aurora_2026-11-24_10-16.md`. `STR`, `ADD`, `EXP`, `COM` as in `PHASE3_BRIEF.md`;
`TOV`, `ING`, `CEC`, `BJO` as in EXP §0.2; `NIL` = `phase2_exploration/review/RULE1_SUBSET_REVIEW_nils_2026-11-23.md`;
`YLV` = `phase2_exploration/review/RULE1_B50_REVIEW_ylva_2026-11-23.md`.
Result files (all under `phase3_selection/outputs/p3a/`): `C` = `p3a_counts.json`, `T` = `p3a_dp2_inputs.json`
(every number of this document that another work package may use), `D` = `p3a_rule1_dryrun.json`,
`I` = `p3a_indep_summary.json`, `W` = `p3a_witness_check.json`, `A` = `p3a_attrib.json`, `X` = `p3a_xcheck.json`;
generated tables `p3a_tables.md` (copied in the appendix, numbered T1–T12).
Tags: VERIFIED = computed in this session from the files named; ESTIMATE; UNVERIFIED = transcribed.
**No signal file was opened. No efficiency was formed. Nothing here is the binding reading and nothing here chooses a
convention: where the frozen text leaves a choice open, the count is given under every reading.**

@@SUMMARY@@

## 1. What was run

@@RUN@@

## 2. What "final" means here, and the definitions used as frozen

1. **Frozen hand-over variant.** STR l.744-746 planned two variants "compared on 100 events in Phase 3 and one is
   frozen"; ADD §3 P6 (approved 17 Nov, decision D9; COM l.322) superseded that line (ADD l.614) and decided per
   stream: v1's radius cut for DIF, NI 22 / 30 / 61.5 mm and NI-X; option (a) ("hybrid": Fatras parent to the Geant4
   vertex time plus injected Geant4 crossings) for DIF-C and NI-C; `autoh` (by class) for `pilot.c0.hs` and
   `pilot.c0.lowpt`; products from the slab exit, β < 0.1 not handed over. The pilot was generated with exactly this
   (table T10, read from the `trunc_mode`, `n_per_ev_mode`, `beta_min` and `handover` fields of all 623 B1 / hs / lowpt
   files in my jobs). **The Phase-2 classifications therefore already ran on the frozen hand-over variant; "final"
   needs no new chain run**, and none was made. What is final here is the classification of those files under every
   reading of the estimator text, with the Phase-2 number reproduced row by row as one of them.
2. **Own-hit classes (STR l.755-762, quoted).** "The no-pile-up state of an event of term t is classified on subsets of
   the term's own hits … For rung r, a width-only pass over those hits finds the ribbon through the PV in the road, of
   the width of r, that holds the most double-crossing layers. The deficits are counted per layer type: k_IP = max(0,
   n_IP(r) − N_IP2), k_2S = max(0, n_2S(r) − N_2S2), k = k_IP + k_2S (the fixed cut N_IT2 ≥ 3 is a cut on a subset of the
   IP layers and is part of k_IP). f₀(r) = P_geo(r) is the probability of k = 0, and f_k(r) that of a deficit k, for
   k = 1 … k_max = ⌊n(r)/2⌋ ("near-pass"). At the counting rungs R01–R04, where the ladder has no width cut yet, the
   width is the finder's maximum core width (frozen configuration, transcribed in Phase 2); at R12–R14 it is the R08
   width." All own hits, before CKF (Df-9 option (a), STR l.780). The ceiling count is near-pass inclusive:
   H = P_geo + Σ_k f_k (STR l.799; advisor ruling LOG 19 Nov 15:24), m = number of (event, road orientation) with
   k ≤ k_max; n = 7, k_max = 3 without the 2S requirement (s = 0) and n = 10, k_max = 5 with N_2S2 ≥ 3 (s = 3).
3. **T2 candidates and the count each one reads** (STR l.1794-1798: R07, R08, R09, R11, R14, R17, R20 and FB(k_adm),
   each with and without the displaced-vertex veto). H applies "the counting and width cuts only … an untested
   conditional is 1, so for an untested term H is flat from R08 to R11 and from R14 to R20" (STR l.800-802); the
   vertex veto is a B3 conditional. So: R07 → (9.4 mm, s = 0); R08 = R09 = R11 → (4.7 mm, s = 0); R14 = R17 = R20 →
   (4.7 mm, s = 3). The fallback is `fb0 = R04 & p > 0.05 & N_2S2 ≥ 3`, `FBk = fb0 & w_core < W_c/2^k`
   (`acts/stage4/finder/production.py` l.180-183 [VERIFIED by reading]), k_adm ∈ {0, …, 4} per hypothesis
   (`wp_rule_tables.py` l.72): FB(k) → (none | 37.5 | 18.75 | 9.4 | 4.7 mm, s = 3). FB(4) has the cuts of R14.
   **FB(0) reads the R04-width count at s = 3**, so the R04 width of STR l.761-762 belongs to a T2 candidate (§4.4).
4. **Attribution (STR l.747-753, quoted).** "Let n(r) be the number of double-crossing layers that rung r requires and
   j the number of the candidate's double-crossing layers whose two hits come from particles of one origin class of §2.
   The candidate is attributed to that class if j ≥ n/2, mixed if 1 ≤ j < n/2 for every class, and pure pile-up if j = 0
   for the hard-scatter and Geant4 classes." In the pilot: the Z(νν) files have `mu = 0.0` and `mode = hs0x` in all
   460 (checked in the job; `p3a_counts.py` stops otherwise) and contain no Geant4 vertex, so every hit is of the one
   class "particles of the hard-scatter vertex that Fatras traces" (STR l.230; conversions and Fatras-made secondaries
   included). **Every counted Z(νν) witness is attributed by construction** (j = its number of double-crossing layers
   ≥ n − k_max ≥ n/2); there is no mixed and no pure-pile-up candidate in a no-pile-up sample of one class. In a B1 /
   hs / lowpt file two classes exist: the products of the Geant4 vertex (the B1 class) and the parent hadron, a Fatras
   particle (pile-up route for the minimum-bias share, hard-scatter route in `pilot.c0.hs`). For every stored row of
   these samples the witness hit table was dumped and j computed per class (§3.3).
5. **Subset pass.** The classifier of Phase 2 (`p2w_subset.py`, sha256 c68b7b69…, reviewed by Nils) is imported
   unchanged and gives the reading BASE. Its readings S1–S5 (CEC l.38-54) are readings of text the strategy does not
   fix; by the advisor ruling of 23 Nov 19:44 (Vigdis) the axis convention and reading S3 are NOT fixed now, and the
   binding-m candidate is the count "as produced, exact or lower bound, valid for 'above' only". I therefore add the
   other readings as separate columns and change nothing in BASE:

| reading | what is counted | where it comes from |
|---|---|---|
| **BASE** | `p2w_subset.plane_best` unchanged: the plane's full hit set judged with the finder's stored axis and w_core < W; else window-and-fill subsets (7 window offsets, axes along the plane and along each IP hit), each judged with its own axis | Phase 2 as produced (binding-m candidate of the 23 Nov ruling) |
| **OWN** | one single axis convention: every set, the full set included, judged with its own in-plane axis (the convention of `p2w_subset._eval`); all my searches | NIL condition 2 (b): "a full set is judged with the finder's axis, a subset with its own" |
| **HARD** | reading S3 replaced by a hard window: every IP hit of the subset inside one window of full width 2W/1.4826 (own axis; pure windows at every IP hit added to the search) | NIL condition 2 (a), his category H |
| **PLANS4** | the full set with the finder's axis; else window-and-fill with the centres **as PLAN S4 words them** ("each IP hit and each midpoint of neighbours", plane's axis), own-axis judged | NIL §1 row 6: "the code is a different heuristic from the one S4 describes" |
| **UNION** | the smallest k of all of the above (both axis conventions, all searches) | information only, like NIL's 1,610 |

   S / F: reading S has no separate N_IT2 requirement (CEC S5: "is part of k_IP"), F requires N_IT2 ≥ 3 of the subset.
   Every count in every reading has a witness; none is a proven maximum: **each is exact or a lower bound, valid for an
   "above" statement only** (NIL condition 1). A zero is "none found by a non-maximal search; not an upper statement"
   (ruling of 23 Nov, item 2).

@@RESULTS@@

## Appendix: generated tables (`outputs/p3a/p3a_tables.md`, written by `src/p3a/p3a_tables.py`)

@@TABLES@@
