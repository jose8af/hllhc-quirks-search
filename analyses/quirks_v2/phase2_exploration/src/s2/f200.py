"""f200.py -- S2-c: f200 with ONE definition and its uncertainty pieces (channel (ii), Sebastian; orchestrator ruling
2026-11-16: f200 allowed in Phase 2, A and m_mig are not computed here).

Definition (STR §4.14 (b)): f200 = sigma(pT(QQbar) > 200 GeV after the shower) / sigma(matched, inclusive), NO eta cut.
Both numerator and denominator come from the SAME inclusive MLM 0-2j sample (p2-b-s2c-inc), so
    f200 = sum_i w_i [pt_pair_i > 200] / sum_i w_i ,
with w the merged nominal weight (convert_hepmc.py 'w', qCut of the shower).  pt_pair = pT of the two quirks after the
shower (npz 'pt_pair').
Pieces (each as a ratio to the nominal on the same events where possible):
  stat     : weighted-binomial error, var = [sum_{pass} w^2 (1-f)^2 + sum_{fail} w^2 f^2] / (sum w)^2
  scale    : 9-point (mu_R, mu_F) x {0.5, 1, 2} merged weights 'MUF=a_MUR=b_PDF=14400_MERGING=<qc>' -> envelope
  pdf      : CT18NLO Hessian members 14401..14458 (pairs 2k-1, 2k): symmetric master formula
             d = 1/2 sqrt(sum_k (X_{2k-1} - X_{2k})^2); reported as given by the set (its CL convention is recorded,
             not converted here; see the EXPLORATION file)
  merging  : re-showers qCut 30 and 60 (p2-b-s2c-rs) vs 45
  tune     : Monash re-shower vs CP5
  fsr      : FSR-off re-shower (S2-d: the shift is quoted; not part of the band)
  fxfx     : optional FxFx samples (p2-b-s2-fxfx) at 500 / 1500 GeV, f200 from their own weights
Usage (on a worker, sim 'ana' env): python f200.py <out.json> <point_label>=<npz_dir>:<glob_prefix> ...
"""
import glob
import json
import logging
import os
import re
import sys

import numpy as np

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('f200')
PT = 200.0


def load(files):
    cols = None
    for f in sorted(files):
        d = np.load(f)
        names = [str(x) for x in d['wvar_names']]
        c = dict(pt=d['pt_pair'], w=d['w'], W=d['wvar'], names=names)
        if cols is None:
            cols = c
        else:
            if names != cols['names']:
                raise SystemExit(f'weight names differ in {f}')
            for k in ('pt', 'w', 'W'):
                cols[k] = np.concatenate([cols[k], c[k]])
    return cols


def frac(pt, w):
    s = w.sum()
    f = w[pt > PT].sum() / s
    p = pt > PT
    var = ((w[p] ** 2).sum() * (1 - f) ** 2 + (w[~p] ** 2).sum() * f ** 2) / s ** 2
    return float(f), float(np.sqrt(var))


def piece_scale(c, qc):
    vals = {}
    for i, n in enumerate(c['names']):
        m = re.fullmatch(r'MUF=([0-9.]+)_MUR=([0-9.]+)_PDF=14400_MERGING=' + re.escape(qc), n)
        if m:
            vals[f'muF{m.group(1)}_muR{m.group(2)}'] = frac(c['pt'], c['W'][:, i])[0]
    return vals


def piece_pdf(c, qc):
    mem = {}
    for i, n in enumerate(c['names']):
        m = re.fullmatch(r'MUF=1.0_MUR=1.0_PDF=(144\d\d)_MERGING=' + re.escape(qc), n)
        if m and int(m.group(1)) > 14400:
            mem[int(m.group(1)) - 14400] = frac(c['pt'], c['W'][:, i])[0]
    if not mem:
        return None
    k = sorted(mem)
    pairs = [(mem[a], mem[a + 1]) for a in k if a % 2 == 1 and a + 1 in mem]
    return dict(n_members=len(mem), d_sym=float(0.5 * np.sqrt(sum((x - y) ** 2 for x, y in pairs))))


def main():
    out = sys.argv[1]
    res = {}
    for arg in sys.argv[2:]:
        label, spec = arg.split('=', 1)
        d, prefix = spec.split(':', 1)
        r = {}
        for var in ('nom', 'qc30', 'qc60', 'monash', 'nofsr'):
            files = glob.glob(os.path.join(d, '*', f'{prefix}*.{var}.npz'))
            if not files:
                continue
            c = load(files)
            f, e = frac(c['pt'], c['w'])
            r[var] = dict(f200=f, stat=e, n_rows=int(len(c['w'])), n_files=len(files))
            if var == 'nom':
                qc = '45.000'
                r['scale'] = piece_scale(c, qc)
                r['pdf'] = piece_pdf(c, qc)
        if 'nom' in r:
            f0 = r['nom']['f200']
            sc = list(r['scale'].values())
            r['rel'] = dict(scale_up=max(sc) / f0 - 1 if sc else None, scale_dn=min(sc) / f0 - 1 if sc else None,
                            pdf=(r['pdf']['d_sym'] / f0) if r['pdf'] else None,
                            **{v: r[v]['f200'] / f0 - 1 for v in ('qc30', 'qc60', 'monash', 'nofsr') if v in r})
        res[label] = r
        log.info('%s: %s', label, json.dumps(r.get('rel', {})))
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
