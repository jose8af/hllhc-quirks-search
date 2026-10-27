"""val_trgs_stats.py -- weight-structure numbers quoted in the prose (review S2-R2 C-3), so that val_headlines.py and the
documents read them from JSON instead of hard-coding them.  Read-only on the samples.

Per stitched TRGS file (17):
  w_ratio_inc_trg   <w_INC>/<w_TRG> over rows with w > 0 (as the SAMPLES.md column)
  inc_event_share   fraction of the tail rows (w != 0, pT(QQ) > 200) that come from INC   (as SAMPLES.md)
  inc_sigma_share   INC share of sum w in the tail (w != 0, pT > 200, |eta| < 2.5)         (as SAMPLES.md)
  unweight_eff_tail fraction of tail rows (w > 0, pT > 200, |eta| < 2.5) kept by mg_events.unweight_mask (seed 12345)
  unweight_eff_all  same over all rows with w > 0
From results/samples.json (matched = MLM files, xqcut set): w0_frac = 1 - n_w_nonzero / n_kept.
Template/toy agreement (review S2-R2 C-7): weighted median of x = 2(gamma* - 1) in the template and toy halves of each TRGS
file, with the selection of val_loader.py (iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200, split=...)); error of each
median from 300 bootstrap resamples of that half (seed 11); pull = (med_toy - med_template) / sqrt(err_t^2 + err_y^2).
Run: pixi run -e ana python scripts/val_trgs_stats.py   -> results/trgs_stats.json"""
import json
import os
import sys

import numpy as np
from scipy.stats import chi2 as chi2dist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vlib import DATA, RES   # noqa
import mg_events as M   # noqa

PTS = [('E', m) for m in range(200, 1600, 100)] + [('S', m) for m in (200, 500, 1000)]


def mm(d, k):
    v = [r[k] for r in d.values()]
    ka = min(d, key=lambda p: d[p][k]); kb = max(d, key=lambda p: d[p][k])
    return dict(min=min(v), max=max(v), argmin=ka, argmax=kb)


def wmed(x, w):
    i = np.argsort(x); c = np.cumsum(w[i]); return float(x[i][np.searchsorted(c, c[-1] / 2)])


def template_toy(pre, m, rng, nboot=300):
    spin = 'F' if pre == 'E' else 'S'
    out = {}
    for sp in ('template', 'toy'):
        ev = [(e[2]['w'], 2 * (e[2]['gstar'] - 1)) for e in M.iter_events(m, 'trig', spin, eta_max=2.5, ptmin=200, split=sp)]
        w = np.array([a[0] for a in ev]); x = np.array([a[1] for a in ev])
        bs = [(lambda ix: wmed(x[ix], w[ix]))(rng.integers(0, len(w), len(w))) for _ in range(nboot)]
        out[sp] = dict(n=len(w), x_median=wmed(x, w), x_median_err=float(np.std(bs)))
    t, y = out['template'], out['toy']
    out['rel_diff_toy_vs_template'] = y['x_median'] / t['x_median'] - 1
    out['pull'] = (y['x_median'] - t['x_median']) / float(np.hypot(t['x_median_err'], y['x_median_err']))
    return out


def main():
    files = {}
    rng = np.random.default_rng(11)
    tt = {}
    for pre, m in PTS:
        c = dict(np.load(os.path.join(DATA, 'npz', f'{pre}-TRGS_m{m}.npz'), allow_pickle=False))
        w = c['w']; o = c['origin']
        tail = (w != 0) & (c['pt_pair'] > 200)
        te = tail & (np.abs(c['eta_pair']) < 2.5)
        acc, _ = M.unweight_mask(c, 12345)
        tp = te & (w > 0)
        files[f'{pre}_{m}'] = dict(
            w_ratio_inc_trg=float(w[(w > 0) & (o == 1)].mean() / w[(w > 0) & (o == 0)].mean()),
            inc_event_share=float((tail & (o == 1)).sum() / tail.sum()),
            inc_sigma_share=float(w[te & (o == 1)].sum() / w[te].sum()),
            unweight_eff_tail=float(acc[tp].sum() / tp.sum()),
            unweight_eff_all=float(acc[w > 0].sum() / (w > 0).sum()))
        tt[f'{pre}_{m}'] = template_toy(pre, m, rng)
    S = json.load(open(os.path.join(RES, 'samples.json')))
    w0 = {f"{r['id']}_m{r['m']}": 1 - r['n_w_nonzero'] / r['n_kept'] for r in S['rows'] if r.get('done') and r.get('xqcut')}
    ka = min(w0, key=w0.get); kb = max(w0, key=w0.get)
    R = dict(note='weight structure of the stitched TRGS files and w = 0 fraction of the matched files (review S2-R2 C-3); '
                  'computed from the npz / samples.json, no uncertainty attached',
             trgs=files,
             ranges={k: mm(files, k) for k in ('w_ratio_inc_trg', 'inc_event_share', 'inc_sigma_share', 'unweight_eff_tail',
                                               'unweight_eff_all')},
             w0_frac_matched=dict(n_files=len(w0), min=w0[ka], max=w0[kb], argmin=ka, argmax=kb),
             template_toy=dict(points=tt, max_abs_pull=max(abs(v['pull']) for v in tt.values()),
                               chi2=float(sum(v['pull'] ** 2 for v in tt.values())), ndf=len(tt),
                               chi2_pvalue=float(chi2dist.sf(sum(v['pull'] ** 2 for v in tt.values()), len(tt))),
                               argmax_abs_pull=max(tt, key=lambda p: abs(tt[p]['pull'])),
                               loader_points={p: tt[p] for p in ('E_200', 'E_500', 'E_1000', 'S_500')}))
    json.dump(R, open(os.path.join(RES, 'trgs_stats.json'), 'w'), indent=1)
    for k, v in R['ranges'].items():
        print(f"{k}: {v['min']:.4f} ({v['argmin']}) .. {v['max']:.4f} ({v['argmax']})")
    print('w0_frac_matched:', R['w0_frac_matched'])
    print('template/toy: max|pull| %.2f (%s), chi2/ndf = %.1f/%d, p = %.2f' % (R['template_toy']['max_abs_pull'],
          R['template_toy']['argmax_abs_pull'], R['template_toy']['chi2'], R['template_toy']['ndf'], R['template_toy']['chi2_pvalue']))
    for p, v in tt.items():
        print(f"{p}: template {v['template']['x_median']:.4f}+-{v['template']['x_median_err']:.4f} (n={v['template']['n']}) "
              f"toy {v['toy']['x_median']:.4f}+-{v['toy']['x_median_err']:.4f} (n={v['toy']['n']}) rel {100 * v['rel_diff_toy_vs_template']:+.2f} % "
              f"pull {v['pull']:+.2f}")


if __name__ == '__main__':
    main()
