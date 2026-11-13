"""f1r_analyse.py -- Stage-4 plan FIXER R1 (TT env): summarise the f1r_finder.py outputs.

  1. PU-only rho = 1 (Fatras only = t0; Fatras + OT density top-up to the TDR = t2): per-trial best-candidate N_L2
     (per-crossing) and the R0 hit-count N_L2h; trials and events reaching each rung; 95 % CL upper limits; effective number
     of independent trials from the event bootstrap.
  2. Signal + PU (blind): per point the fraction of events whose top-ranked candidate is the signal (>= 50 % signal hits)
     and passes rung L ('eff'), the fraction with ANY signal-matched candidate passing L ('eff_anysig', signal-matched = contains >= 50 % of the event's barrel signal hits; the event-level
     selection is 'some candidate passes', blind), and the blind event pass fraction; Clopper-Pearson 68 % intervals.
  3. Margin: per rung, PU pass fraction vs signal efficiency.
  4. Delta-w (R0 rms) and core width for the top PU and signal candidates (critical A-1).
  5. Interaction-count (k) closure demo: the rho = 1 expected number of passing candidates per trial measured directly vs
     predicted from rho = 2 superpositions with the exact thinning weights (no fitted exponent); k_min spectra.
Run (theory_track): pixi run python acts/stage4/probes/f1r_analyse.py
Output: data/acts_stage4/fix_r1/f1r_summary.json
"""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import beta

TT = Path(__file__).resolve().parents[3]
FD = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'finder'
RUNGS = [5, 6, 7, 8, 9, 10]
rng = np.random.default_rng(3)


def load(pat):
    rows = []
    for f in sorted(FD.glob(pat)):
        rows += [json.loads(x) for x in f.read_text().splitlines() if x.strip()]
    return rows


def cp(k, n, cl=0.68):
    a = (1 - cl) / 2
    lo = 0.0 if k == 0 else beta.ppf(a, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - a, k + 1, n - k)
    return [float(lo), float(hi)]


def ul95(k, n):
    return float(beta.ppf(0.95, k + 1, n - k)) if k < n else 1.0


def passes(c, L, chi=None):
    return c['nit2'] >= 3 and c['nl2'] >= L and (chi is None or c['chi2ndf'] < chi)


def pu_summary(rows):
    ev = defaultdict(list)
    for r in rows:
        ev[str(r['ev'])].append(r)
    keys = sorted(ev)
    best = [r['cands'][0] if r['cands'] else None for r in rows]
    out = dict(n_trials=len(rows), n_events=len(keys))
    out['best_nl2_hist'] = {str(L): int(sum(1 for b in best if b and b['nl2'] == L)) for L in range(0, 11)}
    out['best_nl2h_R0_hist'] = {str(L): int(sum(1 for r in rows if r['cands'] and max(c['nl2h'] for c in r['cands']) == L)) for L in range(0, 11)}
    out['max_best_nl2'] = int(max(b['nl2'] for b in best if b))
    per = {}
    for L in RUNGS:
        for chi in (None, 2.0):
            k_tr = sum(1 for r in rows if any(passes(c, L, chi) for c in r['cands']))
            k_ev = sum(1 for e in keys if any(passes(c, L, chi) for r in ev[e] for c in r['cands']))
            # event bootstrap of the per-trial fraction -> effective number of independent trials
            fr = []
            for _ in range(400):
                pick = rng.choice(len(keys), len(keys))
                tr = [r for i in pick for r in ev[keys[i]]]
                fr.append(np.mean([any(passes(c, L, chi) for c in r['cands']) for r in tr]))
            p = k_tr / len(rows)
            var = np.var(fr)
            neff = float(p * (1 - p) / var) if var > 0 else None
            per[f'L{L}' + ('' if chi is None else f'_chi{chi:g}')] = dict(
                trials=k_tr, frac_trials=p, ci68_trials=cp(k_tr, len(rows)), ul95_trials=ul95(k_tr, len(rows)),
                events=k_ev, frac_events=k_ev / len(keys), ul95_events=ul95(k_ev, len(keys)), n_eff_trials=neff)
    out['rungs'] = per
    tops = [b for b in best if b and b['nl2'] >= out['max_best_nl2'] - 1]
    out['top_candidates'] = [{k: b[k] for k in ('nl2', 'nit2', 'not2', 'nl2h', 'chi2ndf', 'dw_old', 'dw_core', 'nz', 'n_int', 'seed_n2') if k in b} for b in tops]
    out['best_chi2ndf_quantiles'] = [float(q) for q in np.quantile([b['chi2ndf'] for b in best if b], [0.1, 0.5, 0.9])]
    out['best_dw_old_quantiles'] = [float(q) for q in np.quantile([b['dw_old'] for b in best if b], [0.1, 0.5, 0.9])]
    out['best_nz_quantiles'] = [float(q) for q in np.quantile([b['nz'] for b in best if b], [0.1, 0.5, 0.9])]
    out['t_trial_s_median'] = float(np.median([r['t_tot'] for r in rows]))
    out['n_refit_median'] = float(np.median([r['n_refit'] for r in rows]))
    if 'dz_nearest_pu_mm' in rows[0]:
        out['dz_nearest_pu_mm_median'] = float(np.median([r['dz_nearest_pu_mm'] for r in rows]))
    # k_min at the loosest stored rung for the top candidates (composition)
    km = [b['thin']['5']['kmin'] for b in best if b and 'thin' in b and b['thin'] and b['thin']['5']['kmin'] > 0]
    out['kmin_L5_best_quantiles'] = [float(q) for q in np.quantile(km, [0.1, 0.5, 0.9])] if km else None
    km8 = [b['thin']['8']['kmin'] for b in best if b and 'thin' in b and b['thin'] and b['thin']['8']['kmin'] > 0]
    out['kmin_L8_best'] = sorted(km8)
    out['n_int_best_quantiles'] = [float(q) for q in np.quantile([b['n_int'] for b in best if b and 'n_int' in b], [0.1, 0.5, 0.9])]
    return out, ev, keys


def sig_summary(rows):
    pts = defaultdict(list)
    for r in rows:
        pts[r['point']].append(r)
    out = {}
    for p, rs in sorted(pts.items()):
        n = len(rs)
        d = dict(n=n, rows=[r['row'] for r in rs])
        top = [r['cands'][0] if r['cands'] else None for r in rs]
        istop = [t is not None and t['sigfrac'] >= 0.5 for t in top]
        d['top_is_signal'] = int(sum(istop))
        d['best_nl2_signal_top'] = [t['nl2'] if s else None for t, s in zip(top, istop)]
        for L in RUNGS:
            for chi in (None, 2.0):
                k = sum(1 for t, s in zip(top, istop) if s and passes(t, L, chi))
                ka = sum(1 for r in rs if any(c['n_sig'] >= 0.5 * r['n_sig_total'] and passes(c, L, chi) for c in r['cands']))
                kb = sum(1 for r in rs if any(passes(c, L, chi) for c in r['cands']))
                d[f'eff_L{L}' + ('' if chi is None else f'_chi{chi:g}')] = dict(k=k, eff=k / n, ci68=cp(k, n),
                    k_anysig=ka, eff_anysig=ka / n, ci68_anysig=cp(ka, n), k_blind_event=kb, eff_blind_event=kb / n)
        st = [t for t, s in zip(top, istop) if s]
        if st:
            d['chi2ndf_q'] = [float(q) for q in np.quantile([t['chi2ndf'] for t in st], [0.1, 0.5, 0.9])]
            d['dw_old_q'] = [float(q) for q in np.quantile([t['dw_old'] for t in st], [0.1, 0.5, 0.9])]
            d['dw_core_q'] = [float(q) for q in np.quantile([t['dw_core'] for t in st], [0.1, 0.5, 0.9])]
            d['nl2h_R0'] = [t['nl2h'] for t in st]
        out[p] = d
    return out


def closure(rows1, rows2):
    """expected passing candidates per trial at rho = 1: direct vs thinned from rho = 2."""
    res = {}
    for L in RUNGS:
        d1 = np.array([sum(1 for c in r['cands'] if passes(c, L)) for r in rows1], float)
        d2 = np.array([sum(c['thin'][str(L)]['p'] for c in r['cands'] if c.get('thin')) for r in rows2], float)
        n2raw = np.array([sum(1 for c in r['cands'] if passes(c, L)) for r in rows2], float)
        b1 = [np.mean(rng.choice(d1, len(d1))) for _ in range(1000)]
        b2 = [np.mean(rng.choice(d2, len(d2))) for _ in range(1000)]
        km = [c['thin'][str(L)]['kmin'] for r in rows2 for c in r['cands'] if c.get('thin') and c['thin'][str(L)]['kmin'] > 0]
        res[f'L{L}'] = dict(direct_rho1=float(d1.mean()), direct_sd=float(np.std(b1)), pred_from_rho2=float(d2.mean()),
                            pred_sd=float(np.std(b2)), raw_rho2=float(n2raw.mean()),
                            thinning_factor=float(d2.mean() / n2raw.mean()) if n2raw.mean() > 0 else None,
                            ratio_direct_over_pred=float(d1.mean() / d2.mean()) if d2.mean() > 0 else None,
                            kmin_rho2_quantiles=[float(q) for q in np.quantile(km, [0.1, 0.5, 0.9])] if km else None)
    return res


S = {}
for t in (0, 2):
    rows = load(f'pu_t{t}_s6_tol30_j*.jsonl')
    if rows:
        S[f'pu_rho1_t{t}'], _, _ = pu_summary(rows)
    srows = load(f'sig_t{t}_s6_tol30_j*.jsonl')
    if srows:
        S[f'sig_t{t}'] = sig_summary(srows)
rows2 = load('pu2_t0_s6_tol30_j*.jsonl')
if rows2:
    S['pu_rho2_t0'], _, _ = pu_summary(rows2)
    S['closure_rho2_to_rho1_t0'] = closure(load('pu_t0_s6_tol30_j*.jsonl'), rows2)
r3 = load('pu_t0_s4_tol30_j*.jsonl')
if r3:
    r4 = [r for r in load('pu_t0_s6_tol30_j*.jsonl') if any((r['ev'], r['road']) == (x['ev'], x['road']) for x in r3)]
    S['tseed_stability'] = dict(n=len(r3), best_tseed4=[r['cands'][0]['nl2'] if r['cands'] else None for r in sorted(r3, key=lambda r: (r['ev'], r['road']))],
                                best_tseed6=[r['cands'][0]['nl2'] if r['cands'] else None for r in sorted(r4, key=lambda r: (r['ev'], r['road']))])
(TT / 'data' / 'acts_stage4' / 'fix_r1' / 'f1r_summary.json').write_text(json.dumps(S, indent=1))
for k, v in S.items():
    if k.startswith('pu'):
        print(k, 'trials', v['n_trials'], 'events', v['n_events'], 'best N_L2 hist', v['best_nl2_hist'], 'R0 N_L2h hist', v['best_nl2h_R0_hist'])
        print('   rungs', {r: (x['trials'], round(x['ul95_trials'], 4), x['events']) for r, x in v['rungs'].items()})
        print('   t/trial', v['t_trial_s_median'], 'kmin L5 q', v['kmin_L5_best_quantiles'], 'n_int q', v['n_int_best_quantiles'], 'chi2 q', v['best_chi2ndf_quantiles'], 'dw_old q', v['best_dw_old_quantiles'])
    elif k.startswith('sig'):
        for p, d in v.items():
            print(k, p, 'n', d['n'], 'top=sig', d['top_is_signal'], 'anysig L9/L10/L9chi2/L10chi2', [d[x]['k_anysig'] for x in ('eff_L9', 'eff_L10', 'eff_L9_chi2', 'eff_L10_chi2')],
                  'blind L10chi2', d['eff_L10_chi2']['k_blind_event'], 'chi2q', d.get('chi2ndf_q'))
    elif k.startswith('closure'):
        for r, x in v.items():
            print(k, r, {a: (round(b, 4) if isinstance(b, float) else b) for a, b in x.items()})
    else:
        print(k, v)
