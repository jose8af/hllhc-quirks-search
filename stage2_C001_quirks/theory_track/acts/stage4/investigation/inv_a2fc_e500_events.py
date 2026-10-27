"""INV_A2FC_E500 step 2: event-level comparison A2 (numpy) vs A2FC (full chain) at a revert point.
For every row: the matched (pre-declared match) candidates with f_CKF < 0.2, their in-job ladder flags and the
core quantities (w_core, p_chi2core, n_core, n_q_core, quirk-hit chi2 share), plus sig.tab bookkeeping
(n_q_written, n_q_ckf, n_q_pool).  Read-only.
usage: python inv_a2fc_e500_events.py F 500 3   -> data/acts_stage4/investigation/inv_a2fc_e500_events_F500_L3.json"""
import json
import sys
from pathlib import Path

import numpy as np

TT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TT))
from acts.stage4.analysis import common as C  # noqa: E402
from acts.stage4.analysis import hitrec as HR  # noqa: E402

OUT = TT / 'data/acts_stage4/investigation'
PREFIX = ('sig.', 'cand.', 'hit.', 'trials.', 'job_id', 'complete', 'chain.')


def per_file(path, lam):
    d = C.load_npz(path, prefix=PREFIX)
    tab = d['sig.tab']; ci = {str(c): i for i, c in enumerate(d['sig.cols'])}
    lk = HR.cand_lookup(d)
    Fc = C.rung_flags(d['cand.rungs'])
    trials_of = {}
    for k, tr, cidx, h in HR.iter_records(d):
        i = lk[(tr, cidx)]
        pv = d['trials.pv'][tr]
        g = HR.geom(d, h, pv, d['cand.normal'][i], d['cand.axis'][i])
        cm, c, w = HR.core(g)
        mt, nc, nq, nl = HR.signal_match(d, h, g, cm)
        if not mt:
            continue
        q = (d['hit.INT'][h].astype(np.int64) % 1_000_000) == C.SIG_VP
        # per-hit normalised residual in the core about the centre (diagnostic of the chi2_core inputs)
        r = (g['wv'] - c) / np.maximum(g['s_n2'], 1e-6)
        trials_of.setdefault(tr, []).append(dict(
            cand=int(i), F=[int(x) for x in np.where(Fc[i][:14])[0]], f_ckf=float(d['cand.f_ckf'][i]),
            w_core=float(d['cand.dw_core'][i]), p_chi2core=float(d['cand.p_chi2core'][i]),
            chi2_core=float(d['cand.chi2_core'][i]), n_core=nc, n_q_core=nq, n_pu_core=int((~q & cm).sum()),
            n_q_layers=nl, nip2=int(d['cand.nip2'][i]), n2s2=int(d['cand.n2s2'][i]), nhit=int(d['cand.nhit'][i]),
            chi2_q_core=float(np.sum(r[q & cm] ** 2)), chi2_pu_core=float(np.sum(r[~q & cm] ** 2)),
            med_abs_r_q=float(np.median(np.abs(r[q & cm]))) if (q & cm).any() else None,
            s_n2_q_med=float(np.median(g['s_n2'][q & cm])) if (q & cm).any() else None,
            w_q_ip=float(1.4826 * np.median(np.abs(g['wv'][q & g['ip']] - np.median(g['wv'][q & g['ip']]))))
            if (q & g['ip']).sum() > 2 else None,
            n_q_ip=int((q & g['ip']).sum()), n_pu_ip=int((~q & g['ip']).sum()),
            normal=[float(x) for x in d['cand.normal'][i]], axis=[float(x) for x in d['cand.axis'][i]]))
    out = {}
    for e in range(len(tab)):
        if abs(float(tab[e, ci['lam']]) - lam) > 1e-9:
            continue
        row = int(tab[e, ci['row']]); ti = int(d['sig.trial'][e])
        ents = [x for x in trials_of.get(ti, []) if x['f_ckf'] < 0.2] if ti >= 0 else []
        out[row] = dict(trial=ti, status=int(tab[e, ci['status']]), probe_excluded=int(tab[e, ci['probe_excluded']]),
                        n_q_written=int(tab[e, ci['n_q_written']]), n_q_ckf=int(tab[e, ci['n_q_ckf']]),
                        n_q_pool=int(tab[e, ci['n_q_pool']]), n_q_road=int(tab[e, ci['n_q_road']]),
                        n_cand_q=int(tab[e, ci['n_cand_q']]),
                        pv=[float(x) for x in d['trials.pv'][ti]] if ti >= 0 else None,
                        n_ckf_hits=int(d['trials.n_ckf_hits'][ti]) if ti >= 0 else None,
                        matched=ents)
    return out


def main():
    spin, m, lam = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    a2 = [j for j in C.manifest('C1') if j['sample'] == 'A2' and j['spin'] == spin and int(j['m']) == m]
    fc = {j['paired_a2_id']: j for j in C.manifest('A2FC') if j['point'].startswith(f'p2/{spin}_m{m}/L{lam:g}_')}
    res = dict(point=f'{spin}{m} L{lam:g}', n_a2_jobs=len(a2), n_fc_jobs=len(fc), rows={})
    for j in sorted(a2, key=lambda x: x['chunk']):
        jf = fc[j['id']]
        assert jf['rows'] == j['rows'] and jf['seed'] == j['seed'], j['id']
        A = per_file(C.PROD.joinpath(*j['out'].split('/')), lam)
        Fd = per_file(C.PROD.joinpath(*jf['out'].split('/')), lam)
        for r in j['rows']:
            res['rows'][r] = dict(job=j['id'], a2=A.get(r), fc=Fd.get(r))
        print(j['id'], 'done', flush=True)
    p = OUT / f'inv_a2fc_e500_events_{spin}{m}_L{lam:g}.json'
    p.write_text(json.dumps(res, indent=0))
    print('->', p)


if __name__ == '__main__':
    main()
