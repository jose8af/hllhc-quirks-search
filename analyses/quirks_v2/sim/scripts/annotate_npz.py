"""annotate_npz.py -- write the yield normalisation into every Stage-2 npz and into SAMPLES_INDEX.json (review S2-R1 B6 /
constructive B-2; fixer 2026-10-11).  Run after val_xsec.py (reads results/xsec.json):
    pixi run -e ana python scripts/annotate_npz.py
Scalars added to each physics npz (E/S INC, TRG, TRGS, LOPS, V-*):
  sigma_norm_fb      recommended normalisation, N_IC = 2 INCLUDED [fb]: 2 x K_WG(13.6 TeV, theory_signal_model §2.3) x
                     LO_MG(CT18NLO, mu = sqrt(s-hat), alpha = 1/127.9, sw2 = 0.22225) for E (probe t16); the TH §2.3 14 TeV
                     column for E-tilde (UNVERIFIED transcription; LO part re-derived)
  sigma_ref_fb       denominator for fractions [fb, N_IC = 1]: INC sigma_matched at the same mass for TRG / TRGS files
                     (V-TUNE-TRG -> V-TUNE-INC; V-SHOWER-x-TRG -> V-SHOWER-x-INC; V-MPI -> E-INC 500, MPI changes sigma_matched by +0.2 %), own sum(w) otherwise
  normalisation_tag  provenance / tag string (VERIFIED, ESTIMATE, UNVERIFIED as in VALIDATION.md §1.2)
Yield of a selection at 3 ab^-1: 3000 * sigma_norm_fb * sum(w_sel) / sigma_ref_fb  (mg_events.sigma_norm_fb).
SAMPLES_INDEX.json gets '_sigma_norm_fb' = {'{spin}_{m}': value} and '_normalisation_note'.
"""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.dirname(HERE)
DATA = os.path.normpath(os.path.join(SIM, '..', 'data', 'sim'))
X = json.load(open(os.path.join(SIM, 'results', 'xsec.json')))
NE = {int(k): v for k, v in X['normalisation_E']['rows'].items()}
NS = {int(k): v for k, v in X['normalisation_S'].items()}


def sigma_norm(spin, m):
    if spin == 'S':
        return NS[m]['sigma_norm_nic2_fb'], 'E-tilde: TH §2.3 14 TeV column, N_IC=2 (UNVERIFIED transcription of K; LO re-derived, VALIDATION §1.1)'
    if m in NE:
        r = NE[m]
        return r['sigma_norm_nic2_fb'], (f"E: 2 x K({r['K']:.3f}; {r['K_tag']}) x LO_MG(alpha=1/127.9, sw2=0.22225, probe t16) "
                                         f"= {r['sigma_norm_nic2_fb']:.5g} fb; {r['tag']}")
    lo, hi = max(k for k in NE if k < m), min(k for k in NE if k > m)          # off-grid (V-INTERP 550): log-linear
    a, b = NE[lo]['sigma_norm_nic2_fb'], NE[hi]['sigma_norm_nic2_fb']
    v = float(np.exp(np.interp(m, [lo, hi], [np.log(a), np.log(b)])))
    return v, f'E: log-linear interpolation of sigma_norm between {lo} and {hi} GeV (ESTIMATE)'


def ref_file(id_, m):
    if id_ in ('E-TRG', 'E-TRGS'):
        return f'E-INC_m{m}.npz'
    if id_ in ('S-TRG', 'S-TRGS'):
        return f'S-INC_m{m}.npz'
    if id_ == 'V-TUNE-TRG':
        return 'V-TUNE-INC_m500.npz'
    if id_ == 'V-MPI':
        return 'E-INC_m500.npz'
    if id_.startswith('V-SHOWER') and id_.endswith('-TRG'):
        return id_[:-4] + f'-INC_m{m}.npz'
    return None


def main():
    idxp = os.path.join(DATA, 'SAMPLES_INDEX.json')
    idx = json.load(open(idxp))
    meta = {}
    for p in sorted(glob.glob(os.path.join(DATA, 'npz', '*_m*.npz'))):
        b = os.path.basename(p)[:-4]
        id_, m = b.rsplit('_m', 1); m = int(m)
        if id_.startswith('P-') or id_.startswith('T2'):
            continue
        c = dict(np.load(p, allow_pickle=False))
        spin = str(c['spin'])
        sn, tag = sigma_norm(spin, m)
        rf = ref_file(id_, m)
        sref = float(np.load(os.path.join(DATA, 'npz', rf))['w'].sum()) if rf else float(c['w'].sum())
        c.update(sigma_norm_fb=float(sn), sigma_ref_fb=sref, normalisation_tag=tag + f'; sigma_ref from {rf or "this file"}',
                 n_ic_in_sigma_norm=2)
        np.savez_compressed(p, **c)
        meta[f'{spin}_{m}'] = float(sn)
        print(f'{b}: sigma_norm {sn:.5g} fb (N_IC=2), sigma_ref {sref:.5g} fb ({rf or "self"})', flush=True)
    idx['_sigma_norm_fb'] = meta
    idx['_normalisation_note'] = ('sigma_norm_fb: N_IC = 2 included, LO(alpha(MZ)) x K (theory_signal_model §2.3); yield = '
                                  '3000/fb^-1 x sigma_norm_fb x sum(w_sel)/sigma_ref_fb (npz scalars; mg_events.sigma_norm_fb). '
                                  'Excludes gamma-gamma (+4.0-4.2 %), Sommerfeld (+5-15 %), NLO EW. See SAMPLES.md.')
    json.dump(idx, open(idxp, 'w'), indent=1, sort_keys=True)


if __name__ == '__main__':
    main()
