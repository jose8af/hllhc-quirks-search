"""val_interp.py -- mass-interpolation closure test (review S2-R1 constructive B-7; fixer 2026-10-11).
Run: pixi run -e ana python scripts/val_interp.py  ->  results/interp.json
Off-grid point V-INTERP m = 550 GeV (E, 0-2j MLM INC, 50k LHE, same settings as E-INC) compared with the interpolation of the
grid neighbours 500 and 600 GeV:
  sigma_matched           log-linear in m between E-INC 500 and E-INC 600;
  f(pT > 200)             linear, TRGS/INC at 500 and 600;
  median gamma*-1 (incl.) linear, E-INC 500 and 600;
  median x = 2(gamma*-1) and median N_osc in the tail (pT > 200, |eta| < 2.5): linear, TRGS 500 and 600 (V-INTERP: INC tail).
Closure = (off-grid - interpolated) / interpolated with the combined bootstrap error; PASS if |pull| < 2.
Tag: ESTIMATE (single generator)."""
import numpy as np

from vlib import S, have, save, boot_quant, wquant


def q50(c, sel, key):
    v = 2 * (c['g'] - 1) if key == 'x' else (c['g'] - 1 if key == 'gm1' else c['nosc'])
    q, e = boot_quant(v[sel], c['w'][sel], (0.5,), nb=150)
    return float(q[0]), float(e[0])


def main():
    if not have('V-INTERP', 550):
        print('no V-INTERP sample'); return
    R = dict(note=__doc__, points={})
    off = S('V-INTERP', 550)
    tail = lambda c: (c['pt'] > 200) & (np.abs(c['eta']) < 2.5) & (c['w'] != 0)
    allw = lambda c: c['w'] != 0
    lo, hi, mid = 500, 600, 550
    t = (mid - lo) / (hi - lo)
    rows = {}
    # sigma_matched: log-linear
    s_lo, s_hi = S('E-INC', lo)['w'].sum(), S('E-INC', hi)['w'].sum()
    e_lo = np.sqrt(np.sum(S('E-INC', lo)['w'] ** 2)); e_hi = np.sqrt(np.sum(S('E-INC', hi)['w'] ** 2))
    s_int = float(np.exp((1 - t) * np.log(s_lo) + t * np.log(s_hi)))
    e_int = s_int * np.hypot((1 - t) * e_lo / s_lo, t * e_hi / s_hi)
    s_off = float(off['w'].sum()); e_off = float(np.sqrt(np.sum(off['w'] ** 2)))
    rows['sigma_matched_fb'] = dict(offgrid=s_off, interp=s_int, rel=s_off / s_int - 1, err=float(np.hypot(e_off / s_off, e_int / s_int)))
    # f(pT>200)
    def fr(id_t, id_i, m):
        ct, ci = S(id_t, m), S(id_i, m)
        f = ct['w'][ct['pt'] > 200].sum() / ci['w'].sum()
        e = np.sqrt(np.sum(ct['w'][ct['pt'] > 200] ** 2)) / ci['w'].sum()
        return float(f), float(e)
    f_lo, fe_lo = fr('E-TRGS', 'E-INC', lo); f_hi, fe_hi = fr('E-TRGS', 'E-INC', hi); f_off, fe_off = fr('V-INTERP', 'V-INTERP', mid)
    f_int = (1 - t) * f_lo + t * f_hi; fe_int = np.hypot((1 - t) * fe_lo, t * fe_hi)
    rows['f_pt200'] = dict(offgrid=f_off, interp=f_int, rel=f_off / f_int - 1, err=float(np.hypot(fe_off / f_off, fe_int / f_int)))
    # medians
    for key, sel_f, src in (('gm1_incl', allw, 'E-INC'), ('x_tail', tail, 'E-TRGS'), ('nosc_tail', tail, 'E-TRGS')):
        k = {'gm1_incl': 'gm1', 'x_tail': 'x', 'nosc_tail': 'nosc'}[key]
        a, ea = q50(S(src, lo), sel_f(S(src, lo)), k); b, eb = q50(S(src, hi), sel_f(S(src, hi)), k)
        o, eo = q50(off, sel_f(off), k)
        v = (1 - t) * a + t * b; ev = np.hypot((1 - t) * ea, t * eb)
        rows[key] = dict(offgrid=o, interp=v, at_500=a, at_600=b, rel=o / v - 1, err=float(np.hypot(eo / o, ev / v)))
    for r in rows.values():
        r['pull'] = r['rel'] / r['err'] if r['err'] > 0 else None
        r['PASS'] = bool(abs(r['pull']) < 2)
    R['points']['F_550'] = rows
    R['n_tail_offgrid'] = int(tail(off).sum())
    save('interp.json', R)
    for k, r in rows.items():
        print(f"{k}: off {r['offgrid']:.5g} interp {r['interp']:.5g} rel {100 * r['rel']:+.2f} +- {100 * r['err']:.2f} % pull {r['pull']:+.2f}")


if __name__ == '__main__':
    main()
