"""p2x_common.py -- helpers of the pilot production code (Phase 2 channel (iii), executor Xavier, 2026-11-16).

Builds on Tatiana's p2c_* modules, which are imported and not modified.

Vertex classes (strategy addendum 1 v2, table of P3-P5; masks of p2c_g4vtx.classify, first arc of p2c_g4vtx.first_arc):
  code 0 dif    decay of pi+-/K+- on the first outward arc, any radius
       1 difc   decay of pi+-/K+- after the first turn
       2 k0l    decay of K0_L
       3 ni22   inelastic (hadronic or photonuclear), first arc, beam pipe
       4 ni30   the same, TBPX L1
       5 ni61   the same, TBPX L2
       6 nix    the same, every other volume
       7 nic    inelastic after the first turn, any volume
       8 conversion   (process 'conv'; not a B1 class, STR §4.4 pt 1)
       9 other        (every other process that ends the primary)
Every vertex gets exactly one code (asserted in `class_codes`).

Content hash: sha256 over every array of a job file except wall-clock timing, in sorted key order (name, dtype,
shape, bytes).  Two runs with the same seeds must give the same hash; it is stored in `meta` and in <out>.sha.json.
"""
import hashlib
import json
from pathlib import Path

import numpy as np

import p2c_common as C

CLASSES = ['dif', 'difc', 'k0l', 'ni22', 'ni30', 'ni61', 'nix', 'nic', 'conversion', 'other']
B1_CLASSES = CLASSES[:8]
CODE = {k: i for i, k in enumerate(CLASSES)}
NO_HASH = ('timing', 'meta')
INPUT_FILES = [C.QV2 / 'acts' / 'geometry' / 'cms_phase2_public.json', C.QV2 / 'sim' / 'stage3' / 'code' / 'surfaces_s3.json',
               C.QV2 / 'acts' / 'scripts' / 'pythia8_tune_CP5.dat']


def class_codes(V, names):
    """One class code per vertex row (p2c_g4vtx.VCOLS).  Asserts that the classes are exclusive and complete."""
    import p2c_g4vtx as GV
    if len(V) == 0:
        return np.zeros(0, np.int8), np.zeros(0, bool)
    m, proc, vol = GV.classify(V, names)
    n_in = np.zeros(len(V), np.int64)
    code = np.full(len(V), CODE['other'], np.int8)
    conv = proc == 'conv'
    code[conv] = CODE['conversion']
    for k in B1_CLASSES:
        n_in += m[k]
        code[m[k]] = CODE[k]
    assert n_in.max() <= 1, 'a vertex is in two B1 classes'
    assert not np.any(conv & (n_in > 0)), 'a conversion vertex is also in a B1 class'
    cnt = np.bincount(code, minlength=len(CLASSES))
    assert cnt.sum() == len(V) and np.array_equal(cnt[:8], [int(m[k].sum()) for k in B1_CLASSES]), 'partition does not sum'
    return code, GV.first_arc(V)


def content_sha256(arrays):
    h = hashlib.sha256()
    for k in sorted(arrays):
        if k in NO_HASH:
            continue
        a = np.ascontiguousarray(arrays[k])
        h.update(k.encode()); h.update(str(a.dtype).encode()); h.update(str(a.shape).encode()); h.update(a.tobytes())
    return h.hexdigest()


def save(out, arrays, meta, extra_sha=None):
    """content hash -> meta, atomic npz (p2c_common.save_job), side file <out stem>.sha.json."""
    meta['content_sha256'] = content_sha256(arrays)
    meta['bytes'] = C.save_job(out, arrays, meta)
    return meta['bytes']


def write_sha(path, files_meta):
    """Small JSON listing the content hash of every file a job wrote (one more declared output of the job)."""
    p = Path(path)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(files_meta, indent=1, default=str) + '\n')
    tmp.replace(p)


def input_hashes(extra=()):
    d = {}
    for p in list(INPUT_FILES) + [Path(x) for x in extra]:
        d[str(p.name)] = C.sha256_file(p) if Path(p).exists() else None
    return d


def src_hashes(*names):
    return {n: C.sha256_file(C.HERE / n) for n in names}


def load_pool(files, prefix='pool'):
    """Parent pool of one or more pool files (p2x_mbgen: prefix 'pool' or 'lowpt'; p2x_hspool: 'pool').
    Returns dict(pdg, pt, eta, file, row, src, dphi, w) and the list of the files' meta summaries."""
    P = dict(pdg=[], pt=[], eta=[], file=[], row=[], src=[], dphi=[], w=[]); metas = []
    for k, f in enumerate(files):
        z, m = C.load_job(f)
        n = len(z[f'{prefix}_pdg'])
        P['pdg'].append(z[f'{prefix}_pdg']); P['pt'].append(z[f'{prefix}_pt']); P['eta'].append(z[f'{prefix}_eta'])
        P['file'].append(np.full(n, k, np.int32)); P['row'].append(np.arange(n, dtype=np.int64))
        P['src'].append(z[f'{prefix}_int'].astype(np.int64))
        P['dphi'].append(z[f'{prefix}_dphi'].astype(np.float64) if f'{prefix}_dphi' in z.files else np.full(n, np.nan))
        P['w'].append(z[f'{prefix}_w'].astype(np.float64) if f'{prefix}_w' in z.files else np.ones(n))
        metas.append(dict(file=str(f), sha256=C.sha256_file(f), mode=m.get('mode'), stream=m.get('stream'),
                          chunk=m.get('chunk'), job_seed=m.get('job_seed'), content_sha256=m.get('content_sha256'),
                          n_src=m.get('n_int', m.get('n_events')), n_pool=int(n)))
    return {k: np.concatenate(v) for k, v in P.items()}, metas
