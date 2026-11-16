# Strategy addendum 1, version 3 (DRAFT, pending the third review and user approval)

Fixer: Yvonne, 2026-11-16 (stamp in the file name, `date`). Replaces versions 1 and 2
(`STRATEGY_ADDENDUM_1_tatiana_2026-11-16_13-31.md`, `STRATEGY_ADDENDUM_1_v2_tatiana_2026-11-16_14-14.md`; both kept
unchanged) after the second critical review `review/critical/ADDENDUM_1_v2_CRITICAL_REVIEW_wanda_2026-11-16_14-37.md`
(ITERATE: 2 A, 5 B, 12 C). Finding-by-finding record: `FIX_REPORT_addendum1_v3_yvonne.md`. This document is
self-contained: with `STR` = `STRATEGY_oscar_2026-11-16_10-41.md` (**not edited**) and `COM` = `COMMITMENTS.md` a reader
needs neither earlier version.

Tags. **[V]** measured in Phase 2, campaign named (data `/nfs/cajuela/jdochoa/quirks_v2/data/p2c/<campaign>/`, logs
`/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/<campaign>/`). **[E]** estimate printed by
`phase2_exploration/src/p2y_addendum1.py`; its complete output is `phase1_strategy/outputs/addendum1_v3_stdout.txt`
and "[n]" below is the section of that file. **[U]** transcribed, not checked. The script runs a byte-identical copy
of the Phase-1 budget script (sha256 548b5ba8…) with named overrides, and reproduces the frozen numbers before
changing anything (76 [36–152]; 790 [712] GeV; K = 10 and T_c = 19 family sizes) [4], [5], [10]. Nothing in this
addendum is in force until it has passed review and the user has approved it. No pilot campaign is submitted by it.

## 0. For the user

### 0.1 What you should read first

1. **The pause at day 15 remains the expected outcome, as at Gate A.** By v1's own conversion counts the pilot is
   expected to hold about 700 full-weight Z(νν) counts and 70–125 decays-in-flight counts; the rule pauses at 4 and
   at 6 [12], [4]. Nothing here changes that (STR l.74, l.97-99). What this addendum changes is the other branch: how
   small the pilot's counts must be for the study *not* to pause.
2. **That room has shrunk.** Counted on everything Geant4 produces, the single-interaction normalisation is 3.7×10⁸
   vertices in 3 ab⁻¹, not 6.8×10⁷. With the samples proposed here an empty pilot reads **B₅₀ = 161 events at an R09
   candidate** (76 at Gate A; limit 300) and **238 / 262 / 284 at an R08 candidate** (pile-up estimate 88 / 118 / 148
   events). The study then pauses at 4 Z(νν) counts or 6 counts in one large B1 sample (R09), and at **1–3 counts
   in any sample at R08**: at R08 the rule can tell "empty" from "anything", no more [4].
3. **The size of that number is set by a convention as much as by the measurements.** Every term of the likelihood
   carries its own zero-count allowance. The same 1.7×10⁷ B1 events read as one term give 62, as three terms 96, as four terms
   with the other classes left out 85, as seven terms 159 (161 with the hard-scatter parents) [4]. The draft follows
   the strategy's convention (seven); the alternatives are decision D1.
4. **Three populations are not read by the rule in this draft, and no test bounds them** (§2 P2, §6): parents of
   0.3–0.5 GeV (0.7–1.4 times the normalisation that is read [E]), parents at 1 < |η| < 1.5 (half as many again
   as the pool [V]), and hard-scatter
   hadrons outside the road (41 per in-road one [V]). The draft samples the first as an alarm only: one count there
   is 1,300–2,600 events, so its zero bounds nothing. Reading it as a term costs 21–35 CPU-h and makes an empty
   pilot pause at the upper R08 estimate (decision D4).
5. **Version 2 called the hand-over "validated as proposed". It was not, for two of the seven classes.** For
   parents that have turned, 30–35 % of the parent's crossings before the vertex had no hit [V] (§2 P6). The fix
   (truncation by time) is coded by the channel's executor; its re-validation is **pending** (one line in P6).
6. **The pool at the approved CPU**: summed zero-count allowance 201 events as timed, 121 with two cost measures of
   which one is not yet demonstrated, against 12.6 at Gate A. Your decision of 2026-11-16 to keep the 457 CPU-h was
   taken on 36–42; it needs confirming at these numbers (D6). Reach if every ceiling is empty: 514–584 GeV median
   [445–514 at the 84 % edge], against 790 [712] [10].
7. **Toys**: on the measured scaling the projected total is 7,710 CPU-h at 60 parameters, above the stop-and-ask
   threshold of 5,992. A backend change measured by another executor would bring it to 4,729–5,141; that result
   has not been reviewed [U] (D7).

### 0.2 Numbers shown at Gate A or since, and what they are now

All version-3 values are printed by the script ([13] and the sections named). "Per count" means events in 3 ab⁻¹
that one counted pilot event stands for.

| quantity | frozen at Gate A | addendum v1 | addendum v2 | **version 3** |
|---|---|---|---|---|
| single-interaction vertices in 3 ab⁻¹ behind the B1 terms | 6.8×10⁷ (4 terms) | 1.6×10⁸ (5 terms) | 3.66×10⁸ (7 terms) | **3.66×10⁸** (7 terms; class counts sum to 193,313 of 245,945 vertices, not 190,730 as v2 printed) [1] |
| one decays-in-flight pilot count | 65 events | 78 | 26.5 (sample 4×10⁶) | **25.9** (hard-scatter share now on its own sample) [2] |
| one count, decays after a turn | not a term | not read | 24.4 (new term) | **23.9**; read only after the hand-over fix (P6) |
| one nuclear-interaction count at 22 / 30 / 61.5 mm | 0.88 / 1.12 / 1.12 | 4.0 / 5.1 / 5.1 | 4.9 / 6.6 / 6.6 | **4.8 / 6.5 / 6.5** |
| one count, interactions in other layers; after a turn | not terms | 74; not read | 23.7; 24.9 (new) | **23.2; 24.3** |
| one count in the hard-scatter-parent sample | inside the terms, no sample | no sample | "≈ 40", not in any table | **4.0** (2×10⁶ vertices; 39.6 with v2's 2×10⁵) [3] |
| one Z(νν) pilot count (all SM processes and multijets) | 18 | 41 | 41.2; 2.1 for a low-weight event | **41.2; 2.1**; provisional until the day-12 MET model |
| day-15 reading with an empty pilot, R09 candidate (limit 300) | 76 | 120 / 191 | 159 (without the hard-scatter sample it said it read) | **161** [16–84 %: 109–232] |
| the same at an R08 candidate, pile-up 88 / 118 / 148 | not printed; 156 / 181 / 204 by the same computation | 225 / 295 | 237 / 261 / 283 | **238 / 262 / 284** |
| pause at how many Z(νν) counts: R09; R08 | 12 (a tie pauses); 8 / 7 / 6 | 3–5; 1–2 | 4; 2 / 1 / 1 | **4; 2 / 1 / 1** |
| pause at how many counts in one large B1 sample: R09; R08 | 4; 3 / 2 / 2 | 2–3; 1–2 | 6; 3 / 2 / 1 | **6; 3 / 2 / 1** |
| pilot generation | 54.5 CPU-h, 52 GB | 108 CPU-h, 97 GB | 131 CPU-h, 144 GB | **135 CPU-h, 156 GB**; 45–67 h on 3–2 slots; Z(νν) + minimum bias (91 CPU-h) start first [8] |
| summed zero-count allowance of the pool at 457 + 208 CPU-h | 12.6 (SM 8.6) | 94–101 | 175–213 as timed, 99–137 with two measures | **201 as timed, 121 with both measures** (B1 part 43 → 23, low-weight classes + 5 to + 9); four-term variant 175 / 99 [9] |
| reach if every ceiling is empty, R09-like, median [84 % edge] | 790 [712] GeV | not given | 506–597 [443–524] | **514 [445] as timed, 584 [514] with both measures** (four terms 522 [451], 597 [524]) [10] |
| the same case at an R08-like selection: B₅₀ in the result | 113 | — | not given | **275 as timed, 208 with both measures** (class limit 300) [10] |
| closure-test family K; ceiling-test family T_c | 10; 19 | 10; 20 | not stated; 22 | **13; 22**. A correct analysis loses a selection to a false FAIL with 7.0–9.9 % (6.9–8.9 % before) [5] |
| extra CPU in 4a for the three new terms | — | not given | + 41 CPU-h | **+ 41 CPU-h** (designs named, not written) |
| projected total (approved 4,609; threshold 5,992) | 4,609 | "unchanged" | 4,780 / 7,700 | **4,787 at the 31-parameter toy cost; 7,710 at 60, 9,604 at 80, 18,246 at 100 parameters**; 4,729–5,141 with the unreviewed backend change [11] |
| Q2 (c): conversion rejection needed if the pilot counts no decay in flight | ×44 (×30 at the weighted photon rate) | unchanged text | unchanged text | **×67 (×46)**; at a quarter of v1's decays-in-flight size ×222 or none (was ×75–150) [12] |
| expected outcome (STR §0) | pause at day 15; background ≈ 0.7–1.0×10⁴ events led by hard-scatter conversions; reach below 243 GeV | unchanged | "not changed by the floors" | **unchanged**: that term is in the SM events (B4), no B1 number enters it. Its decays-in-flight part (385–647 events) becomes 481–810 with the Geant4 first-arc yield [12] |

New measured fact not shown before: photons of the pile-up interactions make **2.4 conversion vertices per triggered
event in the road, 1.0×10⁸ in 3 ab⁻¹** [V: 52,583 in 1.5×10⁶ firings, p2-c-part-0; [1]]. By the frozen route table
(STR §2; §4.4 point 1, l.738-739) they belong to the pile-up term B2, where Fatras makes them inside the pile-up
events; rule 1 reads them through the pile-up estimate only (median 6.7 events at R09).

### 0.3 Decisions

| # | decision | options, with empty-pilot reading R09; R08 (88 / 118 / 148) and cost | drafted / recommended |
|---|---|---|---|
| D1 | How many B1 terms | (a) **seven**: 161; 238 / 262 / 284. K = 13, T_c = 22, + 41 CPU-h in 4a. (b) four, the other classes recorded and left out: 89; 167 / 190 / 212; K = 10, T_c = 19; 2.4×10⁸ vertices unread on no evidence. (c) fewer terms on the same events: three (decays; three radii; other interactions) 99; 177 / 201 / 223, or one 65; 144 / 168 / 190; K = 9 or 7, T_c = 18 or 16; needs a new closure design for B1-a, frozen at Gate A (§3.2) | (a): it is the strategy's convention. (c) is legitimate and cheaper in zeros, but re-opens B1-a |
| D2 | Hard-scatter parents | H1 a 2×10⁶-vertex sample, parents from the Z(νν) pilot events, one term: 161; 238 / 262 / 284; 4 CPU-h. The same read as seven weight classes (STR l.1564 literally): 185; 262 / 286 / **307**. H2 the 2×10⁵ sample of v2: 196; 273 / 297 / **319** (one term), 432 (seven classes). H3 not read, a stated leniency: 159; 237 / 260 / 282. Option on top: hadrons outside the road as a second stratum, + 15 CPU-h: 186; 263 / 287 / **309** | H1 as one term. It is 24 events more lenient than the literal weight-class reading; said here, not hidden |
| D3 | Pilot size | Z(νν) 2.3×10⁶ generated (81 CPU-h; cleared to start, more can be appended): pause at 4 counts. 3.5×10⁶ (+ 42 CPU-h): 148; 225 / 249 / 270, pause at 6. 5.23×10⁶ (+ 103 CPU-h): 139; 216 / 239 / 261, pause at 9. B1 samples doubled (+ 43 CPU-h): 102; 179 / 203 / 225, pause at 16–17 B1 counts | 2.3×10⁶ now; decide the top-up when the first counts are seen at day 7 |
| D4 | Parents of 0.3–0.5 GeV, and at 1 < \|η\| < 1.5 | (a) alarm samples only (2×10⁵ events; one count = 1,300–2,600 events; a zero bounds nothing), stated as an untested limitation. (b) low-p_T as an eighth term sized for 25 events per count: + 21–35 CPU-h; 186; 263 / 287 / **309** | (a), knowing what it leaves open; (b) if you want the population read |
| D5 | R08 candidates | accept that an R08 candidate pauses on 1–3 counts (and on an empty pilot at the upper pile-up estimate under the bold options above), or enlarge by D3 | accept |
| D6 | Pool | confirm 457 + 208 CPU-h at 201 (as timed) or 121 (forced top decays for four samples, one of them run; preselection before the chain, which gives up re-weighting under a varied MET model); or add CPU: an SM allowance of 39 needs 1,094–1,984 CPU-h, 8.6 needs 4,960–8,996 | confirm; tables carry "as timed" until each measure is demonstrated |
| D7 | Toys | the stop rule applies on the measured numpy scaling; the backend change is with another executor and is not part of this addendum | no change of COM T1-i until that result is reviewed |
| D8 | Hand-over rule | parent truncated at the vertex **time** for the classes after a turn (a change of STR l.744, "v1's Truncate"); bulk release of the B1 streams only after the re-validation and one validated job per stream | approve |

The reading is "at the limit" from 299.1 (a tie pauses, STR l.2757). Bold values pause on an empty pilot.

## 1. Why: Phase-2 measurements ("Phase 1 assumed / Phase 2 found / implications")

1. **Unit costs.** Assumed 45 ms per no-pile-up hard-scatter event (STR l.356). Found 127 / 171 / 571 ms for Z(νν) /
   W(τν) / tt̄ 1ℓ per generated event [V: p2-c-t-hs0], 327 ms for tt̄ with forced W decays through the chain
   [V: p2-c-t-ttf, 2 × 1,250 events]. Implications: §3.4, §4.
2. **Preselection.** Assumed pilot and pool events are preselected events. Found: the generator gives events with
   truth MET > 200 GeV; v1's preselection weights them: mean 0.4308 ± 0.0049 / 0.2604 ± 0.0043 / 0.1180 ± 0.0031, in
   two weight classes (≈ 0.98 and ≈ 0.05) of 4,397 + 25, 2,633 + 516, 1,159 + 946 events in 10⁴, the rest at zero
   [V: p2-c-t-hs0]. Implication: M of a sample is Σw/w_max of its full-weight class (0.4396, 0.2657, 0.1205 of the
   generated events), and the 0.05 class is a second counted term (STR l.1564).
3. **Geant4 vertices.** Assumed the v1 rates (straight-line decays at 30–1000 mm; interactions at three radii ×
   0.22). Found [V: p2-c-part-0, 1.5×10⁶ firings of every pool species through the whole tracker]: 245,945 vertices,
   each in exactly one class (§2 P3). Reproduced independently by both reviewers from the stored vertices.
4. **Hand-over.** Assumed Fatras takes every Geant4 product at the vertex. Found it cannot: slow fragments give
   hits before the vertex time [V: p2-c-val-b1]. Products are therefore followed by Geant4 to the exit of their slab
   and those with β < 0.1 are not handed over (§2 P6). The running Fatras instance neither decays nor absorbs
   hadrons: of 40,000 K±, π±, p each 99.96 / 99.98 / 99.96 % reach the outermost barrel layer, p − K = −0.00003 ±
   0.0007 against 0.09 if kaons decayed [V: p2-c-part-fatras]. The parent truncation was faulty for parents that
   have turned (§2 P6).
5. **Toys.** Assumed "may double" (STR l.1720-1722). Found 638 s per 1000 + 1000 toys at 31 parameters, ×17 at 60,
   ×27 and ×75 at 80 and 100 (12 toys each: indications) [V: p2-c-t-pyhf]. Implication: §4.
6. **Fatras step limit** (all samples; not caused by this addendum): 0.03–0.07 particles per hard-scatter event,
   mostly conversion positrons, are dropped with all their hits [V: logs of p2-c-t-hs0, p2-c-t-ttf]. Open point 5.

## 2. Definitions

**P1 Z(νν) pilot: 2.3×10⁶ generated events** (STR l.869; cleared by the orchestrator to start ahead of the B1
streams together with `pilot.mb`; no finding touches them; events can be appended later). m_Z counts events of the
full-weight class: M = 1.011×10⁶, one count = 41.2 events for all SM processes and the multijets (24.8 for Z(νν)
alone); an event of the 0.05 class is counted in a second term at 2.1 events per count [2]. **"41" is provisional:**
it uses v1's preselection and is recomputed with the v2 MET model at day 12 from the generator-level summary stored
with every event. That summary now also holds the scalar sums of the visible final state (|η| < 5 and < 3) and the
final hadrons and photons with |η| < 1.5 and p_T > 0.3 GeV (≈ 1 kB per event [E]; review C-8; in `p2x_hs0.py`), so
that a MET model in ΣE_T needs no regeneration and the hard-scatter parent pool exists at no cost. Jets are stored
down to 15 GeV, not the 10 GeV the review suggested.

**P2 Parents, road, and what is outside.**
- *Pool.* Every π±, K±, p, K⁰_L, n, γ produced within 1 mm of the interaction point with 0.5 < p_T < 20 GeV and
  |η| < 1, natural Pythia mixture, uniform azimuth: 7.13 per minimum-bias interaction, 0.3405 inside a road of
  half-width 0.15 [V: p2-c-part-0].
- *N_t* of a class = N_trig × 200 × 0.3405 × (class vertices per firing) × 1.022 [1]. The last factor is the
  hard-scatter share. It is an upper-side planning value: v1's rates give a share of 0–3 % (v1's total 1.5687–1.5945
  per triggered event, STR l.255; v1's formula on minimum bias × 200 gives 1.560 on 40,000 interactions [U], 1.613 on
  the 25,000 of the partition campaign and 1.594 on 125,000 [V: p2-c-px-mbb-big]), and a first direct count gives 0.872 ± 0.032 pool parents inside the
  road per triggered Z(νν) event against 68.1 from minimum bias, 1.3 % [V: validation slice p2-c-px-hsg-r0, 2,000
  generated events; [1]].
- *Hard-scatter parents (finding A-2).* These parents are stiffer than the sampled ones, so they get their own
  sample **`pilot.c0.hs`: 2×10⁶ vertices in the natural mixture of the seven classes**, from parents inside the road
  of their own event (the frozen definition of N_t), fired through the same Geant4 pass and chain, with the true
  offset to the event's MET road stored. Parents: the stored hadron list of the 2.3×10⁶ Z(νν) pilot events, drawn in
  proportion to the event weight: 8.3×10⁵ distinct parents, 19 firings and 2.4 vertices each [E from V; 3]. With the
  2×10⁴ generator-level events of version 2 the same sample would be 2,100 firings of each of 7,200 parents, and a
  zero would say little about the stiff tail. Rule 1 reads it as **one term**: N_t = 7.9×10⁶ (the 2.2 % share; 4.6×10⁶
  by the measured parent count and the minimum-bias yield), one count = 4.0 events; the seven class samples are
  then normalised to the minimum-bias share alone. Cost 4.1 CPU-h [3]. Options and their readings: §3.1, D2.
- *Road orientations (finding B-1).* B1 events are fired at uniform azimuth with the road left open. **The count
  m of a class sample is the number of (event, road orientation) passes over 21 fixed orientations of full width
  0.30, axes at φ_road + 2πk/21** (STR l.864-866; recorded in the job metadata by `p2x_b1.py`), with N_t as defined
  above. This is exact for the minimum-bias share: summing over orientations integrates over the parent's offset
  from the road, so candidates of curling parents and of wide-angle products in a road that does not contain the
  parent's initial direction are counted. 21 × 0.30 = 6.30 against 2π: the grid over-reads by 0.27 %, on the strict
  side [6]. An event that passes in more than one orientation is counted each time (strict) and flagged. N_t and the
  events per count do not change. For `pilot.c0.hs` the road is the event's own; **hard-scatter hadrons outside the
  road are not fired**: they are 35.5 − 0.87 per triggered event [V], 1.8×10⁸ vertices in 3 ab⁻¹ at the minimum-bias
  yield [E], and a candidate from them in the MET road is read by nothing in this draft. The minimum-bias samples
  measure how often an off-road parent makes a pass (the 20 other orientations); that fraction is reported at day 7
  as an alarm. Reading them directly is the second stratum of D2 (7.3×10⁶ vertices, 25 events per count, 15 CPU-h).
- *Lower p_T edge (finding B-2).* The edge at 0.5 GeV is a convenience of v1's rate definition, not a bound: a
  0.4 GeV parent crosses the inner layers and the three TBPS layers on its first arc. Parents with 0.3 < p_T < 0.5 GeV
  are 5.20 per interaction, 0.2484 in a road, 73 % as many as the pool [V: validation slice p2-c-px-mbb-big, 125,000
  interactions]. Their vertex yield is not measured; at one to two times the pool's, **N_t = 2.6–5.2×10⁸, 0.7–1.4
  times the seven classes together** [E; 6]. The check sample `pilot.c0.lowpt` (2×10⁵ vertices) therefore reads
  1,300–2,600 events per count: **its zero allows 1,500–3,000 events and bounds nothing at the scale of 300.** In
  this draft it is an alarm, not a term: no zero-count allowance enters rule 1 for it; one own-hit pass at a T2
  candidate rung is by itself above 300 and pauses the study; its pass rates at R04–R06 against the pool's are
  reported at day 7. Reading the population properly needs 1.0–2.1×10⁷ events (21–35 CPU-h) and adds a term (D4).
  No written bound (COM B1-e) excludes these parents; until one exists this is an untested population, and the
  paper would have to say so.
- *|η| > 1.* Parents with p_T > 0.5 GeV at 1 < |η| < 1.5 are 3.64 per interaction, 51 % of the pool [V:
  p2-c-px-mbb-big]: N_t = 1.9×10⁸ at the pool's vertex yield, which is not measured there [E; 6]; one count in a
  2×10⁵ check sample would be 940 events. `pilot.mb` keeps a second pool (0.3 < p_T < 20 GeV, |η| < 1.5, outside the
  main pool; `p2x_mbgen.py`), so a check sample can be made later without a new minimum-bias run. None is in the
  pilot: not tested, same consequence as the previous point.

**P3–P5 The partition and the terms** [V counts: p2-c-part-0; N_t and events per count: E, [1], [2]]. "First arc":
transverse path from the origin ≤ πR. N_t in the table includes the factor 1.022; "per count" is with the
hard-scatter share on its own sample (N_t/1.022/M).

| class (vertices in 1.5×10⁶ firings; by parent π± / K± / p / K⁰_L / n / γ) | term | stream | N_t | M | per count |
|---|---|---|---|---|---|
| decays of π±, K± on the first arc, any radius (53,063: 26,641 π±, 26,422 K±) and K⁰_L decays (2,906) | **DIF** | `pilot.c0.dif` | 1.061×10⁸ | 4×10⁶ | 25.9 |
| decays of π±, K± after the first turn (51,441: 35,970 π±, 15,471 K±) | **DIF-C** (new) | `pilot.c0.difc` | 9.75×10⁷ | 4×10⁶ | 23.9 |
| inelastic, first arc, beam pipe (2,583: 1,798 / 246 / 215 / 112 / 206 / 6) | **NI 22 mm** | `pilot.c0.ni22` | 4.90×10⁶ | 10⁶ | 4.8 |
| inelastic, first arc, TBPX L1 (3,502: 2,437 / 380 / 259 / 160 / 251 / 15) | **NI 30 mm** | `pilot.c0.ni30` | 6.64×10⁶ | 10⁶ | 6.5 |
| inelastic, first arc, TBPX L2 (3,496: 2,387 / 375 / 276 / 192 / 253 / 13) | **NI 61.5 mm** | `pilot.c0.ni61` | 6.63×10⁶ | 10⁶ | 6.5 |
| inelastic, first arc, every other layer (50,083: 35,874 / 5,035 / 3,469 / 2,489 / 3,083 / 133) | **NI-X** (new) | `pilot.c0.nix` | 9.49×10⁷ | 4×10⁶ | 23.2 |
| inelastic after the first turn, any layer (26,239: 24,271 π±, 1,185 K±, 783 p) | **NI-C** (new) | `pilot.c0.nic` | 4.97×10⁷ | 2×10⁶ | 24.3 |
| **sum of the B1 classes: 193,313** (+ 52,583 conversions + 49 other = 245,945 = all vertices) | | | **3.66×10⁸** | 1.7×10⁷ | |
| the hard-scatter share of all seven (2.2 % of the sum, upper side) | read as one term at day 15 | `pilot.c0.hs` | 7.9×10⁶ | 2×10⁶ | 4.0 |

- Conversions of primary photons (52,583) are not B1 (route table, §0.2). The 49 "other" vertices (stopped
  protons, 3 photons) are recorded.
- From 6.8×10⁷ to 3.66×10⁸ [1]: first-arc π/K decays inside v1's own range 30–1000 mm are 43,011, N_t = 8.15×10⁷
  against the frozen 6.51×10⁷ (×1.25: Geant4 against the straight-line formula, and the pool against v1's parent
  count); first-arc decays below 30 mm and beyond 1 m add 1.91×10⁷ and K⁰_L decays 5.5×10⁶; the three radii go from
  3.1×10⁶ to 1.82×10⁷ (the factor 0.22 removed: a Geant4 vertex is on its parent's path, and the fraction on the
  plane-hypothesis line is part of H; plus Geant4 yield and neutral parents); the three new classes are 2.4×10⁸, two
  thirds of the total.
- Decays after the first turn: 61 % (31,238 of 51,441) come from parents above 0.57 GeV [V: second review]; they
  turn inside the 1,200 mm Geant4 world and lose energy. The sagitta of a 0.5 m circle is 1.4–3.4 mm over the inner
  layers, below the ribbon widths. No written bound (COM B1-e) excludes these decays for the number of layers a
  rung requires, so DIF-C is a term. If the bound is written and checked before the freeze, the pre-registration
  may drop it; rule 1 at day 15 reads it.
- In the likelihood of Phase 4a the hard-scatter share is inside each of the seven terms, as frozen (STR l.726-727:
  each term "with a hard-scatter share and a ×200 minimum-bias share"): the 4a pool is produced after the freeze,
  when the class yields of the hard-scatter parents are known from `pilot.c0.hs`, and mixes them in at their
  natural proportion. The separate sample is a day-15 device.

**P6 Hand-over (finding A-1).** Products are followed by Geant4 to the exit of the slab of their vertex; products
with β < 0.1 there are not handed to Fatras (0.07–0.12 per NI event [V: p2-c-val-b1x]); the parent is a Fatras
particle truncated at the vertex; the Geant4 crossings of the parent before the vertex are stored with every event.
- *What version 2 validated* [V: p2-c-b1y, p2-c-b1yv; 1,000 events of each of eight streams; [7]]: closure of V4-1,
  no NaN, distinct seeds, no parent hit beyond the vertex radius, no product hit before its production time, 0 slow
  products handed over, 2 Fatras step-limit errors in 8,000 events.
- *What it did not report.* v1's `Truncate` removes the parent's hits by radius (`run_chain.py` l.284). A parent
  that has turned was at larger radii before its vertex, so those hits are removed although they precede it. In the
  first 100 events of each stream, of the Geant4 parent's crossings of a counting surface before the vertex, **433 of
  1,464 (DIF-C, 30 %) and 514 of 1,463 (NI-C, 35 %) have no Fatras parent hit**, against 0 of 988 (DIF) and 2 of 877
  (NI-X). In the other direction, 8 of 9,968 (DIF) and 88 of 7,585 (NI-X) parent hits are later than the vertex time
  (the undecayed Fatras parent returning inside the vertex radius). With that hand-over the pilot would have written
  6×10⁶ of its 1.7×10⁷ B1 events with a third of the parent's pre-vertex crossings missing, and H on own hits (Df-9)
  would have been read low for two of the four large terms. "Validated as proposed" was wrong for these two classes.
- *Rule proposed.* For the classes after a turn (DIF-C, NI-C, and the events of those classes in `pilot.c0.hs` and
  `pilot.c0.lowpt`) the parent is truncated by **time**: parent hits later than the Geant4 vertex time are dropped
  (a new algorithm in `p2x_b1.py`; v1's code is not edited). First-arc classes keep v1's radius cut unless the
  comparison below shows the time cut is at least as good there, in which case one rule (time) serves all. New hard
  check in `p2x_validate.py`: Geant4 pre-vertex crossings of a counting surface without a Fatras parent hit ≤ 2 % in
  every stream.
- **A-1 re-validation: pending, campaign `p2-c-px-tr`** (session Xavier: 2,000 events of every stream with the
  radius cut, the time cut and both; defined in `p2x_pilot_campaigns.py`, not yet run when this was written).
  No result is claimed here.
- The second variant of STR l.744-746 (parent hits made from the stored Geant4 crossings) stays buildable from the
  stored records; it has not been validated and is not proposed.
- Fatras parent against Geant4 parent, version-2 validation: median 0.5–0.9 mm, 4–8 mm at 90 % for the four large
  classes; 5–8 µm at the inner radii [V: p2-c-b1yv].

**P7 Streams and state of the pilot code (finding B-4)** [facts from `phase2_exploration/logs/executor_xavier_2026-11-16_14-23.md`
and the files in `phase2_exploration/src/`, read 14:56].
- Streams: `pilot.mb`, `pilot.g4`, `pilot.hs0.znn`, `pilot.c0.{dif,difc,ni22,ni30,ni61,nix,nic,hs,lowpt}`. One vertex
  per event; road and PV stored, not fixed at generation.
- Exists and has run at slice size: `p2c_hs0.py` and `p2c_mbgen.py` (version-2 timing campaigns); the extended
  `p2x_mbgen.py` (two reproducibility jobs with identical content hash, 3.6 ms per interaction; its first version
  mis-set the cuts of the v1 rate formula, was found by its own slice and rewritten, rerun as p2-c-px-mbb) and the
  generator-level hard-scatter pool `p2x_hspool.py` [V: p2-c-px-mb, p2-c-px-mbb, p2-c-px-hsg].
- Written between 14:34 and 14:55 on 16 November and **not yet validated**: the production vertex job
  `p2x_g4prod.py` (reads the pool from the minimum-bias files; one vertex file per class group; asserts one class
  per vertex), the chain job for a class list `p2x_b1.py` (DIF = dif or k0l; truncation mode and β cut as
  arguments), the Z(νν) job with the extended summary `p2x_hs0.py` (its first slice failed on a coding error and
  was rerun under a new name), the validation `p2x_validate.py`, the campaign generator
  `p2x_pilot_campaigns.py`. Its B1 slices (`p2-c-px-g4`, `p2-c-px-b1`, `p2-c-px-tr`, validation) had not run.
- **Nothing here claims the B1 production code is ready.** Commitment: one job of every stream is passed through
  `p2x_validate.py` (all hard checks, including the new one) before the bulk of that stream is released. The β cut
  is a parameter of the campaign (0.1), no longer an environment variable that defaults to the variant that failed.
  'all'-pass Geant4 jobs hold at most 2×10⁶ firings (the partition job used 2,161 MB for 1.5×10⁶ against a guard of
  3,750 MB): 62 jobs of 10 min [8]. The 'all' pass fires 3 % more than the smallest class needs (NI-X had no margin).
- The partition file `outputs/partition_p2-c-part-0.json` was written by hand-run code after the class definition
  was last edited (the job's own metadata carries the classes of 14:07, before the radial cut was removed); both
  reviewers reproduced every count from the stored vertices. The pilot's own partition is written by
  `p2x_g4prod.py` with its code hash and supersedes it.

## 3. Replacement tables [E]

### 3.1 Rule 1: empty-pilot reading and crossings [4]

B₅₀ with every count zero and the first count at which the reading is at or above 299.1 with the others at zero
(medians of 10⁵ draws, common random numbers; three other seeds move the draft row by at most 1.2). R08 over the
strategy's pile-up range (STR l.2819). The R08 values of the frozen case are computed here; STR prints only R09.

| reading | empty pilot, R09 | R08 at pile-up 88 / 118 / 148 | pause at m_Z: R09; R08 | pause at counts in one of DIF, DIF-C, NI-X, NI-C: R09; R08 |
|---|---|---|---|---|
| STR as frozen (4 B1 terms, v1 N_t, 10⁶ per sample, 18.1 per Z count) | 76 | 156 / 181 / 204 | 12 (299.6; 300.2 with the strategy's own sampler: a tie pauses); 8 / 7 / 6 | DIF 4; 3 / 2 / 2 |
| seven terms, 10⁶ per sample (the strategy's pilot sizes) | **389** | **467 / 491 / 515** | pauses when empty | pauses when empty |
| seven terms, proposed sizes, hard-scatter parents not read (H3; version 2) | 159 | 237 / 260 / 282 | 4; 2 / 1 / 1 | 6; 3 / 2 / 1 |
| **DRAFT: seven terms, proposed sizes, + `pilot.c0.hs` (2×10⁶) as one term (H1)** | **161** | **238 / 262 / 284** | **4; 2 / 1 / 1** | **6; 3 / 2 / 1** (35; 16 / 10 / 4 in the hard-scatter sample) |
| the same, hard-scatter sample as seven weight classes | 185 | 262 / 286 / **307** | 3; 1 / 1 / 0 | 5; 2 / 1 / 0 |
| H2: the 2×10⁵ sample of version 2 as one term | 196 | 273 / 297 / **319** | 3; 1 / 1 / 0 | 4–5; 2 / 1 / 0 |
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

Plainly. With 10⁶ events per sample, as the strategy sized the pilot, the study would pause on no information. With
the proposed sizes, at R09 the rule tells "empty" (161) from "a handful" (4 Z(νν) counts, or 6 in a B1 sample). At
R08 it pauses on 1–3 counts in any sample, and at the upper pile-up estimate on one count anywhere. Every stricter
option of D2 and D4 pauses on an empty pilot at the upper R08 estimate. A pilot that could not pause at R08 on one
count needs about twice these samples (+ 43 CPU-h for B1, + 103 CPU-h for Z(νν)).

### 3.2 The number of terms (decision D1) [4], [5]

*What the strategy's convention says.* STR l.1563 (table of §4.11 point 1): a counted factor has "λ ≥ 0, the expected
simulated count … m ~ Pois(λ), m passing events out of M … λ drawn from Gamma(m + 1)": one such factor per term of
the likelihood. STR l.1564: "one λ per weight class of constant weight w_s". STR l.1575-1578: "*One zero per term.* If
the route of a term contains more than one counted factor with m = 0, only the first in the order of the cuts keeps
its Gamma constraint; the later ones enter at 1" — this limits the zeros inside one term's route, not across terms.
STR l.726-727: the terms of B1 are "decays in flight (DIF) and nuclear interactions at r = 22, 30 and 61.5 mm (NI)":
one term, one sample, one closure test per radius. STR l.2733-2734: rule 1 reads "decays in flight and each
nuclear-interaction radius … on their own pilot samples". So in the frozen design a term is a population with its
own N_t, its own sample, its own Gamma(m + 1), its own ceiling test and its own closure test, and an empty term
contributes N_t/M × Exp(1) to the reading whatever the other terms hold.

*What follows.* The empty-pilot reading grows with the number of terms on the same events. This is the one-zero-per-term
convention, not information about the background:

| B1 terms | empty pilot R09 (hard-scatter parents not read; with H1) | likelihood | closure family K; re-test level | ceiling family T_c; α_c | false FAIL removes a selection | 4a cost |
|---|---|---|---|---|---|---|
| **seven (draft)** | 159; 161 | seven counted B1 factors per candidate, each with its test | 13; 0.0038 | 22; 0.00227 | 7.0–9.9 % | + 41 CPU-h (three closure designs, to be written) |
| four, others left out (lenient) | 85; 89 | as frozen; 2.4×10⁸ of 3.7×10⁸ vertices in no term | 10; 0.0050 | 19; 0.00263 | 6.9–8.9 % (frozen) | 0 |
| three (decays; three radii; other interactions) | 96; 99 | three factors; each sample a natural mixture of its classes | 9; 0.0056 | 18; 0.00278 | 6.9–8.6 % | not costed: B1-a redesigned |
| one | 62; 65 | one factor for all of B1 | 7; 0.0071 | 16; 0.00313 | 6.7–7.9 % | not costed: B1-a redesigned |

*The draft is seven*, because it extends the frozen term list without bending the convention: the frozen rule
already had one allowance per NI radius, and the three new classes have no v1 count and no test, which is exactly
what a term with its own ceiling is for. It also keeps the option of dropping DIF-C if the bound of B1-e is written.
*Four* is cheaper only because it leaves two thirds of the vertices out on no evidence. *Three or one* are honest
alternatives: a count in a natural mixture is an unbiased estimate whatever the mixture, and fewer terms cost fewer
allowances. Their price: the frozen closure designs cannot be kept (DIF is tested at R06–R07 on enriched overlays,
the radii at R05 by the rung split, STR l.1045-1059; a merged term needs one new design, and B1-a was frozen at
Gate A); a count in a rare class is read at the merged transfer factor (one NI 22 mm count would read 21.6 events
instead of 4.8, one DIF count 21.6 instead of 25.9); and a class cannot be dropped later on its own bound. This
draft does not choose them and does not hide them.

*The same question for the hard-scatter sample.* Read literally, STR l.1564 makes `pilot.c0.hs` a second weight
class of each of the seven terms: seven more zeros, 185 instead of 161. The draft reads it as one term, because the
sample is one natural mixture and splitting it adds allowances and no information; this is 24 events more lenient
than the literal reading, and it is put to the user as D2 rather than assumed. In the likelihood of 4a the question
does not arise (P3–P5, last point).

### 3.3 Wording of rule 1 and Df-11 where numbers or samples appear; superseded lines

The definition of the rule is unchanged: every term from the samples that exist at day 15, max(zero-count floor,
N_t·H), H = Gamma(m + 1)/M on own hits before CKF, no pool floor, one Z(νν) count for all SM processes and the
multijets, limit 300, at least 10⁵ draws for the binding median, a tie pauses (STR l.2730-2757, l.2949).

Replacement for the sentences that name samples and numbers (STR l.2733-2737, l.2755-2756, l.2949): "Each B1 class
of addendum 1 (DIF, DIF-C, NI 22, 30, 61.5 mm, NI-X, NI-C) is read on its own pilot sample at N_t/M with the
minimum-bias N_t and the M of the addendum's table, m being the number of (event, road orientation) passes over 21
orientations. The hard-scatter share of the seven classes is read as one term on `pilot.c0.hs`. Every SM
hard-scatter process and the multijets are read at the H per full-weight event of the Z(νν) pilot (M = Σw/w_max;
1.011×10⁶ with v1's weights, replaced by the day-12 MET model), with a second term for the low-weight class.
`pilot.c0.lowpt` enters only with a count." The sentences "≈ 12 Z(νν) pilot counts" and "between 3 and 4
decays-in-flight counts" become the crossings of §3.1.

Superseded where they stand in STR (the text is not edited; these numbers are replaced by this addendum):
§0 l.44-48, l.52, l.79-80, l.95-101; §4.0 l.407-411, the battery rows l.421-424, l.472; §4.4 l.726-727 (term list),
l.744 (truncation), l.797, l.811-813, l.866-871 (pilot sizes), l.876-878, l.881-886 (rates), l.902-916 (Table 4.4a),
l.935-943, l.955, l.968-976 and l.984 (rows of Table 4.4c built on the frozen floors and on a 1.1×10⁷ pool), l.1027,
l.1091; §4.7 l.1308-1313; §4.12 l.1813; §4.17 l.2104 (sample 11), l.2111-2114 (samples 17, 18, 18a, 18b), l.2115
(sample 19); §8 l.2345-2348; §11.2 l.2514, l.2517 (pilot lines); §11.7 l.2733-2737, l.2755-2756, l.2763 ("12.6 to
10.2": recomputed at day 15 from the new floors); §12.1 l.2810-2816, l.2819, l.2823, l.2826-2832, l.2838-2839,
l.2854-2862, l.2875-2880, l.2888-2889, l.2940 (Df-2: K, 19), l.2949, the floors of the Q3 annex l.2958-2962.

### 3.4 Table 4.4a at the approved CPU [9]

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
| low-weight (0.05) class of each process, one zero each (5.1 % of its row; review C-10) | + 8.6 | + 7.1 | + 6.3 | + 4.8 |
| B1, seven classes, one shared Geant4 pass (review B-5) | 23.0 (4.5 for each of DIF, DIF-C, NI-X, NI-C; 1.6 for each radius) | | | |
| B1, four terms (lenient) | 5.8 | | | |
| **all pool terms, seven classes** | **201** | 168 | 152 | **121** |
| all pool terms, four terms, low-weight classes not counted (as in version 2) | 175 | 144 | 128 | 99 |

- Frozen: 12.6 (SM 8.6). Of the SM factor, ×4.5 comes from the unit costs and ×4.3 from the weights.
- B-5: version 2 charged each large class its own Geant4 pass (B1 sum 43.1). One 'all' pass gives the vertices of
  every class at 0.904 ms per firing including the chain for each vertex; the best split puts 86 % of the 208 CPU-h
  on it (7.2×10⁸ firings) and the rest on the three-radii pass: 23.0. The split is flat: with a tenth of the
  three-radii firings the sum is 29.6.
- The lower columns need (i) forced top decays, run through the chain for tt̄ 1ℓ only [V]; tW, tt̄ 2ℓ and t-channel
  need their own forcing and a two-line change per sample of `s4pu.py` at the code freeze; (ii) the frozen v2
  preselection applied before the chain in the 4a generation job. What (ii) gives up: an event failing the nominal
  preselection is not available under a varied MET model, so the MET-model nuisance on H rests on B4-e alone for
  such events, and the pool cannot be re-used if the preselection changes after the freeze. The tables of the
  pre-registration carry the "as timed" column until each measure is demonstrated.
- CPU needed for an SM allowance of 39: 1,094 (both) to 1,984 (as timed) CPU-h; of 8.6: 4,960 to 8,996.
- Rule 3 (a) of §11.7 ("12.6 to 10.2") is recomputed at day 15 from these values.

### 3.5 Reach with every ceiling empty [10]

The strategy's own functions, v1 placeholder efficiencies; the frozen row reproduces as 790 [712]. Median [84 % edge]:
**514 [445] GeV as timed and 584 [514] with both measures** (seven classes, shared Geant4 pass, low-weight classes
counted; predictive B₁₆ / B₅₀ / B₈₄ = 132 / 177 / 235 and 85 / 110 / 143 events); four-term variant 522 [451] and 597
[524]. With version 2's B1 costing the same computation gives version 2's 506 [442] and 565 [503]. At an R08-like
selection with every ceiling empty the result itself holds B₅₀ = 275 (as timed) or 208 (both) against the class limit
of 300 (113 at Gate A): R08 candidates have little room in the result, not only in rule 1. The expected outcome of
the strategy (STR l.66-74) does not depend on these floors.

### 3.6 The (α1), (γ) and Q2 (c) numbers on the new basis [12]

These are what the user reads at day 15 when choosing between Q2 (b) and (c) (STR l.2829-2832, l.2854-2862,
l.2875-2880). Computed like the strategy's v9 table (2×10⁴ draws, R09 pile-up estimate, a factor precise to ≈ 3 %),
on the draft reading. ESTIMATE, v1 placeholder inputs.

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

## 4. Budget, calendar, storage [E from V unit costs; 8, 11]

- **Pilot:** minimum bias 10.0; Geant4 16.4 (1.23×10⁸ firings of all species at 0.305 ms, 4.6×10⁸ of the r < 70 mm
  pass at 0.047 ms); chain for 1.7×10⁷ B1 events 22.4; Z(νν) 81.1; hard-scatter sample 4.1; low-p_T check 0.5:
  **134.5 CPU-h against 54.5 budgeted** (overrun 80, reported under brief D6). Storage 156 GB against 52.
- **Order and calendar.** Z(νν) and `pilot.mb` (91 CPU-h; 30 h on 3 slots, 46 h on 2) are untouched by the findings
  and start first. The B1 part (43 CPU-h; 14 h on 3 slots, 22 h on 2) follows the A-1 re-validation and one
  validated job per stream; `pilot.c0.hs` needs the hadron list of the Z(νν) events. Day 5 is 2026-11-21: the whole
  pilot is 45 h on 3 slots and 67 h on 2, so on 2 slots there is no margin.
- **Families (finding B-3).** With seven B1 terms the eligibility family of STR l.407-408 has **K = 13** (B1-a for
  seven terms; B4-c for four; B2-a; B2-b): the INVESTIGATE and re-test level 0.05/K is 0.0038 instead of 0.0050. The
  ceiling family has **T_c = 22**, α_c = 0.05/22 = 0.00227. For an analysis that performs as declared, at least one
  closure FAIL has probability 5.1–12.0 % (5.1–10.2 % frozen), a false FAIL of either family removes a selection
  with **7.0–9.9 %** (6.9–8.9 % frozen) [5]. These replace the numbers of STR l.407-411, l.421-424, l.472, l.811-813,
  l.1813, l.2345-2348 (PR-1 content) and Df-2 (l.2940), and COM l.23-25, B1-f, T2-a, PR-1, VC-3.
- **Closure designs for DIF-C, NI-X, NI-C** (B1-a): 1,000 unbiased test overlays each (3 × 7 CPU-h), their paired
  pile-up-only pass (≈ 10), derivation overlays (≈ 10): **≈ + 41 CPU-h in 4a**. They are named here and written in
  the pre-registration. No v1 count exists for these classes, so whether a test rung is evaluable is unknown; NOT
  TESTED is covered by Q3 with a new annex row each. Three more auxiliary channels in T1 (more with weight classes).
- **Other lines on the 45 ms guess:** multijet loose population 12.5 → ≈ 28 CPU-h; B6-c 25 → ≈ 71 CPU-h.
- **Projection.** Approved 4,609, threshold 5,992: unchanged as approved figures. Projected total with the changes
  above (+ 182 CPU-h): 4,787 at the 31-parameter toy cost; **7,710 at the measured 60-parameter cost, 9,604 and
  18,246 at 80 and 100 parameters (indications): above 5,992.** By ST-1 (COM l.257) the study stops and asks unless
  the toy cost comes down. Another executor measured a jax backend at 84 / 432 / 857 / 1,898 s per 1000 + 1000 toys at
  31 / 60 / 80 / 100 parameters [U: `executor_viktor_2026-11-16_13-57.md`, campaign p2-c-toy-jax; not reviewed]; if
  that holds the projection is 4,729 at 60 and 5,141 at 100 parameters. COM T1-i is not changed here.

## 5. What does not change, and what does

Unchanged: the 16 T2 candidates and the selection rule; Q1–Q5; Df-1, Df-3 to Df-10; the definition of rule 1 (Df-11)
and its limit of 300; the stop rules; the approved CPU and calendar; the pool allocation rule; brief D7; the
blinding (no signal quantity is used or shown here).
Changed if this addendum is approved: the B1 term list (4 → 7); K (10 → 13), T_c (19 → 22) and α_c in Df-2, the
header of COM, B1-f, T2-a, PR-1, VC-3; the closure tests of B1-a; the Q3 annex; inventory rows 11, 17 and 19; the
number of T1 auxiliary channels; N_t of every B1 term; the parent truncation of the hand-over (time for parents
that have turned); M of the pilot and of the pool (effective events); Table 4.4a and every number derived from it
(list in §3.3); the Q2 (c) numbers (§3.6).

## 6. Open points and limitations, with the resolving power of each test named

1. **Not read by rule 1 in this draft:** parents of 0.3–0.5 GeV (N_t 2.6–5.2×10⁸ [E]; alarm sample at 1,300–2,600
   events per count); parents at 1 < |η| < 1.5 (N_t ≈ 1.9×10⁸ [E]; no sample); hard-scatter hadrons outside
   the road (1.8×10⁸ vertices [E]; alarm through the minimum-bias orientations). Consequence if any of them makes
   candidates at a rate per vertex comparable to the pool's: the B1 terms are under-read by a factor up to about 2,
   and neither rule 1 nor the 4a pool as defined would see it. D4 and D2 give the cost of reading them.
2. Whether vertices outside the three radii, or after a turn, can make candidates needs the finder's frozen cuts
   (channel (i)). Until then every class is a term.
3. Tests named as safety nets: B1-g (Phase 3, 1,000 pile-up events with all secondaries) reads one count as
   N_trig/1,000 = 4.1×10⁴ events at R04–R07: it finds a gross omission at loose rungs and bounds nothing at the scale
   of 300. Tabulating H against parent p_T, η and road offset: an edge bin holding a fraction f of a sample reads
   (events per count)/f, hundreds of events per count for f ≈ 0.1: an alarm, not a bound.
4. Preselection weights under the v2 MET model (day 12); costs and weights of the eleven untimed SM processes.
5. Products with β < 0.1 at the slab exit (0.07–0.12 per NI event) are not handed over; a Geant4 hit of such a
   product in the next layer is not simulated. Fatras drops particles that reach its step limit; the loss of
   conversion legs is not quantified, and whether v1 had it is unverified.
6. The hard-scatter share of N_t (factor 1.022) and the vertex yield of hard-scatter parents are planning values
   until `pilot.c0.hs` exists; the first direct parent count gives 1.3 %.
7. v1's generator cut p̂_T > 150 GeV is not fully efficient for MET > 200 GeV (1.7 % of kept Z(νν) events within
   10 GeV of the cut [V: p2-c-prof]). The split of the chain's 17.5 ms dump stage is not resolved.
8. The A-1 re-validation (P6) and the validation of the B1 production code (P7) are pending.
