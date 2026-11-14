# Arbiter verdict, review cycle 8: STRATEGY v8 (Leopold, 2026-11-14 05:00)

Arbiter: Margaret, fresh session, 2026-11-14 06:10. Role file `agents/arbiter.md` followed in full.
Artifact: `outputs/STRATEGY_leopold_2026-11-14_05-00.md` ("v8"; "l." is a line of v8), `src/strategy_budget.py`
("script"), `outputs/budget_stdout_v8.txt` ("stdout v8"), `COMMITMENTS.md` ("COM"), `FIX_REPORT_cycle7_leopold.md`.
Reviews: physics (Ludmila), critical (Magnus), constructive (Marcel), all 2026-11-14 05:40.
Computation: einstein, `nice -n 19 python3 -I`, standard library; the script rerun unchanged (1 min 28 s, stdout
byte-identical to stdout v8) and a scratch copy with the replacement code of §3 (1 min 15 s, 36 MB). No sub-agent, no git.
Tags: VERIFIED = recomputed in this session; ESTIMATE = a planning number of the strategy (v1 placeholder inputs).

**Verdict: ITERATE.** Category A: none. Category B: one, W1, with its root cause in rule 1 itself. The fix is §3
(script), §4 (two mechanical checks) and §5 (eighteen text replacements). Nothing outside the description and the
definition of the day-15 reading is open.

---

## 1. The definition, pinned from rule 1

### 1.1 What rule 1 says (v8 §11.7, l.2728–2748; Df-9 l.2939; §4.4 point 5 l.874–876)

Operative text of rule 1:

> "The projection is recomputed **for every term of the likelihood** (Tables 4.4a and 4.4c with the measured ceilings,
> the three additions at their MET-model N_trig, DIF and the conversions from the pilot's counts), with max(zero-count
> floor, N_t·H) per term and the pile-up estimate of the development occupancy model […]. The projection of a
> no-pile-up term is N_t·H on all own hits, with no S_CKF and no conditional credit (Df-9) […]. Only the test of a
> Q2 (c) redesign multiplies the leading terms by the redesigned conditional and by S_CKF, each estimated on
> development samples […]. A development survival or conditional fraction enters that test at its 68 % upper value
> (Gamma(m + 1) on its m survivors, as H does for the pilot), never at a central zero […]. If B₅₀ is at most 300
> events […] production proceeds […]. If it is larger, or if both pile-up estimators are above their cap, […] the study
> pauses and the user is asked."

§4.4 point 5 adds: "H at a T2 candidate enters the day-7 and day-15 projections as Gamma(m + 1) of the pilot count m (a
pilot zero is a bound of 12 events for Z(νν))". Df-9 adds: own hits, no S_CKF.

Rule 1 is clear on these points:

| point | what rule 1 fixes |
|---|---|
| hits | all own hits before CKF (Df-9) |
| excluded | S_CKF, every conditional (veto, fit-probability), every credit that exists only after the freeze |
| count convention | H = Gamma(m + 1)/M for m counts in a sample of M events; m = 0 gives Exp(1)/M (68 % upper value 1.14/M) |
| pilot-measured terms | Z(νν) on 2.3×10⁶ events, DIF on 10⁶, each NI radius on 10⁶ (§4.4 point 5: the pilot zero of Z(νν) is 12 events = 1.14 × N_Z/2.3×10⁶, so the exposure is the pilot's) |
| pile-up | the occupancy-model estimate; at day 7 the v1-based R09 EST row |
| statistic and threshold | B₅₀ of the summed predictive distribution; pause if B₅₀ > 300 |

### 1.2 Rule 1 is ambiguous on two points. This is the root cause

**Ambiguity 1: the terms that have no sample at day 15.** Rule 1 says "every term of the likelihood … max(zero-count
floor, N_t·H) per term". At day 15 only three kinds of term have a sample (DIF, NI, Z(νν)). The thirteen other SM
processes and the multijets have none ("no Phase-3 SM sample exists", l.2726–2727), and the pool of Table 4.4a does not
exist either. Rule 1 does not say what H, and what zero-count floor, such a term gets. v8 contains three different
answers:

| reading | where | other SM processes and multijets | B₅₀ at 15 Z(νν) pilot counts, DIF and NI empty |
|---|---|---|---|
| (i) | rows 1–2 of the v8 table; "≈ 20 pilot counts" in §0, §4.4 and rule 1 | zero-count floors of the pool of Table 4.4a | 242, proceed |
| (ii) | the (γ) rows of the v8 table; "≈ 13 in the pilot" | H per event as Z(νν), but as separate counts on pool exposures | 331 (m_H = 70), pause |
| (iii) | the physics reviewer's W1 | H per event as Z(νν), one pilot count on the pilot exposure | 353, pause |

VERIFIED (scratch; 242 and 331 are printed cells of stdout v8 l.357 and l.362, 353 is my run and the reviewer's). A
decision rule takes the pilot counts as its input and must return one number. With 12 to 20 Z(νν) pilot counts v8's
rule returns "proceed" or "pause" depending on which row is read. The v8 table presented (i) and (ii) as two
"branches", but a branch is a hypothesis about nature and the rule cannot know which one holds. The three reviewers
recomputed different numbers because each resolved this ambiguity differently, and each of the five earlier fixes
described one reading while the code or a neighbouring sentence used another.

**My reading: (iii).** Every SM hard-scatter process and the multijets are read at the H per event of the Z(νν) pilot:
one count m_Z, one Gamma draw, transfer factor (Σ N_t + N_MJ)/2.3×10⁶. The zero-count floor of a term at day 15 is the
m = 0 case on the sample that exists at day 15. No floor of Table 4.4a enters. Reasons:

1. *It is what can be measured by day 15.* The only H per SM event that exists at day 15 is the Z(νν) pilot's. A pool
   floor is a planned number for a sample that is produced after the freeze.
2. *Reading (i) is blind to the leading expected background.* The conversions are a hard-scatter feature of every SM
   process (v1 photon rates: 0.231 for Z(νν), 0.255 N_trig-weighted). Under (i) the pilot sees only the Z(νν) share,
   37 % of them (3,559 of 9,527 events). A (c) test would then pass at a conversion rejection of about ×16 (VERIFIED,
   scratch), while the conversions of all processes need ×30–44. Reading (i) therefore makes option (c) look easier
   than it is, by construction.
3. *It is what "(…, DIF and the conversions from the pilot's counts)" and the proxy input of decision point 2
   already imply:* the conversions of all SM processes can be read "from the pilot's counts" only by extending the
   Z(νν) pilot count to them.
4. *It is the stricter reading,* so no number shown can understate the reading.

**Consequence, stated openly.** The pilot-count limit that v8 quotes in §0, §4.4 (three places) and rule 1, "≈ 20
Z(νν) ceiling counts", becomes ≈ 12 (20 × 10.9 = 12 × 18.1 = 218 events). The cycle-7 verdict listed "rule 1 as
written" as settled; it is not single-valued, so I reopen it on this one point. No default answer, CPU-h, calendar
figure or expected outcome changes: the expected reading is two orders of magnitude above 300 under every reading.

**Ambiguity 2: the (c) test and the zero-count floor.** Rule 1 says the (c) test "multiplies the leading terms by the
redesigned conditional and by S_CKF". It does not say whether a zero-count floor is multiplied. The decays-in-flight
pilot floor is 65 × Exp(1) events, the largest single piece of an empty pilot's reading. **My reading:** the factors
multiply a counted term, never its floor. This is the conservative reading and the one the physics reviewer used.

### 1.3 The definition as formulas

**Day-15 reading (rule 1).** With the pilot counts m_D (DIF), m_22, m_30, m_61 (NI) and m_Z (Z(νν)), all on own hits
before CKF at the best candidate:

    B = K_D·g(m_D) + K_22·g(m_22) + K_30·g(m_30) + K_61·g(m_61) + K_SM·g(m_Z) + P
    g(m) ~ Gamma(shape m + 1, scale 1), independent draws, one per pilot sample
    P = min(6.74 · exp(0.59 · n), 425.5 · e),  n ~ N(0, 1),  e ~ Exp(1)
    B₅₀ = median of B;  the study pauses if B₅₀ > 300

No S_CKF, no conditional, no post-freeze credit and no pool floor appear. The terms are summed as independent draws.

| input | value | source | tag as in the strategy |
|---|---|---|---|
| K_D = N_DIF / M_D | 4.0848×10⁷ × 1.5945 / 10⁶ = **65.13** events per count | script `NTRIG` (l.68), `RATE["DIF"]` (l.70); pilot size §4.4 point 5 | N_trig, rate: v1 values read from the v1 record; pilot size: design |
| K_22, K_30, K_61 | 4.0848×10⁷ × (0.09823, 0.12408, 0.12408) × 0.22 / 10⁶ = **0.88, 1.12, 1.12** | script `RATE["NI …"]` (l.70–71) | v1 values |
| K_SM = (Σ N_t + N_MJ) / M_Z | (4.1305×10⁷ + 4×10⁵) / 2.3×10⁶ = **18.13** (= 1.663 × Z(νν)'s own 10.90) | script `SM_NTRIG` (l.75–86), `MJ_PLAN` (l.87), `PILOT_HS` (l.156) | twelve N_t: v1 values; Z(ττ), lost-lepton Z(ℓℓ), multijets: ESTIMATE until the MET model (day 12) |
| P (pile-up) | median 6.74, width 0.59, cap 425.5 × Exp(1) | script `PU9` (l.690) | ESTIMATE from v1 numbers (R09 row) |
| sampling | `pmf_pred`'s generator, seed 7; 20,000 draws | script l.575–603 | — |

**Mapping of a planning branch to pilot counts** (ESTIMATE; this is how the table rows are built, not part of the rule).
A term of after-CKF size X events in 3 ab⁻¹ is expected to give X/(1 − ε_pair)/K own-hit pilot counts, with ε_pair =
0.8–0.98 assumed. For the conversions X is the Z(νν) share times K_SM/K_Z, because the pilot counts only Z(νν) events:
X = `EV_GZ` × 1.663 = 3,559 × 1.663 = 5,918 events at v1's own fall (script l.961–962: N_Z × 0.2306 × (2/500)/6.5). For
the decays in flight X = `ALPHA[…][0]` = 385 or 647 events (pile-up fall ×339 or ×201).

**The (c) test (rule 1, EST).** The same sum, with the two leading terms after S_CKF and the conditional, counted on the
same transfer factors, and the floors kept without credit:

    B_c = K_D·g(d_c / K_D) + ΣK_r·g(0) + K_SM·g(c_c / K_SM) + P

where d_c and c_c are the decays-in-flight and conversion sizes in events after S_CKF and the conditional. For the
grid, d_c = f_D × 385 or 647 and c_c = G/R with G the conversion size of all processes (9,527 at v1's maximum photon
rate 0.379; 6,421 at its N_trig-weighted 0.255; 5,918 as the pilot's Z(νν) count would read it) and R the rejection.
"None suffices" means B₅₀ > 300 with c_c = 0.

### 1.4 The clarification of rule 1 that I order

One sentence removes ambiguity 1 and one clause removes ambiguity 2. They are T10 and T12 of §5.

---

## 2. My computation with that definition

### 2.1 Day-15 table and (c) grid (VERIFIED; the printed lines of the replacement code, §3)

~~~~
  v9 (W1): day-15 reading under §11.7 rule 1, a function of the pilot counts alone (own hits before CKF, no S_CKF, no conditional, no post-freeze credit; the study pauses if B50 > 300)
  basis: events in 3 ab^-1 per pilot count: DIF 65.1 (1e6 events); NI 0.88 / 1.12 / 1.12 (1e6 events per radius); every SM hard-scatter process and the multijets through the Z(nunu) pilot count: 18.1 (= (sum N_t + N_MJ) / 2.3e+06 = 1.66 x Z(nunu)'s own 10.9); pile-up R09 EST median 6.7; no pool floor enters; medians of 20000 draws (seed 7)
  (the v6 (T2) and v7 (U1) lines above are on the Table 4.4c basis: pool floors, conversions of all processes at the photon rate 0.379; they are not the day-15 reading, which is this table)
  | pilot counts (branch) | B50 at day 15 | vs 300 |
  | every pilot count zero | 76 [16-84 %: 37-152] | below |
  | Z(nunu) pilot count m_Z, DIF and NI counts zero; m_Z = 2 / 5 / 8 / 10 / 11 / 12 / 13 / 15 / 20 | 115 / 170 / 226 / 263 / 281 / 300 / 317 / 353 / 445 | below / below / below / below / below / at the limit / above / above / above |
  | DIF pilot count m_D, Z(nunu) and NI counts zero; m_D = 1 / 2 / 3 / 4 / 5 | 138 / 202 / 266 / 331 / 397 | below / below / below / above / above |
  | (gamma), and (beta) at day 15 (its Z(nunu) credit exists only after the freeze): the Z(nunu)-count row; m_H = 10 / 30 / 60 / 100 pool-equivalent counts = m_Z 2.1 / 6.3 / 12.6 / 20.9 | 117 / 195 / 309 / 462 | below / below / above / above |
  | (alpha1), no credit: decays in flight and conversions falling like pile-up; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 31-53, m_D 30-50 | ≈ 2.6e+03-4.3e+03 / 2.5e+04-4.2e+04 (sum of medians) | above |
  | (alpha1'), no credit (expected branch): conversions at their own fall; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 1632, m_D 30-50 | ≈ 3.2e+04-3.3e+04 / 3.2e+05-3.3e+05 (sum of medians) | above |
  | (c) only (EST): (alpha1) with fit-probability credit 2/35 (v1's central pile-up fraction; the test takes its 68 % upper value) on decays in flight and conversions (photon rate 0.379), after CKF; x339 / x201 | 109 / 130 | below / below |
  | (c) only (EST): smallest conversion rejection with B50 <= 300, by the decays-in-flight size f_D x v1's central size ((alpha1) DIF at fall x339 / x201), decays in flight and conversions after CKF (S_CKF estimated), the zero-count floors kept; conversions at v1's photon rate; a factor is precise to about 3 % |
  |   f_D = 0 (pilot count zero) | B50 with the conversions removed 76 / 76 | 0.379: x44 (97.7%) / x44 (97.7%); 0.255: x30 (96.7%) / x30 (96.7%); Z(nunu) 0.231 (the pilot's own): x28 (96.4%) / x28 (96.4%) |
  |   f_D = 1/4 | B50 with the conversions removed 168 / 233 | 0.379: x75 (98.7%) / x150 (99.3%); 0.255: x51 (98.0%) / x101 (99.0%); Z(nunu) 0.231 (the pilot's own): x47 (97.9%) / x93 (98.9%) |
  |   f_D = e^-1 | B50 with the conversions removed 213 / 309 | 0.379: x114 (99.1%) / none suffices; 0.255: x77 (98.7%) / none suffices; Z(nunu) 0.231 (the pilot's own): x71 (98.6%) / none suffices |
  |   f_D = 1 (v1's central size) | B50 with the conversions removed 458 / 718 | 0.379: none suffices / none suffices; 0.255: none suffices / none suffices; Z(nunu) 0.231 (the pilot's own): none suffices / none suffices |
  |   without an S_CKF estimate (own hits; eps_pair 0.8 / 0.98, assumed): f_D = 0: x219 / x2186 at 0.379; f_D >= 1/4: none suffices (decays in flight alone: B50 ≈ 545 or more) |
~~~~

### 2.2 Intermediate numbers for one row of each

**Z(νν) pilot count 12, DIF and NI zero.** DIF: 65.13 × Exp(1), median 45.1, mean 65.1. NI: 3.11 × three Exp(1),
medians sum to 2.2. SM: 18.13 × Gamma(13), median 18.13 × 12.67 = 229.7, mean 235.7. Pile-up median 6.7. The sum of
medians is 283.7 and the sum of means is about 312. The median of the sum must lie between them: B₅₀ = 300 (299.6 with
20,000 draws; 300.0 with `pmf_pred`'s default 3,000 draws; 299.8 with 100,000 draws and seed 11). Neighbours: 281 at
11 and 317 at 13. The limit is therefore at ≈ 12 counts and is not resolved more finely by the draws, so the code
prints "at the limit" between 297 and 303.

**Grid cell f_D = 0, photon rate 0.379.** With no decays-in-flight count, the reading is at 300 when the SM term
carries 12 counts, i.e. 12 × 18.13 = 218 events of conversions. R = 9,527/218 = 43.8, printed ×44 (97.7 %). In the same
way 6,421/218 = 29.5 gives ×30 and 5,918/218 = 27.2 gives ×28. The cell is the Z(νν) row read backwards, so the two
tables cannot disagree.

**(α1′), ε_pair = 0.8, fall ×339.** m_Z = 3,559/0.2/10.90 = 1,632; m_D = 385/0.2/65.13 = 29.5. Sum of medians:
0.67 × 86.38 + 6.74 + 385/0.2 + 5,918/0.2 = 57.9 + 6.7 + 1,923 + 29,591 = 3.16×10⁴.

### 2.3 Precision

A 3,000-draw median is precise to about 1 % at B₅₀ ≈ 300 and 2 % for the empty pilot, and a rejection factor inherits
this divided by the remaining margin: with 3,000 draws the same f_D = 1/2 cell came out ×243 and ×323 when I only
changed the order of the terms (VERIFIED, scratch). This would have produced a ninth disagreement in cycle 9. The
replacement code therefore uses 20,000 draws (0.5 % of a median, about 3 % of a factor), drops the ill-conditioned
f_D = 1/2 row, prints the smallest integer factor that passes, and prints two significant figures for the own-hit
rows so that the text can copy them without rounding a rounded number.

### 2.4 Reconciliation with the printed v8 table and with the three reviewers

I reproduced every reviewer number with the script's own functions before comparing (VERIFIED, scratch).

| quantity | v8 printed | Marcel, Magnus | Ludmila | pinned (§1.3) | what explains each difference |
|---|---|---|---|---|---|
| empty pilot | 75 [38–148] | — | 75 | 76 [37–152] (78 with 3,000 draws) | v8: other SM terms at thirteen pool floors (sum of means 84.9). Pinned: read through the Z(νν) count (86.4) |
| Z(νν) limit | 300 at 20 pilot counts | — | accepted | 300 at 12 | v8: only Z(νν)'s own 10.9 events per count; pinned: 18.1 for all SM. 20 × 10.9 = 12 × 18.1 |
| (γ) at 13 pilot counts | 294, below | — | 318, above; limit at 12 | 317 (318.1 with 3,000 draws); limit at 12 | v8: separate Gamma draws on pool exposures (m_H = 60 pool counts). Ludmila's formula is the pinned one; 318 → 317 is the number of draws |
| (α1′) own hits | 4.96×10⁴–5.09×10⁵ | — | accepted | 3.2×10⁴–3.3×10⁵ | v8: conversions of all processes at the maximum photon rate 0.379 (9,527) on pool floors. Pinned: what the pilot counts, the Z(νν) rate 0.231 scaled by N_trig (5,918). Ratio 0.62 |
| (α1) own hits | 2.85×10³–4.78×10⁴ | — | accepted | 2.6×10³–4.2×10⁴ | the same: conversions 183–308 become 114–191 |
| (c) credit rows | 51 / 74 | "≈ 10 higher" | 61 / 84; 84 / 92 with the DIF pilot floor | 109 / 130 | v8: pool floors, credited sizes as log-normals. Ludmila: pilot floors for the other terms, then the DIF floor in place of the credited DIF. Pinned: the credited sizes counted on top of the pilot floors (§1.3), which adds the credited DIF (22–37) and conversions (10–18) |
| conversions removed, v1's central DIF | 401 / 663 | 401–663 | — | 458 / 718 | pool floors against pilot floors (+55 to +57) |
| grid f_D = 0, 0.379 [0.255] | ×34 [×23] | ×35 [×24] | ×43 [×29]; ×46 [×31] | **×44 [×30]** | ×33.7: pool floors, DIF term dropped. ×35.1: other terms at pilot exposures, DIF still dropped. ×43.3: the same with the DIF pilot floor kept. ×45.5: in addition the conversions counted on Z(νν)'s 10.9 beside a separate empty Z(νν) floor of 10.9, so the Z(νν) floor is counted twice; without that second floor her basis gives ×43.4. Pinned ×43.5 → 44 |
| grid f_D = 1/4, 0.379 | ×52 / ×81 | ×55 / ×90 | ×80 / ×172 | **×75 / ×150** | as above; the DIF now sits on its pilot transfer factor (+0.67 × 65 = 44 events at the median) and the double Z(νν) floor is removed |
| grid f_D = e⁻¹, 0.379 | ×69 / ×235 | ×75 / ×311 | ×127 / none | **×114 / none** | as above. For the fall ×201 the conversion-free reading is 309, above 300 |
| printed ×34 on the pilot basis | — | — | 358, above | 359 | 358.5 is `kap_d15` plus the conversions on the pool factor; mine has them on K_SM. Both are above 300 |
| pilot-own photon rate | — | — | — | ×28 / ×47–93 / ×71–none | new column: the factor at which the pilot's own count would pass, by v1's Z(νν) rate. It is below the 0.255 column by 8 %, so the 0.379 and 0.255 columns do not understate the rule's bar |

No difference is left unexplained. Every v8 cell that differs from the pinned value differs in the direction that
makes a branch or option (c) look easier, except the (α) own-hit rows, which were higher but were not what the pilot
would read.

---

## 3. The fix: (i), recompute on rule 1's own basis

**Decision: (i).** Relabelling (ii) fails the first criterion: the human must be told what the day-15 rule will read,
and no printed v8 row after row 2 is that reading. It also fails the second: ×34, "≈ 20 pilot counts" and 51–74 are
all easier than the reading. The third criterion (mechanical check against the script) holds for (i) through §4.

### 3.1 Script changes (three, and nothing else)

Line numbers are those of the v8 script (1,428 lines).

**(a) Replace l.853–905** (from the comment `# v8 (V1, verdict cycle 7 §4 item S): …` through the line
`print("  |   (alpha1) conversion levels for comparison: …")`, both included) by block A:

~~~~python
# v9 (W1, verdict cycle 8): day-15 reading under §11.7 rule 1 as a function of the pilot counts alone. Samples that exist at
# day 15: the pilot's 1e6 DIF events, 1e6 events per NI radius and PILOT_HS = 2.3e6 Z(nunu) events (no pool, no other SM sample).
# Every term enters at (N_t / M_pilot) x Gamma(m + 1) of an own-hit count before CKF (m = 0: its zero-count floor on the sample
# that exists at day 15): DIF and each NI radius on their own pilot sample; every SM hard-scatter process and the multijets at the
# H per event of the Z(nunu) pilot (one count m_Z, one Gamma draw for all of them). No S_CKF, no conditional, no post-freeze credit,
# no Table 4.4a pool floor. Pile-up: the R09 EST term PU9. B50 = median of D15_ND draws of pmf_pred's generator (seed 7); for the own-hit rows the
# sum of medians sum kappa (m + 0.67) + pile-up median. Rows marked (c) are the Q2 (c) test only (EST): the leading terms after
# S_CKF and the conditional, counted on the same pilot transfer factors, the zero-count floors kept without credit.
D15_NI = ("NI 22 mm", "NI 30 mm", "NI 61.5 mm")
D15_KD = NTRIG * RATE["DIF"] / 1e6
D15_KNI = [NTRIG * RATE[t_] / 1e6 for t_ in D15_NI]
D15_KSM = (sum(SM_NTRIG.values()) + MJ_PLAN) / PILOT_HS
D15_KZ = NZ / PILOT_HS
D15_GZ = 0.23059926668409783                            # v1 photon rate of Z(nunu)+j (= GZ below; background.json -> cprime.gamma.rate.per_process.Znunu_j)
D15_ZCONV = NZ * D15_GZ * (2 / 500.0) / 6.5             # Z(nunu) conversions at R08 after CKF, own fall (= EV_GZ below)
D15_ND = 20000                                          # draws per median (precision: about 0.5 % of a median, about 3 % of a rejection factor)
D15_T1 = ("alpha1 (pile-up fall x339)", "alpha1 (pile-up fall x201)")
D15_G = (("0.379", G_A1P), ("0.255", G_A1P * F_GAM["N_trig-weighted rate 0.255"]), ("Z(nunu) 0.231 (the pilot's own)", D15_ZCONV * D15_KSM / D15_KZ))


def d15_gam(m_z=0.0, m_dif=0.0, m_ni=(0.0, 0.0, 0.0)):
    """rule-1 terms from the pilot counts: (transfer factor, count) for DIF, the three NI radii, all SM + multijets."""
    return [(D15_KD, m_dif)] + [(k_, m_) for k_, m_ in zip(D15_KNI, m_ni)] + [(D15_KSM, m_z)]


def d15_q(gam, nd=None, seed=7):
    """16 %, 50 %, 84 % quantiles of sum kappa x Gamma(m + 1) + PU9: the draws of pmf_pred(gam, (PU9,), nd, seed) without its pmf."""
    nd = D15_ND if nd is None else nd
    rnd = random.Random(seed)
    bs = []
    for _ in range(nd):
        b = sum(k * rnd.gammavariate(m + 1, 1.0) for k, m in gam)
        x = PU9[0] * math.exp(PU9[1] * rnd.gauss(0, 1))
        bs.append(b + min(x, -PU9[2] * rnd.expovariate(1.0)))
    bs.sort()
    return bs[int(0.16 * nd)], bs[nd // 2], bs[int(0.84 * nd)]


def d15_b50(gam):
    return d15_q(gam)[1]


def d15_som(gam):
    return sum(k * (m + 0.67) for k, m in gam) + pu9


def d15_cls(b):
    return "below" if b <= 297 else ("above" if b > 303 else "at the limit")   # within 1 % of 300: not resolved by the draws


def d15_need(fd, tag, g, rmax=1e5):
    """smallest integer conversion rejection R with B50 <= 300; None if B50 > 300 with the conversions removed entirely."""
    md_ = ALPHA[(tag, False)][0] * fd / D15_KD
    if d15_b50(d15_gam(0.0, md_)) > 300:
        return None
    lo, hi = 1.0, rmax
    for _ in range(16):
        mid = math.sqrt(lo * hi)
        if d15_b50(d15_gam(g / mid / D15_KSM, md_)) > 300:
            lo = mid
        else:
            hi = mid
    r_ = math.ceil(hi)
    while d15_b50(d15_gam(g / r_ / D15_KSM, md_)) > 300:
        r_ += 1
    return r_


D15 = {}
print("  v9 (W1): day-15 reading under §11.7 rule 1, a function of the pilot counts alone (own hits before CKF, no S_CKF, no conditional, no post-freeze credit; the study pauses if B50 > 300)")
print(f"  basis: events in 3 ab^-1 per pilot count: DIF {D15_KD:.1f} (1e6 events); NI {' / '.join(f'{k_:.2f}' for k_ in D15_KNI)} (1e6 events per radius); every SM hard-scatter process and the multijets"
      f" through the Z(nunu) pilot count: {D15_KSM:.1f} (= (sum N_t + N_MJ) / {PILOT_HS:.2g} = {D15_KSM / D15_KZ:.2f} x Z(nunu)'s own {D15_KZ:.1f}); pile-up R09 EST median {pu9:.1f}; no pool floor enters; medians of {D15_ND} draws (seed 7)")
print("  (the v6 (T2) and v7 (U1) lines above are on the Table 4.4c basis: pool floors, conversions of all processes at the photon rate 0.379; they are not the day-15 reading, which is this table)")
print("  | pilot counts (branch) | B50 at day 15 | vs 300 |")
D15["empty"] = d15_q(d15_gam())
print(f"  | every pilot count zero | {D15['empty'][1]:.0f} [16-84 %: {D15['empty'][0]:.0f}-{D15['empty'][2]:.0f}] | {d15_cls(D15['empty'][1])} |")
D15["mz"] = [(m_, d15_b50(d15_gam(m_))) for m_ in (2, 5, 8, 10, 11, 12, 13, 15, 20)]
print("  | Z(nunu) pilot count m_Z, DIF and NI counts zero; m_Z = " + " / ".join(str(m_) for m_, _ in D15["mz"]) + " | "
      + " / ".join(f"{b_:.0f}" for _, b_ in D15["mz"]) + " | " + " / ".join(d15_cls(b_) for _, b_ in D15["mz"]) + " |")
D15["md"] = [(m_, d15_b50(d15_gam(0, m_))) for m_ in (1, 2, 3, 4, 5)]
print("  | DIF pilot count m_D, Z(nunu) and NI counts zero; m_D = " + " / ".join(str(m_) for m_, _ in D15["md"]) + " | "
      + " / ".join(f"{b_:.0f}" for _, b_ in D15["md"]) + " | " + " / ".join(d15_cls(b_) for _, b_ in D15["md"]) + " |")
D15["gamma"] = [(mh_, mh_ * PILOT_HS / MZ, d15_b50(d15_gam(mh_ * PILOT_HS / MZ))) for mh_ in (10, 30, 60, 100)]
print("  | (gamma), and (beta) at day 15 (its Z(nunu) credit exists only after the freeze): the Z(nunu)-count row; m_H = " + " / ".join(str(a_) for a_, _, _ in D15["gamma"])
      + " pool-equivalent counts = m_Z " + " / ".join(f"{p_:.1f}" for _, p_, _ in D15["gamma"]) + " | " + " / ".join(f"{b_:.0f}" for _, _, b_ in D15["gamma"])
      + " | " + " / ".join(d15_cls(b_) for _, _, b_ in D15["gamma"]) + " |")
for key_, lab_, zc_ in (("a1", "(alpha1), no credit: decays in flight and conversions falling like pile-up", [D15_ZCONV * 6.5 / f_ for f_ in FALL_PU]),
                        ("a1p", "(alpha1'), no credit (expected branch): conversions at their own fall", [D15_ZCONV, D15_ZCONV])):
    cells = []
    for e_ in (0.8, 0.98):
        v_ = [d15_som(d15_gam(z_ / (1 - e_) / D15_KZ, ALPHA[(t_, False)][0] / (1 - e_) / D15_KD)) for t_, z_ in zip(D15_T1, zc_)]
        D15[(key_, e_)] = v_
        cells.append(f"{v_[0]:.2g}-{v_[1]:.2g}")
    mz_ = sorted({f"{z_ / 0.2 / D15_KZ:.0f}" for z_ in zc_}, key=float)
    print(f"  | {lab_}; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z {'-'.join(mz_)},"
          f" m_D {ALPHA[(D15_T1[0], False)][0] / 0.2 / D15_KD:.0f}-{ALPHA[(D15_T1[1], False)][0] / 0.2 / D15_KD:.0f} | ≈ {cells[0]} / {cells[1]} (sum of medians) | above |")
D15["credit"] = [d15_b50(d15_gam(ALPHA[(t_, True)][1] / D15_KSM, ALPHA[(t_, True)][0] / D15_KD)) for t_ in D15_T1]
print(f"  | (c) only (EST): (alpha1) with fit-probability credit 2/35 (v1's central pile-up fraction; the test takes its 68 % upper value) on decays in flight and conversions (photon rate 0.379), after CKF; x339 / x201"
      f" | {D15['credit'][0]:.0f} / {D15['credit'][1]:.0f} | {d15_cls(D15['credit'][0])} / {d15_cls(D15['credit'][1])} |")
print("  | (c) only (EST): smallest conversion rejection with B50 <= 300, by the decays-in-flight size f_D x v1's central size ((alpha1) DIF at fall x339 / x201), decays in flight and conversions after CKF"
      " (S_CKF estimated), the zero-count floors kept; conversions at v1's photon rate; a factor is precise to about 3 % |")
D15["grid"] = {}
D15["base"] = {}
for fd_, fl_ in ((0.0, "0 (pilot count zero)"), (0.25, "1/4"), (math.exp(-1), "e^-1"), (1.0, "1 (v1's central size)")):
    D15["base"][fd_] = [d15_b50(d15_gam(0.0, ALPHA[(t_, False)][0] * fd_ / D15_KD)) for t_ in D15_T1]
    cells = []
    for gl_, g_ in D15_G:
        nn = [d15_need(fd_, t_, g_) for t_ in D15_T1]
        D15["grid"][(fd_, gl_)] = nn
        cells.append(f"{gl_}: " + " / ".join("none suffices" if x is None else f"x{x:d} ({1 - 1 / x:.1%})" for x in nn))
    print(f"  |   f_D = {fl_} | B50 with the conversions removed {D15['base'][fd_][0]:.0f} / {D15['base'][fd_][1]:.0f} | " + "; ".join(cells) + " |")
D15["own"] = [d15_need(0.0, D15_T1[0], G_A1P / (1 - e_)) for e_ in (0.8, 0.98)]
D15["own_dif"] = [d15_som(d15_gam(0.0, ALPHA[(D15_T1[0], False)][0] * 0.25 / (1 - 0.8) / D15_KD))]
print(f"  |   without an S_CKF estimate (own hits; eps_pair 0.8 / 0.98, assumed): f_D = 0: x{D15['own'][0]:d} / x{D15['own'][1]:d} at 0.379; f_D >= 1/4: none suffices"
      f" (decays in flight alone: B50 ≈ {D15['own_dif'][0]:.0f} or more) |")
~~~~

**(b) In l.964**, inside the f-string, replace
`(day-15 class limit: m_H = 125 in the pool for Z(nunu) alone, about 20 pilot counts: v8 table)` by
`(class limit B50 = 300: m_H = 125 pool counts if Z(nunu) alone sat at its ceiling; the day-15 rule reads the pilot count for every SM process and is at the limit at 12 pilot counts: v9 table)`.

**(c) Insert block B directly after l.964** (before the blank line that precedes `# ---- [10]`):

~~~~python
# v9 (W1) self-test of the day-15 table: every check recomputes from the raw inputs (NTRIG, RATE, SM_NTRIG, MJ_PLAN, the pilot sizes
# written out) through d15_q (tied to pmf_pred by check 2) or an independent draw (seed 11), not through the table rows above.
def d15_test():
    ok = []

    def chk(name, cond, info=""):
        ok.append(bool(cond))
        print(f"  v9 self-test {len(ok)}: {'PASS' if cond else 'FAIL'}: {name}" + (f" [{info}]" if info else ""))
    nsm = sum(SM_NTRIG.values()) + MJ_PLAN
    raw = lambda mz=0.0, md=0.0: [(4.0848e7 * 1.5945 / 1e6, md)] + [(NTRIG * RATE[t_] / 1e6, 0) for t_ in ("NI 22 mm", "NI 30 mm", "NI 61.5 mm")] + [(nsm / 2.3e6, mz)]
    ref = lambda g: d15_q(g)[1]
    # 1 basis: pilot exposures only, no pool transfer factor
    pool = [r[4] for r in rows] + [MJK[0]]
    used = [k for k, _ in d15_gam()]
    chk("basis = pilot exposures (DIF, NI: N_t / 1e6; all SM + multijets: (sum N_t + N_MJ) / 2.3e6); no pool transfer factor used",
        all(abs(a - b) < 1e-9 * b for a, b in zip(used, [k for k, _ in raw()])) and not any(abs(k - p) < 1e-9 * p for k in used for p in pool),
        "kappa " + " / ".join(f"{k:.2f}" for k in used))
    # 2 key cells against pmf_pred on the raw inputs
    cells = [("empty", D15["empty"][1], raw())] + [(f"m_Z = {m}", b, raw(m)) for m, b in D15["mz"] if m in (11, 12, 13)] + [(f"m_D = {m}", b, raw(0, m)) for m, b in D15["md"] if m in (3, 4)]
    dv = [(n, b, pmf_pred(g, (PU9,), nd=D15_ND)[1][1]) for n, b, g in cells if n in ("empty", "m_Z = 12", "m_D = 4")]
    chk("key cells equal pmf_pred(raw inputs, (PU9,), nd = D15_ND)", len(dv) == 3 and all(abs(b - r) < 1e-6 for _, b, r in dv), "; ".join(f"{n}: {r:.1f}" for n, _, r in dv))
    # 3 independent draw (seed 11, 100,000 draws): the table's medians within 2 %
    hs = [(n, b, d15_q(g, nd=100000, seed=11)[1]) for n, b, g in cells]
    chk("key cells within 2 % of an independent 100,000-draw median (seed 11)", all(abs(b - h) < 0.02 * h for _, b, h in hs), "; ".join(f"{n}: {h:.1f}" for n, _, h in hs))
    # 4 monotonic in the counts
    sz = [ref(raw(m)) for m in range(0, 22)]
    sd = [ref(raw(0, m)) for m in range(0, 7)]
    chk("B50 rises with the Z(nunu) count (0-21) and with the DIF count (0-6)", all(a < b for a, b in zip(sz, sz[1:])) and all(a < b for a, b in zip(sd, sd[1:])))
    # 5 thresholds
    chk("threshold: Z(nunu) count 11 below (<= 297), 12 at the limit (297-303), 13 above (> 303); DIF count 3 below, 4 above",
        sz[11] <= 297 < sz[12] <= 303 < sz[13] and sd[3] <= 297 and sd[4] > 303, f"{sz[11]:.1f} / {sz[12]:.1f} / {sz[13]:.1f}; {sd[3]:.1f} / {sd[4]:.1f}")
    # 6 no S_CKF and no conditional in the own-hit rows: (reading - empty sum of medians) x (1 - eps) = after-CKF level of all SM + DIF
    t_ = []
    for e_ in (0.8, 0.98):
        for i_, tg_ in enumerate(D15_T1):
            lev = EV_GZ * nsm / NZ + ALPHA[(tg_, False)][0]
            t_.append(abs((D15[("a1p", e_)][i_] - d15_som(raw())) * (1 - e_) - lev) < 1e-6 * lev)
            lev = EV_GZ * 6.5 / FALL_PU[i_] * nsm / NZ + ALPHA[(tg_, False)][0]
            t_.append(abs((D15[("a1", e_)][i_] - d15_som(raw())) * (1 - e_) - lev) < 1e-6 * lev)
    chk("own-hit rows = after-CKF level x 1/(1 - eps_pair) on top of the empty reading (no S_CKF, no conditional); Z(nunu) conversions = EV_GZ", all(t_) and abs(D15_ZCONV - EV_GZ) < 1e-9 * EV_GZ and D15_GZ == GZ and min(min(v) for k, v in D15.items() if isinstance(k, tuple)) > 300,
        f"(alpha1') at 0.8: {D15[('a1p', 0.8)][0]:.4g}; smallest own-hit cell {min(min(v) for k, v in D15.items() if isinstance(k, tuple)):.4g}, above 300")
    # 7 grid, on an independent draw (seed 11, 50,000 draws): 1.1 x the printed factor passes, the factor / 1.1 fails; "none" where the
    # conversion-free reading is above 300
    hsq = lambda g: d15_q(g, nd=50000, seed=11)[1]
    g_ok = []
    for (fd_, gl_), nn in D15["grid"].items():
        g_ = dict(D15_G)[gl_]
        for tg_, x in zip(D15_T1, nn):
            md_ = ALPHA[(tg_, False)][0] * fd_ / (4.0848e7 * 1.5945 / 1e6)
            if x is None:
                g_ok.append(hsq(raw(0.0, md_)) > 300)
            else:
                g_ok.append(hsq(raw(g_ / (1.1 * x) / (nsm / 2.3e6), md_)) <= 300 < hsq(raw(g_ / (x / 1.1) / (nsm / 2.3e6), md_)))
    chk(f"grid, independent draw: each of the {len(g_ok)} cells passes at 1.1 x its printed factor and fails at the factor / 1.1; 'none suffices' only where B50 > 300 with the conversions removed",
        all(g_ok), f"{sum(g_ok)} of {len(g_ok)}")
    # 8 grid ordering: the factor rises with f_D and with the photon rate
    key = lambda x: 1e99 if x is None else x
    fds = sorted({k[0] for k in D15["grid"]})
    gls = [g[0] for g in D15_G]
    chk("grid: the factor does not fall with f_D, nor from the pilot's own rate to 0.255 to 0.379",
        all(key(D15["grid"][(a, gl)][i]) <= key(D15["grid"][(b, gl)][i]) for a, b in zip(fds, fds[1:]) for gl in gls for i in (0, 1))
        and all(key(D15["grid"][(fd, gls[2])][i]) <= key(D15["grid"][(fd, gls[1])][i]) <= key(D15["grid"][(fd, gls[0])][i]) for fd in fds for i in (0, 1)))
    print(f"  v9 self-test: {'ALL PASS' if all(ok) else 'FAILED'} ({sum(ok)} of {len(ok)})")


d15_test()
~~~~

Also (critical C-5, not printed): in the docstring l.2–4 replace "STRATEGY v4 (STRATEGY_fiona_2026-11-13_23-05.md)" by
"STRATEGY (current version: see COMMITMENTS.md)" and "about ten seconds" by "about 75 seconds".

Block A defines its own names (`D15_*`, `d15_*`); it does not redefine `_b50`, `_cls`, `_need`, `PIL_N`, `K_PIL`,
`kap_d15`, `kd15_noz`, `kzp`, which disappear with the v8 block and are used nowhere else (VERIFIED: the scratch copy
runs to the end). It uses a private `random.Random(7)`, so no later number moves.

### 3.2 Expected output

`budget_stdout_v9.txt` must be 582 lines with sha256
`0ca4af15f22d3025a5b338892b907a29f950b6af8af2050dd2cc5590e003433d` (VERIFIED: two scratch runs, identical). Against
stdout v8, `diff` must give exactly two hunks, `354,376c354,370` and `396c390,399`. I checked with `cmp` that v8 lines
1–353, 377–395 and 397–579 equal the new lines 1–353, 371–389 and 400–582: **every value printed by v8 outside the two
tables is byte-identical**; the only other changed line is the label of (b). Lines 354–370 must equal §2.1 cell by
cell. Lines 390–399 (the label line of (b), then the nine self-test lines) must be:

~~~~
  v5 (R1) P3/P14 EST with the conversions' own fall: Z(nunu) conversion part at R08 = 2.51e+07 x 0.2306 x (2/500) / 6.5 = 3.56e+03 events in 3 ab^-1; m_H = 1.56e+03 in 1.1e+07 pool events, 326 in the pilot's 2.3e+06 events (class limit B50 = 300: m_H = 125 pool counts if Z(nunu) alone sat at its ceiling; the day-15 rule reads the pilot count for every SM process and is at the limit at 12 pilot counts: v9 table)
  v9 self-test 1: PASS: basis = pilot exposures (DIF, NI: N_t / 1e6; all SM + multijets: (sum N_t + N_MJ) / 2.3e6); no pool transfer factor used [kappa 65.13 / 0.88 / 1.12 / 1.12 / 18.13]
  v9 self-test 2: PASS: key cells equal pmf_pred(raw inputs, (PU9,), nd = D15_ND) [empty: 76.4; m_Z = 12: 299.6; m_D = 4: 331.0]
  v9 self-test 3: PASS: key cells within 2 % of an independent 100,000-draw median (seed 11) [empty: 76.3; m_Z = 11: 281.3; m_Z = 12: 299.8; m_Z = 13: 318.0; m_D = 3: 268.7; m_D = 4: 333.3]
  v9 self-test 4: PASS: B50 rises with the Z(nunu) count (0-21) and with the DIF count (0-6)
  v9 self-test 5: PASS: threshold: Z(nunu) count 11 below (<= 297), 12 at the limit (297-303), 13 above (> 303); DIF count 3 below, 4 above [281.1 / 299.6 / 317.3; 265.9 / 331.0]
  v9 self-test 6: PASS: own-hit rows = after-CKF level x 1/(1 - eps_pair) on top of the empty reading (no S_CKF, no conditional); Z(nunu) conversions = EV_GZ [(alpha1') at 0.8: 3.158e+04; smallest own-hit cell 2555, above 300]
  v9 self-test 7: PASS: grid, independent draw: each of the 24 cells passes at 1.1 x its printed factor and fails at the factor / 1.1; 'none suffices' only where B50 > 300 with the conversions removed [24 of 24]
  v9 self-test 8: PASS: grid: the factor does not fall with f_D, nor from the pilot's own rate to 0.255 to 0.379
  v9 self-test: ALL PASS (8 of 8)
~~~~

If the fixer's sha256 differs, the fixer stops and reports the differing cells; it does not adapt the text.

---

## 4. Guard against a ninth member of the family

### 4.1 Self-test in the script (block B above)

It is run by the fixer and again by the cycle-9 physics reviewer. It recomputes from the raw inputs (N_trig, the rates,
the pilot sizes written out as literals), not from the table rows, and prints one PASS/FAIL line per check:

| # | invariant |
|---|---|
| 1 | basis: every transfer factor is N_t/10⁶ (DIF, NI) or (Σ N_t + N_MJ)/2.3×10⁶; no pool transfer factor of Table 4.4a is used |
| 2 | the empty, m_Z = 12 and m_D = 4 cells equal `pmf_pred(raw inputs, (PU9,), nd = 20000)`, the script's established function |
| 3 | six key cells agree within 2 % with an independent draw (seed 11, 100,000 draws) |
| 4 | B₅₀ rises with the Z(νν) count (0–21) and with the DIF count (0–6) |
| 5 | thresholds: Z(νν) count 11 below, 12 at the limit, 13 above; DIF count 3 below, 4 above |
| 6 | no S_CKF and no conditional: each own-hit cell minus the empty sum of medians, times (1 − ε_pair), equals the after-CKF size; the Z(νν) conversions equal `EV_GZ`; every own-hit cell is above 300 |
| 7 | grid, on the independent draw: each factor passes at 1.1 × its printed value and fails at the value/1.1; "none suffices" only where B₅₀ > 300 with the conversions removed |
| 8 | grid ordering: the factor does not fall with f_D, nor from the pilot's own rate to 0.255 to 0.379 |

### 4.2 Text check (new file `phase1_strategy/src/check_day15_text.py`)

The fixer creates this file exactly as below and runs
`python3 -I phase1_strategy/src/check_day15_text.py <STRATEGY v9> phase1_strategy/outputs/budget_stdout_v9.txt`.
It parses the printed table and checks the strategy against it in four parts: (A) the fenced blocks equal the 17
printed lines; (B) sixteen required statements, each built from the printed values, occur the stated number of times;
(C) six regular expressions find every statement of the family (pilot-count limits, rejection factors with and without
percentages, the reading in powers of ten, B₅₀ ranges in "The pause" and Q2) and require a printed value in each;
(D) twenty-one stale strings of v6–v8 have no hit outside §13 and the code fences. The regular expressions and the
value each must equal are the `req`, `scan` and `stale` lists of the file.

~~~~python
#!/usr/bin/env python3
"""Text check of the day-15 family (verdict cycle 8, §4.2). Standard library only.
usage: python3 -I check_day15_text.py STRATEGY.md budget_stdout.txt
Reads the day-15 table and the (c) grid printed by script [9b] (the "v9 (W1)" lines) and checks the strategy against them:
(A) the fenced blocks that quote the table are identical to the printed lines; (B) every required statement is present with the
printed value; (C) every statement of the family found by a regular expression carries a printed value; (D) no stale value is left.
Lines of §13 (history) and lines inside code fences are not scanned in (C) and (D). Prints one line per check and a summary."""
import re
import sys

strategy, stdout = sys.argv[1], sys.argv[2]
out = open(stdout, encoding="utf-8").read().split("\n")
src = open(strategy, encoding="utf-8").read().split("\n")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
res = []


def rec(ok, what, info=""):
    res.append(ok)
    print(("OK       " if ok else "MISMATCH ") + what + (" :: " + info if info else ""))


def sci(v, nd=1):
    e = len(str(int(v))) - 1
    m = f"{v / 10 ** e:.{nd}f}"
    if float(m) >= 10:
        m, e = f"{float(m) / 10:.{nd}f}", e + 1
    return m, str(e).translate(SUP)


# ---- the printed table -----------------------------------------------------------------------------------------------------
i0 = next(i for i, l in enumerate(out) if l.startswith("  v9 (W1): day-15 reading"))
i1 = next(i for i, l in enumerate(out) if l.startswith("  |   without an S_CKF estimate"))
tab = out[i0:i1 + 1]
row = lambda key: next(l for l in tab if key in l)
cells = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]
nums = lambda s: [float(x) for x in re.findall(r"\d+(?:\.\d+)?(?:e[+-]\d+)?", s)]
T = {}
c = cells(row("every pilot count zero"))
T["empty"] = [int(x) for x in re.findall(r"\d+", c[1].replace("16-84", ""))]
for key, name in (("Z(nunu) pilot count m_Z, DIF", "mz"), ("DIF pilot count m_D, Z(nunu)", "md")):
    c = cells(row(key))
    T[name] = list(zip([int(x) for x in c[0].split("=")[1].split("/")], [int(x) for x in c[1].split("/")], [x.strip() for x in c[2].split("/")]))
for key, name in (("(alpha1), no credit", "a1"), ("(alpha1'), no credit", "a1p")):
    T[name] = nums(cells(row(key))[1])                      # lo-hi at 0.8, lo-hi at 0.98
T["credit"] = [int(x) for x in cells(row("with fit-probability credit 2/35"))[1].split("/")]
T["grid"], T["base"] = {}, {}
for l in tab:
    m = re.match(r"\s*\|\s+f_D = (\S+)", l)
    if m:
        c = cells(l)
        T["base"][m.group(1)] = [int(x) for x in re.findall(r"\d+", c[1].replace("B50", ""))]
        for part in c[2].split(";"):
            rate, vals = part.rsplit(":", 1)
            T["grid"][(m.group(1), rate.strip()[:5])] = [None if "none" in v else (int(re.search(r"x(\d+)", v).group(1)), re.search(r"\((\d+\.\d)%\)", v).group(1)) for v in vals.split(" / ")]
T["own"] = [int(x) for x in re.findall(r"x(\d+)", row("without an S_CKF estimate"))]
zl = [m for m, b, k in T["mz"] if k == "at the limit"] or [max(m for m, b, k in T["mz"] if k == "below")]
zb, za = max(m for m, b, k in T["mz"] if k == "below"), min(m for m, b, k in T["mz"] if k == "above")
db, da = max(m for m, b, k in T["md"] if k == "below"), min(m for m, b, k in T["md"] if k == "above")
B = {m: b for m, b, k in T["mz"]}
BD = {m: b for m, b, k in T["md"]}
g = T["grid"]
st = next(l for l in out if l.strip().startswith("v9 self-test:"))
rec("ALL PASS" in st, "script self-test line", st.strip())

# ---- (A) verbatim blocks ---------------------------------------------------------------------------------------------------
fen, inside, body = [], False, [False] * len(src)
for i, l in enumerate(src):
    s = l[2:] if l.startswith("> ") else l
    if s.strip() == "```":
        inside = not inside
        body[i] = True
        continue
    body[i] = inside
    if inside:
        fen.append(s)
quoted = [l for l in fen if l in tab or l.startswith("  v") or l.startswith("  |") or l.startswith("  basis") or l.startswith("  (the v6")]
rec(quoted == tab, "(A) fenced blocks equal the printed table, line for line", f"{len(quoted)} quoted lines, {len(tab)} printed")

# ---- text to scan: outside the fences and outside §13 -----------------------------------------------------------------------
h0 = next((i for i, l in enumerate(src) if l.startswith("## 13.")), len(src))
h1 = next((i for i, l in enumerate(src) if i > h0 and l.startswith("## ")), len(src))
live = [(i, l) for i, l in enumerate(src) if not body[i] and not (h0 <= i < h1)]
text = "\n".join(l for _, l in live)
lineof = lambda pos: live[text.count("\n", 0, pos)][0] + 1
norm = re.sub(r"\s+", " ", text.replace("\n> ", "\n"))

# ---- (B) required statements, built from the printed values ----------------------------------------------------------------
a1p, a1 = T["a1p"], T["a1"]
h_lo, h_hi = sci(a1p[0], 0), sci(a1p[3], 0)
req = [
    ("§0 pause, §0 leading sentence, rider: expected reading", f"≈ {h_lo[0]}×10{h_lo[1]}–{h_hi[0]}×10{h_hi[1]}", 3),
    ("§0 pause: (alpha1) reading", f"≈ {sci(a1[0])[0]}×10{sci(a1[0])[1]}–{sci(a1[3])[0]}×10{sci(a1[3])[1]}", 2),
    ("§0 pause: empty reading", f"B₅₀ ≈ {T['empty'][0]} with every pilot count at zero", 1),
    ("§0, §4.4 (three places), §11.7: Z(nunu) limit", f"≈ {zl[0]} Z(νν) pilot counts", 5),
    ("§0, §11.7: DIF limit", f"between {db} and {da} decays-in-flight pilot counts", 2),
    ("Q2 digest: (alpha1') row", f"≈ {sci(a1p[0])[0]}–{sci(a1p[1])[0]}×10{sci(a1p[0])[1]} (ε_pair 0.8) to {sci(a1p[2])[0]}–{sci(a1p[3])[0]}×10{sci(a1p[2])[1]} (0.98)", 1),
    ("Q2 digest: Z(nunu) row", f"{B[zb]} at {zb}, {B[zl[0]]} at {zl[0]}, {B[za]} at {za} | below up to {zb}, at the limit at {zl[0]}, above from {za}", 1),
    ("Q2 digest: DIF row", f"{BD[db]} at {db}, {BD[da]} at {da} | below up to {db}, above from {da}", 1),
    ("Q2 digest: empty row", f"{T['empty'][0]} (16–84 %: {T['empty'][1]}–{T['empty'][2]}) | below", 1),
    ("Q2 digest: (c) credit row", f"| {T['credit'][0]}–{T['credit'][1]} | below", 1),
    ("Q2 (c): credit route", f"B₅₀ {T['credit'][0]}–{T['credit'][1]}) acts on both", 1),
    ("Q2 (c): conversions removed at the central size", f"B₅₀ is {T['base']['1'][0]}–{T['base']['1'][1]}", 1),
    ("Q2 (c): bar at f_D = 0", f"at least ×{g[('0', '0.379')][0][0]} ({g[('0', '0.379')][0][1]} %) [×{g[('0', '0.255')][0][0]}]", 1),
    ("Q2 (c): bar at f_D = 1/4", f"×{g[('1/4', '0.379')][0][0]}–{g[('1/4', '0.379')][1][0]} ({g[('1/4', '0.379')][0][1]}–{g[('1/4', '0.379')][1][1]} %) [×{g[('1/4', '0.255')][0][0]}–{g[('1/4', '0.255')][1][0]}]", 1),
    ("Q2 (c): bar at f_D = e^-1", (f"×{g[('e^-1', '0.379')][0][0]} ({g[('e^-1', '0.379')][0][1]} %) [×{g[('e^-1', '0.255')][0][0]}] at ×e⁻¹ with the pile-up fall ×339; at ×e⁻¹ with the fall ×201 none suffices"
                                   if g[("e^-1", "0.379")][1] is None and g[("e^-1", "0.379")][0] is not None else "<the e^-1 row changed its pattern: rewrite the sentence from the printed row>"), 1),
    ("Q2 (c): without S_CKF", f"×{T['own'][0]}–{T['own'][1]:,}", 1),
]
for what, frag, n in req:
    k = norm.count(frag)
    rec(k == n, f"(B) {what}", f"'{frag}' found {k}, expected {n}")

# ---- (C) scanners: every statement of the family must carry a printed value ----------------------------------------------
gridset = {v[0] for vs in g.values() for v in vs if v} | set(T["own"])
pct = {v[0]: v[1] for vs in g.values() for v in vs if v}
okc = {str(zl[0]), str(db), str(da)}
scan = [
    ("pilot-count limits", r"(?<![\w.,–-])(\d+(?:\.\d+)?)\s+(?:Z\(νν\)\s+|decays-in-flight\s+)?pilot\s+(?:ceiling\s+)?(?:counts|events)\b", lambda m: m.group(1) in okc),
    ("rejection factor with its percentage", r"×(\d[\d,]*)(?:–(\d[\d,]*))?\s+\((\d+\.\d)(?:–(\d+\.\d))?\s?%\)",
     lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x) and pct.get(int(m.group(1).replace(",", ""))) == m.group(3)
     and (m.group(4) is None or pct.get(int(m.group(2).replace(",", ""))) == m.group(4))),
    ("rejection factor in brackets", r"\[×(\d[\d,]*)(?:–(\d[\d,]*))?\]", lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x)),
    ("'at least xN' / 'xN-M' rejection statements in Q2 (c)", r"(?:at least|factor is)\s+×(\d[\d,]*)(?:–(\d[\d,]*))?", lambda m: all(int(x.replace(",", "")) in gridset for x in m.group(1, 2) if x)),
    ("day-15 reading in powers of ten", r"(?:reading is expected at|expected reading is B₅₀|projected B₅₀)\s+≈\s+(\S+)",
     lambda m: m.group(1).rstrip(".,;)") in {f"{h_lo[0]}×10{h_lo[1]}–{h_hi[0]}×10{h_hi[1]}"}),
]
for what, rx, good in scan:
    hits = list(re.finditer(rx, text))
    bad = [(lineof(m.start()), m.group(0).replace("\n", " ")) for m in hits if not good(m)]
    rec(not bad and len(hits) > 0, f"(C) {what}: {len(hits)} statements", "; ".join(f"l.{a}: '{b}'" for a, b in bad) if bad else "")
q0 = next(i for i, l in live if l.startswith("**Q2,"))
q1 = next(i for i, l in live if l.startswith("**Q3,"))
p0 = next(i for i, l in live if "**The pause.**" in l)
p1 = next(i for i, l in live if "**Leading sentence**" in l)
okr = {(T["credit"][0], T["credit"][1]), (T["base"]["1"][0], T["base"]["1"][1])}
hits = [(i + 1, m) for i, l in live if (q0 <= i < q1 or p0 <= i < p1) for m in re.finditer(r"B₅₀\s+(?:is\s+|≈\s+)?(\d[\d,]*)–(\d[\d,]*)(?![\d×]|\.\d)", l)]
bad = [(i, m.group(0)) for i, m in hits if (int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))) not in okr]
rec(not bad and len(hits) > 0, f"(C) B₅₀ ranges in 'The pause' and in Q2: {len(hits)} statements", "; ".join(f"l.{a}: '{b}'" for a, b in bad))

# ---- (D) stale values of earlier versions ------------------------------------------------------------------------------
stale = [r"v8 table", r"budget_stdout_v8", r"≈ 20\s+(?:Z\(νν\)\s+)?(?:pilot|counts in the pilot|in the pilot|ceiling)", r"≈ 13\s+in the pilot", r"pool-equivalent", r"pilot ceiling",
         r"5(?:\.0)?×10⁴–5(?:\.1)?×10⁵", r"5\.0–5\.1×10[⁴⁵]", r"2\.8×10³–4\.8×10⁴", r"401–663", r"B₅₀ 51–74", r"×34\b", r"×23\]", r"×52–81", r"×69–235", r"×35–55", r"×47–159",
         r"U1 line", r"read as rule 1 reads them", r"would suffice", r"×31\b"]
for rx in stale:
    hits = [lineof(m.start()) for m in re.finditer(rx, text)]
    rec(not hits, f"(D) no '{rx}'", "lines " + ", ".join(map(str, hits)) if hits else "")
print(f"text check: {'ALL OK' if all(res) else 'MISMATCH'} ({sum(res)} of {len(res)})")
~~~~

I ran it on a scratch copy of v8 with the eighteen replacements of §5 applied, against the output of §3: **ALL OK, 45
of 45**. On v8 itself it reports 42 mismatches, so it does detect the family (VERIFIED, scratch). The fixer attaches
its full output to the fix report. Cycle 9 reruns it. A sentence added later that restates a number of the table in a
new form must be added to `req`; otherwise it must cite the table and state no number.

---

## 5. Text: every sentence, caption and table of v8 that cites these tables

My sweep started from the critical reviewer's 71 entries and the fixer's 58. Entries that state only the threshold, the
expected pause, the calendar or a Table 4.4c value on its own basis are unchanged; I confirmed each against §2.1. The
entries that change are the eighteen below. They include the three statements the physics reviewer lists (§0 l.98–99 in
T3; the Q2 table l.2805 in T14; Q2 (c) l.2852–2854 in T16). Each "old" string occurs exactly once in v8 (VERIFIED: the
replacements were applied by a program that asserts this). Sentences now cite the table where they can; the numbers
that remain in prose are exactly those of `req` in §4.2.

**T1. §0, item 3 (the (α1) parenthesis)** (v8 l.63).

Old:

~~~~
rows of the v8 table of script [9b]).
~~~~

New:

~~~~
row of the v9 table of script [9b]).
~~~~

**T2. §0, "Expected" paragraph, branch (β)** (v8 l.79).

Old:

~~~~
so the day-15 rule reads the same ceilings as (γ), v8 table of script [9b])
~~~~

New:

~~~~
so the day-15 rule reads it as (γ), through the Z(νν) pilot count, v9 table of script [9b])
~~~~

**T3. §0, "The pause."** (v8 l.91–99).

Old:

~~~~
It reads every no-pile-up term at
  max(zero-count floor, N_t·H) on all own hits before CKF, from the pilot's counts, with no S_CKF, no conditional (no
  veto, no fit-probability credit) and no credit that exists only after the freeze; its DIF and conversion terms are
  therefore expected ×5–50 above the after-CKF figures of this summary (ε_pair assumed 0.8–0.98, not measured, and not
  bounded above). The expected reading is B₅₀ ≈ 5.0×10⁴–5.1×10⁵ by v1's conversion counts ((α1′)) and ≈ 2.8×10³–4.8×10⁴
  even if decays in flight and conversions fell like the pile-up background ((α1)): the pause is the expected branch.
  The reading is below 300 only if the pilot's ceilings are nearly empty: B₅₀ ≈ 75 with every pilot ceiling at zero;
  Z(νν) alone may count up to ≈ 20 pilot ceiling events, or every SM ceiling up to ≈ 60 pool-equivalent counts (≈ 13
  in the pilot) if they scale with Z(νν) ((γ); (β) is read as (γ) at day 15) (script [9b], v8 table). A conversion veto
~~~~

New:

~~~~
It reads every term from the pilot's
  own-hit counts before CKF, at max(zero-count floor, N_t·H) on the samples that exist at day 15: decays in flight and
  nuclear interactions on their own pilot samples, and every SM hard-scatter process and the multijets at the H per
  event of the Z(νν) pilot, with no S_CKF, no conditional (no veto, no fit-probability credit), no credit that exists
  only after the freeze and no pool floor. One Z(νν) pilot count is 18 events and one decays-in-flight pilot count is
  65. Its decays-in-flight and conversion terms are therefore ×5–50 above their after-CKF sizes (ε_pair assumed
  0.8–0.98, not measured, and not bounded above). The expected reading is B₅₀ ≈ 3×10⁴–3×10⁵ by v1's conversion counts
  ((α1′)) and ≈ 2.6×10³–4.2×10⁴ even if decays in flight and conversions fell like the pile-up background ((α1)): the
  pause is the expected branch. The reading is below 300 only if the pilot's counts are nearly zero: B₅₀ ≈ 76 with
  every pilot count at zero; the limit is at ≈ 12 Z(νν) pilot counts, which is also how the rule reads (β) and (γ), or
  between 3 and 4 decays-in-flight pilot counts (script [9b], v9 table). A conversion veto
~~~~

**T4. §0, "Leading sentence"** (v8 l.115).

Old:

~~~~
(projected B₅₀ ≈ 5×10⁴–5×10⁵ on its own-hit basis against a limit of 300)
~~~~

New:

~~~~
(projected B₅₀ ≈ 3×10⁴–3×10⁵ on its own-hit basis against a limit of 300)
~~~~

**T5. §4.4 point 4, S_CKF (Df-9) paragraph** (v8 l.795).

Old:

~~~~
far above the day-15 class (m_H ≈ 125 pool counts for Z(νν) alone; ≈ 20 counts in the pilot, script [9b] v8 table)
~~~~

New:

~~~~
far above the day-15 limit (≈ 12 Z(νν) pilot counts, script [9b] v9 table; in the result, the class B₅₀ = 300 is m_H ≈ 125 pool counts if Z(νν) alone sat at its ceiling)
~~~~

**T6. §4.4 point 5, "Reading of the pilot (fixed now)"** (v8 l.876).

Old:

~~~~
(a pilot zero is a bound of 12 events for Z(νν); with the other pilot ceilings empty, the day-15 class corresponds to ≈ 20 Z(νν) pilot counts (script [9b], v8 table))
~~~~

New:

~~~~
(a pilot zero is a bound of 12 events for Z(νν) itself and of 21 events for all SM hard-scatter processes and the multijets, which the day-15 rule reads through the same count; with the other pilot counts at zero the day-15 limit is at ≈ 12 Z(νν) pilot counts (script [9b], v9 table))
~~~~

**T7. §4.4, caption of Table 4.4c (last sentence)** (v8 l.961–962).

Old:

~~~~
The reading of the day-15 rule, which admits none of these credits, is the v8
table of script [9b], quoted in Q2.
~~~~

New:

~~~~
The reading of the day-15 rule, which admits none of these credits and is computed on the pilot's exposures, not on these pool floors, is the v9
table of script [9b], quoted in Q2.
~~~~

**T8. §4.4, "Scenarios (β) and (γ)"** (v8 l.1010).

Old:

~~~~
and the rule reads the same ceilings as (γ) (§11.7 rule 1; script [9b], v8 table).
~~~~

New:

~~~~
and the rule reads every SM process through the Z(νν) pilot count, as in (γ) (§11.7 rule 1; script [9b], v9 table).
~~~~

**T9. §4.4, "What is not known"** (v8 l.1025–1026).

Old:

~~~~
(B₅₀ > 300 events; m_H ≈ 125 pool counts for Z(νν) alone, ≈ 20 in the pilot; reach ≈ 560 GeV) is the expected
  branch** by v1's conversion counts; the reading of each branch under §11.7 rule 1 is the v8 table of script [9b],
~~~~

New:

~~~~
(B₅₀ > 300 events: at day 15, ≈ 12 Z(νν) pilot counts with the other pilot counts at zero; in the result, m_H ≈ 125 pool counts if Z(νν) alone sat at its ceiling, reach ≈ 560 GeV) is the expected
  branch** by v1's conversion counts; the reading of each branch under §11.7 rule 1 is the v9 table of script [9b],
~~~~

**T10. §11.7 rule 1, first sentence (the clarification of the rule)** (v8 l.2728–2730).

Old:

~~~~
(Tables 4.4a and 4.4c with the
   measured ceilings, the three additions at their MET-model N_trig, DIF and the conversions from the pilot's counts),
   with max(zero-count floor, N_t·H) per term and the pile-up estimate of the development occupancy model (at day 7:
~~~~

New:

~~~~
from the samples that exist at day 15,
   with max(zero-count floor, N_t·H) per term: H is Gamma(m + 1)/M for the own-hit count m of the pilot sample of M
   events, and the zero-count floor is its m = 0 case on that sample, not the Table 4.4a floor of a pool that does not
   exist yet. Decays in flight and each nuclear-interaction radius are read on their own pilot samples (10⁶ events
   each). Every SM hard-scatter process and the multijets (the three additions at their MET-model N_trig) are read at
   the H per event of the Z(νν) pilot (2.3×10⁶ events; one count m_Z for all of them, their conversions included),
   since no other SM sample exists before the freeze. The reading is therefore a function of the pilot counts alone
   (script [9b], v9 table: one Z(νν) pilot count is 18 events, one decays-in-flight pilot count 65). The pile-up term
   is the estimate of the development occupancy model (at day 7:
~~~~

**T11. §11.7 rule 1, basis sentence** (v8 l.2738–2739).

Old:

~~~~
its DIF and conversion terms are therefore expected ×1/(1 − ε_pair) above the after-CKF rows of Table 4.4c
   (×5–50 at the assumed ε_pair = 0.8–0.98; script [9b], U1 line).
~~~~

New:

~~~~
its DIF and conversion terms are therefore expected ×1/(1 − ε_pair) above their after-CKF sizes
   (×5–50 at the assumed ε_pair = 0.8–0.98; the conversions as the Z(νν) pilot counts them, 5.9×10³ events after CKF by
   v1's Z(νν) photon rate against the 6.4–9.5×10³ of Table 4.4c; script [9b], v9 table).
~~~~

**T12. §11.7 rule 1, the (c) test** (v8 l.2744).

Old:

~~~~
candidates demonstrates a rejection of at most ×n/1.14. No credit in the result comes from these estimates.
~~~~

New:

~~~~
candidates demonstrates a rejection of at most ×n/1.14. These factors multiply a counted term, never its zero-count floor. No credit in the result comes from these estimates.
~~~~

**T13. §11.7 rule 1, the class sentence** (v8 l.2746–2747).

Old:

~~~~
on the pilot, ≈ 20
   Z(νν) ceiling counts with the other pilot ceilings empty; the reading of each branch is the v8 table of script [9b])
~~~~

New:

~~~~
on the pilot, the limit is at ≈ 12
   Z(νν) pilot counts with the other pilot counts at zero, or between 3 and 4 decays-in-flight pilot counts; the reading of each branch is the v9 table of script [9b])
~~~~

**T14. §12.1 Q2 stem: basis sentence, digest table, caption and verbatim day-15 block (one span, from "The day-7 and" to the closing code fence)** (v8 l.2796–2829).

Old: the whole span of 34 lines from the words "The day-7 and" in l.2796 through l.2829, the closing code fence of the verbatim day-15 block (the sentence, the six-row table, the caption and the fenced block). New:

~~~~
The day-7 and
day-15 projections read the pilot's own-hit counts before CKF, with no S_CKF and no conditional credit (Df-9, §11.7 rule 1);
their decays-in-flight and conversion terms are ×5–50 above the after-CKF sizes (ε_pair = 0.8–0.98, assumed, not
measured). What the day-15 rule reads (planning EST; a digest of the printed lines below; B₅₀ against the limit 300):

| pilot counts (branch) | day-15 B₅₀ (rule 1) | vs 300 |
|---|---|---|
| (α1′), v1's conversion counts (expected) | ≈ 3.2–3.3×10⁴ (ε_pair 0.8) to 3.2–3.3×10⁵ (0.98) | above |
| (α1), decays in flight and conversions falling like pile-up, no credit | ≈ 2.6×10³–4.2×10⁴ | above |
| Z(νν) pilot count, the others zero; (β) and (γ) are read through this count | 281 at 11, 300 at 12, 317 at 13 | below up to 11, at the limit at 12, above from 13 |
| decays-in-flight pilot count, the others zero | 266 at 3, 331 at 4 | below up to 3, above from 4 |
| every pilot count zero | 76 (16–84 %: 37–152) | below |
| only in the test of a (c) redesign (EST): (α1) with fit-probability credit on decays in flight and conversions | 109–130 | below |

*Day-15 table, printed lines (script [9b], `budget_stdout_v9.txt` l.354–364, verbatim).* Rule 1 (§11.7) reads every term at max(zero-count floor, N_t·H) from the pilot's own-hit counts before CKF, on the samples that exist at day 15 (decays in flight and nuclear interactions on their own pilot samples; every SM hard-scatter process and the multijets at the H per event of the Z(νν) pilot), with no S_CKF, no conditional credit (no veto, no fit-probability credit), no credit that exists only after the freeze and no pool floor; threshold: the study pauses if B₅₀ > 300 events. ESTIMATE, v1 placeholder inputs; the decays-in-flight term rests on 1–2 v1 counts; the ×5–50 between the before-CKF reading and the after-CKF size rests on an assumed pair efficiency (ε_pair = 0.8–0.98, not measured); the pile-up term is the R09 estimate (median 6.7 events; 88–148 at an R08 selection, Table 4.4c). The pilot is small: four decays-in-flight counts alone pause the study. Rows marked (c) exist only in the test of a Q2 (c) redesign (conditional and S_CKF estimated on development samples, EST).

```
  v9 (W1): day-15 reading under §11.7 rule 1, a function of the pilot counts alone (own hits before CKF, no S_CKF, no conditional, no post-freeze credit; the study pauses if B50 > 300)
  basis: events in 3 ab^-1 per pilot count: DIF 65.1 (1e6 events); NI 0.88 / 1.12 / 1.12 (1e6 events per radius); every SM hard-scatter process and the multijets through the Z(nunu) pilot count: 18.1 (= (sum N_t + N_MJ) / 2.3e+06 = 1.66 x Z(nunu)'s own 10.9); pile-up R09 EST median 6.7; no pool floor enters; medians of 20000 draws (seed 7)
  (the v6 (T2) and v7 (U1) lines above are on the Table 4.4c basis: pool floors, conversions of all processes at the photon rate 0.379; they are not the day-15 reading, which is this table)
  | pilot counts (branch) | B50 at day 15 | vs 300 |
  | every pilot count zero | 76 [16-84 %: 37-152] | below |
  | Z(nunu) pilot count m_Z, DIF and NI counts zero; m_Z = 2 / 5 / 8 / 10 / 11 / 12 / 13 / 15 / 20 | 115 / 170 / 226 / 263 / 281 / 300 / 317 / 353 / 445 | below / below / below / below / below / at the limit / above / above / above |
  | DIF pilot count m_D, Z(nunu) and NI counts zero; m_D = 1 / 2 / 3 / 4 / 5 | 138 / 202 / 266 / 331 / 397 | below / below / below / above / above |
  | (gamma), and (beta) at day 15 (its Z(nunu) credit exists only after the freeze): the Z(nunu)-count row; m_H = 10 / 30 / 60 / 100 pool-equivalent counts = m_Z 2.1 / 6.3 / 12.6 / 20.9 | 117 / 195 / 309 / 462 | below / below / above / above |
  | (alpha1), no credit: decays in flight and conversions falling like pile-up; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 31-53, m_D 30-50 | ≈ 2.6e+03-4.3e+03 / 2.5e+04-4.2e+04 (sum of medians) | above |
  | (alpha1'), no credit (expected branch): conversions at their own fall; own hits at eps_pair 0.8 / 0.98 (assumed); expected pilot counts at 0.8: m_Z 1632, m_D 30-50 | ≈ 3.2e+04-3.3e+04 / 3.2e+05-3.3e+05 (sum of medians) | above |
  | (c) only (EST): (alpha1) with fit-probability credit 2/35 (v1's central pile-up fraction; the test takes its 68 % upper value) on decays in flight and conversions (photon rate 0.379), after CKF; x339 / x201 | 109 / 130 | below / below |
```
~~~~

**T15. §12.1 Q2, upside paragraph** (v8 l.2835–2836).

Old:

~~~~
Their day-15 readings are the (γ) and empty-ceiling rows of
the table.
~~~~

New:

~~~~
Their day-15 readings are the Z(νν)-count and zero-count rows of
the table.
~~~~

**T16. §12.1 Q2 option (c): bar, grid caption, verbatim grid and the closing sentence (one span, from "At v1's central decays-in-flight size" to "acts on both.")** (v8 l.2850–2877).

Old: the whole span of 28 lines from the words "At v1's central decays-in-flight size (385–647 events," in l.2850 through the words "acts on both." in l.2877 (the bar, the caption, the fenced grid and the closing sentence; the rest of l.2877, "The veto's rejection has not", stays). New:

~~~~
At v1's central decays-in-flight size (385–647 events,
> resting on 1–2 counts) no conversion rejection suffices: with the conversions removed, B₅₀ is 458–718. The
> conversion rejection needed (script [9b], v9 table; v1's maximum photon rate 0.379, with its N_trig-weighted rate
> 0.255 in brackets) is at least ×44 (97.7 %) [×30] even if the pilot counted no decay in flight, ×75–150
> (98.7–99.3 %) [×51–101] at a quarter of v1's size, and ×114 (99.1 %) [×77] at ×e⁻¹ with the pile-up fall ×339; at
> ×e⁻¹ with the fall ×201 none suffices. A development sample with no surviving conversion among n attributed
> ones demonstrates at most ×n/1.14 (§11.7 rule 1). These factors assume S_CKF estimated for both terms. If S_CKF
> cannot be estimated before the freeze, the factor is ×219–2,186 with no decay in flight in the pilot, and no
> conversion rejection suffices from a quarter of v1's decays-in-flight size on (ε_pair = 0.8–0.98, not measured).
>
> *(c) rejection grid, printed lines (script [9b], `budget_stdout_v9.txt` l.365–370, verbatim).* The smallest conversion
> rejection with which the (c) test reads B₅₀ ≤ 300 (the pause threshold), by the size of the decays in flight (f_D × v1's
> central size; (α1) decays in flight at the pile-up fall ×339 / ×201). Basis: the pilot's transfer factors of rule 1
> (no pool floor); decays in flight and conversions after CKF, as v1 counted them (the (c) test with S_CKF estimated at
> v1's level), their zero-count floors kept without credit; no credit that exists only after the freeze; the rejection
> itself is the (c) test's conditional (EST). The photon rate sets the size of the conversions: v1's maximum over
> processes (0.379), its N_trig-weighted mean (0.255), and v1's Z(νν) rate (0.231), which is what the pilot's count
> would read. ESTIMATE, v1 placeholder inputs; the decays-in-flight term rests on 1–2 v1 counts; a factor is precise
> to about 3 %.
>
> ```
>   | (c) only (EST): smallest conversion rejection with B50 <= 300, by the decays-in-flight size f_D x v1's central size ((alpha1) DIF at fall x339 / x201), decays in flight and conversions after CKF (S_CKF estimated), the zero-count floors kept; conversions at v1's photon rate; a factor is precise to about 3 % |
>   |   f_D = 0 (pilot count zero) | B50 with the conversions removed 76 / 76 | 0.379: x44 (97.7%) / x44 (97.7%); 0.255: x30 (96.7%) / x30 (96.7%); Z(nunu) 0.231 (the pilot's own): x28 (96.4%) / x28 (96.4%) |
>   |   f_D = 1/4 | B50 with the conversions removed 168 / 233 | 0.379: x75 (98.7%) / x150 (99.3%); 0.255: x51 (98.0%) / x101 (99.0%); Z(nunu) 0.231 (the pilot's own): x47 (97.9%) / x93 (98.9%) |
>   |   f_D = e^-1 | B50 with the conversions removed 213 / 309 | 0.379: x114 (99.1%) / none suffices; 0.255: x77 (98.7%) / none suffices; Z(nunu) 0.231 (the pilot's own): x71 (98.6%) / none suffices |
>   |   f_D = 1 (v1's central size) | B50 with the conversions removed 458 / 718 | 0.379: none suffices / none suffices; 0.255: none suffices / none suffices; Z(nunu) 0.231 (the pilot's own): none suffices / none suffices |
>   |   without an S_CKF estimate (own hits; eps_pair 0.8 / 0.98, assumed): f_D = 0: x219 / x2186 at 0.379; f_D >= 1/4: none suffices (decays in flight alone: B50 ≈ 545 or more) |
> ```
>
> As worded, (c) targets the
> conversions; if you choose it, say whether it may also target the decays in flight. At v1's central size (c)
> cannot work otherwise, and the fit-probability route ((α1) with credit, B₅₀ 109–130) acts on both.
~~~~

**T17. §12.1 Q2, optional rider (1)** (v8 l.2884).

Old:

~~~~
(expected to trigger: the day-7 reading is expected at ≈ 5×10⁴–5×10⁵)
~~~~

New:

~~~~
(expected to trigger: the day-7 reading is expected at ≈ 3×10⁴–3×10⁵)
~~~~

**T18. §12.5 point 2 (critical C-7)** (v8 l.2995).

Old:

~~~~
if decays in flight and conversions fall like the pile-up background (Table 4.4c, (α1)).
~~~~

New:

~~~~
if decays in flight and conversions fall like the pile-up background (Table 4.4c, (α1); after CKF, as v1 counted them).
~~~~


**Bookkeeping (the fixer writes these).**
- Header l.1–7: version 9; fixer and time; "after the eighth arbiter verdict ITERATE
  (`review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md`: finding W1)"; status "for verification (cycle 9)
  and then the user's Gate A".
- New §13.8 "Changes since version 8", with this sentence verbatim: "Rule 1 of §11.7 is made single-valued: every SM
  hard-scatter process and the multijets are read through the Z(νν) pilot count, and no pool floor enters; the day-15
  limit in pilot counts is therefore ≈ 12 Z(νν) counts, not ≈ 20. No default, CPU-h, calendar figure or expected-outcome
  number changed; the day-15 table and the (c) grid are recomputed on that basis and quoted from script [9b] v9 lines."
  One row for W1 (T1–T17, script blocks A and B, the text check) and one row for the C items (T18; critical C-5).
- Code reference (l.3112): the fixer's own measured runtime for version 9 (mine: 1 min 15 s, 36 MB) and one line for
  `check_day15_text.py`.
- COM: pointer to version 9; new section "Changes of rows in version 9" with the row "TG-1 (Q2) | §11.7 rule 1 made
  single-valued (W1): SM processes without a day-15 sample are read through the Z(νν) pilot count; day-15 limit ≈ 12
  Z(νν) pilot counts; (c) factors do not multiply a zero-count floor; no status changed".
- `outputs/budget_stdout_v9.txt`; `outputs/FIX_REPORT_cycle8_<name>.md` with the hunk → item map (T1–T18, bookkeeping),
  the sha256, the nine self-test lines and the full output of the text check.

Nothing else in the strategy changes. In particular Table 4.4c, the stdout lines "v6 (T2)", "v7 (U1)" and "class limit
of decision point 2" stay as they are: they are on the Table 4.4c basis, and the printed table now says so.

---

## 6. Adjudication

### 6.1 Structured table

| # | Finding | Source | Their Cat | Final Cat | Rationale |
|---|---|---|---|---|---|
| 1 | W1: the (γ) rows, the (c) credit rows and the (c) grid are not on the basis their captions state | Physics W1; Critical W1; Constructive B-1 | B, B, B | **B** | Case 1 on severity. Case 4 on content: the reviewers contradict each other on the correct numbers (×35 against ×43–46; the grid "is on the (c) test basis with S_CKF" against "must be on pilot exposures") and on the fix (recompute against relabel). I examined the code and rule 1: both descriptions of the code are right, and the contradiction comes from rule 1 (item 2). Fix (i), §3 |
| 2 | Rule 1 is not single-valued: it does not say what a term without a day-15 sample gets, nor whether (c) factors multiply a floor | Arbiter (case 5); implied by Physics §1 against its own row-2 verdict | — | **B** (root cause of 1; one family) | §1.2. Fixed by T10, T12 and the pinned definition |
| 3 | The (α1′) and (α1) "day-15 readings" (5.0×10⁴–5.1×10⁵; 2.8×10³–4.8×10⁴) are the all-process sizes at the maximum photon rate on pool floors, not what the pilot would read (3.2×10⁴–3.3×10⁵; 2.6×10³–4.2×10⁴) | Arbiter (case 5) | — | **B** (same family) | A number shown to the user as "the expected reading" that the rule would not return. No decision changes. Fixed by block A, T3, T4, T14, T17 |
| 4 | Rejection factors from 3,000-draw medians are not reproducible to better than 6–25 %; B₅₀ = 300.0 at 12 counts is on the threshold | Arbiter (case 5); Physics C-2 in part | —, C | **B** (same family: it is why recomputed numbers differ) | §2.3. Fixed by block A (20,000 draws, integer factors that pass, "at the limit", f_D = 1/2 dropped) and self-test 3, 5, 7 |
| 5 | "Every factor ×1/(1 − ε_pair) larger" is wrong for f_D > 0: the decays in flight grow as well | Physics C-1; Critical C-6 | C, C | C, applied | Replaced by a computed line of the grid and a sentence of T16 |
| 6–18 | the other C items | §6.4 | C | C | §6.4 |

Dismissals: none. Every finding is accepted and fixed in this pass.

### 6.2 Family V1 (cycle 7): final status

| finding | status | evidence |
|---|---|---|
| V1-a: (β) listed as avoiding the pause | closed | no live statement; three reviewers. After this fix (β) and (γ) are one row, the Z(νν) count |
| V1-b: "at ×e⁻¹ the conversions alone would suffice" | closed | "would suffice": 0 hits; kept in the stale list of §4.2. The pinned grid shows ×114 or none at ×e⁻¹ |
| V1-c: the (c) bar "×31–52" | closed in form (a printed grid), **open in value: this is W1** | ×34 was on pool floors with the DIF floor dropped; the bar is ×44 [×30] |
| V1-d: the fit-probability credit acts on the decays in flight | closed | Q2 (c) closing sentence; the credit row (now 109–130) |

W1 is the residual of the family and is the only blocking item. Its root cause (item 2) had not been stated before.

### 6.3 Additions O3–O5

- O3 (§0 item 3, after-CKF label on "projected B₅₀ 590–980"): correct and in scope (critical §3, physics #2). Kept; T1
  only renames the table and makes "rows" singular.
- O4 ("U1 line"): was correct for v8. The U1 line is now labelled in the printed table as not being the day-15
  reading, so T11 and T14 cite the v9 table instead and "U1 line" joins the stale list.
- O5 (runtime in the code reference): correct; updated by the bookkeeping.

### 6.4 The fifteen C items

| item | disposition |
|---|---|
| Physics C-1 ("every factor" must include f_D) | applied now: T16 and the last line of the grid |
| Physics C-2 (print factors rounded up) | applied now: block A prints the smallest integer that passes |
| Physics C-3 (pile-up term is the R09 estimate; 88–148 at R08) | applied now: caption in T14 |
| Physics C-4 (one DIF pilot count is 65 events) | applied now: T3, T10, the DIF row of the table, caption in T14 |
| Critical C-1 (S8 inside the parenthesis) | no action; T6 rewrites the parenthesis |
| Critical C-2 (2.8 against the printed 2.85) | moot: the number is replaced; block A prints two significant figures so that the text copies, not rounds |
| Critical C-3 ("below under ≈ 20") | moot: the row is replaced by T14 |
| Critical C-4 (LOG and fix-report wording on O3) | record only; not the artifact. Safe: no reader of the strategy sees it |
| Critical C-5 (script docstring) | applied now: §3.1 |
| Critical C-6 (scope of "every factor") | applied now, with Physics C-1 |
| Critical C-7 (§12.5 point 2 lacks "after CKF") | applied now: T18 |
| Critical C-8 (pool against pilot exposures in the (c) rows) | superseded by fix (i) |
| Constructive C-1 ((c) credit rows on pool floors) | superseded by fix (i): 109–130 |
| Constructive C-2 (say the summary table is a digest; "below up to ≈ 20") | applied now: T14 ("a digest of the printed lines below") |
| Constructive C-3 ("≈ 2.8×10³" rounding) | moot, as Critical C-2 |

Deferred: none. Gate-A package only: none beyond §7.

---

## 7. The Gate-A package (constructive review, part 3): corrections

The structure, the order and every number outside this family stand (I did not find a mismatch against stdout v8
outside the family). The corrections after my rulings, with the corrected sentences:

1. **Sources line:** "STRATEGY v9 (STR), `budget_stdout_v9.txt` (stdout)."
2. **§1 Headline,** last two sentences: "**The day-15 rule is expected to pause the study**: it reads the pilot's
   own-hit counts before CKF, expected at B₅₀ ≈ 3×10⁴–3×10⁵ against 300 (the ×5–50 rests on an assumed pair efficiency,
   not measured). A conversion veto counts only in a Q2 (c) redesign, and at v1's central decays-in-flight size no
   conversion rejection suffices (without conversions B₅₀ is 458–718)."
3. **§1 Upside:** "(310–370 at width 0.17; still pauses: ≈ 2.6×10³–4.2×10⁴ as the rule reads it)" and "(post-freeze; at
   day 15 read through the Z(νν) pilot count, at the limit at ≈ 12 counts)".
4. **§2 Review line:** "Review: cycles 1–8, Category A 11 → 4 → 1 → 0 → 0 → 0 → 0 → 0, Category B 24 → 14 → 15 → 5 → 3
   → 1 → 4 → 1; [cycle 9: …]. Cycles 7–8 corrected which pilot counts pass the day-15 rule and the (c) bar; cycle 8
   made the rule single-valued (every SM process is read through the Z(νν) pilot count: limit ≈ 12 counts, not ≈ 20)."
5. **§3 Q2 stem:** "Rule 1 reads the pilot's own-hit counts before CKF: no S_CKF, no veto or fit-probability credit,
   nothing post-freeze, no pool floor. Every SM process is read through the one Z(νν) pilot count, since no other SM
   sample exists at day 15 (stdout l.354–364)." Then this table, exactly:

   | pilot counts (branch) | day-15 B₅₀ | vs 300 |
   |---|---|---|
   | (α1′) v1's conversion counts (expected) | ≈ 3×10⁴ (ε_pair 0.8) to 3×10⁵ (0.98) | above |
   | (α1) DIF, conversions fall like pile-up | ≈ 2.6×10³–4.2×10⁴ | above |
   | Z(νν) pilot count, the others zero (also (β), (γ)) | 281 at 11, 300 at 12, 317 at 13 | limit at ≈ 12 |
   | decays-in-flight pilot count, the others zero | 266 at 3, 331 at 4 | below up to 3 |
   | every pilot count zero | 76 (37–152) | below |
   | (c) test only: (α1) with fit-probability credit on DIF and conversions | 109–130 | below |

6. **§3 rejection bullets:** "Rejection a (c) conditional needs (stdout l.365–370; pilot basis, S_CKF estimated, photon
   rate 0.379 [0.255]):
   - none suffices at v1's central decays-in-flight size;
   - ≥ ×44 (97.7 %) [×30] if the pilot counts no decay in flight; ×75–150 [×51–101] at a quarter of that size; ×114
     (99.1 %) [×77] or none at ×e⁻¹;
   - all unmeasured; zero survivors among n show ≤ ×n/1.14; without S_CKF ×219–2,186, and none from a quarter of that
     size on."
7. **§7 risk 1:** "Conversions: no reach beyond existing bounds without a demonstrated conversion rejection of
   ≥ 98.7–99.3 % at a quarter of v1's decays-in-flight size (97.7 % only if the pilot counts none; 99.1 % or none at
   ×e⁻¹) plus a reduction of decays in flight."
8. **§7 risk 2:** "Pilot statistics: an empty pilot already reads B₅₀ 76 of the 300; one decays-in-flight pilot count
   adds 65 events and four alone pause the study; 12 Z(νν) counts reach the limit."
9. **§8 Paths:** "under (c), a conversion rejection of ≥ ×44 (×114 or none if decays in flight are e times below v1's
   central size, none at that size) with a reduction of decays in flight".
10. **§9 Files:** STR v9; `budget_stdout_v9.txt`.
11. **§4 Df-9 cell:** unchanged.
12. **Notes for the orchestrator:** fill "[cycle 9: …]" after the cycle-9 arbiter; the family's numbers are checked
    against stdout v9 l.354–370 (3×10⁴–3×10⁵ and 2.6×10³–4.2×10⁴: l.362–363; 281 / 300 / 317: l.359; 266 / 331: l.360;
    76 (37–152): l.358; 109–130: l.364; grid: l.366–370; 458–718: l.369). "Lower edges, other terms at pool floors" is
    dropped.
13. **Length:** the corrections add about 60 words; the cycle-9 constructive reviewer brings the text back to at most
    1,500 words and states the count.

One point is new for the human and must not be cut: corrections 4 and 5 say that the day-15 limit is ≈ 12 Z(νν) pilot
counts because the pilot's count stands for every SM process.

---

## 8. Regression, motivated-reasoning and pressure checks

- **Regression triggers (§6.7):** no validation test, systematic, fit, bin exclusion or comparison exists in a Phase-1
  strategy; none of the five triggers applies. The one "tautological comparison" risk I checked is the self-test: check
  2 ties the table to `pmf_pred`, checks 3 and 7 use an independent seed and draw count, checks 1, 5 and 6 are
  invariants that the v8 code would have failed (pool factors; "20" instead of "12").
- **Motivated reasoning:** every v8 number of this family that differed from the rule's own reading erred in the
  favourable direction (×34 for ×44; "≈ 20" for ≈ 12; 51–74 for 109–130; 401–663 for 458–718; "×69–235" where the
  ×201 fall admits no factor). The fixer did not choose this; it copied the code the cycle-7 verdict ordered. The
  fix report said openly that the rows used pool floors, and the caption did not. The pinned reading is the stricter
  one on every point, and the two remaining leniencies are printed: the credit row uses v1's central fraction 2/35
  where the test takes its 68 % upper value, and the pilot's own photon rate gives a bar 8 % below the 0.255 column.
- **"Will be addressed later":** nothing in this family is deferred.
- **Reviewer pressure:** no reviewer finding was disputed by the fixer. I overrule one reviewer statement with
  evidence: the physics and critical reviewers accepted row 2 of the v8 table ("Z(νν) alone, ≈ 20 pilot counts") as a
  rule-1 reading. §1.2 shows it cannot stand beside the (γ) reading in one rule (242 against 353 at the same pilot
  count).
- **Competing group:** a group reading the strategy would ask how a 2.3×10⁶-event Z(νν) pilot speaks for W and tt̄
  events. The answer is now in rule 1 (the proxy is stated, with its photon-rate caveat), and the staged 4a samples
  replace it after the freeze.

---

## 9. Iteration history, cycle 9, and what is open

| cycle | version | merged A | merged B | verdict |
|---|---|---|---|---|
| 1 | v1 (Brigitte) | 11 | 24 | ITERATE |
| 2 | v2 (Dmitri) | 4 | 14 | ITERATE |
| 3 | v3 (Emeric) | 1 | 15 | ITERATE |
| 4 | v4 (Fiona) | 0 | 5 | ITERATE |
| 5 | v5 (Gunnar) | 0 | 3 | ITERATE |
| 6 | v6 (Ingrid) | 0 | 1 (U1) | ITERATE |
| 7 | v7 (Jules) | 0 | 4 (one family, V1) | ITERATE |
| 8 | v8 (Leopold) | 0 | 1 (W1; items 1–4 of §6.1 are one finding with its root cause) | ITERATE |

This is cycle 8 of the hard cap of 10. I do not pass because it is the eighth cycle, and I do not iterate on taste:
the rule returned two answers for the same pilot count, and the bar shown for option (c) was ×34 where the rule's own
basis gives ×44.

**Cycle 9: form.** A fresh fixer applies §3, §4.2 and §5 and nothing else. Then fresh sessions:

| role | verifies exactly |
|---|---|
| physics | Reads rule 1 as rewritten (T10–T13) and §1.3 of this verdict. Recomputes the table from the formula with its own scratch code (not block A): the empty reading, B₅₀ at m_Z = 11, 12, 13 and m_D = 3, 4, the two own-hit rows, the credit row, and the grid cells at f_D = 0, 1/4, e⁻¹ for 0.379. Agreement means within 1 % for a median and 5 % for a factor (the draws), with "none suffices" where the conversion-free reading exceeds 300. Runs the script and confirms the nine self-test lines. States whether rule 1 is now single-valued |
| critical | `diff` v8 → v9 of the strategy: every hunk is one of T1–T18 or bookkeeping. Script: three changes of §3.1 and the docstring. stdout: sha256 of §3.2, the two hunks, `cmp` of the lines outside them. Runs `check_day15_text.py` and confirms ALL OK; confirms the file equals §4.2. COM: pointer and the one row |
| constructive | Applies §7 to the package, checks every number of the package against stdout v9 l.354–370, gives the final text with its word count, and confirms that the human is told the limit is ≈ 12 counts and why |
| arbiter | PASS if the three confirm; no new adjudication is expected |

Admissible new findings: a regression of this fix, a factual error in a number shown to the user, or a genuine A.
Settled and not to be reopened: the pinned definition of §1.3; the (c) test on development estimates with the ×n/1.14
rule; the default answers Q1–Q5.

**What is open outside the description and definition of the day-15 decision: nothing.** For the record:
- criteria, samples, budget and calendar are untouched: 4,609 CPU-h, threshold 5,992, 60 days (57.8 without the
  pause); the rider 4,616 / 6,001; stdout outside the two tables is byte-identical;
- the expected outcome is unchanged: ≈ 0.7–1.0×10⁴ events after CKF, reach below 243 GeV with the planned width, the
  pause expected;
- the defaults Q1–Q5 and Df-1 to Df-10 are unchanged; Q2 (a) remains the recommendation;
- one decision threshold is restated, and it is part of this family: the day-15 limit in Z(νν) pilot counts, ≈ 12
  instead of ≈ 20, because rule 1 now says how the SM processes without a sample are read. The threshold B₅₀ > 300
  itself is unchanged.

---

## 10. Verdict

**ITERATE.**
- **Category A:** none.
- **Category B:** W1 (§6.1 items 1–4, one finding). Priority for the fixer: §3.1 (script, then compare the sha256 of
  §3.2) → §4.2 (create the text check) → T10–T13 (rule 1) → T14, T16 (Q2) → T3, T4 (§0) → T5–T9 (§4.4) → T1, T2, T15,
  T17 → T18 and the bookkeeping → run the text check until ALL OK.
- **In the same pass:** the C items marked "applied now" in §6.4.
- **Gate-A package:** the constructive reviewer's part 3 with the corrections of §7.
- **After a cycle-9 PASS,** the artifact of record for Gate A is STRATEGY v9 with `COMMITMENTS.md`,
  `budget_stdout_v9.txt` and `src/check_day15_text.py`.
