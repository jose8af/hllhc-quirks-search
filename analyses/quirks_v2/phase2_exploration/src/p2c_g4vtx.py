"""p2c_g4vtx.py -- Geant4 vertices of primaries drawn from the minimum-bias pool (STR §4.4 pt 1, 2, 5).

  <acts python> p2c_g4vtx.py time <out.npz> <n_int> <n_fire_dif> <n_fire_ni> <stream> <chunk> [physlist] [vertex|exit]
  <acts python> p2c_g4vtx.py scan <out.npz> <n_per_eta>

A "firing" is one pool primary sent through Geant4 from a luminous-region vertex with a uniform azimuth (the detector
model is axially symmetric; the road is assigned afterwards, plan O8).  The pool is re-used with new Geant4 random
numbers; a firing is unbiased in the primary kinematics and in the interaction.
Passes: 'dif' fires pi+- and K+- through the whole tracker (r < 1200 mm); 'ni' fires every pool species and drops
the primary beyond r = 70 mm (beam pipe, TBPX L1, TBPX L2 are the three NI radii of the strategy).
Vertex record (arrays): vtx (n, len(VCOLS)), prod (m, 5) with prod_off, cross (k, 8) with cross_off; names in meta.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

import p2c_common as C

log = C.setup_logging('p2c_g4vtx')
G4SH = str(C.HERE / 'g4' / 'g4hv.sh')
VCOLS = ['fire', 'pass', 'proc', 'vol', 'parent_pdg', 'x', 'y', 'z', 't', 'px', 'py', 'pz', 'nprod', 'ncross',
         'x0', 'y0', 'z0', 't0', 'px0', 'py0', 'pz0']
PASSES = {'dif': dict(species=(211, 321), rmax=1200.0), 'ni': dict(species=(211, 321, 2212, 130, 2112, 22), rmax=70.0),
          'all': dict(species=(211, 321, 2212, 130, 2112, 22), rmax=1200.0)}
MASS = {211: 0.13957039, 321: 0.493677, 2212: 0.93827209, 130: 0.497611, 2112: 0.93956542, 22: 0.0}     # s4cp.py l.33-34; n: PDG
B_T = 3.8112
CHUNK = 500_000


def geom_file(scale=1.0):
    sys.path.insert(0, str(C.HERE / 'g4'))
    import make_geom_g4
    f = Path(f'geom_g4_x{scale:g}.txt').resolve()
    make_geom_g4.main(f, scale)
    return f


def run_g4(args):
    r = subprocess.run([G4SH] + [str(a) for a in args], capture_output=True, text=True)
    line = [ln for ln in r.stdout.splitlines() if ln.startswith('G4HV ')]
    if r.returncode != 0 or not line:
        raise RuntimeError(f'g4hv failed ({r.returncode}): {r.stdout[-2000:]} {r.stderr[-2000:]}')
    kv = dict(x.split('=', 1) for x in line[0].split()[1:])
    return kv, r.stdout


class Names:
    def __init__(self):
        self.proc = {}; self.vol = {}

    def code(self, d, k):
        return d.setdefault(k, len(d))


def parse(path, names, fire0, ipass, prim):
    """prim: (n, 9) fired primaries of this chunk (pdg, x, y, z, t, px, py, pz, unused)."""
    V = []; P = []; X = []; np_ = []; nx = []
    with open(path) as f:
        for ln in f:
            c = ln[0]
            if c == 'V':
                w = ln.split()
                i = int(w[1])
                p0 = prim[i]
                V.append((fire0 + i, ipass, names.code(names.proc, w[2]), names.code(names.vol, w[3]), int(w[4]),
                          *map(float, w[5:12]), int(w[12]), int(w[13]), p0[1], p0[2], p0[3], p0[4], p0[5], p0[6], p0[7]))
                np_.append(0); nx.append(0)
            elif c == 'P':
                w = ln.split(); P.append(tuple(map(float, w[1:10]))); np_[-1] += 1
            elif c == 'X':
                w = ln.split(); X.append((names.code(names.vol, w[1]),) + tuple(map(float, w[2:9]))); nx[-1] += 1
    return V, P, X, np_, nx


def fire(pool, n_fire, pname, seed, geom, physlist, names, fire0=0, handover='vertex'):
    """Fire n_fire primaries of the pool rows allowed in this pass.  Returns record lists and the Geant4 CPU."""
    ps = PASSES[pname]
    sel = np.nonzero(np.isin(np.abs(pool['pdg']), ps['species']))[0]
    rng = np.random.default_rng(seed)
    bs = json.loads((C.QV2 / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())['beamspot']
    sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm'], bs['sigma_t_ps'] * 1e-3])
    out = dict(V=[], P=[], X=[], np=[], nx=[]); cpu = 0.0; init = 0.0; done = 0; counts = {}
    ipass = list(PASSES).index(pname)
    while done < n_fire:
        n = min(CHUNK, n_fire - done)
        idx = sel[rng.integers(0, len(sel), n)]
        phi = rng.uniform(-np.pi, np.pi, n)
        v = rng.normal(0.0, 1.0, (n, 4)) * sig
        pt = pool['pt'][idx].astype(float); eta = pool['eta'][idx].astype(float)
        prim = np.c_[pool['pdg'][idx], v, pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta), idx]
        fin = Path(f'prim_{pname}.txt'); fout = Path(f'vtx_{pname}.txt')
        with open(fin, 'w') as f:
            for i, r in enumerate(prim):
                f.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (i, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
        kv, _ = run_g4([geom, physlist, int(rng.integers(1, 2 ** 31 - 1)), fout, 'prim', fin, ps['rmax']]
                       + (['exit'] if handover == 'exit' else []))
        for k2 in ('nprod_exit', 'nprod_stopped_in_slab'):
            counts[k2] = counts.get(k2, 0) + int(kv.get(k2, 0))
        cpu += float(kv['event_cpu_s']); init += float(kv['init_cpu_s'])
        for k, x in kv.items():
            if '|' in k:
                counts[k] = counts.get(k, 0) + int(x)
        V, P, X, np_, nx = parse(fout, names, fire0 + done, ipass, prim)
        out['V'] += V; out['P'] += P; out['X'] += X; out['np'] += np_; out['nx'] += nx
        done += n
        fin.unlink(); fout.unlink()
    return out, dict(n_fire=n_fire, g4_event_cpu_s=cpu, g4_init_cpu_s=init, cpu_ms_per_firing=1e3 * cpu / max(n_fire, 1),
                     counts=counts)


def pack(recs):
    V = np.array(sum((r['V'] for r in recs), []), float).reshape(-1, len(VCOLS))
    P = np.array(sum((r['P'] for r in recs), []), np.float64).reshape(-1, 9)
    X = np.array(sum((r['X'] for r in recs), []), np.float32).reshape(-1, 8)
    npd = np.array(sum((r['np'] for r in recs), []), np.int64); nxd = np.array(sum((r['nx'] for r in recs), []), np.int64)
    poff = np.r_[0, np.cumsum(npd)]; xoff = np.r_[0, np.cumsum(nxd)]
    return dict(vtx=V, prod=P, prod_off=poff, cross=X, cross_off=xoff)


def first_arc(V):
    """True if the vertex lies on the parent's first outward arc: transverse path from the origin <= pi R, with the
    path from the vertex time and the initial momentum, R = pT / (0.29979e-3 B) mm.  Neutral parents: always True."""
    c = {k: i for i, k in enumerate(VCOLS)}
    ap = np.abs(V[:, c['parent_pdg']]).astype(np.int64)
    m = np.array([MASS.get(int(a), 0.13957039) for a in ap])
    pt = np.hypot(V[:, c['px0']], V[:, c['py0']]); p = np.sqrt(pt ** 2 + V[:, c['pz0']] ** 2)
    beta = p / np.hypot(p, m)
    st = beta * 299.792458 * (V[:, c['t']] - V[:, c['t0']]) * pt / np.maximum(p, 1e-12)
    rad = pt / (0.299792458e-3 * B_T)
    return np.isin(ap, (130, 2112, 22)) | (st <= np.pi * rad)


def classify(V, names):
    """Classes of addendum 1 (v2).  'dif' = decay of pi+-/K+- on the first arc (any radius); 'difc' = the same
    after the first turn; 'k0l' = decay of K0L; 'ni22/30/61' = inelastic (hadronic or photonuclear)
    in the beam pipe / TBPX L1 / TBPX L2 on the first arc; 'nix' = inelastic elsewhere, first arc; 'nic' = inelastic
    anywhere after the first turn.  Returns a dict of boolean masks."""
    pn = {v: k for k, v in names.proc.items()}; vn = {v: k for k, v in names.vol.items()}
    proc = np.array([pn[int(x)] for x in V[:, 2]]); vol = np.array([vn[int(x)] for x in V[:, 3]])
    r = np.hypot(V[:, 5], V[:, 6])
    inel = np.array([('Inelastic' in p) or (p == 'photonNuclear') for p in proc], bool)
    fa = first_arc(V)
    dec = (proc == 'Decay')          # v2 of addendum 1: every radius inside the Geant4 world (r < 1200 mm), nothing dropped
    in_v1_range = (r > 30.0) & (r < 1000.0)
    ap = np.abs(V[:, 4])
    three = np.isin(vol, ('BeamPipe', 'TBPX_L1', 'TBPX_L2'))
    m = dict(dif=dec & np.isin(ap, (211, 321)) & fa, difc=dec & np.isin(ap, (211, 321)) & ~fa, k0l=dec & (ap == 130),
             ni22=inel & (vol == 'BeamPipe') & fa, ni30=inel & (vol == 'TBPX_L1') & fa, ni61=inel & (vol == 'TBPX_L2') & fa,
             nix=inel & ~three & fa, nic=inel & ~fa, ni_any=inel, dif_all=dec & np.isin(ap, (211, 321)),
             dif_v1range=dec & np.isin(ap, (211, 321)) & fa & in_v1_range)
    return m, proc, vol


def partition(out, n_int, n_fire, stream, chunk):
    """Complete partition of the Geant4 vertices of the pool (addendum 1 v2, findings A1, A2, B1, B9, C6): every pool
    species through the whole tracker (r < 1200 mm), slab-exit hand-over; counts per (class, species) and per layer
    group, the pool and the v1 parent counts per interaction.  Every vertex is in exactly one class."""
    import p2c_mbgen
    t0 = time.time()
    arrays, mmeta = p2c_mbgen.generate(n_int, stream, chunk)
    pool = dict(pdg=arrays['pool_pdg'], pt=arrays['pool_pt'], eta=arrays['pool_eta'])
    names = Names()
    seed = C.qv2_seed(stream + '.g4', chunk, mod=2 ** 62)
    rec, st = fire(pool, n_fire, 'all', seed + 3, geom_file(), 'FTFP_BERT', names, handover='exit')
    A = pack([rec]); V = A['vtx']
    m, proc, vol = classify(V, names)
    ap = np.abs(V[:, 4]).astype(np.int64)
    excl = ['dif', 'difc', 'k0l', 'ni22', 'ni30', 'ni61', 'nix', 'nic']
    cls = np.full(len(V), 'other', dtype=object)
    r = np.hypot(V[:, 5], V[:, 6])
    cls[(proc == 'conv')] = 'conversion'
    cls[(proc == 'Decay')] = 'decay of another species'
    n_in = np.zeros(len(V), int)
    for k in excl:
        cls[m[k]] = k; n_in += m[k]
    assert n_in.max() <= 1, 'a vertex is in two classes'
    sp_frac = {int(a): float((np.abs(pool['pdg']) == a).mean()) for a in PASSES['all']['species']}
    table = {}
    for k in sorted(set(cls)):
        table[k] = {str(a): int(((cls == k) & (ap == a)).sum()) for a in PASSES['all']['species']}
        table[k]['all'] = int((cls == k).sum())
    grp = {}
    fa = first_arc(V)
    for v, k, f in zip(vol, cls, fa):
        if k in ('nix', 'nic'):
            g = v.split('_in')[0].split('_out')[0]
            g = 'discs' if g.startswith(('TFPX', 'TEPX', 'TEDD')) else g
            grp.setdefault(g, {'nix': 0, 'nic': 0})[k] += 1
    road = 0.30 / (2 * np.pi)
    meta = dict(mode='partition', stream=stream, chunk=chunk, n_fire=n_fire, n_vertices=int(len(V)), counts=table,
                counts_sum=int(sum(t['all'] for t in table.values())), species_fraction_of_pool=sp_frac,
                pool_per_interaction=mmeta['n_pool_per_interaction'], pool_in_road_per_interaction=mmeta['n_pool_per_interaction'] * road,
                v1_rates=mmeta['rate_per_interaction_in_road'], layer_groups=grp, g4=st, vcols=VCOLS, proc_names=names.proc,
                vol_names=names.vol, product_handover='exit', prod_cols=['pdg', 'px', 'py', 'pz', 'E', 'x', 'y', 'z', 't'],
                cross_cols=['surface', 'x', 'y', 'z', 't', 'px', 'py', 'pz'], t_total_s=round(time.time() - t0, 1),
                yield_per_firing={k: t['all'] / n_fire for k, t in table.items()},
                code_sha256=C.code_hashes([__file__, C.HERE / 'g4' / 'g4hv.cc', C.HERE / 'p2c_mbgen.py']))
    meta['bytes'] = C.save_job(out, dict(A, pool_pdg=pool['pdg'], pool_pt=pool['pt'], pool_eta=pool['eta']), meta)
    log.info('%s', json.dumps(dict(counts=table, sum=meta['counts_sum'], n_vertices=meta['n_vertices'], groups=grp, g4_ms=st['cpu_ms_per_firing'])))


def main(argv):
    mode, out = argv[0], argv[1]
    t0 = time.time()
    if mode == 'scan':
        geom = geom_file()
        kv, so = run_g4([geom, 'FTFP_BERT', 1, 'scan.txt', 'scan', int(argv[2]), 'overlap'])
        rows = [ln.split()[1:] for ln in open('scan.txt') if ln.startswith('S ')]
        names = sorted({r[1] for r in rows})
        S = np.array([[float(r[0]), names.index(r[1])] + [float(x) for x in r[2:]] for r in rows])
        ovl = [ln for ln in so.splitlines() if 'verlap' in ln and 'Checking' not in ln]
        meta = dict(mode='scan', g4=kv, volumes=names, cols=['eta', 'vol', 'path_mm', 'x_over_X0', 'x_over_lambdaI',
                                                              'r_mid_mm', 'z_mid_mm'],
                    overlap_messages=ovl[:50], n_overlap_messages=len(ovl), geometry=Path(geom).read_text(),
                    code_sha256=C.code_hashes([__file__, C.HERE / 'g4' / 'g4hv.cc', C.HERE / 'g4' / 'make_geom_g4.py']))
        C.save_job(out, dict(scan=S), meta)
        log.info('scan: %d rows, %d volumes, overlap messages %d', len(S), len(names), len(ovl))
        return
    if mode == 'part':
        return partition(out, int(argv[2]), int(argv[3]), argv[4], int(argv[5]))
    n_int, n_dif, n_ni, stream, chunk = int(argv[2]), int(argv[3]), int(argv[4]), argv[5], int(argv[6])
    physlist = argv[7] if len(argv) > 7 else 'FTFP_BERT'
    handover = argv[8] if len(argv) > 8 else 'vertex'
    import p2c_mbgen
    arrays, mmeta = p2c_mbgen.generate(n_int, stream, chunk)
    pool = dict(pdg=arrays['pool_pdg'], pt=arrays['pool_pt'], eta=arrays['pool_eta'])
    geom = geom_file()
    names = Names()
    seed = C.qv2_seed(stream + '.g4', chunk, mod=2 ** 62)
    rd, sd = fire(pool, n_dif, 'dif', seed + 1, geom, physlist, names, handover=handover)
    rn, sn = fire(pool, n_ni, 'ni', seed + 2, geom, physlist, names, fire0=n_dif, handover=handover)
    A = pack([rd, rn])
    m, proc, vol = classify(A['vtx'], names)
    ip = A['vtx'][:, 1]
    yld = dict(dif_pass={k: float((v & (ip == 0)).sum()) / max(n_dif, 1) for k, v in m.items()},
               ni_pass={k: float((v & (ip == 1)).sum()) / max(n_ni, 1) for k, v in m.items()})
    n_sel_dif = int(np.isin(np.abs(pool['pdg']), PASSES['dif']['species']).sum())
    meta = dict(mode='g4vtx-time', stream=stream, chunk=chunk, physlist=physlist, product_handover=handover, vcols=VCOLS, proc_names=names.proc,
                vol_names=names.vol, passes=PASSES, mbgen=mmeta, dif=sd, ni=sn, yield_per_firing=yld,
                pool_size=int(len(pool['pdg'])), pool_dif_species=n_sel_dif, t_total_s=round(time.time() - t0, 2),
                prod_cols=['pdg', 'px', 'py', 'pz', 'E', 'x', 'y', 'z', 't'], cross_cols=['surface', 'x', 'y', 'z', 't', 'px', 'py', 'pz'],
                code_sha256=C.code_hashes([__file__, C.HERE / 'g4' / 'g4hv.cc', C.HERE / 'g4' / 'make_geom_g4.py',
                                           C.HERE / 'p2c_mbgen.py']))
    meta['bytes'] = C.save_job(out, dict(A, pool_pdg=pool['pdg'], pool_pt=pool['pt'], pool_eta=pool['eta'],
                                         hist=arrays['hist'], hist_prompt=arrays['hist_prompt']), meta)
    log.info('%s', json.dumps(dict(mb_ms=mmeta['cpu_ms_per_interaction'], pool_per_int=mmeta['n_pool_per_interaction'],
                                   rates=mmeta['rate_per_interaction_in_road'], dif=sd, ni=sn, yld=yld,
                                   bytes=meta['bytes'])))


if __name__ == '__main__':
    main(sys.argv[1:])
