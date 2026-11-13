#!/usr/bin/env bash
# bench_chain.sh -- feasibility A (Anselm): one benchmark unit on a worker, timed by bench_run.py (/usr/bin/time -v).
# Usage (on the worker, e.g. ssh -x maxwell 'bash .../bench_chain.sh <unit> <rep> <conc> [args]'):
#   s3     <m> <lam>        Stage-3 string propagation, one toy job of src/jobs/s3_bench_m<m>_L<lam>.json (1 worker)
#   s4pu   <n> <roads> <rho> <seed>   Stage-4 B1-like PU-200 job: chain (Fatras+digi+CKF) + top-up + finder
#   smoke  <n_mb> <n_pu>    v1 install check acts/scripts/smoke_test.py (M3 record: 39.3 s for 400 200)
#   m5     <nev> <workers>  Stage-1 numerics M5_li_blinearity.py (M3 record: cpu 1153 s for 30 events, 1 worker)
#   m2     <nproc>          Stage-1 numerics M2_single.py all (M3 record: 416 runs, 13 s wall, 7 processes)
#   cp     <topo> <n>       Stage-4 C'0 no-PU single-interaction toy/gun through the chain (run_chain.py cp)
#   gun    <n> <pdg>        Stage-4 particle gun, no PU (run_chain.py gun --mu 0)
# Work dirs: /home/scratch/jdochoa/anselm_bench/<unit>_<args>_r<rep>c<conc> (node-local; deleted by the caller).
# numba caches: node-local /home/scratch/jdochoa/cache/numba_<unit> (never on /home or cajuela).
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
SRC=$QV2/phase1_strategy/src
U=$1; REP=$2; CONC=$3; shift 3
TAG="${U}_$(echo "$*" | tr ' ' '_')"
W=$QV2_SCRATCH/anselm_bench/${TAG}_r${REP}c${CONC}
rm -rf "$W"; mkdir -p "$W"
TTPY="pixi run --manifest-path $QV2/envs/tt/pixi.toml python"
ACTSPY="pixi run --manifest-path $QV2/acts/pixi.toml python"
export PYTHONPYCACHEPREFIX=$QV2_SCRATCH/cache/pyc PYTHONDONTWRITEBYTECODE=1
B="python3 -I $SRC/bench_run.py --rep $REP --conc $CONC --workdir $W --note ${BENCH_NOTE:-warm}"
case "$U" in
  s3)
    m=$1; lam=$2
    n=$(python3 -c "import json;print(len(json.load(open('$SRC/jobs/s3_bench_m${m}_L${lam}.json'))['jobs'][0]['ev']))")
    export NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s3
    $B --label s3_m${m}_L${lam} --units $n -- $TTPY $QV2/sim/stage3/code/run_stage3.py run \
       --jobs $SRC/jobs/s3_bench_m${m}_L${lam}.json --workers 1 --inputs $QV2_DATA/feasibility/chain/stage3_inputs --out $W/out
    # per-event kernel CPU from the output npz (cpu_s per event, recorded by the v1 runner)
    f=$(ls $W/out/s3bench/F_m${m}/*.npz)
    $QV2/envs/tt/.pixi/envs/default/bin/python -c "
import numpy as np, json, os, socket
z = np.load('$f')
rec = dict(rep=$REP, conc=$CONC, host=socket.gethostname(), m=$m, lam=$lam, n=int(len(z['cpu_s'])),
           cpu_ev=z['cpu_s'].tolist(), status=z['status'].tolist(), nsteps=z['nsteps'].tolist(),
           bytes=os.path.getsize('$f'), n_hits=int(len(z['h_x'])))
open('$QV2/phase1_strategy/outputs/feasibility/bench_logs/s3_events.jsonl', 'a').write(json.dumps(rec) + chr(10))
" ;;
  s4pu)
    n=$1; roads=$2; rho=$3; seed=$4
    export QV2_S4_DATA=$W/s4 NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s4
    cd $QV2
    $B --label s4pu_n${n}_roads${roads}_rho${rho} --units $n -- $TTPY $SRC/bench_s4_pu.py BENCH $n $roads $rho $seed ;;
  smoke)
    export QV2_SMOKE_TMP=$W/tmp
    cd $QV2/acts
    $B --label smoke_${1}_${2} --units 1 --unit-name job -- $ACTSPY -W ignore $QV2/acts/scripts/smoke_test.py $1 $2 ;;
  m5|m2)
    # the Stage-1 scripts write results/ next to themselves: run them from a node-local shadow tree of symlinks
    mkdir -p $W/tree/analytic/numerics
    for f in $QV2/analytic/numerics/*.py; do ln -s $f $W/tree/analytic/numerics/; done
    ln -s $QV2/code $W/tree/code
    export NUMBA_CACHE_DIR=$QV2_SCRATCH/cache/numba_s1
    if [ "$U" = m5 ]; then
      $B --label m5_nev${1}_w${2} --units $1 -- $TTPY $W/tree/analytic/numerics/M5_li_blinearity.py $1 $2
    else
      export QV2_NPROC=$1
      $B --label m2_np${1} --units 416 --unit-name run -- $TTPY $W/tree/analytic/numerics/M2_single.py all
    fi ;;
  cp)
    export QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH/cache/pythia_init
    cd $QV2/acts
    $B --label cp_${1}_n${2} --units $2 -- $ACTSPY $QV2/acts/stage4/code/run_chain.py cp --topo $1 $W/out.npz $2 12345 ;;
  gun)
    export QV2_PYTHIA_INIT_DIR=$QV2_SCRATCH/cache/pythia_init
    cd $QV2/acts
    $B --label gun_n${1}_pdg${2} --units $1 -- $ACTSPY $QV2/acts/stage4/code/run_chain.py gun $W/out.npz $1 12345 --mu 0 --gun-pdg $2 ;;
  *) echo "unknown unit $U"; exit 2 ;;
esac
