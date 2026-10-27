"""T3_precession.py -- does the oscillation plane precess in the 3.8 T field, and can the rate measure Lambda? (Q2)

Causal NG propagator (T3_causal.run_causal), m_Q in {500, 1000} GeV, Lambda in {0.6, 1, 2, 3, 5} keV,
LO DY+ISR pairs (pT(QQ) > 200 GeV, |eta| < 1), same events in configurations
   B   : uniform 3.8112 T, no material;   B+M : 3.8 T + full Phase-2 material (MS, dE/dx, straggling).
Observables (all from barrel hits; planes through the origin):
   theta_io : angle between the normal of the plane fitted to the inner hits (IT1-4 + PS1, r <= 25 cm) and the
              normal fitted to the outer hits (PS2..2S3)  -> a "precession over the tracker" observable;
   slope    : linear trend of the signed out-of-plane residual vs r (plane fitted to all hits), in rad;
   Delta_s  : total thickness.
Compare with Knapen's torque estimate Delta phi ~ 1e-5 (v_cm^2/v^2)(B/2T)(2 keV/Lambda)^2 [1708.02243 Eq.8-9].
Run: pixi run python code/T3_precession.py [nev]   (default 24; ~15-30 min on 8 cores)
"""
import os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import plane_fit, sample_events
from T3_causal import run_causal

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
LAMS = [0.6, 1.0, 2.0, 3.0, 5.0]


def obs(hits):
    H = hits[hits[:, 1] < 10]
    if len(H) < 8:
        return [np.nan] * 3
    inn = H[H[:, 1] <= 4]; out = H[H[:, 1] >= 5]
    if len(inn) < 3 or len(out) < 3:
        return [np.nan] * 3
    _, n1 = plane_fit(inn[:, 3:6]); _, n2 = plane_fit(out[:, 3:6])
    th = np.arccos(min(1.0, abs(n1 @ n2)))
    d, n = plane_fit(H[:, 3:6])
    r = np.hypot(H[:, 3], H[:, 4]); res = H[:, 3:6] @ n
    slope = np.polyfit(r, res, 1)[0]
    return [th, abs(slope), d]


def job(a):
    m, lam, k, p1, p2 = a
    o = []
    for cfg in (dict(material=False), dict()):
        r = run_causal(p1, p2, m, lam, seed=500 + k, **cfg)
        o += obs(r['hits'])
    return (m, lam, k, o)


if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    rng = np.random.default_rng(99)
    tasks = []
    for m in (500.0, 1000.0):
        ev = sample_events(m, nev, rng=rng, eta_max=1.0)
        for lam in LAMS:
            for k in range(nev):
                tasks.append((m, lam, k, ev[k][0], ev[k][1]))
    tic = time.time()
    with Pool(8) as pool:
        res = pool.map(job, tasks, chunksize=2)
    print(f'{len(tasks)} jobs in {time.time()-tic:.0f} s')
    rows = np.array([[m, lam, k] + o for (m, lam, k, o) in res])
    np.save(os.path.join(FIG, 'T3_precession.npy'), rows)
    print('| m_Q | Lambda | theta_io B [urad] (16/50/84) | theta_io B+M [urad] | |slope| B [urad] | |slope| B+M [urad] | Knapen Eq.9 x (v_cm/v)^2 [urad] |')
    print('|---|---|---|---|---|---|---|')
    for m in (500.0, 1000.0):
        for lam in LAMS:
            s = (rows[:, 0] == m) & (rows[:, 1] == lam)
            q = lambda c: np.nanpercentile(rows[s, c] * 1e6, [16, 50, 84])
            a, b, c, d = q(3), q(6), q(4), q(7)
            kn = 1e-5 * (3.8112 / 2) * (2 / lam) ** 2 * 1e6
            print(f'| {m:.0f} | {lam} | {a[1]:.3g} ({a[0]:.2g}-{a[2]:.2g}) | {b[1]:.3g} ({b[0]:.2g}-{b[2]:.2g}) | {c[1]:.3g} | {d[1]:.3g} | {kn:.3g} |')
