#!/bin/bash
# Aurora 2026-11-24 (p3-a): witness check on every 24th Z(nunu) pilot file, offsets 0 and 12 (two processes, nice 10).
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh >/dev/null 2>&1
O=$QV2/phase3_selection/outputs/p3a; PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3a
W=/home/scratch/jdochoa/p3a_slice
export NUMBA_CACHE_DIR=$W/numba2 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd $W; mkdir -p wit1; mv wit_*.json wit_*.log wit1/ 2>/dev/null
for o in 0 12; do
  /usr/bin/time -f "cpu %U+%S s wall %e" nice -n 10 $PY $S/p3a_witness_check.py --rows $O/p3a_counts.json.rows_m.npz --stride 24 --offset $o --out $W/wit_$o.json > $W/wit_$o.log 2>&1 &
done
wait
