"""G2 PU-only equivalence test: fast finder (acts/stage4/finder) vs the reference (f1r_finder logic, reference.py) on
the same PU-only trials (trials.py).  Signal-blind: no signal hit enters (PU-only events, no signal efficiency).

Compared per trial (reference outputs read from data/acts_stage4/g2/ref/ref_rho<rho>_t<i>.npz):
  1. seeds   : the set of (a, b) seed pairs passing T_seed (must be identical);
  2. cands   : kept candidates (2-mrad merge, N_L2 >= 4), matched by their seed (a, b): same rank order, same hit set,
               identical integer variables, float variables within tolerance;
  3. rungs   : per-rung (F0 ladder of plan §2.5, cumulative, plus each family on the loosest counting rung) number of
               passing candidates, of distinct passing hit sets, and the per-trial pass flag.
Run (theory_track):  nice -n 10 pixi run python -m acts.stage4.finder.test_equivalence <i0> <i1> [rho] [tag]
  -> data/acts_stage4/g2/equivalence_rho<rho>[_tag].json ; exits non-zero if a hard criterion fails.
Hard criteria: identical seed sets; identical kept-candidate seeds, order and hit sets in >= 99.9 % of candidates;
identical per-trial rung pass flags and |N_pass(fast) - N_pass(ref)| <= max(2, 0.1 % N_pass(ref)) per rung.
"""
import json
import sys
import time

import numpy as np
from scipy.stats import chi2 as CHI2

from . import finder as FF
from . import trials as TR
from .reference import OUT as REFD, VARS as RVARS

INT_VARS = ['nit2', 'not2', 'nl2', 'not2h', 'nl2h', 'nl1', 'nhit', 'nip2', 'n2s2', 'n_core']
FLT_VARS = ['chi2ndf', 'dw_old', 'dw_core', 'chi2_core', 'nz']


def pchi(c2, nc):
    ndf = np.maximum(nc - 2, 1)
    return np.where(np.isfinite(c2) & (nc >= 4), CHI2.sf(np.nan_to_num(c2) * ndf, ndf), np.nan)


def rung_masks(V):
    """V: dict of arrays.  Cumulative F0 ladder (plan §2.5 item 3; F1 rungs not part of this finder) + families."""
    nit2, nip2, n2s2, w = V['nit2'], V['nip2'], V['n2s2'], V['dw_core']
    p = pchi(V['chi2_core'], V['n_core'])
    with np.errstate(invalid='ignore'):
        R = {}
        cur = (nit2 >= 3) & (nip2 >= 4)
        R['01_IP2>=4'] = cur
        for k in (5, 6, 7):
            cur = cur & (nip2 >= k); R['%02d_IP2>=%d' % (k - 3, k)] = cur
        for i, W in enumerate((37.5, 18.75, 9.4, 4.7)):
            cur = cur & (w < W); R['%02d_w<%g' % (5 + i, W)] = cur
        for i, P_ in enumerate((1e-3, 0.01, 0.05)):
            cur = cur & (p > P_); R['%02d_p>%g' % (9 + i, P_)] = cur
        for i, k in enumerate((1, 2, 3)):
            cur = cur & (n2s2 >= k); R['%02d_2S2>=%d' % (12 + i, k)] = cur
        base = (nit2 >= 3) & (nip2 >= 4)
        for W in (37.5, 18.75, 9.4):
            R['fam_IP2>=4_w<%g' % W] = base & (w < W)
        for P_ in (1e-3, 0.05):
            R['fam_IP2>=4_p>%g' % P_] = base & (p > P_)
        R['fam_IP2>=7_w<37.5_p>1e-3'] = base & (nip2 >= 7) & (w < 37.5) & (p > 1e-3)
    return R


def distinct_sets(hits_list, idx):
    """Distinct hit sets (exact identity) among candidates idx."""
    return len({hits_list[i].tobytes() for i in idx})


def compare_trial(i, rho, cfg):
    with np.load(REFD / f'ref_rho{rho}_t{i:03d}.npz') as z:
        ref = {k: z[k] for k in z.files}
    x = TR.trial_inputs(i, rho)
    t0 = time.perf_counter()
    r = FF.find(x['H'], x['sid'], x['pv'], x['phimet'], cfg=cfg, store='all', want_hits=True, want_seeds=True)
    t_fast = time.perf_counter() - t0
    out = dict(trial=i, rho=rho, t_fast_s=round(t_fast, 3), t_ref=json.loads(str(ref['T'])))
    # 1. seeds
    rs = {(int(a), int(b)) for a, b, n2 in ref['seeds']}
    fs = {(int(a), int(b)) for a, b in r['seeds_all']}
    out['seeds'] = dict(n_ref=len(rs), n_fast=len(fs), only_ref=len(rs - fs), only_fast=len(fs - rs))
    out['ntrip'] = dict(ref=int(ref['ntrip']), fast=int(r['n_trip']))
    # 2. candidates
    RV = {k: ref['V'][:, j] for j, k in enumerate(RVARS)}
    FV = dict(r['vars'])
    FV['seed_n2'] = r['seed_n2'].astype(float)
    rab = [tuple(x_) for x_ in ref['seed_ab'].tolist()]
    fab = [tuple(x_) for x_ in r['seed_ab'].tolist()]
    nref, nfast = len(rab), len(fab)
    rh = [ref['hits'][ref['hoff'][k]:ref['hoff'][k + 1]] for k in range(nref)]
    fh = [np.asarray(h, np.int32) for h in r['hits']]
    # match candidates by identical hit set (the 2-mrad merge may keep a different seed of the same duplicate group
    # when two duplicates tie in (N_L2, chi2/ndf) to the last bits: summation order differs)
    fkey = {}
    for k, h in enumerate(fh):
        fkey.setdefault(h.tobytes(), []).append(k)
    ri = []; fi = []
    for k, h in enumerate(rh):
        lst = fkey.get(h.tobytes())
        if lst:
            ri.append(k); fi.append(lst.pop(0))
    ri = np.array(ri, int); fi = np.array(fi, int)
    same_seed = int(sum(rab[a] == fab[b] for a, b in zip(ri, fi)))
    rank_shift = np.abs(ri - fi)
    cm = dict(n_ref=nref, n_fast=nfast, n_matched_hitset=int(len(ri)), n_matched_same_seed=same_seed,
              same_rank_order_by_hitset=bool(len(ri) == nref == nfast and np.all(ri == fi)),
              max_rank_shift=int(rank_shift.max()) if len(ri) else 0)
    cm['n_same_hitset'] = int(len(ri))
    cm['same_rank_order'] = cm['same_rank_order_by_hitset']
    ivd = {}
    for k in INT_VARS + ['seed_n2']:
        if len(ri):
            ivd[k] = int(np.sum(RV[k][ri] != FV[k][fi]))
    cm['int_var_mismatch'] = ivd
    fd = {}
    for k in FLT_VARS:
        if len(ri):
            a = RV[k][ri]; b = FV[k][fi]
            both = np.isfinite(a) & np.isfinite(b)
            rel = np.abs(a[both] - b[both]) / np.maximum(np.abs(a[both]), 1e-12)
            fd[k] = dict(max_rel=float(rel.max()) if both.any() else 0.0, n_rel_gt_1e6=int(np.sum(rel > 1e-6)),
                         nan_mismatch=int(np.sum(np.isfinite(a) != np.isfinite(b))))
    cm['float_var'] = fd
    out['cands'] = cm
    # 3. rungs
    RM = rung_masks(RV); FM = rung_masks(FV)
    rr = {}
    for name in RM:
        a = np.where(RM[name])[0]; b = np.where(FM[name])[0]
        rr[name] = dict(ref=int(len(a)), fast=int(len(b)), ref_sets=distinct_sets(rh, a), fast_sets=distinct_sets(fh, b),
                        pass_ref=bool(len(a) > 0), pass_fast=bool(len(b) > 0))
    out['rungs'] = rr
    out['fast_counters'] = {k: r[k] for k in ('n_road', 'n_trip', 'n_refit', 'n_fast', 'n_kept_all', 'n_regather',
                                              'n_fullscan')}
    out['fast_times_s'] = {k: round(v, 3) for k, v in r['times_s'].items()}
    return out


def summarise(res):
    S = dict(n_trials=len(res))
    S['seeds_identical_trials'] = int(sum(r['seeds']['only_ref'] == 0 and r['seeds']['only_fast'] == 0 for r in res))
    nref = sum(r['cands']['n_ref'] for r in res); nfast = sum(r['cands']['n_fast'] for r in res)
    S['cands'] = dict(n_ref=nref, n_fast=nfast, n_matched_same_seed=sum(r['cands']['n_matched_same_seed'] for r in res),
                      max_rank_shift=max(r['cands']['max_rank_shift'] for r in res),
                      n_same_hitset=sum(r['cands']['n_same_hitset'] for r in res),
                      trials_same_rank_order=int(sum(r['cands']['same_rank_order'] for r in res)))
    S['cands']['frac_same_hitset_of_ref'] = S['cands']['n_same_hitset'] / max(nref, 1)
    ivd = {}
    for r in res:
        for k, v in r['cands']['int_var_mismatch'].items():
            ivd[k] = ivd.get(k, 0) + v
    S['int_var_mismatch'] = ivd
    fd = {}
    for r in res:
        for k, v in r['cands']['float_var'].items():
            d = fd.setdefault(k, dict(max_rel=0.0, n_rel_gt_1e6=0, nan_mismatch=0))
            d['max_rel'] = max(d['max_rel'], v['max_rel']); d['n_rel_gt_1e6'] += v['n_rel_gt_1e6']
            d['nan_mismatch'] += v['nan_mismatch']
    S['float_var'] = fd
    rungs = {}
    for name in res[0]['rungs']:
        a = np.array([r['rungs'][name]['ref'] for r in res]); b = np.array([r['rungs'][name]['fast'] for r in res])
        sa = np.array([r['rungs'][name]['ref_sets'] for r in res]); sb = np.array([r['rungs'][name]['fast_sets'] for r in res])
        rungs[name] = dict(n_ref=int(a.sum()), n_fast=int(b.sum()), sets_ref=int(sa.sum()), sets_fast=int(sb.sum()),
                           trials_pass_ref=int((a > 0).sum()), trials_pass_fast=int((b > 0).sum()),
                           trials_flag_differs=int(((a > 0) != (b > 0)).sum()),
                           max_abs_diff_per_trial=int(np.abs(a - b).max()))
    S['rungs'] = rungs
    hard = dict(
        seeds_identical=S['seeds_identical_trials'] == len(res),
        hitsets_ge_99p9=S['cands']['frac_same_hitset_of_ref'] >= 0.999,
        rung_flags_identical=all(v['trials_flag_differs'] == 0 for v in rungs.values()),
        rung_counts_close=all(abs(v['n_fast'] - v['n_ref']) <= max(2, 1e-3 * v['n_ref']) for v in rungs.values()))
    S['hard_criteria'] = hard
    S['PASS'] = all(hard.values())
    return S


if __name__ == '__main__':
    i0, i1 = int(sys.argv[1]), int(sys.argv[2])
    rho = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    tag = sys.argv[4] if len(sys.argv) > 4 else ''
    cfg = FF.Config(seed_n2_exact=True)
    res = []
    for i in range(i0, i1):
        if not (REFD / f'ref_rho{rho}_t{i:03d}.npz').exists():
            continue
        o = compare_trial(i, rho, cfg)
        res.append(o)
        c = o['cands']
        print('trial', i, 'seeds', o['seeds'], 'cands', c['n_ref'], c['n_fast'], 'same hitsets', c['n_same_hitset'], 'same seed', c['n_matched_same_seed'], 'max rank shift', c['max_rank_shift'],
              'order', c['same_rank_order'], 'int mism', c['int_var_mismatch'], 't_fast', o['t_fast_s'], flush=True)
    S = summarise(res)
    S['config'] = {k: (list(v) if isinstance(v, tuple) else v) for k, v in vars(cfg).items()}
    rep = dict(summary=S, trials=res)
    path = TR.TT / 'data' / 'acts_stage4' / 'g2' / f'equivalence_rho{rho}{("_" + tag) if tag else ""}.json'
    path.write_text(json.dumps(rep, indent=1))
    print(json.dumps(S, indent=1))
    sys.exit(0 if S['PASS'] else 1)
