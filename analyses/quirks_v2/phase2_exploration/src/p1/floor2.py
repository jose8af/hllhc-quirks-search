"""floor2.py -- P1 floor test 2 (STR §4.15; COM P1-a): B*-off runs (v1 FIX2 'off' arm, analytic/numerics/FIX2_runs.py
l.27-50) with the nominal kernel and with the 44-bit-mantissa kernel (nm_kernel_t44.py), at field fractions f, so that
c_k = (Delta_s(B/k) k / Delta_s(B) - 1)/ln k can be formed per event and kernel.  Pre-declared reading: if the per-period
excess is the double-precision floor, the 44-bit kernel shows the nominal kernel's Delta_c(20) distribution already at
k = 2.5 (8x larger eps_perp), with the eps_perp^-2 shape; two-sample test at p > 0.05 (evaluation script, not here).
Settings as FIX2: max_boost 1e-3, hmax_trk 0.02 cm x s, string-queue cap 2^21, detector scaled by s (radii, z-limits,
exits, hmax), vacuum, vertex at the origin.  Events: Phase-1 toy Stage-3 inputs (|eta_pair| < 1 subset) or an npz given.
Usage: python floor2.py <out.json> <kernel nominal|t44> <lam_keV> <s> <mass> <i0> <n> [--fr 1,0.5,0.4,0.25,0.05]
"""
import json
import logging
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
log = logging.getLogger('floor2')
B0 = 3.8112
TOY = '/nfs/cajuela/jdochoa/quirks_v2/data/feasibility/chain/stage3_inputs/F_m{m}_toy.npz'


def main():
    out, kern, lam, s, m, i0, n = (sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                                   int(sys.argv[6]), int(sys.argv[7]))
    frs = [float(x) for x in sys.argv[sys.argv.index('--fr') + 1].split(',')] if '--fr' in sys.argv else [1, 0.5, 0.4, 0.25, 0.05]
    run = __import__('nm_kernel' if kern == 'nominal' else 'nm_kernel_t44').run
    from nm_bstar import bstar_off_fields
    from T3_propagator import plane_fit, REC_RADII, REC_ZMAX
    d = np.load(TOY.format(m=m))
    idx = np.where(np.abs(d['eta']) < 1.0)[0][i0:i0 + n]
    res = dict(kernel=kern, lam_keV=lam, s=s, mass=m, fr=frs, node=socket.gethostname(), events=[],
               start=time.strftime('%Y-%m-%d %H:%M:%S %z'))
    geo = dict(rec_radii=REC_RADII * s, rec_zmax=REC_ZMAX * s, r_exit=118.0 * s, z_exit=290.0 * s,
               hmax_trk=0.02 * s, hmax_out=2.0 * s)
    for i in idx:
        p1, p2 = d['p_qp'][i], d['p_qm'][i]
        ds, st, cpu = [], [], []
        for f in frs:
            t0 = time.process_time()
            El, Bl = bstar_off_fields(p1, p2, float(m), (0.0, 0.0, B0 * f))
            r = run(p1, p2, float(m), lam, B0=Bl[2], Bxy=(Bl[0], Bl[1]), E=El, max_boost=1e-3, max_steps=8_000_000_000,
                    qcap=1 << 21, **geo)
            H = r['hits']
            H = H[H[:, 1] < 10]
            ds.append(float(plane_fit(H[:, 3:6])[0]) if len(H) >= 4 else float('nan'))
            st.append(int(r['status']))
            cpu.append(time.process_time() - t0)
        res['events'].append(dict(row=int(i), p_qp=p1.tolist(), p_qm=p2.tolist(), ds=ds, status=st, cpu_s=cpu))
        log.info('row %d: ds %s status %s cpu %.1f', i, ['%.4g' % x for x in ds], st, sum(cpu))
    res['end'] = time.strftime('%Y-%m-%d %H:%M:%S %z')
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
