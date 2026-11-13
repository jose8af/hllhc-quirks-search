# INV_A2FC_E500: why A2FC loses so much at the deep rungs at E500, Λ = 3 keV

Investigator, 2026-10-16. This investigation was read-only on the frozen code, the production data, the C12_v1 and C12FC_v1
analysis outputs and STAGE4_RESULTS.md. New scripts are in `acts/stage4/investigation/inv_a2fc_e500_*.py` and their
outputs in `data/acts_stage4/investigation/inv_a2fc_e500_*.json`. One A2 PU-only chain re-run (A2_F500_001, 10 events)
went to the session scratchpad. It was not written to production.

**Tags.** [V] means computed here from production, analysis or re-run outputs. [E] means an estimate or an
interpretation.

## 0. Verdict

**Cause: (c) statistics. There is no bookkeeping bug and no new detector-physics effect, so this is not an A-level issue.**

- **The deep rungs are noisy.** At R08–R14 the pass/fail of a given row depends on the **measurement-noise draw**, of
  both the quirk hits and the PU hits. Re-drawing that noise flips about 25–50 % of the passing rows.
- **Most of the noise is re-drawn.** A2FC re-draws all of it relative to A2, so at the deep rungs "same rows, same seeds"
  gives almost no variance reduction.
- **The two productions fall on opposite sides of the noise expectation.**
  - Numpy A2 at E500 3 keV (22/200 at R14) is a high draw. Most of that comes from a favourable PU-noise draw.
  - A2FC (4/200) is a low draw.
  - Fresh noise draws of the A2 model on the A2FC PU events give **10–12/200** at R14.
- **Only one of the 18 lost rows is a genuine full-chain effect.** Row 268 lost 46 of its 83 quirk hits to the CKF.
- **Recommended action:** keep C12FC_v1 as it is. The full chain is the pre-registered reference, and no fix is needed.
  Re-word the §4.3 flag (§6).

## 1. Paired per-rung comparison [V]

Script `inv_a2fc_e500_paired.py`. It compares the C12_v1 and C12FC_v1 `signal_rows_a2.npz` row by row, on the same rows.
The counts are k(A2) → k(A2FC), followed by (A2-only / A2FC-only discordant rows) and the exact two-sided McNemar p.

**E500 3 keV** (n = 200):

| rung | count A2 → A2FC | discordant (A2-only / A2FC-only) | McNemar p |
|---|---|---|---|
| R04 | 64 → 61 | 7/4 | 0.55 |
| R07 (w < 9.4) | 51 → 48 | 7/4 | 0.55 |
| **R08 (w < 4.7)** | 31 → 19 | 15/3 | 0.0075 |
| **R10 (χ²_core p > 0.01)** | 26 → 8 | **18/0** | 7.6e-6 |
| R11 | 23 → 5 | 18/0 | 7.6e-6 |
| R14 | 22 → 4 | 18/0 | 7.6e-6 |
| FB3 | 29 → 11 | 19/1 | 4.0e-5 |

**Which cuts lose the events.** None are lost at R04–R07, so CKF stealing is negligible (64 → 61). The loss comes from:
- the w_core < 4.7 mm cut (R08);
- above all, the χ²_core p cut (R09–R11).

The 2S rungs (R12–R14) lose nothing further. On the lost rows, the A2FC best candidate has a wider core and more PU hits
in it. Examples (w_core in mm, n_PU in core):

| row | A2 w_core / n_PU | A2FC w_core / n_PU |
|---|---|---|
| 8391 | 3.2 / 4 | 8.5 / 19 |
| 5265 | 3.0 / 8 | 6.4 / 16 |

This is the MAD core breaking down once PU hits are about 50 % of the IT+PS hits (`inv_a2fc_e500_events_F500_L3.json`).

**The other 8 revert points at R14 (A2-only / A2FC-only):**

| point | R14 discordant |
|---|---|
| E200 3 | 6/6 |
| E200 5 | 7/4 |
| E500 5 | 13/5 |
| E1000 3 | 1/0 |
| E1000 5 | 6/6 |
| E1500 3 | 4/3 |
| E1500 5 | 7/4 |
| Ẽ500 5 | 6/5 |

- Their sum is 50/33. At FB3 it is 63/39.
- **E500 3 keV is the outlier.** It is the most extreme of the 9 points. With a look-elsewhere factor of about 9–30, the
  global p is about 1e-4 to 1e-3 [E].
- The flip rate is large everywhere: about 40–60 % of the R14-passing rows flip in each direction. So the deep-rung
  outcome is not "the same event plus a small perturbation".

**Control points.** The non-revert points Ẽ500 3 keV and E500 2 keV are bit-identical between the two analyses (L
identical).

## 2. Bookkeeping, check (b): no bug [V]

**Merge code.** `signal.apply_a2fc` (signal.py l.352-392) and `run_all.py` l.346-366 were read in full.
- The A2FC|… → A2|… relabel replaces the whole accumulator entry: rows, L, LT, FB, FBT, obs and best.
- It is guarded by a check that the sorted rows and the probe-excluded and status≠1 counts are equal.

**Checks at all 9 points (`inv_a2fc_e500_summary.py`, `inv_a2fc_e500_trials.py`).** For every point:
- 20 jobs and 200 table rows on each side; the row sets and the row order are identical.
- n_q_written, status and probe_excluded are identical row by row.
- The seeded inputs are identical for 200/200 rows: trials.pv, phimet, trial_seed, seed, delta95, n_btl.
- The pool counters (n_road, n_ckf_hits, n_trip, …) differ symmetrically (frac > 0 ≈ 0.46–0.54) at every point. Nothing
  is special at E500 3 keV.

**Recounts.**
- Recounting R14 from the raw files gives exactly 22 (A2) and 4 (A2FC). The in-job `sig.eff_fckf` definition gives the
  same 18/0 pattern.
- The revert provenance in `signal_eff.json` (eps_R14 0.11 → 0.02, 20 A2FC jobs) matches.
- There are no lost, double-counted or mis-labelled jobs, and no Λ, channel or normalisation mix-up.

## 3. Ingredient isolation (TT-side re-runs with the frozen modules) [V]

**Quirk inputs are identical** (`inv_a2fc_e500_resid.py`). The quirk SimHits that entered A2FC equal the numpy-A2 input:
4994/4994 hits, max |Δtruth| 0.14 µm.

**ACTS and numpy smearing are the same model** (`inv_a2fc_e500_smearstat.py`, `inv_a2fc_e500_cols.py`, PU check).
- The ACTS quirk residuals are Gaussian: rms 0.98–1.01 σ, kurtosis 2.9–3.2.
- There is no per-event coherence: the variance of √n·mean is about 1.
- There is no direction or charge bias.
- The PU smearing of the re-run A2 chain and of A2FC agree to rms 0.99–1.01 in every kind.
- The σ constants are identical.

**Hybrid re-runs** (`inv_a2fc_e500_hybrid.py`, `inv_a2fc_e500_a2pu.py`, chunk 1, rows 730/843/852 lost):
- **Validation.** The re-runs reproduce the stored A2 and the stored A2FC flags exactly, on 10/10 rows each.
- **CKF flags do not matter.**
  - A2 PU positions with the A2FC CKF flags still pass.
  - A2FC PU positions with the A2 CKF flags fail.
- **Both noise draws can flip a row.**
  - A2 PU with the A2FC (ACTS) quirk measurements fails: 730 and 843 at R11, 852 at R08.
  - In the column-swap test (rows 2067 and 4239), only the quirk x, y, z decide. dE, t, ids, σ and flags are irrelevant.

**Noise replicas** (`inv_a2fc_e500_replica.py` → `inv_a2fc_e500_repsum.json`). Numpy quirk-noise re-draws were run on the
A2FC PU events, over the 34 rows that pass R08 in either production:

| sample | R08 | R10 | R11 | R14 |
|---|---|---|---|---|
| numpy production draw on A2FC PU | 25 | 15 | 12 | 12 |
| fresh draw k = 0 | 23 | 14 | 12 | 11 |
| fresh draw k = 1 | 23 | 15 | 11 | 10 |
| **A2FC production** (ACTS draw) | 19 | 8 | 5 | **4** |
| **A2 production** (A2 PU + numpy) | 31 | 26 | 23 | **22** |

R14 pairwise discordance:
- Numpy draws among themselves: 5/4, 5/3 and 3/2 (symmetric).
- ACTS draw against the three numpy draws: 1/9, 1/8 and 0/6.
- Swapping only the PU noise (A2 → A2FC, numpy production quirk draw fixed): 10/0.

**Statistics.**
- The A2-model expectation on these PU events is about 10–11/200 at R14, i.e. ε ≈ 0.05 [E].
- A2 = 22 sits about 3σ high. Most of the excess comes from the A2 PU-noise draw (10/0).
- A2FC = 4 sits about 2–2.5σ low (Poisson-binomial σ ≈ 2–3) [E].
- Both are draws from statistically identical models [V], so the pair is a combined tail of about 1e-4 to 1e-3 after
  look-elsewhere [E]. No mechanism was left untested.

**The one genuine full-chain loss.** Row 268 had 46/83 quirk hits on CKF tracks in A2FC. It passes 3/3 with the numpy
quirks.

## 4. Why INV_SIGNAL_EFF said −7 %

That estimate is the CKF-stealing loss at R04 (the in-job flag), and it holds: R04 64 → 61 (−5 %) [V]. The deep-rung
excess is not CKF stealing. It is measurement-noise variance, which is not captured by a paired small-perturbation
picture.

## 5. Status of the results

- C12FC_v1 is correct as computed.
- Each production's Clopper-Pearson interval is valid for its own sample. A2FC gives ε_R14 = 4/200 (CP68 ≈ 0.011–0.034)
  [E for the interval].
- The pre-registered reference at the revert points is the full chain. Replacing it with A2, or averaging the two, would
  be a post-hoc choice.
- The C12_v1 "largest-ε point" (0.145 at FB3) was itself an upward fluctuation [E].

## 6. Recommended action

1. **No fix.** Nothing in `signal.py` or `run_all.py` is wrong.
2. **Re-word STAGE4_RESULTS §4.3** (orchestrator/executor) from "surprise, not investigated" to: "statistical. Deep-rung
   pass/fail is dominated by the measurement-noise draw, which A2FC fully re-draws. A2 22/200 is high and A2FC 4/200 is
   low against a replica expectation of ≈ 10–11/200. Bookkeeping and models verified identical (INV_A2FC_E500)".
3. **Interpret the deep-rung A2 → A2FC changes as two nearly independent samples.** This applies at all revert points.
   It does not apply at R04, where the comparison is genuinely paired.
4. **Optional, Stage 5 or later.** If a less noisy deep-rung ε is wanted, a pre-declared K-fold noise-replica average
   would be a methodology change and needs pre-registration. It is not recommended before the deadline.

**CPU used:** about 23 CPU-min [E], all at nice 10. That is slightly above the ~20 CPU-min target, because of the ACTS PU
re-run (4.6 min) and the replicas (about 11 min).
