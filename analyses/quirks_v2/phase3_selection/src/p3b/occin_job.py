"""Runner job: occupancy-model inputs from the C1 ρ = 1 development events (B2-b, p3-b, Casper).

  python occin_job.py --id ID --jobs c1pu1-0000,... [--planes 1000]
For every event: replay of the finder input pool (occ_replay; PV checked bit-exact against the stored trial, the job
raises otherwise) -> per-surface z histograms of the pool (density input); for every trial (event, road): the random
plane ensemble of occ_core on the REAL hits -> planes passing each thin_core column (R04 required) and the histogram of
the 10-bit layer masks (>= 2 crossings) over all planes.  Only R04 and R05 enter the model as inputs; the deeper columns
are recorded for diagnostics.  Output $QV2_OUT_DIR/ID.npz."""
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
import occ_core as OC  # noqa: E402
import occ_replay as RP  # noqa: E402
import thin_core as TC  # noqa: E402

SRC = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2/p2-a-c1-pu1/000')
log = logging.getLogger('occin_job')


def seed_of(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % (2 ** 31 - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--planes', type=int, default=1000)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    zh = np.zeros((16, OC.NZB), np.int64)
    rr_min = np.full(16, np.inf); rr_max = np.zeros(16); s0 = np.zeros(16); s1 = np.zeros(16)
    CNT, MH, NT, JB, EV, RD = [], [], [], [], [], []
    nev = 0
    t0 = time.time()
    for jid in a.jobs.split(','):
        z, job = RP.open_job(SRC / f'{jid}.npz')
        tev = z['trials.ev']; tpv = z['trials.pv']; tph = z['trials.phimet']; trd = z['trials.road']
        for ie in range(job['n_events']):
            r = RP.replay(z, job, ie)
            H, sid, pv = r['H'], r['sid'], r['pv']
            tr = np.where(tev == job['ev0'] + ie)[0]
            if not (np.array_equal(tpv[tr], np.repeat(pv[None, :], len(tr), 0)) and
                    np.allclose(tph[tr], r['phimets'][trd[tr]], rtol=0, atol=1e-12)):
                raise RuntimeError(f'{jid} event {ie}: replayed PV/phimet differ from the stored trials')
            zh += OC.z_hist(H, sid)
            nev += 1
            ix = OC.build_index(H, sid)
            rr_min = np.minimum(rr_min, ix['rr'][:, 0]); rr_max = np.maximum(rr_max, ix['rr'][:, 1])
            s0 = ix['s0']; s1 = ix['s1']
            A = OC.trial_arrays(H, sid, pv)
            for t in tr:
                cnt, mh, ntot = OC.real_planes(H, A['LC'], A['SD'], A['U'], A['CX'], A['CY'], A['S0'], A['S1'],
                                               ix['hid'], ix['Z'], ix['bstart'], ix['boff'], ix['nb'], ix['rr'],
                                               ix['s0'], ix['s1'], pv, float(tph[t]), a.planes,
                                               seed_of(f'qv2|p3b.occin|{jid}|{t}'), TC.CHI2_ISF, TC.NCOL)
                CNT.append(cnt); MH.append(mh); NT.append(ntot); JB.append(jid); EV.append(int(tev[t]))
                RD.append(int(trd[t]))
        log.info('%s done, %d events, %.0f s; R04/R05 planes so far %s', jid, nev, time.time() - t0,
                 np.sum(CNT, 0)[:2])
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()
            for f in ('occ_core.py', 'occ_replay.py', 'thin_core.py', 'occin_job.py')}
    meta = dict(jobs=a.jobs.split(','), planes=a.planes, nz_min=OC.NZ_MIN, n_events=nev, code_sha256=code,
                zbins=[OC.ZLO, OC.ZHI, OC.DZ], created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    np.savez_compressed(out / f'{a.id}.npz', cnt=np.array(CNT, np.int64), mask_hist=np.array(MH, np.int64),
                        ntot=np.array(NT, np.int64), job=np.array(JB), ev=np.array(EV), road=np.array(RD),
                        zhist=zh, rr=np.c_[rr_min, rr_max], s0=s0, s1=s1, n_events=np.array(nev),
                        cols=np.array(TC.COLS), meta_json=np.array(json.dumps(meta)))


if __name__ == '__main__':
    main()
