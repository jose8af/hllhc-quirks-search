"""Phase-A validation of the in-job rho = 2 weights (weights.py) on PU-only rho = 2 trials (signal-blind).

Inputs: rho = 2 trials of trials.py, run through the finder (store='loose', hit lists), cached by `cache` below to
data/acts_stage4/g2b/dev/rho2_t<i>.npz (road arrays + candidate CSR; deleted after Phase A).
Checks (all written to data/acts_stage4/g2b/weights_validation.json):
  V-a  exact counting DP vs plain Monte Carlo (n_mc independent subsets per set) on >= 1000 sets, stratified over
       N_IP2 = 4, 5, 6, >= 7: per-set pulls z = (DP - MC)/sqrt(DP (1 - DP)/n_mc) per rung, their mean/rms, the fraction
       with |z| > 3, and the summed weights (DP vs MC with the MC error);
  V-b  the DP vs the f1r probe's own thin_weights (2e4-subset MC, fixed seed) on 100 sets, N_L2 rungs (semantics);
  V-c  subset_weights at q = 1 (no thinning) reproduces the stored full-set rung flags of kernels.cand_vars;
  V-d  importance-sampled subset weights vs plain unconditional Monte Carlo (same subset evaluation) on N_IP2 >= 7 sets;
  V-e  the IS normalisation mean(W) vs the exact DP P(N_IT2 >= 3, N_IP2 >= 7);
  timing per set of each kernel.
Run (theory_track): nice -n 10 pixi run python -m acts.stage4.finder.validate_weights cache 0 1
                    nice -n 10 pixi run python -m acts.stage4.finder.validate_weights run
"""
import json
import os
import sys
import time

import numpy as np

from . import finder as FF
from . import weights as WG
from . import trials as TR

# WPV_OUT=<dir relative to theory_track> redirects the cache and the output (fix WP_RULE R1: data/acts_stage4/wp_fix1)
_OD = TR.TT / os.environ['WPV_OUT'] if os.environ.get('WPV_OUT') else TR.TT / 'data' / 'acts_stage4' / 'g2b'
DEV = _OD / 'dev'
OUTJ = _OD / 'weights_validation.json'
MIP_TIMING = 8.0e-5      # GeV; a provisional dE/dx unit for the timing/validation only (NOT the G1 calibration)


def cache(idx):
    DEV.mkdir(parents=True, exist_ok=True)
    for i in idx:
        x = TR.trial_inputs(i, 2)
        r = FF.find(x['H'], x['sid'], x['pv'], x['phimet'], store='loose', want_hits=True, rho=2.0)
        m = r['road_mask']
        hoff = np.zeros(len(r['hits']) + 1, np.int64)
        hoff[1:] = np.cumsum([len(h) for h in r['hits']])
        np.savez(DEV / f'rho2_t{i:03d}.npz', H=x['H'][m], sid=x['sid'][m], INT=x['INT'][m], pv=x['pv'],
                 phimet=x['phimet'], hoff=hoff, hits=np.concatenate(r['hits']).astype(np.int32), normal=r['normal'],
                 axis=r['axis'], **{'v_' + k: v for k, v in r['vars'].items()})


def load(i):
    z = np.load(DEV / f'rho2_t{i:03d}.npz')
    d = {k: z[k] for k in z.files}
    H = d['H']
    d['U'] = np.ascontiguousarray(H[:, 1:4] - d['pv'][None, :])
    d['LC'] = FF.LC_OF[d['sid']]
    d['SD'] = FF.SIDE_OF[d['sid']]
    r = np.hypot(H[:, 1], H[:, 2])
    d['CX'] = H[:, 1] / r
    d['CY'] = H[:, 2] / r
    d['S0'] = np.ascontiguousarray(H[:, 4])
    d['S1'] = np.ascontiguousarray(H[:, 5])
    un = np.linalg.norm(d['U'], axis=1)
    d['dEc'] = H[:, 11] * np.hypot(d['U'][:, 0], d['U'][:, 1]) / un
    u, inv = np.unique(d['INT'], return_inverse=True)
    d['INTl'] = inv.astype(np.int64)
    d['nI'] = len(u)
    d['hits'] = d['hits'].astype(np.int64)
    return d


def run():
    rng = np.random.default_rng(20261013)
    out = dict(note='PU-only rho = 2 sets (trials.py rho = 2, i = 0, 1), q = 1/2; signal-blind')
    D = [load(0), load(1)]
    # ---------------- V-a: DP vs plain MC on >= 1000 sets (stratified)
    NMC = 20000
    za = []; sums = []; tdp = []; tmc = []
    per_stratum = 160
    for ti, d in enumerate(D):
        nip2 = d['v_nip2']
        sel = []
        for lo, hi in ((4, 5), (5, 6), (6, 7), (7, 99)):
            pool = np.where((nip2 >= lo) & (nip2 < hi))[0]
            sel.append(rng.choice(pool, min(per_stratum, len(pool)), replace=False))
        sel = np.sort(np.concatenate(sel)).astype(np.int64)
        WG.count_weights(d['hoff'], d['hits'], sel[:2], d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, 18)  # compile
        t0 = time.perf_counter()
        Wdp, info = WG.count_weights(d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, 18)
        tdp.append((time.perf_counter() - t0) / len(sel))
        WG.count_weights_mc(d['hoff'], d['hits'], sel[:1], d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, 10, 1)
        t0 = time.perf_counter()
        Wmc = WG.count_weights_mc(d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, NMC, 77 + ti)
        tmc.append((time.perf_counter() - t0) / len(sel))
        za.append((Wdp, Wmc, info, nip2[sel]))
    Wdp = np.concatenate([a[0] for a in za]); Wmc = np.concatenate([a[1] for a in za])
    info = np.concatenate([a[2] for a in za]); nipsel = np.concatenate([a[3] for a in za])
    va = dict(n_sets=int(len(Wdp)), n_mc=NMC, sets_per_stratum={str(k): int(np.sum((nipsel >= k) & (nipsel < k + 1)) if k < 7 else np.sum(nipsel >= 7)) for k in (4, 5, 6, 7)},
              M_max=int(info[:, 1].max()), M_mean=float(info[:, 1].mean()), m_mean=float(info[:, 0].mean()),
              n_flag_Mgt=int(info[:, 2].sum()), ms_per_set_dp=1e3 * float(np.mean(tdp)),
              ms_per_set_mc2e4=1e3 * float(np.mean(tmc)), rungs={})
    for k, name in enumerate(WG.COUNT_COLS):
        p = Wdp[:, k]; e = Wmc[:, k]
        sd = np.sqrt(np.maximum(p * (1 - p), 1e-300) / NMC)
        use = (p > 0) & (p < 1) & (p * NMC > 5)
        z = (p[use] - e[use]) / sd[use]
        # exact zero must give MC zero
        zero_bad = int(np.sum((p == 0) & (e > 0)))
        S_dp = float(p.sum()); S_mc = float(e.sum()); S_err = float(np.sqrt(np.sum(np.maximum(e * (1 - e), 0) / NMC)))
        va['rungs'][name] = dict(n_used=int(use.sum()), z_mean=float(z.mean()) if use.any() else None,
                                 z_rms=float(z.std()) if use.any() else None,
                                 frac_abs_z_gt3=float(np.mean(np.abs(z) > 3)) if use.any() else None,
                                 n_dp_zero_mc_nonzero=zero_bad, sum_dp=S_dp, sum_mc=S_mc, sum_mc_err=S_err,
                                 sum_pull=(S_dp - S_mc) / S_err if S_err > 0 else None)
    out['Va_dp_vs_mc'] = va
    print(json.dumps(va, indent=1), flush=True)
    # ---------------- V-b: vs f1r thin_weights (N_L2 rungs) on 100 sets
    d = D[0]
    sel = np.sort(rng.choice(len(d['hoff']) - 1, 100, replace=False)).astype(np.int64)
    Wdp, _ = WG.count_weights(d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, 18)
    zb = {str(L): [] for L in (5, 6, 7, 8, 9, 10)}
    for r_, c in enumerate(sel):
        hh = d['hits'][d['hoff'][c]:d['hoff'][c + 1]]
        tw, m = FF.thin_weights(hh, d['LC'], d['SD'], d['INT'], 2.0)
        for i, L in enumerate((5, 6, 7, 8, 9, 10)):
            p = Wdp[r_, 4 + i]; e = tw[str(L)]['p']
            if 5 < p * 20000 and p < 1:
                zb[str(L)].append((p - e) / np.sqrt(p * (1 - p) / 20000))
    out['Vb_dp_vs_f1r_thin_weights'] = {L: dict(n=len(v), z_mean=float(np.mean(v)) if v else None,
                                                z_rms=float(np.std(v)) if v else None) for L, v in zb.items()}
    print(json.dumps(out['Vb_dp_vs_f1r_thin_weights']), flush=True)
    # ---------------- V-c: q = 1 reproduces the full-set flags
    from scipy.stats import chi2 as CHI2
    vc = dict(n=0, mismatch={})
    for d in D:
        s7 = np.where(d['v_nip2'] >= 7)[0]
        sel = np.sort(rng.choice(s7, min(1000, len(s7)), replace=False)).astype(np.int64)
        Wm, Wv, nz = WG.subset_weights(d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], d['U'], d['CX'],
                                       d['CY'], d['S0'], d['S1'], d['dEc'], d['normal'], d['axis'], 1.0, 4, 5, 0.030,
                                       MIP_TIMING, WG.CHI2_ISF, 18)
        w = d['v_dw_core'][sel]; nc = d['v_n_core'][sel]; c2 = d['v_chi2_core'][sel]; n2 = d['v_n2s2'][sel]
        ndf = np.maximum(nc - 2, 1)
        with np.errstate(invalid='ignore'):
            p = np.where((nc >= 4) & np.isfinite(c2), CHI2.sf(np.nan_to_num(c2) * ndf, ndf), np.nan)
            ok = np.ones(len(sel), bool); ref = []
            for W_ in WG.W_K:
                ok = ok & (w < W_); ref.append(ok.copy())
            for P_ in WG.P_MIN:
                ok = ok & (p > P_); ref.append(ok.copy())
            for k in (1, 2, 3):
                ok = ok & (n2 >= k); ref.append(ok.copy())
            fb0 = (p > 0.05) & (n2 >= 3)
            fbs = [fb0] + [fb0 & (w < W_) for W_ in WG.W_K]
        # dE/dx columns (fix WP_RULE R1 B-1: core IT hits) vs the full-set production.dedx_sets
        from .production import dedx_sets
        ho = np.zeros(len(sel) + 1, np.int64); ho[1:] = np.cumsum(d['hoff'][sel + 1] - d['hoff'][sel])
        hh = np.concatenate([d['hits'][d['hoff'][c]:d['hoff'][c + 1]] for c in sel])
        de = dedx_sets(ho, hh, d['LC'], d['dEc'], MIP_TIMING, WG.TRUNC_FRAC, d['U'], d['normal'][sel], d['axis'][sel])
        with np.errstate(invalid='ignore'):
            ref_e = [ok & (de > e) for e in WG.E_MIN]
            fb_e = [fk & (de > e) for fk in fbs for e in WG.E_MIN]
        vc['n_dedx_finite'] = vc.get('n_dedx_finite', 0) + int(np.isfinite(de).sum())
        vc['dedx_median_mipunits'] = float(np.nanmedian(de))
        cols = list(range(10)) + list(range(13, 18)) + [10, 11, 12] + list(range(18, 33))
        refs = ref + fbs + ref_e + fb_e
        for k, R in zip(cols, refs):
            name = WG.SUB_COLS[k]
            vc['mismatch'][name] = vc['mismatch'].get(name, 0) + int(np.sum((Wm[:, k] > 0.5) != R))
        vc['n'] += len(sel)
        vc['meanW_not_1'] = vc.get('meanW_not_1', 0) + int(np.sum(np.abs(Wm[:, 33] - 1) > 1e-12))
        vc['n_pass_w<37.5'] = vc.get('n_pass_w<37.5', 0) + int(np.sum(ref[0]))
    out['Vc_q1_full_set'] = vc
    print(json.dumps(vc), flush=True)
    # ---------------- V-d / V-e: IS vs plain MC on N_IP2 >= 7 sets; mean W vs DP
    NSUB = 256
    NPL = 40000
    vd = dict(n_sub_is=NSUB, n_plain=NPL, rungs={})
    acc = []
    tis = []
    for ti, d in enumerate(D):
        s7 = np.where(d['v_nip2'] >= 7)[0]
        # half random, half the narrowest full-set widths (so the deep width rungs are populated)
        nrw = s7[np.argsort(d['v_dw_core'][s7])[:150]]
        rnd = rng.choice(np.setdiff1d(s7, nrw), 150, replace=False)
        sel = np.sort(np.concatenate([nrw, rnd])).astype(np.int64)
        args = (d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], d['U'], d['CX'], d['CY'], d['S0'],
                d['S1'], d['dEc'], d['normal'], d['axis'], 0.5)
        t0 = time.perf_counter()
        Wm, Wv, nz = WG.subset_weights(*args, NSUB, 11 + ti, 0.030, MIP_TIMING, WG.CHI2_ISF, 18)
        tis.append((time.perf_counter() - t0) / len(sel))
        Wp = WG.subset_weights_mc(*args, NPL, 23 + ti, 0.030, MIP_TIMING, WG.CHI2_ISF)
        Wdp, _ = WG.count_weights(d['hoff'], d['hits'], sel, d['LC'], d['SD'], d['INTl'], d['nI'], 0.5, 18)
        acc.append((Wm, Wv, Wp, Wdp[:, 3]))
    Wm = np.concatenate([a[0] for a in acc]); Wv = np.concatenate([a[1] for a in acc])
    Wp = np.concatenate([a[2] for a in acc]); P7 = np.concatenate([a[3] for a in acc])
    for k, name in enumerate(WG.SUB_COLS):
        a = Wm[:, k]; b = Wp[:, k]
        if not np.all(np.isfinite(a)):
            continue
        ea = np.sqrt(Wv[:, k]); eb = np.sqrt(np.maximum(b * (1 - b), 0) / NPL)
        Sa = float(a.sum()); Sb = float(b.sum())
        Ea = float(np.sqrt(np.sum(Wv[:, k]))); Eb = float(np.sqrt(np.sum(eb ** 2)))
        use = (ea > 0) | (eb > 0)
        z = (a[use] - b[use]) / np.sqrt(ea[use] ** 2 + eb[use] ** 2 + 1e-300)
        vd['rungs'][name] = dict(sum_is=Sa, sum_is_err=Ea, sum_plain=Sb, sum_plain_err=Eb,
                                 sum_pull=(Sa - Sb) / np.sqrt(Ea ** 2 + Eb ** 2) if (Ea + Eb) > 0 else None,
                                 n_sets_nonzero=int(np.sum((a > 0) | (b > 0))),
                                 z_rms=float(z.std()) if len(z) > 1 else None, z_mean=float(z.mean()) if len(z) else None)
    vd['ms_per_set_is'] = 1e3 * float(np.mean(tis))
    out['Vd_is_vs_plain'] = vd
    ve = dict(sum_meanW=float(Wm[:, 33].sum()), sum_meanW_err=float(np.sqrt(Wv[:, 33].sum())), sum_dp=float(P7.sum()),
              n_sets_exact_W=int(np.sum(Wv[:, 33] == 0)),          # M = 0: W is constant = the DP value
              max_absdiff_exact_W=float(np.max(np.abs(Wm[Wv[:, 33] == 0, 33] - P7[Wv[:, 33] == 0]), initial=0.0)),
              per_set_z_rms_varying_W=float(np.std(((Wm[:, 33] - P7) / np.sqrt(Wv[:, 33]))[Wv[:, 33] > 0])))
    ve['pull'] = (ve['sum_meanW'] - ve['sum_dp']) / ve['sum_meanW_err']
    out['Ve_meanW_vs_dp'] = ve
    print(json.dumps(vd, indent=1), json.dumps(ve), flush=True)
    OUTJ.write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == 'cache':
        cache([int(a) for a in sys.argv[2:]])
    else:
        run()
