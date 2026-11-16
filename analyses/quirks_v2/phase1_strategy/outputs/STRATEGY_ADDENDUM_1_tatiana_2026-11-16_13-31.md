# Strategy addendum 1 (DRAFT, pending review and user approval) — pilot definition and pool rows after the Phase-2 measurements

Author: Tatiana (Phase-2 executor, channel (iii)), 2026-11-16 13:31. `STR` =
`STRATEGY_oscar_2026-11-16_10-41.md` (version 10, **not edited**); `COM` = `COMMITMENTS.md`. Line numbers are those of
these files. Tags: [V] measured in Phase 2 (campaign under `data/p2c/` with logs under `logs/p2c/`, ledger
`ledger/markers/`); [E] estimate printed by `phase2_exploration/src/p2c_addendum1.py` (output
`data/p2c/p2-c-addendum1/000/p2-c-addendum1-0.json`), which uses a byte-identical copy of the Phase-1 budget script
(sha256 548b5ba8…) with the changed inputs as the named `OVERRIDES` of that file. No pilot campaign has been submitted.
Background: `phase2_exploration/outputs/PILOT_DECISIONS_tatiana_2026-11-16_13-22.md` and `COSTS_POOL_…_13-25.md`;
**where a number differs, this addendum supersedes them** (three do: the preselection weight, the first-arc decay
yield and the pool floors, each explained below).

## 1. Why: what Phase 2 measured

1. **Unit cost of the no-pile-up hard-scatter event.** *Phase 1 assumed* 45 ms (STR Table 4.0 l.356, a guess).
   *Phase 2 found* 127 ms for Z(νν), 171 ms for W(τν), 571 ms for tt̄ 1ℓ per generated event [V: p2-c-t-hs0, 10⁴
   events each]; 3.3 / 9.1 / 48 generator tries per kept event at 9–10 ms each [V: p2-c-prof]. *Implications:* the
   Z(νν) pilot costs 81 CPU-h, not 28.8; the pool rows of Table 4.4a change (§3).
2. **Preselection weight.** *Phase 1 assumed* that pilot and pool events are preselected events (rule 1 reads
   N_trig/M, STR l.2731-2737). *Phase 2 found* that the generator returns events passing truth MET > 200 GeV, and that
   v1's preselection gives them a mean weight of **0.4308 ± 0.0049 for Z(νν), 0.2604 ± 0.0043 for W(τν), 0.1180 ±
   0.0031 for tt̄ 1ℓ** [V: the 10,000 events per process of p2-c-t-hs0]; effective fractions N_eff/N = (Σw)²/(N Σw²)
   = 0.440, 0.268, 0.125. (The 0.397 of my memo was from 200 events, 0.397 ± 0.035.) *Implications:* M in every
   "events per count" and in every SM floor is the effective number, 0.44 × the generated number for Z(νν). The
   statistical error of 0.440 (± 0.005) moves "events per Z(νν) count" by ± 1 % (40.8–41.7). The larger uncertainty is
   that this is v1's preselection (truth MET with 25 GeV smearing): the v2 MET model is fixed at day 12 (STR §4.7), and
   the weights are recomputed then from the generator-level summary stored with every pilot event; rule 1 at day 15
   uses that value. No further measurement is needed before the pilot (cost of this one: 0, existing events).
3. **Geant4 decays.** *Phase 1 assumed* the v1 straight-line rate (STR l.881-886). *Phase 2 found*, per π/K parent of
   the rate phase space: 0.0913 decays at 30 < r < 1000 mm, of which 0.0455 on the first outward arc (transverse path
   ≤ πR) and the rest after the parent has curled back; v1's formula gives 0.0381 [V: p2-c-t-g4-y0, 5×10⁵ firings].
   (The memo's 0.0353 used a 4 ns time cut, not the arc definition.) *Implications:* §2 O12 and the DIF rate.
4. **Geant4 nuclear interactions.** *Phase 1 assumed* three radii and a factor 0.22 (STR l.726-727, l.882-885).
   *Phase 2 found* yields per π± at the three radii of 2.3 / 3.1 / 3.0×10⁻³, equal to v1's rate before the 0.22
   (2.2 / 2.8 / 2.8×10⁻³), and that on the first arc the other layers hold 5.2 times as many inelastic vertices as the
   three radii (6.6 times with curling parents) [V: p2-c-t-g4-y0]. *Implications:* §2 O3 and O4.
5. **Hand-over.** *Phase 1 assumed* Fatras can take every Geant4 product at the vertex (STR l.742-746). *Phase 2
   found* that a third of the hit-making NI products were fragments with β < 0.1 that Fatras transports unphysically
   (hits before their vertex time) [V: p2-c-val-b1]; with products followed by Geant4 to the exit of the vertex slab
   every check passes [V: p2-c-val-b1x]. *Implications:* §2 hand-over.
6. **Toys.** *Phase 1 assumed* the toy cost "may double" from 31 to 60–100 parameters (STR l.1720-1722). *Phase 2
   found* ×17 at 60, ×27 at 80 and ×75 at 100 parameters [V: p2-c-t-pyhf; 12 toys at 80 and 100]. *Implications:* §4.
7. **B1-d and the v1 rates (no change proposed).** Geant4 and ACTS geometry agree (positions identical, x/X₀ to
   4×10⁻⁷) [V: p2-c-matscan]; the v1 DIF and NI rates are reproduced (1.56 and 0.098 per event) [V: p2-c-t-g4].

## 2. Proposed definitions (the draft to be judged), with the rejected alternative and its reading

Rule-1 readings [E] are in the table of §3. "Lowers / raises" refers to events per pilot count against the frozen
numbers (65.1 per DIF count, 0.88 / 1.12 / 1.12 per NI count, 18.1 per Z(νν) count).

**P1 Pilot size (b): 2.3×10⁶ generated Z(νν) events** (as STR l.869 names them), read with the effective size
0.440 × 2.3×10⁶. *Raises* events per Z(νν) count from 18.1 to 41.2 (all SM), 24.8 for Z(νν) alone. Rejected: (a)
0.83×10⁶ generated (29 CPU-h; 114 per count, pause at 2 counts); (c) 5.2×10⁶ generated (184 CPU-h; 18.1 per count).

**P2 (O1) Population of the unbiased DIF and NI events: the v1 rate phase space with the natural Pythia spectrum**
(parents produced within 1 mm of the interaction point, 0.5 < pT < 20 GeV, |η| < 1, π±, K±, p, K⁰_L, n, γ at their
natural proportion; DIF from π±, K± below 10 GeV; road assigned afterwards within ± 0.15). This is the population on
which N_t of Table 4.4a is defined, so it neither lowers nor raises the frozen 65.1. Rejected: every particle Fatras
accepts; its N_t was not measured, and removing the road cut alone gives ≥ 1,364 per DIF count. *Physics argument:*
a parent outside |η| < 1 or the road cannot put two own hits per layer inside a ribbon in the barrel road; a parent
below 0.5 GeV has 2R < 0.88 m and cannot cross the outer barrel layers on its first arc. *What would falsify it:* own-hit
near-pass events from parents at the edges of the phase space. *Test that catches it:* the pilot records pT, η and
the road offset of every parent, so H is tabulated against them in Phase 3; a non-zero H in the lowest pT bin
(0.5–0.7 GeV), the outermost |η| bin (0.9–1.0) or the outermost road bin is the trigger to widen the population before
the freeze. In 4a, B1-g (pile-up events with the Geant4 secondaries of **all** particles, COM l.178) counts
secondary-induced candidates with no phase-space restriction and is compared with the B1 prediction.

**P3 (O12) DIF term = decays on the first outward arc** (transverse path from the origin ≤ πR, 30 < r < 1000 mm),
with **N_t recomputed with the measured Geant4 first-arc yield: N_t = N_trig × 1.59 × 1.19 = 7.77×10⁷**, which *raises*
65.1 to 77.7 per count. The decays after the first turn (as many again, ×2.01 in total) form a separate sample of
2.5×10⁵ pilot events. Rejected: every Geant4 decay in one term (156 per count; pause at 1 count). *Physics argument:*
a parent that has turned has pT < 0.57 GeV; its hits and its muon's lie on a circle of radius < 0.5 m, whose sagitta
over any three counting layers exceeds every ribbon width of the ladder (4.7–9.4 mm, STR l.853) by two orders of
magnitude: this is the analytic bound of STR pt 5. *What would falsify it:* any own-hit pass or near-pass at R05 or
deeper in the curler sample. *Test:* the curler sample is classified in Phase 3 with the same code; if H(R05) > 0
there, the curler decays become part of the DIF term (N_t × 2.01) before the freeze; B1-e's check of the bound
(COM l.176) is this test, and B1-g in 4a counts curler decays among all secondaries.

**P4 (O3) NI rates without the factor 0.22:** N_t = N_trig × (0.098, 0.124, 0.124) = 4.0 / 5.1 / 5.1×10⁶; *raises* the
events per NI count to 4.0 / 5.1 / 5.1. Rejected: keeping 0.22 (0.88 / 1.12 / 1.12). The NI samples come from a Geant4
pass that stops the parent at r = 70 mm, so they are first-arc vertices by construction, consistent with P3.

**P5 (O4) Nuclear interactions in the other layers. STRICT version (drafted as the proposal for review):** a new
term "NI elsewhere" (first-arc inelastic vertices in TBPX L3–L4, the service cylinder, the outer barrel layers and the
discs), N_t = 5.20 × (sum of the three radii) = **7.36×10⁷**, read in rule 1 on its own pilot sample of 10⁶ events
(73.6 events per count), recorded by layer. **Lenient alternative:** the same 10⁶ events recorded and classified, but
no term unless Phase 3 finds H > 0 at R05 or deeper. Numbers of both are in §3: the strict version adds 0.69 × 73.6 =
51 events to the all-zero reading at R09 and brings an empty pilot to 295 at an R08 candidate. Cost of the sample in
either version: 1.7 CPU-h, 4 GB. I cannot show that these vertices make no candidates (§6), which is why the strict
version is the draft.

**P6 Hand-over.** Products are followed by Geant4 until they leave the slab of their vertex and are handed to Fatras
there; products with β < 0.1 at that point are followed by Geant4 to their end and not handed over (O13 (b)); the
parent is the Fatras parent with v1's Truncate, and the Geant4 crossings of the parent are stored so that the second
variant of STR l.744-746 is built from the same pilot (O7); the count of parent hits later than the vertex time is
recorded (O11). Rejected: hand-over at the vertex (fails validation); a tuned β cut. No effect on N_t.

**P7 Smaller ones.** Parents from minimum bias only in the pilot (the hard-scatter share, 1–2 % of the rate, in
Phase 3); one vertex per event; road and PV stored, not fixed at generation; seed streams `pilot.mb`, `pilot.g4`,
`pilot.c0.{dif,difc,ni22,ni30,ni61,nix}`, `pilot.hs0.znn`.

## 3. Replacement tables

**3.1 Rule-1 basis and day-15 table [E].** Supersedes the basis line of STR l.2823 and the rows of l.2810-2816 and
l.2826-2828 for the samples named in §2. "Crossing" = first count at which B₅₀ > 300 with the other counts at zero.
Pile-up: R09 EST median 6.7 (as frozen); R08 EST median 117.9, s_tot 0.43.

| reading | events per count: DIF / NI 22, 30, 61.5 / all SM / NI elsewhere | B₅₀, every count zero: R09 / R08 | crossing m_Z: R09 / R08 | crossing m_DIF: R09 / R08 | crossing m_NIx: R09 / R08 |
|---|---|---|---|---|---|
| STR as frozen | 65.1 / 0.88, 1.12, 1.12 / 18.1 / — | 76 / 181 | 13 / 7 | 4 / 2 | — |
| **proposed, strict P5** | 77.7 / 4.0, 5.1, 5.1 / 41.2 / 73.6 | **191 / 295** | **3 / 1** | **2 / 1** | **2 / 1** |
| proposed, lenient P5 | 77.7 / 4.0, 5.1, 5.1 / 41.2 / — | 120 / 225 | 5 / 2 | 3 / 2 | — |
| lenient, DIF N_t kept at v1 | 65.1 / … | 111 / 215 | 5 / 3 | 3 / 2 | — |
| lenient, 0.22 kept (rejected) | 77.7 / 0.88, 1.12, 1.12 / 41.2 | 109 / 214 | 5 / 3 | 3 / 2 | — |
| lenient, every decay in DIF (rejected) | 156 / … | 176 / 283 | 3 / 1 | 1 / 1 | — |
| lenient, pilot size (a) (rejected) | … / 114 | 181 / 286 | 2 / 1 | 2 / 1 | — |
| lenient, pilot size (c) (rejected) | … / 18.1 | 96 / 202 | 11 / 6 | 3 / 2 | — |
| strict with curling parents in NIx | … / 93.3 | 208 / 312 | 3 / 0 | 2 / 0 | 2 / 0 |

Every proposed change raises the reading; under the strict version an empty pilot reads 191 at R09 and 295 at R08.

**3.2 New wording where a number or sample appears.** §11.7 rule 1 (STR l.2733-2737): "Decays in flight (first-arc
decays, N_t = 7.77×10⁷) and each nuclear-interaction radius (N_t = 4.0, 5.1, 5.1×10⁶, without the factor 0.22) are
read on their own pilot samples (10⁶ events each); nuclear interactions elsewhere (N_t = 7.36×10⁷) on theirs (10⁶
events). Every SM hard-scatter process and the multijets are read at the H per effective event of the Z(νν) pilot
(2.3×10⁶ generated events, effective size N_eff = (Σw)²/Σw² with the preselection weights of the MET model fixed at
day 12; 1.01×10⁶ with v1's weights)." The sentence of l.2737 becomes "one Z(νν) pilot count is 41 events, one
decays-in-flight count 78, one NI-elsewhere count 74". Df-11 (l.2949): the same replacements; its statement "the limit
is at the Z(νν) pilot count that the table marks" refers to §3.1. §0 l.95-101 and §4.4 pt 5 l.876-878 ("≈ 12 Z(νν)
pilot counts", "between 3 and 4 decays-in-flight counts", "18", "65", "B₅₀ ≈ 76") are superseded by §3.1.

**3.3 Table 4.4a at the approved CPU (user decision 2026-11-16) [E].** Supersedes STR l.902-916. Hard-scatter share
457 CPU-h, B1 share 208 CPU-h, rule M_t ∝ √(N_t/c_t), G = 1. **M_t is the effective number of preselected events;
c_t is the cost per effective event** (cost per generated event divided by 0.440, 0.268 or 0.125). This is the
correction to my earlier pool table (summed floor 41.7 / 36.0), which counted generated events as if each were a
preselected event; the user's decision was taken on that table and should be re-read with this one. Costs [V] for
Z(νν), W(τν), tt̄ 1ℓ; the other W and diboson processes use W(τν)'s cost and weight, tW, tt̄ 2ℓ, t-channel use tt̄'s,
ZZ, Z(ττ), Z(ℓℓ) use Z(νν)'s [E, not measured]. Proposed column: tt̄-type samples with forced decays, and the frozen
generator-level preselection applied **before** the chain (possible for the 4a pool, whose preselection is frozen;
not for the pilot).

| term | N_t | cost per effective event (ms): as timed → proposed | M_t effective (generated): as timed → proposed | floor at 68 %: STR → as timed → proposed |
|---|---|---|---|---|
| Z(νν)+jets | 2.51×10⁷ | 289 → 181 | 9.9×10⁵ (2.25×10⁶) → 1.70×10⁶ (3.87×10⁶) | 2.60 → 28.9 → 16.8 |
| W(τ_h) | 5.41×10⁶ | 638 → 421 | 3.1×10⁵ → 5.2×10⁵ (1.93×10⁶) | 1.21 → 20.0 → 11.9 |
| W(eν) | 2.54×10⁶ | 638 → 421 | 2.1×10⁵ → 3.6×10⁵ | 0.83 → 13.7 → 8.1 |
| tt̄ 1ℓ | 2.38×10⁶ | 4,568 → 1,779 | 7.7×10⁴ → 1.67×10⁵ (1.34×10⁶) | 0.80 → 35.4 → 16.2 |
| W(τ_ℓ), W(μν) (each) | 2.2–2.3×10⁶ | 638 → 421 | 2.0×10⁵ → 3.3×10⁵ | 0.78 → 12.9 → 7.7 |
| tW; tt̄ 2ℓ; t-channel | 2.6; 2.1; 1.1×10⁵ | 4,568 → 1,779 | 2.5; 2.3; 1.7×10⁴ → 5.5; 5.0; 3.6×10⁴ | 0.26; 0.24; 0.17 → 11.7; 10.6; 7.6 → 5.4; 4.9; 3.5 |
| WZ; WW | 1.4; 1.3×10⁵ | 638 → 421 | 4.9; 4.7×10⁴ → 8.3; 7.9×10⁴ | 0.19; 0.18 → 3.2; 3.1 → 1.9; 1.8 |
| ZZ; Z(ττ); lost-lepton Z(ℓℓ) | 1.0; 4.3; 0.30×10⁵ | 289 → 181 | 6.4; 12.9; 3.4×10⁴ → 11; 22; 5.9×10⁴ | 0.17; 0.34; 0.09 → 1.9; 3.8; 1.0 → 1.1; 2.2; 0.6 |
| **SM hard scatter, sum** | | | | **8.6 → 166 → 90** |
| DIF (first arc) | 7.77×10⁷ | 12.7 | 2.11×10⁷ (strict) / 3.41×10⁷ (lenient) | 3.04 → 4.2 / 2.6 |
| NI 22 / 30 / 61.5 mm | 4.0 / 5.1 / 5.1×10⁶ | 11.2 / 13.3 / 13.3 | 5.1 / 5.3 / 5.3×10⁶ (strict) | 0.28 / 0.31 / 0.31 → 0.90 / 1.10 / 1.10 |
| NI elsewhere (strict only) | 7.36×10⁷ | 15.3 | 1.86×10⁷ | — → 4.5 |
| **DIF and NI, sum** | | | | **3.9 → 11.8 (strict) / 4.5 (lenient)** |
| **all pool terms** | | | | **12.6 → 101 (proposed, strict) / 94 (lenient)** |

Intermediate cases [E]: forced tt̄ without preselection before the chain, SM sum 134; preselection before the chain
without forced tt̄, 120. I propose both. The forced decays need one logged change of `acts/stage4/code/s4pu.py`
(two entries per tt̄-type sample in `SM_SAMPLES`: W⁺ → ℓν with W⁻ → hadrons, and the charge conjugate; tried at
generator level only [V: p2-c-prof-gen-tt1f], not yet through the chain), noted in `CHAIN_PROVENANCE.md`; the
preselection before the chain needs the v2 preselection as a function callable in the generation job.
The summed floor is ×7.5–8 the frozen 12.6, of which ×2.3–3 comes from the unit cost, ×2.3–8 from the
preselection weight, less what the two cost measures recover. The tt̄-type rows rest on one measured process.

## 4. Budget, calendar, storage

- **Pilot generation [E from V unit costs]:** minimum bias 10⁷ × 3.6 ms = 10.0 CPU-h; Geant4 vertices 9.9 (DIF pass
  2.2×10⁷ firings × 0.41 ms, NI pass 5.7×10⁸ × 0.047 ms); chain for 4×10⁶ + 10⁶ (NI elsewhere) + 2.5×10⁵ (curlers) B1
  events 7.4; Z(νν) 2.3×10⁶ × 127 ms = 81.1. **Sum 108 CPU-h against 54.5 budgeted** (STR l.2514, l.2517 less the 7
  CPU-h of overlays): an overrun of 54 CPU-h, reported under brief D6. Channel (iii)'s Phase-2 total: ≈ 142 CPU-h
  against 84 (3.7 spent so far [V: ledger, p2-c-*]).
- **Calendar:** on 3 slots of schrodinger 108 CPU-h is 36 h of wall time; with approval by day 1 the pilot is
  generated by day 3 (deadline day 5).
- **Storage [E]:** Z(νν) 70 GB, B1 samples 18 GB, vertices and minimum bias 9 GB: **≈ 97 GB against 52** (STR l.2633);
  the study total moves from ≈ 470 to ≈ 515 GB (≈ 715 at the pre-merge cap of 400 GB), against the 1.5 TB soft budget.
- **Approved figures: unchanged.** 4,609 CPU-h and the stop-and-ask threshold 5,992 stay; the pool keeps its 665 CPU-h
  (§3.3); the pilot overrun and the toy finding are projections to be carried at stop-rule checkpoint 1.
- **Toys:** at the measured scaling the 183 CPU-h of toys (STR l.2518, T1 263) would be ≈ 3,100 CPU-h at 60 parameters
  and more beyond; T1 as costed holds only near 31 parameters. Proposed tests, in order, all on the Phase-2 timing
  workspace: a gradient backend (jax or pytorch; needs the install slot; ≈ 1 CPU-h); minuit (≈ 0.5 CPU-h); fixing the
  rates of terms below 1 % of a bin under the pruning rule T1-f (≈ 0.5 CPU-h); the auxiliary channels merged into one
  multi-bin channel (≈ 0.5 CPU-h). COM T1-i (l.211) is not changed until these are measured.

## 5. What does not change

The 16 T2 candidates and the selection rule; every acceptance criterion of COM; the answers Q1–Q5 and the defaults
Df-1 to Df-10; Df-9 (H on all own hits, no S_CKF in the day-15 reading); the definition of rule 1 as pinned in Df-11
(which samples are read, one Z(νν) count for every SM process and the multijets, Gamma(m + 1), no pool floor, the
binding median of ≥ 10⁵ draws, a reading within its precision of 300 pauses); the limit B₅₀ = 300; the stop rules;
the approved CPU and calendar; the pool allocation rule; brief D7 (no production sample before the hash).

## 6. Open points I cannot settle

1. Whether a vertex at TBPX L2 or beyond can make a candidate: needs the finder's frozen cuts (n(r), N_IT2, k_max),
   transcribed by channel (i). If N_IT2 ≥ 3 counts inner-tracker layers with two own hits, such vertices can only be
   near-pass; this is an inference, not a result. It decides between the strict and lenient P5.
2. The preselection weights under the v2 MET model (day 12), and the weights and costs of the eleven SM processes that
   were not timed (the tt̄-type rows carry half of the proposed SM floor).
3. Where the 17.5 ms of the chain's dump go (cProfile does not see callbacks made from ACTS); a rewrite might recover
   part of it; not attempted.
4. v1's generator cut p̂T > 150 GeV is not fully efficient for MET > 200 GeV (1.7 % of kept Z(νν) events within 10 GeV
   of the cut [V: p2-c-prof]); its effect on N_trig is not measured.
5. The Fatras step-limit errors on light fragments and the residual β < 0.1 products (item 4 of my work list).
