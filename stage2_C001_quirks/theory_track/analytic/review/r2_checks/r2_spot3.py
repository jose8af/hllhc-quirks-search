"""r2_spot3.py -- S1-R2, parts O and C of r2_spot2.py (part S output: r2_spot2_partS_out.txt; r2_spot2.py crashed at the
import of r1_lab_c after part S had printed, so parts O/C are re-run here alone).
Part O: round-1 reviewer's 16 events (R1.make_event, rng 2026, m = 500 GeV, gamma* = 1.28, pT = 300 GeV), 1 keV, B0 and B0/4,
  E2's causal kernel (max_boost 1e-3, hmax 0.02, the 10 radii without z cut = conformal hit set) vs the conformal c_4 of
  r1_lab_c_out.txt (N = 4096).  k_B = 8.4-12 events were +0.016..+0.035 above c_E1 with the conformal solver.
Part C: C_meas = 1/c_4 - ln(1/eps_B) from both solvers vs E1's C_ev on the same events.
Run (from TT): pixi run python analytic/review/r2_checks/r2_spot3.py > analytic/review/r2_checks/r2_spot3_out.txt
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (os.path.join(TT, 'code'), os.path.join(TT, 'analytic', 'numerics'), os.path.join(TT, 'analytic', 'review', 'r1_checks')):
    sys.path.insert(0, p)
import R1_conformal_ng as R1          # noqa: E402
import r1_lab_c as L                  # noqa: E402
from nm_kernel import run             # noqa: E402
from nm_conformal import RADII        # noqa: E402
from T3_propagator import plane_fit   # noqa: E402
B0 = 3.8112

r1c4 = {}
for line in open(os.path.join(TT, 'analytic', 'review', 'r1_checks', 'r1_lab_c_out.txt')):
    s = line.split()
    if len(s) > 11 and s[0].isdigit() and s[5] == '4096':
        r1c4[int(s[0])] = float(s[11])
rng = np.random.default_rng(2026)
epsB = 2.99792458e-3 * B0 / R1.sigma_keV(1.0); Lb = np.log(1 / epsB)
print('# Part O/C: ev  k_B  sin_a  c_E1  | c4_conf(r1)  c4_caus | conf-E1  caus-E1  conf-caus | C_E1  C_conf  C_caus')
rows = []
for i in range(16):
    p1, p2 = R1.make_event(rng, 500.0)
    cE = L.c_E1(p1, p2)[0]; sa, kB, gb = L.geometry(p1, p2)
    d = []
    for f in (1.0, 0.25):
        r = run(p1, p2, 500.0, 1.0, B0=B0 * f, max_boost=1e-3, hmax_trk=0.02, rec_radii=RADII, rec_zmax=np.full(10, 1e9))
        H = r['hits']; H = H[H[:, 1] < 10]; d.append(plane_fit(H[:, 3:6])[0])
    c4 = (4 * d[1] / d[0] - 1) / np.log(4); cc = r1c4[i]
    rows.append((kB, cE, cc, c4))
    print(f'{i:3d} {kB:6.2f} {sa:.3f} {cE:.4f} | {cc:.4f}  {c4:.4f} | {cc - cE:+.4f}  {c4 - cE:+.4f}  {cc - c4:+.4f} | '
          f'{1 / cE - Lb:+.3f} {1 / cc - Lb:+.3f} {1 / c4 - Lb:+.3f}', flush=True)
R = np.array(rows)
for lab, s in (('k_B < 6.5', R[:, 0] < 6.5), ('k_B >= 6.5', R[:, 0] >= 6.5), ('all', R[:, 0] > 0)):
    print(f'# {lab:10s} n={s.sum():2d}: median conf-E1 {np.median(R[s, 2] - R[s, 1]):+.4f}, caus-E1 {np.median(R[s, 3] - R[s, 1]):+.4f}, '
          f'conf-caus {np.median(R[s, 2] - R[s, 3]):+.4f};  median C: E1 {np.median(1 / R[s, 1] - Lb):+.3f}, conf {np.median(1 / R[s, 2] - Lb):+.3f}, '
          f'caus {np.median(1 / R[s, 3] - Lb):+.3f}')
