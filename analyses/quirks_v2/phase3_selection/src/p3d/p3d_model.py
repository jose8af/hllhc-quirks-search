"""p3d_model.py -- T1 workspace builder for the v2 term structure (STR §4.11 pt 1; COM T1-a, l.355).  Gorm, 2026-11-24.

SPEC (a JSON-able dict; one spec = one selection, i.e. one T2 candidate)
  cats     ['SR_T', 'SR_G'] (or ['SR'] for one-bin tests): the counting bins c.
  signal   {'yield': {cat: S_c per unit mu}, 'counted': [fid], 'nuis': {name: w | [w_lo, w_hi]}, 'label': str}
           S enters ONLY as a v1 placeholder efficiency (label says so).  No v2 signal efficiency is used anywhere.
  counted  {fid: {'m': m, 'label': str, 'fixed': None | value}}  one rate lambda_f per counted factor (STR l.1563-1564:
           one per weight class); expected auxiliary count lambda_f, observed m (zero allowed).  'fixed' = the
           rate is fixed (alternative (ii) of STR l.1620 or a no-credit value); a fixed rate is not drawn.
  samples  [{'name', 'term', 'yield': {cat: coeff}, 'counted': [fid], 'nuis': {name: w | [w_lo, w_hi]}}]
           expected_c(sample) = coeff_c * prod_f lambda_f * prod_k phi_k(theta_k);  coeff = N_t w_tc / prod M_f
           * (nominal values of its estimator and fixed factors).  A counted fid shared by several samples is ONE
           measurement (shared normfactor and one auxiliary bin).  A term = the samples with the same 'term'
           (several weight classes); each term has exactly one route (its sample list).
  nuis     {name: {'bound': theta_max | None, 'kind': str}}   constrained log-normal nuisances (normsys, code1:
           phi = exp(w theta)); 'bound' = censoring at the no-credit value, theta_max = ln(1/phi0)/s for a
           probability (STR l.1582-1584): a parameter bound in the fit and a clip in the generation.
  mu_max   upper bound of mu (lower bound 0: q~).
Layout: one channel 'SR' (one bin per category) + one channel 'aux' (one bin per counted factor), the merged layout
of Phase 2 (VIK §4 (d)); same likelihood as one channel per count.  pyhf sorts channels: 'SR' < 'aux'.
The model must be built with modifier_settings={'normsys': {'interpcode': 'code1'}} (done here; not stored in the
JSON, so a published workspace states it beside the file, FLO §5).

Spec makers: onebin(kappa, m), v1count(point) (v1 counts with the v2 treatment, readings R1 of the session log),
v1mode() (the Phase-2 collapsed v1-mode workspace), v2_placeholder() (task 3: the v2 term structure, every count
a placeholder).  pyhf is imported lazily (works with the numpy env on maxwell and the jax env on schrodinger).
"""
import copy
import json
import logging
import math
from pathlib import Path

import numpy as np

log = logging.getLogger('p3d_model')

REPO = Path(__file__).resolve().parents[5]
AN1 = REPO / 'stage2_C001_quirks/theory_track/data/acts_stage4/analysis/C12FC_v1'
V1_NORM = 15775.0            # events before selection per unit mu (STR l.1729)
SIGMA_NORM = math.log(1.3)   # v1 run_all.DEFAULTS sigma_norm (run_c1b.py l.30)
SHARED = ('density', 'model_spread', 'normalisation', 'closure', 'trend', 'srt_pv', 'srt_sigt', 'T3')  # v2arith
TH_LO, TH_HI = -5.0, 5.0     # pyhf default bounds of a normsys parameter
U68 = -math.log(0.32)        # 1.139, 68 % upper value of a zero count (STR l.1615)


def _w(w):
    """(w_lo, w_hi) of a log-normal width given as a number or a pair."""
    if isinstance(w, (list, tuple)):
        return float(w[0]), float(w[1])
    return float(w), float(w)


def _normsys(nuis):
    return [{'name': n, 'type': 'normsys', 'data': {'hi': math.exp(_w(w)[1]), 'lo': math.exp(-_w(w)[0])}}
            for n, w in nuis.items() if max(_w(w)) > 0]


def build(spec, censor=True):
    """spec -> (pyhf.Workspace, model).  censor=False drops the censoring bounds (test T1-c (v))."""
    import pyhf
    cats = spec['cats']
    fids = list(spec['counted'])
    lam = lambda f: {'name': 'lam_' + f, 'type': 'normfactor', 'data': None}                       # noqa: E731
    sig = spec['signal']
    samples = [{'name': 'signal', 'data': [float(sig['yield'].get(c, 0.0)) for c in cats],
                'modifiers': [{'name': 'mu', 'type': 'normfactor', 'data': None}]
                + [lam(f) for f in sig.get('counted', [])] + _normsys(sig.get('nuis', {}))}]
    for s in spec['samples']:
        samples.append({'name': s['name'], 'data': [float(s['yield'].get(c, 0.0)) for c in cats],
                        'modifiers': [lam(f) for f in s['counted']] + _normsys(s.get('nuis', {}))})
    channels = [{'name': 'SR', 'samples': samples}]
    obs = [{'name': 'SR', 'data': [0.0] * len(cats)}]
    if fids:
        channels.append({'name': 'aux', 'samples': [
            {'name': 'aux_' + f, 'data': [1.0 if j == i else 0.0 for j in range(len(fids))], 'modifiers': [lam(f)]}
            for i, f in enumerate(fids)]})
        obs.append({'name': 'aux', 'data': [float(spec['counted'][f]['m']) for f in fids]})
    pars = [{'name': 'mu', 'bounds': [[0.0, float(spec.get('mu_max', 1e5))]], 'inits': [1.0]}]
    for f in fids:
        d = spec['counted'][f]; m = float(d['m'])
        p = {'name': 'lam_' + f, 'bounds': [[1e-9, 10.0 * (m + 5.0)]], 'inits': [m + 1.0]}
        if d.get('fixed') is not None:
            p.update(inits=[float(d['fixed'])], fixed=True,
                     bounds=[[min(1e-9, float(d['fixed'])), max(10.0 * (m + 5.0), 2.0 * float(d['fixed']))]])
        pars.append(p)
    used = {m['name'] for s in samples for m in s['modifiers'] if m['type'] == 'normsys'}
    for n, d in spec['nuis'].items():
        if n in used and censor and d.get('bound') is not None:
            pars.append({'name': n, 'bounds': [[TH_LO, float(d['bound'])]], 'inits': [0.0]})
    ws_spec = {'version': '1.0.0', 'channels': channels, 'observations': obs,
               'measurements': [{'name': spec.get('name', 'qv2'), 'config': {'poi': 'mu', 'parameters': pars}}]}
    pyhf.schema.validate(ws_spec, 'workspace.json')          # T1-a: raises if not schema-valid
    ws = pyhf.Workspace(ws_spec)
    model = ws.model(modifier_settings={'normsys': {'interpcode': 'code1'}})
    return ws, model


class Explicit:
    """Explicit numpy form of the spec's expected counts (generation; checked against pyhf at run time)."""

    def __init__(self, spec, censor=True):
        self.spec = spec; self.cats = spec['cats']; self.fids = list(spec['counted'])
        used = []
        for s in [spec['signal']] + spec['samples']:
            for n, w in s.get('nuis', {}).items():
                if max(_w(w)) > 0 and n not in used:
                    used.append(n)
        self.nk = used
        nc, nf, nk = len(self.cats), len(self.fids), len(self.nk)
        rows = spec['samples']
        self.C = np.array([[float(s['yield'].get(c, 0.0)) for c in self.cats] for s in rows]).reshape(len(rows), nc)
        self.A = np.zeros((len(rows), nf)); self.Wh = np.zeros((len(rows), nk)); self.Wl = np.zeros((len(rows), nk))
        for i, s in enumerate(rows):
            for f in s['counted']:
                self.A[i, self.fids.index(f)] = 1.0
            for n, w in s.get('nuis', {}).items():
                if n in self.nk:
                    self.Wl[i, self.nk.index(n)], self.Wh[i, self.nk.index(n)] = _w(w)
        sg = spec['signal']
        self.S = np.array([float(sg['yield'].get(c, 0.0)) for c in self.cats])
        self.As = np.zeros(nf); self.Whs = np.zeros(nk); self.Wls = np.zeros(nk)
        for f in sg.get('counted', []):
            self.As[self.fids.index(f)] = 1.0
        for n, w in sg.get('nuis', {}).items():
            if n in self.nk:
                self.Wls[self.nk.index(n)], self.Whs[self.nk.index(n)] = _w(w)
        self.m = np.array([float(spec['counted'][f]['m']) for f in self.fids])
        self.fixed = np.array([spec['counted'][f].get('fixed') is not None for f in self.fids], bool)
        self.fixval = np.array([float(spec['counted'][f]['fixed']) if spec['counted'][f].get('fixed') is not None
                                else np.nan for f in self.fids])
        self.bound = np.array([(spec['nuis'].get(n, {}).get('bound') if censor else None) or np.inf for n in self.nk],
                              float)
        self.bound_draw = {k: spec['nuis'][n]['bound_draw'] for k, n in enumerate(self.nk)
                           if censor and spec['nuis'].get(n, {}).get('bound_draw')}
        self.bound_gen = self.bound.copy()          # generation: a drawn bound replaces the static fit bound
        for k in self.bound_draw:
            self.bound_gen[k] = np.inf

    def clip_draw(self, th, rng):
        """Generation of a censored estimator whose no-credit bound is itself a zero-count term (STR l.1586-1588):
        theta <= ln(kappa lambda / phi0) / s with lambda ~ Gamma(m + 1) drawn per pseudo-experiment."""
        for k, b in self.bound_draw.items():
            lam = rng.gamma(b['m'] + 1.0, size=th.shape[0])
            th[:, k] = np.minimum(th[:, k], np.log(b['kappa'] * lam / b['phi0']) / b['s'])
        return th

    def expected(self, mu, lam, th):
        """mu (N,), lam (N, nf), th (N, nk) -> main expected counts (N, ncat).  log phi = th+ w_hi + th- w_lo."""
        lam = np.atleast_2d(lam); th = np.atleast_2d(th); mu = np.atleast_1d(mu)
        tp, tm = np.maximum(th, 0.0), np.minimum(th, 0.0)
        with np.errstate(divide='ignore'):
            llam = np.log(lam)
        lb = llam @ self.A.T + tp @ self.Wh.T + tm @ self.Wl.T            # (N, nsamp)
        b = np.exp(lb) @ self.C if self.C.size else np.zeros((len(mu), len(self.cats)))
        ls = llam @ self.As + tp @ self.Whs + tm @ self.Wls                # (N,)
        return b + (mu * np.exp(ls))[:, None] * self.S[None, :]

    def par_vector(self, model, mu, lam, th):
        cfg = model.config
        p = np.array(cfg.suggested_init(), float)
        p[cfg.poi_index] = mu
        for j, f in enumerate(self.fids):
            p[cfg.par_slice('lam_' + f).start] = lam[j]
        for k, n in enumerate(self.nk):
            p[cfg.par_slice(n).start] = th[k]
        return p


def consistency(spec, model, rng, censor=True, ntry=5):
    """Max relative difference between the explicit expected main counts and pyhf's, at random points."""
    import pyhf
    ex = Explicit(spec, censor); tl = pyhf.tensorlib; worst = 0.0
    nmain = len(spec['cats'])
    for _ in range(ntry):
        mu = float(rng.uniform(0, 2)) * float(spec.get('mu_scale', 1.0))
        lam = np.where(ex.fixed, ex.fixval, rng.gamma(ex.m + 1.0))
        th = np.minimum(rng.standard_normal(len(ex.nk)), ex.bound)
        p = ex.par_vector(model, mu, lam, th)
        e_p = np.asarray(tl.tolist(model.expected_actualdata(tl.astensor(p))), float)
        e_t = ex.expected(np.array([mu]), lam[None, :], th[None, :])[0]
        worst = max(worst, float(np.max(np.abs(e_p[:nmain] / e_t - 1.0))),
                    float(np.max(np.abs(e_p[nmain:] - lam) / np.maximum(lam, 1e-300))) if len(lam) else 0.0)
    return worst


# ============================================================================================= spec makers
def onebin(kappa, m, s=1.0, mu_max=1e4):
    """One bin, one counted term B = kappa * lambda, auxiliary count m (T1-c (i), (ii)); signal s per unit mu."""
    return {'name': f'onebin_k{kappa:g}_m{m:g}', 'cats': ['SR'], 'mu_max': mu_max,
            'signal': {'yield': {'SR': s}, 'nuis': {}, 'label': 'one-bin test signal (unit yield)'},
            'counted': {'t': {'m': m, 'label': f'test term, kappa = {kappa:g}'}},
            'samples': [{'name': 't', 'term': 't', 'yield': {'SR': kappa},
                         'counted': ['t'], 'nuis': {}}],
            'nuis': {}, 'meta': {'kappa': kappa, 'm': m}}


def v1_point(point):
    lim = json.loads((AN1 / 'limits.json').read_text())['points'][point]
    return dict(point=point, eff=list(lim['s']), s=[e * V1_NORM for e in lim['s']], b=list(lim['b']),
                sig=list(lim['sigma_ln']), selections=lim.get('selections'),
                mu95_v1_toys=lim['expected_toys']['median'] / V1_NORM if lim.get('expected_toys') else None)


def v1mode(point='A2|F|200|1.5|BM'):
    """Phase-2 v1 mode (STR l.1727-1728): one log-normal background per category, uncorrelated (FLO §5)."""
    p = v1_point(point)
    cats = ['SR_T', 'SR_G']
    return {'name': 'v1mode', 'cats': cats, 'mu_max': 1e5, 'mu_scale': 800.0,
            'signal': {'yield': dict(zip(cats, p['s'])), 'nuis': {},
                       'label': f'v1 placeholder efficiency x {V1_NORM:g} ({point})'},
            'counted': {},
            'samples': [{'name': f'bkg_{c}', 'term': f'bkg_{c}', 'yield': {c: p['b'][i]}, 'counted': [],
                         'nuis': {f'bkg_own_{c}': p['sig'][i]}} for i, c in enumerate(cats)],
            'nuis': {f'bkg_own_{c}': {'bound': None, 'kind': 'v1 collapsed width'} for c in cats},
            'meta': {'point': point, 'v1': p}}


class _Route:
    """Collects one term's route under the conversion rules R1 (session log P0)."""

    def __init__(self, term, spec, notes):
        self.term, self.spec, self.notes = term, spec, notes
        self.coeff = 1.0; self.counted = []; self.binom_s2 = 0.0; self.binom_p = 1.0; self.has_zero = False
        self.run = None              # running (N, M) of a nested chain of one sample

    def _flush(self):
        if self.run is None:
            return
        N, M, lab = self.run; self.run = None
        if N == 0:
            if self.has_zero:        # one zero per term (STR l.1575-1578): later zeros enter at 1
                self.notes.append(f'{self.term}: later zero "{lab}" (0/{M:g}) enters at 1')
                return
            self.has_zero = True
        if N / M < 0.1:              # Poisson for binomial (STR l.1573)
            fid = f'{self.term}|{len(self.counted)}'
            self.spec['counted'][fid] = {'m': float(N), 'M': float(M), 'label': f'{self.term}: {lab}'}
            self.counted.append(fid); self.coeff /= M
        else:
            p = N / M
            self.coeff *= p; self.binom_p *= p; self.binom_s2 += (1.0 - p) / N
        return

    def counted_factor(self, N, M, lab):
        if self.run is not None and abs(M - self.run[0]) < 1e-9 and self.run[0] > 0:
            self.run = (N, self.run[1], self.run[2] + ' -> ' + lab)      # nested chain of one sample collapses
            return
        self._flush(); self.run = (float(N), float(M), lab)

    def fixed(self, v):
        self._flush(); self.coeff *= v

    def done(self):
        self._flush()
        return self


def _route_of_chain(term, factors, spec, notes, f1x=None, holds_zero=False):
    r = _Route(term, spec, notes); r.has_zero = holds_zero
    for f in factors:
        if f.get('value') is not None:
            if f.get('s_ln'):          # a probability without a population (v1: value 1, width 1) -> no credit
                notes.append(f'{term}: "{f["label"]}" value {f["value"]} width {f["s_ln"]} -> no credit (1, no width)')
            r.fixed(f['value'])
        else:
            r.counted_factor(f['N'], f['M'], f['label'])
    if f1x is not None and f1x['M'] >= 10:
        r.counted_factor(f1x['N'], f1x['M'], 'F1 ' + f1x.get('name', ''))
        if f1x.get('c', 1.0) > 1:
            r.fixed(f1x['c'])
    return r.done()


def _add_term(spec, r, base, cats_yield, nuis, kind):
    """One term = one sample (no weight classes in v1).  The term's binomial widths are combined into one nuisance
    (R1), censored at 1 (probability)."""
    nz = dict(nuis)
    if r.binom_s2 > 0:
        s = math.sqrt(r.binom_s2); n = 'binom_' + r.term
        nz[n] = s
        spec['nuis'][n] = {'bound': math.log(1.0 / r.binom_p) / s, 'kind': 'binomial, censored at 1'}
    spec['samples'].append({'name': r.term, 'term': r.term, 'kind': kind, 'counted': r.counted, 'nuis': nz,
                            'yield': {c: base * r.coeff * w for c, w in cats_yield.items()}})


def v1count(point='A2|F|200|1.5|BM', column='FB2', f1_name='h>5&o>5', reading='R1'):
    """The v1-count workspace at v1's selection `column`&`f1_name` (default: v1's best-point selection
    FB2&h>5&o>5) with the v2 treatment (readings R1).  Returns the spec; spec['meta'] holds the conversion notes
    and, per term, the v1 central value for comparison."""
    bg = json.loads((AN1 / 'background.json').read_text())
    bs = json.loads((AN1 / 'bsum_wp.json').read_text())
    srt = json.loads((AN1 / 'srt.json').read_text())['columns']
    n_trig = bs['n_trig']['value']
    cols = [e['column'] for e in bg['end_state']]
    col = cols.index(column)
    fp = bg['f1_factors'].get(column)
    f1x = None
    if fp and f1_name in fp:
        x = fp[f1_name]
        f1x = dict(N=x['N'], M=x['M'], name=f1_name, c=fp.get('c_density') or 1.0)
        if f1x['c'] > 1:
            log.warning('F1 density factor c = %s at %s: v1 applies it only if c - 2 sigma_c > 1; kept at 1 here',
                        f1x['c'], column)
            f1x['c'] = 1.0
    p = v1_point(point)
    spec = {'name': f'v1count_{column}&{f1_name}', 'cats': ['SR_T', 'SR_G'], 'mu_max': 1e5, 'mu_scale': 800.0,
            'signal': {'yield': {'SR_T': p['s'][0], 'SR_G': p['s'][1]}, 'nuis': {},
                       'label': f'v1 placeholder efficiency x {V1_NORM:g} ({point}); not a v2 signal efficiency'},
            'counted': {}, 'samples': [], 'nuis': {}, 'meta': {'point': point, 'v1': p, 'notes': [], 'v1_value': {}}}
    notes = spec['meta']['notes']
    both = {'SR_T': 1.0, 'SR_G': 1.0}
    for name in SHARED:
        spec['nuis'][name] = {'bound': None, 'kind': 'shared (v2arith.SHARED)'}
    esA, esT = bg['end_state'][col], bg['end_state_T'][col]
    if reading == 'R1p':
        _pileup_nocredit(spec, bg, srt, col, column, n_trig, f1x, notes)
    else:
        _pileup_estimator(spec, bg, srt, col, column, n_trig, f1x, notes, esA, esT)
    _v1count_rest(spec, bg, col, f1x, notes, both)
    used = {n for s in spec['samples'] for n in s['nuis']}
    spec['nuis'] = {n: d for n, d in spec['nuis'].items() if n in used}
    spec['name'] += '' if reading == 'R1' else '_R1p'
    spec['meta']['reading'] = reading
    return spec


def _pileup_nocredit(spec, bg, srt, col, column, n_trig, f1x, notes):
    """R1' (advisor ruling Tuva 2026-11-24 point 2; session log P0 R1'): v1's pile-up estimator (thinning, r.m.s. 0.61
    above the cap 0.135, STR l.432-434, l.1165) is not submitted -> no credit: the term enters at its no-credit value,
    the direct bound treated as counted (STR l.1565, l.1585-1588): N_trig x lambda / M_direct with the v1 direct count
    of the rho = 1 sample (background.json samples.B1_trials = 48,000; columns[FB2].B1_groups = 9 in SR-G,
    columns_T[FB2].B1_groups = 0 in SR-T).  No v1 pile-up estimator width enters (stat, model spread, closure, trend,
    density, T3); the N_trig normalisation width (ln 1.3) and the time-tag widths srt_pv, srt_sigt stay."""
    M = float(bg['samples']['B1_trials'])
    cA = next(c for c in bg['columns'] if c['column'] == column)
    cT = next(c for c in bg['columns_T'] if c['column'] == column)
    spec['counted']['PU_direct_G'] = {'m': float(cA['B1_groups']), 'M': M,
                                      'label': f'v1 direct pile-up count, SR-G, {column} (rho = 1, {M:g} trials)'}
    spec['counted']['PU_direct_T'] = {'m': float(cT['B1_groups']), 'M': M,
                                      'label': f'v1 direct pile-up count, SR-T (BTL present), {column}'}
    k = n_trig / M
    spec['samples'].append({'name': 'PU_G', 'term': 'PU_G', 'kind': 'no credit: direct bound (counted)',
                            'counted': ['PU_direct_G'], 'nuis': {'normalisation': SIGMA_NORM}, 'yield': {'SR_G': k}})
    spec['meta']['v1_value']['PU_G_nocredit_nominal'] = k * cA['B1_groups']
    sc = srt.get(column)
    if sc is None:
        return
    # SR-T: present x P(late) and not present x P_oot, each with its direct count replacing the estimator
    for nm, fid, fac in (('PU_T_late', 'PU_direct_T', sc.get('P_late')), ('PU_T_oot', 'PU_direct_G', sc.get('P_oot'))):
        r = _Route(nm, spec, notes)
        r.has_zero = spec['counted'][fid]['m'] == 0
        if fac is not None and fac['M'] >= 10:
            if fac['N'] == 0 and r.has_zero:
                notes.append(f'{nm}: time-tag fraction 0/{fac["M"]} enters at 1 (the direct count already holds the zero)')
            else:
                r.counted_factor(fac['N'], fac['M'], 'time-tag fraction ' + nm)
        r.done()
        if nm == 'PU_T_late' and sc.get('c_time', 1.0) > 1:
            r.coeff *= sc['c_time']
        nz = {'normalisation': SIGMA_NORM, 'srt_pv': sc.get('sigma_ln_PV', 1.0), 'srt_sigt': sc.get('sigma_ln_sigma_t', 1.0)}
        spec['samples'].append({'name': nm, 'term': nm, 'kind': 'no credit: direct bound x time tag',
                                'counted': [fid] + r.counted, 'nuis': nz, 'yield': {'SR_T': k * r.coeff}})


def _pileup_estimator(spec, bg, srt, col, column, n_trig, f1x, notes, esA, esT):
    """R1: v1's pile-up estimator output with its v1 log-normal components (session log P0 R1)."""
    # pile-up, SR-G: estimator output (v1 end state), log-normal components; 'stat' shared by the source column
    r = _route_of_chain('PU_G', [], spec, notes, f1x)
    comps = {k: v for k, v in esA['sigma_ln_components'].items() if v}
    nz = {('stat_PU_A' if k == 'stat' else k): v for k, v in comps.items()}
    spec['nuis']['stat_PU_A'] = {'bound': None, 'kind': 'v1 pile-up estimator statistics (column end_state)'}
    P = esA['base'] * esA['closure_factor'] * esA['trend_factor'] * esA.get('T3_factor', 1.0)
    _add_term(spec, r, n_trig * P, {'SR_G': 1.0}, nz, 'estimator (v1 pile-up)')
    spec['meta']['v1_value']['PU_G'] = n_trig * P
    # pile-up, SR-T: the two time-tag terms (v2arith.srt_pu, srt.json); the P_late / P_oot fractions are counted
    sc = srt.get(column)
    if sc is not None and esT.get('P_per_trial') is not None:
        for nm, base, fac, src, sk in (('PU_T_late', esT['P_per_trial'], sc.get('P_late'), esT, 'stat_PU_T'),
                                       ('PU_T_oot', esA['P_per_trial'], sc.get('P_oot'), esA, 'stat_PU_A')):
            zb = bool(src.get('zero_branch'))
            if zb:
                notes.append(f'{nm}: estimator holds a zero branch (v1 guard): its zero-count time-tag fraction '
                             'enters at 1 (one zero per term)')
            facs = [] if (fac is None or fac['M'] < 10) else [dict(N=fac['N'], M=fac['M'], value=None,
                                                                    label='time-tag fraction ' + nm)]
            r = _route_of_chain(nm, facs, spec, notes, f1x, holds_zero=zb)
            if nm == 'PU_T_late' and sc.get('c_time', 1.0) > 1:
                r.coeff *= sc['c_time']
            comps = {k: v for k, v in src['sigma_ln_components'].items() if v}
            nz = {(sk if k == 'stat' else k): v for k, v in comps.items()}
            nz['srt_pv'] = sc.get('sigma_ln_PV', 1.0); nz['srt_sigt'] = sc.get('sigma_ln_sigma_t', 1.0)
            spec['nuis'][sk] = {'bound': None, 'kind': 'v1 pile-up estimator statistics'}
            _add_term(spec, r, n_trig * base, {'SR_T': 1.0}, nz, 'estimator (v1 pile-up, time tag)')


def _v1count_rest(spec, bg, col, f1x, notes, both):
    """SM and single-interaction (C') terms of the v1-count workspace (same in R1 and R1')."""
    n_trig = json.loads((AN1 / 'bsum_wp.json').read_text())['n_trig']['value']
    # SM processes
    spec['nuis']['normalisation']['kind'] = 'shared: v1 sigma_norm = ln 1.3'
    for proc, sv in bg['sm'].items():
        if proc.startswith('_'):
            continue
        row = sv['rows'][col]; term = 'SM_' + proc
        if sv.get('proxy'):
            if row.get('B') is None:
                continue
            r = _route_of_chain(term, [], spec, notes, f1x)
            n = 'stat_' + term
            spec['nuis'][n] = {'bound': None, 'kind': 'v1 proxy width (no count)'}
            notes.append(f'{term}: v1 proxy (no counts): nominal {sv["N_trig"] * row["P_per_presel_event"]:.4g} with '
                         f'log-normal {row["s_ln"]:.3f}')
            _add_term(spec, r, sv['N_trig'] * row['P_per_presel_event'], both,
                      {n: row['s_ln'], 'normalisation': SIGMA_NORM}, 'v1 proxy')
            continue
        r = _route_of_chain(term, row['factors'], spec, notes, f1x)
        _add_term(spec, r, sv['sigma_pb'] * sv['K'] * 3.0e6, both, {'normalisation': SIGMA_NORM}, 'counted (SM)')
    # single-interaction terms (C')
    for t, cv in bg['cprime'].items():
        row = cv['rows'][col]
        if row.get('P_given_t') is None:
            continue
        term = 'CP_' + t
        rate = cv['rate']
        r = _route_of_chain(term, row['factors'], spec, notes, f1x)
        nz = {'normalisation': SIGMA_NORM}
        if rate.get('sigma_ln'):
            nz['rate_' + t] = rate['sigma_ln']; spec['nuis']['rate_' + t] = {'bound': None, 'kind': 'rate'}
        _add_term(spec, r, n_trig * rate['value'] * (0.22 if t.startswith('ni') else 1.0), both, nz, "counted (C')")


def term_table(spec):
    """Per term: route summary (counted m, M, kappa per category in events per unit lambda of its zero factor)."""
    rows = []
    for s in spec['samples']:
        rows.append(dict(term=s['term'], kind=s.get('kind'), yield_coeff=s['yield'],
                         counted=[(f, spec['counted'][f]['m'], spec['counted'][f].get('M')) for f in s['counted']],
                         nuis=s['nuis']))
    return rows


def predictive(spec, nmc=200000, seed=1, censor=True, terms=None):
    """Monte Carlo of the predictive distribution of each term and of B_c (STR l.1646-1650): every counted rate from
    Gamma(m + 1), every nuisance from N(0, 1) clipped at its bound.  Returns per term (B50, B84, mean) summed over
    categories and per category, and f0 (STR l.1661)."""
    ex = Explicit(spec, censor)
    rng = np.random.default_rng(seed)
    lam = np.where(ex.fixed[None, :], ex.fixval[None, :], rng.gamma(ex.m[None, :] + 1.0, size=(nmc, len(ex.m))))
    th = ex.clip_draw(np.minimum(rng.standard_normal((nmc, len(ex.nk))), ex.bound_gen[None, :]), rng)
    tp, tm = np.maximum(th, 0.0), np.minimum(th, 0.0)
    lb = np.log(lam) @ ex.A.T + tp @ ex.Wh.T + tm @ ex.Wl.T
    per = np.exp(lb)                         # (nmc, nsamp) x coeff per category
    out = {}; tot = np.zeros((nmc, len(ex.cats)))
    zero_mean = 0.0
    for i, s in enumerate(spec['samples']):
        b = per[:, i:i + 1] * ex.C[i][None, :]
        tot += b
        bs = b.sum(1)
        hz = any(spec['counted'][f]['m'] == 0 and spec['counted'][f].get('fixed') is None for f in s['counted'])
        out.setdefault(s['term'], dict(zero=hz, draws=np.zeros(nmc)))['draws'] += bs
    res = {}
    for t, d in out.items():
        x = d['draws']
        res[t] = dict(zero_count=d['zero'], B50=float(np.median(x)), B84=float(np.quantile(x, 0.84)),
                      mean=float(x.mean()))
        if d['zero']:
            zero_mean += float(x.mean())
    tot_all = tot.sum(1)
    cat = {c: dict(B16=float(np.quantile(tot[:, j], 0.16)), B50=float(np.median(tot[:, j])),
                   B84=float(np.quantile(tot[:, j], 0.84)), mean=float(tot[:, j].mean()))
           for j, c in enumerate(ex.cats)}
    for c in cat.values():
        c['sigma_ln'] = 0.5 * math.log(c['B84'] / c['B16']) if c['B16'] > 0 else None
    return dict(terms=res, cats=cat, f0=zero_mean / float(tot_all.mean()), nmc=nmc, seed=seed)


def leading_zero_term(spec, pred):
    z = {t: d for t, d in pred['terms'].items() if d['zero_count']}
    return max(z, key=lambda t: z[t]['B84']) if z else None


def zero_fid(spec, term):
    """The (one) zero-count counted factor of a term."""
    for s in spec['samples']:
        if s['term'] == term:
            for f in s['counted']:
                if spec['counted'][f]['m'] == 0:
                    return f
    return None


def with_alternative(spec, alt):
    """Alternatives of STR l.1619-1625 for T1-c (iv): 'fixed114' fixes every zero-count rate at 1.139 (no Gamma, no
    fit freedom); 'jeffreys' is a generation setting (Gamma(m + 1/2)) and leaves the spec unchanged."""
    sp = copy.deepcopy(spec)
    if alt == 'fixed114':
        for f, d in sp['counted'].items():
            if d['m'] == 0:
                d['fixed'] = U68
    sp['name'] = spec['name'] + '_' + alt
    return sp


# ------------------------------------------------------------------------------------- task 3: v2 term structure
B1_CLASSES = ('DIF', 'DIFC', 'NI22', 'NI30', 'NI61', 'NIX', 'NIC')       # COM l.344 (E4), ADD4
SM_PROCS = ('Znunu', 'Wtau_l', 'Wtau_h', 'ttbar_1l', 'Wenu', 'Wmunu', 'ttbar_2l', 'top_t', 'top_tW', 'WW', 'WZ', 'ZZ',
            'Ztautau', 'Zll_lost')                                         # fourteen SM processes (STR §0 l.45)
# PLACEHOLDER transfer factors (events per unit lambda at R09, ADD l.82 [U]: one count = 25.9, 23.9, 4.8 / 6.5 / 6.5,
# 23.2, 24.3 (B1), 4.0 (hard-scatter share), 41.2 full-weight / 2.1 low-weight Z(nunu)); used for every SM process
KAPPA_PH = {'DIF': 25.9, 'DIFC': 23.9, 'NI22': 4.8, 'NI30': 6.5, 'NI61': 6.5, 'NIX': 23.2, 'NIC': 24.3, 'HS': 4.0,
            'SM_full': 41.2, 'SM_low': 2.1, 'MJ': 41.2}


N_TRIG_V1 = 40848447.93138061      # v1 bsum_wp.json n_trig.value (placeholder for the v2 N_trig)
M_DIRECT_V2 = 96000.0               # the v2 direct trials (STR l.1586)


def v2_placeholder(point='A2|F|500|2|BM', fT_bkg=0.5, counts=None, pu_credit=True):
    """The v2 term structure of one T2 candidate (STR l.1559-1595, COM l.208 + l.355), every number a PLACEHOLDER:
    seven B1 classes (counted ceiling/geometry factor on the no-pile-up sample x survival S, an estimator output
    censored at 1) + the hard-scatter share (one term, ADD D5 H1); fourteen SM processes x two weight classes (one
    counted rate per class, COM l.355) x S_CKF (no credit: 1); the multijets (counted); the pile-up term (estimator
    output with its closure nuisance, censored at its no-credit value); signal from a v1 placeholder efficiency
    with its counted Monte Carlo statistics (an auxiliary channel, STR l.1595) and placeholder nuisances.
    Shared nuisance names (STR l.1590-1595): lumi, norm_<group>, pu_density, material, hit_res, hit_ineff, met,
    closure_<estimator>; signal: f200, trigger, vtx_id."""
    counts = counts or {}
    cats = ['SR_T', 'SR_G']
    w = {'SR_T': fT_bkg, 'SR_G': 1.0 - fT_bkg}
    p = v1_point(point)
    k_sig = 400                     # PLACEHOLDER number of signal MC rows (v1 placeholders on 400 rows, script [13])
    eff = sum(p['eff'])
    msig = round(eff * k_sig)
    spec = {'name': 'v2_placeholder', 'cats': cats, 'mu_max': 1e4, 'mu_scale': 1.0,
            'signal': {'yield': {c: (p['s'][i] / max(msig, 1)) for i, c in enumerate(cats)}, 'counted': ['sigMC'],
                       'nuis': {'lumi': 0.01, 'f200': [0.025, 0.029], 'trigger': 0.05, 'vtx_id': 0.02, 'met': 0.05,
                                'material': 0.02, 'hit_res': 0.02, 'hit_ineff': 0.02},
                       'label': f'PLACEHOLDER: v1 placeholder efficiency ({point}) x {V1_NORM:g}; MC statistics '
                                f'{msig} of {k_sig} placeholder rows; nuisance widths placeholders'},
            'counted': {'sigMC': {'m': float(msig), 'label': 'signal MC statistics (placeholder)'}},
            'samples': [], 'nuis': {}, 'meta': {'placeholder': True, 'point': point}}
    nz = spec['nuis']
    for n in ('lumi', 'f200', 'trigger', 'vtx_id', 'met', 'material', 'hit_res', 'hit_ineff', 'pu_density'):
        nz[n] = {'bound': None, 'kind': 'shared'}
    nz['closure_B1'] = {'bound': None, 'kind': 'closure nuisance of the B1 estimator'}
    for cl in B1_CLASSES + ('HS',):
        f = 'B1_' + cl
        spec['counted'][f] = {'m': float(counts.get(f, 0)), 'label': f'B1 {cl}: ceiling count on its own sample'}
        S0, sS = 0.3, 1.41           # PLACEHOLDER survival and its s_tot (STR §4.0 table, pi_k tested at R06 only)
        nz['S_' + cl] = {'bound': math.log(1.0 / S0) / sS, 'kind': 'survival S, censored at 1'}
        spec['samples'].append({'name': f, 'term': f, 'kind': 'counted x estimator', 'counted': [f],
                                'yield': {c: KAPPA_PH[cl] * S0 * w[c] for c in cats},
                                'nuis': {'S_' + cl: sS, 'closure_B1': 0.231, 'material': 0.05, 'hit_res': 0.03,
                                         'hit_ineff': 0.03, 'pu_density': 0.05, 'lumi': 0.01}})
    groups = {'Znunu': 'V', 'Wtau_l': 'V', 'Wtau_h': 'V', 'Wenu': 'V', 'Wmunu': 'V', 'Ztautau': 'V', 'Zll_lost': 'V',
              'ttbar_1l': 'top', 'ttbar_2l': 'top', 'top_t': 'top', 'top_tW': 'top', 'WW': 'VV', 'WZ': 'VV', 'ZZ': 'VV'}
    for g in set(groups.values()):
        nz['norm_' + g] = {'bound': None, 'kind': 'N_trig normalisation per process group'}
    for pr in SM_PROCS:
        for cls, kap in (('full', KAPPA_PH['SM_full']), ('low', KAPPA_PH['SM_low'])):
            f = f'SM_{pr}_{cls}'
            spec['counted'][f] = {'m': float(counts.get(f, 0)), 'label': f'SM {pr}, {cls}-weight class'}
            spec['samples'].append({'name': f, 'term': 'SM_' + pr, 'kind': 'counted, weighted', 'counted': [f],
                                    'yield': {c: kap * w[c] for c in cats},
                                    'nuis': {'norm_' + groups[pr]: 0.17, 'met': 0.10, 'lumi': 0.01,
                                             'material': 0.02, 'hit_res': 0.02, 'hit_ineff': 0.02}})
    spec['counted']['MJ'] = {'m': float(counts.get('MJ', 0)), 'label': 'multijets'}
    spec['samples'].append({'name': 'MJ', 'term': 'MJ', 'kind': 'counted', 'counted': ['MJ'],
                            'yield': {c: KAPPA_PH['MJ'] * w[c] for c in cats}, 'nuis': {'met': 0.3, 'lumi': 0.01}})
    # pile-up: estimator output (placeholder 5 events at R09, width 0.59, STR §4.0 table), bounded by its no-credit
    # value N_trig x 1.139 / 96,000 = 485 events (STR l.1586-1588) -- fit bound at the 68 % value (open point)
    # pile-up (STR l.1565, l.1585-1588, l.953-954; advisor ruling 2026-11-24 point 8):
    #  credited estimator: nominal x exp(s theta); fit bound at the 68 % value of its no-credit bound (485 events),
    #    generation draws the bound: theta clipped at ln(N_trig lambda / 96,000 / nominal) / s, lambda ~ Gamma(1)
    #    (key 'bound_draw'); PREREG variant: fit bound at the 95 % value (2.996 x 425.5 = 1,275 events).
    #  no credit: a counted factor, m = 0 of M = 96,000 direct trials, free lambda (no fixed bound).
    pu0, spu = 5.0, 0.59
    k_nc = N_TRIG_V1 / M_DIRECT_V2
    if pu_credit:
        nz['closure_PU'] = {'bound': math.log(U68 * k_nc / pu0) / spu, 'kind': 'pile-up closure, bounded at no-credit',
                            'bound_draw': {'kappa': k_nc, 'm': 0.0, 'phi0': pu0, 's': spu},
                            'bound_95': math.log(-math.log(0.05) * k_nc / pu0) / spu}
        spec['samples'].append({'name': 'PU', 'term': 'PU', 'kind': 'estimator', 'counted': [],
                                'yield': {c: pu0 * w[c] for c in cats},
                                'nuis': {'closure_PU': spu, 'pu_density': 0.1, 'hit_res': 0.05, 'hit_ineff': 0.05}})
    else:
        spec['counted']['PU_nc'] = {'m': 0.0, 'M': M_DIRECT_V2, 'label': 'pile-up no credit: direct trials, 0 of 96,000'}
        spec['samples'].append({'name': 'PU', 'term': 'PU', 'kind': 'no credit: direct bound (counted)',
                                'counted': ['PU_nc'], 'yield': {c: k_nc * w[c] for c in cats},
                                'nuis': {'pu_density': 0.1}})
        spec['name'] = 'v2_placeholder_pu_nocredit'
    return spec


def n_parameters(spec):
    nk = {n for s in [spec['signal']] + spec['samples'] for n, w in s.get('nuis', {}).items() if max(_w(w)) > 0}
    return 1 + len(spec['counted']) + len(nk)
