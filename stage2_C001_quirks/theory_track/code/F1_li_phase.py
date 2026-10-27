"""F1_li_phase.py -- fix pass F1: characterise the residual mm-scale hit differences between the literal Li et al.
integrator [1911.02223 Eq.III.6-10] and the causal Nambu-Goto string at Lambda = 2 keV that remain at the finest step
of the R1 reviewer's run (figures/R1_li_literal_out_b.txt, e.g. ev0 7.5 mm, ev4 9.8 mm at step x0.003 while the
thickness agrees to ~10 %).

Questions: (1) is the difference a Li step-convergence effect (compare Li x0.003 with x0.001 and x0.0003)?
(2) is it in-plane (oscillation phase) or out-of-plane? (3) does it start at a particular near-miss crossing?
(4) does it matter for a plane finder (thickness, plane normal) or only for hit-position prediction?

Method: the same events as R1 (make_event from R1_conformal_ng, rng seed 11, m = 500 GeV, gamma* = 1.28, pT = 300 GeV,
3.8 T, no material, 10 barrel radii). The Li kernel is a copy of R1_li_literal.li_run (unchanged physics) that in
addition records the local minima of |r1 - r2| (crossings) with their time and miss distance. Causal reference:
T3_causal.run_causal with the reviewer's settings (max_boost 1e-3, hmax_trk 0.02 cm), which R1 validated against an
independent conformal-gauge NG solver to <= 6 um on hits at 2 keV (figures/R1_conformal_ng_out.txt).
Hit matching: as R1 (same quirk, same layer, nearest time); in addition the hits are decomposed along the causal
plane normal (out-of-plane) and in-plane, and per-(quirk, layer) hit counts are compared.

Run (from theory_track/): pixi run python code/F1_li_phase.py [lam=2] [events=0,1,2,3,4,5] [fracs=0.003,0.001]
Output: printed; copy kept in figures/F1_li_phase_out.txt.
"""
import os, sys, time
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from R1_li_literal import _kl, sigma_keV, li_step, plane_thickness, RADII, KAPPA   # noqa: E402
from R1_conformal_ng import make_event                                              # noqa: E402
from T3_causal import run_causal                                                    # noqa: E402


@njit(cache=True)
def li_run_x(p1, p2, m, sig, Bz, eps, t_end, radii, s0):
    """Copy of R1_li_literal.li_run (explicit Euler, CM-simultaneous steps Eq.III.6-7, s_hat Eq.III.8-9) that also
    records local minima of |r1 - r2| (time of quirk 1, miss distance)."""
    t = np.zeros(2); r = np.zeros((2, 3)); p = np.zeros((2, 3))
    p[0] = p1; p[1] = p2
    q = np.array([1.0, -1.0])
    hits = np.zeros((20000, 6)); nh = 0
    cx = np.zeros((200000, 2)); nc = 0
    dprev2 = 1e30; dprev1 = 1e30
    nstep = 0
    while min(t[0], t[1]) < t_end and nstep < 4_000_000_000:
        E = np.sqrt(m * m + (p * p).sum(axis=1))
        v = p / E.reshape(2, 1)
        beta = (p[0] + p[1]) / (E[0] + E[1])
        rs1 = (r[0] - r[1]) - (t[0] - t[1]) * v[0]
        rs2 = (r[1] - r[0]) - (t[1] - t[0]) * v[1]
        n1 = np.sqrt(rs1 @ rs1); n2 = np.sqrt(rs2 @ rs2)
        s1 = rs1 / n1 if n1 > 1e-14 else s0
        s2 = rs2 / n2 if n2 > 1e-14 else -s0
        F = np.zeros((2, 3))
        for i in range(2):
            si = s1 if i == 0 else s2
            F[i] = _kl(v[i], si, sig)
            F[i, 0] += q[i] * KAPPA * v[i, 1] * Bz
            F[i, 1] -= q[i] * KAPPA * v[i, 0] * Bz
        Et = E[0] + E[1]
        d = r[0] - r[1]
        dn = np.sqrt(d @ d)
        if nstep > 2 and dprev1 < dprev2 and dprev1 <= dn and nc < cx.shape[0]:
            cx[nc, 0] = t[0]; cx[nc, 1] = dprev1; nc += 1
        dprev2 = dprev1; dprev1 = dn
        c1 = 1 - v[0] @ beta - d @ (F[0] - (v[0] @ F[0]) * beta) / Et
        c2 = 1 - v[1] @ beta + d @ (F[1] - (v[1] @ F[1]) * beta) / Et
        if c1 >= c2:
            e1 = eps * c2 / c1; e2 = eps
        else:
            e1 = eps; e2 = eps * c1 / c2
        es = (e1, e2)
        for i in range(2):
            rn = r[i] + v[i] * es[i]
            r0 = np.sqrt(r[i, 0] ** 2 + r[i, 1] ** 2); r1 = np.sqrt(rn[0] ** 2 + rn[1] ** 2)
            for L in range(radii.shape[0]):
                R = radii[L]
                if (r0 - R) * (r1 - R) < 0 and nh < hits.shape[0]:
                    f = (R - r0) / (r1 - r0)
                    hits[nh, 0] = i; hits[nh, 1] = L; hits[nh, 2] = t[i] + f * es[i]
                    hits[nh, 3:6] = r[i] + f * (rn - r[i]); nh += 1
            r[i] = rn
            p[i] = p[i] + F[i] * es[i]
            t[i] += es[i]
        nstep += 1
        if np.sqrt(r[0, 0] ** 2 + r[0, 1] ** 2) > radii[-1] + 3 and np.sqrt(r[1, 0] ** 2 + r[1, 1] ** 2) > radii[-1] + 3:
            break
    return hits[:nh], cx[:nc], nstep


def run_li_x(p1, p2, m, lam, frac, Bz=3.8):
    P = p1 + p2
    E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
    t_end = 1.3 * RADII[-1] / max(np.hypot(P[0], P[1]) / E, 1e-3) + 5
    s0 = (p1 / np.hypot(m, np.linalg.norm(p1)) - p2 / np.hypot(m, np.linalg.norm(p2)))
    s0 = s0 / np.linalg.norm(s0)
    return li_run_x(np.asarray(p1, float), np.asarray(p2, float), float(m), sigma_keV(lam), float(Bz),
                    li_step(m, lam) * frac, float(t_end), RADII, s0)


def plane_normal(h):
    T = h.T @ h / (len(h) - 1)
    w, v = np.linalg.eigh(T)
    return v[:, 0]


def match(H, Hc):
    """R1 matching: same quirk + layer, nearest time.  Returns rows (i_li, j_c, |d|, |d.n|, |d_inplane|, dt)."""
    n = plane_normal(Hc[:, 3:6])
    out = []
    for a, hh in enumerate(H):
        idx = np.where((Hc[:, 0] == hh[0]) & (Hc[:, 1] == hh[1]))[0]
        if len(idx) == 0:
            continue
        j = idx[np.argmin(np.abs(Hc[idx, 2] - hh[2]))]
        d = hh[3:6] - Hc[j, 3:6]
        dn = abs(d @ n)
        out.append((a, j, np.linalg.norm(d), dn, np.linalg.norm(d - (d @ n) * n), hh[2] - Hc[j, 2]))
    return np.array(out), n


def counts(H):
    c = {}
    for hh in H:
        k = (int(hh[0]), int(hh[1]))
        c[k] = c.get(k, 0) + 1
    return c


if __name__ == '__main__':
    lam = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    evsel = [int(x) for x in (sys.argv[2].split(',') if len(sys.argv) > 2 else '0,1,2,3,4,5'.split(','))]
    fracs = [float(x) for x in (sys.argv[3].split(',') if len(sys.argv) > 3 else ['0.003', '0.001'])]
    m = 500.0
    rng = np.random.default_rng(11)
    events = [make_event(rng, m) for _ in range(max(evsel) + 1)]
    for ie in evsel:
        p1, p2 = events[ie]
        rc = run_causal(p1, p2, m, lam, B0=3.8, material=False, rec_radii=RADII, rec_zmax=np.full(10, 1e9),
                        first_length=1e-7, max_boost=1e-3, hmax_trk=0.02)
        Hc = rc['hits']
        dc = plane_thickness(Hc[:, 3:6])
        cc = counts(Hc)
        print(f"\n=== Lambda={lam} ev{ie}: causal thickness {dc*1e4:.3g} um, {len(Hc)} hits", flush=True)
        prev = None
        for frac in fracs:
            tic = time.time()
            H, cx, ns = run_li_x(p1, p2, m, lam, frac)
            M, nC = match(H, Hc)
            nL = plane_normal(H[:, 3:6])
            ang = np.degrees(np.arccos(min(1.0, abs(nL @ nC))))
            cl = counts(H)
            mism = sorted(k for k in set(cl) | set(cc) if cl.get(k, 0) != cc.get(k, 0))
            # thickness of the causal hits w.r.t. the Li plane normal (does the Li plane accept the true hits?)
            dcross = np.sqrt(np.sum((Hc[:, 3:6] @ nL) ** 2) / (len(Hc) - 1))
            big = M[M[:, 2] > 0.01]       # > 100 um
            line = (f"  Li x{frac:g}: {ns:.3g} steps, {time.time()-tic:.0f}s | thickness {plane_thickness(H[:, 3:6])*1e4:.3g} um"
                    f" [{len(H)} hits] | plane-normal angle Li vs causal {ang*1e3:.3g} mdeg | causal hits about Li plane"
                    f" {dcross*1e4:.3g} um | max|dhit| {M[:, 2].max()*1e4:.4g} um, max out-of-plane {M[:, 3].max()*1e4:.3g} um,"
                    f" median|dhit| {np.median(M[:, 2])*1e4:.3g} um | (quirk,layer) count mismatches {mism}")
            print(line, flush=True)
            if len(big):
                # first hit (in time) with |dhit| > 100 um, and the near-miss crossings before it
                order = np.argsort(H[big[:, 0].astype(int), 2])
                b0 = big[order[0]]
                t0 = H[int(b0[0]), 2]
                k = int(b0[0])
                print(f"     hits with |dhit|>100 um: {len(big)}/{len(M)}; first at t={t0:.1f} cm (quirk {int(H[k,0])},"
                      f" layer {int(H[k,1])}), |d|={b0[2]*1e4:.4g} um, out-of-plane {b0[3]*1e4:.3g} um, dt={b0[5]*1e4:.3g} um/c;"
                      f" those hits sit in (quirk,layer) cells with count mismatch: "
                      f"{sum(1 for r in big if (int(H[int(r[0]),0]), int(H[int(r[0]),1])) in mism)}/{len(big)}", flush=True)
                for r in big[order][:6]:
                    hh = H[int(r[0])]
                    print(f"       q{int(hh[0])} L{int(hh[1])} t={hh[2]:.2f} |d|={r[2]*1e4:.4g} um out={r[3]*1e4:.3g} in={r[4]*1e4:.4g} um dt={r[5]*1e4:.4g} um",
                          flush=True)
                pre = cx[cx[:, 0] < t0]
                ncr = len(pre)
                if ncr:
                    js = np.argsort(pre[:, 1])[:3]
                    print(f"     {ncr} crossings before t0; smallest miss distances before t0 [um] (crossing #, t):"
                          f" {[(round(pre[j,1]*1e4, 3), int(j), round(pre[j,0], 1)) for j in js]}; median miss {np.median(pre[:,1])*1e4:.3g} um,"
                          f" 1/Lambda = {1.9733e-14/(lam*1e-6)*1e4:.3g} um", flush=True)
            if prev is not None:
                Mp, _ = match(H, prev)
                print(f"     Li x{frac:g} vs previous Li step: max|dhit| {Mp[:, 2].max()*1e4:.4g} um, thickness change"
                      f" {abs(plane_thickness(H[:, 3:6]) - plane_thickness(prev[:, 3:6]))*1e4:.3g} um", flush=True)
            prev = H
