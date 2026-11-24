"""p3c_dp2.py -- decision-point-2 numbers of work package p3-c from the yield records (p3c_apply), the pilot
weights (p3c_pilot_weights) and the frozen planning tables (phase2 p2c_rule1 -> strategy_budget copy).

  <python> p3c_dp2.py <out_dir> <apply json,...> <pilot weight npz dir or ''>

Writes <out_dir>/p3c_results.json (schema: outputs/p3c/SCHEMA.md).  Conventions fixed in the session log §P6
before any yield existed.
"""
import json
import logging
import math
import sys
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3c_dp2')
HERE = Path(__file__).resolve().parent
P2SRC = HERE.parents[2] / 'phase2_exploration' / 'src'
sys.path.insert(0, str(P2SRC))
import p2c_rule1 as R  # noqa: E402  (frozen N_trig table, allocate(), U68)

LUMI_PB = 3.0e6                      # 3 ab^-1 (STR §0)
K_V = 1.4                            # v1 K-factor of V+jets (normalise.py K_V; R-5 open: UNVERIFIED v1 value)
KFAC = dict(znn=K_V, ztt=K_V, zll=K_V, mjw=1.0, mjs=1.0)
ONE_AT_A_TIME = ['core_up', 'core_dn', 'jes_up', 'jes_dn', 'soft_up', 'soft_dn', 'tail_up', 'tail_dn', 'soft_mix',
                 'lost_e_kept']
# ADD §4.4 "as timed" unit costs (generation, chain) [s] and full-weight fractions, as p2z_addendum1.OVERRIDES
COST = dict(Z=(0.042, 0.085), W=(0.086, 0.085), tt=(0.460, 0.111))
M_FULL = {'Z': 0.4396, 'W': 0.2657, 'tt': 0.1205}


def kind(p):
    return 'Z' if p.startswith('Z') else ('tt' if p.startswith(('tt', 'tW', 't-')) else 'W')


def pool(records):
    """Pooled per-process sums.  Sliced multijets: each slice pooled, then summed."""
    g = {}
    for r in records:
        g.setdefault(r['process'], []).append(r)
    out = {}
    for p, rs in g.items():
        n = sum(r['n'] for r in rs); sw = sum(r['sum_w'] for r in rs)
        sig = sum(r['sigma_gen_mb'] * r['n'] for r in rs) / n * 1e9                       # pb
        sig_rel = math.sqrt(sum((r['sigma_err_mb'] * r['n']) ** 2 for r in rs)) / sum(r['sigma_gen_mb'] * r['n'] for r in rs)

        def q(get):
            s1 = sum(get(r)['S1'] for r in rs); s2 = sum(get(r)['S2'] for r in rs)
            return dict(sigma_pb=sig * s1 / sw, f_presel=s1 / sw, n_eff=(s1 ** 2 / s2) if s2 > 0 else 0.0)
        d = dict(n_generated=n, n_files=len(rs), sigma_gen_pb=sig, sigma_gen_rel_err=sig_rel,
                 var={v: q(lambda r, v=v: r['var'][v]) for v in rs[0]['var']},
                 trig={k: q(lambda r, k=k: r['trig'][k]) for k in rs[0]['trig']},
                 met_cut={k: q(lambda r, k=k: r['met_cut'][k]) for k in rs[0]['met_cut']},
                 v1_like=q(lambda r: r['v1_like']),
                 max_event_share=max(r['var']['nominal']['max_share'] or 0 for r in rs) / len(rs),
                 n_pos=sum(r['var']['nominal']['n_pos'] for r in rs),
                 cutflow=dict(steps=rs[0]['cutflow_nominal_notrig']['steps'],
                              sigma_pb=[sig * sum(r['cutflow_nominal_notrig']['S1'][i] for r in rs) / sw for i in range(5)]),
                 by_pthat=dict(edges=rs[0]['nominal_by_pthat']['edges'],
                               sigma_pb=[sig * sum(r['nominal_by_pthat']['S1'][i] for r in rs) / sw
                                         for i in range(len(rs[0]['nominal_by_pthat']['S1']))]),
                 frac_truthmet_lt200=sum(r['nominal_truthmet_lt200_S1'] for r in rs) / max(sum(r['var']['nominal']['S1'] for r in rs), 1e-300),
                 frac_truthmet_lt150=sum(r['nominal_truthmet_lt150_S1'] for r in rs) / max(sum(r['var']['nominal']['S1'] for r in rs), 1e-300),
                 frac_pthat_lt150=sum(r['nominal_pthat_lt150_S1'] for r in rs) / max(sum(r['var']['nominal']['S1'] for r in rs), 1e-300))
        if 'nominal_by_ntauhad_S1' in rs[0]:
            t = [sum(r['nominal_by_ntauhad_S1'][i] for r in rs) for i in range(3)]
            d['frac_by_n_tau_had'] = [x / max(sum(t), 1e-300) for x in t]
        out[p] = d
    return out


def combine_slices(P):
    sl = sorted(k for k in P if k.startswith('mjs') and k != 'mjs')
    if not sl:
        return
    def comb(path):
        tot = 0.0; var = 0.0
        for s in sl:
            x = P[s]
            for k in path:
                x = x[k]
            tot += x['sigma_pb']; var += x['sigma_pb'] ** 2 / max(x['n_eff'], 1e-9)
        return dict(sigma_pb=tot, n_eff=tot ** 2 / var if var > 0 else 0.0)
    P['mjs'] = dict(n_generated=sum(P[s]['n_generated'] for s in sl), slices={s: dict(
        sigma_gen_pb=P[s]['sigma_gen_pb'], sigma_pb=P[s]['var']['nominal']['sigma_pb'], n_eff=P[s]['var']['nominal']['n_eff'],
        f_presel=P[s]['var']['nominal']['f_presel']) for s in sl},
        sigma_gen_pb=sum(P[s]['sigma_gen_pb'] for s in sl),
        var={v: comb(('var', v)) for v in P[sl[0]]['var']}, trig={k: comb(('trig', k)) for k in P[sl[0]]['trig']},
        met_cut={k: comb(('met_cut', k)) for k in P[sl[0]]['met_cut']}, v1_like=comb(('v1_like',)),
        sigma_gen_rel_err=max(P[s]['sigma_gen_rel_err'] for s in sl))


def ntrig(p, d):
    K = KFAC[p]; nom = d['var']['nominal']
    N = LUMI_PB * K * nom['sigma_pb']
    stat = math.hypot(1 / math.sqrt(max(nom['n_eff'], 1e-9)), d['sigma_gen_rel_err'])
    rat = {v: d['var'][v]['sigma_pb'] / nom['sigma_pb'] for v in d['var'] if v != 'nominal'}
    lo = min([1.0] + list(rat.values())); hi = max([1.0] + list(rat.values()))
    r = dict(N_trig=N, K=K, sigma_presel_pb=nom['sigma_pb'], rel_stat=stat, n_eff_passing=nom['n_eff'],
             ratio_to_nominal=rat, full_variation=dict(lo=N * lo, hi=N * hi, ln_width=0.5 * math.log(hi / lo)),
             trigger_nuisance_erf_shifted_ratio=d['trig']['erf_shifted']['sigma_pb'] / nom['sigma_pb'],
             trigger_off_ratio=d['trig']['none']['sigma_pb'] / nom['sigma_pb'],
             N_trig_by_met_cut={k: LUMI_PB * K * v['sigma_pb'] for k, v in d['met_cut'].items()},
             tag='ESTIMATE (generator-level Pythia 8 LO x K; MET model of p3-c); tail NOT SOURCED')
    for a, b in (('core', ('core_dn', 'core_up')), ('jes', ('jes_dn', 'jes_up')), ('soft', ('soft_dn', 'soft_up')),
                 ('tail_not_sourced', ('tail_dn', 'tail_up'))):
        r[f'ln_{a}'] = [math.log(max(rat[b[0]], 1e-300)), math.log(max(rat[b[1]], 1e-300))]
    return r


def main(argv):
    outd = Path(argv[0]); outd.mkdir(parents=True, exist_ok=True)
    recs = []; model = None
    for f in argv[1].split(','):
        d = json.loads(Path(f).read_text()); recs += d['records']; model = d['model']
    P = pool(recs); combine_slices(P)
    res = dict(schema='outputs/p3c/SCHEMA.md', lumi_pb=LUMI_PB, model=model, samples=P, n_trig={}, checks={})
    for p in ('znn', 'ztt', 'zll', 'mjw', 'mjs'):
        if p in P:
            res['n_trig'][p] = ntrig(p, P[p])
            log.info('%s: N_trig %.4g  rel stat %.3f  n_eff %.1f  full variation [%.3g, %.3g]', p, res['n_trig'][p]['N_trig'],
                     res['n_trig'][p]['rel_stat'], res['n_trig'][p]['n_eff_passing'], res['n_trig'][p]['full_variation']['lo'],
                     res['n_trig'][p]['full_variation']['hi'])
    # ---- internal check (b): multijet yield under two generation biases
    if 'mjw' in res['n_trig'] and 'mjs' in res['n_trig']:
        a, b = res['n_trig']['mjw'], res['n_trig']['mjs']
        lnr = math.log(a['N_trig'] / b['N_trig']); s = math.hypot(a['rel_stat'], b['rel_stat'])
        ok_n = a['n_eff_passing'] >= 100 and b['n_eff_passing'] >= 100
        ok_s = a['rel_stat'] <= 0.1 and b['rel_stat'] <= 0.1
        res['checks']['b_multijet_bias'] = dict(
            N_weighted=a['N_trig'], N_sliced=b['N_trig'], ln_ratio=lnr, sigma_ln=s, n_eff=[a['n_eff_passing'], b['n_eff_passing']],
            within_factor_2=abs(lnr) <= math.log(2), n_eff_ge_100=ok_n, sigma_ln_le_0p1_each=ok_s,
            verdict=('PASS' if abs(lnr) <= math.log(2) else 'FAIL') if (ok_n and ok_s) else 'NOT EVALUABLE',
            by_variation={v: math.log(P['mjw']['var'][v]['sigma_pb'] / P['mjs']['var'][v]['sigma_pb'])
                          for v in P['mjw']['var'] if P['mjs']['var'][v]['sigma_pb'] > 0})
        w = [1 / a['rel_stat'] ** 2, 1 / b['rel_stat'] ** 2]
        Nmj = (a['N_trig'] * w[0] + b['N_trig'] * w[1]) / sum(w)
        res['n_trig']['multijets'] = dict(N_trig=Nmj, rel_stat=1 / math.sqrt(sum(w)), combination='inverse-variance mean of the '
                                          'weighted and the sliced sample', ratio_to_nominal={
            v: (P['mjw']['var'][v]['sigma_pb'] * w[0] / P['mjw']['var']['nominal']['sigma_pb']
                + P['mjs']['var'][v]['sigma_pb'] * w[1] / P['mjs']['var']['nominal']['sigma_pb']) / sum(w)
            for v in P['mjw']['var'] if v != 'nominal'}, K=1.0, tag=a['tag'])
        rr = res['n_trig']['multijets']['ratio_to_nominal']
        lo = min([1.0] + list(rr.values())); hi = max([1.0] + list(rr.values()))
        res['n_trig']['multijets']['full_variation'] = dict(lo=Nmj * lo, hi=Nmj * hi, ln_width=0.5 * math.log(hi / max(lo, 1e-300)))
    # ---- (a) continuity with v1 on the unfiltered Z(nunu) sample
    if 'znn' in P:
        z = P['znn']
        res['checks']['a_continuity_znn_unfiltered'] = dict(
            sigma_v2_pb=z['var']['nominal']['sigma_pb'], sigma_v1_like_pb=z['v1_like']['sigma_pb'],
            ratio_v2_over_v1=z['var']['nominal']['sigma_pb'] / z['v1_like']['sigma_pb'],
            rel_stat=math.hypot(1 / math.sqrt(z['var']['nominal']['n_eff']), 1 / math.sqrt(z['v1_like']['n_eff'])),
            frac_v2_from_truth_met_below_200=z['frac_truthmet_lt200'], frac_v2_from_pthat_below_150=z['frac_pthat_lt150'],
            N_v1_like=LUMI_PB * K_V * z['v1_like']['sigma_pb'], N_v1_frozen=R.SM['Z(nunu)+j'],
            note='reported, no verdict (STR l.1356-1358); N_v1_like/N_v1_frozen compares this generator setup with v1\'s')
    # ---- pilot: M under v2
    sm12 = {k: v for k, v in R.SM.items() if k not in ('Z(tautau)', 'Z(ll) lost')}
    res['frozen'] = dict(N_SM12_v1=sum(sm12.values()), N_Z_v1=R.SM['Z(nunu)+j'], planning=dict(
        Ztautau=R.SM['Z(tautau)'], Zll=R.SM['Z(ll) lost'], multijets=R.MJ), M_v1_measured=993885.9,
        events_per_count_provisional=(sum(R.SM.values()) + R.MJ) / 993885.9)
    pdir = argv[2] if len(argv) > 2 else ''
    if pdir:
        W = []; cols = None
        for f in sorted(Path(pdir).glob('*.npz')):
            z = np.load(f); cols = json.loads(str(z['meta']))['cols']; W.append(z['w'])
        W = np.concatenate(W); c = {k: i for i, k in enumerate(cols)}
        full = W[:, c['n_gamma_veto']] == 0
        wv1 = W[:, c['w_v1']].astype(float)
        pil = dict(n_pilot_events=int(len(W)), M_v1_recomputed=float(wv1[wv1 > 0.06].sum() / 0.98),
                   M_v1_note='sum of w_v1 over the full-weight class (w_v1 > 0.05 x 0.98) / 0.98; frozen value 993,885.9 (BJO l.47)',
                   w_max_v2=1.0, M_v2={}, M_v2_low_class={}, n_pass_v2={})
        for k in cols:
            if k.startswith('w_v2_'):
                w = W[:, c[k]].astype(float)
                pil['M_v2'][k[5:]] = float(w[full].sum()); pil['M_v2_low_class'][k[5:]] = float(w[~full].sum() / 0.05)
                pil['n_pass_v2'][k[5:]] = int((w[full] > 0).sum())
        pil['M_v2_mean20'] = float(W[full, c['p_v2_mean20']].astype(float).sum())
        pil['ratio_sumw_v2_over_v1'] = float(W[:, c['w_v2_nominal']].astype(float).sum() / wv1.sum())
        pil['frac_v2_pass_with_v1_zero'] = float(W[(wv1 == 0), c['w_v2_nominal']].astype(float).sum() / W[:, c['w_v2_nominal']].astype(float).sum())
        pil['frac_v1_pass_with_v2_zero'] = float(wv1[W[:, c['w_v2_nominal']] == 0].sum() / wv1.sum())
        res['pilot'] = pil
        # events per pilot count, three readings (log §P6); additions at their MET-model N_trig
        add = {k: res['n_trig'][k]['N_trig'] for k in ('ztt', 'zll') if k in res['n_trig']}
        add['multijets'] = res['n_trig'].get('multijets', {}).get('N_trig')
        if None not in add.values() and len(add) == 3:
            M = pil['M_v2']['nominal']; n12 = sum(sm12.values()); nz = R.SM['Z(nunu)+j']
            rz_pilot = pil['ratio_sumw_v2_over_v1']
            fz = res['checks']['a_continuity_znn_unfiltered']['frac_v2_from_truth_met_below_200']
            rz = rz_pilot / (1 - fz)                    # incl. migration from truth MET < 200 GeV (not in the pilot)
            sa = sum(add.values())
            epc = dict(
                primary_STR_literal=dict(N_SM=n12 + sa, M=M, events_per_count=(n12 + sa) / M,
                                         Z_alone=nz / M, definition='v1 N_trig of the twelve processes kept (STR l.936) + additions; M = sum of v2 weights, full class'),
                secondary_Z_rescaled=dict(N_SM=n12 - nz + nz * rz + sa, M=M, events_per_count=(n12 - nz + nz * rz + sa) / M,
                                          Z_alone=nz * rz / M, z_ratio_v2_over_v1=rz,
                                          definition='Z(nunu) N_trig x (v2/v1 on the pilot)/(1 - migration fraction); eleven others kept'),
                tertiary_all12_rescaled=dict(N_SM=n12 * rz + sa, M=M, events_per_count=(n12 * rz + sa) / M,
                                             definition='all twelve v1 processes x the Z(nunu) ratio (proxy; no samples)'))
            for nm, e in epc.items():
                e['low_class_events_per_count'] = e['N_SM'] / max(pil['M_v2_low_class']['nominal'], 1e-9) if pil['M_v2_low_class']['nominal'] > 0 else None
            epc['by_variation_primary'] = {}
            for v, Mv in pil['M_v2'].items():
                if v == 'nominal' or v not in res['n_trig']['ztt']['ratio_to_nominal']:
                    continue
                sav = sum(res['n_trig'][k]['N_trig'] * res['n_trig'][k]['ratio_to_nominal'][v] for k in ('ztt', 'zll')) \
                    + add['multijets'] * res['n_trig']['multijets']['ratio_to_nominal'][v]
                epc['by_variation_primary'][v] = (n12 + sav) / Mv
            epc['not_validated_range_primary'] = [min(epc['by_variation_primary'].values()), max(epc['by_variation_primary'].values())]
            res['events_per_Z_pilot_count'] = epc
            res['checks']['c_multijet_share'] = dict(model_share_of_N_SM=add['multijets'] / (n12 + sa),
                                                     published_upper_bound=[0.010, 0.014],
                                                     source='arXiv:1712.02345 Table 8 ("Other" = QCD multijet + gamma+jets), 13 TeV, pile-up 23; retrieval_log #38',
                                                     note='reported, no verdict; order of magnitude only (STR l.1358-1360)')
            # ---- rule 6: pool shares, M_t ~ sqrt(N_t / c_t), SM part of the pool (CPU-h as in ADD §4.4)
            terms = R.NS['terms']; plan = R.NS['allocate'](R.NS['C_POOL']); smn = set(R.SM)
            cpu_sm = sum(plan[t] * cc / R.NS['H'] for t, n, cc in terms if t in smn)

            def table(N, mfull):
                tt = [(p, n, sum(COST[kind(p)]) / mfull[kind(p)]) for p, n in N.items()]
                al = R.NS['allocate'](cpu_sm, tt=tt)
                rows = {p: dict(N_t=n, cost_s_per_full_weight_event=cc, M_t=al[p], cpu_h=al[p] * cc / 3600,
                                floor_68=R.NS['U68'] * n / al[p]) for p, n, cc in tt}
                return dict(rows=rows, floor_sum=sum(r['floor_68'] for r in rows.values()), cpu_h=sum(r['cpu_h'] for r in rows.values()))
            N_new = dict(R.SM); N_new['Z(tautau)'] = add['ztt']; N_new['Z(ll) lost'] = add['zll']
            mz2 = dict(M_FULL); mz2['Z'] = M / 2.3e6
            res['pool_rule6'] = dict(cpu_h_SM=cpu_sm, rule='M_t ~ sqrt(N_t / c_t), c_t = (generation + chain) / full-weight fraction (ADD §4.4, as timed)',
                                     planning=table(dict(R.SM), M_FULL), reallocated=table(N_new, M_FULL),
                                     reallocated_v2_weight_fraction=table(N_new, mz2), full_weight_fraction_Z_v2=M / 2.3e6,
                                     multijets_own_population=dict(N_t=add['multijets'], M_loose=1.0e6, floor_68=R.NS['U68'] * add['multijets'] / 1.0e6,
                                                                   note='STR l.1365-1372: P(r) from a loose population of 1e6 events (B4-e)'))
    (outd / 'p3c_results.json').write_text(json.dumps(res, indent=1) + '\n')
    log.info('written %s', outd / 'p3c_results.json')


if __name__ == '__main__':
    main(sys.argv[1:])
