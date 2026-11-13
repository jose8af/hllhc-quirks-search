# D4: the v1 frozen record (investigator Alfred, 2026-11-13)

**Scope.** This digest covers the tracked v1 Stage-4 record: the frozen rule, the background model, the closure
failure, the signal, and a proposed C1 comparison subset. The 46 GB of bulk data are lost, so everything here comes from
tracked files.

**Path abbreviations.**
- `TT` = `stage2_C001_quirks/theory_track`
- `S4` = `TT/acts/stage4`
- `AN` = `TT/data/acts_stage4/analysis/C12FC_v1`
- `SUM` = `TT/data/acts_stage4/analysis/STAGE4_SUMMARY.json`

**Tags.**
- **[V]**: I re-read or re-derived the number from the JSON, or ran the command myself. The pointer is given.
- **[U]**: transcribed from a report and not re-checked.
- **[E]**: my estimate.

**Extraction scripts** (read-only, stdlib, `python3 -I`):
- `/tmp/claude-10015/-home-users-jdochoa-hllhc-quirks-search/7753271e-2ffb-43c4-ae3d-1d6171a35987/scratchpad/bkg_table.py`
- `/tmp/claude-10015/-home-users-jdochoa-hllhc-quirks-search/7753271e-2ffb-43c4-ae3d-1d6171a35987/scratchpad/sig_table.py`

They regenerate every table below from `AN/*.json`. They live in the scratchpad, so copy them to `QV2/…/src` if they
should be kept.

---

## 1. The frozen rule

### 1.1 Notation and fixed cuts

- A rung is **cumulative**: passing Rk means passing every requirement of R01…Rk (`S4/WP_RULE.md` l.17).
- The fixed cuts apply at every rung (l.106):
  - N_IT2 ≥ 3: at least 3 pixel layers with ≥ 2 crossings;
  - |Δφ(n₃, MET)| < δ₉₅ = 0.15 rad;
  - |η(n₃)| < 1.0, so the selection is barrel only (PC-7);
  - f_CKF < 0.2. This cut is applied to the signal, SM and C′ samples, but no rejection is credited to B_PU (l.123).
- Window W_c = 75 mm (l.48).
- T_seed:
  - The text says T_seed = 6 (l.59).
  - **The operative value is 4**: the pre-declared G3 action, `S4/frozen_inputs.json` → `t_seed`,
    `finder_config.tseed` [V].
- Two categories, SR-T (late BTL timing hit) and SR-G (the rest). Each walks its own copy of the ladder (l.297).

### 1.2 The ladder (`S4/WP_RULE.md` §3, l.277-295) [V]

| rung | cut added | rung | cut added |
|---|---|---|---|
| R01 | N_IT2 ≥ 3 ∧ N_IP2 ≥ 4 | R13 | N_2S2 ≥ 2 |
| R02 | N_IP2 ≥ 5 | R14 | N_2S2 ≥ 3 (= full F0) |
| R03 | N_IP2 ≥ 6 | R15 | h > 2 (non-helicity χ²/ndf) |
| R04 | N_IP2 ≥ 7 (every IT + PS barrel layer) | R16 | h > 3 |
| R05 | w_core < 37.5 mm (W_c/2) | R17 | h > 5 |
| R06 | w_core < 18.75 mm | R18 | o > 2 (opening linearity χ²_lin/ndf) |
| R07 | w_core < 9.4 mm | R19 | o > 3 |
| R08 | w_core < 4.7 mm | R20 | o > 5 |
| R09 | p(χ²_core) > 10⁻³ | R21 | dE/dx > 1.3 MIP (core TBPX, 60 % truncated) |
| R10 | p(χ²_core) > 0.01 | R22 | dE/dx > 1.6 MIP |
| R11 | p(χ²_core) > 0.05 | R23 | dE/dx > 2.0 MIP |
| R12 | N_2S2 ≥ 1 | | |

### 1.3 Working-point rule (§5.1, l.374)

- r*_c = the **loosest rung with B₈₄,c ≤ 0.11 events in 3 ab⁻¹, at r*_c and at every tighter rung**.
- B₈₄ is the 84th percentile of the Monte Carlo sum of the log-normal terms (§4.1, l.347-349).
- 0.11 = 0.3/2.71, chosen so that two categories at σ_ln = 2.3 give 0.3 combined (l.377).
- If both categories have a WP, there is also a combined guard: B₈₄(T+G) ≤ 0.3, with a deterministic continuation of
  at most 44 steps (§5.2).
- Zero-count rule (§4.2, l.352-366):
  - Each conditional is measured on the tightest population with M_j ≥ 10.
  - A factor with N_j ≥ 1 enters as N_j/M_j.
  - **Among a term's zero factors, only the one with the largest M_j enters, as 1.14/M_j with σ_ln = 1.0.** Every other
    zero factor of that term enters as 1, so a bound enters at most once per term.

### 1.4 Fallback (§8, l.680-684)

- r_fb(m, Λ, c) = N_IT2 ≥ 3 ∧ N_IP2 ≥ 7 ∧ p > 0.05 ∧ N_2S2 ≥ 3 ∧ (w_core < W_c/2^k_adm if k_adm ≥ 1) ∧ h > 5 ∧ o > 5
  ∧ (dE/dx > e_adm if any), plus the time tag for SR-T.
- k_adm is the largest k ∈ {0…4} with Λ ≥ Λ_R(m)·2^((k+1)/2). Λ_R is smoothed from `TT/sim/stage3/results/P2.json`.
- e_adm comes from the dilution-aware R_eff/1.25 table.
- The k_adm and e_adm tables are transcribed in WP_RULE A.1 and A.2b (l.829-901) and in `frozen_inputs.json` → `eadm`
  [V].
- This gives 20 columns: FB0-FB4 × {no dE/dx, 1.3, 1.6, 2.0}.
- FB_k is **not nested** in the ladder.
- Per-point best-of is forbidden (l.689).

### 1.5 Freeze chronology [V unless marked]

| when | what | sha256 (verified against the file now) |
|---|---|---|
| ≤ 2026-10-13 | `S4/plan.md` (review R9 PASS) | 77d3dc9e… **MATCH** |
| 2026-10-13 18:19:05 | WP_RULE frozen "signal not yet looked at" (`frozen_inputs.json` → `status`, `frozen_at`) | `WP_RULE.md` 1b2ea9bd… **MATCH** |
| 2026-10-14 00:16 | HASH_ADDENDUM §1-3, applied: G1b hook, ACTS navigation-assertion recovery | run_stage4.py 85b978f5→1258e82a; run_chain.py b1130b40→bdea0e27 |
| 2026-10-14 00:18:48 | T_seed 6 → 4, the only pre-declared T_seed action (G3 §4; HASH_ADDENDUM §5 l.138) | `frozen_inputs.json` 7574e0b5→2adc8f9d (**MATCH** now); run_stage4.py→0d122cfc |
| 2026-10-14 00:31 | C2B scheduling-order change only (HASH_ADDENDUM l.174) | run_stage4.py e371c2b2… **MATCH** now |
| 2026-10-14 01:50 | PC-19 SR-T window amendment (user-approved) | `WP_RULE_PC19.md` d30bcc2f… **MATCH**; `g3/srt_tmin_check.py` 9d0c902a… **MATCH** |
| 2026-10-16 10:37:42 | analysis-code freeze, round "FIXER R6" (previous bce02b6f = C12_v1) | `S4/analysis/inputs/analysis_freeze.json` b42aef4d… **MATCH** |
| 2026-10-16 11:48:22 | C12FC_v1 run (`AN/background.json` → `provenance.created`) | bsum_wp 9077ba14, limits 4f99fe6a, signal_eff 1d487acb, background d4308ec6, manifest 049760fb: all **MATCH** `SUM` → `primary_run.input_sha256` |
| 2026-10-16 (after results PASS) | FIX R3-NORM: f_tail added to N_exp (STAGE4_RESULTS l.7-22) | `HASH_ADDENDUM.md` e273c077…, `STAGE4_RESULTS.md` 0890a90e… |

### 1.6 Hash verification (`sha256sum`, run 2026-11-13)

**`analysis_freeze.json` → `sha256`: 32/32 MATCH, 0 mismatch, 0 lost** [V]. The list covers:
- the 14 analysis modules;
- the 5 analysis input JSONs;
- the finder files finder.py, weights.py and production.py;
- s4pu.py, s4cp.py and s4sig.py;
- jobs C1 and A2FC;
- V46_REVERT_SET;
- `STAGE3_INDEX.json` 67f95ccd;
- P2.json.

**`frozen_inputs.json` → `sha256` (= WP_RULE A.3), 21 files:**
- 13 MATCH.
- 2 MISMATCH, both documented by HASH_ADDENDUM: run_stage4.py is now e371c2b2 and run_chain.py is now bdea0e27.
- **6 LOST** (bulk `data/acts_stage4`):
  - `fix_r4/f4r_admissibility.json`
  - `review_r1_constructive/r1c_signal_handles.json`
  - `frozen/eadm_dilution.json`
  - `review_wp1/r1_inputs.py`
  - `review_wp1/r1_inputs.json`
  - `g1/v49/v49.json`
- Partial corroboration: `AN/signal_eff.json` → `admissibility_inputs_sha256` records the A.3 values of f4r (45847697) and
  eadm (7661bd63) at run time [V].

**HASH_ADDENDUM "sha256 at writing", new files:** run_g1b.py, g1b_tt.py, g1b_apply_*, g1b_regress.py,
g1b_chainfix_test.py and tseed4_verify.py MATCH. Three helper scripts **MISMATCH** (see §7, item I3):

| file | at writing | now |
|---|---|---|
| `validation/g1b_post_g3.sh` | 964f2c83 | a268d276 |
| `validation/chain_c1.sh` | 8e25d337 | 8811fb53 |
| `validation/prodstop_fri.sh` | 9b85500f | 0655754e |

---

## 2. The background model as frozen

### 2.1 Structure and normalisation

**B = N_trig × [P_PU + P_SM,HS + Σ_t rate_t × P(pass | t)] + B_cosmic + B_halo** (WP_RULE l.313).
- B_cosmic and B_halo are argued only, not in the sum (`AN/bsum_wp.json` → `ladder.not_in_sum`) [V].
- N_trig = **4.0848 × 10⁷ ± 2.02 %**, counted after the event-level preselection (user decision D1). Source:
  `bsum_wp.json` → `n_trig.value` / `rel_stat`. The 12-process breakdown sums exactly to the total
  (`n_trig.breakdown.*.N_trig`) [V].
- L = 3 ab⁻¹.
- Normalisation σ_ln = 0.262 (±30 %) on every term [V: `comps.normalisation`].

### 2.2 Terms and how each is estimated

**PU (random planes).**
- B1: ρ = 1, **12 000 events / 48 000 trials** (4 MET roads).
- B2: ρ = 2, **3 000 events / 6 000 trials** (`AN/background.json` → `samples`) [V].
- Estimation by rung:
  - R01-R06: exact thinning (DP for the counting rungs, IS for width/χ²; nsub = 64), × the closure factor.
  - R07 and deeper: not reachable at ρ = 2, so rung factorisation from R06, × c = 1.196, × the closure factor.
- The central value is the upper envelope of {P_main, P_fact, P_pow}.
- Pointers: `background.json` → `columns[i]` (B1_groups, P_thin, P_main, P_fact, main_factors, fact_factors) and
  `end_state[i]` (P_per_trial, closure_factor, sigma_ln_components). B_PU = N_trig × `end_state[i].P_per_trial` [V].

**SM, 12 processes.** Hit-level samples exist for three of them, 2 000 events each: Z(νν)+j, W(τν)+j and tt̄ 1ℓ.
- W(τν) is split into classes τ_ℓ (M = 375 events) and τ_h (M = 1 625).
- **8 proxies** with no hit-level sample: W(eν), W(μν), tt̄ 2ℓ, t-channel top, tW (= 0.10 × N_trig(tt̄)), WW, WZ, ZZ.
  Each takes the max P(r | presel) of its nearest sample (`background.json` → `sm.<p>.proxy_of`).
- K = 1.4, except K_tt = 1.9.
- The proxy share of B_SM is 0.147 at R04, 0.32 at R07 and **0.445 at R09** (`SUM` → `sm_proxy_fraction_of_B_SM`)
  [V].
- Absent from the model: Z(ττ), lost-lepton Z(ℓℓ) and QCD multijets (`n_trig.not_included`) [U on their size].

**C′, single-interaction topologies.**
- 8 topologies: DIF, PV pair, looper, γ conversions, V⁰, and NI at r = 22 / 30 / 61.5 mm.
- C′₀ (no PU) samples: 10⁵ events for γ, V⁰, PV pair and looper; 5 × 10⁴ for DIF; 3 × 10⁴ for each NI.
- C′_PU: **500 events per topology**.
- Estimate = f_pre (from C′₀) × the attributed pass fraction at the deepest rung with ≥ 10 counts in C′_PU × the
  conditionals (× c = 1.196 where factorised), × rate_t per triggered event (Pythia, gen_d123), × the PV-line factor
  0.22 (NI only).
- The looper has 0 counts at R01 in C′_PU, so it takes its depth from C′₀ (0/10⁵ bound).
- Pointer: `background.json` → `cprime.<t>.{n_c0, n_pre, f_pre, rate.value, rate.pv_line_factor, rows[i].factors}`.
  B = N_trig × rate × PV-line × `P_given_t` [V].

### 2.3 Per-rung numbers, SR-G (events in 3 ab⁻¹)

Central values are from `bsum_wp.json` → `ladder.G[i].terms[*].value`. σ_ln is the total per term (stat ⊕ normalisation,
plus model, closure, trend and density for PU). "N/M" is the governing factor from `background.json`. **b** = zero-count
bound. All entries [V].

| term | R04 | R05 | R06 | R07 | R08 | R09 |
|---|---|---|---|---|---|---|
| **PU** B1 direct groups / 48 000 trials | 8 234 601 | 2 386 568 | 11 858 | **35** | 0 | 0 |
| PU B2 ⟨S_ded⟩/trial (6 000 trials; s_ln boot) | 114.36 (0.0077) | 30.96 (0.0079) | 0.389 (0.0060) | — | — | — |
| **PU central** (σ_ln) | 1.05e10 (1.94) | 4.89e9 (2.03) | 3.83e7 (1.36) | 1.35e5 (1.53) | 4.4e3 b (1.92; 0/35) | 252 b (2.22; 0/35·2/35) |
| SM Z(νν) (presel-weighted HS cand. / 2 000 ev) | 1.17e9 (39 033) | 2.70e8 (9 018) | 9.56e5 (32.3; 81 raw) | 1.61e4 b (0/81) | 1.61e4 b | 1.61e4 b |
| SM W(τ_h) | 2.43e8 | 5.62e7 | 1.04e5 (9.0/1 625) | 1.33e4 b (0/1 625) | 1.6e3 b | 158 b |
| SM tt̄ 1ℓ | 1.36e8 | 3.14e7 | 4.60e4 (5.2/2 000) | 9.5e3 b (0/2 000) | 630 b | 630 b |
| SM W(τ_ℓ) | 1.04e8 | 2.36e7 | 8.8e4 (3.0/375) | 8.6e3 b (0/14) | 8.6e3 b | 8.6e3 b |
| SM 8 proxies (sum) | 2.8e8 | 6.6e7 | 2.2e5 | 2.3e4 b | 2.1e4 b | 2.1e4 b |
| C′ DIF (attr./500) | 2.05e7 (166) | 1.00e7 (81) | 2.96e5 (2/81) | 1.48e5 (1/81) | **1.69e5 b (0/81)** | **1.69e5 b** |
| C′ PV pair (24/500 at R02) | 2.96e6 (1/24) | 7.4e5 (6/24) | 1.41e5 b (0/24) | 1.41e5 b | 1.41e5 b | **1.41e5 b** |
| C′ γ | 4.73e6 (153) | 2.66e6 (86) | 4.02e5 (13) | 7.4e4 (2/13) | 4.2e4 b (0/13) | 6.5e3 b |
| C′ V⁰ | 3.68e6 (859) | 1.53e6 (358) | 3.07e4 (6/358) | 5.8e3 b (0/358) | 5.8e3 b | 5.8e3 b |
| C′ NI 22/30/61.5 | 1.7e5 / 3.8e5 / 1.2e6 | 6.2e4 / 1.3e5 / 4.2e5 | 1.8e3 b / 2.7e3 / 2.7e3 | ≈ 3e3 b each | ≈ 3e3 b | ≈ 3e3 b |
| C′ looper | 168 b (0/10⁵ C′₀) | 168 b | 168 b | 168 b | 168 b | 168 b |
| **B₈₄ SR-G** (median) | 7.45e10 (1.26e10) | 3.73e10 (5.36e9) | 1.52e8 (4.13e7) | 1.98e6 (9.34e5) | 1.36e6 (6.34e5) | **1.235e6** (5.46e5) |
| **B₈₄ SR-T** (median) | 2.56e9 (1.97e9) | 6.02e8 (4.63e8) | 3.79e6 (2.65e6) | 1.37e6 (6.8e5) | 1.36e6 (6.36e5) | **1.232e6** (5.45e5) |

Readings:
- The minimum B₈₄ is 1.2346 × 10⁶ at R09, which is **7.050 decades** above 0.11 (`SUM` → `ladder.SR-G.min_B84`,
  `decades_over_0p11_at_min`) [V].
- The SM and C′ terms are identical in SR-T and SR-G: no time-tag credit is given to them (STAGE4_RESULTS l.172).
- Statistical σ_ln per term:
  - in `bsum_wp.json` → `ladder.G[i].terms[j].comps.stat`;
  - zero-bound terms have stat ≥ 1.0;
  - PU stat is 0.008 at R04, 0.177 at R07, 1.24 at R09.
- PU σ_ln components at R04: density 1.80, trend 0.54, model 0.41. At R09: trend 1.26, stat 1.24, density 1.15,
  closure 0.47, model 0.46 (`end_state[i].sigma_ln_components`) [V].

---

## 3. The thinning closure failure

### 3.1 What was measured [V]

The test compares the B2 thinning prediction (ρ = 2 → 1) with the direct B1 per-hit-set group counts, both from the
C1 + C2B union at T_seed = 4.

| test | rung | N_obs (B1) | N_pred (B2 thinned × 48 000) | ratio | z | lever arm | pointer |
|---|---|---|---|---|---|---|---|
| T1 (counting) | R04 | 8 234 601 | 5 489 513 | **1.5001** | **+52.79** | 0.039 (ok) | `background.json` → `closure.T1` |
| T1w (width / χ²) | R05 | 2 386 568 | 1 485 953 | **1.6061** | **+59.40** | 0.029, flagged `lever_ok=false` | `closure.T1w` |

- The statistic is z = ln r / √(1/N_obs + s²_ln,pred), with s_ln,pred = 0.0077 and 0.0079 from the B2 event bootstrap.
- With the B1 bootstrap added, z = 42.6 / 47.1 (`z_with_B1_boot_diag`).
- Branch taken: anti-conservative, with no extra statistics (the user declined the +50 % steps; STAGE4_RESULTS l.716).

### 3.2 The ×2.41 patch

- **×2.409 = 1.5001 × 1.6061.** It multiplies every PU column at and beyond R05, and |ln 1.606| = 0.474 also enters
  σ_ln (`SUM` → `closure.compounded_ge_R05`; `end_state[i].closure_parts`) [V].
- T1w is evaluated at R05 because the tightest rungs with ≥ 10 B1 counts have no lever arm:
  - R06 has lever 0.48 > 0.1;
  - R07 has no ρ = 2 count.
- So the "missing lever arm" branch applies (`closure.T1w.rows`) [V].

### 3.3 Trend

T1 was evaluated at R04-R07 (`closure.trend.points`) [V]:

| rung | ln r |
|---|---|
| R04 | +0.406 |
| R05 | +0.474 |
| R06 | **−0.455** (z = −41) |
| R07 | **−0.954** (z = −5.6) |

- Slope **−0.3608 per rung** (s_boot 0.0045): significant and "conservative".
- So the trend enters σ_ln only, linearly in the rung index: |extrapolated ln r| = 0.18 at R05/R06, 1.26 at R09,
  **1.98 at R11, 3.07 at R14, 6.31 at R23** (`closure.trend.extrapolated_ln_r`).
- The "trend width 2-6.3" quoted in the publication plan is R11 → R23 [V].
- **Note:** at R06 and R07 the direct B1 counts lie *below* the patched central value by ×3.8 and ×4.5:
  - R06: 0.247 against 0.938 per trial;
  - R07: 7.29e-4 against 3.31e-3.
- So the ×2.41 is applied where the direct comparison shows that thinning *over*-predicts [V].

### 3.4 The factor-117 route ambiguity

There are two factorisation routes:
- P_main from R06: p(R07 | R06) = 35/11 858, then the 0/35 bound at R08, then the measured χ² conditionals 2/35, 32/126,
  12/32.
- P_fact from R07: P(R07) = 35/48 000, then the 0/35 bound at R08. Every later zero conditional enters as 1, because
  the single bound is already spent.

The two agree at R07-R09 (ratio 0.5-0.6). From R10 on they split:
- P_fact/P_main = 43.7 at R10 and **116.6 at R11-R14** [V: `columns[i].P_main`, `P_fact`].
- The central value takes the envelope (P_fact).
- ln 117 = **4.76** also enters σ_ln as `model_spread` (`end_state[10..].sigma_ln_components.model_spread`), which
  double counts it.
- At R09 (the minimum) the model spread is only 0.46.

### 3.5 Other closure tests

- T3 is degenerate (`background.json` → `T3.degenerate = true`).
- T1e is untestable: 0 B1 counts at F0e>1.3.
- c-test: c_max = 1.1964 ± 0.0022, from 15.6 M loose candidates, 495 tests, 206 flagged (`background.json` → `c_test`)
  [V].
- Samples: C1 B1 (5 000 events) + C2B (7 000 events) = 12 000 for B1; B2 3 000. CPU: C1b 172.1 + C2B 145.0 CPU-h for the
  whole PU/SM/dens production (`SUM` → `production`) [V].
- Recorded:
  - `background.json` → `closure.*`;
  - `SUM` → `closure`;
  - the G3 pilot at T_seed = 6 had ratio ≈ 1.32 (`S4/g3/G3_REPORT.md` l.175) [U].

---

## 4. Signal

### 4.1 The 40 points and the two paths

- Points: {E200, E500, E1000, E1500, Ẽ500} × Λ ∈ {0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5} keV, configuration BM.
- A2 (PU 200): **180-200 template-half rows per point** (`AN/signal_eff.json` → `a2.points.*.n_den`) [V].
- **Full chain (9 A2FC revert points):** {E200, E500, E1000, E1500} × {3, 5} keV and Ẽ500 at 5 keV. This set was
  pre-declared from A1 CKF-stealing > 5 % (`V46_REVERT_SET.json`, 32e1c6c3 MATCH). The production was 180 jobs, 1 800
  events, 9.7 CPU-h.
- **Fast path (31 points):** numpy row-major digitisation of the quirk hits with no CKF (`SUM` →
  `a2fc_revert.n_points_numpy_A2` = 31) [V].
- Also full chain: **A5 at 1 keV × 5 species-masses** (180-200 rows; `signal_eff.json` → `a5.points`). A5 is not used
  for limits.
- Row-level pass flags (rows × 23 rungs, × 20 FB columns) and the row indices are tracked in
  `AN/signal_rows_a2.npz` and `signal_rows_a5.npz` (keys `<point>|L`, `|FB`, `|rows`) [V: zip listing].
- **A paired row-by-row v1/v2 comparison is therefore possible.**

### 4.2 Pass counts k / n_den at R04-R09 and at r_fb

68 % CP intervals come from `signal_eff.json` → `a2.points.<p>.ladder.<rung>.cp68` and from `SUM` →
`fallback_points.<p>.eps_rfb_cp68`. All [V].

| point | chain | n | R04 | R05 | R06 | R07 | R08 | R09 | r_fb: k (ε, CP68) | μ₉₅/N_exp |
|---|---|---|---|---|---|---|---|---|---|---|
| **E200 1.5** | numpy | 200 | 41 | 41 | 33 | 18 | 5 | 5 | FB2: **9** (0.045, [0.030, 0.065]) | **789.7** |
| E200 2 | numpy | 200 | 45 | 45 | 42 | 31 | 11 | 9 | FB3: 10 (0.050, [0.035, 0.071]) | 820.2 |
| E200 1 | numpy | 188 | 19 | 18 | 14 | 7 | 3 | 3 | FB1: 4 (0.021) | 2 295 |
| E200 1 A5 | full | 188 | 19 | 19 | 14 | 10 | 4 | 4 | — | — |
| E500 2 | numpy | 200 | 52 | 52 | 47 | 29 | 12 | 9 | FB2: 16 (0.080) | 1.84e4 |
| **E500 3** | **full (A2FC)** | 200 | 61 | 61 | 58 | 48 | 19 | 13 | FB3: 11 (0.055, [0.039, 0.076]) | 1.33e4 |
| E200 3 | full | 195 | 36 | 36 | 35 | 28 | 17 | 14 | FB4: 10 (0.051) | 2 796 |
| Ẽ500 3 | numpy | 194 | 47 | 47 | 45 | 31 | 9 | 8 | FB2: 15 (0.077) | 2.77e5 |

- All 40 points are in `sig_table.txt`.
- Seven points have ε = 0 in both bins, so 33 have a limit (`SUM` → `outcome`).

### 4.3 The best point

- **E200, Λ = 1.5 keV, FB2 = 9/200.** I re-counted the 9 from the row array `A2|F|200|1.5|BM|FB` [V].
- CP intervals 68 % [0.0304, 0.0649] and 95 % [0.0208, 0.0837], recomputed exactly [V].
- μ₉₅ (hybrid CLs toys) = 1.2458 × 10⁷ events (`AN/limits.json` → `points.A2|F|200|1.5|BM.expected_toys.median`).
- N_exp = 15 775 = σ_norm 219.2 fb × f_tail 0.04764 × 3 ab⁻¹ × A 0.5035 (`SUM` → `fallback_points.A2|F|200|1.5|BM`).
- **μ₉₅/N_exp = 789.74** (`SUM` → `outcome.best_mu95_over_Nexp.value`) [V: ratio recomputed].
- It was 37.62 before FIX R3-NORM.
- Background behind it:
  - limits.json bins b = [4.51e5 (T), 5.91e5 (G)] with σ_ln [1.75, 2.71];
  - B₈₄ T/G = 2.59e6 / 8.87e6 [V];
  - SR-G is dominated by the 0/24 PV-pair bound.
- Full-chain systematic:
  - Over the 8 other revert points the paired R04 count goes 382 → 318 (× 0.832, discordant 84/20, p = 1.6 × 10⁻¹⁰), and
    r_fb × 0.871 (`SUM` → `a2fc_revert.paired_aggregate_other_8`) [V].
  - E200 1.5 is a numpy point, so ≈ 907 would follow with this factor [E, from the record].
- A2/A5 at 1 keV agree within the binomial error (STAGE4_RESULTS l.320) [U].

---

## 5. Proposal for the C1 comparison subset

### 5.1 Principles

1. **Re-run v1 code at the hashed versions.** Use the 32 analysis_freeze files and the WP_RULE A.3 finder, and log every
   port change in HASH_ADDENDUM style.
   - Pin pyacts 48.0.0: a manylinux_2_34 x86_64 wheel exists (`S4/plan.md` l.162, l.1720) [U].
   - The remaining differences should then be platform floating point only.
2. **Reuse v1 seeds:** job seed = blake2b("stage4|sample|chunk") (WP_RULE l.718), and the same signal rows (`|rows`
   arrays).
   - Paired comparisons are diagnostics.
   - The **pass criterion uses unpaired statistical errors**: INV_A2FC_E500 found that noise re-draws flip 25-50 % of the
     passing rows at R08 and deeper (STAGE4_RESULTS l.369).
3. **Stage 3 only at the three chosen points**, all at Λ ≤ 3 keV. Stage-3 CPU from `STAGE3_INDEX.json` →
   `points.<p>.chunks[*].cpu_s` [V]:

   | Stage-3 point | events | CPU-h |
   |---|---|---|
   | p2/F_m200/L1.5_BM | 463 | 0.15 |
   | p2/F_m200/L2_BM | 463 | 0.35 |
   | p2/F_m500/L3_BM | 492 | 1.12 |

   - All 40 Stage-4 points together cost 29.8 CPU-h.
   - The Λ ≥ 15 keV production cost 323 + 48 = **371 CPU-h**. This confirms the publication plan's "371 CPU-h"
     (l.442) [V].
   - The Stage-3 kernel was bit-identical across Mac and PC in 224/225 events (`TT/sim/stage3/E8_session_log.md` l.13)
     [U]. So per-chunk n_hits and status counts (`STAGE3_INDEX.json` → `chunks[*].n_hits`, `status`) should match
     **exactly**.
   - The md5 values are of npz files that contain timings, so they are not comparable.

### 5.2 Proposed quantities

All v1 values are [V]. "Needed v2" is my [E]. MDE = the relative shift detectable at 2σ, given σ_diff = √(σ₁² + σ₂²).

| # | quantity | v1 value (pointer) | v1 stat | v1 sample | v2 sample proposed | MDE (2σ) |
|---|---|---|---|---|---|---|
| A0 | Stage-3 per-chunk n_hits and status, 3 points | e.g. 2 223 hits in L1.5_c00 | exact | 23 + 10 + 10 chunks | same jobs | bit-level |
| A1 | Arithmetic: B, σ_ln, B₈₄ ladder recomputed from the **recorded** N/M factors | `bsum_wp.json` → `ladder` | MC seed | — | v2 code on v1 counts | ≤ 10⁻³ rel. [E] |
| B1 | PU B1 groups/trial, R04 / R05 / R06 | 171.55 / 49.72 / 0.2470 (`columns[3..5].B1_per_trial`) | s_ln 0.0056 / 0.0062 / ≈ 0.01 [E: Poisson 0.009 + overdispersion] | 12 000 ev | **2 000 ev (8 000 trials)** | ≈ 2 % / 2 % / 6 % |
| B2 | PU B1, R07 | 7.29e-4 (35/48 000) | 0.169 | 12 000 ev | 12 000 ev | ≈ 50 % (thin) |
| B3 | PU B2 ⟨S_ded⟩/trial, R04-R06 | 114.36 / 30.96 / 0.389 (`P_thin`) | 0.0077 / 0.0079 / 0.0060 | 3 000 ev | **750 ev (1 500 trials)** | ≈ 4 % |
| B4 | **T1 and T1w ratios** | 1.5001 / 1.6061 | s_ln ≈ 0.008 (pred) + 0.006 (B1 boot) | as B1, B3 | as B1, B3 | ≈ 4 % |
| B5 | trend slope; c-factor | −0.3608 (s 0.0045); 1.1964 (0.0022) | — | — | as B1 | ≈ 0.02 / 0.5 % |
| C1 | C′₀ f_pre for DIF, NI22, PV pair (n_pre/n_c0) | 0.9495 (47 473/50 000), 0.7593, 0.9031 | binomial ≤ 0.3 % | 5e4 / 3e4 / 1e5 | same | ≤ 1 % |
| C2 | C′_PU attributed counts at R04 / R05, for DIF, γ, V⁰ | 166/81, 153/86, 859/358 (per 500 ev) | 1/√N: 0.08-0.11 at R05 | 500 ev each | 500 same-seed + 500 new | ≈ 30 % at R05 |
| C3 | C′ PV pair at R02 | 24/500 | 0.20 | 500 | **2 000** | ≈ 45 % (thin) |
| C4 | rate_t per triggered event (gen-level): DIF, PV pair, γ | 1.5945 / 30.31 / 0.379 (`cprime.<t>.rate`) | tagged σ_ln 0 [U] | gen_d123 | same | — |
| D1 | N_trig, total and Z(νν) share | 4.0848e7 ± 2.0 %; 2.508e7 | 2.0 % | gen_d123 | same | ≈ 6 % |
| D2 | Z(νν) HS candidates/event at R04 / R05 / R06 | 19.52 / 4.51 / 0.0162 (presel-weighted; 81 raw at R06) | 0.005 / 0.013 / 0.176 | 2 000 ev | 2 000 ev | 1.5 % / 4 % / 50 % |
| S1 | **E200 1.5 keV**: R04, R06, R07; FB2 | 41, 33, 18; 9 of 200 | binomial: 14 %, 16 %, 22 %; FB2 33 % | 200 rows | same 200 rows + 800 new rows | R04 ≈ 31 %, FB2 ≈ 75 % |
| S2 | **E500 3 keV (full chain, A2FC)**: R04, R07; FB3 | 61, 48; 11 of 200 | 11 %, 13 %; 29 % | 200 | same + 800 | ≈ 25 %; ≈ 65 % |
| S3 | **E200 2 keV (numpy; the second-best limit)**: R04, R07; FB3 | 45, 31; 10 of 200 | 13 %, 16 %; 31 % | 200 | same + 800 | ≈ 28 %; ≈ 70 % |

Why these three signal points:
- E200 1.5 keV is mandatory.
- E500 3 keV is the full-chain anomaly point (INV_A2FC_E500, "statistical by exclusion"), so a rerun is informative.
- E200 2 keV is the second-best limit, at the next width level, on the same fast path.
- Alternative to E200 2: **E200 1 keV in both A2 and A5**. It is the only point where v1 has both the fast path and the
  full chain on the same species-mass.

**Cost [E].**
- From the HASH_ADDENDUM constants (l.149-150): about 10 s of chain per PU event plus 8 s per ρ = 1 trial, and 50.6 s per
  ρ = 2 trial.
- B1 2 000 events ≈ 25 CPU-h. B2 750 events ≈ 25 CPU-h. B2 for R07 at 12 000 events ≈ 150 CPU-h, which is optional.
- C′₀ ≈ 12 CPU-h. C′_PU at 1 000-2 000 events per topology × 3 ≈ 10 CPU-h.
- Signal 3 × 1 000 rows ≈ 10-20 CPU-h.
- **Core total ≈ 90 CPU-h without B2-R07.** Laptop timings may not transfer to the Linux workers.

### 5.3 What "within statistical errors" should mean (proposed, fixed before any v2 run)

1. Per quantity i:
   - counts ≥ 10: z_i = (ln x₂ − ln x₁)/√(s₁² + s₂²), with s from the event bootstrap (PU: trial-correlated);
   - counts < 10, or efficiencies: an exact test, converted to a two-sided p_i:
     - conditional binomial for Poisson counts with known exposure;
     - Boschloo or Fisher for k/n.
   - Paired McNemar statistics are reported as diagnostics only.
2. **Look-elsewhere:** N declared quantities. In the table above N ≈ 30 scalar comparisons
   (A0 and A1 excluded, since they are exact).
   - Individual pass: p_i > 0.05/N (Bonferroni; for N = 30, |z| < 3.14).
   - Global pass: χ² = Σ z_i² below the 99th percentile of χ²_N.
   - **Coherence test:** in each family (PU, C′, SM, signal), the inverse-variance mean of ln(x₂/x₁) must be compatible
     with 0 at |z| < 3. This catches a common few-per-cent drift that the individual tests miss.
3. **Exact pieces:**
   - A0: Stage-3 n_hits. Allow ≥ 99 % of events bit-identical, by the v1 cross-machine precedent of 224/225.
   - A1: the analysis arithmetic on v1's recorded counts, within the MC tolerance.
   - The frozen pseudo-random inputs: regenerate `eadm_dilution.json` only if its Stage-3 inputs exist; see §7.
4. **Power statement:** every quantity whose MDE > 50 % is labelled **"gross check only"**. It can catch a bug, not
   validate a port.
5. **On failure:** the quantity is investigated, and no tuning is allowed. A family failure blocks decision point 1 of
   the publication plan (l.516).

**Too thin to compare (flag):**
- PU at R07 and deeper:
  - R07 has 35 counts;
  - R08 and R09 are B1 zeros, so they enter as bounds that only test arithmetic, not physics.
- Every C′ and SM term from R06/R07 on: 0-2 counts on populations of 13-358.
- C′ PV pair beyond R02 (1/24 at R04).
- The looper: 0 everywhere.
- Signal FB columns and R08-R09: 5-19 passes. The best-point 9/200 can only be checked to a factor of about 1.7-2.
- T1e (no counts), T3 (degenerate), and the asymptotic/toy limit ratios.
- μ₉₅ itself is driven by the bounds. I recommend comparing it only through A1 (recomputed from v2 counts with v1 code).

---

## 6. C2: finder cross-checks as specified in v1

**V4-5** (`S4/plan.md` l.1812) [V, spec].
- Run a brute force on **50 signal+PU events and 50 PU-only trials**:
  - an exhaustive scan of PV-plane normals, on a 0.2 mrad grid within ±0.3 rad of the F0 normal, plus a 5 mrad global
    scan over the road;
  - maximise the resolution-weighted inlier count;
  - make an independent scipy least-squares plane fit on the F0 inliers.
- Criterion: **|Δn| < 1 mrad in ≥ 95 % of F0-accepted events**, and every disagreement is inspected.
- It was scheduled at G2 (l.1933, l.2000). The finder speed-ups were to be "checked by V4-5" (l.1919).
- **State: NOT RUN.** STAGE4_RESULTS l.858 and STAGE4_RESULTS_C12v1 l.324 say "no record found", and I found no code
  for it [V by grep].

**V4-4** (`S4/plan.md` l.1811) [V, spec].
- It is a test of **reproducibility and RNG seeds**, not a seed-threshold test:
  - 20 jobs rerun bit-identical on the same machine;
  - different seeds give non-identical outputs;
  - all seeds recorded.
- **State: PARTIAL** (STAGE4_RESULTS l.857):
  - the T_seed = 4 production path is bit-identical to the G3 rerun, 85/85 arrays, with a negative control
    (`validation/tseed4_verify.py` ca21fe4a MATCH; HASH_ADDENDUM l.159-169);
  - the G1b regressions are bit-identical;
  - the 20-job rerun was not found.

**The seed-threshold item is a different test.** It is the T_seed stability test (plan l.505-509; WP_RULE §6.4
l.565-567): the pass fractions of every rung family must be stable when T_seed is lowered by 2.
- G3 measured T_seed 6 → 4 (`S4/g3/G3_REPORT.md` l.158-169) [U]:
  - R06 trial pass fraction +16 % (z = +3.16) at ρ = 1 and +37 % (z = +2.61) at ρ = 2;
  - mean counts +23 % at R04/R05.
- The action T_seed := 4 was triggered and applied.
- **The stability of T_seed = 4 against T_seed = 2 was never tested.** The publication plan's C2 "seed-threshold
  regression (V4-4)" conflates the two items.
- C2 should specify both:
  - V4-4 as written (bit reproducibility on Linux; it fits C1);
  - a T_seed 4 → 2 regression on B1/B2 with the G3 metric.

---

## 7. Inconsistencies in the frozen record, and open questions

**I1.** The WP_RULE.md header (l.3-4) still reads "FREEZE CANDIDATE … NOT YET FROZEN". The file is the frozen one:
- its sha256 1b2ea9bd is checked by run_stage4;
- `frozen_inputs.json` status is "FROZEN … 2026-10-13 18:19".

This is by design, since the file was not edited after the freeze, but the appendix must explain it.

**I2.** Inside WP_RULE, T_seed = 6 (§1.1 l.59, A.4 l.944), and A.3 lists the pre-addendum run_stage4.py and
run_chain.py. The operative values are T_seed = 4 and e371c2b2 / bdea0e27. The governing record is therefore
WP_RULE + HASH_ADDENDUM + PC19, not WP_RULE alone.

**I3.** Three helper-script hashes differ from those HASH_ADDENDUM recorded "at writing" (table in §1.6). The edits are
undocumented. They are not production code.

**I4.** Six hashed frozen inputs are lost (§1.6), including the δ₉₅ script r1_inputs.py.
- Both admissibility generators (`eadm_dilution.py`, `f4r_admissibility.py`; MATCH) read Stage-3 chunk npz files.
- f4r also reads the lost r1c json.
- They span the 307-point grid up to Λ = 40 keV, so they **cannot be regenerated without Stage 3 at Λ ≥ 15 keV**.
- v2 must treat the A.1/A.2b tables and δ₉₅ = 0.15 as frozen transcriptions [V].

**I5. Pre-registration nuance (flag for the human).** The rule, ladder and fallback were frozen before any signal
efficiency (2026-10-13). The **analysis-code freeze b42aef4d dates from 2026-10-16**, after the C12_v1 run had produced
signal efficiencies and limits (freeze bce02b6f).
- The R6 fixes lowered FB0/FB1 B₈₄ by ×4-8 (SR-G) and ×50 (SR-T).
- They moved the best ratio from 1.1 × 10³ to 790 (STAGE4_RESULTS l.115-117, l.789-805).
- FIX R3-NORM came after the results PASS.
- The publication plan's "frozen before any signal efficiency" (l.186) is true for the rule only. The paper appendix
  should state this.

**I6.** The publication plan says "1.14/M with M = 500 to 2000" (l.76).
- In the record the bound is applied to the conditional populations: M = 13 (γ), 24 (PV pair), 35 (PU), 81 (DIF,
  Z(νν)), 1 625 / 2 000 (direct W(τ_h), tt̄).
- The *per-event* reach is about 1.14·c/500 (STAGE4_RESULTS l.191).
- The wording should be fixed.

**I7.** The publication plan says random planes were "measured down 4.9 decades from R04 to R07 by direct count"
(l.167).
- The 4.9 decades are *central values*: the patched thinning, and at R07 the factorisation.
- The direct B1 rate falls 5.37 decades (171.55 → 7.29 × 10⁻⁴ per trial).
- At R06 and R07 the direct counts lie ×3.8-4.5 *below* the central (§3) [V].

**I8.** The C2 naming error for V4-4 is described in §6.

**I9.** T1w at R05 has lever 0.029 (below 0.1) but carries `lever_ok=false` and the "missing lever arm" branch, because
the rule asks for the lever at the tightest rung with ≥ 10 counts. This is internally consistent but easy to misread.

**I10.** `investigation/cmp_all.txt` ε_A2 values differ from `signal_eff.json`:
- E1000 2 keV: 0.165 against 26/190 = 0.137;
- E200 1 keV: 0.12 against 19/188 = 0.101.

The definitions and denominators differ (C12_v1, common rows). It is not the record, so do not use it for C1.

**I11.** STAGE4_RESULTS says "2 000 per SM sample". The W(τν) sample is split into class populations of 375 (τ_ℓ) and
1 625 (τ_h) (`sm.Wtau_*.n_class_events`) [V].

**I12.** At R10 and deeper, the "route" ambiguity is an artefact of the "one bound per term, other zeros enter as 1"
rule applied to two routes, not two physics models. The envelope then takes the route with more zeros set to 1 (§3).

**Open questions for the strategy.**
- (a) Is the C1 signal re-run of v1 ε compatible with the v2 blinding rule? It produces v2-chain signal efficiencies,
  even if only of the v1 selection.
  - I propose to declare it explicitly in the pre-registration as outside the blind.
  - Its 800 extra rows per point must be excluded from the v2 optimisation half (T2/S1).
- (b) Reproduce the fast path exactly, or compare the v1 numpy ε with the v2 full chain? I propose: exact port first (C1),
  and the full-chain difference as a separate, declared S1 measurement.
- (c) For C1, is ACTS pinned at pyacts 48.0.0? Pythia8 must also be pinned. Otherwise C1 tests version drift as well as
  the platform.
- (d) Should B2-R07 (≈ 150 CPU-h for a factor-1.6 test) be bought in C1, or left to B2 (the new thinning repair)?
- (e) Should the 371 CPU-h of Λ ≥ 15 keV Stage 3 that the admissibility tables rest on stay unrerun? I recommend yes,
  keeping the A.1/A.2b tables frozen.
