"""E5 probe: 1-thread wall time of the ACTS seeding + CKF chain (GenericDetector, smearing digi) at high multiplicity,
following ACTS v48.0.0 Examples/Scripts/Python/ckf_tracks.py with ROOT output disabled (not in the PyPI wheel).
Run: probe/venv/bin/python -I -W ignore probe_ckf_timing.py <smearing json> <seeding json> <N per event>"""
import sys, time
import acts, acts.examples, acts.examples.json
from acts import UnitConstants as u
from acts.examples.simulation import (addParticleGun, MomentumConfig, EtaConfig, PhiConfig, ParticleConfig, addFatras,
                                      addDigitization, addDigiParticleSelection, ParticleSelectorConfig)
from acts.examples.reconstruction import (addSeeding, SeedFinderConfigArg, SeedFinderOptionsArg, SeedingAlgorithm,
                                          addCKFTracks, TrackSelectorConfig, CkfConfig)
digi, geosel, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
det = acts.examples.GenericDetector(); tg = det.trackingGeometry()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8 * u.T)); rnd = acts.examples.RandomNumbers(seed=2)
s = acts.examples.Sequencer(events=1, numThreads=1, logLevel=acts.logging.WARNING)
addParticleGun(s, MomentumConfig(0.5 * u.GeV, 5.0 * u.GeV, transverse=True), EtaConfig(-2.5, 2.5, uniform=True),
               PhiConfig(0.0, 360.0 * u.degree), ParticleConfig(N, acts.PdgParticle.ePionPlus, randomizeCharge=True), rnd=rnd)
addFatras(s, tg, field, rnd=rnd)
addDigitization(s, tg, field, digiConfigFile=digi, rnd=rnd)
addDigiParticleSelection(s, ParticleSelectorConfig(pt=(0.5 * u.GeV, None), measurements=(9, None), removeNeutral=True))
addSeeding(s, tg, field,
           SeedFinderConfigArg(r=(None, 200 * u.mm), deltaR=(1 * u.mm, 300 * u.mm), collisionRegion=(-250 * u.mm, 250 * u.mm),
                               z=(-2000 * u.mm, 2000 * u.mm), maxSeedsPerSpM=1, sigmaScattering=5, radLengthPerSeed=0.1,
                               minPt=500 * u.MeV, impactMax=3 * u.mm),
           SeedFinderOptionsArg(bFieldInZ=3.8 * u.T, beamPos=(0.0, 0.0)), seedingAlgorithm=SeedingAlgorithm.GridTriplet,
           initialSigmas=[1 * u.mm, 1 * u.mm, 1 * u.degree, 1 * u.degree, 0 * u.e / u.GeV, 1 * u.ns],
           initialSigmaQoverPt=0.1 * u.e / u.GeV, initialSigmaPtRel=0.1, initialVarInflation=[1.0] * 6,
           geoSelectionConfigFile=geosel, outputDirRoot=None)
addCKFTracks(s, tg, field, TrackSelectorConfig(pt=(500 * u.MeV, None), absEta=(None, 3.0), loc0=(-4.0 * u.mm, 4.0 * u.mm),
             nMeasurementsMin=7, maxHoles=2, maxOutliers=2),
             CkfConfig(chi2CutOffMeasurement=15.0, chi2CutOffOutlier=25.0, numMeasurementsCutOff=10, seedDeduplication=True,
                       stayOnSeed=True), outputDirRoot=None, outputDirCsv=None)
t = time.time(); s.run(); dt = time.time() - t
print(f"N={N} pions, 1 event, 1 thread: gun+Fatras+digi+seeding+CKF = {dt:.2f} s")
