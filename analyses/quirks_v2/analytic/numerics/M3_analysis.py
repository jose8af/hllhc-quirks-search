"""M3_analysis.py -- E2: thickness scans (data/stage1_numerics/M3) -> results/M3.json + stdout tables.

Lambda scan: median, Q68, p16/p84 of Delta_s_B (truth level, plane through the PV, 10 barrel layers), bootstrap errors
(2000 resamples); local exponents d ln median / d ln Lambda between adjacent grid points with paired-event bootstrap; also
the median of per-event exponents.  Delta_s split by the number of vacuum crossings inside r = 108.3 cm (terciles).
B scan (f = B/B0): median Delta_s(f), local exponents d ln Delta_s / d ln f, event-level response per unit B
R_ev(f) = median_events Delta_s(f)/(f Delta_s(1)); hit-level response per unit B R_hit(f) = Q68|d(f)/f| / Q68|d(1)| with
d(f) = hit(f) - hit(f=0) matched by (quirk, layer, n-th crossing), out-of-plane (vacuum-plane normal) and 3D, split into hits
before / after the first crossing (lab time < Dt); T4/S non-linearity metric Q68|d(1) - k d(1/k)| / Q68|d(1)|.
Convergence: prod (max_boost 1e-2, hmax 0.2) vs fine (1e-3, 0.02) on the same events.
Run: pixi run python analytic/numerics/M3_analysis.py
"""
import os, sys, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
from nm_stats import dump, boot, q68, med, summarize

RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'M3')
MASSES = [200.0, 500.0, 1000.0]
LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 10.0]
FRACS = [0.0, 1e-3, 1 / 80, 1 / 20, 1 / 4, 1 / 2, 1.0, 2.0]


def load(m, lam, setting):
    fs = sorted(glob.glob(os.path.join(RAW, f"m{m:g}_L{lam:g}_e*_{setting}_*.npz")))
    out = {}
    for f in fs:
        z = np.load(f)
        iev = int(f.split('_e')[1][:3])
        d = dict(fracs=z['fracs'], ds=z['ds'], Dt=float(z['Dt']), ncross=int(z['ncross_in']), gstar=float(z['gstar']),
                 status=z['status'], bscan=len(z['fracs']) > 1)
        d['hits'] = [z[f'hits{j}'] for j in range(len(z['fracs']))]
        if iev in out and not d['bscan']:
            continue
        out[iev] = d
    return out


def ds_at(d, f):
    j = np.where(np.isclose(d['fracs'], f))[0]
    return d['ds'][j[0]] if len(j) else np.nan


def keyed(H):
    out = {}
    for h in H:
        out[(int(h[0]), int(h[1]), int(h[8]))] = h
    return out


def hit_response(evs):
    from T3_propagator import plane_fit
    acc = {f: dict(pre_n=[], post_n=[], pre_3=[], post_3=[]) for f in FRACS[1:]}
    nl = {k: dict(pre=[], post=[], ref_pre=[], ref_post=[]) for k in (4.0, 20.0, 80.0)}
    for d in evs.values():
        if not d['bscan']:
            continue
        H0 = keyed(d['hits'][0])
        if len(H0) < 4:
            continue
        _, nrm = plane_fit(np.array([h[3:6] for h in H0.values()]))
        Hf = {f: keyed(d['hits'][j]) for j, f in enumerate(d['fracs'])}
        for f in FRACS[1:]:
            for key, h0 in H0.items():
                if key not in Hf[f]:
                    continue
                dv = Hf[f][key][3:6] - h0[3:6]
                part = 'pre' if h0[2] < d['Dt'] else 'post'
                acc[f][part + '_n'].append((dv @ nrm) / f)
                acc[f][part + '_3'].append(np.linalg.norm(dv) / f)
        for k in nl:
            fk = 1.0 / k
            for key, h0 in H0.items():
                if key in Hf[1.0] and key in Hf[fk]:
                    d1 = Hf[1.0][key][3:6] - h0[3:6]; dk = Hf[fk][key][3:6] - h0[3:6]
                    part = 'pre' if h0[2] < d['Dt'] else 'post'
                    nl[k][part].append(np.linalg.norm(d1 - k * dk)); nl[k]['ref_' + part].append(np.linalg.norm(d1))
    out = {}
    for part in ('pre', 'post'):
        for comp in ('n', '3'):
            ref = q68(acc[1.0][f'{part}_{comp}'])
            out[f'R_hit_{part}_{comp}'] = {f'{f:g}': q68(acc[f][f'{part}_{comp}']) / ref for f in FRACS[1:]}
            out[f'n_hits_{part}'] = len(acc[1.0][f'{part}_{comp}'])
    for k in nl:
        out[f'nonlin_k{k:g}'] = {p: (q68(nl[k][p]) / q68(nl[k]['ref_' + p]) if nl[k][p] else np.nan) for p in ('pre', 'post')}
    return out


if __name__ == '__main__':
    res = dict(description=__doc__, lambda_scan={}, b_scan={}, convergence={})
    print('=== Lambda scan: median Delta_s_B [um] (bootstrap err) [Q68]; local exponent to next Lambda')
    for m in MASSES:
        evs = {lam: load(m, lam, 'prod') for lam in LAMS}
        common = sorted(set.intersection(*[set(evs[l].keys()) for l in LAMS]))
        bad = [i for i in common if not all(np.isfinite(ds_at(evs[l][i], 1.0)) and ds_at(evs[l][i], 1.0) > 0 for l in LAMS)]
        res['lambda_scan'][f'm{m:g}_excluded_events'] = [(i, [int(evs[l][i]['status'][-1]) for l in LAMS]) for i in bad]
        common = [i for i in common if i not in bad]
        rows = {}
        for lam in LAMS:
            a = np.array([ds_at(evs[lam][i], 1.0) for i in common]) * 1e4
            rows[lam] = a
            s = summarize(a)
            res['lambda_scan'][f'm{m:g}_L{lam:g}'] = dict(summary_um=s, n_events=len(a))
        expo = {}
        for l1, l2 in zip(LAMS[:-1], LAMS[1:]):
            st = lambda x, y: np.log(np.median(y) / np.median(x)) / np.log(l2 / l1)
            v, e, lo, hi = boot(st, rows[l1], rows[l2])
            pe = np.log(rows[l2] / rows[l1]) / np.log(l2 / l1)
            expo[f'{l1:g}-{l2:g}'] = dict(exponent=v, err=e, p16=lo, p84=hi, per_event_median=float(np.median(pe)),
                                         per_event_q16=float(np.quantile(pe, 0.16)), per_event_q84=float(np.quantile(pe, 0.84)))
        res['lambda_scan'][f'm{m:g}_exponents'] = expo
        # split by number of crossings in the tracker (terciles), per Lambda
        split = {}
        for lam in LAMS:
            nc = np.array([evs[lam][i]['ncross'] for i in common]); a = rows[lam]
            qs = np.quantile(nc, [1 / 3, 2 / 3])
            bins = [nc <= qs[0], (nc > qs[0]) & (nc <= qs[1]), nc > qs[1]]
            split[f'{lam:g}'] = [dict(ncross_median=float(np.median(nc[b])), ds_median=float(np.median(a[b])),
                                      ds_err=boot(np.median, a[b])[1], n=int(b.sum())) for b in bins]
        res['lambda_scan'][f'm{m:g}_split_by_ncross'] = split
        print(f'm = {m:.0f} GeV ({len(common)} common events)')
        for lam in LAMS:
            s = res['lambda_scan'][f'm{m:g}_L{lam:g}']['summary_um']
            ex = expo.get(f'{lam:g}-{LAMS[LAMS.index(lam)+1]:g}', {}) if lam != LAMS[-1] else {}
            sp = split[f'{lam:g}']
            print(f"  Λ={lam:5g}: {s['median']:.4g} ± {s['median_err']:.2g} [Q68 {s['q68']:.3g}, p16-84 {s['p16']:.3g}-{s['p84']:.3g}]"
                  + (f"  n({lam:g}->next) = {ex['exponent']:.3f} ± {ex['err']:.3f} (per-event {ex['per_event_median']:.3f})" if ex else '')
                  + f"  | by Ncross terciles: " + ', '.join(f"N~{b['ncross_median']:.0f}: {b['ds_median']:.3g}" for b in sp))
    print('\n=== B scan (f = B/B0): median Delta_s(f) [um], local exponent, event-level R_ev(f) = med Delta_s(f)/(f Delta_s(1))')
    for m in (500.0, 1000.0):
        for lam in (1.0, 3.0):
            evs = load(m, lam, 'prod')
            evs = {i: d for i, d in evs.items() if d['bscan']}
            ids = sorted(evs)
            ids = [i for i in ids if all(np.isfinite(ds_at(evs[i], f)) for f in FRACS)]
            tab = {f: np.array([ds_at(evs[i], f) for i in ids]) * 1e4 for f in FRACS}
            ent = dict(n_events=len(ids), vacuum_floor_um=summarize(tab[0.0]))
            for f in FRACS[1:]:
                ent[f'f{f:g}'] = summarize(tab[f])
                rr = tab[f] / (f * tab[1.0])
                ent[f'R_ev_f{f:g}'] = dict(zip(('median', 'err', 'p16', 'p84'), boot(np.median, rr)))
            fl = FRACS[1:]
            ent['local_exponents'] = {}
            for f1, f2 in zip(fl[:-1], fl[1:]):
                st = lambda x, y: np.log(np.median(y) / np.median(x)) / np.log(f2 / f1)
                v, e, lo, hi = boot(st, tab[f1], tab[f2])
                ent['local_exponents'][f'{f1:g}-{f2:g}'] = dict(exponent=v, err=e)
            # global power law over f in [1/80, 2] (log-log fit of medians, bootstrap)
            fs = np.array([f for f in fl if f >= 1 / 80])
            def gl(*cols):
                y = np.log([np.median(c) for c in cols]); return np.polyfit(np.log(fs), y, 1)[0]
            v, e, _, _ = boot(gl, *[tab[f] for f in fs])
            ent['power_law_1/80_to_2'] = dict(exponent=v, err=e)
            # log-law fit of the response per unit B: R_ev(f) = 1 + c ln(1/f), f <= 1
            fs2 = np.array([f for f in fl if f <= 1.0])
            def cl(*cols):
                R = np.array([np.median(c / (f * cols[-1])) for c, f in zip(cols[:-1], fs2[:-1])])
                return np.polyfit(np.log(1 / fs2[:-1]), R - 1, 1)[0]
            v, e, _, _ = boot(cl, *[tab[f] for f in fs2])
            ent['R_ev_log_coefficient'] = dict(c=v, err=e, note='fit of R_ev(f) - 1 = c ln(1/f) + const, f in [1e-3, 1/2]')
            ent['c_k_prod'] = {f'{1/f:g}': (ent[f'R_ev_f{f:g}']['median'] - 1) / np.log(1 / f) for f in fl if f < 1}
            evf = {i: d for i, d in load(m, lam, 'fine').items() if d['bscan'] and all(np.isfinite(ds_at(d, f)) for f in FRACS)}
            if evf:
                idf = sorted(evf)
                tf = {f: np.array([ds_at(evf[i], f) for i in idf]) * 1e4 for f in FRACS}
                ent['fine'] = dict(n_events=len(idf))
                for f in fl:
                    rr = tf[f] / (f * tf[1.0])
                    ent['fine'][f'R_ev_f{f:g}'] = dict(zip(('median', 'err', 'p16', 'p84'), boot(np.median, rr)))
                    # prod on the same events for a paired comparison
                    rp = np.array([ds_at(evs[i], f) / (f * ds_at(evs[i], 1.0)) for i in idf if i in evs])
                    ent['fine'][f'R_ev_prod_same_events_f{f:g}'] = float(np.median(rp))
                ent['fine']['c_k'] = {f'{1/f:g}': (ent['fine'][f'R_ev_f{f:g}']['median'] - 1) / np.log(1 / f) for f in fl if f < 1}
                ent['fine']['hit_response'] = hit_response(evf)
            ent['hit_response'] = hit_response(evs)
            res['b_scan'][f'm{m:g}_L{lam:g}'] = ent
            print(f"m={m:.0f} Λ={lam:g} ({len(ids)} ev; vacuum floor median {ent['vacuum_floor_um']['median']:.2g} um):")
            print('   ' + ' '.join(f"f={f:g}: {ent[f'f{f:g}']['median']:.4g}" for f in fl))
            print('   R_ev: ' + ' '.join(f"{f:g}: {ent[f'R_ev_f{f:g}']['median']:.3f}±{ent[f'R_ev_f{f:g}']['err']:.3f}" for f in fl))
            print('   local exp: ' + ' '.join(f"{k}: {v['exponent']:.3f}±{v['err']:.3f}" for k, v in ent['local_exponents'].items())
                  + f"  | global f^{ent['power_law_1/80_to_2']['exponent']:.3f}±{ent['power_law_1/80_to_2']['err']:.3f}; R_ev log coeff c = {ent['R_ev_log_coefficient']['c']:.3f}±{ent['R_ev_log_coefficient']['err']:.3f}")
            print('   c_k=(R_ev-1)/ln k (prod): ' + ' '.join(f"k={k}: {v:.3f}" for k, v in ent['c_k_prod'].items()))
            if 'fine' in ent:
                print(f"   FINE ({ent['fine']['n_events']} ev) R_ev: " + ' '.join(f"{f:g}: {ent['fine'][f'R_ev_f{f:g}']['median']:.3f}±{ent['fine'][f'R_ev_f{f:g}']['err']:.3f} (prod same ev {ent['fine'][f'R_ev_prod_same_events_f{f:g}']:.3f})" for f in fl if f < 1))
                print('   FINE c_k: ' + ' '.join(f"k={k}: {v:.3f}" for k, v in ent['fine']['c_k'].items()))
                hf = ent['fine']['hit_response']
                print('   FINE hit R post out-of-plane: ' + ' '.join(f"{k}:{v:.3f}" for k, v in hf['R_hit_post_n'].items()))
            hr = ent['hit_response']
            for part in ('pre', 'post'):
                print(f"   hit R ({part}, n={hr[f'n_hits_{part}']}): out-of-plane " + ' '.join(f"{k}:{v:.3f}" for k, v in hr[f'R_hit_{part}_n'].items())
                      + ' | 3D ' + ' '.join(f"{k}:{v:.3f}" for k, v in hr[f'R_hit_{part}_3'].items()))
            print('   nonlin metric Q68|d(B)-k d(B/k)|/Q68|d(B)|: ' + ' '.join(f"k={k[8:]}: pre {v['pre']:.4f} post {v['post']:.3f}" for k, v in hr.items() if k.startswith('nonlin')))
    print('\n=== convergence prod vs fine (same events): median and p95 of |Delta_s_fine/Delta_s_prod - 1|')
    for m in MASSES:
        for lam in LAMS:
            a = load(m, lam, 'prod'); b = load(m, lam, 'fine')
            ids = sorted(set(a) & set(b))
            if not ids:
                continue
            r = {}
            for f in (FRACS[1:] if b[ids[0]]['bscan'] else [1.0]):
                rel = np.array([ds_at(b[i], f) / ds_at(a[i], f) - 1 for i in ids])
                r[f'f{f:g}'] = dict(median_absrel=float(np.median(np.abs(rel))), p95_absrel=float(np.quantile(np.abs(rel), 0.95)),
                                    median_rel=float(np.median(rel)), n=len(ids))
            res['convergence'][f'm{m:g}_L{lam:g}'] = r
            print(f"m={m:.0f} Λ={lam:g}: " + ' '.join(f"{k}: {v['median_absrel']:.1e}/{v['p95_absrel']:.1e}" for k, v in r.items()))
    dump(res, os.path.join(HERE, 'results', 'M3.json'))
