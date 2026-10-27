"""R1 constructive check 3: are the P2 edges smooth in m? Fit ln(edge) = a + b ln m + c (ln m)^2 to the E masses with stat errors."""
import json, numpy as np
d = json.load(open('sim/stage3/results/P2.json'))
E = d['edges']
types = ['lower_Nosc1_closed', 'lower_lmax_RIT_closed', 'lower_ds100_hit', 'upper_lmax100um_closed', 'upper_merge100_hit', 'upper_merge25_hit']
for t in types:
    ms, y, s = [], [], []
    for k, v in E.items():
        if not k.startswith('F_'): continue
        e = v[t]
        if e['value'] is None or not np.isfinite(e['value']): continue
        ms.append(float(k[3:])); y.append(np.log(e['value'])); s.append(e['stat_err'] / e['value'])
    ms, y, s = map(np.array, (ms, y, s))
    if len(ms) < 4:
        print(t, 'n =', len(ms), 'masses', ms); continue
    for deg in (1, 2):
        X = np.vander(np.log(ms), deg + 1)
        W = 1 / s**2
        beta = np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (W * y))
        chi2 = np.sum(W * (y - X @ beta)**2); ndf = len(ms) - deg - 1
        pulls = (y - X @ beta) / s
        print(f"{t:24s} deg{deg} n={len(ms):2d} chi2/ndf={chi2:5.1f}/{ndf}  slope(dlnE/dlnm, deg1)={beta[0] if deg==1 else float('nan'):.3f}  max|pull|={np.max(np.abs(pulls)):.1f} at m={ms[np.argmax(np.abs(pulls))]:.0f}")
