"""p2x_mbgen.py -- pilot minimum bias, generator level (stream pilot.mb): p2c_mbgen with a second, wider parent pool.

  <acts python> p2x_mbgen.py <out.npz> <n_interactions> <stream> <chunk> [keep_xpool=1]

Same generator, seeds, histograms and v1 road rates as Tatiana's p2c_mbgen.generate (its loop is repeated here with
the pool cut widened; p2c_mbgen.py is imported for its constants and generator and is not modified; the first version
of this file changed p2c_mbgen.POOL_PT at run time, which also changed the v1 rates: found on slice p2-c-px-mb, fixed).
  pool_*    the pool of addendum 1 v2, P2: pi+-, K+-, p, K0L, n, gamma produced within 1 mm of the interaction point,
            0.5 < pT < 20 GeV, |eta| < 1  (float64 cuts, exactly the rows of p2c_mbgen)
  xpool_*   the same species and production cut OUTSIDE that phase space but inside 0.3 < pT < 20 GeV, |eta| < 1.5:
            the parents of check samples below the pT edge and beyond |eta| = 1 (review of addendum v2, B-2).  Written
            if keep_xpool = 1; its numbers per interaction are always in meta.
Arrays per pool: *_int (interaction index), *_pdg, *_pt, *_eta, *_phi.  Side file <out>.sha.json: content hash.
"""
import sys
import time

import numpy as np

import p2c_common as C
import p2x_common as X
import p2c_mbgen as MB

s4pu = MB.s4pu
log = C.setup_logging('p2x_mbgen')
XPOOL_PT = (0.3, 20.0)
XPOOL_ETA = 1.5


def generate(n_int, stream, chunk):
    gen = MB.make_gen()
    job_seed = C.qv2_seed(stream, chunk)
    rng = np.random.default_rng(s4pu.hseed('p2c-mb', job_seed, mod=2 ** 63))          # as p2c_mbgen.generate
    seeds = rng.integers(1, 900_000_000, n_int)
    hist = np.zeros((len(MB.SPECIES), len(MB.PT_BINS) + 1, len(MB.ETA_BINS) + 1))
    histp = np.zeros_like(hist)
    pool = []; xpool = []
    rate = dict(dif=0.0, ni=0.0, n_dif_parents=0.0, n_ni_parents=0.0)
    n_final = 0
    t0 = time.process_time()
    for k in range(n_int):
        parts, _ = gen.generate(int(seeds[k]))
        a = np.array(parts, float)
        if not len(a):
            continue
        n_final += len(a)
        apdg = np.abs(a[:, 0]).astype(np.int64)
        sp = np.array([MB.SP_OF.get(int(x), 8) for x in apdg])
        pt = np.hypot(a[:, 3], a[:, 4])
        pabs = np.sqrt(pt ** 2 + a[:, 5] ** 2)
        eta = np.arctanh(np.clip(a[:, 5] / np.maximum(pabs, 1e-300), -1 + 1e-15, 1 - 1e-15))
        phi = np.arctan2(a[:, 4], a[:, 3])
        prompt = (np.abs(a[:, 7]) + np.abs(a[:, 8]) + np.abs(a[:, 9])) == 0
        ip = np.digitize(pt, MB.PT_BINS); ie = np.digitize(np.abs(eta), MB.ETA_BINS)
        np.add.at(hist, (sp, ip, ie), 1.0)
        np.add.at(histp, (sp[prompt], ip[prompt], ie[prompt]), 1.0)
        # v1 road-object rates, cuts of gen_d123.road_objects as in p2c_mbgen l.75-84 (fixed numbers, not the pool cut)
        cen = prompt & (np.abs(eta) < 1.0) & (pt > 0.5)
        inw = np.abs(phi) < MB.W_ROAD
        mni = cen & inw & np.isin(apdg, (211, 321, 2212)) & (pt < 20.0) & (a[:, 1] != 0)
        rate['ni'] += float(np.cosh(eta[mni]).sum()); rate['n_ni_parents'] += float(mni.sum())
        mdf = cen & inw & np.isin(apdg, (211, 321)) & (pt < 10.0)
        if mdf.any():
            lam = pt[mdf] / np.where(apdg[mdf] == 321, MB.MK, MB.MPI) * np.where(apdg[mdf] == 321, MB.CT_K, MB.CT_PI)
            rate['dif'] += float((np.exp(-30.0 / lam) - np.exp(-1000.0 / lam)).sum())
            rate['n_dif_parents'] += float(mdf.sum())
        near = (np.hypot(a[:, 7], a[:, 8]) < 1.0) & (np.abs(a[:, 9]) < 1.0) & (sp <= 5)
        mp = near & (np.abs(eta) < 1.0) & (pt > 0.5) & (pt < 20.0)                         # p2c_mbgen l.88
        mx = near & ~mp & (np.abs(eta) < XPOOL_ETA) & (pt > XPOOL_PT[0]) & (pt < XPOOL_PT[1])
        for m, dst in ((mp, pool), (mx, xpool)):
            if m.any():
                dst.append(np.c_[np.full(m.sum(), k), a[m, 0], pt[m], eta[m], phi[m]])
    cpu = time.process_time() - t0
    P = np.concatenate(pool) if pool else np.zeros((0, 5))
    Q = np.concatenate(xpool) if xpool else np.zeros((0, 5))
    road = 2 * MB.W_ROAD / (2 * np.pi)
    q_lo = (Q[:, 2] <= 0.5) & (np.abs(Q[:, 3]) < 1.0); q_fw = (Q[:, 2] > 0.5) & (np.abs(Q[:, 3]) >= 1.0)
    species = (211, 321, 2212, 130, 2112, 22)
    meta = dict(mode='mbgen-x', stream=stream, chunk=chunk, job_seed=job_seed, n_int=n_int, species=MB.SPECIES,
                pool_phase_space=dict(pt=(0.5, 20.0), abs_eta_max=1.0, production_within_mm=1.0, species=MB.SPECIES[:6]),
                xpool_phase_space=dict(pt=XPOOL_PT, abs_eta_max=XPOOL_ETA, production_within_mm=1.0, excludes='the pool phase space'),
                rate_per_interaction_in_road={k: v / n_int for k, v in rate.items()}, w_road=MB.W_ROAD,
                n_final_per_interaction=n_final / n_int, n_pool=int(len(P)), n_xpool=int(len(Q)),
                n_pool_per_interaction=len(P) / n_int, n_xpool_per_interaction=len(Q) / n_int,
                n_lowpt_per_interaction=float(q_lo.sum()) / n_int, n_fwd_per_interaction=float(q_fw.sum()) / n_int,
                pool_in_road_per_interaction=len(P) / n_int * road, lowpt_in_road_per_interaction=float(q_lo.sum()) / n_int * road,
                pool_species={str(s): int((np.abs(P[:, 1]) == s).sum()) for s in species},
                xpool_species={str(s): int((np.abs(Q[:, 1]) == s).sum()) for s in species},
                cpu_ms_per_interaction=1e3 * cpu / n_int, base_lines=list(s4pu.PY_MB),
                code_sha256=dict(C.code_hashes(), **X.src_hashes('p2x_mbgen.py', 'p2c_mbgen.py', 'p2c_common.py', 'p2x_common.py')),
                input_sha256=X.input_hashes())
    arrays = dict(hist=hist, hist_prompt=histp, pt_bins=MB.PT_BINS, eta_bins=MB.ETA_BINS)
    for pre, A in (('pool', P), ('xpool', Q)):
        arrays.update({f'{pre}_int': A[:, 0].astype(np.int32), f'{pre}_pdg': A[:, 1].astype(np.int32),
                       f'{pre}_pt': A[:, 2].astype(np.float32), f'{pre}_eta': A[:, 3].astype(np.float32),
                       f'{pre}_phi': A[:, 4].astype(np.float32)})
    return arrays, meta


def run(out, n_int, stream, chunk, keep_xpool=True):
    arrays, meta = generate(n_int, stream, chunk)
    meta['xpool_kept'] = bool(keep_xpool)
    if not keep_xpool:
        arrays = {k: v for k, v in arrays.items() if not k.startswith('xpool_')}
    X.save(out, arrays, meta)
    X.write_sha(str(out) + '.sha.json', dict(job=dict(stream=stream, chunk=chunk, job_seed=meta['job_seed']),
                                             files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
    log.info('%s', {k: meta[k] for k in ('n_int', 'cpu_ms_per_interaction', 'n_pool_per_interaction', 'n_xpool_per_interaction',
                                         'n_lowpt_per_interaction', 'n_fwd_per_interaction', 'rate_per_interaction_in_road',
                                         'bytes', 'content_sha256')})


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], int(a[1]), a[2], int(a[3]), bool(int(a[4])) if len(a) > 4 else True)
