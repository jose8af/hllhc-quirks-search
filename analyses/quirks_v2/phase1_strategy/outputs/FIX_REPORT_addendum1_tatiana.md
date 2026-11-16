# Fix report — strategy addendum 1 (fixer: Tatiana, 2026-11-16 14:20)

Review: `review/critical/ADDENDUM_1_CRITICAL_REVIEW_ulrich_2026-11-16_13-51.md` (ITERATE; 3 A, 10 B, 7 C).
Result: `STRATEGY_ADDENDUM_1_v2_tatiana_2026-11-16_14-14.md` ("v2"; version 1 unchanged). Tables: `phase2_exploration/
src/p2c_addendum1.py` (version 2) → `data/p2c/p2-c-addendum1v2/000/p2-c-addendum1v2-0.json`. New measurements (validation
slices only, 0.24 CPU-h): campaigns `p2-c-part` (partition, Fatras check), `p2-c-b1y`, `p2-c-b1yv` (hand-over), and
`p2-c-t-ttf` (forced tt̄, run earlier). Protocol of `agents/fixer.md` followed per finding.

| finding | what it asked | what changed | evidence | status |
|---|---|---|---|---|
| **A1** curlers | correct the pT and sagitta statements; size the curler sample; say what rule 1 reads | both statements withdrawn and corrected (v2 §2 "A1, corrected"); no bound is claimed; decays after the first turn are a term, **DIF-C**, N_t = 9.75×10⁷, sample 4×10⁶ events, 24.4 events per count, read in rule 1 | partition [V: p2-c-part-0]: 51,441 later decays (35,970 π, 15,471 K) in 1.5×10⁶ firings; v2 §2 table, §3.1 | RESOLVED |
| **A2** interactions after a turn; species of NI elsewhere; neutral parents; K⁰_L decays | define samples for all of them | complete partition table of all 245,945 vertices (one class each; code asserts it): new terms **NI-X** (first arc, other layers, all six species) and **NI-C** (after a turn); K⁰_L decays (2,906) in DIF; all samples from a Geant4 pass that fires every species; decays at every radius (the 30–1000 mm cut is dropped) | `p2c_g4vtx.py` `classify`, `partition`; `outputs/partition_p2-c-part-0.json`; v2 §2 table (sum 190,730 + 52,583 conversions + 49 other) | RESOLVED |
| **A3** validate the proposed hand-over; Fatras no-decay check on the instance | run O13 (b) through the hard checks on every stream | O13 (b) implemented (`P2C_BETA_MIN = 0.1`) and run on 1,000 events of each of eight streams: all hard checks pass, 0 slow products handed over, 0 product hits before production time. Fatras check on the running chain: K 99.96 %, π 99.98 %, p 99.96 % reach TB2S L3; p − K = −0.00003 ± 0.0007 (0.09 if kaons decayed) | [V: p2-c-b1y, p2-c-b1yv/…-val.json `all_hard_checks_pass: true`; p2-c-part-fatras.json] | RESOLVED (not validated: `pilot.c0.hs`, `pilot.c0.lowpt`, which do not exist yet) |
| **B1** N_t against the sampled population | pool vs v1 parents, Geant4 NI yield, neutral parents | every N_t now = N_trig × 200 × (pool parents in road per interaction, 0.3405) × (class vertices per firing) × 1.022; v1's rate is no longer used | v2 §2 P2 and table; script `RATE`, `NT` | RESOLVED |
| **B2** strict reading over the R08 range; "adds 51" | give the range; say where an empty pilot is at the limit | "adds 51" removed; §3.1 gives R09 and R08 at pile-up 88 / 118 / 148 for every case; stated first in the document that 10⁶-event samples read 387 / 465–513 when empty | v2 header item 2, §3.1 | RESOLVED |
| **B3** what the strict option changes | T_c, α_c, closure test, samples, cost, annex, T1 | v2 §4 second bullet and §5: T_c = 22, α_c = 0.05/22, three closure designs (+ ≈ 41 CPU-h), annex and inventory rows, three T1 channels; "unchanged" list corrected | v2 §4, §5; COM section | RESOLVED (the closure designs themselves are named, not written: they belong to the pre-registration) |
| **B4** floors as timed; forced tt̄ by shares; reach; superseded lines | show both; reach consequence | §3.3 shows as timed / forced / preselection first / both: 213 / 182 / 166 / 137 (seven classes), 175 / 144 / 128 / 99 (lenient); forced tt̄ now **measured through the chain: 327 ms** (replaces 310 and the 346 by shares); reach 506–597 [443–524] GeV from the strategy's functions (frozen row reproduced: 790 [712]); list of superseded STR lines in §3.2 | [V: p2-c-t-ttf]; script `reach`, `table_SM` | RESOLVED |
| **B5** toys against 5,992 | state the projection and the stop rule | v2 header item 5 and §4: ≈ 7,700 CPU-h at the 60-parameter cost, above 5,992; ST-1 applies unless a remedy works; finding restated as measured (31: 200 toys; 60: 120 toys; 80, 100: 12 toys; nothing between 31 and 60) | script `projection` | RESOLVED (the remedy tests are with another executor) |
| **B6** multijets, B6-c, strict test samples | re-project | §4: multijet loose population 12.5 → ≈ 28; B6-c 25 → ≈ 71; strict tests + ≈ 41 CPU-h | script `projection.extra_lines` | RESOLVED as estimates (the multijet cost is not measured) |
| **B7** hard-scatter share | sample, size, date, reading | factor 1.022 in every N_t; sample `pilot.c0.hs` (2×10⁵ vertices, ≈ 1 CPU-h, with the pilot), read as part of each class | v2 §2 P2 | PARTIALLY (defined; the job for it is not written, and the 1.022 is from v1's rates) |
| **B8** weight classes; "41 provisional" | define m per class | m_Z counts full-weight events, M = Σw/w_max; the 0.05 class is its own term at 2.1 events per count; "provisional until the day-12 MET model" stated in §1.2 and in the rule-1 wording | script `sm_terms`; v2 §1.2, §2 P1, §3.2 | RESOLVED |
| **B9** citations; script for first-arc counts | correct | COM lines corrected (B1-e l.181, B1-f l.182, B1-g l.183, T1-i l.216, ST-1 l.257, VC-3 l.283); B1-g named as Phase 3; log path given as `/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/`; first-arc counts now produced by `p2c_g4vtx.first_arc` / `partition` (no constants typed into the table script) | v2 header, §4, §6; `p2c_addendum1.py` reads the partition file | RESOLVED |
| **B10** resolving power; lower pT edge | state it; n_2S or a check sample | §6.2 gives events per count of B1-g (4.1×10⁴) and of an edge bin; the 0.5 GeV edge is called a convenience and a check sample `pilot.c0.lowpt` is proposed; nothing is claimed for \|η\| > 1 or outside the road | v2 §2 P2, §6.2 | PARTIALLY (the low-pT sample is proposed, not run; its N_t is not measured) |
| C1 larger samples | offer | adopted as the proposal (S2: 4, 4, 1, 1, 1, 4, 2 ×10⁶) with the Z(νν) size table | v2 §2, §3.1 | applied |
| C2 class-wise floor | use Σw/w_max | adopted (0.4396, 0.2657, 0.1205); SM floor 169 / 93 instead of 166 / 90 | v2 §3.3 | applied |
| C3 roulette; prescaled failing events | — | not applied: both are 4a pool design choices that need the v2 preselection; the loss (i) of the review is stated in §3.3 | — | not applied, reason given |
| C4 "half"; "×2.3–3" | correct | 33–43 % given per column; ×4.5 (costs) and ×4.3 (weights) | v2 §3.3 | applied |
| C5 label 181 / 7 / 2 | as computed here | done | v2 §3.1 | applied |
| C6 K⁰_L decays | state or add | added to DIF (2,906 in 1.5×10⁶ firings) | v2 §2 table | applied |
| C7 rule 3 (a) numbers | update | listed as superseded; recomputed at day 15 | v2 §5 | applied as a statement |

**Propagation.** Old → new values, all inside the new files (version 1, the memo and the 13:25 cost file are kept as
records and are named as superseded in the v2 header): events per DIF count 77.7 → 26.5 (new N_t and sample size);
NI 4.0 / 5.1 / 5.1 → 4.9 / 6.6 / 6.6; NI elsewhere 73.6 → 23.7 (NI-X) + 24.9 (NI-C); empty-pilot strict 191 / 295 → 159 /
237–283; SM floor 90–166 → 93–169; summed floor 94–101 → 99–137 (and 175–213 as timed); forced tt̄ 310 → 327 ms. The
COMMITMENTS section "by addendum 1" is replaced accordingly (my own section only).
**Regression check.** The frozen cases still reproduce with the version-2 script's functions: reach 790 [712]; the
version-1 output file is untouched. The partition sums to the number of vertices (assert in `partition`).
**Neighbourhood check.** (i) The 30–1000 mm radial cut of v1 had silently dropped 18,964 decays in 1.5×10⁶ firings;
the cut is removed. (ii) The first validation job of `p2-c-b1y` started before the last slice was published (two
jobs in parallel) and failed; rerun as `p2-c-b1yv`. (iii) `signal.py` in the v1 analysis directory shadows the
standard library when that directory is on the path (fixed earlier in `p2c_hs0.py`, `p2c_prof.py`).
**Not done.** No pilot campaign; no edit of STR, of addendum version 1, or of `s4pu.py`.
