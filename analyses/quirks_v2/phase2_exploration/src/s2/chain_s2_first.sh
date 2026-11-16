#!/bin/bash
# chain_s2_first.sh -- channel (ii) (Sebastian): queue the first S2 campaigns on ONE node, one job at a time, after the
# node's other short campaign (channel (iii) p2-c-t-g4 on landau) has finished.  Runs detached on the worker
# (light bash: a directory test every 60 s, then the runner's own driver and bash watcher).
# Usage (from einstein): ssh -x landau 'setsid nohup bash .../chain_s2_first.sh landau > /home/scratch/jdochoa/drivers/chain_s2_first.log 2>&1 &'
set -u
NODE=${1:-landau}
R=/home/users/jdochoa/hllhc-quirks-search/tools/runner
C=/home/users/jdochoa/hllhc-quirks-search/tools/campaigns/p2-b
echo "$(date '+%F %T %z') chain start on $NODE"
while ls -d /home/scratch/jdochoa/p2-c-t-g4* >/dev/null 2>&1; do sleep 60; done
echo "$(date '+%F %T %z') p2-c-t-g4 dirs gone"
for camp in p2-b-s2-mlmtime p2-b-s2-kval p2-b-s2-kscan; do
  echo "$(date '+%F %T %z') launch $camp"
  "$R/bin/qv2run" ssh launch "$C/$camp.json" --nodes "$NODE" --max-per-node 1 --on "$NODE"
  sleep 30
  "$R/bin/qv2-watch" "$C/$camp.json" 60 300
  echo "$(date '+%F %T %z') $camp watcher exit $?"
done
echo "$(date '+%F %T %z') chain end"
