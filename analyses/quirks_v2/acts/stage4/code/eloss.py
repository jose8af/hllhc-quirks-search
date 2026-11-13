"""code/eloss.py -- numpy re-implementation of the Fatras ionisation-loss model (G1, 2026-10-13; pure numpy + scipy,
importable in both envs: acts env `import eloss`, TT env `acts.stage4.code.eloss`).  Review WP_RULE R1 B-2.

Why: PU and muon-gun hits carry Fatras' Landau-sampled loss in the SURFACE MATERIAL SLAB that s4geo decorates the sensor
with (e.g. TBPX 1.2 % X0 = 1.124 mm Si-equivalent, a stacked OT layer's x/X0 split over its two sensors), times the
path correction 1/|cos(incidence)|.  Stage-3 h_dE is the MEAN Bethe loss in the 0.15/0.20 mm ACTIVE Si, without
fluctuation.  For a shared dE/dx unit the quirk deposit must come from the same model on the same slab:

  dE = loc + scale * L,  L ~ standard Landau (scipy.stats.landau; ActsFatras::LandauDistribution),
  loc   = Acts::computeEnergyLossLandau(slab, m, q/p, |q|)       (RPP2018 eq. 33.11, the most probable value)
  scale = Acts::computeEnergyLossLandauSigma(...) = 4 eps / (2 sqrt(2 ln 2))   (Landau FWHM 4 eps -> Gaussian sigma)
  eps   = (K/2) N_e x q^2/beta^2,  N_e = Z * molar density [mol/mm^3],  K = 0.307075 MeV cm^2/mol
  ACTS mean excitation energy I = 16 eV * Z^0.9; density correction delta/2 = ln(beta gamma) + ln(hbar w_p / I) - 1/2
  for beta gamma >= 10 (else 0), hbar w_p = 28.816 eV sqrt(1000 N_e)  [ActsFatras BetheBloch, Acts Interactions.cpp]
Bethe mean (for the V4-1 mean-consistency check against h_dE): Acts::computeEnergyLossBethe (RPP2018 eq. 33.5).
This module is validated, not tuned: closure = the numpy sampler applied to Fatras muon-gun truth hits must reproduce
the Fatras muon-gun deposits (G1_REPORT, V4-9 / F-2).
"""
import numpy as np
from scipy.stats import landau

ME = 0.5109989461e-3          # GeV
K = 0.307075e-3 * 100.0       # GeV mm^2 / mol
PLASMA = 28.816e-9            # GeV
SI_X0, SI_Z, SI_MOLAR = 93.7, 14.0, 0.0831e-3      # s4geo.SI (mm, Z, mol/mm^3)
FWHM_TO_SIGMA = 1.0 / (2.0 * np.sqrt(2.0 * np.log(2.0)))


def _rq(m, p, q=1.0):
    q = np.abs(q)
    mop = m / np.maximum(p, 1e-300)              # m/p (|q/p|/|q| = 1/p)
    beta2 = 1.0 / (1.0 + mop * mop)
    bg = 1.0 / mop
    gamma = np.sqrt(1.0 + bg * bg)
    q2ob2 = q * q + (m * q / p) ** 2               # q^2 + m^2 (q/p)^2
    return q2ob2, beta2, bg, gamma


def _mat(Z=SI_Z, molar=SI_MOLAR):
    Ne = Z * molar
    I = 16e-9 * Z ** 0.9
    return Ne, I


def _delta_half(bg, Ne, I):
    wp = PLASMA * np.sqrt(1000.0 * Ne)
    return np.where(bg < 10.0, 0.0, np.log(np.maximum(bg, 1e-300)) + np.log(wp / I) - 0.5)


def landau_params(thickness, m, p, q=1.0, Z=SI_Z, molar=SI_MOLAR):
    """(loc, scale) [GeV] of the Fatras Landau for a slab of `thickness` mm (path length already included)."""
    Ne, I = _mat(Z, molar)
    q2ob2, beta2, bg, gamma = _rq(m, p, q)
    eps = 0.5 * K * Ne * thickness * q2ob2
    t = 2.0 * ME * bg * bg
    run = np.log(t / I) + np.log(eps / I) + 0.2 - beta2 - 2.0 * _delta_half(bg, Ne, I)
    return eps * run, 4.0 * eps * FWHM_TO_SIGMA


def bethe_mean(thickness, m, p, q=1.0, Z=SI_Z, molar=SI_MOLAR):
    Ne, I = _mat(Z, molar)
    q2ob2, beta2, bg, gamma = _rq(m, p, q)
    eps = 0.5 * K * Ne * thickness * q2ob2
    u = 2.0 * ME * bg * bg
    mf = ME / m
    wmax = 2.0 * ME * bg * bg / (1.0 + 2.0 * gamma * mf + mf * mf)
    run = 0.5 * np.log(u / I) + 0.5 * np.log(wmax / I) - beta2 - _delta_half(bg, Ne, I)
    return 2.0 * eps * run


# scipy.stats.landau is the stable-law parametrisation, NOT the CERNLIB/ROOT standard Landau phi(lambda) that
# ActsFatras::LandauDistribution samples (CERNLIB G110 ranlan).  Verified numerically (G1): lambda = (pi/2) x_scipy + C0,
# with the scipy mode at x = -0.4293148 mapped to the CERNLIB mode -0.2227830 (quantile ratios 1.5709-1.5716 at
# q = 0.1-0.9; CERNLIB median 1.3561).  Without this map the sampler was x0.64 too narrow vs the Fatras deposits.
SCIPY_MODE = -0.4293147964
CERN_MODE = -0.2227830
C0 = CERN_MODE - 0.5 * np.pi * SCIPY_MODE


def std_landau_quantile(u01):
    """CERNLIB/ROOT standard Landau quantile (as ActsFatras::LandauDistribution::quantile)."""
    return 0.5 * np.pi * landau.ppf(u01) + C0


def sample(thickness, m, p, u01, q=1.0):
    """Fatras-model deposit for uniform draws u01 in (0, 1) (one per hit; the caller seeds them per hit):
    location + scale * lambda, lambda ~ CERNLIB Landau (ActsFatras BetheBloch).  Fatras applies no floor; a negative
    draw (P ~ 1e-6 at these eps) is floored at 0 here."""
    loc, sc = landau_params(thickness, m, p, q)
    u01 = np.clip(u01, 1e-12, 1.0 - 1e-12)
    return np.maximum(loc + sc * std_landau_quantile(u01), 0.0)


def slab_thickness(sid, surfs, dmat=None, mat_scale=1.0):
    """Fatras slab thickness [mm] of Stage-3 surface `sid` (s4geo.surface_xX0 x Si X0); 0 for BTL/ETL/T3V."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import json
    tt = Path(__file__).resolve().parents[3]
    if dmat is None:
        d = json.loads((tt / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json').read_text())
        dmat = {mm['name']: mm['xX0'] for mm in d['disc_material']}
    s = surfs[sid]
    k, n = s['kind'], s['name']
    if k in ('BTL', 'ETL', 'T3V'):
        return 0.0
    barrel = {'IT': 0.012, 'PS': 0.025, '2S': 0.018}
    nsens = 2 if (n.endswith('_in') or n.endswith('_out')) else 1
    if s['type'] == 0:
        x = barrel[k]
    else:
        key = n.replace('_p', '').replace('_n', '').replace('_in', '').replace('_out', '')
        x = dmat.get(key, barrel[k])
    return mat_scale * x / nsens * SI_X0


def path_factor(sid_type, x, y, px, py, pz):
    """1/|cos(incidence)|: cylinder normal = radial, disc normal = z."""
    pa = np.sqrt(px * px + py * py + pz * pz)
    r = np.hypot(x, y)
    c_cyl = np.abs(x * px + y * py) / np.maximum(r * pa, 1e-300)
    c_disc = np.abs(pz) / np.maximum(pa, 1e-300)
    c = np.where(np.asarray(sid_type) == 0, c_cyl, c_disc)
    return 1.0 / np.maximum(c, 1e-3)
