# Reach re-estimate with pilot-based backgrounds (Gate A method, v1 placeholder efficiencies)

Tora (executor, Opus 5.5), 2026-11-23 16:36 -05 (`date`). Plan committed before computing: `REACH_REEST_PLAN_tora_2026-11-23.md`
(30afbac). Script `src/reach_reest_tora.py`; output `outputs/reach_reest_tora_2026-11-23.json` (`J`); session log
`logs/executor_tora_2026-11-23_16-31.md`. **Every reach and background number here is an ESTIMATE on v1 placeholder
efficiencies.** No signal file was opened, no v2 signal efficiency was formed or stated, no sealed count was read. The
only signal input is the plan's s95 → reach table that is already inside Gate A's script (`strategy_budget.py` l.654).

## 1. Result

| variant (all at w = 0.17 on the conversion term, as Gate A's headline) | B₅₀ (events) | s95 median [84 %] | **reach, median [84 % edge] (GeV)** | J line |
|---|---|---|---|---|
| **Gate A** (reproduced): conversions 6.4–9.5×10³ + DIF 385–647, SM pool floors | 6,814–10,195 | 1,823–2,725 [2,841–4,204] | **< 243 [< 243]** | 79–151 |
| **LOW**: ρ_γ = 0, DIF at its floor, SM at Gate A's pool floors | 18 | 13.3 [22.1] | **790 [712]** | 175 |
| **CENTRAL**: ρ_γ = 0.057–0.091 × both photon rates (conversions 369–866), DIF at its floor, SM via the pilot's after-CKF pass count 0 | 418–916 | 136–272 [216–424] | **351–444 [293–382]** | 193–247 |
| **HIGH / UL**: ρ_γ = 0.22 (conversions 1,383–2,053), ρ_DIF = 0.064 (DIF 25–41), SM via the pilot's own-hit pass count 11 (before CKF) | 1,963–2,650 | 523–691 [798–1,054] | **< 243–266 [< 243]** | 265–319 |

- Gate A reproduction: the wrapper returns Gate A's four v6 (T1) w = 0.17 rows **exactly** (B₅₀, s95 median and 84 %
  equal to the script's `A1P6` to the last digit; `J` `reproduced_exactly`), and the unchanged script's stdout equals
  `budget_stdout_v9.txt` in all 582 lines (VERIFIED, `J:6-7`).
- The CENTRAL range spans ρ_γ (R05 10/174 → R06 1/11) and the photon rate (0.255 → 0.379): best 444 [382] at
  ρ_γ = 0.057, rate 0.255; worst 351 [293] at ρ_γ = 0.091, rate 0.379. Statistics-only (w = 0): 461–486 [408–429]
  (`J:553, 571`), against Gate A's statistics-only 314–342 [270–297] (stdout l.327-339).
- The LOW row equals Gate A's own "R09-like: floors + pile-up" row (stdout l.300: 790 [712]): with no conversion-led
  term and empty SM ceilings the Gate A method returns its floor-limited reach.

**Reach outlook vs Gate A: more promising, because** the frozen-rule attribution cuts the conversion-led term by ×11–17
(≈ 4–9×10² instead of 0.7–1.0×10⁴), which moves the central ESTIMATE from below 243 GeV to ≈ 350–445 GeV (84 % edge
≈ 290–380); **but** this rests on one source event for ρ_γ, on the "mixed" 60 % of v1's conversion candidates entering
no term, and at the γ upper limit with the pilot's own-hit pass count the reach is back at < 243–266 GeV.

## 2. One substitution at a time (w = 0.17)

| what changes vs Gate A | B₅₀ | reach median [84 %] | J line |
|---|---|---|---|
| conversions × ρ_γ only (0.057 / 0.091; DIF v1 647, SM pool), rate 0.379 | 1,216 / 1,533 | 392 [338] / 347 [291] | 337, 373 |
| conversion-led term × ρ (conversions × ρ_γ, DIF at floor), SM pool | 562 / 878 | 415 [355] / 359 [299] | 355, 391 |
| conversions at the γ UL only (DIF floor, SM pool) | 2,055 | 251 [< 243] | 427 |
| SM via pilot after-CKF pass 0 only (Gate A conversions and DIF) | 10,191 | < 243 [< 243] | 409 |
| SM via pilot own-hit pass 11 only (no conversion term, DIF floor) | 520 | 362 [293] | 445 |
| CENTRAL but DIF kept at Gate A's v1 size (647) | 1,244 / 1,563 | 388 [331] / 347 [288] | 481, 517 |
| CENTRAL but SM via the after-CKF near-pass count 17 (a lower bound) | 1,338 / 1,664 | 296 [< 243] / 277 [< 243] | 463, 499 |

The reach is set by the conversion term; the SM term matters once it is read on own hits (11 counts ≈ 460 events) or on
near-passes (17 counts after CKF ≈ 710 events). The DIF choice moves the central reach by ≤ 30 GeV.

## 3. Inputs

**Substituted (background only):**

| input | Gate A | here | source |
|---|---|---|---|
| ρ_γ, frozen j ≥ 4 / v1 C′_PU rule | 1 (v1 counts) | 10/174 = 0.057 (R05), 1/11 = 0.091 (R06); low 0 (37 % of replicas); UL 4.74/22 = 0.22 | `CPU_ATTRIB_eskil_2026-11-19.md` l.42-43, l.52-53 [VERIFIED counts, UL ESTIMATE] |
| ρ_DIF | 1 | 0 (0/141 at R05) → DIF at its pool floor (projection rule max(floor, N·H), stdout l.384); UL 3.0/47 = 0.064 | Eskil l.12, l.39 |
| NI | — | not moved (ρ_NI 0.024, UL 0.13; < 2 events) | `CPU_ATTRIB_NI_kari_2026-11-23.md` l.10-13, l.68-72 |
| attributed total (check) | 0.7–1.0×10⁴ | 369–866 central; 1,408–2,094 at the UL (Kari: ≈ 4–9×10², UL ≈ 2.2×10³) | Kari l.71-72; `J` rows |
| SM (all processes + multijets via the Z(νν) count, Df-11) | pool floors, 7.98 events summed (`J:76`) | pilot term 41.96 events per count × Γ(m+1); m = 0 (after-CKF pass, central), 11 (own-hit pass, high); pool floors kept for LOW | per count: M = 993,887 (Tove `RULE1_PRELIM_tove_2026-11-19.md` l.51-52; Ingvild `RULE1_VALID_ingvild_2026-11-23.md` l.25), 41.961 recomputed from the script's N_t (VERIFIED, `J:9`); counts R08: own-hit P 11 (`rule1_prelim_counts_tove_2026-11-19.json` l.490-501, Tove l.16, l.46), after-CKF P 0 and N 17 (json l.1010-1022, l.1036-1048; Tove l.57-59) [VERIFIED read] |

The SM pool floors and the multijet floor are removed when the pilot term enters (it stands for all of them, Df-11).
A counted pilot term (m > 0) is a log-normal around 41.96 (m + 1) with width √(w² + 1/(m+1)), the form of Gate A's Z
ceiling row (`strategy_budget.py` l.827); m = 0 is the zero-count floor Γ(1), as Gate A's floors.

**How the rule-1 counts were used, and why.** The rule-1 B₅₀ (10,777 finder near-pass; 63,170 subset pass) is a
**ceiling** on own hits before CKF, near-pass inclusive (H = P_geo + Σ f_k), with no S_CKF and no conditional; the
advisor rulings say it is not a background estimate (LOG 19 Nov 15:24 Åsa, 15:37 Dagny; Tove l.72-73). It is the
day-15 pause test, not the selected background. So no variant uses the near-pass or subset-pass counts as background.
The pilot enters through its **pass** counts: after CKF (0 at R08; the like-for-like reading of Gate A's after-CKF
v1 conversion counts) for CENTRAL, and before CKF on own hits (11) as the HIGH reading. Information only: reading the
rule-1 ceilings as if they were background gives B₅₀ ≈ 1.1×10⁴ / 6.4×10⁴ and reach < 243 GeV (`J:607, 625`); this
states what the ceiling implies, not an expected reach. The rule-1 verdict ("above 300", expected pause) is untouched.

**Kept unchanged from Gate A** (`strategy_budget.py`, values in `J:8-76`): one-bin expected CLs limit from the
predictive pmf (`pmf_pred`, `s95_pmf`, `quant_pmf`; 3,000 draws, seed 7); reach from the plan's σ_ln = 0 row
(`PLAN_REACH`/`MAPR`/`reach_of`, l.654-663; s95 621.5 ↔ 243 GeV is its last point, beyond it "< 243"); v1 placeholder
signal efficiencies (inside that table only); normalisation width w = 0.17 on the conversion term with the count width
√(w² + 1/(m+1)), m = g/κ_Z, κ_Z = 2.282 (l.791, l.812); pile-up term PU9 (R09 EST median 6.74, s_tot 0.59, cap
N_trig/96,000 × Exp(1); l.690); DIF pool floor κ_DIF = 2.668 and NI pool floors (0.79 summed); v1 (α1′) sizes 9,527
conversions and DIF 385 / 647 before scaling, DIF falls ×339 / ×201 (l.720-727); photon rates 0.379 / 0.255 (l.790);
N_trig 4.0848×10⁷.

## 4. Caveats (all sharpen the ESTIMATE label)

1. **ρ_γ rests on one source event** (Eskil l.14-15, Kari l.73); 37 % of the bootstrap replicas give ρ_γ = 0, the
   95 % UL is 0.22. The width w = 0.17 + count width does not carry this; the LOW / CENTRAL / UL rows do.
2. **Attributed is not selected.** 60 % of v1's γ (28 % of V⁰) candidates become "mixed" under the frozen rule: no term,
   bounded only by the completeness test (STR l.751-752; Eskil l.90-95; Kari l.74-76). Gate A's 0.7–1.0×10⁴ stays an
   **upper envelope** (LOG 19 Nov 15:37), and Gate A's < 243 GeV the reach at that envelope.
3. The SM term is read on the pilot (≈ 10⁶ effective events, 41.96 per count); the final pool would give a smaller
   floor (LOW row). The after-CKF counts are information-only lower bounds (variant 1 run only on events with a
   variant-0 candidate, Tove l.57-58), and "41 per count" is provisional until the day-12 MET model (EXPLORATION §9).
4. v1 placeholder efficiencies are ×1/0.87 high (GATE_A.md l.17); the pile-up term is v1-based (EST).

## 5. Compute
One run on schrodinger (nice 15, 1 slot; SLOTS.md 16:33 / 16:35): 97.7 CPU-s (user + sys), max RSS 45 MB, 1 min 47 s
wall (`/usr/bin/time -v`) [VERIFIED] = **0.03 CPU-h**. Unchanged script stdout: `logs/reach_reest_script_stdout_tora_2026-11-23.txt`.
Rerun (from `analyses/quirks_v2`, any worker): `.pixi/envs/default/bin/python -I phase2_exploration/src/reach_reest_tora.py <json> <stdout.txt>`.
