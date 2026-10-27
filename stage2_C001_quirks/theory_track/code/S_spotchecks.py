"""S_spotchecks.py -- synthesis spot checks of headline numbers of the T1-T6 reports (theory track, executor S).

Each check re-derives a number independently (closed form) or re-runs the investigators' code with a NEW random
seed / sample, and prints PASS/FAIL against the number quoted in the report.  Sections:
  A  sigma(1 keV) and the l_max coefficient 3.947 cm (T2 Sec.2.2), plus one ExactPair event vs the closed form
  B  N_osc = sigma R /(2 beta* pT) in the barrel: median at Lambda = 1 keV, pT > 200 GeV (T2 Tab.3.1: ~12, m-indep.)
  C  BTL (r = 114.8 cm) pair-CM delay medians, |eta| < 1.5 (T3 Sec.6: 3.5 / 9.6 / 18.7 ns)
  D  Delta N_eff(BBN) of a decoupled SU(2) / SU(3) glue sector, T_dec ~ 10-60 GeV (T1 Sec.G-T1-4: 0.21 / 0.57)
  E  Lambda conventions: Tc/sqrt(sigma) (Teper 0912.3339 Eq.33) for N = 2, 3 vs T1 lattice table and T5
  F  T6: gamma-gamma / DY ratio from figures/T6_xsec_table.txt and the doublet ctau for dM = 341 MeV
  G  T2 Lambda_low formula of the strategy: 0.458 keV (m/100 GeV)^(1/4) from 1.16 um (m/100)(keV/L)^4 B = 100 um
  H  T3 MS floor: causal string, Phase-2 material, NEW seed: median Delta_s (M, B, B+M) at Lambda = 3 keV,
     m = 500 / 1000 GeV (T3 Tab.3.2: M = 17 / 24 um, B+M = 15 / 25 um) and the x2-material variant (T3: "~x1.4,
     untested numerically")
Run (from theory_track/): pixi run python code/S_spotchecks.py [nev_H]   (default 30; H takes ~5-15 min on 6 cores)
"""
import os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import sigma_from_lambda_keV, ExactPair  # noqa: E402
from T3_propagator import load_cache, sample_events  # noqa: E402

RES = []


def report(tag, value, ref, tol, unit=''):
    ok = abs(value - ref) <= tol
    RES.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {tag}: {value:.4g}{unit} vs quoted {ref:g}{unit} (tolerance {tol:g})")


def weighted_median(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); c /= c[-1]
    return x[i][np.searchsorted(c, 0.5)]


def cache_arrays(m, spin='F', sample='isr'):
    c = load_cache(); key = f'{spin}_{int(m)}_{sample}'
    w = c[key + '_w']; gs = c[key + '_gamma_star']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
    M = 2 * m * gs; P = M * bg; pt = P / np.cosh(eta); E = np.hypot(M, P)
    return w, gs, bg, eta, pt, P, E, M


def sec_A():
    print('\n--- A: sigma and l_max coefficient')
    s = sigma_from_lambda_keV(1.0)
    report('sigma(1 keV) [GeV/cm]', s, 50.68, 0.01)
    report('l_max coefficient 2*100 GeV/sigma [cm]', 200.0 / s, 3.947, 0.002)
    m = 500.0; gs = 1.28; ps = m * np.sqrt(gs ** 2 - 1)
    ex = ExactPair(np.array([ps, 0, 0]), np.array([-ps, 0, 0]), m, m, s)
    t = np.linspace(0, 4 * ps / s, 20001)
    X1, X2 = ex.lab_positions(t)
    lnum = np.max(np.linalg.norm(X1 - X2, axis=1))
    report('ExactPair max separation / closed form (rest frame, gamma*=1.28)', lnum / (2 * (gs - 1) * m / s), 1.0, 1e-4)


def sec_B():
    print('\n--- B: N_osc in the barrel (R = 110 cm), Lambda = 1 keV, LO DY+ISR pT > 200 GeV')
    s = sigma_from_lambda_keV(1.0)
    for m in (200.0, 500.0, 1000.0):
        w, gs, bg, eta, pt, P, E, M = cache_arrays(m)
        bs = np.sqrt(1 - 1 / gs ** 2)
        # barrel exit at R = 110 cm unless |z| > 270 cm first: path to exit along the CM line
        R = np.minimum(110.0, 270.0 / np.maximum(np.abs(np.sinh(eta)), 1e-9))
        nosc = s * R / (2 * bs * pt)
        sel = np.abs(eta) < 2.5
        med = weighted_median(nosc[sel], w[sel])
        report(f'N_osc median m={m:.0f} (T2 Tab.3.1: 12)', med, 12.0, 2.0)


def sec_C():
    print('\n--- C: BTL pair-CM delay (r = 114.8 cm), |eta| < 1.5, pT > 200 GeV')
    ref = {200.0: 3.5, 500.0: 9.6, 1000.0: 18.7}
    c = 29.9792458
    for m in (200.0, 500.0, 1000.0):
        w, gs, bg, eta, pt, P, E, M = cache_arrays(m)
        bT = pt / E
        sel = np.abs(eta) < 1.5
        R = 114.8
        # toa = t - |r|/c with the 3D distance |r| = R cosh(eta) (CMSSW digitiser convention, STRATEGY C8)
        delay = R / (bT * c) - R * np.cosh(eta) / c
        report(f'BTL delay median m={m:.0f} [ns]', weighted_median(delay[sel], w[sel]), ref[m], 0.1 * ref[m])
        i = np.argsort(delay[sel]); cw = np.cumsum(w[sel][i]); cw /= cw[-1]
        print(f'      84th percentile {delay[sel][i][np.searchsorted(cw, 0.84)]:.1f} ns (strategy median 6/16/33 ns)')


def sec_D():
    print('\n--- D: Delta N_eff at BBN for a dark glue sector decoupled at T ~ 10-60 GeV (g*s = 86.25)')
    xi = (10.75 / 86.25) ** (1 / 3)
    for N, ref in ((2, 0.21), (3, 0.57)):
        g = 2 * (N * N - 1)
        report(f'Delta N_eff SU({N})', 4 / 7 * g * xi ** 4, ref, 0.01)
    report('xi after e+e- annihilation', xi * (4 / 11) ** (1 / 3), 0.36, 0.005)


def sec_E():
    print('\n--- E: Lambda conventions')
    for N, ref in ((2, 0.7091), (3, 0.6462)):
        report(f'Tc/sqrt(sigma) SU({N}) from 0.597 + 0.45/N^2', 0.597 + 0.45 / N ** 2, ref, 0.005)
    report('sqrt(sigma) of "Tc = 1 keV" for SU(2) [keV]', 1 / 0.7091, 1.41, 0.01)
    report('ratio of the 1/0.6 convention to the SU(2) lattice value', (1 / 0.6) / (1 / 0.7091), 1.18, 0.01)


def sec_F():
    print('\n--- F: T6 gamma-gamma fraction and doublet ctau')
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T6_xsec_table.txt')
    rows = {}
    for line in open(f):
        if line.startswith('#'):
            continue
        n, v = line.rsplit(' | ', 1); rows[n.strip()] = [float(x) for x in v.split()]
    Ms = [100, 120, 200, 300, 500, 750, 1000, 1500]
    K = {200: 1.110, 500: 1.158, 1000: 1.254}
    dy = 'DY E (1,1)-1 F' if 'DY E (1,1)-1 F' in rows else None
    ga = 'gg(PDF, el+inel) E F' if 'gg(PDF, el+inel) E F' in rows else None
    if dy and ga:
        for m, ref in ((200, 4.5), (500, 4.6), (1000, 5.2)):
            r = 100 * rows[ga][Ms.index(m)] / rows[dy][Ms.index(m)]
            report(f'gamma-gamma(LO)/DY(LO) for E at m={m} [%]', r, ref, 0.3)
            print(f'      relative to the K-corrected DY (the sigma actually used): {r / K[m]:.2f} %')
    else:
        print('      could not identify rows automatically; skipped')
    # doublet ctau: Gamma = G_F^2 |Vud|^2 f_pi^2 dM^3 sqrt(1 - mpi^2/dM^2) / pi  (T6 G-T6-2, c = 1)
    GF, Vud, fpi, mpi, hbarc = 1.1663787e-5, 0.97373, 0.1302, 0.13957, 1.97327e-16   # hbarc in GeV m
    for dM, cc, ref in ((0.341, 1.0, 7.9e-3), (0.166, 2.0, 6.0e-2)):
        G = cc * GF ** 2 * Vud ** 2 * fpi ** 2 * dM ** 3 * np.sqrt(1 - (mpi / dM) ** 2) / np.pi
        report(f'ctau(Q+- -> Q0 pi+-) dM = {dM*1e3:.0f} MeV, c^2 = {cc:g} [mm]', hbarc / G * 1e3, ref * 1e3, 0.15 * ref * 1e3)


def sec_G():
    print('\n--- G: strategy Lambda_low from the 1.16 um formula at 3.8 T')
    for m, ref in ((200, 0.54), (500, 0.69), (1000, 0.81)):
        lam = (1.16 * (m / 100) * 3.8 / 100.0) ** 0.25
        report(f'Lambda_low(formula) m={m} [keV]', lam, ref, 0.01)


def _job(args):
    from T3_ms_thickness import observables
    from T3_causal import run_causal
    from T3_propagator import phase2_tracker
    m, lam, p1, p2, cfg, scale, seed = args
    r = run_causal(p1, p2, m, lam, slabs=phase2_tracker(scale), seed=seed, **cfg)
    return observables(r['hits'])[0]


def sec_H(nev):
    print(f'\n--- H: MS floor, causal string, Phase-2 material, new seed (rng 2026), {nev} events per point')
    cfgs = {'B': dict(B0=3.8112, material=False), 'B+M': dict(B0=3.8112), 'M': dict(B0=0.0)}
    ref = {(500.0, 'M'): 17, (500.0, 'B+M'): 15, (500.0, 'B'): 4.9, (1000.0, 'M'): 24, (1000.0, 'B+M'): 25, (1000.0, 'B'): 3.9}
    rng = np.random.default_rng(2026)
    jobs, keys = [], []
    for m in (500.0, 1000.0):
        evs = sample_events(m, nev, 'isr', rng=rng, eta_max=1.0)
        for i, (p1, p2, _info) in enumerate(evs):
            for name, cfg in cfgs.items():
                jobs.append((m, 3.0, p1, p2, cfg, 1.0, 1000 + i)); keys.append((m, name, 1.0))
            if m == 500.0:
                jobs.append((m, 3.0, p1, p2, cfgs['M'], 2.0, 1000 + i)); keys.append((m, 'M', 2.0))
    with Pool(6) as pool:
        out = pool.map(_job, jobs)
    out = np.array(out) * 1e4
    for (m, name), r in ref.items():
        v = np.array([o for o, k in zip(out, keys) if k == (m, name, 1.0)]); v = v[np.isfinite(v)]
        q = np.percentile(v, [16, 50, 84])
        tol = max(0.35 * r, 2.0)   # ~ statistical spread of a median from 30-60 events with a x3 16-84 band
        report(f'Delta_s median m={m:.0f}, Lambda=3 keV, {name} [um] (16-84: {q[0]:.1f}-{q[2]:.1f})', q[1], r, tol)
    v1 = np.array([o for o, k in zip(out, keys) if k == (500.0, 'M', 1.0)])
    v2 = np.array([o for o, k in zip(out, keys) if k == (500.0, 'M', 2.0)])
    ok = np.isfinite(v1) & np.isfinite(v2)
    print(f'      x2 material, M config, m=500: median ratio Delta_s(x2)/Delta_s(x1) = {np.median(v2[ok]/v1[ok]):.2f} '
          f'(sqrt(2) = 1.41 expected for pure Highland scaling)')


if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    sec_A(); sec_B(); sec_C(); sec_D(); sec_E(); sec_F(); sec_G()
    if nev > 0:
        sec_H(nev)
    print(f'\nSUMMARY: {sum(RES)}/{len(RES)} PASS')
