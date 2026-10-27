"""p2_results.py -- Stage-3 P2 deliverables (E8, 2026-10-13; plan §1.1, §1.3, §4.3 "P2", §7, §9).  Truth level.

Inputs: data/sim_stage3/summary/events_p2.npz and events_mv.npz (extract.py), data/sim_stage3/inputs/<spin>_m<m>_p2.npz
(weight ratios, read only).  Configuration BM (nominal material), |eta_pair| < 4 propagated, luminous vertex.

Template/toy split: every number here uses the TEMPLATE half only, counted inside |eta_pair| < 2.5 (in_eta25), the
counting set of plan §2.  The toy half is left untouched for the Stage-4 pseudo-experiments (only its event and status
counts are reported).  Events with status != 1 are excluded from hit-level statistics at that Lambda (listed).

1. Per-point summaries vs (m, Lambda): N_osc_vac (closed form) median and f(N_osc < 1); l_max median [cm]; thickness
   ds_all / ds_itps medians [um]; tracker hits per event (both quirks), hits per hit surface, surfaces hit, max crossings
   of one surface; n_rev (hit-level turn-arounds) median and f(n_rev = 0 for both quirks); IT pair separation median and
   the merged fractions f(sep_IT < 100 um), f(< 25 um); timing: median of the max hit delay t - t_vtx - d/c on the
   tracker, f(BTL hit), median BTL delay; status counts.  Errors: bootstrap (200 resamples) on the medians/fractions.
2. Lambda edges per species-mass (interpolated in ln Lambda between grid points; first crossing scanning upward):
   lower: (a) median N_osc_vac = 1 and (b) median l_max = R_IT = 14.6 cm (closed forms; exact Lambda^+-2 scaling, so
          evaluated from the 1 keV events); (d) median ds_all = 100 um (truth-level thickness edge, B + M).  The hit-level
          turn-around fraction f(n_rev = 0) was tried as an oscillation indicator and found Lambda-INDEPENDENT (it measures
          whether the lab radial velocity reverses, a kinematic property: 0.84 at E 200, 0.5 at E 1000, 0.38 at E 1500),
          so it is reported per point but not used as an edge;
   upper: (e) median l_max = 100 um (closed form); (f) hit level f(sep_IT < 100 um) = 0.5 (merging); (g) same at 25 um.
   Bootstrap errors (200 resamples of the template events, the same events at every Lambda).
3. Systematic tilts (plan §7) on every edge and on the per-point medians at a reference subset:
   l_max shape +-5 % (w_lmax_up/dn), QED FSR -1.1 % (w_qed; -1.9 % w_qed_19 covers the stat. error; one-sided),
   scale: 9-point and 7-point envelopes of the merged (mu_R, mu_F) columns (default dynamical scale) and the envelope
   over the 4 alternative dynamical scales; PDF: CT18NLO Hessian asymmetric, 90 % -> 68 % CL (/1.645); merging qCut
   67.5/90 vs 45 GeV; tail rate: normalisation only (+12..+15 / -11..-13 %, VALIDATION §5.1) -> no effect on edges or
   shapes, carried as a yield nuisance; material x0.5 / x2: re-propagated MV points (E 200/500/1000/1500, Etilde 500 x
   0.4/0.6/1/3/10/20 keV, same template events) -> shifts of the hit-level statistics and the implied edge shift
   (local slope at the nominal edge).
Output: sim/stage3/results/P2.json, P2_points.json, figures/p2_*.png.
Run (theory_track/): pixi run python sim/stage3/scripts/p2_results.py
"""
import json

import numpy as np

import s3common as C

R_IT = 14.6
NB = 200
LAMS_LO_REF = 1.0


def wmedian(x, w):
    f = np.isfinite(x) & (w > 0)
    if f.sum() == 0:
        return np.nan
    x = x[f]; w = w[f]
    o = np.argsort(x); xs = x[o]; cw = np.cumsum(w[o]); cw /= cw[-1]
    return float(np.interp(0.5, cw, xs))


def wfrac(cond, valid, w):
    ww = w[valid]
    return float(np.sum(ww[cond[valid]]) / np.sum(ww)) if ww.sum() > 0 else np.nan


def crossing(lams, y, y0, log_y=False):
    """first upward-in-Lambda crossing of y = y0, linear in (ln Lambda, y or ln y)."""
    lams = np.asarray(lams, float); y = np.asarray(y, float)
    ok = np.isfinite(y) & ((y > 0) if log_y else True)
    lams, y = lams[ok], y[ok]
    if len(y) < 2:
        return np.nan, 'insufficient'
    t = np.log(y) - np.log(y0) if log_y else y - y0
    for i in range(len(t) - 1):
        if t[i] == 0:
            return float(lams[i]), 'grid'
        if t[i] * t[i + 1] < 0:
            f = t[i] / (t[i] - t[i + 1])
            return float(np.exp(np.log(lams[i]) + f * (np.log(lams[i + 1]) - np.log(lams[i])))), 'interpolated'
    return np.nan, f'no crossing in [{lams[0]:g}, {lams[-1]:g}] keV (y from {y[0]:.3g} to {y[-1]:.3g}, threshold {y0:g})'


def load_points(S, camp):
    meta = json.loads(str(S['point_meta']))
    keys = list(S['point_keys'])
    by = {}
    for k in keys:
        mt = meta[k]
        by.setdefault((mt['spin'], int(mt['m'])), {})[float(mt['lam'])] = keys.index(k)
    return by, keys, meta


def stats_at(S, idx, ev_order, w):
    """matrix of per-event observables in the order ev_order (template, in_eta25)."""
    sel = np.where(S['point'] == idx)[0]
    pos = {int(e): j for j, e in enumerate(S['ev_index'][sel])}
    take = np.array([sel[pos[e]] if e in pos else -1 for e in ev_order])
    def col(c, dtype=float):
        a = np.full(len(ev_order), np.nan)
        ok = take >= 0
        a[ok] = S[c][take[ok]].astype(float)
        return a
    st = col('status')
    good = st == 1
    d = {c: col(c) for c in ('N_osc_vac', 'ell_max', 'ds_all_um', 'ds_itps_um', 'n_trk0', 'n_trk1', 'hits_per_surf', 'n_surf_hit',
                             'max_cross', 'n_rev0', 'n_rev1', 'sep_IT_um', 'dt_trk_max', 'dt_BTL', 'n_BTL', 'floor_flag')}
    for c in ('ds_all_um', 'ds_itps_um', 'n_trk0', 'n_trk1', 'hits_per_surf', 'n_surf_hit', 'max_cross', 'n_rev0', 'n_rev1',
              'sep_IT_um', 'dt_trk_max', 'dt_BTL', 'n_BTL'):
        d[c][~good] = np.nan
    d['good'] = good; d['status'] = st
    return d


def point_stats(d, w):
    g = d['good']
    ntrk = d['n_trk0'] + d['n_trk1']
    norev = (d['n_rev0'] == 0) & (d['n_rev1'] == 0)
    sep = d['sep_IT_um']
    merged100 = np.where(np.isfinite(sep), sep < 100, False); merged25 = np.where(np.isfinite(sep), sep < 25, False)
    return dict(N_osc_med=wmedian(d['N_osc_vac'], w), f_Nosc_lt1=wfrac(d['N_osc_vac'] < 1, np.isfinite(d['N_osc_vac']), w),
                lmax_med_cm=wmedian(d['ell_max'], w), ds_all_med_um=wmedian(d['ds_all_um'], w),
                ds_itps_med_um=wmedian(d['ds_itps_um'], w), ntrk_med=wmedian(ntrk, w), hits_per_surf_med=wmedian(d['hits_per_surf'], w),
                n_surf_med=wmedian(d['n_surf_hit'], w), max_cross_med=wmedian(d['max_cross'], w),
                n_rev_med=wmedian(0.5 * (d['n_rev0'] + d['n_rev1']), w), f_norev=wfrac(norev, g, w),
                sep_IT_med_um=wmedian(sep, w), f_merged100=wfrac(merged100, g, w), f_merged25=wfrac(merged25, g, w),
                f_sep_nan=wfrac(~np.isfinite(sep), g, w), dt_trk_max_med_ns=wmedian(d['dt_trk_max'], w),
                f_BTL=wfrac(d['n_BTL'] > 0, g, w), dt_BTL_med_ns=wmedian(d['dt_BTL'], w), f_floor=wfrac(d['floor_flag'] > 0, np.isfinite(d['floor_flag']), w))


EDGE_DEF = {
    'lower_Nosc1_closed': ('N_osc_med', 1.0, True),
    'lower_lmax_RIT_closed': ('lmax_med_cm', R_IT, True),
    'lower_ds100_hit': ('ds_all_med_um', 100.0, True),
    'upper_lmax100um_closed': ('lmax_med_cm', 0.01, True),
    'upper_merge100_hit': ('f_merged100', 0.5, False),
    'upper_merge25_hit': ('f_merged25', 0.5, False),
}


def closed_edge(d1, w, which, lam_ref):
    """closed-form edges from the events at lam_ref (exact scaling: l_max ~ Lambda^-2, N_osc ~ Lambda^2)."""
    if which == 'lower_Nosc1_closed':
        return lam_ref / np.sqrt(wmedian(d1['N_osc_vac'], w))
    thr = R_IT if which == 'lower_lmax_RIT_closed' else 0.01
    return lam_ref * np.sqrt(wmedian(d1['ell_max'], w) / thr)


def edges_for(D, lams, w, lam_ref):
    out = {}
    PS = {lam: point_stats(D[lam], w) for lam in lams}
    for name, (key, y0, logy) in EDGE_DEF.items():
        if name.endswith('_closed'):
            out[name] = (float(closed_edge(D[lam_ref], w, name, lam_ref)), 'closed_form')
        else:
            out[name] = crossing(lams, [PS[l][key] for l in lams], y0, log_y=logy)
    return out, PS


def main():
    S = np.load(C.SUMM / 'events_p2.npz')
    by, keys, meta = load_points(S, 'p2')
    MV = np.load(C.SUMM / 'events_mv.npz')
    mvby, mvkeys, mvmeta = load_points(MV, 'mv')
    res = dict(meta=dict(script='sim/stage3/scripts/p2_results.py', truth_level=True, selection='template half, |eta_pair| < 2.5, BM',
                         toy_half='untouched (event/status counts only)', tags=dict(
                             measured='VERIFIED (production, bootstrap stat. errors)',
                             closed_form='ESTIMATE (closed forms of plan §1.1 on the production events)',
                             material_edge_shift='ESTIMATE (local-slope extrapolation from the MV points)')),
               edges={}, systematics={}, toy_counts={})
    points = {}
    for (spin, m), lmap in sorted(by.items()):
        lams = sorted(lmap)
        # template counting set (from the 1 keV point; the same rows at every Lambda)
        i1 = lmap[LAMS_LO_REF]
        sel1 = (S['point'] == i1)
        tmpl = sel1 & (S['tt_split'] == 0) & S['in_eta25']
        ev_order = np.sort(S['ev_index'][tmpl])
        res['toy_counts'][f'{spin}_m{m}'] = dict(n_toy_in_eta25=int(np.sum(sel1 & (S['tt_split'] == 1) & S['in_eta25'])),
                                                 n_template_in_eta25=int(len(ev_order)))
        D = {lam: stats_at(S, lmap[lam], ev_order, None) for lam in lams}
        # rows (for the weight ratios) and the input file
        rows_ev = ev_order
        inp = np.load(C.DATA / 'inputs' / f'{spin}_m{m}_p2.npz')
        wr = inp['wvar_ratio'][rows_ev].astype(float)
        names = [str(x) for x in inp['wvar_names']]
        W = dict(nominal=np.ones(len(ev_order)), lmax_up=inp['w_lmax_up'][rows_ev], lmax_dn=inp['w_lmax_dn'][rows_ev],
                 qed=inp['w_qed'][rows_ev], qed19=inp['w_qed_19'][rows_ev])
        lam_list = [l for l in lams if np.isfinite(D[l]['N_osc_vac']).any()]
        E0, PS0 = edges_for(D, lam_list, W['nominal'], LAMS_LO_REF)
        # bootstrap
        rng = np.random.default_rng(12345)
        bs = {k: [] for k in E0}
        bsp = {l: {k: [] for k in PS0[l]} for l in lam_list}
        n = len(ev_order)
        for _ in range(NB):
            ii = rng.integers(0, n, n)
            Db = {l: {k: (v[ii] if isinstance(v, np.ndarray) else v) for k, v in D[l].items()} for l in lam_list}
            Eb, PSb = edges_for(Db, lam_list, W['nominal'], LAMS_LO_REF)
            for k in E0:
                bs[k].append(Eb[k][0])
            for l in lam_list:
                for k in PSb[l]:
                    bsp[l][k].append(PSb[l][k])
        # per-point table
        for l in lam_list:
            key = f'{spin}_m{m}/L{l:g}'
            pnt = {k: dict(value=v, err=float(np.nanstd(bsp[l][k]))) for k, v in PS0[l].items()}
            st = D[l]['status']
            pnt['n_template'] = int(len(ev_order)); pnt['status_counts'] = np.bincount(st[np.isfinite(st)].astype(int), minlength=6).tolist()
            pnt['max_boost'] = meta[keys[lmap[l]]]['max_boost']
            tl = {}
            for wn in ('lmax_up', 'lmax_dn', 'qed', 'qed19'):
                pw = point_stats(D[l], W[wn])
                tl[wn] = {k: pw[k] for k in ('ds_all_med_um', 'ntrk_med', 'f_merged100', 'sep_IT_med_um', 'dt_trk_max_med_ns', 'lmax_med_cm', 'N_osc_med')}
            pnt['tilts'] = tl
            points[key] = pnt
        # systematics on the edges
        syst = {}
        for wn in ('lmax_up', 'lmax_dn', 'qed', 'qed19'):
            Ew, _ = edges_for(D, lam_list, W[wn], LAMS_LO_REF)
            syst[wn] = {k: Ew[k][0] for k in E0}
        def envelope(cols):
            vals = {k: [] for k in E0}
            for j in cols:
                Ew, _ = edges_for(D, lam_list, wr[:, j], LAMS_LO_REF)
                for k in E0:
                    vals[k].append(Ew[k][0])
            return {k: [float(np.nanmin(v)), float(np.nanmax(v))] for k, v in vals.items()}
        sc9 = [i for i, nm in enumerate(names) if nm.startswith('MUF=') and 'PDF=14400' in nm]
        sc7 = [i for i in sc9 if not (('MUF=0.5' in names[i] and 'MUR=2.0' in names[i]) or ('MUF=2.0' in names[i] and 'MUR=0.5' in names[i]))]
        dyn = [i for i, nm in enumerate(names) if nm.startswith('DYN_SCALE=') and 'MUF=1.0_MUR=1.0' in nm]
        mrg = [i for i, nm in enumerate(names) if nm.startswith('Weight_MERGING=') and not nm.endswith('45.000')]
        pdf = sorted([i for i, nm in enumerate(names) if nm.startswith('MUF=1.0_MUR=1.0_PDF=') and 'PDF=14400' not in nm],
                     key=lambda i: int(names[i].split('PDF=')[1].split('_')[0]))
        syst['scale9'] = envelope(sc9); syst['scale7'] = envelope(sc7); syst['dynscale'] = envelope(dyn); syst['merging'] = envelope(mrg)
        # CT18 Hessian (pairs 2k-1, 2k), asymmetric, /1.645
        vals = {k: [] for k in E0}
        for j in pdf:
            Ew, _ = edges_for(D, lam_list, wr[:, j], LAMS_LO_REF)
            for k in E0:
                vals[k].append(Ew[k][0])
        syst['pdf_ct18_68cl'] = {}
        for k in E0:
            x0 = E0[k][0]; v = np.array(vals[k]).reshape(-1, 2)
            up = np.sqrt(np.nansum(np.maximum(np.maximum(v[:, 0] - x0, v[:, 1] - x0), 0) ** 2)) / 1.645
            dn = np.sqrt(np.nansum(np.maximum(np.maximum(x0 - v[:, 0], x0 - v[:, 1]), 0) ** 2)) / 1.645
            syst['pdf_ct18_68cl'][k] = [float(up), float(dn)]
        res['edges'][f'{spin}_m{m}'] = {k: dict(value=v[0], how=v[1], stat_err=float(np.nanstd(bs[k])),
                                                f_boot_finite=float(np.mean(np.isfinite(bs[k])))) for k, v in E0.items()}
        res['systematics'][f'{spin}_m{m}'] = syst
        # material: MV points (same template events) vs nominal
        if (spin, m) in mvby:
            mat = {}
            for k, mt in mvmeta.items():
                if mt['spin'] != spin or int(mt['m']) != m:
                    continue
                l = float(mt['lam']); cfg = mt['cfg']
                Dm = stats_at(MV, mvkeys.index(k), ev_order, None)
                pm = point_stats(Dm, np.ones(len(ev_order)))
                pn = PS0.get(l)
                mat[f'L{l:g}/{cfg}'] = dict(ds_all_med_um=pm['ds_all_med_um'], ds_nom=pn['ds_all_med_um'] if pn else None,
                                            f_merged100=pm['f_merged100'], f_merged100_nom=pn['f_merged100'] if pn else None,
                                            f_norev=pm['f_norev'], f_norev_nom=pn['f_norev'] if pn else None,
                                            ntrk_med=pm['ntrk_med'], ntrk_nom=pn['ntrk_med'] if pn else None,
                                            sep_IT_med_um=pm['sep_IT_med_um'], sep_nom=pn['sep_IT_med_um'] if pn else None,
                                            n_events_mv=int(np.sum(Dm['good'])))
            res['systematics'][f'{spin}_m{m}']['material'] = mat
        print(f'{spin}_m{m}: ' + ', '.join(f"{k.split('_')[1]}={v[0]:.3g}" for k, v in E0.items()), flush=True)
    # material-induced edge shifts (local slope at nominal; ESTIMATE)
    for pk, sy in res['systematics'].items():
        if 'material' not in sy:
            continue
        sh = {}
        spin, m = pk.split('_m'); m = int(m)
        lams = sorted(by[(spin, m)])
        for edge, key, lam_mv, logy in (('lower_ds100_hit', 'ds_all_med_um', [0.4, 0.6], True),
                                        ('upper_merge100_hit', 'f_merged100', [10.0, 20.0], False)):
            e0 = res['edges'][pk][edge]['value']
            if not np.isfinite(e0):
                continue
            # local slope dy/dlnL at the nominal edge from the two bracketing grid points
            ys = [points[f'{pk}/L{l:g}'][key]['value'] for l in lams]
            j = int(np.searchsorted(lams, e0)); j = min(max(j, 1), len(lams) - 1)
            y_a, y_b = ys[j - 1], ys[j]
            if logy:
                y_a, y_b = np.log(y_a), np.log(y_b)
            slope = (y_b - y_a) / (np.log(lams[j]) - np.log(lams[j - 1]))
            for cfg in ('BMx0.5', 'BMx2'):
                # use the MV Lambda nearest to the edge
                lm = min(lam_mv, key=lambda x: abs(np.log(x / e0)))
                r = sy['material'].get(f'L{lm:g}/{cfg}')
                if not r:
                    continue
                if key == 'ds_all_med_um':
                    dy = np.log(r['ds_all_med_um']) - np.log(r['ds_nom'])
                elif key == 'f_merged100':
                    dy = r['f_merged100'] - r['f_merged100_nom']
                else:
                    dy = r['f_norev'] - r['f_norev_nom']
                sh[f'{edge}/{cfg}'] = dict(lam_used=lm, dy=float(dy), slope=float(slope),
                                           rel_edge_shift=float(np.exp(-dy / slope) - 1) if slope != 0 else None)
        sy['material_edge_shift'] = sh
    # total systematic per edge (relative, quadrature): l_max shape (max |up|,|dn|), QED (w_qed_19, one-sided down),
    # scale 7-point envelope, dynamical-scale envelope, CT18 68 % CL, merging qCut envelope, material (MV mass: its own
    # x0.5/x2 shift; other masses: the largest |shift| over the MV masses of that edge, flagged); tail rate: none (norm.)
    mat_max = {}
    for pk, sy in res['systematics'].items():
        for k, v in sy.get('material_edge_shift', {}).items():
            e = k.split('/')[0]
            if v['rel_edge_shift'] is not None:
                mat_max[e] = max(mat_max.get(e, 0.0), abs(v['rel_edge_shift']))
    for pk, sy in res['systematics'].items():
        tot = {}
        for k, ev in res['edges'][pk].items():
            x = ev['value']
            if not np.isfinite(x):
                continue
            rel = lambda y: (y / x - 1) if (y is not None and np.isfinite(y)) else 0.0  # noqa: E731
            comp = dict(lmax=max(abs(rel(sy['lmax_up'][k])), abs(rel(sy['lmax_dn'][k]))),
                        qed_down=abs(min(rel(sy['qed19'][k]), 0.0)),
                        scale7=max(abs(rel(sy['scale7'][k][0])), abs(rel(sy['scale7'][k][1]))),
                        dynscale=max(abs(rel(sy['dynscale'][k][0])), abs(rel(sy['dynscale'][k][1]))),
                        pdf=max(sy['pdf_ct18_68cl'][k]) / x,
                        merging=max(abs(rel(sy['merging'][k][0])), abs(rel(sy['merging'][k][1]))))
            ms = [abs(v['rel_edge_shift']) for kk, v in sy.get('material_edge_shift', {}).items()
                  if kk.startswith(k + '/') and v['rel_edge_shift'] is not None]
            if k.endswith('_closed'):
                comp['material'] = 0.0; how = 'closed form: no material dependence'
            elif ms:
                comp['material'] = max(ms); how = 'own MV points'
            else:
                comp['material'] = mat_max.get(k, 0.0); how = 'max over MV masses (not run at this mass)'
            tot[k] = dict(components_rel=comp, total_rel=float(np.sqrt(sum(v ** 2 for v in comp.values()))),
                          stat_rel=ev['stat_err'] / x, material_how=how)
        sy['total'] = tot
    C.dump('P2.json', res)
    C.dump('P2_points.json', points)
    figures(res, points, by)


def figures(res, points, by):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # edges vs mass
    fig, ax = plt.subplots(figsize=(7, 4.8))
    for spin, mk, lab in (('F', 'o', 'E'), ('S', 's', 'Etilde')):
        ms = sorted(m for (s, m) in by if s == spin)
        for edge, col in (('lower_Nosc1_closed', 'C0'), ('lower_lmax_RIT_closed', 'C1'),
                          ('lower_ds100_hit', 'C2'), ('upper_lmax100um_closed', 'C3'), ('upper_merge100_hit', 'C5'),
                          ('upper_merge25_hit', 'C6')):
            y = [res['edges'][f'{spin}_m{m}'][edge]['value'] for m in ms]
            e = [res['edges'][f'{spin}_m{m}'][edge]['stat_err'] for m in ms]
            ax.errorbar(ms, y, yerr=e, fmt=mk + ('-' if spin == 'F' else ':'), ms=3.5, lw=0.8, color=col,
                        label=(edge if spin == 'F' else None), mfc=('none' if spin == 'S' else col))
    ax.set_yscale('log'); ax.set_xlabel('m [GeV] (filled: E, open: Etilde)'); ax.set_ylabel('Lambda edge [keV]')
    ax.legend(fontsize='x-small', ncol=2); C.fig_label(ax); ax.set_title('truth level', loc='right', fontsize='small')
    fig.savefig(C.FIG / 'p2_edges_vs_mass.png', dpi=150, bbox_inches='tight'); plt.close(fig)
    # observables vs Lambda at a few masses
    fig, axs = plt.subplots(2, 3, figsize=(14, 7.5))
    obs = [('N_osc_med', 'median N_osc (closed form)', True), ('ds_all_med_um', 'median ds_all [um]', True),
           ('ntrk_med', 'median tracker hits / event', False), ('f_norev', 'f(no visible turn-around)', False),
           ('f_merged100', 'f(IT pair separation < 100 um)', False), ('dt_trk_max_med_ns', 'median max hit delay [ns]', True)]
    for ax, (k, lab, lg) in zip(axs.flat, obs):
        for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)):
            ls = sorted(l for l in by[(spin, m)] if f'{spin}_m{m}/L{l:g}' in points)
            y = [points[f'{spin}_m{m}/L{l:g}'][k]['value'] for l in ls]
            e = [points[f'{spin}_m{m}/L{l:g}'][k]['err'] for l in ls]
            ax.errorbar(ls, y, yerr=e, fmt='.-', lw=0.8, label=f'{"E" if spin == "F" else "Etilde"} {m}')
        ax.set_xscale('log'); ax.set_xlabel('Lambda [keV]'); ax.set_ylabel(lab)
        if lg:
            ax.set_yscale('log')
        C.fig_label(ax); ax.set_title('truth level', loc='right', fontsize='small')
    axs[0, 0].legend(fontsize='x-small')
    fig.savefig(C.FIG / 'p2_observables.png', dpi=150, bbox_inches='tight'); plt.close(fig)


if __name__ == '__main__':
    main()
