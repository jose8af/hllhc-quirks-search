import json, numpy as np
B = json.load(open('results/FIX_bstar_off.json')); X = json.load(open('results/FIX_R2_bstar_context.json'))
print('FIX_bstar_off keys:', list(B.keys()))
for k in ('bins','arm_median_difference','summary'):
    if k in B: print(k, json.dumps(B[k])[:1500])
ev = [e for e in B['events'] if e['random'] and e['status_ok']]
# production-composition reweighted off/on median (weights = n_prod_bin / n_sample_bin)
bins = ((0,2),(2,4),(4,6),(6,10),(10,1e9)); nprod = [83,167,128,123,99]
def wmed(x, w):
    o = np.argsort(x); x = np.asarray(x)[o]; w = np.asarray(w)[o]; c = np.cumsum(w)/w.sum(); return x[np.searchsorted(c, .5)]
rng = np.random.default_rng(1)
for arm in ('c_off','c_on'):
    r = np.array([(e[arm]-e['c_ev'])/e['c_ev'] for e in ev]); kb = np.array([e['k_B'] for e in ev])
    w = np.zeros(len(ev))
    for (a,b),n in zip(bins,nprod):
        s = (kb>=a)&(kb<b); w[s] = n/s.sum()
    bs=[]
    for _ in range(4000):
        i = np.concatenate([rng.choice(np.where((kb>=a)&(kb<b))[0], ((kb>=a)&(kb<b)).sum()) for a,b in bins])
        bs.append(wmed(r[i], w[i]))
    print(arm, 'unweighted median %.4f  prod-weighted %.4f +- %.4f' % (np.median(r), wmed(r,w), np.std(bs)))
print(json.dumps(X['off_vs_production']['all']))
