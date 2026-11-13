"""E5 probe (2026-10-11): functional check of the pyacts 48.0.0 PyPI wheel for the hybrid design.

Purpose: show, on 1 thread and a few events, that the wheel can (1) build a tracking geometry (GenericDetector),
(2) run Fatras on SM particles with material, (3) inject EXTERNALLY computed sim-hits (stand-ins for T3_causal
quirk hits) through a Python IAlgorithm, and (4) digitise both hit collections with a smearing config that has
2D pixel and 1D strip (loc0 only = "no z") entries.
Inputs: acts/probe/src/generic-digi-smearing-config.json (ACTS v48.0.0 Examples/Configs, downloaded).
Run (scratch venv, not part of any project env):
    acts/probe/venv/bin/python -I -W ignore acts/probe_hybrid.py <path to generic-digi-smearing-config.json> <outdir>
"""
import sys, time
from pathlib import Path
import acts, acts.examples, acts.examples.json, acts.fatras
from acts import UnitConstants as u
from acts.examples.simulation import (addParticleGun, MomentumConfig, EtaConfig, PhiConfig, ParticleConfig,
                                      addFatras)

digi_cfg = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
t0 = time.time()
det = acts.examples.GenericDetector()
tg = det.trackingGeometry()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8 * u.T))
gctx = acts.GeometryContext.dangerouslyDefaultConstruct()

# collect sensitive surfaces (geometry id, centre radius, z)
sens = []
def visit(srf):
    gid = srf.geometryId
    if gid.sensitive > 0:
        c = srf.center(gctx)
        sens.append((gid, srf, (c[0] ** 2 + c[1] ** 2) ** 0.5, c[2]))
tg.visitSurfaces(visit)
vols = sorted({s[0].volume for s in sens})
print(f"geometry built in {time.time()-t0:.1f} s: {len(sens)} sensitive surfaces, volumes {vols}")

rnd = acts.examples.RandomNumbers(seed=42)
s = acts.examples.Sequencer(events=3, numThreads=1, logLevel=acts.logging.WARNING)
addParticleGun(s, MomentumConfig(1.0 * u.GeV, 10.0 * u.GeV, transverse=True), EtaConfig(-2.0, 2.0, uniform=True),
               PhiConfig(0.0, 360.0 * u.degree), ParticleConfig(5, acts.PdgParticle.eMuon, randomizeCharge=True),
               rnd=rnd)
addFatras(s, tg, field, rnd=rnd)


class InjectExternalHits(acts.examples.IAlgorithm):
    """Adds one externally supplied hit at the centre of each of the first barrel sensitive surfaces found
    (a stand-in for T3_causal hits intersected with ACTS surfaces outside ACTS)."""
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, "InjectExternalHits", acts.logging.INFO)
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, "InputSimHits")
        self.inp.initialize("simhits")
        self.outp = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, "OutputSimHits")
        self.outp.initialize("simhits_plus_ext")

    def execute(self, ctx):
        old = self.inp(ctx.eventStore)
        new = acts.examples.SimHitContainer()
        n_old = 0
        for h in old:
            new.insert(h); n_old += 1
        bc = acts.fatras.Barcode()
        try:
            bc = bc.withVertexPrimary(9).withParticle(1)
        except Exception:
            pass
        n_ext = 0
        for gid, srf, r, z in sens[:: max(1, len(sens) // 6)]:
            c = srf.center(gctx)
            pos4 = acts.Vector4(c[0], c[1], c[2], 0.0)
            mom = acts.Vector4(c[0], c[1], c[2], 0.0)  # radial unit-ish direction; only used for incidence
            nrm = (c[0] ** 2 + c[1] ** 2 + c[2] ** 2) ** 0.5
            p4 = acts.Vector4(100 * c[0] / nrm, 100 * c[1] / nrm, 100 * c[2] / nrm, 100.0)
            new.insert(acts.examples.SimHit(gid, bc, pos4, p4, p4, n_ext)); n_ext += 1
        print(f"  event {ctx.eventNumber}: {n_old} Fatras hits + {n_ext} external hits")
        self.outp(ctx, new)
        return acts.examples.ProcessCode.SUCCESS


s.addAlgorithm(InjectExternalHits())
digiCfg = acts.examples.DigitizationAlgorithm.Config(
    digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(digi_cfg)),
    surfaceByIdentifier=tg.geoIdSurfaceMap(), randomNumbers=rnd, inputSimHits="simhits_plus_ext",
    outputMeasurements="measurements", outputMeasurementParticlesMap="measurement_particles_map",
    outputMeasurementSimHitsMap="measurement_simhits_map", outputParticleMeasurementsMap="particle_measurements_map",
    outputSimHitMeasurementsMap="simhit_measurements_map")
s.addAlgorithm(acts.examples.DigitizationAlgorithm(digiCfg, acts.logging.WARNING))
s.addWriter(acts.examples.CsvMeasurementWriter(level=acts.logging.WARNING, inputMeasurements="measurements",
            inputClusters="", inputMeasurementSimHitsMap="measurement_simhits_map", outputDir=str(out)))
t1 = time.time()
s.run()
print(f"sequence run in {time.time()-t1:.1f} s; CSV written to {out}")
