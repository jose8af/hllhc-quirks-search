#!/bin/bash
# p3-g smoke 3: npo prep on one pilot file of part 0
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
W=/home/scratch/jdochoa/p3g_smoke; cd $W
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3g
/usr/bin/time -f "cpu %U+%S s wall %e rss %M" timeout 600 nice -n 10 $PY $S/p3g_prep.py --mode npo --part 0 --nparts 4 --max-files 1 --out $W/src_npo_t.npz > $W/prep_npo.log 2>&1
echo rc=$? >> $W/prep_npo.log
