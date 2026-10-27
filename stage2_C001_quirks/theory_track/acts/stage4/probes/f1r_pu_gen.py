"""f1r_pu_gen.py -- Stage-4 plan FIXER R1 probe (acts env): fresh PU-200 events with per-measurement TRUTH, no signal.

Same chain as p2_inject_digi.py (copied, not imported: p2 runs at import): Pythia8 CP5 minimum bias (fresh pool, no reuse:
pool size = 200 x NEV), HepMC3 reader with the luminous-region vertex smearing, particle selection pT > 50 MeV |eta| < 4
(charged + photons), Fatras (pMin 30 MeV, conversions on), smearing digitisation with doMerge = False, whole-cylinder
surfaces (nphi = 1; no CKF in this probe).  Output per measurement:
  sid, x, y, z (global, smeared), s0, s1 (local sigmas as in p2), flag (0 = PU), vertexPrimary, particle, generation,
  vertexSecondary, dE [GeV]
plus per event, per ACTS primary vertex: (vp, x, y, z, sum px, sum py, sum pz) of its generation-0 particles (Pythia
displaced decay vertices are separate ACTS primary vertices; they are attached to their interaction at analysis level).
Run (theory_track/acts):  nice pixi run python stage4/probes/f1r_pu_gen.py <worker_id> <n_events>
Output: data/acts_stage4/fix_r1/pu/pu_w<id>.npz
"""
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import acts
import acts.examples
import acts.examples.hepmc3
import acts.examples.json
import acts.fatras
from acts import UnitConstants as u
from acts.examples.simulation import addFatras, addGenParticleSelection, ParticleSelectorConfig

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s4geo  # noqa: E402
import s4pu  # noqa: E402

TT = s4geo.TT
WID = int(sys.argv[1])
NEV = int(sys.argv[2])
OUT = TT / 'data' / 'acts_stage4' / 'fix_r1' / 'pu'
OUT.mkdir(parents=True, exist_ok=True)
GEO = json.loads((TT / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())
bs = GEO['beamspot']
RES = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (16.0, 0.9)}   # production BTL axes
SIG_T_BTL = 0.035

tg, els, sid_of, geo_of, surfs, passive = s4geo.build()
gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8112 * u.T))
tab = {s['sid']: s for s in surfs}
surf_by_geo = {e.surface().geometryId: e.surface() for e in els}


def digi_json():
    entries = []
    for g, sid in sid_of.items():
        s = tab[sid]; k = s['kind']
        srp, slong = RES[k]
        if s['type'] == 0:
            sm = [dict(index=0, mean=0.0, stddev=srp, type='Gauss'), dict(index=1, mean=0.0, stddev=slong, type='Gauss')]
        else:
            rmid = 0.5 * (s['p1'] + s['p2']) * 10
            sm = [dict(index=0, mean=0.0, stddev=slong, type='Gauss'), dict(index=1, mean=0.0, stddev=srp / rmid, type='Gauss')]
        if k == 'BTL':
            sm.append(dict(index=5, mean=0.0, stddev=SIG_T_BTL, type='Gauss'))
        entries.append(dict(volume=g.volume, sensitive=g.sensitive, value=dict(smearing=sm)))
    j = {"acts-geometry-hierarchy-map": {"format-version": 0, "value-identifier": "digitization-configuration"}, "entries": entries}
    p = OUT / f'digi_w{WID}.json'
    p.write_text(json.dumps(j, indent=0))
    return p


DIGI = digi_json()


class Dump(acts.examples.IAlgorithm):
    def __init__(self, store):
        acts.examples.IAlgorithm.__init__(self, 'DumpMeasTruth', acts.logging.WARNING)
        self.m = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'm'); self.m.initialize('measurements')
        self.h = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'h'); self.h.initialize('simhits')
        self.ms = acts.examples.ReadDataHandle(self, acts.examples.MeasurementSimHitsMap, 'ms'); self.ms.initialize('msh')
        self.p = acts.examples.ReadDataHandle(self, acts.examples.SimParticleContainer, 'p'); self.p.initialize('particles_generated')
        self.store = store

    def execute(self, ctx):
        hits = list(self.h(ctx.eventStore)); meas = self.m(ctx.eventStore)
        tr = {}
        for mi, hi in self.ms(ctx.eventStore):
            hh = hits[hi]; b = hh.particleId
            tr[mi] = (int(b.vertexPrimary), int(b.particle), int(b.generation), int(b.vertexSecondary), float(hh.depositedEnergy))
        rows = []
        for mi, mm in enumerate(meas):
            g = mm.geometryId; srf = surf_by_geo[g]
            fp = mm.fullParameters; fp = fp() if callable(fp) else fp; par = np.array(fp, float).ravel()
            si = mm.subspaceIndices; si = si() if callable(si) else si; idx = [int(x) for x in si]
            l0 = par[0] if 0 in idx else 0.0
            l1 = par[1] if 1 in idx else 0.0
            gp = srf.localToGlobal(gctx, acts.Vector2(float(l0), float(l1)), acts.Vector3(1, 0, 0))
            fc = mm.fullCovariance; fc = fc() if callable(fc) else fc
            t = tr.get(mi, (-1, -1, -1, -1, 0.0))
            rows.append((sid_of[g], gp[0], gp[1], gp[2], math.sqrt(float(fc[0, 0])), math.sqrt(float(fc[1, 1])), 0.0) + t)
        vz = {}   # vertexPrimary -> [x, y, z, sum px, sum py, sum pz] of its generation-0 outgoing particles
        for p in self.p(ctx.eventStore):
            b = p.particleId
            if int(b.generation) == 0 and int(b.vertexSecondary) == 0:
                k = int(b.vertexPrimary); fp = p.fourPosition; mom = p.momentum
                if k not in vz:
                    vz[k] = [float(fp[0]), float(fp[1]), float(fp[2]), 0.0, 0.0, 0.0]
                pt = float(p.transverseMomentum); ph = float(p.phi); th = float(p.theta)
                pabs = pt / max(math.sin(th), 1e-12)
                vz[k][3] += pt * math.cos(ph); vz[k][4] += pt * math.sin(ph); vz[k][5] += pabs * math.cos(th)
        self.store.append(dict(meas=np.array(rows, float).reshape(-1, 12),
                               vz=np.array([[k] + v for k, v in sorted(vz.items())], float).reshape(-1, 7)))
        return acts.examples.ProcessCode.SUCCESS


hepmc_path = OUT / f'pool_w{WID}.hepmc3'
seed = 20261100 + WID
t0 = time.time()
s4pu.make_pool(hepmc_path, 200 * NEV, seed, TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat')
t_pool = time.time() - t0
store = []
rnd = acts.examples.RandomNumbers(seed=900 + WID)
s = acts.examples.Sequencer(events=NEV, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
R = acts.examples.hepmc3.HepMC3Reader
vg = acts.examples.GaussianVertexGenerator(
    stddev=acts.Vector4(bs['sigma_xy_um'] * u.um, bs['sigma_xy_um'] * u.um, bs['sigma_z_mm'] * u.mm, bs['sigma_t_ps'] * u.ns / 1000.0),
    mean=acts.Vector4(0, 0, 0, 0))
s.addReader(R(inputs=[R.Input.Fixed(hepmc_path, 200)], level=acts.logging.WARNING, outputEvent='hepmc3_event',
              checkEventNumber=False, numEvents=NEV, randomNumbers=rnd, vertexGenerator=vg))
s.addAlgorithm(acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent='hepmc3_event',
                                                         outputParticles='particles_generated', outputVertices='vertices_generated',
                                                         mergePrimaries=False))
s.addWhiteboardAlias('particles', 'particles_generated')
addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 1100 * u.mm), absZ=(0.0, 2.7 * u.m), eta=(-4.0, 4.0),
                                                  pt=(50 * u.MeV, None), removeNeutral=False))
addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
cfg = acts.examples.DigitizationAlgorithm.Config(
    digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(DIGI)), surfaceByIdentifier=surf_by_geo,
    randomNumbers=rnd, inputSimHits='simhits', outputMeasurements='measurements', doMerge=False,
    outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh', outputParticleMeasurementsMap='pm',
    outputSimHitMeasurementsMap='shm')
s.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING))
s.addAlgorithm(Dump(store))
t1 = time.time(); s.run(); wall = time.time() - t1
np.savez_compressed(OUT / f'pu_w{WID}.npz', **{f'ev{i}': r['meas'] for i, r in enumerate(store)},
                    **{f'vz{i}': r['vz'] for i, r in enumerate(store)},
                    columns=np.array(['sid', 'x', 'y', 'z', 's0', 's1', 'flag', 'vp', 'particle', 'gen', 'vsec', 'dE']))
(OUT / f'pu_w{WID}.json').write_text(json.dumps(dict(worker=WID, n_events=NEV, pool_seed=seed, rnd_seed=900 + WID,
                                                     t_pool_s=round(t_pool, 1), t_chain_s=round(wall, 1),
                                                     n_meas=[int(len(r['meas'])) for r in store]), indent=1))
hepmc_path.unlink()
print('worker', WID, 'done', NEV, 'events, pool', round(t_pool), 's, chain', round(wall), 's')
