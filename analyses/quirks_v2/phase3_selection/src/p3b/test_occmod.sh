#!/bin/bash
# Development test of the occupancy chain (p3-b, Casper): occin on one pu1 file (100 planes per trial), then the model
# with a small ensemble.  Runs in /home/scratch/jdochoa/p3b_dev/occtest on the worker, one process at a time.
set -e
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
D=/home/scratch/jdochoa/p3b_dev/occtest; mkdir -p $D; cd $D
export NUMBA_CACHE_DIR=/home/scratch/jdochoa/p3b_dev/numba QV2_OUT_DIR=$D PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3b
[ -f occin-test.npz ] || /usr/bin/time -f "occin %e s %U user %M kB" nice -n 10 $PY $S/occin_job.py --id occin-test --jobs c1pu1-0000 --planes 100
/usr/bin/time -f "occmod %e s %U user %M kB" nice -n 10 $PY $S/occmod_job.py --id occmod-test --inputs $D --seed 1 --nA ${NA:-3000} --nB ${NB:-200} --nplain 200 --nis 200
$PY - <<'PY'
import numpy as np
d = np.load('occmod-test.npz'); o = np.load('occin-test.npz')
import logging; logging.basicConfig(level=logging.INFO, format='%(message)s'); L = logging.getLogger()
pa = d['pA'].mean(); L.info('E[P_R04] model %.3e ; real planes R04 %.3e (%d), R05 %.3e', pa, o['cnt'][:,0].sum()/(len(o['cnt'])*100), o['cnt'][:,0].sum(), o['cnt'][:,1].sum()/(len(o['cnt'])*100))
L.info('model layer P mean %s', np.round(d['plA_mean'], 3))
mh = o['mask_hist'].sum(0); n = mh.sum()
L.info('real  layer P mean %s', np.round([sum(mh[k] for k in range(1024) if (k >> l) & 1)/n for l in range(10)], 3))
pl = d['plain'].mean(0); isr = d['isr'][:, :, 0].mean(0); isn = d['isr'][:, :, 2].sum(0)
L.info('P(w<W|R04) plain %s ; IS %s ; IS passing toys %s', pl, isr, isn)
L.info('P2S>=1,2,3 (B) %s', d['p2B'].mean(0))
PY
