# C1-d sealed tier: pre-registered choices for `c1_signal_compare.py sealed` (Petra, fixer, 2026-11-19 10:36 -0500)

Committed together with the code BEFORE any sealed read (advisor ruling Oddny, LOG.md 2026-11-19 10:28). Written on
synthetic numbers only: no siga2/siga5 file, key or key name was opened or listed; the study key was not read.
Frozen text: `phase1_strategy/outputs/STRATEGY_oscar_2026-11-16_10-41.md` (STR below); COMMITMENTS C1-d/C1-e; E4.

## Choices where the frozen text leaves room
1. **Signal family** = one "signal" row of the declared-comparison table (STR l.583-585): E200 1.5 keV {R04, R06,
   R07, FB2}; E200 2 keV {R04, R07, FB3}; E500 3 keV {R04, R07, FB3}. Open and sealed quantities of a point are one
   family (4 + 3 + 3 = 10 quantities, as in the table's n column).
2. **Coherence statistic** (STR l.598): the frozen form, inverse-variance mean of ln(x₂/x₁) with diagonal weights,
   |z| < 3; its variance w'Sw/(Σw)² uses the full joint covariance S (as `joint_family` in c1_compare.py, 54610b6 /
   29079b7). This joint value is the printed verdict; the independent-entry value is kept in the encrypted file only.
3. **Width of ln(k₂/k₁)**: binomial delta method, Var ln p̂ = (1/p − 1)/n per sample, v1 and v2 added.
   **v2 covariance** from the 400 rows: Cov(ln p̂_a, ln p̂_b) = (p_ab/(p_a p_b) − 1)/n₂, which for nested rungs
   (R07 ⊂ R06 ⊂ R04) is the nested-binomial value (1/p_outer − 1)/n₂ (checked against a bootstrap in the selftest).
   **v1 covariance** (v1 rows lost): nested rungs the nested-binomial value (1/p₁,outer − 1)/n₁ (exact if v1's
   rungs are nested, as by construction); pairs with the fallback column: v1 correlation = v2's (ESTIMATE, same rule
   as E4/joint_family). v2 nesting violations are counted into the encrypted file.
4. **k = 0** (either sample): that count enters ln and its width as 0.5 (Haldane), and its covariances with the other
   quantities of the family are set to 0 in that sample. The Fisher test uses the raw counts. Flagged in the file.
5. **Individual z for the global sum**: z_i = Φ⁻¹(1 − p_i/2) from the Fisher p (two-sided, unsigned); open-tier p read
   from `outputs/c1_signal_open.json` and re-computed from the rows (mismatch = stop).
6. **Two global verdicts** against the 99th percentile of χ²₄₁ (STR l.597, l.644):
   *frozen-naive* = Σz² of all 41 as independent = `global_partial.sum_z2_naive` of
   `outputs/c1_compare_mattias_2026-11-19.json` (31 background, amended entries) + 4 open + 6 sealed z².
   *joint-block* = `global_partial.sum_z2` of the same file (pu1, pu2, clos, cppu, sm as d'S⁻¹d) + Σ over the three
   signal families of d'S⁻¹d (10 dof); 41 dof in total. Cross-family correlations (T1/T1w with pu1/pu2) not removed.
7. **Twin fallback ratio** full/fast (FB2 at E200 1.5, FB3 at E200 2; expectation ×0.871): encrypted file only.
8. **Guards** (stop, print only "n-complete: no" and the guard's name, write nothing): n₂ ≠ 400 for any of the 10
   quantities or the 4 twin columns; any job marker of p2-a-c1-siga2/siga5 without a done line; open or background
   JSON missing/short (31 entries, n_available 31, n_declared 41, Σz² consistent); open-tier recount ≠ open JSON.
   Any exception: only "crashed: <class>"; fd 1 and 2 go to /dev/null while the sealed path runs.
9. **Key and output**: key via `openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:<key>`, encrypt only; key refused if
   inside the repo or the data tree (`/nfs/cajuela/jdochoa/quirks_v2`), not mode 600-like, or not one hex line. Output
   refused inside the repo or if it exists; written as `.part`, fsync, rename. The ledger marker of the encrypted file
   is left to the orchestrator (sha256 and path are printed).

## Selftest (landau, 2026-11-19 10:35, synthetic only): 11/11 OK
all-PASS + round trip; stdout line count; one-FAIL; n₂ guard (399, 0, twin); incomplete/inconsistent inputs; k = 0;
exception path (in-process and a child writing numbers to fd 1/2: stdout only "crashed: ValueError", stderr empty);
key/out refusals; nested covariance vs bootstrap within 10 %. Real open/background JSONs pass the input guards
(open Σz² 7.45, background naive 16.11 [VERIFIED, landau]).
