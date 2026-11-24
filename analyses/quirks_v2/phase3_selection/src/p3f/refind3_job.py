"""Runner job (p3-f Task B, investigator Jorunn): thinning re-find yield on the 400 control trials of P3B R1.

  python refind3_job.py --id ID --jobs c1pu2-0000,... [--draws 3]
Same replay and checks as p3b/refind_job.py (imported, not edited); K new thinning draws per trial (every interaction
kept with probability 1/2; seeds qv2|p3f.refind|<job>|<trial>|<d>, independent of P3B's), the frozen rho = 1
production.process_trial on each kept pool.  Stored per draw: groups and passing candidates per column, CPU seconds of
the re-find, and the re-found R04 candidates with w_core < 37.5 or p > 1e-3 (process_trial 'full' policy): group id,
variables, hit lists as row indices of the replayed rho = 2 pool.  No direct count is read or compared.
Output $QV2_OUT_DIR/ID.npz."""
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
sys.path.insert(0, str(HERE.parent / 'p3b'))
import refind_job as RJ  # noqa: E402  (dump_event, SRC; sets sys.path for acts via thin_core)
import thin_core as TC  # noqa: E402
from acts.stage4 import run_stage4 as RS  # noqa: E402
from acts.stage4.finder import chain_inputs as CI  # noqa: E402
from acts.stage4.finder import production as PR  # noqa: E402
from acts.stage4.finder import pu_inputs as PI  # noqa: E402

log = logging.getLogger('refind3_job')


def seed_of(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % (2 ** 31 - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--draws', type=int, default=3)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    fz = RS.frozen_inputs()
    cfg, wcfg = PR.config_from_frozen(fz)
    G, P, CPU, JB, EV, RD = [], [], [], [], [], []
    C = {k: [] for k in ('trial', 'draw', 'group', 'dw_core', 'p_chi2core', 'n2s2', 'nip2', 'off', 'hits')}
    hoff = 0
    itr = 0
    t0 = time.time()
    for jid in a.jobs.split(','):
        z = np.load(RJ.SRC / f'{jid}.npz')
        job = json.loads(str(z['meta_json']))['job']
        rho = job['rho']
        streams = np.random.SeedSequence(job['seed']).spawn(job['n_events'])
        for ie in range(job['n_events']):
            rs = np.random.default_rng(streams[ie])
            parts = [CI.prepare_event(*RJ.dump_event(z, ie, k), k, rs) for k in range(rho)]
            H = np.concatenate([p_['H'] for p_ in parts]); sid = np.concatenate([p_['sid'] for p_ in parts])
            INT = np.concatenate([p_['INT'] for p_ in parts])
            pv = PI.lum_pv(rs)
            phi0 = rs.uniform(-np.pi, np.pi)
            tr = np.where(z['trials.ev'] == job['ev0'] + ie)[0]
            uI, inv = np.unique(INT, return_inverse=True)
            key = {r.tobytes(): i for i, r in enumerate(H[:, 1:4].astype(np.float32))}
            for road in range(job['roads']):
                phimet = float((phi0 + road * 2 * np.pi / job['roads'] + np.pi) % (2 * np.pi) - np.pi)
                tseed = int(rs.integers(0, 2 ** 62))
                t = tr[z['trials.road'][tr] == road][0]
                if not (np.array_equal(z['trials.pv'][t], pv) and int(z['trials.trial_seed'][t]) == tseed and
                        abs(float(z['trials.phimet'][t]) - phimet) < 1e-12):
                    raise RuntimeError(f'{jid} ev {ie} road {road}: replay differs from the stored trial')
                g = np.zeros((a.draws, TC.NCOL), np.int64); pp = np.zeros_like(g); cpu = np.zeros(a.draws)
                for d in range(a.draws):
                    rk = np.random.default_rng(seed_of(f'qv2|p3f.refind|{jid}|{t}|{d}'))
                    keepI = rk.random(len(uI)) < 0.5
                    m = keepI[inv]
                    c0 = time.process_time()
                    res = PR.process_trial(H[m], sid[m], INT[m], pv, phimet, 1.0, tseed, cfg=cfg, wcfg=wcfg)
                    cpu[d] = time.process_time() - c0
                    c = res['cand']
                    F = np.unpackbits(c['rungs'], axis=1)[:, :43].astype(bool)
                    Cc = TC.direct_cols(F[:, 3], c['dw_core'].astype(np.float64), c['p_chi2core'].astype(np.float64),
                                        c['n2s2'].astype(np.int64))
                    for j in range(TC.NCOL):
                        mm = Cc[:, j]
                        pp[d, j] = mm.sum()
                        g[d, j] = len(np.unique(c['group'][mm])) if mm.any() else 0
                    if np.any(g[d, :11] != res['row']['n_grp'][3:14]):
                        raise RuntimeError('column recount differs from process_trial n_grp')
                    hr = res['hit']
                    if hr is not None:
                        pos = {int(ci): k for k, ci in enumerate(c['idx'])}
                        pool = np.array([key[r.tobytes()] for r in hr['xyz'].astype(np.float32)], np.int64)
                        for q, ci in enumerate(hr['cand']):
                            k = pos[int(ci)]
                            hl = pool[hr['ref'][hr['off'][q]:hr['off'][q + 1]]]
                            C['trial'].append(itr); C['draw'].append(d); C['group'].append(int(c['group'][k]))
                            C['dw_core'].append(float(c['dw_core'][k])); C['p_chi2core'].append(float(c['p_chi2core'][k]))
                            C['n2s2'].append(int(c['n2s2'][k])); C['nip2'].append(int(c['nip2'][k]))
                            C['off'].append(hoff); C['hits'].append(hl); hoff += len(hl)
                G.append(g); P.append(pp); CPU.append(cpu); JB.append(jid); EV.append(job['ev0'] + ie); RD.append(road)
                itr += 1
        log.info('%s done, %d trials, %.0f s', jid, itr, time.time() - t0)
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in ('refind3_job.py',)}
    code.update({f: hashlib.sha256((HERE.parent / 'p3b' / f).read_bytes()).hexdigest()
                 for f in ('refind_job.py', 'thin_core.py', 'cols.py')})
    meta = dict(jobs=a.jobs.split(','), draws=a.draws, code_sha256=code, frozen=fz,
                created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    C['off'].append(hoff)
    np.savez_compressed(out / f'{a.id}.npz', grp=np.array(G), npass=np.array(P), cpu=np.array(CPU), job=np.array(JB),
                        ev=np.array(EV), road=np.array(RD), cols=np.array(TC.COLS),
                        c_trial=np.array(C['trial'], np.int32), c_draw=np.array(C['draw'], np.int8),
                        c_group=np.array(C['group'], np.int32), c_dw_core=np.array(C['dw_core'], np.float32),
                        c_p_chi2core=np.array(C['p_chi2core'], np.float32), c_n2s2=np.array(C['n2s2'], np.int16),
                        c_nip2=np.array(C['nip2'], np.int16), c_off=np.array(C['off'], np.int64),
                        c_hits=(np.concatenate(C['hits']) if C['hits'] else np.zeros(0, np.int64)).astype(np.int32),
                        meta_json=np.array(json.dumps(meta, default=str)))


if __name__ == '__main__':
    main()
