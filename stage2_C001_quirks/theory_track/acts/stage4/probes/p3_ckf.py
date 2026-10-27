"""p3_ckf.py -- Stage-4 PROBE (E9, plan turn): standard seeding + CKF on the s4geo geometry with PU 200 + injected quirk hits.
Purpose: CPU per event of the CKF used ONLY to remove hits of reconstructed helical tracks before the quirk finder (plan §2),
and a first look at how many quirk measurements end up on CKF tracks.
Seeding: GridTriplet on spacepoints of the 4 TBPX layers + TFPX discs (2D pixel measurements), minPt 0.9 GeV, |z0| < 200 mm,
impactMax 3 mm; CKF over all sensitive surfaces; track selection pT > 0.9 GeV, >= 7 measurements, <= 2 holes.
Run (theory_track/acts): nice pixi run python stage4/probes/p3_ckf.py <stage3 npz> [n_events=3]
Needs data/acts_stage4/p2/digi_smearing_s4.json (written by p2_inject_digi.py).
Output: data/acts_stage4/p3/p3_summary.json
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
from acts.examples.reconstruction import (addSeeding, SeedFinderConfigArg, SeedFinderOptionsArg, SeedingAlgorithm,
                                          addCKFTracks, TrackSelectorConfig, CkfConfig)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s4geo  # noqa: E402
import s4pu  # noqa: E402

TT = s4geo.TT
OUT = TT / 'data' / 'acts_stage4' / 'p3'
OUT.mkdir(parents=True, exist_ok=True)
F = sys.argv[1]
NEV = int(sys.argv[2]) if len(sys.argv) > 2 else 3
NPHI = int(sys.argv[3]) if len(sys.argv) > 3 else 1
bs = json.loads((TT / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())['beamspot']
B0 = 3.8112 * u.T

tg, els, sid_of, geo_of, surfs, passive = s4geo.build(nphi=NPHI)
DIGI = s4geo.write_digi(sid_of, surfs, OUT / f'digi_n{NPHI}.json')
field = acts.ConstantBField(acts.Vector3(0, 0, B0))
tab = {s['sid']: s for s in surfs}
surf_by_geo = {e.surface().geometryId: e.surface() for e in els}
seed_sids = [s['sid'] for s in surfs if s['name'].startswith('TBPX') or s['name'].startswith('TFPX')]
sel = [dict(volume=v) for v in sorted({geo_of[(k, 0)].volume for k in seed_sids})]
(OUT / 'geoSelection_IT.json').write_text(json.dumps(sel))

z = np.load(F)
kinds = [str(k) for k in z['surf_kinds']]
off = z['hit_offsets']; m_q = float(z['m'])
ev_simhits = []
for e in range(NEV):
    rows = []
    for j in range(off[e], off[e + 1]):
        sid = int(z['h_surf'][j])
        if kinds[sid] in ('T3V', 'ETL'):
            continue
        E = float(z['h_E'][j]); px, py_, pz = float(z['h_px'][j]), float(z['h_py'][j]), float(z['h_pz'][j])
        p = math.sqrt(px * px + py_ * py_ + pz * pz); Ea = E - float(z['h_dE'][j]); f = math.sqrt(max(Ea * Ea - m_q * m_q, 0)) / p
        rows.append((sid, int(z['h_quirk'][j]), (z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm, z['h_t'][j] * u.ns),
                     (px * u.GeV, py_ * u.GeV, pz * u.GeV, E * u.GeV), (px * f * u.GeV, py_ * f * u.GeV, pz * f * u.GeV, Ea * u.GeV), j - off[e]))
    ev_simhits.append(rows)


class Inject(acts.examples.IAlgorithm):
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, 'Inject', acts.logging.WARNING)
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_all')

    def execute(self, ctx):
        c = acts.examples.SimHitContainer()
        for h in self.inp(ctx.eventStore):
            c.insert(h)
        for sid, q, x4, p4b, p4a, k in ev_simhits[ctx.eventNumber]:
            bc = acts.fatras.Barcode(); bc.vertexPrimary = 4000; bc.particle = 1 + q
            c.insert(acts.examples.SimHit(geo_of[(sid, 0 if tab[sid]['kind'] == 'BTL' else s4geo.sector(x4[0], x4[1], NPHI))], bc, acts.Vector4(*x4), acts.Vector4(*p4b), acts.Vector4(*p4a), k))
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


class Timer(acts.examples.IAlgorithm):
    def __init__(self, name, store):
        acts.examples.IAlgorithm.__init__(self, name, acts.logging.WARNING); self.store = store; self.nm = name

    def execute(self, ctx):
        self.store.append((ctx.eventNumber, self.nm, time.time()))
        return acts.examples.ProcessCode.SUCCESS


class Count(acts.examples.IAlgorithm):
    def __init__(self, store):
        acts.examples.IAlgorithm.__init__(self, 'Count', acts.logging.WARNING)
        self.t = acts.examples.ReadDataHandle(self, acts.examples.ConstTrackContainer, 't'); self.t.initialize('tracks')
        self.m = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'm'); self.m.initialize('measurements')
        self.ms = acts.examples.ReadDataHandle(self, acts.examples.MeasurementSimHitsMap, 'ms'); self.ms.initialize('measurement_simhits_map')
        self.h = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'hh'); self.h.initialize('simhits_all')
        self.store = store

    def execute(self, ctx):
        tr = self.t(ctx.eventStore); nm = len(self.m(ctx.eventStore))
        row = dict(n_tracks=len(tr), n_meas=nm)
        try:
            used = set(); nt_good = 0
            for i in range(len(tr)):
                t = tr.getTrack(i)
                sts = t.trackStatesReversed
                sts = sts() if callable(sts) else sts
                for ts in sts:
                    h = ts.hasUncalibratedSourceLink
                    h = h() if callable(h) else h
                    if h:
                        sl = ts.uncalibratedSourceLink
                        sl = sl() if callable(sl) else sl
                        used.add(acts.examples.IndexSourceLink.fromSourceLink(sl).index)
            row['n_meas_on_tracks'] = len(used)
            # which measurements are quirk measurements: measurement -> simhit -> particle barcode (vertexPrimary 4000)
            ms = self.ms(ctx.eventStore); hits = list(self.h(ctx.eventStore))
            sig_meas = set()
            try:
                for mi, hi in ms:
                    if hits[hi].particleId.vertexPrimary == 4000:
                        sig_meas.add(mi)
            except Exception as ex2:
                row['ms_api'] = f'{type(ex2).__name__}: {str(ex2)[:150]} | {type(ms)} {[x for x in dir(ms) if not x.startswith("_")][:20]}'
            row['n_signal_meas'] = len(sig_meas); row['n_signal_meas_on_tracks'] = len(sig_meas & used)
        except Exception as ex:   # API probe; report and continue
            row['track_state_api'] = f'{type(ex).__name__}: {str(ex)[:160]}'
        self.store.append(row)
        return acts.examples.ProcessCode.SUCCESS


hepmc = OUT / 'pool_p3.hepmc3'
t_pool = s4pu.make_pool(hepmc, 200 * NEV, 20261015, TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat')
rnd = acts.examples.RandomNumbers(seed=91)
s = acts.examples.Sequencer(events=NEV, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
R = acts.examples.hepmc3.HepMC3Reader
vg = acts.examples.GaussianVertexGenerator(
    stddev=acts.Vector4(bs['sigma_xy_um'] * u.um, bs['sigma_xy_um'] * u.um, bs['sigma_z_mm'] * u.mm, bs['sigma_t_ps'] * u.ns / 1000.0),
    mean=acts.Vector4(0, 0, 0, 0))
s.addReader(R(inputs=[R.Input.Fixed(hepmc, 200)], level=acts.logging.WARNING, outputEvent='hepmc3_event', checkEventNumber=False,
              numEvents=NEV, randomNumbers=rnd, vertexGenerator=vg))
s.addAlgorithm(acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent='hepmc3_event',
                                                         outputParticles='particles_generated', outputVertices='vertices_generated',
                                                         mergePrimaries=False))
s.addWhiteboardAlias('particles', 'particles_generated')
addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 1100 * u.mm), absZ=(0.0, 2.7 * u.m), eta=(-4.0, 4.0),
                                                  pt=(50 * u.MeV, None), removeNeutral=False))
T = []
s.addAlgorithm(Timer('t0', T))
addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
s.addAlgorithm(Inject())
cfg = acts.examples.DigitizationAlgorithm.Config(
    digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(DIGI)), surfaceByIdentifier=surf_by_geo,
    randomNumbers=rnd, inputSimHits='simhits_all', outputMeasurements='measurements', doMerge=False,
    outputMeasurementParticlesMap='measurement_particles_map', outputMeasurementSimHitsMap='measurement_simhits_map',
    outputParticleMeasurementsMap='particle_measurements_map', outputSimHitMeasurementsMap='simhit_measurements_map')
s.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING))
s.addAlgorithm(Timer('t1_digi_done', T))
addSeeding(s, tg, field,
           SeedFinderConfigArg(r=(None, 200 * u.mm), deltaR=(1 * u.mm, 120 * u.mm), collisionRegion=(-200 * u.mm, 200 * u.mm),
                               z=(-1500 * u.mm, 1500 * u.mm), maxSeedsPerSpM=1, sigmaScattering=5, radLengthPerSeed=0.1,
                               minPt=900 * u.MeV, impactMax=3 * u.mm),
           SeedFinderOptionsArg(bFieldInZ=B0, beamPos=(0.0, 0.0)),
           seedingAlgorithm=SeedingAlgorithm.GridTriplet,
           initialSigmas=[1 * u.mm, 1 * u.mm, 1 * u.degree, 1 * u.degree, 0 * u.e / u.GeV, 1 * u.ns],
           initialSigmaQoverPt=0.1 * u.e / u.GeV, initialSigmaPtRel=0.1, initialVarInflation=[1.0] * 6,
           geoSelectionConfigFile=OUT / 'geoSelection_IT.json', logLevel=acts.logging.WARNING)
s.addAlgorithm(Timer('t2_seed_done', T))
addCKFTracks(s, tg, field, TrackSelectorConfig(pt=(900 * u.MeV, None), absEta=(None, 4.0), loc0=(-4.0 * u.mm, 4.0 * u.mm),
                                                nMeasurementsMin=7, maxHoles=2, maxOutliers=2),
             CkfConfig(chi2CutOffMeasurement=15.0, chi2CutOffOutlier=25.0, numMeasurementsCutOff=10, seedDeduplication=True,
                       stayOnSeed=True), logLevel=acts.logging.WARNING)
s.addAlgorithm(Timer('t3_ckf_done', T))
C = []
s.addAlgorithm(Count(C))
t0 = time.time(); s.run(); wall = time.time() - t0
dt = {}
for e in range(NEV):
    tt = {nm: t for ev, nm, t in T if ev == e}
    dt[e] = dict(fatras_inject_digi=tt['t1_digi_done'] - tt['t0'], seeding=tt['t2_seed_done'] - tt['t1_digi_done'],
                 ckf=tt['t3_ckf_done'] - tt['t2_seed_done'])
res = dict(file=F, n_events=NEV, nphi=NPHI, pool_s=round(t_pool, 1), wall_s=round(wall, 1), per_event_times_s=dt, counts=C)
(OUT / f'p3_summary_n{NPHI}.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, default=str)[:1500])
hepmc.unlink()
