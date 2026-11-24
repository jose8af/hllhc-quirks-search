"""p3d_exact.py -- exact one-bin results of the zero-count convention (numpy/scipy; maxwell).  Gorm, 2026-11-24.

Model (STR §4.11 pt 4, script [10] of strategy_budget.py l.1094-1181): one bin, one counted term B = kappa * lambda,
auxiliary count m, lambda ~ Gamma(m + 1) (flat prior).  Marginal of the background count: negative binomial
  P(g) = C(g + m, g) p^(m+1) (1 - p)^g,  p = 1/(1 + kappa)
(the Poisson(kappa lambda) mixture over Gamma(m + 1); for m = 0 the geometric kappa^g/(1+kappa)^(g+1) of STR l.1676).
n = Pois(s) + g (+ Pois(b0) for a known extra background).  CLs(s; n_obs) = P(n <= n_obs | s) / P(n <= n_obs | 0).
Expected limit at quantile p: n_p = smallest n with P(n <= n | 0) >= p, s95 solves CLs(s; n_p) = 0.05.
Coverage (STR l.1695-1700): sum_m Pois(m | lambda) sum_n Pois(n | s + kappa lambda + b0) 1[CLs_m(s; n) > 0.05].

  table <out>                                   the table of STR l.1680-1686 and the coverage of l.1695-1697
  cref  <out> <kappa> <s> <b0> <lambda list>    c_ref of Df-10 for a workspace (readings R5 (a) b0 = 0, (b) b0 > 0)
  curves <out> <kappa list> <m> <mu list>       CLs(mu) at n_16, n_50, n_84 (for the toy comparison of T1-c (i))
"""
import json
import logging
import math
import os
import sys

import numpy as np
from scipy import stats
from scipy.optimize import brentq

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3d_exact')
U68 = -math.log(0.32)


def nb_pmf(nmax, kappa, m):
    g = np.arange(nmax + 1)
    return stats.nbinom.pmf(g, m + 1, 1.0 / (1.0 + kappa))


def conv_cdf(a, b, nmax):
    """CDF up to nmax of the sum of two independent counts with pmfs a, b (FFT convolution)."""
    n = len(a) + len(b)
    size = 1 << int(math.ceil(math.log2(n)))
    c = np.fft.irfft(np.fft.rfft(a, size) * np.fft.rfft(b, size), size)[:nmax + 1]
    return np.clip(np.cumsum(np.clip(c, 0, None)), 0, 1)


def nmax_for(s, kappa, m, b0=0.0):
    mean = s + b0 + kappa * (m + 1)
    sd = math.sqrt(s + b0 + kappa * (m + 1) * (1 + kappa))
    return int(mean + 14 * sd + 50)


def cdf_sig(s, kappa, m, nmax, b0=0.0):
    pois = stats.poisson.pmf(np.arange(nmax + 1), s + b0)
    return conv_cdf(pois, nb_pmf(nmax, kappa, m), nmax)


def s95(nobs, kappa, m, b0=0.0):
    nmax = nobs + 10
    f0 = cdf_sig(0.0, kappa, m, nmax, b0)[nobs]

    def f(s):
        return cdf_sig(s, kappa, m, nmax, b0)[nobs] / f0 - 0.05
    hi = 3.0 + nobs + 1.0
    while f(hi) > 0:
        hi *= 2
    return brentq(f, 1e-9, hi, xtol=1e-9, rtol=1e-10)


def quantile_n(kappa, m, p, b0=0.0):
    nmax = nmax_for(0.0, kappa, m, b0)
    c = cdf_sig(0.0, kappa, m, nmax, b0)
    return int(np.searchsorted(c, p - 1e-15))


def table(out):
    rows = []
    for kappa in (0.1, 1.0, 10.0, 35.0, 124.0):
        hyb = [s95(quantile_n(kappa, 0, f), kappa, 0) for f in (0.16, 0.5, 0.84)]
        fixed_n = int(stats.poisson.median(U68 * kappa))      # scipy median = smallest n with CDF >= 0.5
        while stats.poisson.cdf(fixed_n, U68 * kappa) < 0.5:
            fixed_n += 1
        fix = brentq(lambda s: stats.poisson.cdf(fixed_n, s + U68 * kappa) / stats.poisson.cdf(fixed_n, U68 * kappa)
                     - 0.05, 1e-9, 1e4)
        tru = []
        for lam in (0.5, U68, 2.0, 3.0):
            nm = 0
            while stats.poisson.cdf(nm, lam * kappa) < 0.5:
                nm += 1
            tru.append(s95(nm, kappa, 0))
        rows.append(dict(kappa=kappa, dropped=-math.log(0.05), fixed_114=fix, median=hyb[1], band=[hyb[0], hyb[2]],
                         true_lambda=tru, n_quantiles=[quantile_n(kappa, 0, f) for f in (0.16, 0.5, 0.84)]))
        log.info('kappa %g: fixed %.1f, convention %.1f [%.1f, %.1f], true lambda %s', kappa, fix, hyb[1], hyb[0],
                 hyb[2], ['%.1f' % x for x in tru])
    cov = [dict(kappa=k, lam=lam, **coverage(k, 10.0, 0.0, lam)) for k in (1.0, 10.0) for lam in (0.5, U68, 2.0, 3.0)]
    json.dump(dict(mode='table', rows=rows, coverage_s10=cov), open(out, 'w'), indent=1)


def coverage(kappa, s, b0, lam, mmax=None):
    """Exact coverage of the one-bin convention at true signal s (Pois), true rate lambda, m redrawn."""
    mmax = mmax or int(lam + 12 * math.sqrt(lam) + 12)
    tot = 0.0; given0 = None; per_m = []
    for m in range(0, mmax + 1):
        pm = stats.poisson.pmf(m, lam)
        if pm < 1e-9:
            continue
        mu_true = s + b0 + kappa * lam
        nmax = max(nmax_for(s, kappa, m, b0), int(mu_true + 14 * math.sqrt(mu_true) + 50))
        cs = cdf_sig(s, kappa, m, nmax, b0); c0 = cdf_sig(0.0, kappa, m, nmax, b0)
        ok = cs / np.maximum(c0, 1e-300) > 0.05
        pn = stats.poisson.pmf(np.arange(nmax + 1), mu_true)
        cm = float(np.sum(pn[ok]))
        tot += pm * cm; per_m.append((m, float(pm), cm))
        if m == 0:
            given0 = cm
    return dict(coverage=tot, given_m0=given0, per_m=per_m)


def mode_cref(out, kappa, s, b0, lams):
    rows = []
    for lam in lams:
        c = coverage(kappa, s, b0, lam)
        rows.append(dict(lam=lam, c=c['coverage'], c_ref=min(c['coverage'], 0.95), given_m0=c['given_m0'],
                         per_m=c['per_m']))
        log.info('kappa %g s %g b0 %g lambda %g: coverage %.4f (given m = 0: %.4f)', kappa, s, b0, lam, c['coverage'],
                 c['given_m0'])
    json.dump(dict(mode='cref', kappa=kappa, s=s, b0=b0, rows=rows), open(out, 'w'), indent=1)


def mode_curves(out, kappas, m, mus):
    res = dict(mode='curves', m=m, rows=[])
    for kappa in kappas:
        for p in (0.16, 0.5, 0.84):
            n = quantile_n(kappa, m, p)
            nmax = n + 10
            f0 = cdf_sig(0.0, kappa, m, nmax)[n]
            res['rows'].append(dict(kappa=kappa, p=p, n=n, s95=s95(n, kappa, m),
                                    cls=[float(cdf_sig(mu, kappa, m, nmax)[n] / f0) for mu in mus], mus=mus,
                                    cdf_b_at_n=float(f0), cdf_b_below=float(cdf_sig(0.0, kappa, m, nmax)[n - 1]) if n else 0.0))
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'table':
        table(a[1])
    elif a[0] == 'cref':
        mode_cref(a[1], float(a[2]), float(a[3]), float(a[4]), [float(x) for x in a[5].split(',')])
    elif a[0] == 'curves':
        mode_curves(a[1], [float(x) for x in a[2].split(',')], float(a[3]), [float(x) for x in a[4].split(',')])
    os.sync() if hasattr(os, 'sync') else None
