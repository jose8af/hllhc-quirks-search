# Physics review, cycle 9: STRATEGY v9 (Mireille, 2026-11-14 06:55)

Reviewer: Nadia (physics), fresh session, 2026-11-14 07:25. Role file `agents/physics_reviewer.md` followed (no
methodology spec, no conventions). Scope: the cycle-8 verdict §9 (Margaret) only: rule 1 of §11.7 as pinned, the two
tables recomputed independently, the self-test, the text against the tables, unchanged elsewhere.

Artifact: `outputs/STRATEGY_mireille_2026-11-14_06-55.md` ("v9", "l." = line of v9); previous `STRATEGY_leopold_2026-11-14_05-00.md`
("v8"); `src/strategy_budget.py`; `outputs/budget_stdout_v9.txt`; `src/check_day15_text.py`; `outputs/day15_text_check_v9.txt`.
Read also: `FRAMING.md`, verdict `review/arbiter/STRATEGY_ARBITER_v8_margaret_2026-11-14_06-10.md` (§1–§4, §9, §10),
`FIX_REPORT_cycle8_mireille.md` (claims only), the v1 record `C12FC_v1/background.json` and `bsum_wp.json`.
There are no figures in this artifact (a strategy), so no figure inspection applies.

Computation (einstein, `nice -n 19 python3 -I`, standard library, no git, no sub-agent, one job at a time):
- the script, unchanged: 1 min 16.6 s; output byte-identical to `budget_stdout_v9.txt`, 582 lines, sha256
  `0ca4af15…433d` (the value the verdict §3.2 ordered);
- my own scratch code (scratchpad `nadia_recompute.py`, 1 min 2 s), written from the formulas of verdict §1.3. It reads
  N_trig, the rates and the photon rates directly from the v1 record, not from the script, and uses its own sampler
  (seed 2026, a different draw order). It finds the grid as a root c* (the conversion size at which B₅₀ = 300) and
  then R = G/c*, not by bisection on R. It calls no function of the script;
- a side check (`r08_check.py`): the same reading with the R08 pile-up term in place of R09.

Tags: VERIFIED = recomputed in this session; ESTIMATE = a planning number of the strategy (v1 placeholder inputs).

**Summary.** W1 is RESOLVED. 38 of 38 requested cells agree within tolerance. The self-test gives 8 PASS. The text
checker gives ALL OK (45 of 45). My own reading found no statement that disagrees with the tables. There is no
Category A and no Category B finding. I give four C items. **Approve for execution subject to Gate A.**

---

## 1. The pinned reading of rule 1 (task 1)

### 1.1 What v9 says

Rule 1 (l.2730–2757) now fixes these points:
- the samples: every term is read on the samples that exist at day 15;
- the count: H = Gamma(m + 1)/M, and the zero-count floor is the m = 0 case on that sample, "not the Table 4.4a floor
  of a pool that does not exist yet";
- decays in flight and each NI radius: read on their own 10⁶-event pilot samples;
- every SM hard-scatter process and the multijets: read "at the H per event of the Z(νν) pilot (2.3×10⁶ events; one
  count m_Z for all of them, their conversions included), since no other SM sample exists before the freeze";
- the transfer factors: 18 events per Z(νν) count and 65 per decays-in-flight count;
- the (c) factors: they "multiply a counted term, never its zero-count floor" (l.2753).

Df-11 (l.2949) repeats this reading as an overridable default and points to the alternatives in verdict §1.

### 1.2 Is it sound as a decision rule?

**Yes.** A decision rule must return one number from what exists at day 15.
- The only measured H per SM hard-scatter event at day 15 is the Z(νν) pilot's.
- Pool floors are planned numbers for samples produced after the freeze. Adding them would make the rule depend on a
  production plan, not on a measurement.
- With one count and one Gamma draw, the reading is a function of (m_D, m_22, m_30, m_61, m_Z) and of the pile-up
  estimate alone. VERIFIED: my code reproduces the table from these five counts and the v1 inputs.
- The rule is also physically sensible for the dominant term. Conversions are a feature of every hard-scatter process.
  The alternative reading (i) of verdict §1.2 lets the pilot see only Z(νν)'s 37 % of them, which makes the rule blind
  to most of the leading expected background.

The rule does not take the 1.66 transfer factor from the pilot itself. It depends on the N_trig of Z(ττ), lost-lepton
Z(ℓℓ) and the multijets, which are ESTIMATE until the MET model (day 12). Rule 1 names this ("the three additions at
their MET-model N_trig"). By the script's own ranges (Z(ττ) up to 1.3×10⁶, multijets up to 4×10⁶), K_SM could be up
to about 20.1 instead of 18.1 (+11 %). That moves the limit from 12 to about 11 counts. This is within the stated
ESTIMATE character, so I raise no finding on it.

### 1.3 The assumption about the other SM processes, and the direction of the error

The assumption is that every other SM process, the additions and the multijets have the Z(νν)+jet H per event (own-hit
near-pass sets, conversions included). v1 itself says how far that holds (VERIFIED, `background.json` → `cprime.*.rate.per_process`):

| feature | Z(νν)+j | other processes | consequence for the reading |
|---|---|---|---|
| DIF rate per event | 1.569 | 1.569–1.595 | not relevant: DIF has its own pilot sample, read at the maximum 1.5945 |
| NI rates | 0.0974 / 0.1230 | within 1 % | not relevant (own samples) |
| photon (conversion) rate | **0.2306** | 0.172–0.379; N_trig-weighted mean of the 12 processes 0.2552; mean of the 11 non-Z(νν) processes **0.294** | the pilot under-reads the conversions of all processes: 5,918 events (pilot) against 6,415 at 0.255 (×1.08) and 9,518 at 0.379 (×1.61) |

Z(νν)+jet is also the cleanest of the large processes. tt̄, W and tW events carry more charged particles and photons,
so their non-conversion near-pass H per event is more likely higher than lower. **The direction of the error is
therefore "too lenient"**: by about 8 % on the leading conversion term at v1's weighted rate, and by an unknown amount
(probably upward) for the other features.

How v9 presents this:
- *Stated, in numbers:*
  - rule 1, l.2747–2748: "the conversions as the Z(νν) pilot counts them, 5.9×10³ events after CKF by v1's Z(νν)
    photon rate against the 6.4–9.5×10³ of Table 4.4c";
  - the grid caption, l.2869–2871: the 0.231 column is "what the pilot's count would read".
- *Handled where it matters most:* the (c) test, the only route to a mass reach in the expected case, is quoted in
  Q2 (c) at the stricter 0.379 and 0.255 rates (×44 [×30], l.2857), not at the pilot's own ×28. So the text does not
  understate the (c) bar.
- *Not stated:* no sentence in rule 1, Df-11 or the day-15 caption says in words that the Z(νν) reading is an
  assumption, and that its likely error makes the pause rule slightly lenient.
- *No false claim:* v9 nowhere calls this reading "conservative" or "stricter". The verdict's "stricter reading"
  (§1.2 reason 4) means stricter than reading (i), and it was not copied into the strategy (VERIFIED by grep).

This is an omission of one clause, not a false statement. It does not move a decision: at the expected reading (×10²
above 300) any 8 % is irrelevant, and near the threshold it moves the limit by less than one count. The rule is also a
pre-production gate only, so production measures the real background in either case. → **C-1** (one clause proposed in §6).

### 1.4 Is the consequence "≈ 12 instead of ≈ 20" correctly derived?

**Yes.** VERIFIED:
- 20 × K_Z = 20 × 10.904 = 218.1 events, and 12 × K_SM = 12 × 18.132 = 217.6 events. The same SM content sits on 1.663× the
  transfer factor (K_SM/K_Z = 1.6629, my value from the record).
- My B₅₀ at m_Z = 11 / 12 / 13 is 281.6 / 299.8 / 318.1 (200,000 draws).
- So the crossing is at 12 counts, and 12 is unresolved by the draws (299.8 ± 0.2). The label "at the limit at 12,
  above from 13" (Q2 digest, l.2814) is honest.

The DIF crossing "between 3 and 4" is also right: 268.6 / 333.5.

Two qualifiers that the text gives only in the caption:

1. *The pile-up basis.* The limit holds at the R09 pile-up estimate (median 6.7). The day-15 caption says so
   (l.2819: "the pile-up term is the R09 estimate (median 6.7 events; 88–148 at an R08 selection, Table 4.4c)"). At an
   R08 candidate (pile-up median 118, width 0.43) my side check gives B₅₀ = 291 / 310 at m_Z = 6 / 7 and 243 / 307 at
   m_D = 1 / 2. The limit would then be ≈ 6–7 Z(νν) counts and 1–2 decays-in-flight counts. §0 l.100, §4.4 l.878 and
   rule 1 l.2755 quote "≈ 12" without "at the R09 pile-up estimate". This is correct on its stated basis and stated in
   the caption → **C-2**.
2. *A reading within draw precision of 300.* Rule 1 does not say how precisely the binding B₅₀ is computed, nor what
   happens within the precision of the draws. With v1 inputs, 12 counts give 299.6–300.0 depending on the seed. With
   the real day-15 inputs a tie is improbable, but a binding rule should fix it → **C-3**.

### 1.5 Presentation as an overridable default

Df-11 is labelled "technical; pinned in review cycle 8". It states:
- the reading;
- the consequence, by reference to the row marked "at the limit";
- why it was needed;
- the alternative, with a pointer to verdict §1.

The header and §0 count eleven defaults (l.8, l.141). This is presented correctly. The default's content is not wrong.
What is missing is only the clause of C-1 (assumption and direction), which a user who weighs an override needs.

---

## 2. Independent recomputation (task 2)

### 2.1 Inputs

VERIFIED from the record, against the strategy's values:

| input | mine (from the record) | the strategy's |
|---|---|---|
| K_D | 65.133 | 65.1 |
| K_NI | 0.883 / 1.115 / 1.115 | 0.88 / 1.12 / 1.12 |
| K_SM | 18.132 | 18.1 |
| K_Z | 10.904 | 10.9 |
| pile-up median | 6.740 | 6.7 |
| pile-up cap | 425.5 × Exp(1) | the same |
| (α1) decays in flight | 384.6 / 647.1 | 385 / 647 |
| (α1) conversions | 182.6 / 307.3 | the same |
| conversions at their own fall | 9,517.9 at the record's 0.37863 | 9,527 (the script rounds the rate to 0.379, +0.1 %) |
| Z(νν) conversions | 3,558.9 | the same |
| the same, × K_SM/K_Z | 5,918.2 | the same |

### 2.2 Precision of my numbers

- *Medians.* 200,000 draws. Four independent 50,000-draw medians per key cell scatter by 0.2–0.7 events, so a
  200,000-draw median is precise to about 0.1–0.35 events (≤ 0.15 %).
- *Grid.* Root of B₅₀(c) = 300, 100,000 draws per evaluation, 22 bisection steps on c. The relative precision of a
  factor is 0.3 × 300/c*: 0.4 % (f_D = 0) to 1.4 % (f_D = 1/4, fall ×201).
- *Own-hit rows.* Sums of medians, as in verdict §1.3, so deterministic.
- *Integer factors.* The printed factor is the smallest integer that passes, so I compare my real-valued R with it and
  with its ceiling.

### 2.3 Cell by cell

| # | cell | printed | mine | rel. diff | within tolerance |
|---|---|---|---|---|---|
| 1 | every pilot count zero | 76 [37–152] | 75.9 [36.5–151.3] | +0.1 % | yes |
| 2 | m_Z = 11 | 281 | 281.6 | −0.2 % | yes |
| 3 | m_Z = 12 | 300 (299.6) | 299.8 | −0.1 % | yes |
| 4 | m_Z = 13 | 317 | 318.1 | −0.3 % | yes |
| 5 | m_D = 3 | 266 (265.9) | 268.6 | −1.0 % (−0.97 % on the integer) | yes, at the edge (see below) |
| 6 | m_D = 4 | 331 | 333.5 | −0.7 % | yes |
| 7–8 | (α1′), ε_pair 0.8 | 3.2×10⁴–3.3×10⁴ | 3.158×10⁴ – 3.289×10⁴ | 0 % at 2 s.f. | yes |
| 9–10 | (α1′), ε_pair 0.98 | 3.2×10⁵–3.3×10⁵ | 3.152×10⁵ – 3.283×10⁵ | 0 % | yes |
| 11–12 | (α1), ε_pair 0.8 / 0.98 | 2.6–4.3×10³ / 2.5–4.2×10⁴ | 2,555–4,256 / 2.497–4.198×10⁴ | 0 % | yes |
| 13–14 | credit row ×339 / ×201 | 109 / 130 | 108.2 / 130.2 | +0.7 % / −0.2 % | yes |
| 15–16 | grid f_D = 0, 0.379 (both falls) | ×44 / ×44 | 43.7 (43.8 with the rate 0.379) → 44 | 0 % | yes |
| 17–18 | f_D = 0, 0.255 | ×30 / ×30 | 29.5 → 30 | 0 % | yes |
| 19–20 | f_D = 0, 0.231 | ×28 / ×28 | 27.2 → 28 | 0 % | yes |
| 21–22 | f_D = 1/4, 0.379 | ×75 / ×150 | 74.7 / 150.0 | +0.4 % / 0 % | yes |
| 23–24 | f_D = 1/4, 0.255 | ×51 / ×101 | 50.3 / 101.1 | +1.4 % / −0.1 % | yes |
| 25–26 | f_D = 1/4, 0.231 | ×47 / ×93 | 46.4 / 93.3 | +1.3 % / −0.3 % | yes |
| 27–28 | f_D = e⁻¹, 0.379 | ×114 / none | 114.5 / none (conversion-free 310.9 > 300) | −0.4 % / agrees | yes |
| 29–30 | f_D = e⁻¹, 0.255 | ×77 / none | 77.1 / none | −0.1 % / agrees | yes |
| 31–32 | f_D = e⁻¹, 0.231 | ×71 / none | 71.2 / none | −0.3 % / agrees | yes |
| 33–38 | f_D = 1, all three rates, both falls | none (458 / 718) | none (457.6 / 719.9) | agrees | yes |
| extra | without S_CKF, f_D = 0 | ×219 / ×2,186 | 219.0 / 2,186 | 0 % | yes |
| extra | the same, decays in flight alone, f_D ≥ 1/4 | ≈ 545 | 545 (sum of medians); 554 as a median | 0 % | yes |

**Result: 38 of 38 requested cells within tolerance (1 % on a median, 5 % on a factor). The two extra cells also agree.**

The m_D rows lie low by 0.7–1.0 %, and so do the conversion-free bases that carry decays in flight:

| cell | printed | mine | diff |
|---|---|---|---|
| f_D = 1/4 | 168 / 233 | 169.9 / 235.1 | −1.1 % / −0.9 % |
| f_D = e⁻¹ | 213 / 309 | 214.8 / 310.9 | −0.8 % / −0.6 % |

The cause is the draws, not the formula:
- the script's own independent check (self-test 3, seed 11, 100,000 draws) gives 268.7 and 333.3, the same as mine;
- the table's 20,000 draws all come from one seed-7 stream, so one low fluctuation of the DIF Gamma draws shows in every
  DIF-carrying cell. Its size is ≈ 2.7σ of a 20,000-draw median (σ ≈ 1.0 event at 266).

No classification moves (266/269 below 297, 331/333 above 303), and no factor moves beyond 1.4 %. The f_D = 1/4 base
"168" (−1.1 %) is the only cell just outside 1 %. It was not one of the requested cells, and the text does not quote it
outside the verbatim grid line. → noted in C-4; no finding.

---

## 3. Self-test (task 3)

I ran the script myself: **8 of 8 PASS, "ALL PASS (8 of 8)"**. The bracketed values are identical to verdict §3.2.

Do the checks test what matters?

| # | what it tests | independent of the table code? | would it have caught the cycle-7 defect (pool exposures used where rule 1 says pilot)? |
|---|---|---|---|
| 1 | the transfer factors equal the pilot literals (4.0848e7 × 1.5945 / 1e6; (Σ N_t + N_MJ)/2.3e6), and none equals a pool factor of Table 4.4a | yes for the basis: literals and the pool list, not `d15_gam` | **yes, directly** |
| 2 | three cells against `pmf_pred` on `raw()` inputs | partly: `raw()` is built independently, but the sampler is the same algorithm with the same seed and draw order (it confirms the formula path, not the precision) | yes: a pool-basis table would differ from `raw()` |
| 3 | six cells against seed 11, 100,000 draws | precision only (same function `d15_q`) | no (it is not a basis check) |
| 4, 8 | monotonicity and grid ordering | structural | no |
| 5 | the thresholds 11 / 12 / 13 and 3 / 4 (hard-coded expectations) | a regression guard on the stated limit | yes: under the v8 basis the limit was ≈ 20, so check 5 fails |
| 6 | the own-hit rows equal level/(1 − ε) on top of the empty reading; no S_CKF; Z(νν) conversions = EV_GZ | algebraic, independent of the row code | yes for the conversion basis (EV_GZ × K_SM/K_Z, not 0.379 on pool floors) |
| 7 | each grid factor passes at ×1.1 and fails at ÷1.1 on seed 11 | an independent draw, same function | only for errors larger than 10 % |

The checks therefore guard the *basis* (1, 2, 5, 6) and the *ordering* (4, 8). They would have caught the cycle-7 and
cycle-8 defects: pool exposures (1, 2, 5) and conversions at 0.379 on pool floors (6). What they cannot catch:
- a definition error shared by both paths, for example a wrong K_SM content or a wrong pile-up term. Both use the same
  constants `SM_NTRIG`, `MJ_PLAN` and `PU9`. My independent code, from the record and verdict §1.3, closes that gap;
- a grid factor wrong by 3–10 %, because check 7 brackets at ±10 % while the table claims about 3 %. My recomputation
  shows the factors are within 1.4 %.

Neither gap hides a defect today → C-4 (tighten check 7 to the stated precision; optional).

There is no suspicious agreement. The checks do not pass trivially: check 5 is a fixed expectation that the v8 basis
fails, and check 3 shows the stated precision.

---

## 4. Text against tables (task 4)

### 4.1 The checker

`python3 -I src/check_day15_text.py outputs/STRATEGY_mireille_2026-11-14_06-55.md outputs/budget_stdout_v9.txt`:
**text check: ALL OK (45 of 45)**, 0 MISMATCH. The output is identical to `outputs/day15_text_check_v9.txt` (`diff` empty).

### 4.2 My own reading, beyond the 45 patterns

I read every statement of the family in §0 (l.55–118), §4.4 points 4 and 5, the scenarios and "what is not known"
(l.797, 877–878, 963, 1005–1029), §11.7 rule 1 (l.2730–2757), the defaults Df-9 and Df-11 (l.2947, 2949) and §12.1 Q2
(stem, digest table, caption, upside, (a)/(b)/(c), grid caption, rider; l.2797–2892). I also grepped the non-history
part of v9 (l.1–3023) for every stale v8 value: "≈ 20", "20 pilot", "13 in the pilot", "×34", "×35", "×23", "51–74",
"401", "5.0–5.1", "5×10⁴", "≈ 60 pool", "v8 table", `budget_stdout_v8`.

| statement (line) | table | agrees |
|---|---|---|
| §0: "B₅₀ ≈ 3×10⁴–3×10⁵ … (α1′) and ≈ 2.6×10³–4.2×10⁴ … (α1)" (l.97–98) | 3.2–3.3×10⁴ / 3.2–3.3×10⁵; 2.6×10³ (min at 0.8) to 4.2×10⁴ (max at 0.98) | yes |
| §0: "B₅₀ ≈ 76 … limit at ≈ 12 Z(νν) pilot counts … between 3 and 4 decays-in-flight" (l.99–101) | 76; at the limit at 12; 266 / 331 | yes (basis R09: C-2) |
| §0: "One Z(νν) pilot count is 18 events … decays in flight 65" (l.96–97) | 18.1 / 65.1 | yes |
| §0 leading sentence and rider: "≈ 3×10⁴–3×10⁵" (l.117, l.2892) | (α1′) | yes |
| §0 item 3: "(projected B₅₀ 590–980; (α1); after CKF … the day-15 rule reads this branch on all own hits, (α1) row of the v9 table" (l.62–63) | Table 4.4c after CKF; own-hit row separate | yes; the basis is stated |
| §4.4 l.797: "≈ 3×10² in the pilot (after CKF …), far above the day-15 limit (≈ 12 Z(νν) pilot counts …)" | 326 (stdout l.390) against 12 | yes |
| §4.4 l.878: "a pilot zero is a bound of 12 events for Z(νν) itself and of 21 events for all SM" | 1.14 × 10.90 = 12.4; 1.14 × 18.13 = 20.7 | yes |
| §4.4 l.1012: (β) read through the Z(νν) count, as in (γ) | (γ)/(β) row | yes |
| §4.4 l.1027: "≈ 12 Z(νν) pilot counts …; in the result, m_H ≈ 125 pool counts …" | separate bases, both named | yes |
| §4.4 Table 4.4c (α1) with credit "51–74" (l.978) | Table 4.4c pool basis in the result; its caption (l.963) says the day-15 reading is not this but the v9 table | yes (not a day-15 statement) |
| rule 1: "5.9×10³ … against the 6.4–9.5×10³" (l.2747–2748) | 5,918 / 6,421 / 9,527 | yes |
| rule 1: "≈ 12 … or between 3 and 4" (l.2755–2756) | the table | yes |
| Q2 digest table (l.2812–2817), all six rows | the printed lines | yes |
| Q2 (c): "458–718", "×44 (97.7 %) [×30]", "×75–150 (98.7–99.3 %) [×51–101]", "×114 (99.1 %) [×77] at ×e⁻¹ with ×339; with ×201 none suffices", "×219–2,186", "none … from a quarter" (l.2855–2862) | grid | yes |
| Q2: "four decays-in-flight counts alone pause the study" (l.2819) | 331 at m_D = 4 | yes |
| Q2 upside: "Their day-15 readings are the Z(νν)-count and zero-count rows" (l.2839) | rows 2 and 1 | yes |
| (c) text: "(α1) with credit, B₅₀ 109–130" (l.2885) | 109 / 130 | yes |
| Df-9: basis "own hits, no S_CKF" (l.2947) | rule 1 | yes |
| Df-11: the consequence is the row marked "at the limit" (l.2949) | m_Z = 12 | yes (by reference, no number to go stale) |

**Statements that disagree with the tables: 0.** Statements that lack their basis: none in a strict sense. The pile-up
basis of "≈ 12" is in the caption, not beside each quote (C-2).

### 4.3 Captions

| requirement | day-15 caption (l.2819) | grid caption (l.2864–2872) |
|---|---|---|
| what rule 1 measures | yes: pilot own-hit counts before CKF on the day-15 samples, Z(νν) H per event for all SM, no S_CKF, no conditional, no post-freeze credit, no pool floor | yes: "the pilot's transfer factors of rule 1 (no pool floor)"; decays in flight and conversions after CKF with S_CKF estimated (the (c) test); floors kept without credit |
| threshold | "the study pauses if B₅₀ > 300 events" | "B₅₀ ≤ 300 (the pause threshold)" |
| ESTIMATE on v1 placeholder inputs | yes | yes |
| decays in flight rest on 1–2 v1 counts | yes | yes |
| the ×5–50 rests on an assumed pair efficiency | yes ("ε_pair = 0.8–0.98, not measured") | not in the caption. The main grid rows are after CKF, where ×5–50 does not enter. The own-hit row says "eps_pair 0.8 / 0.98, assumed", and the Q2 (c) text above says "(ε_pair = 0.8–0.98, not measured)" (l.2862). Adequate |

---

## 5. Unchanged elsewhere (task 5)

`diff budget_stdout_v8.txt budget_stdout_v9.txt` gives exactly the two hunks of verdict §3.2:
- `354,376c354,370`: the day-15 table and the grid;
- `396c390,399`: the label line of the v5 (R1) line, then the nine self-test lines.

No other printed value changed (VERIFIED).

`diff` v8 → v9 of the strategy: 33 hunks. Each is one of:
- the header, version and status lines;
- "ten → eleven defaults";
- a day-15 or (c) statement of the family (§0 l.63, 79, 91–101, 117; §4.4 l.797, 878, 963, 1012, 1027–1028; rule 1;
  Q2; the rider);
- Df-11;
- §12.5 point 2 (the C item "after CKF, as v1 counted them", a label only);
- §13.8 (history);
- the code reference (runtime, the checker command).

Untouched (VERIFIED, the lines are outside every hunk):
- the default Q2 (a);
- the expected outcome: "≈ 0.7–1.0×10⁴ events … after CKF, as v1 counted them" (l.67–68, 112–113), and "below 243 GeV"
  with the width 0.17 (l.71, 115, Q2 stem);
- the acceptance criteria;
- the samples;
- the budget and calendar: 4,609 CPU-h, threshold 5,992, 60 days / 57.8 (l.125–137, 2528–2537, 2914).

---

## 6. Findings and judgment (task 6)

**W1: RESOLVED.**
- Rule 1 is now single-valued: one count per pilot sample, one Gamma draw, the transfer factors named, no pool floor,
  and factors never on a floor.
- The tables are on that basis: 38/38 cells VERIFIED independently.
- The text agrees with the tables: 45/45 by the checker and 0 disagreements by my reading.
- The self-test guards the basis.

**Category A: none. Category B: none.**

**Category C (suggestions; none blocks):**

- **C-1 (assumption and direction of the Z(νν) reading).** Add one clause to rule 1 (after "since no other SM sample
  exists before the freeze") and to Df-11. Proposed text:

  > "This assumes that the other processes have the H per event of Z(νν)+jet. By v1's photon rates (0.231 for Z(νν),
  > 0.255 weighted, up to 0.379) the pilot under-reads their conversions by ≈ 8 % (up to ×1.6), and busier processes may
  > have a higher near-pass H, so the rule errs on the lenient side; the (c) test is quoted at 0.255 and 0.379 for this
  > reason."

  Evidence: §1.3.
- **C-2 (pile-up basis of "≈ 12").** Where §0 (l.100), §4.4 (l.878, 1027) and rule 1 (l.2755) quote "≈ 12 Z(νν) pilot
  counts … between 3 and 4", add "(at the R09 pile-up estimate; ≈ 6–7 and 1–2 at an R08 candidate)". Evidence: §1.4,
  my side check.
- **C-3 (precision of the binding computation).** State in rule 1 how many draws the binding B₅₀ uses (for example
  ≥ 10⁵, precise to < 0.3 %), and that a reading within that precision of 300 counts as "above" (pause and ask), the
  side that costs only a question. Evidence: m_Z = 12 gives 299.6–300.0 depending on the seed (§1.4, self-test 2/3).
- **C-4 (draw precision of the DIF rows; self-test 7).** The 20,000 seed-7 draws put every DIF-carrying cell 0.6–1.1 %
  low (§2.3). Optional: raise `D15_ND` for the DIF rows, or note "±1 %" beside the medians. Tighten self-test 7 from
  ±10 % to ±5 %, the precision the caption states as "about 3 %". The stdout would change, so this is for after
  Gate A, if at all.

**Overall: approve for execution subject to Gate A.** There is no blocking item. C-1 is the one I would most like the
human to see, because it is the information needed to judge the Df-11 override. It can be added to the Gate-A package
as one sentence without touching any number.
