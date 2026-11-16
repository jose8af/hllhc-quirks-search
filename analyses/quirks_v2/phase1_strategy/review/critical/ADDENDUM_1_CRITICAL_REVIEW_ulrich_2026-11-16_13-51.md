# Critical review of strategy addendum 1 — Ulrich, 2026-11-16 13:51 (`date`)

Artifact: `phase1_strategy/outputs/STRATEGY_ADDENDUM_1_tatiana_2026-11-16_13-31.md` (ADD). `STR` =
`STRATEGY_oscar_2026-11-16_10-41.md`, `COM` = `COMMITMENTS.md`. Tags: **[V]** re-derived by me in this session (file:line
or my script); **[E]** my estimate; **[U]** transcribed, not checked. My scripts (pure Python, niced, einstein) are in
`/var/tmp/jdochoa/ulrich/`: `r1.py`, `r2.py` (rule 1, own implementation, 4×10⁵ draws × 3 seeds), `pool.py` (Table 4.4a),
`w.py` (weights from the 3×10⁴ events of `data/p2c/p2-c-t-hs0`), `g4.py`, `g4b.py` (first-arc counts from
`data/p2c/p2-c-t-g4/000/p2-c-t-g4-y0.npz`). No git command, no job on a worker, no file written outside this review
and the scratch directory.

## Summary for the orchestrator

**Verdict: ITERATE.** The central correction is right and the arithmetic of the tables reproduces. The addendum is not
ready for the user because (i) three things that decide what the pilot generates are not settled, and (ii) the
numbers the user would be shown for the strict option are on the wrong side of the limit once the normalisations are
made consistent with the population the pilot samples.

What holds [V]:
- M_t and the M of rule 1 must be preselected (weighted) events: N_t is N_trig, the yield after the preselection
  (`gen_d123.py` l.10-19, l.129), so N_t/M is a transfer factor only for preselected events. The 13:25 table counted
  generated events as preselected ones; I reproduce it exactly with that mistake (SM 39.0 / 33.4) and the corrected
  values (SM 166.4 / 133.8 / 120.2 / 89.6; B1 4.51 / 11.79; sums 94.1 / 101.4).
- Weights: 0.4308 ± 0.0049, 0.2604 ± 0.0043, 0.1180 ± 0.0031; N_eff/N 0.440, 0.268, 0.125; non-zero 0.442, 0.315, 0.2105.
- Rule 1: frozen case 76 / 181, crossings 13 / 7 and 4 / 2; proposed strict 192 / 296, 3 / 1, 2 / 1, 2 / 1; lenient
  120 / 225, 5 / 2, 3 / 2; all other rows of ADD §3.1 within the Monte Carlo error. The overrides of
  `p2c_addendum1.py` are the changes the text describes and nothing else; the budget copy is byte-identical
  (sha256 548b5ba8…, both files).
- First-arc counts: 22,759 decays (ADD 22,742), 21,610 / 4,154 inelastic vertices elsewhere / at the three radii
  (ADD 21,599 / 4,154); ratios 1.19, 2.01, 5.20 ± 0.09, 6.59.

What does not hold:
- **A1.** The physics argument for leaving the decays after the first turn out of rule 1 has two wrong numbers
  (53 % of those decays come from parents above 0.57 GeV; the sagitta is not "two orders of magnitude" above the
  ribbon widths, it is below them over three inner layers). The check sample (2.5×10⁵ events) reads 313 events per
  count: a zero count there allows 357 events, more than the limit of 300.
- **A2.** Nuclear interactions of parents that have turned (+52 % of the first-arc vertices) are in no term and in
  no sample, with no argument; the "NI elsewhere" sample has π/K parents only while its N_t and the three-radii
  samples include other species.
- **A3.** The hand-over the pilot would use (O13 (b)) has not been run through the validation; the validated one is
  O13 (a). Fatras "no decay, no hadronic interaction" is still UNVERIFIED in the executor's log.
- **B1/B2.** N_t is under-normalised against the population that is sampled (π/K parents +5.2 %; NI: charged
  parents +4.8 %, Geant4 yield +3–8 %, neutral parents +14.5 %). With consistent values an empty pilot under the
  strict option reads **307–321 at R08** and 203–217 at R09 [E], not 295 / 191. Over the R08 pile-up range of the
  strategy (88–148) the addendum's own strict reading is 271–319. "Strict" therefore means: at an R08 candidate the
  study pauses on an empty pilot.
- **B3–B6.** ADD §5 is wrong under the strict option (a 20th ceiling term changes Df-2 / B1-f); the summed floor
  shown (94–101) leaves out the as-timed case (171–178) and rests on two measures not yet run through the chain;
  the consequence for the reach is not given; with the measured toy scaling the projection is ≈ 7,600 CPU-h at 60
  parameters, above 5,992, and the addendum says only that the approved figures do not change.

A cheap option the addendum does not offer [E]: the DIF and NI-elsewhere pilot samples at 4×10⁶ events instead of
10⁶ (≈ +17 CPU-h, +20 GB; the vertices come from the same Geant4 pass). The strict all-zero reading is then 91 (R09)
/ 193 (R08) instead of 192 / 296. The pilot as drafted spends 81 CPU-h for 41 events per Z(νν) count and 3.5 CPU-h
for 78 events per DIF count.

## Item f: what the user must be told (old → new), and the decisions

Numbers shown at Gate A or since, changed by this addendum. "Corrected" = my value with the normalisation made
consistent (finding B1), [E].

| quantity | shown before | addendum | note |
|---|---|---|---|
| one Z(νν) pilot count (all SM processes read through it) | 18 events | **41** with 2.3×10⁶ generated events; 114 at the budgeted 29 CPU-h; 18 only with 5.2×10⁶ generated (184 CPU-h, 158 GB) | provisional: uses v1's preselection; fixed at day 12 with the v2 MET model |
| one decays-in-flight pilot count | 65 | **78** | corrected ≈ 82 |
| one NI pilot count (22 / 30 / 61.5 mm) | 0.88 / 1.12 / 1.12 | **4.0 / 5.1 / 5.1** | corrected ≈ 5.0 / 6.6 / 6.4 |
| NI in the other layers | not a term | strict: **74 per count** (new term); lenient: recorded only | corrected 78 (π/K parents) to 95 (all hadrons) |
| day-15 reading with an empty pilot, R09 candidate | 76 | **120** lenient / **191** strict | corrected 127 / 203–217 |
| the same at an R08 candidate | not printed (caption: limits "about half as high"); 181 by the same computation | **225** lenient / **295** strict | corrected 232 / **307–321 (above 300)**; 271–319 over the R08 pile-up range 88–148 |
| pause limit in Z(νν) counts, R09 / R08 | 12–13 / 6–7 | lenient 5 / 2; strict 3 / 1 | |
| pause limit in decays-in-flight counts, R09 / R08 | 3–4 / 1–2 | lenient 3 / 2; strict 2 / 1 | under strict one count in any of the three large samples pauses at R08 |
| summed zero-count floor of the pool | 12.6 at Gate A; "roughly 50–60" and 41.7 / 36.0 when the pool decision was taken | **94–101** with forced tt̄ decays and the preselection before the chain; **171–178** as timed | the 171–178 is not written as a sum in the addendum |
| SM part of that floor; Z(νν) alone | 8.6; 2.6 | 90–166; 17–29 | eleven of fourteen processes by proxy |
| pool size, SM | 3.65×10⁷ events (Z(νν) 1.10×10⁷) | 2.4–4.4×10⁶ effective events (Z(νν) 1.0–1.7×10⁶) | [V: sum of the M_eff rows] |
| upside case "every ceiling empty", reach median [84 % edge], R09-like | 790 [712] GeV | not given | [E, strategy's own functions]: **593–601 [526–530]** with both measures, **517–521 [451–453]** as timed; the floor the user accepted (36–42) would have been 692–708 [617–634] |
| unit cost of a no-pile-up hard-scatter event | 45 ms (guess) | 127 / 171 / 571 ms | [V] |
| pilot generation | 54.5 CPU-h, 52 GB | 108 CPU-h, 97 GB | reported overrun |
| toy budget | 183 CPU-h, "may double" | ×17 at 60 parameters (≈ 3,100 CPU-h) | projection ≈ 7,600 CPU-h against the threshold 5,992 unless a mitigation works |
| approved 4,609 CPU-h, threshold 5,992 | — | unchanged as approved figures | the projection is not unchanged (finding B5) |
| ceiling-test family | 19 terms | 20 under the strict option | changes α_c of Df-2 / COM B1-f |

What the corrected floor means [E, from STR Table 4.4c and `strategy_budget.py` l.575-663 run on the new floors; my
check reproduces the frozen rows 790 [713] and 494 [433]]:
- **Expected outcome: no change.** The expected branch is the day-15 pause with a background of ≈ 0.7–1.0×10⁴ events
  (STR l.66-74); 90 more events of floor are 1 % of it.
- **Upside case: about 200 GeV lower than at Gate A, about 100 GeV lower than what the pool decision was taken on.**
  With every ceiling empty the predictive background at an R09-like selection is B₁₆/B₅₀/B₈₄ = 64–70 / 88–94 /
  116–124 events (proposed) or 110–115 / 151–158 / 205–212 (as timed), against 13 / 18 / 25. At an R08-like
  selection the as-timed floors alone give B₅₀ ≈ 252–260, close to the class limit of 300.
- Restoring an SM floor of 39 (the 13:25 figure) needs ≈ 1,050 CPU-h with both measures or ≈ 1,950 as timed, against
  457; the Gate-A floor of 8.6 needs ≈ 4,760–8,840 CPU-h [V: floor ∝ 1/CPU, `pool.py`].

Decisions the user has to take:
1. **Pilot size**: (a) 29 CPU-h, 114 per count; (b) 81 CPU-h, 41 per count (proposed); (c) 184 CPU-h, 18 per count as
   frozen. And, not offered by the addendum: larger DIF / NI-elsewhere samples (≈ +17 CPU-h).
2. **NI in the other layers**: strict (a term now) or lenient (recorded, a term only if Phase 3 finds counts). The
   user must know that strict, as sized, reads at or above 300 at an R08 candidate with an empty pilot.
3. **Whether the pool decision stands** at 94–101 (needs a logged chain change and the v2 preselection in the
   generation job) or 171–178 (nothing changed), or whether CPU is added.
4. **Decays and interactions of parents that have turned**: read in rule 1 or not (finding A1, A2).
5. **N_t changes**: first-arc Geant4 yield (×1.19), removal of the factor 0.22 (×4.5 on the NI terms).
6. **Toys**: the projection exceeds the stop-and-ask threshold on the measured scaling; ≈ 2.5 CPU-h of tests and the
   install slot are requested before any change of T1-i.

---

## a. The effective-events correction

**What M_t means.** STR l.888-889: "For a term with normalisation N_t and M_t simulated events, a zero count allows
N_t/M_t × 1.14". N_t of an SM term is its N_trig (STR l.851-852), the yield after the event preselection
(`gen_d123.py` l.10-19: w = ε_trig × veto factors if the event passes, else 0, l.125-129). N_t/M_t is the events per
simulated event only if the M_t events represent N_trig, i.e. are preselected. STR l.356 costs "generation with
filter, shower, chain" at 45 ms and says "the generation filter efficiency is not measured": Phase 1 took a
filter-level event for a preselected one. Rule 1 has the same structure (l.2731, l.2735: "H is Gamma(m + 1)/M",
"2.3×10⁶ events", 10.9 = N_Z/2.3×10⁶). **The addendum's reading is right; the 13:25 table was wrong** [V: `pool.py`
with f = 1 gives SM 39.0 and 33.4, the 13:25 values].

**Weights** [V: `w.py`, `evt` arrays of the 16 files of `data/p2c/p2-c-t-hs0/000`, 10,000 events per process]:

| process | mean w | N_eff/N | w > 0 | Σw/(w_max N) | weight classes (events of 10⁴) |
|---|---|---|---|---|---|
| Z(νν) | 0.4308 ± 0.0049 | 0.4399 | 0.4422 | 0.4396 | 4,397 at ≈ 0.98; 25 at ≈ 0.05; 5,578 at 0 |
| W(τν) | 0.2604 ± 0.0043 | 0.2683 | 0.3149 | 0.2657 | 2,633; 516; 6,851 |
| tt̄ 1ℓ | 0.1180 ± 0.0031 | 0.1251 | 0.2105 | 0.1205 | 1,159; 946; 7,895 |

**Convention.** STR has two statements: the pooled effective count N_eff = (Σw)²/Σw² (l.383, l.814-816, l.1377) and,
for the likelihood, one Poisson channel per weight class of constant weight, effective counts only inside a class
(l.1564). The addendum uses the pooled form. A zero count in the full-weight class gives M = Σw/w_max, 0.1 % (Z),
1.0 % (W), 3.8 % (tt̄) smaller than N_eff: SM floor 169.4 / 91.1 instead of 166.4 / 89.6 [V]. The addendum follows the
strategy's convention; the difference is small and on the lenient side (C2).

**Table 4.4a** [V: `pool.py`, my own allocation code]. Planned split 456.6 / 208.5 CPU-h; planned floors 8.64 / 3.94
/ 12.59 (STR 8.6 / 3.9 / 12.6). SM floor as timed 166.4, forced tt̄ 133.8, preselection first 120.2, both 89.6. Every
row of ADD §3.3 reproduces to the printed digits (Z(νν) 9.89×10⁵ → 1.70×10⁶ effective, 28.9 → 16.8; tt̄ 1ℓ 7.7×10⁴ →
1.67×10⁵, 35.4 → 16.2; DIF 4.2 / 2.6; NI elsewhere 4.5). Sums: 101.4 strict, 94.1 lenient with both measures;
**178.2 / 170.9 as timed**.

Errors of statement in §3.3 and §6: "the tt̄-type rows carry half of the proposed SM floor" (ADD l.200) — they carry
29.9 of 89.6, 33 % (39 % as timed) [V]. "×2.3–3 comes from the unit cost" (l.164) — the SM floor goes 8.64 → 39.0
from the costs (×4.5) and → 166.4 from the weights (×4.3) [V]; no source for 2.3–3.

## b. Rule-1 readings

Own implementation (`r1.py`): κ·Gamma(m + 1) per term plus the pile-up term min(med·e^(sθ), 425.5·Exp(1)); R09 median
6.74, s 0.59; R08 117.9 (range 87.9–148.0), s 0.43; Σ N_SM + N_MJ = 4.1705×10⁷ = 1.663 N_Z.

| case | per count: DIF / NI / all SM / NIx | all-zero B₅₀ R09 / R08 | m_Z | m_DIF | m_NIx |
|---|---|---|---|---|---|
| STR as frozen | 65.13 / 0.883, 1.115, 1.115 / 18.13 | 76.2 / 181.2 (16–84 %: 37–152 at R09) | 13 / 7 | 4 / 2 | — |
| proposed strict | 77.74 / 4.01, 5.07, 5.07 / 41.21 / 73.57 | 192.0 / 295.8 | 3 / 1 | 2 / 1 | 2 / 1 |
| proposed lenient | the same without NIx | 120.1 / 224.9 | 5 / 2 | 3 / 2 | — |
| lenient, DIF at v1 | 65.13 | 110.6 / 214.8 | 5 / 3 | 3 / 2 | |
| lenient, 0.22 kept | | 108.8 / 213.7 | 5 / 3 | 3 / 2 | |
| every decay in DIF | 156.0 | 175.5 / 282.1 | 3 / 1 | 1 / 1 | |
| pilot (a) | 114.2 | 182.0 / 286.8 | 2 / 1 | 2 / 1 | |
| pilot (c) | 18.13 | 96.2 / 202.0 | 11 / 6 | 3 / 2 | |
| strict, curlers in NIx | 93.27 | 208.4 / 312.4 | 3 / 0 | 2 / 0 | 1–2 / 0 |

Frozen checks: m_Z = 11 / 12 / 13 gives 281.5 / 299.8 / 318.1 (STR l.2814: 281 / 300 / 317); m_D = 3 / 4 gives 268.8 /
333.8 (STR: 266 / 331, 20,000 draws). **All of ADD §3.1 reproduces** (the last row's m_NIx at R09 sits at 300.1, on the
limit).

Overrides (`p2c_addendum1.py` l.19-34 against the text): pilot size and f_eff (P1), the ratio 1.19 (P3), 0.22 removed
(P4), 5.20 / 6.59 (P5), costs (§3.3). `read()` (l.43-57) is `d15_q` of `strategy_budget.py` l.878-888 with the pile-up
term as an argument. Nothing else is changed. Two remarks: (i) "STR as frozen … 181" is not a frozen number: STR
prints only the R09 table and the caption "≈ 6–7 Z(νν) or 1–2 decays-in-flight counts" at R08 (l.2819); (ii) the
medians are of 20,000 draws, the binding one needs ≥ 10⁵ (l.2757); at 4×10⁵ × 3 seeds the strict R08 value is
295.8 ± 0.4, so it is resolved below 300 **at the central pile-up value and with the addendum's N_t**.

**Not robust (B1, B2).**
- ADD l.87: "the strict version adds 0.69 × 73.6 = 51 events" — the table gives 191 − 120 = 71 (R09) and 295 − 225 = 71
  (R08) [V]; medians do not add.
- Over the R08 pile-up range that the strategy itself quotes (88–148, l.2819), the strict all-zero reading is 271.2 /
  296.1 / 318.8 and the lenient 199.7 / 224.8 / 247.5 [V].
- With N_t consistent with the sampled population (next section): DIF 81.8, NI 4.97 / 6.56 / 6.35, NIx 77.7 (π/K
  parents) or 95.0 (all hadrons) per count; all-zero lenient 127.0 / 231.9 (m_Z 5 / 2, m_D 3 / 1); strict
  **202.7 / 306.6** (π/K) or **217.2 / 321.2** (all hadrons), i.e. at R08 the crossing is at zero counts [E].

## c. The definition choices

**Normalisation against the sampled population (B1)** [V: `g4.py` on `p2-c-t-g4-y0.npz`; job log
`/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/p2-c-t-g4/000/p2-c-t-g4-y0.a1.log` l.4].
- The pool that the Geant4 passes fire (`p2c_mbgen.py` l.85-90: produced within 1 mm, 0.5 < pT < 20 GeV) holds
  4.510 π/K per interaction, 0.2153 in a 0.15 road. v1's rate counts parents produced exactly at the origin
  (`gen_d123.py` l.150): 0.2047 (`n_dif_parents`). The pool is **5.2 % larger**. The addendum multiplies v1's rate
  (v1's parent count) by a yield ratio measured per pool parent (0.04548 against 0.00780/0.2047). The term that the
  DIF pilot sample represents is N_trig × 200 × 0.2153 × 0.04552 = N_trig × 1.960 for the minimum-bias share, against
  1.5945 × 1.1936 = 1.903 in the addendum (which contains the hard-scatter share): 81.8 per count with the
  hard-scatter share, not 77.7 [E for the share].
- ADD P2 says the population is the one "on which N_t of Table 4.4a is defined, so it neither lowers nor raises the
  frozen 65.1". It is not the same population (within 1 mm against exactly zero; charged NI parents 0.2298 against
  0.2192, +4.8 %).
- "1.56 against 1.59": consistent [V]. 200 × 0.007802 = 1.560 is the minimum-bias share; v1's 1.5945 includes the
  hard-scatter share (1.5687–1.5945 per process, STR l.255). The v1 formula on the pool gives 0.03828 per parent
  (ADD 0.0381) and the first-arc Geant4 yield is 0.04552: ratio 1.19 ✓.
- NI: the Geant4 yield per π± is 2.31 / 3.05 / 2.95×10⁻³ against v1's 2.24 / 2.83 / 2.83×10⁻³ (+3 %, +8 %, +4 %) [V:
  log counts / (3×10⁶ × 0.5395)]. The DIF N_t is corrected to Geant4, the NI N_t is not.
- **Neutral parents.** P2 puts K⁰_L, n, γ in the population; v1's NI rate has π±, K±, p only (`gen_d123.py` l.163).
  In the 'ni' pass neutral parents make 665 / 900 / 881 inelastic vertices against 4,627 / 6,129 / 6,007 from charged
  ones: **+14.4 / 14.7 / 14.7 %** [V: log l.4, `ni.counts`]. The samples would contain them, N_t does not.
- "NI elsewhere" is taken from the 'dif' pass, which fires π± and K± only (`p2c_g4vtx.py` l.27): no p, n, K⁰_L
  parents in the sample, while N_t = 5.20 × (a rate that includes protons). By layer, first arc: outer barrel
  17,159, TBPX L3–L4 2,822, service cylinder 1,260, discs 369 [V].

**P3 (O12), first arc.** Measurement supported: 45,635 decays at 30 < r < 1000 mm in 5×10⁵ firings, 22,759 with
transverse path ≤ πR [V; my path uses the initial pT and the vertex time]. The argument is not supported:
- "a parent that has turned has pT < 0.57 GeV" (ADD l.72): of the 22,876 later decays, 10,645 have pT < 0.57 GeV,
  8,973 have 0.57–0.684, 3,045 have 0.684–0.8, 213 have 0.8–1.0 [V: `g4b.py`]. Parents turn inside the Geant4
  world radius of 1,200 mm (`p2c_g4vtx.py` l.27), not 1,000 mm, and lose energy; examples: pT 0.805 GeV at the
  origin, 0.793 at the vertex, decay at r = 964 mm after 13.4 ns.
- "sagitta over any three counting layers exceeds every ribbon width of the ladder (4.7–9.4 mm) by two orders of
  magnitude" (l.72-74): with s = L²/(8R) (STR l.856-857), R = 0.5 m and the radii of `sim/stage3/code/surfaces_s3.json`
  (30, 61.5, 104.5, 146.5; 248–251, 371–372, 522–524, 686–688, 859–861, 1,082–1,084 mm): TBPX L1–L3 (L = 75 mm)
  1.4 mm, TBPX L1–L4 3.4 mm, TBPS L1–L3 19 mm, TB2S L1–L3 39 mm, the whole barrel 277 mm [V arithmetic, chord
  approximation]. Over three inner layers the sagitta is **below** every ribbon width; nowhere is it two orders
  above. The bound may hold for the number of layers a rung requires, but that is the bound of COM B1-e, which is
  not written yet (STR l.857-858 asks for a threshold with a scattering allowance).
- The named test cannot carry the exclusion: the curler sample has 2.5×10⁵ events for N_t = 7.8×10⁷, 313 events per
  count; a zero count is 357 events at 68 %. Read as its own term in rule 1 it gives an empty-pilot reading of 367
  (R09) / 472 (R08); at 10⁶ events (the vertices exist in the same pass, chain ≈ 1 CPU-h) 196 / 300 lenient [V:
  `r1.py`]. The trigger "H(R05) > 0" is sensible as a loose-rung alarm, but the addendum does not say what rule 1
  reads when it fires.
- B1-g is cited as "in 4a" (l.65, l.77). It is a Phase-3 test (STR l.265, l.2106 sample 13, COM B1-g phase 3,
  deadline 3). Its power: 1,000 pile-up events, one count = N_trig/1,000 = 4.1×10⁴ events, read at R04–R07 and
  triggered at a factor 2 with N ≥ 24 (COM l.183). It can find a gross omission at loose rungs; it cannot bound
  anything at the 300-event scale at R08–R09. The same holds for every "test that catches it" of P2 and P3.

**Interactions of parents that have turned (A2).** In the 'dif' pass the three radii hold 5,150 inelastic vertices
of which 4,154 on the first arc (+24 %), the other layers 33,947 of which 21,610 (+57 %); all together +52 % [V].
The 'ni' pass stops the parent at r = 70 mm (ADD l.80-81), so these vertices are never generated for the three
radii; the strict NIx term is first-arc only; the curler sample `difc` holds decays only. They are in no term and in
no sample, and the addendum gives no argument for them (their products are not bound by the parent's curvature in
the same way as a decay muon).

**P2 (O1).** Supported: the v1 rate is defined on that phase space and is reproduced. "A parent below 0.5 GeV has
2R < 0.88 m and cannot cross the outer barrel layers on its first arc" is imprecise: 2R = 877 mm reaches TB2S L2
(859 mm); a 0.4 GeV parent (2R = 702 mm) crosses the four inner layers, the three TBPS layers and TB2S L1. Whether
that excludes a pass depends on n_2S(r), which is not quoted. The edge-bin test extrapolates from inside the phase
space; it does not measure outside. A 10⁵-event check sample at 0.3 < pT < 0.5 GeV would measure it (≈ 0.5 CPU-h [E]).
Choice: physics for |η| and the road, convenience for the lower pT edge.

**P4 (O3).** Supported and physics: v1's factor is the fraction of NI vertices on the PV line, applied to a gun
that was generated on it (`acts/stage4/WP_RULE.md` §4.1: "P_PV-line ≈ 0.22 is a conservative upper value";
`wp.py` l.40, l.159-160). The v2 sample is the unselected vertex population, so H contains that fraction. The change
is in the strict direction.

**P5 (O4).** Supported: 13 % of the inelastic vertices are at the three radii [V: 5,150 of 39,097]. The strict
version is the consistent one with the frozen rule ("every term … from the samples that exist at day 15"); the
lenient one leaves a population 5.2 times the NI terms out of the reading on an inference the author herself calls
unverified (ADD §6.1). Both are honest as drafted; the sizes and N_t of the strict one need the fixes above.

**P6 (hand-over).** Supported for the failure and for the slab-exit variant: `p2-c-val-b1-0.json`
`all_hard_checks_pass: false`, `p2-c-val-b1x-0.json` `true` [V]. **Not supported for what is proposed**: P6 adopts
O13 (b) (β < 0.1 products followed to their end by Geant4). The run that passed is O13 (a), with 0.07–0.12 slow
products per NI event still handed over and two Fatras step-limit errors (executor log l.154; ADD §6.5 lists it as
open). No validation of (b) exists, and none on DIF, curler or NI-elsewhere events at pilot settings. The Fatras
physics switch-off is "UNVERIFIED until an empirical check on a Fatras-only π/K gun" (executor log l.148); ADD §1.7
reports B1-d without that caveat. If Fatras decayed pions, DIF would be counted twice.

**P7.** Hard-scatter share: 1–2 % of the rate but the stiffest parents. No sample, stream, size or cost is named
for "in Phase 3", and rule 1 reads the pilot samples; as drafted the share is in N_t and not in H. Dropped until
defined.

**Also dropped (present before the addendum, not changed by it):** K⁰_L is stable in the generator and is tracked by
Geant4 only to r = 70 mm in the 'ni' pass, and `classify()` (`p2c_g4vtx.py` l.128) counts decays of π±, K± only.
K⁰_L decays in the tracker (two charged prongs from a neutral parent) are in no term. Size not measured; [E] a few
per cent of the DIF vertices.

**Double counting:** none found. First arc and later decays are disjoint by path; the three radii and "elsewhere"
are disjoint volumes; one vertex per event by the executor's plan (executor log l.99-101, O6; ADD P7), which I did
not check in `g4hv.cc` [U].

## d. Consistency with what is frozen

- Blinding: no signal quantity in the addendum, the memo, the cost study or the script [V: read in full].
- User decisions respected: Q2 (a), 4,609 / 5,992, the pool decision (re-opened explicitly, ADD l.135-136).
- Rule 1 as pinned (Df-11): samples read, one Z(νν) count for all SM, Gamma(m + 1), no pool floor, ≥ 10⁵ draws, ties
  pause — kept. Changed with statement: pilot M (effective), N_t of DIF and NI, a new sample under strict.
- **Changed without statement (B3).** ADD §5 says every acceptance criterion of COM and Df-1 to Df-10 do not change.
  Under the strict option the ceiling family is 20 terms, not 19 (the addendum's own COM row says so, COM l.295):
  α_c = 0.05/19 is in Df-2 (STR l.2940), §4.0 (l.409-411), COM B1-f (l.182) and VC-3 (l.283). A new term also needs a
  closure design (B1-a names DIF and three radii; K = 10, STR l.407-408), test overlays and their cost, a Q3 annex
  row, an inventory row for 4a, and one more auxiliary channel in T1. None is listed.
- **More lenient than the frozen rule without saying so:** the N_t items of B1 (5–30 % low); the curler NI (A2); the
  hard-scatter share (P7); the pooled N_eff (C2); the strict R08 reading quoted at the central pile-up value only.
- **Citations.** STR lines cited exist as cited (l.356, 726-727, 742-746, 853, 869, 876-878, 881-886, 902-916,
  1720-1722, 2514, 2517, 2518, 2633, 2731-2737, 2810-2816, 2823, 2826-2828, 2949, §0 l.95-101) [V]. COM lines are off
  by five: B1-g is l.183 (cited 178), B1-e l.181 (176), T1-i l.216 (211) [V]. `logs/p2c/` does not exist under the
  analysis directory; the logs are in `/nfs/cajuela/jdochoa/quirks_v2/logs/p2c/` [V].
- **Superseded text not listed in ADD §3.2–3.3**: STR l.44-48 (the "about 13 events" headline), l.79-80 and l.2838-2839
  (reach with every ceiling empty), Table 4.4c rows 1–2 and the R08 row (l.968-969, 984), l.797, l.870 ("10.9"),
  l.878 ("12 … 21 events"), l.935-943, l.1027, l.2755-2756 ("≈ 12 Z(νν) pilot counts … between 3 and 4" inside rule 1
  itself), l.2763 ("12.6 to 10.2"), l.2819 (R08 caption), the floors of the Q3 annex (l.2958-2962), COM B4-c
  ("3.65×10⁷ events").
- **Numbers without a reproducible source:** 22,742, 21,599 and 4,154 are constants in `p2c_addendum1.py` l.25-28; no
  script or log computes the first-arc split (my values 22,759 / 21,610 / 4,154).

## e. Budget and calendar

- Pilot [V arithmetic]: 10.0 + (2.51 + 7.44) + 7.26 + 81.1 = 108.3 CPU-h against 54.5 (STR l.2514, l.2517 less 7).
  Storage 2.3×10⁶ × 30.2 kB = 69.5 GB ✓; 470 → 515 GB ✓. Channel total 84 + 54 + 3.7 ≈ 142 ✓; this is above the
  executor's own 1.3 × 84 = 109 stop line (executor log l.24), which the addendum reports.
- **Toys (B5).** Data [V: `p2-c-t-pyhf-n*.json` and logs]: 31 parameters 100 + 100 toys, 638 s; 60 parameters 10 + 10
  toys in the output (5.80 / 5.25 s per toy) plus 100 s+b toys at 5.83 s in a terminated attempt; 80 and 100
  parameters 6 + 6 toys each (8.9 s, 24.3 s). Synthetic workspace, numpy backend, numerical gradients, `q_median`
  0.0 in every file. Supported: the budget fails by an order of magnitude at 60 parameters with this backend
  (×17.3). Not supported as worded: "holds only near 31" (nothing is measured between 31 and 60); ×27 and ×75 are
  indications from 12 toys. Consequence not drawn: 4,609 − 183 + 3,102 + 54 = **7,582 CPU-h at 60 parameters**, 64 %
  above the approved figure and above 5,992; brief §7 / ST-1 (COM l.257) stop the study on a projected overrun
  above 30 %, and STR l.1721-1722 says the budget "is corrected against the stop rule". ADD l.178-179 says the figures
  are unchanged and defers to checkpoint 1.
- **Other lines on the 45 ms guess (B6)**: the multijet loose population (12.5 CPU-h) and B6-c (25 CPU-h) (STR l.356)
  are not re-projected; the caveat of the 13:25 study on the multijets is dropped.
- **Forced tt̄.** Sound as physics [V: `p2c_hs0.py` l.46-47; `p2-c-prof-gen-tt1f.json`: 23.67 tries, 0 of 7,100 with
  a lepton count other than one, σ ratio 3.159×10⁻⁸/1.445×10⁻⁷ = 0.2186]; two half-samples, generator level only, 300
  kept events. The cost 310 ms subtracts absolute times of the loaded profiling job from the timing job (the cost
  study itself says only its shares are usable): by shares it is 460 × 0.274/0.536 + 111 = 346 ms, SM floor 94.4
  instead of 89.6 [V]. The recipe is measured for tt̄ 1ℓ only; tW, tt̄ 2ℓ and t-channel take its cost by proxy and
  need their own forcing.
- **Preselection before the chain.** Unbiased: a zero-weight event contributes nothing, and the smearing draw is
  seeded per event (`p2c_hs0.py` l.52). Cost model consistent with the stage timings (generation 41.8 ms includes
  the summary; chain 85 ms) [V]. What is lost: (i) events that fail the nominal preselection and pass under a
  varied MET model or threshold, so H under such a variation rests on the B4-e factorisation alone; (ii) the pool
  cannot be re-used if the preselection changes after the freeze; (iii) for tt̄, 946 of 2,105 kept events carry
  3.8 % of Σw (the 0.05 veto class) at full chain cost. A prescaled sample of failing events, and Russian roulette
  on the low-weight class (SM floor 88.2 [E]), would address these.
- Calendar: 108 CPU-h on 3 slots = 36 h ✓.

## Findings

**A — must be resolved before the pilot is submitted**
- **A1** Decays after the first turn: correct the two wrong statements (pT limit, sagitta), state the bound with the
  layer count it applies to, size the curler sample at ≥ 10⁶ events, and say what rule 1 reads from it (own term, or
  excluded on the written bound) with the resulting table row.
- **A2** Interactions of parents that have turned, and the species of the NI-elsewhere sample: define the samples
  (all hadron species; curler vertices as a sample or a term) or state the exclusion with an argument and its
  reading.
- **A3** Hand-over: run the validation on the variant the pilot will use (O13 (b)), on every pilot stream; do the
  empirical Fatras π/K check of B1-d.

**B — must be fixed before PASS**
- **B1** N_t consistent with the sampled population (pool against v1 parents, Geant4 NI yield, neutral parents);
  recompute §3.1 and §3.3.
- **B2** Strict reading: give the R08 range over the pile-up estimate; replace "adds 51" by the table value; say
  plainly that strict as sized is at the limit at R08 with an empty pilot.
- **B3** ADD §5 and the COM section: list what the strict option changes (T_c, α_c, closure test, samples, cost,
  annex, T1 channel).
- **B4** Floors: show 171–178 beside 94–101; forced-tt̄ cost by shares; state that the lower figure needs two
  measures not yet through the chain and eleven proxied processes; add the reach consequence; complete the list of
  superseded lines.
- **B5** Toys: state the projection against 5,992 and the stop rule; restate the finding as measured.
- **B6** Re-project the multijet population and B6-c; cost of the strict option's test samples.
- **B7** Hard-scatter share: sample, size, date, and how rule 1 reads it.
- **B8** Weighted pilot counts: define m for the two weight classes (a 0.05-weight event must not read as a full
  count); state that "41" is provisional until day 12.
- **B9** Citations: COM line numbers, B1-g phase, log path; add the script that produces the first-arc counts.
- **B10** State the resolving power of each named test (B1-g, the edge bins, the curler sample); the lower pT edge
  claim with n_2S(r), or a small check sample below 0.5 GeV.

**C — suggestions**
- **C1** Offer larger DIF and NI-elsewhere pilot samples (4×10⁶: strict 91 / 193, m_Z 6 / 3, m_D 11 / 6; with pilot
  (c) 72 / 172) and a table of Z(νν) pilot sizes between (a) and (c) (1.5×10⁶: 53 CPU-h, 63 per count; 3.5×10⁶:
  123 CPU-h, 27 per count).
- **C2** Class-wise zero-count floor (STR l.1564) instead of pooled N_eff.
- **C3** Russian roulette on the 0.05-weight class; a prescaled sample of failing events in the 4a pool.
- **C4** "half of the proposed SM floor" → a third; drop or source "×2.3–3 from the unit cost".
- **C5** Label 181 / 7 / 2 at R08 as computed here, not as frozen.
- **C6** K⁰_L decays in flight: state the omission or add the species to the DIF pass.
- **C7** Update rule 3 (a) ("12.6 to 10.2") for the new floors.

## Verdict

**ITERATE.** Fixes: A1–A3, B1–B10 as listed. The correction of the pool table, the removal of 0.22, the first-arc
yield and the rule-1 arithmetic are sound and reproduce. Nothing here needs ESCALATE: the user decisions of item f
can be put once the readings are recomputed with consistent N_t and the three sample definitions are settled.
