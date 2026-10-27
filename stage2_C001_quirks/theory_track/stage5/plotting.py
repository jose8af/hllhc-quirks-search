"""stage5/plotting.py -- shared Stage-5 figure style and helpers (C001 quirks theory track).

Plain matplotlib (mplhep is NOT in the theory_track env; nothing is installed).  The style reproduces the JFC plotting
rules of methodology/04-output.md with rcParams: CMS-like sizes, figsize (10, 10) locked, ratio panels
height_ratios [3, 1] with sharex + hspace = 0, PDF + PNG at dpi 200 with bbox_inches='tight', transparent=True, no
set_title, no numeric fontsize, colorbars on an appended axis of the same height (make_square_add_cbar equivalent).

Label (user-approved 2026-10-13, LOG.md l.161): left "Private work (simulation)", right "sqrt(s) = 14 TeV, PU 200,
3 ab^-1"; no experiment name or logo anywhere.  Truth-level figures carry the "truth level" tag.  For truth-level
figures a right-label variant "sqrt(s) = 14 TeV" only is available through ONE flag (the sqrt-s-only rlabel); the
default is the approved full label because the user has not answered that option yet (LOG.md l.181).

Seeded from acts/stage4/u2_panel/make_u2_panel.py (style(), exp_label(), add_tag()); that script is not modified.

Stamps: any input whose label/flags say PLACEHOLDER, DEV, DRY RUN or preliminary propagates a stamp into the figure
(watermark + line under the label) and into the sidecar JSON written by save().  With FINAL = True (make_figures
--final) save() REFUSES any figure carrying a PLACEHOLDER / DEV / DRY RUN stamp: final figures are real-input only.

Lint note (jfc conventions/lint_plots.py): the raw matplotlib text calls below live only in the mplhep-equivalent helpers
exp_label / add_text / draw_stamps / map2d cell annotation (mplhep is not in the env); figure code never calls
ax.text directly.  The 'multiple exp_label() on a sharex figure' hit is the helper's definition + its single call per
main panel (label() is never applied to a ratio panel).
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
import matplotlib  # noqa: E402

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, LogNorm, Normalize, TwoSlopeNorm  # noqa: E402
from mpl_toolkits.axes_grid1 import make_axes_locatable  # noqa: E402

HERE = Path(__file__).resolve().parent
TT = HERE.parent

# ------------------------------------------------------------------------------------------------ label
LLABEL = 'Private work (simulation)'
TRUTH_TAG = 'truth level'
RLABELS = {'full': r'$\sqrt{s}$ = 14 TeV, PU 200, 3 ab$^{-1}$',      # approved (default everywhere)
           'sqrt_s': r'$\sqrt{s}$ = 14 TeV'}                          # truth-level variant, pending user answer
RLABEL_TEXT = {'full': 'sqrt(s) = 14 TeV, PU 200, 3 ab^-1', 'sqrt_s': 'sqrt(s) = 14 TeV'}

# ------------------------------------------------------------------------------------------------ colours
# categorical, fixed order (dataviz reference palette, validated: CVD/normal-vision PASS; contrast WARN on slots 3-5
# relieved by marker shapes + legends + the sidecar JSON tables)
PALETTE = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
MARKERS = ['o', 's', 'D', '^', 'v', 'P', 'X', '<']
INK = '#0b0b0b'
INK2 = '#52514e'
MUTED = '#898781'
# sequential (magnitude, e.g. efficiency): one hue, light -> dark (blue ramp 100..700)
SEQ = LinearSegmentedColormap.from_list('s5_seq', ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95',
                                                   '#0d366b'])
# diverging (polarity around 1, e.g. sigma_95 / sigma_th): blue <-> neutral grey <-> red
DIV = LinearSegmentedColormap.from_list('s5_div', ['#0d366b', '#3987e5', '#9ec5f4', '#f0efec', '#f4a3a2', '#e34948',
                                                   '#8f1f1f'])
# expected-limit bands (conventional green/yellow, taken from the categorical aqua/yellow hues, lightened)
for _cm in (SEQ, DIV):
    if _cm.name not in matplotlib.colormaps:
        matplotlib.colormaps.register(_cm)
BAND1 = '#7fd6b4'
BAND2 = '#f6d27a'

STAMP_COLOUR = '#e34948'
FINAL = False          # set by make_figures --final: save() refuses PLACEHOLDER / DEV / DRY RUN stamps
BIG_STAMPS = ('PLACEHOLDER', 'DEV', 'DRY')
STAMP_WATERMARK = '#f6c4c3'


def style():
    """Global rcParams (CMS-like; the U-2 panel values).  Call once per process (make_figures does)."""
    plt.rcParams.update({
        'font.size': 26, 'axes.labelsize': 'medium', 'legend.fontsize': 'small', 'legend.frameon': False,   # PAPER R2 B-4: x-small -> small (print legibility)
        'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True,
        'xtick.minor.visible': True, 'ytick.minor.visible': True,
        'xtick.major.size': 12, 'ytick.major.size': 12, 'xtick.minor.size': 6, 'ytick.minor.size': 6,
        'xtick.major.pad': 8, 'axes.linewidth': 1.5, 'lines.linewidth': 2.0, 'lines.markersize': 10,
        'errorbar.capsize': 0, 'axes.labelpad': 10, 'axes.formatter.useoffset': False, 'mathtext.default': 'regular',
        'font.family': 'sans-serif', 'font.sans-serif': ['TeX Gyre Heros', 'Helvetica', 'Arial', 'DejaVu Sans'],
        'axes.prop_cycle': matplotlib.cycler(color=PALETTE), 'image.cmap': 's5_seq',
        'pdf.fonttype': 42,
    })
    return plt


# ------------------------------------------------------------------------------------------------ figures
def figure(ratio=False):
    """(10, 10) figure; ratio=True -> (fig, (main, ratio)) with height_ratios [3, 1], sharex, hspace = 0."""
    if not ratio:
        fig, ax = plt.subplots(figsize=(10, 10))
        return fig, ax
    fig, (ax, rx) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw=dict(height_ratios=[3, 1]))
    fig.subplots_adjust(hspace=0)
    plt.setp(ax.get_xticklabels(), visible=False)
    return fig, (ax, rx)


def exp_label(ax, truth=False, rlabel='full', stamps=()):
    """mplhep.label.exp_label(loc=0)-like: left LLABEL (bold), right the sqrt(s)/PU/lumi label.  Main panel only.
    truth=True adds the 'truth level' tag in the axes (top left, via add_text); stamps add one line under the label."""
    if rlabel not in RLABELS:
        raise ValueError(f'rlabel must be one of {list(RLABELS)}')
    if rlabel != 'full' and not truth:
        raise ValueError("the 'sqrt_s' right label is only for truth-level figures")
    ax.text(0.0, 1.005, LLABEL, transform=ax.transAxes, ha='left', va='bottom', fontweight='bold', fontsize='small')
    # with a colorbar (map2d) the right label is right-aligned on the colorbar's outer edge (else it collides)
    # (append_axes gives the colorbar the same height as the main axes, so y = 1.005 is the same line)
    ax.text(1.0, 1.005, RLABELS[rlabel], transform=getattr(ax, '_s5_cax', ax).transAxes, ha='right', va='bottom',
            fontsize='small')
    ax._s5_label = dict(truth=truth, rlabel=rlabel)


def add_text(ax, lines, loc='upper left', x=None, y=None, box=False):
    """mplhep.label.add_text-like in-axes text block (italic, small).  loc in {'upper left', 'upper right',
    'lower left', 'lower right'} or explicit axes-fraction x, y."""
    if isinstance(lines, str):
        lines = [lines]
    pos = {'upper left': (0.04, 0.95, 'left', 'top'), 'upper right': (0.96, 0.95, 'right', 'top'),
           'lower left': (0.04, 0.05, 'left', 'bottom'), 'lower right': (0.96, 0.05, 'right', 'bottom')}[loc]
    xx = pos[0] if x is None else x
    yy = pos[1] if y is None else y
    bb = dict(boxstyle='round,pad=0.3', fc='white', ec='none', alpha=0.85) if box else None
    return ax.text(xx, yy, '\n'.join(lines), transform=ax.transAxes, ha=pos[2], va=pos[3], fontsize='small',  # PAPER R2 B-4
                   fontstyle='italic', zorder=20, bbox=bb)


def label(ax, truth=False, rlabel='full', tag_lines=(), stamps=(), loc='upper left', x=None, y=None, box=None):
    """Full labelling of one main panel: exp_label + (truth tag + tag_lines) block + visible stamps.
    On maps (map2d axes) the tag block goes below the x-axis title (every cell carries data); box=True draws it on
    a white box."""
    exp_label(ax, truth=truth, rlabel=rlabel)
    lines = ([TRUTH_TAG] if truth else []) + list(tag_lines)
    if lines and hasattr(ax, '_s5_cax') and x is None and y is None:
        add_text(ax, lines, loc='upper left', x=0.0, y=-0.15, box=False)   # maps: every cell is data -> tag below
    elif lines:
        add_text(ax, lines, loc=loc, x=x, y=y, box=bool(box))
    draw_stamps(ax, stamps)


def draw_stamps(ax, stamps):
    """PLACEHOLDER / DEV / DRY RUN watermark across the axes + a short line above the label."""
    st = [s for s in stamps if s]
    if not st:
        return
    big = [s for s in st if s.split()[0] in BIG_STAMPS]
    if big:
        ax.text(0.5, 0.5, '\n'.join(dict.fromkeys(s.split(' (')[0] for s in big)), transform=ax.transAxes,
                ha='center', va='center', rotation=30, fontsize='xx-large', fontweight='bold', color=STAMP_WATERMARK,
                zorder=1.5)       # solid light colour: above meshes/bands (z 1), below lines/markers (z 2) (alpha + transparent PNG renders unevenly)
    ax.text(0.0, 1.06, ' | '.join(st), transform=ax.transAxes, ha='left', va='bottom', fontsize='xx-small',
            color=STAMP_COLOUR, fontweight='bold')


def stamps_of(*objs):
    """Stamps propagated from input dicts (labels / flags / dev / placeholder keys)."""
    out = []
    for o in objs:
        if o is None:
            continue
        txt = ' '.join(str(o.get(k, '')) for k in ('label', '_placeholder')) if isinstance(o, dict) else str(o)
        if isinstance(o, dict) and (o.get('placeholder') or o.get('_placeholder')) or 'PLACEHOLDER' in txt:
            out.append('PLACEHOLDER (synthetic inputs, not a result)')
        if isinstance(o, dict) and o.get('dev') or 'DEV' in txt.split('|')[0]:
            out.append('DEV (not frozen / not a result)')
        if 'DRY RUN' in txt:
            out.append('DRY RUN (not a result)')
        if 'preliminary' in txt.lower():
            out.append('preliminary (C1 statistics)')
        if isinstance(o, dict) and any('INCOMPLETE' in str(f) or 'NOT VALID' in str(f) for f in o.get('flags', [])):
            out.append('B sum INCOMPLETE / limits NOT VALID (see flags)')
    return list(dict.fromkeys(out))


def legend(ax, **kw):
    kw.setdefault('loc', 'upper right')
    return ax.legend(**kw)


# ------------------------------------------------------------------------------------------------ helpers
def _edges(c, log):
    c = np.asarray(sorted(c), float)
    if len(c) == 1:
        return np.array([c[0] / 1.2, c[0] * 1.2]) if log else np.array([c[0] - 0.5, c[0] + 0.5])
    if log:
        lc = np.log(c)
        m = 0.5 * (lc[1:] + lc[:-1])
        return np.exp(np.concatenate([[lc[0] - (m[0] - lc[0])], m, [lc[-1] + (lc[-1] - m[-1])]]))
    m = 0.5 * (c[1:] + c[:-1])
    return np.concatenate([[c[0] - (m[0] - c[0])], m, [c[-1] + (c[-1] - m[-1])]])


def grid_from_points(xs, ys, zs):
    """Irregular (x, y, z) points -> (x centres, y centres, Z[ny, nx]) with NaN where a cell is absent."""
    ux = np.array(sorted(set(float(x) for x in xs)))
    uy = np.array(sorted(set(float(y) for y in ys)))
    Z = np.full((len(uy), len(ux)), np.nan)
    for x, y, z in zip(xs, ys, zs):
        Z[np.searchsorted(uy, y), np.searchsorted(ux, x)] = np.nan if z is None else z
    return ux, uy, Z


def add_cbar(fig, ax, mappable, label_):
    """Colorbar on an appended axis of the same height (mplhep make_square_add_cbar equivalent)."""
    cax = make_axes_locatable(ax).append_axes('right', size='5%', pad=0.15)
    cb = fig.colorbar(mappable, cax=cax)
    cb.set_label(label_)
    cax.minorticks_off()
    return cb


def map2d(fig, ax, x, y, Z, zlabel, xlog=False, ylog=True, zlog=False, vmin=None, vmax=None, cmap=None,
          center=None, contours=(), contour_styles=None, annotate=False, fmt='{:.2f}'):
    """(m_Q x Lambda) map: x = mass centres, y = Lambda centres, Z[ny, nx] (NaN = no point, left blank).
    Cell edges at the (geometric) midpoints.  contours: list of levels drawn on the cell-centre grid.
    center: value for a diverging norm (cmap defaults to DIV then).  annotate: print the value in each cell."""
    Zm = np.ma.masked_invalid(np.asarray(Z, float))
    if center is not None:
        cmap = cmap or DIV
        if zlog:
            norm = LogNorm(vmin=vmin, vmax=vmax)
            # symmetric in log around center
        else:
            norm = TwoSlopeNorm(vcenter=center, vmin=vmin, vmax=vmax)
    else:
        cmap = cmap or SEQ
        norm = LogNorm(vmin=vmin, vmax=vmax) if zlog else Normalize(vmin=vmin, vmax=vmax)
    pm = ax.pcolormesh(_edges(x, xlog), _edges(y, ylog), Zm, cmap=cmap, norm=norm, shading='flat',
                       edgecolors='face', linewidth=0)
    ax.set_xscale('log' if xlog else 'linear')
    ax.set_yscale('log' if ylog else 'linear')
    if contours and Zm.count() >= 4 and len(x) >= 2 and len(y) >= 2:
        sty = contour_styles or [dict(colors=INK, linestyles='-', linewidths=2.5)] * len(contours)
        for lev, s in zip(contours, sty):
            if np.nanmin(Z) < lev < np.nanmax(Z):
                ax.contour(np.asarray(x, float), np.asarray(y, float), np.ma.filled(Zm, np.nan), levels=[lev], **s)
    if annotate:
        fmtf = fmt if callable(fmt) else fmt.format
        for j, yy in enumerate(y):
            for i, xx in enumerate(x):
                if not np.ma.is_masked(Zm[j, i]):
                    v = Zm[j, i]
                    rgba = pm.cmap(pm.norm(v))
                    lum = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
                    ax.text(xx, yy, fmtf(v), ha='center', va='center', fontsize='x-small',   # PAPER R2 B-4
                            color='white' if lum < 0.5 else INK)
    cb = add_cbar(fig, ax, pm, zlabel)
    ax._s5_cax = cb.ax
    fmt_ = matplotlib.ticker.FormatStrFormatter('%g')
    for axis, c, lg in ((ax.xaxis, x, xlog), (ax.yaxis, y, ylog)):     # ticks at the grid centres, plain numbers
        if lg:
            axis.set_major_locator(matplotlib.ticker.FixedLocator(list(c)))
            axis.set_major_formatter(fmt_)
            axis.set_minor_locator(matplotlib.ticker.NullLocator())
    return pm, cb


def limit_plot(ax, x, median, band1=None, band2=None, theory=None, observed=None, median_alt=None,
               labels=None, xlog=False, ylog=True):
    """Expected limit with +-1 sigma / +-2 sigma bands and a theory curve.
    median: expected median (primary); band1 / band2: (lo, hi) arrays (None entries skipped); median_alt: a second
    median (e.g. the asymptotic cross-check) drawn dotted; theory: dict(x, y, lo, hi, label)."""
    lab = dict(median='Expected (median)', band1=r'Expected $\pm$1$\sigma$', band2=r'Expected $\pm$2$\sigma$',
               alt='Expected, asymptotic (cross-check)', obs='Observed')
    lab.update(labels or {})
    x = np.asarray(x, float)

    def ok(a):
        return a is not None and np.all([v is not None for v in a])
    if band2 is not None and ok(band2[0]) and ok(band2[1]):
        ax.fill_between(x, np.asarray(band2[0], float), np.asarray(band2[1], float), color=BAND2, lw=0,
                        label=lab['band2'])
    if band1 is not None and ok(band1[0]) and ok(band1[1]):
        ax.fill_between(x, np.asarray(band1[0], float), np.asarray(band1[1], float), color=BAND1, lw=0,
                        label=lab['band1'])
    ax.plot(x, np.asarray(median, float), '--', color=INK, lw=2.5, label=lab['median'])
    if median_alt is not None:
        ax.plot(x, np.asarray(median_alt, float), ':', color=INK2, lw=2.0, label=lab['alt'])
    if observed is not None:
        ax.plot(x, observed, '-', color=INK, marker='o', label=lab['obs'])
    if theory is not None:
        tx = np.asarray(theory['x'], float)
        ax.plot(tx, theory['y'], '-', color=PALETTE[7], lw=2.5, label=theory.get('label', 'Theory'))
        if theory.get('lo') is not None:
            ax.fill_between(tx, theory['lo'], theory['hi'], color=PALETTE[7], alpha=0.25, lw=0)
    ax.set_xscale('log' if xlog else 'linear')
    ax.set_yscale('log' if ylog else 'linear')


def log_ticks(axis, values):
    """Major ticks of a log axis at the given grid values, plain-number labels, no minor labels (no '2x10^0')."""
    axis.set_major_locator(matplotlib.ticker.FixedLocator(sorted(set(float(v) for v in values))))
    axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
    axis.set_minor_formatter(matplotlib.ticker.NullFormatter())


RUNG_TEX = {'IP2>=': r'$N_{IP2}\geq$', '2S2>=': r'$N_{2S2}\geq$', 'w<': r'$w_{core}<$', 'p>': r'$p(\chi^2_{core})>$',
            'h>': r'$h>$', 'o>': r'$o>$', 'e>': r'$dE/dx>$'}


def rung_label(name, short=True):
    """'R04_IP2>=7' -> 'R04  N_IP2 >= 7' (math, no bare underscore).  short=True -> rung number + cut."""
    head, _, cut = str(name).partition('_')
    cut = cut.split(' ')[0]
    for k, v in RUNG_TEX.items():
        if cut.startswith(k):
            return f'{head} {v}{cut[len(k):]}' if not short else f'{v}{cut[len(k):]}'
    return str(name).replace('_', ' ')


def eff_vs_rung(ax, rung_names, series, ylog=False, ylabel='signal efficiency', families=None):
    """Efficiency (or any per-rung quantity) vs ladder rung.  series: list of dict(label, y, lo, hi[, color,
    marker]); lo/hi are absolute interval edges (e.g. CP 68 %).  Rung tick labels rotated, human readable.
    On a log axis, y = 0 entries are not drawn (marker and error bar), the caller states it in the tag."""
    xs = np.arange(1, len(rung_names) + 1)
    for i, s in enumerate(series):
        y = np.array([np.nan if v is None else v for v in s['y']], float)
        if ylog:
            y[y <= 0] = np.nan
        yerr = None
        if s.get('lo') is not None:
            lo = np.array([np.nan if v is None else v for v in s['lo']], float)
            hi = np.array([np.nan if v is None else v for v in s['hi']], float)
            yerr = np.vstack([np.clip(y - lo, 0, None), np.clip(hi - y, 0, None)])
        ax.errorbar(xs, y, yerr=yerr, fmt=s.get('marker', MARKERS[i % 8]) + s.get('ls', '-'), lw=1.2,
                    color=s.get('color', PALETTE[i % 8]), label=s['label'], ms=8)
    ax.set_xticks(xs)
    ax.set_xticklabels([rung_label(n, short=False) for n in rung_names], rotation=90, fontsize='x-small')  # R-number + cut (PAPER R2 B-4)
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlim(0.3, len(rung_names) + 0.7)
    if ylog:
        ax.set_yscale('log')
    ax.set_ylabel(ylabel)
    ax.set_xlabel('selection ladder rung (cumulative)')
    if families:
        for xb in families:
            ax.axvline(xb + 0.5, color=MUTED, lw=0.8, ls=':', zorder=0)


def hist_errorbar(ax, edges, counts, label, color, density=True):
    """Histogram with sqrt(N) errors from raw counts (plain-matplotlib histplot equivalent: stairs + error bars).
    density=True -> unit area, errors scaled identically (derived quantity: explicit yerr); density='fraction' ->
    fraction of entries per bin, error sqrt(n)/N."""
    counts = np.asarray(counts, float)
    edges = np.asarray(edges, float)
    err = np.sqrt(counts)
    if density == 'fraction' and counts.sum() > 0:
        n = counts.sum()
        counts, err = counts / n, err / n
    elif density and counts.sum() > 0:
        w = np.diff(edges) * counts.sum()
        counts, err = counts / w, err / w
    ax.stairs(counts, edges, color=color, lw=2.0, label=label)
    c = 0.5 * (edges[1:] + edges[:-1])
    ax.errorbar(c, counts, yerr=err, fmt='none', ecolor=color, lw=1.2)


# ------------------------------------------------------------------------------------------------ save
def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _rel(p):
    p = Path(p).resolve()
    try:
        return str(p.relative_to(TT))
    except ValueError:
        return str(p)


def save(fig, outdir, name, inputs=(), stamps=(), meta=None, code=()):
    """Write <outdir>/<name>.pdf, .png (dpi 200, tight, transparent) and <name>.json (provenance sidecar):
    sha256 of every input file and of the code (this module + `code`), stamps, label variant, meta.  Closes fig."""
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    bad = [s for s in stamps if s and s.split()[0] in BIG_STAMPS]
    if FINAL and bad:
        plt.close(fig)
        raise RuntimeError(f'REFUSED (final figures, real inputs only): {name} carries stamp(s) {bad}')
    fig.savefig(outdir / f'{name}.pdf', bbox_inches='tight', dpi=200, transparent=True)
    fig.savefig(outdir / f'{name}.png', bbox_inches='tight', dpi=200, transparent=True)
    lab = {}
    for ax in fig.axes:
        if hasattr(ax, '_s5_label'):
            lab = dict(ax._s5_label)
            break
    side = dict(figure=name, files=[f'{name}.pdf', f'{name}.png'],
                created=_dt.datetime.now().isoformat(timespec='seconds'),
                stamps=list(dict.fromkeys(stamps)),
                label=dict(left=LLABEL, right=RLABEL_TEXT.get(lab.get('rlabel', 'full')),
                           truth_level_tag=bool(lab.get('truth')), experiment_name_or_logo=False),
                inputs={_rel(p): sha256(p) for p in inputs if Path(p).exists()},
                inputs_missing=[_rel(p) for p in inputs if not Path(p).exists()],
                code_sha256={_rel(p): sha256(p) for p in [Path(__file__), *code]},
                env=dict(python=sys.version.split()[0], matplotlib=matplotlib.__version__, numpy=np.__version__,
                         nice=os.nice(0) if hasattr(os, 'nice') else None),
                meta=meta or {})
    (outdir / f'{name}.json').write_text(json.dumps(side, indent=1, default=str))
    plt.close(fig)
    return side
