"""kscan_eval.py -- S2-b: K(m) = sigma_NLO / sigma_LO (fixed order, aMC@NLO, loop_quirkE), with the NLO 9-point scale
envelope and the PDF uncertainty as printed by aMC@NLO's summary (reweight_PDF), per mass and PDF set.
Input: campaign p2-b-s2-kscan (and p2-b-s2-kscan-p4l if it exists), JSON per job.
Output: ../../outputs/s2/kfactors.json.  K error: from the two independent MC integration errors.
Run (light, stdlib): python3 -I kscan_eval.py
"""
import glob
import json
import logging
import math
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger('kscan_eval')
DATA = Path('/nfs/cajuela/jdochoa/quirks_v2/data')
OUT = Path(__file__).resolve().parents[2] / 'outputs' / 's2'


def main():
    res = {}
    for camp in ('p2-b-s2-kscan', 'p2-b-s2-kscan-p4l'):
        for f in sorted(glob.glob(str(DATA / camp / '*' / '*.json'))):
            d = json.load(open(f))
            key = f"{d['spin']}_{d['lhaid']}"
            pts = {}
            for p in d['points']:
                pts.setdefault(p['mass'], {})[p['order']] = p
            for m, o in pts.items():
                if 'LO' not in o or 'NLO' not in o:
                    continue
                lo, nlo = o['LO'], o['NLO']
                k = nlo['sigma_pb'] / lo['sigma_pb']
                ek = k * math.hypot(nlo['err_pb'] / nlo['sigma_pb'], lo['err_pb'] / lo['sigma_pb'])
                res.setdefault(key, {})[m] = dict(
                    sigma_lo_pb=lo['sigma_pb'], err_lo=lo['err_pb'], sigma_nlo_pb=nlo['sigma_pb'], err_nlo=nlo['err_pb'],
                    K=round(k, 4), K_err=round(ek, 4), nlo_scale_up_pct=nlo.get('scale_up_pct'),
                    nlo_scale_dn_pct=nlo.get('scale_dn_pct'), nlo_pdf_up_pct=nlo.get('pdf_up_pct'),
                    nlo_pdf_dn_pct=nlo.get('pdf_dn_pct'), lo_scale_up_pct=lo.get('scale_up_pct'),
                    lo_scale_dn_pct=lo.get('scale_dn_pct'), job=Path(f).stem, cpu_s_nlo=nlo.get('cpu_s'))
    for key in res:
        res[key] = dict(sorted(res[key].items()))
        for m, r in res[key].items():
            log.info('%s m=%d K=%.4f+-%.4f scale %+s/%s %% pdf %s/%s %%', key, m, r['K'], r['K_err'],
                     r['nlo_scale_up_pct'], r['nlo_scale_dn_pct'], r['nlo_pdf_up_pct'], r['nlo_pdf_dn_pct'])
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(dict(definition='K = sigma_NLO(QCD, fixed order) / sigma_LO(fixed order), same model loop_quirkE, '
                              'mu_R = mu_F = H_T/2 (dynamical_scale_choice -1), 14 TeV, N_IC = 1',
                   tag='VERIFIED (computed, campaign p2-b-s2-kscan)', results=res), open(OUT / 'kfactors.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
