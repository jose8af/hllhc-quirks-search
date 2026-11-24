"""p3g_common.py -- shared definitions of work package p3-g (channel (i), B1 + B3 development; Tormod, 2026-11-24).

Attribution (STR l.747-753, COM B1-f, quoted in the artifact): n(r) = number of double-crossing layers rung r requires;
j_c = number of the candidate's double-crossing layers whose two crossings come from particles of ONE origin class c.
  attributed to c   if j_c >= n/2
  mixed             if 1 <= j_c < n/2 for every class
  pure pile-up      if j_c = 0 for the hard-scatter and Geant4 classes (here: the "own" class of the overlaid term)
Layer rule (Eskil's cpu_attrib.py, the one the study already used): a TBPX layer counts with >= 2 hits of the class,
a stacked (PS, 2S) layer with >= 2 hits of the class on each of its two sensors (crossings = min(in, out)).
j is evaluated on all band hits of the candidate (as cpu_attrib.py).  Two readings of "the candidate's double-crossing
layers" are carried (none chosen): JA = the layer types rung r requires (IP layers for R01-R11; IP + 2S for R12-R14),
JB = all ten layers.
"""
import hashlib
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[2]
REPO = QV2.parents[1]
P2SRC = QV2 / 'phase2_exploration' / 'src'
P3SRC = QV2 / 'phase3_selection' / 'src'
OUT = QV2 / 'phase3_selection' / 'outputs' / 'p3g'
DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data')

OWN_VP = 3500            # v1 GUN_VP: the overlaid no-pile-up event's hits are inserted with this vp (cppu mode)
HS_VP = 3000             # hard-scatter vertex of the SM chain (zhl mode: the own class)
TOPUP_BASE = 500_000     # pu_inputs.topup: INT % 1e6 >= 500000 for top-up rows (pile-up class)
# rung columns of production.RUNGS (F matrix of g1b_tt.trial)
R = {f'R{k:02d}': k - 1 for k in range(1, 15)}
R.update({f'FB{k}': 17 + k for k in range(5)})
NREQ = {'R01': 4, 'R02': 5, 'R03': 6, **{f'R{k:02d}': 7 for k in range(4, 12)}, 'R12': 8, 'R13': 9, 'R14': 10,
        **{f'FB{k}': 10 for k in range(5)}}
STORE_RUNGS = [f'R{k:02d}' for k in range(1, 15)] + [f'FB{k}' for k in range(5)]
CAND_COLS = (['ev', 'trial', 'cidx', 'rbits', 'nit2', 'nip2', 'n2s2', 'w_core', 'p_chi2', 'n_band', 'n_own', 'n_ckf_band',
              'f_ckf', 'jo_ip', 'jo_2s', 'jp_ip', 'jp_2s', 'jg_ip', 'jg_2s', 'n_g4vtx_layers', 'n_g4vtx']
             + [f'co{l}' for l in range(10)] + [f'ca{l}' for l in range(10)])


def setup_logging(name):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s', stream=sys.stderr)
    return logging.getLogger(name)


def qv2_seed(stream, chunk, mod=2 ** 62):
    """blake2b("qv2|stream|chunk") (STR §4.17 seed scheme), 8 bytes little endian."""
    return int.from_bytes(hashlib.blake2b(f'qv2|{stream}|{chunk}'.encode(), digest_size=8).digest(), 'little') % mod


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def layer_crossings(lc, sd, mask):
    """crossings per layer (10,) of the hits selected by mask: TBPX = hits, stacked = min(in, out)."""
    out = np.zeros(10, np.int64)
    for L in range(10):
        a = (lc == L) & mask
        out[L] = int(a.sum()) if L < 4 else int(min((a & (sd == 1)).sum(), (a & (sd == 2)).sum()))
    return out


def j_split(cr):
    """(IP, 2S) numbers of layers with >= 2 crossings."""
    return int((cr[:7] >= 2).sum()), int((cr[7:] >= 2).sum())


def rbits(Frow):
    b = 0
    for i, r in enumerate(STORE_RUNGS):
        if Frow[R[r]]:
            b |= 1 << i
    return b


def passes(rb, rung):
    return (np.asarray(rb, np.int64) >> STORE_RUNGS.index(rung)) & 1 == 1


def categories(C, rung, reading='A', own='jo', other=('jp',), g4=None):
    """Attribution categories of candidates (structured columns dict C) at a rung.
    Returns dict of bool arrays: att_own, att_other (any other class), mixed, pure (j_own = 0 and j_g4 = 0)."""
    n = NREQ[rung]
    two_s = rung in ('R12', 'R13', 'R14') or rung.startswith('FB')

    def jj(p):
        if reading == 'A':
            return C[f'{p}_ip'] + (C[f'{p}_2s'] if two_s else 0)
        return C[f'{p}_ip'] + C[f'{p}_2s']
    jo = jj(own)
    js = [jj(p) for p in other]
    jg = jj(g4) if g4 else np.zeros_like(jo)
    half = n / 2.0
    att_own = jo >= half
    att_oth = np.zeros_like(att_own)
    for x in js:
        att_oth |= x >= half
    if g4:
        att_oth |= jg >= half
    all_c = [jo] + js + ([jg] if g4 else [])
    mixed = np.ones_like(att_own)
    for x in all_c:
        mixed &= (x < half)
    mixed &= np.max(np.stack(all_c), axis=0) >= 1
    pure = (jo == 0) & (jg == 0)
    mixed &= ~pure          # "pure pile-up if j = 0 for the hard-scatter and Geant4 classes" takes precedence
    return dict(att_own=att_own, att_other=att_oth, mixed=mixed, pure=pure)


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.part')
    tmp.write_text(json.dumps(obj, indent=1, default=lambda o: o.item() if hasattr(o, 'item') else str(o)))
    os.replace(tmp, path)
