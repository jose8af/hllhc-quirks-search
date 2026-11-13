"""FU_analysis.py -- E2 follow-up (post-unblinding) analysis -> results/FU.json.  Blind results are not modified.

E1 closed forms used (analytic/NEAR_MISS_IMPULSE.md §3.2, §4.1-4.2, §5.3; predictions.json):
  rho = gamma* beta*;  b_odd/l_max = eps_perp [gamma* - asinh(rho)/rho]/(gamma* - 1);  K(g) = (3 ln2 - 2) - 0.506 ln g - 0.077 ln^2 g
  c_ev = 1/[ln(l_max/b_odd) + K(gamma*)];  G = 2[gamma* - asinh(rho)/rho]/(rho artanh beta*);  eta/eps = G [ln(l_max/b_odd) + K]
  vacuum: psi = Ahat (b/l_max)[ln(l_max/b) + K_vac], Ahat = 2(gamma*-1)/(rho artanh beta*), K_vac(NR) = 3 ln 2 - 2.
FU1: c at 3 keV.  (a) per-event measured c_k = (R(1/k) - 1)/ln k vs per-event c_ev(E1) on the SAME events, in gamma* bins;
     (b) precision tests (round-off replicas, conformal N = 4096, max_boost 1e-4); (c) B ratios 1/2, 1/4 only.
FU2: M2a refit with Ahat fixed to E1's value -> K_vac = ln(L/l_max) per gamma* (incl. 1.01, 1.02), per crossing and solver.
FU3: classification of the full-event odd-crossing residual (psi_odd - CM law) and of the per-pair residual vs E1's
     eta/eps closed form, by m_Q, Lambda, gamma*, step size.
Run: pixi run python analytic/numerics/FU_analysis.py
"""
import os, sys, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
from nm_stats import dump, boot
from T2_propagator import ExactPair, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T

D = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics')
B0 = 3.8112
GBINS = [(1.0, 1.1), (1.1, 1.2), (1.2, 1.35), (1.35, 1.6), (1.6, 10.0)]


def Kfun(g):
    lg = np.log(g)
    return (3 * np.log(2) - 2) - 0.506 * lg - 0.077 * lg ** 2


def kin(p1, p2, m, lam):
    sig = sigma_from_lambda_keV(lam)
    ex = ExactPair(p1, p2, m, m, sig)
    gs = ex.E1s / m; rho = np.sqrt(gs ** 2 - 1); bs = rho / gs
    Es = ex.gamma * np.cross(ex.beta, [0, 0, B0]) * EB_GEV_PER_CM_PER_T
    Ep = Es - (Es @ ex.n) * ex.n
    eps = np.linalg.norm(Ep) / sig
    bl = eps * (gs - np.arcsinh(rho) / rho) / (gs - 1)
    c_ev = 1 / (np.log(1 / bl) + Kfun(gs))
    G = 2 * (gs - np.arcsinh(rho) / rho) / (rho * np.arctanh(bs))
    return dict(gstar=gs, eps=eps, b_over_lmax=bl, c_E1=c_ev, G=G, eta_E1=G * (np.log(1 / bl) + Kfun(gs)))


def med_boot(a):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    if len(a) < 2:
        return [float(np.median(a)) if len(a) else np.nan, np.nan, int(len(a))]
    v, e, _, _ = boot(np.median, a, n_boot=1000)
    return [v, e, int(len(a))]


# ---------------------------------------------------------------- FU1 (a), (c): per-event c on the M3 events
def fu1a():
    out = {}
    for m in (500.0, 1000.0):
        for lam in (1.0, 3.0):
            for setting in ('prod', 'fine'):
                rows = []
                for f in sorted(glob.glob(os.path.join(D, 'M3', f"m{m:g}_L{lam:g}_e*_{setting}_B.npz"))):
                    z = np.load(f)
                    fr = z['fracs']; ds = z['ds']
                    if not np.all(np.isfinite(ds[1:])):
                        continue
                    d1 = ds[np.isclose(fr, 1.0)][0]
                    k = kin(z['p1'], z['p2'], m, lam)
                    row = dict(iev=int(f.split('_e')[1][:3]), **k)
                    for kk in (2, 4, 20, 80):
                        dk = ds[np.isclose(fr, 1 / kk)][0]
                        row[f'R{kk}'] = dk * kk / d1
                        row[f'c{kk}'] = (dk * kk / d1 - 1) / np.log(kk)
                    rows.append(row)
                out[f'm{m:g}_L{lam:g}_{setting}'] = summarize_c(rows, lam)
    return out


def summarize_c(rows, lam, ks=(2, 4, 20)):
    if not rows:
        return {}
    res = dict(n=len(rows))
    sel_all = rows
    def block(rr):
        e = {}
        e['n'] = len(rr)
        e['c_E1_median'] = med_boot([r['c_E1'] for r in rr])
        for kk in ks:
            e[f'c{kk}_median_of_events'] = med_boot([r[f'c{kk}'] for r in rr])
            Rm = np.median([r[f'R{kk}'] for r in rr])
            e[f'c{kk}_from_median_R'] = float((Rm - 1) / np.log(kk))
            e[f'pred_R{kk}_E1_median'] = float(np.median([1 + r['c_E1'] * np.log(kk) for r in rr]))
            e[f'meas_R{kk}_median'] = float(Rm)
            e[f'diff_c{kk}_minus_E1_median'] = med_boot([r[f'c{kk}'] - r['c_E1'] for r in rr])
        return e
    res['all'] = block(sel_all)
    res['gamma_lt_1p5'] = block([r for r in rows if r['gstar'] < 1.5])
    res['gamma_bins'] = {f'{lo}-{hi}': block([r for r in rows if lo <= r['gstar'] < hi]) for lo, hi in GBINS
                         if len([r for r in rows if lo <= r['gstar'] < hi]) >= 3}
    return res


# ---------------------------------------------------------------- FU1 (b): precision / step tests on the FU runs
def fu_load(m, lam, setting):
    out = {}
    for f in glob.glob(os.path.join(D, 'FU', f"m{m:g}_L{lam:g}_e*_{setting}.npz")):
        z = np.load(f)
        if np.all(z['status'] == 1):          # status 5 = string-queue overflow (truncated run) -> excluded
            out[int(f.split('_e')[1][:3])] = z['ds']
    return out


def cvals(ds):
    """c_k for f = 1/2, 1/4, 1/20 from Delta_s at FR = [1, 1/2, 1/4, 1/20]."""
    return np.array([(ds[1] * 2 / ds[0] - 1) / np.log(2), (ds[2] * 4 / ds[0] - 1) / np.log(4),
                     (ds[3] * 20 / ds[0] - 1) / np.log(20)])


def fu1b():
    res = {}
    # round-off replicas
    for lam in (1.0, 3.0):
        base = fu_load(500.0, lam, 'rnd0')
        reps = [fu_load(500.0, lam, f'rnd{j}') for j in range(1, 5)]
        dsd, cd = [], []
        for i, d0 in base.items():
            if not all(i in r for r in reps):
                continue
            allds = np.array([d0] + [r[i] for r in reps])
            dsd.append(np.std(allds, axis=0) / np.mean(allds, axis=0))
            cs = np.array([cvals(x) for x in allds])
            cd.append(np.std(cs, axis=0))
        dsd = np.array(dsd); cd = np.array(cd)
        if len(dsd):
            res[f'roundoff_L{lam:g}'] = dict(n=len(dsd), rel_sd_ds_median=np.median(dsd, axis=0).tolist(),
                                            rel_sd_ds_p90=np.quantile(dsd, 0.9, axis=0).tolist(),
                                            sd_c_per_event_median=np.median(cd, axis=0).tolist(),
                                            sd_c_per_event_p90=np.quantile(cd, 0.9, axis=0).tolist(),
                                            note='f = [1, 1/2, 1/4, 1/20]; c for k = 2, 4, 20; 5 replicas at 1e-14 relative')
    # step: prod (M3) vs fine vs vfine on the same events, 3 keV
    for m in (500.0, 1000.0):
        fine = fu_load(m, 3.0, 'fine'); vf = fu_load(m, 3.0, 'vfine')
        prod = {}
        for f in glob.glob(os.path.join(D, 'M3', f"m{m:g}_L3_e*_prod_B.npz")):
            z = np.load(f); fr = z['fracs']; ds = z['ds']
            prod[int(f.split('_e')[1][:3])] = np.array([ds[np.isclose(fr, x)][0] for x in (1.0, 0.5, 0.25, 0.05)])
        ent = {}
        for name, S in (('prod', prod), ('fine', fine), ('vfine', vf)):
            ids = sorted(i for i in S if np.all(np.isfinite(S[i])))
            if not ids:
                continue
            C = np.array([cvals(S[i]) for i in ids])
            R = np.array([[S[i][1] * 2 / S[i][0], S[i][2] * 4 / S[i][0], S[i][3] * 20 / S[i][0]] for i in ids])
            ent[name] = dict(n=len(ids), c_from_median_R=[float((np.median(R[:, j]) - 1) / np.log(k)) for j, k in enumerate((2, 4, 20))],
                             c_median_of_events=[med_boot(C[:, j]) for j in range(3)])
        # paired on the vfine events
        ids = sorted(set(vf) & set(fine) & set(prod))
        for a, b in (('prod', 'vfine'), ('fine', 'vfine'), ('prod', 'fine')):
            SA = {'prod': prod, 'fine': fine, 'vfine': vf}[a]; SB = {'prod': prod, 'fine': fine, 'vfine': vf}[b]
            dd = np.array([cvals(SA[i]) - cvals(SB[i]) for i in ids if np.all(np.isfinite(SA[i])) and np.all(np.isfinite(SB[i]))])
            if len(dd):
                ent[f'paired_{a}_minus_{b}'] = dict(n=len(dd), median=np.median(dd, axis=0).tolist(),
                                                    err=[boot(np.median, dd[:, j], n_boot=1000)[1] for j in range(3)])
        E = {}
        for f in glob.glob(os.path.join(D, 'M3', f"m{m:g}_L3_e*_prod_B.npz")):
            z = np.load(f); E[int(f.split('_e')[1][:3])] = kin(z['p1'], z['p2'], m, 3.0)
        for name, S in (('prod', prod), ('fine', fine), ('vfine', vf)):
            for sel, lo, hi in (('all', 1.0, 99.0), ('g_lt_1p5', 1.0, 1.5), ('g_lt_1p2', 1.0, 1.2), ('g_ge_1p5', 1.5, 99.0)):
                ids = [i for i in S if np.all(np.isfinite(S[i])) and lo <= E[i]['gstar'] < hi]
                if len(ids) < 3:
                    continue
                dd = np.array([cvals(S[i]) - E[i]['c_E1'] for i in ids])
                ent[f'paired_{name}_minus_E1_{sel}'] = dict(n=len(ids), c_E1_median=float(np.median([E[i]['c_E1'] for i in ids])),
                                                           median=np.median(dd, axis=0).tolist(),
                                                           err=[boot(np.median, dd[:, j], n_boot=1000)[1] for j in range(3)])
        res[f'step_m{m:g}_L3'] = ent
    # conformal (independent arithmetic) vs causal fine, same hit definition
    cf = fu_load(500.0, 3.0, 'conf'); cc = fu_load(500.0, 3.0, 'cfine')
    ids = sorted(i for i in set(cf) & set(cc) if np.all(np.isfinite(cf[i])) and np.all(np.isfinite(cc[i])))
    if ids:
        Cf = np.array([cvals(cf[i]) for i in ids]); Cc = np.array([cvals(cc[i]) for i in ids])
        res['conformal_vs_causal_L3'] = dict(n=len(ids), c_conf_median=np.median(Cf, axis=0).tolist(),
                                             c_causal_median=np.median(Cc, axis=0).tolist(),
                                             paired_diff_median=np.median(Cf - Cc, axis=0).tolist(),
                                             paired_diff_err=[boot(np.median, (Cf - Cc)[:, j], n_boot=1000)[1] for j in range(3)],
                                             ds_ratio_median=float(np.median([cf[i][0] / cc[i][0] for i in ids])))
    return res


# ---------------------------------------------------------------- FU2: M2a refit with Ahat fixed
def fu2(blmax_cut=None):
    KI = {k: i for i, k in enumerate(('k', 'parity', 'b', 'bN', 'bP', 'gamma1', 'vrel', 'l_before', 'dA_N', 'dA_P',
                                      'dPiTP_N', 'dPiTP_P', 'dJTP_N', 'dJTP_P', 'aN', 'aP', 'r_lab', 'flag', 'cos_b_E', 't'))}
    res = {}
    for gs in (1.01, 1.02, 1.05, 1.3, 2.0, 3.0):
        rho = np.sqrt(gs ** 2 - 1); bs = rho / gs
        Ahat = 2 * (gs - 1) / (rho * np.arctanh(bs))
        fl = 3e-8 if gs <= 1.3 else 1e-6
        ent = dict(Ahat_E1=Ahat)
        allK = []
        for solver in ('causal0.01', 'causal0.001', 'conf256', 'conf2048'):
            vals = {1: [], 2: []}; free = []; perb = []
            for f in glob.glob(os.path.join(HERE, 'results', 'raw', 'M2', f'A_g{gs:g}_d*_{solver}_L1_m500.npz')):
                z = np.load(f)
                if not bool(z.get('valid', True)):
                    continue
                T = z['T']; l0 = float(z['l0']); d = float(z['d']); lmax = 2 * (gs - 1) * l0
                for j in range(min(2, len(T))):
                    b = T[j, KI['b']]
                    if not (fl <= b / l0 <= 1e-3 and abs(b / d - 1) < 3e-4):
                        continue
                    if blmax_cut is not None and b / lmax > blmax_cut:
                        continue
                    psi_b = T[j, KI['dA_N']] * np.sign(T[j, KI['bN']]) * (-1) ** j
                    y = psi_b / (b / lmax)                    # = Ahat ln(lmax/b) + Ahat K_vac
                    vals[j + 1].append(y / Ahat - np.log(lmax / b))
                    perb.append((float(b / lmax), j + 1, float(y / Ahat - np.log(lmax / b))))
                    free.append((np.log(lmax / b), y))
            e = {}
            for kk in (1, 2):
                a = np.array(vals[kk])
                if len(a):
                    e[f'K_vac_crossing{kk}'] = [float(np.mean(a)), float(np.std(a) / np.sqrt(len(a))), float(np.std(a)), len(a)]
            a = np.array(vals[1] + vals[2])
            if len(a):
                e['K_vac'] = [float(np.mean(a)), float(np.std(a) / np.sqrt(len(a))), float(np.std(a)), len(a)]
                e['L_over_lmax'] = float(np.exp(np.mean(a)))
                allK += list(a)
            if len(free) >= 4:
                x, y = np.array(free).T
                A = np.vstack([x, np.ones_like(x)]).T
                (sl, ic), *_ = np.linalg.lstsq(A, y, rcond=None)
                e['free_fit_Ahat'] = float(sl); e['free_fit_Kvac'] = float(ic / sl)
            e['per_b'] = sorted(perb)
            ent[solver] = e
        if allK:
            ent['K_vac_all_solvers'] = [float(np.mean(allK)), float(np.std(allK) / np.sqrt(len(allK))), float(np.std(allK)), len(allK)]
        res[f'{gs:g}'] = ent
    res['K_vac_NR_E1'] = 3 * np.log(2) - 2
    return res


# ---------------------------------------------------------------- FU3: odd-crossing residual classification
def fu3():
    import M1_analysis as A
    laws = A.m2_laws()
    res = {}
    for setting in ('prod', 'fine', 'prodall'):
        allrows = []
        for m in (200.0, 500.0, 1000.0):
            for lam in (0.6, 1.0, 2.0, 3.0, 5.0):
                evs = A.load(m, lam, 'prod' if setting == 'prodall' else setting)
                if setting == 'prod':
                    evs = [d for d in evs if d['iev'] < 20]        # same events as 'fine'
                for d in evs:
                    p1 = None
                    rows = A.per_crossing([d], laws)
                    odd = [r for r in rows if r['parity'] == 1]; even = [r for r in rows if r['parity'] == 0]
                    if not odd or not even:
                        continue
                    g = d['gstar']; rho = np.sqrt(g ** 2 - 1); bs = rho / g
                    G = 2 * (g - np.arcsinh(rho) / rho) / (rho * np.arctanh(bs))
                    po = np.median([r['psi'] for r in odd]); pe = np.median([r['psi'] for r in even])
                    eps = np.median([r['eps'] for r in odd])
                    bl = eps * (g - np.arcsinh(rho) / rho) / (g - 1)
                    eta = G * (np.log(1 / bl) + Kfun(g))
                    allrows.append(dict(m=m, lam=lam, g=g, res_odd=np.median([r['psi'] - r['psi_pred_M2b'] for r in odd]),
                                        res_pair_E1=po + pe - eta, psi_pair=po + pe, eta_E1=eta))
        R = allrows
        e = {}
        e['all'] = dict(res_odd=med_boot([r['res_odd'] for r in R]), res_pair_E1=med_boot([r['res_pair_E1'] for r in R]),
                        rel_pair=med_boot([r['res_pair_E1'] / r['eta_E1'] for r in R]))
        e['by_m'] = {f'{m:g}': dict(res_odd=med_boot([r['res_odd'] for r in R if r['m'] == m]),
                                    res_pair_E1=med_boot([r['res_pair_E1'] for r in R if r['m'] == m])) for m in (200.0, 500.0, 1000.0)}
        e['by_lam'] = {f'{l:g}': dict(res_odd=med_boot([r['res_odd'] for r in R if r['lam'] == l]),
                                      res_pair_E1=med_boot([r['res_pair_E1'] for r in R if r['lam'] == l])) for l in (0.6, 1.0, 2.0, 3.0, 5.0)}
        e['by_gstar'] = {f'{lo}-{hi}': dict(res_odd=med_boot([r['res_odd'] for r in R if lo <= r['g'] < hi]),
                                            res_pair_E1=med_boot([r['res_pair_E1'] for r in R if lo <= r['g'] < hi])) for lo, hi in GBINS}
        res[setting + ('' if setting == 'prodall' else '_first20')] = e
    return res


if __name__ == '__main__':
    out = dict(description=__doc__)
    out['FU1a'] = fu1a()
    out['FU1b'] = fu1b()
    out['FU2'] = fu2()
    out['FU2_blmax_le_1e-3'] = fu2(1e-3)
    out['FU2_blmax_le_1e-4'] = fu2(1e-4)
    out['FU3'] = fu3()
    dump(out, os.path.join(HERE, 'results', 'FU.json'))
    f = out['FU1a']
    print('=== FU1a: per-event c (median of events) vs E1 c_ev on the same events; [value, err, n]')
    for key, v in f.items():
        if not v:
            continue
        for sel in ('all', 'gamma_lt_1p5'):
            b = v[sel]
            print(f"{key:18s} {sel:13s} n={b['n']:3d} c_E1={b['c_E1_median'][0]:.4f} | " +
                  ' '.join(f"c{k}={b[f'c{k}_median_of_events'][0]:.4f}±{b[f'c{k}_median_of_events'][1]:.4f} (Rmed->{b[f'c{k}_from_median_R']:.4f}; diff {b[f'diff_c{k}_minus_E1_median'][0]:+.4f}±{b[f'diff_c{k}_minus_E1_median'][1]:.4f})" for k in (2, 4, 20)))
        for gb, b in v['gamma_bins'].items():
            print(f"{'':18s} g*={gb:9s} n={b['n']:3d} c_E1={b['c_E1_median'][0]:.4f} | " +
                  ' '.join(f"diff c{k} {b[f'diff_c{k}_minus_E1_median'][0]:+.4f}±{b[f'diff_c{k}_minus_E1_median'][1]:.4f}" for k in (2, 4, 20)))
    print('=== FU1b'); print(json.dumps(out['FU1b'], indent=0, default=float)[:4000])
    print('=== FU2')
    for gs, v in out['FU2'].items():
        if isinstance(v, dict):
            print(gs, f"Ahat_E1={v['Ahat_E1']:.4f}", {s: (round(e['K_vac'][0], 4), round(e['K_vac'][1], 4), e['K_vac'][3], round(e.get('free_fit_Ahat', np.nan), 4)) for s, e in v.items() if isinstance(e, dict) and 'K_vac' in e},
                  'all:', v.get('K_vac_all_solvers'))
    print('=== FU3'); print(json.dumps(out['FU3'], indent=0, default=float)[:3000])
