"""p3-f Task A analysis (investigator Jorunn): measurement (i) and the verdict measurement M_T of amendment A1
(`outputs/p3f/CAUSE_METHOD_jorunn_A1.md`): per-configuration refit transfer, the pre-stated criterion of A.3, C2 and the
diagnostics.  Reads the p3-f-occx outputs (mode counts) and the p3-b closure JSON (frozen model outputs; the observed
residuals only as the comparison target).  Writes outputs/p3f/occx_result.json.

  python occx_ana.py [--glob 'p3-f-occx/*/occx-*.npz'] [--out occx_result.json]"""
import argparse
import glob
import json
import logging
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3f')
OUT = HERE.parents[1] / 'outputs' / 'p3f'
P3B = HERE.parents[1] / 'outputs' / 'p3b' / 'b2_dev_closure.json'
log = logging.getLogger('occx_ana')
RLN = ['R04', 'R05', 'R06', 'R07', 'R08', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3', 'R07x2S>=3']
COLI = {'R04': 0, 'R05': 1, 'R06': 2, 'R07': 3, 'R08': 4, 'R04x2S>=3': 13, 'R05x2S>=3': 16, 'R06x2S>=3': 19,
        'R07x2S>=3': 20}
NB = 2000
CAP_PREC = 0.12


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--glob', default='p3-f-occx/*/occx-*.npz')
    ap.add_argument('--out', default='occx_result.json')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    fs = sorted(glob.glob(str(DATA / a.glob)))
    dd = [np.load(f) for f in fs]
    meta = json.loads(str(dd[0]['meta_json']))
    M = meta['planes']
    cnt = np.concatenate([d['cnt'] for d in dd]).astype(float)            # (ntr, 2, ncol): fixed, refit (N_IP2 >= 5)
    cnt5 = np.concatenate([d['cnt5'] for d in dd]).astype(float)          # refit passers with fixed N_IP2 = 5
    ntr = len(cnt)
    key = np.char.add(np.char.add(np.concatenate([d['job'] for d in dd]).astype(str), '|'),
                      np.concatenate([d['ev'] for d in dd]).astype(str))
    uev, inv = np.unique(key, return_inverse=True)
    nev = len(uev)
    ci = [COLI[c] for c in RLN]
    X = np.stack([cnt[:, 0, ci], cnt[:, 1, ci], cnt[:, 1, ci] - cnt5[:, ci]], axis=1) / M   # fixed, refit>=5, refit>=6
    rng = np.random.default_rng(20261124)
    W = rng.multinomial(nev, np.full(nev, 1 / nev), size=NB).astype(float)
    ne = np.bincount(inv, minlength=nev).astype(float)
    Sv = np.zeros((nev,) + X.shape[1:]); np.add.at(Sv, inv, X)
    Pn = Sv.sum(0) / ne.sum()
    Pr = np.tensordot(W, Sv, axes=(1, 0)) / (W @ ne)[:, None, None]
    i = {c: k for k, c in enumerate(RLN)}
    R = json.loads(P3B.read_text())['occupancy']
    Em = R['E_model']; Emc = R['E_model_relMC']; Preal = R['P_real']; C05 = R['C_R05']; C04 = R['C_R04']
    obs = {c: R['predictions'][c]['const'] for c in ('R04', 'R05', 'R06', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3')}
    Bm = {'R04': Preal['R04'], 'R05': Preal['R05'], 'R06': C05 * Em['R06'],
          'R04x2S>=3': Preal['R04x2S>=3'], 'R05x2S>=3': Preal['R05x2S>=3'], 'R06x2S>=3': C05 * Em['R06x2S>=3']}
    res = dict(method=['outputs/p3f/CAUSE_METHOD_jorunn.md', 'outputs/p3f/CAUSE_METHOD_jorunn_A1.md'], files=len(fs),
               trials=ntr, events=nev, planes_per_trial=M, configurations=int(ntr * M), meta=meta)
    names = ['fixed', 'refit_nip5', 'refit_nip6']
    res['per_rung'] = {c: {names[m]: dict(P=float(Pn[m, i[c]]), count=float(Sv[:, m, i[c]].sum() * M))
                           for m in range(3)} for c in RLN}
    # C2: share of refit R04 from fixed N_IP2 = 5
    c2 = float(cnt5[:, 0].sum() / cnt[:, 1, 0].sum())
    reading = 1 if c2 > 0.05 else 2
    res['C2'] = dict(share_refit_R04_from_fixed_NIP2_eq_5=c2, verdict_reading=names[reading],
                     rule='> 0.05 -> N_IP2 >= 5 reading, else N_IP2 >= 6')
    # measurement (i)
    k6, k5, k4 = i['R06'], i['R05'], i['R04']
    C06 = Pn[0, k6] / Em['R06']
    sd_lnC06 = float(np.sqrt(np.var(np.log(Pr[:, 0, k6]), ddof=1) + Emc['R06'] ** 2))
    res['measurement_i'] = dict(
        n_R06_fixed=float(Sv[:, 0, k6].sum() * M), P_fix_R06=float(Pn[0, k6]), E_model_R06=Em['R06'], C_R06=float(C06),
        sd_ln_C_R06=sd_lnC06, C_R05_new=float(Pn[0, k5] / Em['R05']), C_R04_new=float(Pn[0, k4] / Em['R04']),
        C_R05_p3b=C05, C_R04_p3b=C04, ln_C06_over_C05_p3b=float(np.log(C06 / C05)),
        sd_ln_C06_over_C05=float(np.sqrt(sd_lnC06 ** 2 + Emc['R05'] ** 2)))
    crit = {}
    for fam, (r4, rr) in {'s0': ('R04', ('R05', 'R06')), 's3': ('R04x2S>=3', ('R05x2S>=3', 'R06x2S>=3'))}.items():
        for m in (1, 2):
            out = {}
            for r in rr:
                lt = float(np.log(Pn[m, i[r]] / Pn[m, i[r4]]))
                ltr = np.log(Pr[:, m, i[r]] / Pr[:, m, i[r4]])
                sT = float(np.std(ltr[np.isfinite(ltr)], ddof=1))
                pred = obs[r4]['ln_r'] + np.log(Bm[r] / Bm[r4]) - lt
                o = obs[r]['ln_r']; so = obs[r]['sigma_tot']
                sc = float(np.hypot(sT, so))
                tr = lt - float(np.log(Pn[0, i[r]] / Pn[0, i[r4]]))
                trr = ltr - np.log(Pr[:, 0, i[r]] / Pr[:, 0, i[r4]])
                out[r] = dict(ln_r_pred=float(pred), sigma_T=sT, ln_r_obs=o, sigma_tot_obs=so, sigma_comb=sc,
                              diff=float(pred - o), pull=float((pred - o) / sc),
                              a_sign=bool(np.sign(pred) == np.sign(o)), b_within_2sigma=bool(abs(pred - o) <= 2 * sc),
                              c_nonzero_2sigma=bool(abs(pred) >= 2 * sT), ln_refit_fall=lt,
                              ln_model_fall=float(np.log(Bm[r] / Bm[r4])),
                              refit_transfer_vs_fixed=float(tr),
                              sd_refit_transfer=float(np.std(trr[np.isfinite(trr)], ddof=1)))
            good = [out[r]['a_sign'] and out[r]['b_within_2sigma'] and out[r]['c_nonzero_2sigma'] for r in rr]
            prec = out[rr[1]]['sigma_T'] <= CAP_PREC
            v = ('CAUSE FOUND' if all(good) and prec else 'CAUSE NOT FOUND (insufficient precision)' if not prec
                 else 'CAUSE NOT FOUND (partial)' if sum(good) == 1 else 'CAUSE NOT FOUND')
            out['verdict'] = v
            crit[f'{fam}_{names[m]}'] = out
    res['criterion'] = crit
    res['verdict'] = crit[f's0_{names[reading]}']['verdict']
    res['verdict_other_reading'] = crit[f's0_{names[3 - reading]}']['verdict']
    res['D4p_P_refit_R04_over_P_fix_R04'] = {names[m]: float(Pn[m, k4] / Pn[0, k4]) for m in (1, 2)}
    res['rho_implied'] = {names[m]: {c: float((Pn[m, i[c]] / Pn[0, i[c]]) / (Pn[m, k4] / Pn[0, k4]))
                                     for c in ('R05', 'R06', 'R07')} for m in (1, 2)}
    cpu_note = 'CPU from the ledger markers, not from this file'
    res['note'] = cpu_note
    (OUT / a.out).write_text(json.dumps(res, indent=1))
    log.info('C2 share %.4f -> reading %s', c2, names[reading])
    log.info('verdict: %s (other reading: %s)', res['verdict'], res['verdict_other_reading'])
    for m in (1, 2):
        for r in ('R05', 'R06'):
            o = crit[f's0_{names[m]}'][r]
            log.info('%s %s: pred %+.3f +- %.3f  obs %+.3f +- %.3f  pull %+.2f  transfer vs fixed %+.3f +- %.3f',
                     names[m], r, o['ln_r_pred'], o['sigma_T'], o['ln_r_obs'], o['sigma_tot_obs'], o['pull'],
                     o['refit_transfer_vs_fixed'], o['sd_refit_transfer'])
    log.info('C(R06) = %.3f, ln C06/C05 = %+.3f +- %.3f (n_R06 fixed %d)', C06,
             res['measurement_i']['ln_C06_over_C05_p3b'], res['measurement_i']['sd_ln_C06_over_C05'],
             res['measurement_i']['n_R06_fixed'])


if __name__ == '__main__':
    main()
