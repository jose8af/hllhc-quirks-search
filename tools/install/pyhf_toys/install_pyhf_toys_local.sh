#!/usr/bin/env bash
# install_pyhf_toys_local.sh -- pyhf 0.7.6 + jax (CPU) + iminuit on THIS worker's local disk, node-local package cache;
# nothing written to NFS except the small solved lock copied back next to this script (pattern of install_g4_local.sh).
# Usage (on schrodinger, never on einstein; only while holding the study's install slot):
#   nice -n 19 bash /home/users/jdochoa/hllhc-quirks-search/tools/install/pyhf_toys/install_pyhf_toys_local.sh
set -euo pipefail
. /home/users/jdochoa/hllhc-quirks-search/tools/env.sh
if [ "$(hostname -s)" = "einstein" ]; then echo "refusing to run on einstein (head node)"; exit 1; fi
SRC=$(cd "$(dirname "$0")" && pwd)
DST=/home/scratch/jdochoa/envs/pyhf_toys
mkdir -p "$DST" /home/scratch/jdochoa/cache/rattler
cp "$SRC/pixi.toml" "$DST/"
[ -f "$SRC/pixi.lock" ] && cp "$SRC/pixi.lock" "$DST/"
cd "$DST"
echo "$(date -Is) pixi install start"
FROZEN=""; [ -f "$SRC/pixi.lock" ] && FROZEN="--frozen"
PIXI_CACHE_DIR=/home/scratch/jdochoa/cache/rattler nice -n 19 ionice -c3 /usr/bin/time -v pixi install $FROZEN 2>&1 | tail -25
echo "$(date -Is) pixi install end"
if [ ! -f "$SRC/pixi.lock" ]; then cp "$DST/pixi.lock" "$SRC/pixi.lock.part"; mv "$SRC/pixi.lock.part" "$SRC/pixi.lock"; fi
E=$DST/.pixi/envs/default
PYTHONDONTWRITEBYTECODE=1 "$E/bin/python" -I -c "import pyhf, jax, jaxlib, iminuit, scipy, numpy; print('pyhf', pyhf.__version__, 'jax', jax.__version__, 'jaxlib', jaxlib.__version__, 'iminuit', iminuit.__version__, 'scipy', scipy.__version__, 'numpy', numpy.__version__)"
printf 'host=%s\ndate=%s\nlock_sha256=%s\nenv_size=%s\n' "$(hostname -s)" "$(date -Is)" \
  "$(sha256sum "$DST/pixi.lock" | cut -d' ' -f1)" "$(du -sh "$E" | cut -f1)" > "$DST/INSTALLED.part"
mv "$DST/INSTALLED.part" "$DST/INSTALLED"; cat "$DST/INSTALLED"
