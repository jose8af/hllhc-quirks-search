"""M1_analysis.py -- E2: merge per-event per-crossing tables of M1_events.py -> results/M1.json + stdout tables.

Per (m, Lambda), causal 'prod' (max_boost 1e-2) files, crossings with r_lab < 108.3 cm (inside the barrel tracker):
  b_odd, b_odd/(eps_perp l_k)   (eps_perp = q|E*_perp|/sigma at the crossing, l_k = separation amplitude before it)
  b_even, b_even growth per crossing pair (slope of b_even vs crossing index; causal prod is NOT converged for b_even,
         use 'fine' and the conformal subset)
  |cos(b_odd, E*_perp)|
  psi_odd/eps_perp, psi_even/eps_perp: out-of-plane apsidal (axis) rotation across odd / even crossings, signed relative
         to E*_perp (reference: sign of b_N at odd crossings)
  kappa: log slope of the string impulse profile at odd crossings (units sigma b / v)
  and the predictions of the CM-frame M2 laws evaluated per crossing at the event's gamma*, eps_perp:
         psi_odd(M2b fit, interpolated in ln(gamma*-1)), psi_odd(M2a law at the measured b_odd), b_odd(M2b).
Uncertainties: event-block bootstrap (resample events, pool their crossings), 1000 resamples.
Convergence / solver checks: per-crossing relative differences prod vs fine (same events) and causal fine vs conformal.
Run: pixi run python analytic/numerics/M1_analysis.py
"""
import os, sys, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from nm_stats import dump

RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'M1')
MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.6, 1.0, 2.0, 3.0, 5.0, 10.0]
R_TRK = 108.3


def load(m, lam, setting):
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, f"m{m:g}_L{lam:g}_e*_{setting}.npz"))):
        z = np.load(f, allow_pickle=True)
        if not bool(z['valid']) or len(z['T']) == 0:
            continue
        keys = [str(k) for k in z['keys']]
        T = z['T']
        d = {k: T[:, i] for i, k in enumerate(keys)}
        d['kappa'] = z['fits'][:, 0]; d['kappa0'] = z['fits'][:, 1]
        d['iev'] = int(f.split('_e')[1][:3])
        for k in ('m', 'lam', 'sig', 'Th', 'gstar', 'pt', 'eta', 'lmax', 'Estar', 'nsteps', 'cpu'):
            d[k] = float(z[k])
        out.append(d)
    return out


def m2_laws():
    """Interpolators of the M2 CM-frame fits in x = ln(gamma*-1)."""
    js = json.load(open(os.path.join(HERE, 'results', 'M2.json')))
    gs = np.array([1.05, 1.3, 2.0, 3.0]); x = np.log(gs - 1)
    Ao = np.array([js['M2b'][f'g{g:g}_th90_causal0.001']['A_odd'] for g in gs])
    Ko = np.array([js['M2b'][f'g{g:g}_th90_causal0.001']['K_odd'] for g in gs])
    pe = np.array([js['M2b'][f'g{g:g}_th90_causal0.001']['psi_even_over_eps'] for g in gs])
    bo = np.array([js['M2b'][f'g{g:g}_th90_causal0.001']['b_odd_over_eps_l0'] for g in gs])
    A = np.array([js['M2a'][f'{g:g}']['causal0.01']['A'] for g in gs])
    K = np.array([js['M2a'][f'{g:g}']['causal0.01']['K'] for g in gs])
    kap = np.array([js['M2a'][f'{g:g}']['causal0.01']['kappa_med'] for g in gs])
    f = lambda arr: (lambda g: np.interp(np.log(np.clip(g, 1.05, 3.0) - 1), x, arr))
    cb = bo / (2 * (gs - 1))                      # b_odd/(eps l_max)
    return dict(Ao=f(Ao), Ko=f(Ko), pe=f(pe), bo=f(bo), cb=f(cb), A=f(A), K=f(K), kappa=f(kap))


def per_crossing(evs, laws):
    rows = []
    for d in evs:
        ins = (d['r_lab'] < R_TRK) & (d['k'] >= 1)
        odd = ins & (d['parity'] == 1); even = ins & (d['parity'] == 0)
        if odd.sum() == 0:
            continue
        # direction of E*_perp (= b_odd direction, |cos| ~ 1) in the (eN, eP) basis, per event
        uN = np.nanmedian(d['bN'][odd] / d['b'][odd]); uP = np.nanmedian(d['bP'][odd] / d['b'][odd])
        nu = np.hypot(uN, uP); uN /= nu; uP /= nu
        sE = np.sign(np.nanmedian(d['bN'][odd]))
        l0 = d['m'] / d['sig']
        eps = d['E_perp'] / d['sig']
        g = d['gstar']
        psi = d['dA_N'] * uN + d['dA_P'] * uP          # axis rotation projected on E*_perp
        psi_N = d['dA_N'] * sE                         # out-of-plane (lab-plane normal) component
        for i in np.where(ins)[0]:
            e = eps[i]
            row = dict(iev=d['iev'], k=d['k'][i], parity=d['parity'][i], b=d['b'][i], eps=e, l=d['l_before'][i],
                       l0=l0, gstar=g, psi=psi[i] / e, cosbE=abs(d['cos_b_E'][i]), kappa=d['kappa'][i],
                       g1=d['gamma1'][i], aN=d['aN'][i] * sE, psiN=psi_N[i] / e, uN=abs(uN))
            if d['parity'][i] == 1:
                row['b_norm'] = d['b'][i] / (e * d['l_before'][i]) if np.isfinite(d['l_before'][i]) else np.nan
                row['b_pred'] = laws['cb'](g) * e * d['l_before'][i]
                row['psi_pred_M2b'] = laws['Ao'](g) * np.log(1 / e) + laws['Ko'](g)
                bl = d['b'][i] / l0
                row['psi_pred_M2a'] = (bl * (laws['A'](g) * np.log(1 / bl) + laws['K'](g))) / e
                row['kappa_pred'] = laws['kappa'](g)
            else:
                row['psi_pred_M2b'] = laws['pe'](g)
            rows.append(row)
    return rows


class Pooled:
    """Per-event column arrays for a fast event-block bootstrap."""

    def __init__(self, rows):
        self.ev = sorted(set(r['iev'] for r in rows))
        keys = set().union(*[r.keys() for r in rows]) if rows else set()
        self.cols = {}
        for e in self.ev:
            rr = [r for r in rows if r['iev'] == e]
            self.cols[e] = {k: np.array([r.get(k, np.nan) for r in rr], float) for k in keys}

    def cat(self, evlist):
        out = {}
        for k in self.cols[self.ev[0]]:
            out[k] = np.concatenate([self.cols[e][k] for e in evlist])
        return out


def block_boot(P, fn, n_boot=500, seed=7):
    val = fn(P.cat(P.ev))
    rng = np.random.default_rng(seed)
    bs = np.array([fn(P.cat(rng.choice(P.ev, len(P.ev)))) for _ in range(n_boot)], float)
    bs = bs[np.isfinite(bs)]
    return float(val), float(np.std(bs)) if len(bs) else np.nan


def med_of(key, par=None):
    def f(c):
        a = c[key] if par is None else c[key][c['parity'] == par]
        a = a[np.isfinite(a)]
        return np.median(a) if len(a) else np.nan
    return f


def b_even_growth(evs):
    """Per event slope of b_even vs crossing index (least squares) and intercept; returns medians."""
    sl = []; ic = []
    for d in evs:
        sel = (d['parity'] == 0) & (d['r_lab'] < R_TRK) & (d['k'] >= 1)
        if sel.sum() >= 3:
            p = np.polyfit(d['k'][sel], d['b'][sel], 1)
            sl.append(p[0] * 2); ic.append(p[1])
    return float(np.median(sl)) if sl else np.nan, float(np.median(ic)) if ic else np.nan


def compare(evA, evB, keys=('b', 'dA_N', 'kappa')):
    """Per-crossing relative differences between two settings on the same events (matched by event and k)."""
    B = {d['iev']: d for d in evB}
    out = {}
    for par in (1, 0):
        for key in keys:
            rel = []
            for d in evA:
                e = B.get(d['iev'])
                if e is None:
                    continue
                n = min(len(d['k']), len(e['k']))
                sel = (d['parity'][:n] == par) & (d['r_lab'][:n] < R_TRK) & (d['k'][:n] == e['k'][:n])
                a = d[key][:n][sel]; b = e[key][:n][sel]
                ok = np.isfinite(a) & np.isfinite(b) & (np.abs(b) > 0)
                rel += list(a[ok] / b[ok] - 1)
            rel = np.abs(np.array(rel))
            out[f"{'odd' if par else 'even'}_{key}"] = dict(n=int(len(rel)), median_absrel=float(np.median(rel)) if len(rel) else np.nan,
                                                          p95_absrel=float(np.quantile(rel, 0.95)) if len(rel) else np.nan)
    return out


if __name__ == '__main__':
    laws = m2_laws()
    res = {}; cpu = 0.0
    print('| m | Λ | nev | ncross(in) | b_odd med [Å] | b_odd/(ε⊥ l) | b_odd/b_pred(M2b) | |cos(b,E*⊥)| | b_even med [Å] (prod) | ψ_odd/ε⊥ | pred M2b | pred M2a(b) | ψ_even/ε⊥ | pred | κ | κ pred |')
    for m in MASSES:
        for lam in LAMS:
            evs = load(m, lam, 'prod')
            if not evs:
                continue
            cpu += sum(d['cpu'] for d in evs)
            rows = per_crossing(evs, laws)
            P = Pooled(rows)
            q = {}
            for name, key, par in (('b_odd', 'b', 1), ('b_odd_norm', 'b_norm', 1), ('b_even', 'b', 0),
                                   ('psi_odd', 'psi', 1), ('psi_even', 'psi', 0), ('kappa_odd', 'kappa', 1),
                                   ('psi_odd_pred_M2b', 'psi_pred_M2b', 1), ('psi_odd_pred_M2a', 'psi_pred_M2a', 1),
                                   ('psi_even_pred_M2b', 'psi_pred_M2b', 0), ('kappa_pred', 'kappa_pred', 1),
                                   ('cosbE', 'cosbE', 1), ('eps', 'eps', 1), ('gstar', 'gstar', 1),
                                   ('psiN_odd', 'psiN', 1), ('psiN_even', 'psiN', 0), ('uN', 'uN', 1)):
                q[name] = block_boot(P, med_of(key, par))
            o = lambda c: c['parity'] == 1
            q['b_odd_over_pred'] = block_boot(P, lambda c: np.nanmedian((c['b'] / c['b_pred'])[o(c)]))
            q['psi_odd_minus_M2b'] = block_boot(P, lambda c: np.nanmedian((c['psi'] - c['psi_pred_M2b'])[o(c)]))
            q['psi_even_minus_M2b'] = block_boot(P, lambda c: np.nanmedian((c['psi'] - c['psi_pred_M2b'])[~o(c)]))
            q['kappa_minus_M2a'] = block_boot(P, lambda c: np.nanmedian((c['kappa'] - c['kappa_pred'])[o(c)]))
            # per crossing-pair axis rotation (odd + following even), per unit eps: what accumulates in the tracker
            q['psi_pair'] = block_boot(P, lambda c: np.nanmedian(c['psi'][o(c)]) + np.nanmedian(c['psi'][~o(c)]))
            q['b_even_growth_per_pair_prod'], q['b_even_intercept_prod'] = b_even_growth(evs)
            fine = load(m, lam, 'fine')
            if fine:
                q['b_even_growth_per_pair_fine'], q['b_even_intercept_fine'] = b_even_growth(fine)
                rf = per_crossing(fine, laws)
                Pf = Pooled(rf)
                q['b_even_fine'] = block_boot(Pf, med_of('b', 0))
                q['psi_odd_fine'] = block_boot(Pf, med_of('psi', 1))
                q['psi_even_fine'] = block_boot(Pf, med_of('psi', 0))
                q['convergence_prod_vs_fine'] = compare(evs, fine)
                cpu += sum(d['cpu'] for d in fine)
            for N in (256, 1024):
                conf = load(m, lam, f'conf{N}')
                if conf:
                    cpu += sum(d['cpu'] for d in conf)
                    q[f'conf{N}_vs_fine'] = compare(fine, conf) if fine else None
                    q[f'b_even_growth_per_pair_conf{N}'], q[f'b_even_intercept_conf{N}'] = b_even_growth(conf)
                    q[f'conf{N}_gstar'] = [d['gstar'] for d in conf]
            q['nev'] = len(evs); q['ncross_in'] = len(rows)
            res[f'm{m:g}_L{lam:g}'] = q
            A = lambda k: q[k][0]
            print(f"| {m:.0f} | {lam:g} | {len(evs)} | {len(rows)} | {A('b_odd')*1e8:.4g}±{q['b_odd'][1]*1e8:.2g} | {A('b_odd_norm'):.3f}±{q['b_odd_norm'][1]:.3f} | "
                  f"{A('b_odd_over_pred'):.3f}±{q['b_odd_over_pred'][1]:.3f} | {A('cosbE'):.5f} | {A('b_even')*1e8:.3g} | {A('psi_odd'):.3f}±{q['psi_odd'][1]:.3f} | "
                  f"{A('psi_odd_pred_M2b'):.3f} | {A('psi_odd_pred_M2a'):.3f} | {A('psi_even'):.3f}±{q['psi_even'][1]:.3f} | {A('psi_even_pred_M2b'):.3f} | "
                  f"{A('kappa_odd'):.3f}±{q['kappa_odd'][1]:.3f} | {A('kappa_pred'):.3f} |", flush=True)
    res['cpu_seconds_total_jobs'] = cpu
    res['description'] = __doc__
    dump(res, os.path.join(HERE, 'results', 'M1.json'))
    print('\nconvergence (prod vs fine) and solver (fine vs conformal) per-crossing |rel diff| medians / p95:')
    for key, q in res.items():
        if not isinstance(q, dict) or 'convergence_prod_vs_fine' not in q:
            continue
        c = q['convergence_prod_vs_fine']
        s = ' '.join(f"{k}:{v['median_absrel']:.1e}/{v['p95_absrel']:.1e}" for k, v in c.items())
        print(f"{key} prod/fine: {s}")
        for N in (256, 1024):
            if q.get(f'conf{N}_vs_fine'):
                c = q[f'conf{N}_vs_fine']
                print(f"{key} fine/conf{N}: " + ' '.join(f"{k}:{v['median_absrel']:.1e}/{v['p95_absrel']:.1e}" for k, v in c.items()))
        print(f"   b_even growth per pair [Å]: prod {q['b_even_growth_per_pair_prod']*1e8:.3g}, fine {q.get('b_even_growth_per_pair_fine', np.nan)*1e8:.3g}, "
              f"conf256 {q.get('b_even_growth_per_pair_conf256', np.nan)*1e8:.3g}, conf1024 {q.get('b_even_growth_per_pair_conf1024', np.nan)*1e8:.3g}; "
              f"intercepts prod {q['b_even_intercept_prod']*1e8:.3g} fine {q.get('b_even_intercept_fine', np.nan)*1e8:.3g} conf1024 {q.get('b_even_intercept_conf1024', np.nan)*1e8:.3g}")
    print(f"total job CPU {cpu:.0f} s")
