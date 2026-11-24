"""Replay of the finder input pool of C1 ρ = 1 development events from their stored chain dumps (p3-b, Casper).

`run_stage4.run_pu_job` builds each event with `chain_inputs.prepare_event(ev, tru, vz, k, rs)` where
rs = default_rng(SeedSequence(job_seed).spawn(n_events)[ie]); the top-up, CKF removal and merging consume rs in that
order; then pv = pu_inputs.lum_pv(rs), phi0 = rs.uniform(-pi, pi), and per road phimet = phi0 + road 2 pi / roads
(wrapped).  Replaying this from the dumps gives the exact finder input (verified against the stored PV of every trial).
"""
import json
import sys
from pathlib import Path

import numpy as np

QV2 = Path(__file__).resolve().parents[3]
if str(QV2) not in sys.path:
    sys.path.insert(0, str(QV2))
from acts.stage4.finder import chain_inputs as CI   # noqa: E402
from acts.stage4.finder import pu_inputs as PI      # noqa: E402
from acts.stage4.finder import finder as FF         # noqa: E402


def open_job(path):
    z = np.load(path)
    meta = json.loads(str(z['meta_json']))
    job = meta['job']
    return z, job


def replay(z, job, ie):
    """-> dict(H, sid, INT, pv, phimets (roads,))  for event ie of the job (ρ = 1)."""
    ss = np.random.SeedSequence(job['seed'])
    rs = np.random.default_rng(ss.spawn(job['n_events'])[ie])
    p = f'dump.{ie}_0.'
    n = len(z[p + 'sid'])
    ev = np.zeros((n, 13))
    ev[:, 0] = z[p + 'sid']; ev[:, 1:4] = z[p + 'xyz']; ev[:, 4:6] = z[p + 's01']; ev[:, 6] = z[p + 'flag']
    ev[:, 7] = z[p + 'vp']; ev[:, 8] = z[p + 'particle']; ev[:, 9] = z[p + 'gen']; ev[:, 10] = z[p + 'vsec']
    ev[:, 11] = z[p + 'dE']; ev[:, 12] = z[p + 't']
    part = CI.prepare_event(ev, z[p + 'tru'].astype(np.float64), z[p + 'vz'].astype(np.float64), 0, rs)
    pv = PI.lum_pv(rs)
    phi0 = rs.uniform(-np.pi, np.pi)
    roads = job['roads']
    phimets = np.array([float((phi0 + r * 2 * np.pi / roads + np.pi) % (2 * np.pi) - np.pi) for r in range(roads)])
    return dict(H=part['H'], sid=part['sid'], INT=part['INT'], pv=pv, phimets=phimets, stats=part['stats'])


if __name__ == '__main__':
    import logging
    import time
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    z, job = open_job(sys.argv[1])
    for ie in range(2):
        t0 = time.time()
        r = replay(z, job, ie)
        tr = np.where(z['trials.ev'] == job['ev0'] + ie)[0]
        okpv = np.allclose(z['trials.pv'][tr], r['pv'][None, :], atol=0, rtol=0)
        okph = np.allclose(np.sort(z['trials.phimet'][tr]), np.sort(r['phimets']), atol=1e-12)
        ev = z['chain.evstats'][z['chain.evstats'][:, 0] == ie][0] if 'chain.evstats' in z.files else None
        logging.info('event %d: %.1f s, pool %d, PV identical %s, phimet identical %s, stats %s, stored evstats %s',
                     ie, time.time() - t0, len(r['H']), okpv, okph, r['stats'], ev)
