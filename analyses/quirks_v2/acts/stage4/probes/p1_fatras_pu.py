"""p1_fatras_pu.py -- Stage-4 PROBE (E9, plan turn).  Fatras on the s4geo geometry (Stage-3 simplified surfaces).
  A. muon gun (pT 1-10 GeV, |eta| < 2.5, 3.8 T): hits per muon, hits lie on the named surfaces (|r - R| or |z - z_d| < 1 um).
  B. PU-200: Pythia8 CP5 minimum bias (14 TeV SoftQCD:inelastic; K0S/Lambda/hyperons decayed by Pythia (tau0Max 1000 mm)
     but pi+-/K+- kept stable; Fatras does no decays) -> HepMC3 -> HepMC3Reader (200 per event, Gaussian luminous region
     from geometry/cms_phase2_public.json) -> particle selection -> Fatras (photon conversion on) -> hits per surface.
     Two selections: 'ch150' (charged, pT > 150 MeV: the smoke-test setting) and 'all50' (charged + photons, pT > 50 MeV).
     Times: Pythia generation and Python HepMC3 conversion per interaction; Fatras per PU-200 event (1 thread).
Run (theory_track/acts):  nice pixi run python stage4/probes/p1_fatras_pu.py [n_mb=1200] [n_pu_events=5]
Outputs: data/acts_stage4/p1/{p1_summary.json, hits_<sel>.npz} (hits: surface id, x, y, z, t, particle barcode, event).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import acts
import acts.examples
import acts.examples.hepmc3
import acts.fatras
from acts import UnitConstants as u
from acts.examples.simulation import (addParticleGun, MomentumConfig, EtaConfig, PhiConfig, ParticleConfig, addFatras,
                                      addGenParticleSelection, ParticleSelectorConfig)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s4geo  # noqa: E402

TT = s4geo.TT
OUT = TT / 'data' / 'acts_stage4' / 'p1'
OUT.mkdir(parents=True, exist_ok=True)
N_MB = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
N_PU_EV = int(sys.argv[2]) if len(sys.argv) > 2 else 5
CP5 = TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
GEO = json.loads((TT / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())
bs = GEO['beamspot']

tg, els, sid_of, geo_of, surfs, passive = s4geo.build()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8112 * u.T))     # B0 of the Stage-3 kernel (3.8112 T)
summary = dict(n_mb=N_MB, n_pu_events=N_PU_EV)


class HitDump(acts.examples.IAlgorithm):
    def __init__(self, key, store):
        acts.examples.IAlgorithm.__init__(self, 'HitDump_' + key, acts.logging.WARNING)
        self.h = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'h'); self.h.initialize(key)
        self.store = store

    def execute(self, ctx):
        rows = []
        for h in self.h(ctx.eventStore):
            p = h.fourPosition
            sid = sid_of.get(h.geometryId, -1)
            bc = h.particleId
            rows.append((sid, p[0], p[1], p[2], p[3], bc.vertexPrimary, bc.particle, bc.generation))
        self.store.append(np.array(rows, float).reshape(-1, 8))
        return acts.examples.ProcessCode.SUCCESS


def surface_residual(a):
    """|r - R| for cylinders, |z - z_d| for discs [mm]."""
    sid = a[:, 0].astype(int)
    out = np.full(len(a), np.nan)
    tab = {s['sid']: s for s in surfs}
    for k in np.unique(sid):
        if k < 0:
            continue
        s = tab[k]; m = sid == k
        if s['type'] == 0:
            out[m] = np.abs(np.hypot(a[m, 1], a[m, 2]) - s['p0'] * 10)
        else:
            out[m] = np.abs(a[m, 3] - s['p0'] * 10)
    return out


# ---------------------------------------------------------------- A. muon gun
t0 = time.time()
storeA = []
rnd = acts.examples.RandomNumbers(seed=101)
s = acts.examples.Sequencer(events=200, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
addParticleGun(s, MomentumConfig(1.0 * u.GeV, 10.0 * u.GeV, transverse=True), EtaConfig(-2.5, 2.5, uniform=True),
               PhiConfig(0.0, 360.0 * u.degree), ParticleConfig(1, acts.PdgParticle.eMuon, randomizeCharge=True), rnd=rnd)
addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
s.addAlgorithm(HitDump('simhits', storeA))
s.run()
a = np.vstack(storeA)
res = surface_residual(a)
nh = [len(x) for x in storeA]
kinds = np.array([surfs[int(k)]['kind'] if k >= 0 else 'none' for k in a[:, 0]])
summary['A_gun'] = dict(events=len(storeA), hits_per_muon_mean=float(np.mean(nh)), hits_per_muon_min=int(np.min(nh)),
                        hits_per_muon_max=int(np.max(nh)), unmapped=int(np.sum(a[:, 0] < 0)),
                        max_surface_residual_mm=float(np.nanmax(res)),
                        hits_by_kind={k: int(np.sum(kinds == k)) for k in np.unique(kinds)}, wall_s=round(time.time() - t0, 1))
print('A', json.dumps(summary['A_gun']))

# ---------------------------------------------------------------- B. PU-200
import pythia8, pyhepmc  # noqa: E402
hepmc_path = OUT / 'minbias_pool.hepmc3'
py = pythia8.Pythia("", False)
py.readFile(str(CP5))
for line in ("Beams:eCM = 14000.", "SoftQCD:inelastic = on", "ParticleDecays:limitTau0 = on", "ParticleDecays:tau0Max = 1000.",
             "211:mayDecay = off", "321:mayDecay = off", "13:mayDecay = off", "130:mayDecay = off",
             "Print:quiet = on", "Random:setSeed = on", "Random:seed = 20261013", "Next:numberCount = 0"):
    py.readString(line)
t0 = time.time(); assert py.init(); t_init = time.time() - t0


def to_hepmc(ev, iev):
    ge = pyhepmc.GenEvent(pyhepmc.Units.GEV, pyhepmc.Units.MM)
    ge.event_number = iev
    parts = [None] * ev.size()
    for i in range(1, ev.size()):
        p = ev[i]
        gp = pyhepmc.GenParticle(pyhepmc.FourVector(p.px(), p.py(), p.pz(), p.e()), p.id(), 1 if p.isFinal() else (4 if i <= 2 else 2))
        gp.generated_mass = p.m(); parts[i] = gp; ge.add_particle(gp)
    endv = {}
    for i in range(3, ev.size()):
        p = ev[i]
        moms = tuple(sorted(set(m for m in p.motherList() if m > 0))) or (1, 2)
        v = endv.get(moms)
        if v is None:
            v = pyhepmc.GenVertex(pyhepmc.FourVector(p.xProd(), p.yProd(), p.zProd(), p.tProd()))
            for m in moms:
                if parts[m].end_vertex is None:
                    v.add_particle_in(parts[m])
            ge.add_vertex(v); endv[moms] = v
        v.add_particle_out(parts[i])
    return ge


t_py = t_conv = 0.0; n_ok = 0
with pyhepmc.io.WriterAscii(str(hepmc_path)) as w:
    while n_ok < N_MB:
        t1 = time.time()
        if not py.next():
            continue
        t2 = time.time()
        w.write(to_hepmc(py.event, n_ok)); n_ok += 1
        t_py += t2 - t1; t_conv += time.time() - t2
summary['B_pythia'] = dict(init_s=round(t_init, 1), ms_per_interaction_pythia=1e3 * t_py / N_MB,
                           ms_per_interaction_hepmc_conversion=1e3 * t_conv / N_MB,
                           file_MB=round(hepmc_path.stat().st_size / 1e6, 1), sigma_inel_mb=py.infoPython().sigmaGen())
print('B pythia', json.dumps(summary['B_pythia']))

for sel, ptmin, neutral in (('ch150', 150 * u.MeV, True), ('all50', 50 * u.MeV, False)):
    store = []; tA = {}
    rnd = acts.examples.RandomNumbers(seed=43)
    s = acts.examples.Sequencer(events=N_PU_EV, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
    R = acts.examples.hepmc3.HepMC3Reader
    vg = acts.examples.GaussianVertexGenerator(
        stddev=acts.Vector4(bs['sigma_xy_um'] * u.um, bs['sigma_xy_um'] * u.um, bs['sigma_z_mm'] * u.mm, bs['sigma_t_ps'] * u.ns / 1000.0),
        mean=acts.Vector4(0, 0, 0, 0))
    s.addReader(R(inputs=[R.Input.Fixed(hepmc_path, 200)], level=acts.logging.WARNING, outputEvent='hepmc3_event',
                  checkEventNumber=False, numEvents=N_PU_EV, randomNumbers=rnd, vertexGenerator=vg))
    s.addAlgorithm(acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent='hepmc3_event',
                                                             outputParticles='particles_generated', outputVertices='vertices_generated',
                                                             mergePrimaries=False))
    s.addWhiteboardAlias('particles', 'particles_generated')
    addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 1100 * u.mm), absZ=(0.0, 2.7 * u.m), eta=(-4.0, 4.0),
                                                      pt=(ptmin, None), removeNeutral=neutral))
    addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
    s.addAlgorithm(HitDump('simhits', store))
    t0 = time.time(); s.run(); wall = time.time() - t0
    a = np.vstack([np.c_[x, np.full(len(x), i)] for i, x in enumerate(store)])
    np.savez_compressed(OUT / f'hits_{sel}.npz', hits=a.astype(np.float32))
    res = surface_residual(a)
    per = {}
    for sdef in surfs:
        if sdef['kind'] == 'T3V':
            continue
        m = a[:, 0] == sdef['sid']
        if sdef['type'] == 0:
            area = 2 * np.pi * sdef['p0'] * (sdef['p2'] - sdef['p1'])
        else:
            area = np.pi * (sdef['p2'] ** 2 - sdef['p1'] ** 2)
        per[sdef['name']] = dict(hits_per_event=float(m.sum() / N_PU_EV), per_cm2=float(m.sum() / N_PU_EV / area))
    summary['B_' + sel] = dict(wall_s_total=round(wall, 1), s_per_event=round(wall / N_PU_EV, 2),
                               hits_per_event=float(len(a) / N_PU_EV), unmapped=int(np.sum(a[:, 0] < 0)),
                               max_surface_residual_mm=float(np.nanmax(res)), per_surface=per)
    print('B', sel, 's/event', round(wall / N_PU_EV, 2), 'hits/event', len(a) / N_PU_EV,
          {k: round(per[k]['per_cm2'], 2) for k in ('TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1_in', 'TB2S_L1_in', 'TB2S_L3_out', 'TFPX_D1_p', 'TEPX_D1_p')})
(OUT / 'p1_summary.json').write_text(json.dumps(summary, indent=1))
hepmc_path.unlink()
