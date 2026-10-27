"""make_u2_panel.py -- U-2 (a): measured B + multiple-scattering (MS) combination panel for P1 (truth level).

Stage-4 plan §9 (acts/stage4/plan.md); user decision U-2 (a) (LOG.md).  Executor, 2026-10-13.

What it does (read-only on the Stage-3 outputs; writes only into acts/stage4/u2_panel/):
  * Reads the Stage-3 P1 per-event table data/sim_stage3/summary/events_p1.npz (written by
    sim/stage3/scripts/extract.py) and the delivered sim/stage3/results/P1.json.
  * Per (species-mass, Lambda) cell, with the selection of sim/stage3/scripts/p1_results.py (status == 1, finite
    Delta_s > 0; Delta_s = ds_barrel_um, the plane thickness on the 10 virtual barrel layers), it recomputes:
      - median Delta_s_B, Delta_s_MS, Delta_s_BM (+- bootstrap, 1000 resamples, seed 12345 -- the p1_results.py recipe);
      - on the rows valid in all three configurations (same generated events, "shared rows"):
        r_q = Delta_s_BM / sqrt(Delta_s_B^2 + Delta_s_MS^2)   (ratio to quadrature),
        r_l = Delta_s_BM / (Delta_s_B + Delta_s_MS)           (ratio to the linear sum),
        x   = Delta_s_B / Delta_s_MS,
        q_l = (Delta_s_B + Delta_s_MS) / sqrt(Delta_s_B^2 + Delta_s_MS^2)  (what r_q would be for a linear sum);
        each as a median +- bootstrap error.
  * Checks that the recomputed medians/errors reproduce P1.json (Ds_B/Ds_MS/Ds_BM and B_MS_combination) and stores the
    maximum absolute difference in u2_panel.json (traceability).
  * Lambda_cross (B = MS crossover) is read from P1.json B_MS_crossover_keV (not recomputed).
Figures (fig/, PDF + PNG):
  u2_thickness_<point>.{pdf,png}   (5 files) main: Delta_s_B, Delta_s_MS, Delta_s_BM vs Lambda, with the quadrature and
                                   linear sum of the medians as references; ratio panel: per-event paired median r_q,
                                   the linear-sum expectation median(q_l), the line 1 (quadrature), Lambda_cross.
  u2_ratio_vs_x.{pdf,png}          r_q vs x (34 cells), reference 1 and the single-event linear-sum curve (1+x)/sqrt(1+x^2).
  u2_ratio_vs_lamcross.{pdf,png}   r_q vs Lambda/Lambda_cross (34 cells).
Numbers: u2_panel.json (every plotted number, with provenance).

Plotting: JFC rules (methodology/04-output.md).  Deviation, stated: mplhep is not installed in the theory_track env and
code/plotting.py does not exist (the Stage-3 helper sim/stage3/scripts/s3common.fig_label is a one-line ax.text label).
The CMS-like stylesheet is therefore set through rcParams here, and the label is drawn by exp_label() below, which
places text the way mplhep.label.exp_label(loc=0) does (above the axes, left and right).  The label is the user-approved
"Private work (simulation)" + "truth level" tag, right "sqrt(s) = 14 TeV, PU 200, 3 ab^-1"; no experiment name/logo.

Compute: < 1 CPU-min.  Run (from theory_track/):  pixi run python acts/stage4/u2_panel/make_u2_panel.py
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
TT = HERE.parents[2]
FIG = HERE / 'fig'
EVENTS = TT / 'data' / 'sim_stage3' / 'summary' / 'events_p1.npz'
P1JSON = TT / 'sim' / 'stage3' / 'results' / 'P1.json'
OUTJSON = HERE / 'u2_panel.json'

POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]   # as in p1_results.py
LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
NB = 1000
RNG_SEED = 12345                                                          # as in p1_results.py
# categorical colours (validated with the dataviz validator: CVD/normal-vision PASS; low contrast relieved by marker
# shapes, legends and the JSON table); fixed order = POINTS order
COL = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
MRK = ['o', 's', 'D', '^', 'v']
LLABEL = 'Private work (simulation)'
TAG = 'truth level'
RLABEL = r'$\sqrt{s}$ = 14 TeV, PU 200, 3 ab$^{-1}$'


# ---------------------------------------------------------------- statistics (identical recipe to p1_results.py)
def boot(fn, *arrs, nb=NB, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    n = len(arrs[0])
    if n < 3:
        return np.nan
    return float(np.std([fn(*[a[i] for a in arrs]) for i in (rng.integers(0, n, n) for _ in range(nb))]))


def med_err(x):
    x = x[np.isfinite(x)]
    return (float(np.median(x)), boot(np.median, x)) if len(x) else (np.nan, np.nan)


def plabel(spin, m):
    return (r'$\tilde{E}$' if spin == 'S' else 'E') + f' {m} GeV'


# ---------------------------------------------------------------- data
def compute():
    S = np.load(EVENTS)
    keys = list(S['point_keys'])
    P1 = json.load(open(P1JSON))

    def get(spin, m, lam, cfg):
        k = f'p1/{spin}_m{m}/L{lam:g}_{cfg}'
        if k not in keys:
            return None
        sel = S['point'] == keys.index(k)
        o = np.argsort(S['ev_index'][sel], kind='stable')
        d = {c: S[c][sel][o] for c in ('row', 'ds_barrel_um', 'status', 'floor_flag')}
        d['ok'] = (d['status'] == 1) & np.isfinite(d['ds_barrel_um']) & (d['ds_barrel_um'] > 0)
        return d

    out = dict(points={}, check_vs_P1json={}, lambda_cross_keV=P1['B_MS_crossover_keV'])
    dmax = dict(Ds_median_rel=0.0, Ds_err_rel=0.0, rq_median_abs=0.0, rq_err_abs=0.0, rl_median_abs=0.0)
    for spin, m in POINTS:
        pk = f'{spin}_m{m}'
        lc = P1['B_MS_crossover_keV'][pk]
        cells = {}
        for lam in LAMS:
            ref = P1['points'][pk]['by_lambda'][f'L{lam:g}']
            c = dict(lam_keV=lam, lam_over_cross=lam / lc)
            ds = {}
            for nm, cfg in (('B', 'B'), ('MS', 'M'), ('BM', 'BM')):
                d = get(spin, m, lam, cfg)
                if d is None:
                    continue
                ds[nm] = d
                med, err = med_err(d['ds_barrel_um'][d['ok']])
                c[f'Ds_{nm}'] = dict(median_um=med, err_um=err, n=int(d['ok'].sum()))
                rk = {'B': 'Ds_B', 'MS': 'Ds_MS', 'BM': 'Ds_BM'}[nm]
                rm = ref[rk]['median_raw_um' if nm == 'B' else 'median_um']
                re_ = ref[rk]['err_raw_um' if nm == 'B' else 'err_um']
                dmax['Ds_median_rel'] = max(dmax['Ds_median_rel'], abs(med / rm - 1))
                dmax['Ds_err_rel'] = max(dmax['Ds_err_rel'], abs(err / re_ - 1))
            if 'B' in ds:
                c['Ds_B']['f_floor_flag'] = float(np.mean(ds['B']['floor_flag']))
                c['Ds_B']['syst_unattributed_rel'] = 0.05 if lam > 5 else 0.0   # P-9, as in P1.json
                c['Ds_B']['withheld_floor_dominated_in_P1'] = bool(ref['Ds_B']['withheld_floor_dominated'])
            if 'B' in ds and 'MS' in ds:
                b, mm = c['Ds_B']['median_um'], c['Ds_MS']['median_um']
                eb, em = c['Ds_B']['err_um'], c['Ds_MS']['err_um']
                q = float(np.hypot(b, mm))
                c['quadrature_of_medians_um'] = dict(value=q, err=float(np.hypot(b * eb, mm * em) / q))
                c['linear_sum_of_medians_um'] = dict(value=b + mm, err=float(np.hypot(eb, em)))
            if all(k in ds for k in ('B', 'MS', 'BM')):
                mp = {k: dict(zip(ds[k]['row'][ds[k]['ok']].tolist(), ds[k]['ds_barrel_um'][ds[k]['ok']].tolist()))
                      for k in ds}
                rows = sorted(set(mp['B']) & set(mp['MS']) & set(mp['BM']))
                B_ = np.array([mp['B'][r] for r in rows]); M_ = np.array([mp['MS'][r] for r in rows])
                BM_ = np.array([mp['BM'][r] for r in rows])
                h = np.hypot(B_, M_)
                rq, erq = med_err(BM_ / h)
                rl, erl = med_err(BM_ / (B_ + M_))
                x, ex = med_err(B_ / M_)
                ql, eql = med_err((B_ + M_) / h)
                c['paired'] = dict(n=len(rows), ratio_to_quadrature=dict(median=rq, err=erq),
                                   ratio_to_linear=dict(median=rl, err=erl), x_B_over_MS=dict(median=x, err=ex),
                                   linear_sum_expectation_of_ratio=dict(median=ql, err=eql),
                                   pull_from_quadrature=(rq - 1) / erq)
                rc = ref['B_MS_combination']
                assert rc['n'] == len(rows)
                dmax['rq_median_abs'] = max(dmax['rq_median_abs'], abs(rq - rc['median_BM_over_quadrature']))
                dmax['rq_err_abs'] = max(dmax['rq_err_abs'], abs(erq - rc['err']))
                dmax['rl_median_abs'] = max(dmax['rl_median_abs'], abs(rl - rc['median_BM_over_linear']))
            cells[f'L{lam:g}'] = c
        out['points'][pk] = dict(label=plabel(spin, m).replace('$\\tilde{E}$', 'Etilde'), lambda_cross_keV=lc,
                                 by_lambda=cells)
    out['check_vs_P1json'] = dict(max_differences=dmax,
                                  note='recomputed from events_p1.npz with the p1_results.py selection and bootstrap; '
                                       'Ds_* relative, ratios absolute')
    return out


def summary(out):
    """Ranges quoted in U2_PANEL.md (all from the cells above; nothing fitted)."""
    cells = [(pk, c) for pk, v in out['points'].items() for c in v['by_lambda'].values() if 'paired' in c]
    def rng_(sel):
        v = [c['paired']['ratio_to_quadrature']['median'] for pk, c in cells if sel(c)]
        return dict(n_cells=len(v), min=min(v), max=max(v)) if v else None
    s = dict(n_cells=len(cells),
             by_lambda_band={'0.45 keV': rng_(lambda c: c['lam_keV'] == 0.45),
                             '0.6 keV': rng_(lambda c: c['lam_keV'] == 0.6),
                             '1-3 keV': rng_(lambda c: 1.0 <= c['lam_keV'] <= 3.0),
                             '5-10 keV': rng_(lambda c: c['lam_keV'] >= 5.0)},
             by_x_band={'x > 3 (B dominant)': rng_(lambda c: c['paired']['x_B_over_MS']['median'] > 3),
                        '1/3 <= x <= 3 (comparable)': rng_(lambda c: 1 / 3 <= c['paired']['x_B_over_MS']['median'] <= 3),
                        'x < 1/3 (MS dominant)': rng_(lambda c: c['paired']['x_B_over_MS']['median'] < 1 / 3)})
    mn = min(cells, key=lambda t: t[1]['paired']['ratio_to_quadrature']['median'])
    s['minimum_cell'] = dict(point=mn[0], lam_keV=mn[1]['lam_keV'], **mn[1]['paired']['ratio_to_quadrature'],
                             pull_from_quadrature=mn[1]['paired']['pull_from_quadrature'])
    s['cells_below_quadrature_gt_3sigma'] = [f"{pk}/L{c['lam_keV']:g}" for pk, c in cells
                                             if c['paired']['pull_from_quadrature'] < -3]
    s['cells_above_quadrature_gt_2sigma'] = [f"{pk}/L{c['lam_keV']:g}" for pk, c in cells
                                             if c['paired']['pull_from_quadrature'] > 2]
    s['ratio_to_linear_range'] = [min(c['paired']['ratio_to_linear']['median'] for _, c in cells),
                                  max(c['paired']['ratio_to_linear']['median'] for _, c in cells)]
    return s


# ---------------------------------------------------------------- plotting
def style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # CMS-like stylesheet (mplhep "CMS" is not available in this env): set globally, no per-call numeric font sizes
    plt.rcParams.update({
        'font.size': 26, 'axes.labelsize': 'medium', 'legend.fontsize': 'x-small', 'legend.frameon': False,
        'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True,
        'xtick.minor.visible': True, 'ytick.minor.visible': True,
        'xtick.major.size': 12, 'ytick.major.size': 12, 'xtick.minor.size': 6, 'ytick.minor.size': 6,
        'xtick.major.pad': 8, 'axes.linewidth': 1.5, 'lines.linewidth': 2.0, 'lines.markersize': 10,
        'errorbar.capsize': 0, 'axes.labelpad': 10, 'axes.formatter.useoffset': False, 'mathtext.default': 'regular',
        'font.family': 'sans-serif', 'font.sans-serif': ['TeX Gyre Heros', 'Helvetica', 'Arial', 'DejaVu Sans'],
    })
    return plt


def exp_label(ax):
    """mplhep.label.exp_label(loc=0)-like label: left "Private work (simulation)", right sqrt(s)/PU/lumi; no experiment name.
    (mplhep not installed in this env; this is the one place text is placed with ax.text.)"""
    ax.text(0.0, 1.005, LLABEL, transform=ax.transAxes, ha='left', va='bottom', fontweight='bold', fontsize='small')
    ax.text(1.0, 1.005, RLABEL, transform=ax.transAxes, ha='right', va='bottom', fontsize='small')


def add_tag(ax, lines, x=0.04, y=0.95):
    """mplhep.label.add_text-like in-axes tag (top-left): the 'truth level' tag and the sample."""
    ax.text(x, y, '\n'.join(lines), transform=ax.transAxes, ha='left', va='top', fontsize='x-small', fontstyle='italic')


def save(fig, name):
    for ext in ('pdf', 'png'):
        fig.savefig(FIG / f'{name}.{ext}', bbox_inches='tight', dpi=200, transparent=True)


def fig_thickness(plt, out, spin, m, ic):
    from matplotlib.ticker import FixedLocator, NullFormatter, FormatStrFormatter
    pk = f'{spin}_m{m}'
    V = out['points'][pk]
    cells = V['by_lambda']
    lc = V['lambda_cross_keV']
    fig, (ax, rx) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
    fig.subplots_adjust(hspace=0)
    L = np.array([c['lam_keV'] for c in cells.values()])

    def series(key, sub='median_um', esub='err_um'):
        sel = [k for k, c in cells.items() if key in c]
        lam = np.array([cells[k]['lam_keV'] for k in sel])
        y = np.array([cells[k][key][sub] for k in sel]); e = np.array([cells[k][key][esub] for k in sel])
        return lam, y, e

    lb, yb, eb = series('Ds_B')
    # B-only above 5 keV: +-5 % unattributed (P-9) added in quadrature to the statistical error
    eb_tot = np.hypot(eb, np.where(lb > 5, 0.05 * yb, 0.0))
    lm, ym, em = series('Ds_MS'); lbm, ybm, ebm = series('Ds_BM')
    lq, yq, eq = series('quadrature_of_medians_um', 'value', 'err')
    ll, yl, el = series('linear_sum_of_medians_um', 'value', 'err')
    ax.errorbar(lb, yb, yerr=eb_tot, fmt='o', color=COL[0], label=r'B only, $\Delta s_{B}$')
    ax.errorbar(lm, ym, yerr=em, fmt='s', color=COL[1], label=r'material only (MS), $\Delta s_{MS}$')
    ax.errorbar(lbm, ybm, yerr=ebm, fmt='D', color=COL[2], label=r'B + material, $\Delta s_{BM}$')
    ax.plot(lq, yq, '--', color='0.15', label=r'quadrature of medians, $\sqrt{\Delta s_B^2 + \Delta s_{MS}^2}$')
    ax.plot(ll, yl, ':', color='0.45', label=r'linear sum of medians, $\Delta s_B + \Delta s_{MS}$')
    ax.axvline(lc, ymin=0.27, ymax=0.58, color='0.6', lw=1.2, ls='-.', zorder=0)   # between the tag and the legend
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_ylabel(r'median plane thickness $\Delta s$ [$\mu$m]')
    allv = np.concatenate([yb, ym, ybm, yl])
    ax.set_ylim(0.3 * allv.min(), 40 * allv.max())
    ax.set_xlim(0.38, 12.0)
    ax.legend(loc='upper right', title=None)
    exp_label(ax)
    add_tag(ax, [TAG, plabel(spin, m) + r', $|\eta_{pair}| < 1$', rf'dash-dot: $\Lambda_{{cross}}$ = {lc:.2f} keV'],
            x=0.04, y=0.24)
    # ratio panel
    sel = [k for k, c in cells.items() if 'paired' in c]
    lr = np.array([cells[k]['lam_keV'] for k in sel])
    rq = np.array([cells[k]['paired']['ratio_to_quadrature']['median'] for k in sel])
    erq = np.array([cells[k]['paired']['ratio_to_quadrature']['err'] for k in sel])
    ql = np.array([cells[k]['paired']['linear_sum_expectation_of_ratio']['median'] for k in sel])
    rx.axhline(1.0, color='0.15', ls='--')
    rx.plot(lr, ql, ':', color='0.45')
    rx.errorbar(lr, rq, yerr=erq, fmt='D', color=COL[2])
    rx.axvline(lc, color='0.6', lw=1.2, ls='-.', zorder=0)
    rx.set_ylim(0.65, 1.55)
    rx.set_ylabel(r'$\frac{\Delta s_{BM}}{\sqrt{\Delta s_B^2+\Delta s_{MS}^2}}$')
    rx.set_xlabel(r'string tension scale $\Lambda$ [keV]')
    rx.xaxis.set_major_locator(FixedLocator([0.5, 1, 2, 3, 5, 10]))
    rx.xaxis.set_major_formatter(FormatStrFormatter('%g')); rx.xaxis.set_minor_formatter(NullFormatter())
    rx.set_yticks([0.8, 1.0, 1.2, 1.4])
    plt.setp(ax.get_xticklabels(), visible=False)
    name = f'u2_thickness_{pk}'
    save(fig, name); plt.close(fig)
    return name


def fig_ratio_vs(plt, out, mode):
    from matplotlib.ticker import FixedLocator, NullFormatter, FormatStrFormatter
    fig, ax = plt.subplots(figsize=(10, 10))
    if mode == 'x':
        xx = np.logspace(-2, 3, 400)
        ax.plot(xx, (1 + xx) / np.sqrt(1 + xx ** 2), ':', color='0.45',
                label=r'linear sum (single event), $(1+x)/\sqrt{1+x^2}$')
    ax.axhline(1.0, color='0.15', ls='--', label='quadrature')
    if mode == 'lc':
        ax.axvline(1.0, color='0.6', lw=1.2, ls='-.', zorder=0)
    for i, (spin, m) in enumerate(POINTS):
        V = out['points'][f'{spin}_m{m}']['by_lambda']
        cs = [c for c in V.values() if 'paired' in c]
        y = np.array([c['paired']['ratio_to_quadrature']['median'] for c in cs])
        ey = np.array([c['paired']['ratio_to_quadrature']['err'] for c in cs])
        if mode == 'x':
            x = np.array([c['paired']['x_B_over_MS']['median'] for c in cs])
            ex = np.array([c['paired']['x_B_over_MS']['err'] for c in cs])
            ax.errorbar(x, y, xerr=ex, yerr=ey, fmt=MRK[i], color=COL[i], label=plabel(spin, m))
        else:
            x = np.array([c['lam_over_cross'] for c in cs])
            ax.errorbar(x, y, yerr=ey, fmt=MRK[i] + '-', lw=1.0, color=COL[i], label=plabel(spin, m))
    ax.set_xscale('log')
    ax.set_ylabel(r'median $\Delta s_{BM}/\sqrt{\Delta s_B^2+\Delta s_{MS}^2}$ (per event)')
    if mode == 'x':
        ax.set_xlabel(r'median $x = \Delta s_B/\Delta s_{MS}$ (per event)')
        ax.set_xlim(0.02, 30); ax.set_ylim(0.6, 1.75)
        ax.xaxis.set_major_locator(FixedLocator([0.03, 0.1, 0.3, 1, 3, 10, 30]))
        ncol = 2
    else:
        ax.set_xlabel(r'$\Lambda/\Lambda_{cross}$  ($\Delta s_B = \Delta s_{MS}$ at $\Lambda_{cross}$)')
        ax.set_xlim(0.2, 12); ax.set_ylim(0.6, 1.45)
        ax.xaxis.set_major_locator(FixedLocator([0.3, 0.5, 1, 2, 3, 5, 10]))
        ncol = 2
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g')); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(loc='upper right', ncol=ncol)
    exp_label(ax)
    add_tag(ax, [TAG, r'P1, $|\eta_{pair}| < 1$, 34 cells'], x=0.04, y=0.08 if mode == 'x' else 0.08)
    name = 'u2_ratio_vs_x' if mode == 'x' else 'u2_ratio_vs_lamcross'
    save(fig, name); plt.close(fig)
    return name


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    out = compute()
    out['summary'] = summary(out)
    out['meta'] = dict(
        script='acts/stage4/u2_panel/make_u2_panel.py', truth_level=True,
        inputs=dict(events='data/sim_stage3/summary/events_p1.npz', p1='sim/stage3/results/P1.json',
                    lambda_cross='P1.json: B_MS_crossover_keV (log-log interpolation of median Ds_B = median Ds_MS)'),
        selection='p1_results.py: status == 1, finite ds_barrel_um > 0, per configuration; ratios on rows valid in B, M and BM',
        errors='bootstrap of the median, 1000 resamples, seed 12345 (statistical only); Ds_B above 5 keV: +-5 % '
               'unattributed (P-9) added in quadrature in the figures only',
        tags=dict(measured='VERIFIED (measured on the Stage-3 production, recomputed and matched to P1.json)',
                  quadrature_and_linear_of_medians='derived reference curves (combinations of measured medians), not a model',
                  single_event_linear_curve='algebraic identity (1+x)/sqrt(1+x^2), not a fit'),
        label=dict(left=LLABEL, tag=TAG, right='sqrt(s) = 14 TeV, PU 200, 3 ab^-1 (user-approved; PU is not simulated at truth level)'))
    names = [fig_thickness(plt_, out, s, m, i) for plt_ in [style()] for i, (s, m) in enumerate(POINTS)]
    plt = style()
    names += [fig_ratio_vs(plt, out, 'x'), fig_ratio_vs(plt, out, 'lc')]
    out['meta']['figures'] = [f'acts/stage4/u2_panel/fig/{n}.{{pdf,png}}' for n in names]
    json.dump(out, open(OUTJSON, 'w'), indent=1)
    print(json.dumps(out['check_vs_P1json'], indent=1))
    print(json.dumps(out['summary'], indent=1))


if __name__ == '__main__':
    main()
