# Critical review: Phase 1 STRATEGY v5 (quirks v2), review cycle 5

Reviewer: Hedwig (critical), 2026-11-14 01:25. Fresh to this panel. Role and template: `agents/critical_reviewer.md`
(adversarial stance, show the work, A/B/C). Rules: `AGENT_RULES.md` (light standard-library `python3 -I`, niced, on
einstein; no sub-agents, no git writes). Session log: `phase1_strategy/logs/critical_hedwig_2026-11-14_01-25.md`.

**Artifact.** `phase1_strategy/outputs/STRATEGY_gunnar_2026-11-14_00-50.md` ("v5", 2,943 lines), `COMMITMENTS.md`
("COM"), `phase1_strategy/src/strategy_budget.py` ("script"), `outputs/budget_stdout_v4.txt` / `_v5.txt`.
**Reference:** cycle-4 arbiter verdict `STRATEGY_ARBITER_v4_greta_2026-11-14_00-25.md` ("AV"), its §6 work list and §9 scope.
v4 = `STRATEGY_fiona_2026-11-13_23-05.md`.

**Scope (AV §9).** Verify R1–R5 and the adopted C items; full diff check v4 → v5; numbers; headline and Gate-A
consistency; final completeness sweep. New findings only for regressions, factual errors in numbers shown to the
user, or genuine A.

**Verdict of this review: 0 Category A, 0 Category B, 7 Category C.** R1–R5 RESOLVED; all adopted C items RESOLVED;
no unattributed hunk in the strategy, COM or the script; the script output differs from v4 only in the ordered values.

---

## 0. What I ran (evidence base)

| check | command / source | result |
|---|---|---|
| fresh script run | `nice -n 19 python3 -I src/strategy_budget.py` (16.5 s) → scratchpad `fresh.txt` | `diff budget_stdout_v5.txt fresh.txt`: **identical** |
| v4 → v5 output | `diff budget_stdout_v4.txt budget_stdout_v5.txt` (102 diff lines) | §2.3 below: only R5 totals and their consequences, R3 storage, R1 [9b] rows and mapping, G-C14 line |
| strategy diff | `diff STRATEGY_fiona… STRATEGY_gunnar…` (64 hunks) | §2.1 |
| COM, script diff | `git diff HEAD~1 -- COMMITMENTS.md strategy_budget.py` (read-only) | §2.2 |
| own R1 arithmetic | scratchpad `hedwig_check.py`, `hedwig_check2.py` (script loaded by `runpy`, its own `pmf_pred`, `s95_pmf`, `s95_fixed`, `rfmt`; independent Poisson tails) | §1, R1 |
| v1 record | `AN1/background.json` → `cprime.gamma.rows`, `cprime.dif.rows`, `cprime.gamma.rate`, `cprime.dif.rate` | §1, R1 |
| PLAN | `publication_plan.tex` l.112–124 (reach table), l.494–509 (outcomes) | 10⁵ column = 243 GeV (σ_ln = 0); σ_ln = 0.2: "--" (below 200) at 10⁴ |
| brief | `prompt.md` l.79 (D6), l.341–348 (§7 stop list) | quoted verbatim in v5 §11.6 l.2644–2653 |
| fix-report phrases | every quoted grep phrase of `FIX_REPORT_cycle4_gunnar.md` §1 tested as substring of v5/COM/script/stdout | 52 / 52 present (one spans the `> >` blockquote markup of Q3) |

---

## 1. R1–R5: status

### R1 — the honest headline: **RESOLVED**

**Recomputation from the v1 record (VERIFIED, my run).**
- `cprime.gamma.rows`: R04 153/500, R05 86/500, R06 13/500, R07 = R06 × p(R07|R06) = 2/13, R08 0/13, R09 2/13.
  `cprime.dif.rows`: R04 166, R05 81, conditionals 2/81 (R06), 1/81 (R07), 0/81 (R08). Matches v5 §0 point 3 and Table 4.4b.
- Measured conversion falls: 86/13 = ×6.6, 13/2 = ×6.5. Pile-up falls from the script: 0.2470/r07 = ×338.7 and
  49.72/0.2470 = ×201.3.
- Pile-up-like fall from 13 at R06: μ(R07) = 0.0384 / 0.0646; P(≥ 2) = **7.18×10⁻⁴ / 2.00×10⁻³** (my own Poisson
  tail, `1 − Σ_{k<2}`). From 86 at R05: μ(R06) = 0.254 / 0.427 against 13 seen (script: P = 2.3×10⁻¹⁸ / 1.7×10⁻¹⁵).
  DIF from 2: P(≥ 1) = 0.59 % / 0.99 %. All identical to script line "v5 (R1) conversion fall test".
- Size: N_trig 4.0848×10⁷ × 0.379 × 2/500 = 6.19×10⁴ conversions at R07; /6.5 = **9,527** at R08 (R09 = R08, no
  credit); DIF 1.30×10⁵/338.7 = 385, /201.3 = 647. Sum with floors and pile-up: B₅₀ = **9,929 / 10,193**.
- Reach (script functions): s₉₅ median 352.2 / 360.6 → **317 / 314 GeV**; 84 % s₉₅ 494.7 / 505.3 → **273 / 270 GeV**;
  fixed B s₉₅ 196.6–199.3 → **394 / 392 GeV** (my call with the rounded B₅₀ 9,929 gives 197.0 → 393; difference only
  from rounding of B₅₀). The arbiter's "394 / 391" vs the script's "394 / 392": the fixer correctly quotes the script.
- Extended mapping: `MAPR` now ends `(621.5, 243)`; the PLAN 10⁵ column is 243 (PLAN l.121). Values above 393 GeV are
  unchanged (v4/v5 output diff shows no change in any pre-existing reach row other than the two "< 393" (α2) rows).

**Text against AV §5–§7 and §6 R1 points 1–8.**
| AV item | v5 location and quoted phrase | check |
|---|---|---|
| §5.1 §0 point 3 | §0 l.55–61 "The conversions fell by ×6.6 and ×6.5 per width step (86 → 13 → 2) … ≈ 9.5×10³ events at R08–R09 … (scenario (α1′), Table 4.4c)" | verbatim; numbers = printed |
| §5.2 "Expected" | §0 l.63–89 "≈ 10⁴ events, with a reach of ≈ 270 GeV at the 84 % edge (median ≈ 315 GeV; ≈ 390 GeV if that background were known exactly, below 200 GeV if it carries a systematic width of 0.2, PLAN l.122)" | verbatim; label "ESTIMATE, v1 placeholder efficiencies; every reach number rests on them" |
| leading sentence | §0 l.91–94 "**Leading sentence** … ≈ 270 GeV at the 84 % edge (median ≈ 315; ≈ 390 GeV if the background were known exactly), and the day-15 rule is expected to pause the study before production." | verbatim to AV §5.2 |
| 1 (script [9b]) | `PLAN_REACH` + `(1e5, 243.0)`; two `alpha1'` tags; `row(..., pred=True)`; fixed-B print; e^(±1) and log-normal lines; m_H = 1000 `row()`; fall-test print; HEADLINE v5 line | all present and printed (stdout l.285–327) |
| 2 (Table 4.4c) | l.943 m_H = 1000 "2,229 / 2,299 / 2,373 \| 0.03 \| 168 [119, 237] \| 415 [369]"; l.944 (β) "(at its floor); conditional on the promotion model being submitted"; l.947 "v1's **pile-up** fit-probability fraction 2/35 … p(R09 \| R06) is 2/13"; l.948 e^(±1) row "571–535 / 437–400 [519–486 / 390–355]"; l.949 (α1′) "317–314 [273–270]; ≈ 390 (394–392) at fixed B"; l.950 credit "332–331 [250]"; l.951 (α2) "262 (fixed B, an upper edge of the reach)"; l.952 "below 243" | each = printed value (stdout l.305, 316–325) |
| 3 (scenario text) | l.959–962 "For the conversions that fall is measured on two independent steps … rejected at p ≈ 10⁻³"; l.965–967 "which acts on the level of the counts rather than on their ratio"; l.968–974 "This is a planning uncertainty of the size … a median reach of 262 GeV (pile-up fall ×339) and below 243 GeV (×201) … statistics-only … below 200 GeV (PLAN l.122)" | log-normal values = stdout l.326–327 (262; < 243) |
| 4 (Df-9 EST, pilot reading) | l.770–773 "m_H ≈ 1.6×10³ for Z(νν) at R08 (≈ 3×10² in the pilot)"; l.852 "(pile-up fall; ≈ 3×10² if the conversions keep v1's fall)" | script: 3.56×10³ events, m_H 1.56×10³, 326 in pilot; `GZ` = 0.23059926668409783 equals `cprime.gamma.rate.per_process.Znunu_j` (read by me) |
| 6 (§11.7 rule 1) | l.2702–2703 "By v1's own conversion counts (scenario (α1′) of Table 4.4c) this is the expected branch; what follows is Q2." | verbatim |
| 7 (Q2) | l.2743–2764 | verbatim to AV §7, ≈ 2 days turnaround (N-C4) |
| 8 (wording) | grep "promotion credit": 0 hits; grep "realistic branch": only §13.3 history row l.2904 | clean |

### R2 — Q3 annex complete: **RESOLVED**
- Annex rows l.2827–2829: "**route 5: promotion model not submitted**", "**route 6: S_CKF NOT TESTED**", "**B4-e, size**
  (in route 3)", each with all six columns as AV §6 R2. Route-5 status "unlikely if R04 occupancy is as v1's, not
  excluded (2–4 qualifying classes expected)" as ordered.
- B4-e size: 4×10⁵ × 1.14/100 = 4,560 → "4.6×10³", range 0.1–10 % → 456–45,600 → "460–46,000": correct; >300 = above
  the day-15 class: correct.
- Q3 text l.2771–2774: "B4-e (a B4-e failure alone sets a floor of ≈ 4.6×10³ events); B2-c at depth; the promotion
  model not submitted; S_CKF not tested. Reach under the default: (β) of Table 4.4c: 705–640 GeV at the 84 % edge …
  if the promotion model is submitted". (β) edges printed 706 / 684 / 641 → "705–640": correct.

### R3 — pilot before its code: **RESOLVED**
- §4.4 point 5 l.847–850 "The pilot's no-pile-up jobs keep the full hit records (≈ 52 GB … provisionally by day 7 and
  with the frozen hand-over variant by day 12; the 1,000 near-pass overlays (7 CPU-h) are made from that
  classification." Storage: (4×10⁶ + 2.3×10⁶) × 8.2 kB = 51.7 GB (stdout l.215), §11.4 row l.2595 "52", total
  417 → 469 GB → "≈ 470 (≈ 670 at the pre-merge cap)" l.2599, §0 l.109 "470 GB", §11.6 l.2671 "470–670 GB", B1
  storage l.1073. Consistent.
- §11.7 inputs l.2683–2684 "generated by day 5, classified provisionally by day 7 and finally by day 12"; rule 1
  l.2693–2696 gives the day-7 input (v1-based EST pile-up rows) and the date of the occupancy model's R04–R05 inputs
  ("by day 14 at the latest"), as AV asked the fixer to determine; §4.4 point 4 l.817 "at the latest by day 14"; §11.3
  row 5–17 l.2543 "classification of the pilot's records (by day 7)". grep "finished by" / "(finished": 0 hits; the
  remaining "from the finished pilot" (l.2697) refers to the day-7 preliminary projection, after the provisional
  classification: no contradiction.

### R4 — S_CKF samples: **RESOLVED**
- §4.4 point 4 l.758–763: "for DIF on the enriched test overlays with their weights, derivation R04–R05, test R06 and
  R07 where evaluable; for NI by the rung split, derivation R04, test R05; for each SM process on its hit-level halves
  … the restriction to unbiased samples applies to the ceiling and leak tests only." Verbatim to AV §6 R4.
- Df-9 l.2809 "(DIF R06 on the enriched overlays, NI R05 by the rung split, SM R06)"; COM B1-f row l.127 same samples
  and rungs. Route 6 consistent (DIF 31 expected / 24 needed; NI 92 / 120 / 378).

### R5 — paired passes for the eleven processes: **RESOLVED**
- Script [3] row "paired pile-up-only finder pass on 1,000 test-half events of each of the eleven other SM processes …
  35.8 | 11000 x 11.7 s | M | R5" (stdout l.61). 11,000 × 11.7 s = 35.75 CPU-h. [5″] block printed.
- Totals (fresh run): MUST 4,019.4; reduced 4,452.9; full 4,966.2; approved 4,452.9 + 156.5 = **4,609.4**;
  1.3 × = **5,992.2**; MUST-only 4,175.9 / 5,429; full 5,122.7 / 6,660; contingency 75.3 + 696.6 + 1,378 = 2,150;
  envelope 6,759 / 8,787; guesses doubled 5,987 < 5,992; critical path 2,489 CPU-h = 14.3 d; calendar
  **57.8 / 56.9 / 58.1** days. All match AV's expectations and are quoted identically in §0, §11.2 (l.2485–2501),
  §11.3 (21–35.3 … 51.8–57.8), §11.6 (l.2656–2666), Q4 (l.2779–2787), COM ST-1 (l.202).
- Text: §4.4 point 4 (ii) l.798–800 "62 CPU-h … **each of the fifteen SM processes**" (19,000 × 11.7 s = 61.75);
  the borrowing sentence is deleted (grep "closest in topology": 0 hits); §4.0 point 6 l.435–437 H′ sentence; §4.7
  l.1366 "1,186" (1,150 − 13 + 49) and l.1369–1370; inventory row 20 l.2080; COM B1-f, B4-c.

### Adopted C items (AV §6): all **RESOLVED**
| item | v5 / COM evidence |
|---|---|
| G-C1 | §0 l.99–101 "MUST items: **4,019 CPU-h** … 4,453 … **4,609** … 4,966 CPU-h (5,123 with the reserve)" |
| G-C2 | Df-10 l.2810 and COM T1-h l.160 "4.7–4.9 %" (script: 0.047 / 0.049, stdout l.502–503) |
| G-C5 / Ph-C4 | l.895–901 "0.34 = 2 × 0.17 … [U]"; "1.1 % …; with the multijets at 1 % it is 2.1 % [E: 1.1 % + 4×10⁵/4.08×10⁷ = 1.0 %]" (4×10⁵/4.0848×10⁷ = 0.98 %) |
| G-C6 | l.897 "`AN1/bsum_wp.json` → `n_trig.not_included` [U]" |
| G-C14 | l.230–232 "1.5687 for WZ to 1.5945 for tt̄ 2ℓ"; `s4cp.py` l.115 is `pv = vtx[:3] + rng.normal(…)` (read by me); `cprime.dif.rate.per_process.WZ` = 1.56874 |
| N-C11 | §11.3 table ends "51.8–57.8" |
| G-C3 | COM REF-2 "R-10 and R-20 before Phase 4a" |
| G-C11 | COM S1-a deadline column 4a → 4b; consistent with §11.3 (S1 chain in days 36.8–41.8) |
| G-C4 | l.1353–1354 "The four supplied processes (Z(νν), W(τ_h), W(τ_ℓ), tt̄ 1ℓ) … Of the four terms sized at an expected 31 counts" |
| N-C1 | Q4 l.2780–2781 "43.5 days have no critical-path production …" (57.8 − 14.3 = 43.5) |
| N-C4 | Q2 (a) "≈ 2 days of turnaround" |
| N-C6 | Df-8 l.2808 "chosen up front: +156 CPU-h (the conditional ≤ 236 CPU-h … is the switch after a failed f_T check)" |
| G-C9 | l.1350–1351 and §11.7 rule 4 l.2715–2716 "on its derivation parity half"; COM B4-c |
| Ph-C7 | l.1330–1332 "also tests the B4-e factorisation, and a FAIL is charged to the factorisation first" |
| Ph-C1, Ph-C2, Ph-C5, G-C10, N-C5, N-C7, N-C9 | inside R1/R2 above; Q4 review additions "39 + 36 = 75" (stdout: 39.1 + 35.78) |

Items AV left for later phases (G-C7, G-C8, G-C12, N-C3, G-C13, G-C15, Ph-C6, N-C2, N-C10, N-C8) are not re-raised; I
found nothing showing AV's reasoning on them to be factually wrong.

---

## 2. Diff check (complete)

### 2.1 Strategy v4 → v5: 64 hunks, every one attributed
| v5 lines | content | attributed to |
|---|---|---|
| 1, 3–5, 7 | version, fixer, status "cycle 5" | bookkeeping |
| 38–39 | "Projected outcome … (the expected branch is in 'Expected' below …)" | R1 |
| 56–96 | §0 point 3, Expected, leading sentence, "Three things can improve the bounded outcome" | R1 |
| 99–101 | cost figures | R5, G-C1 |
| 109 | storage 470 / 670 | R3 |
| 112–114 | threshold 5,992; Q2 summary wording | R5; R1 |
| 230–233 | DIF rate range, `s4cp.py` l.115 | G-C14 |
| 435–437 | H′ for SM processes | R5 (Ph-C3) |
| 758–763 | S_CKF samples | R4 |
| 770–773 | Df-9 EST with conversion fall | R1 point 4 |
| 798–800 | paired pass on fifteen processes, borrowing deleted | R5 |
| 817 | per-k comparison by day 14 | R3 |
| 847–850 | pilot records | R3 |
| 852 | pilot reading "≈ 3×10²" | R1 point 4 |
| 895–898, 900–901 | 0.34 [U]; `n_trig.not_included`; 1.1 % / 2.1 % | G-C5/Ph-C4, G-C6 |
| 943–944 | m_H = 1000 row; (β) label | Ph-C2/G-C10; Ph-C1/G-B2 |
| 947–952 | credit labels, e^(±1), (α1′) rows, (α2) values | R1, Ph-C5, G-C10 |
| 959–962, 965–974 | scenario text | R1 point 3 |
| 992–993 | "expected branch" in "What is not known" | R1 point 8 |
| 1073 | B1 storage line | R3 |
| 1330–1332 | multijet ceiling ↔ B4-e | Ph-C7 |
| 1350–1351 | derivation parity half | G-C9 |
| 1353–1354 | processes vs terms | G-C4 |
| 1366, 1369–1370 | B4 cost 1,186; 15,000 paired events | R5 |
| 1634–1635 | §4.11 point 3 conditional on the pause | R1 |
| 2080 | inventory row 20 | R5 |
| 2460 | jobs 11,100 / 53 slot-h (stdout 11,132) | R5 consequence |
| 2485–2501, 2513–2515, 2532–2536 | §11.2 tables, v4→v5 delta, contingency | R5 |
| 2543 | §11.3 channel (i) classification | R3 |
| 2546–2553, 2564, 2680 | calendar rows, decision-point dates | R5, N-C11 |
| 2595, 2599, 2671 | storage | R3 |
| 2632 | production 13.4–14.6 days | R5 |
| 2656–2666 | §11.6 figures | R5 |
| 2683–2684, 2693–2696 | §11.7 inputs, day-7 input | R3 |
| 2702–2703 | rule 1 "expected branch" | R1 point 6 |
| 2715–2716 | rule 4 derivation parity half | G-C9 |
| 2743–2764 | Q2 | R1 point 7, N-C4 |
| 2771–2774 | Q3 routes and (β) clause | R2, N-C5 |
| 2779–2787 | Q4 | R5, N-C1 |
| 2808–2810 | Df-8, Df-9, Df-10 | N-C6, R4, G-C2 |
| 2827–2829 | annex rows | R2 |
| 2865–2870 | §12.5 points 2–3 | R1 (listed in §13.4) |
| 2922–2935 | §13.4 change table | bookkeeping |

**Unattributed hunks: none.**

### 2.2 COM and script (`git diff HEAD~1`)
- COM: header (v5 pointer), v5 change table, B1-f (R4 + R5), B4-c (R5 + G-C9), T1-h (G-C2), S1-a (G-C11), REF-2
  (G-C3), TG-1 (R1), ST-1 (R5). **None unattributed.**
- Script: docstring; `N_PAIRED` and the R5 `add()` row; v3→v4 history line rewritten with `R_ADD` subtracted (keeps
  its printed output identical to v4: stdout l.125 unchanged); v4→v5 line; [5″] block; R3 storage line; `PLAN_REACH`
  10⁵ column; fall test; two `alpha1'` tags; `row(pred=)`; m_H = 1000 `row()`; fixed-B print; e^(±1)/log-normal block;
  HEADLINE v5; P3/P14 conversion EST (`GZ` sourced); G-C14 DIF-rate line. All inside AV §9 point 3's list.
  **None unattributed.** (`N_PAIRED` is defined but not used in any computation, as in v4; harmless.)

### 2.3 Outputs
`budget_stdout_v5.txt` = fresh run, byte-identical. v4 → v5 differences: R5 row and every total that follows from it
(4a MUST, totals, B4, Phase-4a sum, approved/thresholds, contingency M 717 → 753, envelope, guesses doubled, calendar
lines incl. range 48.7 → 48.9 and 50 %-utilisation values, jobs 11,043 → 11,132 / 53 slot-h); R3 storage line and total
417 → 469 GB; R1: mapping gains `(621.5, 243)`, fall test, (α1′) inputs and rows, fixed-B lines, (α2) "< 393" → 262 /
"< 243", e^(±1) and log-normal lines, HEADLINE v5, conversion m_H EST; Ph-C2 m_H = 1000 row; G-C14 line. No other
printed value changed (floors 13.0 [12.2–17.8], ceiling family 4.9 %, combined 6.9–8.9 %, T1 462/459 and 0.047/0.049,
fluctuation route 0.30 all unchanged).

---

## 3. Numbers and superseded values

Fresh run confirms: approved **4,609** (4,609.4), threshold **5,992** (= 1.3 × 4,609.4 = 5,992.2), calendar **57.8**
days, floor **13.0** (12.2–17.8), ceiling family 4.9 %, combined 6.9–8.9 %, T1 coverage family 4.7–4.9 %. Each is
quoted identically in v5 (§0, §4.0, §4.4, §4.11, §11, Q4, Df-2, Df-10) and COM (ST-1, T1-h).

Greps in v5 and COM (each hit inspected):
- 4,574 / 5,946 / 57.6 / 3,984 / 4,417 / 4,930: only v5 l.2515 ("Version 4 had …"), §13.3/§13.4 rows (l.2915, 2919,
  2934) and COM l.56 (v4 change table). Historical, labelled. 5,087, 4,570, 5,090, 2,146, 5,952, 420 GB, 620 GB: 0 hits.
- 2,950 / 3,968 (l.2887), 4,378 / 5,691 (l.2511, 2915), 11.7 as floor (l.903 "Keeping the version-3 summed floor of
  11.7 …", l.2903): history only. Other "11.7" hits are the 11.7 s trial cost.
- 710 / 790: l.72 and Q2 l.2750 as the labelled upper edge ("an upper edge"), Table 4.4c l.938 "790 [712]" (upper
  edge row); l.167, 1712, 2358–2359 are the v1 μ₉₅/N_exp ratio. Never leading or expected.
- 470–500: only as the (α1) median in the upper branches (l.68, l.2749). Not as a pessimistic or leading branch.
- "promotion credit", "and therefore weak", "below 393": 0 hits. "realistic": l.2573 (utilisation, unrelated), l.2904 (history).

---

## 4. Headline and Gate-A consistency across the document

| statement | §0 summary | Table 4.4c / scenario text | §11.7 rules | Q2 / Q3 / Q4 | §12.5 | COM |
|---|---|---|---|---|---|---|
| expected: ≈ 10⁴ events led by conversions | l.60, l.65, l.92 | (α1′) 9,929–10,193 | rule 1: (α1′) "expected branch" | Q2 "≈ 10⁴" | point 3 "≈ 10⁴ events" | TG-1: "expected branch is a measured background" |
| 270 (84 %) / 315 (median) / 390 (fixed B) / < 200 at σ_ln 0.2 | l.65–66, l.93 | 273–270 / 317–314 / 394–392; l.973–974 | — | Q2 l.2745–2746; (b) "≈ 270–390" | point 3 "≈ 270 … below 200" | — |
| day-15 pause expected | l.66–67, l.82–83, l.94 | l.991–993 | rule 1 | Q2 preamble | point 3 | TG-1 |
| upside (α1) 420–455 (470–500); factor e 400–570; (β) 705–640 (770–695); empty 710 (790); 1,026 | l.68–74 | 455–421 / 504–469; 571–400; 706–641 / 767–695; 712 / 790 | ≤ 300 → ≈ 560+ | Q2 l.2748–2750; Q3 (β) | point 2 (600–1,000 events) | — |
| label ESTIMATE, v1 placeholder efficiencies | l.63, l.91 | caption l.926–927 "EST, v1 placeholder efficiencies"; l.972 | rule 1 l.2699 | §12.1 l.2733–2735; Q2; Q3 | point 3 | — |

No contradiction in any number. Q2 has three options, each with cost and paper ((a) ≈ 2 days, reserve inside the
approved figure, then (b)/(c); (b) 0 CPU-h, no delay, "real background" paper; (c) redesign time not estimable,
development allowance and reserve, "middle" paper or (b)). Gate A: Q1–Q5 with ● defaults and alternatives with costs,
Df-1–Df-10, annex; the brief's stop conditions are quoted exactly (prompt.md l.341–348 and l.79 against v5
l.2644–2653: identical) — but in §11.6, not in §12.1 (C-5). Two wording issues (C-1, C-6) below.

---

## 5. Completeness sweep for PASS

| requirement | evidence in v5 | status |
|---|---|---|
| C1–C3, B1–B7, T1–T2, S1–S2, P1: method, pre-fixed criterion, statistics, CPU-h, phase | §4.1–§4.15 (headings carry MUST/SHOULD and phases); COM rows C1-a … P1-d each with criterion, phase, deadline; per-item CPU-h in §11.2 and script [3] | complete; no row removed in v5 |
| S3 as fixed by the user | §4.16 "S3 (dropped, brief D1) … outlook, tagged EST" = prompt.md l.66 | ✓ |
| S4 / S5 proposal | §4.16 [DP4] with costs (≈ 740 CPU-h; ≈ 50 CPU-h) | ✓ |
| ≥ 2 approaches, MVA position | §3.2 table; [DP3] BDT cross-check, COM MVA-1 | ✓ |
| backgrounds classified | §2 table (irreducible / reducible / instrumental with sizes) | ✓ |
| conventions enumeration | §5.1–§5.2 (27 Will-implement / N/A entries) | ✓ |
| reference analyses | §6.1–§6.2 | ✓ |
| labels | §7 index | ✓ |
| flagship figures | §9 (seven flagship, supporting, seven diagrams) | ✓ |
| 25 referee questions | §10: 25 numbered rows | ✓ |
| pre-registration outline | §8 | ✓ |
| schedule with decision points | §11.3, §11.7 | ✓ |
| blinding | §4.1, BL-1; v5 adds no signal quantity (diff §2.1) | ✓ |
| nothing discarded returns | diff §2.1: no endcap, no ρ = 3, no Λ ≥ 15 keV, no new grid point; Q2 (c) is a conditional already in B3-b | ✓ |

"What would a competing group have that we don't?" A measured conversion rejection (vertex veto) — offered as Q2 (c)
and the B3-b conditional; acceptable as a user decision, not a gap.

---

## 6. New findings (all Category C)

**C-1 (§12.5 point 3, l.2867–2870): "a reach below the existing bounds at low mass" now sits beside "the expected
branch … ≈ 270 GeV at the 84 % edge".** The fix appended the expected-branch clause to an older sentence. 270 GeV
(statistics only) is above the < 180 GeV bounds quoted in §0 and Q2; only with σ_ln = 0.2 is it "below 200 GeV", i.e.
at the bounds. Suggest: "a measured background; reach ≈ 270 GeV at the 84 % edge statistics-only, at or below the
existing bounds (< 200 GeV) with a systematic width of 0.2". Not B: no number differs and Q2 carries the precise text.

**C-2 (stale attributions).** l.16 "(Brigitte, Dmitri, Emeric or Fiona, whoever wrote it)" omits Gunnar, who wrote
new [V] tags (e.g. `s4cp.py` l.115). §12.2 l.2837 "(entries [Fiona] for this version …)" — the v5 entries are
`[Gunnar]` (`experiment_log.md` l.402–414).

**C-3 (disclosure of the conversion rate behind "≈ 10⁴").** The (α) rows use v1's conservative rate 0.379 per event
(`cprime.gamma.rate.choice` = "max over SM processes (conservative)", the tt̄ 1ℓ value); v1 also records the
N_trig-weighted mean 0.255. With the weighted mean (my run of the script's `pmf_pred`): conversions 6,421, B₅₀ 6,825,
reach median 342, **84 % edge 297**, fixed B 419 GeV. Still "≈ 10⁴ order", still far above the day-15 class, so the
headline and the expected pause stand, and the choice is the conservative one; but the rate choice is not stated in
§0 or Table 4.4c (grep "0.379": only l.556). One clause in the scenario text would make it visible.

**C-4 (§0 l.58 rounding).** "0.04–0.06 counts at R07": the printed μ are 0.038 / 0.065; "0.04–0.07" (or "0.04–0.065")
matches the script.

**C-5 (Gate-A self-containment).** §12.1 does not quote, or point to, the brief's stop conditions; they are quoted
exactly in §11.6. Add to Q4 "(stop conditions of brief §7 quoted in §11.6)" so the Gate-A package read alone carries them.

**C-6 (Q2 upside wording, AV text copied verbatim).** "if Z(νν) is tested and the other ceilings count 10–100 events,
≈ 705–640 GeV" drops "conditional on the promotion model being submitted" (stated in §0, Table 4.4c, Q3) and "count
10–100 events" means simulated ceiling counts m_H (23–230 background events, Table 4.4c), not background events.

**C-7 (COM tags).** COM T2-h and TG-1 keep the tag "(Q2)"; after Q2 became "the deliverable if the background is
large", the link of T2-h (estimate-only selection) to Q2 is not explained. A one-word note or retag would avoid an
orphaned cross-reference at Gate A.

---

## 7. Conclusion

- R1, R2, R3, R4, R5: **RESOLVED**. Adopted C items: **all RESOLVED**.
- Diff check: every hunk of the strategy, COM and script attributed; **no unattributed hunk**; script output changes
  only in the ordered values; fresh run identical to `budget_stdout_v5.txt`.
- Numbers: 4,609 / 5,992 / 57.8 days / floor 13.0 / 6.9–8.9 % / 4.9 % / 4.7–4.9 % reproduced; superseded values
  appear only in labelled history.
- **No Category A and no Category B item remains open.** Seven Category C items (C-1 … C-7), none blocking PASS;
  C-1, C-3 and C-5 are the ones worth applying before the Gate-A package is assembled.
