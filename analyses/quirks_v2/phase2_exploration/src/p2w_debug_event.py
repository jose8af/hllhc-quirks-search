"""p2w_debug_event.py -- one Z(nunu) pilot event: frozen finder candidates next to p2w_subset (Cecilie, 2026-11-19).

  <tt python> p2w_debug_event.py <pilot znn file> <event>
"""
import hashlib
import json
import logging
import sys

import numpy as np

import p2w_subset as W

log = logging.getLogger('p2w_debug_event')


def main(path, i):
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    RS, CI, FF, K, GT, cfg, wcfg = W.load_frozen()
    z = np.load(path); meta = json.loads(str(z['meta'])); ec = meta['evt_cols']; evt = z['evt']
    off = z['hit_off']; s = slice(int(off[i]), int(off[i + 1])); hits = z['hits'][s]; tru = z['tru'][s]
    vtx = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
    h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
    pv = vtx + np.random.default_rng(int.from_bytes(h, 'little')).normal(0, 1, 3) * np.array([0.010, 0.010, 0.015])
    phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
    sid = hits[:, 0].astype(np.int64); b = FF.LC_OF[sid] >= 0
    Hm = CI.merge_pool(hits[b].astype(np.float64), tru[b].astype(np.float64))[0]; sidm = Hm[:, 0].astype(np.int64)
    r = FF.find(Hm, sidm, pv, phim, cfg=cfg, store='loose', want_csr=True)
    V = r['vars']; ax = r['axis']; eta = np.arcsinh(ax[:, 2] / np.hypot(ax[:, 0], ax[:, 1]))
    m = r['road_mask']; LC = FF.LC_OF[sidm[m]]; SD = FF.SIDE_OF[sidm[m]]
    for c in range(len(V['nip2'])):
        hh = r['csr_hits'][r['csr_off'][c]:r['csr_off'][c + 1]]
        a_, b_ = r['seed_ab'][c]
        log.info('finder %d: nit2 %d nip2 %d n2s2 %d nl2 %d w_core %.5f nhit %d dphi %.5f eta %.5f seed layers %d %d sin %.2e',
                 c, V['nit2'][c], V['nip2'][c], V['n2s2'][c], V['nl2'][c], V['dw_core'][c], V['nhit'][c], r['dphi_met'][c],
                 eta[c], LC[a_], LC[b_],
                 np.linalg.norm(np.cross(Hm[m][a_, 1:4] - pv, Hm[m][b_, 1:4] - pv)) / np.linalg.norm(Hm[m][a_, 1:4] - pv) / np.linalg.norm(Hm[m][b_, 1:4] - pv))
        log.info('   hits (layer, side): %s', sorted(zip(LC[hh].tolist(), SD[hh].tolist())))
    kb, nr, ns, npl, ng, bad = W.classify_pool(Hm, pv, phim, cfg, wcfg, FF, K)
    log.info('subset: n_road %d seeds %d planes %d greedy %d', nr, ns, npl, ng)
    log.info('k F s0 per width %s  s3 %s;  k S s0 %s  s3 %s', kb[:, 0, 1], kb[:, 1, 1], kb[:, 0, 0], kb[:, 1, 0])


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))


def seed_refit(path, i, c):
    """The finder's candidate c of event i: its seed through the full-scan refit used by p2w_subset."""
    logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stderr)
    RS, CI, FF, K, GT, cfg, wcfg = W.load_frozen()
    z = np.load(path); meta = json.loads(str(z['meta'])); ec = meta['evt_cols']; evt = z['evt']
    off = z['hit_off']; s = slice(int(off[i]), int(off[i + 1])); hits = z['hits'][s]; tru = z['tru'][s]
    vtx = evt[i, [ec.index('vtx_x'), ec.index('vtx_y'), ec.index('vtx_z')]]
    h = hashlib.blake2b(f'p2t-pv|{meta["stream"]}|{meta["chunk"]}|{i}'.encode(), digest_size=8).digest()
    pv = vtx + np.random.default_rng(int.from_bytes(h, 'little')).normal(0, 1, 3) * np.array([0.010, 0.010, 0.015])
    phim = float((evt[i, ec.index('phimet_reco_v1')] + np.pi) % (2 * np.pi) - np.pi)
    sid = hits[:, 0].astype(np.int64); b = FF.LC_OF[sid] >= 0
    Hm = CI.merge_pool(hits[b].astype(np.float64), tru[b].astype(np.float64))[0]; sidm = Hm[:, 0].astype(np.int64)
    r = FF.find(Hm, sidm, pv, phim, cfg=cfg, store='loose', want_csr=True)
    m = r['road_mask']
    U = np.ascontiguousarray(Hm[m, 1:4] - pv[None, :]); n = len(U)
    sd = sidm[m]; LC = FF.LC_OF[sd]; SD = FF.SIDE_OF[sd]; J = FF.JLOC_OF[sd]
    rH = np.hypot(Hm[m, 1], Hm[m, 2])
    P = np.empty((6, n)); P[:3] = U.T; P[3] = Hm[m, 1] / rH; P[4] = Hm[m, 2] / rH; P[5] = np.linalg.norm(U, axis=1)
    SF = np.zeros((16, 8))
    for j in range(16):
        if (J == j).any():
            SF[j, 3] = Hm[m, 4][J == j][0]; SF[j, 4] = Hm[m, 5][J == j][0]
            log.info('surface %d: sigma constant %s', j, bool(np.all(Hm[m, 4][J == j] == SF[j, 3]) and np.all(Hm[m, 5][J == j] == SF[j, 4])))
    ia, ib = r['seed_ab'][c]
    n0 = np.cross(U[ia], U[ib]); n0 /= np.linalg.norm(n0)
    a0 = U[ia] / P[5, ia] + U[ib] / P[5, ib]; a0 /= np.linalg.norm(a0)
    L = np.where(np.abs(U @ n0) < np.where(LC >= 7, 60.0, 5.0))[0].astype(np.int64)
    out = K.refit_packed(L, len(L), P, J, LC, SD, np.arange(n).astype(np.int64), n0, a0, float(cfg.w_c), int(cfg.iters),
                         float(cfg.t_tol), 2.5, SF, np.empty(n, np.int64), np.zeros((3, 3)), np.zeros((10, 3), np.int64),
                         np.empty(16), np.empty(n, np.int64), np.empty(n), 0, n0[0], n0[1], n0[2])
    log.info('full-scan refit of the finder seed: status %d nl2 %d nit2 %d nsel %d nfin %d; finder normal %s mine %s', out[0],
             out[4], out[5], out[7], out[12], r['normal'][c], out[1:4])
    log.info('finder hits %s', r['csr_hits'][r['csr_off'][c]:r['csr_off'][c + 1]].tolist())


if __name__ == '__main__' and len(sys.argv) > 3:
    seed_refit(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
