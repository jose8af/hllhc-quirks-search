"""Reviewer Dorte (critical review of p3-b, 2026-11-24): independent re-derivation of key B2 development numbers.

Read-only on the p3-b and C1 outputs; writes one JSON next to this script.  Run on maxwell, nice 19, 1 process:
  envs/tt/.pixi/envs/default/bin/python -I phase3_selection/review/critical/dorte_rederive.py [ntrials] [K]
A. aggregation of p3-b-thin / p3-b-direct outputs: trial uniqueness (double counting), rates, ln r, r.m.s.;
B. direct counts recomputed from the raw C1 pu1 trial rows (trials.n_grp), independent of direct_job.py;
C. thinning re-implemented here in plain numpy/python (own grouping with python sets, own counting and w_core) on the
   first `ntrials` C1 pu2 trials with K own draws; q = 1 identity against the stored rho = 2 n_grp; q = 1/2 rates
   compared with the p3-b-thin K = 64 means of the same trials.
"""
import glob
import json
import logging
import sys
import time
from pathlib import Path

import numpy as np

QV2 = Path('/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2')
sys.path.insert(0, str(QV2))
from acts.stage4.finder import finder as FF  # noqa: E402  (geometry tables LC_OF, SIDE_OF only)

D3 = Path('/nfs/cajuela/jdochoa/quirks_v2/data/p3b')
C1 = Path('/nfs/cajuela/jdochoa/quirks_v2/data/phase2')
OUT = Path(__file__).resolve().parent / 'dorte_rederive.json'
log = logging.getLogger('dorte')
WK = (37.5, 18.75, 9.4, 4.7)  # R05..R08 w_core cuts


def part_a():
    res = {}
    for camp, pat in (('p3-b-thin', 'thin-*.npz'), ('p3-b-direct', 'direct-*.npz')):
        fs = sorted(glob.glob(str(D3 / camp / '*' / pat)))
        G, keys = [], []
        for f in fs:
            d = np.load(f)
            g = d['grp'].astype(float)
            G.append(g.mean(1) if g.ndim == 3 else g)
            keys += [f'{j}|{e}|{r}' for j, e, r in zip(d['job'], d['ev'], d['road'])]
            cols = list(d['cols'])
            if camp == 'p3-b-thin':
                r8 = cols.index('R08')
                res.setdefault('thin_R08_subset_groups_total', 0)
                res['thin_R08_subset_groups_total'] += int(d['grp'][:, :, r8].sum())
                res.setdefault('thin_R08_subsets_with_pass', 0)
                res['thin_R08_subsets_with_pass'] += int((d['grp'][:, :, r8] > 0).sum())
        G = np.concatenate(G)
        res[camp] = dict(files=len(fs), trials=len(keys), unique_trials=len(set(keys)),
                         events=len({k.rsplit('|', 1)[0] for k in keys}),
                         rate={c: float(G[:, cols.index(c)].mean()) for c in ('R04', 'R05', 'R06', 'R07', 'R08')},
                         count={c: float(G[:, cols.index(c)].sum()) for c in ('R04', 'R05', 'R06', 'R07')})
    t, d = res['p3-b-thin']['rate'], res['p3-b-direct']['rate']
    lr = {c: float(np.log(t[c] / d[c])) for c in ('R04', 'R05', 'R06', 'R07')}
    res['ln_r_thin'] = lr
    res['rms_R04_R06'] = float(np.sqrt(np.mean([lr[c] ** 2 for c in ('R04', 'R05', 'R06')])))
    res['rms_R04_R05'] = float(np.sqrt(np.mean([lr[c] ** 2 for c in ('R04', 'R05')])))
    return res


def part_b():
    fs = sorted(glob.glob(str(C1 / 'p2-a-c1-pu1' / '000' / 'c1pu1-*.npz')))
    fs = [f for f in fs if 'premerge' not in f]
    tot = np.zeros(4); ntr = 0
    for f in fs:
        z = np.load(f)
        ng = z['trials.n_grp'][:, 3:7].astype(float)
        tot += np.maximum(ng, 0).sum(0); ntr += len(ng)
    return dict(files=len(fs), trials=ntr, counts=dict(zip(('R04', 'R05', 'R06', 'R07'), tot.tolist())),
                rate=dict(zip(('R04', 'R05', 'R06', 'R07'), (tot / ntr).tolist())))


def subset_count(t, keep_hit):
    """Own implementation: groups (R04, R05, R06, R07) of one thinned subset; keep_hit bool per union hit."""
    off, ref, sel = t['off'], t['ref'], t['sel']
    LC, SD, U, N2 = t['LC'], t['SD'], t['U'], t['N2']
    passers = []
    for c in sel:
        h = ref[off[c]:off[c + 1]]
        h = h[keep_hit[h]]
        lc, sd = LC[h], SD[h]
        nit2 = nip2 = 0
        for layer in range(7):
            if layer < 4:
                k = int(np.sum((lc == layer) & (sd == 0)))
            else:
                k = min(int(np.sum((lc == layer) & (sd == 1))), int(np.sum((lc == layer) & (sd == 2))))
            if k >= 2:
                nip2 += 1
                nit2 += layer < 4
        if nit2 < 3 or nip2 < 7:
            continue
        ip = h[lc <= 6]
        w = np.nan
        if len(ip) > 2:
            x = U[ip] @ N2[c]
            w = 1.4826 * np.median(np.abs(x - np.median(x)))
        passers.append((set(h.tolist()), w))
    # greedy grouping, rank order, leader-based, frac 0.5 of the smaller set, first group in creation order
    lsize, gid, inv_idx = [], [], {}
    for s, _ in passers:
        cnt = {}
        for hh in s:
            for L in inv_idx.get(hh, ()):
                cnt[L] = cnt.get(L, 0) + 1
        ok = [L for L, n in cnt.items() if n >= 0.5 * min(len(s), lsize[L])]
        if ok:
            g = min(ok)
        else:
            g = len(lsize)
            lsize.append(len(s))
            for hh in s:
                inv_idx.setdefault(hh, []).append(g)
        gid.append(g)
    out = []
    for r in range(4):
        gs = {g for g, (_, w) in zip(gid, passers) if r == 0 or (np.isfinite(w) and w < WK[r - 1])}
        out.append(len(gs))
    return out


def part_c(ntr, K):
    thin = {}
    for f in sorted(glob.glob(str(D3 / 'p3-b-thin' / '*' / 'thin-*.npz'))):
        d = np.load(f)
        cols = list(d['cols'])
        ix = [cols.index(c) for c in ('R04', 'R05', 'R06', 'R07')]
        for i, (j, e, r) in enumerate(zip(d['job'], d['ev'], d['road'])):
            thin[f'{j}|{e}|{r}'] = d['grp'][i][:, ix].mean(0)
    rng = np.random.default_rng(20261124)
    own, theirs, ident = [], [], []
    done = 0
    for jf in sorted(glob.glob(str(C1 / 'p2-a-c1-pu2' / '000' / 'c1pu2-*.premerge.npz'))):
        jid = Path(jf).name.split('.')[0]
        z = np.load(jf)
        m = np.load(str(jf).replace('.premerge', ''))
        for t in range(len(m['trials.ev'])):
            if done >= ntr:
                break
            p = f't{t}/'
            xyz = z[p + 'h_xyz'].astype(float)
            pv = m['trials.pv'][t].astype(float)
            nrm = z[p + 'normal'].astype(float); axs = z[p + 'axis'].astype(float)
            sid = z[p + 'h_sid'].astype(int)
            al = z[p + 'aligned'].astype(bool)
            sel = np.where(al & (z[p + 'v_nit2'] >= 3) & (z[p + 'v_nip2'] >= 7))[0]
            T = dict(off=z[p + 'off'].astype(int), ref=z[p + 'ref'].astype(int), sel=sel, LC=FF.LC_OF[sid],
                     SD=FF.SIDE_OF[sid], U=xyz - pv[None, :], N2=np.cross(nrm, axs))
            INT = z[p + 'h_INT']
            uI, inv = np.unique(INT, return_inverse=True)
            t0 = time.time()
            q1 = subset_count(T, np.ones(len(xyz), bool))
            ident.append(dict(trial=f'{jid}|{t}', own_q1=q1, stored=m['trials.n_grp'][t, 3:7].tolist()))
            cs = []
            for _ in range(K):
                keepI = rng.random(len(uI)) < 0.5
                cs.append(subset_count(T, keepI[inv]))
            own.append(np.mean(cs, 0))
            key = f'{jid}|{int(m["trials.ev"][t])}|{int(m["trials.road"][t])}'
            theirs.append(thin[key])
            log.info('%s t%d: q=1 own %s stored %s; own q=1/2 mean %s; p3-b %s (%.0f s)', jid, t, q1,
                     m['trials.n_grp'][t, 3:7].tolist(), np.round(own[-1], 2).tolist(), np.round(thin[key], 2).tolist(),
                     time.time() - t0)
            done += 1
        if done >= ntr:
            break
    own = np.array(own); theirs = np.array(theirs)
    return dict(trials=done, K_own=K, identity=ident, own_rate=own.mean(0).tolist(), p3b_rate_same_trials=theirs.mean(0).tolist(),
                ratio_own_over_p3b=(own.mean(0) / theirs.mean(0)).tolist(),
                sd_trial_ratio_R04=float(np.std(own[:, 0] / theirs[:, 0], ddof=1) / np.sqrt(done)))


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    ntr = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    R = dict(A=part_a())
    log.info('A %s', json.dumps(R['A']))
    R['B'] = part_b()
    log.info('B %s', json.dumps(R['B']))
    OUT.write_text(json.dumps(R, indent=1))
    R['C'] = part_c(ntr, K)
    log.info('C %s', json.dumps({k: v for k, v in R['C'].items() if k != 'identity'}))
    OUT.write_text(json.dumps(R, indent=1))


if __name__ == '__main__':
    main()
