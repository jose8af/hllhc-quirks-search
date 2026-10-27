"""T4_fisher_report.py -- tables and figures from the T4_fisher.py Jacobians.

Reads figures/T4_fisher_<m>_<lam>.pkl and prints
  (1) model-validation residuals per layer (Q1): first-order B effect |y_B - y_vac|, second-order remainder
      |y_B - y_vac - 20 (y_{B/20} - y_vac)|, mean-energy-loss shift |y_E - y_B|, MS sigma (thin scatterers), resolution;
  (2) degeneracy analysis of the vacuum Fisher matrix (eigenvectors of the smallest eigenvalues);
  (3) Cramer-Rao resolutions per event (median) and for an ensemble of N events (sum of per-event Schur complements
      on (ln m, ln Lambda)) for the measurement configurations listed in CONFIGS;
  (4) linearised prediction windows per layer given the hits on the layers inside it (Q4b / Q5).
Inputs (UNVERIFIED where marked in the report): resolutions in T4_model (SIG_RPHI, SIG_Z); MTD BTL sigma_t = 35 ps;
IT dE/dx 25 % per hit; MET resolution 25 GeV per component; PV z0 30 um; material-scale prior 10 %.
Output: printed tables; figures/T4_fisher_summary.png; figures/T4_fisher_summary.npz.
Run: pixi run python code/T4_fisher_report.py [sigma_met_GeV]
"""
import os, sys, pickle, glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import SIG_RPHI, SIG_Z, SENS_NAMES, PNAMES, UNAMES, momenta, theta_to_nat, dtheta_dnat  # noqa: E402
from T2_propagator import C_CM_PER_NS, sigma_from_lambda_keV  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
SIG_T = 35e-3 * C_CM_PER_NS       # 35 ps in cm
SIG_E = 0.25
SIG_MET = float(sys.argv[1]) if len(sys.argv) > 1 else 25.0
SIG_Z0 = 30e-4
SIG_MAT = 0.10
MASSES = [200, 500, 1000]
LAMS = [1.0, 3.0, 10.0]

# name: (jacobian set, measurement types, use MS cov, priors)
CONFIGS = {
    'P0 vacuum, positions':                 ('vac', 'rz', False, ()),
    'P1 B, positions (no MS)':              ('B', 'rz', False, ()),
    'P2 B, positions + MS':                 ('B', 'rz', True, ()),
    'P3 P2 + mean dE/dx loss model':        ('E', 'rz', True, ('mat',)),
    'M1 P2 + MET + PV':                     ('B', 'rz', True, ('met', 'pv')),
    'M2 M1 + BTL timing':                   ('B', 'rzt', True, ('met', 'pv')),
    'M3 M2 + IT dE/dx':                     ('B', 'rzte', True, ('met', 'pv')),
    'M4 M3 + eloss model':                  ('E', 'rzte', True, ('met', 'pv', 'mat')),
    'T1 B, pos+MS + BTL + dE/dx (no MET)':  ('B', 'rzte', True, ('pv',)),
}


def sig_of(kk):
    L, typ = kk[1], kk[3]
    return {'r': SIG_RPHI[L], 'z': SIG_Z[L], 't': SIG_T, 'e': SIG_E}[typ]


def fisher(o, cfg, natural=False):
    jset, types, use_ms, priors = CONFIGS[cfg]
    J = o['J'][jset]
    if jset == 'E':
        # Exact scaling (Sec. 2.1): at fixed (l0, velocities) the mean energy loss depends on mat_scale/m_Q only, so
        # its part of d y/d ln sigma equals -d y/d ln(mat_scale).  The finite-difference ln-sigma step was tuned on the
        # (much smaller) pure-B response and is non-linear for the mm-scale energy-loss phase shifts, so the column is
        # rebuilt from the B-only column and the mat_scale column (step 0.05, linear).
        J = dict(J)
        J[8] = {k: o['J']['B'][8][k] - J[9][k] for k in J[9] if k in o['J']['B'][8]}
    npar = len(J)
    keys = None
    for i in range(npar):
        ks = set(J[i])
        keys = ks if keys is None else keys & ks
    if use_ms:
        for col in o['Jxi']:
            keys &= set(col)
    keys = sorted(k for k in keys if k[3] in types and np.isfinite(sig_of(k)))
    if len(keys) < 12:
        return None, keys, None, None
    A = np.array([[J[i][k] for i in range(npar)] for k in keys])
    C = np.diag([sig_of(k) ** 2 for k in keys])
    if use_ms and o['Jxi']:
        X = np.array([[col[k] for col in o['Jxi']] for k in keys])
        C = C + X @ X.T
    Ci = np.linalg.inv(C)
    Iu = A.T @ Ci @ A                       # Fisher in natural parameters u (T4_model.UNAMES)
    th = o['theta']; pt = np.exp(th[1])
    th_full = np.r_[th, 1.0] if npar > 9 else th
    Dinv = np.linalg.inv(dtheta_dnat(theta_to_nat(th_full)))
    I = Dinv.T @ Iu @ Dinv                  # Fisher in physical parameters theta (T4_model.PNAMES)
    if natural:
        return Iu, keys, A, C
    if 'met' in priors:
        I[1, 1] += (pt / SIG_MET) ** 2
        I[2, 2] += (pt / SIG_MET) ** 2
    if 'pv' in priors:
        I[0, 0] += 1 / SIG_Z0 ** 2
    if 'mat' in priors and npar > 9:
        I[9, 9] += 1 / SIG_MAT ** 2
    return I, keys, A, C


def schur(I, a=(7, 8)):
    a = list(a)
    b = [i for i in range(I.shape[0]) if i not in a]
    Ibb = I[np.ix_(b, b)]
    return I[np.ix_(a, a)] - I[np.ix_(a, b)] @ np.linalg.pinv(Ibb, rcond=1e-14) @ I[np.ix_(b, a)]


def cov_from(I):
    try:
        w = np.linalg.eigvalsh(I)
        if w.min() <= w.max() * 1e-15:
            return None
        return np.linalg.inv(I)
    except np.linalg.LinAlgError:
        return None


def load(m, lam):
    fn = os.path.join(FIG, f'T4_fisher_{m}_{lam:g}.pkl')
    if not os.path.exists(fn):
        return None
    with open(fn, 'rb') as f:
        return pickle.load(f)


def q(v, qs=(0.16, 0.5, 0.84)):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    return np.quantile(v, qs) if len(v) else [np.nan] * 3


def validation(data):
    print('\n=== (1) Model-validation residuals per layer [um]: 68% quantile of |delta| over events/hits ===')
    print('cols: layer | |B-vac| | 2nd-order(B) | |eloss shift| | sigma_MS | sigma_res')
    rows = {}
    for (m, lam), D in sorted(data.items()):
        per = {L: dict(B=[], nl=[], E=[], ms=[], Bz=[], nlz=[], msz=[]) for L in range(10)}
        for o in D:
            yv, yB, yBs, yE = o['y']['vac'], o['y']['B'], o['y']['Bs'], o['y']['E']
            msvar = {}
            for col in o['Jxi']:
                for k, v in col.items():
                    msvar[k] = msvar.get(k, 0.0) + v * v
            for k, v in yB.items():
                if k[3] not in 'rz':
                    continue
                L = k[1]
                t = '' if k[3] == 'r' else 'z'
                if k in yv and k in yBs:
                    per[L]['B' if not t else 'Bz'].append(v - yv[k])
                    per[L]['nl' if not t else 'nlz'].append(v - yv[k] - 20 * (yBs[k] - yv[k]))
                if k in yE and not t:
                    per[L]['E'].append(yE[k] - v)
                if k in msvar:
                    per[L]['ms' if not t else 'msz'].append(np.sqrt(msvar[k]))
        # robust spread: 68 % quantile of |delta| (a few near-tangent hits change their crossing index between runs
        # and would dominate an RMS)
        rms = lambda a: np.quantile(np.abs(a), 0.68) * 1e4 if len(a) else np.nan  # noqa: E731
        print(f'-- m = {m} GeV, Lambda = {lam:g} keV ({len(D)} events)')
        rows[(m, lam)] = {}
        for L in range(10):
            p = per[L]
            r = (rms(p['B']), rms(p['nl']), rms(p['E']), rms(p['ms']), SIG_RPHI[L] * 1e4,
                 rms(p['Bz']), rms(p['nlz']), rms(p['msz']), SIG_Z[L] * 1e4)
            rows[(m, lam)][L] = r
            print(f'   {SENS_NAMES[L]:4s} rphi: B {r[0]:9.1f} | nonlin {r[1]:8.2f} | eloss {r[2]:8.1f} | MS {r[3]:7.1f} | '
                  f'res {r[4]:5.1f}   z: B {r[5]:8.1f} nonlin {r[6]:7.2f} MS {r[7]:7.1f} res {r[8]:7.0f}')
    return rows


def degeneracy(data):
    print('\n=== (2) Natural-parameter Fisher: what positions alone measure (per-event median sigma) ===')
    print('    u = ' + ', '.join(UNAMES) + '; ln sigma column norm relative to the largest column')
    for (m, lam), D in sorted(data.items()):
        for cfg in ('P0 vacuum, positions', 'P2 B, positions + MS', 'T1 B, pos+MS + BTL + dE/dx (no MET)'):
            sig8 = []; rel = []
            for o in D:
                Iu, *_ = fisher(o, cfg, natural=True)
                if Iu is None:
                    continue
                rel.append(np.sqrt(Iu[8, 8] / np.max(np.diag(Iu))))
                cv = np.linalg.inv(Iu[:8, :8])          # fixing ln sigma (vacuum symmetry direction)
                sig8.append(np.sqrt(np.diag(cv)))
            s8 = np.median(sig8, axis=0)
            print(f'm={m} L={lam:g} {cfg[:24]:24s}: |col ln sigma|/max = {np.median(rel):.1e}; sigma(u | ln sigma fixed): '
                  + ', '.join(f'{UNAMES[i]} {s8[i]:.2g}' for i in range(8)))


def resolutions(data):
    print(f'\n=== (3) Cramer-Rao resolutions (sigma_MET = {SIG_MET} GeV/component) ===')
    res = {}
    for (m, lam), D in sorted(data.items()):
        print(f'-- m = {m} GeV, Lambda = {lam:g} keV, {len(D)} events. Columns: per-event median [16-84%] '
              f'sigma(m)/m, sigma(L)/L, sigma(pT)/pT, rho(m,L) ; ensemble N=10/30/100: sigma(m)/m, sigma(L)/L')
        for cfg in CONFIGS:
            sm, sl, sp, rh = [], [], [], []
            shared_mat = 'mat' in CONFIGS[cfg][3]
            # the material scale is ONE global nuisance shared by all events: keep it in the Schur complement and
            # add its prior once for the ensemble (otherwise the prior would be counted N times)
            Ssum = np.zeros((3, 3)) if shared_mat else np.zeros((2, 2))
            for o in D:
                I, *_ = fisher(o, cfg)
                if I is None:
                    continue
                if shared_mat:
                    I0 = I.copy(); I0[9, 9] -= 1 / SIG_MAT ** 2
                    S = schur(I0, a=(7, 8, 9))
                else:
                    S = schur(I)
                Ssum += S
                cv = cov_from(I)
                if cv is None:
                    sm.append(np.inf); sl.append(np.inf); sp.append(np.inf); rh.append(np.nan)
                else:
                    sm.append(np.sqrt(cv[7, 7])); sl.append(np.sqrt(cv[8, 8])); sp.append(np.sqrt(cv[1, 1]))
                    rh.append(cv[7, 8] / np.sqrt(cv[7, 7] * cv[8, 8]))
            Smean = Ssum / len(D)
            ens = {}
            for N in (10, 30, 100):
                SN = Smean * N
                if shared_mat:
                    SN = SN.copy(); SN[2, 2] += 1 / SIG_MAT ** 2
                cv = cov_from(SN)
                ens[N] = (np.sqrt(cv[0, 0]), np.sqrt(cv[1, 1])) if cv is not None else (np.inf, np.inf)
            res[(m, lam, cfg)] = dict(sm=q(sm), sl=q(sl), sp=q(sp), rho=np.nanmedian(rh) if np.isfinite(rh).any() else np.nan, ens=ens)
            f = lambda x: f'{x:.2g}' if np.isfinite(x) else 'inf'  # noqa: E731
            qq = lambda a: f'{f(a[1])} [{f(a[0])}-{f(a[2])}]'  # noqa: E731
            r = res[(m, lam, cfg)]
            print(f'   {cfg:38s} m: {qq(r["sm"]):24s} L: {qq(r["sl"]):24s} pT: {qq(r["sp"]):22s} rho {r["rho"]:+.2f} | '
                  + ' '.join(f'N={N}: {f(ens[N][0])}/{f(ens[N][1])}' for N in ens))
    return res


def prediction(data):
    """Linearised predictive width of the hits at layer L given hits at layers < L (config M1 priors + broad priors)."""
    print('\n=== (4) Predictive r*phi window (1 sigma, um) at layer L from the fit to layers < L, vs quirk separation ===')
    broad = np.array([SIG_Z0, 0, 0, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0])
    out = {}
    for (m, lam), D in sorted(data.items()):
        per = {L: ([], []) for L in range(1, 10)}
        for o in D:
            I, keys, A, C = fisher(o, 'M1 P2 + MET + PV', natural=True)
            if I is None:
                continue
            th = o['theta']; pt = np.exp(th[1])
            pr = broad.copy(); pr[1] = 0.3; pr[2] = SIG_MET / pt      # natural-parameter priors (A is d y / d u)
            P = np.diag(pr ** 2)
            Sig = A @ P @ A.T + C
            Ls = np.array([k[1] for k in keys]); typ = np.array([k[3] for k in keys])
            yB = o['y']['B']
            for L in range(1, 10):
                a = np.where(Ls < L)[0]; b = np.where((Ls == L) & (typ == 'r'))[0]
                if len(a) < 4 or len(b) == 0:
                    continue
                Saa = Sig[np.ix_(a, a)]; Sab = Sig[np.ix_(a, b)]; Sbb = Sig[np.ix_(b, b)]
                cond = Sbb - Sab.T @ np.linalg.solve(Saa, Sab)
                sp = np.sqrt(np.clip(np.diag(cond), 0, None))
                per[L][0].extend(sp)
                # quirk separation at this layer (first crossings)
                k0, k1 = (0, L, 1, 'r'), (1, L, 1, 'r')
                if k0 in yB and k1 in yB:
                    per[L][1].append(abs(yB[k0] - yB[k1]))
        out[(m, lam)] = {L: (np.median(per[L][0]) * 1e4 if per[L][0] else np.nan,
                             np.median(per[L][1]) * 1e4 if per[L][1] else np.nan) for L in per}
        print(f'm={m} L={lam:g}: ' + ' '.join(f'{SENS_NAMES[L]} {out[(m, lam)][L][0]:.0f}/{out[(m, lam)][L][1]:.0f}'
                                               for L in range(1, 10)))
    return out


def figure(res, val):
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.6))
    cfgs = ['P2 B, positions + MS', 'M1 P2 + MET + PV', 'M3 M2 + IT dE/dx', 'M4 M3 + eloss model']
    cols = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    for j, m in enumerate(MASSES):
        ax = axs[j]
        for c, cfg in zip(cols, cfgs):
            ym = [res.get((m, lam, cfg), {}).get('ens', {}).get(30, (np.nan, np.nan))[0] for lam in LAMS]
            yl = [res.get((m, lam, cfg), {}).get('ens', {}).get(30, (np.nan, np.nan))[1] for lam in LAMS]
            ax.loglog(LAMS, ym, 'o-', color=c, label=f'σ(m)/m  {cfg}')
            ax.loglog(LAMS, yl, 's--', color=c, label=f'σ(Λ)/Λ  {cfg}')
        ax.set_title(f'm_Q = {m} GeV, N = 30 events (Cramér-Rao)', fontsize=10)
        ax.set_xlabel('Λ [keV]'); ax.set_ylabel('relative resolution')
        ax.grid(alpha=0.3, which='both')
        if j == 0:
            ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, 'T4_fisher_summary.png'), dpi=130)


def main():
    data = {}
    for m in MASSES:
        for lam in LAMS:
            D = load(m, lam)
            if D:
                data[(m, lam)] = D
    val = validation(data)
    degeneracy(data)
    res = resolutions(data)
    pred = prediction(data)
    figure(res, val)
    np.savez(os.path.join(FIG, 'T4_fisher_summary.npz'), res=np.array([res], dtype=object),
             val=np.array([val], dtype=object), pred=np.array([pred], dtype=object))


if __name__ == '__main__':
    main()
