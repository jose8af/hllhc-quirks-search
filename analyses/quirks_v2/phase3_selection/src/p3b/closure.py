"""B2 development closure, s_model, N_eff, widths and the day-15 pile-up term (p3-b, executor Casper).

Run on a worker (numpy/scipy; light):  python closure.py  -> outputs/p3b/b2_dev_closure.json, outputs/p3b/pileup_term.json
Inputs (campaign outputs on cajuela, development role only):
  p3-b-thin    repaired thinning of C1 pu2 (1,000 events, 2,000 trials, K = 64)
  p3-b-direct  direct counts of C1 pu1 (4,000 events, 16,000 trials)
  p3-b-occin   occupancy inputs on the same pu1 events (densities; random-plane ensemble on real hits)
  p3-b-occmod  occupancy model evaluated on the ensemble (stage A/B sums)
Every rule below is STR §4.0 points 2-7 as frozen; nothing here is tuned to a result (see the artifact).
"""
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np
from scipy.stats import chi2 as CHI2

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cols as TC  # noqa: E402

DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3b')
OUT = HERE.parents[1] / 'outputs' / 'p3b'
log = logging.getLogger('closure')

LN15 = np.log(1.5)
CAP = LN15 / 3                      # 0.135: s_model cap and evaluable limit for F = 1.5 (STR §4.0 points 3, 4 (c))
B0 = LN15                           # b0 = ln F (point 7)
K_FAM = 13                          # K after addendum 1 (COM l.340): INVESTIGATE/re-test level 0.05/K
NTRIG_V1 = 4.0848e7                 # phase1_strategy/src/strategy_budget.py l.68 (bsum_wp.json n_trig) [UNVERIFIED there]
NB = 2000
COL = {c: i for i, c in enumerate(TC.COLS)}
CUM = ['R04', 'R05', 'R06', 'R07']
CROSS = ['R04x2S>=1', 'R04x2S>=2', 'R04x2S>=3', 'R05x2S>=1', 'R05x2S>=2', 'R05x2S>=3', 'R06x2S>=1', 'R06x2S>=2',
         'R06x2S>=3', 'R05xp>0.001', 'R05xp>0.01', 'R05xp>0.05', 'R06xp>0.001', 'R06xp>0.01', 'R06xp>0.05']
RIDX = {'R04': 4, 'R05': 5, 'R06': 6, 'R07': 7, 'R08': 8, 'R09': 9}


def ev_keys(job, ev):
    k = np.char.add(np.char.add(job.astype(str), '|'), ev.astype(str))
    u, inv = np.unique(k, return_inverse=True)
    return inv, len(u)


def boot_weights(nev, B, seed):
    rng = np.random.default_rng(seed)
    return rng.multinomial(nev, np.full(nev, 1.0 / nev), size=B).astype(np.float64)


def rates_boot(X, inv, nev, W):
    """X (ntr, ncol) per-trial values; W (B, nev) event weights -> nominal rates (ncol,), replicas (B, ncol)."""
    Se = np.zeros((nev, X.shape[1])); np.add.at(Se, inv, X)
    ne = np.bincount(inv, minlength=nev).astype(np.float64)
    nom = Se.sum(0) / ne.sum()
    rep = (W @ Se) / (W @ ne)[:, None]
    return nom, rep


def load(campaign, pattern):
    fs = sorted(glob.glob(str(DATA / campaign / '*' / pattern)))
    return fs, [np.load(f) for f in fs]


def closure_block(ln_nom, ln_rep, N, sP, names, smodel):
    """(a), (b), evaluability for one estimator against direct counts.  ln_nom/ln_rep: ln r nominal and replicas."""
    out = {}
    sig = np.sqrt(1.0 / np.maximum(N, 1e-300) + sP ** 2)
    ev = np.isfinite(ln_nom) & (N > 0) & (sig <= CAP)
    for i, n in enumerate(names):
        a = None
        if ev[i]:
            x = abs(ln_nom[i])
            a = 'pass' if x <= LN15 else ('INVESTIGATE' if x <= LN15 + 2 * sig[i] else 'FAIL')
        out[n] = dict(ln_r=float(ln_nom[i]) if np.isfinite(ln_nom[i]) else None, r=float(np.exp(ln_nom[i]))
                      if np.isfinite(ln_nom[i]) else None, N_direct=float(N[i]), s_P=float(sP[i]),
                      sigma_tot=float(sig[i]), evaluable=bool(ev[i]), tolerance_a=a)
    e = np.where(ev)[0]
    res = dict(rungs=out, evaluable=[names[i] for i in e])
    if len(e):
        V = np.cov(ln_rep[:, e].T, ddof=1).reshape(len(e), len(e))
        y = ln_nom[e]
        for lab, sm in (('V_boot_only', 0.0), ('V_boot_plus_smodel2J', smodel)):
            Vt = V + sm ** 2 * np.ones((len(e), len(e)))
            c2 = float(y @ np.linalg.solve(Vt, y))
            p = float(CHI2.sf(c2, len(e)))
            pulls = (y / np.sqrt(np.diag(Vt))).tolist()
            res[lab] = dict(chi2=c2, ndf=len(e), chi2_ndf=c2 / len(e), p=p, pulls=pulls,
                            b_verdict='pass' if p >= 0.05 else ('INVESTIGATE' if p >= 0.05 / K_FAM else 'FAIL'),
                            jfc_alarm=bool(c2 / len(e) < 0.1 or c2 / len(e) > 3 or max(abs(np.array(pulls))) > 5))
    return res


def slope_options(y, V, idx):
    """Slope of ln r against the rung index under the weight options of EXP §10 item 8 (reported, none chosen)."""
    x = np.asarray(idx, float)
    X = np.c_[np.ones_like(x), x]
    o = {}
    for lab, Wm in (('unweighted_OLS', np.eye(len(x))), ('WLS_bootstrap_diag', np.diag(1 / np.diag(V))),
                    ('GLS_full_bootstrap_covariance', np.linalg.inv(V))):
        A = X.T @ Wm @ X
        beta = np.linalg.solve(A, X.T @ Wm @ y)
        # covariance of the estimator under the true covariance V (sandwich), valid for any weight choice
        Ai = np.linalg.inv(A)
        cov = Ai @ X.T @ Wm @ V @ Wm @ X @ Ai
        o[lab] = dict(b=float(beta[1]), sigma_b=float(np.sqrt(cov[1, 1])))
    return o


def s_tot(smodel, sf, bhat, sigb, d_in, d_out):
    return float(np.sqrt(smodel ** 2 + sf ** 2 + (bhat ** 2 + sigb ** 2) * d_in ** 2 + B0 ** 2 * d_out ** 2))


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    OUT.mkdir(parents=True, exist_ok=True)
    R = {}
    # ---------------- direct development counts
    fd, dd = load('p3-b-direct', 'direct-*.npz')
    Gd = np.concatenate([d['grp'] for d in dd]).astype(np.float64)
    invd, nevd = ev_keys(np.concatenate([d['job'] for d in dd]), np.concatenate([d['ev'] for d in dd]))
    Wd = boot_weights(nevd, NB, 11)
    dnom, drep = rates_boot(Gd, invd, nevd, Wd)
    Nd = Gd.sum(0)
    R['direct'] = dict(files=len(fd), trials=int(len(Gd)), events=int(nevd),
                       counts={c: float(Nd[i]) for i, c in enumerate(TC.COLS)},
                       rate={c: float(dnom[i]) for i, c in enumerate(TC.COLS)})
    # ---------------- repaired thinning
    ft, tt = load('p3-b-thin', 'thin-*.npz')
    have_thin = len(tt) > 0
    if have_thin:
        G = np.concatenate([d['grp'] for d in tt]).astype(np.float64)          # (ntr, K, ncol)
        Pn = np.concatenate([d['npass'] for d in tt]).astype(np.float64)
        Tm = G.mean(1)
        invt, nevt = ev_keys(np.concatenate([d['job'] for d in tt]), np.concatenate([d['ev'] for d in tt]))
        Wt = boot_weights(nevt, NB, 12)
        tnom, trep = rates_boot(Tm, invt, nevt, Wt)
        unom, _ = rates_boot(Pn.mean(1), invt, nevt, Wt)
        with np.errstate(divide='ignore', invalid='ignore'):
            sP = np.std(trep, axis=0, ddof=1) / tnom          # relative bootstrap error (defined when replicas hit 0)
            ln_nom = np.log(tnom / dnom)
            ln_rep = np.log(trep / drep)
        neff = np.where(np.isfinite(sP) & (sP > 0), 1.0 / sP ** 2, 0.0)
        names = CUM + CROSS
        ix = [COL[c] for c in names]
        cum_ix = [COL[c] for c in CUM]
        # s_model of thinning: r.m.s. of ln r over the evaluable development rungs (cumulative; crossing variant)
        sig = np.sqrt(1 / np.maximum(Nd, 1e-300) + sP ** 2)
        evc = [i for i in cum_ix if np.isfinite(ln_nom[i]) and Nd[i] > 0 and sig[i] <= CAP]
        evx = [i for i in ix if np.isfinite(ln_nom[i]) and Nd[i] > 0 and sig[i] <= CAP]
        sm_c = float(np.sqrt(np.mean(ln_nom[evc] ** 2))) if evc else None
        sm_x = float(np.sqrt(np.mean(ln_nom[evx] ** 2))) if evx else None
        blk = closure_block(ln_nom[ix], ln_rep[:, ix], Nd[ix], sP[ix], names, sm_c or 0.0)
        # slope options on the evaluable cumulative rungs
        e_i = [i for i in cum_ix if i in evc]
        sl = None
        if len(e_i) >= 2:
            Vc = np.cov(ln_rep[:, e_i].T, ddof=1)
            sl = slope_options(ln_nom[e_i], Vc, [RIDX[TC.COLS[i]] for i in e_i]) if len(e_i) >= 3 else \
                dict(two_point=dict(b=float((ln_nom[e_i[-1]] - ln_nom[e_i[0]]) / (RIDX[TC.COLS[e_i[-1]]] -
                                                                                    RIDX[TC.COLS[e_i[0]]])), sigma_b=B0))
        R['thinning'] = dict(files=len(ft), trials=int(len(Tm)), events=int(nevt), K=int(G.shape[1]),
                             rate={c: float(tnom[i]) for i, c in enumerate(TC.COLS)},
                             union_rate={c: float(unom[i]) for i, c in enumerate(TC.COLS)},
                             s_boot={c: float(sP[i]) for i, c in enumerate(TC.COLS)},
                             N_eff={c: float(neff[i]) for i, c in enumerate(TC.COLS)},
                             closure=blk, s_model_cumulative=sm_c, s_model_with_crossing=sm_x,
                             cap=CAP, above_cap_cumulative=None if sm_c is None else bool(sm_c > CAP),
                             above_cap_with_crossing=None if sm_x is None else bool(sm_x > CAP), slope=sl)
        # B2-g: projection of N_eff to 3,000 rho = 2 events (N_eff ∝ events) against the 96,000-trial direct sample
        proj = {}
        for c in ['R04', 'R05', 'R06', 'R07', 'R08', 'R06x2S>=3', 'R07x2S>=3', 'R06xp>0.001']:
            i = COL[c]
            n96 = dnom[i] * 96000
            ne3 = neff[i] * 3000 / nevt
            st = np.sqrt((1 / n96 if n96 > 0 else np.inf) + (1 / ne3 if ne3 > 0 else np.inf))
            proj[c] = dict(N_eff_dev=float(neff[i]), N_eff_3000=float(ne3), N_direct_96k_expected=float(n96),
                           sigma_tot=float(st), evaluable=bool(st <= CAP))
        R['thinning']['B2g_projection'] = proj
    # ---------------- occupancy model
    fo, oo = load('p3-b-occin', 'occin-*.npz')
    fm, mm = load('p3-b-occmod', 'occmod-*.npz')
    if oo and mm:
        cnt = np.concatenate([d['cnt'] for d in oo]).astype(np.float64)
        planes = json.loads(str(oo[0]['meta_json']))['planes']
        invo, nevo = ev_keys(np.concatenate([d['job'] for d in oo]), np.concatenate([d['ev'] for d in oo]))
        # the occin events are the direct events: joint bootstrap over the same event keys
        kd = np.unique(np.char.add(np.char.add(np.concatenate([d['job'] for d in dd]).astype(str), '|'),
                                   np.concatenate([d['ev'] for d in dd]).astype(str)))
        ko = np.unique(np.char.add(np.char.add(np.concatenate([d['job'] for d in oo]).astype(str), '|'),
                                   np.concatenate([d['ev'] for d in oo]).astype(str)))
        same = bool(len(kd) == len(ko) and np.all(kd == ko))
        pnom, prep = rates_boot(cnt / planes, invo, nevo, Wd if same else boot_weights(nevo, NB, 13))
        # model expectations per column (stage A x stage B), per seed file -> mean and MC spread
        cols_m = ['R04', 'R05', 'R06', 'R07', 'R08', 'R04x2S>=1', 'R04x2S>=2', 'R04x2S>=3', 'R05x2S>=1', 'R05x2S>=2',
                  'R05x2S>=3', 'R06x2S>=1', 'R06x2S>=2', 'R06x2S>=3', 'R07x2S>=3', 'R08x2S>=3']
        Em = []; Em_plain = []
        for d in mm:
            pa = d['pA'].mean()
            isw = d['isr'][:, :, 0]                       # (nB, 4) IS estimate of P(w < W_k | R04, θ)
            pl = d['plain']
            p2 = d['p2B']
            e = {'R04': pa}; ep = {'R04': pa}
            for k, c in enumerate(['R05', 'R06', 'R07', 'R08']):
                e[c] = pa * isw[:, k].mean(); ep[c] = pa * pl[:, k].mean()
            for j in (1, 2, 3):
                e[f'R04x2S>={j}'] = pa * p2[:, j - 1].mean()
                for k, c in enumerate(['R05', 'R06']):
                    e[f'{c}x2S>={j}'] = pa * (p2[:, j - 1] * isw[:, k]).mean()
            e['R07x2S>=3'] = pa * (p2[:, 2] * isw[:, 2]).mean()
            e['R08x2S>=3'] = pa * (p2[:, 2] * isw[:, 3]).mean()
            Em.append([e[c] for c in cols_m]); Em_plain.append([ep.get(c, np.nan) for c in cols_m])
        Em = np.array(Em); Em_plain = np.array(Em_plain)
        em = Em.mean(0)
        em_err = Em.std(0, ddof=1) / np.sqrt(len(Em)) if len(Em) > 1 else np.full(len(cols_m), np.nan)
        sm_mc = em_err / em                             # relative MC error of the model
        ci = {c: i for i, c in enumerate(cols_m)}
        P = {c: pnom[COL[c]] for c in cols_m}
        C04 = P['R04'] / em[ci['R04']]; C05 = P['R05'] / em[ci['R05']]
        # N_cfg from R04-R05 (GLS on y = ln(B_dir / P_real), joint bootstrap covariance)
        i4, i5 = COL['R04'], COL['R05']
        y = np.log(dnom[[i4, i5]] / pnom[[i4, i5]])
        yrep = np.log(drep[:, [i4, i5]] / prep[:, [i4, i5]])
        Vy = np.cov(yrep.T, ddof=1)
        one = np.ones(2)
        lnN = float(one @ np.linalg.solve(Vy, y) / (one @ np.linalg.solve(Vy, one)))
        lnN_rep = (np.linalg.solve(Vy, one) @ yrep.T) / (one @ np.linalg.solve(Vy, one))
        Ncfg = np.exp(lnN)
        wdiag = 1 / np.diag(Vy)
        lnN_diag = float(np.dot(wdiag, y) / wdiag.sum())          # reported variant (diagonal weights)
        gls_w = np.linalg.solve(Vy, one) / (one @ np.linalg.solve(Vy, one))
        insample = {c: float(lnN + np.log(pnom[COL[c]]) - np.log(dnom[COL[c]])) for c in ('R04', 'R05')}
        rms_in = float(np.sqrt(np.mean(np.array(list(insample.values())) ** 2)))

        def pred(c, variant='const'):
            base = 'R04' if c.startswith('R04') else 'R05'
            C = C04 if base == 'R04' else C05
            k = RIDX[c[:3]] - 5 if base == 'R05' else 0
            if variant == 'trend' and k > 0:
                C = C05 * (C05 / C04) ** k
            return Ncfg * C * em[ci[c]]

        def pred_rep(c):
            """bootstrap replicas of the prediction (data part; the model MC error is added separately)."""
            base = 'R04' if c.startswith('R04') else 'R05'
            pr = prep[:, COL[base]] / em[ci[base]]
            return np.exp(lnN_rep) * pr * em[ci[c]]

        occ = dict(planes_per_trial=planes, trials=int(len(cnt)), same_events_as_direct=same,
                   P_real={c: float(pnom[COL[c]]) for c in cols_m + ['R06', 'R07']},
                   P_real_counts={c: float(cnt[:, COL[c]].sum()) for c in cols_m},
                   E_model={c: float(em[i]) for i, c in enumerate(cols_m)},
                   E_model_relMC={c: float(sm_mc[i]) for i, c in enumerate(cols_m)},
                   E_model_plain={c: float(np.nanmean(Em_plain[:, i])) for i, c in enumerate(cols_m)},
                   C_R04=float(C04), C_R05=float(C05), N_cfg=float(Ncfg), lnN_gls_weights=gls_w.tolist(),
                   N_cfg_diag_variant=float(np.exp(lnN_diag)), insample_ln_r=insample,
                   insample_rms=rms_in)
        rows = {}
        for c in cols_m:
            i = COL[c]
            for var in ('const', 'trend'):
                b = pred(c, var)
                lr = float(np.log(b / dnom[i])) if dnom[i] > 0 else None
                rep = pred_rep(c)
                sp = float(np.sqrt(np.var(np.log(rep), ddof=1) + sm_mc[ci[c]] ** 2))
                lrr = np.log(rep / drep[:, i]) if dnom[i] > 0 else None
                sig = float(np.sqrt(1 / Nd[i] + sp ** 2)) if Nd[i] > 0 else None
                rows.setdefault(c, {})[var] = dict(rate=float(b), ln_r=lr, s_P=sp, sigma_tot=sig, N_direct=float(Nd[i]),
                                                   evaluable=bool(sig is not None and sig <= CAP),
                                                   sd_lnr_boot=float(np.std(lrr, ddof=1)) if lrr is not None else None)
        occ['predictions'] = rows
        lr06 = rows['R06']['const']['ln_r']
        occ['held_out_R06'] = dict(const=lr06, trend=rows['R06']['trend']['ln_r'])
        occ['s_model'] = float(max(abs(lr06), rms_in)) if lr06 is not None else None
        occ['s_model_trend_variant'] = float(max(abs(rows['R06']['trend']['ln_r']), rms_in))
        occ['cap'] = CAP
        occ['above_cap'] = bool(occ['s_model'] > CAP) if occ['s_model'] is not None else None
        # fit-probability pass fractions from the development finder candidates passing R06 (Df-2; shared input)
        f = {p: float(dnom[COL[f'R06xp>{p}']] / dnom[COL['R06']]) for p in ('0.001', '0.01', '0.05')}
        occ['fitprob_fraction_from_R06_candidates'] = f
        # day-15 model: one scale A on R04-R07 (weights 1/(σ_stat² + s_model²)), widths from the model
        sm = occ['s_model']
        ys, ws = [], []
        for c in ('R04', 'R05', 'R06', 'R07'):
            i = COL[c]
            if Nd[i] <= 0:
                continue
            st2 = 1 / Nd[i] + sm_mc[ci[c]] ** 2
            ys.append(np.log(dnom[i] / em[ci[c]])); ws.append(1 / (st2 + sm ** 2))
        lnA = float(np.dot(ys, ws) / np.sum(ws))
        occ['day15_scale'] = dict(lnA=lnA, rungs_used=['R04', 'R05', 'R06', 'R07'], weights=[float(w) for w in ws],
                                  residuals={c: float(lnA - y_) for c, y_ in zip(('R04', 'R05', 'R06', 'R07'), ys)})
        R['occupancy'] = occ
    (OUT / 'b2_dev_closure.json').write_text(json.dumps(R, indent=1))
    log.info('written %s', OUT / 'b2_dev_closure.json')


if __name__ == '__main__':
    main()
