"""p3c_validate.py -- sigma_soft from the source point and the external validation of B4-b (STR §4.7; log §P4).

  <python> p3c_validate.py <out_dir> zmm=<file,...> tt=<file,...>

Writes <out_dir>/model.json (sigma_soft per target, mixture fitted to Fig. 34) and <out_dir>/validation.json.
Verdict rules, readings and tolerances were fixed in the session log (2026-11-24 10:16) before this script existed.
"""
import json
import logging
import sys
from pathlib import Path

import numpy as np

import metmodel as M
import p3c_io as IO

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s')
log = logging.getLogger('p3c_validate')

# ---- readings of the public figures (ESTIMATE; reading errors as tolerance) --------------------------------------
UPERP_TARGETS = dict(nominal=29.8, **{'25': 25.0, '32.5': 32.5})     # CMS NOTE-2018/006 Fig. 35 right, text p. 19
UPAR_REF, UPAR_TOL = 31.8, 1.0                                        # Fig. 35 left at 1.4 /mm
# Fig. 34, Phase 2 curve, 6 GeV bins on 0-120 GeV, my reading from a 400 dpi rendering (log 10:16); sum 1.0126
FIG34 = np.array([0.036, 0.100, 0.143, 0.151, 0.130, 0.112, 0.092, 0.070, 0.055, 0.0366, 0.0252, 0.0208, 0.0130,
                  0.0092, 0.0060, 0.00425, 0.00305, 0.00226, 0.00242, 0.0008])
FIG34_EDGES = np.arange(0, 121, 6.0)
TAIL_THR, TAIL_TOL = (60.0, 78.0, 90.0), 0.20
# ATL-PHYS-PUB-2019-005 Fig. 18, "ITk full eta coverage", readings of retrieval_log #15 / SEB §1.3
ATLAS = [(500., 36.5), (1000., 37.5), (2000., 42.0), (3000., 46.5), (4000., 50.5)]
ATLAS_TOL, ATLAS_MIN_EV = 0.5, 1000
K_VAL = 4


def zmm_arrays(files):
    """Per-event quantities of Z -> mu mu: q (dimuon pT vector) and model inputs with the two muons removed."""
    parts = []
    for f in files:
        d = IO.load(f)
        inp = d['inp']; lp, lm = inp['lp'], inp['lm']
        ismu = lm & (np.abs(lp[:, :, 0]) == 13) & (np.abs(lp[:, :, 2]) < 2.8)
        ok = ismu.sum(1) == 2
        qx = (lp[:, :, 1] * np.cos(lp[:, :, 3]) * ismu).sum(1); qy = (lp[:, :, 1] * np.sin(lp[:, :, 3]) * ismu).sum(1)
        # other prompt leptons (rare) stay in the unclustered sum; the two muons are measured exactly
        ox = (lp[:, :, 1] * np.cos(lp[:, :, 3]) * (lm & ~ismu)).sum(1)
        oy = (lp[:, :, 1] * np.sin(lp[:, :, 3]) * (lm & ~ismu)).sum(1)
        inp = dict(inp); inp['ux'] = inp['ux'] + ox; inp['uy'] = inp['uy'] + oy
        inp['lm'] = np.zeros_like(lm)
        parts.append((IO.sub(inp, ok), qx[ok], qy[ok], len(ok)))
    inp = {k: np.concatenate([p[0][k] for p in parts]) for k in parts[0][0]}
    return inp, np.concatenate([p[1] for p in parts]), np.concatenate([p[2] for p in parts]), sum(p[3] for p in parts)


def recoil(inp, qx, qy, par, rng, K=K_VAL, chunk=20000):
    """-> u_par residual, u_perp, MET (each (n, K)) for a parameter set; hadronic recoil h = jets + U + S."""
    n = len(qx); up = np.zeros((n, K)); ut = np.zeros((n, K)); met = np.zeros((n, K))
    q = np.hypot(qx, qy); ex, ey = qx / np.maximum(q, 1e-9), qy / np.maximum(q, 1e-9)
    for a in range(0, n, chunk):
        sl = slice(a, a + chunk)
        o = M.apply(IO.sub(inp, sl), par, rng, K, return_met=True)
        hx, hy = o['hx'], o['hy']
        up[sl] = hx * ex[sl, None] + hy * ey[sl, None] + q[sl, None]       # 0 for a perfect recoil measurement
        ut[sl] = -hx * ey[sl, None] + hy * ex[sl, None]
        met[sl] = np.hypot(hx + qx[sl, None], hy + qy[sl, None])
    return up, ut, met


def rms_err(x):
    x = np.asarray(x).ravel(); n = len(x) / K_VAL                           # throws of one event are correlated
    s = float(np.sqrt(np.mean(x ** 2) - np.mean(x) ** 2))
    k = float(np.mean((x - x.mean()) ** 4) / s ** 4)
    return s, s * float(np.sqrt(max(k - 1, 0.1) / (4 * n)))


def half68(x):
    lo, hi = np.quantile(np.asarray(x).ravel(), [0.1587, 0.8413])
    return float(0.5 * (hi - lo))


def tails(met):
    h = np.histogram(met.ravel(), FIG34_EDGES)[0].astype(float)
    n_in = h.sum(); frac = h / n_in
    out = {}
    for t in TAIL_THR:
        k = int(round(t / 6.0))
        fm = float(frac[k:].sum()); ff = float(FIG34[k:].sum() / FIG34.sum())
        nt = h[k:].sum() / K_VAL
        stat = fm / np.sqrt(max(nt, 1.0))
        tol = float(np.hypot(TAIL_TOL * ff, stat))
        out[f'{t:g}'] = dict(model=fm, figure=ff, ratio=fm / ff, tolerance=tol, mc_stat=float(stat),
                             passes=bool(abs(fm - ff) <= tol))
    return out, frac


def summarise(name, inp, qx, qy, par, rng, sel30):
    up, ut, met = recoil(inp, qx, qy, par, rng)
    s_par, e_par = rms_err(up[sel30]); s_perp, e_perp = rms_err(ut[sel30])
    tl, frac = tails(met)
    tol = float(np.hypot(UPAR_TOL, e_par))
    r = dict(sigma_soft=par.get('sigma_soft'), soft_mix=par.get('soft_mix'), u_par_rms=s_par, u_par_rms_err=e_par,
             u_par_half68=half68(up[sel30]), u_par_mean=float(up[sel30].mean()), u_perp_rms=s_perp,
             u_perp_rms_err=e_perp, u_perp_half68=half68(ut[sel30]), u_par_ref=UPAR_REF, u_par_tolerance=tol,
             u_par_passes=bool(abs(s_par - UPAR_REF) <= tol), tail=tl, shape_model=frac.tolist(),
             shape_figure=(FIG34 / FIG34.sum()).tolist(),
             shape_max_abs_ln_ratio=float(np.max(np.abs(np.log(np.maximum(frac, 1e-9) / (FIG34 / FIG34.sum()))))),
             met_mean=float(met[met < 120].mean()), frac_above_120=float(np.mean(met >= 120)))
    r['RB_passes'] = bool(r['u_par_passes'] and all(v['passes'] for v in tl.values()))
    log.info('%-12s soft %s: u_perp %.2f+-%.2f  u_par %.2f+-%.2f (ref %.1f+-%.1f, %s)  tails %s  -> R-B %s', name,
             par.get('soft_mix') or round(par['sigma_soft'], 2), s_perp, e_perp, s_par, e_par, UPAR_REF, UPAR_TOL,
             'pass' if r['u_par_passes'] else 'FAIL',
             {k: (round(v['ratio'], 2), 'pass' if v['passes'] else 'FAIL') for k, v in tl.items()},
             'PASS' if r['RB_passes'] else 'FAIL')
    return r


def fit_mixture(inp, qx, qy, par0, rng):
    """Two-Gaussian soft term fitted to the Fig. 34 shape (least squares in ln, 20 bins): grid over (f2, s1, s2)."""
    n = min(len(qx), 200000)
    o = M.apply(IO.sub(inp, slice(0, n)), dict(par0, sigma_soft=0.0, soft_mix=None), rng, 1, return_met=True)
    ax = o['hx'][:, 0] + qx[:n]; ay = o['hy'][:, 0] + qy[:n]
    g1, g2 = rng.standard_normal(n), rng.standard_normal(n)
    sig = np.arange(8.0, 70.5, 1.0)
    H = np.array([np.histogram(np.hypot(ax + s * g1, ay + s * g2), FIG34_EDGES)[0] / n for s in sig])
    ref = np.log(FIG34 / FIG34.sum()); best = (1e9, None)
    for i1, s1 in enumerate(sig):
        for i2 in range(i1 + 1, len(sig)):
            for f2 in np.arange(0.02, 0.62, 0.02):
                h = (1 - f2) * H[i1] + f2 * H[i2]
                h = h / h.sum()
                c = float(np.sum((np.log(np.maximum(h, 1e-12)) - ref) ** 2))
                if c < best[0]:
                    best = (c, (float(f2), float(s1), float(sig[i2])))
    # best single Gaussian by the same measure, for the record
    c1 = [float(np.sum((np.log(np.maximum(h / h.sum(), 1e-12)) - ref) ** 2)) for h in H]
    return best, (float(sig[int(np.argmin(c1))]), float(min(c1)))


def tt_validation(files, par, rng, K=2):
    res = []; se = []
    for f in files:
        d = IO.load(f)
        o = M.apply(d['inp'], par, rng, K, return_met=True)
        # reco MET = -h ; true MET = neutrino sum
        dx = -o['hx'] - d['met'][:, 0:1]; dy = -o['hy'] - d['met'][:, 1:2]
        res.append(np.concatenate([dx, dy], 1)); se.append(d['sumet5'])
    res = np.concatenate(res); se = np.concatenate(se)
    out = []
    for c, ref in ATLAS:
        m = np.abs(se - c) < 0.2 * c
        nev = int(m.sum())
        if nev < 10:
            out.append(dict(sumet=c, n_events=nev, figure=ref, populated=False)); continue
        x = res[m].ravel(); s = float(np.sqrt(np.mean(x ** 2)))
        k = float(np.mean(x ** 4) / s ** 4); e = s * float(np.sqrt(max(k - 1, 0.1) / (4 * nev)))
        tol = float(np.hypot(ATLAS_TOL, e))
        out.append(dict(sumet=c, window=[0.8 * c, 1.2 * c], n_events=nev, model_rms=s, model_rms_err=e, figure=ref,
                        tolerance=tol, populated=nev >= ATLAS_MIN_EV, passes=bool(abs(s - ref) <= tol)))
        log.info('tt-bar sumET %.0f GeV: n %d  model RMS %.2f+-%.2f  figure %.1f  -> %s', c, nev, s, e, ref,
                 'pass' if out[-1]['passes'] else 'FAIL')
    edges = np.array([0, 300, 400, 500, 600, 800, 1000, 1300, 1600, 2000, 2500, 3200, 4500.])
    curve = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (se >= a) & (se < b)
        if m.sum() >= 200:
            curve.append(dict(lo=a, hi=b, n=int(m.sum()), rms=float(np.sqrt(np.mean(res[m] ** 2))),
                              mean_sumet=float(se[m].mean())))
    pop = [o for o in out if o.get('populated')]
    return dict(points=out, curve=curve, n_events=int(len(se)), sumet_quantiles=np.quantile(se, [.05, .5, .95]).tolist(),
                RA_passes=bool(pop and all(o['passes'] for o in pop)), n_points_populated=len(pop))


def main(argv):
    outd = Path(argv[0]); outd.mkdir(parents=True, exist_ok=True)
    files = {a.split('=')[0]: a.split('=')[1].split(',') for a in argv[1:]}
    rng = np.random.default_rng(20261124)
    inp, qx, qy, n_gen = zmm_arrays(files['zmm'])
    q = np.hypot(qx, qy); sel30 = q > 30.0
    log.info('Z->mumu: %d generated, %d with two prompt muons pT > 10 |eta| < 2.8, %d with pT(Z) > 30', n_gen, len(q),
             int(sel30.sum()))
    # ---- sigma_soft from the u_perp target: sigma_soft^2 = target^2 - V_perp(model without S)
    p0 = dict(M.NOMINAL, sigma_soft=0.0)
    up0, ut0, _ = recoil(inp, qx, qy, p0, rng)
    vperp = float(np.mean(ut0[sel30] ** 2) - np.mean(ut0[sel30]) ** 2)
    vpar = float(np.mean(up0[sel30] ** 2) - np.mean(up0[sel30]) ** 2)
    model = dict(v_perp_no_soft=vperp, v_par_no_soft=vpar, u_perp_targets=UPERP_TARGETS,
                 sigma_soft={k: float(np.sqrt(t ** 2 - vperp)) for k, t in UPERP_TARGETS.items()},
                 n_zmm=int(len(q)), n_zmm_pt30=int(sel30.sum()), source='CMS NOTE-2018/006 Fig. 35 right (u_perp), '
                 'mean PU density 1.4 /mm; sigma_soft^2 = target^2 - V_perp')
    log.info('V_perp without soft term %.1f GeV^2 (rms %.2f GeV), V_par %.1f (rms %.2f) -> sigma_soft %s', vperp,
             np.sqrt(vperp), vpar, np.sqrt(vpar), {k: round(v, 2) for k, v in model['sigma_soft'].items()})
    (c2, mix), (s1, c1) = fit_mixture(inp, qx, qy, M.NOMINAL, rng)
    model['soft_mix_fit34'] = list(mix); model['soft_mix_fit34_cost'] = c2
    model['best_single_gaussian_fig34'] = dict(sigma=s1, cost=c1)
    log.info('mixture fitted to Fig. 34: f2 %.2f, sigma1 %.0f, sigma2 %.0f (cost %.3f); best single Gaussian %.0f GeV '
             '(cost %.3f)', *mix, c2, s1, c1)
    (outd / 'model.json').write_text(json.dumps(model, indent=1) + '\n')
    # ---- R-B on the nominal and on the declared variants (each with its own numbers; nominal is not changed)
    val = dict(reading_RB={}, declared='phase3_selection/logs/executor_birgit_2026-11-24_10-16.md §P4')
    variants = {'nominal': M.params('nominal', model), 'soft_dn_25': M.params('soft_dn', model),
                'soft_up_32.5': M.params('soft_up', model), 'tail_dn': M.params('tail_dn', model),
                'tail_up': M.params('tail_up', model), 'core_up': M.params('core_up', model),
                'core_dn': M.params('core_dn', model),
                'remed_density': dict(M.params('nominal', model), soft_density=True),
                'remed_mixture_fig34': M.params('soft_mix', model),
                'remed_single_bestfit34': dict(M.params('nominal', model), sigma_soft=s1)}
    for name, par in variants.items():
        val['reading_RB'][name] = summarise(name, inp, qx, qy, par, rng, sel30)
    # ---- R-A
    if 'tt' in files:
        val['reading_RA'] = {name: tt_validation(files['tt'], variants[name], rng)
                             for name in ('nominal', 'soft_up_32.5', 'remed_mixture_fig34')}
    val['verdicts'] = dict(RB=val['reading_RB']['nominal']['RB_passes'],
                           RA=val.get('reading_RA', {}).get('nominal', {}).get('RA_passes'))
    (outd / 'validation.json').write_text(json.dumps(val, indent=1) + '\n')
    log.info('verdicts (nominal): %s', val['verdicts'])


if __name__ == '__main__':
    main(sys.argv[1:])
