"""R1 constructive check 5 (ACTS env): probe the V8 measurement deficit. Same surfaces/digi config as val_v8.py.
Variants (D = C with doMerge=False): A = val_v8 as is (10 events in one ACTS event, barcode = quirk only); B = unique barcode per (event, quirk)
(vertexPrimary = event+1); C = B without T3V hits. Logs at INFO to catch the digitiser's own messages.
Run: cd acts && pixi run python ../sim/stage3/review/r1_constructive_checks/c5_v8_digi_probe.py <npz> [variant]"""
import json, sys, tempfile
from pathlib import Path
import numpy as np
import acts, acts.examples, acts.examples.json, acts.fatras
from acts import UnitConstants as u
TT = Path(__file__).resolve().parents[4]
f = sys.argv[1]; var = sys.argv[2] if len(sys.argv) > 2 else 'A'; nev = 10
lvl = acts.logging.INFO if len(sys.argv) > 3 else acts.logging.WARNING
z = np.load(f); surf = z['surf_table']; kinds = [str(k) for k in z['surf_kinds']]
S = []
for i, (ty, p0, p1, p2) in enumerate(surf):
    if ty < 0.5:
        s = acts.Surface.createCylinder(acts.Transform3(acts.Vector3(0.0, 0.0, 0.0)), acts.CylinderBounds(p0 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    else:
        s = acts.Surface.createDisc(acts.Transform3(acts.Vector3(0.0, 0.0, p0 * 10.0 * u.mm)), acts.RadialBounds(p1 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    s.assignGeometryId(acts.GeometryIdentifier(volume=1, layer=i + 1, sensitive=1)); S.append(s)
off = z['hit_offsets']; args = []
for e in range(nev):
    for j in range(off[e], off[e + 1]):
        sid = int(z['h_surf'][j])
        if var in ('C', 'D') and kinds[sid] == 'T3V': continue
        bc = acts.fatras.Barcode(); bc.vertexPrimary = 9 if var == 'A' else e + 1; bc.particle = 1 + int(z['h_quirk'][j])
        p = np.array([z['h_px'][j], z['h_py'][j], z['h_pz'][j]])
        p4 = acts.Vector4(p[0] * u.GeV, p[1] * u.GeV, p[2] * u.GeV, z['h_E'][j] * u.GeV)
        args.append((sid, bc, (z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm, z['h_t'][j] * u.ns), p4, j - off[e]))
dj = json.load(open(TT / 'acts/scripts/configs/generic-digi-smearing-config.json'))
dj['entries'] = [dict(volume=1, value=dj['entries'][0]['value'])]
tmpd = Path(tempfile.mkdtemp()); (tmpd / 'digi.json').write_text(json.dumps(dj)); store = {}
class Inject(acts.examples.IAlgorithm):
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, 'Inject', lvl)
        self.o = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'o'); self.o.initialize('simhits')
    def execute(self, ctx):
        c = acts.examples.SimHitContainer()
        for sid_, bc_, x4, p4_, k_ in args:
            c.insert(acts.examples.SimHit(S[sid_].geometryId, bc_, acts.Vector4(*x4), p4_, p4_, k_))
        store['n_in_container'] = len(c)
        self.o(ctx, c); return acts.examples.ProcessCode.SUCCESS
class CountM(acts.examples.IAlgorithm):
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, 'CountM', lvl)
        self.h = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'h'); self.h.initialize('meas')
    def execute(self, ctx):
        store['n_meas'] = len(self.h(ctx.eventStore)); return acts.examples.ProcessCode.SUCCESS
cfg = acts.examples.DigitizationAlgorithm.Config(
    digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(tmpd / 'digi.json')),
    surfaceByIdentifier={s.geometryId: s for s in S}, randomNumbers=acts.examples.RandomNumbers(seed=7),
    inputSimHits='simhits', outputMeasurements='meas', outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh',
    outputParticleMeasurementsMap='pm', outputSimHitMeasurementsMap='shm')
if var == 'D': cfg.doMerge = False
for k in ('doMerge', 'mergeNsigma', 'minEnergyDeposit', 'doClusterization', 'doOutputCells'):
    if hasattr(cfg, k): store['cfg_' + k] = getattr(cfg, k)
seq = acts.examples.Sequencer(events=1, numThreads=1, logLevel=lvl)
seq.addAlgorithm(Inject()); seq.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, lvl)); seq.addAlgorithm(CountM()); seq.run()
print(json.dumps(dict(file=f, variant=var, n_args=len(args), **{k: (v if isinstance(v, (int, float, bool)) else str(v)) for k, v in store.items()})))
