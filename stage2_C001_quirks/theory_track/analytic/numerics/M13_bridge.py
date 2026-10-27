"""M13_bridge.py -- E2: does the measured per-crossing axis-rotation law (M1, in-tracker crossings) account for the measured
thickness response (M3)?  Purely numerical bookkeeping of measured quantities (no analytic input from E1).

From M1 (results/M1.json): psi_pair(Lambda) = median psi_odd/eps + median psi_even/eps (fine settings, converged), the
out-of-plane-relevant axis rotation per crossing pair in units of eps_perp, and the median eps_perp of the odd crossings.
Fit psi_pair = a ln(1/eps) + b over Lambda = 0.6-5 keV (per mass).  If the thickness is proportional to the accumulated
axis rotation, Delta_s ~ l * N_pairs * eps * psi_pair, with eps ~ B/Lambda^2, l ~ Lambda^-2, N ~ Lambda^2, then
  response per unit B   R(k) = psi_pair(eps/k)/psi_pair(eps) = 1 + c ln k,  c = a / psi_pair(eps)
  local B exponent      d ln Delta_s / d ln B = 1 - c
  local Lambda exponent d ln Delta_s / d ln Lambda = -2 + 2c
Compared with M3: c_k = (R_ev(1/k) - 1)/ln k (k = 2..20/80 within the precision floor) and the measured exponents.
Run: pixi run python analytic/numerics/M13_bridge.py
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nm_stats import dump

M1 = json.load(open(os.path.join(HERE, 'results', 'M1.json')))
M3 = json.load(open(os.path.join(HERE, 'results', 'M3.json')))
out = {}
for m in (200.0, 500.0, 1000.0):
    lams = [0.6, 1.0, 2.0, 3.0, 5.0]
    eps = np.array([M1[f'm{m:g}_L{l:g}']['eps'][0] for l in lams])
    pp = np.array([M1[f'm{m:g}_L{l:g}']['psi_odd_fine'][0] + M1[f'm{m:g}_L{l:g}']['psi_even_fine'][0] for l in lams])
    pe = np.array([np.hypot(M1[f'm{m:g}_L{l:g}']['psi_odd_fine'][1], M1[f'm{m:g}_L{l:g}']['psi_even_fine'][1]) for l in lams])
    x = np.log(1 / eps)
    w = 1 / pe ** 2
    A = np.vstack([x, np.ones_like(x)]).T
    cov = np.linalg.inv(A.T @ (A * w[:, None]))
    a, b = cov @ (A.T @ (w * pp))
    ea = np.sqrt(cov[0, 0])
    ent = dict(Lambda=lams, eps_median=eps, psi_pair=pp, psi_pair_err=pe, fit_a=a, fit_a_err=ea, fit_b=b,
               chi2=float(np.sum(w * (pp - (a * x + b)) ** 2)), ndf=len(lams) - 2)
    ent['c_pred'] = {f'{l:g}': a / (a * xi + b) for l, xi in zip(lams, x)}
    ent['c_pred_err'] = {f'{l:g}': ea / (a * xi + b) for l, xi in zip(lams, x)}
    ent['B_exponent_pred'] = {f'{l:g}': 1 - a / (a * xi + b) for l, xi in zip(lams, x)}
    ent['Lambda_exponent_pred'] = {f'{l:g}': -2 + 2 * a / (a * xi + b) for l, xi in zip(lams, x)}
    meas = {}
    for l in (1.0, 3.0):
        key = f'm{m:g}_L{l:g}'
        if key in M3['b_scan']:
            ck = M3['b_scan'][key]['c_k_prod']
            kmax = 80 if l == 1.0 else 20       # within the precision floor (b_odd/l0 >~ 1e-7)
            meas[f'{l:g}'] = dict(c_k={k: v for k, v in ck.items() if float(k) <= kmax},
                                  c_mean=float(np.mean([v for k, v in ck.items() if float(k) <= kmax])),
                                  B_exponent_global=M3['b_scan'][key]['power_law_1/80_to_2']['exponent'])
    ent['M3_measured'] = meas
    ent['M3_Lambda_exponents'] = M3['lambda_scan'][f'm{m:g}_exponents']
    out[f'm{m:g}'] = ent
    print(f"m={m:.0f}: psi_pair = {a:.3f}±{ea:.3f} ln(1/eps) + {b:.3f} (chi2/ndf {ent['chi2']:.1f}/{ent['ndf']}); "
          + ' '.join(f"L={l}: eps={e:.2e} psi_pair={p:.2f}±{q:.2f}" for l, e, p, q in zip(lams, eps, pp, pe)))
    print('   c_pred: ' + ' '.join(f"{l}: {ent['c_pred'][l]:.3f}±{ent['c_pred_err'][l]:.3f}" for l in ent['c_pred'])
          + ' | measured c (M3): ' + ' '.join(f"{l}: {v['c_mean']:.3f} {v['c_k']}" for l, v in meas.items()))
    print('   Lambda exponent pred: ' + ' '.join(f"{l}: {v:.3f}" for l, v in ent['Lambda_exponent_pred'].items())
          + ' | measured: ' + ' '.join(f"{k}: {v['exponent']:.2f}±{v['err']:.2f}" for k, v in ent['M3_Lambda_exponents'].items()))
out['description'] = __doc__
dump(out, os.path.join(HERE, 'results', 'M13_bridge.json'))
