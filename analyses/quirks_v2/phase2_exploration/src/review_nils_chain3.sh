#!/bin/bash
# Nils, 2026-11-23: diagnostics of p2w_subset.py's own witnesses (T7 trials, then the events my search did not confirm).
QV2=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2
W=/home/scratch/jdochoa/nils_r1s
export NUMBA_CACHE_DIR=$W/numba PYTHONDONTWRITEBYTECODE=1
cd $W
PY=$QV2/envs/tt/.pixi/envs/default/bin/python
/usr/bin/time -v timeout 900 nice -n 15 $PY -B $QV2/phase2_exploration/src/review_nils_witness.py t7 $W/out/t7.json > out/t7.log 2>&1
/usr/bin/time -v timeout 1700 nice -n 15 $PY -B $QV2/phase2_exploration/src/review_nils_witness.py events $W/out/todo.json $W/out/wit.json 430 > out/wit.log 2>&1
touch out/CHAIN3_DONE
