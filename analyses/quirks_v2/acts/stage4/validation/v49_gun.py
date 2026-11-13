"""V4-9 (geometry and material) + the dE/dx MIP unit (WP_RULE F-2/F-3) + the eloss.py closure (review WP_RULE R1 B-2),
from the G1 chain muon-gun outputs (run_chain.py gun).  Not signal.  TT env:
  pixi run python -m acts.stage4.validation.v49_gun
Inputs data/acts_stage4/g1/v49/{mu_mip, mu_bnd_n32, mu_bnd_n1, mu_hl}.npz; output v49.json there.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import ks_2samp

from acts.stage4.code import eloss as EL

TT = Path(__file__).resolve().parents[3]
D = TT / 'data' / 'acts_stage4' / 'g1' / 'v49'
S = json.loads((TT / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())['surfaces']
KIND = np.array([s['kind'] for s in S]); TYPE = np.array([s['type'] for s in S])
NAME = [s['name'] for s in S]
TBPX = [i for i, n in enumerate(NAME) if n.startswith('TBPX')]
MMU = 0.1056583755
TRUNC = 0.6


def load(name):
    z = np.load(D / f'{name}.npz')
    m = json.loads(str(z['meta']))
    evs = []
    for i in range(m['n_events']):
        evs.append(dict(ev=z[f'ev{i}'], tru=z[f'tru{i}'], vz=z[f'vz{i}'], mom=z[f'mom{i}'] if f'mom{i}' in z.files else None))
    return z, m, evs


def per_muon(evs):
    """-> list of (event, vp, vertex row, hit rows idx) per gun muon."""
    out = []
    for ie, e in enumerate(evs):
        vp = e['ev'][:, 7].astype(np.int64)
        for v in e['vz']:
            k = int(v[0])
            out.append((ie, k, v, np.where(vp == k)[0]))
    return out


def trunc_mean(x):
    x = np.sort(x)
    k = max(1, min(len(x), int(np.ceil(TRUNC * len(x)))))
    return x[:k].mean()


def main():
    res = {}
    # ---------------------------------------------------------------- 1. central pattern + on-surface (n32)
    z, m, evs = load('mu_mip')
    res['mu_mip'] = dict(n_events=m['n_events'], v41_pass=m['v41_pass'], max_onsurf_um=float(z['v41'][:, 6].max()),
                         n_lost=m.get('n_lost_simhits'))
    pat = []; dedx_trk = []; bg_trk = []; pooled = []; fat = []; smp = []; fat_kind = {}; smp_kind = {}
    rng = np.random.default_rng(12345)
    for ie, k, v, idx in per_muon(evs):
        e = evs[ie]['ev'][idx]; tr = evs[ie]['tru'][idx]; mo = evs[ie]['mom'][idx]
        p = math.sqrt(v[5] ** 2 + v[6] ** 2 + v[7] ** 2)
        eta = math.asinh(v[7] / math.hypot(v[5], v[6]))
        sid = e[:, 0].astype(np.int64)
        if abs(eta) < 0.8:
            pat.append(len(idx) == 17 and len(np.unique(sid)) == 17)
        # dE/dx estimator (WP_RULE D1): TBPX hits, dE * r_xy/|u| from the true vertex, lowest-60 % mean
        it = np.isin(sid, TBPX)
        if it.sum() >= 1:
            u = e[it, 1:4] - v[1:4]
            dc = e[it, 11] * np.hypot(u[:, 0], u[:, 1]) / np.linalg.norm(u, axis=1)
            dedx_trk.append(trunc_mean(dc)); bg_trk.append(p / MMU); pooled.append(dc)
        # eloss closure: Fatras deposit vs the numpy sampler at the same p, slab and incidence (Si sensors)
        si = np.isin(KIND[sid], ['IT', 'PS', '2S'])
        if si.any():
            pb = np.linalg.norm(mo[si, 0:3], axis=1)
            th = np.array([EL.slab_thickness(s, S) for s in sid[si]])
            pf = EL.path_factor(TYPE[sid[si]], tr[si, 0], tr[si, 1], mo[si, 0], mo[si, 1], mo[si, 2])
            ds = EL.sample(th * pf, MMU, pb, rng.random(si.sum()))
            for kk, a, b in zip(KIND[sid[si]], e[si, 11], ds):
                fat_kind.setdefault(kk, []).append(a); smp_kind.setdefault(kk, []).append(b)
            fat.append(e[si, 11] / (th * pf)); smp.append(ds / (th * pf))
    pooled = np.concatenate(pooled)
    mip_track = float(np.median(dedx_trk)); mip_pooled = float(trunc_mean(pooled))
    res['central_pattern_17'] = dict(n_muons=len(pat), frac_17=float(np.mean(pat)), pass_=bool(np.mean(pat) >= 0.99))
    # sampler-side MIP unit: replace each TBPX deposit by the sampler draw (same hits) and recompute the estimator
    fat = np.concatenate(fat); smp = np.concatenate(smp)
    ks = {k: dict(n=len(fat_kind[k]), fatras_median_keV=1e6 * float(np.median(fat_kind[k])),
                  sampler_median_keV=1e6 * float(np.median(smp_kind[k])),
                  ratio_median=float(np.median(smp_kind[k]) / np.median(fat_kind[k])),
                  fatras_q90_keV=1e6 * float(np.percentile(fat_kind[k], 90)),
                  sampler_q90_keV=1e6 * float(np.percentile(smp_kind[k], 90)),
                  ks_p=float(ks_2samp(fat_kind[k], smp_kind[k]).pvalue)) for k in fat_kind}
    # MIP unit with the sampler (closure criterion: within 3 %)
    rng2 = np.random.default_rng(777)
    dedx_s = []; pooled_s = []
    for ie, k, v, idx in per_muon(evs):
        e = evs[ie]['ev'][idx]; tr = evs[ie]['tru'][idx]; mo = evs[ie]['mom'][idx]
        sid = e[:, 0].astype(np.int64); it = np.isin(sid, TBPX)
        if it.sum() >= 1:
            pb = np.linalg.norm(mo[it, 0:3], axis=1)
            th = np.array([EL.slab_thickness(s, S) for s in sid[it]])
            pf = EL.path_factor(TYPE[sid[it]], tr[it, 0], tr[it, 1], mo[it, 0], mo[it, 1], mo[it, 2])
            ds = EL.sample(th * pf, MMU, pb, rng2.random(it.sum()))
            u = e[it, 1:4] - v[1:4]
            dcs = ds * np.hypot(u[:, 0], u[:, 1]) / np.linalg.norm(u, axis=1)
            dedx_s.append(trunc_mean(dcs)); pooled_s.append(dcs)
    mip_s = float(np.median(dedx_s)); mip_ps = float(trunc_mean(np.concatenate(pooled_s)))
    res['mip_unit'] = dict(definition='FROZEN (frozen_inputs mip_definition): mip_gev = mip_gev_pooled_truncated = the '
                                      'pooled 0.6-truncated mean of the path-corrected (x r_xy/|u|, u from the true '
                                      'vertex) TBPX deposits of all muon-gun hits (pT U[1,10] GeV, eta U[-2.5,2.5], '
                                      'luminous-region vertex; same Fatras/digi/slab config as PU). '
                                      'mip_gev_track_median (per-track lowest-60 % mean, median over tracks) is the '
                                      'superseded draft definition, kept as a diagnostic only.',
                           mip_gev=mip_pooled,
                           n_tracks=len(dedx_trk), mip_gev_track_median=mip_track,
                           mip_gev_pooled_truncated=mip_pooled, muon_betagamma_median=float(np.median(bg_trk)),
                           n_pooled_hits=int(len(pooled)),
                           sampler_mip_gev_track_median=mip_s, sampler_over_fatras=mip_s / mip_track,
                           sampler_mip_gev_pooled_truncated=mip_ps, sampler_over_fatras_pooled=mip_ps / mip_pooled,
                           closure_pass_3pct=bool(abs(mip_ps / mip_pooled - 1) < 0.03),
                           closure_track_median_diag=bool(abs(mip_s / mip_track - 1) < 0.03))
    res['eloss_closure_per_kind'] = ks
    # ---------------------------------------------------------------- 2. sector-boundary gun (n32 vs n1)
    _, m32, e32 = load('mu_bnd_n32'); _, m1, e1 = load('mu_bnd_n1')
    d_cnt = []; d_sid = []; res_b = []; res_bulk = []
    for a, b in zip(per_muon(e32), per_muon(e1)):
        ea = e32[a[0]]['ev'][a[3]]; eb = e1[b[0]]['ev'][b[3]]
        d_cnt.append(len(a[3]) - len(b[3]))
        d_sid.append(not np.array_equal(np.sort(ea[:, 0]), np.sort(eb[:, 0])))
        ta = e32[a[0]]['tru'][a[3]]
        bar = TYPE[ea[:, 0].astype(np.int64)] == 0
        ph_m = np.arctan2(ea[bar, 2], ea[bar, 1]); ph_t = np.arctan2(ta[bar, 1], ta[bar, 0])
        r = np.hypot(ta[bar, 0], ta[bar, 1])
        drphi = r * ((ph_m - ph_t + np.pi) % (2 * np.pi) - np.pi)
        sec = (ph_t + np.pi) / (2 * np.pi / 32)
        dist = r * np.minimum(sec - np.floor(sec), np.ceil(sec) - sec) * (2 * np.pi / 32)    # mm to the boundary
        kk = KIND[ea[bar, 0].astype(np.int64)]
        sig = np.where(kk == 'IT', 7.2e-3, np.where(kk == 'PS', 28.9e-3, np.where(kk == '2S', 26.0e-3, 16.0)))
        near = (dist < 2 * sig) & (kk != 'BTL')
        res_b.append(drphi[near] / sig[near]); res_bulk.append(drphi[(dist > 5 * sig) & (kk != 'BTL')] / sig[(dist > 5 * sig) & (kk != 'BTL')])
    rb = np.concatenate(res_b); rk = np.concatenate(res_bulk)
    res['sector_boundary'] = dict(n_muons=len(d_cnt), n32_v41=m32['v41_pass'], n1_v41=m1['v41_pass'],
                                  muons_with_hit_count_diff=int(np.sum(np.array(d_cnt) != 0)),
                                  muons_with_surface_set_diff=int(np.sum(d_sid)),
                                  hit_count_diff_values=sorted(set(int(x) for x in d_cnt)),
                                  near_boundary_hits_lt_2sigma=int(len(rb)),
                                  pull_rms_near=float(np.std(rb)) if len(rb) else None,
                                  pull_rms_bulk=float(np.std(rk)),
                                  pass_=bool(np.sum(np.array(d_cnt) != 0) == 0))
    # ---------------------------------------------------------------- 3. Highland at TBPX L1 (1 GeV/c muons, eta ~ 0)
    _, mh, eh = load('mu_hl')
    th_x = []; th_y = []; pp = []
    for ie, k, v, idx in per_muon(eh):
        e = eh[ie]['ev'][idx]; mo = eh[ie]['mom'][idx]
        l1 = np.where(e[:, 0] == 0)[0]
        if len(l1) != 1:
            continue
        b = mo[l1[0], 0:3]; a = mo[l1[0], 4:7]
        bh = b / np.linalg.norm(b)
        # two orthogonal projections: transverse-azimuthal and longitudinal
        e1v = np.cross([0, 0, 1.0], bh); e1v /= np.linalg.norm(e1v); e2v = np.cross(bh, e1v)
        ah = a / np.linalg.norm(a)
        th_x.append(np.arctan2(ah @ e1v, ah @ bh)); th_y.append(np.arctan2(ah @ e2v, ah @ bh))
        pp.append(np.linalg.norm(b))
    th = np.concatenate([th_x, th_y]); p = float(np.median(pp))
    beta = p / math.sqrt(p * p + MMU * MMU)
    x = 0.012               # TBPX x/X0 (normal incidence at eta ~ 0)
    hl = 13.6e-3 / (beta * p) * math.sqrt(x) * (1 + 0.038 * math.log(x / beta ** 2))
    core = 1.4826 * np.median(np.abs(th - np.median(th)))
    # PDG definition of theta0 (RPP 'Passage of particles through matter', Highland formula): the width of a Gaussian
    # fit to the central 98 % of the projected-angle distribution -> truncated-Gaussian ML fit on |theta| < q98
    from scipy.optimize import minimize_scalar
    from scipy.stats import norm
    c = np.percentile(np.abs(th), 98); tc = th[np.abs(th) < c]

    def nll(sg):
        return -(np.sum(norm.logpdf(tc, 0, sg)) - len(tc) * np.log(norm.cdf(c / sg) - norm.cdf(-c / sg)))
    sg98 = minimize_scalar(nll, bounds=(1e-5, 1e-1), method='bounded').x
    res['highland'] = dict(n=len(pp), p_gev=p, x_X0=x, highland_rad=hl,
                           fatras_gauss_fit_central98_rad=float(sg98), ratio=float(sg98 / hl),
                           fatras_core_mad_sigma_rad=float(core), ratio_mad=float(core / hl),
                           pass_10pct=bool(abs(sg98 / hl - 1) < 0.10),
                           note='criterion uses the PDG theta0 definition (Gaussian fit to the central 98 %); the '
                                'MAD core is reported as a diagnostic (Fatras GaussianMixture has a narrower core)')
    (D / 'v49.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
