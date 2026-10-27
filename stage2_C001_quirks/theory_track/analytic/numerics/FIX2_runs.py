"""FIX2_runs.py -- E2 fix pass 2 (review S1-R2, N1/N2): decisive runs.  Earlier results are not modified.

Events: M3 events (T2 cache, seed 777 + m, |eta| < 1, 120-event draw), B scans f = B/B0.  Causal kernel nm_kernel, max_boost 1e-3,
hmax 0.02 cm (x s), string-queue cap 2^21.
 N1 (a)+(b): Lambda = 3 keV, m = 500/1000 GeV, events 0-39, f in {1, 1/2, 1/4, 1/20}:
   'on_s<s>'  : full lab field (B* on), detector radii, z-limits, exits and hmax scaled by s in {1/9, 1/3}  (s = 1 is FU 'fine')
   'off_s<s>' : B* switched off: uniform lab fields E_lab = gamma^2 beta x fB, B_lab = gamma^2[beta(beta.fB) - beta^2 fB]
                (nm_bstar.py) -> pure E* = gamma beta x fB in the pair (P0) frame; s in {1/9, 1/3, 1}
   Scale invariance: (1 keV, B0/9, R) == (3 keV, B0, R/9) exactly, so s = 1/9 is R2's 1-keV same-window test (9x fewer periods),
   s = 1/3 has 3x fewer periods; per-period physics (eps_perp, b/l0, gamma*, k_B, alpha) is identical.
   'eperp_s<s>': B* off AND E*_par off (pair frame field = E*_perp only, nm_bstar.eperp_only_fields), s in {1/9, 1}.
 N2: at the nominal field, f in {1, 1/2} (c at B0 from k_f = 2): Lambda = 5, 7, 10, 13 keV, 500 GeV events 0-29 (13 keV: 0-19);
   Lambda = 5, 7, 10 keV, 1 TeV events 0-19.  'b0v': max_boost 1e-4, hmax 0.005, Lambda = 7 keV, 500 GeV, events 0-4.
Outputs: data/stage1_numerics/FIX2/<tag>.npz (Delta_s per f, status), one per job, skipped if present.
Run: pixi run python analytic/numerics/FIX2_runs.py
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, '..', '..', 'data', 'stage1_numerics', 'FIX2'); os.makedirs(RAW, exist_ok=True)
B0 = 3.8112


def job(args):
    kind, m, lam, iev, s, bstar, frs, mb, hm, p1, p2 = args
    tag = f"{kind}_m{m:g}_L{lam:g}_e{iev:03d}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 0.0
    from nm_kernel import run
    from nm_bstar import bstar_off_fields, eperp_only_fields
    from T3_propagator import plane_fit, REC_RADII, REC_ZMAX
    t0 = time.time()
    ds, st = [], []
    for f in frs:
        geo = dict(rec_radii=REC_RADII * s, rec_zmax=REC_ZMAX * s, r_exit=118.0 * s, z_exit=290.0 * s,
                   hmax_trk=hm * s, hmax_out=2.0 * s)
        if bstar == 'eperp':
            from T2_propagator import ExactPair, sigma_from_lambda_keV
            n0 = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam)).n
            El, Bl = eperp_only_fields(p1, p2, m, n0, (0.0, 0.0, B0 * f))
            r = run(p1, p2, m, lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, max_boost=mb, max_steps=8_000_000_000,
                    qcap=1 << 21, **geo)
        elif bstar:
            r = run(p1, p2, m, lam, B0=B0 * f, max_boost=mb, max_steps=8_000_000_000, qcap=1 << 21, **geo)
        else:
            El, Bl = bstar_off_fields(p1, p2, m, (0.0, 0.0, B0 * f))
            r = run(p1, p2, m, lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, max_boost=mb, max_steps=8_000_000_000,
                    qcap=1 << 21, **geo)
        H = r['hits']; H = H[H[:, 1] < 10]
        ds.append(plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan); st.append(r['status'])
    np.savez(fn, ds=np.array(ds), fr=np.array(frs), status=np.array(st), s=s, bstar=bstar, cpu=time.time() - t0)
    return tag, time.time() - t0


if __name__ == '__main__':
    from T3_propagator import sample_events
    FR = [1.0, 0.5, 0.25, 0.05]
    tasks = []
    evs = {m: sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0) for m in (500.0, 1000.0)}
    for m in (500.0, 1000.0):
        for i in range(40):
            p1, p2, _ = evs[m][i]
            for s, sname in ((1 / 9, '9'), (1 / 3, '3')):
                tasks.append((f'on_s{sname}', m, 3.0, i, s, True, FR, 1e-3, 0.02, p1, p2))
            for s, sname in ((1 / 9, '9'), (1 / 3, '3'), (1.0, '1')):
                tasks.append((f'off_s{sname}', m, 3.0, i, s, False, FR, 1e-3, 0.02, p1, p2))
            for s, sname in ((1 / 9, '9'), (1.0, '1')):
                tasks.append((f'eperp_s{sname}', m, 3.0, i, s, 'eperp', FR, 1e-3, 0.02, p1, p2))
    for m, lams, nev in ((500.0, (5.0, 7.0, 10.0, 13.0), 30), (1000.0, (5.0, 7.0, 10.0), 20)):
        for lam in lams:
            for i in range(20 if (lam == 13.0) else nev):
                p1, p2, _ = evs[m][i]
                tasks.append(('b0', m, lam, i, 1.0, True, [1.0, 0.5], 1e-3, 0.02, p1, p2))
    for i in range(5):
        p1, p2, _ = evs[500.0][i]
        tasks.append(('b0v', 500.0, 7.0, i, 1.0, True, [1.0, 0.5], 1e-4, 0.005, p1, p2))
    tasks.sort(key=lambda a: -(a[2] ** 2 * (10 if a[7] < 1e-3 else 1) * (0.2 if a[0].startswith(('on', 'off')) else 1)))
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(7, mp_context=mp.get_context('spawn')) as ex:
        for i, (tag, dt) in enumerate(ex.map(job, tasks, chunksize=1)):
            cpu += dt
            if i % 50 == 0 or dt > 300:
                print(f"[{i+1}/{len(tasks)}] {tag} {dt:.0f}s (wall {time.time()-tic:.0f}s, cpu {cpu:.0f}s)", flush=True)
    print(f"FIX2 runs done: {len(tasks)} jobs, wall {time.time()-tic:.0f} s, cpu {cpu:.0f} s", flush=True)
