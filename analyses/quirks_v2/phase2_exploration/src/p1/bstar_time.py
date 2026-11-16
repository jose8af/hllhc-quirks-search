"""bstar_time.py -- P1 re-timing (channel (ii), Sebastian, 2026-11-16): the per-event cost of v1's paired B*-off test on
a worker, run exactly as v1's TT/sim/stage3/scripts/fix_bstar_off.py job() (l.33-60): for each event four runs of the
Stage-1 general-field kernel analytic/numerics/nm_kernel.run (arms on/off x fields B0, B0/2), max_boost 1e-3,
hmax_trk 0.2 cm, qcap 2^19, vacuum, vertex at the origin; Delta_s = plane fit of the barrel hits (layer id < 10).
Inputs: the Phase-1 toy Stage-3 inputs (FEAS_A §2.5; data/feasibility/chain/stage3_inputs/F_m{500,1000}_toy.npz).
This is a TIMING job: the c values are written but are not physics (toy kinematics).
Usage: python bstar_time.py <out.json> <lam_keV> <n_events_per_mass> [--masses 500,1000]
Run with the TT env (numba): $QV2/envs/tt/.pixi/envs/default/bin/python; NUMBA_CACHE_DIR is set to scratch.
"""
import json
import logging
import os
import socket
import sys
import time

QV2 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2'
for p in (f'{QV2}/analytic/numerics', f'{QV2}/code', f'{QV2}/sim/stage3/code'):
    sys.path.insert(0, p)
import numpy as np  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stdout)
log = logging.getLogger('bstar_time')
B0 = 3.8112   # v1 s3common.py l.31 (C.B0)
TOY = '/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/chain/stage3_inputs/F_m{m}_toy.npz'


def one_event(p1, p2, m, lam):
    from nm_kernel import run
    from nm_bstar import bstar_off_fields
    from s3_physics import plane_fit
    out, cpus = {}, {}
    for arm in ('on', 'off'):
        for cfg, f in (('B', 1.0), ('B2', 0.5)):
            t0 = time.process_time()
            kw = dict(max_boost=1e-3, hmax_trk=0.2, qcap=1 << 19, max_steps=20_000_000_000)
            if arm == 'on':
                r = run(p1, p2, m, lam, B0=B0 * f, **kw)
            else:
                El, Bl = bstar_off_fields(p1, p2, m, (0.0, 0.0, B0 * f))
                r = run(p1, p2, m, lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, **kw)
            H = r['hits']
            H = H[H[:, 1] < 10]
            ds = plane_fit(H[:, 3:6], np.zeros(3))[0] * 1e4 if len(H) >= 4 else float('nan')
            out[f'{arm}_{cfg}'] = (float(ds), int(r['status']))
            cpus[f'{arm}_{cfg}'] = time.process_time() - t0
    return out, cpus


def main():
    outp, lam, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    masses = [int(x) for x in sys.argv[sys.argv.index('--masses') + 1].split(',')] if '--masses' in sys.argv else [500, 1000]
    # warm-up: numba compilation, timed separately and excluded from the per-event cost
    d = np.load(TOY.format(m=masses[0]))
    t0 = time.process_time()
    one_event(d['p_qp'][0], d['p_qm'][0], float(masses[0]), lam)
    warm = time.process_time() - t0
    res = dict(lam_keV=lam, node=socket.gethostname(), warmup_cpu_s=warm, events=[],
               start=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    for m in masses:
        d = np.load(TOY.format(m=m))
        idx = np.where(d['in_eta25'])[0][1:1 + n]
        for i in idx:
            o, c = one_event(d['p_qp'][i], d['p_qm'][i], float(m), lam)
            res['events'].append(dict(mass=m, row=int(i), cpu_s=sum(c.values()), cpu_by_run=c,
                                      status={k: v[1] for k, v in o.items()}, ds_um={k: v[0] for k, v in o.items()}))
            log.info('m=%d row=%d cpu=%.1f s status=%s', m, i, sum(c.values()), [v[1] for v in o.values()])
    cp = np.array([e['cpu_s'] for e in res['events']])
    res['summary'] = dict(n=len(cp), mean_cpu_s=float(cp.mean()), median_cpu_s=float(np.median(cp)),
                          max_cpu_s=float(cp.max()), by_mass={m: float(np.mean([e['cpu_s'] for e in res['events']
                                                                                 if e['mass'] == m])) for m in masses})
    res['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    json.dump(res, open(outp, 'w'), indent=1)
    log.info('summary %s', res['summary'])


if __name__ == '__main__':
    main()
