"""Figures of the B2 development closure (p3-b, Casper; review-cycle-1 fixes by Ivar, 2026-11-24).
Plotting only: reads outputs/p3b/b2_dev_closure.json and outputs/p3b/pileup_term.json.
Run with the analysis environment (mplhep):  .pixi/envs/default/bin/python plots.py
Label: "Private work (simulation)" (STUDY OVERRIDES); no experiment name.
Cycle-1 fixes (Elias A/B items): x-axis labels; legends in empty regions; y range of the ln r figure widened so that the
R07 points and every error bar are inside the frame; open markers = not evaluable; error bars on both occupancy
readings; no-credit value drawn at R08-R09; rung notation in the tick labels kept short and defined in the captions."""
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


def ticklabel(n):
    return n.replace('x', r'$\otimes$').replace('>=', r'$\geq$')


def _points(ax, x, y, e, ev, fmt, color, lab):
    """filled markers for evaluable comparisons, open markers for not-evaluable ones (σ_tot > ln 1.5/3)."""
    for sel, mfc, suffix in ((ev, color, ''), (~ev, 'none', ', not evaluable')):
        if sel.any():
            ax.errorbar(x[sel], y[sel], yerr=e[sel], fmt=fmt, color=color, mfc=mfc, label=lab + suffix)


def fig_lnr(R):
    names = ['R04', 'R05', 'R06', 'R07', 'R04x2S>=1', 'R04x2S>=2', 'R04x2S>=3', 'R05x2S>=1', 'R05x2S>=2', 'R05x2S>=3',
             'R06x2S>=1', 'R06x2S>=2', 'R06x2S>=3', 'R05xp>0.001', 'R05xp>0.01', 'R05xp>0.05', 'R06xp>0.001',
             'R06xp>0.01', 'R06xp>0.05']
    x = np.arange(len(names), dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    lo, hi = -1.0, 1.2
    th = R.get('thinning', {}).get('closure', {}).get('rungs', {})
    oc = R.get('occupancy', {}).get('predictions', {})
    for src, get, dx, fmt, color, lab in (
            (th, lambda n: th.get(n), -0.12, 'o', 'C0', 'repaired thinning'),
            (oc, lambda n: (oc.get(n) or {}).get('const'), +0.12, 's', 'C1', 'occupancy model')):
        rows = [get(n) for n in names]
        m = np.array([r is not None and r.get('ln_r') is not None for r in rows])
        if not m.any():
            continue
        y = np.array([r['ln_r'] for r, k in zip(rows, m) if k])
        e = np.array([r['sigma_tot'] for r, k in zip(rows, m) if k])
        ev = np.array([bool(r['evaluable']) for r, k in zip(rows, m) if k])
        _points(ax, x[m] + dx, y, e, ev, fmt, color, lab)
        lo = min(lo, float(np.min(y - e)) - 0.1); hi = max(hi, float(np.max(y + e)) + 0.1)
    for v, ls, lab in ((LN15, '--', r'$\pm\ln 1.5$ (tolerance)'), (CAP, ':', r'$\pm\ln 1.5/3$ (cap)')):
        ax.axhline(v, ls=ls, color='grey', label=lab)
        ax.axhline(-v, ls=ls, color='grey')
    ax.axhline(0, color='k', lw=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([ticklabel(n) for n in names], rotation=90)
    ax.set_xlabel('Rung / crossing rung')
    ax.set_ylabel(r'$\ln r$ = ln(prediction / direct count)')
    ax.set_ylim(lo, hi + 0.35)
    ax.legend(fontsize='x-small', loc='lower left', ncol=2)
    label(ax)
    save(fig, 'b2_dev_lnr')


def fig_rates(R, P):
    rungs = ['R04', 'R05', 'R06', 'R07', 'R08', 'R09']
    x = np.arange(len(rungs), dtype=float)
    fig, ax = plt.subplots(figsize=(10, 10))
    d = R['direct']
    yd = np.array([d['rate'][r] for r in rungs]); nd = np.array([d['counts'][r] for r in rungs])
    md = nd > 0
    ax.errorbar(x[md] - 0.15, yd[md], yerr=yd[md] / np.sqrt(nd[md]), fmt='o', color='k',
                label=r'direct count ($\rho = 1$)')
    if 'thinning' in R:
        t = R['thinning']
        yt = np.array([t['rate'][r] for r in rungs]); st = np.array([t['s_boot'][r] for r in rungs])
        mt = yt > 0
        ax.errorbar(x[mt] - 0.05, yt[mt], yerr=yt[mt] * st[mt], fmt='^', color='C0',
                    label=r'repaired thinning ($\rho = 2$)')
    c = P['candidates']
    wo = np.array([c[r]['width_s_tot']['measured_dev'] for r in rungs])
    yo = np.array([c[r]['occupancy_day15']['rate_per_trial'] for r in rungs])
    ax.errorbar(x + 0.05, yo, yerr=[yo * (1 - np.exp(-wo)), yo * (np.exp(wo) - 1)], fmt='s', color='C1',
                label='occupancy model, reading (i)')
    yb = np.array([c[r]['occupancy_B2b_model']['rate_per_trial'] if c[r]['occupancy_B2b_model'] else np.nan
                   for r in rungs])
    mb = np.isfinite(yb)
    ax.errorbar(x[mb] + 0.15, yb[mb], yerr=[yb[mb] * (1 - np.exp(-wo[mb])), yb[mb] * (np.exp(wo[mb]) - 1)], fmt='D',
                color='C2', label='occupancy model, reading (ii)')
    nc = P['no_credit_value']['events_zero_count_68'] / P['N_trig_used']
    ax.hlines(nc, 3.6, 5.4, colors='C3', linestyles='--', label='no-credit value (96,000 trials)')
    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels(rungs)
    ax.set_xlabel('Rung')
    ax.set_ylabel('Pile-up groups per trial')
    ax.set_ylim(1e-11, 1e5)
    ax.legend(fontsize='x-small', loc='lower left')
    label(ax)
    save(fig, 'b2_dev_rates')


def fig_neff(R):
    if 'thinning' not in R:
        return
    t = R['thinning']
    rungs = ['R04', 'R05', 'R06', 'R07', 'R08', 'R06x2S>=3', 'R07x2S>=3', 'R05xp>0.001', 'R06xp>0.001']
    x = np.arange(len(rungs))
    y = np.array([t['N_eff'][r] for r in rungs])
    fig, ax = plt.subplots(figsize=(10, 10))
    m = y > 0
    ax.plot(x[m], y[m], 'o', color='C0', label=r'$N_{eff} = 1/s_{boot}^2$, 1,000 $\rho = 2$ events')
    ax.plot(x[m], 3 * y[m], 'o', mfc='none', color='C0', label=r'projected to 3,000 events ($\times 3$)')
    ax.axhline(1 / CAP ** 2, ls='--', color='grey', label=r'$N_{eff}$ at which $s_P = \ln 1.5/3$')
    ax.set_yscale('log')
    ax.set_ylim(1, 1e7)
    ax.set_xticks(x)
    ax.set_xticklabels([ticklabel(r) for r in rungs], rotation=60)
    ax.set_xlabel('Rung / crossing rung')
    ax.set_ylabel('Effective count of the thinning prediction')
    ax.legend(fontsize='x-small', loc='upper right')
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
