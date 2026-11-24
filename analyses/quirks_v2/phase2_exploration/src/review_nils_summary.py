"""review_nils_summary.py -- merge the five part JSONs of review_nils_subset.py (Nils, 2026-11-23).
  <tt python> -B review_nils_summary.py OUTDIR OUT.json [TODO.json]"""
import json, sys, glob
import numpy as np
d = [json.load(open(f)) for f in sorted(glob.glob(sys.argv[1] + '/part*.json'))]
assert len({x['script_sha256'] for x in d}) == 1
files = [f for x in d for f in x['files']]
assert sorted(f['gi'] for f in files) == list(range(460)), len(files)
path = {f['gi']: f['path'] for f in files}
full = {f['gi'] for f in files if f['full']}
E = np.array([e for x in d for e in x['events']])   # gi, ev, w, herS, herF, myS, myF, myH, n_road, nip2, nit2, wcore, n_ip, n_hit
bad = [[b[0], b[1], [y for y in b[2] if y[1] <= 3]] for x in d for b in x['bad']]
bad = [b for b in bad if b[2]]
Z = E[:, 2] >= 0.5
res = dict(script_sha256=d[0]['script_sha256'], cpu_s=sum(x['cpu_s'] for x in d), n_files=len(files), n_full_files=len(full),
           n_events_checked=int(sum(f['n_checked'] for f in files)), n_bad_witness_k_le3=len(bad), bad=bad[:50])
def cnt(m): return int(m.sum())
for cls, zm in (('Z', Z), ('Zlow', ~Z)):
    hs = zm & (E[:, 3] >= 0) & (E[:, 3] <= 3); hf = zm & (E[:, 4] >= 0) & (E[:, 4] <= 3)
    r = dict(her_S=cnt(hs), her_F=cnt(hf),
             her_S_confirmed_by_my_S=cnt(hs & (E[:, 5] <= 3)), her_S_confirmed_same_or_lower_k=cnt(hs & (E[:, 5] <= E[:, 3])),
             her_S_my_k_higher_but_le3=cnt(hs & (E[:, 5] <= 3) & (E[:, 5] > E[:, 3])),
             her_S_my_k_lower=cnt(hs & (E[:, 5] < E[:, 3])),
             her_S_not_confirmed=cnt(hs & (E[:, 5] > 3)),
             her_F_confirmed_by_my_F=cnt(hf & (E[:, 6] <= 3)), her_F_not_confirmed=cnt(hf & (E[:, 6] > 3)),
             her_S_with_hard_window_witness=cnt(hs & (E[:, 7] <= 3)),
             row_events_her_gt3_my_S_le3=cnt(zm & (E[:, 3] > 3) & (E[:, 5] <= 3)),
             row_events_her_gt3_my_F_le3=cnt(zm & (E[:, 4] > 3) & (E[:, 6] <= 3)),
             my_S_by_k_on_her_S={str(k): cnt(hs & (E[:, 5] == k)) for k in range(4)},
             her_S_by_k={str(k): cnt(hs & (E[:, 3] == k)) for k in range(4)})
    fm = zm & np.isin(E[:, 0], list(full))
    hsf = fm & (E[:, 3] >= 0) & (E[:, 3] <= 3); msf = fm & (E[:, 5] <= 3)
    r['full_files'] = dict(n_files=len(full), her_S=cnt(hsf), my_S=cnt(msf), both=cnt(hsf & msf), only_her=cnt(hsf & ~msf),
                           only_mine=cnt(msf & ~hsf), only_mine_without_her_row=cnt(msf & (E[:, 3] < 0)),
                           her_F=cnt(fm & (E[:, 4] >= 0) & (E[:, 4] <= 3)), my_F=cnt(fm & (E[:, 6] <= 3)),
                           both_F=cnt(fm & (E[:, 4] >= 0) & (E[:, 4] <= 3) & (E[:, 6] <= 3)),
                           my_H=cnt(fm & (E[:, 7] <= 3)), union_S=cnt(hsf | msf))
    res[cls] = r
res['unconfirmed_S'] = [[path[int(e[0])], int(e[1]), int(e[3]), int(e[4]), int(e[5]), int(e[6])] for e in E if 0 <= e[3] <= 3 and e[5] > 3]
res['unconfirmed_F'] = [[path[int(e[0])], int(e[1]), int(e[3]), int(e[4]), int(e[5]), int(e[6])] for e in E if 0 <= e[4] <= 3 and e[6] > 3]
res['k_higher'] = [[path[int(e[0])], int(e[1]), int(e[3]), int(e[4]), int(e[5]), int(e[6])] for e in E if 0 <= e[3] <= 3 and e[3] < e[5] <= 3]
res['only_mine_full'] = [[path[int(e[0])], int(e[1]), int(e[3]), int(e[4]), int(e[5]), int(e[6])] for e in E if int(e[0]) in full and e[5] <= 3 and not (0 <= e[3] <= 3)]
json.dump(res, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('unconfirmed_S', 'unconfirmed_F', 'k_higher', 'only_mine_full')}, indent=1))
print(len(res['unconfirmed_S']), len(res['unconfirmed_F']), len(res['k_higher']), len(res['only_mine_full']))
if len(sys.argv) > 3:
    todo = {(x[0], x[1]): x for x in res['unconfirmed_S'] + res['unconfirmed_F']}
    rng = np.random.default_rng(20261123)
    kh = res['k_higher']; pick = rng.choice(len(kh), min(40, len(kh)), replace=False) if kh else []
    for i in pick: todo.setdefault((kh[i][0], kh[i][1]), kh[i])
    conf = [[path[int(e[0])], int(e[1]), int(e[3]), int(e[4])] for e in E if 0 <= e[3] <= 3 and e[5] <= e[3]]
    for i in rng.choice(len(conf), 40, replace=False): todo.setdefault((conf[i][0], conf[i][1]), conf[i])
    json.dump([[v[0], v[1], v[2], v[3]] for v in todo.values()], open(sys.argv[3], 'w'))
    print('todo', len(todo))
