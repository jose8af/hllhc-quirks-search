#!/bin/bash
# m2_linux.sh -- P1-d "Linux difference" (STR §4.15): rerun v1's Stage-1 M2 numerics (analytic/numerics/M2_single.py all)
# and its analysis (M2_analysis.py) on a Linux worker, entirely in the job scratch (the scripts write __file__-relative
# results/raw/M2/*.npz: 416 small files, which must not go to /home/users), and publish the merged M2.json, the stdout
# table and a tarball of the raw runs.  Compared afterwards with v1's tracked results/M2.json (p1/m2_compare.py).
set -euo pipefail
QV2=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2
W=$QV2_SCRATCH_DIR/tree
mkdir -p $W/analytic $W/code
cp -r $QV2/analytic/numerics $W/analytic/
cp -r $QV2/code/. $W/code/
rm -rf $W/analytic/numerics/results/raw $W/analytic/numerics/results/M2.json
export NUMBA_CACHE_DIR=$QV2_SCRATCH_DIR/numba PYTHONDONTWRITEBYTECODE=1 QV2_NPROC=1 OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
PY=$QV2/envs/tt/.pixi/envs/default/bin/python
cd $W/analytic/numerics
$PY M2_single.py all > $QV2_OUT_DIR/m2_single_stdout.txt 2>&1
$PY M2_analysis.py > $QV2_OUT_DIR/m2_analysis_stdout.txt 2>&1
cp results/M2.json $QV2_OUT_DIR/M2_linux.json
tar czf $QV2_OUT_DIR/M2_linux_raw.tar.gz -C results raw/M2
