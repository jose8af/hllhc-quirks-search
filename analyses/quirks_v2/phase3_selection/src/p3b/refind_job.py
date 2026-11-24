"""Runner job — B2-a remediation attempt 1 (diagnostic control; p3-b, Casper): thin ρ = 2 development events at HIT level
and re-run the frozen ρ = 1 finder on the thinned pool.

  python refind_job.py --id ID --jobs c1pu2-0000,... [--draws 1]
For each ρ = 2 event with chain dumps (C1 pu2 jobs 0000-0039, 5 events each), the finder pool of both crossings is
replayed exactly (chain_inputs.prepare_event with the job's RNG stream; PV, phimet and the trial seeds are checked against
the stored trials, the job raises otherwise).  Per trial and draw, every interaction of the pool is kept with probability
1/2 (the thinning unit of thin_core: INT id; one Bernoulli per interaction), and production.process_trial runs at
ρ = 1 on the kept hits with the frozen configuration (road 0.15, T_seed 4), the stored trial seed and PV.  A ρ = 2
trial is two independent ρ = 1 chain events (each with its own top-up, CKF removal and merging), so the thinned pool
is a ρ = 1 pool in distribution; its counts are compared with the direct ρ = 1 counts (sample check) and with the
repaired-thinning prediction of the same trials (estimator check).  Output $QV2_OUT_DIR/ID.npz: grp (ntr, draws,
NCOL), npass, job, ev, road."""
import argparse
import hashlib
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import thin_core as TC  # noqa: E402  (sets sys.path for acts)
from acts.stage4 import run_stage4 as RS  # noqa: E402
from acts.stage4.finder import chain_inputs as CI  # noqa: E402
from acts.stage4.finder import production as PR  # noqa: E402
from acts.stage4.finder import pu_inputs as PI  # noqa: E402

SRC = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2/p2-a-c1-pu2/000')
log = logging.getLogger('refind_job')


def seed_of(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % (2 ** 31 - 1)


def dump_event(z, ie, k):
    p = f'dump.{ie}_{k}.'
    n = len(z[p + 'sid'])
    ev = np.zeros((n, 13))
    ev[:, 0] = z[p + 'sid']; ev[:, 1:4] = z[p + 'xyz']; ev[:, 4:6] = z[p + 's01']; ev[:, 6] = z[p + 'flag']
    ev[:, 7] = z[p + 'vp']; ev[:, 8] = z[p + 'particle']; ev[:, 9] = z[p + 'gen']; ev[:, 10] = z[p + 'vsec']
    ev[:, 11] = z[p + 'dE']; ev[:, 12] = z[p + 't']
    return ev, z[p + 'tru'].astype(np.float64), z[p + 'vz'].astype(np.float64)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--draws', type=int, default=1)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    fz = RS.frozen_inputs()
    cfg, wcfg = PR.config_from_frozen(fz)
    G, P, JB, EV, RD = [], [], [], [], []
    t0 = time.time()
    for jid in a.jobs.split(','):
        z = np.load(SRC / f'{jid}.npz')
        job = json.loads(str(z['meta_json']))['job']
        rho = job['rho']
        streams = np.random.SeedSequence(job['seed']).spawn(job['n_events'])
        for ie in range(job['n_events']):
            rs = np.random.default_rng(streams[ie])
            parts = [CI.prepare_event(*dump_event(z, ie, k), k, rs) for k in range(rho)]
            H = np.concatenate([p_['H'] for p_ in parts]); sid = np.concatenate([p_['sid'] for p_ in parts])
            INT = np.concatenate([p_['INT'] for p_ in parts])
            pv = PI.lum_pv(rs)
            phi0 = rs.uniform(-np.pi, np.pi)
            tr = np.where(z['trials.ev'] == job['ev0'] + ie)[0]
            uI, inv = np.unique(INT, return_inverse=True)
            for road in range(job['roads']):
                phimet = float((phi0 + road * 2 * np.pi / job['roads'] + np.pi) % (2 * np.pi) - np.pi)
                tseed = int(rs.integers(0, 2 ** 62))
                t = tr[z['trials.road'][tr] == road][0]
                if not (np.array_equal(z['trials.pv'][t], pv) and int(z['trials.trial_seed'][t]) == tseed and
                        abs(float(z['trials.phimet'][t]) - phimet) < 1e-12):
                    raise RuntimeError(f'{jid} ev {ie} road {road}: replay differs from the stored trial')
                g = np.zeros((a.draws, TC.NCOL), np.int64); pp = np.zeros_like(g)
                for d in range(a.draws):
                    rk = np.random.default_rng(seed_of(f'qv2|p3b.refind|{jid}|{t}|{d}'))
                    keepI = rk.random(len(uI)) < 0.5
                    m = keepI[inv]
                    res = PR.process_trial(H[m], sid[m], INT[m], pv, phimet, 1.0, tseed, cfg=cfg, wcfg=wcfg)
                    c = res['cand']
                    F = np.unpackbits(c['rungs'], axis=1)[:, :43].astype(bool)
                    C = TC.direct_cols(F[:, 3], c['dw_core'].astype(np.float64), c['p_chi2core'].astype(np.float64),
                                       c['n2s2'].astype(np.int64))
                    for j in range(TC.NCOL):
                        mm = C[:, j]
                        pp[d, j] = mm.sum()
                        g[d, j] = len(np.unique(c['group'][mm])) if mm.any() else 0
                    if np.any(g[d, :11] != res['row']['n_grp'][3:14]):
                        raise RuntimeError('column recount differs from process_trial n_grp')
                G.append(g); P.append(pp); JB.append(jid); EV.append(job['ev0'] + ie); RD.append(road)
        log.info('%s done, %.0f s', jid, time.time() - t0)
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in ('refind_job.py', 'thin_core.py', 'cols.py')}
    meta = dict(jobs=a.jobs.split(','), draws=a.draws, code_sha256=code, frozen=fz,
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    np.savez_compressed(out / f'{a.id}.npz', grp=np.array(G), npass=np.array(P), job=np.array(JB), ev=np.array(EV),
                        road=np.array(RD), cols=np.array(TC.COLS), meta_json=np.array(json.dumps(meta, default=str)))


if __name__ == '__main__':
    main()
