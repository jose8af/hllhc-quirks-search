"""T2_approx_errors.py -- accuracy of the oscillation-length / period shorthands used in the quirk
literature, relative to the exact vacuum solution (theory track, investigator T2).

Exact (equal masses, CM energy per quirk gamma* m, momentum p* = m gamma* beta*):
   l_max = 2 (gamma*-1) m / sigma,  crossing-to-crossing CM time t_c = 2 p*/sigma,
   lab crossing spacing D = 2 p* (beta gamma)_pair / sigma.
Shorthands tested (ratio to exact):
   K17  : "d_cm ~ 2 cm (gamma-1)(m/100 GeV)(keV/Lambda)^2"        [1708.02243 Eq.1; 2410.00269 Eq.1]
   F24  : "l ~ 1 cm (m/100 GeV)(keV/Lambda)^2"                    [2404.13814 Eq.2.6; 2607.26195 p.2; 2512.20696 Eq.1]
   EL18 : "l ~ 10 cm (m/TeV)(keV/Lambda)^2"                       [1811.08903 Eq.1.1]  (same as F24)
   NR   : l = m beta*^2/sigma (non-relativistic energy balance)
   UR   : l = 2 E*/sigma (massless-endpoint yo-yo)
   T_NR : t_c = 2 sqrt(2 m E_kin)/sigma                             [1811.08903 below Eq.B.3; 2404.13814 above Eq.4.2]
   Li L : lab width L = l_max sin(theta*)                           [2002.07503 Eq.III.1]  vs exact transverse width
Also: time-averaged fraction of the kinetic energy stored in the string, f(gamma*).
Inputs: gamma* distributions from T2_kinematics.py (cache file T2_CACHE in data/cache; regenerated
automatically if missing).
Output: figures/T2_approx_errors.png and a table on stdout.
Run:  pixi run python code/T2_approx_errors.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, '..', 'figures')
HB = 1.973269804e-14
UNIT = 2 * 100.0 / ((1e-6) ** 2 / HB)   # 2 m/sigma for m=100 GeV, Lambda = 1 keV  [cm] = 3.947 cm


def ratios(g):
    b = np.sqrt(1 - 1 / g ** 2)
    exact = g - 1                                  # in units of UNIT (2 m/sigma)
    return {
        'K17: 2 cm (γ−1)': (2.0 / UNIT) * (g - 1) / exact,
        'F24/EL18: 1 cm (no γ)': (1.0 / UNIT) / exact,
        'NR: mβ²/σ': (b ** 2 / 2) / exact,
        'UR: 2E*/σ': g / exact,
        'T_NR: 2√(2mE_kin)/σ (period)': np.sqrt(2 / (g + 1)),
    }


def string_fraction(g):
    """time-average of sigma*|x1-x2| / E_kin(total); p uniform in [0,p*] over time."""
    ps = np.sqrt(g * g - 1)
    meanE = 0.5 * (np.sqrt(1 + ps ** 2) + np.arcsinh(ps) / ps)   # <sqrt(1+p^2)> on [0,ps], m=1
    return (g - meanE) / (g - 1)


def wq(v, w, qs=(0.16, 0.5, 0.84)):
    i = np.argsort(v); v = v[i]; c = np.cumsum(w[i]); c /= c[-1]
    return [v[min(np.searchsorted(c, q), len(v) - 1)] for q in qs]


if __name__ == '__main__':
    import subprocess, sys
    sys.path.insert(0, HERE)
    from T2_kinematics import CACHE
    if not os.path.exists(CACHE):          # regenerate the data/cache cache if missing
        subprocess.run([sys.executable, os.path.join(HERE, 'T2_kinematics.py')], check=True)
    cache = np.load(CACHE)
    print('UNIT 2m/sigma (m=100 GeV, 1 keV) = %.4f cm' % UNIT)
    print('\n| shorthand | ratio to exact: fermion E 500 GeV pT>200 (16/50/84%) | scalar Ẽ 500 GeV | fermion E 1000 GeV | fermion E 200 GeV |')
    print('|---|---|---|---|---|')
    keys = list(ratios(np.array([1.2])).keys())
    rows = {k: [] for k in keys}
    rows['Li L = l_max sinθ* vs exact width'] = []
    rows['string-energy fraction <E_str>/E_kin'] = []
    for tag in ('F_500_isr', 'S_500_isr', 'F_1000_isr', 'F_200_isr'):
        g = cache[f'{tag}_gamma_star']; w = cache[f'{tag}_w']
        r = ratios(g)
        for k in keys:
            rows[k].append(wq(r[k], w))
        rows['string-energy fraction <E_str>/E_kin'].append(wq(string_fraction(g), w))
    for k, v in rows.items():
        if v:
            print(f'| {k} | ' + ' | '.join('%.3g / %.3g / %.3g' % tuple(x) for x in v) + ' |')
    # Li width: need chord factor -> recompute from cstar, bg_pair, gamma*
    for tag in ('F_500_isr', 'F_200_isr'):
        g = cache[f'{tag}_gamma_star']; w = cache[f'{tag}_w']; c = cache[f'{tag}_cstar']; bg = cache[f'{tag}_bg_pair']
        b = bg / np.sqrt(1 + bg ** 2); k = np.abs(b * c)
        u = np.zeros_like(g)
        for _ in range(60):
            u = k * (g - np.sqrt(1 + u * u))
        cf = (g - np.sqrt(1 + u * u)) / (g - 1)
        q = wq(1 / cf, w, (0.5, 0.84, 0.98))
        print(f'Li width / exact width, {tag}: median {q[0]:.4f}, 84% {q[1]:.4f}, 98% {q[2]:.4f}')
    # figure
    gg = np.linspace(1.001, 3.0, 400)
    r = ratios(gg)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ax = axes[0]
    for i, (k, v) in enumerate(r.items()):
        ax.plot(gg, v, label=k, color=f'C{i}')
    ax.axhline(1, color='k', lw=0.8)
    ax.set_yscale('log'); ax.set_ylim(0.2, 20); ax.set_xlabel('γ* (per-quirk Lorentz factor in pair CM)')
    ax.set_ylabel('shorthand / exact'); ax.grid(alpha=0.3, which='both')
    ax2 = ax.twinx()
    for tag, ls, lab in (('F_500_isr', '-', 'E 500 GeV, pT>200'), ('S_500_isr', '--', 'Ẽ 500 GeV, pT>200')):
        h, b = np.histogram(cache[f'{tag}_gamma_star'], bins=np.linspace(1, 3, 81), weights=cache[f'{tag}_w'])
        ax2.fill_between(b[:-1], h / h.sum(), step='post', alpha=0.15, color='gray' if ls == '-' else 'C9', label=lab)
    ax2.set_yticks([]); ax2.legend(loc='upper center', fontsize=7)
    ax.legend(fontsize=7, loc='upper right')
    ax.set_title('Oscillation length / period shorthands vs exact')
    ax = axes[1]
    ax.plot(gg, string_fraction(gg), color='C0')
    ax.axhline(2 / 3, ls=':', color='k'); ax.axhline(0.5, ls=':', color='k')
    ax.text(2.5, 0.675, 'NR virial 2/3', fontsize=8); ax.text(2.5, 0.51, 'UR limit 1/2', fontsize=8)
    ax.set_xlabel('γ*'); ax.set_ylabel('time-averaged ⟨E_string⟩ / E_kin'); ax.grid(alpha=0.3)
    ax.set_title('Energy stored in the string (exact)')
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'T2_approx_errors.png'), dpi=130)
    print('figure written')
