#!/bin/bash
# Vilde (reviewer, p3-a round 2): second half of the independent search (Sindre C-4).
# p3a_indep.py unchanged, --stride 2 --offset 1 (the 230 Z(nunu) pilot files Aurora's 'ind' variant did not read).
# One process at a time, nice 15, 8 sequential parts (each resumable: a part with an output is skipped).
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
W=/home/scratch/jdochoa/vilde_ind2; mkdir -p $W/numba
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1
PY=$QV2/envs/tt/.pixi/envs/default/bin/python; S=$QV2/phase3_selection/src/p3a
for p in 0 1 2 3 4 5 6 7; do
  [ -f $W/vilde2-$p.ind.json ] && continue
  /usr/bin/time -v nice -n 15 ionice -c3 $PY -B $S/p3a_indep.py --part $p --nparts 8 --stride 2 --offset 1 \
     --out $W/vilde2-$p.ind.json > $W/part$p.log 2>&1
done
echo ALLDONE > $W/done.flag
