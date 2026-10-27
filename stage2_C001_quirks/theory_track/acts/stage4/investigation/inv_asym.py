"""INV item 1: why the in-house asymptotic CLs is ~2.7e-4 of the toys at FB0/FB1 (read-only; imports frozen stats.py)."""
import json, sys
import numpy as np
from scipy.optimize import minimize
from acts.stage4.analysis import stats as ST

import os
TAG = os.environ.get('TAG', 'C12_v1')
L = json.load(open(f'data/acts_stage4/analysis/{TAG}/limits.json'))['points']
key = 'A2|F|200|0.45|BM'
p = L[key]; s, b, sg = p['s'], p['b'], p['sigma_ln']
print('point', key, 's', s, 'b', b, 'sig', sg)
nll, nA = ST._model(s, b, [{}, {}], sg)
n = np.asarray(b); aux = np.zeros(nA)
mu = 1e8
f = lambda a: nll(mu, a, n, aux)
r = minimize(f, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA)
print('frozen _profile at mu=1e8: alpha', r.x, 'nit', r.nit, 'msg', r.message, 'nll', r.fun, 'nll(0)', f(aux))
# same problem with the saturated (n ln n - n) constant removed -> deviance scale O(1)
const = float(np.sum(n - n * np.log(n)))
g = lambda a: f(a) - const
r2 = minimize(g, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA)
print('offset nll  at mu=1e8: alpha', r2.x, 'nit', r2.nit, 'nll', r2.fun)
q_frozen = 2 * (r.fun - f(aux) * 0 - ST._profile(nll, nA, n, aux, mu=0.0)[0])
print('q frozen', ST.qtilde_asimov(mu, s, b, [{}, {}], sg))
# fixed asymptotic: profile with offset
def q_fixed(mu):
    def prof(m):
        h = lambda a: nll(m, a, n, aux) - const
        return minimize(h, aux.copy(), method='L-BFGS-B', bounds=[(-5, 5)] * nA).fun
    return max(2 * (prof(mu) - prof(0.0)), 0.0)
from scipy.stats import norm
from scipy.optimize import brentq
def lim(qf):
    fn = lambda m: (1 - norm.cdf(np.sqrt(qf(m)))) / 0.5 - 0.05
    hi = 1.0
    while fn(hi) > 0: hi *= 4
    return brentq(fn, hi / 4, hi, rtol=1e-6)
out = {}
for k in sys.argv[1:] or list(L):
    q = L[k]
    if 'expected_asymptotic' not in q: continue
    s_, b_, sg_ = q['s'], q['b'], q['sigma_ln']
    nll, nA = ST._model(s_, b_, [{}, {}], sg_); n = np.asarray(b_); aux = np.zeros(nA)
    const = float(np.sum(n - n * np.log(np.maximum(n, 1e-300))))
    fixed = lim(q_fixed)
    toy = q['expected_toys']['median']; asy = q['expected_asymptotic']['median']
    out[k] = dict(sel=q['selections'][1], b=b_, sigma_ln=sg_, toy=toy, asym_frozen=asy, asym_offset=fixed,
                  ratio_frozen=(asy / toy if asy else None), ratio_offset=fixed / toy,
                  noprofile_1p96sqrtb_over_s=1.96 * np.sqrt(sum(bi for bi, si in zip(b_, s_) if si > 0) / max(len([x for x in s_ if x > 0]), 1)) / max(s_))
    print(k, json.dumps({kk: (round(v, 4) if isinstance(v, float) and abs(v) < 10 else v) for kk, v in out[k].items()}, default=str))
json.dump(out, open(f'data/acts_stage4/investigation/inv_asym_{TAG}.json', 'w'), indent=1, default=str)
