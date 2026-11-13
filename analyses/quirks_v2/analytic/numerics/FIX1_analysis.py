"""FIX1_analysis.py -- E2 fix pass 1 (reviews S1-R1) -> results/FIX1.json.  Earlier results are not modified.

A1(a): per-event c_f - c_E1 at 3 keV (and 1 keV) split by kB = |B*|/|E*_perp| (CM magnetic over transverse electric field, both in
       field units; E1/R1 convention q|B*|/sigma = kB eps), by kB_perp (B* component perp. to the CM axis), and by gamma*;
       per-event spread (16/50/84 %), not only medians.  c_f = (R(f) - 1)/ln(1/f), f = 1/2, 1/4, 1/20.
A1(b): max_boost 1e-4 (queue cap 2^21) on 40 events per mass vs 1e-3, paired; and vs E1.
A1 / C4: replica test (perturbation 1e-14, 1e-10, 1e-8): does the c_f excess change? does the spread scale with the perturbation?
B6(i): Li / causal thickness ratio at gamma* = 2.  B6(ii): T3 event list re-run vs figures/T3_ms_thickness.npy and vs the M3 sample.
B6(iii): low-gamma* full-event residual vs step size (prod 1e-2, fine 1e-3, vfine 1e-4).
Run: pixi run python analytic/numerics/FIX1_analysis.py
"""
import os, sys, glob, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
from nm_stats import dump, boot
from T2_propagator import ExactPair, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T
import FU_analysis as F

D = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics')
TT = os.path.join(HERE, '..', '..')
B0 = 3.8112
KBINS = [(0, 3), (3, 5), (5, 7), (7, 10), (10, 1e9)]
GB = [(1.0, 1.15), (1.15, 1.3), (1.3, 1.6), (1.6, 99)]


def kin2(p1, p2, m, lam):
    k = F.kin(p1, p2, m, lam)
    sig = sigma_from_lambda_keV(lam)
    ex = ExactPair(p1, p2, m, m, sig)
    b = ex.beta; g = ex.gamma; bh = b / np.linalg.norm(b)
    Bl = np.array([0, 0, B0])
    Bs = g * Bl - (g - 1) * (Bl @ bh) * bh                      # CM magnetic field (lab B only)
    Es = g * np.cross(b, Bl)                                   # CM electric field
    Ep = Es - (Es @ ex.n) * ex.n
    Bp = Bs - (Bs @ ex.n) * ex.n
    k.update(kB=np.linalg.norm(Bs) / np.linalg.norm(Ep), kB_perp=np.linalg.norm(Bp) / np.linalg.norm(Ep),
             sin_alpha=np.linalg.norm(Ep) / np.linalg.norm(Es))
    return k


def cf(ds):
    return np.array([(ds[1] * 2 / ds[0] - 1) / np.log(2), (ds[2] * 4 / ds[0] - 1) / np.log(4), (ds[3] * 20 / ds[0] - 1) / np.log(20)])


def m3_ds(m, lam, setting):
    out = {}
    for f in glob.glob(os.path.join(D, 'M3', f"m{m:g}_L{lam:g}_e*_{setting}_B.npz")):
        z = np.load(f); fr = z['fracs']
        ds = np.array([z['ds'][np.isclose(fr, x)][0] for x in (1.0, 0.5, 0.25, 0.05)])
        if np.all(np.isfinite(ds)) and np.all(z['status'] == 1):
            out[int(f.split('_e')[1][:3])] = (ds, z['p1'], z['p2'])
    return out


def fix_load(kind, m=None, extra=''):
    out = {}
    for f in glob.glob(os.path.join(D, 'FIX1', f"{kind}_{'' if m is None else f'{float(m)}_'}*{extra}.npz")):
        out[os.path.basename(f)[:-4]] = np.load(f)
    return out


def split(rows, key, bins):
    res = {}
    for lo, hi in bins:
        rr = [r for r in rows if lo <= r[key] < hi]
        if len(rr) < 3:
            continue
        d = np.array([r['d'] for r in rr])
        res[f'{lo:g}-{hi:g}'] = dict(n=len(rr), c_E1=float(np.median([r['c_E1'] for r in rr])),
                                     median=np.median(d, 0).tolist(),
                                     err=[boot(np.median, d[:, j], n_boot=500)[1] for j in range(3)],
                                     p16=np.quantile(d, 0.16, 0).tolist(), p84=np.quantile(d, 0.84, 0).tolist())
    return res


def a1a():
    res = {}
    for lam, settings in ((3.0, ('fine_FU', 'prod_M3')), (1.0, ('prod_M3', 'fine_M3'))):
        for m in (500.0, 1000.0):
            m3 = m3_ds(m, lam, 'prod')
            for s in settings:
                if s == 'fine_FU':
                    S = {i: (F.fu_load(m, lam, 'fine')[i],) + m3[i][1:] for i in F.fu_load(m, lam, 'fine') if i in m3}
                elif s == 'prod_M3':
                    S = m3
                else:
                    S = m3_ds(m, lam, 'fine')
                rows = []
                for i, (ds, p1, p2) in S.items():
                    if not np.all(np.isfinite(ds)):
                        continue
                    k = kin2(p1, p2, m, lam)
                    rows.append(dict(iev=i, d=cf(ds) - k['c_E1'], **k))
                ent = dict(n=len(rows), all=split(rows, 'gstar', [(1.0, 99)]),
                           by_kB=split(rows, 'kB', KBINS), by_kB_perp=split(rows, 'kB_perp', KBINS),
                           by_gstar=split(rows, 'gstar', GB))
                # 2D: low gamma* and low kB
                ent['g_lt_1p3_kB_lt_5'] = split([r for r in rows if r['gstar'] < 1.3], 'kB', [(0, 5), (5, 1e9)])
                ent['kB_quantiles'] = np.quantile([r['kB'] for r in rows], [0.16, 0.5, 0.84]).tolist()
                ent['corr_d20_kB'] = float(np.corrcoef([r['d'][2] for r in rows], [r['kB'] for r in rows])[0, 1])
                ent['corr_d20_gstar'] = float(np.corrcoef([r['d'][2] for r in rows], [r['gstar'] for r in rows])[0, 1])
                res[f'L{lam:g}_m{m:g}_{s}'] = ent
    return res


def a1b():
    res = {}
    for m in (500.0, 1000.0):
        vf = {}
        for tag, z in fix_load('vfine40', m).items():
            if np.all(z['status'] == 1) and np.all(np.isfinite(z['ds'])):
                vf[int(tag.split('_')[2])] = z['ds']
        nall = len(fix_load('vfine40', m))
        fine = F.fu_load(m, 3.0, 'fine'); m3 = m3_ds(m, 3.0, 'prod')
        ids = sorted(i for i in vf if i in fine and i in m3)
        if not ids:
            continue
        cE = np.array([kin2(m3[i][1], m3[i][2], m, 3.0)['c_E1'] for i in ids])
        Cv = np.array([cf(vf[i]) for i in ids]); Cf = np.array([cf(fine[i]) for i in ids])
        dv = Cv - cE[:, None]; dfv = Cf - Cv
        res[f'm{m:g}'] = dict(n_valid=len(ids), n_run=nall,
                              vfine_minus_E1=dict(median=np.median(dv, 0).tolist(), err=[boot(np.median, dv[:, j], n_boot=1000)[1] for j in range(3)],
                                                  p16=np.quantile(dv, 0.16, 0).tolist(), p84=np.quantile(dv, 0.84, 0).tolist(),
                                                  frac_positive=(dv > 0).mean(0).tolist()),
                              fine_minus_vfine=dict(median=np.median(dfv, 0).tolist(), err=[boot(np.median, dfv[:, j], n_boot=1000)[1] for j in range(3)],
                                                    rms=np.sqrt(np.mean(dfv ** 2, 0)).tolist()),
                              c_vfine_from_medianR=[float((np.median([vf[i][j + 1] * (2, 4, 20)[j] / vf[i][0] for i in ids]) - 1) / np.log((2, 4, 20)[j])) for j in range(3)],
                              c_E1_median=float(np.median(cE)),
                              c20_minus_c2_vfine=dict(median=float(np.median(Cv[:, 2] - Cv[:, 0])), frac_positive=float((Cv[:, 2] > Cv[:, 0]).mean())))
    return res


def rep():
    R = fix_load('rep', 500.0)
    by = {}
    for tag, z in R.items():
        parts = tag.split('_')            # rep_500.0_i_delta_j
        i = int(parts[2]); d = float(parts[3])
        if not np.all(z['status'] == 1):
            continue
        by.setdefault(i, {}).setdefault(d, []).append(z['ds'])
    res = {}
    for d in (1e-14, 1e-10, 1e-8):
        sds, sdc, shift = [], [], []
        for i, v in by.items():
            if 0.0 not in v or d not in v:
                continue
            base = v[0.0][0]
            arr = np.array(v[d])
            sds.append(np.std(np.vstack([arr, base]), 0) / base)
            sdc.append(np.std([cf(x) for x in arr] + [cf(base)], 0))
            shift.append(np.mean([cf(x) for x in arr], 0) - cf(base))
        if sds:
            res[f'{d:g}'] = dict(n_events=len(sds), rel_sd_ds_median=np.median(sds, 0).tolist(), sd_c_median=np.median(sdc, 0).tolist(),
                                 mean_c_shift_median=np.median(shift, 0).tolist())
    return res


def li2():
    L = fix_load('li2')
    ds = {}
    for tag, z in L.items():
        _, i, frac = tag.split('_')
        ds.setdefault(int(i), {})[float(frac)] = float(z['ds'])
    r3 = np.array([v[1e-3] / v[0.0] for v in ds.values() if 1e-3 in v and 0.0 in v])
    r4 = np.array([v[3e-4] / v[0.0] for v in ds.values() if 3e-4 in v and 0.0 in v])
    c34 = np.array([v[3e-4] / v[1e-3] for v in ds.values() if 3e-4 in v and 1e-3 in v])
    out = dict(n=len(r3))
    if len(r3):
        out.update(ratio_li1e3_over_causal=dict(median=float(np.median(r3)), err=boot(np.median, r3)[1], p16=float(np.quantile(r3, 0.16)),
                                                p84=float(np.quantile(r3, 0.84))))
    if len(r4):
        out.update(ratio_li3e4_over_causal=dict(median=float(np.median(r4)), err=boot(np.median, r4)[1], n=len(r4)),
                   li3e4_over_li1e3=dict(median=float(np.median(c34)), min=float(c34.min()), max=float(c34.max())))
    return out


def t3ev():
    T3 = np.load(os.path.join(TT, 'figures', 'T3_ms_thickness.npy'))
    res = {}
    for m in (200.0, 500.0, 1000.0):
        for lam in (1.0, 3.0, 10.0):
            sel = (T3[:, 0] == m) & (T3[:, 1] == lam)
            t3 = {int(r[2]): r[6] for r in T3[sel]}
            mine = {}
            for tag, z in fix_load('t3ev', m, f'').items():
                p = tag.split('_')
                if float(p[2]) == lam:
                    mine[int(p[3])] = float(z['ds'])
            ids = sorted(set(t3) & set(mine))
            if not ids:
                continue
            rat = np.array([mine[i] / t3[i] for i in ids])
            a3 = np.array([t3[i] for i in ids]) * 1e4
            m3 = F.fu_load  # placeholder
            m3v = []
            for f in glob.glob(os.path.join(D, 'M3', f"m{m:g}_L{lam:g}_e*_prod_*.npz")):
                z = np.load(f); fr = z['fracs']; v = z['ds'][np.isclose(fr, 1.0)][0]
                if np.isfinite(v):
                    m3v.append(v * 1e4)
            m3v = np.array(m3v)
            gt3 = np.array([r[4] for r in T3[sel]])
            res[f'm{m:g}_L{lam:g}'] = dict(n=len(ids), rerun_over_T3_median=float(np.median(rat)), rerun_over_T3_min=float(rat.min()),
                                           rerun_over_T3_max=float(rat.max()),
                                           T3_median_um=boot(np.median, a3)[:2], M3_median_um=boot(np.median, m3v)[:2],
                                           T3_gstar_median=float(np.median(gt3)))
    return res


def b6iii():
    import M1_analysis as A
    laws = A.m2_laws()
    out = {}
    for setting in ('prod', 'fine', 'vfine'):
        rows = []
        for m in (200.0, 500.0, 1000.0):
            for lam in ((1.0,) if setting == 'vfine' else (0.6, 1.0, 2.0)):
                evs = A.load(m, lam, setting)
                for d in evs:
                    if d['iev'] >= 60:
                        continue
                    try:
                        rr = A.per_crossing([d], laws)
                    except (IndexError, ValueError):
                        continue
                    odd = [r for r in rr if r['parity'] == 1]; even = [r for r in rr if r['parity'] == 0]
                    if not odd or not even:
                        continue
                    g = d['gstar']; rho = np.sqrt(g * g - 1); bs = rho / g
                    G = 2 * (g - np.arcsinh(rho) / rho) / (rho * np.arctanh(bs))
                    eps = np.median([r['eps'] for r in odd]); bl = eps * (g - np.arcsinh(rho) / rho) / (g - 1)
                    eta = G * (np.log(1 / bl) + F.Kfun(g))
                    rows.append(dict(m=m, lam=lam, iev=d['iev'], g=g, res_odd=np.median([r['psi'] - r['psi_pred_M2b'] for r in odd]),
                                     res_pair=np.median([r['psi'] for r in odd]) + np.median([r['psi'] for r in even]) - eta))
        out[setting] = rows
    # paired comparison on common (m, lam, iev) with gamma* < 1.2
    res = {}
    key = lambda r: (r['m'], r['lam'], r['iev'])
    P = {s: {key(r): r for r in out[s]} for s in out}
    for a, b in (('prod', 'fine'), ('fine', 'vfine'), ('prod', 'vfine')):
        ks = [k for k in P[a] if k in P[b] and P[a][k]['g'] < 1.2]
        if len(ks) < 3:
            continue
        for q in ('res_odd', 'res_pair'):
            va = np.array([P[a][k][q] for k in ks]); vb = np.array([P[b][k][q] for k in ks])
            res[f'{a}_vs_{b}_{q}_g<1.2'] = dict(n=len(ks), a_median=F.med_boot(va)[:2], b_median=F.med_boot(vb)[:2],
                                               paired_diff=F.med_boot(va - vb)[:2])
    for s in out:
        rr = [r for r in out[s] if r['g'] < 1.2]
        if rr:
            res[f'{s}_all_g<1.2'] = dict(n=len(rr), res_odd=F.med_boot([r['res_odd'] for r in rr])[:2],
                                         res_pair=F.med_boot([r['res_pair'] for r in rr])[:2])
    return res


if __name__ == '__main__':
    out = dict(description=__doc__)
    for name, fn in (('A1a_kB_split', a1a), ('A1b_vfine40', a1b), ('replicas', rep), ('B6i_li_gamma2', li2),
                     ('B6ii_T3_events', t3ev), ('B6iii_lowgamma_residual', b6iii)):
        try:
            out[name] = fn()
        except Exception as e:      # keep partial results while runs are still in progress
            out[name] = dict(error=repr(e))
        print(f'=== {name}'); print(json.dumps(out[name], default=float)[:3500])
    out['roundoff_FU_from_json'] = json.load(open(os.path.join(HERE, 'results', 'FU.json')))['FU1b'].get('roundoff_L3')
    dump(out, os.path.join(HERE, 'results', 'FIX1.json'))
