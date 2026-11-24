# Schema of the p3-b machine-readable outputs (Casper, 2026-11-24)

Two files; both are written by scripts in `phase3_selection/src/p3b/` from the development campaigns `p3-b-thin`,
`p3-b-direct`, `p3-b-occin`, `p3-b-occmod` (markers in `ledger/markers/p3-b-*`). No signal sample is read.

## `pileup_term.json` (schema `p3b.pileup_term.v1`) — the file p3-a's day-15 projection reads

Units: a **rate** is the number of distinct pile-up hit sets (groups, [SD4]) per trial (one trial = one triggered event
with one MET road). The pile-up term in events is `rate_per_trial × N_trig`. The file carries `events` computed with
`N_trig_used` = 4.0848×10⁷ (the value of the frozen projection script, `phase1_strategy/src/strategy_budget.py` l.68);
**p3-a multiplies `rate_per_trial` by its own N_trig** (MET model) and must not use `events` if its N_trig differs.

Top level:
| key | meaning |
|---|---|
| `schema`, `source`, `source_sha256` | version; the closure JSON this file was computed from, and its hash |
| `N_trig_used`, `N_trig_source` | see above |
| `no_credit_value` | the pile-up term's no-credit value (zero-count bound of the 96,000-trial direct sample, STR l.1177; mean N_trig/96,000 as drawn by the frozen script) — unchanged by p3-b, recorded for completeness |
| `estimators.occupancy` | `s_model` (B2-b definition: max(|ln r| at the held-out development R06, in-sample r.m.s. at R04–R05)), `cap` = ln 1.5/3, `above_cap` (bool), `s_model_trend_variant`, `crossing_2S_dev` (number of evaluable development 2S crossing rungs, whether all are within ln 1.5, their r.m.s. `s_f`) |
| `estimators.thinning` | `s_model_cumulative` (r.m.s. of ln r over the evaluable development cumulative rungs), `s_model_with_crossing` (crossing rungs included; the frozen text does not say which, both reported), `cap`, `above_cap`, `above_cap_with_crossing` |
| `both_estimators_above_cap` | bool: the STR §11.7 rule-1 pause condition "if both pile-up estimators are above their cap" evaluated with the cumulative thinning s_model; if the two thinning readings disagree, the artifact says so |
| `candidates` | one record per candidate key (below) |

Candidate keys: `R04`…`R09` (family `s0`: cumulative ladder rung, no 2S requirement) and `R04x2S>=3`…`R09x2S>=3`
(family `s3`: the same rung AND N_2S2 ≥ 3, i.e. the crossing rung of the 2S family; R09 includes the fit-probability
cut p > 10⁻³). Per record:
| key | meaning |
|---|---|
| `family` | `s0` or `s3` |
| `occupancy_day15` | **the day-15 pile-up term** (STR l.2737-2741: the development occupancy model with its R04–R07 inputs): `rate_per_trial`, `events` (at `N_trig_used`), `mc_rel_error` (Monte-Carlo error of the model expectation, relative), `fitprob_fraction` (R09 only: the pass fraction p > 10⁻³ of development finder groups at R06, a shared input, Df-2) |
| `occupancy_B2b_model` | the B2-b model (inputs at R04–R05 only): `rate_per_trial`, `events`, `ln_r_dev` (against the development direct count; R06 is the held-out rung), `sigma_tot_dev` |
| `width_s_tot` | log-normal width s_tot (STR §4.0 point 7) under three bookkeepings: `planning_cap_with_2S_credit`, `planning_cap_no_2S_credit` (the frozen projection's planning convention: s_model at the cap, width family tested at R06–R07 at 4a), `measured_dev` (measured s_model, development evaluability: width family tested at R06 only, 2S credit if the development 2S crossing comparisons are all within ln 1.5). For `s0` candidates the two planning entries are equal. Which one the binding reading uses is fixed by the frozen projection text, not here (artifact §6) |
| `distances` | d_in and d_out behind each width |
| `thinning` | repaired-thinning rate (development ρ = 2 sample), `s_boot` (relative bootstrap error over ρ = 2 events), `N_eff` = 1/s_boot² |
| `direct_dev` | development direct count (C1 ρ = 1, 16,000 trials), rate, events |

The term enters the projection as a log-normal with median `occupancy_day15.events` (rescaled to p3-a's N_trig) and
width `width_s_tot[<convention>]`, censored at the no-credit value as the frozen script does.

## `b2_dev_closure.json`
Development closure numbers behind the artifact: `direct` (counts and rates per column), `thinning` (rates, union
rates, s_boot, N_eff, the closure block per rung with ln r, σ_tot, evaluability and tolerance (a), the χ² tests (b) with
and without s_model, JFC alarm flags, s_model, slope options, the B2-g projection), `occupancy` (P_real on real hits,
E_model, correlation factors C_R04/C_R05, N_cfg, in-sample residuals, predictions per column with ln r, held-out R06,
s_model, fit-probability fractions, the day-15 scale). Column names are `src/p3b/cols.py`.

## Review cycle 1 additions (fixer Ivar, 2026-11-24; P3B v2) — no v1 key changed
**Status for every reader (p3-a included):** both estimators are above the cap; the R08/R09 values in `occupancy_day15`
and `occupancy_B2b_model` are **the rule-1 projection input only, "no credit"** (advisor B2CAP point 8 (ii)); the
widths are bookkeeping that would apply only to a submitted estimator. Two day-15 readings exist and neither is chosen
here (P3B v2 §6.1): (i) `occupancy_day15` (one scale on R04–R07), (ii) `occupancy_B2b_model` (R04–R05 normalisation).
| key | meaning |
|---|---|
| `no_credit_value.events_zero_count_68_dev16000` | N_trig·1.14/16,000 = 2,910: the zero-count bound of the 16,000 development trials, a reading of "the samples that exist at day 15" to flag (P3B v2 §6.3), not chosen |
| `candidates.R09*.occupancy_B2b_model` | now filled: the B2-b R08 (resp. R08x2S>=3) value × `fitprob_fraction` (was `null` in v1) |
| `width_s_tot.planning_cap_lastR06_with_2S_credit`, `..._no_2S_credit` | planning convention (s_model at the cap) with R06 as the last evaluable width-test rung (R07 not evaluable at the development direct rate, P3B §3.4); the v1 `planning_cap_*` keys keep R07 as last test rung (evaluable only at v1's rate) |

`is_check_stats.json` (`src/p3b/is_check.py --mode stats`): per occmod seed and combined, the IS estimate of E_model at
R05–R08, its relative error from the seed spread and from the within-seed spread of the per-configuration means, the
share of the top 1 % / top 10 configurations, the effective numbers of configurations and toys, and the stored plain-toy
pass counts. `is_check.json` (`--mode combine`): the paired check on all 6,400 stored stage-B configurations — stored
IS sum, fresh IS sum (2,000 toys per configuration and rung, new seeds) and plain sum (10⁵ toys per configuration) at R07
and R08, with the plain pass counts. Diagnostic only: neither file is an input of any frozen number.
