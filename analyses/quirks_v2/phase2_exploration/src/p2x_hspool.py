"""p2x_hspool.py -- hard-scatter parent pool for the sample `pilot.c0.hs` (addendum 1 v2, P2; finding B7).

  <acts python> p2x_hspool.py <out.npz> <sample e.g. Znunu_j> <n_events> <stream> <chunk>

Generator level only (no detector simulation): s4pu.HardScatter unchanged (CP5, 14 TeV, pT-hat > 150 GeV, truth
MET(nu) > 200 GeV filter), one accepted event per seed, with v1's generator-level preselection weight
(gen_d123.presel, unchanged) and its road axis phi_MET,reco.  Pool = final-state pi+-, K+-, p, K0L, n, gamma produced
within 1 mm of the interaction point with 0.5 < pT < 20 GeV, |eta| < 1 (the pool phase space of p2c_mbgen) AND inside
the road of their event: |dphi(parent, phi_MET,reco)| < 0.15 (gen_d123.road_objects l.149).
Output arrays:
  pool_int (event index in this file), pool_pdg, pool_pt, pool_eta, pool_phi,
  pool_dphi   phi(parent) - phi_MET,reco of its event (the road offset, kept through Geant4 and the chain)
  pool_w      v1 preselection weight of the event (0 for events failing it: kept, flagged by the weight)
  evt (n_ev, len(EVT_COLS))
Side file <out>.sha.json: content hash.
"""
import math
import sys
import time

import numpy as np

import signal  # noqa: F401  (stdlib, before acts/stage4/analysis/signal.py can shadow it)
import subprocess  # noqa: F401

import p2c_common as C
import p2x_common as X

sys.path.insert(0, str(C.CODE))
sys.path.insert(0, str(C.ANA))
import s4pu  # noqa: E402
import gen_d123  # noqa: E402

log = C.setup_logging('p2x_hspool')
CP5 = C.QV2 / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
EVT_COLS = ['met_x', 'met_y', 'hs_tries', 'sigma_gen_mb', 'w_v1', 'met_reco_v1', 'phimet_reco_v1', 'n_pool_any_phi',
            'n_pool_in_road', 'ev_seed_lo', 'ev_seed_hi']
SPECIES = (211, 321, 2212, 130, 2112, 22)
POOL_PT = (0.5, 20.0)
POOL_ETA = 1.0
W_ROAD = gen_d123.W_ROAD


def run(out, sample, n_events, stream, chunk):
    t0 = time.time()
    job_seed = C.qv2_seed(stream, chunk)
    hs = s4pu.HardScatter(CP5, sample, tt=C.QV2)
    sj30 = gen_d123.slowjet()
    evt = np.zeros((n_events, len(EVT_COLS)))
    rows = []
    c0 = time.process_time()
    for i in range(n_events):
        ev_seed = s4pu.hseed('p2x-hspool', sample, job_seed, i, mod=2 ** 62)
        parts, met, ntry, sgen = hs.generate(s4pu.hseed('hs', ev_seed))
        ev = hs.gen.py.event
        rng = np.random.default_rng(s4pu.hseed('p2c-presel', sample, ev_seed, mod=2 ** 62))
        w, det, phm = gen_d123.presel(ev, met, rng, sj30)
        n_any = 0; n_road = 0
        for k in range(ev.size()):
            p = ev[k]
            if not p.isFinal() or p.idAbs() not in SPECIES:
                continue
            pt = p.pT()
            if not (POOL_PT[0] < pt < POOL_PT[1]) or abs(p.eta()) >= POOL_ETA:
                continue
            if math.hypot(p.xProd(), p.yProd()) >= 1.0 or abs(p.zProd()) >= 1.0:
                continue
            n_any += 1
            d = gen_d123.dphi(p.phi(), phm)
            if abs(d) < W_ROAD:
                n_road += 1
                rows.append((i, p.id(), pt, p.eta(), p.phi(), d, w))
        evt[i] = (met[0], met[1], ntry, sgen, w, det['met_reco'], phm, n_any, n_road, ev_seed % 2 ** 31, ev_seed // 2 ** 31)
    cpu = time.process_time() - c0
    P = np.array(rows, float).reshape(-1, 7)
    w = evt[:, 4]
    arrays = dict(evt=evt, pool_int=P[:, 0].astype(np.int32), pool_pdg=P[:, 1].astype(np.int32),
                  pool_pt=P[:, 2].astype(np.float32), pool_eta=P[:, 3].astype(np.float32),
                  pool_phi=P[:, 4].astype(np.float32), pool_dphi=P[:, 5].astype(np.float32), pool_w=P[:, 6].astype(np.float32))
    meta = dict(mode='hspool', sample=sample, stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events,
                evt_cols=EVT_COLS, pool_phase_space=dict(pt=POOL_PT, abs_eta_max=POOL_ETA, production_within_mm=1.0,
                                                         species=list(SPECIES), road_half_width=W_ROAD,
                                                         road_axis='phi of v1 MET_reco (gen_d123.presel)'),
                n_pool=int(len(P)), pool_in_road_per_event=float(len(P) / n_events),
                pool_in_road_per_event_weighted=float((evt[:, 8] * w).sum() / max(w.sum(), 1e-300)),
                pool_any_phi_per_event=float(evt[:, 7].mean()), sum_w=float(w.sum()), sum_w2=float((w ** 2).sum()),
                n_w_positive=int((w > 0).sum()), sum_tries=int(evt[:, 2].sum()), cpu_ms_per_event=1e3 * cpu / n_events,
                generator=dict(lines=s4pu.SM_SAMPLES[sample][0], pthat_min=s4pu.SM_SAMPLES[sample][1],
                               met_min=s4pu.MET_MIN, pre_met=s4pu.PRE_MET),
                t_total_s=round(time.time() - t0, 2),
                code_sha256=dict(C.code_hashes([C.ANA / 'gen_d123.py']), **X.src_hashes('p2x_hspool.py', 'p2x_common.py', 'p2c_common.py')),
                input_sha256=X.input_hashes())
    X.save(out, arrays, meta)
    X.write_sha(str(out) + '.sha.json', dict(job=dict(stream=stream, chunk=chunk, job_seed=job_seed),
                                             files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
    log.info('%s', {k: meta[k] for k in ('sample', 'n_events', 'n_pool', 'pool_in_road_per_event',
                                         'pool_in_road_per_event_weighted', 'pool_any_phi_per_event', 'cpu_ms_per_event',
                                         'bytes', 'content_sha256')})


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]))
