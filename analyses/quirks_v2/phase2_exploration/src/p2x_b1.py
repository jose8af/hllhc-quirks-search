"""p2x_b1.py -- pilot no-pile-up single-interaction events for a CLASS LIST (addendum 1 v2), one Geant4 vertex each.

  <acts python> p2x_b1.py <sample> <classes: a+b+...> <out.npz> <n_events> <stream> <chunk> <first> <beta_min> <vertex file> \
                          [trunc: radius|time|both|auto|hybrid|autoh = radius] [n_road_orientations = 21]

  sample    name of the pilot sample (dif, difc, ni22, ni30, ni61, nix, nic, hs, lowpt); only a label and a seed tag
  classes   classes of p2x_common.B1_CLASSES that form the sample (DIF sample of addendum v2 = dif+k0l)
  first     the events are the vertices [first, first + n_events) of those classes in ONE group file of p2x_g4prod.py,
            in file (= firing) order; the job fails if the file holds fewer (never a silent short sample)
  beta_min  hand-over cut of addendum v2 P6 (0.1): products slower than this at the slab exit are not given to Fatras

  trunc     how the Fatras parent is cut at the Geant4 vertex (review of addendum v2, finding A-1):
            auto    time for the classes difc and nic (after a turn), radius for the first-arc classes
            radius  v1's run_chain.Truncate: parent SimHits at r > r_vertex dropped (wrong for a parent that has turned:
                    its earlier hits at larger radius are dropped too)
            time    parent SimHits LATER than the Geant4 vertex time dropped (class TruncateParent below)
            both    dropped if later than the vertex time OR beyond the vertex radius
            hybrid  time cut, and the stored Geant4 crossings of the parent later than its last kept Fatras hit are
                    added as SimHits (class HybridParent; option (a) of outputs/HALF_TURN_*.md: Fatras makes no hit
                    beyond half a turn).  autoh = hybrid for difc and nic, radius for the first-arc classes

Chain and hand-over as Tatiana's p2c_b1.py / p2c_handover.py (imported, not modified): Fatras parent, truncated as
chosen (variant A), Geant4 products from the slab exit, run_chain.build_sequencer unchanged with CKF, SimHits of the
event stored on every surface.  The Geant4 crossings of the parent before the vertex are stored (variant B input).

Per event (`evt`, columns EVT_COLS): everything of p2c_b1.EVT_COLS, plus the vertex class, the parent kinematics at
its origin (pdg, pT, eta, phi), the road offset, the vertex radius / z / time / volume, first-arc flag, parent
momentum at the vertex, pool provenance and source weight.  The last two columns are the event seed.
Road: N_t of addendum v2 counts parents inside a road of half-width 0.15.  `road_dphi` = phi(parent at origin) -
phi(road axis): the true offset for a hard-scatter pool (from the pool file), else a draw U(-0.15, 0.15) seeded per
event; `phi_road` = phi(parent) - road_dphi.  The number of road orientations to be tested per event in Phase 3
(21 = 2 pi / 0.30 non-overlapping roads, axes phi_road + 2 pi k / 21) is recorded in meta['road_orientations'].  `phimet` is Tatiana's independent uniform draw (kept).  Nothing is cut
on either; Phase 3 chooses the convention.
"""
import json
import math
import shutil
import sys
import tempfile
import time

import numpy as np

import p2c_common as C
import p2c_b1 as B1
import p2c_handover as HO
import p2x_common as X

rc = B1.rc
s4pu = B1.s4pu

acts = rc.acts
u = rc.u
log = C.setup_logging('p2x_b1')
TRUNC_MODES = ('radius', 'time', 'both')
AFTER_TURN = ('difc', 'nic')          # 'auto': time for these classes, radius (v1) for the first-arc classes


class TruncateParent(acts.examples.IAlgorithm):
    """run_chain.Truncate (l.266-290) with a time criterion.  trunc_of(event) -> list of (vp, vsec, particle, r_cut [mm],
    t_cut [ns], mode); generation-0 SimHits of that particle are dropped if (mode radius) r > r_cut, (mode time) t > t_cut,
    (mode both) either; the mode is given per event (so 'auto' can depend on the vertex class).  Reads 'simhits', writes 'simhits_t', stores n_trunc_dropped (as run_chain.Truncate)."""

    def __init__(self, trunc_of, store, mode):
        acts.examples.IAlgorithm.__init__(self, 'TruncateParentX', acts.logging.WARNING)
        self.trunc_of = trunc_of; self.store = store; self.mode = mode
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_t')

    def execute(self, ctx):
        cut = {(int(a), int(b), int(c)): (float(r), float(t), m) for a, b, c, r, t, m in self.trunc_of(ctx.eventNumber)}
        c = acts.examples.SimHitContainer(); nd = 0
        for h in self.inp(ctx.eventStore):
            b = h.particleId
            key = (int(b.vertexPrimary), int(b.vertexSecondary), int(b.particle))
            if key in cut and int(b.generation) == 0:
                fp = h.fourPosition
                far = math.hypot(fp[0], fp[1]) > cut[key][0]
                late = fp[3] / u.ns > cut[key][1]
                mode = cut[key][2]
                if (mode == 'radius' and far) or (mode == 'time' and late) or (mode == 'both' and (far or late)):
                    nd += 1
                    continue
            c.insert(h)
        self.store[ctx.eventNumber]['n_trunc_dropped'] = nd
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS
NEW_COLS = ['cls', 'parent_pdg', 'parent_pt0', 'parent_eta0', 'parent_phi0', 'road_dphi', 'phi_road', 'vtx_r', 'vtx_z',
            'vtx_t', 'vtx_vol', 'first_arc', 'parent_p_vtx', 'fire', 'pool_file', 'pool_row', 'src_index', 'w_src']
EVT_COLS = B1.EVT_COLS[:-2] + NEW_COLS + B1.EVT_COLS[-2:]
W_ROAD = 0.15


class HybridParent(acts.examples.IAlgorithm):
    """Option (a) of outputs/HALF_TURN_*.md for parents that have turned: Fatras leaves no hit beyond half a turn, so
    the Fatras parent is kept up to the Geant4 vertex time (as TruncateParent, mode time) and the stored Geant4
    crossings of the parent that are LATER than its last kept Fatras hit (+ T_EPS) are added as SimHits (as
    run_chain.Inject does for stored hits: same geometry ids, barcode of the parent, generation 0).  Events whose mode
    is 'radius' get v1's radius cut and no injection.  Reads 'simhits', writes 'simhits_all' (given to build_sequencer
    as `inject`).  what_of(event) -> (vp, vsec, particle, r_cut, t_cut, mode, mass, crossings (k, 8) cross_cols with
    the surface as a chain sid), or None for an event without a charged parent."""
    T_EPS = 0.005          # ns: a Geant4 crossing within 1.5 mm of flight of the last Fatras hit is taken as the same crossing

    def __init__(self, G, what_of, store):
        acts.examples.IAlgorithm.__init__(self, 'HybridParent', acts.logging.WARNING)
        self.G = G; self.what_of = what_of; self.store = store
        self.inp = acts.examples.ReadDataHandle(self, acts.examples.SimHitContainer, 'in'); self.inp.initialize('simhits')
        self.out = acts.examples.WriteDataHandle(self, acts.examples.SimHitContainer, 'out'); self.out.initialize('simhits_all')

    def execute(self, ctx):
        w = self.what_of(ctx.eventNumber)
        c = acts.examples.SimHitContainer(); nd = 0; ninj = 0; t_last = -1e30
        key = None if w is None else (int(w[0]), int(w[1]), int(w[2]))
        for h in self.inp(ctx.eventStore):
            b = h.particleId
            if key is not None and (int(b.vertexPrimary), int(b.vertexSecondary), int(b.particle)) == key and int(b.generation) == 0:
                fp = h.fourPosition
                t = fp[3] / u.ns
                if (w[5] == 'radius' and math.hypot(fp[0], fp[1]) > w[3]) or (w[5] != 'radius' and t > w[4]):
                    nd += 1
                    continue
                t_last = max(t_last, t)
            c.insert(h)
        if w is not None and w[5] != 'radius':
            geo_of = self.G['geo_of']; nphi = self.G['nphi']; tab = self.G['tab']
            for k, x in enumerate(w[7]):
                if x[4] <= t_last + self.T_EPS or x[4] > w[4]:
                    continue
                sid = int(x[0])
                en = math.sqrt(x[5] ** 2 + x[6] ** 2 + x[7] ** 2 + w[6] ** 2)
                bc = acts.fatras.Barcode(); bc.vertexPrimary = key[0]; bc.vertexSecondary = key[1]; bc.particle = key[2]
                sec = 0 if tab[sid]['kind'] == 'BTL' else rc.s4geo.sector(x[1], x[2], nphi)
                p4 = acts.Vector4(x[5] * u.GeV, x[6] * u.GeV, x[7] * u.GeV, en * u.GeV)
                c.insert(acts.examples.SimHit(geo_of[(sid, sec)], bc, acts.Vector4(x[1] * u.mm, x[2] * u.mm, x[3] * u.mm, x[4] * u.ns),
                                              p4, p4, 100000 + k))
                ninj += 1
        self.store[ctx.eventNumber]['n_trunc_dropped'] = nd
        self.store[ctx.eventNumber]['n_parent_injected'] = ninj
        self.out(ctx, c)
        return acts.examples.ProcessCode.SUCCESS


def load(vfile, classes, first, n):
    z, meta = C.load_job(vfile)
    assert meta.get('mode') == 'g4prod', f'{vfile} is not a p2x_g4prod vertex file'
    missing = [c for c in classes if c not in meta['complete_classes'] or c not in meta['group_classes']]
    assert not missing, f'classes {missing} are not (completely) in {vfile}'
    cls = z['cls']
    idx = np.nonzero(np.isin(cls, [X.CODE[c] for c in classes]))[0]
    if len(idx) < first + n:
        raise RuntimeError(f'{vfile}: {len(idx)} vertices of {classes}, need [{first}, {first + n})')
    take = idx[first:first + n]
    po = z['prod_off']; xo = z['cross_off']; prod = z['prod']; cross = z['cross']; vtx = z['vtx']; src = z['src']
    V = [vtx[i] for i in take]; PR = [prod[po[i]:po[i + 1]] for i in take]; CR = [cross[xo[i]:xo[i + 1]] for i in take]
    return V, PR, CR, cls[take], src[take], meta


def run(sample, classes, out, n_events, stream, chunk, first, beta_min, vfile, trunc_mode='radius', n_orient=21):
    t_start = time.time()
    HO.BETA_MIN = float(beta_min)
    job_seed = C.qv2_seed(stream, chunk)
    V, PR, CR, cls, src, vmeta = load(vfile, classes, first, n_events)
    assert np.all(np.isin(cls, [X.CODE[c] for c in classes])) and len(cls) == n_events
    vcols = vmeta['vcols']; scol = {k: i for i, k in enumerate(vmeta['src_cols'])}
    ev_seeds = [s4pu.hseed('p2x-b1', sample, job_seed, i, mod=2 ** 62) for i in range(n_events)]
    dec = HO.Decayer(job_seed)
    bs = s4pu.load_beamspot(rc.TT)
    sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm']])
    scratch = tempfile.mkdtemp(prefix='p2x_b1_', dir='.')
    try:
        G = rc.geometry(scratch)
        rc.BTL_SIDS.update(s['sid'] for s in G['surfs'] if s['kind'] == 'BTL')
        store = {}; aux = {}
        rc.TIMES.clear()
        assert trunc_mode in TRUNC_MODES + ('auto', 'hybrid', 'autoh')
        after = [X.CODE[c] for c in AFTER_TURN]
        hyb = trunc_mode in ('hybrid', 'autoh')
        ev_mode = [('time' if cls[i] in after else 'radius') if trunc_mode in ('auto', 'autoh') else
                   ('time' if trunc_mode == 'hybrid' else trunc_mode) for i in range(n_events)]
        sid_of_name = {s_['name']: s_['sid'] for s_ in G['surfs']}
        code_sid = {int(c): sid_of_name.get(nm, -1) for nm, c in vmeta['vol_names'].items()}

        def what_of(i):
            tl = store[i]['info']['trunc']
            if not tl:
                return None
            t = tl[0]
            g = dict(zip(vcols, V[i]))
            cr = np.array(CR[i], float).reshape(-1, 8)
            sid = np.array([code_sid.get(int(c), -1) for c in cr[:, 0]])
            cr = np.c_[sid, cr[:, 1:]][sid >= 0]
            return (t[0], t[1], t[2], t[3], t[4], t[5], HO.MASS.get(abs(int(g['parent_pdg'])), 0.13957039), cr)

        def provider(i):
            P, trunc, npg, ninj, nslow = HO.event_rows(V[i], PR[i], vcols, dec, ev_seeds[i])
            rng = np.random.default_rng(s4pu.hseed('p2x-b1-pv', sample, ev_seeds[i], mod=2 ** 63))
            pv = rng.normal(0, 1, 3) * sig
            phimet = rng.uniform(-np.pi, np.pi)
            droad = rng.uniform(-W_ROAD, W_ROAD)
            g = dict(zip(vcols, V[i]))
            vz = np.array([[s4pu.GUN_VP, g['x0'], g['y0'], g['z0'], g['t0'], g['px0'], g['py0'], g['pz0']]])
            aux[i] = (P, pv, phimet, npg, ninj, len(trunc), nslow, droad)
            return P, vz, dict(trunc=[(*t, g['t'], ev_mode[i]) for t in trunc], n_particles=len(P))
        if hyb:                             # option (a): time cut + Geant4 crossings beyond the Fatras parent's last hit
            s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True, inject=HybridParent(G, what_of, store),
                                   store_vp={s4pu.GUN_VP})
        else:
            if trunc_mode == 'radius':          # v1's own class, unchanged code path
                trunc = rc.Truncate(lambda i: [t[:4] for t in store[i]['info']['trunc']], store)
            else:
                trunc = TruncateParent(lambda i: store[i]['info']['trunc'], store, trunc_mode)
            s = rc.build_sequencer(G, n_events, job_seed, provider, store, with_ckf=True, truncate=trunc,
                                   store_vp={s4pu.GUN_VP})
        s.run()
        v41 = np.zeros((n_events, len(rc.V41_COLS))); tim = np.zeros((n_events, len(rc.T_COLS)))
        st = {}
        for e, nm, t in rc.TIMES:
            st.setdefault(e, {})[nm] = t
        evt = np.zeros((n_events, len(EVT_COLS)))
        hits = []; tru = []; vzs = []; toys = []; inj = []
        for i in range(n_events):
            r = store[i]; ev = r['ev']
            v41[i] = (r['nh'], r['nm'], r['nmap'], r['bij'], r['nunm'], len(ev), r['onsurf'], 0, 0, 0, r['ntr'],
                      r['nckf'], r['n_in'])
            x = st.get(i, {})
            t2 = x.get('t2_digi', 0.0); t3 = x.get('t3_seed', t2); t4 = x.get('t4_ckf', t3)
            tim[i] = (r['t_gen'], r['t_source'], t2 - x.get('t1_source', t2), t3 - t2, t4 - t3, r['t_dump'])
            P, pv, phimet, npg, ninj, ntr, nslow, droad = aux[i]
            g = dict(zip(vcols, V[i]))
            pt0 = float(np.hypot(g['px0'], g['py0'])); phi0 = float(np.arctan2(g['py0'], g['px0']))
            eta0 = float(np.arcsinh(g['pz0'] / max(pt0, 1e-300)))
            sd = float(src[i, scol['road_dphi']])
            rd = sd if np.isfinite(sd) else droad
            phi_road = (phi0 - rd + np.pi) % (2 * np.pi) - np.pi
            evt[i] = (first + i, *pv, phimet, npg, ninj, r.get('n_trunc_dropped', 0), ntr, nslow,
                      cls[i], g['parent_pdg'], pt0, eta0, phi0, rd, phi_road, float(np.hypot(g['x'], g['y'])), g['z'], g['t'],
                      g['vol'], src[i, scol['first_arc']], float(np.sqrt(g['px'] ** 2 + g['py'] ** 2 + g['pz'] ** 2)), g['fire'],
                      src[i, scol['pool_file']], src[i, scol['pool_row']], src[i, scol['src_index']], src[i, scol['w_src']],
                      ev_seeds[i] % 2 ** 31, ev_seeds[i] // 2 ** 31)
            hits.append(ev); tru.append(r['tru']); vzs.append(r['vz']); toys.append(r['toy_simhits']); inj.append(P)
        H, hoff = C.concat(hits, len(rc.COLS), np.float32)
        T, _ = C.concat(tru, 3, np.float32)
        VZ, voff = C.concat(vzs, 8, np.float64)
        TOY, toff = C.concat(toys, len(rc.TOY_COLS), np.float64)
        INJ, ioff = C.concat(inj, 12, np.float64)
        GP, gpoff = C.concat(PR, 9, np.float64)
        GC, gcoff = C.concat(CR, 8, np.float32)
        v41_pass = bool(np.all(v41[:, 3] == 1) and np.all(v41[:, 4] == 0) and np.all(v41[:, 6] < 1.0)
                        and np.all(v41[:, 0] - v41[:, 1] <= np.maximum(2, 1e-5 * v41[:, 0])))
        ccol = EVT_COLS.index('cls')
        n_cls = {c: int((evt[:, ccol] == X.CODE[c]).sum()) for c in classes}
        assert sum(n_cls.values()) == n_events, 'an event outside the classes of its sample'
        vsum = {k: vmeta.get(k) for k in ('stream', 'chunk', 'job_seed', 'g4_pass', 'n_fire', 'group', 'group_classes',
                                          'content_sha256', 'pool_prefix', 'pool_files', 'physlist', 'product_handover')}
        meta = dict(mode='b1x', term=sample, sample=sample, classes=classes, class_codes=X.CODE, n_per_class=n_cls,
                    stream=stream, chunk=chunk, job_seed=job_seed, n_events=n_events, first_vertex=first,
                    vertex_file=str(vfile), vertex_file_sha256=C.sha256_file(vfile), vertex_file_meta=vsum,
                    beta_min=float(beta_min), trunc_mode=trunc_mode,
                    handover=f'A (Fatras parent, truncated at the vertex by {trunc_mode}); products from the slab exit; beta < {HO.BETA_MIN} not handed over; '
                             'Geant4 parent crossings stored (variant B input)',
                    chain=rc.CHAIN, columns=rc.COLS, v41_cols=rc.V41_COLS, timing_cols=rc.T_COLS, evt_cols=EVT_COLS,
                    vcols=vcols, toy_cols=rc.TOY_COLS, pcols=s4pu.PCOLS, surface_names=vmeta['vol_names'],
                    proc_names=vmeta['proc_names'], road_half_width=W_ROAD,
                    road_orientations=dict(n=int(n_orient), axis_k='phi_road + 2 pi k / n, k = 0 .. n-1',
                                           note='review of addendum v2, B-1: if adopted, the own-hit count of a sample is the number of '
                                                '(event, orientation) passes; a recorded parameter, nothing is simulated per orientation'),
                    prod_cols=['pdg', 'px', 'py', 'pz', 'E', 'x', 'y', 'z', 't'],
                    cross_cols=['surface', 'x', 'y', 'z', 't', 'px', 'py', 'pz'], v41_pass=v41_pass,
                    n_lost_simhits=int(np.sum(v41[:, 0] - v41[:, 1])),
                    code_sha256=dict(C.code_hashes(), **X.src_hashes('p2x_b1.py', 'p2x_common.py', 'p2c_b1.py', 'p2c_common.py',
                                                                     'p2c_handover.py', 'p2c_g4vtx.py')),
                    input_sha256=X.input_hashes(),
                    t_total_s=round(time.time() - t_start, 3),
                    mean_s_per_event={c: float(tim[:, k].mean()) for k, c in enumerate(rc.T_COLS)},
                    n_hits=int(len(H)), n_simhits=int(len(TOY)), n_ckf_tracks=int(v41[:, 10].sum()),
                    mean_injected=float(evt[:, 6].mean()), mean_trunc_dropped=float(evt[:, 7].mean()),
                    mean_injected_slow=float(evt[:, 9].mean()),
                    mean_parent_hits_injected_from_geant4=float(np.mean([store[i].get('n_parent_injected', 0) for i in range(n_events)])))
        arrays = dict(hits=H, hit_off=hoff, tru=T, vz=VZ, vz_off=voff, v41=v41, timing=tim, evt=evt,
                      gvtx=np.array(V, float).reshape(-1, len(vcols)), gprod=GP, gprod_off=gpoff, gcross=GC, gcross_off=gcoff,
                      inj=INJ, inj_off=ioff, toy=TOY, toy_off=toff)
        X.save(out, arrays, meta)
        X.write_sha(str(out) + '.sha.json', dict(job=dict(sample=sample, stream=stream, chunk=chunk, job_seed=job_seed,
                                                          first=first, n_events=n_events),
                                                 files={str(out).rsplit('/', 1)[-1]: meta['content_sha256']}))
        log.info(json.dumps({k: meta[k] for k in ('sample', 'n_events', 'n_per_class', 't_total_s', 'v41_pass', 'mean_s_per_event',
                                                  'n_hits', 'n_simhits', 'mean_injected', 'mean_injected_slow',
                                                  'mean_trunc_dropped', 'bytes', 'content_sha256')}))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1].split('+'), a[2], int(a[3]), a[4], int(a[5]), int(a[6]), float(a[7]), a[8], a[9] if len(a) > 9 else 'radius',
        int(a[10]) if len(a) > 10 else 21)
