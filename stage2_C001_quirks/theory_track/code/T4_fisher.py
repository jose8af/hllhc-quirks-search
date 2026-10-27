"""T4_fisher.py -- Jacobians, Fisher information and model-validation residuals for quirk-pair hit patterns.

For each (m_Q, Lambda) in {200, 500, 1000} GeV x {1, 3, 10} keV, sample LO DY+ISR pairs (T2 cache, pT(QQ) > 200 GeV,
|eta_pair| < 1; fermion E) and, per event, with the T4_model causal-string kernel (B uniform 3.8112 T, thin-scatterer
material):
  1. nominal runs: vacuum (B = 0), B/20, B, B + mean energy loss  -> per-layer model-validation residuals
     (first-order B effect, second-order (non-linear in B) remainder, energy-loss shift);
  2. Jacobians of the measurement vector y w.r.t. the NATURAL parameters u = [z0, ln (beta gamma)_T, phi, eta,
     ln(g*-1), cos*, phi*, ln l0, ln sigma] (+ mat_scale) (T4_model.theta_to_nat; Fisher converted to physical later)
     by central finite differences (adaptive step: max position shift ~ 20 um), for (a) B = 0, (b) B, (c) B + eloss
     (+ mat_scale nuisance);
  3. MS Jacobian: one run per (quirk, material crossing, direction) with a deterministic deflection
     xi = 0.3 theta0 -> C_MS = J_xi J_xi^T (thin scatterers, Highland; linear).
Measurement vector y: per hit (quirk k, layer L, crossing n): r*dphi and z (L = 0-9), BTL time of the first crossing
(L = 10), ln(dE/dx) for IT hits (L = 0-3).  Hit-to-quirk assignment is assumed known.
Output: figures/T4_fisher_<m>_<lam>.pkl (per-event Jacobians, keys, residuals).  Analysis: T4_fisher_report.py.
Run: pixi run python code/T4_fisher.py [nev] [nproc]      (default 16 events per point, 4 processes; ~30-60 min)
"""
import os, sys, time, pickle
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import run, sample_theta, B_CMS, SENS_R, bethe, momenta, PNAMES, theta_to_nat, nat_to_theta  # noqa: E402
from T2_propagator import sigma_from_lambda_keV  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
H0 = np.array([1e-3, 1e-4, 1e-5, 1e-5, 1e-4, 1e-5, 1e-4, 1e-5, 1e-2, 0.05])   # natural-parameter steps
TARGET = 20e-4     # target max position shift of a finite-difference step [cm]
XI_EPS = 0.3


def measure(hits, phi_ref):
    y = {}
    for h in hits:
        k, L, n = int(h[0]), int(h[1]), int(h[9])
        if L <= 9:
            ph = np.arctan2(h[4], h[3]) - phi_ref
            ph = (ph + np.pi) % (2 * np.pi) - np.pi
            y[(k, L, n, 'r')] = SENS_R[L] * ph
            y[(k, L, n, 'z')] = h[5]
            if L <= 3:
                y[(k, L, n, 'e')] = np.log(bethe(h[10]))
        elif L == 10 and n == 1:
            y[(k, L, n, 't')] = h[2]
    return y


def maxpos(d):
    v = [abs(x) for kk, x in d.items() if kk[3] in 'rz']
    return max(v) if v else 0.0


def jacobian(theta, phi_ref, base_kw, idx, steps, adapt):
    """Central finite differences w.r.t. the NATURAL parameters u = theta_to_nat(theta) (T4_model.UNAMES)."""
    u0 = theta_to_nat(theta)
    cols = {}
    used = {}
    for i in idx:
        h = steps[i]
        for it in range(2 if adapt else 1):
            up = u0.copy(); um = u0.copy(); up[i] += h; um[i] -= h
            yp = measure(run(nat_to_theta(up), **base_kw)['hits'], phi_ref)
            ym = measure(run(nat_to_theta(um), **base_kw)['hits'], phi_ref)
            keys = set(yp) & set(ym)
            d = {kk: (yp[kk] - ym[kk]) / 2 for kk in keys}
            mp = maxpos(d)
            if adapt and it == 0 and mp > 0:
                fac = TARGET / mp
                if 0.3 < fac < 3:
                    break
                h = min(h * min(max(fac, 1e-4), 1e4), 0.3)
                continue
            break
        cols[i] = {kk: v / h for kk, v in d.items()}
        used[i] = h
    return cols, used


def event_job(args):
    m, lam, iev, theta = args
    t0 = time.time()
    theta = theta.copy(); theta[8] = np.log(lam)
    phi_ref = theta[2]
    out = dict(m=m, lam=lam, iev=iev, theta=theta.copy())
    # --- nominal runs
    kw_vac = dict(B0=0.0); kw_B = dict(B0=B_CMS); kw_E = dict(B0=B_CMS, do_eloss=True)
    r_vac = run(theta, **kw_vac); r_B = run(theta, **kw_B); r_Bs = run(theta, B0=B_CMS / 20)
    th10 = np.r_[theta, 1.0]
    r_E = run(th10, **kw_E)
    y = {name: measure(r['hits'], phi_ref) for name, r in (('vac', r_vac), ('B', r_B), ('Bs', r_Bs), ('E', r_E))}
    out['y'] = y
    out['hits_B'] = r_B['hits']
    # --- Jacobians
    JB, steps = jacobian(theta, phi_ref, kw_B, range(9), H0.copy(), True)
    # vacuum: ln sigma at fixed l0 and velocities is an exact symmetry -> use the B step (derivative ~ 0)
    st = H0.copy()
    for i, h in steps.items():
        st[i] = h
    Jvac, _ = jacobian(theta, phi_ref, kw_vac, range(9), st, False)
    JE, _ = jacobian(th10, phi_ref, kw_E, range(10), st, False)
    out['J'] = dict(vac=Jvac, B=JB, E=JE)
    out['steps'] = st
    # --- MS Jacobian (B, no eloss, do_ms with deterministic xi)
    r_ms = run(theta, B0=B_CMS, do_ms=True)
    nmat = r_ms['nmat']
    Jxi = []
    y0 = measure(r_ms['hits'], phi_ref)
    for k in (0, 1):
        for c in range(min(int(nmat[k]), 64)):
            for j in (0, 1):
                xi = np.zeros((2, 64, 2)); xi[k, c, j] = XI_EPS
                yy = measure(run(theta, B0=B_CMS, do_ms=True, xi=xi)['hits'], phi_ref)
                Jxi.append({kk: (yy[kk] - y0[kk]) / XI_EPS for kk in set(yy) & set(y0)})
    out['Jxi'] = Jxi
    out['nmat'] = nmat
    out['time'] = time.time() - t0
    return out


def main():
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    masses = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [200.0, 500.0, 1000.0]
    lams = [float(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [1.0, 3.0, 10.0]
    for m in masses:
        rng = np.random.default_rng(int(m) + 11)
        thetas = sample_theta(m, nev, rng, eta_max=1.0)
        for lam in lams:
            fn = os.path.join(FIG, f'T4_fisher_{int(m)}_{lam:g}.pkl')
            if os.path.exists(fn):
                print('exists', fn); continue
            tic = time.time()
            with Pool(nproc) as pool:
                res = pool.map(event_job, [(m, lam, i, th) for i, th in enumerate(thetas)])
            with open(fn, 'wb') as f:
                pickle.dump(res, f)
            print(f'm={m} lam={lam}: {len(res)} events, {time.time() - tic:.0f} s', flush=True)


if __name__ == '__main__':
    main()
