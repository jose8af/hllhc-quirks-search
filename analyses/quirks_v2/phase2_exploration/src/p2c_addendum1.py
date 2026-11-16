"""p2c_addendum1.py -- every table of strategy addendum 1, VERSION 2 (after the critical review).  ESTIMATE.

  /usr/bin/python3 -I p2c_addendum1.py <out.json>

Phase-1 budget script: through p2c_rule1 (byte-identical copy, executed unchanged).  Changed inputs: the named
OVERRIDES below, each with its Phase-2 source.  The Geant4 vertex partition is read from
outputs/partition_p2-c-part-0.json (written from data/p2c/p2-c-part/000/p2-c-part-0.npz with p2c_g4vtx.classify).
(Version 1 of this script, which printed the tables of the first addendum, is replaced; its output
data/p2c/p2-c-addendum1/000/p2-c-addendum1-0.json is kept.)
"""
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import p2c_rule1 as R  # noqa: E402

NS = R.NS
NTRIG, SM, MJ, NZ = R.NTRIG, R.SM, R.MJ, R.NZ
U68, H, alloc = NS['U68'], NS['H'], NS['allocate']
PART = json.loads((HERE.parent / 'outputs' / 'partition_p2-c-part-0.json').read_text())
OVERRIDES = dict(
    PILOT_HS_GENERATED=2.3e6,
    # weight classes of the v1 preselection, 10,000 events per process [V: p2-c-t-hs0]: full class M = sum(w) / w_max
    M_FULL={'Z': 0.4396, 'W': 0.2657, 'tt': 0.1205}, LOW_CLASS={'Z': (0.0025, 0.05), 'W': (0.0516, 0.05), 'tt': (0.0946, 0.05)},
    F_PASS={'Z': 0.442, 'W': 0.315, 'tt': 0.2105},
    F_HS=1.5945 / 1.560,             # hard-scatter share of the parents on top of 200 x minimum bias [E: v1 rates, STR l.255]
    R08_PILEUP=(87.9, 117.9, 148.0),  # STR l.2819 range and its centre
    COST=dict(Z=(0.042, 0.085), W=(0.086, 0.085), tt=(0.460, 0.111), tt_forced=(0.216, 0.111)),   # [V: p2-c-t-hs0; forced: p2-c-t-ttf 0.327 s]
    CHAIN_B1=dict(DIF=0.0037, DIFC=0.0037, NI22=0.0038, NI30=0.0059, NI61=0.0059, NIX=0.0059, NIC=0.0059),   # [V: p2-c-t-b1x]
    G4_ALL_MS=PART['g4_ms_per_firing'], G4_NI_MS=0.0469,
)
O = OVERRIDES
NF = PART['n_fire']
CNT = {k: v['all'] for k, v in PART['counts'].items()}
CLASSES = dict(DIF=CNT['dif'] + CNT['k0l'], DIFC=CNT['difc'], NI22=CNT['ni22'], NI30=CNT['ni30'], NI61=CNT['ni61'],
               NIX=CNT['nix'], NIC=CNT['nic'])
RATE = {k: 200.0 * PART['pool_in_road_per_interaction'] * c / NF * O['F_HS'] for k, c in CLASSES.items()}   # per triggered event
NT = {k: NTRIG * r for k, r in RATE.items()}
SIZES = {'S1 (10^6 per sample)': dict(DIF=1e6, DIFC=1e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=1e6, NIC=1e6),
         'S2 (proposed: 4, 4, 1, 1, 1, 4, 2 x 10^6)': dict(DIF=4e6, DIFC=4e6, NI22=1e6, NI30=1e6, NI61=1e6, NIX=4e6, NIC=2e6)}
ND = 100000


def b50(gam, pu, seed=7):
    rnd = random.Random(seed); bs = []
    for _ in range(ND):
        b = sum(k * rnd.gammavariate(m + 1, 1.0) for k, m in gam)
        x = pu[0] * math.exp(pu[1] * rnd.gauss(0, 1))
        bs.append(b + min(x, -pu[2] * rnd.expovariate(1.0)))
    bs.sort()
    return bs[ND // 2]


def kind(p):
    return 'Z' if p.startswith('Z') else ('tt' if p.startswith(('tt', 'tW', 't-')) else 'W')


def sm_terms(n_generated):
    """all SM + multijets through the Z(nunu) pilot: full-weight class and the 0.05 class as two counted terms."""
    tot = sum(SM.values()) + MJ
    m_full = n_generated * O['M_FULL']['Z']
    k_full = tot / m_full
    f_low, w_low = O['LOW_CLASS']['Z']
    return k_full, k_full * w_low / 0.98, m_full


def readings(sizes, terms_in_rule, n_gen):
    k_full, k_low, _ = sm_terms(n_gen)
    base = [(NT[t] / sizes[t], t) for t in terms_in_rule]
    out = {}
    pus = [('R09', R.PU9)] + [(f'R08 pile-up {x:g}', (x, 0.43, R.PU_CAP)) for x in O['R08_PILEUP']]
    for lab, pu in pus:
        def gam(counts):
            return [(k, counts.get(t, 0)) for k, t in base] + [(k_full, counts.get('Z', 0)), (k_low, 0)]
        r = dict(b50_all_zero=round(b50(gam({}), pu), 1))
        for t in ['Z'] + [x for x in terms_in_rule if x not in ('NI22', 'NI30', 'NI61')]:     # crossings: 20,000 draws
            c = None
            for m in range(0, 40):
                if R.b50(gam({t: m}), pu) > 300:
                    c = m
                    break
            r['cross_' + t] = c
        out[lab] = r
    return out


def reach(floors):
    gam = [(x, 0) for x in floors] + [NS['MJK']]
    pmf, (b16, b50_, b84) = NS['pmf_pred'](gam, (R.PU9,))
    lim = [NS['s95_pmf'](pmf, NS['quant_pmf'](pmf, f)) for f in (0.16, 0.5, 0.84)]
    return dict(B16=b16, B50=b50_, B84=b84, s95_median=lim[1], reach_median=NS['reach_of'](lim[1]), reach_84_edge=NS['reach_of'](lim[2]))


def main(out):
    res = dict(overrides=O, partition=dict(n_fire=NF, counts=CNT, sum=PART['counts_sum'], n_vertices=PART['n_vertices']),
               copy_sha256=R.hashlib.sha256(R.COPY.read_bytes()).hexdigest(), tag='ESTIMATE')
    res['classes'] = {k: dict(count=CLASSES[k], yield_per_firing=CLASSES[k] / NF, rate_per_triggered_event=RATE[k], N_t=NT[k],
                              events_per_count={s: NT[k] / sz[k] for s, sz in SIZES.items()}) for k in CLASSES}
    res['not_B1'] = dict(conversion=CNT['conversion'], other=CNT['other'])
    kf, kl, mf = sm_terms(O['PILOT_HS_GENERATED'])
    res['sm'] = dict(events_per_full_weight_count=kf, events_per_low_weight_count=kl, M_full=mf, Z_alone=NZ / mf,
                     by_pilot_size={f'{n:g}': sm_terms(n)[0] for n in (0.83e6, 1.5e6, 2.3e6, 3.5e6, 5.23e6)})
    allt = list(CLASSES); len_t = ['DIF', 'NI22', 'NI30', 'NI61']
    res['readings'] = {}
    for sl, sz in SIZES.items():
        res['readings'][f'strict (7 B1 terms), {sl}'] = readings(sz, allt, 2.3e6)
        res['readings'][f'lenient (DIF + 3 NI radii read; others recorded), {sl}'] = readings(sz, len_t, 2.3e6)
    s2 = SIZES['S2 (proposed: 4, 4, 1, 1, 1, 4, 2 x 10^6)']
    res['readings']['strict, S2, Z pilot (c) 5.23e6 generated'] = readings(s2, allt, 5.23e6)
    res['readings']['strict, S2, Z pilot 3.5e6 generated'] = readings(s2, allt, 3.5e6)
    # ---- pilot cost for S1 and S2 [E from V unit costs]
    cost = {}
    for sl, sz in SIZES.items():
        n_all = max(sz['NIX'] / (CLASSES['NIX'] / NF), sz['DIF'] / (CLASSES['DIF'] / NF), sz['DIFC'] / (CLASSES['DIFC'] / NF),
                    sz['NIC'] / (CLASSES['NIC'] / NF))
        need_ni = max(sz['NI22'] - n_all * CLASSES['NI22'] / NF, 0.0)
        n_ni = need_ni / (CLASSES['NI22'] / NF / (1 - 0.0))          # NI pass yield per firing taken as the all-pass first-arc yield
        g4 = (n_all * O['G4_ALL_MS'] + n_ni * O['G4_NI_MS']) / 3.6e6
        chain = sum(sz[t] * O['CHAIN_B1'][t] for t in sz) / 3600.0
        zc = O['PILOT_HS_GENERATED'] * 0.127 / 3600.0
        nev = sum(sz.values())
        cost[sl] = dict(firings_all=n_all, firings_ni=n_ni, g4_cpu_h=g4, chain_cpu_h=chain, mbgen_cpu_h=10.0, z_cpu_h=zc,
                        total_cpu_h=g4 + chain + 10.0 + zc, b1_events=nev, storage_gb=nev * 3.5e-6 + nev * 0.8e-6 + 69.5 + 1.5)
    res['pilot_cost'] = cost
    # ---- Table 4.4a at fixed CPU
    terms = NS['terms']; plan = alloc(NS['C_POOL'])
    smn = set(SM)
    cpu_sm = sum(plan[t] * c / H for t, n, c in terms if t in smn); cpu_b1 = sum(plan[t] * c / H for t, n, c in terms if t not in smn)
    tabs = {}
    for lab, forced, pf in (('as timed', False, False), ('forced tt', True, False), ('preselection before the chain', False, True),
                            ('both', True, True)):
        tt = []
        for p, n in SM.items():
            k = kind(p)
            cg, cc = O['COST']['tt_forced' if (k == 'tt' and forced) else k]
            cge = cg + (O['F_PASS'][k] if pf else 1.0) * cc
            tt.append((p, n, cge / O['M_FULL'][k], cge, k))
        al = alloc(cpu_sm, tt=[(t, n, c) for t, n, c, _, _ in tt])
        rows = [dict(term=t, N_t=n, cost_gen_ms=1e3 * cge, cost_eff_ms=1e3 * c, M_eff=al[t], M_gen=al[t] / O['M_FULL'][k],
                     floor68=U68 * n / al[t]) for t, n, c, cge, k in tt]
        tabs[lab] = dict(rows=rows, floor_SM=sum(r['floor68'] for r in rows), tt_type_share=sum(r['floor68'] for r in rows if kind(r['term']) == 'tt') / sum(r['floor68'] for r in rows))
    res['table_SM'] = tabs
    g4_per = {t: O['G4_ALL_MS'] * 1e-3 / (CLASSES[t] / NF) for t in ('DIF', 'DIFC', 'NIX', 'NIC')}
    g4_per.update({t: O['G4_NI_MS'] * 1e-3 / ((CLASSES['NI22'] + CLASSES['NI30'] + CLASSES['NI61']) / NF) for t in ('NI22', 'NI30', 'NI61')})
    b1 = {}
    for lab, use in (('strict (7 terms)', allt), ('lenient (4 terms)', len_t)):
        tt = [(t, NT[t], O['CHAIN_B1'][t] + g4_per[t]) for t in use]
        al = alloc(cpu_b1, tt=tt)
        b1[lab] = dict(rows=[dict(term=t, N_t=n, cost_ms=1e3 * c, M_t=al[t], floor68=U68 * n / al[t]) for t, n, c in tt],
                       floor_B1=sum(U68 * n / al[t] for t, n, c in tt))
    res['table_B1'] = b1
    res['floor_sums'] = {f'{a} + {b_}': tabs[a]['floor_SM'] + b1[b_]['floor_B1'] for a in tabs for b_ in b1}
    res['cpu_for_SM_floor'] = {f'floor {x:g}': {a: cpu_sm * tabs[a]['floor_SM'] / x for a in ('as timed', 'both')} for x in (39.0, 8.6)}
    # ---- reach with every ceiling empty (strategy's own functions; EST, v1 placeholder efficiencies)
    res['reach'] = {}
    for a, b_ in (('as timed', 'strict (7 terms)'), ('both', 'strict (7 terms)'), ('as timed', 'lenient (4 terms)'), ('both', 'lenient (4 terms)')):
        fl = [r['floor68'] / U68 for r in tabs[a]['rows']] + [r['floor68'] / U68 for r in b1[b_]['rows']]
        res['reach'][f'{a} + {b_}'] = reach(fl)
    res['reach']['frozen (check: 790 [712])'] = reach([n / plan[t] for t, n, c in terms])
    # ---- toys and the lines on the 45 ms guess, against the approved figures
    ratio = {'31': 638 / 652.0, '60': 11052 / 652.0}
    pil = cost['S2 (proposed: 4, 4, 1, 1, 1, 4, 2 x 10^6)']['total_cpu_h']
    extra = dict(pilot_overrun=pil - 54.5, multijet_loose=1e6 * 0.100 / 3600 - 12.5, b6c=25.0 * (0.127 / 0.045) - 25.0)
    res['projection'] = dict(approved=4609.0, threshold=5992.0, extra_lines=extra,
                             total_by_toy_scaling={k: 4609.0 - 183.0 + 183.0 * v + sum(extra.values()) for k, v in ratio.items()})
    Path(out).write_text(json.dumps(res, indent=1))


if __name__ == '__main__':
    main(sys.argv[1])
