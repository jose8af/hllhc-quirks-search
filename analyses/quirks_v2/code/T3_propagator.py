"""T3_propagator.py -- quirk-pair propagator through the CMS Phase-2 B field and material
(theory track, investigator T3).

Purpose
-------
Fast (numba) lab-frame integrator of the two quirk endpoints joined by a straight Nambu-Goto string,
with (i) the Lorentz force in a uniform / simplified-CMS / solenoid-map field, and (ii) material
effects applied by operator splitting after every accepted integration step:
    * mean ionisation energy loss (Bethe, no density effect; linear below beta = 0.02, as in
      T6_stopping.py, so that f_stop is computed with the same stopping power that T6 used);
    * energy-loss straggling (Gaussian, Bohr variance) -- optional;
    * multiple Coulomb scattering (Highland, PDG RPP 2024 Eq.34.16, applied as a Gaussian 3D
      deflection with variance proportional to the path length in the step) -- optional.
The string model is the same as T2_propagator.LabStraightString (Kang-Luty endpoint force
[0805.4642 Eq.3.8] with s_hat along the lab-simultaneous separation), which T2 showed to be EXACT
in vacuum (T2_test_propagator.py); it is re-implemented here in numba because the solve_ivp version
is ~10^3 x too slow for 10^3-10^5 string crossings per event.  Validation against T2's ExactPair and
LabStraightString: T3_test_propagator.py.

Units: cm, GeV, c = 1 (time in cm; divide by 29.979 for ns).  B in tesla.  sigma in GeV/cm
(sigma_from_lambda_keV from T2_propagator).

Material model (see T3 report Sec.2): `phase2_tracker()` returns thin cylindrical slabs (radius,
x/X0 at normal incidence, physical radial width, half-length).  Outside the tracker the Evans-Luty
cylindrical CMS model [1811.08903 Tab.1] (density rho_m x fill factor zeta) is used
(`cms_outer_regions()`).

How to run: this is a library.  `pixi run python code/T3_test_propagator.py` runs the checks.
"""
from __future__ import annotations

import os
import sys
import numpy as np
from numba import njit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from T2_propagator import sigma_from_lambda_keV, C_CM_PER_NS, EB_GEV_PER_CM_PER_T  # noqa: E402

ME = 0.51099895e-3          # GeV
KBB = 0.307075e-3            # GeV cm^2 / mol  (PDG K)
X0_SI = 9.37                 # cm

# material codes: 0 vacuum, 1 Si, 2 PbWO4, 3 Cu(brass), 4 Fe, 5 air
#            Z/A      I [GeV]     X0 [cm]   rho [g/cm3]
MAT = np.array([
    [0.0,     1.0e-7,  1e30,    0.0],
    [0.49848, 173e-9,  9.370,   2.329],
    [0.41315, 600.7e-9, 0.8903, 8.300],
    [0.45636, 322e-9,  1.436,   8.960],
    [0.46557, 286e-9,  1.757,   7.874],
    [0.49919, 85.7e-9, 30390.,  0.0012],
])


# ------------------------------------------------------------------------------------------------
# Geometry / material
# ------------------------------------------------------------------------------------------------
def phase2_tracker(scale=1.0, it_layers=(3.0, 6.1, 10.4, 14.6), ot_layers=(24.9, 37.2, 52.3, 68.8, 86.0, 108.3)):
    """Thin cylindrical slabs: columns R [cm], x/X0 (normal incidence), radial width w [cm], |z| half-length [cm],
    is_sensor (1 = recorded as a hit layer).  Numbers and their status: report Sec.2 (mostly UNVERIFIED)."""
    rows = [[2.2, 0.0023, 0.1, 300.0, 0]]                           # Be beam pipe 0.8 mm
    for R in it_layers:
        rows.append([R, 0.012, 1.0, 20.0, 1])                         # TBPX: module 0.825% [2407.13721 Tab.1] + support
    rows.append([19.0, 0.010, 1.0, 120.0, 0])                         # IT service cylinder (UNVERIFIED)
    for R in ot_layers[:3]:
        rows.append([R, 0.025, 2.0, 120.0, 1])                        # PS layers (UNVERIFIED)
    for R in ot_layers[3:]:
        rows.append([R, 0.018, 2.0, 120.0, 1])                        # 2S layers (UNVERIFIED)
    a = np.array(rows, float)
    a[:, 1] *= scale
    return a


def cms_outer_regions():
    """Evans-Luty cylindrical CMS [1811.08903 Tab.1]: rmin, rmax, zmin, zmax, material code, zeta,
    rmin_is_eta3 (1: inner radius set by eta = 3 at given z).  Tracker volume handled by slabs."""
    R = [
        # ECal barrel and endcap
        [118.5, 181.1, 0.0, 293.5, 2, 0.33, 0],
        [0.0, 181.1, 293.5, 390.0, 2, 0.33, 1],
        # HCal
        [181.1, 286.4, 0.0, 568.0, 3, 0.68, 0],
        [0.0, 286.4, 390.0, 568.0, 3, 0.68, 1],
        # Magnet (coil + cryostat) as iron, zeta 0.5
        [295.0, 380.0, 0.0, 645.0, 4, 0.5, 0],
        # Muon-system barrel iron
        [380.0, 410.0, 0.0, 140.0, 4, 1.0, 0],
        [455.0, 490.5, 0.0, 724.0, 4, 1.0, 0],
        [528.5, 597.5, 0.0, 661.0, 4, 1.0, 0],
        [635.5, 700.0, 0.0, 661.0, 4, 1.0, 0],
        # Muon-system endcap iron
        [0.0, 105.0, 568.0, 630.0, 4, 1.0, 1],
        [0.0, 270.0, 630.0, 724.0, 4, 1.0, 1],
        [0.0, 695.5, 724.0, 791.5, 4, 1.0, 1],
        [0.0, 129.0, 791.5, 849.5, 4, 1.0, 1],
        [0.0, 695.5, 849.5, 917.0, 4, 1.0, 1],
        [0.0, 140.0, 917.0, 975.0, 4, 1.0, 1],
        [0.0, 695.5, 975.0, 1005.0, 4, 1.0, 1],
        [0.0, 150.0, 1005.0, 1063.0, 4, 1.0, 1],
        [0.0, 695.5, 1063.0, 1083.0, 4, 1.0, 1],
    ]
    return np.array(R, float)


REGION_NAMES = ['ECAL', 'ECAL-EC', 'HCAL', 'HCAL-EC', 'coil', 'MB1-Fe', 'MB2-Fe', 'MB3-Fe', 'MB4-Fe'] + \
               [f'ME-Fe{i}' for i in range(9)]


# ------------------------------------------------------------------------------------------------
# numba kernels
# ------------------------------------------------------------------------------------------------
@njit(cache=True)
def stopping_power(beta, q2, za_rho, I):
    """Mean dE/dx [GeV/cm] (Bethe without density effect; L >= 0.6; linear in beta below 0.02)."""
    if za_rho <= 0.0:
        return 0.0
    bp = 0.02
    b = beta if beta > bp else bp
    g2 = 1.0 / (1.0 - b * b)
    L = np.log(2.0 * ME * b * b * g2 / I)
    if L < 0.6:
        L = 0.6
    s = KBB * za_rho * q2 / (b * b) * (L - b * b)
    if beta < bp:
        s *= beta / bp
    return s


@njit(cache=True)
def material_at(x, y, z, slabs, regions, mat):
    """Return (za_rho [g/cm3 * Z/A], I [GeV], X0_eff [cm], layer_xX0, region id).
    region id: -1 vacuum/air, 100+k tracker slab k, j outer region j."""
    r = np.sqrt(x * x + y * y)
    az = abs(z)
    if r < 118.5 and az < 293.5:
        for k in range(slabs.shape[0]):
            R = slabs[k, 0]; w = slabs[k, 2]
            if abs(r - R) < 0.5 * w and az < slabs[k, 3]:
                xX0 = slabs[k, 1]
                rho = mat[1, 3] * xX0 * mat[1, 2] / w
                return mat[1, 0] * rho, mat[1, 1], w / xX0, xX0, 100 + k
        return 0.0, 1.0, 1e30, 1.0, -1
    for j in range(regions.shape[0]):
        rmin = regions[j, 0]
        if regions[j, 6] > 0.5:
            rmin = az / np.sinh(3.0)
        if r >= rmin and r < regions[j, 1] and az >= regions[j, 2] and az < regions[j, 3]:
            mc = int(regions[j, 4]); zeta = regions[j, 5]
            return mat[mc, 0] * mat[mc, 3] * zeta, mat[mc, 1], mat[mc, 2] / zeta, 1.0, j
    return mat[5, 0] * mat[5, 3], mat[5, 1], mat[5, 2], 1.0, -1


@njit(cache=True)
def bfield(x, y, z, bmode, B0, bgrid, rgrid, zgrid):
    """bmode 0: uniform B0 zhat; 1: simplified CMS (B0 inside r<295,|z|<645; -1.8 T in barrel yoke iron
    r 380-700, |z|<661; 0 elsewhere); 2: (Br, Bz) map on (rgrid, zgrid), axisymmetric, scaled so Bz(0,0)=B0."""
    if bmode == 0:
        return 0.0, 0.0, B0
    r = np.sqrt(x * x + y * y)
    az = abs(z)
    if bmode == 1:
        if r < 295.0 and az < 645.0:
            return 0.0, 0.0, B0
        if r >= 380.0 and r < 700.0 and az < 661.0:
            if (r < 410.0 and az < 140.0) or (r >= 455.0 and r < 490.5) or (r >= 528.5 and r < 597.5) or (r >= 635.5):
                return 0.0, 0.0, -1.8
        return 0.0, 0.0, 0.0
    # bmode 2: bilinear interpolation on (r, |z|); Br odd in z
    nr = rgrid.shape[0]; nz = zgrid.shape[0]
    dr = rgrid[1] - rgrid[0]; dz = zgrid[1] - zgrid[0]
    fr = (r - rgrid[0]) / dr; fz = (az - zgrid[0]) / dz
    i = int(fr); j = int(fz)
    if i < 0: i = 0
    if j < 0: j = 0
    if i > nr - 2: i = nr - 2
    if j > nz - 2: j = nz - 2
    a = fr - i; b = fz - j
    br = (1 - a) * (1 - b) * bgrid[0, i, j] + a * (1 - b) * bgrid[0, i + 1, j] + (1 - a) * b * bgrid[0, i, j + 1] + a * b * bgrid[0, i + 1, j + 1]
    bz = (1 - a) * (1 - b) * bgrid[1, i, j] + a * (1 - b) * bgrid[1, i + 1, j] + (1 - a) * b * bgrid[1, i, j + 1] + a * b * bgrid[1, i + 1, j + 1]
    if z < 0:
        br = -br
    if r > 0:
        return br * x / r, br * y / r, bz
    return 0.0, 0.0, bz


@njit(cache=True)
def rhs(y, out, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid):
    dx = y[0] - y[6]; dy = y[1] - y[7]; dz = y[2] - y[8]
    nd = np.sqrt(dx * dx + dy * dy + dz * dz)
    if nd > 0.0:
        sx = dx / nd; sy = dy / nd; sz = dz / nd
    else:
        # production point: s_hat = unit(v1 - v2) (exact lab string direction, T2 report Sec.2.1)
        Ea = np.sqrt(m1 * m1 + y[3] ** 2 + y[4] ** 2 + y[5] ** 2)
        Eb = np.sqrt(m2 * m2 + y[9] ** 2 + y[10] ** 2 + y[11] ** 2)
        sx = y[3] / Ea - y[9] / Eb; sy = y[4] / Ea - y[10] / Eb; sz = y[5] / Ea - y[11] / Eb
        nn = np.sqrt(sx * sx + sy * sy + sz * sz)
        if nn > 0:
            sx /= nn; sy /= nn; sz /= nn
    for i in range(2):
        o = 6 * i
        m = m1 if i == 0 else m2
        q = q1 if i == 0 else q2
        sg = 1.0 if i == 0 else -1.0
        px = y[o + 3]; py = y[o + 4]; pz = y[o + 5]
        E = np.sqrt(m * m + px * px + py * py + pz * pz)
        vx = px / E; vy = py / E; vz = pz / E
        ux = sg * sx; uy = sg * sy; uz = sg * sz
        vpar = vx * ux + vy * uy + vz * uz
        wx = vx - vpar * ux; wy = vy - vpar * uy; wz = vz - vpar * uz
        vp2 = wx * wx + wy * wy + wz * wz
        root = np.sqrt(max(1.0 - vp2, 1e-300))
        fx = -sigma * (root * ux + vpar * wx / root)
        fy = -sigma * (root * uy + vpar * wy / root)
        fz = -sigma * (root * uz + vpar * wz / root)
        if q != 0.0 and (B0 != 0.0 or bmode == 2):
            bx, by, bz = bfield(y[o], y[o + 1], y[o + 2], bmode, B0, bgrid, rgrid, zgrid)
            c = q * EB_GEV_PER_CM_PER_T
            fx += c * (vy * bz - vz * by)
            fy += c * (vz * bx - vx * bz)
            fz += c * (vx * by - vy * bx)
        out[o] = vx; out[o + 1] = vy; out[o + 2] = vz
        out[o + 3] = fx; out[o + 4] = fy; out[o + 5] = fz


# Dormand-Prince 5(4) tableau
A21 = 1 / 5
A31, A32 = 3 / 40, 9 / 40
A41, A42, A43 = 44 / 45, -56 / 15, 32 / 9
A51, A52, A53, A54 = 19372 / 6561, -25360 / 2187, 64448 / 6561, -212 / 729
A61, A62, A63, A64, A65 = 9017 / 3168, -355 / 33, 46732 / 5247, 49 / 176, -5103 / 18656
B1, B3, B4, B5, B6 = 35 / 384, 500 / 1113, 125 / 192, -2187 / 6784, 11 / 84
E1, E3, E4, E5, E6, E7 = 71 / 57600, -71 / 16695, 71 / 1920, -17253 / 339200, 22 / 525, -1 / 40


@njit(cache=True)
def _apply_material(y, i, m, q, h, slabs, regions, mat, do_eloss, do_strag, do_ms, eacc):
    """Material kick on endpoint i over a time step h (path |v| h) at its current position."""
    o = 6 * i
    px = y[o + 3]; py = y[o + 4]; pz = y[o + 5]
    p = np.sqrt(px * px + py * py + pz * pz)
    if p <= 0.0:
        return
    E = np.sqrt(m * m + p * p)
    beta = p / E
    za_rho, I, X0, xlay, reg = material_at(y[o], y[o + 1], y[o + 2], slabs, regions, mat)
    if za_rho <= 0.0:
        return
    ds = beta * h
    q2 = q * q
    if do_eloss:
        dE = stopping_power(beta, q2, za_rho, I) * ds
        if do_strag:
            g2 = 1.0 / (1.0 - beta * beta)
            var = 0.1569e-6 * za_rho * ds * q2 * (1.0 - 0.5 * beta * beta) * g2   # GeV^2 (Bohr)
            dE += np.sqrt(var) * np.random.normal()
            if dE < 0.0:
                dE = 0.0
        eacc[i] += dE
        Ek = E - m - dE
        if Ek <= 1e-9 * m:
            Ek = 1e-9 * m
        pn = np.sqrt((Ek + m) ** 2 - m * m)
        f = pn / p
        px *= f; py *= f; pz *= f; p = pn
        E = Ek + m; beta = p / E
    if do_ms and X0 < 1e29:
        xr = xlay / (beta * beta) * q2
        if xr < 1e-4:
            xr = 1e-4
        flog = 1.0 + 0.038 * np.log(xr)
        if flog < 0.5:
            flog = 0.5
        th0 = 13.6e-3 / (beta * p) * abs(q) * np.sqrt(ds / X0) * flog
        t1 = th0 * np.random.normal(); t2 = th0 * np.random.normal()
        # orthonormal basis perpendicular to p
        ux = px / p; uy = py / p; uz = pz / p
        if abs(ux) < 0.9:
            ax, ay, az = 1.0, 0.0, 0.0
        else:
            ax, ay, az = 0.0, 1.0, 0.0
        e1x = uy * az - uz * ay; e1y = uz * ax - ux * az; e1z = ux * ay - uy * ax
        n1 = np.sqrt(e1x * e1x + e1y * e1y + e1z * e1z)
        e1x /= n1; e1y /= n1; e1z /= n1
        e2x = uy * e1z - uz * e1y; e2y = uz * e1x - ux * e1z; e2z = ux * e1y - uy * e1x
        th = np.sqrt(t1 * t1 + t2 * t2)
        if th > 0:
            c = np.cos(th); s = np.sin(th) / th
            px = p * (c * ux + s * (t1 * e1x + t2 * e2x))
            py = p * (c * uy + s * (t1 * e1y + t2 * e2y))
            pz = p * (c * uz + s * (t1 * e1z + t2 * e2z))
    y[o + 3] = px; y[o + 4] = py; y[o + 5] = pz


@njit(cache=True)
def propagate(y0, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid,
              slabs, regions, mat, rec_radii, rec_zmax,
              do_eloss, do_strag, do_ms, t_end, r_exit, z_exit, beta_stop,
              rtol, atol_x, atol_p, hmax_trk, hmax_out, seed, max_hits, max_steps):
    """Integrate from t = 0.  Returns (status, t, y, hits[n,9], n_hits, eacc[2], nsteps, nkick).
    hits columns: quirk, record-layer index, t, x, y, z, beta, |p|, crossing count of that quirk on layer.
    status: 0 t_end reached, 1 both quirks outside (r_exit, z_exit), 2 stopped (pair beta < beta_stop and
    inside material), 3 max_steps."""
    if seed >= 0:
        np.random.seed(seed)
    y = y0.copy()
    yn = np.empty(12); ye = np.empty(12)
    k1 = np.empty(12); k2 = np.empty(12); k3 = np.empty(12); k4 = np.empty(12)
    k5 = np.empty(12); k6 = np.empty(12); k7 = np.empty(12); tmp = np.empty(12)
    hits = np.zeros((max_hits, 9))
    nh = 0
    eacc = np.zeros(2)
    ncnt = np.zeros((2, rec_radii.shape[0]))
    t = 0.0
    rhs(y, k1, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
    h = 1e-6
    status = 0
    nsteps = 0
    nkick = 0
    nland = 0
    while t < t_end:
        if nsteps >= max_steps:
            status = 3
            break
        r1 = np.sqrt(y[0] ** 2 + y[1] ** 2); r2 = np.sqrt(y[6] ** 2 + y[7] ** 2)
        inside_trk = (r1 < 120.0 and abs(y[2]) < 300.0) or (r2 < 120.0 and abs(y[8]) < 300.0)
        hmax = hmax_trk if inside_trk else hmax_out
        if h > hmax:
            h = hmax
        if t + h > t_end:
            h = t_end - t
        # --- DP45 step
        for j in range(12):
            tmp[j] = y[j] + h * A21 * k1[j]
        rhs(tmp, k2, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        for j in range(12):
            tmp[j] = y[j] + h * (A31 * k1[j] + A32 * k2[j])
        rhs(tmp, k3, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        for j in range(12):
            tmp[j] = y[j] + h * (A41 * k1[j] + A42 * k2[j] + A43 * k3[j])
        rhs(tmp, k4, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        for j in range(12):
            tmp[j] = y[j] + h * (A51 * k1[j] + A52 * k2[j] + A53 * k3[j] + A54 * k4[j])
        rhs(tmp, k5, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        for j in range(12):
            tmp[j] = y[j] + h * (A61 * k1[j] + A62 * k2[j] + A63 * k3[j] + A64 * k4[j] + A65 * k5[j])
        rhs(tmp, k6, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        for j in range(12):
            yn[j] = y[j] + h * (B1 * k1[j] + B3 * k3[j] + B4 * k4[j] + B5 * k5[j] + B6 * k6[j])
        rhs(yn, k7, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
        err = 0.0
        for j in range(12):
            ye[j] = h * (E1 * k1[j] + E3 * k3[j] + E4 * k4[j] + E5 * k5[j] + E6 * k6[j] + E7 * k7[j])
        # error norm on relative (x1-x2, p1-p2) and centre (x1+x2, p1+p2) variables, so that the tolerance
        # on the separation is relative to the separation, not to the distance from the origin
        for j in range(6):
            a = atol_x if j < 3 else atol_p
            er = ye[j] - ye[6 + j]; ec = ye[j] + ye[6 + j]
            sr = a + rtol * max(abs(y[j] - y[6 + j]), abs(yn[j] - yn[6 + j]))
            scc = a + rtol * max(abs(y[j] + y[6 + j]), abs(yn[j] + yn[6 + j]))
            err = max(err, abs(er) / sr, abs(ec) / scc)
        if err > 1.0:
            h *= max(0.1, 0.9 * err ** (-0.2))
            if h < 1e-14:
                h = 1e-14
                # accept anyway (should not happen)
            else:
                continue
        # --- string crossing inside the step: shorten the step to land just past the crossing so that the
        #     force discontinuity (s_hat flip) always sits on a step boundary (as solve_ivp events in T2)
        d0x = y[0] - y[6]; d0y = y[1] - y[7]; d0z = y[2] - y[8]
        n0 = np.sqrt(d0x * d0x + d0y * d0y + d0z * d0z)
        if n0 > 0.0 and nland < 30:
            gb = ((yn[0] - yn[6]) * d0x + (yn[1] - yn[7]) * d0y + (yn[2] - yn[8]) * d0z) / n0
            if gb < 0.0:
                # Hermite estimate of the fraction f where g = d.s_ref = 0
                flo = 0.0; fhi = 1.0
                for it in range(60):
                    f = 0.5 * (flo + fhi)
                    h00 = 2 * f ** 3 - 3 * f ** 2 + 1; h10 = f ** 3 - 2 * f ** 2 + f
                    h01 = -2 * f ** 3 + 3 * f ** 2; h11 = f ** 3 - f ** 2
                    g = 0.0
                    for c3 in range(3):
                        dc = h00 * (y[c3] - y[6 + c3]) + h10 * h * (k1[c3] - k1[6 + c3]) \
                            + h01 * (yn[c3] - yn[6 + c3]) + h11 * h * (k7[c3] - k7[6 + c3])
                        g += dc * (d0x, d0y, d0z)[c3] / n0
                    if g > 0.0:
                        flo = f
                    else:
                        fhi = f
                if fhi < 1.0 - 1e-6:
                    h = h * fhi * (1.0 + 1e-6) + 1e-15
                    nland += 1
                    continue
        nland = 0
        nsteps += 1
        # --- accepted: record radius crossings (linear interpolation)
        for i in range(2):
            o = 6 * i
            ra = np.sqrt(y[o] ** 2 + y[o + 1] ** 2); rb = np.sqrt(yn[o] ** 2 + yn[o + 1] ** 2)
            for L in range(rec_radii.shape[0]):
                R = rec_radii[L]
                if (ra - R) * (rb - R) < 0.0:
                    # cubic Hermite interpolation of x(t) on the step (positions + velocities k1, k7)
                    flo = 0.0; fhi = 1.0
                    for it in range(50):
                        f = 0.5 * (flo + fhi)
                        h00 = 2 * f ** 3 - 3 * f ** 2 + 1; h10 = f ** 3 - 2 * f ** 2 + f
                        h01 = -2 * f ** 3 + 3 * f ** 2; h11 = f ** 3 - f ** 2
                        xc = h00 * y[o] + h10 * h * k1[o] + h01 * yn[o] + h11 * h * k7[o]
                        yc = h00 * y[o + 1] + h10 * h * k1[o + 1] + h01 * yn[o + 1] + h11 * h * k7[o + 1]
                        rc = np.sqrt(xc * xc + yc * yc)
                        if (rc - R) * (ra - R) > 0.0:
                            flo = f
                        else:
                            fhi = f
                    zc = h00 * y[o + 2] + h10 * h * k1[o + 2] + h01 * yn[o + 2] + h11 * h * k7[o + 2]
                    if abs(zc) < rec_zmax[L] and nh < max_hits:
                        ncnt[i, L] += 1
                        hits[nh, 0] = i; hits[nh, 1] = L; hits[nh, 2] = t + f * h
                        hits[nh, 3] = xc; hits[nh, 4] = yc
                        hits[nh, 5] = zc
                        pp = np.sqrt(yn[o + 3] ** 2 + yn[o + 4] ** 2 + yn[o + 5] ** 2)
                        mm = m1 if i == 0 else m2
                        hits[nh, 6] = pp / np.sqrt(mm * mm + pp * pp); hits[nh, 7] = pp
                        hits[nh, 8] = ncnt[i, L]
                        nh += 1
        for j in range(12):
            y[j] = yn[j]
        t += h
        # --- material (operator splitting)
        if do_eloss or do_ms:
            _apply_material(y, 0, m1, q1, h, slabs, regions, mat, do_eloss, do_strag, do_ms, eacc)
            _apply_material(y, 1, m2, q2, h, slabs, regions, mat, do_eloss, do_strag, do_ms, eacc)
            rhs(y, k1, m1, m2, sigma, q1, q2, bmode, B0, bgrid, rgrid, zgrid)
            nkick += 1
        else:
            for j in range(12):
                k1[j] = k7[j]
        # --- step size update
        if err > 0:
            h *= min(5.0, 0.9 * err ** (-0.2))
        else:
            h *= 5.0
        # --- termination checks
        r1 = np.sqrt(y[0] ** 2 + y[1] ** 2); r2 = np.sqrt(y[6] ** 2 + y[7] ** 2)
        if (r1 > r_exit or abs(y[2]) > z_exit) and (r2 > r_exit or abs(y[8]) > z_exit):
            status = 1
            break
        if beta_stop > 0.0 and (nsteps % 64) == 0:
            Px = y[3] + y[9]; Py = y[4] + y[10]; Pz = y[5] + y[11]
            Ea = np.sqrt(m1 * m1 + y[3] ** 2 + y[4] ** 2 + y[5] ** 2)
            Eb = np.sqrt(m2 * m2 + y[9] ** 2 + y[10] ** 2 + y[11] ** 2)
            dd = np.sqrt((y[0] - y[6]) ** 2 + (y[1] - y[7]) ** 2 + (y[2] - y[8]) ** 2)
            Et = Ea + Eb + sigma * dd
            if np.sqrt(Px * Px + Py * Py + Pz * Pz) / Et < beta_stop:
                status = 2
                break
    return status, t, y, hits[:nh].copy(), nh, eacc, nsteps, nkick


# ------------------------------------------------------------------------------------------------
# Python-side helpers
# ------------------------------------------------------------------------------------------------
DUMMY_GRID = (np.zeros((2, 2, 2)), np.array([0.0, 1.0]), np.array([0.0, 1.0]))

REC_RADII = np.array([3.0, 6.1, 10.4, 14.6, 24.9, 37.2, 52.3, 68.8, 86.0, 108.3, 114.8, 129.0])
REC_ZMAX = np.array([20.0] * 4 + [120.0] * 6 + [130.0, 300.0])
REC_NAMES = ['IT1', 'IT2', 'IT3', 'IT4', 'PS1', 'PS2', 'PS3', '2S1', '2S2', '2S3', 'BTL', 'ECALface']


def run_pair(p1, p2, m, lam_keV, B0=3.8112, bmode=0, material=True, ms=True, eloss=True, strag=True,
             slabs=None, regions=None, t_end=None, r_exit=118.0, z_exit=290.0, beta_stop=0.0,
             rtol=1e-9, seed=1, charges=(1.0, -1.0), hmax_trk=0.5, hmax_out=2.0, grid=None,
             max_hits=200000, max_steps=200_000_000, rec_radii=REC_RADII, rec_zmax=REC_ZMAX):
    """Propagate one pair produced at the origin.  Returns dict with hits, final state, status."""
    sig = sigma_from_lambda_keV(lam_keV)
    if slabs is None:
        slabs = phase2_tracker()
    if regions is None:
        regions = cms_outer_regions()
    if grid is None:
        grid = DUMMY_GRID
    y0 = np.r_[0, 0, 0, np.asarray(p1, float), 0, 0, 0, np.asarray(p2, float)].astype(float)
    if t_end is None:
        P = np.asarray(p1) + np.asarray(p2)
        E = np.hypot(m, np.linalg.norm(p1)) + np.hypot(m, np.linalg.norm(p2))
        bT = np.hypot(P[0], P[1]) / E
        t_end = 1.3 * r_exit / max(bT, 0.02) + 50.0
    out = propagate(y0, float(m), float(m), sig, float(charges[0]), float(charges[1]), int(bmode), float(B0),
                    grid[0], grid[1], grid[2], slabs, regions, MAT, np.asarray(rec_radii, float),
                    np.asarray(rec_zmax, float), bool(material and eloss), bool(material and strag),
                    bool(material and ms), float(t_end), float(r_exit), float(z_exit), float(beta_stop),
                    float(rtol), 1e-12, 1e-10, float(hmax_trk), float(hmax_out), int(seed), int(max_hits),
                    int(max_steps))
    status, t, y, hits, nh, eacc, nsteps, nkick = out
    return dict(status=status, t=t, y=y, hits=hits, eacc=eacc, nsteps=nsteps)


def plane_fit(points):
    """Best plane through the origin: returns (thickness = sqrt(min eigenvalue of T_ij = sum h_i h_j/(N-1)),
    unit normal) [1708.02243 Eq.11; 2002.07503 Eq.C.1]."""
    h = np.asarray(points, float)
    T = h.T @ h / (len(h) - 1)
    w, v = np.linalg.eigh(T)
    return np.sqrt(max(w[0], 0.0)), v[:, 0]


# ------------------------------------------------------------------------------------------------
# Event sampling from the T2 kinematics cache (LO DY + ISR, pT(QQ) > 200 GeV; or inclusive pT = 0)
# ------------------------------------------------------------------------------------------------
_CACHE = None


def load_cache():
    global _CACHE
    if _CACHE is None:
        # T2 keeps the ~170 MB cache outside the project (T2_kinematics.py, env T2_CACHE)
        path = os.environ.get('T2_CACHE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'cache', 'T2_kinematics_cache.npz'))
        if not os.path.exists(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'T2_kinematics_cache.npz')
        _CACHE = np.load(path)
    return _CACHE


def sample_events(m, n, sample='isr', spin='F', rng=None, eta_max=None, ptmin=None):
    """Draw n pairs (p1, p2) [GeV] from T2's weighted LO samples (T2_kinematics.py).  The cache stores
    gamma*, cos(theta*) w.r.t. the pair velocity, (beta gamma)_pair and eta_pair; phi and the azimuth of
    the quirk axis around the pair velocity are drawn uniformly (ESTIMATE quality, see T2 report Sec.3)."""
    rng = rng or np.random.default_rng(1)
    c = load_cache()
    key = f'{spin}_{int(m)}_{sample}'
    w = c[key + '_w']; gs = c[key + '_gamma_star']; cs = c[key + '_cstar']; bg = c[key + '_bg_pair']; eta = c[key + '_eta_pair']
    M = 2 * m * gs
    Pmag = M * bg
    pt = Pmag / np.cosh(eta)
    sel = np.ones(len(w), bool)
    if eta_max is not None:
        sel &= np.abs(eta) < eta_max
    if ptmin is not None:
        sel &= pt > ptmin
    idx_all = np.where(sel)[0]
    p = w[idx_all] / w[idx_all].sum()
    idx = rng.choice(idx_all, size=n, p=p)
    out = []
    for k in idx:
        phi = rng.uniform(0, 2 * np.pi)
        if sample == 'incl':
            P = np.array([0.0, 0.0, np.sign(eta[k]) * Pmag[k]])
        else:
            P = np.array([pt[k] * np.cos(phi), pt[k] * np.sin(phi), Pmag[k] * np.tanh(eta[k])])
        E = np.hypot(M[k], Pmag[k])
        b = P / E
        bh = b / np.linalg.norm(b) if np.linalg.norm(b) > 0 else np.array([0, 0, 1.0])
        tmpv = np.array([1.0, 0, 0]) if abs(bh[0]) < 0.9 else np.array([0, 1.0, 0])
        e1 = np.cross(bh, tmpv); e1 /= np.linalg.norm(e1); e2 = np.cross(bh, e1)
        ct = cs[k]; st = np.sqrt(max(0.0, 1 - ct * ct)); ph = rng.uniform(0, 2 * np.pi)
        n_ = ct * bh + st * (np.cos(ph) * e1 + np.sin(ph) * e2)
        ps = m * np.sqrt(gs[k] ** 2 - 1); e_ = np.hypot(m, ps)
        g = E / M[k]; b2 = b @ b
        pv = []
        for sgn in (1, -1):
            q = sgn * ps * n_
            bp = b @ q
            pv.append(q + (((g - 1) * bp / b2 if b2 > 0 else 0.0) + g * e_) * b)
        out.append((pv[0], pv[1], dict(gstar=gs[k], cstar=ct, bg=bg[k], eta=eta[k], pt=pt[k], M=M[k], w=w[k])))
    return out
