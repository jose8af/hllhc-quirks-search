"""S_Bscan.py -- synthesis follow-up to S_Bnonlin.py: shape of the causal-string B response over 4 decades of B.

Question: T4 (G-T4-4) and S_Bnonlin.py find that the hit displacement per unit B of the causal string is ~1.3-1.4x
larger at B/20-B/80 than at 3.8 T, converged in max_boost.  Is this (a) a B-independent offset between the exact
B = 0 run (exactly head-on crossings) and the B -> 0 limit (near-miss crossings), (b) a B log B term, or (c) a power
law?  Response ratio R(f) = Q68|d(f)/f| / Q68|d(1)| with d(f) = y(f B) - y(ref); two references: ref = B = 0 and
ref = 1e-6 B (near-miss crossings, but negligible field).  (a) predicts R ~ 1/f with ref = 0 and R -> const with
ref = 1e-6; (b) R = 1 + c ln(1/f); (c) R = f^-k.
Run (from theory_track/): pixi run python code/S_Bscan.py [nev] [m] [lam]   (default 3 events, 500 GeV, 1 keV; ~1 min)
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T4_model import run, sample_theta, B_CMS  # noqa: E402
from S_Bnonlin import hits_by_key, disp, q68, GROUPS  # noqa: E402
from T3_propagator import plane_fit  # noqa: E402

FR = [1e-4, 1e-3, 1 / 80, 1 / 20, 1 / 4, 1.0]


def main():
    nev = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    m = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
    lam = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    rng = np.random.default_rng(int(m) + 11)
    thetas = sample_theta(m, nev, rng, eta_max=1.0)
    for refname, fref in (('B=0', 0.0), ('1e-6 B', 1e-6)):
        acc = {g: {f: [] for f in FR} for g in GROUPS}
        for th in thetas:
            th = th.copy(); th[8] = np.log(lam)
            H0 = hits_by_key(run(th, B0=B_CMS * fref)['hits'])
            _, nrm = plane_fit(np.array([h[3:6] for h in H0.values()]))
            for f in FR:
                HB = hits_by_key(run(th, B0=B_CMS * f)['hits'])
                for k in H0:
                    if k in HB:
                        for g, Ls in GROUPS.items():
                            if k[1] in Ls:
                                acc[g][f].append(disp(HB[k], H0[k], nrm)[0] / f)
        print(f'm={m:.0f} GeV, Lambda={lam:g} keV, {nev} events, reference {refname}')
        print('group  ' + '  '.join(f'R({f:.2g})' for f in FR) + '   Q68|d(1)| [um]')
        for g in GROUPS:
            q1 = q68(acc[g][1.0])
            print(f'{g:5s}  ' + '  '.join(f'{q68(acc[g][f]) / q1:8.3f}' for f in FR) + f'   {q1*1e4:.2f}')
        # power-law and log fits to the 2S group
        f = np.array(FR[:-1]); R = np.array([q68(acc['2S'][x]) / q68(acc['2S'][1.0]) for x in FR[:-1]])
        k = -np.polyfit(np.log(f), np.log(R), 1)[0]
        c = np.polyfit(np.log(1 / f), R - 1, 1)[0]
        print(f'2S: best power law R = f^-{k:.3f}; best log law R = 1 + {c:.3f} ln(1/f); '
              f'power-law pred. R(1e-4) = {1e-4**-k:.2f}, log pred. = {1 + c*np.log(1e4):.2f}\n')


if __name__ == '__main__':
    main()
