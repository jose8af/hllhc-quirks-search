"""code/s4pu.py -- Stage-4 PRODUCTION generators (G1, 2026-10-13; acts env).  Plan §1.4, §1.8, §4.2.

Pythia8 (CP5, 14 TeV) -> numpy particle arrays -> (run_chain.ParticleSource) acts.examples.SimParticle objects.  There is
NO HepMC3 step (plan §1.4: the Python HepMC3 transport cost 4.6 s per PU-200 event).

Particle array (one row per particle that enters Fatras), columns PCOLS:
  vp     interaction id = ACTS barcode vertexPrimary (PU: 1..n_int; hard scatter HS_VP; guns/toys GUN_VP)
  vsec   0 for particles from the interaction point, >= 1 for each distinct displaced Pythia decay vertex
  pdg, q, m [GeV], x, y, z [mm], t [ns], px, py, pz [GeV]
Vertices (vz rows): vp, x, y, z [mm], t [ns], sum px, sum py, sum pz of the selected prompt particles.

Selection into Fatras (plan §1.4): final-state charged particles and photons with pT > 50 MeV, |eta| < 4, production point
inside rho < 1100 mm, |z| < 2700 mm.  (The probe/interim chains also passed neutral hadrons with removeNeutral = False;
without hadronic physics in Fatras they leave no hits, so dropping them changes no hit.)
Decays as the probes (s4pu probe PY_LINES): K0S, Lambda, hyperons decayed by Pythia (tau0Max = 1000 mm, daughters at the
displaced vertex); pi+-, K+-, mu, K0L stable (Fatras does no decays).
Seeds: every interaction is generated after Pythia's RNG is re-initialised with its own seed (rndm.init), so an
interaction is reproducible from (event seed, interaction index) alone, independent of chunking.
"""
import hashlib
import math

import numpy as np
import pythia8

PCOLS = ['vp', 'vsec', 'pdg', 'q', 'm', 'x', 'y', 'z', 't', 'px', 'py', 'pz']
C_MM_PER_NS = 299.792458
HS_VP = 3000          # hard-scatter interaction (SM samples)
GUN_VP = 3500         # guns / toys (C')
SIG_VP = 4000         # Stage-3 quirks (plan §1.3)
PY_MB = ("Beams:eCM = 14000.", "SoftQCD:inelastic = on", "ParticleDecays:limitTau0 = on", "ParticleDecays:tau0Max = 1000.",
         "211:mayDecay = off", "321:mayDecay = off", "13:mayDecay = off", "130:mayDecay = off", "Print:quiet = on",
         "Next:numberCount = 0", "Next:numberShowEvent = 0", "Next:numberShowInfo = 0", "Next:numberShowProcess = 0")
PT_MIN, ETA_MAX, RHO_MAX, Z_MAX = 0.05, 4.0, 1100.0, 2700.0


def hseed(*parts, mod=900_000_000):
    """Deterministic seed from strings/ints (blake2b, as the Stage-3 rule)."""
    s = '|'.join(str(p) for p in parts)
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % mod


def load_beamspot(tt):
    import json
    return json.loads((tt / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())['beamspot']


class PythiaGen:
    """One Pythia instance, initialised once; generate(seed) re-seeds the RNG per interaction."""

    def __init__(self, cp5_path, extra_lines=(), base_lines=PY_MB, init_seed=1):
        self.py = pythia8.Pythia("", False)
        self.py.readFile(str(cp5_path))
        for line in tuple(base_lines) + tuple(extra_lines) + ("Random:setSeed = on", f"Random:seed = {init_seed}"):
            self.py.readString(line)
        if not self.py.init():
            raise RuntimeError('Pythia init failed')

    def generate(self, seed):
        """-> list of final-state particle tuples (pdg, q, m, px, py, pz, e, xProd, yProd, zProd, tProd[mm/c])
        and the Pythia event object (for truth MET etc.)."""
        self.py.rndm.init(int(seed) % 900_000_000)
        n_try = 0
        while not self.py.next():
            n_try += 1
            if n_try > 100:
                raise RuntimeError('Pythia failed 100 times')
        ev = self.py.event
        out = []
        for j in range(ev.size()):
            p = ev[j]
            if not p.isFinal():
                continue
            out.append((p.id(), p.charge(), p.m(), p.px(), p.py(), p.pz(), p.e(), p.xProd(), p.yProd(), p.zProd(),
                        p.tProd()))
        return out, ev


def select_and_place(parts, vp, vtx, vsec_start=1):
    """Apply the Fatras input selection and place an interaction's particles at the vertex vtx = (x, y, z, t[ns]).
    Returns (rows (n, 12) PCOLS, prompt momentum sum (3,), number of displaced vertices)."""
    if not parts:
        return np.zeros((0, len(PCOLS))), np.zeros(3), 0
    a = np.array(parts, float)
    pdg = a[:, 0]; q = a[:, 1]
    pt = np.hypot(a[:, 3], a[:, 4])
    pabs = np.sqrt(pt ** 2 + a[:, 5] ** 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        eta = np.arctanh(np.where(pabs > 0, a[:, 5] / np.maximum(pabs, 1e-300), 0.0))
    x = a[:, 7] + vtx[0]; y = a[:, 8] + vtx[1]; z = a[:, 9] + vtx[2]
    t = a[:, 10] / C_MM_PER_NS + vtx[3]
    keep = (((q != 0) | (pdg == 22)) & (pt > PT_MIN) & (np.abs(eta) < ETA_MAX) & (np.hypot(x, y) < RHO_MAX)
            & (np.abs(z) < Z_MAX))
    disp = (np.abs(a[:, 7]) + np.abs(a[:, 8]) + np.abs(a[:, 9])) > 0
    # displaced vertices: one id per distinct Pythia production point
    vsec = np.zeros(len(a), np.int64)
    nd = 0
    if disp.any():
        key = np.round(a[disp, 7:11], 9)
        _, inv = np.unique(key, axis=0, return_inverse=True)
        vsec[disp] = vsec_start + inv.ravel()
        nd = int(inv.max()) + 1
    rows = np.c_[np.full(len(a), vp), vsec, pdg, q, a[:, 2], x, y, z, t, a[:, 3], a[:, 4], a[:, 5]][keep]
    psum = a[keep & ~disp][:, 3:6].sum(0) if (keep & ~disp).any() else np.zeros(3)
    return rows, psum, nd


def mpi_init_lines(tt, tag='minbias'):
    """Pythia MPI-initialisation reuse (init 13.6 s -> 0.1 s; events identical to ~1e-11 relative, G1 check).  The file
    is created once (atomic rename) and then only read (reuseInit = 2)."""
    import os
    d = tt / 'data' / 'acts_stage4' / 'g1' / 'pythia_init'
    f = d / f'mpi_cp5_14tev_{tag}.dat'
    if not f.exists():
        d.mkdir(parents=True, exist_ok=True)
        tmp = d / f'.tmp_{os.getpid()}_{f.name}'
        return (f"MultipartonInteractions:reuseInit = 1", f"MultipartonInteractions:initFile = {tmp}"), (tmp, f)
    return (f"MultipartonInteractions:reuseInit = 2", f"MultipartonInteractions:initFile = {f}"), None


class MinBias:
    """Seeded PU-200 events: Poisson(mu) interactions, each at its own luminous-region vertex (plan §1.3/§1.4)."""

    def __init__(self, cp5_path, beamspot, mu=200.0, tt=None):
        lines, mv = mpi_init_lines(tt) if tt is not None else ((), None)
        self.gen = PythiaGen(cp5_path, extra_lines=lines)
        if mv is not None:
            import os
            os.replace(mv[0], mv[1])
        self.bs = beamspot
        self.mu = mu

    def event(self, ev_seed, n_int=None):
        rng = np.random.default_rng(hseed('pu-event', ev_seed, mod=2 ** 63))
        n = int(rng.poisson(self.mu)) if n_int is None else int(n_int)
        sig = np.array([self.bs['sigma_xy_um'] * 1e-3, self.bs['sigma_xy_um'] * 1e-3, self.bs['sigma_z_mm'],
                        self.bs['sigma_t_ps'] * 1e-3])
        vtx = rng.normal(0.0, 1.0, (n, 4)) * sig
        seeds = rng.integers(1, 900_000_000, n)
        rows = []; vz = []
        for k in range(n):
            parts, _ = self.gen.generate(seeds[k])
            r, psum, _ = select_and_place(parts, k + 1, vtx[k])
            rows.append(r)
            vz.append((k + 1, *vtx[k], *psum))
        P = np.concatenate(rows) if rows else np.zeros((0, len(PCOLS)))
        return P, np.array(vz, float).reshape(-1, 8), dict(n_int=n, n_particles=len(P))


def gun_event(ev_seed, pdg=13, mass=0.1056583755, pt_range=(1.0, 10.0), eta_range=(-2.5, 2.5), n=10, beamspot=None,
              vertex='lum', phi_mode='uniform', nphi=32, dphi_max=2e-3, random_sign=True):
    """Particle gun: n particles per event, each its own interaction id vp = GUN_VP + k (one particle per 'vertex').
    pT uniform in pt_range, eta uniform, phi uniform or (phi_mode='boundary') at a random phi-sector boundary
    -pi + j 2pi/nphi plus U(-dphi_max, dphi_max).  Vertex: luminous region ('lum') or the origin."""
    rng = np.random.default_rng(hseed('gun-event', ev_seed, mod=2 ** 63))
    pt = rng.uniform(pt_range[0], pt_range[1], n)
    eta = rng.uniform(eta_range[0], eta_range[1], n)
    if phi_mode == 'boundary':
        phi = -np.pi + rng.integers(0, nphi, n) * (2 * np.pi / nphi) + rng.uniform(-dphi_max, dphi_max, n)
    else:
        phi = rng.uniform(-np.pi, np.pi, n)
    sgn = rng.choice([-1, 1], n) if random_sign else np.ones(n)
    # pdg sign convention: +13 = mu-, charge -1 (PDG); a 'sign' flips particle <-> antiparticle
    pdgs = pdg * sgn
    q0 = {13: -1.0, 11: -1.0, 211: 1.0, 321: 1.0, 2212: 1.0}.get(abs(pdg), 0.0)
    q = q0 * sgn
    if vertex == 'lum':
        sig = np.array([beamspot['sigma_xy_um'] * 1e-3, beamspot['sigma_xy_um'] * 1e-3, beamspot['sigma_z_mm'],
                        beamspot['sigma_t_ps'] * 1e-3])
        v = rng.normal(0, 1, (n, 4)) * sig
    else:
        v = np.zeros((n, 4))
    px = pt * np.cos(phi); py = pt * np.sin(phi); pz = pt * np.sinh(eta)
    vp = GUN_VP + np.arange(n)
    P = np.c_[vp, np.zeros(n), pdgs, q, np.full(n, mass), v, px, py, pz]
    vz = np.c_[vp, v, px, py, pz]
    return P, vz, dict(n_particles=n)


# ------------------------------------------------------------------------------------------------ SM hard scatter (§4.2)
SM_SAMPLES = {
    # name: (process lines, pTHatMin) -- plan §4.2 / p6 probe; truth MET (sum of final-state neutrinos) > 200 GeV filter
    'Znunu_j': (["WeakBosonAndParton:qqbar2gmZg = on", "WeakBosonAndParton:qg2gmZq = on", "WeakZ0:gmZmode = 2",
                 "23:onMode = off", "23:onIfAny = 12 14 16"], 150.0),
    'Wenu_j': (["WeakBosonAndParton:qqbar2Wg = on", "WeakBosonAndParton:qg2Wq = on", "24:onMode = off",
                "24:onIfAny = 11"], 150.0),
    'Wmunu_j': (["WeakBosonAndParton:qqbar2Wg = on", "WeakBosonAndParton:qg2Wq = on", "24:onMode = off",
                 "24:onIfAny = 13"], 150.0),
    'Wtaunu_j': (["WeakBosonAndParton:qqbar2Wg = on", "WeakBosonAndParton:qg2Wq = on", "24:onMode = off",
                  "24:onIfAny = 15"], 150.0),
    'Wtauhnu_j': (["WeakBosonAndParton:qqbar2Wg = on", "WeakBosonAndParton:qg2Wq = on", "24:onMode = off",
                   "24:onIfAny = 15", "15:offIfAny = 11 13"], 150.0),          # tau forced hadronic (§4.2 subsample)
    'ttbar_1l': (["Top:gg2ttbar = on", "Top:qqbar2ttbar = on"], 150.0),      # exactly one W -> l nu (filter below)
}
MET_MIN = 200.0
PRE_MET = 150.0           # parton-level neutrino pre-filter before hadronisation (tau-decay neutrinos come later)


class HardScatter:
    """Pythia hard-scatter generator with the truth-MET filter (plan §4.2).  MPI and hadronisation on (the UE is part
    of the hit-level event).  generate(seed) -> (particles list as PythiaGen.generate, truth MET (2,), n_tries)."""

    def __init__(self, cp5_path, name, tt=None):
        lines, pt = SM_SAMPLES[name]
        base = ("Beams:eCM = 14000.", f"PhaseSpace:pTHatMin = {pt}", "ParticleDecays:limitTau0 = on",
                "ParticleDecays:tau0Max = 1000.", "211:mayDecay = off", "321:mayDecay = off", "13:mayDecay = off",
                "130:mayDecay = off", "Print:quiet = on", "Next:numberCount = 0", "PartonLevel:MPI = on",
                "HadronLevel:all = off")
        mpi, mv = mpi_init_lines(tt, tag=f'hs_{name}') if tt is not None else ((), None)
        self.gen = PythiaGen(cp5_path, extra_lines=tuple(lines) + tuple(mpi), base_lines=base)
        if mv is not None:
            import os
            os.replace(mv[0], mv[1])
        self.name = name

    def _met(self, ev):
        mx = my = 0.0
        for k in range(ev.size()):
            p = ev[k]
            if p.isFinal() and abs(p.id()) in (12, 14, 16):
                mx += p.px(); my += p.py()
        return mx, my

    def _nlep_w(self, ev):
        n = 0
        # count W bosons (bottom copies) decaying to a charged lepton
        seen = set()
        for k in range(ev.size()):
            p = ev[k]
            if abs(p.id()) != 24:
                continue
            b = p.iBotCopy()
            if b in seen:
                continue
            seen.add(b)
            w = ev[b]
            ds = [ev[j] for j in range(w.daughter1(), w.daughter2() + 1)] if w.daughter1() > 0 else []
            if any(abs(x.id()) in (11, 13, 15) for x in ds):
                n += 1
        return n

    def generate(self, seed, max_tries=200000):
        py = self.gen.py
        py.rndm.init(int(seed) % 900_000_000)
        for n_try in range(1, max_tries + 1):
            if not py.next():
                continue
            ev = py.event
            if self.name == 'ttbar_1l' and self._nlep_w(ev) != 1:
                continue
            mx, my = self._met(ev)
            if math.hypot(mx, my) < PRE_MET:
                continue
            if not py.forceHadronLevel():
                continue
            ev = py.event
            mx, my = self._met(ev)
            if math.hypot(mx, my) < MET_MIN:
                continue
            out = []
            for j in range(ev.size()):
                p = ev[j]
                if p.isFinal():
                    out.append((p.id(), p.charge(), p.m(), p.px(), p.py(), p.pz(), p.e(), p.xProd(), p.yProd(),
                                p.zProd(), p.tProd()))
            return out, np.array([mx, my]), n_try, py.infoPython().sigmaGen()
        raise RuntimeError('MET filter: no event accepted')


class SMEvent:
    """SM hard scatter (vp = HS_VP) + PU-200 (plan §4.2: 'each with PU 200')."""

    def __init__(self, cp5_path, beamspot, name, mu=200.0, tt=None):
        self.hs = HardScatter(cp5_path, name, tt=tt)
        self.mb = MinBias(cp5_path, beamspot, mu=mu, tt=tt) if mu > 0 else None
        self.bs = beamspot

    def event(self, ev_seed):
        rng = np.random.default_rng(hseed('hs-vertex', ev_seed, mod=2 ** 63))
        sig = np.array([self.bs['sigma_xy_um'] * 1e-3, self.bs['sigma_xy_um'] * 1e-3, self.bs['sigma_z_mm'],
                        self.bs['sigma_t_ps'] * 1e-3])
        vtx = rng.normal(0, 1, 4) * sig
        parts, met, ntry, sgen = self.hs.generate(hseed('hs', ev_seed))
        rows, psum, _ = select_and_place(parts, HS_VP, vtx)
        vzh = np.array([[HS_VP, *vtx, *psum]])
        if self.mb is not None:
            P, vz, info = self.mb.event(hseed('hs-pu', ev_seed, mod=2 ** 62))
            P = np.concatenate([rows, P]); vz = np.concatenate([vzh, vz])
        else:
            P, vz, info = rows, vzh, dict(n_int=0)
        info.update(hs_met=met.tolist(), hs_tries=ntry, hs_sigma_gen_mb=sgen, hs_vtx=vtx.tolist(), n_hs=len(rows))
        return P, vz, info
