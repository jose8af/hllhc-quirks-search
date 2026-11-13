"""T2_kinematics.py -- distributions of quirk oscillation length, oscillations in the CMS tracker and
crossing time for Drell-Yan quirk pairs at sqrt(s) = 14 TeV (theory track, investigator T2).

Physics model (parton level, LO, ESTIMATE quality; stated in the report Sec. 3):
  * PDFs: CT18NLO central member, LHAPDF lhagrid1 file read directly (no LHAPDF library).
    Path: env T2_PDF (default: data/pdf/CT18NLO).  Download:
    https://lhapdfsets.web.cern.ch/current/CT18NLO.tar.gz  ->  CT18NLO/CT18NLO_0000.dat
  * Quirk = vector-like SU(2)-singlet, charge -1 ("E"; fermion F or scalar S), gamma*/Z couplings
    as in research/theory_signal_model.md App. A (alpha = 1/127.9, sW2 = 0.2222).
  * Inclusive sample: LO q qbar -> gamma*/Z -> QQbar, pT(QQ) = 0, mu_F = M.
  * ISR sample: q qbar -> V*(M) g and q g -> V*(M) q (and qbar g) 2->2 matrix elements
      |M|^2(qqbar->V*g) = (8/9) (t^2+u^2+2 s M^2)/(t u),  |M|^2(q(a)g(b)->V*q) = -(1/3) (s^2+t^2+2 u M^2)/(s t)
    times the V*(M) -> QQbar line shape  C_q(M) R(beta)/M^2  (R_F = beta(3-beta^2)/2, R_S = beta^3/4),
    alpha_s(mu) one-loop with alpha_s(MZ)=0.118, mu_F = mu_R = m_T(V*).  Cut pT(QQ) > 200 GeV.
  * Decay angle in the pair rest frame w.r.t. the Collins-Soper axis: F: 2 - beta^2 sin^2(theta),
    S: sin^2(theta) (exact for the inclusive LO case; an approximation for V*+jet).
Outputs:
  * l_max (exact CM max separation (M-2m)/sigma), lab max transverse separation (exact, T2_propagator),
    number of oscillations inside r < 110 cm, |z| < 270 cm (exact: crossings every 2p*(beta gamma)/sigma
    along the pair line of flight; 1 oscillation = 2 crossings), lab time between crossings 2p* gamma/sigma.
  * figures/T2_lmax_distributions.png, figures/T2_nosc_tracker.png, figures/T2_isr_assumptions.png
  * table printed to stdout (copied into the report).
Run:  pixi run python code/T2_kinematics.py   (about 1-2 minutes)
"""
import os
import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import sigma_from_lambda_keV, C_CM_PER_NS

PDF_PATH = os.environ.get('T2_PDF', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'pdf', 'CT18NLO', 'CT18NLO_0000.dat'))
# large intermediate cache (~170 MB): kept in theory_track/data/cache/ (env T2_CACHE overrides)
CACHE = os.environ.get('T2_CACHE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cache', 'T2_kinematics_cache.npz'))
FIGDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
SQRTS = 14000.0
R_TRK, Z_TRK = 110.0, 270.0
LAMS = [0.3, 1.0, 3.0, 10.0, 30.0]
MASSES = [200.0, 500.0, 1000.0]
rng = np.random.default_rng(12345)


class PDF:
    def __init__(self, path):
        txt = open(path).read().split('---')
        self.blocks = []
        for b in txt[1:]:
            lines = [l for l in b.strip().split('\n') if l.strip()]
            if len(lines) < 4:
                continue
            xs = np.array(lines[0].split(), float); qs = np.array(lines[1].split(), float)
            fl = [int(v) for v in lines[2].split()]
            vals = np.array(' '.join(lines[3:]).split(), float).reshape(len(xs), len(qs), len(fl))
            sp = {f: RectBivariateSpline(np.log(xs), np.log(qs ** 2), vals[:, :, i], kx=3, ky=3)
                  for i, f in enumerate(fl)}
            self.blocks.append((qs[0], qs[-1], xs[0], sp))

    def xf(self, fl, x, q):
        x = np.asarray(x, float); q = np.minimum(np.asarray(q, float) * np.ones_like(x), self.blocks[-1][1])
        out = np.zeros_like(x)
        done = np.zeros(x.shape, bool)
        for qmin, qmax, xmin, sp in self.blocks:
            sel = (~done) & (q >= qmin) & (q <= qmax)
            if sel.any() and fl in sp:
                out[sel] = sp[fl].ev(np.log(np.clip(x[sel], xmin, 1.0)), np.log(q[sel] ** 2))
            done |= sel
        return np.where(x < 1, np.maximum(out, 0.0), 0.0)


ALPHA, SW2, MZ, GZ = 1 / 127.9, 0.2222, 91.1876, 2.4952
sw, cw = np.sqrt(SW2), np.sqrt(1 - SW2)
QUARKS = {1: (-0.5, -1 / 3), 2: (0.5, 2 / 3), 3: (-0.5, -1 / 3), 4: (0.5, 2 / 3), 5: (-0.5, -1 / 3)}
VE = (0.0 - 2 * (-1.0) * SW2) / (2 * sw * cw)


def coupling(q, M2):
    """gamma*/Z coupling factor V_q(M) for q qbar -> E Ebar (vector-like E, a_E = 0)."""
    T3, Qq = QUARKS[q]
    vq = (T3 - 2 * Qq * SW2) / (2 * sw * cw); aq = T3 / (2 * sw * cw)
    chi = M2 / (M2 - MZ ** 2 + 1j * MZ * GZ)
    return Qq ** 2 + 2 * Qq * (-1.0) * vq * VE * chi.real + (vq ** 2 + aq ** 2) * VE ** 2 * np.abs(chi) ** 2


def Rbeta(beta, spin):
    return beta * (3 - beta ** 2) / 2 if spin == 'F' else beta ** 3 / 4


def alphas(mu):
    b0 = (33 - 2 * 5) / (12 * np.pi)
    return 0.118 / (1 + 0.118 * b0 * np.log(mu ** 2 / MZ ** 2))


def sample_inclusive(pdf, m, spin, n=300000):
    S = SQRTS ** 2
    lt0 = np.log(4 * m * m / S)
    lt = rng.uniform(lt0, 0, n); tau = np.exp(lt)
    lx1 = rng.uniform(lt, 0); x1 = np.exp(lx1); x2 = tau / x1
    M2 = tau * S; M = np.sqrt(M2)
    beta = np.sqrt(np.clip(1 - 4 * m * m / M2, 0, 1))
    w = np.zeros(n)
    for q in QUARKS:
        lum = (pdf.xf(q, x1, M) * pdf.xf(-q, x2, M) + pdf.xf(-q, x1, M) * pdf.xf(q, x2, M)) / (x1 * x2)
        w += lum * coupling(q, M2)
    w *= Rbeta(beta, spin) / M2 * tau * (-lt0) * (-lt)
    y = 0.5 * np.log(x1 / x2)
    return dict(M=M, pT=np.zeros(n), y=y, phi=rng.uniform(0, 2 * np.pi, n), w=w)


def sample_isr(pdf, m, spin, n=600000, ptmin=200.0):
    S = SQRTS ** 2; rs = SQRTS
    Mmax = min(rs - 2 * ptmin, 2 * m + 4000)
    lM = rng.uniform(np.log(2 * m), np.log(Mmax), n); M = np.exp(lM)
    lpt = rng.uniform(np.log(ptmin), np.log(2500.0), n); pT = np.exp(lpt)
    yV = rng.uniform(-3.5, 3.5, n); yj = rng.uniform(-5.0, 5.0, n)
    mT = np.sqrt(M ** 2 + pT ** 2)
    x1 = (mT * np.exp(yV) + pT * np.exp(yj)) / rs
    x2 = (mT * np.exp(-yV) + pT * np.exp(-yj)) / rs
    ok = (x1 < 1) & (x2 < 1)
    s = x1 * x2 * S
    t = M ** 2 - x1 * rs * mT * np.exp(-yV)
    u = M ** 2 - x2 * rs * mT * np.exp(yV)
    M2 = M ** 2
    beta = np.sqrt(np.clip(1 - 4 * m * m / M2, 0, 1))
    mu = mT
    A_qq = (8 / 9) * (t ** 2 + u ** 2 + 2 * s * M2) / (t * u)          # q(x1) qbar(x2) -> V g
    # crossing of qqbar->Vg (b <-> gluon): q(a) g(b) -> V q gives -(s^2 + t^2 + 2 u M^2)/(s t) with
    # t = (p_a - q)^2, u = (p_b - q)^2 as defined above; g(a) q(b) is the a<->b mirror (t <-> u).
    A_qg = -(1 / 3) * (s ** 2 + t ** 2 + 2 * u * M2) / (s * t)          # q(x1) g(x2) -> V q
    A_gq = -(1 / 3) * (s ** 2 + u ** 2 + 2 * t * M2) / (s * u)          # g(x1) q(x2) -> V q
    w = np.zeros(n)
    g1 = pdf.xf(21, x1, mu) / x1; g2 = pdf.xf(21, x2, mu) / x2
    for q in QUARKS:
        cq = coupling(q, M2)
        fq1 = pdf.xf(q, x1, mu) / x1; fa1 = pdf.xf(-q, x1, mu) / x1
        fq2 = pdf.xf(q, x2, mu) / x2; fa2 = pdf.xf(-q, x2, mu) / x2
        w += cq * ((fq1 * fa2 + fa1 * fq2) * A_qq + (fq1 + fa1) * g2 * A_qg + g1 * (fq2 + fa2) * A_gq)
    # d sigma ~ x1 f1 x2 f2 |M|^2 / s^2  dyV dyj dpT^2  x  C R / M^2 dM^2 ; jacobians of log sampling
    w *= x1 * x2 / s ** 2 * alphas(mu) * Rbeta(beta, spin) / M2 * (2 * M * M) * (2 * pT * pT)
    w = np.where(ok & (beta > 0), w, 0.0)
    return dict(M=M, pT=pT, y=yV, phi=rng.uniform(0, 2 * np.pi, n), w=w)


def decay_and_observables(ev, m, spin):
    """Attach CM decay angle and compute lam-independent quantities."""
    M = ev['M']; n = len(M)
    beta = np.sqrt(np.clip(1 - 4 * m * m / M ** 2, 0, 1))
    # accept-reject cos theta (Collins-Soper) for the angular distribution
    ct = np.empty(n); todo = np.arange(n)
    while len(todo):
        c = rng.uniform(-1, 1, len(todo)); r = rng.uniform(0, 1, len(todo))
        if spin == 'F':
            acc = r * 2 <= (2 - beta[todo] ** 2 * (1 - c ** 2))
        else:
            acc = r <= (1 - c ** 2)
        ct[todo[acc]] = c[acc]; todo = todo[~acc]
    phis = rng.uniform(0, 2 * np.pi, n)
    # pair 4-momentum (lab): pT along azimuth phi, rapidity y
    mT = np.sqrt(M ** 2 + ev['pT'] ** 2)
    E = mT * np.cosh(ev['y']); pz = mT * np.sinh(ev['y'])
    px = ev['pT'] * np.cos(ev['phi']); py = ev['pT'] * np.sin(ev['phi'])
    P = np.stack([px, py, pz], 1)
    bvec = P / E[:, None]
    bmag = np.linalg.norm(bvec, axis=1)
    g = E / M
    # Collins-Soper axis approximated by the pair direction for the angle relevant here:
    # we need cos(theta*) between the quirk axis n and the pair velocity.  For pT=0 pairs the CS axis
    # is the beam (= pair velocity direction).  For V+jet we use the CS axis built from the beams.
    zhat = np.array([0, 0, 1.0])
    # CS axis in the pair rest frame ~ bisector of beam directions; approximate by beam axis boosted:
    # angle between CS z and pair velocity in the rest frame: cos a = (pz-ish); compute exactly:
    pa = np.stack([np.zeros(n), np.zeros(n), np.ones(n)], 1)     # beam a direction (massless, E=1)
    def boost_to_rest(vec3, e, b):
        b2 = np.sum(b * b, 1); gg = 1 / np.sqrt(1 - b2)
        bp = np.sum(b * vec3, 1)
        coef = np.where(b2 > 0, (gg - 1) * bp / np.where(b2 > 0, b2, 1), 0) - gg * e
        return vec3 + coef[:, None] * b
    ka = boost_to_rest(pa, np.ones(n), bvec); kb = boost_to_rest(-pa, np.ones(n), bvec)
    ka /= np.linalg.norm(ka, axis=1)[:, None]; kb /= np.linalg.norm(kb, axis=1)[:, None]
    zcs = ka - kb; zcs /= np.linalg.norm(zcs, axis=1)[:, None]
    # random orthonormal completion
    tmp = np.where(np.abs(zcs[:, [0]]) < 0.9, np.array([[1.0, 0, 0]]), np.array([[0, 1.0, 0]]))
    e1 = np.cross(zcs, tmp); e1 /= np.linalg.norm(e1, axis=1)[:, None]; e2 = np.cross(zcs, e1)
    st = np.sqrt(1 - ct ** 2)
    nvec = ct[:, None] * zcs + (st * np.cos(phis))[:, None] * e1 + (st * np.sin(phis))[:, None] * e2
    bhat = np.where(bmag[:, None] > 0, bvec / np.where(bmag > 0, bmag, 1)[:, None], zhat)
    cstar = np.sum(nvec * bhat, 1)
    pstar = m * beta / np.sqrt(1 - beta ** 2)
    gstar = 1 / np.sqrt(1 - beta ** 2)
    # exact lab max transverse separation factor (T2_propagator.ExactPair.lab_max_separation), vectorised
    k = np.abs(bmag * cstar)
    u = np.zeros(n)
    for _ in range(60):     # fixed point u = k (g* - sqrt(1+u^2)), contraction since |k|<1
        u = k * (gstar - np.sqrt(1 + u * u))
    chord_fac = (gstar - np.sqrt(1 + u * u)) / (gstar - 1)        # <= 1
    # path length to leave the tracker cylinder along the pair direction
    sint = np.hypot(bvec[:, 0], bvec[:, 1]) / np.where(bmag > 0, bmag, 1)
    cost = np.abs(bvec[:, 2]) / np.where(bmag > 0, bmag, 1)
    with np.errstate(divide='ignore'):
        Sexit = np.minimum(np.where(sint > 0, R_TRK / sint, np.inf), np.where(cost > 0, Z_TRK / cost, np.inf))
    ev.update(beta_star=beta, gamma_star=gstar, pstar=pstar, cstar=cstar, chord_fac=chord_fac,
              bg_pair=g * bmag, g_pair=g, Sexit=Sexit, eta_pair=np.arctanh(np.clip(P[:, 2] / np.maximum(np.linalg.norm(P, axis=1), 1e-9), -0.999999, 0.999999)),
              betaT=np.hypot(bvec[:, 0], bvec[:, 1]))
    return ev


def per_lambda(ev, m, lam):
    sig = sigma_from_lambda_keV(lam)
    lmax = 2 * (ev['gamma_star'] - 1) * m / sig                       # cm
    ltrans = lmax * ev['chord_fac'] * np.sqrt(np.clip(1 - ev['cstar'] ** 2, 0, 1))
    D = 2 * ev['pstar'] * ev['bg_pair'] / sig                         # cm between crossings
    with np.errstate(divide='ignore', invalid='ignore'):
        ncross = np.where(D > 0, ev['Sexit'] / D, np.inf)
    dt = 2 * ev['pstar'] * ev['g_pair'] / sig / C_CM_PER_NS            # ns between crossings
    return dict(lmax=lmax, ltrans=ltrans, nosc=ncross / 2, dtc=dt)


def wq(v, w, qs=(0.16, 0.5, 0.84)):
    i = np.argsort(v); v = v[i]; c = np.cumsum(w[i]); c /= c[-1]
    return [v[min(np.searchsorted(c, q), len(v) - 1)] for q in qs]


def fmt(x):
    if not np.isfinite(x):
        return 'inf'
    if x >= 100:
        return f'{x:.3g}'
    if x >= 1:
        return f'{x:.2g}' if x < 10 else f'{x:.0f}'
    return f'{x:.2g}'


def lenfmt(cm):
    if cm >= 1:
        return f'{cm:.3g} cm'
    if cm >= 0.1:
        return f'{cm * 10:.3g} mm'
    return f'{cm * 1e4:.3g} µm'


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    pdf = PDF(PDF_PATH)
    samples = {}
    for spin in ('F', 'S'):
        for m in MASSES:
            inc = decay_and_observables(sample_inclusive(pdf, m, spin), m, spin)
            isr = decay_and_observables(sample_isr(pdf, m, spin), m, spin)
            samples[(spin, m, 'incl')] = inc
            samples[(spin, m, 'isr')] = isr
            for tag, ev in (('incl', inc), ('isr', isr)):
                w = ev['w']; neff = w.sum() ** 2 / np.sum(w ** 2)
                print(f'# spin={spin} m={m:.0f} {tag}: N_eff={neff:.0f}  gamma*(16/50/84)=' +
                      ' '.join(f'{v:.3f}' for v in wq(ev['gamma_star'], w)) +
                      '  beta*(50)=%.2f' % wq(ev['beta_star'], w)[1] +
                      '  (beta gamma)_pair(16/50/84)=' + ' '.join(f'{v:.3f}' for v in wq(ev['bg_pair'], w)) +
                      '  beta_T(50)=%.3f' % wq(ev['betaT'], w)[1] +
                      '  |cos theta*|(50)=%.2f' % wq(np.abs(ev['cstar']), w)[1] +
                      '  chord_fac(16)=%.4f' % wq(ev['chord_fac'], w)[0])
    # ---- main table ----
    print('\n## Table: fermion E, 14 TeV.  l_max (CM) | lab transverse width | N_osc (r<110cm,|z|<270cm) | dt between crossings')
    print('| m_Q | Λ [keV] | sel | l_max 16/50/84 | w_T,lab 50 | N_osc 16/50/84 | frac N_osc<1 | Δt_cross 50 [ns] |')
    print('|---|---|---|---|---|---|---|---|')
    for m in MASSES:
        for lam in LAMS:
            for tag in ('incl', 'isr'):
                ev = samples[('F', m, tag)]; w = ev['w']; o = per_lambda(ev, m, lam)
                if tag == 'isr':
                    sel = np.abs(ev['eta_pair']) < 2.5
                else:
                    sel = np.ones(len(w), bool)
                ww = w * sel
                lq = wq(o['lmax'], ww); nq = wq(o['nosc'], ww)
                f1 = ww[o['nosc'] < 1].sum() / ww.sum()
                print(f"| {m:.0f} | {lam} | {'incl. (pT=0)' if tag == 'incl' else 'pT>200, |η|<2.5'} | "
                      f"{lenfmt(lq[0])} / {lenfmt(lq[1])} / {lenfmt(lq[2])} | {lenfmt(wq(o['ltrans'], ww)[1])} | "
                      f"{fmt(nq[0])} / {fmt(nq[1])} / {fmt(nq[2])} | {f1:.2f} | {wq(o['dtc'], ww)[1]:.3g} |")
    # scalar summary
    print('\n## scalar Etilde: l_max median ratio S/F and N_osc median ratio S/F (pT>200)')
    for m in MASSES:
        evF = samples[('F', m, 'isr')]; evS = samples[('S', m, 'isr')]
        oF = per_lambda(evF, m, 1.0); oS = per_lambda(evS, m, 1.0)
        print(f'm={m:.0f}: l_max S/F = {wq(oS["lmax"], evS["w"])[1] / wq(oF["lmax"], evF["w"])[1]:.2f}; '
              f'N_osc S/F = {wq(oS["nosc"], evS["w"])[1] / wq(oF["nosc"], evF["w"])[1]:.2f}')
    # ---- ISR assumptions: inclusive vs fixed-pT(250) on LO kinematics vs true V+jet ----
    print('\n## ISR-boost assumptions (m=500, F, Λ=1 keV): medians')
    m = 500.0
    inc = samples[('F', m, 'incl')]; isr = samples[('F', m, 'isr')]
    o_inc = per_lambda(inc, m, 1.0); o_isr = per_lambda(isr, m, 1.0)
    # fixed pT=250 added to inclusive kinematics (theory_signal_model App. A method)
    fx = {k: v.copy() for k, v in inc.items()}
    fx['pT'] = np.full(len(fx['M']), 250.0)
    fx = decay_and_observables(fx, m, 'F')
    o_fx = per_lambda(fx, m, 1.0)
    for name, ev, o in (('inclusive pT=0', inc, o_inc), ('fixed pT=250 on LO (App.A)', fx, o_fx),
                        ('V*+jet pT>200', isr, o_isr)):
        w = ev['w']
        print(f'{name:28s}: gamma*={wq(ev["gamma_star"], w)[1]:.3f}  l_max={wq(o["lmax"], w)[1]:.2f} cm '
              f'(beta gamma)_pair={wq(ev["bg_pair"], w)[1]:.3f} beta_T={wq(ev["betaT"], w)[1]:.3f} '
              f'N_osc={wq(o["nosc"], w)[1]:.1f} pT(50)={wq(ev["pT"], w)[1]:.0f}')
    # ---- figures ----
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, m in zip(axes, MASSES):
        for spin, ls in (('F', '-'), ('S', '--')):
            for tag, col in (('incl', 'C0'), ('isr', 'C3')):
                ev = samples[(spin, m, tag)]; o = per_lambda(ev, m, 1.0)
                bins = np.logspace(-3, 2, 61)
                h, _ = np.histogram(o['lmax'], bins=bins, weights=ev['w'])
                h = h / h.sum()
                ax.step(bins[:-1], h, where='post', ls=ls, color=col,
                        label=f"{'fermion E' if spin == 'F' else 'scalar Ẽ'}, {'inclusive' if tag == 'incl' else 'pT(QQ̄)>200 GeV'}")
        ax.set_xscale('log'); ax.set_title(f'm_Q = {m:.0f} GeV, Λ = 1 keV')
        ax.set_xlabel('ℓ_max = (M_QQ̄ − 2m_Q)/Λ²  [cm]   (scale ∝ (1 keV/Λ)²)')
        ax.grid(alpha=0.3)
    axes[0].set_ylabel('fraction / bin'); axes[0].legend(fontsize=7)
    fig.suptitle('Exact CM oscillation length, LO Drell-Yan 14 TeV (CT18NLO), T2 ESTIMATE')
    fig.tight_layout(); fig.savefig(os.path.join(FIGDIR, 'T2_lmax_distributions.png'), dpi=130)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, m in zip(axes, MASSES):
        ev = samples[('F', m, 'isr')]; sel = np.abs(ev['eta_pair']) < 2.5
        for i, lam in enumerate(LAMS):
            o = per_lambda(ev, m, lam)
            bins = np.logspace(-2, 6, 81)
            h, _ = np.histogram(o['nosc'][sel], bins=bins, weights=ev['w'][sel]); h = h / h.sum()
            ax.step(bins[:-1], h, where='post', label=f'Λ = {lam} keV', color=f'C{i}')
        ax.axvline(1, color='k', lw=0.8, ls=':')
        ax.set_xscale('log'); ax.set_title(f'fermion E, m_Q = {m:.0f} GeV, pT(QQ̄)>200 GeV')
        ax.set_xlabel('oscillations inside r<1.1 m, |z|<2.7 m'); ax.grid(alpha=0.3)
    axes[0].set_ylabel('fraction / bin'); axes[0].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(FIGDIR, 'T2_nosc_tracker.png'), dpi=130)
    # ISR assumption figure
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for name, ev, o, col in (('inclusive (pT=0)', inc, o_inc, 'C0'), ('fixed pT=250 GeV on LO DY', fx, o_fx, 'C2'),
                             ('V*+jet, pT>200 GeV', isr, o_isr, 'C3')):
        h, b = np.histogram(ev['gamma_star'], bins=np.linspace(1, 3, 81), weights=ev['w']); axes[0].step(b[:-1], h / h.sum(), where='post', label=name, color=col)
        h, b = np.histogram(o['nosc'], bins=np.logspace(-1, 4, 81), weights=ev['w']); axes[1].step(b[:-1], h / h.sum(), where='post', label=name, color=col)
    axes[0].set_xlabel('γ* of each quirk in the pair CM'); axes[1].set_xscale('log')
    axes[1].set_xlabel('oscillations inside the tracker (Λ = 1 keV)')
    for a in axes:
        a.grid(alpha=0.3); a.legend(fontsize=8)
    fig.suptitle('m_Q = 500 GeV fermion E: effect of the ISR-boost model (T2 ESTIMATE)')
    fig.tight_layout(); fig.savefig(os.path.join(FIGDIR, 'T2_isr_assumptions.png'), dpi=130)
    np.savez_compressed(CACHE,
                        **{f'{s}_{int(m)}_{t}_{k}': v for (s, m, t), ev in samples.items()
                           for k, v in ev.items() if k in ('gamma_star', 'w', 'cstar', 'bg_pair', 'eta_pair')})
    print('figures written')
