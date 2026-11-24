"""Reviewer Liv (cycle 2, P3B v2): re-analysis of the fixer's B3 importance-sampling check. Read-only.

Inputs: the 8 p3-b-occmod outputs (stored IS, 200 toys/config) and the fixer's 3 scratch outputs
/home/scratch/jdochoa/ivar-ischeck-{0,1,2}/ischeck-*.npz (plain 1e5 + fresh IS 2,000 toys per config, all 6,400
configs). Writes liv_ischeck.json next to this script. Questions:
 (1) are the 6,400 configs covered once each; (2) how concentrated are the 45 plain R08 passes over configs;
 (3) toy-level vs configuration-level error of E_model(R08) (and R07) from independent replicates
     (stored, fresh, plain: Cov across configs of two independent estimates = variance of the true per-config p);
 (4) candidate readings of DOR's "~12 %" from isr[:, 3, 1];
 (5) paired plain-vs-IS significance with the toy-level IS errors (R07, R08).
"""
import glob, json, sys
import numpy as np

D = '/nfs/cajuela/jdochoa/quirks_v2/data/p3b/p3-b-occmod/'
fs = sorted(glob.glob(D + '*/occmod-*.npz'))
occ = [np.load(f) for f in fs]
nis0 = json.loads(str(occ[0]['meta_json']))['nis']
pA = np.array([o['pA'].mean() for o in occ])
paths = sorted(glob.glob('/home/scratch/jdochoa/ivar-ischeck-*/ischeck-*.npz'))
ck = [np.load(p) for p in paths]
sel = np.concatenate([c['sel'] for c in ck])
plain = np.concatenate([c['plain'] for c in ck])
isr = np.concatenate([c['isr'] for c in ck])  # (N, 2 [R07,R08], 3 [m1,m2,npass])
st8 = np.concatenate([c['stored_m1_R08'] for c in ck])
nplain = int(ck[0]['nplain']); nisf = int(ck[0]['nis'])
out = {'files_occmod': [f.split('/')[-1] for f in fs], 'files_check': paths, 'nis_stored': nis0, 'nplain': nplain,
       'nis_fresh': nisf}
keys = set(map(tuple, sel.tolist()))
out['n_rows'] = int(len(sel)); out['n_unique'] = len(keys)
out['n_expected'] = int(sum(o['isr'].shape[0] for o in occ))
# per-config pA weighting: E = mean_seed pA_s * mean_b m1 ; seeds have equal nB, so use pA of the config's seed
pa_c = pA[sel[:, 0]]
res = {}
for kk, rung, kst in ((0, 'R07', 2), (1, 'R08', 3)):
    s = np.array([occ[fi]['isr'][b, kst, 0] for fi, b in sel])
    s2 = np.array([occ[fi]['isr'][b, kst, 1] for fi, b in sel])
    f = isr[:, kk, 0]; f2 = isr[:, kk, 1]
    p = plain[:, kst]
    kpl = np.rint(p * nplain).astype(int)
    N = len(s)
    r = {}
    r['plain_passes'] = int(kpl.sum())
    r['n_configs_with_plain_pass'] = int((kpl > 0).sum())
    srt = np.sort(kpl)[::-1]
    r['plain_top_counts'] = srt[:10].tolist()
    r['plain_top5_share'] = float(srt[:5].sum() / max(1, srt.sum()))
    # toy-level errors (variance of the sum over configs, conditional on configs)
    vt_s = np.clip(s2 - s ** 2, 0, None) / nis0
    vt_f = np.clip(f2 - f ** 2, 0, None) / nisf
    vt_p = p * (1 - p) / nplain
    r['rel_toy_stored'] = float(np.sqrt(vt_s.sum()) / s.sum())
    r['rel_toy_fresh'] = float(np.sqrt(vt_f.sum()) / f.sum())
    r['rel_toy_plain'] = float(np.sqrt(vt_p.sum()) / p.sum())
    # total (config + toy) error of the mean from each estimate's spread over configs
    for nm, x in (('stored', s), ('fresh', f), ('plain', p)):
        r[f'rel_total_{nm}'] = float(x.std(ddof=1) / np.sqrt(N) / x.mean())
        r[f'ess_configs_{nm}'] = float(x.sum() ** 2 / (x ** 2).sum()) if (x ** 2).sum() > 0 else None
        o = np.sort(x)[::-1]
        r[f'top1pct_share_{nm}'] = float(o[:N // 100].sum() / o.sum())
    # configuration-level variance of the true p: Cov of independent estimates across configs
    for a_, b_, nm in ((s, f, 'stored_fresh'), (s, p, 'stored_plain'), (f, p, 'fresh_plain')):
        cv = np.cov(a_, b_)[0, 1]
        m = 0.5 * (a_.mean() + b_.mean())
        r[f'rel_config_from_cov_{nm}'] = float(np.sqrt(max(cv, 0) / N) / m)
        r[f'cov_{nm}_sign'] = float(np.sign(cv))
        r[f'corr_{nm}'] = float(np.corrcoef(a_, b_)[0, 1])
    # paired ratios with toy-level errors
    r['plain_over_stored'] = float(p.sum() / s.sum())
    r['plain_over_fresh'] = float(p.sum() / f.sum())
    r['fresh_over_stored'] = float(f.sum() / s.sum())
    e1 = np.hypot(r['rel_toy_plain'], r['rel_toy_stored'])
    e2 = np.hypot(r['rel_toy_plain'], r['rel_toy_fresh'])
    r['pull_plain_vs_stored_toy'] = float((r['plain_over_stored'] - 1) / e1)
    r['pull_plain_vs_fresh_toy'] = float((r['plain_over_fresh'] - 1) / e2)
    r['rel_err_plain_over_stored'] = float(e1)
    r['rel_err_plain_over_fresh'] = float(e2)
    # pooled estimate of E from all three (diagnostic) and where the plain passes sit in the stored ranking
    rank = np.argsort(-s)
    pos = np.empty(N, int); pos[rank] = np.arange(N)
    r['plain_pass_configs_stored_rank'] = sorted(pos[kpl > 0].tolist())[:50]
    r['stored_zero_where_plain_pass'] = int(((s == 0) & (kpl > 0)).sum())
    r['fresh_zero_where_plain_pass'] = int(((f == 0) & (kpl > 0)).sum())
    res[rung] = r
out['rungs'] = res
# (4) readings of DOR's ~12 % from the stored isr[:, 3, 1] alone (per seed, then 8-seed mean)
d4 = {}
per = []
for o in occ:
    m1 = o['isr'][:, 3, 0]; m2 = o['isr'][:, 3, 1]; nB = len(m1)
    per.append(dict(rel_toy=float(np.sqrt(np.clip(m2 - m1 ** 2, 0, None).sum() / nis0) / m1.sum()),
                    rel_m2_naive=float(np.sqrt(m2.sum() / nis0) / m1.sum()),
                    rel_within=float(m1.std(ddof=1) / np.sqrt(nB) / m1.mean()),
                    ess_toys=float((m1.sum() * nis0) ** 2 / (m2.sum() * nis0))))
d4['per_seed'] = per
E = np.array([pA[i] * occ[i]['isr'][:, 3, 0].mean() for i in range(len(occ))])
for key in ('rel_toy', 'rel_m2_naive', 'rel_within'):
    rr = np.array([q[key] for q in per])
    d4[f'pooled_{key}'] = float(np.sqrt(np.sum((E * rr) ** 2)) / len(E) / E.mean())
    d4[f'mean_{key}_over_sqrt8'] = float(rr.mean() / np.sqrt(len(E)))
    d4[f'rms_{key}_over_sqrt8'] = float(np.sqrt((rr ** 2).mean()) / np.sqrt(len(E)))
ess = np.array([q['ess_toys'] for q in per])
d4['ess_toys_total'] = float(ess.sum()); d4['rel_from_total_ess'] = float(1 / np.sqrt(ess.sum()))
d4['rel_from_mean_ess_per_seed_over_sqrt8'] = float(np.mean(1 / np.sqrt(ess)) / np.sqrt(8))
out['dor_12pct_readings'] = d4
json.dump(out, open(sys.argv[1], 'w'), indent=1)
