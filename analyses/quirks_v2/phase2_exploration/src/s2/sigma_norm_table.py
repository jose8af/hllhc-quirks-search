"""sigma_norm_table.py -- S2-b (COM S2-b; STR §4.14 [SD11], Df-3): the table sigma_norm(m) with both PDF sets, and the
resummed cross-check normalisation beside it.  Channel (ii), executor Edgar, 2026-11-17.  Stdlib only (einstein).

sigma_norm = N_IC x sigma_NLO(MG5_aMC, loop_quirkE, fixed order, mu_R = mu_F = H_T/2, 14 TeV), N_IC = 2 (STR l.151),
from outputs/s2/kfactors.json (campaigns p2-b-s2-kscan, p2-b-s2-kscan-p4l).  Errors as printed by aMC@NLO's run summary:
scale = envelope of 9 (mu_R, mu_F) values (the 7-point envelope of [SD11] is contained in it; the 9 individual values
were not kept), PDF = CT18NLO Hessian at 90 % C.L. or PDF4LHC21_40 symmetric Hessian at 68 % C.L. (retrieval_log #19),
integration error.  Nominal set: PDF4LHC21 ([SD11]: "the nominal is PDF4LHC21 if it installs"); CT18NLO is the variant.
Resummed cross-check: sigma_NLO x R(m), R = sigma(NLO+NLL)/sigma(NLO) from Resummino 3.1.2 for ~e_R pairs (scalar),
squarks and gluino decoupled, same PDF set, Resummino's central scale (m1 + m2)/2 (campaign p2-b-s2-nll).  The public
WG tables give NLO+NLL only (no NLO column, retrieval_log #16), so the ratio cannot be taken from them; Resummino is the
code that produced those tables.  For the fermion E the scalar's R is applied (assumption, flagged): no public code
ships the NLO+NLL for a colour-singlet fermion pair of this kind.
Usage: python3 -I sigma_norm_table.py <out.json>
"""
import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marker_files import done_outputs  # noqa: E402

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('sigma_norm')
HERE = os.path.dirname(os.path.abspath(__file__))
KF = os.path.join(HERE, '..', '..', 'outputs', 's2', 'kfactors.json')
N_IC = 2
SETS = (('93100', 'PDF4LHC21_40', '68 % C.L. (symmhessian)'), ('14400', 'CT18NLO', '90 % C.L. (hessian)'))


def nll_ratios():
    """{(pdf_name, mass): dict(R, lo, nlo, nll)} from the done outputs of p2-b-s2-nll."""
    out = {}
    for f in done_outputs('p2-b-s2-nll', suffix='.json'):
        d = json.load(open(f))
        by_m = {}
        for p in d['points']:
            by_m.setdefault(p['mass'], {}).update(p['results'])
        for m, r in by_m.items():
            if 'NLO' in r and 'NLO+NLL' in r:
                out[(d.get('pdf', 'CT18NLO'), m)] = dict(R=r['NLO+NLL'][0] / r['NLO'][0], nlo_pb=r['NLO'], nll_pb=r['NLO+NLL'],
                                                         lo_pb=r.get('LO'), source=os.path.basename(f))
    return out


def main():
    out = sys.argv[1]
    kf = json.load(open(KF))['results']
    R = nll_ratios()
    res = dict(definition=__doc__.split('Usage')[0], n_ic=N_IC, tables={})
    for spin in ('E', 'S'):
        for lhaid, name, cl in SETS:
            key = f'{spin}_{lhaid}'
            rows = []
            for m in sorted(kf[key], key=int):
                x = kf[key][m]
                s = N_IC * x['sigma_nlo_pb'] * 1e3
                rr = R.get((name, int(m)))
                rows.append(dict(mass=int(m), sigma_nlo_pb_NIC1=x['sigma_nlo_pb'], sigma_norm_fb=s,
                                 int_err_pct=100 * x['err_nlo'] / x['sigma_nlo_pb'],
                                 scale9_up_pct=x['nlo_scale_up_pct'], scale9_dn_pct=x['nlo_scale_dn_pct'],
                                 pdf_up_pct=x['nlo_pdf_up_pct'], pdf_dn_pct=x['nlo_pdf_dn_pct'], K=x['K'], K_err=x['K_err'],
                                 R_nllnlo_scalar=rr['R'] if rr else None,
                                 sigma_norm_resummed_fb=s * rr['R'] if rr else None))
            res['tables'][key] = dict(spin=spin, pdf=name, pdf_cl=cl, nominal=(lhaid == '93100'), rows=rows)
            for r in rows:
                log.info('%s %s m=%4d sigma_norm=%.5g fb  scale +%.1f/-%.1f %%  pdf +%.1f/-%.1f %%  R=%s', spin, name, r['mass'],
                         r['sigma_norm_fb'], r['scale9_up_pct'], r['scale9_dn_pct'], r['pdf_up_pct'], r['pdf_dn_pct'],
                         None if r['R_nllnlo_scalar'] is None else round(r['R_nllnlo_scalar'], 4))
    # set-to-set comparison of the central values (E only, every mass)
    cmp_ = []
    for m in sorted(kf['E_93100'], key=int):
        a, b = kf['E_93100'][m]['sigma_nlo_pb'], kf['E_14400'][m]['sigma_nlo_pb']
        cmp_.append(dict(mass=int(m), p4l_over_ct18=a / b))
    res['E_set_ratio'] = cmp_
    res['nll_points'] = {f'{k[0]}_{k[1]}': v for k, v in sorted(R.items())}
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
