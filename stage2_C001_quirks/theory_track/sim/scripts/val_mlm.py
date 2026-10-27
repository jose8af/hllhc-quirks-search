"""val_mlm.py -- VALIDATION §4: MLM matching (differential jet rates, qCut variation, multiplicity, ME-cut closure).
Run: pixi run -e ana python scripts/val_mlm.py.  Output: results/mlm.json, figures/djr_*.png, figures/mlm_*.png.
DJR source: ../data/sim/aux/<ID>/m<m>_c<k>/tag_1_djrs.dat (MG5aMC_PY8_interface histograms log10 d_{n,n+1} per ME
multiplicity JETSAMPLE@0/1/2; columns xmin xmax central dy TMS=... scale variations).  Chunks are summed."""
import glob
import os
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from vlib import S, have, save, FIG, LABEL, DATA, hist_norm


def read_djr(files):
    """Raw MG5aMC_PY8_interface djrs.dat of each split job: one <run> with 12 <histogram> blocks = (log10d01, d12, d23, d34)
    for ME multiplicity 0, then 1, then 2; columns xmin xmax Weight_MERGING=<qCut> WeightError <other variations...>.
    Splits are averaged (equal-size jobs)."""
    H = {}
    cols = None
    for f in files:
        txt = open(f).read()
        cols = re.search(r'header="([^"]*)"', txt).group(1).split(';')
        count = {}
        for blk in txt.split('<histogram name="')[1:]:
            name = blk.split('"', 1)[0]
            k = count.get(name, 0); count[name] = k + 1
            rows = []
            for l in blk.split('\n')[1:]:
                if l.strip().startswith('</histogram'):
                    break
                p = l.split()
                if len(p) >= 4:
                    rows.append([float(x) for x in p])
            a = np.array(rows)
            key = (name, k)
            n = len(files)
            if key in H:
                e2 = H[key][:, 3] ** 2 + (a[:, 3] / n) ** 2
                H[key][:, 2:] += a[:, 2:] / n
                H[key][:, 3] = np.sqrt(e2)
            else:
                H[key] = a.copy(); H[key][:, 2:] /= n
    return H, cols


def step_test(x, y, err2, lq, half=0.3):
    """Local step test at log10(qCut) (review S2-R1 B8): weighted straight-line fits of ln(y) on [lq-half, lq) and
    (lq, lq+half]; discontinuity = exp(right(lq) - left(lq)) - 1 with its fit error; slope ratio right/left; and the
    adjacent-bin step = y(first bin right of lq) / y(last bin left of lq) / exp(mean slope x bin distance) - 1.
    PASS_10pct (plan V4a: no step > 10 % at qCut) if |disc| < 0.10; also reported: significance of the step |disc|/err."""
    ok = (y > 0) & (err2 > 0)
    res = {}
    fits = {}
    for side, sel in (('left', ok & (x >= lq - half) & (x < lq)), ('right', ok & (x > lq) & (x <= lq + half))):
        if sel.sum() < 3:
            return None
        sig = np.sqrt(err2[sel]) / y[sel]                # error of ln y
        A = np.vstack([np.ones(sel.sum()), x[sel] - lq]).T / sig[:, None]
        b = np.log(y[sel]) / sig
        cov = np.linalg.inv(A.T @ A); p = cov @ A.T @ b
        chi2 = float(np.sum((A @ p - b) ** 2)); ndf = int(sel.sum() - 2)
        fits[side] = (p, cov); res[f'{side}_chi2_ndf'] = chi2 / max(ndf, 1); res[f'slope_{side}'] = float(p[1])
    d = fits['right'][0][0] - fits['left'][0][0]
    de = float(np.sqrt(fits['right'][1][0, 0] + fits['left'][1][0, 0]))
    res['disc'] = float(np.exp(d) - 1); res['disc_err'] = float(np.exp(d) * de)
    res['slope_ratio'] = res['slope_right'] / res['slope_left'] if res['slope_left'] != 0 else None
    il = np.where(ok & (x < lq))[0][-1]; ir = np.where(ok & (x > lq))[0][0]
    ms = 0.5 * (res['slope_left'] + res['slope_right'])
    res['adjacent_bin_step'] = float(y[ir] / y[il] / np.exp(ms * (x[ir] - x[il])) - 1)
    res['adjacent_bin_step_err'] = float(np.sqrt(err2[ir] / y[ir] ** 2 + err2[il] / y[il] ** 2))
    res['PASS_10pct'] = bool(abs(res['disc']) < 0.10)
    res['disc_significance'] = float(abs(res['disc']) / res['disc_err'])
    return res


def djr_plot(id_, m, qcut):
    files = sorted(glob.glob(os.path.join(DATA, 'aux', id_, f'm{m}_c*', 'split_*', 'djrs.dat')))
    if not files:
        return None
    H, cols = read_djr(files)
    out = {}
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.5), sharex='col', gridspec_kw=dict(height_ratios=[3, 1]))
    for j, var in enumerate(('log10d01', 'log10d12')):
        ax = axes[0, j]
        tot = None
        for k in (0, 1, 2):
            a = H.get((var, k))
            if a is None:
                continue
            x = 0.5 * (a[:, 0] + a[:, 1]); y = a[:, 2]
            ax.step(x, y, where='mid', label=f'{k}-parton ME')
            tot = y.copy() if tot is None else tot + y
            err2 = a[:, 3] ** 2 if k == 0 else err2 + a[:, 3] ** 2
        ax.step(x, tot, where='mid', color='k', label='sum')
        lq = np.log10(qcut)
        ax.axvline(lq, color='gray', ls=':'); ax.set_yscale('log'); ax.legend(fontsize=7)
        ax.set_title(f'{LABEL}  {id_} m={m}: {var}', loc='left', fontsize=9)
        # smoothness: ratio of the summed DJR to a quadratic fit in log(y) over a window around log10(qCut)
        win = (x > lq - 0.6) & (x < lq + 0.6) & (tot > 0)
        if win.sum() > 5:
            cf = np.polyfit(x[win], np.log(tot[win]), 2)
            fit = np.exp(np.polyval(cf, x))
            r = tot / fit
            near = (np.abs(x - lq) < 0.1) & (tot > 0)
            pull = (tot - fit) / np.sqrt(np.maximum(err2, 1e-300))
            out[var] = dict(max_dev_near_qcut=float(np.max(np.abs(r[near] - 1))) if near.any() else None,
                            rms_dev_window=float(np.sqrt(np.mean((r[win] - 1) ** 2))),
                            chi2_ndf_window=float(np.sum(pull[win] ** 2) / max(win.sum() - 3, 1)),
                            mean_rel_stat_err_window=float(np.mean(np.sqrt(err2[win]) / tot[win])))
            out[var]['step_at_qcut'] = step_test(x, tot, err2, lq)
            axes[1, j].plot(x[win], r[win], '.'); axes[1, j].axhline(1, color='k', lw=0.6); axes[1, j].set_ylim(0.7, 1.3)
            axes[1, j].axvline(lq, color='gray', ls=':')
        axes[1, j].set_xlabel(var + ' [log10 GeV]'); axes[1, 0].set_ylabel('sum / smooth fit')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, f'djr_{id_}_m{m}.png'), dpi=110); plt.close(fig)
    return out


def fpt(c, w=None, cut=200.0):
    w = c['w'] if w is None else w
    return float(w[c['pt'] > cut].sum() / w.sum())


def main():
    R = dict(note=__doc__)
    R['djr'] = {}
    for id_, m, q in (('E-INC', 200, 45), ('E-INC', 500, 45), ('E-INC', 1000, 45), ('V-MERGE-20', 500, 30),
                      ('V-MERGE-50', 500, 75), ('E-TRG', 500, 45), ('S-INC', 500, 45)):
        if have(id_, m):
            R['djr'][f'{id_}_m{m}'] = djr_plot(id_, m, q)
    # qCut variation (500 GeV)
    qv = {}
    for id_, lab in (('V-MERGE-20', 'xqcut20_qcut30'), ('E-INC', 'xqcut30_qcut45'), ('V-MERGE-50', 'xqcut50_qcut75'), ('V-NJ1', 'nj1_xqcut30_qcut45')):
        if have(id_, 500):
            c = S(id_, 500)
            qv[lab] = dict(sigma_fb=float(c['w'].sum()), f_pt200=fpt(c), f_pt300=fpt(c, cut=300), n=int(len(c['w'])))
    if have('E-INC', 500):
        c = S('E-INC', 500)
        for n in c['wvar_names']:
            if n.startswith('Weight_MERGING=') and not n.endswith('45.000'):
                w = c['wvar'][:, c['wvar_names'].index(n)]
                qv['inweight_' + n.split('=')[1]] = dict(sigma_fb=float(w.sum()), f_pt200=fpt(c, w), f_pt300=fpt(c, w, 300))
    R['qcut_variation_m500'] = qv
    # figure: pT(QQ) spectra for the merging variations, normalised
    if qv:
        b = np.concatenate([np.linspace(0, 200, 21), np.linspace(220, 800, 30)])
        fig, ax = plt.subplots(2, 1, figsize=(6.5, 6), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
        ref = S('E-INC', 500); h0, e0 = hist_norm(ref['pt'], ref['w'], b)
        cx = 0.5 * (b[1:] + b[:-1])
        for id_, lab in (('E-INC', '(30,45) nominal'), ('V-MERGE-20', '(20,30)'), ('V-MERGE-50', '(50,75)'), ('V-NJ1', '0-1j (30,45)')):
            if have(id_, 500):
                c = S(id_, 500); h, e = hist_norm(c['pt'], c['w'], b)
                ax[0].errorbar(cx, h, yerr=e, fmt='.', ms=3, label=lab)
                with np.errstate(divide='ignore', invalid='ignore'):
                    ax[1].errorbar(cx, h / h0, yerr=e / h0, fmt='.', ms=3)
        for n in ('Weight_MERGING=67.500', 'Weight_MERGING=90.000'):
            w = ref['wvar'][:, ref['wvar_names'].index(n)]; h, e = hist_norm(ref['pt'], w, b)
            ax[0].step(cx, h, where='mid', label='in-weight qCut ' + n.split('=')[1])
            with np.errstate(divide='ignore', invalid='ignore'):
                ax[1].step(cx, h / h0, where='mid')
        ax[0].set_yscale('log'); ax[0].legend(fontsize=7); ax[0].set_title(f'{LABEL}  E, m=500: merging variations', loc='left', fontsize=9)
        ax[1].set_ylim(0.6, 1.4); ax[1].axhline(1, color='k', lw=0.6); ax[1].set_xlabel('p_T(QQ̄) [GeV]'); ax[1].set_ylabel('var / nominal')
        fig.tight_layout(); fig.savefig(os.path.join(FIG, 'mlm_qcut_variation_m500.png'), dpi=110); plt.close(fig)
    # ME-cut closure (TRG vs INC above 200) and migration fraction
    clo = {}
    for spin, pre in (('F', 'E'), ('S', 'S')):
        for m in (200, 500, 1000):
            if not (have(f'{pre}-INC', m) and have(f'{pre}-TRG', m)):
                continue
            inc, trg = S(f'{pre}-INC', m), S(f'{pre}-TRG', m)
            si = inc['pt'] > 200; st = trg['pt'] > 200
            s_inc = inc['w'][si].sum(); s_trg = trg['w'][st].sum()
            e_inc = np.sqrt(np.sum(inc['w'][si] ** 2)); e_trg = np.sqrt(np.sum(trg['w'][st] ** 2))
            mig = inc['w'][si & (inc['pt_hard'] < 100)].sum() / s_inc
            mig_e = np.sqrt(np.sum(inc['w'][si & (inc['pt_hard'] < 100)] ** 2)) / s_inc
            b = np.linspace(200, 1000, 17); cx = 0.5 * (b[1:] + b[:-1])
            hi, ei = np.histogram(inc['pt'][si], b, weights=inc['w'][si])[0], np.sqrt(np.histogram(inc['pt'][si], b, weights=inc['w'][si] ** 2)[0])
            ht, et = np.histogram(trg['pt'][st], b, weights=trg['w'][st])[0], np.sqrt(np.histogram(trg['pt'][st], b, weights=trg['w'][st] ** 2)[0])
            ok = (ei > 0) & (et > 0)
            chi2 = float(np.sum((hi[ok] - ht[ok]) ** 2 / (ei[ok] ** 2 + et[ok] ** 2)))
            sh = si & (inc['pt_hard'] >= 100)
            s_inc_h = inc['w'][sh].sum(); e_inc_h = np.sqrt(np.sum(inc['w'][sh] ** 2))
            gen_cut = dict(sigma_pt200_INC_MEge100=s_inc_h, ratio_TRG_over_INC_MEge100=s_trg / s_inc_h,
                           ratio_err=s_trg / s_inc_h * np.hypot(e_inc_h / s_inc_h, e_trg / s_trg))
            clo[f'{spin}_{m}'] = dict(generation_cut_closure=gen_cut, sigma_pt200_INC_fb=s_inc, err_INC=e_inc, sigma_pt200_TRG_fb=s_trg, err_TRG=e_trg,
                                      ratio_TRG_over_INC=s_trg / s_inc, ratio_err=s_trg / s_inc * np.hypot(e_inc / s_inc, e_trg / s_trg),
                                      migration_MEpt_lt100=mig, migration_err=mig_e,
                                      migration_MEpt_lt150=float(inc['w'][si & (inc['pt_hard'] < 150)].sum() / s_inc),
                                      shape_chi2=chi2, ndf=int(ok.sum()),
                                      f_TRG_events_pt200=float(np.mean(trg['pt'][trg['w'] > 0] > 200)))
            if m == 500:
                fig, ax = plt.subplots(2, 1, figsize=(6, 5.5), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
                ax[0].errorbar(cx, hi, yerr=ei, fmt='o', ms=3, label='E-INC (no ME cut)')
                ax[0].errorbar(cx, ht, yerr=et, fmt='s', ms=3, label='E-TRG (ME pT(QQ̄)>100)')
                ax[0].set_yscale('log'); ax[0].legend(fontsize=8); ax[0].set_ylabel('dσ [fb/bin], N_IC=1')
                ax[0].set_title(f'{LABEL}  {pre}, m={m}: ME-cut closure', loc='left', fontsize=9)
                with np.errstate(divide='ignore', invalid='ignore'):
                    ax[1].errorbar(cx, ht / hi, yerr=ht / hi * np.hypot(ei / hi, et / ht), fmt='.')
                ax[1].axhline(1, color='k', lw=0.6); ax[1].set_ylim(0.7, 1.3); ax[1].set_xlabel('p_T(QQ̄) [GeV]'); ax[1].set_ylabel('TRG/INC')
                fig.tight_layout(); fig.savefig(os.path.join(FIG, f'mlm_closure_{spin}_m{m}.png'), dpi=110); plt.close(fig)
    R['me_cut_closure'] = clo
    save('mlm.json', R)
    print('wrote results/mlm.json')


if __name__ == '__main__':
    main()
