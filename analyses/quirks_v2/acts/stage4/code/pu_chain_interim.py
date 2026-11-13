"""pu_chain_interim.py -- INTERIM PU-only chain for the Stage-4 runner (acts env), Phase A.

!! INTERIM: this is the fix-R1 probe chain (acts/stage4/probes/f1r_pu_gen.py) made seedable and Poisson.  It is NOT the
!! production chain of plan §1.8 / gate G1 (run_chain.py: direct SimParticle reader, CKF removal, signal injection,
!! SM hard scatter, guns/toys, V4-1 records).  run_stage4.py refuses production manifests while this chain is the one
!! in use (CHAIN = 'interim'); it is used for the runner smoke test and for development only.

Chain: Pythia8 CP5 14 TeV minimum bias pool (probes/s4pu.py) -> HepMC3 reader, Poisson(mu) interactions per event,
luminous-region vertex smearing -> particle selection (pT > 50 MeV, |eta| < 4, charged + photons) -> Fatras (pMin 30 MeV,
conversions on) -> smearing digitisation (doMerge = False; production BTL axes) -> per-measurement dump.
Missing w.r.t. production (plan): CKF removal (§1.6), the SimParticle reader (§1.4; HepMC3 costs ~4.6 s/event),
V4-1 per-job records, exact interaction ids for Pythia displaced-decay vertices (mapped by their smeared z as in f1r).

Output npz: ev<i> (n, 13) float64 columns COLS, vz<i> (per ACTS primary vertex: vp, x, y, z, sum px, py, pz),
meta (json).
Run (theory_track/acts):  pixi run python stage4/code/pu_chain_interim.py <out.npz> <n_events> <seed> [mu=200]
"""
import json
import math
import sys
import tempfile
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'probes'))
import s4geo  # noqa: E402
import s4pu  # noqa: E402

COLS = ['sid', 'x', 'y', 'z', 's0', 's1', 'flag', 'vp', 'particle', 'gen', 'vsec', 'dE', 't']
CHAIN = 'interim-f1r-hepmc3-noCKF'
TT = s4geo.TT
RES = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (16.0, 0.9)}
SIG_T_BTL = 0.035


def main(out, nev, seed, mu=200.0):
    t_start = time.time()
    out = Path(out)
    GEO = json.loads((TT / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())
    bs = GEO['beamspot']
    tg, els, sid_of, geo_of, surfs, passive = s4geo.build()
    gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
    field = acts.ConstantBField(acts.Vector3(0, 0, 3.8112 * u.T))
    tab = {s['sid']: s for s in surfs}
    surf_by_geo = {e.surface().geometryId: e.surface() for e in els}
    tmpd = Path(tempfile.mkdtemp(prefix='puchain_', dir=str(out.parent)))
    entries = []
    for g, sid in sid_of.items():
        s = tab[sid]; k = s['kind']
        srp, slong = RES[k]
        if s['type'] == 0:
            sm = [dict(index=0, mean=0.0, stddev=srp, type='Gauss'), dict(index=1, mean=0.0, stddev=slong, type='Gauss')]
        else:
            rmid = 0.5 * (s['p1'] + s['p2']) * 10
            sm = [dict(index=0, mean=0.0, stddev=slong, type='Gauss'),
                  dict(index=1, mean=0.0, stddev=srp / rmid, type='Gauss')]
        if k == 'BTL':
            sm.append(dict(index=5, mean=0.0, stddev=SIG_T_BTL, type='Gauss'))
        entries.append(dict(volume=g.volume, sensitive=g.sensitive, value=dict(smearing=sm)))
    digi = tmpd / 'digi.json'
    digi.write_text(json.dumps({"acts-geometry-hierarchy-map": {"format-version": 0,
                                                                "value-identifier": "digitization-configuration"},
                                "entries": entries}))

    store = []

    class Dump(acts.examples.IAlgorithm):
        def __init__(self):
            acts.examples.IAlgorithm.__init__(self, 'DumpMeasTruth', acts.logging.WARNING)
            self.m = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'm'); self.m.initialize('measurements')
            self.h = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'h'); self.h.initialize('simhits')
            self.ms = acts.examples.ReadDataHandle(self, acts.examples.MeasurementSimHitsMap, 'ms'); self.ms.initialize('msh')
            self.p = acts.examples.ReadDataHandle(self, acts.examples.SimParticleContainer, 'p'); self.p.initialize('particles_generated')

        def execute(self, ctx):
            hits = list(self.h(ctx.eventStore)); meas = self.m(ctx.eventStore)
            tr = {}
            for mi, hi in self.ms(ctx.eventStore):
                hh = hits[hi]; b = hh.particleId
                tr[mi] = (int(b.vertexPrimary), int(b.particle), int(b.generation), int(b.vertexSecondary),
                          float(hh.depositedEnergy), float(hh.time))
            rows = []
            for mi, mm in enumerate(meas):
                g = mm.geometryId; srf = surf_by_geo[g]
                fp = mm.fullParameters; fp = fp() if callable(fp) else fp; par = np.array(fp, float).ravel()
                si = mm.subspaceIndices; si = si() if callable(si) else si; idx = [int(x) for x in si]
                l0 = par[0] if 0 in idx else 0.0
                l1 = par[1] if 1 in idx else 0.0
                gp = srf.localToGlobal(gctx, acts.Vector2(float(l0), float(l1)), acts.Vector3(1, 0, 0))
                fc = mm.fullCovariance; fc = fc() if callable(fc) else fc
                t = tr.get(mi, (-1, -1, -1, -1, 0.0, 0.0))
                tm = par[idx.index(5)] if 5 in idx else t[5]          # BTL: smeared time; else the SimHit time
                rows.append((sid_of[g], gp[0], gp[1], gp[2], math.sqrt(float(fc[0, 0])), math.sqrt(float(fc[1, 1])),
                             0.0) + t[:5] + (tm,))
            vz = {}
            for p in self.p(ctx.eventStore):
                b = p.particleId
                if int(b.generation) == 0 and int(b.vertexSecondary) == 0:
                    k = int(b.vertexPrimary); fpp = p.fourPosition
                    if k not in vz:
                        vz[k] = [float(fpp[0]), float(fpp[1]), float(fpp[2]), 0.0, 0.0, 0.0]
                    pt = float(p.transverseMomentum); ph = float(p.phi); th = float(p.theta)
                    pabs = pt / max(math.sin(th), 1e-12)
                    vz[k][3] += pt * math.cos(ph); vz[k][4] += pt * math.sin(ph); vz[k][5] += pabs * math.cos(th)
            store.append(dict(meas=np.array(rows, float).reshape(-1, len(COLS)),
                              vz=np.array([[k] + v for k, v in sorted(vz.items())], float).reshape(-1, 7)))
            return acts.examples.ProcessCode.SUCCESS

    npool = int(mu * nev + 6 * math.sqrt(mu * nev) + 50)
    pool = tmpd / 'pool.hepmc3'
    t0 = time.time()
    s4pu.make_pool(pool, npool, int(seed) % 900_000_000, TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat')
    t_pool = time.time() - t0
    rnd = acts.examples.RandomNumbers(seed=int(seed) % 2_000_000_000 + 1)
    s = acts.examples.Sequencer(events=nev, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
    R = acts.examples.hepmc3.HepMC3Reader
    vg = acts.examples.GaussianVertexGenerator(
        stddev=acts.Vector4(bs['sigma_xy_um'] * u.um, bs['sigma_xy_um'] * u.um, bs['sigma_z_mm'] * u.mm,
                            bs['sigma_t_ps'] * u.ns / 1000.0), mean=acts.Vector4(0, 0, 0, 0))
    s.addReader(R(inputs=[R.Input.Poisson(pool, mu)], level=acts.logging.WARNING, outputEvent='hepmc3_event',
                  checkEventNumber=False, numEvents=nev, randomNumbers=rnd, vertexGenerator=vg))
    s.addAlgorithm(acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent='hepmc3_event',
                                                             outputParticles='particles_generated',
                                                             outputVertices='vertices_generated', mergePrimaries=False))
    s.addWhiteboardAlias('particles', 'particles_generated')
    addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 1100 * u.mm), absZ=(0.0, 2.7 * u.m), eta=(-4.0, 4.0),
                                                      pt=(50 * u.MeV, None), removeNeutral=False))
    addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
    cfg = acts.examples.DigitizationAlgorithm.Config(
        digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(digi)), surfaceByIdentifier=surf_by_geo,
        randomNumbers=rnd, inputSimHits='simhits', outputMeasurements='measurements', doMerge=False,
        outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh', outputParticleMeasurementsMap='pm',
        outputSimHitMeasurementsMap='shm')
    s.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING))
    s.addAlgorithm(Dump())
    t1 = time.time(); s.run(); t_chain = time.time() - t1
    meta = dict(chain=CHAIN, n_events=nev, seed=int(seed), mu=mu, pool_size=npool, t_pool_s=round(t_pool, 2),
                t_chain_s=round(t_chain, 2), t_total_s=round(time.time() - t_start, 2), columns=COLS,
                n_meas=[int(len(r['meas'])) for r in store], n_vertices=[int(len(r['vz'])) for r in store])
    tmp = out.with_name(out.name + '.tmp.npz')
    np.savez(tmp, **{f'ev{i}': r['meas'] for i, r in enumerate(store)}, **{f'vz{i}': r['vz'] for i, r in enumerate(store)},
             meta=np.array(json.dumps(meta)))
    tmp.replace(out)
    for f in tmpd.iterdir():
        f.unlink()
    tmpd.rmdir()
    print(json.dumps(meta))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]) if len(sys.argv) > 4 else 200.0)
