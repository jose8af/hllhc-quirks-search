# Reach re-estimate with pilot-based backgrounds: PLAN (written before any computation)

Tora (executor, Opus 5.5), 2026-11-23 16:31 -05 (`date`). Task: EXPLORATION.md §9 PENDING block "reach re-estimate"
(ORCHESTRATOR_STATE l.69, LOG 19 Nov 17:22). Everything produced is **ESTIMATE on v1 placeholder efficiencies**.
Blinding: no signal file is opened, no v2 signal efficiency is formed or stated, no sealed count is read.

## Method (unchanged from Gate A)
- Gate A's reach comes from `phase1_strategy/src/strategy_budget.py` ([9b], l.569-831; last changed in c69c1b7, the
  commit that wrote `outputs/budget_stdout_v9.txt`, the stdout of record of GATE_A.md l.3, l.8). Headline: the v6 (T1)
  rows (stdout l.326-342): (α1′) no credit, conversion term as a log-normal of median g and width √(w² + 1/(m+1)),
  m = g/κ_Z, w = 0.17 (W_NORM, l.791); DIF counted as κ_DIF·Γ(m+1); pool zero-count floors `kap_nodif`; pile-up R09
  term PU9; one-bin expected CLs limit s95 from the predictive pmf (`pmf_pred`, `s95_pmf`, 3,000 draws, seed 7) at the
  median and 84 % quantile; reach from s95 by the plan's σ_ln = 0 row (`PLAN_REACH`/`MAPR`/`reach_of`, l.654-663;
  s95 621.5 ↔ 243 GeV is the last point, beyond it "< 243").
- New wrapper `phase2_exploration/src/reach_reest_tora.py` runs the unchanged script with `runpy` (its stdout to a
  file), checks that its v6 (T1) and [9b] mapping lines reproduce `budget_stdout_v9.txt` byte for byte, then calls the
  script's own functions with the substituted background inputs. No function of the script is modified or re-coded.

## What changes (background inputs only)
1. **Conversion-led term** (Gate A: conversions 9,530 / 6,420 at photon rate 0.379 / 0.255, + DIF 385 / 647):
   × the frozen-rule attribution fractions (Eskil `CPU_ATTRIB_eskil_2026-11-19.md` l.42-43, l.38-39; Kari
   `CPU_ATTRIB_NI_kari_2026-11-23.md` l.65-72): ρ_γ = 0.057 (R05) / 0.091 (R06) central, 0 low (37 % of bootstrap
   replicas), 0.22 event-level 95 % UL; ρ_DIF = 0 central (term at its pool floor, Gate A's projection rule
   max(floor, N·H), stdout l.384), 0.064 UL. NI does not move the total (Kari l.68-70). Same log-normal form, same w.
2. **Z(νν) / SM term** (Gate A: SM pool floors, planned pool). Replaced by the pilot read through Df-11 (every SM process
   and multijets via the one Z(νν) pilot count, 41.96 events per count, M = 993,887; Tove l.51-52, Ingvild l.25):
   the SM pool floors and the multijet floor are removed from `kap_nodif` to avoid double counting.
   Counts (R08 = R09 width): after-CKF finder pass 0 (central), own-hit finder pass before CKF 11 (high), Gate A's pool
   floors kept (low). After-CKF near-pass 17 (a lower bound) as a sensitivity row. Counted terms get the same
   √(w² + 1/(m+1)) width as Gate A's Z ceiling row (l.827).
   **Rule-1 counts as ceilings only:** the frozen rule-1 count (near-pass inclusive; finder N = 253, subset S = 1,501)
   is a ceiling on own hits before CKF, not a background estimate (advisor Åsa, LOG 19 Nov 15:24; Dagny 15:37). It is
   shown in one information row only ("what the ceiling would imply"), never as a variant.
3. Variants: **low** (ρ = 0, DIF floor, Z pool floors), **central** (ρ_γ 0.057–0.091 × both photon rates, DIF floor,
   Z after-CKF pilot zero), **high/UL** (ρ_γ 0.22, ρ_DIF 0.064, Z own-hit pass 11), plus one-factor-at-a-time rows
   (each substitution alone; DIF kept at Gate A's v1 size; w = 0 statistics-only).

## Kept unchanged (listed in the result)
Pile-up PU9 (R09 EST median, s_tot 0.59, cap N_trig/96,000 × Exp(1)); DIF and NI pool floors; DIF falls ×339 / ×201;
photon rates 0.379 / 0.255; w = 0.17; N_trig 4.0848×10⁷; the plan's s95 → reach table; v1 placeholder signal
efficiencies (inside the table); 3,000 draws, seed 7; the one-bin CLs method.

## Compute
Pure Python (math, random), no toys, no jax: run once on schrodinger (nice 15, 1 slot, SLOTS line + release),
expected < 10 CPU-min. Output: `outputs/REACH_REEST_tora_2026-11-23.{md,json}`, log `logs/executor_tora_2026-11-23_16-31.md`.
