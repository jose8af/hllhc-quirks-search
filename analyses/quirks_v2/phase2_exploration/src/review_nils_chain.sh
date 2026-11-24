#!/bin/bash
# Nils, 2026-11-23: the five review jobs of review_nils_subset.py, one at a time (1 slot), on a worker.
QV2=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2
W=/home/scratch/jdochoa/nils_r1s
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1
mkdir -p $W/out $W/numba; cd $W
for p in 0 1 2 3 4; do
  [ -f out/part$p.json ] && continue
  /usr/bin/time -v timeout 1750 nice -n 15 $QV2/envs/tt/.pixi/envs/default/bin/python -B \
    $QV2/phase2_exploration/src/review_nils_subset.py --part $p --nparts 5 --full-mod 8 --out $W/out/part$p.json > out/part$p.log 2>&1
done
touch out/CHAIN_DONE
