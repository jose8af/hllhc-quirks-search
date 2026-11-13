"""p2_inject_digi.py -- Stage-4 PROBE (E9, plan turn).  Stage-3 truth hits -> ACTS (s4geo surfaces) -> smearing digitisation,
alone and overlaid on Fatras PU-200, one ACTS event per physics event (HANDOVER_STAGE4 §4 items 1-4).

Injection (HANDOVER §1/§4): kinds T3V skipped (and ETL, not in the probe geometry); one ACTS event per physics event; barcode
vertexPrimary = 4000 (signal tag; PU vertices are 1..200), particle = 1 + h_quirk; p4_after built from h_dE (E_after = E - dE,
|p| rescaled on shell with the quirk mass) so that depositedEnergy() = h_dE; doMerge = False (user U-5 (b)).
Digitisation (smearing, CMS Phase-2-like, from acts/geometry/cms_phase2_public.json module_types; binary resolution pitch/sqrt12
as baseline; Gaussian approximation for strip/macro-pixel lengths):
  IT  (25 x 100 um):    rphi 7.2 um, long (z barrel / r disc) 28.9 um
  PS  (100 um x 1.467 mm): rphi 28.9 um, long 423 um
  2S  (90 um x 50.27 mm):  rphi 26.0 um, long 14.5 mm
  BTL (ESTIMATE, timing layer): rphi 0.87 mm, z 16 mm, time 35 ps (UNVERIFIED)
  Disc surfaces: loc0 = r (long), loc1 = phi with sigma_phi = sigma_rphi / r_mid (full-disc approximation, see plan §1.4).
Checks: (i) signal only: n_meas == n_SimHits (exact, doMerge = False) for every event; (ii) each measurement maps back to one
SimHit; (iii) timing per step with PU overlay.
Run (theory_track/acts): nice pixi run python stage4/probes/p2_inject_digi.py <stage3 npz> [n_events=10] [n_mb=1200]
Outputs: data/acts_stage4/p2/{p2_summary.json, meas_<tag>.npz (global measurement positions + covariance + truth link)}.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s4geo  # noqa: E402

TT = s4geo.TT
OUT = TT / 'data' / 'acts_stage4' / 'p2'
OUT.mkdir(parents=True, exist_ok=True)
F = sys.argv[1]
NEV = int(sys.argv[2]) if len(sys.argv) > 2 else 10
N_MB = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
GEO = json.loads((TT / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())
bs = GEO['beamspot']
RES = {'IT': (7.2e-3, 28.9e-3), 'PS': (28.9e-3, 0.423), '2S': (26.0e-3, 14.5), 'BTL': (0.87, 16.0)}   # mm (rphi, long)
SIG_T_BTL = 0.035   # ns, ESTIMATE/UNVERIFIED (MTD TDR order of magnitude)

tg, els, sid_of, geo_of, surfs, passive = s4geo.build()
gctx = acts.GeometryContext.dangerouslyDefaultConstruct()
field = acts.ConstantBField(acts.Vector3(0, 0, 3.8112 * u.T))
tab = {s['sid']: s for s in surfs}
surf_by_geo = {e.surface().geometryId: e.surface() for e in els}


def digi_json():
    entries = []
    for g, sid in sid_of.items():
        s = tab[sid]; k = s['kind']
        srp, slong = RES[k]
        if s['type'] == 0:
            sm = [dict(index=0, mean=0.0, stddev=srp, type='Gauss'), dict(index=1, mean=0.0, stddev=slong, type='Gauss')]
        else:
            rmid = 0.5 * (s['p1'] + s['p2']) * 10
            sm = [dict(index=0, mean=0.0, stddev=slong, type='Gauss'), dict(index=1, mean=0.0, stddev=srp / rmid, type='Gauss')]
        if k == 'BTL':
            sm.append(dict(index=5, mean=0.0, stddev=SIG_T_BTL, type='Gauss'))
        entries.append(dict(volume=g.volume, sensitive=g.sensitive, value=dict(smearing=sm)))
    j = {"acts-geometry-hierarchy-map": {"format-version": 0, "value-identifier": "digitization-configuration"}, "entries": entries}
    p = OUT / 'digi_smearing_s4.json'
    p.write_text(json.dumps(j, indent=0))
    return p


DIGI = digi_json()
z = np.load(F)
kinds = [str(k) for k in z['surf_kinds']]
off = z['hit_offsets']
m_q = float(z['m'])
geo_of_sid = {v: k for k, v in sid_of.items()}
CENTRAL = len(sys.argv) > 4 and sys.argv[4] == 'central'
EVSEL = [e for e in range(len(off) - 1) if (not CENTRAL or abs(float(z['eta'][e])) < 1.0) and int(z['status'][e]) == 1][:NEV]
NEV = len(EVSEL)
ev_simhits = []
for e in EVSEL:
    rows = []
    for j in range(off[e], off[e + 1]):
        sid = int(z['h_surf'][j])
        if kinds[sid] in ('T3V', 'ETL'):
            continue
        E = float(z['h_E'][j]); px, py_, pz = float(z['h_px'][j]), float(z['h_py'][j]), float(z['h_pz'][j])
        p = math.sqrt(px * px + py_ * py_ + pz * pz)
        Ea = E - float(z['h_dE'][j]); pa = math.sqrt(max(Ea * Ea - m_q * m_q, 0.0)); f = pa / p
        rows.append((sid, int(z['h_quirk'][j]), (z['h_x'][j] * u.mm, z['h_y'][j] * u.mm, z['h_z'][j] * u.mm, z['h_t'][j] * u.ns),
                     (px * u.GeV, py_ * u.GeV, pz * u.GeV, E * u.GeV), (px * f * u.GeV, py_ * f * u.GeV, pz * f * u.GeV, Ea * u.GeV), j - off[e]))
    ev_simhits.append(rows)


class Inject(acts.examples.IAlgorithm):
    """Adds the physics event's quirk SimHits to the (optional) PU SimHits; event number -> physics event."""
    def __init__(self, with_pu):
        acts.examples.IAlgorithm.__init__(self, 'InjectStage3', acts.logging.WARNING)
        self.with_pu = with_pu
        if with_pu:
            self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_all')

    def execute(self, ctx):
        c = acts.examples.SimHitContainer()
        if self.with_pu:
            for h in self.inp(ctx.eventStore):
                c.insert(h)
        for sid, q, x4, p4b, p4a, k in ev_simhits[ctx.eventNumber]:
            bc = acts.fatras.Barcode(); bc.vertexPrimary = 4000; bc.particle = 1 + q
            c.insert(acts.examples.SimHit(geo_of_sid[sid], bc, acts.Vector4(*x4), acts.Vector4(*p4b), acts.Vector4(*p4a), k))
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


class Dump(acts.examples.IAlgorithm):
    def __init__(self, store):
        acts.examples.IAlgorithm.__init__(self, 'DumpMeas', acts.logging.WARNING)
        self.m = acts.examples.ReadDataHandle(self, acts.examples.MeasurementContainer, 'm'); self.m.initialize('measurements')
        self.h = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'h'); self.h.initialize('simhits_all')
        self.ms = acts.examples.ReadDataHandle(self, acts.examples.MeasurementSimHitsMap, 'ms'); self.ms.initialize('msh')
        self.store = store

    def execute(self, ctx):
        t0 = time.time()
        hits = list(self.h(ctx.eventStore)); meas = self.m(ctx.eventStore)
        flag = {}
        for mi, hi in self.ms(ctx.eventStore):
            b = hits[hi].particleId
            flag[mi] = (1 + int(b.particle) - 1) if b.vertexPrimary == 4000 else 0   # 1/2 = quirk +q/-q, 0 = PU
        rows = []
        for mi, mm in enumerate(meas):
            g = mm.geometryId; srf = surf_by_geo[g]
            fp = mm.fullParameters; fp = fp() if callable(fp) else fp; par = np.array(fp, float).ravel()
            si = mm.subspaceIndices; si = si() if callable(si) else si; idx = [int(x) for x in si]
            l0 = par[0] if 0 in idx else 0.0   # fullParameters is the full 6-vector (subspace given by idx)
            l1 = par[1] if 1 in idx else 0.0
            gp = srf.localToGlobal(gctx, acts.Vector2(float(l0), float(l1)), acts.Vector3(1, 0, 0))
            fc = mm.fullCovariance; fc = fc() if callable(fc) else fc
            cov = np.array([[float(fc[a, b]) for b in range(2)] for a in range(2)])
            rows.append((sid_of[g], gp[0], gp[1], gp[2], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), flag.get(mi, -1)))
        sig = sum(1 for h in hits if h.particleId.vertexPrimary == 4000)
        self.store.append(dict(n_simhits=len(hits), n_signal_simhits=sig, n_meas=len(meas),
                               meas=np.array(rows, float).reshape(-1, 7), dump_s=time.time() - t0))
        return acts.examples.ProcessCode.SUCCESS


def run(with_pu, tag):
    store = []
    rnd = acts.examples.RandomNumbers(seed=77)
    s = acts.examples.Sequencer(events=NEV, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False)
    if with_pu:
        R = acts.examples.hepmc3.HepMC3Reader
        vg = acts.examples.GaussianVertexGenerator(
            stddev=acts.Vector4(bs['sigma_xy_um'] * u.um, bs['sigma_xy_um'] * u.um, bs['sigma_z_mm'] * u.mm, bs['sigma_t_ps'] * u.ns / 1000.0),
            mean=acts.Vector4(0, 0, 0, 0))
        s.addReader(R(inputs=[R.Input.Fixed(hepmc_path, 200)], level=acts.logging.WARNING, outputEvent='hepmc3_event',
                      checkEventNumber=False, numEvents=NEV, randomNumbers=rnd, vertexGenerator=vg))
        s.addAlgorithm(acts.examples.hepmc3.HepMC3InputConverter(level=acts.logging.WARNING, inputEvent='hepmc3_event',
                                                                 outputParticles='particles_generated', outputVertices='vertices_generated',
                                                                 mergePrimaries=False))
        s.addWhiteboardAlias('particles', 'particles_generated')
        addGenParticleSelection(s, ParticleSelectorConfig(rho=(0.0, 1100 * u.mm), absZ=(0.0, 2.7 * u.m), eta=(-4.0, 4.0),
                                                          pt=(50 * u.MeV, None), removeNeutral=False))
        addFatras(s, tg, field, rnd=rnd, pMin=0.03 * u.GeV, logLevel=acts.logging.ERROR)
    s.addAlgorithm(Inject(with_pu))
    cfg = acts.examples.DigitizationAlgorithm.Config(
        digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(DIGI)), surfaceByIdentifier=surf_by_geo,
        randomNumbers=rnd, inputSimHits='simhits_all', outputMeasurements='measurements', doMerge=False,
        outputMeasurementParticlesMap='mp', outputMeasurementSimHitsMap='msh', outputParticleMeasurementsMap='pm',
        outputSimHitMeasurementsMap='shm')
    s.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING))
    s.addAlgorithm(Dump(store))
    t0 = time.time(); s.run(); wall = time.time() - t0
    np.savez_compressed(OUT / f'meas_{tag}_{Path(F).stem}{"_central" if CENTRAL else ""}.npz', vtx=z['vtx'][EVSEL], recoil=z['recoil'][EVSEL], p_qp=z['p_qp'][EVSEL], p_qm=z['p_qm'][EVSEL], evsel=np.array(EVSEL),
                        **{f'ev{i}': r['meas'] for i, r in enumerate(store)})
    return store, wall


summary = dict(file=F, n_events=NEV, m=m_q, lam_keV=float(z['lam_keV']), cfg=str(z['cfg']))
st, wall = run(False, 'sig')
summary['signal_only'] = dict(wall_s=round(wall, 2), per_event=[(r['n_simhits'], r['n_meas']) for r in st],
                              exact=all(r['n_simhits'] == r['n_meas'] for r in st), events=EVSEL,
                              n_injected=[len(x) for x in ev_simhits], n_T3V_ETL_skipped=int(sum(off[e + 1] - off[e] for e in EVSEL) - sum(len(x) for x in ev_simhits)))
# residual check: each signal-only measurement vs the nearest truth hit on the same surface (ACTS reorders hits by geoId)
mres = []
for e, r in enumerate(st):
    me = r['meas']; tr = np.array([[x[0], x[2][0], x[2][1], x[2][2]] for x in ev_simhits[e]])
    for row in me:
        cand = tr[tr[:, 0] == row[0]]
        mres.append(np.min(np.linalg.norm(cand[:, 1:4] - row[1:4], axis=1)) if len(cand) else np.inf)
mr = np.array(mres)
summary['signal_only']['meas_to_nearest_truth_same_surface_mm'] = dict(median=float(np.median(mr)), p99=float(np.percentile(mr, 99)), max=float(mr.max()))
print('signal only', json.dumps(summary['signal_only']))
if N_MB == 0:
    (OUT / 'p2_summary.json').write_text(json.dumps(summary, indent=1)); sys.exit(0)
import s4pu  # noqa: E402
hepmc_path = OUT / 'minbias_pool_p2.hepmc3'
t_pool = s4pu.make_pool(hepmc_path, N_MB, 20261014, TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat')
st, wall = run(True, 'sig_pu')
summary['pool'] = dict(n=N_MB, wall_s=round(t_pool, 1))
nsig = [r['n_signal_simhits'] for r in st]
summary['signal_plus_pu'] = dict(wall_s=round(wall, 2), s_per_event=round(wall / NEV, 2), n_simhits=[r['n_simhits'] for r in st],
                                 n_meas=[r['n_meas'] for r in st], exact=all(r['n_simhits'] == r['n_meas'] for r in st),
                                 n_signal_simhits=nsig, signal_matches_injected=nsig == [len(x) for x in ev_simhits],
                                 dump_s_per_event=round(float(np.mean([r['dump_s'] for r in st])), 2))
print('signal+PU', json.dumps(summary['signal_plus_pu']))
(OUT / 'p2_summary.json').write_text(json.dumps(summary, indent=1))
hepmc_path.unlink()
