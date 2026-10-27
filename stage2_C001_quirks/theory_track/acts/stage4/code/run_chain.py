"""code/run_chain.py -- Stage-4 PRODUCTION chain (gate G1, 2026-10-13; acts env).  Plan §1 (R9 PASS), §1.8.

One call = one chain job: generate/inject -> Fatras on the 32-phi-sector Stage-3 surfaces -> smearing digitisation
(doMerge = False) -> GridTriplet seeding + CKF (pT > 0.9 GeV) -> per-event compact npz for the TT side.

  pixi run python stage4/code/run_chain.py pu  <out.npz> <n_events> <job_seed> [--mu 200]       (run from theory_track/acts)

Output npz (per chain event i):
  ev<i>   (n, 13) float64, columns COLS (= pu_chain_interim.COLS, so finder/pu_inputs.py reads it unchanged):
          sid (Stage-3 surface id), x, y, z (smeared global, mm), s0, s1 (local sigma, mm), flag (bit0: measurement on a
          selected CKF track), vp, particle, gen, vsec (truth barcode), dE (GeV), t (ns; BTL: smeared time)
          ONLY the barrel counting surfaces (TBPX L1-4, TBPS/TB2S in/out) and the BTL are written (the finder is barrel-
          only, WP_RULE §1.1); every other measurement enters only the V4-1 counts and the CKF.
  tru<i>  (n, 3) float32 truth (SimHit) global position of each written measurement (analysis-level merging, U-5 b)
  vz<i>   (n_int, 8): vp, x, y, z [mm], t [ns], sum px, py, pz of the selected prompt particles (exact interaction ids)
  v41     (n_events, len(V41_COLS)) V4-1 ingestion-closure record per event (all surfaces)
  timing  (n_events, len(T_COLS)) seconds per stage
  meta    JSON (mode, seeds, versions, column names, totals)

Fixed pitfalls carried from the probes: Fatras pMin = 30 MeV; material molar densities in mol/mm^3 (s4geo); doMerge = False
explicitly; times in ns on output (ACTS internal time unit is mm/c).
"""
import argparse
import json
import math
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import acts
import acts.examples
import acts.examples.json
import acts.fatras
from acts import UnitConstants as u
from acts.examples.simulation import addFatras
from acts.examples.reconstruction import (addSeeding, SeedFinderConfigArg, SeedFinderOptionsArg, SeedingAlgorithm,
                                          addCKFTracks, TrackSelectorConfig, CkfConfig)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import s4geo  # noqa: E402
import s4pu  # noqa: E402

CHAIN = 'g1-v1'
TT = s4geo.TT
CP5 = TT / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat'
COLS = ['sid', 'x', 'y', 'z', 's0', 's1', 'flag', 'vp', 'particle', 'gen', 'vsec', 'dE', 't']
V41_COLS = ['n_simhits', 'n_meas', 'n_map', 'map_injective', 'n_unmapped_geo', 'n_written', 'max_onsurf_um',
            'n_causal_viol', 'n_sig_simhits', 'n_sig_meas', 'n_ckf_tracks', 'n_ckf_meas', 'n_particles_in']
T_COLS = ['gen', 'source', 'fatras_digi', 'seeding', 'ckf', 'dump']
TOY_COLS = ['sid', 'x', 'y', 'z', 't_ns', 'pxb', 'pyb', 'pzb', 'Eb', 'pxa', 'pya', 'pza', 'Ea', 'vp', 'vsec', 'particle',
            'gen', 'sub']
NPHI = 32
B0 = 3.8112 * u.T
BARREL_COUNT = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4'] + [f'{a}_L{k}_{s}' for a in ('TBPS', 'TB2S') for k in (1, 2, 3)
                                                                for s in ('in', 'out')]
TIMES = []          # (event, stage, wall time) stamps


def _call(x):
    return x() if callable(x) else x


class Stamp(acts.examples.IAlgorithm):
    def __init__(self, name):
        acts.examples.IAlgorithm.__init__(self, 'Stamp_' + name, acts.logging.WARNING)
        self.nm = name

    def execute(self, ctx):
        TIMES.append((ctx.eventNumber, self.nm, time.perf_counter()))
        return acts.examples.ProcessCode.SUCCESS


class ParticleSource(acts.examples.IAlgorithm):
    """Direct SimParticle reader (plan §1.4): provider(event_number) -> (P (n, 12) s4pu.PCOLS, vz, info)."""

    def __init__(self, provider, store):
        acts.examples.IAlgorithm.__init__(self, 'ParticleSource', acts.logging.WARNING)
        self.provider = provider
        self.store = store
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimParticleContainer, 'out')
        self.out.initialize('particles_input')

    def execute(self, ctx):
        t0 = time.perf_counter()
        P, vz, info = self.provider(ctx.eventNumber)
        t1 = time.perf_counter()
        c = acts.examples.SimParticleContainer()
        cnt = {}
        SP = acts.examples.SimParticle; BC = acts.fatras.Barcode; V4 = acts.Vector4; V3 = acts.Vector3
        Pdg = acts.PdgParticle
        for row in P.tolist():
            vp, vsec, pdg, q, m, x, y, z, t, px, py, pz = row
            key = (int(vp), int(vsec))
            k = cnt.get(key, 0) + 1
            cnt[key] = k
            b = BC(); b.vertexPrimary = key[0]; b.vertexSecondary = key[1]; b.particle = k
            p = SP(b, Pdg(int(pdg)), q, m * u.GeV)
            p.fourPosition = V4(x * u.mm, y * u.mm, z * u.mm, t * u.ns)
            pa = math.sqrt(px * px + py * py + pz * pz)
            p.direction = V3(px / pa, py / pa, pz / pa)
            p.absoluteMomentum = pa * u.GeV
            c.insert(p)
        self.out(ctx, c)
        self.store[ctx.eventNumber] = dict(vz=vz, info=info, n_in=len(P), t_gen=t1 - t0,
                                           t_source=time.perf_counter() - t1)
        return acts.examples.ProcessCode.SUCCESS


class Dump(acts.examples.IAlgorithm):
    """Per event: written measurements (barrel counting + BTL) with CKF flag and truth, plus the V4-1 record."""

    def __init__(self, G, store, with_ckf=True, with_mom=False, count_vp=None, store_vp=None):
        acts.examples.IAlgorithm.__init__(self, 'Dump', acts.logging.WARNING)
        self.G = G; self.store = store; self.with_ckf = with_ckf; self.with_mom = with_mom; self.count_vp = count_vp
        self.store_vp = store_vp
        H = acts.examples.ReadDataHandle
        self.m = H(self, acts.examples.MeasurementContainer, 'm'); self.m.initialize('measurements')
        self.h = H(self, acts.examples.SimHitContainer, 'h'); self.h.initialize('simhits_all')
        self.ms = H(self, acts.examples.MeasurementSimHitsMap, 'ms'); self.ms.initialize('measurement_simhits_map')
        if with_ckf:
            self.t = H(self, acts.examples.ConstTrackContainer, 't'); self.t.initialize('tracks')

    def execute(self, ctx):
        t0 = time.perf_counter()
        G = self.G
        es = ctx.eventStore
        hits = self.h(es)
        meas = self.m(es)
        nh = len(hits); nm = len(meas)
        # measurement -> simhit map (doMerge = False: one simhit per measurement)
        m2h = np.full(nm, -1, np.int64); nmap = 0; multi = 0
        for mi, hi in self.ms(es):
            if m2h[mi] >= 0:
                multi += 1
            m2h[mi] = hi; nmap += 1
        # V4-1 map test: every measurement has exactly one simhit and no simhit is used twice.  A simhit can be LOST
        # (no measurement) when ACTS's bounded smearing fails minMaxRetries = 10 times at a surface/sector bound
        # (G1: 3 of 3.0e6 simhits in 24 PU events); those are counted and listed (lost<i>).
        bij = int(nmap == nm and multi == 0 and np.all(m2h >= 0) and len(np.unique(m2h)) == nm and nm <= nh)
        lost = []
        if nh != nm:        # simhits without a measurement (bounded smearing gave up): record where they are
            hl0 = list(hits)
            miss = np.setdiff1d(np.arange(nh), m2h[m2h >= 0])
            for hi in miss[:50]:
                hh = hl0[int(hi)]; fp = hh.fourPosition; g = hh.geometryId
                lost.append((G['geo_sid'].get(g.value, -1), g.volume, g.layer, g.sensitive, fp[0], fp[1], fp[2],
                             int(hh.particleId.vertexPrimary)))
        # CKF-used measurements
        used = np.zeros(nm, bool); ntr = 0
        if self.with_ckf:
            tr = self.t(es)
            ntr = len(tr)
            ISL = acts.examples.IndexSourceLink
            for i in range(ntr):
                for ts in _call(tr.getTrack(i).trackStatesReversed):
                    if _call(ts.hasUncalibratedSourceLink):
                        used[int(_call(ISL.fromSourceLink(_call(ts.uncalibratedSourceLink)).index))] = True
        if self.count_vp is not None:     # V4-1 for injected hits: measurements of injected simhits on ALL surfaces
            hl1 = list(hits)
            inj = np.array([int(h_.particleId.vertexPrimary) in self.count_vp for h_ in hl1], bool)
            mh = m2h[m2h >= 0]
            nsm = int(inj[mh].sum())
            # injected deposits survive digitisation unchanged (depositedEnergy = E_before - E_after)
            self.store[ctx.eventNumber]['n_sig_meas_all'] = nsm
            self.store[ctx.eventNumber]['ckf_sig'] = int(np.sum(used[m2h >= 0] & inj[mh])) if self.with_ckf else 0
            self.store[ctx.eventNumber]['inj_dE'] = np.array([h_.depositedEnergy / u.GeV for h_, f in zip(hl1, inj) if f])
        if self.store_vp is not None:     # C'0: the toy's SimHits on ALL surfaces (inserted into C'_PU events, §4.2)
            sh = []
            for h_ in hits:
                b = h_.particleId
                if int(b.vertexPrimary) in self.store_vp:
                    fp = h_.fourPosition; b4 = h_.momentum4Before; a4 = h_.momentum4After
                    sh.append((G['geo_sid'].get(h_.geometryId.value, -1), fp[0], fp[1], fp[2], fp[3] / u.ns,
                               b4[0], b4[1], b4[2], b4[3], a4[0], a4[1], a4[2], a4[3], int(b.vertexPrimary),
                               int(b.vertexSecondary), int(b.particle), int(b.generation), int(b.subParticle)))
            self.store[ctx.eventNumber]['toy_simhits'] = np.array(sh, float).reshape(-1, 18)
        # written measurements: barrel counting + BTL
        rows = []; tru = []; nunm = 0; mom = []
        geo_sid = G['geo_sid']; wsid = G['write_sid']
        hl = list(hits)
        for mi, mm in enumerate(meas):
            gv = mm.geometryId.value
            sid = geo_sid.get(gv, -1)
            if sid < 0:
                nunm += 1
                continue
            if sid not in wsid:
                continue
            par = _call(mm.fullParameters); idx = [int(k) for k in _call(mm.subspaceIndices)]
            l0 = par[0] if 0 in idx else 0.0
            l1 = par[1] if 1 in idx else 0.0
            fc = _call(mm.fullCovariance)
            hh = hl[m2h[mi]] if m2h[mi] >= 0 else None
            if hh is not None:
                b = hh.particleId; fp = hh.fourPosition
                trow = (int(b.vertexPrimary), int(b.particle), int(b.generation), int(b.vertexSecondary),
                        float(hh.depositedEnergy) / u.GeV, float(hh.time) / u.ns)
                tru.append((fp[0], fp[1], fp[2]))
                if self.with_mom:
                    b4 = hh.momentum4Before; a4 = hh.momentum4After
                    mom.append((b4[0], b4[1], b4[2], b4[3], a4[0], a4[1], a4[2], a4[3]))
            else:
                trow = (-1, -1, -1, -1, 0.0, 0.0); tru.append((np.nan, np.nan, np.nan))
                if self.with_mom:
                    mom.append((np.nan,) * 8)
            tm = par[5] / u.ns if 5 in idx else trow[5]
            rows.append((sid, l0, l1, math.sqrt(fc[0, 0]), math.sqrt(fc[1, 1]), float(used[mi])) + trow[:5] + (tm,))
        R = np.array(rows, float).reshape(-1, 12)
        ev = np.zeros((len(R), len(COLS)))
        if len(R):
            sid = R[:, 0].astype(np.int64)
            Rad = G['rad'][sid]; zc = G['zc'][sid]
            phi = R[:, 1] / Rad
            ev[:, 0] = sid; ev[:, 1] = Rad * np.cos(phi); ev[:, 2] = Rad * np.sin(phi); ev[:, 3] = R[:, 2] + zc
            ev[:, 4:] = R[:, 3:]
        T = np.array(tru, float).reshape(-1, 3)
        onsurf = float(np.max(np.abs(np.hypot(T[:, 0], T[:, 1]) - G['rad'][ev[:, 0].astype(np.int64)]))) * 1e3 \
            if len(T) else 0.0
        self.store[ctx.eventNumber].update(ev=ev, tru=T.astype(np.float32), nh=nh, nm=nm, nmap=nmap, bij=bij, nunm=nunm,
                                           lost=np.array(lost, float).reshape(-1, 8),
                                           mom=np.array(mom, float).reshape(-1, 8) if self.with_mom else None,
                                           onsurf=onsurf, ntr=ntr, nckf=int(used.sum()),
                                           t_dump=time.perf_counter() - t0)
        return acts.examples.ProcessCode.SUCCESS


class Inject(acts.examples.IAlgorithm):
    """Adds stored SimHits (Stage-3 quirk hits, plan §1.3; or stored C'0 toy hits, §4.2) to the Fatras SimHits.
    hits_of(event_number) -> list of (sid, vp, particle, x4 [mm, ns], p4_before [GeV], p4_after [GeV], index)."""

    def __init__(self, G, hits_of, store, with_input=True, in_key='simhits'):
        acts.examples.IAlgorithm.__init__(self, 'InjectStored', acts.logging.WARNING)
        self.G = G; self.hits_of = hits_of; self.store = store; self.with_input = with_input
        if with_input:
            self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize(in_key)
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_all')

    def execute(self, ctx):
        c = acts.examples.SimHitContainer()
        if self.with_input:
            for h in self.inp(ctx.eventStore):
                c.insert(h)
        geo_of = self.G['geo_of']; nphi = self.G['nphi']; tab = self.G['tab']
        n = 0
        for hh in self.hits_of(ctx.eventNumber):
            sid, vp, part, x4, pb, pa, k = hh[:7]
            bc = acts.fatras.Barcode(); bc.vertexPrimary = int(vp); bc.particle = int(part)
            if len(hh) > 7:          # stored C'0 toy hit: full barcode
                bc.vertexSecondary = int(hh[7]); bc.generation = int(hh[8]); bc.subParticle = int(hh[9])
            sec = 0 if tab[sid]['kind'] == 'BTL' else s4geo.sector(x4[0], x4[1], nphi)
            c.insert(acts.examples.SimHit(geo_of[(sid, sec)], bc,
                                          acts.Vector4(x4[0] * u.mm, x4[1] * u.mm, x4[2] * u.mm, x4[3] * u.ns),
                                          acts.Vector4(*(v * u.GeV for v in pb)), acts.Vector4(*(v * u.GeV for v in pa)),
                                          int(k)))
            n += 1
        self.store[ctx.eventNumber]['n_sig_simhits'] = n
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


class Truncate(acts.examples.IAlgorithm):
    """C' NI / DIF toys (plan §4.2): drop the parent's Fatras SimHits beyond its kink/NI radius.
    trunc_of(event) -> list of (vp, vsec, particle, r_cut [mm]).  Writes 'simhits_t'."""

    def __init__(self, trunc_of, store):
        acts.examples.IAlgorithm.__init__(self, 'TruncateParent', acts.logging.WARNING)
        self.trunc_of = trunc_of; self.store = store
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_t')

    def execute(self, ctx):
        cut = {(int(a), int(b), int(c)): float(r) for a, b, c, r in self.trunc_of(ctx.eventNumber)}
        c = acts.examples.SimHitContainer(); nd = 0
        for h in self.inp(ctx.eventStore):
            b = h.particleId
            key = (int(b.vertexPrimary), int(b.vertexSecondary), int(b.particle))
            if key in cut and int(b.generation) == 0:
                fp = h.fourPosition
                if math.hypot(fp[0], fp[1]) > cut[key]:
                    nd += 1
                    continue
            c.insert(h)
        self.store[ctx.eventNumber]['n_trunc_dropped'] = nd
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


def geometry(scratch, mat_scale=1.0, nphi=NPHI):
    tg, els, sid_of, geo_of, surfs, passive = s4geo.build(nphi=nphi, scratch=scratch, mat_scale=mat_scale)
    tab = {s['sid']: s for s in surfs}
    ns = max(tab) + 1
    rad = np.full(ns, np.nan); zc = np.zeros(ns)
    for s in surfs:
        if s['type'] == 0:
            rad[s['sid']] = s['p0'] * 10.0
            zc[s['sid']] = 0.0         # cylinder transform at z = 0.5 (z0 + z1): symmetric surfaces -> 0
            assert abs(s['p1'] + s['p2']) < 1e-9 or s['kind'] in ('T3V',), s['name']
    names = {s['name']: s['sid'] for s in surfs}
    write_sid = {names[n] for n in BARREL_COUNT} | {names['BTL']}
    digi = s4geo.write_digi(sid_of, surfs, Path(scratch) / 'digi.json')
    seed_sids = [s['sid'] for s in surfs if s['name'].startswith('TBPX') or s['name'].startswith('TFPX')]
    sel = [dict(volume=v) for v in sorted({geo_of[(k, 0)].volume for k in seed_sids})]
    gsel = Path(scratch) / 'geoSelection_IT.json'
    gsel.write_text(json.dumps(sel))
    return dict(tg=tg, els=els, sid_of=sid_of, geo_of=geo_of, surfs=surfs, tab=tab, rad=rad, zc=zc, nphi=nphi,
                geo_sid={g.value: s for g, s in sid_of.items()}, write_sid=write_sid, digi=digi, gsel=gsel,
                surf_by_geo={e.surface().geometryId: e.surface() for e in els})


def build_sequencer(G, n_events, rnd_seed, provider, store, inject=None, with_ckf=True, ckf_cut=10, two_way=True,
                    timing_dir=None, with_mom=False, count_vp=None, truncate=None, store_vp=None):
    field = acts.ConstantBField(acts.Vector3(0, 0, B0))
    rnd = acts.examples.RandomNumbers(seed=int(rnd_seed) % 2_000_000_000 + 1)
    kw = dict(outputDir=str(timing_dir)) if timing_dir else {}
    s = acts.examples.Sequencer(events=n_events, numThreads=1, logLevel=acts.logging.WARNING, failOnUnmaskedFpe=False,
                                **kw)
    s.addAlgorithm(Stamp('t0'))
    s.addAlgorithm(ParticleSource(provider, store))
    s.addAlgorithm(Stamp('t1_source'))
    s.addWhiteboardAlias('particles_selected', 'particles_input')      # read only by the ACTS truth matchers
    addFatras(s, G['tg'], field, rnd=rnd, pMin=0.03 * u.GeV, inputParticles='particles_input',
              logLevel=acts.logging.ERROR)
    if truncate is not None:
        s.addAlgorithm(truncate)
    if inject is not None:
        s.addAlgorithm(inject)
    else:
        s.addWhiteboardAlias('simhits_all', 'simhits_t' if truncate is not None else 'simhits')
    cfg = acts.examples.DigitizationAlgorithm.Config(
        digitizationConfigs=acts.examples.json.readDigiConfigFromJson(str(G['digi'])),
        surfaceByIdentifier=G['surf_by_geo'], randomNumbers=rnd, inputSimHits='simhits_all',
        outputMeasurements='measurements', doMerge=False,
        outputMeasurementParticlesMap='measurement_particles_map', outputMeasurementSimHitsMap='measurement_simhits_map',
        outputParticleMeasurementsMap='particle_measurements_map', outputSimHitMeasurementsMap='simhit_measurements_map')
    s.addAlgorithm(acts.examples.DigitizationAlgorithm(cfg, acts.logging.WARNING))
    s.addAlgorithm(Stamp('t2_digi'))
    if with_ckf:
        addSeeding(s, G['tg'], field,
                   SeedFinderConfigArg(r=(None, 200 * u.mm), deltaR=(1 * u.mm, 120 * u.mm),
                                       collisionRegion=(-200 * u.mm, 200 * u.mm), z=(-1500 * u.mm, 1500 * u.mm),
                                       maxSeedsPerSpM=1, sigmaScattering=5, radLengthPerSeed=0.1, minPt=900 * u.MeV,
                                       impactMax=3 * u.mm),
                   SeedFinderOptionsArg(bFieldInZ=B0, beamPos=(0.0, 0.0)),
                   seedingAlgorithm=SeedingAlgorithm.GridTriplet,
                   initialSigmas=[1 * u.mm, 1 * u.mm, 1 * u.degree, 1 * u.degree, 0 * u.e / u.GeV, 1 * u.ns],
                   initialSigmaQoverPt=0.1 * u.e / u.GeV, initialSigmaPtRel=0.1, initialVarInflation=[1.0] * 6,
                   geoSelectionConfigFile=G['gsel'], logLevel=acts.logging.WARNING)
        s.addAlgorithm(Stamp('t3_seed'))
        addCKFTracks(s, G['tg'], field,
                     TrackSelectorConfig(pt=(900 * u.MeV, None), absEta=(None, 4.0), loc0=(-4.0 * u.mm, 4.0 * u.mm),
                                         nMeasurementsMin=7, maxHoles=2, maxOutliers=2),
                     CkfConfig(chi2CutOffMeasurement=15.0, chi2CutOffOutlier=25.0, numMeasurementsCutOff=ckf_cut,
                               seedDeduplication=True, stayOnSeed=True), twoWay=two_way, logLevel=acts.logging.WARNING)
        s.addAlgorithm(Stamp('t4_ckf'))
    s.addAlgorithm(Dump(G, store, with_ckf=with_ckf, with_mom=with_mom, count_vp=count_vp, store_vp=store_vp))
    s.addAlgorithm(Stamp('t5_dump'))
    return s


def finish(out, store, n_events, meta, t_start):
    v41 = np.zeros((n_events, len(V41_COLS)))
    tim = np.zeros((n_events, len(T_COLS)))
    st = {}
    for e, nm, t in TIMES:
        st.setdefault(e, {})[nm] = t
    arrays = {}
    for i in range(n_events):
        r = store[i]
        ev = r['ev']
        vz = r['vz']
        # causality: every simhit written must satisfy t >= t_vtx(vp) + |x - v|/c (SimHit truth position)
        ncv = 0
        if len(ev) and len(vz):
            vp = ev[:, 7].astype(np.int64)
            lut = {int(v[0]): v for v in vz}
            m = np.array([x in lut for x in vp])
            if m.any():
                V = np.array([lut[x] for x in vp[m]])
                d = np.linalg.norm(r['tru'][m].astype(np.float64) - V[:, 1:4], axis=1)
                tt = ev[m, 12].copy()
                btl = (ev[m, 0] == ev[m, 0]) & np.isin(ev[m, 0].astype(np.int64), list(BTL_SIDS))
                tt = np.where(btl, np.nan, tt)          # BTL time column is the smeared time
                ncv = int(np.nansum(tt < V[:, 4] + d / s4pu.C_MM_PER_NS - 1e-6))
        sig = int(r.get('n_sig_meas_all', np.sum(ev[:, 7] == s4pu.SIG_VP) if len(ev) else 0))
        v41[i] = (r['nh'], r['nm'], r['nmap'], r['bij'], r['nunm'], len(ev), r['onsurf'], ncv, r.get('n_sig_simhits', 0),
                  sig, r['ntr'], r['nckf'], r['n_in'])
        s = st.get(i, {})
        t2 = s.get('t2_digi', 0.0); t3 = s.get('t3_seed', t2); t4 = s.get('t4_ckf', t3)
        tim[i] = (r['t_gen'], r['t_source'], t2 - s.get('t1_source', t2), t3 - t2, t4 - t3, r['t_dump'])
        arrays[f'ev{i}'] = ev
        arrays[f'tru{i}'] = r['tru']
        arrays[f'vz{i}'] = vz
        if len(r['lost']):
            arrays[f'lost{i}'] = r['lost']
        if r.get('toy_simhits') is not None:
            arrays[f'toy{i}'] = r['toy_simhits']
        if r.get('mom') is not None:
            arrays[f'mom{i}'] = r['mom'].astype(np.float32)
    meta.update(chain=CHAIN, columns=COLS, v41_cols=V41_COLS, timing_cols=T_COLS, n_events=n_events,
                t_total_s=round(time.time() - t_start, 3),
                v41_pass=bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                              and np.all(v41[:, 7] == 0)
                              and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0]))
                              and np.all(v41[:, 8] == v41[:, 9])),
                n_lost_simhits=int(np.sum(v41[:, 0] - v41[:, 1])),
                n_meas=[int(x) for x in v41[:, 1]], n_written=[int(x) for x in v41[:, 5]],
                mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(T_COLS)})
    out = Path(out)
    tmp = out.with_name(out.name + '.tmp.npz')
    np.savez(tmp, v41=v41, timing=tim, meta=np.array(json.dumps(meta, default=str)), **arrays)
    os.replace(tmp, out)
    return meta


BTL_SIDS = set()


NAV_ERR = 'insideBounds'          # G1b fix (HASH_ADDENDUM.md): ACTS GridPortalLink navigation assertion
MAX_REPLACE = 5


def _apply_replace(ev_seeds, a, meta, tag):
    """G1b fix: replace the generator seed of the events listed in --replace-event (deterministic new seed)."""
    rep = []
    for k in a.replace_event:
        old = int(ev_seeds[k])
        new = s4pu.hseed('nav-replace', tag, a.seed, k, old, mod=2 ** 62)
        ev_seeds[k] = new
        rep.append(dict(event=int(k), old_seed=old, new_seed=int(new),
                        reason="ACTS navigation assertion (GridPortalLink insideBounds) in this event's original run"))
    if rep:
        meta['replaced_events'] = rep
    return ev_seeds


def _failed_event(store, n):
    for i in range(n):
        if 'ev' not in store.get(i, {}):
            return i
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['pu', 'gun', 'sig', 'sm', 'cp', 'cppu'])
    ap.add_argument('--topo', default=None, help="cp: C' topology (s4cp.TOPOS)")
    ap.add_argument('--cp-file', default=None, help="cppu: C'0 chain output with stored toy SimHits")
    ap.add_argument('--cp-events', default=None, help="cppu: JSON list of C'0 event indices to overlay")
    ap.add_argument('--sample', default=None, help='sm: SM sample name (s4pu.SM_SAMPLES)')
    ap.add_argument('out')
    ap.add_argument('n_events', type=int)
    ap.add_argument('seed', type=int)
    ap.add_argument('--mu', type=float, default=200.0)
    ap.add_argument('--no-ckf', action='store_true')
    ap.add_argument('--ckf-cut', type=int, default=10)
    ap.add_argument('--one-way', action='store_true')
    ap.add_argument('--timing-dir', default=None)
    ap.add_argument('--nphi', type=int, default=NPHI)
    ap.add_argument('--mat-scale', type=float, default=1.0)
    ap.add_argument('--gun-pdg', type=int, default=13)
    ap.add_argument('--gun-mass', type=float, default=0.1056583755)
    ap.add_argument('--gun-pt', type=float, nargs=2, default=(1.0, 10.0))
    ap.add_argument('--gun-eta', type=float, nargs=2, default=(-2.5, 2.5))
    ap.add_argument('--gun-n', type=int, default=10)
    ap.add_argument('--gun-vertex', default='lum', choices=['lum', 'origin'])
    ap.add_argument('--gun-phi', default='uniform', choices=['uniform', 'boundary'])
    ap.add_argument('--with-mom', action='store_true')
    ap.add_argument('--event-seeds', default=None, help='JSON list of per-event PU seeds (row-major signal PU)')
    ap.add_argument('--point', default=None, help='sig: Stage-3 point key, e.g. p2/F_m1000/L1_BM')
    ap.add_argument('--rows', default=None, help='sig: JSON list of Stage-3 rows (one ACTS event per row)')
    ap.add_argument('--no-pu', action='store_true', help='sig: no PU (A1)')
    ap.add_argument('--replace-event', type=int, action='append', default=[],
                    help='G1b fix: replace this event\'s generator seed (set automatically after a navigation assertion)')
    a = ap.parse_args(argv)
    t_start = time.time()
    scratch = tempfile.mkdtemp(prefix='s4chain_')
    try:
        G = geometry(scratch, mat_scale=a.mat_scale, nphi=a.nphi)
        BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        t_geo = time.time() - t_start
        store = {}
        meta = dict(mode=a.mode, job_seed=a.seed, mu=a.mu, nphi=a.nphi, mat_scale=a.mat_scale, ckf=not a.no_ckf, ckf_cut=a.ckf_cut,
                    ckf_two_way=not a.one_way, t_geometry_s=round(t_geo, 2),
                    acts=str(acts.version) if hasattr(acts, 'version') else '48.0.0')
        if a.mode == 'pu':
            mb = s4pu.MinBias(CP5, s4pu.load_beamspot(TT), mu=a.mu, tt=TT)
            ev_seeds = [s4pu.hseed('pu', a.seed, i, mod=2 ** 62) for i in range(a.n_events)]
            if a.event_seeds:
                ev_seeds = [int(x) for x in json.loads(Path(a.event_seeds).read_text())]
                assert len(ev_seeds) == a.n_events
            _apply_replace(ev_seeds, a, meta, 'pu')
            meta['event_seeds'] = ev_seeds

            def provider(i):
                return mb.event(ev_seeds[i])
            s = build_sequencer(G, a.n_events, a.seed, provider, store, with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut,
                                two_way=not a.one_way, timing_dir=a.timing_dir)
        elif a.mode == 'sig':
            # A5 / A1 full chain: one ACTS event per physics row; quirk SimHits (T3V/ETL skipped, hit-time window and
            # hit efficiency applied before digitisation) injected with p4_after from the Fatras-model deposit
            import s4sig
            P = s4sig.Point(a.point)
            spin = a.point.split('/')[1].split('_')[0]
            rows = [int(x) for x in json.loads(Path(a.rows).read_text())]
            assert len(rows) == a.n_events
            slab = s4sig.slab_table(a.mat_scale)
            sig_info = {}

            def hits_of(i):
                h, ev = P.event(rows[i])
                d = s4sig.digitise(h, ev, P.m, spin, rows[i], P.lam, slab)       # V4-1 counters + the dE draws
                sid = h['h_surf'].astype(np.int64)
                kind = s4sig.KIND[sid]
                phys = ~np.isin(kind, ['T3V', 'ETL'])
                vt = ev['vtx']
                dd = np.sqrt((h['h_x'] - vt[0]) ** 2 + (h['h_y'] - vt[1]) ** 2 + (h['h_z'] - vt[2]) ** 2)
                late = h['h_t'] - vt[3] - dd / s4pu.C_MM_PER_NS > s4sig.T_ACC_NS
                ue = np.random.default_rng(s4sig.hseed('sig-smear', spin, P.m, rows[i]))
                ue.normal(0.0, 1.0, (len(sid), 3)); ue = ue.random(len(sid))      # same draws as s4sig.digitise
                keep = phys & ~late & (ue < s4sig.EFF)
                out = []
                dE = d['dE_all']
                for j in np.where(keep)[0]:
                    E = float(h['h_E'][j]); px, py, pz = float(h['h_px'][j]), float(h['h_py'][j]), float(h['h_pz'][j])
                    pp = math.sqrt(px * px + py * py + pz * pz)
                    Ea = E - float(dE[j]); f = math.sqrt(max(Ea * Ea - P.m * P.m, 0.0)) / pp
                    out.append((int(sid[j]), s4pu.SIG_VP, 1 + int(h['h_quirk'][j]),
                                (float(h['h_x'][j]), float(h['h_y'][j]), float(h['h_z'][j]), float(h['h_t'][j])),
                                (px, py, pz, E), (px * f, py * f, pz * f, Ea), int(j)))
                sig_info[i] = dict(row=rows[i], n_inj=len(out), v41_numpy=d['v41'],
                                   dE_inj=np.array([float(dE[j]) for j in np.where(keep)[0]]))
                return out
            if a.no_pu:
                def provider(i):
                    return np.zeros((0, len(s4pu.PCOLS))), np.zeros((0, 8)), dict(n_int=0)
            else:
                mb = s4pu.MinBias(CP5, s4pu.load_beamspot(TT), mu=a.mu, tt=TT)
                ev_seeds = [s4pu.hseed('sigpu', spin, P.m, r, mod=2 ** 62) for r in rows]
                _apply_replace(ev_seeds, a, meta, 'sig')

                def provider(i):
                    return mb.event(ev_seeds[i])
            meta.update(point=a.point, rows=rows, no_pu=a.no_pu)
            s = build_sequencer(G, a.n_events, a.seed, provider, store, inject=Inject(G, hits_of, store),
                                with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut, two_way=not a.one_way,
                                count_vp={s4pu.SIG_VP})
        elif a.mode == 'sm':
            # SM hard scatter (vp = 3000, truth MET > 200 GeV) + PU 200 (plan §4.2, block C)
            sm = s4pu.SMEvent(CP5, s4pu.load_beamspot(TT), a.sample, mu=a.mu, tt=TT)
            ev_seeds = [s4pu.hseed('sm', a.sample, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]
            _apply_replace(ev_seeds, a, meta, 'sm')
            meta.update(sample=a.sample, event_seeds=ev_seeds)

            def provider(i):
                return sm.event(ev_seeds[i])
            s = build_sequencer(G, a.n_events, a.seed, provider, store, with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut,
                                two_way=not a.one_way, timing_dir=a.timing_dir)
        elif a.mode == 'cp':
            # C'0: topology gun/toy without PU (plan §4.2); the toy SimHits are stored for the C'_PU insertion
            import s4cp
            bs = s4pu.load_beamspot(TT)
            mbg = None
            if a.topo == 'pvpair':
                lines, mv = s4pu.mpi_init_lines(TT)
                mbg = s4pu.PythiaGen(CP5, extra_lines=lines)
            cp = s4cp.CPrime(bs, minbias=mbg)
            ev_seeds = [s4pu.hseed('cp0', a.topo, a.seed, i, mod=2 ** 62) for i in range(a.n_events)]
            _apply_replace(ev_seeds, a, meta, 'cp0')
            meta.update(topo=a.topo, event_seeds=ev_seeds, toy_cols=TOY_COLS)

            def provider(i):
                return cp.event(a.topo, ev_seeds[i])
            trunc = Truncate(lambda i: store[i]['info']['trunc'], store) if a.topo.startswith('ni') or a.topo == 'dif' \
                else None
            s = build_sequencer(G, a.n_events, a.seed, provider, store, with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut,
                                two_way=not a.one_way, timing_dir=a.timing_dir, truncate=trunc,
                                store_vp={s4pu.GUN_VP})
        elif a.mode == 'cppu':
            # C'_PU: a TDR PU-200 event + the STORED C'0 toy SimHits inserted (not re-simulated), same PV and road
            zc = np.load(a.cp_file)
            mc = json.loads(str(zc['meta']))
            evs = [int(x) for x in json.loads(Path(a.cp_events).read_text())]
            assert len(evs) == a.n_events
            toys = [zc[f'toy{e}'] for e in evs]
            infos = [mc['ev_info'][e] for e in evs]
            mb = s4pu.MinBias(CP5, s4pu.load_beamspot(TT), mu=a.mu, tt=TT)
            ev_seeds = [s4pu.hseed('cppu', mc['topo'], mc['job_seed'], e, a.seed, mod=2 ** 62) for e in evs]
            _apply_replace(ev_seeds, a, meta, 'cppu')
            meta.update(topo=mc['topo'], cp_file=str(a.cp_file), cp_job_seed=mc['job_seed'], cp_events=evs,
                        event_seeds=ev_seeds, toy_info=infos)

            def provider(i):
                return mb.event(ev_seeds[i])

            def hits_of(i):
                T = toys[i]
                return [(int(r[0]), int(r[13]), int(r[15]), (r[1], r[2], r[3], r[4]), (r[5], r[6], r[7], r[8]),
                         (r[9], r[10], r[11], r[12]), k, int(r[14]), int(r[16]), int(r[17])) for k, r in enumerate(T)]
            s = build_sequencer(G, a.n_events, a.seed, provider, store, inject=Inject(G, hits_of, store),
                                with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut, two_way=not a.one_way,
                                count_vp={s4pu.GUN_VP})
        elif a.mode == 'gun':
            bs = s4pu.load_beamspot(TT)
            ev_seeds = [s4pu.hseed('gun', a.seed, i, mod=2 ** 62) for i in range(a.n_events)]
            meta.update(event_seeds=ev_seeds, gun=dict(pdg=a.gun_pdg, mass=a.gun_mass, pt=a.gun_pt, eta=a.gun_eta,
                                                       n=a.gun_n, vertex=a.gun_vertex, phi=a.gun_phi))

            def provider(i):
                return s4pu.gun_event(ev_seeds[i], pdg=a.gun_pdg, mass=a.gun_mass, pt_range=a.gun_pt,
                                      eta_range=a.gun_eta, n=a.gun_n, beamspot=bs, vertex=a.gun_vertex,
                                      phi_mode=a.gun_phi, nphi=max(a.nphi, 32))
            s = build_sequencer(G, a.n_events, a.seed, provider, store, with_ckf=not a.no_ckf, ckf_cut=a.ckf_cut,
                                two_way=not a.one_way, timing_dir=a.timing_dir, with_mom=a.with_mom)
        try:
            s.run()
        except RuntimeError as exc:          # G1b fix (HASH_ADDENDUM.md): rerun with the failing event replaced
            k = _failed_event(store, a.n_events)
            if (NAV_ERR not in str(exc) or k is None or k in a.replace_event or len(a.replace_event) >= MAX_REPLACE
                    or a.mode == 'gun'):
                raise
            print(f'[run_chain] navigation assertion in event {k}; rerunning the job with that event replaced',
                  file=sys.stderr, flush=True)
            TIMES.clear()
            return main(list(sys.argv[1:] if argv is None else argv) + ['--replace-event', str(k)])
        if a.mode == 'sig':
            for i, r in sig_info.items():
                st = store[i]
                same = bool(np.allclose(np.sort(st.get('inj_dE', np.zeros(0))), np.sort(r['dE_inj']), rtol=1e-6, atol=1e-12))
                r.update(n_meas_all=st.get('n_sig_meas_all', -1), ckf_sig=st.get('ckf_sig', 0), dE_equal=same)
                r.pop('dE_inj', None)
            meta['sig_v41'] = [sig_info[i] for i in range(a.n_events)]
            meta['sig_v41_pass'] = bool(all(r['n_meas_all'] == r['n_inj'] and r['dE_equal'] and r['v41_numpy']['pass']
                                            for r in sig_info.values()))
        meta['ev_info'] = [{k: v for k, v in store[i]['info'].items()} for i in range(a.n_events)]
        meta = finish(a.out, store, a.n_events, meta, t_start)
        print(json.dumps({k: meta[k] for k in ('chain', 'n_events', 't_total_s', 'v41_pass', 'mean_s_per_event',
                                               'n_meas', 'n_written', 't_geometry_s')}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
