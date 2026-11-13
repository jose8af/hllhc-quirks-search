"""f2r_cost.py -- Stage-4 plan FIXER R2 (review R2 B-5): compute cost as a function of the finder time per trial at the
TDR-normalised density, plus B2 at its own rho = 2 time.  Pure arithmetic on the plan §6.2 inputs (ESTIMATE) and on the
stored fix-R1 / fix-R2 timings; no finder run.

Recommended scope (plan §6.2): non-finder base = 330 CPU-h (the fix-R1 total at 2 s/trial and 16 s per rho = 2 trial)
minus the finder share.  Finder trials: A2 61 344 + A3 9 000 + A4 12 000 + A5 4 000 + B1 80 000 + C 25 000 = 191 344 rho = 1
trials; B2 = 5 000 events x 2 roads = 10 000 rho = 2 trials (+ PU simulation 2 x 4.7 s per event, already in the base).
Optional rho = 3: 2 000 events x (3 x 4.7 s + t3).
Lean scope (§6.2 'lean' column): ~97 000 rho = 1 trials and 5 000 rho = 2 trials, base fitted the same way to 160 CPU-h.

It also estimates the share of the measured fix-R1 rho = 2 time (Fatras density, 8 trials) that is the O(N_fast x N_kept)
Python duplicate-merge loop, from the stored counts (n_refit ~ N_fast upper bound, len(cands) ~ N_kept) and the per-
comparison cost measured by f2r_profile.py.
Rows with t2 = 8 t1 use the R0 rho^3 assumption (ESTIMATE); t1 = 211 s is the measured median at the full normalised
density with the duplicate merge vectorised (f2r_profile_summary.json -> t1); no rho = 2 time at that density is measured.
Output: data/acts_stage4/fix_r2/f2r_cost.json
"""
import glob
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
OUT = TT / 'data' / 'acts_stage4' / 'fix_r2'
N1_REC, N2_REC = 191344, 10000
N1_LEAN, N2_LEAN = 97000, 5000
BASE_REC = 330.0 - N1_REC * 2 / 3600 - N2_REC * 16 / 3600
BASE_LEAN = 160.0 - N1_LEAN * 2 / 3600 - N2_LEAN * 16 / 3600


def total(base, n1, n2, t1, t2):
    return base + n1 * t1 / 3600 + n2 * t2 / 3600


rows = []
for t1, t2 in [(2, 16), (2, 50), (4, 32), (4, 100), (5, 40), (5, 200), (10, 80), (10, 500), (12, 1000), (20, 160), (48, 1000), (211, 1688)]:
    rows.append(dict(t1_s=t1, t2_s=t2, rec_cpu_h=round(total(BASE_REC, N1_REC, N2_REC, t1, t2)),
                     lean_cpu_h=round(total(BASE_LEAN, N1_LEAN, N2_LEAN, t1, t2)),
                     rec_wall_h_7w=round(total(BASE_REC, N1_REC, N2_REC, t1, t2) / 7)))
# G3 pilot cost: 2 000 B1 events x (4.7 + 4 t1) + 500 rho = 2 events x (2 x 4.7 + 2 t2)
pilot = [dict(t1_s=t1, t2_s=t2, pilot_cpu_h=round((2000 * (4.7 + 4 * t1) + 500 * (9.4 + 2 * t2)) / 3600, 1))
         for t1, t2 in [(2, 16), (4, 20), (12, 100), (48, 1000)]]
# B2 budget -> rho = 2 gate value: B2 (rec) = 5 000 x (9.4 + 2 t2) s <= budget
b2_gate = {f'{b}_cpuh': round((b * 3600 / 5000 - 9.4) / 2, 1) for b in (58, 70, 100)}

# dedup share of the stored rho = 2 trials
prof = [json.loads(Path(f).read_text()) for f in sorted(glob.glob(str(OUT / 'f2r_profile_t*_o*.json')))]
per_cmp = [t['per_cmp_python_us'] for p in prof for t in p['trials'] if t['per_cmp_python_us'] > 0]
pc = float(np.median(per_cmp)) * 1e-6 if per_cmp else 1e-6
thin_ms = [t['thin_ms_rho2_median'] for p in prof for t in p['trials'] if t.get('thin_ms_rho2_median')]
tw = float(np.median(thin_ms)) * 1e-3 if thin_ms else 0.012
r2 = []
for f in sorted(glob.glob(str(TT / 'data/acts_stage4/fix_r1/finder/pu2_t0_s6_tol30_j*.jsonl'))):
    for line in open(f):
        if line.strip():
            r = json.loads(line)
            nf, nk = r['n_refit'], len(r['cands'])
            nth = sum(1 for c in r['cands'] if 'thin' in c)
            r2.append(dict(t_tot=r['t_tot'], t_seed=r['t_seed'], n_refit=nf, n_kept_ge4=nk, n_thin=nth,
                           dedup_est_s=round(pc * nf * nk / 2, 1), thin_est_s=round(tw * nth, 1)))
share = [x['dedup_est_s'] / x['t_tot'] for x in r2]
share_thin = [x['thin_est_s'] / x['t_tot'] for x in r2]
res = dict(base_rec_cpu_h=round(BASE_REC, 1), base_lean_cpu_h=round(BASE_LEAN, 1),
           cpu_h_per_s_rho1_rec=round(N1_REC / 3600, 1), cpu_h_per_s_rho2_rec=round(N2_REC / 3600, 2),
           table=rows, g3_pilot=pilot, b2_gate_t2_s_for_budget=b2_gate,
           per_cmp_python_us_median=pc * 1e6, thin_ms_per_candidate=tw * 1e3,
           rho2_fatras_stored=dict(trials=r2, dedup_share_median=round(float(np.median(share)), 2) if share else None,
                                   thin_share_median=round(float(np.median(share_thin)), 2) if share_thin else None,
                                   note='estimate: N_fast ~ n_refit (upper), N_kept ~ len(cands) (lower); comparisons ~ N_fast*N_kept/2'))
(OUT / 'f2r_cost.json').write_text(json.dumps(res, indent=1))
print(json.dumps({k: v for k, v in res.items() if k != 'rho2_fatras_stored'}, indent=1))
print('rho2 dedup / thin share median', res['rho2_fatras_stored']['dedup_share_median'], res['rho2_fatras_stored']['thin_share_median'])
for x in r2:
    print(x)
