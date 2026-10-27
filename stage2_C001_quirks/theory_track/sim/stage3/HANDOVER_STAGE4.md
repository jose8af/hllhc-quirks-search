# Stage 3 → Stage 4 handover: the truth-level hit files

E8 (executor), 2026-10-13. Everything here is **truth level**: true hit positions, no digitisation or reconstruction.

Companion documents:
- `SAMPLES.md`: inventory;
- `VALIDATION.md`: the checks;
- `plan.md` §4: design;
- `code/run_stage3.py`: the writer, the authoritative schema.

## 0. Which files to use
- **Index.** `data/sim_stage3/STAGE3_INDEX.json` → `points[<campaign>/<spin>_m<m>/L<Λ>_<cfg>]` → `chunks[]`. Each chunk
  gives the file path relative to `data/sim_stage3/`, the machine, events, hits, md5 and status counts. The same layout
  as symlinks: `data/sim_stage3/canon/`.
- **Stage-4 input** = campaign **`p2`**, configuration `BM`:
  - |η_pair| < 4 propagated; the counting set is |η_pair| < 2.5 (`in_eta25`);
  - luminous-region vertex, all surfaces, nominal material;
  - E 200-1500 (14 masses) and Ẽ 200/500/1000;
  - Λ 0.3-10 keV (16 points) at every mass; 15/20/30 keV (+40 keV for E ≥ 1000, Ẽ ≥ 500) at E {200, 300, 500, 700,
    1000, 1200, 1500} and Ẽ.
- **Material variants:** campaign `mv` (`BMx0.5`, `BMx2`). Same template events as p2, at E 200/500/1000/1500 and Ẽ 500,
  × Λ {0.4, 0.6, 1, 3, 10, 20} keV.
- **P1** (campaign `p1`): |η| < 1, vertex at the origin, configurations B/B2/V/M/BM/×0.5/×2. These are physics checks,
  not Stage-4 input.
- **Template vs toy.** `tt_split` = 0 template, 1 toy. The **toy half was not used in Stage 3** (only counted), so it is
  free for pseudo-experiments. At Λ ≥ 15 keV only E 1000/1200 have toys.
- **Status.** Use status == 1 (both quirks left the tracker volume).
  - Status 4 (108 events, 0.05 %; near-threshold pairs with material): incomplete. Label-swapped replacements for 18 of
    them are in `data/sim_stage3/validation/v7_status4/status4_rerun.npz`. Recommended: drop them and carry them as an
    efficiency loss of ≤ 1.5 % per point. They are near-threshold pairs (γ* − 1 ≤ 0.01, ℓ_max ≪ 100 µm, physically
    merged), so dropping them biases the merging edge one way: worst case (E 1500, 10-40 keV, ≤ 3/200) the merge100 edge
    moves up by ≈ 1.9 %, below its 4 % stat error; carry it as a one-sided systematic or count them as merged (ESTIMATE,
    constructive C-4).
  - Status 0 (85 events at Λ ≤ 0.5 keV, mostly 0.3-0.4 keV; ≤ 4/200 per template point): reached t_end inside the
    tracker, so the late hits are missing. The edges are unaffected (N_osc = 1 is closed form; the Δs = 100 µm edge sits at
    0.47-0.55 keV); only the late-time hit and hit-count observables at 0.3-0.4 keV are affected.
- **Machines.** Mac and PC files are equivalent: kernel output is bit-identical in 224/225 overlap events
  (`results/xover.json`). The `xover/` clones are duplicates; do not count them twice.

## 1. Schema (one npz per job = point × configuration × chunk; `np.load(f, allow_pickle=False)`)
**Units:** mm, ns, GeV (ACTS conventions: multiply by `acts.UnitConstants.mm/ns/GeV`). Thicknesses are in µm (`*_um`),
and ℓ_max is in **cm** (closed form, kernel units).

**Header scalars:**

| field | meaning |
|---|---|
| `job_id`, `complete`, `n_events` | job id (= file path), integrity flag (1) and event count |
| `kernel_version`, `spin`, `m`, `lam_keV`, `cfg`, `max_boost`, `chunk` | point and configuration |
| `meta_json` | JSON: kernel/runner version, code md5s, original-code md5s, input file + md5, Stage-2 source + md5, the selection (incl. the unweighting seed and the tilt exponents), configuration (B0, material, mat_scale, max_boost, hmax, qcap, max_steps, r/z exit), seed rule, env (platform, versions, host), wall/CPU, units, hit columns |
| `job_json` | the job definition (event indices into the input file) |
| `sigma_norm_fb`, `sigma_ref_fb`, `w_max` | Stage-2 normalisation and the common unweighted weight [fb, N_IC = 1] |
| `surf_table` (93 × 4), `surf_names`, `surf_kinds` | recording surfaces: (type 0 cylinder: R, zmin, zmax / type 1 disc: z, rmin, rmax) in **cm**; names and kinds (§2) |
| `wvar_names` (106) | the merged scale/PDF/merging weight names |

**Per event** (length n):

| field | meaning |
|---|---|
| `ev_index`, `row`, `src_chunk`, `ievt_lhe`, `py8_seed` | provenance (row in the Stage-2 TRGS file; joins to the full Pythia record via `sim/scripts/reshower.py`) |
| `tt_split`, `in_eta25` | template/toy split; counting-region flag |
| `w`, `w_orig`, `wvar_ratio` (n × 106, float32) | common weight w_max; original row weight; variation weights / w_orig |
| `w_lmax_up`, `w_lmax_dn`, `w_qed`, `w_qed_19` | plan §7 tilts (ℓ_max ±5 %, QED −1.1 % / −1.9 %), mean 1 on the counting set |
| `p_qp`, `p_qm` (n × 3), `recoil` (n × 4), `jets` (n × 4 × 4) | initial quirk momenta, recoil (MET proxy), jets (Stage 2) |
| `cstar`, `pt`, `eta`, `M`, `gstar`, `x` | pair kinematics (x = 2(γ* − 1)) |
| `ell_max` [cm], `N_osc_vac`, `eps_B`, `eps_perp`, `bodd_l0`, `k_B`, `c_ev`, `C_ev`, `floor_flag` | closed-form truth at B₀ (`s3_physics.pair_truth`); floor_flag = b_odd/ℓ₀ < 10⁻⁷ |
| `vtx` (n × 4) | production vertex (x, y, z, t) [mm, ns] (zeros for the origin vertex) |
| `seed` | per-event kernel seed |
| `status`, `nsteps`, `maxq`, `rerun`, `swapped` | exit code (0 t_end, 1 left volume, 2 stopped, 3 max steps, 4 deadlock, 5 queue overflow); steps; max queue; rerun flag (never set); bootstrap label swap |
| `X_end`, `P_end` (n × 2 × 4), `eacc` (n × 2) | final 4-positions [cm, kernel units] and 4-momenta [GeV]; integrated ionisation loss [GeV] |
| `ds_barrel_um`, `ds_all_um`, `ds_itps_um`, `res_max_um`, `n_plane` | plane thickness through the vertex: 10 virtual T3 layers / all tracker surfaces / IT+PS only; max residual; plane normal (**sign arbitrary**). eigh-based: numerical floor ≈ 0.015 µm |
| `nhit_surf` (n × 93 × 2) | hits per surface per quirk |
| `cpu_s`, `wall_s` | per-event cost |

**Per hit** (CSR: hits of event i are `[hit_offsets[i], hit_offsets[i+1])`):

| field | meaning |
|---|---|
| `h_quirk` | 0 = +q, 1 = −q |
| `h_surf`, `h_icross` | surface id (row of surf_table), crossing index on that surface |
| `h_t`, `h_x`, `h_y`, `h_z` | ns, mm |
| `h_px`, `h_py`, `h_pz`, `h_E` | 4-momentum at the crossing [GeV] (interpolated between the pre- and post-chord momenta, E on shell) |
| `h_dE` (float32) | mean Bethe loss in the active Si thickness along the direction [GeV] (path capped at 20 × thickness) |

**Energy deposit (fix R1, constructive B-6).** The V8 injection built SimHits with p4_before = p4_after, so
`depositedEnergy()` = 0. That is harmless for Gaussian smearing, but a geometric (channelised) digitiser with a charge
threshold — what a CMS-like IT/PS/2S segmentation needs — would drop or mis-weight every quirk hit. **Stage 4 must build
p4_after from `h_dE`:** E_after = E − h_dE with |p| reduced to stay on shell (mass m), so that `depositedEnergy()` = h_dE.
`h_dE` is the mean Bethe loss; Landau fluctuations can be added in Stage 4 if the threshold model needs them.
| `h_dl` (float32) | chord length of the step [mm] |

## 2. Surfaces and ACTS geometry identifiers

**Geometry contract (fix R1, constructive B-7; read first).**
- Every Stage-3 hit lies **on the simplified surfaces** of `surfaces_s3.json` (full cylinders and discs at the D111 nominal
  radii/z), to 2×10⁻¹⁰ µm. **No trajectories are stored**, only the crossings.
- Stage 4 must therefore use the **same simplified surfaces as its sensitive surfaces**, and the Fatras PU-200 hits must be
  simulated on the same surfaces, so that quirk and pile-up hits share one geometry (plan D1 (a)).
- Each cylinder/disc is then one ACTS digitisation "module". That matters for merging and clustering: with the ACTS
  default `doMerge = True` the two quirks' close hits on one surface are merged (§4).
- Straight-line extrapolation from a cylinder to a module plane is not safe for quirks: the plane-cylinder sagitta is
  w²/8R ≈ 1.7 mm on TBPX L1, over which the string force (σ ≈ 5 GeV/mm × (Λ/keV)²) bends the track by O(10 µm) at 1 keV
  and more at higher Λ (ESTIMATE). Module planes (17 092 modules, INSTALL_CHECK §3) therefore mean a rerun of the Stage-4
  subset with a module-plane recorder (plan D1 (b)). This is user decision **U-4** (`DECISIONS_PENDING.md`).

The surface table (`code/surfaces_s3.json`, copied into every file) is the `simplified` block of
`acts/geometry/cms_phase2_public.json` (D111 nominal radii and z):
- each stacked OT module type is represented by two sensors at ±s/2 (`_in`/`_out`);
- TEDD discs are split into PS and 2S parts;
- plus the BTL cylinder and an ETL proxy disc at |z| = 2920 mm (z UNVERIFIED).

Surface kinds:
- **`T3V`, ids 83-92: virtual copies of the 10 T3 barrel radii.** They are used only for the Stage-1 thickness definition.
  **Stage 4 must skip kind T3V.**
- `BTL` and `ETL` are timing layers (no Si thickness).
- The tilted TBPS rings are flat, and the disc ring z-staggering is not modelled (approximations of the simplified block,
  UNVERIFIED).

**Name → GeometryIdentifier.**
- Stage 4 builds its Blueprint from the same JSON and should map by `surf_names` (D111 names), not by Stage-3 id.
- The V8 test (`validation/val_v8.py`) used a provisional map: volume 1, layer = surface id + 1, sensitive 1, one ACTS
  surface per Stage-3 surface built from `surf_table`.

The table, ids 0-92:

| id | name | kind | type | R or z [mm] | z or r range [mm] | active Si [mm] |
|---|---|---|---|---|---|---|
| 0 | TBPX_L1 | IT | cylinder | 30.00 | -200.1 .. 200.1 | 0.15 |
| 1 | TBPX_L2 | IT | cylinder | 61.50 | -201.4 .. 201.4 | 0.15 |
| 2 | TBPX_L3 | IT | cylinder | 104.50 | -201.4 .. 201.4 | 0.15 |
| 3 | TBPX_L4 | IT | cylinder | 146.50 | -201.4 .. 201.4 | 0.15 |
| 4 | TBPS_L1_in | PS | cylinder | 248.14 | -1202.9 .. 1202.9 | 0.20 |
| 5 | TBPS_L1_out | PS | cylinder | 250.74 | -1202.9 .. 1202.9 | 0.20 |
| 6 | TBPS_L2_in | PS | cylinder | 370.88 | -1203.5 .. 1203.5 | 0.20 |
| 7 | TBPS_L2_out | PS | cylinder | 372.48 | -1203.5 .. 1203.5 | 0.20 |
| 8 | TBPS_L3_in | PS | cylinder | 521.90 | -1201.9 .. 1201.9 | 0.20 |
| 9 | TBPS_L3_out | PS | cylinder | 523.50 | -1201.9 .. 1201.9 | 0.20 |
| 10 | TB2S_L1_in | 2S | cylinder | 686.10 | -1174.2 .. 1174.2 | 0.20 |
| 11 | TB2S_L1_out | 2S | cylinder | 687.90 | -1174.2 .. 1174.2 | 0.20 |
| 12 | TB2S_L2_in | 2S | cylinder | 859.10 | -1174.2 .. 1174.2 | 0.20 |
| 13 | TB2S_L2_out | 2S | cylinder | 860.90 | -1174.2 .. 1174.2 | 0.20 |
| 14 | TB2S_L3_in | 2S | cylinder | 1082.10 | -1174.2 .. 1174.2 | 0.20 |
| 15 | TB2S_L3_out | 2S | cylinder | 1083.90 | -1174.2 .. 1174.2 | 0.20 |
| 16 | TFPX_D1_p | IT | disc | 250.00 | 31.0 .. 164.0 | 0.15 |
| 17 | TFPX_D2_p | IT | disc | 319.76 | 31.0 .. 164.0 | 0.15 |
| 18 | TFPX_D3_p | IT | disc | 408.99 | 31.0 .. 164.0 | 0.15 |
| 19 | TFPX_D4_p | IT | disc | 523.11 | 31.0 .. 164.0 | 0.15 |
| 20 | TFPX_D5_p | IT | disc | 669.08 | 31.0 .. 164.0 | 0.15 |
| 21 | TFPX_D6_p | IT | disc | 840.78 | 31.0 .. 164.0 | 0.15 |
| 22 | TFPX_D7_p | IT | disc | 1109.57 | 31.0 .. 164.0 | 0.15 |
| 23 | TFPX_D8_p | IT | disc | 1400.00 | 31.0 .. 164.0 | 0.15 |
| 24 | TEPX_D1_p | IT | disc | 1750.00 | 65.1 .. 254.5 | 0.15 |
| 25 | TEPX_D2_p | IT | disc | 2009.59 | 65.1 .. 254.5 | 0.15 |
| 26 | TEPX_D3_p | IT | disc | 2307.69 | 65.1 .. 254.5 | 0.15 |
| 27 | TEPX_D4_p | IT | disc | 2650.00 | 65.1 .. 254.5 | 0.15 |
| 28 | TEDD_D1_p_PS_in | PS | disc | 1309.80 | 241.1 .. 656.9 | 0.20 |
| 29 | TEDD_D1_p_PS_out | PS | disc | 1313.80 | 241.1 .. 656.9 | 0.20 |
| 30 | TEDD_D1_p_2S_in | 2S | disc | 1310.90 | 656.9 .. 1074.4 | 0.20 |
| 31 | TEDD_D1_p_2S_out | 2S | disc | 1312.70 | 656.9 .. 1074.4 | 0.20 |
| 32 | TEDD_D2_p_PS_in | PS | disc | 1548.00 | 241.1 .. 656.9 | 0.20 |
| 33 | TEDD_D2_p_PS_out | PS | disc | 1552.00 | 241.1 .. 656.9 | 0.20 |
| 34 | TEDD_D2_p_2S_in | 2S | disc | 1549.10 | 656.9 .. 1074.4 | 0.20 |
| 35 | TEDD_D2_p_2S_out | 2S | disc | 1550.90 | 656.9 .. 1074.4 | 0.20 |
| 36 | TEDD_D3_p_PS_in | PS | disc | 1851.40 | 334.8 .. 627.7 | 0.20 |
| 37 | TEDD_D3_p_PS_out | PS | disc | 1855.40 | 334.8 .. 627.7 | 0.20 |
| 38 | TEDD_D3_p_2S_in | 2S | disc | 1852.50 | 627.7 .. 1074.4 | 0.20 |
| 39 | TEDD_D3_p_2S_out | 2S | disc | 1854.30 | 627.7 .. 1074.4 | 0.20 |
| 40 | TEDD_D4_p_PS_in | PS | disc | 2214.19 | 334.8 .. 627.7 | 0.20 |
| 41 | TEDD_D4_p_PS_out | PS | disc | 2218.19 | 334.8 .. 627.7 | 0.20 |
| 42 | TEDD_D4_p_2S_in | 2S | disc | 2215.29 | 627.7 .. 1074.4 | 0.20 |
| 43 | TEDD_D4_p_2S_out | 2S | disc | 2217.09 | 627.7 .. 1074.4 | 0.20 |
| 44 | TEDD_D5_p_PS_in | PS | disc | 2648.00 | 334.8 .. 627.7 | 0.20 |
| 45 | TEDD_D5_p_PS_out | PS | disc | 2652.00 | 334.8 .. 627.7 | 0.20 |
| 46 | TEDD_D5_p_2S_in | 2S | disc | 2649.10 | 627.7 .. 1074.4 | 0.20 |
| 47 | TEDD_D5_p_2S_out | 2S | disc | 2650.90 | 627.7 .. 1074.4 | 0.20 |
| 48 | TFPX_D1_n | IT | disc | -250.00 | 31.0 .. 164.0 | 0.15 |
| 49 | TFPX_D2_n | IT | disc | -319.76 | 31.0 .. 164.0 | 0.15 |
| 50 | TFPX_D3_n | IT | disc | -408.99 | 31.0 .. 164.0 | 0.15 |
| 51 | TFPX_D4_n | IT | disc | -523.11 | 31.0 .. 164.0 | 0.15 |
| 52 | TFPX_D5_n | IT | disc | -669.08 | 31.0 .. 164.0 | 0.15 |
| 53 | TFPX_D6_n | IT | disc | -840.78 | 31.0 .. 164.0 | 0.15 |
| 54 | TFPX_D7_n | IT | disc | -1109.57 | 31.0 .. 164.0 | 0.15 |
| 55 | TFPX_D8_n | IT | disc | -1400.00 | 31.0 .. 164.0 | 0.15 |
| 56 | TEPX_D1_n | IT | disc | -1750.00 | 65.1 .. 254.5 | 0.15 |
| 57 | TEPX_D2_n | IT | disc | -2009.59 | 65.1 .. 254.5 | 0.15 |
| 58 | TEPX_D3_n | IT | disc | -2307.69 | 65.1 .. 254.5 | 0.15 |
| 59 | TEPX_D4_n | IT | disc | -2650.00 | 65.1 .. 254.5 | 0.15 |
| 60 | TEDD_D1_n_PS_in | PS | disc | -1309.80 | 241.1 .. 656.9 | 0.20 |
| 61 | TEDD_D1_n_PS_out | PS | disc | -1313.80 | 241.1 .. 656.9 | 0.20 |
| 62 | TEDD_D1_n_2S_in | 2S | disc | -1310.90 | 656.9 .. 1074.4 | 0.20 |
| 63 | TEDD_D1_n_2S_out | 2S | disc | -1312.70 | 656.9 .. 1074.4 | 0.20 |
| 64 | TEDD_D2_n_PS_in | PS | disc | -1548.00 | 241.1 .. 656.9 | 0.20 |
| 65 | TEDD_D2_n_PS_out | PS | disc | -1552.00 | 241.1 .. 656.9 | 0.20 |
| 66 | TEDD_D2_n_2S_in | 2S | disc | -1549.10 | 656.9 .. 1074.4 | 0.20 |
| 67 | TEDD_D2_n_2S_out | 2S | disc | -1550.90 | 656.9 .. 1074.4 | 0.20 |
| 68 | TEDD_D3_n_PS_in | PS | disc | -1851.40 | 334.8 .. 627.7 | 0.20 |
| 69 | TEDD_D3_n_PS_out | PS | disc | -1855.40 | 334.8 .. 627.7 | 0.20 |
| 70 | TEDD_D3_n_2S_in | 2S | disc | -1852.50 | 627.7 .. 1074.4 | 0.20 |
| 71 | TEDD_D3_n_2S_out | 2S | disc | -1854.30 | 627.7 .. 1074.4 | 0.20 |
| 72 | TEDD_D4_n_PS_in | PS | disc | -2214.19 | 334.8 .. 627.7 | 0.20 |
| 73 | TEDD_D4_n_PS_out | PS | disc | -2218.19 | 334.8 .. 627.7 | 0.20 |
| 74 | TEDD_D4_n_2S_in | 2S | disc | -2215.29 | 627.7 .. 1074.4 | 0.20 |
| 75 | TEDD_D4_n_2S_out | 2S | disc | -2217.09 | 627.7 .. 1074.4 | 0.20 |
| 76 | TEDD_D5_n_PS_in | PS | disc | -2648.00 | 334.8 .. 627.7 | 0.20 |
| 77 | TEDD_D5_n_PS_out | PS | disc | -2652.00 | 334.8 .. 627.7 | 0.20 |
| 78 | TEDD_D5_n_2S_in | 2S | disc | -2649.10 | 627.7 .. 1074.4 | 0.20 |
| 79 | TEDD_D5_n_2S_out | 2S | disc | -2650.90 | 627.7 .. 1074.4 | 0.20 |
| 80 | BTL | BTL | cylinder | 1148.00 | -2600.0 .. 2600.0 | 0.00 |
| 81 | ETL_p | ETL | disc | 2920.00 | 292.0 .. 1185.0 | 0.00 |
| 82 | ETL_n | ETL | disc | -2920.00 | 292.0 .. 1185.0 | 0.00 |
| 83 | T3V_0 | T3V | cylinder | 30.00 | -200.0 .. 200.0 | 0.00 |
| 84 | T3V_1 | T3V | cylinder | 61.00 | -200.0 .. 200.0 | 0.00 |
| 85 | T3V_2 | T3V | cylinder | 104.00 | -200.0 .. 200.0 | 0.00 |
| 86 | T3V_3 | T3V | cylinder | 146.00 | -200.0 .. 200.0 | 0.00 |
| 87 | T3V_4 | T3V | cylinder | 249.00 | -1200.0 .. 1200.0 | 0.00 |
| 88 | T3V_5 | T3V | cylinder | 372.00 | -1200.0 .. 1200.0 | 0.00 |
| 89 | T3V_6 | T3V | cylinder | 523.00 | -1200.0 .. 1200.0 | 0.00 |
| 90 | T3V_7 | T3V | cylinder | 688.00 | -1200.0 .. 1200.0 | 0.00 |
| 91 | T3V_8 | T3V | cylinder | 860.00 | -1200.0 .. 1200.0 | 0.00 |
| 92 | T3V_9 | T3V | cylinder | 1083.00 | -1200.0 .. 1200.0 | 0.00 |

## 3. Seeds and reproducibility
- **Per-event kernel seed:** blake2b(`"spin|m|row|lam|cfg"`, 8-byte digest, little endian) & 0x7fffffff. It does not
  depend on chunking, worker or machine (V6: 50 jobs bit-identical on rerun; V7: 108 status-4 events reproduced, incl. 40
  PC events on the Mac).
- **Vertex:** `default_rng(blake2b("vtx|spin|m|row"))` → (x, y, z, t) ~ N(0, [5 µm, 5 µm, 45 mm, 190 ps]). It is the same
  for an event at every Λ and configuration.
- **Unweighting:** the Stage-2 loader's hit-or-miss, seed 12345. Every event carries w_max (N_eff = N); V9 checks it
  against the weighted mode.
- **Same rows at every Λ** (per species-mass and selection), so Λ-to-Λ differences carry no generator noise.
- **Cross-machine:** Mac arm64 and PC x86-64 give bit-identical kernel output except for rare ulp amplification (1/225
  events, 4.4 µm).

## 4. V8 (Stage-4 ingestion test) status
- Gate (smoke file, E500 1 keV BM, 10 events): 430/430 physical hits `isOnSurface` (1 µm), 573 SimHits → 573
  measurements.
- Production files (`results/V8_production.json`): every physical hit is on its surface, units are right, and t ≥ r/c
  (PASS). The literal measurement-count criterion n_meas = n_SimHits **FAILS** at 10, 15 and 30 keV with the ACTS defaults.
- **Cause (VERIFIED in fix R1, `validation/val_v8_merge.py`, `results/V8_merge.jsonl`):** `DigitizationAlgorithm.Config()`
  (pyacts 48.0.0) defaults to `doMerge = True`, `mergeNsigma = 1`, i.e. smeared measurements on the same surface within
  1σ (14.4 µm here) are merged. Since each Stage-3 surface is one ACTS surface, the **two quirks' close hits** merge in the
  merged regime. With `doMerge = False` the counts are exact:

  | Λ [keV] | 1 | 10 | 15 | 30 |
  |---|---|---|---|---|
  | measurements / SimHits, default (`doMerge = True`) | 491/491 | 463/470 | 442/472 | 375/448 |
  | `doMerge = False` | 491/491 | 470/470 | 472/472 | 448/448 |
  | T3V skipped, one barcode per (event, quirk): default / `doMerge = False` | 378/378 / 378/378 | 360/366 / 366/366 | 336/362 / 362/362 | 296/356 / 356/356 |
  | cross-quirk same-surface pairs < 30 µm (physical surfaces, 10 events) | 0 | 4 | 22 | 72 |

  The losses track the cross-quirk close pairs, not repeated crossings by one quirk (E8's hypothesis, withdrawn).
- **Stage-4 actions:**
  1. set `doMerge` explicitly. The default (1σ = 14.4 µm on whole-cylinder "modules") matches neither physical pixel
     clustering nor "no merging"; the choice is user decision **U-5** (geometric digitisation with CMS-like pitch and
     clustering, or smearing with `doMerge = False`);
  2. skip kind T3V before digitisation (92-113 T3V hits per 10-event file were injected and counted in V8);
  3. inject **one ACTS event per physics event**, with per-event barcodes (vertexPrimary = event) for truth matching.
     This is a **requirement not yet tested**: every V8 variant (A, B, C) still injects the 10 physics events of a file
     into one ACTS event (fix R2, review C-8). It does not affect the counts above, since `doMerge = False` gives exact
     counts in every variant, but Stage 4 must verify it;
  4. fill the energy deposit from `h_dE` (§1).

## 5. Things Stage 4 should know
1. **Precision floor.** B-only thickness is not computable in double precision above ≈ 10-20 keV. The `floor_flag`
   fraction in P2 is 7 / 31 / 53 / 70 / 86 / 99.5 % at 5 / 10 / 15 / 20 / 30 / 40 keV. B+M hit positions are unaffected
   at the µm level (MS-dominated thickness).
2. **Step settings.** max_boost 10⁻³ up to 5 keV, 10⁻² above (V3: hit positions converged below the IT resolution).
3. **Edges** (README, `results/P2.json`):
   - the truth-level thickness edge is at 0.47-0.55 keV, flat in m;
   - ℓ_max = R_IT at 0.43-0.94 keV, with d ln Λ/d ln m = 0.249 ± 0.019 (measured; **not** √m);
   - merged at 100 µm at 13-25 keV (hit level): this is f(sep_IT < 100 µm) = 50 % on the **median-based** truth-level IT
     pair separation, measured at E 200/300/500/700/1000/1200/1500 and Ẽ; at the other E masses it is interpolated
     (`P2.json` `edge_fits_in_m`, flagged). The interpolated values carry the fit (stat) error only (`err_fit`
     0.40-0.58 keV); Stage 4 must add the systematic of the neighbouring measured masses (fix R2, C-5). It is ≈ flat at 19.4-20.4 keV above 700 GeV, so **interpolate the hit-level
     curve in ln m, not √m**. The 25 µm edge exists at 3 masses only (E 200/300/1000).
   - The 100/25 µm thresholds are truth-level pair separations; the physical merging edge is set in Stage 4 by IT
     clustering (25 × 100 µm² pixels; merging in a 2D grid is anisotropic).
   - Use the edges **smoothed in m** (`edge_fits_in_m`; quadratic in ln m with covariance): the F_m800 → F_m900 dip of the
     ℓ_max edges (−11 %) is template statistics (median γ* − 1 0.2525 → 0.1760 in the 200 template events).
   - The continuous Λ handle is the median IT pair separation ∝ Λ⁻² (1-30 keV), `P2.json` `sep_IT_handle`; log-log
     slopes −1.985 … −2.022, each ± 0.02-0.04 (`results/FIX_R2_notes.json`, fix R2 C-3).

   Dense Λ points exist in these regions.
4. **Systematics.**
   - Tilts (`w_lmax_*`, `w_qed*`) and `wvar_ratio` are per-event weights. On 200 template events a reweighted median jumps
     between neighbouring events; use the bootstrap-averaged paired shifts (`P2.json` `systematics.*.robust_shifts`,
     totals `total_rel_robust`) and note that the stat and syst errors share the same 200 events (correlated).
   - The robust totals are **upper bounds**: 198 of the 243 robust ℓ_max/QED/PDF components are below 2× their own
     template-sampling sd (`robust_shift_sampling_sd_rel`), so they are dominated by template sampling noise (fix R2,
     review C-4). Deferred to Stage 4: symmetrisation of the up/down shifts and the treatment of shifts below 2σ (drop
     or keep as noise-limited bounds). Until then use them as conservative bounds, not as measured shifts.
   - P1 paired ratios measured/model exclude 4 events whose c06 rotating-yo-yo model Δs is exactly 0 (an unexplained
     c06 edge case; F_m200/L5 row 54998, F_m1000/L0.45 row 30405, F_m1500/L3 row 735, S_m500/L5 row 22057;
     `results/FIX_R2_notes.json`). Medians are unaffected (fix R2, review C-6).
   - Material ×0.5/×2 is in `mv`.
   - The tail rate (+12…+15 / −11…−13 %) is a normalisation nuisance on yields.
   - σ_norm uncertainties are in the Stage-2 header numbers.
5. **Toys.** At Λ ≥ 15 keV toys exist only for E 1000/1200 (200 each, ≈ 6 independent N = 30 pseudo-experiments per
   point); merged-regime coverage can be tested only there (template ↔ toy swap is free where both exist). More toys: U-3.
6. **Template interpolation (suggestion, constructive C-9):** vacuum observables depend on (m, Λ) via ℓ₀ = m/Λ² and the
   velocities (S-4); interpolating templates in (ℓ₀, ε_B, m) rather than (m, Λ) should reduce interpolation error.
7. The plane normal `n_plane` has an arbitrary sign. The stored thicknesses have a 0.015 µm eigh floor; use an SVD fit
   for sub-0.1 µm work.
