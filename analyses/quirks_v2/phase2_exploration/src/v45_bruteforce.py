"""v45_bruteforce.py -- C2-a, V4-5 brute-force cross-check of the F0 plane finder (channel (i), Rosalie, 2026-11-16).

Independent of acts/stage4/finder/finder.py and kernels.py (only the event preparation of chain_inputs.py is reused to
rebuild the identical hit pool from the stored S6 dumps).  Definition (STR §4.2, COM C2-a; fixed here before any run):
  * F0 normal n_F0: the stored normal of the top-ranked (lowest index) aligned candidate of the trial passing R04.
  * window hits: road hits (|dphi(hit, MET)| < road + asin(w_c / r), as the reference road) with |u . n2| <= w_c,
    n2 = n_F0 x a_F0 (in-plane, perpendicular to the F0 axis), w_c = 75 mm; u = hit - PV.
  * score(n) = sum_i exp(-(u_i . n)^2 / (2 s_i^2)),  s_i^2 = (sigma_rphi,i (n . e_phi,i))^2 + (sigma_z,i n_z)^2 + t_tol^2,
    t_tol = 0.030 mm: the resolution-weighted inlier count.
  * exhaustive scan: n = normalise(n_F0 + alpha e1 + beta e2), alpha, beta in [-0.3, 0.3] rad on a 0.2 mrad grid
    (3001 x 3001 normals); brute-force optimum = the maximum.  The score of every grid normal is accumulated hit by hit
    over the cells with |u . n| <= 4 sigma (bound per grid row); a cell outside a hit's band would get <= exp(-8) =
    3.4e-4 from that hit (revision 14:40 after the timing job: the direct sum costs ~52 min per trial at 18k window hits).
    Global scan (diagnostic: is there a better plane elsewhere?): same accumulation with ALL road hits on a 5 mrad grid
    of tangent coordinates within ±1.2 (±50 deg) of n_F0.
  * independent fit: scipy.optimize.least_squares on the two angles of n, residuals (u_i . n) / s_i over the F0
    inliers (|u . n_F0| <= 3 s_i within the window), started from n_F0.
  * agreement: |dn| = arccos(|n . n'|) < 1 mrad for (F0, optimum) and (F0, fit).  Criterion: >= 48 of 50 per sample.
BLINDING: signal mode takes the first events in file order whose in-job R04 bit (open tier) is set; it prints and stores
no count of rows scanned, so no pass fraction can be read from its output.
Modes:  pu  --files a.npz,b.npz --n 50   (first trials of the C1 rho = 1 sample with an F0 candidate at R04)
        (signal mode: added when the C1 full-chain outputs exist)
Output: $QV2_OUT_DIR/<tag>.json (per-trial angles, scores, timing).  Env: TT env python (numba, scipy).
"""
import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
sys.path.insert(0, str(QV2))
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
log = logging.getLogger("v45")
W_C, T_TOL, ROAD = 75.0, 0.030, 0.15
GRID_HALF, GRID_STEP, GLOBAL_STEP = 0.3, 2e-4, 5e-3
SELFCHECK = False
FULL_SPHERE = 0.0
GLOBAL_HALF = 1.2    # global scan: tangent-plane coordinates up to ±1.2 (±50 deg) around n_F0, all road hits

try:
    import numba as nb
    jit = nb.njit(cache=True, fastmath=False)    # serial: one core per runner job
    prange = range
except ImportError:      # pragma: no cover
    jit = lambda f: f    # noqa: E731
    prange = range


@jit
def scan_grid(U, EPX, EPY, S0, S1, n0, e1, e2, half, step):
    m = int(round(2 * half / step)) + 1
    best = np.full(m, -1.0)
    bj = np.zeros(m, np.int64)
    for i in prange(m):
        a = -half + i * step
        for j in range(m):
            b = -half + j * step
            nx = n0[0] + a * e1[0] + b * e2[0]; ny = n0[1] + a * e1[1] + b * e2[1]; nz = n0[2] + a * e1[2] + b * e2[2]
            nn = np.sqrt(nx * nx + ny * ny + nz * nz); nx /= nn; ny /= nn; nz /= nn
            s = 0.0
            for k in range(U.shape[0]):
                d = U[k, 0] * nx + U[k, 1] * ny + U[k, 2] * nz
                cp = S0[k] * (nx * EPX[k] + ny * EPY[k]); cz = S1[k] * nz
                v = cp * cp + cz * cz + 0.0009
                s += np.exp(-d * d / (2 * v))
            if s > best[i]:
                best[i] = s; bj[i] = j
    return best, bj


@jit
def scan_band(U, EPX, EPY, S0, S1, n0, e1, e2, half, step, K):
    """Same score as scan_grid on the same grid, accumulated hit by hit over the band of grid cells where
    |u . n| <= K sigma_row (sigma bounded per grid row); cells outside the band would add <= exp(-K^2/2) per hit."""
    m = int(round(2 * half / step)) + 1
    G = np.zeros((m, m))
    for k in range(U.shape[0]):
        c0 = U[k, 0] * n0[0] + U[k, 1] * n0[1] + U[k, 2] * n0[2]
        c1 = U[k, 0] * e1[0] + U[k, 1] * e1[1] + U[k, 2] * e1[2]
        c2 = U[k, 0] * e2[0] + U[k, 1] * e2[1] + U[k, 2] * e2[2]
        for i in range(m):
            a = -half + i * step
            # bound sigma over the row (|n| >= 1, numerators linear in b)
            pz0 = n0[2] + a * e1[2]; pzh = abs(e2[2]) * half
            pf0 = (n0[0] + a * e1[0]) * EPX[k] + (n0[1] + a * e1[1]) * EPY[k]
            pfh = abs(e2[0] * EPX[k] + e2[1] * EPY[k]) * half
            nmax = np.sqrt(1.0 + a * a + half * half)
            vmax = (S0[k] * (abs(pf0) + pfh)) ** 2 + (S1[k] * (abs(pz0) + pzh)) ** 2 + 0.0009
            T = K * np.sqrt(vmax) * nmax
            cc = c0 + a * c1
            if abs(c2) < 1e-12:
                if abs(cc) > T:
                    continue
                jlo, jhi = 0, m - 1
            else:
                b1 = (-T - cc) / c2; b2 = (T - cc) / c2
                if b1 > b2:
                    b1, b2 = b2, b1
                jlo = int(np.floor((b1 + half) / step)); jhi = int(np.ceil((b2 + half) / step))
                if jhi < 0 or jlo > m - 1:
                    continue
                jlo = max(jlo, 0); jhi = min(jhi, m - 1)
            for j in range(jlo, jhi + 1):
                b = -half + j * step
                nx = n0[0] + a * e1[0] + b * e2[0]; ny = n0[1] + a * e1[1] + b * e2[1]; nz = n0[2] + a * e1[2] + b * e2[2]
                nn = np.sqrt(nx * nx + ny * ny + nz * nz)
                d = (cc + b * c2) / nn
                cp = S0[k] * (nx * EPX[k] + ny * EPY[k]) / nn; cz = S1[k] * nz / nn
                v = cp * cp + cz * cz + 0.0009
                G[i, j] += np.exp(-d * d / (2 * v))
    return G


@jit
def scan_sphere(U, EPX, EPY, S0, S1, step):
    nt = int(np.pi / step) + 1
    best = np.full(nt, -1.0)
    bp = np.zeros(nt)
    for i in prange(nt):
        th = i * step
        st = np.sin(th)
        nphi = max(1, int(np.pi * st / step) + 1)      # half sphere in phi (n and -n are the same plane)
        for j in range(nphi):
            ph = j * np.pi / nphi
            nx = st * np.cos(ph); ny = st * np.sin(ph); nz = np.cos(th)
            s = 0.0
            for k in range(U.shape[0]):
                d = U[k, 0] * nx + U[k, 1] * ny + U[k, 2] * nz
                cp = S0[k] * (nx * EPX[k] + ny * EPY[k]); cz = S1[k] * nz
                v = cp * cp + cz * cz + 0.0009
                s += np.exp(-d * d / (2 * v))
            if s > best[i]:
                best[i] = s; bp[i] = ph
    return best, bp


def basis(n0):
    t = np.array([0.0, 0.0, 1.0]) if abs(n0[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(n0, t); e1 /= np.linalg.norm(e1)
    e2 = np.cross(n0, e1)
    return e1, e2


def score(U, EPX, EPY, S0, S1, n):
    d = U @ n
    v = (S0 * (n[0] * EPX + n[1] * EPY)) ** 2 + (S1 * n[2]) ** 2 + T_TOL ** 2
    return float(np.exp(-d * d / (2 * v)).sum()), v


def ang(a, b):
    return float(np.arccos(min(1.0, abs(float(np.dot(a, b)) / (np.linalg.norm(a) * np.linalg.norm(b))))))


def lsq_fit(U, EPX, EPY, S0, S1, n0):
    from scipy.optimize import least_squares
    _, v0 = score(U, EPX, EPY, S0, S1, n0)
    inl = np.abs(U @ n0) <= 3 * np.sqrt(v0)
    e1, e2 = basis(n0)

    def nvec(p):
        n = n0 + p[0] * e1 + p[1] * e2
        return n / np.linalg.norm(n)

    def resid(p):
        n = nvec(p)
        _, v = score(U[inl], EPX[inl], EPY[inl], S0[inl], S1[inl], n)
        return (U[inl] @ n) / np.sqrt(v)
    r = least_squares(resid, np.zeros(2), method="lm", xtol=1e-12, ftol=1e-12)
    return nvec(r.x), int(inl.sum()), bool(r.success)


def analyse(H, pv, phimet, n0, a0, do_global=True, half=None, step=None, gstep=None):
    half = GRID_HALF if half is None else half
    step = GRID_STEP if step is None else step
    gstep = GLOBAL_STEP if gstep is None else gstep
    U0 = H[:, 1:4] - pv[None, :]
    r = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    road = dph < ROAD + np.arcsin(np.minimum(1.0, W_C / r))
    n0 = n0 / np.linalg.norm(n0); a0 = a0 / np.linalg.norm(a0)
    n2 = np.cross(n0, a0); n2 /= np.linalg.norm(n2)
    win = road & (np.abs(U0 @ n2) <= W_C)
    phi = np.arctan2(H[:, 2], H[:, 1])
    EPX, EPY = -np.sin(phi), np.cos(phi)
    S0, S1 = H[:, 4], H[:, 5]
    sel = lambda m: (np.ascontiguousarray(U0[m]), np.ascontiguousarray(EPX[m]), np.ascontiguousarray(EPY[m]),  # noqa
                     np.ascontiguousarray(S0[m]), np.ascontiguousarray(S1[m]))
    W = sel(win)
    e1, e2 = basis(n0)
    t0 = time.time()
    log.info("window %d hits, road %d hits; fine scan %d^2 normals", int(win.sum()), int(road.sum()),
             int(round(2 * half / step)) + 1)
    if SELFCHECK:            # band accumulation against the direct sum on a small grid around n_F0
        Gd, _ = scan_grid(*W, n0, e1, e2, 0.004, step)
        Gb = scan_band(*W, n0, e1, e2, 0.004, step, 4.0)
        Gdd = np.array([[0.0]])
        m_ = Gb.shape[0]
        full = np.zeros((m_, m_))
        for ii in range(m_):     # recompute the direct grid fully (scan_grid keeps only the row maxima)
            for jj in range(m_):
                nv = n0 + (-0.004 + ii * step) * e1 + (-0.004 + jj * step) * e2
                full[ii, jj] = score(*W, nv / np.linalg.norm(nv))[0]
        del Gd, Gdd
        selfcheck = float(np.max(np.abs(full - Gb)) / np.max(full))
        log.info("selfcheck band vs direct (41x41 grid): max rel diff %.3g", selfcheck)
    G = scan_band(*W, n0, e1, e2, half, step, 4.0)
    i, j = np.unravel_index(int(np.argmax(G)), G.shape)
    best = G.max(1)
    a = -half + i * step; b = -half + j * step
    nb_ = n0 + a * e1 + b * e2; nb_ /= np.linalg.norm(nb_)
    t_fine = time.time() - t0
    nf, n_inl, ok = lsq_fit(*W, n0)
    out = dict(selfcheck_band_vs_direct=selfcheck if SELFCHECK else None, n_window=int(win.sum()), n_road=int(road.sum()), score_F0=score(*W, n0)[0], score_opt=float(best[i]),
               dn_F0_opt_mrad=1e3 * ang(n0, nb_), dn_F0_fit_mrad=1e3 * ang(n0, nf), dn_opt_fit_mrad=1e3 * ang(nb_, nf),
               opt_on_grid_edge=bool(i in (0, len(best) - 1) or j in (0, len(best) - 1)), n_inliers_fit=n_inl,
               half=half, step=step,
               fit_success=ok, t_fine_s=t_fine, n_opt=nb_.tolist(), n_fit=nf.tolist(), n_F0=n0.tolist())
    if do_global:
        t0 = time.time()
        R_ = sel(road)
        log.info("fine scan %.1f s; global scan step %.4g", t_fine, gstep)
        GG = scan_band(*R_, n0, e1, e2, GLOBAL_HALF, gstep, 4.0)
        gi, gj = np.unravel_index(int(np.argmax(GG)), GG.shape)
        ng = n0 + (-GLOBAL_HALF + gi * gstep) * e1 + (-GLOBAL_HALF + gj * gstep) * e2
        ng /= np.linalg.norm(ng)
        sF0_road = score(*R_, n0)[0]
        out.update(global_best_score_road=float(GG[gi, gj]), score_F0_road=sF0_road, dn_F0_global_mrad=1e3 * ang(n0, ng),
                   global_better_elsewhere=bool(gb[k] > sF0_road and ang(n0, ng) > half), t_global_s=time.time() - t0)
    if FULL_SPHERE:          # closing check of the ±50 deg restriction: direct sum over the whole half sphere, all road hits
        t0 = time.time()
        R_ = sel(road)
        sb, sp = scan_sphere(*R_, FULL_SPHERE)
        k = int(np.argmax(sb)); th = k * FULL_SPHERE
        ns = np.array([np.sin(th) * np.cos(sp[k]), np.sin(th) * np.sin(sp[k]), np.cos(th)])
        out.update(sphere_step=FULL_SPHERE, sphere_best_score=float(sb[k]), dn_F0_sphere_mrad=1e3 * ang(n0, ns),
                   sphere_best_outside_50deg=bool(ang(n0, ns) > np.arctan(GLOBAL_HALF)),
                   sphere_best_minus_global_best=float(sb[k] - out.get("global_best_score_road", np.nan)),
                   t_sphere_s=time.time() - t0)
    out["agree"] = bool(out["dn_F0_opt_mrad"] < 1.0 and out["dn_F0_fit_mrad"] < 1.0)
    return out


def pu_trials(files, n_want):
    """First n_want trials (file order) with an aligned F0 candidate at R04; rebuilds the hit pool from the S6 dumps."""
    from acts.stage4 import run_stage4 as RS
    from acts.stage4.finder import chain_inputs as CI
    from acts.stage4.finder import pu_inputs as PI
    got = 0
    for p in files:
        z = np.load(p, allow_pickle=False)
        meta = json.loads(str(z["meta_json"]))
        job = meta["job"]
        assert job["rho"] == 1 and job["dump_events"] == job["n_events"], "need rho = 1 jobs with dumps of every event"
        streams = np.random.SeedSequence(job["seed"]).spawn(job["n_events"])
        R04 = np.unpackbits(z["cand.rungs"], axis=1)[:, 3].astype(bool)
        ctr = z["cand.trial"]; cidx = z["cand.idx"]
        cache = {}
        for t in range(int(z["n_trials"])):
            if not R04[ctr == t].any():
                continue
            ie = int(z["trials.ev"][t]) - int(job["ev0"])
            if ie not in cache:
                pre = f"dump.{ie}_0."
                n = len(z[pre + "sid"])
                ev = np.zeros((n, 13))
                ev[:, 0] = z[pre + "sid"]; ev[:, 1:4] = z[pre + "xyz"]; ev[:, 4:6] = z[pre + "s01"]
                ev[:, 6] = z[pre + "flag"]; ev[:, 7] = z[pre + "vp"]; ev[:, 8] = z[pre + "particle"]
                ev[:, 9] = z[pre + "gen"]; ev[:, 10] = z[pre + "vsec"]; ev[:, 11] = z[pre + "dE"]; ev[:, 12] = z[pre + "t"]
                rs = np.random.default_rng(streams[ie])
                part = CI.prepare_event(ev, z[pre + "tru"], z[pre + "vz"].astype(np.float64), 0, rs, ratios=None)
                pv_chk = PI.lum_pv(rs)
                cache = {ie: (part, pv_chk)}
            part, pv_chk = cache[ie]
            pv = z["trials.pv"][t].astype(np.float64)
            m = (ctr == t) & R04
            k = np.where(m)[0][np.argmin(cidx[m])]
            yield dict(file=Path(p).name, trial=t, ev=int(z["trials.ev"][t]), road=int(z["trials.road"][t]),
                       n_road_stored=int(z["trials.n_road"][t]),
                       pv_reproduced=bool(np.allclose(pv_chk, pv)), H=part["H"], pv=pv,
                       phimet=float(z["trials.phimet"][t]), n0=z["cand.normal"][k].astype(np.float64),
                       a0=z["cand.axis"][k].astype(np.float64), road_cfg=float(meta["finder_cfg"]["road"]))
            got += 1
            if got >= n_want:
                z.close()
                return
        z.close()


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pu"])
    ap.add_argument("--files", required=True)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--skip", type=int, default=0, help="skip the first K selected trials (job splitting)")
    ap.add_argument("--no-global", action="store_true")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--half", type=float, default=None, help="timing tests only (default 0.3 rad)")
    ap.add_argument("--step", type=float, default=None, help="timing tests only (default 0.2 mrad)")
    ap.add_argument("--gstep", type=float, default=None, help="timing tests only (default 5 mrad)")
    ap.add_argument("--selfcheck", action="store_true")
    ap.add_argument("--full-sphere", type=float, default=0.0, help="also a direct half-sphere scan at this step (rad)")
    a = ap.parse_args()
    global SELFCHECK, FULL_SPHERE
    SELFCHECK = a.selfcheck
    FULL_SPHERE = a.full_sphere
    res = []
    for i, tr in enumerate(pu_trials(a.files.split(","), a.skip + a.n)):
        if i < a.skip:
            continue
        assert abs(tr["road_cfg"] - ROAD) < 1e-12
        t0 = time.time()
        r = analyse(tr["H"], tr["pv"], tr["phimet"], tr["n0"], tr["a0"], do_global=not a.no_global, half=a.half, step=a.step,
                    gstep=a.gstep)
        r.update({k: tr[k] for k in ("file", "trial", "ev", "road", "pv_reproduced", "n_road_stored")},
                 t_total_s=time.time() - t0)
        r["pool_reproduced"] = bool(r["n_road"] == r["n_road_stored"] and r["pv_reproduced"])
        log.info("trial %s/%d: dn(F0,opt) %.3f mrad, dn(F0,fit) %.3f mrad, window %d, %.1f s", tr["file"], tr["trial"],
                 r["dn_F0_opt_mrad"], r["dn_F0_fit_mrad"], r["n_window"], r["t_total_s"])
        res.append(r)
    out = Path(os.environ.get("QV2_OUT_DIR", "."))
    summ = dict(mode=a.mode, n=len(res), n_agree=sum(r["agree"] for r in res),
                definition=__doc__.split("Definition")[1].split("BLINDING")[0], trials=res)
    (out / f"{a.tag}.json").write_text(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
