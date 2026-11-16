#!/usr/bin/env bash
# g4hv.sh -- run g4hv on this worker; builds it once per node and source version in node-local scratch.
#   g4hv.sh <args of g4hv>          (never on einstein)
# Pre-flight (FEAS_B): the node-local Geant4 env must match the tracked lock.
set -euo pipefail
REPO=/home/users/jdochoa/hllhc-quirks-search
SRC=$REPO/analyses/quirks_v2/phase2_exploration/src/g4
G4=/home/scratch/jdochoa/envs/g4
E=$G4/.pixi/envs/default
[ "$(hostname -s)" != einstein ] || { echo "refusing to run on einstein" >&2; exit 1; }
grep -q "lock_sha256=$(sha256sum $REPO/tools/install/g4/pixi.lock | cut -d' ' -f1)" $G4/INSTALLED \
  || { echo "Geant4 env on $(hostname -s) does not match the lock" >&2; exit 3; }
stamp=$(cat $SRC/g4hv.cc $SRC/CMakeLists.txt | sha256sum | cut -c1-16)
C=/home/scratch/jdochoa/cache/g4hv
BIN=$C/$stamp/g4hv
export PATH=$E/bin:$PATH CONDA_PREFIX=$E
# Geant4 data sets and compiler variables: the env's activation scripts
set +eu
for f in $E/etc/conda/activate.d/*.sh; do . "$f" > /dev/null 2>&1; done
set -eu
if [ ! -x "$BIN" ]; then
  mkdir -p $C
  (
    flock -w 600 9
    if [ ! -x "$BIN" ]; then
      B=/var/tmp/jdochoa/g4hv_build_$stamp.$$
      rm -rf $B; mkdir -p $B
      cmake -S $SRC -B $B -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=$E -DCMAKE_IGNORE_PREFIX_PATH=/usr > $B/cmake.log 2>&1 \
        && make -C $B > $B/make.log 2>&1 || { tail -30 $B/cmake.log $B/make.log >&2; exit 4; }
      mkdir -p $C/.tmp.$$ && cp $B/g4hv $C/.tmp.$$/ && mv $C/.tmp.$$ $C/$stamp
      rm -rf $B
    fi
  ) 9> $C/.lock
fi
exec "$BIN" "$@"
