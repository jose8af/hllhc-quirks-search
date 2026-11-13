"""val_v8_merge.py -- Stage-3 fix pass R1 (critical B-5, constructive B-5): cause of the V8 measurement deficit.
Same surfaces, injection and generic smearing digi config as val_v8.py (ACTS env, pyacts 48.0.0); reproduces the
constructive reviewer's probe review/r1_constructive_checks/c5_v8_digi_probe.py in stage3.
DigitizationAlgorithm.Config() defaults to doMerge = True, mergeNsigma = 1: smeared measurements on the SAME surface within
1 sigma are merged.  Here each Stage-3 surface is ONE ACTS surface (a whole cylinder or disc), so the two quirks' close hits
in the merged regime (and repeated crossings) can merge.
Variants (first n events of the file):
  A  = val_v8 as run (all events in one ACTS event, barcode = quirk only, T3V hits injected);
  C  = one barcode per (event, quirk) (vertexPrimary = event + 1), T3V hits NOT injected (Stage-4 recommendation);
each with doMerge = True (default) and doMerge = False.  Also counted from the file (no ACTS): cross-quirk same-surface hit
pairs within 10/30/100 um per event (physical surfaces), and same-quirk repeated crossings.
Run (theory_track/acts):  pixi run python ../sim/stage3/validation/val_v8_merge.py <npz> <variant A|C> <merge 0|1> [n=10]
Driver: the 4 V8 production files x {A, C} x {1, 0}; results appended to sim/stage3/results/V8_merge.jsonl.
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import acts
import acts.examples
import acts.examples.json
import acts.fatras
from acts import UnitConstants as u

HERE = Path(__file__).resolve().parent
TT = HERE.parents[2]
f, var, merge = sys.argv[1], sys.argv[2], bool(int(sys.argv[3]))
nev = int(sys.argv[4]) if len(sys.argv) > 4 else 10
z = np.load(f)
surf = z['surf_table']; kinds = [str(k) for k in z['surf_kinds']]
S = []
for i, (ty, p0, p1, p2) in enumerate(surf):
    if ty < 0.5:
        s = acts.Surface.createCylinder(acts.Transform3(acts.Vector3(0.0, 0.0, 0.0)), acts.CylinderBounds(p0 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    else:
        s = acts.Surface.createDisc(acts.Transform3(acts.Vector3(0.0, 0.0, p0 * 10.0 * u.mm)), acts.RadialBounds(p1 * 10.0 * u.mm, p2 * 10.0 * u.mm))
    s.assignGeometryId(acts.GeometryIdentifier(volume=1, layer=i + 1, sensitive=1)); S.append(s)
off = z['hit_offsets']; args = []
close = {10: 0, 30: 0, 100: 0}; rep_same = 0
for e in range(nev):
    lo, hi = off[e], off[e + 1]
    sid_e = z['h_surf'][lo:hi].astype(int); q_e = z['h_quirk'][lo:hi].astype(int)
    xyz = np.c_[z['h_x'][lo:hi], z['h_y'][lo:hi], z['h_z'][lo:hi]] * 1e3   # um
    for sid in np.unique(sid_e):
        if kinds[sid] == 'T3V':
            continue
        a = np.where((sid_e == sid) & (q_e == 0))[0]; b = np.where((sid_e == sid) & (q_e == 1))[0]
        rep_same += max(len(a) - 1, 0) + max(len(b) - 1, 0)
        if len(a) and len(b):
            d = np.linalg.norm(xyz[a][:, None, :] - xyz[b][None, :, :], axis=2).ravel()
            for t in close:
                close[t] += int(np.sum(d < t))
    for j in range(lo, hi):
        sid = int(z['h_surf'][j])
        if var == 'C' and kinds[sid] == 'T3V':
            continue
        bc = acts.fatras.Barcode(); bc.vertexPrimary = 9 if var == 'A' else e + 1; bc.particle = 1 + int(z['h_quirk'][j])
        p4 = acts.Vector4(z['h_px'][j] * u.GeV, z['h_py'][j] * u.GeV, z['h_pz'][j] * u.GeV, z['h_E'][j] * u.GeV)
        args.append((sid, bc, (z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm, z['h_t'][j] * u.ns), p4, j - lo))
dj = json.load(open(TT / 'acts/scripts/configs/generic-digi-smearing-config.json'))
dj['entries'] = [dict(volume=1, value=dj['entries'][0]['value'])]
tmpd = Path(tempfile.mkdtemp()); (tmpd / 'digi.json').write_text(json.dumps(dj)); store = {}


class Inject(acts.examples.IAlgorithm):
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, 'Inject', acts.logging.WARNING)
        self.o = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'o'); self.o.initialize('simhits')

    def execute(self, ctx):
        c = acts.examples.SimHitContainer()
        for sid_, bc_, x4, p4_, k_ in args:
            c.insert(acts.examples.SimHit(S[sid_].geometryId, bc_, acts.Vector4(*x4), p4_, p4_, k_))
        store['n_simhits_in_container'] = len(c)
        self.o(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


class CountM(acts.examples.IAlgorithm):
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, 'CountM', acts.logging.WARNING)
        self.h = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'h'); self.h.initialize('meas')

    def execute(self, ctx):
        store['n_meas'] = len(self.h(ctx.eventStore))
        return acts.examples.ProcessCode.SUCCESS


cfg = acts.examples.DigitizationAlgorithm.Config(
    digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(tmpd / 'digi.json')),
    surfaceByIdentifier={s.geometryId: s for s in S}, randomNumbers=acts.examples.RandomNumbers(seed=7),
    inputSimHits='simhits', outputMeasurements='meas', outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh',
    outputParticleMeasurementsMap='pm', outputSimHitMeasurementsMap='shm')
default = dict(doMerge=cfg.doMerge, mergeNsigma=cfg.mergeNsigma)
cfg.doMerge = merge
seq = acts.examples.Sequencer(events=1, numThreads=1, logLevel=acts.logging.WARNING)
seq.addAlgorithm(Inject()); seq.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING)); seq.addAlgorithm(CountM()); seq.run()
rec = dict(file=str(Path(f).resolve().relative_to(TT / 'data' / 'sim_stage3')), lam_keV=float(z['lam_keV']), variant=var, doMerge=merge,
           default_config=default, n_events=nev, n_simhits=len(args), n_meas=store['n_meas'],
           cross_quirk_pairs_within_um=close, same_quirk_repeated_crossings=rep_same, acts_version='.'.join(map(str, acts.__version__)))
with open(HERE.parent / 'results' / 'V8_merge.jsonl', 'a') as fo:
    fo.write(json.dumps(rec) + '\n')
print(json.dumps(rec))
