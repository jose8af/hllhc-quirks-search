"""R1-constructive check 4: Stage-3 statistics per TRGS point: rows, w=0 rows, tail events (pT>200, |eta|<2.5, w>0),
Kish N_eff, INC-origin share, and what 'first N in file order' would select."""
import numpy as np, json
idx=json.load(open('../data/sim/SAMPLES_INDEX.json'))
print(f"{'file':16s} {'rows':>7s} {'w=0':>6s} {'N_tail':>7s} {'Neff':>7s} {'Neff/N':>6s} {'INCev%':>6s} {'INCsig%':>7s} {'wINC/wTRG':>9s} {'firstINCpos':>11s}")
for pre in ('E','S'):
    for m in range(200,1600,100):
        f=f'../data/sim/npz/{pre}-TRGS_m{m}.npz'
        try: c=np.load(f)
        except FileNotFoundError: continue
        w=c['w']; o=c['origin']; t=(w>0)&(c['pt_pair']>200)&(np.abs(c['eta_pair'])<2.5)
        ws=w[t]; neff=ws.sum()**2/(ws**2).sum()
        pos=np.argmax(o[np.where(t)[0]]==1)
        print(f"{pre}-TRGS_m{m:<6d} {len(w):7d} {(w==0).sum():6d} {t.sum():7d} {neff:7.0f} {neff/t.sum():6.3f} {100*(o[t]==1).mean():6.2f} {100*w[t&(o==1)].sum()/ws.sum():7.2f} {np.median(w[(o==1)&(w>0)])/np.median(w[(o==0)&(w>0)]):9.2f} {pos:11d}")
print('index aliases for trig:', {k:v for k,v in idx.items() if k.endswith('_trig')} if len(idx)<400 else 'many')
