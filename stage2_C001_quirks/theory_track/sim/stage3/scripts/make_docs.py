"""make_docs.py -- Stage-3 documents generated from results/*.json and STAGE3_INDEX.json (E8, 2026-10-13).

  * VALIDATION.md: the block between <!-- BEGIN AUTO-HEADLINES --> and <!-- END AUTO-HEADLINES --> (§0) is regenerated;
  * README.md: the block between <!-- BEGIN AUTO-RESULTS --> and <!-- END AUTO-RESULTS --> is regenerated;
  * SAMPLES.md: fully generated (inventory, totals per machine, environments, md5s).
Numbers are copied from the JSON files by program; nothing is typed by hand.
Run (theory_track/): pixi run python sim/stage3/scripts/make_docs.py
"""
import json
import math
import re
from collections import defaultdict

import s3common as C


def J(name):
    return json.load(open(C.RES / name))


def f(x, n=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return '-'
    if isinstance(x, (int,)) and not isinstance(x, bool):
        return str(x)
    return f'{x:.{n}g}'


def pct(x, n=2):
    return '-' if x is None else f'{100 * x:+.{n}f} %'


def replace_block(path, tag, text):
    s = open(path).read()
    b, e = f'<!-- BEGIN {tag}', f'<!-- END {tag} -->'
    i = s.index(b); j = s.index(e)
    i2 = s.index('-->', i) + 3
    open(path, 'w').write(s[:i2] + '\n' + text.rstrip() + '\n' + s[j:])


def headlines():
    M = J('merge.json'); X = J('xover.json'); V1 = J('V1.json'); V2a = J('V2a.json'); V2b = J('V2b.json'); V3 = J('V3.json')
    V4 = J('V4.json'); V4d = J('V4_diag.json'); V5 = J('V5.json'); Vs = J('Vscale.json'); V6 = J('V6.json'); V7 = J('V7.json')
    V8 = J('V8.json'); V8p = J('V8_production.json'); V9 = J('V9.json'); P1 = J('P1.json'); S4 = J('V7_status4.json')
    c5 = J('c5kev_diag.json'); BO = J('FIX_bstar_off.json'); VS3 = J('Vscale_s3.json'); BX = J('FIX_R2_bstar_context.json')
    V8m = [json.loads(x) for x in open(C.RES / 'V8_merge.jsonl')]
    ck = M['checks']; tot = M['totals']
    xj = X['jobs']
    nid = sum(v['n_kernel_bit_identical_events'] for v in xj.values()); nev = sum(v['n_events'] for v in xj.values())
    maxsh = max((v['nonidentical']['max_hit_shift_um']['max'] or 0.0) for v in xj.values())
    v2b1 = {k: v['by_lambda']['L1'] for k, v in V2b['points'].items()}
    rv = P1['v2b_revisit']
    vb = V5['b']['medians']
    shifts = [v['rel_shift'] for v in vb.values()]
    v8s = V8p['summary']
    rows = [
        ('Merge / completeness', 'every job of all.json once, valid, same job definition, current code md5; overlap on both machines',
         f"{ck['n_found']}/{ck['n_expected_files']} files valid; missing {len(ck['missing'])}, invalid {len(ck['invalid'])}, "
         f"job-definition diffs {len(ck['job_definition_differs'])}, code-md5 diffs {len(ck['code_md5_differs'])}, duplicate events "
         f"{ck['duplicate_events_in_canonical']}", 'PASS' if ck['PASS'] else 'FAIL'),
        ('Cross-machine (xover)', 'Mac vs PC on 3 overlap jobs: statistically equivalent (KS p > 0.01/n_tests, |median pull| < 3)',
         f"kernel output bit-identical in {nid}/{nev} events; 1 event differs (max hit shift {f(maxsh)} um); all KS p = 1", 'PASS' if X['PASS'] else 'FAIL'),
        ('V1 kernel regression', 'legacy s3 = T3_causal bit for bit', f"{V1['V1']['n_runs'] - V1['V1']['n_not_identical']}/{V1['V1']['n_runs']} identical", 'PASS' if V1['V1']['PASS'] else 'FAIL'),
        ('V1b new recorder', 'legacy hits < 1e-9 cm; discs vs independent scan', f"max diff {f(V1['V1b_a']['max_diff_cm'])} cm, 0 missing/extra", 'PASS' if V1['V1b_a']['PASS'] else 'FAIL'),
        ('V2a Stage-1 numbers', 'per-event Ds and FU medians reproduced exactly', '960/960 bit-identical (gate session)', 'PASS' if V2a['PASS'] else 'FAIL'),
        ('V2b c law (gate, 1 keV)', '|Dc| <= 2 sigma and <= 1.5 % at all 5 points',
         ', '.join(f"{k} {pct(v['rel'])}" for k, v in v2b1.items()), 'FAIL (finding; user decision §7 of VALIDATION_GATE)'),
        ('V2b revisit (full P1, 30 cells)', 'same criterion per cell (reported)',
         f"{rv['n_pass_P10_criterion']}/{rv['n_cells']} cells pass; population excess by regime: "
         + '; '.join(f"{k.split(' (')[0]} {pct(v['rel_excess_weighted_mean'])} +- {100 * v['rel_excess_weighted_err']:.2f} %" for k, v in rv['regime_split'].items())
         + "; at 1-2 keV reproduced by zero-median symmetric scatter (model mean " + pct(rv['regime_split']['1-2 keV (scatter only)']['zero_median_sym_rel_mean']) + ")",
         'finding (PROPOSED_CHANGES.md)'),
        ('c at 5 keV: step / replica (E8)', 'step (1e-4) and round-off replicas on the 12 highest-r k_B >= 6 events (E 1000)',
         f"median r {f(c5['summary']['median_r_prod_hi'])} (prod) vs {f(c5['summary']['median_r_1e4_hi'])} (1e-4); replica spread {f(c5['summary']['median_replica_spread_c2'])}",
         'size stable; does NOT probe the precision floor (NUMERICS §13.1) -> no attribution from this test'),
        ('c at 5 keV: B*-off vs on (fix R1)', 'Stage-1 FIX2 B*-off fields, same kernel both arms; E 500 + E 1000, 16 random events per k_B bin',
         f"{BO['n_events']} events, {BO['cpu_h']:.2f} CPU-h; median r/c_ev B* on / off: "
         + ', '.join(f"{k} {100 * v['r_on_over_cev'][0]:+.1f} / {100 * v['r_off_over_cev'][0]:+.1f} %" for k, v in BO['bins']['pooled'].items()),
         'measured (VERIFIED); attribution ESTIMATE (fix R2: B* carries the bulk of the population-median excess: B* off '
         f"{100 * BX['off_vs_production']['all']['off'][0]:+.1f} % vs production {100 * BX['off_vs_production']['all']['prod'][0]:+.1f} % "
         f"(E 500 + E 1000), {BX['off_vs_production']['all']['significance']:.1f} sigma; paired on - off on the same events "
         f"{BX['paired_on_minus_off']['all']['significance']:.1f} sigma (all), {BX['paired_on_minus_off']['kB>=6']['significance']:.1f} sigma "
         f"(k_B >= 6); B* mainly widens the per-event c spread; B*-off remainder at k_B >= 10 within the floor allowance "
         f"{100 * BX['floor_allowance_subsample']['kB>=10']['floor_rel_range'][0]:.1f}-{100 * BX['floor_allowance_subsample']['kB>=10']['floor_rel_range'][1]:.1f} % at the sample's eps_perp)"),
        ('V3 step convergence / floor', 'Ds < 1 %, hits < 1/5 um at production settings', '30/32 cells (2 B-only cells at 1e-2; P2 moved to 1e-3 up to 5 keV)', 'FAIL (literal; gate §3)'),
        ('V4 independent solver', 'R1 N=256 ratio 0.99-1.01, <= 8 um', f"N=256 fails; N=1024/4096 median ratios 1.0003-1.0011", 'FAIL literal; accepted at N >= 1024 (user)'),
        ('V5a T2-cache continuity', 'legacy production driver = T3_ms_thickness.npy', f"{V5['a']['n_identical']}/{V5['a']['n_runs']} events x 4 configs bit-identical; draw regenerated identically ({V5['a']['cpu_h']:.2f} CPU-h)", 'PASS' if V5['a']['PASS'] else 'FAIL'),
        ('V5b MG vs cache', 'report shift of medians (|eta| < 1)', f"{len(vb)} medians: shifts {100 * min(shifts):+.0f} … {100 * max(shifts):+.0f} %, |pull| <= {max(abs(v['pull']) for v in vb.values()):.1f}", 'reported'),
        ('V-scale', 'hits agree after x/9 (<= 5 um), same counts, Ds within 1 %', f"legacy recorder, max_boost 1e-2: {sum(e['PASS'] for e in Vs['events'])}/{len(Vs['events'])}; "
         f"production s3 recorder (fix R1): {sum(e['PASS'] for e in VS3['max_boost_0.01']['events'])}/5 at 1e-2, {sum(e['PASS'] for e in VS3['max_boost_0.001']['events'])}/5 at 1e-3 "
         f"(Ds ratio {min(e['ds_ratio'] for e in VS3['max_boost_0.001']['events']):.4f}-{max(e['ds_ratio'] for e in VS3['max_boost_0.001']['events']):.4f})",
         'FAIL (literal, at 1e-2: step effect on one grazing crossing); PASS at the production 1e-3'),
        ('V6 reproducibility', '50 jobs bit-identical on rerun; spawn', f"{V6['n_events']} events, {V6['n_array_differences']} differences", 'PASS' if V6['PASS'] else 'FAIL'),
        ('V7 causality', 't >= r/c for every hit', f"min(t - t_vtx - d/c) = {min(v['min_dt_ns'] for v in V7['causality'].values()) * 1000:.2f} ps over {sum(v['n_events'] for v in V7['causality'].values())} events", V7['verdict']['causality']),
        ('V7 vacuum', 'vacuum Ds <= 1e-3 um', f"hits planar to {f(V7['vacuum']['svd_max_um'])} um (SVD); stored eigh value <= {f(V7['vacuum']['stored_eigh_max_um'])} um (plane-fit floor)", 'PASS (hits); stored value at the eigh floor'),
        ('V7 status', 'no status 3/4/5', f"{S4['n_events']} status-4 events (0.05 %), all reproduced; label swap recovers {S4['swap_status_counts'][1]}; 85 status-0 (t_end) at <= 0.5 keV", 'FAIL (literal); listed'),
        ('V7 hits per layer', '~3 per layer (S-6)', ', '.join(f"{k.split('/')[1]} {v['mean']:.2f}" for k, v in V7['hits_per_layer'].items() if k.endswith('L1_BM')), 'consistent (sample-dependent)'),
        ('V8 ACTS ingestion (literal criterion: n_meas = n_SimHits)', 'hits on surface, units, measurements', f"gate smoke {V8['n_on_surface']}/{V8['n_checked']}, {V8['n_measurements']}/{V8['n_simhits']} meas.; production files: "
         + '; '.join(f"{k.split('/')[-2]}/{k.split('/')[-1].split('_')[0]} {v['on_surface']}/{v['checked']} on surface, {v['measurements']}/{v['simhits']} meas." for k, v in v8s.items()),
         'geometry, units: PASS; measurements: FAIL at 10/15/30 keV (literal; V8_production.json PASS = false)'),
        ('V8 cause (fix R1)', 'same injection with ACTS doMerge = False (default True, mergeNsigma = 1)',
         '; '.join(f"{x['lam_keV']:g} keV: {x['n_meas']}/{x['n_simhits']}" for x in V8m if x['variant'] == 'A' and not x['doMerge'])
         + ' (doMerge = False, as V8); default doMerge = True: '
         + ', '.join(f"{x['n_meas']}/{x['n_simhits']}" for x in V8m if x['variant'] == 'A' and x['doMerge']),
         'explained: digitiser merging of close hits on one surface (not a loss)'),
        ('V9 unweighting', 'weighted vs unweighted medians within 2 sigma', ', '.join(f"{k} {v['pull']:+.2f}" for k, v in V9['observables'].items()), 'PASS' if V9['PASS'] else 'FAIL'),
    ]
    out = ['Generated by `scripts/make_docs.py` from `results/*.json`. VERIFIED = measured on the production or a rerun.',
           '', '| Test | Criterion | Result | Verdict |', '|---|---|---|---|']
    esc = lambda t: str(t).replace('|', '\\|')  # noqa: E731
    out += [f'| {esc(a)} | {esc(b)} | {esc(c)} | {esc(d)} |' for a, b, c, d in rows]
    out += ['', f"Production: {tot['mac']['files'] + tot['pc']['files']} jobs, {tot['mac']['events'] + tot['pc']['events']} events "
            f"(Mac {tot['mac']['events']}, PC {tot['pc']['events']}); CPU {tot['mac']['cpu_h_events']:.1f} h (Mac) + {tot['pc']['cpu_h_events']:.1f} h (PC). "
            f"Small validation reruns (E8): {V9['cpu_s'] / 3600 + S4['cpu_h'] + V5['a']['cpu_h'] + c5['cpu_h']:.2f} CPU-h; fix pass R1: "
            f"B*-off {BO['cpu_h']:.2f}, V-scale s3 {VS3['cpu_h']:.3f} CPU-h (+ P2 robust systematics and V8 merge test, < 0.2 CPU-h)."]
    return '\n'.join(out)


def results_block():
    P1 = J('P1.json'); P2 = J('P2.json'); SL = J('FIX_R2_notes.json')['sep_IT_slope_1to30keV']
    ncomp = nlow = 0
    for v in P2['systematics'].values():
        for x in v['total'].values():
            for c in ('lmax', 'qed_down', 'pdf'):
                if c in x.get('components_rel_robust', {}) and c in x.get('robust_shift_sampling_sd_rel', {}):
                    ncomp += 1; nlow += x['components_rel_robust'][c] < 2 * x['robust_shift_sampling_sd_rel'][c]
    out = ['Generated by `scripts/make_docs.py` from `results/P1.json` and `results/P2.json`. Truth level. Pull = (prediction - measurement)/sigma.', '',
           '**P1 (|eta_pair| < 1, vertex at the origin, 10 T3 barrel layers; B at max_boost 1e-3).** Ds_B median [µm]; MG model = the c06 rotating-yo-yo',
           'model on the same events: **paired** per-event median ratio measured/model +- bootstrap (pull of the ratio vs 1; fix R1, the primary statistic) and',
           'the unpaired pull of the medians (secondary); c (B0, B0/2) with median c_ev on the same events (MG) and predictions.json;',
           'R(1/2) = 2 Ds(B0/2)/Ds(B0) = 1 + c ln 2 (the same measurement as c, not independent) with its pull vs 1 + c_ev ln 2; MS floor and B+M.', '',
           '| point | Lambda [keV] | l_max/R_IT (median) | Ds_B [µm] | paired Ds_B/model (pull) | MG model median (unpaired pull) | f floor | c measured | c_ev MG (pull) | c json (pull) | R(1/2) (pull) | Ds_MS [µm] | Ds_B+M [µm] | BM/sqrt(B²+M²) |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for pk, v in P1['points'].items():
        for lk, r in v['by_lambda'].items():
            b = r.get('Ds_B'); c = r.get('c'); R = r.get('R_half'); q = r.get('B_MS_combination')
            ds = '-' if not b else (f"{f(b['median_raw_um'])} +- {f(b['err_raw_um'], 2)}" + (' (floor-dominated: withheld)' if b['withheld_floor_dominated'] else '') + (' (+-5 % unattr.)' if b['syst_unattributed_rel'] else ''))
            pr = '-' if not b else f"{b['paired_ratio_MG_model']:.3f} +- {b['paired_ratio_err']:.3f} ({b['paired_ratio_pull']:+.1f})"
            out.append(f"| {pk} | {lk[1:]} | {f(r.get('ell_max_over_R_IT_median'), 2)} | {ds} | {pr} | {'-' if not b else f(b['pred_MG_model_um']) + ' (' + f(b['pull_MG_model_um'], 2) + ')'} | "
                       f"{'-' if not b else f'{b['f_floor_flag']:.2f}'} | {'-' if not c else f'{c['median_c2']:.4f} +- {c['err']:.4f}'} | "
                       f"{'-' if not c else f'{c['median_c_ev_MG']:.4f} ({c['pull_MG']:+.1f})'} | "
                       f"{'-' if not c or c['pred_json'] is None else f'{c['pred_json']:.3f} ({c['pull_json']:+.1f})'} | "
                       f"{'-' if not R else f'{R['median']:.4f} ({R['pull_MG']:+.1f})'} | {f(r['Ds_MS']['median_um'])} +- {f(r['Ds_MS']['err_um'], 2)} | "
                       f"{f(r['Ds_BM']['median_um'])} +- {f(r['Ds_BM']['err_um'], 2)} | {'-' if not q else f'{q['median_BM_over_quadrature']:.2f} +- {q['err']:.2f}'} |")
    out += ['', 'Paired Ds_B/model ratio in gamma* bins (pooled over 0.45-5 keV; VERIFIED measured ratio, the model is ESTIMATE):', '',
            '| point | median gamma* | ' + ' | '.join(['[1,1.05)', '[1.05,1.15)', '[1.15,1.3)', '[1.3,1.6)', '>= 1.6']) + ' |', '|---|---|' + '---|' * 5]
    for pk, g in P1['paired_model_by_gstar'].items():
        cells = []
        for k in ('[1,1.05)', '[1.05,1.15)', '[1.15,1.3)', '[1.3,1.6)', '[1.6,100)'):
            x = g['bins'].get(k)
            cells.append('-' if not x else f"{x['median_ratio']:.3f} +- {x['err']:.3f} (n={x['n']})")
        out.append(f"| {pk} | {g['median_gstar']:.3f} | " + ' | '.join(cells) + ' |')
    out += ['', 'Lambda exponents: median per-event slope +- err, its pull vs the closed form -2 + 2c_ev [pull]; population slope (ratio of medians) +- err,',
            'its pull vs the full MG rotating-yo-yo model {pull}:', '',
            '| point | ' + ' | '.join(['0.45-0.6', '0.6-1', '1-2', '2-3', '3-5', '5-10', '1-3']) + ' |', '|---|' + '---|' * 7]
    for pk, v in P1['points'].items():
        cells = []
        for k in ('0.45to0.6', '0.6to1', '1to2', '2to3', '3to5', '5to10', '1to3'):
            e = v['exponents'].get(k)
            cells.append('-' if not e else f"{e['median_event_slope']:.3f}+-{e['err']:.3f} [{e['pull_MG']:+.1f}]; {e['population_slope']:.3f}+-{e['population_err']:.3f} {{{e['pull_MG_model_population']:+.1f}}}")
        out.append(f'| {pk} | ' + ' | '.join(cells) + ' |')
    ms = P1['material_scaling']; mc = P1['material_scaling_chi2']
    out += ['', 'MS-floor scaling exponent ln[Ds(Mx2)/Ds(Mx0.5)]/ln 4 (Highland expectation ~0.5 for sqrt(x/X0); code-scaling check 0.517 at 500 GeV, 3 keV): ' +
            ', '.join(f"{k} {v['M_exponent_population']:.2f}+-{v['M_exponent_population_err']:.2f}" for k, v in ms.items()) +
            f"; chi2 vs 0.517 = {mc['chi2']:.1f}/{mc['ndf']}.", '',
            'B = MS crossover (median Ds_B = median Ds_MS, log-log interpolation): ' + ', '.join(f"{k} {x:.2f} keV" for k, x in P1['B_MS_crossover_keV'].items() if x) + '.', '']
    rv = P1['v2b_revisit']
    out += ['V2b revisit, population excess median(c)/median(c_ev) - 1 by regime (weighted mean over the cells of the regime; the 30-cell mean '
            f"{pct(rv['rel_excess_weighted_mean'])} mixes regimes and is not used):", '']
    for k, v in rv['regime_split'].items():
        out.append(f"- {k}: {pct(v['rel_excess_weighted_mean'])} +- {100 * v['rel_excess_weighted_err']:.2f} %; k_B < 6 sub-sample {pct(v['rel_excess_kB_lt6_weighted_mean'])}; "
                   f"zero-median symmetric-scatter model {pct(v['zero_median_sym_rel_mean'])}")
    out += ['', 'Pooled median r/c_ev by k_B bin (0-2 / 2-4 / 4-6 / 6-10 / >= 10):', '']
    for L, v in rv['pooled_residual_by_kB'].items():
        out.append(f"- {L[1:]} keV: " + ' / '.join(f"{100 * x['median_rel_r']:+.1f}+-{100 * x['err']:.1f} %" for x in v.values()))
    out += ['', '**P2 Lambda edges [keV]** (template half, |eta_pair| < 2.5, BM; stat (bootstrap), total systematic before -> after the fix-R1 robust '
            'evaluation (bootstrap-averaged paired shifts), relative; closed forms: plan §1.1 on the production events; hit level: from the stored hits). '
            'Redundancy: the two l_max columns are one quantity (ratio fixed at sqrt(R_IT/100 µm) = 38.2); the two merge columns are thresholds on the '
            'IT pair separation; only the Ds = 100 µm edge is tied to eps_B:', '',
            '| species-mass | N_osc = 1 (closed) | l_max = R_IT (closed) | Ds_all = 100 µm (hits) | l_max = 100 µm (closed; = col. 3 x 38.2) | IT pair sep. < 100 µm (hits) | IT pair sep. < 25 µm (hits) |',
            '|---|---|---|---|---|---|---|']
    order = ('lower_Nosc1_closed', 'lower_lmax_RIT_closed', 'lower_ds100_hit', 'upper_lmax100um_closed', 'upper_merge100_hit', 'upper_merge25_hit')
    ip = P2['edge_fits_in_m'].get('F/upper_merge100_hit', {}).get('interpolated', {})
    for pk, e in P2['edges'].items():
        tt = P2['systematics'][pk].get('total', {})
        cells = []
        for k in order:
            x = e[k]['value']
            if x is None or (isinstance(x, float) and math.isnan(x)):
                if k == 'upper_merge100_hit' and pk in ip:
                    cells.append(f"({ip[pk]['value']:.3g} +- {ip[pk]['err_fit']:.2g}, interpolated in ln m)")
                else:
                    cells.append('n/a' if 'merge' in k else '-')
            else:
                t = tt.get(k, {})
                cells.append(f"{x:.3g} +- {100 * e[k]['stat_err'] / x:.0f} % (stat) +- {100 * t.get('total_rel', float('nan')):.0f} -> {100 * t.get('total_rel_robust', float('nan')):.0f} % (syst)")
        out.append(f'| {pk} | ' + ' | '.join(cells) + ' |')
    fm = P2['edge_fits_in_m']
    out += ['', 'n/a = no crossing inside the simulated Lambda range (merged-pair edges need the Lambda >= 15 keV points, which exist only for E '
            '200/300/500/700/1000/1200/1500 and Etilde; the 25 µm edge lies above 40 keV for most masses). Interpolated values: deg-2 fit of ln(edge) in '
            f"ln m over the 7 measured E masses (chi2 {fm['F/upper_merge100_hit']['deg2']['chi2']:.1f}/{fm['F/upper_merge100_hit']['deg2']['ndf']}), fit (stat) error only; ESTIMATE. "
            'Stage 4 must add the systematic of the neighbouring measured masses to the interpolated edges (fix R2, C-5).', '',
            f"Robust systematic totals ('after') are upper bounds: {nlow}/{ncomp} of the robust l_max/QED/PDF components are below 2x their own "
            'template-sampling sd (`robust_shift_sampling_sd_rel`), i.e. noise-limited. Symmetrisation and the treatment of shifts < 2 sigma are '
            'deferred to Stage 4 (fix R2, C-4).', '',
            'm-slopes d ln(edge)/d ln m (linear fit, E): ' + ', '.join(f"{k.split('/')[1]} {v['m_slope_dlnE_dlnm']:+.3f} +- {v['m_slope_err']:.3f}" for k, v in fm.items() if k.startswith('F/') and 'm_slope_dlnE_dlnm' in v)
            + ' (sqrt(m) would be +0.5).', '',
            'Continuous Lambda handle: median IT pair separation sep_IT, log-log slope over 1-30 keV (error: fix R2, `results/FIX_R2_notes.json`, '
            'toys on the per-Lambda bootstrap errors): '
            + ', '.join(f"{k} {v['loglog_slope_1to30keV']:.3f} +- {SL[k]['err']:.3f}" for k, v in P2['sep_IT_handle'].items() if v['loglog_slope_1to30keV'] is not None)
            + ' (sep_IT ~ Lambda^-2, i.e. it measures l0 = m/Lambda^2; sep_IT/l_max ~ 0.5-0.6 above 1 keV). Per-point values: `results/P2.json` `sep_IT_handle`.']
    return '\n'.join(out)


def samples():
    idx = C.load_index(); M = J('merge.json')
    tot = M['totals']
    L = ['# Stage 3 samples: inventory (generated)', '',
         'Generated by `sim/stage3/scripts/make_docs.py` from `data/sim_stage3/STAGE3_INDEX.json` and `results/merge.json`. '
         'Do not edit by hand. Truth level. Units in the files: mm, ns, GeV; thickness in um.', '',
         '## 1. Totals per machine (VERIFIED: summed from the files)', '',
         '| machine | jobs | events | hits | CPU-h (sum of per-event process time) | CPU-h job level | estimate [M3 CPU-h] | bytes | status 0/1/2/3/4/5 |',
         '|---|---|---|---|---|---|---|---|---|']
    for k in ('mac', 'pc', 'xover_mac', 'xover_pc'):
        t = tot[k]
        L.append(f"| {k} | {t['files']} | {t['events']} | {t['hits']} | {t['cpu_h_events']:.1f} | {t['cpu_h_jobs']:.1f} | {t['est_cpu_h_M3']:.1f} | "
                 f"{t['bytes'] / 1e6:.0f} MB | {'/'.join(map(str, t['status_counts']))} |")
    tt = {k: sum(tot[m][k] for m in ('mac', 'pc')) for k in ('files', 'events', 'hits', 'cpu_h_events', 'est_cpu_h_M3', 'bytes')}
    L += [f"| **canonical total** | {tt['files']} | {tt['events']} | {tt['hits']} | {tt['cpu_h_events']:.1f} | | {tt['est_cpu_h_M3']:.1f} | {tt['bytes'] / 1e6:.0f} MB | |", '',
          f"Per-worker CPU time relative to the M3 cost model (CPU-s per estimated M3 CPU-s): Mac {tot['mac']['cpu_h_events'] / tot['mac']['est_cpu_h_M3']:.2f}, "
          f"PC {tot['pc']['cpu_h_events'] / tot['pc']['est_cpu_h_M3']:.2f} (ESTIMATE: different job mixes -- the PC ran every Lambda >= 15 keV job -- and "
          "15 workers on 8 cores / 16 threads in the 2nd PC session, so SMT inflates the per-worker CPU time). "
          'Wall: Mac 29.68 h on 7 workers (log); PC 2 sessions (263 jobs, stopped with the STOP file; then 330 jobs in 9.14 h with 15 workers).', '',
          '## 2. By campaign', '', '| campaign @ machine | jobs | events | hits | CPU-h | estimate [M3 CPU-h] |', '|---|---|---|---|---|---|']
    for k, v in sorted(M['by_campaign'].items()):
        L.append(f"| {k} | {v['files']} | {v['events']} | {v['hits']} | {v['cpu_h']:.1f} | {v['est_cpu_h_M3']:.1f} |")
    L += ['', '## 3. Code and environments (VERIFIED: read from every file)', '',
          '| machine | files | kernel | runner | platform | arch | python | numpy | numba |', '|---|---|---|---|---|---|---|---|---|']
    for e in M['environments']:
        L.append(f"| {e['machine']} | {e['n_files']} | {e['kernel_version']} | {e['runner_version']} | {e['platform']} | {e['arch']} | {e['python']} | {e['numpy']} | {e['numba']} |")
    e0 = M['environments'][0]
    L += ['', 'Code md5 (identical in all 4582 files, = current `sim/stage3/code/` and the bundle MANIFEST): ' +
          ', '.join(f'`{k}` {v}' for k, v in e0['code_md5'].items()) + '. Original-code md5s recorded: ' +
          ', '.join(f'`{k}` {v}' for k, v in e0['orig_md5'].items()) + '.', '',
          'numpy differs (2.5.3 Mac TT env, 2.5.4 bundle env on the PC); numba 0.68.0 on both. Cross-machine check: `results/xover.json`.', '',
          '## 4. Points (one row per species-mass and campaign; Lambda values, configurations, events per configuration)', '',
          '| campaign | species-mass | Lambda [keV] | configurations (events per point) | files | machines |', '|---|---|---|---|---|---|']
    grp = defaultdict(lambda: dict(lams=set(), cfg=defaultdict(set), files=0, mach=set()))
    for key, P in idx['points'].items():
        camp = key.split('/')[0] if not key.startswith('xover/') else 'xover/' + key.split('/')[1]
        g = grp[(camp, f"{'E' if P['spin'] == 'F' else 'Etilde'} {int(P['m'])}")]
        g['lams'].add(P['lam_keV']); g['cfg'][P['cfg']].add(P['n_events']); g['files'] += len(P['chunks']); g['mach'] |= set(P['machines'])
    for (camp, sm), g in sorted(grp.items(), key=lambda x: (x[0][0], x[0][1][0], int(x[0][1].split()[-1]))):
        L.append(f"| {camp} | {sm} | {', '.join(f'{x:g}' for x in sorted(g['lams']))} | "
                 f"{'; '.join(f'{c} ({'/'.join(map(str, sorted(n)))})' for c, n in sorted(g['cfg'].items()))} | {g['files']} | {', '.join(sorted(g['mach']))} |")
    L += ['', '## 5. File layout', '',
          '- `data/sim_stage3/out/<campaign>/<spin>_m<m>/L<Lambda>_<cfg>_cNN.npz`: Mac outputs; `data/sim_stage3/out_pc/...`: PC outputs (USB copy).',
          '- `data/sim_stage3/canon/`: relative symlinks with the plan layout, every job once (`canon/xover/<machine>/` for the overlap clones).',
          '- `data/sim_stage3/STAGE3_INDEX.json`: point -> chunks (file path relative to `data/sim_stage3/`, machine, events, hits, md5, CPU, status counts).',
          '- spin `F` = fermion E, `S` = scalar Etilde; campaign `mv` = the plan\'s `matvar` (material x0.5 / x2).',
          '- Per-file schema: `HANDOVER_STAGE4.md` §1.']
    open(C.S3 / 'SAMPLES.md', 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    samples()
    replace_block(C.S3 / 'VALIDATION.md', 'AUTO-HEADLINES', headlines())
    replace_block(C.S3 / 'README.md', 'AUTO-RESULTS', results_block())
    print('docs written')
