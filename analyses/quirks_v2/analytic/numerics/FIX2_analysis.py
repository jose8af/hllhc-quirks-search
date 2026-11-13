"""FIX2_analysis.py -- E2 fix pass 2 (review S1-R2 N1/N2) -> results/FIX2.json.  Earlier results are not modified.

Per event: c(k_f) = (R(1/k_f) - 1)/ln k_f, k_f = 2, 4, 20; Delta_c = c - c_E1 (E1 per-event closed form, FU_analysis.kin);
k_B = |B*_perp|/|E*_perp| (E1 binding definition); b_odd/l0 at B0/20 from E1's closed form (b_odd/l_max x l_max/l0 / 20).
N1 (a) B* on vs off (paired), (b) period-number scan s = 1/9, 1/3, 1 (detector scaled; same per-period physics),
   (c) 2D bins in k_B and b_odd/l0.   N2: Delta_c(k_f = 2) at B0 for Lambda = 5-13 keV, population and k_B > 10 tail,
   convergence (max_boost 1e-4 subset at 7 keV), and the implied effect on Delta_s_B(Lambda)/Delta_s_B(3 keV) at B0.
Run: pixi run python analytic/numerics/FIX2_analysis.py
"""
import os, sys, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
from nm_stats import dump, boot
import FU_analysis as F
from FIX1_analysis import kin2

D = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics')


def mb(a, n=1000):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    if len(a) < 2:
        return [float(np.median(a)) if len(a) else np.nan, np.nan, int(len(a))]
    v, e, _, _ = boot(np.median, a, n_boot=n)
    return [v, e, int(len(a))]


def load_kind(kind, m, lam):
    out = {}
    for f in glob.glob(os.path.join(D, 'FIX2', f"{kind}_m{m:g}_L{lam:g}_e*.npz")):
        z = np.load(f)
        if np.all(z['status'] == 1) and np.all(np.isfinite(z['ds'])):
            out[int(f.split('_e')[-1][:3])] = z['ds']
    return out


def cvec(ds):
    ks = [2, 4, 20][:len(ds) - 1]
    return np.array([(ds[j + 1] * k / ds[0] - 1) / np.log(k) for j, k in enumerate(ks)])


def evkin(m, lam, ids):
    from T3_propagator import sample_events
    evs = sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0)
    out = {}
    for i in ids:
        k = kin2(evs[i][0], evs[i][1], m, lam)
        k['b_l0_B20'] = k['b_over_lmax'] * 2 * (k['gstar'] - 1) / 20
        out[i] = k
    return out


def n1():
    res = {}
    for m in (500.0, 1000.0):
        sets = {'on_s1': {i: v for i, v in F.fu_load(m, 3.0, 'fine').items() if i < 40}}
        for k in ('on_s9', 'on_s3', 'off_s9', 'off_s3', 'off_s1', 'eperp_s9', 'eperp_s1'):
            sets[k] = load_kind(k, m, 3.0)
        ids = sorted(set.intersection(*[set(v) for v in sets.values()]))
        K = evkin(m, 3.0, ids)
        cE = np.array([K[i]['c_E1'] for i in ids])
        kB = np.array([K[i]['kB_perp'] for i in ids]); bl = np.array([K[i]['b_l0_B20'] for i in ids])
        D_ = {k: np.array([cvec(v[i]) for i in ids]) - cE[:, None] for k, v in sets.items()}
        ent = dict(n=len(ids), kB_median=float(np.median(kB)), b_l0_B20_median=float(np.median(bl)))
        for k, d in D_.items():
            ent[k] = dict(median=[mb(d[:, j]) for j in range(3)],
                          kB_lt5=[mb(d[kB < 5, j]) for j in range(3)], kB_ge5=[mb(d[kB >= 5, j]) for j in range(3)],
                          kB_gt10=[mb(d[kB > 10, j]) for j in range(3)])
        for s in ('s9', 's3', 's1'):
            dd = D_[f'on_{s}'] - D_[f'off_{s}']
            ent[f'on_minus_off_{s}'] = dict(median=[mb(dd[:, j]) for j in range(3)],
                                            kB_ge5=[mb(dd[kB >= 5, j]) for j in range(3)])
        # 2D: split by kB at 5 and b/l0 at the median within each kB class
        bmed = np.median(bl)
        two = {}
        for cname, ck in (('kB<5', kB < 5), ('kB>=5', kB >= 5)):
            bm = np.median(bl[ck]) if ck.sum() else bmed
            for bname, cb in (('small_b', bl < bm), ('large_b', bl >= bm)):
                sel = ck & cb
                two[f'{cname},{bname}'] = dict(n=int(sel.sum()), b_l0_median=float(np.median(bl[sel])) if sel.sum() else np.nan,
                                               kB_median=float(np.median(kB[sel])) if sel.sum() else np.nan,
                                               on_s1_c20=mb(D_['on_s1'][sel, 2]), off_s1_c20=mb(D_['off_s1'][sel, 2]),
                                               on_s9_c20=mb(D_['on_s9'][sel, 2]), eperp_s1_c20=mb(D_['eperp_s1'][sel, 2]))
        # b/l0 split at fixed kB tercile
        ent['two_d'] = two
        lb = np.log(bl); r = {}
        for k in ('on_s1', 'off_s1', 'on_s9', 'eperp_s1'):
            y = D_[k][:, 2]
            ok = np.isfinite(y)
            # partial correlations (rank) of Delta_c20 with kB and with b/l0
            from scipy.stats import spearmanr
            rk = lambda a: np.argsort(np.argsort(a)).astype(float)
            Y, X1, X2 = rk(y[ok]), rk(kB[ok]), rk(lb[ok])
            def partial(a, b, c):
                ra = a - np.polyval(np.polyfit(c, a, 1), c); rb = b - np.polyval(np.polyfit(c, b, 1), c)
                return float(np.corrcoef(ra, rb)[0, 1])
            r[k] = dict(spearman_kB=float(spearmanr(y[ok], kB[ok])[0]), spearman_b=float(spearmanr(y[ok], lb[ok])[0]),
                        partial_kB_given_b=partial(Y, X1, X2), partial_b_given_kB=partial(Y, X2, X1))
        ent['correlations_c20'] = r
        ent['spearman_kB_b'] = float(np.corrcoef(np.argsort(np.argsort(kB)), np.argsort(np.argsort(lb)))[0, 1])
        res[f'm{m:g}'] = ent
    return res


def n2():
    res = {}
    for m, lams in ((500.0, (5.0, 7.0, 10.0, 13.0)), (1000.0, (5.0, 7.0, 10.0))):
        for lam in lams:
            S = load_kind('b0', m, lam)
            if not S:
                continue
            ids = sorted(S)
            K = evkin(m, lam, ids)
            d = np.array([cvec(S[i])[0] - K[i]['c_E1'] for i in ids])
            kB = np.array([K[i]['kB_perp'] for i in ids])
            cE = np.array([K[i]['c_E1'] for i in ids]); cm = np.array([cvec(S[i])[0] for i in ids])
            res[f'm{m:g}_L{lam:g}'] = dict(n=len(ids), c_E1_median=float(np.median(cE)), c_meas_median=mb(cm),
                                           delta_c2=mb(d), delta_c2_kB_gt10=mb(d[kB > 10]), delta_c2_kB_lt5=mb(d[kB < 5]),
                                           p16_p84=[float(np.quantile(d, 0.16)), float(np.quantile(d, 0.84))],
                                           n_kB_gt10=int((kB > 10).sum()))
    # convergence at 7 keV
    S = load_kind('b0', 500.0, 7.0); V = load_kind('b0v', 500.0, 7.0)
    ids = sorted(set(S) & set(V))
    if ids:
        dd = np.array([cvec(S[i])[0] - cvec(V[i])[0] for i in ids])
        res['convergence_7keV_fine_minus_vfine'] = dict(n=len(ids), values=dd.tolist(), median=float(np.median(dd)))
    # implied effect on Delta_s_B(Lambda)/Delta_s_B(3 keV) at B0: d ln Ds / d ln Lambda = -2 + 2c
    for m in (500.0, 1000.0):
        pts = [(3.0, 0.0)] + [(lam, res[f'm{m:g}_L{lam:g}']['delta_c2'][0]) for lam in (5.0, 7.0, 10.0, 13.0) if f'm{m:g}_L{lam:g}' in res]
        cum = 0.0; eff = {}
        for (l1, d1), (l2, d2) in zip(pts[:-1], pts[1:]):
            cum += 2 * 0.5 * (d1 + d2) * np.log(l2 / l1)
            eff[f'{l2:g}'] = float(np.exp(cum) - 1)
        res[f'm{m:g}_implied_rel_change_of_Ds_vs_3keV'] = eff
    return res


if __name__ == '__main__':
    out = dict(description=__doc__)
    for name, fn in (('N1', n1), ('N2', n2)):
        try:
            out[name] = fn()
        except Exception as e:
            import traceback; traceback.print_exc()
            out[name] = dict(error=repr(e))
    dump(out, os.path.join(HERE, 'results', 'FIX2.json'))
    print(json.dumps(out, default=float, indent=0)[:12000])
