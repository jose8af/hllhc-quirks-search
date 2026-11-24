"""p3d_summary.py -- verdicts and machine-readable results of p3-d from the campaign outputs.  Gorm, 2026-11-24.
Reads only files whose runner marker says `done`.  Light (numpy; run on a worker with the numpy env).
  onebin   T1-c (i), (ii), the pyhf demonstration (STR l.1601) -> outputs/p3d/t1c_onebin.json
  recipe   the refined recipe on the v1-mode workspace (10 replicas) -> outputs/p3d/recipe_v1mode.json
  cover <tag ...>  T1-c (iii)-(v) from the coverage campaigns -> outputs/p3d/t1c_coverage.json
Toy error of a limit: bootstrap of the stored q arrays at every evaluated point (200 resamples), the limit
recomputed on the same points with the recipe's interpolation (no new points).
"""
import json
import logging
import math
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p3d_toys as pt  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p3d_summary')
AN = Path(__file__).resolve().parents[3]
DATA = AN / 'data' / 'p3d'
MARK = AN / 'ledger' / 'markers'
OUT = AN / 'phase3_selection' / 'outputs' / 'p3d'


def load(camp, job):
    mk = MARK / camp / '000' / f'{job}.marker'
    if not mk.exists() or '"done"' not in mk.read_text():
        return None
    return json.load(open(DATA / camp / '000' / f'{job}.json'))


def mu95(points, p, rule, empty='hi'):
    s = pt.limit_status([(r['mu'], pt.counts_of(r, p, rule)) for r in points], empty=empty, refine=1e9)
    return s.get('mu95'), s


def boot(points, p, rule, nb=200, seed=7):
    rng = np.random.default_rng(seed)
    arr = [(r['mu'], pt._a(r['qb']), pt._a(r['qsb'])) for r in points]
    vals = []
    for _ in range(nb):
        pts = []
        for mu, qb, qs in arr:
            pts.append((mu, pt.cls_counts(qb[rng.integers(0, len(qb), len(qb))], qs[rng.integers(0, len(qs), len(qs))],
                                          p, rule)))
        v = pt.limit_status(pts, refine=1e9).get('mu95')
        if v is not None:
            vals.append(v)
    return (float(np.std(vals, ddof=1)) if len(vals) > 10 else None), len(vals)


def edge_counts(r, level):
    """Counts with q_obs forced to the level-th largest DISTINCT b-only q (ties within 1e-5): for one bin, level 0 =
    q(n = 0), level 1 = q(n = 1).  Used for the discrete median edge at kappa = 1 (reported both sides, none chosen)."""
    qb = pt._a(r['qb']); qs = pt._a(r['qsb'])
    qb = qb[np.isfinite(qb)]; qs = qs[np.isfinite(qs)]
    lv = []
    for v in np.sort(qb)[::-1]:
        if not lv or lv[-1] - v > pt.TIE_TOL:
            lv.append(v)
        if len(lv) > level:
            break
    qo = lv[level]
    ksb = int(np.sum(qs >= qo - pt.TIE_TOL)); kb = int(np.sum(qb >= qo - pt.TIE_TOL))
    return dict(resolved=True, kb=kb, nb=len(qb), ksb=ksb, nsb=len(qs), q_obs=float(qo),
                cls=(ksb / len(qs)) / (kb / len(qb)), frac_b_at_or_above=kb / len(qb))


def onebin():
    res = dict(c1=[], c2=[], demo0=None)
    curves = load('p3-d-pyhf', 'p3-d-exact-curves'); table = load('p3-d-pyhf', 'p3-d-exact-table')
    ana = {}
    for r in curves['rows']:
        ana[(r['kappa'], r['p'])] = r
    for k in ('1', '10', '35'):
        d = load('p3-d-one', f'p3-d-one-c1-k{k}')
        if d is None:
            continue
        for p in (0.16, 0.5, 0.84):
            for rule in (('ecdf', 'npmedian') if p == 0.5 else ('ecdf',)):
                v, s = mu95(d['points'], p, rule)
                e, nb = boot(d['points'], p, rule)
                a = ana[(float(k), p)]['s95']
                z = (v - a) / e if (v is not None and e) else None
                res['c1'].append(dict(kappa=float(k), p=p, rule=rule, toy=v, toy_err=e, analytic=a, z=z,
                                      bracket=s.get('bracket'), within_1sigma=(abs(z) <= 1) if z is not None else None,
                                      within_2sigma=(abs(z) <= 2) if z is not None else None,
                                      n_points=len(d['points']), dropped=sum(r['b']['dropped'] + r['sb']['dropped']
                                                                             for r in d['points'])))
                log.info('T1-c (i) kappa %s p %s %s: toy %s +- %s, analytic %.3f, z %s', k, p, rule, v, e, a, z)
    for k in ('1', '10', '35'):
        for m in ('100', '1000'):
            d = load('p3-d-one', f'p3-d-one-c2-k{k}-m{m}'); r0 = load('p3-d-pyhf', f'p3-d-pyhf-std-k{k}-m{m}')
            if d is None or r0 is None:
                continue
            for p in (0.16, 0.5, 0.84):
                v, _ = mu95(d['points'], p, 'ecdf'); e, _ = boot(d['points'], p, 'ecdf')
                v0, _ = mu95(r0['points'], p, 'ecdf'); e0, _ = boot(r0['points'], p, 'ecdf')
                z = (v - v0) / math.hypot(e, e0) if None not in (v, v0, e, e0) else None
                res['c2'].append(dict(kappa=float(k), m=float(m), p=p, convention=v, convention_err=e, pyhf_std=v0,
                                      pyhf_std_err=e0, z=z, within_1sigma=(abs(z) <= 1) if z is not None else None,
                                      within_2sigma=(abs(z) <= 2) if z is not None else None))
                log.info('T1-c (ii) kappa %s m %s p %s: convention %s +- %s, pyhf %s +- %s, z %s', k, m, p, v, e, v0,
                         e0, z)
    d1 = load('p3-d-one', 'p3-d-one-c1-k1')
    if d1 is not None:
        res['c1_k1_median_edge'] = {}
        for lev, lab in ((0, 'side n_obs = 0 (analytic convention, CDF_b(0) = 0.5 >= 0.5)'), (1, 'side n_obs = 1')):
            pts = [(r['mu'], edge_counts(r, lev)) for r in d1['points']]
            st = pt.limit_status(pts, refine=1e9)
            res['c1_k1_median_edge'][lab] = dict(mu95=st.get('mu95'), bracket=st.get('bracket'),
                                                 analytic=[3.0, 5.7][lev],
                                                 frac_b_n0=[c['frac_b_at_or_above'] for _, c in pts] if lev == 0 else None)
        log.info('kappa 1 median edge: %s', {k: v['mu95'] for k, v in res['c1_k1_median_edge'].items()})
    dem = []
    for k in ('1', '10', '35'):
        d = load('p3-d-pyhf', f'p3-d-pyhf-demo0-k{k}')
        if d:
            r = d['rows'][0]
            dem.append({x: r[x] for x in ('kappa', 'lam_hat_bkg_only', 'b_only_toys_n_gt0', 'b_only_toys_aux_gt0',
                                          'expected_toys', 'expected_asymptotic')} | dict(ntoys=d['ntoys']))
    res['demo0'] = dem
    res['exact_table'] = table
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(OUT / 't1c_onebin.json', 'w'), indent=1)


def recipe():
    rows = []
    for i in range(10):
        d = load('p3-d-one', f'p3-d-one-rec-{i:02d}')
        if d is None:
            continue
        st = d['status']
        rows.append(dict(seed=d['seed'], refined_ecdf=st['0.5|ecdf'].get('mu95'), status=st['0.5|ecdf']['status'],
                         bracket=st['0.5|ecdf'].get('bracket'), empty_upper=st['0.5|ecdf'].get('empty_upper'),
                         refined_npmedian=st['0.5|npmedian'].get('mu95'),
                         frozen_grid_ecdf=st['0.5|ecdf'].get('frozen_grid_value'),
                         frozen_grid_npmedian=st['0.5|npmedian'].get('frozen_grid_value'),
                         variants=st['0.5|ecdf'].get('variants'), n_points=len(d['points']),
                         dropped=sum(r['b']['dropped'] + r['sb']['dropped'] for r in d['points']),
                         toys=sum(2 * r['ntoys'] for r in d['points']), mu_a=d['mu_a'],
                         cpu_s_per_unit=float(np.median([r['cpu_s_per_unit'] for r in d['points']]))))
    out = dict(rows=rows)
    for key in ('refined_ecdf', 'refined_npmedian', 'frozen_grid_ecdf', 'frozen_grid_npmedian'):
        x = np.array([r[key] for r in rows if r[key] is not None], float)
        if len(x) > 1:
            out[key] = dict(n=len(x), mean=float(x.mean()), sd=float(x.std(ddof=1)), min=float(x.min()),
                            max=float(x.max()), inside_v1_window=int(np.sum((x >= 710.77) & (x <= 868.72))))
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT / 'recipe_v1mode.json', 'w'), indent=1)
    log.info('recipe: %s', {k: v for k, v in out.items() if k != 'rows'})


if __name__ == '__main__':
    {'onebin': onebin, 'recipe': recipe}[sys.argv[1]]()
