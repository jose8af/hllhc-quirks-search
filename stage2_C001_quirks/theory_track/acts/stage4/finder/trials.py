"""PU-only G2 trial set (signal-blind): rho = 1 full TDR-normalised density (IT + OT top-up, f1r topup mode 1) and
rho = 2 superpositions.  Inputs are the 56 fix-R1 PU-200 events (data/acts_stage4/fix_r1/pu, Fatras in time) read with
the probe's own helpers (read-only import of acts/stage4/probes/f1r_finder.py).  Every trial is fully determined by its
index: the top-up, the luminous-region PV and the MET road angle come from default_rng(SEED0 + index).

  rho = 1 trial i (i = 0..55): event i, one road at phi0.
  rho = 2 trial i: events (2i, 2i+1) superposed (each with its own top-up), one road.
"""
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT / 'acts' / 'stage4' / 'probes'))
import f1r_finder as F  # noqa: E402

F.TOPUP_MODE = 1          # IT + OT top-up = the plan's adopted TDR-normalised density
F.T_TOL = 0.030
SEED0 = 4_200_000
_EVS = None


def events():
    global _EVS
    if _EVS is None:
        _EVS = F.load_pu()
    return _EVS


def trial_inputs(i, rho=1):
    evs = events()
    rng = np.random.default_rng(SEED0 + 1000 * rho + i)
    if rho == 1:
        tag, e, vz = evs[i]
        H, sid, INT, SIG, uz = F.prep(e, vz, tag, rng, True)
        evid = [int(tag)]
    elif rho == 2:
        a, b = 2 * i, 2 * i + 1
        Ha, sa, Ia, Sa, ua = F.prep(evs[a][1], evs[a][2], evs[a][0], rng, True)
        Hb, sb, Ib, Sb, ub = F.prep(evs[b][1], evs[b][2], evs[b][0], rng, True)
        H = np.concatenate([Ha, Hb]); sid = np.concatenate([sa, sb]); INT = np.concatenate([Ia, Ib])
        SIG = np.concatenate([Sa, Sb])
        evid = [int(evs[a][0]), int(evs[b][0])]
    else:
        raise ValueError(rho)
    pv = F.lum_pv(rng)
    phimet = float(rng.uniform(-np.pi, np.pi))
    return dict(H=H, sid=sid, INT=INT, SIG=SIG, pv=pv, phimet=phimet, ev=evid)
