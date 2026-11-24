"""p3-f Task A analysis (investigator Jorunn): measurement (i) and M_G of CAUSE_METHOD_jorunn.md, the pre-stated
criterion, and the decomposition D1-D4.  Reads the p3-f-occx outputs and the p3-b closure JSON (model outputs, the
observed residuals as the comparison target).  Writes outputs/p3f/occx_result.json.

  python occx_ana.py [--glob 'p3-f-occx/*/occx-*.npz'] [--out occx_result.json] [--c2]
--c2 : the eligibility-loss check (runs on a campaign-mode output made with --nip-elig 5; R04 only)."""
import argparse
import glob
import json
import logging
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3f')
OUT = HERE.parents[1] / 'outputs' / 'p3f'
P3B = HERE.parents[1] / 'outputs' / 'p3b' / 'b2_dev_closure.json'
log = logging.getLogger('occx_ana')
RLN = ['R04', 'R05', 'R06', 'R07', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3', 'R07x2S>=3']
COLI = {'R04': 0, 'R05': 1, 'R06': 2, 'R07': 3, 'R04x2S>=3': 13, 'R05x2S>=3': 16, 'R06x2S>=3': 19, 'R07x2S>=3': 20}
NB = 2000


def load(pattern):
    fs = sorted(glob.glob(str(DATA / pattern)))
    return fs, [np.load(f) for f in fs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--glob', default='p3-f-occx/*/occx-*.npz')
    ap.add_argument('--out', default='occx_result.json')
    ap.add_argument('--c2', action='store_true')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    fs, dd = load(a.glob)
    meta = json.loads(str(dd[0]['meta_json']))
    M = meta['planes']
    cnt = np.concatenate([d['cnt'] for d in dd]).astype(float)          # (ntr, 2, ncol)
    ntr = len(cnt)
    key = np.char.add(np.char.add(np.concatenate([d['job'] for d in dd]).astype(str), '|'),
                      np.concatenate([d['ev'] for d in dd]).astype(str))
    uev, inv = np.unique(key, return_inverse=True)
    nev = len(uev)
    # per-trial HT sums
    G = np.zeros((ntr, 2, len(RLN)))
    off = 0
    edge_w = np.zeros((2, len(RLN))); all_w = np.zeros((2, len(RLN)))
    nrec = np.zeros(2); nedge = np.zeros(2); ndbl = []
    nip5_w = 0.0; r04_w = 0.0
    for d in dd:
        t = d['v_trial'].astype(int) + off
        mp = d['v_map'].astype(int); fl = d['v_flags'].astype(bool); s = d['v_s']; V = d['v_V']; ed = d['v_edge']
        aux = d['v_aux']
        with np.errstate(divide='ignore'):
            w = np.where(fl, s[:, None] / np.where(V > 0, V, np.nan), 0.0) / M
        if np.any(fl & ~(V > 0)):
            raise RuntimeError('V = 0 for a passing rung')
        np.add.at(G, (t, mp), w)
        for k in (0, 1):
            m = mp == k
            nrec[k] += m.sum(); nedge[k] += (m & ed).sum()
            edge_w[k] += w[m & ed].sum(0); all_w[k] += w[m].sum(0)
        ndbl.append(d['v_ndbl'])
        m1 = mp == 1
        nip5_w += w[m1 & (aux[:, 3] == 5), 0].sum(); r04_w += w[m1, 0].sum()
        off += len(d['cnt'])
    if a.c2:
        res = dict(trials=ntr, nip_elig=meta['nip_elig'], frac_G_refit_R04_from_fixed_NIP2_eq_5=float(nip5_w / r04_w),
                   criterion='> 0.05 -> campaign uses N_IP2 >= 5')
        log.info('C2: fraction of G_refit(R04) from fixed N_IP2 = 5: %.4f', nip5_w / r04_w)
        (OUT / a.out).write_text(json.dumps(res, indent=1))
        return
    rng = np.random.default_rng(20261124)
    W = rng.multinomial(nev, np.full(nev, 1 / nev), size=NB).astype(float)
    ne = np.bincount(inv, minlength=nev).astype(float)

    def boot(X):
        Sv = np.zeros((nev,) + X.shape[1:]); np.add.at(Sv, inv, X)
        nom = Sv.sum(0) / ne.sum()
        rep = np.tensordot(W, Sv, axes=(1, 0)) / (W @ ne).reshape((NB,) + (1,) * (X.ndim - 1))
        return nom, rep

    P = cnt[:, :, [COLI[c] for c in RLN]] / M
    Pn, Pr = boot(P)
    Gn, Gr = boot(G)
    R = json.loads(P3B.read_text())['occupancy']
    Em = R['E_model']; Emc = R['E_model_relMC']; Preal = R['P_real']
    C05 = R['C_R05']; C04 = R['C_R04']
    pred_obs = {c: R['predictions'][c]['const'] for c in ('R04', 'R05', 'R06', 'R04x2S>=3', 'R05x2S>=3', 'R06x2S>=3')}
    lnr04 = pred_obs['R04']['ln_r']
    # model ratios B_model(r)/B_model(R04) (frozen p3-b outputs), s = 0 and s = 3 families
    Bm = {'R04': Preal['R04'], 'R05': Preal['R05'], 'R06': C05 * Em['R06'],
          'R04x2S>=3': Preal['R04x2S>=3'], 'R05x2S>=3': Preal['R05x2S>=3'], 'R06x2S>=3': C05 * Em['R06x2S>=3']}
    res = dict(method='outputs/p3f/CAUSE_METHOD_jorunn.md', files=len(fs), trials=ntr, events=nev, planes_per_trial=M,
               meta=meta)
    # (i) fixed-ribbon occupancy, C(R06)
    i = {c: k for k, c in enumerate(RLN)}
    m_i = {}
    for c in RLN:
        k = i[c]
        m_i[c] = dict(P_fix=float(Pn[0, k]), P_fix_count=float(cnt[:, 0, COLI[c]].sum()),
                      P_refit=float(Pn[1, k]), P_refit_count=float(cnt[:, 1, COLI[c]].sum()),
                      G_fix=float(Gn[0, k]), G_refit=float(Gn[1, k]),
                      sd_ln_G_fix=float(np.std(np.log(Gr[:, 0, k]), ddof=1)) if Gn[0, k] > 0 else None,
                      sd_ln_G_refit=float(np.std(np.log(Gr[:, 1, k]), ddof=1)) if Gn[1, k] > 0 else None)
    res['per_rung'] = m_i
    k6, k5, k4 = i['R06'], i['R05'], i['R04']
    C06 = Pn[0, k6] / Em['R06']
    lnC = np.log(Pr[:, 0, k6] / Em['R06'])
    res['measurement_i'] = dict(C_R06=float(C06), sd_ln_C_R06=float(np.sqrt(np.var(lnC, ddof=1) + Emc['R06'] ** 2)),
                                C_R05_new=float(Pn[0, k5] / Em['R05']), C_R04_new=float(Pn[0, k4] / Em['R04']),
                                C_R05_p3b=C05, C_R04_p3b=C04,
                                D3_ln_C05_over_C06=float(np.log(C05 / C06)),
                                sd_D3=float(np.sqrt(np.var(lnC, ddof=1) + Emc['R06'] ** 2)),
                                n_R06_fixed=float(cnt[:, 0, 2].sum()))
    # predictions and the criterion
    crit = {}
    for fam, (r4, rr) in {'s0': ('R04', ('R05', 'R06')), 's3': ('R04x2S>=3', ('R05x2S>=3', 'R06x2S>=3'))}.items():
        for mp, name in ((1, 'M_G_refit'), (0, 'D1_fixed')):
            out = {}
            for r in rr:
                lnG = np.log(Gn[mp, i[r]] / Gn[mp, i[r4]])
                lnGr = np.log(Gr[:, mp, i[r]] / Gr[:, mp, i[r4]])
                sG = float(np.std(lnGr[np.isfinite(lnGr)], ddof=1))
                lnr4 = pred_obs[r4]['ln_r']
                pred = lnr4 + np.log(Bm[r] / Bm[r4]) - lnG
                obs = pred_obs[r]['ln_r']; so = pred_obs[r]['sigma_tot']
                sc = float(np.hypot(sG, so))
                a_ = bool(np.sign(pred) == np.sign(obs)); b_ = bool(abs(pred - obs) <= 2 * sc); c_ = bool(abs(pred) >= 2 * sG)
                # D2: per-configuration refit transfer (no distinct counting)
                d2 = float(np.log(Pn[1, i[r]] / Pn[1, i[r4]]) - np.log(Pn[0, i[r]] / Pn[0, i[r4]]))
                out[r] = dict(ln_r_pred=float(pred), sigma_G=sG, ln_r_obs=obs, sigma_tot_obs=so, sigma_comb=sc,
                              diff=float(pred - obs), pull=float((pred - obs) / sc), a_sign=a_, b_within_2sigma=b_,
                              c_nonzero_2sigma=c_, ln_G_ratio=float(lnG), ln_model_ratio=float(np.log(Bm[r] / Bm[r4])),
                              D2_refit_transfer=d2)
            if name == 'M_G_refit':
                ok = all(out[r]['a_sign'] and out[r]['b_within_2sigma'] and out[r]['c_nonzero_2sigma'] for r in rr)
                nok = sum(out[r]['a_sign'] and out[r]['b_within_2sigma'] and out[r]['c_nonzero_2sigma'] for r in rr)
                prec = out[rr[1]]['sigma_G'] <= 0.12
                verdict = ('CAUSE FOUND' if ok and prec else
                           'CAUSE NOT FOUND (insufficient precision)' if not prec else
                           'CAUSE NOT FOUND (partial)' if nok == 1 else 'CAUSE NOT FOUND')
                out['verdict'] = verdict if fam == 's0' else verdict + ' [s = 3 family: diagnostic only]'
            crit[f'{fam}_{name}'] = out
    res['criterion'] = crit
    res['verdict'] = crit['s0_M_G_refit']['verdict']
    res['D4_G_refit_R04_vs_direct_R04'] = dict(G_refit_R04=float(Gn[1, k4]), B_dir_R04=170.8564375,
                                               ln_ratio=float(np.log(Gn[1, k4] / 170.8564375)),
                                               G_fix_R04=float(Gn[0, k4]))
    nd = np.concatenate(ndbl)
    res['sampler'] = dict(records=nrec.tolist(), edge_flagged=nedge.tolist(),
                          edge_share_of_HT_weight={m: (edge_w[k] / np.maximum(all_w[k], 1e-300)).tolist()
                                                   for k, m in ((0, 'fixed'), (1, 'refit'))},
                          mean_doublings=float(nd.mean()), max_doublings=int(nd.max()))
    # implied ratio rho(r) (only reported; the redesign is written only if CAUSE FOUND)
    res['rho_measured'] = {c: float((Gn[1, i[c]] / Pn[0, i[c]]) / (Gn[1, k4] / Pn[0, k4])) for c in ('R05', 'R06')}
    res['rho_measured_s3'] = {c: float((Gn[1, i[c]] / Pn[0, i[c]]) / (Gn[1, i['R04x2S>=3']] / Pn[0, i['R04x2S>=3']]))
                              for c in ('R05x2S>=3', 'R06x2S>=3')}
    (OUT / a.out).write_text(json.dumps(res, indent=1, default=float))
    log.info('verdict: %s', res['verdict'])
    for r in ('R05', 'R06'):
        o = crit['s0_M_G_refit'][r]
        log.info('%s: pred %+.3f +- %.3f  obs %+.3f +- %.3f  pull %+.2f  (fixed-map D1 %+.3f, D2 %+.3f)', r,
                 o['ln_r_pred'], o['sigma_G'], o['ln_r_obs'], o['sigma_tot_obs'], o['pull'],
                 crit['s0_D1_fixed'][r]['ln_r_pred'], o['D2_refit_transfer'])
    log.info('C(R06) = %.3f (ln C05/C06 = %+.3f +- %.3f)', C06, res['measurement_i']['D3_ln_C05_over_C06'],
             res['measurement_i']['sd_D3'])


if __name__ == '__main__':
    main()
