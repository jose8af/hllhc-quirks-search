"""T4_local.py -- local hit-pattern signatures for seeding and triggering (Q4c, Q5).

Per LO DY+ISR event (T2 cache, pT(QQ) > 200 GeV, |eta| < 1, fermion E), causal-string model (T4_model, 3.8112 T, no
material), m_Q in {200, 500, 1000} GeV, Lambda in {0.3, 1, 3, 10} keV.  Computes:
  (1) Delta N_osc between consecutive barrel layers, N(r) = sigma r / (2 beta* pT) [T2 Sec.2.2] (closed form);
  (2) OT stub bend: hits on pseudo-sensors at R + d (PS d = 1.6/2.6/2.6 mm, 2S d = 1.8 mm; UNVERIFIED Phase-2 module
      spacings) paired with the main-sensor hit of the same quirk (nearest time); apparent stub pT
      pT_app = 0.3 B R / (2 sin|alpha|), tan alpha = d(r phi)/d.  Fraction passing pT_app > 2 GeV (L1 track trigger
      stub window, CMS Phase-2 L1 TDR nominal 2 GeV; UNVERIFIED as a per-layer window) and > 3 GeV;
  (3) triplets of first crossings at three consecutive layers for the same quirk: signed curvature of the circle through
      the three r-phi points, apparent pT_app = 0.3 B / |kappa|, and whether the centre of curvature lies on the
      partner's side (string pull) -- fraction of triplets "curving towards the partner";
  (4) separation of the two quirks' r-phi hits (first crossings) vs layer: fraction of events with a non-monotonic
      separation sequence (opposite-charge helix pairs from one vertex have a monotonic one);
  (5) the r-phi midpoint of the two quirks' first-crossing hits: RMS distance to the straight line PV -> phi_pair
      (zero-curvature "CM track"), in units of the half-separation.
Output: printed table, figures/T4_local.png, figures/T4_local.npz.
Run: pixi run python code/T4_local.py [nev]     (~5-10 min)
"""
import os, sys
import numpy as np
from multiprocessing import Pool
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import run, sample_theta, SENS_R, SENS_Z, B_CMS, momenta  # noqa: E402
from T2_propagator import sigma_from_lambda_keV  # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
DSP = np.array([0.16, 0.26, 0.26, 0.18, 0.18, 0.18])        # sensor spacings [cm] for OT layers 4..9 (UNVERIFIED)
SR = np.r_[SENS_R[:10], SENS_R[4:10] + DSP]
SZ = np.r_[SENS_Z[:10], SENS_Z[4:10]]
KB = 0.299792458 * B_CMS          # GeV per m of radius of curvature


def job(args):
    m, lam, th = args
    th = th.copy(); th[8] = np.log(lam)
    r = run(th, sens_r=SR, sens_z=SZ, hmax=0.01)
    H = r['hits']
    phi0 = th[2]
    out = dict()
    # (2) stubs
    stubs = []
    for L in range(4, 10):
        Lp = 10 + (L - 4)
        for k in (0, 1):
            A = H[(H[:, 0] == k) & (H[:, 1] == L)]
            Bp = H[(H[:, 0] == k) & (H[:, 1] == Lp)]
            for h in A:
                if len(Bp) == 0:
                    stubs.append(0.0); continue
                j = np.argmin(np.abs(Bp[:, 2] - h[2]))
                if abs(Bp[j, 2] - h[2]) > 5.0:          # > 5 cm/c apart in time: no stub partner (turning point)
                    stubs.append(0.0); continue
                dphi = (np.arctan2(Bp[j, 4], Bp[j, 3]) - np.arctan2(h[4], h[3]) + np.pi) % (2 * np.pi) - np.pi
                drphi = SENS_R[L] * dphi
                sa = abs(np.sin(np.arctan2(drphi, DSP[L - 4])))
                stubs.append(KB * SENS_R[L] / 100 / (2 * max(sa, 1e-9)))
    out['stub_pt'] = np.array(stubs)
    # first crossings
    first = {}
    for h in H:
        if int(h[9]) == 1 and int(h[1]) < 10:
            first[(int(h[0]), int(h[1]))] = h
    # (3) triplets
    tri = []
    for k in (0, 1):
        for L in range(0, 8):
            if all((k, L + i) in first for i in range(3)) and (1 - k, L + 1) in first:
                P = np.array([first[(k, L + i)][3:5] for i in range(3)]) / 100.0     # metres
                a, b, cc = P
                d = 2 * (a[0] * (b[1] - cc[1]) + b[0] * (cc[1] - a[1]) + cc[0] * (a[1] - b[1]))
                if abs(d) < 1e-15:
                    continue
                ux = ((a @ a) * (b[1] - cc[1]) + (b @ b) * (cc[1] - a[1]) + (cc @ cc) * (a[1] - b[1])) / d
                uy = ((a @ a) * (cc[0] - b[0]) + (b @ b) * (a[0] - cc[0]) + (cc @ cc) * (b[0] - a[0])) / d
                Rc = np.hypot(a[0] - ux, a[1] - uy)
                partner = first[(1 - k, L + 1)][3:5] / 100.0
                # centre on partner side: (centre - b) . (partner - b) > 0
                toward = (np.array([ux, uy]) - b) @ (partner - b) > 0
                tri.append((L, KB * Rc, toward))
    out['tri'] = np.array(tri) if tri else np.zeros((0, 3))
    # (4) separation monotonicity and (5) midpoint straightness
    seps, mids, halfs = [], [], []
    for L in range(10):
        if (0, L) in first and (1, L) in first:
            r0 = SENS_R[L]
            p0 = (np.arctan2(first[(0, L)][4], first[(0, L)][3]) - phi0 + np.pi) % (2 * np.pi) - np.pi
            p1 = (np.arctan2(first[(1, L)][4], first[(1, L)][3]) - phi0 + np.pi) % (2 * np.pi) - np.pi
            seps.append(r0 * abs(p0 - p1)); mids.append(r0 * 0.5 * (p0 + p1)); halfs.append(0.5 * r0 * abs(p0 - p1))
    seps = np.array(seps)
    nonmono = False
    if len(seps) >= 3:
        ds = np.diff(seps)
        nonmono = bool(np.any(ds > 0) and np.any(ds < 0))
    out['nonmono'] = nonmono if len(seps) >= 3 else np.nan
    out['mid_rms'] = np.sqrt(np.mean(np.square(mids))) if mids else np.nan
    out['half_rms'] = np.sqrt(np.mean(np.square(halfs))) if halfs else np.nan
    # (1) Delta N between consecutive layers
    p1, p2, _, mm, _ = momenta(th)
    gs = 1 + np.exp(th[4]); bs = np.sqrt(1 - 1 / gs ** 2); pt = np.exp(th[1])
    out['dN'] = sigma_from_lambda_keV(lam) * np.diff(SENS_R[:10]) / (2 * bs * pt)
    out['nhits'] = np.array([np.sum(H[:, 1] == L) for L in range(10)])
    return out


def main():
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    res = {}
    for m in (200, 500, 1000):
        rng = np.random.default_rng(m + 77)
        ths = sample_theta(float(m), nev, rng, eta_max=1.0)
        for lam in (0.3, 1.0, 3.0, 10.0):
            with Pool(2) as pool:
                res[(m, lam)] = pool.map(job, [(float(m), lam, th) for th in ths])
    print('m | L[keV] | dN(IT1-2, IT4-PS1, 2S2-2S3) median | stub pass pT>2 / >3 GeV | stub pT_app median | '
          'triplets: median pT_app [GeV], frac pT_app<2 GeV, frac toward partner | frac non-monotonic sep | '
          'midpoint RMS / half-sep RMS | hits/layer IT1..2S3')
    summ = {}
    for (m, lam), R in sorted(res.items()):
        dN = np.median([o['dN'] for o in R], axis=0)
        st = np.concatenate([o['stub_pt'] for o in R])
        tri = np.concatenate([o['tri'] for o in R if len(o['tri'])]) if any(len(o['tri']) for o in R) else np.zeros((0, 3))
        nm = np.nanmean([o['nonmono'] for o in R])
        mid = np.nanmedian([o['mid_rms'] / o['half_rms'] for o in R if o['half_rms'] > 0])
        nh = np.mean([o['nhits'] for o in R], axis=0)
        s = dict(dN=dN, stub2=(st > 2).mean(), stub3=(st > 3).mean(), stubmed=np.median(st),
                 tri_pt=np.median(tri[:, 1]) if len(tri) else np.nan,
                 tri_lt2=(tri[:, 1] < 2).mean() if len(tri) else np.nan,
                 tri_tow=tri[:, 2].mean() if len(tri) else np.nan, nonmono=nm, mid=mid, nh=nh, stubs=st)
        summ[(m, lam)] = s
        print(f'{m:5d} | {lam:4.1f} | {dN[0]:.2g}, {dN[3]:.2g}, {dN[8]:.2g} | {s["stub2"]:.2f} / {s["stub3"]:.2f} | '
              f'{s["stubmed"]:.2g} | {s["tri_pt"]:.2g}, {s["tri_lt2"]:.2f}, {s["tri_tow"]:.2f} | {nm:.2f} | {mid:.2f} | '
              + ' '.join(f'{x:.1f}' for x in nh))
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    for lam, c in zip((0.3, 1.0, 3.0, 10.0), ('C0', 'C1', 'C2', 'C3')):
        st = summ[(500, lam)]['stubs']
        axs[0].hist(np.log10(np.clip(st, 1e-3, 1e4)), bins=np.linspace(-1, 4, 101), histtype='step', density=True,
                    color=c, label=f'Λ = {lam:g} keV (pass 2 GeV: {summ[(500, lam)]["stub2"]:.2f})')
    axs[0].axvline(np.log10(2), color='k', ls='--', lw=0.8)
    axs[0].set_xlabel('log10 apparent stub pT [GeV]'); axs[0].set_title('m_Q = 500 GeV: OT stub bend of quirk hits', fontsize=9)
    axs[0].legend(fontsize=7)
    lams = (0.3, 1.0, 3.0, 10.0)
    for m, c in zip((200, 500, 1000), ('C0', 'C1', 'C2')):
        axs[1].semilogx(lams, [summ[(m, l)]['stub2'] for l in lams], 'o-', color=c, label=f'stub pT_app > 2 GeV, m={m}')
        axs[1].semilogx(lams, [summ[(m, l)]['tri_tow'] for l in lams], 's--', color=c, label=f'triplet curves to partner, m={m}')
        axs[1].semilogx(lams, [summ[(m, l)]['nonmono'] for l in lams], '^:', color=c, label=f'non-monotonic separation, m={m}')
    axs[1].set_xlabel('Λ [keV]'); axs[1].set_ylabel('fraction'); axs[1].legend(fontsize=6); axs[1].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'T4_local.png'), dpi=130)


if __name__ == '__main__':
    main()
