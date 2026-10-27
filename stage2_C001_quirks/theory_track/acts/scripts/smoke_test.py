"""smoke_test.py -- Stage-4 ACTS env smoke test (E5, 2026-10-11).  Infrastructure check only, no physics results.

What it checks, in the installed env theory_track/acts/pixi.toml (route R1 of INSTALL_CHECK.md):
  A. versions of pyacts, pythia8, pyhepmc, numpy, uproot, awkward.
  B. hybrid chain: ACTS GenericDetector (stand-in geometry), particle gun -> Fatras (3.8 T), plus EXTERNALLY computed
     sim-hits injected by a Python IAlgorithm (stand-in for T3_causal quirk hits), then ACTS digitisation of both
     (generic smearing config: 2D pixels, 1D strips).
  C. PU-200 path: Pythia8 minimum bias (14 TeV, SoftQCD:inelastic, CMS CP5 tune, ParticleDecays:limitTau0 with
     tau0Max = 10 mm as in CMS generation) -> full decay tree converted to HepMC3 with pyhepmc -> ACTS HepMC3Reader
     merging 200 interactions per event, each with its own vertex from a Gaussian luminous region (sigma_z = 45 mm,
     sigma_t = 190 ps [CMS-TDR-020 p.2-3]; sigma_xy = 5 um ESTIMATE from CERN-2020-010 Table 2-1 p.18; values in
     acts/geometry/cms_phase2_public.json "beamspot") -> charged-particle selection -> Fatras -> digitisation.
  D. reads acts/geometry/cms_phase2_public.json (the D111 public layout) and prints the layer summary.
Inputs: scripts/configs/generic-digi-smearing-config.json (ACTS v48.0.0 Examples/Configs), scripts/pythia8_tune_CP5.dat
(copy of sim/cards/pythia8_tune_CP5.dat), geometry/cms_phase2_public.json.
Run from theory_track/acts/:   nice pixi run python scripts/smoke_test.py [n_minbias=400] [n_pu=200]
Output: stdout (saved as scripts/smoke_test_output.txt).  Temporary HepMC3 file in probe/smoke_tmp/ (deleted at the end).
Single thread; keep it light while other production runs.
"""
import json, os, shutil, sys, time
from pathlib import Path

import numpy as np
import acts, acts.examples, acts.examples.json, acts.examples.hepmc3, acts.fatras
from acts import UnitConstants as u
from acts.examples.simulation import (addParticleGun, MomentumConfig, EtaConfig, PhiConfig, ParticleConfig, addFatras,
                                      addGenParticleSelection, ParticleSelectorConfig)
import pythia8, pyhepmc, uproot, awkward

HERE = Path(__file__).resolve().parent
ACTS_DIR = HERE.parent
DIGI = HERE / "configs" / "generic-digi-smearing-config.json"
CP5 = HERE / "pythia8_tune_CP5.dat"
GEO = ACTS_DIR / "geometry" / "cms_phase2_public.json"
TMP = ACTS_DIR / "probe" / "smoke_tmp"
N_MB = int(sys.argv[1]) if len(sys.argv) > 1 else 400
N_PU = int(sys.argv[2]) if len(sys.argv) > 2 else 200
t_all = time.time()
ok = {}

# ---------------------------------------------------------------- A. versions
print("== A. versions")
print(f"python {sys.version.split()[0]} | acts {'.'.join(map(str, acts.__version__))} | pythia8 module {pythia8.__file__.split('/')[-1]}"
      f" | pyhepmc {pyhepmc.__version__} | numpy {np.__version__} | uproot {uproot.__version__} | awkward {awkward.__version__}")

# ---------------------------------------------------------------- shared geometry (stand-in)
det = acts.examples.GenericDetector()
tg = det.trackingGeometry()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8 * u.T))
gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
sens = []
tg.visitSurfaces(lambda srf: sens.append(srf) if srf.geometryId.sensitive > 0 else None)
print(f"GenericDetector: {len(sens)} sensitive surfaces")


def digi_alg(inp, tag):
    cfg = acts.examples.DigitizationAlgorithm.Config(
        digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(DIGI)),
        surfaceByIdentifier=tg.geoIdSurfaceMap(), randomNumbers=acts.examples.RandomNumbers(seed=7),
        inputSimHits=inp, outputMeasurements=f"measurements_{tag}",
        outputMeasurementParticlesMap=f"mpmap_{tag}", outputMeasurementSimHitsMap=f"mshmap_{tag}",
        outputParticleMeasurementsMap=f"pmmap_{tag}", outputSimHitMeasurementsMap=f"shmmap_{tag}")
    return acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING)


class Counter(acts.examples.IAlgorithm):
    """Counts objects in whiteboard collections and stores them per event."""
    def __init__(self, name, specs, store):
        acts.examples.IAlgorithm.__init__(self, name, acts.logging.WARNING)
        self.h = []
        for key, typ in specs:
            hd = acts.examples.ReadDataHandle(self, typ, key + "_h"); hd.initialize(key); self.h.append((key, hd))
        self.store = store

    def execute(self, ctx):
        row = {}
        for key, hd in self.h:
            obj = hd(ctx.eventStore)
            row[key] = len(obj)
            if key.startswith("particles"):
                zs = [p.fourPosition[2] for p in obj]
                ts = [p.fourPosition[3] for p in obj]
                row["vtx_z_rms_mm"] = float(np.std(zs)) if zs else 0.0
                row["vtx_t_rms_ps"] = float(np.std(ts)) / (u.ns / 1000.0) if ts else 0.0
        self.store.append(row)
        return acts.examples.ProcessCode.SUCCESS


# ---------------------------------------------------------------- B. hybrid chain
print("\n== B. hybrid chain: gun -> Fatras + injected external hits -> digitisation")
rows_b = []


class InjectExternalHits(acts.examples.IAlgorithm):
    """Copies Fatras sim-hits and adds one external hit at the centre of every n-th sensitive surface."""
    def __init__(self):
        acts.examples.IAlgorithm.__init__(self, "InjectExternalHits", acts.logging.WARNING)
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, "InputSimHits")
        self.inp.initialize("simhits")
        self.outp = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, "OutputSimHits")
        self.outp.initialize("simhits_plus_ext")
        self.picked = sens[:: max(1, len(sens) // 6)]

    def execute(self, ctx):
        new = acts.examples.SimHitContainer()
        n_old = 0
        for h in self.inp(ctx.eventStore):
            new.insert(h); n_old += 1
        bc = acts.fatras.Barcode(); bc.vertexPrimary = 9; bc.particle = 1   # tag for 'external' (quirk) hits
        for k, srf in enumerate(self.picked):
            c = srf.center(gctx)
            nrm = float(np.sqrt(c[0] ** 2 + c[1] ** 2 + c[2] ** 2))
            p4 = acts.Vector4(500 * c[0] / nrm, 500 * c[1] / nrm, 500 * c[2] / nrm, 500.0)   # GeV-scale, radial
            new.insert(acts.examples.SimHit(srf.geometryId, bc, acts.Vector4(c[0], c[1], c[2], 0.0), p4, p4, k))
        rows_b.append(dict(fatras_hits=n_old, external_hits=len(self.picked)))
        self.outp(ctx, new)
        return acts.examples.ProcessCode.SUCCESS


t0 = time.time()
rnd = acts.examples.RandomNumbers(seed=42)
s = acts.examples.Sequencer(events=3, numThreads=1, logLevel=acts.logging.WARNING)
addParticleGun(s, MomentumConfig(1.0 * u.GeV, 10.0 * u.GeV, transverse=True), EtaConfig(-2.0, 2.0, uniform=True),
               PhiConfig(0.0, 360.0 * u.degree), ParticleConfig(5, acts.PdgParticle.eMuon, randomizeCharge=True), rnd=rnd)
addFatras(s, tg, field, rnd=rnd)
s.addAlgorithm(InjectExternalHits())
s.addAlgorithm(digi_alg("simhits_plus_ext", "b"))
cnt_b = []
s.addAlgorithm(Counter("CountB", [("measurements_b", acts.examples.MeasurementContainer)], cnt_b))
s.run()
for i, (r, c) in enumerate(zip(rows_b, cnt_b)):
    print(f"  event {i}: {r['fatras_hits']} Fatras hits + {r['external_hits']} external hits -> {c['measurements_b']} measurements")
ok["B"] = all(c["measurements_b"] == r["fatras_hits"] + r["external_hits"] for r, c in zip(rows_b, cnt_b))
print(f"  B {'PASS' if ok['B'] else 'FAIL'} ({time.time() - t0:.1f} s)")

# ---------------------------------------------------------------- C. PU-200 path
print(f"\n== C. Pythia8 CP5 minimum bias ({N_MB} interactions) -> HepMC3 -> ACTS ({N_PU} per event) -> Fatras -> digitisation")
geo = json.loads(GEO.read_text())
bs = geo["beamspot"]
TMP.mkdir(parents=True, exist_ok=True)
hepmc_path = TMP / "minbias_cp5_14TeV.hepmc3"

t0 = time.time()
py = pythia8.Pythia("", False)
py.readFile(str(CP5))
for line in ("Beams:eCM = 14000.", "SoftQCD:inelastic = on", "ParticleDecays:limitTau0 = on",
             "ParticleDecays:tau0Max = 10.", "Print:quiet = on", "Random:setSeed = on", "Random:seed = 20261011", "Next:numberCount = 0"):
    py.readString(line)
assert py.init(), "Pythia init failed"
t_init = time.time() - t0
t0 = time.time()


def to_hepmc(ev, iev):
    """Full-record Pythia8 -> HepMC3 conversion (same logic as Pythia8ToHepMC: a vertex per decaying mother system)."""
    ge = pyhepmc.GenEvent(pyhepmc.Units.GEV, pyhepmc.Units.MM)
    ge.event_number = iev
    parts = [None] * ev.size()
    for i in range(1, ev.size()):
        p = ev[i]
        gp = pyhepmc.GenParticle(pyhepmc.FourVector(p.px(), p.py(), p.pz(), p.e()), p.id(), 1 if p.isFinal() else (4 if i <= 2 else 2))
        gp.generated_mass = p.m()
        parts[i] = gp
        ge.add_particle(gp)
    endv = {}
    for i in range(3, ev.size()):
        p = ev[i]
        moms = tuple(sorted(set(m for m in p.motherList() if m > 0)))
        if not moms:
            moms = (1, 2)
        v = endv.get(moms)
        if v is None:
            v = pyhepmc.GenVertex(pyhepmc.FourVector(p.xProd(), p.yProd(), p.zProd(), p.tProd()))
            for m in moms:
                if parts[m].end_vertex is None:
                    v.add_particle_in(parts[m])
            ge.add_vertex(v)
            endv[moms] = v
        v.add_particle_out(parts[i])
    return ge


n_ok = 0; n_ch = []
with pyhepmc.io.WriterAscii(str(hepmc_path)) as w:
    while n_ok < N_MB:
        if not py.next():
            continue
        ev = py.event
        n_ch.append(sum(1 for i in range(ev.size()) if ev[i].isFinal() and ev[i].isCharged() and abs(ev[i].eta()) < 2.5))
        w.write(to_hepmc(ev, n_ok)); n_ok += 1
t_gen = time.time() - t0
sig = py.infoPython().sigmaGen()
print(f"  Pythia8: init {t_init:.1f} s; {n_ok} events in {t_gen:.1f} s (incl. Python HepMC3 conversion); sigma_gen(inelastic) = {sig:.1f} mb; "
      f"<N_ch(|eta|<2.5)> = {np.mean(n_ch):.1f}; file {hepmc_path.stat().st_size / 1e6:.0f} MB")

n_ev = N_MB // N_PU
t0 = time.time()
rnd = acts.examples.RandomNumbers(seed=43)
# FatrasSimulation raises a few floating-point UNDERFLOWS (FLTUND, in exp(); benign) at PU-200 multiplicity. The wheel's
# Sequencer fails on unmasked FPEs by default, so they are tracked and reported but do not abort the run.
s = acts.examples.Sequencer(events=n_ev, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
R = acts.examples.hepmc3.HepMC3Reader
vg = acts.examples.GaussianVertexGenerator(
    stddev=acts.Vector4(bs["sigma_xy_um"] * u.um, bs["sigma_xy_um"] * u.um, bs["sigma_z_mm"] * u.mm, bs["sigma_t_ps"] * u.ns / 1000.0),
    mean=acts.Vector4(0, 0, 0, 0))
s.addReader(R(inputs=[R.Input.Fixed(hepmc_path, N_PU)], level=acts.logging.WARNING, outputEvent="hepmc3_event",
              checkEventNumber=False, numEvents=n_ev, randomNumbers=rnd, vertexGenerator=vg))
conv = acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent="hepmc3_event",
                                                 outputParticles="particles_generated", outputVertices="vertices_generated",
                                                 mergePrimaries=False)
s.addAlgorithm(conv)
s.addWhiteboardAlias("particles", "particles_generated")
addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 24 * u.mm), absZ=(0.0, 1.0 * u.m), eta=(-4.0, 4.0),
                                                  pt=(150 * u.MeV, None), removeNeutral=True))
addFatras(s, tg, field, rnd=rnd)
s.addAlgorithm(digi_alg("simhits", "c"))
cnt_c = []
s.addAlgorithm(Counter("CountC", [("particles_generated", acts.examples.SimParticleContainer),
                                  ("particles_generated_selected", acts.examples.SimParticleContainer),
                                  ("simhits", acts.examples.SimHitContainer),
                                  ("measurements_c", acts.examples.MeasurementContainer)], cnt_c))
s.run()
t_acts = time.time() - t0
for i, c in enumerate(cnt_c):
    print(f"  PU-{N_PU} event {i}: {c['particles_generated']} generated particles, {c['particles_generated_selected']} "
          f"charged selected (pT>150 MeV, |eta|<4), {c['simhits']} sim-hits, {c['measurements_c']} measurements; "
          f"selected-particle vertex rms z = {c['vtx_z_rms_mm']:.1f} mm, t = {c['vtx_t_rms_ps']:.0f} ps")
ok["C"] = len(cnt_c) == n_ev and all(c["measurements_c"] > 1000 for c in cnt_c) and \
    all(20 < c["vtx_z_rms_mm"] < 80 for c in cnt_c)
print(f"  ACTS part: {t_acts:.1f} s for {n_ev} PU-{N_PU} events (1 thread)")
print(f"  C {'PASS' if ok['C'] else 'FAIL'} (expects >1000 measurements/event and a vertex z spread of 20-80 mm from "
      f"sigma_z = {bs['sigma_z_mm']} mm)")

# ---------------------------------------------------------------- D. public geometry file
print("\n== D. acts/geometry/cms_phase2_public.json (baseline D111)")
for e in geo["barrel_layers"]:
    print(f"  {e['name']:8s} r = {e['r_nominal_mm']:8.2f} mm (TDR-2017 {e['TDR_2017']['r_mm']:7.1f}; T3 {e['T3_slab_r_mm']:6.0f})"
          f"  |z| <= {e['z_max_nominal_mm']:7.1f} mm  {e['module_types']}")
print(f"  discs per side: {len(geo['endcap_discs'])}; beamspot: sigma_z {bs['sigma_z_mm']} mm, sigma_t {bs['sigma_t_ps']} ps, "
      f"sigma_xy {bs['sigma_xy_um']} um; material baseline: {geo['material']['baseline']}")
ok["D"] = len(geo["barrel_layers"]) == 10 and len(geo["endcap_discs"]) == 17

shutil.rmtree(TMP, ignore_errors=True)
print(f"\nSUMMARY: {' '.join(f'{k}:{'PASS' if v else 'FAIL'}' for k, v in ok.items())} | total {time.time() - t_all:.1f} s")
sys.exit(0 if all(ok.values()) else 1)
