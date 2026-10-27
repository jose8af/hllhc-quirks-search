"""A2FC <-> A2 pairing check (read-only on prod/).  usage: a2fc_pairing.py JOB_ID [JOB_ID ...] [--rerun]

Per A2FC job vs its paired A2 job (jobs/A2FC.json 'paired_a2_id'):
  1. rows / event order: A2FC sig.tab rows == A2 sig.tab rows at the same Lambda (same order = same ACTS event numbers);
  2. seeds: A2FC chain job_seed == A2 chain job_seed; A2 chain event_seeds == hseed('sigpu', spin, m, row) of the A2FC
     rows (the seeds run_chain.py sig uses); PV/MET/top-up/trial seeds are row-keyed (identical by construction);
  3. PU content per event: A2 chain.v41 n_simhits / n_particles_in == A2FC (n_simhits - n_sig_simhits) / n_particles_in;
  4. PU measurements: IT PU hits of the A2 stored hit records vs the nearest A2FC IT PU measurement of the same event
     (re-smeared, so ~ resolution, not 0); PU BTL row counts (positions re-smeared);
  5. (--rerun) re-run the A2 PU-only chain (run_chain.py pu, A2 job seed, A2 event seeds) into the scratch dir and
     compare its PU measurements with the A2FC dump (non-quirk rows): sid, truth (tru), barcode, xyz.
Writes data/acts_stage4/investigation/a2fc_pairing_<JOB>.json."""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np

from acts.stage4 import run_stage4 as RS, run_g1b as RG
from acts.stage4.code import s4sig as S

OUT = RS.TT / 'data/acts_stage4/investigation'
jobs = {j['id']: j for j in json.loads((RS.JOBS / 'A2FC.json').read_text())['jobs']}
c1 = {j['id']: j for j in json.loads((RS.JOBS / 'C1.json').read_text())['jobs']}
SIG = 4000


def check(jid, rerun):
    j = jobs[jid]; a = c1[j['paired_a2_id']]
    zf = np.load(RS.out_path(j)); za = np.load(RS.out_path(a))
    mf = json.loads(str(zf['meta_json'])); ma = json.loads(str(za['meta_json']))
    res = dict(job=jid, a2=a['id'], lam=j['lam'])
    cf = [str(c) for c in zf['sig.cols']]; ci = {c: i for i, c in enumerate(cf)}
    tf = zf['sig.tab']; ta = za['sig.tab']
    ra = [int(r) for r in ta[np.isclose(ta[:, ci['lam']], j['lam'])][:, ci['row']]]
    rf = [int(r) for r in tf[:, ci['row']]]
    res['rows_equal'] = rf == ra == a['rows']
    res['job_seed_equal'] = int(mf['chain_meta']['job_seed']) == int(ma['chain_meta']['job_seed']) == int(a['seed'])
    spin, m = a['spin'], float(S.Point(j['point']).m)
    res['pu_event_seeds_equal'] = [int(x) for x in ma['chain_meta']['event_seeds']] == \
        [int(S.hseed('sigpu', spin, m, r, mod=2 ** 62)) for r in rf]
    vc = [str(c) for c in zf['chain.v41_cols']]; vi = {c: i for i, c in enumerate(vc)}
    vf = zf['chain.v41']; va = za['chain.v41']
    res['pu_simhits_A2'] = va[:, vi['n_simhits']].astype(int).tolist()
    res['pu_simhits_A2FC'] = (vf[:, vi['n_simhits']] - vf[:, vi['n_sig_simhits']]).astype(int).tolist()
    res['pu_simhits_equal'] = res['pu_simhits_A2'] == res['pu_simhits_A2FC']
    res['particles_in_equal'] = va[:, vi['n_particles_in']].tolist() == vf[:, vi['n_particles_in']].tolist()
    # 4. PU hits of the A2 stored records vs the A2FC dumps (same event index): nearest A2FC PU measurement on the
    #    same surface kind.  Exact equality is NOT expected (ACTS re-draws the smearing once quirk SimHits are in the
    #    event; the records also contain top-up hits, which are not in the chain dump); IT distances ~ resolution.
    from scipy.spatial import cKDTree
    tev = za['trials.ev']; off = za['hit.off']; ref = za['hit.ref']; ht = za['hit.trial']
    dd = []
    for ie in range(j['n_events']):
        k = f'dump.{ie}_0.'
        mm = (zf[k + 'vp'] != SIG) & (S.KIND[zf[k + 'sid'].astype(int)] == 'IT')
        tree = cKDTree(zf[k + 'xyz'][mm])
        rs_ = [r for r in range(len(ht)) if int(tev[int(ht[r])]) == ie]
        if not rs_:
            continue
        h = np.unique(np.concatenate([ref[off[r]:off[r + 1]] for r in rs_]))
        h = h[((za['hit.INT'][h] % 1_000_000) != SIG) & (S.KIND[za['hit.sid'][h].astype(int)] == 'IT')]
        if len(h):
            dd.append(tree.query(za['hit.xyz'][h].astype(np.float64))[0])
    dd = np.concatenate(dd) if dd else np.zeros(0)
    res['a2_record_IT_pu_hits'] = int(len(dd))
    res['a2_record_IT_pu_nn_dist_um_q10_50_90'] = (np.quantile(dd, [0.1, 0.5, 0.9]) * 1e3).round(1).tolist() if len(dd) else None
    bc = [str(c) for c in za['btl_cols']]
    ba = za['btl']; bf = zf['btl']
    bi = bc.index('INT') if 'INT' in bc else -1
    bfp = bf[(bf[:, bi] % 1_000_000) != SIG] if bi >= 0 else bf
    res['btl_cols'] = bc
    res['pu_btl_rows'] = [len(ba), len(bfp)]
    res['pu_btl_identical'] = bool(len(ba) == len(bfp) and np.array_equal(
        np.sort(np.round(ba, 5), axis=0), np.sort(np.round(bfp, 5), axis=0)))
    if rerun:
        sc = Path(tempfile.mkdtemp(prefix='a2fc_pair_'))
        seeds = [S.hseed('sigpu', spin, m, r, mod=2 ** 62) for r in a['rows']]
        sf = sc / 'seeds.json'; sf.write_text(json.dumps(seeds))
        tmp = sc / 'pu.npz'
        RG.chain(a, tmp, ['pu', tmp, len(a['rows']), a['seed'], '--event-seeds', sf])
        zp = np.load(tmp)
        per = []
        for ie in range(j['n_events']):
            ep = zp[f'ev{ie}']; tp = zp[f'tru{ie}']
            k = f'dump.{ie}_0.'
            vp = zf[k + 'vp']; m_ = vp != SIG
            ef = np.c_[zf[k + 'sid'], zf[k + 'xyz']][m_]; tf_ = zf[k + 'tru'][m_]
            pf = np.c_[zf[k + 'particle'], zf[k + 'vp'], zf[k + 'gen'], zf[k + 'vsec']][m_]
            pp = np.c_[ep[:, 8], ep[:, 7], ep[:, 9], ep[:, 10]]
            ka = np.lexsort(np.c_[ep[:, 0], np.round(tp, 4), pp].T[::-1])
            kf = np.lexsort(np.c_[ef[:, 0], np.round(tf_, 4), pf].T[::-1])
            same_n = len(ep) == len(ef)
            d = dict(ev=ie, n_pu_meas_rerun=len(ep), n_pu_meas_A2FC=int(m_.sum()))
            if same_n:
                d['sid_equal'] = bool(np.array_equal(ep[ka, 0], ef[kf, 0]))
                d['truth_maxdiff'] = float(np.max(np.abs(tp[ka].astype(float) - tf_[kf].astype(float))))
                d['barcode_equal'] = bool(np.array_equal(pp[ka].astype(np.int64), pf[kf].astype(np.int64)))
                d['xyz_maxdiff_mm'] = float(np.max(np.abs(ep[ka, 1:4] - ef[kf, 1:4])))
                d['xyz_identical_frac'] = float(np.mean(np.all(np.abs(ep[ka, 1:4] - ef[kf, 1:4]) < 1e-6, axis=1)))
            per.append(d)
        res['rerun_pu_chain'] = per
        zp.close()
    zf.close(); za.close()
    print(json.dumps(res, default=str, indent=1))
    (OUT / f'a2fc_pairing_{jid}.json').write_text(json.dumps(res, default=str, indent=1))


if __name__ == '__main__':
    rr = '--rerun' in sys.argv
    for jid in [x for x in sys.argv[1:] if not x.startswith('--')]:
        check(jid, rr)
