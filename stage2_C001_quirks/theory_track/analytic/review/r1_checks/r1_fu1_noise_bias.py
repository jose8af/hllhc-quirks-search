"""r1_fu1_noise_bias.py -- S1-R1 critical reviewer, independent re-analysis of E2's FU1 raw files (3 keV c).

Questions:
 (1) Can the measured round-off noise (5 replicas, 1e-14 perturbation, production settings) produce the k-dependent upward
     bias of c at 3 keV (fine: c_k - c_E1 = +0.002/+0.0055/+0.011 at k = 2/4/20)?  The thickness is sqrt(min eigenvalue),
     so mean-zero noise enters in quadrature: bias(Delta_s)/Delta_s ~ (rel. noise)^2 / 2 (second order).  We compute the
     implied bias of c_k from the replica spread, event by event, and compare with the observed excess.
 (2) Is the 1e-4 ("vfine") convergence subsample representative?  Theory predicts c_k independent of k (R exactly linear in
     ln k).  Compare the k-growth c_20 - c_2 and c_4 - c_2 (fine, 1e-3) on vfine survivors vs non-survivors.
Inputs: data/stage1_numerics/FU/*.npz (E2 raw; ds at f = 1, 1/2, 1/4, 1/20; status).
Run: pixi run python analytic/review/r1_checks/r1_fu1_noise_bias.py > analytic/review/r1_checks/r1_fu1_noise_bias_out.txt
"""
import glob, os
import numpy as np

TT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = os.path.join(TT, 'data', 'stage1_numerics', 'FU')
K = np.array([2.0, 4.0, 20.0])


def load(m, lam, setting, require_ok=True):
    out = {}
    for f in glob.glob(os.path.join(D, f"m{m:g}_L{lam:g}_e*_{setting}.npz")):
        z = np.load(f)
        ok = np.all(z['status'] == 1)
        if ok or not require_ok:
            out[int(f.split('_e')[-1][:3])] = (z['ds'], ok)
    return out


def ck(ds):
    return (ds[1:] / K[None, :][0] ** -1 / ds[0] - 1) / np.log(K) if False else \
        np.array([(ds[i + 1] * K[i] / ds[0] - 1) / np.log(K[i]) for i in range(3)])


def boot_med(x, n=2000, rng=np.random.default_rng(1)):
    x = np.asarray(x); x = x[np.isfinite(x)]
    if len(x) == 0:
        return np.nan, np.nan, 0
    b = [np.median(rng.choice(x, len(x))) for _ in range(n)]
    return np.median(x), np.std(b), len(x)


print('=== (1) round-off replicas: implied quadrature bias on c_k (500 GeV) ===')
for lam in (1.0, 3.0):
    base = load(500.0, lam, 'rnd0')
    reps = [load(500.0, lam, f'rnd{j}') for j in range(1, 5)]
    rel_sd, cb, cspread = [], [], []
    for i, (d0, _) in base.items():
        if not all(i in r for r in reps):
            continue
        A = np.array([d0] + [r[i][0] for r in reps])           # 5 x 4
        mu = A.mean(0); sd = A.std(0, ddof=1)
        rs = sd / mu
        rel_sd.append(rs)
        # quadrature model: Delta_s_obs^2 = Delta_s^2 + n^2, replica sd of Delta_s ~ n/sqrt(2) at most -> n/Delta_s <~ sqrt(2) rs
        # => relative bias b(f) = (n/Delta_s)^2 / 2 <~ rs^2.  Generous upper bound: b(f) = rs(f)^2 (times 1, not 1/2).
        bias = rs ** 2
        R = mu[1:] * K / mu[0]
        cb.append((R * (1 + bias[1:]) / (1 + bias[0]) - R) / np.log(K))
        cspread.append(np.std([ck(a) for a in A], axis=0, ddof=1))
    rel_sd = np.array(rel_sd); cb = np.array(cb)
    print(f'Lambda = {lam:g} keV, n = {len(rel_sd)} events')
    print('  replica rel. sd of Delta_s, median / mean / p90 at f=1,1/2,1/4,1/20:')
    print('   ', np.round(np.median(rel_sd, 0), 5), np.round(rel_sd.mean(0), 5), np.round(np.quantile(rel_sd, 0.9, 0), 5))
    print('  implied upward bias of c_k from noise (upper bound b = rs^2), k = 2,4,20: median',
          np.round(np.median(cb, 0), 6), ' mean', np.round(cb.mean(0), 6), ' max', np.round(cb.max(0), 5))
print('  observed (E2 FU.json, fine 1e-3, 500 GeV, 3 keV): c_k - c_E1 = +0.0021, +0.0055, +0.0113 (k = 2, 4, 20)')
print('  => required bias of Delta_s(1/k) relative: k=4: 0.0055*ln4/1.13 = %.4f ; k=20: 0.0113*ln20/1.28 = %.4f'
      % (0.0055 * np.log(4) / 1.13, 0.0113 * np.log(20) / 1.28))

print()
print('=== (2) k-dependence of c_k (theory: c_k independent of k) and representativeness of the 1e-4 subsample ===')
for m in (500.0, 1000.0):
    fine = load(m, 3.0, 'fine'); vf_all = load(m, 3.0, 'vfine', require_ok=False)
    surv = sorted(i for i, (_, ok) in vf_all.items() if ok)
    tried = sorted(vf_all)
    nons = [i for i in tried if i not in surv]
    print(f'm = {m:g} GeV: vfine tried {len(tried)} events, all-f status OK: {len(surv)} -> {surv}')
    for lab, idx in (('fine, all events', sorted(fine)), ('fine, vfine survivors', [i for i in surv if i in fine]),
                     ('fine, vfine non-survivors (first 20)', [i for i in nons if i in fine]),
                     ('fine, events >= 20', [i for i in fine if i >= 20])):
        C = np.array([ck(fine[i][0]) for i in idx])
        if len(C) == 0:
            continue
        d42 = boot_med(C[:, 1] - C[:, 0]); d202 = boot_med(C[:, 2] - C[:, 0])
        print(f'  {lab:40s} n={len(C):3d}  median c_k = {np.round(np.median(C, 0), 4)}   '
              f'c4-c2 = {d42[0]:+.4f} +- {d42[1]:.4f}   c20-c2 = {d202[0]:+.4f} +- {d202[1]:.4f}')
    C = np.array([ck(vf_all[i][0]) for i in surv])
    if len(C):
        print(f'  {"vfine (1e-4), survivors":40s} n={len(C):3d}  median c_k = {np.round(np.median(C, 0), 4)}')
    # median Delta_s at f = 1 of survivors vs others (proxy for event type)
    ds1_s = [fine[i][0][0] for i in surv if i in fine]; ds1_n = [fine[i][0][0] for i in fine if i not in surv]
    print(f'  median Delta_s(B0) [cm]: survivors {np.median(ds1_s):.3e}, others {np.median(ds1_n):.3e}')

print()
print('=== (3) same k-growth test at 1 keV, production (converged at 1 keV per E2) ===')
for m in (500.0, 1000.0):
    r = load(m, 1.0, 'rnd0')
    if r:
        C = np.array([ck(v[0]) for v in r.values()])
        print(f'  m={m:g}, 1 keV rnd0 (prod, 30 ev): median c_k = {np.round(np.median(C, 0), 4)}, '
              f'c20-c2 = {boot_med(C[:, 2] - C[:, 0])[0]:+.4f} +- {boot_med(C[:, 2] - C[:, 0])[1]:.4f}')
    r = load(m, 3.0, 'rnd0')
    if r:
        C = np.array([ck(v[0]) for v in r.values()])
        print(f'  m={m:g}, 3 keV rnd0 (prod, 30 ev): median c_k = {np.round(np.median(C, 0), 4)}, '
              f'c20-c2 = {boot_med(C[:, 2] - C[:, 0])[0]:+.4f} +- {boot_med(C[:, 2] - C[:, 0])[1]:.4f}')

print()
print('=== (4) paired fine(1e-3) - vfine(1e-4) per event on survivors, c_k (k = 2, 4, 20) ===')
for m in (500.0, 1000.0):
    fine = load(m, 3.0, 'fine'); vf = load(m, 3.0, 'vfine')
    idx = sorted(i for i in vf if i in fine)
    Dd = np.array([ck(fine[i][0]) - ck(vf[i][0]) for i in idx])
    for i, row in zip(idx, Dd):
        print(f'  m={m:g} ev {i:2d}: fine-vfine = {np.round(row, 4)}   c_vfine = {np.round(ck(vf[i][0]), 4)}')
    print(f'  m={m:g}: median paired diff = {np.round(np.median(Dd, 0), 4)}, rms = {np.round(np.sqrt((Dd ** 2).mean(0)), 4)}')
