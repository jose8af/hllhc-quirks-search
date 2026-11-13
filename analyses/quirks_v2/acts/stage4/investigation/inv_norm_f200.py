"""INV_NORM_F200: tail fraction f of the Stage-3 p2 population and the corrected N_exp / mu95/N_exp.

f_p2 = sum w(TRGS rows with pT(QQ) > 200, |eta_pair| < 4) / sigma_ref_fb   (the population A is conditional on;
       sim/stage3/code/make_inputs.py extract(): w > 0, ptmin 200, eta_max 4; mg_events.sigma_norm_fb convention)
Cross-checks: positive-only weights, |eta|<2.5 and no-eta variants, the hit-or-miss count x w_max, xsec.json
trigger_yields_E.  Then N_exp_corr = N_exp_3ab x f_p2 and ratio_corr = mu95/N_exp_corr for every fallback point of
data/acts_stage4/analysis/STAGE4_SUMMARY.json.  Read-only; writes data/acts_stage4/investigation/inv_norm_f200.json.
Usage: python -I inv_norm_f200.py <TT>
"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(sys.argv[1])
NPZ = TT / 'data' / 'sim' / 'npz'
OUT = TT / 'data' / 'acts_stage4' / 'investigation' / 'inv_norm_f200.json'
xs = json.loads((TT / 'sim' / 'results' / 'xsec.json').read_text())
S4 = json.loads((TT / 'data' / 'acts_stage4' / 'analysis' / 'STAGE4_SUMMARY.json').read_text())
lim = json.loads((TT / 'data' / 'acts_stage4' / 'analysis' / 'C12FC_v1' / 'limits.json').read_text())
acc = json.loads((TT / 'data' / 'acts_stage4' / 'analysis' / 'C12FC_v1' / 'acceptance.json').read_text())

pts = S4['fallback_points']
need = sorted({(k.split('|')[1], int(k.split('|')[2])) for k in pts})
F = {}
for sp, m in need:
    p = NPZ / f"{'E' if sp == 'F' else 'S'}-TRGS_m{m}.npz"
    z = np.load(p, allow_pickle=False)
    w = z['w']; pt = z['pt_pair']; eta = np.abs(z['eta_pair'])
    sref = float(z['sigma_ref_fb']); snorm = float(z['sigma_norm_fb'])
    t = pt > 200
    u = np.random.default_rng(12345).random(len(w)); wmax = float(w[w > 0].max())
    hm = (w > 0) & (u < w / wmax)                                   # make_inputs / mg_events.unweight_mask
    F[f'{sp}{m}'] = dict(
        file=p.name, sigma_ref_fb=sref, sigma_norm_fb_file=snorm, w_neg_frac=float((w < 0).mean()),
        f_p2=float(w[t & (eta < 4)].sum() / sref),
        f_p2_pos=float(w[t & (eta < 4) & (w > 0)].sum() / sref),
        f_p2_hitmiss=float((hm & t & (eta < 4)).sum() * wmax / sref),
        f_all_eta=float(w[t].sum() / sref), f_eta25=float(w[t & (eta < 2.5)].sum() / sref),
        xsec_json_f_pt200=(xs['trigger_yields_E']['rows'].get(str(m), {}).get('f_pt200_TRG_over_INC')
                           if sp == 'F' else None),
        xsec_json_sigma_norm=(xs['normalisation_E']['rows'][str(m)]['sigma_norm_nic2_fb'] if sp == 'F'
                              else xs['normalisation_S'][str(m)]['sigma_norm_nic2_fb']))
    print(sp, m, {k: (round(v, 5) if isinstance(v, float) else v) for k, v in F[f'{sp}{m}'].items()})

rows = {}
for k, v in pts.items():
    sp, m = k.split('|')[1], int(k.split('|')[2])
    f = F[f'{sp}{m}']['f_p2']
    A = acc['points'][k]['A_trig_presel']
    ne = v['sigma_norm_fb'] * 3000.0 * A
    mu = lim['points'].get(k, {}).get('expected_primary')
    r = dict(A=A, N_exp_reproduced=ne, N_exp_summary=v['N_exp_3ab'], f_p2=f, N_exp_corr=ne * f,
             mu95=mu, ratio_summary=v['mu95_over_Nexp'],
             ratio_corr=(mu / (ne * f)) if mu else None,
             mu5_ratio_corr=(v['mu_5sigma'] / (ne * f)) if v.get('mu_5sigma') else None,
             S_at_rfb_corr=v['S_at_rfb'] * f, sigma95_fb_summary=v['sigma95_fb'],
             sigma95_over_sigma_th_summary=(v['sigma95_fb'] / v['sigma_norm_fb']) if v['sigma95_fb'] else None)
    rows[k] = r
ok = {k: r for k, r in rows.items() if r['ratio_corr']}
b0 = min(ok, key=lambda k: ok[k]['ratio_summary']); b1 = min(ok, key=lambda k: ok[k]['ratio_corr'])
res = dict(f=F, points=rows, best_before=dict(point=b0, ratio=ok[b0]['ratio_summary']),
           best_after=dict(point=b1, ratio=ok[b1]['ratio_corr'], ratio_before_same_point=ok[b1]['ratio_summary']),
           max_rel_diff_Nexp_reproduction=max(abs(r['N_exp_reproduced'] / r['N_exp_summary'] - 1) for r in rows.values()))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(res, indent=1))
print('best before', res['best_before'], '\nbest after', res['best_after'], '\nrepro', res['max_rel_diff_Nexp_reproduction'])
for k in sorted(ok, key=lambda k: ok[k]['ratio_corr'])[:8]:
    print(k, round(ok[k]['ratio_summary'], 2), '->', round(ok[k]['ratio_corr'], 1), 'f', round(ok[k]['f_p2'], 4))
