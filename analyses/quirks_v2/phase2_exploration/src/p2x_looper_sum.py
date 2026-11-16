"""p2x_looper_sum.py -- summary of the proper looper gun (campaign p2-c-px-lp): counts of v1's own job outputs per rung,
the funnel of the frozen finder, candidate variables where candidates exist, Geant4 truth of the particles and the
times of the arcs after half a turn.  No signal quantity.

  <tt or acts python> p2x_looper_sum.py <out.json> <dir with <id>.npz, <id>.truth.npz>
"""
import glob
import json
import sys
from pathlib import Path

import numpy as np

N_TRIG = 4.0848e7            # STR l.200 (v1 AN1/bsum_wp.json n_trig), as used in addendum 1


def q(a, ps=(0.1, 0.5, 0.9, 0.99)):
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    return [float(x) for x in np.quantile(a, ps)] if len(a) else None


def one_set(files):
    R = None; tot = dict(events=0, trials=0, seed=0, refit=0, kept=0, ip2ge6=0, ip2ge7=0, skipped=0, with_cand=0, attr=0, attr_rung=0)
    ev_pass = None; cand_pass = None; T = []; cfg = None; meta_chain = None; v41 = True
    best_nip2 = []; best_nit2 = []; best_n2s2 = []; best_nl2 = []; cand_rows = []; n_road = []; deep = []
    for f in files:
        z = np.load(f)
        m = json.loads(str(z['meta_json']))
        R = m['rungs']; cfg = m['finder_cfg']; meta_chain = m['chain_meta']; v41 &= bool(m.get('v41_pass'))
        E = z['cp.ev']; ec = [str(x) for x in z['cp.ev_cols']]
        tot['events'] += len(E); tot['skipped'] += int(E[:, ec.index('skipped')].sum())
        tot['with_cand'] += int((E[:, ec.index('n_cand')] > 0).sum()); tot['attr'] += int((E[:, ec.index('n_attr_all')] > 0).sum())
        tot['attr_rung'] += int((E[:, ec.index('n_attr_any')] > 0).sum())
        nt = int(z['n_trials']); tot['trials'] += nt
        if nt:
            npass = z['trials.n_pass']
            ev_pass = (npass > 0).sum(0) if ev_pass is None else ev_pass + (npass > 0).sum(0)
            cand_pass = npass.sum(0) if cand_pass is None else cand_pass + npass.sum(0)
            tot['seed'] += int((z['trials.n_trip'] > 0).sum()); tot['refit'] += int((z['trials.n_refit'] > 0).sum())
            tot['kept'] += int((z['trials.n_kept_all'] > 0).sum()); tot['ip2ge6'] += int((z['trials.n_ip2ge6'] > 0).sum())
            tot['ip2ge7'] += int((z['trials.n_ip2ge7'] > 0).sum()); n_road += z['trials.n_road'].tolist()
            for t in np.nonzero(npass[:, 3] > 0)[0]:
                deep.append(dict(file=Path(f).name, trial=int(t), ev=int(z['trials.ev'][t])))
            ck = [k for k in z.files if k.startswith('cand.')]
            if 'cand.trial' in z.files and len(z['cand.trial']):
                tr = z['cand.trial']
                for name, dst in (('cand.nip2', best_nip2), ('cand.nit2', best_nit2), ('cand.n2s2', best_n2s2), ('cand.nl2', best_nl2)):
                    if name in z.files:
                        v = z[name]
                        dst += [int(v[tr == t].max()) for t in np.unique(tr)]
                if len(cand_rows) < 40:
                    for i in range(min(len(tr), 40 - len(cand_rows))):
                        cand_rows.append({k[5:]: (float(z[k][i]) if np.ndim(z[k][i]) == 0 else None) for k in ck})
        T.append(np.load(f[:-4] + '.truth.npz'))
        z.close()
    cols = [str(x) for x in T[0]['cols']]
    X = np.concatenate([t['truth'] for t in T]); c = {k: i for i, k in enumerate(cols)}
    procs = {}
    for t in T:
        pc = json.loads(str(t['proc'])); inv = {v: k for k, v in pc.items()}
        for code, n in zip(*np.unique(t['truth'][:, c['end_proc']].astype(int), return_counts=True)):
            procs[inv[int(code)]] = procs.get(inv[int(code)], 0) + int(n)
    own = None
    if 'layer_cross' in T[0].files:
        # upper bounds from the particle's own crossings with NO plane requirement: a layer can be a double-crossing
        # layer of some ribbon only if the particle crosses it at least twice (IT: crossings; stacked OT: min(in, out)),
        # the counting rule of acts/stage4/finder/README.md "Seeds"
        L = np.concatenate([t['layer_cross'] for t in T]).astype(int)
        it2 = (L[:, :4] >= 2).sum(1)
        ps2 = sum((np.minimum(L[:, 4 + 2 * k], L[:, 5 + 2 * k]) >= 2).astype(int) for k in range(3))
        s2 = sum((np.minimum(L[:, 10 + 2 * k], L[:, 11 + 2 * k]) >= 2).astype(int) for k in range(3))
        ip2 = it2 + ps2
        n_ = len(L)
        own = dict(note='own crossings only, no plane, road or width requirement: an upper bound on every count',
                   N_IT2_max_hist_0_to_4=np.bincount(it2, minlength=5).tolist(), N_PS2_max_hist_0_to_3=np.bincount(ps2, minlength=4).tolist(),
                   N_2S2_max_hist_0_to_3=np.bincount(s2, minlength=4).tolist(), N_IP2_max_hist_0_to_7=np.bincount(ip2, minlength=8).tolist(),
                   frac_N_IT2_max_ge3=float((it2 >= 3).mean()),
                   frac_N_IT2_ge3_and_N_IP2_max_ge={str(k): float(((it2 >= 3) & (ip2 >= k)).mean()) for k in (4, 5, 6, 7)},
                   deficit_k_IP_at_R04_hist_0_to_7=np.bincount(np.maximum(0, 7 - ip2), minlength=8).tolist(), n=n_)
    nmeas = np.concatenate([t['n_meas'] for t in T]); nwr = np.concatenate([t['n_written'] for t in T])
    hist = lambda a, hi: np.bincount(np.clip(np.asarray(a, int), 0, hi), minlength=hi + 1).tolist()  # noqa: E731
    return dict(n_files=len(files), rungs=R[:14], finder_cfg=cfg, v41_pass_all=bool(v41), totals=tot,
                events_passing_rung=dict(zip(R[:14], [int(x) for x in (ev_pass[:14] if ev_pass is not None else [0] * 14)])),
                candidates_passing_rung=dict(zip(R[:14], [int(x) for x in (cand_pass[:14] if cand_pass is not None else [0] * 14)])),
                trials_passing_R04_or_deeper=deep[:100],
                funnel=dict(events=tot['events'], fewer_than_3_pool_hits=tot['skipped'], finder_run=tot['trials'],
                            with_seed_Tseed=tot['seed'], with_refit=tot['refit'], with_kept_candidate_NL2ge4=tot['kept'],
                            with_candidate_in_v1_record=tot['with_cand']),
                n_road_hits_q10_q50_q90_q99=q(n_road), best_candidate_per_event=dict(
                    n=len(best_nip2), N_IP2_hist_0_to_8=hist(best_nip2, 8) if best_nip2 else None,
                    N_IT2_hist_0_to_4=hist(best_nit2, 4) if best_nit2 else None,
                    N_2S2_hist_0_to_3=hist(best_n2s2, 3) if best_n2s2 else None, N_L2_hist_0_to_10=hist(best_nl2, 10) if best_nl2 else None),
                first_candidate_rows=cand_rows[:20],
                particles=dict(pt_q=q(X[:, c['pt']]), abs_eta_q=q(np.abs(X[:, c['eta']])),
                               pdg=dict(zip(*[[int(a) for a in u] for u in np.unique(X[:, c['pdg']].astype(int), return_counts=True)])) if False else
                               {str(int(a)): int(n) for a, n in zip(*np.unique(X[:, c['pdg']].astype(int), return_counts=True))},
                               end_process=procs, end_turn_q=q(X[:, c['end_turn']]), end_time_ns_q=q(X[:, c['end_t']]),
                               frac_alive_after_half_turn=float(np.mean(X[:, c['end_turn']] > 0.5)),
                               frac_alive_after_one_turn=float(np.mean(X[:, c['end_turn']] > 1.0))),
                crossings=dict(sensitive_all_per_event=float(X[:, c['n_cross_all']].mean()), injected_per_event=float(X[:, c['n_inj']].mean()),
                               counting_per_event=float(X[:, c['n_cross_counting']].mean()),
                               counting_after_half_turn_per_event=float(X[:, c['n_cross_counting_after_half_turn']].mean()),
                               events_with_crossing_after_half_turn=float(np.mean(X[:, c['n_cross_counting_after_half_turn']] > 0)),
                               measurements_per_event=float(nmeas.mean()), written_per_event=float(nwr.mean())),
                own_crossing_upper_bounds=own,
                arc_times_ns=dict(first_crossing_after_half_turn_q=q(X[:, c['t_first_after_half_turn']]),
                                  median_crossing_after_half_turn_q=q(X[:, c['t_median_after_half_turn']]),
                                  last_crossing_q=q(X[:, c['t_last']])),
                chain_meta={k: meta_chain.get(k) for k in ('looper_set', 'pool_rows', 'pool_interactions',
                                                            'loopers_prompt_central_per_mb_interaction', 'source')})


def main(out, d):
    res = {}
    for s in ('nat', 'flat'):
        files = sorted(f for f in glob.glob(f'{d}/*-{s}-*.npz') if not f.endswith('.truth.npz'))
        if files:
            res[s] = one_set(files)
    r = res.get('nat')
    if r:
        rate = r['chain_meta']['loopers_prompt_central_per_mb_interaction']
        aim = 0.2 / (2 * np.pi)          # the gun starts the particle within +-0.1 of the road axis
        nt = N_TRIG * 200 * rate * aim
        res['normalisation'] = dict(n_trig=N_TRIG, loopers_prompt_central_pt_below_0p63_per_mb_interaction=rate,
                                    fraction_starting_within_0p1_of_a_road_axis=aim, loopers_per_triggered_event=200 * rate * aim,
                                    N_t_in_3_ab=nt, events_per_count=nt / r['totals']['events'],
                                    zero_count_68pct_upper=1.14 * nt / r['totals']['events'],
                                    note='minimum-bias share only (x 200 interactions); N_trig of STR l.200')
    Path(out + '.tmp').write_text(json.dumps(res, indent=1, default=str))
    Path(out + '.tmp').replace(out)
    for s, r in res.items():
        sys.stderr.write(s + ' ' + json.dumps({k: v for k, v in r.items() if k not in ('first_candidate_rows',)}, default=str)[:3000] + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
