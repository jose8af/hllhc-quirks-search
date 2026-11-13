"""c08_K_fit.py -- E1: smooth fit of the exact-NG constant K(gamma*) (NEAR_MISS_IMPULSE.md §4.2).
Data: c03_causal_E_out_mb1e-4.txt (max_boost 1e-4, mean over eps = 1e-5, 1e-4), plus the analytic NR limit
K(1) = 3 ln 2 - 2 (c05).  Fit K = K_NR + a x + b x^2 with x = ln(gamma*), K_NR fixed.  Also compares with the
quasi-static (QS) and Kang-Luty (KL) straight-string constants of c04.
Run: pixi run python analytic/checks/c08_K_fit.py > analytic/checks/c08_K_fit_out.txt
"""
import numpy as np
KNR = 3 * np.log(2) - 2
g = np.array([1.05, 1.28, 1.6, 2.0, 3.0])
K = np.array([0.05625, -0.0490, -0.17535, -0.3095, -0.5688])
x = np.log(g)
A = np.vstack([x, x**2]).T
coef, *_ = np.linalg.lstsq(A, K - KNR, rcond=None)
print(f'K_NR = {KNR:.6f}; fit K = K_NR + ({coef[0]:+.4f}) ln g + ({coef[1]:+.4f}) ln^2 g')
for gi, Ki in zip(g, K):
    xf = np.log(gi)
    print(f'  gamma*={gi}: K_num={Ki:+.4f}  K_fit={KNR + coef[0]*xf + coef[1]*xf**2:+.4f}')
be = np.sqrt(g**2 - 1) / g
print('compare: K_num - K_NR vs ln(beta*/artanh beta*):', np.round(K - KNR, 4), np.round(np.log(be / np.arctanh(be)), 4))
