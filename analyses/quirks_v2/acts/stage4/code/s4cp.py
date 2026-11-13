"""code/s4cp.py -- C' topology guns and toys (plan §4.2; G1, 2026-10-13; acts env, numpy + Pythia for the PV-pair spectrum).

Every C' event is one topology instance aimed into one MET road, with all toy particles under one interaction id
vp = GUN_VP (3500); vsec = 0 for particles from the PV, 1 for daughters/prongs of the decay/NI vertex.  The event stores
its own road phi_MET and its own smeared PV draw (sigma 10, 10, 15 um around the true vertex; plan §1.7), both drawn from
the event seed, so the with-PU overlay uses exactly the same PV and road (§4.2 'shared PV').

Topologies (plan §4.2 table and C' bullet; every distribution is an ESTIMATE documented here, G1_REPORT §C'):
  gamma   photon, pT log-uniform 0.5-50 GeV, |eta| < 1, phi = phi_MET + U(-0.1, 0.1)              (converts in Fatras)
  v0      K0S (50 %) / Lambda (50 %), pT log-uniform 0.5-50 GeV; decay point from the exponential in the lab
          (beta gamma c tau: 26.84 / 78.9 mm); charged 2-body mode only (K0S -> pi+ pi- BR 0.692, Lambda -> p pi- BR
          0.639; the BR enters rate_t), isotropic in the rest frame
  pvpair  two charged particles of ONE Pythia minimum-bias interaction (pT > 0.05 GeV, |eta| < 1.2) keeping their pT,
          delta phi, delta eta, rotated so that the pair's mean phi = phi_MET + U(-0.1, 0.1); both as pions with their charges
  looper  pi+- or e+- (50/50), pT U(0.05, 0.7) GeV, |eta| < 0.3, from (x_PV, y_PV, z_PV + U(-0.5, 0.5) mm)
  niR     nuclear-interaction toy at r_NI = R mm (22, 30, 61.5): parent pi+- pT log-uniform 0.5-20 GeV from the PV; its
          Fatras hits beyond r_NI + 0.5 mm are removed (so for 30 / 61.5 mm the parent keeps its L1 / L1+L2 hits);
          n_charged prongs = 1 + Poisson(1.5) (ESTIMATE; plan: multiplicity from the literature UNVERIFIED), pions,
          momenta = 0.7 p_parent x Dirichlet(1,..,1), directions around the parent's direction at the NI point with
          polar angle |N(0, 0.2 rad)| (plan: 0.1-0.3 rad spread) and uniform azimuth; start at the parent's helix point
  dif     decay in flight: parent pi+- / K+- (50/50), pT log-uniform 0.5-10 GeV from the PV; decay radius from the
          lab exponential (c tau 7804 / 3712 mm) restricted to 30-1000 mm (the in-tracker decays, plan §4.2 B_DIF rate
          from Pythia); parent hits beyond the decay radius removed; daughter mu from the 2-body decay (pi/K -> mu nu)
"""
import math

import numpy as np

from s4pu import GUN_VP, hseed, select_and_place  # noqa: F401

B_T = 3.8112
KAPPA = 0.299792458e-3 * B_T          # GeV / mm per unit charge: R[mm] = pT / (KAPPA |q|)
MPI, MK, MP, MMU, ME = 0.13957039, 0.493677, 0.93827209, 0.1056583755, 0.51099895e-3
MK0, MLAM = 0.497611, 1.115683
C_MM_NS = 299.792458
TOPOS = ['gamma', 'v0', 'pvpair', 'looper', 'ni22', 'ni30', 'ni61', 'dif']
AIM = 0.1


def helix_point(x0, p3, q, r_target, t0=0.0, m=MPI, ds=0.05, smax=3000.0):
    """Point, momentum direction and time where the helix from x0 (mm) with momentum p3 (GeV) first reaches transverse
    radius r_target (mm).  B along +z; a positive charge turns clockwise (ACTS/Fatras convention, checked vs Fatras
    hits in G1).  Returns (x3, p3_at_point, t) or None if the radius is not reached."""
    pt = math.hypot(p3[0], p3[1]); phi0 = math.atan2(p3[1], p3[0])
    cot = p3[2] / pt
    w = -q * KAPPA / pt                    # dphi / ds (s = transverse arc length, mm)
    s = np.arange(0.0, smax, ds)
    if abs(w) < 1e-12:
        x = x0[0] + s * math.cos(phi0); y = x0[1] + s * math.sin(phi0)
    else:
        x = x0[0] + (np.sin(phi0 + w * s) - math.sin(phi0)) / w
        y = x0[1] - (np.cos(phi0 + w * s) - math.cos(phi0)) / w
    r = np.hypot(x, y)
    k = np.nonzero(r >= r_target)[0]
    if len(k) == 0:
        return None
    k = k[0]
    if k > 0:   # linear refinement inside the last step
        f = (r_target - r[k - 1]) / max(r[k] - r[k - 1], 1e-12)
        sk = s[k - 1] + f * ds
    else:
        sk = 0.0
    if abs(w) < 1e-12:
        xx = x0[0] + sk * math.cos(phi0); yy = x0[1] + sk * math.sin(phi0); ph = phi0
    else:
        xx = x0[0] + (math.sin(phi0 + w * sk) - math.sin(phi0)) / w
        yy = x0[1] - (math.cos(phi0 + w * sk) - math.cos(phi0)) / w
        ph = phi0 + w * sk
    zz = x0[2] + sk * cot
    pa = math.sqrt(pt * pt + p3[2] ** 2)
    beta = pa / math.sqrt(pa * pa + m * m)
    t = t0 + sk * math.sqrt(1 + cot * cot) / (beta * C_MM_NS)
    return np.array([xx, yy, zz]), np.array([pt * math.cos(ph), pt * math.sin(ph), p3[2]]), t


def two_body(rng, M, P3, m1, m2):
    """Isotropic 2-body decay of a particle of mass M and lab momentum P3 -> lab momenta of the two daughters."""
    pstar = math.sqrt(max((M * M - (m1 + m2) ** 2) * (M * M - (m1 - m2) ** 2), 0.0)) / (2 * M)
    ct = rng.uniform(-1, 1); ph = rng.uniform(0, 2 * math.pi); st = math.sqrt(1 - ct * ct)
    d = np.array([st * math.cos(ph), st * math.sin(ph), ct])
    E1 = math.sqrt(pstar ** 2 + m1 * m1); E2 = math.sqrt(pstar ** 2 + m2 * m2)
    P = np.asarray(P3, float); E = math.sqrt(P @ P + M * M)
    b = P / E; g = E / M; b2 = b @ b
    out = []
    for (Ei, pi) in ((E1, pstar * d), (E2, -pstar * d)):
        bp = b @ pi
        coef = ((g - 1) * bp / b2 + g * Ei) if b2 > 0 else 0.0
        out.append(pi + coef * b)
    return out


def rot_to(dvec, theta, phi):
    """Unit vector at polar angle theta / azimuth phi around the unit vector dvec."""
    d = dvec / np.linalg.norm(dvec)
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = np.cross(d, a); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
    return math.cos(theta) * d + math.sin(theta) * (math.cos(phi) * e1 + math.sin(phi) * e2)


def _p3(pt, eta, phi):
    return np.array([pt * math.cos(phi), pt * math.sin(phi), pt * math.sinh(eta)])


class CPrime:
    def __init__(self, beamspot, minbias=None):
        self.bs = beamspot
        self.mb = minbias          # s4pu.PythiaGen (only for pvpair)

    def event(self, topo, ev_seed):
        """-> (P rows PCOLS, vz rows, info dict incl. pv (stored smeared PV), phimet, trunc [(vp, vsec, particle, r_cut)])."""
        rng = np.random.default_rng(hseed('cp', topo, ev_seed, mod=2 ** 63))
        bs = self.bs
        sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm'], bs['sigma_t_ps'] * 1e-3])
        vtx = rng.normal(0, 1, 4) * sig
        pv = vtx[:3] + rng.normal(0, 1, 3) * np.array([0.010, 0.010, 0.015])
        phimet = rng.uniform(-math.pi, math.pi)
        rows = []; trunc = []

        def add(pdg, q, m, x3, t, p3, vsec, part):
            rows.append((GUN_VP, vsec, pdg, q, m, x3[0], x3[1], x3[2], t, p3[0], p3[1], p3[2]))
            return part

        aim = phimet + rng.uniform(-AIM, AIM)
        x0 = vtx[:3]; t0 = vtx[3]
        if topo == 'gamma':
            pt = math.exp(rng.uniform(math.log(0.5), math.log(50.0)))
            add(22, 0.0, 0.0, x0, t0, _p3(pt, rng.uniform(-1, 1), aim), 0, 1)
        elif topo == 'v0':
            k0 = rng.random() < 0.5
            M, ctau = (MK0, 26.844) if k0 else (MLAM, 78.9)
            pt = math.exp(rng.uniform(math.log(0.5), math.log(50.0)))
            P3 = _p3(pt, rng.uniform(-1, 1), aim); pa = np.linalg.norm(P3)
            L = rng.exponential(pa / M * ctau)
            xd = x0 + L * P3 / pa
            td = t0 + L / (pa / math.sqrt(pa * pa + M * M) * C_MM_NS)
            if k0:
                a, b = two_body(rng, M, P3, MPI, MPI); add(211, 1.0, MPI, xd, td, a, 1, 1); add(-211, -1.0, MPI, xd, td, b, 1, 2)
            else:
                a, b = two_body(rng, M, P3, MP, MPI); add(2212, 1.0, MP, xd, td, a, 1, 1); add(-211, -1.0, MPI, xd, td, b, 1, 2)
        elif topo == 'pvpair':
            for _ in range(1000):
                parts, _ev = self.mb.generate(int(rng.integers(1, 900_000_000)))
                ch = [p for p in parts if p[1] != 0 and math.hypot(p[3], p[4]) > 0.05
                      and abs(math.asinh(p[5] / math.hypot(p[3], p[4]))) < 1.2
                      and abs(p[7]) + abs(p[8]) + abs(p[9]) == 0]
                if len(ch) >= 2:
                    break
            i, j = rng.choice(len(ch), 2, replace=False)
            a, b = ch[i], ch[j]
            phia = math.atan2(a[4], a[3]); phib = math.atan2(b[4], b[3])
            dphi = (phib - phia + math.pi) % (2 * math.pi) - math.pi
            rot = aim - (phia + 0.5 * dphi)
            for k, pp in enumerate((a, b)):
                pt = math.hypot(pp[3], pp[4]); ph = math.atan2(pp[4], pp[3]) + rot
                add(211 if pp[1] > 0 else -211, float(np.sign(pp[1])), MPI, x0, t0,
                    np.array([pt * math.cos(ph), pt * math.sin(ph), pp[5]]), 0, k + 1)
        elif topo == 'looper':
            e = rng.random() < 0.5
            q = float(rng.choice([-1.0, 1.0]))
            pdg = (11 if q < 0 else -11) if e else (211 if q > 0 else -211)
            m = ME if e else MPI
            xs = x0 + np.array([0.0, 0.0, rng.uniform(-0.5, 0.5)])
            add(pdg, q, m, xs, t0, _p3(rng.uniform(0.05, 0.7), rng.uniform(-0.3, 0.3), aim), 0, 1)
        elif topo.startswith('ni'):
            rni = {'ni22': 22.0, 'ni30': 30.0, 'ni61': 61.5}[topo]
            q = float(rng.choice([-1.0, 1.0]))
            pt = math.exp(rng.uniform(math.log(0.5), math.log(20.0)))
            P3 = _p3(pt, rng.uniform(-1, 1), aim)
            add(211 if q > 0 else -211, q, MPI, x0, t0, P3, 0, 1)
            hp = helix_point(x0, P3, q, rni, t0, MPI)
            trunc.append((GUN_VP, 0, 1, rni + 0.5))
            npr = 1 + int(rng.poisson(1.5))
            frac = rng.dirichlet(np.ones(npr)) * 0.7
            pa = np.linalg.norm(hp[1])
            for k in range(npr):
                d = rot_to(hp[1], abs(rng.normal(0, 0.2)), rng.uniform(0, 2 * math.pi))
                qq = float(rng.choice([-1.0, 1.0]))
                add(211 if qq > 0 else -211, qq, MPI, hp[0], hp[2], frac[k] * pa * d, 1, k + 2)
        elif topo == 'dif':
            kaon = rng.random() < 0.5
            M, ctau = (MK, 3712.0) if kaon else (MPI, 7804.5)
            q = float(rng.choice([-1.0, 1.0]))
            pt = math.exp(rng.uniform(math.log(0.5), math.log(10.0)))
            P3 = _p3(pt, rng.uniform(-1, 1), aim); pa = np.linalg.norm(P3)
            lam = pa / M * ctau * (pt / pa)              # mean decay length in the transverse radius (straight line)
            u = rng.uniform(1 - math.exp(-30.0 / lam), 1 - math.exp(-1000.0 / lam))
            rd = -lam * math.log(1 - u)
            add((321 if q > 0 else -321) if kaon else (211 if q > 0 else -211), q, M, x0, t0, P3, 0, 1)
            hp = helix_point(x0, P3, q, rd, t0, M)
            trunc.append((GUN_VP, 0, 1, rd))
            if hp is not None:
                mu, _nu = two_body(rng, M, hp[1] * pa / np.linalg.norm(hp[1]), MMU, 0.0)
                add(-13 if q > 0 else 13, q, MMU, hp[0], hp[2], mu, 1, 2)
        else:
            raise KeyError(topo)
        P = np.array(rows, float).reshape(-1, 12)
        org = P[P[:, 1] == 0][0, 5:9] if (len(P) and (P[:, 1] == 0).any()) else vtx    # the toy's true origin
        vz = np.array([[GUN_VP, *org, *(P[P[:, 1] == 0][:, 9:12].sum(0) if len(P) else np.zeros(3))]])
        return P, vz, dict(topo=topo, pv=pv.tolist(), phimet=phimet, vtx=vtx.tolist(), trunc=trunc, n_particles=len(P))
