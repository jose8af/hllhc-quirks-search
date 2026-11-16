"""p2c_mbgen.py -- generator-level minimum bias (pilot of STR §4.4 pt 5: spectra, rates, primaries for Geant4).

  <acts python> p2c_mbgen.py <out.npz> <n_interactions> <stream> <chunk>

Generator: the production minimum bias unchanged (s4pu.PythiaGen with PY_MB + CP5, 14 TeV, pi+-, K+-, mu, K0L stable).
Output:
  hist (9, 62, 22)   final-state particles per species (SPECIES) in pT (PT_BINS, 60 log bins 0.05-50 GeV, with
                     under/overflow) and |eta| (ETA_BINS, 20 bins 0-5, with overflow); prompt and displaced together
  hist_prompt        the same for prompt particles only (production point = interaction point)
  pool_*             the primaries of the v1 rate phase space (gen_d123.road_objects without the road cut):
                     pi+-, K+-, p, K0L, n, gamma produced within 1 mm of the interaction point, 0.5 < pT < 20 GeV,
                     |eta| < 1: interaction index, pdg, pT, eta, phi
  meta               rates per interaction of the v1 road objects (road at phi = 0, half-width 0.15): 'dif' (sum of the
                     decay probability between r = 30 and 1000 mm) and 'ni' (sum of cosh eta), as gen_d123 l.141-169
"""
import math
import os
import sys
import time

import numpy as np

import p2c_common as C

sys.path.insert(0, str(C.CODE))
import s4pu  # noqa: E402

log = C.setup_logging('p2c_mbgen')
CP5 = C.QV2 / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
SPECIES = ['pi', 'K', 'p', 'K0L', 'n', 'gamma', 'e', 'mu', 'other']
SP_OF = {211: 0, 321: 1, 2212: 2, 130: 3, 2112: 4, 22: 5, 11: 6, 13: 7}
PT_BINS = np.geomspace(0.05, 50.0, 61)
ETA_BINS = np.linspace(0.0, 5.0, 21)
POOL_PT = (0.5, 20.0)
POOL_ETA = 1.0
W_ROAD = 0.15
MK, MPI, CT_K, CT_PI = 0.493677, 0.13957039, 3712.0, 7804.5        # as acts/stage4/analysis/gen_d123.py l.51, l.166


def make_gen():
    lines, mv = s4pu.mpi_init_lines(C.QV2)
    gen = s4pu.PythiaGen(CP5, extra_lines=lines)
    if mv is not None:
        os.replace(mv[0], mv[1])
    return gen


def generate(n_int, stream, chunk, gen=None):
    gen = gen or make_gen()
    job_seed = C.qv2_seed(stream, chunk)
    rng = np.random.default_rng(s4pu.hseed('p2c-mb', job_seed, mod=2 ** 63))
    seeds = rng.integers(1, 900_000_000, n_int)
    hist = np.zeros((len(SPECIES), len(PT_BINS) + 1, len(ETA_BINS) + 1))
    histp = np.zeros_like(hist)
    pool = []
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
        sp = np.array([SP_OF.get(int(x), 8) for x in apdg])
        pt = np.hypot(a[:, 3], a[:, 4])
        pabs = np.sqrt(pt ** 2 + a[:, 5] ** 2)
        eta = np.arctanh(np.clip(a[:, 5] / np.maximum(pabs, 1e-300), -1 + 1e-15, 1 - 1e-15))
        phi = np.arctan2(a[:, 4], a[:, 3])
        prompt = (np.abs(a[:, 7]) + np.abs(a[:, 8]) + np.abs(a[:, 9])) == 0
        ip = np.digitize(pt, PT_BINS); ie = np.digitize(np.abs(eta), ETA_BINS)
        np.add.at(hist, (sp, ip, ie), 1.0)
        np.add.at(histp, (sp[prompt], ip[prompt], ie[prompt]), 1.0)
        cen = prompt & (np.abs(eta) < POOL_ETA) & (pt > POOL_PT[0])
        inw = np.abs(phi) < W_ROAD
        # v1 road-object rates (gen_d123.road_objects): charged prompt, in the road
        mni = cen & inw & np.isin(apdg, (211, 321, 2212)) & (pt < 20.0) & (a[:, 1] != 0)
        rate['ni'] += float(np.cosh(eta[mni]).sum()); rate['n_ni_parents'] += float(mni.sum())
        mdf = cen & inw & np.isin(apdg, (211, 321)) & (pt < 10.0)
        if mdf.any():
            lam = pt[mdf] / np.where(apdg[mdf] == 321, MK, MPI) * np.where(apdg[mdf] == 321, CT_K, CT_PI)
            rate['dif'] += float((np.exp(-30.0 / lam) - np.exp(-1000.0 / lam)).sum())
            rate['n_dif_parents'] += float(mdf.sum())
        # pool: produced within 1 mm of the interaction point (v1's exact-zero 'prompt' test drops the daughters of
        # eta, eta' and pi0, whose Pythia production point is displaced by nanometres; photons had no such cut in v1)
        near = (np.hypot(a[:, 7], a[:, 8]) < 1.0) & (np.abs(a[:, 9]) < 1.0)
        mp = near & (np.abs(eta) < POOL_ETA) & (pt > POOL_PT[0]) & (pt < POOL_PT[1]) & (sp <= 5)
        if mp.any():
            pool.append(np.c_[np.full(mp.sum(), k), a[mp, 0], pt[mp], eta[mp], phi[mp]])
    cpu = time.process_time() - t0
    P = np.concatenate(pool) if pool else np.zeros((0, 5))
    meta = dict(mode='mbgen', stream=stream, chunk=chunk, job_seed=job_seed, n_int=n_int, species=SPECIES,
                pool_phase_space=dict(pt=POOL_PT, abs_eta_max=POOL_ETA, production_within_mm=1.0, species=SPECIES[:6]),
                rate_per_interaction_in_road={k: v / n_int for k, v in rate.items()}, w_road=W_ROAD,
                n_final_per_interaction=n_final / n_int, n_pool_per_interaction=len(P) / n_int,
                cpu_ms_per_interaction=1e3 * cpu / n_int, base_lines=list(s4pu.PY_MB),
                code_sha256=C.code_hashes([__file__, C.HERE / 'p2c_common.py']))
    arrays = dict(hist=hist, hist_prompt=histp, pt_bins=PT_BINS, eta_bins=ETA_BINS,
                  pool_int=P[:, 0].astype(np.int32), pool_pdg=P[:, 1].astype(np.int32),
                  pool_pt=P[:, 2].astype(np.float32), pool_eta=P[:, 3].astype(np.float32),
                  pool_phi=P[:, 4].astype(np.float32))
    return arrays, meta


if __name__ == '__main__':
    out, n, stream, chunk = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    arrays, meta = generate(n, stream, chunk)
    meta['bytes'] = C.save_job(out, arrays, meta)
    log.info('%s', {k: meta[k] for k in ('n_int', 'cpu_ms_per_interaction', 'n_pool_per_interaction',
                                         'rate_per_interaction_in_road', 'bytes')})
    assert math.isfinite(meta['cpu_ms_per_interaction'])
