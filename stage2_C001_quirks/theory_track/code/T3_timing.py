"""T3_timing.py -- hit arrival times of quirk pairs at the CMS Phase-2 barrel layers and the MTD BTL (Q4).

Inputs: T2 kinematics cache (LO DY + ISR, pT(QQ) > 200 GeV, weighted; T2_kinematics.py), fermion E, m in {200, 500, 1000}.
Method (ESTIMATE):
  (a) CM-only: the pair centre moves on a straight line (vacuum; energy loss in the tracker is < 0.3 GeV of
      >= 100 GeV kinetic energy, T3_propagator test) -> crossing time t = R / beta_T.  Delay (the quantity the
      CMSSW Phase-2 digitiser cuts on, STRATEGY_DRAFT C8): toa = t - |r|/c, |r| = sqrt(R^2 + z^2).
  (b) Full per-quirk exact vacuum world lines (T2 ExactPair, boosted yo-yo; exact in vacuum, T2 report Sec.2) for
      Lambda in {0.3, 1, 3} keV on a subsample: time of every crossing of each layer radius by each quirk.
      Above 3 keV the oscillation amplitude is < 5 mm and the per-hit time differs from (a) by < 0.2 ns.
  Windows: OT (PS, 2S) toa in (-12.5, 12.5) ns; IT [-5, 20) ns (CMSSW SiPhase2Digitizer defaults quoted in
  STRATEGY_DRAFT C8); BTL: no window applied (reported as delay distribution).
  Acceptance: barrel |z| < 20 cm (IT, UNVERIFIED), < 120 cm (OT, UNVERIFIED), BTL |eta| < 1.45.
Run: pixi run python code/T3_timing.py    (~2-4 min).  Output: tables on stdout, figures/T3_timing.png
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import ExactPair, sigma_from_lambda_keV, C_CM_PER_NS
from T3_propagator import load_cache, sample_events

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
LAYERS = [('IT1', 3.0, 20.), ('IT2', 6.1, 20.), ('IT3', 10.4, 20.), ('IT4', 14.6, 20.), ('PS1', 24.9, 120.), ('PS2', 37.2, 120.),
          ('PS3', 52.3, 120.), ('2S1', 68.8, 120.), ('2S2', 86.0, 120.), ('2S3', 108.3, 120.), ('BTL', 114.8, 114.8 * np.sinh(1.45))]
WIN = {'IT': (-5.0, 20.0), 'PS': (-12.5, 12.5), '2S': (-12.5, 12.5), 'BTL': (-1e9, 1e9)}


def wq(v, w, qs=(0.16, 0.5, 0.84)):
    i = np.argsort(v); v = v[i]; c = np.cumsum(w[i]); c /= c[-1]
    return [v[min(np.searchsorted(c, q), len(v) - 1)] for q in qs]


def cm_only(m, eta_max=1.5):
    c = load_cache(); key = f'F_{int(m)}_isr'
    w = c[key + '_w']; gs = c[key + '_gamma_star']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
    sel = np.abs(eta) < eta_max
    w, gs, bg, eta = w[sel], gs[sel], bg[sel], eta[sel]
    beta = bg / np.sqrt(1 + bg ** 2)
    bT = beta / np.cosh(eta)
    rows = {}
    for name, R, zmax in LAYERS:
        z = R * np.sinh(eta)
        acc = np.abs(z) < zmax
        t_ns = R / bT / C_CM_PER_NS
        toa = t_ns - np.sqrt(R * R + z * z) / C_CM_PER_NS
        lo, hi = WIN[name[:2] if name != 'BTL' else 'BTL']
        inwin = (toa > lo) & (toa < hi)
        rows[name] = dict(q=wq(toa[acc], w[acc]), lost=np.sum(w[acc & ~inwin]) / np.sum(w[acc]), acc=np.sum(w[acc]) / np.sum(w))
    return rows, (bT, w)


def per_quirk(m, lam, n=400, eta_max=1.5, rng=None):
    """Exact vacuum world lines; returns arrays of (layer index, toa [ns], delta vs CM toa [ns])."""
    rng = rng or np.random.default_rng(5)
    ev = sample_events(m, n, rng=rng, eta_max=eta_max)
    sig = sigma_from_lambda_keV(lam)
    out = []
    for (p1, p2, info) in ev:
        ex = ExactPair(p1, p2, m, m, sig)
        bT = np.hypot(ex.beta[0], ex.beta[1])
        tmax_lab = 1.25 * 120.0 / bT
        tc_max = tmax_lab / ex.gamma + 2 * ex.lmax
        nper = max(tc_max / ex.Tcm, 1.0)
        npts = int(min(4e5, 400 * nper + 2000))
        tc = np.linspace(0, tc_max, npts)
        x1, x2 = ex.x_cm(tc)
        for k, xs in enumerate((x1, x2)):
            t, X = ex._event_lab(tc, xs)
            r = np.hypot(X[:, 0], X[:, 1])
            for li, (name, R, zmax) in enumerate(LAYERS):
                s = np.sign(r - R)
                idx = np.where(s[:-1] * s[1:] < 0)[0]
                for i in idx:
                    f = (R - r[i]) / (r[i + 1] - r[i])
                    th = t[i] + f * (t[i + 1] - t[i]); zh = X[i, 2] + f * (X[i + 1, 2] - X[i, 2])
                    if abs(zh) > zmax:
                        continue
                    toa = (th - np.sqrt(R * R + zh * zh)) / C_CM_PER_NS
                    tcm = (R / bT - np.sqrt(R * R + (R * ex.beta[2] / bT) ** 2)) / C_CM_PER_NS
                    out.append((li, toa, toa - tcm, k, 1.0))   # events already drawn proportional to weight
    return np.array(out)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    print('(a) CM-only delay toa = t - |r|/c [ns], LO DY+ISR pT(QQ)>200 GeV, |eta_pair|<1.5; median (16-84%), and '
          'fraction of hits outside the CMSSW window (OT +-12.5 ns, IT [-5,20) ns)')
    print('| m_Q | ' + ' | '.join(n for n, _, _ in LAYERS) + ' |')
    print('|---|' + '---|' * len(LAYERS))
    allrows = {}
    for m in (200.0, 500.0, 1000.0):
        rows, (bT, w) = cm_only(m)
        allrows[m] = (rows, bT, w)
        print(f'| {m:.0f} | ' + ' | '.join(f"{rows[n]['q'][1]:.1f} ({rows[n]['q'][0]:.1f}-{rows[n]['q'][2]:.1f})" for n, _, _ in LAYERS) + ' |')
        print(f'| lost | ' + ' | '.join(f"{rows[n]['lost']:.2f}" if n != 'BTL' else '-' for n, _, _ in LAYERS) + ' |')
        print(f'  m={m:.0f}: beta_T quantiles (16/50/84) = {np.round(wq(bT, w), 3)}')
    print('\n(b) exact per-quirk hits (vacuum yo-yo): spread of toa about the CM value [ns], all crossings, median |dt|, 95% |dt|; '
          'lost fraction per layer group (IT / PS / 2S) vs CM-only')
    figdat = {}
    for m in (500.0, 1000.0):
        for lam in (0.3, 1.0, 3.0):
            A = per_quirk(m, lam, n=300)
            figdat[(m, lam)] = A
            dt = np.abs(A[:, 2]); w = A[:, 4]
            s = []
            for grp, lis in (('IT', [0, 1, 2, 3]), ('PS', [4, 5, 6]), ('2S', [7, 8, 9])):
                sel = np.isin(A[:, 0], lis)
                lo, hi = WIN[grp]
                lost = np.sum(w[sel & ~((A[:, 1] > lo) & (A[:, 1] < hi))]) / np.sum(w[sel])
                s.append(f'{grp} lost {lost:.2f}')
            nh = np.bincount(A[:, 0].astype(int), minlength=11)[:11] / 300.0
            s.append('hits/event per layer (IT1..2S3,BTL) = ' + ' '.join(f'{x:.1f}' for x in nh))
            print(f'm={m:.0f} Lambda={lam}: median|dt| = {np.median(dt):.3f} ns, 95% = {np.percentile(dt, 95):.2f} ns; ' + ', '.join(s), flush=True)
    # figure
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    cols = {200.0: '#1f77b4', 500.0: '#d62728', 1000.0: '#2ca02c'}
    Rs = [R for _, R, _ in LAYERS]
    for m, (rows, bT, w) in allrows.items():
        q = np.array([rows[n]['q'] for n, _, _ in LAYERS])
        ax[0].plot(Rs, q[:, 1], 'o-', color=cols[m], label=f'm_Q = {m:.0f} GeV (median)')
        ax[0].fill_between(Rs, q[:, 0], q[:, 2], color=cols[m], alpha=0.2)
    ax[0].axhline(12.5, color='k', ls='--', lw=1); ax[0].axhline(20, color='k', ls=':', lw=1)
    ax[0].text(2, 13.2, 'OT window +12.5 ns', fontsize=8); ax[0].text(2, 20.7, 'IT window +20 ns', fontsize=8)
    ax[0].set_xlabel('layer radius R [cm]'); ax[0].set_ylabel('toa = t - |r|/c [ns]'); ax[0].set_ylim(0, 60)
    ax[0].set_title('pair-CM delay, pT(QQ)>200 GeV, |eta|<1.5 (16-84% band)', fontsize=9); ax[0].legend(fontsize=8)
    for (m, lam), A in figdat.items():
        if m != 500.0:
            continue
        sel = A[:, 0] >= 7
        ax[1].hist(A[sel, 2], bins=np.linspace(-3, 3, 121), weights=A[sel, 4], histtype='step', density=True, label=f'Λ = {lam} keV')
    ax[1].set_xlabel('per-quirk toa minus CM toa [ns] (2S layers, m_Q = 500 GeV)'); ax[1].set_ylabel('density')
    ax[1].set_yscale('log'); ax[1].legend(fontsize=8); ax[1].set_title('effect of the oscillation on hit times', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'T3_timing.png'), dpi=130)
    print('figure written')
