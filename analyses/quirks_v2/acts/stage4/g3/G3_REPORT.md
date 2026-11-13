# G3 pilot report (C001 Stage 4, PU-only)

**Verdict: G3 FAIL. Branch: anti-conservative (T1 and T1w), and the T_seed action is triggered → ask the user. C1 should
not launch until the user decides on T_seed and the closure branch.**

- **Authority.** `acts/stage4/WP_RULE.md` (frozen; its sha256 matches `frozen_inputs.json`, unchanged), §2, §6.1-§6.4,
  §5.4 item 11, and plan §4.1 step 4 and §11 item 4.
- **Code.** `acts/stage4/g3/analyse_g3.py` (the tests) and `acts/stage4/g3/g3_rerun.py` (the T_seed and nsub variant
  re-runs: the frozen runner unchanged, one config parameter overridden, output redirected).
- **Results.** `data/acts_stage4/g3/g3_results.json` is the single source for every number below. The SR-T per-hit
  spectrum is in `srt_dt_hist.npy`.
- **Re-runs.** `data/acts_stage4/g3/rerun/{tseed4,nsub256}/`.
- **Inputs.** PU-only. No signal input of any kind.

## 0. Sample and admission

| | manifest | used | left out |
|---|---|---|---|
| G3B1 (ρ = 1, 25 ev × 4 roads per job) | 80 jobs | **77** (1 925 events, 7 700 trials) | **G3B1_00021, G3B1_00059, G3B1_00077** |
| G3B2 (ρ = 2, 10 ev × 2 roads per job) | 50 jobs | **50** (500 events, 1 000 trials) | none |

- **Failed jobs.** All three failures are the same ACTS `GridPortalLink insideBounds` navigation assertion in Fatras
  (the φ-sector portal artefact, G1B_REPORT). They are left out by orchestrator decision: the cause is random and
  job-level, so it cannot bias the finder outcome. The total is 127/130.
- **Deep validation.** `run_stage4 check --campaign G3` reports 127 valid, 0 invalid, 3 missing (the three above) and
  0 V4-1 failures (exit 0).
- **Item 11 admission.** All 127 files carry the frozen A.3 code hashes and the frozen WP_RULE sha256 (`1b2ea9bd…`), so
  G3 enters the background union.

## 1. Closure tests (i): T1, T1w, T1e and the trend

Counts are per distinct hit set, which is the governing convention (§2):
- B1 uses `n_grp`.
- B2 uses `S_ded`, and N_pred = n_trials(B1) × ⟨S_ded⟩.
- z = ln(N_obs/N_pred)/√(1/N_obs + σ²_ln,pred), with σ_ln,pred from a 2 000-replica B2 event bootstrap.
- The pre-registered criterion is |z| < 2 together with a lever arm ⟨S_ded⟩/⟨N_grp(ρ=2)⟩ ≤ 0.1.

| test (family it governs) | rung | N_obs (B1) | N_pred | N_obs/N_pred | σ_ln,pred | z | lever arm | criterion | result | branch |
|---|---|---|---|---|---|---|---|---|---|---|
| **T1** (counting R01-R04) | R04 N_IP2≥7 | 1 093 533 | 828 841 | **1.319** | 0.019 | **+14.3** | 0.041 ✓ | \|z\|<2, λ≤0.1 | **FAIL** | **anti-conservative** |
| **T1w** (width, χ²_core, 2S: R05-R14) | tightest ≥10-count rung = R06 (1 505); λ = 0.666 ✗ → largest lever arm R05 | 318 628 | 223 686 | **1.424** | 0.020 | **+17.6** | 0.031 | same | **FAIL** | **anti-conservative (missing lever arm at R06; z > +2 at R05 anyway)** |
| T1e (dE/dx) | F0e>1.3 | 0 | — | — | — | — | — | ≥10 B1 counts, else T3 | untestable | falls to T3 |
| T3 (factorisation) | R06 from R04 | 1 505 | 1 505 | 1 | — | — | — | \|z\|<2 | **not informative** (degenerate) | — |

- **Diagnostic z with the B1 event bootstrap.** Replacing the frozen 1/N_obs term with the B1 event bootstrap gives
  z = +11.4 (T1) and +13.8 (T1w). The branch is the same.
- **Reading B for T1.** Evaluating T1 at the tightest ladder rung with ≥ 10 counts gives the same rung and branch as
  T1w.

**Trend test.** The test uses the rungs R04-R14 that have at least 10 B1 counts: R04, R05 and R06 (R07 has 9).

| rung | ln(N_obs/N_pred) | σ | z |
|---|---|---|---|
| R04 | +0.277 | 0.019 | +14.3 |
| R05 | +0.354 | 0.020 | +17.6 |
| R06 | −0.547 | 0.030 | −18.3 |

- **Slope.** −0.324 per rung, with σ = 0.012 from the joint event bootstrap (t = −27.9) and 0.017 from WLS (t = −18.8).
- **Result.** The trend is significant and its direction is conservative.
- **Rule applied.** The slope extrapolated to the WP rung is added to σ_ln only, not to the central value. The fitted
  ln r at each rung is in the JSON (`trend.extrapolated_ln_r`), for example −0.89 at R08, −1.54 at R10 and −2.83 at
  R14. At deep WP rungs this adds about 1-3 units to σ_ln, which inflates B₈₄ by e^(1…3).

**What the pre-registered branches imply** (WP_RULE §6.4; "no model shopping"):
- **T1 and T1w anti-conservative.** The only remedy is more statistics in pre-declared +50 % B1/B2 steps: at most two,
  each a user-approved run of about a day or less.
  - The residual is a bias, not a fluctuation: ×1.32 and ×1.42 at σ_ln ≈ 0.02. More statistics can only raise |z|.
  - So the end state is predictable: B_PU = the upper envelope of {thinning, power law, factorisation} × N_obs/N_pred
    of the failed test, with σ_ln enlarged to cover the spread.
  - Literal compounding (§6.4) gives ×1.32 on R04 and ×1.32 × 1.42 = ×1.87 on R05 and deeper (width, χ²_core, 2S, F1).
  - **Flag:** this literal compounding double-counts the R04 part, because T1w's ratio at R05 is cumulative. It is
    conservative.
- **Conservative trend.** It enters σ_ln at every deep rung.
- The orchestrator's pre-registered ordering for under-prediction is: more statistics → the most conservative model →
  user.

**Cause (diagnostic only).** A cause cannot change the branch without a logged re-review (§6.4). The per-hit-set
grouping at ρ = 2 merges more than at ρ = 1:

| rung | ρ = 1 N_pass/N_grp | ρ = 2 S_uni/S_ded | union-count closure |
|---|---|---|---|
| R04 | 1.668 | 3.366 | 0.654 |
| R05 | 1.366 | 3.03 | 0.642 |
| R06 | — | — | 0.426 |

- At R04, union ratio × (S_uni/S_ded) / (N_pass/N_grp) = 0.654 × 3.366 / 1.668 = 1.32, which reproduces the
  per-hit-set ratio exactly.
- So the thinning estimator itself over-predicts, conservatively, in union counts, as in the fix-R1 pilot. The
  anti-conservative result comes from the ρ = 2 groups (≥ 50 % shared hits at double density). These merge sets that are
  distinct at ρ = 1, and taking the maximum weight per group then under-counts.
- A rule change to union-governed counting would need the user and a re-review.

## 2. (ii) SR-T time-position independence on the loose rungs

**Per-hit spectrum.** The per-hit Δt spectrum comes from the in-band BTL hits of the B1 loose candidates (S3 sample
passing R01): 1 963 659 candidates and 594 708 in-band hits.
- Kernel check against the stored `btl_n_band` and `btl_dt0`: 1 mismatch in 1.96 × 10⁶ (a band-edge float32 case), and
  max |Δdt0| = 8 × 10⁻⁷ ns.

**t_min.**
- **In time only:** t_min = **6.12 ns** (the rate is 1.0 × 10⁻³ at 5 ns).
- **With the frozen out-of-time overlay (k = −12…+3): t_min = 25.0 ns = Δt_acc.** The SR-T window is empty.
  - The prompt hits of the following crossing (k = +1) land at Δt ≈ 25 ns. R(t) therefore stays at 8.8 × 10⁻³ from
    5 ns to 24.5 ns.
  - This is a design issue of the frozen SR-T definition: Δt_acc coincides with the next bunch crossing.
  - It is not a G3 branch input, and the review R1 note says SR-T does not enter the G3 decision.
  - **It needs a decision (a logged rule change and re-review) before any SR-T signal ε.** It does not block C1
    production, because t_min is applied offline.

**Independence test at the in-time t_min.** The late fraction (earliest in-band hit in [t_min, 25 ns]) is tested in
bins of N_IP2 and in terciles of w_core, p(χ²_core) and road-hit count. The criterion is p > 0.05.
- **Governing p.** Rao-Scott corrected for event clustering, because candidates of one trial share BTL hits
  (deff 2.5-8).
  - **Loose sample:** 34 late out of 487 729. p = 0.57 (N_IP2), 0.96 (w_core), 0.34 (χ²_core) and 0.42 (density):
    **PASS**.
  - **R04:** 48 late out of 320 142. p = 0.90, 0.91 and 0.31: **PASS**.
- **Naive binomial p.** The R04 density test gives 0.0008, which would fail. This is driven by the clustering
  (deff ≈ 8), and the naive p is reported as a diagnostic.
- **With the overlay t_min:** 0 late candidates, so the test cannot be run.

## 3. (iii) Reach at ρ = 2 and (v) PU population per rung

"Reachable" means at least 10 per-hit-set groups summed over the B2 trials.

| rung | B1 Σ groups (pass) | B1 trial pass fraction | B2 Σ groups (pass) | P̂₁ = ⟨S_ded⟩ per trial | lever arm | reachable at ρ = 2 |
|---|---|---|---|---|---|---|
| R04 N_IP2≥7 | 1 093 533 (1 824 063) | 1.000 | 2 656 084 | 107.6 | 0.041 | yes |
| R05 w<37.5 | 318 628 (435 301) | 0.9996 | 944 545 | 29.05 | 0.031 | yes |
| R06 w<18.75 | 1 505 (1 576) | 0.173 | 507 | 0.338 | 0.666 | yes (**deepest**) |
| R07 w<9.4 | 9 | 0.0012 | 0 | 1.5 × 10⁻³ | — | no |
| R08 w<4.7 | 0 | 0 | 0 | 4.1 × 10⁻⁶ | — | no |
| R09 p>10⁻³ | 0 | 0 | 0 | 9.3 × 10⁻⁷ | — | no |
| R10-R14, F0e* | 0 | 0 | 0 | 0 | — | no |
| FB0 / FB1 / FB2 | 9 / 4 / 1 | — | 1 / 1 / 0 | 3.0 / 1.2 / 0.24 × 10⁻³ | — | no |

**Width and χ²_core rungs populated by PU** (G3 (v)):
- At ρ = 1 the populated rungs are R05, R06 and R07 (9 counts).
- At ρ = 2 they are R05 and R06 directly. The in-job weights still reach R08 and R09 through subsets.
- The χ²_core rungs (R09-R11) and the 2S rungs are empty at G3 statistics.

**Consequences.**
- Beyond R06, the rate at any WP rung must come from rung factorisation (T3). T3 is not informative at G3:
  - from R04 to R06 the step is degenerate (the same variable is tightened twice);
  - R05 would need R03 records, which are not stored;
  - R09 would need R07, which has 9 counts.
- T1e cannot be tested (0 B1 counts at F0e>1.3).
- Under the rule, C5 (ρ = 3) is offered only if T3 *fails*. Whether T3 passes is open until production statistics
  exist.

## 4. (iv) T_seed stability: pre-declared action TRIGGERED

The test pairs the stored T_seed = 6 jobs with re-runs at T_seed = 4 on identical events:
- B1: 5 jobs, 500 trials.
- B2: 3 jobs, 60 trials.
- Reproducibility: chain `evstats` and the trial PV/ev are identical in all 8 jobs.
- σ comes from a paired event bootstrap.

| sample | rung | metric | T_seed 6 | T_seed 4 | change | z (paired) |
|---|---|---|---|---|---|---|
| B1 | R06 | **trial pass fraction** | 0.178 | 0.206 | +16 % | **+3.16** |
| B1 | R04 / R05 | mean groups per trial | 162.1 / 47.6 | 200.1 / 58.8 | +23 % / +23 % | +19.2 / +16.0 |
| B1 | R06 | mean groups per trial | 0.200 | 0.252 | +26 % | +4.41 |
| B2 | R06 | **trial pass fraction** | 0.317 | 0.433 | +37 % | **+2.61** |
| B2 | R04 / R05 / R06 | ⟨S_ded⟩ | 95.9 / 25.8 / 0.312 | 103.3 / 27.9 / 0.363 | +8 % / +8 % / +16 % | +20.9 / +18.0 / +11.6 |

- **Rule.** WP_RULE §6.4: "if the per-family pass fractions move by > 2σ between T_seed = 6 and 4, T_seed(ρ) := 4, the
  jobs are re-timed (G2b criterion) and the change is logged".
- **Result.** The literal reading (trial pass fraction) moves by > 2σ at R06 (the width family) at both ρ. The
  conservative reading (mean count) moves at every rung. **The action is triggered at ρ = 1 and ρ = 2.**
- **Re-timing (under the same production load).**
  - t₁: 5.52 → 8.02 s per trial (×1.45).
  - t₂: 34.4 → 50.6 s per trial (×1.47).
  - G2b's 35.0 s × 1.47 ≈ 52 s ≤ t₂,max = 66 s (C1 → C2), so the G2b criterion still passes (ESTIMATE).
- **Effect on closure (diagnostic).** T_seed = 4 raises the ρ = 1 counts (+23 %) more than the ρ = 2 prediction (+8 %).
  The per-hit-set T1 ratio would grow from ×1.32 to about ×1.51 (ESTIMATE). G3's closure tests characterise the
  T_seed = 6 finder.
- **Action needed from the orchestrator or user.** Change `finder_config.tseed` in the frozen inputs. This is a logged
  change of a frozen file; this agent did not edit it. Then regenerate the manifests and hashes, and decide whether G3
  must be re-run at T_seed = 4 (≈ 17 × 1.46 ≈ 25 CPU-h) before C1.

## 5. Other pre-registered checks

- **IS run checks (§6.3).**
  - 4 of 1 000 B2 trials have |meanW_pull| ≥ 3 (max 3.25), and 3 trials have |meanW_pull_T| ≥ 3 (max 3.46). About 2.7
    are expected for Gaussian pulls. They are flagged and reported, with no action.
  - Zero-draw fraction: 7.1 %.
- **C-4 diagnostic (nsub 64 → 256, G3B2_00001, 20 trials).** The S_ded ratio is 1.000 (R04), 0.992 (R05), 0.913 (R06)
  and 0.854 (R07). The max-of-noisy-IS bias is up to about 9-15 % at the narrow rungs and is conservative. It is
  reported only.
- **Factorisation/independence c-test (§6.4; diagnostic at G3).** Pairs and triples of layers (≥ 2 crossings) were
  tested in 3 density bins, on 1.96 × 10⁶ loose candidates. 220 of 495 have c > 1 at 2σ. The largest is c_max = 1.27
  (TBPS L2-L3 + TB2S L3, densest bin). This c multiplies the factorised estimates post-production.
- **V4-1.** 127/127 jobs pass, over 2 925 chain events (1 925 B1, 1 000 B2 PU events): `map_injective` everywhere, 0
  unmapped, 0 causal violations, max on-surface distance 0.10 µm, 0 signal hits (PU-only, as required).

## 6. Throughput under production load, and disk

- **Pilot timing.** 18:19 → 00:07, i.e. 5.80 h wall, with 7 workers on the MacBook Air M3 at nice 10.
  - The total job wall was 30.4 h against 16.5 h estimated (**wall/estimate 1.85**).
  - Throughput was 3.6-3.8 est-CPU-s per wall-s in the B1 phase. In the B2 phase only 4 jobs ran at once (the 19 GB
    memory budget at 4 GB each), so the overall figure is **2.84**.

| quantity | measured (G3, under load) | manifest constant |
|---|---|---|
| t₁ (finder per ρ = 1 trial) | mean **5.60 s**, median 5.28, q90 8.12 | 3.26 s |
| t₂ (finder + weights per ρ = 2 trial) | mean **37.1 s**, median 36.6, q90 50.2 | 20.1 s |
| chain per PU event | 10.2 s (B1), 9.3 s (B2) | 4.83 s |
| job wall: B1 / B2 | 820 s / 930 s | — |

- **C1 at T_seed = 6.** The G1b report's 95.7 CPU-h becomes about 24-27 h wall at 3.6-4.0, or about 34 h if the B2
  block is memory-gated like G3 (2.84).
- **C1 at T_seed = 4.** About 62 of C1's CPU-h are finder time, so ×1.45 adds about 28 CPU-h, giving about 124 CPU-h
  and **about 31-34 h wall** (ESTIMATE).
- **Disk.** G3 production is 2.40 GB (≈ 4 GB was estimated). The analysis and re-runs take 0.21 GB. 120 GiB are free.

## 7. Readings taken where the frozen text is ambiguous

All readings are conservative and flagged.
1. **T1 rung.** T1 governs R01-R04, and per-hit-set counts apply from R04 on, so r₁ = R04. Reading B (the tightest
   ladder rung) gives the same branch.
2. **Lever arm.** The rule's "move to the next tighter rung with ≥ 10 counts" has no candidate when r₁ is already the
   tightest. A lever-arm failure there (R06, λ = 0.67) is taken as "no such rung", which gives the anti-conservative
   branch. The alternative reading (r₁ = R05) also gives z = +17.6, anti-conservative.
3. **z.** The frozen 1/N_obs term is used. The B1-bootstrap z is reported and does not change any branch.
4. **Trend significance.** The trend counts as significant if either the bootstrap σ or the WLS σ gives |t| > 2. Both do.
5. **T_seed "pass fraction".** The trial pass indicator is tested, and the mean count is also tested. The literal metric
   triggers by itself.
6. **SR-T.**
   - The overlay is built as 15 shifted copies of the measured in-time spectrum (the overlay events are independent PU-200
     events).
   - The binning is not specified by the rule; the plan's 3-bin convention is used.
   - The p-value is Rao-Scott corrected for clustering. The naive p is reported.
7. **T3.** The degenerate same-variable step is reported as "not informative", not as a pass.

## 8. What blocks C1

1. **T_seed = 4 (pre-declared action, triggered).**
   - Needed: the logged frozen-config change, re-hash, manifest regeneration, and the C1 cost update (≈ 31-34 h).
   - Decide whether G3 is re-run at T_seed = 4.
2. **Anti-conservative closure branch (T1 ×1.32, T1w ×1.42, z = +14/+18).**
   - The user approves or declines the pre-declared +50 % statistics steps, which cannot remove a bias. Otherwise the
     upper-envelope × N_obs/N_pred value applies, compounded along the ladder, plus the conservative-trend σ_ln.
   - Any switch to union-governed counting (union closure 0.65, conservative) would be a rule change needing a logged
     re-review.
   - This does not stop C1 producing data, but it fixes how C1's B_PU will be computed and how feasible a WP is.
3. **Not blocking C1 production, but needed before any SR-T signal ε:** the SR-T t_min definition (with the overlay,
   t_min = Δt_acc = 25 ns).
4. **For the record:** the G1b patches (`validation/g1b_post_g3.sh`) can now be applied. No stage-4 run process is
   alive, and the leftover wait loops of this agent are killed.
