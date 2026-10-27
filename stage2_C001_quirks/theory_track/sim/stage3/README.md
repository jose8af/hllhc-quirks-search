# Stage 3: T3_causal_s3 propagation of the Stage-2 quirk samples (C001 theory track)

E7 (plan, gate, production; 2026-10-11/12) and E8 (post-production; 2026-10-13).

Status:
- Production finished on both machines, merged and checked.
- P1 and P2 deliverables are produced.
- R1 reviews (critical + constructive) addressed in fix pass R1: `review/FIX_S3_R1.md`.
- Next: re-review, then the user checkpoint Stage 3 → 4 with the open user decisions in `DECISIONS_PENDING.md` (U-1…U-5).
- Deviations from plan §9 (O-1 not done, no pixi tasks, script names): `VALIDATION.md` §9.1.

Everything is **truth level**. Tags: VERIFIED = measured on the production; ESTIMATE = model or interpretation;
UNVERIFIED = transcribed.

## What is here
| file | content |
|---|---|
| `plan.md` | the plan (grid, schema §4, validation §5, systematics §7, decisions D1-D16) |
| `VALIDATION_GATE.md` | E7 gate: V1-V4, V6, V8 smoke; V2b finding; user decisions §7 |
| `RUNNING.md`, `jobs/` | the production job lists (`all = mac + pc`, `overlap`), split, and how it ran |
| `code/` | kernel `T3_causal_s3.py` (s3.2), runner `run_stage3.py`, `s3_physics.py`, surfaces, input/job makers |
| `scripts/` | post-production: `merge_index.py`, `extract.py`, `xover.py`, `p1_model_mg.py`, `p1_results.py`, `p2_results.py`, `val_v5.py`, `val_v7.py`, `val_v7_status4.py`, `val_v9.py`, `val_vscale.py`, `val_c5kev.py`, `make_docs.py`; fix R1: `fix_a1_floor.py`, `fix_bstar_off.py`, `val_vscale_s3.py` (and `validation/val_v8_merge.py`) |
| `SAMPLES.md` | generated inventory: totals per machine (events, CPU-h), environments, md5s, points |
| `VALIDATION.md` | all validation items, §0 generated from `results/*.json` |
| `results/*.json` | single source of every number (P1.json, P2.json, P2_points.json, merge.json, xover.json, V*.json) |
| `PROPOSED_CHANGES.md` | proposed P-10 (c law) wording from the full P1 statistics; `analytic/` is not edited |
| `DECISIONS_PENDING.md` | user decisions U-1…U-5 with options, costs and the reviewers' recommendations |
| `HANDOVER_STAGE4.md` | Stage-4 note: schema, units, surface names → ACTS geometry IDs, seeds, V8 |
| `figures/` | internal diagnostics, labelled "Private work (simulation)", truth level (restyle deferred to Stage 5) |

Data: `data/sim_stage3/`:
- `out/` (Mac) and `out_pc/` (PC);
- `canon/` (symlinks, every job once);
- `STAGE3_INDEX.json`;
- `summary/` (per-event tables);
- `validation/`.

## Headlines
1. **Merge (VERIFIED).**
   - 4576 production jobs: Mac 3986 and PC 590, plus 3 overlap clones on each machine.
   - All files are present once and valid, with identical code md5.
   - 218 571 events, 12.74 M hits.
   - CPU: 207.5 CPU-h on the Mac and 375.5 CPU-h on the PC (sum of per-event process time). The plan estimated 498
     M3-CPU-h.
2. **Cross-machine check (VERIFIED).**
   - Kernel output is bit-identical Mac vs PC in 224/225 overlap events. The one exception has a 4.4 µm maximum hit shift.
   - All KS p = 1.
   - The PC outputs are used.
3. **P1 Δs_B (measured VERIFIED; model ESTIMATE).** The E1 rotating-yo-yo model (c06, unmodified), re-evaluated on the same
   MG events, agrees with the measured Δs_B per event (paired median ratio measured/model) to:
   - 0.990-1.002 for E ≥ 500 GeV at 0.6-5 keV (0.980 at E 500, 0.45 keV); 0.966-0.990 at E 200 (−3 … −11σ paired);
   - Ẽ 500: 0.986 at 0.6 keV, then 0.947-0.969 at 1-5 keV (−4 … −10σ);
   - i.e. ≤ 3.4 % (E) and ≤ 5.3 % (Ẽ), within c06's declared 1-4 %. The cause is γ*, not spin: the ratio is within 0.8 %
     for γ* < 1.3, 0.96-0.98 at γ* 1.3-1.6 and 0.89-0.93 above 1.6 for both species (Ẽ has the higher γ*, median 1.44 vs
     1.27). Ẽ/E = 1.15 ± 0.10 vs 1.16 (P-24) is therefore a weak test; the paired one is the useful one.
   - Above 5 keV the paired ratio rises: 1.001 / 1.008 (E 500 / E 1000) at 7 keV and **1.016 ± 0.005 / 1.027 ± 0.005 at
     10 keV** (unflagged events alone 1.019 / 1.033, so not carried by floor-flagged events). This turns part of the
     unattributed ±5 % (P-9) into a measured +1.6/+2.7 %, same sign as the c excess, and matches Stage-1 FIX2's direct B₀
     shifts (+2.8/+3.4 %).
   - The unpaired pulls of the medians (|pull| ≤ 1.7) are kept only as a secondary column; they have little power.
   - Δs_B is flat in m: d ln Δs_B/d ln m = −0.004 … −0.07 for 0.45-5 keV.
   - R(1/2) = 2Δs(B₀/2)/Δs(B₀) ≡ 1 + c ln 2 is the same measurement as c, not independent support: at 500 GeV it is
     1.0737 ± 0.0007 (1 keV; 2.4σ above P-13's 1.072, the same +2 % as c) and 1.0593 ± 0.0006 (3 keV; P-14 1.059).
4. **P1 c law (PROPOSED_CHANGES.md; numbers VERIFIED, readings ESTIMATE).**
   - Per event, conditional median: holds at 1-2 keV (paired median within ±1.5 %, every k_B bin within ±2.4 %). Window in
     dimensionless terms: median ℓ_max/R_IT ≲ 0.6 and k_B ≲ 4.
   - Population median, by regime: +1.71 ± 0.29 % at 1-2 keV, reproduced by the zero-median symmetric scatter (+2.04 %),
     i.e. an estimator effect; 0.6 keV +0.64 ± 0.40 %; 0.45 keV −1.43 ± 0.51 % (law fails: k_B-ordered residuals
     +6 % → −26 %); 3-5 keV +6.22 ± 0.45 %. (The E8 30-cell mean +1.85 ± 0.19 % mixed these regimes; withdrawn.)
   - Λ exponents: −2 + 2c_ev is the asymptotic (ℓ_max ≪ R_IT) exponent. The 0.6→1 keV slopes are 3.9-5.9σ steeper than
     −2 + 2c_ev at all 5 points; 1→2 keV is 4.1σ / 4.5σ off at E 1500 / Ẽ 500 (the highest ℓ_max/R_IT); 1→3 keV is
     3.0σ / 3.4σ / 3.9σ off at E 1000 / E 1500 / Ẽ 500 (measured slopes steeper; E8 had quoted these as "within 0.03,
     VERIFIED"). The full MG model agrees in every interval (|pull| ≤ 2.6, population slopes).
   - At 3-5 keV high-k_B events carry a positive c excess (size VERIFIED): up to +57 ± 11 % at 5 keV for k_B ≥ 10 (B₀/2
     ≡ 7.1 keV per oscillation), and +3-5 % already at k_B < 4. **Attribution ESTIMATE:** it is cumulative (grows with
     N_osc at matched k_B, ε⊥), and switching B* off removes the bulk of the population-median excess (B*-off run, E 500 + E 1000,
     160 events: B* off +1.8 ± 0.7 % against +9.7 ± 1.3 % for the full production of the same masses, 5.5σ; paired on the
     same events the on − off difference is +8.6 ± 4.2 % for all (2.1σ) and +27.6 ± 11.8 % for k_B ≥ 6 (2.3σ); the k_B < 4
     part is consistent with removal at 1.8σ). B* mainly widens the per-event spread of c (k_B ≥ 10: median per-event
     change +8 ± 19 %, IQR −30 … +112 % of c). With B* off the median is ≤ 3 % for k_B < 10 and +12 ± 3 % at k_B ≥ 10,
     inside the Stage-1 floor-law allowance (6.9-18.2 % at these events' ε⊥). `scripts/fix_r2_bstar_context.py`;
     VALIDATION §8 item 5. The double-precision floor test (D12/O-1) was not done.
5. **P1 MS floor (VERIFIED).** Δs_MS ≈ 10 / 13-16 / 17-22 / 18-28 / 12-16 µm (E 200/500/1000/1500, Ẽ 500), nearly
   Λ-independent. The crossover Δs_B = Δs_MS falls with mass: 1.91 / 1.50 / 1.25 / 1.16 keV (E 200/500/1000/1500) and
   1.59 keV (Ẽ 500). B and MS add **sub-quadrature** per event in the crossover region: median Δs_BM/√(Δs_B² + Δs_M²) =
   0.99-1.00 at 0.45 keV, 0.95-1.00 at 0.6 keV, 0.80-0.97 at 1-3 keV (measured; the combination rule is the open user
   decision U-2). The material scaling exponents are 0.36-0.62; against the single-point code-scaling value 0.517
   χ² = 26.0/10, with E 1000 and E 1500 low (0.36-0.38 ± 0.06-0.07, 2-2.6σ). Highland's √(x/X₀) is the expectation (≈ 0.5).
   The P2 material systematic is unaffected (it uses the direct ×0.5/×2 runs).
6. **P2: a sensitivity map plus per-event templates (template half; VERIFIED hit level, ESTIMATE closed forms).**
   - **Continuous Λ handle:** the median IT pair separation scales as Λ⁻² from 1 to 30 keV at every species-mass (log-log
     slopes −1.985 … −2.022, each ± 0.02-0.04, all consistent with −2; fix R2, `results/FIX_R2_notes.json`; E 1000: 38.5 mm → 9.3 mm → 0.37 mm → 95 µm at 1/2/10/20 keV), i.e. it measures ℓ₀ = m/Λ²
     (sep_IT/ℓ_max ≈ 0.5-0.6 above 1 keV). Below ≈ 1.5 keV Δs_B (Λ only, m-flat) together with sep_IT (ℓ₀) breaks the
     (m, Λ) degeneracy without the recoil. Tracker hits/event, maximum hit delay and the turn-around fraction are flat in Λ
     (they carry m via the velocities).
   - **Edges** (6 columns, ≈ 2-3 independent pieces of information):
     - N_osc = 1 at 0.28-0.33 keV, independent of m (closed form);
     - median ℓ_max = R_IT at 0.43 → 0.78 keV (E 200 → 1500) and 0.59 → 0.94 keV (Ẽ); median ℓ_max = 100 µm at 16 → 30 keV
       (E) and 23 → 36 keV (Ẽ) — **the same quantity** at two thresholds (ratio fixed at 38.2); m-slope
       d ln Λ/d ln m = 0.249 ± 0.019 (not √m, which would be 0.5);
     - truth-level thickness edge (median Δs_all = 100 µm, B + M) at 0.47-0.55 keV, flat in m — the only edge tied to ε_B;
     - hit-level merging edge f(IT pair separation < 100 µm) = 50 % at 12.8 → 20.4 keV (E) and 17.7 → 25 keV (Ẽ): slope
       0.25 ± 0.02 overall, ≈ flat at 19.4-20.4 keV above 700 GeV; measured at 7 E masses and interpolated (flagged, fit
       error) at the other 7; the 25 µm edge is a second threshold on the same separation (3 masses).
   - **Systematics** (ℓ_max ±5 %, QED, scale, PDF, merging, material ×0.5/×2): re-evaluated in fix R1 as bootstrap-averaged
     paired shifts to remove reweighted-median jumps. Per edge type the median total moves 1.8→2.3 / 4.7→4.2 / 3.7→3.6 /
     4.7→4.2 / 5.0→5.2 / 3.0→3.7 % and the maximum 11.3 → 8.1 % (F_m1100 ℓ_max: PDF 7.3 → 2.2 %). The envelope terms
     carry a positive noise bias under averaging, so the "after" values are conservative; 198 of the 243 robust ℓ_max/QED/PDF
     components are below 2× their sampling σ (`robust_shift_sampling_sd_rel`), so the robust totals are noise-limited
     **upper bounds** (fix R2, C-4; symmetrisation and the < 2σ treatment deferred to Stage 4, HANDOVER §5). The tail rate is a normalisation and does not move the edges.
   - **Toys:** at Λ ≥ 15 keV only E 1000/1200 have toys; merged-regime coverage is testable there only (U-3).
7. **Open items (VALIDATION.md §9; DECISIONS_PENDING.md):**
   - 108 status-4 events (0.05 %; near-threshold pairs with material);
   - V3, V4, V-scale (at 10⁻²) and V8 (counts) literal failures, all explained; V8 cause found (ACTS `doMerge`);
   - D12/O-1 floor test not done (planned side study);
   - the P-10 revision (proposal) and the user decisions U-1…U-5.

## Results tables (generated)
<!-- BEGIN AUTO-RESULTS (generated by scripts/make_docs.py from results/*.json; do not edit by hand) -->
Generated by `scripts/make_docs.py` from `results/P1.json` and `results/P2.json`. Truth level. Pull = (prediction - measurement)/sigma.

**P1 (|eta_pair| < 1, vertex at the origin, 10 T3 barrel layers; B at max_boost 1e-3).** Ds_B median [µm]; MG model = the c06 rotating-yo-yo
model on the same events: **paired** per-event median ratio measured/model +- bootstrap (pull of the ratio vs 1; fix R1, the primary statistic) and
the unpaired pull of the medians (secondary); c (B0, B0/2) with median c_ev on the same events (MG) and predictions.json;
R(1/2) = 2 Ds(B0/2)/Ds(B0) = 1 + c ln 2 (the same measurement as c, not independent) with its pull vs 1 + c_ev ln 2; MS floor and B+M.

| point | Lambda [keV] | l_max/R_IT (median) | Ds_B [µm] | paired Ds_B/model (pull) | MG model median (unpaired pull) | f floor | c measured | c_ev MG (pull) | c json (pull) | R(1/2) (pull) | Ds_MS [µm] | Ds_B+M [µm] | BM/sqrt(B²+M²) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F_m200 | 0.45 | 0.93 | 137 +- 8.2 | 0.966 +- 0.003 (-10.3) | 143 (0.71) | 0.00 | 0.1424 +- 0.0019 | 0.1374 (-2.6) | - | 1.0987 (-2.6) | 9.62 +- 0.69 | 140 +- 8.6 | 1.00 +- 0.00 |
| F_m200 | 0.6 | 0.52 | 78.4 +- 4.5 | 0.975 +- 0.003 (-7.8) | 84 (1.2) | 0.00 | 0.1307 +- 0.0015 | 0.1274 (-2.2) | 0.128 (-1.8) | 1.0906 (-2.2) | 10.4 +- 0.91 | 78.3 +- 3.2 | 1.00 +- 0.01 |
| F_m200 | 1 | 0.19 | 31.1 +- 1.8 | 0.986 +- 0.001 (-9.4) | 32 (0.52) | 0.00 | 0.1135 +- 0.0014 | 0.1127 (-0.5) | 0.113 (-0.3) | 1.0787 (-0.5) | 9.85 +- 0.6 | 33.3 +- 2.4 | 0.97 +- 0.02 |
| F_m200 | 2 | 0.047 | 9.32 +- 0.61 | 0.987 +- 0.002 (-6.4) | 9.8 (0.79) | 0.00 | 0.0995 +- 0.0016 | 0.0975 (-1.3) | 0.098 (-0.9) | 1.0690 (-1.3) | 10.1 +- 0.59 | 13 +- 1.2 | 0.94 +- 0.06 |
| F_m200 | 3 | 0.021 | 4.28 +- 0.28 | 0.989 +- 0.003 (-3.4) | 4.3 (0.087) | 0.00 | 0.0923 +- 0.0017 | 0.0903 (-1.2) | 0.091 (-0.8) | 1.0640 (-1.2) | 11.2 +- 0.92 | 10.2 +- 0.58 | 0.80 +- 0.04 |
| F_m200 | 5 | 0.0075 | 1.64 +- 0.092 | 0.990 +- 0.002 (-4.2) | 1.68 (0.54) | 0.01 | 0.0905 +- 0.0016 | 0.0827 (-5.0) | 0.083 (-4.8) | 1.0627 (-5.0) | 11.3 +- 0.58 | 10.2 +- 0.64 | 0.89 +- 0.05 |
| F_m200 | 7 | - | - | - | - | - | - | - | - | - | 10.4 +- 1.1 | 10.6 +- 0.77 | - |
| F_m200 | 10 | - | - | - | - | - | - | - | - | - | 10.6 +- 0.99 | 9.95 +- 0.64 | - |
| F_m500 | 0.45 | 1.8 | 132 +- 7.8 | 0.980 +- 0.004 (-4.7) | 133 (0.18) | 0.00 | 0.1251 +- 0.0015 | 0.1251 (+0.0) | - | 1.0867 (+0.0) | 13.3 +- 0.94 | 132 +- 8.2 | 1.00 +- 0.00 |
| F_m500 | 0.6 | 1 | 77.2 +- 3.6 | 0.990 +- 0.002 (-4.9) | 79.1 (0.55) | 0.00 | 0.1190 +- 0.0010 | 0.1167 (-2.3) | 0.116 (-2.9) | 1.0825 (-2.3) | 13.2 +- 0.89 | 75.1 +- 5.1 | 0.96 +- 0.01 |
| F_m500 | 1 | 0.37 | 29.5 +- 1.6 | 0.993 +- 0.001 (-5.5) | 30.1 (0.34) | 0.00 | 0.1064 +- 0.0009 | 0.1043 (-2.2) | 0.104 (-2.5) | 1.0737 (-2.2) | 13.2 +- 1.1 | 33.2 +- 1.4 | 0.94 +- 0.02 |
| F_m500 | 2 | 0.092 | 8.77 +- 0.51 | 0.995 +- 0.002 (-2.8) | 9.06 (0.57) | 0.00 | 0.0909 +- 0.0009 | 0.0911 (+0.2) | 0.091 (+0.1) | 1.0630 (+0.2) | 15.6 +- 1.2 | 16 +- 0.89 | 0.81 +- 0.04 |
| F_m500 | 3 | 0.041 | 3.99 +- 0.2 | 0.995 +- 0.002 (-2.6) | 4.05 (0.27) | 0.02 | 0.0855 +- 0.0009 | 0.0848 (-0.8) | 0.085 (-0.6) | 1.0593 (-0.8) | 14.3 +- 1.5 | 13.6 +- 0.82 | 0.88 +- 0.06 |
| F_m500 | 5 | 0.015 | 1.56 +- 0.08 | 0.997 +- 0.001 (-2.4) | 1.6 (0.56) | 0.03 | 0.0865 +- 0.0011 | 0.0781 (-7.8) | 0.078 (-7.8) | 1.0600 (-7.8) | 15.5 +- 1 | 15.2 +- 1.3 | 0.99 +- 0.06 |
| F_m500 | 7 | 0.0076 | 0.91 +- 0.069 (+-5 % unattr.) | 1.001 +- 0.002 (+0.4) | 0.905 (-0.06) | 0.06 | - | - | - | - | 14.9 +- 1.5 | 15.4 +- 1.6 | 0.98 +- 0.12 |
| F_m500 | 10 | 0.0037 | 0.482 +- 0.04 (+-5 % unattr.) | 1.016 +- 0.005 (+3.5) | 0.464 (-0.44) | 0.17 | - | - | - | - | 12.8 +- 1.2 | 12.2 +- 0.89 | 0.95 +- 0.08 |
| F_m1000 | 0.45 | 2.6 | 131 +- 7.1 | 0.994 +- 0.004 (-1.4) | 130 (-0.14) | 0.00 | 0.1142 +- 0.0013 | 0.1170 (+2.1) | - | 1.0792 (+2.1) | 17.8 +- 1.4 | 141 +- 6.4 | 0.99 +- 0.01 |
| F_m1000 | 0.6 | 1.4 | 75.6 +- 3.9 | 0.995 +- 0.002 (-2.6) | 76.8 (0.31) | 0.00 | 0.1107 +- 0.0009 | 0.1096 (-1.2) | 0.111 (+0.3) | 1.0767 (-1.2) | 17.2 +- 1.5 | 84.3 +- 4.6 | 0.99 +- 0.01 |
| F_m1000 | 1 | 0.52 | 28.7 +- 1.5 | 0.998 +- 0.001 (-2.5) | 29.7 (0.68) | 0.00 | 0.0996 +- 0.0008 | 0.0986 (-1.3) | 0.100 (+0.4) | 1.0691 (-1.3) | 18.2 +- 1.2 | 38.9 +- 2.2 | 0.95 +- 0.03 |
| F_m1000 | 2 | 0.13 | 8.23 +- 0.42 | 0.998 +- 0.001 (-2.2) | 8.46 (0.54) | 0.01 | 0.0879 +- 0.0006 | 0.0867 (-1.9) | 0.088 (+0.1) | 1.0609 (-1.9) | 21.7 +- 1.6 | 23.4 +- 1.6 | 0.88 +- 0.04 |
| F_m1000 | 3 | 0.058 | 3.91 +- 0.17 | 0.997 +- 0.001 (-3.3) | 4.04 (0.77) | 0.02 | 0.0855 +- 0.0006 | 0.0810 (-7.0) | 0.082 (-5.5) | 1.0593 (-7.0) | 18.9 +- 1.5 | 21.8 +- 2.3 | 0.95 +- 0.05 |
| F_m1000 | 5 | 0.021 | 1.49 +- 0.077 | 1.000 +- 0.001 (-0.1) | 1.53 (0.47) | 0.07 | 0.0848 +- 0.0015 | 0.0748 (-6.8) | 0.076 (-6.0) | 1.0588 (-6.8) | 22.3 +- 1.5 | 21.2 +- 2.5 | 0.93 +- 0.07 |
| F_m1000 | 7 | 0.0097 | 0.821 +- 0.051 (+-5 % unattr.) | 1.008 +- 0.002 (+4.9) | 0.812 (-0.17) | 0.17 | - | - | - | - | 19.3 +- 1.8 | 18.5 +- 2 | 1.02 +- 0.08 |
| F_m1000 | 10 | 0.0047 | 0.445 +- 0.032 (+-5 % unattr.) | 1.027 +- 0.005 (+5.4) | 0.415 (-0.95) | 0.37 | - | - | - | - | 19.4 +- 1.8 | 18.3 +- 2.1 | 0.98 +- 0.06 |
| F_m1500 | 0.45 | 3 | 136 +- 6 | 1.001 +- 0.003 (+0.2) | 139 (0.47) | 0.00 | 0.1089 +- 0.0013 | 0.1138 (+3.7) | - | 1.0755 (+3.7) | 17.6 +- 1.7 | 137 +- 6.1 | 0.99 +- 0.01 |
| F_m1500 | 0.6 | 1.7 | 78.9 +- 3.2 | 1.000 +- 0.002 (-0.1) | 79.8 (0.27) | 0.00 | 0.1053 +- 0.0010 | 0.1068 (+1.5) | - | 1.0730 (+1.5) | 22.4 +- 1.8 | 77.1 +- 3.7 | 0.95 +- 0.02 |
| F_m1500 | 1 | 0.61 | 30.4 +- 1.1 | 0.999 +- 0.001 (-1.3) | 30.6 (0.23) | 0.00 | 0.0983 +- 0.0010 | 0.0963 (-2.0) | - | 1.0681 (-2.0) | 22.8 +- 1.5 | 38.8 +- 2.2 | 0.93 +- 0.04 |
| F_m1500 | 2 | 0.15 | 8.18 +- 0.36 | 0.999 +- 0.001 (-1.8) | 8.21 (0.066) | 0.02 | 0.0869 +- 0.0005 | 0.0849 (-4.3) | - | 1.0603 (-4.3) | 23.9 +- 2.4 | 25.3 +- 1.9 | 0.89 +- 0.04 |
| F_m1500 | 3 | 0.068 | 3.95 +- 0.14 | 1.000 +- 0.001 (-0.6) | 4 (0.34) | 0.04 | 0.0834 +- 0.0010 | 0.0795 (-4.1) | - | 1.0578 (-4.1) | 23.3 +- 2.7 | 24.4 +- 2.2 | 0.97 +- 0.05 |
| F_m1500 | 5 | 0.024 | 1.56 +- 0.047 | 1.002 +- 0.000 (+5.6) | 1.55 (-0.25) | 0.10 | 0.0848 +- 0.0016 | 0.0735 (-7.2) | - | 1.0588 (-7.2) | 24.5 +- 2 | 24.7 +- 2.3 | 1.09 +- 0.07 |
| F_m1500 | 7 | - | - | - | - | - | - | - | - | - | 25.6 +- 2.7 | 24.4 +- 3 | - |
| F_m1500 | 10 | - | - | - | - | - | - | - | - | - | 28.1 +- 2.3 | 22.3 +- 2 | - |
| S_m500 | 0.45 | 2.9 | 162 +- 8.4 | 0.993 +- 0.006 (-1.2) | 155 (-0.86) | 0.00 | 0.1152 +- 0.0027 | 0.1234 (+3.0) | - | 1.0799 (+3.0) | 12.9 +- 0.89 | 159 +- 7 | 1.00 +- 0.00 |
| S_m500 | 0.6 | 1.6 | 90.4 +- 3.9 | 0.986 +- 0.003 (-4.2) | 92.1 (0.46) | 0.00 | 0.1138 +- 0.0017 | 0.1152 (+0.8) | - | 1.0789 (+0.8) | 11.5 +- 1.1 | 84.1 +- 3.4 | 0.98 +- 0.01 |
| S_m500 | 1 | 0.59 | 33.9 +- 2.3 | 0.969 +- 0.005 (-5.8) | 36.2 (0.97) | 0.00 | 0.1063 +- 0.0014 | 0.1031 (-2.4) | - | 1.0737 (-2.4) | 14.5 +- 1.3 | 34.2 +- 1.7 | 0.95 +- 0.02 |
| S_m500 | 2 | 0.15 | 9.27 +- 0.58 | 0.954 +- 0.007 (-6.6) | 10.3 (1.7) | 0.00 | 0.0939 +- 0.0016 | 0.0902 (-2.3) | - | 1.0651 (-2.3) | 14 +- 1.1 | 16.7 +- 1.1 | 0.85 +- 0.06 |
| S_m500 | 3 | 0.066 | 4.44 +- 0.25 | 0.947 +- 0.005 (-9.7) | 4.73 (1.2) | 0.00 | 0.0899 +- 0.0014 | 0.0841 (-4.3) | - | 1.0623 (-4.3) | 15.7 +- 0.88 | 15 +- 1.4 | 0.92 +- 0.06 |
| S_m500 | 5 | 0.024 | 1.79 +- 0.12 | 0.952 +- 0.008 (-6.0) | 1.85 (0.53) | 0.00 | 0.0908 +- 0.0024 | 0.0774 (-5.7) | - | 1.0630 (-5.7) | 14.3 +- 0.94 | 14.8 +- 0.85 | 1.03 +- 0.07 |
| S_m500 | 7 | - | - | - | - | - | - | - | - | - | 15 +- 1.2 | 12.9 +- 1.2 | - |
| S_m500 | 10 | - | - | - | - | - | - | - | - | - | 13.6 +- 1.5 | 14.2 +- 1.4 | - |

Paired Ds_B/model ratio in gamma* bins (pooled over 0.45-5 keV; VERIFIED measured ratio, the model is ESTIMATE):

| point | median gamma* | [1,1.05) | [1.05,1.15) | [1.15,1.3) | [1.3,1.6) | >= 1.6 |
|---|---|---|---|---|---|---|
| F_m200 | 1.348 | 1.008 +- 0.005 (n=90) | 1.004 +- 0.003 (n=281) | 0.999 +- 0.001 (n=420) | 0.981 +- 0.002 (n=468) | 0.924 +- 0.003 (n=540) |
| F_m500 | 1.272 | 1.003 +- 0.001 (n=156) | 1.002 +- 0.001 (n=450) | 0.997 +- 0.001 (n=378) | 0.979 +- 0.002 (n=480) | 0.928 +- 0.007 (n=336) |
| F_m1000 | 1.190 | 1.002 +- 0.001 (n=192) | 1.002 +- 0.000 (n=540) | 1.000 +- 0.001 (n=492) | 0.958 +- 0.004 (n=372) | 0.917 +- 0.008 (n=203) |
| F_m1500 | 1.150 | 1.001 +- 0.001 (n=209) | 1.002 +- 0.000 (n=690) | 0.999 +- 0.001 (n=486) | 0.956 +- 0.004 (n=348) | 0.890 +- 0.014 (n=66) |
| S_m500 | 1.438 | 1.004 +- 0.008 (n=12) | 1.001 +- 0.001 (n=132) | 0.997 +- 0.001 (n=335) | 0.963 +- 0.002 (n=714) | 0.905 +- 0.003 (n=606) |

Lambda exponents: median per-event slope +- err, its pull vs the closed form -2 + 2c_ev [pull]; population slope (ratio of medians) +- err,
its pull vs the full MG rotating-yo-yo model {pull}:

| point | 0.45-0.6 | 0.6-1 | 1-2 | 2-3 | 3-5 | 5-10 | 1-3 |
|---|---|---|---|---|---|---|---|
| F_m200 | -1.855+-0.047 [+2.6]; -1.934+-0.124 {+0.7} | -1.892+-0.034 [+3.9]; -1.812+-0.069 {-1.1} | -1.807+-0.017 [+1.0]; -1.739+-0.054 {+0.6} | -1.837+-0.023 [+1.1]; -1.919+-0.099 {-1.1} | -1.793+-0.024 [-1.4]; -1.883+-0.079 {+0.6} | - | -1.820+-0.010 [+2.3]; -1.805+-0.037 {-0.6} |
| F_m500 | -1.890+-0.044 [+3.0]; -1.862+-0.121 {+0.4} | -1.904+-0.022 [+5.7]; -1.879+-0.061 {-0.2} | -1.807+-0.015 [+0.1]; -1.751+-0.046 {+0.4} | -1.826+-0.023 [+0.1]; -1.942+-0.089 {-0.5} | -1.849+-0.020 [+0.6]; -1.843+-0.060 {+0.5} | -1.746+-0.026 [-4.0]; -1.718+-0.068 {-2.0} | -1.813+-0.009 [+0.3]; -1.822+-0.030 {-0.2} |
| F_m1000 | -1.990+-0.049 [+4.5]; -1.899+-0.111 {+0.7} | -1.883+-0.021 [+4.3]; -1.897+-0.062 {+0.6} | -1.831+-0.013 [+1.2]; -1.802+-0.048 {-0.2} | -1.832+-0.021 [-0.0]; -1.837+-0.063 {+0.2} | -1.836+-0.016 [-0.5]; -1.881+-0.057 {-0.3} | -1.708+-0.027 [-5.5]; -1.705+-0.069 {-2.0} | -1.849+-0.009 [+3.0]; -1.815+-0.027 {-0.0} |
| F_m1500 | -2.060+-0.035 [+7.9]; -1.887+-0.096 {-0.4} | -1.887+-0.022 [+4.0]; -1.870+-0.051 {-0.1} | -1.856+-0.009 [+4.1]; -1.892+-0.035 {-0.2} | -1.839+-0.023 [+0.1]; -1.797+-0.060 {+0.4} | -1.831+-0.016 [-1.0]; -1.817+-0.035 {-1.1} | - | -1.848+-0.007 [+3.4]; -1.857+-0.020 {+0.2} |
| S_m500 | -2.104+-0.066 [+5.2]; -2.030+-0.112 {+2.0} | -1.945+-0.028 [+5.9]; -1.918+-0.075 {+1.2} | -1.861+-0.012 [+4.5]; -1.871+-0.052 {+1.1} | -1.812+-0.020 [-0.7]; -1.817+-0.081 {-1.2} | -1.827+-0.020 [-0.6]; -1.782+-0.065 {-0.9} | - | -1.841+-0.007 [+3.9]; -1.851+-0.034 {-0.0} |

MS-floor scaling exponent ln[Ds(Mx2)/Ds(Mx0.5)]/ln 4 (Highland expectation ~0.5 for sqrt(x/X0); code-scaling check 0.517 at 500 GeV, 3 keV): F_m200/L1 0.51+-0.05, F_m200/L3 0.62+-0.06, F_m500/L1 0.47+-0.06, F_m500/L3 0.47+-0.07, F_m1000/L1 0.36+-0.06, F_m1000/L3 0.38+-0.07, F_m1500/L1 0.46+-0.06, F_m1500/L3 0.37+-0.06, S_m500/L1 0.42+-0.06, S_m500/L3 0.48+-0.06; chi2 vs 0.517 = 26.0/10.

B = MS crossover (median Ds_B = median Ds_MS, log-log interpolation): F_m200 1.91 keV, F_m500 1.50 keV, F_m1000 1.25 keV, F_m1500 1.16 keV, S_m500 1.59 keV.

V2b revisit, population excess median(c)/median(c_ev) - 1 by regime (weighted mean over the cells of the regime; the 30-cell mean +1.85 % mixes regimes and is not used):

- 0.45 keV (law fails): -1.43 % +- 0.51 %; k_B < 6 sub-sample +1.62 %; zero-median symmetric-scatter model +0.82 %
- 0.6 keV (onset): +0.64 % +- 0.40 %; k_B < 6 sub-sample +1.36 %; zero-median symmetric-scatter model +1.86 %
- 1-2 keV (scatter only): +1.71 % +- 0.29 %; k_B < 6 sub-sample +0.47 %; zero-median symmetric-scatter model +2.04 %
- 3-5 keV (k_B-ordered excess): +6.22 % +- 0.45 %; k_B < 6 sub-sample +3.47 %; zero-median symmetric-scatter model +1.97 %

Pooled median r/c_ev by k_B bin (0-2 / 2-4 / 4-6 / 6-10 / >= 10):

- 0.45 keV: +6.0+-0.6 % / +2.0+-0.5 % / -2.4+-1.1 % / -7.2+-1.9 % / -26.3+-4.4 %
- 0.6 keV: +2.8+-0.4 % / +0.8+-0.3 % / -0.1+-0.6 % / -1.6+-1.0 % / -7.3+-2.3 %
- 1 keV: +0.2+-0.3 % / -0.1+-0.3 % / -0.0+-0.4 % / +0.2+-0.9 % / -2.0+-1.4 %
- 2 keV: -0.2+-0.3 % / -0.7+-0.4 % / +0.7+-0.8 % / -1.8+-1.1 % / +2.4+-1.6 %
- 3 keV: -0.4+-0.5 % / +0.8+-0.5 % / +2.4+-1.1 % / +3.3+-1.8 % / +8.9+-3.1 %
- 5 keV: +2.0+-1.0 % / +6.5+-1.3 % / +12.9+-2.6 % / +18.6+-6.0 % / +56.5+-11.6 %

**P2 Lambda edges [keV]** (template half, |eta_pair| < 2.5, BM; stat (bootstrap), total systematic before -> after the fix-R1 robust evaluation (bootstrap-averaged paired shifts), relative; closed forms: plan §1.1 on the production events; hit level: from the stored hits). Redundancy: the two l_max columns are one quantity (ratio fixed at sqrt(R_IT/100 µm) = 38.2); the two merge columns are thresholds on the IT pair separation; only the Ds = 100 µm edge is tied to eps_B:

| species-mass | N_osc = 1 (closed) | l_max = R_IT (closed) | Ds_all = 100 µm (hits) | l_max = 100 µm (closed; = col. 3 x 38.2) | IT pair sep. < 100 µm (hits) | IT pair sep. < 25 µm (hits) |
|---|---|---|---|---|---|---|
| F_m200 | 0.296 +- 2 % (stat) +- 3 -> 5 % (syst) | 0.427 +- 4 % (stat) +- 6 -> 8 % (syst) | 0.5 +- 2 % (stat) +- 3 -> 3 % (syst) | 16.3 +- 4 % (stat) +- 6 -> 8 % (syst) | 12.8 +- 4 % (stat) +- 5 -> 5 % (syst) | 26.3 +- 4 % (stat) +- 3 -> 4 % (syst) |
| F_m300 | 0.28 +- 3 % (stat) +- 1 -> 3 % (syst) | 0.502 +- 5 % (stat) +- 2 -> 4 % (syst) | 0.496 +- 3 % (stat) +- 4 -> 4 % (syst) | 19.2 +- 5 % (stat) +- 2 -> 4 % (syst) | 13.8 +- 5 % (stat) +- 5 -> 5 % (syst) | 27.8 +- 5 % (stat) +- 4 -> 4 % (syst) |
| F_m400 | 0.307 +- 2 % (stat) +- 1 -> 2 % (syst) | 0.591 +- 5 % (stat) +- 6 -> 4 % (syst) | 0.489 +- 2 % (stat) +- 3 -> 3 % (syst) | 22.6 +- 5 % (stat) +- 6 -> 4 % (syst) | (15.9 +- 0.45, interpolated in ln m) | n/a |
| F_m500 | 0.291 +- 3 % (stat) +- 2 -> 2 % (syst) | 0.626 +- 6 % (stat) +- 4 -> 4 % (syst) | 0.512 +- 3 % (stat) +- 3 -> 3 % (syst) | 23.9 +- 6 % (stat) +- 4 -> 4 % (syst) | 16.4 +- 5 % (stat) +- 4 -> 5 % (syst) | n/a |
| F_m600 | 0.305 +- 3 % (stat) +- 2 -> 2 % (syst) | 0.647 +- 4 % (stat) +- 4 -> 4 % (syst) | 0.511 +- 4 % (stat) +- 4 -> 4 % (syst) | 24.7 +- 4 % (stat) +- 4 -> 4 % (syst) | (17.7 +- 0.52, interpolated in ln m) | n/a |
| F_m700 | 0.3 +- 3 % (stat) +- 5 -> 4 % (syst) | 0.686 +- 4 % (stat) +- 6 -> 5 % (syst) | 0.506 +- 3 % (stat) +- 4 -> 4 % (syst) | 26.2 +- 4 % (stat) +- 6 -> 5 % (syst) | 19.4 +- 5 % (stat) +- 8 -> 8 % (syst) | n/a |
| F_m800 | 0.308 +- 4 % (stat) +- 3 -> 4 % (syst) | 0.737 +- 5 % (stat) +- 3 -> 4 % (syst) | 0.53 +- 3 % (stat) +- 4 -> 4 % (syst) | 28.2 +- 5 % (stat) +- 3 -> 4 % (syst) | (18.8 +- 0.46, interpolated in ln m) | n/a |
| F_m900 | 0.292 +- 2 % (stat) +- 2 -> 2 % (syst) | 0.652 +- 4 % (stat) +- 5 -> 4 % (syst) | 0.484 +- 4 % (stat) +- 4 -> 5 % (syst) | 24.9 +- 4 % (stat) +- 5 -> 4 % (syst) | (19.2 +- 0.42, interpolated in ln m) | n/a |
| F_m1000 | 0.301 +- 2 % (stat) +- 2 -> 2 % (syst) | 0.681 +- 4 % (stat) +- 5 -> 4 % (syst) | 0.473 +- 2 % (stat) +- 1 -> 2 % (syst) | 26 +- 4 % (stat) +- 5 -> 4 % (syst) | 19.4 +- 4 % (stat) +- 4 -> 4 % (syst) | 39.3 +- 3 % (stat) +- 3 -> 3 % (syst) |
| F_m1100 | 0.296 +- 4 % (stat) +- 4 -> 3 % (syst) | 0.695 +- 6 % (stat) +- 11 -> 5 % (syst) | 0.495 +- 3 % (stat) +- 5 -> 4 % (syst) | 26.6 +- 6 % (stat) +- 11 -> 5 % (syst) | (19.8 +- 0.4, interpolated in ln m) | n/a |
| F_m1200 | 0.31 +- 3 % (stat) +- 3 -> 3 % (syst) | 0.712 +- 3 % (stat) +- 4 -> 4 % (syst) | 0.498 +- 3 % (stat) +- 5 -> 3 % (syst) | 27.2 +- 3 % (stat) +- 4 -> 4 % (syst) | 20.4 +- 4 % (stat) +- 6 -> 5 % (syst) | n/a |
| F_m1300 | 0.281 +- 3 % (stat) +- 8 -> 5 % (syst) | 0.716 +- 4 % (stat) +- 5 -> 6 % (syst) | 0.485 +- 2 % (stat) +- 3 -> 4 % (syst) | 27.4 +- 4 % (stat) +- 5 -> 6 % (syst) | (20.2 +- 0.5, interpolated in ln m) | n/a |
| F_m1400 | 0.285 +- 2 % (stat) +- 1 -> 2 % (syst) | 0.762 +- 4 % (stat) +- 3 -> 4 % (syst) | 0.476 +- 3 % (stat) +- 4 -> 4 % (syst) | 29.1 +- 4 % (stat) +- 3 -> 4 % (syst) | (20.3 +- 0.58, interpolated in ln m) | n/a |
| F_m1500 | 0.291 +- 2 % (stat) +- 2 -> 1 % (syst) | 0.776 +- 4 % (stat) +- 5 -> 3 % (syst) | 0.486 +- 3 % (stat) +- 3 -> 4 % (syst) | 29.6 +- 4 % (stat) +- 5 -> 3 % (syst) | 19.8 +- 4 % (stat) +- 6 -> 6 % (syst) | n/a |
| S_m200 | 0.321 +- 3 % (stat) +- 2 -> 2 % (syst) | 0.593 +- 3 % (stat) +- 4 -> 4 % (syst) | 0.544 +- 2 % (stat) +- 3 -> 3 % (syst) | 22.7 +- 3 % (stat) +- 4 -> 4 % (syst) | 17.7 +- 3 % (stat) +- 5 -> 6 % (syst) | n/a |
| S_m500 | 0.328 +- 3 % (stat) +- 1 -> 2 % (syst) | 0.783 +- 5 % (stat) +- 6 -> 4 % (syst) | 0.548 +- 2 % (stat) +- 4 -> 4 % (syst) | 29.9 +- 5 % (stat) +- 6 -> 4 % (syst) | 22.9 +- 3 % (stat) +- 5 -> 5 % (syst) | n/a |
| S_m1000 | 0.317 +- 2 % (stat) +- 1 -> 1 % (syst) | 0.941 +- 3 % (stat) +- 5 -> 5 % (syst) | 0.546 +- 2 % (stat) +- 3 -> 3 % (syst) | 36 +- 3 % (stat) +- 5 -> 5 % (syst) | 25 +- 3 % (stat) +- 5 -> 5 % (syst) | n/a |

n/a = no crossing inside the simulated Lambda range (merged-pair edges need the Lambda >= 15 keV points, which exist only for E 200/300/500/700/1000/1200/1500 and Etilde; the 25 µm edge lies above 40 keV for most masses). Interpolated values: deg-2 fit of ln(edge) in ln m over the 7 measured E masses (chi2 4.6/4), fit (stat) error only; ESTIMATE. Stage 4 must add the systematic of the neighbouring measured masses to the interpolated edges (fix R2, C-5).

Robust systematic totals ('after') are upper bounds: 198/243 of the robust l_max/QED/PDF components are below 2x their own template-sampling sd (`robust_shift_sampling_sd_rel`), i.e. noise-limited. Symmetrisation and the treatment of shifts < 2 sigma are deferred to Stage 4 (fix R2, C-4).

m-slopes d ln(edge)/d ln m (linear fit, E): lower_Nosc1_closed -0.007 +- 0.011, lower_lmax_RIT_closed +0.249 +- 0.019, lower_ds100_hit -0.018 +- 0.011, upper_lmax100um_closed +0.249 +- 0.019, upper_merge100_hit +0.248 +- 0.022, upper_merge25_hit +0.258 +- 0.027 (sqrt(m) would be +0.5).

Continuous Lambda handle: median IT pair separation sep_IT, log-log slope over 1-30 keV (error: fix R2, `results/FIX_R2_notes.json`, toys on the per-Lambda bootstrap errors): F_m200 -2.002 +- 0.022, F_m300 -1.997 +- 0.032, F_m400 -2.022 +- 0.040, F_m500 -2.008 +- 0.028, F_m600 -1.993 +- 0.036, F_m700 -1.992 +- 0.026, F_m800 -2.016 +- 0.030, F_m900 -2.008 +- 0.039, F_m1000 -1.985 +- 0.023, F_m1100 -2.014 +- 0.037, F_m1200 -1.997 +- 0.017, F_m1300 -2.020 +- 0.027, F_m1400 -2.012 +- 0.044, F_m1500 -2.008 +- 0.026, S_m200 -2.003 +- 0.018, S_m500 -2.013 +- 0.020, S_m1000 -2.004 +- 0.018 (sep_IT ~ Lambda^-2, i.e. it measures l0 = m/Lambda^2; sep_IT/l_max ~ 0.5-0.6 above 1 keV). Per-point values: `results/P2.json` `sep_IT_handle`.
<!-- END AUTO-RESULTS -->

## Figures (internal; "Private work (simulation) -- truth level", one tag per panel; final restyle in Stage 5)
- `figures/p1_dsB_c.png`: median Δs_B and median c vs Λ; lines: the MG-model Δs_B and the median c_ev on the same events.
- `figures/p1_v2b_revisit.png`: population excess median(c)/median(c_ev) − 1 per cell vs the shift produced by a
  zero-median symmetric scatter with the observed per-event spread (colour = Λ, marker = point). The 1-2 keV cells lie near
  the diagonal (estimator effect); the 0.45 keV cells (law fails) and the 3-5 keV high-k_B cells stand off it. Grey band ±1.5 %.
  Right panel (fix R2, C-7: own x axis): the stratified permutation, a near-identity check by construction (not evidence).
- `figures/p1_B_MS_BM.png`: B-only, material-only and B + material thickness vs Λ (E 500, E 1000).
- `figures/p2_edges_vs_mass.png`: the Λ edges vs mass (E filled, Ẽ open); crosses: merge edge interpolated in ln m.
- `figures/p2_observables.png`: N_osc, Δs_all, IT pair separation (the continuous Λ handle, ∝ Λ⁻²), tracker hits,
  turn-around fraction, merged fraction and hit delay vs Λ at 5 species-masses.
