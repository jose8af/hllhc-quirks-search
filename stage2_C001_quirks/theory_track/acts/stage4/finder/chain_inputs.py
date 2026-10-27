"""TT-side event preparation for the G1 production chain (acts/stage4/code/run_chain.py), 2026-10-13.  Signal-blind.

From one G1 chain event (ev: (n, 13) COLS sid, x, y, z, s0, s1, flag, vp, particle, gen, vsec, dE, t; tru: (n, 3) truth
positions; vz: per-interaction vertices) this builds the finder's hit pool of plan §1.1 / §1.4-§1.6, in this order
(WP_RULE §1.1 "the hit pool after CKF removal, analysis-level merging and the hit-time window"):

  1. barrel counting surfaces + BTL;  exact interaction ids INT = tag * 10^6 + vp (G1 reader: vp is the interaction);
  2. TDR top-up (plan §1.4, D4-15): pu_inputs.topup, unchanged (ratios x the event's own pre-CKF Fatras crossings per
     layer, z / dE / t resampled from the layer's pre-CKF hits, phi uniform, one interaction per top-up crossing);
  3. CKF removal (plan §1.6 item 1): Fatras measurements with flag bit0 (on a selected CKF track: pT > 0.9 GeV, >= 7
     measurements, <= 2 holes, |d0| < 4 mm) leave the pool; they are returned separately (f_CKF band counts, D5);
  4. analysis-level merging (plan §1.5, U-5 b): on each barrel sensor (Stage-3 surface id; the 32 phi-sectors are one
     geometric surface) two measurements merge when |du| < p_u and |dv| < p_v at their TRUTH positions (u = R phi,
     v = z; top-up crossings: their generated position).  Connected components merge into one measurement: position =
     mean of the measured (phi, z) on the nominal radius, sigma_u/v = the surface sigma (see merge_pool), dE = sum, t = min,
     truth link = the member with the largest dE, flag bit1 = merged.  Pitches (plan §1.5 table): IT 25 um x 100 um,
     PS 100 um x 1.467 mm, 2S 90 um x 50.27 mm; scale 1 (nominal) or 2 (the 2-pitch variation);
  5. (signal only, not used here) hit-time window and hit efficiency.
The finder input is the barrel pool; BTL hits are returned separately (SR-T offline, S5).
"""
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

from . import finder as FF
from . import pu_inputs as PI

KIND = PI.KIND
PITCH = {'IT': (0.025, 0.100), 'PS': (0.100, 1.467), '2S': (0.090, 50.27)}      # mm (u = r phi, v = z)
RAD = np.array([s['p0'] * 10.0 if s['type'] == 0 else np.nan for s in FF.S])
BARREL_SIDS = np.where(FF.LC_OF >= 0)[0]


def merge_pool(H, T, scale=1.0):
    """Analysis-level merging (U-5 b).  H (n, 13) measurements, T (n, 3) truth positions.
    Returns (H_merged (m, 13), member -> merged index (n,), n_groups_merged, n_hits_in_merged, n_sigma_enlarged)."""
    n = len(H)
    if n == 0:
        return H.copy(), np.zeros(0, np.int64), 0, 0, 0
    sid = H[:, 0].astype(np.int64)
    rows = []; cols = []
    for s in np.unique(sid):
        k = KIND[s]
        if k not in PITCH:
            continue
        pu, pv = PITCH[k]; pu *= scale; pv *= scale
        idx = np.where(sid == s)[0]
        if len(idx) < 2:
            continue
        R = RAD[s]
        uu = R * np.arctan2(T[idx, 1], T[idx, 0])
        vv = T[idx, 2]
        o = np.argsort(uu, kind='stable')
        u_s = uu[o]; v_s = vv[o]; i_s = idx[o]
        # wrap: append the head (u + 2 pi R) so pairs across phi = +-pi are seen
        circ = 2 * np.pi * R
        head = u_s - u_s[0] < pu
        u_e = np.concatenate([u_s, u_s[head] + circ]); v_e = np.concatenate([v_s, v_s[head]])
        i_e = np.concatenate([i_s, i_s[head]])
        m = len(u_s)
        for sh in range(1, len(u_e)):
            du = u_e[sh:sh + m] - u_e[:len(u_e[sh:sh + m])]
            ok = du < pu
            if not ok.any():
                break
            a = np.arange(len(du))[ok]
            close = np.abs(v_e[a + sh] - v_e[a]) < pv
            a = a[close]
            if len(a):
                ia = i_e[a]; ib = i_e[a + sh]
                ne = ia != ib
                rows.append(ia[ne]); cols.append(ib[ne])
    if not rows or sum(len(r) for r in rows) == 0:
        return H.copy(), np.arange(n), 0, 0, 0
    r = np.concatenate(rows); c = np.concatenate(cols)
    g = coo_matrix((np.ones(len(r), np.int8), (r, c)), shape=(n, n))
    ncomp, lab = connected_components(g, directed=False)
    size = np.bincount(lab, minlength=ncomp)
    # keep the original order: the merged measurement sits at the first member's position in the output
    first = np.full(ncomp, n, np.int64)
    np.minimum.at(first, lab, np.arange(n))
    order = np.argsort(first, kind='stable')
    newidx = np.empty(ncomp, np.int64); newidx[order] = np.arange(ncomp)
    out = H[first[order]].copy()
    multi = np.where(size > 1)[0]
    n_enl = 0
    for cpt in multi:
        mem = np.where(lab == cpt)[0]
        hm = H[mem]
        s = int(hm[0, 0]); R = RAD[s]
        ph = np.arctan2(hm[:, 2], hm[:, 1])
        ph0 = ph[0]
        dph = (ph - ph0 + np.pi) % (2 * np.pi) - np.pi
        phm = ph0 + dph.mean()
        vM = hm[:, 3]
        # plan error max(sigma, |Delta|/sqrt12) with Delta the TRUTH separation (the quantity of the merge test).  For a
        # pair |Delta| < pitch, so it equals sigma = pitch/sqrt12 always; only >= 3-member chains (or the 2-pitch
        # variation) can enlarge it.  The finder assumes a per-surface constant sigma (finder.build_index), so the
        # pool keeps the surface sigma and the enlargement is only counted (n_enlarged; G1_REPORT deviation 3).
        tph = np.arctan2(T[mem, 1], T[mem, 0])
        tu = R * ((tph - tph[0] + np.pi) % (2 * np.pi) - np.pi); tv = T[mem, 2]
        j = newidx[cpt]
        best = mem[np.argmax(H[mem, 11])]
        row = H[best].copy()
        row[1] = R * np.cos(phm); row[2] = R * np.sin(phm); row[3] = vM.mean()
        row[4] = hm[:, 4].max(); row[5] = hm[:, 5].max()
        if (tu.max() - tu.min()) / np.sqrt(12.0) > row[4] or (tv.max() - tv.min()) / np.sqrt(12.0) > row[5]:
            n_enl += 1
        row[6] = float(int(row[6]) | 2)
        row[11] = hm[:, 11].sum()
        row[12] = hm[:, 12].min()
        out[j] = row
    return out, newidx[lab], int(len(multi)), int(size[multi].sum()), n_enl


def prepare_event(ev, tru, vz, tag, rng, do_topup=True, ratios=None, ckf_remove=True, merge=True, merge_scale=1.0):
    """-> dict(H, sid, INT (finder pool), btl, btl_INT, uz, ckf (CKF-removed barrel hits, 13 cols), stats)."""
    sid_all = ev[:, 0].astype(np.int64)
    INT_all = tag * 1_000_000 + ev[:, 7].astype(np.int64)
    bar = FF.LC_OF[sid_all] >= 0
    btl = KIND[sid_all] == 'BTL'
    H0 = ev[bar]; s0 = sid_all[bar]; I0 = INT_all[bar]; T0 = tru[bar].astype(np.float64)
    st = dict(n_fatras=int(len(H0)))
    if do_topup:
        t, ti = PI.topup(H0, s0, rng, tag, ratios)
    else:
        t, ti = np.zeros((0, H0.shape[1])), np.zeros(0, np.int64)
    st['n_topup'] = int(len(t))
    ck = (H0[:, 6].astype(np.int64) & 1) == 1 if ckf_remove else np.zeros(len(H0), bool)
    st['n_ckf_removed'] = int(ck.sum())
    Hp = np.concatenate([H0[~ck], t]); Ip = np.concatenate([I0[~ck], ti])
    Tp = np.concatenate([T0[~ck], t[:, 1:4]])
    if merge:
        Hm, mapi, ng, nh, nenl = merge_pool(Hp, Tp, merge_scale)
        first = np.full(len(Hm), -1, np.int64)
        # INT of the merged measurement: that of its truth-link member (largest dE); diagnostics/thinning approximation
        Im = np.zeros(len(Hm), np.int64)
        Im[mapi] = Ip          # last writer wins; fix for merged ones below
        if ng:
            sz = np.bincount(mapi, minlength=len(Hm))
            for j in np.where(sz > 1)[0]:
                mem = np.where(mapi == j)[0]
                Im[j] = Ip[mem[np.argmax(Hp[mem, 11])]]
        del first
    else:
        Hm, mapi, ng, nh, Im, nenl = Hp, np.arange(len(Hp)), 0, 0, Ip, 0
    st.update(n_pool=int(len(Hm)), n_merged_groups=ng, n_merged_hits=nh, n_sigma_enlarged=nenl)
    uz = np.array(sorted(set(np.round(vz[:, 3], 6)))) if len(vz) else np.zeros(0)
    return dict(H=Hm, sid=Hm[:, 0].astype(np.int64), INT=Im, btl=ev[btl], btl_INT=INT_all[btl], uz=uz, ckf=H0[ck],
                pre_map=mapi, stats=st)


def ckf_band_counts(ckfH, pv, phimet, normals, axes, w_c=75.0, road=0.25, t_tol=0.030, chunk=256):
    """Number of CKF-removed barrel measurements inside each candidate's collection band (WP_RULE §1.1 items 1, 3:
    road, |n.u| < 3 sigma_tot with sigma_tot^2 = max(sigma_n, 1e-4)^2 + t_tol^2, forward u.n3 > 0, |u.n2| < W_c).
    f_CKF (DRAFT-D5) = n_ckf_band / (n_ckf_band + candidate in-band hits).  Not a cut here (stored only)."""
    nc = len(normals)
    out = np.zeros(nc, np.int32)
    if nc == 0 or len(ckfH) == 0:
        return out
    U = ckfH[:, 1:4] - pv[None, :]
    r = np.hypot(U[:, 0], U[:, 1])
    dph = np.abs((np.arctan2(U[:, 1], U[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
    m = dph < road + np.arcsin(np.minimum(1.0, w_c / r))
    U = U[m]
    if len(U) == 0:
        return out
    cx = ckfH[m, 1] / np.hypot(ckfH[m, 1], ckfH[m, 2]); cy = ckfH[m, 2] / np.hypot(ckfH[m, 1], ckfH[m, 2])
    s0 = ckfH[m, 4]; s1 = ckfH[m, 5]
    N = np.asarray(normals, np.float64); A = np.asarray(axes, np.float64)
    N2 = np.cross(N, A)
    for a in range(0, nc, chunk):
        n = N[a:a + chunk]; ax = A[a:a + chunk]; n2 = N2[a:a + chunk]
        d = n @ U.T
        sn = np.sqrt((-n[:, 0:1] * cy[None] + n[:, 1:2] * cx[None]) ** 2 * s0[None] ** 2 + n[:, 2:3] ** 2 * s1[None] ** 2)
        st2 = np.maximum(sn, 1e-4) ** 2 + t_tol ** 2
        ok = (d * d < 9.0 * st2) & ((ax @ U.T) > 0) & (np.abs(n2 @ U.T) < w_c)
        out[a:a + chunk] = ok.sum(1)
    return out
