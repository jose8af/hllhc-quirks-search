"""B3 check of the occupancy model's importance sampling (IS) at R07/R08 (p3-b review cycle 1, fixer Ivar).

Diagnostic only: it changes no input, no definition and no number of the frozen model (occ_model / occmod_job).
Reads the 8 p3-b-occmod outputs (stage-B configurations, per-configuration IS sums isr[b, k, (m1, m2, npass)] and plain
pass fractions) and

  --mode stats : error of E_model(R0k) | R04 from (i) the spread of the 8 seeds and (ii) the within-seed spread of the
                 per-configuration IS means (the configurations are iid draws, so var_b(m1)/nB contains both the
                 configuration and the toy noise); weight concentration (share of the top 1 % of configurations); IS
                 effective sample sizes.  Writes outputs/p3b/is_check_stats.json.
  --mode strat : stratified check on the configurations that carry the R08 IS sum: for the top-N stage-B
                 configurations (ranked by their stored R08 IS mean) it rebuilds the units with the same densities and
                 runs (a) plain toys (unbiased, no IS) and (b) fresh IS toys with new seeds (the stored ranking selects
                 upward fluctuations of the stored IS; a fresh IS run on the same stratum is not selected).  Writes
                 $QV2_OUT_DIR/<id>.npz.
  --mode combine : reads the strat outputs, writes outputs/p3b/is_check.json.
"""
import argparse
import glob
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'outputs' / 'p3b'
DATA = Path(os.environ.get('QV2_DATA', '/nfs/cajuela/jdochoa/quirks_v2/data')) / 'p3b'
log = logging.getLogger('is_check')
RUNGS = ['R05', 'R06', 'R07', 'R08']


def occmod_files():
    return sorted(glob.glob(str(DATA / 'p3-b-occmod' / '*' / 'occmod-*.npz')))


def stats():
    fs = occmod_files()
    seeds = []
    for f in fs:
        d = np.load(f)
        pa = d['pA'].mean()
        isr = d['isr']; nB = isr.shape[0]
        nis = json.loads(str(d['meta_json']))['nis']
        row = {}
        for k, c in enumerate(RUNGS):
            m1 = isr[:, k, 0]; m2 = isr[:, k, 1]; npass = isr[:, k, 2]
            e = pa * m1.mean()
            rel_within = m1.std(ddof=1) / np.sqrt(nB) / m1.mean() if m1.mean() > 0 else np.nan
            srt = np.sort(m1)[::-1]
            top1 = srt[:max(1, nB // 100)].sum() / m1.sum() if m1.sum() > 0 else np.nan
            # toy-level effective sample size of the IS weights: (Σw)²/Σw² over all toys of the seed (passing toys
            # carry w, failing 0), from the per-configuration sums m1 = Σw/nis, m2 = Σw²/nis
            ess = (m1.sum() * nis) ** 2 / (m2.sum() * nis) if m2.sum() > 0 else 0.0
            ess_cfg = m1.sum() ** 2 / (m1 ** 2).sum() if m1.sum() > 0 else 0.0
            plain = d['plain'][:, k]
            row[c] = dict(E=float(e), E_plain=float(pa * plain.mean()), plain_pass_toys=float(plain.sum() * 200),
                          rel_within=float(rel_within), top1pct_share=float(top1), ess_toys=float(ess),
                          ess_configs=float(ess_cfg), is_pass_toys=float(npass.sum()),
                          expected_plain_pass=float(m1.sum() * 200))
        seeds.append(dict(file=os.path.basename(f), nB=int(nB), pA=float(pa), rungs=row))
    res = {}
    for c in RUNGS:
        E = np.array([s['rungs'][c]['E'] for s in seeds])
        rw = np.array([s['rungs'][c]['rel_within'] for s in seeds])
        # pooled within-seed error of the 8-seed mean: sqrt(Σ (E_s rw_s)²)/8 / mean
        rel_pooled = float(np.sqrt(np.sum((E * rw) ** 2)) / len(E) / E.mean())
        # all configurations pooled (8 × nB iid draws, common pA spread neglected: pA has < 1 % error)
        m1all = np.concatenate([np.load(f)['isr'][:, RUNGS.index(c), 0] for f in fs])
        srt = np.sort(m1all)[::-1]
        res[c] = dict(E_mean=float(E.mean()), rel_seed_spread=float(E.std(ddof=1) / np.sqrt(len(E)) / E.mean()),
                      rel_within_pooled=rel_pooled,
                      rel_all_configs=float(m1all.std(ddof=1) / np.sqrt(len(m1all)) / m1all.mean()),
                      top1pct_share_all=float(srt[:len(srt) // 100].sum() / srt.sum()),
                      top10_share_all=float(srt[:10].sum() / srt.sum()),
                      ess_configs_all=float(srt.sum() ** 2 / (srt ** 2).sum()),
                      E_plain_mean=float(np.mean([s['rungs'][c]['E_plain'] for s in seeds])),
                      plain_pass_toys=float(sum(s['rungs'][c]['plain_pass_toys'] for s in seeds)),
                      expected_plain_pass=float(sum(s['rungs'][c]['expected_plain_pass'] for s in seeds)),
                      is_pass_toys=float(sum(s['rungs'][c]['is_pass_toys'] for s in seeds)))
    out = dict(files=[os.path.basename(f) for f in fs], per_seed=seeds, combined=res)
    (OUT / 'is_check_stats.json').write_text(json.dumps(out, indent=1))
    for c in RUNGS:
        log.info('%s %s', c, json.dumps(res[c]))


def strat(a):
    sys.path.insert(0, str(HERE))
    import occ_core as OC  # noqa: E402
    import occ_model as OM  # noqa: E402
    import occmod_job as OJ  # noqa: E402
    from numba import njit

    @njit
    def nb_seed(s):
        np.random.seed(s)

    fs = occmod_files()
    files_in = sorted(glob.glob(str(DATA / 'p3-b-occin' / '*' / 'occin-*.npz')))
    D = OJ.densities(files_in)
    # ranking over all stage-B configurations of the 8 seeds by the stored R08 IS mean
    recs = []
    for fi, f in enumerate(fs):
        d = np.load(f)
        m1 = d['isr'][:, 3, 0]
        for b in np.nonzero(m1 > 0)[0]:
            recs.append((m1[b], fi, int(b)))
    recs.sort(reverse=True)
    if a.all:
        # every stage-B configuration of the 8 seeds in file order (unranked, so no selection effect)
        recs = []
        for fi, f in enumerate(fs):
            m1 = np.load(f)['isr'][:, 3, 0]
            recs += [(m1[b], fi, b) for b in range(len(m1))]
    sel = recs[a.first:a.first + a.ntop]
    nb_seed(a.seed)
    S = np.empty(OM.MAXP); Wt = np.empty(OM.MAXP); off = np.zeros(23, np.int64); lam = np.zeros(22)
    cache = {}
    plain = np.zeros((len(sel), 4)); isr = np.zeros((len(sel), 2, 3)); stored = np.zeros(len(sel))
    t0 = time.time(); tpl = 0.0; tis = 0.0
    for j, (m1, fi, b) in enumerate(sel):
        if fi not in cache:
            d = np.load(fs[fi]); cache[fi] = (d['th'], d['idxB'])
        th, idx = cache[fi]
        i = idx[b]
        pv = th[i, :3]; phimet = th[i, 3]
        n, ax = OC.plane_from(th[i, 4], th[i, 5], th[i, 6])
        OM.config_units(n, ax, pv, phimet, D['R'], D['s0'], D['s1'], D['cdf'], D['cdfp'], False, S, Wt, off, lam)
        no = off[OM.NCAT]
        cw = np.cumsum(Wt[:no])
        ss = np.empty(no); sw = np.empty(no)
        for c in range(OM.NCAT):
            lo, hi = off[c], off[c + 1]
            o = np.argsort(S[lo:hi], kind='stable')
            ss[lo:hi] = S[lo:hi][o]; sw[lo:hi] = Wt[lo:hi][o]
        scw = np.cumsum(sw)
        o4 = np.zeros(4)
        t1 = time.process_time()
        OM.plain_toys(S[:no], cw, off, lam, a.nplain, o4)
        tpl += time.process_time() - t1
        plain[j] = o4
        t1 = time.process_time()
        for kk, k in enumerate((2, 3)):
            r = np.zeros(3)
            if a.nis > 0:
                OM.is_toys(S[:no], cw, off, lam, a.nis, k, 0.5, ss, scw, np.zeros(1, np.int64), r)
            isr[j, kk] = r
        tis += time.process_time() - t1
        stored[j] = m1
        if j % 5 == 0:
            log.info('config %d/%d, %.0f s (plain %.1f s, IS %.1f s CPU)', j, len(sel), time.time() - t0, tpl, tis)
    out = Path(os.environ.get('QV2_OUT_DIR', '.'))
    np.savez_compressed(out / f'{a.id}.npz', plain=plain, isr=isr, stored_m1_R08=stored,
                        sel=np.array([(fi, b) for _, fi, b in sel]), nplain=a.nplain, nis=a.nis, seed=a.seed,
                        first=a.first, n_all=len(recs), cpu_s=time.process_time(), cpu_plain=tpl, cpu_is=tis,
                        all=a.all)


def combine(paths):
    fs = occmod_files()
    m1all = np.concatenate([np.load(f)['isr'][:, 3, 0] for f in fs])
    m1all7 = np.concatenate([np.load(f)['isr'][:, 2, 0] for f in fs])
    tot = m1all.sum()
    pl = []; is7 = []; is8 = []; st = []; sel = []; np_ = None; cpu = 0.0
    for p in paths:
        d = np.load(p)
        pl.append(d['plain']); is7.append(d['isr'][:, 0, 0]); is8.append(d['isr'][:, 1, 0]); st.append(d['stored_m1_R08'])
        sel.append(d['sel']); np_ = int(d['nplain']); nis = int(d['nis']); cpu += float(d['cpu_s'])
    pl = np.concatenate(pl); is7 = np.concatenate(is7); is8 = np.concatenate(is8); st = np.concatenate(st)
    sel = np.concatenate(sel)
    # stored R07 IS means of the same configurations
    st7 = np.array([np.load(fs[fi])['isr'][b, 2, 0] for fi, b in sel])
    k_pass8 = pl[:, 3].sum() * np_
    k_pass7 = pl[:, 2].sum() * np_
    res = dict(n_configs=int(len(st)), n_configs_all=int(len(m1all)), nplain=np_, nis_fresh=nis, cpu_s=cpu,
               stratum_share_of_stored_R08_sum=float(st.sum() / tot),
               R08=dict(stored_IS_sum=float(st.sum()), fresh_IS_sum=float(is8.sum()),
                        plain_sum=float(pl[:, 3].sum()), plain_pass_toys=float(k_pass8),
                        plain_rel_err=float(1 / np.sqrt(k_pass8)) if k_pass8 > 0 else None,
                        fresh_over_stored=float(is8.sum() / st.sum()),
                        plain_over_fresh=float(pl[:, 3].sum() / is8.sum()) if is8.sum() > 0 else None,
                        plain_over_stored=float(pl[:, 3].sum() / st.sum())),
               R07=dict(stored_IS_sum=float(st7.sum()), fresh_IS_sum=float(is7.sum()), plain_sum=float(pl[:, 2].sum()),
                        plain_pass_toys=float(k_pass7),
                        stratum_share_of_stored_R07_sum=float(st7.sum() / m1all7.sum())))
    (OUT / 'is_check.json').write_text(json.dumps(res, indent=1))
    log.info(json.dumps(res, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['stats', 'strat', 'combine'])
    ap.add_argument('--id', default='ischeck-000')
    ap.add_argument('--ntop', type=int, default=64)
    ap.add_argument('--first', type=int, default=0)
    ap.add_argument('--nplain', type=int, default=100000)
    ap.add_argument('--nis', type=int, default=2000)
    ap.add_argument('--seed', type=int, default=777001)
    ap.add_argument('--all', action='store_true')
    ap.add_argument('paths', nargs='*')
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    if a.mode == 'stats':
        stats()
    elif a.mode == 'strat':
        strat(a)
    else:
        combine(a.paths)


if __name__ == '__main__':
    main()
