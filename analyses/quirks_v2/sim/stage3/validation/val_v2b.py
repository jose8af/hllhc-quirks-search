"""val_v2b.py -- Stage-3 validation V2b, THE GATE: the c law on the MadGraph sample (plan §5, criteria fixed there).

Inputs: the production P1 outputs (campaign p1; run through run_stage3.py with jobs/v2b.json): B (B0 = 3.8112 T) and
B2 (B0/2), max_boost 1e-3, |eta_pair| < 1, vertex at the origin, 300 MG events per point (TRGS, pT > 200, unweighted,
template; E 1500 both halves), Lambda = 0.6, 1, 2 keV, species-masses E 200/500/1000/1500 and Etilde 500.
Observable: Delta_s_B = ds_barrel (plane through the vertex on the 10 virtual T3 barrel layers = the Stage-1 definition).
Measured c per event (Stage-1 convention, FU_analysis): c2 = (R(1/2) - 1)/ln 2, R(1/2) = 2 Ds(B0/2)/Ds(B0).
Prediction per event: c_ev = 1/[ln(l_max/b_odd) + K(gamma*)] from analytic/checks/c06_rotating_yoyo.pair_params and K_of
(imported, read only) on the same events at B0.  (The E1 polynomial K of FU_analysis is reported as a cross-check.)

GATE (P-10, fixed in plan §5; operationalised here before looking at the result): at Lambda = 1 keV, for EACH of the
5 species-masses: Dc = median(c2) - median(c_ev); sigma = bootstrap std of Dc (events resampled in pairs, 2000
resamples, seed 12345).  Point passes if |Dc| <= 2 sigma AND |Dc|/median(c_ev) <= 1.5 %.  V2b PASSES if all 5 points pass.
Reported, not gating (plan §5 list): Lambda exponents vs -2 + 2c (P-11), R(1/2) (P-13: 1.072 at 500 GeV), m dependence
of Delta_s_B at 1 keV (P-15), Etilde 500 vs E 500 (P-24), C re-derived on the MG sample vs predictions.json (a difference
is a sample effect, not a failure), and the k_B < 6 / >= 6 split.
Output: sim/stage3/results/V2b.json.  Run: pixi run python sim/stage3/validation/val_v2b.py
"""
import glob
import json

import numpy as np

import vcommon as V

OUT = V.TT / 'data' / 'sim_stage3' / 'out'
POINTS = [('F', 200), ('F', 500), ('F', 1000), ('F', 1500), ('S', 500)]
LAMS = [0.6, 1.0, 2.0]
NB = 2000


def load(spin, m, lam, cfg):
    fs = sorted(glob.glob(str(OUT / 'p1' / f'{spin}_m{m}' / f'L{lam:g}_{cfg}_c*.npz')))
    ev = []; ds = []; p1 = []; p2 = []; st = []
    for f in fs:
        with np.load(f) as z:
            ev.append(z['ev_index']); ds.append(z['ds_barrel_um']); p1.append(z['p_qp']); p2.append(z['p_qm']); st.append(z['status'])
    if not fs:
        return None
    return dict(ev=np.concatenate(ev), ds=np.concatenate(ds), p1=np.concatenate(p1), p2=np.concatenate(p2), st=np.concatenate(st))


def boot_diff(a, b, stat=np.median, nb=NB, seed=12345):
    rng = np.random.default_rng(seed)
    n = len(a); out = np.empty(nb)
    for k in range(nb):
        i = rng.integers(0, n, n)
        out[k] = stat(a[i]) - stat(b[i])
    return float(np.std(out))


def boot_stat(a, stat=np.median, nb=NB, seed=12345):
    rng = np.random.default_rng(seed)
    n = len(a)
    return float(np.std([stat(a[rng.integers(0, n, n)]) for _ in range(nb)]))


if __name__ == '__main__':
    V.add_orig_code_path()
    from c06_rotating_yoyo import pair_params, K_of
    from c13_population import angles
    from FU_analysis import Kfun
    preds = json.load(open(V.TT / 'analytic' / 'predictions.json'))
    res = dict(criteria='per point at 1 keV: |median(c2) - median(c_ev)| <= 2 sigma_boot AND <= 1.5 % of median(c_ev); '
                        'V2b PASS iff all 5 points pass', points={})
    gate = True
    dsmed = {}
    for spin, m in POINTS:
        P = {}
        for lam in LAMS:
            b = load(spin, m, lam, 'B'); h = load(spin, m, lam, 'B2')
            if b is None or h is None:
                continue
            assert np.array_equal(b['ev'], h['ev'])
            ok = np.isfinite(b['ds']) & np.isfinite(h['ds']) & (b['ds'] > 0)
            c2 = (2 * h['ds'] / b['ds'] - 1) / np.log(2)
            cev = np.zeros(len(c2)); cE1 = np.zeros(len(c2)); kB = np.zeros(len(c2)); Cev = np.zeros(len(c2))
            for i in range(len(c2)):
                pp = pair_params(b['p1'][i], b['p2'][i], float(m), lam)
                cev[i] = 1.0 / (pp['L'] + K_of(pp['gs']))
                cE1[i] = 1.0 / (pp['L'] + Kfun(pp['gs']))
                kB[i] = angles(b['p1'][i], b['p2'][i], float(m), lam)[1]
                epsB = 2.99792458e-3 * V.B0 / pp['sig']
                Cev[i] = 1.0 / cev[i] - np.log(1.0 / epsB)
            c2o, ceo = c2[ok], cev[ok]
            dc = float(np.median(c2o) - np.median(ceo))
            sig = boot_diff(c2o, ceo)
            R2 = 2 * h['ds'][ok] / b['ds'][ok]
            row = dict(n=int(ok.sum()), n_total=len(c2), status_counts=np.bincount(b['st'], minlength=6).tolist(),
                       median_c2=float(np.median(c2o)), median_c2_err=boot_stat(c2o), median_c_ev=float(np.median(ceo)),
                       median_c_E1poly=float(np.median(cE1[ok])), Dc=dc, sigma_Dc=sig, pull=dc / sig if sig > 0 else np.nan,
                       rel=dc / float(np.median(ceo)), paired_median_diff=float(np.median(c2o - ceo)),
                       median_R2=float(np.median(R2)), median_ds_B_um=float(np.median(b['ds'][ok])),
                       median_ds_B_err=boot_stat(b['ds'][ok]),
                       C_measured=float(1.0 / np.median(c2o) - np.log(1.0 / (2.99792458e-3 * V.B0 / pp['sig']))),
                       C_pred_median=float(np.median(Cev[ok])),
                       kB_lt6=dict(n=int(np.sum(ok & (kB < 6))), median_c2=float(np.median(c2[ok & (kB < 6)])) if np.any(ok & (kB < 6)) else None,
                                   median_c_ev=float(np.median(cev[ok & (kB < 6)])) if np.any(ok & (kB < 6)) else None),
                       kB_ge6=dict(n=int(np.sum(ok & (kB >= 6))), median_c2=float(np.median(c2[ok & (kB >= 6)])) if np.any(ok & (kB >= 6)) else None,
                                   median_c_ev=float(np.median(cev[ok & (kB >= 6)])) if np.any(ok & (kB >= 6)) else None))
            if lam == 1.0:
                row['PASS'] = bool(abs(dc) <= 2 * sig and abs(dc) / np.median(ceo) <= 0.015)
                gate &= row['PASS']
            P[f'L{lam:g}'] = dict(row, _ds=b['ds'], _cev=cev, _ok=ok)
        # exponents (P-11): per-event slopes between adjacent Lambda, vs -2 + 2 c_ev at the geometric-mean Lambda
        ex = {}
        for la, lb in ((0.6, 1.0), (1.0, 2.0)):
            A, Bq = P.get(f'L{la:g}'), P.get(f'L{lb:g}')
            if A is None or Bq is None:
                continue
            ok = A['_ok'] & Bq['_ok']
            sl = np.log(Bq['_ds'][ok] / A['_ds'][ok]) / np.log(lb / la)
            pred = -2 + 2 * 0.5 * (A['_cev'][ok] + Bq['_cev'][ok])
            pop = np.log(np.median(Bq['_ds'][ok]) / np.median(A['_ds'][ok])) / np.log(lb / la)
            ex[f'{la:g}to{lb:g}'] = dict(median_event_slope=float(np.median(sl)), err=boot_stat(sl), median_pred=float(np.median(pred)),
                                         population_slope=float(pop))
        for k in list(P):
            for kk in ('_ds', '_cev', '_ok'):
                P[k].pop(kk)
        res['points'][f'{spin}_m{m}'] = dict(by_lambda=P, exponents=ex)
        if 'L1' in P:
            dsmed[f'{spin}_m{m}'] = (P['L1']['median_ds_B_um'], P['L1']['median_ds_B_err'])
    res['P13_R2_E500_1keV'] = dict(measured=res['points']['F_m500']['by_lambda']['L1']['median_R2'], predicted=1.072)
    res['P15_m_dependence_1keV_median_ds_um'] = {k: v for k, v in dsmed.items() if k.startswith('F')}
    res['P15_model_medians_T3_sample_um'] = {'F_m200': 33.5, 'F_m500': 31.1, 'F_m1000': 29.5}
    lm = np.log([200, 500, 1000, 1500]); lv = np.log([dsmed[f'F_m{m}'][0] for m in (200, 500, 1000, 1500)])
    res['P15_slope_dln_ds_dln_m'] = float(np.polyfit(lm, lv, 1)[0])
    res['P24_S500_over_F500_1keV'] = dict(measured=dsmed['S_m500'][0] / dsmed['F_m500'][0], predicted_model=36.0 / 31.0)
    res['C_predictions_json_T3_sample'] = preds['thickness_law_v4']['C_population']
    res['PASS'] = bool(gate)
    V.dump('V2b.json', res)
    print('V2b GATE:', 'PASS' if gate else 'FAIL')
    for k, v in res['points'].items():
        r = v['by_lambda'].get('L1', {})
        print(f"  {k} 1 keV: n={r.get('n')} median c2={r.get('median_c2', np.nan):.4f} +- {r.get('median_c2_err', np.nan):.4f}, "
              f"median c_ev={r.get('median_c_ev', np.nan):.4f}, Dc={r.get('Dc', np.nan):+.4f} +- {r.get('sigma_Dc', np.nan):.4f} "
              f"({100 * r.get('rel', np.nan):+.2f} %), PASS={r.get('PASS')}")
        for lam in ('L0.6', 'L2'):
            r2 = v['by_lambda'].get(lam, {})
            if r2:
                print(f"     {lam}: c2={r2['median_c2']:.4f} c_ev={r2['median_c_ev']:.4f} Dc={r2['Dc']:+.4f}+-{r2['sigma_Dc']:.4f}")
        print('     exponents', {kk: (round(e['median_event_slope'], 3), round(e['median_pred'], 3)) for kk, e in v['exponents'].items()})
    print('P13', res['P13_R2_E500_1keV'], 'P15', res['P15_m_dependence_1keV_median_ds_um'], 'slope', round(res['P15_slope_dln_ds_dln_m'], 3),
          'P24', res['P24_S500_over_F500_1keV'])
