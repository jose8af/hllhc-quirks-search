"""f200.py -- S2-c (COM S2-c; STR §4.14 (b)): f200 with ONE definition, its uncertainty pieces and the T1 nuisance.
Channel (ii): written by Sebastian (2026-11-16), reworked by Edgar (2026-11-17): file list from done markers, 7- and
9-point scale envelopes, asymmetric Hessian PDF, variant shifts with statistical errors, combination, v1 comparison.
Orchestrator ruling 2026-11-16 12:14: f200 is allowed in Phase 2 (COM BL-1, selection-independent); A and m_mig are not
computed here, and nothing else is computed from the signal samples.

DEFINITION (the only one; STR §4.14 (b)): f200 = sigma(pT(QQbar) > 200 GeV after the shower) / sigma(matched, inclusive),
NO eta cut.  Numerator and denominator come from the SAME inclusive MLM 0-2j sample (p2-b-s2c-inc):
    f200 = sum_i w_i [pt_pair_i > 200] / sum_i w_i
with w = nominal merged weight (npz 'w', fb per event; sum w = sigma_matched at qCut 45) and pt_pair = pT of the
quirk pair after the shower (npz 'pt_pair'; convert_hepmc.py).  Rows with w = 0 contribute nothing.

PIECES (each computed as the same ratio with another weight column or on a re-shower of the same LHE events):
  stat   : weighted binomial, var = [sum_pass w^2 (1-f)^2 + sum_fail w^2 f^2] / (sum w)^2
  scale  : LHE weights 'MUF=a_MUR=b_PDF=14400_MERGING=45.000', a, b in {0.5, 1, 2}; envelope relative to (1, 1);
           7-point (without (0.5, 2), (2, 0.5)) = nominal choice, 9-point reported beside it
  pdf    : CT18NLO Hessian members 14401..14458 (eigenvector pairs 2k-1, 2k) relative to member 0 (= 14400, the
           generation PDF); asymmetric master formula
             up = sqrt(sum_k max(X_{2k-1} - X0, X_{2k} - X0, 0)^2),  dn = sqrt(sum_k max(X0 - X_{2k-1}, X0 - X_{2k}, 0)^2)
           and symmetric 1/2 sqrt(sum_k (X_{2k-1} - X_{2k})^2); quoted at the set's 90 % C.L. (CT18NLO.info,
           retrieval_log #19) and converted to 68 % under a Gaussian assumption (divide by Phi^-1(0.95), computed here;
           CT18 itself prints no factor, retrieval_log #30): ESTIMATE
  merging: re-showers with qCut 30 and 60 GeV against 45 (p2-b-s2c-rs, same LHE); envelope of the two shifts
  tune   : Monash re-shower against CP5; one-sided shift, symmetrised (|shift| up and down) by convention
  fsr    : FSR-off re-shower; the shift is QUOTED (S2-d), it is NOT part of the band
  fxfx   : not run (orchestrator / user: on hold, 30-minute exception pending); the band carries no FxFx term
Shift errors: (i) unpaired sqrt(stat_nom^2 + stat_var^2), conservative; (ii) PAIRED: the re-showers use the same LHE
events, which are matched by chunk and by the bit-identical hard-process quirk momenta (p_qp_hard, p_qm_hard; status-23
LHE kinematics); the linearised variance of f_var - f_nom is sum over the union of events of (b_i - a_i)^2 with
a_i = w_i (I_i - f)/sum w for each sample (0 where an event is absent).  (ii) is the error quoted for the shift.
BAND = quadrature sum of scale (7-point), pdf (68 %), merging, tune and stat, separately up and down; the T1 nuisance is
one asymmetric log-normal on the signal yield with kappa_up = 1 + up, kappa_dn = 1 - dn (pyhf normsys hi/lo).
Limiting checks done in the code: a weight column identical to w gives a zero shift; the central scale and PDF-member-0
columns reproduce the nominal f200.
Usage (on a worker, TT env with numpy): python f200.py <out.json> [--allow-partial]
"""
import json
import logging
import os
import re
import sys
from statistics import NormalDist

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marker_files import done_outputs  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('f200')
PT = 200.0
POINTS = (('E200', 'finc-m200-c'), ('E500', 'finc-m500-c'), ('E1000', 'finc-m1000-c'), ('E1500', 'finc-m1500-c'),
          ('S500', 'sinc-m500-c'))
V1 = dict(E200=0.04764, E500=0.10418, E1000=0.14585, E1500=0.16876, S500=0.1135)   # STR §4.14 (b), D5 §2 [U]
N_CHUNKS = 5
CL90_TO_68 = NormalDist().inv_cdf(0.95)


def load(files):
    cols = None
    for j, f in enumerate(sorted(files)):
        d = np.load(f)
        names = [str(x) for x in d['wvar_names']]
        n = len(d['w'])
        chunk = float(int(str(d['tag']).split('.')[0].rsplit('-c', 1)[1]))      # chunk number from the tag
        key = np.ascontiguousarray(np.hstack([np.full((n, 1), chunk), d['p_qp_hard'], d['p_qm_hard']]))
        c = dict(pt=d['pt_pair'], w=d['w'], W=d['wvar'], names=names, key=key.view('V72').ravel(),
                 tags=[str(d['tag']).split('.')[0]])
        if cols is None:
            cols = c
        else:
            if names != cols['names']:
                raise SystemExit(f'weight names differ in {f}')
            for k in ('pt', 'w', 'W', 'key', 'tags'):
                cols[k] = np.concatenate([cols[k], c[k]]) if k != 'tags' else cols[k] + c[k]
    return cols


def paired_shift_err(cn, cv):
    """sigma of f_var - f_nom with events matched on (chunk, hard quirk momenta); see the docstring."""
    def contrib(c):
        w, p = c['w'], c['pt'] > PT
        f = w[p].sum() / w.sum()
        return w * (p - f) / w.sum()
    a, b = contrib(cn), contrib(cv)
    if len(np.unique(cn['key'])) != len(cn['key']) or len(np.unique(cv['key'])) != len(cv['key']):
        return None, None
    common, ia, ib = np.intersect1d(cn['key'], cv['key'], return_indices=True)
    only_a = np.setdiff1d(np.arange(len(a)), ia)
    only_b = np.setdiff1d(np.arange(len(b)), ib)
    var = ((b[ib] - a[ia]) ** 2).sum() + (a[only_a] ** 2).sum() + (b[only_b] ** 2).sum()
    return float(np.sqrt(var)), int(len(common))


def frac(pt, w):
    s = w.sum()
    p = pt > PT
    f = w[p].sum() / s
    var = ((w[p] ** 2).sum() * (1 - f) ** 2 + (w[~p] ** 2).sum() * f ** 2) / s ** 2
    return float(f), float(np.sqrt(var))


def col(c, name):
    return c['W'][:, c['names'].index(name)]


def piece_scale(c):
    vals = {}
    for i, n in enumerate(c['names']):
        m = re.fullmatch(r'MUF=([0-9.]+)_MUR=([0-9.]+)_PDF=14400_MERGING=45\.000', n)
        if m:
            vals[(float(m.group(1)), float(m.group(2)))] = frac(c['pt'], c['W'][:, i])[0]
    f0 = vals[(1.0, 1.0)]
    seven = {k: v for k, v in vals.items() if k not in ((0.5, 2.0), (2.0, 0.5))}
    out = dict(central=f0, points={f'muF{a}_muR{b}': v for (a, b), v in vals.items()})
    for lab, s in (('7pt', seven), ('9pt', vals)):
        out[lab] = dict(n=len(s), up=max(s.values()) / f0 - 1, dn=1 - min(s.values()) / f0)
    return out


def piece_pdf(c):
    mem = {}
    for i, n in enumerate(c['names']):
        m = re.fullmatch(r'MUF=1\.0_MUR=1\.0_PDF=(144\d\d)_MERGING=45\.000', n)
        if m:
            mem[int(m.group(1)) - 14400] = frac(c['pt'], c['W'][:, i])[0]
    x0 = mem[0]
    pairs = [(mem[k], mem[k + 1]) for k in sorted(mem) if k % 2 == 1 and k + 1 in mem]
    up = np.sqrt(sum(max(a - x0, b - x0, 0.0) ** 2 for a, b in pairs))
    dn = np.sqrt(sum(max(x0 - a, x0 - b, 0.0) ** 2 for a, b in pairs))
    sym = 0.5 * np.sqrt(sum((a - b) ** 2 for a, b in pairs))
    return dict(member0=x0, n_members=len(mem) - 1, n_pairs=len(pairs),
                cl90=dict(up=float(up / x0), dn=float(dn / x0), sym=float(sym / x0)),
                cl68_gauss=dict(up=float(up / x0 / CL90_TO_68), dn=float(dn / x0 / CL90_TO_68),
                                sym=float(sym / x0 / CL90_TO_68), factor=CL90_TO_68))


def main():
    out = sys.argv[1]
    partial = '--allow-partial' in sys.argv
    res = dict(definition=__doc__.split('Usage')[0], points={})
    for label, prefix in POINTS:
        r = {}
        nom_files = done_outputs('p2-b-s2c-inc', suffix='.nom.npz', prefix=prefix, verify=True)
        if len(nom_files) != N_CHUNKS and not partial:
            raise SystemExit(f'{label}: {len(nom_files)} nominal chunks done, {N_CHUNKS} expected')
        c = load(nom_files)
        f0, e0 = frac(c['pt'], c['w'])
        assert frac(c['pt'], c['w'].copy())[0] == f0                     # identical column -> zero shift
        r['nom'] = dict(f200=f0, stat=e0, n_rows=int(len(c['w'])), n_rows_w_pos=int((c['w'] > 0).sum()),
                        n_files=len(nom_files), sigma_matched_fb_NIC1=float(c['w'].sum() / len(nom_files) * 1.0))
        r['nom']['sigma_matched_note'] = 'sum w over all chunks divided by the number of chunks (each chunk normalised to sigma)'
        r['check_weight_Weight_equals_w'] = float(np.max(np.abs(col(c, 'Weight_MERGING=45.000') - c['w'])) /
                                                  max(np.max(np.abs(c['w'])), 1e-300)) if 'Weight_MERGING=45.000' in c['names'] else None
        r['scale'] = piece_scale(c)
        r['pdf'] = piece_pdf(c)
        r['check_central_reproduces_nominal'] = dict(scale_central_minus_nom=r['scale']['central'] - f0,
                                                     pdf_member0_minus_nom=r['pdf']['member0'] - f0)
        cn = dict(pt=c['pt'], w=c['w'], key=c['key'])
        cn_tags = c['tags']
        r['check_paired_self'] = paired_shift_err(cn, cn)        # limiting case: identical samples -> 0
        del c
        r['variants'] = {}
        for var in ('qc30', 'qc60', 'monash', 'nofsr'):
            files = done_outputs('p2-b-s2c-rs', suffix=f'.{var}.npz', prefix=prefix, verify=True)
            if len(files) != N_CHUNKS and not partial:
                raise SystemExit(f'{label} {var}: {len(files)} chunks done, {N_CHUNKS} expected')
            if not files:
                continue
            cv = load(files)
            if cv['tags'] != cn_tags and not partial:
                raise SystemExit(f'{label} {var}: chunk tags differ: {cv["tags"]} vs {cn_tags}')
            fv, ev = frac(cv['pt'], cv['w'])
            pe, nm = paired_shift_err(cn, cv)
            r['variants'][var] = dict(f200=fv, stat=ev, n_rows=int(len(cv['w'])), n_files=len(files),
                                      shift=fv / f0 - 1, shift_err_unpaired=float(np.hypot(e0, ev) / f0),
                                      shift_err_paired=None if pe is None else pe / f0, n_events_matched=nm,
                                      shift_signif_paired=None if pe is None else (fv - f0) / pe)
            del cv
        V = r['variants']
        sh = [V[v]['shift'] for v in ('qc30', 'qc60') if v in V]
        merg_up = max([0.0] + sh)
        merg_dn = max([0.0] + [-x for x in sh])
        tune = abs(V['monash']['shift']) if 'monash' in V else 0.0
        st = e0 / f0
        up = float(np.sqrt(r['scale']['7pt']['up'] ** 2 + r['pdf']['cl68_gauss']['up'] ** 2 + merg_up ** 2 + tune ** 2 + st ** 2))
        dn = float(np.sqrt(r['scale']['7pt']['dn'] ** 2 + r['pdf']['cl68_gauss']['dn'] ** 2 + merg_dn ** 2 + tune ** 2 + st ** 2))
        r['band'] = dict(components_rel=dict(scale7_up=r['scale']['7pt']['up'], scale7_dn=r['scale']['7pt']['dn'],
                                             pdf68_up=r['pdf']['cl68_gauss']['up'], pdf68_dn=r['pdf']['cl68_gauss']['dn'],
                                             merging_up=merg_up, merging_dn=merg_dn, tune_sym=tune, stat=st),
                         up=up, dn=dn, fxfx='not run: on hold pending the user ruling on a 30-minute exception',
                         fsr_off_shift_quoted_not_in_band=V.get('nofsr', {}).get('shift'))
        r['T1_nuisance'] = dict(type='asymmetric log-normal on the signal yield (pyhf normsys)', kappa_up=1 + up, kappa_dn=1 - dn)
        r['v1'] = dict(f200_v1=V1[label], ratio_new_over_v1=f0 / V1[label], ratio_stat=e0 / V1[label])
        res['points'][label] = r
        log.info('%s f200 = %.5f +- %.5f (v1 %.5f) band +%.3f/-%.3f | %s', label, f0, e0, V1[label], up, dn,
                 json.dumps(r['band']['components_rel']))
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
