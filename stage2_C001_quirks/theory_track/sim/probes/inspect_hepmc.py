import sys, numpy as np, pyhepmc
f = sys.argv[1]
nq = []; st = []; vt = []; w0 = []; nw = None; names = None; nfs = []; ptQQ = []; ptvis = []
with pyhepmc.open(f) as fh:
    for i, ev in enumerate(fh):
        if i == 0:
            names = ev.weight_names; nw = len(ev.weights)
            print('units', ev.momentum_unit, ev.length_unit, 'nweights', nw, names[:6], '...', names[-6:])
            print('xsec', ev.cross_section.xsec() if ev.cross_section else None)
        qs = [p for p in ev.particles if abs(p.pid) in (9000011, 9000013) and p.status == 1]
        allq = [p for p in ev.particles if abs(p.pid) in (9000011, 9000013)]
        nq.append(len(qs)); st.append(tuple(sorted(set(p.status for p in allq))))
        if qs:
            v = qs[0].production_vertex
            vt.append((v.position.x, v.position.y, v.position.z, v.position.t))
        P = sum((np.array([p.momentum.px, p.momentum.py, p.momentum.pz, p.momentum.e]) for p in qs), np.zeros(4))
        ptQQ.append(np.hypot(P[0], P[1]))
        vis = np.zeros(4)
        for p in ev.particles:
            if p.status == 1 and abs(p.pid) not in (12, 14, 16, 9000011, 9000013):
                vis += [p.momentum.px, p.momentum.py, p.momentum.pz, p.momentum.e]
        ptvis.append(np.hypot(vis[0] + P[0], vis[1] + P[1]))
        nfs.append(sum(1 for p in ev.particles if p.status == 1))
        w0.append(ev.weights[0])
w0 = np.array(w0)
print('events', len(nq), 'n final quirks per event', np.bincount(nq), 'quirk status sets', set(st))
print('vertex (mm) first 3', vt[:3], ' max |v|', np.max(np.abs(np.array(vt)), axis=0))
print('final-state multiplicity mean', np.mean(nfs))
print('central weight: frac nonzero', np.mean(w0 != 0), 'sum', w0.sum(), 'mean', w0.mean(), 'unique', np.unique(np.round(w0, 12))[:5])
print('pT(QQ) median', np.median(ptQQ), ' |pT(QQ)+pT(vis)| max (balance)', np.max(ptvis))
