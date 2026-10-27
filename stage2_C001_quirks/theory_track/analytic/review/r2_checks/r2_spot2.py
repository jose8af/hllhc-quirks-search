"""r2_spot2.py -- S1-R2 independent numerical spot checks (replaces r2_spot.py, which was stopped: the unmodified R1 conformal
solver hangs at 2 keV, weak B; no output was kept).

Part S ('scale-free test' of the B* attribution of the 3 keV excess, NEAR_MISS v4 §9.3): classical NG is scale-free, so the
per-period physics of an event at (Lambda = 3 keV, B) equals that of the same event at (1 keV, B/9) (same eps_perp, b/l0,
gamma*, k_B, angles); only the number of periods in the tracker (9x fewer at 1 keV) and the lever differ.  The law predicts the
SAME c for the window [B0/9 -> B0/180] at 1 keV as for [B0 -> B0/20] at 3 keV (c_E1 identical).  A per-period effect (B* or a
per-crossing floor effect) must give the same excess; an effect that accumulates with the number of crossings will not.
  Causal kernel nm_kernel (E2's T3 copy), max_boost 1e-3, hmax 0.02 cm, default hit set (same as E2's FU 'fine' 3 keV runs),
  M3 events (seed 777+m), compared per event with E2's FU fine 3 keV Delta_s at f = 1 and 1/20.
Part O: round-1 reviewer's 16 events (R1.make_event, rng 2026, gamma* = 1.28, pT = 300 GeV), 1 keV, B0 and B0/4, causal
  (1e-3, 10 radii, no z cut) vs the conformal c_4 of r1_lab_c_out.txt (k_B = 8.4-12 events were +0.016..+0.035 there).
Part C: thickness-law constant C from two B values (B0, B0/4) with the INDEPENDENT conformal solver: re-analysis of the
  round-1 reviewer's unmodified-R1 runs (r1_lab_c_out.txt, N = 4096, 16 events) and of this run's causal values on the same
  events: C_meas = 1/c_4 - ln(1/eps_B) vs E1's C_ev.  (Conformal runs on M3 events were dropped: the unmodified R1 solver
  takes > 90 s per run on several of them and a SIGALRM guard cannot interrupt numba code.)
Run (from TT): pixi run python analytic/review/r2_checks/r2_spot2.py > analytic/review/r2_checks/r2_spot2_out.txt
"""
import os, sys, time, signal
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
for p in (os.path.join(TT, 'code'), os.path.join(TT, 'analytic', 'numerics'), HERE):
    sys.path.insert(0, p)
B0 = 3.8112
NS, NC = 60, 16


class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


def job(a):
    kind, i, m, p1, p2 = a
    from nm_kernel import run
    from T3_propagator import plane_fit
    from nm_conformal import RADII
    t0 = time.time(); out = dict(kind=kind, i=i, m=m)
    if kind == 'S':
        for f in (1 / 9, 1 / 180):
            r = run(p1, p2, m, 1.0, B0=B0 * f, max_boost=1e-3, hmax_trk=0.02, max_steps=4_000_000_000)
            H = r['hits']; H = H[H[:, 1] < 10]
            out[f] = plane_fit(H[:, 3:6])[0] if (len(H) >= 4 and r['status'] == 1) else np.nan
    elif kind in ('O', 'C'):
        for f in (1.0, 0.25):
            r = run(p1, p2, m, 1.0, B0=B0 * f, max_boost=1e-3, hmax_trk=0.02, rec_radii=RADII, rec_zmax=np.full(10, 1e9))
            H = r['hits']; H = H[H[:, 1] < 10]
            out[('cau', f)] = plane_fit(H[:, 3:6])[0]
            if kind == 'C':
                import R1_conformal_ng as R1
                signal.signal(signal.SIGALRM, _alarm); signal.alarm(90)
                try:
                    Hc, _, _ = R1.run(p1, p2, m, 1.0, Bz=B0 * f, N=4096)
                    Hc = Hc[Hc[:, 1] < 10]
                    out[('conf', f)] = R1.plane_thickness(Hc[:, 3:6])[0]
                except TO:
                    out[('conf', f)] = np.nan
                signal.alarm(0)
    out['cpu'] = time.time() - t0
    return out


if __name__ == '__main__':
    import R1_conformal_ng as R1
    from T3_propagator import sample_events
    import FIX1_analysis as X
    import FU_analysis as F
    from r2_kB_confound import boot_med
    t0 = time.time()
    tasks = []
    evs = {}
    for m in (500.0, 1000.0):
        evs[m] = sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0)
        tasks += [('S', i, m, evs[m][i][0], evs[m][i][1]) for i in range(NS)]
    rng = np.random.default_rng(2026)
    outl = [R1.make_event(rng, 500.0) for _ in range(16)]
    tasks += [('O', i, 500.0, p[0], p[1]) for i, p in enumerate(outl)]
    with ProcessPoolExecutor(6, mp_context=mp.get_context('spawn')) as ex:
        rows = list(ex.map(job, tasks))
    cpu = sum(r['cpu'] for r in rows)
    # ---------------- Part S
    print('# Part S: scale-free test. c3 = 3 keV window B0 -> B0/20 (E2 FU fine), c1 = 1 keV window B0/9 -> B0/180 (this run); same c_E1')
    for m in (500.0, 1000.0):
        fu = F.fu_load(m, 3.0, 'fine')
        R = []
        for r in [r for r in rows if r['kind'] == 'S' and r['m'] == m]:
            i = r['i']
            if i not in fu or not np.isfinite(r[1 / 9]) or not np.isfinite(r[1 / 180]):
                continue
            k = X.kin2(evs[m][i][0], evs[m][i][1], m, 3.0)
            c3 = (fu[i][3] * 20 / fu[i][0] - 1) / np.log(20)
            c1 = (r[1 / 180] * 20 / r[1 / 9] - 1) / np.log(20)
            R.append((k['kB_perp'], k['c_E1'], c3, c1, fu[i][0], r[1 / 9]))
        R = np.array(R)
        print(f'm = {m:.0f} GeV, n = {len(R)}; Ds(1 keV, B0/9)/Ds(3 keV, B0) median {np.median(R[:, 5] / R[:, 4]):.3f} (scale-free mapping: same qB/sigma)')
        for lo, hi in ((0, 5), (5, 10), (10, 1e9), (0, 1e9)):
            s = (R[:, 0] >= lo) & (R[:, 0] < hi)
            if s.sum() < 3:
                continue
            a = boot_med(R[s, 2] - R[s, 1]); b = boot_med(R[s, 3] - R[s, 1]); d = boot_med(R[s, 2] - R[s, 3])
            print(f'  k_B in [{lo},{hi:g}) n={s.sum():3d}: c3 - c_E1 = {a[0]:+.4f} +- {a[1]:.4f};  c1 - c_E1 = {b[0]:+.4f} +- {b[1]:.4f};  '
                  f'paired c3 - c1 = {d[0]:+.4f} +- {d[1]:.4f}')
    # ---------------- Part O
    r1c4 = {}
    for line in open(os.path.join(TT, 'analytic', 'review', 'r1_checks', 'r1_lab_c_out.txt')):
        s = line.split()
        if len(s) > 11 and s[0].isdigit() and s[5] == '4096':
            r1c4[int(s[0])] = float(s[11])
    geo = {}
    import r1_lab_c as L  # noqa
    print('\n# Part O: round-1 events, 1 keV: c4 causal (this run) vs conformal (r1_lab_c_out, N=4096); c_E1 and k_B from r1 geometry')
    print('# ev  kB     c_E1    c4_conf  c4_caus  conf-caus')
    for r in sorted([r for r in rows if r['kind'] == 'O'], key=lambda r: r['i']):
        i = r['i']; p1, p2 = outl[i]
        cE = L.c_E1(p1, p2)[0]; sa, kB, gb = L.geometry(p1, p2)
        c4 = (4 * r[('cau', 0.25)] / r[('cau', 1.0)] - 1) / np.log(4)
        print(f'{i:3d}  {kB:6.2f}  {cE:.4f}  {r1c4.get(i, np.nan):.4f}   {c4:.4f}   {r1c4.get(i, np.nan) - c4:+.4f}')
    # ---------------- Part C (re-analysis: conformal c4 from round 1, causal c4 from this run, same 16 events)
    epsB = 2.99792458e-3 * B0 / R1.sigma_keV(1.0); Lb = np.log(1 / epsB)
    print(f'\n# Part C: C = 1/c4 - ln(1/eps_B), ln(1/eps_B) = {Lb:.3f}; round-1 events (gamma* = 1.28, pT = 300 GeV), 1 keV, 500 GeV')
    CC = []
    for r in sorted([r for r in rows if r['kind'] == 'O'], key=lambda r: r['i']):
        i = r['i']; p1, p2 = outl[i]
        cE = L.c_E1(p1, p2)[0]; sa, kB, gb = L.geometry(p1, p2)
        c4 = (4 * r[('cau', 0.25)] / r[('cau', 1.0)] - 1) / np.log(4)
        CC.append((kB, 1 / cE - Lb, 1 / r1c4[i] - Lb, 1 / c4 - Lb))
    CC = np.array(CC)
    for lab, sel in (('all', CC[:, 0] > -1), ('k_B < 6.5', CC[:, 0] < 6.5)):
        print(f'#  {lab:9s} n={sel.sum():2d}: median C_E1 = {np.median(CC[sel, 1]):+.3f};  conformal C_meas = {np.median(CC[sel, 2]):+.3f} '
              f'(median diff {np.median(CC[sel, 2] - CC[sel, 1]):+.3f});  causal C_meas = {np.median(CC[sel, 3]):+.3f} (median diff {np.median(CC[sel, 3] - CC[sel, 1]):+.3f})')
    print(f'# wall {time.time() - t0:.0f} s, cpu {cpu:.0f} s')
