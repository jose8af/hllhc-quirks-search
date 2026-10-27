"""val_xsec.py -- VALIDATION §1: cross sections (Stage 2, E4).  Run: pixi run -e ana python scripts/val_xsec.py
Inputs: probe logs sim/probes/t3,t4,t12,t15,t16 (MG LO inclusive, mu = sqrt(s)); production samples *-LOPS, *-INC
(scale / PDF / NNPDF23LO weights); theory_signal_model §2.3 table (TH, transcribed below with its numbers).
Output: results/xsec.json, figures/xsec_*.png.  All sigma per N_IC = 1 unless the key says n_ic2."""
import os
import re

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from vlib import S, have, save, FIG, SIM, LABEL

PROBES = os.path.join(SIM, 'probes')
# research/theory_signal_model.md §2.3 (14 TeV column, N_IC = 2, LO_CT18 x K_WG(13.6 TeV)) and App. A raw LO
TH_M = [150, 200, 250, 300, 400, 500, 600, 700, 800, 1000, 1200]
TH_K136 = [1.101, 1.110, 1.118, 1.127, 1.142, 1.158, 1.175, 1.192, 1.211, 1.254, 1.292]   # 1200: 13 TeV value (TH note)
TH_E14 = [605, 220, 97.5, 49.0, 15.7, 6.11, 2.69, 1.29, 0.660, 0.197, 0.0656]
TH_S14 = [54.3, 19.2, 8.29, 4.06, 1.23, 0.458, 0.192, 0.0883, 0.0432, 0.0118, 0.00364]
TH_PDF = [3.3, 3.7, 4.2, 4.5, 5.5, 6.6, 7.9, 9.7, 11.9, 18.5, 25.0]                    # % (PDF4LHC21, WG scalar)
TH_SCALE_LO = {200: (+0.5, -0.8), 500: (+5.3, -4.9), 1000: (+9.1, -7.9)}               # % mu x1/2 / x2 at sqrt(s)
APPA_LO = {200: 99.1, 500: 2.636, 1000: 0.0785}                                        # fb, N_IC=1, alpha=1/127.9
T6 = {200: 219, 500: 5.94, 1000: 0.179}                                                # fb, N_IC=2 [T6 §2]
K_LIT_2404 = {200: 1.33, 1000: 1.45}                                                   # E, 13 TeV [2404.13814 Sec.3]
ALPHA_RESCALE = (132.50698 / 127.9) ** 2                                              # MG Gmu -> alpha(MZ)=1/127.9


def parse(logname):
    t = open(os.path.join(PROBES, logname)).read()
    out = []
    for blk in re.split(r'\nlaunch ', t)[1:]:
        name = re.search(r'-n (\S+)', blk).group(1)
        xs = re.search(r'Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb', blk)
        if xs:
            out.append((name, float(xs.group(1)) * 1e3, float(xs.group(2)) * 1e3))
    return out


def first_xs(logname):
    t = open(os.path.join(PROBES, logname)).read()
    xs = re.search(r'Cross-section :\s+([0-9.eE+-]+) \+- ([0-9.eE+-]+) pb', t)
    return float(xs.group(1)) * 1e3, float(xs.group(2)) * 1e3


def name_of(c, base):
    for n in c['wvar_names']:
        if n.startswith(base + '_MERGING='):
            return n
    raise KeyError(base)


def bands(c):
    """sigma (nominal), 9-point scale envelope (dyn -1), dyn-scale alternatives, CT18 Hessian (68 %), NNPDF23LO."""
    W = c['wvar']; nm = c['wvar_names']
    col = lambda n: W[:, nm.index(n)]
    s0 = c['w'].sum()
    sc = {}
    for muf in ('0.5', '1.0', '2.0'):
        for mur in ('0.5', '1.0', '2.0'):
            sc[f'muF{muf}_muR{mur}'] = col(name_of(c, f'MUF={muf}_MUR={mur}_PDF=14400')).sum()
    dyn = {d: col(name_of(c, f'DYN_SCALE={d}_MUF=1.0_MUR=1.0_PDF=14400')).sum() for d in (1, 2, 3, 4)}
    mem = np.array([col(name_of(c, f'MUF=1.0_MUR=1.0_PDF={14400 + k}')).sum() for k in range(1, 59)])
    dp = np.sqrt(np.sum(np.maximum.reduce([mem[0::2] - s0, mem[1::2] - s0, np.zeros(29)]) ** 2))
    dm = np.sqrt(np.sum(np.maximum.reduce([s0 - mem[0::2], s0 - mem[1::2], np.zeros(29)]) ** 2))
    # NNPDF23LO central: unmerged AUX_104 times the per-event merging factor (nominal / unmerged central AUX_45)
    a45, a104 = col('AUX_45'), col('AUX_104')
    fac = np.divide(c['w'], a45, out=np.zeros_like(a45), where=a45 != 0)
    s_nn = np.sum(a104 * fac)
    vals = np.array(list(sc.values()))
    return dict(sigma=s0, scale_up_pct=100 * (vals.max() / s0 - 1), scale_dn_pct=100 * (vals.min() / s0 - 1),
                scale_7pt_up_pct=100 * (max(v for k, v in sc.items() if not ('0.5' in k and '2.0' in k)) / s0 - 1),
                scale_7pt_dn_pct=100 * (min(v for k, v in sc.items() if not ('0.5' in k and '2.0' in k)) / s0 - 1),
                scale_points=sc, dyn=dyn, pdf_up90_pct=100 * dp / s0, pdf_dn90_pct=100 * dm / s0,
                pdf_up68_pct=100 * dp / s0 / 1.645, pdf_dn68_pct=100 * dm / s0 / 1.645,
                nnpdf23lo_over_ct18=s_nn / s0, mc_stat_pct=100 / np.sqrt(len(c['w'])))


def main():
    R = dict(tags='VERIFIED = measured here and cross-checked; ESTIMATE = derived (interpolation, extrapolation, '
                  'rescaling); UNVERIFIED = transcribed, not re-derived')
    # ---- 1.1 LO inclusive vs App. A (alpha rescaled)
    lo = {}
    for name, xs, dxs in parse('t4_xsec.log'):
        lo[name] = (xs, dxs)
    lo['E_m500'] = first_xs('t3_E_incl.log')
    rows = []
    for m in (200, 500, 1000):
        e = lo[f'E_m{m}']
        rows.append(dict(m=m, spin='F', mg_fb=e[0], mg_err=e[1], ref_fb=APPA_LO[m] / ALPHA_RESCALE,
                         ratio=e[0] / (APPA_LO[m] / ALPHA_RESCALE), tag='VERIFIED'))
    for m in (200, 500, 1000):
        s = lo[f'S_m{m}']
        k = TH_K136[TH_M.index(m)]
        ref = TH_S14[TH_M.index(m)] / (2 * k) / ALPHA_RESCALE
        rows.append(dict(m=m, spin='S', mg_fb=s[0], mg_err=s[1], ref_fb=ref, ratio=s[0] / ref, tag='VERIFIED'))
    R['lo_vs_appA'] = dict(note='MG inclusive pp->QQbar, CT18NLO, mu=sqrt(s), Gmu (alpha=1/132.507); reference = '
                                'App.A raw LO (F) or TH §2.3 14 TeV/(2K) (S), times (127.9/132.507)^2', rows=rows)
    # ---- 1.2 hand-written vs FeynRules
    p = parse('t12_xcheck.log')
    R['fr_vs_hw'] = dict(note='p = g u d s (no c, b), m = 500, identical EW inputs; order FR_E, FR_S, HW_E, HW_S',
                         sigma_fb=[(n, v, e) for n, v, e in p], ratio_E=p[0][1] / p[2][1], ratio_S=p[1][1] / p[3][1],
                         tag='VERIFIED')
    # ---- 1.3 EW scheme
    ew = {n: (v, e) for n, v, e in parse('t15_ewscheme.log')}
    ewr = []
    for m in (200, 500, 1000):
        base = lo[f'E_m{m}'][0]
        ewr.append(dict(m=m, gmu_fb=base, alphaMZ_sw2_0p2337_fb=ew[f'ew_a_m{m}'][0], alphaMZ_sw2_0p2222_fb=ew[f'ew_b_m{m}'][0],
                        ratio_a=ew[f'ew_a_m{m}'][0] / base, ratio_b=ew[f'ew_b_m{m}'][0] / base))
    R['ew_scheme'] = dict(note='(a) aEWM1=127.9 with Gf, MZ fixed (=> sw2=0.2337); (b) aEWM1=127.9 with Gf scaled so that '
                               'sw2=0.22225 (pure alpha rescale; expected (132.507/127.9)^2 = %.4f). Nominal MG = Gmu '
                               '(alpha=1/132.507, sw2=0.22225).' % ALPHA_RESCALE, rows=ewr, tag='VERIFIED')
    # ---- 1.4 normalisation table (TH §2.3) on the production grid
    grid = {}
    t16 = {n: (v, e) for n, v, e in parse('t16_lo_grid.log')} if os.path.exists(os.path.join(PROBES, 't16_lo_grid.log')) else {}
    for m in range(200, 1600, 100):
        if m <= 1200:
            K = float(np.interp(m, TH_M, TH_K136)); ktag = 'interpolated (TH §2.3, ESTIMATE between table masses)'
            k_unc = 0.0
        else:
            # slope between K(13.6 TeV, 1000) and K(13 TeV, 1200) (mixes two sqrt(s), C-2); the pure 13 TeV slope gives -0.5 % at
            # 1500 GeV -> assign +-2 % (linear vs quadratic / slope choice, ESTIMATE)
            K = TH_K136[-1] + (TH_K136[-1] - TH_K136[-2]) / 200 * (m - 1200); ktag = 'linear extrapolation of K beyond 1200 GeV (ESTIMATE, +-2 %)'
            k_unc = 2.0
        lo_m = t16.get(f'lo_m{m}', (np.nan, np.nan))
        sig_norm = 2 * K * lo_m[0]          # t16: aEWM1 = 127.9, Gf = 1.208403e-5 (sw2 = 0.22225) set explicitly = TH convention
        th = TH_E14[TH_M.index(m)] if m in TH_M else None
        pdf = float(np.interp(m, TH_M, TH_PDF)) if m <= 1200 else TH_PDF[-1]
        grid[m] = dict(lo_mg_alpha127p9_fb=lo_m[0], lo_err=lo_m[1], K=K, K_tag=ktag, K_unc_pct=k_unc, sigma_norm_nic2_fb=sig_norm,
                       th_table_nic2_fb=th, ratio_to_th=(sig_norm / th if th else None), pdf_unc_pct_th=pdf,
                       pdf_unc_note=('PDF4LHC21 (TH §2.3), interpolated' if m <= 1200 else
                                     'frozen at the 1200 GeV value: LOWER BOUND (C-2)'),
                       tag='ESTIMATE' if m not in TH_M else 'VERIFIED (LO two-code check; K transcribed from TH = UNVERIFIED)')
    R['normalisation_E'] = dict(note='sigma_norm = N_IC(2) x K_WG(13.6 TeV, TH §2.3) x sigma_LO(MG, CT18NLO, mu=sqrt(s), alpha=1/127.9, '
                                     'sw2=0.22225 = TH App. A convention; probe t16, param card verified in the run banner); use for event yields; LO-MLM gives shapes',
                                rows=grid)
    snorm = {}
    for m in (200, 500, 1000):
        snorm[m] = dict(sigma_norm_nic2_fb=TH_S14[TH_M.index(m)], source='TH §2.3 Etilde 14 TeV column (UNVERIFIED transcription, '
                        'LO part re-derived in lo_vs_appA)')
    R['normalisation_S'] = snorm
    # ---- 1.5 bands from the samples (LOPS = inclusive LO+PS; INC = matched)
    B = {}
    for spin, pre in (('F', 'E'), ('S', 'S')):
        for m in (200, 500, 1000):
            for kind in ('LOPS', 'INC'):
                id_ = f'{pre}-{kind}'
                if have(id_, m):
                    B[f'{spin}_{m}_{kind}'] = bands(S(id_, m))
    R['bands'] = dict(note='sample sigma (N_IC=1, LO, CT18NLO, dyn -1 = MG default; INC = MLM matched at qCut 45); scale = '
                           '9-point envelope (7-point excludes the (1/2,2) corners); PDF = CT18NLO Hessian (90 %CL, /1.645 '
                           'for 68 %); NNPDF23LO/CT18 = LO-PDF / NLO-PDF ratio', rows=B, tag='computed from weights; ESTIMATE as uncertainty (review S2-R2 C-1)')
    # ---- 1.6 comparisons
    cmp_ = {}
    for m in (200, 500, 1000):
        d = dict(TH_nic2=TH_E14[TH_M.index(m)], T6_nic2=T6[m], T6_over_TH=T6[m] / TH_E14[TH_M.index(m)])
        if f'F_{m}_LOPS' in B:
            b = B[f'F_{m}_LOPS']
            d['LOPS_dyn4_over_appA_rescaled'] = b['dyn'][4] / (APPA_LO[m] / ALPHA_RESCALE)
            d['NNPDF23LO_over_CT18'] = b['nnpdf23lo_over_ct18']
            if m in K_LIT_2404:
                k = TH_K136[TH_M.index(m)]
                d['K_lit_reconstructed'] = k / b['nnpdf23lo_over_ct18']
                d['K_2404_13TeV'] = K_LIT_2404[m]
                d['K_ratio'] = d['K_lit_reconstructed'] / K_LIT_2404[m]
            d['LOPS_scale_9pt_pct'] = (b['scale_up_pct'], b['scale_dn_pct'])
        if f'F_{m}_INC' in B and f'F_{m}_LOPS' in B:
            d['INC_over_LOPS_same_dyn'] = {k: B[f'F_{m}_INC']['dyn'][k] / B[f'F_{m}_LOPS']['dyn'][k] for k in (1, 2, 3, 4)}
            d['INC_over_LOPS_nominal'] = B[f'F_{m}_INC']['sigma'] / B[f'F_{m}_LOPS']['sigma']
        d['TH_LO_scale_pct_mu_sqrt_s'] = TH_SCALE_LO[m]
        cmp_[m] = d
    R['comparisons_E'] = cmp_
    # ---- 1.7 trigger-level yields on the grid: f(pT(QQ)>200) from the matched samples (shape), normalisation from 1.4
    Y = {}
    for m in range(200, 1600, 100):
        row = {}
        if have('E-INC', m):
            c = S('E-INC', m); w = c['w']
            row['f_pt200_INC'] = float(w[c['pt'] > 200].sum() / w.sum())
            row['f_pt200_eta25_INC'] = float(w[(c['pt'] > 200) & (np.abs(c['eta']) < 2.5)].sum() / w.sum())
            row['f_stat_INC'] = float(np.sqrt(np.sum(w[c['pt'] > 200] ** 2)) / w.sum())
            if have('E-TRGS', m):
                ct = S('E-TRGS', m)
                tt = ct['pt'] > 200; te = tt & (np.abs(ct['eta']) < 2.5)
                row['f_pt200_TRG_over_INC'] = float(ct['w'][tt].sum() / w.sum())
                row['f_pt200_eta25_TRG_over_INC'] = float(ct['w'][te].sum() / w.sum())
                # statistical error of f: TRGS numerator (Kish) and INC denominator (C-15)
                row['f_stat_TRGS'] = float(row['f_pt200_TRG_over_INC'] * np.hypot(np.sqrt(np.sum(ct['w'][tt] ** 2)) / ct['w'][tt].sum(),
                                                                                    np.sqrt(np.sum(w ** 2)) / w.sum()))
                row['n_tail_TRGS'] = int(np.sum(te & (ct['w'] != 0)))
                row['neff_tail_TRGS'] = float(ct['w'][te].sum() ** 2 / np.sum(ct['w'][te] ** 2))
        sn = grid[m]['sigma_norm_nic2_fb']
        f = row.get('f_pt200_TRG_over_INC', row.get('f_pt200_INC'))
        if f is not None:
            row['sigma_norm_pt200_nic2_fb'] = sn * f
            row['N_3iab_pt200'] = sn * f * 3000.0
            row['N_3iab_pt200_eta25'] = sn * row.get('f_pt200_eta25_TRG_over_INC', row.get('f_pt200_eta25_INC')) * 3000.0
            # B-4: MC effective statistics vs the expected 3 ab^-1 signal after a Knapen-like selection (eps = 0.28 x 0.65 = 0.18)
            row['N_3iab_pt200_eta25_eps018'] = 0.18 * row['N_3iab_pt200_eta25']
            if 'neff_tail_TRGS' in row:
                row['neff_over_N3iab_eps018'] = row['neff_tail_TRGS'] / row['N_3iab_pt200_eta25_eps018']
                row['neff_over_N3iab'] = row['neff_tail_TRGS'] / row['N_3iab_pt200_eta25']
        Y[m] = row
    R['trigger_yields_E'] = dict(note='f = sigma_matched(pT(QQ)>200 after shower)/sigma_matched(inclusive) at LO-MLM (CP5); '
                                      'TRGS (stitched) numerator (higher stat) over INC denominator; N = sigma_norm(N_IC=2) x f x 3 ab^-1 '
                                      '(ESTIMATE: LO shape x NNLL-K normalisation)', rows=Y)
    save('xsec.json', R)
    # ---- figure: normalisation table and LO
    ms = sorted(grid)
    fig, ax = plt.subplots(2, 1, figsize=(6.4, 6), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
    mi = [m for m in ms if m <= 1200]; me = [m for m in ms if m > 1200]
    ax[0].semilogy(mi, [grid[m]['sigma_norm_nic2_fb'] for m in mi], 'o-', label='LO(MG, CT18NLO) x K (TH §2.3), N_IC=2')
    ax[0].semilogy(me, [grid[m]['sigma_norm_nic2_fb'] for m in me], 'o', mfc='none', color='C0', label='same, K extrapolated (ESTIMATE)')
    ax[0].semilogy(TH_M, TH_E14, 's', mfc='none', label='TH §2.3 table (E, 14 TeV)')
    ax[0].semilogy(list(T6), list(T6.values()), '^', mfc='none', label='T6 (LO x K, NNPDF3.1 luxqed)')
    ax[0].set_ylabel('σ(pp → EĒ) [fb]'); ax[0].legend(fontsize=8); ax[0].set_title(LABEL, loc='left', fontsize=9)
    ax[1].plot([m for m in ms if grid[m]['ratio_to_th']], [grid[m]['ratio_to_th'] for m in ms if grid[m]['ratio_to_th']], 'o')
    ax[1].axhline(1, color='k', lw=0.6); ax[1].set_ylim(0.97, 1.03); ax[1].set_ylabel('ours / TH'); ax[1].set_xlabel('m_Q [GeV]')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'xsec_normalisation.png'), dpi=120)
    print('wrote results/xsec.json, figures/xsec_normalisation.png')


if __name__ == '__main__':
    main()
