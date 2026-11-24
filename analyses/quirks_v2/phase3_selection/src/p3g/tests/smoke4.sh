#!/bin/bash
# p3-g smoke 4: g4pu, 1 event, 2 roads
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
W=/home/scratch/jdochoa/p3g_smoke; cd $W
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 QV2_OUT_DIR=$W/out QV2_PYTHIA_INIT_DIR=$W/pythia_init
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3g
/usr/bin/time -f "cpu %U+%S s wall %e rss %M" timeout 600 nice -n 10 $PY $S/p3g_ovl_job.py --id smk-g4pu --mode g4pu --n ${1:-1} --stream p3g.smoke --chunk 0 --roads 2 > $W/ovl_g4pu.log 2>&1
echo rc=$? >> $W/ovl_g4pu.log
