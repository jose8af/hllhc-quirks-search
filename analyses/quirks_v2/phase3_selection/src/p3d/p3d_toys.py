"""p3d_toys.py -- T1 hybrid toys, the limit recipe, stored distributions and coverage (STR §4.11 pt 2; COM T1-c, T1-i,
l.295-296, l.356).  Gorm, 2026-11-24.  Runs on the jax env (schrodinger) for every fit; the counting and limit code
(cls_counts, limit_status) is numpy only and is imported by p3d_pyhfstd.py.

GENERATION (STR l.1626-1629): per pseudo-experiment every counted rate lambda_f ~ Gamma(m_f + a) (a = 1 flat prior;
a = 1/2 Jeffreys alternative; a fixed rate stays fixed), every constrained nuisance theta ~ N(0, 1) clipped at its
censoring bound (and at the pyhf range [-5, 5]); n_c ~ Pois(expected_c(mu, lambda, theta)); auxiliary observations
stay at m (or at m' for the stored distributions of the coverage test).
TEST STATISTIC: q~_mu from two pyhf fits (fixed_poi_fit with do_stitch, fit), q = 0 if mu_hat > mu.
FIT GUARD (FLO §4): SLSQP tolerance 1e-10; start = previous toy's result of the same ensemble (warm start, VIK e3),
the free fit chained from the fixed fit; accepted if the Newton decrement (jax gradient and Hessian over the
parameters neither fixed nor within 1e-6 of the range of a bound) is below 1e-4 for both fits and t_free <= t_fix
(+1e-6 relative); else retried from the generated values, then from the default start; else dropped.  A mu point is
unresolved if more than 2 % of an ensemble is dropped.
CLs: q_obs(p) = ceil(p N)-th largest b-only q (rule 'ecdf', R6 (a)) or numpy.median (rule 'npmedian', R6 (b), p = 0.5
only); k = #(q >= q_obs - 1e-5); CLs = (k_sb/N_sb)/(k_b/N_b).
LIMIT RECIPE (R9, proposed for PREREG_v2): grid mu_a x GRID, x1.5 extensions while not bracketed, then bisection
(geometric midpoint) of the first-crossing bracket until mu_hi/mu_lo - 1 <= 2 %; every evaluated point enters the
first-crossing search; ln-CLs linear interpolation in mu inside the final bracket; an empty s+b tail counts as
excluded and, at the upper end of the final bracket, gives mu95 = mu_hi.

MODES (one JSON output each; through the runner)
  check  <out> <specname> [censor]                                schema, consistency, Asimov limit mu_a, predictive
  limit  <out> <specname> <settings> <seed> <ntoys> <quantiles> <budget_s> [prior files...]
  store  <out> <specname> <settings> <seed> <ntoys> <fid> <m'> <mu list>
  cover  <out> <specname> <settings> <seed> <fid> <mu_true> <lambda list> <npe> <store files...>
  cost   <out> <specname> <settings> <ntoys> <mu>
settings: comma list censor=0/1, a=1/0.5, alt=fixed114, tol=1e-10.  specname: see p3d_specs.get().
"""
import json
import logging
import math
import os
import resource
import sys
import time

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
os.environ.setdefault('XLA_FLAGS', '--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1')
os.environ.setdefault('JAX_PLATFORMS', 'cpu')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np  # noqa: E402

import p3d_model as pm  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3d_toys')

TIE_TOL = 1e-5
MAX_DROP = 0.02
GRID = (0.4, 0.55, 0.75, 1.0, 1.35, 1.8, 2.5, 3.5)          # STR l.1640
REFINE = 0.02                                                # bisection to 2 % (COM l.295)
ND_MAX = 1e-4                                                # Newton-decrement acceptance (FLO §4 (b))
pyhf = None


# ============================================================================================ counting (numpy only)
def q_obs_of(qb, p, rule='ecdf'):
    s = np.sort(qb)
    n = len(s)
    if rule == 'npmedian':
        return float(np.median(s))
    k = int(math.ceil(p * n))                 # the k-th largest
    return float(s[n - k])


def cls_counts(qb, qsb, p=0.5, rule='ecdf', tol=TIE_TOL):
    qb = np.asarray(qb, float); qsb = np.asarray(qsb, float)
    nb0, ns0 = len(qb), len(qsb)
    qb = qb[np.isfinite(qb)]; qsb = qsb[np.isfinite(qsb)]
    if len(qb) == 0 or len(qsb) == 0:
        return dict(resolved=False, kb=0, nb=0, ksb=0, nsb=0, q_obs=None, cls=None)
    qo = q_obs_of(qb, p, rule)
    ksb = int(np.sum(qsb >= qo - tol)); kb = int(np.sum(qb >= qo - tol))
    res = bool(1 - len(qb) / nb0 <= MAX_DROP and 1 - len(qsb) / ns0 <= MAX_DROP)
    return dict(resolved=res, kb=kb, nb=int(len(qb)), ksb=ksb, nsb=int(len(qsb)), q_obs=qo,
                cls=(ksb / len(qsb)) / (kb / len(qb)))


def cls_at(qb, qsb, qo, tol=TIE_TOL):
    """CLs for a given observed q (coverage: observed pseudo-data against stored distributions)."""
    qb = qb[np.isfinite(qb)]; qsb = qsb[np.isfinite(qsb)]
    kb = np.sum(qb[None, :] >= np.asarray(qo)[:, None] - tol, 1)
    ksb = np.sum(qsb[None, :] >= np.asarray(qo)[:, None] - tol, 1)
    return (ksb / len(qsb)) / np.maximum(kb / len(qb), 1e-300), ksb


def limit_status(points, empty='hi', refine=REFINE):
    """points: [(mu, counts)].  First crossing of CLs = 0.05 from low mu over the resolved points.  Returns status
    'extend_down' | 'extend_up' | 'refine' (with the mu to evaluate next) | 'ok' (mu95) | 'unresolved'."""
    pts = sorted([(m, c) for m, c in points if c['resolved']], key=lambda x: x[0])
    if len(pts) < 2:
        return dict(status='unresolved')
    if pts[0][1]['cls'] <= 0.05:
        return dict(status='extend_down', next=pts[0][0] / 1.5)
    for i in range(len(pts) - 1):
        (m1, c1), (m2, c2) = pts[i], pts[i + 1]
        if c1['cls'] > 0.05 >= c2['cls']:
            inside = [m for m, c in points if not c['resolved'] and m1 < m < m2]
            if m2 / m1 - 1.0 > refine * (1 + 1e-9):
                return dict(status='refine', next=math.sqrt(m1 * m2), bracket=[m1, m2], unresolved_inside=inside)
            zero = c2['ksb'] == 0
            if zero and empty == 'hi':
                mu95 = m2
            else:
                k2 = c2['ksb'] if not zero else (1.139 if empty == 'k1139' else 0.5)
                l1, l2 = math.log(c1['cls']), math.log(k2 / c2['nsb'] / (c2['kb'] / c2['nb']))
                mu95 = m1 + (math.log(0.05) - l1) * (m2 - m1) / (l2 - l1)
            return dict(status='ok', mu95=float(mu95), bracket=[m1, m2], cls_bracket=[c1['cls'], c2['cls']],
                        empty_upper=bool(zero), unresolved_inside=inside)
    return dict(status='extend_up', next=pts[-1][0] * 1.5)


def limit_frozen(points):
    """The frozen recipe without refinement (grid + extensions, ln interpolation, empty tail as 1.139 counts):
    for comparison only."""
    pts = sorted([(m, c) for m, c in points if c['resolved']], key=lambda x: x[0])
    for i in range(len(pts) - 1):
        (m1, c1), (m2, c2) = pts[i], pts[i + 1]
        if c1['cls'] > 0.05 >= c2['cls']:
            k2 = c2['ksb'] or 1.139
            l1, l2 = math.log(c1['cls']), math.log(k2 / c2['nsb'] / (c2['kb'] / c2['nb']))
            return m1 + (math.log(0.05) - l1) * (m2 - m1) / (l2 - l1)
    return None


# ============================================================================================ settings and fits
def parse_settings(text):
    s = dict(censor=1, a=1.0, alt='', tol=1e-10, warm=1)
    for kv in (text or '').split(','):
        if kv and kv != '-':
            k, v = kv.split('=')
            s[k] = v if k == 'alt' else (float(v) if k in ('a', 'tol') else int(v))
    return s


def set_backend(tol):
    global pyhf
    import pyhf as _p
    pyhf = _p
    kw = {} if tol is None or tol <= 0 else dict(tolerance=tol)
    pyhf.set_backend('jax', pyhf.optimize.scipy_optimizer(**kw))
    return pyhf.tensorlib


class Engine:
    def __init__(self, spec, st):
        self.spec = spec; self.st = st
        if st['alt'] == 'fixed114':
            spec = pm.with_alternative(spec, 'fixed114'); self.spec = spec
        self.censor = bool(st['censor'])
        self.ws, self.model = pm.build(spec, censor=self.censor)
        self.ex = pm.Explicit(spec, censor=self.censor)
        cfg = self.model.config; self.cfg = cfg
        self.bounds = np.array(cfg.suggested_bounds(), float); self.fixed = list(cfg.suggested_fixed())
        self.i_mu = cfg.poi_index
        self.auxdata = np.asarray(cfg.auxdata, float)
        self.tl = pyhf.tensorlib
        self.fid_idx = {f: cfg.par_slice('lam_' + f).start for f in self.ex.fids}
        self.th_idx = [cfg.par_slice(n).start for n in self.ex.nk]
        self.fixed_idx = [i for i, x in enumerate(self.fixed) if x]
        import jax
        f = lambda p, d: pyhf.infer.mle.twice_nll(p, d, self.model)[0]                    # noqa: E731
        try:
            self._g = jax.jit(jax.grad(f)); self._h = jax.jit(jax.hessian(f)); self._f = jax.jit(f)
            self._g(self.tl.astensor(np.array(cfg.suggested_init(), float)), self.tl.astensor(self.data(
                np.ones(len(spec['cats'])), self.ex.m)))
        except Exception as e:  # noqa: BLE001
            log.warning('jit of the guard failed (%r); using un-jitted jax', e)
            self._g = jax.grad(f); self._h = jax.hessian(f); self._f = f
        self.cpu_fit = 0.0; self.nfit = 0; self.cpu_guard = 0.0
        self.prev = None
        self.th_lo = np.full(len(self.ex.nk), pm.TH_LO)
        self.th_hi = np.minimum(self.ex.bound, pm.TH_HI)

    def nparams(self):
        return int(self.cfg.npars)

    def data(self, n, aux):
        return np.concatenate([np.asarray(n, float), np.asarray(aux, float), self.auxdata])

    def default_init(self, aux, mu):
        p = np.array(self.cfg.suggested_init(), float)
        for j, f in enumerate(self.ex.fids):
            if not self.ex.fixed[j]:
                p[self.fid_idx[f]] = aux[j] + 1.0
        p[self.i_mu] = mu
        return p

    def gen_pars(self, mu, lam, th):
        return self.ex.par_vector(self.model, mu, lam, th)

    def newton(self, pars, d, exclude_mu):
        c0 = time.process_time()
        p = self.tl.astensor(pars)
        g = np.asarray(self._g(p, d), float); H = np.asarray(self._h(p, d), float)
        b = self.bounds; span = b[:, 1] - b[:, 0]
        # active set (KKT): at a bound, or within KKT_FRAC of the range from it with the gradient pointing outward
        lo_act = ((pars - b[:, 0]) <= 1e-6 * span) | (((pars - b[:, 0]) <= self.KKT_FRAC * span) & (g > 0))
        hi_act = ((b[:, 1] - pars) <= 1e-6 * span) | (((b[:, 1] - pars) <= self.KKT_FRAC * span) & (g < 0))
        free = [i for i in range(len(pars)) if i not in self.fixed_idx and not (exclude_mu and i == self.i_mu)
                and not lo_act[i] and not hi_act[i]]
        self.cpu_guard += time.process_time() - c0
        if not free:
            return 0.0
        gs = g[free]; Hs = H[np.ix_(free, free)]
        if not np.all(np.isfinite(Hs)) or not np.all(np.isfinite(gs)):
            return float('inf')
        if self.KKT_FRAC == 0.0:          # the Phase-2 form (Cholesky); kept for comparison
            try:
                np.linalg.cholesky(Hs)
            except np.linalg.LinAlgError:
                return float('inf')
            return float(0.5 * gs @ np.linalg.solve(Hs, gs))
        e, v = np.linalg.eigh(0.5 * (Hs + Hs.T))
        emax = max(float(np.max(np.abs(e))), 1e-300)
        if e[0] < -1e-6 * emax:           # a saddle or a maximum: not a minimum
            return float('inf')
        keep = e > 1e-12 * emax           # directions without curvature carry no Newton step
        proj = v.T @ gs
        return float(0.5 * np.sum(proj[keep] ** 2 / e[keep]))

    METHODS = ('SLSQP', 'L-BFGS-B')       # pyhf's scipy optimizer, method option (pyhf opt_scipy.py l.64)
    KKT_FRAC = 1e-3                       # remediation 3 (session log 15:10); 0 = the Phase-2 guard

    def fit1(self, d, mu, start, method):
        """One pyhf fit: fixed mu (mu given) or free (mu None).  Returns (pars, twice_nll) or None on exception."""
        c0 = time.process_time()
        try:
            s0 = np.clip(start, self.bounds[:, 0], self.bounds[:, 1])
            if mu is not None:
                s0[self.i_mu] = mu
                p, t = pyhf.infer.mle.fixed_poi_fit(mu, d, self.model, list(s0), self.bounds.tolist(), self.fixed,
                                                    return_fitted_val=True, do_stitch=True, method=method)
            else:
                p, t = pyhf.infer.mle.fit(d, self.model, list(s0), self.bounds.tolist(), self.fixed,
                                          return_fitted_val=True, do_stitch=True, method=method)
            out = (np.asarray(self.tl.tolist(p), float), float(t))
        except Exception:  # noqa: BLE001 -- a failed attempt, counted by the caller
            out = None
        self.cpu_fit += time.process_time() - c0; self.nfit += 1
        return out

    def polish(self, r, d, exclude_mu):
        """Project parameters within KKT_FRAC of the range from a bound, gradient pointing outward, onto the bound;
        keep the projected point if its twice-NLL is not higher (remediation 3)."""
        if self.KKT_FRAC == 0.0:
            return r
        p, t = r
        c0 = time.process_time()
        g = np.asarray(self._g(self.tl.astensor(p), d), float)
        b = self.bounds; span = b[:, 1] - b[:, 0]
        q = p.copy()
        lo = ((p - b[:, 0]) <= self.KKT_FRAC * span) & (g > 0)
        hi = ((b[:, 1] - p) <= self.KKT_FRAC * span) & (g < 0)
        for i in self.fixed_idx + ([self.i_mu] if exclude_mu else []):
            lo[i] = hi[i] = False
        if not (lo.any() or hi.any()):
            self.cpu_guard += time.process_time() - c0
            return r
        q[lo] = b[lo, 0]; q[hi] = b[hi, 1]
        t2 = float(np.asarray(self._f(self.tl.astensor(q), d)))
        self.cpu_guard += time.process_time() - c0
        return (q, t2) if np.isfinite(t2) and t2 <= t else r

    def best_fit(self, d, mu, starts, first_ok=True):
        """Attempts (start x method) in order; accepted = finite and Newton decrement < ND_MAX.  Returns
        (pars, t, newton, attempt index) of the first accepted (first_ok) or of the lowest accepted t."""
        best = None; k = 0
        for s0 in starts:
            for meth in self.METHODS:
                r = self.fit1(d, mu, s0, meth); k += 1
                if r is None or not np.isfinite(r[1]):
                    continue
                r = self.polish(r, d, mu is not None)
                nd = self.newton(r[0], d, mu is not None)
                if nd < ND_MAX and (best is None or r[1] < best[1]):
                    best = (r[0], r[1], nd, k - 1)
                    if first_ok:
                        return best
                if best is not None and not first_ok:
                    break
        return best

    def two_fits(self, d, mu, init_fix):
        r1 = self.fit1(d, mu, init_fix, 'SLSQP'); r2 = self.fit1(d, None, r1[0], 'SLSQP')
        return r1[0], r1[1], r2[0], r2[1]

    def q(self, n, aux, mu, gen=None):
        """q~_mu with the guard.  Fixed fit: starts warm / generated values / default, each with SLSQP then L-BFGS-B,
        first accepted.  Free fit: from the accepted fixed-fit point and from the generated values (mu at its
        generated value), the lower accepted minimum (never above t_fix: the fixed-fit point is feasible).
        Returns (q or nan, status 0 first attempt / 1 retried / 2 dropped, max Newton decrement)."""
        d = self.tl.astensor(self.data(n, aux))
        warm = self.st['warm'] and self.prev is not None
        # 1. free fit: from the generated values and the previous toy's free minimum; the lower accepted minimum
        fr_starts = ([gen.copy()] if gen is not None else []) + ([self.prev[1].copy()] if warm else [])
        if not fr_starts:
            fr_starts = [self.default_init(aux, 0.0)]
        fr = self.best_fit(d, None, fr_starts, first_ok=False)
        if fr is None:
            fr = self.best_fit(d, None, [self.default_init(aux, 0.0)], first_ok=True)
            if fr is None:
                return float('nan'), 2, None
        pu, tu, n2, k2 = fr
        muhat = pu[self.i_mu]
        # 2. fixed fit: from the free minimum (mu set), the previous toy's fixed minimum, the generated values
        starts = [pu.copy()] + ([self.prev[0].copy()] if warm else []) + ([gen.copy()] if gen is not None else [])
        fx = self.best_fit(d, mu, starts, first_ok=True)
        retried = fx is None or fx[3] > 0
        if fx is None:          # 3. continuation in mu from mu_hat (4 steps), each step warm-started
            p = pu.copy(); ok = True
            for k in range(1, 5):
                mk = muhat + (mu - muhat) * k / 4.0
                r = self.best_fit(d, mk, [p], first_ok=True)
                if r is None:
                    ok = False; break
                p = r[0]
            fx = r if ok else None
        if fx is None:
            return float('nan'), 2, None
        pf, tf, n1, k1 = fx
        if tu > tf + 1e-6 * max(1.0, abs(tf)):
            return float('nan'), 2, None
        self.prev = (pf, pu)
        return (0.0 if muhat > mu else max(tf - tu, 0.0)), (1 if retried else 0), max(n1, n2)

    def draw(self, mu, ntoys, rng, a, aux_m=None, lam_true=None, th_mode='draw'):
        """Hybrid draw.  aux_m: the auxiliary observations used for the Gamma(m + a) posterior (default: spec m).
        lam_true / th_mode='zero': fixed true values instead (coverage pseudo-experiments)."""
        ex = self.ex
        m = ex.m if aux_m is None else np.asarray(aux_m, float)
        if lam_true is None:
            lam = rng.gamma(m[None, :] + a, size=(ntoys, len(m))) if len(m) else np.zeros((ntoys, 0))
        else:
            lam = np.broadcast_to(np.asarray(lam_true, float), (ntoys, len(m))).copy()
        lam[:, ex.fixed] = ex.fixval[ex.fixed]
        if th_mode == 'zero':
            th = np.zeros((ntoys, len(ex.nk)))
        else:
            th = rng.standard_normal((ntoys, len(ex.nk)))
            th = np.clip(th, self.th_lo[None, :], (self.th_hi if self.censor else np.full(len(ex.nk), pm.TH_HI))[None, :])
        e = ex.expected(np.full(ntoys, mu), lam, th)
        n = rng.poisson(e).astype(float)
        return n, lam, th

    def ensemble(self, mu, ntoys, seed, e, a, aux_m=None):
        """One ensemble (e = 0 background-only, 1 signal + background) at mu."""
        rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(e), mu_key(mu)]))
        aux = self.ex.m if aux_m is None else np.asarray(aux_m, float)
        mu_gen = 0.0 if e == 0 else mu
        n, lam, th = self.draw(mu_gen, ntoys, rng, a, aux_m=aux)
        self.prev = None
        q = np.empty(ntoys); stt = np.zeros(ntoys, int); nd = []
        for i in range(ntoys):
            q[i], stt[i], x = self.q(n[i], aux, mu, self.gen_pars(mu_gen, lam[i], th[i]))
            if x is not None:
                nd.append(x)
        return q, dict(retried=int(np.sum(stt == 1)), dropped=int(np.sum(stt == 2)),
                       newton_max=float(max(nd)) if nd else None)

    def point(self, mu, ntoys, seed, a, aux_m=None):
        c0 = time.process_time(); f0 = self.cpu_fit; g0 = self.cpu_guard
        qb, ib = self.ensemble(mu, ntoys, seed, 0, a, aux_m)
        qs, isb = self.ensemble(mu, ntoys, seed, 1, a, aux_m)
        cpu = time.process_time() - c0
        rec = dict(mu=float(mu), ntoys=ntoys, seed=seed, qb=_r(qb), qsb=_r(qs), b=ib, sb=isb, cpu_s=cpu,
                   fit_cpu_s=self.cpu_fit - f0, guard_cpu_s=self.cpu_guard - g0,
                   cpu_s_per_unit=1000.0 * cpu / ntoys)
        log.info('mu %.5g: dropped %d/%d retried %d/%d, %.1f s per 1000+1000 (fits %.1f, guard %.1f)', mu,
                 ib['dropped'], isb['dropped'], ib['retried'], isb['retried'], rec['cpu_s_per_unit'],
                 1000 * rec['fit_cpu_s'] / ntoys, 1000 * rec['guard_cpu_s'] / ntoys)
        return rec

    def asimov_q(self, mu):
        ex = self.ex
        lam = np.where(ex.fixed, ex.fixval, ex.m + 1.0)
        n = ex.expected(np.array([0.0]), lam[None, :], np.zeros((1, len(ex.nk))))[0]
        aux = np.where(ex.fixed, ex.m, ex.m + 1.0)
        self.prev = None
        q, stt, _ = self.q(n, aux, mu, self.gen_pars(0.0, lam, np.zeros(len(ex.nk))))
        return q

    def mu_asym(self, mu0):
        from scipy.optimize import brentq
        from scipy.special import ndtr
        f = lambda m: 2.0 * (1.0 - float(ndtr(math.sqrt(max(self.asimov_q(m), 0.0))))) - 0.05      # noqa: E731
        lo, hi = mu0, mu0
        while f(lo) < 0 and lo > 1e-8:
            lo /= 2
        while f(hi) > 0 and hi < 1e12:
            hi *= 2
        return float(brentq(f, lo, hi, rtol=1e-6))


def mu_key(mu):
    return int(round((math.log(mu) + 60.0) * 1e6))


def _r(x):
    return [None if not np.isfinite(v) else float('%.9g' % v) for v in x]


def _a(x):
    return np.array([np.nan if v is None else v for v in x], float)


def counts_of(rec, p, rule):
    return cls_counts(_a(rec['qb']), _a(rec['qsb']), p, rule)


def dump(out, res):
    res['max_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f)
    os.replace(out + '.tmp', out)


def versions():
    import jax
    import scipy
    return dict(pyhf=pyhf.__version__, jax=jax.__version__, numpy=np.__version__, scipy=scipy.__version__,
                host=os.uname().nodename)


# ============================================================================================ modes
def mode_check(out, specname, settings):
    import p3d_specs
    st = parse_settings(settings); set_backend(st['tol'])
    spec = p3d_specs.get(specname)
    res = dict(versions(), mode='check', spec=specname, settings=st)
    eng = Engine(spec, st)
    res['schema_valid'] = True                       # build() validates and raises otherwise
    res['n_par'] = eng.nparams(); res['n_counted'] = len(eng.ex.fids); res['n_nuis'] = len(eng.ex.nk)
    res['par_order'] = list(eng.cfg.par_order)
    res['gen_check'] = pm.consistency(eng.spec, eng.model, np.random.default_rng(424242), censor=eng.censor)
    res['predictive'] = pm.predictive(eng.spec, nmc=200000, seed=20261124, censor=eng.censor)
    res['leading_zero_term'] = pm.leading_zero_term(eng.spec, res['predictive'])
    res['leading_fid'] = pm.zero_fid(eng.spec, res['leading_zero_term']) if res['leading_zero_term'] else None
    c0 = time.process_time()
    try:
        res['mu_a'] = eng.mu_asym(float(spec.get('mu_scale', 1.0)) * 3.0)
    except Exception as e:  # noqa: BLE001
        res['mu_a'] = None; res['mu_a_error'] = repr(e)[:300]
    res['mu_a_cpu_s'] = time.process_time() - c0
    res['terms'] = pm.term_table(eng.spec); res['notes'] = eng.spec.get('meta', {}).get('notes')
    res['workspace'] = dict(eng.ws)
    dump(out, res)
    log.info('check %s: %d parameters, gen_check %.2g, mu_a %s, leading zero term %s, f0 %.3f', specname,
             res['n_par'], res['gen_check'], res['mu_a'], res['leading_zero_term'], res['predictive']['f0'])


def mode_limit(out, specname, settings, seed, ntoys, quantiles, budget, priors):
    """The recipe R9 for every quantile in `quantiles`, resumable from prior output files of the same mode."""
    import p3d_specs
    st = parse_settings(settings); set_backend(st['tol'])
    spec = p3d_specs.get(specname)
    eng = Engine(spec, st)
    t0 = time.time()
    pts = []; mu_a = None
    for f in priors:
        d = json.load(open(f))
        pts += d['points']; mu_a = d['mu_a']
    if mu_a is None:
        mu_a = eng.mu_asym(float(spec.get('mu_scale', 1.0)) * 3.0)
    res = dict(versions(), mode='limit', spec=specname, settings=st, seed=seed, ntoys=ntoys, mu_a=mu_a,
               quantiles=quantiles, n_par=eng.nparams(), priors=[os.path.basename(f) for f in priors])
    new = []
    done = set(round(p['mu'], 9) for p in pts)
    for g in GRID:                                   # the frozen grid first
        m = mu_a * g
        if round(m, 9) not in done:
            if time.time() - t0 > budget:
                break
            rec = eng.point(m, ntoys, seed, st['a']); pts.append(rec); new.append(rec); done.add(round(m, 9))
    status = {}; tried = {}
    while time.time() - t0 < budget:
        nxt = None
        for p in quantiles:
            for rule in (('ecdf', 'npmedian') if p == 0.5 else ('ecdf',)):
                s = limit_status([(r['mu'], counts_of(r, p, rule)) for r in pts])
                status[f'{p}|{rule}'] = s
                if s['status'] in ('extend_up', 'extend_down', 'refine') and nxt is None:
                    nxt = s['next']
        if nxt is None or len(pts) > 40:
            break
        key = round(nxt, 9)
        if tried.get(key, 0) >= 2:                   # unresolved twice: the refinement stops (recipe step 5)
            res['stopped_unresolved'] = nxt
            break
        rec = eng.point(nxt, ntoys, seed + tried.get(key, 0), st['a']); pts.append(rec); new.append(rec)
        tried[key] = tried.get(key, 0) + 1
    for p in quantiles:
        for rule in (('ecdf', 'npmedian') if p == 0.5 else ('ecdf',)):
            cs = [(r['mu'], counts_of(r, p, rule)) for r in pts]
            s = limit_status(cs)
            s['frozen_grid_value'] = limit_frozen([(r['mu'], counts_of(r, p, rule)) for r in pts
                                                   if any(abs(r['mu'] / mu_a / g - 1) < 1e-9 for g in GRID)])
            s['variants'] = {e: limit_status(cs, empty=e).get('mu95') for e in ('k1139', 'k05')}
            status[f'{p}|{rule}'] = s
    res['status'] = status; res['points'] = new
    res['complete'] = all(s['status'] == 'ok' for s in status.values())
    res['fit_cpu_s'] = eng.cpu_fit; res['guard_cpu_s'] = eng.cpu_guard; res['n_fits'] = eng.nfit
    dump(out, res)
    log.info('limit %s: %s', specname, {k: (v['status'], v.get('mu95')) for k, v in status.items()})


def mode_store(out, specname, settings, seed, ntoys, fid, mprime, mus):
    import p3d_specs
    st = parse_settings(settings); set_backend(st['tol'])
    spec = p3d_specs.get(specname)
    eng = Engine(spec, st)
    aux = eng.ex.m.copy(); aux[eng.ex.fids.index(fid)] = mprime
    res = dict(versions(), mode='store', spec=specname, settings=st, seed=seed, ntoys=ntoys, fid=fid, mprime=mprime,
               n_par=eng.nparams(), points=[])
    for mu in mus:
        res['points'].append(eng.point(mu, ntoys, seed + 1000 * int(mprime), st['a'], aux_m=aux))
    res['fit_cpu_s'] = eng.cpu_fit; res['guard_cpu_s'] = eng.cpu_guard
    dump(out, res)


def mode_cover(out, specname, settings, seed, fid, mu_true, lams, npe, stores, readings=('A', 'B'),
               extra=None):
    """Coverage pseudo-experiments (T1-c (iii), (v)): true signal mu_true, true rate lambda for the leading zero-count
    factor `fid` with its simulated count redrawn m' ~ Pois(lambda); other counted rates at m + 1 (their counts not
    redrawn); nuisances drawn from their constraint (reading A) or at 0 (reading B).  Each pseudo-experiment's limit
    uses the stored distributions at its m'.  covered = mu95 >= mu_true, i.e. CLs > 0.05 at every stored mu <= mu_true
    (exact: mu_true is a stored grid value)."""
    import p3d_specs
    st = parse_settings(settings); set_backend(st['tol'])
    spec = p3d_specs.get(specname)
    eng = Engine(spec, st)
    ex = eng.ex; j = ex.fids.index(fid)
    dist = {}
    for f in stores:
        d = json.load(open(f))
        for p in d['points']:
            dist.setdefault(int(d['mprime']), {})[round(p['mu'], 9)] = (_a(p['qb']), _a(p['qsb']), p)
    res = dict(versions(), mode='cover', spec=specname, settings=st, seed=seed, fid=fid, mu_true=mu_true, lams=lams,
               npe=npe, n_par=eng.nparams(), rows=[])
    lam_true0 = np.where(ex.fixed, ex.fixval, ex.m + 1.0)
    for lam in lams:
        for rd in readings:
            rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(round(lam * 1000)), ord(rd)]))
            lt = lam_true0.copy(); lt[j] = lam
            mp = rng.poisson(lam, size=npe)
            n, _, th = eng.draw(mu_true, npe, rng, st['a'], lam_true=lt, th_mode='zero' if rd == 'B' else 'draw')
            row = dict(lam=lam, reading=rd, mprime=mp.tolist(), covered=[], mu95=[], missing_mprime=0, dropped=0)
            for i in range(npe):
                if int(mp[i]) not in dist:
                    row['missing_mprime'] += 1; row['covered'].append(None); row['mu95'].append(None); continue
                aux = ex.m.copy(); aux[j] = mp[i]
                dd = dist[int(mp[i])]
                mus = sorted(dd)
                eng.prev = None
                qo = []
                for mu in mus:
                    q, s, _ = eng.q(n[i], aux, mu, eng.gen_pars(mu_true, lt, th[i]))
                    qo.append(q)
                if not np.all(np.isfinite(qo)):
                    row['dropped'] += 1; row['covered'].append(None); row['mu95'].append(None); continue
                cl = [cls_at(dd[mu][0], dd[mu][1], [q])[0][0] for mu, q in zip(mus, qo)]
                ks = [int(cls_at(dd[mu][0], dd[mu][1], [q])[1][0]) for mu, q in zip(mus, qo)]
                cov = all(c > 0.05 for mu, c in zip(mus, cl) if mu <= mu_true * (1 + 1e-9))
                mu95 = None
                for a_ in range(len(mus) - 1):
                    if cl[a_] > 0.05 >= cl[a_ + 1]:
                        if ks[a_ + 1] == 0:
                            mu95 = mus[a_ + 1]
                        else:
                            l1, l2 = math.log(cl[a_]), math.log(cl[a_ + 1])
                            mu95 = mus[a_] + (math.log(0.05) - l1) * (mus[a_ + 1] - mus[a_]) / (l2 - l1)
                        break
                if mu95 is None:
                    mu95 = (mus[0] if cl[0] <= 0.05 else float('inf'))
                row['covered'].append(bool(cov)); row['mu95'].append(float(mu95))
            ok = [c for c in row['covered'] if c is not None]
            row['n'] = len(ok); row['k'] = int(sum(ok))
            m95 = np.array([x for x in row['mu95'] if x is not None], float)
            row['median_mu95_over_mu_true'] = float(np.median(m95) / mu_true) if len(m95) else None
            res['rows'].append(row)
            log.info('cover lam %.2f reading %s: %d of %d covered (missing m\' %d, dropped %d), median ratio %s',
                     lam, rd, row['k'], row['n'], row['missing_mprime'], row['dropped'],
                     row['median_mu95_over_mu_true'])
    if extra == 'bonly':                             # the analogue of STR l.1680 last column: s = 0, m' = 0, true lambda
        for lam in lams:
            rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(round(lam * 1000)), 98]))
            lt = lam_true0.copy(); lt[j] = lam
            n, _, th = eng.draw(0.0, npe, rng, st['a'], lam_true=lt)
            dd = dist[0]; mus = sorted(dd); m95 = []
            for i in range(npe):
                eng.prev = None
                qo = [eng.q(n[i], ex.m, mu, eng.gen_pars(0.0, lt, th[i]))[0] for mu in mus]
                cl = [cls_at(dd[mu][0], dd[mu][1], [q])[0][0] for mu, q in zip(mus, qo)]
                v = float('inf')
                for a_ in range(len(mus) - 1):
                    if cl[a_] > 0.05 >= cl[a_ + 1]:
                        l1, l2 = math.log(cl[a_]), math.log(max(cl[a_ + 1], 1e-300))
                        v = mus[a_] + (math.log(0.05) - l1) * (mus[a_ + 1] - mus[a_]) / (l2 - l1); break
                m95.append(v)
            res.setdefault('bonly', []).append(dict(lam=lam, median_mu95=float(np.median(m95)), mu95=m95))
    res['fit_cpu_s'] = eng.cpu_fit; res['guard_cpu_s'] = eng.cpu_guard; res['n_fits'] = eng.nfit
    dump(out, res)


def mode_cost(out, specname, settings, ntoys, mu):
    import p3d_specs
    st = parse_settings(settings); set_backend(st['tol'])
    spec = p3d_specs.get(specname)
    eng = Engine(spec, st)
    res = dict(versions(), mode='cost', spec=specname, settings=st, n_par=eng.nparams())
    rec = eng.point(mu, ntoys, 20261124, st['a'])
    res['point'] = {k: v for k, v in rec.items() if k not in ('qb', 'qsb')}
    res['cls'] = counts_of(rec, 0.5, 'ecdf')
    dump(out, res)


def main(argv):
    md = argv[0]
    if md == 'check':
        return mode_check(argv[1], argv[2], argv[3] if len(argv) > 3 else '')
    if md == 'limit':
        return mode_limit(argv[1], argv[2], argv[3], int(argv[4]), int(argv[5]),
                          [float(x) for x in argv[6].split(',')], float(argv[7]), argv[8:])
    if md == 'store':
        return mode_store(argv[1], argv[2], argv[3], int(argv[4]), int(argv[5]), argv[6], float(argv[7]),
                          [float(x) for x in argv[8].split(',')])
    if md == 'cover':
        return mode_cover(argv[1], argv[2], argv[3], int(argv[4]), argv[5], float(argv[6]),
                          [float(x) for x in argv[7].split(',')], int(argv[8]),
                          [a for a in argv[9:] if not a.startswith('--')],
                          extra='bonly' if '--bonly' in argv else None)
    if md == 'cost':
        return mode_cost(argv[1], argv[2], argv[3], int(argv[4]), float(argv[5]))
    raise SystemExit(f'unknown mode {md}')


if __name__ == '__main__':
    main(sys.argv[1:])
