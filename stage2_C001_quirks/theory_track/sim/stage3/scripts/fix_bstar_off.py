"""fix_bstar_off.py -- Stage-3 fix pass R1 (critical A-1, approved run): B*-off vs B*-on c at Lambda = 5 keV on P1 events.

Method = Stage-1 FIX2 (analytic/numerics/NUMERICS.md §13; nm_bstar.bstar_off_fields): the uniform lab fields
E_lab = gamma^2 beta x fB, B_lab = gamma^2 [beta (beta.fB) - beta^2 fB] transform to exactly (E*, B* = 0) in the event's
pair (P0) frame.  The production kernel T3_causal_s3 has no E-field input, so BOTH arms (on and off) are run with the
Stage-1 general-field kernel analytic/numerics/nm_kernel.run (imported read-only; bit-identical to code/T3_causal for
z-only B), at the production P1 settings: vacuum, vertex at the origin, max_boost 1e-3, hmax_trk 0.2 cm, qcap 2^19.
Delta_s = plane (through the vertex) fit on the 10 T3 barrel layers (layer id < 10), as ds_barrel_um in production.
c2 = (2 Ds(B0/2)/Ds(B0) - 1)/ln 2.  The B*-on arm is also compared with the production ds_barrel_um (control).

Events: P1 F_m500 and F_m1000 at 5 keV (B and B2 both status 1), 16 per k_B bin [0,2),[2,4),[4,6),[6,10),[10,inf)
(8 with rng 2026, then 8 more with rng 2027), plus for F_m1000 the 16 rows of results/c5kev_diag.json (12 top-r k_B >= 6,
4 k_B < 2 controls; selected on large r, so they are reported separately and NOT used in the k_B-bin medians).
Raw: data/sim_stage3/fix_r1/bstar/<pk>_r<row>.npz (skip if present).  Output: results/FIX_bstar_off.json.
Run (theory_track/): pixi run python sim/stage3/scripts/fix_bstar_off.py [--time]
"""
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import s3common as C

NUM = C.TT / 'analytic' / 'numerics'
RAW = C.DATA / 'fix_r1' / 'bstar'
BINS = ((0, 2), (2, 4), (4, 6), (6, 10), (10, 1e9))
LAM = 5.0


def job(a):
    pk, row, p1, p2, m = a
    fn = RAW / f'{pk}_r{int(row)}.npz'
    if fn.exists():
        return str(fn), 0.0
    for p in (str(NUM), str(C.TT / 'code')):
        if p not in sys.path:
            sys.path.insert(0, p)
    from nm_kernel import run
    from nm_bstar import bstar_off_fields
    from s3_physics import plane_fit
    t0 = time.process_time()
    out = {}
    for arm in ('on', 'off'):
        for cfg, f in (('B', 1.0), ('B2', 0.5)):
            kw = dict(max_boost=1e-3, hmax_trk=0.2, qcap=1 << 19, max_steps=20_000_000_000)
            if arm == 'on':
                r = run(p1, p2, m, LAM, B0=C.B0 * f, **kw)
            else:
                El, Bl = bstar_off_fields(p1, p2, m, (0.0, 0.0, C.B0 * f))
                r = run(p1, p2, m, LAM, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, **kw)
            H = r['hits']; H = H[H[:, 1] < 10]
            ds = plane_fit(H[:, 3:6], np.zeros(3))[0] * 1e4 if len(H) >= 4 else np.nan
            out[f'{arm}_{cfg}'] = (ds, int(r['status']))
    cpu = time.process_time() - t0
    np.savez(fn, **{k + '_ds': v[0] for k, v in out.items()}, **{k + '_st': v[1] for k, v in out.items()}, cpu=cpu)
    return str(fn), cpu


def events():
    S = np.load(C.SUMM / 'events_p1.npz'); keys = list(S['point_keys'])
    rng = np.random.default_rng(2026); rng2 = np.random.default_rng(2027)
    c5 = [e['row'] for e in json.load(open(C.RES / 'c5kev_diag.json'))['events']]
    ev = {}
    for pk, m in (('F_m500', 500.0), ('F_m1000', 1000.0)):
        def get(cfg):
            sel = S['point'] == keys.index(f'p1/{pk}/L5_{cfg}')
            o = np.argsort(S['ev_index'][sel], kind='stable')
            return {c: S[c][sel][o] for c in ('row', 'ds_barrel_um', 'status', 'c_ev', 'k_B', 'eps_perp', 'p_qp', 'p_qm', 'gstar')}
        b, h = get('B'), get('B2')
        ok = (b['status'] == 1) & (h['status'] == 1) & (b['ds_barrel_um'] > 0)
        pick = set()
        for a, bb in BINS:
            idx = np.where(ok & (b['k_B'] >= a) & (b['k_B'] < bb))[0]
            pick |= set(rng.choice(idx, min(8, len(idx)), replace=False).tolist())
        rand = set(pick)
        for a, bb in BINS:   # second batch (8 more per bin, rng 2027), the first batch is kept as a subset
            idx = np.array(sorted(set(np.where(ok & (b['k_B'] >= a) & (b['k_B'] < bb))[0].tolist()) - rand))
            rand |= set(rng2.choice(idx, min(8, len(idx)), replace=False).tolist())
        pick = set(rand)
        if pk == 'F_m1000':
            pick |= set(np.where(np.isin(b['row'], c5) & ok)[0].tolist())
        for i in sorted(pick):
            ev[(pk, int(b['row'][i]))] = dict(random=i in rand, m=m, p1=b['p_qp'][i], p2=b['p_qm'][i], k_B=float(b['k_B'][i]),
                                              eps=float(b['eps_perp'][i]), c_ev=float(b['c_ev'][i]), gstar=float(b['gstar'][i]),
                                              dsB_prod=float(b['ds_barrel_um'][i]), dsB2_prod=float(h['ds_barrel_um'][i]),
                                              c5kev=int(b['row'][i]) in c5)
    return ev


def bmed(x, rng, nb=1000):
    x = np.asarray(x); x = x[np.isfinite(x)]
    if len(x) < 2:
        return float(np.median(x)) if len(x) else np.nan, np.nan
    return float(np.median(x)), float(np.std([np.median(rng.choice(x, len(x))) for _ in range(nb)]))


def arm_diff(on, off, rng, nb=1000):
    """median(r_on/c_ev) - median(r_off/c_ev) over the same events, paired bootstrap error (robust to the heavy tails)."""
    on = np.asarray(on); off = np.asarray(off); n = len(on)
    d0 = float(np.median(on) - np.median(off))
    bs = [np.median(on[i]) - np.median(off[i]) for i in (rng.integers(0, n, n) for _ in range(nb))]
    return d0, float(np.std(bs))


def analyse(ev):
    rng = np.random.default_rng(5)
    rows = []
    for (pk, row), e in ev.items():
        fn = RAW / f'{pk}_r{row}.npz'
        if not fn.exists():
            continue
        d = np.load(fn)
        st = all(int(d[f'{a}_{c}_st']) == 1 for a in ('on', 'off') for c in ('B', 'B2'))
        con = (2 * d['on_B2_ds'] / d['on_B_ds'] - 1) / np.log(2)
        coff = (2 * d['off_B2_ds'] / d['off_B_ds'] - 1) / np.log(2)
        cprod = (2 * e['dsB2_prod'] / e['dsB_prod'] - 1) / np.log(2)
        rows.append(dict(point=pk, row=row, random=e['random'], k_B=e['k_B'], eps_perp=e['eps'], gstar=e['gstar'], c_ev=e['c_ev'], c5kev=e['c5kev'],
                         status_ok=st, c_prod=float(cprod), c_on=float(con), c_off=float(coff),
                         dsB_prod=e['dsB_prod'], dsB_on=float(d['on_B_ds']), dsB_off=float(d['off_B_ds']),
                         dsB2_on=float(d['on_B2_ds']), dsB2_off=float(d['off_B2_ds']), cpu_s=float(d['cpu'])))
    res = dict(method='Stage-1 FIX2 B*-off fields (nm_bstar) with nm_kernel.run; both arms same kernel; P1 production settings',
               lam_keV=LAM, n_events=len(rows), cpu_h=sum(r['cpu_s'] for r in rows) / 3600, tag='VERIFIED (measured, truth level)',
               bins={}, control={}, events=rows)
    for pk in ('F_m500', 'F_m1000', 'pooled', 'c5kev_top_r', 'c5kev_controls'):
        if pk.startswith('c5kev'):
            R = [r for r in rows if r['status_ok'] and r['c5kev'] and ((r['k_B'] >= 6) == (pk == 'c5kev_top_r'))]
        else:
            R = [r for r in rows if r['status_ok'] and r['random'] and (pk == 'pooled' or r['point'] == pk)]
        dprod = [r['dsB_on'] / r['dsB_prod'] - 1 for r in R]
        res['control'][pk] = dict(n=len(R), median_rel_dsB_on_vs_prod=float(np.median(dprod)) if R else None,
                                  max_abs_rel=float(np.max(np.abs(dprod))) if R else None,
                                  median_abs_c_on_minus_prod=float(np.median([abs(r['c_on'] - r['c_prod']) for r in R])) if R else None)
        res['bins'][pk] = {}
        for a, bb in BINS + ((0, 1e9),):
            s = [r for r in R if a <= r['k_B'] < bb]
            if not s:
                continue
            on = [(r['c_on'] - r['c_ev']) / r['c_ev'] for r in s]
            off = [(r['c_off'] - r['c_ev']) / r['c_ev'] for r in s]
            dif = [r['c_on'] - r['c_off'] for r in s]
            difrel = [(r['c_on'] - r['c_off']) / r['c_ev'] for r in s]
            dsrat = [r['dsB_on'] / r['dsB_off'] - 1 for r in s]
            k = f'kB[{a:g},{bb:g})' if bb < 1e9 else (f'kB>={a:g}' if a > 0 else 'all')
            res['bins'][pk][k] = dict(n=len(s), median_eps_perp=float(np.median([r['eps_perp'] for r in s])),
                                      r_on_over_cev=bmed(on, rng), r_off_over_cev=bmed(off, rng),
                                      dc_on_minus_off=bmed(dif, rng), dc_on_minus_off_over_cev=bmed(difrel, rng),
                                      dsB_on_over_off_minus1=bmed(dsrat, rng),
                                      arm_median_difference=arm_diff(on, off, rng),
                                      frac_abs_dc_gt_0p01=float(np.mean(np.abs(dif) > 0.01)))
    C.dump('FIX_bstar_off.json', res)
    return res


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    ev = events()
    tasks = [(pk, row, e['p1'], e['p2'], e['m']) for (pk, row), e in ev.items()]
    if '--time' in sys.argv:
        tasks = tasks[:1]
    tasks.sort(key=lambda t: -ev[(t[0], t[1])]['k_B'])
    tic = time.time()
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        for fn, cpu in ex.map(job, tasks):
            print(f'{fn.split("/")[-1]} {cpu:.0f} s', flush=True)
    print('wall', time.time() - tic, 'n tasks', len(tasks))
    if '--time' not in sys.argv:
        res = analyse(ev)
        print(json.dumps(dict(control=res['control'], bins=res['bins'], cpu_h=res['cpu_h']), indent=1))


if __name__ == '__main__':
    main()
