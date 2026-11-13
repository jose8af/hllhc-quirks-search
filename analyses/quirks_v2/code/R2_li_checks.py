"""R2_li_checks.py -- reviewer R2: two independent extensions of the Li-literal vs causal comparison behind S-1.

Purpose
  (a) 'gamma' mode: is "Li method ~15 % low in thickness when converged" a general statement, or a property of the single
      kinematic point (m=500 GeV, gamma*=1.28, pT=300 GeV) used by every R1/F1 comparison?  Runs Li-literal (R1 kernel,
      1911.02223 Eq.III.6-10) at two step fractions and the causal port (T3_causal, converged settings as in R1) for
      several gamma* at fixed Lambda.
  (b) 'fine' mode: does the 3 keV Li/causal ratio converge (and to ~0.85) if the step is pushed below R1's x0.003?
      Same events as R1 (seed 11, 6 events, make_event defaults), Lambda=3 keV, fractions given on the command line.
Inputs: R1_li_literal.run_li / plane_thickness (Li kernel), R1_conformal_ng.make_event (kinematics), T3_causal.run_causal.
Run (from theory_track/):
  pixi run python code/R2_li_checks.py gamma <lam> <gstar list> <nev> <frac list> [seed]
  pixi run python code/R2_li_checks.py fine  <lam> <event idx list> <frac list> [seed] [nev_drawn]
Outputs printed (redirect to figures/R2_li_checks_out.txt).
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R1_li_literal import run_li, plane_thickness, RADII
from R1_conformal_ng import make_event
from T3_causal import run_causal

M = 500.0


def causal(p1, p2, lam):
    rc = run_causal(p1, p2, M, lam, B0=3.8, material=False, rec_radii=RADII, rec_zmax=np.full(10, 1e9),
                    first_length=1e-7, max_boost=1e-3, hmax_trk=0.02)
    return rc['hits']


def match(H, Hc):
    """max |dhit| and max out-of-plane |dhit| (w.r.t. causal plane normal), nearest-time matching per (quirk, layer)."""
    h = Hc[:, 3:6]
    w, v = np.linalg.eigh(h.T @ h)
    n = v[:, 0]
    dm = 0.0; dn = 0.0
    for hh in H:
        cand = Hc[(Hc[:, 0] == hh[0]) & (Hc[:, 1] == hh[1])]
        if len(cand) == 0:
            continue
        j = np.argmin(np.abs(cand[:, 2] - hh[2]))
        d = cand[j, 3:6] - hh[3:6]
        dm = max(dm, np.linalg.norm(d)); dn = max(dn, abs(d @ n))
    return dm, dn


def one(p1, p2, lam, fracs, tag):
    t0 = time.time()
    Hc = causal(p1, p2, lam)
    dc = plane_thickness(Hc[:, 3:6])
    row = [f"{tag}: causal {dc*1e4:.3g} um [{len(Hc)}]"]
    for f in fracs:
        H, ns = run_li(p1, p2, M, lam, frac=f)
        dl = plane_thickness(H[:, 3:6])
        dm, dn = match(H, Hc)
        row.append(f"Li(x{f:g}) {dl*1e4:.3g} um [{len(H)}] ratio {dl/dc:.3f} max|dhit| {dm*1e4:.3g} um "
                   f"max|dn| {dn*1e4:.3g} um")
    row.append(f"({time.time()-t0:.0f}s)")
    print(' | '.join(row), flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    lam = float(sys.argv[2])
    if mode == 'gamma':
        gs = [float(x) for x in sys.argv[3].split(',')]
        nev = int(sys.argv[4])
        fracs = [float(x) for x in sys.argv[5].split(',')]
        seed = int(sys.argv[6]) if len(sys.argv) > 6 else 23
        for g in gs:
            rng = np.random.default_rng(seed)
            for ie in range(nev):
                p1, p2 = make_event(rng, M, gstar=g)
                one(p1, p2, lam, fracs, f"Lambda={lam} gstar={g} ev{ie}")
    elif mode == 'fine':
        idx = [int(x) for x in sys.argv[3].split(',')]
        fracs = [float(x) for x in sys.argv[4].split(',')]
        seed = int(sys.argv[5]) if len(sys.argv) > 5 else 11
        nd = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        rng = np.random.default_rng(seed)
        evs = [make_event(rng, M) for _ in range(nd)]
        for ie in idx:
            p1, p2 = evs[ie]
            one(p1, p2, lam, fracs, f"Lambda={lam} seed{seed} ev{ie}")
