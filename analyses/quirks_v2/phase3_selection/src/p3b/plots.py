"""Figures of the B2 development closure (p3-b, Casper).  Plotting only: reads outputs/p3b/b2_dev_closure.json.
Run with the analysis environment (mplhep):  .pixi/envs/default/bin/python plots.py
Label: "Private work (simulation)" (STUDY OVERRIDES); no experiment name."""
import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as mh  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'outputs'
FIG = OUT / 'figures'
log = logging.getLogger('plots')
LN15 = np.log(1.5)
CAP = LN15 / 3
RL = r'PU 200'


def label(ax):
    mh.label.exp_label(exp='', llabel='Private work (simulation)', data=True, rlabel=RL, loc=0, ax=ax)


def save(fig, name):
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / f'{name}.pdf', bbox_inches='tight', dpi=200, transparent=True)
    fig.savefig(FIG / f'{name}.png', bbox_inches='tight', dpi=200, transparent=True)
    plt.close(fig)
    log.info('figure %s', name)


def fig_lnr(R):
    names = ['R04', 'R05', 'R06', 'R07', 'R04x2S>=1', 'R04x2S>=2', 'R04x2S>=3', 'R05x2S>=1', 'R05x2S>=2', 'R05x2S>=3',
             'R06x2S>=1', 'R06x2S>=2', 'R06x2S>=3', 'R05xp>0.001', 'R05xp>0.01', 'R05xp>0.05', 'R06xp>0.001',
             'R06xp>0.01', 'R06xp>0.05']
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(10, 10))
    th = R.get('thinning', {}).get('closure', {}).get('rungs', {})
    y = [th.get(n, {}).get('ln_r') for n in names]
    e = [th.get(n, {}).get('sigma_tot') for n in names]
    m = np.array([v is not None for v in y])
    ax.errorbar(x[m] - 0.12, np.array(y, dtype=object)[m].astype(float), yerr=np.array(e, dtype=object)[m].astype(float),
                fmt='o', color='C0', label='repaired thinning (development)')
    oc = R.get('occupancy', {}).get('predictions', {})
    y2 = [oc.get(n, {}).get('const', {}).get('ln_r') for n in names]
    e2 = [oc.get(n, {}).get('const', {}).get('sigma_tot') for n in names]
    m2 = np.array([v is not None for v in y2])
    if m2.any():
        ax.errorbar(x[m2] + 0.12, np.array(y2, dtype=object)[m2].astype(float),
                    yerr=np.array(e2, dtype=object)[m2].astype(float), fmt='s', color='C1',
                    label='occupancy model (R04, R05 derivation; R06 held out)')
    for v, ls, lab in ((LN15, '--', r'$\pm\ln 1.5$ (tolerance)'), (CAP, ':', r'$\pm\ln 1.5/3$ (cap)')):
        ax.axhline(v, ls=ls, color='grey', label=lab)
        ax.axhline(-v, ls=ls, color='grey')
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([n.replace('x', r'$\otimes$').replace('>=', r'$\geq$') for n in names], rotation=90)
    ax.set_ylabel(r'$\ln r$ = ln(prediction / direct count)')
    ax.set_ylim(-1.2, 1.2)
    ax.legend(fontsize='x-small', loc='lower left')
    label(ax)
    save(fig, 'b2_dev_lnr')


def fig_rates(R, P):
    rungs = ['R04', 'R05', 'R06', 'R07', 'R08', 'R09']
    x = np.arange(len(rungs))
    fig, ax = plt.subplots(figsize=(10, 10))
    d = R['direct']
    yd = np.array([d['rate'][r] for r in rungs]); nd = np.array([d['counts'][r] for r in rungs])
    md = nd > 0
    ax.errorbar(x[md] - 0.15, yd[md], yerr=yd[md] / np.sqrt(nd[md]), fmt='o', color='k',
                label='direct count, C1 $\\rho = 1$ (16,000 trials)')
    if 'thinning' in R:
        t = R['thinning']
        yt = np.array([t['rate'][r] for r in rungs]); st = np.array([t['s_boot'][r] for r in rungs])
        mt = yt > 0
        ax.errorbar(x[mt] - 0.05, yt[mt], yerr=yt[mt] * st[mt], fmt='^', color='C0',
                    label='repaired thinning, C1 $\\rho = 2$ (2,000 trials, K = 64)')
    c = P['candidates']
    yo = np.array([c[r]['occupancy_day15']['rate_per_trial'] for r in rungs])
    wo = np.array([c[r]['width_s_tot']['measured_dev'] for r in rungs])
    ax.errorbar(x + 0.05, yo, yerr=[yo * (1 - np.exp(-wo)), yo * (np.exp(wo) - 1)], fmt='s', color='C1',
                label='occupancy model, day-15 scale (width $s_{tot}$, development bookkeeping)')
    yb = np.array([c[r]['occupancy_B2b_model']['rate_per_trial'] if c[r]['occupancy_B2b_model'] else np.nan
                   for r in rungs])
    mb = np.isfinite(yb)
    ax.plot(x[mb] + 0.15, yb[mb], 'D', color='C2', label='occupancy model, R04-R05 derivation (B2-b)')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(rungs)
    ax.set_ylabel('pile-up groups per trial')
    ax.set_ylim(1e-8, 1e5)
    ax.legend(fontsize='x-small', loc='upper right')
    label(ax)
    save(fig, 'b2_dev_rates')


def fig_neff(R):
    if 'thinning' not in R:
        return
    t = R['thinning']
    rungs = ['R04', 'R05', 'R06', 'R07', 'R08', 'R06x2S>=3', 'R07x2S>=3', 'R06xp>0.001', 'R05xp>0.001']
    x = np.arange(len(rungs))
    y = np.array([t['N_eff'][r] for r in rungs])
    fig, ax = plt.subplots(figsize=(10, 10))
    m = y > 0
    ax.plot(x[m], y[m], 'o', color='C0', label='$N_{eff} = 1/s_{boot}^2$, 1,000 $\\rho = 2$ events')
    ax.plot(x[m], 3 * y[m], 'o', mfc='none', color='C0', label='projected to 3,000 events ($\\times 3$)')
    ax.axhline(1 / CAP ** 2, ls='--', color='grey', label=r'$N_{eff}$ for $s_P = \ln 1.5/3$ alone')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels([r.replace('x', r'$\otimes$').replace('>=', r'$\geq$') for r in rungs], rotation=60)
    ax.set_ylabel('effective count of the thinning prediction')
    ax.legend(fontsize='x-small')
    label(ax)
    save(fig, 'b2_dev_neff')


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    R = json.loads((OUT / 'p3b' / 'b2_dev_closure.json').read_text())
    P = json.loads((OUT / 'p3b' / 'pileup_term.json').read_text())
    mh.style.use('CMS')
    fig_lnr(R)
    fig_rates(R, P)
    fig_neff(R)


if __name__ == '__main__':
    main()
