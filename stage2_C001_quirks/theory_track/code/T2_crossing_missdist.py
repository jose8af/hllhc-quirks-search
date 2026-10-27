"""T2_crossing_missdist.py -- distance of closest approach of the two quirks at each crossing, in vacuum
plus a uniform solenoid field (3.8 T), from the exact causal Nambu-Goto propagator (Athena port).
Compared with the confinement length 1/Lambda (hbar c/Lambda = 1.973 Angstrom x keV/Lambda), which
controls whether non-perturbative glueball emission ('epsilon per crossing') [1811.08903 App.B.1;
2404.13814 Eq.4.1] and short-distance Coulomb/annihilation physics can act at a crossing.
Theory track, investigator T2.  Run: pixi run python code/T2_crossing_missdist.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import CausalNullString, ExactPair, interp_track, sigma_from_lambda_keV, HBARC_GEV_CM
from T2_string_methods_B import make_event

Q = (1.0, -1.0)


def miss_distances(m, lam, p1, p2, B, ncross=8, mb=1e-4):
    sig = sigma_from_lambda_keV(lam)
    ex = ExactPair(p1, p2, m, m, sig)
    D, Dt = ex.crossing_spacing_lab()
    traj, _ = CausalNullString(m, sig, charges=Q, Bfield=B, max_boost=mb, first_length=1e-12).run(p1, p2, (ncross + 0.5) * Dt, max_steps=20_000_000)
    out = []
    for k in range(1, ncross + 1):
        # search window around the k-th crossing of the vacuum solution
        tw = np.linspace((k - 0.05) * Dt, (k + 0.05) * Dt, 4001)
        d = np.linalg.norm(interp_track(traj[0], tw) - interp_track(traj[1], tw), axis=1)
        j = np.argmin(d)
        for _ in range(3):      # refine
            lo, hi = tw[max(j - 2, 0)], tw[min(j + 2, len(tw) - 1)]
            tw = np.linspace(lo, hi, 4001)
            d = np.linalg.norm(interp_track(traj[0], tw) - interp_track(traj[1], tw), axis=1)
            j = np.argmin(d)
        out.append(d[j])
    return np.array(out), HBARC_GEV_CM / (lam * 1e-6)


if __name__ == '__main__':
    rng = np.random.default_rng(11)
    m = 500.0
    events = [make_event(rng, m) for _ in range(3)]
    print('| Λ [keV] | B [T] | 1/Λ [Å] | miss distance b at crossings 1..8 (event-median) [Å] | b·Λ (median over crossings and events) |')
    print('|---|---|---|---|---|')
    for lam in (1.0, 3.0, 10.0, 30.0, 100.0):
        for Bz in (0.0, 3.8):
            allb = []
            for (p1, p2, bT) in events:
                b, linv = miss_distances(m, lam, p1, p2, np.array([0, 0, Bz]), ncross=6,
                                         mb=1e-3 if lam <= 3 else 1e-4)
                allb.append(b)
            allb = np.array(allb)
            med = np.median(allb, axis=0)
            print(f'| {lam} | {Bz} | {linv * 1e8:.3g} | ' + ', '.join(f'{x * 1e8:.3g}' for x in med) +
                  f' | {np.median(allb) / linv:.3g} |', flush=True)
