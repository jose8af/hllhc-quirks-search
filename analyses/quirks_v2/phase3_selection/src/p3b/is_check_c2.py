"""Cycle-2 correction of the occupancy model's MC error at R08/R09 (p3-b review cycle 2, fixer Ivar; Liv B-new-1).

Standard library only (runs on einstein without numpy; no new Monte Carlo).  Inputs:
  outputs/p3b/is_check_inputs/ischeck-{0,1,2}.npz  the per-configuration outputs of `is_check.py --mode strat --all`
                                                   (copied from maxwell scratch; sha256 in SCHEMA.md)
  $QV2_DATA/p3b/p3-b-occmod/*/occmod-*.npz         the stored IS (isr[:, k, (m1, m2, npass)], 200 toys/configuration)
  outputs/p3b/is_check.json, is_check_stats.json, b2_dev_closure.json
Method (all toy-level, same 6,400 configurations):
  rel_toy(X) = sqrt(Σ_b (m2_b − m1_b²)/n_is) / Σ_b m1_b                       (stored: n_is = 200; fresh: 2,000)
  per-toy relative variance v(X) = rel_toy(X)² · N_toys(X); the stored value's error re-estimated with the fresh
  per-toy variance: rel_stored_c2 = rel_toy(fresh) · sqrt(n_fresh / n_stored)  (the stored estimate is a lower bound
  because its 200-toy runs do not sample the weight tail; this one is itself a lower bound if the tail is still
  under-sampled at 2,000 toys).
  R09 adds the binomial error of the fit-probability fraction f = n/N (47 of 3,966 development R06 groups):
  sqrt((1 − f)/n).
  mc_rel_error_c2(R08) = rel_stored_c2(R08); mc_rel_error_c2(R09) = sqrt(rel_stored_c2(R08)² + fitprob_rel²).
Writes outputs/p3b/is_check_c2.json.  `--patch` also adds the single key `occupancy_day15.mc_rel_error_c2` to the R08,
R09, R08x2S>=3 and R09x2S>=3 records of outputs/p3b/pileup_term.json (no other key touched); pileup_term.py imports
`c2_errors` and writes the same key on a rerun.
"""
import array
import ast
import glob
import json
import math
import os
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'outputs' / 'p3b'
DATA = Path(os.environ.get('QV2_DATA', '/nfs/cajuela/jdochoa/quirks_v2/data')) / 'p3b'
N_STORED, N_FRESH = 200, 2000


def npy_member(path, name):
    """(flat float64 list, shape) of member `name` of an .npz, parsed with the standard library."""
    with zipfile.ZipFile(path) as z:
        b = z.read(name + '.npy')
    assert b[:6] == b'\x93NUMPY'
    major = b[6]
    if major == 1:
        hl = int.from_bytes(b[8:10], 'little'); off = 10
    else:
        hl = int.from_bytes(b[8:12], 'little'); off = 12
    hdr = ast.literal_eval(b[off:off + hl].decode('latin1'))
    assert hdr['descr'] == '<f8' and not hdr['fortran_order'], hdr
    a = array.array('d'); a.frombytes(b[off + hl:])
    if sys.byteorder != 'little':
        a.byteswap()
    return a, hdr['shape']


def rel_toy(rows, nis):
    """rows: list of (m1, m2) per configuration."""
    s1 = sum(m1 for m1, _ in rows)
    var = sum(max(m2 - m1 * m1, 0.0) for m1, m2 in rows) / nis
    return math.sqrt(var) / s1


def c2_errors(out=OUT):
    """Return the cycle-2 error record (dict); reads the inputs listed in the module docstring."""
    fresh = {'R07': [], 'R08': []}
    for f in sorted(glob.glob(str(out / 'is_check_inputs' / 'ischeck-*.npz'))):
        a, sh = npy_member(f, 'isr')                       # (n, 2, 3): rungs (R07, R08) × (m1, m2, npass)
        n = sh[0]
        for j in range(n):
            for kk, c in enumerate(('R07', 'R08')):
                base = (j * 2 + kk) * 3
                fresh[c].append((a[base], a[base + 1]))
    stored = {'R07': [], 'R08': []}
    for f in sorted(glob.glob(str(DATA / 'p3-b-occmod' / '*' / 'occmod-*.npz'))):
        a, sh = npy_member(f, 'isr')                       # (nB, 4, 3): rungs R05..R08
        for b in range(sh[0]):
            for k, c in ((2, 'R07'), (3, 'R08')):
                base = (b * 4 + k) * 3
                stored[c].append((a[base], a[base + 1]))
    ic = json.loads((out / 'is_check.json').read_text())
    st = json.loads((out / 'is_check_stats.json').read_text())['combined']
    cl = json.loads((out / 'b2_dev_closure.json').read_text())
    nfp = cl['direct']['counts']['R06xp>0.001']; n06 = cl['direct']['counts']['R06']
    f = nfp / n06
    rec = {'n_configs_fresh': len(fresh['R08']), 'n_configs_stored': len(stored['R08']),
           'nis_stored': N_STORED, 'nis_fresh': N_FRESH, 'rungs': {}}
    for c in ('R07', 'R08'):
        rs = rel_toy(stored[c], N_STORED); rf = rel_toy(fresh[c], N_FRESH)
        ratio = (rf * rf * N_FRESH) / (rs * rs * N_STORED)
        rec['rungs'][c] = dict(rel_toy_stored=rs, rel_toy_fresh=rf, per_toy_variance_ratio_fresh_over_stored=ratio,
                               rel_stored_c2=rf * math.sqrt(N_FRESH / N_STORED),
                               plain_over_stored=ic[c]['plain_sum'] / ic[c]['stored_IS_sum'],
                               plain_over_fresh=ic[c]['plain_sum'] / ic[c]['fresh_IS_sum'],
                               plain_passes=ic[c]['plain_pass_toys'],
                               plain_rel_err=1 / math.sqrt(ic[c]['plain_pass_toys']))
    rec['rungs']['R06'] = dict(plain_over_stored=st['R06']['E_plain_mean'] / st['R06']['E_mean'],
                               plain_passes=st['R06']['plain_pass_toys'],
                               plain_rel_err=1 / math.sqrt(st['R06']['plain_pass_toys']))
    rec['ess_toys_stored_R08'] = dict(total=None, per_seed=[s['rungs']['R08']['ess_toys']
                                                            for s in json.loads((out / 'is_check_stats.json')
                                                                                .read_text())['per_seed']])
    rec['ess_toys_stored_R08']['total'] = sum(rec['ess_toys_stored_R08']['per_seed'])
    rec['fitprob'] = dict(n_pass=nfp, n_R06=n06, fraction=f, rel_err=math.sqrt((1 - f) / nfp))
    r08 = rec['rungs']['R08']['rel_stored_c2']
    rec['mc_rel_error_c2'] = {'R08': r08, 'R08x2S>=3': r08,
                              'R09': math.hypot(r08, rec['fitprob']['rel_err']),
                              'R09x2S>=3': math.hypot(r08, rec['fitprob']['rel_err'])}
    return rec


def main():
    rec = c2_errors()
    (OUT / 'is_check_c2.json').write_text(json.dumps(rec, indent=1))
    if '--patch' in sys.argv:
        p = OUT / 'pileup_term.json'
        P = json.loads(p.read_text())
        for c, v in rec['mc_rel_error_c2'].items():
            P['candidates'][c]['occupancy_day15']['mc_rel_error_c2'] = v
        p.write_text(json.dumps(P, indent=1))
    sys.stdout.write(json.dumps(rec, indent=1) + '\n')


if __name__ == '__main__':
    main()
