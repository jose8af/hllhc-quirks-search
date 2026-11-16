#!/bin/bash
# queue_maxwell1.sh <campaign.json>... -- channel (ii) on maxwell under the orchestrator's 12:58 ruling (ONE light slot):
# first the node-local Herwig/Resummino install (install slot; pgrep check of all workers), then the campaigns in order,
# one job at a time.
set -u
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
H=/home/users/jdochoa/hllhc-quirks-search/analyses/quirks_v2/phase2_exploration/src/herwig
echo "$(date '+%F %T %z') start"
busy=0
for n in landau maxwell schrodinger; do
  if ssh -x -o BatchMode=yes $n "pgrep -af 'pixi (install|add)' | grep -v pgrep" | grep -q pixi; then busy=1; echo "pixi install running on $n: skip install"; fi
done
if [ $busy = 0 ]; then
  echo "$(date '+%F %T %z') install start"; timeout 14400 bash "$H/install_herwig_local.sh"; echo "$(date '+%F %T %z') install exit $?"
fi
for c in "$@"; do
  echo "$(date '+%F %T %z') launch $c"
  "$R/bin/qv2run" ssh launch "$c" --nodes maxwell --max-per-node 1 --on maxwell; sleep 30
  "$R/bin/qv2-watch" "$c" 60 300; echo "$(date '+%F %T %z') $c watcher exit $?"
done
echo "$(date '+%F %T %z') queue_maxwell1 end"
