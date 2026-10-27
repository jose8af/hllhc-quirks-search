"""R1 constructive check 6: where are the status-4 (deadlock) and status-0 (t_end) events, in the P2 template counting set?
Worst-case effect on f_merged100 if every status-4 event were merged (f -> f + n4/n)."""
import numpy as np, collections, json
for camp in ('p1', 'p2', 'mv'):
    z = np.load(f'data/sim_stage3/summary/events_{camp}.npz', allow_pickle=False)
    keys = z['point_keys']; pt = z['point']; st = z['status']; tt = z['tt_split']; e25 = z['in_eta25']
    c4 = collections.Counter(); c0 = collections.Counter(); ntot = collections.Counter()
    for i, k in enumerate(keys):
        m = pt == i
        sel = m & (tt == 0) & e25 if camp != 'p1' else m
        L = float(k.split('/L')[1].split('_')[0]); cfg = k.split('_')[-1]
        c4[(L, cfg)] += int((sel & (st == 4)).sum()); c0[(L, cfg)] += int((sel & (st == 0)).sum()); ntot[(L, cfg)] += int(sel.sum())
    print(camp, 'status4 by (Lambda,cfg) [counting set]:', {k: v for k, v in sorted(c4.items()) if v})
    print(camp, 'status0 by (Lambda,cfg) [counting set]:', {k: v for k, v in sorted(c0.items()) if v})
    if camp == 'p2':
        worst = []
        for i, k in enumerate(keys):
            m = (pt == i) & (tt == 0) & e25; n4 = int((m & (st == 4)).sum())
            if n4: worst.append((k, n4, int(m.sum())))
        print('p2 template points with status 4 (key, n4, n):', sorted(worst, key=lambda t: -t[1] / t[2])[:8])

# part 2: f_merged100 near the E1500 edge (slope for the worst-case status-4 shift); status-0 per mass at 0.3 keV
P = json.load(open('sim/stage3/results/P2_points.json'))
for L in ('10', '15', '20', '30', '40'):
    v = P.get(f'F_m1500/L{L}')
    if v: print('F_m1500 L', L, 'f_merged100 =', v['f_merged100'], 'status', v['status_counts'])
z = np.load('data/sim_stage3/summary/events_p2.npz', allow_pickle=False)
keys = z['point_keys']; pt = z['point']; st = z['status']; tt = z['tt_split']; e25 = z['in_eta25']
print('status0 at 0.3 keV per mass:', {str(k): int(((pt == i) & (st == 0) & (tt == 0) & e25).sum()) for i, k in enumerate(keys) if '/L0.3_' in k and ((pt == i) & (st == 0)).sum()})
