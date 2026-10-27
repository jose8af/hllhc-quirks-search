"""T2_string_methods_B.py -- compare string-force prescriptions once an external force is present
(uniform 3.8 T solenoid field, no material).  Theory track, investigator T2 (input for T3).

Methods (all exact in vacuum, see T2_test_propagator.py):
  causal : CausalNullString  = port of the ATLAS Athena Quirks algorithm (exact Nambu-Goto dynamics for
           piecewise-null string data; conserves P_quirks + P_string - sum_i q_i x_i x B exactly).
  labSS  : LabStraightString = Kang-Luty force with s_hat along the lab-simultaneous separation
           (equivalent to the Li et al. prescription 2002.07503 Eq.VIII.3-4, which reduces to the
           lab-simultaneous direction; checked on the exact solution in the report).
  cmSS   : straight string in the instantaneous pair CM frame (quirk momenta), CM-simultaneous
           separation by extrapolation along CM velocities, KL force in CM, 4-force boosted back.
Observables per event: hits at CMS Phase-2 barrel radii (IT 3.0/6.1/10.4/14.6 cm, OT 24.9/37.2/52.3/
68.8/86.0/108.3 cm; ideal, no material), plane thickness d_min [1708.02243; 2002.07503 Eq.C.1],
max hit displacement relative to 'causal', and drift of the canonical momentum
  dP = P_quirks - P0 - sum_i q_i x_i x B  evaluated at crossings (exactly 0 +- string momentum for
  exact dynamics; a secular growth signals momentum non-conservation of the approximation).
Run: pixi run python code/T2_string_methods_B.py   (few minutes).  Output: table on stdout and
figures/T2_string_methods_B.png
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import (ExactPair, LabStraightString, CausalNullString, kang_luty_force, interp_track,
                           sigma_from_lambda_keV, EB_GEV_PER_CM_PER_T, plane_thickness, radius_crossings)

RADII = [3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3]
BZ = 3.8
Q = (1.0, -1.0)


def _boost(t, x, b):
    b2 = b @ b; g = 1 / np.sqrt(1 - b2); bx = b @ x
    return g * (t - bx), x + ((g - 1) * bx / b2 - g * t) * b


def _boostv(v, b):
    b2 = b @ b; g = 1 / np.sqrt(1 - b2); vb = v @ b
    vpar = vb / b2 * b
    return (vpar - b + (v - vpar) / g) / (1 - vb)


def _force_to_lab(F, v, b):
    gv = 1 / np.sqrt(1 - v @ v); K0 = gv * (F @ v); K = gv * F
    b2 = b @ b; g = 1 / np.sqrt(1 - b2); Kb = K @ b
    Kl = K + ((g - 1) * Kb / b2 + g * K0) * b
    vl = ((v @ b) / b2 * b + b + (v - (v @ b) / b2 * b) / g) / (1 + v @ b)
    return Kl * np.sqrt(1 - vl @ vl)


class CMStraightString(LabStraightString):
    def _rhs(self, t, y, sref):
        x1, p1, x2, p2 = y[0:3], y[3:6], y[6:9], y[9:12]
        m1, m2 = self.m
        E1 = np.sqrt(m1 ** 2 + p1 @ p1); E2 = np.sqrt(m2 ** 2 + p2 @ p2)
        b = (p1 + p2) / (E1 + E2); v1 = p1 / E1; v2 = p2 / E2
        t1s, x1s = _boost(t, x1, b); t2s, x2s = _boost(t, x2, b)
        v1s = _boostv(v1, b); v2s = _boostv(v2, b)
        tb = max(t1s, t2s)
        d = (x1s + v1s * (tb - t1s)) - (x2s + v2s * (tb - t2s))
        nd = np.linalg.norm(d)
        if nd > 1e-12:
            s = d / nd
        else:
            s = _boostv(sref, b); s /= np.linalg.norm(s)
        out = np.empty(12)
        for i, (x, v, vs, ss) in enumerate(((x1, v1, v1s, s), (x2, v2, v2s, -s))):
            F = _force_to_lab(kang_luty_force(vs, ss, self.sigma), vs, b)
            if self.fext is not None:
                F = F + self.fext(i, x, (p1, p2)[i], t)
            out[6 * i:6 * i + 3] = v; out[6 * i + 3:6 * i + 6] = F
        return out


def make_event(rng, m, gstar=1.28, pt=300.0):
    M = 2 * m * gstar
    phi = rng.uniform(0, 2 * np.pi); y = rng.uniform(-0.8, 0.8)
    mT = np.hypot(M, pt)
    P = np.array([pt * np.cos(phi), pt * np.sin(phi), mT * np.sinh(y)]); E = mT * np.cosh(y)
    ps = m * np.sqrt(gstar ** 2 - 1)
    c = rng.uniform(-1, 1); ph = rng.uniform(0, 2 * np.pi); s = np.sqrt(1 - c * c)
    n = np.array([s * np.cos(ph), s * np.sin(ph), c])
    b = P / E; g = E / M
    out = []
    for sgn in (1, -1):
        pv = sgn * ps * n; e = np.hypot(m, ps)
        bp = b @ pv; b2 = b @ b
        out.append(pv + ((g - 1) * bp / b2 + g * e) * b)
    return out[0], out[1], np.linalg.norm(b[:2])


def hits_from(t, X):
    return [h for h in radius_crossings(t, X, RADII)]


def run_event(m, lam, p1, p2, betaT, max_boost=1e-2):
    sig = sigma_from_lambda_keV(lam)
    Bv = np.array([0, 0, BZ])

    def fext(i, x, p, t):
        E = np.sqrt(m * m + p @ p)
        return Q[i] * EB_GEV_PER_CM_PER_T * np.cross(p / E, Bv)
    t_end = 112.0 / max(betaT, 1e-3) + 20
    res = {}
    tic = time.time()
    traj, mom = CausalNullString(m, sig, charges=Q, Bfield=Bv, max_boost=max_boost,
                                 first_length=1e-9).run(p1, p2, t_end)
    res['causal'] = dict(tracks=[(T[:, 0], T[:, 1:]) for T in traj])
    for name, cls in (('labSS', LabStraightString), ('cmSS', CMStraightString)):
        sol = cls(m, m, sig, fext=fext, rtol=1e-10).run(p1, p2, t_end)
        y = sol['y']
        res[name] = dict(tracks=[(sol['t'], y[:, 0:3]), (sol['t'], y[:, 6:9])], sol=sol)
        # canonical-momentum drift at the last crossing inside the tracker
        P0 = p1 + p2
        r = np.hypot(0.5 * (y[:, 0] + y[:, 6]), 0.5 * (y[:, 1] + y[:, 7]))
        tc = sol['tcross'][np.interp(sol['tcross'], sol['t'], r) < 108] if len(sol['tcross']) else []
        if len(tc):
            k = np.argmin(np.abs(sol['t'] - tc[-1])); yy = y[k]
            can = yy[3:6] + yy[9:12] - EB_GEV_PER_CM_PER_T * np.cross(Q[0] * yy[0:3] + Q[1] * yy[6:9], Bv)
            res[name]['dP'] = np.linalg.norm(can - P0); res[name]['ncross'] = len(tc)
        else:
            res[name]['dP'] = np.nan; res[name]['ncross'] = 0
    for name in res:
        hits = []
        for (t, X) in res[name]['tracks']:
            hits += [h[2] for h in hits_from(t, X)]
        res[name]['hits'] = np.array(hits)
        res[name]['d'] = plane_thickness(hits) if len(hits) >= 3 else np.nan
    # hit displacement vs causal (nearest hit on same layer, same quirk)
    for name in ('labSS', 'cmSS'):
        dmax = 0.0
        for k in (0, 1):
            hc = hits_from(*res['causal']['tracks'][k]); hs = hits_from(*res[name]['tracks'][k])
            for R in RADII:
                A = [h[2] for h in hc if h[0] == R]; Bh = [h[2] for h in hs if h[0] == R]
                if A and Bh:
                    for a in A:
                        dmax = max(dmax, min(np.linalg.norm(a - b) for b in Bh))
        res[name]['dhit'] = dmax
    res['time'] = time.time() - tic
    return res


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    rng = np.random.default_rng(7)
    m = 500.0
    rows = []
    print('| Λ [keV] | event | N_cross(tracker) | d_min causal [µm] | d_min labSS [µm] | d_min cmSS [µm] | max Δhit labSS [µm] | max Δhit cmSS [µm] | |ΔP_canon| labSS [MeV] | cmSS [MeV] |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    events = [make_event(rng, m) for _ in range(4)]
    for lam in (0.6, 1.0, 2.0, 5.0):
        for ie, (p1, p2, bT) in enumerate(events):
            r = run_event(m, lam, p1, p2, bT)
            row = (lam, ie, r['labSS']['ncross'], r['causal']['d'] * 1e4, r['labSS']['d'] * 1e4, r['cmSS']['d'] * 1e4,
                   r['labSS']['dhit'] * 1e4, r['cmSS']['dhit'] * 1e4, r['labSS']['dP'] * 1e3, r['cmSS']['dP'] * 1e3)
            rows.append(row)
            print('| %.1f | %d | %d | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g | %.3g |' % row, flush=True)
    rows = np.array(rows)
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T2_string_methods_B.npy'), rows)
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    for j, (lab, col) in enumerate((('causal (Athena port)', 'k'), ('lab-simultaneous straight string', 'C3'),
                                    ('CM straight string', 'C0'))):
        ax[0].scatter(rows[:, 0] * (1 + 0.03 * (j - 1)), rows[:, 3 + j], color=col, label=lab, s=18)
    lam = np.logspace(np.log10(0.5), np.log10(6), 50)
    ax[0].plot(lam, 1.16 * 5 * 3.8 / lam ** 4, 'k:', label='1.16 µm (m/100)(keV/Λ)⁴ B/T [1911.02223]')
    ax[0].set_xscale('log'); ax[0].set_yscale('log'); ax[0].set_xlabel('Λ [keV]'); ax[0].set_ylabel('plane thickness d_min [µm]')
    ax[0].legend(fontsize=7); ax[0].grid(alpha=0.3, which='both')
    ax[1].scatter(rows[:, 0] * 0.97, rows[:, 6], color='C3', label='lab-simultaneous straight', s=18)
    ax[1].scatter(rows[:, 0] * 1.03, rows[:, 7], color='C0', label='CM straight', s=18)
    ax[1].set_xscale('log'); ax[1].set_yscale('log'); ax[1].set_xlabel('Λ [keV]')
    ax[1].set_ylabel('max |hit(straight) − hit(causal)| [µm]'); ax[1].legend(fontsize=7); ax[1].grid(alpha=0.3, which='both')
    fig.suptitle('m_Q = 500 GeV, uniform 3.8 T, no material: string prescriptions vs exact causal NG (T2 ESTIMATE)')
    fig.tight_layout(); fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T2_string_methods_B.png'), dpi=130)
    print('done')
