"""S_Bnonlin.py -- synthesis check of T4's claim G-T4-4 ("the causal-string B response is not linear in B;
vacuum + first-order B misses 30-45 % of the 3.8 T effect").

Purpose
-------
Re-run the T4 causal-string kernel (T4_model.run, a copy of the Athena/T2/T3 null-vector algorithm) for the same
events at B = f * 3.8112 T, f in {0, 1/80, 1/20, 1/4, 1}, and at two numerical settings (max_boost = 1e-2, the T4
default, and 1e-3 with a smaller step cap), then decompose the hit displacement y(B) - y(0):
  * rphi (the T4 observable), and the 3D displacement projected on the vacuum-plane normal (out-of-plane) vs in-plane;
  * hits split by crossing steepness |v_r|/|v_T| at the hit (steep >= 0.5 vs shallow, near-tangent < 0.5),
    because a crossing-point displacement at fixed radius amplifies a trajectory shift by 1/|v_r| (non-linear
    when the shift is comparable to the curvature of a near-tangent crossing);
  * T4's non-linearity metric: Q68 |d(B) - 20 d(B/20)| / Q68 |d(B)| per layer group (IT / PS / 2S).
Also prints the response ratio R(f) = Q68|d(f)/f| / Q68|d(1)| (=1 for a linear response).

Inputs: T2 kinematics cache (T3_propagator.load_cache; env T2_CACHE or data/cache), T4_model.
Run (from theory_track/): pixi run python code/S_Bnonlin.py [nev] [m1,m2] [lam1,lam2]   (default 6 events, 500,1000 GeV,
1,3 keV; ~5-15 min)
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import run, sample_theta, momenta, SENS_R, B_CMS  # noqa: E402
from T3_propagator import plane_fit  # noqa: E402

FRACS = [1 / 80, 1 / 20, 1 / 4, 1.0]
GROUPS = {'IT': range(0, 4), 'PS': range(4, 7), '2S': range(7, 10)}


def hits_by_key(hits):
    out = {}
    for h in hits:
        L = int(h[1])
        if L > 9:
            continue
        out[(int(h[0]), L, int(h[9]))] = h
    return out


def disp(hb, h0, nrm):
    """rphi displacement (cm), out-of-plane (cm), steepness of the vacuum crossing."""
    R = SENS_R[int(h0[1])]
    ph = np.arctan2(hb[4], hb[3]) - np.arctan2(h0[4], h0[3])
    ph = (ph + np.pi) % (2 * np.pi) - np.pi
    d3 = hb[3:6] - h0[3:6]
    x, y = h0[3], h0[4]; px, py = h0[6], h0[7]
    vr = (px * x + py * y) / R
    vt = np.hypot(px, py)
    steep = abs(vr) / max(vt, 1e-12)
    return R * ph, float(d3 @ nrm), steep


def one_event(theta, mb, hmax):
    r0 = run(theta, B0=0.0, max_boost=mb, hmax=hmax)
    H0 = hits_by_key(r0['hits'])
    pts = np.array([h[3:6] for h in H0.values()])
    _, nrm = plane_fit(pts)
    res = {}
    for f in FRACS:
        rb = run(theta, B0=B_CMS * f, max_boost=mb, hmax=hmax)
        HB = hits_by_key(rb['hits'])
        res[f] = {k: disp(HB[k], H0[k], nrm) for k in H0 if k in HB}
    return res


def q68(a):
    a = np.abs(np.asarray(a))
    return np.quantile(a, 0.68) if len(a) else np.nan


def main():
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    masses = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [500.0, 1000.0]
    lams = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [1.0, 3.0]
    settings = [(1e-2, 0.01), (1e-3, 0.002)]
    for m in masses:
        rng = np.random.default_rng(int(m) + 11)       # same seed convention as T4_fisher.py
        thetas = sample_theta(m, nev, rng, eta_max=1.0)
        for lam in lams:
            for mb, hmax in settings:
                t0 = time.time()
                allres = []
                for th in thetas:
                    th = th.copy(); th[8] = np.log(lam)
                    allres.append(one_event(th, mb, hmax))
                print(f'\n=== m={m:.0f} GeV, Lambda={lam:g} keV, max_boost={mb:g}, hmax={hmax} cm '
                      f'({nev} events, {time.time()-t0:.0f} s)')
                print('group  sel     |d(B)| Q68 [um]: rphi  outpl | nonlin T4-metric rphi  outpl | '
                      'R(1/80) R(1/20) R(1/4) [rphi]  | Nhits')
                for gname, Ls in GROUPS.items():
                    for sel in ('all', 'steep', 'shallow'):
                        dB_r, dB_n, nl_r, nl_n = [], [], [], []
                        rat = {f: [] for f in FRACS}
                        for res in allres:
                            for k, (dr, dn, st) in res[1.0].items():
                                if k[1] not in Ls:
                                    continue
                                if sel == 'steep' and st < 0.5:
                                    continue
                                if sel == 'shallow' and st >= 0.5:
                                    continue
                                if k not in res[1 / 20]:
                                    continue
                                dB_r.append(dr); dB_n.append(dn)
                                nl_r.append(dr - 20 * res[1 / 20][k][0])
                                nl_n.append(dn - 20 * res[1 / 20][k][1])
                                for f in FRACS:
                                    if k in res[f]:
                                        rat[f].append(res[f][k][0] / f)
                        if not dB_r:
                            continue
                        qB = q68(dB_r)
                        print(f'{gname:4s} {sel:8s} {qB*1e4:10.2f} {q68(dB_n)*1e4:7.2f} | '
                              f'{q68(nl_r)/qB:22.3f} {q68(nl_n)/max(q68(dB_n),1e-12):6.3f} | '
                              f'{q68(rat[1/80])/qB:7.3f} {q68(rat[1/20])/qB:7.3f} {q68(rat[1/4])/qB:7.3f}'
                              f'          | {len(dB_r)}')
                sys.stdout.flush()


if __name__ == '__main__':
    main()
