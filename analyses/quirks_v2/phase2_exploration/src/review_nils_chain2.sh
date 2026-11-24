#!/bin/bash
# Nils, 2026-11-23: rerun of parts 1-3 of review_nils_chain.sh (killed by the 1750 s wall limit: NFS-read bound, CPU ~630 s
# each, no output), as six smaller rows-only jobs (gi % 10 in 1,2,3,6,7,8; no full mode), one at a time.
QV2=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2
W=/home/scratch/jdochoa/nils_r1s
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1
cd $W
for p in 1 2 3 6 7 8; do
  [ -f out/partq$p.json ] && continue
  /usr/bin/time -v timeout 1750 nice -n 15 $QV2/envs/tt/.pixi/envs/default/bin/python -B \
    $QV2/phase2_exploration/src/review_nils_subset.py --part $p --nparts 10 --full-mod 0 --out $W/out/partq$p.json > out/partq$p.log 2>&1
done
touch out/CHAIN2_DONE
