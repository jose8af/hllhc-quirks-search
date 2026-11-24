"""Runner job: evaluate the semi-analytic occupancy model (occ_model) on the configuration ensemble (B2-b, p3-b, Casper).

  python occmod_job.py --id ID --inputs <dir with p3-b-occin outputs> --seed S [--nA 200000 --nB 4000 --nplain 200
                       --nis 200 --beta 0.5]
Densities: the summed per-surface z histograms of the occin outputs (development events), ρ_j = counts / (N_ev 2π R_j DZ).
Stage A: nA configurations from the prior (PV from the luminous region, phimet uniform, occ_core plane ensemble) ->
P_R04(θ), P(N_2S2 >= j | θ), per-layer probabilities.  Stage B: nB configurations resampled ∝ P_R04(θ) -> plain toys
(R05-R08) and importance-sampled toys (R05-R08) conditional on R04, with the 2S weights.
Output $QV2_OUT_DIR/ID.npz with the stage sums (see keys)."""
import argparse
import glob
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
import occ_model as OM  # noqa: E402

log = logging.getLogger('occmod_job')


def densities(files):
    zh = None; nev = 0
    for f in files:
        d = np.load(f)
        zh = d['zhist'].astype(np.float64) if zh is None else zh + d['zhist']
        nev += int(d['n_events']); s0 = d['s0']; s1 = d['s1']
    R = OC.FF.R_NOM.copy()
    rho = zh / (nev * 2 * np.pi * R[:, None] * OC.DZ)
    cdf = np.zeros((16, OC.NZB + 1))
    cdf[:, 1:] = np.cumsum(rho * OC.DZ, axis=1)
    cdfp = np.array([(cdf[4 + 2 * k] + cdf[5 + 2 * k]) / 2 for k in range(6)])
    return dict(R=R, s0=s0, s1=s1, cdf=cdf, cdfp=cdfp, nev=nev, rho=rho)


def draw_theta(rng):
    while True:
        pv = np.array([rng.normal(0, 5e-3), rng.normal(0, 5e-3), rng.normal(0, 45.0)])
        phimet = rng.uniform(-np.pi, np.pi)
        phia = phimet + OC.ROAD * (2 * rng.random() - 1); eta = 2 * rng.random() - 1; psi = np.pi * rng.random()
        if abs(np.sin(psi)) / np.cosh(eta) >= OC.NZ_MIN:
            return pv, phimet, phia, eta, psi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--inputs', required=True)
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--nA', type=int, default=200000)
    ap.add_argument('--nB', type=int, default=4000)
    ap.add_argument('--nplain', type=int, default=200)
    ap.add_argument('--nis', type=int, default=200)
    ap.add_argument('--beta', type=float, default=0.5)
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    files = sorted(glob.glob(os.path.join(a.inputs, '*', 'occin-*.npz')) + glob.glob(os.path.join(a.inputs, 'occin-*.npz')))
    D = densities(files)
    log.info('densities from %d files, %d events', len(files), D['nev'])
    rng = np.random.default_rng(a.seed)
    np.random.seed(a.seed % (2 ** 31 - 1))
    OM.np.random.seed(a.seed % (2 ** 31 - 1))
    S = np.empty(OM.MAXP); Wt = np.empty(OM.MAXP); off = np.zeros(23, np.int64); lam = np.zeros(22); pl = np.zeros(10)
    th = np.zeros((a.nA, 7)); pA = np.zeros(a.nA); p2A = np.zeros((a.nA, 3)); plA = np.zeros(10); lamA = np.zeros(22)
    t0 = time.time(); nover = 0
    for i in range(a.nA):
        pv, phimet, phia, eta, psi = draw_theta(rng)
        n, ax = OC.plane_from(phia, eta, psi)
        nc = OM.config_units(n, ax, pv, phimet, D['R'], D['s0'], D['s1'], D['cdf'], D['cdfp'], False, S, Wt, off, lam)
        if nc < 0:
            nover += 1
            continue
        OM.layer_probs(lam, pl)
        th[i] = [pv[0], pv[1], pv[2], phimet, phia, eta, psi]
        pA[i] = np.prod(pl[:7])
        for j in range(3):
            p2A[i, j] = OM.p2s(pl, j + 1)
        plA += pl; lamA += lam
    log.info('stage A: %d configurations in %.0f s, mean P_R04 %.3e, overflow %d', a.nA, time.time() - t0, pA.mean(),
             nover)
    # stage B: resample ∝ P_R04
    pr = pA / pA.sum()
    idx = rng.choice(a.nA, size=a.nB, p=pr)
    plain = np.zeros((a.nB, 4)); isr = np.zeros((a.nB, 4, 3)); p2B = np.zeros((a.nB, 3))
    t0 = time.time()
    for b, i in enumerate(idx):
        pv = th[i, :3]; phimet = th[i, 3]
        n, ax = OC.plane_from(th[i, 4], th[i, 5], th[i, 6])
        OM.config_units(n, ax, pv, phimet, D['R'], D['s0'], D['s1'], D['cdf'], D['cdfp'], False, S, Wt, off, lam)
        p2B[b] = p2A[i]
        cw = np.cumsum(Wt[:off[OM.NCAT]])
        # per-category sorted positions with cumulative weights
        ss = np.empty(off[OM.NCAT]); sw = np.empty(off[OM.NCAT])
        for c in range(OM.NCAT):
            lo, hi = off[c], off[c + 1]
            o = np.argsort(S[lo:hi], kind='stable')
            ss[lo:hi] = S[lo:hi][o]; sw[lo:hi] = Wt[lo:hi][o]
        scw = np.cumsum(sw)
        o4 = np.zeros(4)
        OM.plain_toys(S[:off[OM.NCAT]], cw, off, lam, a.nplain, o4)
        plain[b] = o4
        for k in range(4):
            r = np.zeros(3)
            OM.is_toys(S[:off[OM.NCAT]], cw, off, lam, a.nis, k, a.beta, ss, scw, np.zeros(1, np.int64), r)
            isr[b, k] = r
        if b % 500 == 0:
            log.info('stage B %d/%d, %.0f s', b, a.nB, time.time() - t0)
    code = {f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()
            for f in ('occ_core.py', 'occ_model.py', 'occmod_job.py')}
    meta = dict(inputs=files, nev=D['nev'], nA=a.nA, nB=a.nB, nplain=a.nplain, nis=a.nis, beta=a.beta, seed=a.seed,
                code_sha256=code, created_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    np.savez_compressed(out / f'{a.id}.npz', pA=pA, p2A=p2A, plA_mean=plA / a.nA, lamA_mean=lamA / a.nA, th=th,
                        idxB=idx, plain=plain, isr=isr, p2B=p2B, rho=D['rho'], meta_json=np.array(json.dumps(meta)))


if __name__ == '__main__':
    main()
