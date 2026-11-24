#!/bin/bash
# p3-g smoke 2: overlay job on the 4-event DIF source; arg1 = mu, arg2 = n, arg3 = trials, arg4 = mode, arg5 = src
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
W=/home/scratch/jdochoa/p3g_smoke; cd $W
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 QV2_OUT_DIR=$W/out
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3g
mu=$1; n=$2; tr=$3; mode=${4:-dif}; src=${5:-$W/src_dif4.npz}
/usr/bin/time -f "cpu %U+%S s wall %e rss %M" timeout 600 nice -n 10 $PY $S/p3g_ovl_job.py --id smk-$mode-mu$mu --mode $mode --src $src --first 0 --n $n --stream p3g.smoke --chunk 0 --trials $tr --mu $mu > $W/ovl_${mode}_mu$mu.log 2>&1
echo rc=$? >> $W/ovl_${mode}_mu$mu.log
