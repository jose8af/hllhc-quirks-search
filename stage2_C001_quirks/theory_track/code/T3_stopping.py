"""T3_stopping.py -- fraction of quirk pairs that stop in the CMS calorimeters / coil / yoke (Q5, input for T6).

Propagator: causal NG string (T3_causal.run_causal), simplified CMS field (bmode 1: 3.8 T inside the coil,
-1.8 T in barrel yoke iron, UNVERIFIED), material = Phase-2 tracker slabs + Evans-Luty cylindrical CMS
[1811.08903 Tab.1], mean Bethe dE/dx (same S(beta) as T6_stopping.py), straggling and MS on.
Stop criterion: pair-CM velocity |sum p_i| / sum E_i < 0.01 (for a 1-D yo-yo the quirks' total momentum in the pair
frame vanishes, so this ratio IS the CM velocity).  At beta_cm = 0.01 the residual CM range is
< 1 cm of iron for these masses (ESTIMATE, Bethe range scaling), i.e. negligible.  The remaining internal energy is
dissipated in place in ~0.1-0.3 us (T6_stopping.py).  Exit: r > 750 cm or |z| > 1100 cm.
Samples (fermion E, LO, T2 cache):
  'isr'  : DY + ISR, pT(QQ) > 200 GeV (the triggered sample of the tracker search);
  'incl' : inclusive DY (LO pT = 0) given a pair pT drawn from p(pT) ~ pT exp(-pT/p0), <pT> = 2 p0, p0 = 15 GeV
           (ESTIMATE of the Sudakov peak for M ~ 0.5-2.5 TeV DY; UNVERIFIED); rapidity and M kept.
Regions reported: tracker, ECAL+HCAL barrel |eta_stop| < 1 (Evans-Luty 'fiducial'), all calorimeter, coil, yoke, escaped.
Run: pixi run python code/T3_stopping.py [nev] [lams comma-separated]   (default 200, 0.3,1,3)
"""
import os, sys, time
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T3_propagator import load_cache, material_at, phase2_tracker, cms_outer_regions, MAT, sample_events
from T3_causal import run_causal

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')


def sample_incl(m, n, rng, p0=15.0):
    c = load_cache(); key = f'F_{int(m)}_incl'
    w = c[key + '_w']; gs = c[key + '_gamma_star']; cs = c[key + '_cstar']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
    idx = rng.choice(len(w), size=n, p=w / w.sum())
    out = []
    for k in idx:
        M = 2 * m * gs[k]
        y = np.arcsinh(np.sign(eta[k]) * bg[k])        # pT = 0: P_z = M sinh y
        pt = rng.gamma(2.0, p0)
        mT = np.hypot(M, pt); phi = rng.uniform(0, 2 * np.pi)
        P = np.array([pt * np.cos(phi), pt * np.sin(phi), mT * np.sinh(y)]); E = mT * np.cosh(y)
        b = P / E; bh = b / np.linalg.norm(b)
        tmp = np.array([1.0, 0, 0]) if abs(bh[0]) < 0.9 else np.array([0, 1.0, 0])
        e1 = np.cross(bh, tmp); e1 /= np.linalg.norm(e1); e2 = np.cross(bh, e1)
        ct = cs[k]; st = np.sqrt(max(0, 1 - ct * ct)); ph = rng.uniform(0, 2 * np.pi)
        nn = ct * bh + st * (np.cos(ph) * e1 + np.sin(ph) * e2)
        ps = m * np.sqrt(gs[k] ** 2 - 1); e_ = np.hypot(m, ps); g = E / M; b2 = b @ b
        pv = [sg * ps * nn + ((g - 1) * (b @ (sg * ps * nn)) / b2 + g * e_) * b for sg in (1, -1)]
        out.append((pv[0], pv[1], dict(pt=pt, eta=np.arcsinh(P[2] / pt), bg=np.linalg.norm(P) / M)))
    return out


CATS = ['tracker', 'ECAL+HCAL |eta|<1', 'calo other', 'coil', 'yoke', 'air/other', 'escaped', 'unfinished']


def classify(r):
    if r['status'] == 1:
        return 6
    if r['status'] != 2:
        return 7
    X = 0.5 * (r['X'][0, 1:] + r['X'][1, 1:])
    rr = np.hypot(X[0], X[1]); eta = np.arcsinh(X[2] / max(rr, 1e-9))
    if rr < 118.5 and abs(X[2]) < 293.5:
        return 0
    za, I, X0, xl, reg = material_at(X[0], X[1], X[2], phase2_tracker(), cms_outer_regions(), MAT)
    if reg in (0, 2) and abs(eta) < 1.0:
        return 1
    if reg in (0, 1, 2, 3):
        return 2
    if reg == 4:
        return 3
    if reg >= 5:
        return 4
    return 5


def job(a):
    m, lam, sample, k, p1, p2 = a
    r = run_causal(p1, p2, m, lam, bmode=1, r_exit=750.0, z_exit=1100.0, beta_stop=0.01, t_end=3e5, hmax_trk=0.5,
                   hmax_out=2.0, seed=7000 + k, rec_radii=np.array([1e9]), rec_zmax=np.array([1e9]), max_hits=10,
                   max_steps=60_000_000)
    X = 0.5 * (r['X'][0, 1:] + r['X'][1, 1:])
    return (m, lam, sample, k, classify(r), r['X'][0, 0], np.hypot(X[0], X[1]), X[2], r['eacc'].sum(), r['nsteps'])


if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    lams = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [0.3, 1.0, 3.0]
    rng = np.random.default_rng(31)
    tasks = []
    for m in (200.0, 500.0, 1000.0):
        evs = {'isr': sample_events(m, nev, rng=rng), 'incl': sample_incl(m, nev, rng)}
        for lam in lams:
            for sname, ev in evs.items():
                for k in range(nev):
                    tasks.append((m, lam, sname, k, ev[k][0], ev[k][1]))
    tic = time.time()
    with Pool(8) as pool:
        res = pool.map(job, tasks, chunksize=1)
    print(f'{len(tasks)} jobs in {time.time()-tic:.0f} s', flush=True)
    tag = '_'.join(f'{l:g}' for l in lams)
    rows = np.array([[m, lam, 0 if s == 'isr' else 1, k, c, t, rr, z, e, ns] for (m, lam, s, k, c, t, rr, z, e, ns) in res])
    np.save(os.path.join(FIG, f'T3_stopping_{tag}.npy'), rows)
    print('| sample | m_Q | Lambda | ' + ' | '.join(CATS) + ' | median t_stop [ns] (fiducial) |')
    print('|---|---|---|' + '---|' * len(CATS) + '---|')
    for si, sname in enumerate(('isr', 'incl')):
        for m in (200.0, 500.0, 1000.0):
            for lam in lams:
                s = (rows[:, 0] == m) & (rows[:, 1] == lam) & (rows[:, 2] == si)
                n = s.sum()
                fr = [np.sum(rows[s, 4] == c) / n for c in range(len(CATS))]
                fid = s & (rows[:, 4] == 1)
                tmed = np.median(rows[fid, 5]) / 29.979 if fid.sum() else np.nan
                print(f'| {sname} | {m:.0f} | {lam} | ' + ' | '.join(f'{f:.3f}' for f in fr) + f' | {tmed:.0f} |')
