"""S_msscale.py -- synthesis check: does the multiple-scattering plane thickness of the causal string scale as
sqrt(x/X0)?  (T3 report Sec.10 G-T3-1 assumes "x1.4 on Delta_s for x2 material (sqrt scaling, untested
numerically)"; S_spotchecks.py section H found a median per-event ratio of 0.83 with independent random streams.)

Method: T3_causal.run_causal, B = 0, MS only (no mean dE/dx, no straggling: the random stream is then used only by MS,
so the same seed gives the same normal deviates and theta0 scales exactly as sqrt(scale) per kick), material scale
s in {0.25, 0.5, 1, 2, 4} on T3_propagator.phase2_tracker; LO DY+ISR events from the T2 cache (pT > 200 GeV,
|eta| < 1).  Prints median and geometric-mean Delta_s per scale and the fitted exponent of Delta_s vs s.
Also repeats s = 1, 2 with B = 3.8112 T and full material (dE/dx + straggling + MS) to compare the realistic case.
Run (from theory_track/): pixi run python code/S_msscale.py [nev] [m] [lam]   (default 40 events, 500 GeV, 3 keV)
"""
import os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import sample_events, phase2_tracker  # noqa: E402

SCALES = [0.25, 0.5, 1.0, 2.0, 4.0]


def job(a):
    from T3_causal import run_causal
    from T3_ms_thickness import observables
    m, lam, p1, p2, s, seed, mode = a
    if mode == 'ms':
        r = run_causal(p1, p2, m, lam, B0=0.0, eloss=False, strag=False, ms=True, slabs=phase2_tracker(s), seed=seed)
    else:
        r = run_causal(p1, p2, m, lam, B0=3.8112, slabs=phase2_tracker(s), seed=seed)
    return observables(r['hits'])[0] * 1e4


def main():
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    m = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
    lam = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
    evs = sample_events(m, nev, 'isr', rng=np.random.default_rng(77), eta_max=1.0)
    jobs = [(m, lam, p1, p2, s, 500 + i, 'ms') for i, (p1, p2, _) in enumerate(evs) for s in SCALES]
    jobs += [(m, lam, p1, p2, s, 500 + i, 'full') for i, (p1, p2, _) in enumerate(evs) for s in (1.0, 2.0)]
    with Pool(6) as pool:
        out = pool.map(job, jobs)
    ms = np.array(out[:nev * len(SCALES)]).reshape(nev, len(SCALES))
    full = np.array(out[nev * len(SCALES):]).reshape(nev, 2)
    print(f'm = {m:.0f} GeV, Lambda = {lam:g} keV, {nev} events; B = 0, MS only, same random deviates')
    for j, s in enumerate(SCALES):
        v = ms[:, j]; v = v[np.isfinite(v) & (v > 0)]
        print(f'  scale {s:5.2f}: median {np.median(v):7.2f} um, geo-mean {np.exp(np.mean(np.log(v))):7.2f} um, '
              f'median per-event ratio to s=1: {np.median(ms[:, j] / ms[:, 2]):.3f} (sqrt: {np.sqrt(s):.3f})')
    ok = np.all(np.isfinite(ms) & (ms > 0), axis=1)
    k = np.polyfit(np.log(SCALES), np.mean(np.log(ms[ok]), axis=0), 1)[0]
    print(f'  fitted exponent d ln(Delta_s) / d ln(scale) = {k:.3f} (Highland: ~0.5)')
    print('  B = 3.8 T + full material (dE/dx, straggling, MS), s = 1 vs 2: medians '
          f'{np.nanmedian(full[:, 0]):.2f} / {np.nanmedian(full[:, 1]):.2f} um, '
          f'median per-event ratio {np.nanmedian(full[:, 1] / full[:, 0]):.3f}')


if __name__ == '__main__':
    main()
