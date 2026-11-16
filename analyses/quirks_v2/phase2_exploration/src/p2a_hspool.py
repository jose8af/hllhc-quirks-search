"""p2a_hspool.py -- hard-scatter parent pools from FINISHED Z(nunu) pilot files (addendum 1 v3, P2 "Hard-scatter parents";
Phase 2 channel (iii), executor Albert, 2026-11-16).

  <acts python> p2a_hspool.py <out.npz> <stream> <chunk> <keep_offroad: 0|1> <znn file.npz> [...]

Reads (read-only) files of p2x_hs0.py (mode hs0x): per event the list `had` (final hadrons and photons of the hard
scatter, |eta| < 1.5, pT > 0.3 GeV: pdg, pT, eta, phi, production radius and z) and `evt` (v1 preselection weight
w_v1, road axis phimet_reco_v1, event seed).  Nothing is generated here and no random number is drawn: the output is
a function of the input files and their order; <stream> and <chunk> are labels (and the job-seed tag in meta).

Pool phase space = the one of the minimum-bias pool (p2c_mbgen l.88, p2x_hspool.py): pi+-, K+-, p, K0L, n, gamma
produced within 1 mm of the interaction point (r_prod < 1 mm, |z_prod| < 1 mm in the generator frame), 0.5 < pT < 20
GeV, |eta| < 1.
  pool_*    parents INSIDE the road of their own event, |dphi(parent, phimet_reco_v1)| < 0.15 (the frozen definition of
            N_t): pool_int (row of `evt` in this file), pool_pdg, pool_pt, pool_eta, pool_phi, pool_dphi (the true road
            offset, kept through Geant4 and the chain), pool_w (w_v1 of the event; p2x_g4prod draw=weighted draws
            parents in proportion to it, so events failing v1's preselection (w = 0) are never fired)
  opool_*   the same phase space OUTSIDE the road (optional population "off-road hard-scatter hadrons"); written if
            keep_offroad = 1
  evt       per source event: source file index, event index in that file, chunk of the source job, w_v1,
            phimet_reco_v1, number of pool-phase-space parents at any azimuth and inside the road, event seed (lo, hi)
The format is the one p2x_common.load_pool reads (prefix 'pool' or 'opool').  Side file <out>.sha.json: content hash.
"""
import sys
import time

import numpy as np

import p2c_common as C
import p2x_common as X

log = C.setup_logging('p2a_hspool')
SPECIES = (211, 321, 2212, 130, 2112, 22)
POOL_PT = (0.5, 20.0)
POOL_ETA = 1.0
PROD_MM = 1.0
W_ROAD = 0.15
EVT_COLS = ['src_file', 'src_event', 'src_chunk', 'w_v1', 'phimet_reco_v1', 'n_pool_any_phi', 'n_pool_in_road',
            'ev_seed_lo', 'ev_seed_hi']


def run(out, stream, chunk, keep_offroad, files):
    t0 = time.time()
    evts = []; rows_in = []; rows_out = []; srcs = []; n0 = 0
    for k, f in enumerate(files):
        z, m = C.load_job(f)
        assert m.get('mode') == 'hs0x', f'{f} is not a p2x_hs0 file'
        ec = {c: i for i, c in enumerate(m['evt_cols'])}; hc = {c: i for i, c in enumerate(m['had_cols'])}
        ev = z['evt']; had = z['had'].astype(np.float64); off = z['had_off']
        n = len(ev)
        assert len(off) == n + 1 and off[-1] == len(had)
        iev = np.repeat(np.arange(n), np.diff(off))
        pt = had[:, hc['pt']]; eta = had[:, hc['eta']]; phi = had[:, hc['phi']]
        near = (had[:, hc['r_prod']] < PROD_MM) & (np.abs(had[:, hc['z_prod']]) < PROD_MM)
        inps = (np.isin(np.abs(had[:, hc['pdg']]).astype(np.int64), SPECIES) & near & (pt > POOL_PT[0]) & (pt < POOL_PT[1])
                & (np.abs(eta) < POOL_ETA))
        w = ev[:, ec['w_v1']]; phm = ev[:, ec['phimet_reco_v1']]
        d = (phi - phm[iev] + np.pi) % (2 * np.pi) - np.pi
        inroad = inps & (np.abs(d) < W_ROAD)
        offroad = inps & ~(np.abs(d) < W_ROAD)
        for msk, dst in ((inroad, rows_in), (offroad, rows_out)):
            dst.append(np.c_[n0 + iev[msk], had[msk, hc['pdg']], pt[msk], eta[msk], phi[msk], d[msk], w[iev[msk]]])
        e = np.zeros((n, len(EVT_COLS)))
        e[:, 0] = k; e[:, 1] = np.arange(n); e[:, 2] = m['chunk']; e[:, 3] = w; e[:, 4] = phm
        e[:, 5] = np.bincount(iev[inps], minlength=n); e[:, 6] = np.bincount(iev[inroad], minlength=n)
        e[:, 7] = ev[:, ec['ev_seed_lo']]; e[:, 8] = ev[:, ec['ev_seed_hi']]
        evts.append(e); n0 += n
        srcs.append(dict(file=str(f), stream=m['stream'], chunk=m['chunk'], job_seed=m['job_seed'], n_events=m['n_events'],
                         content_sha256=m['content_sha256'], had_per_event=float(len(had) / n),
                         frac_had_produced_within_1mm=float(near.mean())))
    evt = np.concatenate(evts)
    w = evt[:, 3]
    arrays = dict(evt=evt)
    for pre, rows in (('pool', rows_in), ('opool', rows_out)):
        if pre == 'opool' and not keep_offroad:
            continue
        P = np.concatenate(rows) if rows else np.zeros((0, 7))
        arrays.update({f'{pre}_int': P[:, 0].astype(np.int32), f'{pre}_pdg': P[:, 1].astype(np.int32),
                       f'{pre}_pt': P[:, 2].astype(np.float32), f'{pre}_eta': P[:, 3].astype(np.float32),
                       f'{pre}_phi': P[:, 4].astype(np.float32), f'{pre}_dphi': P[:, 5].astype(np.float32),
                       f'{pre}_w': P[:, 6].astype(np.float32)})
    n_in = sum(len(r) for r in rows_in); n_out = sum(len(r) for r in rows_out)
    w_in = float(sum(r[:, 6].sum() for r in rows_in)); w_out = float(sum(r[:, 6].sum() for r in rows_out))
    n_in_wpos = int(sum((r[:, 6] > 0).sum() for r in rows_in))
    meta = dict(mode='hspool-x', stream=stream, chunk=chunk, job_seed=C.qv2_seed(stream, chunk), n_events=int(len(evt)),
                evt_cols=EVT_COLS, source_files=srcs,
                pool_phase_space=dict(pt=POOL_PT, abs_eta_max=POOL_ETA, production_within_mm=PROD_MM, species=list(SPECIES),
                                      road_half_width=W_ROAD, road_axis='phimet_reco_v1 of the event (gen_d123.presel)'),
                n_pool=int(n_in), n_opool=int(n_out), opool_kept=bool(keep_offroad),
                n_pool_with_positive_weight=n_in_wpos,
                pool_in_road_per_event=float(n_in / len(evt)), pool_off_road_per_event=float(n_out / len(evt)),
                pool_any_phi_per_event=float(evt[:, 5].mean()),
                pool_in_road_per_event_weighted=float(w_in / max(w.sum(), 1e-300)),
                pool_off_road_per_event_weighted=float(w_out / max(w.sum(), 1e-300)),
                sum_w=float(w.sum()), sum_w2=float((w ** 2).sum()), n_w_positive=int((w > 0).sum()),
                n_w_full=int((w > 0.5).sum()), n_w_low=int(((w > 0) & (w <= 0.5)).sum()),
                t_total_s=round(time.time() - t0, 2),
                code_sha256=X.src_hashes('p2a_hspool.py', 'p2x_common.py', 'p2c_common.py'), input_sha256=X.input_hashes())
    X.save(out, arrays, meta)
    X.write_sha(str(out) + '.sha.json', dict(job=dict(stream=stream, chunk=chunk, n_events=int(len(evt)), n_files=len(files)),
                                             files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
    log.info('%s', {k: meta[k] for k in ('n_events', 'n_pool', 'n_opool', 'n_pool_with_positive_weight', 'pool_in_road_per_event',
                                         'pool_in_road_per_event_weighted', 'pool_off_road_per_event', 'pool_any_phi_per_event',
                                         'sum_w', 'n_w_full', 'n_w_low', 't_total_s', 'bytes', 'content_sha256')})
    log.info('sources: %s', [(s['chunk'], s['frac_had_produced_within_1mm']) for s in srcs])


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), bool(int(a[3])), a[4:])
