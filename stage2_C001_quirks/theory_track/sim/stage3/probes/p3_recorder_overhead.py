"""p3_recorder_overhead.py -- Stage-3 probe 3: cost of recording more surfaces in T3_causal (unmodified code).

Uses only run_causal's existing rec_radii/rec_zmax arguments: 12 radii (REC_RADII) vs 36 radii (REC_RADII + the stacked
second sensor of the 6 OT layers + 18 dummy cylinders standing in for the ~34 disc checks; the disc test in the proposed
kernel is one z comparison per disc, cheaper than a cylinder test, so this over-estimates the overhead).
Interleaved repeats on the same events, 1 thread.  E 500 GeV, TRGS template, |eta| < 2.5, max_boost 1e-2.
Output: data/sim_stage3/probes/p3_recorder_overhead.json.  Run: nice pixi run python sim/stage3/probes/p3_recorder_overhead.py
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(TT, 'code')); sys.path.insert(0, os.path.join(TT, 'sim', 'scripts'))
import mg_events as mg  # noqa
from T3_causal import run_causal  # noqa
from T3_propagator import REC_RADII, REC_ZMAX  # noqa

extra = np.array([24.9 + 0.16, 37.2 + 0.26, 52.3 + 0.40, 68.8 + 0.18, 86.0 + 0.40, 108.3 + 0.40] +
                 list(np.linspace(4.0, 100.0, 18)))
R36 = np.concatenate([REC_RADII, extra]); Z36 = np.concatenate([REC_ZMAX, np.full(len(extra), 120.0)])
ev = []
for k, e in enumerate(mg.iter_events(500, 'trig', 'F', eta_max=2.5, ptmin=200.0, split='template', unweight=True)):
    ev.append(e)
    if len(ev) == 8:
        break
run_causal(ev[0][0], ev[0][1], 500.0, 1.0)   # compile
res = {}
for lam in (1.0, 3.0):
    for cfg, kw in (('B', dict(material=False)), ('BM', dict(material=True))):
        t12 = t36 = 0.0; h12 = h36 = 0
        for rep in range(2):
            for i, (p1, p2, info) in enumerate(ev):
                t0 = time.perf_counter(); r = run_causal(p1, p2, 500.0, lam, seed=11 + i, **kw); t12 += time.perf_counter() - t0
                h12 += len(r['hits'])
                t0 = time.perf_counter()
                r = run_causal(p1, p2, 500.0, lam, seed=11 + i, rec_radii=R36, rec_zmax=Z36, **kw)
                t36 += time.perf_counter() - t0; h36 += len(r['hits'])
        res[f'{lam:g}keV_{cfg}'] = dict(t12_s=round(t12, 3), t36_s=round(t36, 3), ratio=round(t36 / t12, 3), hits12=h12, hits36=h36)
        print(lam, cfg, res[f'{lam:g}keV_{cfg}'], flush=True)
json.dump(res, open(os.path.join(TT, 'data', 'sim_stage3', 'probes', 'p3_recorder_overhead.json'), 'w'), indent=1)
