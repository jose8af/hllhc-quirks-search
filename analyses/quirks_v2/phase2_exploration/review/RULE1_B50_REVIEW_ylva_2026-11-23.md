# Independent re-derivation of the rule-1 B₅₀ from the subset-pass counts, and the single M of the Z term

Ylva (Fable 5.2, reviewer, rule 1(c)), 2026-11-23 19:50 -05 (`date`). Advisor ruling Vigdis, LOG.md l.1003, item 3(a).
I wrote or ran none of the scripts reviewed. My script: `src/review_ylva_b50.py` (sha256 f77cb6a9…; standard library
only; imports no study script; 19.7 CPU-s on einstein, nice 19, 211 MB). Output `J` = `review/rule1_b50_review_ylva_2026-11-23.json`.
Tags: VERIFIED = re-derived by me (file:line or `J` key); ESTIMATE; UNVERIFIED = transcribed.
No signal file, no pilot event file and no sealed count was read; no efficiency was formed.
Short names: `BUD` = `phase1_strategy/src/strategy_budget.py` (sha256 548b5ba8…, = the copy the addendum executes);
`P2Z` = `src/p2z_addendum1.py`; `C`, `B` = Ingvild's `rule1_valid_{c,b50}_ingvild_2026-11-23.json`; `STR`, `ADD` = the
frozen strategy and addendum 1 v5.

## Verdict

**B₅₀ arithmetic CONFIRMED.** All eight readings (S and F × four T2 candidates) are reproduced within the Monte-Carlo
error of the published medians; the largest difference is −3.9 events of 63,294 (6×10⁻⁵, 0.5 σ). **No reading is
near 300**: the smallest B₅₀ is 62,035 (F, R09) against the limit 299.1, and the smallest of my 10⁶ single draws is
53,824 (F) / 55,783 (S). **Single M of the Z term: 993,885.9 (Björn's)**; replacing 993,887.3 by it moves every B₅₀
by +0.09 events, nothing beyond rounding.

## 1. B₅₀ [VERIFIED]

Rule as frozen: B = Σ_t (N_t/M_t)·Gamma(m_t + 1) + min(med·e^{s·g}, cap·Exp(1)), median of ≥ 10⁵ draws, a reading
≥ 300·(1 − 0.003) = 299.1 pauses (STR l.2730-2757, l.2949 Df-11; ADD l.597-609).

| | R09 [16–84 %] | R08 @ 88 | R08 @ 118 | R08 @ 148 |
|---|---|---|---|---|
| **(S), m_Z = 1,501** — Ingvild (10⁵ draws, MC error 6–7; `B:109,146,183,220`) | 63,170 [61,578–64,802] | 63,246 | 63,271 | 63,294 |
| mine, part C: 10⁶ independent draws (MC error 1.9–2.2) | 63,167 [61,563–64,797] | 63,244 | 63,268 | 63,290 |
| mine, part B: 10⁵ draws, three Gamma seeds | 63,166 / 63,174 / 63,172 | 63,242–63,251 | 63,267–63,275 | 63,289–63,296 |
| mine, part D: closed form, no random numbers | 63,169 | 63,245 | 63,269 | 63,292 |
| difference C − Ingvild (in σ of the two MC errors) | −2.5 (−0.4) | −2.7 (−0.4) | −3.3 (−0.5) | −3.9 (−0.5) |
| **(F), m_Z = 1,474** — Ingvild (`B:529,566,603,640`) | 62,037 [60,460–63,654] | 62,113 | 62,138 | 62,161 |
| mine, part C | 62,035 [60,443–63,657] | 62,113 | 62,136 | 62,158 |
| mine, part D | 62,036 | 62,112 | 62,136 | 62,159 |
| difference C − Ingvild (σ) | −1.6 (−0.3) | −0.8 (−0.1) | −2.0 (−0.3) | −2.2 (−0.3) |

(`J` `comparison`.) The 16 % edge differs by −15 / −16 events (S / F): 1.9 σ of one fluctuation that her S and F
readings share (same generator state); 0.02 % of the edge, no effect on any statement.

How each part was done:
- **A, constants and streams.** The empty pilot (every m = 0, planned M) with the addendum's random streams
  re-implemented in my script gives 160.8102 / 238.3145 / 262.2589 / 283.8006: equal to `B` `empty_check` to 6×10⁻¹⁴
  and to the approved row `addendum1_v4_stdout.txt` l.66 (160.8; 238.3 / 262.3 / 283.8). My N_t agree with `B` `N_t`
  to 3×10⁻¹⁵. This fixes every N_t, the planned M and the four pile-up rows bit for bit.
- **B.** Floors on those streams, Gamma(m) from Python's generator instead of numpy's.
- **C.** Different seed, Gamma(m + 1) drawn directly, 10⁶ draws; nothing shared with Ingvild's run but the constants.
- **D.** mean − κ₃/(6σ²): Z term 41.9611 × 1,502 = 63,025.6; nine floors 119.1; 0.05 class 2.1409 × 14 = 30.0;
  pile-up mean 7.9 (R09; 84.6 / 108.7 / 131.0 at R08) by quadrature; skewness term 13.98; σ = 1,627.

Inputs (line numbers found by the script, `J` `cited`; the script stops if the cited text is not on the line):

| input | value | source |
|---|---|---|
| m_Z, m of the 0.05 class, every other term | 1,501 (S) / 1,474 (F); 13; 0 | `C:360-361` (S), `C:760-761` (F); tables at `C:351`, `C:751` [taken as given, see §3] |
| N_t(Z) = 12 SM processes + Z(ττ) + Z(ℓℓ) lost + multijets | 41,704,631.6 | `BUD` l.75-77, l.83, l.86, l.87; `P2Z` l.142 |
| M of the Z term (as used by Ingvild) | 993,887.34 → 41.9611 events per count | `rule1_prelim_counts_tove_2026-11-19.json` l.28, l.60 |
| 0.05 class | N_t(Z) × 0.05/0.98 / M = 2.1409 per count | `P2Z` l.57, l.153 |
| N_t of the seven B1 classes (minimum-bias share) | N_trig × 200 × 0.340513 × count / 1.5×10⁶ = 1.038×10⁸ … 4.79×10⁶ | `BUD` l.68; `P2Z` l.132-137; `partition_p2-c-part-0.json` l.4, l.15, counts l.85-157 |
| hard-scatter term | Σ N_t × (F_HS − 1) = 7.93×10⁶, F_HS = 1.5945/1.560 | `P2Z` l.59, l.138 |
| M of B1 / hs | 4, 4, 1, 1, 1, 4, 2 ×10⁶; 2×10⁶ | `P2Z` l.140, l.72 |
| pile-up R09 | median 6.740 = ½(R08 falls ×339, ×201) × 2/35; width 0.59 | `BUD` l.671-675, l.686, l.690 |
| pile-up R08 | medians 87.9 / 117.9 / 148.0; width 0.43 | `P2Z` l.60, l.190 |
| cap | N_trig/96,000 = 425.5 × Exp(1) | `BUD` l.678, l.886 |
| limit | 300 × (1 − 0.003) = 299.1 | `P2Z` l.67, l.191; STR l.2757 |

Flagged-event variants: only the M of five B1 / hs / low-pT terms change (by ≤ 5×10⁻⁵), all with m = 0: ≤ 0.003
events [ESTIMATE from `B` `events_per_count`]; consistent with Ingvild's "identical".

## 2. The single M of the Z term [VERIFIED]

**993,885.9 (Björn) is right; 993,887.3 (Tove) is high by 1.42 (1.4×10⁻⁶).** Definition: M = Σw/w_max of the
full-weight class (ADD l.337-338, l.607); nothing in it rounds the weights.

- Tove's value is reproduced exactly from the `w_hist` tables of the 61 classified outputs (weights rounded to four
  decimals, `p2t_classify.py:168`): 974,009.5933 / 0.98 = 993,887.3401 (`J` `M.M_rounded_hist`).
- Independent of Björn's script: the pilot writer stores its own unrounded Σw per file (`p2x_hs0.py:211`
  `sum_w_v1`, carried in the classified `meta`). Over the 460 files it is 974,402.4807 (`J` `M.sum_w_writer`);
  Björn's full + low sums equal it to 1×10⁻⁹. The rounded histogram total is 1.4001 above it.
- Rigorous bound without reading an event file: exact Σw(full) = writer total − Σw(low), and Σw(low) = 394.2875
  ± 0.405 (8,095 events, rounding error ≤ 5×10⁻⁵ each). Hence **M ∈ [993,885.50, 993,886.32]**: contains Björn's
  993,885.924, excludes Tove's 993,887.340. Class sizes 994,446 / 8,095 / 1,297,459 and w_max = 0.98 agree.
- Effect: events per count 41.96113 → 41.96119; **every B₅₀ +0.09 events** (same 10⁶ draws, `J` `shift_bjorn_M`).
  Quoted values unchanged (63,170; 62,037; 41.96 per count; "M = 993,887" becomes "993,886").

Recommendation: the binding text quotes M = 993,885.9 (source `review_bjorn_zdenominator_2026-11-19.json` l.17); any
script that carries 993,887 (`reach_reest_tora.py:54`, `reach_reest_mixed_tora.py:37`) need not be re-run.

## 3. Observations (none changes the verdict)

1. **Not covered here:** the counts m themselves (Nils reviewed R08, s = 0); the N_2S2 ≥ 3 candidates (no pile-up
   estimate, no B₅₀ exists to check; 969 / 846 counts); Ingvild's numpy Gamma stream bit for bit (no numpy on
   einstein; parts B–D make it unnecessary). `p2t_rule1_prelim.py` l.38-59 read: it does what its docstring says.
2. **Unweighted m against weighted M** (Björn D4), not evaluated on the subset count: m is an event count, M is
   Σw/w_max. Full-class weights are 0.9739–0.98, so a weighted m is lower by at most 0.62 % (≤ 390 events of
   63,170) [ESTIMATE, bound]; on the finder count it was 0.06 %. Lowering, far from 300.
3. **0.05 class** read at 2.1409 per count (measured M) where the addendum prints 2.10 (planned M) (Björn D6):
   0.5 event.
4. **Measured or planned M** (Tove A4, open): with the planned 1,011,080 the readings are 62,095 (S) / 60,982 (F)
   at R09 (`J` `ylva_C_planned_M`), −1.7 %. The choice does not touch the verdict.
5. What would bring a reading to 299.1: m_Z ≈ 3 at R09 (ADD: pause at 4 counts), i.e. the count would have to be
   wrong by a factor ≈ 400.

## 4. Limits

The check is of arithmetic: constants, formula, draws, quantiles. It says nothing on whether 1,501 is the right
count, on the pile-up estimate itself (v1-based rows, ESTIMATE as physics) or on the open reading questions S1–S5.
