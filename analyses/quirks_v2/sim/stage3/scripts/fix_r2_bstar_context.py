"""fix_r2_bstar_context.py -- Stage-3 fix pass R2 (review B-1, C-1, C-2): significance and context of the B*-off test.

No new production.  Reads only saved outputs:
  results/FIX_bstar_off.json   (per-event c_on, c_off, c_prod, c_ev, k_B, eps_perp of the 160 random + 11 c5kev events)
  data/sim_stage3/summary/events_p1.npz   (full P1 production at 5 keV, F_m500 + F_m1000)
and writes results/FIX_R2_bstar_context.json with:
  (1) paired on - off difference of the median r/c_ev (same events, paired bootstrap; fix_bstar_off.arm_diff) for the
      k_B bins and the pooled selections k_B < 4, k_B >= 6, all;
  (2) the B*-off arm against the full production population of the same two masses (E500 + E1000, same status cuts as
      fix_bstar_off.events), per k_B bin and all; the difference is also given against the production complement
      (production events NOT in the B*-off sample) so that the two samples are disjoint;
  (3) per-event (c_on - c_off)/c_ev quantiles per bin (B* as a widening of the per-event c distribution);
  (4) the on-arm control in c units: events with |c_on - c_prod| > 0.01, max, and their Ds_B (review C-1);
  (5) the Stage-1 floor-law allowance (fix_a1_floor.py formula) at the B*-off subsample's own eps_perp (review C-2).
Run (theory_track/): pixi run python sim/stage3/scripts/fix_r2_bstar_context.py   (< 1 CPU-min)
"""
import json

import numpy as np

import s3common as C
from fix_bstar_off import BINS, arm_diff, bmed

U = 2.2e-16   # as fix_a1_floor.py
NB = 20000


def key(a, bb):
    return f'kB[{a:g},{bb:g})' if bb < 1e9 else (f'kB>={a:g}' if a > 0 else 'all')


def production():
    """r/c_ev at 5 keV for every F_m500/F_m1000 production event passing the fix_bstar_off selection."""
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    out = []
    for pk in ('F_m500', 'F_m1000'):
        def get(cfg):
            sel = S['point'] == keys.index(f'p1/{pk}/L5_{cfg}')
            o = np.argsort(S['ev_index'][sel], kind='stable')
            return {c: S[c][sel][o] for c in ('row', 'ds_barrel_um', 'status', 'c_ev', 'k_B')}
        b, h = get('B'), get('B2')
        ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
        c2 = (2 * h['ds_barrel_um'] / b['ds_barrel_um'] - 1) / np.log(2)
        for i in np.where(ok)[0]:
            out.append((pk, int(b['row'][i]), float(b['k_B'][i]), float((c2[i] - b['c_ev'][i]) / b['c_ev'][i])))
    return out


def main():
    rng = np.random.default_rng(20261013)
    BO = json.load(open(C.RES / 'FIX_bstar_off.json'))
    ev = [e for e in BO['events'] if e['random'] and e['status_ok']]
    sample = {(e['point'], e['row']) for e in ev}
    prod = production()
    sels = [*BINS, (0, 4), (6, 1e9), (0, 1e9)]
    res = dict(source=['results/FIX_bstar_off.json', 'data/sim_stage3/summary/events_p1.npz'], lam_keV=5.0, n_bootstrap=NB,
               tag='VERIFIED (measured, truth level); attribution remains ESTIMATE', paired_on_minus_off={},
               off_vs_production={}, per_event_on_minus_off_over_cev={}, floor_allowance_subsample={}, control_c={})
    for a, bb in sels:
        s = [e for e in ev if a <= e['k_B'] < bb]
        on = np.array([(e['c_on'] - e['c_ev']) / e['c_ev'] for e in s]); off = np.array([(e['c_off'] - e['c_ev']) / e['c_ev'] for e in s])
        d, de = arm_diff(on, off, rng, NB)
        k = key(a, bb)
        res['paired_on_minus_off'][k] = dict(n=len(s), on=bmed(on, rng, NB), off=bmed(off, rng, NB), on_minus_off=[d, de],
                                              significance=d / de, frac_on_gt_off=float(np.mean(on > off)))
        P = np.array([r for (pk, row, kb, r) in prod if a <= kb < bb])
        Pc = np.array([r for (pk, row, kb, r) in prod if a <= kb < bb and (pk, row) not in sample])
        p, pe = bmed(P, rng, NB); pc, pce = bmed(Pc, rng, NB); o, oe = bmed(off, rng, NB)
        res['off_vs_production'][k] = dict(n_prod=len(P), prod=[p, pe], n_off=len(s), off=[o, oe],
                                           prod_minus_off=[p - o, float(np.hypot(pe, oe))], significance=(p - o) / np.hypot(pe, oe),
                                           n_prod_complement=len(Pc), prod_complement=[pc, pce],
                                           complement_minus_off=[pc - o, float(np.hypot(pce, oe))],
                                           significance_complement=(pc - o) / np.hypot(pce, oe))
        q = np.array([(e['c_on'] - e['c_off']) / e['c_ev'] for e in s])
        res['per_event_on_minus_off_over_cev'][k] = dict(n=len(s), median=bmed(q, rng, NB),
                                                         q10_25_50_75_90=np.quantile(q, [.1, .25, .5, .75, .9]).tolist(),
                                                         frac_positive=float(np.mean(q > 0)))
        eps = np.array([e['eps_perp'] for e in s]); cm = float(np.median([e['c_ev'] for e in s]))
        fl = [float(np.median(1.06 * 3 * A * U / eps ** 2 / np.log(2)) / cm) for A in (1.9, 5.0)]
        res['floor_allowance_subsample'][k] = dict(median_eps_perp=float(np.median(eps)), floor_rel_range=fl)
    dc = np.array([abs(e['c_on'] - e['c_prod']) for e in ev])
    big = [dict(point=e['point'], row=e['row'], k_B=e['k_B'], abs_dc=abs(e['c_on'] - e['c_prod']), dsB_on_um=e['dsB_on'],
                rel_dsB_on_vs_prod=e['dsB_on'] / e['dsB_prod'] - 1) for e in ev if abs(e['c_on'] - e['c_prod']) > 0.01]
    res['control_c'] = dict(n=len(ev), median_abs_dc=float(np.median(dc)), max_abs_dc=float(dc.max()),
                            n_abs_dc_gt_0p01=len(big), events_abs_dc_gt_0p01=big)
    C.dump('FIX_R2_bstar_context.json', res)
    f = lambda x: f'{100 * x[0]:+.1f} +- {100 * x[1]:.1f} %'  # noqa: E731
    for k in res['paired_on_minus_off']:
        a = res['paired_on_minus_off'][k]; b = res['off_vs_production'][k]; c = res['per_event_on_minus_off_over_cev'][k]
        print(f"{k:10s} n={a['n']:3d} on {f(a['on'])} off {f(a['off'])} on-off {f(a['on_minus_off'])} ({a['significance']:.1f}s) | "
              f"prod(n={b['n_prod']}) {f(b['prod'])} prod-off {f(b['prod_minus_off'])} ({b['significance']:.1f}s; complement "
              f"{b['significance_complement']:.1f}s) | per-ev med {f(c['median'])} IQR {100 * c['q10_25_50_75_90'][1]:+.0f}..{100 * c['q10_25_50_75_90'][3]:+.0f} % "
              f"| floor {100 * res['floor_allowance_subsample'][k]['floor_rel_range'][0]:.1f}-{100 * res['floor_allowance_subsample'][k]['floor_rel_range'][1]:.1f} %")
    print('control c:', {k: v for k, v in res['control_c'].items() if k != 'events_abs_dc_gt_0p01'})
    for e in big:
        print('  ', e)


if __name__ == '__main__':
    main()
