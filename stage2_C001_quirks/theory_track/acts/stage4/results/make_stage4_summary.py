"""Build data/acts_stage4/analysis/STAGE4_SUMMARY.json (schema 'STAGE4_SUMMARY v2') and the helper tables
acts/stage4/results/tables_<run>.md from ONE frozen non-DEV Stage-4 analysis run (default C12FC_v1).

Read-only on every input.  Standard library only, so it runs with `python3 -I`:

    python3 -I acts/stage4/results/make_stage4_summary.py            # from the theory_track root
    python3 -I acts/stage4/results/make_stage4_summary.py --run C12FC_v1 --compare C12_v1

Supersedes the session-scratchpad scripts headline.py / summary.py / tables.py (2026-10-16 09:44) that produced the
C12_v1 summary (kept as STAGE4_SUMMARY_C12v1.json).  Logic of the extraction is the same; added: A2FC revert, toy
bands, asymptotic/toys ratio, class composition per rung, D11 readings, edges/sep_IT/acceptance products, cited
investigation numbers (read from data/acts_stage4/investigation/*.json, not transcribed).

Tags in the output: VERIFIED = read from the run outputs (or a direct ratio/sum of such numbers); ESTIMATE = derived
here or model-dependent; UNVERIFIED = transcribed.
"""
import argparse
import glob
import hashlib
import json
import math
from pathlib import Path

TT = Path(__file__).resolve().parents[3]
ANA = TT / 'data' / 'acts_stage4' / 'analysis'
INV = TT / 'data' / 'acts_stage4' / 'investigation'
PROD = TT / 'data' / 'acts_stage4' / 'prod'
XSEC = TT / 'sim' / 'results' / 'xsec.json'
L_FB = 3000.0                                      # 3 ab^-1 in fb^-1
BUDGET_C, BUDGET_SUM = 0.11, 0.3                   # WP_RULE per-category / combined budget
REPORT = ('R_A', 'R_B', 'R_C', 'R_D', 'R_E')
SPM = ('F200', 'F500', 'F1000', 'F1500', 'S500')


def J(p):
    return json.load(open(p))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def cls(label):
    return 'PU' if label.startswith('PU') else ('SM' if label.startswith('SM') else 'Cprime')


def sigma_norm_fb():
    """sigma_norm per species-mass from sim/results/xsec.json (E: sigma_norm_nic2_fb, includes N_IC = 2; S: TH column)."""
    x = J(XSEC)
    o = {f'F{m}': x['normalisation_E']['rows'][str(m)]['sigma_norm_nic2_fb'] for m in (200, 500, 1000, 1500)}
    o['S500'] = x['normalisation_S']['500']['sigma_norm_nic2_fb']
    return o


NPZ_SIM = TT / 'data' / 'sim' / 'npz'


def tail_fraction():
    """f = P(pT(QQ) > 200 GeV, |eta_pair| < 4) per species-mass: the population the Stage-3 p2 template (and hence
    acceptance.json A_trig_presel) is conditional on (sim/stage3/code/make_inputs.py: TRGS, ptmin 200, eta_max 4).
    FIX R3-NORM (INV_NORM_F200): N_exp = sigma_norm x f x L x A; before this fix f was omitted (ratios too optimistic
    by 1/f).  E: xsec.json trigger_yields_E.rows[m].f_pt200_TRG_over_INC (= sum w_TRGS(pT > 200) / sigma_ref, the
    mg_events.sigma_norm_fb convention).  S (no xsec.json row): computed here exactly as in
    acts/stage4/investigation/inv_norm_f200.py, sum w(pT_pair > 200, |eta_pair| < 4) / sigma_ref_fb of
    data/sim/npz/S-TRGS_m500.npz."""
    x = J(XSEC)
    o = {}
    for m in (200, 500, 1000, 1500):
        o[f'F{m}'] = dict(value=x['trigger_yields_E']['rows'][str(m)]['f_pt200_TRG_over_INC'],
                          source=f'sim/results/xsec.json trigger_yields_E.rows.{m}.f_pt200_TRG_over_INC',
                          tag='VERIFIED (xsec.json; = INV_NORM_F200 f_p2 to < 2e-4 relative)')
    p = NPZ_SIM / 'S-TRGS_m500.npz'
    z = _npz(p, ('w', 'pt_pair', 'eta_pair', 'sigma_ref_fb'))
    num = sum(w for w, pt, eta in zip(z['w'], z['pt_pair'], z['eta_pair']) if pt > 200 and abs(eta) < 4)
    o['S500'] = dict(value=num / z['sigma_ref_fb'], source=f'{p.relative_to(TT)}: sum w(pT_pair > 200, |eta_pair| < 4) '
                                                           f'/ sigma_ref_fb (as inv_norm_f200.py)',
                     tag='VERIFIED (computed from the TRGS npz; = INV_NORM_F200 f_p2)')
    inv = INV / 'inv_norm_f200.json'
    if inv.exists():
        fi = J(inv)['f']
        for k, v in o.items():
            v['inv_norm_f200_f_p2'] = fi[k]['f_p2']
    return o


def terms_summary(terms):
    agg = {}
    for t in terms:
        agg[cls(t['label'])] = agg.get(cls(t['label']), 0.0) + t['value']
    top = sorted(terms, key=lambda t: -t['value'])[:3]
    return agg, [dict(label=t['label'], value=t['value'], zero_bound=t.get('zero_branch')) for t in top]


# ------------------------------------------------------------------------------------------------ headline
def headline(D):
    bs, bg, se, ss, lim, acc = (J(D / f) for f in ('bsum_wp.json', 'background.json', 'signal_eff.json',
                                                   'signal_srt.json', 'limits.json', 'acceptance.json'))
    man = J(D / 'manifest.json')
    SN = sigma_norm_fb()
    TF = tail_fraction()
    out = dict(source_dir=str(D.relative_to(TT)), label=bs['label'], provenance=bs['provenance'],
               n_trig=dict(value=bs['n_trig']['value'], rel_stat=bs['n_trig']['rel_stat']),
               samples=bg['samples'], wp=bs['rule']['wp'], complete_inputs=bs['rule'].get('complete_inputs'),
               runtime_s=man.get('runtime_s'), schema_check=man.get('schema_check'),
               status={k: dict(manifest=v['manifest'], used=v['used'], replaced_events=v['replaced_events'],
                               missing=v['missing']['n'], invalid=v['invalid']['n'],
                               not_admitted=v['not_admitted']['n'], excluded=v['excluded']['n'])
                       for k, v in man['status'].items()})
    # ladder per category
    lad = {}
    for c in ('T', 'G'):
        rows = []
        for r in bs['ladder'][c]:
            agg, top = terms_summary(r['terms'])
            put = [t for t in r['terms'] if t['label'].startswith('PU')]
            pu = dict(value=sum(t['value'] for t in put),
                      sigma_ln=max(math.sqrt(sum(v * v for v in t['comps'].values())) for t in put) if put else None,
                      comps=put[0]['comps'] if put else None, zero_branch=any(t['zero_branch'] for t in put))
            rows.append(dict(rung=r['name'], B84=r['B84'], B_median=r['B_median'], zero_branch=r['zero_branch'],
                             pu_term=pu, central_by_class=agg, top3=top, top_term=top[0]['label'],
                             top_term_zero_bound=top[0]['zero_bound'],
                             decades_over_0p11=math.log10(r['B84'] / BUDGET_C)))
        best = min(rows, key=lambda x: x['B84'])
        lad[c] = dict(rows=rows, min_B84=best['B84'], min_B84_rung=best['rung'],
                      min_decades_over_0p11=math.log10(best['B84'] / BUDGET_C),
                      first_rung_fails=next(r['rung'] for r in rows if r['B84'] > BUDGET_C))
    out['ladder'] = lad
    fb = {}
    for k, v in bs['ladder']['FB'].items():
        fb[k] = {}
        for c in ('T', 'G'):
            agg, top = terms_summary(v[c]['terms'])
            fb[k][c] = dict(B84=v[c]['B84'], B_median=v[c]['B_median'], central_by_class=agg, top3=top,
                            top_term=top[0]['label'])
    out['fallback_B'] = fb
    es = {}
    for key in ('end_state', 'end_state_T'):
        es[key] = {e['column']: dict(P_per_trial=e['P_per_trial'], B=e['P_per_trial'] * bs['n_trig']['value'],
                                     closure_factor=e['closure_factor'], sigma_ln=e['sigma_ln'],
                                     sigma_ln_components=e['sigma_ln_components'], zero_branch=e['zero_branch'],
                                     reachable_rho2=e['reachable_rho2']) for e in bg[key]}
    out['pu_end_state'] = es
    cl = bg['closure']
    out['closure'] = dict(T1=dict(rung=cl['T1']['r1'], ratio=cl['T1']['ratio'], z=cl['T1']['z'], lever=cl['T1']['lever'],
                                  branch=cl['T1']['branch']),
                          T1w=dict(rung=cl['T1w']['r1'], ratio=cl['T1w']['ratio'], z=cl['T1w']['z'],
                                   lever=cl['T1w']['lever'], branch=cl['T1w']['branch']),
                          T1e=cl['T1e']['branch'], trend_slope=cl['trend']['slope'],
                          trend_direction=cl['trend']['direction'], T3_informative=bg['T3']['informative'],
                          c_factor=bg['c_factor_applied'], reach=bg['reach'], reach_T=bg['reach_T'],
                          rho_dens=bg['rho_dens']['rho_dens'],
                          compounded_ge_R05=es['end_state']['R05_w<37.5']['closure_factor'])
    out['pu_reach_per_trial_rho2_k20'] = 1e-6 / bg['samples']['B2_trials']   # plan §4.1 step 2: 2^-20 / N_trials
    out['srt_window_ns'] = ss['window_ns']
    out['sm_proxy_fraction_of_B_SM'] = bg['sm'].get('_proxy_fraction_of_B_SM')
    # C' per-topology summary (D11 readings, low gun count, V4-10)
    cpo = {}
    for t, v in bg['cprime'].items():
        rd = {}
        for r in v['rows']:
            u = (r.get('dedx_readings') or {}).get('used')
            if u:
                rd[u] = rd.get(u, 0) + 1
        cpo[t] = dict(f_pre=v['f_pre'], v410_leak=v['v410_leak'], low_gun_count=(v.get('low_gun_count') or {}).get('applied'),
                      rate_t=v.get('rate', {}).get('value') if isinstance(v.get('rate'), dict) else v.get('rate'),
                      dedx_reading_used=rd)
    out['cprime'] = cpo
    # signal + limits
    sig = {}
    adm = se['admissibility']
    for k, x in se['a2']['points'].items():
        sp, m, l = x['spin'], int(x['m']), x['lam']
        a = adm[f"{sp}|{m}|{l:g}"]
        rfb = a['r_fb']
        a5 = se['a5']['points'].get(k.replace('A2', 'A5'))
        li = lim['points'].get(k, {})
        A = acc['points'][k]['A_trig_presel']
        ft = TF[f'{sp}{m}']['value']                 # FIX R3-NORM: A is conditional on pT(QQ) > 200 GeV, |eta| < 4
        n_exp = SN[f'{sp}{m}'] * ft * L_FB * A
        toys = li.get('expected_toys') or {}
        asy = li.get('expected_asymptotic') or {}
        mu = li.get('expected_primary')
        sig[k] = dict(spin=sp, m=m, lam=l, n_den=x['n_den'], k_adm=a['k_adm'], e_adm=a['e_adm'], r_fb=rfb,
                      k_consistent=a['k_consistent'], replaced_by_a2fc=bool(x.get('replaced_by_a2fc')),
                      eps_A2={r: x['report_rungs'][r]['eps'] for r in REPORT},
                      eps_A2_cp68={r: x['report_rungs'][r]['cp68'] for r in REPORT},
                      eps_A2_rfb=x['fallback'][rfb]['eps'], eps_A2_rfb_cp68=x['fallback'][rfb]['cp68'],
                      eps_A2_SRT_rfb=ss['points'][k]['fallback_SRT'][rfb]['eps'],
                      eps_A5={r: a5['report_rungs'][r]['eps'] for r in REPORT} if a5 else None,
                      A_trig_presel=A, A_factors={kk: vv for kk, vv in acc['points'][k]['factors'].items()
                                                  if isinstance(vv, float)},
                      sigma_norm_fb=SN[f'{sp}{m}'], f_tail=ft, A_incl=A * ft,
                      n_pt200_before_cuts=SN[f'{sp}{m}'] * ft * L_FB,
                      limit=dict(selections=li.get('selections'), s=li.get('s'), b=li.get('b'),
                                 sigma_ln=li.get('sigma_ln'), mu95_toys=mu,
                                 mu95_toys_band1s=toys.get('band_1s'), mu95_toys_band2s=toys.get('band_2s'),
                                 mu95_asym=asy.get('median'), mu95_asym_band1s=asy.get('band_1s'),
                                 asym_over_toys=(asy['median'] / mu) if (mu and asy.get('median')) else None,
                                 sigma95_fb=(mu / (L_FB * A * ft)) if mu else None,   # on inclusive sigma(pp->QQ)
                                 n_exp_signal=n_exp, S_at_rfb=n_exp * x['fallback'][rfb]['eps'],
                                 mu95_over_nexp=(mu / n_exp) if mu else None,
                                 mu_5sigma=(li.get('discovery') or {}).get('mu_5sigma'),
                                 mu_3events=(li.get('discovery') or {}).get('mu_3events')))
    out['signal'] = sig
    out['tail_fraction'] = TF
    rv = se['a2'].get('a2fc_revert') or dict(points={})
    out['a2fc_revert'] = {k: {kk: vv for kk, vv in v.items() if kk != 'jobs'} | dict(n_jobs=len(v['jobs']))
                          for k, v in rv['points'].items()}
    out['a2fc_revert_meta'] = {k: v for k, v in rv.items() if k != 'points'}
    # products
    ed = J(D / 'edges_det.json')
    E = {}
    for k, v in ed['points'].items():
        t = v['truth']
        E[k] = dict(R04_lower=v['R04']['lower'], R04_upper=v['R04']['upper'],
                    R14_lower=v['R14']['lower'], R14_upper=v['R14']['upper'],
                    truth={n: dict(value=t[n]['value'], stat_err=t[n]['stat_err']) for n in t})
    out['edges_det'] = E
    sp_ = J(D / 'sep_it_det.json')
    out['sep_it_det'] = dict(pu200_measurable=sp_.get('pu200_measurable'), pu200_note=sp_.get('pu200_note'),
                             points={k: v for k, v in sp_['points'].items()
                                     if k.endswith('|BM') and (k.startswith('A2') or k.startswith('A5')
                                                               or k.split('|')[1] + k.split('|')[2] in
                                                               ('F200', 'F500', 'F1000', 'F1500', 'S500'))})
    out['input_sha256'] = {f: sha(D / f) for f in ('bsum_wp.json', 'limits.json', 'signal_eff.json',
                                                    'background.json', 'manifest.json')}
    return out


# ------------------------------------------------------------------------------------------------ cited inputs
def cited():
    """Investigation numbers cited by the report, read from their json outputs (VERIFIED by the investigators)."""
    o = {}
    v43 = {}
    for s in SPM:
        p = INV / f'a1_ladder_{s}.json'
        if p.exists():
            d = J(p)
            v43[s] = {l: dict(n=v['n'], matched_any=v['matched_any'], matched_R04=v['matched_R04'],
                              all_eta_eps_R04=v['all_eta_eps_R04'], barrel_fraction=v['barrel_fraction'])
                      for l, v in d.items()}
    o['V4_3_A1_barrel'] = dict(source='data/acts_stage4/investigation/a1_ladder_*.json (INV_SIGNAL_EFF §1)',
                               definition='A1 (no PU), |eta_pair| < 1, status 1, not probe-excluded; matched_any = '
                                          'some candidate with >= 50 % of the written quirk hits', points=v43)
    td = {}
    for s in SPM:
        p = INV / f'truth_degeneracy_{s}.json'
        if p.exists():
            td[s] = J(p)
    o['truth_degeneracy'] = dict(source='data/acts_stage4/investigation/truth_degeneracy_*.json (INV_SIGNAL_EFF §3.1)',
                                 points=td)
    p = INV / 'a2fc_summary.json'
    o['a2fc_injob'] = J(p) if p.exists() else None
    return o


def cpu_hours():
    """Sum of job walls per campaign from the production progress logs (single-threaded jobs: ~ CPU-h)."""
    out = {}
    for f in ('C1', 'C2', 'A2FC'):
        p = next(iter(glob.glob(str(PROD / f / '_progress_*.jsonl'))), None)
        if not p:
            continue
        camp, seen = None, {}
        for line in open(p):
            d = json.loads(line)
            if d['event'] == 'start':
                camp = d.get('campaign')
            elif d['event'] == 'done':
                seen[(camp, d['id'])] = d['wall']
        for (c, _), w in seen.items():
            out.setdefault(c, dict(jobs=0, cpu_h=0.0))
            out[c]['jobs'] += 1
            out[c]['cpu_h'] += w / 3600
    return out


def p1_block():
    """P1 (B-field coplanarity vs the MS floor): truth level only (plan D4-9); read from the U-2 panel."""
    p = TT / 'acts' / 'stage4' / 'u2_panel' / 'u2_panel.json'
    u = J(p)
    return dict(detector_level='NOT MEASURED (plan D4-9: event-level out-of-plane resolution 23-30 um = MS floor; '
                               'no detector-level coplanarity observable in the frozen Stage-4 outputs)',
                truth_source=str(p.relative_to(TT)), r_q_by_lambda_band=u['summary']['by_lambda_band'],
                lambda_cross_keV=u['lambda_cross_keV'], tag='VERIFIED (truth level, Stage-3 P1 / U-2 panel)')


# ------------------------------------------------------------------------------------------------ m_Q observables
def _npz(p, names):
    """Minimal stdlib reader of the numeric / bool / unicode arrays of a numpy .npz (no numpy in python3 -I)."""
    import array
    import ast
    import zipfile
    z, out = zipfile.ZipFile(p), {}
    for nm in z.namelist():
        k = nm[:-4]
        if k not in names:
            continue
        b = z.read(nm)
        off = 10 if b[6] == 1 else 12
        hl = int.from_bytes(b[8:off], 'little')
        hd = ast.literal_eval(b[off:off + hl].decode())
        raw, dt, sh = b[off + hl:], hd['descr'], hd['shape']
        n = 1
        for s in sh:
            n *= s
        if dt in ('<f8', '<i8'):
            a = array.array('d' if dt == '<f8' else 'q')
            a.frombytes(raw[:8 * n])
            a = a.tolist()
        elif dt == '|b1':
            a = [x != 0 for x in raw[:n]]
        elif dt.startswith('<U'):
            w = 4 * int(dt[2:])
            a = [raw[i * w:(i + 1) * w].decode('utf-32-le').rstrip('\x00') for i in range(max(n, 1))]
        else:
            raise ValueError(f'{p}:{k}: unsupported dtype {dt}')
        if len(sh) == 2:
            a = [a[i * sh[1]:(i + 1) * sh[1]] for i in range(sh[0])]
        elif len(sh) == 0:
            a = a[0]
        out[k] = a
    return out


def _q(v, p):
    """Quantile with linear interpolation (numpy default), v already finite."""
    v = sorted(v)
    if not v:
        return None
    x = (len(v) - 1) * p
    i = int(math.floor(x))
    return v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * (x - i)


def clopper_pearson(k, n, cl=0.6826894921370859):
    """Exact (Clopper-Pearson) central binomial interval by bisection on the binomial tail (stdlib)."""
    a = (1 - cl) / 2

    def tail_ge(p):    # P(X >= k | p)
        return sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))

    def bis(f, target, inc):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if (f(mid) < target) == inc:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else bis(tail_ge, a, True)
    hi = 1.0 if k == n else bis(lambda p: 1 - tail_ge(p) + math.comb(n, k) * p ** k * (1 - p) ** (n - k), a, False)
    return [lo, hi]


def mass_observables(D, signal):
    """D4-13 (a) m_Q / l_max observables (plan l. 997, 1856), re-extracted from signal_obs_{a1,a2}.npz with the same
    selection as the C12_v1 summary: B-field model BM only, signal-matched candidates passing R04, first (lowest-index)
    matched candidate per (point, row), finite values only, pooled over Lambda per species-mass.  Added: the same at
    each A2 point's r_fb (FB_k & h > 5 & o > 5 & f_CKF < 0.2, i.e. the epsilon definition), and per-point w_core
    medians at R04.  A2 includes the A2FC full-chain rows at the 9 revert points."""
    cols = ['key', 'row', 'L', 'FB', 'FB_names', 'M_est', 'beta_tof', 'dedx', 'w_core', 'f_ckf']
    grid = sorted({v['lam'] for v in signal.values()})
    rfb = {k: v['r_fb'].split('&')[0] for k, v in signal.items()}
    fin = lambda d, ii, c: [d[c][i] for i in ii if math.isfinite(d[c][i])]  # noqa: E731

    def stats(d, ii):
        M, b, e = fin(d, ii, 'M_est'), fin(d, ii, 'beta_tof'), fin(d, ii, 'dedx')
        r = lambda v, p, nd: None if _q(v, p) is None else round(_q(v, p), nd)  # noqa: E731
        return dict(n=len(ii), M_est_finite_fraction=round(len(M) / len(ii), 3) if ii else None,
                    M_est_GeV=dict(median=r(M, .5, 0), q16=r(M, .16, 0), q84=r(M, .84, 0)),
                    beta_tof=dict(median=r(b, .5, 3), q16=r(b, .16, 3), q84=r(b, .84, 3)),
                    dedx_MIP=dict(median=r(e, .5, 3), q16=r(e, .16, 3), q84=r(e, .84, 3)))

    out = {}
    pair = {}
    for kind in ('a1', 'a2'):
        d = _npz(D / f'signal_obs_{kind}.npz', cols + ['m'])
        seen, n_ev, rat = set(), 0, []
        for i, k in enumerate(d['key']):          # R04 & f_CKF < 0.2 (epsilon definition), first per (point, row)
            if k.split('|')[4] != 'BM' or not d['L'][i][3] or not d['f_ckf'][i] < 0.2 or (k, d['row'][i]) in seen:
                continue
            seen.add((k, d['row'][i]))
            n_ev += 1
            if math.isfinite(d['M_est'][i]):
                rat.append(d['M_est'][i] / d['m'][i])
        pair[kind.upper()] = dict(n_events=n_ev, n_defined=len(rat), median_M_est_over_mQ=round(_q(rat, .5), 3),
                                  n_below_0p5_mQ=sum(x < 0.5 for x in rat),
                                  frac_below_0p5_mQ=round(sum(x < 0.5 for x in rat) / len(rat), 4),
                                  n_below_1p5_mQ=sum(x < 1.5 for x in rat), min_M_est_over_mQ=round(min(rat), 3))
        fbi = {nm: i for i, nm in enumerate(d['FB_names'])}
        pooled_R04, pooled_rfb, point_R04 = {}, {}, {}
        seen_R04, seen_rfb = set(), set()
        for i, k in enumerate(d['key']):
            p = k.split('|')                       # kind|spin|m|lam|cfg
            sm = p[1] + p[2]
            if p[4] != 'BM' or sm not in SPM:
                continue
            if d['L'][i][3] and (k, d['row'][i]) not in seen_R04:       # R04 = L[:, 3]
                seen_R04.add((k, d['row'][i]))
                pooled_R04.setdefault(sm, []).append(i)
                point_R04.setdefault(k, []).append(i)
            ka = 'A2|' + '|'.join(p[1:])
            if kind == 'a2' and ka in rfb and d['FB'][i][fbi[rfb[ka]]] and d['f_ckf'][i] < 0.2 \
                    and (k, d['row'][i]) not in seen_rfb:
                seen_rfb.add((k, d['row'][i]))
                pooled_rfb.setdefault(sm, []).append(i)
        o = dict(pooled_R04={sm: stats(d, pooled_R04.get(sm, [])) for sm in SPM})
        if kind == 'a2':
            o['pooled_rfb'] = {sm: stats(d, pooled_rfb.get(sm, [])) for sm in SPM}
        wc = {}
        for k, ii in point_R04.items():
            p = k.split('|')
            if float(p[3]) in grid:
                w = fin(d, ii, 'w_core')
                wc[f'{p[1]}{p[2]}|{float(p[3]):g}'] = dict(n=len(w), median_mm=round(_q(w, .5), 2) if w else None)
        o['w_core_median_R04_by_point'] = dict(sorted(wc.items()))
        out[kind.upper()] = o
    m = {s: float(s[1:]) for s in SPM}
    rat = {kd: {s: out[kd]['pooled_R04'][s]['M_est_GeV']['median'] / m[s] for s in SPM} for kd in ('A1', 'A2')}
    out['M_est_over_m_R04'] = dict(values={kd: {s: round(v, 2) for s, v in r_.items()} for kd, r_ in rat.items()},
                                   range_A2=[round(min(rat['A2'].values()), 2), round(max(rat['A2'].values()), 2)],
                                   range_A1=[round(min(rat['A1'].values()), 2), round(max(rat['A1'].values()), 2)],
                                   tag='ESTIMATE (per-species median of the pair-mass proxy M_est / m_Q; '
                                       'M_est estimates M_QQbar >= 2 m_Q; not a calibrated m_Q measurement)')
    med = [out['A2']['pooled_R04'][s]['M_est_GeV']['median'] for s in ('F200', 'F500', 'F1000', 'F1500')]
    out['M_est_over_mQ_pooled'] = dict(
        values=pair, physics='M_est estimates the pair mass M_QQbar >= 2 m_Q (signal.py l. 203): the pooled median '
                             'is just above the 2 m_Q threshold (2.26 m_Q at PU 200, pulled down by the PU low '
                             'cluster; 2.46 m_Q without PU), not at m_Q',
        selection='BM; R04 & f_CKF < 0.2 (epsilon definition); first matched candidate per (point, row); pooled over '
                  'every point of the sample (A2: the 40 points; A1: every A1 BM point); cross-checked by '
                  'stage5/review/REVIEW_STAGE5_R2.md (1051 / 850 / 2.256 / 19.06 %)',
        tag='VERIFIED (detector level)')
    out['A2_E_monotone_in_m_R04'] = all(a < b for a, b in zip(med, med[1:]))
    out['selection'] = ('BM only; signal-matched candidates; R04 (L[:,3]) resp. r_fb (FB_k & h>5 & o>5 & f_CKF < 0.2); '
                        'first matched candidate per (point, row); finite values; pooled over Lambda (A1: every Lambda '
                        'of the A1 grid, A2: 0.45-5 keV); quantiles with linear interpolation. Same selection as '
                        'STAGE4_SUMMARY_C12v1.json M_est_median_* (reproduces those values exactly on C12_v1).')
    out['definition'] = 'M_est = MET * cosh(eta_axis) / (beta gamma)_ToF (BTL); NaN where beta_ToF >= 1 or undefined'
    out['not_produced'] = ('t_est / chi2 vs Lambda (the plan\'s P2 timing fit) and results/sensitivity.json are not '
                           'produced by the frozen pipeline; the limits and discovery mu are in limits.json.')
    out['tag'] = 'VERIFIED (detector level; read from signal_obs_a1/a2.npz of the primary run)'
    return out


def sign_test_p(a, b):
    """Exact two-sided sign (McNemar) test p for a vs b discordant pairs."""
    n, m = a + b, min(a, b)
    return min(1.0, 2 * sum(math.comb(n, j) for j in range(m + 1)) / 2 ** n)


def a2fc_paired_aggregate(revert_keys, fallback):
    """Paired numpy-A2 vs A2FC counts summed over the revert points other than E500 3 keV, read from the
    INV_A2FC_E500 output inv_a2fc_e500_paired.json (same rows, row by row)."""
    p = INV / 'inv_a2fc_e500_paired.json'
    if not p.exists():
        return None
    d = J(p)
    keys = [k for k in revert_keys if k != 'A2|F|500|3|BM']
    sel = {'R04': lambda v, k: v['ladder']['R04_IP2>=7'], 'R14': lambda v, k: v['ladder']['R14_2S2>=3'],
           'r_fb': lambda v, k: v['fb'][fallback[k]['r_fb'].split('&')[0]], 'FB3': lambda v, k: v['fb']['FB3']}
    o = {}
    for nm, f in sel.items():
        t = dict(k_numpy=0, k_fullchain=0, numpy_only=0, fullchain_only=0)
        for k in keys:
            x = f(d[k], k)
            t['k_numpy'] += x['k_a2']; t['k_fullchain'] += x['k_fc']
            t['numpy_only'] += x['a2_only']; t['fullchain_only'] += x['fc_only']
        t['ratio_fullchain_over_numpy'] = round(t['k_fullchain'] / t['k_numpy'], 3)
        t['sign_test_p'] = sign_test_p(t['numpy_only'], t['fullchain_only'])
        o[nm] = t
    o['points'] = keys
    o['n_rfb_ratio_le_1'] = sum(1 for k in keys if sel['r_fb'](d[k], k)['k_fc'] <= sel['r_fb'](d[k], k)['k_a2'])
    o['source'] = 'data/acts_stage4/investigation/inv_a2fc_e500_paired.json (INV_A2FC_E500 §1)'
    return o


SAMPLE_EVENTS = {"C' dif": 500, "C' pvpair": 500, "C' gamma": 500, 'SM Znunu_j': 2000}


def stats_reach(h, rungs=('R08_w<4.7', 'R09_p>1e-3')):
    """Re-check of INV_STATS_BKG §5 on the primary run: B84 of single bounded terms (value x e^sigma, central = median)
    and the events per sample that would bring that term alone to 0.11 if the zero persists (bound ~ 1/N)."""
    o = {}
    for rg in rungs:
        r = next(x for x in h['ladder']['G']['rows'] if x['rung'] == rg)
        pu = r['pu_term']
        d = dict(PU_alone_B84=pu['value'] * math.exp(pu['sigma_ln']), PU_central=pu['value'], PU_sigma_ln=pu['sigma_ln'])
        o[rg] = d
    D = TT / h['source_dir']
    bs = J(D / 'bsum_wp.json')
    for rg in rungs:
        r = next(x for x in bs['ladder']['G'] if x['name'] == rg)
        for t in r['terms']:
            if t['label'] in SAMPLE_EVENTS:
                sl = math.sqrt(sum(v * v for v in t['comps'].values()))
                b84 = t['value'] * math.exp(sl)
                n0 = SAMPLE_EVENTS[t['label']]
                o[rg][t['label']] = dict(central=t['value'], sigma_ln=sl, B84_alone=b84, zero_bound=t.get('zero_branch'),
                                         events_now=n0, events_needed_alone=n0 * b84 / BUDGET_C)
    o['tag'] = 'ESTIMATE (single log-normal per term; N_needed = N_now x B84_alone / 0.11, i.e. the bound ~ 1/N)'
    return o


# ------------------------------------------------------------------------------------------------ summary
def best_limit(h):
    return min((v['limit']['mu95_over_nexp'], k) for k, v in h['signal'].items() if v['limit']['mu95_over_nexp'])


def lad_short(h):
    keys = {'R_A': 'R04_IP2>=7', 'R_B': 'R06_w<18.75', 'R07': 'R07_w<9.4', 'R08': 'R08_w<4.7', 'R09': 'R09_p>1e-3',
            'R_D': 'R14_2S2>=3', 'R_E': 'R23_e>2.0'}
    o = {}
    for c in 'TG':
        rows = {r['rung']: r for r in h['ladder'][c]['rows']}
        o[f'SR-{c}'] = dict(min_B84=h['ladder'][c]['min_B84'], min_B84_rung=h['ladder'][c]['min_B84_rung'],
                            decades_over_0p11_at_min=h['ladder'][c]['min_decades_over_0p11'],
                            first_rung_failing=h['ladder'][c]['first_rung_fails'],
                            B84_at={k: rows[v]['B84'] for k, v in keys.items()},
                            B_median_at={k: rows[v]['B_median'] for k, v in keys.items()},
                            central_by_class_at={k: rows[v]['central_by_class'] for k, v in keys.items()},
                            top3_at={k: rows[v]['top3'] for k, v in keys.items()})
    return o


def build(h, hc, cit, cpu, run, cmp_run):
    best = best_limit(h)
    lim_pts = [v for v in h['signal'].values() if v['limit']['mu95_toys']]
    ratios = [v['limit']['asym_over_toys'] for v in lim_pts if v['limit']['asym_over_toys']]
    pts = {}
    for k, v in h['signal'].items():
        l = v['limit']
        pts[k] = dict(r_fb=v['r_fb'], k_adm=v['k_adm'], e_adm=v['e_adm'], replaced_by_a2fc=v['replaced_by_a2fc'],
                      eps_rfb=v['eps_A2_rfb'], eps_rfb_cp68=v['eps_A2_rfb_cp68'], eps_SRT_rfb=v['eps_A2_SRT_rfb'],
                      n_den=v['n_den'], k_rfb=round(v['eps_A2_rfb'] * v['n_den']),
                      eps_rfb_cp95=clopper_pearson(round(v['eps_A2_rfb'] * v['n_den']), v['n_den'], 0.95),
                      eps_reporting_rungs=v['eps_A2'], eps_A5=v['eps_A5'], A_trig_presel=v['A_trig_presel'],
                      f_tail=v['f_tail'], A_incl=v['A_incl'], N_pt200_before_cuts_3ab=v['n_pt200_before_cuts'],
                      sigma_norm_fb=v['sigma_norm_fb'], N_exp_3ab=l['n_exp_signal'], S_at_rfb=l['S_at_rfb'],
                      B84_rfb={c: h['fallback_B'][v['r_fb']][c]['B84'] for c in 'TG'},
                      B_median_rfb={c: h['fallback_B'][v['r_fb']][c]['B_median'] for c in 'TG'},
                      mu95_toys_events=l['mu95_toys'], mu95_toys_band1s=l['mu95_toys_band1s'],
                      mu95_toys_band2s=l['mu95_toys_band2s'], mu95_asymptotic_events=l['mu95_asym'],
                      asym_over_toys=l['asym_over_toys'], sigma95_fb=l['sigma95_fb'],
                      mu95_over_Nexp=l['mu95_over_nexp'], mu_5sigma=l['mu_5sigma'])
    fbB = {k: {c: dict(B84=v[c]['B84'], B_median=v[c]['B_median'], top_term=v[c]['top_term'],
                       central_by_class=v[c]['central_by_class']) for c in 'TG'} for k, v in h['fallback_B'].items()}
    # A2FC: like-for-like vs the numpy A2 of the comparison run (same rows)
    a2fc = {}
    for k, v in h['a2fc_revert'].items():
        o = dict(eps_R04_numpy=v['eps_R04_a2_numpy'], eps_R04_fullchain=v['eps_R04_a2fc'],
                 eps_R14_numpy=v['eps_R14_a2_numpy'], eps_R14_fullchain=v['eps_R14_a2fc'], n_den=v['n_den'])
        if hc and k in hc['signal']:
            o['eps_rfb_numpy'] = hc['signal'][k]['eps_A2_rfb']
            o['eps_rfb_fullchain'] = h['signal'][k]['eps_A2_rfb']
            o['r_fb'] = h['signal'][k]['r_fb']
            o['mu95_toys_numpy'] = hc['signal'][k]['limit']['mu95_toys']
            o['mu95_toys_fullchain'] = h['signal'][k]['limit']['mu95_toys']
        a2fc[k] = o
    a1 = {k: v for k, v in h['edges_det'].items() if k.startswith('A1|') and k.split('|')[1] + k.split('|')[2] in SPM}
    a2e = {k: v for k, v in h['edges_det'].items() if k.startswith('A2|')}
    sep = h['sep_it_det']['points']
    sepA2 = [v for k, v in sep.items() if k.startswith('A2|')]
    tot_cpu = sum(v['cpu_h'] for v in cpu.values())
    v43p = cit['V4_3_A1_barrel']['points']
    _r = [v43p[s_][l]['matched_R04'] for s_ in v43p for l in ('1.5', '2.0') if l in v43p[s_]]
    v43R04 = (min(_r), max(_r)) if _r else (float('nan'), float('nan'))
    mobs = mass_observables(TT / h['source_dir'], h['signal'])
    fcr = {k: v['eps_rfb_fullchain'] / v['eps_rfb_numpy'] for k, v in a2fc.items() if v.get('eps_rfb_numpy')}
    oth = [x for k, x in fcr.items() if k != 'A2|F|500|3|BM']
    pag = a2fc_paired_aggregate(list(h['a2fc_revert']), h['signal'])
    best0 = best_limit(h)
    fsys = dict(
        factor_rfb=pag['r_fb']['ratio_fullchain_over_numpy'], factor_R04=pag['R04']['ratio_fullchain_over_numpy'],
        n_points_affected=sum(1 for v in h['signal'].values() if not v['replaced_by_a2fc']),
        best_point_affected=not h['signal'][best0[1]]['replaced_by_a2fc'],
        best_ratio_corrected_rfb=best0[0] / pag['r_fb']['ratio_fullchain_over_numpy'],
        best_ratio_corrected_R04=best0[0] / pag['R04']['ratio_fullchain_over_numpy'],
        note='systematic full-chain inefficiency (CKF) measured at the 8 other revert points (3-5 keV, where the V4-6 '
             'CKF fraction exceeds 5 %); the 31 numpy-A2 points may overestimate eps by up to about this factor (the '
             'loss is likely smaller at <= 2 keV, where CKF stealing is below the 5 % revert threshold); applied here '
             'only as an ESTIMATE of the systematic on eps, not to any limit; no exclusion either way',
        tag='ESTIMATE (systematic on eps)') if pag else None
    S = dict(
        schema='STAGE4_SUMMARY v2',
        created='2026-10-16',
        built_by='acts/stage4/results/make_stage4_summary.py (python3 -I, stdlib only)',
        report='acts/stage4/STAGE4_RESULTS.md',
        superseded_versions=dict(summary='data/acts_stage4/analysis/STAGE4_SUMMARY_C12v1.json',
                                 report='acts/stage4/STAGE4_RESULTS_C12v1.md',
                                 note='written from C12_v1 (freeze bce02b6f, before FIX_ANALYSIS_R6 and A2FC); stale'),
        tags_note='VERIFIED = read from the frozen non-DEV outputs of the primary run (freeze b42aef4d...) or a direct '
                  'ratio of such numbers; ESTIMATE = derived here or model-dependent; UNVERIFIED = transcribed. '
                  'Detector level = ACTS-hybrid (Fatras + hybrid plane finder) in a public-geometry CMS-Phase-2-like '
                  'model, PU 200 normalised to the TDR occupancy, barrel only (|eta(n3)| < 1). Truth level = Stage-3 '
                  'generator/kernel quantities. No CMS software or CMS data.',
        primary_run=dict(dir=h['source_dir'], campaigns=h['provenance']['campaigns'], t_seed=h['provenance']['t_seed'],
                         freeze_sha256=h['provenance']['freeze_sha256'], dev=h['provenance'].get('dev'),
                         runtime_s=h['runtime_s'], schema_check=h['schema_check'], input_sha256=h['input_sha256'],
                         admission=h['status'], tag='VERIFIED'),
        comparison_run=dict(dir=hc['source_dir'], campaigns=hc['provenance']['campaigns'],
                            freeze_sha256=hc['provenance']['freeze_sha256'],
                            note='superseded (pre-R6 freeze, numpy A2 at the 9 revert points)') if hc else None,
        production=dict(cpu_h_by_campaign={k: dict(jobs=v['jobs'], cpu_h=round(v['cpu_h'], 1)) for k, v in cpu.items()},
                        cpu_h_total=round(tot_cpu, 1),
                        tag='VERIFIED as sum of job walls in prod/*/_progress_*.jsonl; ESTIMATE as CPU-h (1 core/job)'),
        outcome=dict(wp_T=h['wp']['T'], wp_G=h['wp']['G'], branch=h['wp']['branch'],
                     complete_inputs=h['complete_inputs'], tag='VERIFIED',
                     plain='No working point in SR-T or SR-G: B84 > 0.11 at every rung of both ladders; the '
                           'pre-defined fallback (plan 2.6 / WP_RULE 8, D4-17 (i)) applies at every (m, Lambda, spin). '
                           'No expected exclusion or discovery at any of the 40 A2 points.',
                     best_mu95_over_Nexp=dict(value=best[0], point=best[1],
                                              tag='ESTIMATE (mu95 VERIFIED toys; N_exp = sigma_norm (N_IC = 2) x f_tail '
                                                  'x L x A with sigma_norm and f_tail from sim/results/xsec.json (S: '
                                                  'TRGS npz) and truth-level A; eps(FB2) = 9/200, '
                                                  'CP68 [0.030, 0.065] (full statistical uncertainty); numpy-A2 eps: '
                                                  'full-chain systematic x 0.87 -> ratio ~ %.0f, see '
                                                  'a2fc_revert.fullchain_eps_systematic)'
                                                  % (fsys['best_ratio_corrected_rfb'] if fsys else float('nan')),
                                              value_before_fix_r3_norm=best[0] * h['signal'][best[1]]['f_tail'],
                                              note='expected limits use zero-count simulation bounds as background '
                                                   'central values: they measure the reach of this simulation '
                                                   'set-up and are conservative, not the physics reach of a real '
                                                   'search'),
                     n_points=len(h['signal']), n_points_with_limit=len(lim_pts),
                     n_points_eps0_both_bins=len(h['signal']) - len(lim_pts),
                     asym_over_toys_range=[min(ratios), max(ratios)] if ratios else None),
        n_trig=dict(value=h['n_trig']['value'], rel_stat=h['n_trig']['rel_stat'],
                    tag='VERIFIED as pipeline number; ESTIMATE as physics (generator-level Pythia + preselection '
                        'proxies; USER D1: after the event-level preselection)'),
        samples=h['samples'],
        pu_reach_per_trial_rho2=dict(value=h['pu_reach_per_trial_rho2_k20'],
                                     requirement_if_PU_takes_SRG_budget=BUDGET_C / 10 / h['n_trig']['value'],
                                     formula='~1e-6 / N_trials(rho=2), i.e. 2^-20 ~ 1e-6 (plan 4.1 step 2, l. 1110)',
                                     tag='ESTIMATE'),
        closure=h['closure'],
        ladder=lad_short(h),
        pu_end_state={k: {c: dict(B=v['B'], sigma_ln=v['sigma_ln'], closure_factor=v['closure_factor'],
                                  zero_branch=v['zero_branch'], components=v['sigma_ln_components'])
                          for c, v in h['pu_end_state'][k].items()} for k in ('end_state', 'end_state_T')},
        sm_proxy_fraction_of_B_SM=h['sm_proxy_fraction_of_B_SM'],
        cprime=h['cprime'],
        fallback_B=fbB,
        normalisation=dict(
            formula='N_exp = sigma_norm (N_IC = 2) x f_tail x L (3 ab^-1) x A_trig_presel; A_incl = A_trig_presel x '
                    'f_tail; sigma95_fb = mu95 / (L x A_incl) is a limit on the inclusive sigma(pp -> QQbar)',
            f_tail=h['tail_fraction'],
            f_tail_definition='sum w(TRGS, pT(QQbar) > 200 GeV, |eta_pair| < 4) / sigma_ref (INC sigma_matched): '
                              'the population the Stage-3 p2 template and acceptance.json A_trig_presel are '
                              'conditional on (sim/stage3/code/make_inputs.py: sample trig, ptmin 200, eta_max 4)',
            erratum='FIX R3-NORM (2026-10-16, after the results PASS): f_tail was omitted before; N_exp, S, sigma95 '
                    'were too optimistic and mu95/N_exp, mu_5sigma/N_exp too small by 1/f_tail = 5.9-21. mu95, B, eps, '
                    'limits.json and acceptance.json unchanged. Found by the P2 audit + paper review R2 A-2, '
                    'verified in acts/stage4/investigation/INV_NORM_F200.md; fix log acts/stage4/review/'
                    'FIX_RESULTS_R3_NORM.md',
            tag='VERIFIED (inputs); N_exp ESTIMATE (sigma_norm K factor and Etilde column are [U])'),
        fallback_points=pts,
        a2fc_revert=dict(meta=h['a2fc_revert_meta'], points=a2fc,
                         eps_rfb_fullchain_over_numpy={k: round(v, 3) for k, v in fcr.items()},
                         eps_rfb_ratio_range_other_8=[round(min(oth), 2), round(max(oth), 2)] if oth else None,
                         n_points_numpy_A2=sum(1 for v in h['signal'].values() if not v['replaced_by_a2fc']),
                         paired_aggregate_other_8=pag,
                         fullchain_eps_systematic=fsys,
                         investigation=dict(
                             file='acts/stage4/investigation/INV_A2FC_E500.md', status='CLOSED (2026-10-16)',
                             verdict='statistics + measurement-noise draws; no merge/bookkeeping bug; identical inputs '
                                     'and identical noise model (ACTS vs numpy smearing); deep-rung pass/fail is set by '
                                     'the noise draw, which A2FC fully re-draws, so the deep-rung paired comparison is '
                                     'effectively unpaired. Numpy A2 22/200 at R14 is high, A2FC 4/200 low, against a '
                                     'replica expectation of >~10-11/200 (eps ~ 0.05; only numpy quirk noise was '
                                     're-drawn, the ACTS quirk-noise draw was never replicated). At E500 3 keV the only '
                                     'identified full-chain-specific loss is row 268 (CKF stole 46/83 quirk hits; 1/64 '
                                     '= 1.6 % at R04; net R04 64 -> 61). At the other 8 revert points the paired R04 '
                                     'comparison shows a systematic one-sided full-chain loss (84/20 discordant, '
                                     'p ~ 1.6e-10; r_fb x 0.87): a real CKF-driven inefficiency, not noise.',
                             mcnemar_p_R10_R14=7.6e-6, global_p_after_look_elsewhere=[1e-4, 1e-3],
                             p_tag='ESTIMATE; somewhat unusual; no mechanism found; "statistics" is a conclusion by '
                                   'exclusion (fresh ACTS-seed quirk replicas not run)',
                             replica_eps_R14_E500_3keV=dict(value=0.05, k_range=[10, 11], n=200, lower_bound=True,
                                                            tag='ESTIMATE (>~; only the 34 rows passing R08 in either '
                                                                'production were re-drawn)'),
                             consequence='no fix; C12FC_v1 stands; deep-rung / fallback eps carry large statistical '
                                         'uncertainty (few passing events); the CP interval is the full statistical '
                                         'uncertainty (noise draws are part of it); in addition a full-chain '
                                         'systematic on the numpy-A2 eps (fullchain_eps_systematic)'),
                         tag='VERIFIED (signal_eff.json a2.a2fc_revert; numpy values from the same rows)'),
        srt_window_ns=h['srt_window_ns'],
        p2_detector=dict(
            edges_A1_R04={k: dict(lower=v['R04_lower'], upper=v['R04_upper'],
                                  truth_lmax_RIT=v['truth']['lower_lmax_RIT_closed'],
                                  truth_ds100=v['truth']['lower_ds100_hit'],
                                  truth_merge100_median=v['truth']['upper_merge100_hit']) for k, v in a1.items()},
            edges_A2_R04={k: dict(lower=v['R04_lower'], upper=v['R04_upper']) for k, v in a2e.items()},
            sep_IT_det_pu200=dict(measurable=h['sep_it_det']['pu200_measurable'], note=h['sep_it_det']['pu200_note'],
                                  flags=sorted({str(v.get('flag')) for v in sepA2}),
                                  median_range_mm=[min(v['sep_det_median_mm'] for v in sepA2 if v['n']),
                                                   max(v['sep_det_median_mm'] for v in sepA2 if v['n'])]),
            mass_observables=mobs,
            M_est_median_A2_GeV={s: mobs['A2']['pooled_R04'][s]['M_est_GeV']['median'] for s in SPM},
            M_est_median_A1_GeV={s: mobs['A1']['pooled_R04'][s]['M_est_GeV']['median'] for s in SPM},
            P2_verdict=dict(
                m_Q='No measurement of m_Q at PU 200; only qualitative handles ("partial"). M_est = MET cosh(eta)/'
                    '(beta gamma)_ToF is a pair-mass proxy (M_QQbar >= 2 m_Q). Pooled median 2.26 m_Q at PU 200 (850 '
                    'events with M_est defined), just above the 2 m_Q threshold (no PU: 2.46 m_Q); 0 events below '
                    '1.5 m_Q without PU; at PU 200 29 %% below 1.5 m_Q and 19 %% below 0.5 m_Q (PU-induced low cluster '
                    'from in-time BTL hits). The medians order the four E masses, but the per-event spread is huge and '
                    'the median/m ratio is species-dependent. No m_Q fit, no t_est, no sensitivity.json.'
                    .replace('%%', '%'),
                Lambda='Only through the epsilon window (lower edge 1.0-1.2 keV at PU 200; A1 upper edge 4.7-6.6 '
                       'keV) and, without PU, sep_IT^det and w_core; sep_IT^det NOT MEASURABLE at PU 200.'),
            tag='VERIFIED (detector level; A1 = no PU, A2 = PU 200 incl. the A2FC full-chain revert points)'),
        p1=p1_block(),
        statistics_reach=stats_reach(h),
        cited_investigations=cit,
        validations={'V4-1': 'PASS in 2 294 / 2 295 jobs; analysis admission 0 missing / 0 invalid / 0 not admitted; '
                             'A2FC_F1000_L3_000 V4-1 FAIL (3/145 007 PU SimHits unmeasured) admitted (D13)',
                     'V4-2': 'DONE (fix R1); rho_dens %.3f < 1.05' % h['closure']['rho_dens'],
                     'V4-3': 'PARTIAL: eps_find >= 0.9 at 1.5-2 keV (Se500 also 3 keV) with the any-candidate '
                             '>= 50 %% match (matched_any, defined post hoc in INV_SIGNAL_EFF §1); with R04 required '
                             '(matched_R04) %.2f-%.2f there; not met at 1, 3, 5 keV (understood: merging / seed '
                             'degeneracy / CKF); pre-declared comparator (d), the 12.8-25 keV hit-level merging edge, '
                             'not met (A1 upper edges 4.7-6.6 keV); W_c/t_tol attribution: no effect at 2-5 keV'
                             % v43R04,
                     'V4-4': 'PARTIAL (T_seed/regression bit-identity only)', 'V4-5': 'NOT RUN',
                     'V4-6': 'A5 at 1 keV 0.21-0.57 %; A1 > 5 % at 3-5 keV -> 9-point A2FC full-chain revert applied',
                     'V4-7': 'FAIL -> pre-registered anti-conservative end state; T3 non-informative',
                     'V4-8': 'N/A (Mac only)', 'V4-9': 'PASS (G1)', 'V4-10': 'PASS (leak 0)'},
    )
    return S


# ------------------------------------------------------------------------------------------------ tables
def e(x):
    return '–' if x is None else ('%.1e' % x)


def tables(h, hc):
    L = []
    P = L.append
    KEY = ['R04_IP2>=7', 'R05_w<37.5', 'R06_w<18.75', 'R07_w<9.4', 'R08_w<4.7', 'R09_p>1e-3', 'R11_p>0.05',
           'R14_2S2>=3', 'R20_o>5', 'R23_e>2.0']
    lad = {c: {r['rung']: r for r in h['ladder'][c]['rows']} for c in 'TG'}
    P('### ladder (SR-G PU column)')
    P('| rung | B_PU central | σ_ln(PU) [trend, density, model, closure, stat] | B₈₄ SR-T | B₈₄ SR-G | top term SR-G | decades over 0.11 (T / G) |')
    P('|---|---|---|---|---|---|---|')
    for k in KEY:
        rT, rG = lad['T'][k], lad['G'][k]
        p = rG['pu_term']; c = p['comps']
        P(f"| {k} | {e(p['value'])}{' (bound)' if p['zero_branch'] else ''} | {p['sigma_ln']:.2f} [{c['trend']:.2f}, "
          f"{c['density']:.2f}, {c['model_spread']:.2f}, {c['closure']:.2f}, {c['stat']:.2f}] | {e(rT['B84'])} | "
          f"{e(rG['B84'])} | {rG['top_term']}{' (bound)' if rG['top_term_zero_bound'] else ''} | "
          f"{rT['decades_over_0p11']:.2f} / {rG['decades_over_0p11']:.2f} |")
    P('')
    P('### class split (central, events), SR-G / SR-T')
    P('| rung | PU G | SM G | C′ G | PU T | SM T | C′ T | top 3 (G) |')
    P('|---|---|---|---|---|---|---|---|')
    for k in KEY:
        a, b = lad['G'][k]['central_by_class'], lad['T'][k]['central_by_class']
        t3 = '; '.join(f"{t['label']} {e(t['value'])}" for t in lad['G'][k]['top3'])
        P(f"| {k} | {e(a.get('PU'))} | {e(a.get('SM'))} | {e(a.get('Cprime'))} | {e(b.get('PU'))} | {e(b.get('SM'))} | "
          f"{e(b.get('Cprime'))} | {t3} |")
    P('')
    P('### FB')
    P('| selection | B₈₄ SR-T | B₈₄ SR-G | median SR-G | top SR-G | top SR-T |')
    P('|---|---|---|---|---|---|')
    for k, v in h['fallback_B'].items():
        P(f"| {k.replace('&h>5&o>5', '')} | {e(v['T']['B84'])} | {e(v['G']['B84'])} | {e(v['G']['B_median'])} | "
          f"{v['G']['top_term']} | {v['T']['top_term']} |")
    P('')
    P('### signal / fallback')
    P('N_exp = σ_norm · f · 3 ab⁻¹ · A (f = P(pT(QQ̄) > 200 GeV, |η| < 4); FIX R3-NORM: f was omitted before)')
    P('')
    P('| point | r_fb | ε(r_fb) [68 % CP] | ε_SR-T | A | f | N_exp | S | B₈₄ T / G | μ₉₅ toys [±1σ] | asym/toys | μ₉₅/N_exp | FC |')
    P('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for k, v in h['signal'].items():
        l = v['limit']; b1 = l['mu95_toys_band1s']; fbB = h['fallback_B'][v['r_fb']]
        lim = (f"{e(l['mu95_toys'])} [{e(b1[0])}, {e(b1[1])}] | {l['asym_over_toys']:.2f} | {l['mu95_over_nexp']:.3g}"
               if l['mu95_toys'] else 'no limit (ε = 0 in both bins) | – | –')
        P(f"| {v['spin']}{v['m']} {v['lam']:g} | {v['r_fb'].replace('&h>5&o>5', '')} | {v['eps_A2_rfb']:.3f} "
          f"[{v['eps_A2_rfb_cp68'][0]:.3f}, {v['eps_A2_rfb_cp68'][1]:.3f}] | {v['eps_A2_SRT_rfb']:.3f} | "
          f"{v['A_trig_presel']:.2f} | {v['f_tail']:.4f} | {l['n_exp_signal']:.3g} | {l['S_at_rfb']:.3g} | {e(fbB['T']['B84'])} / "
          f"{e(fbB['G']['B84'])} | {lim} | {'FC' if v['replaced_by_a2fc'] else ''} |")
    P('')
    P('### eps at reporting rungs')
    P('| point | R_A | R_B | R_C | R_D | R_E | A5 R_A / R_B / R_C | FC |')
    P('|---|---|---|---|---|---|---|---|')
    for k, v in h['signal'].items():
        ee, a5 = v['eps_A2'], v['eps_A5']
        P(f"| {v['spin']}{v['m']} {v['lam']:g} | " + ' | '.join(f"{ee[r]:.3f}" for r in REPORT)
          + ' | ' + (f"{a5['R_A']:.3f} / {a5['R_B']:.3f} / {a5['R_C']:.3f}" if a5 else '–')
          + f" | {'FC' if v['replaced_by_a2fc'] else ''} |")
    P('')
    P('### A2FC revert')
    P('| point | n | R04 numpy → FC | R14 numpy → FC | r_fb | ε(r_fb) numpy → FC | μ₉₅ numpy → FC |')
    P('|---|---|---|---|---|---|---|')
    for k, v in h['a2fc_revert'].items():
        s = h['signal'][k]
        c = hc['signal'][k] if hc else None
        P(f"| {s['spin']}{s['m']} {s['lam']:g} | {v['n_den']} | {v['eps_R04_a2_numpy']:.3f} → {v['eps_R04_a2fc']:.3f} | "
          f"{v['eps_R14_a2_numpy']:.3f} → {v['eps_R14_a2fc']:.3f} | {s['r_fb'].replace('&h>5&o>5', '')} | "
          + (f"{c['eps_A2_rfb']:.3f} → {s['eps_A2_rfb']:.3f} | {e(c['limit']['mu95_toys'])} → "
             f"{e(s['limit']['mu95_toys'])} |" if c else '– | – |'))
    mo = mass_observables(TT / h['source_dir'], h['signal'])
    P('')
    P('### m_Q handles (BM, matched, first candidate per row, pooled over Λ; median [q16, q84])')
    P('| species-mass | sample / selection | n | M_est (GeV) | finite | β_ToF | dE/dx (MIP) |')
    P('|---|---|---|---|---|---|---|')
    for s_ in SPM:
        for kd, sel in (('A1', 'pooled_R04'), ('A2', 'pooled_R04'), ('A2', 'pooled_rfb')):
            x = mo[kd][sel][s_]
            if not x['n']:
                P(f"| {s_} | {kd} {sel[7:]} | 0 | – | – | – | – |")
                continue
            M, b, d_ = x['M_est_GeV'], x['beta_tof'], x['dedx_MIP']
            P(f"| {s_} | {kd} {sel[7:]} | {x['n']} | {M['median']:.0f} [{M['q16']:.0f}, {M['q84']:.0f}] | "
              f"{x['M_est_finite_fraction']:.2f} | {b['median']:.2f} [{b['q16']:.2f}, {b['q84']:.2f}] | "
              f"{d_['median']:.2f} [{d_['q16']:.2f}, {d_['q84']:.2f}] |")
    P('')
    P('### w_core median at R04 (mm), A1 / A2, per point')
    P('| point | A1 (n) | A2 (n) |')
    P('|---|---|---|')
    for k_ in sorted(mo['A2']['w_core_median_R04_by_point'], key=lambda z: (SPM.index(z.split('|')[0]), float(z.split('|')[1]))):
        a_, b_ = mo['A1']['w_core_median_R04_by_point'].get(k_), mo['A2']['w_core_median_R04_by_point'][k_]
        f_ = lambda z: '–' if not z or z['median_mm'] is None else f"{z['median_mm']:.1f} ({z['n']})"  # noqa: E731
        P(f"| {k_} | {f_(a_)} | {f_(b_)} |")
    if hc:
        P('')
        P(f"### {hc['source_dir'].split('/')[-1]} -> {h['source_dir'].split('/')[-1]}")
        P('| quantity | old | new |')
        P('|---|---|---|')
        for c in 'TG':
            P(f"| min B₈₄ SR-{c} (rung) | {e(hc['ladder'][c]['min_B84'])} ({hc['ladder'][c]['min_B84_rung']}) | "
              f"{e(h['ladder'][c]['min_B84'])} ({h['ladder'][c]['min_B84_rung']}) |")
        for k in ('FB0&h>5&o>5', 'FB1&h>5&o>5', 'FB2&h>5&o>5', 'FB3&h>5&o>5', 'FB4&h>5&o>5', 'FB4e>1.3&h>5&o>5',
                  'FB4e>1.6&h>5&o>5'):
            a, b = hc['fallback_B'][k], h['fallback_B'][k]
            P(f"| B₈₄ T / G {k.replace('&h>5&o>5', '')} | {e(a['T']['B84'])} / {e(a['G']['B84'])} | "
              f"{e(b['T']['B84'])} / {e(b['G']['B84'])} |")
        b0, b1_ = best_limit(hc), best_limit(h)
        P(f"| best μ₉₅/N_exp (point) | {b0[0]:.1f} ({b0[1]}) | {b1_[0]:.1f} ({b1_[1]}) |")
    return '\n'.join(L) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', default='C12FC_v1')
    ap.add_argument('--compare', default='C12_v1')
    ap.add_argument('--out', default=str(ANA / 'STAGE4_SUMMARY.json'))
    a = ap.parse_args()
    h = headline(ANA / a.run)
    hc = headline(ANA / a.compare) if a.compare else None
    assert h['provenance'].get('dev') is False and h['provenance'].get('freeze_match') is True, 'primary run not frozen non-DEV'
    S = build(h, hc, cited(), cpu_hours(), a.run, a.compare)
    Path(a.out).write_text(json.dumps(S, indent=1, default=float))
    here = Path(__file__).resolve().parent
    (here / f'headline_{a.run}.json').write_text(json.dumps(h, indent=1, default=float))
    (here / f'tables_{a.run}.md').write_text(tables(h, hc))
    print('written', a.out, here / f'headline_{a.run}.json', here / f'tables_{a.run}.md')


if __name__ == '__main__':
    main()
