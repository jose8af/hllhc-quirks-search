"""F1_standin.py -- fix pass F1, spot check for R1-critical A-1/A-3: "was T2's lab-simultaneous straight string
(labSS) a faithful stand-in for the published Li et al. integrator?"  Tested on EXACTLY the events behind the
synthesis v1 S-1 numbers: T2_string_methods_B.py events (rng seed 7, 4 events, m = 500 GeV, gamma* = 1.28,
pT = 300 GeV, 3.8 T, no material, 10 barrel radii).

Per event and Lambda in {0.6, 1, 2} keV:
  causal  : T3_causal.run_causal (max_boost 1e-3, hmax 0.02 cm; validated against an independent conformal-gauge NG
            solver by R1 to <= 1 % in thickness);
  Li      : R1_li_literal.run_li = literal Li et al. integrator [1911.02223 Eq.III.6-10], step = f x Eq.III.10 bound,
            f = 1 (printed bound), 0.01, 0.003;
  labSS / cmSS : T2's stored values (figures/T2_string_methods_B.npy, columns d_labSS, d_cmSS), i.e. the numbers
            that produced "x0.04-60" in v1.
Output: thickness ratios to causal; pass criterion for "labSS is a stand-in for Li": |labSS/Li - 1| < 0.5.
Run (from theory_track/): pixi run python code/F1_standin.py      Output copy: figures/F1_standin_out.txt
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R1_li_literal import run_li, plane_thickness, RADII   # noqa: E402
from T2_string_methods_B import make_event                  # noqa: E402
from T3_causal import run_causal                            # noqa: E402

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')

if __name__ == '__main__':
    rng = np.random.default_rng(7)
    m = 500.0
    events = [make_event(rng, m) for _ in range(4)]
    t2 = np.load(os.path.join(FIG, 'T2_string_methods_B.npy'))     # lam, ie, ncross, d_c, d_lab, d_cm, ...
    fracs = [1.0, 0.01, 0.003]
    allr = []
    print('| Λ | ev | causal (T3, µm) | T2 causal (µm) | Li ×1 | Li ×0.01 | Li ×0.003 | T2 labSS | T2 cmSS | Li/causal | labSS/causal | labSS/Li |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for lam in (0.6, 1.0, 2.0):
        for ie, (p1, p2, bT) in enumerate(events):
            rc = run_causal(p1, p2, m, lam, B0=3.8, material=False, rec_radii=np.array(RADII), rec_zmax=np.full(10, 1e9),
                            first_length=1e-7, max_boost=1e-3, hmax_trk=0.02)
            dc = plane_thickness(rc['hits'][:, 3:6]) * 1e4
            dl = []
            for f in fracs:
                H, ns = run_li(p1, p2, m, lam, frac=f)
                dl.append(plane_thickness(H[:, 3:6]) * 1e4)
            row = t2[(np.abs(t2[:, 0] - lam) < 1e-9) & (t2[:, 1] == ie)][0]
            dt2c, dlab, dcm = row[3], row[4], row[5]
            allr.append((lam, ie, dc, dl[-1], dlab, dcm))
            print(f'| {lam:g} | {ie} | {dc:.3g} | {dt2c:.3g} | {dl[0]:.3g} | {dl[1]:.3g} | {dl[2]:.3g} | {dlab:.3g} | {dcm:.3g} |'
                  f' {dl[-1]/dc:.2f} | {dlab/dc:.2f} | {dlab/dl[-1]:.2f} |', flush=True)
    a = np.array(allr)
    r_li = a[:, 3] / a[:, 2]; r_lab = a[:, 4] / a[:, 2]; r_cm = a[:, 5] / a[:, 2]
    print(f'\nLi(x0.003)/causal: median {np.median(r_li):.2f}, range {r_li.min():.2f}-{r_li.max():.2f}')
    print(f'labSS/causal     : median {np.median(r_lab):.2f}, range {r_lab.min():.2f}-{r_lab.max():.2f}')
    print(f'cmSS/causal      : median {np.median(r_cm):.2f}, range {r_cm.min():.2f}-{r_cm.max():.2f}')
    ok = np.abs(a[:, 4] / a[:, 3] - 1) < 0.5
    print(f'"labSS is a stand-in for Li" (|labSS/Li - 1| < 0.5): {ok.sum()}/{len(ok)} events -> '
          f'{"PASS" if ok.all() else "FAIL"}')
