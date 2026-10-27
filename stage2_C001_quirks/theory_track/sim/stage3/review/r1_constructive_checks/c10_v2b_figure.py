"""R1 constructive check 10: which 'expected' shift does figures/p1_v2b_revisit.png plot, and is it a near-identity?
Per cell: observed population shift Dc_pop vs (a) strat_perm_expected_Dc (r permuted within c_ev deciles: keeps the
conditional median of r), (b) scatter_expected_Dc (r re-centred in gamma* bins, random signs: the zero-median model of
the text), (c) zero_median_symmetric_scatter_Dc. Relative to median c_ev."""
import json, numpy as np
d = json.load(open('sim/stage3/results/P1.json'))
print(f"{'cell':16s} {'obs%':>6s} {'perm%':>6s} {'scat%':>6s} {'zmsym%':>7s}  paired_med_r/c_ev%")
O, A, B = [], [], []
for pt, v in d['points'].items():
    for L, b in v['by_lambda'].items():
        c = b.get('c')
        if not c or c.get('Dc_pop') is None: continue
        ce = c['median_c_ev_MG']
        o, a, s, z0 = (100 * c[k] / ce for k in ('Dc_pop', 'strat_perm_expected_Dc', 'scatter_expected_Dc', 'zero_median_symmetric_scatter_Dc'))
        O.append(o); A.append(a); B.append(s)
        print(f"{pt + '/' + L:16s} {o:6.2f} {a:6.2f} {s:6.2f} {z0:7.2f}  {100 * c['paired_median_r'] / ce:6.2f}")
O, A, B = map(np.array, (O, A, B))
print('rms(obs - perm) = %.2f %%, rms(obs - scatter) = %.2f %%, corr(obs,perm) = %.3f, corr(obs,scatter) = %.3f'
      % (np.sqrt(np.mean((O - A) ** 2)), np.sqrt(np.mean((O - B) ** 2)), np.corrcoef(O, A)[0, 1], np.corrcoef(O, B)[0, 1]))
