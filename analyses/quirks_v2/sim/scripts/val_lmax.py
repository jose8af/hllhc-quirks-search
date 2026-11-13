"""val_lmax.py -- VALIDATION §3: ISR-tail change and l_max / N_osc bias (synthesis S-13).  Run: pixi run -e ana python
scripts/val_lmax.py.  Output: results/lmax_bias.json, figures/lmax_bias.png.
l_max = 2 (gamma* - 1) m / sigma = 3.947 cm (gamma*-1)(m/100 GeV)(keV/Lambda)^2  [T2 §2.2]  -> we quote x = 2(gamma*-1)
(l_max in units of m/sigma, Lambda independent).  N_osc at Lambda = 1 keV (scales as Lambda^2), T2_kinematics formula.
Models (selection pT(QQ) > 200 GeV and |eta_pair| < 2.5, the T2 table selection, unless stated):
  (i)   fixed-pT trick [TH App. A; T2 §3]: inclusive LO kinematics (pT = 0) + a fixed pT = 250 GeV kick, all events
        (the trick applies no pT cut; gamma* is that of inclusive DY).  Built both from the old cache and from E-LOPS
        (pre-shower kinematics), (i') the same with |eta| < 2.5 after the kick.
  (ii)  old T2 LO V*+jet ('isr' cache).
  (iii) MG LO + Pythia shower (E-LOPS), after shower.
  (iv)  MG 0-2j MLM, stitched TRGS = E-TRG (ME cut 100) U E-INC[pT_ME < 100] = reference; E-INC as cross-check.
Uncertainties on (iv): bootstrap stat; scale (9-point weights); merging (V-MERGE-20/50 vs E-INC, 500 GeV); tune
(V-TUNE-TRG vs E-TRG); MPI (V-MPI vs E-TRG); shower (V-SHOWER) and emission alpha_s (MG --alps) from results/shower.json.
LIKE-FOR-LIKE (review S2-R1 B4, fixer): the selection of (i) has no eta cut, that of (iv) has |eta| < 2.5.  Reported:
  (i') vs (iv)      : |eta| < 2.5 on both sides = the like-for-like comparison (PRIMARY for N_osc and l_max);
  (i)  vs (iv-noeta): no eta cut on either side (reference TRGS with pT > 200 only) = T2 §3's definition as implemented
                       (T2_kinematics.py:287-302 used no eta cut on either side, m = 500 only);
  (i)  vs (iv)      : the mixed comparison quoted in the first VALIDATION draft (kept for traceability).
syst_budget: per point, the relative uncertainties of the reference median of x (prop. to l_max) and of N_osc:
stat, scale (half 9-pt envelope), merging (larger of |V-MERGE-20|, |V-MERGE-50| at 500 GeV, applied to every mass, ESTIMATE),
shower (larger of |V-SHOWER UP|, |DN| at 500 GeV, all masses, ESTIMATE), alps (larger of |alps 0.5|, |alps 2| at this
point); total = quadrature."""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from vlib import S, old, have, save, FIG, LABEL, boot_quant, wquant, nosc, neff

QS = (0.16, 0.5, 0.84)


def fixed_pt(g, y, w, m, pt=250.0):
    M = 2 * m * g
    mT = np.sqrt(M ** 2 + pt ** 2)
    pz = mT * np.sinh(y)
    bg = np.sqrt(pt ** 2 + pz ** 2) / M
    eta = np.arcsinh(pz / pt)
    return dict(g=g, w=w, bg=bg, eta=eta, nosc=nosc(g, bg, eta, m), pt=np.full_like(g, pt))


def stats(d, sel):
    x = 2 * (d['g'][sel] - 1); w = d['w'][sel]
    qx, ex = boot_quant(x, w, QS, nb=150)
    qn, en = boot_quant(d['nosc'][sel], w, QS, nb=150)
    return dict(x_q=qx, x_err=ex, nosc_q=qn, nosc_err=en, neff=neff(w))


def tailsel(d, eta=2.5):
    return (d['pt'] > 200) & (np.abs(d['eta']) < eta) & (d['w'] != 0)


def main():
    R = dict(note=__doc__, points={})
    for spin, pre in (('F', 'E'), ('S', 'S')):
        for m in (200, 500, 1000):
            if not (have(f'{pre}-TRGS', m) and have(f'{pre}-LOPS', m)):
                continue
            P = {}
            oi, ox = old(spin, m, 'incl'), old(spin, m, 'isr')
            P['i_fixedpt_oldcache'] = stats(fixed_pt(oi['g'], oi['y'], oi['w'], m), np.ones(len(oi['g']), bool))
            lops = S(f'{pre}-LOPS', m)
            yh = np.zeros_like(lops['g_hard'])
            H = lops['p_qq_hard']; yh = 0.5 * np.log((H[:, 0] + H[:, 3]) / (H[:, 0] - H[:, 3]))
            fx = fixed_pt(lops['g_hard'], yh, lops['w'], m)
            P['i_fixedpt_MGLO'] = stats(fx, np.ones(len(fx['g']), bool))
            P['ip_fixedpt_MGLO_eta25'] = stats(fx, np.abs(fx['eta']) < 2.5)
            P['ii_T2_Vjet'] = stats(ox, tailsel(ox))
            P['iii_MG_LOPS'] = stats(lops, tailsel(lops))
            trg = S(f'{pre}-TRGS', m)        # TRG U INC[pT_ME<100] (stitch_trg.py)
            P['iv_MG_MLM_TRGS'] = stats(trg, tailsel(trg))
            P['iv_MG_MLM_TRGS_noeta'] = stats(trg, tailsel(trg, eta=np.inf))
            P['iv_MG_MLM_TRG_mecut_only'] = stats(S(f'{pre}-TRG', m), tailsel(S(f'{pre}-TRG', m)))
            if have(f'{pre}-INC', m):
                inc = S(f'{pre}-INC', m)
                P['iv_MG_MLM_INC'] = stats(inc, tailsel(inc))
                P['f_pt200_INC'] = float(inc['w'][inc['pt'] > 200].sum() / inc['w'].sum())
            P['f_pt200_LOPS'] = float(lops['w'][lops['pt'] > 200].sum() / lops['w'].sum())
            # systematics on (iv)
            ref = P['iv_MG_MLM_TRGS']
            sel = tailsel(trg)
            sc = []
            for n in trg['wvar_names']:
                if n.startswith('MUF=') and 'PDF=14400_' in n:
                    w = trg['wvar'][:, trg['wvar_names'].index(n)]
                    s2 = sel & (w != 0)
                    sc.append((wquant(2 * (trg['g'][s2] - 1), w[s2])[1], wquant(trg['nosc'][s2], w[s2])[1]))
            sc = np.array(sc)
            syst = dict(scale_x=[sc[:, 0].min() / ref['x_q'][1] - 1, sc[:, 0].max() / ref['x_q'][1] - 1],
                        scale_nosc=[sc[:, 1].min() / ref['nosc_q'][1] - 1, sc[:, 1].max() / ref['nosc_q'][1] - 1])
            if spin == 'F' and m == 500:
                r_cut = stats(S('E-TRG', 500), tailsel(S('E-TRG', 500)))   # like-with-like: ME-cut samples
                for tag, id_ in (('tune_Monash', 'V-TUNE-TRG'), ('mpi_off', 'V-MPI')):
                    if have(id_, 500):
                        v = stats(S(id_, 500), tailsel(S(id_, 500)))
                        syst[tag + '_x'] = v['x_q'][1] / r_cut['x_q'][1] - 1
                        syst[tag + '_nosc'] = v['nosc_q'][1] / r_cut['nosc_q'][1] - 1
                        syst[tag + '_stat'] = float(np.hypot(v['x_err'][1] / v['x_q'][1], r_cut['x_err'][1] / r_cut['x_q'][1]))
                if have('E-INC', 500):
                    r0 = P['iv_MG_MLM_INC']
                    for tag in ('V-MERGE-20', 'V-MERGE-50'):
                        if have(tag, 500):
                            v = stats(S(tag, 500), tailsel(S(tag, 500)))
                            syst[tag + '_x'] = v['x_q'][1] / r0['x_q'][1] - 1
                            syst[tag + '_nosc'] = v['nosc_q'][1] / r0['nosc_q'][1] - 1
                            syst[tag + '_stat'] = float(np.hypot(v['x_err'][1] / v['x_q'][1], r0['x_err'][1] / r0['x_q'][1]))
            P['syst_on_iv'] = syst
            # biases relative to (iv)
            bias = {}
            for k in ('i_fixedpt_oldcache', 'i_fixedpt_MGLO', 'ip_fixedpt_MGLO_eta25', 'ii_T2_Vjet', 'iii_MG_LOPS', 'iv_MG_MLM_INC', 'iv_MG_MLM_TRG_mecut_only'):
                if k not in P:
                    continue
                v = P[k]
                bx = v['x_q'][1] / ref['x_q'][1] - 1
                ex = (1 + bx) * np.hypot(v['x_err'][1] / v['x_q'][1], ref['x_err'][1] / ref['x_q'][1])
                bn = v['nosc_q'][1] / ref['nosc_q'][1] - 1
                en = (1 + bn) * np.hypot(v['nosc_err'][1] / v['nosc_q'][1], ref['nosc_err'][1] / ref['nosc_q'][1])
                bias[k] = dict(lmax_median_bias=bx, lmax_stat=ex, nosc_median_bias=bn, nosc_stat=en)
            ref0 = P['iv_MG_MLM_TRGS_noeta']
            for k in ('i_fixedpt_oldcache', 'i_fixedpt_MGLO'):
                v = P[k]
                bx = v['x_q'][1] / ref0['x_q'][1] - 1
                bn = v['nosc_q'][1] / ref0['nosc_q'][1] - 1
                bias[k + '_vs_iv_noeta'] = dict(lmax_median_bias=bx, lmax_stat=(1 + bx) * np.hypot(v['x_err'][1] / v['x_q'][1], ref0['x_err'][1] / ref0['x_q'][1]),
                                                nosc_median_bias=bn, nosc_stat=(1 + bn) * np.hypot(v['nosc_err'][1] / v['nosc_q'][1], ref0['nosc_err'][1] / ref0['nosc_q'][1]))
            P['bias_vs_iv'] = bias
            # systematics budget on the reference medians (B5)
            sb = {}
            for q, key in (('x', 'x'), ('nosc', 'nosc')):
                st = ref[f'{key}_err'][1] / ref[f'{key}_q'][1]
                scl = 0.5 * (syst[f'scale_{key}'][1] - syst[f'scale_{key}'][0])
                sb[q] = dict(stat=float(st), scale=float(scl))
            P['syst_budget'] = sb
            R['points'][f'{spin}_{m}'] = P
            print(spin, m, {k: round(v['lmax_median_bias'], 3) for k, v in bias.items()}, flush=True)
    # global (500 GeV) merging and shower envelopes, alps per point -> syst budget
    import json
    shp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results', 'shower.json')
    sh = json.load(open(shp)) if os.path.exists(shp) else {}
    s500 = R['points'].get('F_500', {}).get('syst_on_iv', {})
    merg = {q: max(abs(s500.get(f'V-MERGE-20_{q}', 0.0)), abs(s500.get(f'V-MERGE-50_{q}', 0.0))) for q in ('x', 'nosc')}
    vs = sh.get('vshower_m500', {})
    shw = {q: max([abs(vs[v]['rel_to_nominal'][{'x': 'x_median', 'nosc': 'nosc_median'}[q]]) for v in ('UP', 'DN') if v in vs] or [0.0])
           for q in ('x', 'nosc')}
    for pt, P in R['points'].items():
        al = sh.get('alps_and_scale9', {}).get(pt, {})
        for q in ('x', 'nosc'):
            k = {'x': 'x_median', 'nosc': 'nosc_median'}[q]
            a = max([abs(al[v]['rel_to_nominal'][k]) for v in ('alps0p5', 'alps2') if v in al] or [0.0])
            b = P['syst_budget'][q]
            b.update(merging=merg[q], shower=shw[q], alps=a)
            b['total'] = float(np.sqrt(sum(b[x] ** 2 for x in ('stat', 'scale', 'merging', 'shower', 'alps'))))
            b['note'] = 'merging and shower envelopes measured at E 500 GeV and applied to all points (ESTIMATE)'
    save('lmax_bias.json', R)
    # figure: median 2(gamma*-1) per model
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    keys = [('ip_fixedpt_MGLO_eta25', "(i') fixed pT, MG LO, |η|<2.5"), ('i_fixedpt_MGLO_vs_iv_noeta', '(i) fixed pT, MG LO, no η cut (both)'),
            ('ii_T2_Vjet', '(ii) T2 V*+jet'), ('iii_MG_LOPS', '(iii) MG LO+PS'), ('iv_MG_MLM_INC', 'MG MLM incl.')]
    for ax, spin in zip(axes, ('F', 'S')):
        for j, (k, lab) in enumerate(keys):
            xs, ys, es = [], [], []
            for m in (200, 500, 1000):
                p = R['points'].get(f'{spin}_{m}')
                if p and k in p['bias_vs_iv']:
                    xs.append(m * (1 + 0.02 * (j - 2))); ys.append(100 * p['bias_vs_iv'][k]['lmax_median_bias']); es.append(100 * p['bias_vs_iv'][k]['lmax_stat'])
            ax.errorbar(xs, ys, yerr=es, fmt='o', label=lab)
        ax.axhline(0, color='k', lw=0.6); ax.set_xlabel('m_Q [GeV]')
        ax.set_ylabel('median ℓ_max bias vs MG MLM (TRGS, pT(QQ̄)>200 GeV) [%]'); ax.set_title(f'{LABEL}  {"E" if spin == "F" else "Ẽ"}', loc='left', fontsize=9)
    axes[0].legend(fontsize=7); fig.tight_layout(); fig.savefig(os.path.join(FIG, 'lmax_bias.png'), dpi=120)


if __name__ == '__main__':
    main()
