"""M2_single.py -- E2 measurement M2: controlled near-miss crossings in the pair CM frame (no tracker).

M2a (vacuum angular-momentum yo-yo, exact for the causal kernel): x1,2 = +-(d/2) e, p1,2 = +-p* n (n = z, e = x),
    static straight string of length d.  J = d p*, so the miss distance at every crossing is b = J/p* = d (checked).
    Scan d/l0 = 1e-10 ... 1e-2 (l0 = m/sigma), gamma* = 1.05, 1.3, 2, 3.  Observables per crossing k = 1..3:
    b, apsidal rotation psi_k = (A_TP,k - A_TP,k-1).e (axis = separation at the turning points), TP-to-TP relative
    transverse momentum change, impulse profile dPi(tau).  Solvers: causal kernel (max_boost 1e-2, 1e-3),
    conformal (N = 256, 2048), and the CM-frame straight string (Kang-Luty force, T2 LabStraightString, which in the
    CM frame with P = 0 is the Li CM-simultaneous straight string) as the heuristic's reference.
M2b (field-driven crossings): constant transverse E (GeV/cm per unit charge, eps = qE/sigma) along e, pair produced
    at a point (Athena bootstrap) with p1,2 = +-p* n; eps = 1e-9 ... 1e-3; gamma* = 1.05, 1.3, 2, 3; orientation scan
    (angle of E to n = 90, 60, 30 deg) at gamma* = 1.3.  6 crossings.  Causal (1e-2, 1e-3) and conformal (N = 256, 1024).
Outputs: results/raw/M2/*.npz (one file per run, skipped if present), merged results/M2.json (by M2_analysis.py).
Run: pixi run python analytic/numerics/M2_single.py [a|b|ss|all]      (~5-15 min on 7 cores)
"""
import os, sys, time
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', 'code'))
RAW = os.path.join(HERE, 'results', 'raw', 'M2'); os.makedirs(RAW, exist_ok=True)

M = 500.0
LAM = 1.0
GSTARS = [1.05, 1.3, 2.0, 3.0]
DGRID = 10.0 ** np.arange(-10, -1.99, 0.5)
EGRID = 10.0 ** np.arange(-9, -2.99, 0.5)
KEYS = ('k', 'parity', 'b', 'bN', 'bP', 'gamma1', 'vrel', 'l_before', 'dA_N', 'dA_P', 'dPiTP_N', 'dPiTP_P',
        'dJTP_N', 'dJTP_P', 'aN', 'aP', 'r_lab', 'flag', 'cos_b_E', 't')


def setup(gs, lam=LAM, m=M):
    from T2_propagator import sigma_from_lambda_keV
    sig = sigma_from_lambda_keV(lam)
    ps = m * np.sqrt(gs ** 2 - 1); Es = np.hypot(m, ps)
    return sig, ps, Es, 2 * ps / sig, m / sig


def conf_valid(r):
    """The conformal gauge degenerates when the string collapses to ~zero length at a crossing (b/l0 <~ 1e-10):
    lab time then stops being monotonic in tau.  Such runs are flagged invalid."""
    R0, R1 = r['rec']
    return bool(len(R0) > 10 and np.all(np.diff(R0[:, 1]) > 0) and np.all(np.diff(R1[:, 1]) > 0))


def job_a(args):
    gs, dl, solver, par, lam, m = args
    tag = f"A_g{gs:g}_d{dl:.3e}_{solver}{par:g}_L{lam:g}_m{m:g}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 'skip'
    from nm_kernel import run
    import nm_conformal as NC
    from nm_crossings import analyse, table
    sig, ps, Es, Th, l0 = setup(gs, lam, m)
    n = np.array([0.0, 0.0, 1.0]); e = np.array([1.0, 0.0, 0.0])
    d = dl * l0
    p1 = ps * n; p2 = -ps * n
    P0 = np.r_[2 * Es, 0, 0, 0]; pi = (np.r_[Es, p1], np.r_[Es, p2])
    t0 = time.time()
    if solver == 'causal':
        r = run(p1, p2, m, sigma=sig, B0=0.0, x1_0=0.5 * d * e, x2_0=-0.5 * d * e, d_init=d, e_init=e,
                t_end=3.7 * Th, r_exit=1e9, z_exit=1e9, max_boost=par, hmax_trk=1e9, hmax_out=1e9, rec=True,
                rec_dt=Th / 400, rec_radii=np.array([1e8]), rec_zmax=np.array([1e9]))
        res = analyse(r['rec'][0], r['rec'][1], 'causal', P0, m, sig, n, eN=e, Th=Th, p_init=pi, ncross_max=3)
    else:
        N = int(par)
        r = NC.run(p1, p2, m, sigma=sig, Bz=0.0, N=N, d_init=d, e_init=e, t_end=3.7 * Th, r_stop=1e9, rec=True,
                   rec_dt=Th / 400, radii=np.array([1e8]))
        if not conf_valid(r):
            np.savez(fn, valid=False, gs=gs, dl=dl, cpu=time.time() - t0)
            return tag, 'invalid (conformal gauge breakdown)'
        res = analyse(r['rec'][0], r['rec'][1], 'conf', P0, m, sig, n, eN=e, Th=Th, p_init=pi, ncross_max=3,
                      h_conf=np.pi / N)
    T, _ = table(res, KEYS)
    prof = np.array([c['profile'] for c in res['crossings']])
    np.savez(fn, valid=True, T=T, keys=np.array(KEYS), prof=prof, gs=gs, dl=dl, d=d, sig=sig, ps=ps, Th=Th, l0=l0, m=m, lam=lam,
             v=ps / Es, nsteps=r['nsteps'], status=r['status'], cpu=time.time() - t0)
    return tag, f"{time.time()-t0:.1f}s"


def job_ss(args):
    """Straight string (Kang-Luty force, CM frame) for the M2a initial data: b at the first crossing (event of the
    longitudinal separation), apsidal rotation between the two turning points around it."""
    gs, dl = args
    tag = f"SS_g{gs:g}_d{dl:.3e}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 'skip'
    from T2_propagator import LabStraightString
    sig, ps, Es, Th, l0 = setup(gs)
    n = np.array([0.0, 0.0, 1.0]); e = np.array([1.0, 0.0, 0.0])
    d = dl * l0
    t0 = time.time()
    ss = LabStraightString(M, M, sig, rtol=1e-12, atol_x=1e-16 * l0, atol_p=1e-13)
    out = ss.run(ps * n, -ps * n, 2.2 * Th, x1=0.5 * d * e, x2=-0.5 * d * e, max_step=Th / 300)
    t = out['t']; y = out['y']
    sep = y[:, 0:3] - y[:, 6:9]
    s = np.linalg.norm(sep, axis=1)
    i0 = np.argmax(np.where(t < Th, s, -1)); i1 = np.argmax(np.where((t > Th) & (t < 2 * Th), s, -1))
    A0 = sep[i0] / s[i0]; A1 = -sep[i1] / s[i1]
    zl = sep @ n
    win = np.where((t > 0.5 * Th) & (t < 1.5 * Th))[0]
    jj = win[np.where(np.sign(zl[win][:-1]) != np.sign(zl[win][1:]))[0][0]]
    E1 = np.sqrt(M ** 2 + (y[jj, 3:6] ** 2).sum()); E2 = np.sqrt(M ** 2 + (y[jj, 9:12] ** 2).sum())
    dv = y[jj, 3:6] / E1 - y[jj, 9:12] / E2
    dx = sep[jj]
    b = float(np.linalg.norm(dx - (dx @ dv) / (dv @ dv) * dv))
    tc = out['tcross']
    p1a = y[i0, 3:6]; p1b = y[i1, 3:6]
    np.savez(fn, gs=gs, dl=dl, d=d, b=b, psi=float((A1 - A0) @ e), l_before=s[i0], l_after=s[i1],
             dPi=float(((p1b - y[i1, 9:12]) - (p1a - y[i0, 9:12])) @ e / 2), Th=Th, l0=l0, sig=sig,
             ncross=len(tc), cpu=time.time() - t0)
    return tag, f"{time.time()-t0:.1f}s"


def job_b(args):
    gs, eps, theta_deg, solver, par = args
    tag = f"B_g{gs:g}_e{eps:.3e}_th{theta_deg:g}_{solver}{par:g}"
    fn = os.path.join(RAW, tag + '.npz')
    if os.path.exists(fn):
        return tag, 'skip'
    from nm_kernel import run
    import nm_conformal as NC
    from nm_crossings import analyse, table
    sig, ps, Es, Th, l0 = setup(gs)
    n = np.array([0.0, 0.0, 1.0])
    th = np.radians(theta_deg)
    Edir = np.array([np.sin(th), 0.0, np.cos(th)])
    Ev = eps * sig * Edir
    eN = np.array([1.0, 0.0, 0.0])
    p1 = ps * n; p2 = -ps * n
    P0 = np.r_[2 * Es, 0, 0, 0]; pi = (np.r_[Es, p1], np.r_[Es, p2])
    t0 = time.time()
    if solver == 'causal':
        r = run(p1, p2, M, sigma=sig, B0=0.0, E=Ev, t_end=6.7 * Th, r_exit=1e9, z_exit=1e9, max_boost=par,
                hmax_trk=1e9, hmax_out=1e9, first_length=1e-9 * l0, rec=True, rec_dt=Th / 400,
                rec_radii=np.array([1e8]), rec_zmax=np.array([1e9]))
        res = analyse(r['rec'][0], r['rec'][1], 'causal', P0, M, sig, n, eN=eN, Estar=Ev, Th=Th, p_init=pi,
                      ncross_max=6)
    else:
        N = int(par)
        # the collinear R1 bootstrap is degenerate for an exactly 1-D CM configuration (conformal gauge singular when the
        # string collapses at a crossing); seed a small static string d = 1e-3 eps l0 along y (adds b_odd*(1+5e-7)) (perpendicular to E)
        r = NC.run(p1, p2, M, sigma=sig, Bz=0.0, E=Ev, N=N, d_init=1e-3 * eps * l0, e_init=np.array([0.0, 1.0, 0.0]),
                   t_end=6.7 * Th, r_stop=1e9, rec=True, rec_dt=Th / 400, radii=np.array([1e8]))
        if not conf_valid(r):
            np.savez(fn, valid=False, gs=gs, eps=eps, theta=theta_deg, cpu=time.time() - t0)
            return tag, 'invalid (conformal gauge breakdown)'
        res = analyse(r['rec'][0], r['rec'][1], 'conf', P0, M, sig, n, eN=eN, Estar=Ev, Th=Th, p_init=pi,
                      ncross_max=6, h_conf=np.pi / N)
    T, _ = table(res, KEYS)
    prof = np.array([c['profile'] for c in res['crossings']])
    np.savez(fn, valid=True, T=T, keys=np.array(KEYS), prof=prof, gs=gs, eps=eps, theta=theta_deg, sig=sig, ps=ps, Th=Th,
             l0=l0, v=ps / Es, nsteps=r['nsteps'], status=r['status'], cpu=time.time() - t0)
    return tag, f"{time.time()-t0:.1f}s"


def tasks(which):
    ta, ts, tb = [], [], []
    if which in ('a', 'all'):
        for gs in GSTARS:
            for i, dl in enumerate(DGRID):
                ta += [(gs, dl, 'causal', 1e-2, LAM, M), (gs, dl, 'conf', 256, LAM, M)]
                if i % 2 == 0:
                    ta += [(gs, dl, 'causal', 1e-3, LAM, M), (gs, dl, 'conf', 2048, LAM, M)]
        # scale-invariance check: different (Lambda, m) at the same gamma*, d/l0
        for dl in (1e-8, 1e-5, 1e-3):
            ta += [(1.3, dl, 'causal', 1e-2, 3.0, 1000.0), (1.3, dl, 'causal', 1e-2, 0.6, 200.0)]
    if which in ('ss', 'all'):
        for gs in GSTARS:
            for dl in DGRID[::2]:
                if dl >= 1e-9:
                    ts.append((gs, dl))
    if which in ('b', 'all'):
        for gs in GSTARS:
            for i, eps in enumerate(EGRID):
                tb += [(gs, eps, 90.0, 'causal', 1e-2), (gs, eps, 90.0, 'causal', 1e-3)]
                if eps >= 1e-6:
                    tb += [(gs, eps, 90.0, 'conf', 256)]
                    if i % 2 == 0:
                        tb += [(gs, eps, 90.0, 'conf', 1024)]
        for th in (60.0, 30.0):
            for eps in EGRID[::2]:
                tb += [(1.3, eps, th, 'causal', 1e-3)]
                if eps >= 1e-6:
                    tb += [(1.3, eps, th, 'conf', 256)]
    return ta, ts, tb


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    ta, ts, tb = tasks(which)
    tic = time.time()
    ctx = mp.get_context('spawn')
    with ProcessPoolExecutor(7, mp_context=ctx) as ex:
        futs = [ex.submit(job_a, a) for a in ta] + [ex.submit(job_b, b) for b in tb] + [ex.submit(job_ss, s) for s in ts]
        for i, f in enumerate(futs):
            tag, msg = f.result()
            if i % 20 == 0 or 'SS' in tag:
                print(f"[{i+1}/{len(futs)}] {tag}: {msg}  ({time.time()-tic:.0f}s)", flush=True)
    print(f"M2 done: {len(futs)} runs in {time.time()-tic:.0f} s wall", flush=True)
