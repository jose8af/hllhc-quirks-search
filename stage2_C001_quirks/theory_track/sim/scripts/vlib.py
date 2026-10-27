"""vlib.py -- shared helpers for the Stage-2 validation scripts (sim/scripts/val_*.py).  Pure numpy/matplotlib.
Sample access: S(id, m) -> dict of arrays from ../data/sim/npz/<id>_m<m>.npz (weights w in fb/event, N_IC = 1).
Old LO cache (code/T2_kinematics.py output): old(spin, m, key) with key in {'incl', 'isr'} -> same observables."""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
TT = os.path.dirname(SIM)
DATA = os.path.join(TT, 'data', 'sim')
RES = os.path.join(SIM, 'results')
FIG = os.path.join(SIM, 'figures')
OLD = os.path.join(TT, 'data', 'cache', 'T2_kinematics_cache.npz')
os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
SIG_PER_KEV2 = 50.68           # GeV/cm per keV^2 (BRIEF; sigma = Lambda^2)
R_TRK, Z_TRK = 110.0, 270.0    # cm, as in T2_kinematics.py
LABEL = 'Private work (simulation, generator level)'   # never a CMS-type label (fixer S2-R1)
_cache = {}


def path(id_, m):
    return os.path.join(DATA, 'npz', f'{id_}_m{int(m)}.npz')


def have(id_, m):
    return os.path.exists(path(id_, m))


def S(id_, m):
    p = path(id_, m)
    if p not in _cache:
        c = dict(np.load(p, allow_pickle=False))
        c['wvar_names'] = [str(x) for x in c['wvar_names']]
        c['m'] = float(c['mq'])
        _add_obs(c)
        _cache[p] = c
    return _cache[p]


def _boost_gamma_star(pp, pm):
    P = pp + pm
    M = np.sqrt(np.maximum(P[:, 0] ** 2 - np.sum(P[:, 1:] ** 2, 1), 0))
    b = P[:, 1:] / P[:, :1]
    b2 = np.sum(b * b, 1); g = 1 / np.sqrt(1 - b2)
    e_star = g * (pp[:, 0] - np.sum(b * pp[:, 1:], 1))
    mq = np.sqrt(np.maximum(pp[:, 0] ** 2 - np.sum(pp[:, 1:] ** 2, 1), 0))
    return e_star / mq, M


def _add_obs(c):
    P = c['p_qp'] + c['p_qm']
    c['pt'] = c['pt_pair']; c['y'] = c['y_pair']; c['eta'] = c['eta_pair']; c['M'] = c['m_pair']; c['g'] = c['gamma_star']
    H = c['p_qq_hard']
    c['pt_hard'] = np.hypot(H[:, 1], H[:, 2])
    c['g_hard'], c['M_hard'] = _boost_gamma_star(c['p_qp_hard'], c['p_qm_hard'])
    c['beta_star'] = np.sqrt(np.clip(1 - 1 / c['g'] ** 2, 0, 1))
    c['bg'] = c['bg_pair']
    c['nosc'] = nosc(c['g'], c['bg'], c['eta'], c['m'])
    c['recoil_pt'] = np.hypot(c['recoil'][:, 1], c['recoil'][:, 2])
    c['recoil5_pt'] = np.hypot(c['recoil_eta5'][:, 1], c['recoil_eta5'][:, 2])
    tot = c['recoil'] + c['nu'] + P
    c['balance_pt'] = np.hypot(tot[:, 1], tot[:, 2])
    c['j1pt'] = c['jets'][:, 0, 0]


def nosc(g, bg, eta, m, lam=1.0):
    """Oscillations inside r < 110 cm, |z| < 270 cm (T2_kinematics.per_lambda): crossings every
    D = 2 p* (beta gamma)_pair / sigma along the line of flight; N_osc = S_exit / D / 2.  Lambda = 1 keV."""
    sig = SIG_PER_KEV2 * lam ** 2
    pstar = m * np.sqrt(np.maximum(g ** 2 - 1, 0))
    D = 2 * pstar * bg / sig
    th = 2 * np.arctan(np.exp(-eta))
    sint, cost = np.abs(np.sin(th)), np.abs(np.cos(th))
    with np.errstate(divide='ignore', invalid='ignore'):
        sexit = np.minimum(np.where(sint > 0, R_TRK / sint, np.inf), np.where(cost > 0, Z_TRK / cost, np.inf))
        return np.where(D > 0, sexit / D / 2, np.inf)


def old(spin, m, key):
    o = np.load(OLD)
    k = f'{spin}_{int(m)}_{key}'
    g = o[k + '_gamma_star']; w = o[k + '_w']; bg = o[k + '_bg_pair']; eta = o[k + '_eta_pair']
    M = 2 * m * g
    if key == 'incl':
        pt = np.zeros_like(g); y = np.sign(eta) * np.arcsinh(bg); eta_ = np.sign(eta) * 50.0
    else:
        pt = M * bg / np.cosh(eta)
        pz = M * bg * np.tanh(eta); E = M * np.sqrt(1 + bg ** 2)
        y = 0.5 * np.log((E + pz) / (E - pz)); eta_ = eta
    ok = w > 0
    d = dict(g=g[ok], w=w[ok] / w[ok].sum(), bg=bg[ok], eta=eta_[ok], M=M[ok], pt=pt[ok], y=y[ok], m=float(m),
             cstar=o[k + '_cstar'][ok])
    d['nosc'] = nosc(d['g'], d['bg'], d['eta'], m)
    return d


def wquant(v, w, qs=(0.16, 0.5, 0.84)):
    v = np.asarray(v); w = np.asarray(w, float)
    ok = (w > 0) & np.isfinite(v)
    v, w = v[ok], w[ok]
    i = np.argsort(v); v = v[i]; c = np.cumsum(w[i]); c /= c[-1]
    return np.array([v[min(np.searchsorted(c, q), len(v) - 1)] for q in qs])


def boot_quant(v, w, qs=(0.16, 0.5, 0.84), nb=200, seed=1):
    """Weighted quantiles with bootstrap (event resampling) standard errors."""
    rng = np.random.default_rng(seed)
    v = np.asarray(v); w = np.asarray(w, float)
    ok = (w != 0) & np.isfinite(v); v, w = v[ok], w[ok]
    q0 = wquant(v, w, qs)
    bs = np.array([wquant(v[ix], w[ix], qs) for ix in (rng.integers(0, len(v), len(v)) for _ in range(nb))])
    return q0, bs.std(0)


def neff(w):
    w = np.asarray(w, float)
    return float(w.sum() ** 2 / np.sum(w ** 2)) if np.sum(w ** 2) > 0 else 0.0


def wvar(c, name):
    return c['wvar'][:, c['wvar_names'].index(name)]


def save(name, obj):
    def conv(o):
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, np.ndarray):
            return conv(o.tolist())
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        return o
    p = os.path.join(RES, name)
    json.dump(conv(obj), open(p, 'w'), indent=1)
    return p


def hist_norm(v, w, bins):
    h, _ = np.histogram(v, bins=bins, weights=w)
    h2, _ = np.histogram(v, bins=bins, weights=np.asarray(w) ** 2)
    s = np.sum(w[(v >= bins[0]) & (v < bins[-1])])
    return h / s, np.sqrt(h2) / s
