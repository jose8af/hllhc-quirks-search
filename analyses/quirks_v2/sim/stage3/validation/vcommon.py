"""vcommon.py -- shared helpers for the Stage-3 validation scripts (Mac only; reads the Stage-2 loader and code/).
Environment: NUMBA_CACHE_DIR=sim/stage3/.numba_cache and PYTHONDONTWRITEBYTECODE=1 are set here before numba loads,
so no cache file is written under code/ or sim/scripts/.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S3 = HERE.parent
TT = S3.parents[1]
os.environ.setdefault('NUMBA_CACHE_DIR', str(S3 / '.numba_cache'))
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
sys.dont_write_bytecode = True
for p in (S3 / 'code', TT / 'sim' / 'scripts'):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
VOUT = TT / 'data' / 'sim_stage3' / 'validation'
VOUT.mkdir(parents=True, exist_ok=True)
RES = S3 / 'results'
RES.mkdir(exist_ok=True)
B0 = 3.8112


def add_orig_code_path():
    """Only for V1/V2a/V4: the original theory-track code (read only)."""
    for p in (TT / 'code', TT / 'analytic' / 'checks', TT / 'analytic' / 'numerics'):
        if str(p) not in sys.path:
            sys.path.append(str(p))


def mg_events(m, n, spin='F', eta_max=2.5, split='template'):
    import mg_events as mg
    out = []
    for e in mg.iter_events(m, 'trig', spin, eta_max=eta_max, ptmin=200.0, split=split, unweight=True):
        out.append(e)
        if len(out) == n:
            break
    return out


def dump(name, obj):
    p = RES / name
    json.dump(obj, open(p, 'w'), indent=1, default=float)
    return p
