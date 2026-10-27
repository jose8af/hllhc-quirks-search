"""Peak memory of one finder process at rho = 1 / 2 (PU-only; reads only the needed fix-R1 PU events).
Run (theory_track): pixi run python -m acts.stage4.finder.mem_probe <rho>  -> prints JSON (ru_maxrss in GB)."""
import json
import resource
import sys

import numpy as np

from . import trials as TR


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9   # macOS: bytes


if __name__ == '__main__':
    rho = int(sys.argv[1])
    F = TR.F
    r0 = rss()
    from . import finder as FF
    files = sorted(F.PUD.glob('pu_w*.npz'))
    d = np.load(files[0])
    evs = []
    for k in sorted([k for k in d.files if k.startswith('ev')], key=lambda k: int(k[2:]))[:rho]:
        evs.append((int(k[2:]), d[k], d['vz' + k[2:]]))
    rng = np.random.default_rng(5)
    parts = [F.prep(e, vz, tag, rng, True) for tag, e, vz in evs]
    H = np.concatenate([p[0] for p in parts]); sid = np.concatenate([p[1] for p in parts])
    INT = np.concatenate([p[2] for p in parts]); SIG = np.concatenate([p[3] for p in parts])
    pv = F.lum_pv(rng); phimet = float(rng.uniform(-np.pi, np.pi))
    r1 = rss()
    FF.find(H, sid, pv, phimet, store='loose')          # includes numba cache load / compile
    r2 = rss()
    FF.find(H, sid, pv, phimet, INT=INT, SIG=SIG, store='loose')
    r3 = rss()
    print(json.dumps(dict(rho=rho, rss_after_imports_GB=round(r0, 3), rss_after_input_GB=round(r1, 3),
                          peak_after_first_find_GB=round(r2, 3), peak_after_second_find_GB=round(r3, 3),
                          n_hits=int(len(H)))))
