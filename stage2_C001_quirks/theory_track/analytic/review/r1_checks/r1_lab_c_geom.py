"""r1_lab_c_geom.py -- S1-R1: geometry (sin alpha, kB = |B*perp|/|E*perp|) of the 16 events of r1_lab_c.py (same seed).
Run: pixi run python analytic/review/r1_checks/r1_lab_c_geom.py > analytic/review/r1_checks/r1_lab_c_geom_out.txt"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r1_lab_c as L  # noqa: E402

rng = np.random.default_rng(2026)
print('# ev  sin(alpha)  kB=|B*perp|/|E*perp|  gamma_cm beta_cm')
for ie in range(16):
    p1, p2 = L.R1.make_event(rng, L.M)
    sa, kB, gb = L.geometry(p1, p2)
    print(f'{ie:3d}   {sa:.3f}     {kB:7.2f}          {gb:.3f}')
