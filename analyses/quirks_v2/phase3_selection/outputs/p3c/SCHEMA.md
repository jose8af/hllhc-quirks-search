# Schema of the p3-c result files (`phase3_selection/outputs/p3c/`)

Written by `src/p3c/p3c_validate.py` and `src/p3c/p3c_dp2.py`. All yields are events in 3 ab^-1 unless a key says
`sigma_*_pb`. Every number is ESTIMATE (generator-level Pythia 8 LO x K, MET model of p3-c); everything that depends
on the jet-response tail carries "NOT SOURCED".

## `model.json` (the model's derived parameters; input of every other script)
| key | meaning |
|---|---|
| `sigma_soft.{nominal,25,32.5}` | Gaussian soft-term width per component [GeV] for the u_perp targets 29.8, 25, 32.5 GeV |
| `v_perp_no_soft`, `v_par_no_soft` | variance [GeV^2] of the recoil components in Z->mumu, pT(Z) > 30 GeV, without soft term |
| `soft_mix_fit34` | (f2, sigma1, sigma2) of the two-Gaussian soft term fitted to the Fig. 34 shape (variation `soft_mix`) |
| `best_single_gaussian_fig34` | best single-Gaussian width by the same measure (record only) |

## `validation.json`
`reading_RB.<variant>`: `u_par_rms`, `u_par_rms_err`, `u_par_ref`, `u_par_tolerance`, `u_par_passes`, `u_perp_rms`,
`tail.<threshold>.{model,figure,ratio,tolerance,passes}`, `shape_model`, `shape_figure` (20 bins of 6 GeV), `RB_passes`.
`reading_RA.<variant>`: `points[]` (`sumet`, `n_events`, `model_rms`, `model_rms_err`, `figure`, `tolerance`,
`populated`, `passes`), `curve[]`, `RA_passes`. `verdicts.{RB,RA}`: booleans for the nominal model.

## `p3c_results.json` (read by the projection script of p3-a)
| key | meaning |
|---|---|
| `n_trig.<p>` for p in `ztt`, `zll`, `multijets`, `znn`, `mjw`, `mjs` | `N_trig` (nominal), `K`, `rel_stat` (relative MC error), `n_eff_passing`, `ratio_to_nominal.<variation>`, `full_variation.{lo,hi,ln_width}` (envelope over all variations: the "not validated" width of STR l.1387), `ln_core`, `ln_jes`, `ln_soft`, `ln_tail_not_sourced` ([down, up] log shifts), `trigger_nuisance_erf_shifted_ratio`, `N_trig_by_met_cut` |
| `events_per_Z_pilot_count.primary_STR_literal` | `N_SM`, `M`, `events_per_count`, `Z_alone`: **replaces the provisional 41** (definition in the key `definition`) |
| `events_per_Z_pilot_count.secondary_Z_rescaled`, `.tertiary_all12_rescaled` | the two other readings; `by_variation_primary`, `not_validated_range_primary` |
| `pilot` | `M_v2.<variation>` (sum of v2 weights, full class), `M_v2_low_class`, `n_pass_v2`, `M_v2_mean20`, `M_v1_recomputed`, `ratio_sumw_v2_over_v1` |
| `pool_rule6` | `planning`, `reallocated`, `reallocated_v2_weight_fraction`: per process `N_t`, `M_t` (full-weight events), `cpu_h`, `floor_68`; `floor_sum`; `multijets_own_population` |
| `checks.b_multijet_bias` | internal check (b): `N_weighted`, `N_sliced`, `ln_ratio`, `sigma_ln`, `n_eff`, `verdict` |
| `checks.a_continuity_znn_unfiltered`, `checks.c_multijet_share` | reported, no verdict |
| `samples.<process>` | pooled generator sums: `sigma_gen_pb`, `var.<variation>.{sigma_pb,f_presel,n_eff}`, `cutflow`, `by_pthat`, ... |
| `frozen` | the frozen planning inputs used (v1 N_trig of the twelve processes, planning values of the additions, M of v1) |

## Per-event v2 weights of the pilot: `data/p3c/p3-c-pw2/000/p3-c-pw2-NN.npz`
Array `w` (one row per pilot event, file order of `tools/runner/examples/p3c/p3-c-pw2-NN.txt`), columns in `meta.cols`:
`chunk` (pilot file number), `event` (index in the file), `truth_met`, `w_v1`, `n_gamma_veto`, `met_reco_v2`,
`p_v2_mean20` (mean weight of 20 throws), `w_v2_trig_erf_shifted`, `w_v2_<variation>` (single-throw weight, the same
random numbers for every variation), `phimet_reco_v2` (azimuth of the nominal MET_reco of that throw: the
road axis under the v2 model). Campaign `p3-c-pw` holds the same rows without the last column (weights identical,
checked). A pilot event belongs to the v2 full-weight class if `w_v2_nominal > 0` and
`n_gamma_veto == 0`; M = sum of `w_v2_nominal` over that class (w_max = 1).
