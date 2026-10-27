"""r1_conf_cm_g2.py -- S1-R1: same as r1_conf_cm.py at gamma* = 2 (K and the B* effect vs eps), offset-averaged (fb = 0.03).
Run: pixi run python analytic/review/r1_checks/r1_conf_cm_g2.py > analytic/review/r1_checks/r1_conf_cm_g2_out.txt"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r1_conf_cm import pm_run  # noqa: E402

g = 2.0
bb = np.sqrt(1 - 1 / g ** 2); r_ = g * bb
bpred = 2 * (g - np.arcsinh(r_) / r_); G = bpred / (r_ * np.arctanh(bb))
lr = np.log((g - 1) / (g - np.arcsinh(r_) / r_))
print(f'# gamma* = 2: E1 b_odd/(eps l0) = {bpred:.5f}, G = {G:.5f}, E1 K(2) = -0.309 (c03, mb 1e-4)')
base = {}
for eps in (1e-5, 1e-4):
    for N in (1024, 4096):
        res, st = pm_run(g, eps, N, 0.03)
        if res is None:
            print(f'eps={eps:.0e} N={N}: status {st}'); continue
        bn, eta, out = res
        K = eta / (eps * G) - (np.log(1 / eps) + lr)
        base[(eps, N)] = eta
        print(f'eps={eps:.0e} N={N}: b_1/(eps l0) = {bn:.5f} (ratio {bn / bpred:.5f}), eta/eps = {eta / eps:.5f}, K = {K:+.4f}', flush=True)
print('# B* along z, kB = q|B*|/(sigma eps): d eta/eta (N = 1024)')
for eps in (1e-5, 1e-4):
    for kB in (2.0, 4.0, 8.0):
        res, st = pm_run(g, eps, 1024, 0.03, kB=kB, Bdir=(0, 0, 1))
        if res is None or (eps, 1024) not in base:
            print(f'eps={eps:.0e} kB={kB}: status {st}'); continue
        print(f'eps={eps:.0e} kB={kB:4.1f}: d eta/eta = {res[1] / base[(eps, 1024)] - 1:+.4e}', flush=True)
