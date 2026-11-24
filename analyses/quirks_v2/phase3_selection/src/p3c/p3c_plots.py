"""p3c_plots.py -- figures of work package p3-c (plotting only; reads validation.json and p3c_results.json).

  <QV2 pixi python> p3c_plots.py <dir with validation.json, p3c_results.json> <figure dir>
"""
import json
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as mh  # noqa: E402
import numpy as np  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('p3c_plots')
mh.style.use('CMS')
EDGES = np.arange(0, 121, 6.0)


def label(ax):
    mh.label.exp_label(exp='', llabel='Private work (simulation)', rlabel='14 TeV', loc=0, data=True, ax=ax)


def save(fig, out, name):
    for ext in ('pdf', 'png'):
        fig.savefig(out / f'{name}.{ext}', bbox_inches='tight', dpi=200, transparent=True)
    plt.close(fig)
    log.info('wrote %s', out / name)


def fig_shape(val, out):
    rb = val['reading_RB']; ref = np.array(rb['nominal']['shape_figure'])
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    fig.subplots_adjust(hspace=0)
    x = 0.5 * (EDGES[1:] + EDGES[:-1])
    for key, lab in (('nominal', 'model, nominal (one Gaussian soft term)'),
                     ('remed_mixture_fig34', 'model, two-Gaussian soft term fitted to this figure'),
                     ('soft_dn_25', 'model, soft-term target 25 GeV')):
        m = np.array(rb[key]['shape_model'])
        mh.histplot(m, EDGES, ax=ax, label=lab)
        mh.histplot(m / ref, EDGES, ax=rax)
    ax.errorbar(x, ref, yerr=0.2 * ref, fmt='ko', label='public Phase-2 figure at pile-up 200 (read by eye, 20 %)')
    rax.errorbar(x, np.ones_like(x), yerr=0.2, fmt='ko')
    ax.set_yscale('log'); ax.set_ylabel('fraction of events per 6 GeV'); rax.set_ylabel('model / figure')
    rax.set_xlabel(r'$p_{T}^{miss}$ in $Z\to\mu\mu$ events [GeV]'); rax.set_ylim(0.3, 2.2); ax.set_xlim(0, 120)
    ax.legend(fontsize='x-small'); label(ax)
    save(fig, out, 'p3c_met_shape_zmm')


def fig_tt(val, out):
    ra = val['reading_RA']
    fig, ax = plt.subplots(figsize=(10, 10))
    for key, lab in (('nominal', 'model, nominal'), ('soft_up_32.5', 'model, soft-term target 32.5 GeV'),
                     ('remed_mixture_fig34', 'model, two-Gaussian soft term')):
        c = ra[key]['curve']
        ax.plot([p['mean_sumet'] for p in c], [p['rms'] for p in c], marker='o', label=lab)
    pts = ra['nominal']['points']
    ax.errorbar([p['sumet'] for p in pts], [p['figure'] for p in pts], yerr=0.5, fmt='ks',
                label='public figure of the other experiment, pile-up 200 (read by eye)')
    ax.set_xlabel(r'$\Sigma E_{T}$ [GeV]')
    ax.set_ylabel(r'RMS of $E_{x,y}^{miss}$(reco) $-$ $E_{x,y}^{miss}$(true) in $t\bar{t}$ [GeV]')
    ax.set_xlim(0, 4500); ax.set_ylim(25, 80); ax.legend(fontsize='x-small', loc='upper right'); label(ax)
    save(fig, out, 'p3c_met_rms_ttbar')


def fig_var(res, out):
    fig, ax = plt.subplots(figsize=(10, 10))
    procs = [(k, l) for k, l in (('ztt', r'$Z(\tau\tau)$'), ('zll', r'lost-lepton $Z(\ell\ell)$'), ('multijets', 'multijets'),
                                 ('znn', r'$Z(\nu\nu)$')) if k in res['n_trig']]
    vs = list(res['n_trig'][procs[0][0]]['ratio_to_nominal'])
    for i, (k, lab) in enumerate(procs):
        r = res['n_trig'][k]['ratio_to_nominal']
        ax.plot(np.arange(len(vs)) + 0.1 * (i - 1.5), [r[v] for v in vs], 'o', label=lab)
    ax.axhline(1.0, color='gray', linestyle='--')
    ax.set_xticks(np.arange(len(vs))); ax.set_xticklabels([v.replace('_', ' ') for v in vs], rotation=60, ha='right', fontsize='x-small')
    ax.set_yscale('log'); ax.set_ylabel(r'$N_{trig}$(variation) / $N_{trig}$(nominal)')
    ax.legend(fontsize='x-small'); label(ax)
    save(fig, out, 'p3c_ntrig_variations')


def fig_mj(res, out):
    S = res['samples']
    if 'mjw' not in S:
        return
    fig, ax = plt.subplots(figsize=(10, 10))
    e = np.array(S['mjw']['by_pthat']['edges'][:-1] + [3600.0])
    w = np.array(S['mjw']['by_pthat']['sigma_pb'])
    s = np.sum([np.array(S[k]['by_pthat']['sigma_pb']) for k in S if k.startswith('mjs') and k != 'mjs'], axis=0)
    mh.histplot(w, e, ax=ax, label=r'weighted sample ($\hat{p}_{T}^{5}$ bias)')
    mh.histplot(s, e, ax=ax, label=r'five unweighted $\hat{p}_{T}$ slices')
    ax.set_xlabel(r'$\hat{p}_{T}$ [GeV]'); ax.set_ylabel('multijet cross section after the preselection per bin [pb]')
    ax.set_yscale('log'); ax.set_xscale('log'); ax.set_xlim(100, 3600); ax.legend(fontsize='x-small'); label(ax)
    save(fig, out, 'p3c_multijet_pthat')


def main(argv):
    d = Path(argv[0]); out = Path(argv[1]); out.mkdir(parents=True, exist_ok=True)
    val = json.loads((d / 'validation.json').read_text())
    fig_shape(val, out); fig_tt(val, out)
    if (d / 'p3c_results.json').exists():
        res = json.loads((d / 'p3c_results.json').read_text())
        fig_var(res, out); fig_mj(res, out)


if __name__ == '__main__':
    main(sys.argv[1:])
