"""p2c_common.py -- shared helpers of Phase-2 channel (iii) (executor Tatiana, 2026-11-16).

Seeds: job seed = blake2b("qv2|<stream>|<chunk>") (STR §4.17), the v1 hash family (`s4pu.hseed`).
Record layout of the pilot files (one compressed npz per job), written by `save_job`, read by `load_job`:
  hits (N, 13) float32   run_chain.COLS for every written measurement of all events (barrel counting surfaces + BTL)
  hit_off (n_ev + 1)     event i owns hits[hit_off[i]:hit_off[i+1]]
  tru (N, 3) float32     truth (SimHit) position of each written measurement
  vz (M, 8), vz_off      vertices per event (vp, x, y, z, t, sum px, py, pz)
  v41 (n_ev, 13)         V4-1 ingestion-closure record (run_chain.V41_COLS)
  timing (n_ev, 6)       seconds per stage (run_chain.T_COLS)
  meta                   JSON string
plus mode-specific arrays (documented in the writer).
"""
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
CODE = QV2 / 'acts' / 'stage4' / 'code'
ANA = QV2 / 'acts' / 'stage4' / 'analysis'
CHAIN_FILES = ['run_chain.py', 's4pu.py', 's4geo.py', 's4cp.py']


def setup_logging(name):
    try:
        from rich.logging import RichHandler
        handlers = [RichHandler(rich_tracebacks=True, show_path=False)]
    except ImportError:          # the acts and g4 environments have no rich
        handlers = [logging.StreamHandler(sys.stderr)]
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(message)s', handlers=handlers)
    return logging.getLogger(name)


def qv2_seed(stream, chunk, mod=900_000_000):
    """blake2b("qv2|stream|chunk"), digest 8 bytes little endian, as s4pu.hseed('qv2', stream, chunk)."""
    s = f'qv2|{stream}|{chunk}'
    return int.from_bytes(hashlib.blake2b(s.encode(), digest_size=8).digest(), 'little') % mod


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def code_hashes(extra=()):
    d = {f: sha256_file(CODE / f) for f in CHAIN_FILES}
    for p in extra:
        d[str(Path(p).name)] = sha256_file(p)
    return d


def concat(arrs, width, dtype):
    off = np.zeros(len(arrs) + 1, np.int64)
    for i, a in enumerate(arrs):
        off[i + 1] = off[i] + len(a)
    if off[-1] == 0:
        return np.zeros((0, width), dtype), off
    return np.concatenate([np.asarray(a, dtype).reshape(-1, width) for a in arrs]), off


def save_job(out, arrays, meta):
    """Atomic compressed write inside the job's scratch directory (the runner publishes it to cajuela)."""
    out = Path(out)
    tmp = out.with_name(out.name + '.tmp.npz')
    np.savez_compressed(tmp, meta=np.array(json.dumps(meta, default=str)), **arrays)
    os.replace(tmp, out)
    return out.stat().st_size


def load_job(path):
    z = np.load(path)
    meta = json.loads(str(z['meta']))
    return z, meta


def event_hits(z, i):
    """Hits of event i in the v1 per-event layout (float64, run_chain.COLS)."""
    a, b = int(z['hit_off'][i]), int(z['hit_off'][i + 1])
    return z['hits'][a:b].astype(np.float64)
