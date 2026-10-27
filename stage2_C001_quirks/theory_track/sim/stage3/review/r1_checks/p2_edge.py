"""R1 reviewer: independent recomputation of P2 edges (ds_all = 100 um, f(sep_IT < 100 um) = 0.5) from events_p2.npz,
template half (tt_split == 0) in |eta| < 2.5, and the effect of the status != 1 exclusion (status 0 -> +inf thickness /
status 4 -> merged, the extreme assumptions)."""
import json
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[4]
S = np.load(TT / 'data/sim_stage3/summary/events_p2.npz')
meta = json.loads(str(S['point_meta'])); keys = list(S['point_keys'])
P2 = json.load(open(TT / 'sim/stage3/results/P2.json'))


def cross(l, y, y0, logy):
    l = np.log(np.asarray(l)); y = np.asarray(y, float)
    t = (np.log(y) - np.log(y0)) if logy else (y - y0)
    for i in range(len(t) - 1):
        if np.isfinite(t[i]) and np.isfinite(t[i + 1]) and t[i] * t[i + 1] < 0:
            return float(np.exp(l[i] + t[i] / (t[i] - t[i + 1]) * (l[i + 1] - l[i])))
    return np.nan


by = {}
for k in keys:
    m = meta[k]
    if m.get('cfg', 'BM') != 'BM':
        continue
    by.setdefault(f"{m['spin']}_m{int(m['m'])}", {})[float(m['lam'])] = keys.index(k)
tot = dict(st0=0, st4=0)
for pk in sorted(by):
    lams = sorted(by[pk]); ref = by[pk][1.0]
    s1 = (S['point'] == ref) & (S['tt_split'] == 0) & S['in_eta25']
    evs = set(S['ev_index'][s1].tolist())
    ds = {}; fm = {}; ds_inc = {}; fm_inc = {}; nbad = {}
    for l in lams:
        s = (S['point'] == by[pk][l]) & np.isin(S['ev_index'], list(evs))
        st = S['status'][s]; good = st == 1
        d = S['ds_all_um'][s]; sep = S['sep_IT_um'][s]
        ds[l] = np.nanmedian(d[good])
        dd = d.copy(); dd[st == 0] = np.inf; dd[st == 4] = 0.0  # status 0 still in the tracker: assume thick; status 4: thin
        ds_inc[l] = np.median(dd[np.isfinite(dd) | (st == 0)])
        mg = np.where(np.isfinite(sep), sep < 100, False)
        fm[l] = mg[good].mean()
        mi = mg.copy(); mi[st == 4] = True  # status 4: near-threshold, assume merged
        fm_inc[l] = mi[(st == 1) | (st == 4)].mean()
        nbad[l] = (int((st == 0).sum()), int((st == 4).sum()))
        tot['st0'] += nbad[l][0]; tot['st4'] += nbad[l][1]
    e = P2['edges'][pk]
    a = cross(lams, [ds[l] for l in lams], 100, True); b = cross(lams, [ds_inc[l] for l in lams], 100, True)
    c = cross(lams, [fm[l] for l in lams], 0.5, False); d_ = cross(lams, [fm_inc[l] for l in lams], 0.5, False)
    bad = {l: v for l, v in nbad.items() if v != (0, 0)}
    print(f"{pk:8s} n_tmpl={len(evs)} ds100: mine {a:.4f} json {e['lower_ds100_hit']['value']:.4f} incl.st0/4 {b:.4f} "
          f"({100*(b/a-1):+.1f}%) | merge100: mine {c:.3f} json {e['upper_merge100_hit']['value']:.3f} incl.st4 {d_:.3f} "
          f"({100*(d_/c-1):+.1f}%) | bad (st0,st4) {bad}")
print('template-half status 0 / 4 totals:', tot)
