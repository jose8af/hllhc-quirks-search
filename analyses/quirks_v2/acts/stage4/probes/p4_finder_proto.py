"""p4_finder_proto.py -- Stage-4 PROBE (E9, plan turn): CPU and combinatorics of a baseline PV-plane finder (plan §2, F0)
on digitised PU-200 events (with and without the injected quirk pair).  NOT the final finder; parameters are placeholders,
nothing here is tuned on signal (5 events per file are far too few for that anyway).

F0 prototype:
  hits u_i = x_i - PV (PV = Stage-3 vertex, truth; the plan smears it).  Per-hit out-of-plane error for a normal n:
  sigma_n^2 = (n.a)^2 s_a^2 + (n.b)^2 s_b^2 with (a, b) = (phi_hat, z_hat) on cylinders, (r_hat, phi_hat) on discs.
  1. seeds: pairs (a in TBPS_L3_in, b in TBPS_L1_in) and (a in TBPS_L2_in, b in TBPX_L4) with |dphi| < 0.15, |deta| < 0.15;
     n = unit(u_a x u_b); skip if sin(angle(u_a, u_b)) < 2e-3 (degenerate ribbon).
  2. collect: hits with |n.u| < 3 sqrt(sigma_n^2 + (sig_seed |u|)^2), sig_seed = 0.5 mm / (|u_a| sin angle), on the seed side
     (u.axis > 0), within |u.n2| < 5 cm of the axis.  score = (# layers with >= 2 hits, # layers with >= 1 hit).
  3. for seeds with >= 6 layers hit: 3 x [weighted PV-constrained plane fit -> recollect with 3 sigma_n].
     Report chi2/ndf, t_est (weighted rms out-of-plane), width dw, N_L2, N_L1, and signal-hit purity/efficiency (truth flag).
Run (theory_track):  pixi run python acts/stage4/probes/p4_finder_proto.py data/acts_stage4/p2/meas_sig_pu_L1_BM_c00.npz
Output: data/acts_stage4/p4/p4_<stem>.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit

TT = Path(__file__).resolve().parents[3]
OUT = TT / 'data' / 'acts_stage4' / 'p4'
OUT.mkdir(parents=True, exist_ok=True)
S = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']


DISC_BASES = sorted({s['name'].replace('_in', '').replace('_out', '').replace('_PS', '').replace('_2S', '')
                     for s in S if s['type'] == 1 and s['kind'] in ('IT', 'PS', '2S')})


def layer_of(s):
    n = s['name']
    for k, p in enumerate(['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']):
        if n.startswith(p):
            return k
    if s['kind'] in ('IT', 'PS', '2S'):        # discs: one counting layer per disc (in/out, PS/2S parts together)
        base = n.replace('_in', '').replace('_out', '').replace('_PS', '').replace('_2S', '')
        return 10 + DISC_BASES.index(base)
    return -1


LAY = np.array([layer_of(s) for s in S])
_u = {v: i for i, v in enumerate(sorted(set(LAY[LAY >= 0])))}
LAYC = np.array([_u.get(v, -1) for v in LAY])          # compact counting-layer index, -1 = not counted (BTL, ETL, T3V)
STYPE = np.array([s['type'] for s in S])
NAMES = [s['name'] for s in S]
SID = {n: i for i, n in enumerate(NAMES)}


@njit(cache=True)
def sig_n(n, x, y, typ, s0, s1):
    """out-of-plane error of one hit for unit normal n (global hit position x, y relative to the beam line)."""
    r = np.hypot(x, y)
    cx, cy = x / r, y / r
    if typ == 0:     # cylinder: s0 along phi_hat, s1 along z
        a = -n[0] * cy + n[1] * cx
        b = n[2]
        return np.sqrt(a * a * s0 * s0 + b * b * s1 * s1)
    a = n[0] * cx + n[1] * cy             # disc: s0 along r_hat; s1 = sigma_phi -> r sigma_phi along phi_hat
    b = -n[0] * cy + n[1] * cx
    return np.sqrt(a * a * s0 * s0 + b * b * (s1 * r) ** 2)


@njit(cache=True)
def run_seeds(U, X, Y, TYP, S0, S1, LC, nlay, A, B, dphi_max, deta_max, phiU, etaU):
    out = []
    nseed = 0
    for ia in A:
        for ib in B:
            dp = phiU[ia] - phiU[ib]
            if dp > np.pi:
                dp -= 2 * np.pi
            if dp < -np.pi:
                dp += 2 * np.pi
            if abs(dp) > dphi_max or abs(etaU[ia] - etaU[ib]) > deta_max:
                continue
            ua = U[ia]; ub = U[ib]
            c = np.cross(ua, ub)
            na, nb = np.linalg.norm(ua), np.linalg.norm(ub)
            sn = np.linalg.norm(c) / (na * nb)
            if sn < 2e-3:
                continue
            nseed += 1
            n = c / np.linalg.norm(c)
            axis = (ua / na + ub / nb); axis = axis / np.linalg.norm(axis)
            n2 = np.cross(n, axis)
            sseed = 0.5 / (na * sn)
            cnt = np.zeros(nlay, np.int32)
            for i in range(U.shape[0]):
                if LC[i] < 0:
                    continue
                d = U[i, 0] * n[0] + U[i, 1] * n[1] + U[i, 2] * n[2]
                ui = np.sqrt(U[i, 0] ** 2 + U[i, 1] ** 2 + U[i, 2] ** 2)
                if U[i, 0] * axis[0] + U[i, 1] * axis[1] + U[i, 2] * axis[2] <= 0:
                    continue
                if abs(U[i, 0] * n2[0] + U[i, 1] * n2[1] + U[i, 2] * n2[2]) > 50.0:
                    continue
                sg = sig_n(n, X[i], Y[i], TYP[i], S0[i], S1[i])
                if abs(d) < 3 * np.sqrt(sg * sg + (sseed * ui) ** 2):
                    cnt[LC[i]] += 1
            n1 = 0; n2c = 0
            for k in range(nlay):
                if cnt[k] >= 1:
                    n1 += 1
                if cnt[k] >= 2:
                    n2c += 1
            if n1 >= 6:
                out.append((ia, ib, n1, n2c))
    return out, nseed


def refit(U, X, Y, TYP, S0, S1, LC, n, axis, iters=3):
    """PV-constrained weighted plane fit (smallest eigenvector of sum w u u^T), recollect at 3 sigma_n."""
    for _ in range(iters):
        sg = np.array([sig_n(n, X[i], Y[i], TYP[i], S0[i], S1[i]) for i in range(len(U))])
        d = U @ n
        sel = (np.abs(d) < 3 * np.maximum(sg, 1e-4)) & ((U @ axis) > 0) & (LC >= 0) & (np.abs(U @ np.cross(n, axis)) < 50.0)
        if sel.sum() < 4:
            return None
        w = 1.0 / sg[sel] ** 2
        M = (U[sel] * w[:, None]).T @ U[sel]
        ev, evec = np.linalg.eigh(M)
        n = evec[:, 0] if evec[:, 0] @ n >= 0 else -evec[:, 0]
    sg = np.array([sig_n(n, X[i], Y[i], TYP[i], S0[i], S1[i]) for i in range(len(U))])
    d = U @ n
    sel = (np.abs(d) < 3 * np.maximum(sg, 1e-4)) & ((U @ axis) > 0) & (LC >= 0) & (np.abs(U @ np.cross(n, axis)) < 50.0)
    w = 1.0 / sg[sel] ** 2
    chi2 = float(np.sum(d[sel] ** 2 * w)); ndf = int(sel.sum()) - 2
    lc = LC[sel]
    nl1 = len(set(lc)); nl2 = int(np.sum(np.bincount(lc) >= 2))
    t_est = float(np.sqrt(np.sum(d[sel] ** 2 * w) / np.sum(w)))
    dw = float(np.std(U[sel] @ np.cross(n, axis)))
    return dict(n=n.tolist(), sel=np.where(sel)[0], chi2ndf=chi2 / max(ndf, 1), t_est_um=1e3 * t_est, dw_mm=dw, nl1=nl1, nl2=nl2, nhit=int(sel.sum()))


def event(h, vtx, keep_signal=True):
    if not keep_signal:
        h = h[h[:, 6] == 0]
    sid = h[:, 0].astype(int)
    U = h[:, 1:4] - vtx[None, :3]
    X, Y = h[:, 1], h[:, 2]
    TYP = STYPE[sid]; LC = LAYC[sid]
    S0, S1 = h[:, 4], h[:, 5]
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    t0 = time.time()
    cands = []; nseed_tot = 0
    for la, lb in (('TBPS_L3_in', 'TBPS_L1_in'), ('TBPS_L2_in', 'TBPX_L4')):
        A = np.where(sid == SID[la])[0]; B = np.where(sid == SID[lb])[0]
        out, ns = run_seeds(U, X, Y, TYP, S0, S1, LC, LAYC.max() + 1, A, B, 0.15, 0.15, phiU, etaU)
        cands += out; nseed_tot += ns
    t_seed = time.time() - t0
    cands.sort(key=lambda c: (-c[3], -c[2]))
    fits = []
    for ia, ib, n1, n2 in cands[:20]:
        n = np.cross(U[ia], U[ib]); n /= np.linalg.norm(n)
        axis = U[ia] / np.linalg.norm(U[ia]) + U[ib] / np.linalg.norm(U[ib]); axis /= np.linalg.norm(axis)
        f = refit(U, X, Y, TYP, S0, S1, LC, n, axis)
        if f is None:
            continue
        fl = h[f['sel'], 6]
        f['n_sig_in'] = int(np.sum(fl > 0)); f['n_sig_tot'] = int(np.sum(h[:, 6] > 0)); f.pop('sel')
        fits.append(f)
    fits.sort(key=lambda f: (-f['nl2'], f['chi2ndf']))
    return dict(n_hits=len(h), n_seeds=nseed_tot, n_cand_ge6=len(cands), t_seed_s=round(t_seed, 2),
                t_total_s=round(time.time() - t0, 2), best=fits[0] if fits else None,
                top3=[{k: f[k] for k in ('nl1', 'nl2', 'nhit', 'chi2ndf', 't_est_um', 'dw_mm', 'n_sig_in')} for f in fits[:3]])


if __name__ == '__main__':
    f = Path(sys.argv[1])
    d = np.load(f)
    evs = sorted([k for k in d.files if k.startswith('ev')], key=lambda k: int(k[2:]))
    res = dict(file=str(f), events=[])
    event(d[evs[0]][:2000], d['vtx'][0])      # numba compile
    for i, k in enumerate(evs):
        h = d[k]; vtx = d['vtx'][i]
        r_sig = event(h, vtx, True)
        r_pu = event(h, vtx, False)
        res['events'].append(dict(sig_pu=r_sig, pu_only=r_pu))
        b = r_sig['best']; bp = r_pu['best']
        print(i, 'hits', r_sig['n_hits'], 'seeds', r_sig['n_seeds'], 'cand>=6L', r_sig['n_cand_ge6'], 't', r_sig['t_total_s'], 's | best sig+PU:',
              None if b is None else (b['nl1'], b['nl2'], b['nhit'], round(b['chi2ndf'], 2), round(b['t_est_um'], 1), round(b['dw_mm'], 2), f"{b['n_sig_in']}/{b['n_sig_tot']}"),
              '| PU-only cand>=6L', r_pu['n_cand_ge6'], 'best', None if bp is None else (bp['nl1'], bp['nl2'], bp['nhit'], round(bp['chi2ndf'], 2), round(bp['dw_mm'], 2)))
    (OUT / f'p4_{f.stem}.json').write_text(json.dumps(res, indent=1, default=float))
