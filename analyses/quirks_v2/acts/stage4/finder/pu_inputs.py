"""Production PU-only trial inputs (TT level), Phase A.  Signal-blind.

From one chain event (measurement rows, columns pu_chain_interim.COLS = sid, x, y, z, s0, s1, flag, vp, particle, gen,
vsec, dE, t) this builds the TDR-normalised event of plan §1.4: the barrel counting-layer hits, interaction ids, and the
per-layer top-up.  The top-up is the f1r one (TOPUP ratios, z resampled from the layer's hits, phi uniform, one
interaction per top-up crossing, stacked layers get an in/out pair at the same (phi, z)) with ONE change (Phase A):
the top-up hit's dE and time are resampled from the same sensor's own Fatras hits, because f1r set dE = 0, which would
bias the PU dE/dx low (anti-conservative for the dE/dx rungs; 63 % of the IT hits of a normalised event are top-up).
The finder output does not depend on dE or t, so G2a t1 and the equivalence test are unaffected.
BTL hits are returned separately (SR-T, F1 offline).  Interaction ids are trial-local (tag * 10^6 + ...).
"""
import numpy as np

from . import finder as FF

TOPUP = {'TBPX_L1': 2.77, 'TBPX_L2': 2.26, 'TBPX_L3': 2.81, 'TBPX_L4': 3.72, 'TBPS_L1': 2.56, 'TBPS_L2': 3.25,
         'TBPS_L3': 4.31, 'TB2S_L1': 4.00, 'TB2S_L2': 5.16, 'TB2S_L3': 7.27}     # = f1r_finder.TOPUP (nominal, V4-2)
KIND = np.array([s['kind'] for s in FF.S])
RAD = {i: s['p0'] * 10.0 for i, s in enumerate(FF.S) if s['type'] == 0}
NCOL = 13


def interaction_ids(e, vz, tag):
    """f1r_finder.interaction_ids: ACTS vertexPrimary -> interaction by the vertex's smeared z (prompt vertices of one
    interaction share it; Pythia displaced-decay vertices get their own id -- an INTERIM limitation, exact ids come
    with the G1 SimParticle reader)."""
    zkey = {int(v[0]): round(float(v[3]), 6) for v in vz}
    uz = {z: i for i, z in enumerate(sorted(set(zkey.values())))}
    vp = e[:, 7].astype(np.int64)
    ids = np.array([uz.get(zkey.get(int(x), -1e9), 99999) for x in vp], np.int64)
    return tag * 1_000_000 + ids, np.array(sorted(uz))


def topup(e, sid, rng, tag, ratios=None):
    ratios = ratios or TOPUP
    rows = []
    k = 0
    for li, name in enumerate(FF.LAYERS):
        f = ratios[name] - 1.0
        ids = [FF.SID[name]] if li < 4 else [FF.SID[name + '_in'], FF.SID[name + '_out']]
        on0 = sid == ids[0]
        z_pool = e[on0, 3]
        if len(z_pool) == 0:
            continue
        ntop = rng.poisson(f * len(z_pool))
        zs = rng.choice(z_pool, ntop)
        ph = rng.uniform(-np.pi, np.pi, ntop)
        for s_ in ids:
            on = sid == s_
            Rr = RAD[s_]
            blk = np.zeros((ntop, NCOL))
            blk[:, 0] = s_
            blk[:, 1] = Rr * np.cos(ph); blk[:, 2] = Rr * np.sin(ph); blk[:, 3] = zs
            blk[:, 4:6] = e[on][0, 4:6]
            blk[:, 6] = 0; blk[:, 7] = -1; blk[:, 8] = -1; blk[:, 9] = -1; blk[:, 10] = 0
            j = rng.integers(0, on.sum(), ntop)
            blk[:, 11] = e[on][j, 11]                 # dE resampled from this sensor's Fatras hits (Phase A)
            blk[:, 12] = e[on][j, 12]                 # time likewise
            rows.append((blk, tag * 1_000_000 + 500_000 + k + np.arange(ntop)))
        k += ntop
    if not rows:
        return np.zeros((0, NCOL)), np.zeros(0, np.int64)
    return np.concatenate([r[0] for r in rows]), np.concatenate([r[1] for r in rows])


def build_event(meas, vz, tag, rng, do_topup=True, ratios=None):
    """-> dict(H (n, 13) barrel counting hits incl. top-up, sid, INT, btl (m, 13), btl_INT, uz (prompt vertex z))."""
    sid_all = meas[:, 0].astype(np.int64)
    INT_all, uz = interaction_ids(meas, vz, tag)
    bar = FF.LC_OF[sid_all] >= 0
    btl = KIND[sid_all] == 'BTL'
    H = meas[bar]; sid = sid_all[bar]; INT = INT_all[bar]
    if do_topup:
        t, ti = topup(H, sid, rng, tag, ratios)
        H = np.concatenate([H, t]); sid = np.concatenate([sid, t[:, 0].astype(np.int64)]); INT = np.concatenate([INT, ti])
    return dict(H=H, sid=sid, INT=INT, btl=meas[btl], btl_INT=INT_all[btl], uz=uz)


def lum_pv(rng):
    """PU-only trial PV: luminous-region point (sigma_xy 5 um, sigma_z 45 mm), independent of the PU vertices (§4.1)."""
    return np.array([rng.normal(0, 5e-3), rng.normal(0, 5e-3), rng.normal(0, 45.0)])
