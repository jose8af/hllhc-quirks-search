import sys, numpy as np, pyhepmc
res = []
with pyhepmc.open(sys.argv[1]) as fh:
    for i, ev in enumerate(fh):
        qs = [p for p in ev.particles if abs(p.pid) == 9000011 and p.status == 1]
        P = sum(np.array([p.momentum.px, p.momentum.py]) for p in qs)
        ptqq = np.hypot(*P)
        # photons whose ancestor chain contains a quirk
        gq = 0.0; gmax = 0.0
        for p in ev.particles:
            if p.pid == 22 and p.status == 1:
                pt = np.hypot(p.momentum.px, p.momentum.py); gmax = max(gmax, pt)
                v = p.production_vertex
                if v is not None and any(abs(m.pid) == 9000011 for m in v.particles_in):
                    gq = max(gq, pt)
        hard = [p for p in ev.particles if p.status == 23 and abs(p.pid) == 9000011]
        ph = np.hypot(*sum(np.array([p.momentum.px, p.momentum.py]) for p in hard))
        res.append((ptqq, ph, gq, gmax))
r = np.array(res)
s = (r[:, 0] > 200) & (r[:, 1] < 150)
print('events with pT(QQ)>200 & ME pT<150:', s.sum())
for row in r[s]:
    print('pTQQ %.0f  pT_ME %.0f  max pT photon from quirk %.0f  max pT photon any %.0f' % tuple(row))
print('fraction of all events with a quirk-FSR photon pT>50: %.4f, >100: %.4f' % (np.mean(r[:, 2] > 50), np.mean(r[:, 2] > 100)))
