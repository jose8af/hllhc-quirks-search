"""S1-R3: error propagation of E2's implied Delta_s_B(Lambda)/Delta_s_B(3 keV) shift (FIX2 N2), trapezoid as in FIX2_analysis.py,
point errors = bootstrap errors of the population Delta_c(2) medians (independent), Delta_c(3 keV) = 0 (FIX2 convention) or the FU value."""
import json, os, numpy as np
TT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
N2 = json.load(open(os.path.join(TT, 'analytic', 'numerics', 'results', 'FIX2.json')))['N2']
for m, lams in ((500, (5, 7, 10, 13)), (1000, (5, 7, 10))):
    pts = [(3.0, 0.0, 0.0)] + [(l, N2[f'm{m}_L{l}']['delta_c2'][0], N2[f'm{m}_L{l}']['delta_c2'][1]) for l in lams]
    w = np.zeros(len(pts)); out = []
    for i in range(1, len(pts)):
        dl = np.log(pts[i][0] / pts[i - 1][0]); w[i - 1] += dl; w[i] += dl          # 2 * 0.5 * (d1 + d2) * dl
        val = sum(w[j] * pts[j][1] for j in range(i + 1)); err = np.sqrt(sum((w[j] * pts[j][2]) ** 2 for j in range(i + 1)))
        out.append(f"{pts[i][0]:g} keV: {100*(np.exp(val)-1):+.1f} % +- {100*err:.1f} %")
    print(f"m={m}: " + '; '.join(out))
