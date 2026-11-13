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
Fix pass R1 (2026-10-13; review/FIX_S3_R1.md) added, without changing the nominal edges or stat errors:
  (i) 'syst_robust': every template-weight systematic shift re-evaluated as a bootstrap-averaged PAIRED shift (NB_SYST common
      resamples; shift_b = E_w(b) - E_nom(b), averaged; its std = the shift's sampling error), which removes the jumps of a
      reweighted median on 200 events; totals before ('total') and after ('total_robust');
  (ii) 'sep_IT_handle': median IT pair separation vs Lambda per species-mass (the continuous Lambda handle) and its log-log
      slope; (iii) 'edge_fits_in_m': ln(edge) = a + b ln m (+ c ln^2 m) fits with covariance, the m-slope, and the merge100 edge
      INTERPOLATED (flagged) at the masses without Lambda >= 15 keV points; (iv) 'edge_redundancy'.
Output: sim/stage3/results/P2.json, P2_points.json, figures/p2_*.png.
Run (theory_track/): pixi run python sim/stage3/scripts/p2_results.py
"""
import json

import numpy as np

import s3common as C

R_IT = 14.6
NB = 200
NB_SYST = 40
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
        # fix R1 (constructive B-9): bootstrap-averaged paired systematic shifts (robust against median jumps)
        rngs = np.random.default_rng(777)
        cols = dict(lmax_up=('w', 'lmax_up'), lmax_dn=('w', 'lmax_dn'), qed=('w', 'qed'), qed19=('w', 'qed19'))
        groups = dict(scale9=sc9, scale7=sc7, dynscale=dyn, merging=mrg)
        acc = {k: {e: [] for e in E0} for k in list(cols) + ['scale7_lo', 'scale7_hi', 'dynscale_lo', 'dynscale_hi',
                                                             'merging_lo', 'merging_hi', 'pdf_up', 'pdf_dn']}
        need = sorted(set(sc7) | set(dyn) | set(mrg) | set(pdf))
        for _ in range(NB_SYST):
            ii = rngs.integers(0, n, n)
            Db = {l: {k: (v[ii] if isinstance(v, np.ndarray) else v) for k, v in D[l].items()} for l in lam_list}
            e0b = {k: v[0] for k, v in edges_for(Db, lam_list, W['nominal'][ii], LAMS_LO_REF)[0].items()}
            for wn in cols:
                eb = edges_for(Db, lam_list, W[wn][ii], LAMS_LO_REF)[0]
                for e in E0:
                    acc[wn][e].append(eb[e][0] - e0b[e])
            ec = {j: {k: v[0] for k, v in edges_for(Db, lam_list, wr[ii, j], LAMS_LO_REF)[0].items()} for j in need}
            for g in ('scale7', 'dynscale', 'merging'):
                for e in E0:
                    d_ = [ec[j][e] - e0b[e] for j in groups[g]]
                    acc[g + '_lo'][e].append(np.nanmin(d_)); acc[g + '_hi'][e].append(np.nanmax(d_))
            for e in E0:
                v = np.array([ec[j][e] for j in pdf]).reshape(-1, 2) - e0b[e]
                acc['pdf_up'][e].append(np.sqrt(np.nansum(np.maximum(np.maximum(v[:, 0], v[:, 1]), 0) ** 2)) / 1.645)
                acc['pdf_dn'][e].append(np.sqrt(np.nansum(np.maximum(np.maximum(-v[:, 0], -v[:, 1]), 0) ** 2)) / 1.645)
        syst['robust_shifts'] = {k: {e: dict(mean=float(np.nanmean(v)), sd=float(np.nanstd(v)),
                                             mc_err=float(np.nanstd(v) / np.sqrt(max(np.isfinite(v).sum(), 1))))
                                     for e, v in d_.items()} for k, d_ in acc.items()}
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
            # fix R1 (B-9): same composition rule with the bootstrap-averaged paired shifts
            rs = sy['robust_shifts']
            g = lambda nm: rs[nm][k]['mean'] / x  # noqa: E731
            compr = dict(lmax=max(abs(g('lmax_up')), abs(g('lmax_dn'))), qed_down=abs(min(g('qed19'), 0.0)),
                         scale7=max(abs(g('scale7_lo')), abs(g('scale7_hi'))), dynscale=max(abs(g('dynscale_lo')), abs(g('dynscale_hi'))),
                         pdf=max(g('pdf_up'), g('pdf_dn')), merging=max(abs(g('merging_lo')), abs(g('merging_hi'))), material=comp['material'])
            sd = dict(lmax=max(rs['lmax_up'][k]['sd'], rs['lmax_dn'][k]['sd']) / x, qed_down=rs['qed19'][k]['sd'] / x,
                      pdf=max(rs['pdf_up'][k]['sd'], rs['pdf_dn'][k]['sd']) / x)
            tot[k]['components_rel_robust'] = compr
            tot[k]['robust_shift_sampling_sd_rel'] = sd
            tot[k]['total_rel_robust'] = float(np.sqrt(sum(v ** 2 for v in compr.values())))
        sy['total'] = tot
    # fix R1 (B-8, B-11, critical B-6): continuous handle, redundancy, smooth fits in m with the interpolated merge edges
    res['sep_IT_handle'] = {}
    for (spin, m), lmap in sorted(by.items()):
        ls = [l for l in sorted(lmap) if f'{spin}_m{m}/L{l:g}' in points]
        y = [points[f'{spin}_m{m}/L{l:g}']['sep_IT_med_um']['value'] for l in ls]
        e = [points[f'{spin}_m{m}/L{l:g}']['sep_IT_med_um']['err'] for l in ls]
        lm = [points[f'{spin}_m{m}/L{l:g}']['lmax_med_cm']['value'] * 1e4 for l in ls]
        sel = [i for i, l in enumerate(ls) if 1.0 <= l <= 30.0 and np.isfinite(y[i]) and y[i] > 0]
        sl = np.polyfit(np.log([ls[i] for i in sel]), np.log([y[i] for i in sel]), 1)[0] if len(sel) >= 3 else None
        res['sep_IT_handle'][f'{spin}_m{m}'] = dict(lam_keV=ls, sep_IT_med_um=y, err_um=e,
                                                    loglog_slope_1to30keV=(float(sl) if sl is not None else None),
                                                    ratio_sep_to_lmax_med=[float(a / b) if (b and np.isfinite(a)) else None for a, b in zip(y, lm)])
    fits = {}
    for spin in ('F', 'S'):
        ms_all = sorted(m for (s_, m) in by if s_ == spin)
        for k in EDGE_DEF:
            mm = [m for m in ms_all if np.isfinite(res['edges'][f'{spin}_m{m}'][k]['value'])]
            if len(mm) < 3:
                continue
            x = np.log(mm); yv = np.log([res['edges'][f'{spin}_m{m}'][k]['value'] for m in mm])
            sg = np.array([res['edges'][f'{spin}_m{m}'][k]['stat_err'] / res['edges'][f'{spin}_m{m}'][k]['value'] for m in mm])
            out = {}
            for deg in (1, 2):
                if len(mm) <= deg + 1:
                    continue
                A = np.vander(x - np.log(500.0), deg + 1, increasing=True)
                Wt = 1 / sg ** 2
                cov = np.linalg.inv(A.T @ (A * Wt[:, None])); par = cov @ (A.T @ (Wt * yv))
                chi2 = float(np.sum(Wt * (yv - A @ par) ** 2))
                out[f'deg{deg}'] = dict(params=par.tolist(), cov=cov.tolist(), chi2=chi2, ndf=len(mm) - deg - 1,
                                        x0='ln(500 GeV)', form='ln(edge/keV) = sum_i p_i (ln m - ln 500)^i')
            if 'deg1' in out:
                out['m_slope_dlnE_dlnm'] = out['deg1']['params'][1]; out['m_slope_err'] = float(np.sqrt(out['deg1']['cov'][1][1]))
            if k == 'upper_merge100_hit' and spin == 'F' and 'deg2' in out:
                par = np.array(out['deg2']['params']); cov = np.array(out['deg2']['cov'])
                interp = {}
                for m in ms_all:
                    if m in mm or not (min(mm) < m < max(mm)):
                        continue
                    a = np.vander([np.log(m) - np.log(500.0)], 3, increasing=True)[0]
                    v = float(np.exp(a @ par)); ev = float(v * np.sqrt(a @ cov @ a))
                    interp[f'F_m{m}'] = dict(value=v, err_fit=ev, how='interpolated (deg-2 fit in ln m, stat-weighted; not measured)')
                out['interpolated'] = interp
            fits[f'{spin}/{k}'] = out
    res['edge_fits_in_m'] = fits
    rr = [res['edges'][pk]['upper_lmax100um_closed']['value'] / res['edges'][pk]['lower_lmax_RIT_closed']['value'] for pk in res['edges']]
    res['edge_redundancy'] = dict(
        lmax_pair='lower_lmax_RIT_closed and upper_lmax100um_closed are the SAME median l_max at two thresholds: ratio = '
                  f'sqrt(R_IT/100 um) = {np.sqrt(R_IT / 0.01):.2f} at every mass (measured {min(rr):.2f}-{max(rr):.2f}); one piece of information',
        merge_pair='upper_merge100_hit and upper_merge25_hit are two thresholds on the same IT pair separation (sep_IT ~ 0.5-0.6 l_max); '
                   'and merge100 tracks upper_lmax100um_closed (same m-slope)',
        Nosc1='lower_Nosc1_closed: closed form, m-independent (0.28-0.33 keV)',
        thickness='lower_ds100_hit is the only edge tied to eps_B (B + MS); flat in m',
        continuous='sep_IT ~ Lambda^-2 (l0 = m/Lambda^2) from 1 to 30 keV (sep_IT_handle) is the continuous Lambda meter; Ds_B '
                   'carries Lambda (m-flat) only below ~1.5 keV (MS floor above)')
    C.dump('P2.json', res)
    C.dump('P2_points.json', points)
    figures(res, points, by)


EDGE_LABEL = {'lower_Nosc1_closed': r'$N_{osc}$ = 1 (closed form)', 'lower_lmax_RIT_closed': r'$\ell_{max}$ = $R_{IT}$ (closed form)',
              'lower_ds100_hit': r'$\Delta s$ = 100 $\mu$m (hits)', 'upper_lmax100um_closed': r'$\ell_{max}$ = 100 $\mu$m (closed form)',
              'upper_merge100_hit': r'IT pair separation < 100 $\mu$m (hits)', 'upper_merge25_hit': r'IT pair separation < 25 $\mu$m (hits)'}


def plabel(spin, m):
    return (r'$\tilde{E}$' if spin == 'S' else 'E') + f' {m} GeV'


def figures(res, points, by):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    # edges vs mass (fix R1: physics labels; interpolated merge edges shown open with a cross)
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for spin, mk in (('F', 'o'), ('S', 's')):
        ms = sorted(m for (s, m) in by if s == spin)
        for edge, col in (('lower_Nosc1_closed', 'C0'), ('lower_lmax_RIT_closed', 'C1'),
                          ('lower_ds100_hit', 'C2'), ('upper_lmax100um_closed', 'C3'), ('upper_merge100_hit', 'C5'),
                          ('upper_merge25_hit', 'C6')):
            y = [res['edges'][f'{spin}_m{m}'][edge]['value'] for m in ms]
            e = [res['edges'][f'{spin}_m{m}'][edge]['stat_err'] for m in ms]
            ax.errorbar(ms, y, yerr=e, fmt=mk + ('-' if spin == 'F' else ':'), ms=3.5, lw=0.8, color=col,
                        label=(EDGE_LABEL[edge] if spin == 'F' else None), mfc=('none' if spin == 'S' else col))
    ip = res.get('edge_fits_in_m', {}).get('F/upper_merge100_hit', {}).get('interpolated', {})
    if ip:
        ax.errorbar([int(k.split('_m')[1]) for k in ip], [v['value'] for v in ip.values()], yerr=[v['err_fit'] for v in ip.values()],
                    fmt='x', color='C5', ms=5, lw=0.8, label='IT pair sep. < 100 $\\mu$m: interpolated in ln m (not measured)')
    ax.set_yscale('log'); ax.set_xlabel(r'$m$ [GeV] (filled: E, open: $\tilde{E}$)'); ax.set_ylabel(r'$\Lambda$ edge [keV]')
    ax.legend(fontsize='x-small', loc='upper left', bbox_to_anchor=(1.01, 1.0)); C.fig_label(ax)
    fig.savefig(C.FIG / 'p2_edges_vs_mass.png', dpi=150, bbox_inches='tight'); plt.close(fig)
    # observables vs Lambda at a few masses (fix R1: + IT pair separation, the continuous Lambda handle)
    fig, axs = plt.subplots(2, 4, figsize=(18, 7.5))
    obs = [('N_osc_med', r'median $N_{osc}$ (closed form)', True), ('ds_all_med_um', r'median $\Delta s$ (all layers) [$\mu$m]', True),
           ('sep_IT_med_um', r'median IT pair separation [$\mu$m]', True),
           ('ntrk_med', 'median tracker hits / event', False), ('f_norev', 'f(no visible turn-around)', False),
           ('f_merged100', r'f(IT pair separation < 100 $\mu$m)', False), ('dt_trk_max_med_ns', 'median max hit delay [ns]', True)]
    for ax, (k, lab, lg) in zip(axs.flat, obs):
        for spin, m in (('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)):
            ls = sorted(l for l in by[(spin, m)] if f'{spin}_m{m}/L{l:g}' in points)
            y = [points[f'{spin}_m{m}/L{l:g}'][k]['value'] for l in ls]
            e = [points[f'{spin}_m{m}/L{l:g}'][k]['err'] for l in ls]
            ax.errorbar(ls, y, yerr=e, fmt='.-', lw=0.8, label=plabel(spin, m))
        if k == 'sep_IT_med_um':
            xx = np.array([1.0, 30.0]); ax.plot(xx, 3.8e4 * xx ** -2.0, 'k:', lw=0.8, label=r'$\propto \Lambda^{-2}$')
            ax.legend(fontsize='x-small')
        ax.set_xscale('log'); ax.set_xlabel(r'$\Lambda$ [keV]'); ax.set_ylabel(lab)
        if lg:
            ax.set_yscale('log')
        C.fig_label(ax)
    axs[0, 0].legend(fontsize='x-small')
    axs.flat[-1].axis('off')
    fig.subplots_adjust(hspace=0.42)   # fix R2 (review C-7): top-row x labels no longer overlap the bottom-row tags
    fig.savefig(C.FIG / 'p2_observables.png', dpi=150, bbox_inches='tight'); plt.close(fig)


def figures_only():
    res = json.load(open(C.RES / 'P2.json')); points = json.load(open(C.RES / 'P2_points.json'))
    by = {}
    for k in points:
        pk, lk = k.split('/'); sp, m = pk.split('_m')
        by.setdefault((sp, int(m)), {})[float(lk[1:])] = None
    figures(res, points, by)


if __name__ == '__main__':
    import sys
    figures_only() if '--figures-only' in sys.argv else main()
