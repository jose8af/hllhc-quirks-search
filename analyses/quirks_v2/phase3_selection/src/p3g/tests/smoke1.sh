#!/bin/bash
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
W=/home/scratch/jdochoa/p3g_smoke; mkdir -p $W; cd $W
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3g
/usr/bin/time -f "cpu %U+%S s wall %e rss %M" timeout 600 nice -n 10 $PY $S/p3g_prep.py --mode dif --n 4 --out $W/src_dif4.npz > $W/prep_dif.log 2>&1
echo prep rc=$? >> $W/prep_dif.log
