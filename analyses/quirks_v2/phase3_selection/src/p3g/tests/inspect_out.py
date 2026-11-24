"""print the event tables and a candidate summary of p3g job outputs (tests only)."""
import json, sys
import numpy as np
for f in sys.argv[1:]:
    z = np.load(f); m = json.loads(str(z['meta']))
    print(f, {k: m[k] for k in ('mode', 'n_events', 'trials', 't_chain_s', 'wall_s', 'v41_pass') if k in m})
    np.set_printoptions(linewidth=200, suppress=True, precision=4)
    print(m.get('ev_cols')); print(z['ev'][:, :8])
    print(m.get('evs_cols')); print(z['evs'])
    C = z['cand']; cc = m['cand_cols']
    if len(C):
        d = {k: C[:, i] for i, k in enumerate(cc)}
        for t in (0, 1, 2):
            s = d['trial'] == t
            print('trial', t, 'cands', int(s.sum()), 'with own', int((s & (d['n_own'] > 0)).sum()),
                  'jo_ip>=4', int((s & (d['jo_ip'] >= 4)).sum()), 'max jo_ip', d['jo_ip'][s].max() if s.any() else -1)
