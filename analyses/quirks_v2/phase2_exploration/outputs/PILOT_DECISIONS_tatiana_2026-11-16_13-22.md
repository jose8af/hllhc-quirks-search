# Pilot decision memo — channel (iii), Tatiana, 2026-11-16 13:22

`STR` = `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md`, `COM` = `COMMITMENTS.md`. Tags: [V] measured in
Phase 2 (campaign under `data/p2c/`, `logs/p2c/`), [E] estimate. Rule-1 readings: [E], computed by
`phase2_exploration/src/p2c_rule1.py` with a byte-identical copy of the Phase-1 budget script (sha256 548b5ba8…;
outputs `data/p2c/p2-c-rule1/000/p2-c-rule1-0.json`, `p2-c-rule1b`). "Crossing" = the first pilot count at which the
rule-1 B₅₀ exceeds 300 with the other counts at zero (STR reading: 13 Z(νν) counts, i.e. "at the limit at 12"; 4 DIF
counts). R09 uses the EST pile-up median 6.7 events, R08 117.9 (s_tot 0.43). No pilot campaign is submitted.

## Pilot size (was O5): what one Z(νν) count means

**STR/COM.** 2.3×10⁶ no-pile-up Z(νν)+jets events, 28.8 CPU-h (STR l.869-870, l.1313); rule 1 reads every SM process
and the multijets at "the H per event of the Z(νν) pilot (2.3×10⁶ events)" (l.2734-2737, Df-11 l.2949): 18.1 events
per count for all SM, 10.9 for Z(νν) alone (l.2823).
**Measured.** 0.127 s per event [V: p2-c-t-hs0], 30 kB per event. The generator returns events passing truth
MET > 200 GeV; v1 then weights by its preselection: mean weight 0.397, 40.5 % of events with non-zero weight
[V: 200 events, p2-c-t-hs0s2]. Rule 1's 18.1 assumes 2.3×10⁶ *preselected* events.

| option | filter-level events | effective preselected | CPU-h | GB | events per count (all SM / Z alone) | B₅₀ all counts zero R09 / R08 | crossing m_Z R09 / R08 |
|---|---|---|---|---|---|---|---|
| STR as written | — | 2.3×10⁶ | 28.8 (at 45 ms) | — | 18.1 / 10.9 | 76 / 181 | 13 / 7 |
| (a) budget kept | 0.83×10⁶ | 3.3×10⁵ | 29 | 25 | 127 / 76 | 168 / 273 | 2 / 1 |
| (b) 2.3×10⁶ generated | 2.3×10⁶ | 9.1×10⁵ | 81 | 70 | 45.7 / 27.5 | 104 / 208 | 5 / 3 |
| (c) 2.3×10⁶ preselected-equivalent | 5.8×10⁶ | 2.3×10⁶ | 204 | 175 | 18.1 / 10.9 | 76 / 181 | 13 / 7 |

Frozen text touched: (a), (b) change the 18.1 / 10.9 and "≈ 12 counts" of §0, §4.4 pt 5, §11.7 rule 1, Df-11 and the
v9 table; (c) changes only the cost (§11.2 B4 pilot 29 → 204). The effective size rests on v1's preselection; the v2
MET model (day 12) will change it. **Recommendation: (b).** It keeps the sample the strategy names, costs +52 CPU-h,
and still resolves a pause from a proceed (crossing at 5 counts at R09). (a) pauses on 2 counts. Note: with the user's
pool decision the Z(νν) production pool itself is only 3.1–3.3×10⁶ events (table in `COSTS_POOL_tatiana_…md`).

## O1 population of the "unbiased" DIF and NI events
**STR.** "10⁶ unbiased no-pile-up events each for DIF and the three NI radii" (l.868); N_t = 6.51×10⁷ (Table 4.4a
l.904) = N_trig × 1.59. **v1 rate phase space** [V: `acts/stage4/analysis/gen_d123.py` l.141-169]: prompt π±/K±,
0.5 < pT < 10 GeV (NI: π/K/p, < 20 GeV), |η| < 1, within 0.15 of the road. **Measured:** recomputed on Pythia
minimum bias: DIF 1.56 and NI 0.098 per event [V: p2-c-t-g4], equal to v1.
(a) natural spectrum inside that phase space: 65.1 events per DIF count, N_t unchanged, nothing frozen changes.
(b) every hadron Fatras accepts: N_t not measured; dropping the road cut alone multiplies it by 2π/0.30 = 20.9 →
≥ 1,364 events per DIF count, B₅₀ ≥ 1,070 with all counts zero [E]: the rule would pause on an empty pilot.
STR pt 1 (l.737) also lists K⁰_L, n, γ as primaries; v1's NI rate has charged parents only. I include the neutral
parents at their natural proportion (4–5 % each of the pool; γ 24 %, with an NI yield of 1–3×10⁻⁵) and record the
species. **Recommendation: (a).**

## O12 decays of curling parents (new)
**STR.** rate_DIF = v1 formula, decay between r = 30 and 1000 mm on a straight line (l.881-886). **Measured.** Geant4:
0.0913 decays at 30 < r < 1000 mm per π/K firing; 65 % from parents below 0.66 GeV, median decay time 6.5 ns; decays
within 4 ns: 0.0353 per firing, v1's analytic value 0.038 [V: p2-c-t-g4-y0].
(a) every Geant4 decay: N_t × 2.59 → 169 events per DIF count; B₅₀ all-zero 179 (R09) / 284 (R08); crossing m_D 1 / 1
(with Z option (b)); changes N_t(DIF) in Table 4.4a and "one DIF count is 65". (b) DIF sample = decays on the first
outward arc (transverse path ≤ πR): 65.1 per count, crossing m_D 4 / 2; the later decays form a second sample
(2.5×10⁵ events, 0.3 CPU-h) for the check of the analytic bound. **Recommendation: (b).**
*Phase 1 assumed* the DIF rate is the straight-line decay probability between 30 and 1000 mm. *Phase 2 found* 2.6 times
more Geant4 decays in that radial range, from parents that curl. *Implications:* either N_t(DIF) rises by 2.6 with a
population that the sagitta bound should exclude, or the term is defined on the first arc and the curler decays are
shown empty by the bound and its check; B1-c (rates) must compare like with like.

## O3 NI "PV-line factor" 0.22
**STR.** rates 0.098 / 0.124 / 0.124 "each × 0.22" (l.882-885); the v9 basis line reads 0.88 / 1.12 / 1.12 events per
NI count (l.2823). **Measured.** Geant4 inelastic vertices per π± firing 2.3 / 3.1 / 3.0×10⁻³ against v1's
x/λ × ⟨cosh η⟩ = 2.2 / 2.8 / 2.8×10⁻³ [V]: v1's rate before the 0.22 is confirmed; nothing in the generation
corresponds to 0.22. (a) drop it: 4.0 / 5.1 / 5.1 per count, N_t(NI) × 4.5, B₅₀ all-zero 115 instead of 104 (R09),
crossing m_D 3 instead of 4; changes Table 4.4a NI rows and the basis line. (b) keep it: nothing changes, but an
efficiency-like factor sits inside N_t. **Recommendation: (a).**
*Phase 1 assumed* a fraction 0.22 of NI vertices lies on the plane-hypothesis line. *Phase 2 found* that a Geant4 vertex
lies on its parent's path by construction, so the factor is part of what the pilot measures (H), not of the rate.
*Implications:* N_t(NI) ×4.5; the NI floors of Table 4.4a become 1.3 / 1.4 / 1.4 at the planned M_t [E].

## O4 nuclear interactions outside the three radii
**STR.** NI terms at r = 22, 30, 61.5 mm only (l.726-727). **Fact [V: p2-c-t-g4, π/K, pT > 0.5 GeV, |η| < 1].**
Inelastic vertices per firing: beam pipe 0.40 %, TBPX L1 0.31, L2 0.32, L3 0.31, L4 0.28, service cylinder 0.34,
TBPS L1/L2/L3 0.80 / 0.84 / 0.88, TB2S L1/L2/L3 0.71 / 1.03 / 0.62, discs 0.98; total 7.8 %, of which the three
strategy radii 1.03 % (13 %). Part of the outer-layer excess is from curling parents (O12). **Fact (geometry).**
Counting surfaces beyond the vertex: L3 → 1 inner-tracker layer + 6 outer stacks; L4 → 6 stacks; TBPS Lk → 6 − k
stacks. **Inference [E], not checked against the finder.** Products exist only beyond the vertex, so own-hit
double-crossing layers can only lie beyond it; if the fixed cut N_IT2 ≥ 3 (l.759) counts inner-tracker layers with two
own hits, a vertex at L2 or beyond cannot pass by own hits and enters only as a near-pass with a deficit. Whether such
deficits stay within k_max needs the transcribed finder cuts (channel (i)). I cannot say these vertices make no
candidates. **Cost of recording them:** the DIF pass already produces ≈ 2.2×10⁶ of them; 10⁶ through the chain cost
≈ 1.7 CPU-h and 4 GB. (a) pilot at the three radii only; (b) plus a fourth sample "NI elsewhere" (10⁶ events, by
layer). **Recommendation: (b)**; it enters rule 1 only if the addendum makes it a term (N_t ≈ 7 × the three radii).
*Phase 1 assumed* three NI radii. *Phase 2 found* 87 % of the inelastic vertices of the same parents elsewhere.
*Implications:* an unmeasured population 7 times larger than the NI terms; measured for 1.7 CPU-h.

## Hand-over (O7, O11, O13)
**STR.** products as rows of the v1 particle array, parent hits from Fatras with v1's Truncate, two variants compared in
Phase 3 (l.742-746). **Measured [V: p2-c-val-b1, p2-c-val-b1x].** (i) Products handed over at the vertex: a third of
the hit-making products were fragments with β < 0.1 that Fatras transports; 48 hits earlier than their vertex.
(ii) Products tracked by Geant4 to the exit of the vertex slab: 25–28 % stop inside; all checks pass; 0.07–0.12
products per NI event with β < 0.1 remain; two Fatras step-limit errors. (iii) Fatras parent against Geant4 parent:
DIF 0.6 mm median, 5 mm at 90 %; NI 6–9 µm. (iv) v1 Truncate keeps 7–14 late parent hits per 2,000 DIF events.
Options: O13 (a) exit hand-over as is; (b) Geant4 also follows β < 0.1 products to their end; (c) a fixed cut.
O7: simulate variant A and store the Geant4 parent crossings. O11: v1 Truncate, time-based removal at analysis
level. No effect on N_t or events per count; H changes (unknown size). **Recommendation: O13 (b), O7 and O11 as stated.**
*Phase 1 assumed* Fatras can take every Geant4 product. *Phase 2 found* it cannot (slow fragments). *Implications:* the
hand-over point is the slab exit; [DT1] (Fatras from the vertex) would reintroduce the fault.

## Smaller choices (no effect on rule-1 numbers)
- **O2** hard-scatter share of the parents (1–2 % of the rate): pilot from minimum bias only; add in Phase 3.
- **O6** one vertex per event; a primary whose first vertex is of another type is not a DIF event.
- **O8** road and PV not fixed at generation; origin, an independent PV draw and a road draw are stored.
- **O9** closed by the orchestrator: no B2 work in channel (iii).
- **O10** seed streams `pilot.mb`, `pilot.g4`, `pilot.c0.{dif,ni22,ni30,ni61}`, `pilot.hs0.znn` (INV-1, STR l.2104).
- **Z(νν) generator cut:** 1.7 % of accepted events have p̂T within 10 GeV of the 150 GeV cut [V: p2-c-prof], so v1's
  cut is not fully efficient for MET > 200 GeV; size not measured.
