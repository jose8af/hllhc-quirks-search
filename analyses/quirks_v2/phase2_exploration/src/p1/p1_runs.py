"""p1_runs.py -- P1 production runs on new events (EXPLORATION §3.1), channel (ii) Sebastian, 2026-11-16.
Events: an npz written by make_p1_events.py (p_qp, p_qm 3-momenta [GeV], closed-form c_ev, k_B, eps_perp, gstar at the
npz's Lambda); rows [i0, i0 + n).  Kernel settings as v1's B*-off test (sim/stage3/scripts/fix_bstar_off.py l.33-60):
max_boost 1e-3, hmax_trk 0.2 cm, qcap 2^19, vacuum, vertex at the origin, Delta_s = plane fit of hits on the 10 barrel
layers (layer id < 10), c2 = (2 Delta_s(B0/2)/Delta_s(B0) - 1)/ln 2.
Modes:
  bstar : 4 runs per event (arms on/off x fields B0, B0/2)      -> P1-b (paired B*-off test)
  pop   : 2 runs per event (arm on, fields B0, B0/2)           -> P1-c (population estimator: paired median c2 - c_ev)
  floor : FIX2 'off' arm at fractions f with kernel nominal|t44|dd|rn44|rn47 (rn*: round-to-nearest diagnostic), detector scaled by s, hmax 0.02 cm x s, qcap 2^21
          (analytic/numerics/FIX2_runs.py l.27-50)                -> P1-a floor test 2 / dd diagnostic
Usage: python p1_runs.py <out.json> <events.npz> <mode> <lam_keV> <i0> <n> [--kernel K] [--s S] [--fr 1,0.5,...]
"""
import json
import logging
import math
import os
import socket
import sys
import time

QV2 = '/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2'
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (f'{QV2}/analytic/numerics', f'{QV2}/code', f'{QV2}/sim/stage3/code', HERE):
    sys.path.insert(0, p)
import numpy as np  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stdout)
log = logging.getLogger('p1_runs')
B0 = 3.8112    # v1 s3common.py l.31


def ds_of(r, origin0=True):
    from s3_physics import plane_fit
    H = r['hits']
    H = H[H[:, 1] < 10]
    return float(plane_fit(H[:, 3:6], np.zeros(3))[0]) * 1e4 if len(H) >= 4 else float('nan')   # um


def main():
    a = sys.argv
    out, evf, mode, lam, i0, n = a[1], a[2], a[3], float(a[4]), int(a[5]), int(a[6])
    kern = a[a.index('--kernel') + 1] if '--kernel' in a else 'nominal'
    s = float(a[a.index('--s') + 1]) if '--s' in a else 1.0
    frs = [float(x) for x in a[a.index('--fr') + 1].split(',')] if '--fr' in a else [1, 0.5, 0.4, 0.25, 0.05]
    run = __import__({'nominal': 'nm_kernel', 't44': 'nm_kernel_t44', 'dd': 'nm_kernel_dd',
                      'rn44': 'nm_kernel_rn44', 'rn47': 'nm_kernel_rn47'}[kern]).run   # rn*: Edgar 2026-11-17 diagnostic
    from nm_bstar import bstar_off_fields
    E = np.load(evf)
    m = float(E['mass'])
    res = dict(mode=mode, lam_keV=lam, kernel=kern, s=s, events_file=evf, mass=m, node=socket.gethostname(),
               start=time.strftime('%Y-%m-%d %H:%M:%S %z'), events=[])
    for i in range(i0, min(i0 + n, len(E['p_qp']))):
        p1, p2 = E['p_qp'][i], E['p_qm'][i]
        t0 = time.process_time()
        rec = dict(i=i, row=int(E['row'][i]), src=str(E['src'][i]), c_ev=float(E['c_ev'][i]), k_B=float(E['k_B'][i]),
                   eps_perp=float(E['eps_perp'][i]), gstar=float(E['gstar'][i]))
        if mode in ('bstar', 'pop'):
            kw = dict(max_boost=1e-3, hmax_trk=0.2, qcap=1 << 19, max_steps=20_000_000_000)
            arms = ('on', 'off') if mode == 'bstar' else ('on',)
            for arm in arms:
                d = {}
                for cfg, f in (('B', 1.0), ('B2', 0.5)):
                    if arm == 'on':
                        r = run(p1, p2, m, lam, B0=B0 * f, **kw)
                    else:
                        El, Bl = bstar_off_fields(p1, p2, m, (0.0, 0.0, B0 * f))
                        r = run(p1, p2, m, lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, **kw)
                    d[cfg] = (ds_of(r), int(r['status']))
                rec[f'{arm}_ds_B'], rec[f'{arm}_ds_B2'] = d['B'][0], d['B2'][0]
                rec[f'{arm}_status'] = [d['B'][1], d['B2'][1]]
                rec[f'c_{arm}'] = (2 * d['B2'][0] / d['B'][0] - 1) / math.log(2) if d['B'][0] > 0 else float('nan')
        else:
            from T3_propagator import REC_RADII, REC_ZMAX, plane_fit
            geo = dict(rec_radii=REC_RADII * s, rec_zmax=REC_ZMAX * s, r_exit=118.0 * s, z_exit=290.0 * s,
                       hmax_trk=0.02 * s, hmax_out=2.0 * s)
            ds, st = [], []
            for f in frs:
                El, Bl = bstar_off_fields(p1, p2, m, (0.0, 0.0, B0 * f))
                r = run(p1, p2, m, lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, max_boost=1e-3, max_steps=8_000_000_000,
                        qcap=1 << 21, **geo)
                H = r['hits']
                H = H[H[:, 1] < 10]
                ds.append(float(plane_fit(H[:, 3:6])[0]) if len(H) >= 4 else float('nan'))
                st.append(int(r['status']))
            rec.update(fr=frs, ds=ds, status=st)
        rec['cpu_s'] = time.process_time() - t0
        res['events'].append(rec)
        log.info('i=%d cpu %.1f s', i, rec['cpu_s'])
    res['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
