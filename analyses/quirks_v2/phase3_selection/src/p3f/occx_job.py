"""Runner job (p3-f, investigator Jorunn): measurements (i) and (ii) of `outputs/p3f/CAUSE_METHOD_jorunn.md` on the C1
ρ = 1 development sample (c1.pu1).

  python occx_job.py --id ID --jobs c1pu1-0000,... [--planes 10000] [--mode campaign|validate] [--trials K]
                     [--nip-elig 6] [--events E]
campaign : per trial, the frozen ensemble (10,000 configurations, fresh seeds), fixed and refit maps (counts per
           column), basin volumes V_r for the subsampled R04 passers (R06: all, nloc 256; R05 not R06: 1/2; R04 only:
           1/8; nloc 64).  Output $QV2_OUT_DIR/ID.npz.
validate : V1 recapture / V2 saturation / C2 eligibility on the first K trials of the given jobs (no subsampling, sets
           stored).  Output $QV2_OUT_DIR/ID.npz.
No direct count is read: only the chain dumps and the stored trial PV/phimet (replay check) are used."""
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
import occx_core as XC  # noqa: E402
OC = XC.OC
TC = XC.TC
sys.path.insert(0, str(HERE.parent / 'p3b'))
import occ_replay as RP  # noqa: E402

SRC = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2/p2-a-c1-pu1/000')
log = logging.getLogger('occx_job')
P_R04_ONLY = 1.0 / 8.0
P_R05_ONLY = 1.0 / 2.0
NLOC = 256
NLOC_R06 = 1024
MAXDBL = 6


def seed_of(s):
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % (2 ** 31 - 1)


def trial_inputs(z, job, ie):
    r = RP.replay(z, job, ie)
    H, sid, pv = r['H'], r['sid'], r['pv']
    tev = z['trials.ev']; tpv = z['trials.pv']; tph = z['trials.phimet']; trd = z['trials.road']
    tr = np.where(tev == job['ev0'] + ie)[0]
    if not (np.array_equal(tpv[tr], np.repeat(pv[None, :], len(tr), 0)) and
            np.allclose(tph[tr], r['phimets'][trd[tr]], rtol=0, atol=1e-12)):
        raise RuntimeError('replayed PV/phimet differ from the stored trials')
    ix = OC.build_index(H, sid)
    A = OC.trial_arrays(H, sid, pv)
    return H, sid, pv, tr, ix, A, tph, trd, tev


def args_of(H, pv, ph, ix, A, prej):
    return (pv, ph, H, A['LC'], A['SD'], A['U'], A['CX'], A['CY'], A['S0'], A['S1'], ix['hid'], ix['Z'], ix['bstart'],
            ix['boff'], ix['nb'], ix['rr'], ix['s0'], ix['s1'], prej)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--jobs', required=True)
    ap.add_argument('--planes', type=int, default=10000)
    ap.add_argument('--mode', default='campaign')
    ap.add_argument('--trials', type=int, default=4)
    ap.add_argument('--events', type=int, default=0, help='limit events per file (tests)')
    ap.add_argument('--nip-elig', type=int, default=6)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    prej = XC.pre_of_surface()
    volD = XC.vol_D()
    cap = max(1000, a.planes // 20)
    t0 = time.time()
    R = dict(cnt=[], nelig=[], nip5=[], job=[], ev=[], road=[], tsec=[])
    S = dict(trial=[], map=[], flags=[], s=[], V=[], ndbl=[], edge=[], nmem=[], h=[], aux=[], nloc=[])
    VAL = []
    itrial = 0
    done = False
    for jid in a.jobs.split(','):
        z, job = RP.open_job(SRC / f'{jid}.npz')
        nev = job['n_events'] if a.events <= 0 else min(a.events, job['n_events'])
        for ie in range(nev):
            H, sid, pv, tr, ix, A, tph, trd, tev = trial_inputs(z, job, ie)
            for t in tr:
                ts = time.time()
                ph = float(tph[t])
                base = args_of(H, pv, ph, ix, A, prej)
                sd = seed_of(f'qv2|p3f.occx|{jid}|{t}|{a.mode}')
                cnt, nelig, rec, recf, aux, nip5 = XC.scan_trial(a.planes, sd, *base, TC.CHI2_ISF, a.nip_elig,
                                                                 TC.NCOL, cap)
                rng = np.random.default_rng(sd + 1)
                f = recf
                if a.mode == 'campaign':
                    u = rng.random(len(rec))
                    sw = np.where(f[:, 2], 1.0, np.where(f[:, 1], 1 / P_R05_ONLY, 1 / P_R04_ONLY))
                    take = np.where(f[:, 2] | (f[:, 1] & ~f[:, 2] & (u < P_R05_ONLY)) |
                                    (~f[:, 1] & (u < P_R04_ONLY)))[0]
                else:
                    sw = np.ones(len(rec))
                    take = np.arange(len(rec))
                nloc = np.where(f[take, 2], NLOC_R06, NLOC).astype(np.int64)
                seeds = np.array([seed_of(f'qv2|p3f.occx.V|{jid}|{t}|{k}|{a.mode}') for k in take], np.int64)
                V, ND, ED, NM, HB, off, hits = XC.volumes(rec, recf, take.astype(np.int64), nloc, seeds, MAXDBL,
                                                          *base, TC.CHI2_ISF, a.nip_elig, volD, TC.NCOL,
                                                          a.mode != 'campaign')
                R['cnt'].append(cnt); R['nelig'].append(nelig); R['nip5'].append(nip5); R['job'].append(jid)
                R['ev'].append(int(tev[t])); R['road'].append(int(trd[t])); R['tsec'].append(time.time() - ts)
                S['trial'].append(np.full(len(take), itrial)); S['map'].append(rec[take, 0].astype(np.int8))
                S['flags'].append(recf[take][:, XC.RL]); S['s'].append(sw[take]); S['V'].append(V)
                S['ndbl'].append(ND); S['edge'].append(ED); S['nmem'].append(NM); S['h'].append(HB)
                S['aux'].append(aux[take]); S['nloc'].append(nloc)
                if a.mode != 'campaign':
                    VAL.append(dict(trial=itrial, rec=rec, recf=recf, aux=aux, off=off, hits=hits, V=V, nroad=len(H)))
                log.info('%s ev %d trial %d: %.1f s; R04 fixed/refit %d/%d, eligible %d, V for %d (dbl %d, edge %d)',
                         jid, ie, t, time.time() - ts, cnt[0, 0], cnt[1, 0], nelig, len(take), ND.sum(), ED.sum())
                itrial += 1
                if a.mode != 'campaign' and itrial >= a.trials:
                    done = True
                    break
            if done:
                break
        if done:
            break
    log.info('done: %d trials, %.0f s', itrial, time.time() - t0)
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest() for f in ('occx_core.py', 'occx_job.py')}
    code.update({f: hashlib.sha256((HERE.parent / 'p3b' / f).read_bytes()).hexdigest()
                 for f in ('occ_core.py', 'occ_replay.py', 'thin_core.py')})
    meta = dict(jobs=a.jobs.split(','), planes=a.planes, mode=a.mode, nip_elig=a.nip_elig, volD=volD,
                p_r04_only=P_R04_ONLY, p_r05_only=P_R05_ONLY, nloc=NLOC, nloc_r06=NLOC_R06, maxdbl=MAXDBL,
                rl=XC.RL.tolist(), code_sha256=code, created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    cat = {k: (np.concatenate(v) if len(v) else np.zeros(0)) for k, v in S.items()}
    extra = {}
    if VAL:
        for k, d in enumerate(VAL):
            for kk, vv in d.items():
                extra[f'val{k}_{kk}'] = np.asarray(vv)
    np.savez_compressed(out / f'{a.id}.npz', cnt=np.array(R['cnt'], np.int64), nelig=np.array(R['nelig']),
                        nip5=np.array(R['nip5']), job=np.array(R['job']), ev=np.array(R['ev']),
                        road=np.array(R['road']), tsec=np.array(R['tsec']),
                        **{'v_' + k: v for k, v in cat.items()}, **extra, meta_json=np.array(json.dumps(meta)))


if __name__ == '__main__':
    main()
