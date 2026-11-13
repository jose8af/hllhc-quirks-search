"""stats.py -- log-normal B sums and B84 (WP_RULE §4.1), the working-point rule (§5.1-§5.3), and the Stage-5 two-bin
counting likelihood (plan §2.6 deliverable 2, D4-13): pyhf JSON workspace + expected 95 % CL limits.

Log-normal convention: each B term = central x exp(sigma_ln z), z ~ N(0, 1) (central = median).  sigma_ln is carried
as named components; components in SHARED are one z per component name across all terms AND both categories (WP_RULE
§5.2: density normalisation, extrapolation model, K-factor/normalisation fully correlated); every other component is
independent per term.  B84 = the 84th percentile of the Monte-Carlo sum.

Limits: pyhf model = two channels (SR-T, SR-G), one bin each, signal 'normfactor' mu, background with 'normsys'
modifiers hi = exp(sigma), lo = exp(-sigma) (pyhf interpcode code1 = exponential = exactly the log-normal), shared
components with the SAME modifier name in both channels (correlated).  pyhf is NOT in the theory_track env; the in-house
asymptotic CLs (q~_mu, Asimov, Cowan et al. 2011, the pyhf 'asymptotics' calculator) is used and was cross-checked
against pyhf 0.7.6 in an isolated interpreter (ANALYSIS_DEV_REPORT §4).  A toy-based CLs is also provided because the
asymptotic formulae fail at B << 1 (b -> 0 gives 1.92 instead of 3.0 events).
"""
import numpy as np
from scipy.optimize import minimize, brentq
from scipy.stats import norm, poisson

SHARED = ('density', 'model_spread', 'normalisation', 'closure', 'trend', 'srt_pv', 'srt_sigt', 'T3')   # B-9 (i)
B84_CAT = 0.11
B84_COMB = 0.30


# ================================================================================================ log-normal sums
def sample_terms(terms, nmc, rng, zshared=None):
    """terms: list of dict(value, comps={name: sigma}).  Returns (nmc,) sum samples and the shared z used."""
    zshared = {} if zshared is None else zshared
    tot = np.zeros(nmc)
    for t in terms:
        if t.get('value') is None or t['value'] <= 0:
            continue
        lz = np.zeros(nmc)
        for name, s in (t.get('comps') or {}).items():
            if not s:
                continue
            if name in SHARED:
                if name not in zshared:
                    zshared[name] = rng.standard_normal(nmc)
                z = zshared[name]
            else:
                z = rng.standard_normal(nmc)
            lz += s * z
        tot += t['value'] * np.exp(lz)
    return tot, zshared


def b84(terms, nmc=200_000, seed=20261014):
    rng = np.random.default_rng(seed)
    s, _ = sample_terms(terms, nmc, rng)
    return float(np.quantile(s, 0.84)), float(np.median(s)), float(np.mean(s))


def b84_pair(terms_T, terms_G, nmc=200_000, seed=20261014):
    rng = np.random.default_rng(seed)
    sT, zs = sample_terms(terms_T, nmc, rng)
    sG, _ = sample_terms(terms_G, nmc, rng, zs)
    return float(np.quantile(sT + sG, 0.84))


# ================================================================================================ WP rule
def rstar(b84_by_rung):
    """§5.1: the loosest rung r with B84_c(r) <= 0.11 for r AND every tighter rung (rungs 1..23 in ladder order)."""
    R = len(b84_by_rung)
    ok_tail = [False] * R
    run = True
    for i in range(R - 1, -1, -1):
        run = run and (b84_by_rung[i] is not None and b84_by_rung[i] <= B84_CAT)
        ok_tail[i] = run
    for i in range(R):
        if ok_tail[i]:
            return i + 1
    return None


def combined_guard(rT, rG, terms_by_rung_T, terms_by_rung_G, b84T, b84G, nmc=100_000):
    """§5.2 combined guard and deterministic continuation.  terms_by_rung_c[r-1] = list of terms.  Returns dict."""
    R = len(terms_by_rung_T)
    log = []
    cache = {}

    def comb(a, b):
        if (a, b) not in cache:
            cache[(a, b)] = b84_pair(terms_by_rung_T[a - 1], terms_by_rung_G[b - 1], nmc=nmc)
        return cache[(a, b)]

    def accepted(a, b):
        for x in range(a, R + 1):
            for y in range(b, R + 1):
                if comb(x, y) > B84_COMB:
                    return False
        return True
    a, b = rT, rG
    for step in range(2 * (R - 1) + 1):
        if accepted(a, b):
            return dict(accepted=True, pair=(a, b), combined_b84=comb(a, b), steps=step, log=log)
        log.append(dict(pair=(a, b), combined_b84=comb(a, b)))
        if a == R and b == R:
            break
        if b == R or (a < R and b84T[a - 1] > b84G[b - 1]):
            a += 1
        else:
            b += 1                     # tie or larger SR-G B84 -> SR-G moves (tie: SR-G)
    return dict(accepted=False, pair=None, note='(R, R) reached and not accepted: both categories under §8 fallback',
                log=log)


def wp_rule(b84T, b84G, terms_T, terms_G):
    rT = rstar(b84T); rG = rstar(b84G)
    out = dict(r_star_T=rT, r_star_G=rG)
    if rT is not None and rG is not None:
        g = combined_guard(rT, rG, terms_T, terms_G, b84T, b84G)
        out['combined_guard'] = g
        if g['accepted']:
            out['wp'] = dict(T=g['pair'][0], G=g['pair'][1], branch='both categories, combined guard accepted')
        else:
            out['wp'] = dict(T=None, G=None, branch='combined guard failed at (R, R): §8 fallback for both')
    elif rT is not None or rG is not None:
        out['wp'] = dict(T=rT, G=rG, branch='exactly one category has a WP (§5.2): no combined check')
    else:
        out['wp'] = dict(T=None, G=None, branch='no WP in either category (§5.3): §8 fallback, user told')
    return out


# ================================================================================================ workspace
def workspace(s, b, sig_shared, sig_own, names=('SR_T', 'SR_G'), meas='quirk_counting'):
    """pyhf JSON workspace (schema 1.0.0) of the two-bin counting likelihood.  s, b: per-channel yields;
    sig_shared[c] = {component: sigma} correlated across channels (same modifier name); sig_own[c] = sigma (own)."""
    ch = []; obs = []
    for i, c in enumerate(names):
        mods_b = [dict(name=f'bkg_{k}', type='normsys', data=dict(hi=float(np.exp(v)), lo=float(np.exp(-v))))
                  for k, v in sig_shared[i].items() if v > 0]
        if sig_own[i] > 0:
            mods_b.append(dict(name=f'bkg_own_{c}', type='normsys',
                               data=dict(hi=float(np.exp(sig_own[i])), lo=float(np.exp(-sig_own[i])))))
        ch.append(dict(name=c, samples=[dict(name='signal', data=[float(s[i])],
                                             modifiers=[dict(name='mu', type='normfactor', data=None)]),
                                        dict(name='background', data=[float(b[i])], modifiers=mods_b)]))
        obs.append(dict(name=c, data=[float(b[i])]))
    return dict(channels=ch, observations=obs, version='1.0.0',
                measurements=[dict(name=meas, config=dict(poi='mu', parameters=[dict(name='mu', bounds=[[0.0, 1000.0]], inits=[1.0])]))])


# ================================================================================================ in-house asymptotic CLs
def _model(s, b, sh, own):
    """Returns nll(mu, alphas, data) for the workspace model (code1 interpolation = exp(sigma alpha))."""
    s = np.asarray(s, float); b = np.asarray(b, float)
    shn = sorted({k for d in sh for k in d})
    nA = len(shn) + len(b)

    def lam(mu, al):
        ln = np.zeros(len(b))
        for i in range(len(b)):
            for j, k in enumerate(shn):
                ln[i] += sh[i].get(k, 0.0) * al[j]
            ln[i] += own[i] * al[len(shn) + i]
        return mu * s + b * np.exp(ln)

    def nll(mu, al, n, aux):
        """FIX R6 (INV_STATS_BKG item 1): minus the saturated offset n - n ln n (pyhf-equivalent; q~ unchanged).
        Without it |NLL| ~ 3e9 at b ~ 1e8, so L-BFGS-B's RELATIVE ftol (2.2e-9 -> dNLL ~ 6) stopped the nuisance
        profile after one step and the asymptotic limit fell to the unprofiled 1.96 sqrt(b)/s."""
        la = np.maximum(lam(mu, al), 1e-300)
        n = np.asarray(n, float)
        sat = np.where(n > 0, n - n * np.log(np.maximum(n, 1e-300)), 0.0)
        return float(np.sum(la - n * np.log(la) - sat) + 0.5 * np.sum((al - aux) ** 2))
    return nll, nA


def _profile(nll, nA, n, aux, mu=None, mu_bounds=(0, 1e4)):
    if mu is None:
        f = lambda x: nll(x[0], x[1:], n, aux)                          # noqa: E731
        x0 = np.r_[1.0, aux]
        r = minimize(f, x0, method='L-BFGS-B', bounds=[mu_bounds] + [(-5, 5)] * nA)
        return r.fun, r.x[0]
    f = lambda x: nll(mu, x, n, aux)                                    # noqa: E731
    r = minimize(f, np.array(aux, float), method='L-BFGS-B', bounds=[(-5, 5)] * nA)
    return r.fun, mu


def qtilde_asimov(mu, s, b, sh, own):
    nll, nA = _model(s, b, sh, own)
    n = np.asarray(b, float); aux = np.zeros(nA)                      # Asimov b-only: n = b, aux = 0, muhat = 0
    l0, _ = _profile(nll, nA, n, aux, mu=0.0)
    lm, _ = _profile(nll, nA, n, aux, mu=mu)
    return max(2 * (lm - l0), 0.0)


def expected_limit_asymptotic(s, b, sh, own, cl=0.95):
    """Median and +-1, +-2 sigma expected CLs upper limits on mu (q~_mu asymptotics on the b-only Asimov dataset)."""
    out = {}
    for N in (-2, -1, 0, 1, 2):
        def f(mu):
            qa = qtilde_asimov(mu, s, b, sh, own)
            sq = np.sqrt(qa)
            clsb = 1 - norm.cdf(sq - N); clb = norm.cdf(N)
            return clsb / clb - (1 - cl)
        hi = 1.0
        while f(hi) > 0 and hi < 1e16:
            hi *= 4
        lo = hi / 4 if hi > 1 else 1e-6
        while f(lo) < 0 and lo > 1e-12:
            lo /= 4
        if f(hi) > 0 or f(lo) < 0:
            out[N] = None
            continue
        out[N] = float(brentq(f, lo, hi, xtol=1e-9 * hi, rtol=1e-8))
    return dict(median=out[0], band_1s=[out[-1], out[1]], band_2s=[out[-2], out[2]], calculator='asymptotic q~_mu',
                primary=False, role='cross-check (D4)')


NTOYS_PRIMARY = 5000          # D4 (orchestrator 2026-10-14): toys are the PRIMARY expected limit; fixed count and seed
TOY_SEED = 20261014


def expected_limit_toys(s, b, sh, own, cl=0.95, ntoys=NTOYS_PRIMARY, seed=TOY_SEED):
    """Hybrid (Bayesian-marginalised nuisance) CLs with the number-count test statistic Q = sum_c n_c w_c,
    w_c = ln(1 + mu s_c / b_c); median expected limit under b-only.  Exact at b -> 0 (3.0 events for one bin).
    REVIEW R1 C-4: common random numbers -- the nuisance draws and the b-only toys are drawn ONCE and the s+b toys
    re-use the same seeded stream at every mu, so CLs(mu) is deterministic during the bisection (numpy Poisson; the
    scipy inverse-CDF variant was exact-monotone but ~45 s per point)."""
    rng = np.random.default_rng(seed)
    s = np.asarray(s, float); b = np.asarray(b, float)
    shn = sorted({k for d in sh for k in d})
    zs = {k: rng.standard_normal(ntoys) for k in shn}
    ln = np.zeros((ntoys, len(b)))
    for i in range(len(b)):
        for k in shn:
            ln[:, i] += sh[i].get(k, 0.0) * zs[k]
        ln[:, i] += own[i] * rng.standard_normal(ntoys)
    bt = b[None, :] * np.exp(ln)
    nb_obs = rng.poisson(bt); nb = rng.poisson(bt)

    def cls(mu, q):
        w = np.log1p(mu * s / np.maximum(b, 1e-12))
        nsb = np.random.default_rng([seed, 1]).poisson(bt + mu * s[None, :])   # same stream at every mu (CRN)
        qobs = float(np.quantile((nb_obs * w).sum(1), q))
        clsb = np.mean((nsb * w).sum(1) <= qobs); clb = np.mean((nb * w).sum(1) <= qobs)
        return clsb / max(clb, 1e-12)

    def solve(q):
        lo, hi = 0.0, 1.0
        while cls(hi, q) > 1 - cl and hi < 1e16:
            hi *= 4
        lo = hi / 4 if hi > 1 else 0.0
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if cls(mid, q) > 1 - cl:
                lo = mid
            else:
                hi = mid
        return float(hi)
    # expected-limit quantiles of the b-only test statistic (Stage-5 request: toy-based +-1/2 sigma bands)
    qs = dict(m2=norm.cdf(-2), m1=norm.cdf(-1), med=0.5, p1=norm.cdf(1), p2=norm.cdf(2))
    v = {k: solve(q) for k, q in qs.items()}
    return dict(median=v['med'], band_1s=[v['m1'], v['p1']], band_2s=[v['m2'], v['p2']],
                calculator=f'toys (hybrid CLs, {ntoys} toys, seed {seed}, common random numbers)', primary=True,
                band_note='quantiles of the b-only test statistic (same toys); discrete at small B')


def discovery(s, b, sigma_ln):
    """Asimov discovery significance of one bin with a log-normal-uncertain b (approximate: Cowan Z_A with the b
    uncertainty folded as sigma_b = b sigma_ln) and the 3-event statement (only where B84 <= 0.3, background-free)."""
    sb = b * sigma_ln
    if b <= 0:
        return dict(Z_A=None)
    if sb > 0:
        z2 = 2 * ((s + b) * np.log((s + b) * (b + sb ** 2) / (b * b + (s + b) * sb ** 2))
                  - b * b / sb ** 2 * np.log(1 + sb ** 2 * s / (b * (b + sb ** 2))))
    else:
        z2 = 2 * ((s + b) * np.log(1 + s / b) - s)
    return dict(Z_A=float(np.sqrt(max(z2, 0.0))), p_3events_bkg_only=float(poisson.sf(2, b)))


def discovery_reach(s, b, sig_ln, b84_comb=None, z_target=5.0):
    """D4-13 discovery outputs per point: (i) where the combined B84 <= 0.3 (background-free, §5.2/§8) the 3-event
    statement mu_3 = 3 / sum(s); (ii) mu for Z_A = 5 with the per-bin Asimov significances added in quadrature
    (approximate combination, flagged)."""
    s = np.asarray(s, float); b = np.asarray(b, float)
    out = dict(mu_3events=(3.0 / s.sum()) if (b84_comb is not None and b84_comb <= B84_COMB and s.sum() > 0) else None)

    def z(mu):
        zz = [discovery(mu * si, bi, sl)['Z_A'] or 0.0 for si, bi, sl in zip(s, b, sig_ln) if si > 0 and bi > 0]
        return float(np.sqrt(np.sum(np.square(zz)))) if zz else 0.0
    if s.sum() <= 0 or not np.any((s > 0) & (b > 0)):
        out['mu_5sigma'] = None
        return out
    hi = 1.0
    while z(hi) < z_target and hi < 1e9:
        hi *= 2
    out['mu_5sigma'] = float(brentq(lambda m: z(m) - z_target, 1e-9, hi)) if z(hi) >= z_target else None
    out['note'] = 'Z_A per bin (Cowan, b uncertainty sigma_b = b sigma_ln), bins combined in quadrature (approximate)'
    return out
