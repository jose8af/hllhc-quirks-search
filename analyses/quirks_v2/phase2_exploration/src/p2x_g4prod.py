"""p2x_g4prod.py -- production mode of the Geant4 vertex generation: parent pool read from pool FILES.

  <acts python> p2x_g4prod.py <out_prefix> <pass: all|ni> <n_fire> <stream> <chunk> <pool_prefix: pool|lowpt> \
                              <groups> <pool file> [...]

  groups   comma list  name=class+class,...   e.g.  dif=dif+k0l,difc=difc,nix=nix,nic=nic,ni22=ni22,ni30=ni30,ni61=ni61
           or one mixed group  hs=dif+difc+k0l+ni22+ni30+ni61+nix+nic.  One vertex file <out_prefix>.<name>.npz is
           written per group, holding the vertices of its classes in firing order (an unbiased sequence).
  pass     'all': every pool species through the whole tracker (r < 1200 mm);  'ni': every species, primary dropped
           beyond r = 70 mm (only ni22, ni30, ni61 are complete in this pass: other groups are refused).

Physics as validated by Tatiana (p2c_g4vtx.py, imported, not modified): a firing = one pool parent, drawn uniformly
with replacement from the pool rows, from a luminous-region vertex with a uniform azimuth; Geant4 FTFP_BERT; products
followed to the exit of the slab of their vertex ('exit').  The firing loop below is p2c_g4vtx.fire with the pool row
of every firing kept (fire() does not return it).
Every vertex is classified into exactly one of ten classes (p2x_common.class_codes: asserted); the full partition
table (class x species, conversions and 'other' included) is in meta of every file.  Products and crossings are
stored for the B1 classes of the group only.
Arrays per group file: vtx (n, len(VCOLS)), cls (n) int8, src (n, len(SRC_COLS)), prod (m, 9), prod_off, cross (k, 8),
cross_off.  Side file <out_prefix>.sha.json: content hash of every group file.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

import p2c_common as C
import p2c_g4vtx as GV
import p2x_common as X

sys.path.insert(0, str(C.CODE))
import s4pu  # noqa: E402

log = C.setup_logging('p2x_g4prod')
SRC_COLS = ['pool_file', 'pool_row', 'src_index', 'phi_fire', 'road_dphi', 'w_src', 'first_arc']
NI_PASS_COMPLETE = ('ni22', 'ni30', 'ni61')
SUB = 500_000


def parse_groups(spec):
    g = {}
    for item in spec.split(','):
        name, cl = item.split('=')
        cls = cl.split('+')
        assert all(c in X.B1_CLASSES for c in cls), f'unknown class in group {item}'
        g[name] = cls
    used = sum(g.values(), [])
    assert len(used) == len(set(used)), 'a class appears in two groups'
    return g


def fire_chunk(pool, sel, n, pname, seed, geom, physlist, names, fire0):
    """One sub-chunk of n firings (p2c_g4vtx.fire l.88-110, pool row kept)."""
    ps = GV.PASSES[pname]
    rng = np.random.default_rng(seed)
    bs = json.loads((C.QV2 / 'acts' / 'geometry' / 'cms_phase2_public.json').read_text())['beamspot']
    sig = np.array([bs['sigma_xy_um'] * 1e-3, bs['sigma_xy_um'] * 1e-3, bs['sigma_z_mm'], bs['sigma_t_ps'] * 1e-3])
    idx = sel[rng.integers(0, len(sel), n)]
    phi = rng.uniform(-np.pi, np.pi, n)
    v = rng.normal(0.0, 1.0, (n, 4)) * sig
    pt = pool['pt'][idx].astype(float); eta = pool['eta'][idx].astype(float)
    prim = np.c_[pool['pdg'][idx], v, pt * np.cos(phi), pt * np.sin(phi), pt * np.sinh(eta), idx]
    fin = Path(f'prim_{pname}.txt'); fout = Path(f'vtx_{pname}.txt')
    with open(fin, 'w') as f:
        for i, r in enumerate(prim):
            f.write('%d %d %.6f %.6f %.6f %.6f %.9g %.9g %.9g\n' % (i, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
    kv, _ = GV.run_g4([geom, physlist, int(rng.integers(1, 2 ** 31 - 1)), fout, 'prim', fin, ps['rmax'], 'exit'])
    V, P, Xc, np_, nx = GV.parse(fout, names, fire0, list(GV.PASSES).index(pname), prim)
    fin.unlink(); fout.unlink()
    A = GV.pack([dict(V=V, P=P, X=Xc, np=np_, nx=nx)])
    loc = (A['vtx'][:, 0] - fire0).astype(np.int64)            # index of the firing inside this sub-chunk
    return A, idx[loc], phi[loc], kv


def take(A, keep):
    """Rows `keep` (sorted indices) of a packed record, with their products and crossings."""
    po, xo = A['prod_off'], A['cross_off']
    npd = po[1:] - po[:-1]; nxd = xo[1:] - xo[:-1]
    km = np.zeros(len(A['vtx']), bool); km[keep] = True
    return dict(vtx=A['vtx'][keep], prod=A['prod'][np.repeat(km, npd)], cross=A['cross'][np.repeat(km, nxd)],
                nprod=npd[keep], ncross=nxd[keep])


def run(out_prefix, pname, n_fire, stream, chunk, pool_prefix, groups, pool_files, physlist='FTFP_BERT'):
    t0 = time.time()
    if pname == 'ni':
        bad = [c for cl in groups.values() for c in cl if c not in NI_PASS_COMPLETE]
        assert not bad, f"classes {bad} are not complete in the 'ni' pass (primary dropped beyond r = 70 mm)"
    job_seed = C.qv2_seed(stream, chunk)
    pool, pool_meta = X.load_pool(pool_files, pool_prefix)
    sel = np.nonzero(np.isin(np.abs(pool['pdg']), GV.PASSES[pname]['species']))[0]
    assert len(sel) > 0, 'empty parent pool'
    geom = GV.geom_file()
    names = GV.Names()
    species = GV.PASSES['all']['species']
    table = {k: {str(a): 0 for a in species} for k in X.CLASSES}
    parts = {g: [] for g in groups}
    g4 = dict(event_cpu_s=0.0, init_cpu_s=0.0, nprod_exit=0, nprod_stopped_in_slab=0, nvtx=0, ndropped=0)
    done = 0; j = 0
    while done < n_fire:
        n = min(SUB, n_fire - done)
        seed = s4pu.hseed('p2x-g4', job_seed, pname, j, mod=2 ** 62)
        A, prow, phi, kv = fire_chunk(pool, sel, n, pname, seed, geom, physlist, names, done)
        for k in g4:
            g4[k] += float(kv.get(k, 0)) if k.endswith('_s') else int(kv.get(k, 0))
        code, fa = X.class_codes(A['vtx'], names)
        ap = np.abs(A['vtx'][:, 4]).astype(np.int64)
        for ci, cname in enumerate(X.CLASSES):
            mc = code == ci
            for a in species:
                table[cname][str(a)] += int((mc & (ap == a)).sum())
        src = np.c_[pool['file'][prow], pool['row'][prow], pool['src'][prow], phi, pool['dphi'][prow], pool['w'][prow], fa]
        for g, cl in groups.items():
            keep = np.nonzero(np.isin(code, [X.CODE[c] for c in cl]))[0]
            r = take(A, keep); r['cls'] = code[keep]; r['src'] = src[keep]
            parts[g].append(r)
        done += n; j += 1
        del A
    for k in table:
        table[k]['all'] = sum(table[k].values())
    n_vtx = sum(t['all'] for t in table.values())
    assert n_vtx == g4['nvtx'], f'vertices parsed {n_vtx} != Geant4 summary {g4["nvtx"]}'
    base = dict(mode='g4prod', g4_pass=pname, stream=stream, chunk=chunk, job_seed=job_seed, n_fire=n_fire, physlist=physlist,
                product_handover='exit', pool_prefix=pool_prefix, pool_files=pool_meta, pool_rows=int(len(pool['pdg'])),
                pool_rows_in_pass=int(len(sel)), groups=groups, counts=table, counts_sum=n_vtx, classes=X.CLASSES,
                yield_per_firing={k: t['all'] / n_fire for k, t in table.items()},
                complete_classes=list(NI_PASS_COMPLETE) if pname == 'ni' else list(X.B1_CLASSES),
                vcols=GV.VCOLS, src_cols=SRC_COLS, proc_names=names.proc, vol_names=names.vol,
                prod_cols=['pdg', 'px', 'py', 'pz', 'E', 'x', 'y', 'z', 't'],
                cross_cols=['surface', 'x', 'y', 'z', 't', 'px', 'py', 'pz'], g4=g4,
                g4_ms_per_firing=1e3 * g4['event_cpu_s'] / n_fire,
                code_sha256=dict(C.code_hashes([C.HERE / 'g4' / 'g4hv.cc', C.HERE / 'g4' / 'make_geom_g4.py', C.HERE / 'g4' / 'g4hv.sh',
                                                C.HERE / 'g4' / 'CMakeLists.txt']),
                                 **X.src_hashes('p2x_g4prod.py', 'p2x_common.py', 'p2c_g4vtx.py', 'p2c_common.py')),
                input_sha256=X.input_hashes([C.QV2.parents[1] / 'tools' / 'install' / 'g4' / 'pixi.lock']),
                geometry_sha256=C.sha256_file(geom))
    shas = {}
    for g, cl in groups.items():
        ps = parts[g]
        arrays = dict(vtx=np.concatenate([p['vtx'] for p in ps]), cls=np.concatenate([p['cls'] for p in ps]).astype(np.int8),
                      src=np.concatenate([p['src'] for p in ps]), prod=np.concatenate([p['prod'] for p in ps]),
                      cross=np.concatenate([p['cross'] for p in ps]))
        arrays['prod_off'] = np.r_[0, np.cumsum(np.concatenate([p['nprod'] for p in ps]))].astype(np.int64)
        arrays['cross_off'] = np.r_[0, np.cumsum(np.concatenate([p['ncross'] for p in ps]))].astype(np.int64)
        assert arrays['prod_off'][-1] == len(arrays['prod']) and arrays['cross_off'][-1] == len(arrays['cross'])
        assert np.all(np.isin(arrays['cls'], [X.CODE[c] for c in cl])), 'a vertex outside the classes of its group'
        meta = dict(base, group=g, group_classes=cl, n_vertices=int(len(arrays['vtx'])),
                    n_per_class={c: int((arrays['cls'] == X.CODE[c]).sum()) for c in cl},
                    t_total_s=round(time.time() - t0, 1))
        f = f'{out_prefix}.{g}.npz'
        X.save(f, arrays, meta)
        shas[Path(f).name] = meta['content_sha256']
        log.info('group %s: %d vertices %s, %d bytes, sha %s', g, meta['n_vertices'], meta['n_per_class'], meta['bytes'],
                 meta['content_sha256'][:16])
    X.write_sha(f'{out_prefix}.sha.json', dict(job=dict(stream=stream, chunk=chunk, job_seed=job_seed, g4_pass=pname,
                                                        n_fire=n_fire), counts=table, g4=g4, files=shas))
    log.info('%s', json.dumps(dict(n_fire=n_fire, counts={k: t['all'] for k, t in table.items()}, g4=g4,
                                   t_total_s=round(time.time() - t0, 1))))


if __name__ == '__main__':
    a = sys.argv[1:]
    run(a[0], a[1], int(a[2]), a[3], int(a[4]), a[5], parse_groups(a[6]), a[7:])
