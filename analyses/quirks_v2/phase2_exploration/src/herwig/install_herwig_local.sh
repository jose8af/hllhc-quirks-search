#!/usr/bin/env bash
# install_herwig_local.sh -- Herwig 7.3.0 (conda-forge) on THIS worker's local disk, node-local package cache, no NFS
# writes except the small solved lock copied back next to this script.  Pattern of tools/install/install_g4_local.sh.
# Usage (on a worker, never on einstein; only while holding the study's install slot):
#   nice -n 19 bash .../phase2_exploration/src/herwig/install_herwig_local.sh
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
if [ "$(hostname -s)" = "einstein" ]; then echo "refusing to run on einstein (head node)"; exit 1; fi
SRC=$(cd "$(dirname "$0")" && pwd)
DST=/home/scratch/jdochoa/envs/herwig
mkdir -p "$DST" /home/scratch/jdochoa/cache/rattler
cp "$SRC/pixi.toml" "$DST/"
[ -f "$SRC/pixi.lock" ] && cp "$SRC/pixi.lock" "$DST/"
cd "$DST"
echo "$(date -Is) pixi install start"
PIXI_CACHE_DIR=/home/scratch/jdochoa/cache/rattler nice -n 19 ionice -c3 /usr/bin/time -v pixi install 2>&1 | tail -30
echo "$(date -Is) pixi install end"
if [ ! -f "$SRC/pixi.lock" ]; then cp "$DST/pixi.lock" "$SRC/pixi.lock.part"; mv "$SRC/pixi.lock.part" "$SRC/pixi.lock"; fi
E=$DST/.pixi/envs/default
"$E/bin/Herwig" --version || true
ls "$E/share/Herwig" | head
printf 'host=%s\ndate=%s\nlock_sha256=%s\nenv_size=%s\n' "$(hostname -s)" "$(date -Is)" \
  "$(sha256sum "$DST/pixi.lock" | cut -d' ' -f1)" "$(du -sh "$E" | cut -f1)" > "$DST/INSTALLED.part"
mv "$DST/INSTALLED.part" "$DST/INSTALLED"; cat "$DST/INSTALLED"
