"""Frozen dE/dx admissibility e_adm(m, Lambda) with PU dilution (WP_RULE.md §8; fix of review WP_RULE R1 B-1).

Signal-blind: generator/truth-level inputs only (Stage-3 truth TBPX hit counts and beta*gamma_IT, the Bethe restricted-
loss model of plan §2.6, plan §2.1 PU numbers). No detector-level signal efficiency, no detector response of the signal.

Model (pre-declared; the "frozen mixture model" of review WP_RULE R1 B-1 (ii)(a)):
  * estimator = the production one (WP_RULE.md §1.4): mean of the lowest 60 % of the path-corrected dE of the candidate's
    CORE TBPX hits (|u.n2 - c| <= 2.5 w_core), in units of the pooled MIP unit (same estimator on a large pooled MIP
    sample, i.e. the F-2 definition);
  * per-hit loss in MIP units: Moyal(loc = R_hit, scale = 0.12 R_hit) (thin-Si Landau proxy of the review), R_hit = 1
    for PU (MIP) hits and R = R(beta*gamma_IT(m, Lambda)) for quirk hits; R = the plan §2.6 restricted-loss ratio
    (PDG-2024 Si, T_cut = 100 keV) of the quirk at beta*gamma_IT(m, Lambda) (max rule) to the muon gun at
    beta*gamma_mu = 92 (F-3);
  * quirk hits: n_q(m, Lambda) = median over the point's fiducial template-half events (tt_split == 0, in_eta25,
    status == 1, |eta_pair| < ETA_MAX) of the number of truth TBPX quirk hits (both quirks); all of them in the core;
  * PU hits in the core: Poisson, mean sum_l mu_c,l * min(1, 2 * 2.5 * W_k / X_l), with mu_c,l the TDR-normalised
    in-band TBPX crossings of plan §2.1 (8, 3, 1.5, 1.0 for L1-L4), X_l = min(2 W_c, 2 r_l) the n2-extent of the
    in-window layer intersection, W_k = W_c / 2^k at k = k_adm(m, Lambda) (the width bound of the admissible rung, the
    worst case for that rung); k_adm = 0 (no width cut) -> the full band (factor 1);
  * R_eff(m, Lambda) = the median of the estimator over NTOY toys; e_adm = the largest e in {1.3, 1.6, 2.0} with
    e <= R_eff / 1.25, else none.
  If the B1-measured in-band TBPX crossing density ratio rho_dens (PU-only; operational definition in WP_RULE.md §8)
  exceeds 1.05 (fix WP_RULE R2 C-5; was 20 %), this script is re-run unchanged with MU_C scaled by rho_dens
  (pre-declared, PU-only input; WP_RULE.md §8).
Run (theory_track): nice -n 10 pixi run python -m acts.stage4.finder.eadm_dilution [mu_scale]
Output: data/acts_stage4/frozen/eadm_dilution.json
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.stats import moyal

TT = Path(__file__).resolve().parents[3]
S3 = TT / 'data/sim_stage3'
F4R = TT / 'data/acts_stage4/fix_r4/f4r_admissibility.json'
OUT = TT / 'data/acts_stage4/frozen/eadm_dilution.json'
ETA_MAX = 1.0                                   # barrel-only fiducial limit (WP_RULE.md §1.2)
BG_MU = 92.0                                    # F-3: median beta*gamma of the V4-9 muon gun (pT U[1,10], |eta| < 2.5)
MU_C = np.array([8.0, 3.0, 1.5, 1.0])           # plan §2.1, TDR-normalised in-band TBPX L1-L4 crossings
R_L = np.array([30.0, 61.5, 104.5, 146.5])      # mm, TBPX radii (surfaces_s3.json)
W_C = 75.0
W_K = [None, 37.5, 18.75, 9.4, 4.7]
E_LEV = (1.3, 1.6, 2.0)
MARGIN = 1.25
TRUNC = 0.6
NTOY = 4000
SEED = 20261013

ME = 0.51099895e-3; I_SI = 173.0e-9; MMU = 0.1056583755
CB, X0, X1, A_, K_, D0 = 4.4355, 0.2015, 2.8716, 0.1492, 3.2546, 0.14     # PDG-2024 Si (WP_RULE.md §8)


def delta(bgv):
    x = math.log10(bgv)
    if x >= X1:
        return 2 * math.log(10) * x - CB
    if x >= X0:
        return 2 * math.log(10) * x - CB + A_ * (X1 - x) ** K_
    return D0 * 10 ** (2 * (x - X0))


def loss(bgv, M, tcut=1e-4):
    g = math.sqrt(1 + bgv * bgv); b2 = bgv * bgv / (g * g)
    tmax = 2 * ME * bgv * bgv / (1 + 2 * g * ME / M + (ME / M) ** 2); tup = min(tcut, tmax)
    return (0.5 * math.log(2 * ME * bgv * bgv * tup / I_SI ** 2) - b2 / 2 * (1 + tup / tmax) - delta(bgv) / 2) / b2


def est(v):
    """lowest-60 % truncated mean along the last axis (v sorted inside); NaN-padded rows allowed."""
    v = np.sort(v, axis=-1)
    n = np.sum(np.isfinite(v), axis=-1)
    k = np.maximum(1, np.ceil(TRUNC * n).astype(int))
    cs = np.nancumsum(np.where(np.isfinite(v), v, 0.0), axis=-1)
    return cs[np.arange(len(v)), k - 1] / k


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(mu_scale=1.0):
    rng = np.random.default_rng(SEED)
    f4r = json.loads(F4R.read_text())
    idx = json.loads((S3 / 'STAGE3_INDEX.json').read_text())
    # ---- n_q(m, Lambda): truth TBPX quirk hits, fiducial template-half events
    nq = {}
    for key, pt in idx['points'].items():
        if not (key.startswith('p2/') and key.endswith('_BM')):
            continue
        sp = key.split('/')[1]; lam = float(key.split('/')[2][1:].replace('_BM', ''))
        n = []
        for ch in pt['chunks']:
            d = np.load(S3 / ch['file'])
            assert list(d['surf_names'][:4]) == ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4']
            pp = d['p_qp'] + d['p_qm']
            eta = np.arcsinh(pp[:, 2] / np.maximum(np.hypot(pp[:, 0], pp[:, 1]), 1e-12))
            sel = (d['tt_split'] == 0) & (d['in_eta25'] > 0) & (d['status'] == 1) & (np.abs(eta) < ETA_MAX)
            n.append(d['nhit_surf'][sel][:, 0:4, :].sum(axis=(1, 2)))
        n = np.concatenate(n)
        nq.setdefault(sp, {})['%g' % lam] = (int(np.median(n)) if len(n) else None, int(len(n)))
    # ---- pooled MIP unit of the estimator (large-n limit, F-2 definition)
    unit = float(est(moyal.rvs(loc=1, scale=0.12, size=(1, 400000), random_state=rng))[0])
    lmu = loss(BG_MU, MMU)
    xl = np.minimum(2 * W_C, 2 * R_L)
    res = {}
    for sp, v in f4r['betagamma_IT'].items():
        m = float(sp.split('_m')[1])
        thr = f4r['Lambda_R'][sp]['k_thresholds_keV']
        row = {}
        for lam, bpt in v['per_Lambda'].items():
            L = float(lam)
            k = max([kk for kk in range(1, 5) if L >= thr['k>=%d' % kk]], default=0)
            b = max(v['betagamma_IT'], bpt)
            R = loss(b, m) / lmu
            nqv, nev = nq.get(sp, {}).get(lam, (None, 0))
            if not nqv:
                row[lam] = dict(k_adm=k, bg=b, R=round(R, 3), n_q=nqv, n_ev=nev, R_eff=None, e_adm=None,
                                e_adm_undiluted=max([e for e in E_LEV if e <= R / MARGIN], default=None))
                continue
            fr = 1.0 if k == 0 else np.minimum(1.0, 2 * 2.5 * W_K[k] / xl)
            mu_pu = float(mu_scale * np.sum(MU_C * fr))
            npu = rng.poisson(mu_pu, NTOY)
            nmax = nqv + int(npu.max())
            V = np.full((NTOY, nmax), np.nan)
            V[:, :nqv] = moyal.rvs(loc=R, scale=0.12 * R, size=(NTOY, nqv), random_state=rng)
            P = moyal.rvs(loc=1, scale=0.12, size=(NTOY, nmax - nqv), random_state=rng)
            P[np.arange(nmax - nqv)[None, :] >= npu[:, None]] = np.nan
            V[:, nqv:] = P
            e = est(V) / unit
            Reff = float(np.median(e))
            row[lam] = dict(k_adm=k, bg=round(b, 3), R=round(R, 3), n_q=nqv, n_ev=nev, mu_pu_core=round(mu_pu, 2),
                            R_eff=round(Reff, 3),
                            e_adm=max([x for x in E_LEV if x <= Reff / MARGIN], default=None),
                            e_adm_undiluted=max([x for x in E_LEV if x <= R / MARGIN], default=None))
        res[sp] = row
    out = dict(note=__doc__, eta_max=ETA_MAX, bg_mu=BG_MU, mu_c=MU_C.tolist(), mu_scale=mu_scale, x_l_mm=xl.tolist(),
               unit_estimator=unit, ntoy=NTOY, seed=SEED, margin=MARGIN, trunc=TRUNC,
               inputs_sha256={'f4r_admissibility.json': sha(F4R), 'STAGE3_INDEX.json': sha(S3 / 'STAGE3_INDEX.json'),
                              'eadm_dilution.py': sha(__file__)},
               e_adm=res)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    for sp, row in res.items():
        print(sp, ' '.join('%s:k%d/%s/%s' % (l, r['k_adm'], r['e_adm_undiluted'], r['e_adm']) for l, r in row.items()))


if __name__ == '__main__':
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 1.0)
