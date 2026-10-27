"""T2_covariance_test.py -- Lorentz-covariance test of string-force prescriptions with an external field
(theory track, investigator T2).

Idea: an exact Nambu-Goto treatment is frame independent.  Take a pair produced at rest (p2 = -p1 along x)
in a uniform transverse electric field E0 z (rest frame), solve in that frame, and Lorentz-transform the
trajectories to a 'lab' in which the pair moves with velocity beta along y (or x); in the lab the fields are
E = gamma E0 z, B = gamma beta y x E0 (field transformation).  Then solve directly in the lab with each
method and compare with the transformed rest-frame solution.  A method whose lab solution disagrees with
its own (or the causal) rest-frame solution is not Lorentz covariant at O(F_ext).
Methods: causal null-vector string (Athena port), lab-simultaneous straight string (labSS, ~ Li et al.),
straight string in the instantaneous CM of the quirks (cmSS), and in the true conserved CM (trueCM).
Run: pixi run python code/T2_covariance_test.py
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import (CausalNullString, LabStraightString, kang_luty_force, interp_track,
                           sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T)
from T2_string_methods_B import CMStraightString, _boost, _boostv, _force_to_lab

m = 500.0; sig = sigma_from_lambda_keV(1.0); gs = 1.3
ps = m * np.sqrt(gs ** 2 - 1)
E0 = 1e-4 * sig
Q = (1.0, -1.0)


def to_lab(T4, u):
    """rest-frame events (N,4) -> lab events, rest frame moving with velocity u (3-vector) in the lab."""
    g = 1 / np.sqrt(1 - u @ u); t = T4[:, 0]; x = T4[:, 1:]
    ux = x @ u; u2 = u @ u
    tl = g * (t + ux)
    xl = x + np.outer((g - 1) * ux / u2 + g * t, u)
    return np.c_[tl, xl]


def fields_lab(u):
    g = 1 / np.sqrt(1 - u @ u)
    Erest = np.array([0, 0, E0])
    upar = (Erest @ u) / (u @ u) * u
    El = upar + g * (Erest - upar)
    Bl_GeVcm = g * np.cross(u, Erest)                    # in GeV/cm per unit charge (c=1)
    return El, Bl_GeVcm / EB_GEV_PER_CM_PER_T            # B in tesla


def boost_p(p, u):
    """momentum of a particle with rest-frame momentum p (mass m) seen in the lab."""
    E = np.sqrt(m * m + p @ p); g = 1 / np.sqrt(1 - u @ u); pu = p @ u
    return p + ((g - 1) * pu / (u @ u) + g * E) * u


def solve(method, p1, p2, E, B, t_end):
    if method == 'causal':
        traj, _ = CausalNullString(m, sig, charges=Q, Efield=E, Bfield=B, max_boost=2e-3, first_length=1e-9).run(p1, p2, t_end)
        return traj
    def fext(i, x, p, t):
        v = p / np.sqrt(m * m + p @ p)
        return Q[i] * (E + EB_GEV_PER_CM_PER_T * np.cross(v, B))
    cls = LabStraightString if method == 'labSS' else CMStraightString
    sol = cls(m, m, sig, fext=fext, rtol=1e-11).run(p1, p2, t_end)
    return [np.c_[sol['t'], sol['y'][:, 0:3]], np.c_[sol['t'], sol['y'][:, 6:9]]]


if __name__ == '__main__':
    T = 4 * ps / sig
    p1r = np.array([ps, 0, 0.]); p2r = -p1r
    rest = {meth: solve(meth, p1r, p2r, np.array([0, 0, E0]), np.zeros(3), 3.2 * T) for meth in ('causal', 'labSS')}
    print('rest frame: max|z1-z2| causal %.3g um, straight %.3g um, max diff %.3g um' % (
        1e4 * np.max(np.abs(interp_track(rest['causal'][0], np.linspace(0, 3 * T, 3000))[:, 2] - interp_track(rest['causal'][1], np.linspace(0, 3 * T, 3000))[:, 2])),
        1e4 * np.max(np.abs(interp_track(rest['labSS'][0], np.linspace(0, 3 * T, 3000))[:, 2] - interp_track(rest['labSS'][1], np.linspace(0, 3 * T, 3000))[:, 2])),
        1e4 * np.max(np.abs(interp_track(rest['causal'][0], np.linspace(0, 3 * T, 3000)) - interp_track(rest['labSS'][0], np.linspace(0, 3 * T, 3000))))))
    print('| boost | method | max |x_lab(method) - Λ·x_rest(causal)| [µm] | max |x_lab(method) - Λ·x_rest(same method)| [µm] | out-of-plane (z) part [µm] |')
    print('|---|---|---|---|---|')
    for bdir, beta in (('y', 0.6), ('x', 0.6), ('y', 0.9)):
        u = beta * (np.array([0, 1.0, 0]) if bdir == 'y' else np.array([1.0, 0, 0]))
        El, Bl = fields_lab(u)
        p1, p2 = boost_p(p1r, u), boost_p(p2r, u)
        g = 1 / np.sqrt(1 - beta ** 2)
        t_end = 2.5 * T * g
        ref = [to_lab(rest['causal'][k], u) for k in (0, 1)]
        tt = np.linspace(0.02 * t_end, 0.98 * t_end, 2500)
        for meth in ('causal', 'labSS', 'cmSS'):
            lab = solve(meth, p1, p2, El, Bl, t_end)
            own = [to_lab(rest['causal' if meth == 'causal' else 'labSS'][k], u) for k in (0, 1)]
            d_ref = max(np.max(np.linalg.norm(interp_track(lab[k], tt) - interp_track(ref[k], tt), axis=1)) for k in (0, 1))
            d_own = max(np.max(np.linalg.norm(interp_track(lab[k], tt) - interp_track(own[k], tt), axis=1)) for k in (0, 1))
            d_z = max(np.max(np.abs(interp_track(lab[k], tt)[:, 2] - interp_track(ref[k], tt)[:, 2])) for k in (0, 1))
            print(f'| β={beta} along {bdir} | {meth} | {d_ref * 1e4:.3g} | {d_own * 1e4:.3g} | {d_z * 1e4:.3g} |', flush=True)
