"""p2c_validate.py -- hand-over validation on a slice of B1 events (STR §4.4 pt 2; risk "hand-over of the parent's hits").

  <acts python> p2c_validate.py <out.json> <b1 npz> [...]

Checks per file (no rung, no candidate, no selection quantity is formed):
 1. integrity: V4-1 closure, no NaN, hit offsets consistent, event seeds distinct;
 2. truncation: no written hit of the parent (vsec = 0, generation 0) beyond the vertex radius (v1 Truncate), and the
    number of parent hits kept that are LATER than the Geant4 vertex time (a parent that curls back, plan O11);
 3. products: no hit of a product (vsec >= 1) earlier than the vertex time; fraction of events with product hits;
 4. momentum balance at the vertex for decays: |sum p(products) - p(parent)| / p(parent) from the Geant4 record;
 5. variant A against variant B on the first 100 events with a charged parent: for every counting surface crossed
    before the vertex, distance in r-phi and z between the Fatras parent hit (truth position) and the first Geant4
    crossing of the same surface; and the number of surfaces crossed by one and not by the other.
"""
import json
import sys
from pathlib import Path

import numpy as np

import p2c_common as C

log = C.setup_logging('p2c_validate')
SURF = json.loads((C.QV2 / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
SID_NAME = {i: s['name'] for i, s in enumerate(SURF)}


def q(a, ps=(0.5, 0.9, 0.99)):
    a = np.asarray(a, float)
    return [float(np.quantile(a, p)) for p in ps] if len(a) else None


def one(path):
    z, m = C.load_job(path)
    H = z['hits']; ho = z['hit_off']; T = z['tru']; ev = z['evt']; G = z['gvtx']; vc = m['vcols']
    gc = z['gcross']; gco = z['gcross_off']; gp = z['gprod']; gpo = z['gprod_off']
    n = len(ev)
    code_name = {v: k for k, v in m['surface_names'].items()}
    col = {k: i for i, k in enumerate(m['columns'])}
    res = dict(file=str(path), term=m['term'], n_events=n, v41_pass=m['v41_pass'], nan_hits=int(np.isnan(H).sum()),
               offsets_ok=bool(ho[0] == 0 and ho[-1] == len(H) and np.all(np.diff(ho) >= 0)),
               seeds_distinct=bool(len(np.unique(ev[:, -2] + ev[:, -1] * 2.0 ** 31)) == n),
               hits_per_event=float(len(H) / n), ckf_tracks_per_event=float(z['v41'][:, 10].mean()),
               events_without_hits=int(np.sum(np.diff(ho) == 0)), sha_hits=C.hashlib.sha256(H.tobytes()).hexdigest()[:16])
    late_parent = 0; beyond = 0; early_prod = 0; with_prod_hits = 0; n_parent_hits = 0; n_prod_hits = 0
    dbal = []; drphi = []; dz = []; only_f = 0; only_g = 0; both = 0; ncmp = 0
    for i in range(n):
        h = H[ho[i]:ho[i + 1]].astype(float); t = T[ho[i]:ho[i + 1]].astype(float)
        g = dict(zip(vc, G[i]))
        rv = np.hypot(g['x'], g['y'])
        par = (h[:, col['vsec']] == 0) & (h[:, col['gen']] == 0) & (h[:, col['particle']] == 1)
        btl = np.array([SID_NAME[int(s)] == 'BTL' for s in h[:, col['sid']]], bool)
        rt = np.hypot(t[:, 0], t[:, 1])
        n_parent_hits += int(par.sum())
        beyond += int(np.sum(par & (rt > rv + 1e-3)))
        late_parent += int(np.sum(par & ~btl & (h[:, col['t']] > g['t'] + 0.010)))
        pr = h[:, col['vsec']] >= 1
        n_prod_hits += int(pr.sum())
        with_prod_hits += int(pr.any())
        early_prod += int(np.sum(pr & ~btl & (h[:, col['t']] < g['t'] - 0.010)))
        P = gp[gpo[i]:gpo[i + 1]].astype(float)
        pp = np.array([g['px'], g['py'], g['pz']])
        if m['term'] == 'dif' and len(P) and np.linalg.norm(pp) > 0:
            dbal.append(float(np.linalg.norm(P[:, 1:4].sum(0) - pp) / np.linalg.norm(pp)))
        if ncmp < 100 and ev[i, 8] > 0:          # charged parent: variant A against variant B
            ncmp += 1
            X = gc[gco[i]:gco[i + 1]].astype(float)
            first = {}
            for r in X:
                first.setdefault(code_name[int(r[0])], r)
            fat = {}
            for k in np.nonzero(par & ~btl)[0]:
                fat.setdefault(SID_NAME[int(h[k, col['sid']])], (t[k], h[k, col['t']]))
            for nm in set(first) | set(fat):
                if nm == 'BTL' or SURF[[s['name'] for s in SURF].index(nm)]['type'] != 0:
                    continue
                if nm in first and nm in fat:
                    both += 1
                    a = fat[nm][0]; b = first[nm][1:4]
                    ra = np.hypot(a[0], a[1])
                    dph = (np.arctan2(a[1], a[0]) - np.arctan2(b[1], b[0]) + np.pi) % (2 * np.pi) - np.pi
                    drphi.append(float(ra * dph)); dz.append(float(a[2] - b[2]))
                elif nm in fat:
                    only_f += 1
                else:
                    only_g += 1
    res.update(parent_hits=n_parent_hits, parent_hits_beyond_vertex_radius=beyond,
               parent_hits_later_than_vertex_time=late_parent, product_hits_earlier_than_vertex=early_prod,
               frac_events_with_product_hits=with_prod_hits / n, product_hits=n_prod_hits,
               product_handover=m.get('handover'), mean_injected=m.get('mean_injected'),
               mean_injected_slow=m.get('mean_injected_slow'),
               decay_momentum_imbalance_q50_q90_q99=q(dbal),
               ab_events=ncmp, ab_surfaces_both=both, ab_only_fatras=only_f, ab_only_geant4=only_g,
               ab_abs_drphi_mm_q50_q90_q99=q(np.abs(drphi)), ab_abs_dz_mm_q50_q90_q99=q(np.abs(dz)),
               ab_drphi_mean_mm=float(np.mean(drphi)) if drphi else None)
    return res


def main(out, files):
    res = [one(f) for f in files]
    ok = all(r['v41_pass'] and r['nan_hits'] == 0 and r['offsets_ok'] and r['seeds_distinct']
             and r['parent_hits_beyond_vertex_radius'] == 0 and r['product_hits_earlier_than_vertex'] == 0 for r in res)
    distinct = len({r['sha_hits'] for r in res}) == len(res)
    Path(out + '.tmp').write_text(json.dumps(dict(all_hard_checks_pass=bool(ok), outputs_not_identical=distinct, files=res),
                                             indent=1))
    Path(out + '.tmp').replace(out)
    for r in res:
        log.info('%s', json.dumps({k: r[k] for k in r if k != 'file'}))
    log.info('hard checks pass: %s; outputs distinct: %s', ok, distinct)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
