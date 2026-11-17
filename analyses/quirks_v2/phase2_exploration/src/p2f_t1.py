"""p2f_t1.py -- T1 workspace builder (STR §4.11 pt 1), its v1 mode, and the check T1-b.  Executor Flora, 2026-11-17.
Builder and generation convention copied from p2c_t1.py (Tatiana) and p2v_toys.py (Viktor); neither file is edited.

BUILDER (for Phase 3 to extend)
  build(terms, nuis, signal, fixed=(), layout='merged', mu_max=1e5) -> (workspace, model)
    terms   [{name, kappa: {cat: float}, m: int, nuis: {name: log_width}}]   counted factors: free rate lambda_t
            (normfactor) constrained only by a Poisson auxiliary bin with observation m_t (zero allowed);
            kappa = N_t w / M_t, events per unit lambda
    nuis    {name: {'bound': theta_max or None}}   constrained nuisances (normsys, code1 = exp(width * theta));
            'bound' = the censoring bound ln(1/phi0)/s of a probability factor (STR l.1582-1584)
    signal  {'yield': {cat: S}, 'nuis': {name: log_width}}
    fixed   [{name, yield: {cat: B}, nuis: {name: log_width}}]   backgrounds with a nominal yield and log-normal
            nuisances only.  THIS IS THE v1-MODE SWITCH: v1 mode = terms == [] and one `fixed` entry per category
            with its own nuisance (v1_inputs() + v1_model()); the v2 treatment = `terms` filled, `fixed` empty.
    layout  'merged' (one 2-bin channel 'SR' + one multi-bin channel 'aux'; Viktor's validated layout) or 'std'
            (one channel per category and per auxiliary count; Tatiana's).  Same likelihood.
  The model must be created with modifier_settings={'normsys': {'interpcode': 'code1'}} (done here; it is NOT stored
  in the workspace JSON: a published workspace needs this setting stated beside it).
  Inputs of the v1 mode: v1_inputs('limits') reads the collapsed numbers of v1's limits.json (median and
  ln(B84/median) per category).  WHERE v2arith SHOULD ENTER: v1_inputs() is the only place that reads collapsed
  numbers; Phase 3 should build `terms`/`fixed` from v2arith.core (Factor, chain, Term, sample_sum) term by term, and
  for a v1-mode check take the medians and widths from v2arith.core.sample_sum on the v1 terms (the values in
  outputs/c1b_arith.json -> T1_input_schema.v2_*; v1_inputs('v2arith') reads them, diagnostic only).
  Backend: set_backend(name) -> pyhf 0.7.6, 'jax' (float64) or 'numpy', scipy optimiser (SLSQP).
  Tie tolerance: TIE_TOL = 1e-5 in cls_counts() ("q >= q_obs" is q >= q_obs - TIE_TOL; Viktor, TOY_COST §4).
  Zero s+b count: ZERO_K = 1.139 in limit_from_points() (plan §2.2 item 6).

MODES (all through the runner on a worker; plan and rules in logs/executor_flora_2026-11-17_08-21.md §2)
  setup   <out.json> <ws_out.json> [quick]        schema (T1-a), consistency checks, asymptotic scan, mu_a
  pt      <out.json> <backend> <mu> <ntoys> <seed> [conf]          one mu, both ensembles (conf: tol=..,newton_t=..)
  pair    <out.json> <jax.json> <numpy.json>                       paired comparison of two `pt` files
  vcheck  <out.json> <p2v_toys output>                             tie-tolerant CLs of a Viktor-format file
  t1b     <out.json> <mu_a> <seed> [ntoys=1000] [nrefine=6] [conf] the frozen procedure for one replica
  v1stat  <out.json> [ntoys=5000]                                  DIAGNOSTIC: v1's number-count statistic
  ref     <out.json> <mu_a> [ntoys=200000]                         DIAGNOSTIC: exact q~ on a large ensemble
  summary <out.json> <mu_a> <replica files ...>                    verdict by the rules fixed in the plan
"""
import json
import os
import sys
import time

for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
os.environ.setdefault('XLA_FLAGS', '--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1')

import logging  # noqa: E402
import resource  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402
from scipy.special import gammaln, ndtr  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p2f_t1')

CATS = ('SR_T', 'SR_G')
TIE_TOL = 1e-5            # ties in "q >= q_obs" (plan §2.2 item 3)
ZERO_K = 1.139            # count used for an empty s+b tail in the ln interpolation (plan §2.2 item 6; STR l.1615)
MAX_DROP = 0.02           # maximum dropped fraction per ensemble at a mu point (ruling 16 Nov 13:47)
ACC_ABS, ACC_REL = 1e-3, 1e-4     # accuracy rule of a pyhf fit against the exact one-dimensional profile
GRID = (0.4, 0.55, 0.75, 1.0, 1.35, 1.8, 2.5, 3.5)       # STR l.1640
MU_MAX = 1.0e5
GEN_TOL, NLL_TOL = 1e-9, 1e-5   # consistency with pyhf: expected counts (relative); twice-NLL relative to max(1, |t|)
                                # (lgamma(n + 1) reaches 1e10 at the largest counts, so 1e-16 relative is 1e-6 absolute)
TH_LO, TH_HI = -5.0, 5.0  # pyhf default bounds of a normsys parameter
REPO = Path(__file__).resolve().parents[4]
AN1 = REPO / 'stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1'
C1B = Path(__file__).resolve().parents[1] / 'outputs' / 'c1b_arith.json'
V1_POINT = 'A2|F|200|1.5|BM'
V1_NORM = 15775.0         # events before selection per unit mu (STR l.192, l.1729)
SEEDS = tuple(2026111701 + i for i in range(10))          # plan §2.2 item 9

pyhf = None


CONF = dict(tol=None, newton_t=0)     # tol: SLSQP tolerance (None = pyhf/scipy default 1e-6); newton_t: 1 = the SR-T
#                                       start value gets one Newton step (closed form) so that its gradient vanishes


def set_conf(text):
    for kv in (text or '').split(','):
        if kv and kv != '-':
            k, v = kv.split('=')
            CONF[k] = float(v) if k == 'tol' else int(v)


def set_backend(name):
    global pyhf
    import pyhf as _p
    pyhf = _p
    kw = {} if CONF['tol'] is None else dict(tolerance=CONF['tol'])
    pyhf.set_backend(name, pyhf.optimize.scipy_optimizer(**kw))
    return pyhf.tensorlib


def dump(out, res):
    with open(out + '.tmp', 'w') as f:
        json.dump(res, f)
    os.replace(out + '.tmp', out)


# ================================================================================================ builder
def _normsys(ws):
    return [{'name': n, 'type': 'normsys', 'data': {'hi': float(np.exp(w)), 'lo': float(np.exp(-w))}}
            for n, w in ws.items()]


def build(terms, nuis, signal, fixed=(), layout='merged', mu_max=MU_MAX):
    """See the module docstring.  Returns (pyhf.Workspace, model)."""
    channels = []; obs = []
    lam = lambda t: {'name': 'lam_' + t['name'], 'type': 'normfactor', 'data': None}      # noqa: E731
    mu = {'name': 'mu', 'type': 'normfactor', 'data': None}
    if layout == 'std':
        for c in CATS:
            samples = [{'name': 'signal', 'data': [float(signal['yield'][c])],
                        'modifiers': [mu] + _normsys(signal['nuis'])}]
            for t in terms:
                if t['kappa'].get(c, 0.0) > 0:
                    samples.append({'name': t['name'], 'data': [float(t['kappa'][c])],
                                    'modifiers': [lam(t)] + _normsys(t['nuis'])})
            for fb in fixed:
                if fb['yield'].get(c, 0.0) > 0:
                    samples.append({'name': fb['name'], 'data': [float(fb['yield'][c])],
                                    'modifiers': _normsys(fb['nuis'])})
            channels.append({'name': c, 'samples': samples}); obs.append({'name': c, 'data': [0.0]})
        for t in terms:
            channels.append({'name': 'aux_' + t['name'],
                             'samples': [{'name': 'count', 'data': [1.0], 'modifiers': [lam(t)]}]})
            obs.append({'name': 'aux_' + t['name'], 'data': [float(t['m'])]})
    elif layout == 'merged':
        samples = [{'name': 'signal', 'data': [float(signal['yield'][c]) for c in CATS],
                    'modifiers': [mu] + _normsys(signal['nuis'])}]
        for t in terms:
            samples.append({'name': t['name'], 'data': [float(t['kappa'].get(c, 0.0)) for c in CATS],
                            'modifiers': [lam(t)] + _normsys(t['nuis'])})
        for fb in fixed:
            samples.append({'name': fb['name'], 'data': [float(fb['yield'].get(c, 0.0)) for c in CATS],
                            'modifiers': _normsys(fb['nuis'])})
        channels.append({'name': 'SR', 'samples': samples}); obs.append({'name': 'SR', 'data': [0.0, 0.0]})
        if terms:
            n = len(terms)
            aux = [{'name': t['name'], 'data': [1.0 if j == i else 0.0 for j in range(n)], 'modifiers': [lam(t)]}
                   for i, t in enumerate(terms)]
            channels.append({'name': 'aux', 'samples': aux})
            obs.append({'name': 'aux', 'data': [float(t['m']) for t in terms]})
    else:
        raise ValueError(layout)
    pars = [{'name': 'mu', 'bounds': [[0.0, float(mu_max)]], 'inits': [1.0]}]
    for t in terms:
        pars.append({'name': 'lam_' + t['name'], 'bounds': [[1e-9, 10.0 * (t['m'] + 5.0)]], 'inits': [t['m'] + 1.0]})
    for n, d in nuis.items():
        if d.get('bound') is not None:
            pars.append({'name': n, 'bounds': [[TH_LO, float(d['bound'])]], 'inits': [0.0]})
    spec = {'version': '1.0.0', 'channels': channels, 'observations': obs,
            'measurements': [{'name': 'qv2', 'config': {'poi': 'mu', 'parameters': pars}}]}
    ws = pyhf.Workspace(spec)
    model = ws.model(modifier_settings={'normsys': {'interpcode': 'code1'}})
    return ws, model


def v1_inputs(source='limits'):
    """Collapsed v1 numbers of the best point: S per unit mu, median background and log width per category."""
    lim = json.loads((AN1 / 'limits.json').read_text())['points'][V1_POINT]
    d = dict(point=V1_POINT, eff=lim['s'], s=[e * V1_NORM for e in lim['s']], b=list(lim['b']),
             sig=list(lim['sigma_ln']), mu95_v1_toys=lim['expected_toys']['median'] / V1_NORM,
             mu95_v1_asym=lim['expected_asymptotic']['median'] / V1_NORM, source=source)
    if source == 'v2arith':        # diagnostic: the same v1 terms summed by v2arith's own Monte Carlo
        sch = json.loads(C1B.read_text())['T1_input_schema']
        d['b'] = list(sch['v2_median']); d['sig'] = list(sch['v2_ln_B84_over_median'])
    return d


def v1_model(inp, layout='merged'):
    """v1 mode: one log-normal background per category, uncorrelated (STR l.1727-1728)."""
    fixed = [{'name': f'bkg_{c}', 'yield': {c: inp['b'][i]}, 'nuis': {f'bkg_own_{c}': inp['sig'][i]}}
             for i, c in enumerate(CATS)]
    nuis = {f'bkg_own_{c}': {'bound': None} for c in CATS}
    signal = {'yield': {c: inp['s'][i] for i, c in enumerate(CATS)}, 'nuis': {}}
    return build([], nuis, signal, fixed=fixed, layout=layout)


# ================================================================================================ exact profile (numpy)
def tnll_bin(n, lam, th):
    """Twice the negative log-likelihood of one category in pyhf's normalisation (Poisson pmf x unit Gaussian)."""
    return 2.0 * (lam - n * np.log(lam) + gammaln(n + 1.0)) + th * th + np.log(2.0 * np.pi)


def ref_bin(n, a, b, sig, ngrid=257, chunk=20000):
    """min over theta in [TH_LO, TH_HI] of tnll_bin(n, a + b exp(sig theta), theta); vectorised over n (and a).
    Coarse grid, then bisection on the derivative g = sig lam_b (1 - n/lam) + theta in the two cells around the
    grid minimum.  Returns (theta, twice_nll, n_anomalies)."""
    n = np.atleast_1d(np.asarray(n, float)); a = np.broadcast_to(np.asarray(a, float), n.shape)
    grid = np.linspace(TH_LO, TH_HI, ngrid); eg = b * np.exp(sig * grid)
    th = np.empty(n.shape); anom = 0

    def g(t, nn, aa):
        lb = b * np.exp(sig * t)
        return sig * lb * (1.0 - nn / (aa + lb)) + t
    for i0 in range(0, len(n), chunk):
        nn = n[i0:i0 + chunk]; aa = a[i0:i0 + chunk]
        lam = aa[:, None] + eg[None, :]
        f = lam - nn[:, None] * np.log(lam) + 0.5 * grid[None, :] ** 2
        k = f.argmin(1)
        lo = grid[np.maximum(k - 1, 0)]; hi = grid[np.minimum(k + 1, ngrid - 1)]
        glo, ghi = g(lo, nn, aa), g(hi, nn, aa)
        l, h = lo.copy(), hi.copy()
        for _ in range(70):
            m = 0.5 * (l + h)
            up = g(m, nn, aa) > 0
            h = np.where(up, m, h); l = np.where(up, l, m)
        t = np.where(glo >= 0, lo, np.where(ghi <= 0, hi, 0.5 * (l + h)))
        anom += int(np.sum((glo >= 0) & (lo > TH_LO)) + np.sum((ghi <= 0) & (hi < TH_HI)))
        th[i0:i0 + chunk] = t
    return th, tnll_bin(n, a + b * np.exp(sig * th), th), anom


class V1Truth:
    """Generation and exact profiles of the v1-mode model (numpy).  Requires S_T = 0 (true at v1's best point):
    then the categories decouple, SR-T cancels in q~ and each profile is one-dimensional."""

    def __init__(self, inp, mu_max=MU_MAX):
        self.s = np.array(inp['s'], float); self.b = np.array(inp['b'], float); self.sig = np.array(inp['sig'], float)
        self.mu_max = mu_max
        if self.s[0] != 0.0 or self.s[1] <= 0.0:
            raise SystemExit('V1Truth needs S_T = 0 and S_G > 0')

    def expected(self, mu, th):
        return mu * self.s + self.b * np.exp(self.sig * th)

    def draw(self, mu, ntoys, rng):
        """theta (N, 2) in the order (T, G) from N(0, 1), then n (N, 2) Poisson (plan §2.2 item 8)."""
        th = rng.standard_normal((ntoys, 2))
        return rng.poisson(self.expected(mu, th)).astype(float), th

    def ref_fixed_G(self, n_g, mu):
        return ref_bin(n_g, mu * self.s[1], self.b[1], self.sig[1])

    def ref_free_G(self, n_g):
        n_g = np.atleast_1d(np.asarray(n_g, float))
        s, b, sig = self.s[1], self.b[1], self.sig[1]
        mu_un = (n_g - b) / s
        muhat = np.clip(mu_un, 0.0, self.mu_max)
        th = np.zeros(n_g.shape); t2 = tnll_bin(n_g, np.maximum(n_g, 1e-300), 0.0)     # n >= b: perfect fit
        sel = (mu_un < 0) | (mu_un > self.mu_max)
        anom = 0
        if sel.any():
            th[sel], t2[sel], anom = ref_bin(n_g[sel], muhat[sel] * s, b, sig)
        return muhat, th, t2, anom

    def ref_T(self, n_t):
        return ref_bin(n_t, 0.0, self.b[0], self.sig[0])

    def q_ref(self, n_g, mu):
        """Exact q~_mu (SR-G only; SR-T cancels)."""
        _, t_fix, a1 = self.ref_fixed_G(n_g, mu)
        muhat, _, t_free, a2 = self.ref_free_G(n_g)
        return np.where(muhat > mu, 0.0, np.clip(t_fix - t_free, 0.0, None)), a1 + a2

    def starts(self, n, mu):
        """Closed-form start values of the two pyhf fits (plan §2.2 item 1): (th_T, th_G fixed, mu free, th_G free)."""
        c = lambda x: float(np.clip(x, -4.9, 4.9))                                      # noqa: E731
        th_t = c(np.log(max(n[0], 0.5) / self.b[0]) / self.sig[0])
        if CONF['newton_t'] and n[0] >= 1:      # d/dtheta of (lam - n ln lam + theta^2/2) at lam = n is theta
            th_t = c(th_t - th_t / (self.sig[0] ** 2 * n[0] + 1.0))
        thg_fix = c(np.log(max(n[1] - mu * self.s[1], 0.5) / self.b[1]) / self.sig[1])
        if n[1] >= self.b[1]:
            mu0 = min((n[1] - self.b[1]) / self.s[1], 0.999 * self.mu_max)
            thg_free = c(np.log(max(n[1] - mu0 * self.s[1], 0.5) / self.b[1]) / self.sig[1])
        else:
            mu0 = 0.0; thg_free = c(np.log(max(n[1], 0.5) / self.b[1]) / self.sig[1])
        return th_t, thg_fix, mu0, thg_free


class Fitter:
    """q~_mu from two pyhf fits (fixed_poi_fit with do_stitch, fit) and pyhf's own _qmu_like formula."""

    def __init__(self, model, truth, layout='merged'):
        self.model, self.truth, self.layout = model, truth, layout
        cfg = model.config
        self.cfg = cfg
        self.i_mu = cfg.poi_index
        self.i_t = cfg.par_slice('bkg_own_SR_T').start; self.i_g = cfg.par_slice('bkg_own_SR_G').start
        self.bounds = [list(b) for b in cfg.suggested_bounds()]; self.fixed = list(cfg.suggested_fixed())
        self.aux = np.asarray(cfg.auxdata, float)
        self.tl = pyhf.tensorlib
        self.cpu = 0.0; self.nfit = 0

    def data(self, n):
        if self.layout == 'merged':
            main = np.array([n[0], n[1]], float)
        else:
            main = np.concatenate([[n[CATS.index(c)]] for c in self.cfg.channels]).astype(float)
        return self.tl.astensor(np.concatenate([main, self.aux]))

    def pars(self, mu, th_t, th_g):
        p = np.array(self.cfg.suggested_init(), float)
        p[self.i_mu] = mu; p[self.i_t] = th_t; p[self.i_g] = th_g
        return p

    def two_fits(self, n, mu, init_fix, init_free):
        d = self.data(n)
        c0 = time.process_time()
        pf, t_fix = pyhf.infer.mle.fixed_poi_fit(mu, d, self.model, list(init_fix), self.bounds, self.fixed,
                                                 return_fitted_val=True, do_stitch=True)
        pu, t_free = pyhf.infer.mle.fit(d, self.model, list(init_free), self.bounds, self.fixed,
                                        return_fitted_val=True)
        self.cpu += time.process_time() - c0; self.nfit += 2
        t_fix, t_free = float(t_fix), float(t_free)
        muhat = float(self.tl.tolist(pu)[self.i_mu])
        q = 0.0 if muhat > mu else max(t_fix - t_free, 0.0)
        return q, t_fix, t_free, muhat

    def q_toy(self, n, mu, th_gen, mu_gen, q_ref):
        """Plan §2.2 items 1-2.  Returns (q or nan, status 0 ok / 1 retried / 2 dropped, reason bits of the first
        attempt: 1 exception, 2 inaccurate; q of the first attempt or nan)."""
        tr = self.truth
        th_t, thg_fix, mu0, thg_free = tr.starts(n, mu)
        reason = 0; q1 = float('nan')
        try:
            q1 = self.two_fits(n, mu, self.pars(mu, th_t, thg_fix), self.pars(mu0, th_t, thg_free))[0]
            if abs(q1 - q_ref) <= max(ACC_ABS, ACC_REL * abs(q_ref)):
                return q1, 0, 0, q1
            reason = 2
        except Exception:  # noqa: BLE001 - counted, retried once, then dropped (ruling 16 Nov 13:47)
            reason = 1
        c = lambda x: float(np.clip(x, -4.9, 4.9))                                      # noqa: E731
        tt, tg = c(th_gen[0]), c(th_gen[1])
        mu_s = float(np.clip((n[1] - tr.b[1] * np.exp(tr.sig[1] * tg)) / tr.s[1], 0.0, 0.999 * tr.mu_max))
        try:
            q2 = self.two_fits(n, mu, self.pars(mu, tt, tg), self.pars(mu_s, tt, tg))[0]
            if abs(q2 - q_ref) <= max(ACC_ABS, ACC_REL * abs(q_ref)):
                return q2, 1, reason, q1
        except Exception:  # noqa: BLE001
            pass
        return float('nan'), 2, reason, q1

    def q_asimov(self, mu):
        """q~_mu on the b-only Asimov data (n = b, auxiliary data 0) from the same two pyhf fits."""
        tr = self.truth
        n = tr.b.copy()
        th_t, thg_fix, mu0, thg_free = tr.starts(n, mu)
        q, t_fix, t_free, muhat = self.two_fits(n, mu, self.pars(mu, th_t, thg_fix), self.pars(mu0, th_t, thg_free))
        return q


def cls_asym(q_a):
    """Median expected CLs of the asymptotic q~ calculator: CLs+b = 1 - Phi(sqrt(qA)), CLb = 0.5."""
    return 2.0 * (1.0 - float(ndtr(np.sqrt(max(q_a, 0.0)))))


def consistency(model, fitter, truth, rng):
    """Generation formula and likelihood normalisation against pyhf at random parameter points."""
    tl = pyhf.tensorlib
    worst_e = worst_n = 0.0
    for _ in range(5):
        mu = float(rng.uniform(0, 2000)); th = rng.standard_normal(2)
        p = fitter.pars(mu, th[0], th[1])
        e_p = np.asarray(tl.tolist(model.expected_actualdata(tl.astensor(p))), float)
        e_t = truth.expected(mu, th)
        if fitter.layout != 'merged':
            e_t = np.array([e_t[CATS.index(c)] for c in model.config.channels])
        worst_e = max(worst_e, float(np.max(np.abs(e_p / e_t - 1))))
        n = rng.poisson(truth.expected(mu, th)).astype(float)
        t_p = float(np.asarray(tl.tolist(pyhf.infer.mle.twice_nll(tl.astensor(p), fitter.data(n), model))).ravel()[0])
        lam = truth.expected(mu, th)
        t_t = float(np.sum(tnll_bin(n, lam, th)))
        worst_n = max(worst_n, abs(t_p - t_t) / max(1.0, abs(t_t)))
    return worst_e, worst_n


# ================================================================================================ CLs and the limit
def cls_counts(qb, qsb, tol=TIE_TOL, which='median'):
    """Counts of the CLs estimate at one mu.  qb, qsb: arrays with nan for dropped toys."""
    qb = np.asarray(qb, float); qsb = np.asarray(qsb, float)
    nb_all, nsb_all = len(qb), len(qsb)
    qb = qb[np.isfinite(qb)]; qsb = qsb[np.isfinite(qsb)]
    if len(qb) == 0 or len(qsb) == 0:
        return dict(resolved=False, drop_b=1.0, drop_sb=1.0, nb=0, nsb=0, kb=0, ksb=0, q_obs=None)
    srt = np.sort(qb)
    if which == 'median':
        q_obs = float(np.median(srt))
    elif which == 'lower':
        q_obs = float(srt[(len(srt) - 1) // 2])
    else:
        q_obs = float(srt[len(srt) // 2])
    ksb = int(np.sum(qsb >= q_obs - tol)); kb = int(np.sum(qb >= q_obs - tol))
    drop_b = 1.0 - len(qb) / nb_all; drop_sb = 1.0 - len(qsb) / nsb_all
    return dict(q_obs=q_obs, ksb=ksb, nsb=int(len(qsb)), kb=kb, nb=int(len(qb)), drop_b=drop_b, drop_sb=drop_sb,
                resolved=bool(drop_b <= MAX_DROP and drop_sb <= MAX_DROP))


def cls_value(c, zero_k=ZERO_K):
    """(CLs, relative binomial error, zero flag) from the counts; an empty s+b tail is replaced by zero_k counts."""
    zero = c['ksb'] == 0
    k = zero_k if zero else float(c['ksb'])
    psb = k / c['nsb']; pb1 = c['kb'] / c['nb']
    rel = np.sqrt(max(1.0 - psb, 0.0) / k + max(1.0 - pb1, 0.0) / max(c['kb'], 1))
    return psb / pb1, float(rel), bool(zero)


def limit_from_points(points, zero_k=ZERO_K, interp='log'):
    """points: [(mu, counts)].  STR l.1641-1643 with the choices of plan §2.2 items 6-7.  Returns a dict with status
    'ok' | 'extend_up' | 'extend_down' | 'unresolved'."""
    pts = sorted([(m, c) for m, c in points if c['resolved']], key=lambda x: x[0])
    n_unres = len(points) - len(pts)
    if len(pts) < 2:
        return dict(status='unresolved', n_unresolved=n_unres)
    v = [cls_value(c, zero_k) for _, c in pts]
    if v[0][0] <= 0.05:
        return dict(status='extend_down', n_unresolved=n_unres)
    for i in range(len(pts) - 1):
        if v[i][0] > 0.05 >= v[i + 1][0]:
            m1, m2 = pts[i][0], pts[i + 1][0]
            if interp == 'log':
                l1, l2, L = np.log(v[i][0]), np.log(v[i + 1][0]), np.log(0.05)
                e1, e2 = v[i][1], v[i + 1][1]
            else:                               # diagnostic: linear in CLs, a zero count stays zero
                c1 = v[i][0]; c2 = 0.0 if v[i + 1][2] else v[i + 1][0]
                l1, l2, L = c1, c2, 0.05
                e1, e2 = v[i][1] * c1, v[i + 1][1] * c2
            mu95 = m1 + (L - l1) * (m2 - m1) / (l2 - l1)
            d1 = (m2 - m1) * (L - l2) / (l2 - l1) ** 2; d2 = -(m2 - m1) * (L - l1) / (l2 - l1) ** 2
            err = float(np.hypot(d1 * e1, d2 * e2))
            # the unresolved points lying inside the bracket invalidate it (the crossing is "not used" there)
            inside = [m for m, c in points if not c['resolved'] and m1 < m < m2]
            return dict(status='ok' if not inside else 'unresolved', mu95=float(mu95), err_binomial=err,
                        bracket=[float(m1), float(m2)], cls_bracket=[v[i][0], v[i + 1][0]],
                        zero_upper=v[i + 1][2], n_unresolved=n_unres)
    return dict(status='extend_up', n_unresolved=n_unres)


# ================================================================================================ modes
def ensembles(fit, truth, mu, ntoys, seed):
    """Both ensembles at one mu (plan §2.2 item 8).  Returns the per-mu record."""
    rec = dict(mu=float(mu), ntoys=ntoys, seed=seed)
    for e, (lab, mu_gen) in enumerate((('b', 0.0), ('sb', mu))):
        rng = np.random.default_rng([seed, int(round(1000 * mu)), e])
        n, th = truth.draw(mu_gen, ntoys, rng)
        q_ref, anom = truth.q_ref(n[:, 1], mu)
        c0, f0 = fit.cpu, fit.nfit
        t0 = time.process_time()
        q = np.empty(ntoys); st = np.empty(ntoys, int); rs = np.empty(ntoys, int); q1 = np.empty(ntoys)
        for i in range(ntoys):
            q[i], st[i], rs[i], q1[i] = fit.q_toy(n[i], mu, th[i], mu_gen, float(q_ref[i]))
        ok = np.isfinite(q)
        rec[lab] = dict(q=[None if not o else float(x) for x, o in zip(q, ok)], q_ref=q_ref.tolist(),
                        q_first=[None if not np.isfinite(x) else float(x) for x in q1],
                        status=st.tolist(), reason=rs.tolist(), n_G=n[:, 1].tolist(),
                        retried=int(np.sum(st == 1)), dropped=int(np.sum(st == 2)),
                        first_exception=int(np.sum(rs == 1)), first_inaccurate=int(np.sum(rs == 2)),
                        max_abs_dq=float(np.max(np.abs(q[ok] - q_ref[ok]))) if ok.any() else None,
                        ref_anomalies=int(anom), fit_cpu_s=fit.cpu - c0, n_fits=fit.nfit - f0,
                        loop_cpu_s=time.process_time() - t0)
    qb = np.array([np.nan if x is None else x for x in rec['b']['q']])
    qs = np.array([np.nan if x is None else x for x in rec['sb']['q']])
    rec['counts'] = cls_counts(qb, qs)
    rec['fit_cpu_s_per_1000_plus_1000'] = 1000.0 * (rec['b']['fit_cpu_s'] + rec['sb']['fit_cpu_s']) / ntoys
    rec['loop_cpu_s_per_1000_plus_1000'] = 1000.0 * (rec['b']['loop_cpu_s'] + rec['sb']['loop_cpu_s']) / ntoys
    c = rec['counts']
    log.info('mu %.3f: ksb %s/%s kb %s/%s q_obs %s dropped b %d sb %d retried %d %d; %.1f s fits per 1000+1000',
             mu, c.get('ksb'), c.get('nsb'), c.get('kb'), c.get('nb'), c.get('q_obs'), rec['b']['dropped'],
             rec['sb']['dropped'], rec['b']['retried'], rec['sb']['retried'], rec['fit_cpu_s_per_1000_plus_1000'])
    return rec


def versions():
    import scipy
    v = dict(pyhf=pyhf.__version__, numpy=np.__version__, scipy=scipy.__version__, host=os.uname().nodename,
             backend=pyhf.tensorlib.name, conf=dict(CONF))
    try:
        import jax
        v['jax'] = jax.__version__
    except ImportError:
        pass
    return v


def asym_root(fit, truth, lo=700.0):
    hi = truth.b[1] / truth.s[1] * (1.0 - 1e-3)       # CLs_asym = 0.011 there
    f = lambda m: cls_asym(fit.q_asimov(m)) - 0.05                                    # noqa: E731
    return float(brentq(f, lo, hi, xtol=1e-3, rtol=1e-12))


def mode_setup(out, ws_out, quick=False):
    set_backend('jax')
    res = dict(versions(), mode='setup')
    inp = v1_inputs('limits')
    res['inputs'] = inp
    truth = V1Truth(inp)
    rng = np.random.default_rng(424242)
    for layout in ('merged', 'std'):
        ws, model = v1_model(inp, layout)
        pyhf.schema.validate(ws, 'workspace.json')            # T1-a: raises if the workspace is not schema-valid
        fit = Fitter(model, truth, layout)
        we, wn = consistency(model, fit, truth, rng)
        res[f'schema_valid_{layout}'] = True
        res[f'gen_check_{layout}'] = we; res[f'nll_check_{layout}'] = wn
        res[f'n_par_{layout}'] = model.config.npars
        res[f'par_order_{layout}'] = list(model.config.par_order)
        if layout == 'merged':
            with open(ws_out + '.tmp', 'w') as f:
                json.dump(dict(ws), f, indent=1)
            os.replace(ws_out + '.tmp', ws_out)
            fit_m = fit
    if max(res['gen_check_merged'], res['gen_check_std']) > GEN_TOL or max(res['nll_check_merged'], res['nll_check_std']) > NLL_TOL:
        dump(out, res)
        raise SystemExit('consistency check against pyhf failed')
    # check 1: Tatiana's scan (780..900 step 4) and her interpolation (linear in CLs between the bracketing points)
    scan = []
    for m in (np.arange(780.0, 900.1, 4.0) if not quick else np.arange(820.0, 836.1, 4.0)):
        qa = fit_m.q_asimov(float(m))
        qr = float(truth.q_ref(truth.b[1:2], float(m))[0][0])
        scan.append((float(m), cls_asym(qa), qa, qr))
    mu_interp = None
    for a, c in zip(scan[:-1], scan[1:]):
        if a[1] >= 0.05 > c[1]:
            mu_interp = float(a[0] + (a[1] - 0.05) * (c[0] - a[0]) / (a[1] - c[1])); break
    res['asym_scan'] = scan; res['mu_a_interp_4grid'] = mu_interp
    res['mu_a_root'] = asym_root(fit_m, truth)
    res['mu_a_root_exact_profile'] = float(brentq(
        lambda m: cls_asym(float(truth.q_ref(truth.b[1:2], m)[0][0])) - 0.05, 700.0,
        truth.b[1] / truth.s[1] * (1 - 1e-3), xtol=1e-6))
    res['mu95_v1_asym'] = inp['mu95_v1_asym']; res['mu95_v1_toys'] = inp['mu95_v1_toys']
    # cross-check with pyhf's own asymptotic calculator (default start values; may fail, recorded)
    hyp = []
    asimov = fit_m.data(truth.b)
    for m in (780.0, 820.0, 828.0):
        try:
            r = pyhf.infer.hypotest(m, asimov, fit_m.model, test_stat='qtilde', return_expected=True)
            hyp.append((m, float(r[1]), None))
        except Exception as e:  # noqa: BLE001
            hyp.append((m, None, repr(e)[:200]))
    res['pyhf_hypotest'] = hyp
    # diagnostic: the same with v2arith's own Monte Carlo of the v1 terms
    inp2 = v1_inputs('v2arith'); tr2 = V1Truth(inp2); _, m2 = v1_model(inp2)
    res['inputs_v2arith'] = dict(b=inp2['b'], sig=inp2['sig'])
    res['mu_a_root_v2arith_inputs'] = asym_root(Fitter(m2, tr2), tr2)
    res['fit_cpu_s'] = fit_m.cpu; res['n_fits'] = fit_m.nfit
    res['max_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    dump(out, res)
    log.info('setup: 4-grid interpolation %s, root %.4f (exact profile %.4f), v1 asymptotic %.4f', mu_interp,
             res['mu_a_root'], res['mu_a_root_exact_profile'], inp['mu95_v1_asym'])


def mode_pt(out, backend, mu, ntoys, seed):
    set_backend(backend)
    inp = v1_inputs('limits'); truth = V1Truth(inp)
    ws, model = v1_model(inp)
    fit = Fitter(model, truth)
    we, wn = consistency(model, fit, truth, np.random.default_rng(424242))
    res = dict(versions(), mode='pt', gen_check=we, nll_check=wn)
    res['point'] = ensembles(fit, truth, mu, ntoys, seed)
    res['max_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    dump(out, res)


def _qarr(x):
    return np.array([np.nan if v is None else v for v in x], float)


def mode_pair(out, fa, fb):
    a = json.load(open(fa)); b = json.load(open(fb))
    res = dict(mode='pair', a=dict(backend=a['backend'], file=os.path.basename(fa)),
               b=dict(backend=b['backend'], file=os.path.basename(fb)), mu=a['point']['mu'])
    worst = 0.0; nbad = 0; ntot = 0
    for lab in ('b', 'sb'):
        qa, qb = _qarr(a['point'][lab]['q']), _qarr(b['point'][lab]['q'])
        if a['point'][lab]['n_G'] != b['point'][lab]['n_G']:
            raise SystemExit('the two files do not hold the same pseudo-data')
        ok = np.isfinite(qa) & np.isfinite(qb)
        d = np.abs(qa[ok] - qb[ok]); tol = np.maximum(ACC_ABS, ACC_REL * np.abs(qa[ok]))
        res[lab] = dict(n=int(len(qa)), both_ok=int(ok.sum()), max_abs_dq=float(d.max()) if len(d) else None,
                        n_beyond_tol=int(np.sum(d > tol)), dropped_a=a['point'][lab]['dropped'],
                        dropped_b=b['point'][lab]['dropped'], retried_a=a['point'][lab]['retried'],
                        retried_b=b['point'][lab]['retried'])
        worst = max(worst, float(d.max()) if len(d) else 0.0); nbad += int(np.sum(d > tol)); ntot += int(ok.sum())
    ca, cb = a['point']['counts'], b['point']['counts']
    res['counts_a'] = ca; res['counts_b'] = cb
    res['cls_a'] = cls_value(ca)[0] if ca['nb'] else None; res['cls_b'] = cls_value(cb)[0] if cb['nb'] else None
    res['s_per_unit_a'] = a['point']['fit_cpu_s_per_1000_plus_1000']
    res['s_per_unit_b'] = b['point']['fit_cpu_s_per_1000_plus_1000']
    res['pass'] = bool(nbad == 0 and abs(ca['ksb'] - cb['ksb']) <= 1 and abs(ca['kb'] - cb['kb']) <= 1)
    dump(out, res)
    log.info('pair: max |dq| %.3g, %d of %d beyond tolerance, CLs %s vs %s, pass %s', worst, nbad, ntot, res['cls_a'],
             res['cls_b'], res['pass'])


def mode_vcheck(out, fv):
    d = json.load(open(fv))
    qb = _qarr(d['b']['q']); qs = _qarr(d['sb']['q'])
    c = cls_counts(qb, qs); c0 = cls_counts(qb, qs, tol=0.0)
    res = dict(mode='vcheck', file=os.path.basename(fv), config=d.get('config'), n_par=d.get('n_par'),
               mu=d.get('mu_test'), counts=c, cls_tie_tolerant=c['ksb'] / c['nsb'] / (c['kb'] / c['nb']),
               cls_raw=c0['ksb'] / c0['nsb'] / (c0['kb'] / c0['nb']), cls_in_file=d.get('cls'),
               s_per_unit=d.get('cpu_s_per_1000_sb_plus_1000_b'), expected=0.1372)
    res['pass'] = bool(abs(res['cls_tie_tolerant'] - 0.1372) <= 0.0005)
    dump(out, res)
    log.info('vcheck: CLs tie-tolerant %.4f raw %.4f (expected 0.1372), %.1f s per unit', res['cls_tie_tolerant'],
             res['cls_raw'], res['s_per_unit'] or -1)


def mode_t1b(out, mu_a, seed, ntoys=1000, nrefine=6):
    set_backend('jax')
    t_start = time.process_time()
    inp = v1_inputs('limits'); truth = V1Truth(inp)
    ws, model = v1_model(inp)
    pyhf.schema.validate(ws, 'workspace.json')
    fit = Fitter(model, truth)
    we, wn = consistency(model, fit, truth, np.random.default_rng(424242))
    if we > GEN_TOL or wn > NLL_TOL:
        raise SystemExit(f'consistency check against pyhf failed: {we} {wn}')
    res = dict(versions(), mode='t1b', mu_a=mu_a, seed=seed, ntoys=ntoys, gen_check=we, nll_check=wn,
               inputs=inp, grid_factors=list(GRID), tie_tol=TIE_TOL, zero_k=ZERO_K, max_drop=MAX_DROP)
    pts = [ensembles(fit, truth, mu_a * g, ntoys, seed) for g in GRID]
    lim = limit_from_points([(p['mu'], p['counts']) for p in pts])
    n_ext = 0
    while lim['status'] in ('extend_up', 'extend_down') and n_ext < 4:        # STR l.1642-1643
        mus = sorted(p['mu'] for p in pts)
        m_new = mus[-1] * 1.5 if lim['status'] == 'extend_up' else mus[0] / 1.5
        pts.append(ensembles(fit, truth, m_new, ntoys, seed)); n_ext += 1
        lim = limit_from_points([(p['mu'], p['counts']) for p in pts])
    res['points'] = pts; res['limit'] = lim; res['n_extensions'] = n_ext
    res['cpu_s_frozen'] = time.process_time() - t_start
    # DIAGNOSTIC (no verdict): bisection refinement of the bracket, 1000 + 1000 toys per step
    ref_pts = []
    if lim['status'] == 'ok' and nrefine > 0:
        lo, hi = lim['bracket']
        for _ in range(nrefine):
            if time.process_time() - t_start > 1100:       # stay inside the 30-minute job
                break
            mid = 0.5 * (lo + hi)
            p = ensembles(fit, truth, mid, ntoys, seed); ref_pts.append(p)
            c = p['counts']
            if c['resolved'] and cls_value(c)[0] > 0.05:
                lo = mid
            else:
                hi = mid
        res['refine_bracket'] = [lo, hi]
    res['refine_points'] = ref_pts
    res['cpu_s_total'] = time.process_time() - t_start
    res['fit_cpu_s'] = fit.cpu; res['n_fits'] = fit.nfit
    res['max_rss_mb'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    dump(out, res)
    log.info('t1b seed %d: %s', seed, lim)


def v1_limit_numbercount(s, b, own, ntoys, seed, order='v1', cl=0.95):
    """DIAGNOSTIC ONLY (no verdict): v1's statistic, copied from acts/stage4/analysis/stats.py l.216-258
    (expected_limit_toys, median only, no shared component): Q = sum_c n_c ln(1 + mu s_c / b_c), nuisances
    marginalised, common random numbers.  order='v1': the random-number order of v1 (one standard_normal(ntoys) per
    category); order='t': Tatiana's re-implementation (standard_normal((ntoys, 2)))."""
    rng = np.random.default_rng(seed)
    s = np.asarray(s, float); b = np.asarray(b, float)
    ln = np.zeros((ntoys, len(b)))
    if order == 'v1':
        for i in range(len(b)):
            ln[:, i] += own[i] * rng.standard_normal(ntoys)
    else:
        ln = np.asarray(own)[None, :] * rng.standard_normal((ntoys, len(b)))
    bt = b[None, :] * np.exp(ln)
    nb_obs = rng.poisson(bt); nb = rng.poisson(bt)

    def cls(mu):
        w = np.log1p(mu * s / np.maximum(b, 1e-12))
        nsb = np.random.default_rng([seed, 1]).poisson(bt + mu * s[None, :])
        qobs = float(np.quantile((nb_obs * w).sum(1), 0.5))
        clsb = np.mean((nsb * w).sum(1) <= qobs); clb = np.mean((nb * w).sum(1) <= qobs)
        return clsb / max(clb, 1e-12)
    lo, hi = 0.0, 1.0
    while cls(hi) > 1 - cl and hi < 1e16:
        hi *= 4
    lo = hi / 4 if hi > 1 else 0.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if cls(mid) > 1 - cl:
            lo = mid
        else:
            hi = mid
    return float(hi)


def mode_v1stat(out, ntoys=5000):
    inp = v1_inputs('limits')
    seeds = [20261014] + [2026111701 + i for i in range(11)]
    # v1's own units: s = efficiencies, mu in events before selection; divided by 15,775 afterwards
    v1o = [v1_limit_numbercount(inp['eff'], inp['b'], inp['sig'], ntoys, sd) / V1_NORM for sd in seeds]
    tseeds = [20261116, 20261117, 20261118, 20261014]
    to = [v1_limit_numbercount(inp['s'], inp['b'], inp['sig'], ntoys, sd, order='t') for sd in tseeds]
    a = np.array(v1o)
    res = dict(mode='v1stat', numpy=np.__version__, ntoys=ntoys, seeds=seeds, mu95=v1o, mu95_v1=inp['mu95_v1_toys'],
               reproduces_v1_seed=abs(v1o[0] - inp['mu95_v1_toys']), mean=float(a.mean()), sd=float(a.std(ddof=1)),
               mean_other=float(a[1:].mean()), sd_other=float(a[1:].std(ddof=1)), min=float(a.min()),
               max=float(a.max()), tatiana_order_seeds=tseeds, tatiana_order_mu95=to,
               tatiana_reported=[831.8091474633098, 814.2753628953337, 814.0169953159111, 794.3974736472547])
    # the same statistic with 10x the toys (how much of the scatter is toy noise)
    res['mu95_50000_toys'] = [v1_limit_numbercount(inp['eff'], inp['b'], inp['sig'], 10 * ntoys, sd) / V1_NORM
                              for sd in seeds[:4]]
    dump(out, res)
    log.info('v1stat: v1 seed %.3f (v1 %.3f); 12 seeds mean %.1f sd %.1f', v1o[0], inp['mu95_v1_toys'], res['mean'],
             res['sd'])


def mode_ref(out, mu_a, ntoys=200000):
    """DIAGNOSTIC (no verdict): CLs(mu) of the T1 statistic with the exact one-dimensional profiles, large ensembles."""
    inp = v1_inputs('limits'); truth = V1Truth(inp)
    edge = truth.b[1] / truth.s[1]
    mus = sorted({round(m, 4) for m in [0.4 * mu_a, 0.55 * mu_a, 0.75 * mu_a, 700.0, 760.0, 790.0, 810.0, 820.0, 824.0,
                                         826.0, 828.0, mu_a, 830.0, 831.0, 832.0, 832.5, 833.0, 836.0, 1.35 * mu_a]})
    rows = []
    for mu in mus:
        q = {}
        for e, mg in enumerate((0.0, mu)):
            rng = np.random.default_rng([777, int(round(1000 * mu)), e])
            n, _ = truth.draw(mg, ntoys, rng)
            q[e], _ = truth.q_ref(n[:, 1], mu)
        c = cls_counts(q[0], q[1])
        p_jump = float(ndtr(np.log(mu / edge) / truth.sig[1]))
        cls_cf = 2.0 * float(ndtr(np.log(1.0 - mu / edge) / truth.sig[1])) if mu < edge else 0.0
        rows.append(dict(mu=mu, counts=c, cls=c['ksb'] / c['nsb'] / (c['kb'] / c['nb']), p_jump_closed_form=p_jump,
                         cls_closed_form=cls_cf, frac_b_q_above_100=float(np.mean(q[0] > 100.0))))
        log.info('ref mu %.2f: CLs %.5f (closed form %.5f), q_obs %.4g', mu, rows[-1]['cls'], cls_cf, c['q_obs'])
    lim = limit_from_points([(r['mu'], r['counts']) for r in rows])
    dump(out, dict(mode='ref', ntoys=ntoys, mu_a=mu_a, edge_b_over_s=float(edge), rows=rows, limit_fine_grid=lim,
                   numpy=np.__version__))


def _replica_variants(rep):
    """Limits of one replica under the primary rules and the diagnostic variants (from the stored q)."""
    def pts(key='q', tol=TIE_TOL, which='median', drop='rule'):
        o = []
        for p in rep['points']:
            qb, qs = _qarr(p['b'][key]), _qarr(p['sb'][key])
            if drop == 'exc':        # exceptions only: keep the first-attempt value where the fit returned one
                qb = np.where(np.isfinite(_qarr(p['b']['q_first'])), _qarr(p['b']['q_first']), _qarr(p['b']['q']))
                qs = np.where(np.isfinite(_qarr(p['sb']['q_first'])), _qarr(p['sb']['q_first']), _qarr(p['sb']['q']))
            o.append((p['mu'], cls_counts(qb, qs, tol=tol, which=which)))
        return o
    v = dict(primary=limit_from_points(pts()))
    v['zero_k_0.5'] = limit_from_points(pts(), zero_k=0.5)
    v['zero_k_1'] = limit_from_points(pts(), zero_k=1.0)
    v['linear_cls'] = limit_from_points(pts(), interp='lin')
    v['tie_tol_0'] = limit_from_points(pts(tol=0.0))
    v['median_lower'] = limit_from_points(pts(which='lower'))
    v['median_upper'] = limit_from_points(pts(which='upper'))
    v['exceptions_only'] = limit_from_points(pts(drop='exc'))
    v['exact_q'] = limit_from_points(pts(key='q_ref'))
    allp = rep['points'] + rep.get('refine_points', [])
    o = [(p['mu'], cls_counts(_qarr(p['b']['q']), _qarr(p['sb']['q']))) for p in allp]
    v['refined'] = limit_from_points(o)
    return v


def verdict_of(mu, sig, lo, hi):
    if mu - sig >= lo and mu + sig <= hi:
        return 'PASS'
    if mu + sig < lo or mu - sig > hi:
        return 'FAIL'
    return 'STRADDLES'


def mode_summary(out, mu_a, files):
    inp = v1_inputs('limits')
    v1 = inp['mu95_v1_toys']; lo, hi = 0.9 * v1, 1.1 * v1
    reps = sorted((json.load(open(f)) for f in files), key=lambda r: r['seed'])      # SEEDS is ascending
    res = dict(mode='summary', mu_a=mu_a, mu95_v1=v1, window=[lo, hi], seeds=[r['seed'] for r in reps],
               rules=dict(tie_tol=TIE_TOL, zero_k=ZERO_K, max_drop=MAX_DROP, acc=[ACC_ABS, ACC_REL]))
    table = []; var = []
    for r in reps:
        v = _replica_variants(r); var.append(v)
        row = dict(seed=r['seed'], n_extensions=r['n_extensions'], primary=v['primary'],
                   variants={k: (x.get('mu95'), x['status']) for k, x in v.items()},
                   points=[dict(mu=p['mu'], counts=p['counts'], cls=(cls_value(p['counts'])[0] if p['counts']['nb'] else None),
                                dropped=[p['b']['dropped'], p['sb']['dropped']],
                                retried=[p['b']['retried'], p['sb']['retried']],
                                first_exception=[p['b']['first_exception'], p['sb']['first_exception']],
                                first_inaccurate=[p['b']['first_inaccurate'], p['sb']['first_inaccurate']],
                                max_abs_dq=[p['b']['max_abs_dq'], p['sb']['max_abs_dq']],
                                frac_b_on_jump=float(np.mean(np.array(p['b']['q_ref']) > 100.0)),
                                fit_s_per_unit=p['fit_cpu_s_per_1000_plus_1000'],
                                loop_s_per_unit=p['loop_cpu_s_per_1000_plus_1000']) for p in r['points']],
                   refine=[dict(mu=p['mu'], cls=(cls_value(p['counts'])[0] if p['counts']['nb'] else None),
                                ksb=p['counts']['ksb'], resolved=p['counts']['resolved']) for p in r.get('refine_points', [])],
                   refine_bracket=r.get('refine_bracket'), cpu_s_total=r['cpu_s_total'], cpu_s_frozen=r['cpu_s_frozen'],
                   n_fits=r['n_fits'], fit_cpu_s=r['fit_cpu_s'], max_rss_mb=r['max_rss_mb'])
        table.append(row)
    res['replicas'] = table
    # failed fits over everything
    tot = dict(toys=0, dropped=0, retried=0, exc=0, inacc=0); worst_drop = 0.0
    for r in reps:
        for p in r['points']:
            for lab in ('b', 'sb'):
                e = p[lab]; n = len(e['q'])
                tot['toys'] += n; tot['dropped'] += e['dropped']; tot['retried'] += e['retried']
                tot['exc'] += e['first_exception']; tot['inacc'] += e['first_inaccurate']
                worst_drop = max(worst_drop, e['dropped'] / n)
    res['fits'] = dict(tot, worst_dropped_fraction_per_ensemble=worst_drop)
    # timing on the real v1 workspace
    fs = np.array([p['fit_cpu_s_per_1000_plus_1000'] for r in reps for p in r['points']])
    ls = np.array([p['loop_cpu_s_per_1000_plus_1000'] for r in reps for p in r['points']])
    res['timing'] = dict(n_par=3, fit_s_per_unit_mean=float(fs.mean()), fit_s_per_unit_sd=float(fs.std(ddof=1)),
                         fit_s_per_unit_min=float(fs.min()), fit_s_per_unit_max=float(fs.max()),
                         fit_s_per_unit_median=float(np.median(fs)),   # the first point of a job includes the jit compilation
                         loop_s_per_unit_mean=float(ls.mean()), n_units=int(len(fs)))
    # verdict (plan §2.3)
    ok = [(r['seed'], v['primary']) for r, v in zip(reps, var) if v['primary']['status'] == 'ok']
    mus = np.array([x['mu95'] for _, x in ok])
    res['n_resolved'] = len(ok)
    res['n_inside_window'] = int(np.sum((mus >= lo) & (mus <= hi))); res['n_outside_window'] = int(len(mus) - res['n_inside_window'])
    for k in var[0]:
        a = np.array([v[k]['mu95'] for v in var if v[k]['status'] == 'ok'])
        res.setdefault('variant_stats', {})[k] = dict(n=int(len(a)), mean=float(a.mean()) if len(a) else None,
                                                      sd=float(a.std(ddof=1)) if len(a) > 1 else None,
                                                      values=a.tolist(),
                                                      n_inside=int(np.sum((a >= lo) & (a <= hi))))
    if len(ok) < 8:
        res['verdict'] = 'NOT RESOLVED (numerics: fewer than 8 of 10 replicas resolved)'
        dump(out, res); return
    prim_seed, prim = ok[0]
    sd = float(mus.std(ddof=1)); sig = max(sd, prim['err_binomial'])
    v0 = verdict_of(prim['mu95'], sig, lo, hi)
    res['primary'] = dict(seed=prim_seed, mu95=prim['mu95'], ratio_to_v1=prim['mu95'] / v1, sd_replicas=sd,
                          err_binomial=prim['err_binomial'], sigma_toy=sig, interval=[prim['mu95'] - sig, prim['mu95'] + sig],
                          reading=v0, bracket=prim['bracket'], cls_bracket=prim['cls_bracket'], zero_upper=prim['zero_upper'])
    res['replica_mean'] = float(mus.mean()); res['replica_values'] = mus.tolist()
    # pooled escalation (computed always, read only if the primary straddles)
    mu_list = sorted({round(p['mu'], 6) for r in reps for p in r['points']})
    pooled = {}
    for m in mu_list:
        qb = np.concatenate([_qarr(p['b']['q']) for r in reps for p in r['points'] if round(p['mu'], 6) == m])
        qs = np.concatenate([_qarr(p['sb']['q']) for r in reps for p in r['points'] if round(p['mu'], 6) == m])
        pooled[m] = (qb, qs)
    plim = limit_from_points([(m, cls_counts(*pooled[m])) for m in mu_list])
    rng = np.random.default_rng(20261117)
    boot = []; nfail = 0
    for _ in range(500):
        o = []
        for m in mu_list:
            qb, qs = pooled[m]
            o.append((m, cls_counts(qb[rng.integers(0, len(qb), len(qb))], qs[rng.integers(0, len(qs), len(qs))])))
        bl = limit_from_points(o)
        if bl['status'] == 'ok':
            boot.append(bl['mu95'])
        else:
            nfail += 1
    res['pooled'] = dict(limit=plim, toys_per_mu={str(m): [int(len(pooled[m][0])), int(len(pooled[m][1]))] for m in mu_list},
                         cls={str(m): cls_value(cls_counts(*pooled[m]))[0] for m in mu_list},
                         frac_b_dropped={str(m): float(np.mean(~np.isfinite(pooled[m][0]))) for m in mu_list},
                         boot_n=len(boot), boot_not_ok=nfail, boot_sd=float(np.std(boot, ddof=1)) if len(boot) > 1 else None,
                         boot_quantiles=[float(x) for x in np.quantile(boot, [0.025, 0.16, 0.5, 0.84, 0.975])] if boot else None,
                         boot_frac_inside=float(np.mean((np.array(boot) >= lo) & (np.array(boot) <= hi))) if boot else None)
    if v0 != 'STRADDLES':
        res['verdict'] = v0
    elif plim['status'] != 'ok' or len(boot) < 2:
        res['verdict'] = 'NOT RESOLVED (straddles; pooled limit not defined)'
    else:
        v1p = verdict_of(plim['mu95'], res['pooled']['boot_sd'], lo, hi)
        res['pooled']['reading'] = v1p
        res['verdict'] = v1p if v1p != 'STRADDLES' else 'NOT RESOLVED (straddles at 1000 + 1000 and pooled)'
    dump(out, res)
    log.info('T1-b: %s; primary %.1f +- %.1f (ratio %.3f), replicas %s', res['verdict'], prim['mu95'], sig,
             prim['mu95'] / v1, np.round(mus, 1).tolist())


def newton_decrement(model, data, pars, bounds, fixed_idx=()):
    """GUARD for any workspace (jax backend): g^T H^-1 g / 2 of twice_nll at a returned fit point, over the parameters
    that are neither fixed nor at a bound.  It estimates how far the objective is above its minimum: ~0 for a
    converged fit (accept below 1e-4), 1e5 at the false "success" of the pyhf trap.  inf if the Hessian is not
    positive definite.  Use it after every pyhf fit where no exact profile exists (the v2 workspace)."""
    import jax
    tl = pyhf.tensorlib
    f = lambda q: pyhf.infer.mle.twice_nll(q, data, model)[0]                         # noqa: E731
    p = tl.astensor(pars)
    g = np.asarray(tl.tolist(jax.grad(f)(p)), float); H = np.asarray(tl.tolist(jax.hessian(f)(p)), float)
    pv = np.asarray(tl.tolist(p), float); b = np.asarray(bounds, float)
    free = [i for i in range(len(pv)) if i not in fixed_idx and b[i, 0] + 1e-8 < pv[i] < b[i, 1] - 1e-8]
    if not free:
        return 0.0
    gs = g[free]; Hs = H[np.ix_(free, free)]
    try:
        np.linalg.cholesky(Hs)
    except np.linalg.LinAlgError:
        return float('inf')
    return float(0.5 * gs @ np.linalg.solve(Hs, gs))


def mode_hyporepro(out):
    """Minimal reproduction of the pyhf trap (log 08:37): with default start values the fixed-mu fit of this
    workspace stops far from the minimum and reports success, so pyhf.infer.hypotest returns CLs = 0.0 without
    raising.  Recorded per mu: the true CLs (exact profile), hypotest as called by default, the fixed-mu fit from the
    default start (excess of twice-NLL over the exact minimum, gradient at the returned point), the same from the
    closed-form start, and all of it again with SLSQP tolerance 1e-10."""
    import jax
    inp = v1_inputs('limits'); truth = V1Truth(inp)
    res = dict(mode='hyporepro', rows=[])
    for tol in (None, 1e-10):
        CONF['tol'] = tol
        set_backend('jax')
        tl = pyhf.tensorlib
        ws, model = v1_model(inp); fit = Fitter(model, truth)
        asimov = fit.data(truth.b)
        gradf = jax.grad(lambda p: pyhf.infer.mle.twice_nll(p, asimov, model)[0])
        for mu in (780.0, 820.0, 828.0):
            t_exact = float(truth.ref_T(truth.b[0:1])[1][0] + truth.ref_fixed_G(truth.b[1:2], mu)[1][0])
            r = dict(tol=tol, mu=mu, cls_true=cls_asym(float(truth.q_ref(truth.b[1:2], mu)[0][0])),
                     twice_nll_exact_fixed=t_exact, default_init=list(model.config.suggested_init()))
            th_t, thg_fix, mu0, thg_free = truth.starts(truth.b, mu)
            start = fit.pars(mu, th_t, thg_fix)
            for lab, kw in (('hypotest_default', {}), ('hypotest_closed_form_init', dict(init_pars=list(start)))):
                try:
                    h = pyhf.infer.hypotest(mu, asimov, model, test_stat='qtilde', return_expected=True, **kw)
                    r[lab] = [float(h[0]), float(h[1])]
                except Exception as e:  # noqa: BLE001
                    r[lab] = repr(e)[:200]
            for lab, ini in (('fit_default_start', None), ('fit_closed_form_start', list(start))):
                try:
                    pf, t = pyhf.infer.mle.fixed_poi_fit(mu, asimov, model, ini, return_fitted_val=True)
                    g = np.asarray(tl.tolist(gradf(pf)), float)
                    r[lab] = dict(newton_decrement=newton_decrement(model, asimov, pf, fit.bounds, (fit.i_mu,)),
                                  pars=[float(x) for x in tl.tolist(pf)], twice_nll=float(t),
                                  excess_over_exact=float(t) - t_exact, grad=g.tolist(),
                                  par_order=list(model.config.par_order))
                except Exception as e:  # noqa: BLE001
                    r[lab] = repr(e)[:200]
            res['rows'].append(r)
            log.info('hyporepro tol %s mu %.0f: true %.4f hypotest %s / %s', tol, mu, r['cls_true'],
                     r['hypotest_default'], r['hypotest_closed_form_init'])
    dump(out, res)


def main(argv):
    mode = argv[0]
    if mode == 'hyporepro':
        return mode_hyporepro(argv[1])
    if mode == 'setup':
        return mode_setup(argv[1], argv[2], quick=len(argv) > 3)
    if mode == 'pt':
        set_conf(argv[6] if len(argv) > 6 else '')
        return mode_pt(argv[1], argv[2], float(argv[3]), int(argv[4]), int(argv[5]))
    if mode == 'pair':
        return mode_pair(argv[1], argv[2], argv[3])
    if mode == 'vcheck':
        return mode_vcheck(argv[1], argv[2])
    if mode == 't1b':
        set_conf(argv[6] if len(argv) > 6 else '')
        return mode_t1b(argv[1], float(argv[2]), int(argv[3]), int(argv[4]) if len(argv) > 4 else 1000,
                        int(argv[5]) if len(argv) > 5 else 6)
    if mode == 'v1stat':
        return mode_v1stat(argv[1], int(argv[2]) if len(argv) > 2 else 5000)
    if mode == 'ref':
        return mode_ref(argv[1], float(argv[2]), int(argv[3]) if len(argv) > 3 else 200000)
    if mode == 'summary':
        return mode_summary(argv[1], float(argv[2]), argv[3:])
    raise SystemExit(__doc__)


if __name__ == '__main__':
    main(sys.argv[1:])
