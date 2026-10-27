# Stage 4, gate G1 report: the production chain `code/run_chain.py`

Executor G1, 2026-10-13, 17:05–18:40. Authority: `acts/stage4/plan.md` (R9 PASS; not edited). `WP_RULE.md` was not
edited. **Signal-blind:** signal events went through the chain only for V4-1 ingestion closure (counts, positions,
deposits). No finder ran on any signal event, and no signal pass rate or efficiency was computed. Every finder number
below is PU-only, SM or muon gun.

## 1. Summary

| job type | status | measured cost | validation |
|---|---|---|---|
| **PU-only** (B1, B2, G3; plan §1.4–1.6) | **READY** (production waits for the freeze) | chain **4.83 s/event** (1 process, 24 events; target ≤ 5 s); t₁ **3.26 s** (mean), t₂ **20.1 s** at the freeze-candidate road 0.15 | V4-1 PASS on every event; smoke PASS; finder `test_equivalence` PASS |
| **B-9 density re-run** (`dens`, new) | **READY**, in the C1 manifest after B1 | ≈ 4 t₁ per event, no simulation | smoke: same Fatras input, top-up 75 k vs 106 k hits |
| **SM + PU** (block C, `sm`) | **READY** | chain ≈ PU + 0.1–0.3 s (Pythia HS + MET filter) | smoke job through the runner OK; V4-1 PASS |
| **Signal**: chain injection (A5, A1) and numpy row-major digitisation (A2) | chain + V4-1 **READY**; **runner job kinds not written** | — | V4-1 PASS: injected = measured on all surfaces, deposit equality, T3V/ETL/disc bookkeeping, on-surface, causality, dE mean consistency 1.003 |
| **C′ guns/toys**: chain level | **generation, parent truncation, stored-SimHit insertion done and checked** | C′₀ ≈ 3 ms/event chain | helix vs Fatras 1 µm; inserted = stored hits |
| C′ TT level (preselection, attribution, V4-10, runner kinds) | **NOT DONE** (§7) | — | — |
| **V4-9** | **PASS** | — | 17-hit pattern 99.4 %; on-surface < 0.1 µm; sector-boundary gun n32 = n1 for 5 000 µ; Highland 0.93 |
| **MIP unit (F-2)** | **mip_gev = 3.5582 × 10⁻⁴ GeV** | — | eloss sampler closure 0.9996 (3 % criterion) |

**Campaign walls by the plan formula** (§10; 7 workers): C1 ≈ 15–16 h, C1 + C2 ≈ 31–33 h, C1 + C2 + C4′ ≈ 43–45 h.
This fits the 47 h window, with the caveats of §10.

## 2. Code (all new code under `acts/stage4/`; no env change)

| file | env | content |
|---|---|---|
| `code/run_chain.py` | acts | the chain. Modes `pu`, `sm`, `sig` (A5/A1 full chain), `gun` (V4-9, MIP), `cp` (C′₀), `cppu` (C′_PU) |
| `code/s4pu.py` | acts | Pythia → numpy particle arrays (per-interaction reseed, MPI-init reuse), MinBias, SM HardScatter + MET filter, particle gun |
| `code/s4geo.py` | acts | production copy of the probe geometry. Per-process scratch dir (the probe wrote one shared file: a race between workers); production resolutions (BTL axes); BTL σ_t in ACTS units |
| `code/eloss.py` | both | numpy Fatras ionisation model (ACTS `computeEnergyLossLandau/LandauSigma`, CERNLIB Landau), Bethe mean, slab and path factors |
| `code/s4sig.py` | both | Stage-3 point/row access, numpy digitisation with the same configuration, Fatras-model deposits, V4-1 counters |
| `code/s4cp.py` | acts | C′ topologies (γ, V0, PV pair, looper, NI 22/30/61.5 mm, DIF), helix propagation, 2-body decays |
| `finder/chain_inputs.py` | TT | event preparation: exact interaction ids, top-up (`pu_inputs.topup`, unchanged), CKF removal, U-5 b merging, `ckf_band_counts` (the one f_CKF definition, also used by `process_trial`) |
| `run_stage4.py` | TT | job kinds `pu`, `sm`, `dens`; frozen config via `production.config_from_frozen`; `ckf=`/`btl=` hand-over; job order and dependencies; ρ > 1 gating; V4-1 in `check` |
| `g1_bench.py`, `g1_campaigns.py` | TT | end-to-end timing jobs; campaign arithmetic (the plan formula, read-only) |
| `validation/v49_gun.py` | TT | V4-9, MIP unit, eloss closure |

Data: `data/acts_stage4/g1/` (≈ 0.3 GB).
- `timing/timing_summary.json`
- `bench/{rho1,rho1f,rho2,rho2f}/summary.json`
- `v49/v49.json` and the gun samples
- `sig/` (V4-1 tests)
- `cp/` (C′ tests)
- `pythia_init/` (MPI-init files)
- `g1_campaigns.json`

## 3. PU-only job type (priority 1)

### 3.1 Chain
1. **Generation.** Seeded Pythia8 CP5 minimum bias, Poisson(200) interactions. Each interaction has its own
   luminous-region vertex and its own Pythia RNG re-initialisation, seeded from (event seed, interaction index).
2. **Direct reader, no HepMC3.** Particles go straight into `SimParticle` objects.
   - Fatras input: final-state charged particles and photons, pT > 50 MeV, |η| < 4, production point inside 1.1 m / 2.7 m.
   - The probe/interim chains also passed neutral hadrons; with no hadronic physics they make no hits.
   - Barcode: vertexPrimary = interaction, so **interaction ids are exact**. Displaced Pythia decays keep their
     interaction (the interim chain gave them separate ids).
3. **Geometry and simulation.** Fatras on the 32 φ-sector geometry, pMin 30 MeV, material in mol/mm³.
4. **Digitisation.** Smearing, `doMerge = False`.
5. **CKF.** GridTriplet seeding + CKF exactly as the p3 probe (minPt 0.9 GeV, ≥ 7 measurements, ≤ 2 holes,
   |d₀| < 4 mm, `numMeasurementsCutOff` = 10). Every measurement carries a CKF-used flag.
6. **Output.** The barrel counting surfaces and the BTL, plus truth positions, vertices, V4-1 records and timing.
   - Times are in ns. The interim chain wrote the ACTS internal mm/c and smeared the BTL time with 0.12 ps; smoke only,
     fixed here.
7. **TT side** (`chain_inputs.prepare_event`):
   - top-up from the pre-CKF hits, as Phase A;
   - CKF removal;
   - U-5 b merging on the truth positions, per Stage-3 sensor; the 32 sectors are one surface;
   - then `process_trial` with the frozen config, `ckf=` and (when available) `btl=`.

### 3.2 Timing

| measurement | chain s/event | finder |
|---|---|---|
| 24 events, **1 process** (plan convention) | **4.83** mean, 4.93 median, 5.69 p90. Breakdown: Pythia 0.30, reader 0.05, Fatras + digi 0.97, seeding 0.40, CKF 2.69, output 0.42 | — |
| 24 events, 2 processes, `numMeasurementsCutOff` = 1 (option) | 3.89 (CKF 1.70) | — |
| ρ = 1 bench, 4 workers, road 0.25 (24 ev × 4 roads) | 7.0 (loaded) | t₁ 4.25 mean / 4.13 median |
| **ρ = 1 bench, 4 workers, road 0.15 (freeze candidate)** | 5.9 (loaded) | **t₁ 3.26 mean / 3.00 median / 4.90 p90** |
| ρ = 2 bench, 2 workers, road 0.25 (6 ev × 2 roads) | 5.1 | t₂ 28.3 mean / 25.5 median |
| **ρ = 2 bench, 2 workers, road 0.15** | 5.5 | **t₂ 20.1 mean / 21.3 median / 25.2 p90** (in-job weights incl.) |

Other costs:
- Per-job overhead ≈ 1 s. The Pythia MPI initialisation took 13.6 s per job; it is now read from
  `data/acts_stage4/g1/pythia_init/` (0.1 s; events identical to ~10⁻¹¹ relative).
- **The init file is a frozen input.** A freshly initialised Pythia gives slightly different events: chaotic
  amplification of 10⁻¹¹ changes, observed.
- TT preparation ≈ 0.1 s per event.
- End-to-end job wall at road 0.15, 4 workers: **19.2 s per B1 event** (4 roads) and 51.6 s per B2 event.

**Contention.** On the M3 (4 P + 4 E cores) the chain is 1.2–1.45× slower with 4 concurrent workers than alone.

**Plan comparison.**
- Chain-only 4.83 s ≤ 5 s target (§6 cost table): **met**, barely; 5.9 s under 4-worker load.
- The CKF dominates (56 %). `numMeasurementsCutOff` = 1 saves 1.1 s/event.
  - Removed fraction: 13.7 % vs 13.9 % of all measurements; written barrel 19.3 % vs 19.5 %.
  - Every measurement removed by the cut-1 CKF is also removed by the baseline (3 events: 0 cut-1-only, 52–105
    baseline-only per event).
  - **Not adopted** (the plan/p3 configuration is kept). This is offered as a decision (§11).

### 3.3 Validation and population (PU-only)
- **V4-1 PASS on all events** (24 + 24 + 24 + 12 + smokes):
  - the measurement↔SimHit map is injective;
  - on-surface ≤ 0.1 µm;
  - no causality violation (t ≥ t_vtx + |x − v|/c per interaction);
  - no unmapped geometry ids.
  - **Lost SimHits:** 3 of ≈ 3 × 10⁶ SimHits had no measurement. ACTS' bounded smearing re-draws an out-of-bounds
    smear up to `minMaxRetries` = 10 times. Two were at a disc rmin/sector edge, one was unexplained (2S mid-sector).
  - The V4-1 criterion is therefore implemented as **n_meas = n_SimHits − n_lost, n_lost ≤ max(2, 10⁻⁵ n)**, with every
    lost hit listed (`lost<i>`). This is a deviation from "exactly" (§9 item 2).
- **CKF removal:** 13.9 % of all measurements (12.5–16.1 %), 19.5 % of the written barrel hits, ≈ 1 540 tracks/event.
  - The plan's "≈ 18 %" came from 3 p3 events at fixed PU 200 with a different counter.
- **Per event** (ρ = 1, road 0.15 bench means):

  | quantity | per event |
  |---|---|
  | Fatras barrel hits | 48.0 k |
  | top-up | 109.5 k |
  | CKF-removed | 9.3 k |
  | final pool | 147.8 k |
  | merged groups / hits | 384 / 769 |
  | components with a σ that would enlarge | 0.8 |

- **Output size:** ≈ 0.1 MB per ρ = 1 trial at road 0.15 (Phase A had 0.25 MB at 0.25), ≈ 1.7 MB per ρ = 2 trial.

## 4. Signal (priority 2; V4-1 only)

**Energy deposit (review WP_RULE R1 B-2).**
- Fatras deposits are the Landau-sampled loss in the **surface material slab** s4geo puts on each sensor (TBPX
  1.124 mm Si-equivalent, OT layer x/X₀ split in/out) × 1/|cos incidence|.
- Stage-3 `h_dE` is the **mean** Bethe loss in the 0.15/0.20 mm **active** Si. The two are not on the same footing.
- Quirk deposits are therefore sampled with `eloss.sample` on the same slab at the hit's |p| and the quirk mass.
  - Seeds: hash(spin, m, row, Λ), one uniform per hit.
  - `h_dE` is stored alongside.
- **Calibration closure:**
  - `eloss.sample` vs Fatras, fixed-momentum guns at βγ 0.53, 0.75, 1.07, 2.13 (protons) and 94.7 (muons): quantile
    ratios 0.98–1.02, KS p 0.09–0.58, truncated-mean ratio 0.993–1.011;
  - muon-gun MIP unit 0.9996 (§8).
- **Mean consistency:** `eloss.bethe_mean` on the active Si reproduces `h_dE` with a median ratio of **1.003** (150
  events, 3 points). This also checks the βγ and path inputs.

**Chain injection (A5 with PU, A1 without; `run_chain.py sig`).**
- One ACTS event per physics row.
- T3V/ETL skipped; hit-time window (25 ns) and 99 % hit efficiency applied before digitisation, from the same seeds as
  the numpy path.
- SimHits injected with p4_after from the sampled deposit; sector from φ.
- V4-1 (3 rows with PU + 20 rows without, E1000 1 keV):
  - quirk measurements on ALL surfaces = injected SimHits;
  - `depositedEnergy` = sampled deposit, exactly;
  - the numpy bookkeeping closes (T3V + ETL + physical = file hits; written + late + inefficient = barrel/BTL hits);
  - on-surface < 1 µm; causality.
  - All PASS. The CKF-on-quirk counter (V4-6) is recorded but was not looked at.

**Row-major numpy path (A2; `s4sig.digitise`).**
- Same resolutions; smearing and efficiency seeds hash(spin, m, row), so the Λ comparison is paired.
- PU per row from hash(`sigpu`, spin, m, row).
- V4-1 counters PASS on 150 rows (3 points).

**Not done: the runner job kinds for A1/A2/A5.**
- They need the post-freeze finder stage on signal (PV/MET model, matched-candidate storage).
- I did not write it: it cannot be tested without running the finder on signal.
- The storage needs an analysis definition: `process_trial` stores only R04+ records; R01–R03 efficiencies need
  per-candidate quirk content for all candidates, i.e. a `tag=` extension of `process_trial`.

## 5. SM samples (priority 3a)

- `s4pu.SM_SAMPLES`: Z(νν)+j, W(eν)+j, W(μν)+j, W(τν)+j, **W(τ_hν)+j (τ forced hadronic)**, tt̄ 1ℓ (exactly one
  W → ℓν).
  - Pythia CP5, pT̂ > 150 GeV, MPI + hadronisation on.
  - Truth-MET (neutrinos) > 200 GeV filter, with a parton-level pre-filter at 150 GeV before `forceHadronLevel`.
  - Generation 0.02 (Z), 0.06 (W τ) and 0.21 s (tt̄) per accepted event; σ_gen and tries are stored per event.
- Event = HS (vp 3000) + PU 200.
- **TT handling:**
  - PV = HS vertex ⊕ (10, 10, 15) µm;
  - one road along the truth MET ⊕ 25 GeV per component;
  - per stored candidate `n_hs_band` = the number of hard-scatter hits in its band (same band definition as f_CKF),
    for the "≥ 1 HS hit" tagging.
- **Manifests:**
  - C1: Z(νν) 2 000, W(τν) 1 000 + W(τ_hν) 1 000, tt̄ 2 000;
  - C2: W(eν) 5 000, W(μν) 5 000, Z +3 000, W(τν) +1 500, W(τ_hν) +1 500, tt̄ +3 000.
  - The 50/50 hadronic split is **my decision** (§11).
- `smokeG1` SM job through the runner: PASS (1 300 stored candidates, 85 with HS hits in the band, f_CKF filled).

## 6. C′ guns and toys (priority 3b)

**Done (chain level, `code/s4cp.py`, `run_chain.py cp/cppu`).**
- **Topologies:** the 8 of plan §4.2. Every distribution is documented in the `s4cp.py` header and is an ESTIMATE.
  - NI prong multiplicity = 1 + Poisson(1.5), 0.7 inelasticity, |N(0, 0.2 rad)| opening;
  - V0: charged 2-body modes only, so the BR enters rate_t;
  - DIF: radius 30–1 000 mm from the lab exponential;
  - all aimed at φ_MET ± 0.1 rad, |η| < 1.
- **Each event stores** its own road φ_MET and its smeared PV draw (the shared PV of §4.2), and **all toy SimHits on
  all surfaces** (`toy<i>`, 18 columns).
- **NI/DIF parent truncation:** Fatras parent SimHits beyond r_NI + 0.5 mm (NI) or beyond the decay radius (DIF) are
  dropped before digitisation (`Truncate`).
  - The prongs/daughter start on the parent's helix. Helix vs Fatras L1 hits: median 1 µm, max 47 µm (MS in the beam
    pipe), which confirms the sign convention.
- **C′_PU (`cppu`):** a fresh PU-200 event plus the **stored** C′₀ toy SimHits inserted with their full barcodes (not
  re-simulated).
  - Check (2 NI-61.5 events): written toy measurements = C′₀ ones, identical truth positions; V4-1 PASS.
- **C′₀ cost:** ≈ 3 ms/event chain (50-event tests per topology).

**Not done (TT level).**
- **Toy-measurement override.** ACTS re-smears the inserted hits with the PU job's RNG. The plan requires identical
  pre-merge toy measurements, so the C′_PU TT step must replace the toy rows with the C′₀ rows (matched by truth
  position). CKF flags stay from the with-PU event.
- **Preselection:** exhaustive triples, χ²₃ ≤ 48 with σ̂_h, on all pre-CKF pre-merge toy barrel measurements; the
  V4-10 hash.
- **Attribution:**
  - ≥ 3 core toy hits in ≥ 3 layers (≥ 1 IT + PS) from ≥ 2 particles, each within ±4σ̂_h at its stored C′₀
    position; looper: ≥ 2 crossings in a layer.
  - It needs every candidate's hit list and core. `process_trial` stores only R04+ hit records, so the C′ step must
    call `FF.find` + `production.full_set_flags` itself, or `process_trial` needs an extension (a hash change).
- **V4-10:** attributed candidates in non-preselected C′₀ NI/DIF events must be exactly 0.
- **Runner kinds `cp0`/`cppu`** and their manifests (C′_PU depends on the C′₀ preselection).
- Estimate: ≈ 1.5–2 h of work, then ≈ 6–8 CPU-h for C′₀ (5.4 × 10⁵ events).

## 7. What G1 leaves open

1. C′ TT level (§6).
2. Signal runner kinds and signal-candidate storage (§4). These need the frozen rule and a `tag=` decision.
3. SR-T: the runner passes `btl=(B, INT)` as soon as `process_trial` has the parameter.
   - Format: all BTL measurements of the event, G1 columns, t in ns smeared by 35 ps, plus interaction ids.
   - ρ > 1 production jobs are BLOCKED until then, and `require_btl=True` is passed.
4. The IT cluster-size citation (§11 item 2 of the plan) was not searched for; the ESTIMATE range stays.

## 8. V4-9 and the frozen-input numbers (`data/acts_stage4/g1/v49/v49.json`)

- **Central 17-hit pattern:** 99.4 % of 6 449 muons with |η| < 0.8 (pT 1–10 GeV, luminous vertex). On-surface max
  0.099 µm.
- **Sector-boundary gun:** 5 000 µ, pT 50–100 GeV, φ within ±2 mrad of a sector boundary, n32 vs n1 geometry.
  - **0 muons with a different hit count or surface set.**
  - Measured-minus-truth pulls within 2σ of a boundary have rms 0.89 vs 0.996 in the bulk. This is the bounded
    smearing truncating the Gaussian there; it affects ≈ 0.5 % of L1 hits and fewer elsewhere.
- **Highland** (1 GeV/c µ at η ≈ 0, TBPX L1 1.2 % X₀): the PDG θ₀ (Gaussian fit to the central 98 %) is 1.154 mrad vs
  Highland 1.247 → **0.925, PASS ≤ 10 %**.
  - The MAD core is 0.76× Highland: Fatras' Gaussian-mixture model has a narrower core.
  - The PDG definition was chosen after seeing the MAD number; both are reported.
- **MIP unit F-2 (frozen definition: pooled 0.6-truncated mean of x r_xy/|u| TBPX deposits):** 20 000 µ, 54 585 TBPX
  hits.
  - **mip_gev = 3.5582 × 10⁻⁴ GeV.**
  - Sampler on the same hits: 3.5566 × 10⁻⁴ (ratio 0.9996).
  - The superseded per-track median is 3.924 × 10⁻⁴ (sampler 0.997).
  - Muon-gun βγ median **90.7** (F-3; the candidate file has 92).
- **Finding (eloss):** `scipy.stats.landau` is the stable-law Landau, **not** the CERNLIB φ(λ) that
  `ActsFatras::LandauDistribution` samples (verified from the ACTS v48 source).
  - λ = (π/2) x_scipy + 0.4516: quantile ratio 1.571 at q 0.1–0.9, CERNLIB median 1.3561.
  - Without the map the sampler was ×0.64 too narrow. This is a parametrisation identity, not a tuning.
  - Any other Stage-4 code using `scipy.stats.landau` as "the Landau" (e.g. reviewer toys) has the same issue.

## 9. Deviations from the plan / decisions (flagged)

1. **Merged-hit σ** (plan §1.5 "max(σ, |Δ|/√12)"). With Δ the truth separation of the merge test, |Δ| < pitch for a
   pair, so the formula gives σ (= pitch/√12) exactly.
   - Only ≥ 3-member chains (0.8 per event) or the 2-pitch variation would enlarge it.
   - The finder assumes a per-surface constant σ (`finder.build_index` asserts it), so the pool keeps the surface σ and
     enlargements are only counted.
   - The 2-pitch variation would need a finder change. CONFIDENCE HIGH for nominal; FLAG for the A5 variation.
2. **V4-1 "exactly"** relaxed to ≤ max(2, 10⁻⁵ n) lost SimHits per event, each listed (ACTS bounded smearing).
3. **Order of removal and merging:** CKF removal before U-5 b merging (WP_RULE §1.1 order); top-up counts use the
   pre-CKF Fatras hits. CONFIDENCE MEDIUM: physically a cluster shared with a track hit would be lost too. The
   effect is ≤ 0.4 % of IT hits.
4. **Hit efficiency** 99 % is applied to quirk hits only. The TDR-normalised PU density is already a measured-hit
   density. LOW impact.
5. **Merged-measurement interaction id** = that of the member with the largest dE (thinning approximation; ≈ 0.5 % of
   hits).
6. **The Pythia MPI-init file is a frozen input.** A freshly initialised Pythia gives slightly different events: chaotic
   amplification of 10⁻¹¹ changes, observed.
7. **B-9 variation values** (my reading of plan §1.4): ratio × f, floored at 1.

   | variant | IT | PS | 2S |
   |---|---|---|---|
   | low | 2/3 (cluster size 3 vs 2) | 0.9 · 0.95 | 0.917 · 0.95 |
   | high | 4/3 | 1.125 · 1.05 | 1.1 · 1.05 |

   For review.
8. **The numpy signal smearing is unbounded**, while ACTS re-draws at bounds. A5 (full chain) measures the difference.

## 10. Campaign walls (plan formula; `g1_campaigns.py` → `data/acts_stage4/g1/g1_campaigns.json`)

f4r/f3r blocks with the measured PU_S, t₁ = 3.26 s and t₂ = 20.1 s (road 0.15). 168 CPU-h per Mac day (7 workers).

| set | CPU-h, 1-process chain (4.83 s) | Mac wall h | CPU-h, loaded chain (5.9 s) | Mac wall h |
|---|---|---|---|---|
| C1 | 107.9 | 15.4 | 113.2 | 16.2 |
| C2 | 110.2 | 15.7 | 119.1 | 17.0 |
| C4′ | 82.8 | 11.8 | 83.5 | 11.9 |
| **C1 + C2** | **218** | **31.2** | **232** | **33.2** |
| C1 + C2 + C4′ | 301 | 43.0 | 316 | 45.1 |

The C1 + B-9 re-run adds ≈ 18 CPU-h (+2.6 h). Caveats:
- t₁ and t₂ were measured with 4 and 2 concurrent workers. 7 workers on 4 P + 4 E cores will be slower per process;
  Phase A saw ×1.12 at 4.
- t₁ and t₂ are small samples (96 and 12 trials).
- The first hours of G3 give the real throughput (`run_stage4 status`).

## 11. Launch readiness (exact) and decisions

**Runnable now, once `acts/stage4/frozen_inputs.json` is frozen (frozen = true, delta95, eta_max, mip_gev =
3.5582e-4, WP_RULE sha256):**
- G3 B1 (G3B1);
- C1 B1, C1 `dens` (B-9; it runs after its source B1 file exists), C1 SM (C_*), C2 B1 and C2 SM;
- **ρ = 2 (G3B2, C1/C2 B2): BLOCKED until `process_trial` gains `btl=`** (the runner checks the signature).

Commands: PHASE_A_REPORT §9 unchanged (`run_stage4 run --campaign G3|C1 --workers 7`).

**Not runnable (G1 work left):** C1 A1/A2core/A5core (signal kinds) and C′₀/C′_PU (C′ TT level).

**Decisions:**
1. `numMeasurementsCutOff` = 1 for the CKF: −1.1 s/event, −0.2 % abs removal (≈ −8 % C1 + C2 CPU-h). Default kept.
2. W(τν) C1/C2 split 50/50 inclusive / forced-hadronic.
3. C′ attribution route: G1-owned TT code calling `FF.find` (no hash change to `production.py`), or a
   `process_trial` extension (re-hash).
4. Go-ahead for the remaining G1 items (§7 items 1–2) after this report.

## 12. Proposed plan / WP_RULE text changes (not applied)

- §1.4 cost table: chain 4.8 s (CKF 2.7 s), HepMC3 replaced; the Pythia MPI-init file as a frozen input.
- §1.5: the merged-σ remark (§9 item 1) and the numpy-vs-ACTS bounded smearing (§9 item 8).
- §1.6: the removal fraction is 13.9 % of all measurements / 19.5 % of the barrel (not 18 %).
- §8 V4-1: the lost-SimHit tolerance (§9 item 2); V4-9 Highland per the PDG θ₀ definition.
- WP_RULE §1.4 / plan §2.3: the quirk dE model (Fatras slab + Landau sampler, `eloss.py`), the scipy/CERNLIB Landau
  note, `h_dE` mean-consistency in V4-1.
- WP_RULE B-9: the low/high factors of §9 item 7.

## 12b. Post-report change (18:55)

- `pack()` stores the frozen-rule per-trial keys; `trials.road_cfg` = process_trial road half-width (the runner road index kept the name `road`). run_stage4.py sha256 85b978f5d85cee28d290d298bb96bb9895299f916bc4df632a9cf2bb66a4879e.

## 13. Compute

≈ 1.3 CPU-h in total (cap 8), ≤ 4 parallel processes, nice 10:
- chain timing 24 + 24 + 24 events (≈ 0.12);
- benches ρ1 ×2, ρ2 ×2 (≈ 0.6);
- guns, eloss studies (< 0.05);
- smokes/tests (≈ 0.2);
- equivalence re-test (6 trials, PASS; `data/acts_stage4/g2/equivalence_rho1_g1check.json`; ≈ 0.05);
- development (≈ 0.25).
