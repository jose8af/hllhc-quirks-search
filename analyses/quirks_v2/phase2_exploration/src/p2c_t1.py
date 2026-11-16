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
  <pyhf python> p2c_t1.py v1 <out.json> [n_toys]                                  COM T1-b: v1 best point, v1 treatment
"""
import json
import os
import sys
import time

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import logging  # noqa: E402
from pathlib import Path  # noqa: E402
import resource  # noqa: E402

import numpy as np  # noqa: E402
import pyhf  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p2c_t1')
CATS = ('SR_T', 'SR_G')


def build(terms, nuis, signal, fixed=(), mu_max=1.0e3):
    """terms: [{name, kappa: {cat: float}, m: int, nuis: {name: log_width}}]
    nuis: {name: {'bound': theta_max or None}}; signal: {'yield': {cat: S}, 'nuis': {name: log_width}}.
    fixed: [{name, yield: {cat: B}, nuis: {name: log_width}}] background samples with a nominal yield and log-normal
    nuisances only (v1 mode: one log-normal background per category).  normsys uses the pure exponential
    interpolation (code1), i.e. a log-normal factor exp(width * theta), as STR §4.11 pt 1 and v1's `_model`.
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
        for fb in fixed:
            if fb['yield'].get(c, 0.0) > 0:
                samples.append({'name': fb['name'], 'data': [float(fb['yield'][c])], 'modifiers': normsys(fb['nuis'])})
        channels.append({'name': c, 'samples': samples}); obs.append({'name': c, 'data': [0.0]})
    for t in terms:
        channels.append({'name': 'aux_' + t['name'],
                         'samples': [{'name': 'count', 'data': [1.0],
                                      'modifiers': [{'name': 'lam_' + t['name'], 'type': 'normfactor', 'data': None}]}]})
        obs.append({'name': 'aux_' + t['name'], 'data': [float(t['m'])]})
    pars = [{'name': 'mu', 'bounds': [[0.0, float(mu_max)]], 'inits': [1.0]}]
    for t in terms:
        pars.append({'name': 'lam_' + t['name'], 'bounds': [[1e-9, 10.0 * (t['m'] + 5.0)]], 'inits': [t['m'] + 1.0]})
    for n, d in nuis.items():
        if d.get('bound') is not None:
            pars.append({'name': n, 'bounds': [[-5.0, float(d['bound'])]], 'inits': [0.0]})
    spec = {'version': '1.0.0', 'channels': channels, 'observations': obs,
            'measurements': [{'name': 'qv2', 'config': {'poi': 'mu', 'parameters': pars}}]}
    ws = pyhf.Workspace(spec)
    model = ws.model(modifier_settings={'normsys': {'interpcode': 'code1'}})
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


AN1 = Path(__file__).resolve().parents[4] / 'stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1'
V1_POINT = 'A2|F|200|1.5|BM'
V1_NORM = 15775.0            # events before selection per unit mu (STR §4.11 T1-b: mu95 = 1.2458e7 / 15,775 = 789.7)


def v1_mode(out, ntoys, seed=20261116):
    """T1-b: the v1 best point with v1's treatment (one log-normal background per category, uncorrelated), limit by
    the T1 procedure (hybrid generation, q~_mu from two pyhf fits, CLs at the median of the b-only ensemble)."""
    lim = json.loads((AN1 / 'limits.json').read_text())['points'][V1_POINT]
    eff, b, sg = lim['s'], lim['b'], lim['sigma_ln']
    fixed = [{'name': f'bkg_{c}', 'yield': {c: b[i]}, 'nuis': {f'bkg_own_{c}': sg[i]}} for i, c in enumerate(CATS)]
    nuis = {f'bkg_own_{c}': {'bound': None} for c in CATS}
    signal = {'yield': {c: eff[i] * V1_NORM for i, c in enumerate(CATS)}, 'nuis': {}}
    # first attempt (p2-c-t1-v1, scipy SLSQP): fits failed at counts of 5e5 with a nuisance of log width 2.7 (assert
    # result.success; CLs not monotone, spurious asymptotic root at 435.6).  Minuit is used for the v1 mode.
    opt = sys.argv[4] if len(sys.argv) > 4 else 'minuit'
    pyhf.set_backend('numpy', pyhf.optimize.minuit_optimizer(tolerance=1e-3) if opt == 'minuit' else 'scipy')
    ws, model, info = build([], nuis, signal, fixed=fixed, mu_max=1.0e5)
    cfg = model.config
    asimov = np.asarray(model.expected_data(np.asarray(cfg.suggested_init()) * 0 + [0.0 if i == cfg.poi_index else 0.0
                                                                                   for i in range(cfg.npars)]))

    def cls_asym(mu):
        r = pyhf.infer.hypotest(mu, asimov, model, test_stat='qtilde', return_expected=True)
        return float(r[1])
    scan = [(m, cls_asym(m)) for m in np.geomspace(100.0, 3000.0, 35)]
    mono = all(a[1] >= c[1] - 1e-6 for a, c in zip(scan[:-1], scan[1:]))
    mu_a = None
    for a, c in zip(scan[:-1], scan[1:]):
        if a[1] >= 0.05 > c[1]:
            mu_a = float(a[0] + (a[1] - 0.05) * (c[0] - a[0]) / (a[1] - c[1]))
            break
    log.info('asymptotic scan monotone: %s; mu_a %s', mono, mu_a)
    if mu_a is None:
        mu_a = float(b[1] / signal['yield'][CATS[1]])
    rng = np.random.default_rng(seed)
    grid = [mu_a * x for x in (0.8, 0.9, 0.95, 1.0, 1.05, 1.15)]
    t0 = time.process_time(); pts = []; nfail = 0
    order = cfg.channels

    def toys(mu_gen, mu_test):
        nonlocal nfail
        q = []
        for _ in range(ntoys):
            d = generate(model, [], nuis, mu_gen, rng)
            try:
                q.append(qtilde(model, d, mu_test))
            except Exception:  # noqa: BLE001
                nfail += 1
        return np.array(q)
    for mu in grid:
        qb = toys(0.0, mu); qs = toys(mu, mu)
        qmed = np.median(qb)
        clsb = float(np.mean(qs >= qmed)); clb = float(np.mean(qb >= qmed))
        pts.append(dict(mu=mu, cls=clsb / max(clb, 1e-12), clsb=clsb, clb=clb, q_median_b=float(qmed)))
        log.info('mu %.1f: CLs %.4f (CLsb %.4f, CLb %.4f)', mu, pts[-1]['cls'], clsb, clb)
    mu95 = None
    for a, c in zip(pts[:-1], pts[1:]):
        if a['cls'] > 0 and c['cls'] > 0 and (a['cls'] - 0.05) * (c['cls'] - 0.05) <= 0:
            la, lc = np.log(a['cls']), np.log(c['cls'])
            mu95 = float(a['mu'] + (np.log(0.05) - la) * (c['mu'] - a['mu']) / (lc - la))
    v1 = lim['expected_toys']['median'] / V1_NORM
    res = dict(point=V1_POINT, inputs=dict(eff=eff, b=b, sigma_ln=sg, norm=V1_NORM), n_par=info['n_par'], order=order,
               mu95_v1_toys=v1, mu95_v1_asymptotic=lim['expected_asymptotic']['median'] / V1_NORM, mu95_asymptotic_pyhf=mu_a,
               asymptotic_scan=scan, asymptotic_scan_monotone=mono, optimizer=opt,
               ntoys_per_ensemble=ntoys, grid=pts, mu95_toys_T1=mu95, ratio_to_v1=(mu95 / v1 if mu95 else None),
               within_10_percent=(abs(mu95 / v1 - 1) <= 0.10 if mu95 else None), n_failed_fits=nfail,
               cpu_s=time.process_time() - t0, schema_valid=True, pyhf=pyhf.__version__)
    pyhf.schema.validate(ws, 'workspace.json')
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f, indent=1)
    os.replace(out + '.tmp', out)
    log.info('T1-b: mu95 (T1 toys) %s, pyhf asymptotic %.1f, v1 toys %.1f, v1 asymptotic %.1f', mu95, mu_a, v1,
             res['mu95_v1_asymptotic'])


def _v1_setup(tol=1e-4):
    lim = json.loads((AN1 / 'limits.json').read_text())['points'][V1_POINT]
    eff, b, sg = lim['s'], lim['b'], lim['sigma_ln']
    fixed = [{'name': f'bkg_{c}', 'yield': {c: b[i]}, 'nuis': {f'bkg_own_{c}': sg[i]}} for i, c in enumerate(CATS)]
    nuis = {f'bkg_own_{c}': {'bound': None} for c in CATS}
    signal = {'yield': {c: eff[i] * V1_NORM for i, c in enumerate(CATS)}, 'nuis': {}}
    pyhf.set_backend('numpy', pyhf.optimize.minuit_optimizer(tolerance=tol, strategy=2))
    ws, model, info = build([], nuis, signal, fixed=fixed, mu_max=1.0e5)
    return lim, nuis, signal, model


def v1_point(out, mu, ntoys, seed):
    """One mu of the refined T1-b run: b-only and s+b ensembles, failed-fit rule of the session log (retry once from
    the generated nuisance values, then drop; dropped fraction reported)."""
    lim, nuis, signal, model = _v1_setup()
    cfg = model.config
    rng = np.random.default_rng(seed)
    t0 = time.process_time()

    def gen(mu_gen):
        pars = np.array(cfg.suggested_init(), float); pars[cfg.poi_index] = mu_gen
        th = {}
        for n in nuis:
            th[n] = rng.normal(); pars[cfg.par_slice(n)] = th[n]
        exp = np.asarray(model.expected_actualdata(pars))
        return np.concatenate([rng.poisson(exp), np.asarray(cfg.auxdata)]), th

    def q_of(d, th):
        init = cfg.suggested_init(); bounds = cfg.suggested_bounds(); fixed_ = cfg.suggested_fixed()
        try:
            return float(pyhf.infer.test_statistics.qmu_tilde(mu, d, model, init, bounds, fixed_)), 0
        except Exception:  # noqa: BLE001
            for n, v in th.items():
                init[cfg.par_slice(n).start] = float(np.clip(v, -4.9, 4.9))
            try:
                return float(pyhf.infer.test_statistics.qmu_tilde(mu, d, model, init, bounds, fixed_)), 1
            except Exception:  # noqa: BLE001
                return None, 2
    res = dict(mu=mu, ntoys=ntoys, seed=seed)
    for lab, mg in (('b', 0.0), ('sb', mu)):
        q = []; retried = dropped = 0
        for _ in range(ntoys):
            d, th = gen(mg)
            v, st = q_of(d, th)
            retried += st == 1; dropped += st == 2
            if v is not None:
                q.append(v)
        res[lab] = dict(q=q, retried=int(retried), dropped=int(dropped))
    res['cpu_s'] = time.process_time() - t0
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f)
    os.replace(out + '.tmp', out)
    log.info('mu %.1f: dropped b %d sb %d of %d; retried %d %d', mu, res['b']['dropped'], res['sb']['dropped'], ntoys,
             res['b']['retried'], res['sb']['retried'])


def limit_numbercount(s, b, sig, ntoys, seed, cl=0.95):
    """DIAGNOSTIC ONLY (no verdict): v1's statistic, the weighted number count Q = sum_c n_c ln(1 + mu s_c / b_c) with the
    nuisances marginalised (hybrid CLs), as acts/stage4/analysis/stats.py l.216-258, re-implemented with its own seed."""
    rng = np.random.default_rng(seed)
    s = np.asarray(s, float); b = np.asarray(b, float)
    bt = b[None, :] * np.exp(np.asarray(sig)[None, :] * rng.standard_normal((ntoys, len(b))))
    nb_obs = rng.poisson(bt); nb = rng.poisson(bt)

    def cls(mu):
        w = np.log1p(mu * s / b)
        nsb = np.random.default_rng([seed, 1]).poisson(bt + mu * s[None, :])
        qobs = float(np.quantile((nb_obs * w).sum(1), 0.5))
        return np.mean((nsb * w).sum(1) <= qobs) / max(np.mean((nb * w).sum(1) <= qobs), 1e-12)
    lo, hi = 0.0, 1.0
    while cls(hi) > 1 - cl and hi < 1e12:
        hi *= 4
    lo = hi / 4
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if cls(mid) > 1 - cl else (lo, mid)
    return float(hi)


def v1_diag(out):
    lim, nuis, signal, model = _v1_setup()
    cfg = model.config
    asimov = np.asarray(model.expected_data(np.zeros(cfg.npars)))
    scan = []
    for m in np.arange(780.0, 900.1, 4.0):
        try:
            scan.append((float(m), float(pyhf.infer.hypotest(m, asimov, model, test_stat='qtilde', return_expected=True)[1])))
        except Exception:  # noqa: BLE001
            scan.append((float(m), None))
    ok = [x for x in scan if x[1] is not None]
    mu_a = None
    for a, c in zip(ok[:-1], ok[1:]):
        if a[1] >= 0.05 > c[1]:
            mu_a = float(a[0] + (a[1] - 0.05) * (c[0] - a[0]) / (a[1] - c[1]))
            break
    s = [signal['yield'][c] for c in CATS]
    nc = [limit_numbercount(s, lim['b'], lim['sigma_ln'], 5000, sd) for sd in (20261116, 20261117, 20261118, 20261014)]
    res = dict(asymptotic_scan=scan, mu95_asymptotic_pyhf_fine=mu_a, mu95_v1_asymptotic=lim['expected_asymptotic']['median'] / V1_NORM,
               mu95_v1_toys=lim['expected_toys']['median'] / V1_NORM, diagnostic_v1_statistic_mu95=nc,
               diagnostic_seeds=[20261116, 20261117, 20261118, 20261014], b_over_s=lim['b'][1] / s[1])
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f, indent=1)
    os.replace(out + '.tmp', out)
    log.info('fine asymptotic %s (v1 %.1f); v1-statistic diagnostic %s (v1 %.1f)', mu_a, res['mu95_v1_asymptotic'], nc,
             res['mu95_v1_toys'])


def main(argv):
    mode, out = argv[0], argv[1]
    if mode == 'v1pt':
        return v1_point(out, float(argv[2]), int(argv[3]), int(argv[4]))
    if mode == 'v1diag':
        return v1_diag(out)
    if mode == 'v1':
        return v1_mode(out, int(argv[2]) if len(argv) > 2 else 500)
    if mode != 'time':
        raise SystemExit('modes: time, v1')
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
