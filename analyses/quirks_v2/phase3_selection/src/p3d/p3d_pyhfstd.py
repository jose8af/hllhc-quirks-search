"""p3d_pyhfstd.py -- pyhf 0.7.6's OWN toy calculator on one-bin workspaces (numpy backend; maxwell).  Gorm, 2026-11-24.

  demo0 <out> <kappa list> <ntoys>        STR l.1601 "[U] to be confirmed in Phase 3": the expected limit of pyhf's
        standard procedures (toys at the conditional MLE, ToyCalculator; and the asymptotic calculator, Asimov
        data at the fitted nuisances) on the one-bin workspace with one counted term, m = 0, kappa = N/M.  Data:
        n = 0 (the nominal expectation kappa * m), auxiliary count 0.  Records the fitted lambda_hat, the b-only toy
        counts, and the expected limits.
  std <out> <kappa> <m> <ntoys> <seed>    T1-c (ii) reference: pyhf's ToyCalculator on the same bin with the
        background as a Poisson-constrained `shapesys` (data kappa m, uncertainty kappa sqrt(m), i.e. tau = m),
        data n = kappa m; the sampled q~ distributions are exported and read with the same counting and limit
        recipe as our convention (p3d_toys.cls_counts / limit_status), so only the generation differs.
"""
import json
import logging
import math
import os
import sys
import time

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402
import pyhf  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

import p3d_model as pm  # noqa: E402
import p3d_toys as pt  # noqa: E402  (counting code only; jax is not imported at module level)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3d_pyhfstd')
logging.getLogger('pyhf').setLevel(logging.WARNING)
pyhf.set_backend('numpy')


def dump(out, res):
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f)
    os.replace(out + '.tmp', out)


def shapesys_model(kappa, m):
    spec = {'channels': [{'name': 'SR', 'samples': [
        {'name': 'signal', 'data': [1.0], 'modifiers': [{'name': 'mu', 'type': 'normfactor', 'data': None}]},
        {'name': 'bkg', 'data': [kappa * m],
         'modifiers': [{'name': 'stat_bkg', 'type': 'shapesys', 'data': [kappa * math.sqrt(m)]}]}]}],
        'observations': [{'name': 'SR', 'data': [kappa * m]}], 'version': '1.0.0',
        'measurements': [{'name': 'std', 'config': {'poi': 'mu', 'parameters': [
            {'name': 'mu', 'bounds': [[0.0, 1e5]], 'inits': [1.0]}]}}]}
    pyhf.schema.validate(spec, 'workspace.json')
    ws = pyhf.Workspace(spec)
    return ws, ws.model()


def expected_cls_scan(model, data, calctype, mus, ntoys=None, seed=0):
    out = []
    for mu in mus:
        if calctype == 'toybased':
            np.random.seed(seed + int(round(mu * 1000)))
            r = pyhf.infer.hypotest(mu, data, model, test_stat='qtilde', calctype='toybased', ntoys=ntoys,
                                    return_expected_set=True, track_progress=False)
        else:
            r = pyhf.infer.hypotest(mu, data, model, test_stat='qtilde', return_expected_set=True)
        out.append((float(mu), float(r[0]), [float(x) for x in r[1]]))
    return out


def crossing(scan, idx=2):
    for (m1, _, e1), (m2, _, e2) in zip(scan[:-1], scan[1:]):
        c1, c2 = e1[idx], e2[idx]
        if c1 > 0.05 >= c2:
            if c2 <= 0:
                return m2
            return m1 + (math.log(0.05) - math.log(c1)) * (m2 - m1) / (math.log(c2) - math.log(c1))
    return None


def mode_demo0(out, kappas, ntoys):
    res = dict(mode='demo0', pyhf=pyhf.__version__, numpy=np.__version__, ntoys=ntoys, rows=[])
    for kappa in kappas:
        spec = pm.onebin(kappa, 0.0)
        ws, model = pm.build(spec)
        data = [0.0, 0.0] + list(model.config.auxdata)          # n = 0, auxiliary count 0
        init = model.config.suggested_init(); bnd = model.config.suggested_bounds(); fx = model.config.suggested_fixed()
        p0 = pyhf.infer.mle.fixed_poi_fit(0.0, data, model, init, bnd, fx)
        lam_hat = float(p0[model.config.par_slice('lam_t').start])
        pdf = model.make_pdf(pyhf.tensorlib.astensor(p0))
        np.random.seed(7)
        smp = np.asarray(pdf.sample((ntoys,)))
        mus = np.concatenate([np.linspace(0.5, 6.0, 23), [8.0, 12.0, 20.0, 40.0]])
        sc_t = expected_cls_scan(model, data, 'toybased', mus, ntoys, seed=1000 * int(kappa))
        sc_a = expected_cls_scan(model, data, 'asymptotics', mus)
        res['rows'].append(dict(kappa=kappa, lam_hat_bkg_only=lam_hat, b_only_toys_n_gt0=int(np.sum(smp[:, 0] > 0)),
                                b_only_toys_aux_gt0=int(np.sum(smp[:, 1] > 0)), expected_toys=crossing(sc_t),
                                expected_asymptotic=crossing(sc_a), scan_toys=sc_t, scan_asym=sc_a,
                                analytic_convention_median={1.0: 3.0, 10.0: 10.8, 35.0: 27.8}.get(kappa)))
        log.info('demo0 kappa %g: lambda_hat %.3g, b-only toys with n > 0: %d of %d; expected toys %s, asymptotic %s',
                 kappa, lam_hat, res['rows'][-1]['b_only_toys_n_gt0'], ntoys, res['rows'][-1]['expected_toys'],
                 res['rows'][-1]['expected_asymptotic'])
    dump(out, res)


def mode_std(out, kappa, m, ntoys, seed, budget=1500.0):
    t0 = time.time()
    ws, model = shapesys_model(kappa, m)
    data = [kappa * m] + list(model.config.auxdata)
    f = lambda mu: float(pyhf.infer.hypotest(mu, data, model, test_stat='qtilde', return_expected_set=True)[1][2]) - 0.05  # noqa: E731
    hi = 2.0 * math.sqrt(kappa * m * (1 + kappa)) + 5.0
    while f(hi) > 0:
        hi *= 2
    mu_a = brentq(f, 1e-3, hi, rtol=1e-6)
    res = dict(mode='std', pyhf=pyhf.__version__, kappa=kappa, m=m, ntoys=ntoys, seed=seed, mu_a=mu_a, points=[])
    pts = []

    def evaluate(mu):
        np.random.seed([seed, pt.mu_key(mu) % (2 ** 31)])
        calc = pyhf.infer.utils.create_calculator('toybased', data, model, ntoys=ntoys, test_stat='qtilde',
                                                  track_progress=False)
        sb, b = calc.distributions(mu)
        rec = dict(mu=float(mu), qb=pt._r(np.asarray(b.samples, float)), qsb=pt._r(np.asarray(sb.samples, float)))
        pts.append(rec); res['points'].append(rec)
        log.info('std kappa %g m %g mu %.4g: %s', kappa, m, mu, pt.counts_of(rec, 0.5, 'ecdf'))
    for g in pt.GRID:
        evaluate(mu_a * g)
    status = {}
    while time.time() - t0 < budget and len(pts) < 40:
        nxt = None
        for p in (0.16, 0.5, 0.84):
            s = pt.limit_status([(r['mu'], pt.counts_of(r, p, 'ecdf')) for r in pts]); status[str(p)] = s
            if s['status'] != 'ok' and s.get('next') and nxt is None:
                nxt = s['next']
        if nxt is None:
            break
        evaluate(nxt)
    for p in (0.16, 0.5, 0.84):
        status[str(p)] = pt.limit_status([(r['mu'], pt.counts_of(r, p, 'ecdf')) for r in pts])
    status['0.5|npmedian'] = pt.limit_status([(r['mu'], pt.counts_of(r, 0.5, 'npmedian')) for r in pts])
    res['status'] = status
    res['complete'] = all(s['status'] == 'ok' for s in status.values())
    dump(out, res)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'demo0':
        mode_demo0(a[1], [float(x) for x in a[2].split(',')], int(a[3]))
    elif a[0] == 'std':
        mode_std(a[1], float(a[2]), float(a[3]), int(a[4]), int(a[5]))
