"""add_rowmap.py -- add per-row provenance and the template/toy split to the merged Stage-2 npz files (fixer S2-R1, review
items B-5 and B-8).  Run (sim/): pixi run -e ana python scripts/add_rowmap.py [ID_m<m> ...]   (default: all physics files)

Columns added (one value per row):
  chunk     int16  MG chunk k of the point (LHE file data/sim/lhe/<ID>/m<m>_c<k>.lhe.gz; seed in npz/chunks/<ID>/m<m>_c<k>.done.json)
  ievt_lhe  int32  0-based index of the event in that LHE file
  py8_job   int8   Pythia job j (the chunk LHE is cut into NJOBS = 6 consecutive pieces, produce.split_lhe)
  ievt_job  int32  0-based index of the event inside job j (Pythia is sequential: rerun job j from its start to regenerate it)
  py8_seed  int64  Random:seed of job j = (seed_chunk * 10 + j) % 900000000 + 1 (produce.run_chunk)
  tt_split  int8   deterministic template/toy flag: 0 = template, 1 = toy (B-8).  bit 0 of splitmix64(crc32(ID), m, chunk,
                   ievt_lhe): independent of file order, selection and Lambda; ~50/50.
Matching: the two quirks of each row before the shower (p_qp_hard, p_qm_hard = Pythia status 23 = LHE momenta; 6-D) are
matched to the quirk pair of the LHE events of all chunks of the point: exact (< 1e-6 GeV) for ~99.8 % of the
rows; Pythia puts massless LHE c/b quarks on shell and rescales the event (<= 0.4 GeV on the quirk) for the rest, so the
criterion is nearest distance < 2 GeV with the next-nearest event >= 20x further.
Checks (abort on failure): every row matched exactly once; (chunk, job) blocks follow the merged 'tag' order; ievt_job
strictly increasing inside each block.  Scalar 'rowmap_version' records the run.  Idempotent (recomputes and overwrites).
"""
import glob
import gzip
import json
import os
import re
import sys
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data', 'sim'))
NJOBS = 6
RX = re.compile(rb'^\s*-90000(?:11|13)\s+1\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)', re.M)
RXN = re.compile(rb'^\s*90000(?:11|13)\s+1\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)', re.M)
PHYS = ('E-INC', 'E-TRG', 'E-LOPS', 'S-INC', 'S-TRG', 'S-LOPS', 'V-TUNE-TRG', 'V-TUNE-INC', 'V-MERGE-20', 'V-MERGE-50',
        'V-NJ1', 'V-MPI', 'V-INTERP')
M64 = (1 << 64) - 1


def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & M64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & M64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & M64
    return x ^ (x >> 31)


def tt_split(id_, m, chunk, ievt):
    base = (zlib.crc32(id_.encode()) << 32) ^ (int(m) << 20)
    return np.array([splitmix64(base ^ (int(c) << 24) ^ int(i)) & 1 for c, i in zip(chunk, ievt)], np.int8)


def lhe_quirks(path):
    with gzip.open(path, 'rb') as f:
        txt = f.read()
    nev = txt.count(b'<event>')
    q = np.array([[float(a), float(b), float(c)] for a, b, c in RX.findall(txt)])
    qn = np.array([[float(a), float(b), float(c)] for a, b, c in RXN.findall(txt)])
    assert len(q) == nev and len(qn) == nev, (path, len(q), len(qn), nev)
    return np.hstack([q, qn])


def process(id_, m):
    f = os.path.join(DATA, 'npz', f'{id_}_m{m}.npz')
    c = dict(np.load(f, allow_pickle=False))
    dones = sorted(glob.glob(os.path.join(DATA, 'npz', 'chunks', id_, f'm{m}_c*.done.json')),
                   key=lambda s: int(re.search(r'_c(\d+)\.done', s).group(1)))
    Q, CH, IEV, seeds, nl = [], [], [], {}, {}
    for d in dones:
        k = int(re.search(r'_c(\d+)\.done', d).group(1))
        dj = json.load(open(d))
        q = lhe_quirks(os.path.join(DATA, 'lhe', id_, f'm{m}_c{k}.lhe.gz'))
        assert len(q) == dj['n_lhe']
        Q.append(q); CH.append(np.full(len(q), k)); IEV.append(np.arange(len(q))); seeds[k] = dj['seed']; nl[k] = len(q)
    Q = np.concatenate(Q); CH = np.concatenate(CH); IEV = np.concatenate(IEV)
    assert int(c['nlhe']) == len(Q), (f, int(c['nlhe']), len(Q))
    from scipy.spatial import cKDTree
    P = np.hstack([c['p_qp_hard'][:, 1:], c['p_qm_hard'][:, 1:]])      # both quirks (6-D): unique even at 200k events
    d, nn = cKDTree(Q).query(P, k=2)
    # exact (<1e-6) for ~99.8 % of rows; Pythia puts massless LHE c/b quarks on shell and rescales the event, which moves
    # the quirk by <= 0.4 GeV in 0.2-1 % of events -> tolerance 2 GeV, and the next-nearest LHE event must be >= 20x further
    ok = (d[:, 0] < 2.0) & (d[:, 1] > 20 * np.maximum(d[:, 0], 1e-3))
    assert ok.all(), f'{f}: {np.sum(~ok)} rows without a unique LHE match (max d {d[:, 0].max():.3g})'
    n_exact = int(np.sum(d[:, 0] < 1e-6))
    src = nn[:, 0]
    assert len(np.unique(src)) == len(src), f'{f}: duplicate matches'
    chunk = CH[src]; ievt = IEV[src]
    job = np.empty(len(src), np.int8); ijob = np.empty(len(src), np.int32); seed = np.empty(len(src), np.int64)
    for k, n in nl.items():
        sizes = [n // NJOBS + (1 if j < n % NJOBS else 0) for j in range(NJOBS)]
        edges = np.cumsum([0] + sizes)
        s = chunk == k
        jj = np.searchsorted(edges, ievt[s], side='right') - 1
        job[s] = jj; ijob[s] = ievt[s] - edges[jj]
        seed[s] = (seeds[k] * 10 + jj) % 900000000 + 1
    # block structure vs the merged tag order (chunk-job blocks, events in order inside each block)
    blk = chunk.astype(np.int64) * 10 + job
    change = np.r_[True, blk[1:] != blk[:-1]]
    order = blk[change]
    tags = [str(t) for t in np.atleast_1d(c['tag'])]
    exp = [int(re.search(r'_c(\d+)_s(\d+)$', t).group(1)) * 10 + int(re.search(r'_s(\d+)$', t).group(1)) for t in tags]
    exp = [e for e in exp if e in set(order)]          # a split can have 0 kept rows only in tiny pilots
    assert list(order) == exp, f'{f}: block order {list(order)[:12]} != tag order {exp[:12]}'
    for b in order:
        s = blk == b
        assert np.all(np.diff(ijob[s]) > 0), f'{f}: events not ordered inside block {b}'
    c.update(chunk=chunk.astype(np.int16), ievt_lhe=ievt.astype(np.int32), py8_job=job, ievt_job=ijob, py8_seed=seed,
             tt_split=tt_split(id_, m, chunk, ievt), rowmap_version='add_rowmap.py fixer S2-R1 2026-10-11')
    np.savez_compressed(f, **c)
    return f'{id_}_m{m}: {len(src)} rows ({n_exact} exact, max d {d[:, 0].max():.2g} GeV) matched to {len(Q)} LHE events in {len(nl)} chunks; toy fraction {c["tt_split"].mean():.3f}'


def main():
    if len(sys.argv) > 1:
        todo = [(a.rsplit('_m', 1)[0], int(a.rsplit('_m', 1)[1])) for a in sys.argv[1:]]
    else:
        todo = []
        for p in sorted(glob.glob(os.path.join(DATA, 'npz', '*_m*.npz'))):
            b = os.path.basename(p)[:-4]
            id_, m = b.rsplit('_m', 1)
            if id_ in PHYS:
                todo.append((id_, int(m)))
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(int(os.environ.get('NPROC', 6))) as ex:
        for r in ex.map(process, *zip(*todo)):
            print(r, flush=True)


if __name__ == '__main__':
    main()
