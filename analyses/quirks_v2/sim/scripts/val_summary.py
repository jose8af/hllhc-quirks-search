"""val_summary.py -- print markdown tables from sim/results/*.json (used to write VALIDATION.md).
Run: pixi run -e ana python scripts/val_summary.py > results/summary_tables.md"""
import json
import os

RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
J = lambda n: json.load(open(os.path.join(RES, n))) if os.path.exists(os.path.join(RES, n)) else None
p = lambda *a: print(*a)


def f(x, d=3):
    return '—' if x is None else (f'{x:.{d}g}' if isinstance(x, float) else str(x))


x = J('xsec.json')
if x:
    p('## xsec: LO vs App.A'); p('| spin | m | MG [fb] | ref [fb] | ratio |'); p('|---|---|---|---|---|')
    for r in x['lo_vs_appA']['rows']:
        p(f"| {r['spin']} | {r['m']} | {r['mg_fb']:.4g} ± {r['mg_err']:.2g} | {r['ref_fb']:.4g} | {r['ratio']:.4f} |")
    p(f"\nFR/HW: E {x['fr_vs_hw']['ratio_E']:.4f}, S {x['fr_vs_hw']['ratio_S']:.4f}")
    p('\n## EW scheme'); p('| m | Gmu | (a) 127.9, sw2 0.2337 | ratio | (b) 127.9, sw2 0.2222 | ratio |'); p('|---|---|---|---|---|---|')
    for r in x['ew_scheme']['rows']:
        p(f"| {r['m']} | {r['gmu_fb']:.4g} | {r['alphaMZ_sw2_0p2337_fb']:.4g} | {r['ratio_a']:.4f} | {r['alphaMZ_sw2_0p2222_fb']:.4g} | {r['ratio_b']:.4f} |")
    p('\n## normalisation + yields'); p('| m | LO (α=1/127.9) [fb] | K | σ_norm N_IC=2 [fb] | /TH | f(pT>200) INC | f(pT>200) TRGS/INC | N(3/ab, pT>200) | N(3/ab, pT>200, |η|<2.5) |'); p('|---|---|---|---|---|---|---|---|---|')
    for m, r in x['normalisation_E']['rows'].items():
        y = x.get('trigger_yields_E', {}).get('rows', {}).get(m, {})
        p(f"| {m} | {r['lo_mg_alpha127p9_fb']:.4g} | {r['K']:.3f} | {r['sigma_norm_nic2_fb']:.4g} | {f(r['ratio_to_th'], 4)} | {f(y.get('f_pt200_INC'))} | {f(y.get('f_pt200_TRG_over_INC'))} | {f(y.get('N_3iab_pt200'))} | {f(y.get('N_3iab_pt200_eta25'))} |")
    p('\n## bands'); p('| sample | σ [fb] | scale 9pt | PDF68 | dyn1/2/3/4 | NNPDF23LO/CT18 |'); p('|---|---|---|---|---|---|')
    for k, b in x['bands']['rows'].items():
        dyn = '/'.join(f"{b['dyn'][d] / b['sigma']:.3f}" for d in ('1', '2', '3', '4'))
        p(f"| {k} | {b['sigma']:.4g} | +{b['scale_up_pct']:.1f}/{b['scale_dn_pct']:.1f} % | +{b['pdf_up68_pct']:.1f}/-{b['pdf_dn68_pct']:.1f} % | {dyn} | {b['nnpdf23lo_over_ct18']:.3f} |")
    p('\n## comparisons'); p(json.dumps(x['comparisons_E'], indent=0)[:3000])
s = J('spectra.json')
if s:
    p('\n## spectra medians (ratio MG/old)'); p('| point | sel | sample | γ*-1 q50 | ratio | m(QQ) q50 | ratio | pT q50 | y q16/q84 |'); p('|---|---|---|---|---|---|---|---|---|')
    for pt, P in s['points'].items():
        for sel, D in P.items():
            for k, v in D.items():
                r = v.get('median_ratio_to_old', {})
                p(f"| {pt} | {sel} | {k} | {v['gm1']['q50']:.4f} ± {v['gm1']['err'][1]:.4f} | {f(r.get('gm1'), 4)} | {v['M']['q50']:.0f} | {f(r.get('M'), 4)} | {v['pt']['q50']:.0f} | {v['y']['q16']:.2f}/{v['y']['q84']:.2f} |")
l = J('lmax_bias.json')
if l:
    p('\n## l_max bias vs MLM (TRGS)'); p('| point | model | ℓ_max median bias | stat | N_osc median bias | stat |'); p('|---|---|---|---|---|---|')
    for pt, P in l['points'].items():
        for k, v in P['bias_vs_iv'].items():
            p(f"| {pt} | {k} | {100 * v['lmax_median_bias']:+.1f} % | {100 * v['lmax_stat']:.1f} % | {100 * v['nosc_median_bias']:+.1f} % | {100 * v['nosc_stat']:.1f} % |")
        p(f"| {pt} | syst on ref | {json.dumps({k: (round(100 * v, 1) if isinstance(v, float) else [round(100 * u, 1) for u in v]) for k, v in P['syst_on_iv'].items()})} | | | |")
        p(f"| {pt} | f(pT>200) INC / LOPS | {f(P.get('f_pt200_INC'))} / {f(P.get('f_pt200_LOPS'))} | | | |")
m = J('mlm.json')
if m:
    p('\n## MLM'); p(json.dumps(m['djr'], indent=0)); p(json.dumps(m['qcut_variation_m500'], indent=0)); p(json.dumps(m['me_cut_closure'], indent=0))
t = J('tune.json')
if t:
    p('\n## tune'); p('| comparison | quantity | nominal q50 | variation q50 | rel |'); p('|---|---|---|---|---|')
    for k, v in t['comparisons'].items():
        for q, r in v['rel_change_variation_over_nominal'].items():
            a = v['nominal'].get(q); b = v['variation'].get(q)
            aa = a['q50'] if isinstance(a, dict) else a; bb = b['q50'] if isinstance(b, dict) else b
            p(f"| {k} | {q} | {f(aa, 4)} | {f(bb, 4)} | {100 * r:+.1f} % |")
o = J('loader.json')
if o:
    p('\n## loader'); p(json.dumps(o, indent=0)[:4000])
