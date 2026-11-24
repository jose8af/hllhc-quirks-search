#!/bin/bash
# p3-g smoke 5: zhl regeneration of c1sm-0000, first N events (check C2)
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
W=/home/scratch/jdochoa/p3g_smoke; cd $W
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 QV2_OUT_DIR=$W/out QV2_PYTHIA_INIT_DIR=$W/pythia_init
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3g
/usr/bin/time -f "cpu %U+%S s wall %e rss %M" timeout 600 nice -n 10 $PY $S/p3g_ovl_job.py --id smk-zhl --mode zhl --n ${1:-2} --chunk 0 --trials T1,T0 > $W/ovl_zhl.log 2>&1
echo rc=$? >> $W/ovl_zhl.log
