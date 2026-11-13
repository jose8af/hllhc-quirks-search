"""Production F0 finder (fast; G2a).  Same selection as acts/stage4/probes/f1r_finder.trial(); see README.md for every
difference.  Env: theory_track pixi env (numba), as the reference probe and plan §1.8.

API
  res = find(H, sid, pv, phimet, cfg=Config(), INT=None, rho=1.0, store='all')
    H      (n, >=6) measurements: col 1-3 global x, y, z [mm], col 4-5 local sigma (u, v) [mm] (f1r 12-column format)
    sid    (n,) global surface ids of surfaces_s3.json (non-barrel-counting surfaces are ignored)
    pv     (3,) PV [mm];  phimet: MET direction [rad]
    INT    (n,) interaction ids (truth, diagnostics only): thinning weights (f1r thin_weights, rung N_L2 >= L with
           N_IT2 >= 3) of the top-ranked candidate (thin_mode='top', the f1r rho = 1 behaviour) or of every stored
           candidate (thin_mode='all', the f1r rho > 1 behaviour; unaffordable at the full density, see README)
    store  'all'   every kept candidate with N_L2 >= 4 (reference output),
           'loose' only candidates passing the loosest ladder rung (N_IT2 >= 3 and N_IP2 >= 4)
  returns dict(cands=V (structured numpy array, rank order), hits=CSR (offsets, road-hit indices), counters, timers)
"""
import json
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import kernels as K

TT = Path(__file__).resolve().parents[3]
S = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
NS = len(S)
LAYERS = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']
LC_OF = np.full(NS, -1, np.int64)
SIDE_OF = np.zeros(NS, np.int64)
for _i, _s in enumerate(S):
    for _k, _p in enumerate(LAYERS):
        if _s['name'] == _p or _s['name'].startswith(_p + '_'):
            LC_OF[_i] = _k
            SIDE_OF[_i] = 1 if _s['name'].endswith('_in') else (2 if _s['name'].endswith('_out') else 0)
SID = {s['name']: i for i, s in enumerate(S)}
# local surface index j (0..15) of a global surface id
JLOC_OF = np.full(NS, -1, np.int64)
for _i in range(NS):
    _k = LC_OF[_i]
    if _k < 0:
        continue
    JLOC_OF[_i] = _k if _k < 4 else 4 + 2 * (_k - 4) + (SIDE_OF[_i] - 1)
R_NOM = np.zeros(16)
for _i in range(NS):
    if JLOC_OF[_i] >= 0:
        R_NOM[JLOC_OF[_i]] = S[_i]['p0'] * 10.0
RUNGS = [5, 6, 7, 8, 9, 10]

VAR_NAMES = ['nit2', 'not2', 'nl2', 'not2h', 'nl2h', 'nl1', 'chi2ndf', 'nhit', 'dw_old', 'dw_core', 'nip2', 'n2s2',
             'chi2_core', 'n_core', 'nz']


@dataclass
class Config:
    w_c: float = 75.0          # mm, collection window (plan §2.2 item 1)
    road: float = 0.25         # rad, delta_road
    t_tol: float = 0.030       # mm, plane-thickness tolerance
    tseed: int = 6             # seed N_L2 threshold (fix-R1 value)
    iters: int = 3             # refit iterations
    # implementation-only parameters (no effect on the output, only on speed)
    arc_mm: tuple = (4.0, 8.0, 12.0, 15.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0)
    arc_mm_refit: tuple = (12.0, 24.0, 36.0, 45.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 200.0, 200.0, 200.0, 200.0, 200.0,
                           200.0)   # coarser bins for the refit gather (index 2)
    dz_mm: tuple = (1.0, 2.0, 3.0, 4.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0)
    dfac: float = 1.5          # refit gather margin delta = max(dmin, dfac * sigma_seed)
    dmin: float = 2e-4
    seed_order: tuple = (3, 2, 4, 5, 6, 7, 8, 9, 1, 0)   # layer order of the early-terminated seed score
    early: bool = True         # seed-score early termination (seed N_L2 stored as a lower bound)
    seed_n2_exact: bool = False  # recompute the exact seed N_L2 for stored candidates


def road_select(H, sid, pv, phimet, cfg):
    """Reference road (f1r_finder.trial, first lines), restricted to the barrel counting surfaces."""
    keep = LC_OF[sid] >= 0
    U0 = H[:, 1:4] - pv[None, :]
    r0 = np.hypot(U0[:, 0], U0[:, 1])
    dph = np.abs((np.arctan2(U0[:, 1], U0[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    m = keep & (dph < cfg.road + np.arcsin(np.minimum(1.0, cfg.w_c / r0)))
    return m, U0


def build_index(U, CX, CY, J, S0, S1, phimet, cfg, arcs=None):
    arcs = cfg.arc_mm if arcs is None else arcs
    n = len(U)
    psi = np.arctan2(U[:, 1], U[:, 0])
    r = np.hypot(U[:, 0], U[:, 1])
    un = np.sqrt(U[:, 0] ** 2 + U[:, 1] ** 2 + U[:, 2] ** 2)
    SF = np.zeros((16, 8))
    SI = np.zeros((16, 7), np.int64)
    gb = np.empty(n, np.int64)
    boff = 0
    ce_l = []
    se_l = []
    for j in range(16):
        mj = J == j
        nb = max(8, int(np.ceil(2 * np.pi * R_NOM[j] / arcs[j])))
        bw = 2 * np.pi / nb
        b = np.minimum(np.floor((psi[mj] + np.pi) / bw).astype(np.int64), nb - 1)
        b = np.maximum(b, 0)
        gb[mj] = boff + b
        edges = -np.pi + bw * np.arange(nb + 1)
        ce_l.append(np.cos(edges)); se_l.append(np.sin(edges))
        if mj.any():
            rmin = r[mj].min(); rmax = r[mj].max(); umax = un[mj].max()
            s0 = S0[mj][0]; s1 = S1[mj][0]
            assert np.all(S0[mj] == s0) and np.all(S1[mj] == s1), 'per-surface constant sigma assumed by the index'
        else:
            rmin = rmax = R_NOM[j]; umax = 0.0; s0 = s1 = 0.0
        # road bins: contiguous arc around phimet; verified against the hits, else every bin
        hw = cfg.road + np.arcsin(min(1.0, cfg.w_c / max(rmin, 1e-9))) + 2 * bw
        if hw >= np.pi:
            kf, kn = 0, nb
        else:
            kf = int(np.floor((K.wrap(phimet - hw) + np.pi) / bw)) % nb
            kn = int(np.ceil(2 * hw / bw)) + 2
            if kn >= nb or (mj.any() and np.any(((b - kf) % nb) >= kn)):
                kf, kn = 0, nb
        if mj.any():
            zmin = U[mj, 2].min(); zmax = U[mj, 2].max()
        else:
            zmin = zmax = 0.0
        dz = cfg.dz_mm[j]
        nzc = int(np.floor((zmax - zmin) / dz)) + 1
        SF[j] = (rmin, rmax, umax, s0, s1, bw, zmin, dz)
        SI[j] = (nb, boff, boff + j, kf, kn, 0, nzc)
        boff += nb
    order = np.lexsort((U[:, 2], gb))
    bstart = np.searchsorted(gb[order], np.arange(boff + 1)).astype(np.int64)
    # 2-D (phi bin, z cell) grid: CS[coff_j + k (nzc_j + 1) + c] = first position of cell c of bin k of surface j
    jpos = J[order]
    cell = np.clip(np.floor((U[order, 2] - SF[jpos, 6]) / SF[jpos, 7]).astype(np.int64), 0, SI[jpos, 6] - 1)
    MAXC = int(SI[:, 6].max()) + 1
    key = gb[order] * MAXC + cell
    qk = []; coff = 0
    for j in range(16):
        nb, bo, nzc = SI[j, 0], SI[j, 1], SI[j, 6]
        SI[j, 5] = coff
        qk.append(((bo + np.arange(nb))[:, None] * MAXC + np.arange(nzc + 1)[None, :]).ravel())
        coff += nb * (nzc + 1)
    CS = np.searchsorted(key, np.concatenate(qk)).astype(np.int64)
    P = np.ascontiguousarray(np.vstack([U[order, 0], U[order, 1], U[order, 2], CX[order], CY[order], un[order]]))
    pid = order.astype(np.int64)
    ce = np.concatenate(ce_l); se = np.concatenate(se_l)
    PRE = np.where(K.SURF_LC >= 7, 60.0, 5.0)
    PJ = J[order].astype(np.int64)
    # non-empty bins per surface (all bins of a surface are scanned by the refit gather; empty ones skipped)
    cnt = np.diff(bstart)
    NEB = []; NEO = [0]
    for j in range(16):
        nb, bo = SI[j, 0], SI[j, 1]
        ks = np.nonzero(cnt[bo:bo + nb])[0]
        NEB.append(ks); NEO.append(NEO[-1] + len(ks))
    NEB = np.concatenate(NEB).astype(np.int64); NEO = np.array(NEO, np.int64)
    return P, CS, pid, bstart, ce, se, SF, SI, PRE, PJ, NEB, NEO


def thin_weights(hidx, LC, SD, INT, rho):
    """Copy of f1r_finder.thin_weights (P(pass rung L | each interaction kept with q = 1/rho), k_min)."""
    NL = 10
    ints, inv = np.unique(INT[hidx], return_inverse=True)
    m = len(ints)
    C = np.zeros((m, NL, 3), np.int64)
    np.add.at(C, (inv, LC[hidx], SD[hidx]), 1)
    C = C.reshape(m, -1)
    q = 1.0 / rho
    if m <= 12:
        masks = np.arange(1 << m, dtype=np.int64)
        Bm = ((masks[:, None] >> np.arange(m)) & 1).astype(np.int64)
        prob = None
    else:
        rng = np.random.default_rng(12345)
        Bm = (rng.random((20000, m)) < q).astype(np.int64)
        prob = 1.0 / len(Bm)
    cnt = (Bm @ C).reshape(len(Bm), NL, 3)
    cr = np.concatenate([cnt[:, :4, 0], np.minimum(cnt[:, 4:, 1], cnt[:, 4:, 2])], axis=1)
    nit2 = (cr[:, :4] >= 2).sum(1); nl2 = (cr >= 2).sum(1)
    size = Bm.sum(1)
    wts = (q ** size) * ((1 - q) ** (m - size)) if prob is None else np.full(len(Bm), prob)
    res = {}
    for L in RUNGS:
        ok = (nit2 >= 3) & (nl2 >= L)
        res[str(L)] = dict(p=float(wts[ok].sum()), kmin=int(size[ok].min()) if ok.any() else -1)
    return res, m


def find(H, sid, pv, phimet, cfg=None, INT=None, SIG=None, rho=1.0, store='all', want_hits=False, want_seeds=False,
         thin_mode='top', want_csr=False):
    cfg = cfg or Config()
    T = {}
    t0 = time.perf_counter()
    m, U0 = road_select(H, sid, pv, phimet, cfg)
    U = np.ascontiguousarray(U0[m]); X = np.ascontiguousarray(H[m, 1]); Y = np.ascontiguousarray(H[m, 2])
    S0 = np.ascontiguousarray(H[m, 4]); S1 = np.ascontiguousarray(H[m, 5])
    sd = sid[m]; LC = LC_OF[sd]; SD = SIDE_OF[sd]; J = JLOC_OF[sd]
    rH = np.hypot(X, Y); CX = X / rH; CY = Y / rH
    phiU = np.arctan2(U[:, 1], U[:, 0]); etaU = np.arcsinh(U[:, 2] / np.hypot(U[:, 0], U[:, 1]))
    A_idx = np.where(sd == SID['TBPX_L4'])[0]
    P, CS, pid, bstart, ce, se, SF, SI, PRE, PJ, NEB, NEO = build_index(U, CX, CY, J, S0, S1, phimet, cfg)
    # second (coarser) index for the refit gather; the refit's hit ids are positions in this index
    (P2, CS2, pid2, bstart2, ce2, se2, SF2, SI2, PRE2, PJ2, NEB2,
     NEO2) = build_index(U, CX, CY, J, S0, S1, phimet, cfg, cfg.arc_mm_refit)
    PLC2 = K.SURF_LC[PJ2]; PSD2 = K.SURF_SD[PJ2]
    T['road_index'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    oa, ob, on, ntrip = K.seeds_fast(U, phiU, etaU, A_idx, pid, pid, P, CS, bstart, ce, se, SF, SI, phimet, cfg.road,
                                     cfg.w_c, cfg.tseed, cfg.t_tol, cfg.early, np.array(cfg.seed_order, np.int64))
    T['seeds'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    NL2, NIT2, CHI, NSEL, NF, AX, N0, A0, DM, hoff, hits, n_reg, n_full = K.refit_all(
        U, LC, oa, ob, P2, CS2, PJ2, PLC2, PSD2, pid2, bstart2, ce2, se2, SF2, SI2, PRE2, NEB2, NEO2, cfg.w_c, cfg.iters,
        cfg.t_tol,
        cfg.dfac, cfg.dmin)
    T['refit'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    fast = np.where(NL2 >= 4)[0]
    order = fast[np.lexsort((CHI[fast], -NL2[fast]))]          # stable: reference (-N_L2, chi2/ndf) sort
    keep = K.dedup(NF, order, 2.1e-3)
    kept = order[keep[order]]
    T['dedup'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    V = K.cand_vars(U, CX, CY, S0, S1, LC, SD, hoff, hits, kept, NF, AX, cfg.t_tol, pid2, store == 'loose')
    sel = V[:, 2] >= 4
    if store == 'loose':
        sel &= (V[:, 0] >= 3) & (V[:, 10] >= 4)
    kept = kept[sel]; V = V[sel]
    seed_n2 = on[kept].astype(np.int64)
    if cfg.seed_n2_exact and len(kept):
        seed_n2 = K.seed_n2_exact(U, oa[kept], ob[kept], P, CS, bstart, ce, se, SF, SI, cfg.w_c, cfg.t_tol, cfg.tseed)
    dphi = np.abs((np.arctan2(AX[kept, 1], AX[kept, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    T['vars'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    thin = None
    if INT is not None and len(kept) and thin_mode != 'none':
        # f1r_finder.trial semantics: the top-ranked candidate (rho = 1) or every stored candidate (thin_mode='all',
        # the f1r rho > 1 behaviour; 2e4-subset MC, ~15-25 ms per set: NOT affordable at the full density, see
        # G2A_REPORT.md -- the production rho = 2 weights need the plan §4.1 step 3b methods / sub-sampling strata)
        INTm = INT[m]
        SIGm = SIG[m] if SIG is not None else np.zeros(len(U), np.int64)
        thin = []
        for r_, c in enumerate(kept):
            if V[r_, 2] >= 5 and (thin_mode == 'all' or r_ == 0):
                h = pid2[hits[hoff[c]:hoff[c + 1]]]
                if np.sum(SIGm[h] > 0) == 0:
                    thin.append((r_,) + thin_weights(h, LC, SD, INTm, rho))
            if thin_mode != 'all':
                break
    T['thin'] = time.perf_counter() - t0
    out = dict(n_road=int(m.sum()), n_trip=int(ntrip), n_refit=int(len(oa)), n_fast=int(len(fast)),
               n_kept_all=int(keep.sum()), n_regather=int(n_reg), n_fullscan=int(n_full),
               vars={k: V[:, i] for i, k in enumerate(VAR_NAMES)}, seed_n2=seed_n2, normal=NF[kept], axis=AX[kept],
               dphi_met=dphi, seed_ab=np.c_[oa[kept], ob[kept]], thin=thin, times_s=T,
               t_tot=sum(T.values()))
    if want_hits:
        out['hits'] = [np.sort(pid2[hits[hoff[c]:hoff[c + 1]]]) for c in kept]
        out['road_mask'] = m
    if want_csr:
        # Phase A (production): the same hit lists as want_hits, as one CSR (offsets, ascending road indices)
        out['csr_off'], out['csr_hits'] = K.csr_hits(hoff, hits, kept, pid2)
        out['road_mask'] = m
    if want_seeds:
        out['seeds_all'] = np.c_[oa, ob]
    return out
