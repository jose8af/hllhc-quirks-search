"""val_v3.py -- Stage-3 validation V3: step convergence and the double-precision floor (plan §5, §6.3).

Events: P2 selection (input F_m<m>_p2.npz, template, |eta_pair| < 2.5), m = 200 and 1000 GeV, vertex at the origin,
s3 recorder (all surfaces).  Deterministic configurations so that runs pair across step sizes:
  B (3.8112 T, no material), BE (B + mean dE/dx, no straggling/MS), BK (B + one 3 MeV kick at r = 3 cm: J != 0 as MS).
Cells (events per mass): Lambda 1, 3 keV: max_boost 1e-2, 1e-3, 1e-4 (20 ev); 10 keV: 1e-2, 1e-3 (20 ev);
  20, 30 keV: 1e-2, 1e-3 (6 ev, B and BK only; the plan's 20 events at 30 keV cost ~8 CPU-h at 1e-3 -- reduced for
  budget, stated in VALIDATION_GATE.md); hmax 0.2 vs 0.05 cm at 0.3 and 1 keV (B, 1e-3, 20 ev).
Replicas (floor): B at the production setting 1e-2, initial momenta x (1 + 1e-14 N(0,1)), 3 replicas, at 10 (20 ev),
  20 and 30 keV (6 ev): per-event relative spread of Delta_s -> floor_flag calibration.
Metrics per pair of settings (test vs reference): Delta_s change (ds_all, plane through the vertex, median over events of
  the per-event ratio - 1); hit displacement for hits matched by (quirk, surface, crossing index): per event the max
  out-of-plane (along the reference plane normal) and in-plane component; median over events and worst event; fraction
  of events whose crossing counts differ.
Criteria (plan §5): Delta_s change < 1 % at Lambda <= 5 keV; hits < 1 um out of plane and < 5 um in plane (median over
  events of the per-event max) for the production setting (P2: 1e-3 at <= 1.5 keV, 1e-2 above; P1 B: 1e-3).
Output: sim/stage3/results/V3.json.  Run: nice pixi run python sim/stage3/validation/val_v3.py
"""
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import vcommon as V

CFG = {'B': dict(B0=V.B0, material=False), 'BE': dict(B0=V.B0, material=True, ms=False, strag=False),
       'BK': dict(B0=V.B0, material=False)}


def events(m, n):
    z = np.load(V.TT / 'data' / 'sim_stage3' / 'inputs' / f'F_m{m}_p2.npz')
    idx = np.where((z['tt_split'] == 0) & z['in_eta25'])[0][:n]
    return [(int(i), z['p_qp'][i], z['p_qm'][i]) for i in idx]


def job(a):
    m, lam, i, p1, p2, cfg, mb, hm, rep = a
    from T3_causal_s3 import run_causal_s3
    kw = dict(CFG[cfg])
    if cfg == 'BK':
        u = np.cross(p1, [0.0, 0.0, 1.0]); u /= np.linalg.norm(u)
        kw['kick'] = (0, 3.0, 3e-3 * u)
    if rep > 0:
        g = np.random.default_rng(1000 * rep + i)
        p1 = p1 * (1 + 1e-14 * g.standard_normal(3)); p2 = p2 * (1 + 1e-14 * g.standard_normal(3))
    t0 = time.perf_counter()
    r = run_causal_s3(p1, p2, float(m), lam, max_boost=mb, hmax_trk=hm, seed=1, **kw)
    return (m, lam, i, cfg, mb, hm, rep), dict(hits=r['hits'], status=r['status'], nsteps=r['nsteps'], wall=time.perf_counter() - t0)


def compare(ref, tst):
    """median/worst over events of per-event max out-of-plane / in-plane displacement [um], ds ratio, count changes."""
    from T3_causal_s3 import load_surfaces
    from s3_physics import plane_fit
    S = load_surfaces(); trk = np.where(np.isin(np.array(S['kinds']), ['IT', 'PS', '2S']))[0]
    oop = []; inp = []; ratio = []; nchg = 0; n = 0
    for k in ref:
        if k not in tst:
            continue
        a = ref[k]['hits']; b = tst[k]['hits']
        a = a[np.isin(a[:, 1], trk)]; b = b[np.isin(b[:, 1], trk)]
        if len(a) < 4 or len(b) < 4:
            continue
        n += 1
        da, nrm, _ = plane_fit(a[:, 4:7]); db, _, _ = plane_fit(b[:, 4:7])
        ratio.append(db / da if da > 0 else np.nan)
        ka = {(int(h[0]), int(h[1]), int(h[2])): h for h in a}; kb = {(int(h[0]), int(h[1]), int(h[2])): h for h in b}
        if set(ka) != set(kb):
            nchg += 1
        mo = 0.0; mi = 0.0
        for key in set(ka) & set(kb):
            d = kb[key][4:7] - ka[key][4:7]
            o = abs(d @ nrm); mo = max(mo, o); mi = max(mi, float(np.sqrt(max(d @ d - o * o, 0.0))))
        oop.append(mo * 1e4); inp.append(mi * 1e4)
    if n == 0:
        return {}
    ratio = np.array(ratio)
    return dict(n=n, ds_change_median=float(np.nanmedian(ratio) - 1), ds_change_abs_p90=float(np.nanpercentile(np.abs(ratio - 1), 90)),
                oop_med_um=float(np.median(oop)), oop_max_um=float(np.max(oop)), inp_med_um=float(np.median(inp)),
                inp_max_um=float(np.max(inp)), frac_count_changed=nchg / n)


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    T = []
    for m in (200, 1000):
        ev20 = events(m, 20); ev6 = ev20[:6]
        for lam in (1.0, 3.0):
            for cfg in ('B', 'BE', 'BK'):
                for mb in (1e-2, 1e-3, 1e-4):
                    T += [(m, lam, i, p1, p2, cfg, mb, 0.2, 0) for i, p1, p2 in ev20]
        for cfg in ('B', 'BE', 'BK'):
            for mb in (1e-2, 1e-3):
                T += [(m, 10.0, i, p1, p2, cfg, mb, 0.2, 0) for i, p1, p2 in ev20]
        for lam in (20.0, 30.0):
            for cfg in ('B', 'BK'):
                for mb in (1e-2, 1e-3):
                    T += [(m, lam, i, p1, p2, cfg, mb, 0.2, 0) for i, p1, p2 in ev6]
        for lam in (0.3, 1.0):
            T += [(m, lam, i, p1, p2, 'B', 1e-3, 0.05, 0) for i, p1, p2 in ev20]
            if lam == 0.3:
                T += [(m, lam, i, p1, p2, 'B', 1e-3, 0.2, 0) for i, p1, p2 in ev20]
        for lam, evs in ((10.0, ev20), (20.0, ev6), (30.0, ev6)):
            for rep in (1, 2, 3):
                T += [(m, lam, i, p1, p2, 'B', 1e-2, 0.2, rep) for i, p1, p2 in evs]
    T.sort(key=lambda t: -(t[1] ** 2 / t[6] * (1.6 if t[5] == 'BK' else 1.0)))
    tic = time.time()
    R = {}
    with ProcessPoolExecutor(7) as ex:
        for key, r in ex.map(job, T):
            R[key] = r
    out = dict(wall_s=time.time() - tic, cpu_s=sum(r['wall'] for r in R.values()), n_runs=len(R),
               status_counts=np.bincount([int(r['status']) for r in R.values()], minlength=6).tolist(), cells={}, replicas={})

    def sel(m, lam, cfg, mb, hm=0.2, rep=0):
        return {k[2]: v for k, v in R.items() if k[:2] == (m, lam) and k[3] == cfg and k[4] == mb and k[5] == hm and k[6] == rep}
    for m in (200, 1000):
        for lam in (1.0, 3.0, 10.0, 20.0, 30.0):
            for cfg in ('B', 'BE', 'BK'):
                for t_mb, r_mb in ((1e-2, 1e-3), (1e-3, 1e-4)):
                    a = sel(m, lam, cfg, r_mb); b = sel(m, lam, cfg, t_mb)
                    if a and b:
                        out['cells'][f'm{m}_L{lam:g}_{cfg}_{t_mb:g}vs{r_mb:g}'] = compare(a, b)
        for lam in (0.3, 1.0):
            a = sel(m, lam, 'B', 1e-3, 0.05); b = sel(m, lam, 'B', 1e-3, 0.2)
            if a and b:
                out['cells'][f'm{m}_L{lam:g}_B_hmax0.2vs0.05'] = compare(a, b)
        from s3_physics import plane_fit
        from T3_causal_s3 import load_surfaces
        S = load_surfaces(); trk = np.where(np.isin(np.array(S['kinds']), ['IT', 'PS', '2S']))[0]
        for lam in (10.0, 20.0, 30.0):
            ref = sel(m, lam, 'B', 1e-2)
            spread = []
            for i, r0 in ref.items():
                ds = []
                for rep in (0, 1, 2, 3):
                    rr = r0 if rep == 0 else sel(m, lam, 'B', 1e-2, 0.2, rep).get(i)
                    h = rr['hits']; h = h[np.isin(h[:, 1], trk)]
                    ds.append(plane_fit(h[:, 4:7])[0])
                ds = np.array(ds)
                spread.append(float(np.std(ds) / np.mean(ds)))
            out['replicas'][f'm{m}_L{lam:g}'] = dict(n=len(spread), median_rel_spread=float(np.median(spread)),
                                                     max_rel_spread=float(np.max(spread)), frac_gt_1pct=float(np.mean(np.array(spread) > 0.01)))
    # verdicts for the production settings
    verdict = {}
    for k, c in out['cells'].items():
        if not c:
            continue
        lam = float(k.split('_')[1][1:])
        prod = ('1e-03vs0.0001' in k or '0.001vs0.0001' in k) if lam <= 1.5 else ('0.01vs0.001' in k)
        if 'hmax' in k:
            prod = True
        if prod:
            ok_h = c['oop_med_um'] < 1.0 and c['inp_med_um'] < 5.0
            ok_d = abs(c['ds_change_median']) < 0.01 if (lam <= 5 and k.split('_')[2] == 'B') else True
            verdict[k] = dict(PASS=bool(ok_h and ok_d), oop_med_um=c['oop_med_um'], inp_med_um=c['inp_med_um'], ds_change=c['ds_change_median'])
    # P1 B production (1e-3) at 3 keV
    for m in (200, 1000):
        k = f'm{m}_L3_B_0.001vs0.0001'
        if out['cells'].get(k):
            c = out['cells'][k]
            verdict[k + '_P1'] = dict(PASS=bool(abs(c['ds_change_median']) < 0.01 and c['oop_med_um'] < 1 and c['inp_med_um'] < 5),
                                      ds_change=c['ds_change_median'], oop_med_um=c['oop_med_um'], inp_med_um=c['inp_med_um'])
    out['verdicts'] = verdict
    out['PASS'] = bool(all(v['PASS'] for v in verdict.values()))
    V.dump('V3.json', out)
    import json
    print(json.dumps(dict(verdicts=verdict, replicas=out['replicas'], status=out['status_counts'], wall=out['wall_s'], cpu=out['cpu_s']), indent=1))
