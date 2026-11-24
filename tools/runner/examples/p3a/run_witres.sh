#!/bin/bash
# Aurora 2026-11-24 (p3-a): resolve the 'subset_failed' witnesses with the kernel's plane normal (one process, nice 10).
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
O=$QV2/phase3_selection/outputs/p3a; W=/home/scratch/jdochoa/p3a_slice
export NUMBA_CACHE_DIR=$W/numba2 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd $W
/usr/bin/time -f "cpu %U+%S s wall %e" nice -n 10 $QV2/envs/tt/.pixi/envs/default/bin/python $QV2/phase3_selection/src/p3a/p3a_witness_resolve.py $O/p3a_witness_check.json $O/p3a_witness_resolve.json > $W/witres.log 2>&1
