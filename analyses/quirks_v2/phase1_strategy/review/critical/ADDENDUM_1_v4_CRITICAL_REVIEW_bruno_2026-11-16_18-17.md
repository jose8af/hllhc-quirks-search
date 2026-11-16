# Critical review (third and last round) of strategy addendum 1, version 4 — Bruno, 2026-11-16 18:17 (`date`)

Artifact: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_v4_zoe_2026-11-16_17-26.md` ("v4", as edited at 18:02), with
`FIX_REPORT_addendum1_v4_zoe.md`, `phase2_exploration/src/p2z_addendum1.py`, `addendum1_v4_stdout.txt` and the section
"Changes of rows by addendum 1" of `COMMITMENTS.md` (COM). `STR` = `STRATEGY_oscar_2026-11-16_10-41.md`.
Tags: **[V]** re-derived or read by me in this session (file, field or my script); **[E]** my estimate; **[U]** not
checked by me. My scripts (pure Python, `nice -n 19`, one at a time, einstein): `/var/tmp/jdochoa/bruno/chk.py`
(own sampler for rule 1, pilot cost, storage, calendar, toys, robustness test, pool floor; no author code imported),
`chk2.py`, `reach.py` (the strategy's own functions on a scratch copy of `strategy_budget.py`, sha256 548b5ba8…),
`keys.py`; output `chk.out`. No git command, no job on a worker, no subagent, nothing written outside this file and
my scratch directory.

## Summary

Version 4 is an honest and careful document and its arithmetic is right: every number I recomputed reproduces
(42 listed in section d), the script's overrides are what the text says, the stdout is what the text quotes, the
hand-over rule per stream is supported by the validation counted with multiplicity, and the half-turn limit is
stated with its measurements, with the mechanism tagged as inference and the fractions as lower bounds. I found **no
Category A**: nothing would make the user decide on a wrong rule-1, cost, pool or reach number, and the pilot
definition is the one the measurements support.

**Verdict: ITERATE, with four B items that are all text (exact replacements given); no number of §4 changes.**
Per the three-round limit this goes to the user with the list below. The four:

- **B-1 (new fact, measured after v4 was closed).** At 25,000 events per file the hard check "no product hit
  before the vertex time" fails for NI-X: one event in 25,000 has a fragment of β = 0.134 (above the β cut of 0.1)
  with Fatras hits at t = −32 ns (`LOG.md` 18:15; executor log Albert 18:13). v4 P6 says "no product hit before its
  production time", which is true of the 2,000-event files only. The hand-over the user is asked to approve (D9) has
  an open parameter; the NI streams must not be released before it is settled.
- **B-2 (the robustness test, D2).** The pre-declared reading is not single-valued: "the day-15 reading is quoted
  with it" does not say whether a measured increase enters the binding reading; the trend threshold is "2σ" in one
  bullet and "its error" in the next. My rulings on the two flagged design points are in section c, with the text.
- **B-3 (§0, what the user reads).** §0.1 item 3 says the pile-up estimate is "the one term the day-15 rule takes
  from the present simulation without any allowance". Every term is. And §0 does not say that the looper zero is in
  finder candidates, not in the quantity the day-15 rule counts, nor that the same zero read for the hard-scatter
  event's own loopers (286 events at 68 %) would, as a term, put an empty pilot at about 350 [V: `chk2.py`].
- **B-4 (D6).** "Under-read by up to a factor 2" is 2.4 for one population and 2.7–3.4 for the three together, from
  v4's own numbers.

If B-1 to B-4 and the C items are applied as written, **I see no need for a further review of the text**; B-1 is
then closed by the measurement in progress and by the release condition, not by a reviewer.

MUST items within 4,609 / 5,992 CPU-h: none looks infeasible on the planning case (projection 4,663 / 4,723 / 4,844,
+ 22–28 with D2 [V]). T1-i depends on the jax configuration holding on a real workspace (not shown; old backend
7,080–23,564, above the threshold). The expected outcome of Gate A (pause at day 15) still holds: about 717 Z(νν)
pilot counts expected against a pause at 4.

## Item g: what the user must know and decide (12 lines)

1. The fast simulation records no hit beyond half a turn of any particle; v1 had this and did not know. Missing
   against Geant4: at least 25 % (Z(νν)) and 37 % (pile-up interaction) of the written hits, 34–58 % in the PS layers.
2. Your option B was applied as you stated it: 0 finder candidates in 2×10⁵ single loopers, so the chain is kept.
   The zero is weak: it allows 2.2×10⁴ events (pile-up loopers) and 286 (hard-scatter loopers); as a term of the
   day-15 rule the latter alone would read about 350 on an empty pilot. It is carried as limitation [L15], not a term.
3. Not tested at all: a looper together with pile-up. **D2**: accept a 600-event test (22–28 CPU-h, by day 15)?
   Recommended. With it, decide whether a measured increase enters the binding day-15 reading (recommended: yes).
4. **D1**: confirm the chain is kept. This also adds one item to the frozen paper-correction list (v1's looper
   bound measured nothing) and changes how the 1,000 looper overlays are made.
5. Day-15 rule, unchanged since version 3: an empty pilot reads 161 at R09 (76 at Gate A) and 238 / 262 / 284 at
   R08 (limit 300); pause at 4 Z(νν) counts or 6 counts in a large B1 sample (R09), at 1–3 counts (R08). The pause
   remains the expected outcome (about 700 Z(νν) counts expected).
6. **D4, D5**: seven B1 terms and the hard-scatter parents as one term (24 events more lenient than the literal
   reading; with the literal reading an empty pilot pauses at the upper R08 estimate).
7. **D6**: three populations are read by nothing (parents of 0.3–0.5 GeV, 1 < |η| < 1.5, off-road hard-scatter
   hadrons); together they could under-read the B1 terms by a factor up to about 3. The analytic bound of B1-e is
   no longer claimed.
8. **D3, D9**: B1 pilot sizes (47 CPU-h, to start about 18 Nov 16:15, end 19 Nov 15:45 on two lanes) and the
   hand-over per stream. The production code is not finished, and a slow-fragment artefact (1 NI-X event in 25,000)
   was found at 18:15: the NI streams wait for it, and a change of the β cut comes back to you.
9. **D7**: the pool at the approved CPU has a zero-count allowance of 201 events (121 with two measures of which one
   is not demonstrated), not the 36–42 your earlier decision was taken on; reach if all is empty 514–584 GeV (790).
10. **D8**: an R08 candidate pauses on 1–3 counts; a pile-up estimate 25 % higher makes an empty pilot pause at the
    upper R08 estimate.
11. Costs: pilot 142 CPU-h and 167 GB (54.5 and 52 budgeted); projected total 4,663–4,844 CPU-h, below 5,992,
    provided the faster toy configuration holds on a real workspace (**D10**, for information).
12. Quirk hits do not pass through the fast simulation and are not truncated (checked in the code); the effect of
    the missing arcs on the signal through the other hits of the event is not measured before the verdicts.

---

## a. Regression (second review, and the items the first review left partial)

| finding | status | evidence checked by me |
|---|---|---|
| **A-1** parent truncation, DIF-C and NI-C | **RESOLVED for the parent.** Residuals stated in v4: products and all other particles stop at half a turn ([L15]); new residual B-1 | `p2-c-px-val2-0.json`, `-val3-0.json` re-read with my own loop [V]: with multiplicity, radius cut DIF 20 / 18,735, NI 30 mm 0 / 893, NI 61.5 mm 0 / 2,627, NI-X 15 / 15,368; DIF-C 28,692 / 49,048 (58.5 %), NI-C 35,335 / 53,131 (66.5 %); time cut 19,802 and 24,021 (40.4 %, 45.2 %), NI-X 506 (3.29 %, fails); hybrid 18 (0.04 %) and 25 (0.05 %), extra 785 (1.58 %) and 828 (1.54 %); `autoh` mixed 30 / 27,044 and 41 / 34,546; r0 = r1; V4-1 true in all 35 files. Once per surface: 435 / 1,470 and 498 / 1,475 (radius), 20 and 16 (time) [V] |
| A-1, validator flag | **Handled as a release condition** | `all_hard_checks_pass` false in val3 with `hard_without_a1` false for the six turned-parent files, through `parent_hits_beyond_vertex_radius` 19,643 / 25,945 / 7,340 / 12,551 [V]. Stated in v4 P6 (iv), P7, §5, §7.1 point 9, D9 and COM B1-a. A per-mode check now exists in `p2x_validate.py` (l.183-207, l.246-252, file of 17:25 [V]); it has not been run on an option-(a) file (C-8) |
| **A-2** `pilot.c0.hs` in rule 1 | **RESOLVED** | own sampler [V]: H1 one term 160.3; 238.0 / 261.8 / 283.7 (v4 161; 238 / 262 / 284); seven weight classes 184.4; 262.0 / 285.8 / 307.8; H2 195.2; 272.4 / 296.6 / 318.5; H2 as classes 430.9; H3 158.9; 236.4 / 260.2 / 282.1. One count 3.96; 8.3×10⁵ distinct parents is [U] |
| **B-1** road | **RESOLVED** | 21 × 0.30 / 2π = 1.0027 [V]; N_t × m / M summed over orientations is the rate in one road by rotation symmetry |
| **B-2** low p_T, \|η\| > 1 | **RESOLVED as a statement**; quantification of the sum understated (B-4) | N_t 2.61 / 5.23×10⁸, 1,307 / 2,615 per count, zero allows 1,489 / 2,978; forward 1.83×10⁸ (v4 1.9×10⁸: its script multiplies by F_HS and uses the slice's pool) [V] |
| **B-3** consequences, bookkeeping | **RESOLVED**, three lines missing from the superseded list (C-4) | K = 13, T_c = 22; "at least one FAIL" 1 − (1 − 0.0040)¹³ = 0.051 and 1 − (1 − 0.0098)¹³ = 0.120; either family 0.070 / 0.100 [V arithmetic from the per-test values of stdout [5]; the per-test values themselves are [U]] |
| **B-4** state of the pilot code | **RESOLVED as a statement** ("nothing here says the B1 production is ready"); §0 does not carry it (C-2) | v4 P7; executor log Albert: campaign files are still to be written |
| **B-5** B1 pool floor | **RESOLVED** | my own optimisation [V]: 'all' pass 0.904 ms per firing, 'ni' 0.0810; best split 86 %; 4.52 for each large class, 1.64 per radius; sum 23.0; pool sums 201.0 and 121.2 |
| C-1 … C-12 | applied, or superseded as the fix report says | C-2: 193,313 and 61 % [V: stdout [1], partition JSON]; C-3: frozen row 12 (299.6–300.2; mine 300) [V]; C-7: 1.234×10⁸ = 1.03 × 1.198×10⁸ [V]; C-8: `jets10` p_T > 10 GeV (`PILOT_READY…` l.55 [V]); C-9: 62 jobs [V]; C-4 not applied as code, provenance stated |
| first review A3 | follows A-1 | as above |
| first review B3, B7, B10 | resolved through B-3, A-2, B-1 / B-2 above | — |

What remains wrong on the present chain, all stated by v4: the products of every vertex and every other particle
stop at half a turn; H of every class and of every SM term is counted without those arcs. Not stated: the validation
of option (a) is a count per surface. The injected hits are the Geant4 crossings themselves, so the 0.04–0.05 % is a
closure of the injection and of the seam, not an independent test; and it does not see positions (C-7).

## b. The half-turn limitation [L15]

**Supported by the measurement files** [V]: `p2-c-px-htg-mb.json`: 243.86 written hits, 311.60 Geant4 crossings,
88.84 after half a turn (28.5 %), 91.01 without a hit (37.3 %); by layer 8.3 / 14.4 / 20.9 / 25.9 % (TBPX), 57.8 /
56.7 / 53.0 % (TBPS), 45.9 / 37.5 / 24.2 % (TB2S); 1,676 of 174,722 without a record (0.96 %); 133,891 alive after
one turn (76.6 %). Z(νν) values as in stdout [15]. The mechanism is tagged as inference, "no v1 file mentions it" as
[U], the fractions as lower bounds. Since 18:15 the full reference gives 25.2 % and 37.5 % (`LOG.md`): the "1 %
without a record" caveat is closed, the "secondaries" one stays (C-6).

**The looper gun** [V: `p2-c-px-lpds-0.json`]: 100,000 + 100,000 events; finder run 97,137 / 97,149; seed triple
72,773 / 74,446; seeds above threshold 33 / 34; candidates 0 / 0; every rung 0; 18.20 crossings per event, 9.19 after
half a turn. The funnel labels are right: in `finder.py` l.206-250 `n_trip` counts triples, `n_refit` is the number
of seeds that passed T_seed and were refitted, `n_kept_all` the candidates with N_L2 ≥ 4 after the refit (the JSON
key `with_seed_Tseed` for the 72,773 is a misnomer, not an error of v4). Bound: N_t 1.898×10⁹, 1.898×10⁴ per count,
2.16×10⁴ at 68 %; hard-scatter reading 2.51×10⁷, 251, 286 [V]. §1.3 gives the limits of the zero the same weight as
the result. Two things are missing, and both belong in §0 (B-3):

1. *The currency.* The zero is in candidates of the frozen finder, seed threshold included. The day-15 rule does
   not count finder candidates: it counts own-hit classes k ≤ k_max by a width-only subset search, and "finder
   seeding and grouping" are "not used" there (STR l.755-762, l.778). That code does not exist (the looper report
   says so; v4 dropped the sentence). What the gun gives in that currency is an upper bound by multiplicity: 3.5 %
   of the loopers could reach R04 and 10.5 % its near-pass classes (3,453 + 2,346 + 2,405 + 2,312 of 10⁵ [V]). The
   27 % of events without a seed triple carry no statement at all. The stored gun events can be classified when
   the Phase-3 code exists, at no simulation cost.
2. *What the zero would read as a term.* With the hard-scatter looper zero as one more zero-count term (251 per
   count) an empty pilot reads **351 at R09** and 430 / 457 / 481 at R08; with both gun sets as one sample (126 per
   count) 265 and 345 / 370 / 393; with the pile-up looper zero (1.9×10⁴) 1.3×10⁴ [V: `chk2.py`]. v4 treats the
   topology as a limitation and not as a term. That is what the user's option B gives ("if not, the chain is kept
   and the limitation stated with the measurement behind it"), so it is **not more lenient than the user's rule**;
   but it is the most lenient point of the draft against the strategy's own convention, and the user should see
   the number when confirming D1.

**Consequences per term.**
- *Pile-up.* I read `TT/acts/stage4/plan.md` l.296-311 and `finder/pu_inputs.py` l.5-17, l.34, l.66-74 [V]: the
  top-up adds (ratio − 1) × the event's own crossings per layer (ratios 2.26–7.27), z resampled, φ uniform, in/out
  pairs in the stacked layers, at the level of the finder input (after the chain); the looper-pair top-up is a
  variation only. STR §4.5 (l.1119-1227) says nothing about loopers or the top-up; l.264 and l.275-277 do, and are
  not contradicted. v4's sentences ("number per layer normalised, arrangement not restored"; "the closure of the two
  estimators against direct counts cannot see it") are supported. One addition: the occupancy model, which alone
  carries the pile-up term beyond R07 (STR l.1192-1195), takes its layer-to-layer correlation factors from the same
  events (l.1140-1146).
- *B1 classes, SM hard scatter.* Stated correctly. STR l.788 ("H … is then a true ceiling") holds inside the chain
  only; it is not in the superseded list (C-4).
- *Signal.* v4 says it is not known whether Stage 3 has a path or time cut. I read the code (no signal quantity):
  `TT/sim/stage3/code/T3_causal_s3.py` has no turn or path limit; it records every root of every chord (l.262) and
  ends a pair at t_end (l.303; default 1.3 r_exit/β_T + 50 cm/c, l.579-582), at the step cap (status 3, l.300; 2×10¹⁰),
  at the hit cap (status 5, l.489; 4×10⁵), at β_stop (status 2, l.505-513) or at the exit (r_exit 118 cm, z_exit
  293 cm; `run_stage3.py` l.233); `run_chain.Inject` (l.232-262) adds the stored hits without Fatras [V]. So the pair's
  own hits are not truncated by [L15]: **this gap is closed by reading, and it does not hold the freeze.** What
  stays open: how many pairs end at a cap (a truth-level census, to be read from v1's tracked record or added to
  BL-1 with the user's agreement), and the effect through the other hits of a signal event (f_CKF, shapes, hits
  around the ribbon), which only the optional signal arm of D2 measures, after the verdicts (C-5).
- *C1.* Correct.

**Label and placement.** [L15] is the next free label (STR §7 ends at [L14], l.2285-2299 [V]); the four places
named are right. **Silently invalidated and not listed as superseded:** STR l.728-730 (the looper gun topology kept
as 1,000 full-pile-up events), l.1306 (loopers inside the B4 terms), l.788; the frozen list C3 (COM l.176, "all 24
items") gets a 25th item, and inventory row 19 changes, on a proposal "to the orchestrator" only: both are changes
of frozen items and belong in D1 (C-9). COM B1-e's bound is withdrawn in the COM table but in no decision row (C-10).

## c. The robustness test (D2)

Sound in outline: the same events and seeds, pile-up only, development role, read where direct counts exist, sized
like every other reduced B6 background row. Recomputed [V]: Geant4 200 × 52.6 × 0.41 ms = 4.3 s (3.7 s at the 0.354 ms
per particle measured on exactly this population, `p2-c-px-htg-mb.json` → `g4_ms_per_particle`); nominal 12.3 + 4 ×
11.3 = 57.5 s; 600 events: varied 10.3 / 13.2 / 16.1, partner 9.6, + 2: **21.9–27.7 CPU-h**; 1,000 events 35.1–44.8;
R06 593 counts, unpaired error 0.058; 202 events for 200 counts. The R04, R05 rates are at STR l.249, l.747; R06
0.247 = 1,482 / 6,000 (l.1185).

**Ruling on design point 1 (top-up): the fixed-density design is right, with three additions.** The top-up ratios
normalise to a full-simulation occupancy that already contains the in-time loopers, so arcs on top of an unchanged
top-up would count them twice. Fixed density does not hide the effect, but r alone can: exchanging random crossings
for arcs lowers the random part and raises the correlated part, and the two can cancel in r. So (i) the candidates
that contain a layer made by one particle's later arc are also counted by truth, which is the direct measurement of
"a looper together with pile-up" on about 10⁶ loopers; (ii) the varied sample's top-up is a subset of the nominal
draws, otherwise the pair is not paired in its largest hit population; (iii) the density is fixed at the raw level
at which the ratios were derived. Also read the 2S crossing rungs: 19.7 % of single loopers cross a 2S layer twice
in both sensors [V: `N_2S2_max_hist`], and the missing crossings are largest in the outer layers. Cost: the injected
crossings pass the chain while the top-up does not, so the chain stage holds about 37 % more hits even at fixed
density: + 0.5–1 CPU-h [E], inside the range.

**Ruling on design point 2 (nuisance under [SD17]): allowed, but as a correction, not a symmetric nuisance.**
[SD17] forbids round-number variations at their measured size; variations "already defined by sources" enter at
their measured size (STR l.1477-1478), and the strategy carries generator and physics-list differences that way
(COM SY-4, SY-5). Geant4 transport of the same particles is such a source. But the shift has a known sign of
origin (hits that exist and are not simulated): a measured increase is applied to the central value, with its error
and the extrapolation width; no credit for a decrease. Whether the corrected term enters the **binding** day-15
reading changes the pinned Df-11 and is the user's choice; it must be asked with D2.

Timing: the freeze is at day 17 (STR l.2267), the decision point at day 15; "by day 15" is right, "the freeze … by
day 15" is not. A chain fix after the pilot regenerates it (142 CPU-h, about three days on two lanes): not said.

## d. Numbers recomputed [V: `chk.py`, `chk2.py`, `reach.py`]

| quantity (v4) | v4 | mine |
|---|---|---|
| N_t DIF, DIF-C, NI 22 / 30 / 61.5, NI-X, NI-C; sum; ratio to frozen | 1.061×10⁸, 9.75×10⁷, 4.90 / 6.64 / 6.63×10⁶, 9.49×10⁷, 4.97×10⁷; 3.66×10⁸; 5.37 | 1.061, 0.9751, 0.04896, 0.06638, 0.06627, 0.9494, 0.4974 ×10⁸; 3.664×10⁸; 5.369 |
| per count, draft: DIF, DIF-C, radii, NI-X, NI-C, HS, Z, Z low | 25.9; 23.9; 4.8 / 6.5 / 6.5; 23.2; 24.3; 4.0; 41.2; 2.1 | 25.95; 23.85; 4.79 / 6.49 / 6.48; 23.22; 24.33; 3.96; 41.25; 2.10 |
| frozen per count DIF, NI, Z | 65; 0.88 / 1.12 / 1.12; 18 | 65.13; 0.88 / 1.12 / 1.12; 18.13 |
| frozen empty pilot R09 [16–84 %]; R08 | 76 [36–152]; 156 / 181 / 204 | 76.0 [36–152]; 156.5 / 181.4 / 203.9 |
| frozen crossings: Z R09; R08; DIF R09; R08 | 12; 8 / 7 / 6; 4; 3 / 2 / 2 | 12 (300); 8 / 7 / 6; 4; 3 / 2 / 2 |
| draft empty pilot R09 [16–84 %]; R08 | 161 [109–232]; 238 / 262 / 284 | 160.3 [108–232]; 238.0 / 261.8 / 283.7 |
| draft crossings: Z; large B1 sample; HS sample | 4; 2 / 1 / 1 — 6; 3 / 2 / 1 — 35; 16 / 10 / 4 | 4; 2 / 1 / 1 — 6; 3 / 2 / 1 (DIF and NI-X) — 35; 16 / 10 / 4 |
| seven terms at 10⁶ | 389; 467 / 491 / 515 | 388.0; 466.1 / 491.1 / 513.8 |
| off-road stratum; low-p_T term | 186; 263 / 287 / 309 (both) | 185.3; 262.9 / 287.0 / 308.8 (both) |
| Z(νν) 3.5×10⁶; 5.23×10⁶ | 148; 225 / 249 / 270 — 139; 216 / 239 / 261 | 147.4; 224.5 / 248.1 / 269.8 — 138.5; 215.5 / 239.2 / 260.8 |
| B1 doubled; crossings | 102; 179 / 203 / 225; 16–17, 10–11, 8–9, 6–7 | 101.3; 178.8 / 202.7 / 224.6; 16–17, 10–11, 8–9, 6–7 |
| four / three / one term with H1 | 89; 99; 65 | 88.4; 99.0; 65.2 |
| pile-up × 1.10 / 1.25 / 1.5 / 2 at R08 | 246 / 271 / 294; 256 / 283 / 308; 273 / 303 / 329; 302 / 336 / 365 | 245.3 / 270.6 / 293.7; 255.7 / 283.3 / 307.9; 272.1 / 302.8 / 329.6; 302.1 / 337.2 / 366.3 |
| Z(νν) job; mb | 133.8 ms, 33.84 kB (three jobs); 9.83 CPU-h | 133.4 ms, 33.74 kB on the seven jobs done at 18:15, wall / CPU 1.006; 9.83 (five jobs) [V: markers] |
| pilot: part 1; Geant4; chain; hs; B1 part; total; overrun | 95.3; 18.4; 23.8; 4.2; 47.0; 142.3; 88 | 95.3; 18.4; 23.8; 4.23; 47.0; 142.3; 87.8 |
| storage: B1; Z(νν); vertex files; total | 71.3; 77.8; 16.0; 167 GB | 71.3; 77.8; 16.0; 167 |
| calendar: mb; Z(νν); B1 on 2 / 1 / 3 lanes; margin | 17 Nov 02:30; 18 Nov 16:15; 19 Nov 15:45 / 20 Nov 15:15 / 19 Nov 08:00; 32 h | 02:28; 16:17; 15:46 / 15:15 / 07:56; 32.2 h (8.7 h on one lane). Day 5 = 2026-11-21 (day 0 = 16 Nov, COM l.49-50) |
| doubling B1; Z(νν) top-ups; regeneration | + 46; + 45 / + 109; 29 | + 46.5; + 44.6 / + 108.9; 29.5 |
| toys 60 / 80 / 100; totals; band | 47 / 108 / 228; 4,663 / 4,723 / 4,844; 4,645–4,981 | 47.0 / 107.6 / 228.4; 4,663 / 4,723 / 4,844; 4,645–4,981 |
| old backend totals | 7,705 / 9,591 / 18,199; 7,080 and 23,564 | the same |
| B1 pool floor; pool sums | 23.0; 201 / 121 | 23.0; 201.0 / 121.2 |
| reach, frozen; as timed; both | 790 [712]; 514 [445]; 584 [514] | 790 [712]; 513 [445]; 581 [514] (B 133 / 177 / 234 and 85 / 111 / 143; R08-like B₅₀ 275 and 208) |
| looper bound; hard-scatter reading; gun size for 25 events | 1.9×10⁹, 1.9×10⁴, 2.2×10⁴; 251, 286; 8.7×10⁷, 264 CPU-h | 1.90×10⁹, 1.90×10⁴, 2.16×10⁴; 251, 286; 8.65×10⁷, 264 |

Differences: all within the Monte Carlo error of 10⁵ draws (at most 0.7 on a reading; the reach by 1–3 GeV).
Overrides: `OVERRIDES` and `OVERRIDES_V3` are those of version 3; `OVERRIDES_V4` (l.92-118) holds only the measured
pilot job costs, the production-code Geant4 costs, the option-(a) chain costs, the bytes per event, the toy units
and timings, and the unit costs of the test; none enters sections [1]–[7], [9], [10], [12] [V: read l.1-300]. The
sampler is `d15_q` (`strategy_budget.py` l.878-888 [V]). Not recomputed by me: the Q2 (c) grid of §4.6 (plausible:
the room below 300 falls from 224 to 139, and ×44 × 224 / 139 = ×71 against the printed ×67) and the per-test
false-FAIL probabilities of [5] [U].

Small points: "41 per in-road one" is the ratio of all to in-road (35.5 / 0.872); off-road per in-road is 39.7.
The R08 values in the "frozen at Gate A" column were not printed at Gate A (C-3).

## e. The decisions D1–D10

| # | options complete and fair? | numbers | missing or lenient |
|---|---|---|---|
| D1 | yes | 95 CPU-h is part 1 only; with the B1 part launched it is 142 | the C3 item and inventory row 19 (C-9); the currency of the zero and the 286 / 351 reading (B-3) |
| D2 | yes | 22–28 [V] | whether a shift enters the binding reading; the regeneration exposure (B-2) |
| D3 | yes | 47; 24 with 389; + 46 with 102 [V] | the production code is not finished (C-2); NI streams wait for B-1 |
| D4 | yes; (c) fairly put | 161 / 89 / 99 / 65 [V] | none |
| D5 | yes | 185 and 307; 196 and 319; 159 [V] | **named leniency 1**: one term instead of seven weight classes, 24 events; disclosure adequate (D5, §4.2) |
| D6 | yes | 186; 309 [V] | **named leniency 2**: three unread populations; disclosure adequate except the factor (B-4) and B1-e (C-10) |
| D7 | yes | 201 / 121; 1,094–1,984; 4,960–8,996 [V; the last two by the second review's script] | none; the confirmation at the corrected figure is asked, as required |
| D8 | yes | [V] | none |
| D9 | yes | [V] | β cut open (B-1) |
| D10 | yes | [V] | T1-b under the jax configuration not shown: stated |

Further leniencies against the frozen strategy read literally, beyond the two v4 names: (3) [L15] itself is not a
term although the strategy's convention gives every unpopulated term a zero-count allowance (section b; the user's
option B covers it, the number is missing); (4) every H is counted on hits without the later arcs (stated in
[L15] (iii), not in §0: B-3). I found no other.

Expected outcome of Gate A: v4's "unchanged" is supported for the pause (717 full-weight Z(νν) counts and 74–125
decays-in-flight counts expected, stdout [12] l.263: 1,632 × 0.4396 = 717 [V]) and for the leading term (the
conversions are in B4; no B1 normalisation enters). Two caveats are missing (C-11).

## f. Consistency

COM section: every row line cited starts with its identifier (l.23-25 header; l.168 C1-a; l.177-183 B1-a…g; l.197
B4-c; l.203, l.205 B6-a, B6-c; l.208 T1-a; l.216 T1-i; l.217 T2-a; l.249 PR-1; l.257 ST-1; l.258 INV-1; l.283 VC-3)
[V]; every number in it agrees with v4. Rows touched and absent: B2-a…c (a note), B6-d (if D2 shows an effect), C3
(C-13). Unchanged as claimed: the 16 T2 candidates, the criteria, Q1–Q5, and the pinned definition of rule 1
(samples that exist, max(floor, N_t·H), Gamma(m + 1)/M, no pool floor, a tie pauses at 299.1, 10⁵ draws) [V: STR
l.2730-2757 against v4 §4.3 and the script's `LIMIT`, `ND`]. Blinding: no v2 signal efficiency anywhere in v4, the
script or the stdout [V: grep]; the test of D2 is pile-up only. I looked at no signal quantity.

## Findings

### B (must be fixed before the user approves; exact text; line breaks inside quoted old text are to be ignored)

**B-1 Slow-fragment residue at production size.**
- v4 §3 P6, old: `no product hit before its production time; no slow product handed` → new: `no product hit before
  its production time in these 2,000-event files (at 25,000 events the check fails: (vi) below); no slow product handed`
- v4 §3 P6, old: `the B1 job counts such losses.` → new: `the B1 job counts such losses. (vi) **Found after this
  draft (LOG.md 18:15; campaigns p2-c-pa-val0, p2-c-pa-dg1):** at 25,000 events per file the hard check "no product hit
  before the vertex time" fails for NI-X (6 hits) and NI-C (1 hit). Five are correct (secondaries made along the
  parent's path before its final vertex; the check is now per product). Two hits, in one of 25,000 NI-X events, come
  from a fragment with β = 0.134, above the β cut of 0.1, with Fatras hits at t = −32 ns: a residue of the
  slow-fragment pathology, about 4×10⁻⁵ per NI-X event from one event, of order 160 events in the 4×10⁶ NI-X pilot
  sample. Its rate on 1.5×10⁵ NI events and a β scan (0.15, 0.2, 0.3) are being measured. **Release condition:** no
  stream with nuclear interactions (NI 22 / 30 / 61.5 mm, NI-X, NI-C, pilot.c0.hs, pilot.c0.lowpt) is released
  before this is settled, by a per-event flag that removes such events from the count m and reports their number, or
  by a higher β cut; a change of the β cut is put to the user.`
- v4 §0.3 D9, old: `criterion ≤ 2 % with multiplicity; one validated job per stream before its bulk is released` →
  new: `criterion ≤ 2 % with multiplicity; one validated job per stream before its bulk is released; the streams
  with nuclear interactions only after the slow-fragment residue found at 18:15 (1 NI-X event in 25,000, §3 P6 (vi))
  is settled: the β cut (0.1) may have to rise, which comes back to you`

**B-2 Reading and design of the robustness test.**
- v4 §1.5, old: `mixes it with a density change that the top-up rows of B6 already vary.` → new: the same sentence
  followed by ` Fixed with the third review: the density is fixed at the raw level at which the top-up ratios were
  derived (before CKF); the top-up crossings of the varied sample are a subset of the nominal sample's draws (the
  last ones of each layer are dropped), so that the pair differs only by the exchange of random crossings for arcs;
  where a layer of an event has more injected crossings than top-up crossings its top-up is zero and the excess is
  reported. The injected crossings pass the chain and the top-up does not, so the chain stage of the varied sample
  holds about 37 % more hits (+ 0.5–1 CPU-h, inside the range below).`
- old: `object of [SD4], errors from the bootstrap over events.` → new: the same followed by ` Read in addition, at
  no CPU and without a verdict: (a) in the varied sample, the candidates at R04–R06 with at least one double-crossing
  layer whose two hits come from one particle, one of them beyond half a turn (truth): the direct count of a looper
  together with pile-up, which r alone could hide if the loss of random crossings and the gain of arcs cancel;
  (b) r at the 2S crossing rungs (N_2S2 ≥ 1, 2, 3 on top of R04–R06, STR §4.0 point 7), because 20 % of single loopers
  cross a 2S layer twice in both sensors [V: p2-c-px-lpds] and the missing crossings are largest in the outer layers.`
- old: `the measured log-shift is carried by the pile-up estimate as a nuisance of the measured size, extrapolated
  to depth with the width of STR §4.0 point 7, and the day-15 reading is quoted with it.` → new: `if r(R06) > 1 the
  pile-up estimate is multiplied by r(R06), with a width of its bootstrap error and the width of STR §4.0 point 7
  counted from R06; no credit is taken for r < 1. This is a correction of an estimate known to lack hits, not a
  symmetric nuisance. [SD17] allows it: the variation is not a round number but is defined by a source (Geant4
  transport of the same particles), like the top-up limits and the tune (STR l.1477-1478). **With D2 the user chooses**
  whether the binding day-15 reading uses the corrected pile-up term (recommended; stricter than the pinned Df-11) or
  Df-11 stays as pinned and the corrected reading is reported beside it.`
- old: `Whether a measured two-simulation difference may enter as a nuisance under [SD17] (STR l.1469-1482) is for
  the reviewer and the user; the alternative is the next bullet.` → delete.
- old: `or rising with depth beyond its error` → new: `or ln r(R06) − ln r(R04) above zero by more than 2σ of that
  difference`
- old: `*When.* Before the freeze (Phase 3, by day 15), on development-role events` → new: `*When.* By decision
  point 2 (day 15), two days before the freeze (day 17, STR l.2267), on development-role events`
- old: `After the freeze the outcome "effect" could no longer lead to a chain fix.` → new: the same followed by ` A
  chain fix regenerates the whole pilot (≈ 142 CPU-h, about three days on two lanes) and moves the day-15 reading;
  this exposure exists from the moment the B1 part is launched on the present chain.`
- v4 §0.3 D2, old: `can still lead to a chain fix. Decline` → new: `can still lead to a chain fix (which regenerates
  the pilot, ≈ 142 CPU-h and about three days); with it you choose whether a measured increase enters the binding
  day-15 reading (recommended) or is reported beside it. Decline`

**B-3 §0.1, items 1 to 3.**
- old: `So the simulation is kept.` → new: `So the simulation is kept. The zero is in candidates of the frozen finder,
  its seed threshold included. The day-15 rule counts something wider (near-pass classes on a term's own hits,
  without the seed threshold), for which the code does not exist yet: by multiplicity alone 3.5 % of these loopers
  could reach R04 and 10 % its near-pass classes [V], an upper bound, not a value. The stored gun events are
  classified with that code when it exists (no new simulation).`
- old: `uses [E]. The test fired one particle at a time.` → new: `uses [E]. Read for the curling particles of the
  hard-scatter event itself the same zero allows 286 events [E]; as one more zero-count term of the day-15 rule it
  would put an empty pilot at about 350 at R09 instead of 161 (265 with both gun sets as one sample) [E: third
  review]. It is carried as a limitation and not as a term: that is what your option B gives, and it is the most
  lenient point of this draft. The test fired one particle at a time.`
- old: `pile-up estimate is the one term the day-15 rule takes from the present simulation without any allowance: if
  the` → new: `no term of the day-15 rule carries an allowance for the missing arcs (every count is made on the
  present simulation), and the pile-up term is the one whose hit pattern is known to lack a third of its correlated
  hits: if the` (the words `It matters because the` before it become `It matters because`).

**B-4 The factor in D6.**
- v4 §0.3 D6, old: `the B1 terms are under-read by up to a factor 2 |` → new: `the B1 terms are under-read by a
  factor up to 2.4 for one population (low p_T at twice the pool's yield) and 2.7–3.4 for the three together
  (1 + 0.7–1.4 + 0.5 + 0.5) |`
- v4 §7.1, old: `under-read by a factor up to about 2 (D6)` → new: `under-read by a factor up to 2.4 for one of them
  and 2.7–3.4 for the three together (D6)`

### C (suggestions; exact text; no re-review needed)

- **C-1** §0.1 item 6, old: `The check used by the second review missed the fault; the stricter measure is now the
  criterion.` → new: `The second review found the fault with a check that counts a surface once; that check
  understated it (30–34 % for 58–67 %) and would have passed the time cut (1.4 % / 1.1 % where 40 % / 45 % are
  missing). The measure with multiplicity is now the criterion; it compares numbers of hits per surface, not
  positions.` COM B1-a, old: `(the once-per-surface measure missed the fault)` → new: `(the once-per-surface measure
  understated the fault and would have passed the time cut)`.
- **C-2** §0.1 item 7, old: `waits for your approval and should start when Z(νν) ends, about` → new: `waits for
  your approval and for its production code (no campaign file exists yet; one validated job per stream comes first,
  §3 P7) and should start when Z(νν) ends, about`
- **C-3** §0.2, old: `| 156 / 181 / 204 | 238 / 262 / 284 |` → new: `| 156 / 181 / 204 (not printed at Gate A, which
  said "at fewer counts"; same computation) | 238 / 262 / 284 |`. §0.1 item 5, old: `(41 per in-road one [V])` → new:
  `(40 per in-road one [V])`.
- **C-4** §4.3, old: `(term list), l.744-746 (truncation and the choice between two variants: decided per stream,
  P6), l.797,` → new: `(term list), l.728-730 (the 1,000 looper events kept as a diagnostic population: §1.1 point
  1), l.744-746 (truncation and the choice between two variants: decided per stream, P6), l.788 ("a true ceiling":
  true inside the chain; the later arcs are in neither H nor the overlays, [L15] (iii)), l.797,`. Old: `l.1027, l.1071
  (looper row), l.1091; §4.7 l.1308-1313;` → new: `l.1027, l.1071 (looper row), l.1091; §4.7 l.1306 (loopers inside
  the B4 terms: first half turn only), l.1308-1313;`
- **C-5** §1.1 point 5, old: `**Not known, not looked at:** whether a quirk pair ever makes more than half a turn in
  Stage 3, and whether Stage 3 has a path or time cut of its own (not read in this session; no v2 signal quantity was
  computed or looked at).` → new: `**Read by the third reviewer (code only; no signal quantity):** the Stage-3
  propagator has no turn or path limit. It records every root of every chord and ends a pair at the exit (r = 118
  cm, |z| = 293 cm), at t_end (1.3 r_exit/β_T + 50 cm/c by default), at its step and hit caps (2×10¹⁰ steps, 4×10⁵
  hits) or at β_stop (TT/sim/stage3/code/T3_causal_s3.py l.262, l.300-312, l.489, l.505-513, l.579-582;
  run_stage3.py l.233). The pair's own hits are therefore not truncated by [L15]. **Still open:** how many pairs end
  at a cap and not at the exit (a truth-level census, from v1's tracked record, or added to BL-1 with the user's
  agreement, before the freeze).`
- **C-6** §7.1 point 1, old: `The Geant4 reference of the half-turn fractions still lacks 1 % of the tracks (its
  rerun is queued): lower bounds.` → new: `With the complete Geant4 reference (p2-c-pa-htg, LOG.md 18:15) the
  fractions are 25.2 % and 37.5 %; they remain lower bounds because detector secondaries are not compared.`
- **C-7** §3 P6 (ii), old: `on the first half turn the two agree for 98–99.9 % of the crossings.` → new: the same
  followed by ` In position the two parents differ on the same surface of the first arc by 0.4–0.8 mm (median) and
  5–8 mm (90 %) in rφ [V: ab_abs_drphi of p2-c-px-val2-0.json, radius rows], so the hybrid parent has a step of
  that size at the seam, far above the finder's 30 µm tolerance; the ≤ 2 % criterion counts hits per surface and
  does not see it, and the injected hits are the Geant4 crossings themselves, so the criterion is a closure of the
  injection, not an independent test. No bias of H is expected from the step (the alignment of a curling parent's
  arcs in one plane is accidental); none is measured.`
- **C-8** §3 P7, old: `(P6 (iv)); no job has run at production size for the chain streams.` → new: `(P6 (iv); a
  per-mode check was written into p2x_validate.py at 17:25 by the successor session and has not yet been run on an
  option-(a) file); no option-(a) job has run at production size (the first-arc streams at 25,000 events pass the
  parent check, 0.00–0.18 %, and show the residue of P6 (vi)).`
- **C-9** §0.3 D1, old: `pile-up case untested) |` → new: `pile-up case untested). With (a) you also approve two
  changes of items frozen at Gate A: a 25th item of the paper-correction list C3 ("v1's looper bound of 168 events
  and its 0 in 10⁵ measured nothing"), and the 1,000 looper overlays of inventory row 19 made from Geant4 crossings
  injected as hits, not with Fatras (same size, same cost order) |`
- **C-10** §0.3 D6, old: `all three stated as untested. (b)` → new: `all three stated as untested; the analytic
  bound of COM B1-e ("soft bulk excluded") is no longer claimed until it is written and checked. (b)`
- **C-11** §0.2, old: `reach below 243 GeV | unchanged | **unchanged** |` → new: `reach below 243 GeV | unchanged |
  **unchanged**: about 700 Z(νν) pilot counts expected against a pause at 4 [12]. Not in it: the three new classes
  (2.4×10⁸ vertices, no v1 count) can only add, and v1's conversion counts were themselves made without the later
  arcs |`
- **C-12** COM, three rows to add to the section "Changes of rows by addendum 1":
  `| B2-a, B2-b, B2-c (l.184-186) | unchanged; noted: both estimators, the occupancy model's correlation factors and the direct counts are made on the same chain, so their closure cannot see [L15] (ADD4 §1.1 point 2) |`
  `| B6-d (l.206, Df-7) | only if D2 is accepted and the row shows an increase: it enters as a correction of the pile-up estimate with its measured error, a source-defined variation (STR l.1477-1478), by the reading of ADD4 §1.5 |`
  `| C3 (l.176) | proposed with ADD4 D1 (a): a 25th item, "v1's looper bound measured nothing" |`

## Verdict

**ITERATE** on B-1 to B-4. No Category A. Not ESCALATE: nothing here needs a decision that is not already in
D1–D10 once the texts above are in (D2 gains one sub-choice, D1 two disclosed consequences, D9 one condition). The
running part of the pilot is not touched by any finding. The B1 part must not be submitted before B-1 is settled and
one job per stream has passed the validation with the per-mode check; that is a matter for the release condition and
does not need another review round.
