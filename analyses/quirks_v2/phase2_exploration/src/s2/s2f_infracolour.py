"""s2f_infracolour.py -- S2-f (COM S2-f; STR §4.14 (a')): the O(alpha_IC) infracolour Coulomb correction per mass,
averaged over the generated beta distribution of each sample.  FORM USED (STR §4.14 (a'), "from review P-B5 and the
arbiter's re-derivation; to be replaced by a cited treatment, R-12"; tagged accordingly, NOT a literature value):
    alpha_IC(mu) = 2 pi / (b0 ln(mu/Lambda)),  b0 = 22/3 (one-loop pure SU(2)),  mu = m
    delta(beta)  = C_F alpha_IC (pi/(2 beta) - 4/pi),  C_F = 3/4
and, as the refinement quoted there, the vector-current threshold factor
    delta_V(beta) = C_F alpha_IC [pi/(2 beta) - (3 + beta)/(4 pi) (pi^2/2 - 3/4)].
beta = velocity of each quirk in the pair rest frame at production, from the hard-process momenta (npz p_qp_hard,
p_qm_hard; status-23 LHE kinematics).  Average weighted by the nominal merged weight w (w > 0 rows; inclusive sample).
Limiting check printed: alpha_IC -> 0 gives delta = 0 (Lambda -> 0 is alpha -> 0 logarithmically); substitution check
against STR: alpha_IC(200 GeV, 1 keV) = 0.045, delta = +3.3/+6.3/+13.3 % at beta = 0.7/0.5/0.3.
Lambda grid: the eight Stage-3 values 0.45, 0.6, 0.85, 1, 1.5, 2, 3, 5 keV (STR §4.0 l.369-370 and §4.13).
Usage (worker, numpy env): python s2f_infracolour.py <out.json> <label>=<campaign>:<file prefix> ...
(Edgar 2026-11-17: files are the '.nom.npz' outputs listed in the campaign's done markers, sha256 re-checked;
 delta averaged vectorised; the weighted beta quantiles and the weight fraction at beta < 0.1, where the O(alpha)
 expansion is least reliable, are recorded.)
"""
import json
import logging
import math
import os
import sys

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('s2f')
B0, CF = 22.0 / 3.0, 0.75
LAMS_KEV = [0.45, 0.6, 0.85, 1.0, 1.5, 2.0, 3.0, 5.0]


def alpha_ic(mu_gev, lam_kev):
    return 2 * math.pi / (B0 * math.log(mu_gev / (lam_kev * 1e-6)))


def delta(beta, a):
    return CF * a * (math.pi / (2 * beta) - 4 / math.pi)


def delta_v(beta, a):
    return CF * a * (math.pi / (2 * beta) - (3 + beta) / (4 * math.pi) * (math.pi ** 2 / 2 - 0.75))


def beta_cm(p1, p2):
    """quirk speed in the pair rest frame from 4-vectors (E, px, py, pz) arrays [N, 4]."""
    P = p1 + p2
    m2 = P[:, 0] ** 2 - (P[:, 1:] ** 2).sum(1)
    mq2 = p1[:, 0] ** 2 - (p1[:, 1:] ** 2).sum(1)
    return np.sqrt(np.clip(1 - 4 * mq2 / m2, 0, 1))


def main():
    out = sys.argv[1]
    a = alpha_ic(200.0, 1.0)
    chk = dict(alpha_200GeV_1keV=a, delta_pct_beta_0p7_0p5_0p3=[100 * delta(b, a) for b in (0.7, 0.5, 0.3)],
               delta_v_pct=[100 * delta_v(b, a) for b in (0.7, 0.5, 0.3)])
    log.info('substitution check: %s', chk)
    res = dict(check=chk, form='STR §4.14 (a\'): review P-B5 / arbiter; not sourced (R-12 pending)', points={})
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from marker_files import done_outputs
    for arg in sys.argv[2:]:
        label, spec = arg.split('=', 1)
        camp, prefix = spec.split(':', 1)
        files = done_outputs(camp, suffix='.nom.npz', prefix=prefix, verify=True)
        if not files:
            log.warning('%s: no done files', label)
            continue
        b, w, m, spin = [], [], None, None
        for f in files:
            d = np.load(f)
            pos = d['w'] > 0
            b.append(beta_cm(d['p_qp_hard'][pos], d['p_qm_hard'][pos]))
            w.append(d['w'][pos])
            m, spin = float(d['mq']), str(d['spin'])
        b = np.concatenate(b)
        w = np.concatenate(w)
        ok = b > 1e-6
        bo, wo = b[ok], w[ok]
        srt = np.argsort(bo)
        cw = np.cumsum(wo[srt]) / wo.sum()
        q = {str(x): float(bo[srt][np.searchsorted(cw, x)]) for x in (0.05, 0.16, 0.5, 0.84, 0.95)}
        r = dict(mass=m, spin=spin, n=int(ok.sum()), n_dropped_beta0=int((~ok).sum()), files=len(files),
                 beta_weighted_quantiles=q, weight_frac_beta_lt_0p1=float(wo[bo < 0.1].sum() / wo.sum()),
                 mean_inv_beta=float(np.average(1 / bo, weights=wo)), by_lambda={})
        for lam in LAMS_KEV:
            al = alpha_ic(m, lam)
            dl = CF * al * (math.pi / (2 * bo) - 4 / math.pi)
            dv = CF * al * (math.pi / (2 * bo) - (3 + bo) / (4 * math.pi) * (math.pi ** 2 / 2 - 0.75))
            r['by_lambda'][str(lam)] = dict(alpha_ic=al, mean_delta=float(np.average(dl, weights=wo)),
                                            mean_delta_v=float(np.average(dv, weights=wo)))
        res['points'][label] = r
        log.info('%s m=%g n=%d: delta(1 keV) = %.4f', label, m, r['n'], r['by_lambda']['1.0']['mean_delta'])
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
