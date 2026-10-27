"""E5 probe: 1-thread wall time of Fatras + digitisation for a PU-200-sized particle multiplicity (gun stand-in,
no Pythia8), GenericDetector, 3.8 T.  Run: probe/venv/bin/python -I -W ignore probe_pu_timing.py <smearing json> <N>"""
import sys, time
import acts, acts.examples, acts.examples.json
from acts import UnitConstants as u
from acts.examples.simulation import addParticleGun, MomentumConfig, EtaConfig, PhiConfig, ParticleConfig, addFatras, addDigitization
cfg, N = sys.argv[1], int(sys.argv[2])
det = acts.examples.GenericDetector(); tg = det.trackingGeometry()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8 * u.T)); rnd = acts.examples.RandomNumbers(seed=1)
s = acts.examples.Sequencer(events=2, numThreads=1, logLevel=acts.logging.WARNING)
addParticleGun(s, MomentumConfig(0.5 * u.GeV, 5.0 * u.GeV, transverse=True), EtaConfig(-2.5, 2.5, uniform=True),
               PhiConfig(0.0, 360.0 * u.degree), ParticleConfig(N, acts.PdgParticle.ePionPlus, randomizeCharge=True), rnd=rnd)
addFatras(s, tg, field, rnd=rnd)
addDigitization(s, tg, field, digiConfigFile=cfg, rnd=rnd)
t = time.time(); s.run(); dt = time.time() - t
print(f"N={N} charged pions/event, 2 events, 1 thread: {dt:.2f} s total, {dt/2:.2f} s/event")
