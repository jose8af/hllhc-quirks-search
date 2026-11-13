"""val_v2a.py -- Stage-3 validation V2a: the Stage-1 numbers reproduced by the Stage-3 kernel (legacy mode) on the SAME
Stage-1 events (old T2-cache sample, T3_propagator.sample_events(m, 120, default_rng(777 + m), eta_max=1)).

Settings are those of the stored Stage-1 runs, so the comparison is exact:
  1 keV : M3 'prod' (max_boost 1e-2, hmax 0.2 cm), f = B/B0 in {1, 1/2} -> data/stage1_numerics/M3/m<m>_L1_e<i>_prod_B.npz
  3 keV : FU1 'fine' (max_boost 1e-3, hmax 0.02 cm), f in {1, 1/2}      -> data/stage1_numerics/FU/m<m>_L3_e<i>_fine.npz
(The plan's "max_boost 1e-3" applies to the 3 keV FU1 runs; the stored 120-event 1 keV runs are the M3 prod runs.)
Delta_s = plane through the origin on the 10 barrel layers (T3 definition); c2 = (2 Ds(B0/2)/Ds(B0) - 1)/ln 2 per event.
PASS: every per-event Delta_s equal to the stored value (bit for bit; reported as max relative difference), and the
median c2 equal to FU.json (FU1a m<m>_L1_prod, FU1b step_m<m>_L3 'fine').
Output: sim/stage3/results/V2a.json.  Run: nice pixi run python sim/stage3/validation/val_v2a.py
"""
import glob
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import vcommon as V

D1 = V.TT / 'data' / 'stage1_numerics'


def job(a):
    m, lam, iev, p1, p2 = a
    from T3_causal_s3 import run_causal_s3
    from s3_physics import plane_fit
    mb, hm = (1e-2, 0.2) if lam == 1.0 else (1e-3, 0.02)
    ds = []
    for f in (1.0, 0.5):
        r = run_causal_s3(p1, p2, m, lam, B0=V.B0 * f, material=False, max_boost=mb, hmax_trk=hm, max_steps=4_000_000_000,
                          legacy=True)
        H = r['hits']; H = H[H[:, 1] < 10]
        ds.append(plane_fit(H[:, 3:6])[0] if len(H) >= 4 else np.nan)
    return m, lam, iev, ds


if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    V.add_orig_code_path()
    from T3_propagator import sample_events
    tasks = []; ref = {}; fu_ok = {}
    regen_same = True
    for m in (500.0, 1000.0):
        evs = sample_events(m, 120, rng=np.random.default_rng(777 + int(m)), eta_max=1.0)
        for i, (p1, p2, info) in enumerate(evs):
            z = np.load(D1 / 'M3' / f'm{m:g}_L1_e{i:03d}_prod_B.npz')
            regen_same &= bool(np.array_equal(z['p1'], p1) and np.array_equal(z['p2'], p2))
            fr = z['fracs']
            ref[(m, 1.0, i)] = (float(z['ds'][np.isclose(fr, 1.0)][0]), float(z['ds'][np.isclose(fr, 0.5)][0]))
            zf = np.load(D1 / 'FU' / f'm{m:g}_L3_e{i:03d}_fine.npz')
            ref[(m, 3.0, i)] = (float(zf['ds'][0]), float(zf['ds'][1]))
            # FU_analysis keeps an event only if Delta_s is finite at every stored B fraction
            fu_ok[(m, 1.0, i)] = bool(np.all(np.isfinite(z['ds'][1:])))
            fu_ok[(m, 3.0, i)] = bool(np.all(np.isfinite(zf['ds'])) and np.all(zf['status'] == 1))   # FU_analysis.fu_load: status != 1 (queue overflow at some f) excluded
            for lam in (1.0, 3.0):
                tasks.append((m, lam, i, p1, p2))
    tasks.sort(key=lambda t: -t[1])
    tic = time.time()
    raw = V.VOUT / 'V2a_raw.npy'
    if raw.exists():
        R = list(np.load(raw, allow_pickle=True))
    else:
        with ProcessPoolExecutor(7) as ex:
            R = list(ex.map(job, tasks))
        np.save(raw, np.array(R, dtype=object), allow_pickle=True)
    import json
    FU = json.load(open(V.TT / 'analytic' / 'numerics' / 'results' / 'FU.json'))
    out = dict(events_regenerated_identical_to_M3_files=regen_same, wall_s=time.time() - tic, points={})
    allpass = regen_same
    for m in (500.0, 1000.0):
        for lam in (1.0, 3.0):
            rr = [r for r in R if r[0] == m and r[1] == lam]
            rel = []; nbit = 0; c2 = []; c2ref = []
            for _, _, i, ds in rr:
                a = ref[(m, lam, i)]
                for k in (0, 1):
                    if np.isfinite(a[k]) or np.isfinite(ds[k]):
                        rel.append(abs(ds[k] / a[k] - 1) if (a[k] != 0 and np.isfinite(a[k]) and np.isfinite(ds[k])) else (0.0 if (np.isnan(a[k]) and np.isnan(ds[k])) else np.inf))
                        nbit += int(ds[k] == a[k] or (np.isnan(ds[k]) and np.isnan(a[k])))
                    else:
                        nbit += 1          # both NaN (fewer than 4 hits): identical
                if np.all(np.isfinite(ds)) and np.all(np.isfinite(a)) and fu_ok[(m, lam, i)]:
                    c2.append((2 * ds[1] / ds[0] - 1) / np.log(2)); c2ref.append((2 * a[1] / a[0] - 1) / np.log(2))
            if lam == 1.0:
                fu = FU['FU1a'][f'm{m:g}_L1_prod']['all']['c2_median_of_events'][0]
            else:
                fu = FU['FU1b'][f'step_m{m:g}_L3']['fine']['c_median_of_events'][0][0]
            med = float(np.median(c2))
            ok = (nbit == 2 * len(rr)) and abs(med - fu) < 1e-12 * max(1, abs(fu)) * 1e3
            allpass &= ok
            out['points'][f'm{m:g}_L{lam:g}'] = dict(n_events=len(rr), n_ds_bit_identical=nbit, n_ds=2 * len(rr),
                                                    max_rel_diff=float(max(rel)) if rel else 0.0, median_c2=med, median_c2_stored_events=float(np.median(c2ref)),
                                                    FU_json_median_c2=fu, n_c2=len(c2), PASS=bool(ok))
    out['PASS'] = bool(allpass)
    V.dump('V2a.json', out)
    print(json.dumps(out, indent=1))
