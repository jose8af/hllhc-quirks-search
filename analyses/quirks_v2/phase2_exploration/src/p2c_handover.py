"""p2c_handover.py -- Geant4 vertex -> rows of the v1 particle array (STR §4.4 pt 2; hand-over variant A).

Variant A (simulated here): Fatras propagates the charged parent from its origin and v1's `run_chain.Truncate`
removes its hits beyond the vertex radius; the Geant4 products start at the Geant4 vertex.  Variant B (the parent's
Geant4 crossings converted to hits) is built at analysis level from the stored crossings (`gcross`).

Products.  Geant4 records the products at the vertex and stops them (g4hv).  Short-lived products (pi0, K0S, Lambda,
Sigma, eta, ...) are decayed here with Pythia under the production decay settings of s4pu.PY_MB (tau0Max = 1000 mm;
pi+-, K+-, mu, K0L stable), so the photons and displaced daughters reach Fatras as in every other sample.  Selection
into Fatras as s4pu.select_and_place: charged particles and photons, pT > 50 MeV, |eta| < 4, production point inside
rho < 1100 mm, |z| < 2700 mm.  Nuclear fragments and hadrons outside SAFE_PDG are passed with their own charge and
mass under the proton code (the Fatras energy loss and scattering use charge and mass; the code only selects the
electron and photon processes).  Conversion vertices of a primary photon are not handed over (STR §4.4 pt 1).
"""
import math
import sys

import numpy as np

import p2c_common as C

sys.path.insert(0, str(C.CODE))
import s4pu  # noqa: E402
import pythia8  # noqa: E402

GUN_VP = s4pu.GUN_VP
SAFE_PDG = {11, 13, 22, 211, 321, 2212}
CHARGE3 = {11: -3, 13: -3, 211: 3, 321: 3, 2212: 3}
MASS = {11: 0.51099895e-3, 13: 0.1056583755, 211: 0.13957039, 321: 0.493677, 2212: 0.93827209}    # s4cp.py l.33


class Decayer:
    def __init__(self, seed):
        self.py = pythia8.Pythia('', False)
        for ln in ('ProcessLevel:all = off', 'ParticleDecays:limitTau0 = on', 'ParticleDecays:tau0Max = 1000.',
                   '211:mayDecay = off', '321:mayDecay = off', '13:mayDecay = off', '130:mayDecay = off',
                   'Print:quiet = on', 'Next:numberCount = 0', 'Random:setSeed = on', f'Random:seed = {int(seed) % 900000000}'):
            self.py.readString(ln)
        if not self.py.init():
            raise RuntimeError('Pythia decayer init failed')

    def decay(self, prods, seed):
        """prods: (n, 9) pdg, px, py, pz, E, x, y, z (mm), t (ns): each product at its hand-over point.  Returns list of
        (pdg, q, m, x, y, z, t_ns, px, py, pz, displaced: bool, beta) of final particles."""
        py = self.py
        py.rndm.init(int(seed) % 900_000_000)
        ev = py.event
        ev.reset()
        out = []
        start = []
        for pdg, px, py_, pz, e, x0, y0, z0, t0 in prods:
            xv = (x0, y0, z0); tv_ns = t0; tmm = tv_ns * s4pu.C_MM_PER_NS
            pdg = int(pdg)
            m2 = e * e - px * px - py_ * py_ - pz * pz
            m = math.sqrt(max(m2, 0.0))
            if abs(pdg) >= 1000000000:                       # nucleus 100ZZZAAAI: passed directly
                z = (abs(pdg) // 10000) % 1000
                out.append((pdg, float(z), m, xv[0], xv[1], xv[2], tv_ns, px, py_, pz, False,
                            math.sqrt(max(e * e - m2, 0.0)) / max(e, 1e-12)))
                continue
            if not py.particleData.isParticle(pdg):
                continue
            i = ev.append(pdg, 91, 0, 0, px, py_, pz, e, m)
            ev[i].vProd(pythia8.Vec4(xv[0], xv[1], xv[2], tmm))
            ev[i].tau(ev[i].tau0() * py.rndm.exp())
            start.append(xv)
        if ev.size() > 1:
            py.moreDecays()
            for k in range(1, ev.size()):
                p = ev[k]
                if not p.isFinal():
                    continue
                disp = p.mother1() > 0          # daughter of a product decayed here: a later, displaced vertex
                out.append((p.id(), p.charge(), p.m(), p.xProd(), p.yProd(), p.zProd(), p.tProd() / s4pu.C_MM_PER_NS,
                            p.px(), p.py(), p.pz(), disp, p.pAbs() / max(p.e(), 1e-12)))
        return out


def fatras_rows(final):
    """Fatras input selection and vsec numbering: 1 = at the Geant4 vertex, 2.. = one per distinct later decay point."""
    rows = []; keys = {}
    nslow = 0
    for pdg, q, m, x, y, z, t, px, py_, pz, disp, beta in final:
        pt = math.hypot(px, py_)
        if pt <= s4pu.PT_MIN or not (q != 0 or pdg == 22):
            continue
        eta = math.asinh(pz / pt)
        if abs(eta) >= s4pu.ETA_MAX or math.hypot(x, y) >= s4pu.RHO_MAX or abs(z) >= s4pu.Z_MAX:
            continue
        vsec = 1
        if disp:
            vsec = keys.setdefault((round(x, 6), round(y, 6), round(z, 6)), 2 + len(keys))
        code = int(pdg)
        if abs(code) not in SAFE_PDG:
            code = 2212 if q > 0 else -2212
        nslow += beta < 0.1
        rows.append((GUN_VP, vsec, code, q, m, x, y, z, t, px, py_, pz))
    return rows, nslow


def event_rows(v, prods, vcols, decayer, seed):
    """One Geant4 vertex -> (P rows (n, 12) PCOLS, trunc list, n_products_g4, n_injected, n_injected with beta < 0.1)."""
    g = dict(zip(vcols, v))
    pdg = int(g['parent_pdg']); a = abs(pdg)
    rows = []; trunc = []
    if a in CHARGE3:
        q = (CHARGE3[a] / 3.0) * (1 if pdg > 0 else -1)
        rows.append((GUN_VP, 0, pdg, q, MASS[a], g['x0'], g['y0'], g['z0'], g['t0'], g['px0'], g['py0'], g['pz0']))
        trunc.append((GUN_VP, 0, 1, math.hypot(g['x'], g['y'])))
    final = decayer.decay(prods, seed)
    pr, nslow = fatras_rows(final)
    P = np.array(rows + pr, float).reshape(-1, 12)
    return P, trunc, len(prods), len(pr), nslow
