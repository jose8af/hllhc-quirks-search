"""selftest.py -- unit / self-checks of the REVIEW_ANALYSIS_R1 fixes (read-only on prod; < 1 min, nice 15).

    nice -n 15 pixi run python -m acts.stage4.analysis.selftest
"""
import json
import sys

import numpy as np

from acts.stage4.analysis import common as C
from acts.stage4.analysis import background as BG
from acts.stage4.analysis import wp as WP
from acts.stage4.analysis import stats as ST
from acts.stage4.analysis import srt as SR


def es(P, zb, reach=False):
    return dict(P_per_trial=P, zero_branch=zb, reachable_rho2=reach, trend_factor=1.0,
                sigma_ln_components=dict(stat=0.1, density=1.0))


# ================================================================================================ FIX R6 tests
def _cands(n, dedx, trial=None):
    """Synthetic C' candidate arrays (cp.cand.* layout) passing every in-job rung; dE/dx given."""
    return {'cp.cand.attributed': np.ones(n, bool), 'cp.cand.trial': np.arange(n) if trial is None else trial,
            'cp.cand.rungs': np.packbits(np.ones((n, 48), bool), axis=1), 'cp.cand.f_ckf': np.zeros(n),
            'cp.cand.p_chi2core': np.full(n, 0.5), 'cp.cand.dw_core': np.full(n, 1.0), 'cp.cand.nit2': np.full(n, 4),
            'cp.cand.nip2': np.full(n, 8), 'cp.cand.n2s2': np.full(n, 3), 'cp.cand.dphi_met': np.zeros(n),
            'cp.cand.eta_axis': np.zeros(n), 'cp.cand.dedx': np.asarray(dedx, float)}


def _nested_rec(n_start, n_r09, n_r10, n_r11, start_col):
    """Records passing the start rung; p cuts nested R09 > R10 > R11 (n_r09 >= n_r10 >= n_r11); all else passes."""
    F = np.zeros((n_start, C.NR), bool); F[:, :start_col + 1] = True
    REQ = np.ones((n_start, 17), bool)
    REQ[:, 8] = np.arange(n_start) < n_r09; REQ[:, 9] = np.arange(n_start) < n_r10; REQ[:, 10] = np.arange(n_start) < n_r11
    return BG.SimpleRecords(F, REQ, np.arange(n_start))


def r6_tests(R, tmp):
    from acts.stage4.analysis import signal as SG, products as PD, hitrec as HR
    from acts.stage4.analysis import run_all as RA
    # 1. asymptotic NLL with the saturated offset: asymptotic/toys at the C12_v1 FB0 / FB1 inputs (frozen: 2.7e-4)
    rr = []
    for s_, b_, sg_ in (([0.0, 0.01], [75197332.82, 87531796.16], [0.83363, 1.12452]),          # E200 0.45 keV FB0
                        ([0.015, 0.015], [57448802.18, 64639003.91], [0.87915, 1.07668])):      # E1500 1.5 keV FB1
        rr.append(ST.expected_limit_asymptotic(s_, b_, [{}, {}], sg_)['median'] /
                  ST.expected_limit_toys(s_, b_, [{}, {}], sg_)['median'])
    R['R6_1_asym_over_toys_FB0_FB1'] = [round(x, 3) for x in rr]
    R['R6_1_asym_converges_FB0_FB1'] = bool(all(0.75 <= x <= 1.1 for x in rr))
    # 2. A28 merge population never contains an added cut of the merged variable
    #    (a) C12 SR-T FB2: start R06 (& BTL), p(R09 | R06) = 16/1874, R10 < 10 -> merged R11 tail on R06, not R06 & R09
    rec = _nested_rec(1874, 16, 5, 0, 5)
    fs = BG.chain_factors(rec, 5, C.COL['FB2'], np.ones(1874, bool), None)
    pf = [f for f in fs if f['var'] == 'p']
    R['R6_2_srt_fb2_merge_on_R06'] = bool(len(pf) == 1 and pf[0]['M'] == 1874 and pf[0]['N'] == 0 and
                                          'merged' in pf[0]['label'] and '| R06' in pf[0]['label'] and
                                          'R09' not in pf[0]['label'].split('|')[1])
    #    (b) SM rows: Z(nunu) FB0 0/29 -> 0/M_start, W(tau_h)/tt 1l FB0 1/30 -> 1/M_start, FB1 0/10 -> 0/M_start
    ok = []
    for name, col, sc, n09, n10, n11 in (('Znunu FB0', 'FB0', 3, 29, 5, 0), ('Wtau_h FB0', 'FB0', 3, 30, 5, 1),
                                          ('tt1l FB0', 'FB0', 3, 57, 6, 1), ('Znunu FB1', 'FB1', 4, 10, 3, 0)):
        rec = _nested_rec(3000, n09, n10, n11, sc)
        T = BG.Term(name)
        deep = BG.depth_term(T, rec, None, 6000, C.COL[col], None)
        ev = T.evaluate()
        want = 0.5 * (n11 / 3000 if n11 else 1.14 / 3000)
        ok.append(deep == sc and abs(ev['value'] / want - 1) < 1e-12)
    R['R6_2_sm_fb0_fb1_merge_on_start'] = bool(all(ok))
    # 3. looper 'low gun counts' (WP_RULE §7): 0 R01 passes in 500 C'_PU events -> depth from C'0 (1.14/1e5, not /500)
    js0 = [dict(job=dict(topo='looper'), meta=dict(v410=dict(n_events=100000, n_pre=395)), d_cp={}, tr={'ev': []})]
    jsp = [dict(job=dict(topo='looper'), meta={}, d_cp={}, tr={'ev': np.arange(500)})]
    cp = BG.cprime_term(js0, jsp, {}, log=lambda *a: None, nboot=20)['looper']
    r8 = cp['rows'][7]
    R['R6_3_looper_low_gun_from_C0'] = bool(cp['low_gun_count']['applied'] and
                                            abs(r8['P_given_t'] - 1.14 / 1e5) < 1e-15 and
                                            r8['factors'][0]['label'].startswith("C'0 attributed"))
    # 4. D11: C' dE/dx in both readings, the larger P used; h/o: C'0 factor 1 vs B1-PU, the larger B used
    js0 = [dict(job=dict(topo='v0'), meta=dict(v410=dict(n_events=100000, n_pre=0)),
                d_cp=_cands(12, np.full(12, 2.5)), tr={'ev': []})]
    jsp = [dict(job=dict(topo='v0'), meta={}, d_cp=_cands(100, np.r_[np.full(30, 2.5), np.full(70, 1.0)]),
                tr={'ev': np.arange(500)})]
    cp = BG.cprime_term(js0, jsp, {}, log=lambda *a: None, nboot=20)['v0']
    r14, re13 = cp['rows'][13], cp['rows'][14]
    dr = re13.get('dedx_readings', {})
    R['R6_4_dedx_both_readings_larger_used'] = bool(
        dr and abs(dr["C'_PU chain"]['P'] - 0.2 * 0.3) < 1e-12 and abs(dr["C'0 factor"]['P'] - 0.2) < 1e-12 and
        dr['used'] == "C'0 factor" and abs(re13['P_given_t'] - r14['P_given_t']) < 1e-15)
    cpd = {'v0': dict(rows=[dict(P_given_t=1e-3, s_ln=0.1, zero_branch=False)] * 37, rate=dict(value=0.1))}
    t = WP.cp_terms(cpd, 13, 1e8, 0.26, dict(N=3, M=30, s_ln=0.5, population='R14'))[0]
    R['R6_4_ho_c0_factor1_larger_used'] = bool(abs(t['value'] - 1e8 * 0.1 * 1e-3) < 1e-9 and
                                               t['ho_reading'] == "C'0 (factor 1)")
    # 5. sep_IT^det from core hits only; PU-200 values flagged not measurable
    g = dict(LC=np.zeros(8, int), wv=np.array([1.0, 1.0, -1.0, -1.0, 40.0, 45.0, -40.0, -50.0]))
    cm = np.r_[np.ones(4, bool), np.zeros(4, bool)]
    R['R6_5_sepit_core_only'] = bool(HR.sep_it(g, 0.0, cm) == 2.0 and HR.sep_it(g, 0.0) > 20)
    z = dict(key=np.array(['A2|F|500|3|BM', 'A1|F|500|3|BM']), L=np.ones((2, 23), bool),
             sep_it_det_mm=np.array([13.4, 3.0]))
    sp = PD.sep_it_det({'a2': z})['points']
    R['R6_5_sepit_pu200_flagged'] = bool(sp['A2|F|500|3|BM']['measurable'] is False and
                                         'NOT MEASURABLE' in sp['A2|F|500|3|BM']['flag'] and
                                         sp['A1|F|500|3|BM']['measurable'] is True and
                                         sp['A2|F|500|3|BM']['sep_det_median_mm'] == 13.4)
    # 6. V4-6 revert: A2 entries replaced by A2FC (same rows), refused when a revert point lacks A2FC (unless dev)
    def ent(sample, rows, k):
        L = np.zeros((len(rows), 23), bool); L[:k, :] = True
        return dict(sample=sample, spin='F', m=500.0, lam=3.0, cfg='BM', rows=list(rows), L=L, probe_excluded=0,
                    status_ne1=0)
    acc = {'A2|F|500|3|BM': ent('A2', range(10), 9), 'A2|F|500|5|BM': ent('A2', range(10), 8)}
    fc = {'A2FC|F|500|3|BM': ent('A2FC', range(10), 7)}
    rv = [('F', 500.0, 3.0)]
    pr = SG.apply_a2fc(acc, fc, rv, dev=False, log=lambda *a: None)
    R['R6_6_a2fc_replaces'] = bool(acc['A2|F|500|3|BM']['L'][:, 3].sum() == 7 and acc['A2|F|500|3|BM']['sample'] == 'A2'
                                   and pr['points']['A2|F|500|3|BM']['eps_R04_a2_numpy'] == 0.9 and
                                   acc['A2|F|500|5|BM']['L'][:, 3].sum() == 8)
    acc2 = {'A2|F|500|3|BM': ent('A2', range(10), 9), 'A2|F|500|5|BM': ent('A2', range(10), 8)}
    def refused_(fn):
        try:
            fn(); return False
        except SystemExit as e:
            return 'REFUSED' in str(e)
    R['R6_6_a2fc_missing_refused'] = refused_(lambda: SG.apply_a2fc(acc2, fc, rv + [('F', 500.0, 5.0)], dev=False,
                                                                    log=lambda *a: None))
    fc_part = {'A2FC|F|500|3|BM': ent('A2FC', range(5), 4)}
    R['R6_6_a2fc_partial_rows_refused'] = refused_(lambda: SG.apply_a2fc(dict(acc2), fc_part, rv, dev=False,
                                                                         log=lambda *a: None))
    pr = SG.apply_a2fc(acc2, fc, rv + [('F', 500.0, 5.0)], dev=True, log=lambda *a: None)
    R['R6_6_a2fc_dev_records_missing'] = bool(len(pr['missing']) == 1 and acc2['A2|F|500|5|BM']['L'][:, 3].sum() == 8)
    R['R6_6_revert_set_loaded'] = len(SG.a2fc_revert_set())
    R['R6_6_campaign_A2FC'] = bool(RA.CAMPAIGN_MAP.get('A2FC') == ('A2FC', ('a5',)))
    if '--no-e2e' not in sys.argv:
        # run_all on real files: a frozen non-dev signal stage without A2FC is REFUSED; with --dev and A2FC the
        # available revert points are replaced and A2FC never enters the A5 sample
        try:
            RA.main(['--campaigns', 'C1a', '--stages', 'signal', '--max-jobs', '2', '--out', str(tmp / 'r6a')])
            R['R6_6_run_all_without_A2FC_refused'] = False
        except SystemExit as e:              # must be the V4-6 refusal (not the freeze refusal)
            R['R6_6_run_all_without_A2FC_refused'] = 'REFUSED (V4-6' in str(e)
            R['R6_6_refusal_msg'] = str(e)[:100]
        try:
            RA.main(['--campaigns', 'C1a,A2FC', '--stages', 'signal', '--dev', '--max-jobs', '2',
                     '--out', str(tmp / 'r6b')])
            sg = json.loads((tmp / 'r6b' / 'signal_eff.json').read_text())
            rv_ = sg['a2']['a2fc_revert']
            R['R6_6_run_all_a2fc_replaced'] = sorted(rv_['points'])
            R['R6_6_run_all_a2fc_ok'] = bool('A2|F|200|3|BM' in rv_['points'] and
                                             not any(k.startswith('A2FC') for k in sg.get('a5', {}).get('points', {}))
                                             and sg['a2']['points']['A2|F|200|3|BM'].get('replaced_by_a2fc'))
        except BaseException as e:                                     # noqa: BLE001
            R['R6_6_run_all_a2fc_ok'] = False; R['R6_6_run_all_error'] = repr(e)[:300]


def main():
    R = {}
    # A-1: P_T > P_all beyond reach -> the no-BTL summand uses the full column (> 0)
    t = WP.srt_pu_term(es(2e-6, True), es(3e-7, True), None,
                       dict(P_late=dict(N=0, M=254), P_oot=dict(N=4.0, M=1000), sigma_ln_PV=0.3), 1.0, 'x')
    R['A1_not_present_positive'] = bool(t[1]['value'] > 0 and abs(t[1]['value'] - 3e-7 * 4 / 1000) < 1e-15)
    # A-2: base holds its bound + timing 0/254 -> still exactly one bound (the timing zero enters as 1)
    R['A2_one_bound_srt'] = bool(t[0]['n_bounds'] <= 1 and abs(t[0]['value'] - 2e-6) < 1e-18)
    p = WP.pu_term(es(1e-6, True), dict(N=0, M=500, s_ln=None, population='R14', c=1.0), 1.0, 'y')
    R['A2_one_bound_pu'] = bool(abs(p['value'] - 1e-6) < 1e-18)
    v, s, zb = WP._f1_on_row(5.0, 0.3, True, dict(N=0, M=100, s_ln=None))
    R['A2_one_bound_sm_cp'] = bool(v == 5.0)
    v2, s2, zb2 = WP._f1_on_row(5.0, 0.3, False, dict(N=0, M=100, s_ln=None))
    R['A2_bound_when_none'] = bool(abs(v2 - 5.0 * 1.14 / 100) < 1e-12 and zb2)
    # A-3: SM/C' depth starts at the deepest ladder rung CONTAINED in the column (FB0 -> R04, not R14)
    n = 400
    rng = np.random.default_rng(1)
    F = np.zeros((n, C.NR), bool); F[:, :4] = True; F[:200, 4:14] = True
    REQ = np.ones((n, 17), bool); REQ[200:, 4:8] = False
    rec = BG.SimpleRecords(F, REQ, np.arange(n))
    T = BG.Term('t')
    deep_fb0 = BG.depth_term(T, rec, None, n, C.COL['FB0'], None)
    T2 = BG.Term('t2')
    deep_r14 = BG.depth_term(T2, rec, None, n, 13, None)
    R['A3_fb0_starts_at_R04'] = bool(deep_fb0 == 3 and deep_r14 == 13)
    R['A3_fb0_differs_from_R14'] = bool(abs(T.evaluate()['value'] - T2.evaluate()['value']) > 1e-9)
    # A-4: OOT lookups use the job-relative S5 event index and find in-band hits (G3B1 as the stand-in file set)
    evx = SR.c1_b1_event_index(C.manifest('G3'), sample='G3B1')
    jid, path, ev0, e = evx[300]
    with np.load(path, allow_pickle=False) as z:
        c = {k: z['cand.' + k] for k in ('normal', 'axis', 'trial', 'tag')}
        pv = z['trials.pv']; trev = z['trials.ev']
    i = int(np.where((c['tag'] & 1) > 0)[0][0])
    obs = [dict(row=r, spin='F', m=1000.0, pv=pv[c['trial'][i]], normal=c['normal'][i].astype(float),
                axis=c['axis'][i].astype(float), t_pv=0.0, t_raw_in=np.inf, dt_earliest=np.nan) for r in range(20)]
    tags, chk = SR.signal_srt(obs, evx, 6.07, 24.025)
    R['A4_oot_hits_found'] = bool(chk['pass_'] and chk['n_oot_inband_hits'] > 0 and chk['n_lookups_missing_file'] < chk['n_lookups'])
    R['A4_check'] = chk
    R['A4_relative_index'] = bool(ev0 == int(trev.min()) and evx[0][3] == 0)
    # B-2: missing lever arm never lowers B
    f, s, why = BG.family_correction(dict(ratio=0.58), 'anti-conservative (missing lever arm)')
    R['B2_missing_lever_arm'] = bool(f == 1.0 and abs(s - abs(np.log(0.58))) < 1e-12)
    # B-1: T3 correction function
    R['B1_T3_degenerate_flagged'] = BG.t3_correction(dict(informative=False, z=0.0))[0] == 1.0
    R['B1_T3_anti'] = bool(abs(BG.t3_correction(dict(z=3.0, ln_r=0.5))[0] - np.exp(0.5)) < 1e-12)
    # D4 / C-4: toys deterministic, 3.0 events at b -> 0 (5000 toys: MC precision ~2 %, tolerance 5 %)
    a = ST.expected_limit_toys([1.0], [1e-4], [{}], [0.5]); b = ST.expected_limit_toys([1.0], [1e-4], [{}], [0.5])
    R['D4_toys_b0_3events'] = bool(abs(a['median'] - 3.0) < 0.15 and a['median'] == b['median'])
    # D8: credited h/o factor is detected
    R['D8_guard'] = bool(WP.f1_credited(dict(N=9, M=10)) and not WP.f1_credited(dict(N=10, M=10)))
    # C-2: admission of a C1 A2 job (if present) with the frozen_inputs comparison
    js = [x for x in C.job_files(['C1'], kinds=('a2',)) if x[1] is not None][:1]
    if js:
        m = C.load_npz(js[0][1], keys=('job_id',))['meta']
        R['C2_admission_C1_A2'] = C.admission(m, 'a2', 4)['ok']
    # R2 / D2: gun pT regeneration replays s4cp's RNG exactly (stored phi_MET of C'0 events reproduced)
    bad = 0; n = 0
    for topo in ('gamma', 'v0', 'looper', 'ni30', 'dif'):
        p = C.PROD / 'C1' / 'Cp0' / f'Cp0_{topo}_000.npz'
        if not p.exists():
            continue
        d = C.load_npz(p, keys=('cp.ev',))
        seeds = d['meta']['chain_meta']['event_seeds']
        for row in d['cp.ev'][:200]:
            pt, ph = BG.gun_pt(topo, seeds[int(row[0]) - int(d['meta']['job']['ev0'])])
            n += 1; bad += int(abs(((ph - row[10]) + np.pi) % (2 * np.pi) - np.pi) > 1e-9)
            lo, hi = BG.GUN_RANGE[topo][1:]
            bad += int(not (lo <= pt <= hi))
    R['R2_gun_rng_replay'] = bool(n > 0 and bad == 0)
    R['R2_gun_rng_replay_n'] = n
    # R2 / D2: P_PV-line 0.22 on the NI terms only
    cp = {'ni30': dict(rows=[dict(P_given_t=1e-3, s_ln=0.1, zero_branch=False)] * 37, rate=dict(value=0.1)),
          'dif': dict(rows=[dict(P_given_t=1e-3, s_ln=0.1, zero_branch=False)] * 37, rate=dict(value=0.1))}
    t = {x['label']: x['value'] for x in WP.cp_terms(cp, 13, 1e8, 0.26, None)}
    R['R2_ni_pv_line'] = bool(abs(t["C' ni30"] - 1e8 * 0.1 * 0.22 * 1e-3) < 1e-6 and abs(t["C' dif"] - 1e4) < 1e-6)
    # REVIEW R2 B-2: refusal / DEV-propagation paths
    import tempfile, shutil
    from pathlib import Path
    from acts.stage4.analysis import run_all as RA
    tmp = Path(tempfile.mkdtemp())
    alt = tmp / 'norm_alt.json'; shutil.copy(C.HERE / 'inputs' / 'normalisation.json', alt)
    def refused(fn):
        try:
            fn(); return False
        except SystemExit as e:
            return 'REFUSED' in str(e)
    R['B2_inputs_refused'] = refused(lambda: RA.main(['--campaigns', 'G3', '--dry-run-g3', '--stages', 'none',
                                                       '--inputs', str(alt), '--out', str(tmp / 'o1')]))
    try:
        RA.main(['--campaigns', 'G3', '--dry-run-g3', '--dev', '--stages', 'none', '--inputs', str(alt),
                 '--out', str(tmp / 'o2')])
        m = json.loads((tmp / 'o2' / 'manifest.json').read_text())
        R['B2_inputs_dev_stamped'] = bool(m['dev'] and m['label'].startswith('DEV') and not m['freeze']['match'])
    except SystemExit:
        R['B2_inputs_dev_stamped'] = False
    dryb = C.DATA / 'analysis' / 'dryrun_g3_tseed6'
    if (dryb / 'bsum_wp.json').exists():
        sig = tmp / 'sig'; bkg = tmp / 'bkg'; sig.mkdir(); bkg.mkdir()
        pts = {'A2|F|1000|1|BM': dict(sample='A2', spin='F', m=1000.0, lam=1.0, cfg='BM', n_den=10,
                                      ladder={nm: dict(k=1, eps=0.1) for nm in C.LADDER_NAMES},
                                      fallback={f + '&h>5&o>5': dict(k=1, eps=0.1) for f in C.RUNGS[17:37]})}
        (sig / 'signal_eff.json').write_text(json.dumps(dict(label='SYNTHETIC', a2=dict(points=pts))))
        shutil.copy(dryb / 'bsum_wp.json', bkg / 'bsum_wp.json')
        (bkg / 'manifest.json').write_text(json.dumps(dict(t_seed=6, label='bkg', dev=False, freeze=dict(match=True))))
        (sig / 'manifest.json').write_text(json.dumps(dict(t_seed=6, label='sig', dev=True, freeze=dict(match=True))))
        log = lambda *a: None                                                         # noqa: E731
        R['B2_limits_refuse_dev_upstream'] = refused(lambda: RA.limits_stage(sig, bkg, tmp, log, dev=True and False))
        (sig / 'manifest.json').write_text(json.dumps(dict(t_seed=6, label='sig', dev=False, freeze=dict(match=False))))
        R['B2_limits_refuse_unfrozen_upstream'] = refused(lambda: RA.limits_stage(sig, bkg, tmp, log, dev=False))
        try:
            res = RA.limits_stage(sig, bkg, tmp, log, dev=True)
            R['B2_limits_dev_propagated'] = bool(res['dev'] and res['label'].startswith('DEV'))
        except SystemExit:
            R['B2_limits_dev_propagated'] = False
    # REVIEW R3 B-1: the reviewer's exact reproduction (scratchpad r3/b2_probe2.py): stale DEV outputs in the SAME
    # output directory must not be certified by the frozen run's own manifest
    if (dryb / 'bsum_wp.json').exists():
        o = tmp / 'o5'; o.mkdir()
        (o / 'manifest.json').write_text(json.dumps(dict(t_seed=4, label='DEV (not frozen / not a result) | earlier',
                                                          dev=True, freeze=dict(match=False))))
        (o / 'signal_eff.json').write_text(json.dumps(dict(label='DEV (not frozen / not a result) | earlier',
                                                            a2=dict(points=pts))))
        b = json.loads((dryb / 'bsum_wp.json').read_text())
        (o / 'bsum_wp.json').write_text(json.dumps(b))
        run = lambda extra=(): RA.main(['--campaigns', 'C1', '--stages', 'limits', '--out', str(o)] + list(extra))  # noqa
        R['R3B1_repro_refused'] = refused(run)
        b['rule']['complete_inputs'] = True
        (o / 'bsum_wp.json').write_text(json.dumps(b))
        (o / 'manifest.json').write_text(json.dumps(dict(t_seed=4, label='DEV | earlier', dev=True,
                                                          freeze=dict(match=False))))
        R['R3B1_repro_complete_refused'] = refused(run) and not (o / 'limits.json').exists()
        try:
            run(['--dev'])
            R['R3B1_repro_dev_stamped'] = bool(json.loads((o / 'limits.json').read_text())['dev'])
        except SystemExit:
            R['R3B1_repro_dev_stamped'] = False
        # positive path: inputs stamped by the frozen code give a NON-DEV limit
        o2 = tmp / 'o6'; o2.mkdir()
        st = C.provenance(False, True, t_seed=4, campaigns=['C1'])
        (o2 / 'signal_eff.json').write_text(json.dumps(dict(label='stamped', provenance=st, a2=dict(points=pts))))
        (o2 / 'bsum_wp.json').write_text(json.dumps(dict(b, provenance=st)))
        try:
            RA.main(['--campaigns', 'C1', '--stages', 'limits', '--out', str(o2)])
            R['R3B1_stamped_frozen_nondev'] = not json.loads((o2 / 'limits.json').read_text())['dev']
        except SystemExit as e:
            R['R3B1_stamped_frozen_nondev'] = False; R['R3B1_stamped_msg'] = str(e)[:120]
        # products in the same directory: a stale signal_eff.json without a stamp must be refused without --dev
        R['R3B1_products_refused'] = refused(lambda: RA.main(['--campaigns', 'C1a', '--stages', 'products',
                                                              '--out', str(o)]))
    # REVIEW R4 B-1 item 2: the WHOLE default stage list end to end (signal -> background -> srt -> wp -> products ->
    # limits), non-refusal --dev path, small input (2 jobs per kind)
    if '--no-e2e' not in sys.argv:
        oe = tmp / 'e2e'
        try:
            RA.main(['--campaigns', 'C1a,C1b', '--dev', '--max-jobs', '2', '--nboot', '50', '--f1-max', '200',
                     '--out', str(oe)])
            outs = sorted(p_.name for p_ in oe.iterdir())
            need = ['signal_eff.json', 'background.json', 'srt.json', 'bsum_wp.json', 'acceptance.json', 'edges_det.json',
                    'sep_it_det.json', 'limits.json']
            R['R4B1_e2e_default_stages'] = all(x in outs for x in need)
            R['R4B1_e2e_limits_dev'] = bool(json.loads((oe / 'limits.json').read_text())['dev'])
            R['R4B1_e2e_missing'] = [x for x in need if x not in outs]
        except BaseException as e:                                     # noqa: BLE001
            R['R4B1_e2e_default_stages'] = False; R['R4B1_e2e_error'] = repr(e)[:300]
    r6_tests(R, tmp)                                                     # FIX R6
    shutil.rmtree(tmp, ignore_errors=True)
    R['freeze'] = C.freeze_status()['match']
    ok = all(v for k, v in R.items() if isinstance(v, bool) and k != 'freeze')
    print(json.dumps(R, indent=1, default=str))
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
