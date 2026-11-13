"""val_tune.py -- VALIDATION §5: CP5 (nominal) vs Monash, and MPI on vs off, on the observables that matter for the
quirk analysis: pT(QQ) (trigger / ISR tail), the recoil system (MET proxy: |pT(recoil, |eta|<5)|, its balance against
pT(QQ), leading-jet pT, jet multiplicity), gamma* and N_osc.  m_Q = 500 GeV fermion.
Run: pixi run -e ana python scripts/val_tune.py.  Output: results/tune.json, figures/tune_*.png."""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from vlib import S, have, save, FIG, LABEL, boot_quant, hist_norm


def summ(c):
    w = c['w']; ok = w != 0
    t = (c['pt'] > 200) & ok
    o = dict(sigma_fb=float(w.sum()), n=int(ok.sum()), f_pt200=float(w[t].sum() / w.sum()))
    for k, v, s in (('pt', c['pt'], ok), ('recoil5_pt', c['recoil5_pt'], ok), ('j1pt', c['j1pt'], ok),
                    ('gstar_tail', c['g'], t), ('nosc_tail', c['nosc'], t & (np.abs(c['eta']) < 2.5)),
                    ('recoil5_over_ptQQ_tail', c['recoil5_pt'] / np.maximum(c['pt'], 1e-9), t),
                    ('balance_pt', c['balance_pt'], ok)):
        q, e = boot_quant(v[s], w[s], nb=100)
        o[k] = dict(q16=q[0], q50=q[1], q84=q[2], err=e.tolist())
    o['njet_mean_tail'] = float(np.sum(c['njet'][t] * w[t]) / w[t].sum())
    o['njet_mean'] = float(np.sum(c['njet'][ok] * w[ok]) / w[ok].sum())
    # azimuthal alignment of the recoil (|eta|<5) with -pT(QQ): the MET direction the trigger sees
    P = c['p_qp'] + c['p_qm']
    phiQ = np.arctan2(P[:, 2], P[:, 1]); phiR = np.arctan2(c['recoil_eta5'][:, 2], c['recoil_eta5'][:, 1])
    dphi = np.abs((phiR - phiQ + np.pi) % (2 * np.pi) - np.pi)
    q, e = boot_quant(np.pi - dphi[t], w[t], nb=100)
    o['dphi_recoil_vs_minus_ptQQ_tail'] = dict(q50=q[1], q84=q[2], err=e.tolist())
    return o


def main():
    R = dict(note=__doc__, comparisons={})
    pairs = [('TRG_CP5_vs_Monash', 'E-TRG', 'V-TUNE-TRG'), ('INC_CP5_vs_Monash', 'E-INC', 'V-TUNE-INC'),
             ('TRG_MPIon_vs_off', 'E-TRG', 'V-MPI')]
    for lab, a, b in pairs:
        if not (have(a, 500) and have(b, 500)):
            continue
        A, B = summ(S(a, 500)), summ(S(b, 500))
        rel = {k: B[k]['q50'] / A[k]['q50'] - 1 for k in A if isinstance(A[k], dict) and A[k].get('q50')}
        rel.update(sigma=B['sigma_fb'] / A['sigma_fb'] - 1, f_pt200=B['f_pt200'] / A['f_pt200'] - 1,
                   njet_mean_tail=B['njet_mean_tail'] / A['njet_mean_tail'] - 1)
        R['comparisons'][lab] = dict(nominal=A, variation=B, rel_change_variation_over_nominal=rel)
        # figure
        fig, axes = plt.subplots(2, 3, figsize=(14, 6), sharex='col', gridspec_kw=dict(height_ratios=[3, 1]))
        ca, cb = S(a, 500), S(b, 500)
        for j, (key, bins, xl) in enumerate((('pt', np.linspace(0, 800, 33), 'p_T(QQ̄) [GeV]'),
                                             ('recoil5_pt', np.linspace(0, 800, 33), '|p_T(recoil, |η|<5)| [GeV]'),
                                             ('j1pt', np.linspace(0, 800, 33), 'leading jet p_T [GeV]'))):
            cx = 0.5 * (bins[1:] + bins[:-1])
            ha, ea = hist_norm(ca[key], ca['w'], bins); hb, eb = hist_norm(cb[key], cb['w'], bins)
            axes[0, j].errorbar(cx, ha, yerr=ea, fmt='.', label=a + (' (CP5, MPI on)'))
            axes[0, j].errorbar(cx, hb, yerr=eb, fmt='.', label=b)
            axes[0, j].set_yscale('log'); axes[0, j].legend(fontsize=7)
            with np.errstate(divide='ignore', invalid='ignore'):
                axes[1, j].errorbar(cx, hb / ha, yerr=hb / ha * np.hypot(ea / ha, eb / hb), fmt='.')
            axes[1, j].axhline(1, color='k', lw=0.6); axes[1, j].set_ylim(0.7, 1.3); axes[1, j].set_xlabel(xl)
        axes[0, 0].set_title(f'{LABEL}  E, m=500: {lab}', loc='left', fontsize=9); axes[1, 0].set_ylabel('variation / nominal')
        fig.tight_layout(); fig.savefig(os.path.join(FIG, f'tune_{lab}.png'), dpi=110); plt.close(fig)
        print(lab, {k: round(v, 3) for k, v in rel.items()}, flush=True)
    save('tune.json', R)


if __name__ == '__main__':
    main()
