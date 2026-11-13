"""F1_smear.py -- fix pass F1 (answers R1-critical B-2): effect of Phase-2 hit resolution and of the missing z
information of 2S modules on the plane-thickness observable, which T3/S quoted at truth-hit level only.

Events: LO DY+ISR pairs from the T2 cache (pT(QQ) > 200 GeV, |eta_pair| < 1) via T3_propagator.sample_events,
propagated with the causal NG propagator T3_causal.run_causal in the realistic configuration (3.8 T + Phase-2
material model of T3 Sec.2: MS + dE/dx + straggling), production settings (max_boost 1e-2, hmax 0.2 cm) as T3.
Hits: crossings of the 10 barrel layers (IT |z| < 20 cm, OT |z| < 120 cm).

Detector model (pitch/sqrt(12), binary readout -> uniform error of width = pitch; UNVERIFIED pitches, TDR not opened):
   IT  (L0-3, r = 3.0-14.6 cm): 25 x 100 um pixels    -> sigma_rphi 7.2 um,  sigma_z 28.9 um
   PS  (L4-6, r = 24.9-52.3 cm): 100 um x 1.5 mm macro-pixel -> sigma_rphi 28.9 um, sigma_z 433 um
   2S  (L7-9, r = 68.8-108.3 cm): 90 um x 5 cm strips, no stereo -> sigma_rphi 26.0 um, sigma_z 14.4 mm
   r is taken as exact (layer radius).

Observables per event:
   ds_true  : T3/S thickness, sqrt(min eigenvalue of sum h h^T/(N-1)), true hits, plane through the origin (truth level)
   ds_naive : the same eigenvalue estimator on smeared hits (what an unweighted fit would report)
   weighted fit: n minimises chi2(n) = sum (n.h_i)^2 / s_i(n)^2, s_i(n)^2 = (n.phihat_i)^2 sr_i^2 + n_z^2 sz_i^2
       (iterated reweighting, 8 iterations); chi2/ndf with ndf = N - 2;
   t_est    : intrinsic thickness estimate, solves sum (n.h_i)^2/(s_i^2 + t^2) = ndf (0 if chi2 <= ndf)
   s_eff    : effective out-of-plane resolution of the event, (mean_i 1/s_i^2)^-1/2, with s_i at the fitted normal
   per-layer-type median s_i (out-of-plane resolution of one hit) for IT/PS/2S.
Efficiencies: truth ds_true < 100 / 30 um vs reconstructed t_est < 100 / 30 um and chi2 p-value > 1 %.

Run (from theory_track/): pixi run python code/F1_smear.py [nev=60] [masses=500,1000] [lams=0.3,0.45,0.6,1,3,10]
Output: printed table (copy in figures/F1_smear_out.txt), per-event array figures/F1_smear.npy.
"""
import os, sys, time
import numpy as np
from multiprocessing import Pool
from scipy.stats import chi2 as chi2dist
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import sample_events, phase2_tracker, plane_fit   # noqa: E402
from T3_causal import run_causal                                     # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
PITCH_RPHI = np.array([25.0] * 4 + [100.0] * 3 + [90.0] * 3) * 1e-4      # cm
PITCH_Z = np.array([100.0] * 4 + [1500.0] * 3 + [50000.0] * 3) * 1e-4    # cm
SR = PITCH_RPHI / np.sqrt(12); SZ = PITCH_Z / np.sqrt(12)


def smear(H, rng):
    x, y, z = H[:, 3], H[:, 4], H[:, 5]
    L = H[:, 1].astype(int)
    r = np.hypot(x, y)
    ph = np.arctan2(y, x)
    drphi = rng.uniform(-0.5, 0.5, len(H)) * PITCH_RPHI[L]
    dz = rng.uniform(-0.5, 0.5, len(H)) * PITCH_Z[L]
    ph2 = ph + drphi / r
    return np.column_stack([r * np.cos(ph2), r * np.sin(ph2), z + dz])


def sig_n(P, L, n):
    ph = np.arctan2(P[:, 1], P[:, 0])
    phihat = np.column_stack([-np.sin(ph), np.cos(ph), np.zeros(len(P))])
    nphi = phihat @ n
    return np.sqrt(nphi ** 2 * SR[L] ** 2 + n[2] ** 2 * SZ[L] ** 2)


def weighted_plane(P, L, n0):
    n = n0.copy()
    for _ in range(8):
        s = sig_n(P, L, n)
        w = 1.0 / s ** 2
        T = (P * w[:, None]).T @ P
        ev, V = np.linalg.eigh(T)
        n = V[:, 0]
    s = sig_n(P, L, n)
    res = P @ n
    return n, res, s


def t_estimate(res, s, ndf):
    f = lambda t: np.sum(res ** 2 / (s ** 2 + t ** 2)) - ndf
    if f(0.0) <= 0:
        return 0.0
    return brentq(f, 0.0, 10.0)


def job(args):
    m, lam, k, p1, p2, seed = args
    r = run_causal(p1, p2, m, lam, slabs=phase2_tracker(), seed=seed)
    H = r['hits']
    H = H[H[:, 1] < 10]
    if len(H) < 5:
        return None
    rng = np.random.default_rng(seed + 7)
    L = H[:, 1].astype(int)
    ds_true, n_true = plane_fit(H[:, 3:6])
    P = smear(H, rng)
    ds_naive, n_naive = plane_fit(P)
    sel = L < 7
    n0 = plane_fit(P[sel])[1] if sel.sum() >= 3 else n_naive
    n, res, s = weighted_plane(P, L, n0)
    ndf = len(P) - 2
    c2 = np.sum(res ** 2 / s ** 2)
    pval = chi2dist.sf(c2, ndf)
    t = t_estimate(res, s, ndf)
    seff = np.mean(1 / s ** 2) ** -0.5
    sIT = np.median(s[L < 4]) if np.any(L < 4) else np.nan
    sPS = np.median(s[(L >= 4) & (L < 7)]) if np.any((L >= 4) & (L < 7)) else np.nan
    s2S = np.median(s[L >= 7]) if np.any(L >= 7) else np.nan
    # truth thickness restricted to IT+PS (the hits that carry out-of-plane information)
    ds_itps = plane_fit(H[sel, 3:6])[0] if sel.sum() >= 4 else np.nan
    return [m, lam, k, len(H), ds_true, ds_naive, c2 / ndf, pval, t, seff, sIT, sPS, s2S, abs(n[2]), ds_itps]


if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    masses = [float(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else ['500', '1000'])]
    lams = [float(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['0.3', '0.45', '0.6', '1', '3', '10'])]
    nproc = int(os.environ.get('F1_NPROC', 4))
    rng = np.random.default_rng(4242)
    tasks = []
    for m in masses:
        ev = sample_events(m, nev, rng=rng, eta_max=1.0)
        for lam in lams:
            for k in range(nev):
                tasks.append((m, lam, k, ev[k][0], ev[k][1], 5000 + k))
    tic = time.time()
    with Pool(nproc) as pool:
        res = pool.map(job, tasks, chunksize=2)
    rows = np.array([r for r in res if r is not None], float)
    np.save(os.path.join(FIG, 'F1_smear.npy'), rows)
    print(f'{len(rows)} events in {time.time()-tic:.0f} s; configuration B+M (3.8 T + material), causal string')
    print('| m_Q | Lambda | N | truth ds med [um] | naive ds on smeared hits med | weighted chi2/ndf med | t_est med [um] |'
          ' s_eff med [um] | s_hit IT/PS/2S med [um] | f(ds_true<100) | f(t_est<100) | f(p>1%) | f(ds_true<30) | f(t_est<30) |'
          ' truth IT+PS ds med |')
    print('|' + '---|' * 16)
    for m in masses:
        for lam in lams:
            R = rows[(rows[:, 0] == m) & (rows[:, 1] == lam)]
            if len(R) == 0:
                continue
            med = lambda j: np.nanmedian(R[:, j])
            print(f'| {m:.0f} | {lam:g} | {len(R)} | {med(4)*1e4:.3g} | {med(5)*1e4:.3g} | {med(6):.2f} | {med(8)*1e4:.3g} |'
                  f' {med(9)*1e4:.3g} | {med(10)*1e4:.3g}/{med(11)*1e4:.3g}/{med(12)*1e4:.3g} |'
                  f' {np.mean(R[:,4]<0.01):.2f} | {np.mean(R[:,8]<0.01):.2f} | {np.mean(R[:,7]>0.01):.2f} |'
                  f' {np.mean(R[:,4]<0.003):.2f} | {np.mean(R[:,8]<0.003):.2f} | {med(14)*1e4:.3g} |', flush=True)
    print(f'median |n_z| of fitted plane normal: {np.median(rows[:, 13]):.2f}')
