"""M5_li_blinearity.py -- E2 measurement M5 (coordinator request): is the B ln(1/B) non-linearity of the causal string
present in a step-converged straight string?

Integrator: the literal Li-Li-Pei-Zhang CM-simultaneous straight string of code/R1_li_literal.li_run, via its scalarised
copy nm_li.run_li (validated against it: 0.3 um at 1e-3 of the printed step;
explicit Euler, Kang-Luty force, CM simultaneity Eq.III.6-7, s_hat Eq.III.8-9), at 1e-3 of the printed step bound for
all events and 3e-4 for the first NCONV events (convergence check).  Reference: causal kernel (nm_kernel = T3_causal B-only) at max_boost 1e-3, hmax 0.02 cm.
Events: the R1 recipe (R1_conformal_ng.make_event: m = 500 GeV, gamma* = 1.28, pT = 300 GeV, |y| < 0.8), seed 2026,
NEV events, Lambda = 1 keV.  B = B0 x {1, 1/4, 1/20, 1/80}, B0 = 3.8 T (R1 convention), plus B = 0 for each integrator.
Metrics (hits matched by quirk, layer and order of crossing of that layer):
  d(f) = hit(f B0) - hit(0) [same integrator, same step, so step-dependent in-plane phase errors cancel to first order];
  response per unit B  R(k) = median_hits |d(B0/k)| k / |d(B0)|, and the S/T4 metric Q68|d(B0) - k d(B0/k)| / Q68|d(B0)|,
  split into hits before / after the first crossing (vacuum lab crossing time Dt); also the event-level
  Delta_s(B0/k) k / Delta_s(B0).
Output: results/raw/M5/ev<i>.npz (one per event), results/M5.json.
Run: pixi run python analytic/numerics/M5_li_blinearity.py [NEV] [workers]
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, 'results', 'raw', 'M5'); os.makedirs(RAW, exist_ok=True)
M = 500.0; LAM = 1.0; B0 = 3.8
KS = [1.0, 4.0, 20.0, 80.0]
LI_FRACS = [1e-3, 3e-4]
NCONV = 6          # events with the 3e-4 step-convergence check (one Li run at 1e-3 = 5e7 Euler steps ~ 90 s)


def keyed(H):
    """dict (quirk, layer, n-th crossing of that layer) -> hit row [k, L, t, x, y, z]."""
    out = {}; cnt = {}
    for h in H[np.argsort(H[:, 2])]:
        key = (int(h[0]), int(h[1])); cnt[key] = cnt.get(key, 0) + 1
        out[key + (cnt[key],)] = h
    return out


def job(args):
    i, p1, p2 = args
    fn = os.path.join(RAW, f'ev{i:03d}.npz')
    if os.path.exists(fn):
        return i, 0.0
    from nm_li import run_li, RADII
    from nm_kernel import run
    t0 = time.time()
    out = {}
    for frac in (LI_FRACS if i < NCONV else LI_FRACS[:1]):
        for k in [0.0] + KS:
            Bz = 0.0 if k == 0.0 else B0 / k
            H, ns = run_li(p1, p2, M, LAM, Bz=Bz, frac=frac)
            out[f'li{frac:g}_k{k:g}'] = H
    for k in [0.0] + KS:
        Bz = 0.0 if k == 0.0 else B0 / k
        r = run(p1, p2, M, LAM, B0=Bz, max_boost=1e-3, hmax_trk=0.02, rec_radii=RADII, rec_zmax=np.full(10, 1e9))
        out[f'causal_k{k:g}'] = r['hits'][:, :6]
    np.savez(fn, p1=p1, p2=p2, **out)
    return i, time.time() - t0


def analyse(nev, first=None):
    from T2_propagator import ExactPair, sigma_from_lambda_keV
    from nm_stats import q68, boot, dump
    from T3_propagator import plane_fit
    res = {}
    for integ in [f'li{f:g}' for f in LI_FRACS] + ['causal']:
        per = {k: dict(pre=[], post=[], nl_pre=[], nl_post=[], ds=[], ds_ratio=[]) for k in KS[1:]}
        dB_pre_all, dB_post_all = [], []
        for i in range(nev if first is None else first):
            fn = os.path.join(RAW, f'ev{i:03d}.npz')
            if not os.path.exists(fn):
                continue
            z = np.load(fn)
            if f'{integ}_k0' not in z:
                continue
            ex = ExactPair(z['p1'], z['p2'], M, M, sigma_from_lambda_keV(LAM))
            Dt = ex.crossing_spacing_lab()[1]
            H0 = keyed(z[f'{integ}_k0'])
            H1 = keyed(z[f'{integ}_k1'])
            d1 = {key: H1[key][3:6] - H0[key][3:6] for key in H1 if key in H0}
            ds1 = plane_fit(z[f'{integ}_k1'][:, 3:6])[0]
            for k in KS[1:]:
                Hk = keyed(z[f'{integ}_k{k:g}'])
                dsk = plane_fit(z[f'{integ}_k{k:g}'][:, 3:6])[0]
                per[k]['ds_ratio'].append(dsk * k / ds1)
                for key, dv in d1.items():
                    if key not in Hk:
                        continue
                    dk = Hk[key][3:6] - H0[key][3:6]
                    pre = H1[key][2] < Dt
                    nb = np.linalg.norm(dv)
                    if nb <= 0:
                        continue
                    per[k]['pre' if pre else 'post'].append(np.linalg.norm(dk) * k / nb)
                    per[k]['nl_pre' if pre else 'nl_post'].append((np.linalg.norm(dv - k * dk), nb))
        e = {}
        for k in KS[1:]:
            p = per[k]
            ent = {}
            for part in ('pre', 'post'):
                a = np.array(p[part])
                ent[f'R_{part}_median'], ent[f'R_{part}_err'], _, _ = boot(lambda x: np.median(x), a) if len(a) > 1 else (np.nan, np.nan, 0, 0)
                ent[f'n_{part}'] = int(len(a))
                nl = np.array(p[f'nl_{part}'])
                ent[f'nonlin_{part}'] = float(q68(nl[:, 0]) / q68(nl[:, 1])) if len(nl) else np.nan
            ds = np.array(p['ds_ratio'])
            ent['ds_ratio_median'], ent['ds_ratio_err'], _, _ = boot(lambda x: np.median(x), ds)
            e[f'k{k:g}'] = ent
        res[integ] = e
    return res


if __name__ == '__main__':
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    nw = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    from R1_conformal_ng import make_event
    rng = np.random.default_rng(2026)
    evs = [make_event(rng, M) for _ in range(nev)]
    tic = time.time(); cpu = 0.0
    with ProcessPoolExecutor(nw, mp_context=mp.get_context('spawn')) as ex:
        for i, dt in ex.map(job, [(i, p1, p2) for i, (p1, p2) in enumerate(evs)]):
            cpu += dt
            if i % 5 == 0:
                print(f'ev{i}: {dt:.1f}s (wall {time.time()-tic:.0f}s)', flush=True)
    res = analyse(nev)
    res6 = analyse(nev, first=NCONV)
    from nm_stats import dump
    dump(dict(description=__doc__, results=res, results_first_NCONV_events=res6, nev=nev, nconv=NCONV,
              cpu_seconds_this_invocation=cpu, cpu_seconds_first_run=1153.0), os.path.join(HERE, 'results', 'M5.json'))
    for integ, e in res6.items():
        for k, ent in e.items():
            print(f"[first {NCONV} ev] {integ:9s} {k:4s} | R_post {ent['R_post_median']:.4f}±{ent['R_post_err']:.4f} | nonlin post {ent['nonlin_post']:.4f} | ds ratio {ent['ds_ratio_median']:.4f}±{ent['ds_ratio_err']:.4f}")
    print('integrator | k | R_pre (median k|d(B/k)|/|d(B)|) | R_post | nonlin pre | nonlin post | Delta_s(B/k) k/Delta_s(B)')
    for integ, e in res.items():
        for k, ent in e.items():
            print(f"{integ:9s} {k:4s} | {ent['R_pre_median']:.4f}±{ent['R_pre_err']:.4f} ({ent['n_pre']}) | {ent['R_post_median']:.4f}±{ent['R_post_err']:.4f} ({ent['n_post']}) | "
                  f"{ent['nonlin_pre']:.4f} | {ent['nonlin_post']:.4f} | {ent['ds_ratio_median']:.4f}±{ent['ds_ratio_err']:.4f}")
    print(f'cpu {cpu:.0f}s')
