"""M4_summary.py -- E2: collect the convergence / solver-independence numbers of M1-M3, M5 into results/M4.json.
Settings varied by x10: causal max_boost 1e-2 -> 1e-3 and hmax 0.2 -> 0.02 cm (together); conformal N 256 -> 1024/2048/4096;
Li Euler step 1e-3 -> 3e-4 of the printed bound.  Floors: vacuum (B = 0) thickness, vacuum miss distance, precision floor.
Run: pixi run python analytic/numerics/M4_summary.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from nm_stats import dump
J = lambda n: json.load(open(os.path.join(HERE, 'results', n)))
M1, M2, M3, M5, MC = J('M1.json'), J('M2.json'), J('M3.json'), J('M5.json'), J('M4_conformal_thickness.json')
out = dict(description=__doc__)
out['M1_prod_vs_fine'] = {k: v['convergence_prod_vs_fine'] for k, v in M1.items() if isinstance(v, dict) and 'convergence_prod_vs_fine' in v}
out['M1_fine_vs_conformal'] = {k: {N: v.get(f'conf{N}_vs_fine') for N in (256, 1024)} for k, v in M1.items() if isinstance(v, dict) and v.get('conf1024_vs_fine')}
out['M2a_solver_spread_Ahat'] = {g: {s: M2['M2a'][g][s].get('Ahat') for s in M2['M2a'][g]} for g in ('1.05', '1.3', '2', '3')}
out['M2b_solver_spread'] = {k: dict(A_odd=v.get('A_odd'), K_odd=v.get('K_odd'), psi_even=v.get('psi_even_over_eps_') or v.get('psi_even_over_eps'),
                                    b_odd=v.get('b_odd_over_eps_l0')) for k, v in M2['M2b'].items() if 'A_odd' in v}
out['M3_prod_vs_fine'] = M3['convergence']
out['M3_vacuum_floor_um'] = {k: v['vacuum_floor_um'] for k, v in M3['b_scan'].items()}
out['M3_conformal_vs_causal'] = MC
out['M5_li_step'] = M5['results_first_NCONV_events']
out['precision_floor'] = dict(b_over_l0=dict(gamma_le_1p3=3e-8, gamma_ge_2=1e-6),
                              note='both solvers; Minkowski products of near-collinear null vectors lose precision ~ (b/l)^2. '
                                   'M3 points with b_odd/l0 <~ 1e-7 (B/1000 at 1 keV, B/80 and B/1000 at 3 keV) are floor-affected.')
out['vacuum_miss_distance_cm'] = '<= 1e-12 (causal, B = 0, 30 crossings; nm_crossings test)'
dump(out, os.path.join(HERE, 'results', 'M4.json'))
print('written results/M4.json')
