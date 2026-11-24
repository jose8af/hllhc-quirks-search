"""p3d_specs.py -- named specs for p3d_toys (names are shell-safe).  Gorm, 2026-11-24.

  onebin_k<kappa>_m<m>   one bin, one counted term (T1-c (i), (ii)); signal yield 1 per unit mu
  v1mode                 Phase-2 v1-mode workspace (collapsed, STR l.1727-1728), v1 best point
  v1count_p1             v1 counts, v2 treatment, selection FB2&h>5&o>5, signal of A2|F|200|1.5|BM (v1 best point)
  v1count_p2             the same workspace, signal of A2|F|500|2|BM (reading R2 of the session log)
  v1countp_p1, _p2       reading R1': v1's pile-up estimator (above its cap) at no credit = v1's direct bound, counted
  v2ph                   the v2 term structure with placeholder counts (task 3); pile-up credited (estimator)
  v2ph_nc                the same with the pile-up term at no credit (counted, m = 0, M = 96,000)
Every signal yield is a v1 placeholder efficiency x 15,775 (labelled in spec['signal']['label']).
"""
import p3d_model as pm

POINTS = {'p1': 'A2|F|200|1.5|BM', 'p2': 'A2|F|500|2|BM', 'p3': 'A2|S|500|3|BM'}


def get(name):
    if name.startswith('onebin_'):
        _, k, m = name.split('_')
        return pm.onebin(float(k[1:]), float(m[1:]))
    if name == 'v1mode':
        return pm.v1mode(POINTS['p1'])
    if name.startswith('v1count_'):
        return pm.v1count(POINTS[name.split('_')[1]])
    if name.startswith('v1countp_'):                 # reading R1' (advisor ruling 2026-11-24)
        return pm.v1count(POINTS[name.split('_')[1]], reading='R1p')
    if name == 'v2ph_nc':                            # placeholder with the pile-up term at no credit
        return pm.v2_placeholder(pu_credit=False)
    if name == 'v2ph':
        return pm.v2_placeholder()
    raise KeyError(name)
