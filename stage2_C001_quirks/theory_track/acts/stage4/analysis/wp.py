"""wp.py -- assemble the full B sum per category and rung (WP_RULE §4.1, PC-19 for SR-T), B84, and the WP rule.

B_c(r) = N_trig x P_PU,c(r) + sum_s B_SM,s(r) + sum_t N_trig rate_t P(r | t)      (+ B_cosmic + B_halo: arguments only,
                                                                                 not in this sum; flagged)
  SR-G (category G): P_PU,G(r) = the full-column B_PU (conservative reading: no subtraction of the SR-T candidates).
  SR-T (category T): P_PU,T(r) = P(r & BTL) x P(late) + P(r & no BTL) x P_OOT  (PC-19 composition), each summand a §4.2
                     term; timing sigma_ln,PV and sigma_ln,sigma_t added to both summands.
  SM, C': no time-tag credit in SR-T (conservative reading: enter both categories in full).
Ladder rungs 1..14 = in-job columns 0..13; R15-R20 = R14 x p(h/o | R14); R21-R23 = F0e>x x p(h>5 & o>5 | F0e>x);
fallback selections = FB_k[e] x p(h>5 & o>5 | FB_k[e]).
"""
import numpy as np

from acts.stage4.analysis import common as C
from acts.stage4.analysis import stats as ST
from acts.stage4.analysis.background import Term

F1_OF_RUNG = {15: ('h>2', 13), 16: ('h>3', 13), 17: ('h>5', 13), 18: ('h>5&o>2', 13), 19: ('h>5&o>3', 13),
              20: ('h>5&o>5', 13), 21: ('h>5&o>5', 14), 22: ('h>5&o>5', 15), 23: ('h>5&o>5', 16)}


def f1_factor(f1, parent_col, name):
    fp = f1.get(C.RUNGS[parent_col]) if f1 else None
    if not fp or fp.get('population') is None or name not in fp:
        return None, dict(note='F1 conditional unavailable: factor 1 (no rejection credited)')
    x = fp[name]
    c = fp.get('c_density')
    # correlation factor: applied if c > 1 at 2 sigma (binomial sigma of the bin ratio, approximate)
    c_apply = 1.0
    if c is not None and c > 1:
        nb = [b for b in fp['density_bins'] if b['p'] is not None and b['M']]
        if nb:
            b = max(nb, key=lambda q: q['p'])
            sc = c * np.sqrt(1 / max(b['N'], 1) + 1 / max(x['N'], 1)) if x['N'] else np.inf
            if c - 2 * sc > 1:
                c_apply = c
    return dict(N=x['N'], M=x['M'], s_ln=x.get('s_ln'), population=fp['population'], c=c_apply), None


P_PV_LINE = 0.22      # WP_RULE §4.1 l.318-320: B_NI = sum_r (NIs/event at r) x P_PV-line x P(pass | r) x N_trig


def add_guarded(T, label, N, M, s_ln, holds_bound):
    """REVIEW_ANALYSIS_R1 A-2: WP_RULE §4.2 'a bound enters at most once per term'.  A zero factor appended to a
    term whose base already carries its 1.14/M bound enters as 1 (the pu_term guard, the more conservative of the two
    readings the reviewer allows: the base keeps its bound)."""
    if N == 0 and holds_bound:
        T.add(f'{label} = 0/{M:g} but the term already holds its bound: enters as 1', None, None, value=1.0, s_ln=0.0)
    else:
        T.add(label, N, M, s_ln=s_ln)


def f1_credited(f1x):
    """D8 (decided): T3s is required only if an h/o factor < 1 is credited."""
    return f1x is not None and f1x['M'] >= 10 and f1x['N'] < f1x['M']


def pu_term(es_col, f1x, n_trig, label):
    """One PU term = in-job column end state (value per trial, sigma components) [x F1 conditional (zero rule)]."""
    if es_col.get('P_per_trial') is None:
        return None
    T = Term(label)
    T.add('P_PU column end state', None, None, value=es_col['P_per_trial'], s_ln=0.0)
    zb = bool(es_col.get('zero_branch'))
    if f1x is not None:
        add_guarded(T, f"p(F1 | {f1x['population']})", f1x['N'], f1x['M'], f1x['s_ln'], zb)
        if f1x['c'] > 1:
            T.add('c (F1 density-bin correlation)', None, None, value=f1x['c'], s_ln=0.0)
    ev = T.evaluate()
    comps = dict(es_col['sigma_ln_components'])
    comps['stat'] = float(np.sqrt(comps.get('stat', 0.0) ** 2 + ev['s_ln'] ** 2))
    return dict(label=label, value=n_trig * ev['value'], comps=comps, zero_branch=zb or ev['zero_branch'],
                factors=ev['factors'], trend_factor=es_col.get('trend_factor', 1.0))


def srt_pu_term(es_T, es_all, f1x, srt_col, n_trig, label):
    """PC-19 SR-T PU term: P(r & BTL) P(late) + P(r & no BTL) P_OOT, each summand ONE §4.2 term (A-2 guard).
    A-1: P(r & no BTL) = P(r) - P(r & BTL) only where both columns are thinning estimates reachable at rho = 2 (PC-18
    'both in-job'); elsewhere the full-column end state P(r) >= P(r & no BTL) is used (conservative)."""
    if es_T.get('P_per_trial') is None or es_all.get('P_per_trial') is None or srt_col is None:
        return []
    out = []
    both_thin = bool(es_T.get('reachable_rho2')) and bool(es_all.get('reachable_rho2'))
    p_t = es_T['P_per_trial']
    if both_thin:
        p_nt = es_all['P_per_trial'] - p_t
        nt_src = es_all
        if p_nt <= 0:                    # never enter a zero: fall back to the full column (conservative)
            p_nt, both_thin = es_all['P_per_trial'], False
    else:
        p_nt, nt_src = es_all['P_per_trial'], es_all
    for nm, base, fac, src in (('present x P(late)', p_t, srt_col.get('P_late'), es_T),
                               ('not present x P_OOT', p_nt, srt_col.get('P_oot'), nt_src)):
        T = Term(label + ' ' + nm)
        zb = bool(src.get('zero_branch'))
        T.add('base' + (' (full column, A-1)' if nm.startswith('not') and not both_thin else ''), None, None,
              value=base, s_ln=0.0)
        if f1x is not None:
            add_guarded(T, f"p(F1 | {f1x['population']})", f1x['N'], f1x['M'], f1x['s_ln'], zb)
        if fac is None or fac['M'] < 10:
            T.add('timing factor: no population with M >= 10', None, None, value=1.0, s_ln=1.0)
        else:
            zb2 = zb
            add_guarded(T, 'timing factor', fac['N'], fac['M'], None, zb2)
            if nm.startswith('present') and srt_col.get('c_time', 1.0) > 1:     # B-4: time-independence failure
                T.add('c_time (SR-T time-independence failed)', None, None, value=srt_col['c_time'], s_ln=0.0)
        ev = T.evaluate()
        comps = dict(src['sigma_ln_components'])
        comps['stat'] = float(np.sqrt(comps.get('stat', 0.0) ** 2 + ev['s_ln'] ** 2))
        comps['srt_pv'] = srt_col.get('sigma_ln_PV', 1.0); comps['srt_sigt'] = srt_col.get('sigma_ln_sigma_t', 1.0)
        nb = sum(1 for f in ev['factors'] if f.get('zero_bound')) + int(zb)
        out.append(dict(label=T.name, value=n_trig * ev['value'], comps=comps, zero_branch=zb or ev['zero_branch'],
                        factors=ev['factors'], n_bounds=nb, trend_factor=src.get('trend_factor', 1.0)))
    return out


def _f1_on_row(val, st, zb, f1x):
    """F1 factor on an SM / C' row as one §4.2 term with the A-2 guard."""
    if f1x is None or f1x['M'] < 10:
        return val, st, zb
    T = Term('row x F1')
    T.add('row', None, None, value=val, s_ln=0.0)
    add_guarded(T, 'p(F1)', f1x['N'], f1x['M'], f1x['s_ln'], zb)
    ev = T.evaluate()
    return ev['value'], float(np.sqrt(st ** 2 + ev['s_ln'] ** 2)), zb or ev['zero_branch']


def sm_terms(sm, col, sigma_norm, f1x):
    """A-3: the SM row of the column's own requirement set (rows exist for every COL_REQ column 0-36)."""
    out = []
    for s, v in (sm or {}).items():
        if s.startswith('_'):
            if s == '_error':
                out.append(dict(label='SM', value=None, missing=v))
            continue
        r = v['rows'][col]
        if r.get('B') is None:
            out.append(dict(label=f'SM {s}', value=None, missing='cross section'))
            continue
        val, st, zb = _f1_on_row(r['B'], r['s_ln'], bool(r['zero_branch']), f1x)
        out.append(dict(label=f'SM {s}' + (' [PROXY]' if v.get('proxy') else ''), value=val,
                        comps=dict(stat=st, normalisation=sigma_norm), zero_branch=zb))
    return out


def cp_terms(cp, col, n_trig, sigma_norm, f1x):
    """A-3: the C' row of the column's own requirement set."""
    out = []
    for t, v in (cp or {}).items():
        r = v['rows'][col]
        rate = (v.get('rate') or {}).get('value')
        if r.get('P_given_t') is None:
            out.append(dict(label=f"C' {t}", value=None, missing=r.get('missing', 'P(pass | t) missing')))
            continue
        if rate is None:
            out.append(dict(label=f"C' {t}", value=None, missing='rate_t (Pythia generator-level, per triggered event '
                                                                 'in the road) not provided'))
            continue
        pv_line = P_PV_LINE if t.startswith('ni') else 1.0          # WP_RULE.md:318 (B_NI only; DIF: factor 1, l.321)
        base = n_trig * rate * pv_line * r['P_given_t']
        # D11 (DECIDED 2026-10-16, FIX R6): the C' h/o factor in BOTH readings -- the B1-PU F1 conditional
        # (implemented reading) and the C'0 factor (literal WP_RULE §7; = 1, no rejection credited, because the C'0
        # outputs carry no S4 hit records, background.cprime_term 'ho_c0') -- the LARGER B is used (tie: larger sigma)
        rA = _f1_on_row(base, r['s_ln'], bool(r['zero_branch']), f1x)
        rB = (base, r['s_ln'], bool(r['zero_branch']))
        useB = (rB[0], rB[1]) > (rA[0], rA[1])
        val, st, zb = rB if useB else rA
        rs = (v.get('rate') or {}).get('sigma_ln', 0.0)
        out.append(dict(label=f"C' {t}", value=val, comps=dict(stat=st, normalisation=sigma_norm, rate=rs),
                        zero_branch=zb, ho_reading=("C'0 (factor 1)" if useB else 'B1-PU F1') if f1x is not None
                        else None))
    return out


def assemble(es_all, es_T, f1, srt_cols, sm, cp, n_trig, sigma_norm, trend_fn=None):
    """-> dict(T=[23 rungs], G=[23 rungs], FB={name: {T, G}}) with terms and B84.  trend_fn(x) -> (sigma, factor):
    the trend term is re-evaluated at the ladder index of the rung itself for R15-R20 (WP_RULE §6.4 'extrapolated to
    the WP rung')."""
    res = {'T': [], 'G': [], 'FB': {}}
    flags = set()
    if sm is None:
        flags.add('SM (C) term not provided')
    if cp is None:
        flags.add("C' terms not provided")

    def retrend(terms, x):
        if trend_fn is None:
            return terms
        s_new, f_new = trend_fn(x)
        for t in terms:
            if t['label'].startswith('PU') and 'trend' in t['comps']:
                t['comps'] = dict(t['comps'], trend=s_new)
                t['value'] = t['value'] * f_new / max(t.get('trend_factor', 1.0), 1e-300)   # B-9 (ii)
        return terms

    def build(col_inj, f1x, label):
        tG = []; tT = []
        p = pu_term(es_all[col_inj], f1x, n_trig, f'PU {label}')
        if p:
            tG.append(p)
        tT += srt_pu_term(es_T[col_inj] if es_T else {}, es_all[col_inj], f1x,
                          (srt_cols or {}).get(C.RUNGS[col_inj]), n_trig, f'PU-SRT {label}')
        if f1_credited(f1x):
            flags.add(f'T3s REQUIRED (D8): an h/o factor < 1 is credited at {label} ({f1x["N"]}/{f1x["M"]})')
        others = sm_terms(sm, col_inj, sigma_norm, f1x) + cp_terms(cp, col_inj, n_trig, sigma_norm, f1x)
        for o in others:
            if o.get('value') is None:
                flags.add(o['label'] + ': ' + o.get('missing', 'missing'))
                continue
            tG.append(o); tT.append(o)
        return tT, tG

    for r in range(1, 24):
        if r <= 14:
            col = r - 1; f1x = None
        else:
            name, col = F1_OF_RUNG[r]
            f1x, why = f1_factor(f1, col, name)
        tT, tG = build(col, f1x, C.LADDER_NAMES[r - 1])
        if 15 <= r <= 20:
            tT = retrend(tT, r); tG = retrend(tG, r)
        for c, terms in (('T', tT), ('G', tG)):
            if not terms:
                res[c].append(dict(rung=r, name=C.LADDER_NAMES[r - 1], B84=None, terms=[])); continue
            b84, med, mean = ST.b84(terms, nmc=100_000)
            res[c].append(dict(rung=r, name=C.LADDER_NAMES[r - 1], B84=b84, B_median=med, B_mean=mean,
                               zero_branch=any(t.get('zero_branch') for t in terms),
                               terms=[dict(label=t['label'], value=t['value'], comps=t['comps'],
                                           zero_branch=t.get('zero_branch')) for t in terms]))
    for fbn in C.RUNGS[17:37]:
        col = C.COL[fbn]
        f1x, why = f1_factor(f1, col, 'h>5&o>5')
        tT, tG = build(col, f1x, fbn + '&h>5&o>5')
        res['FB'][fbn + '&h>5&o>5'] = {}
        for c, terms in (('T', tT), ('G', tG)):
            b84, med, mean = ST.b84(terms, nmc=100_000) if terms else (None, None, None)
            res['FB'][fbn + '&h>5&o>5'][c] = dict(B84=b84, B_median=med, B_mean=mean,
                                                  zero_branch=any(t.get('zero_branch') for t in terms),
                                                  terms=[dict(label=t['label'], value=t['value'], comps=t['comps'])
                                                         for t in terms])
    res['missing_inputs'] = sorted(flags)
    res['complete'] = not flags
    res['not_in_sum'] = ['B_cosmic: argument only (plan §4.2: expected << 0.1 events; CMS cosmic rate UNVERIFIED)',
                         'B_halo: argument only (plan §4.2: negligible)']                                 # C-1
    res['T3s_required'] = any(f.startswith('T3s REQUIRED') for f in flags)
    return res


def apply_rule(lad):
    b84T = [x['B84'] for x in lad['T']]; b84G = [x['B84'] for x in lad['G']]
    termsT = [[dict(value=t['value'], comps=t['comps']) for t in x['terms']] for x in lad['T']]
    termsG = [[dict(value=t['value'], comps=t['comps']) for t in x['terms']] for x in lad['G']]
    out = ST.wp_rule(b84T, b84G, termsT, termsG)
    out['complete_inputs'] = lad['complete']
    if not lad['complete']:
        out['WARNING'] = ('B sum incomplete (missing inputs: ' + '; '.join(lad['missing_inputs']) +
                          ') -> WP NOT VALID for a result')
    return out
