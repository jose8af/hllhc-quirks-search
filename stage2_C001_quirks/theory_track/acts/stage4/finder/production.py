"""Production per-trial processing for PU-only trials (rho = 1 and rho = 2): finder -> distinct-hit-set groups ->
full-set rung flags -> (rho > 1) in-job thinning weights -> per-trial rung tables + the stored records of the storage
policy (acts/stage4/WP_RULE.md §S).  Signal-blind; truth (interaction ids) enters only the weights and diagnostics.

Rung columns (RUNGS, 43): the cumulative F0 ladder of plan §2.5 item 3 (R01-R14), F0 x dE/dx (F0e*), the fallback F0
parts FB0-FB4 and FB_k x dE/dx (plan §2.6), and the N_L2 diagnostic rungs of the fix-R1 pilot (L2>=*).  F1 h/o and the
SR-T time tag are NOT in-job (plan §4.1 step 3b: factorised at rho = 1 from the stored records).

SR-T in-job first factor (WP_RULE.md §1.4, §6.2; fix WP_RULE R2 B-2): with btl=(B, INT_B) the same 43 columns are also
computed AND ">= 1 in-band BTL hit" (RUNGS_T; row keys *_T, cand keys btl_*, w_T): the factor P(r and BTL-present) of
the SR-T factorisation P(r and BTL-present) x P(late).  The time window [t_min, dt_acc] and the out-of-time overlay
enter only P(late) (offline, B1 + overlay; t_min is fixed FROM B1, so it cannot be applied in-job).  btl=None leaves
every output of the 43 columns bit-identical and adds no key.

ρ = 1: per trial, per rung: N_pass (candidates), N_grp (distinct hit-set groups with >= 1 passing member).
ρ = 2: additionally S_uni = sum over candidates of w_r and S_ded = sum over groups of max_member w_r (Horvitz-Thompson
over the pre-declared sub-sampling of the per-subset families), and the IS variance of each.
"""
import time
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import chi2 as CHI2

from . import finder as FF
from . import weights as WG

RUNGS = (['R01_IP2>=4', 'R02_IP2>=5', 'R03_IP2>=6', 'R04_IP2>=7', 'R05_w<37.5', 'R06_w<18.75', 'R07_w<9.4',
          'R08_w<4.7', 'R09_p>1e-3', 'R10_p>0.01', 'R11_p>0.05', 'R12_2S2>=1', 'R13_2S2>=2', 'R14_2S2>=3',
          'F0e>1.3', 'F0e>1.6', 'F0e>2.0'] + ['FB%d' % k for k in range(5)] +
         ['FB%de>%g' % (k, e) for k in range(5) for e in (1.3, 1.6, 2.0)] + ['L2>=%d' % L for L in range(5, 11)])
NR = len(RUNGS)                                     # 43
# column maps from the weight kernels to RUNGS
MAP_DP = {0: 0, 1: 1, 2: 2, 3: 3, 37: 4, 38: 5, 39: 6, 40: 7, 41: 8, 42: 9}          # RUNGS idx -> COUNT_COLS idx
MAP_IS = {**{4 + k: k for k in range(10)}, 14: 10, 15: 11, 16: 12, **{17 + k: 13 + k for k in range(5)},
          **{22 + k: 18 + k for k in range(15)}}                                        # RUNGS idx -> SUB_COLS idx
RUNGS_T = [n + '&BTL' for n in RUNGS]              # SR-T first-factor columns (btl= given)
CROSS_COLS = ['c_' + n for n in FF.LAYERS]
NOGRP = (0, 1, 2, 37, 38, 39, 40, 41, 42)          # rungs not inside R04: no per-hit-set count (union counts only)


@dataclass
class WCfg:
    """In-job weight and storage parameters (pre-declared in WP_RULE.md; values fixed at G2b)."""
    nsub: int = 64               # IS subsets per weighted set (G2b: frozen at 64)
    f_is: float = 1.0            # fraction of IS groups weighted per trial (G2b passed without sub-sampling: f = 1)
    f_dp: float = 1.0            # counting-rung DP on every set (exact, ~4 us per set)
    f_b: float = 0.01            # hit-record sample (b): fraction of loose sets (rho > 1); compact sample at rho = 1
    n_a: int = 200               # hit-record sample (a): max sets passing N_IP2 >= 7 per trial (rho > 1)
    mip_gev: float = -1.0        # dE/dx unit (GeV); <= 0: dE/dx rungs not computed (until the G1 muon-gun calibration)
    trunc_frac: float = WG.TRUNC_FRAC
    group_frac: float = 0.5      # distinct hit sets: >= 50 % of the smaller set shared with the group leader
    mmax: int = 18               # max multi-layer interactions enumerated exactly (never exceeded: M <= 10 measured)
    ttol: float = 0.030
    delta95: float = 0.25        # rad; F0 fixed cut |dphi(n3, MET)| < delta95 at every rung (plan §2.2 item 6) AND the
                                 # finder road half-width (finder.Config.road must equal it; review WP_RULE R1 A-1).
                                 # 0.25 = planning value (dev/smoke); FROZEN value 0.15 (WP_RULE.md §1.3, frozen_inputs)
    eta_max: float = 1.0         # F0 fixed cut |eta(n3)| < eta_max at every rung: barrel-only selection (D4-12 re-decided
                                 # by the user 2026-10-13; WP_RULE.md §1.2, geometry-only value). FROZEN value 1.0
    require_btl: bool = False    # True: process_trial raises for rho > 1 without btl= (SR-T in-job column; review
                                 # WP_RULE R2 B-2).  config_from_frozen sets it to fz['frozen'] (fail closed in production)


def road_arrays(H, sid, INT, pv, m):
    U = np.ascontiguousarray(H[m, 1:4] - pv[None, :])
    r = np.hypot(H[m, 1], H[m, 2])
    un = np.linalg.norm(U, axis=1)
    u, inv = np.unique(INT[m], return_inverse=True)
    return dict(U=U, LC=FF.LC_OF[sid[m]], SD=FF.SIDE_OF[sid[m]], CX=H[m, 1] / r, CY=H[m, 2] / r,
                S0=np.ascontiguousarray(H[m, 4]), S1=np.ascontiguousarray(H[m, 5]),
                dEc=np.ascontiguousarray(H[m, 11] * np.hypot(U[:, 0], U[:, 1]) / un),
                INTl=inv.astype(np.int64), nI=int(len(u)), INTu=u)


def dedx_sets(hoff, hits, LC, dEc, mip, frac, U=None, normals=None, axes=None):
    """Full-set dE/dx per candidate (MIP units; NaN if mip <= 0 or no core IT hit): truncated mean (lowest frac) of the
    path-corrected dE of the candidate's CORE IT (TBPX) hits, |u.n2 - c| <= 2.5 w_core with c, w_core = median,
    1.4826 MAD of u.n2 over its in-band IT + PS hits (the chi2_core core; WP_RULE.md §1.4, review WP_RULE R1 B-1).
    Same arithmetic as weights.subset_weights at q = 1.  U/normals/axes = None: legacy in-band estimator (tests only)."""
    out = np.full(len(hoff) - 1, np.nan)
    if mip <= 0:
        return out
    for c in range(len(out)):
        h = hits[hoff[c]:hoff[c + 1]]
        if U is not None:
            ip = h[LC[h] <= 6]
            if len(ip) < 3:
                continue
            n = normals[c]; ax = axes[c]
            n2 = np.array([n[1] * ax[2] - n[2] * ax[1], n[2] * ax[0] - n[0] * ax[2], n[0] * ax[1] - n[1] * ax[0]])
            wv = U[ip] @ n2
            cm = np.median(wv)
            wc = 1.4826 * np.median(np.abs(wv - cm))
            it = (LC[ip] <= 3) & (wv >= cm - 2.5 * wc) & (wv <= cm + 2.5 * wc)
            v = np.sort(dEc[ip[it]])
        else:
            v = np.sort(dEc[h[LC[h] <= 3]])
        if len(v):
            k = max(1, min(len(v), int(np.ceil(frac * len(v)))))
            out[c] = v[:k].mean() / mip
    return out


def config_from_frozen(fz):
    """(cfg, wcfg) from a frozen_inputs.json dict (data/acts_stage4/frozen/; WP_RULE.md Appendix A.4): road = delta95,
    eta_max, mip_gev (null -> dE/dx columns NaN; filled in fix R2), require_btl = frozen, finder_config overrides."""
    d95 = float(fz['delta95'])
    cfg = FF.Config(road=d95)
    for k, v in (fz.get('finder_config') or {}).items():
        if not hasattr(cfg, k):
            raise RuntimeError('frozen finder_config key %r unknown to finder.Config' % k)
        setattr(cfg, k, v)
    mip = fz.get('mip_gev')
    wcfg = WCfg(delta95=d95, eta_max=float(fz['eta_max']),
                mip_gev=float(mip) if isinstance(mip, (int, float)) else -1.0, require_btl=bool(fz.get('frozen')))
    if abs(cfg.road - wcfg.delta95) > 1e-12:
        raise RuntimeError('road != delta95 (WP_RULE.md §1.1 item 1)')
    return cfg, wcfg


def btl_inputs(btl, pv, INTu):
    """btl = (B, INT_B): B (n, >= 6) BTL measurements in the G1 columns (sid, x, y, z, s0, s1, ..., t in ns at col 12),
    ALL BTL hits of the trial (not pre-filtered); INT_B the interaction id per row (same scheme as the tracker INT).
    Returns the kernel arrays and the combined interaction ids gB (road interactions -> their INTl index < nI; others
    -> nI + k)."""
    B = np.asarray(btl[0], np.float64)
    IB = np.asarray(btl[1], np.int64)
    if B.ndim != 2 or (len(B) and B.shape[1] < 6) or len(IB) != len(B):
        raise ValueError('btl must be (B (n, >= 6) G1 columns, INT (n,))')
    nI = len(INTu)
    UB = np.ascontiguousarray(B[:, 1:4] - pv[None, :]) if len(B) else np.zeros((0, 3))
    r = np.hypot(B[:, 1], B[:, 2]) if len(B) else np.zeros(0)
    TB = np.ascontiguousarray(B[:, 12]) if (len(B) and B.shape[1] > 12) else np.full(len(B), np.nan)
    pos = np.searchsorted(INTu, IB)
    inr = (pos < nI) & (INTu[np.minimum(pos, max(nI - 1, 0))] == IB) if nI else np.zeros(len(IB), bool)
    gB = np.where(inr, pos, -1).astype(np.int64)
    uo, inv = np.unique(IB[~inr], return_inverse=True)
    gB[~inr] = nI + inv
    return dict(UB=UB, CXB=np.ascontiguousarray(B[:, 1] / r) if len(B) else np.zeros(0),
                CYB=np.ascontiguousarray(B[:, 2] / r) if len(B) else np.zeros(0),
                S0B=np.ascontiguousarray(B[:, 4]) if len(B) else np.zeros(0),
                S1B=np.ascontiguousarray(B[:, 5]) if len(B) else np.zeros(0), TB=TB, gB=gB, nG=int(nI + len(uo)),
                n=int(len(B)), n_int=int(len(np.unique(IB))))


def btl_csr(bt, sel, nc, normals, axes, cfg):
    """In-band BTL CSR per CANDIDATE (indexed by candidate id; empty outside sel) + per-sel nhit, dt0."""
    sel = np.asarray(sel, np.int64)
    boff, bint, nhit, dt0 = WG.btl_band(np.ascontiguousarray(normals, np.float64), np.ascontiguousarray(axes, np.float64),
                                        sel, bt['UB'], bt['CXB'], bt['CYB'], bt['S0B'], bt['S1B'], bt['TB'], bt['gB'],
                                        bt['nG'], cfg.t_tol, cfg.w_c)
    cnt = np.zeros(nc, np.int64)
    cnt[sel] = np.diff(boff)
    boffC = np.zeros(nc + 1, np.int64)
    boffC[1:] = np.cumsum(cnt)
    return boffC, bint, nhit, dt0


def full_set_flags(V, dedx):
    """Rung pass flags (ncand, NR) of the full candidate sets at their own density (plan §2.5 ladder, §2.6 FB)."""
    nit2, nip2, n2s2, nl2, w = V['nit2'], V['nip2'], V['n2s2'], V['nl2'], V['dw_core']
    nc, c2 = V['n_core'], V['chi2_core']
    ndf = np.maximum(nc - 2, 1)
    F = np.zeros((len(nit2), NR), bool)
    with np.errstate(invalid='ignore'):
        p = np.where((nc >= 4) & np.isfinite(c2), CHI2.sf(np.nan_to_num(c2) * ndf, ndf), np.nan)
        ok = (nit2 >= 3) & (nip2 >= 4)
        F[:, 0] = ok
        for k in (5, 6, 7):
            ok = ok & (nip2 >= k); F[:, k - 4] = ok
        r4 = ok.copy()
        for i, W_ in enumerate(WG.W_K):
            ok = ok & (w < W_); F[:, 4 + i] = ok
        for i, P_ in enumerate(WG.P_MIN):
            ok = ok & (p > P_); F[:, 8 + i] = ok
        for i, k in enumerate((1, 2, 3)):
            ok = ok & (n2s2 >= k); F[:, 11 + i] = ok
        for i, e in enumerate(WG.E_MIN):
            F[:, 14 + i] = ok & (dedx > e)
        fb0 = r4 & (p > 0.05) & (n2s2 >= 3)
        for k in range(5):
            fk = fb0 if k == 0 else fb0 & (w < WG.W_K[k - 1])
            F[:, 17 + k] = fk
            for j, e in enumerate(WG.E_MIN):
                F[:, 22 + 3 * k + j] = fk & (dedx > e)
        for i, L in enumerate(range(5, 11)):
            F[:, 37 + i] = (nit2 >= 3) & (nl2 >= L)
    return F, p


def crossings(hoff, hits, LC, SD):
    """Per-candidate crossings per barrel layer (10 cols, capped at 255)."""
    n = len(hoff) - 1
    cnt = np.zeros((n, 10, 3), np.int64)
    cid = np.repeat(np.arange(n), np.diff(hoff))
    np.add.at(cnt, (cid, LC[hits], SD[hits]), 1)
    cr = np.concatenate([cnt[:, :4, 0], np.minimum(cnt[:, 4:, 1], cnt[:, 4:, 2])], axis=1)
    return np.minimum(cr, 255).astype(np.uint8)


def process_trial(H, sid, INT, pv, phimet, rho, seed, cfg=None, wcfg=None, extra_hit_cols=None, ckf=None, btl=None,
                  require_btl=None):
    """One PU-only trial (one road).  H: (n, >= 12) measurement rows (f1r column layout: sid, x, y, z, s0, s1, flag, vp,
    particle, gen, vsec, dE[, t]) = the finder pool AFTER CKF removal; INT: interaction id per row.
    cfg: finder.Config; its road MUST equal wcfg.delta95 (road = delta95, WP_RULE.md §1.1 item 1; review WP_RULE R1
    A-1); cfg=None builds Config(road=wcfg.delta95).  wcfg: WCfg (delta95, eta_max, mip_gev, ...).
    ckf: (m, >= 6) CKF-used (removed) barrel measurements, same columns as H (finder/chain_inputs.prepare_event 'ckf');
    per stored candidate n_ckf_band (chain_inputs.ckf_band_counts, the one definition) and f_CKF = n_ckf_band /
    (n_ckf_band + in-band hits) are stored (WP_RULE.md §1.1 item 9; NOT a cut in the in-job ladders: B_PU credits no
    f_CKF rejection).  ckf=None: no CKF information (interim chain) -> n_ckf_band = -1, f_CKF = NaN.
    btl: (B, INT_B) ALL BTL measurements of the trial (G1 columns, t in ns at col 12) and their interaction ids -> the
    SR-T first-factor columns (RUNGS_T): row n_pass_T, n_grp_T (every rho) and S_uni_T, S_ded_T, V_uni_T,
    meanW_pull_T (rho > 1); cand btl_n_band, btl_n_int, btl_dt0 (and w_T at rho > 1).  btl=None with
    require_btl (None -> wcfg.require_btl) and rho > 1 raises (review WP_RULE R2 B-2; the G1 runner passes
    require_btl=True for rho > 1 production jobs).
    Returns dict(row=per-trial scalars and rung tables, cand=compact candidate records, hit=hit-record tables)."""
    wcfg = wcfg or WCfg()
    cfg = cfg or FF.Config(road=wcfg.delta95)
    if abs(cfg.road - wcfg.delta95) > 1e-12:
        raise ValueError('finder road %.6g != delta95 %.6g (WP_RULE.md §1.1 item 1: road = delta95)'
                         % (cfg.road, wcfg.delta95))
    if btl is None and rho > 1 and (wcfg.require_btl if require_btl is None else require_btl):
        raise RuntimeError('rho > 1 production trial without btl=: the SR-T in-job BTL-presence columns are required '
                           '(WP_RULE.md §1.4; review WP_RULE R2 B-2)')
    rng = np.random.default_rng(seed)
    T = {}
    t0 = time.perf_counter()
    r = FF.find(H, sid, pv, phimet, cfg=cfg, store='loose', want_csr=True)
    T['find'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    m = r['road_mask']
    road_idx = np.where(m)[0]
    A = road_arrays(H, sid, INT, pv, m)
    hoff = r['csr_off']
    hits = r['csr_hits']
    nc = len(hoff) - 1
    V = r['vars']
    # distinct hit sets: greedy grouping in rank order over the candidates passing R04 (N_IT2 >= 3, N_IP2 >= 7);
    # other candidates carry gid = -1 (WP_RULE.md §2: the per-hit-set convention applies from R04 on)
    gid = np.full(nc, -1, np.int64)
    ax_ = r['axis']
    eta_ax = np.arcsinh(ax_[:, 2] / np.maximum(np.hypot(ax_[:, 0], ax_[:, 1]), 1e-12)) if nc else np.zeros(0)
    # F0 fixed cuts, part of every rung: |dphi(n3, MET)| < delta95 and the barrel-only |eta(n3)| < eta_max (WP_RULE §1.2)
    aligned = (r['dphi_met'] < wcfg.delta95) & (np.abs(eta_ax) < wcfg.eta_max)
    r4 = np.where((V['nit2'] >= 3) & (V['nip2'] >= 7) & aligned)[0] if nc else np.zeros(0, np.int64)
    if len(r4):
        ho4 = np.zeros(len(r4) + 1, np.int64)
        ho4[1:] = np.cumsum(hoff[r4 + 1] - hoff[r4])
        hi4 = np.concatenate([hits[hoff[c]:hoff[c + 1]] for c in r4])
        gid[r4] = WG.group_sets(ho4, hi4, int(m.sum()), wcfg.group_frac)
    ngrp = int(gid.max()) + 1 if len(r4) else 0
    T['group'] = time.perf_counter() - t0
    t0 = time.perf_counter()
    dedx = np.full(nc, np.nan)
    if len(r4) and wcfg.mip_gev > 0:      # dE/dx rungs are inside R04
        ho4 = np.zeros(len(r4) + 1, np.int64)
        ho4[1:] = np.cumsum(hoff[r4 + 1] - hoff[r4])
        dedx[r4] = dedx_sets(ho4, np.concatenate([hits[hoff[c]:hoff[c + 1]] for c in r4]), A['LC'], A['dEc'],
                             wcfg.mip_gev, wcfg.trunc_frac, A['U'], r['normal'][r4], r['axis'][r4])
    F, pchi = full_set_flags(V, dedx)
    F &= aligned[:, None]
    n_pass = F.sum(0).astype(np.int64)
    n_grp = np.zeros(NR, np.int64)
    for k in range(NR):
        if k in NOGRP:
            n_grp[k] = -1
        elif n_pass[k]:
            n_grp[k] = len(np.unique(gid[F[:, k]]))
    T['flags'] = time.perf_counter() - t0
    bt = None
    if btl is not None:
        t0 = time.perf_counter()
        bt = btl_inputs(btl, pv, A['INTu'])
        alg = np.where(aligned)[0].astype(np.int64)        # misaligned candidates fail every rung
        boffC, bintC, nh_al, _ = btl_csr(bt, alg, nc, r['normal'], r['axis'], cfg)
        present = np.zeros(nc, bool)
        present[alg] = nh_al > 0
        FT = F & present[:, None]
        n_pass_T = FT.sum(0).astype(np.int64)
        n_grp_T = np.zeros(NR, np.int64)
        for k in range(NR):
            if k in NOGRP:
                n_grp_T[k] = -1
            elif n_pass_T[k]:
                n_grp_T[k] = len(np.unique(gid[FT[:, k]]))
        T['btl'] = time.perf_counter() - t0
    row = dict(rho=rho, seed=seed, pv=pv, phimet=phimet, n_road=r['n_road'], n_trip=r['n_trip'], n_refit=r['n_refit'],
               n_kept_all=r['n_kept_all'], n_loose=nc, n_groups=ngrp, n_pass=n_pass, n_grp=n_grp,
               n_ip2ge7=int(np.sum(V['nip2'] >= 7)), n_ip2ge6=int(np.sum(V['nip2'] >= 6)),
               n_aligned=int(aligned.sum()), road=float(cfg.road), delta95=float(wcfg.delta95),
               eta_max=float(wcfg.eta_max), mip_gev=float(wcfg.mip_gev), n_ckf_hits=-1 if ckf is None else len(ckf))
    if bt is not None:
        row.update(n_btl=bt['n'], n_btl_int=bt['n_int'], n_btl_present=int(present.sum()), n_pass_T=n_pass_T,
                   n_grp_T=n_grp_T)
    nip2 = V['nip2']
    q = 1.0 / rho
    Wset = None
    is_sel = np.zeros(0, np.int64)
    if rho > 1 and nc:
        # ---- counting rungs: exact DP on every set (f_dp = 1)
        t0 = time.perf_counter()
        allsel = np.where(aligned)[0].astype(np.int64)          # misaligned candidates have w = 0 at every rung
        Wdp, info = WG.count_weights(hoff, hits, allsel, A['LC'], A['SD'], A['INTl'], A['nI'], q, wcfg.mmax)
        T['w_dp'] = time.perf_counter() - t0
        if info[:, 2].any():
            raise RuntimeError('multi-layer interactions above mmax: %d sets' % int(info[:, 2].sum()))
        if bt is not None:      # SR-T counting columns, exact: w_T = w - (1 - q)^|I_B| w(S minus I_B)
            t0b = time.perf_counter()
            nB = (boffC[allsel + 1] - boffC[allsel]).astype(np.float64)
            hr, hh, ndrop = WG.drop_interactions(hoff, hits, allsel, A['INTl'], A['nI'], boffC, bintC)
            Wred = Wdp.copy()
            ov = np.where(ndrop > 0)[0]
            if len(ov):
                Wo, info_o = WG.count_weights(hr, hh, ov.astype(np.int64), A['LC'], A['SD'], A['INTl'], A['nI'], q,
                                              wcfg.mmax)
                if info_o[:, 2].any():
                    raise RuntimeError('multi-layer interactions above mmax (BTL-reduced sets)')
                Wred[ov] = Wo
            WdpT = np.clip(Wdp - (1.0 - q) ** nB[:, None] * Wred, 0.0, Wdp)
            T['w_dp_btl'] = time.perf_counter() - t0b
        # ---- per-subset families: group-level Bernoulli(f_is) sub-sampling of the IS groups
        t0 = time.perf_counter()
        is_grp = np.unique(gid[r4])
        u = rng.random(len(is_grp))
        samp_grp = is_grp[u < wcfg.f_is]
        insamp = np.zeros(ngrp + 1, bool)
        insamp[samp_grp] = True
        is_sel = r4[insamp[gid[r4]]].astype(np.int64)
        Wis = np.zeros((len(is_sel), WG.N_SUB_OUT)); Vis = np.zeros_like(Wis); nzero = np.zeros(len(is_sel), np.int64)
        WisT = np.zeros_like(Wis); VisT = np.zeros_like(Wis)
        if len(is_sel) and bt is None:
            Wis, Vis, nzero = WG.subset_weights(hoff, hits, is_sel, A['LC'], A['SD'], A['INTl'], A['nI'], A['U'],
                                                A['CX'], A['CY'], A['S0'], A['S1'], A['dEc'], r['normal'], r['axis'],
                                                q, wcfg.nsub, int(seed % (2 ** 31 - 1)), wcfg.ttol, wcfg.mip_gev,
                                                WG.CHI2_ISF, wcfg.mmax)
        elif len(is_sel):       # same draws (bit-identical Wis, Vis, nzero) + the SR-T per-subset factor
            Wis, Vis, nzero, WisT, VisT = WG.subset_weights_btl(
                hoff, hits, is_sel, A['LC'], A['SD'], A['INTl'], A['nI'], A['U'], A['CX'], A['CY'], A['S0'], A['S1'],
                A['dEc'], r['normal'], r['axis'], q, wcfg.nsub, int(seed % (2 ** 31 - 1)), wcfg.ttol, wcfg.mip_gev,
                WG.CHI2_ISF, wcfg.mmax, boffC, bintC)
        T['w_is'] = time.perf_counter() - t0
        t0 = time.perf_counter()
        # ---- per-set weights in RUNGS columns (IS columns 0 outside the IS sample; HT factor applied in the sums)
        Wset = np.zeros((nc, NR), np.float32)
        Vset = np.zeros((nc, NR), np.float32)
        for k, j in MAP_DP.items():
            Wset[allsel, k] = Wdp[:, j]
        for k, j in MAP_IS.items():
            Wset[is_sel, k] = Wis[:, j]
            Vset[is_sel, k] = Vis[:, j]
        isc = np.array(sorted(MAP_IS))
        fac = np.ones(NR)
        fac[isc] = 1.0 / wcfg.f_is
        S_uni = np.nansum(Wset, 0, dtype=np.float64) * fac
        V_uni = np.nansum(Vset, 0, dtype=np.float64) * fac ** 2
        # group max (dedup): max over members per group
        Gmax = np.zeros((ngrp, NR))
        g4 = gid >= 0
        np.maximum.at(Gmax, gid[g4], np.nan_to_num(Wset[g4]).astype(np.float64))
        S_ded = Gmax.sum(0) * fac
        S_ded[list(NOGRP)] = np.nan
        if wcfg.mip_gev <= 0:
            for k in list(range(14, 17)) + list(range(22, 37)):
                S_uni[k] = np.nan; S_ded[k] = np.nan
        row.update(S_uni=S_uni, S_ded=S_ded, V_uni=V_uni, n_is_groups=int(len(is_grp)),
                   n_is_groups_sampled=int(len(samp_grp)), n_is_sets=int(len(is_sel)),
                   is_zero_draw_frac=float(nzero.sum() / max(1, len(is_sel) * wcfg.nsub)),
                   meanW_vs_dp=float(np.sum(Wis[:, 33]) - np.sum(Wset[is_sel, 3])) if len(is_sel) else 0.0,
                   # per-trial run check (review WP_RULE R1 C-7): |pull| < 3 expected
                   meanW_pull=float((np.sum(Wis[:, 33]) - np.sum(Wset[is_sel, 3])) / np.sqrt(np.sum(Vis[:, 33])))
                   if len(is_sel) and np.sum(Vis[:, 33]) > 0 else 0.0,
                   M_max=int(info[:, 1].max()) if len(info) else 0,
                   m_mean=float(info[:, 0].mean()) if len(info) else 0.0)
        if bt is not None:
            WsetT = np.zeros((nc, NR), np.float32)
            VsetT = np.zeros((nc, NR), np.float32)
            for k, j in MAP_DP.items():
                WsetT[allsel, k] = WdpT[:, j]
            for k, j in MAP_IS.items():
                WsetT[is_sel, k] = WisT[:, j]
                VsetT[is_sel, k] = VisT[:, j]
            S_uni_T = np.nansum(WsetT, 0, dtype=np.float64) * fac
            V_uni_T = np.nansum(VsetT, 0, dtype=np.float64) * fac ** 2
            GmaxT = np.zeros((ngrp, NR))
            np.maximum.at(GmaxT, gid[g4], np.nan_to_num(WsetT[g4]).astype(np.float64))
            S_ded_T = GmaxT.sum(0) * fac
            S_ded_T[list(NOGRP)] = np.nan
            if wcfg.mip_gev <= 0:
                for k in list(range(14, 17)) + list(range(22, 37)):
                    S_uni_T[k] = np.nan; S_ded_T[k] = np.nan
            row.update(S_uni_T=S_uni_T, S_ded_T=S_ded_T, V_uni_T=V_uni_T,
                       # run check: IS mean(W f) vs the exact DP P(R04 and BTL-present); |pull| < 3 expected
                       meanW_pull_T=float((np.sum(WisT[:, 33]) - np.sum(WsetT[is_sel, 3])) / np.sqrt(np.sum(VisT[:, 33])))
                       if len(is_sel) and np.sum(VisT[:, 33]) > 0 else 0.0)
        T['w_sum'] = time.perf_counter() - t0
    # ---------------- storage policy (WP_RULE.md §S)
    t0 = time.perf_counter()
    if rho == 1:
        compact = np.where(F[:, 3])[0]                                       # N_IP2 >= 7 (rung R04)
        samp_b = np.where(rng.random(nc) < wcfg.f_b)[0]                      # 1 % loose sample (compact)
        full = np.where(F[:, 3] & ((V['dw_core'] < 37.5) | (np.nan_to_num(pchi) > 1e-3)))[0]
    else:
        cand7 = is_sel
        samp_a = np.sort(rng.choice(cand7, min(wcfg.n_a, len(cand7)), replace=False)) if len(cand7) else cand7
        samp_b = np.where(rng.random(nc) < wcfg.f_b)[0]
        compact = np.union1d(samp_a, samp_b)
        full = compact
    keep = np.union1d(compact, samp_b).astype(np.int64)
    if len(keep):
        hk = np.zeros(len(keep) + 1, np.int64)
        hk[1:] = np.cumsum(hoff[keep + 1] - hoff[keep])
        cr = crossings(hk, np.concatenate([hits[hoff[c]:hoff[c + 1]] for c in keep]), A['LC'], A['SD'])
    else:
        cr = np.zeros((0, 10), np.uint8)
    tag = np.zeros(len(keep), np.uint8)              # bit0 compact policy set, bit1 sample (b), bit2 full hit record
    tag[np.isin(keep, compact)] |= 1
    tag[np.isin(keep, samp_b)] |= 2
    tag[np.isin(keep, full)] |= 4
    cand = dict(idx=keep.astype(np.int32), tag=tag, group=gid[keep].astype(np.int32),
                **{k: V[k][keep].astype(np.float32) for k in ('chi2ndf', 'dw_old', 'dw_core', 'chi2_core', 'nz')},
                **{k: V[k][keep].astype(np.int16) for k in ('nit2', 'not2', 'nl2', 'nip2', 'n2s2', 'nl1', 'nhit',
                                                             'n_core', 'not2h')},
                p_chi2core=pchi[keep].astype(np.float32), dedx=dedx[keep].astype(np.float32),
                cross=cr, normal=r['normal'][keep].astype(np.float32), axis=r['axis'][keep].astype(np.float32),
                dphi_met=r['dphi_met'][keep].astype(np.float32), seed_n2=r['seed_n2'][keep].astype(np.int16),
                rungs=np.packbits(F[keep], axis=1))
    # f_CKF (WP_RULE.md §1.1 item 9): CKF-used measurements in the candidate's final band (one definition:
    # chain_inputs.ckf_band_counts, also used by run_stage4), stored only
    nband = (hoff[keep + 1] - hoff[keep]).astype(np.int64)
    if ckf is not None:
        from . import chain_inputs as CI
        nck = CI.ckf_band_counts(np.asarray(ckf), pv, phimet, r['normal'][keep], r['axis'][keep], w_c=cfg.w_c,
                                 road=cfg.road, t_tol=cfg.t_tol).astype(np.int32)
        cand['n_ckf_band'] = nck
        cand['f_ckf'] = (nck / np.maximum(nck + nband, 1)).astype(np.float32)
    else:
        cand['n_ckf_band'] = np.full(len(keep), -1, np.int32)
        cand['f_ckf'] = np.full(len(keep), np.nan, np.float32)
    cand['n_band'] = nband.astype(np.int32)
    cand['eta_axis'] = eta_ax[keep].astype(np.float32)
    if Wset is not None:
        cand['w'] = Wset[keep].astype(np.float32)
        cand['is_weighted'] = np.isin(keep, is_sel)
    if bt is not None:      # SR-T per stored candidate (any alignment): in-band BTL hits, interactions, earliest dt
        bo_k, _, nh_k, dt_k = WG.btl_band(np.ascontiguousarray(r['normal'], np.float64),
                                          np.ascontiguousarray(r['axis'], np.float64), keep.astype(np.int64), bt['UB'],
                                          bt['CXB'], bt['CYB'], bt['S0B'], bt['S1B'], bt['TB'], bt['gB'], bt['nG'],
                                          cfg.t_tol, cfg.w_c)
        cand['btl_n_band'] = np.minimum(nh_k, 32767).astype(np.int16)
        cand['btl_n_int'] = np.minimum(np.diff(bo_k), 32767).astype(np.int16)
        cand['btl_dt0'] = dt_k.astype(np.float32)
        if Wset is not None:
            cand['w_T'] = WsetT[keep].astype(np.float32)
    # hit records: CSR into a per-trial union table of the referenced road hits
    fk = keep[(tag & 4) > 0]
    if len(fk):
        refs = [hits[hoff[c]:hoff[c + 1]] for c in fk]
        uni, inv = np.unique(np.concatenate(refs), return_inverse=True)
        roff = np.zeros(len(fk) + 1, np.int64)
        roff[1:] = np.cumsum([len(x) for x in refs])
        Hr = H[road_idx[uni]]
        hit = dict(cand=fk.astype(np.int32), off=roff.astype(np.int32), ref=inv.astype(np.int32),
                   xyz=Hr[:, 1:4].astype(np.float32), sid=sid[road_idx[uni]].astype(np.int16),
                   s01=Hr[:, 4:6].astype(np.float32), dE=Hr[:, 11].astype(np.float32),
                   INT=INT[road_idx[uni]].astype(np.int64), particle=Hr[:, 8].astype(np.int32),
                   gen=Hr[:, 9].astype(np.int8))
        if H.shape[1] > 12:
            hit['t'] = Hr[:, 12].astype(np.float32)
    else:
        hit = None
    T['store'] = time.perf_counter() - t0
    row['times'] = T
    row['t_total'] = float(sum(T.values()))
    return dict(row=row, cand=cand, hit=hit)
