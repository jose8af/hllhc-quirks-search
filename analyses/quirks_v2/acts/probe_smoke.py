"""E5 smoke probe: import pyacts 48.0.0 and list the pieces needed for the hybrid design (no simulation)."""
import time, re
t0 = time.time()
import acts, acts.examples
print("acts", acts.__version__, "import s", round(time.time() - t0, 2))
import acts.fatras, acts.json
def has(mod, names):
    for n in names:
        print(f"  {mod.__name__}.{n}: {'yes' if hasattr(mod, n) else 'NO'}")
has(acts, ["CylinderSurface", "DiscSurface", "PlaneSurface", "Surface", "CylinderBounds", "RadialBounds",
           "Transform3", "GeometryContext", "MagneticFieldContext", "ConstantBField", "SolenoidBField",
           "EigenStepper", "StraightLineStepper", "AtlasStepper", "Navigator", "Propagator",
           "Material", "MaterialSlab", "HomogeneousSurfaceMaterial", "TrackingGeometry",
           "Experimental", "BlueprintNode", "Blueprint", "CylinderContainerBlueprintNode",
           "LayerBlueprintNode", "StaticBlueprintNode", "ProtoLayer", "BoundaryTolerance",
           "Intersection3D", "SurfaceIntersection", "BoundTrackParameters", "ParticleHypothesis"])
has(acts.examples, ["GenericDetector", "TelescopeDetector", "Sequencer", "ParticleGun", "EventGenerator",
                    "FatrasSimulation", "DigitizationAlgorithm", "DigitizationConfig", "readDigiConfigFromJson",
                    "writeDigiConfigToJson", "DigiConfigConverter", "GeometricConfig", "SmearingConfig",
                    "HepMC3Reader", "HepMC3InputConverter", "CsvSimHitWriter", "CsvMeasurementWriter",
                    "PropagationAlgorithm", "SeedingAlgorithm", "TrackFindingAlgorithm", "ParquetWriter",
                    "SimHitReader", "CsvSimHitReader", "CsvParticleReader", "RandomNumbers"])
import acts.examples.simulation as sim
print("  simulation helpers:", [n for n in dir(sim) if n.startswith("add")])
import acts.examples.reconstruction as rec
print("  reconstruction helpers:", [n for n in dir(rec) if n.startswith("add")][:30])
for m in ["pythia8", "root", "edm4hep", "geant4", "dd4hep", "odd"]:
    try:
        __import__("acts.examples." + m); print("  acts.examples." + m, "OK")
    except Exception as e:
        print("  acts.examples." + m, "unavailable:", type(e).__name__)
# surface intersection probe
gctx = acts.GeometryContext()
u = acts.UnitConstants
try:
    cyl = acts.CylinderSurface(acts.Transform3.Identity() if hasattr(acts.Transform3, "Identity") else acts.Transform3(), 30 * u.mm, 200 * u.mm)
    print("  CylinderSurface built:", cyl)
except Exception as e:
    print("  CylinderSurface ctor:", type(e).__name__, str(e)[:300])
print("  Surface methods:", [n for n in dir(acts.Surface) if not n.startswith("_")])
print("  total s", round(time.time() - t0, 2))
