"""INV_A2FC_E500 step 3: per-point paired summary of the event-level JSONs (inv_a2fc_e500_events_*.json).
For rows where both A2 and A2FC have a matched f_CKF<0.2 candidate passing R04: the R04 candidate with the smallest
w_core in each; paired medians of w_core, quirk-only IT+PS width, PU hits in core, p_chi2core; bookkeeping equality.
-> data/acts_stage4/investigation/inv_a2fc_e500_summary.json"""
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
D = TT / 'data/acts_stage4/investigation'
PTS = ['F200_L3', 'F200_L5', 'F500_L3', 'F500_L5', 'F1000_L3', 'F1000_L5', 'F1500_L3', 'F1500_L5', 'S500_L5']


def pick(ms):
    c = [x for x in ms if 3 in x['F']]
    return min(c, key=lambda x: x['w_core']) if c else None


def main():
    out = {}
    for p in PTS:
        d = json.loads((D / f'inv_a2fc_e500_events_{p}.json').read_text())
        R = d['rows']
        bk = dict(n_rows=len(R), n_missing=sum(1 for r in R.values() if r['a2'] is None or r['fc'] is None))
        ok = [r for r in R.values() if r['a2'] and r['fc']]
        bk['nqw_equal'] = all(r['a2']['n_q_written'] == r['fc']['n_q_written'] for r in ok)
        bk['status_equal'] = all(r['a2']['status'] == r['fc']['status'] for r in ok)
        bk['probe_equal'] = all(r['a2']['probe_excluded'] == r['fc']['probe_excluded'] for r in ok)
        bk['pv_equal'] = all(r['a2']['pv'] == r['fc']['pv'] for r in ok if r['a2']['pv'] and r['fc']['pv'])
        bk['frac_rows_nqckf_gt0_fc'] = float(np.mean([r['fc']['n_q_ckf'] > 0 for r in ok]))
        bk['mean_fq_ckf_fc'] = float(np.mean([r['fc']['n_q_ckf'] / max(r['fc']['n_q_written'], 1) for r in ok]))
        pairs = [(pick(r['a2']['matched']), pick(r['fc']['matched'])) for r in ok]
        pairs = [(a, f) for a, f in pairs if a and f]
        st = dict(n_pairs=len(pairs))
        for k in ('w_core', 'w_q_ip', 'n_pu_core', 'n_pu_ip', 'n_q_core', 'n_q_ip', 'p_chi2core'):
            a = np.array([x[0][k] if x[0][k] is not None else np.nan for x in pairs], float)
            f = np.array([x[1][k] if x[1][k] is not None else np.nan for x in pairs], float)
            st[k] = dict(med_a2=float(np.nanmedian(a)), med_fc=float(np.nanmedian(f)),
                         med_ratio=float(np.nanmedian(f / a)) if k.startswith('w') else None,
                         med_diff=float(np.nanmedian(f - a)), frac_fc_gt_a2=float(np.nanmean(f > a)))
        # fraction of R04 pairs whose FC w_core exceeds 4.7 while A2 is below
        st['n_a2_w_lt4.7'] = int(sum(a['w_core'] < 4.7 for a, f in pairs))
        st['n_fc_w_lt4.7'] = int(sum(f['w_core'] < 4.7 for a, f in pairs))
        st['n_a2_p_gt0.05'] = int(sum(a['p_chi2core'] > 0.05 for a, f in pairs))
        st['n_fc_p_gt0.05'] = int(sum(f['p_chi2core'] > 0.05 for a, f in pairs))
        out[p] = dict(bookkeeping=bk, paired=st)
        print(p, bk)
        print('   n', st['n_pairs'], ' '.join(f"{k}: {st[k]['med_a2']:.3g}->{st[k]['med_fc']:.3g} (fc>a2 {st[k]['frac_fc_gt_a2']:.2f})"
                                      for k in ('w_core', 'w_q_ip', 'n_pu_core', 'n_pu_ip', 'p_chi2core')),
              ' w<4.7', st['n_a2_w_lt4.7'], '->', st['n_fc_w_lt4.7'], ' p>.05', st['n_a2_p_gt0.05'], '->',
              st['n_fc_p_gt0.05'])
    (D / 'inv_a2fc_e500_summary.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
