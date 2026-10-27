import sys, numpy as np, pyhepmc
W = None; names = None
with pyhepmc.open(sys.argv[1]) as fh:
    rows = []
    for ev in fh:
        if names is None:
            names = list(ev.weight_names)
        rows.append(list(ev.weights))
W = np.array(rows); N = 1000
print(len(names), W.shape)
for i, k in enumerate(names):
    if 'AUX' in k:
        continue
    v = W[:, i]
    if k.startswith('Weight') or 'MUF=1.0_MUR=1.0' in k or ('MUF=2.0_MUR=2.0' in k) or ('MUF=0.5_MUR=0.5' in k):
        print(f'{k:50s} sum/N_LHE = {v.sum()/N*1e3:.4f} fb  nonzero = {np.mean(v!=0):.3f}')
aux = [k for k in names if 'AUX' in k]; print('AUX weights', len(aux), 'sample sums', [round(W[:, names.index(k)].sum()/N*1e3, 4) for k in aux[:5]])
