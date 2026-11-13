#!/usr/bin/env bash
# install_g4_local.sh -- Geant4 11.4.3 (conda-forge, noqt) + its data sets on THIS worker's local disk (quirks v2).
# User decision 2026-11-13: the Geant4 env lives on each worker at /home/scratch/jdochoa/envs/g4 (node-local, also seen
# by pods through the scratch hostPath), with a node-local package cache, so nothing is written to the NFS home.
# Canonical manifest + lock: tools/install/g4/pixi.{toml,lock}.  Idempotent: exits 0 at once if the stamp matches the lock.
# Usage (on a worker, never on einstein):  bash /home/users/jdochoa/hllhc-quirks-search/tools/install/install_g4_local.sh
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
if [ "$(hostname -s)" = "einstein" ]; then echo "refusing to run on einstein (head node)"; exit 1; fi
SRC=$REPO/tools/install/g4
DST=/home/scratch/jdochoa/envs/g4
STAMP=$DST/INSTALLED
LOCKSHA=$(sha256sum "$SRC/pixi.lock" | cut -d' ' -f1)
if [ -f "$STAMP" ] && grep -q "lock_sha256=$LOCKSHA" "$STAMP"; then
  echo "g4 env already installed and matches the lock ($LOCKSHA)"; exit 0
fi
mkdir -p "$DST" /home/scratch/jdochoa/cache/rattler
rm -f "$STAMP"
cp "$SRC/pixi.toml" "$SRC/pixi.lock" "$DST/"
cd "$DST"
PIXI_CACHE_DIR=/home/scratch/jdochoa/cache/rattler nice -n 10 pixi install --frozen
E=$DST/.pixi/envs/default
# verify: every file listed in conda-meta/*.json exists
MISSING=$(python3 -I - "$E" <<'PY'
import json, glob, os, sys
e = sys.argv[1]; n = m = 0
for j in glob.glob(os.path.join(e, 'conda-meta', '*.json')):
    for f in json.load(open(j)).get('files', []):
        n += 1
        m += not os.path.lexists(os.path.join(e, f))
print(m, n)
PY
)
echo "conda-meta check: missing/total = $MISSING"
[ "${MISSING%% *}" = "0" ] || { echo "env incomplete"; exit 1; }
G4V=$(pixi run --frozen geant4-config --version)
DATA=$(du -sh "$E/share/Geant4/data" 2>/dev/null | cut -f1 || echo "?")
printf 'host=%s\ndate=%s\nlock_sha256=%s\ngeant4=%s\ndata_size=%s\nenv_size=%s\n' "$(hostname -s)" "$(date -Is)" \
  "$LOCKSHA" "$G4V" "$DATA" "$(du -sh "$E" | cut -f1)" > "$STAMP.part"
mv "$STAMP.part" "$STAMP"
cat "$STAMP"
# Pre-flight for Geant4 jobs (run in the job, not here):
#   grep -q "lock_sha256=$(sha256sum $REPO/tools/install/g4/pixi.lock | cut -d' ' -f1)" /home/scratch/jdochoa/envs/g4/INSTALLED
