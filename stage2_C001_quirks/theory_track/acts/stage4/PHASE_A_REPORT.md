# Stage 4, Phase A report: in-job ρ = 2 weights, storage policy, G2b, WP_RULE draft, production runner

Executor, 2026-10-13, 16:15-17:15. All work was PU-only and signal-blind: no signal efficiency, signal toy or signal
yield was computed or looked at. The authority is `acts/stage4/plan.md` (R9 PASS); it was not edited. Proposed plan
changes are in §7.

## 1. Summary

- **ρ = 2 counting-rung weights are exact.** A DP per layer is combined with exact enumeration of the few interactions
  that touch several layers. Cost: **4 µs per set**; the old Monte Carlo cost 12 ms (×3 000). Agreement with plain MC
  on 1 280 sets is within MC error.
- **The width, χ²_core, 2S and dE/dx families are in the job.** They use importance sampling conditional on
  N_IP2 ≥ 7, with the core re-centred per subset (plan §4.1 step 3b), 64 subsets per set.
- **G2b PASS.** t₂ = **33.9 s median, 33.1 ± 1.7 s mean** over 12 ρ = 2 trials (finder 25.9 s, in-job work 7.2 s).
  The criterion for C1 → C2 is t₂ ≤ **66 s**.
  - No sub-sampling is needed, so the pre-declared fractions are **f_lo = f_hi = 1**.
  - C4′ fits the 47 h window only if t₂ ≤ 24 s. With the reported 6 h lead (53 h) the limit is 49 s, which is met.
- **Storage.**
  - Every trial: per-rung counts, flags and weight sums.
  - Compact records: every candidate at R04 (N_IP2 ≥ 7 plus the Δφ cut), and a 1 % sample of the loose candidates.
  - **Full hit records** (ρ = 1): R04 ∧ (w_core < 37.5 mm ∨ p(χ²_core) > 10⁻³), the exact population any rung ≥ R05 or
    any fallback selection can reach.
  - ρ = 2: the plan's hit-record samples (a) and (b).
  - Total ≈ **37-42 GB** for G3 + C1 + C2 + C4′.
- **`WP_RULE.md` is a DRAFT**, with the transcription, the storage policy, the frozen-input tables and the code sha256s.
  - 5 open freeze inputs (δ₉₅, MIP unit, muon-gun βγ, SR-T in-job factor, f_CKF/CKF).
  - 8 executor DRAFT decisions for the reviewer.
- **Runner `acts/stage4/run_stage4.py`**: run / status / check / smoke / manifest, detached-friendly, restartable, STOP
  file, nice, memory-aware scheduling.
  - **Smoke: PASS** on 2 PU-only jobs (interim chain), bit-identical on a rerun.
  - Production is **refused** until the G1 chain `run_chain.py` exists and `WP_RULE.md` is frozen. Nothing was launched.
- **The main blocker is G1.** There is no production chain yet: no SimParticle PU reader, no CKF, no signal, SM or C′
  jobs. The G3 pilot and C1 cannot start as the plan defines them until it exists (§9).

## 2. What was built (all under `acts/stage4/`)

| file | content |
|---|---|
| `finder/weights.py` | `count_weights` (exact counting DP), `subset_weights` (conditional IS; 34 columns: R05-R14, F0 × dE/dx, FB0-FB4, FB × dE/dx, mean W), plain-MC references, `group_sets` (greedy distinct-hit-set grouping, the review-R2 rule) and an exact prefix-filter variant (`group_sets_fast`, kept but slower at this density) |
| `finder/production.py` | `process_trial`: finder → R04 grouping → the 43-column full-set rung flags (incl. the fixed Δφ < δ₉₅ cut) → ρ > 1 weights (DP on every aligned set, IS on every R04 set) → per-rung sums → storage selection |
| `finder/pu_inputs.py` | production PU trial inputs from a chain event: interaction ids, the TDR top-up **with dE and t resampled from the sensor's own Fatras hits** (f1r set dE = 0, so 63 % of the IT hits had no dE), BTL hits, PV |
| `finder/finder.py`, `kernels.py` | only `find(..., want_csr=True)` and `kernels.csr_hits` added (the same hit lists as one CSR; default unchanged). **`test_equivalence` re-run: PASS**, 24 trials, 2 514 806 identical candidates (`data/acts_stage4/g2b/equivalence_rho1_phaseA.json`) |
| `finder/validate_weights.py`, `bench_g2b.py`, `g2b_criterion.py`, `wp_rule_tables.py` | validation, G2b timing, G2b criterion, WP_RULE appendix generator |
| `code/pu_chain_interim.py` | **interim** PU chain (acts env): the f1r probe chain made seedable, with Poisson(200) pile-up and a time column. HepMC3 transport, **no CKF**. For smoke/development only |
| `run_stage4.py` | production runner; manifests in `jobs/{C1,C2,C4p,G3,smoke}.json` |
| `WP_RULE.md` (+ generated `WP_RULE_tables.md`) | the DRAFT rule |

## 3. ρ = 2 in-job weights: method and validation (`data/acts_stage4/g2b/weights_validation.json`)

**Counting rungs (R01-R04, the N_L2 diagnostics, N_2S2 at R04).**
- Per layer, "≥ 2 crossings" depends only on (min(n_in, 2), min(n_out, 2)).
- Interactions that touch one layer act independently per layer (a 9-state DP per layer).
- Interactions that touch ≥ 2 layers are few: M ≤ 7 on the validation sets, ≤ 12 in G2b, median 2-3. They are
  enumerated exactly (2^M configurations).
- The joint law of (N_IT2, N_PS2, N_2S2) is the Poisson-binomial of the layer outcomes. This is exact; no Monte Carlo.

**V-a: DP vs plain MC (2·10⁴ independent subsets per set) on 1 280 ρ = 2 PU sets** (320 each at N_IP2 = 4, 5, 6, ≥ 7)
- Over all 13 counting columns: per-set pulls mean −0.04…+0.02, rms 0.98-1.05; |z| > 3 in ≤ 0.7 % of sets.
- Summed-weight pulls −1.3…+0.4.
- No set has DP = 0 with MC > 0.
- Cost 3.8 µs vs 12.0 ms per set.

**V-b: DP vs the f1r probe's own `thin_weights` (100 sets, N_L2 rungs).** Per-set pull rms 0.84-1.02. The mean offset of
−0.1…−0.2 is expected: f1r uses one fixed MC seed for every set, so its errors are correlated.

**Per-subset families (R05-R14, F0 × dE/dx, FB0-FB4 ± dE/dx).**
- Multi-layer interactions are drawn ~ Bernoulli(q).
- Each IP layer's single-layer interactions are drawn exactly conditional on that layer reaching ≥ 2 crossings
  (forward sampling against the backward success table).
- The 2S single-layer interactions are drawn ~ Bernoulli(q).
- IS weight W = Π_IP p_l(base), so E[W f] = E_q[1{N_IP2 ≥ 7} f]: unbiased.
- The subset evaluation is the plan's: c(T) and w_core(T) from T's IT + PS hits, the re-centred core, the 2S rule,
  λ_min (closed form) against tabulated χ² quantiles, and N_2S2(T).

**Validation of the per-subset families**
- **V-c: q = 1 reproduces the stored full-set flags.** 2 000 sets, 15 flag columns, **0 mismatches**.
- **V-d: IS (256 subsets) vs unconditional plain MC (4·10⁴ subsets)** on 600 N_IP2 ≥ 7 sets (the 300 narrowest + 300
  random):

  | column | summed-weight pull |
  |---|---|
  | w < 37.5 | +0.03 |
  | w < 18.75 | −0.41 |
  | w < 9.4 | −1.06 |
  | FB0 | +1.10 |
  | FB1 | +0.86 |
  | FB2 | +0.80 |

  Per-set pull rms 0.83-1.18.
- **V-e: Σ mean W vs the exact DP P(N_IP2 ≥ 7):** 14.440 ± 0.027 vs 14.399 (pull 1.5). Where M = 0, W is exact to 10⁻¹¹.

**Production setting.** 64 subsets per set: the same estimator, more variance per set. The per-trial IS relative error
is 0.2 % at R05, 3 % at R06 and ≈ 40 % at R07. The trial-to-trial spread dominates, and the event bootstrap includes the
IS noise.

**Distinct hit sets (plan §4.1, "counted once per distinct passing hit set").**
- Exact greedy grouping of the full loose population costs **144 s per ρ = 2 trial**: 3·10⁵ sets, and every road hit is
  shared by ≈ 900 sets (median). It would cost ≈ 4 s per ρ = 1 trial, which would double t₁.
- A prefix-filter join does not help at this density (178 s).
- Grouping the **R04 population** costs 0.7-1.4 s per ρ = 2 trial and ≈ 0 at ρ = 1.
- At R04, the dedup factor is ×3.4-4.6 at ρ = 2 (e.g. 38 937 sets → 8 529 groups). This is the duplicate-counting
  effect the per-hit-set convention targets.
- Adopted as DRAFT-D2: per-hit-set counts from R04 on; union counts at every rung (plan change §7 (i)).

## 4. G2b (plan §11; `data/acts_stage4/g2b/timing_g2b_final.json`, `g2b_criterion.json`)

- **Setup.** The G2a ρ = 2 trial set (`trials.py`, i = 0-11), the normalised density, one process, one thread. The full
  production path is timed: finder, R04 grouping, flags, exact DP on every aligned set, IS on every R04 set, sums,
  storage selection, and the npz write measured separately.

| stage (mean of 12) | s |
|---|---|
| finder | 25.86 |
| grouping (R04) | 0.66 |
| full-set flags | 0.16 |
| counting DP (all sets, ≈ 2.3·10⁵ aligned) | 0.75 |
| IS (all R04 sets, ≈ 2.5·10⁴, 64 subsets) | 5.53 |
| sums + storage | 0.10 |
| **t₂ per trial** | **median 33.9 [31.6, 36.3], mean 33.1 ± 1.7, p90 38.5** |

- **Peak RSS**: 2.5 GB in this run, 3.9 GB in the first run, which had no Δφ cut. The runner budgets 4 GB per B2 job, so
  at most 4 B2 jobs run at once under the 19 GB default.
- **Storage**: 1.7 MB per ρ = 2 trial.
- **Criterion** (the f4r/f3r block arithmetic, t₁ = 3.86 s mean from G2a, t₂ = 33.1 s, 7 workers = 168 CPU-h/day):

  | set | t₂,max (47 h window) | t₂,max (53 h, with the 6 h lead) | CPU-h at measured | Mac wall h (7 / 5.5 workers) | verdict |
  |---|---|---|---|---|---|
  | C1 | 118 s | 118 s | 121 | 17.3 / 22.0 | PASS |
  | **C1 → C2 (chosen)** | **66 s** (C2's one-day cap binds) | 66 s | 121 + 133 | 36.0 / 45.8 | **PASS** |
  | C1 → C2 → C4′ | 24 s | 49 s | + 92 | 49.2 / 62.6 | fails at 47 h; passes only with the 6 h lead |

  C4′ stays under the user's rule (only if C2 ends by Thu 22:00).
- **Strata.** The plan applies the strata only if G2b fails. It passes at full cost, so **f_lo = f_hi = 1** (`WCfg.f_is = 1`,
  frozen in WP_RULE §6.3).
- **Caveats.**
  1. The 7-worker capacity is the plan convention; G2a measured ×1.12 per trial with 4 parallel processes. At 5.5
     effective workers, C1 + C2 needs 45.8 h, tight against 47 h.
  2. On **fresh Poisson PU** (smoke, 2 events only), t₁ was 4.0-6.2 s per trial (8 trials) vs 3.86 s on the G2a set.
     G1 must re-measure t₁ with ≥ 20 production events. At t₁ = 5 s the decision-table row is still C1 + C2 (42 h), but
     without C4′.
  3. The PU event cost of 4.7 s is the plan ESTIMATE. The interim chain costs 16-18 s per event (Python HepMC3 pool), so
     the G1 SimParticle reader is required.

## 5. Storage policy and disk (WP_RULE §S)

- **ρ = 1.**
  - S1, every trial: seeds, PV, roads, counters, timers, and per rung (43) N_pass and N_grp.
  - S2: compact records of every R04 candidate (≈ 400-1 300 per trial).
  - S3: a 1 % Bernoulli sample of the loose candidates, for the loose factorisation/independence test.
  - **S4 full hit records** of R04 ∧ (w_core < 37.5 mm ∨ p(χ²_core) > 10⁻³) (≈ 140-300 per trial).
  - S5: the BTL hits of every event.
  - S6: the chain-output dumps of the first 2 000 C1 B1 events (plan C-10; compact, 1.2 MB per event).
- **ρ = 2.**
  - S1′: per-trial S_uni, S_ded and the IS variance per rung.
  - (a) ≤ 200 R04 sets per trial and (b) 1 % of the loose sets: compact record, all 43 weights, full hit records.
- **Why the S4 threshold and not N_IP2 ≥ 6 or ≥ 7 alone.**
  - Every rung ≥ R05 requires w_core < 37.5 mm, and every fallback F0 part requires it (FB1-FB4) or p > 0.05 ⊂
    p > 10⁻³ (FB0).
  - So S4 holds every candidate that can pass any rung beyond R04 or any fallback selection, and every item-4a measuring
    population inside them (R05 alone has ≥ 10 per trial).
  - N_IP2 ≥ 7 would cost ×4 more hit records with no rule-relevant gain, and ≥ 6 ×15.
- **Measured** (compressed): ≈ 0.25 MB per ρ = 1 trial, ≈ 1.9 MB per ρ = 2 trial (sample (b) dominates).
- **Disk:**

  | block | GB |
  |---|---|
  | G3 | ≈ 4 |
  | C1 | ≈ 15 (B1 5.0, dumps 2.4, B2 3.8, G1 blocks ≈ 4 ESTIMATE) |
  | C2 | ≈ 15 (B1 7.0, B2 7.7) |
  | C4′ | 3-8 |
  | **total** | **≈ 37-42 (≤ 50)**; 128 GB were free |

## 6. Runner and smoke test

**Commands (from `theory_track/`, TT pixi env):**
- `pixi run python -m acts.stage4.run_stage4 {manifest|run|status|check|smoke} --campaign {C1|C2|C4p|G3|smoke}`.
- Defaults: `--workers 7 --mem-gb 19 --nice 10`.

**Behaviour.**
- One npz per job, written atomically; a rerun skips valid outputs.
- STOP file: `data/acts_stage4/prod/<campaign>/STOP`.
- Progress and errors go to `_progress_<host>.jsonl` / `_errors_<host>.log`.
- Each output records the job seeds, the chain meta, the code sha256s (incl. `WP_RULE.md`) and the frozen inputs.

**Manifests** (plan §6.2 contents).

| campaign | runnable PU-only part | listed as BLOCKED until G1 |
|---|---|---|
| C1 | B1 200 + B2 100 jobs (50 CPU-h) | A1, A2core, A5core, C, C′₀, C′_PU, val (72 CPU-h) |
| C2 | B1 280 + B2 200 jobs (83 CPU-h) | SM C (50 CPU-h) |
| C4′ | — | all of it (92 CPU-h) |
| G3 | 80 + 50 jobs (22 CPU-h) | — |

**Guards.** `run` refuses any campaign except `smoke`:
- while `code/run_chain.py` (G1) is missing;
- while `acts/stage4/frozen_inputs.json` (frozen = true, δ₉₅, mip_gev, the WP_RULE.md sha256) is missing or does not
  match.

Both refusals were checked; `--allow-interim` overrides for development only.

**Smoke (2 PU-only jobs, interim chain, 2 workers): PASS in ≈ 100 s.**
- SMB1: 2 events × 4 roads at ρ = 1. 8 trials, n_loose 0.74-1.1·10⁵, N_pass(R04) 375-1 000, 3.2 MB incl. 1 dump event.
- SMB2: 1 ρ = 2 event × 2 roads. S_uni(R04) 852 / 666, 3.8 MB.
- A rerun was bit-identical in every per-trial count (determinism).
- Outputs: `data/acts_stage4/prod/smoke/`.

## 7. Proposed plan changes (for the reviewer; `plan.md` not edited)

1. **Per-hit-set convention from R04 on** (§4.1 step 2, §11 G3 (i)). R01-R03 and the N_L2 diagnostics use union counts
   at both densities. Union counts are kept at every rung, and the trend test is reported in both conventions. Reason:
   cost (§3).
2. **Per-set ρ = 2 weights are not stored for every set** (§4.1 storage bullet "23 + ≤ 20 × 4 B per set": ≈ 52 MB per
   trial, ≈ 300 GB). Instead: per-trial sums (union and dedup) and their IS variance, and the full per-set weights for
   hit-record samples (a) and (b). The estimator, the bootstrap, T1, the trend and the reachability use only per-trial
   quantities.
3. **Storage policy S1-S8** (WP_RULE §S) added to the plan as a frozen item. Disk §6.3 becomes ≈ 37-42 GB.
4. **The top-up carries dE and t** resampled from the sensor's own Fatras hits (§1.4; f1r used dE = 0, which is
   anti-conservative for the dE/dx rungs).
5. **The IS settings and strata are fixed at G2b**: nsub = 64, f_lo = f_hi = 1 (§4.1 step 3b).
6. **The in-job rung set is 43 columns** (WP_RULE §6.3). h/o/SR-T are factorised at ρ = 1 per the plan's table, so they
   are not in-job. The plan's "23 ladder rungs + ≤ 20 fallback selections" become R01-R14, F0 × e, FB0-4, FB × e and the
   N_L2 diagnostics.

## 8. Physics observations (PU-only; for G3 planning; no closure claim)

On the 12 G2b ρ = 2 trials (final configuration, δ₉₅ = 0.25):

| rung | full sets passing at ρ = 2 | ⟨Σ_groups max w⟩ per trial |
|---|---|---|
| R04 | 2.5·10⁴ | 240 |
| R05 | 4.9·10³ | 66 |
| R06 | 0.75 | 0.65 |
| R07 | 0 | 2·10⁻³ |
| R08 and the χ²_core / 2S rungs after the width rungs | 0 | 0 |
| FB0 | — | 3·10⁻³ |
| FB1 | — | 1.4·10⁻³ |
| FB2 | — | 1·10⁻⁴ |

- **R06 should be "reachable at ρ = 2"** (≥ 10 full-set passes) after ≈ 14 trials; C1 has 2 000.
- **R07 and deeper are not reachable** in these trials. As the plan anticipates, the deepest rungs will rest on rung
  factorisation (T3).
- The Δφ < δ₉₅ cut removes ≈ 25 % of the R04 candidates.

## 9. Launch commands (exact; NOT run). Preconditions first

**Preconditions, both enforced by the runner:**
- (a) G1 delivers `acts/stage4/code/run_chain.py`, with a `pu` mode `run_chain.py pu <out.npz> <n_events> <seed>` that
  writes the same npz layout as `pu_chain_interim.py` (SimParticle reader, CKF removal with the CKF-used flag, V4-1
  records), plus the job kinds for A1/A2/A5/C/C′ in `run_stage4.py`;
- (b) `WP_RULE.md` reviewed and frozen, and `acts/stage4/frozen_inputs.json` written:
  `{"frozen": true, "delta95": <rule value>, "mip_gev": <G1 muon gun>, "wp_rule_sha256": "<sha256 of WP_RULE.md>"}`.

**G3 pilot** (B1 2 000 + B2 500; ≈ 22 CPU-h ≈ 3.2 h at 7 workers at the G2a/G2b speeds):

```
cd /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track
mkdir -p data/acts_stage4/prod/G3
nohup nice -n 10 caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign G3 --workers 7 --mem-gb 19 \
    > data/acts_stage4/prod/G3/run_stdout.txt 2>&1 &
pixi run python -m acts.stage4.run_stage4 status --campaign G3        # progress / ETA
touch data/acts_stage4/prod/G3/STOP                                    # graceful stop
```

**C1** (≈ 121 CPU-h ≈ 17 h at 7 workers; the PU-only part runs now, the rest when G1 adds the job kinds):

```
cd /Users/jochoafl/FISICA_USFQ/hllhc_search/stage2_C001_quirks/theory_track
mkdir -p data/acts_stage4/prod/C1
nohup nice -n 10 caffeinate -i pixi run python -m acts.stage4.run_stage4 run --campaign C1 --workers 7 --mem-gb 19 \
    > data/acts_stage4/prod/C1/run_stdout.txt 2>&1 &
pixi run python -m acts.stage4.run_stage4 status --campaign C1
pixi run python -m acts.stage4.run_stage4 check --campaign C1          # deep validation after the run
```

Keep the Mac on power with the lid open (`caffeinate -i` does not prevent lid-close sleep).

**Development only:** the same commands with `--allow-interim` run the PU-only jobs on the interim chain, i.e. no CKF,
the HepMC3 transport at ≈ 16 s per event, and no freeze check. The outputs record chain = interim. **Not recommended**
for G3: the pre-registered closure branch would be decided on a hit pool without the ≈ 18 % CKF removal.

## 10. Decisions needed

1. **G1 now** (the critical path). Neither the G3 pilot nor C1 can run as the plan defines them without the production
   chain.
   - The PU part (SimParticle reader, CKF, V4-1) unblocks G3 and the PU-only 50 CPU-h of C1.
   - The signal, SM and C′ parts unblock the rest.
   - Option: run G3 on the interim chain now as development (§9). Not recommended.
2. **WP_RULE freeze**: a reviewer checks the draft against the plan, then the user/orchestrator settles:
   - open inputs F-1 δ₉₅ (generator-level rule; it also sets the road), F-2 MIP unit, F-3 muon-gun βγ / the e_adm table,
     F-4 the SR-T in-job factor (not implemented), F-5 f_CKF/CKF;
   - DRAFT decisions D1 (dE/dx estimator), D2 (per-hit-set from R04), D3 (IS settings), D5 (f_CKF before CKF removal),
     D6 (h/o undefined → pass), D7 (SR-T band/overlay), D9 (top-up dE/t), D4-12 (endcap not implemented: F0 is
     barrel-only, |η| ≲ 1).
3. **The plan changes of §7.**
4. **Scope risk.** If G1 measures t₁ ≈ 5 s on production PU (smoke indication), C1 + C2 still fits (42 h) but C4′ does
   not. The Thu 22:00 rule decides as planned.

## 11. Compute used

≈ 1.0 CPU-h in total (cap 6), at most 3 parallel processes, all nice:
- G2b timing (2 × 12 ρ = 2 trials): ≈ 0.4 CPU-h;
- grouping studies: ≈ 0.15;
- validation: ≈ 0.05;
- equivalence re-test (24 trials): ≈ 0.1;
- 3 smoke runs: ≈ 0.15;
- probes and development: ≈ 0.15.

Outputs:
- `data/acts_stage4/g2b/`: 40 MB (timing JSONs, per-trial G2b outputs `out_main/`, `out_final/`, validation,
  equivalence, criterion). The 0.33 GB development cache was deleted.
- `data/acts_stage4/prod/smoke/`: 7 MB.
