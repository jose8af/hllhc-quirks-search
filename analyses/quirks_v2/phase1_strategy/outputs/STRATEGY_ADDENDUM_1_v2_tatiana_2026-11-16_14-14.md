# Strategy addendum 1, version 2 (DRAFT, pending re-review and user approval)

Author and fixer: Tatiana, 2026-11-16 14:14. Replaces `STRATEGY_ADDENDUM_1_tatiana_2026-11-16_13-31.md` (kept unchanged)
after the critical review `review/critical/ADDENDUM_1_CRITICAL_REVIEW_ulrich_2026-11-16_13-51.md` (ITERATE, 3 A, 10 B);
finding-by-finding record in `FIX_REPORT_addendum1_tatiana.md`. `STR` = `STRATEGY_oscar_2026-11-16_10-41.md` (**not
edited**), `COM` = `COMMITMENTS.md`. Tags: [V] measured in Phase 2, campaign name given (data in
`/nfs/cajuela/jdochoa/quirks_v2/data/p2c/<campaign>/`, logs in `/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/<campaign>/`);
[E] printed by `phase2_exploration/src/p2c_addendum1.py` (version 2; output `p2-c-addendum1v2/000/p2-c-addendum1v2-0.json`),
which runs a byte-identical copy of the Phase-1 budget script (sha256 548b5ba8…) with named overrides and reads the
vertex partition from `phase2_exploration/outputs/partition_p2-c-part-0.json`. No pilot campaign is submitted.

**What the user must see first.**
1. Counted on everything Geant4 produces from the parents of the v1 rate phase space, the single-interaction
   normalisation is **3.7×10⁸ vertices in 3 ab⁻¹, not the 6.8×10⁷ of Table 4.4a** [E from V counts]: half of the
   decays and a third of the nuclear interactions come from parents that have curled back, and 87 % of the first-arc
   interactions are outside the three radii of the strategy. Nothing in Phase 2 shows that any of these classes cannot
   make candidates. This version therefore reads every class in rule 1.
2. With 10⁶ events per sample, as the strategy sized the pilot, **an empty pilot would read B₅₀ = 387 at an R09
   candidate and 465–513 at R08: the study would pause on no information.** That is a property of the sample sizes,
   not of the background. With the sizes proposed here (17×10⁶ B1 events, +21 CPU-h) an empty pilot reads 159 (R09)
   and 237–283 (R08), and one count in any large sample is 24–41 events.
3. At an R08 candidate even the proposed pilot leaves little room: one or two counts in any sample pause the study.
4. The pool at the approved CPU has a summed zero-count floor of **175–213 events as timed, 99–137 with two cost
   measures of which one is not yet run through the chain**, against 12.6 at Gate A. The upside reach ("every ceiling
   empty") falls from 790 [712] GeV to 506–597 [443–524] GeV [E, v1 placeholder efficiencies].
5. With the measured toy scaling the projected total is ≈ 7,660 CPU-h at 60 parameters, above the stop-and-ask
   threshold of 5,992, unless one of the remedies now being tested by a separate executor works.

## 1. Why: Phase-2 measurements ("Phase 1 assumed / Phase 2 found / Implications")

1. **Unit costs.** Assumed 45 ms per no-pile-up hard-scatter event (STR l.356). Found 127 / 171 / 571 ms for Z(νν) /
   W(τν) / tt̄ 1ℓ per generated event [V: p2-c-t-hs0], and 327 ms for tt̄ with forced W decays through the chain
   [V: p2-c-t-ttf, 2 × 1,250 events]. Implications: §3.3, §4.
2. **Preselection.** Assumed pilot and pool events are preselected events. Found: the generator gives events passing
   truth MET > 200 GeV; v1's preselection weights them: mean 0.4308 ± 0.0049 / 0.2604 ± 0.0043 / 0.1180 ± 0.0031; two
   weight classes (≈ 0.98 and ≈ 0.05) with 4,397 + 25, 2,633 + 516, 1,159 + 946 events in 10⁴, the rest at zero
   [V: p2-c-t-hs0; reviewer's `w.py`]. Implications: M is Σw/w_max of the full-weight class (0.4396, 0.2657, 0.1205 of
   the generated events); a count in the 0.05 class is its own term (§2 P1). **"41 events per Z(νν) count" is
   provisional: it uses v1's preselection and is recomputed with the v2 MET model at day 12** from the generator-level
   summary stored with every pilot event; its statistical error is ± 1 %.
3. **Geant4 vertices: the complete partition** (§2 P2–P5). Assumed: the v1 rates (straight-line decays at 30–1000 mm,
   NI at three radii × 0.22). Found [V: p2-c-part-0, 1.5×10⁶ firings of every pool species through the whole tracker;
   classes of `p2c_g4vtx.classify`]: 245,945 vertices, each in exactly one class, table in §2.
4. **Hand-over.** Assumed Fatras takes every Geant4 product at the vertex. Found it cannot [V: p2-c-val-b1]; the
   proposed variant is validated (§2 P6). The running Fatras instance does not decay or absorb hadrons: of 40,000
   K±, π±, p each (1–2 GeV, |η| < 0.3) 99.96 %, 99.98 %, 99.96 % reach the outermost barrel layer, proton minus kaon
   = −0.00003 ± 0.0007 against 0.09 if kaons decayed; no hit of a later generation [V: p2-c-part-fatras]. B1-d's
   physics statement is now verified on the instance, not only on the configuration class.
5. **Toys.** Assumed "may double" (STR l.1720-1722). Found 638 s per 1000 + 1000 toys at 31 parameters (200 toys),
   5.3–5.8 s per toy at 60 parameters (120 toys; ×17), 8.9 s and 24.3 s at 80 and 100 parameters (12 toys each:
   indications) [V: p2-c-t-pyhf]; nothing measured between 31 and 60. Implications: §4.
6. **Fatras step limit (all samples, not caused by this addendum).** 0.03–0.07 particles per hard-scatter event,
   mostly conversion positrons, fail with "maximum number of steps" and are dropped with all their hits
   [V: logs of p2-c-t-hs0, p2-c-t-ttf]. Unquantified loss of conversion legs; listed in §6.

## 2. Proposed definitions

**P1 Z(νν) pilot: 2.3×10⁶ generated events** (STR l.869). m_Z counts events of the full-weight class; M = Σw/w_max =
1.011×10⁶; one count = 41.2 events for all SM processes and the multijets (24.8 for Z(νν) alone); an event of the
0.05 class is counted in a second term at 2.1 events per count. Other sizes [E]: 0.83×10⁶ (29 CPU-h) 114; 1.5×10⁶
(53 CPU-h) 63; 3.5×10⁶ (123 CPU-h) 27; 5.23×10⁶ (184 CPU-h) 18.1 per count.

**P2 Parents.** Every π±, K±, p, K⁰_L, n, γ produced within 1 mm of the interaction point with 0.5 < pT < 20 GeV and
|η| < 1, natural Pythia mixture; 7.13 per minimum-bias interaction, 0.3405 inside a road of half-width 0.15
[V: p2-c-part-0]. N_t of every class is computed from **this** pool (not from v1's parent count, which is 5 % smaller):
N_t = N_trig × 200 × 0.3405 × (vertices of the class per firing) × 1.022, the last factor being the hard-scatter
share of the parents [E: v1 rates 1.5945/1.560, STR l.255]. The hard-scatter parents themselves are stiffer than the
sampled ones: a sample `pilot.c0.hs` (2×10⁵ vertices from the in-road hadrons of 2×10⁴ generated Z(νν) events, each
fired repeatedly; ≈ 1 CPU-h; by day 5 with the pilot) is read in rule 1 as part of each class with its own weight
(share 2.2 % of N_t; one count ≈ 40 events [E]). Lower pT edge: a 0.4 GeV parent still crosses the inner layers and
the three TBPS layers on its first arc, so the edge at 0.5 GeV is a convenience of v1's rate definition, not a bound;
a check sample `pilot.c0.lowpt` (0.3 < pT < 0.5 GeV, 2×10⁵ vertices, ≈ 0.5 CPU-h) is generated with the pilot and its
N_t taken from the 10⁷-interaction generator-level sample; it is read in rule 1 if it has any own-hit count at R05 or
deeper. |η| < 1 and the road are physics (barrel road of the finder); they are not tested outside (§6).

**P3–P5 The partition and the terms** [V counts: p2-c-part-0; N_t and events per count: E]. "First arc": transverse
path from the origin ≤ πR. Conversions of primary photons (52,583) are not B1 (STR §2 route table); 49 vertices of
other processes (stopped protons, 3 photons) are below 0.02 % and are recorded with class "other".

| class (vertices in 1.5×10⁶ firings; by parent π± / K± / p / K⁰_L / n / γ) | term of rule 1 | pilot sample, stream | N_t | M proposed | events per count |
|---|---|---|---|---|---|
| decays of π±, K± on the first arc, any radius (53,063: 26,641 π±, 26,422 K±) and K⁰_L decays (2,906) | **DIF** | `pilot.c0.dif` | 1.06×10⁸ | 4×10⁶ | 26.5 |
| decays of π±, K± after the first turn (51,441: 35,970 π±, 15,471 K±) | **DIF-C** (new) | `pilot.c0.difc` | 9.75×10⁷ | 4×10⁶ | 24.4 |
| inelastic, first arc, beam pipe (2,583: 1,798 / 246 / 215 / 112 / 206 / 6) | **NI 22 mm** | `pilot.c0.ni22` | 4.90×10⁶ | 10⁶ | 4.9 |
| inelastic, first arc, TBPX L1 (3,502) | **NI 30 mm** | `pilot.c0.ni30` | 6.64×10⁶ | 10⁶ | 6.6 |
| inelastic, first arc, TBPX L2 (3,496) | **NI 61.5 mm** | `pilot.c0.ni61` | 6.63×10⁶ | 10⁶ | 6.6 |
| inelastic, first arc, every other layer (50,083: 35,874 / 5,035 / 3,469 / 2,489 / 3,083 / 133) | **NI-X** (new) | `pilot.c0.nix` | 9.49×10⁷ | 4×10⁶ | 23.7 |
| inelastic after the first turn, any layer (26,239: 24,271 π±, 1,185 K±, 783 p) | **NI-C** (new) | `pilot.c0.nic` | 4.97×10⁷ | 2×10⁶ | 24.9 |
| **sum of the B1 classes: 190,730** (+ 52,583 conversions + 49 other = 245,945 = all vertices) | | | **3.66×10⁸** | 1.7×10⁷ | |

For comparison, first-arc π/K decays inside v1's radial range 30–1000 mm are 43,011, i.e. N_t = 8.15×10⁷ against the
frozen 6.51×10⁷ (×1.25: pool +5 %, Geant4 yield ×1.19); the frozen NI rates × (1/0.22) are 4.0 / 5.1 / 5.1×10⁶
against 4.9 / 6.6 / 6.6×10⁶ here (charged parents +5 %, Geant4 yield +3–8 %, neutral parents +14 %).

*A1, corrected.* Two statements of version 1 were wrong: 53 % of the later decays come from parents above 0.57 GeV
(they turn inside the 1,200 mm Geant4 world and lose energy), and the sagitta of a 0.5 m circle is 1.4–3.4 mm over
the inner layers, below the ribbon widths, 19–39 mm over three outer layers and 277 mm over the barrel: not "two
orders of magnitude" above. No written bound (COM B1-e) exists yet that excludes these decays for the number of
layers a rung requires, so they are **not excluded**: DIF-C is a term, sized like DIF. If the bound of B1-e is written
and checked before the freeze, the pre-registration may drop the term; rule 1 at day 15 reads it.
*A2.* Interactions of parents that have turned (NI-C) are a term; every sample is drawn from all six species
(the 'all' Geant4 pass); K⁰_L decays are in DIF. *P4 (the factor 0.22)* is removed as in version 1: a Geant4 vertex
is on its parent's path, and the fraction on the plane-hypothesis line is part of H. This raises the NI terms.
*Rejected alternatives and their readings* are the "lenient" rows of §3.1 (only DIF and the three radii read):
lower readings bought by leaving 2.4×10⁸ of the 3.7×10⁸ vertices out of rule 1 on no evidence.

**P6 Hand-over (validated as proposed).** Products are followed by Geant4 to the exit of the slab of their vertex;
products with β < 0.1 there are not handed to Fatras; Fatras parent with v1's Truncate; the Geant4 crossings of the
parent are stored. Validation on 1,000 events of each of the eight streams [V: p2-c-b1y, p2-c-b1yv]: every hard
check passes (V4-1 closure, no parent hit beyond the vertex radius, **no product hit before its production time**,
no NaN, distinct seeds); 0 products with β < 0.1 handed over; 2 Fatras step-limit errors in 8,000 events; products
handed over per vertex 1.2 (DIF), 1.1 (DIF-C), 2.5 (K⁰_L), 2.9–3.3 (NI), 3.2 (NI-X), 2.2 (NI-C). Size of what the
β cut removes: 0.07–0.12 products per NI event [V: p2-c-val-b1x]; whether Geant4 would give them a hit in the next
layer is not simulated (§6). Fatras parent against Geant4 parent: median 0.5–0.9 mm, 4–8 mm at 90 % for DIF, DIF-C,
NI-X, NI-C; 5–8 µm at the inner radii.

**P7.** One vertex per event; road and PV stored, not fixed at generation; streams as in the table plus `pilot.mb`,
`pilot.g4`, `pilot.hs0.znn`, `pilot.c0.hs`, `pilot.c0.lowpt`.

## 3. Replacement tables [E]

**3.1 Rule 1: empty-pilot reading and crossings.** B₅₀ with every count zero (10⁵ draws) and the first count at
which B₅₀ > 300 with the others at zero (2×10⁴ draws). R08 over the strategy's pile-up range 88 / 118 / 148 events
(STR l.2819). The R08 numbers of the frozen case (181; 7; 2) are computed here; STR prints only the R09 table.

| reading | B₅₀ empty pilot, R09 | R08 at pile-up 88 / 118 / 148 | crossing m_Z: R09; R08 | crossing, each of DIF, DIF-C, NI-X, NI-C: R09; R08 |
|---|---|---|---|---|
| STR as frozen (4 B1 terms, v1 N_t, 18.1 per Z count) | 76 | — / 181 / — | 13; 7 | DIF 4; 2 |
| **all classes read, 10⁶ per sample** | **387** | **465 / 490 / 513** | 0; 0 | 0; 0 — pauses when empty |
| **all classes read, proposed sizes (S2)** | **159** | **237 / 261 / 283** | 4; 2 / 1 / 1 | 6; 3 / 2 / 1 |
| S2 with the Z(νν) pilot at 3.5×10⁶ generated | 146 | 223 / 247 / 268 | 6; 3 / 2 / 2 | 6–7; 3–4 / 3 / 2 |
| S2 with the Z(νν) pilot at 5.23×10⁶ generated | 137 | 214 / 238 / 259 | 9; 5 / 4 / 3 | 7; 4 / 3 / 2 |
| lenient (only DIF and three radii read), 10⁶ per sample | 146 | 227 / 253 / 276 | 4; 2 / 2 / 1 | DIF 2; 1 |
| lenient, S2 sizes | 85 | 164 / 188 / 210 | 6; 4 / 3 / 3 | DIF 9; 6 / 5 / 4 |

Plainly: at R09 the proposed pilot can tell "empty" (159) from "a handful of counts" (pause at 4 Z(νν) counts or 6
counts in a B1 sample). At R08 it pauses on 1–3 counts in any sample; at the upper pile-up estimate one count
anywhere pauses. A pilot that could not pause at R08 on one count would need about twice these samples again
(+ ≈ 45 CPU-h for B1, + 100 CPU-h for Z(νν)); the user may prefer to accept the R08 behaviour.

**3.2 Wording of rule 1 and Df-11 where numbers or samples appear** (STR l.2733-2737, l.2755-2756, l.2949; also
superseded: §0 l.44-48, l.79-80, l.95-101; §4.4 l.797, l.870, l.876-878, l.935-943, l.968-969, l.984, l.1027; §11.7
l.2763; §12.1 l.2810-2816, l.2819, l.2823, l.2826-2828, l.2838-2839, the floors of the Q3 annex l.2958-2962; COM B4-c):
"Each B1 class of addendum 1 (DIF, DIF-C, NI 22, 30, 61.5 mm, NI-X, NI-C) is read on its own pilot sample at
N_t/M with the N_t and M of the addendum's table. Every SM hard-scatter process and the multijets are read at the H
per full-weight event of the Z(νν) pilot (M = Σw/w_max; 1.011×10⁶ with v1's weights, to be replaced by the day-12 MET
model), with a second term for the low-weight class." The sentences "≈ 12 Z(νν) pilot counts" and "between 3 and 4
decays-in-flight counts" become the crossings of §3.1. The definition of the rule (samples that exist, Gamma(m + 1),
no pool floor, ≥ 10⁵ draws for the binding median, ties pause) is unchanged.

**3.3 Table 4.4a at the approved CPU** (user decision 2026-11-16; supersedes STR l.902-916; shares 457 and 208
CPU-h; rule M_t ∝ √(N_t/c_t), G = 1; M effective = full-weight class; costs [V] for Z(νν), W(τν), tt̄ 1ℓ, the eleven
others by proxy [E]).

| SM floor at 68 % (events) | as timed | forced tt̄ (327 ms [V]) | preselection before the chain | both |
|---|---|---|---|---|
| Z(νν)+jets | 29.2 | 26.4 | 19.6 | 17.1 |
| W(τ_h) | 20.2 | 18.3 | 14.0 | 12.2 |
| W(eν) | 13.8 | 12.5 | 9.6 | 8.3 |
| tt̄ 1ℓ | 36.4 | 24.9 | 28.5 | 17.5 |
| **SM sum (14 processes)** | **169** | **138** | **123** | **93** |
| share of the tt̄-type rows (tt̄ 1ℓ, tW, tt̄ 2ℓ, t-channel) | 40 % | 33 % | 43 % | 35 % |
| B1, all seven classes at 208 CPU-h | 43.1 (DIF 9.1, DIF-C 9.0, NI 1.9 / 2.4 / 2.4, NI-X 9.7, NI-C 8.7) | | | |
| B1, lenient (four terms) | 5.8 | | | |
| **all pool terms, seven classes / lenient** | **213 / 175** | 182 / 144 | 166 / 128 | **137 / 99** |

The frozen value was 12.6 (SM 8.6). Of the SM factor, ×4.5 comes from the unit costs and ×4.3 from the weights. The
lower columns need: (i) forced tt̄ decays, run through the chain for tt̄ 1ℓ only [V]; tW, tt̄ 2ℓ and t-channel need their
own forcing, and a two-line change per sample of `s4pu.py` at the code freeze; (ii) the frozen v2 preselection
applied before the chain in the generation job (possible for the 4a pool only; an event that fails the nominal
preselection is then not available for a varied MET model). I propose both, and that the tables of the
pre-registration carry the "as timed" column until each is demonstrated. CPU needed to restore an SM floor of 39:
≈ 1,090 (both) to 1,980 (as timed) CPU-h; of 8.6: 4,960 to 9,000 CPU-h.

**Reach with every ceiling empty, R09-like selection** [E: the strategy's own functions, v1 placeholder
efficiencies; the frozen row reproduces as 790 [712]]: median [84 % edge] 597 [524] GeV (both measures, lenient),
565 [503] (both, seven classes), 522 [451] (as timed, lenient), 506 [443] (as timed, seven classes). The expected
outcome of the strategy (pause at day 15 on a background of ≈ 10⁴ events, STR l.66-74) is not changed by the floors.

## 4. Budget, calendar, storage [E from V unit costs]

- **Pilot, proposed sizes:** minimum bias 10.0; Geant4 16.2 (1.2×10⁸ firings of all species at 0.305 ms; 4.6×10⁸ of
  the r < 70 mm pass at 0.047 ms); chain for 1.7×10⁷ B1 events 22.4; Z(νν) 81.1; the two small samples ≈ 1.5:
  **≈ 131 CPU-h against 54.5 budgeted** (overrun 77, reported under brief D6); with 10⁶ per sample 113. Storage ≈ 144
  GB against 52; study total ≈ 560 GB (≈ 760 at the pre-merge cap of 400 GB) against the 1.5 TB soft budget.
  Wall time on 2–3 slots of schrodinger: 44–66 h.
- **If all seven classes are terms:** T_c = 22 ceiling terms instead of 19, α_c = 0.05/22 (Df-2 STR l.2940, §4.0
  l.409-411, COM B1-f l.182, VC-3 l.283); B1-a needs a closure design for DIF-C, NI-X, NI-C: 1,000 unbiased test
  overlays each (3 × 7 CPU-h), their paired pile-up-only pass (≈ 10 CPU-h), derivation overlays (≈ 10 CPU-h); three
  rows in the Q3 annex and in the inventory (sample 19); three more auxiliary channels in T1. **≈ +41 CPU-h in 4a.**
- **Other lines on the 45 ms guess:** multijet loose population 12.5 → ≈ 28 CPU-h; B6-c 25 → ≈ 71 CPU-h.
- **Projection against the approved figures.** Approved 4,609, threshold 5,992: unchanged as approved figures. Projected
  total with these changes and toys at the 31-parameter cost: ≈ 4,780 CPU-h. With the measured 60-parameter toy cost
  (×17): **≈ 7,700 CPU-h, above 5,992**: by ST-1 (COM l.257) the study stops and asks unless a remedy brings the toy
  cost back; the remedy tests (gradient backend, minuit, pruning, merged auxiliary channels; ≈ 2.5 CPU-h) are being
  run by a separate executor and COM T1-i (l.216) is not changed until they are measured.

## 5. What does not change, and what does

Unchanged: the 16 T2 candidates and the selection rule; Q1–Q5; Df-1, Df-3 to Df-10; Df-9; the definition of rule 1
(Df-11) and its limit of 300; the stop rules; the approved CPU and calendar; the pool allocation rule; brief D7.
Changed if this addendum is approved: the B1 term list (4 → 7), hence T_c and α_c in Df-2 and COM B1-f, the closure
tests of B1-a, the Q3 annex, the inventory and the number of T1 channels (§4); N_t of every B1 term; M of the pilot
and of the pool (effective events); Table 4.4a and every number derived from it (list in §3.2); COM rule 3 (a) of
§11.7 ("12.6 to 10.2") is recomputed at day 15 from the new floors.

## 6. Open points, with the resolving power of the tests named

1. Whether vertices outside the three radii, or after a turn, can make candidates: needs the finder's frozen cuts
   (channel (i)). Until then every class is a term.
2. Tests named as safety nets and what they can resolve: B1-g (Phase 3, 1,000 pile-up events with all secondaries):
   one count = N_trig/1,000 = 4.1×10⁴ events, read at R04–R07: finds a gross omission at loose rungs, bounds nothing at
   the 300-event scale. Tabulating H against parent pT, η and road offset: an edge bin holding a fraction f of a
   sample has (events per count)/f, i.e. hundreds of events per count for f ≈ 0.1; it is an alarm, not a bound, and it
   does not measure outside the phase space. `pilot.c0.lowpt` measures below 0.5 GeV directly; nothing measures
   |η| > 1 or outside the road.
3. Preselection weights under the v2 MET model (day 12); costs and weights of the eleven untimed SM processes.
4. Products with β < 0.1 at the slab exit (0.07–0.12 per NI event) are not handed over; a Geant4 hit in the next
   layer from such a product is not simulated.
5. Fatras drops particles that reach its step limit (§1.6); the loss of conversion legs is not quantified, and
   whether v1 had it is unverified.
6. v1's generator cut p̂T > 150 GeV is not fully efficient for MET > 200 GeV (1.7 % of kept Z(νν) events within
   10 GeV of the cut [V: p2-c-prof]).
7. The split of the chain's 17.5 ms dump stage is not resolved.
