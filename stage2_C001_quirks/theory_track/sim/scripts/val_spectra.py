"""val_spectra.py -- VALIDATION §2: pT(QQ), gamma*, m(QQ), y spectra of the MG5_aMC+Pythia8 samples vs the old LO
cache (data/cache/T2_kinematics_cache.npz, code/T2_kinematics.py), with ratios.  Run: pixi run -e ana python
scripts/val_spectra.py.  Output: results/spectra.json, figures/spectra_{F,S}_m{m}_{incl,tail}.png.
Selections:
  incl : all events.  Old 'incl' (LO, pT = 0) vs E-LOPS (LO + Pythia ISR) vs E-INC (0-2j MLM).
  tail : pT(QQ) > 200 GeV and |y| < 3.5 (T2 generated y_V in [-3.5, 3.5], pT < 2500).  Old 'isr' (LO V*+jet) vs
         E-TRGS (MLM, ME cut 100 stitched with INC[pT_ME<100]), E-INC, E-LOPS.  A second view adds |eta_pair| < 2.5 (T2's table selection)."""
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from vlib import S, old, have, save, FIG, LABEL, boot_quant, hist_norm, neff

OBS = {'pt': ('p_T(QQ̄) [GeV]', None), 'g': ('γ* (each quirk, pair CM)', None), 'M': ('m(QQ̄) [GeV]', None),
       'y': ('y(QQ̄)', None)}


def bins_for(obs, m, sel):
    if obs == 'pt':
        return np.linspace(0, 600, 31) if sel == 'incl' else np.linspace(200, 1200, 26)
    if obs == 'g':
        return np.linspace(1, 3, 41)
    if obs == 'M':
        return np.linspace(2 * m, 2 * m + max(6 * m, 1500), 41)
    return np.linspace(-3.5, 3.5, 29)


def select(d, sel, eta25=False):
    if sel == 'incl':
        s = np.ones(len(d['w']), bool)
    else:
        s = (d['pt'] > 200) & (np.abs(d['y']) < 3.5) & (d['pt'] < 2500)
        if eta25:
            s &= np.abs(d['eta']) < 2.5
    return s


def summarize(d, s):
    w = d['w'] * s
    out = dict(neff=neff(w[w != 0]), n=int(np.sum(s & (d['w'] != 0))))
    for o in ('pt', 'g', 'M', 'y'):
        q, e = boot_quant(d[o][s], d['w'][s], nb=100)
        out[o] = dict(q16=q[0], q50=q[1], q84=q[2], err=e.tolist())
    q, e = boot_quant(d['g'][s] - 1, d['w'][s], nb=100)
    out['gm1'] = dict(q16=q[0], q50=q[1], q84=q[2], err=e.tolist())
    return out


def main():
    R = dict(note='weighted 16/50/84 quantiles with bootstrap errors (computed from weights; ESTIMATE as uncertainty); old cache = T2 LO generator '
                  '(arbitrary-unit weights, shapes only)', points={})
    for spin, pre in (('F', 'E'), ('S', 'S')):
        for m in (200, 500, 1000):
            if not have(f'{pre}-INC', m):
                continue
            new = {k: S(f'{pre}-{k}', m) for k in ('LOPS', 'INC', 'TRGS') if have(f'{pre}-{k}', m)}
            olds = {'incl': old(spin, m, 'incl'), 'isr': old(spin, m, 'isr')}
            P = {}
            for sel in ('incl', 'tail', 'tail_eta25'):
                base = 'incl' if sel == 'incl' else 'tail'
                e25 = sel == 'tail_eta25'
                o = olds['incl'] if base == 'incl' else olds['isr']
                P[sel] = {'old_T2': summarize(o, select(o, base, e25))}
                for k, d in new.items():
                    if base == 'incl' and k == 'TRGS':
                        continue
                    P[sel][f'MG_{k}'] = summarize(d, select(d, base, e25))
                # ratios of medians to old
                ref = P[sel]['old_T2']
                for k in list(P[sel]):
                    if k.startswith('MG_'):
                        P[sel][k]['median_ratio_to_old'] = {ob: P[sel][k][ob]['q50'] / ref[ob]['q50'] if ref[ob]['q50'] else None
                                                            for ob in ('g', 'M', 'gm1')}
                # figure
                fig, axes = plt.subplots(2, 4, figsize=(15, 6), sharex='col', gridspec_kw=dict(height_ratios=[3, 1]))
                for j, ob in enumerate(('pt', 'g', 'M', 'y')):
                    b = bins_for(ob, m, base)
                    c = 0.5 * (b[1:] + b[:-1])
                    so = select(o, base, e25)
                    ho, eo = hist_norm(o[ob][so], o['w'][so], b)
                    if not (base == 'incl' and ob == 'pt'):
                        axes[0, j].step(c, ho, where='mid', color='k', label='old T2 LO' + (' (pT=0)' if base == 'incl' else ' V*+jet'))
                    for k, col in (('LOPS', 'C0'), ('INC', 'C1'), ('TRGS', 'C3')):
                        if k not in new or (base == 'incl' and k == 'TRGS'):
                            continue
                        d = new[k]; sn = select(d, base, e25)
                        h, e = hist_norm(d[ob][sn], d['w'][sn], b)
                        axes[0, j].errorbar(c, h, yerr=e, fmt='.', ms=3, color=col, label={'LOPS': 'MG LO+PS', 'INC': 'MG MLM 0-2j', 'TRGS': 'MG MLM, stitched TRG'}[k])
                        if not (base == 'incl' and ob == 'pt'):
                            with np.errstate(divide='ignore', invalid='ignore'):
                                axes[1, j].errorbar(c, h / ho, yerr=e / ho, fmt='.', ms=3, color=col)
                    axes[1, j].axhline(1, color='k', lw=0.6); axes[1, j].set_ylim(0.5, 1.5)
                    axes[1, j].set_xlabel(OBS[ob][0]); axes[0, j].set_yscale('log' if ob in ('pt', 'M') else 'linear')
                axes[0, 0].legend(fontsize=7); axes[1, 0].set_ylabel('MG / old')
                axes[0, 0].set_title(f'{LABEL}  {"E" if spin == "F" else "Ẽ"}, m={m} GeV, {sel}', loc='left', fontsize=9)
                fig.tight_layout(); fig.savefig(os.path.join(FIG, f'spectra_{spin}_m{m}_{sel}.png'), dpi=110); plt.close(fig)
            R['points'][f'{spin}_{m}'] = P
            print('done', spin, m, flush=True)
    save('spectra.json', R)


if __name__ == '__main__':
    main()
