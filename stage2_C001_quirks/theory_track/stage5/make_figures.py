"""stage5/make_figures.py -- the Stage-5 figure set (C001 quirks theory track), from Stage-4 outputs read per
acts/stage4/analysis/inputs/schema.json (v1), plus the truth-level figures (U-2 panel, Stage-3 truth edges).

    # detector level, from a Stage-4 results directory (run_all --out ...), or the synthetic placeholders:
    nice -n 15 pixi run python stage5/make_figures.py --results stage5/placeholder_inputs
    nice -n 15 pixi run python stage5/make_figures.py --results data/acts_stage4/analysis/<tag> [--proposed DIR]
    # truth level (real, approved inputs): U-2 panel from acts/stage4/u2_panel/u2_panel.json + P2 truth edges
    nice -n 15 pixi run python stage5/make_figures.py --truth [--truth-rlabel full|sqrt_s]
    # FINAL set (real inputs only; refuses placeholder / DEV / dry-run inputs): detector figures into
    # stage5/figures/final/, truth figures into final/truth/ (full right label) and final/truth_sqrt_s/
    nice -n 15 pixi run python stage5/make_figures.py --final --results data/acts_stage4/analysis/C12FC_v1 --truth
    nice -n 15 pixi run python stage5/make_figures.py --final --truth --truth-rlabel sqrt_s

Outputs: stage5/figures/<tag>/<id>.{pdf,png,json} (+ index.json with the status of every figure id).  <tag> =
'placeholder' when the inputs are PLACEHOLDER, 'truth' for --truth, 'final' for --final, else the results directory
name.  Read-only on every input; never writes under acts/stage4/ or data/acts_stage4/.  A figure whose input is missing
or fails the schema check is SKIPPED with its reason in index.json (never silently).
The schema-v2 extension files (acceptance, edges_det, sep_it_det, event_display) are read from --proposed if given,
else from <results>/proposed/ if that directory exists (placeholder layout), else from the results directory itself
(the real run_all layout, e.g. C12FC_v1).  The Stage-4 outcome (WP status, fallback branch, best limit, N_exp per
point, truth merged-surface fractions) is read from <results>/../STAGE4_SUMMARY.json when its primary_run.dir is the
results directory (else those annotations are omitted and the reason is logged in index.json).  The D7 existing-limit
overlay reads stage5/external_bounds.json (schema 'external_bounds v1', stage5/EXTERNAL_BOUNDS.md).
"""
import argparse
import json
import sys
import traceback
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TT = HERE.parent
sys.path.insert(0, str(HERE))
import plotting as P  # noqa: E402

SCHEMA = TT / 'acts' / 'stage4' / 'analysis' / 'inputs' / 'schema.json'
XSEC = TT / 'sim' / 'results' / 'xsec.json'
P2 = TT / 'sim' / 'stage3' / 'results' / 'P2.json'
U2 = TT / 'acts' / 'stage4' / 'u2_panel' / 'u2_panel.json'
EXT = HERE / 'external_bounds.json'     # Stage-5 own input (FASER / D0 / Farina-Low; build_external_bounds.py)
LUMI_FB = 3000.0
REPORT = ['R_A', 'R_B', 'R_C', 'R_D', 'R_E']
REPORT_TXT = {'R_A': r'$R_A$: end of F0 counting ($N_{IP2}\geq 7$)', 'R_B': r'$R_B$: $R_A$ + $w_{core}<18.75$ mm',
              'R_C': r'$R_C$: $R_A$ + $w_{core}<4.7$ mm', 'R_D': r'$R_D$: full F0 ladder',
              'R_E': r'$R_E$: tightest rung (full F1)'}
FALLBACK_TXT = r'no WP: fallback selection $r_{fb}$ per point'      # PAPER R2 B-4: shorter, no internal section ids
NPZ_ALIASES = {'file': ('file', 'src_file')}      # schema v1 name -> accepted array names (run_all writes src_file)
INV = TT / 'data' / 'acts_stage4' / 'investigation'   # read-only (truth_degeneracy_*.json fallback for D9)
SPIN_TXT = {'F': 'E', 'S': r'$\tilde{E}$'}
SPIN_LONG = {'F': r'E = (1,1)$_{-1}$ fermion', 'S': r'$\tilde{E}$ scalar'}
CODE = [Path(__file__)]


class Skip(Exception):
    pass


def plabel(spin, m):
    return f'{SPIN_TXT[spin]} {int(m)} GeV'


def lam_txt(lam):
    return rf'$\Lambda$ = {lam:g} keV'


# ================================================================================================ inputs
class Inputs:
    def __init__(self, results, proposed=None):
        self.dir = Path(results)
        if proposed:
            self.prop = Path(proposed)
        elif (self.dir / 'proposed').is_dir():
            self.prop = self.dir / 'proposed'           # placeholder layout
        else:
            self.prop = self.dir                        # real run_all layout: extension files at the top level
        self.schema = json.loads(SCHEMA.read_text())
        self._c = {}
        self.summary, self.summary_note = self._summary()

    def _summary(self):
        """STAGE4_SUMMARY.json next to the run dir, used only if it describes THIS run (primary_run.dir)."""
        p = self.dir.parent / 'STAGE4_SUMMARY.json'
        if not p.exists():
            return None, f'no {p.name} next to the results dir'
        d = json.loads(p.read_text())
        rd = Path(d.get('primary_run', {}).get('dir', ''))
        rd = rd if rd.is_absolute() else TT / rd
        if rd.resolve() != self.dir.resolve():
            return None, f'{p.name} primary_run.dir = {rd} is not the results dir; summary not used'
        self.summary_path = p
        return d, f'{_rel_tt(p)} (schema {d.get("schema")}) used'

    def outcome(self):
        """WP status from bsum_wp.json -> rule (authoritative) + headline numbers from STAGE4_SUMMARY.json."""
        bw = self.json('bsum_wp.json') or {}
        wp = (bw.get('rule') or {}).get('wp') or {}
        o = dict(wp_T=wp.get('T'), wp_G=wp.get('G'), branch=wp.get('branch') or (bw.get('rule') or {}).get('branch'))
        o['fallback'] = o['wp_T'] is None and o['wp_G'] is None
        if self.summary:
            so = self.summary.get('outcome', {})
            o.update(best=so.get('best_mu95_over_Nexp'), n_points=so.get('n_points'),
                     n_with_limit=so.get('n_points_with_limit'), n_eps0=so.get('n_points_eps0_both_bins'),
                     ladder=self.summary.get('ladder'))
            if (so.get('wp_T'), so.get('wp_G')) != (o['wp_T'], o['wp_G']):
                raise RuntimeError('STAGE4_SUMMARY outcome WP != bsum_wp.json rule WP')
        return o

    def fallback_point(self, key):
        return ((self.summary or {}).get('fallback_points') or {}).get(key)

    def path(self, name, proposed=False):
        return (self.prop if proposed else self.dir) / name

    def json(self, name, proposed=False):
        k = ('p:' if proposed else '') + name
        if k not in self._c:
            p = self.path(name, proposed)
            self._c[k] = json.loads(p.read_text()) if p.exists() else None
        return self._c[k]

    def npz(self, name, proposed=False):
        p = self.path(name, proposed)
        return np.load(p, allow_pickle=False) if p.exists() else None

    def need(self, name, proposed=False):
        d = self.json(name, proposed) if name.endswith('.json') else self.npz(name, proposed)
        if d is None:
            raise Skip(f'input missing: {self.path(name, proposed)}' + (' (proposed extension, NOT in schema v1)'
                                                                         if proposed else ''))
        return d

    def check(self):
        """Deep schema check of what make_figures reads (run_all.validate_outputs checks only top-level keys)."""
        issues = []
        F = self.schema['files']
        for f, spec in F.items():
            if '<' in f or not f.endswith('.json'):
                continue
            d = self.json(f)
            if d is None:
                issues.append(f'{f}: absent')
                continue
            issues += [f'{f}: missing {k}' for k in spec.get('required', {}) if k not in d]
        se = self.json('signal_eff.json')
        if se:
            preq = list(F['signal_eff.json']['point'])
            for kind in ('a1', 'a2', 'a5'):
                if kind not in se:
                    issues.append(f'signal_eff.json: kind {kind} absent')
                    continue
                for k in F['signal_eff.json']['per_kind']['a1|a2|a5']:
                    if k not in se[kind]:
                        issues.append(f'signal_eff.json/{kind}: missing {k}')
                for key, t in list(se[kind].get('points', {}).items())[:3]:
                    issues += [f'signal_eff.json/{kind}/{key}: missing {k}' for k in preq if k not in t]
        bw = self.json('bsum_wp.json')
        if bw:
            for c in ('T', 'G'):
                for r in bw['ladder'].get(c, [])[:1]:
                    issues += [f'bsum_wp.json/ladder/{c}: missing {k}' for k in F['bsum_wp.json']['rung'] if k not in r]
        z = self.npz('signal_obs_a2.npz')
        if z is not None:
            want = [a.split()[0] for a in F['signal_obs_<kind>.npz']['arrays']]
            issues += [f'signal_obs_a2.npz: missing array {a}' for a in want
                       if not any(n in z.files for n in NPZ_ALIASES.get(a, (a,)))]
        return issues


def _rel_tt(p):
    try:
        return str(Path(p).resolve().relative_to(TT))
    except ValueError:
        return str(p)


def stamps(I, *names):
    objs = [I.json('manifest.json')] + [I.json(n) for n in names if n.endswith('.json')]
    return P.stamps_of(*objs)


def a2_points(I):
    se = I.need('signal_eff.json')
    if 'a2' not in se:
        raise Skip('signal_eff.json has no a2 (A2 templates)')
    return se['a2']['points']


def by_mass(pts, spin):
    out = {}
    for key, t in pts.items():
        if t['spin'] == spin:
            out.setdefault(float(t['m']), []).append((float(t['lam']), key, t))
    return {m: sorted(v) for m, v in sorted(out.items())}


def sel_lams(lams, n=8):
    lams = sorted(set(lams))
    if len(lams) <= n:
        return lams
    idx = np.unique(np.round(np.linspace(0, len(lams) - 1, n)).astype(int))
    return [lams[i] for i in idx]


def theory_E():
    """sigma_norm (N_IC = 2) for E from sim/results/xsec.json, with the PDF uncertainty (TH §2.3) as band."""
    d = json.loads(XSEC.read_text())['normalisation_E']['rows']
    m = np.array(sorted(float(k) for k in d))
    y = np.array([d[f'{int(x)}']['sigma_norm_nic2_fb'] for x in m])
    u = np.array([(d[f'{int(x)}'].get('pdf_unc_pct_th') or 0.0) / 100 for x in m])
    return dict(x=m, y=y, lo=y * (1 - u), hi=y * (1 + u), label=r'$\sigma_{th}$ (E, $N_{IC}$ = 2, $K_{QCD}$, PDF unc.)')   # PAPER R3 C-3: K is NNLO_approx+NNLL, not NLO


def theory_S():
    d = json.loads(XSEC.read_text())['normalisation_S']
    return {float(k): v['sigma_norm_nic2_fb'] for k, v in d.items()}


def tail_fraction(spin, m):
    """FIX R3-NORM (acts/stage4/investigation/INV_NORM_F200.md): f = P(pT(QQ) > 200 GeV, |eta_pair| < 4), the population
    acceptance.json A_trig_presel is conditional on (Stage-3 template: TRGS, ptmin 200, eta_max 4).  E: xsec.json
    trigger_yields_E f_pt200_TRG_over_INC; Etilde (no xsec.json row): sum w(pT > 200, |eta| < 4) / sigma_ref_fb of
    data/sim/npz/S-TRGS_m<m>.npz (as inv_norm_f200.py and make_stage4_summary.py)."""
    if spin == 'F':
        r = json.loads(XSEC.read_text())['trigger_yields_E']['rows'].get(f'{int(m)}')
        return r['f_pt200_TRG_over_INC'] if r else None
    p = TT / 'data' / 'sim' / 'npz' / f'S-TRGS_m{int(m)}.npz'
    if not p.exists():
        return None
    z = np.load(p, allow_pickle=False)
    w, pt, eta = z['w'], z['pt_pair'], np.abs(z['eta_pair'])
    return float(w[(pt > 200) & (eta < 4)].sum() / float(z['sigma_ref_fb']))


def acceptance(I, key, t):
    """Inclusive-normalised A(trigger + preselection) per point: acceptance.json A_trig_presel (truth level, Stage 3;
    schema-v2 extension; conditional on pT(QQ) > 200 GeV) x the tail fraction f (FIX R3-NORM) if present, else the
    ESTIMATE trigger proxy f(pT(QQ) > 200, |eta| < 2.5) from sim/results/xsec.json trigger_yields_E (no
    preselection; E only).  Both branches are fractions of the inclusive sigma(pp -> QQ)."""
    ac = I.json('acceptance.json', proposed=True)
    if ac and key in ac.get('points', {}):
        f = tail_fraction(t['spin'], t['m'])
        if f is None:
            return None, None
        return ac['points'][key]['A_trig_presel'] * f, 'acceptance.json (truth level, Stage 3) x f(pT > 200)'
    if t['spin'] != 'F':
        return None, None
    rows = json.loads(XSEC.read_text())['trigger_yields_E']['rows']
    r = rows.get(f"{int(t['m'])}")
    return (r['f_pt200_eta25_TRG_over_INC'], 'ESTIMATE: xsec.json trigger proxy, no preselection') if r else (None, None)


def sigma_norm(spin, m):
    """sigma_norm [fb] (sim/results/xsec.json): E -> normalisation_E sigma_norm_nic2_fb, Etilde -> normalisation_S."""
    x = json.loads(XSEC.read_text())
    if spin == 'F':
        r = x['normalisation_E']['rows'].get(f'{int(m)}')
    else:
        r = x['normalisation_S'].get(f'{int(m)}')
    return r['sigma_norm_nic2_fb'] if r else None


def n_exp(I, key, t):
    """Predicted signal events in the trigger + preselection acceptance, N_exp = sigma_norm x 3 ab^-1 x A, with A the
    inclusive-normalised acceptance (A_trig_presel x f, FIX R3-NORM).
    Cross-checked against STAGE4_SUMMARY.json fallback_points[key].N_exp_3ab when the summary is used."""
    A, src = acceptance(I, key, t)
    s = sigma_norm(t['spin'], t['m'])
    if not A or s is None:
        return None, src
    n = s * LUMI_FB * A
    fp = I.fallback_point(key)
    if fp and fp.get('N_exp_3ab') and abs(fp['N_exp_3ab'] / n - 1) > 1e-6:
        raise RuntimeError(f'N_exp mismatch at {key}: {n} vs STAGE4_SUMMARY {fp["N_exp_3ab"]}')
    return n, src


def toy_limit(e):
    """(median, band1 (lo, hi), band2 (lo, hi), asymptotic median) of one limits.json point; toys are primary (D4),
    their bands are quantiles of the b-only test statistic from the same toys.  NaN where absent."""
    t = e.get('expected_toys') or {}
    a = e.get('expected_asymptotic') or {}
    f = lambda v: np.nan if v is None else float(v)              # noqa: E731
    b1 = t.get('band_1s') or [None, None]
    b2 = t.get('band_2s') or [None, None]
    return f(t.get('median')), (f(b1[0]), f(b1[1])), (f(b2[0]), f(b2[1])), f(a.get('median'))


def thin_ticks(vals, rmin=1.25):
    """grid values for log-axis tick labels, dropping a value closer than a factor rmin to the next larger kept one
    (e.g. 0.85 next to 1)."""
    out = []
    for v in sorted(set(vals), reverse=True):
        if not out or out[-1] / v >= rmin:
            out.append(v)
    return sorted(out)


def has_limit(e):
    return bool(e.get('expected_toys'))


def fallback_tag(I):
    o = I.outcome()
    if o['fallback']:
        return FALLBACK_TXT
    return f"working point: SR-T r* = {o['wp_T']}, SR-G r* = {o['wp_G']}"


def sci(v):
    """compact mathtext number for map cells: 37.6 -> '38', 1.25e7 -> '1.3x10^7'."""
    if not np.isfinite(v):
        return ''
    if v < 100:
        return f'{v:.3g}'
    k = int(np.floor(np.log10(v)))
    return rf'${v / 10 ** k:.1f}{{\times}}10^{{{k}}}$'


# ================================================================================================ detector figures
def fig_eps_maps(I, ctx):
    pts = a2_points(I)
    lim = I.json('limits.json')
    st = stamps(I, 'signal_eff.json')
    fb = I.outcome()['fallback'] if lim else False
    names = []
    F = by_mass(pts, 'F')
    if len(F) < 1:
        raise Skip('no E points')
    sels = REPORT + (['primary'] if lim else [])
    for sel in sels:
        xs, ys, zs = [], [], []
        for m, L in F.items():
            for lam, key, t in L:
                if sel == 'primary':
                    e = lim['points'].get(key, {}).get('s')
                    z = float(sum(e)) if e is not None else None
                else:
                    z = t['report_rungs'][sel]['eps']
                xs.append(m); ys.append(lam); zs.append(z)
        x, y, Z = P.grid_from_points(xs, ys, zs)
        fig, ax = P.figure()
        if sel == 'primary':
            zl = r'$\varepsilon(r_{fb})$, SR-T + SR-G' if fb else r'$\varepsilon$ (primary selection, SR-T + SR-G)'
        else:
            zl = r'signal efficiency $\varepsilon$'
        P.map2d(fig, ax, x, y, Z, zl, xlog=True, ylog=True, vmin=0, vmax=max(np.nanmax(Z), 1e-3),
                annotate=Z.size <= 64, fmt='{:.3f}')
        ax.set_xlabel(r'quirk mass $m_Q$ [GeV]')
        ax.set_ylabel(r'string tension scale $\Lambda$ [keV]')
        tag = [SPIN_LONG['F'] + ', PU 200 (8 cells full chain)']        # PAPER R2 B-4/C-2: E map has 8 A2FC cells
        if sel == 'primary':
            tag.append(FALLBACK_TXT if fb else 'primary selection per point (WP)')
        else:
            tag.append(REPORT_TXT[sel] + (r'; $\varepsilon$ is a lower bound' if sel == 'R_A' else ''))
        P.label(ax, tag_lines=tag, stamps=st, loc='lower right')
        nm = f"D1_eps_map_{'rfb' if (sel == 'primary' and fb) else sel}"
        P.save(fig, ctx['out'], nm, inputs=[I.path('signal_eff.json'), I.path('limits.json')], stamps=st, code=CODE,
               meta=dict(level='detector', selection=sel, fallback=fb, n_points=int(np.isfinite(Z).sum())))
        names.append(nm)
    return names


def fig_eff_vs_rung(I, ctx):
    from acts_names import LADDER_NAMES
    pts = a2_points(I)
    st = stamps(I, 'signal_eff.json')
    names = []
    for spin in ('F', 'S'):
        for m, L in by_mass(pts, spin).items():
            keep = sel_lams([l for l, _, _ in L])
            ser = []
            for lam, key, t in L:
                if lam not in keep:
                    continue
                lad = t['ladder']
                ser.append(dict(label=lam_txt(lam), y=[lad[n]['eps'] for n in LADDER_NAMES],
                                lo=[lad[n]['cp68'][0] for n in LADDER_NAMES],
                                hi=[lad[n]['cp68'][1] for n in LADDER_NAMES]))
            fig, ax = P.figure()
            P.eff_vs_rung(ax, LADDER_NAMES, ser, ylog=True, ylabel=r'signal efficiency $\varepsilon$',
                          families=[4, 8, 11, 14, 17, 20])
            ymin = min([v for s in ser for v in s['y'] if v] or [1e-3])
            ax.set_ylim(ymin / 300, 30.0)                # room for the tag below / legend above the data (PAPER R2 B-4)
            P.legend(ax, ncol=2, loc='upper right')
            P.label(ax, tag_lines=[plabel(spin, m) + ', A2 (PU 200)', 'error bars: CP 68 %',
                                   r'$\varepsilon$ = 0 not drawn (log scale)'], stamps=st, loc='lower left')
            nm = f"D2_eff_vs_rung_{spin}{int(m)}"
            P.save(fig, ctx['out'], nm, inputs=[I.path('signal_eff.json')], stamps=st, code=CODE,
                   meta=dict(level='detector', point=f'{spin}{int(m)}', lambdas=keep))
            names.append(nm)
    return names


def fig_bsum(I, ctx):
    from acts_names import LADDER_NAMES
    bw = I.need('bsum_wp.json')
    st = stamps(I, 'bsum_wp.json')
    o = I.outcome()
    lad = bw['ladder']
    ser = []
    for i, (c, txt) in enumerate((('T', 'SR-T'), ('G', 'SR-G'))):
        ser.append(dict(label=rf'{txt}: $B_{{84}}$', y=[r.get('B84') for r in lad[c]], color=P.PALETTE[i],
                        marker=P.MARKERS[i]))
        ser.append(dict(label=rf'{txt}: median $B$', y=[r.get('B_median') for r in lad[c]], color=P.PALETTE[i],
                        marker=P.MARKERS[i], ls=':'))
    fig, ax = P.figure()
    P.eff_vs_rung(ax, LADDER_NAMES, ser, ylog=True, ylabel=r'background events in 3 ab$^{-1}$',
                  families=[4, 8, 11, 14, 17, 20])
    ax.axhline(0.11, color=P.INK, ls='--', lw=1.5, label=r'$B_{84,c}$ = 0.11 (budget)')
    ax.axhline(0.3, color=P.MUTED, ls='-.', lw=1.5, label=r'$B_{84}$ = 0.3 (comb.)')
    for c, i in (('T', 0), ('G', 1)):
        r = (bw['rule'].get('wp') or {}).get(c)
        if r:
            ax.axvline(r, color=P.PALETTE[i], lw=1.2, ls='--', zorder=0)
    tag = []
    if o['fallback']:
        tag.append(r'no WP: $B_{84}$ > 0.11 at every rung in SR-T and SR-G')
        lad_s = (o.get('ladder') or {}).get('SR-G') or {}
        if lad_s.get('min_B84_rung') in LADDER_NAMES:
            xi = LADDER_NAMES.index(lad_s['min_B84_rung']) + 1
            ax.plot([xi], [lad_s['min_B84']], marker='*', ms=22, color=P.INK, ls='none', zorder=5,
                    label=r'min. $B_{84}$')
            tag += [rf"minimum $B_{{84}}$ = {sci(lad_s['min_B84'])} at {lad_s['min_B84_rung'].split('_')[0]}"
                    " (SR-T and SR-G),",
                    rf"i.e. {lad_s['decades_over_0p11_at_min']:.2f} decades above 0.11"]
        tag.append(r'fallback: limits at the pre-declared $r_{fb}$')     # PAPER R2 B-4
    else:
        tag += [f"working point: SR-T r* = {o['wp_T']}, SR-G r* = {o['wp_G']}", 'vertical dashed: r* per category']
    vals = [v for s in ser for v in s['y'] if v]
    ax.set_ylim(1e-3, max(vals + [1]) * 1e5)
    P.legend(ax, ncol=2)
    P.label(ax, tag_lines=tag, stamps=st, loc='upper left', y=0.37)
    P.save(fig, ctx['out'], 'D3_bsum_vs_rung', inputs=[I.path('bsum_wp.json'), getattr(I, 'summary_path', None)
                                                       or I.path('bsum_wp.json')], stamps=st, code=CODE,
           meta=dict(level='detector', complete_inputs=bw['rule'].get('complete_inputs'), wp=bw['rule'].get('wp'),
                     branch=o['branch']))
    return ['D3_bsum_vs_rung']


def fig_pfake(I, ctx):
    from acts_names import LADDER_NAMES
    bk = I.need('background.json')
    st = stamps(I, 'background.json')
    cols = bk['columns'][:14]
    es = bk['end_state'][:14]
    names = LADDER_NAMES[:14]
    x = np.arange(1, 15)
    fig, (ax, rx) = P.figure(ratio=True)
    g = lambda r, k: np.nan if r.get(k) is None else r[k]   # noqa: E731
    yd = np.array([g(r, 'B1_per_trial') for r in cols])
    nb = np.array([g(r, 'B1_groups') for r in cols])
    yt = np.array([g(r, 'P_thin') for r in cols])
    yf = np.array([g(r, 'P_fact') for r in cols])
    yd[yd <= 0] = np.nan
    ax.errorbar(x, yd, yerr=np.where(nb > 0, yd / np.sqrt(np.maximum(nb, 1)), np.nan), fmt='o', color=P.INK,
                label=r'B1 direct ($\rho$ = 1)')
    ax.plot(x, yt, 's', mfc='none', color=P.PALETTE[0], label=r'thinning ($\rho$ = 2)')
    # REVIEW R1 B5: P_fact == B1_per_trial wherever B1_groups > 0 (R01-R07) by construction -> draw the model only
    # where it is an independent extrapolation (B1 = 0, rungs >= R08), so the diamonds do not read as agreement
    same = (nb > 0) & np.isclose(yf, np.nan_to_num(yd), rtol=1e-9, atol=0)
    yf_ext = np.where(same, np.nan, yf)
    ax.plot(x, yf_ext, 'D', mfc='none', color=P.PALETTE[1],
            label=r'factorisation ($\geq$ R08)')
    pe = np.array([g(r, 'P_per_trial') for r in es])
    sl = np.array([g(r, 'sigma_ln') for r in es])
    ax.fill_between(x, pe * np.exp(-sl), pe * np.exp(sl), color='#a8e3cb', lw=0,
                    label=r'end state $\pm\sigma_{ln}$')
    ax.plot(x, pe, '-', color=P.PALETTE[2], label='end state (closure)')
    ax.set_yscale('log')
    ax.set_ylabel('PU fake candidates per trial')
    v = np.concatenate([a[np.isfinite(a) & (a > 0)] for a in (yd, yt, yf_ext, pe, pe * np.exp(-sl), pe * np.exp(sl))])
    ax.set_ylim(v.min() / 1e8, v.max() * 1e7)
    P.legend(ax, ncol=2, handlelength=1.2, columnspacing=0.8)       # PAPER R2 B-4: fits the axes at 'small'
    cl = bk['closure']
    P.label(ax, tag_lines=['PU 200 only, MET roads', f"closure T1: {cl.get('T1', {}).get('branch')} "
                                                    f"(trend: {'yes' if cl.get('trend', {}).get('significant') else 'no'})",
                           r'rungs $\geq$ R08: zero-count bounds',
                           r'factorisation $\equiv$ B1 direct at R01-R07 (not drawn)'],
            stamps=st, loc='lower left')
    tp = cl.get('trend', {}).get('points', [])
    if tp:
        rx.errorbar([p['x'] for p in tp], [np.exp(p['ln_r']) for p in tp],
                    yerr=[np.exp(p['ln_r']) * p['sig'] for p in tp], fmt='o', color=P.INK)
    rx.axhline(1.0, color=P.MUTED, ls='--')
    rx.set_ylim(0.3, 2.2)
    rx.set_ylabel(r'$N_{obs}/N_{pred}$')
    rx.set_xticks(x)
    rx.set_xticklabels([P.rung_label(n, short=False) for n in names], rotation=90, fontsize='xx-small')
    rx.xaxis.set_minor_locator(P.matplotlib.ticker.NullLocator())
    rx.set_xlim(0.3, 14.7)
    rx.set_xlabel('selection ladder rung (cumulative)')
    P.save(fig, ctx['out'], 'D4_pfake_extrapolation', inputs=[I.path('background.json')], stamps=st, code=CODE,
           meta=dict(level='detector', closure_branch=cl.get('T1', {}).get('branch'),
                     y_quantity='expected PU fake candidates (groups) per trial (B1_per_trial = B1_groups / trials)',
                     factorisation_drawn_rungs=[n for n, q in zip(names, same) if not q],
                     factorisation_equals_direct_rungs=[n for n, q in zip(names, same) if q]))
    return ['D4_pfake_extrapolation']


def log_frame(ax, lo, hi, bot=0.25, top=0.32):
    """Log y range with the data spanning the middle (1 - bot - top) of the axes: the bottom `bot` fraction is kept
    for the tag block, the top `top` fraction for the legend (REVIEW R1 C1: no empty decades beyond that)."""
    d = max(np.log10(hi / lo), 1.0)
    t = d / (1.0 - bot - top)
    ax.set_ylim(lo / 10 ** (bot * t), hi * 10 ** (top * t))


def fig_limit_mu(I, ctx):
    pts = a2_points(I)
    lim = I.need('limits.json')
    st = stamps(I, 'limits.json')
    fb = I.outcome()['fallback']
    names = []
    for spin in ('F', 'S'):
        for m, L in by_mass(pts, spin).items():
            rows = [(lam, key, t, lim['points'].get(key, {})) for lam, key, t in L]
            ok = [r for r in rows if has_limit(r[3])]
            nolim = [r[0] for r in rows if not has_limit(r[3])]
            if not ok:
                continue
            lam = np.array([r[0] for r in ok])
            T = [toy_limit(r[3]) for r in ok]
            med = np.array([q[0] for q in T])
            b1 = (np.array([q[1][0] for q in T]), np.array([q[1][1] for q in T]))
            b2 = (np.array([q[2][0] for q in T]), np.array([q[2][1] for q in T]))
            am = np.array([q[3] for q in T])
            ne = np.array([n_exp(I, k, t)[0] or np.nan for _, k, t, _ in ok])
            fig, ax = P.figure()
            P.limit_plot(ax, lam, med, band1=b1, band2=b2, median_alt=am, xlog=True, ylog=True,
                         labels=dict(median='Expected median (toys, primary)',
                                     band1=r'Expected $\pm$1$\sigma$ (toys)', band2=r'Expected $\pm$2$\sigma$ (toys)',
                                     alt='Expected median, asymptotic (cross-check)'))
            ax.plot(lam, ne, '-', marker='o', color=P.PALETTE[7], lw=2.5,
                    label=r'predicted $N_{exp} = \sigma_{norm}\cdot f\cdot L\cdot A$')
            ax.set_xlabel(r'string tension scale $\Lambda$ [keV]')
            ax.set_ylabel(r'95 % CL upper limit on $N_{sig}$ (in acceptance)')
            P.log_ticks(ax.xaxis, thin_ticks([r[0] for r in rows]))
            ax.set_xlim(min(r[0] for r in rows) / 1.15, max(r[0] for r in rows) * 1.15)
            v = np.concatenate([med, b2[1], b2[0], ne])
            v = v[np.isfinite(v) & (v > 0)]
            log_frame(ax, v.min(), v.max())                   # REVIEW R1 C1: room for tag + legend only
            P.legend(ax)
            r = med / ne
            j = int(np.nanargmin(r))
            tag = [plabel(spin, m) + ', SR-T + SR-G two-bin counting',
                   (r'at $r_{fb}$ (no WP, fallback)' if fb else 'at the WP selection'),
                   rf'best $\mu_{{95}}/N_{{exp}}$ = {sci(r[j])} at $\Lambda$ = {lam[j]:g} keV (no exclusion)'
                   if r[j] > 1 else rf'$\mu_{{95}}/N_{{exp}}$ < 1 at $\Lambda$ = {lam[j]:g} keV']
            if nolim:
                tag.append(r'no limit ($\varepsilon$ = 0) at $\Lambda$ = ' + ', '.join(f'{l:g}' for l in nolim) + ' keV')
            P.label(ax, tag_lines=tag, stamps=st, loc='lower left')
            nm = f'D5_limit_mu_vs_lambda_{spin}{int(m)}'
            P.save(fig, ctx['out'], nm, inputs=[I.path('limits.json'), I.path('signal_eff.json'),
                                                I.path('acceptance.json', True), XSEC], stamps=st,
                   code=CODE, meta=dict(level='detector', point=f'{spin}{int(m)}', bands='toys (primary)',
                                        mu95_over_Nexp={f'{l:g}': float(q) for l, q in zip(lam, r)},
                                        no_limit_lambdas=nolim))
            names.append(nm)
    if not names:
        raise Skip('no point with an expected limit')
    return names


def _xsec_table(I, pts, lim):
    """rows: spin, m, lam, key, sigma95 toys median, asymptotic median, toy band1/band2, mu_5sigma (as sigma), A src."""
    out = []
    for key, t in pts.items():
        e = lim['points'].get(key, {})
        if not has_limit(e):
            continue
        A, src = acceptance(I, key, t)
        if not A:
            continue
        f = 1.0 / (LUMI_FB * A)
        med, b1, b2, am = toy_limit(e)
        d5 = (e.get('discovery') or {}).get('mu_5sigma')
        out.append(dict(spin=t['spin'], m=float(t['m']), lam=float(t['lam']), key=key, med=med * f, am=am * f,
                        b1=[b1[0] * f, b1[1] * f], b2=[b2[0] * f, b2[1] * f],
                        d5=(d5 * f) if d5 else np.nan, A_src=src))
    return out


def fig_limit_xsec(I, ctx):
    pts = a2_points(I)
    lim = I.need('limits.json')
    st = stamps(I, 'limits.json')
    fb = I.outcome()['fallback']
    rows = [r for r in _xsec_table(I, pts, lim) if r['spin'] == 'F']
    if not rows:
        raise Skip('no E point with a limit and an acceptance')
    srcs = sorted({r['A_src'] for r in rows})
    th = theory_E()
    names = []
    lams = sorted({r['lam'] for r in rows})
    for lam in [l for l in lams if l in (0.6, 1.0, 1.5, 2.0, 3.0, 5.0)] or lams[:3]:
        R = sorted([r for r in rows if r['lam'] == lam], key=lambda r: r['m'])
        if len(R) < 2:
            continue
        m = np.array([r['m'] for r in R])
        fig, ax = P.figure()
        P.limit_plot(ax, m, [r['med'] for r in R], band1=([r['b1'][0] for r in R], [r['b1'][1] for r in R]),
                     band2=([r['b2'][0] for r in R], [r['b2'][1] for r in R]), median_alt=[r['am'] for r in R],
                     theory=th, xlog=False, ylog=True,
                     labels=dict(median='Expected median (toys, primary)', band1=r'Expected $\pm$1$\sigma$ (toys)',
                                 band2=r'Expected $\pm$2$\sigma$ (toys)',
                                 alt='Expected median, asymptotic (cross-check)'))
        ax.set_xlabel(r'quirk mass $m_Q$ [GeV]')
        ax.set_ylabel(r'95 % CL limit on inclusive $\sigma(pp\to Q\bar{Q})$ [fb]')   # FIX R3-NORM: A x f
        ax.set_xlim(150, 1550)
        v = np.array([r['b2'][1] for r in R] + [r['b2'][0] for r in R] + list(th['y']), float)
        v = v[np.isfinite(v) & (v > 0)]
        log_frame(ax, v.min(), v.max())                       # REVIEW R1 C1: room for tag + legend only
        P.legend(ax)
        ratio = [r['med'] / float(np.exp(np.interp(r['m'], th['x'], np.log(th['y'])))) for r in R]
        mis = sorted({int(t['m']) for k, t in pts.items() if t['spin'] == 'F' and float(t['lam']) == lam}
                     - {int(r['m']) for r in R})
        tag = ['E, ' + lam_txt(lam) + (r', at $r_{fb}$ (no WP)' if fb else ''),     # PAPER R2 B-4: no file names (sigma_th label held: NORM-ANCHOR, coordinator 2026-10-16)
               'A: ' + '; '.join('truth-level acceptance (Stage 3)' if 'truth' in s_ else s_ for s_ in srcs),
               rf'$\sigma_{{95}}/\sigma_{{th}}$ $\geq$ {sci(min(ratio))}: no exclusion'
               if min(ratio) > 1 else rf'min $\sigma_{{95}}/\sigma_{{th}}$ = {sci(min(ratio))}']
        if mis:
            tag.append(r'no limit ($\varepsilon$ = 0): $m_Q$ = ' + ', '.join(map(str, mis)) + ' GeV')
        P.label(ax, tag_lines=tag, stamps=st, loc='lower left')
        nm = f"D6_limit_xsec_vs_m_L{lam:g}".replace('.', 'p')
        P.save(fig, ctx['out'], nm, inputs=[I.path('limits.json'), I.path('signal_eff.json'), XSEC,
                                            I.path('acceptance.json', True)], stamps=st, code=CODE,
               meta=dict(level='detector (A truth level)', lam_keV=lam, acceptance_source=srcs,
                         sigma95_over_sigma_th={f"{int(r['m'])}": q for r, q in zip(R, ratio)}))
        names.append(nm)
    if not names:
        raise Skip('fewer than 2 masses per Lambda')
    return names


# REVIEW R1 C5: in-figure names of the recast curves (citation of a recast, not an experiment label)
EXT_DISPLAY = {'CMS HSCP recast': 'Farina-Low HSCP recast', 'ATLAS/CMS monojet recast': 'monojet recast',
               'CMS out-of-time recast': 'Evans-Luty out-of-time recast'}
EXT_STYLE = [P.PALETTE[5], P.PALETTE[6], P.PALETTE[3], P.PALETTE[4], P.INK2, P.MUTED]


def overlay_external(ax, ext, model):
    """Draw the existing limits of stage5/external_bounds.json (schema 'external_bounds v1', see
    stage5/EXTERNAL_BOUNDS.md) for `model` ('E' or 'Etilde') on a (m [GeV], Lambda [keV]) axes, without changing
    the axes range.  Only curves with draw = true and model in applies_to.  kind: upper_mass_edge -> hatched region
    from the left frame to the curve + line; polygon -> hatched closed region; benchmarks -> markers.
    Returns (legend handles of the curves visible in the range, labels of the curves entirely outside it)."""
    xl, yl = ax.get_xlim(), ax.get_ylim()
    inside = lambda m, l: xl[0] < m < xl[1] and yl[0] < l < yl[1]                      # noqa: E731
    hs, outside = [], []
    k = 0
    for cid, c in ext['curves'].items():
        if not c.get('draw') or model not in c['applies_to']:
            continue
        pts = np.asarray(c['points'], float)
        m, lam = pts[:, 0], pts[:, 1]
        name_ = EXT_DISPLAY.get(c['label'].split(' (')[0], c['label'].split(' (')[0])
        lab = f"{c['label']} [{c['uncertainty_tag']}]"
        span = f"{name_} ({lam.min():.2g}-{lam.max():.4g} keV, m < {m.max():.0f} GeV)"
        col = EXT_STYLE[k % len(EXT_STYLE)]
        if c['kind'] == 'upper_mass_edge':
            o = np.argsort(lam)
            m, lam = m[o], lam[o]
            ll = np.geomspace(lam[0], lam[-1], 400)
            mm = np.interp(np.log(ll), np.log(lam), m)
            if not any(inside(a, b) for a, b in zip(mm, ll)):
                outside.append(span)
                continue
            ax.fill_betweenx(lam, np.full_like(m, min(xl[0], m.min()) * 0.5), m, facecolor='none', edgecolor=col,
                             hatch='//', lw=0, zorder=3)
            ax.plot(m, lam, color=col, lw=2.0, zorder=3.5)
            h = (P.matplotlib.patches.Patch(facecolor='none', edgecolor=col, hatch='//', lw=2.0, label=lab))
        elif c['kind'] == 'polygon':
            if not (m.min() < xl[1] and m.max() > xl[0] and lam.min() < yl[1] and lam.max() > yl[0]):
                outside.append(span)
                continue
            h = P.matplotlib.patches.Polygon(pts, closed=True, facecolor='none', edgecolor=col, hatch='\\\\',
                                             lw=2.0, zorder=3, label=lab)
            ax.add_patch(h)
        elif c['kind'] == 'benchmarks':
            if not any(inside(a, b) for a, b in zip(m, lam)):
                outside.append(f"{name_} (points at {', '.join(f'{b:g}' for b in lam)} keV)")
                continue
            h = ax.plot(m, lam, ls='none', marker=P.MARKERS[k % len(P.MARKERS)], ms=9, color=col, zorder=4,
                        label=lab)[0]
        else:
            raise ValueError(f'external_bounds: unknown kind {c["kind"]!r} for {cid}')
        hs.append(h)
        k += 1
    ax.set_xlim(xl)
    ax.set_ylim(yl)
    return hs, outside


def fig_excl_map(I, ctx):
    pts = a2_points(I)
    lim = I.need('limits.json')
    st = stamps(I, 'limits.json')
    fb = I.outcome()['fallback']
    rows = [r for r in _xsec_table(I, pts, lim) if r['spin'] == 'F']
    if not rows:
        raise Skip('no E point with a limit and an acceptance')
    th = theory_E()
    sth = lambda m: float(np.exp(np.interp(m, th['x'], np.log(th['y']))))   # noqa: E731
    allF = [(float(t['m']), float(t['lam'])) for t in pts.values() if t['spin'] == 'F']
    # the grid covers every A2 E point (eps = 0 points stay blank); grid_from_points writes in order, so the None
    # fillers come FIRST and the real cells overwrite them
    def grid(vals):
        return P.grid_from_points([a for a, b in allF] + [r['m'] for r in rows],
                                  [b for a, b in allF] + [r['lam'] for r in rows], [None] * len(allF) + vals)
    x, y, Z = grid([r['med'] / sth(r['m']) for r in rows])
    _, _, Zlo = grid([r['b1'][0] / sth(r['m']) for r in rows])
    _, _, Zhi = grid([r['b1'][1] / sth(r['m']) for r in rows])
    _, _, Zd = grid([r['d5'] / sth(r['m']) for r in rows])
    fig, ax = P.figure()
    zmin, zmax = np.nanmin(Z), np.nanmax(Z)
    if zmin > 1:              # nothing excluded: one-sided sequential log scale starting at 1 (no unused blue half)
        P.map2d(fig, ax, x, y, Z, r'expected $\sigma_{95}/\sigma_{th}$ (toys median)', xlog=True, ylog=True,
                zlog=True, vmin=1.0, vmax=10 ** np.ceil(np.log10(zmax)), annotate=True, fmt=sci)
    else:
        r = 10 ** max(np.ceil(np.nanmax(np.abs(np.log10(Z[np.isfinite(Z) & (Z > 0)])))), 1)
        P.map2d(fig, ax, x, y, Z, r'expected $\sigma_{95}/\sigma_{th}$ (toys median)', xlog=True, ylog=True,
                zlog=True, vmin=1 / r, vmax=r, center=1.0, annotate=True, fmt=sci)
    ax.set_xlabel(r'quirk mass $m_Q$ [GeV]')
    ax.set_ylabel(r'string tension scale $\Lambda$ [keV]')
    hs = []
    drawn = {}
    for nm_, Zc, ls, lab in (('exp', Z, '-', r'expected exclusion ($\sigma_{95} = \sigma_{th}$)'),
                             ('lo', Zlo, '--', r'expected $\pm$1$\sigma$ (toys)'), ('hi', Zhi, '--', None),
                             ('disc', Zd, ':', r'5$\sigma$ discovery (expected)')):
        drawn[nm_] = bool(np.isfinite(Zc).sum() >= 4 and np.nanmin(Zc) < 1 < np.nanmax(Zc) and len(x) > 1
                          and len(y) > 1)
        if drawn[nm_]:
            ax.contour(x, y, np.log10(Zc), levels=[0.0], colors=P.INK, linestyles=ls, linewidths=2.5)
            if lab:
                hs.append(P.matplotlib.lines.Line2D([], [], color=P.INK, ls=ls, lw=2.5, label=lab))
    ext = json.loads(EXT.read_text()) if EXT.exists() else None
    # PAPER R2 B-4: short tag at print size.  The bounds outside the plotted range, the 5 sigma statement and the
    # full-chain efficiency systematic (INV_A2FC_E500 CLOSED: x 0.87, STAGE4_RESULTS 4.3) are in the paper caption
    # and in the sidecar meta (outside_range, discovery_cells).
    tag = [SPIN_LONG['F'] + (r', at $r_{fb}$ (no WP)' if fb else ''),
           'A: truth-level acceptance (Stage 3)' if all('truth' in r['A_src'] for r in rows)
           else 'A: ' + '; '.join(sorted({r['A_src'] for r in rows}))]
    if not drawn['exp']:
        zlo = float(np.nanmin(Zlo)) if np.isfinite(Zlo).any() else float('nan')   # PAPER R3 C-1: quote the -1 sigma edge
        tag.append(rf'no expected exclusion: median $\geq$ {zmin:.3g} in every cell'
                   + (rf', $-1\sigma$ edge $\geq$ {sci(10 ** (np.floor(np.log10(zlo) * 100) / 100)) if zlo >= 100 else int(np.floor(zlo))}'
                      if not drawn['lo'] else ''))   # PAPER R4: floor, not round (54.6 -> '54')
    nd = int(np.isfinite(Zd).sum())
    tag.append(r'blank cells: $\varepsilon$ = 0 (no limit)')
    outside = []
    if ext:
        hx, outside = overlay_external(ax, ext, 'E')
        cname = {P.PALETTE[5]: 'green', P.PALETTE[6]: 'purple', P.PALETTE[3]: 'yellow', P.PALETTE[4]: 'pink',
                 P.INK2: 'dark grey', P.MUTED: 'grey'}
        for h in hx:        # described in the tag (an in-axes legend would cover map cells)
            col = h.get_edgecolor() if hasattr(h, 'get_edgecolor') else h.get_color()
            col = P.matplotlib.colors.to_hex(col)
            tag.insert(2, f"{cname.get(col, col)} hatched: {h.get_label().split(' [')[0]}, 95 % CL exclusion")
    else:
        tag.append('FASER / D0 / Farina-Low overlay: stage5/external_bounds.json missing')
    if hs:
        ax.legend(handles=hs, loc='upper left')
    ax.xaxis.set_major_formatter(P.matplotlib.ticker.FormatStrFormatter('%g'))
    ax.yaxis.set_major_formatter(P.matplotlib.ticker.FormatStrFormatter('%g'))
    P.label(ax, tag_lines=tag, stamps=st, loc='lower right')
    P.save(fig, ctx['out'], 'D7_exclusion_map', inputs=[I.path('limits.json'), I.path('signal_eff.json'), XSEC,
                                                         I.path('acceptance.json', True), EXT],
           stamps=st, code=CODE, meta=dict(level='detector (A truth level)', contours_drawn=drawn,
                                           min_sigma95_over_sigma_th=float(zmin), outside_range=outside,
                                           discovery_cells=nd))
    return ['D7_exclusion_map']


def fig_mest(I, ctx):
    pts = a2_points(I)
    z = I.need('signal_obs_a2.npz')
    lim = I.json('limits.json')
    st = stamps(I, 'signal_eff.json')
    fb = I.outcome()['fallback'] if lim else False
    keys = z['key'].astype(str)
    fb_names = [str(n) + '&h>5&o>5' for n in z['FB_names']]
    L, FB, fck, M = z['L'], z['FB'], z['f_ckf'], z['M_est']
    names = []
    for selmode in ('R_A', 'primary'):
        if selmode == 'primary' and not lim:
            continue
        for spin in ('F', 'S'):
            for m, Lp in by_mass(pts, spin).items():
                keep = sel_lams([l for l, _, _ in Lp], 4)
                fig, ax = P.figure()
                n_any = 0
                curves = {}
                data = []
                for i, (lam, key, t) in enumerate([q for q in Lp if q[0] in keep]):
                    sel = (keys == key) & (fck < 0.2)
                    if selmode == 'R_A':
                        sel &= L[:, 3]
                        selname = r'$R_A$ ($N_{IP2}\geq 7$)'
                    else:
                        pr = lim['points'][key]['primary']['G']
                        if pr['kind'] == 'r*':
                            sel &= L[:, pr['rung'] - 1]
                        elif pr['name'] in fb_names:
                            sel &= FB[:, fb_names.index(pr['name'])]
                        else:
                            raise RuntimeError(f'unknown selection {pr["name"]} at {key}')
                        selname = r'$r_{fb}$ (fallback)' if fb else 'WP selection'
                    # one entry per event: the first (best-ranked) candidate of each row
                    idx = np.where(sel)[0]
                    _, first = np.unique(z['row'][idx], return_index=True)
                    v = M[idx[first]]
                    v = v[np.isfinite(v)]
                    if len(v) < 5:
                        continue
                    data.append((i, lam, v, len(first)))
                # REVIEW R1 B1: M_est is a pair-mass proxy (M_QQ >= 2 m_Q, entries up to ~6 m_Q).  Bins of 0.4 m_Q
                # (2 m_Q on a bin edge); range = up to the largest entry, between 3.2 and 6 m_Q (at a fixed 3 m_Q,
                # 50-70 % of the E~500 entries were in the overflow bin)
                bw = 0.4 * m
                rmax = max([float(np.max(v)) for _, _, v, _ in data] or [3 * m])
                hi = bw * min(15, max(8, int(np.ceil(rmax / bw + 1e-9))))
                edges = np.arange(0, hi + 0.5 * bw, bw)
                for i, lam, v, nev in data:
                    n_any += 1
                    r_ = v / m
                    curves[f'{lam:g}'] = dict(N_events=int(len(v)), N_undefined=int(nev - len(v)),
                                             median_over_m=float(np.median(r_)),
                                             frac_below_0p5m=float(np.mean(r_ < 0.5)),
                                             n_1p3_1p7m=int(((r_ > 1.3) & (r_ < 1.7)).sum()),
                                             frac_overflow=float(np.mean(v >= hi)))
                    cnt, _ = np.histogram(np.clip(v, 0, hi * 0.999), edges)
                    P.hist_errorbar(ax, edges, cnt, f'{lam_txt(lam)} (N = {len(v)})', P.PALETTE[i],
                                    density='fraction')
                if not n_any:
                    P.plt.close(fig)
                    continue
                # reference lines stop below the tag / legend block (ymax in axes fraction)
                # REVIEW R1 B1: only the 2 m_Q threshold is marked (M_est estimates the pair mass, not m_Q)
                ax.axvline(2 * m, ymax=0.45, color=P.INK, ls='--', lw=2.0,
                           label=r'2 $m_Q$ ($M_{Q\bar{Q}}$ threshold)')
                ax.set_xlabel(r'$M_{est}$ = MET cosh$\eta_{axis}$ / $(\beta\gamma)_{ToF}$ [GeV]')
                ax.set_ylabel(f'fraction of events / {bw:g} GeV')
                ax.set_xlim(0, hi)
                ax.set_ylim(0, ax.get_ylim()[1] * 2.5)       # PAPER R2 B-4: tag below the legend, above the data
                P.legend(ax)
                P.label(ax, tag_lines=[plabel(spin, m) + ', PU 200, ' + selname,      # PAPER R2 B-4: shorter
                                       r'$f_{CKF}$ < 0.2, best cand. per event',
                                       r'last bin: overflow; $M_{est}$: pair-mass proxy'],
                        stamps=st, loc='upper left', y=0.64)
                nm = f"D8_mest_{'RA' if selmode == 'R_A' else ('rfb' if fb else 'primary')}_{spin}{int(m)}"
                P.save(fig, ctx['out'], nm, inputs=[I.path('signal_obs_a2.npz'), I.path('limits.json')],
                       stamps=st, code=CODE, meta=dict(level='detector', point=f'{spin}{int(m)}', lambdas=keep,
                                                       selection=selmode, x_range_GeV=[0.0, float(hi)],
                                                       per_curve_event_level=curves,
                                                       estimator='pair-mass proxy |MET| cosh(eta)/(beta gamma), '
                                                                 'M_QQ >= 2 m_Q (acts/stage4/analysis/signal.py)'))
                names.append(nm)
    return names


TRUTH_EDGES = [('lower_lmax_RIT_closed', r'lower: median $\ell_{max} = R_{IT}$'),
               ('lower_Nosc1_closed', r'lower: $N_{osc}$ = 1'),
               ('upper_merge100_hit', r'upper: 100 $\mu$m merging'),
               ('upper_lmax100um_closed', r'upper: median $\ell_{max}$ = 100 $\mu$m')]


def p2_edges():
    p = json.loads(P2.read_text())['edges']
    out = {}
    for k, v in p.items():
        spin, m = k.split('_m')
        for e, _ in TRUTH_EDGES:
            if e in v and v[e].get('value') is not None and np.isfinite(v[e]['value']):
                out.setdefault(e, {}).setdefault(spin, []).append((float(m), v[e]['value'], v[e].get('stat_err')))
    return out


def merged_surface_edges(I, key='f_merge_any'):
    """Truth-level upper-edge comparator (INV_SIGNAL_EFF §3.1, STAGE4_RESULTS §6.1): the Lambda where the fraction of
    central events with ANY inner-pixel surface merged (key='f_merge_any'; or merged OR seed-degenerate,
    key='f_either') crosses 50 %.  Linear interpolation in ln Lambda between the bracketing grid points; error from
    the binomial sigma_f = sqrt(f (1 - f) / n) at 50 % divided by the local slope df/dlnLambda (ESTIMATE).
    Source: STAGE4_SUMMARY.json cited_investigations.truth_degeneracy (else the investigation JSONs, read-only).
    Returns {(spin, m): (Lambda50, err)} and the source path."""
    src = None
    pts = ((I.summary or {}).get('cited_investigations') or {}).get('truth_degeneracy', {}).get('points')
    if pts:
        src = I.summary_path
    else:
        pts = {}
        for p in sorted(INV.glob('truth_degeneracy_*.json')):
            pts[p.stem.split('_')[-1]] = json.loads(p.read_text())
            src = INV
    out = {}
    for sm, d in pts.items():
        spin, m = sm[0], float(sm[1:])
        g = sorted((float(l), v[key], v['n']) for l, v in d.items())
        for (l1, f1, n1), (l2, f2, n2) in zip(g[:-1], g[1:]):
            if f1 < 0.5 <= f2:
                u = np.log(l1) + (0.5 - f1) / (f2 - f1) * (np.log(l2) - np.log(l1))
                slope = (f2 - f1) / (np.log(l2) - np.log(l1))
                sf = np.sqrt(0.25 / (0.5 * (n1 + n2)))
                out[(spin, m)] = (float(np.exp(u)), float(np.exp(u) * sf / slope))
                break
    return out, src


def fig_edges(I, ctx):
    ed = I.need('edges_det.json', proposed=True)
    st = list(dict.fromkeys(stamps(I) + P.stamps_of(ed)))
    pts = ed['points']
    if not all(len(k.split('|')) == 3 for k in pts):
        raise Skip("edges_det.json layout is not 'sample|spin|m' (schema v2)")
    fig, ax = P.figure()

    def series(sample, spin, rung, side):
        d = []
        for k, v in pts.items():
            s_, sp, m = k.split('|')
            e = (v.get(rung) or {}).get(side) or {}
            if s_ == sample and sp == spin:
                d.append((float(m), e.get('value'), e.get('stat_err')))
        return sorted(d)

    def truth(spin, name):
        d = []
        for k, v in pts.items():
            s_, sp, m = k.split('|')
            e = (v.get('truth') or {}).get(name) or {}
            if s_ == 'A1' and sp == spin and e.get('value') is not None:
                d.append((float(m), e['value'], e.get('stat_err') or 0))
        return sorted(d)

    def draw(d, fmt, color, label, spin, **kw):
        d = [q for q in d if q[1] is not None]
        if not d:
            return
        ax.errorbar([q[0] for q in d], [q[1] for q in d], yerr=[q[2] or 0 for q in d], fmt=fmt, color=color,
                    mfc=None if spin == 'F' else 'none', ls='-' if spin == 'F' else 'none', lw=1.2,
                    label=label if spin == 'F' else None, **kw)

    a2_upper_missing = []
    for spin in ('F', 'S'):
        draw(truth(spin, 'lower_lmax_RIT_closed'), 'D', P.MUTED, r'truth lower: median $\ell_{max} = R_{IT}$', spin,
             ms=9)
        draw(series('A1', spin, 'R04', 'lower'), 'o', P.PALETTE[0], 'A1 (no PU), lower edge', spin)
        draw(series('A1', spin, 'R04', 'upper'), 's', P.PALETTE[0], 'A1 (no PU), upper edge', spin)
        draw(series('A2', spin, 'R04', 'lower'), 'o', P.PALETTE[1], 'A2 (PU 200), lower edge', spin, ms=12)
        for m, v, _ in series('A2', spin, 'R04', 'upper'):
            if v is None:
                a2_upper_missing.append((spin, m))
    lammax_a2 = max(max(v.get('lam_keV') or [0]) for k, v in pts.items() if k.startswith('A2|'))
    if a2_upper_missing:
        for spin in ('F', 'S'):
            mm = [m for s_, m in a2_upper_missing if s_ == spin]
            if mm:
                ax.plot(np.array(mm) - 30, [lammax_a2] * len(mm), ls='none', marker=r'$\uparrow$', ms=26,
                        color=P.PALETTE[1],
                        label=rf'A2 upper edge: none below {lammax_a2:g} keV (grid end)' if spin == 'F' else None)
    tm, src_tm = merged_surface_edges(I, 'f_merge_any')
    te, _ = merged_surface_edges(I, 'f_either')
    for spin in ('F', 'S'):
        for dd, fmt, lab, dx in ((tm, 'P', 'truth upper (post hoc): any surface merged', 30),
                                 (te, 'X', 'truth upper (post hoc): merged or seed-degen.', 60)):
            q = sorted((m + dx, v[0], v[1]) for (s_, m), v in dd.items() if s_ == spin)
            if q:
                ax.errorbar([a for a, _, _ in q], [b for _, b, _ in q], yerr=[c for _, _, c in q], fmt=fmt,
                            color=P.PALETTE[6] if fmt == 'P' else P.PALETTE[4], ms=14,
                            mfc=None if spin == 'F' else 'none', ls='none',
                            label=lab if spin == 'F' else None)
    ax.plot([], [], 'o', color=P.INK, label=r'filled: E, open: $\tilde{E}$ (some markers offset in $m_Q$)')
    ax.set_yscale('log')
    ax.set_xlabel(r'quirk mass $m_Q$ [GeV]')
    ax.set_ylabel(r'$\Lambda$ edge [keV]')
    ax.set_xlim(120, 1620)
    ax.set_ylim(0.012, 3e4)               # REVIEW R1 B4 / PAPER R2 B-4: tag below, legend above the data
    P.log_ticks(ax.yaxis, [0.1, 0.3, 1, 3, 10, 30, 100])
    h, l = ax.get_legend_handles_labels()
    order = sorted(range(len(l)), key=lambda i: (l[i].startswith('filled'), 0))
    ax.legend([h[i] for i in order], [l[i] for i in order], loc='upper right', ncol=1, fontsize='x-small')   # 8 entries
    P.label(ax, tag_lines=[r'half-maximum of $\varepsilon(R_A)$ in ln $\Lambda$',      # PAPER R2 B-4: no report ids
                           'detector level vs truth-level comparators',
                           'not drawn: pre-declared 12.8-25 keV edge',   # PAPER R3 C-4
                           r'(not met; A1 upper edges $\times$2.7-3.5 lower)'],
            stamps=st, loc='lower right')
    P.save(fig, ctx['out'], 'D9_edges_det_vs_truth', inputs=[I.path('edges_det.json', True),
                                                             src_tm if src_tm and Path(src_tm).is_file()
                                                             else I.path('edges_det.json', True)],
           stamps=st, code=CODE,
           meta=dict(level='detector + truth-level comparators', truth_upper_source=_rel_tt(src_tm or ''),
                     truth_upper_any_merged={f'{s}{int(m)}': v for (s, m), v in tm.items()},
                     truth_upper_merged_or_seed={f'{s}{int(m)}': v for (s, m), v in te.items()},
                     a2_upper_missing=[f'{s}{int(m)}' for s, m in a2_upper_missing],
                     display_offsets_GeV=dict(truth_any_merged=30, truth_merged_or_seed=60, a2_upper_arrow=-30),
                     not_drawn='Stage-3 upper_merge100_hit (median IT sep < 100 um, 13-25 keV): not the comparator '
                               'of the detector upper edge (STAGE4_RESULTS §6.1)'))
    return ['D9_edges_det_vs_truth']


def fig_sepit(I, ctx):
    sp = I.need('sep_it_det.json', proposed=True)
    st = list(dict.fromkeys(stamps(I) + P.stamps_of(sp)))
    species = [('F', 200.0), ('F', 500.0), ('F', 1000.0), ('F', 1500.0), ('S', 500.0)]
    fig, (ax, rx) = P.figure(ratio=True)
    meas, notm = {}, []
    for key, v in sp['points'].items():
        smp, spin, m, lam, var = key.split('|')
        if var != 'BM':
            continue
        if v.get('measurable', not v.get('pu200')) and smp == 'A1':
            if (spin, float(m)) in species and v.get('err_mm') is not None and v.get('n', 0) >= 5:
                meas.setdefault((spin, float(m)), []).append(v)
        elif not v.get('measurable', True):
            notm.append(v)
    if notm:
        ax.plot([v['sep_truth_median_mm'] for v in notm], [v['sep_det_median_mm'] for v in notm], 'x', ls='none',
                color=P.MUTED, ms=9, mew=2, zorder=1.8,
                label='PU 200 (A2, A5): NOT MEASURABLE (flag)')
    for i, k in enumerate(species):
        V = sorted(meas.get(k, []), key=lambda v: v['sep_truth_median_mm'])
        if not V:
            continue
        xt = np.array([v['sep_truth_median_mm'] for v in V])
        yd = np.array([v['sep_det_median_mm'] for v in V])
        er = np.array([v['err_mm'] for v in V])
        ax.errorbar(xt, yd, yerr=er, fmt=P.MARKERS[i] + '-', lw=1.0, color=P.PALETTE[i],
                    label='A1 (no PU): ' + plabel(*k))
        rx.errorbar(xt, yd / xt, yerr=er / xt, fmt=P.MARKERS[i], color=P.PALETTE[i])
    lim_ = np.array([0.1, 300])
    ax.plot(lim_, lim_, '--', color=P.INK2, label='detector = truth')
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(*lim_); ax.set_ylim(0.13, 3e4)       # PAPER R2 B-4: legend clear of the PU-200 points
    rx.set_xscale('log')
    ax.set_ylabel(r'median $d_{IT}^{det}$ [mm]')            # PAPER R2 B-4: symbol of the note
    rx.axhline(1, color=P.INK2, ls='--')
    rx.set_ylim(0.0, 3.0)
    rx.set_yticks([0.5, 1, 1.5, 2, 2.5])
    rx.set_ylabel('det / truth')
    rx.set_xlabel(r'median truth $d_{IT}$ (Stage 3) [mm]')
    P.log_ticks(rx.xaxis, [0.1, 0.3, 1, 3, 10, 30, 100])
    P.legend(ax, loc='upper left', ncol=1)
    P.label(ax, tag_lines=[r'$d_{IT}\propto\Lambda^{-2}$, core hits, $R_A$ cand.',      # PAPER R2 B-4: 2 lines
                           'A1: n < 5 not drawn; ratio: A1 only'],
            stamps=st, loc='lower right')
    P.save(fig, ctx['out'], 'D10_sepit_calibration', inputs=[I.path('sep_it_det.json', True)],
           stamps=st, code=CODE, meta=dict(level='detector', pu200_measurable=sp.get('pu200_measurable'),
                                           pu200_note=sp.get('pu200_note'), n_A1_drawn=sum(map(len, meas.values())),
                                           n_pu200_not_measurable=len(notm)))
    return ['D10_sepit_calibration']


def fake_road(fk):
    """MET road of the D11 PU-only fake: phi = trials.phimet[trial], half-width trials.delta95[trial] from the fake's
    B1 job file data/acts_stage4/prod/*/B1/<job>.npz (read-only; the frozen event_display.npz has met_phi = null)."""
    job, t = fk.get('job'), fk.get('trial')
    if not job or t is None:
        return None
    cand = sorted((TT / 'data' / 'acts_stage4' / 'prod').glob(f'*/B1/{job}.npz'))
    if not cand:
        return None
    with np.load(cand[0], allow_pickle=False) as d:
        phi = float(d['trials.phimet'][int(t)])
        d95 = float(d['trials.delta95'][int(t)]) if 'trials.delta95' in d.files else float('nan')
        ev = int(d['trials.ev'][int(t)]) if 'trials.ev' in d.files else None
        rd = int(d['trials.road'][int(t)]) if 'trials.road' in d.files else None
    return dict(phi=phi, delta95=d95, ev=ev, road=rd, path=cand[0])


def fig_event_display(I, ctx):
    z = I.need('event_display.npz', proposed=True)
    lab = str(z['label']) if 'label' in z.files else ''
    st = list(dict.fromkeys(stamps(I) + P.stamps_of(lab)))
    try:
        info = json.loads(lab)
    except ValueError:
        info = {}
    fig, ax = P.figure()
    cls = z['cls']
    ren = {'PU (signal event)': 'PU hits, signal cand.', 'quirk': 'quirk hits, signal cand.',   # PAPER R2 B-4: shorter
           'PU-only fake': 'best PU-only fake'}
    nmz = [ren.get(str(n), str(n)) for n in z['cls_names']]
    sty = [dict(color=P.MUTED, ms=5, mfc='none'), dict(color=P.PALETTE[0], ms=10),
           dict(color=P.PALETTE[1], ms=8, marker='s')]
    for c in range(len(nmz)):
        s = cls == c
        kw = dict(sty[c % 3])
        mk = kw.pop('marker', 'o')
        ax.plot(z['x'][s], z['y'][s], mk, ls='none', label=f'{nmz[c]} ({int(s.sum())})', **kw)
    ph = float(np.ravel(z['met_phi'])[0])
    ax.plot([0, 1100 * np.cos(ph)], [0, 1100 * np.sin(ph)], '--', color=P.INK, lw=1.5,
            label='MET (signal event)')
    # REVIEW R1 B2: the fake's own MET road.  event_display.npz stores met_phi = null for the fake (frozen Stage-4
    # products.py looks up 'trials_phimet', a key the B1 job dict never holds); read trials.phimet[trial] and
    # trials.delta95 from the fake's B1 job file instead (read-only).
    fk = info.get('pu_fake', {}) if isinstance(info, dict) else {}
    road = fake_road(fk)
    if road:
        road['dphi_to_signal_met'] = float(abs((road['phi'] - ph + np.pi) % (2 * np.pi) - np.pi))
        fsel = (cls == 2) & (np.hypot(z['x'], z['y']) > 100)
        road['fake_hits_median_phi_r_gt_100mm'] = (float(np.median(np.arctan2(z['y'][fsel], z['x'][fsel])))
                                                   if fsel.any() else None)
        phf, d95 = road['phi'], road['delta95']
        ax.plot([0, 1100 * np.cos(phf)], [0, 1100 * np.sin(phf)], ':', color=P.PALETTE[1], lw=2.5,
                label=rf'MET road, fake ($\pm${d95:g} rad)')
    # square frame; empty band below the hits for the (6-line) tag block, room top-right for the legend
    S = 2.3 * max(np.ptp(z['x']), np.ptp(z['y']), 200.0)     # PAPER R2 B-4: room for the larger legend (right)
    x0, y0 = z['x'].min() - 0.08 * S, z['y'].min() - 0.27 * S
    ax.set_xlim(x0, x0 + S); ax.set_ylim(y0, y0 + S)
    ax.set_aspect('equal', adjustable='datalim')      # equal spans on a square axes: no limit change needed
    ax.set_xlabel('x [mm]'); ax.set_ylabel('y [mm]')
    P.legend(ax, ncol=1, markerscale=1.5)
    sg, pf = info.get('signal', {}), info.get('pu_fake', {})
    tag = ['transverse view, candidate-band hits']
    if sg:
        k = sg.get('key', '').split('|')
        tag.append(f"signal: {plabel(k[1], float(k[2]))}, {lam_txt(float(k[3]))} ({sg.get('depth')} of R01-R14)"
                   if len(k) >= 4 else f"signal: {sg.get('key')}")
    if pf:
        tag += [f"PU-only fake: other event ({pf.get('depth')} of R01-R14)"]   # PAPER R2 B-4: job id in the sidecar only
        if road:
            tag += [rf"fake road {road['dphi_to_signal_met']:.3f} rad from signal MET (chance)"]
    P.label(ax, tag_lines=tag, stamps=st, loc='lower left')
    P.save(fig, ctx['out'], 'D11_event_display', inputs=[I.path('event_display.npz', True)]
           + ([road['path']] if road else []), stamps=st, code=CODE,
           meta=dict(level='detector', events=info, fake_road=({k: v for k, v in road.items() if k != 'path'}
                                                               | dict(source=_rel_tt(road['path'])))
                     if road else 'not found (B1 job file missing)',
                     signal_met_phi=ph))
    return ['D11_event_display']


DETECTOR = [('D1', 'eps(m, Lambda) maps at R_A..R_E and the primary (fallback r_fb) selection', fig_eps_maps),
            ('D2', 'eps vs ladder rung per species-mass', fig_eff_vs_rung),
            ('D3', 'B84 / median B vs rung, SR-T and SR-G, r*', fig_bsum),
            ('D4', 'PU fake-rate extrapolation with closure', fig_pfake),
            ('D5', 'expected limit on N_sig vs Lambda per mass', fig_limit_mu),
            ('D6', 'expected sigma limit vs m (bands) + theory sigma', fig_limit_xsec),
            ('D7', 'expected exclusion / discovery map in (m, Lambda)', fig_excl_map),
            ('D8', 'M_est spectra per mass (R_A and r_fb)', fig_mest),
            ('D9', 'detector-level vs truth edges', fig_edges),
            ('D10', 'sep_IT^det calibration vs truth', fig_sepit),
            ('D11', 'event display (signal in PU 200 vs best PU fake)', fig_event_display)]


# ================================================================================================ truth figures
def u2_thickness(U, pk, ctx):
    from matplotlib.ticker import FixedLocator, FormatStrFormatter, NullFormatter
    V = U['points'][pk]
    cells = V['by_lambda']
    lc = V['lambda_cross_keV']
    spin, m = pk.split('_m')
    fig, (ax, rx) = P.figure(ratio=True)

    def series(key, sub='median_um', esub='err_um'):
        sel = [k for k, c in cells.items() if key in c]
        return (np.array([cells[k]['lam_keV'] for k in sel]), np.array([cells[k][key][sub] for k in sel]),
                np.array([cells[k][key][esub] for k in sel]))
    lb, yb, eb = series('Ds_B')
    eb_tot = np.hypot(eb, np.where(lb > 5, 0.05 * yb, 0.0))       # P-9 +-5 % above 5 keV (as the U-2 panel)
    lm, ym, em = series('Ds_MS'); lbm, ybm, ebm = series('Ds_BM')
    lq, yq, _ = series('quadrature_of_medians_um', 'value', 'err')
    ll, yl, _ = series('linear_sum_of_medians_um', 'value', 'err')
    C = P.PALETTE
    ax.errorbar(lb, yb, yerr=eb_tot, fmt='o', color=C[0], label=r'B only, $\Delta s_{B}$')
    ax.errorbar(lm, ym, yerr=em, fmt='s', color=C[1], label=r'material only (MS), $\Delta s_{MS}$')
    ax.errorbar(lbm, ybm, yerr=ebm, fmt='D', color=C[2], label=r'B + material, $\Delta s_{BM}$')
    ax.plot(lq, yq, '--', color='0.15', label=r'quadrature of medians, $\sqrt{\Delta s_B^2 + \Delta s_{MS}^2}$')
    ax.plot(ll, yl, ':', color='0.45', label=r'linear sum of medians, $\Delta s_B + \Delta s_{MS}$')
    ax.axvline(lc, ymin=0.27, ymax=0.58, color='0.6', lw=1.2, ls='-.', zorder=0)
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_ylabel(r'median plane thickness $\Delta s$ [$\mu$m]')
    allv = np.concatenate([yb, ym, ybm, yl])
    ax.set_ylim(0.3 * allv.min(), 40 * allv.max())
    ax.set_xlim(0.38, 12.0)
    P.legend(ax)
    P.label(ax, truth=True, rlabel=ctx['rlabel'],
            tag_lines=[plabel(spin, int(m)) + r', $|\eta_{pair}| < 1$', rf'dash-dot: $\Lambda_{{cross}}$ = {lc:.2f} keV'],
            x=0.04, y=0.24)
    sel = [k for k, c in cells.items() if 'paired' in c]
    lr = np.array([cells[k]['lam_keV'] for k in sel])
    rq = np.array([cells[k]['paired']['ratio_to_quadrature']['median'] for k in sel])
    erq = np.array([cells[k]['paired']['ratio_to_quadrature']['err'] for k in sel])
    ql = np.array([cells[k]['paired']['linear_sum_expectation_of_ratio']['median'] for k in sel])
    rx.axhline(1.0, color='0.15', ls='--')
    rx.plot(lr, ql, ':', color='0.45')
    rx.errorbar(lr, rq, yerr=erq, fmt='D', color=C[2])
    rx.axvline(lc, color='0.6', lw=1.2, ls='-.', zorder=0)
    rx.set_ylim(0.65, 1.55)
    rx.set_ylabel(r'$\frac{\Delta s_{BM}}{\sqrt{\Delta s_B^2+\Delta s_{MS}^2}}$')
    rx.set_xlabel(r'string tension scale $\Lambda$ [keV]')
    rx.xaxis.set_major_locator(FixedLocator([0.5, 1, 2, 3, 5, 10]))
    rx.xaxis.set_major_formatter(FormatStrFormatter('%g')); rx.xaxis.set_minor_formatter(NullFormatter())
    rx.set_yticks([0.8, 1.0, 1.2, 1.4])
    nm = f'T1_u2_thickness_{pk}'
    P.save(fig, ctx['out'], nm, inputs=[U2], code=CODE,
           meta=dict(level='truth', source='acts/stage4/u2_panel/u2_panel.json (numbers unchanged; restyle only)',
                     point=pk))
    return nm


def u2_ratio(U, mode, ctx):
    from matplotlib.ticker import FixedLocator, FormatStrFormatter, NullFormatter
    fig, ax = P.figure()
    if mode == 'x':
        xx = np.logspace(-2, 3, 400)
        ax.plot(xx, (1 + xx) / np.sqrt(1 + xx ** 2), ':', color='0.45',
                label=r'linear sum (single event), $(1+x)/\sqrt{1+x^2}$')
    ax.axhline(1.0, color='0.15', ls='--', label='quadrature')
    if mode == 'lc':
        ax.axvline(1.0, color='0.6', lw=1.2, ls='-.', zorder=0)
    ncell = 0
    for i, pk in enumerate(U['points']):
        spin, m = pk.split('_m')
        cs = [c for c in U['points'][pk]['by_lambda'].values() if 'paired' in c]
        ncell += len(cs)
        y = np.array([c['paired']['ratio_to_quadrature']['median'] for c in cs])
        ey = np.array([c['paired']['ratio_to_quadrature']['err'] for c in cs])
        if mode == 'x':
            x = np.array([c['paired']['x_B_over_MS']['median'] for c in cs])
            ex = np.array([c['paired']['x_B_over_MS']['err'] for c in cs])
            ax.errorbar(x, y, xerr=ex, yerr=ey, fmt=P.MARKERS[i], color=P.PALETTE[i], label=plabel(spin, int(m)))
        else:
            x = np.array([c['lam_over_cross'] for c in cs])
            ax.errorbar(x, y, yerr=ey, fmt=P.MARKERS[i] + '-', lw=1.0, color=P.PALETTE[i], label=plabel(spin, int(m)))
    ax.set_xscale('log')
    ax.set_ylabel(r'median $\Delta s_{BM}/\sqrt{\Delta s_B^2+\Delta s_{MS}^2}$ (per event)')
    if mode == 'x':
        ax.set_xlabel(r'median $x = \Delta s_B/\Delta s_{MS}$ (per event)')
        ax.set_xlim(0.02, 30); ax.set_ylim(0.6, 1.75)
        ax.xaxis.set_major_locator(FixedLocator([0.03, 0.1, 0.3, 1, 3, 10, 30]))
    else:
        ax.set_xlabel(r'$\Lambda/\Lambda_{cross}$  ($\Delta s_B = \Delta s_{MS}$ at $\Lambda_{cross}$)')
        ax.set_xlim(0.2, 12); ax.set_ylim(0.6, 1.45)
        ax.xaxis.set_major_locator(FixedLocator([0.3, 0.5, 1, 2, 3, 5, 10]))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%g')); ax.xaxis.set_minor_formatter(NullFormatter())
    P.legend(ax, ncol=2)
    P.label(ax, truth=True, rlabel=ctx['rlabel'], tag_lines=[rf'P1, $|\eta_{{pair}}| < 1$, {ncell} cells'],
            loc='lower left')
    nm = 'T2_u2_ratio_vs_x' if mode == 'x' else 'T3_u2_ratio_vs_lamcross'
    P.save(fig, ctx['out'], nm, inputs=[U2], code=CODE,
           meta=dict(level='truth', source='acts/stage4/u2_panel/u2_panel.json (numbers unchanged; restyle only)'))
    return nm


def truth_edges(ctx):
    p = json.loads(P2.read_text())
    tr = p2_edges()
    fits = p['edge_fits_in_m']
    fig, ax = P.figure()
    for i, (e, txt) in enumerate(TRUTH_EDGES):
        for spin, mfc in (('F', None), ('S', 'none')):
            d = sorted(tr.get(e, {}).get(spin, []))
            if not d:
                continue
            ax.errorbar([q[0] for q in d], [q[1] for q in d], yerr=[q[2] or 0 for q in d], fmt=P.MARKERS[i], mfc=mfc,
                        color=P.PALETTE[i], ls='none', label=txt if spin == 'F' else None)
            f = fits.get(f'{spin}/{e}', {})
            fd = f.get('deg2') or f.get('deg1')
            if fd:
                mm = np.linspace(min(q[0] for q in d), max(q[0] for q in d), 100)
                u = np.log(mm / 500.0)
                ax.plot(mm, np.exp(sum(c * u ** k for k, c in enumerate(fd['params']))), '-' if spin == 'F' else ':',
                        color=P.PALETTE[i], lw=1.5)
    ax.plot([], [], 'o', color=P.INK, label='E (filled), smoothed fit: solid')
    ax.plot([], [], 'o', mfc='none', color=P.INK, label=r'$\tilde{E}$ (open), smoothed fit: dotted')
    ax.set_yscale('log')
    ax.set_ylim(0.15, 1500)
    ax.set_xlim(150, 1550)
    ax.set_xlabel(r'quirk mass $m_Q$ [GeV]')
    ax.set_ylabel(r'$\Lambda$ edge [keV]')
    P.legend(ax, ncol=1)
    P.label(ax, truth=True, rlabel=ctx['rlabel'], tag_lines=[r'P2 template half, $|\eta_{pair}| < 2.5$',
                                                             'upper edges: median-separation quantities,',
                                                             'not the comparator of the detector upper edge'],   # PAPER R2: no '(see D9)'
            loc='upper left', y=0.45)                      # empty band between the lower and upper edges
    P.save(fig, ctx['out'], 'T4_truth_edges_vs_mass', inputs=[P2], code=CODE,
           meta=dict(level='truth', source='sim/stage3/results/P2.json edges + edge_fits_in_m (deg2, else deg1)'))
    return 'T4_truth_edges_vs_mass'


# ================================================================================================ driver
def run(entries, ctx):
    index = {}
    for fid, desc, fn in entries:
        try:
            names = fn(ctx)
            index[fid] = dict(desc=desc, status='OK' if names else 'EMPTY', figures=names or [])
        except Skip as e:
            index[fid] = dict(desc=desc, status='SKIPPED', reason=str(e))
        except Exception as e:                                   # noqa: BLE001  (never silent: logged in index)
            index[fid] = dict(desc=desc, status='ERROR', reason=f'{type(e).__name__}: {e}',
                              trace=traceback.format_exc()[-1500:])
        print(f"{fid:4s} {index[fid]['status']:8s} {desc}"
              + (f" -- {str(index[fid].get('reason'))[:300]}" if index[fid].get('reason') else
                 f" ({len(index[fid]['figures'])} figs)"))
    return index


def final_guard(I, res):
    """--final: refuse anything that is not a frozen, non-DEV, real Stage-4 run (placeholder, DEV, dry run, freeze
    mismatch, inputs under stage5/placeholder_inputs).  Returns the list of checks passed (for index.json)."""
    man = I.json('manifest.json') or {}
    why = []
    if 'placeholder_inputs' in str(res) or (I.prop and 'placeholder_inputs' in str(I.prop)):
        why.append('inputs under stage5/placeholder_inputs')
    for n in ('manifest.json', 'signal_eff.json', 'bsum_wp.json', 'limits.json', 'background.json'):
        d = I.json(n) or {}
        st = [x for x in P.stamps_of(d) if x.split()[0] in P.BIG_STAMPS]
        if st:
            why.append(f'{n}: {st}')
        if d.get('dev') or d.get('placeholder') or d.get('_placeholder'):
            why.append(f'{n}: dev/placeholder flag set')
    pv = (I.json('limits.json') or {}).get('provenance') or {}
    if pv.get('freeze_match') is False:
        why.append('limits.json provenance freeze_match = false')
    if why:
        raise SystemExit('REFUSED (--final needs the frozen real Stage-4 outputs): ' + '; '.join(why))
    return ['not placeholder', 'not DEV / dry run', f"freeze_match = {pv.get('freeze_match')}",
            f"freeze {str(pv.get('freeze_sha256'))[:12]}"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', help='Stage-4 results directory (run_all --out) or stage5/placeholder_inputs')
    ap.add_argument('--proposed', help='directory of the schema-v2 extension inputs (acceptance, edges_det, '
                                       'sep_it_det, event_display); default <results>/proposed if it exists, '
                                       'else <results>')
    ap.add_argument('--final', action='store_true',
                    help='final figure set from REAL inputs only (refuses placeholder / DEV / dry-run inputs and '
                         'any stamped figure); default output stage5/figures/final[/truth|/truth_sqrt_s]')
    ap.add_argument('--truth', action='store_true', help='truth-level figures (U-2 panel, P2 truth edges)')
    ap.add_argument('--truth-rlabel', default='full', choices=('full', 'sqrt_s'),
                    help="right label on truth-level figures: 'full' (approved default) or 'sqrt_s' (pending user)")
    ap.add_argument('--out', help='output directory (default stage5/figures/<tag>)')
    ap.add_argument('--only', help='comma-separated figure ids (e.g. D1,D7)')
    a = ap.parse_args(argv)
    try:
        import os
        os.nice(15)
    except OSError:
        pass
    P.style()
    P.FINAL = bool(a.final)
    if not a.results and not a.truth:
        ap.error('give --results and/or --truth')
    allidx = {}
    if a.truth:
        sub = 'truth' if a.truth_rlabel == 'full' else 'truth_sqrt_s'
        out = (Path(a.out) / sub if a.out else HERE / 'figures' / 'final' / sub) if a.final else \
            (Path(a.out) if a.out else HERE / 'figures' / sub)
        ctx = dict(out=out, rlabel=a.truth_rlabel)
        U = json.loads(U2.read_text())
        ent = [(f'T1_{pk}', f'U-2 thickness + ratio panel {pk}', (lambda c, pk=pk: [u2_thickness(U, pk, c)]))
               for pk in U['points']]
        ent += [('T2', 'U-2 ratio vs x = Ds_B/Ds_MS', lambda c: [u2_ratio(U, 'x', c)]),
                ('T3', 'U-2 ratio vs Lambda/Lambda_cross', lambda c: [u2_ratio(U, 'lc', c)]),
                ('T4', 'Stage-3 truth Lambda edges vs mass', lambda c: [truth_edges(c)])]
        if a.only:
            ent = [e for e in ent if e[0].split('_')[0] in a.only.split(',')]
        idx = run(ent, ctx)
        out.mkdir(parents=True, exist_ok=True)
        (out / 'index.json').write_text(json.dumps(dict(level='truth', rlabel=a.truth_rlabel, figures=idx), indent=1))
        allidx['truth'] = idx
    if a.results:
        res = Path(a.results)
        if not res.is_absolute():
            res = TT / res
        I = Inputs(res, a.proposed)
        issues = I.check()
        man = I.json('manifest.json') or {}
        checks = final_guard(I, res) if a.final else []
        tag = 'final' if a.final else ('placeholder' if 'PLACEHOLDER' in str(man.get('label', '')) else res.name)
        out = Path(a.out) if a.out else HERE / 'figures' / tag
        print(f'extension inputs from: {I.prop}; summary: {I.summary_note}')
        if 'acts_stage4' in str(out) or 'acts/stage4' in str(out):
            raise SystemExit('REFUSED: Stage-5 figures are never written under acts/stage4 or data/acts_stage4')
        print(f'schema check: {len(issues)} issue(s)' + ''.join(f'\n  - {s}' for s in issues[:20]))
        ctx = dict(out=out)
        ent = [(fid, desc, (lambda c, fn=fn: fn(I, c))) for fid, desc, fn in DETECTOR]
        if a.only:
            ent = [e for e in ent if e[0] in a.only.split(',')]
        idx = run(ent, ctx)
        out.mkdir(parents=True, exist_ok=True)
        if a.only and (out / 'index.json').is_file():   # partial regeneration: keep the other ids' entries
            old = json.loads((out / 'index.json').read_text()).get('figures', {})
            idx = {**old, **idx}
            idx = {k: idx[k] for k in [d[0] for d in DETECTOR] if k in idx}
        try:
            outcome = I.outcome()
        except Exception as e:                                   # noqa: BLE001
            outcome = dict(error=str(e))
        (out / 'index.json').write_text(json.dumps(dict(
            level='detector', results=_rel_tt(res), extension_inputs=_rel_tt(I.prop), final=bool(a.final),
            final_checks=checks, summary=I.summary_note, stage4_outcome=outcome, schema_issues=issues,
            npz_aliases=NPZ_ALIASES, stamps=P.stamps_of(man), figures=idx), indent=1, default=str))
        allidx['detector'] = idx
    bad = [f for v in allidx.values() for f, d in v.items() if d['status'] == 'ERROR']
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
