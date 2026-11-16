"""p2x_mbgen.py -- pilot minimum bias, generator level: p2c_mbgen.generate with a second, low-pT parent pool.

  <acts python> p2x_mbgen.py <out.npz> <n_interactions> <stream> <chunk> [lowpt_min=0.3] [keep_lowpt_pool=1]

p2c_mbgen.py is not modified: its module constant POOL_PT is set at run time to (lowpt_min, 20) and the pool it
returns is split here at pT = 0.5 GeV (on the stored float32 values):
  pool_*   0.5 < pT < 20 GeV  (the pool of addendum 1 v2, P2: pi+-, K+-, p, K0L, n, gamma within 1 mm, |eta| < 1)
  lowpt_*  lowpt_min < pT <= 0.5 GeV, same species and cuts (check sample `pilot.c0.lowpt`); written only if
           keep_lowpt_pool = 1; its number per interaction is always in meta (the N_t input of that sample)
Histograms, v1 road rates and seeds are those of p2c_mbgen.generate (the generator stream does not depend on the pool
cut).  Side file <out>.sha.json: content hash.
"""
import sys

import numpy as np

import p2c_common as C
import p2x_common as X
import p2c_mbgen as MB

log = C.setup_logging('p2x_mbgen')
PT_SPLIT = 0.5


def run(out, n_int, stream, chunk, lowpt_min=0.3, keep_lowpt=True):
    MB.POOL_PT = (float(lowpt_min), 20.0)
    arrays, meta = MB.generate(n_int, stream, chunk)
    hi = arrays['pool_pt'] > np.float32(PT_SPLIT)
    full = {k: arrays[k] for k in ('pool_int', 'pool_pdg', 'pool_pt', 'pool_eta', 'pool_phi')}
    for k, a in full.items():
        arrays[k] = a[hi]
        if keep_lowpt:
            arrays[k.replace('pool_', 'lowpt_')] = a[~hi]
    n_hi = int(hi.sum()); n_lo = int((~hi).sum())
    road = 2 * MB.W_ROAD / (2 * np.pi)
    sp = {str(a): int((np.abs(full['pool_pdg'][hi]) == a).sum()) for a in (211, 321, 2212, 130, 2112, 22)}
    sp_lo = {str(a): int((np.abs(full['pool_pdg'][~hi]) == a).sum()) for a in (211, 321, 2212, 130, 2112, 22)}
    meta.update(mode='mbgen-x', pool_phase_space=dict(pt=(PT_SPLIT, 20.0), abs_eta_max=MB.POOL_ETA, production_within_mm=1.0,
                                                      species=MB.SPECIES[:6]),
                lowpt_phase_space=dict(pt=(float(lowpt_min), PT_SPLIT)), lowpt_pool_kept=bool(keep_lowpt),
                n_pool=n_hi, n_lowpt=n_lo, n_pool_per_interaction=n_hi / n_int, n_lowpt_per_interaction=n_lo / n_int,
                pool_in_road_per_interaction=n_hi / n_int * road, lowpt_in_road_per_interaction=n_lo / n_int * road,
                pool_species=sp, lowpt_species=sp_lo,
                code_sha256=dict(C.code_hashes(), **X.src_hashes('p2x_mbgen.py', 'p2c_mbgen.py', 'p2c_common.py', 'p2x_common.py')),
                input_sha256=X.input_hashes())
    X.save(out, arrays, meta)
    X.write_sha(str(out) + '.sha.json', dict(job=dict(stream=stream, chunk=chunk, job_seed=meta['job_seed']),
                                             files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
    log.info('%s', {k: meta[k] for k in ('n_int', 'cpu_ms_per_interaction', 'n_pool_per_interaction',
                                         'n_lowpt_per_interaction', 'rate_per_interaction_in_road', 'bytes', 'content_sha256')})


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], int(a[1]), a[2], int(a[3]), float(a[4]) if len(a) > 4 else 0.3, bool(int(a[5])) if len(a) > 5 else True)
