"""xover.py -- Stage-3 cross-machine check (E8, 2026-10-13): Mac (Apple M3, macOS arm64) vs PC (AMD 7800X3D, Windows
x86-64) on the 3 overlap jobs (jobs/overlap.json: P1 E500 1 keV B; P2 E500 1 keV BM; P2 E1000 3 keV BM), same events,
same per-event seeds, same code md5.

Criterion (fixed here before looking at the comparison, from the task statement): the PC outputs are usable if they are
statistically equivalent to the Mac outputs:
  1. count events whose kernel output is bit-identical (all 13 hit columns, status, nsteps, X_end, P_end, eacc, hits per
     surface); the numpy post-processing (plane fit via LAPACK eigh, closed-form truth via libm) is compared separately
     (max relative difference; the plane-normal sign is arbitrary);
  2. for the rest: the per-event difference size (hit positions matched by (quirk, surface, crossing index), delta
     thickness), and two-sample KS tests on the per-event observables (ds_barrel/ds_all/ds_itps, n hits per surface,
     n_rev, sep_IT, hit positions r, z, phi, t pooled) -- PASS if no KS p-value < 0.01 after the observable count
     (Bonferroni over the tests of a job), and the pull of every median (Mac - PC)/sigma_boot is |pull| < 3.
  A systematic difference (any failing test) -> STOP and report.
Output: sim/stage3/results/xover.json.  Run (theory_track/): pixi run python sim/stage3/scripts/xover.py
"""
import json

import numpy as np
from scipy.stats import ks_2samp

import s3common as C

HC = ('h_quirk', 'h_surf', 'h_icross', 'h_t', 'h_x', 'h_y', 'h_z', 'h_px', 'h_py', 'h_pz', 'h_E', 'h_dE', 'h_dl')
EVC = ('status', 'nsteps', 'X_end', 'P_end', 'eacc', 'nhit_surf', 'seed')      # kernel output per event
POST = ('ds_barrel_um', 'ds_all_um', 'ds_itps_um', 'res_max_um', 'gstar', 'ell_max', 'N_osc_vac', 'bodd_l0', 'k_B', 'c_ev')
OBS = ('ds_barrel_um', 'ds_all_um', 'ds_itps_um', 'n_trk0', 'n_trk1', 'hits_per_surf', 'n_surf_hit', 'max_cross',
       'n_rev0', 'n_rev1', 'sep_IT_um', 'dt_trk_max')


def boot_med_diff(a, b, nb=2000, seed=1):
    rng = np.random.default_rng(seed)
    n = len(a)
    d = [np.median(a[i]) - np.median(b[i]) for i in (rng.integers(0, n, n) for _ in range(nb))]
    return float(np.std(d))


def main():
    idx = C.load_index()
    ovl = C.load_joblist('overlap')
    summ = {m: np.load(C.SUMM / f'events_xover_{m}.npz') for m in ('mac', 'pc')}
    res = dict(criterion=__doc__.split('Criterion')[1].split('Output:')[0].strip(), jobs={})
    allpass = True
    for j in ovl:
        key = j['id'].split('/', 1)[1].rsplit('_c', 1)[0]
        f = {m: C.DATA / idx['points'][f'xover/{m}/{key}']['chunks'][0]['file'] for m in ('mac', 'pc')}
        Z = {m: dict(np.load(f[m])) for m in f}
        a, b = Z['mac'], Z['pc']
        n = int(a['n_events'])
        ident = np.zeros(n, bool); maxdx = np.full(n, np.nan); dds = np.full(n, np.nan); same_nhit = np.zeros(n, bool)
        for i in range(n):
            oa = slice(a['hit_offsets'][i], a['hit_offsets'][i + 1]); ob = slice(b['hit_offsets'][i], b['hit_offsets'][i + 1])
            ok = all(np.array_equal(a[k][oa], b[k][ob]) for k in HC)
            ok &= all(np.array_equal(a[k][i], b[k][i], equal_nan=True) for k in EVC)
            ident[i] = ok
            dds[i] = a['ds_all_um'][i] - b['ds_all_um'][i]
            # matched hits by (quirk, surface, icross)
            ka = {(int(q), int(s), int(c)): (x, y, z) for q, s, c, x, y, z in zip(a['h_quirk'][oa], a['h_surf'][oa], a['h_icross'][oa],
                                                                                 a['h_x'][oa], a['h_y'][oa], a['h_z'][oa])}
            kb = {(int(q), int(s), int(c)): (x, y, z) for q, s, c, x, y, z in zip(b['h_quirk'][ob], b['h_surf'][ob], b['h_icross'][ob],
                                                                                 b['h_x'][ob], b['h_y'][ob], b['h_z'][ob])}
            same_nhit[i] = set(ka) == set(kb)
            com = set(ka) & set(kb)
            if com:
                maxdx[i] = max(np.linalg.norm(np.subtract(ka[k], kb[k])) for k in com) * 1000.0
        # file-level equality of the per-event scalar arrays
        file_identical = all(np.array_equal(a[k], b[k], equal_nan=True) for k in HC + EVC + ('hit_offsets',))
        post = {}
        for k in POST:
            x, y = a[k][ident], b[k][ident]
            fin = np.isfinite(x) & np.isfinite(y)
            rel = np.abs(x[fin] - y[fin]) / np.maximum(np.abs(x[fin]), 1e-300)
            post[k] = dict(n_differ=int(np.sum(x[fin] != y[fin])), max_rel=float(rel.max()) if len(rel) else 0.0,
                           max_abs=float(np.abs(x[fin] - y[fin]).max()) if len(rel) else 0.0)
        nrm_same_up_to_sign = bool(np.allclose(np.abs(np.einsum('ij,ij->i', a['n_plane'][ident], b['n_plane'][ident])), 1.0, atol=1e-6,
                                               equal_nan=True))
        # distributions (per-event observables from the summary tables) and pooled hit coordinates
        sa = summ['mac']; sb = summ['pc']
        pa = list(sa['point_keys']).index(f'xover/mac/{key}'); pb = list(sb['point_keys']).index(f'xover/pc/{key}')
        ma = sa['point'] == pa; mb = sb['point'] == pb
        tests = {}
        for o in OBS:
            xa = sa[o][ma].astype(float); xb = sb[o][mb].astype(float)
            fin = np.isfinite(xa) & np.isfinite(xb)
            if fin.sum() < 5:
                continue
            xa, xb = xa[fin], xb[fin]
            ks = ks_2samp(xa, xb)
            sig = boot_med_diff(xa, xb)
            dm = float(np.median(xa) - np.median(xb))
            tests[o] = dict(n=int(fin.sum()), median_mac=float(np.median(xa)), median_pc=float(np.median(xb)), dmed=dm, sigma=sig,
                            pull=(dm / sig if sig > 0 else (0.0 if dm == 0 else np.inf)), ks_D=float(ks.statistic),
                            ks_p=float(ks.pvalue), paired_identical_frac=float(np.mean(xa == xb)))
        for nm, fa, fb in (('hit_r_mm', np.hypot(a['h_x'], a['h_y']), np.hypot(b['h_x'], b['h_y'])), ('hit_z_mm', a['h_z'], b['h_z']),
                           ('hit_phi', np.arctan2(a['h_y'], a['h_x']), np.arctan2(b['h_y'], b['h_x'])), ('hit_t_ns', a['h_t'], b['h_t'])):
            ks = ks_2samp(fa, fb)
            tests[nm] = dict(n_mac=len(fa), n_pc=len(fb), ks_D=float(ks.statistic), ks_p=float(ks.pvalue),
                             median_mac=float(np.median(fa)), median_pc=float(np.median(fb)))
        ntest = len(tests)
        fails = [k for k, t in tests.items() if t['ks_p'] < 0.01 / ntest or abs(t.get('pull', 0.0)) >= 3]
        ok = not fails
        allpass &= ok
        nonid = ~ident
        res['jobs'][j['id']] = dict(clone_of=j['clone_of'], n_events=n, n_kernel_bit_identical_events=int(ident.sum()),
                                    postprocessing_on_kernel_identical_events=post, plane_normal_equal_up_to_sign=nrm_same_up_to_sign,
                                    file_arrays_identical=bool(file_identical), n_same_hit_keys=int(same_nhit.sum()),
                                    n_hits=dict(mac=int(len(a['h_x'])), pc=int(len(b['h_x']))),
                                    nonidentical=dict(n=int(nonid.sum()),
                                                      max_hit_shift_um=dict(median=float(np.nanmedian(maxdx[nonid])) if nonid.any() else None,
                                                                            max=float(np.nanmax(maxdx[nonid])) if nonid.any() else None,
                                                                            values=[float(x) for x in np.sort(maxdx[nonid])]),
                                                      d_ds_all_um=[float(x) for x in dds[nonid]],
                                                      rel_d_ds_all=[float(x) for x in (dds / a['ds_all_um'])[nonid]],
                                                      status_mac=a['status'][nonid].tolist(), status_pc=b['status'][nonid].tolist(),
                                                      nsteps_diff=(a['nsteps'][nonid] - b['nsteps'][nonid]).tolist()),
                                    tests=tests, failing=fails, PASS=ok)
        print(j['id'], f'{int(ident.sum())}/{n} kernel-bit-identical; non-identical max hit shift {np.nanmax(maxdx[nonid]) if nonid.any() else 0:.3g} um;',
              'PASS' if ok else f'FAIL {fails}', flush=True)
    res['PASS'] = bool(allpass)
    C.dump('xover.json', res)
    print('XOVER', 'PASS' if allpass else 'FAIL')


if __name__ == '__main__':
    main()
