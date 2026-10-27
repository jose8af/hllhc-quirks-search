"""R1 constructive check 8: which P2 per-point observables carry Lambda between the thickness edge (~0.5 keV) and the
merging edge (~15 keV)? d ln(obs)/d ln(Lambda) from P2_points.json at E 200/1000/1500."""
import json, numpy as np
P = json.load(open('sim/stage3/results/P2_points.json'))
obs = ['ds_all_med_um', 'sep_IT_med_um', 'lmax_med_cm', 'ntrk_med', 'dt_trk_max_med_ns', 'f_merged100', 'max_cross_med', 'hits_per_surf_med']
for sp in ('F_m200', 'F_m1000', 'F_m1500'):
    Ls = sorted({float(k.split('/L')[1]) for k in P if k.startswith(sp + '/')})
    print(sp)
    for o in obs:
        vals = [(L, P[f'{sp}/L{L:g}'][o]['value'], P[f'{sp}/L{L:g}'][o].get('err')) for L in Ls if isinstance(P[f'{sp}/L{L:g}'].get(o), dict)]
        s = '  '.join(f'{L:g}:{v:.3g}' for L, v, e in vals if L in (0.3, 0.5, 1, 2, 3, 5, 10, 20, 30))
        print(f'  {o:20s} {s}')
