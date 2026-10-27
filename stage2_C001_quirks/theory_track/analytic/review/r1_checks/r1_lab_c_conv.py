"""r1_lab_c_conv.py -- S1-R1: N-convergence (4096 vs 16384) of the large-kB outlier events 0, 3, 4 (and control 2) of r1_lab_c.py.
Run: pixi run python analytic/review/r1_checks/r1_lab_c_conv.py > analytic/review/r1_checks/r1_lab_c_conv_out.txt"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_lab_c as L  # noqa: E402

rng = np.random.default_rng(2026)
ev = [L.R1.make_event(rng, L.M) for _ in range(16)]
for ie in (0, 2, 3, 4):
    p1, p2 = ev[ie]
    cE, gs, eps = L.c_E1(p1, p2)
    for N in (4096, 16384):
        d0, _ = L.ds(p1, p2, L.B0, N); d4, _ = L.ds(p1, p2, L.B0 / 4, N)
        c4 = (4 * d4 / d0 - 1) / np.log(4)
        print(f'ev {ie}: N={N:5d}  Ds(B0)={d0 * 1e4:.4f} um  Ds(B0/4)={d4 * 1e4:.4f} um  c4={c4:.4f}  c_E1={cE:.4f}  diff={c4 - cE:+.4f}', flush=True)
