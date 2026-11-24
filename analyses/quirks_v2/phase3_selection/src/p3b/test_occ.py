"""Checks of occ_core (p3-b, Casper): band_hits against a brute-force numpy band on every hit; timing of real_planes."""
import logging
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import occ_core as OC  # noqa: E402
import occ_replay as RP  # noqa: E402
import thin_core as TC  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger('test_occ')
z, job = RP.open_job(sys.argv[1])
r = RP.replay(z, job, 0)
H, sid, pv = r['H'], r['sid'], r['pv']
ix = OC.build_index(H, sid)
phimet = r['phimets'][0]
rng = np.random.default_rng(1)
out = np.empty(len(H), np.int64)
U = H[:, 1:4] - pv
rr = np.hypot(H[:, 1], H[:, 2]); cx = H[:, 1] / rr; cy = H[:, 2] / rr
r0 = np.hypot(U[:, 0], U[:, 1])
dph = np.abs((np.arctan2(U[:, 1], U[:, 0]) - phimet + np.pi) % (2 * np.pi) - np.pi)
road = dph < OC.ROAD + np.arcsin(np.minimum(1.0, OC.WC / r0))
nbad = 0; ntest = 0; nsum = 0
while ntest < 300:
    phia = phimet + 0.15 * (2 * rng.random() - 1); eta = 2 * rng.random() - 1; psi = np.pi * rng.random()
    if abs(np.sin(psi)) / np.cosh(eta) < OC.NZ_MIN:
        continue
    ntest += 1
    n, a = OC.plane_from(phia, eta, psi)
    m = OC.band_hits(n, a, pv, phimet, H, ix['hid'], ix['Z'], ix['bstart'], ix['boff'], ix['nb'], ix['rr'],
                     ix['s0'], ix['s1'], out)
    got = np.sort(out[:m])
    n2 = np.cross(n, a)
    d = U @ n
    sc2 = (-n[0] * cy + n[1] * cx) ** 2 * H[:, 4] ** 2 + n[2] ** 2 * H[:, 5] ** 2
    ok = (d * d < 9 * (np.maximum(sc2, 1e-8) + 0.03 ** 2)) & (U @ a > 0) & (np.abs(U @ n2) < 75) & road
    ref = np.where(ok)[0]
    nsum += len(ref)
    if len(ref) != len(got) or np.any(ref != got):
        nbad += 1
log.info('band_hits vs brute force: %d mismatching planes of %d (mean in-band hits %.1f)', nbad, ntest, nsum / ntest)
A = OC.trial_arrays(H, sid, pv)
for npl in (2000, 20000):
    t0 = time.time()
    cnt, mh, ntot = OC.real_planes(H, A['LC'], A['SD'], A['U'], A['CX'], A['CY'], A['S0'], A['S1'], ix['hid'], ix['Z'],
                                   ix['bstart'], ix['boff'], ix['nb'], ix['rr'], ix['s0'], ix['s1'], pv, phimet,
                                   npl, 7, TC.CHI2_ISF, TC.NCOL)
    lay = np.array([sum(mh[k] for k in range(1024) if (k >> l) & 1) for l in range(10)]) / npl
    log.info('real_planes %d: %.1f s; R04..R07 %s; P(layer>=2) %s; mean in-band %.1f', npl, time.time() - t0,
             cnt[:4], np.round(lay, 3), ntot / npl)
