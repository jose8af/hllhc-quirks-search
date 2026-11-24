"""Exploration (no direct count read): layer-mask multiplicities of the p3-b occin random-plane ensemble."""
import sys
import numpy as np
z = np.load(sys.argv[1])
mh = z['mask_hist'].sum(0); ntr = len(z['mask_hist'])
m = np.arange(1024)
ip = np.array([bin(x & 127).count('1') for x in m]); it = np.array([bin(x & 15).count('1') for x in m])
l2 = np.array([bin(x).count('1') for x in m])
tot = mh.sum(); print('trials', ntr, 'planes', tot)
for k in range(3, 8):
    s = mh[(ip >= k) & (it >= 3)].sum(); print('IP2>=%d & IT2>=3' % k, s, s / tot, 'per trial at 1e4:', s / ntr * 10)
for k in range(4, 11):
    s = mh[(l2 >= k)].sum(); print('NL2>=%d' % k, s / tot)
print('in-band hits per plane', z['ntot'].mean() / 1000)
print('cnt R04 R05 R06', z['cnt'][:, :3].sum(0))
