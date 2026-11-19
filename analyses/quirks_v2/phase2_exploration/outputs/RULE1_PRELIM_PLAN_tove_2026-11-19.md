# Plan: pilot classification and PRELIMINARY rule-1 projection (day-7 reading, done early)

Tove (Fable 5.2, executor, rule 1(c)), written 2026-11-19 11:14 -05 (`date`), **before any pilot array was opened**
(only directory listings, file sizes and the writer scripts were read). Information for the user, not a decision:
the day-7 rider was not taken (COMMITMENTS.md l.37); the binding reading is day 15.

`STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`; `ADD` =
`phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v5_clara_2026-11-16_18-21.md` (approved 2026-11-17, COMMITMENTS section "Addendum 1: APPROVED BY THE USER");
`OUT4` = `phase1_strategy/outputs/addendum1_v4_stdout.txt`; `COM` = `COMMITMENTS.md`.

## 1. The rule as frozen (nothing here is mine)

B = Σ_t κ_t · Gamma(m_t + 1) + pile-up term; B₅₀ = median over draws; pause if B₅₀ > 300.

| element | frozen text | where |
|---|---|---|
| per term | max(zero-count floor, N_t·H), H = Gamma(m + 1)/M, m the own-hit count of the pilot sample of M events; the floor is the m = 0 case on that sample; no pool floor | STR l.2730-2733, Df-11 l.2949 |
| basis | all own hits, before CKF, no S_CKF, no conditional credit | STR l.2745-2746 (Df-9), l.2819 |
| H | H(r) = P_geo(r) + Σ_{k=1…k_max} f_k(r), k_max = ⌊n(r)/2⌋, counting and width cuts only; flat R08–R11 and R14–R20 for an untested term | STR l.755-761, l.799-803 |
| B1 terms | seven classes (DIF, DIF-C, NI 22/30/61.5, NI-X, NI-C), each on its own sample at N_t/M with the minimum-bias N_t; m = number of (event, road orientation) passes over 21 orientations, axes φ_road + 2πk/21 | ADD l.384-386, l.601-605; COM l.359 |
| hard-scatter share | one term on `pilot.c0.hs`, N_t 7.9×10⁶, 4.0 events per count, road = the event's own | ADD l.377-383, l.605-606 (D5 H1) |
| SM + multijets | one count m_Z on the full-weight class of the Z(νν) pilot, M = Σw/w_max (1.011×10⁶ with v1's weights), 41.2 events per count; second term for the 0.05-weight class at 2.1 per count | STR l.2735-2737; ADD l.358-360, l.606-608 |
| `pilot.c0.lowpt` | alarm, "enters only with a count" (1,300–2,600 events per count) | ADD l.395-400, l.608 |
| pile-up term | at day 7 the v1-based EST rows of Table 4.4c: R09 median 6.7; R08 88 / 118 / 148 (width 0.43, cap as in script [9b]) | STR l.2738-2741, l.2819; OUT4 l.47-50 |
| candidate | "B₅₀ is read at the best candidate: the candidate with the lowest G" | STR l.2753-2754 |
| precision | "The binding B₅₀ is the median of at least 10⁵ draws (precise to about 0.3 %), and a reading within that precision of 300 counts as larger"; coded as B₅₀ ≥ 300 × (1 − 0.003) = 299.1 pauses | STR l.2757; OUT4 l.47; Gate-A E6 kept (COM l.42) |
| reference numbers | events per count DIF 25.95, DIFC 23.85, NI22 4.79, NI30 6.49, NI61 6.48, NIX 23.22, NIC 24.33, HS 3.96, Z 41.25, Zlow 2.10; empty pilot B₅₀ 160.8 (R09), 238.3 / 262.3 / 283.8 (R08) | OUT4 l.65-66; ADD §4.1 draft row; COM l.359 |
| code | `phase2_exploration/src/p2z_addendum1.py` l.160-246 (streams, `case`, `crossing`, LIMIT), which executes the byte-identical copy of the Phase-1 budget script through `p2c_rule1.py` (campaigns p2-c-rule1, p2-c-rule1b) | — |

## 2. Pilot quantities that enter

1. m per B1 class and rung: passes summed over the 21 orientations, per stream `pilot.c0.{dif,difc,ni22,ni30,ni61,nix,nic}`.
2. m_hs on `pilot.c0.hs` (one orientation, `phi_road`).
3. m_Z (full-weight class) and m_Zlow (0.05 class) on `pilot.hs0.znn` at the stored `phimet_reco_v1`; M = Σw_v1/w_max
   re-measured from the files (reported next to the planned 1.011×10⁶).
4. Count on `pilot.c0.lowpt` (alarm). M per sample from the file metadata (events actually written).
5. Alarm of ADD l.391-392: fraction of B1 passes in orientations k ≠ 0.
`pilot.mb` and the Geant4 vertex files do not enter. No signal file is touched; no efficiency is formed.

## 3. Classification I will run (PROVISIONAL)

Job script `phase2_exploration/src/p2t_classify.py` (new, read-only on pilot files), per event and orientation:
- pool = all rows on the barrel counting surfaces, **CKF-flagged rows kept** (Df-9), v1's analysis-level merging
  (`finder/chain_inputs.merge_pool`, unchanged), no top-up;
- the frozen v1 finder unchanged: `finder.find(..., cfg from frozen_inputs.json (road = δ₉₅ = 0.15, t_seed 4), store='loose')`,
  the fixed cuts |Δφ(n₃, MET)| < 0.15 and |η(n₃)| < 1, and the rung flags of `production.full_set_flags`
  (R01–R14; no dE/dx). Every aligned loose candidate (N_IT2 ≥ 3, N_IP2 ≥ 4) is stored with N_IT2, N_IP2, N_2S2,
  w_core, p(χ²_core), hit counts, CKF-flagged hits, product hits, orientation index.
- From the stored candidates, per (event, orientation) and per width W ∈ {37.5, 18.75, 9.4, 4.7 mm} (R05–R08) and
  N_2S2 requirement: **(P) finder pass** (k = 0: a candidate with N_IP2 ≥ 7 inside the width) and **(N) finder
  near-pass** (a candidate inside the width with deficit k = 7 − N_IP2 (+ missing 2S layers at R12–R14) ≤ k_max).
  T2 candidates covered: R07, R08, R09 = R11 (flat), R14 = R17 = R20 (flat), FB at each width.
- Exact speed-up, no effect on the result: an orientation is passed to the finder only if its road hits have at
  least 4 IP layers with ≥ 2 hits (necessary for any loose candidate); verified on a slice by running both ways.
- Cross-check pass (information only): the same with the CKF-flagged rows removed (v1's pool), where CPU allows.
- PV: B1/hs/lowpt the stored PV draw; Z(νν) the stored vertex plus v1's N(0, (10, 10, 15) µm) draw seeded from the
  event seed (v1 `g1b_tt.pv_met`); the MET axis is the stored one, no new MET draw.

## 4. Flagged events (early product hits, D9)

Flag = `n_early_prod` > 0 at β_min 0.1 (318 events in the NI classes + 38 in hs, LOG.md 18 Nov 11:02, 19 Nov 10:20).
Per the advisor's D9 ruling (LOG.md 18 Nov 11:03): **binding variant WITH flagged events; WITHOUT (flagged events
removed from m and M) as cross-check.** Both are computed for every count and for B₅₀; a flagged event among the
passes is listed individually.

## 5. Projection and precision

New script `p2t_rule1_prelim.py`: imports `p2z_addendum1` (constants, pile-up streams, LIMIT) unchanged; must first
reproduce the empty-pilot row (160.8; 238.3 / 262.3 / 283.8) with the planned M, then insert the measured m and M.
10⁵ draws, common random numbers, 4 seeds. Quoted: B₅₀, 16–84 % interval, seed scatter of the median, the Monte-Carlo
error of the median, and the tie rule (≥ 299.1 counts as larger). The statistical meaning of a count (Poisson, in the
Gamma(m + 1)) is inside B₅₀ by construction and is not an additional error. Readings at R09 and at R08 (88/118/148).

## 6. Ambiguities: listed, NOT resolved by me

- **A1 (largest). What "own-hit count m" is computed with.** STR l.755-761 defines H on "a width-only pass … the
  ribbon through the PV in the road … that holds the most double-crossing layers", with near-pass classes up to
  k_max, and says the subset definition "replaces the finder's choice" (l.777). No such code exists; STR l.872-874
  makes it channel (i)'s first Phase-3 task. My brief says "the frozen v1 finder". I compute (P) and (N) of §3 with
  the frozen finder; (P) is P_geo as the finder sees it, (N) ≤ the frozen H (the finder seeds only N_L2 ≥ t_seed
  configurations and reports one core width per candidate, not the best ribbon of a given width). **Both are lower
  bounds on the frozen m_H; a reading above 300 with them stays above, a reading below is not shown to be below.**
  Which one is the binding m, or whether the subset pass must be written first, is the orchestrator's/user's.
- **A2. N_IT2 ≥ 3 inside k_IP** (STR l.758-759) has no counting rule; the finder's loose store drops N_IT2 < 3, so (N)
  has no deficit in N_IT2.
- **A3. Best candidate** (lowest G) is not determined at day 7; I report R09 and the three R08 pile-up estimates and
  compute no G (no efficiency is touched).
- **A4. M of the Z(νν) term**: planned 1.011×10⁶ or the Σw/w_max measured on the written files; both given.
- **A5. PV of the Z(νν) events** and **merging before the finder** are provisional choices of §3 (v1's), not frozen for v2.
- **A6. The Z(νν) preselection** is v1's ("41" provisional until the day-12 MET model, ADD l.360-362).
- **A7. Flagged events**: binding variant is a recommendation of the advisor to be fixed in PREREG_v2, not yet frozen.
- **A8. `pilot.c0.lowpt` with a count**: the events per count is a range (1,300–2,600); both ends given if needed.
- **A9. Multiple passes of one event** in several orientations are each counted (ADD l.386-387) and flagged.

## 7. Compute

Workers only, through the runner (`qv2run ssh launch <absolute campaign path>`), nice, ≤ 3 jobs per node, never
einstein, SLOTS.md line first. A timing slice (≤ 0.1 CPU-h) fixes the estimate; **if the full classification
projects above 10 CPU-h I stop and ask.** Output: compact candidate tables under
`/nfs/cajuela/jdochoa/quirks_v2/data/p2c/…` with markers. Result file: `outputs/RULE1_PRELIM_tove_2026-11-19.md`.
