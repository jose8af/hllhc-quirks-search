# Strategy addendum 1, version 5 (for the user's approval)

Version 5, fixer Clara, 2026-11-16 18:21 (`date`), after the third critical review ITERATE (`phase1_strategy/review/critical/ADDENDUM_1_v4_CRITICAL_REVIEW_bruno_2026-11-16_18-17.md`): B-1…B-4 and C-1…C-12 applied as exact text; no number of the §4 tables or of the script output changed; text cells of §0.2 and §0.3 did (D6's factor is now 2.4 for one population and 2.7–3.4 for the three), and §0.1 item 5 now reads 40, not 41. Status: for the user's approval. Record: `FIX_REPORT_addendum1_v5_clara.md`; one row per review item in "Changes since version 4" at the end. Version 4 is kept unchanged; the header of version 4 follows.

Fixer: Zoe, 2026-11-16 (stamp in the file name, `date`). Replaces versions 1 to 3
(`STRATEGY_ADDENDUM_1_tatiana_2026-11-16_13-31.md`, `…_v2_tatiana_2026-11-16_14-14.md`, `…_v3_yvonne_2026-11-16_15-04.md`;
all kept unchanged). Version 4 is version 3 with the measurements made since 15:04 integrated; it is not a redesign.
Record of what changed and why: `FIX_REPORT_addendum1_v4_zoe.md`. This document is self-contained: with `STR` =
`STRATEGY_oscar_2026-11-16_10-41.md` (**not edited**) and `COM` = `COMMITMENTS.md` a reader needs no earlier version.

Tags. **[V]** measured in Phase 2, campaign named (validation slices: `data/p2c/px_validation/<campaign>/000/`; earlier
campaigns `data/p2c/<campaign>/`; markers `ledger/markers/<campaign>/000/`). **[E]** estimate printed by
`phase2_exploration/src/p2z_addendum1.py`; its complete output is `phase1_strategy/outputs/addendum1_v4_stdout.txt` and
"[n]" below is the section of that file. **[U]** transcribed, not checked. The script is a copy of version 3's script
with named `OVERRIDES_V4`; it still runs the byte-identical copy of the Phase-1 budget script (sha256 548b5ba8…) and
reproduces the frozen numbers first (76 [36–152]; 790 [712] GeV; K = 10, T_c = 19) [4], [5], [10]. Sections [1]–[7],
[9], [10], [12] print the same numbers as version 3's output (checked by `diff`); [8], [11] and [14]–[18] are new.
Nothing here is in force until it has passed review and the user has approved it. **No B1 campaign is submitted by it.**
Part 1 of the pilot (`pilot.mb` and Z(νν)) was launched by the orchestrator on 2026-11-16 16:39 on the user's approval
(`LOG.md`, 16:36 and 16:40) and is not a proposal of this document.

## 0. For the user

### 0.1 Summary in plain language

1. **The detector simulation has a limit nobody knew about, and it stays.** The fast simulation used by v1 and v2 stops
   recording hits after half a turn of any particle. Slow particles that curl in the magnetic field make many more
   crossings in reality: compared with the full simulation (Geant4), at least 25 % of the hits of a Z(νν) event and
   37 % of the hits of a pile-up interaction are missing, up to 34–58 % in the middle tracker layers [V] (§1). v1 never
   mentions it; v1's test of curling particles ("0 of 10⁵") could not have counted anything. You chose on 16 November
   to measure first and keep the simulation if curling particles make no candidates. The measurement found **0
   candidates in 2×10⁵ single curling particles with their full trajectories** [V: p2-c-px-lpd, all 2×10⁵ events].
   So the simulation is kept. The zero is in candidates of the frozen finder, its seed threshold included. The day-15 rule counts something wider (near-pass classes on a term's own hits, without the seed threshold), for which the code does not exist yet: by multiplicity alone 3.5 % of these loopers could reach R04 and 10 % its near-pass classes [V], an upper bound, not a value. The stored gun events are classified with that code when it exists (no new simulation).
2. **That zero is a weak bound, and it does not cover the case that matters most.** One count in that test would stand
   for 1.9×10⁴ events in 3 ab⁻¹; a zero allows 2.2×10⁴ events at 68 %, against the scale of 300 that the day-15 rule
   uses [E]. Read for the curling particles of the hard-scatter event itself the same zero allows 286 events [E]; as one more zero-count term of the day-15 rule it would put an empty pilot at about 350 at R09 instead of 161 (265 with both gun sets as one sample) [E: third review]. It is carried as a limitation and not as a term: that is what your option B gives, and it is the most lenient point of this draft. The test fired one particle at a time. A curling particle **together with pile-up hits** was not tested
   at all, nor particles starting outside the road, at |η| > 1, or displaced. The limitation is real and only weakly
   bounded; it is drafted as limitation **[L15]** (§1.4) and must appear in the paper.
3. **A further test is proposed for you to accept or decline** (§1.5): a pile-up sample with the later arcs restored
   from Geant4, compared with the same events on the present simulation. Cost 22–28 CPU-h [E]. It matters because
   no term of the day-15 rule carries an allowance for the missing arcs (every count is made on the present simulation), and the pile-up term is the one whose hit pattern is known to lack a third of its correlated hits: if the
   true pile-up count at a candidate selection were 25 % higher, an empty pilot would already read 308 at the upper
   R08 estimate (limit 300); 50 % higher, 303 at the central one [E; 17].
4. **The pause at day 15 remains the expected outcome, as at Gate A** (about 700 Z(νν) counts and 70–125
   decays-in-flight counts expected by v1's own conversion counts; the rule pauses at 4 and at 6) [12], [4]. The room
   for the other branch is what shrank: an empty pilot reads **161 at an R09 candidate (76 at Gate A; limit 300) and
   238 / 262 / 284 at an R08 candidate**; the study pauses at 4 Z(νν) counts or 6 counts in one large single-interaction
   sample (R09), and at **1–3 counts in any sample at R08**. These numbers are those of version 3; nothing measured
   since changes them.
5. **Three populations are still not read by the rule, and no test bounds them**: parents of 0.3–0.5 GeV (0.7–1.4
   times the normalisation that is read [E]), parents at 1 < |η| < 1.5 (half as many again as the pool [V]) and
   hard-scatter hadrons outside the road (40 per in-road one [V]) (§3 P2, D4).
6. **The hand-over between the two simulations is now settled by measurement** (§3 P6). For five of the seven classes
   v1's rule works (0.0–0.11 % of the parent's crossings without a hit). For the two classes "after a turn" no
   truncation rule can work, because of item 1; a hybrid (fast simulation to half a turn, the stored Geant4 crossings
   beyond) passes (0.04 % / 0.05 %) and is adopted. The second review found the fault with a check that counts a surface once; that check understated it (30–34 % for 58–67 %) and would have passed the time cut (1.4 % / 1.1 % where 40 % / 45 % are missing). The measure with multiplicity is now the criterion; it compares numbers of hits per surface, not positions.
7. **Costs.** Pilot 142 CPU-h and 167 GB (135 and 156 in version 3; 54.5 and 52 budgeted): part 1, running, 95 CPU-h
   and 80 GB; the single-interaction part, 47 CPU-h, waits for your approval and for its production code (no campaign file exists yet; one validated job per stream comes first, §3 P7) and should start when Z(νν) ends, about
   18 November 16:15; it then ends about 19 November 15:45 on two lanes, 32 hours before day 5 (21 November) [E; 8].
   **Toys: the stop-rule exposure of version 3 is gone on present evidence**: with a faster fit configuration the toy
   programme costs 47 / 108 / 228 CPU-h at 60 / 80 / 100 parameters against the 183 budgeted, and the projected total
   is 4,663 / 4,723 / 4,844 CPU-h against the threshold 5,992 (7,710–18,246 with the old configuration). This rests on
   a synthetic workspace, with a factor 1.6 either way, and is re-measured on the first real one [V units, E totals; 11].
8. **The pool at the approved CPU** still needs your confirmation: summed zero-count allowance 201 events as timed,
   121 with two cost measures of which one is not demonstrated (12.6 at Gate A; your decision of 16 November was taken
   on 36–42). Reach if every ceiling is empty: 514–584 GeV median [445–514 at the 84 % edge], against 790 [712] [9], [10].
9. **The signal's own hits are not truncated** (§1.1 point 5): quirk hits are injected without the fast simulation, and the Stage-3 propagator has no turn limit (read in the code by the third reviewer). The effect of the missing arcs of the other particles of a signal event and of its pile-up on the signal efficiency is not measured before the closure verdicts.

### 0.2 What you were shown at Gate A, in version 3, and now

"Per count" = events in 3 ab⁻¹ that one counted pilot event stands for. Rows that did not change since version 3 say so.

| quantity | frozen at Gate A | version 3 | **version 5** |
|---|---|---|---|
| does the simulation follow curling particles? | assumed yes (STR l.210, l.230-232; v1 plan l.1267) | not known | **no hit beyond half a turn of any particle** [V: p2-c-px-a1e, -htg]; missing against Geant4: ≥ 25 % of the written hits (Z(νν)), ≥ 37 % (minimum bias), 34–58 % in TBPS; chain kept by your option B; limitation [L15] |
| background from curling particles ("loopers") | 0 in 10⁵ guns (STR l.1071): by construction of the limit, not a measurement | — | **0 candidates in 10⁵ + 10⁵ single loopers with full Geant4 trajectories [V: p2-c-px-lpd, all 2×10⁵ events]; bound: 2.2×10⁴ events at 68 %** [E]; a looper with pile-up: not tested |
| day-15 reading with an empty pilot, R09 candidate (limit 300) | 76 | 161 [16–84 %: 109–232] | **161, unchanged** [4] |
| the same at an R08 candidate, pile-up estimate 88 / 118 / 148 | 156 / 181 / 204 (not printed at Gate A, which said "at fewer counts"; same computation) | 238 / 262 / 284 | **238 / 262 / 284, unchanged**; new: 256 / 283 / **308** if pile-up is 25 % above the present chain's estimate, 273 / **303** / **329** if 50 % [17] |
| pause at how many Z(νν) counts: R09; R08 | 12; 8 / 7 / 6 | 4; 2 / 1 / 1 | **unchanged** |
| pause at how many counts in one large B1 sample: R09; R08 | 4; 3 / 2 / 2 | 6; 3 / 2 / 1 | **unchanged** |
| single-interaction vertices in 3 ab⁻¹ behind the B1 terms | 6.8×10⁷ (4 terms) | 3.66×10⁸ (7 terms) | **unchanged** [1] |
| one count: decays in flight; after a turn; three radii; other layers; interactions after a turn; hard-scatter sample; Z(νν) | 65; —; 0.88 / 1.12 / 1.12; —; —; —; 18 | 25.9; 23.9; 4.8 / 6.5 / 6.5; 23.2; 24.3; 4.0; 41.2 (2.1 low-weight) | **unchanged** [2], [3] |
| not read by the rule | — | parents of 0.3–0.5 GeV; 1 < \|η\| < 1.5; off-road hard-scatter hadrons | **unchanged** (D4) |
| hand-over of the parent at the Geant4 vertex | "v1's Truncate" (STR l.744) | time cut for parents that have turned, re-validation pending | **v1's radius cut for the five first-arc classes (0.0–0.11 % missing); for DIF-C, NI-C: Fatras to half a turn + stored Geant4 crossings beyond (0.04 % / 0.05 % missing, 1.5 % duplicates at the seam)** [V: p2-c-px-tr, p2-c-px-hy; 14] |
| pilot generation | 54.5 CPU-h, 52 GB | 135 CPU-h, 156 GB | **142 CPU-h, 167 GB**: part 1 (launched 16 Nov 16:39) 95.3 CPU-h, 80 GB, ends about 18 Nov 16:15; B1 part 47.0 CPU-h, then about 19 Nov 15:45 on 2 lanes (day 5 = 21 Nov) [8] |
| Z(νν) summary: softest stored jets | — | "15 GeV" (wrong) | **10 GeV** (`jets10`: p_T > 10 GeV, \|η\| < 5; `jets`: > 20 GeV, \|η\| < 4.7); the full particle list is not stored: another jet radius = regeneration from seeds, ≈ 29 CPU-h [E] |
| summed zero-count allowance of the pool at 457 + 208 CPU-h | 12.6 (SM 8.6) | 201 as timed, 121 with both measures | **unchanged**; with the unit costs measured since: about 204 as timed (sensitivity, not adopted) [9] |
| reach if every ceiling is empty, R09-like, median [84 % edge] | 790 [712] GeV | 514 [445] as timed, 584 [514] with both measures | **unchanged** [10] |
| closure family K; ceiling family T_c | 10; 19 | 13; 22 | **unchanged** [5] |
| toy programme (budget 183 CPU-h) | 183 | 3,102 / 4,996 / 13,638 at 60 / 80 / 100 parameters | **47 / 108 / 228 CPU-h** with the jax configuration (factor 1.6: 29–75 / 67–172 / 143–365) [V units, synthetic workspace]; old configuration 2,464–3,090 at 60, 13,583–18,948 at 100 |
| projected total (approved 4,609; threshold 5,992) | 4,609 | 7,710 at 60, 9,604 at 80, 18,246 at 100 parameters: above the threshold | **4,663 / 4,723 / 4,844: below** (4,645–4,981 over the factor 1.6); old configuration 7,705 / 9,591 / 18,199: above [11] |
| Q2 (c): conversion rejection needed if the pilot counts no decay in flight | ×44 (×30 at the weighted photon rate) | ×67 (×46) | **unchanged** [12] |
| expected outcome (STR §0) | pause at day 15; background ≈ 0.7–1.0×10⁴ events led by hard-scatter conversions; reach below 243 GeV | unchanged | **unchanged**: about 700 Z(νν) pilot counts expected against a pause at 4 [12]. Not in it: the three new classes (2.4×10⁸ vertices, no v1 count) can only add, and v1's conversion counts were themselves made without the later arcs |

### 0.3 Decisions

Readings are "empty pilot at R09; at R08 for pile-up 88 / 118 / 148"; bold values pause on an empty pilot (a tie
pauses from 299.1, STR l.2757). Costs [E].

| # | decision | options and cost | recommendation |
|---|---|---|---|
| D1 | **Limitation [L15] and the chain** (new) | (a) confirm: the chain is kept as your option B says, [L15] is stated with the looper measurement and its weak bound (§1.4). (b) fix the chain (rebuild of ACTS or repeated passes; days of work; every sample regenerated, the running Z(νν) pilot included, ≈ 95 CPU-h; hits + 25–37 %; C1 still at v1's setting) | (a): it is what your rule gives for a zero. It is only as strong as the zero (2.2×10⁴ events allowed; pile-up case untested). With (a) you also approve two changes of items frozen at Gate A: a 25th item of the paper-correction list C3 ("v1's looper bound of 168 events and its 0 in 10⁵ measured nothing"), and the 1,000 looper overlays of inventory row 19 made from Geant4 crossings injected as hits, not with Fatras (same size, same cost order) |
| D2 | **Robustness test on the pile-up term** (new; §1.5) | accept: eighth row of the B6 table, 600 events with the later arcs restored against the same events on the present chain, read at R04–R06; 22–28 CPU-h (12–18 if an existing nominal sample serves); run before the freeze, so that outcome "effect" can still lead to a chain fix (which regenerates the pilot, ≈ 142 CPU-h and about three days); with it you choose whether a measured increase enters the binding day-15 reading (recommended) or is reported beside it. Decline: [L15] stands on the single-looper zero alone; the pile-up arrangement effect stays unmeasured and the paper says so | accept. It is the only measurement that addresses a looper together with pile-up, and its cost is 0.5 % of the budget |
| D3 | **B1 pilot sizes** (to start about 18 Nov) | as proposed: DIF, DIF-C, NI-X 4×10⁶; NI-C 2×10⁶; three radii 10⁶ each; hard-scatter sample 2×10⁶; low-p_T alarm 2×10⁵: 47 CPU-h, ends about 19 Nov 15:45 on 2 lanes. Strategy's sizes (10⁶ each): 24 CPU-h, **389; 467 / 491 / 515**: pauses when empty. All doubled: + 46 CPU-h, 102; 179 / 203 / 225, pause at 16–17 B1 counts; ends about 20 Nov 15:00 on 2 lanes, 9 h before day 5 | as proposed |
| D4 | **Number of B1 terms** | (a) seven: 161; 238 / 262 / 284; K = 13, T_c = 22, + 41 CPU-h in 4a. (b) four, the other classes left out: 89; 167 / 190 / 212; 2.4×10⁸ vertices unread on no evidence. (c) fewer terms on the same events: three 99; 177 / 201 / 223, or one 65; 144 / 168 / 190; K = 9 or 7; needs a new closure design for B1-a, frozen at Gate A (§4.2). The difference between 65 and 161 is the convention "one zero per term", not information | (a): the strategy's convention. (c) is legitimate and cheaper in zeros but re-opens B1-a |
| D5 | **Hard-scatter parents** | H1: 2×10⁶-vertex sample, parents from the finished Z(νν) pilot files, one term: 161; 238 / 262 / 284; 4 CPU-h; cannot start before Z(νν) ends. Same as seven weight classes (STR l.1564 literally): 185; 262 / 286 / **307**. H2 (2×10⁵): 196; 273 / 297 / **319**. H3 not read: 159; 237 / 260 / 282 | H1 as one term; 24 events more lenient than the literal reading, said here |
| D6 | **Three unread populations** | (a) as drafted: 0.3–0.5 GeV parents as an alarm sample only (one count = 1,300–2,600 events: a zero bounds nothing); 1 < \|η\| < 1.5 no sample; off-road hard-scatter hadrons alarm through the 20 other orientations; all three stated as untested; the analytic bound of COM B1-e ("soft bulk excluded") is no longer claimed until it is written and checked. (b) low p_T as an eighth term at 25 events per count: + 21–35 CPU-h; 186; 263 / 287 / **309**. (c) off-road hadrons as a second stratum: + 15 CPU-h; 186; 263 / 287 / **309** | (a), knowing what it leaves open: if any of the three makes candidates at the pool's rate per vertex, the B1 terms are under-read by a factor up to 2.4 for one population (low p_T at twice the pool's yield) and 2.7–3.4 for the three together (1 + 0.7–1.4 + 0.5 + 0.5) |
| D7 | **Pool** | confirm 457 + 208 CPU-h at an allowance of 201 (as timed) or 121 (both measures; one of them, forced top decays, run for tt̄ 1ℓ only; the other gives up re-weighting under a varied MET model), reach 514–584 GeV; or add CPU: an SM allowance of 39 needs 1,094–1,984 CPU-h, of 8.6 needs 4,960–8,996 | confirm; tables carry "as timed" until each measure is demonstrated |
| D8 | **R08 candidates** | accept that an R08 candidate pauses on 1–3 counts (and on an empty pilot under the bold options, or if the pile-up estimate moves up by 25–50 %), or enlarge: Z(νν) to 3.5×10⁶ (+ 45 CPU-h): 148; 225 / 249 / 270; to 5.23×10⁶ (+ 109): 139; 216 / 239 / 261; B1 doubled as in D3 | accept; decide the Z(νν) top-up at day 7 from the first counts |
| D9 | **Hand-over rule per stream** (changes STR l.744) | approve: radius cut for DIF, NI 22 / 30 / 61.5 mm, NI-X; option (a) for DIF-C, NI-C and such events in the mixed samples; criterion ≤ 2 % with multiplicity; one validated job per stream before its bulk is released; the streams with nuclear interactions only after the slow-fragment residue found at 18:15 (1 NI-X event in 25,000, §3 P6 (vi)) is settled: the β cut (0.1) may have to rise, which comes back to you | approve |
| D10 | **Toys** (for information; object if you disagree) | planning on the jax configuration (same pyhf likelihood, fits and statistic; another backend and start values); T1-i is not changed; cost re-measured on the first real workspace; the old-backend projection (above 5,992) is kept on record | no action |

Resolved since version 3 without a new decision: the Z(νν) pilot at 2.3×10⁶ generated events runs (v3 D3, first
option); the truncation question of v3 D8 is answered by measurement (now D9).

## 1. The half-turn limit (strategy-revision input)

### 1.1 Statement

**Phase 1 assumed** that the chain propagates curling particles. The strategy lists loopers among the particles "that
Fatras traces" in the route table (STR l.230, l.232), keeps "loopers" as a sub-topology (l.210, l.728, l.1071, l.1306)
and takes over v1's plan, which lists in-time loopers with "repeated crossings, 2 hits per layer from one particle"
as simulated (`TT/acts/stage4/plan.md` l.1267 [V: read]); the hand-over gives "the parent's hits up to the vertex"
(STR l.744).

**Phase 2 found** [V: `outputs/HALF_TURN_xavier_2026-11-16_16-08.md`, `A1_TRUNCATION_xavier_2026-11-16_15-40.md`;
campaigns p2-c-px-a1d, -a1e, -ht, -htg; numbers re-read from the campaign JSON by the script, 15]:
- In this chain (Fatras of pyacts 48.0.0 as `run_chain.py` l.326-327 calls it) **no particle leaves a hit beyond
  half a turn of its helix.** In 5,000 Z(νν) slice events 231 of 3.94×10⁶ hits of generated charged particles
  (0.006 %) lie beyond 0.5 turn, behind a sharp edge; the Fatras parent's last hit is at ≤ 0.50 turn in every B1
  slice stream.
- Against Geant4 (every charged particle given to Fatras re-fired from its own production point until it decays,
  interacts, stops, leaves the tracker or reaches 25 ns), per event:

| | Z(νν), no pile-up (2,000 events) | one minimum-bias interaction (20,000) |
|---|---|---|
| central charged particles; of them below 0.63 GeV (turn inside the barrel) | 40.0; 19.3 (48 %) | 12.5; 8.7 (70 %) |
| written hits on counting surfaces | 833 | 244 |
| Geant4 crossings of the same particles | 958 | 312 |
| of which after half a turn | 204 (21.3 %) | 88.8 (28.5 %) |
| **Geant4 crossings without a simulated hit** | **209 = 25 % of the written hits** | **91.0 = 37 % of the written hits** |
| the same by layer, relative to the hits on the layer: TBPX L1–L4 | 7 / 11 / 15 / 18 % | 8 / 14 / 21 / 26 % |
| TBPS L1 / L2 / L3 | **42 / 39 / 34 %** | **58 / 57 / 53 %** |
| TB2S L1 / L2 / L3 | 27 / 20 / 11 % | 46 / 38 / 24 % |
| of the particles below 0.63 GeV: still alive after one full turn | 77 % | 77 % |

  For one crossing at 200 interactions: 4.9×10⁴ written hits, 1.8×10⁴ crossings without a hit [E].
  **These fractions are lower bounds, twice over:** detector secondaries are not in the comparison (5 % of the
  written hits), and 0.97 % of the low-p_T particles had no Geant4 record in these runs (tracks ended by
  transportation only; the looper report's addendum of 17:20 shows they are multi-turn loopers), so the true
  fractions are slightly higher. With the complete Geant4 reference (p2-c-pa-htg, LOG.md 18:15) they are 25.2 % and 37.5 %; only the first reason remains (§7.1 point 1).
- **Mechanism.** `run_chain.py` passes no loop, path or step setting; the Python configuration of
  `FatrasSimulation` in pyacts 48.0.0 has none; the compiled library carries a path-limit aborter. That it is ACTS's
  default loop protection is an inference [U]: the source is not installed. **Not configurable without rebuilding
  ACTS** (no build was attempted).
- **v1.** No v1 file mentions a loop or path limit (grep by the executor over the v1 tree [U by me]). v1's looper gun
  counted 0 of 10⁵ without pile-up and 0 of 500 with it; a particle stopped at half a turn moves outward only and
  cannot cross a layer twice, so **that zero follows from the limit and measured nothing.** v1 had the limit (same
  pyacts version, same chain code) and did not know it.

**Implications**, by what is touched:

1. **The looper sub-topology (STR §2 Table 2.1, l.210; route table l.230, l.232; l.1071).** v1's bound "168 b" and the
   entry "0 in 10⁵ no-pile-up guns" are void as measurements. The route table stays as it is (loopers of the
   hard-scatter event belong to B4, of pile-up to B2), but **neither route contains a looper's later arcs**, because
   both are made by Fatras. The 1,000 unbiased "looper" overlays of sample 19 (STR l.2115), if made with a Fatras gun,
   hold no repeated crossings; if that diagnostic population is kept, it has to be made with the Geant4-crossing gun
   of §1.3 (same size, same cost order). The addition of "v1's looper bound measured nothing" to the paper-correction
   list C3 (`ERRATA_v1.md`) is proposed to the orchestrator; C3's list was frozen at Gate A.
2. **The pile-up term (B2, STR §4.5).** The pile-up events are Fatras events plus v1's occupancy top-up. The top-up
   adds, per layer, (ratio − 1) × the event's own Fatras crossings, "z resampled from the layer's hits, φ uniform",
   with ratios 2.3–7.3 that normalise the density to the public TDR occupancy (`plan.md` l.299-310 [V: read]; STR
   l.264, l.275-277). So what can be supported is this: **the number of hits per layer is normalised to the public
   occupancy whatever Fatras lacks; the added crossings are independent of each other in φ**, so the correlation
   between successive arcs of one particle (the same circle crossed again, the same two-hit pattern in consecutive
   layers) is not restored. v1's plan attributes the density deficit to "out-of-time loopers and missing
   secondaries" (l.301); part of it is this in-time effect (37 % of the Fatras hits per interaction against a
   deficit of ×2.3–7.3 [E]). A "looper-pair" top-up exists in v1 only as a variation (l.308-310: pairs with the
   separation spectrum of Fatras same-particle double crossings, which with the limit are first-half-turn
   crossings). Whether the missing correlation changes the pile-up count at any rung is **not known**. Both pile-up
   estimators (repaired thinning and the occupancy model) and the direct counts are built on the same events, so
   their closure against each other (B2-a, B2-b, B2-c) cannot see it. STR §4.5 itself says nothing about loopers.
3. **The B1 classes.** Parents of DIF-C and NI-C get their later arcs from Geant4 (§3 P6). **The products of every
   vertex, and every other particle of every sample, still stop at half a turn.** A soft product that curls is
   simulated on its first half turn only. The own-hit ceiling H of the seven classes is counted without those arcs.
4. **The SM hard-scatter terms (B4) and the Z(νν) pilot.** H per event is counted on own hits that lack 209
   crossings per event (21 % of the true crossings of the event's own particles). The pilot is the v1 chain: it is
   self-consistent with C1 and with every v2 number, and it is final as generated under D1 (a).
5. **The signal.** Quirk hits do not come from Fatras: they are the Stage-3 string-propagator hits injected through
   `run_chain.Inject` (`run_chain.py` l.232; `s4sig.py` header; the same path the looper gun used [V: read]), so the
   limit does not truncate the quirk pair's own hits. **Known:** that path exists and bypasses Fatras. **Read by the third reviewer (code only; no signal quantity):** the Stage-3 propagator has no turn or path limit. It records every root of every chord and ends a pair at the exit (r = 118 cm, |z| = 293 cm), at t_end (1.3 r_exit/β_T + 50 cm/c by default), at its step and hit caps (2×10¹⁰ steps, 4×10⁵ hits) or at β_stop (TT/sim/stage3/code/T3_causal_s3.py l.262, l.300-312, l.489, l.505-513, l.579-582; run_stage3.py l.233). The pair's own hits are therefore not truncated by [L15]. **Still open:** how many pairs end at a cap and not at the exit (a truth-level census, from v1's tracked record, or added to BL-1 with the user's agreement, before the freeze). The other
   particles of a signal event and its pile-up are Fatras particles and lack their later arcs like everywhere else;
   an effect on the signal efficiency could only come through those hits (CKF fraction, shape cuts, hits around the
   ribbon) and is not measured.
6. **C1.** v1 ran with the limit. C1 reruns v1's code with v1's setting and reproduces v1 whatever is decided for
   v2; under D1 (b) the v1-to-v2 comparison would contain the chain change.
7. **Review finding A-1** could not be closed by any truncation rule (§3 P6).

### 1.2 The user's decision

`LOG.md` 2026-11-16 16:36, answering the notice of 16:10: "**B recommended measure first**": the looper measurement
runs first and the Z(νν) pilot starts on the chain as it is; if loopers make candidates the chain is fixed and the
pilot regenerated (≈ 95 CPU-h); if not, the chain is kept and the limitation is stated with the measurement behind it.

### 1.3 The measurement: a looper gun with full trajectories

[V: `outputs/LOOPER_GUN_xavier_2026-11-16_16-38.md` with its addenda; campaign **p2-c-px-lpd** (40 of 40 jobs),
summary `p2-c-px-lpds-0.json` re-read by the script, 16. This is the rerun of the first gun (p2-c-px-lp), in which
985 and 1,003 events of 10⁵ had no Geant4 record and no hit (multi-turn loopers whose track ended by transportation
only). They are recovered: **the zero now covers all 2×10⁵ events**, and the seed-threshold and candidate counts
did not change (first run: finder run 96,153 / 96,147, seed triple 72,105 / 73,756, 33 / 34, 0 / 0).]

Single prompt charged particles of a minimum-bias interaction with |η| < 1 and p_T < 0.63 GeV ("nat": natural
spectrum, median 0.33 GeV; "flat": uniform in 0.1–0.63 GeV), followed by Geant4 until they decay, interact, stop,
leave the tracker or reach 25 ns; **every** crossing injected as a hit through the chain's digitisation, seeding and
CKF; the frozen v1 finder (road 0.15, T_seed 4) with v1's road draw (the particle starts within ± 0.1 of the road
axis; one road per event). No pile-up. 18.2 crossings of counting surfaces per event, 9.2 of them after half a turn.

| events | natural spectrum | flat in p_T | removed by |
|---|---|---|---|
| generated | 100,000 | 100,000 | |
| finder run (≥ 3 hits in the pool) | 97,137 | 97,149 | |
| with at least one seed triple | 72,773 | 74,446 | road and seed geometry |
| with a seed of score ≥ T_seed = 4 | **33** | **34** | **the seed threshold** |
| with a candidate after the refit | **0** | **0** | **the plane refit** |
| passing any rung R01–R14 | 0 | 0 | |

Multiplicity alone does not remove them: counted with no plane, road or width requirement, 10 % of the loopers cross
enough layers twice for R01 and 3.5 % for R04 [V: p2-c-px-lpbs; unchanged in the rerun per the looper report]. What removes them is that the crossings of
successive turns do not lie in one plane through the primary vertex within the finder's tolerances.

**What the zero does not bound** (same weight as the result):
- N_t of what was fired: 7.30 such particles per minimum-bias interaction [V] × 200 × the fraction 0.0318 starting
  within ± 0.1 of the road axis × N_trig = **1.9×10⁹ in 3 ab⁻¹** [E]. **One count = 1.9×10⁴ events; the zero allows
  2.2×10⁴ events at 68 %**, against the scale of 300 (unchanged by the rerun: M is 10⁵ per set as before). A zero that allowed 25 events would need 8.7×10⁷ gun events,
  ≈ 264 CPU-h [E; 16].
- Read for the hard-scatter event's own loopers (19.3 per Z(νν) event [V] × 0.0318 = 0.6 per triggered event, N_t
  2.5×10⁷, with the minimum-bias spectrum standing in for theirs): one count = 251 events, the zero allows 286 [E]:
  by itself at the scale of the limit.
- **Not covered at all:** loopers starting outside ± 0.1 of the road axis (97 % of them; their later arcs can enter
  the road), |η| > 1, displaced loopers, the products of the looper's decay or interaction, the dE/dx rungs, and
  **above all a looper together with other particles**: with pile-up, a looper's correlated hits can complete
  layers that random hits started, which is the promotion mechanism of STR §4.4 and the pile-up term itself.
- A hit-time window of one bunch crossing removes none of these arcs (they arrive 2.7–7.1 ns after the collision at
  the 10–90 % quantiles of the first one) [V].

So: **the chain is kept, by the user's rule; the limitation is real and only weakly bounded.**

### 1.4 Limitation [L15] (next free label; STR §7 ends at [L14], l.2285-2299)

Draft text for the label index and the pre-registration:

> **[L15] No hit beyond half a turn.** The fast simulation (Fatras, pyacts 48.0.0) records no hit beyond half a turn
> of any particle; the limit is compiled in, was present and unnoticed in v1, and is kept in v2. Measured against
> Geant4, crossings without a simulated hit are at least 25 % of the written hits in a no-pile-up Z(νν) event and at
> least 37 % in a minimum-bias interaction (34–58 % on the TBPS layers). Consequences: (i) the topology "repeated
> crossings of the same layers by one curling particle" is absent from every sample, except for the parent of a
> decay or interaction after a turn (DIF-C, NI-C), whose later arcs are taken from Geant4; (ii) the pile-up hit
> density is normalised in number per layer by the occupancy top-up, not in the arrangement of the hits; (iii) the
> own-hit ceilings H are counted without the later arcs. Measurement behind keeping the chain: 0 candidates at any
> rung in 10⁵ + 10⁵ single loopers with full Geant4 trajectories through the frozen finder. That zero allows
> 2.2×10⁴ events in 3 ab⁻¹ at 68 % for pile-up loopers starting within ± 0.1 of the road axis; it does not cover
> loopers starting elsewhere, at |η| > 1 or displaced, nor a looper together with other particles. [If D2 is
> accepted: "A pile-up sample with the later arcs restored changes the pile-up count at R04–R06 by …".]

Where it must appear: (1) the limitations index of the paper and of the analysis note, with the numbers above;
(2) the description of the detector simulation in the method section, one sentence; (3) the caption or text of every
statement about "loopers" (the v1 erratum included); (4) **the abstract-level limitations if a later test shows an
effect**: the row of §1.5 classified "not robust", or a μ₉₅ shift above 10 % (the threshold Df-7 uses for a
robustness variation without a sourced size, STR l.1479-1482).

### 1.5 Proposed robustness test (option; for the user to accept or decline — D2)

*What.* An **eighth row of the B6 robustness table** (STR §4.9, l.1464-1491; COM B6-a l.203, B6-c l.205): "later
arcs restored". A ρ = 1 pile-up sample in which every charged particle of the 200 interactions is also fired through
Geant4 and its crossings beyond half a turn are injected as hits (the mechanism validated for the parents of option
(a), §3 P6: Fatras to half a turn, Geant4 crossings beyond, a fixed 0.005 ns seam), compared with **the same events
and seeds on the present chain** (the paired design of STR l.1505-1507). Pile-up only; no signal quantity. One design
point must be fixed before it runs: the top-up. Proposed: total density per layer kept at the TDR normalisation (the
top-up of a layer reduced by the number of injected crossings), so that the row measures the arrangement at fixed
number, which is exactly what [L15] leaves open; the alternative (arcs on top of an unchanged top-up, about 30 % more
Fatras-level hits) mixes it with a density change that the top-up rows of B6 already vary. Fixed with the third review: the density is fixed at the raw level at which the top-up ratios were derived (before CKF); the top-up crossings of the varied sample are a subset of the nominal sample's draws (the last ones of each layer are dropped), so that the pair differs only by the exchange of random crossings for arcs; where a layer of an event has more injected crossings than top-up crossings its top-up is zero and the excess is reported. The injected crossings pass the chain and the top-up does not, so the chain stage of the varied sample holds about 37 % more hits (+ 0.5–1 CPU-h, inside the range below).

*Where it can be read.* At the rungs where direct pile-up counts exist: R04, R05 and R06 (v1 direct rates 171.6,
49.7 and 0.247 per trial [U: STR l.249, l.747, l.1185]). R07 (7.3×10⁻⁴ per trial) is not evaluable at any affordable
size.

*Size.* The B6 criterion: statistical error on ln(B_var/B_nom) below 0.1 at R06 (STR l.1500-1501). Unpaired Poisson
counting needs 200 counts per sample at R06: 810 trials, **≈ 200 events** as a minimum [E]. Proposed: **600 events**
(2,400 trials), the size of every other reduced B6 background row (STR l.1513): 593 counts expected at R06, unpaired
error 0.058; at R04–R05 the Poisson error is below 0.005 [E; 17]. These are lower bounds on the error (the candidates
of one event are correlated; the bootstrap over events gives the number), and upper values for the paired design.

*Cost* [ESTIMATE from measured unit costs; 17]: Geant4 for the arcs 200 × 52.6 charged particles × 0.41 ms per
firing [V: p2-c-t-g4] = 4.3 s per crossing; chain 12.3 s per crossing and finder 11.3 s per trial, 4 trials
[V: p2-a-day0-pu1]. Varied sample, 600 events: 10.3 CPU-h at fixed density; 13.2–16.1 CPU-h with 30 % more hits
(finder cost linear to quadratic in the hits; its scaling is not measured [U]). Nominal partner on the same events
9.6 CPU-h, unless an existing sample of the same events serves. Slice and validation of the injection inside a
pile-up event ≈ 2 CPU-h (judgement). **Total 22–28 CPU-h (12–18 with an existing partner)**; 35–45 CPU-h at 1,000
events. Optional signal arm (the B6 signal column, read only after the closure verdicts): 10–12 CPU-h. With the test
the projection stays at 4,690–4,872 CPU-h. New code: the option-(a) injection applied to every low-p_T particle of a
pile-up event; a few hours of work [E, from the executor's estimate for option (a)], with its own check for
duplicates at the seam.

*When.* By decision point 2 (day 15), two days before the freeze (day 17, STR l.2267), on development-role events: its result is a property of the chain,
not a closure verdict. After the freeze the outcome "effect" could no longer lead to a chain fix. A chain fix regenerates the whole pilot (≈ 142 CPU-h, about three days on two lanes) and moves the day-15 reading; this exposure exists from the moment the B1 part is launched on the present chain.

*Pre-declared reading.* r(R) = B_var/B_nom of pile-up candidates per trial at R04, R05, R06, counted as the frozen
object of [SD4], errors from the bootstrap over events. Read in addition, at no CPU and without a verdict: (a) in the varied sample, the candidates at R04–R06 with at least one double-crossing layer whose two hits come from one particle, one of them beyond half a turn (truth): the direct count of a looper together with pile-up, which r alone could hide if the loss of random crossings and the gain of arcs cancel; (b) r at the 2S crossing rungs (N_2S2 ≥ 1, 2, 3 on top of R04–R06, STR §4.0 point 7), because 20 % of single loopers cross a 2S layer twice in both sensors [V: p2-c-px-lpds] and the missing crossings are largest in the outer layers.
- Evaluated (B6-a): error on ln r below 0.1 at R06. If not reached with 600 events, the row is reported as not
  evaluated at R06; no events are added without asking.
- **No effect:** |ln r| ≤ 0.1 and within 2σ of zero at all three rungs, and no trend of ln r from R04 to R06 beyond
  2σ. Then [L15] is stated with a measured size ("the pile-up count at R04–R06 changes by less than …"); the chain
  is kept. It remains a statement about R04–R06: the pile-up term at the candidate selections (R08 and beyond) is an
  extrapolation in either chain.
- **Effect, "robust" by the frozen B6-b threshold** (|ln r| ≤ ln 2 at R04–R06, STR l.1502): if r(R06) > 1 the pile-up estimate is multiplied by r(R06), with a width of its bootstrap error and the width of STR §4.0 point 7 counted from R06; no credit is taken for r < 1. This is a correction of an estimate known to lack hits, not a symmetric nuisance. [SD17] allows it: the variation is not a round number but is defined by a source (Geant4 transport of the same particles), like the top-up limits and the tune (STR l.1477-1478). **With D2 the user chooses** whether the binding day-15 reading uses the corrected pile-up term (recommended; stricter than the pinned Df-11) or Df-11 stays as pinned and the corrected reading is reported beside it. The numbers that make this matter: with the pile-up median
  × 1.10 / 1.25 / 1.5 / 2 an empty pilot reads 162 / 163 / 165 / 169 at R09 and 246 / 271 / 294, 256 / 283 / **308**,
  273 / **303** / **329**, **302** / **336** / **365** at R08 [E; 17]. 
- **Effect, "not robust"** (|ln r| > ln 2 at a rung, or ln r(R06) − ln r(R04) above zero by more than 2σ of that difference): named in the
  limitations and at abstract level; the user is asked to choose between the correction of the robust case and fixing the chain (D1 (b)),
  before the freeze.

*What the test would not cover:* the single-interaction and hard-scatter terms' own later arcs (products), the
unread populations of D6, rungs beyond R06, and the signal unless the signal arm is added.

*The alternative of doing nothing more:* cost 0; [L15] stands on the single-looper zero with its bound of 2.2×10⁴
events; the paper states that the effect of the missing arcs on the pile-up background is not measured.

## 2. Other Phase-2 measurements behind this addendum ("Phase 1 assumed / Phase 2 found / implications")

1. **Unit costs.** Assumed 45 ms per no-pile-up hard-scatter event (STR l.356). Found 127 / 171 / 571 ms for Z(νν) /
   W(τν) / tt̄ 1ℓ per generated event [V: p2-c-t-hs0], 327 ms for tt̄ with forced W decays [V: p2-c-t-ttf]; the pilot's
   Z(νν) jobs, with the extended summary, cost 133.8 ms per event (662.7–677.7 CPU-s per 5,000) and 33.84 kB
   [V: markers of p2-c-pilot-znn-00000…2, read by me]. Implications: §4.4, §5.
2. **Preselection.** Assumed pilot and pool events are preselected events. Found: the generator gives events with
   truth MET > 200 GeV; v1's preselection weights them: mean 0.4308 ± 0.0049 / 0.2604 ± 0.0043 / 0.1180 ± 0.0031, in
   two weight classes (≈ 0.98 and ≈ 0.05) [V: p2-c-t-hs0]. Implication: M of a sample is Σw/w_max of its full-weight
   class (0.4396, 0.2657, 0.1205 of the generated events), and the 0.05 class is a second counted term (STR l.1564).
3. **Geant4 vertices.** Assumed the v1 rates (straight-line decays at 30–1000 mm; interactions at three radii ×
   0.22). Found [V: p2-c-part-0, 1.5×10⁶ firings of every pool species]: 245,945 vertices, each in exactly one class
   (§3 P3). Reproduced independently by both reviewers.
4. **Hand-over.** Assumed Fatras takes every Geant4 product at the vertex and v1's `Truncate` gives the parent's
   hits. Found: slow fragments give hits before the vertex time, so products are followed by Geant4 to the exit of
   their slab and those with β < 0.1 are not handed over [V: p2-c-val-b1]; the running Fatras neither decays nor
   absorbs hadrons [V: p2-c-part-fatras]; and the parent's hits after half a turn do not exist (§1, §3 P6).
5. **Toys.** Assumed "may double" (STR l.1720-1722). Found ×17 at 60 parameters with pyhf's numpy backend
   [V: p2-c-t-pyhf; reproduced on another node, p2-c-toy-base], and a configuration of the same pyhf that brings it
   back (§5) [V: p2-c-toy-jax, -ref, -tune, -fix].
6. **Fatras step limit** (all samples; not caused by this addendum): 0.03–0.07 particles per hard-scatter event,
   mostly conversion positrons, are dropped with all their hits [V: logs of p2-c-t-hs0, p2-c-t-ttf; 0.032 per event
   in p2-c-px-znnb]. Open point 5.

## 3. Definitions

**P1 Z(νν) pilot: 2.3×10⁶ generated events** (STR l.869), **running since 2026-11-16 16:39** (campaigns
`p2-c-pilot-znn-00…15`, 460 jobs; with `pilot.mb`, campaign `p2-c-pilot-mb`, 40 jobs). The first three Z(νν) files
and one minimum-bias file pass all hard checks [V: p2-c-px-pv1-0.json, `all_hard_checks_pass: true`, 4 files, read].
m_Z counts events of the full-weight class: M = 1.011×10⁶, one count = 41.2 events for all SM processes and the
multijets (24.8 for Z(νν) alone); an event of the 0.05 class is counted in a second term at 2.1 events per count [2].
**"41" is provisional:** it uses v1's preselection and is recomputed with the v2 MET model at day 12 from the
generator-level summary stored with every event. **What that summary holds (correction of version 3)** [V:
`PILOT_READY_xavier_2026-11-16_15-09.md` §3]: truth MET and neutrinos; **`jets` (anti-k_T 0.4, p_T > 20 GeV,
|η| < 4.7) and `jets10` (p_T > 10 GeV, |η| < 5)**, not "down to 15 GeV"; e and μ above 5 GeV, photons above 10 GeV,
τ with visible momentum; scalar and vector sums of the visible final state in |η| < 5 and < 3; p̂_T, weight; and the
final hadrons and photons with |η| < 1.5 and p_T > 0.3 GeV, which are the parent pool of `pilot.c0.hs`. **The full
particle list is not stored:** a MET model that needs another jet radius, another clustering input or leptons below
5 GeV needs the events regenerated at generator level from the stored seeds, ≈ 29 CPU-h for 2.3×10⁶ [E; 8]; the chain
is not rerun for that. Events can be appended (new chunks, nothing existing touched).

**P2 Parents, road, and what is outside** (unchanged from version 3).
- *Pool.* Every π±, K±, p, K⁰_L, n, γ produced within 1 mm of the interaction point with 0.5 < p_T < 20 GeV and
  |η| < 1, natural Pythia mixture, uniform azimuth: 7.13 per minimum-bias interaction, 0.3405 inside a road of
  half-width 0.15 [V: p2-c-part-0].
- *N_t* of a class = N_trig × 200 × 0.3405 × (class vertices per firing) × 1.022 [1]. The last factor is the
  hard-scatter share, an upper-side planning value: v1's rates give 0–3 %, a first direct count 1.3 % (0.872 ± 0.032
  pool parents inside the road per triggered Z(νν) event against 68.1 from minimum bias [V: p2-c-px-hsg-r0; 1]).
- *Hard-scatter parents.* Own sample **`pilot.c0.hs`: 2×10⁶ vertices in the natural mixture of the seven classes**,
  from parents inside the road of their own event, with the true offset to the event's MET road stored. Parents: the
  stored hadron list of the 2.3×10⁶ Z(νν) pilot events, drawn in proportion to the event weight: 8.3×10⁵ distinct
  parents, 19 firings and 2.4 vertices each [E from V; 3]. **Consequence for the order: this sample cannot be started
  before the Z(νν) files are complete** (§5). Rule 1 reads it as **one term**: N_t = 7.9×10⁶, one count = 4.0
  events; the seven class samples are then normalised to the minimum-bias share alone. Its events of the classes
  after a turn use option (a) (mode `autoh`, P6).
- *Road orientations.* **The count m of a class sample is the number of (event, road orientation) passes over 21
  fixed orientations of full width 0.30, axes at φ_road + 2πk/21** (STR l.864-866), with N_t as defined. 21 × 0.30 =
  6.30 against 2π: over-read by 0.27 %, strict side [6]. An event that passes in more than one orientation is counted
  each time and flagged. For `pilot.c0.hs` the road is the event's own; **hard-scatter hadrons outside the road are
  not fired**: 35.5 − 0.87 per triggered event [V], 1.8×10⁸ vertices in 3 ab⁻¹ at the minimum-bias yield [E]; a
  candidate from them in the MET road is read by nothing in this draft. The fraction of off-road passes in the
  minimum-bias samples is reported at day 7 as an alarm. Reading them directly: D6 (c).
- *Lower p_T edge.* The edge at 0.5 GeV is a convenience of v1's rate definition, not a bound. Parents with
  0.3 < p_T < 0.5 GeV are 5.20 per interaction, 73 % as many as the pool [V: p2-c-px-mbb-big]. Their vertex yield is
  not measured; at one to two times the pool's, **N_t = 2.6–5.2×10⁸, 0.7–1.4 times the seven classes together**
  [E; 6]. The check sample `pilot.c0.lowpt` (2×10⁵ vertices, mode `autoh`) reads 1,300–2,600 events per count: **its
  zero allows 1,500–3,000 events and bounds nothing at the scale of 300.** It is an alarm, not a term: no zero-count
  allowance enters rule 1 for it; one own-hit pass at a T2 candidate rung is by itself above 300 and pauses the
  study. These are also the parents that curl most: [L15] applies to their products in full. Reading the population
  as a term: D6 (b). No written bound (COM B1-e) excludes these parents.
- *|η| > 1.* Parents with p_T > 0.5 GeV at 1 < |η| < 1.5 are 3.64 per interaction, 51 % of the pool [V:
  p2-c-px-mbb-big]: N_t = 1.9×10⁸ at the pool's vertex yield, not measured there [E; 6]. `pilot.mb` keeps a second
  pool (0.3 < p_T < 20 GeV, |η| < 1.5, outside the main pool), so a check sample can be made later without a new
  minimum-bias run. None is in the pilot: not tested.

**P3–P5 The partition and the terms** (unchanged) [V counts: p2-c-part-0; N_t and events per count: E, [1], [2]].
"First arc": transverse path from the origin ≤ πR. N_t includes the factor 1.022; "per count" is with the
hard-scatter share on its own sample.

| class (vertices in 1.5×10⁶ firings; by parent π± / K± / p / K⁰_L / n / γ) | term | stream | N_t | M | per count | parent hand-over (P6) |
|---|---|---|---|---|---|---|
| decays of π±, K± on the first arc, any radius (53,063: 26,641 π±, 26,422 K±) and K⁰_L decays (2,906) | **DIF** | `pilot.c0.dif` | 1.061×10⁸ | 4×10⁶ | 25.9 | radius cut |
| decays of π±, K± after the first turn (51,441: 35,970 π±, 15,471 K±) | **DIF-C** | `pilot.c0.difc` | 9.75×10⁷ | 4×10⁶ | 23.9 | **option (a)** |
| inelastic, first arc, beam pipe (2,583: 1,798 / 246 / 215 / 112 / 206 / 6) | **NI 22 mm** | `pilot.c0.ni22` | 4.90×10⁶ | 10⁶ | 4.8 | radius cut |
| inelastic, first arc, TBPX L1 (3,502: 2,437 / 380 / 259 / 160 / 251 / 15) | **NI 30 mm** | `pilot.c0.ni30` | 6.64×10⁶ | 10⁶ | 6.5 | radius cut |
| inelastic, first arc, TBPX L2 (3,496: 2,387 / 375 / 276 / 192 / 253 / 13) | **NI 61.5 mm** | `pilot.c0.ni61` | 6.63×10⁶ | 10⁶ | 6.5 | radius cut |
| inelastic, first arc, every other layer (50,083: 35,874 / 5,035 / 3,469 / 2,489 / 3,083 / 133) | **NI-X** | `pilot.c0.nix` | 9.49×10⁷ | 4×10⁶ | 23.2 | radius cut |
| inelastic after the first turn, any layer (26,239: 24,271 π±, 1,185 K±, 783 p) | **NI-C** | `pilot.c0.nic` | 4.97×10⁷ | 2×10⁶ | 24.3 | **option (a)** |
| **sum of the B1 classes: 193,313** (+ 52,583 conversions + 49 other = 245,945 = all vertices) | | | **3.66×10⁸** | 1.7×10⁷ | | |
| the hard-scatter share of all seven (2.2 % of the sum, upper side) | one term at day 15 | `pilot.c0.hs` | 7.9×10⁶ | 2×10⁶ | 4.0 | by class (`autoh`) |

- Conversions of primary photons (52,583) are not B1: by the frozen route table (STR §2; §4.4 point 1, l.738-739)
  the conversions of pile-up photons (2.4 per triggered event in the road, 1.0×10⁸ in 3 ab⁻¹ [V; 1]) belong to B2,
  where Fatras makes them; rule 1 reads them through the pile-up estimate only. The 49 "other" vertices are recorded.
- From 6.8×10⁷ to 3.66×10⁸ [1]: first-arc π/K decays inside v1's own range 30–1000 mm give N_t = 8.15×10⁷ against the
  frozen 6.51×10⁷ (×1.25); first-arc decays below 30 mm and beyond 1 m add 1.91×10⁷ and K⁰_L decays 5.5×10⁶; the
  three radii go from 3.1×10⁶ to 1.82×10⁷ (the factor 0.22 removed; Geant4 yield; neutral parents); the three new
  classes are 2.4×10⁸, two thirds of the total.
- Decays after the first turn: 61 % (31,238 of 51,441) come from parents above 0.57 GeV [V: second review]. No
  written bound (COM B1-e) excludes these decays, so DIF-C is a term. If the bound is written and checked before the
  freeze, the pre-registration may drop it; rule 1 at day 15 reads it.
- In the likelihood of Phase 4a the hard-scatter share is inside each of the seven terms, as frozen (STR l.726-727);
  the separate sample is a day-15 device.

**P6 Hand-over (review finding A-1): settled by measurement.**
Products are followed by Geant4 to the exit of the slab of their vertex; products with β < 0.1 there are not handed
to Fatras (0.07–0.12 per NI event [V: p2-c-val-b1x]); the Geant4 crossings of the parent before the vertex are stored
with every event. The parent:
- *The fault, as version 3 reported it.* v1's `Truncate` removes the parent's hits by radius (`run_chain.py`
  l.284). In version 2's validation, 433 of 1,464 (DIF-C) and 514 of 1,463 (NI-C) pre-vertex crossings of the Geant4
  parent had no Fatras parent hit, on a measure that counts a surface once [V: p2-c-b1yv; 7]. Version 3 proposed a
  cut by time and left its re-validation as a placeholder.
- *The re-validation* [V: campaign p2-c-px-tr, 27 jobs = 9 streams × radius / time / both, 2,000 events each, the
  same vertices and seeds; validation p2-c-px-val2; `outputs/A1_TRUNCATION_xavier_2026-11-16_15-40.md`; every number
  below re-read from `p2-c-px-val2-0.json` by the script, 14]. Measure: Geant4 crossings of a barrel counting surface
  by the parent before its vertex **with multiplicity**, all events with a charged parent.

| stream | cut | Geant4 crossings | without a parent hit | parent hits later than the vertex time | ≤ 2 % |
|---|---|---|---|---|---|
| DIF | radius / time | 18,735 | 20 (0.11 %) / 47 (0.25 %) | 19 / 0 | pass / pass |
| NI 30 mm | radius / time | 893 | 0 / 4 (0.45 %) | 0 / 0 | pass / pass |
| NI 61.5 mm | radius / time | 2,627 | 0 / 29 (1.10 %) | 0 / 0 | pass / pass |
| NI-X | radius / time | 15,368 | 15 (0.10 %) / 506 (3.29 %) | 208 / 0 | pass / **fail** |
| DIF-C | radius / time | 49,048 | 28,692 (58.5 %) / 19,802 (40.4 %) | 0 / 0 | **fail / fail** |
| NI-C | radius / time | 53,131 | 35,335 (66.5 %) / 24,021 (45.2 %) | 0 / 0 | **fail / fail** |

  (NI 22 mm: the beam pipe is inside the first layer, no pre-vertex crossing. "Both" equals the worse of the two in
  every stream.) **First-arc streams: v1's radius cut is kept**; the time cut is no better anywhere and fails for
  NI-X. What the radius cut leaves: parent hits later than the vertex time, 19 of 18,792 (DIF) and 208 of 15,356
  (NI-X, 1.4 %): extra hits, the strict side for a ceiling on own hits. **After-a-turn streams: no truncation
  passes**, because the hits beyond half a turn do not exist (§1): the Geant4 parent of these classes reaches its
  vertex at a median of 1.0 turn.
- **The second review's measure missed the size of the fault.** Counting a surface once, a return arc over surfaces
  already crossed on the way out is invisible: with the radius cut that measure reads 435 of 1,470 (DIF-C) and 498
  of 1,475 (NI-C), 30 % and 34 %, where 58.5 % and 66.5 % of the crossings are missing; with the time cut it reads
  20 and 16, 1.4 % and 1.1 %, which would have passed a 2 % check, while 40 % and 45 % are missing [V; 14]. **The measure with multiplicity is the criterion** (`a1_*` fields of `p2x_validate.py`,
  threshold 2 %).
- **Option (a), adopted for DIF-C and NI-C** [V: campaign p2-c-px-hy, 8 jobs, the same vertices and seeds;
  validation p2-c-px-val3; `outputs/A1_OPTION_A_xavier_2026-11-16_16-17.md`; re-read from `p2-c-px-val3-0.json`, 14].
  The Fatras parent is kept up to the Geant4 vertex time (Fatras stops it at half a turn); the stored Geant4
  crossings of the parent before the vertex that are later than its last kept Fatras hit by more than 0.005 ns
  (1.5 mm of flight; fixed before the run, not tuned) are added as hits with the parent's barcode at the Geant4
  position, time and momentum, and go through digitisation, seeding and CKF like every other hit (class
  `HybridParent` of `p2x_b1.py`; no v1 file is changed).

| stream | mode | Geant4 crossings | without a parent hit | parent hits without a Geant4 crossing | ≤ 2 % | before (radius / time) |
|---|---|---|---|---|---|---|
| DIF-C | hybrid | 49,048 | 18 (0.04 %) | 785 (1.58 %) | **pass** | 58.5 % / 40.4 % |
| NI-C | hybrid | 53,131 | 25 (0.05 %) | 828 (1.54 %) | **pass** | 66.5 % / 45.2 % |
| mixed slice, hard-scatter type | `autoh` | 27,044 | 30 (0.11 %) | 297 (1.09 %) | pass | 37.9 % / 25.8 % |
| mixed slice, low p_T | `autoh` | 34,546 | 41 (0.12 %) | 694 (1.97 %) | pass | 60.2 % / 47.2 % |
| DIF, NI-X | `autoh` (= radius) | 18,735; 15,368 | 20; 15 | 9; 3 | pass | identical to the radius rows |

  V4-1 closure passes in all 8 files; no NaN; no product hit before its production time in these 2,000-event files (at 25,000 events the check fails: (vi) below); no slow product handed
  over; the class of every event equals the class recomputed from its vertex; reruns identical (DIF-C r0 = r1, NI-C
  r0 = r1). The 1.5 % "hits without a Geant4 crossing" are duplicates at the seam (the last Fatras hits and the first
  injected crossings of one passage when the two codes differ by more than 0.005 ns): extra parent hits, strict side.
  12.6 (DIF-C) and 14.0 (NI-C) parent hits per event come from Geant4.
- **What option (a) does not do, and what is not yet shown.** (i) **The products of the vertex, and every other
  particle of every sample, still stop at half a turn** ([L15]). (ii) The injected parent hits carry Geant4's
  scattering and energy loss, the first half turn Fatras's; on the first half turn the two agree for 98–99.9 % of the crossings. In position the two parents differ on the same surface of the first arc by 0.4–0.8 mm (median) and 5–8 mm (90 %) in rφ [V: ab_abs_drphi of p2-c-px-val2-0.json, radius rows], so the hybrid parent has a step of that size at the seam, far above the finder's 30 µm tolerance; the ≤ 2 % criterion counts hits per surface and does not see it, and the injected hits are the Geant4 crossings themselves, so the criterion is a closure of the injection, not an independent test. No bias of H is expected from the step (the alignment of a curling parent's arcs in one plane is accidental); none is measured. (iii) The mixed slices used old slice pools (repeated parents), not the pools of P2. (iv) **The
  validator's overall flag reads `all_hard_checks_pass: false` for the six option-(a) files with turned parents**
  [V; 14]: its check "no parent hit beyond the vertex radius" does not apply to a parent that has turned (19,643 and
  25,945 such hits are the correct earlier arcs); every other hard check passes. Until `p2x_validate.py` makes that
  check class-aware, "one validated job per stream" cannot read all-pass for these streams; this is a condition for
  releasing them (P7). (v) An injected hit close to a sensor edge can be lost in digitisation at the 10⁻⁶ level, as
  for any hit (looper report, addendum); the B1 job counts such losses. (vi) **Found after this draft (LOG.md 18:15; campaigns p2-c-pa-val0, p2-c-pa-dg1):** at 25,000 events per file the hard check "no product hit before the vertex time" fails for NI-X (6 hits) and NI-C (1 hit). Five are correct (secondaries made along the parent's path before its final vertex; the check is now per product). Two hits, in one of 25,000 NI-X events, come from a fragment with β = 0.134, above the β cut of 0.1, with Fatras hits at t = −32 ns: a residue of the slow-fragment pathology, about 4×10⁻⁵ per NI-X event from one event, of order 160 events in the 4×10⁶ NI-X pilot sample. Its rate on 1.5×10⁵ NI events and a β scan (0.15, 0.2, 0.3) are being measured. **Release condition:** no stream with nuclear interactions (NI 22 / 30 / 61.5 mm, NI-X, NI-C, pilot.c0.hs, pilot.c0.lowpt) is released before this is settled, by a per-event flag that removes such events from the count m and reports their number, or by a higher β cut; a change of the β cut is put to the user.
- The pure second variant of STR l.744-746 (all parent hits from Geant4 crossings) is not adopted: it would discard
  a Fatras parent that agrees with Geant4 on the first half turn.

**P7 Streams and state of the pilot code** [facts from `PILOT_READY_xavier_2026-11-16_15-09.md`, the two A-1 reports
and `LOG.md`; nothing run by me on a worker].
- Streams: `pilot.mb`, `pilot.g4`, `pilot.hs0.znn`, `pilot.c0.{dif,difc,ni22,ni30,ni61,nix,nic,hs,lowpt}`. One vertex
  per event; road and PV stored, not fixed at generation.
- **Running:** `pilot.mb` and `pilot.hs0.znn` (P1). Their scripts and inputs are frozen until the last job is done
  (hashes in the plan file).
- **Run at slice size, with results:** the production vertex job `p2x_g4prod.py` (campaign p2-c-px-g4: identical
  hashes for the same seed; 'all' pass 0.338 ms per firing all-in, 1,060 MB and 226 MB of vertex files per 2×10⁶
  firings; 'ni' pass 0.054 ms per firing; one class per vertex asserted) and the chain job `p2x_b1.py` with every
  truncation mode on every stream (p2-c-px-tr, p2-c-px-hy) [V].
- **Not shown, and therefore not claimed:** no B1 campaign file is written; the hard-scatter and low-p_T streams
  were run on old slice pools, not from the Z(νν) hadron list and the `pilot.mb` pools; the validator's flag is not
  class-aware (P6 (iv); a per-mode check was written into p2x_validate.py at 17:25 by the successor session and has not yet been run on an option-(a) file); no option-(a) job has run at production size (the first-arc streams at 25,000 events pass the parent check, 0.00–0.18 %, and show the residue of P6 (vi)). **Nothing here says the B1
  production is ready.** Commitment: one job of every stream is passed through `p2x_validate.py`, with the criterion
  ≤ 2 % with multiplicity and the class-aware radius check, before the bulk of that stream is released. The β cut is
  a campaign parameter (0.1). 'all'-pass Geant4 jobs hold at most 2×10⁶ firings: 62 jobs of 11 min [8], firing 3 %
  more than the smallest class needs.
- The partition file `outputs/partition_p2-c-part-0.json` was written by hand-run code after the class definition
  was last edited; both reviewers reproduced every count from the stored vertices. The pilot's own partition,
  written by `p2x_g4prod.py` with its code hash, supersedes it.

## 4. Replacement tables [E] (unchanged from version 3; every number reprinted by the version-4 script)

### 4.1 Rule 1: empty-pilot reading and crossings [4]

B₅₀ with every count zero and the first count at which the reading is at or above 299.1 with the others at zero
(medians of 10⁵ draws, common random numbers; three other seeds move the draft row by at most 1.2). R08 over the
strategy's pile-up range (STR l.2819). **The pile-up term of every row is the present chain's estimate** (§1.5 for
what a shift of it does).

| reading | empty pilot, R09 | R08 at pile-up 88 / 118 / 148 | pause at m_Z: R09; R08 | pause at counts in one of DIF, DIF-C, NI-X, NI-C: R09; R08 |
|---|---|---|---|---|
| STR as frozen (4 B1 terms, v1 N_t, 10⁶ per sample, 18.1 per Z count) | 76 | 156 / 181 / 204 | 12 (299.6; a tie pauses); 8 / 7 / 6 | DIF 4; 3 / 2 / 2 |
| seven terms, 10⁶ per sample (the strategy's pilot sizes) | **389** | **467 / 491 / 515** | pauses when empty | pauses when empty |
| seven terms, proposed sizes, hard-scatter parents not read (H3) | 159 | 237 / 260 / 282 | 4; 2 / 1 / 1 | 6; 3 / 2 / 1 |
| **DRAFT: seven terms, proposed sizes, + `pilot.c0.hs` (2×10⁶) as one term (H1)** | **161** | **238 / 262 / 284** | **4; 2 / 1 / 1** | **6; 3 / 2 / 1** (35; 16 / 10 / 4 in the hard-scatter sample) |
| the same, hard-scatter sample as seven weight classes | 185 | 262 / 286 / **307** | 3; 1 / 1 / 0 | 5; 2 / 1 / 0 |
| H2: a 2×10⁵ hard-scatter sample as one term | 196 | 273 / 297 / **319** | 3; 1 / 1 / 0 | 4–5; 2 / 1 / 0 |
| H2 as seven weight classes | **432** | **509 / 533 / 555** | pauses when empty | pauses when empty |
| draft + hard-scatter hadrons outside the road (7.3×10⁶ vertices, one term) | 186 | 263 / 287 / **309** | 3; 1 / 1 / 0 | 5; 2 / 1 / 0 |
| draft + low-p_T parents as a term at 25 events per count | 186 | 263 / 287 / **309** | 3; 1 / 1 / 0 | — |
| draft, Z(νν) pilot 3.5×10⁶ generated | 148 | 225 / 249 / 270 | 6; 3 / 2 / 2 | 6–7; 3–4 / 2–3 / 2 |
| draft, Z(νν) pilot 5.23×10⁶ generated | 139 | 216 / 239 / 261 | 9; 5 / 4 / 3 | 7; 4 / 3 / 2 |
| draft, every B1 sample doubled | 102 | 179 / 203 / 225 | 5; 3 / 3 / 2 | 16–17; 10–11 / 8–9 / 6–7 |
| four terms (lenient), proposed sizes; with H1 | 85; 89 | 163 / 187 / 209; 167 / 190 / 212 | 6; 4 / 3 / 3 | DIF 9; 6 / 5 / 4 |
| four terms (lenient), 10⁶ per sample | 147 | 227 / 252 / 275 | 4; 2 / 2 / 1 | DIF 2; 1 / 1 / 1 |
| three terms on the same events; with H1 | 96; 99 | 174 / 198 / 220; 177 / 201 / 223 | 5; 4 / 3 / 2 | 8–9; 5–6 / 4–5 / 4 |
| one term on the same events; with H1 | 62; 65 | 141 / 164 / 186; 144 / 168 / 190 | 6; 4 / 4 / 3 | 11; 8 / 7 / 6 |
| draft, pile-up median × 1.25 (illustration of [L15], §1.5) | 163 | 256 / 283 / **308** | | |
| draft, pile-up median × 1.5; × 2 | 165; 169 | 273 / **303** / **329**; **302 / 336 / 365** | | |

Plainly. With 10⁶ events per sample, as the strategy sized the pilot, the study would pause on no information. With
the proposed sizes, at R09 the rule tells "empty" (161) from "a handful" (4 Z(νν) counts, or 6 in a B1 sample). At
R08 it pauses on 1–3 counts in any sample, and at the upper pile-up estimate on one count anywhere. Every stricter
option of D5 and D6 pauses on an empty pilot at the upper R08 estimate, and so does a pile-up estimate 25 % higher.
A pilot that could not pause at R08 on one count needs about twice these samples (+ 46 CPU-h for B1, + 109 CPU-h for
Z(νν)).

### 4.2 The number of terms (decision D4) [4], [5]

*What the strategy's convention says.* STR l.1563: a counted factor has "λ ≥ 0, the expected simulated count …
m ~ Pois(λ), m passing events out of M … λ drawn from Gamma(m + 1)": one such factor per term of the likelihood. STR
l.1564: "one λ per weight class of constant weight w_s". STR l.1575-1578: "*One zero per term.* If the route of a
term contains more than one counted factor with m = 0, only the first in the order of the cuts keeps its Gamma
constraint; the later ones enter at 1" — this limits the zeros inside one term's route, not across terms. STR
l.726-727: the terms of B1 are "decays in flight (DIF) and nuclear interactions at r = 22, 30 and 61.5 mm (NI)". STR
l.2733-2734: rule 1 reads "decays in flight and each nuclear-interaction radius … on their own pilot samples". So in
the frozen design a term is a population with its own N_t, sample, Gamma(m + 1), ceiling test and closure test, and
an empty term contributes N_t/M × Exp(1) to the reading whatever the other terms hold.

*What follows.* The empty-pilot reading grows with the number of terms on the same events. This is the
one-zero-per-term convention, not information about the background:

| B1 terms | empty pilot R09 (hard-scatter parents not read; with H1) | likelihood | closure family K; re-test level | ceiling family T_c; α_c | false FAIL removes a selection | 4a cost |
|---|---|---|---|---|---|---|
| **seven (draft)** | 159; 161 | seven counted B1 factors per candidate, each with its test | 13; 0.0038 | 22; 0.00227 | 7.0–9.9 % | + 41 CPU-h (three closure designs, to be written) |
| four, others left out (lenient) | 85; 89 | as frozen; 2.4×10⁸ of 3.7×10⁸ vertices in no term | 10; 0.0050 | 19; 0.00263 | 6.9–8.9 % (frozen) | 0 |
| three (decays; three radii; other interactions) | 96; 99 | three factors; each sample a natural mixture of its classes | 9; 0.0056 | 18; 0.00278 | 6.9–8.6 % | not costed: B1-a redesigned |
| one | 62; 65 | one factor for all of B1 | 7; 0.0071 | 16; 0.00313 | 6.7–7.9 % | not costed: B1-a redesigned |

*The draft is seven*, because it extends the frozen term list without bending the convention: the frozen rule
already had one allowance per NI radius, and the three new classes have no v1 count and no test, which is what a
term with its own ceiling is for. It also keeps the option of dropping DIF-C if the bound of B1-e is written.
*Four* is cheaper only because it leaves two thirds of the vertices out on no evidence. *Three or one* are honest
alternatives: a count in a natural mixture is an unbiased estimate whatever the mixture, and fewer terms cost fewer
allowances. Their price: the frozen closure designs cannot be kept (DIF is tested at R06–R07 on enriched overlays,
the radii at R05 by the rung split, STR l.1045-1059; a merged term needs one new design, and B1-a was frozen at
Gate A); a count in a rare class is read at the merged transfer factor (one NI 22 mm count would read 21.6 events
instead of 4.8); a class cannot be dropped later on its own bound; and the two after-a-turn classes, whose parent
hand-over differs (P6), could no longer be read apart. This draft does not choose them and does not hide them.

*The same question for the hard-scatter sample.* Read literally, STR l.1564 makes `pilot.c0.hs` a second weight
class of each of the seven terms: seven more zeros, 185 instead of 161. The draft reads it as one term, because the
sample is one natural mixture; this is 24 events more lenient than the literal reading, and it is put to the user as
D5.

### 4.3 Wording of rule 1 and Df-11 where numbers or samples appear; superseded lines

The definition of the rule is unchanged: every term from the samples that exist at day 15, max(zero-count floor,
N_t·H), H = Gamma(m + 1)/M on own hits before CKF, no pool floor, one Z(νν) count for all SM processes and the
multijets, limit 300, at least 10⁵ draws for the binding median, a tie pauses (STR l.2730-2757, l.2949). The pile-up
term is the present chain's estimate, or that estimate corrected by the robustness test if D2 is accepted, it shows an increase and the user chooses that it enter the binding reading (§1.5); [L15] is not a term of the rule.

Replacement for the sentences that name samples and numbers (STR l.2733-2737, l.2755-2756, l.2949): "Each B1 class
of addendum 1 (DIF, DIF-C, NI 22, 30, 61.5 mm, NI-X, NI-C) is read on its own pilot sample at N_t/M with the
minimum-bias N_t and the M of the addendum's table, m being the number of (event, road orientation) passes over 21
orientations; the parents of DIF-C and NI-C carry their Geant4 crossings beyond half a turn. The hard-scatter share
of the seven classes is read as one term on `pilot.c0.hs`. Every SM hard-scatter process and the multijets are read
at the H per full-weight event of the Z(νν) pilot (M = Σw/w_max; 1.011×10⁶ with v1's weights, replaced by the day-12
MET model), with a second term for the low-weight class. `pilot.c0.lowpt` enters only with a count." The sentences
"≈ 12 Z(νν) pilot counts" and "between 3 and 4 decays-in-flight counts" become the crossings of §4.1.

Superseded where they stand in STR (the text is not edited; these numbers or statements are replaced by this
addendum): §0 l.44-48, l.52, l.79-80, l.95-101; §2 l.210 (the looper entries "168 b"), l.230 and l.232 ("loopers"
among what Fatras traces: first half turn only); §4.0 l.407-411, the battery rows l.421-424, l.472; §4.4 l.726-727
(term list), l.728-730 (the 1,000 looper events kept as a diagnostic population: §1.1 point 1), l.744-746 (truncation and the choice between two variants: decided per stream, P6), l.788 ("a true ceiling": true inside the chain; the later arcs are in neither H nor the overlays, [L15] (iii)), l.797, l.811-813,
l.866-871 (pilot sizes), l.876-878, l.881-886 (rates), l.902-916 (Table 4.4a), l.935-943, l.955, l.968-976 and l.984,
l.1027, l.1071 (looper row), l.1091; §4.7 l.1306 (loopers inside the B4 terms: first half turn only), l.1308-1313; §4.11 l.1720-1722 (toy cost "may double"); §4.12 l.1813; §4.17
l.2104 (sample 11), l.2111-2114 (samples 17, 18, 18a, 18b), l.2115 (sample 19); §7 l.2285-2299 (a limitation [L15] is
added); §8 l.2345-2348; §11.2 l.2514, l.2517 (pilot lines); §11.7 l.2733-2737, l.2755-2756, l.2763; §12.1 l.2810-2816,
l.2819, l.2823, l.2826-2832, l.2838-2839, l.2854-2862, l.2875-2880, l.2888-2889, l.2940 (Df-2: K, 19), l.2949, the
floors of the Q3 annex l.2958-2962; §12.5 point 4 l.3012 (the hand-over is consistent for the parent; not for curling
products).

### 4.4 Table 4.4a at the approved CPU [9]

User decision of 2026-11-16: the pool keeps 457 (SM) + 208 (B1) CPU-h. Rule M_t ∝ √(N_t/c_t), G = 1. M is the
full-weight class. Costs [V] for Z(νν), W(τν), tt̄ 1ℓ; the eleven other processes by proxy [E].

| zero-count allowance at 68 % (events) | as timed | forced tt̄ (327 ms [V]) | preselection before the chain | both |
|---|---|---|---|---|
| Z(νν)+jets | 29.2 | 26.4 | 19.6 | 17.1 |
| W(τ_h) | 20.2 | 18.3 | 14.0 | 12.2 |
| W(eν) | 13.8 | 12.5 | 9.6 | 8.3 |
| tt̄ 1ℓ | 36.4 | 24.9 | 28.5 | 17.5 |
| **SM sum (14 processes), full-weight classes** | **169.4** | **138.3** | **122.5** | **93.4** |
| share of the tt̄-type rows | 40 % | 33 % | 43 % | 35 % |
| low-weight (0.05) class of each process, one zero each | + 8.6 | + 7.1 | + 6.3 | + 4.8 |
| B1, seven classes, one shared Geant4 pass | 23.0 (4.5 for each of DIF, DIF-C, NI-X, NI-C; 1.6 for each radius) | | | |
| B1, four terms (lenient) | 5.8 | | | |
| **all pool terms, seven classes** | **201** | 168 | 152 | **121** |
| all pool terms, four terms, low-weight classes not counted | 175 | 144 | 128 | 99 |

- Frozen: 12.6 (SM 8.6). Of the SM factor, ×4.5 comes from the unit costs and ×4.3 from the weights.
- **Not re-derived in version 4, said here:** the table uses the unit costs of version 3 (Z(νν) 127 ms; Geant4
  0.305 ms per firing; chain 3.7–5.9 ms). With the costs measured since (133.8 ms for the pilot's Z(νν) job with its
  summary; 0.338 ms; option (a) for two classes) the B1 row would be 24.9 and the "as timed" sum about 204 [E; 9,
  sensitivity line]. The table is re-derived at the day-12 re-allocation in any case (STR §11.7 point 6).
- The lower columns need (i) forced top decays, run through the chain for tt̄ 1ℓ only [V]; (ii) the frozen v2
  preselection applied before the chain in the 4a generation job. What (ii) gives up: an event failing the nominal
  preselection is not available under a varied MET model, and the pool cannot be re-used if the preselection changes
  after the freeze. The tables of the pre-registration carry the "as timed" column until each measure is
  demonstrated.
- CPU needed for an SM allowance of 39: 1,094 (both) to 1,984 (as timed) CPU-h; of 8.6: 4,960 to 8,996.
- Rule 3 (a) of §11.7 ("12.6 to 10.2") is recomputed at day 15 from these values.

### 4.5 Reach with every ceiling empty [10]

The strategy's own functions, v1 placeholder efficiencies; the frozen row reproduces as 790 [712]. Median [84 % edge]:
**514 [445] GeV as timed and 584 [514] with both measures** (predictive B₁₆ / B₅₀ / B₈₄ = 132 / 177 / 235 and
85 / 110 / 143 events); four-term variant 522 [451] and 597 [524]. At an R08-like selection with every ceiling empty
the result itself holds B₅₀ = 275 (as timed) or 208 (both) against the class limit of 300 (113 at Gate A): R08
candidates have little room in the result, not only in rule 1. The expected outcome of the strategy (STR l.66-74)
does not depend on these floors. None of these numbers contains an allowance for [L15].

### 4.6 The (α1), (γ) and Q2 (c) numbers on the new basis [12]

What the user reads at day 15 when choosing between Q2 (b) and (c) (STR l.2829-2832, l.2854-2862, l.2875-2880).
Computed like the strategy's v9 table (2×10⁴ draws, R09 pile-up estimate), on the draft reading. ESTIMATE, v1
placeholder inputs.

- Empty reading 161 instead of 76: the room below 300 falls from 224 to 139 events.
- (α1) decays in flight after CKF, 385–647 events from v1's 1–2 counts, become 481–810 with the first-arc Geant4
  yield inside v1's own definition (×1.25). The other classes have no v1 count.
- (γ) row: m_H = 10 / 30 / 60 / 100 pool-equivalent counts are 0.9 / 2.8 / 5.5 / 9.2 full-weight pilot counts and read
  197 / 272 / 386 / 538 (frozen: 117 / 195 / 309 / 462).
- (α1) with fit-probability credit on decays in flight and conversions (the (c) test only): 192 / 215 (frozen
  109 / 130): still below 300.

| decays-in-flight size, f_D × v1's central size | B₅₀ with the conversions removed (fall ×339 / ×201) | smallest conversion rejection with B₅₀ ≤ 300: photon rate 0.379 [0.255] {Z(νν) 0.231} | frozen |
|---|---|---|---|
| 0 (pilot count zero) | 161 / 161 | ×67 [×46] {×42} | 76; ×44 [×30] {×28} |
| 1/4 | 257 / 323 | ×222 [×150] {×135} / none suffices | 168 / 233; ×75 / ×150 |
| 1/4, with the Geant4 first-arc yield (×1.25) | 281 / 364 | ×494 [×333] {×303} / none suffices | — |
| e⁻¹ | 303 / 400 | none suffices | 213 / 309; ×114 / none |
| 1 | 547 / 808 | none suffices | 458 / 718; none |
| no S_CKF estimate, f_D = 0 (ε_pair 0.8 / 0.98) | | ×335 / ×3,350 | ×219 / ×2,186 |

So option (c) is harder than Gate A showed: it needs a conversion rejection of ×67 even with no decay in flight in
the pilot, and at a quarter of v1's decays-in-flight size it works only for the faster pile-up fall.

## 5. Budget, calendar, storage [E from V unit costs; 8, 11]

- **Pilot: 142.3 CPU-h against 54.5 budgeted** (overrun 88, reported under brief D6; 134.5 in version 3).
  *Part 1, launched:* minimum bias 9.8 (880–889 CPU-s per 2.5×10⁵ interactions [V]) + Z(νν) 85.5 (133.8 ms per event
  on the first three jobs [V]; 81.1 in version 3 at 127 ms without the summary) = **95.3 CPU-h**; the orchestrator's
  estimate at launch was 95. *B1 part, not launched:* Geant4 18.4 (1.23×10⁸ firings of all species at the
  production code's 0.338 ms, 4.6×10⁸ of the r < 70 mm pass at 0.054 ms [V: p2-c-px-g4]; 16.4 in version 3 at the
  partition job's costs); chain 23.8 (DIF-C and NI-C at the option-(a) stage sums 4.8 and 6.2 ms [V: p2-c-px-hy];
  22.4 before); hard-scatter sample 4.2; low-p_T check 0.5: **47.0 CPU-h** (43.4 in version 3).
- **Storage: 167 GB against 52 budgeted** (156 in version 3): Z(νν) 77.8 (33.84 kB per event [V]) + minimum bias 2.2
  = **80 GB for part 1**; B1 events 71.3 (1.92×10⁷ events at the measured slice sizes per stream, 2.6–5.4 kB [V:
  p2-c-px-tr, -hy]; version 3 used 4.3 kB for all); **Geant4 vertex files 16.0 (62 × 0.226 GB measured per 'all' job
  + 2 for the 'ni' pass [E]), which version 3 did not count.** cajuela had 3.9 TB free at 15:28 (`LOG.md`).
- **Order and dates** [E: wall time = CPU time, lanes never idle; 8]. Part 1 runs on 2 lanes of schrodinger since
  16 Nov 16:39: `pilot.mb` complete about 17 Nov 02:30 (first campaign of lane 0), **Z(νν) complete about 18 Nov
  16:15** (the orchestrator's 16:30). The Geant4 passes need `pilot.mb` only; **`pilot.c0.hs` needs the finished
  Z(νν) files as its parent pool and cannot start before 18 Nov 16:15.** The B1 streams then take the two lanes:
  complete about **19 Nov 15:45**, 32 h before day 5 (2026-11-21); on one lane 20 Nov 15:15 (9 h); on three 19 Nov
  08:00. If the Geant4 passes run on a third slot before Z(νν) ends, about 19 Nov 06:30. Before any of it: the
  third review, the user's approval (D3, D5, D9), the campaign files, the class-aware validator and one validated
  job per stream. With every B1 sample doubled (D3) the two lanes end about 20 Nov 15:00.
- **Families.** With seven B1 terms the eligibility family of STR l.407-408 has **K = 13** (B1-a for seven terms;
  B4-c for four; B2-a; B2-b): the INVESTIGATE and re-test level 0.05/K is 0.0038 instead of 0.0050. The ceiling
  family has **T_c = 22**, α_c = 0.05/22 = 0.00227. For an analysis that performs as declared, at least one closure
  FAIL has probability 5.1–12.0 % (5.1–10.2 % frozen), a false FAIL of either family removes a selection with
  **7.0–9.9 %** (6.9–8.9 % frozen) [5]. These replace the numbers of STR l.407-411, l.421-424, l.472, l.811-813,
  l.1813, l.2345-2348 and Df-2 (l.2940), and COM l.23-25, B1-f, T2-a, PR-1, VC-3.
- **Closure designs for DIF-C, NI-X, NI-C** (B1-a): 1,000 unbiased test overlays each (3 × 7 CPU-h), their paired
  pile-up-only pass (≈ 10), derivation overlays (≈ 10): **≈ + 41 CPU-h in 4a**. Named here, written in the
  pre-registration. No v1 count exists for these classes; NOT TESTED is covered by Q3 with a new annex row each.
- **Other lines on the 45 ms guess:** multijet loose population 12.5 → ≈ 28 CPU-h; B6-c 25 → ≈ 71 CPU-h.
- **Toys** [V per unit: `outputs/TOY_COST_viktor_2026-11-16_16-33.md`, campaigns p2-c-toy-{jax,base,ref,tune,fix},
  2.58 CPU-h on schrodinger; synthetic workspace]. Configuration: pyhf 0.7.6 on the jax backend, scipy SLSQP with
  automatic-differentiation gradients, merged auxiliary channels, the POI removed from the fit instead of
  constrained, fits started from the previous toy. Per unit of 1000 + 1000 toys: 30.5 / 168 / 385 / 817 s at
  31 / 60 / 80 / 100 parameters, against 487 / 8,814 / — / 67,780 s for numpy + scipy on the same node. Same CLs at
  the test point (0.1372 ± 0.0165 at μ = 5, 31 parameters, once tied values of the statistic are compared within
  10⁻⁵), 0 failed fits in 25,180 toys. The toy programme (1,006 units, STR §4.11 point 5 and T1-c (iii)):
  **47 / 108 / 228 CPU-h at 60 / 80 / 100 parameters against 183**; break-even ≈ 93 parameters. **Not shown:** the
  cost on a real v2 workspace (the executor's judgement: a factor ≈ 1.6 either way, i.e. 29–75 / 67–172 / 143–365);
  the jax path for the v1-mode workspace (T1-b); the environment exists on one node only. To be re-measured on the
  first real workspace before Phase 4b (one 100 + 100 job). At 100 parameters the central value is above the 183 of
  the toy line by 45 CPU-h, and the conditional all-exact draw (296) above the strategy's 236.
- **Projection** (approved 4,609; threshold 5,992; both unchanged as approved figures) [11]. Extras + 190 CPU-h
  (pilot + 88, multijet + 15, B6-c + 46, new closure designs + 41).
  **Planning case (jax configuration): 4,663 / 4,723 / 4,844 CPU-h at 60 / 80 / 100 parameters; 4,645–4,981 over the
  factor 1.6: below 5,992 in every case**, and 54–235 above the approved figure (reported overrun, not a stop).
  With the robustness test of §1.5: + 22–28.
  **Old backend, kept on record:** 7,705 / 9,591 / 18,199 on version 3's timings (7,710 / 9,604 / 18,246 as version 3
  printed them with its smaller pilot), 7,080 at 60 and 23,564 at 100 parameters on the second node's: above 5,992.
  By ST-1 (COM l.257) the study would stop and ask in that case; it applies only if the jax configuration fails on
  the real workspace.

## 6. What does not change, and what does

Unchanged: the 16 T2 candidates and the selection rule; Q1–Q5; Df-1, Df-3 to Df-10; the definition of rule 1 (Df-11; its pile-up term only as chosen with D2)
and its limit of 300; the stop rules; the approved CPU and calendar; the pool allocation rule; brief D7; the
blinding (no signal quantity is used or shown here); the detector chain (v1's, with its half-turn limit); T1-i.
Changed if this addendum is approved: the B1 term list (4 → 7); K (10 → 13), T_c (19 → 22) and α_c in Df-2, the
header of COM, B1-f, T2-a, PR-1, VC-3; the closure tests of B1-a; the Q3 annex; inventory rows 11, 17 and 19; the
number of T1 auxiliary channels; N_t of every B1 term; **the parent hand-over (radius cut for first-arc classes,
option (a) for the two classes after a turn; criterion with multiplicity)**; M of the pilot and of the pool
(effective events); Table 4.4a and every number derived from it (list in §4.3); the Q2 (c) numbers (§4.6); **a new
limitation [L15] in STR §7**; **the looper statements of STR §2 and §4.4**; and, only if the user accepts D2, an
eighth row of the B6 table (COM B6-a, B6-c, B6-d) and, if the user so chooses with D2, its correction of the pile-up term in the binding day-15 reading (§1.5).

## 7. Open points and limitations

### 7.1 Open points, with the resolving power of each test named

1. **[L15]** (§1): chain-wide, weakly bounded; a looper with pile-up untested unless D2 is accepted. With the complete Geant4 reference (p2-c-pa-htg, LOG.md 18:15) the fractions are 25.2 % and 37.5 %; they remain lower bounds because detector secondaries are not compared.
2. **Not read by rule 1:** parents of 0.3–0.5 GeV (N_t 2.6–5.2×10⁸ [E]; alarm sample at 1,300–2,600 events per
   count); parents at 1 < |η| < 1.5 (N_t ≈ 1.9×10⁸ [E]; no sample); hard-scatter hadrons outside the road (1.8×10⁸
   vertices [E]; alarm through the minimum-bias orientations). If any of them makes candidates at a rate per vertex
   comparable to the pool's, the B1 terms are under-read by a factor up to 2.4 for one of them and 2.7–3.4 for the three together (D6).
3. Whether vertices outside the three radii, or after a turn, can make candidates needs the finder's frozen cuts.
   Until then every class is a term.
4. Tests named as safety nets: B1-g (Phase 3, 1,000 pile-up events with all secondaries) reads one count as
   N_trig/1,000 = 4.1×10⁴ events at R04–R07: an alarm at loose rungs, no bound at the scale of 300. Its Geant4
   secondaries are handed to Fatras and stop at half a turn like every product. Tabulating H against parent p_T, η
   and road offset: an edge bin holding a fraction f of a sample reads (events per count)/f: an alarm, not a bound.
5. Products with β < 0.1 at the slab exit (0.07–0.12 per NI event) are not handed over. Fatras drops particles that
   reach its step limit (0.03–0.07 per hard-scatter event); the loss of conversion legs is not quantified, and whether v1
   had it is unverified.
6. Preselection weights under the v2 MET model (day 12); costs and weights of the eleven untimed SM processes.
7. The hard-scatter share of N_t (1.022) and the vertex yield of hard-scatter parents are planning values until
   `pilot.c0.hs` exists; the first direct parent count gives 1.3 %.
8. v1's generator cut p̂_T > 150 GeV is not fully efficient for MET > 200 GeV (1.7 % of kept Z(νν) events within
   10 GeV of the cut [V: p2-c-prof]).
9. The B1 production code: campaign files, class-aware validator, one validated job per stream (P7).
10. The toy cost on a real workspace (§5).

### 7.2 Version 3's open points and decisions, one by one

| version 3 | state in version 4 |
|---|---|
| open point 1 (three unread populations) | still for the user (D6); unchanged numbers |
| open point 2 (classes need the frozen finder cuts) | unchanged |
| open point 3 (safety nets are alarms) | unchanged; B1-g note on [L15] added |
| open point 4 (weights at day 12; untimed processes) | unchanged |
| open point 5 (slow products; step limit) | unchanged |
| open point 6 (hard-scatter share) | unchanged |
| open point 7 (p̂_T cut; dump stage split) | first part unchanged; the dump stage is 17.3 ms of 130.7 in the pilot's Z(νν) job [V: p2-c-px-znnb], not pursued |
| open point 8 (A-1 re-validation; B1 code) | **A-1 resolved** (P6); B1 code: slice-run, not production-ready (P7, 7.1 point 9) |
| D1 number of terms | still for the user (now D4); unchanged |
| D2 hard-scatter parents | still for the user (now D5); order fixed by the Z(νν) end date |
| D3 pilot size | Z(νν) at 2.3×10⁶ **launched on the user's approval**; B1 sizes still for the user (D3); Z(νν) top-up at day 7 (D8), costs now + 45 / + 109 CPU-h |
| D4 low p_T and \|η\| | still for the user (D6) |
| D5 R08 | still for the user (D8); one more way to pause when empty (pile-up shift) shown |
| D6 pool | still for the user (D7); unchanged numbers, sensitivity 204 stated |
| D7 toys | **changed**: the stop rule is not triggered on the planning case; for information (D10) |
| D8 hand-over (time cut) | **changed**: the time cut is withdrawn; radius cut and option (a) per stream (D9) |
| new | D1 ([L15], chain kept), D2 (robustness test) |

## Changes since version 4

Line numbers are those of this file. Items marked COMMITMENTS.md change that file only.

| review item | section / line | status |
|---|---|---|
| B-1 | §3 P6, paragraph after the option-(a) table, l.481 | applied |
| B-1 | §3 P6 (v), l.494 | applied |
| B-1 | §0.3 D9, l.109 | applied |
| B-2 | §1.5 What, l.281 | applied |
| B-2 | §1.5 Pre-declared reading, l.308 | applied |
| B-2 | §1.5 Effect robust, l.315 | applied |
| B-2 | §1.5 Effect robust (deletion), l.317 | applied (sentence deleted) |
| B-2 | §1.5 Effect not robust, l.318 | applied |
| B-2 | §1.5 When, l.304 | applied |
| B-2 | §1.5 When, l.305 | applied |
| B-2 | §0.3 D2, l.102 | applied |
| B-3 | §0.1 item 1, l.33 | applied |
| B-3 | §0.1 item 2, l.36 | applied |
| B-3 | §0.1 item 3, l.41 | applied |
| B-3 | §0.1 item 3, l.40 | applied |
| B-4 | §0.3 D6, l.106 | applied |
| B-4 | §7.1 point 2, l.763 | applied |
| C-1 | §0.1 item 6, l.56 | applied |
| C-2 | §0.1 item 7, l.58 | applied |
| C-3 | §0.2 row R08, l.77 | applied |
| C-3 | §0.1 item 5, l.52 | applied |
| C-4 | §4.3 superseded list, l.613 | applied |
| C-4 | §4.3 superseded list, l.615 | applied |
| C-5 | §1.1 point 5, l.190 | applied |
| C-6 | §7.1 point 1, l.759 | applied |
| C-7 | §3 P6 (ii), l.488 | applied |
| C-8 | §3 P7, l.510 | applied |
| C-9 | §0.3 D1, l.101 | applied |
| C-10 | §0.3 D6, l.106 | applied |
| C-11 | §0.2 expected-outcome row, l.92 | applied |
| C-1 (COM) | COMMITMENTS.md, section "Changes of rows by addendum 1", COM B1-a | applied |
| C-12 | COMMITMENTS.md, section "Changes of rows by addendum 1", row C3 (l.176) inserted after row C1-a (l.168) | applied |
| C-12 | COMMITMENTS.md, section "Changes of rows by addendum 1", row B2-a, B2-b, B2-c (l.184-186) inserted after row B1-g (l.183) | applied |
| C-12 | COMMITMENTS.md, section "Changes of rows by addendum 1", row B6-d (l.206) inserted after row B6-a, B6-c (l.203, l.205) | applied |
