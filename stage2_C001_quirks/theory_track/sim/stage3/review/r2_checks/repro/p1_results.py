"""p1_results.py -- Stage-3 P1 results (E8, 2026-10-13; plan §1.2, §4.3 "P1", §5 V2b, §9).  Truth level.

Inputs: data/sim_stage3/summary/events_p1.npz (extract.py), data/sim_stage3/summary/p1_model_mg.npz (p1_model_mg.py),
analytic/predictions.json and analytic/checks/c07_predictions_out.txt (read only; the c07 table is parsed, not typed).
Selection: |eta_pair| < 1, vertex at the origin; Delta_s = plane through the vertex on the 10 virtual T3 barrel layers
(ds_barrel_um, the Stage-1 definition).  Events with status != 1 or non-finite Delta_s are dropped per configuration
(listed counts); paired quantities use events valid in both configurations.

Per point (E 200/500/1000/1500, Etilde 500) and Lambda (0.45 ... 10 keV):
  Ds_B (B), Ds_MS (M), Ds_B+M (BM): median +- bootstrap (1000 resamples, seed 12345);
  c2 = (2 Ds(B0/2)/Ds(B0) - 1)/ln 2 per event (Stage-1 convention; Lambda <= 5 keV); R(1/2) = 2 Ds(B0/2)/Ds(B0);
  Lambda exponents between adjacent Lambda: median per-event slope and population slope (ratio of medians);
  C = 1/median(c2) - ln(1/eps_B) (thickness_law_v4);  material exponent ln[Ds(Mx2)/Ds(Mx0.5)]/ln 4 (1, 3 keV) vs 0.517.
Predictions: (i) predictions.json / c07 (T3-cache sample, E 200/500/1000 only); (ii) re-derived on the SAME MG events:
  median c_ev (closed form per event, in the files), the c06 rotating-yo-yo model Ds (p1_model_mg), -2 + 2 c_ev,
  1 + c_ev ln 2, median C_ev.  Pull convention of NEAR_MISS §9: pull = (prediction - measurement)/sigma_meas.
Precision floor: floor_flag = b_odd/l0 < 1e-7 per event.  A B-only number is NOT stated (value withheld, 'floor-dominated')
  where >= 50 % of the events are flagged; where 0 < f < 50 % the median of the unflagged events is also given.
  Above 5 keV every B-only number carries the unattributed +-5 % (P-9) as a systematic.
V2b revisit (full P1 statistics, Lambda <= 5 keV, 30 cells): population Dc = median(c2) - median(c_ev), paired median and
  mean of r = c2 - c_ev, the k_B >= 6 population, and the median shift expected from the per-event scatter alone
  (permutation: median(c_ev + r_perm) - median(c_ev), r permuted across events, 300 permutations).
Fix pass R1 (2026-10-13; review/FIX_S3_R1.md) added, without changing any earlier number: paired per-event Ds_B/model ratios
  (cell, unflagged, gamma* bins), exponent pulls vs the full MG model, median l_max/R_IT per cell, MS-exponent chi2,
  per-event B/MS combination BM/sqrt(B^2+M^2) and the B = MS crossover, the V2b regime split; V2b figure x-axis = the
  zero-median symmetric-scatter model (the stratified permutation is a near-identity, shown grey).
Output: sim/stage3/results/P1.json, figures/p1_*.png.  Run (theory_track/): pixi run python sim/stage3/scripts/p1_results.py
"""
import json
import re

import numpy as np

import s3common as C

POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
LAMS = [0.45, 0.6, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]
NB = 1000
RNG_SEED = 12345
B_LOW = 6.0


def boot(fn, *arrs, nb=NB, seed=RNG_SEED):
    rng = np.random.default_rng(seed)
    n = len(arrs[0])
    if n < 3:
        return np.nan
    return float(np.std([fn(*[a[i] for a in arrs]) for i in (rng.integers(0, n, n) for _ in range(nb))]))


def med_err(x):
    x = x[np.isfinite(x)]
    return (float(np.median(x)), boot(np.median, x)) if len(x) else (np.nan, np.nan)


def parse_c07():
    txt = open(C.TT / 'analytic' / 'checks' / 'c07_predictions_out.txt').read()
    out = {}
    for blk in txt.split('=== m = ')[1:]:
        m = int(blk.split(' GeV')[0])
        d = {}
        for line in blk.splitlines():
            mm = re.match(r'\s*([\d.]+) \|\s+([\d.e+-]+) \(.*?\) \| ([\d.]+) ', line)
            if mm:
                d[float(mm.group(1))] = dict(ds_model_um=float(mm.group(2)), c_ev_median=float(mm.group(3)))
        out[m] = d
    return out


def main():
    S = np.load(C.SUMM / 'events_p1.npz')
    keys = list(S['point_keys'])
    MG = np.load(C.SUMM / 'p1_model_mg.npz')
    preds = json.load(open(C.TT / 'analytic' / 'predictions.json'))
    c07 = parse_c07()
    cj = preds['c']['values_median']
    Cj = preds['thickness_law_v4']['C_population']

    def get(spin, m, lam, cfg):
        k = f'p1/{spin}_m{m}/L{lam:g}_{cfg}'
        if k not in keys:
            return None
        sel = S['point'] == keys.index(k)
        o = np.argsort(S['ev_index'][sel], kind='stable')
        d = {c: S[c][sel][o] for c in ('ev_index', 'row', 'ds_barrel_um', 'status', 'c_ev', 'C_ev', 'k_B', 'eps_B',
                                       'floor_flag', 'gstar', 'bodd_l0', 'nsteps', 'ell_max')}
        d['ok'] = (d['status'] == 1) & np.isfinite(d['ds_barrel_um']) & (d['ds_barrel_um'] > 0)
        return d

    def model_mg(spin, m, lam, rows):
        sel = (MG['point'] == f'{spin}_m{m}') & np.isclose(MG['lam'], lam)
        mp = dict(zip(MG['row'][sel].tolist(), MG['ds_model_um'][sel].tolist()))
        return np.array([mp.get(int(r), np.nan) for r in rows])

    res = dict(meta=dict(script='sim/stage3/scripts/p1_results.py', truth_level=True, tags=dict(
        measured='VERIFIED (measured on the production; statistical error = bootstrap)',
        predictions_json='UNVERIFIED here (transcribed by program from analytic/; E1 status as stated there)',
        mg_rederived='ESTIMATE (closed form / rotating-yo-yo model evaluated on the MG events)'),
        pull='(prediction - measurement)/sigma_meas', floor_rule='B-only value withheld if f(floor_flag) >= 0.5'),
        points={}, v2b_revisit={}, vacuum={}, material_scaling={})
    excl = {}
    for spin, m in POINTS:
        pk = f'{spin}_m{m}'
        P = {}
        for lam in LAMS:
            row = dict()
            b = get(spin, m, lam, 'B'); h = get(spin, m, lam, 'B2'); mm_ = get(spin, m, lam, 'M'); bm = get(spin, m, lam, 'BM')
            for nm, d in (('B', b), ('B2', h), ('M', mm_), ('BM', bm)):
                if d is not None:
                    excl[f'{pk}/L{lam:g}/{nm}'] = dict(n=len(d['ok']), n_dropped=int((~d['ok']).sum()),
                                                      status=np.bincount(d['status'].astype(int), minlength=6).tolist())
            ref = b if b is not None else mm_
            ff = float(np.mean(ref['floor_flag'])) if b is not None else None
            row['n_events'] = len(ref['ok'])
            if b is not None:
                ok = b['ok']
                ds = b['ds_barrel_um'][ok]
                med, err = med_err(ds)
                withheld = ff >= 0.5
                mgm = model_mg(spin, m, lam, b['row'][ok])
                row['Ds_B'] = dict(median_um=None if withheld else med, err_um=None if withheld else err,
                                   median_raw_um=med, err_raw_um=err, f_floor_flag=ff, withheld_floor_dominated=bool(withheld),
                                   median_unflagged_um=(med_err(ds[~b['floor_flag'][ok]])[0] if ff > 0 else None),
                                   syst_unattributed_rel=(0.05 if lam > 5 else 0.0),
                                   pred_T3_model_um=c07.get(m, {}).get(lam, {}).get('ds_model_um') if spin == 'F' else None,
                                   pred_MG_model_um=float(np.nanmedian(mgm)), pred_MG_model_err_um=boot(np.nanmedian, mgm),
                                   median_ratio_to_MG_model_per_event=float(np.nanmedian(ds / mgm)))
                # fix R1 (B-2): paired per-event ratio measured/model on the same events, bootstrap error, pull vs 1
                q = ds / mgm; fq = np.isfinite(q)
                pr, pe = med_err(q[fq])
                row['Ds_B'].update(paired_ratio_MG_model=pr, paired_ratio_err=pe, paired_ratio_pull=(pr - 1) / pe if pe > 0 else None,
                                   paired_ratio_n_model_zero=int((~fq).sum()),
                                   paired_ratio_unflagged=(med_err(q[fq & ~b['floor_flag'][ok]]) if ff > 0 else None))
                row['ell_max_over_R_IT_median'] = float(np.median(b['ell_max'][ok]) / 14.6)
                for t in ('pred_T3_model_um', 'pred_MG_model_um'):
                    pv = row['Ds_B'][t]
                    row['Ds_B']['pull_' + t[5:]] = (pv - med) / err if (pv is not None and err > 0) else None
                row['c_ev_median_MG'] = float(np.median(b['c_ev'][ok]))
                row['C_ev_median_MG'] = float(np.median(b['C_ev'][ok]))
            if b is not None and h is not None:
                ok = b['ok'] & h['ok']
                R2 = 2 * h['ds_barrel_um'][ok] / b['ds_barrel_um'][ok]
                c2 = (R2 - 1) / np.log(2)
                cev = b['c_ev'][ok]; kB = b['k_B'][ok]
                r = c2 - cev
                mc, ec = med_err(c2)
                cjv = cj.get(f'm{m}', {}).get(f'{lam:g}keV') if spin == 'F' else None
                epsB = float(np.median(b['eps_B'][ok]))
                row['c'] = dict(n=int(ok.sum()), median_c2=mc, err=ec, median_c_ev_MG=float(np.median(cev)),
                                pred_json=cjv, pull_json=((cjv - mc) / ec if cjv is not None else None),
                                pull_MG=(float(np.median(cev)) - mc) / ec,
                                Dc_pop=float(np.median(c2) - np.median(cev)),
                                sigma_Dc=boot(lambda a, b_: np.median(a) - np.median(b_), c2, cev),
                                rel_Dc_pop=float((np.median(c2) - np.median(cev)) / np.median(cev)),
                                paired_median_r=float(np.median(r)), paired_median_r_err=boot(np.median, r),
                                paired_mean_r=float(np.mean(r)), paired_mean_r_err=float(np.std(r) / np.sqrt(len(r))),
                                robust_sigma_r=float(1.4826 * np.median(np.abs(r - np.median(r)))),
                                C_measured=float(1 / mc - np.log(1 / epsB)), C_pred_json=(Cj.get(f'm{m}') if spin == 'F' else None),
                                C_ev_median_MG=float(np.median(b['C_ev'][ok])))
                rng = np.random.default_rng(RNG_SEED)
                perm = [np.median(cev + rng.permutation(r)) - np.median(cev) for _ in range(300)]
                # stratified permutation: r permuted only among events in the same c_ev decile (keeps the
                # heteroscedasticity, removes any within-decile correlation) -> the median shift that per-event scatter
                # with the observed conditional distribution produces
                dec = np.digitize(cev, np.quantile(cev, np.linspace(0, 1, 11)[1:-1]))
                sperm = []
                for _ in range(300):
                    rp = r.copy()
                    for sdec in np.unique(dec):
                        ii = np.where(dec == sdec)[0]; rp[ii] = r[rng.permutation(ii)]
                    sperm.append(np.median(cev + rp) - np.median(cev))
                # symmetric zero-median scatter: within gamma* bins, r centred on its bin median and given random signs
                gb = np.digitize(b['gstar'][ok], [1.05, 1.15, 1.3, 1.6, 2.0])
                r0 = r.copy()
                for sg in np.unique(gb):
                    r0[gb == sg] -= np.median(r[gb == sg])
                sym = [np.median(cev + r0 * rng.choice([-1.0, 1.0], len(r0))) - np.median(cev) for _ in range(300)]
                lo = kB < B_LOW
                row['c']['scatter_expected_Dc'] = float(np.mean(perm))
                row['c']['scatter_expected_Dc_spread'] = float(np.std(perm))
                row['c']['strat_perm_expected_Dc'] = float(np.mean(sperm))
                row['c']['zero_median_symmetric_scatter_Dc'] = float(np.mean(sym))
                row['c']['residual_by_kB'] = {f'[{a:g},{bb:g})': dict(n=int(np.sum((kB >= a) & (kB < bb))),
                                                                      median_rel_r=float(np.median((r / cev)[(kB >= a) & (kB < bb)])))
                                              for a, bb in ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9)) if np.sum((kB >= a) & (kB < bb)) >= 3}
                row['c']['kB_lt6'] = dict(n=int(lo.sum()), median_c2=float(np.median(c2[lo])), median_c_ev=float(np.median(cev[lo])),
                                          Dc_pop=float(np.median(c2[lo]) - np.median(cev[lo])),
                                          sigma_Dc=boot(lambda a, b_: np.median(a) - np.median(b_), c2[lo], cev[lo]),
                                          paired_median_r=float(np.median(r[lo])), robust_sigma_r=float(1.4826 * np.median(np.abs(r[lo] - np.median(r[lo])))))
                if (~lo).sum() >= 3:
                    row['c']['kB_ge6'] = dict(n=int((~lo).sum()), frac=float(np.mean(~lo)), median_c2=float(np.median(c2[~lo])),
                                              median_c_ev=float(np.median(cev[~lo])), paired_median_r=float(np.median(r[~lo])),
                                              paired_mean_r=float(np.mean(r[~lo])),
                                              robust_sigma_r=float(1.4826 * np.median(np.abs(r[~lo] - np.median(r[~lo])))),
                                              frac_r_gt_0=float(np.mean(r[~lo] > 0)))
                else:
                    row['c']['kB_ge6'] = dict(n=int((~lo).sum()), frac=float(np.mean(~lo)))
                mR, eR = med_err(R2)
                Rj = None
                if spin == 'F' and m == 500 and lam == 1.0:
                    Rj = 1.072
                elif spin == 'F' and m == 1000 and lam == 1.0:
                    Rj = 1.069
                elif spin == 'F' and m == 500 and lam == 3.0:
                    Rj = 1.059
                elif cjv is not None:
                    Rj = 1 + cjv * np.log(2)
                row['R_half'] = dict(median=mR, err=eR, pred_MG=float(np.median(1 + cev * np.log(2))), pred_json=Rj,
                                     pred_json_note='P-13/P-14 table where given (500 GeV 1/3 keV, 1000 GeV 1 keV), else 1 + c_json ln 2',
                                     pull_json=((Rj - mR) / eR if Rj is not None else None),
                                     pull_MG=(float(np.median(1 + cev * np.log(2))) - mR) / eR)
            for nm, d in (('Ds_MS', mm_), ('Ds_BM', bm)):
                if d is not None:
                    med, err = med_err(d['ds_barrel_um'][d['ok']])
                    row[nm] = dict(median_um=med, err_um=err, n=int(d['ok'].sum()))
            if b is not None and mm_ is not None and 'Ds_B' in row:
                row['MS_dominates'] = bool(row['Ds_MS']['median_um'] > row['Ds_B']['median_raw_um'])
            if b is not None and mm_ is not None and bm is not None:
                # fix R1 (B-4): per-event combination of B and MS on the same rows (VERIFIED, measured)
                dB = dict(zip(b['row'][b['ok']].tolist(), b['ds_barrel_um'][b['ok']].tolist()))
                dM = dict(zip(mm_['row'][mm_['ok']].tolist(), mm_['ds_barrel_um'][mm_['ok']].tolist()))
                dBM = dict(zip(bm['row'][bm['ok']].tolist(), bm['ds_barrel_um'][bm['ok']].tolist()))
                rr_ = sorted(set(dB) & set(dM) & set(dBM))
                quad = np.array([dBM[q] / np.hypot(dB[q], dM[q]) for q in rr_]); lin = np.array([dBM[q] / (dB[q] + dM[q]) for q in rr_])
                mq, eq = med_err(quad)
                row['B_MS_combination'] = dict(n=len(rr_), median_BM_over_quadrature=mq, err=eq, median_BM_over_linear=float(np.median(lin)))
            P[f'L{lam:g}'] = row
        # exponents
        ex = {}
        for la, lb in list(zip(LAMS[:-1], LAMS[1:])) + [(5.0, 10.0), (1.0, 3.0), (3.0, 10.0)]:
            A = get(spin, m, la, 'B'); Bq = get(spin, m, lb, 'B')
            if A is None or Bq is None:
                continue
            assert np.array_equal(A['row'][:min(len(A['row']), len(Bq['row']))], Bq['row'][:min(len(A['row']), len(Bq['row']))])
            n = min(len(A['row']), len(Bq['row']))
            ok = A['ok'][:n] & Bq['ok'][:n]
            a = A['ds_barrel_um'][:n][ok]; b_ = Bq['ds_barrel_um'][:n][ok]
            sl = np.log(b_ / a) / np.log(lb / la)
            pop = lambda x, y: np.log(np.median(y) / np.median(x)) / np.log(lb / la)  # noqa: E731
            pred_ev = -2 + 2 * 0.5 * (A['c_ev'][:n][ok] + Bq['c_ev'][:n][ok])
            ma = model_mg(spin, m, la, A['row'][:n][ok]); mb = model_mg(spin, m, lb, A['row'][:n][ok])
            okm = np.isfinite(ma) & np.isfinite(mb)
            ff = max(float(np.mean(A['floor_flag'][:n])), float(np.mean(Bq['floor_flag'][:n])))
            c7 = c07.get(m, {}) if spin == 'F' else {}
            p_c07 = (np.log(c7[lb]['ds_model_um'] / c7[la]['ds_model_um']) / np.log(lb / la)) if (la in c7 and lb in c7) else None
            med_sl = float(np.median(sl)); e_sl = boot(np.median, sl)
            ex[f'{la:g}to{lb:g}'] = dict(n=int(ok.sum()), median_event_slope=med_sl, err=e_sl, population_slope=float(pop(a, b_)),
                                         population_err=boot(pop, a, b_), pred_MG_event_median=float(np.median(pred_ev)),
                                         pull_MG=(float(np.median(pred_ev)) - med_sl) / e_sl,
                                         pred_MG_model_population=float(pop(ma[okm], mb[okm])),
                                         pull_MG_model_population=float((pop(ma[okm], mb[okm]) - pop(a, b_)) / boot(pop, a, b_)),
                                         pred_T3_model_population=p_c07, f_floor_max=ff,
                                         withheld_floor_dominated=bool(ff >= 0.5))
        res['points'][pk] = dict(by_lambda=P, exponents=ex)
        # vacuum and material scaling
        for lam in (1.0, 3.0):
            v = get(spin, m, lam, 'V')
            if v is not None:
                res['vacuum'][f'{pk}/L{lam:g}'] = dict(n=len(v['ok']), max_ds_um=float(np.nanmax(v['ds_barrel_um'])),
                                                       median_ds_um=float(np.nanmedian(v['ds_barrel_um'])),
                                                       status=np.bincount(v['status'].astype(int), minlength=6).tolist())
            ms = {}
            for cfg in ('Mx0.5', 'M', 'Mx2', 'BMx0.5', 'BM', 'BMx2'):
                d = get(spin, m, lam, cfg)
                ms[cfg] = med_err(d['ds_barrel_um'][d['ok']])
            okp = None
            d05 = get(spin, m, lam, 'Mx0.5'); d2 = get(spin, m, lam, 'Mx2')
            okp = d05['ok'] & d2['ok']
            sl = np.log(d2['ds_barrel_um'][okp] / d05['ds_barrel_um'][okp]) / np.log(4)
            pop = lambda x, y: np.log(np.median(y) / np.median(x)) / np.log(4)  # noqa: E731
            res['material_scaling'][f'{pk}/L{lam:g}'] = dict(
                medians_um={k: v[0] for k, v in ms.items()}, errs_um={k: v[1] for k, v in ms.items()},
                M_exponent_population=float(pop(d05['ds_barrel_um'][okp], d2['ds_barrel_um'][okp])),
                M_exponent_population_err=boot(pop, d05['ds_barrel_um'][okp], d2['ds_barrel_um'][okp]),
                M_exponent_event_median=float(np.median(sl)), pred=0.517,
                BM_ratio_x2_over_x05=ms['BMx2'][0] / ms['BMx0.5'][0])
    res['dropped_events'] = {k: v for k, v in excl.items() if v['n_dropped']}
    # fix R1 (B-2, constructive c9): paired Ds_B/model ratio in gamma* bins, pooled over Lambda <= 5 keV, per point
    gbins = (1.0, 1.05, 1.15, 1.3, 1.6, 100.0)
    res['paired_model_by_gstar'] = {}
    for spin, m in POINTS:
        qq, gg = [], []
        for lam in LAMS[:6]:
            b = get(spin, m, lam, 'B'); ok = b['ok']
            mgm = model_mg(spin, m, lam, b['row'][ok]); q = b['ds_barrel_um'][ok] / mgm; fq = np.isfinite(q)
            qq += list(q[fq]); gg += list(b['gstar'][ok][fq])
        qq = np.array(qq); gg = np.array(gg)
        res['paired_model_by_gstar'][f'{spin}_m{m}'] = dict(median_gstar=float(np.median(gg)), bins={
            f'[{a:g},{bb:g})': dict(n=int(((gg >= a) & (gg < bb)).sum()), median_ratio=med_err(qq[(gg >= a) & (gg < bb)])[0],
                                    err=med_err(qq[(gg >= a) & (gg < bb)])[1]) for a, bb in zip(gbins[:-1], gbins[1:]) if ((gg >= a) & (gg < bb)).sum() >= 10})
    # fix R1 (B-4): B = MS crossover (log-log interpolation of the medians) and the MS-exponent chi2 vs 0.517
    res['B_MS_crossover_keV'] = {}
    for spin, m in POINTS:
        v = res['points'][f'{spin}_m{m}']['by_lambda']
        L = [l for l in LAMS if 'Ds_B' in v[f'L{l:g}']]
        d = [np.log(v[f'L{l:g}']['Ds_B']['median_raw_um'] / v[f'L{l:g}']['Ds_MS']['median_um']) for l in L]
        x = None
        for i in range(len(L) - 1):
            if d[i] > 0 >= d[i + 1]:
                x = float(np.exp(np.log(L[i]) + (np.log(L[i + 1]) - np.log(L[i])) * d[i] / (d[i] - d[i + 1])))
                break
        res['B_MS_crossover_keV'][f'{spin}_m{m}'] = x
    msv = [(v['M_exponent_population'] - 0.517) / v['M_exponent_population_err'] for v in res['material_scaling'].values()]
    res['material_scaling_chi2'] = dict(chi2=float(np.sum(np.square(msv))), ndf=len(msv), pulls=[float(x) for x in msv],
                                        note='population exponents vs the single-point code-scaling check 0.517 (S_msscale, 500 GeV, 3 keV)')
    # P-15 (m dependence) and P-24 (scalar/fermion) per Lambda
    p15 = {}; p24 = {}
    for lam in LAMS:
        meds = [res['points'][f'F_m{m}']['by_lambda'][f'L{lam:g}'].get('Ds_B', {}).get('median_raw_um') for m in (200, 500, 1000, 1500)]
        if all(x is not None for x in meds):
            p15[f'L{lam:g}'] = dict(medians_um=meds, slope_dln_dlnm=float(np.polyfit(np.log([200, 500, 1000, 1500]), np.log(meds), 1)[0]))
        f5 = res['points']['F_m500']['by_lambda'][f'L{lam:g}'].get('Ds_B'); s5 = res['points']['S_m500']['by_lambda'][f'L{lam:g}'].get('Ds_B')
        if f5 and s5:
            rr = s5['median_raw_um'] / f5['median_raw_um']
            p24[f'L{lam:g}'] = dict(ratio=rr, err=rr * np.hypot(s5['err_raw_um'] / s5['median_raw_um'], f5['err_raw_um'] / f5['median_raw_um']),
                                    pred_model=36.0 / 31.0 if lam == 1.0 else None,
                                    pred_MG_model=s5['pred_MG_model_um'] / f5['pred_MG_model_um'])
    res['P15_m_dependence'] = p15
    res['P15_model_T3_1keV_um'] = preds['accumulation']['model_median_Ds_um_1keV']
    res['P24_scalar_over_fermion_500'] = p24
    # V2b revisit: summary over all cells
    cells = []
    for pk, v in res['points'].items():
        for lk, row in v['by_lambda'].items():
            if 'c' in row:
                c = row['c']
                cells.append(dict(point=pk, lam=float(lk[1:]), rel=c['rel_Dc_pop'], Dc=c['Dc_pop'], sig=c['sigma_Dc'],
                                  pull=c['Dc_pop'] / c['sigma_Dc'], paired=c['paired_median_r'], paired_err=c['paired_median_r_err'],
                                  mean_r=c['paired_mean_r'], mean_r_err=c['paired_mean_r_err'], scatter=c['scatter_expected_Dc'],
                                  strat=c['strat_perm_expected_Dc'], sym=c['zero_median_symmetric_scatter_Dc'],
                                  frac_kB6=c['kB_ge6'].get('frac'), Dc_lt6=c['kB_lt6']['Dc_pop'], sig_lt6=c['kB_lt6']['sigma_Dc'],
                                  rel_lt6=c['kB_lt6']['Dc_pop'] / c['kB_lt6']['median_c_ev'], cev=c['median_c_ev_MG'],
                                  pass_1p5=bool(abs(c['Dc_pop']) <= 2 * c['sigma_Dc'] and abs(c['rel_Dc_pop']) <= 0.015)))
    # pooled (5 points) median relative residual per k_B bin and Lambda
    pooled_kb = {}
    for lam in (0.45, 0.6, 1.0, 2.0, 3.0, 5.0):
        rr = []; kk = []
        for spin, m in POINTS:
            b_ = None
            sel_b = S['point'] == keys.index(f'p1/{spin}_m{m}/L{lam:g}_B'); sel_h = S['point'] == keys.index(f'p1/{spin}_m{m}/L{lam:g}_B2')
            ob = np.argsort(S['ev_index'][sel_b]); oh = np.argsort(S['ev_index'][sel_h])
            db = S['ds_barrel_um'][sel_b][ob]; dh = S['ds_barrel_um'][sel_h][oh]
            okk = (S['status'][sel_b][ob] == 1) & (S['status'][sel_h][oh] == 1) & (db > 0)
            ce = S['c_ev'][sel_b][ob]
            rr += list((((2 * dh / db - 1) / np.log(2) - ce) / ce)[okk]); kk += list(S['k_B'][sel_b][ob][okk])
        rr = np.array(rr); kk = np.array(kk)
        pooled_kb[f'L{lam:g}'] = {f'[{a:g},{bb:g})': dict(n=int(np.sum((kk >= a) & (kk < bb))), median_rel_r=float(np.median(rr[(kk >= a) & (kk < bb)])),
                                                          err=boot(np.median, rr[(kk >= a) & (kk < bb)]),
                                                          robust_sigma=float(1.4826 * np.median(np.abs(rr[(kk >= a) & (kk < bb)] - np.median(rr[(kk >= a) & (kk < bb)])))))
                                  for a, bb in ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9))}
    rel = np.array([x['rel'] for x in cells]); w = np.array([(x['cev'] / x['sig']) ** 2 for x in cells])
    rel_lt6 = np.array([x['rel_lt6'] for x in cells]); w6 = np.array([(x['cev'] / x['sig_lt6']) ** 2 for x in cells])
    sc = np.array([x['scatter'] / x['cev'] for x in cells])
    res['v2b_revisit'] = dict(
        cells=cells, n_cells=len(cells), n_pass_P10_criterion=int(sum(x['pass_1p5'] for x in cells)),
        rel_excess_weighted_mean=float(np.sum(w * rel) / np.sum(w)), rel_excess_weighted_err=float(1 / np.sqrt(np.sum(w))),
        rel_excess_range=[float(rel.min()), float(rel.max())],
        rel_excess_kB_lt6_weighted_mean=float(np.sum(w6 * rel_lt6) / np.sum(w6)), rel_excess_kB_lt6_err=float(1 / np.sqrt(np.sum(w6))),
        scatter_expected_rel_mean=float(np.mean(sc)), scatter_expected_rel_range=[float(sc.min()), float(sc.max())],
        corr_rel_vs_scatter=float(np.corrcoef(rel, sc)[0, 1]),
        corr_rel_vs_scatter_note='near-tautological (the unstratified permutation keeps the median of r); not evidence (fix R1, critical B-1)',
        regime_split={nm: dict(lams=ls, rel_excess_weighted_mean=float(np.sum((w * rel)[sel_]) / np.sum(w[sel_])),
                                rel_excess_weighted_err=float(1 / np.sqrt(np.sum(w[sel_]))),
                                rel_excess_kB_lt6_weighted_mean=float(np.sum((w6 * rel_lt6)[sel_]) / np.sum(w6[sel_])),
                                zero_median_sym_rel_mean=float(np.mean(np.array([x['sym'] / x['cev'] for x in cells])[sel_])))
                      for nm, ls in (('0.45 keV (law fails)', [0.45]), ('0.6 keV (onset)', [0.6]), ('1-2 keV (scatter only)', [1.0, 2.0]),
                                     ('3-5 keV (k_B-ordered excess)', [3.0, 5.0]))
                      for sel_ in [np.isin([x['lam'] for x in cells], ls)]},
        by_lambda={f'L{lam:g}': dict(rel_excess=[x['rel'] for x in cells if x['lam'] == lam],
                                      strat_perm_rel=[x['strat'] / x['cev'] for x in cells if x['lam'] == lam],
                                      zero_median_sym_rel=[x['sym'] / x['cev'] for x in cells if x['lam'] == lam],
                                      paired_rel=[x['paired'] / x['cev'] for x in cells if x['lam'] == lam],
                                      points=[x['point'] for x in cells if x['lam'] == lam])
                   for lam in sorted({x['lam'] for x in cells})},
        pooled_residual_by_kB=pooled_kb,
        corr_rel_vs_frac_kB6=float(np.corrcoef(rel, [x['frac_kB6'] for x in cells])[0, 1]),
        paired_median_rel_range=[float(min(x['paired'] / x['cev'] for x in cells)), float(max(x['paired'] / x['cev'] for x in cells))],
        mean_r_rel_range=[float(min(x['mean_r'] / x['cev'] for x in cells)), float(max(x['mean_r'] / x['cev'] for x in cells))])
    C.dump('P1.json', res)
    figures(res)
    # console summary
    print('V2b revisit:', {k: v for k, v in res['v2b_revisit'].items() if k != 'cells'})
    for x in cells:
        print(f"  {x['point']:7s} {x['lam']:5.2f} keV: Dc {100 * x['rel']:+5.2f} % ({x['pull']:+.1f} sig), paired {100 * x['paired'] / x['cev']:+5.2f} %, "
              f"strat-perm {100 * x['strat'] / x['cev']:+5.2f} %, sym {100 * x['sym'] / x['cev']:+5.2f} %, k_B<6 {100 * x['rel_lt6']:+5.2f} %, f(kB>=6) {x['frac_kB6']:.2f}")


def plabel(pk):
    """physics label for a point key (fix R1, C items: no code identifiers in legends)."""
    sp, m = pk.split('_m')
    return (r'$\tilde{E}$' if sp == 'S' else 'E') + f' {m} GeV'


def figures(res):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    # 1. Ds_B vs Lambda with predictions
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axs[0]
    for (pk, v), mk in zip(res['points'].items(), 'osD^v'):
        L = [float(k[1:]) for k, r in v['by_lambda'].items() if 'Ds_B' in r]
        y = [v['by_lambda'][f'L{l:g}']['Ds_B']['median_raw_um'] for l in L]
        e = [v['by_lambda'][f'L{l:g}']['Ds_B']['err_raw_um'] for l in L]
        pm = [v['by_lambda'][f'L{l:g}']['Ds_B']['pred_MG_model_um'] for l in L]
        eb = ax.errorbar(L, y, yerr=e, fmt=mk, ms=4, label=plabel(pk))
        ax.plot(L, pm, '-', lw=0.8, color=eb[0].get_color())
    ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel(r'$\Lambda$ [keV]'); ax.set_ylabel(r'median $\Delta s_B$ (10 barrel layers) [$\mu$m]')
    ax.legend(fontsize='small', title='points: measured; lines: model', title_fontsize='x-small'); C.fig_label(ax)
    ax = axs[1]
    for (pk, v), mk in zip(res['points'].items(), 'osD^v'):
        L = [float(k[1:]) for k, r in v['by_lambda'].items() if 'c' in r]
        y = [v['by_lambda'][f'L{l:g}']['c']['median_c2'] for l in L]
        e = [v['by_lambda'][f'L{l:g}']['c']['err'] for l in L]
        p = [v['by_lambda'][f'L{l:g}']['c']['median_c_ev_MG'] for l in L]
        eb = ax.errorbar(L, y, yerr=e, fmt=mk, ms=4, label=plabel(pk))
        ax.plot(L, p, '-', lw=0.8, color=eb[0].get_color())
    ax.set_xscale('log'); ax.set_xlabel(r'$\Lambda$ [keV]'); ax.set_ylabel(r'median $c$ from $B_0$, $B_0/2$; lines: median $c_{ev}$')
    ax.xaxis.set_major_locator(FixedLocator([0.5, 1, 2, 3, 5])); ax.xaxis.set_major_formatter(ScalarFormatter()); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.legend(fontsize='small'); C.fig_label(ax)
    fig.savefig(C.FIG / 'p1_dsB_c.png', dpi=150, bbox_inches='tight'); plt.close(fig)
    # 2. V2b revisit: population excess vs the zero-median symmetric-scatter model (fix R1, constructive A-1).
    #    The stratified permutation keeps the conditional median of r, so it reproduces the observed excess by construction
    #    (corr 0.999): shown only as a grey identity check.
    cells = res['v2b_revisit']['cells']
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot([x['strat'] / x['cev'] * 100 for x in cells], [x['rel'] * 100 for x in cells], '.', color='0.7', ms=5, zorder=0,
            label='grey: x = stratified permutation\n(identity check, not a model;\nmost points off scale, on the diagonal)')
    cmap = {0.45: 'C3', 0.6: 'C1', 1.0: 'C0', 2.0: 'C9', 3.0: 'C2', 5.0: 'C4'}
    for pk, mk in zip([p for p in res['points']], 'osD^v'):
        cc = [x for x in cells if x['point'] == pk]
        for x in cc:
            ax.errorbar(x['sym'] / x['cev'] * 100, x['rel'] * 100, yerr=x['sig'] / x['cev'] * 100, fmt=mk, ms=5, color=cmap[x['lam']])
    for pk, mk in zip([p for p in res['points']], 'osD^v'):
        ax.plot([], [], mk, color='k', ms=5, label=plabel(pk))
    for lam, col in cmap.items():
        ax.plot([], [], 's', color=col, ms=6, label=rf'$\Lambda$ = {lam:g} keV')
    lim = [-8, 18]
    ax.plot(lim, lim, 'k:', lw=0.8); ax.axhspan(-1.5, 1.5, color='0.92', zorder=-1)
    ax.set_xlim(-1, 4.5); ax.set_ylim(-8, 18)
    ax.set_xlabel('median shift from zero-median symmetric scatter [%]'); ax.set_ylabel(r'population excess median($c$)/median($c_{ev}$) $-$ 1 [%]')
    ax.legend(fontsize='x-small', loc='upper left', bbox_to_anchor=(1.01, 1.0)); C.fig_label(ax)
    fig.savefig(C.FIG / 'p1_v2b_revisit.png', dpi=150, bbox_inches='tight'); plt.close(fig)
    # 3. B, MS, B+M thickness vs Lambda (E 500, E 1000)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    for ax, pk in zip(axs, ('F_m500', 'F_m1000')):
        v = res['points'][pk]['by_lambda']
        for nm, key, mk in (('B only', 'Ds_B', 'o'), ('material only (MS)', 'Ds_MS', 's'), ('B + material', 'Ds_BM', 'D')):
            L = [float(k[1:]) for k, r in v.items() if key in r]
            y = [v[f'L{l:g}'][key]['median_um' if key != 'Ds_B' else 'median_raw_um'] for l in L]
            e = [v[f'L{l:g}'][key]['err_um' if key != 'Ds_B' else 'err_raw_um'] for l in L]
            ax.errorbar(L, y, yerr=e, fmt=mk + '-', ms=4, lw=0.8, label=nm)
        ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlabel(r'$\Lambda$ [keV]'); ax.legend(fontsize='small', title=plabel(pk))
        C.fig_label(ax)
    axs[0].set_ylabel(r'median $\Delta s$ (10 barrel layers) [$\mu$m]')
    fig.savefig(C.FIG / 'p1_B_MS_BM.png', dpi=150, bbox_inches='tight'); plt.close(fig)


if __name__ == '__main__':
    main()
