# P3B_PILEUP — Phase 3, work package p3-b: B2 pile-up (repaired thinning, occupancy model, day-15 pile-up term)

Executor Casper (Opus), 2026-11-24, 10:19–14:30 -0500 (`date`). Session log
`phase3_selection/logs/executor_casper_2026-11-24_10-19.md`; experiment log `phase3_selection/experiment_log.md`
(entries of 24 Nov, p3-b). Code `phase3_selection/src/p3b/`; machine-readable results `phase3_selection/outputs/p3b/`
(schema `SCHEMA.md`); figures `phase3_selection/outputs/figures/b2_dev_*.{pdf,png}`.

**Role of everything below: development** (STR §4.17 rows 1–2, C1 ρ = 1 and ρ = 2 samples). No B2-a/B2-b *verdict* is
given here; the verdicts are read at 4a on the independent 96,000-trial test sample. What this work package fixes
before the freeze is the s_model of each estimator against its cap, N_eff, crossing-rung evaluability, and the day-15
pile-up term. **Blinding:** no signal sample was opened, no signal quantity formed.

Tags: [V] verified here (file, campaign or command cited), [E] estimate, [U] transcribed, not checked.

## 0. Summary (the numbers decision point 2 reads)

| quantity | value | tag / source |
|---|---|---|
| repaired thinning (B2-a), development ln r = ln(P/N) at R04 / R05 / R06 | +0.259 / +0.319 / +0.773 (σ_tot 0.014 / 0.016 / 0.020); R07 +1.47 (7 direct counts, not evaluable) | [V] `b2_dev_closure.json` → thinning.closure |
| thinning development s_model (r.m.s. over the evaluable cumulative rungs; with crossing rungs) | **0.506** (0.536) | [V] same |
| occupancy model (B2-b): in-sample ln r R04 / R05; **held-out R06** | +0.006 / −0.166; **+0.355 ± 0.034** (R07: +1.36, not evaluable) | [V] → occupancy |
| occupancy development s_model = max(\|ln r(R06)\|, in-sample r.m.s. 0.118) | **0.355** (trend variant 0.374) | [V] |
| cap ln 1.5/3 | 0.135 | STR §4.0 point 4 (c) |
| **cap status** | **both estimators above the cap** | [V] `pileup_term.json` → `both_estimators_above_cap: true` |
| cause of the thinning excess (remediation 1, control) | the thinned ρ = 2 pool, re-found by the ρ = 1 finder, reproduces the direct counts (ln −0.03 / −0.07 / +0.05 ± 0.03 / 0.04 / 0.10); the estimator exceeds the re-found count on the SAME trials by +0.31 / +0.40 / +0.74 | [V] `b2a_refind_control.json` |
| N_eff of thinning (1,000 ρ = 2 events) R04 / R05 / R06 / R07 / R08 | 5,142 / 4,056 / 6,861 / 228 / 4.1 | [V] |
| day-15 pile-up term (occupancy model, R04–R07 inputs), events at N_trig = 4.0848×10⁷ | R07 5.5×10⁴; **R08 347; R09 4.1**; s = 3: R08 301, R09 3.6 (table §6) | [V] `pileup_term.json` |
| CPU used | 4.74 CPU-h in campaigns + ≈ 0.15 interactive tests ≈ **4.9 of 15** | [V] markers; [E] tests |

**Stop-and-report item (PHASE3_BRIEF §2; STR §11.7 rule 1).** *Phase 1 assumed* that the repaired thinning ([SD4]:
grouping at the target density) and an independent occupancy model could each be brought inside s_model ≤ 0.135 on
the development samples. *Phase 3 found* that both over-predict the development direct count at the first held-out
width step (R06) — thinning ×2.17, the occupancy model ×1.43 — so both development s_model values are above the cap.
*Implications:* by STR §11.7 rule 1 ("if both pile-up estimators are above their cap, the outcome class has changed:
the study pauses and the user is asked") the day-15 reading pauses on this item independently of B₅₀; by rule 2 each
estimator is "redesigned if a cause is found by day 15; otherwise the pre-registration declares it not submitted".
A cause is identified for both (§3.3, §4.4); no redesign is adopted here (Phase 3 does not redesign; an adopted
redesign would be chosen after seeing R06). Decision for the orchestrator/user: §8.

## 1. What was run

| campaign | content | jobs | CPU-h | status |
|---|---|---|---|---|
| `p3-b-thin` | repaired thinning of C1 ρ = 2 (`p2-a-c1-pu2`, 1,000 events, 2,000 trials), K = 64, q = 1/2 | 50 | 1.392 | 50/50 done |
| `p3-b-direct` | direct development counts per trial and column (C1 ρ = 1, `p2-a-c1-pu1`, 4,000 events, 16,000 trials) | 4 | 0.015 | 4/4 |
| `p3-b-occin` | occupancy inputs: replayed ρ = 1 finder pools, per-surface densities, 1,000 random planes per trial on real hits | 20 | 1.541 | 20/20 |
| `p3-b-occmod` | occupancy model on the configuration ensemble (8 seeds; occmod-000 re-run with `--force` because its first attempt started before the last occin file existed and read 19 of 20 files) | 8 (+1) | 0.478 | 8/8 |
| `p3-b-refind` | remediation 1 control: ρ = 2 events with dumps (C1 pu2 jobs 0000–0039, 200 events, 400 trials) thinned at hit level, frozen ρ = 1 finder re-run | 20 | 1.317 | 20/20 |
| interactive tests on maxwell (identity, band, replay, model, variants) | — | — | ≈ 0.15 [E] | — |

CPU from the markers (one row per job attempt with a terminal status, summed) [V]. All on maxwell, ≤ 3 concurrent
jobs (one development test was started while three jobs ran at 10:31 and killed within a minute; recorded in the session
log). Slot lines in `SLOTS.md`. Campaign definitions `src/p3b/campaigns/p3-b-*.json` (`make_campaigns.py`).

## 2. Definitions used as frozen (nothing chosen here)

- **Counted object [SD4]** (STR l.1128-1131): distinct hit sets after the grouping (`weights.group_sets`, rank order,
  ≥ 50 % of the smaller set shared with the group leader) applied at ρ = 1; per rung the number of groups with ≥ 1
  passing member (exactly `production.process_trial`'s `n_grp`). The union (passing candidates, no grouping) is a
  diagnostic only.
- **Thinning unit** (STR l.1135-1136, "v1's thinning unit, transcribed from the v1 code"): the interaction id INT of
  the finder pool, keep probability q = 1/ρ (`acts/stage4/finder/weights.py` l.5-8: "w_r = Σ_{T⊂S} q^|T|(1−q)^{|S|−|T|},
  q = 1/rho … Each top-up crossing is its own interaction"; `count_weights`, `_subset_core`) [V: read]. One Bernoulli
  draw per interaction **shared by all candidates of the trial** (a thinned trial is one ρ = 1-like event, so that the
  grouping acts on one event), K = 64 draws per trial, plane and axis fixed at their ρ = 2 values (v1 plan step 3b,
  `weights.py` l.6-7 "no refit after thinning"), all rung variables recomputed on the kept hits with the arithmetic of
  `kernels.cand_vars` / `production.full_set_flags` [V: `thin_core.py`].
- **Closure statistic, evaluability, tolerance, (b), s_model, cap, verdict classes, s_tot**: STR §4.0 points 2–7;
  K = 13 (COM l.340). The JFC alarm band is applied to (b) (STR l.435).
- **Rungs and columns** (`src/p3b/cols.py`): cumulative R04–R14; crossing rungs R0k⊗2S≥j (k = 4,5,6) and R0k⊗p>P
  (k = 5,6); the s = 3 family R0k ∧ N_2S2 ≥ 3 (k = 4…9); FB0–FB4.

## 3. B2-a repaired thinning

### 3.1 Code checks [V]
1. **Identity:** with q = 1 the code reproduces the stored ρ = 2 `n_grp` **and** `n_pass` of c1pu2-0000 trials 0 and 1
   at R04–R14 exactly (2731 / 1019 / 2 and 3061 / 1120 / 0 groups) — `test_thin.py`.
2. The direct job recomputes R04–R14 from the stored candidates and raises unless they equal `trials.n_grp`/`n_pass`
   and the stored rung bits — passed on all 200 files.

### 3.2 Development closure (1,000 ρ = 2 events vs 4,000 ρ = 1 events)

| rung | direct rate (count) | thinning rate | ln r | σ_tot | evaluable | (a) |
|---|---|---|---|---|---|---|
| R04 | 170.9 (2,733,703) | 221.4 | +0.259 | 0.014 | yes | within ln 1.5 |
| R05 | 49.46 (791,291) | 68.06 | +0.319 | 0.016 | yes | within ln 1.5 |
| R06 | 0.2479 (3,966) | 0.5372 | **+0.773** | 0.020 | yes | beyond L + 2σ (FAIL range) |
| R07 | 4.4×10⁻⁴ (7) | 1.90×10⁻³ | +1.47 | 0.38 | no | — |
| R04⊗2S≥3 / R05⊗2S≥3 / R06⊗2S≥3 | 146.6 / 43.34 / 0.2193 | 185.2 / 57.83 / 0.4594 | +0.234 / +0.289 / +0.740 | 0.015 / 0.017 / 0.022 | yes | pass / pass / FAIL range |
| R05⊗p>10⁻³ / R05⊗p>0.01 | 0.0403 (644) / 0.0066 (106) | 0.0803 / 0.0139 | +0.690 / +0.746 | 0.041 / 0.101 | yes | FAIL range |
| R06⊗p>10⁻³ | 0.0029 (47) | 0.0067 | +0.83 | 0.151 | no | — |

Rates are groups per trial; σ_tot² = 1/N + s_P² (STR §4.0 point 2), s_P = relative bootstrap error over ρ = 2 events
(2,000 replicas). (b) over the 14 evaluable rungs: χ² = 4,839 / 14 with V_boot, 3,392 / 14 with V_boot + s_model²J
(p ≈ 0, FAIL range; JFC alarm χ²/ndf > 3) [V]. Development **s_model = 0.506** (cumulative evaluable rungs R04–R06;
0.536 with the crossing rungs) — **above the cap 0.135** under either reading (the frozen text does not say which
rungs; both reported, the cap status does not depend on it). The union count over-predicts too (405 vs ≈ 285 passing
candidates per trial at R04, ×1.42), in the direction and at the size of v1's T_seed-6 union pilot (×1.53, STR l.1124 [U]).

Compared with v1 (STR l.1121-1123 [U]: under-prediction ×1.50 / ×1.61 at R04 / R05, over-prediction at R06–R07), the
repair moves R04–R05 from under- to over-prediction and does not remove the steepening with depth.

### 3.3 Remediation attempts (≥ 3; JFC) — what was tried, what it showed
| # | attempt | result [V] | reading |
|---|---|---|---|
| R0 | code-bug search: q = 1 identity, direct recount identity, union against v1's pilot | all as expected (§3.1, §3.2) | no code bug found |
| R1 | **hit-level control** (`refind_job.py`): each of 400 ρ = 2 trials with dumps replayed exactly (PV, phimet, trial seed checked), every interaction kept with probability ½, the frozen ρ = 1 finder re-run (`process_trial` at ρ = 1) | re-found / direct: ln −0.032 ± 0.032 (R04), −0.069 ± 0.035 (R05), +0.048 ± 0.104 (R06, 104 counts); repaired thinning / re-found **on the same trials** (paired bootstrap): +0.306 ± 0.009, +0.399 ± 0.011, +0.741 ± 0.104 | **Cause identified.** The thinned ρ = 2 pool is a ρ = 1 pool (a ρ = 2 trial is two independent ρ = 1 chain events, each with its own top-up, CKF removal and merging), so the sample and the thinning unit are right. The excess is the estimator definition: thinning counts the hit sets of the ρ = 2 candidate planes that still pass after thinning (≈ 300 thinned R04 passers per subset from ≈ 1.25×10⁴ ρ = 2 candidates), whereas the ρ = 1 finder finds and keeps fewer distinct sets (seeding, 3-iteration refit from its own seeds); the gap grows as the width cut tightens. |
| R2 | refit (finder arithmetic, 3 iterations) + finder dedup (2 mrad) of every thinned R04 passer before grouping (`thin_trial_var` mode 1; mode 2 without dedup) | fails its own sanity check: at q = 1 (no thinning) 2,361 / 2,644 groups against the stored 2,731 / 3,061 (the stored planes are not fixed points of a further refit, and a refit on the stored band can only lose hits); at q = ½ ≈ 96–102 groups per trial (×≈ 0.56 of the direct) | not a valid emulation; not adopted |
| R3 | re-ranking the thinned sets by (−N_L2, χ²/ndf) before the grouping (mode 3) | ≤ 1 % change | the rank order is not the cause |

Conclusion for B2-a: development s_model 0.506 > 0.135, the cause is identified (R1), and no redesign that stays
inside the frozen definition ("thinning has no fitted parameter", STR l.1138-1139) is available: correcting the excess
would need a ρ-dependent finder-efficiency factor, i.e. a patch of the ×2.41 type that STR l.1175 forbids. Under the
frozen rule thinning is **not submitted** (no credit), unless the user/orchestrator orders a redesign at decision
point 2 (§8).

### 3.4 N_eff (B2-g) and crossing-rung evaluability

N_eff = 1/s_boot² on 1,000 ρ = 2 events [V]: R04 5,142; R05 4,056; R06 6,861; R07 228; R08 4.1 (four passing subsets
in 128,000); R06⊗2S≥3 5,589; R07⊗2S≥3 189; R05⊗p>10⁻³ 6,142; R06⊗p>10⁻³ 698; R06⊗p>0.05 57; FB0 505, FB1 237,
FB2 46. Compared with STR's projection (N_eff ≈ 80 at R07 for 3,000 events, ≤ 10 at R08, l.1187-1190 [E]): R07 is
better (683 projected to 3,000 events), R08 as projected (≈ 12).

**B2-g projection to the 3,000-event production (N_eff ∝ events) against the 96,000-trial direct sample at the
development direct rates** [V: `B2g_projection`]: evaluable (σ_tot ≤ 0.135) at R04 (σ 0.008), R05 (0.009), R06
(0.010), R06⊗2S≥3 (0.010), R06⊗p>10⁻³ (0.063); **not evaluable at R07** (σ_tot 0.159, set by the 42 expected direct
counts at the development rate 4.4×10⁻⁴, not by N_eff 683; at v1's rate 7.3×10⁻⁴ the 70 counts of STR l.1182 would
give 0.126) and R07⊗2S≥3 (0.187). Deepest evaluable cumulative rung for PREREG_v2: **R06** (R07 marginal, depends on the
direct rate). [DT2] (STR l.1198-1200): "if repaired thinning has no evaluable rung beyond R06 on the development
sample, its validated range is declared as R04–R06" applies — but with s_model above the cap the validated range is
moot unless thinning is redesigned.

**B2-c (agreement at depth, R08+):** thinning N_eff at R08 is 4 (12 projected) → σ ≥ 0.29 → **NOT EVALUABLE** as STR
expected (l.1192). For information at R07 (development, not a criterion rung): thinning / occupancy = 1.90 / 1.71
×10⁻³, ln ratio +0.10.

## 4. B2-b occupancy model

### 4.1 Model (new code `occ_core.py`, `occ_model.py`, `occmod_job.py`; definition frozen at 10:56 before any
comparison with a direct count, session log)
- **Configuration ensemble θ** (a "ribbon through the vertex and along the road", STR l.1140-1142): PV from the luminous
  region (σ_xy 5 µm, σ_z 45 mm, `pu_inputs.lum_pv`), MET azimuth uniform, axis azimuth φ_MET ± 0.15 (δ95), axis
  η ∈ U(−1, 1), plane rotation ψ ∈ U(0, π) about the axis with |n_z| ≥ 0.2. Band = the finder's: |u·n| < 3σ(n),
  u·a > 0, |u·n2| < 75 mm, and the road.
- **Densities** ρ_j(z): hits per mm² per event on each of the 16 barrel surfaces, φ-averaged, 2 mm z bins, from the 4,000
  replayed ρ = 1 development pools (finder input: after CKF removal and merging, top-up included). Replay checked: PV and
  phimet of every one of the 16,000 trials bit-identical to the stored trials (the job raises otherwise) [V].
- **Expected in-band hits**: at azimuth φ on a surface of radius R the band is |z − z*(φ)| < δ(φ) with
  z*(φ) = pv_z − [n_x(R cos φ − pv_x) + n_y(R sin φ − pv_y)]/n_z and δ = 3σ/|n_z|. *Derivation:* at fixed φ,
  u·n = n_x u_x + n_y u_y + n_z(z − pv_z) is linear in z with slope n_z and vanishes at z*, so |u·n| < 3σ ⇔
  |z − z*| < 3σ/|n_z|. λ = Σ_φ R Δφ ∫ρ_j dz over the interval (0.5 mm arc steps; 1/3/9 sub-steps across the band for
  TBPX/PS/2S).
- **Layers**: TBPX: N ~ Poisson(λ), P(≥ 2) = 1 − e^{−λ}(1 + λ). Stacked: crossings are hit pairs at one (φ, z) (top-up by
  construction, `pu_inputs.topup`); pairs in both sensor bands (b), only in the inner (i), only in the outer (o) are
  independent Poissons, crossings = min(b + i, b + o) (`cand_vars`), so
  P(≥ 2) = P(b ≥ 2) + P(b = 1)P(i ≥ 1)P(o ≥ 1) + P(b = 0)P(i ≥ 2)P(o ≥ 2) (the three exhaustive cases of b).
  *Checks:* λ → 0 gives P → 0 as λ²/2 (TBPX); λ_i = λ_o = 0 reduces the stacked formula to P(b ≥ 2) (pairs only).
  R04 = all seven IP layers ≥ 2 (N_IP2 ≥ 7 ⇒ N_IT2 = 4 ≥ 3). N_2S2: Poisson-binomial of the three 2S layers.
- **Width rungs**: w_core = 1.4826 MAD of u·n2 over the pooled IP hits (pairs twice) — toys conditional on R04 (exact
  conditional count law), positions drawn from the band's position density; R05–R08 by importance sampling (window of
  half-width W/1.4826 at a centre from a grid, mixture (1 − β)g + βg·1_win/G, β = 0.5; weight = g / proposal, exact);
  plain Monte Carlo as the check.
- **Measured correlation factors** C(r) = P_real(r)/E_model(r): the same ensemble on the **real** hits of the 16,000
  development trials (16×10⁶ planes; `band_hits` checked against a brute-force band on every hit, 0/300 mismatches).
- **Normalisation** N_cfg (effective configurations per trial): GLS fit of ln(B_dir/P_real) at R04–R05 (joint event
  bootstrap). Prediction beyond R05: B(r) = N_cfg · C(R05) · E_model(r) (C held at R05; the log-linear R04→R05 trend of C
  is the reported variant). Fit-probability rungs: pass fractions of the development R06 finder groups (Df-2, shared
  input). s_model = max(|ln r(R06)|, in-sample r.m.s.) (STR l.1146-1148).

### 4.2 Checks of the model [V]
- Per-layer P(≥ 2 crossings) on the ensemble, model vs real hits (20 test events): TBPX 0.997/0.854/0.437/0.254 vs
  0.997/0.846/0.438/0.250; TBPS 0.337/0.141/0.052 vs 0.341/0.143/0.050; TB2S 0.950/0.857/0.656 vs 0.939/0.841/0.636.
- IS vs plain Monte Carlo (8 seeds × 800 configurations, 200 toys each): R05 1.845 vs 1.848 ×10⁻⁴; R06 1.558 vs
  1.629 ×10⁻⁶ (MC errors 0.9 % / 2.4 %); R07 7.54 vs 7.24 ×10⁻⁹. Model MC error at R08 7 %.
- Correlation factor measured on real hits: **C(R04) = 1.184, C(R05) = 1.207**; post hoc (diagnostic only, not an
  input) C(R06) = P_real/E_model = 1.94×10⁻⁶/1.56×10⁻⁶ = 1.24 (31 real planes, ±18 %): the model describes the
  occupancy of random ribbons on real ρ = 1 hits to a constant factor from R04 to R06.

### 4.3 Development closure [V: `b2_dev_closure.json` → occupancy]
N_cfg = 1.880×10⁵ (GLS weights 0.964 R04 / 0.036 R05).

| rung | direct | model (B2-b) | ln r | σ_tot | role |
|---|---|---|---|---|---|
| R04 | 170.9 | 171.9 | +0.006 | 0.010 | derivation (in sample) |
| R05 | 49.46 | 41.87 | −0.166 | 0.019 | derivation (in sample) |
| **R06** | 0.2479 | 0.3534 | **+0.355** | 0.034 | **held out** |
| R07 | 4.4×10⁻⁴ (7) | 1.71×10⁻³ | +1.36 | 0.38 | not evaluable |
| R04 / R05 / R06 ⊗ 2S≥3 | 146.6 / 43.34 / 0.2193 | 145.0 / 35.60 / 0.3028 | −0.011 / −0.197 / +0.322 | 0.010 / 0.020 / 0.035 | 2S crossing comparisons |

R06 is within ln 1.5 (tolerance (a)) but 10σ from zero statistically: **s_model = 0.355 > cap 0.135** (trend variant
0.374). The 2S factor itself is predicted to ≤ 3 %: ln r(R0k⊗2S≥3) − ln r(R0k) = −0.017 / −0.030 / −0.032 at k = 4/5/6;
the crossing ln r follow their base rungs. JFC band: the held-out pull with statistical errors only is 10.6σ (alarm);
with s_model in V the single held-out rung gives χ² = 1 by construction (tautological, not a test).

### 4.4 Remediation attempts for B2-b
| # | attempt | held-out ln r(R06) | reading |
|---|---|---|---|
| O1 | pre-declared trend variant of C | +0.374 | no |
| O2 | normalisation variants: R04 only / diagonal weights / R05 only | +0.349 / +0.389 / +0.521 | the R06 excess does not come from the fit |
| O3 | replace the model's width fall by the real-hit random-plane fall (N_cfg · P_real(R06), diagnostic) | +0.385 | the occupancy of random ribbons is right (§4.2); the excess is in the map from configurations to the finder's distinct groups |
| O4 | random planes vs finder groups, direct comparison: R05/R04 = 0.244 (real planes) vs 0.289 (finder); R06/R05 = 0.0087 ± 18 % vs 0.0050 | — | **cause identified**: the number of finder-distinct groups per passing configuration (N_cfg) is not rung-independent; it rises by e^{+0.17} from R04 to R05 and falls by ≈ e^{−0.5} from R05 to R06 |

The same pattern as thinning (§3.3 R1): both estimators count hit sets that *exist* at ρ = 1 (random ribbons, thinned
ρ = 2 planes); the direct count is what the finder *finds and keeps as distinct*; the two diverge as the width cut
tightens. No redesign from R04–R05 inputs alone can predict the sign change of the N_cfg trend between R05 and R06; a
redesign that uses R06 would no longer have a held-out development rung. Under the frozen rule the occupancy model is
**not submitted** (no credit) unless redesigned at decision point 2 (§8).

## 5. Closure-slope weights (EXP §10 item 8; options stated, none chosen)
STR §4.0 point 7 fits b̂ ± σ_b "the fitted slope of ln r against the rung index" for n ≥ 3 evaluable rungs without
fixing the weights. Every option's outcome (sandwich σ_b, valid for any weights) [V]:

| sample | unweighted OLS | WLS, bootstrap diagonal | GLS, full bootstrap covariance |
|---|---|---|---|
| v2 repaired thinning, development R04–R06 | +0.257 ± 0.009 | +0.244 ± 0.009 | +0.082 ± 0.002 |
| C1 (v1-type thinning), R04–R06, C1 sign convention ln(N/P) (MAT l.127-146, RAG [U]) | −0.423 | −0.365 ± 0.008 (frozen seed) | not computed |

The weight dependence is a factor 3 on v2's development points (the nested rungs are strongly correlated and the
three points are not on a line), as in C1. Options for PREREG_v2: (1) unweighted OLS with the sandwich σ_b; (2) WLS
with weights fixed before the test from the development bootstrap; (3) GLS with the test-sample covariance; (4) any of
them with σ_b enlarged by the spread between options. The choice is the orchestrator's/user's; with both estimators
above the cap it matters only if one is redesigned.

## 6. Day-15 pile-up term per T2 candidate (`outputs/p3b/pileup_term.json`)
STR l.2737-2741: the term is the development occupancy model's estimate with its R04–R07 inputs. Implemented as the
same model with one scale A fitted on the development direct counts at R04–R07 (weights 1/(σ_stat² + s_model²);
residuals R04 −0.22, R05 −0.41, R06 +0.11, R07 +1.12 — a single scale cannot fit R04–R07, consistent with §4.4).
Rates per trial; events = rate × N_trig with N_trig = 4.0848×10⁷ (the frozen projection script's value,
`strategy_budget.py` l.68 [U]); **p3-a rescales to its MET-model N_trig**.

| candidate | rate / trial | events | width s_tot: planning (cap) | width: measured (dev) | thinning (dev) | direct dev count |
|---|---|---|---|---|---|---|
| R04 | 137.2 | 5.6×10⁹ | 0.135 | 0.355 | 221.4 | 2,733,703 |
| R05 | 32.8 | 1.3×10⁹ | 0.135 | 0.355 | 68.1 | 791,291 |
| R06 | 0.277 | 1.13×10⁷ | 0.135 | 0.355 | 0.537 | 3,966 |
| R07 | 1.34×10⁻³ | 5.5×10⁴ | 0.135 | 0.539 | 1.90×10⁻³ | 7 |
| **R08** | 8.49×10⁻⁶ | **347** | 0.427 | 0.885 | 3.1×10⁻⁵ (N_eff 4) | 0 |
| **R09** | 1.01×10⁻⁷ | **4.1** | 0.589 | 0.974 | 0 | 0 |
| R04 ∧ N_2S2≥3 | 115.7 | 4.7×10⁹ | 0.191 (2S credit) / 1.224 | 0.419 | 185.2 | 2,345,475 |
| R05 ∧ N_2S2≥3 | 27.9 | 1.1×10⁹ | 0.191 / 1.224 | 0.419 | 57.8 | 693,390 |
| R06 ∧ N_2S2≥3 | 0.237 | 9.7×10⁶ | 0.191 / 1.224 | 0.419 | 0.459 | 3,509 |
| R07 ∧ N_2S2≥3 | 1.15×10⁻³ | 4.7×10⁴ | 0.191 / 1.224 | 0.583 | 1.63×10⁻³ | 5 |
| **R08 ∧ N_2S2≥3** | 7.36×10⁻⁶ | **301** | 0.448 / 1.289 | 0.913 | 3.1×10⁻⁵ | 0 |
| **R09 ∧ N_2S2≥3** | 8.72×10⁻⁸ | **3.6** | 0.604 / 1.677 | 0.999 | 0 | 0 |

Widths: s_tot² = s_model² + Σs_f² + (b̂² + σ_b²)d_in² + b₀²d_out², b₀ = ln 1.5 (STR §4.0 point 7). *Planning (cap)* is the
convention of the frozen projection (s_model at the cap, width family tested at R06–R07 at 4a, b̂ := 0, σ_b := b₀):
checks — R08: √(0.135² + 0.405²) = 0.427 = STR l.518 "0.43"; R09: √(0.135² + 2·0.405²) = 0.589 = "0.59"; with no
crossing credit the s = 3 rows add d_out = 3. *Measured (dev)*: s_model 0.355, width family tested at R06 only
(d_in = 1, 2 at R07, R08), 2S credit with s_f = 0.224 (all nine development 2S comparisons within ln 1.5). R09 uses the
fit-probability fraction 0.0119 (47 of 3,966 development R06 groups pass p > 10⁻³) — shared input (Df-2). The MC error
of the model is ≤ 7.3 % at every candidate. **These widths assume a submitted estimator; with both above the cap the
frozen rule gives the term no credit** — which value the binding reading uses is decided at decision point 2, not here.
For orientation [E]: every estimator over-predicts the finder's count at R06 (×1.4–2.2) and R07 (×3–4 on 7 counts), so
the occupancy R08/R09 values are more likely high than low; this is not a credit.

## 7. Definitions for PREREG_v2 and production (written, not launched)
- **B2-d** direct sample: `src/p3b/campaigns/prod/p4a-b2-prod-pu1.json` — 24,000 events × 4 roads = 96,000 trials,
  stream `prod.pu1`, 1,200 jobs of 20 events (≈ 1,114 s each at 55.7 s/event, EXP §3.1), ≈ 371 CPU-h, `--dump 0`
  (flag: the C1 sample kept dumps, 2.64 MiB/event; nothing in B2's test needs them; 63 GB if wanted).
- **ρ = 2 sample**: `p4a-b2-prod-pu2.json` — 3,000 events × 2 roads, stream `prod.pu2`, pre-merge store N_IP2 ≥ 6, 600
  jobs of 5 events (≈ 1,015 s each), ≈ 169 CPU-h, max RSS 2.1 GB → ≤ 2 jobs per node, ≈ 203 GB pre-merge store.
  Thinning afterwards with `thin_job.py` (K = 64).
- Launch (orchestrator, after the PREREG_v2 hash): `tools/runner/bin/qv2run ssh launch <abs path>.json --nodes
  landau,maxwell,schrodinger [--max-per-node N] --on <node>` (absolute campaign path: a relative one fails in the remote
  driver). Both files load in `qv2run status` (1,200 / 600 jobs pending) [V].
- For PREREG_v2: [SD4] object and the thinning unit as in §2; the occupancy model definition of §4.1 with its frozen
  choices (session log 10:56); N_eff per rung and the B2-g projection (§3.4); evaluability of the crossing rungs
  (thinning: 2S crossings at R04–R06 and R05⊗p>10⁻³, R05⊗p>0.01 evaluable on development; R06⊗p not; occupancy: 2S
  crossings R04–R06 evaluable, fit-probability/shape comparisons consistency only); the slope-weight options (§5).
- **Enlarged development sample (100 CPU-h line): not requested.** It cannot change either cap status (s_model is a
  bias, the R06 statistics are already at σ 0.02–0.03), and development R07 would need ≈ 1.25×10⁵ trials (31,000 events)
  for 55 counts at the development rate. Shape crossing rungs (R15–R20 ⊗ R06) were not computed (the h/o variables
  need the hit records and the WP_RULE F1 definitions; consistency-only for the occupancy model) — open item.

## 8. Decisions needed (orchestrator / user)
1. **Rule-1 pause condition met on the pile-up item**: both estimators above the cap at day 15 (STR §11.7 rule 1; already
   expected to pause on B₅₀). The pause package should carry §0's statement.
2. **Rule 2 per estimator**: declare "not submitted" (no credit; pile-up term at its no-credit value; selections stay
   available flagged) or order a redesign. Causes are identified for both (§3.3, §4.4). Redesign options I see, none
   adopted: (a) thinning with a full ρ = 1 re-find of each thinned subset (an exact estimator but ≈ 11 s per subset —
   with K = 64 ≈ 1,200 CPU-h for 3,000 events, and its gain over direct counting is small); (b) an occupancy model whose
   configuration-to-group map N_cfg(r) is measured (e.g. by running the finder's refit from random seeds on real hits),
   with R06 then no longer held out; (c) accept a larger declared s_model (STR §4.0 point 4 (c) allows "a larger
   declared value" but the cap still applies).
3. Which width bookkeeping the binding projection uses for the pile-up term (§6), if any credit remains.
4. Slope-weight option (§5) for PREREG_v2.

## 9. Figures
![Development closure of both pile-up estimators: ln r = ln(prediction / direct development count) per rung and
crossing rung, repaired thinning (circles, 1,000 ρ = 2 events, K = 64) and the occupancy model (squares; R04 and R05
are its derivation rungs, R06 is held out). Error bars are σ_tot of STR §4.0 point 2. Dashed lines: the tolerance
±ln 1.5; dotted: the cap ±ln 1.5/3. R07 points (7 direct counts) lie above the frame.](figures/b2_dev_lnr.pdf)

![Pile-up groups per trial against the rung: development direct count (C1 ρ = 1, 16,000 trials, Poisson errors),
repaired thinning (bootstrap errors), the occupancy model with R04–R05 inputs (B2-b) and the day-15 version with one
scale on R04–R07 (error bars: the development-bookkeeping width s_tot). R08–R09 have no direct count; the R09 values
use the fit-probability fraction of development R06 groups.](figures/b2_dev_rates.pdf)

![Effective count N_eff = 1/s_boot² of the repaired-thinning prediction per rung on 1,000 ρ = 2 events (filled) and
projected to the 3,000-event production (open, ×3); the dashed line is the N_eff at which s_P alone equals the
evaluable limit ln 1.5/3. R08 has N_eff ≈ 4 (four passing subsets in 128,000).](figures/b2_dev_neff.pdf)

## 10. Self-check
- Frozen definitions used as written: [SD4], thinning unit, K = 64, §4.0 points 2–7, K = 13; no criterion reworded;
  every open choice reported under each reading (s_model rung set, C trend, N_cfg weights, width bookkeeping, slope
  weights). Model definition frozen before any comparison (session log 10:56).
- ≥ 3 remediation attempts per failing estimator: thinning R0–R3, occupancy O1–O4 (§3.3, §4.4); no scale factor
  applied; no parameter tuned to a direct count beyond the declared R04–R05 (B2-b) and R04–R07 (day-15) normalisations.
- Formulas: z*, δ, the Poisson layer probabilities, s_tot — derived or cited, with limiting-case and substitution
  checks (§4.1, §6). IS checked against plain MC (§4.2).
- JFC alarm bands: thinning (b) χ²/ndf 242–346 → alarm, reported as such, not reframed; occupancy held-out pull 10.6σ
  (statistical) → alarm; `passes`-type flags in the JSON (`above_cap: true`, `b_verdict: FAIL`) agree with this text.
- Blinding: no signal file opened. Numbers tagged; CPU 4.9 of 15 CPU-h.
- JFC "≥ 2 selection approaches", MVA, cutflow, data/MC: **not this work package** (T2 / consolidation; no collider
  data). Plotting: mplhep, (10, 10), "Private work (simulation)", PDF + PNG, explicit yerr, no titles; `conventions/lint_plots.py` run on a
  copy of `plots.py` (the linter only scans `*/src/*.py`, one level): no violations.

## 11. Open issues
1. Both estimators above the cap → decision point 2 (§8).
2. Shape crossing rungs (R15–R20 ⊗ R06) not computed (§7).
3. `occmod-000`'s first attempt read 19 of 20 density files (re-run with `--force`; its first output was replaced).
4. The development direct rate at R07 (7 / 16,000) is below v1's (35 / 48,000) by 1.07σ (MAT l.64); the B2-g R07
   evaluability depends on it.
5. `p3-b-thin` jobs started after 10:56 record a different `thin_core.py` sha256 (column names moved to `cols.py`, no
   logic change); the remediation variants were appended to `thin_core.py` after the campaign (diagnostic code path
   only).
