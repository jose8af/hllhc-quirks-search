"""T3_test_propagator.py -- validation of the numba propagator T3_propagator.propagate.

Checks
  1. Vacuum (no B, no material): lab positions at several times vs T2 ExactPair (exact boosted yo-yo).
  2. Vacuum: recorded hit positions (cubic-Hermite crossing interpolation) vs ExactPair.
  3. Pair at rest, uniform 3.8 T: CM-frame energy E1 + E2 + sigma|x1-x2| (1-D yo-yo; exact invariant).
  4. Uniform 3.8 T, no material: final positions and plane thickness vs T2 LabStraightString (DOP853, rtol 1e-11).
  5. Timing: wall-clock per event with full material at Lambda = 1, 10, 30 keV.
Run: pixi run python code/T3_test_propagator.py
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import (run_pair, plane_fit, REC_RADII, sample_events, propagate, phase2_tracker,
                           cms_outer_regions, MAT, DUMMY_GRID)
from T2_propagator import ExactPair, LabStraightString, sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T

ok_all = True


def check(name, ok, info=''):
    global ok_all
    ok_all &= bool(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {info}", flush=True)


def final_state(p1, p2, m, lam, B, T, rtol=1e-10):
    y0 = np.r_[0, 0, 0, p1, 0, 0, 0, p2].astype(float)
    out = propagate(y0, m, m, sigma_from_lambda_keV(lam), 1.0, -1.0, 0, B, *DUMMY_GRID, phase2_tracker(),
                    cms_outer_regions(), MAT, REC_RADII, np.full(len(REC_RADII), 1e9), False, False, False,
                    float(T), 1e12, 1e12, 0.0, rtol, 1e-12, 1e-10, 0.5, 2.0, 1, 10, 10 ** 9)
    return out[2], out[6]


m = 500.0
p1 = np.array([200.0, 300.0, 30.0]); p2 = np.array([-100.0, 280.0, -20.0])

# 1. vacuum positions vs exact
for lam in (0.3, 1.0, 3.0, 10.0):
    ex = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam))
    err = 0.0; ns = 0
    for T in (3.0, 37.0, 151.0, 400.0):
        y, ns = final_state(p1, p2, m, lam, 0.0, T)
        X1, X2 = ex.lab_positions([T])
        err = max(err, np.linalg.norm(y[0:3] - X1[0]), np.linalg.norm(y[6:9] - X2[0]))
    check(f'vacuum positions vs ExactPair, Lambda={lam} keV', err < (1e-6 if lam <= 3 else 3e-4),
          f'max|dx| = {err*1e4:.2g} um, = {err/ex.lmax:.1e} l_max (t up to 400 cm, {ns} steps)')

# 2. vacuum hits
for lam in (1.0, 3.0):
    r = run_pair(p1, p2, m, lam, B0=0.0, material=False, rtol=1e-10)
    ex = ExactPair(p1, p2, m, m, sigma_from_lambda_keV(lam))
    H = r['hits']; err = 0.0
    for k in range(len(H)):
        i = int(H[k, 0]); X1, X2 = ex.lab_positions([H[k, 2]])
        err = max(err, np.linalg.norm((X1, X2)[i][0] - H[k, 3:6]))
    check(f'vacuum hit positions vs ExactPair, Lambda={lam} keV', err < 1e-4, f'max|dx| = {err*1e4:.2g} um over {len(H)} hits')

# 3. pair at rest (1-D yo-yo) in B: invariant energy
for lam in (0.3, 1.0, 10.0):
    sig = sigma_from_lambda_keV(lam)
    q = np.array([150.0, 200.0, 100.0])
    y, ns = final_state(q, -q, m, lam, 3.8112, 500.0)
    E0 = 2 * np.hypot(m, np.linalg.norm(q))
    E = np.hypot(m, np.linalg.norm(y[3:6])) + np.hypot(m, np.linalg.norm(y[9:12])) + sig * np.linalg.norm(y[0:3] - y[6:9])
    check(f'energy invariant, pair at rest in 3.8 T, Lambda={lam} keV', abs(E / E0 - 1) < 1e-7,
          f'|dE/E| = {abs(E/E0-1):.1e} after 500 cm ({ns} steps)')

# 4. vs T2 LabStraightString in uniform B
Bv = np.array([0, 0, 3.8112]); Q = (1.0, -1.0)
for lam in (0.6, 1.0, 2.0):
    sig = sigma_from_lambda_keV(lam)

    def fext(i, x, p, t):
        E = np.sqrt(m * m + p @ p)
        return Q[i] * EB_GEV_PER_CM_PER_T * np.cross(p / E, Bv)
    T = 300.0
    tic = time.time(); sol = LabStraightString(m, m, sig, fext=fext, rtol=1e-11).run(p1, p2, T); t2 = time.time() - tic
    y, ns = final_state(p1, p2, m, lam, 3.8112, T, rtol=1e-11)
    dx = max(np.linalg.norm(y[0:3] - sol['y'][-1, 0:3]), np.linalg.norm(y[6:9] - sol['y'][-1, 6:9]))
    r = run_pair(p1, p2, m, lam, B0=3.8112, material=False, rtol=1e-11, r_exit=1e9, z_exit=1e9, t_end=1500.0)
    H = r['hits'][r['hits'][:, 1] < 10]
    d3, _ = plane_fit(H[:, 3:6])
    # at 2 keV T2 differs by ~2 um after ~170 crossings: T2's fixed 'free nudge' step after each crossing
    # event (h = 1e-9 t) is not error-controlled; T3 is converged in rtol to < 1e-3 um (see report Sec.3.1)
    check(f'uniform B: T3 vs T2 LabStraightString final positions, Lambda={lam} keV', dx < (1e-5 if lam < 2 else 5e-4),
          f'max|dx| at t = 300 cm: {dx*1e4:.2g} um (T2 {t2:.1f} s); thickness of T3 hits {d3*1e4:.2f} um')

# 5. timing with full material
rng = np.random.default_rng(3)
ev = sample_events(500, 1, rng=rng, eta_max=1.0)
for lam in (1.0, 10.0, 30.0):
    tic = time.time()
    r = run_pair(ev[0][0], ev[0][1], 500.0, lam)
    print(f'  timing Lambda={lam}: {time.time()-tic:.2f} s, nsteps={r["nsteps"]}, hits={len(r["hits"])}, '
          f'E lost in tracker = {r["eacc"].sum()*1e3:.0f} MeV', flush=True)
print('ALL PASS' if ok_all else 'SOME FAILURES')
