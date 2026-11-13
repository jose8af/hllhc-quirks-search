"""Self-check: every headline number of acts/stage4/STAGE4_RESULTS.md recomputed from the C12FC_v1 JSON (and the cited
investigation JSON), formatted, and searched for in the report text.  Read-only, stdlib only:

    python3 -I acts/stage4/results/selfcheck_stage4.py

Exit status 1 if any check fails.
"""
import json
import math
import sys
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
D = TT / 'data' / 'acts_stage4' / 'analysis' / 'C12FC_v1'
OLD = TT / 'data' / 'acts_stage4' / 'analysis' / 'C12_v1'
REP = (TT / 'acts' / 'stage4' / 'STAGE4_RESULTS.md').read_text()
S = json.load(open(TT / 'data' / 'acts_stage4' / 'analysis' / 'STAGE4_SUMMARY.json'))
J = lambda p: json.load(open(p))  # noqa: E731
bs, lim, se, bg, man, acc = (J(D / f) for f in ('bsum_wp.json', 'limits.json', 'signal_eff.json', 'background.json',
                                                 'manifest.json', 'acceptance.json'))
SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
fails, n = [], 0


def sci(x, d=1):
    m, e = f'{x:.{d}e}'.split('e')
    return f'{m} × 10{str(int(e)).translate(SUP)}'


def check(label, cond, detail=''):
    global n
    n += 1
    if not cond:
        fails.append(f'{label}: {detail}')
    print(('OK   ' if cond else 'FAIL ') + label + (f'  [{detail}]' if detail else ''))


def in_rep(label, s):
    check(label, s in REP, f'"{s}" not found in report' if s not in REP else s)


# ---- outcome
check('WP T/G null', bs['rule']['wp']['T'] is None and bs['rule']['wp']['G'] is None)
check('branch', bs['rule']['wp']['branch'] == 'no WP in either category (§5.3): §8 fallback, user told')
check('complete_inputs', bs['rule']['complete_inputs'] is True)
check('non-DEV + freeze', lim['provenance']['dev'] is False and lim['provenance']['freeze_match'] is True)
in_rep('freeze sha', lim['provenance']['freeze_sha256'])
for c in 'TG':
    rows = bs['ladder'][c]
    best = min(rows, key=lambda r: r['B84'])
    check(f'min B84 {c} rung R09', best['name'] == 'R09_p>1e-3', best['name'])
    check(f'min B84 {c} = 1.23e6', round(best['B84'] / 1e6, 2) == 1.23, best['B84'])
    check(f'decades {c} = 7.05', round(math.log10(best['B84'] / 0.11), 2) == 7.05)
    check(f'R01 fails {c}', rows[0]['B84'] > 0.11 and all(r['B84'] > 0.11 for r in rows))
in_rep('min B84 text', '1.23 × 10⁶ (R09')
in_rep('decades text', '**7.05**')
r = {x['name']: x for x in bs['ladder']['T']}; g = {x['name']: x for x in bs['ladder']['G']}
in_rep('R04 T/G', f"{sci(r['R04_IP2>=7']['B84'])} (10.4 decades) | {sci(g['R04_IP2>=7']['B84'])} (11.8 decades)")
fb3 = bs['ladder']['FB']['FB3&h>5&o>5']
in_rep('FB3 B84', f"| best fallback column (FB3 = R14's non-width cuts ∧ w < 9.4 mm) | {sci(fb3['T']['B84'])} | {sci(fb3['G']['B84'])} |")
check('FB3 combined decades 7.1', round(math.log10((fb3['T']['B84'] + fb3['G']['B84']) / 0.3), 1) == 7.1)
# ---- composition at R09
cls = lambda l: 'PU' if l.startswith('PU') else ('SM' if l.startswith('SM') else 'C')  # noqa: E731
agg = {}
for t in g['R09_p>1e-3']['terms']:
    agg[cls(t['label'])] = agg.get(cls(t['label']), 0) + t['value']
in_rep('R09 composition', f"| **R09** | {sci(agg['PU'])} (bound) | {sci(agg['SM'])} (bounds) | {sci(agg['C'])} (bounds) |")
check('proxy fraction R09 = 45 %', round(bg['sm']['_proxy_fraction_of_B_SM']['R09_p>1e-3'], 2) == 0.45)
# ---- statistics reach
sr = S['statistics_reach']['R09_p>1e-3']
check('PU alone R09 2.3e3', round(sr['PU_alone_B84'], -2) == 2300, sr['PU_alone_B84'])
check('PU alone R08 3.0e4', round(S['statistics_reach']['R08_w<4.7']['PU_alone_B84'], -3) == 30000)
in_rep('pvpair needed', f"**{sci(sr["C' pvpair"]['events_needed_alone'])}**")
in_rep('dif needed', f"**{sci(sr["C' dif"]['events_needed_alone'])}**")
in_rep('Znunu needed', f"**{sci(sr['SM Znunu_j']['events_needed_alone'])}**")
# ---- closure
cl = bg['closure']
in_rep('T1', f"**{cl['T1']['ratio']:.3f}** | +{cl['T1']['z']:.1f}")
in_rep('T1w', f"**{cl['T1w']['ratio']:.3f}** | +{cl['T1w']['z']:.1f}")
es = {e['column']: e for e in bg['end_state']}
in_rep('compounded', f"**× {es['R05_w<37.5']['closure_factor']:.3f}**")
check('compounded = T1*T1w', abs(es['R05_w<37.5']['closure_factor'] - cl['T1']['ratio'] * cl['T1w']['ratio']) < 1e-9)
in_rep('trend slope', f"slope {cl['trend']['slope']:.3f} per rung".replace('-', '−'))
check('T3 not informative', bg['T3']['informative'] is False)
in_rep('c factor', f"| {bg['c_factor_applied']:.3f} |")
in_rep('rho2 reach', f"**{sci(1e-6 / bg['samples']['B2_trials'])}**")
check('reach R06/R07', bg['reach'] == {'deepest_reachable_rho2': 'R06_w<18.75', 'deepest_B1_ge10': 'R07_w<9.4'})
in_rep('SR-T window', f"**[{J(D / 'signal_srt.json')['window_ns'][0]}, {J(D / 'signal_srt.json')['window_ns'][1]}] ns**")
# ---- signal
P = S['fallback_points']
check('max eps(r_fb) 0.080', round(max(v['eps_rfb'] for v in P.values()), 3) == 0.080)
check('7 eps=0 points', sum(1 for v in P.values() if v['mu95_toys_events'] is None) == 7)
rv = se['a2']['a2fc_revert']
check('9 revert points', rv['n_revert'] == 9 and sum(1 for v in se['a2']['points'].values() if v.get('replaced_by_a2fc')) == 9)
e5 = rv['points']['A2|F|500|3|BM']
in_rep('E500 3 R14', f"**{e5['eps_R14_a2_numpy']:.3f} → {e5['eps_R14_a2fc']:.3f}**")
in_rep('E500 3 FB3', f"**{J(OLD / 'signal_eff.json')['a2']['points']['A2|F|500|3|BM']['fallback']['FB3&h>5&o>5']['eps']:.3f} → "
                     f"{se['a2']['points']['A2|F|500|3|BM']['fallback']['FB3&h>5&o>5']['eps']:.3f}**")
old = J(OLD / 'signal_eff.json')['a2']['points']
changed = sorted(k for k in old if old[k]['report_rungs'] != se['a2']['points'][k]['report_rungs'])
check('only revert points changed', changed == sorted(rv['points']), changed)
rel = [v['eps_R04_a2fc'] / v['eps_R04_a2_numpy'] - 1 for v in rv['points'].values()]
check('R04 full chain 5-30 % below', -0.31 < min(rel) and max(rel) < -0.04, [round(x, 3) for x in rel])
v43 = S['cited_investigations']['V4_3_A1_barrel']['points']
vals = [v43[s][l]['matched_any'] for s in v43 for l in ('1.5', '2.0') if l in v43[s]] + [v43['S500']['3.0']['matched_any']]
check('V4-3 0.90-0.97', round(min(vals), 2) == 0.90 and round(max(vals), 2) == 0.97, [round(x, 3) for x in vals])
# ---- limits
b = P['A2|F|200|1.5|BM']
best = min((v['mu95_over_Nexp'], k) for k, v in P.items() if v['mu95_over_Nexp'])
check('best point E200 1.5', best[1] == 'A2|F|200|1.5|BM')
in_rep('best ratio', f"**{best[0]:.0f}**")
in_rep('best mu95', f"**{b['mu95_toys_events'] / 1e7:.2f} × 10⁷**")
in_rep('band1s', f"[{sci(b['mu95_toys_band1s'][0])}, {sci(b['mu95_toys_band1s'][1])}]")
in_rep('sigma95', f"σ₉₅ = {sci(b['sigma95_fb'])} fb")
second = sorted((v['mu95_over_Nexp'], k) for k, v in P.items() if v['mu95_over_Nexp'])[1]
check('second E200 2 = 820', second[1] == 'A2|F|200|2|BM' and round(second[0]) == 820, second)
worst = max(v['mu95_over_Nexp'] for v in P.values() if v['mu95_over_Nexp'])
check('worst 6.0e7', round(worst / 1e7, 1) == 6.0, worst)
rat = [v['asym_over_toys'] for v in P.values() if v['asym_over_toys']]
in_rep('asym/toys range', f"**Asymptotic/toys: {min(rat):.2f}–{max(rat):.2f}**")
d5 = [v['mu_5sigma'] for v in P.values() if v['mu_5sigma']]
check('5 sigma 16 points 2.2e8-1.0e9', len(d5) == 16 and round(min(d5) / 1e8, 1) == 2.2 and round(max(d5) / 1e9, 1) == 1.0)
s3 = sorted(k for k, v in P.items() if v['S_at_rfb'] >= 3)
_s3 = lambda k: (('|F|200|' in k) or ('|F|500|' in k and float(k.split('|')[3]) >= 0.6)  # noqa: E731
                 or ('|F|1000|' in k and float(k.split('|')[3]) in (2, 5)) or ('|S|500|' in k and float(k.split('|')[3]) >= 2))
check('S>=3 set (FIX R3-NORM: 20 points)', s3 == sorted(k for k in P if _s3(k)) and len(s3) == 20, len(s3))
check('E1500 max S 0.29', round(max(v['S_at_rfb'] for k, v in P.items() if '|1500|' in k), 2) == 0.29)
check('E1000 max S 3.4', round(max(v['S_at_rfb'] for k, v in P.items() if '|1000|' in k), 1) == 3.4)
in_rep('S>=3 text', 'S ≥ 3 only at E200 (every Λ), E500 at Λ ≥ 0.6 keV, E1000 at 2 and 5 keV (max 3.4) and Ẽ500 at Λ ≥ 2 keV')
# ---- edges / sep / P1
E = S['p2_detector']['edges_A1_R04']
ups = [E[f'A1|{s}'][ 'upper']['value'] for s in ('F|200', 'F|500', 'F|1000', 'F|1500', 'S|500')]
in_rep('A1 upper edges', ' / '.join(f'{u:.2f}' for u in ups))
tdg = S['cited_investigations']['truth_degeneracy']['points']
in_rep('f_merge_any 5 keV', ' / '.join(f"{tdg[s]['5.0']['f_merge_any']:.2f}" for s in ('F200', 'F500', 'F1000', 'F1500', 'S500')))
check('sep_IT pu200 not measurable', J(D / 'sep_it_det.json')['pu200_measurable'] is False)
in_rep('NOT MEASURABLE', 'NOT MEASURABLE AT PU 200')
u = S['p1']['r_q_by_lambda_band']
in_rep('P1 r_q 1-3', f"**{u['1-3 keV']['min']:.2f}–{u['1-3 keV']['max']:.2f} at 1–3 keV**")
# ---- FIX R1 (REVIEW_RESULTS_R1): m_Q handles (A-1), B-1 scope, B-3, B-2, C-1, C-3, C-10
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_stage4_summary as MS  # noqa: E402
old_sum = J(TT / 'data' / 'acts_stage4' / 'analysis' / 'STAGE4_SUMMARY_C12v1.json')['p2_detector']
hc_sig = {k: dict(lam=v['lam'], r_fb=J(OLD / 'signal_eff.json')['admissibility'][f"{v['spin']}|{int(v['m'])}|{v['lam']:g}"]['r_fb'])
          for k, v in J(OLD / 'signal_eff.json')['a2']['points'].items()}
mo_old = MS.mass_observables(OLD, hc_sig)
for kd in ('A1', 'A2'):
    got = {s: mo_old[kd]['pooled_R04'][s]['M_est_GeV']['median'] for s in MS.SPM}
    check(f'M_est selection reproduces C12_v1 {kd}', got == {s: float(v) for s, v in old_sum[f'M_est_median_{kd}_GeV'].items()},
          got)
mo = S['p2_detector']['mass_observables']
new_sig = {k: dict(lam=v['lam'], r_fb=v['r_fb']) for k, v in S['fallback_points'].items()
           for v in [dict(v, lam=float(k.split('|')[3]))]}
check('mass_observables recomputed = JSON', json.loads(json.dumps(MS.mass_observables(D, new_sig), default=float)) == mo)
SPM_ = ('F200', 'F500', 'F1000', 'F1500', 'S500')
med2 = [mo['A2']['pooled_R04'][s]['M_est_GeV']['median'] for s in SPM_]
med1 = [mo['A1']['pooled_R04'][s]['M_est_GeV']['median'] for s in SPM_]
check('M_est A2 monotone in m (E)', mo['A2_E_monotone_in_m_R04'] is True and med2[:4] == sorted(med2[:4]))
fmt = lambda x: f'{x:,.0f}'.replace(',', ' ')  # noqa: E731
in_rep('M_est A2 ordering text', ' < '.join(fmt(x) for x in med2[:4]) + ' GeV')
in_rep('M_est A2 §0 text', '(' + ' / '.join(fmt(x) for x in med2[:4]) + ' GeV), but')
for s, nm in zip(SPM_, ('E200', 'E500', 'E1000', 'E1500', 'Ẽ500')):
    a1, a2, af = (mo[k][sel][s] for k, sel in (('A1', 'pooled_R04'), ('A2', 'pooled_R04'), ('A2', 'pooled_rfb')))
    q = lambda x: f"{x['M_est_GeV']['median']:.0f} [{x['M_est_GeV']['q16']:.0f}, {x['M_est_GeV']['q84']:.0f}]"  # noqa: E731
    in_rep(f'm_Q row {nm}', f"| {nm} | {q(a1)} | **{a2['M_est_GeV']['median']:.0f}** [{a2['M_est_GeV']['q16']:.0f}, "
           f"{a2['M_est_GeV']['q84']:.0f}] | {q(af)} | {a1['M_est_finite_fraction']:.2f} / {a2['M_est_finite_fraction']:.2f} | "
           f"{a1['beta_tof']['median']:.2f} / {a2['beta_tof']['median']:.2f} | {a1['dedx_MIP']['median']:.2f} / "
           f"{a2['dedx_MIP']['median']:.2f} |")
rr = mo['M_est_over_m_R04']
pm = mo['M_est_over_mQ_pooled']['values']
check('pair-mass pooled A2 = Stage-5 R2 (1051/850/2.256/19.06 %)', (pm['A2']['n_events'], pm['A2']['n_defined'],
      pm['A2']['median_M_est_over_mQ'], pm['A2']['frac_below_0p5_mQ']) == (1051, 850, 2.256, 0.1906), pm['A2'])
check('A1: 0 events below 1.5 m_Q', pm['A1']['n_below_1p5_mQ'] == 0 and pm['A1']['min_M_est_over_mQ'] > 1.5)
in_rep('median 2.26 m_Q text', f"median is {pm['A2']['median_M_est_over_mQ']:.2f} m_Q")
in_rep('N = 850 text', f"N = {pm['A2']['n_defined']}")
in_rep('19 % below 0.5 m_Q text', f"{round(100 * pm['A2']['frac_below_0p5_mQ'])} % below 0.5 m_Q")
in_rep('0 below 1.5 m_Q text', f"0 of {fmt(pm['A1']['n_defined'])}; minimum")
in_rep('pair-mass wording', 'estimates the pair mass M_QQ̄ ≥ 2 m_Q, not m_Q')
check('no "≈ 2.1–2.5 m" scale wording', '2.1–2.5 m' not in REP and '2.2–2.8 m' not in REP)
wc1, wc2 = mo['A1']['w_core_median_R04_by_point'], mo['A2']['w_core_median_R04_by_point']
in_rep('w_core A1 E500', ' / '.join(f"{wc1[f'F500|{l}']['median_mm']:.1f}" for l in ('1', '2', '3', '5')) + ' mm at 1 / 2 / 3 / 5 keV')
in_rep('w_core A2 E500', '(E500: ' + ' / '.join(f"{wc2[f'F500|{l}']['median_mm']:.1f}" for l in ('1', '2', '3', '5')) + ' mm')
in_rep('t_est not produced', 't_est / χ² vs Λ and `results/sensitivity.json` are **not produced**')
# B-1
fr = S['a2fc_revert']
oth = fr['eps_rfb_ratio_range_other_8']
check('FC/numpy other-8 range 0.67-1.25', oth == [0.67, 1.25], oth)
in_rep('FC/numpy range text', f"**{oth[0]:.2f}–{oth[1]:.2f}**")
in_rep('E500 3 outlier', f"**{fr['eps_rfb_fullchain_over_numpy']['A2|F|500|3|BM']:.2f}**")
check('31 numpy A2 points', fr['n_points_numpy_A2'] == 31)
in_rep('INV anchor', '<!-- INV_A2FC_E500 -->')
check('INV anchors filled (2)', REP.count('<!-- INV_A2FC_E500 -->') == 2 and 'OPEN' not in REP and ' pending' not in REP)
check('JSON investigation CLOSED', fr['investigation']['status'].startswith('CLOSED'))
INVD = TT / 'data' / 'acts_stage4' / 'investigation'
pr = J(INVD / 'inv_a2fc_e500_paired.json')['A2|F|500|3|BM']['ladder']
check('McNemar 7.6e-6 at R10-R14', all(round(pr[k]['p_mcnemar'], 7) == 7.6e-6 for k in ('R10_p>0.01', 'R11_p>0.05', 'R14_2S2>=3')),
      [pr[k]['p_mcnemar'] for k in ('R10_p>0.01', 'R11_p>0.05', 'R14_2S2>=3')])
check('R14 18/0 discordant', (pr['R14_2S2>=3']['a2_only'], pr['R14_2S2>=3']['fc_only']) == (18, 0))
in_rep('McNemar text', '**7.6 × 10⁻⁶** [E]')
in_rep('global p text', '**≈ 10⁻⁴–10⁻³** [E]')
in_rep('no mechanism', 'no mechanism was found')
in_rep('unpaired', 'paired comparison is effectively unpaired')
rp = J(INVD / 'inv_a2fc_e500_repsum.json')['tallies']
check('replica R14 fresh draws 10-11', sorted([rp['FCPU_numpy_k0'][-1], rp['FCPU_numpy_k1'][-1]]) == [10, 11])
in_rep('replica eps 0.05', '**ε_R14 ≈ 0.05**')
# Clopper-Pearson: our CP68 reproduces the pipeline's cp68 at all 40 points; quoted intervals
cpbad = [k for k, v in P.items() if any(abs(a - b) > 1e-6 for a, b in zip(MS.clopper_pearson(v['k_rfb'], v['n_den']), v['eps_rfb_cp68']))]
check('CP68 (stdlib) = pipeline cp68 at 40 points', not cpbad, cpbad)
cp = lambda v, c: '[' + ', '.join(f'{x:.3f}' for x in v[c]) + ']'  # noqa: E731
b15, e53 = P['A2|F|200|1.5|BM'], P['A2|F|500|3|BM']
in_rep('E200 1.5 CP68/95', f"9/200, 68 % CP {cp(b15, 'eps_rfb_cp68')}, 95 % {cp(b15, 'eps_rfb_cp95')}")
in_rep('E500 3 FB3 CP', f"11/200 = 0.055, 68 % CP {cp(e53, 'eps_rfb_cp68')}, 95 % [{e53['eps_rfb_cp95'][0]:.3f},\n  "
       f"{e53['eps_rfb_cp95'][1]:.3f}]")
in_rep('E500 3 R14 CP68', '4/200 = 0.020 (68 % CP [' + ', '.join(f'{x:.3f}' for x in MS.clopper_pearson(4, 200)) + '])')
# known frozen-code bug (products.py) listed
import importlib.util as _iu  # noqa: E402
_src = (TT / 'acts' / 'stage4' / 'analysis' / 'products.py').read_text().splitlines()
_bg = (TT / 'acts' / 'stage4' / 'analysis' / 'background.py').read_text()
_tr = _bg[_bg.index('TR_KEYS = ['):_bg.index(']', _bg.index('TR_KEYS = ['))]
check('products.py l.205-206 trials_phimet, absent from TR_KEYS', any('trials_phimet' in x for x in _src[204:206])
      and "'phimet'" not in _tr and 'trials_phimet' not in _tr)
check('event_display met_phi null', json.loads(MS._npz(D / 'event_display.npz', ['label'])['label'])['pu_fake']['met_phi'] is None)
in_rep('products.py caveat', "`acts/stage4/analysis/products.py` l. 205–206 looks up")
fb3_old = J(OLD / 'signal_eff.json')['a2']['points']['A2|F|500|3|BM']['fallback']['FB3&h>5&o>5']
fb3_new = se['a2']['points']['A2|F|500|3|BM']['fallback']['FB3&h>5&o>5']
in_rep('FB3 counts 29 -> 11', f"passes {round(fb3_old['eps'] * 200)} → {round(fb3_new['eps'] * 200)} of 200")
# B-3
pu = S['statistics_reach']['R09_p>1e-3']
c = next(t for t in bs['ladder']['G'] if t['name'] == 'R09_p>1e-3')['terms']
pc = next(t for t in c if t['label'].startswith('PU'))['comps']
check('PU N needed ~1.0e9', round(bg['samples']['B1_trials'] * pu['PU_alone_B84'] / 0.11 / 1e9, 1) == 1.0)
check('trend+density 1.7 -> median 0.02', round(math.hypot(pc['trend'], pc['density']), 1) == 1.7 and
      round(0.11 / math.exp(math.hypot(pc['trend'], pc['density'])), 2) == 0.02)
check('PU normalisation 0.26', round(pc['normalisation'], 2) == 0.26)
# B-2
_r4 = [v43[s][l]['matched_R04'] for s in v43 for l in ('1.5', '2.0') if l in v43[s]]
in_rep('matched_R04 range', f"{min(_r4):.2f}–{max(_r4):.2f}")
check('V4-3 PARTIAL in JSON', S['validations']['V4-3'].startswith('PARTIAL'))
in_rep('V4-3 PARTIAL text', '**V4-3 status: PARTIAL.**')
# C-1
xs = J(TT / 'sim' / 'results' / 'xsec.json')
check('sigma_norm E200 = 219.2 (N_IC = 2)', round(xs['normalisation_E']['rows']['200']['sigma_norm_nic2_fb'], 1) == 219.2)
in_rep('N_IC resolved', '**N_IC = 2 (resolved).**')
# C-3
in_rep('33 of 40 text', 'the 33 points with ε > 0 also get an')
# C-10: §1.4 "used at" column vs limits.json admissibility
USED = {'FB0': {'E200 0.45', 'E200 0.6', 'E200 0.85', 'E500 0.45', 'E500 0.6', 'E500 0.85', 'E500 1', 'E1000 0.45',
                'E1000 0.6', 'E1000 0.85', 'E1000 1', 'E1500 0.45', 'E1500 0.6', 'E1500 0.85', 'E1500 1', 'S500 0.45',
                'S500 0.6', 'S500 0.85', 'S500 1', 'S500 1.5'},
        'FB1': {'E200 1', 'E500 1.5', 'E1000 1.5', 'E1000 2', 'E1500 1.5', 'E1500 2', 'S500 2'},
        'FB2': {'E200 1.5', 'E500 2', 'S500 3'}, 'FB3': {'E200 2', 'E500 3', 'E1000 3', 'E1500 3'},
        'FB4': {'E200 3', 'E200 5', 'E500 5', 'S500 5'}, 'FB4e>1.3': {'E1000 5'}, 'FB4e>1.6': {'E1500 5'}}
got = {}
for k, v in lim['points'].items():
    p_ = k.split('|')
    got.setdefault(v['primary']['admissibility']['r_fb'].split('&')[0], set()).add(
        ('E' if p_[1] == 'F' else 'S') + p_[2] + ' ' + p_[3])
check('§1.4 used-at = limits.json r_fb', got == USED)
check('summary r_fb = limits.json r_fb', all(S['fallback_points'][k]['r_fb'] == v['primary']['admissibility']['r_fb']
                                              for k, v in lim['points'].items()))
# ---- FIX R2 (REVIEW_RESULTS_R2): B-1 systematic full-chain loss; C-1..C-9
SEC0 = REP[REP.index('## 0.'):REP.index('## 1.')]
ag = fr['paired_aggregate_other_8']
check('8 other revert points', len(ag['points']) == 8 and 'A2|F|500|3|BM' not in ag['points'])
check('R04 84/20, p ~1.6e-10, x0.83', (ag['R04']['numpy_only'], ag['R04']['fullchain_only']) == (84, 20)
      and round(ag['R04']['sign_test_p'] * 1e10, 1) == 1.6 and round(ag['R04']['ratio_fullchain_over_numpy'], 2) == 0.83)
check('r_fb 116 -> 101 x0.87, 7 of 8 <= 1', (ag['r_fb']['k_numpy'], ag['r_fb']['k_fullchain']) == (116, 101)
      and round(ag['r_fb']['ratio_fullchain_over_numpy'], 2) == 0.87 and ag['n_rfb_ratio_le_1'] == 7)
for nm in ('R04', 'R14', 'r_fb', 'FB3'):
    a = ag[nm]
    check(f'aggregate {nm} = sum over paired.json', a['k_numpy'] - a['numpy_only'] == a['k_fullchain'] - a['fullchain_only'])
in_rep('aggregate R04 row', f"| R04 (genuinely paired) | {ag['R04']['k_numpy']} → {ag['R04']['k_fullchain']} | **× "
       f"{ag['R04']['ratio_fullchain_over_numpy']:.2f}** | **{ag['R04']['numpy_only']} / {ag['R04']['fullchain_only']}** | "
       f"**1.6 × 10⁻¹⁰** |")
in_rep('aggregate r_fb row', f"| r_fb (each point's own) | {ag['r_fb']['k_numpy']} → {ag['r_fb']['k_fullchain']} | **× "
       f"{ag['r_fb']['ratio_fullchain_over_numpy']:.2f}** | {ag['r_fb']['numpy_only']} / {ag['r_fb']['fullchain_only']} | "
       f"{ag['r_fb']['sign_test_p']:.2f} |")
fs = fr['fullchain_eps_systematic']
check('best point on numpy A2, 31 points', fs['best_point_affected'] is True and fs['n_points_affected'] == 31)
check('corrected ratio ~910 / ~950', round(fs['best_ratio_corrected_rfb'], -1) == 910 and round(fs['best_ratio_corrected_R04'], -1) == 950,
      (fs['best_ratio_corrected_rfb'], fs['best_ratio_corrected_R04']))
in_rep('corrected ratio §0', 'the best ratio becomes **≈ 910** (790/0.87; ≈ 950 with the R04 factor 0.83)')
check('§0: unusual + no mechanism', 'statistically unusual (global p ≈ 10⁻⁴–10⁻³)' in SEC0 and 'no mechanism was\nfound' in SEC0)
check('§0: systematic, not noise; null unaffected', 'not noise' in SEC0 and 'no exclusion, is unaffected' in SEC0)
in_rep('ACTS quirk noise never replicated', 'the ACTS quirk-noise draw was never replicated')
check('old over-reach wording gone', 'not a systematic shift' not in REP and 'only genuine full-chain loss' not in REP
      and 'do not include the noise-draw spread' not in REP)
in_rep('row 268 1.6 %', '1/64 = 1.6 % at R04')
check('JSON verdict no "-5 % at R04"', '~ -5 % at R04' not in fr['investigation']['verdict'])
# C-8
cpu95 = b15['eps_rfb_cp95'][1]
check('95 % CP upper -> ~420; exclusion needs eps ~36', round(best[0] * b15['eps_rfb'] / cpu95, -1) == 420 and
      round(best[0] * b15['eps_rfb']) == 36)
in_rep('C-8 text', f"the 95 % CP upper ε ({cpu95:.3f}) gives ≈ 420; an exclusion would need ε ≈ 36")
# C-3
in_rep('A1 median 2.46', f"({pm['A1']['median_M_est_over_mQ']:.2f} m_Q without PU)")
in_rep('29 % below 1.5', f"{round(100 * pm['A2']['n_below_1p5_mQ'] / pm['A2']['n_defined'])} % ({pm['A2']['n_below_1p5_mQ']} of "
       f"{pm['A2']['n_defined']}) do")
check('no "at the pair-mass threshold"', 'at the pair-mass threshold' not in REP)
# C-4
r09 = {t['label']: t['value'] for t in g['R09_p>1e-3']['terms']}
check('C-4 individual bounds 1.4-1.7e5', round(r09["C' pvpair"] / 1e5, 1) == 1.4 and round(r09["C' dif"] / 1e5, 1) == 1.7)
in_rep('C-4 text', 'Individually these bounds are 1.4–1.7 × 10⁵ events')
# C-5, C-6, C-7, C-9, C-2
in_rep('C-5 lower bound', 'of ≳ 10–11/200')
in_rep('C-6 post hoc label', 'physically appropriate comparator (post hoc)')
in_rep('C-7 heading', '**What was measured at detector level.**')
in_rep('C-9 plain', 'the\n  signal would have to be 790 times larger than predicted to be excluded')
in_rep('C-2 P2 verdict word', '**P2 (m_Q, Λ): no measurement of m_Q or Λ at PU 200; only qualitative handles.**')
# ---- FIX R3-NORM (INV_NORM_F200): independent check of the signal normalisation.  The checks above only re-read
# N_exp from STAGE4_SUMMARY.json (and C-1 only that sigma_norm is the inclusive 219.2 fb), so they validated whatever
# formula the summary used.  Here N_exp is recomputed from the primary inputs: sigma_norm and f from xsec.json (Etilde:
# f from the investigation's numpy computation on S-TRGS_m500.npz, not from make_stage4_summary), A from
# acceptance.json, mu95 from limits.json.
L3 = 3000.0
finv = J(INVD / 'inv_norm_f200.json')
SNx = {f'F{m}': xs['normalisation_E']['rows'][str(m)]['sigma_norm_nic2_fb'] for m in (200, 500, 1000, 1500)}
SNx['S500'] = xs['normalisation_S']['500']['sigma_norm_nic2_fb']
Fx = {f'F{m}': xs['trigger_yields_E']['rows'][str(m)]['f_pt200_TRG_over_INC'] for m in (200, 500, 1000, 1500)}
Fx['S500'] = finv['f']['S500']['f_p2']
check('f_tail: E = xsec.json, S = inv_norm_f200 f_p2', all(abs(S['normalisation']['f_tail'][s]['value'] / Fx[s] - 1) < 1e-12
                                                          for s in Fx))
check('f_tail E ~ inv_norm_f200 f_p2 (< 2e-4)', all(abs(Fx[s] / finv['f'][s]['f_p2'] - 1) < 2e-4 for s in Fx))
bad_n, bad_s, bad_r, bad_sane = [], [], [], []
for k, v in P.items():
    sp_ = k.split('|')[1] + k.split('|')[2]
    A_ = acc['points'][k]['A_trig_presel']
    ne = SNx[sp_] * Fx[sp_] * L3 * A_
    if abs(v['N_exp_3ab'] / ne - 1) > 1e-9 or abs(v['A_incl'] / (A_ * Fx[sp_]) - 1) > 1e-12:
        bad_n.append(k)
    mu_ = lim['points'].get(k, {}).get('expected_primary')
    if mu_ and (abs(v['sigma95_fb'] / (mu_ / (L3 * A_ * Fx[sp_])) - 1) > 1e-9):
        bad_s.append(k)
    if mu_ and abs(v['mu95_over_Nexp'] / (mu_ / ne) - 1) > 1e-9:
        bad_r.append(k)
    # sanity: N_exp (after |eta| < 2.5, trigger, preselection) <= N(pT > 200) before cuts, and <= N(pT > 200, |eta| < 2.5)
    if sp_.startswith('F'):
        row = xs['trigger_yields_E']['rows'][sp_[1:]]
        n200, n200e = row['N_3iab_pt200'], row['N_3iab_pt200_eta25']
    else:
        n200 = n200e = SNx[sp_] * Fx[sp_] * L3
    if not (v['N_exp_3ab'] <= n200e <= n200 * (1 + 1e-12)):
        bad_sane.append(k)
check('N_exp = sigma_norm f L A (xsec.json + acceptance.json), 40 points', not bad_n and len(P) == 40, bad_n)
check('sigma95 = mu95 / (L A f) (limits.json), inclusive sigma', not bad_s, bad_s)
check('mu95/N_exp = limits.json mu95 / independent N_exp', not bad_r, bad_r)
check('sanity N_exp <= N(pT > 200 [, |eta| < 2.5]) before cuts, 40 points', not bad_sane, bad_sane)
b_old = b['N_exp_3ab'] / Fx['F200']
check('old (no f) E200 N_exp would fail the sanity check', b_old > xs['trigger_yields_E']['rows']['200']['N_3iab_pt200'], b_old)
check('best = inv_norm_f200 best_after (E200 1.5, 790)', finv['best_after']['point'] == best[1]
      and abs(best[0] / finv['best_after']['ratio'] - 1) < 1e-3 and round(best[0]) == 790, best)
in_rep('erratum box', '**Erratum (FIX R3-NORM, 2026-10-16).**')
in_rep('N_exp formula text', 'N_exp = σ_norm · f · 3 ab⁻¹ · A')
check('old formula header gone', 'N_exp = σ_norm·3 ab⁻¹·A' not in REP and '**μ₉₅/N_exp = 37.6**' not in REP)
in_rep('sigma95 inclusive text', 'σ₉₅ = μ₉₅/(3 ab⁻¹ · f · A)')
# ---- provenance
st = man['status']
check('2295 jobs admitted', sum(v['manifest'] for v in st.values()) == 2295 and
      all(v['missing']['n'] == v['invalid']['n'] == v['not_admitted']['n'] == 0 for v in st.values()))
check('11 replaced events', sum(v['replaced_events'] for v in st.values()) == 11)
in_rep('CPU-h', f"**{round(S['production']['cpu_h_total'])} CPU-h**")
check('campaigns', man['campaigns'] == ['C1a', 'C1b', 'C2B', 'A2FC'] and man['t_seed'] == 4)
check('schema ok', all(v == 'ok' for v in man['schema_check'].values()))
in_rep('N_trig', f"{bs['n_trig']['value'] / 1e7:.2f} × 10⁷ ± {100 * bs['n_trig']['rel_stat']:.1f} %")
print(f'\n{n - len(fails)}/{n} checks passed')
sys.exit(1 if fails else 0)
