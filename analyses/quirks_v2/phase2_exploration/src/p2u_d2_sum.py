"""p2u_d2_sum.py -- D2 robustness row "later arcs restored": the pre-declared reading (plan
outputs/D2_PLAN_ulrika_2026-11-19.md §2, §3, §6).

  <tt python> p2u_d2_sum.py <out.json> --nom-camp p2-a-c1-pu1 --nom-jobs 0 30 --var-camp p2-c-d2-find [--nboot 2000]

r(R) = sum over the paired trials of n_grp,var(R) / n_grp,nom(R) at R04, R05, R06 ([SD4] count: trials.n_grp), with
the event-level (clustered) bootstrap: the same event resample for both arms and all rungs (joint replicas), 2,000
replicas, fixed seed; unpaired bootstrap and Poisson widths beside it.  Additional readings without a verdict: (a)
varied candidates at R04-R06 with a sensor holding two hits of one particle at least one of which is injected (from
the stored hit records), (b) r at N_2S2 >= 1, 2, 3 on top of R04-R06 (groups recounted from the candidate records).
Reads only pile-up files (no signal file).
"""
import argparse
import json
import logging
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
QV2 = HERE.parents[1]
MARK = QV2 / 'ledger' / 'markers'
log = logging.getLogger('p2u_d2_sum')
RUNG = dict(R04=3, R05=4, R06=5)
SEED = 20261119


def done_paths(camp):
    out = {}
    for p in sorted((MARK / camp).glob('*/*.marker')):
        done = None
        for line in p.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('status') == 'done':
                done = d
        if done:
            for o in done['outputs']:
                out[o['name']] = (o['path'], done.get('cpu_s'), done.get('max_rss_mb'))
    return out


def recount(z, ev_ids):
    """Per event: n_grp at R04-R06 from trials, and the group recount from candidate records for k = 0..3 (n2s2 >= k)."""
    tev = z['trials.ev']; ng = z['trials.n_grp'][:, [3, 4, 5]].astype(np.int64)
    ctr = z['cand.trial']; cg = z['cand.group'].astype(np.int64); n2 = z['cand.n2s2'].astype(np.int64)
    bits = np.unpackbits(z['cand.rungs'], axis=1)[:, :43].astype(bool)
    E = {e: i for i, e in enumerate(ev_ids)}
    A = np.zeros((len(ev_ids), 3), np.int64)
    np.add.at(A, np.array([E[int(e)] for e in tev]), ng)
    B = np.zeros((len(ev_ids), 4, 3), np.int64)          # [event, k, rung]
    for kk in range(4):
        for j, col in enumerate((3, 4, 5)):
            m = bits[:, col] & (cg >= 0) & (n2 >= kk)
            pairs = np.unique(np.c_[ctr[m], cg[m]], axis=0) if m.any() else np.zeros((0, 2), np.int64)
            if len(pairs):
                np.add.at(B[:, kk, j], np.array([E[int(tev[t])] for t in pairs[:, 0]]), 1)
    return A, B


def truth_a(z, inj_avail):
    """(a): candidates with a full hit record passing R04 / R05 / R06 that have a sensor with >= 2 hits of one particle
    (same INT, vsec, particle, generation 0), at least one injected.  Returns counts of (candidates, groups) per rung and
    the number of hit-recorded candidates per rung."""
    res = {r: dict(n_cand_with_record=0, n_cand_double_one_injected=0, n_cand_double_same_particle_any=0,
                   groups_double_one_injected=0) for r in RUNG}
    if 'hit.cand' not in z.files:
        return res
    htr = z['hit.trial']; hc = z['hit.cand']; off = z['hit.off']; ref = z['hit.ref']
    sid = z['hit.sid'].astype(np.int64); INT = z['hit.INT']; par = z['hit.particle'].astype(np.int64); gen = z['hit.gen']
    inj = z['hit.inj'] if inj_avail else np.zeros(len(sid), bool)
    vs = z['hit.vsec'].astype(np.int64) if inj_avail else np.zeros(len(sid), np.int64)
    ctr = z['cand.trial']; cid = z['cand.idx']; cg = z['cand.group']
    bits = np.unpackbits(z['cand.rungs'], axis=1)[:, :43].astype(bool)
    look = {(int(t), int(c)): k for k, (t, c) in enumerate(zip(ctr, cid))}
    seen = {r: set() for r in RUNG}
    for h in range(len(hc)):
        k = look[(int(htr[h]), int(hc[h]))]
        rows = ref[off[h]:off[h + 1]]
        keyrows = {}
        for q in rows:
            if gen[q] != 0 or par[q] < 0:
                continue
            keyrows.setdefault((int(sid[q]), int(INT[q]), int(vs[q]), int(par[q])), []).append(q)
        dbl_any = any(len(v) >= 2 for v in keyrows.values())
        dbl_inj = any(len(v) >= 2 and bool(np.any(inj[v])) for v in keyrows.values())
        for r, col in RUNG.items():
            if bits[k, col]:
                res[r]['n_cand_with_record'] += 1
                res[r]['n_cand_double_same_particle_any'] += int(dbl_any)
                if dbl_inj:
                    res[r]['n_cand_double_one_injected'] += 1
                    seen[r].add((int(ctr[k]), int(cg[k])))
    for r in RUNG:
        res[r]['groups_double_one_injected'] = len(seen[r])
    return res


def boot(Nn, Nv, nboot, rng):
    """Joint paired event bootstrap of ln(sum Nv / sum Nn) for every column; also the unpaired one."""
    E = len(Nn)
    est = np.log(Nv.sum(0) / Nn.sum(0))
    P = np.empty((nboot, Nn.shape[1])); U = np.empty((nboot, Nn.shape[1]))
    for b in range(nboot):
        i = rng.integers(0, E, E); j = rng.integers(0, E, E)
        with np.errstate(divide='ignore', invalid='ignore'):
            P[b] = np.log(Nv[i].sum(0) / Nn[i].sum(0))
            U[b] = np.log(Nv[j].sum(0) / Nn[i].sum(0))
    return est, P, U


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', stream=sys.stderr)
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--nom-camp', default='p2-a-c1-pu1')
    ap.add_argument('--nom-jobs', type=int, nargs=2, default=(0, 30)); ap.add_argument('--var-camp', default='p2-c-d2-find')
    ap.add_argument('--chain-camp', default='p2-c-d2-chain'); ap.add_argument('--nboot', type=int, default=2000)
    a = ap.parse_args()
    nom = done_paths(a.nom_camp); var = done_paths(a.var_camp); ch = done_paths(a.chain_camp)
    Nn, Nv, Bn, Bv, ev_all = [], [], [], [], []
    pair_bad = 0; ta = None; lay = []; evst = []; chain_ev = []; chain_meta = []
    for K in range(*a.nom_jobs):
        nid = f'c1pu1-{K:04d}'
        zn = np.load(nom[f'{nid}.npz'][0])
        vparts = [var[f'p2-c-d2-find-{K:04d}-{h}.npz'][0] for h in ('a', 'b')]
        zvs = [np.load(p) for p in vparts]
        ev_ids = sorted(set(int(e) for e in zn['trials.ev']))
        A, B = recount(zn, ev_ids)
        Nn.append(A); Bn.append(B)
        Av = np.zeros_like(A); Bvv = np.zeros_like(B)
        for zv in zvs:
            evv = sorted(set(int(e) for e in zv['trials.ev']))
            a_, b_ = recount(zv, evv)
            idx = [ev_ids.index(e) for e in evv]
            Av[idx] += a_; Bvv[idx] += b_
            # pairing: same (ev, road) -> same pv, phimet, trial seed
            tn = {(int(e), int(r)): k for k, (e, r) in enumerate(zip(zn['trials.ev'], zn['trials.road']))}
            for k, (e, r) in enumerate(zip(zv['trials.ev'], zv['trials.road'])):
                j = tn[(int(e), int(r))]
                if not (zn['trials.trial_seed'][j] == zv['trials.trial_seed'][k] and np.array_equal(zn['trials.pv'][j], zv['trials.pv'][k])
                        and zn['trials.phimet'][j] == zv['trials.phimet'][k]):
                    pair_bad += 1
            t = truth_a(zv, True)
            ta = t if ta is None else {r: {q: ta[r][q] + t[r][q] for q in ta[r]} for r in RUNG}
            lay.append(zv['d2.layer']); evst.append(zv['d2.evstats'])
        Nv.append(Av); Bv.append(Bvv); ev_all += ev_ids
        zc = np.load(ch[f'p2-c-d2-chain-{K:04d}.npz'][0])
        chain_ev.append(zc['evs']); chain_meta.append(json.loads(str(zc['meta'])))
        log.info('job %s: nominal %s varied %s', nid, A.sum(0).tolist(), Av.sum(0).tolist())
    Nn = np.concatenate(Nn); Nv = np.concatenate(Nv); Bn = np.concatenate(Bn); Bv = np.concatenate(Bv)
    # recount check: k = 0 group recount equals trials.n_grp in both arms
    rc_ok = bool(np.array_equal(Bn[:, 0, :], Nn) and np.array_equal(Bv[:, 0, :], Nv))
    cols = ['R04', 'R05', 'R06'] + [f'{r}&2S2>={k}' for k in (1, 2, 3) for r in ('R04', 'R05', 'R06')]
    Xn = np.c_[Nn, Bn[:, 1:, :].reshape(len(Nn), -1)].astype(float)
    Xv = np.c_[Nv, Bv[:, 1:, :].reshape(len(Nv), -1)].astype(float)
    rng = np.random.default_rng(SEED)
    est, P, U = boot(Xn, Xv, a.nboot, rng)
    ntr = 4 * len(Nn)
    rows = {}
    for j, c in enumerate(cols):
        okP = np.isfinite(P[:, j]); okU = np.isfinite(U[:, j])
        rows[c] = dict(B_nom_sum=float(Xn[:, j].sum()), B_var_sum=float(Xv[:, j].sum()), n_trials=ntr,
                       B_nom_per_trial=float(Xn[:, j].sum() / ntr), B_var_per_trial=float(Xv[:, j].sum() / ntr),
                       r=float(math.exp(est[j])) if np.isfinite(est[j]) else None, ln_r=float(est[j]),
                       s_ln_paired_boot=float(np.std(P[okP, j], ddof=1)) if okP.sum() > 1 else None,
                       s_ln_unpaired_boot=float(np.std(U[okU, j], ddof=1)) if okU.sum() > 1 else None,
                       s_ln_poisson=float(math.sqrt(1 / Xn[:, j].sum() + 1 / Xv[:, j].sum())) if Xn[:, j].sum() > 0 and Xv[:, j].sum() > 0 else None,
                       n_boot_dropped=int((~okP).sum()))
    tr = P[:, 2] - P[:, 0]
    trend = dict(d=float(est[2] - est[0]), s_paired_boot=float(np.std(tr[np.isfinite(tr)], ddof=1)))
    trend['z'] = trend['d'] / trend['s_paired_boot']
    # pre-declared reading (ADD1 v5 §1.5, copied in the plan §6)
    lr = {r: rows[r]['ln_r'] for r in RUNG}; s = {r: rows[r]['s_ln_paired_boot'] for r in RUNG}
    evaluated = s['R06'] < 0.1
    no_effect = all(abs(lr[r]) <= 0.1 and abs(lr[r]) <= 2 * s[r] for r in RUNG) and abs(trend['z']) <= 2
    not_robust = any(abs(lr[r]) > math.log(2) for r in RUNG) or trend['z'] > 2
    verdict = 'no effect' if no_effect else ('effect, not robust' if not_robust else 'effect, robust')
    correction = (verdict == 'effect, robust' and lr['R06'] > 0)
    L = np.concatenate(lay); EVS = np.concatenate(evst); CE = np.concatenate(chain_ev)
    lay_cols = ['ev', 'layer', 'n_inj', 'n_inj_outer', 'n_topup_cross', 'n_dropped', 'excess']
    by_layer = {}
    from_layers = ['TBPX_L1', 'TBPX_L2', 'TBPX_L3', 'TBPX_L4', 'TBPS_L1', 'TBPS_L2', 'TBPS_L3', 'TB2S_L1', 'TB2S_L2', 'TB2S_L3']
    for li, nm in enumerate(from_layers):
        m = L[:, 1] == li
        by_layer[nm] = {c: float(L[m, k].mean()) for k, c in enumerate(lay_cols) if k >= 2}
        by_layer[nm]['events_with_excess'] = int(np.sum(L[m, 6] > 0))
    ecols = chain_meta[0]['evs_cols']
    res = dict(rows=rows, trend_R06_minus_R04=trend, n_events=int(len(Nn)), n_trials=ntr, n_boot=a.nboot, boot_seed=SEED,
               pairing_mismatched_trials=pair_bad, group_recount_equals_n_grp=rc_ok,
               reading=dict(evaluated_B6a=bool(evaluated), no_effect=bool(no_effect), not_robust=bool(not_robust), verdict=verdict,
                            b6d_correction_applies=bool(correction),
                            b6d_factor=rows['R06']['r'] if correction else None,
                            b6d_factor_s_ln=rows['R06']['s_ln_paired_boot'] if correction else None),
               truth_a_varied=ta, layers_mean_per_event=by_layer,
               chain_per_event_mean={c: float(CE[:, k].mean()) for k, c in enumerate(ecols)},
               chain_nominal_match_all=bool(all(m['nominal_match_all'] for m in chain_meta)),
               chain_ckf_flag_changed_total=int(sum(m['n_ckf_flag_changed'] for m in chain_meta)),
               chain_v41_ok_all=bool(all(m['v41_ok_all'] for m in chain_meta)),
               finder_evstats_mean={c: float(EVS[:, k].mean()) for k, c in enumerate(['ev', 'n_fatras', 'n_inj_barrel', 'n_topup', 'n_ckf_removed',
                                                                                     'n_pool', 'n_merged_groups', 'n_merged_hits',
                                                                                     'n_sigma_enlarged', 'n_inj_pool'])},
               cpu_s=dict(chain=float(sum(v[1] or 0 for k, v in ch.items())), finder=float(sum(v[1] or 0 for k, v in var.items())),
                          nominal_jobs=float(sum(nom[f'c1pu1-{K:04d}.npz'][1] for K in range(*a.nom_jobs)))))
    Path(a.out + '.tmp').write_text(json.dumps(res, indent=1, default=str))
    Path(a.out + '.tmp').replace(a.out)
    log.info('%s', json.dumps(dict(rows={c: (rows[c]['r'], rows[c]['s_ln_paired_boot']) for c in cols}, trend=trend,
                                   reading=res['reading'])))


if __name__ == '__main__':
    main()
