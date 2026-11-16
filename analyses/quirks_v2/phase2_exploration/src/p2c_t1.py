"""p2c_t1.py -- T1 workspace builder (STR §4.11 pt 1) and the toy-cost measurement against the number of parameters.

Model per selection: two counting bins c in {T, G},
    n_c ~ Pois( mu S_c prod phi^S + sum_t kappa_{t,c} lambda_t prod phi^t ),      m_t ~ Pois(lambda_t)   (auxiliary)
- counted factor: free rate lambda_t >= 0 (pyhf `normfactor`), constrained only by its auxiliary one-bin channel with
  the simulated count m_t as observation (a zero is representable, unlike `shapesys`; FEAS_C R9, STR §4.11 pt 2);
  kappa_{t,c} = N_t w_{t,c} / M_t is the transfer factor (events per unit lambda);
- constrained nuisances: `normsys` shared by name across terms, categories and the signal; a censored factor
  (probability phi0 with log width s) gets the parameter bound theta <= ln(1/phi0)/s (STR §4.11 pt 1);
- signal strength mu (`normfactor`).
Generation of pseudo-experiments (the hybrid convention of STR §4.11 pt 2): lambda_t ~ Gamma(m_t + 1), every
constrained nuisance from its constraint (censored at its bound), n_T and n_G from the model; the auxiliary
observations stay at m_t.  Test statistic q~_mu from two pyhf fits.

  <pyhf python> p2c_t1.py time <out.json> <n_terms> <n_nuis> <n_toys> [seed]      synthetic sizes, timing only
"""
import json
import os
import sys
import time

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import logging  # noqa: E402
import resource  # noqa: E402

import numpy as np  # noqa: E402
import pyhf  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p2c_t1')
CATS = ('SR_T', 'SR_G')


def build(terms, nuis, signal):
    """terms: [{name, kappa: {cat: float}, m: int, nuis: {name: log_width}}]
    nuis: {name: {'bound': theta_max or None}}; signal: {'yield': {cat: S}, 'nuis': {name: log_width}}.
    Returns (workspace, model, info)."""
    def normsys(ws):
        return [{'name': n, 'type': 'normsys', 'data': {'hi': float(np.exp(w)), 'lo': float(np.exp(-w))}}
                for n, w in ws.items()]
    channels = []; obs = []
    for c in CATS:
        samples = [{'name': 'signal', 'data': [float(signal['yield'][c])],
                    'modifiers': [{'name': 'mu', 'type': 'normfactor', 'data': None}] + normsys(signal['nuis'])}]
        for t in terms:
            if t['kappa'].get(c, 0.0) <= 0:
                continue
            samples.append({'name': t['name'], 'data': [float(t['kappa'][c])],
                            'modifiers': [{'name': 'lam_' + t['name'], 'type': 'normfactor', 'data': None}]
                            + normsys(t['nuis'])})
        channels.append({'name': c, 'samples': samples}); obs.append({'name': c, 'data': [0.0]})
    for t in terms:
        channels.append({'name': 'aux_' + t['name'],
                         'samples': [{'name': 'count', 'data': [1.0],
                                      'modifiers': [{'name': 'lam_' + t['name'], 'type': 'normfactor', 'data': None}]}]})
        obs.append({'name': 'aux_' + t['name'], 'data': [float(t['m'])]})
    pars = [{'name': 'mu', 'bounds': [[0.0, 1.0e3]], 'inits': [1.0]}]
    for t in terms:
        pars.append({'name': 'lam_' + t['name'], 'bounds': [[1e-9, 10.0 * (t['m'] + 5.0)]], 'inits': [t['m'] + 1.0]})
    for n, d in nuis.items():
        if d.get('bound') is not None:
            pars.append({'name': n, 'bounds': [[-5.0, float(d['bound'])]], 'inits': [0.0]})
    spec = {'version': '1.0.0', 'channels': channels, 'observations': obs,
            'measurements': [{'name': 'qv2', 'config': {'poi': 'mu', 'parameters': pars}}]}
    ws = pyhf.Workspace(spec)
    model = ws.model()
    return ws, model, dict(n_par=model.config.npars, n_terms=len(terms), n_nuis=len(nuis))


def generate(model, terms, nuis, mu, rng):
    """One pseudo-experiment of the hybrid convention: returns the full data vector (main + auxiliary data)."""
    cfg = model.config
    pars = np.array(cfg.suggested_init(), float)
    pars[cfg.poi_index] = mu
    for t in terms:
        pars[cfg.par_slice('lam_' + t['name'])] = rng.gamma(t['m'] + 1.0)
    for n, d in nuis.items():
        th = rng.normal()
        if d.get('bound') is not None:
            th = min(th, d['bound'])
        pars[cfg.par_slice(n)] = th
    exp = np.asarray(model.expected_actualdata(pars))
    data = exp.copy()
    order = cfg.channels
    for c in CATS:
        i = order.index(c)
        data[i] = rng.poisson(exp[i])
    for t in terms:                       # auxiliary observations stay at the simulated counts
        data[order.index('aux_' + t['name'])] = t['m']
    return np.concatenate([data, np.asarray(cfg.auxdata)])


def qtilde(model, data, mu):
    init = model.config.suggested_init(); bounds = model.config.suggested_bounds(); fixed = model.config.suggested_fixed()
    return float(pyhf.infer.test_statistics.qmu_tilde(mu, data, model, init, bounds, fixed))


def synthetic(n_terms, n_nuis, seed):
    """Sizes only (no study number): counts in {0, 0, 1, 1, 2, 3, 5, 8}, transfer factors 0.01-0.3 (as FEAS_C R9)."""
    rng = np.random.default_rng(seed)
    names = [f'nu{j}' for j in range(n_nuis)]
    nuis = {n: {'bound': (1.5 if j % 4 == 3 else None)} for j, n in enumerate(names)}
    terms = []
    for t in range(n_terms):
        own = {names[j]: float(rng.uniform(0.02, 0.4)) for j in range(n_nuis) if j < 2 or (t + j) % 3 == 0}
        terms.append(dict(name=f't{t}', m=int(rng.choice([0, 0, 1, 1, 2, 3, 5, 8])),
                          kappa={c: float(rng.uniform(0.01, 0.3)) for c in CATS}, nuis=own))
    signal = {'yield': {'SR_T': 1.5, 'SR_G': 1.5}, 'nuis': {names[0]: 0.02, names[1]: 0.05}}
    return terms, nuis, signal


def main(argv):
    mode, out = argv[0], argv[1]
    if mode != 'time':
        raise SystemExit('modes: time')
    n_terms, n_nuis, n_toys = int(argv[2]), int(argv[3]), int(argv[4])
    seed = int(argv[5]) if len(argv) > 5 else 20261116
    pyhf.set_backend('numpy', 'scipy')
    terms, nuis, signal = synthetic(n_terms, n_nuis, seed)
    ws, model, info = build(terms, nuis, signal)
    rng = np.random.default_rng(seed + 1)
    mu_test = 3.0
    res = dict(info, n_toys=n_toys, mu_test=mu_test, pyhf=pyhf.__version__, numpy=np.__version__)
    for label, mu_gen in (('sb', mu_test), ('b', 0.0)):
        c0 = time.process_time(); q = []; nfail = 0
        for _ in range(n_toys):
            d = generate(model, terms, nuis, mu_gen, rng)
            try:
                q.append(qtilde(model, d, mu_test))
            except Exception:  # noqa: BLE001 - a failed fit is counted, not hidden
                nfail += 1
        cpu = time.process_time() - c0
        res[label] = dict(cpu_s=round(cpu, 3), cpu_s_per_toy=cpu / n_toys, n_fail=nfail,
                          q_median=float(np.median(q)) if q else None)
        log.info('%s: %d toys, %.3f s per toy (two fits), %d failed fits', label, n_toys, cpu / n_toys, nfail)
    res['cpu_s_per_1000_sb_plus_1000_b'] = 1000.0 * (res['sb']['cpu_s_per_toy'] + res['b']['cpu_s_per_toy'])
    res['max_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f, indent=1)
    os.replace(out + '.tmp', out)
    log.info('n_par %d: %.0f s per 1000 + 1000 toys at one mu', info['n_par'], res['cpu_s_per_1000_sb_plus_1000_b'])


if __name__ == '__main__':
    main(sys.argv[1:])
