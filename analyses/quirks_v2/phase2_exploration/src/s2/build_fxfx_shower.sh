#!/bin/bash
# Build our FxFx shower driver (fxfx_shower.cc) against the installed HEPTools Pythia 8.313 (no change to installed
# software).  Run on a worker:  nice -n 10 bash build_fxfx_shower.sh
# Compiles in /var/tmp/jdochoa (node-local), installs one file $SW/fxfx_shower/fxfx_shower-<sha256[:16] of source>.
set -euo pipefail
SRC=$(cd "$(dirname "$0")" && pwd)/fxfx_shower.cc
P8=/home/users/jdochoa/sw/mg5/MG5_aMC_v2_9_22/HEPTools/pythia8
H=$(sha256sum "$SRC" | cut -c1-16)
B=/var/tmp/jdochoa/fxfx_shower_build/$H
DST=/home/users/jdochoa/sw/fxfx_shower
mkdir -p "$B" "$DST"
cd "$B"
g++ $("$P8/bin/pythia8-config" --cxxflags) "$SRC" -o fxfx_shower $("$P8/bin/pythia8-config" --libs) 2>&1 | tee build.log
rc=0; ./fxfx_shower 2>/dev/null || rc=$?; test $rc -eq 2   # usage check
cp fxfx_shower "$DST/fxfx_shower-$H.part" && mv "$DST/fxfx_shower-$H.part" "$DST/fxfx_shower-$H"
echo "built $DST/fxfx_shower-$H ($(g++ --version | head -1))"
