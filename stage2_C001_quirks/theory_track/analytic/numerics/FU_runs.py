"""FU_runs.py -- E2 follow-up (post-unblinding) runs.  Blind results are not modified; new outputs only.

FU1 (c at 3 keV): the M3 events (T2 cache, seed 777 + m, |eta| < 1) re-run at B0 x f, f in {1, 1/2, 1/4, 1/20}:
  'fine'   : causal max_boost 1e-3, hmax 0.02 cm, all 120 events, m = 500, 1000 GeV, Lambda = 3 keV
  'vfine'  : causal max_boost 1e-4, hmax 0.005 cm, first 20 events (same masses, 3 keV)
  'rnd<j>' : production settings with the initial 3-momenta perturbed by a relative 1e-14 (seeded, j = 1..4), first 30
             events at 500 GeV, Lambda = 1 and 3 keV -> direct measure of round-off (precision-floor) noise in Delta_s(f)
  'conf'   : conformal solver N = 4096 (independent arithmetic and discretisation), first 12 events, 500 GeV, 3 keV,
             10 barrel radii without z cut; with a causal fine run on the same hit definition ('cfine')
FU2 (vacuum constant): M2a runs at gamma* = 1.01 and 1.02 (M2_single.job_a; files added to results/raw/M2).
Outputs: data/stage1_numerics/FU/<tag>.npz (Delta_s per f, status, gamma*), one per job, skipped if present.
Run: pixi run python analytic/numerics/FU_runs.py
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'FU'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112
FR = [1.0, 0.5, 0.25, 0.05]


def job(args):
    m, lam, iev, p1, p2, setting = args
    tag = f"m{m:g}_L{lam:g}_e{iev:03d}_{setting}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 0.0
    from nm_kernel import run
    from T3_propagator import plane_fit
    import nm_conformal as NC
    t0 = time.time()
    p1 = np.array(p1, float); p2 = np.array(p2, float)
    if setting.startswith('rnd'):
        rng = np.random.default_rng(1000 * int(setting[3:]) + iev)
        p1 = p1 * (1 + 1e-14 * rng.standard_normal(3)); p2 = p2 * (1 + 1e-14 * rng.standard_normal(3))
    ds = []; st = []
    for f in FR:
        if setting == 'conf':
            r = NC.run(p1, p2, m, lam, Bz=B0 * f, N=4096)
            H = r['hits']; s = r['status']
        else:
            if setting in ('fine', 'cfine'):
                mb, hm = 1e-3, 0.02
            elif setting == 'vfine':
                mb, hm = 1e-4, 0.005
            else:
                mb, hm = 1e-2, 0.2
            kw = dict(rec_radii=NC.RADII, rec_zmax=np.full(10, 1e9)) if setting == 'cfine' else {}
            r = run(p1, p2, m, lam, B0=B0 * f, max_boost=mb, hmax_trk=hm, max_steps=4_000_000_000, **kw)
            H = r['hits']; H = H[H[:, 1] < 10]; s = r['status']
        ds.append(plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan); st.append(s)
    np.savez(fn, ds=np.array(ds), fr=np.array(FR), status=np.array(st), cpu=time.time() - t0)
    return tag, time.time() - t0


if __name__ == '__main__':
    from T3_propagator import sample_events
    import M2_single as MS
    tasks = []
    evs = {m: sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0) for m in (500.0, 1000.0)}
    for m in (500.0, 1000.0):
        for i, (p1, p2, info) in enumerate(evs[m]):
            tasks.append((m, 3.0, i, p1, p2, 'fine'))
            if i < 20:
                tasks.append((m, 3.0, i, p1, p2, 'vfine'))
    for i, (p1, p2, info) in enumerate(evs[500.0][:30]):
        for lam in (1.0, 3.0):
            for j in range(1, 5):
                tasks.append((500.0, lam, i, p1, p2, f'rnd{j}'))
            tasks.append((500.0, lam, i, p1, p2, 'rnd0'))      # unperturbed production reference (same code path)
        if i < 12:
            tasks.append((500.0, 3.0, i, p1, p2, 'conf'))
            tasks.append((500.0, 3.0, i, p1, p2, 'cfine'))
    m2a = []
    for gs in (1.01, 1.02):
        for k, dl in enumerate(MS.DGRID):
            m2a += [(gs, dl, 'causal', 1e-2, MS.LAM, MS.M), (gs, dl, 'conf', 256, MS.LAM, MS.M)]
            if k % 2 == 0:
                m2a += [(gs, dl, 'causal', 1e-3, MS.LAM, MS.M), (gs, dl, 'conf', 2048, MS.LAM, MS.M)]
    tasks.sort(key=lambda a: -(10 if a[5] == 'vfine' else 3 if a[5] in ('conf',) else 1))
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        futs = [ex.submit(MS.job_a, a) for a in m2a] + [ex.submit(job, t) for t in tasks]
        for i, fu in enumerate(futs):
            r = fu.result()
            if isinstance(r[1], float):
                cpu += r[1]
            if i % 100 == 0:
                print(f"[{i+1}/{len(futs)}] {r[0]} (wall {time.time()-tic:.0f}s, cpu {cpu:.0f}s)", flush=True)
    print(f"FU runs done: {len(futs)} jobs, wall {time.time()-tic:.0f} s, cpu {cpu:.0f} s", flush=True)
