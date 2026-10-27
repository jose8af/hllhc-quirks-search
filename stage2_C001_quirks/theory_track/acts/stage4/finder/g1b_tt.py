"""G1b TT-side code for the signal (A1/A2/A5) and C' (C'0 / C'_PU) job kinds (2026-10-13; post-freeze).

NEW module (no frozen file changed).  It CALLS the frozen code (finder.find via production.process_trial,
production.full_set_flags / dedx_sets / road_arrays / btl_csr, chain_inputs.merge_pool / ckf_band_counts,
pu_inputs.topup) and adds only what the signal and C' kinds need on top of the frozen per-trial output:

* assemble(): the finder pool of one event exactly as chain_inputs.prepare_event (top-up -> CKF removal -> U-5 b
  merging, INT of a merged measurement = its largest-dE member), with ONE difference: the TDR top-up is generated from
  the event's PU (non-inserted) barrel rows only, so that inserted signal / toy hits never change the PU top-up
  (row-major A2 pairing across Lambda: the same PU pool at every Lambda; identical rule in A5 and C'_PU).  With no
  inserted rows it is prepare_event bit for bit (checked in g1b smoke: test_assemble_equals_prepare).
  It also returns the pre-merge pool (Hp, Tp, Ip) and the member -> merged map, so that every inserted (quirk / toy)
  pre-merge measurement can be followed into the merged pool ("links").
* trial(): production.process_trial (frozen; S1-S5 records unchanged) + the full candidate list of the same finder call
  (finder.find captured in-process; process_trial is not modified), and the rung flags F (ncand, 43) recomputed with
  the frozen helpers in process_trial's order; F.sum(0) == row['n_pass'] is ASSERTED on every trial (any divergence
  from the frozen code raises).
* signal_summary(): per rung, the event passes for the efficiency iff a candidate passes the rung AND contains >= 50 % of
  the event's written barrel quirk measurements (plan §2.4 definition; quirk measurements counted pre-CKF, pre-merge:
  CKF stealing and merging are losses), with and without f_CKF < 0.2 (WP_RULE §1.2: a signal selection cut) and with
  BTL presence (SR-T first factor).  Every candidate with >= 1 quirk link is stored (compact).
* C' (WP_RULE §7, plan §4.2): sigma_hat, exhaustive-triple preselection (chi2_3 <= 48 about the stored PV, >= 2 toy
  particles, 3 distinct layers), attribution of every candidate (>= 3 core toy links in >= 3 layers, >= 1 IT+PS,
  each within 4 sigma_hat of the candidate plane at its STORED C'0 position; >= 2 toy particles, looper: >= 2 crossings in
  >= 1 layer), the V4-10 per-event hash of the pre-CKF, pre-merge toy measurements + PV, and the C'_PU toy-row
  replacement (with-PU toy rows -> the C'0 rows, matched by SimHit truth position; CKF flags from the with-PU event).
"""
import dataclasses
import hashlib

import numpy as np

from . import chain_inputs as CI
from . import finder as FF
from . import production as PR
from . import pu_inputs as PI
from . import weights as WG

SIG_VP = 4000
GUN_VP = 3500
HS_VP = 3000
PV_SIGMA = np.array([0.010, 0.010, 0.015])     # mm, plan §1.7
MET_SIGMA = 25.0                                # GeV per component, plan §1.7
DN_MAX = 2e-3                                   # rad, WP_RULE §7 sigma_hat
T_TOL = 0.030                                   # mm
CHI2_PRE = 48.0                                 # 3 x 4^2
NSIG_ATTR = 4.0
FRAC_MATCH = 0.5
FCKF_CUT = 0.2
TRIPLE_CHUNK = 20000


# ------------------------------------------------------------------------------------------------------------ pool
def assemble(ev, tru, tag, rng, inserted_vp=(), do_topup=True, ratios=None, merge_scale=1.0):
    """chain_inputs.prepare_event with the top-up drawn from the non-inserted barrel rows only (module docstring).
    -> dict(H, sid, INT, btl, btl_INT, ckf, uz-less) + Hp/Tp/Ip (pre-merge pool), pre_map (Hp row -> H row), H0 (all
    written barrel rows, pre-CKF), H0_keep (H0 index of each Fatras row of Hp), stats."""
    sid_all = ev[:, 0].astype(np.int64)
    INT_all = tag * 1_000_000 + ev[:, 7].astype(np.int64)
    bar = FF.LC_OF[sid_all] >= 0
    btl = CI.KIND[sid_all] == 'BTL'
    H0 = ev[bar]; s0 = sid_all[bar]; I0 = INT_all[bar]; T0 = tru[bar].astype(np.float64)
    ins = np.isin(H0[:, 7].astype(np.int64), np.asarray(inserted_vp, np.int64)) if len(inserted_vp) else \
        np.zeros(len(H0), bool)
    st = dict(n_fatras=int(len(H0)), n_inserted=int(ins.sum()))
    if do_topup:
        t, ti = PI.topup(H0[~ins], s0[~ins], rng, tag, ratios)
    else:
        t, ti = np.zeros((0, H0.shape[1])), np.zeros(0, np.int64)
    st['n_topup'] = int(len(t))
    ck = (H0[:, 6].astype(np.int64) & 1) == 1
    st['n_ckf_removed'] = int(ck.sum())
    keep0 = np.where(~ck)[0]
    Hp = np.concatenate([H0[keep0], t]); Ip = np.concatenate([I0[keep0], ti])
    Tp = np.concatenate([T0[keep0], t[:, 1:4]])
    Hm, mapi, ng, nh, nenl = CI.merge_pool(Hp, Tp, merge_scale)
    Im = np.zeros(len(Hm), np.int64)
    Im[mapi] = Ip
    if ng:
        sz = np.bincount(mapi, minlength=len(Hm))
        for j in np.where(sz > 1)[0]:
            mem = np.where(mapi == j)[0]
            Im[j] = Ip[mem[np.argmax(Hp[mem, 11])]]
    st.update(n_pool=int(len(Hm)), n_merged_groups=ng, n_merged_hits=nh, n_sigma_enlarged=nenl)
    return dict(H=Hm, sid=Hm[:, 0].astype(np.int64), INT=Im, btl=ev[btl], btl_INT=INT_all[btl], ckf=H0[ck],
                Hp=Hp, Tp=Tp, Ip=Ip, pre_map=mapi, H0=H0, T0=T0, H0_keep=keep0, H0_ckf=ck, stats=st)


def pv_met(vtx, met_true, rng):
    """plan §1.7: PV = true vertex + N(0, (10, 10, 15) um); MET = truth MET + N(0, 25 GeV) per component."""
    pv = np.asarray(vtx[:3], float) + rng.normal(0.0, 1.0, 3) * PV_SIGMA
    met = np.asarray(met_true[:2], float) + rng.normal(0.0, MET_SIGMA, 2)
    return pv, float(np.arctan2(met[1], met[0]))


# ----------------------------------------------------------------------------------------------------------- trial
def trial(H, sid, INT, pv, phimet, seed, cfg, wcfg, ckf=None, btl=None):
    """production.process_trial (frozen) at rho = 1 + the captured finder output and the full rung flags.
    -> (res, X) with X = dict(r (finder.find output), road_idx, hoff, hits, A (road arrays), F, pchi, dedx, aligned, eta)."""
    cap = {}
    orig = FF.find

    def _find(*a, **k):
        out = orig(*a, **k)
        cap['r'] = out
        return out
    FF.find = _find
    try:
        res = PR.process_trial(H, sid, INT, pv, phimet, 1.0, seed, cfg=cfg, wcfg=wcfg, ckf=ckf, btl=btl)
    finally:
        FF.find = orig
    r = cap['r']
    m = r['road_mask']
    road_idx = np.where(m)[0]
    A = PR.road_arrays(H, sid, INT, pv, m)
    hoff = r['csr_off']; hits = r['csr_hits']
    nc = len(hoff) - 1
    V = r['vars']
    ax_ = r['axis']
    eta = np.arcsinh(ax_[:, 2] / np.maximum(np.hypot(ax_[:, 0], ax_[:, 1]), 1e-12)) if nc else np.zeros(0)
    aligned = (r['dphi_met'] < wcfg.delta95) & (np.abs(eta) < wcfg.eta_max)
    r4 = np.where((V['nit2'] >= 3) & (V['nip2'] >= 7) & aligned)[0] if nc else np.zeros(0, np.int64)
    dedx = np.full(nc, np.nan)
    if len(r4) and wcfg.mip_gev > 0:
        ho4 = np.zeros(len(r4) + 1, np.int64)
        ho4[1:] = np.cumsum(hoff[r4 + 1] - hoff[r4])
        dedx[r4] = PR.dedx_sets(ho4, np.concatenate([hits[hoff[c]:hoff[c + 1]] for c in r4]), A['LC'], A['dEc'],
                                wcfg.mip_gev, wcfg.trunc_frac, A['U'], r['normal'][r4], r['axis'][r4])
    F, pchi = PR.full_set_flags(V, dedx)
    F &= aligned[:, None]
    if not np.array_equal(F.sum(0).astype(np.int64), np.asarray(res['row']['n_pass'], np.int64)):
        raise RuntimeError('g1b_tt.trial: recomputed rung flags differ from process_trial n_pass')
    return res, dict(r=r, road_idx=road_idx, hoff=hoff, hits=hits, A=A, F=F, pchi=pchi, dedx=dedx, aligned=aligned,
                     eta=eta, nc=nc)


def core_mask(X, c):
    """Core of candidate c (WP_RULE §1.1 item 7; kernels.cand_vars): IT+PS in-band hits with |u.n2 - c| <= 2.5 w_core,
    2S hits within that interval enlarged by 3 |n2_z| sigma_1.  Needs >= 3 IT+PS hits (else empty).
    -> (road indices of the band, bool core mask)."""
    h = X['hits'][X['hoff'][c]:X['hoff'][c + 1]]
    A = X['A']
    n = X['r']['normal'][c]; ax = X['r']['axis'][c]
    n2 = np.cross(n, ax)
    wv = A['U'][h] @ n2
    ip = A['LC'][h] <= 6
    core = np.zeros(len(h), bool)
    if ip.sum() > 2:
        wi = wv[ip]
        cm = np.median(wi)
        s = 1.4826 * np.median(np.abs(wi - cm))
        lo = cm - 2.5 * s; hi = cm + 2.5 * s
        s2 = np.abs(n2[2]) * A['S1'][h]
        core = np.where(ip, (wv >= lo) & (wv <= hi), (wv >= lo - 3 * s2) & (wv <= hi + 3 * s2))
    return h, core


def links(P, inserted_vp):
    """Pre-merge inserted (quirk / toy) rows of the Fatras part of Hp -> merged pool row.
    -> (Hp row indices, pool row indices)."""
    nF = len(P['H0_keep'])
    vp = P['Hp'][:nF, 7].astype(np.int64)
    j = np.where(np.isin(vp, np.asarray(inserted_vp, np.int64)))[0]
    return j, P['pre_map'][j]


def cand_extra(X, cands, pv, phimet, cfg, ckf, btl_kernel=None):
    """f_CKF (chain_inputs.ckf_band_counts, the one definition) and BTL presence (weights.btl_band) for chosen candidates."""
    cands = np.asarray(cands, np.int64)
    r = X['r']
    nband = (X['hoff'][cands + 1] - X['hoff'][cands]).astype(np.int64)
    if ckf is not None and len(cands):
        nck = CI.ckf_band_counts(np.asarray(ckf), pv, phimet, r['normal'][cands], r['axis'][cands], w_c=cfg.w_c,
                                 road=cfg.road, t_tol=cfg.t_tol).astype(np.int64)
        fck = nck / np.maximum(nck + nband, 1)
    else:
        nck = np.full(len(cands), -1); fck = np.full(len(cands), np.nan)
    nbt = np.full(len(cands), -1, np.int64)
    if btl_kernel is not None and len(cands):
        bt = btl_kernel
        _, _, nh, _ = WG.btl_band(np.ascontiguousarray(r['normal'], np.float64), np.ascontiguousarray(r['axis'], np.float64),
                                  cands, bt['UB'], bt['CXB'], bt['CYB'], bt['S0B'], bt['S1B'], bt['TB'], bt['gB'],
                                  bt['nG'], cfg.t_tol, cfg.w_c)
        nbt = nh.astype(np.int64)
    return nck, fck, nbt


# ---------------------------------------------------------------------------------------------------------- signal
def signal_summary(P, X, n_q_written, pv, phimet, cfg, ckf, btl):
    """Matched-candidate efficiency flags per rung (module docstring).  n_q_written: the event's written barrel quirk
    measurements (pre-CKF, pre-merge) = the denominator."""
    nR = PR.NR
    out = dict(eff=np.zeros(nR, bool), eff_fckf=np.zeros(nR, bool), eff_T=np.zeros(nR, bool),
               eff_fckf_T=np.zeros(nR, bool), best_frac=0.0, n_q_pool=0, n_q_road=0, n_cand_q=0)
    j, pj = links(P, (SIG_VP,))
    nq_pool = np.bincount(pj, minlength=len(P['H'])) if len(j) else np.zeros(len(P['H']), np.int64)
    out['n_q_pool'] = int(len(j))
    nc = X['nc']
    if nc == 0 or n_q_written == 0:
        return out, None
    nq_road = nq_pool[X['road_idx']]
    out['n_q_road'] = int(nq_road.sum())
    hoff = X['hoff']; hits = X['hits']
    cid = np.repeat(np.arange(nc), np.diff(hoff))
    nq = np.bincount(cid, weights=nq_road[hits], minlength=nc).astype(np.int64)
    frac = nq / float(n_q_written)
    out['best_frac'] = float(frac.max())
    sel = np.where(nq > 0)[0]
    out['n_cand_q'] = int(len(sel))
    if not len(sel):
        return out, None
    bt = PR.btl_inputs(btl, pv, X['A']['INTu']) if btl is not None else None
    nck, fck, nbt = cand_extra(X, sel, pv, phimet, cfg, ckf, bt)
    F = X['F'][sel]
    mt = frac[sel] >= FRAC_MATCH
    okf = np.nan_to_num(fck, nan=1.0) < FCKF_CUT
    pres = nbt > 0
    out['eff'] = (F & mt[:, None]).any(0)
    out['eff_fckf'] = (F & (mt & okf)[:, None]).any(0)
    out['eff_T'] = (F & (mt & pres)[:, None]).any(0)
    out['eff_fckf_T'] = (F & (mt & okf & pres)[:, None]).any(0)
    V = X['r']['vars']
    rec = dict(idx=sel.astype(np.int32), nq=nq[sel].astype(np.int16), frac=frac[sel].astype(np.float32),
               rungs=np.packbits(F, axis=1), n_ckf_band=nck.astype(np.int32), f_ckf=fck.astype(np.float32),
               btl_n_band=np.minimum(nbt, 32767).astype(np.int16), n_band=np.diff(hoff)[sel].astype(np.int32),
               p_chi2core=X['pchi'][sel].astype(np.float32), dedx=X['dedx'][sel].astype(np.float32),
               normal=X['r']['normal'][sel].astype(np.float32), axis=X['r']['axis'][sel].astype(np.float32),
               dphi_met=X['r']['dphi_met'][sel].astype(np.float32), eta_axis=X['eta'][sel].astype(np.float32),
               **{k: V[k][sel].astype(np.float32) for k in ('chi2ndf', 'dw_core', 'chi2_core')},
               **{k: V[k][sel].astype(np.int16) for k in ('nit2', 'nip2', 'n2s2', 'nl2', 'nhit', 'n_core')})
    return out, rec


# -------------------------------------------------------------------------------------------------------------- C'
def sigma_hat(rows, pv):
    """WP_RULE §7: sigma_hat^2 = sigma_loc,max^2 + t_tol^2 + (dn_max |u|)^2 (rows: G1 columns, s0/s1 at 4/5)."""
    u = rows[:, 1:4] - pv[None, :]
    return np.sqrt(np.maximum(rows[:, 4], rows[:, 5]) ** 2 + T_TOL ** 2 + (DN_MAX * np.linalg.norm(u, axis=1)) ** 2)


def toy_keys(rows, tru, toysim):
    """Toy particle key per toy measurement row: (vsec, particle, generation, subParticle) of its SimHit, matched by the
    truth position (the measurement's SimHit; toysim columns run_chain.TOY_COLS).  -> int64 keys, n_unmatched."""
    key = np.full(len(rows), -1, np.int64)
    if not len(rows):
        return key, 0
    S = np.asarray(toysim, np.float64)
    if not len(S):
        return key, len(rows)
    T = np.asarray(tru, np.float64)
    d = np.abs(T[:, None, :] - S[None, :, 1:4]).max(2)
    j = np.argmin(d, 1)
    ok = d[np.arange(len(T)), j] < 1e-3
    s = S[j]
    k = (s[:, 14].astype(np.int64) * 1_000_000 + s[:, 15].astype(np.int64) * 1_000 + s[:, 16].astype(np.int64) * 10
         + s[:, 17].astype(np.int64))
    key[ok] = k[ok]
    return key, int((~ok).sum())


def toy_hash(rows, tru, pv):
    """V4-10 per-event hash: the pre-CKF, pre-merge toy measurements (sid, x, y, z, s0, s1, particle, gen, vsec, dE, t;
    rows sorted by truth position) + their truth positions (float32) + the PV."""
    o = np.lexsort((np.asarray(tru)[:, 2], np.asarray(tru)[:, 1], np.asarray(tru)[:, 0])) if len(rows) else np.zeros(0, int)
    h = hashlib.sha256()
    h.update(np.ascontiguousarray(np.asarray(rows)[o][:, [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12]], np.float64).tobytes())
    h.update(np.ascontiguousarray(np.asarray(tru)[o], np.float32).tobytes())
    h.update(np.ascontiguousarray(np.asarray(pv, np.float64)).tobytes())
    return h.hexdigest()[:24]


def preselect(rows, keys, pv):
    """Exhaustive triples of toy barrel measurements in 3 distinct layers from >= 2 distinct toy particles:
    chi2_3 = lambda_min(sum u u^T / sigma_hat^2) about the stored PV.  -> (preselected, min chi2_3, n_triples)."""
    n = len(rows)
    if n < 3:
        return False, np.inf, 0
    LC = FF.LC_OF[rows[:, 0].astype(np.int64)]
    u = rows[:, 1:4] - pv[None, :]
    sh = sigma_hat(rows, pv)
    w = u / sh[:, None]
    M1 = w[:, :, None] * w[:, None, :]                       # (n, 3, 3)
    a, b = np.triu_indices(n, 1)
    best = np.inf; ntri = 0
    for c in range(2, n):
        m = b < c
        aa = a[m]; bb = b[m]
        ok = (LC[aa] != LC[bb]) & (LC[aa] != LC[c]) & (LC[bb] != LC[c]) & \
             ~((keys[aa] == keys[bb]) & (keys[bb] == keys[c]))
        if not ok.any():
            continue
        aa = aa[ok]; bb = bb[ok]
        ntri += len(aa)
        M = M1[aa] + M1[bb] + M1[c][None]
        lam = np.linalg.eigvalsh(M)[:, 0]
        best = min(best, float(lam.min()))
    return bool(best <= CHI2_PRE), best, ntri


def attribute(X, P, toy_rows_hp, toy_keys_hp, pv, looper=False):
    """Attribution of every candidate (WP_RULE §7).  toy_rows_hp: Hp row indices of the toy pre-merge measurements in
    the pool (links); their Hp rows ARE the stored C'0 measurements (C'_PU: replaced rows).  toy_keys_hp: particle keys.
    -> dict per candidate: attributed (bool), n_links (passing core toy links), n_layers, n_part, max_cross."""
    nc = X['nc']
    att = np.zeros(nc, bool); nl = np.zeros(nc, np.int16); nly = np.zeros(nc, np.int8); npt = np.zeros(nc, np.int8)
    mcr = np.zeros(nc, np.int8)
    n_impl = 0; n_impl_fail = 0
    if nc == 0 or not len(toy_rows_hp):
        return dict(attributed=att, n_links=nl, n_layers=nly, n_part=npt, max_cross=mcr, n_impl=0, n_impl_fail=0)
    Hp = P['Hp']
    pool_of = P['pre_map'][toy_rows_hp]
    R = Hp[toy_rows_hp]
    U = R[:, 1:4] - pv[None, :]
    sh = sigma_hat(R, pv)
    LCt = FF.LC_OF[R[:, 0].astype(np.int64)]
    SDt = FF.SIDE_OF[R[:, 0].astype(np.int64)]
    # pool row -> its toy links
    order = np.argsort(pool_of, kind='stable')
    ps = pool_of[order]
    road_pos = np.full(len(P['H']), -1, np.int64)
    road_pos[X['road_idx']] = np.arange(len(X['road_idx']))
    toy_pool_rows = np.unique(pool_of)
    in_road = road_pos[toy_pool_rows] >= 0
    if not in_road.any():
        return dict(attributed=att, n_links=nl, n_layers=nly, n_part=npt, max_cross=mcr, n_impl=0, n_impl_fail=0)
    toy_road = set(road_pos[toy_pool_rows[in_road]].tolist())
    hoff = X['hoff']; hits = X['hits']
    cid = np.repeat(np.arange(nc), np.diff(hoff))
    has_toy = np.zeros(nc, bool)
    if len(hits):
        th = np.isin(hits, np.fromiter(toy_road, np.int64))
        has_toy[np.unique(cid[th])] = True
    for c in np.where(has_toy)[0]:
        h, core = core_mask(X, c)
        hc = h[core]
        if not len(hc):
            continue
        prow = X['road_idx'][hc]                                  # pool rows of the core hits
        lo = np.searchsorted(ps, prow, 'left'); hi = np.searchsorted(ps, prow, 'right')
        li = np.concatenate([order[lo[q]:hi[q]] for q in range(len(prow))]) if len(prow) else np.zeros(0, int)
        if not len(li):
            continue
        n = X['r']['normal'][c]
        ok = np.abs(U[li] @ n) <= NSIG_ATTR * sh[li]
        li = li[ok]
        if not len(li):
            continue
        lay = LCt[li]
        nl[c] = len(li); nly[c] = len(np.unique(lay)); npt[c] = len(np.unique(toy_keys_hp[li]))
        cnt = np.zeros((10, 3), np.int64)
        np.add.at(cnt, (lay, SDt[li]), 1)
        cr = np.concatenate([cnt[:4, 0], np.minimum(cnt[4:, 1], cnt[4:, 2])])
        mcr[c] = int(min(cr.max(), 127))
        base = len(li) >= 3 and nly[c] >= 3 and bool((lay <= 6).any())
        att[c] = base and (mcr[c] >= 2 if looper else npt[c] >= 2)
        if att[c] and not looper:
            # positive control of the necessity argument (WP_RULE §7 'why f_pre is exact'): the candidate's own passing
            # links must contain a preselection triple (chi2_3 <= 48 about the same PV, same sigma_hat)
            n_impl += 1
            if not preselect(R[li], toy_keys_hp[li], pv)[0]:
                n_impl_fail += 1
    return dict(attributed=att, n_links=nl, n_layers=nly, n_part=npt, max_cross=mcr, n_impl=n_impl,
                n_impl_fail=n_impl_fail)


def replace_toy_rows(ev, tru, toy_ev, toy_tru):
    """C'_PU: the with-PU event's toy measurement rows (vp GUN_VP, re-smeared by ACTS with the PU job's RNG) are replaced
    by the stored C'0 rows (identical pre-merge measurements, WP_RULE §7), matched by SimHit truth position; the CKF
    flag (col 6) is kept from the with-PU event.  -> (ev', n_matched, n_pu_toy_unmatched, n_c0_unmatched)."""
    ev = ev.copy()
    t_idx = np.where(ev[:, 7].astype(np.int64) == GUN_VP)[0]
    if not len(t_idx) or not len(toy_ev):
        return ev, 0, len(t_idx), len(toy_ev)
    d = np.abs(np.asarray(tru, np.float64)[t_idx][:, None, :] - np.asarray(toy_tru, np.float64)[None, :, :]).max(2)
    j = np.argmin(d, 1)
    ok = d[np.arange(len(t_idx)), j] < 1e-4
    jj = j[ok]
    one2one = len(np.unique(jj)) == len(jj)
    if not one2one:
        raise RuntimeError('C\'_PU toy-row matching is not one-to-one')
    rows = t_idx[ok]
    flag = ev[rows, 6].copy()
    ev[rows] = toy_ev[jj]
    ev[rows, 6] = flag
    return ev, int(ok.sum()), int((~ok).sum()), int(len(toy_ev) - ok.sum())


def with_cfg(cfg, **kw):
    return dataclasses.replace(cfg, **kw)
