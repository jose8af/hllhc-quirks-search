"""sindre_recount.py -- independent recount of the p3-a job outputs (Sindre, reviewer, 2026-11-24).
Does not import any p3a script. Columns addressed by NAME. Read-only. Usage: python -I sindre_recount.py out.json"""
import glob, json, sys, collections
import numpy as np
D = '/nfs/cajuela/jdochoa/quirks_v2/data/p3a/'
W = ['R04n', 'R04w', 'R05', 'R06', 'R07', 'R08']
KMAX = {0: 3, 3: 5}
def load(pat):
    rows = []; seen = collections.Counter(); z_ = collections.defaultdict(float); M = collections.defaultdict(int)
    wmax = 0.0; ic = None; nfile = collections.Counter(); cfg = set(); opt = set()
    for f in sorted(glob.glob(pat)):
        z = np.load(f); m = json.loads(str(z['meta']))
        ic = m['i_cols']; fc = m['f_cols']
        cfg.add(json.dumps(m['config'], sort_keys=True)); opt.add(json.dumps(m['options'], sort_keys=True))
        ri = z['rows_i']; rf = z['rows_f']
        for fi, fm in enumerate(m['files']):
            seen[fm['path']] += 1; nfile[fm['stream']] += 1
            assert fm['n_classified_range'] == fm['n_events']
            if fm['stream'] == 'pilot.hs0.znn':
                for k in ('n_events', 'n_full', 'n_low', 'n_zero', 'sum_w_full', 'sum_w_low', 'n_used'):
                    z_[k] += fm[k]
                wmax = max(wmax, fm['w_max'])
            else:
                M[fm['stream']] += fm['n_events']
        for i in range(len(ri)):
            fm = m['files'][int(ri[i, 0])]
            d = dict(zip(ic, ri[i].tolist())); d['w'] = float(rf[i, fc.index('w')]); d['stream'] = fm['stream']; d['path'] = fm['path']
            rows.append(d)
    return rows, seen, dict(z_), dict(M), wmax, nfile, cfg, opt
def kread(d, reading, w, s, r):
    kb = d[f'kb_{w}_s{s}_{r}']; c = [d[f'k_c{j}_{w}_s{s}_{r}'] for j in range(5)]
    return {'BASE': kb, 'PLANS4': min(c[0], c[3]), 'OWN': min(c[1:]), 'HARD': c[4], 'UNION': min(c + [kb])}[reading]
out = {}
for lab, pat in (('m', '*.m.npz'), ('u', '*.u.npz'), ('pv0', '*.pv0.npz'), ('pv2', '*.pv2.npz')):
    rows = []; seen = collections.Counter(); Z = {}; M = {}; wmax = 0; nf = collections.Counter(); cfg = set(); opt = set()
    for camp in ('p3-a-clsxz', 'p3-a-clsxb'):
        r, s_, z_, M_, wm, nf_, c_, o_ = load(D + camp + '/000/' + pat)
        rows += r; seen.update(s_); M.update(M_); nf.update(nf_); cfg |= c_; opt |= o_
        if z_: Z = z_; wmax = wm
    o = dict(n_rows=len(rows), n_pilot_files=len(seen), max_times_seen=max(seen.values()) if seen else 0, files_per_stream=dict(nf),
             Z=Z, w_max=wmax, M_Z=(Z['sum_w_full'] / wmax if Z else None), M=M, n_config=len(cfg), options=sorted(opt), config=sorted(cfg)[:1])
    keys = collections.Counter((d['path'], d['event'], d['orient']) for d in rows)
    o['dup_row_keys'] = sum(1 for v in keys.values() if v > 1)
    zr = [d for d in rows if d['stream'] == 'pilot.hs0.znn']
    o['Z_rows'] = len(zr); o['Z_rows_w0'] = sum(d['w'] == 0 for d in zr); o['Z_orient_values'] = sorted(set(d['orient'] for d in zr))
    o['Z_w_between'] = sum(0.05 < d['w'] < 0.5 or 0 < d['w'] < 0.05 for d in zr)
    o['Z_w_values_low'] = sorted(set(round(d['w'], 4) for d in zr if d['w'] < 0.5))[:10]
    o['Z_w_min_full'] = min((d['w'] for d in zr if d['w'] >= 0.5), default=None)
    t = {}
    for rd in ('BASE', 'PLANS4', 'OWN', 'HARD', 'UNION'):
        for w in W:
            for s in (0, 3):
                for r in 'SF':
                    ok = [d for d in rows if kread(d, rd, w, s, r) <= KMAX[s]]
                    c = collections.Counter(('Z' if d['w'] >= 0.5 else 'Zlow' if d['w'] > 0 else 'Zzero') if d['stream'] == 'pilot.hs0.znn' else d['stream'] for d in ok)
                    t[f'{rd}_{r}_{w}_s{s}'] = dict(c)
                    if rd == 'BASE' and s == 0 and r == 'S':
                        o.setdefault('by_k', {})[w] = dict(collections.Counter(kread(d, rd, w, s, r) for d in ok if d['stream'] == 'pilot.hs0.znn' and d['w'] >= 0.5))
                        o.setdefault('wsum', {})[w] = sum(d['w'] for d in ok if d['stream'] == 'pilot.hs0.znn' and d['w'] >= 0.5)
    o['tables'] = t
    o['nonZ_rows'] = [{k: v for k, v in d.items() if k in ('path', 'event', 'orient', 'cls', 'n_early_prod', 'stream') or k.startswith('kb_') or k.startswith('wit_')} for d in rows if d['stream'] != 'pilot.hs0.znn']
    o['flagged_rows_any'] = sum(d['n_early_prod'] > 0 for d in rows)
    # events counted more than once over orientations (non-Z)
    out[lab] = o
json.dump(out, open(sys.argv[1], 'w'), indent=1)
