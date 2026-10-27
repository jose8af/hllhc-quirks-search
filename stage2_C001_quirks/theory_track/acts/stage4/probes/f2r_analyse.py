"""f2r_analyse.py -- Stage-4 plan FIXER R2: summarise data/acts_stage4/fix_r2/f2r_profile_t*_o*.json.
(1) time per stage (median over trials, and share of the original-code estimate) per density;
(2) PU-only core-width / core-chi2 diagnostics (review R2 B-1): per trial, the minimum plain and trimmed core width over
    candidates with N_IT2 >= 3 and N_L2 >= L (L = 8, 9, 10), and quantiles of chi2/ndf (all in-band hits) vs core-hit
    chi2/ndf.  No signal is read.
Output: data/acts_stage4/fix_r2/f2r_profile_summary.json
"""
import glob
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
OUT = TT / 'data' / 'acts_stage4' / 'fix_r2'
q = lambda a, p=(10, 50, 90): [round(float(x), 3) for x in np.percentile(a, p)] if len(a) else None
res = {}
for mode in (2, 1):
    files = sorted(glob.glob(str(OUT / f'f2r_profile_t{mode}_o*.json')))
    trials = [t for f in files for t in json.loads(Path(f).read_text())['trials']]
    if not trials:
        continue
    st = {k: [t['times_s'][k] for t in trials] for k in trials[0]['times_s']}
    tot = [t['total_original_est_s'] for t in trials]
    fixed = [t['times_s']['road'] + t['times_s']['seeds'] + t['times_s']['refitnb'] + t['times_s']['dedup_vectorised']
             + t['times_s']['refitnp_est'] for t in trials]
    d = dict(n_trials=len(trials),
             label={2: 'TDR-OT (OT topped up; fix-R1 48 s/trial density)', 1: 'TDR-normalised IT + OT (adopted baseline)'}[mode],
             n_road_hits=q([t['n_road'] for t in trials]), n_L4_L3_L2=[q([t[k] for t in trials]) for k in ('n_A', 'n_B', 'n_C')],
             n_refit=q([t['n_refit'] for t in trials]), n_fast=q([t['n_fast'] for t in trials]),
             n_kept=q([t['n_kept'] for t in trials]), n_distinct_hitsets=q([t['n_distinct_hitsets'] for t in trials]),
             stage_s_median={k: round(float(np.median(v)), 2) for k, v in st.items()},
             original_total_est_s=q(tot),
             share_of_original_median={k: round(float(np.median(np.array(v) / np.array(tot))), 3) for k, v in st.items()
                                       if k in ('seeds', 'refitnb', 'dedup_python_est', 'refitnp_est')},
             with_vectorised_dedup_s=q(fixed),
             per_cmp_python_us=q([t['per_cmp_python_us'] for t in trials]),
             refitnp_ms_each=q([t['refitnp_ms_each'] for t in trials]),
             thin_ms_rho1=q([t['thin_ms_rho1_median'] for t in trials if t['thin_ms_rho1_median']]),
             thin_ms_rho2=q([t['thin_ms_rho2_median'] for t in trials if t['thin_ms_rho2_median']]))
    core = {}
    for L in (8, 9, 10):
        mins_p, mins_t, chi_all, chi_core, ncore, nint, chi1, ncore1, ninb, wall = [], [], [], [], [], [], [], [], [], []
        for t in trials:
            cs = [c for c in t['cores_L8'] if c['nl2'] >= L]
            if not cs:
                continue
            mins_p.append(min(c['w_plain'] for c in cs)); mins_t.append(min(c['w_trim'] for c in cs))
            wall += [c['w_plain'] for c in cs]
            chi_all += [c['chi2ndf'] for c in cs]; chi_core += [c['chi2_core'] for c in cs if c['chi2_core'] == c['chi2_core']]
            ncore += [c['n_core'] for c in cs]; nint += [c['n_int'] for c in cs]
            chi1 += [c['chi2_core1'] for c in cs if c.get('chi2_core1', float('nan')) == c.get('chi2_core1', float('nan'))]
            ncore1 += [c['n_core1'] for c in cs if 'n_core1' in c]; ninb += [c['n_inband'] for c in cs if 'n_inband' in c]
        core[f'NL2_ge{L}'] = dict(n_trials_with_cand=len(mins_p), n_cands=len(wall),
                                  min_w_plain_per_trial_mm=[round(x, 1) for x in sorted(mins_p)],
                                  w_plain_all_cands_q_mm=q(wall),
                                  min_w_trim_per_trial_mm=[round(x, 1) for x in sorted(mins_t)],
                                  chi2ndf_all_q=q(chi_all), chi2ndf_core_trim_q=q(chi_core), n_core_trim_hits_q=q(ncore),
                                  chi2ndf_core_onestep_q=q(chi1), n_core_onestep_q=q(ncore1), n_inband_q=q(ninb),
                                  n_interactions_q=q(nint),
                                  trials_with_cand_below_mm={str(W): sum(1 for t in trials if any(c['nl2'] >= L and c['w_plain'] < W for c in t['cores_L8'])) for W in (37.5, 18.75, 9.4, 4.7)},
                                  cands_below_mm={str(W): int(sum(1 for x in wall if x < W)) for W in (37.5, 18.75, 9.4, 4.7)})
    d['pu_core_diagnostics'] = core
    res[f't{mode}'] = d
(OUT / 'f2r_profile_summary.json').write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
