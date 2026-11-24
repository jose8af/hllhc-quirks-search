"""metmodel.py -- the reconstruction-level MET model of B4-b (STR §4.7), work package p3-c (executor Birgit).

Definition, sources and pre-declared variations: `phase3_selection/logs/executor_birgit_2026-11-24_10-16.md` §P2-P3 and
the artifact `outputs/P3C_MET_MODEL_birgit_2026-11-24.md` §2.  numpy only (runs in the acts environment and anywhere).

  MET_reco = | -( sum_jets R_j pT_j + sum_{reconstructed prompt e, mu} pT + U_true + S ) |

Parameter sources (CMS NOTE-2018/006, printed pages; readings of SEB §1.5 [ESTIMATE, +-0.01 / +-1 GeV]):
  JER      Fig. 25 p. 16   sigma(pT/pT_gen) vs pT_gen, |eta| < 1.3, 1.3-1.7, 1.7-2.8, PF+PUPPI, PU 200
  soft     Fig. 35 p. 21   u_perp width at the mean PU density 1.4 /mm (target; sigma_soft is derived from it, see
                           p3c_validate.py), range 25 GeV (text p. 19) to 32.5 GeV (highest density point)
  leptons  p. 7, Fig. 10 p. 8, Fig. 13 p. 9 (e); Fig. 17 p. 11 (mu)
  JES/JER  Table 1 p. 29 (variations)
  tail     NOT SOURCED for Phase 2 (retrieval_log #14, #20, #32-#36); size anchored on arXiv:1607.03663 §8.3 (Run 1)
Trigger: CERN-LHCC-2020-004 Fig. 3.125 p. 188 (readings of phase2_exploration/outputs/s2/trigger_turnon.json).
"""
import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[2]
TRIG_JSON = QV2 / 'phase2_exploration' / 'outputs' / 's2' / 'trigger_turnon.json'

# --- Fig. 25 readings (pT_gen [GeV], sigma) per |eta| bin; SEB §1.5.  Ranges read as intervals enter at their middle.
JER_ETA_EDGES = np.array([1.3, 1.7])                  # bins: < 1.3, 1.3-1.7, >= 1.7 (used up to 4.7: extrapolation)
JER_TAB = [
    np.array([(30, .23), (50, .18), (60, .16), (80, .14), (100, .13), (130, .12), (170, .107), (250, .09), (350, .077),
              (480, .067)]),
    np.array([(30, .27), (50, .185), (80, .18), (100, .17), (150, .155), (250, .15), (450, .1475)]),
    np.array([(30, .27), (50, .22), (80, .18), (100, .175), (150, .165), (250, .155), (450, .17)]),
]
JET_PT_MIN = 30.0            # lower edge of Fig. 25; jets below are part of U_true
JET_ETA_MAX = 4.7
LEP_PT_MIN = 10.0
JMAX, LMAX = 12, 4

NOMINAL = dict(
    jer_scale=1.0, jer_shift=0.0,      # sigma -> jer_scale * sigma + jer_shift
    jes=1.0,
    f_tail=0.015, k_tail=3.0,          # NOT SOURCED (see module docstring)
    f_tail_prop=None,                  # numerical only: proposal tail probability for importance sampling
    sigma_soft=None,                   # GeV per component; set from soft_target by p3c_validate.py (model.json)
    soft_mix=None,                     # None or (f2, sigma1, sigma2): two-Gaussian soft term (variation)
    soft_density=False,                # sigma_soft scaled with the PU density (remediation variant, not nominal)
    lost_electron_in_sum=False,        # False: STR literal (every lost lepton left out of the sum)
    met_cut=250.0, jet_cut=100.0, jet_eta=2.4, mindphi=0.5,
    trig='fig3125',                    # 'fig3125' | 'erf_shifted' (user's option (b) nuisance) | 'none'
    veto_gamma_w=0.05,                 # v1 value (gen_d123.VETO_INEFF), not sourced
)

# pre-declared variations (log §P3); each is a dict of changes to NOMINAL (sigma_soft entries are targets of u_perp)
VARIATIONS = {
    'nominal': {},
    'core_up': dict(jer_scale=1.05, jer_shift=0.01), 'core_dn': dict(jer_scale=0.95, jer_shift=-0.01),
    'jes_up': dict(jes=1.025), 'jes_dn': dict(jes=0.975),
    'soft_up': dict(soft_target=32.5), 'soft_dn': dict(soft_target=25.0),
    'tail_up': dict(f_tail=0.03, k_tail=5.0), 'tail_dn': dict(f_tail=0.0),
    'soft_mix': dict(soft_mix='fit34'),
    'lost_e_kept': dict(lost_electron_in_sum=True),
    'all_up': dict(jer_scale=1.05, jer_shift=0.01, soft_target=32.5, f_tail=0.03, k_tail=5.0),
    'all_dn': dict(jer_scale=0.95, jer_shift=-0.01, soft_target=25.0, f_tail=0.0),
}


def jer_sigma(pt, eta):
    """Fig. 25: linear in ln pT between the read points, constant outside; |eta| >= 1.7 bin used up to 4.7."""
    pt = np.asarray(pt, float); ae = np.abs(np.asarray(eta, float))
    ib = np.digitize(ae, JER_ETA_EDGES)
    out = np.zeros_like(pt)
    lp = np.log(np.maximum(pt, 1e-3))
    for b, tab in enumerate(JER_TAB):
        m = ib == b
        if m.any():
            out[m] = np.interp(lp[m], np.log(tab[:, 0]), tab[:, 1])
    return out


def eff_lepton(pdg, pt, eta):
    """Reconstruction + identification probability of a prompt e / mu (0 outside the acceptance)."""
    a = np.abs(np.asarray(pdg)); pt = np.asarray(pt, float); ae = np.abs(np.asarray(eta, float))
    e_end = np.interp(pt, [10.0, 40.0], [0.65, 0.97])
    eps_e = np.where(ae < 1.4, 0.975, np.where(ae < 3.0, e_end, 0.0))
    eps_m = np.where(ae < 2.0, 0.97, np.where(ae < 2.8, 0.995, 0.0))
    return np.where(a == 11, eps_e, np.where(a == 13, eps_m, 0.0))


_TRIG = None


def trig_eff(met, kind='fig3125'):
    """L1 MET turn-on evaluated at MET_reco.  'fig3125': digitised curve; 'erf_shifted': the erf through Table 4.1
    (50 % at 128, 90 % at 200 GeV) with the 50 % point shifted up by one width (COM l.366, option (b))."""
    global _TRIG
    met = np.asarray(met, float)
    if kind == 'none':
        return np.ones_like(met)
    if _TRIG is None:
        d = json.loads(TRIG_JSON.read_text())
        r = np.array(d['fig3125_readings'], float)
        _TRIG = (r[:, 0], np.clip(r[:, 1], 0.0, 1.0))
    if kind == 'fig3125':
        return np.interp(met, _TRIG[0], _TRIG[1], left=_TRIG[1][0], right=1.0)
    if kind == 'erf_shifted':
        sig = (200.0 - 128.0) / 1.2815515655446004          # z(0.9); 56.18 GeV as EDG §2.6
        z = (met - (128.0 + sig)) / (sig * math.sqrt(2))
        return 0.5 * (1 + np.vectorize(math.erf)(z))
    raise ValueError(kind)


def dphi(a, b):
    return (a - b + np.pi) % (2 * np.pi) - np.pi


def build_inputs(evt_px5, evt_py5, jets, jet_off, lep, lep_off):
    """Summaries (pilot or p3c_gen layout) -> padded model inputs.
    jets (J, >=3): pT, eta, phi; lep (L, 6): pdg, pT, eta, phi, iso, prompt.
    Prompt e/mu with pT > 10 GeV are taken out of the jets (vector subtraction from a jet within dR < 0.4)."""
    n = len(evt_px5)
    jp = np.zeros((n, JMAX, 3)); jm = np.zeros((n, JMAX), bool)
    lp = np.zeros((n, LMAX, 5)); lm = np.zeros((n, LMAX), bool)        # pdg, pt, eta, phi, iso_ok
    ngam = np.zeros(n)
    jets = np.asarray(jets, float); lep = np.asarray(lep, float)
    for i in range(n):
        J = jets[jet_off[i]:jet_off[i + 1], :3].copy()
        L = lep[lep_off[i]:lep_off[i + 1]]
        if len(L):
            a = np.abs(L[:, 0])
            g = (a == 22) & (L[:, 5] > 0.5) & (L[:, 1] > 15.0) & (np.abs(L[:, 2]) < 2.5) & (L[:, 4] < 0.2 * L[:, 1])
            ngam[i] = g.sum()
            sel = L[((a == 11) | (a == 13)) & (L[:, 5] > 0.5) & (L[:, 1] > LEP_PT_MIN)]
            sel = sel[np.argsort(-sel[:, 1])][:LMAX]
            for k, l in enumerate(sel):
                lp[i, k] = (l[0], l[1], l[2], l[3], float(l[4] < 0.2 * l[1])); lm[i, k] = True
                if len(J):
                    dr = np.hypot(J[:, 1] - l[2], dphi(J[:, 2], l[3]))
                    j = int(np.argmin(dr))
                    if dr[j] < 0.4:
                        px = J[j, 0] * math.cos(J[j, 2]) - l[1] * math.cos(l[3])
                        py = J[j, 0] * math.sin(J[j, 2]) - l[1] * math.sin(l[3])
                        J[j, 0] = math.hypot(px, py); J[j, 2] = math.atan2(py, px)
        if len(J):
            J = J[(J[:, 0] >= JET_PT_MIN) & (np.abs(J[:, 1]) < JET_ETA_MAX)]
            J = J[np.argsort(-J[:, 0])][:JMAX]
            jp[i, :len(J)] = J; jm[i, :len(J)] = True
    jx = (jp[:, :, 0] * np.cos(jp[:, :, 2]) * jm).sum(1); jy = (jp[:, :, 0] * np.sin(jp[:, :, 2]) * jm).sum(1)
    lx = (lp[:, :, 1] * np.cos(lp[:, :, 3]) * lm).sum(1); ly = (lp[:, :, 1] * np.sin(lp[:, :, 3]) * lm).sum(1)
    ux = np.asarray(evt_px5, float) - jx - lx; uy = np.asarray(evt_py5, float) - jy - ly      # U_true
    return dict(jp=jp, jm=jm, lp=lp, lm=lm, ngam=ngam, ux=ux, uy=uy)


def apply(inp, par, rng, n_throw=1, return_met=False, density=None):
    """Apply the model.  Returns dict with w (n, K) event weights (eps_trig x preselection x vetoes) and, if
    return_met, the reconstructed sums.  `par` = NOMINAL updated with a variation and a numeric sigma_soft."""
    jp, jm, lp, lm = inp['jp'], inp['jm'], inp['lp'], inp['lm']
    n, K = len(jp), n_throw
    pt = jp[:, None, :, 0]; eta = jp[:, None, :, 1]; phi = jp[:, None, :, 2]; m = jm[:, None, :]
    sig = np.maximum(par['jer_scale'] * jer_sigma(jp[:, :, 0], jp[:, :, 1]) + par['jer_shift'], 0.0)[:, None, :]
    R = 1.0 + sig * rng.standard_normal((n, K, JMAX))
    if par['f_tail'] > 0:
        t = rng.random((n, K, JMAX)) < par['f_tail']
        R = np.where(t, 1.0 - np.abs(par['k_tail'] * sig * rng.standard_normal((n, K, JMAX))), R)
    iw = None
    if par['f_tail'] > 0 and par.get('f_tail_prop'):
        # importance sampling of the tail state: drawn with f_tail_prop, weighted back to f_tail (exact reweighting)
        fp, f = par['f_tail_prop'], par['f_tail']
        t2 = rng.random((n, K, JMAX)) < fp
        R = np.where(t2, 1.0 - np.abs(par['k_tail'] * sig * rng.standard_normal((n, K, JMAX))),
                     1.0 + sig * rng.standard_normal((n, K, JMAX)))
        iw = np.where(m, np.where(t2, f / fp, (1 - f) / (1 - fp)), 1.0).prod(2)
    R = np.maximum(R, 0.0) * par['jes']
    rmin = np.where(m, R, 9.0).min(2)                  # diagnostic: lowest response among the model jets
    ptr = np.where(m, R * pt, 0.0)
    sx = (ptr * np.cos(phi)).sum(2); sy = (ptr * np.sin(phi)).sum(2)
    # leptons
    eps = eff_lepton(lp[:, :, 0], lp[:, :, 1], lp[:, :, 2]) * lm
    rec = rng.random((n, K, LMAX)) < eps[:, None, :]
    lpx = (lp[:, :, 1] * np.cos(lp[:, :, 3]))[:, None, :]; lpy = (lp[:, :, 1] * np.sin(lp[:, :, 3]))[:, None, :]
    keep = rec
    if par['lost_electron_in_sum']:
        keep = rec | ((np.abs(lp[:, :, 0]) == 11) & lm)[:, None, :]
    sx = sx + (keep * lpx).sum(2); sy = sy + (keep * lpy).sum(2)
    veto = (rec & ((lp[:, :, 1] > LEP_PT_MIN) & (np.abs(lp[:, :, 2]) < 2.5) & (lp[:, :, 4] > 0.5))[:, None, :]).any(2)
    # soft term
    if par.get('soft_mix'):
        f2, s1, s2 = par['soft_mix']
        s = np.where(rng.random((n, K)) < f2, s2, s1)
    else:
        s = np.full((n, K), float(par['sigma_soft']))
    if par.get('soft_density'):
        # sigma(rho)/sigma(1.4) from the dotted line of Fig. 35 right (25.0 + 3.75 rho); rho = 1.98 exp(-x^2/2)
        rho = 1.98 * np.exp(-0.5 * rng.standard_normal((n, K)) ** 2) if density is None else density
        s = s * (25.0 + 3.75 * rho) / (25.0 + 3.75 * 1.4)
    nx = s * rng.standard_normal((n, K)); ny = s * rng.standard_normal((n, K))
    hx = sx + inp['ux'][:, None] + nx; hy = sy + inp['uy'][:, None] + ny          # reconstructed visible sum
    met = np.hypot(hx, hy); phim = np.arctan2(-hy, -hx)
    # preselection on reconstructed jets
    lead = (m & (ptr > par['jet_cut']) & (np.abs(eta) < par['jet_eta'])).any(2)
    ptr_s = np.where(ptr > JET_PT_MIN, ptr, -1.0)
    order = np.argsort(-ptr_s, axis=2)[:, :, :4]
    p4 = np.take_along_axis(ptr_s, order, 2); f4 = np.take_along_axis(np.broadcast_to(phi, ptr.shape), order, 2)
    dp = np.where(p4 > 0, np.abs(dphi(f4, phim[:, :, None])), 9.0).min(2)
    ok = (met > par['met_cut']) & lead & (dp > par['mindphi']) & ~veto
    w = ok * trig_eff(met, par['trig']) * (par['veto_gamma_w'] ** inp['ngam'])[:, None]
    if iw is not None:
        w = w * iw
    out = dict(w=w, iw=iw)
    if return_met:
        out.update(hx=hx, hy=hy, met=met, jx=sx, jy=sy, nx=nx, ny=ny, lead=lead, mindphi=dp, veto=veto, rmin=rmin)
    return out


def params(variation='nominal', model=None):
    """Parameter set of a named variation.  `model` = contents of outputs/p3c/model.json (sigma_soft per target,
    fitted mixture)."""
    p = dict(NOMINAL); v = dict(VARIATIONS[variation])
    tgt = v.pop('soft_target', None)
    if v.get('soft_mix') == 'fit34':
        v['soft_mix'] = tuple(model['soft_mix_fit34']) if model else None
    p.update(v)
    if model is not None:
        key = 'nominal' if tgt is None else f'{tgt:g}'
        p['sigma_soft'] = model['sigma_soft'][key]
    return p
