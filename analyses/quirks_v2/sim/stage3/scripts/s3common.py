"""s3common.py -- shared paths and helpers for the Stage-3 post-production scripts (E8, 2026-10-13).

Read-only on the production outputs.  The canonical view of the production is data/sim_stage3/STAGE3_INDEX.json
(written by merge_index.py): every job of jobs/all.json once, pointing into out/ (Mac) or out_pc/ (PC), plus the
3 cross-machine overlap clones (campaign xover) kept separately per machine.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S3 = HERE.parent
TT = S3.parents[1]
DATA = TT / 'data' / 'sim_stage3'
OUT = {'mac': DATA / 'out', 'pc': DATA / 'out_pc'}
JOBS = S3 / 'jobs'
RES = S3 / 'results'
FIG = S3 / 'figures'
SUMM = DATA / 'summary'
INDEX = DATA / 'STAGE3_INDEX.json'
os.environ.setdefault('NUMBA_CACHE_DIR', str(S3 / '.numba_cache'))
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
sys.dont_write_bytecode = True
for p in (S3 / 'code',):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
SUMM.mkdir(parents=True, exist_ok=True)
B0 = 3.8112
C_MM_PER_NS = 299.792458
LABEL = 'Private work (simulation)'


def load_joblist(name):
    return json.load(open(JOBS / f'{name}.json'))['jobs']


def dump(name, obj):
    p = RES / name
    json.dump(obj, open(p, 'w'), indent=1, default=_default)
    return p


def _default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    raise TypeError(type(o))


def load_index():
    return json.load(open(INDEX))


def point_key(j):
    return f"{j['campaign']}/{j['spin']}_m{int(j['m'])}/L{float(j['lam']):g}_{j['cfg']}"


def fig_label(ax, extra='truth level'):
    """Plain internal label: 'Private work (simulation)', truth level.  No experiment-style label (Stage-5 restyle)."""
    ax.text(0.0, 1.01, f'{LABEL}  --  {extra}', transform=ax.transAxes, ha='left', va='bottom', fontsize='small')
