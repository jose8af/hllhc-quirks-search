"""val_v8.py -- Stage-3 validation V8: Stage-4 ingestion of a Stage-3 output file in the ACTS env (acts/pixi.toml,
pyacts 48.0.0), along the injection path of acts/scripts/smoke_test.py part B.  Run in the ACTS env:
    cd theory_track/acts && pixi run python ../sim/stage3/validation/val_v8.py <stage3_output.npz> [n_events=10]
Steps: (1) build one ACTS surface per Stage-3 recording surface from the file's own surf_table (cylinder:
CylinderBounds(R, half z); disc: RadialBounds(rmin, rmax) at z), each with its own GeometryIdentifier (volume 1,
layer = surface id + 1, sensitive 1); (2) every hit of the first n events on a physical surface (kinds IT, PS, 2S, BTL,
ETL; the virtual T3V layers are skipped) is checked with Surface.isOnSurface at its global position (mm) and momentum
direction; (3) every hit is converted to an acts.examples.SimHit (4-position x, y, z [mm], t [ns] x acts.UnitConstants,
4-momentum [GeV] before = after, barcode tagging the quirk) in a SimHitContainer; (4) digitisation attempted with the
generic smearing config on these surfaces (needs the surfaces in the config's geometry selection; reported).
PASS: all physical hits on their surface (tolerance 1 um), all SimHits constructed with the right units.
Output: sim/stage3/results/V8.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import acts
import acts.examples
import acts.examples.json
import acts.fatras
from acts import UnitConstants as u

HERE = Path(__file__).resolve().parent
f = sys.argv[1]
nev = int(sys.argv[2]) if len(sys.argv) > 2 else 10
z = np.load(f)
surf = z['surf_table']; kinds = [str(k) for k in z['surf_kinds']]; names = [str(k) for k in z['surf_names']]
gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
S = []
for i, (ty, p0, p1, p2) in enumerate(surf):
    if ty < 0.5:
        s = acts.Surface.createCylinder(acts.Transform3(acts.Vector3(0.0, 0.0, 0.0)), acts.CylinderBounds(p0 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    else:
        s = acts.Surface.createDisc(acts.Transform3(acts.Vector3(0.0, 0.0, p0 * 10.0 * u.mm)), acts.RadialBounds(p1 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    s.assignGeometryId(acts.GeometryIdentifier(volume=1, layer=i + 1, sensitive=1))
    S.append(s)
tolnames = [x for x in dir(acts.BoundaryTolerance) if not x.startswith('_')]
try:
    tol = acts.BoundaryTolerance.absoluteEuclidean(1e-3 * u.mm)
except Exception:
    tol = acts.BoundaryTolerance.infinite()
off = z['hit_offsets']
n_chk = n_on = n_skip = 0; worst = []
hits = acts.examples.SimHitContainer()
simhit_args = []
for e in range(min(nev, len(off) - 1)):
    for j in range(off[e], off[e + 1]):
        sid = int(z['h_surf'][j])
        pos = acts.Vector3(z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm)
        p = np.array([z['h_px'][j], z['h_py'][j], z['h_pz'][j]])
        d = acts.Vector3(*(p / np.linalg.norm(p)))
        bc = acts.fatras.Barcode(); bc.vertexPrimary = 9; bc.particle = 1 + int(z['h_quirk'][j])
        p4 = acts.Vector4(p[0] * u.GeV, p[1] * u.GeV, p[2] * u.GeV, z['h_E'][j] * u.GeV)
        sh = acts.examples.SimHit(S[sid].geometryId, bc, acts.Vector4(z['h_x'][j] * u.mm, z['h_y'][j] * u.mm,
                                                                       z['h_z'][j] * u.mm, z['h_t'][j] * u.ns), p4, p4, j - off[e])
        hits.insert(sh)
        simhit_args.append((sid, bc, (z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm, z['h_t'][j] * u.ns), p4, j - off[e]))
        if kinds[sid] == 'T3V':
            n_skip += 1
            continue
        n_chk += 1
        ok = S[sid].isOnSurface(gctx, pos, d, tol, 1e-3 * u.mm)
        n_on += int(ok)
        if not ok:
            worst.append((names[sid], float(z['h_x'][j]), float(z['h_y'][j]), float(z['h_z'][j])))
# unit sanity: t vs straight-line flight time from the vertex (hit time >= r/c)
r3 = np.sqrt((z['h_x'] - np.repeat(z['vtx'][:, 0], np.diff(off))) ** 2 + (z['h_y'] - np.repeat(z['vtx'][:, 1], np.diff(off))) ** 2
             + (z['h_z'] - np.repeat(z['vtx'][:, 2], np.diff(off))) ** 2)
dt = z['h_t'] - np.repeat(z['vtx'][:, 3], np.diff(off)) - r3 / 299.792458
digi = 'not attempted'
n_meas = -1
try:
    import tempfile
    DIGI = HERE.parents[2] / 'acts' / 'scripts' / 'configs' / 'generic-digi-smearing-config.json'
    dj = json.load(open(DIGI))
    # same generic 2D Gaussian smearing entry (GenericDetector pixel volume 7), re-keyed to volume 1 = Stage-3 surfaces
    dj['entries'] = [dict(volume=1, value=dj['entries'][0]['value'])]
    tmpd = Path(tempfile.mkdtemp()); (tmpd / 'digi.json').write_text(json.dumps(dj))
    store = {}

    class Inject(acts.examples.IAlgorithm):
        def __init__(self):
            acts.examples.IAlgorithm.__init__(self, 'InjectStage3', acts.logging.WARNING)
            self.outp = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'OutputSimHits')
            self.outp.initialize('simhits')

        def execute(self, ctx):
            c = acts.examples.SimHitContainer()
            for sid_, bc_, x4, p4_, k_ in simhit_args:
                c.insert(acts.examples.SimHit(S[sid_].geometryId, bc_, acts.Vector4(*x4), p4_, p4_, k_))
            self.outp(ctx, c)
            return acts.examples.ProcessCode.SUCCESS

    class CountM(acts.examples.IAlgorithm):
        def __init__(self):
            acts.examples.IAlgorithm.__init__(self, 'CountM', acts.logging.WARNING)
            self.h = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'm_h'); self.h.initialize('meas')

        def execute(self, ctx):
            store['n'] = len(self.h(ctx.eventStore))
            return acts.examples.ProcessCode.SUCCESS

    cfg = acts.examples.DigitizationAlgorithm.Config(
        digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(tmpd / 'digi.json')),
        surfaceByIdentifier={s.geometryId: s for s in S}, randomNumbers=acts.examples.RandomNumbers(seed=7),
        inputSimHits='simhits', outputMeasurements='meas', outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh',
        outputParticleMeasurementsMap='pm', outputSimHitMeasurementsMap='shm')
    seq = acts.examples.Sequencer(events=1, numThreads=1, logLevel=acts.logging.WARNING)
    seq.addAlgorithm(Inject()); seq.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING)); seq.addAlgorithm(CountM())
    seq.run()
    n_meas = int(store.get('n', -1))
    digi = f'Sequencer: injected {len(simhit_args)} SimHits -> DigitizationAlgorithm (generic 2D Gaussian smearing re-keyed to the Stage-3 surfaces) -> {n_meas} measurements'
except Exception as ex:
    digi = f'digitisation failed ({type(ex).__name__}: {str(ex)[:300]})'
res = dict(file=str(f), n_events=min(nev, len(off) - 1), n_simhits=len(simhit_args), n_checked=n_chk, n_on_surface=n_on,
           n_virtual_skipped=n_skip, not_on_surface=worst[:10], tolerance_mm=1e-3,
           min_t_minus_r_over_c_ns=float(dt.min()), frac_t_below_r_over_c=float(np.mean(dt < -1e-6)),
           digitisation=digi, n_measurements=n_meas, boundary_tolerance_options=tolnames, acts_version='.'.join(map(str, acts.__version__)))
res['PASS'] = bool(n_on == n_chk and len(simhit_args) == int(off[min(nev, len(off) - 1)]) and res['frac_t_below_r_over_c'] == 0.0 and n_meas == len(simhit_args))
out = HERE.parent / 'results' / 'V8.json'
json.dump(res, open(out, 'w'), indent=1)
print(json.dumps(res, indent=1))
