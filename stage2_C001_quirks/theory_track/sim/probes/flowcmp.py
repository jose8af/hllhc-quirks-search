import sys, numpy as np, pyhepmc, glob
def acc(files):
    out = []
    for f in files:
        with pyhepmc.open(f) as fh:
            for ev in fh:
                n = list(ev.weight_names)
                out.append((ev.event_number, ev.weight('Weight_MERGING=45.000') != 0, len(ev.particles)))
    return out
G = sys.argv[1]
a = acc([sys.argv[2]])
b = acc(sorted(glob.glob(G + '/mine/split_*/events.hepmc')))
print('MG flow:', len(a), 'acc', np.mean([x[1] for x in a]), 'npart first', [x[2] for x in a[:5]])
print('mine   :', len(b), 'acc', np.mean([x[1] for x in b]), 'npart first', [x[2] for x in b[:5]])
